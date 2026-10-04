"""PD executor (merged, M1): ROUTE PLANNING + RUIN & RECREATE + MORNING KITS, with adaptive search, forecast hands and
finite-supply awareness.  Original work, Shawn404, 25 Sep 2026.  Pure Python, no numpy; engine semantics of
kaggriculture._apply_unit_action.

Base = design 1 (tools/pd/pd_exec_edf_kits.py, the best of the four M1 designs); additions measured on the WF31
executor harness with tools/tmp/pd_bench.py (24 PLAN + 16 US seats, same hands; held-out seats via --cache holdout):
  * adaptive search budget: ruin & recreate stops after rr_stall iterations without a strict improvement on loose
    turns; tight turns (pool not empty or < tight_slack route slack, from hour 1, >= 2 units) get tight_mult x the
    turn budget.
  * virtual units (cfg virt): at hour 0 the plan includes yesterday's number of hands (own history) at their predicted
    spawn tiles (engine rule) with one turn of delay; arriving hands take over their planned routes; virtual units
    not realised by virt_hours are dropped (jobs -> pool).  Commands are only ever issued for units that exist.
  * ruins seeded next to pool jobs on tight turns (rr_pool_seed).
  * speed: exact bounding-box pruning of insertion scans, full-state route snapshots (no re-evaluation on restore),
    per-route urgency flag, cheap RNG, O(1) kit maths in the kit-aware insertion.
  * finite supplies (cfg supply_aware): outstanding pickups per route are tracked; insertions / tail exchanges that
    need shed stock the other units' pickups already claim are infeasible; kit margins only out of surplus; a FEED /
    FERTILIZE blocked on an empty shed is handed to a unit that carries a spare.  A lone unit without forecast hands
    carries only what its next lone_h turns use (animals; supplies when short).  No effect when the shed is ample.
  * grafts tested and left off: lone-farmer hour-0 animal horizon (zones it4 / imitate; neutral once routes are
    planned jointly), land-day +1 hand (no land-day misses left).

What it is
  An online executor for a day's TASK LIST ({tile: [(op, arg), ...]} in logical order per tile; no timings, no unit
  assignment).  Every turn it looks only at the observable farm (tiles, unit positions, unit inventories, shed) and its
  own records, keeps one ROUTE per planned unit (an ordered list of task tiles), repairs / improves the routes with a
  bounded search, and emits one command per present unit.

Model
  * job = the pending chain of one tile today; service = chain length (+1 DIG / HARVEST when a PLANT / BUILD head sits on
    a weed or an occupied tile); needs = WHEAT per FEED, FERTILIZER per FERTILIZE, one animal per PLACE.
  * value = 1 per task + root cascade (PLANT: the crop's later tasks; PLACE: 3.3 tasks per remaining day) + critical
    bonuses (WATER on a plant unwatered yesterday or planted today -> it weeds tonight; FEED on an animal unfed yesterday
    -> it escapes tonight) + production at stake.  Deadline = hour 23 for everything (the engine refreshes after the
    hour-23 step); decaying harvests (past max_lifespan_step, -1 unit per 2 steps) carry a lateness cost per turn.
  * route duration = kit turns + travel (Manhattan, units never collide) + service.  Kit ("morning kit"): a unit on a
    shed-access tile pays one PICKUP turn per item type its route needs and does not carry (order-aware: collected
    fertiliser / harvested wheat earlier in the route count); away from the shed it detours to the nearest access tile
    first.  Feasible iff duration <= 24 - hour.
  * plan: root-first cheapest insertion, first-improvement local search (relocate, or-opt / 2-opt, tail exchange) and
    ruin & recreate, bounded by an evaluation budget per turn (safety time cap ls_time_ms, incl. pool insertion).
    Jobs that fit nowhere wait in a value-ordered pool; critical jobs may eject cheaper ones.
  * warm start: yesterday's served order per unit index seeds the routes (own history); own-history rescue of
    yesterday's missed WATER / FEED whose plant / animal dies tonight.
  * land: jobs on LOCKED tiles become schedulable the turn the quadrant is bought (idle units walk towards it).
  * animals: a PLACE job stays with the unit that carries its animal; others need free shed stock.

Honesty: never sees recorded timings, positions, unit assignments or future hires; unit counts come from the farm,
the hands forecast from its own previous day.
Interface:  ex = PDExecutor(cfg); ex.begin_day(day, tasks); acts = ex.act(view) every turn; ex.end_day().
  view = {'step', 'day', 'hour', 'tiles' (tiles[y][x]), 'units' ([(x, y)] farmer first), 'inv' ([dict]), 'shed'}
         (+ optional 'pending_buys' {animal: n}, 'harv_need' (items) - B5, see below).

B5 (CS build, 27 Sep 2026; every addition behind a cfg key whose default reproduces the routes above exactly):
  Read-only API for the other CS components (call after act() of the step; eta 0 = the unit's command at the NEXT step):
    route_ops(H)   -> [(unit, eta_turns, (x, y), op, arg)] for the ops the routes start within H turns (virtual units
                      included; unit >= ex.n_units = a forecast hand), from the _route_prefix_needs walk
    slack()        -> {unit: free turns left today after its route}  (cap - dur; an idle unit: turns left)
    pending_ops()  -> {op: count} over every chain still held (routes, pool, locked, reserved, collect sub-jobs)
    add_chain(tile, ops, replace=False) -> the chains / pool plumbing (_pd_fill / _pd_land_fill); the job enters the
                      pool (or the locked set) at the next act()
    note_buys({animal: n}) -> animals with a buy in flight (cfg nosupply_skip 'wait')
  cfg: 'margin_w' (kit wheat margin; 0 = kits sized to the leg), 'deliver' preset 'melons' / 'deliver_items'
    (melons-only same-day delivery), 'nosupply_skip' 'wait' (a PLACE whose animal has a pending buy waits in the pool),
    'split_collect' (herd job FEED+CARE+HARVEST / collect job COLLECT_FERTILIZER that a passing route can absorb) with
    'f_shed_w' (route cost per FERTILIZER unit drawn from the shed = weight on in-route fertiliser credit),
    'harv_batch' (cow / sheep harvested only at a full production unless it would overflow / is needed / late game),
    'kit_way' (first-leg kits: productive commands before the kit where the kit can be picked up on the way).
CS build-2 review (results/portable/cs_build2_review.txt; default off): cfg 'seed_hold' + view['hold_tiles'] - the jobs of
  those tiles (PLANTs whose seed the layer cannot deliver) wait outside the routes like a LOCKED tile's job.
"""
import random
import time
B = 10
NT = B * B
ACCESS_XY = ((4, 4), (5, 4), (4, 5), (5, 5))
ACCESS = frozenset((_q1197 * B + x for x, _q1197 in ACCESS_XY))
ACC_ORDER = tuple((_q1197 * B + x for x, _q1197 in ACCESS_XY))
D = [[abs(a % B - b % B) + abs(a // B - b // B) for b in range(NT)] for a in range(NT)]
ACC_NEAR = [min(sorted(ACCESS), key=lambda s, t=t: D[t][s]) for t in range(NT)]
ACC_D = [D[t][ACC_NEAR[t]] for t in range(NT)]
CENTER_D = ACC_D
NEG = -10 ** 9
SUPPLY_EASY = 200
NEAR = [sorted(range(NT), key=lambda b, a=a: (D[a][b], b)) for a in range(NT)]
RING = {_q974: [[b for b in NEAR[a] if 0 < D[a][b] <= _q974] for a in range(NT)] for _q974 in (1, 2, 3, 4)}
XY = [(t % B, t // B) for t in range(NT)]

class _Sub(int):
    """B5 split_collect: id of the COLLECT_FERTILIZER sub-job of animal tile t.  Its integer value IS the tile (so the
    geometry tables D / XY / NEAR, tiles[t // B][t % B] and _step work unchanged, also in pd_layer, which reads
    ex.routes[u].tl / ex.chains with tile arithmetic); equality is type-strict and the hash distinct, so it is a
    separate key in chains / jobs / where / pool and a separate element in route lists."""
    __slots__ = ()

    def __eq__(_q1052, _q857):
        return type(_q857) is _Sub and int.__eq__(_q1052, _q857)

    def __ne__(_q1052, _q857):
        return not (type(_q857) is _Sub and int.__eq__(_q1052, _q857))

    def __hash__(_q1052):
        return NT + int(_q1052)

    def __repr__(_q1052):
        return 'S%d' % int(_q1052)
SUBS = [_Sub(t) for t in range(NT)]
NEARS = [[x for b in NEAR[a] for x in (b, SUBS[b])] for a in range(NT)]
HARV_BATCH = {'COW': 3, 'SHEEP': 4}
ANIMAL_ITEM = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}
DELIVER_PRESETS = {'melons': {'items': ('MELON',), 'h0': 8, 'h1': 20, 'kmin': 4}}
CROPS = {'WHEAT': {'first_yield_day': 2, 'max_yield_day': 4, 'interval': 0, 'max_yield': 6, 'ongoing': False}, 'CARROT': {'first_yield_day': 2, 'max_yield_day': 3, 'interval': 0, 'max_yield': 4, 'ongoing': False}, 'TOMATO': {'first_yield_day': 8, 'max_yield_day': 8, 'interval': 1, 'max_yield': 4, 'ongoing': True}, 'STRAWBERRY': {'first_yield_day': 10, 'max_yield_day': 10, 'interval': 2, 'max_yield': 4, 'ongoing': True}, 'MELON': {'first_yield_day': 10, 'max_yield_day': 12, 'interval': 0, 'max_yield': 6, 'ongoing': False}}
STRUCT = {'GOOSE': 'COOP', 'COW': 'PASTURE', 'SHEEP': 'PASTURE'}
ANIMAL_INFO = {'GOOSE': (4, 1, 4), 'COW': (8, 2, 6), 'SHEEP': (6, 3, 6)}
ANIMALS = ('GOOSE', 'COW', 'SHEEP')
BUILD_OPS = ('BUILD_PASTURE', 'BUILD_COOP')
PLANT_CASCADE = {'WHEAT': 5.0, 'CARROT': 4.0, 'MELON': 12.0, 'TOMATO': 20.0, 'STRAWBERRY': 20.0}
DEFAULT_CFG = {'ls_budget': 6000, 'ls_time_ms': 18.0, 'warm': True, 'recover': True, 'prepos': True, 'margin_w': 2, 'margin_f': 1, 'fresh_on_arrival': False, 'reserve_hours': 3, 'crit_thresh': 4.0, 'tail_x': True, 'late_w': 0.5, 'prod_w': 1.0, 'prod_wheat': 0.3, 'prices': None, 'price_ref': 60.0, 'price_cap': 4.0, 'credit': True, 'rescue': True, 'prune_r': 0, 'nosupply_skip': True, 'rr': True, 'rr_budget': 15000, 'turn_budget': 30000, 'budget_full_cap': 10, 'rr_lmax': 6, 'rr_routes': 3, 'rr_stall': 40, 'rr_stall_per_job': 0.0, 'stall_loose_only': True, 'tight_mult': 2.0, 'tight_slack': 0.1, 'tight_min_hour': 1, 'tight_mult_h0': 1.5, 'tight_min_units': 2, 'eval_charge': 0, 'rr_pool_seed': 0.5, 'virt': True, 'virt_hours': 3, 'virt_max': 20, 'supply_aware': True, 'bb_prune': True, 'lone_h': 4, 'h0_animal_h': 0, 'early_items': None, 'early_urg': 0.0, 'cap_cut': 0, 'rot_full': False, 'deliver': None, 'deliver_items': None, 'split_collect': False, 'split_val': 0.0, 'f_shed_w': 0.0, 'harv_batch': None, 'harv_last_day': 28, 'harv_need': None, 'kit_way': None, 'seed_hold': False, 'water_split': False, 'water_guard': False, 'eject_multi': 0, 'dlv_slack_until': None, 'ret_leg': False}

def _step(_q888, t):
    """One Manhattan step from tile p towards tile t (x first)."""
    px, _q960 = (_q888 % B, _q888 // B)
    _q1144, _q1145 = (t % B, t // B)
    if px < _q1144:
        return 'EAST'
    if px > _q1144:
        return 'WEST'
    if _q960 < _q1145:
        return 'SOUTH'
    if _q960 > _q1145:
        return 'NORTH'
    return None

def head_state(tile, op, arg, day, recover=True):
    """'ok' executable now | 'dig' / 'harvest' = one clearing command first | 'moot' | 'locked'."""
    if tile == 'LOCKED':
        return 'locked'
    _q673 = isinstance(tile, dict)
    kind = tile.get('kind') if _q673 else None
    if op == 'WATER':
        return 'ok' if kind == 'PLANT' and (not tile.get('watered_today')) else 'moot'
    if op == 'HARVEST':
        if not _q673 or tile.get('yield_units', 0) <= 0:
            return 'moot'
        if kind == 'PLANT' and day - tile.get('planted_day', day) < CROPS[tile['crop']]['first_yield_day']:
            return 'moot'
        return 'ok'
    if op == 'FERTILIZE':
        return 'ok' if kind == 'PLANT' else 'moot'
    if op == 'FEED':
        return 'ok' if _q673 and tile.get('animal') and (not tile.get('fed_today')) else 'moot'
    if op == 'CARE':
        return 'ok' if _q673 and tile.get('animal') and (not tile.get('cared_today')) else 'moot'
    if op == 'COLLECT_FERTILIZER':
        return 'ok' if _q673 and tile.get('animal') and tile.get('fertilizer_available') else 'moot'
    if op == 'PLACE':
        if _q673 and kind == STRUCT.get(arg) and (not tile.get('animal')):
            return 'ok'
        return 'moot'
    if op == 'DIG':
        return 'ok' if tile is not None and (not (_q673 and tile.get('animal'))) else 'moot'
    if op == 'PLANT' or op in BUILD_OPS:
        if tile is None:
            return 'ok'
        if kind == 'WEED':
            return 'dig'
        if not recover or (_q673 and tile.get('animal')):
            return 'moot'
        if kind == 'PLANT':
            _q421 = CROPS[tile['crop']]
            if not _q421['ongoing'] and tile.get('yield_units', 0) > 0 and (day - tile.get('planted_day', day) >= _q421['first_yield_day']):
                return 'harvest'
            return 'dig'
        if kind in ('COOP', 'PASTURE'):
            if op == 'BUILD_COOP' and kind == 'COOP' or (op == 'BUILD_PASTURE' and kind == 'PASTURE'):
                return 'moot'
            return 'dig'
        return 'moot'
    return 'ok'

class Job:
    __slots__ = ('t', 'chain', 's', 'w', 'f', 'a', 'val', 'crit', 'urg', 'pre', 'dw', 'df')

    def __init__(_q1052, t, chain):
        _q1052.t = t
        _q1052.chain = chain
        _q1052.s = len(chain)
        _q1052.w = 0
        _q1052.f = 0
        _q1052.a = None
        _q1052.val = 1.0
        _q1052.crit = False
        _q1052.urg = 0.0
        _q1052.pre = None
        _q1052.dw = 0
        _q1052.df = 0

class Route:
    __slots__ = ('tl', 'W', 'F', 'A', 'inner', 'serv', 'dur', 'kt', 'sp', 'cw', 'pmw', 'smw', 'cf', 'pmf', 'smf', 'nW', 'nF', 'bb', 'ug', 'oW', 'oF')

    def __init__(_q1052):
        _q1052.tl = []
        _q1052.W = 0
        _q1052.F = 0
        _q1052.A = {}
        _q1052.inner = 0
        _q1052.serv = 0
        _q1052.dur = 0
        _q1052.kt = 0
        _q1052.sp = -1
        _q1052.cw = []
        _q1052.pmw = [0]
        _q1052.smw = [NEG]
        _q1052.cf = []
        _q1052.pmf = [0]
        _q1052.smf = [NEG]
        _q1052.nW = 0
        _q1052.nF = 0
        _q1052.bb = (0, 9, 0, 9)
        _q1052.ug = False
        _q1052.oW = 0
        _q1052.oF = 0
_SNAP = ('W', 'F', 'A', 'inner', 'serv', 'dur', 'kt', 'sp', 'cw', 'pmw', 'smw', 'cf', 'pmf', 'smf', 'nW', 'nF', 'bb', 'ug', 'oW', 'oF')

def _snap(_q970):
    """Route state for an exact restore: _eval replaces (never mutates) the aggregate lists / dicts, so references
    suffice; the tile list is mutated in place and is copied."""
    return (list(_q970.tl), _q970.W, _q970.F, _q970.A, _q970.inner, _q970.serv, _q970.dur, _q970.kt, _q970.sp, _q970.cw, _q970.pmw, _q970.smw, _q970.cf, _q970.pmf, _q970.smf, _q970.nW, _q970.nF, _q970.bb, _q970.ug, _q970.oW, _q970.oF)

def _restore(_q970, _q1076):
    _q970.tl, _q970.W, _q970.F, _q970.A, _q970.inner, _q970.serv, _q970.dur, _q970.kt, _q970.sp, _q970.cw, _q970.pmw, _q970.smw, _q970.cf, _q970.pmf, _q970.smf, _q970.nW, _q970.nF, _q970.bb, _q970.ug, _q970.oW, _q970.oF = _q1076

def _addA(A, a, _q1062=1):
    if not a:
        return A
    _q2 = dict(A)
    for k, _q1159 in a.items():
        n = _q2.get(k, 0) + _q1062 * _q1159
        if n:
            _q2[k] = n
        else:
            _q2.pop(k, None)
    return _q2

class PDExecutor:

    def __init__(_q1052, cfg=None):
        _q1052.cfg = dict(DEFAULT_CFG)
        if cfg:
            _q1052.cfg.update(cfg)
        _q1052.day = -1
        _q1052.template = {}
        _q1052.missed_prev = {}
        _q1052.is_tight = False
        _q1052.eval_charge = _q1052.cfg['eval_charge']
        _q1052.prev_hands = 0
        _q1052.n_plan = 0
        _q1052.n_units = 0
        _q1052.max_units = 0
        _q1052.delay = []
        _q1052.outW = _q1052.outF = 0
        _q1052.supply_on = False
        _q1052.shed = {}
        _q1052.invW, _q1052.invF, _q1052.invA = ([], [], [])
        _q1052.dlv_t = {}
        _q1052.dlv_on = set()
        _q1052.cur_inv = []
        _q1052.stats = {'evals': 0, 'replans': 0, 'fresh_wins': 0, 'ejects': 0, 'detours': 0, 'recover': 0, 'overflow_drops': 0, 'ls_moves': 0, 'rr_iter': 0, 'rr_acc': 0, 'rescue_jobs': 0, 'nosupply': 0}
        _q498 = _q1052.cfg.get('deliver')
        if isinstance(_q498, str):
            _q498 = DELIVER_PRESETS.get(_q498)
        if _q498 and _q1052.cfg.get('deliver_items'):
            _q498 = dict(_q498, items=tuple(_q1052.cfg['deliver_items']))
        _q1052.dlv_cfg = _q498
        _q1052.split_on = bool(_q1052.cfg.get('split_collect'))
        if _q1052.split_on and _q1052.cfg.get('split_collect') != 'free':
            _q1052._best_insert = _q1052._best_insert_split
        _q1052.fb = float(_q1052.cfg.get('f_shed_w') or 0.0)
        if _q1052.fb:
            _q1052._cost = _q1052._cost_fb
            _q1052._best_insert_kit = _q1052._best_insert_kit_fb
        hb = _q1052.cfg.get('harv_batch')
        _q1052.hb = dict(HARV_BATCH) if hb is True else dict(hb) if hb else None
        _q713 = _q1052.cfg.get('kit_way') or None
        _q1052.kw = 'way' if _q713 is True else _q713
        _q1052.wait_on = _q1052.cfg.get('nosupply_skip') == 'wait'
        _q1052.pending_buys = {}
        _q1052.harv_need = frozenset(_q1052.cfg.get('harv_need') or ())
        _q1052.held = frozenset()
        _q1052.chains = {}
        _q1052.jobs = {}
        _q1052.routes = []
        _q1052.where = {}
        _q1052.pool = set()
        _q1052.locked = set()
        _q1052.res_set = set()
        _q1052._svc = set()
        _q1052._snap = None
        _q1052._hb_new = set()
        _q1052.ret = False
        _q1052.tiles = None

    def begin_day(_q1052, day, tasks):
        """tasks: {(x, y): [(op, arg), ...]} - today's task list (logical order per tile, nothing else)."""
        _q1052.day = day
        _q1052.chains = {}
        for (x, _q1197), ts in tasks.items():
            if ts:
                _q1052.chains[_q1197 * B + x] = [tuple(t) for t in ts]
        if _q1052.split_on:
            for t in list(_q1052.chains):
                _q1052._split_one(t)
        _q1052._svc = set()
        _q1052._snap = None
        _q1052._hb_new = set()
        _q1052.jobs = {}
        _q1052.routes = []
        _q1052.where = {}
        _q1052.pool = set()
        _q1052.locked = set()
        _q1052.reserved = {}
        _q1052.res_set = set()
        _q1052.served = {}
        _q1052.n_units = 0
        _q1052.n_plan = 0
        _q1052.max_units = 0
        _q1052.hour = -1
        _q1052.started = False
        _q1052.is_tight = False
        _q1052.eval_charge = _q1052.cfg['eval_charge']
        _q1052.dlv_t = {}
        _q1052.dlv_on = set()

    def end_day(_q1052):
        """Keep today's served order per unit index as tomorrow's warm-start template, and the WATER / FEED tasks
        this executor did not do today (its own record) for tomorrow's rescue check."""
        _q1052.template = {_q1147: list(tl) for _q1147, tl in _q1052.served.items() if tl}
        _q1052.prev_hands = max(0, _q1052.max_units - 1)
        mp = {}
        for t, _q428 in _q1052.chains.items():
            ops = {op for op, _ in _q428 if op in ('WATER', 'FEED')}
            if ops:
                mp[t] = ops
        _q1052.missed_prev = mp

    def _add_rescues(_q1052, tiles):
        """A WATER / FEED this executor missed yesterday leaves the plant / animal one miss from dying tonight.  If
        today's list has no such op on that tile (the plan skips it today) and the tile is not cleared today, add one
        auxiliary op (flagged arg '_aux'; the command is issued without it)."""
        for t, ops in _q1052.missed_prev.items():
            tile = tiles[t // B][t % B]
            if not isinstance(tile, dict):
                continue
            _q428 = _q1052.chains.get(t, [])
            _q452 = [op for op, _ in _q428]
            if 'WATER' in ops and tile.get('kind') == 'PLANT' and (tile.get('consecutive_unwatered', 0) >= 1) and ('WATER' not in _q452) and ('PLANT' not in _q452) and ('DIG' not in _q452):
                _q421 = CROPS.get(tile.get('crop'))
                if _q421 and (not _q421['ongoing']) and ('HARVEST' in _q452):
                    continue
                _q1052.chains[t] = [('WATER', '_aux')] + _q428
                _q1052.stats['rescue_jobs'] += 1
            elif 'FEED' in ops and tile.get('animal') and (tile.get('consecutive_unfed', 0) >= 1) and ('FEED' not in _q452):
                _q1052.chains[t] = [('FEED', '_aux')] + _q428
                _q1052.stats['rescue_jobs'] += 1

    def _split_one(_q1052, t):
        """split_collect: move the COLLECT_FERTILIZER ops of a mixed (animal) chain on tile t to the collect sub-job
        SUBS[t]; the herd job keeps FEED / CARE / HARVEST / ... in their order.  A collect-only chain stays whole."""
        if type(t) is _Sub:
            return
        _q428 = _q1052.chains.get(t)
        if not _q428 or len(_q428) < 2:
            return
        _q443 = [x for x in _q428 if x[0] == 'COLLECT_FERTILIZER']
        if not _q443 or len(_q443) == len(_q428):
            return
        _q1052.chains[t] = [x for x in _q428 if x[0] != 'COLLECT_FERTILIZER']
        s = SUBS[t]
        _q947 = _q1052.chains.get(s)
        _q1052.chains[s] = _q947 + _q443 if _q947 else _q443
        _q1052.stats['split_jobs'] = _q1052.stats.get('split_jobs', 0) + 1

    def _harv_filter(_q1052, tiles, _q703):
        """harv_batch: drop today's HARVEST of a batch animal (cow / sheep by default) holding fewer units than one full
        production, unless tonight's production would overflow max_held, the animal may escape tonight (unfed
        yesterday and no FEED in its chain), the product is needed now, or day >= harv_last_day."""
        hb = _q1052.hb
        if not hb or _q1052.day >= int(_q1052.cfg.get('harv_last_day') or 0):
            return
        need = _q1052.harv_need
        for t in _q703:
            _q428 = _q1052.chains.get(t)
            if not _q428 or not any((op == 'HARVEST' for op, _ in _q428)):
                continue
            tile = tiles[t // B][t % B]
            if not isinstance(tile, dict):
                continue
            _q336 = tile.get('animal')
            _q780 = hb.get(_q336) if _q336 else None
            if not _q780:
                continue
            _q1197 = tile.get('yield_units', 0)
            if _q1197 <= 0 or _q1197 >= _q780 or ANIMAL_ITEM.get(_q336) in need:
                continue
            _q574, _q678, cap = ANIMAL_INFO[_q336]
            _q511 = _q1052.day + 1 - tile.get('placed_day', _q1052.day) - _q574
            if _q511 >= 0 and _q511 % _q678 == 0 and (_q1197 + 1 + tile.get('pending_care_bonus', 0) > cap):
                continue
            if tile.get('consecutive_unfed', 0) >= 1 and (not tile.get('fed_today')) and (not any((op == 'FEED' for op, _ in _q428))):
                continue
            rest = [x for x in _q428 if x[0] != 'HARVEST']
            if rest:
                _q1052.chains[t] = rest
            else:
                _q1052.chains.pop(t, None)
            _q1052.stats['harv_skip'] = _q1052.stats.get('harv_skip', 0) + 1
            _q1052.stats['harv_skip_units'] = _q1052.stats.get('harv_skip_units', 0) + _q1197

    def note_buys(_q1052, pending):
        """{animal: n} bought and not yet in the shed (cfg nosupply_skip 'wait'); replaces the previous record."""
        _q1052.pending_buys = dict(pending or {})

    def add_chain(_q1052, tile, ops, _q988=False):
        """Add today's chain for a tile ((x, y) or index): appended to the tile's chain, or replacing it.  Same plumbing
        as pd_layer's _pd_fill / _pd_land_fill (ex.chains[t] = [...]); the job is (re)read at the next act(), which puts
        it into the pool, or into the locked set on a LOCKED tile.  Returns True if anything was added."""
        if isinstance(tile, (tuple, list)):
            t = int(tile[1]) * B + int(tile[0])
        else:
            t = int(tile)
        if not 0 <= t < NT:
            return False
        new = []
        for x in ops or ():
            if isinstance(x, str):
                new.append((x, None))
            else:
                x = tuple(x)
                new.append((x[0], x[1] if len(x) > 1 else None))
        if not new:
            return False
        _q428 = _q1052.chains.get(t)
        if _q428 and (not _q988):
            _q428.extend(new)
        else:
            _q1052.chains[t] = new
        if _q1052.split_on:
            _q1052._split_one(t)
        if _q1052.hb:
            _q1052._hb_new.add(t)
        return True

    def pending_ops(_q1052):
        """{op: count} of every op still held in today's chains (routes, pool, locked, reserved, collect sub-jobs)."""
        c = {}
        for _q428 in _q1052.chains.values():
            for op, _ in _q428:
                c[op] = c.get(op, 0) + 1
        return c

    def slack(_q1052):
        """{unit: free turns} after this step's commands: turns left today minus the rest of the unit's route
        (cap - dur of the route as planned at command time; an idle unit: the turns left).  Virtual (forecast) units
        are included (unit >= n_units)."""
        if not _q1052._snap:
            return {}
        cap, rows = _q1052._snap
        return {_q1147: max(0, cap - _q475 if ne else cap - 1) for _q1147, (_q475, ne) in enumerate(rows)}

    def route_ops(_q1052, H, _q946=False):
        """[(unit, eta, (x, y), op, arg)] for the ops the routes start within H turns (eta < H), eta counted from the
        NEXT step (0 = the unit's command at step t+1 when called after act() of step t).  The _route_prefix_needs walk
        over the route model of this step (kit turns, travel, one turn per op; a clearing DIG / HARVEST before a
        PLANT / BUILD is listed as that op with arg None).  Virtual units are included unless present_only."""
        _q880 = []
        _q1104 = _q1052._svc
        jobs = _q1052.jobs
        chains = _q1052.chains
        U = _q1052.n_units if _q946 else len(_q1052.routes)
        for _q1147 in range(min(U, len(_q1052.routes))):
            _q970 = _q1052.routes[_q1147]
            if not _q970.tl:
                continue
            _q1140 = _q970.kt - (0 if _q1147 in _q1104 else 1)
            _q888 = _q970.sp
            for t in _q970.tl:
                _q681 = jobs.get(t)
                _q428 = chains.get(t)
                if _q681 is None or not _q428:
                    continue
                _q1140 += D[_q888][t]
                _q888 = t
                if _q1140 >= H:
                    break
                _q1123 = int(t)
                xy = (_q1123 % B, _q1123 // B)
                _q520 = _q1140
                if _q681.pre in ('dig', 'harvest'):
                    _q880.append((_q1147, max(0, _q520), xy, 'DIG' if _q681.pre == 'dig' else 'HARVEST', None))
                    _q520 += 1
                for op, arg in _q428:
                    if _q520 >= H:
                        break
                    _q880.append((_q1147, max(0, _q520), xy, op, None if arg == '_aux' else arg))
                    _q520 += 1
                _q1140 += _q681.s
        return _q880

    def _job_value(_q1052, _q681, tile):
        rem = max(0, 29 - _q1052.day)
        _q1159 = 0.0
        crit = False
        ops = [op for op, _ in _q681.chain]
        for op, arg in _q681.chain:
            _q1159 += 1.0
            if op == 'PLANT':
                _q1159 += min(PLANT_CASCADE.get(arg, 5.0), 1.2 * rem)
                crit = True
            elif op == 'PLACE':
                _q1159 += 3.3 * rem
                crit = True
            elif op == 'HARVEST':
                if isinstance(tile, dict) and tile.get('crop', 'X') != 'WHEAT':
                    _q1159 += 1.0
        urg = 0.0
        if isinstance(tile, dict):
            k = tile.get('kind')
            if k == 'PLANT':
                _q421 = CROPS[tile['crop']]
                age = _q1052.day - tile.get('planted_day', _q1052.day)
                if 'WATER' in ops and tile.get('consecutive_unwatered', 0) >= 1:
                    if _q421['ongoing']:
                        _q742 = _q421['first_yield_day'] + _q421['interval'] * _q421['max_yield'] + 1
                    else:
                        _q742 = _q421['max_yield_day'] + 1
                    _q1159 += max(1.0, 1.2 * (_q742 - age))
                    crit = True
                mls = tile.get('max_lifespan_step', -1)
                if 'HARVEST' in ops and 0 <= mls <= 24 * (_q1052.day + 1):
                    urg = 1.0
            elif tile.get('animal'):
                if 'FEED' in ops and tile.get('consecutive_unfed', 0) >= 1:
                    _q1159 += 3.3 * rem
                    crit = True
            _q527 = _q1052.cfg.get('early_items')
            if _q527 and 'HARVEST' in ops and (not urg):
                item = tile.get('crop') if k == 'PLANT' else {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}.get(tile.get('animal'))
                if item in _q527 and tile.get('yield_units', 0) > 0:
                    urg = float(_q1052.cfg.get('early_urg') or 0.0)
        _q681.crit = crit or _q1159 >= _q1052.cfg['crit_thresh'] * max(1, len(_q681.chain))
        pw = _q1052.cfg['prod_w']
        if pw:
            _q1159 += pw * _q1052._prod_units(_q681, tile, ops)
        _q681.val = _q1159
        _q681.urg = urg

    @staticmethod
    def _prod_night(_q421, tile, x):
        """Does an ongoing crop produce in the refresh after day x?"""
        _q511 = x + 1 - tile.get('planted_day', x) - _q421['first_yield_day']
        if _q511 < 0 or _q511 % _q421['interval']:
            return False
        return _q511 // _q421['interval'] + 1 <= _q421['max_yield']

    def _prod_units(_q1052, _q681, tile, ops):
        """Production units at stake if this job is skipped today (engine formulas; wheat down-weighted)."""
        if not isinstance(tile, dict):
            return 0.0
        day = _q1052.day
        units = 0.0
        if tile.get('kind') == 'PLANT':
            crop = tile['crop']
            _q421 = CROPS[crop]
            _q787 = _q1052.cfg['prod_wheat'] if crop == 'WHEAT' else 1.0
            if _q1052.cfg['prices']:
                _q787 = _q1052._pw(crop)
            _q912 = tile.get('planted_day', day)
            age = day - _q912
            _q598 = tile.get('fertilized_until_day', -1)
            _q564 = _q598 >= day or 'FERTILIZE' in ops
            _q1190 = (_q421['max_yield_day'] + 1) // 2
            if 'WATER' in ops and (not tile.get('watered_today')):
                if not _q421['ongoing']:
                    if _q1190 <= age <= _q421['max_yield_day'] and tile.get('yield_units', 0) < _q421['max_yield']:
                        units += 2.0 if _q564 else 1.0
                elif _q564 and _q1052._prod_night(_q421, tile, day):
                    units += 1.0
            if 'FERTILIZE' in ops:
                for x in (day, day + 1, day + 2):
                    if x <= _q598:
                        continue
                    if _q421['ongoing']:
                        if _q1052._prod_night(_q421, tile, x):
                            units += 1.0
                    elif _q1190 <= x - _q912 <= _q421['max_yield_day']:
                        units += 1.0
            if 'HARVEST' in ops:
                _q1197 = tile.get('yield_units', 0)
                if _q421['ongoing']:
                    _q856 = (2 if _q564 else 1) if _q1052._prod_night(_q421, tile, day) else 0
                    units += max(0, _q1197 + _q856 - _q421['max_yield'])
                else:
                    mls = tile.get('max_lifespan_step', -1)
                    if 0 <= mls <= 24 * (day + 1):
                        if _q1052.cfg.get('rot_full') and mls <= 24 * day + getattr(_q1052, 'hour', 0):
                            units += float(_q1197)
                        else:
                            units += 0.5 * _q1197
            return units * _q787
        _q336 = tile.get('animal')
        if _q336:
            _q574, _q678, cap = ANIMAL_INFO[_q336]
            _q511 = day + 1 - tile.get('placed_day', day) - _q574
            prod = _q511 >= 0 and _q511 % _q678 == 0
            fed = tile.get('fed_today') or 'FEED' in ops
            if 'CARE' in ops and (not tile.get('cared_today')) and fed:
                units += 1.0
            if prod and 'FEED' in ops and (not tile.get('fed_today')):
                units += tile.get('pending_care_bonus', 0)
            if 'HARVEST' in ops:
                _q1197 = tile.get('yield_units', 0)
                units += max(0, _q1197 + (1 + tile.get('pending_care_bonus', 0) if prod else 0) - cap)
            if _q1052.cfg['prices']:
                _q953 = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}.get(_q336)
                units *= _q1052._pw(_q953)
                if 'COLLECT_FERTILIZER' in ops and tile.get('fertilizer_available'):
                    units += _q1052._pw('FERTILIZER')
        return units

    def _pw(_q1052, item):
        """Price weight of one unit of item (M2: quote / price_ref, capped)."""
        px = _q1052.cfg['prices'].get(item)
        if not px:
            return 1.0
        return min(_q1052.cfg['price_cap'], float(px) / _q1052.cfg['price_ref'])

    def _refresh_job(_q1052, t, tiles):
        """Drop moot heads; recompute service / needs / value.  Returns the Job or None (chain done)."""
        _q428 = _q1052.chains.get(t)
        tile = tiles[t // B][t % B]
        rec = _q1052.cfg['recover']
        pre = None
        while _q428:
            st = head_state(tile, _q428[0][0], _q428[0][1], _q1052.day, rec)
            if st == 'moot':
                _q428.pop(0)
                continue
            if st != 'ok':
                pre = st
            break
        if not _q428:
            _q1052.chains.pop(t, None)
            return None
        _q681 = _q1052.jobs.get(t)
        if _q681 is None:
            _q681 = Job(t, _q428)
            _q1052.jobs[t] = _q681
        _q681.chain = _q428
        _q681.pre = pre
        _q681.s = len(_q428) + (1 if pre in ('dig', 'harvest') else 0)
        w = f = 0
        a = None
        for op, arg in _q428:
            if op == 'FEED':
                w += 1
            elif op == 'FERTILIZE':
                f += 1
            elif op == 'PLACE':
                if a is None:
                    a = {}
                a[arg] = a.get(arg, 0) + 1
        _q681.w, _q681.f, _q681.a = (w, f, a)
        sw = _q1054 = 0
        if _q1052.cfg['credit'] and isinstance(tile, dict):
            if tile.get('animal'):
                if tile.get('fertilizer_available'):
                    _q1054 = sum((1 for op, _ in _q428 if op == 'COLLECT_FERTILIZER'))
            elif tile.get('kind') == 'PLANT' and tile.get('crop') == 'WHEAT' and any((op == 'HARVEST' for op, _ in _q428)):
                sw = max(0, tile.get('yield_units', 0) - 1)
        _q681.dw = w - sw
        _q681.df = f - _q1054
        _q1052._job_value(_q681, tile)
        if _q1052.split_on and type(t) is _Sub and _q1052.cfg.get('split_val'):
            _q681.val += float(_q1052.cfg['split_val'])
        return _q681

    def _kit(_q1052, _q1147, W, F, A):
        """(kit turns, start tile) for a route with needs W / F / A for unit u."""
        kt = _q1052.dlv_t.get(_q1147, 0) if _q1052.dlv_t else 0
        if W > _q1052.invW[_q1147]:
            kt += 1
        if F > _q1052.invF[_q1147]:
            kt += 1
        if A:
            _q654 = _q1052.invA[_q1147]
            for k, c in A.items():
                if c > _q654.get(k, 0):
                    kt += 1
        _q888 = _q1052.pos[_q1147]
        _q498 = _q1052.delay[_q1147]
        if kt:
            if _q888 in ACCESS:
                return (kt + _q498, _q888)
            return (ACC_D[_q888] + kt + _q498, ACC_NEAR[_q888])
        return (_q498, _q888)

    def _late(_q1052, _q1147, _q970):
        """Soft lateness cost of decaying harvests in route order."""
        _q759 = _q1052.cfg['late_w']
        if not _q759:
            return 0.0
        jobs = _q1052.jobs
        tl = _q970.tl
        c = 0.0
        _q1140 = _q970.kt
        _q888 = _q970.sp
        _q640 = False
        for t in tl:
            _q681 = jobs[t]
            _q1140 += D[_q888][t] + _q681.s
            _q888 = t
            if _q681.urg:
                c += _q759 * _q1140 * _q681.urg
                _q640 = True
        return c if _q640 else 0.0

    def _eval(_q1052, _q1147, _q970):
        """Full recomputation of a route's aggregates (incl. the order-aware kit prefix / suffix maxima)."""
        tl = _q970.tl
        jobs = _q1052.jobs
        W = F = S = I = 0
        A = {}
        _q947 = -1
        n = len(tl)
        _q1052.evals += _q1052.eval_charge * n
        cw = [0] * n
        cf = [0] * n
        pmw = [0] * (n + 1)
        pmf = [0] * (n + 1)
        _q317 = _q313 = 0
        _q762 = _q761 = 0
        ug = False
        for _q652, t in enumerate(tl):
            _q681 = jobs[t]
            if _q681.urg:
                ug = True
            W += _q681.w
            F += _q681.f
            S += _q681.s
            if _q681.a:
                for k, _q1159 in _q681.a.items():
                    A[k] = A.get(k, 0) + _q1159
            if _q947 >= 0:
                I += D[_q947][t]
            _q947 = t
            pmw[_q652] = _q762
            pmf[_q652] = _q761
            _q317 += _q681.dw
            _q313 += _q681.df
            cw[_q652] = _q317
            cf[_q652] = _q313
            if _q317 > _q762:
                _q762 = _q317
            if _q313 > _q761:
                _q761 = _q313
        pmw[n] = _q762
        pmf[n] = _q761
        smw = [NEG] * (n + 1)
        smf = [NEG] * (n + 1)
        for _q652 in range(n - 1, -1, -1):
            smw[_q652] = cw[_q652] if cw[_q652] > smw[_q652 + 1] else smw[_q652 + 1]
            smf[_q652] = cf[_q652] if cf[_q652] > smf[_q652 + 1] else smf[_q652 + 1]
        _q970.cw, _q970.pmw, _q970.smw, _q970.cf, _q970.pmf, _q970.smf = (cw, pmw, smw, cf, pmf, smf)
        _q970.nW, _q970.nF = (_q762, _q761)
        _q970.W, _q970.F, _q970.A, _q970.serv, _q970.inner = (W, F, A, S, I)
        _q970.ug = ug
        _q882 = _q762 - _q1052.invW[_q1147]
        if _q882 < 0:
            _q882 = 0
        _q866 = _q761 - _q1052.invF[_q1147]
        if _q866 < 0:
            _q866 = 0
        _q1052.outW += _q882 - _q970.oW
        _q1052.outF += _q866 - _q970.oF
        _q970.oW, _q970.oF = (_q882, _q866)
        if tl:
            kt, sp = _q1052._kit(_q1147, _q762, _q761, A)
            _q970.kt, _q970.sp = (kt, sp)
            _q970.dur = kt + D[sp][tl[0]] + I + S
            if _q1052.ret:
                _q970.dur += ACC_D[tl[-1]] + 1
            _q1191 = _q1192 = sp % B
            _q1198 = _q1199 = sp // B
            for t in tl:
                x, _q1197 = XY[t]
                if x < _q1191:
                    _q1191 = x
                elif x > _q1192:
                    _q1192 = x
                if _q1197 < _q1198:
                    _q1198 = _q1197
                elif _q1197 > _q1199:
                    _q1199 = _q1197
            _q970.bb = (_q1191, _q1192, _q1198, _q1199)
        else:
            _q888 = _q1052.pos[_q1147]
            _q970.kt, _q970.sp = (_q1052.delay[_q1147], _q888)
            _q970.dur = 0
            _q970.bb = (_q888 % B, _q888 % B, _q888 // B, _q888 // B)
        return _q970.dur

    def _cost(_q1052, _q1147, _q970):
        if not _q970.ug:
            return _q970.dur
        return _q970.dur + (_q1052._late(_q1147, _q970) if _q1052.cfg['late_w'] else 0.0)

    def _cost_fb(_q1052, _q1147, _q970):
        """_cost with the B5 f_shed_w objective: + fb per FERTILIZER unit the unit must draw from the shed (r.oF).
        Bound over _cost in __init__ when f_shed_w > 0."""
        if not _q970.ug:
            return _q970.dur + _q1052.fb * _q970.oF
        return _q970.dur + (_q1052._late(_q1147, _q970) if _q1052.cfg['late_w'] else 0.0) + _q1052.fb * _q970.oF

    def _animal_ok(_q1052, _q1147, _q681):
        """Can unit u get the animals of job j (carried spare, or free shed stock)?"""
        _q970 = _q1052.routes[_q1147]
        _q654 = _q1052.invA[_q1147]
        for k, c in _q681.a.items():
            spare = _q654.get(k, 0) - _q970.A.get(k, 0)
            if spare >= c:
                continue
            if _q1052.shed_free.get(k, 0) < c - max(0, spare):
                return False
        return True

    def _pinned(_q1052, _q1147, _q681):
        """A PLACE job stays with a unit that carries its animal."""
        if not _q681.a:
            return False
        _q654 = _q1052.invA[_q1147]
        return any((_q654.get(k, 0) > 0 for k in _q681.a))

    def _calc_shed_free(_q1052):
        _q1054 = {}
        for k in ANIMALS:
            _q489 = 0
            for _q1147, _q970 in enumerate(_q1052.routes):
                _q489 += max(0, _q970.A.get(k, 0) - _q1052.invA[_q1147].get(k, 0))
            _q1054[k] = _q1052.shed.get(k, 0) - _q489
        _q1052.shed_free = _q1054

    def _best_insert(_q1052, _q1147, _q681, cap=None):
        """Cheapest position for job j in route u -> (new_dur, k) or (None, None) if infeasible."""
        if _q681.a and (not _q1052._animal_ok(_q1147, _q681)):
            return (None, None)
        _q970 = _q1052.routes[_q1147]
        tl = _q970.tl
        n = len(tl)
        if cap is None:
            cap = _q1052.cap
        _q1052.evals += n + 1
        dw, df = (_q681.dw, _q681.df)
        if dw >= 0 and df >= 0 and (_q970.dur + _q681.s > cap):
            if dw or df:
                _q1052.evals += n + 1
            return (None, None)
        if dw or df:
            return _q1052._best_insert_kit(_q1147, _q681, _q970, _addA(_q970.A, _q681.a) if _q681.a else _q970.A, cap)
        t = _q681.t
        _q11 = D[t]
        if _q681.a:
            kt, sp = _q1052._kit(_q1147, _q970.nW, _q970.nF, _addA(_q970.A, _q681.a))
        else:
            kt, sp = (_q970.kt, _q970.sp)
        base = kt + _q970.inner + _q970.serv + _q681.s
        if n == 0:
            _q829 = base + D[sp][t]
            if _q1052.ret:
                _q829 += ACC_D[t] + 1
            return (_q829, 0) if _q829 <= cap else (None, None)
        _q10 = D[sp]
        t0 = tl[0]
        best = base + _q10[t] + _q11[t0]
        _q365 = 0
        base += _q10[t0]
        _q947 = t0
        _q9 = D[t0]
        _q503 = _q11[t0]
        for k in range(1, n):
            _q855 = tl[k]
            _q499 = _q11[_q855]
            c = base + _q503 + _q499 - _q9[_q855]
            if c < best:
                best, _q365 = (c, k)
            _q947 = _q855
            _q9 = D[_q855]
            _q503 = _q499
        c = base + _q503
        if _q1052.ret:
            best += ACC_D[tl[-1]] + 1
            c += ACC_D[t] + 1
        if c < best:
            best, _q365 = (c, n)
        if best <= cap:
            return (best, _q365)
        return (None, None)

    def _best_insert_split(_q1052, _q1147, _q681, cap=None):
        """split_collect (B5; bound over _best_insert in __init__): a collect job may go into its herd job's route, a
        route holding FERTILIZE jobs (the credit), or any route while its herd job is not routed."""
        t = _q681.t
        if type(t) is _Sub:
            _q649 = _q1052.where.get(int(t))
            if _q649 is not None and _q649 != _q1147 and (not _q1052.routes[_q1147].F):
                _q1052.evals += 1
                return (None, None)
        return PDExecutor._best_insert(_q1052, _q1147, _q681, cap)

    def _best_insert_kit(_q1052, _q1147, _q681, _q970, _q2, cap):
        """_best_insert for a job that changes the kit: exact order-aware start need per position (O(1) each)."""
        tl = _q970.tl
        n = len(tl)
        t = _q681.t
        dw, df = (_q681.dw, _q681.df)
        _q11 = D[t]
        base = _q970.inner + _q970.serv + _q681.s
        cw, pmw, smw, cf, pmf, smf = (_q970.cw, _q970.pmw, _q970.smw, _q970.cf, _q970.pmf, _q970.smf)
        _q669 = _q1052.invW[_q1147]
        _q668 = _q1052.invF[_q1147]
        _q698 = _q1052.dlv_t.get(_q1147, 0) if _q1052.dlv_t else 0
        if _q2:
            _q654 = _q1052.invA[_q1147]
            for _q692, _q396 in _q2.items():
                if _q396 > _q654.get(_q692, 0):
                    _q698 += 1
        _q888 = _q1052.pos[_q1147]
        _q498 = _q1052.delay[_q1147]
        _q661 = _q888 in ACCESS
        _q322 = ACC_D[_q888]
        _q1033 = _q1052.supply_on
        if _q1033:
            _q405 = _q1052.shed.get('WHEAT', 0) - _q1052.outW + _q970.oW + _q669
            _q404 = _q1052.shed.get('FERTILIZER', 0) - _q1052.outF + _q970.oF + _q668
        _q7 = D[ACC_NEAR[_q888]]
        _q8 = D[_q888]
        best, _q365 = (None, None)
        t0 = tl[0] if n else -1
        _q995 = _q1052.ret
        for k in range(n + 1):
            _q392 = cw[k - 1] if k else 0
            _q360 = cf[k - 1] if k else 0
            _q854 = pmw[k]
            x = _q392 + dw
            if x > _q854:
                _q854 = x
            x = smw[k] + dw
            if x > _q854:
                _q854 = x
            _q843 = pmf[k]
            x = _q360 + df
            if x > _q843:
                _q843 = x
            x = smf[k] + df
            if x > _q843:
                _q843 = x
            if _q1033 and (_q854 > _q669 and _q854 > _q405 and (_q854 > _q970.nW) or (_q843 > _q668 and _q843 > _q404 and (_q843 > _q970.nF))):
                continue
            kt = _q698 + _q498
            if _q854 > _q669:
                kt += 1
            if _q843 > _q668:
                kt += 1
            if kt > _q498 and (not _q661):
                kt += _q322
                _q10 = _q7
            else:
                _q10 = _q8
            if n == 0:
                c = kt + base + _q10[t]
            elif k == 0:
                c = kt + base + _q10[t] + _q11[t0]
            elif k == n:
                c = kt + base + _q10[t0] + _q11[tl[-1]]
            else:
                c = kt + base + _q10[t0] + _q11[tl[k - 1]] + _q11[tl[k]] - D[tl[k - 1]][tl[k]]
            if _q995:
                c += (ACC_D[t] if k == n else ACC_D[tl[-1]]) + 1
            if best is None or c < best:
                best, _q365 = (c, k)
        _q1052.evals += n + 1
        if best is not None and best <= cap:
            return (best, _q365)
        return (None, None)

    def _best_insert_kit_fb(_q1052, _q1147, _q681, _q970, _q2, cap):
        """_best_insert_kit with the f_shed_w objective (B5; bound over _best_insert_kit in __init__ when f_shed_w > 0):
        positions are ranked by duration + fb x the FERTILIZER the unit must draw from the shed; only positions whose
        duration fits cap are candidates.  Returns (biased new cost, k), where biased new cost - r.dur is the biased
        insertion delta (the route's cost is r.dur + fb * r.oF)."""
        fb = _q1052.fb
        tl = _q970.tl
        n = len(tl)
        t = _q681.t
        dw, df = (_q681.dw, _q681.df)
        _q11 = D[t]
        base = _q970.inner + _q970.serv + _q681.s
        cw, pmw, smw, cf, pmf, smf = (_q970.cw, _q970.pmw, _q970.smw, _q970.cf, _q970.pmf, _q970.smf)
        _q669 = _q1052.invW[_q1147]
        _q668 = _q1052.invF[_q1147]
        _q698 = _q1052.dlv_t.get(_q1147, 0) if _q1052.dlv_t else 0
        if _q2:
            _q654 = _q1052.invA[_q1147]
            for _q692, _q396 in _q2.items():
                if _q396 > _q654.get(_q692, 0):
                    _q698 += 1
        _q888 = _q1052.pos[_q1147]
        _q498 = _q1052.delay[_q1147]
        _q661 = _q888 in ACCESS
        _q322 = ACC_D[_q888]
        _q1033 = _q1052.supply_on
        if _q1033:
            _q405 = _q1052.shed.get('WHEAT', 0) - _q1052.outW + _q970.oW + _q669
            _q404 = _q1052.shed.get('FERTILIZER', 0) - _q1052.outF + _q970.oF + _q668
        _q7 = D[ACC_NEAR[_q888]]
        _q8 = D[_q888]
        _q861 = _q970.oF
        best, _q365 = (None, None)
        t0 = tl[0] if n else -1
        _q995 = _q1052.ret
        for k in range(n + 1):
            _q392 = cw[k - 1] if k else 0
            _q360 = cf[k - 1] if k else 0
            _q854 = pmw[k]
            x = _q392 + dw
            if x > _q854:
                _q854 = x
            x = smw[k] + dw
            if x > _q854:
                _q854 = x
            _q843 = pmf[k]
            x = _q360 + df
            if x > _q843:
                _q843 = x
            x = smf[k] + df
            if x > _q843:
                _q843 = x
            if _q1033 and (_q854 > _q669 and _q854 > _q405 and (_q854 > _q970.nW) or (_q843 > _q668 and _q843 > _q404 and (_q843 > _q970.nF))):
                continue
            kt = _q698 + _q498
            if _q854 > _q669:
                kt += 1
            if _q843 > _q668:
                kt += 1
            if kt > _q498 and (not _q661):
                kt += _q322
                _q10 = _q7
            else:
                _q10 = _q8
            if n == 0:
                c = kt + base + _q10[t]
            elif k == 0:
                c = kt + base + _q10[t] + _q11[t0]
            elif k == n:
                c = kt + base + _q10[t0] + _q11[tl[-1]]
            else:
                c = kt + base + _q10[t0] + _q11[tl[k - 1]] + _q11[tl[k]] - D[tl[k - 1]][tl[k]]
            if _q995:
                c += (ACC_D[t] if k == n else ACC_D[tl[-1]]) + 1
            if c > cap:
                continue
            _q418 = c + fb * ((_q843 - _q668 if _q843 > _q668 else 0) - _q861)
            if best is None or _q418 < best:
                best, _q365 = (_q418, k)
        _q1052.evals += n + 1
        if best is not None:
            return (best, _q365)
        return (None, None)

    def _remove_dur(_q1052, _q1147, _q652, _q362=True):
        _q970 = _q1052.routes[_q1147]
        tl = _q970.tl
        n = len(tl)
        if n == 1:
            return -_q1052.fb * _q970.oF if _q1052.fb and _q362 else 0
        t = tl[_q652]
        _q681 = _q1052.jobs[t]
        inner = _q970.inner
        if _q652 == 0:
            inner -= D[t][tl[1]]
            _q574 = tl[1]
        else:
            _q957 = tl[_q652 - 1]
            if _q652 == n - 1:
                inner -= D[_q957][t]
            else:
                _q855 = tl[_q652 + 1]
                inner += D[_q957][_q855] - D[_q957][t] - D[t][_q855]
            _q574 = tl[0]
        _q2 = _addA(_q970.A, _q681.a, -1) if _q681.a else _q970.A
        if _q681.dw or _q681.df:
            _q854 = _q970.pmw[_q652]
            x = _q970.smw[_q652 + 1] - _q681.dw
            if x > _q854:
                _q854 = x
            _q843 = _q970.pmf[_q652]
            x = _q970.smf[_q652 + 1] - _q681.df
            if x > _q843:
                _q843 = x
        else:
            _q854, _q843 = (_q970.nW, _q970.nF)
        kt, sp = _q1052._kit(_q1147, _q854, _q843, _q2)
        _q1010 = (ACC_D[tl[-2]] if _q652 == n - 1 else ACC_D[tl[-1]]) + 1 if _q1052.ret else 0
        if _q1052.fb and _q362 and (_q843 != _q970.nF):
            _q866 = _q843 - _q1052.invF[_q1147]
            return kt + D[sp][_q574] + inner + _q970.serv - _q681.s + _q1010 + _q1052.fb * ((_q866 if _q866 > 0 else 0) - _q970.oF)
        return kt + D[sp][_q574] + inner + _q970.serv - _q681.s + _q1010

    def _insert(_q1052, _q1147, t, k):
        _q970 = _q1052.routes[_q1147]
        _q970.tl.insert(k, t)
        _q1052._eval(_q1147, _q970)
        _q1052.where[t] = _q1147
        _q1052.pool.discard(t)

    def _remove(_q1052, _q1147, t):
        _q970 = _q1052.routes[_q1147]
        _q970.tl.remove(t)
        _q1052._eval(_q1147, _q970)
        _q1052.where.pop(t, None)

    def _timeout(_q1052):
        if _q1052.evals >= _q1052.budget_end:
            return True
        if time.perf_counter() >= _q1052.t_end:
            _q1052.tcap_hit = True
            return True
        return False

    def _cheapest(_q1052, t):
        _q681 = _q1052.jobs[t]
        _q942 = _q1052.cfg['prune_r']
        if _q942:
            _q401 = set()
            where = _q1052.where
            for _q1107 in RING[_q942][t]:
                _q1148 = where.get(_q1107)
                if _q1148 is not None:
                    _q401.add(_q1148)
            for _q1147 in range(_q1052.n_plan):
                _q970 = _q1052.routes[_q1147]
                if not _q970.tl or D[_q970.sp][t] <= _q942:
                    _q401.add(_q1147)
            if len(_q401) < _q1052.n_plan:
                best, _q381, _q365 = (None, None, None)
                for _q1147 in _q401:
                    _q829, k = _q1052._best_insert(_q1147, _q681)
                    if _q829 is None:
                        continue
                    c = _q829 - _q1052.routes[_q1147].dur
                    if best is None or c < best or (c == best and _q1147 < _q381):
                        best, _q381, _q365 = (c, _q1147, k)
                if _q381 is not None:
                    return (_q381, _q365)
        best, _q381, _q365 = (None, None, None)
        U = _q1052.n_plan
        routes = _q1052.routes
        if _q1052.cfg['bb_prune'] and U > 2 and (_q681.dw >= 0) and (_q681.df >= 0):
            _q1144, _q1145 = XY[t]
            _q873 = []
            for _q1147 in range(U):
                _q1191, _q1192, _q1198, _q1199 = routes[_q1147].bb
                _q498 = (_q1191 - _q1144 if _q1144 < _q1191 else _q1144 - _q1192 if _q1144 > _q1192 else 0) + (_q1198 - _q1145 if _q1145 < _q1198 else _q1145 - _q1199 if _q1145 > _q1199 else 0)
                _q873.append((_q498, _q1147))
            _q873.sort()
            _q687 = _q681.s
            _q706 = 2 if _q681.dw or _q681.df else 1
            for _q498, _q1147 in _q873:
                if best is not None:
                    _q731 = _q687 + _q498
                    if _q731 > best or (_q731 == best and _q1147 > _q381):
                        if not _q681.a or _q1052._animal_ok(_q1147, _q681):
                            _q1052.evals += _q706 * (len(routes[_q1147].tl) + 1)
                        continue
                _q829, k = _q1052._best_insert(_q1147, _q681)
                if _q829 is None:
                    continue
                c = _q829 - routes[_q1147].dur
                if best is None or c < best or (c == best and _q1147 < _q381):
                    best, _q381, _q365 = (c, _q1147, k)
            return (_q381, _q365)
        for _q1147 in range(U):
            _q829, k = _q1052._best_insert(_q1147, _q681)
            if _q829 is None:
                continue
            c = _q829 - routes[_q1147].dur
            if best is None or c < best:
                best, _q381, _q365 = (c, _q1147, k)
        return (_q381, _q365)

    def _construct(_q1052, _q686):
        """Root-first cheapest insertion (critical first, then farthest first) into the present units' routes."""
        _q873 = sorted(_q686, key=lambda t: (not _q1052.jobs[t].crit, -CENTER_D[t], t))
        _q737 = []
        for t in _q873:
            _q381, _q365 = _q1052._cheapest(t)
            if _q381 is None:
                _q737.append(t)
            else:
                _q1052._insert(_q381, t, _q365)
        return _q737

    def _plan_total(_q1052):
        _q938 = sum((_q1052.jobs[t].val for t in _q1052.pool))
        return 1000.0 * _q938 + sum((_q1052._cost(_q1147, _q970) for _q1147, _q970 in enumerate(_q1052.routes)))

    def _must_water(_q1052, t):
        """audit2: is job t a must-WATER (a WATER on a PLANT tile with consecutive_unwatered >= 1, not watered today:
        the plant weeds tonight without it)?"""
        _q428 = _q1052.chains.get(t)
        if not _q428 or type(t) is _Sub or _q1052.tiles is None:
            return False
        if not any((op == 'WATER' for op, _ in _q428)):
            return False
        _q1123 = int(t)
        tile = _q1052.tiles[_q1123 // B][_q1123 % B]
        return isinstance(tile, dict) and tile.get('kind') == 'PLANT' and (not tile.get('watered_today')) and (int(tile.get('consecutive_unwatered', 0) or 0) >= 1)

    def _strip_fert(_q1052, t):
        _q428 = _q1052.chains.get(t)
        if not _q428 or not any((op == 'FERTILIZE' for op, _ in _q428)) or (not _q1052._must_water(t)):
            return False
        _q428[:] = [_q857 for _q857 in _q428 if _q857[0] != 'FERTILIZE']
        if not _q428 or _q1052._refresh_job(t, _q1052.tiles) is None:
            return False
        _q1052.stats['water_split'] = _q1052.stats.get('water_split', 0) + 1
        return True

    def _fix_overflow(_q1052):
        """Routes longer than the turns left drop their lowest value-per-turn jobs into the pool."""
        _q618 = _q1052.cfg.get('water_guard')
        _q1082 = _q1052.cfg.get('water_split')
        for _q1147, _q970 in enumerate(_q1052.routes):
            while _q970.tl and _q970.dur > _q1052.cap:
                best, _q361 = (None, None)
                _q358, _q363 = (None, None)
                for _q652, t in enumerate(_q970.tl):
                    if _q652 == 0 and _q1147 < _q1052.n_units and (_q1052.pos[_q1147] == t % NT):
                        continue
                    _q681 = _q1052.jobs[t]
                    _q1039 = _q970.dur - _q1052._remove_dur(_q1147, _q652, False)
                    _q1043 = _q681.val / max(1.0, _q1039)
                    if _q618 and _q1052._must_water(t):
                        if _q358 is None or _q1043 < _q358:
                            _q358, _q363 = (_q1043, _q652)
                        continue
                    if best is None or _q1043 < best:
                        best, _q361 = (_q1043, _q652)
                if _q361 is None:
                    _q361 = _q363
                if _q361 is None:
                    break
                t = _q970.tl[_q361]
                if _q1082 and _q1052._strip_fert(t):
                    _q1052._eval(_q1147, _q970)
                    continue
                _q1052._remove(_q1147, t)
                _q1052.pool.add(t)
                _q1052.stats['overflow_drops'] += 1

    def _insert_pool(_q1052):
        if not _q1052.pool:
            return
        for t in sorted(_q1052.pool, key=lambda t: (-_q1052.jobs[t].val, t)):
            if time.perf_counter() >= _q1052.t_end:
                _q1052.tcap_hit = True
                break
            _q381, _q365 = _q1052._cheapest(t)
            if _q381 is not None:
                _q1052._insert(_q381, t, _q365)
                _q1052._calc_shed_free()
            elif _q1052.jobs[t].crit:
                _q1052._eject_for(t)
                if t in _q1052.pool and _q1052.cfg.get('water_split') and _q1052._strip_fert(t):
                    _q381, _q365 = _q1052._cheapest(t)
                    if _q381 is not None:
                        _q1052._insert(_q381, t, _q365)
                        _q1052._calc_shed_free()
                    elif _q1052.jobs[t].crit:
                        _q1052._eject_for(t)
                if t in _q1052.pool and int(_q1052.cfg.get('eject_multi') or 0) > 1 and _q1052.jobs[t].crit and _q1052._must_water(t):
                    _q1052._eject_multi(t)

    def _evictable(_q1052, t, _q1107, _q681, _q683):
        if not _q683.crit or _q1052._must_water(_q1107) or (not _q1052._must_water(t)):
            return False
        return any((op in ('PLANT', 'PLACE') for op, _ in _q683.chain))

    def _eject_for(_q1052, t):
        """Put critical job t in by removing one cheaper, non-critical job of a route (min value removed)."""
        _q681 = _q1052.jobs[t]
        best = None
        _q538 = _q1052.cfg.get('water_guard') == 'evict'
        for _q1147, _q970 in enumerate(_q1052.routes):
            for _q652, _q1107 in enumerate(_q970.tl):
                _q683 = _q1052.jobs[_q1107]
                if (_q683.val >= _q681.val or _q683.crit) and (not (_q538 and _q1052._evictable(t, _q1107, _q681, _q683))):
                    continue
                if _q652 == 0 and _q1147 < _q1052.n_units and (_q1052.pos[_q1147] == _q1107 % NT) or _q1052._pinned(_q1147, _q683):
                    continue
                _q1039 = _q970.dur - _q1052._remove_dur(_q1147, _q652, False)
                _q829, k = _q1052._best_insert(_q1147, _q681, cap=_q1052.cap + _q1039)
                if _q829 is None:
                    continue
                if best is None or _q683.val < best[0]:
                    best = (_q683.val, _q1147, _q1107)
        if best is None:
            return
        _, _q1147, _q1107 = best
        _q970 = _q1052.routes[_q1147]
        _q868 = list(_q970.tl)
        _q1052._remove(_q1147, _q1107)
        _q829, k = _q1052._best_insert(_q1147, _q681)
        if _q829 is not None:
            _q1052._insert(_q1147, t, k)
            _q1052.pool.add(_q1107)
            _q1052.stats['ejects'] += 1
        else:
            _q970.tl = _q868
            _q1052._eval(_q1147, _q970)
            _q1052.where[_q1107] = _q1147

    def _eject_multi(_q1052, t):
        _q681 = _q1052.jobs[t]
        _q710 = int(_q1052.cfg.get('eject_multi') or 0)
        best = None
        for _q1147, _q970 in enumerate(_q1052.routes[:_q1052.n_plan]):
            _q401 = []
            for _q652, _q1107 in enumerate(_q970.tl):
                _q683 = _q1052.jobs[_q1107]
                if _q683.crit or (_q652 == 0 and _q1147 < _q1052.n_units and (_q1052.pos[_q1147] == _q1107 % NT)) or _q1052._pinned(_q1147, _q683):
                    continue
                _q401.append((_q683.val, _q1107))
            if len(_q401) < 2:
                continue
            _q401.sort()
            _q1076 = _snap(_q970)
            oW, oF = (_q970.oW, _q970.oF)
            _q982 = []
            _q1133 = 0.0
            _q575 = False
            for v2, _q1107 in _q401[:_q710]:
                if _q1133 + v2 >= _q681.val:
                    break
                _q970.tl.remove(_q1107)
                _q982.append(_q1107)
                _q1133 += v2
                _q1052._eval(_q1147, _q970)
                if len(_q982) >= 2:
                    _q829, k = _q1052._best_insert(_q1147, _q681)
                    if _q829 is not None:
                        _q575 = True
                        break
            _q1052.outW += oW - _q970.oW
            _q1052.outF += oF - _q970.oF
            _restore(_q970, _q1076)
            if _q575 and (best is None or _q1133 < best[0]):
                best = (_q1133, _q1147, list(_q982))
        if best is None:
            return False
        _, _q1147, _q982 = best
        _q970 = _q1052.routes[_q1147]
        _q1076 = _snap(_q970)
        oW, oF = (_q970.oW, _q970.oF)
        for _q1107 in _q982:
            _q1052._remove(_q1147, _q1107)
        _q829, k = _q1052._best_insert(_q1147, _q681)
        if _q829 is None:
            _q1052.outW += oW - _q970.oW
            _q1052.outF += oF - _q970.oF
            _restore(_q970, _q1076)
            for _q1107 in _q982:
                _q1052.where[_q1107] = _q1147
            return False
        _q1052._insert(_q1147, t, k)
        for _q1107 in _q982:
            _q1052.pool.add(_q1107)
        _q1052._calc_shed_free()
        _q1052.stats['eject_multi'] = _q1052.stats.get('eject_multi', 0) + 1
        return True

    def _ls(_q1052):
        """First-improvement local search: relocate, intra or-opt / 2-opt, tail exchange."""
        U = _q1052.n_plan
        if U == 0:
            return
        _q659 = True
        while _q659 and (not _q1052._timeout()):
            _q659 = False
            if _q1052._relocate_pass():
                _q659 = True
            if _q1052._timeout():
                return
            if _q1052._intra_pass():
                _q659 = True
            if _q1052._timeout():
                return
            if _q1052.cfg['tail_x'] and _q1052._tail_pass():
                _q659 = True

    def _relocate_pass(_q1052):
        routes = _q1052.routes
        U = _q1052.n_plan
        _q729 = bool(_q1052.cfg['late_w'])
        _q339 = False
        for a in range(U):
            _q975 = routes[a]
            _q652 = 0
            while _q652 < len(_q975.tl):
                if _q1052._timeout():
                    return _q339
                t = _q975.tl[_q652]
                _q681 = _q1052.jobs[t]
                if _q652 == 0 and a < _q1052.n_units and (_q1052.pos[a] == t % NT) or _q1052._pinned(a, _q681):
                    _q652 += 1
                    continue
                _q607 = _q975.dur - _q1052._remove_dur(a, _q652)
                best, bb, _q365 = (-1e-09, None, None)
                for b in range(U):
                    if b == a:
                        continue
                    _q980 = routes[b]
                    if _q980.dur + _q681.s > _q1052.cap:
                        continue
                    _q829, k = _q1052._best_insert(b, _q681)
                    if _q829 is None:
                        continue
                    _q488 = _q829 - _q980.dur - _q607
                    if _q488 < best:
                        best, bb, _q365 = (_q488, b, k)
                if bb is not None:
                    fb = _q1052.fb
                    if _q729 and (_q681.urg or _q975.dur + fb * _q975.oF != _q1052._cost(a, _q975) or routes[bb].dur + fb * routes[bb].oF != _q1052._cost(bb, routes[bb])):
                        _q356 = _q1052._cost(a, _q975) + _q1052._cost(bb, routes[bb])
                        _q1052._remove(a, t)
                        _q1052._insert(bb, t, _q365)
                        after = _q1052._cost(a, _q975) + _q1052._cost(bb, routes[bb])
                        if after > _q356 - 1e-09:
                            _q1052._remove(bb, t)
                            _q1052._insert(a, t, _q652)
                            _q652 += 1
                            continue
                    else:
                        _q1052._remove(a, t)
                        _q1052._insert(bb, t, _q365)
                    if _q681.a:
                        _q1052._calc_shed_free()
                    _q1052.stats['ls_moves'] += 1
                    _q339 = True
                    continue
                _q652 += 1
        return _q339

    def _intra_pass(_q1052):
        """Or-opt (one job) and 2-opt on each route's open path from its start tile (same job set -> same kit)."""
        _q339 = False
        for a in range(_q1052.n_plan):
            if _q1052._timeout():
                return _q339
            _q975 = _q1052.routes[a]
            n = len(_q975.tl)
            if n < 2:
                continue
            _q577 = a < _q1052.n_units and _q1052.pos[a] == _q975.tl[0] % NT
            _q729 = _q1052.cfg['late_w'] and any((_q1052.jobs[t].urg for t in _q975.tl))
            _q469 = _q1052._cost(a, _q975)
            _q659 = True
            while _q659 and (not _q1052._timeout()):
                _q659 = False
                _q32 = [_q975.sp] + _q975.tl
                m = len(_q32)
                lo = 2 if _q577 else 1
                for _q652 in range(lo, m - 1):
                    _q311 = _q32[_q652 - 1]
                    _q47 = _q32[_q652]
                    _q6 = D[_q311]
                    for k in range(_q652 + 1, m):
                        _q48 = _q32[k]
                        if k + 1 < m:
                            _q855 = _q32[k + 1]
                            _q488 = _q6[_q48] + D[_q47][_q855] - _q6[_q47] - D[_q48][_q855]
                        else:
                            _q488 = _q6[_q48] - _q6[_q47]
                        if _q488 < -1e-09:
                            new = _q32[1:_q652] + _q32[_q652:k + 1][::-1] + _q32[k + 1:]
                            if _q1052._accept_intra(a, _q975, new, _q469, _q729):
                                _q469 = _q1052._cost(a, _q975)
                                _q659 = True
                                _q339 = True
                                break
                    if _q659:
                        break
                    _q1052.evals += m - _q652
                if _q659:
                    continue
                for _q652 in range(lo, m):
                    x = _q32[_q652]
                    _q957 = _q32[_q652 - 1]
                    if _q652 + 1 < m:
                        _q855 = _q32[_q652 + 1]
                        rem = D[_q957][_q855] - D[_q957][x] - D[x][_q855]
                    else:
                        rem = -D[_q957][x]
                    _q49 = _q32[:_q652] + _q32[_q652 + 1:]
                    _q12 = D[x]
                    for k in range(lo - 1, len(_q49)):
                        if k == _q652 - 1:
                            continue
                        _q961 = _q49[k]
                        if k + 1 < len(_q49):
                            _q962 = _q49[k + 1]
                            _q666 = _q12[_q961] + _q12[_q962] - D[_q961][_q962]
                        else:
                            _q666 = _q12[_q961]
                        if rem + _q666 < -1e-09:
                            new = _q49[1:k + 1] + [x] + _q49[k + 1:]
                            if _q1052._accept_intra(a, _q975, new, _q469, _q729):
                                _q469 = _q1052._cost(a, _q975)
                                _q659 = True
                                _q339 = True
                                break
                    _q1052.evals += len(_q49)
                    if _q659:
                        break
        return _q339

    def _accept_intra(_q1052, a, _q975, new, _q469, _q729):
        _q868 = _q975.tl
        _q870 = _q975.dur
        _q975.tl = new
        _q1052._eval(a, _q975)
        c = _q1052._cost(a, _q975)
        if c < _q469 - 1e-09 and (_q975.dur <= _q1052.cap or _q975.dur <= _q870):
            _q1052.stats['ls_moves'] += 1
            return True
        _q975.tl = _q868
        _q1052._eval(a, _q975)
        return False

    def _prefix(_q1052, _q1147, _q970):
        tl = _q970.tl
        jobs = _q1052.jobs
        _q44 = [0]
        _q34 = [0]
        _q41 = [0]
        _q37 = [0, 0]
        for _q656, t in enumerate(tl):
            _q681 = jobs[t]
            _q44.append(_q44[-1] + _q681.w)
            _q34.append(_q34[-1] + _q681.f)
            _q41.append(_q41[-1] + _q681.s)
            if _q656 >= 1:
                _q37.append(_q37[-1] + D[tl[_q656 - 1]][t])
        return (_q44, _q34, _q41, _q37)

    def _tail_pass(_q1052):
        U = _q1052.n_plan
        _q339 = False
        pre = [_q1052._prefix(_q1147, _q1052.routes[_q1147]) for _q1147 in range(U)]
        for a in range(U):
            for b in range(a + 1, U):
                if _q1052._timeout():
                    return _q339
                if _q1052._tail_x(a, b, pre[a], pre[b]):
                    pre[a] = _q1052._prefix(a, _q1052.routes[a])
                    pre[b] = _q1052._prefix(b, _q1052.routes[b])
                    _q339 = True
        return _q339

    def _tail_x(_q1052, a, b, _q898, pb):
        _q975, _q980 = (_q1052.routes[a], _q1052.routes[b])
        _q1, _q4 = (_q975.tl, _q980.tl)
        _q825, _q828 = (len(_q1), len(_q4))
        if _q825 == 0 and _q828 == 0 or _q975.A or _q980.A:
            return False
        _q729 = _q1052.cfg['late_w'] and (any((_q1052.jobs[t].urg for t in _q1)) or any((_q1052.jobs[t].urg for t in _q4)))
        _q467 = _q975.dur + _q980.dur
        fb = _q1052.fb
        _q468 = _q467 + fb * (_q975.oF + _q980.oF) if fb else _q467
        cap = _q1052.cap
        _q45, _q35, _q42, _q38 = _q898
        _q46, _q36, _q43, _q39 = pb
        _q24, Ib = (_q38[_q825] if _q825 else 0, _q39[_q828] if _q828 else 0)
        _q62, _q19, _q57 = (_q45[_q825], _q35[_q825], _q42[_q825])
        _q63, _q20, _q58 = (_q46[_q828], _q36[_q828], _q43[_q828])
        _q658 = 1 if _q825 and a < _q1052.n_units and (_q1052.pos[a] == _q1[0] % NT) else 0
        _q708 = 1 if _q828 and b < _q1052.n_units and (_q1052.pos[b] == _q4[0] % NT) else 0
        _q1052.evals += (_q825 + 1) * (_q828 + 1)
        _q473, _q934, _q1074, _q425, _q932, _q1071 = (_q975.cw, _q975.pmw, _q975.smw, _q975.cf, _q975.pmf, _q975.smf)
        _q474, _q935, _q1075, _q426, _q933, _q1072 = (_q980.cw, _q980.pmw, _q980.smw, _q980.cf, _q980.pmf, _q980.smf)
        _q995 = _q1052.ret
        for _q652 in range(_q658, _q825 + 1):
            _q417 = _q473[_q652 - 1] if _q652 else 0
            _q398 = _q425[_q652 - 1] if _q652 else 0
            _q1034 = _q38[_q652] if _q652 >= 1 else 0
            _q1035 = _q24 - _q38[_q652 + 1] if _q652 < _q825 else 0
            for k in range(_q708, _q828 + 1):
                if _q652 == _q825 and k == _q828 or (_q652 == 0 and k == 0):
                    continue
                _q1041 = _q39[k] if k >= 1 else 0
                _q1042 = Ib - _q39[k + 1] if k < _q828 else 0
                _q420 = _q474[k - 1] if k else 0
                _q419 = _q426[k - 1] if k else 0
                _q60 = _q934[_q652]
                x = _q417 - _q420 + _q1075[k]
                if x > _q60:
                    _q60 = x
                _q13 = _q932[_q652]
                x = _q398 - _q419 + _q1072[k]
                if x > _q13:
                    _q13 = x
                _q54 = _q42[_q652] + _q58 - _q43[k]
                _q22 = _q1034 + _q1042 + (D[_q1[_q652 - 1]][_q4[k]] if _q652 >= 1 and k < _q828 else 0)
                _q544 = _q1[0] if _q652 >= 1 else _q4[k] if k < _q828 else -1
                if _q544 >= 0:
                    kt, sp = _q1052._kit(a, _q60, _q13, None)
                    _q477 = kt + D[sp][_q544] + _q22 + _q54
                    if _q995:
                        _q477 += ACC_D[_q4[-1] if k < _q828 else _q1[_q652 - 1]] + 1
                else:
                    _q477 = 0
                if _q477 > cap:
                    continue
                _q61 = _q935[k]
                x = _q420 - _q417 + _q1074[_q652]
                if x > _q61:
                    _q61 = x
                _q14 = _q933[k]
                x = _q419 - _q398 + _q1071[_q652]
                if x > _q14:
                    _q14 = x
                _q55 = _q43[k] + _q57 - _q42[_q652]
                _q23 = _q1041 + _q1035 + (D[_q4[k - 1]][_q1[_q652]] if k >= 1 and _q652 < _q825 else 0)
                _q545 = _q4[0] if k >= 1 else _q1[_q652] if _q652 < _q825 else -1
                if _q545 >= 0:
                    kt, sp = _q1052._kit(b, _q61, _q14, None)
                    _q478 = kt + D[sp][_q545] + _q23 + _q55
                    if _q995:
                        _q478 += ACC_D[_q1[-1] if _q652 < _q825 else _q4[k - 1]] + 1
                else:
                    _q478 = 0
                if _q478 > cap:
                    continue
                if fb:
                    _q859 = _q13 - _q1052.invF[a]
                    _q860 = _q14 - _q1052.invF[b]
                    if _q477 + _q478 + fb * ((_q859 if _q859 > 0 else 0) + (_q860 if _q860 > 0 else 0)) >= _q468 - 1e-09:
                        continue
                elif _q477 + _q478 >= _q467 - 1e-09:
                    continue
                if _q1052.supply_on and (not _q1052._supply_ok2(a, b, _q60, _q13, _q61, _q14)):
                    continue
                _q837 = _q1[:_q652] + _q4[k:]
                _q838 = _q4[:k] + _q1[_q652:]
                if _q729:
                    _q356 = _q1052._cost(a, _q975) + _q1052._cost(b, _q980)
                _q975.tl, _q980.tl = (_q837, _q838)
                _q1052._eval(a, _q975)
                _q1052._eval(b, _q980)
                if _q729 and _q1052._cost(a, _q975) + _q1052._cost(b, _q980) >= _q356 - 1e-09:
                    _q975.tl, _q980.tl = (_q1, _q4)
                    _q1052._eval(a, _q975)
                    _q1052._eval(b, _q980)
                    continue
                for t in _q837:
                    _q1052.where[t] = a
                for t in _q838:
                    _q1052.where[t] = b
                _q1052.stats['ls_moves'] += 1
                return True
        return False

    def _supply_ok2(_q1052, a, b, _q60, _q13, _q61, _q14):
        """Tail exchange: can the shed cover the two routes' new start needs (after the other units' pickups)?"""
        _q975, _q980 = (_q1052.routes[a], _q1052.routes[b])
        _q882 = max(0, _q60 - _q1052.invW[a]) + max(0, _q61 - _q1052.invW[b]) - _q975.oW - _q980.oW
        _q866 = max(0, _q13 - _q1052.invF[a]) + max(0, _q14 - _q1052.invF[b]) - _q975.oF - _q980.oF
        return (_q882 <= 0 or _q1052.shed.get('WHEAT', 0) - _q1052.outW >= _q882) and (_q866 <= 0 or _q1052.shed.get('FERTILIZER', 0) - _q1052.outF >= _q866)

    def _movable(_q1052, _q1147, _q652, t):
        return not (_q652 == 0 and _q1147 < _q1052.n_units and (_q1052.pos[_q1147] == t % NT) or _q1052._pinned(_q1147, _q1052.jobs[t]))

    def _rr(_q1052):
        """Ruin & recreate (SISR-lite): remove strings of consecutive jobs from up to rr_routes routes near a random
        seed job, re-insert them and the pool (critical first; random / far / value order), keep if not worse.
        Incremental objective (only touched routes are re-costed), lazy snapshots of touched routes."""
        cfg = _q1052.cfg
        rng = random.Random(_q1052.day * 7919 + _q1052.hour * 131 + 17)
        _q1012 = rng.random
        jobs = _q1052.jobs
        routes = _q1052.routes
        _q338 = False
        _q747 = cfg['rr_lmax']
        _q817 = cfg['rr_routes']
        ps = cfg['rr_pool_seed']
        _q1090 = cfg['rr_stall'] if not (cfg['stall_loose_only'] and _q1052.is_tight) else 0
        if _q1090:
            _q1090 += cfg['rr_stall_per_job'] * len(_q1052.where)
        _q1089 = 0
        while not _q1052._timeout():
            if not _q1052.where:
                return _q338
            if _q1090 and _q1089 >= _q1090:
                _q1052.stats['rr_stall_stop'] = _q1052.stats.get('rr_stall_stop', 0) + 1
                return _q338
            _q1089 += 1
            _q1052.stats['rr_iter'] += 1
            _q343 = list(_q1052.where)
            _q1052.evals += len(_q343) // 2 + 40
            seed = _q343[int(_q1012() * len(_q343))]
            if ps and _q1052.pool and (_q1012() < ps):
                _q922 = sorted(_q1052.pool)
                _q889 = _q922[int(_q1012() * len(_q922))]
                for _q1107 in (NEARS if _q1052.split_on else NEAR)[_q889]:
                    if _q1107 in _q1052.where:
                        seed = _q1107
                        break
            _q815 = 1 + int(_q1012() * _q817)
            _q1077 = {}
            _q982 = []
            where = _q1052.where
            for t in (NEARS if _q1052.split_on else NEAR)[seed]:
                if len(_q1077) >= _q815:
                    break
                _q1147 = where.get(t)
                if _q1147 is None or _q1147 in _q1077:
                    continue
                _q970 = routes[_q1147]
                tl = _q970.tl
                _q652 = tl.index(t)
                _q25 = 1 + int(_q1012() * min(len(tl), _q747))
                lo = max(0, min(_q652 - int(_q1012() * _q25), len(tl) - _q25))
                _q1051 = [x for k, x in enumerate(tl[lo:lo + _q25]) if _q1052._movable(_q1147, lo + k, x)]
                if not _q1051:
                    continue
                _q1077[_q1147] = (_snap(_q970), _q1052._cost(_q1147, _q970))
                for x in _q1051:
                    tl.remove(x)
                    where.pop(x, None)
                    _q982.append(x)
                _q1052._eval(_q1147, _q970)
            _q1052.evals += 4 * len(_q982) + 4
            if not _q982:
                continue
            _q937 = set(_q1052.pool)
            _q939 = sum((jobs[t].val for t in _q937))
            if any((jobs[t].a for t in _q982)):
                _q1052._calc_shed_free()
            _q1131 = _q982 + sorted(_q937)
            _q1052.pool = set()
            mode = int(_q1012() * 3)
            if mode == 0:
                rng.shuffle(_q1131)
                _q1131.sort(key=lambda t: not jobs[t].crit)
            elif mode == 1:
                _q1131.sort(key=lambda t: (not jobs[t].crit, -CENTER_D[t], t))
            else:
                _q1131.sort(key=lambda t: (not jobs[t].crit, -jobs[t].val / max(1, jobs[t].s), CENTER_D[t], t))
            for t in _q1131:
                _q381, _q365 = _q1052._cheapest(t)
                if _q381 is None:
                    _q1052.pool.add(t)
                else:
                    if _q381 not in _q1077:
                        _q1077[_q381] = (_snap(routes[_q381]), _q1052._cost(_q381, routes[_q381]))
                    _q1052._insert(_q381, t, _q365)
                    if jobs[t].a:
                        _q1052._calc_shed_free()
            _q356 = 1000.0 * _q939 + sum((c for _, c in _q1077.values()))
            after = 1000.0 * sum((jobs[t].val for t in _q1052.pool)) + sum((_q1052._cost(_q1147, routes[_q1147]) for _q1147 in _q1077))
            _q1052.evals += len(_q1077) * 3
            if after <= _q356 + 1e-09:
                if after < _q356 - 1e-09:
                    _q1052.stats['rr_acc'] += 1
                    _q338 = True
                    _q1089 = 0
                continue
            for _q1147 in _q1077:
                for t in routes[_q1147].tl:
                    where.pop(t, None)
            for t in _q982:
                where.pop(t, None)
            for _q1147, (_q1076, _) in _q1077.items():
                _q970 = routes[_q1147]
                _q1052.outW -= _q970.oW
                _q1052.outF -= _q970.oF
                _restore(_q970, _q1076)
                _q1052.outW += _q970.oW
                _q1052.outF += _q970.oF
                for t in _q970.tl:
                    where[t] = _q1147
            _q1052.pool = _q937
            if any((jobs[t].a for t in _q982)):
                _q1052._calc_shed_free()
        return _q338

    def _sync_units(_q1052, _q1161):
        units = _q1161['units']
        _q672 = _q1161['inv']
        n = len(units)
        _q1052.pos = [_q888[1] * B + _q888[0] for _q888 in units]
        _q1052.invW = []
        _q1052.invF = []
        _q1052.invA = []
        for _q1147 in range(n):
            _q679 = _q672[_q1147] if _q1147 < len(_q672) else {}
            _q1052.invW.append(_q679.get('WHEAT', 0))
            _q1052.invF.append(_q679.get('FERTILIZER', 0))
            _q1052.invA.append({k: _q679[k] for k in ANIMALS if _q679.get(k, 0) > 0})
        _q1052.shed = _q1161.get('shed', {})
        _q1052.delay = [0] * n
        _q1052.cur_inv = _q672
        _q498 = _q1052.dlv_cfg
        _q1052.dlv_t = {}
        if _q498:
            hour = _q1161.get('hour', 0)
            _q1068 = _q1052.cfg.get('dlv_slack_until')
            _q1067 = 24 - hour - int(_q1052.cfg.get('cap_cut') or 0)
            if _q498['h0'] <= hour <= _q498['h1']:
                for _q1147 in range(n):
                    _q679 = _q672[_q1147] if _q1147 < len(_q672) else {}
                    _q1146 = [_q675 for _q675 in _q498['items'] if _q679.get(_q675, 0) > 0]
                    if not _q1146:
                        continue
                    k = sum((_q679.get(_q675, 0) for _q675 in _q498['items']))
                    if (k >= _q498['kmin'] or _q1147 in _q1052.dlv_on) and ACC_D[_q1052.pos[_q1147]] + len(_q1146) <= 23 - hour:
                        if _q1068 is not None and hour < _q1068 and (_q1147 not in _q1052.dlv_on) and (_q1147 < len(_q1052.routes)):
                            _q974 = _q1052.routes[_q1147]
                            if (_q974.dur if _q974.tl else 0) + ACC_D[_q1052.pos[_q1147]] + len(_q1146) > _q1067:
                                continue
                        _q1052.dlv_t[_q1147] = len(_q1146)
                        _q1052.stats['dlv_turns'] = _q1052.stats.get('dlv_turns', 0) + 1
            _q1052.dlv_on = set(_q1052.dlv_t)
        return n

    def _virtual_units(_q1052):
        """Positions / inventories / start delay of the virtual units (u >= n_units): predicted spawn tiles by the
        engine's rule (_spawn_hand: first shed-access tile with the fewest units, NW-NE-SW-SE order), empty hands,
        one turn of delay (a hand hired now acts from the next step)."""
        n = _q1052.n_units
        if _q1052.n_plan <= n:
            return
        _q865 = {a: 0 for a in ACC_ORDER}
        for _q888 in _q1052.pos[:n]:
            if _q888 in _q865:
                _q865[_q888] += 1
        for _q1147 in range(n, _q1052.n_plan):
            a = min(ACC_ORDER, key=lambda x: (_q865[x], ACC_ORDER.index(x)))
            _q865[a] += 1
            _q1052.pos.append(a)
            _q1052.invW.append(0)
            _q1052.invF.append(0)
            _q1052.invA.append({})
            _q1052.delay.append(1)

    def _sync_jobs(_q1052, tiles):
        for t in list(_q1052.chains):
            _q1169 = t in _q1052.locked
            _q681 = _q1052._refresh_job(t, tiles)
            if _q681 is None:
                _q1147 = _q1052.where.get(t)
                if _q1147 is not None:
                    _q1052._remove(_q1147, t)
                _q1052.pool.discard(t)
                _q1052.locked.discard(t)
                _q1052.res_set.discard(t)
                _q1052.jobs.pop(t, None)
                continue
            if _q681.pre == 'locked':
                _q1052.locked.add(t)
                continue
            if _q1052.held and t in _q1052.held:
                _q1147 = _q1052.where.get(t)
                if _q1147 is not None:
                    _q1052._remove(_q1147, t)
                _q1052.pool.discard(t)
                _q1052.res_set.discard(t)
                _q1052.locked.add(t)
                _q1052.stats['seed_held'] = _q1052.stats.get('seed_held', 0) + 1
                continue
            if _q1169:
                _q1052.locked.discard(t)
                _q1052.pool.add(t)
            elif t not in _q1052.where and t not in _q1052.pool and (t not in _q1052.res_set):
                _q1052.pool.add(t)

    def act(_q1052, _q1161):
        t0 = time.perf_counter()
        cfg = _q1052.cfg
        _q1052.evals = 0
        _q1052.tcap_hit = False
        _q1052.budget_end = cfg['ls_budget']
        _q1052.t_end = t0 + cfg['ls_time_ms'] / 1000.0
        tiles = _q1161['tiles']
        hour = _q1161['hour']
        _q1052.hour = hour
        _q1052.tiles = tiles
        _q1052.ret = bool(cfg.get('ret_leg'))
        _q1052.cap = max(1, 24 - hour - int(cfg.get('cap_cut') or 0)) if cfg.get('cap_cut') else 24 - hour
        n = _q1052._sync_units(_q1161)
        if n > _q1052.max_units:
            _q1052.max_units = n
        if 'pending_buys' in _q1161:
            _q1052.pending_buys = dict(_q1161.get('pending_buys') or {})
        if 'harv_need' in _q1161:
            _q1052.harv_need = frozenset(_q1161.get('harv_need') or ()) | frozenset(cfg.get('harv_need') or ())
        if cfg.get('seed_hold'):
            _q1052.held = frozenset(_q1161.get('hold_tiles') or ())
        if not _q1052.started:
            _q1052.started = True
            if cfg['rescue'] and _q1052.missed_prev:
                _q1052._add_rescues(tiles)
            if _q1052.hb:
                _q1052._harv_filter(tiles, list(_q1052.chains))
                _q1052._hb_new = set()
            for t in list(_q1052.chains):
                _q681 = _q1052._refresh_job(t, tiles)
                if _q681 is not None and _q681.pre == 'locked':
                    _q1052.locked.add(t)
            if cfg['warm'] and _q1052.template:
                _q1115 = set()
                for _q1147 in sorted(_q1052.template):
                    tl = [t for t in _q1052.template[_q1147] if t in _q1052.jobs and t not in _q1052.locked and (t not in _q1115)]
                    _q1115.update(tl)
                    _q1052.reserved[_q1147] = tl
                _q1052.res_set = _q1115
            for t in _q1052.jobs:
                if t not in _q1052.locked and t not in _q1052.res_set:
                    _q1052.pool.add(t)
        _q574 = _q1052.n_plan == 0
        _q342 = n > _q1052.n_units
        while _q1052.n_units < n:
            _q1147 = _q1052.n_units
            _q1052.n_units += 1
            if _q1147 < len(_q1052.routes):
                _q1052.stats['virt_real'] = _q1052.stats.get('virt_real', 0) + 1
                continue
            _q1052.routes.append(Route())
            if _q1147 in _q1052.reserved:
                _q1052._take_reserved(_q1147)
        if _q574 and cfg['virt'] and (_q1052.prev_hands > 0) and (hour < cfg['virt_hours']):
            for k in range(min(_q1052.prev_hands, cfg['virt_max'])):
                _q1147 = len(_q1052.routes)
                _q1052.routes.append(Route())
                _q1052.stats['virt_made'] = _q1052.stats.get('virt_made', 0) + 1
                if _q1147 in _q1052.reserved:
                    _q1052._take_reserved(_q1147)
        if len(_q1052.routes) > _q1052.n_units and hour >= cfg['virt_hours']:
            for _q1147 in range(_q1052.n_units, len(_q1052.routes)):
                for t in _q1052.routes[_q1147].tl:
                    _q1052.where.pop(t, None)
                    if t in _q1052.jobs and t not in _q1052.locked:
                        _q1052.pool.add(t)
                _q1052.stats['virt_dropped'] = _q1052.stats.get('virt_dropped', 0) + 1
            del _q1052.routes[_q1052.n_units:]
        _q1052.n_plan = len(_q1052.routes)
        _q1052._virtual_units()
        if _q1052.reserved and hour >= cfg['reserve_hours']:
            for _q1147 in list(_q1052.reserved):
                for t in _q1052.reserved.pop(_q1147):
                    _q1052.res_set.discard(t)
                    if t in _q1052.jobs and t not in _q1052.where and (t not in _q1052.locked):
                        _q1052.pool.add(t)
        if _q1052._hb_new:
            _q1052._harv_filter(tiles, list(_q1052._hb_new))
            _q1052._hb_new = set()
        _q1052._sync_jobs(tiles)
        _q1052.outW = _q1052.outF = 0
        for _q970 in _q1052.routes:
            _q970.oW = _q970.oF = 0
        for _q1147 in range(_q1052.n_plan):
            _q1052._eval(_q1147, _q1052.routes[_q1147])
        sh = _q1052.shed
        _q1052.supply_on = cfg['supply_aware'] and (sh.get('WHEAT', 0) < _q1052.outW + SUPPLY_EASY or sh.get('FERTILIZER', 0) < _q1052.outF + SUPPLY_EASY)
        if _q1052.supply_on:
            _q1052.stats['supply_turns'] = _q1052.stats.get('supply_turns', 0) + 1
        _q1052._calc_shed_free()
        if _q342 and cfg['fresh_on_arrival'] and (hour > 0):
            _q1052._replan_fresh()
        _q1052._fix_overflow()
        _q1052._calc_shed_free()
        _q1052._insert_pool()
        _q1052._ls()
        _q1052._insert_pool()
        if cfg['rr'] and _q1052.n_plan:
            _q1052.is_tight = _q1052._tight()
            if cfg['turn_budget']:
                _q1116 = cfg['turn_budget']
                if _q1052.is_tight:
                    _q1116 *= cfg['tight_mult'] if _q1052.hour > 0 else cfg['tight_mult_h0']
                    _q1052.stats['tight_turns'] = _q1052.stats.get('tight_turns', 0) + 1
                _q1116 = int(_q1116 * min(1.0, _q1052.cap / float(cfg['budget_full_cap'])))
                _q1052.budget_end = max(_q1052.evals, _q1116 - cfg['ls_budget'] // 2)
            else:
                _q1052.budget_end = _q1052.evals + cfg['rr_budget']
            if _q1052._rr():
                _q1052.budget_end = _q1052.evals + cfg['ls_budget'] // 2
                _q1052._ls()
        _q1052.stats['evals'] += _q1052.evals
        if _q1052.tcap_hit:
            _q1052.stats['tcap_turns'] = _q1052.stats.get('tcap_turns', 0) + 1
        _q1052._snap = (_q1052.cap, [(_q970.dur, bool(_q970.tl)) for _q970 in _q1052.routes])
        _q1052._svc = set()
        return _q1052._actions(_q1161)

    def _tight(_q1052):
        """A turn is tight when some job does not fit (pool) or the routes' total slack is below tight_slack of the
        unit-turns left."""
        if _q1052.hour < _q1052.cfg['tight_min_hour'] or _q1052.n_plan < _q1052.cfg['tight_min_units']:
            return False
        if _q1052.pool:
            return True
        U = _q1052.n_plan
        slack = sum((_q1052.cap - _q1052.delay[_q1147] - _q970.dur for _q1147, _q970 in enumerate(_q1052.routes[:U])))
        return slack < _q1052.cfg['tight_slack'] * U * _q1052.cap

    def _take_reserved(_q1052, _q1147):
        tl = [t for t in _q1052.reserved.pop(_q1147) if t in _q1052.jobs and t not in _q1052.where and (t not in _q1052.locked)]
        for t in tl:
            _q1052.res_set.discard(t)
            _q1052.where[t] = _q1147
            _q1052.pool.discard(t)
        _q1052.routes[_q1147].tl = tl

    def _replan_fresh(_q1052):
        """Fresh construction for all present units; keep it if cheaper than the repaired plan."""
        _q1052.stats['replans'] += 1
        _q1052._fix_overflow()
        _q1052._insert_pool()
        _q869 = _q1052._plan_total()
        _q986 = [list(_q970.tl) for _q970 in _q1052.routes]
        _q985 = set(_q1052.pool)
        _q987 = dict(_q1052.where)
        seeds = []
        for _q1147, _q970 in enumerate(_q1052.routes):
            keep = []
            for _q652, t in enumerate(_q970.tl):
                _q681 = _q1052.jobs[t]
                if _q652 == 0 and _q1147 < _q1052.n_units and (_q1052.pos[_q1147] == t % NT) or _q1052._pinned(_q1147, _q681):
                    keep.append(t)
            seeds.append(keep)
        _q1049 = set((t for s in seeds for t in s))
        _q332 = [t for t in _q1052.jobs if t not in _q1052.locked and t not in _q1052.res_set and (t not in _q1049)]
        _q1052.where = {}
        for _q1147, _q970 in enumerate(_q1052.routes):
            _q970.tl = list(seeds[_q1147])
            _q1052._eval(_q1147, _q970)
            for t in _q970.tl:
                _q1052.where[t] = _q1147
        _q1052.pool = set()
        _q1052._calc_shed_free()
        _q737 = _q1052._construct(_q332)
        _q1052.pool = set(_q737)
        _q1052._insert_pool()
        _q839 = _q1052._plan_total()
        if _q839 < _q869 - 1e-09:
            _q1052.stats['fresh_wins'] += 1
            return
        for _q1147, _q970 in enumerate(_q1052.routes):
            _q970.tl = list(_q986[_q1147])
            _q1052._eval(_q1147, _q970)
        _q1052.where = _q987
        _q1052.pool = _q985
        _q1052._calc_shed_free()

    def _actions(_q1052, _q1161):
        tiles = _q1161['tiles']
        acts = []
        for _q1147 in range(_q1052.n_units):
            acts.append(_q1052._unit_action(_q1147, _q1052.routes[_q1147], _q1052.pos[_q1147], tiles))
        return acts

    def _kit_need(_q1052, _q1147, _q970):
        need = []
        nW, nF, A = (_q970.nW, _q970.nF, _q970.A)
        _q741 = _q1052.cfg['lone_h']
        if _q741 and _q1052.n_units == 1 and (_q1052.n_plan == 1) and (_q970.A or _q1052.supply_on):
            _q894, _q896, _q895 = _q1052._route_prefix_needs(_q1147, _q970, _q741)
            A = _q894
            if _q1052.supply_on:
                nW, nF = (_q896, _q895)
        if _q1052.cfg['supply_aware']:
            if nW > _q1052.invW[_q1147]:
                q = nW - _q1052.invW[_q1147]
                spare = _q1052.shed.get('WHEAT', 0) - _q1052.outW
                need.append(('WHEAT', q + max(0, min(_q1052.cfg['margin_w'], spare))))
            if nF > _q1052.invF[_q1147]:
                q = nF - _q1052.invF[_q1147]
                spare = _q1052.shed.get('FERTILIZER', 0) - _q1052.outF
                need.append(('FERTILIZER', q + max(0, min(_q1052.cfg['margin_f'], spare))))
        else:
            if _q970.nW > _q1052.invW[_q1147]:
                need.append(('WHEAT', _q970.nW - _q1052.invW[_q1147] + _q1052.cfg['margin_w']))
            if _q970.nF > _q1052.invF[_q1147]:
                need.append(('FERTILIZER', _q970.nF - _q1052.invF[_q1147] + _q1052.cfg['margin_f']))
        if A:
            h0 = _q1052.cfg['h0_animal_h']
            if h0 and _q1052.hour == 0 and (_q1052.n_units == 1):
                A = _q1052._route_animals_within(_q1147, _q970, h0)
            for k, c in A.items():
                if c > _q1052.invA[_q1147].get(k, 0):
                    need.append((k, c - _q1052.invA[_q1147].get(k, 0)))
        if _q1052.cfg['nosupply_skip']:
            need = [x for x in need if _q1052.shed.get(x[0], 0) > 0]
        return need

    def _route_prefix_needs(_q1052, _q1147, _q970, H):
        """(animals, start WHEAT need, start FERTILIZER need) of the jobs this route starts within H turns."""
        A = {}
        _q1140 = _q970.kt
        _q888 = _q970.sp
        jobs = _q1052.jobs
        _q317 = _q313 = _q762 = _q761 = 0
        for t in _q970.tl:
            _q1140 += D[_q888][t]
            if _q1140 >= H:
                break
            _q681 = jobs[t]
            if _q681.a:
                for k, c in _q681.a.items():
                    A[k] = A.get(k, 0) + c
            _q317 += _q681.dw
            _q313 += _q681.df
            if _q317 > _q762:
                _q762 = _q317
            if _q313 > _q761:
                _q761 = _q313
            _q1140 += _q681.s
            _q888 = t
        return (A, _q762, _q761)

    def _kit_defer(_q1052, _q1147, _q970, _q888):
        """kit_way (B5, first-leg kits).  True -> the unit serves its head job now and fetches its kit later.
        Only the leading jobs it can serve with what it carries qualify (order-aware net WHEAT / FERTILIZER needs,
        carried animals), and never when no later job needs the kit.
          'block': the unit stands on a shed-access tile and the head job is on an access tile - the kit is picked up
                   there afterwards (same turns, same route model; the productive command comes first: a hand's first
                   leg starts with the animals at the shed);
          'way'  : 'block', plus a unit away from the shed defers when fetching the kit between two later jobs (the
                   shed on the way) is strictly shorter than the detour now, and its route slack covers the start-kit
                   charge the route model keeps making meanwhile (the model stays conservative)."""
        tl = _q970.tl
        n = len(tl)
        if not n:
            return False
        jobs = _q1052.jobs
        _q680, _q653 = (_q1052.invW[_q1147], _q1052.invF[_q1147])
        _q654 = _q1052.invA[_q1147]
        cw = cf = 0
        _q1149 = None
        _q710 = 0
        for _q652 in range(n):
            _q681 = jobs.get(tl[_q652])
            if _q681 is None:
                break
            cw += _q681.dw
            cf += _q681.df
            if _q681.w and cw > _q680 or (_q681.f and cf > _q653):
                break
            if _q681.a:
                _q1149 = dict(_q1149) if _q1149 else {}
                short = False
                for k, c in _q681.a.items():
                    _q1149[k] = _q1149.get(k, 0) + c
                    if _q1149[k] > _q654.get(k, 0):
                        short = True
                if short:
                    break
            _q710 = _q652 + 1
        if _q710 == 0 or _q710 >= n:
            return False
        _q661 = _q888 in ACCESS
        if _q661:
            if tl[0] % NT in ACCESS:
                _q1052.stats['kit_defer'] = _q1052.stats.get('kit_defer', 0) + 1
                return True
            return False
        if _q1052.kw != 'way':
            return False
        best = ACC_D[_q888] + D[ACC_NEAR[_q888]][tl[0]] - D[_q888][tl[0]]
        _q364 = 0
        for _q684 in range(1, _q710 + 1):
            x, _q1197 = (tl[_q684 - 1], tl[_q684])
            _q484 = ACC_D[x] + D[ACC_NEAR[x]][_q1197] - D[x][_q1197]
            if _q484 < best:
                best, _q364 = (_q484, _q684)
        if _q364 == 0:
            return False
        if _q1052.cap - _q970.dur < 2 * max((ACC_D[x] for x in tl[:_q364])):
            return False
        _q1052.stats['kit_way'] = _q1052.stats.get('kit_way', 0) + 1
        return True

    def _route_animals_within(_q1052, _q1147, _q970, H):
        """Animals of the PLACE jobs this route starts within H turns (graft from the zones / imitate executors: the
        lone farmer at hour 0 plans provisionally for the whole farm and must not hoard every animal - a carried
        animal pins its PLACE job to the carrier, so the hands that appear next turn could not take them)."""
        A = {}
        _q1140 = _q970.kt
        _q888 = _q970.sp
        jobs = _q1052.jobs
        for t in _q970.tl:
            _q1140 += D[_q888][t]
            if _q1140 >= H:
                break
            _q681 = jobs[t]
            if _q681.a:
                for k, c in _q681.a.items():
                    A[k] = A.get(k, 0) + c
            _q1140 += _q681.s
            _q888 = t
        return A

    def _unit_action(_q1052, _q1147, _q970, _q888, tiles):
        while _q970.tl and _q970.tl[0] not in _q1052.chains:
            t = _q970.tl.pop(0)
            _q1052.where.pop(t, None)
        if _q1052.dlv_t and _q1052.dlv_t.get(_q1147):
            if _q888 in ACCESS:
                _q679 = _q1052.cur_inv[_q1147] if _q1147 < len(_q1052.cur_inv) else {}
                _q677 = [(_q679.get(_q675, 0), _q675) for _q675 in _q1052.dlv_cfg['items'] if _q679.get(_q675, 0) > 0]
                if _q677:
                    q, _q675 = max(_q677)
                    _q1052.stats['dlv_place'] = _q1052.stats.get('dlv_place', 0) + 1
                    return ['PLACE', _q675, int(q)]
            else:
                return [_step(_q888, ACC_NEAR[_q888])]
        if not _q970.tl:
            _q1052._eval(_q1147, _q970)
            return _q1052._idle_action(_q1147, _q888)
        need = _q1052._kit_need(_q1147, _q970)
        if need and _q1052.kw and _q1052._kit_defer(_q1147, _q970, _q888):
            need = None
        if need:
            if _q888 in ACCESS:
                need.sort(key=lambda x: (x[0] not in ANIMALS, -x[1]))
                for item, q in need:
                    avail = _q1052.shed.get(item, 0)
                    if avail > 0:
                        return ['PICKUP', item, int(min(q, avail))]
            else:
                _q1052.stats['detours'] += 1
                return [_step(_q888, ACC_NEAR[_q888])]
        t = _q970.tl[0]
        if _q888 != t % NT:
            return [_step(_q888, t)]
        _q681 = _q1052.jobs[t]
        _q428 = _q1052.chains[t]
        if _q681.pre in ('dig', 'harvest'):
            _q1052.stats['recover'] += 1
            _q439 = 'DIG' if _q681.pre == 'dig' else 'HARVEST'
            _q681.pre = None
            _q681.s = len(_q428)
            _q1052._served(_q1147, t)
            _q1052._svc.add(_q1147)
            return [_q439]
        op, arg = _q428[0]
        if op == 'FEED' and _q1052.invW[_q1147] <= 0 or (op == 'FERTILIZE' and _q1052.invF[_q1147] <= 0) or (op == 'PLACE' and _q1052.invA[_q1147].get(arg, 0) <= 0):
            item = 'WHEAT' if op == 'FEED' else 'FERTILIZER' if op == 'FERTILIZE' else arg
            if _q1052.cfg['supply_aware'] and _q1052.shed.get(item, 0) <= 0 and (item in ('WHEAT', 'FERTILIZER')) and _q1052._spare_elsewhere(_q1147, item):
                _q1052.stats['handback'] = _q1052.stats.get('handback', 0) + 1
                _q970.tl.pop(0)
                _q1052.where.pop(t, None)
                _q1052.pool.add(t)
                return _q1052._unit_action(_q1147, _q970, _q888, tiles)
            if _q1052.cfg['nosupply_skip'] and _q1052.shed.get(item, 0) <= 0:
                if _q1052.wait_on and op == 'PLACE' and (_q1052.pending_buys.get(arg, 0) > 0):
                    _q1052.stats['place_wait'] = _q1052.stats.get('place_wait', 0) + 1
                    _q970.tl.pop(0)
                    _q1052.where.pop(t, None)
                    _q1052.pool.add(t)
                    return _q1052._unit_action(_q1147, _q970, _q888, tiles)
                _q1052.stats['nosupply'] += 1
                _q428.pop(0)
                if not _q428:
                    _q1052.chains.pop(t, None)
                    _q970.tl.pop(0)
                    _q1052.where.pop(t, None)
                    _q1052.jobs.pop(t, None)
                    return _q1052._unit_action(_q1147, _q970, _q888, tiles)
                _q681.s = len(_q428)
                return _q1052._unit_action(_q1147, _q970, _q888, tiles)
            _q1052.stats['detours'] += 1
            if _q888 in ACCESS:
                item = 'WHEAT' if op == 'FEED' else 'FERTILIZER' if op == 'FERTILIZE' else arg
                return ['PICKUP', item, 1 + (_q1052.cfg['margin_w'] if op == 'FEED' else 0)]
            return [_step(_q888, ACC_NEAR[_q888])]
        _q428.pop(0)
        if op == 'FEED':
            _q1052.invW[_q1147] -= 1
        elif op == 'FERTILIZE':
            _q1052.invF[_q1147] -= 1
        elif op == 'PLACE':
            _q1052.invA[_q1147][arg] -= 1
        _q1052._served(_q1147, t)
        _q1052._svc.add(_q1147)
        if not _q428:
            _q1052.chains.pop(t, None)
            _q970.tl.pop(0)
            _q1052.where.pop(t, None)
            _q1052.jobs.pop(t, None)
        else:
            _q681.s = len(_q428)
        if arg is None or arg == '_aux':
            return [op]
        return [op, arg]

    def _spare_elsewhere(_q1052, _q1147, item):
        for _q1159 in range(_q1052.n_units):
            if _q1159 == _q1147:
                continue
            _q1027 = _q1052.routes[_q1159]
            if item == 'WHEAT' and _q1052.invW[_q1159] > _q1027.nW:
                return True
            if item == 'FERTILIZER' and _q1052.invF[_q1159] > _q1027.nF:
                return True
        return False

    def _served(_q1052, _q1147, t):
        s = _q1052.served.setdefault(_q1147, [])
        if t not in s:
            s.append(t)

    def _idle_action(_q1052, _q1147, _q888):
        if _q1052.cfg['prepos'] and _q1052.locked:
            _q745 = _q1052.locked - _q1052.held if _q1052.held else _q1052.locked
            if _q745:
                _q1120 = min(_q745, key=lambda t: (D[_q888][t], t))
                if D[_q888][_q1120] > 1:
                    return [_step(_q888, _q1120)]
        return ['PASS']
EDFKitsExecutor = PDExecutor