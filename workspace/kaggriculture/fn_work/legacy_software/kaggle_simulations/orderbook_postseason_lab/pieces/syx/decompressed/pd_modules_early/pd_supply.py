"""PD - Supply controller (C7) and Fertiliser allocator (C9) of the coordinated planner system ("CS").
(Original work, Shawn404, 27 Sep 2026.)  Spec: results/portable/sys_design.txt 6.5 (C7) and 6.7 (C9); DSM reference
numbers from results/portable/sys_timeline.txt.  Pure Python, no engine import, no file access.  Build report + exact
API: results/portable/cs_build_B3.txt; tests tools/tmp/cs_b3_test.py.

    sup = Supply(cfg)                                    # one per seat, lives across days
    rows = sup.step(S, ex, final_cmds, hour, day, pending)   # every step, after the guards (+ replanter), before the market
        -> [(prio, ['BUY_SEED' | 'BUY_PRODUCT' | 'BUY_ANIMAL', item, n]), ...] sorted by prio (0 most urgent)
    orders = Supply.plain(rows)                          # the bare market orders, same order
    rows = Supply.pack(rows, k)                          # merge rows of the same (op, item) until <= k rows remain
    sup.w_keep                                           # shed WHEAT the market must not sell below this step
    sup.keep_over(reserve_w)                             # extra WHEAT hold over a market controller's own reserve
    sup.animal_buys                                      # {animal: n} issued this step (-> ex.note_buys)
    fert = Fert(cfg)
    chains = fert.plan_day(S, chains, collections_today) # hour 0, before ex.begin_day: FERTILIZE ops cut to the budget
    sells = fert.sell_orders(S, hour, quote, kept_ops)   # hours 0-2 surplus sale rows (<= 4 units each); day 29: all
    fert.reserve(kept_ops, collections)                  # shed FERTILIZER the market's other sale rows must keep

Engine facts used (kaggriculture 1.32.x): units act before the market, so a seed / wheat / animal bought at step t is
usable from step t+1; bought WHEAT / FERTILIZER / animals land in the shed (they need shed room, cap 100), seeds live
outside the shed; the engine drops ALL PLANTs of a crop in a step whose PLANT count exceeds the seeds held (atomic PLANT
rule); FEED needs a carried WHEAT, FERTILIZE a carried FERTILIZER, PLACE a carried animal; HARVEST puts the tile's units
into the unit's inventory; COLLECT_FERTILIZER +1 FERTILIZER.

Executor API used (tools/pd/pd_exec.py, task B5): ex.route_ops(H) -> [(unit, eta, (x, y), op, arg)] for the ops the
routes start within H turns, eta counted from the NEXT step (eta 0 = the command at step t+1 when called after act() of
step t; route_ops(H) returns eta < H); ex.pending_ops() -> {op: count}; ex.chains ({tile index y*10+x: [(op, arg)]},
read-only, for the per-crop / per-animal detail; a split collect sub-job has the same tile index);
ex.note_buys({animal: n}) is fed by the caller from Supply.animal_buys.  Without route_ops (an executor before B5) the
routes are walked from ex.routes / ex.chains the same way (_route_ops_fallback).  "Due within h turns" below = eta < h;
"next turn" = eta 0.

SUPPLY (C7), every step
  Seeds, per crop c:
    used_now[c] = PLANT c in this step's final commands (consumed before the market; 0 if the atomic rule blocks them);
    due[c]      = PLANT c ops in route_ops(seed_h[c]) = eta < seed_h[c] (WHEAT 2: steps t+1, t+2) (+ PLANT chains that
                  appeared since the last step and are not routed yet: a replanter / land-fill job on the tile its unit
                  stands on is planted next step);
    buffer[c]   = seed_buf[c] (WHEAT 6, CARROT 2 (+6 when >= 4 carrot PLANTs are due within 6 h), TOMATO 2, STRAWBERRY 0,
                  MELON 0), only on days <= last_day[c], and never more than today's remaining PLANT c ops beyond the due
                  ones plus the overnight buffer (the overnight buffer only while tomorrow can still plant c);
    buy[c]      = max(0, due[c] + buffer[c] - (seeds[c] - used_now[c]) - pending[c]).
    STRAWBERRY looks 8 turns ahead (seed_h) with no buffer (DSM holds 0.2; 69% of its seeds planted within 8 steps).
    Priority: the part short for the PLANTs due next turn (eta 0) -> P_DUE; the rest -> P_BUFFER.
  Feed wheat (days < 29):
    Walk every unit's route (route_ops over the rest of the day) with its carried WHEAT after this step: a wheat HARVEST
    credits max(0, units - 1) (the executor's own credit rule), a FEED takes one unit or counts as short (must-feed
    animal -> critical short).  FEED ops in chains that no route holds are short too.
    need_rem = max(0, short - spare_use x spare)   (spare = wheat left at the end of the routes)
             = FEEDs left - carried - own harvest credited earlier in the same routes, in the aggregate.
    h0 / h1 / h9 (wheat_hours): buy max(0, need_rem + wheat_margin - shed) in one row; nothing while
      shed - need_rem > wheat_surplus_max; at h9 (margin_if_short_hours) only when the shed is short for today's FEEDs
      (the re-check).  The part short for today's FEEDs -> P_FEED, the margin -> P_BUFFER.
    any hour: emergency lot (P_FEED) when the critical shorts exceed shed + spare (a must-feed animal no unit can feed).
    day-10 bridge (bridge_day, bridge_hours 9 / 10): FEEDs of days 10-12 (today's left + animals x 2 days) minus shed,
      carried and the own wheat harvestable by day 12 -> bought (P_BRIDGE, cash clipped by the engine).
  Animals: PLACE a (or the BUILD before it on the same tile) in route_ops(anim_h = 8) and not covered by the animals in
    the shed / carried -> BUY_ANIMAL (P_ANIMAL).  A PLACE the executor cannot route without its animal (pool) is bought
    from anim_pool_hour (the executor schedules it the step after the animal arrives).  After anim_fail_max failed tries
    (an issued buy whose animal did not arrive) the animal falls back to the batch: every pending PLACE of it is bought,
    retried until anim_retry_h; after that it is reported in .unfunded (C12 may drop those PLACE / FEED / CARE ops).
    P8 cfg herd_cap {animal: max count} (None = off): each buy is cut so the animals owned (standing + shed + carried) +
    pending + the buy stay <= the cap.
  Fertiliser: fert_buy 'chain' (default) buys only the FERTILIZE ops actually in the chains that the shed, the carried
    units and 0.95 x the pending COLLECT ops cannot cover, at quotes <= fert_q0 (hours 0-2) / fert_q (hours 3-20) - the
    leak-free replacement of pd_plan's hour-0 order (which counted never-scheduled level-1 plan fertilisers) and of the
    layer's _pd_topup.  fert_buy None = never buy (design 6.5; MEASURED -525, t -2.0 on cs_T1Lm - keep it a switch).
  Priorities: P_FEED 0 (wheat for today's FEEDs / must-feed) < P_DUE 1 (seeds for PLANTs due next turn) <
    P_ANIMAL 2 < P_BUFFER 3 (seed buffers, wheat margin, fertiliser) < P_BRIDGE 4.  cfg merge True: one row per
    (op, item), carrying its most urgent priority.
  CS build-2 review fixes (results/portable/cs_build2_review.txt; each a cfg key, off by default = the behaviour above):
    seed_today   the seeds of EVERY PLANT still in today's chains on an unlocked tile are bought now (P_TODAY 1.5,
                 ahead of the animals), not only the PLANTs due within seed_h.  JIT seeds let a same-step animal buy
                 (P_ANIMAL) take the cash of a cash-short day (day 9 after the land, day 10) and the later-due seeds
                 then found no cash: units stood on seed-blocked PLANT tiles for hours (44-66 blocked turns, day-9
                 plantings 17 -> 3 in a smoke world).  The plan's own batch (the parent) buys the day's seeds first.
    wheat_retry  the P_FEED deficit issued at a wheat hour is re-issued at the next steps (<= emergency_last_h) while
                 it is still short: the layer never carries Supply rows, so a P_FEED row cut by cash / the order
                 window at h1 otherwise waited for h9.
    note_sent()  the caller reports the rows that survived its packing: an animal row it never sent is not a failed
                 try (it counted towards the fallback / unfunded state).

FERTILISER ALLOCATOR (C9), hour 0 (6.7)
  Budget B = shed + carried + collect_eff (0.95) x today's COLLECT_FERTILIZER ops.  Each FERTILIZE op in the chains is
  valued per unit of fertiliser: pd_tasks' marginal units (wheat age 2 +2, carrot age 2 +1, strawberry ages 9 / 13 and
  tomato 7 / 10: the productions it covers) x the crop's quote.  Kept best-first within (1 - sell_share) x B (sell_share:
  the share of the day's fertiliser kept for sale - a fertiliser unit we stop selling pays the tape rival, measured on
  cs_T1Lm: own +2.9k, rival +2.8k), and only while value >= min_ratio x fertiliser quote + rival_add; the rest are cut from
  the chains.
  Sale (sell_orders): hours 0-2 sell the shed fertiliser above (kept ops - 0.9 x collections) in rows of <= 4:
  quote >= $30 all of it; $15-30 half (the rest kept, the kept hoard <= 20); < $15 none (kept for own use; only the
  stock above hoard_low_max); day 29: everything.
"""
import math
import time
import pd_tasks as _PT
from pd_state import ACCESS, ANIMALS, CROPS, FINAL_DAY
ACCESS_SET = frozenset(ACCESS)
STRUCT_OF = {'GOOSE': 'COOP', 'COW': 'PASTURE', 'SHEEP': 'PASTURE'}
BUILD_OPS = {'BUILD_COOP': 'COOP', 'BUILD_PASTURE': 'PASTURE'}
PRODUCT_OF = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}
SEED_ORDER = ('STRAWBERRY', 'TOMATO', 'MELON', 'CARROT', 'WHEAT')
ANIMAL_ORDER = ('COW', 'SHEEP', 'GOOSE')
P_FEED, P_DUE, P_ANIMAL, P_BUFFER, P_BRIDGE = (0, 1, 2, 3, 4)
P_TODAY = 1.5
SUPPLY_CFG = {'seeds': True, 'seed_buf': {'WHEAT': 6, 'CARROT': 2, 'TOMATO': 2, 'STRAWBERRY': 0, 'MELON': 0}, 'seed_h': {'WHEAT': 2, 'CARROT': 2, 'TOMATO': 2, 'STRAWBERRY': 8, 'MELON': 2}, 'carrot_block': (6, 6, 4), 'last_day': {'WHEAT': 27, 'CARROT': 27, 'TOMATO': 20, 'STRAWBERRY': 17, 'MELON': 19}, 'new_chain_due': True, 'wheat': True, 'wheat_hours': (0, 1, 9), 'wheat_margin': 6, 'margin_if_short_hours': (9,), 'wheat_surplus_max': 10, 'spare_use': 1.0, 'credit': True, 'emergency': True, 'emergency_margin': 1, 'emergency_last_h': 21, 'topup_any_hour': False, 'bridge_day': 10, 'bridge_hours': (9, 10), 'bridge_days': 3, 'bridge_rate': 1.0, 'animals': True, 'anim_h': 8, 'anim_pool_hour': 1, 'anim_fail_max': 2, 'anim_retry_h': 10, 'anim_last_h': 20, 'fert_buy': 'chain', 'fert_q0': 60.0, 'fert_q': 80.0, 'fert_hours': (0, 20), 'collect_eff': 0.95, 'merge': True, 'seed_today': False, 'wheat_retry': False, 'animal_order': ANIMAL_ORDER, 'herd_cap': None}
FERT_CFG = {'collect_eff': 0.95, 'sell_share': 0.4, 'min_ratio': 1.0, 'rival_add': 0.0, 'max_use': None, 'unit_value': None, 'sell_hours': (0, 1, 2), 'row_max': 4, 'rows_max': 3, 'keep_collect': 0.9, 'hi': 30.0, 'lo': 15.0, 'hoard_max': 20, 'hoard_low_max': 40, 'buy_extra': None}

