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
ACCESS = frozenset((_q1272 * B + x for x, _q1272 in ACCESS_XY))
ACC_ORDER = tuple((_q1272 * B + x for x, _q1272 in ACCESS_XY))
D = [[abs(a % B - b % B) + abs(a // B - b // B) for b in range(NT)] for a in range(NT)]
ACC_NEAR = [min(sorted(ACCESS), key=lambda s, t=t: D[t][s]) for t in range(NT)]
ACC_D = [D[t][ACC_NEAR[t]] for t in range(NT)]
CENTER_D = ACC_D
NEG = -10 ** 9
SUPPLY_EASY = 200
NEAR = [sorted(range(NT), key=lambda b, a=a: (D[a][b], b)) for a in range(NT)]
RING = {_q1040: [[b for b in NEAR[a] if 0 < D[a][b] <= _q1040] for a in range(NT)] for _q1040 in (1, 2, 3, 4)}
XY = [(t % B, t // B) for t in range(NT)]

class _Sub(int):
    """B5 split_collect: id of the COLLECT_FERTILIZER sub-job of animal tile t.  Its integer value IS the tile (so the
    geometry tables D / XY / NEAR, tiles[t // B][t % B] and _step work unchanged, also in pd_layer, which reads
    ex.routes[u].tl / ex.chains with tile arithmetic); equality is type-strict and the hash distinct, so it is a
    separate key in chains / jobs / where / pool and a separate element in route lists."""
    __slots__ = ()

    def __eq__(_q1120, _q922):
        return type(_q922) is _Sub and int.__eq__(_q1120, _q922)

    def __ne__(_q1120, _q922):
        return not (type(_q922) is _Sub and int.__eq__(_q1120, _q922))

    def __hash__(_q1120):
        return NT + int(_q1120)

    def __repr__(_q1120):
        return 'S%d' % int(_q1120)
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

def _step(_q954, t):
    """One Manhattan step from tile p towards tile t (x first)."""
    px, _q1027 = (_q954 % B, _q954 // B)
    _q1218, _q1219 = (t % B, t // B)
    if px < _q1218:
        return 'EAST'
    if px > _q1218:
        return 'WEST'
    if _q1027 < _q1219:
        return 'SOUTH'
    if _q1027 > _q1219:
        return 'NORTH'
    return None

def head_state(tile, op, arg, day, recover=True):
    """'ok' executable now | 'dig' / 'harvest' = one clearing command first | 'moot' | 'locked'."""
    if tile == 'LOCKED':
        return 'locked'
    _q736 = isinstance(tile, dict)
    kind = tile.get('kind') if _q736 else None
    if op == 'WATER':
        return 'ok' if kind == 'PLANT' and (not tile.get('watered_today')) else 'moot'
    if op == 'HARVEST':
        if not _q736 or tile.get('yield_units', 0) <= 0:
            return 'moot'
        if kind == 'PLANT' and day - tile.get('planted_day', day) < CROPS[tile['crop']]['first_yield_day']:
            return 'moot'
        return 'ok'
    if op == 'FERTILIZE':
        return 'ok' if kind == 'PLANT' else 'moot'
    if op == 'FEED':
        return 'ok' if _q736 and tile.get('animal') and (not tile.get('fed_today')) else 'moot'
    if op == 'CARE':
        return 'ok' if _q736 and tile.get('animal') and (not tile.get('cared_today')) else 'moot'
    if op == 'COLLECT_FERTILIZER':
        return 'ok' if _q736 and tile.get('animal') and tile.get('fertilizer_available') else 'moot'
    if op == 'PLACE':
        if _q736 and kind == STRUCT.get(arg) and (not tile.get('animal')):
            return 'ok'
        return 'moot'
    if op == 'DIG':
        return 'ok' if tile is not None and (not (_q736 and tile.get('animal'))) else 'moot'
    if op == 'PLANT' or op in BUILD_OPS:
        if tile is None:
            return 'ok'
        if kind == 'WEED':
            return 'dig'
        if not recover or (_q736 and tile.get('animal')):
            return 'moot'
        if kind == 'PLANT':
            _q474 = CROPS[tile['crop']]
            if not _q474['ongoing'] and tile.get('yield_units', 0) > 0 and (day - tile.get('planted_day', day) >= _q474['first_yield_day']):
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

    def __init__(_q1120, t, chain):
        _q1120.t = t
        _q1120.chain = chain
        _q1120.s = len(chain)
        _q1120.w = 0
        _q1120.f = 0
        _q1120.a = None
        _q1120.val = 1.0
        _q1120.crit = False
        _q1120.urg = 0.0
        _q1120.pre = None
        _q1120.dw = 0
        _q1120.df = 0

class Route:
    __slots__ = ('tl', 'W', 'F', 'A', 'inner', 'serv', 'dur', 'kt', 'sp', 'cw', 'pmw', 'smw', 'cf', 'pmf', 'smf', 'nW', 'nF', 'bb', 'ug', 'oW', 'oF')

    def __init__(_q1120):
        _q1120.tl = []
        _q1120.W = 0
        _q1120.F = 0
        _q1120.A = {}
        _q1120.inner = 0
        _q1120.serv = 0
        _q1120.dur = 0
        _q1120.kt = 0
        _q1120.sp = -1
        _q1120.cw = []
        _q1120.pmw = [0]
        _q1120.smw = [NEG]
        _q1120.cf = []
        _q1120.pmf = [0]
        _q1120.smf = [NEG]
        _q1120.nW = 0
        _q1120.nF = 0
        _q1120.bb = (0, 9, 0, 9)
        _q1120.ug = False
        _q1120.oW = 0
        _q1120.oF = 0
_SNAP = ('W', 'F', 'A', 'inner', 'serv', 'dur', 'kt', 'sp', 'cw', 'pmw', 'smw', 'cf', 'pmf', 'smf', 'nW', 'nF', 'bb', 'ug', 'oW', 'oF')

def _snap(_q1036):
    """Route state for an exact restore: _eval replaces (never mutates) the aggregate lists / dicts, so references
    suffice; the tile list is mutated in place and is copied."""
    return (list(_q1036.tl), _q1036.W, _q1036.F, _q1036.A, _q1036.inner, _q1036.serv, _q1036.dur, _q1036.kt, _q1036.sp, _q1036.cw, _q1036.pmw, _q1036.smw, _q1036.cf, _q1036.pmf, _q1036.smf, _q1036.nW, _q1036.nF, _q1036.bb, _q1036.ug, _q1036.oW, _q1036.oF)

def _restore(_q1036, _q1146):
    _q1036.tl, _q1036.W, _q1036.F, _q1036.A, _q1036.inner, _q1036.serv, _q1036.dur, _q1036.kt, _q1036.sp, _q1036.cw, _q1036.pmw, _q1036.smw, _q1036.cf, _q1036.pmf, _q1036.smf, _q1036.nW, _q1036.nF, _q1036.bb, _q1036.ug, _q1036.oW, _q1036.oF = _q1146

def _addA(A, a, _q1132=1):
    if not a:
        return A
    _q2 = dict(A)
    for k, _q1233 in a.items():
        n = _q2.get(k, 0) + _q1132 * _q1233
        if n:
            _q2[k] = n
        else:
            _q2.pop(k, None)
    return _q2

class PDExecutor:

    def __init__(_q1120, cfg=None):
        _q1120.cfg = dict(DEFAULT_CFG)
        if cfg:
            _q1120.cfg.update(cfg)
        _q1120.day = -1
        _q1120.template = {}
        _q1120.missed_prev = {}
        _q1120.is_tight = False
        _q1120.eval_charge = _q1120.cfg['eval_charge']
        _q1120.prev_hands = 0
        _q1120.n_plan = 0
        _q1120.n_units = 0
        _q1120.max_units = 0
        _q1120.delay = []
        _q1120.outW = _q1120.outF = 0
        _q1120.supply_on = False
        _q1120.shed = {}
        _q1120.invW, _q1120.invF, _q1120.invA = ([], [], [])
        _q1120.dlv_t = {}
        _q1120.dlv_on = set()
        _q1120.cur_inv = []
        _q1120.stats = {'evals': 0, 'replans': 0, 'fresh_wins': 0, 'ejects': 0, 'detours': 0, 'recover': 0, 'overflow_drops': 0, 'ls_moves': 0, 'rr_iter': 0, 'rr_acc': 0, 'rescue_jobs': 0, 'nosupply': 0}
        _q554 = _q1120.cfg.get('deliver')
        if isinstance(_q554, str):
            _q554 = DELIVER_PRESETS.get(_q554)
        if _q554 and _q1120.cfg.get('deliver_items'):
            _q554 = dict(_q554, items=tuple(_q1120.cfg['deliver_items']))
        _q1120.dlv_cfg = _q554
        _q1120.split_on = bool(_q1120.cfg.get('split_collect'))
        if _q1120.split_on and _q1120.cfg.get('split_collect') != 'free':
            _q1120._best_insert = _q1120._best_insert_split
        _q1120.fb = float(_q1120.cfg.get('f_shed_w') or 0.0)
        if _q1120.fb:
            _q1120._cost = _q1120._cost_fb
            _q1120._best_insert_kit = _q1120._best_insert_kit_fb
        hb = _q1120.cfg.get('harv_batch')
        _q1120.hb = dict(HARV_BATCH) if hb is True else dict(hb) if hb else None
        _q775 = _q1120.cfg.get('kit_way') or None
        _q1120.kw = 'way' if _q775 is True else _q775
        _q1120.wait_on = _q1120.cfg.get('nosupply_skip') == 'wait'
        _q1120.pending_buys = {}
        _q1120.harv_need = frozenset(_q1120.cfg.get('harv_need') or ())
        _q1120.held = frozenset()
        _q1120.chains = {}
        _q1120.jobs = {}
        _q1120.routes = []
        _q1120.where = {}
        _q1120.pool = set()
        _q1120.locked = set()
        _q1120.res_set = set()
        _q1120._svc = set()
        _q1120._snap = None
        _q1120._hb_new = set()
        _q1120.ret = False
        _q1120.tiles = None

    def begin_day(_q1120, day, tasks):
        """tasks: {(x, y): [(op, arg), ...]} - today's task list (logical order per tile, nothing else)."""
        _q1120.day = day
        _q1120.chains = {}
        for (x, _q1272), ts in tasks.items():
            if ts:
                _q1120.chains[_q1272 * B + x] = [tuple(t) for t in ts]
        if _q1120.split_on:
            for t in list(_q1120.chains):
                _q1120._split_one(t)
        _q1120._svc = set()
        _q1120._snap = None
        _q1120._hb_new = set()
        _q1120.jobs = {}
        _q1120.routes = []
        _q1120.where = {}
        _q1120.pool = set()
        _q1120.locked = set()
        _q1120.reserved = {}
        _q1120.res_set = set()
        _q1120.served = {}
        _q1120.n_units = 0
        _q1120.n_plan = 0
        _q1120.max_units = 0
        _q1120.hour = -1
        _q1120.started = False
        _q1120.is_tight = False
        _q1120.eval_charge = _q1120.cfg['eval_charge']
        _q1120.dlv_t = {}
        _q1120.dlv_on = set()

    def end_day(_q1120):
        """Keep today's served order per unit index as tomorrow's warm-start template, and the WATER / FEED tasks
        this executor did not do today (its own record) for tomorrow's rescue check."""
        _q1120.template = {_q1221: list(tl) for _q1221, tl in _q1120.served.items() if tl}
        _q1120.prev_hands = max(0, _q1120.max_units - 1)
        mp = {}
        for t, _q481 in _q1120.chains.items():
            ops = {op for op, _ in _q481 if op in ('WATER', 'FEED')}
            if ops:
                mp[t] = ops
        _q1120.missed_prev = mp

    def _add_rescues(_q1120, tiles):
        """A WATER / FEED this executor missed yesterday leaves the plant / animal one miss from dying tonight.  If
        today's list has no such op on that tile (the plan skips it today) and the tile is not cleared today, add one
        auxiliary op (flagged arg '_aux'; the command is issued without it)."""
        for t, ops in _q1120.missed_prev.items():
            tile = tiles[t // B][t % B]
            if not isinstance(tile, dict):
                continue
            _q481 = _q1120.chains.get(t, [])
            _q507 = [op for op, _ in _q481]
            if 'WATER' in ops and tile.get('kind') == 'PLANT' and (tile.get('consecutive_unwatered', 0) >= 1) and ('WATER' not in _q507) and ('PLANT' not in _q507) and ('DIG' not in _q507):
                _q474 = CROPS.get(tile.get('crop'))
                if _q474 and (not _q474['ongoing']) and ('HARVEST' in _q507):
                    continue
                _q1120.chains[t] = [('WATER', '_aux')] + _q481
                _q1120.stats['rescue_jobs'] += 1
            elif 'FEED' in ops and tile.get('animal') and (tile.get('consecutive_unfed', 0) >= 1) and ('FEED' not in _q507):
                _q1120.chains[t] = [('FEED', '_aux')] + _q481
                _q1120.stats['rescue_jobs'] += 1

    def _split_one(_q1120, t):
        """split_collect: move the COLLECT_FERTILIZER ops of a mixed (animal) chain on tile t to the collect sub-job
        SUBS[t]; the herd job keeps FEED / CARE / HARVEST / ... in their order.  A collect-only chain stays whole."""
        if type(t) is _Sub:
            return
        _q481 = _q1120.chains.get(t)
        if not _q481 or len(_q481) < 2:
            return
        _q498 = [x for x in _q481 if x[0] == 'COLLECT_FERTILIZER']
        if not _q498 or len(_q498) == len(_q481):
            return
        _q1120.chains[t] = [x for x in _q481 if x[0] != 'COLLECT_FERTILIZER']
        s = SUBS[t]
        prev = _q1120.chains.get(s)
        _q1120.chains[s] = prev + _q498 if prev else _q498
        _q1120.stats['split_jobs'] = _q1120.stats.get('split_jobs', 0) + 1

    def _harv_filter(_q1120, tiles, _q765):
        """harv_batch: drop today's HARVEST of a batch animal (cow / sheep by default) holding fewer units than one full
        production, unless tonight's production would overflow max_held, the animal may escape tonight (unfed
        yesterday and no FEED in its chain), the product is needed now, or day >= harv_last_day."""
        hb = _q1120.hb
        if not hb or _q1120.day >= int(_q1120.cfg.get('harv_last_day') or 0):
            return
        need = _q1120.harv_need
        for t in _q765:
            _q481 = _q1120.chains.get(t)
            if not _q481 or not any((op == 'HARVEST' for op, _ in _q481)):
                continue
            tile = tiles[t // B][t % B]
            if not isinstance(tile, dict):
                continue
            _q388 = tile.get('animal')
            _q843 = hb.get(_q388) if _q388 else None
            if not _q843:
                continue
            _q1272 = tile.get('yield_units', 0)
            if _q1272 <= 0 or _q1272 >= _q843 or ANIMAL_ITEM.get(_q388) in need:
                continue
            _q629, _q740, cap = ANIMAL_INFO[_q388]
            _q566 = _q1120.day + 1 - tile.get('placed_day', _q1120.day) - _q629
            if _q566 >= 0 and _q566 % _q740 == 0 and (_q1272 + 1 + tile.get('pending_care_bonus', 0) > cap):
                continue
            if tile.get('consecutive_unfed', 0) >= 1 and (not tile.get('fed_today')) and (not any((op == 'FEED' for op, _ in _q481))):
                continue
            rest = [x for x in _q481 if x[0] != 'HARVEST']
            if rest:
                _q1120.chains[t] = rest
            else:
                _q1120.chains.pop(t, None)
            _q1120.stats['harv_skip'] = _q1120.stats.get('harv_skip', 0) + 1
            _q1120.stats['harv_skip_units'] = _q1120.stats.get('harv_skip_units', 0) + _q1272

    def note_buys(_q1120, pending):
        """{animal: n} bought and not yet in the shed (cfg nosupply_skip 'wait'); replaces the previous record."""
        _q1120.pending_buys = dict(pending or {})

    def add_chain(_q1120, tile, ops, _q1056=False):
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
        _q481 = _q1120.chains.get(t)
        if _q481 and (not _q1056):
            _q481.extend(new)
        else:
            _q1120.chains[t] = new
        if _q1120.split_on:
            _q1120._split_one(t)
        if _q1120.hb:
            _q1120._hb_new.add(t)
        return True

    def pending_ops(_q1120):
        """{op: count} of every op still held in today's chains (routes, pool, locked, reserved, collect sub-jobs)."""
        c = {}
        for _q481 in _q1120.chains.values():
            for op, _ in _q481:
                c[op] = c.get(op, 0) + 1
        return c

    def slack(_q1120):
        """{unit: free turns} after this step's commands: turns left today minus the rest of the unit's route
        (cap - dur of the route as planned at command time; an idle unit: the turns left).  Virtual (forecast) units
        are included (unit >= n_units)."""
        if not _q1120._snap:
            return {}
        cap, rows = _q1120._snap
        return {_q1221: max(0, cap - _q530 if ne else cap - 1) for _q1221, (_q530, ne) in enumerate(rows)}

    def route_ops(_q1120, H, _q1013=False):
        """[(unit, eta, (x, y), op, arg)] for the ops the routes start within H turns (eta < H), eta counted from the
        NEXT step (0 = the unit's command at step t+1 when called after act() of step t).  The _route_prefix_needs walk
        over the route model of this step (kit turns, travel, one turn per op; a clearing DIG / HARVEST before a
        PLANT / BUILD is listed as that op with arg None).  Virtual units are included unless present_only."""
        _q946 = []
        _q1175 = _q1120._svc
        jobs = _q1120.jobs
        chains = _q1120.chains
        U = _q1120.n_units if _q1013 else len(_q1120.routes)
        for _q1221 in range(min(U, len(_q1120.routes))):
            _q1036 = _q1120.routes[_q1221]
            if not _q1036.tl:
                continue
            _q1214 = _q1036.kt - (0 if _q1221 in _q1175 else 1)
            _q954 = _q1036.sp
            for t in _q1036.tl:
                _q743 = jobs.get(t)
                _q481 = chains.get(t)
                if _q743 is None or not _q481:
                    continue
                _q1214 += D[_q954][t]
                _q954 = t
                if _q1214 >= H:
                    break
                _q1196 = int(t)
                xy = (_q1196 % B, _q1196 // B)
                _q575 = _q1214
                if _q743.pre in ('dig', 'harvest'):
                    _q946.append((_q1221, max(0, _q575), xy, 'DIG' if _q743.pre == 'dig' else 'HARVEST', None))
                    _q575 += 1
                for op, arg in _q481:
                    if _q575 >= H:
                        break
                    _q946.append((_q1221, max(0, _q575), xy, op, None if arg == '_aux' else arg))
                    _q575 += 1
                _q1214 += _q743.s
        return _q946

    def _job_value(_q1120, _q743, tile):
        rem = max(0, 29 - _q1120.day)
        _q1233 = 0.0
        crit = False
        ops = [op for op, _ in _q743.chain]
        for op, arg in _q743.chain:
            _q1233 += 1.0
            if op == 'PLANT':
                _q1233 += min(PLANT_CASCADE.get(arg, 5.0), 1.2 * rem)
                crit = True
            elif op == 'PLACE':
                _q1233 += 3.3 * rem
                crit = True
            elif op == 'HARVEST':
                if isinstance(tile, dict) and tile.get('crop', 'X') != 'WHEAT':
                    _q1233 += 1.0
        urg = 0.0
        if isinstance(tile, dict):
            k = tile.get('kind')
            if k == 'PLANT':
                _q474 = CROPS[tile['crop']]
                age = _q1120.day - tile.get('planted_day', _q1120.day)
                if 'WATER' in ops and tile.get('consecutive_unwatered', 0) >= 1:
                    if _q474['ongoing']:
                        _q804 = _q474['first_yield_day'] + _q474['interval'] * _q474['max_yield'] + 1
                    else:
                        _q804 = _q474['max_yield_day'] + 1
                    _q1233 += max(1.0, 1.2 * (_q804 - age))
                    crit = True
                mls = tile.get('max_lifespan_step', -1)
                if 'HARVEST' in ops and 0 <= mls <= 24 * (_q1120.day + 1):
                    urg = 1.0
            elif tile.get('animal'):
                if 'FEED' in ops and tile.get('consecutive_unfed', 0) >= 1:
                    _q1233 += 3.3 * rem
                    crit = True
            _q582 = _q1120.cfg.get('early_items')
            if _q582 and 'HARVEST' in ops and (not urg):
                item = tile.get('crop') if k == 'PLANT' else {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}.get(tile.get('animal'))
                if item in _q582 and tile.get('yield_units', 0) > 0:
                    urg = float(_q1120.cfg.get('early_urg') or 0.0)
        _q743.crit = crit or _q1233 >= _q1120.cfg['crit_thresh'] * max(1, len(_q743.chain))
        pw = _q1120.cfg['prod_w']
        if pw:
            _q1233 += pw * _q1120._prod_units(_q743, tile, ops)
        _q743.val = _q1233
        _q743.urg = urg

    @staticmethod
    def _prod_night(_q474, tile, x):
        """Does an ongoing crop produce in the refresh after day x?"""
        _q566 = x + 1 - tile.get('planted_day', x) - _q474['first_yield_day']
        if _q566 < 0 or _q566 % _q474['interval']:
            return False
        return _q566 // _q474['interval'] + 1 <= _q474['max_yield']

    def _prod_units(_q1120, _q743, tile, ops):
        """Production units at stake if this job is skipped today (engine formulas; wheat down-weighted)."""
        if not isinstance(tile, dict):
            return 0.0
        day = _q1120.day
        units = 0.0
        if tile.get('kind') == 'PLANT':
            crop = tile['crop']
            _q474 = CROPS[crop]
            _q850 = _q1120.cfg['prod_wheat'] if crop == 'WHEAT' else 1.0
            if _q1120.cfg['prices']:
                _q850 = _q1120._pw(crop)
            _q978 = tile.get('planted_day', day)
            age = day - _q978
            _q654 = tile.get('fertilized_until_day', -1)
            _q619 = _q654 >= day or 'FERTILIZE' in ops
            _q1265 = (_q474['max_yield_day'] + 1) // 2
            if 'WATER' in ops and (not tile.get('watered_today')):
                if not _q474['ongoing']:
                    if _q1265 <= age <= _q474['max_yield_day'] and tile.get('yield_units', 0) < _q474['max_yield']:
                        units += 2.0 if _q619 else 1.0
                elif _q619 and _q1120._prod_night(_q474, tile, day):
                    units += 1.0
            if 'FERTILIZE' in ops:
                for x in (day, day + 1, day + 2):
                    if x <= _q654:
                        continue
                    if _q474['ongoing']:
                        if _q1120._prod_night(_q474, tile, x):
                            units += 1.0
                    elif _q1265 <= x - _q978 <= _q474['max_yield_day']:
                        units += 1.0
            if 'HARVEST' in ops:
                _q1272 = tile.get('yield_units', 0)
                if _q474['ongoing']:
                    _q921 = (2 if _q619 else 1) if _q1120._prod_night(_q474, tile, day) else 0
                    units += max(0, _q1272 + _q921 - _q474['max_yield'])
                else:
                    mls = tile.get('max_lifespan_step', -1)
                    if 0 <= mls <= 24 * (day + 1):
                        if _q1120.cfg.get('rot_full') and mls <= 24 * day + getattr(_q1120, 'hour', 0):
                            units += float(_q1272)
                        else:
                            units += 0.5 * _q1272
            return units * _q850
        _q388 = tile.get('animal')
        if _q388:
            _q629, _q740, cap = ANIMAL_INFO[_q388]
            _q566 = day + 1 - tile.get('placed_day', day) - _q629
            prod = _q566 >= 0 and _q566 % _q740 == 0
            fed = tile.get('fed_today') or 'FEED' in ops
            if 'CARE' in ops and (not tile.get('cared_today')) and fed:
                units += 1.0
            if prod and 'FEED' in ops and (not tile.get('fed_today')):
                units += tile.get('pending_care_bonus', 0)
            if 'HARVEST' in ops:
                _q1272 = tile.get('yield_units', 0)
                units += max(0, _q1272 + (1 + tile.get('pending_care_bonus', 0) if prod else 0) - cap)
            if _q1120.cfg['prices']:
                _q1019 = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}.get(_q388)
                units *= _q1120._pw(_q1019)
                if 'COLLECT_FERTILIZER' in ops and tile.get('fertilizer_available'):
                    units += _q1120._pw('FERTILIZER')
        return units

    def _pw(_q1120, item):
        """Price weight of one unit of item (M2: quote / price_ref, capped)."""
        px = _q1120.cfg['prices'].get(item)
        if not px:
            return 1.0
        return min(_q1120.cfg['price_cap'], float(px) / _q1120.cfg['price_ref'])

    def _refresh_job(_q1120, t, tiles):
        """Drop moot heads; recompute service / needs / value.  Returns the Job or None (chain done)."""
        _q481 = _q1120.chains.get(t)
        tile = tiles[t // B][t % B]
        rec = _q1120.cfg['recover']
        pre = None
        while _q481:
            st = head_state(tile, _q481[0][0], _q481[0][1], _q1120.day, rec)
            if st == 'moot':
                _q481.pop(0)
                continue
            if st != 'ok':
                pre = st
            break
        if not _q481:
            _q1120.chains.pop(t, None)
            return None
        _q743 = _q1120.jobs.get(t)
        if _q743 is None:
            _q743 = Job(t, _q481)
            _q1120.jobs[t] = _q743
        _q743.chain = _q481
        _q743.pre = pre
        _q743.s = len(_q481) + (1 if pre in ('dig', 'harvest') else 0)
        w = f = 0
        a = None
        for op, arg in _q481:
            if op == 'FEED':
                w += 1
            elif op == 'FERTILIZE':
                f += 1
            elif op == 'PLACE':
                if a is None:
                    a = {}
                a[arg] = a.get(arg, 0) + 1
        _q743.w, _q743.f, _q743.a = (w, f, a)
        sw = _q1122 = 0
        if _q1120.cfg['credit'] and isinstance(tile, dict):
            if tile.get('animal'):
                if tile.get('fertilizer_available'):
                    _q1122 = sum((1 for op, _ in _q481 if op == 'COLLECT_FERTILIZER'))
            elif tile.get('kind') == 'PLANT' and tile.get('crop') == 'WHEAT' and any((op == 'HARVEST' for op, _ in _q481)):
                sw = max(0, tile.get('yield_units', 0) - 1)
        _q743.dw = w - sw
        _q743.df = f - _q1122
        _q1120._job_value(_q743, tile)
        if _q1120.split_on and type(t) is _Sub and _q1120.cfg.get('split_val'):
            _q743.val += float(_q1120.cfg['split_val'])
        return _q743

    def _kit(_q1120, _q1221, W, F, A):
        """(kit turns, start tile) for a route with needs W / F / A for unit u."""
        kt = _q1120.dlv_t.get(_q1221, 0) if _q1120.dlv_t else 0
        if W > _q1120.invW[_q1221]:
            kt += 1
        if F > _q1120.invF[_q1221]:
            kt += 1
        if A:
            _q715 = _q1120.invA[_q1221]
            for k, c in A.items():
                if c > _q715.get(k, 0):
                    kt += 1
        _q954 = _q1120.pos[_q1221]
        _q554 = _q1120.delay[_q1221]
        if kt:
            if _q954 in ACCESS:
                return (kt + _q554, _q954)
            return (ACC_D[_q954] + kt + _q554, ACC_NEAR[_q954])
        return (_q554, _q954)

    def _late(_q1120, _q1221, _q1036):
        """Soft lateness cost of decaying harvests in route order."""
        _q821 = _q1120.cfg['late_w']
        if not _q821:
            return 0.0
        jobs = _q1120.jobs
        tl = _q1036.tl
        c = 0.0
        _q1214 = _q1036.kt
        _q954 = _q1036.sp
        _q700 = False
        for t in tl:
            _q743 = jobs[t]
            _q1214 += D[_q954][t] + _q743.s
            _q954 = t
            if _q743.urg:
                c += _q821 * _q1214 * _q743.urg
                _q700 = True
        return c if _q700 else 0.0

    def _eval(_q1120, _q1221, _q1036):
        """Full recomputation of a route's aggregates (incl. the order-aware kit prefix / suffix maxima)."""
        tl = _q1036.tl
        jobs = _q1120.jobs
        W = F = S = I = 0
        A = {}
        prev = -1
        n = len(tl)
        _q1120.evals += _q1120.eval_charge * n
        cw = [0] * n
        cf = [0] * n
        pmw = [0] * (n + 1)
        pmf = [0] * (n + 1)
        _q367 = _q363 = 0
        _q824 = _q823 = 0
        ug = False
        for _q712, t in enumerate(tl):
            _q743 = jobs[t]
            if _q743.urg:
                ug = True
            W += _q743.w
            F += _q743.f
            S += _q743.s
            if _q743.a:
                for k, _q1233 in _q743.a.items():
                    A[k] = A.get(k, 0) + _q1233
            if prev >= 0:
                I += D[prev][t]
            prev = t
            pmw[_q712] = _q824
            pmf[_q712] = _q823
            _q367 += _q743.dw
            _q363 += _q743.df
            cw[_q712] = _q367
            cf[_q712] = _q363
            if _q367 > _q824:
                _q824 = _q367
            if _q363 > _q823:
                _q823 = _q363
        pmw[n] = _q824
        pmf[n] = _q823
        smw = [NEG] * (n + 1)
        smf = [NEG] * (n + 1)
        for _q712 in range(n - 1, -1, -1):
            smw[_q712] = cw[_q712] if cw[_q712] > smw[_q712 + 1] else smw[_q712 + 1]
            smf[_q712] = cf[_q712] if cf[_q712] > smf[_q712 + 1] else smf[_q712 + 1]
        _q1036.cw, _q1036.pmw, _q1036.smw, _q1036.cf, _q1036.pmf, _q1036.smf = (cw, pmw, smw, cf, pmf, smf)
        _q1036.nW, _q1036.nF = (_q824, _q823)
        _q1036.W, _q1036.F, _q1036.A, _q1036.serv, _q1036.inner = (W, F, A, S, I)
        _q1036.ug = ug
        _q948 = _q824 - _q1120.invW[_q1221]
        if _q948 < 0:
            _q948 = 0
        _q931 = _q823 - _q1120.invF[_q1221]
        if _q931 < 0:
            _q931 = 0
        _q1120.outW += _q948 - _q1036.oW
        _q1120.outF += _q931 - _q1036.oF
        _q1036.oW, _q1036.oF = (_q948, _q931)
        if tl:
            kt, sp = _q1120._kit(_q1221, _q824, _q823, A)
            _q1036.kt, _q1036.sp = (kt, sp)
            _q1036.dur = kt + D[sp][tl[0]] + I + S
            if _q1120.ret:
                _q1036.dur += ACC_D[tl[-1]] + 1
            _q1266 = _q1267 = sp % B
            _q1273 = _q1274 = sp // B
            for t in tl:
                x, _q1272 = XY[t]
                if x < _q1266:
                    _q1266 = x
                elif x > _q1267:
                    _q1267 = x
                if _q1272 < _q1273:
                    _q1273 = _q1272
                elif _q1272 > _q1274:
                    _q1274 = _q1272
            _q1036.bb = (_q1266, _q1267, _q1273, _q1274)
        else:
            _q954 = _q1120.pos[_q1221]
            _q1036.kt, _q1036.sp = (_q1120.delay[_q1221], _q954)
            _q1036.dur = 0
            _q1036.bb = (_q954 % B, _q954 % B, _q954 // B, _q954 // B)
        return _q1036.dur

    def _cost(_q1120, _q1221, _q1036):
        if not _q1036.ug:
            return _q1036.dur
        return _q1036.dur + (_q1120._late(_q1221, _q1036) if _q1120.cfg['late_w'] else 0.0)

    def _cost_fb(_q1120, _q1221, _q1036):
        """_cost with the B5 f_shed_w objective: + fb per FERTILIZER unit the unit must draw from the shed (r.oF).
        Bound over _cost in __init__ when f_shed_w > 0."""
        if not _q1036.ug:
            return _q1036.dur + _q1120.fb * _q1036.oF
        return _q1036.dur + (_q1120._late(_q1221, _q1036) if _q1120.cfg['late_w'] else 0.0) + _q1120.fb * _q1036.oF

    def _animal_ok(_q1120, _q1221, _q743):
        """Can unit u get the animals of job j (carried spare, or free shed stock)?"""
        _q1036 = _q1120.routes[_q1221]
        _q715 = _q1120.invA[_q1221]
        for k, c in _q743.a.items():
            spare = _q715.get(k, 0) - _q1036.A.get(k, 0)
            if spare >= c:
                continue
            if _q1120.shed_free.get(k, 0) < c - max(0, spare):
                return False
        return True

    def _pinned(_q1120, _q1221, _q743):
        """A PLACE job stays with a unit that carries its animal."""
        if not _q743.a:
            return False
        _q715 = _q1120.invA[_q1221]
        return any((_q715.get(k, 0) > 0 for k in _q743.a))

    def _calc_shed_free(_q1120):
        _q1122 = {}
        for k in ANIMALS:
            _q544 = 0
            for _q1221, _q1036 in enumerate(_q1120.routes):
                _q544 += max(0, _q1036.A.get(k, 0) - _q1120.invA[_q1221].get(k, 0))
            _q1122[k] = _q1120.shed.get(k, 0) - _q544
        _q1120.shed_free = _q1122

    def _best_insert(_q1120, _q1221, _q743, cap=None):
        """Cheapest position for job j in route u -> (new_dur, k) or (None, None) if infeasible."""
        if _q743.a and (not _q1120._animal_ok(_q1221, _q743)):
            return (None, None)
        _q1036 = _q1120.routes[_q1221]
        tl = _q1036.tl
        n = len(tl)
        if cap is None:
            cap = _q1120.cap
        _q1120.evals += n + 1
        dw, df = (_q743.dw, _q743.df)
        if dw >= 0 and df >= 0 and (_q1036.dur + _q743.s > cap):
            if dw or df:
                _q1120.evals += n + 1
            return (None, None)
        if dw or df:
            return _q1120._best_insert_kit(_q1221, _q743, _q1036, _addA(_q1036.A, _q743.a) if _q743.a else _q1036.A, cap)
        t = _q743.t
        _q11 = D[t]
        if _q743.a:
            kt, sp = _q1120._kit(_q1221, _q1036.nW, _q1036.nF, _addA(_q1036.A, _q743.a))
        else:
            kt, sp = (_q1036.kt, _q1036.sp)
        base = kt + _q1036.inner + _q1036.serv + _q743.s
        if n == 0:
            _q893 = base + D[sp][t]
            if _q1120.ret:
                _q893 += ACC_D[t] + 1
            return (_q893, 0) if _q893 <= cap else (None, None)
        _q10 = D[sp]
        t0 = tl[0]
        best = base + _q10[t] + _q11[t0]
        _q417 = 0
        base += _q10[t0]
        prev = t0
        _q9 = D[t0]
        _q558 = _q11[t0]
        for k in range(1, n):
            _q920 = tl[k]
            _q555 = _q11[_q920]
            c = base + _q558 + _q555 - _q9[_q920]
            if c < best:
                best, _q417 = (c, k)
            prev = _q920
            _q9 = D[_q920]
            _q558 = _q555
        c = base + _q558
        if _q1120.ret:
            best += ACC_D[tl[-1]] + 1
            c += ACC_D[t] + 1
        if c < best:
            best, _q417 = (c, n)
        if best <= cap:
            return (best, _q417)
        return (None, None)

    def _best_insert_split(_q1120, _q1221, _q743, cap=None):
        """split_collect (B5; bound over _best_insert in __init__): a collect job may go into its herd job's route, a
        route holding FERTILIZE jobs (the credit), or any route while its herd job is not routed."""
        t = _q743.t
        if type(t) is _Sub:
            _q709 = _q1120.where.get(int(t))
            if _q709 is not None and _q709 != _q1221 and (not _q1120.routes[_q1221].F):
                _q1120.evals += 1
                return (None, None)
        return PDExecutor._best_insert(_q1120, _q1221, _q743, cap)

    def _best_insert_kit(_q1120, _q1221, _q743, _q1036, _q2, cap):
        """_best_insert for a job that changes the kit: exact order-aware start need per position (O(1) each)."""
        tl = _q1036.tl
        n = len(tl)
        t = _q743.t
        dw, df = (_q743.dw, _q743.df)
        _q11 = D[t]
        base = _q1036.inner + _q1036.serv + _q743.s
        cw, pmw, smw, cf, pmf, smf = (_q1036.cw, _q1036.pmw, _q1036.smw, _q1036.cf, _q1036.pmf, _q1036.smf)
        _q732 = _q1120.invW[_q1221]
        _q731 = _q1120.invF[_q1221]
        _q760 = _q1120.dlv_t.get(_q1221, 0) if _q1120.dlv_t else 0
        if _q2:
            _q715 = _q1120.invA[_q1221]
            for _q754, _q449 in _q2.items():
                if _q449 > _q715.get(_q754, 0):
                    _q760 += 1
        _q954 = _q1120.pos[_q1221]
        _q554 = _q1120.delay[_q1221]
        _q723 = _q954 in ACCESS
        _q372 = ACC_D[_q954]
        _q1101 = _q1120.supply_on
        if _q1101:
            _q458 = _q1120.shed.get('WHEAT', 0) - _q1120.outW + _q1036.oW + _q732
            _q457 = _q1120.shed.get('FERTILIZER', 0) - _q1120.outF + _q1036.oF + _q731
        _q7 = D[ACC_NEAR[_q954]]
        _q8 = D[_q954]
        best, _q417 = (None, None)
        t0 = tl[0] if n else -1
        _q1063 = _q1120.ret
        for k in range(n + 1):
            _q445 = cw[k - 1] if k else 0
            _q412 = cf[k - 1] if k else 0
            _q919 = pmw[k]
            x = _q445 + dw
            if x > _q919:
                _q919 = x
            x = smw[k] + dw
            if x > _q919:
                _q919 = x
            _q907 = pmf[k]
            x = _q412 + df
            if x > _q907:
                _q907 = x
            x = smf[k] + df
            if x > _q907:
                _q907 = x
            if _q1101 and (_q919 > _q732 and _q919 > _q458 and (_q919 > _q1036.nW) or (_q907 > _q731 and _q907 > _q457 and (_q907 > _q1036.nF))):
                continue
            kt = _q760 + _q554
            if _q919 > _q732:
                kt += 1
            if _q907 > _q731:
                kt += 1
            if kt > _q554 and (not _q723):
                kt += _q372
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
            if _q1063:
                c += (ACC_D[t] if k == n else ACC_D[tl[-1]]) + 1
            if best is None or c < best:
                best, _q417 = (c, k)
        _q1120.evals += n + 1
        if best is not None and best <= cap:
            return (best, _q417)
        return (None, None)

    def _best_insert_kit_fb(_q1120, _q1221, _q743, _q1036, _q2, cap):
        """_best_insert_kit with the f_shed_w objective (B5; bound over _best_insert_kit in __init__ when f_shed_w > 0):
        positions are ranked by duration + fb x the FERTILIZER the unit must draw from the shed; only positions whose
        duration fits cap are candidates.  Returns (biased new cost, k), where biased new cost - r.dur is the biased
        insertion delta (the route's cost is r.dur + fb * r.oF)."""
        fb = _q1120.fb
        tl = _q1036.tl
        n = len(tl)
        t = _q743.t
        dw, df = (_q743.dw, _q743.df)
        _q11 = D[t]
        base = _q1036.inner + _q1036.serv + _q743.s
        cw, pmw, smw, cf, pmf, smf = (_q1036.cw, _q1036.pmw, _q1036.smw, _q1036.cf, _q1036.pmf, _q1036.smf)
        _q732 = _q1120.invW[_q1221]
        _q731 = _q1120.invF[_q1221]
        _q760 = _q1120.dlv_t.get(_q1221, 0) if _q1120.dlv_t else 0
        if _q2:
            _q715 = _q1120.invA[_q1221]
            for _q754, _q449 in _q2.items():
                if _q449 > _q715.get(_q754, 0):
                    _q760 += 1
        _q954 = _q1120.pos[_q1221]
        _q554 = _q1120.delay[_q1221]
        _q723 = _q954 in ACCESS
        _q372 = ACC_D[_q954]
        _q1101 = _q1120.supply_on
        if _q1101:
            _q458 = _q1120.shed.get('WHEAT', 0) - _q1120.outW + _q1036.oW + _q732
            _q457 = _q1120.shed.get('FERTILIZER', 0) - _q1120.outF + _q1036.oF + _q731
        _q7 = D[ACC_NEAR[_q954]]
        _q8 = D[_q954]
        _q926 = _q1036.oF
        best, _q417 = (None, None)
        t0 = tl[0] if n else -1
        _q1063 = _q1120.ret
        for k in range(n + 1):
            _q445 = cw[k - 1] if k else 0
            _q412 = cf[k - 1] if k else 0
            _q919 = pmw[k]
            x = _q445 + dw
            if x > _q919:
                _q919 = x
            x = smw[k] + dw
            if x > _q919:
                _q919 = x
            _q907 = pmf[k]
            x = _q412 + df
            if x > _q907:
                _q907 = x
            x = smf[k] + df
            if x > _q907:
                _q907 = x
            if _q1101 and (_q919 > _q732 and _q919 > _q458 and (_q919 > _q1036.nW) or (_q907 > _q731 and _q907 > _q457 and (_q907 > _q1036.nF))):
                continue
            kt = _q760 + _q554
            if _q919 > _q732:
                kt += 1
            if _q907 > _q731:
                kt += 1
            if kt > _q554 and (not _q723):
                kt += _q372
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
            if _q1063:
                c += (ACC_D[t] if k == n else ACC_D[tl[-1]]) + 1
            if c > cap:
                continue
            _q471 = c + fb * ((_q907 - _q731 if _q907 > _q731 else 0) - _q926)
            if best is None or _q471 < best:
                best, _q417 = (_q471, k)
        _q1120.evals += n + 1
        if best is not None:
            return (best, _q417)
        return (None, None)

    def _remove_dur(_q1120, _q1221, _q712, _q414=True):
        _q1036 = _q1120.routes[_q1221]
        tl = _q1036.tl
        n = len(tl)
        if n == 1:
            return -_q1120.fb * _q1036.oF if _q1120.fb and _q414 else 0
        t = tl[_q712]
        _q743 = _q1120.jobs[t]
        inner = _q1036.inner
        if _q712 == 0:
            inner -= D[t][tl[1]]
            _q629 = tl[1]
        else:
            _q1023 = tl[_q712 - 1]
            if _q712 == n - 1:
                inner -= D[_q1023][t]
            else:
                _q920 = tl[_q712 + 1]
                inner += D[_q1023][_q920] - D[_q1023][t] - D[t][_q920]
            _q629 = tl[0]
        _q2 = _addA(_q1036.A, _q743.a, -1) if _q743.a else _q1036.A
        if _q743.dw or _q743.df:
            _q919 = _q1036.pmw[_q712]
            x = _q1036.smw[_q712 + 1] - _q743.dw
            if x > _q919:
                _q919 = x
            _q907 = _q1036.pmf[_q712]
            x = _q1036.smf[_q712 + 1] - _q743.df
            if x > _q907:
                _q907 = x
        else:
            _q919, _q907 = (_q1036.nW, _q1036.nF)
        kt, sp = _q1120._kit(_q1221, _q919, _q907, _q2)
        _q1078 = (ACC_D[tl[-2]] if _q712 == n - 1 else ACC_D[tl[-1]]) + 1 if _q1120.ret else 0
        if _q1120.fb and _q414 and (_q907 != _q1036.nF):
            _q931 = _q907 - _q1120.invF[_q1221]
            return kt + D[sp][_q629] + inner + _q1036.serv - _q743.s + _q1078 + _q1120.fb * ((_q931 if _q931 > 0 else 0) - _q1036.oF)
        return kt + D[sp][_q629] + inner + _q1036.serv - _q743.s + _q1078

    def _insert(_q1120, _q1221, t, k):
        _q1036 = _q1120.routes[_q1221]
        _q1036.tl.insert(k, t)
        _q1120._eval(_q1221, _q1036)
        _q1120.where[t] = _q1221
        _q1120.pool.discard(t)

    def _remove(_q1120, _q1221, t):
        _q1036 = _q1120.routes[_q1221]
        _q1036.tl.remove(t)
        _q1120._eval(_q1221, _q1036)
        _q1120.where.pop(t, None)

    def _timeout(_q1120):
        if _q1120.evals >= _q1120.budget_end:
            return True
        if time.perf_counter() >= _q1120.t_end:
            _q1120.tcap_hit = True
            return True
        return False

    def _cheapest(_q1120, t):
        _q743 = _q1120.jobs[t]
        _q1009 = _q1120.cfg['prune_r']
        if _q1009:
            _q454 = set()
            where = _q1120.where
            for _q1178 in RING[_q1009][t]:
                _q1222 = where.get(_q1178)
                if _q1222 is not None:
                    _q454.add(_q1222)
            for _q1221 in range(_q1120.n_plan):
                _q1036 = _q1120.routes[_q1221]
                if not _q1036.tl or D[_q1036.sp][t] <= _q1009:
                    _q454.add(_q1221)
            if len(_q454) < _q1120.n_plan:
                best, _q434, _q417 = (None, None, None)
                for _q1221 in _q454:
                    _q893, k = _q1120._best_insert(_q1221, _q743)
                    if _q893 is None:
                        continue
                    c = _q893 - _q1120.routes[_q1221].dur
                    if best is None or c < best or (c == best and _q1221 < _q434):
                        best, _q434, _q417 = (c, _q1221, k)
                if _q434 is not None:
                    return (_q434, _q417)
        best, _q434, _q417 = (None, None, None)
        U = _q1120.n_plan
        routes = _q1120.routes
        if _q1120.cfg['bb_prune'] and U > 2 and (_q743.dw >= 0) and (_q743.df >= 0):
            _q1218, _q1219 = XY[t]
            _q938 = []
            for _q1221 in range(U):
                _q1266, _q1267, _q1273, _q1274 = routes[_q1221].bb
                _q554 = (_q1266 - _q1218 if _q1218 < _q1266 else _q1218 - _q1267 if _q1218 > _q1267 else 0) + (_q1273 - _q1219 if _q1219 < _q1273 else _q1219 - _q1274 if _q1219 > _q1274 else 0)
                _q938.append((_q554, _q1221))
            _q938.sort()
            _q749 = _q743.s
            _q768 = 2 if _q743.dw or _q743.df else 1
            for _q554, _q1221 in _q938:
                if best is not None:
                    _q793 = _q749 + _q554
                    if _q793 > best or (_q793 == best and _q1221 > _q434):
                        if not _q743.a or _q1120._animal_ok(_q1221, _q743):
                            _q1120.evals += _q768 * (len(routes[_q1221].tl) + 1)
                        continue
                _q893, k = _q1120._best_insert(_q1221, _q743)
                if _q893 is None:
                    continue
                c = _q893 - routes[_q1221].dur
                if best is None or c < best or (c == best and _q1221 < _q434):
                    best, _q434, _q417 = (c, _q1221, k)
            return (_q434, _q417)
        for _q1221 in range(U):
            _q893, k = _q1120._best_insert(_q1221, _q743)
            if _q893 is None:
                continue
            c = _q893 - routes[_q1221].dur
            if best is None or c < best:
                best, _q434, _q417 = (c, _q1221, k)
        return (_q434, _q417)

    def _construct(_q1120, _q748):
        """Root-first cheapest insertion (critical first, then farthest first) into the present units' routes."""
        _q938 = sorted(_q748, key=lambda t: (not _q1120.jobs[t].crit, -CENTER_D[t], t))
        _q799 = []
        for t in _q938:
            _q434, _q417 = _q1120._cheapest(t)
            if _q434 is None:
                _q799.append(t)
            else:
                _q1120._insert(_q434, t, _q417)
        return _q799

    def _plan_total(_q1120):
        _q1005 = sum((_q1120.jobs[t].val for t in _q1120.pool))
        return 1000.0 * _q1005 + sum((_q1120._cost(_q1221, _q1036) for _q1221, _q1036 in enumerate(_q1120.routes)))

    def _must_water(_q1120, t):
        """audit2: is job t a must-WATER (a WATER on a PLANT tile with consecutive_unwatered >= 1, not watered today:
        the plant weeds tonight without it)?"""
        _q481 = _q1120.chains.get(t)
        if not _q481 or type(t) is _Sub or _q1120.tiles is None:
            return False
        if not any((op == 'WATER' for op, _ in _q481)):
            return False
        _q1196 = int(t)
        tile = _q1120.tiles[_q1196 // B][_q1196 % B]
        return isinstance(tile, dict) and tile.get('kind') == 'PLANT' and (not tile.get('watered_today')) and (int(tile.get('consecutive_unwatered', 0) or 0) >= 1)

    def _strip_fert(_q1120, t):
        _q481 = _q1120.chains.get(t)
        if not _q481 or not any((op == 'FERTILIZE' for op, _ in _q481)) or (not _q1120._must_water(t)):
            return False
        _q481[:] = [_q922 for _q922 in _q481 if _q922[0] != 'FERTILIZE']
        if not _q481 or _q1120._refresh_job(t, _q1120.tiles) is None:
            return False
        _q1120.stats['water_split'] = _q1120.stats.get('water_split', 0) + 1
        return True

    def _fix_overflow(_q1120):
        """Routes longer than the turns left drop their lowest value-per-turn jobs into the pool."""
        _q675 = _q1120.cfg.get('water_guard')
        _q1152 = _q1120.cfg.get('water_split')
        for _q1221, _q1036 in enumerate(_q1120.routes):
            while _q1036.tl and _q1036.dur > _q1120.cap:
                best, _q413 = (None, None)
                _q410, _q415 = (None, None)
                for _q712, t in enumerate(_q1036.tl):
                    if _q712 == 0 and _q1221 < _q1120.n_units and (_q1120.pos[_q1221] == t % NT):
                        continue
                    _q743 = _q1120.jobs[t]
                    _q1107 = _q1036.dur - _q1120._remove_dur(_q1221, _q712, False)
                    _q1111 = _q743.val / max(1.0, _q1107)
                    if _q675 and _q1120._must_water(t):
                        if _q410 is None or _q1111 < _q410:
                            _q410, _q415 = (_q1111, _q712)
                        continue
                    if best is None or _q1111 < best:
                        best, _q413 = (_q1111, _q712)
                if _q413 is None:
                    _q413 = _q415
                if _q413 is None:
                    break
                t = _q1036.tl[_q413]
                if _q1152 and _q1120._strip_fert(t):
                    _q1120._eval(_q1221, _q1036)
                    continue
                _q1120._remove(_q1221, t)
                _q1120.pool.add(t)
                _q1120.stats['overflow_drops'] += 1

    def _insert_pool(_q1120):
        if not _q1120.pool:
            return
        for t in sorted(_q1120.pool, key=lambda t: (-_q1120.jobs[t].val, t)):
            if time.perf_counter() >= _q1120.t_end:
                _q1120.tcap_hit = True
                break
            _q434, _q417 = _q1120._cheapest(t)
            if _q434 is not None:
                _q1120._insert(_q434, t, _q417)
                _q1120._calc_shed_free()
            elif _q1120.jobs[t].crit:
                _q1120._eject_for(t)
                if t in _q1120.pool and _q1120.cfg.get('water_split') and _q1120._strip_fert(t):
                    _q434, _q417 = _q1120._cheapest(t)
                    if _q434 is not None:
                        _q1120._insert(_q434, t, _q417)
                        _q1120._calc_shed_free()
                    elif _q1120.jobs[t].crit:
                        _q1120._eject_for(t)
                if t in _q1120.pool and int(_q1120.cfg.get('eject_multi') or 0) > 1 and _q1120.jobs[t].crit and _q1120._must_water(t):
                    _q1120._eject_multi(t)

    def _evictable(_q1120, t, _q1178, _q743, _q745):
        if not _q745.crit or _q1120._must_water(_q1178) or (not _q1120._must_water(t)):
            return False
        return any((op in ('PLANT', 'PLACE') for op, _ in _q745.chain))

    def _eject_for(_q1120, t):
        """Put critical job t in by removing one cheaper, non-critical job of a route (min value removed)."""
        _q743 = _q1120.jobs[t]
        best = None
        _q593 = _q1120.cfg.get('water_guard') == 'evict'
        for _q1221, _q1036 in enumerate(_q1120.routes):
            for _q712, _q1178 in enumerate(_q1036.tl):
                _q745 = _q1120.jobs[_q1178]
                if (_q745.val >= _q743.val or _q745.crit) and (not (_q593 and _q1120._evictable(t, _q1178, _q743, _q745))):
                    continue
                if _q712 == 0 and _q1221 < _q1120.n_units and (_q1120.pos[_q1221] == _q1178 % NT) or _q1120._pinned(_q1221, _q745):
                    continue
                _q1107 = _q1036.dur - _q1120._remove_dur(_q1221, _q712, False)
                _q893, k = _q1120._best_insert(_q1221, _q743, cap=_q1120.cap + _q1107)
                if _q893 is None:
                    continue
                if best is None or _q745.val < best[0]:
                    best = (_q745.val, _q1221, _q1178)
        if best is None:
            return
        _, _q1221, _q1178 = best
        _q1036 = _q1120.routes[_q1221]
        _q933 = list(_q1036.tl)
        _q1120._remove(_q1221, _q1178)
        _q893, k = _q1120._best_insert(_q1221, _q743)
        if _q893 is not None:
            _q1120._insert(_q1221, t, k)
            _q1120.pool.add(_q1178)
            _q1120.stats['ejects'] += 1
        else:
            _q1036.tl = _q933
            _q1120._eval(_q1221, _q1036)
            _q1120.where[_q1178] = _q1221

    def _eject_multi(_q1120, t):
        _q743 = _q1120.jobs[t]
        _q772 = int(_q1120.cfg.get('eject_multi') or 0)
        best = None
        for _q1221, _q1036 in enumerate(_q1120.routes[:_q1120.n_plan]):
            _q454 = []
            for _q712, _q1178 in enumerate(_q1036.tl):
                _q745 = _q1120.jobs[_q1178]
                if _q745.crit or (_q712 == 0 and _q1221 < _q1120.n_units and (_q1120.pos[_q1221] == _q1178 % NT)) or _q1120._pinned(_q1221, _q745):
                    continue
                _q454.append((_q745.val, _q1178))
            if len(_q454) < 2:
                continue
            _q454.sort()
            _q1146 = _snap(_q1036)
            oW, oF = (_q1036.oW, _q1036.oF)
            _q1050 = []
            _q1206 = 0.0
            fit = False
            for v2, _q1178 in _q454[:_q772]:
                if _q1206 + v2 >= _q743.val:
                    break
                _q1036.tl.remove(_q1178)
                _q1050.append(_q1178)
                _q1206 += v2
                _q1120._eval(_q1221, _q1036)
                if len(_q1050) >= 2:
                    _q893, k = _q1120._best_insert(_q1221, _q743)
                    if _q893 is not None:
                        fit = True
                        break
            _q1120.outW += oW - _q1036.oW
            _q1120.outF += oF - _q1036.oF
            _restore(_q1036, _q1146)
            if fit and (best is None or _q1206 < best[0]):
                best = (_q1206, _q1221, list(_q1050))
        if best is None:
            return False
        _, _q1221, _q1050 = best
        _q1036 = _q1120.routes[_q1221]
        _q1146 = _snap(_q1036)
        oW, oF = (_q1036.oW, _q1036.oF)
        for _q1178 in _q1050:
            _q1120._remove(_q1221, _q1178)
        _q893, k = _q1120._best_insert(_q1221, _q743)
        if _q893 is None:
            _q1120.outW += oW - _q1036.oW
            _q1120.outF += oF - _q1036.oF
            _restore(_q1036, _q1146)
            for _q1178 in _q1050:
                _q1120.where[_q1178] = _q1221
            return False
        _q1120._insert(_q1221, t, k)
        for _q1178 in _q1050:
            _q1120.pool.add(_q1178)
        _q1120._calc_shed_free()
        _q1120.stats['eject_multi'] = _q1120.stats.get('eject_multi', 0) + 1
        return True

    def _ls(_q1120):
        """First-improvement local search: relocate, intra or-opt / 2-opt, tail exchange."""
        U = _q1120.n_plan
        if U == 0:
            return
        _q720 = True
        while _q720 and (not _q1120._timeout()):
            _q720 = False
            if _q1120._relocate_pass():
                _q720 = True
            if _q1120._timeout():
                return
            if _q1120._intra_pass():
                _q720 = True
            if _q1120._timeout():
                return
            if _q1120.cfg['tail_x'] and _q1120._tail_pass():
                _q720 = True

    def _relocate_pass(_q1120):
        routes = _q1120.routes
        U = _q1120.n_plan
        _q791 = bool(_q1120.cfg['late_w'])
        _q391 = False
        for a in range(U):
            _q1041 = routes[a]
            _q712 = 0
            while _q712 < len(_q1041.tl):
                if _q1120._timeout():
                    return _q391
                t = _q1041.tl[_q712]
                _q743 = _q1120.jobs[t]
                if _q712 == 0 and a < _q1120.n_units and (_q1120.pos[a] == t % NT) or _q1120._pinned(a, _q743):
                    _q712 += 1
                    continue
                _q664 = _q1041.dur - _q1120._remove_dur(a, _q712)
                best, bb, _q417 = (-1e-09, None, None)
                for b in range(U):
                    if b == a:
                        continue
                    _q1047 = routes[b]
                    if _q1047.dur + _q743.s > _q1120.cap:
                        continue
                    _q893, k = _q1120._best_insert(b, _q743)
                    if _q893 is None:
                        continue
                    _q543 = _q893 - _q1047.dur - _q664
                    if _q543 < best:
                        best, bb, _q417 = (_q543, b, k)
                if bb is not None:
                    fb = _q1120.fb
                    if _q791 and (_q743.urg or _q1041.dur + fb * _q1041.oF != _q1120._cost(a, _q1041) or routes[bb].dur + fb * routes[bb].oF != _q1120._cost(bb, routes[bb])):
                        _q408 = _q1120._cost(a, _q1041) + _q1120._cost(bb, routes[bb])
                        _q1120._remove(a, t)
                        _q1120._insert(bb, t, _q417)
                        after = _q1120._cost(a, _q1041) + _q1120._cost(bb, routes[bb])
                        if after > _q408 - 1e-09:
                            _q1120._remove(bb, t)
                            _q1120._insert(a, t, _q712)
                            _q712 += 1
                            continue
                    else:
                        _q1120._remove(a, t)
                        _q1120._insert(bb, t, _q417)
                    if _q743.a:
                        _q1120._calc_shed_free()
                    _q1120.stats['ls_moves'] += 1
                    _q391 = True
                    continue
                _q712 += 1
        return _q391

    def _intra_pass(_q1120):
        """Or-opt (one job) and 2-opt on each route's open path from its start tile (same job set -> same kit)."""
        _q391 = False
        for a in range(_q1120.n_plan):
            if _q1120._timeout():
                return _q391
            _q1041 = _q1120.routes[a]
            n = len(_q1041.tl)
            if n < 2:
                continue
            _q631 = a < _q1120.n_units and _q1120.pos[a] == _q1041.tl[0] % NT
            _q791 = _q1120.cfg['late_w'] and any((_q1120.jobs[t].urg for t in _q1041.tl))
            _q524 = _q1120._cost(a, _q1041)
            _q720 = True
            while _q720 and (not _q1120._timeout()):
                _q720 = False
                _q32 = [_q1041.sp] + _q1041.tl
                m = len(_q32)
                lo = 2 if _q631 else 1
                for _q712 in range(lo, m - 1):
                    _q361 = _q32[_q712 - 1]
                    _q47 = _q32[_q712]
                    _q6 = D[_q361]
                    for k in range(_q712 + 1, m):
                        _q48 = _q32[k]
                        if k + 1 < m:
                            _q920 = _q32[k + 1]
                            _q543 = _q6[_q48] + D[_q47][_q920] - _q6[_q47] - D[_q48][_q920]
                        else:
                            _q543 = _q6[_q48] - _q6[_q47]
                        if _q543 < -1e-09:
                            new = _q32[1:_q712] + _q32[_q712:k + 1][::-1] + _q32[k + 1:]
                            if _q1120._accept_intra(a, _q1041, new, _q524, _q791):
                                _q524 = _q1120._cost(a, _q1041)
                                _q720 = True
                                _q391 = True
                                break
                    if _q720:
                        break
                    _q1120.evals += m - _q712
                if _q720:
                    continue
                for _q712 in range(lo, m):
                    x = _q32[_q712]
                    _q1023 = _q32[_q712 - 1]
                    if _q712 + 1 < m:
                        _q920 = _q32[_q712 + 1]
                        rem = D[_q1023][_q920] - D[_q1023][x] - D[x][_q920]
                    else:
                        rem = -D[_q1023][x]
                    _q49 = _q32[:_q712] + _q32[_q712 + 1:]
                    _q12 = D[x]
                    for k in range(lo - 1, len(_q49)):
                        if k == _q712 - 1:
                            continue
                        q0 = _q49[k]
                        if k + 1 < len(_q49):
                            _q1028 = _q49[k + 1]
                            _q728 = _q12[q0] + _q12[_q1028] - D[q0][_q1028]
                        else:
                            _q728 = _q12[q0]
                        if rem + _q728 < -1e-09:
                            new = _q49[1:k + 1] + [x] + _q49[k + 1:]
                            if _q1120._accept_intra(a, _q1041, new, _q524, _q791):
                                _q524 = _q1120._cost(a, _q1041)
                                _q720 = True
                                _q391 = True
                                break
                    _q1120.evals += len(_q49)
                    if _q720:
                        break
        return _q391

    def _accept_intra(_q1120, a, _q1041, new, _q524, _q791):
        _q933 = _q1041.tl
        _q935 = _q1041.dur
        _q1041.tl = new
        _q1120._eval(a, _q1041)
        c = _q1120._cost(a, _q1041)
        if c < _q524 - 1e-09 and (_q1041.dur <= _q1120.cap or _q1041.dur <= _q935):
            _q1120.stats['ls_moves'] += 1
            return True
        _q1041.tl = _q933
        _q1120._eval(a, _q1041)
        return False

    def _prefix(_q1120, _q1221, _q1036):
        tl = _q1036.tl
        jobs = _q1120.jobs
        _q44 = [0]
        _q34 = [0]
        _q41 = [0]
        _q37 = [0, 0]
        for _q717, t in enumerate(tl):
            _q743 = jobs[t]
            _q44.append(_q44[-1] + _q743.w)
            _q34.append(_q34[-1] + _q743.f)
            _q41.append(_q41[-1] + _q743.s)
            if _q717 >= 1:
                _q37.append(_q37[-1] + D[tl[_q717 - 1]][t])
        return (_q44, _q34, _q41, _q37)

    def _tail_pass(_q1120):
        U = _q1120.n_plan
        _q391 = False
        pre = [_q1120._prefix(_q1221, _q1120.routes[_q1221]) for _q1221 in range(U)]
        for a in range(U):
            for b in range(a + 1, U):
                if _q1120._timeout():
                    return _q391
                if _q1120._tail_x(a, b, pre[a], pre[b]):
                    pre[a] = _q1120._prefix(a, _q1120.routes[a])
                    pre[b] = _q1120._prefix(b, _q1120.routes[b])
                    _q391 = True
        return _q391

    def _tail_x(_q1120, a, b, _q964, pb):
        _q1041, _q1047 = (_q1120.routes[a], _q1120.routes[b])
        _q1, _q4 = (_q1041.tl, _q1047.tl)
        _q889, _q892 = (len(_q1), len(_q4))
        if _q889 == 0 and _q892 == 0 or _q1041.A or _q1047.A:
            return False
        _q791 = _q1120.cfg['late_w'] and (any((_q1120.jobs[t].urg for t in _q1)) or any((_q1120.jobs[t].urg for t in _q4)))
        _q522 = _q1041.dur + _q1047.dur
        fb = _q1120.fb
        _q523 = _q522 + fb * (_q1041.oF + _q1047.oF) if fb else _q522
        cap = _q1120.cap
        _q45, _q35, _q42, _q38 = _q964
        _q46, _q36, _q43, _q39 = pb
        _q24, Ib = (_q38[_q889] if _q889 else 0, _q39[_q892] if _q892 else 0)
        _q62, _q19, _q57 = (_q45[_q889], _q35[_q889], _q42[_q889])
        _q63, _q20, _q58 = (_q46[_q892], _q36[_q892], _q43[_q892])
        _q719 = 1 if _q889 and a < _q1120.n_units and (_q1120.pos[a] == _q1[0] % NT) else 0
        _q770 = 1 if _q892 and b < _q1120.n_units and (_q1120.pos[b] == _q4[0] % NT) else 0
        _q1120.evals += (_q889 + 1) * (_q892 + 1)
        _q528, _q1000, _q1144, _q478, _q998, _q1141 = (_q1041.cw, _q1041.pmw, _q1041.smw, _q1041.cf, _q1041.pmf, _q1041.smf)
        _q529, _q1001, _q1145, _q479, _q999, _q1142 = (_q1047.cw, _q1047.pmw, _q1047.smw, _q1047.cf, _q1047.pmf, _q1047.smf)
        _q1063 = _q1120.ret
        for _q712 in range(_q719, _q889 + 1):
            _q470 = _q528[_q712 - 1] if _q712 else 0
            _q451 = _q478[_q712 - 1] if _q712 else 0
            _q1102 = _q38[_q712] if _q712 >= 1 else 0
            _q1103 = _q24 - _q38[_q712 + 1] if _q712 < _q889 else 0
            for k in range(_q770, _q892 + 1):
                if _q712 == _q889 and k == _q892 or (_q712 == 0 and k == 0):
                    continue
                _q1109 = _q39[k] if k >= 1 else 0
                _q1110 = Ib - _q39[k + 1] if k < _q892 else 0
                _q473 = _q529[k - 1] if k else 0
                _q472 = _q479[k - 1] if k else 0
                _q60 = _q1000[_q712]
                x = _q470 - _q473 + _q1145[k]
                if x > _q60:
                    _q60 = x
                _q13 = _q998[_q712]
                x = _q451 - _q472 + _q1142[k]
                if x > _q13:
                    _q13 = x
                _q54 = _q42[_q712] + _q58 - _q43[k]
                _q22 = _q1102 + _q1110 + (D[_q1[_q712 - 1]][_q4[k]] if _q712 >= 1 and k < _q892 else 0)
                _q599 = _q1[0] if _q712 >= 1 else _q4[k] if k < _q892 else -1
                if _q599 >= 0:
                    kt, sp = _q1120._kit(a, _q60, _q13, None)
                    _q532 = kt + D[sp][_q599] + _q22 + _q54
                    if _q1063:
                        _q532 += ACC_D[_q4[-1] if k < _q892 else _q1[_q712 - 1]] + 1
                else:
                    _q532 = 0
                if _q532 > cap:
                    continue
                _q61 = _q1001[k]
                x = _q473 - _q470 + _q1144[_q712]
                if x > _q61:
                    _q61 = x
                _q14 = _q999[k]
                x = _q472 - _q451 + _q1141[_q712]
                if x > _q14:
                    _q14 = x
                _q55 = _q43[k] + _q57 - _q42[_q712]
                _q23 = _q1109 + _q1103 + (D[_q4[k - 1]][_q1[_q712]] if k >= 1 and _q712 < _q889 else 0)
                _q600 = _q4[0] if k >= 1 else _q1[_q712] if _q712 < _q889 else -1
                if _q600 >= 0:
                    kt, sp = _q1120._kit(b, _q61, _q14, None)
                    _q533 = kt + D[sp][_q600] + _q23 + _q55
                    if _q1063:
                        _q533 += ACC_D[_q1[-1] if _q712 < _q889 else _q4[k - 1]] + 1
                else:
                    _q533 = 0
                if _q533 > cap:
                    continue
                if fb:
                    _q924 = _q13 - _q1120.invF[a]
                    _q925 = _q14 - _q1120.invF[b]
                    if _q532 + _q533 + fb * ((_q924 if _q924 > 0 else 0) + (_q925 if _q925 > 0 else 0)) >= _q523 - 1e-09:
                        continue
                elif _q532 + _q533 >= _q522 - 1e-09:
                    continue
                if _q1120.supply_on and (not _q1120._supply_ok2(a, b, _q60, _q13, _q61, _q14)):
                    continue
                _q901 = _q1[:_q712] + _q4[k:]
                _q902 = _q4[:k] + _q1[_q712:]
                if _q791:
                    _q408 = _q1120._cost(a, _q1041) + _q1120._cost(b, _q1047)
                _q1041.tl, _q1047.tl = (_q901, _q902)
                _q1120._eval(a, _q1041)
                _q1120._eval(b, _q1047)
                if _q791 and _q1120._cost(a, _q1041) + _q1120._cost(b, _q1047) >= _q408 - 1e-09:
                    _q1041.tl, _q1047.tl = (_q1, _q4)
                    _q1120._eval(a, _q1041)
                    _q1120._eval(b, _q1047)
                    continue
                for t in _q901:
                    _q1120.where[t] = a
                for t in _q902:
                    _q1120.where[t] = b
                _q1120.stats['ls_moves'] += 1
                return True
        return False

    def _supply_ok2(_q1120, a, b, _q60, _q13, _q61, _q14):
        """Tail exchange: can the shed cover the two routes' new start needs (after the other units' pickups)?"""
        _q1041, _q1047 = (_q1120.routes[a], _q1120.routes[b])
        _q948 = max(0, _q60 - _q1120.invW[a]) + max(0, _q61 - _q1120.invW[b]) - _q1041.oW - _q1047.oW
        _q931 = max(0, _q13 - _q1120.invF[a]) + max(0, _q14 - _q1120.invF[b]) - _q1041.oF - _q1047.oF
        return (_q948 <= 0 or _q1120.shed.get('WHEAT', 0) - _q1120.outW >= _q948) and (_q931 <= 0 or _q1120.shed.get('FERTILIZER', 0) - _q1120.outF >= _q931)

    def _movable(_q1120, _q1221, _q712, t):
        return not (_q712 == 0 and _q1221 < _q1120.n_units and (_q1120.pos[_q1221] == t % NT) or _q1120._pinned(_q1221, _q1120.jobs[t]))

    def _rr(_q1120):
        """Ruin & recreate (SISR-lite): remove strings of consecutive jobs from up to rr_routes routes near a random
        seed job, re-insert them and the pool (critical first; random / far / value order), keep if not worse.
        Incremental objective (only touched routes are re-costed), lazy snapshots of touched routes."""
        cfg = _q1120.cfg
        rng = random.Random(_q1120.day * 7919 + _q1120.hour * 131 + 17)
        _q1080 = rng.random
        jobs = _q1120.jobs
        routes = _q1120.routes
        _q390 = False
        _q809 = cfg['rr_lmax']
        _q881 = cfg['rr_routes']
        ps = cfg['rr_pool_seed']
        _q1160 = cfg['rr_stall'] if not (cfg['stall_loose_only'] and _q1120.is_tight) else 0
        if _q1160:
            _q1160 += cfg['rr_stall_per_job'] * len(_q1120.where)
        _q1159 = 0
        while not _q1120._timeout():
            if not _q1120.where:
                return _q390
            if _q1160 and _q1159 >= _q1160:
                _q1120.stats['rr_stall_stop'] = _q1120.stats.get('rr_stall_stop', 0) + 1
                return _q390
            _q1159 += 1
            _q1120.stats['rr_iter'] += 1
            _q395 = list(_q1120.where)
            _q1120.evals += len(_q395) // 2 + 40
            seed = _q395[int(_q1080() * len(_q395))]
            if ps and _q1120.pool and (_q1080() < ps):
                _q988 = sorted(_q1120.pool)
                _q955 = _q988[int(_q1080() * len(_q988))]
                for _q1178 in (NEARS if _q1120.split_on else NEAR)[_q955]:
                    if _q1178 in _q1120.where:
                        seed = _q1178
                        break
            _q879 = 1 + int(_q1080() * _q881)
            _q1147 = {}
            _q1050 = []
            where = _q1120.where
            for t in (NEARS if _q1120.split_on else NEAR)[seed]:
                if len(_q1147) >= _q879:
                    break
                _q1221 = where.get(t)
                if _q1221 is None or _q1221 in _q1147:
                    continue
                _q1036 = routes[_q1221]
                tl = _q1036.tl
                _q712 = tl.index(t)
                _q25 = 1 + int(_q1080() * min(len(tl), _q809))
                lo = max(0, min(_q712 - int(_q1080() * _q25), len(tl) - _q25))
                _q1119 = [x for k, x in enumerate(tl[lo:lo + _q25]) if _q1120._movable(_q1221, lo + k, x)]
                if not _q1119:
                    continue
                _q1147[_q1221] = (_snap(_q1036), _q1120._cost(_q1221, _q1036))
                for x in _q1119:
                    tl.remove(x)
                    where.pop(x, None)
                    _q1050.append(x)
                _q1120._eval(_q1221, _q1036)
            _q1120.evals += 4 * len(_q1050) + 4
            if not _q1050:
                continue
            _q1004 = set(_q1120.pool)
            _q1006 = sum((jobs[t].val for t in _q1004))
            if any((jobs[t].a for t in _q1050)):
                _q1120._calc_shed_free()
            _q1204 = _q1050 + sorted(_q1004)
            _q1120.pool = set()
            mode = int(_q1080() * 3)
            if mode == 0:
                rng.shuffle(_q1204)
                _q1204.sort(key=lambda t: not jobs[t].crit)
            elif mode == 1:
                _q1204.sort(key=lambda t: (not jobs[t].crit, -CENTER_D[t], t))
            else:
                _q1204.sort(key=lambda t: (not jobs[t].crit, -jobs[t].val / max(1, jobs[t].s), CENTER_D[t], t))
            for t in _q1204:
                _q434, _q417 = _q1120._cheapest(t)
                if _q434 is None:
                    _q1120.pool.add(t)
                else:
                    if _q434 not in _q1147:
                        _q1147[_q434] = (_snap(routes[_q434]), _q1120._cost(_q434, routes[_q434]))
                    _q1120._insert(_q434, t, _q417)
                    if jobs[t].a:
                        _q1120._calc_shed_free()
            _q408 = 1000.0 * _q1006 + sum((c for _, c in _q1147.values()))
            after = 1000.0 * sum((jobs[t].val for t in _q1120.pool)) + sum((_q1120._cost(_q1221, routes[_q1221]) for _q1221 in _q1147))
            _q1120.evals += len(_q1147) * 3
            if after <= _q408 + 1e-09:
                if after < _q408 - 1e-09:
                    _q1120.stats['rr_acc'] += 1
                    _q390 = True
                    _q1159 = 0
                continue
            for _q1221 in _q1147:
                for t in routes[_q1221].tl:
                    where.pop(t, None)
            for t in _q1050:
                where.pop(t, None)
            for _q1221, (_q1146, _) in _q1147.items():
                _q1036 = routes[_q1221]
                _q1120.outW -= _q1036.oW
                _q1120.outF -= _q1036.oF
                _restore(_q1036, _q1146)
                _q1120.outW += _q1036.oW
                _q1120.outF += _q1036.oF
                for t in _q1036.tl:
                    where[t] = _q1221
            _q1120.pool = _q1004
            if any((jobs[t].a for t in _q1050)):
                _q1120._calc_shed_free()
        return _q390

    def _sync_units(_q1120, _q1235):
        units = _q1235['units']
        _q735 = _q1235['inv']
        n = len(units)
        _q1120.pos = [_q954[1] * B + _q954[0] for _q954 in units]
        _q1120.invW = []
        _q1120.invF = []
        _q1120.invA = []
        for _q1221 in range(n):
            _q741 = _q735[_q1221] if _q1221 < len(_q735) else {}
            _q1120.invW.append(_q741.get('WHEAT', 0))
            _q1120.invF.append(_q741.get('FERTILIZER', 0))
            _q1120.invA.append({k: _q741[k] for k in ANIMALS if _q741.get(k, 0) > 0})
        _q1120.shed = _q1235.get('shed', {})
        _q1120.delay = [0] * n
        _q1120.cur_inv = _q735
        _q554 = _q1120.dlv_cfg
        _q1120.dlv_t = {}
        if _q554:
            hour = _q1235.get('hour', 0)
            _q1138 = _q1120.cfg.get('dlv_slack_until')
            _q1137 = 24 - hour - int(_q1120.cfg.get('cap_cut') or 0)
            if _q554['h0'] <= hour <= _q554['h1']:
                for _q1221 in range(n):
                    _q741 = _q735[_q1221] if _q1221 < len(_q735) else {}
                    _q1220 = [it for it in _q554['items'] if _q741.get(it, 0) > 0]
                    if not _q1220:
                        continue
                    k = sum((_q741.get(it, 0) for it in _q554['items']))
                    if (k >= _q554['kmin'] or _q1221 in _q1120.dlv_on) and ACC_D[_q1120.pos[_q1221]] + len(_q1220) <= 23 - hour:
                        if _q1138 is not None and hour < _q1138 and (_q1221 not in _q1120.dlv_on) and (_q1221 < len(_q1120.routes)):
                            _q1040 = _q1120.routes[_q1221]
                            if (_q1040.dur if _q1040.tl else 0) + ACC_D[_q1120.pos[_q1221]] + len(_q1220) > _q1137:
                                continue
                        _q1120.dlv_t[_q1221] = len(_q1220)
                        _q1120.stats['dlv_turns'] = _q1120.stats.get('dlv_turns', 0) + 1
            _q1120.dlv_on = set(_q1120.dlv_t)
        return n

    def _virtual_units(_q1120):
        """Positions / inventories / start delay of the virtual units (u >= n_units): predicted spawn tiles by the
        engine's rule (_spawn_hand: first shed-access tile with the fewest units, NW-NE-SW-SE order), empty hands,
        one turn of delay (a hand hired now acts from the next step)."""
        n = _q1120.n_units
        if _q1120.n_plan <= n:
            return
        _q930 = {a: 0 for a in ACC_ORDER}
        for _q954 in _q1120.pos[:n]:
            if _q954 in _q930:
                _q930[_q954] += 1
        for _q1221 in range(n, _q1120.n_plan):
            a = min(ACC_ORDER, key=lambda x: (_q930[x], ACC_ORDER.index(x)))
            _q930[a] += 1
            _q1120.pos.append(a)
            _q1120.invW.append(0)
            _q1120.invF.append(0)
            _q1120.invA.append({})
            _q1120.delay.append(1)

    def _sync_jobs(_q1120, tiles):
        for t in list(_q1120.chains):
            _q1244 = t in _q1120.locked
            _q743 = _q1120._refresh_job(t, tiles)
            if _q743 is None:
                _q1221 = _q1120.where.get(t)
                if _q1221 is not None:
                    _q1120._remove(_q1221, t)
                _q1120.pool.discard(t)
                _q1120.locked.discard(t)
                _q1120.res_set.discard(t)
                _q1120.jobs.pop(t, None)
                continue
            if _q743.pre == 'locked':
                _q1120.locked.add(t)
                continue
            if _q1120.held and t in _q1120.held:
                _q1221 = _q1120.where.get(t)
                if _q1221 is not None:
                    _q1120._remove(_q1221, t)
                _q1120.pool.discard(t)
                _q1120.res_set.discard(t)
                _q1120.locked.add(t)
                _q1120.stats['seed_held'] = _q1120.stats.get('seed_held', 0) + 1
                continue
            if _q1244:
                _q1120.locked.discard(t)
                _q1120.pool.add(t)
            elif t not in _q1120.where and t not in _q1120.pool and (t not in _q1120.res_set):
                _q1120.pool.add(t)

    def act(_q1120, _q1235):
        t0 = time.perf_counter()
        cfg = _q1120.cfg
        _q1120.evals = 0
        _q1120.tcap_hit = False
        _q1120.budget_end = cfg['ls_budget']
        _q1120.t_end = t0 + cfg['ls_time_ms'] / 1000.0
        tiles = _q1235['tiles']
        hour = _q1235['hour']
        _q1120.hour = hour
        _q1120.tiles = tiles
        _q1120.ret = bool(cfg.get('ret_leg'))
        _q1120.cap = max(1, 24 - hour - int(cfg.get('cap_cut') or 0)) if cfg.get('cap_cut') else 24 - hour
        n = _q1120._sync_units(_q1235)
        if n > _q1120.max_units:
            _q1120.max_units = n
        if 'pending_buys' in _q1235:
            _q1120.pending_buys = dict(_q1235.get('pending_buys') or {})
        if 'harv_need' in _q1235:
            _q1120.harv_need = frozenset(_q1235.get('harv_need') or ()) | frozenset(cfg.get('harv_need') or ())
        if cfg.get('seed_hold'):
            _q1120.held = frozenset(_q1235.get('hold_tiles') or ())
        if not _q1120.started:
            _q1120.started = True
            if cfg['rescue'] and _q1120.missed_prev:
                _q1120._add_rescues(tiles)
            if _q1120.hb:
                _q1120._harv_filter(tiles, list(_q1120.chains))
                _q1120._hb_new = set()
            for t in list(_q1120.chains):
                _q743 = _q1120._refresh_job(t, tiles)
                if _q743 is not None and _q743.pre == 'locked':
                    _q1120.locked.add(t)
            if cfg['warm'] and _q1120.template:
                _q1187 = set()
                for _q1221 in sorted(_q1120.template):
                    tl = [t for t in _q1120.template[_q1221] if t in _q1120.jobs and t not in _q1120.locked and (t not in _q1187)]
                    _q1187.update(tl)
                    _q1120.reserved[_q1221] = tl
                _q1120.res_set = _q1187
            for t in _q1120.jobs:
                if t not in _q1120.locked and t not in _q1120.res_set:
                    _q1120.pool.add(t)
        _q629 = _q1120.n_plan == 0
        _q394 = n > _q1120.n_units
        while _q1120.n_units < n:
            _q1221 = _q1120.n_units
            _q1120.n_units += 1
            if _q1221 < len(_q1120.routes):
                _q1120.stats['virt_real'] = _q1120.stats.get('virt_real', 0) + 1
                continue
            _q1120.routes.append(Route())
            if _q1221 in _q1120.reserved:
                _q1120._take_reserved(_q1221)
        if _q629 and cfg['virt'] and (_q1120.prev_hands > 0) and (hour < cfg['virt_hours']):
            for k in range(min(_q1120.prev_hands, cfg['virt_max'])):
                _q1221 = len(_q1120.routes)
                _q1120.routes.append(Route())
                _q1120.stats['virt_made'] = _q1120.stats.get('virt_made', 0) + 1
                if _q1221 in _q1120.reserved:
                    _q1120._take_reserved(_q1221)
        if len(_q1120.routes) > _q1120.n_units and hour >= cfg['virt_hours']:
            for _q1221 in range(_q1120.n_units, len(_q1120.routes)):
                for t in _q1120.routes[_q1221].tl:
                    _q1120.where.pop(t, None)
                    if t in _q1120.jobs and t not in _q1120.locked:
                        _q1120.pool.add(t)
                _q1120.stats['virt_dropped'] = _q1120.stats.get('virt_dropped', 0) + 1
            del _q1120.routes[_q1120.n_units:]
        _q1120.n_plan = len(_q1120.routes)
        _q1120._virtual_units()
        if _q1120.reserved and hour >= cfg['reserve_hours']:
            for _q1221 in list(_q1120.reserved):
                for t in _q1120.reserved.pop(_q1221):
                    _q1120.res_set.discard(t)
                    if t in _q1120.jobs and t not in _q1120.where and (t not in _q1120.locked):
                        _q1120.pool.add(t)
        if _q1120._hb_new:
            _q1120._harv_filter(tiles, list(_q1120._hb_new))
            _q1120._hb_new = set()
        _q1120._sync_jobs(tiles)
        _q1120.outW = _q1120.outF = 0
        for _q1036 in _q1120.routes:
            _q1036.oW = _q1036.oF = 0
        for _q1221 in range(_q1120.n_plan):
            _q1120._eval(_q1221, _q1120.routes[_q1221])
        sh = _q1120.shed
        _q1120.supply_on = cfg['supply_aware'] and (sh.get('WHEAT', 0) < _q1120.outW + SUPPLY_EASY or sh.get('FERTILIZER', 0) < _q1120.outF + SUPPLY_EASY)
        if _q1120.supply_on:
            _q1120.stats['supply_turns'] = _q1120.stats.get('supply_turns', 0) + 1
        _q1120._calc_shed_free()
        if _q394 and cfg['fresh_on_arrival'] and (hour > 0):
            _q1120._replan_fresh()
        _q1120._fix_overflow()
        _q1120._calc_shed_free()
        _q1120._insert_pool()
        _q1120._ls()
        _q1120._insert_pool()
        if cfg['rr'] and _q1120.n_plan:
            _q1120.is_tight = _q1120._tight()
            if cfg['turn_budget']:
                _q1189 = cfg['turn_budget']
                if _q1120.is_tight:
                    _q1189 *= cfg['tight_mult'] if _q1120.hour > 0 else cfg['tight_mult_h0']
                    _q1120.stats['tight_turns'] = _q1120.stats.get('tight_turns', 0) + 1
                _q1189 = int(_q1189 * min(1.0, _q1120.cap / float(cfg['budget_full_cap'])))
                _q1120.budget_end = max(_q1120.evals, _q1189 - cfg['ls_budget'] // 2)
            else:
                _q1120.budget_end = _q1120.evals + cfg['rr_budget']
            if _q1120._rr():
                _q1120.budget_end = _q1120.evals + cfg['ls_budget'] // 2
                _q1120._ls()
        _q1120.stats['evals'] += _q1120.evals
        if _q1120.tcap_hit:
            _q1120.stats['tcap_turns'] = _q1120.stats.get('tcap_turns', 0) + 1
        _q1120._snap = (_q1120.cap, [(_q1036.dur, bool(_q1036.tl)) for _q1036 in _q1120.routes])
        _q1120._svc = set()
        return _q1120._actions(_q1235)

    def _tight(_q1120):
        """A turn is tight when some job does not fit (pool) or the routes' total slack is below tight_slack of the
        unit-turns left."""
        if _q1120.hour < _q1120.cfg['tight_min_hour'] or _q1120.n_plan < _q1120.cfg['tight_min_units']:
            return False
        if _q1120.pool:
            return True
        U = _q1120.n_plan
        slack = sum((_q1120.cap - _q1120.delay[_q1221] - _q1036.dur for _q1221, _q1036 in enumerate(_q1120.routes[:U])))
        return slack < _q1120.cfg['tight_slack'] * U * _q1120.cap

    def _take_reserved(_q1120, _q1221):
        tl = [t for t in _q1120.reserved.pop(_q1221) if t in _q1120.jobs and t not in _q1120.where and (t not in _q1120.locked)]
        for t in tl:
            _q1120.res_set.discard(t)
            _q1120.where[t] = _q1221
            _q1120.pool.discard(t)
        _q1120.routes[_q1221].tl = tl

    def _replan_fresh(_q1120):
        """Fresh construction for all present units; keep it if cheaper than the repaired plan."""
        _q1120.stats['replans'] += 1
        _q1120._fix_overflow()
        _q1120._insert_pool()
        _q934 = _q1120._plan_total()
        _q1054 = [list(_q1036.tl) for _q1036 in _q1120.routes]
        _q1053 = set(_q1120.pool)
        _q1055 = dict(_q1120.where)
        seeds = []
        for _q1221, _q1036 in enumerate(_q1120.routes):
            keep = []
            for _q712, t in enumerate(_q1036.tl):
                _q743 = _q1120.jobs[t]
                if _q712 == 0 and _q1221 < _q1120.n_units and (_q1120.pos[_q1221] == t % NT) or _q1120._pinned(_q1221, _q743):
                    keep.append(t)
            seeds.append(keep)
        _q1117 = set((t for s in seeds for t in s))
        _q384 = [t for t in _q1120.jobs if t not in _q1120.locked and t not in _q1120.res_set and (t not in _q1117)]
        _q1120.where = {}
        for _q1221, _q1036 in enumerate(_q1120.routes):
            _q1036.tl = list(seeds[_q1221])
            _q1120._eval(_q1221, _q1036)
            for t in _q1036.tl:
                _q1120.where[t] = _q1221
        _q1120.pool = set()
        _q1120._calc_shed_free()
        _q799 = _q1120._construct(_q384)
        _q1120.pool = set(_q799)
        _q1120._insert_pool()
        _q903 = _q1120._plan_total()
        if _q903 < _q934 - 1e-09:
            _q1120.stats['fresh_wins'] += 1
            return
        for _q1221, _q1036 in enumerate(_q1120.routes):
            _q1036.tl = list(_q1054[_q1221])
            _q1120._eval(_q1221, _q1036)
        _q1120.where = _q1055
        _q1120.pool = _q1053
        _q1120._calc_shed_free()

    def _actions(_q1120, _q1235):
        tiles = _q1235['tiles']
        acts = []
        for _q1221 in range(_q1120.n_units):
            acts.append(_q1120._unit_action(_q1221, _q1120.routes[_q1221], _q1120.pos[_q1221], tiles))
        return acts

    def _kit_need(_q1120, _q1221, _q1036):
        need = []
        nW, nF, A = (_q1036.nW, _q1036.nF, _q1036.A)
        _q803 = _q1120.cfg['lone_h']
        if _q803 and _q1120.n_units == 1 and (_q1120.n_plan == 1) and (_q1036.A or _q1120.supply_on):
            _q960, _q962, _q961 = _q1120._route_prefix_needs(_q1221, _q1036, _q803)
            A = _q960
            if _q1120.supply_on:
                nW, nF = (_q962, _q961)
        if _q1120.cfg['supply_aware']:
            if nW > _q1120.invW[_q1221]:
                q = nW - _q1120.invW[_q1221]
                spare = _q1120.shed.get('WHEAT', 0) - _q1120.outW
                need.append(('WHEAT', q + max(0, min(_q1120.cfg['margin_w'], spare))))
            if nF > _q1120.invF[_q1221]:
                q = nF - _q1120.invF[_q1221]
                spare = _q1120.shed.get('FERTILIZER', 0) - _q1120.outF
                need.append(('FERTILIZER', q + max(0, min(_q1120.cfg['margin_f'], spare))))
        else:
            if _q1036.nW > _q1120.invW[_q1221]:
                need.append(('WHEAT', _q1036.nW - _q1120.invW[_q1221] + _q1120.cfg['margin_w']))
            if _q1036.nF > _q1120.invF[_q1221]:
                need.append(('FERTILIZER', _q1036.nF - _q1120.invF[_q1221] + _q1120.cfg['margin_f']))
        if A:
            h0 = _q1120.cfg['h0_animal_h']
            if h0 and _q1120.hour == 0 and (_q1120.n_units == 1):
                A = _q1120._route_animals_within(_q1221, _q1036, h0)
            for k, c in A.items():
                if c > _q1120.invA[_q1221].get(k, 0):
                    need.append((k, c - _q1120.invA[_q1221].get(k, 0)))
        if _q1120.cfg['nosupply_skip']:
            need = [x for x in need if _q1120.shed.get(x[0], 0) > 0]
        return need

    def _route_prefix_needs(_q1120, _q1221, _q1036, H):
        """(animals, start WHEAT need, start FERTILIZER need) of the jobs this route starts within H turns."""
        A = {}
        _q1214 = _q1036.kt
        _q954 = _q1036.sp
        jobs = _q1120.jobs
        _q367 = _q363 = _q824 = _q823 = 0
        for t in _q1036.tl:
            _q1214 += D[_q954][t]
            if _q1214 >= H:
                break
            _q743 = jobs[t]
            if _q743.a:
                for k, c in _q743.a.items():
                    A[k] = A.get(k, 0) + c
            _q367 += _q743.dw
            _q363 += _q743.df
            if _q367 > _q824:
                _q824 = _q367
            if _q363 > _q823:
                _q823 = _q363
            _q1214 += _q743.s
            _q954 = t
        return (A, _q824, _q823)

    def _kit_defer(_q1120, _q1221, _q1036, _q954):
        """kit_way (B5, first-leg kits).  True -> the unit serves its head job now and fetches its kit later.
        Only the leading jobs it can serve with what it carries qualify (order-aware net WHEAT / FERTILIZER needs,
        carried animals), and never when no later job needs the kit.
          'block': the unit stands on a shed-access tile and the head job is on an access tile - the kit is picked up
                   there afterwards (same turns, same route model; the productive command comes first: a hand's first
                   leg starts with the animals at the shed);
          'way'  : 'block', plus a unit away from the shed defers when fetching the kit between two later jobs (the
                   shed on the way) is strictly shorter than the detour now, and its route slack covers the start-kit
                   charge the route model keeps making meanwhile (the model stays conservative)."""
        tl = _q1036.tl
        n = len(tl)
        if not n:
            return False
        jobs = _q1120.jobs
        _q742, _q714 = (_q1120.invW[_q1221], _q1120.invF[_q1221])
        _q715 = _q1120.invA[_q1221]
        cw = cf = 0
        _q1223 = None
        _q772 = 0
        for _q712 in range(n):
            _q743 = jobs.get(tl[_q712])
            if _q743 is None:
                break
            cw += _q743.dw
            cf += _q743.df
            if _q743.w and cw > _q742 or (_q743.f and cf > _q714):
                break
            if _q743.a:
                _q1223 = dict(_q1223) if _q1223 else {}
                short = False
                for k, c in _q743.a.items():
                    _q1223[k] = _q1223.get(k, 0) + c
                    if _q1223[k] > _q715.get(k, 0):
                        short = True
                if short:
                    break
            _q772 = _q712 + 1
        if _q772 == 0 or _q772 >= n:
            return False
        _q723 = _q954 in ACCESS
        if _q723:
            if tl[0] % NT in ACCESS:
                _q1120.stats['kit_defer'] = _q1120.stats.get('kit_defer', 0) + 1
                return True
            return False
        if _q1120.kw != 'way':
            return False
        best = ACC_D[_q954] + D[ACC_NEAR[_q954]][tl[0]] - D[_q954][tl[0]]
        _q416 = 0
        for _q746 in range(1, _q772 + 1):
            x, _q1272 = (tl[_q746 - 1], tl[_q746])
            _q539 = ACC_D[x] + D[ACC_NEAR[x]][_q1272] - D[x][_q1272]
            if _q539 < best:
                best, _q416 = (_q539, _q746)
        if _q416 == 0:
            return False
        if _q1120.cap - _q1036.dur < 2 * max((ACC_D[x] for x in tl[:_q416])):
            return False
        _q1120.stats['kit_way'] = _q1120.stats.get('kit_way', 0) + 1
        return True

    def _route_animals_within(_q1120, _q1221, _q1036, H):
        """Animals of the PLACE jobs this route starts within H turns (graft from the zones / imitate executors: the
        lone farmer at hour 0 plans provisionally for the whole farm and must not hoard every animal - a carried
        animal pins its PLACE job to the carrier, so the hands that appear next turn could not take them)."""
        A = {}
        _q1214 = _q1036.kt
        _q954 = _q1036.sp
        jobs = _q1120.jobs
        for t in _q1036.tl:
            _q1214 += D[_q954][t]
            if _q1214 >= H:
                break
            _q743 = jobs[t]
            if _q743.a:
                for k, c in _q743.a.items():
                    A[k] = A.get(k, 0) + c
            _q1214 += _q743.s
            _q954 = t
        return A

    def _unit_action(_q1120, _q1221, _q1036, _q954, tiles):
        while _q1036.tl and _q1036.tl[0] not in _q1120.chains:
            t = _q1036.tl.pop(0)
            _q1120.where.pop(t, None)
        if _q1120.dlv_t and _q1120.dlv_t.get(_q1221):
            if _q954 in ACCESS:
                _q741 = _q1120.cur_inv[_q1221] if _q1221 < len(_q1120.cur_inv) else {}
                _q739 = [(_q741.get(it, 0), it) for it in _q1120.dlv_cfg['items'] if _q741.get(it, 0) > 0]
                if _q739:
                    q, it = max(_q739)
                    _q1120.stats['dlv_place'] = _q1120.stats.get('dlv_place', 0) + 1
                    return ['PLACE', it, int(q)]
            else:
                return [_step(_q954, ACC_NEAR[_q954])]
        if not _q1036.tl:
            _q1120._eval(_q1221, _q1036)
            return _q1120._idle_action(_q1221, _q954)
        need = _q1120._kit_need(_q1221, _q1036)
        if need and _q1120.kw and _q1120._kit_defer(_q1221, _q1036, _q954):
            need = None
        if need:
            if _q954 in ACCESS:
                need.sort(key=lambda x: (x[0] not in ANIMALS, -x[1]))
                for item, q in need:
                    avail = _q1120.shed.get(item, 0)
                    if avail > 0:
                        return ['PICKUP', item, int(min(q, avail))]
            else:
                _q1120.stats['detours'] += 1
                return [_step(_q954, ACC_NEAR[_q954])]
        t = _q1036.tl[0]
        if _q954 != t % NT:
            return [_step(_q954, t)]
        _q743 = _q1120.jobs[t]
        _q481 = _q1120.chains[t]
        if _q743.pre in ('dig', 'harvest'):
            _q1120.stats['recover'] += 1
            _q493 = 'DIG' if _q743.pre == 'dig' else 'HARVEST'
            _q743.pre = None
            _q743.s = len(_q481)
            _q1120._served(_q1221, t)
            _q1120._svc.add(_q1221)
            return [_q493]
        op, arg = _q481[0]
        if op == 'FEED' and _q1120.invW[_q1221] <= 0 or (op == 'FERTILIZE' and _q1120.invF[_q1221] <= 0) or (op == 'PLACE' and _q1120.invA[_q1221].get(arg, 0) <= 0):
            item = 'WHEAT' if op == 'FEED' else 'FERTILIZER' if op == 'FERTILIZE' else arg
            if _q1120.cfg['supply_aware'] and _q1120.shed.get(item, 0) <= 0 and (item in ('WHEAT', 'FERTILIZER')) and _q1120._spare_elsewhere(_q1221, item):
                _q1120.stats['handback'] = _q1120.stats.get('handback', 0) + 1
                _q1036.tl.pop(0)
                _q1120.where.pop(t, None)
                _q1120.pool.add(t)
                return _q1120._unit_action(_q1221, _q1036, _q954, tiles)
            if _q1120.cfg['nosupply_skip'] and _q1120.shed.get(item, 0) <= 0:
                if _q1120.wait_on and op == 'PLACE' and (_q1120.pending_buys.get(arg, 0) > 0):
                    _q1120.stats['place_wait'] = _q1120.stats.get('place_wait', 0) + 1
                    _q1036.tl.pop(0)
                    _q1120.where.pop(t, None)
                    _q1120.pool.add(t)
                    return _q1120._unit_action(_q1221, _q1036, _q954, tiles)
                _q1120.stats['nosupply'] += 1
                _q481.pop(0)
                if not _q481:
                    _q1120.chains.pop(t, None)
                    _q1036.tl.pop(0)
                    _q1120.where.pop(t, None)
                    _q1120.jobs.pop(t, None)
                    return _q1120._unit_action(_q1221, _q1036, _q954, tiles)
                _q743.s = len(_q481)
                return _q1120._unit_action(_q1221, _q1036, _q954, tiles)
            _q1120.stats['detours'] += 1
            if _q954 in ACCESS:
                item = 'WHEAT' if op == 'FEED' else 'FERTILIZER' if op == 'FERTILIZE' else arg
                return ['PICKUP', item, 1 + (_q1120.cfg['margin_w'] if op == 'FEED' else 0)]
            return [_step(_q954, ACC_NEAR[_q954])]
        _q481.pop(0)
        if op == 'FEED':
            _q1120.invW[_q1221] -= 1
        elif op == 'FERTILIZE':
            _q1120.invF[_q1221] -= 1
        elif op == 'PLACE':
            _q1120.invA[_q1221][arg] -= 1
        _q1120._served(_q1221, t)
        _q1120._svc.add(_q1221)
        if not _q481:
            _q1120.chains.pop(t, None)
            _q1036.tl.pop(0)
            _q1120.where.pop(t, None)
            _q1120.jobs.pop(t, None)
        else:
            _q743.s = len(_q481)
        if arg is None or arg == '_aux':
            return [op]
        return [op, arg]

    def _spare_elsewhere(_q1120, _q1221, item):
        for _q1233 in range(_q1120.n_units):
            if _q1233 == _q1221:
                continue
            _q1095 = _q1120.routes[_q1233]
            if item == 'WHEAT' and _q1120.invW[_q1233] > _q1095.nW:
                return True
            if item == 'FERTILIZER' and _q1120.invF[_q1233] > _q1095.nF:
                return True
        return False

    def _served(_q1120, _q1221, t):
        s = _q1120.served.setdefault(_q1221, [])
        if t not in s:
            s.append(t)

    def _idle_action(_q1120, _q1221, _q954):
        if _q1120.cfg['prepos'] and _q1120.locked:
            _q807 = _q1120.locked - _q1120.held if _q1120.held else _q1120.locked
            if _q807:
                _q1193 = min(_q807, key=lambda t: (D[_q954][t], t))
                if D[_q954][_q1193] > 1:
                    return [_step(_q954, _q1193)]
        return ['PASS']
EDFKitsExecutor = PDExecutor