def _tile(S, xy):
    return S.tiles[xy[1]][xy[0]]

def _xy(t):
    if isinstance(t, tuple):
        return t
    return (t % 10, t // 10)

def after_units(S, _q441):
    """The farm at market time: this step's unit commands (farmer first, then hands) applied with the engine's rules to
    the shed, the seeds and every unit's inventory.  Returns dict(shed, seeds, inv (list per unit), planted {crop: n},
    blocked (crops the atomic rule drops), fed (tiles fed this step))."""
    shed = {k: int(_q1159) for k, _q1159 in S.shed.items() if _q1159}
    seeds = {k: int(_q1159) for k, _q1159 in S.seeds.items() if _q1159}
    _q672 = [dict(_q652) for _q652 in S.inventories]
    n = min(len(S.units), len(_q441 or ()))
    _q489 = {}
    for _q1147 in range(n):
        c = _q441[_q1147]
        if isinstance(c, (list, tuple)) and len(c) >= 2 and (c[0] == 'PLANT'):
            _q489[c[1]] = _q489.get(c[1], 0) + 1
    blocked = {k for k, _q1159 in _q489.items() if _q1159 > seeds.get(k, 0)}
    planted = {}
    fed = set()
    cap = int(getattr(S, 'shed_capacity', 100) or 100)
    tiles = S.tiles
    for _q1147 in range(n):
        c = _q441[_q1147]
        if not isinstance(c, (list, tuple)) or not c:
            continue
        op = c[0]
        x, _q1197 = S.units[_q1147]
        while len(_q672) <= _q1147:
            _q672.append({})
        inv = _q672[_q1147]
        t = tiles[_q1197][x]
        _q319 = (x, _q1197) in ACCESS_SET
        if op == 'PICKUP':
            if _q319 and len(c) >= 2:
                q = int(c[2]) if len(c) >= 3 else 1
                q = min(max(0, q), shed.get(c[1], 0))
                if q > 0:
                    shed[c[1]] -= q
                    inv[c[1]] = inv.get(c[1], 0) + q
            continue
        if op == 'DROP':
            if _q319:
                for _q675, q in list(inv.items()):
                    room = max(0, cap - sum(shed.values()))
                    k = min(int(q), room)
                    if k > 0:
                        shed[_q675] = shed.get(_q675, 0) + k
                    del inv[_q675]
            continue
        if op == 'PLACE':
            if len(c) < 2:
                continue
            _q675 = c[1]
            if _q675 in ANIMALS and isinstance(t, dict) and (t.get('kind') == STRUCT_OF[_q675]) and ('animal' not in t):
                if inv.get(_q675, 0) > 0:
                    inv[_q675] -= 1
                continue
            if _q319:
                q = int(c[2]) if len(c) >= 3 else 1
                q = min(max(0, q), inv.get(_q675, 0), max(0, cap - sum(shed.values())))
                if q > 0:
                    inv[_q675] -= q
                    shed[_q675] = shed.get(_q675, 0) + q
            continue
        if t == 'LOCKED':
            continue
        if op == 'PLANT':
            if len(c) >= 2 and c[1] in CROPS and (c[1] not in blocked) and (t is None) and (seeds.get(c[1], 0) > 0):
                seeds[c[1]] -= 1
                planted[c[1]] = planted.get(c[1], 0) + 1
        elif op == 'FEED':
            if isinstance(t, dict) and 'animal' in t and (not t.get('fed_today')) and ((x, _q1197) not in fed) and (inv.get('WHEAT', 0) > 0):
                inv['WHEAT'] -= 1
                fed.add((x, _q1197))
        elif op == 'FERTILIZE':
            if isinstance(t, dict) and t.get('kind') == 'PLANT' and (inv.get('FERTILIZER', 0) > 0):
                inv['FERTILIZER'] -= 1
        elif op == 'HARVEST':
            if isinstance(t, dict) and int(t.get('yield_units', 0) or 0) > 0:
                if t.get('kind') == 'PLANT':
                    _q458 = t.get('crop')
                    if _q458 in CROPS and S.day - int(t.get('planted_day', S.day)) >= CROPS[_q458]['fyd']:
                        inv[_q458] = inv.get(_q458, 0) + int(t['yield_units'])
                elif t.get('animal') in PRODUCT_OF:
                    _q675 = PRODUCT_OF[t['animal']]
                    inv[_q675] = inv.get(_q675, 0) + int(t['yield_units'])
        elif op == 'COLLECT_FERTILIZER':
            if isinstance(t, dict) and 'animal' in t and t.get('fertilizer_available'):
                inv['FERTILIZER'] = inv.get('FERTILIZER', 0) + 1
    return {'shed': shed, 'seeds': seeds, 'inv': _q672, 'planted': planted, 'blocked': blocked, 'fed': fed}

def _route_ops_fallback(ex, H):
    """route_ops(H) for an executor without the B5 API: the same walk over ex.routes (kit turns + Manhattan travel +
    one turn per chain op, a clearing DIG / HARVEST listed first when the job has one), eta from the next step (the
    step's own command is assumed to be a move: kit turns - 1), ops with eta < H."""
    _q880 = []
    routes = getattr(ex, 'routes', None) or []
    chains = getattr(ex, 'chains', None) or {}
    jobs = getattr(ex, 'jobs', None) or {}
    for _q1147, _q970 in enumerate(routes):
        tl = list(getattr(_q970, 'tl', ()) or ())
        if not tl:
            continue
        _q1140 = int(getattr(_q970, 'kt', 0) or 0) - 1
        _q888 = getattr(_q970, 'sp', -1)
        if _q888 is None or _q888 < 0:
            try:
                _q888 = ex.pos[_q1147]
            except Exception:
                _q888 = 44
        px, _q960 = (_q888 % 10, _q888 // 10)
        for t in tl:
            _q428 = chains.get(t)
            _q681 = jobs.get(t)
            if _q681 is None or not _q428:
                continue
            x, _q1197 = (t % 10, t // 10)
            _q1140 += abs(px - x) + abs(_q960 - _q1197)
            px, _q960 = (x, _q1197)
            if _q1140 >= H:
                break
            _q520 = _q1140
            if getattr(_q681, 'pre', None) in ('dig', 'harvest'):
                _q880.append((_q1147, max(0, _q520), (x, _q1197), 'DIG' if _q681.pre == 'dig' else 'HARVEST', None))
                _q520 += 1
            for op, arg in _q428:
                if _q520 >= H:
                    break
                _q880.append((_q1147, max(0, _q520), (x, _q1197), op, None if arg == '_aux' else arg))
                _q520 += 1
            _q1140 += int(getattr(_q681, 's', len(_q428)) or len(_q428))
    return _q880

def _route_ops(ex, H):
    f = getattr(ex, 'route_ops', None)
    if callable(f):
        return list(f(H) or ())
    return _route_ops_fallback(ex, H)

def scan_chains(ex):
    """{(op, arg): count} of the ops still in the executor's chains and {(x, y): [(op, arg)]} (ex.chains when present,
    else ex.pending_ops() - then only op-level counts, keyed (op, None))."""
    _q453 = {}
    tiles = {}
    _q428 = getattr(ex, 'chains', None)
    if isinstance(_q428, dict):
        for t, ops in _q428.items():
            xy = _xy(t)
            _q753 = []
            for _q857 in ops or ():
                op = _q857[0]
                arg = _q857[1] if len(_q857) > 1 else None
                k = (op, arg if op in ('PLANT', 'PLACE') else None)
                _q453[k] = _q453.get(k, 0) + 1
                _q753.append((op, arg))
            if _q753:
                if xy in tiles:
                    tiles[xy] = tiles[xy] + _q753
                else:
                    tiles[xy] = _q753
        return (_q453, tiles)
    f = getattr(ex, 'pending_ops', None)
    if callable(f):
        for k, _q1159 in (f() or {}).items():
            if isinstance(k, tuple):
                _q453[k[0], k[1] if k[0] in ('PLANT', 'PLACE') else None] = int(_q1159)
            else:
                _q453[k, None] = int(_q1159)
    return (_q453, tiles)

def _norm_pending(pending):
    """{(op, item): units} of purchase orders already queued for this step's market by other code: a list of market
    orders, or a dict keyed (op, item) - string keys: an animal -> BUY_ANIMAL, 'seed_<CROP>' -> BUY_SEED, 'WHEAT' /
    'FERTILIZER' -> BUY_PRODUCT."""
    _q880 = {}
    if not pending:
        return _q880
    if isinstance(pending, dict):
        for k, _q1159 in pending.items():
            if isinstance(k, tuple):
                key = (k[0], k[1])
            elif k in ANIMALS:
                key = ('BUY_ANIMAL', k)
            elif isinstance(k, str) and k.startswith('seed_'):
                key = ('BUY_SEED', k[5:])
            else:
                key = ('BUY_PRODUCT', k)
            _q880[key] = _q880.get(key, 0) + int(_q1159)
        return _q880
    for _q857 in pending:
        if isinstance(_q857, (list, tuple)) and len(_q857) >= 3 and (_q857[0] in ('BUY_SEED', 'BUY_PRODUCT', 'BUY_ANIMAL')):
            try:
                _q880[_q857[0], _q857[1]] = _q880.get((_q857[0], _q857[1]), 0) + int(_q857[2])
            except (TypeError, ValueError):
                pass
    return _q880

def wheat_by(_q458, day, _q478):
    """Wheat units crop cr delivers at its harvest if that falls on or before day d2 (cut at age 3 when fertilised,
    else age 4; one WATER a day in the yield window, +2 fertilised / +1; decay ignored), else 0."""
    if _q458.crop != 'WHEAT':
        return 0
    fert = _q458.fert_until >= _q458.planted_day + 3
    _q635 = _q458.planted_day + (3 if fert else 4)
    if _q635 > _q478:
        return 0
    _q1147 = _q458.units
    _q1190 = (CROPS['WHEAT']['myd'] + 1) // 2
    for _q475 in range(max(day, _q458.planted_day + _q1190), _q635 + 1):
        if _q475 == day and _q458.watered:
            continue
        _q1147 = min(CROPS['WHEAT']['max_yield'], _q1147 + (2 if _q458.fert_until >= _q475 else 1))
    return _q1147

class Supply:
    """Per-step purchasing driven by the executor's routes (design 6.5).  One instance per seat."""

    def __init__(_q1052, cfg=None):
        _q1052.cfg = dict(SUPPLY_CFG)
        if cfg:
            _q1052.cfg.update(cfg)
        _q1052.day = -1
        _q1052.fert_req = None
        _q1052.hold = set()
        _q1052.w_keep = 0
        _q1052.last = {}
        _q1052.failed_parts = set()
        _q1052.unfunded = {}
        _q1052.animal_buys = {}
        _q1052.errors = 0
        _q1052.last_error = ''
        _q1052.stats = {'steps': 0, 'rows': 0, 'units': {}, 'emergency': 0, 'emergency_units': 0, 'bridge_units': 0, 'anim_fail': 0, 'anim_fallback': 0, 'seed_urgent': 0, 'ms_sum': 0.0, 'ms_max': 0.0}
        _q1052._new_day(-1)

    def _new_day(_q1052, day):
        _q1052.day = day
        _q1052.anim_fail = {}
        _q1052.anim_fallback = set()
        _q1052.anim_issued = {}
        _q1052.prev_plant_tiles = None
        _q1052._new_plants = set()
        _q1052.unfunded = {}
        _q1052._w_buy0 = 0

    @staticmethod
    def plain(rows):
        return [list(_q857) for _, _q857 in rows]

    def note_sent(_q1052, orders):
        """Review fix: the caller reports the purchase orders it actually put into this step's list (after its own
        packing); animal buys it left out are not issued (no failed try next step, not in animal_buys)."""
        sent = {}
        for _q857 in orders or ():
            if isinstance(_q857, (list, tuple)) and len(_q857) >= 3 and (_q857[0] == 'BUY_ANIMAL'):
                sent[_q857[1]] = sent.get(_q857[1], 0) + int(_q857[2])
        _q674 = {}
        for a, (k, _q356) in _q1052.anim_issued.items():
            s = min(int(k), sent.get(a, 0))
            if s > 0:
                _q674[a] = (s, _q356)
        _q1052.anim_issued = _q674
        _q1052.animal_buys = {a: k for a, (k, _) in _q674.items()}

    def keep_over(_q1052, _q993):
        """Extra shed WHEAT to hold on top of a market controller's own WHEAT reserve (e.g. pd_market.wheat_reserve of
        wheat_ctl) so that the margin / bridge stock bought here is not sold back: max(0, w_keep - reserve_w)."""
        return max(0, int(_q1052.w_keep) - int(_q993 or 0))

    @staticmethod
    def pack(rows, k):
        """Merge rows of the same (op, item) (most urgent priority, summed units) until at most k rows remain; then drop
        the least urgent rows."""
        rows = [(_q888, list(_q857)) for _q888, _q857 in rows]
        if len(rows) <= k:
            return rows
        _q773 = {}
        _q873 = []
        for _q888, _q857 in rows:
            key = (_q857[0], _q857[1])
            if key in _q773:
                q, _q860 = _q773[key]
                _q860[2] = int(_q860[2]) + int(_q857[2])
                _q773[key] = (min(q, _q888), _q860)
            else:
                _q773[key] = (_q888, _q857)
                _q873.append(key)
        _q880 = sorted((_q773[key] for key in _q873), key=lambda _q970: _q970[0])
        return _q880[:max(0, k)]

    def step(_q1052, S, ex, _q569, hour, day, pending=None):
        t0 = time.perf_counter()
        if day != _q1052.day:
            _q1052._new_day(day)
        cfg = _q1052.cfg
        _q1052.failed_parts = set()
        _q319 = {}
        _q914 = _norm_pending(pending)
        try:
            A = after_units(S, _q569 or [])
        except Exception as _q520:
            _q1052._err('after_units', _q520)
            A = {'shed': dict(S.shed), 'seeds': dict(S.seeds), 'inv': [dict(_q652) for _q652 in S.inventories], 'planted': {}, 'blocked': set(), 'fed': set()}
        try:
            _q453, _q462 = scan_chains(ex)
        except Exception as _q520:
            _q1052._err('scan_chains', _q520)
            _q453, _q462 = ({}, {})
        H = max(24 - hour, int(cfg['anim_h']), max(cfg['seed_h'].values()), int(cfg['carrot_block'][1]))
        try:
            ops = _route_ops(ex, H)
        except Exception as _q520:
            ops = []
            _q1052._err('route_ops', _q520)
        _q1017 = set((xy for _, _, xy, _, _ in ops))
        _q1052.last = {'hour': hour, 'day': day}
        _q471 = set()
        for xy, _q753 in _q462.items():
            for op, arg in _q753:
                if op == 'PLANT':
                    _q471.add((xy, arg))
        _q840 = set()
        if _q1052.prev_plant_tiles is not None and hour > 0:
            _q840 = _q471 - _q1052.prev_plant_tiles
        _q1052.prev_plant_tiles = _q471
        _q1052._new_plants = _q840
        for _q900, _q581 in (('wheat', _q1052._wheat), ('seeds', _q1052._seeds), ('animals', _q1052._animals), ('fert', _q1052._fert)):
            if not cfg.get(_q900 if _q900 != 'fert' else 'fert_buy') or _q900 in _q1052.hold:
                continue
            try:
                _q581(S, ex, A, _q453, _q462, ops, _q1017, hour, day, _q914, _q319)
            except Exception as _q520:
                _q1052.failed_parts.add(_q900)
                _q1052._err(_q900, _q520)
        room = max(0, int(getattr(S, 'shed_capacity', 100) or 100) - sum(A['shed'].values()) - sum((q for (op, _), q in _q914.items() if op in ('BUY_PRODUCT', 'BUY_ANIMAL'))))
        for key in sorted(_q319, key=lambda k: (k[0],) + _q1052._sub(k[1], k[2])):
            if key[1] in ('BUY_PRODUCT', 'BUY_ANIMAL'):
                q = min(_q319[key], room)
                room -= q
                _q319[key] = q
        _q1052.anim_issued = {}
        for (_q888, op, _q675), q in _q319.items():
            if op == 'BUY_ANIMAL' and q > 0:
                _q689, _ = _q1052.anim_issued.get(_q675, (0, 0))
                _q1052.anim_issued[_q675] = (_q689 + q, _q1052._owned(S, _q675))
        _q1052.animal_buys = {a: k for a, (k, _) in _q1052.anim_issued.items()}
        rows = _q1052._rows(_q319)
        st = _q1052.stats
        st['steps'] += 1
        st['rows'] += len(rows)
        for _, _q857 in rows:
            k = _q857[1] if _q857[0] != 'BUY_SEED' else 'seed_' + _q857[1]
            st['units'][k] = st['units'].get(k, 0) + int(_q857[2])
        ms = 1000.0 * (time.perf_counter() - t0)
        st['ms_sum'] += ms
        if ms > st['ms_max']:
            st['ms_max'] = round(ms, 3)
        return rows

    def _err(_q1052, _q900, _q520):
        _q1052.errors += 1
        _q1052.last_error = ('%s %s' % (_q900, repr(_q520)))[:240]

    def _add(_q1052, _q319, _q949, op, item, q):
        q = int(q)
        if q > 0:
            _q319[_q949, op, item] = _q319.get((_q949, op, item), 0) + q

    def _sub(_q1052, op, item):
        """Row order inside a priority: WHEAT, FERTILIZER, seeds (dear first), animals (cfg animal_order)."""
        if op == 'BUY_PRODUCT':
            return (0, 0 if item == 'WHEAT' else 1)
        if op == 'BUY_SEED':
            return (1, SEED_ORDER.index(item) if item in SEED_ORDER else 9)
        _q873 = tuple(_q1052.cfg.get('animal_order') or ANIMAL_ORDER)
        return (2, _q873.index(item) if item in _q873 else 9)

    def _rows(_q1052, _q319):
        _q1101 = _q1052._sub
        if _q1052.cfg.get('merge', True):
            m = {}
            for (_q888, op, _q675), q in _q319.items():
                if q <= 0:
                    continue
                if (op, _q675) in m:
                    _q889, _q961 = m[op, _q675]
                    m[op, _q675] = (min(_q889, _q888), _q961 + q)
                else:
                    m[op, _q675] = (_q888, q)
            items = [(_q888, op, _q675, q) for (op, _q675), (_q888, q) in m.items()]
        else:
            items = [(_q888, op, _q675, q) for (_q888, op, _q675), q in _q319.items() if q > 0]
        items.sort(key=lambda _q970: (_q970[0],) + _q1101(_q970[1], _q970[2]))
        return [(_q888, [op, _q675, int(q)]) for _q888, op, _q675, q in items]

    def _seeds(_q1052, S, ex, A, _q453, _q462, ops, _q1017, hour, day, _q914, _q319):
        cfg = _q1052.cfg
        _q383 = cfg['seed_buf']
        _q644 = cfg['seed_h']
        _q370, _q369, _q371 = cfg['carrot_block']
        _q514 = {}
        _q515 = {}
        _q516 = 0
        for _q1147, _q536, xy, op, arg in ops:
            if op != 'PLANT' or arg not in CROPS:
                continue
            if _q536 < int(_q644.get(arg, 2)):
                _q514[arg] = _q514.get(arg, 0) + 1
                if _q536 < 1:
                    _q515[arg] = _q515.get(arg, 0) + 1
            if arg == 'CARROT' and _q536 < _q369:
                _q516 += 1
        if cfg.get('new_chain_due'):
            for xy, arg in _q1052._new_plants:
                if xy not in _q1017 and arg in CROPS and (_tile(S, xy) != 'LOCKED'):
                    _q514[arg] = _q514.get(arg, 0) + 1
                    _q515[arg] = _q515.get(arg, 0) + 1
        seeds = A['seeds']
        _q723 = cfg['last_day']
        today = cfg.get('seed_today')
        _q916 = {}
        if today:
            for xy, _q753 in _q462.items():
                if _tile(S, xy) == 'LOCKED':
                    continue
                for op, arg in _q753:
                    if op == 'PLANT' and arg in CROPS:
                        _q916[arg] = _q916.get(arg, 0) + 1
        _q665 = {}
        for c in CROPS:
            _q475 = _q514.get(c, 0)
            _q915 = max(_q453.get(('PLANT', c), 0), _q475)
            b = int(_q383.get(c, 0))
            if c == 'CARROT' and _q516 >= _q371:
                b += int(_q370)
            _q733 = int(_q723.get(c, 27))
            if day <= _q733:
                _q881 = int(_q383.get(c, 0)) if day < _q733 else 0
                b = min(b, max(0, _q915 - _q475) + _q881)
            else:
                b = 0
            _q630 = int(seeds.get(c, 0)) + int(_q914.get(('BUY_SEED', c), 0))
            _q1120 = max(_q475 + b, _q916.get(c, 0)) if today else _q475 + b
            need = max(0, _q1120 - _q630)
            if need <= 0:
                continue
            _q1154 = min(need, max(0, _q515.get(c, 0) - _q630))
            if _q1154:
                _q1052.stats['seed_urgent'] += 1
            _q1052._add(_q319, P_DUE, 'BUY_SEED', c, _q1154)
            _q1117 = 0
            if today:
                _q1117 = min(need - _q1154, max(0, _q916.get(c, 0) - _q630 - _q1154))
                _q1052._add(_q319, P_TODAY, 'BUY_SEED', c, _q1117)
            _q1052._add(_q319, P_BUFFER, 'BUY_SEED', c, need - _q1154 - _q1117)
            _q665[c] = (_q475, b, _q630, need)
        _q1052.last['seeds'] = _q665

    def _wheat_walk(_q1052, S, A, _q462, ops, _q1017):
        """(short, crit_short, spare, credit_used, feeds_routed) over the routes + the unrouted FEEDs."""
        cfg = _q1052.cfg
        inv = A['inv']
        _q917 = {}
        _q589 = {}
        for _q1147, _q536, xy, op, arg in ops:
            if op in ('FEED', 'HARVEST'):
                _q917.setdefault(_q1147, []).append((_q536, op, xy))
                if op == 'FEED':
                    _q589[xy] = _q589.get(xy, 0) + 1
        short = crit = spare = credit = 0
        for _q1147, _q753 in _q917.items():
            _q753.sort(key=lambda _q970: _q970[0])
            _q350 = int(inv[_q1147].get('WHEAT', 0)) if _q1147 < len(inv) else 0
            for _q536, op, xy in _q753:
                if op == 'HARVEST':
                    if not cfg['credit']:
                        continue
                    _q458 = S.crops.get(xy)
                    if _q458 is not None and _q458.crop == 'WHEAT' and (_q458.units > 0) and (_q458.age >= CROPS['WHEAT']['fyd']):
                        _q350 += max(0, _q458.units - 1)
                        credit += max(0, _q458.units - 1)
                    continue
                if _q350 > 0:
                    _q350 -= 1
                else:
                    short += 1
                    _q336 = S.animals.get(xy)
                    if _q336 is not None and _q336.must_feed:
                        crit += 1
            spare += _q350
        for _q1147 in range(len(inv)):
            if _q1147 not in _q917:
                spare += int(inv[_q1147].get('WHEAT', 0))
        pool = 0
        for xy, _q753 in _q462.items():
            _q843 = sum((1 for op, _ in _q753 if op == 'FEED')) - _q589.get(xy, 0)
            if _q843 > 0:
                pool += _q843
                _q336 = S.animals.get(xy)
                if _q336 is not None and _q336.must_feed:
                    crit += _q843
        return (short + pool, crit, spare, credit, pool)

    def _wheat(_q1052, S, ex, A, _q453, _q462, ops, _q1017, hour, day, _q914, _q319):
        cfg = _q1052.cfg
        if day >= FINAL_DAY:
            _q1052.w_keep = 0
            _q1052.last['wheat'] = None
            return
        short, crit, spare, credit, pool = _q1052._wheat_walk(S, A, _q462, ops, _q1017)
        F = _q453.get(('FEED', None), 0)
        if not _q462 and F:
            carried = sum((int(_q652.get('WHEAT', 0)) for _q652 in A['inv']))
            short, spare = (F, carried)
        sh = int(A['shed'].get('WHEAT', 0))
        pw = int(_q914.get(('BUY_PRODUCT', 'WHEAT'), 0))
        _q1100 = float(cfg['spare_use'])
        need_rem = max(0, int(math.ceil(short - _q1100 * spare - 1e-09)))
        margin = int(cfg['wheat_margin'])
        _q384 = _q385 = 0
        _q996 = bool(cfg.get('wheat_retry')) and _q1052._w_buy0 > 0 and (hour not in cfg['wheat_hours']) and (hour <= int(cfg['emergency_last_h']))
        if hour in cfg['wheat_hours'] or cfg.get('topup_any_hour') or _q996:
            if sh - need_rem <= int(cfg['wheat_surplus_max']):
                _q487 = max(0, need_rem - sh - pw)
                _q384 = _q487
                if hour in cfg['wheat_hours'] and (_q487 > 0 or hour not in cfg['margin_if_short_hours']):
                    _q385 = max(0, need_rem + margin - sh - pw) - _q487
        _q528 = 0
        if cfg['emergency'] and crit > 0 and (hour <= int(cfg['emergency_last_h'])):
            _q454 = sh + pw + int(_q1100 * spare)
            if crit > _q454:
                _q528 = crit - _q454 + int(cfg['emergency_margin'])
                if _q528 > _q384:
                    _q1052.stats['emergency'] += 1
                    _q1052.stats['emergency_units'] += _q528 - _q384
                    _q385 = max(0, _q385 - (_q528 - _q384))
                    _q384 = _q528
        bridge = 0
        _q355 = cfg.get('bridge_day')
        if _q355 is not None and day == int(_q355) and (hour in cfg['bridge_hours']):
            _q478 = day + int(cfg['bridge_days']) - 1
            _q810 = len(S.animals) + _q453.get(('PLACE', 'GOOSE'), 0) + _q453.get(('PLACE', 'COW'), 0) + _q453.get(('PLACE', 'SHEEP'), 0)
            _q832 = F + float(cfg['bridge_rate']) * _q810 * (_q478 - day)
            carried = sum((int(_q652.get('WHEAT', 0)) for _q652 in A['inv']))
            _q883 = sum((wheat_by(_q458, day, _q478) for _q458 in S.crops.values()))
            _q631 = sh + carried + _q883 + pw + _q384 + _q385
            bridge = max(0, int(math.ceil(_q832 - _q631 - 1e-09)))
            _q1052.stats['bridge_units'] += bridge
        _q1052._add(_q319, P_FEED, 'BUY_PRODUCT', 'WHEAT', _q384)
        _q1052._add(_q319, P_BUFFER, 'BUY_PRODUCT', 'WHEAT', _q385)
        _q1052._add(_q319, P_BRIDGE, 'BUY_PRODUCT', 'WHEAT', bridge)
        _q1052._w_buy0 = _q384
        _q1052.w_keep = need_rem + margin + (bridge if bridge else 0)
        _q1052.last['wheat'] = {'feeds': F, 'short': short, 'crit': crit, 'spare': spare, 'credit': credit, 'pool': pool, 'need_rem': need_rem, 'shed': sh, 'buy': _q384 + _q385, 'emergency': _q528, 'bridge': bridge}

    @staticmethod
    def _owned(S, a):
        n = sum((1 for _q336 in S.animals.values() if _q336.animal == a)) + int(S.shed.get(a, 0))
        for inv in S.inventories:
            n += int(inv.get(a, 0) or 0)
        return n

    def _animals(_q1052, S, ex, A, _q453, _q462, ops, _q1017, hour, day, _q914, _q319):
        cfg = _q1052.cfg
        for a, (k, _q356) in _q1052.anim_issued.items():
            if _q1052._owned(S, a) < _q356 + k:
                _q1052.anim_fail[a] = _q1052.anim_fail.get(a, 0) + 1
                _q1052.stats['anim_fail'] += 1
                if _q1052.anim_fail[a] >= int(cfg['anim_fail_max']) and a not in _q1052.anim_fallback:
                    _q1052.anim_fallback.add(a)
                    _q1052.stats['anim_fallback'] += 1
        H = int(cfg['anim_h'])
        _q537 = {}
        for _q1147, _q536, xy, op, arg in ops:
            if op == 'PLACE' or op in BUILD_OPS:
                if xy not in _q537 or _q536 < _q537[xy]:
                    _q537[xy] = _q536
        _q1168 = {}
        if _q462:
            for xy, _q753 in _q462.items():
                for op, arg in _q753:
                    if op == 'PLACE' and arg in ANIMALS:
                        _q1168.setdefault(arg, []).append(xy)
        else:
            for (op, arg), n in _q453.items():
                if op == 'PLACE' and arg in ANIMALS:
                    _q1168.setdefault(arg, []).extend([None] * n)
        inv = A['inv']
        _q665 = {}
        for a, tiles in _q1168.items():
            _q630 = int(A['shed'].get(a, 0)) + sum((int(_q652.get(a, 0)) for _q652 in inv)) + int(_q914.get(('BUY_ANIMAL', a), 0))
            _q734 = _q617 = pool = 0
            for xy in tiles:
                if xy is None:
                    pool += 1
                    continue
                if _tile(S, xy) == 'LOCKED':
                    continue
                if xy in _q537:
                    if _q537[xy] < H:
                        _q734 += 1
                    else:
                        _q617 += 1
                else:
                    pool += 1
            if a in _q1052.unfunded or hour > int(cfg['anim_last_h']):
                continue
            if a in _q1052.anim_fallback:
                if hour > int(cfg['anim_retry_h']):
                    _q737 = max(0, _q734 + _q617 + pool - _q630)
                    if _q737:
                        _q1052.unfunded[a] = _q737
                    continue
                _q989 = _q734 + _q617 + pool
            else:
                _q989 = _q734 + min(_q617, max(0, _q630 - _q734))
                if hour >= int(cfg['anim_pool_hour']):
                    _q989 += pool
            buy = max(0, _q989 - _q630)
            _q633 = cfg.get('herd_cap')
            if _q633 and _q633.get(a) is not None:
                buy = min(buy, max(0, int(_q633[a]) - _q1052._owned(S, a) - int(_q914.get(('BUY_ANIMAL', a), 0))))
            _q665[a] = (_q734, _q617, pool, _q630, buy)
            if buy:
                _q1052._add(_q319, P_ANIMAL, 'BUY_ANIMAL', a, buy)
        _q1052.last['animals'] = _q665

    def _fert(_q1052, S, ex, A, _q453, _q462, ops, _q1017, hour, day, _q914, _q319):
        cfg = _q1052.cfg
        if cfg.get('fert_buy') != 'chain' or day >= FINAL_DAY:
            return
        h0, h1 = cfg['fert_hours']
        if not h0 <= hour <= h1:
            return
        _q547 = _q453.get(('FERTILIZE', None), 0)
        if _q547 <= 0:
            return
        _q443 = _q453.get(('COLLECT_FERTILIZER', None), 0)
        _q555 = sum((int(_q652.get('FERTILIZER', 0)) for _q652 in A['inv']))
        _q594 = int(A['shed'].get('FERTILIZER', 0))
        short = _q547 - _q594 - _q555 - float(cfg['collect_eff']) * _q443 - int(_q914.get(('BUY_PRODUCT', 'FERTILIZER'), 0))
        q = float(S.prices.get('FERTILIZER', 999) or 999)
        _q410 = float(cfg['fert_q0'] if hour <= 2 else cfg['fert_q'])
        k = int(math.ceil(short - 1e-09))
        _q589 = _q1052.fert_req
        if _q589 is not None and _q589[0] == day and (q <= _q410):
            k = max(k, int(_q589[1]) - int(_q914.get(('BUY_PRODUCT', 'FERTILIZER'), 0)))
            _q1052.fert_req = None
        if k > 0 and q <= _q410:
            _q1052._add(_q319, P_BUFFER, 'BUY_PRODUCT', 'FERTILIZER', k)
            _q1052.last['fert'] = (_q547, _q443, _q594, _q555, k)

class Fert:
    """Fertiliser allocator (design 6.7): the day's FERTILIZE ops within the fertiliser we have, the surplus sold at
    hours 0-2 by the price rule.  One instance per seat."""

    def __init__(_q1052, cfg=None):
        _q1052.cfg = dict(FERT_CFG)
        if cfg:
            _q1052.cfg.update(cfg)
        _q1052.day = -1
        _q1052.buy_req = 0
        _q1052.kept_ops = 0
        _q1052.collections = 0
        _q1052.hoard = 0
        _q1052.to_sell = 0
        _q1052.sell_day = None
        _q1052.last = {}
        _q1052.errors = 0
        _q1052.last_error = ''
        _q1052.stats = {'days': 0, 'kept': 0, 'cut': 0, 'cut_value': 0, 'sold': 0, 'ms_max': 0.0}

    def value(_q1052, S, xy):
        """$ value of one FERTILIZE on tile xy today: marginal units (pd_tasks) x the crop's unit value (0: no crop)."""
        _q458 = S.crops.get(xy)
        if _q458 is None:
            return 0.0
        try:
            m = _PT._fert_marginal(_q458, S.day)
        except Exception:
            m = 0.0
        _q1158 = (_q1052.cfg.get('unit_value') or {}).get(_q458.crop)
        if _q1158 is None:
            _q1158 = float(S.prices.get(_q458.crop, 0) or 0)
        return float(m) * float(_q1158)

    def plan_day(_q1052, S, chains, _q444=None):
        """chains {(x, y) or tile index: [(op, arg)]} -> a new chains dict whose FERTILIZE ops are the best ones within
        the budget (the input is not mutated).  collections_today: today's COLLECT_FERTILIZER ops (None: counted in
        chains)."""
        t0 = time.perf_counter()
        cfg = _q1052.cfg
        _q1052.day = S.day
        if _q444 is None:
            _q444 = sum((1 for _q753 in chains.values() for _q857 in _q753 if _q857[0] == 'COLLECT_FERTILIZER'))
        _q443 = int(_q444)
        shed_f = int(S.shed.get('FERTILIZER', 0))
        _q412 = sum((int(_q652.get('FERTILIZER', 0) or 0) for _q652 in S.inventories))
        supply = shed_f + _q412 + float(cfg['collect_eff']) * _q443
        _q1156 = supply * (1.0 - float(cfg['sell_share']))
        if cfg.get('max_use') is not None:
            _q1156 = min(_q1156, float(cfg['max_use']))
        q = float(S.prices.get('FERTILIZER', 100) or 100)
        thr = float(cfg['min_ratio']) * q + float(cfg['rival_add'])
        _q402 = []
        for t, _q753 in chains.items():
            xy = _xy(t)
            n = sum((1 for _q857 in _q753 if _q857[0] == 'FERTILIZE'))
            if n:
                _q1159 = _q1052.value(S, xy)
                for _q652 in range(n):
                    _q402.append((-_q1159, xy[1], xy[0], _q652, t, _q1159))
        _q402.sort()
        _q1052.buy_req = 0
        _q393 = cfg.get('buy_extra')
        if _q393 and q <= float(_q393.get('q', 35.0)):
            _q811 = sum((1 for _q396 in _q402 if _q396[5] >= thr and _q396[5] > 0))
            _q798 = int(_q1156 + 1e-09)
            _q543 = [_q396 for _q396 in _q402[_q798:] if _q396[5] >= q + float(_q393.get('margin', 2.0)) and _q396[5] >= thr and (_q396[5] > 0)]
            _q693 = min(int(_q393.get('cap', 12)), len(_q543), max(0, _q811 - _q798))
            if _q693 > 0:
                _q1156 += _q693
                _q1052.buy_req = _q693
        kept = {}
        _q806 = 0
        _q472 = 0.0
        cut = []
        for _q836, _, _, _q652, t, _q1159 in _q402:
            if _q806 + 1 <= _q1156 + 1e-09 and _q1159 >= thr and (_q1159 > 0):
                kept[t] = kept.get(t, 0) + 1
                _q806 += 1
            else:
                cut.append((_xy(t), round(_q1159, 1)))
                _q472 += _q1159
        _q880 = {}
        for t, _q753 in chains.items():
            k = kept.get(t, 0)
            new = []
            for _q857 in _q753:
                if _q857[0] == 'FERTILIZE':
                    if k <= 0:
                        continue
                    k -= 1
                new.append(tuple(_q857))
            if new:
                _q880[t] = new
        _q1052.kept_ops = _q806
        _q1052.collections = _q443
        _q1052.hoard = 0
        st = _q1052.stats
        st['days'] += 1
        st['kept'] += _q806
        st['cut'] += len(cut)
        st['cut_value'] += int(_q472)
        _q1052.last = {'supply': round(supply, 2), 'use_budget': round(_q1156, 2), 'thr': round(thr, 1), 'kept': _q806, 'cut': cut, 'collections': _q443, 'shed': shed_f, 'carried': _q412, 'buy_req': _q1052.buy_req}
        ms = 1000.0 * (time.perf_counter() - t0)
        if ms > st['ms_max']:
            st['ms_max'] = round(ms, 3)
        return _q880

    def keep_level(_q1052, kept_ops, collections=None):
        """Shed fertiliser needed for the kept ops beyond what the collections will bring (sale keep)."""
        _q443 = _q1052.collections if collections is None else int(collections)
        return max(0, int(math.ceil(int(kept_ops) - float(_q1052.cfg['keep_collect']) * _q443 - 1e-09)))

    def reserve(_q1052, kept_ops, collections=None):
        """FERTILIZER units the market's other sale rows (and the room guard's protected level) must keep: the sale keep
        plus the hoard the price rule retained today."""
        return _q1052.keep_level(kept_ops, collections) + int(_q1052.hoard)

    def unsold(_q1052, k):
        """Review fix: k units of this hour's sell_orders rows did not make the market list (order window): they go
        back to to_sell (sold at the next sale hour as decided) instead of being re-classified as new stock, which in
        the $15-30 band halved them again into the hoard at every dropped hour."""
        k = int(k)
        if k > 0 and getattr(_q1052, 'sell_day', None) is not None:
            _q1052.to_sell += k
            _q1052.stats['sold'] -= k

    def sell_orders(_q1052, S, hour, quote=None, kept_ops=None, collections=None, shed_f=None):
        """[['SELL', 'FERTILIZER', n <= row_max], ...] (at most rows_max rows): hours 0-2 of days < 29, the shed
        fertiliser above keep_level by the price rule; day 29: everything in one row.  kept_ops = FERTILIZE ops still
        pending (default: today's kept count), collections = COLLECT ops still pending (default: today's), shed_f = the
        shed fertiliser at market time (default: S.shed)."""
        cfg = _q1052.cfg
        if getattr(_q1052, 'sell_day', None) != S.day:
            _q1052.sell_day = S.day
            _q1052.hoard = 0
            _q1052.to_sell = 0
        _q594 = int(S.shed.get('FERTILIZER', 0)) if shed_f is None else int(shed_f)
        if _q594 <= 0:
            _q1052.hoard = _q1052.to_sell = 0
            return []
        if S.day >= FINAL_DAY:
            _q1052.stats['sold'] += _q594
            return [['SELL', 'FERTILIZER', _q594]]
        if hour not in cfg['sell_hours']:
            return []
        q = float(S.prices.get('FERTILIZER', 0) if quote is None else quote)
        keep = _q1052.keep_level(_q1052.kept_ops if kept_ops is None else kept_ops, collections)
        if q >= float(cfg['hi']) and _q1052.hoard:
            _q1052.to_sell += _q1052.hoard
            _q1052.hoard = 0
        new = _q594 - keep - _q1052.hoard - _q1052.to_sell
        if new < 0:
            _q475 = min(-new, _q1052.to_sell)
            _q1052.to_sell -= _q475
            _q1052.hoard = max(0, _q1052.hoard - (-new - _q475))
        elif new > 0:
            if q >= float(cfg['hi']):
                _q699 = new
            elif q >= float(cfg['lo']):
                _q699 = max(int(math.ceil(new / 2.0)), new - max(0, int(cfg['hoard_max']) - _q1052.hoard))
            else:
                _q699 = max(0, new - max(0, int(cfg['hoard_low_max']) - _q1052.hoard))
            _q1052.hoard += new - _q699
            _q1052.to_sell += _q699
        k = min(_q1052.to_sell, int(cfg['row_max']) * int(cfg['rows_max']))
        _q1052.to_sell -= k
        if k <= 0:
            return []
        _q880 = []
        _q737 = k
        while _q737 > 0:
            n = min(_q737, int(cfg['row_max']))
            _q880.append(['SELL', 'FERTILIZER', n])
            _q737 -= n
        _q1052.stats['sold'] += k
        return _q880