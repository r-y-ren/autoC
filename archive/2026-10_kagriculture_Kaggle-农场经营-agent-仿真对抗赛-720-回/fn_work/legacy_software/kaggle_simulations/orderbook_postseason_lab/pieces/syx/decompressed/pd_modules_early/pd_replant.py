"""PD - Replanter (C6), Labour controller (C8) and day Ledger (C13 telemetry) of the CS coordinated planner.
Original work, Shawn404, 27 Sep 2026.  Pure Python, no engine import, no file access.

Spec: results/portable/sys_design.txt sections 6.4 (C6), 6.6 (C8), 6.11 (C13) and 10 (fallbacks).
Report and exact API: results/portable/cs_build_B4.txt.  Tests: tools/tmp/cs_b4_test.py.

Executor API (tools/pd/pd_exec.py, task B5), used only through these names:
  ex.route_ops(H) -> [(unit, eta_turns, (x, y), op, arg)]  ops that start within H turns
  ex.slack()      -> {unit: free_turns}                     cap - delay - dur per route
  ex.add_chain((x, y), [(op, arg), ...])                    adds a job to today's chains / pool
  ex.pending_ops() -> {op: count}                           ops still in the chains
  ex.chains (read only here: {tile y*10+x: [(op, arg)]}) tells which tiles hold a job.
If a method is missing (an executor built before B5), the module falls back to the executor's own records (routes /
cap / delay) and to the _pd_fill plumbing (ex.chains[t] = chain; ex.pool.add(t) when the tile has no route).

Replanter.step(S, ex, plan_state, hour, day, acts=None) -> [((x, y), chain)]
  Runs at hours 1-21 on days <= 27, after the unit guards, on the step's FINAL commands (acts; with acts=None it sees
  only what the observation shows, i.e. a tile freed this step one step later).  Candidate tiles are owned tiles that
  are empty / weedy / a spent plant after this step's commands and hold no chain (a tile gets at most one Replanter
  chain a day, so nothing is ever double-booked).  Three sources, in this order:
    land   a tile that was LOCKED at hour 0 (a quadrant bought during the day) -> [PLANT WHEAT, WATER] up to
           land_last_h 19 (the S4 _pd_land_fill behaviour, absorbed; no slack test, like S4; later such a tile is an
           ordinary fill candidate);
    freed  a tile that was NOT free at hour 0 (harvested / dug / spent during the day, or by this step's commands) ->
           [DIG if weed / spent] PLANT c, WATER at once - the unit that freed it usually stands on it;
    fill   from fill_h[0] (12): tiles free since hour 0 that the plan left empty (and freed tiles not taken) when the
           units' route slack allows: units with slack >= fill_turns (3) each; at most floor(total slack / 3) jobs;
           each job charged max(3, travel from the unit's route end + service) against that unit's slack; nearest
           tiles to the units with slack first; not while jobs wait in the executor pool and no unit PASSes this step
           (fill_pool_block 'tight': jobs that wait while units idle are supply-blocked, not labour-blocked).
  Crop c (freed and fill): the first crop of quota_order (S, T, C) with today's quota remainder left and inside its
  window (S <= 15, T <= 18, C <= 27); else WHEAT while standing wheat tonight < W* + 4; else CARROT on days 20-27;
  else WHEAT.  Quota remainders are decremented as they are used.  It never checks seeds: the PLANT is published to
  the executor, the supply controller (C7) buys the seed, the seed guard holds the op until it arrives
  (seed_shortfall() gives the fallback buy list while C7 is not built).
  make_plan_state(S, plan) (= Replanter.begin_day) builds the plan state at hour 0: W* (plan['wheat']['wstar'] in
  wheat_first mode, else the same W* formula), the quota remainder per crop (plan['targets'][y] quota - today), the
  tiles free and locked at hour 0, and the day's addition log.

Labour.hires(S, chains, ledger, day, tasks=None, n_l3=None) -> (n_h0, n_h1), or None = not decided here
  hands = clamp(ceil((ops x TPT - 24) / 22.3), 8, 12);  ops = today's chain ops at hour 0 + yesterday's Replanter jobs
  x 3;  TPT = EMA of the Ledger's realised busy turns per effective op (start 1.95; days >= 10 with >= 40 effective
  ops).  Feedback from yesterday's Ledger day: +1 (cap 12) if missed chain ops at hour 23 > 6 or the pool held jobs on
  >= 4 steps from hour 12; else -1 if PASS unit-turns at hours 5-23 > 15 and the pool was empty on every step from hour
  12 (add_tight True: only pool steps on which no unit PASSed, and missed ops only after a busy evening).  The result
  stays inside [8, 12] (fb_below_lo False) and never below the must-do floor ceil(level-3 ops x 1.95 / 22.3).  Orders: min(hands, 8) HIRE at hour 0, the rest at hour 1.  None on days outside 10-28 (day 29 keeps
  _PD_D29_HIRES; day 9 keeps the land-day path) and on an internal error (fallback: the ladder / HIRE_FLEX path).

Ledger: per-day telemetry from each step's final commands (C13).  step(S, acts, pool_n=None, pending=None,
  rp_added=None) classifies the commands exactly like tools/tmp/sys_audit_lib.classify_turn (effective = the engine
  would change state) and accumulates unit-turns, PASS by hour, busy turns, effective ops by op, plantings by hour,
  seed-blocked PLANTs, pool occupancy from hour 12, missed chain ops at hour 23 (pending = ex.pending_ops() after the
  hour-23 act) and Replanter additions.  derived(day) gives the C8 inputs (tpt, pass_h5_23, pool_empty_h12,
  pool_steps_h12, missed, rp_jobs).
Every public entry catches its own exceptions (design section 10): Replanter -> no chain edits this step; Labour ->
None; Ledger -> the step is skipped (counted in .errors).
"""
import math
import time
B = 10
BUILD_OPS = ('BUILD_COOP', 'BUILD_PASTURE')
MOVES = ('NORTH', 'SOUTH', 'EAST', 'WEST')
ANIMALS = ('GOOSE', 'COW', 'SHEEP')
STRUCT = {'GOOSE': 'COOP', 'COW': 'PASTURE', 'SHEEP': 'PASTURE'}
FYD = {'WHEAT': 2, 'CARROT': 2, 'TOMATO': 8, 'STRAWBERRY': 10, 'MELON': 10}
ONGOING = {'WHEAT': False, 'CARROT': False, 'TOMATO': True, 'STRAWBERRY': True, 'MELON': False}
TILE_OPS = ('PLANT', 'WATER', 'HARVEST', 'FERTILIZE', 'FEED', 'CARE', 'COLLECT_FERTILIZER', 'DIG', 'BUILD_PASTURE', 'BUILD_COOP')
Q_KEY = {'STRAWBERRY': 'S', 'TOMATO': 'T', 'CARROT': 'C'}
FREE_ST = ('empty', 'weed', 'spent')
RP_CFG = {'hours': (1, 21), 'last_day': 27, 'windows': {'STRAWBERRY': 15, 'TOMATO': 18, 'CARROT': 27}, 'quota_order': ('STRAWBERRY', 'TOMATO', 'CARROT'), 'w_margin': 4, 'carrot_days': (20, 27), 'wstar': (1.2, 0.2, 0.3), 'wstar_last': 27, 'freed': True, 'freed_need_slack': False, 'fill': True, 'fill_h': (12, 21), 'fill_turns': 3, 'fill_charge_travel': True, 'fill_pool_block': 'tight', 'fill_cands': 24, 'land': True, 'land_last_h': 19, 'land_crop': 'WHEAT', 'max_per_step': 25, 'max_per_tile': 1, 'predict': True, 'explicit_dig': True}
LAB_CFG = {'days': (10, 28), 'tpt0': 1.95, 'ema': True, 'alpha': 0.25, 'ema_from_day': 10, 'min_eff': 40, 'tpt_lo': 1.6, 'tpt_hi': 2.6, 'far': 24.0, 'hand': 22.3, 'lo': 8, 'hi': 12, 'rp_ops': 3.0, 'fb': True, 'cut_pass': 15, 'cut_h': (5, 23), 'pool_h': 12, 'add_missed': 6, 'add_pool_steps': 4, 'add_tight': False, 'fb_below_lo': False, 'floor_tpt': 1.95, 'h0_max': 8}
LEDGER_CFG = {'pool_h': 12, 'missed_skip': ()}

def _xy(k):
    """Tile key (int y*10+x or (x, y)) -> (x, y)."""
    if isinstance(k, int):
        return (k % B, k // B)
    return (int(k[0]), int(k[1]))

def _dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def _chains(ex):
    _q428 = getattr(ex, 'chains', None)
    return _q428 if isinstance(_q428, dict) else {}

def _pool_n(ex):
    try:
        return len(getattr(ex, 'pool', ()) or ())
    except TypeError:
        return 0

def ex_slack(ex):
    """{unit: free turns}: ex.slack(), else cap - delay - dur of the executor's own routes (present units)."""
    f = getattr(ex, 'slack', None)
    if callable(f):
        return {int(_q1147): float(_q1159) for _q1147, _q1159 in (f() or {}).items()}
    routes = getattr(ex, 'routes', None)
    cap = getattr(ex, 'cap', None)
    if not routes or cap is None:
        return {}
    _q498 = getattr(ex, 'delay', None) or []
    n = int(getattr(ex, 'n_units', len(routes)) or 0)
    return {_q1147: float(cap - (_q498[_q1147] if _q1147 < len(_q498) else 0) - _q970.dur) for _q1147, _q970 in enumerate(routes[:n])}

def ex_route_ends(ex, H):
    """{unit: (x, y)} the tile of each unit's last op within H turns: ex.route_ops(H), else the last route tile."""
    f = getattr(ex, 'route_ops', None)
    _q880 = {}
    if callable(f):
        best = {}
        for _q1018 in f(H) or ():
            _q1147, _q536, xy = (_q1018[0], _q1018[1], _q1018[2])
            if _q1147 not in best or _q536 >= best[_q1147]:
                best[_q1147] = _q536
                _q880[_q1147] = _xy(xy)
        return _q880
    for _q1147, _q970 in enumerate(getattr(ex, 'routes', None) or ()):
        tl = getattr(_q970, 'tl', None)
        if tl:
            _q880[_q1147] = _xy(tl[-1])
    return _q880

def ex_add_chain(ex, xy, chain):
    """ex.add_chain(xy, chain), else the _pd_fill plumbing."""
    f = getattr(ex, 'add_chain', None)
    if callable(f):
        f(xy, list(chain))
        return
    t = xy[1] * B + xy[0]
    ex.chains[t] = [tuple(_q857) for _q857 in chain]
    if t not in (getattr(ex, 'where', None) or {}):
        ex.pool.add(t)

def ex_pending_ops(ex):
    """{op: count} of the ops still in the chains: ex.pending_ops(), else counted from ex.chains."""
    f = getattr(ex, 'pending_ops', None)
    if callable(f):
        return dict(f() or {})
    _q880 = {}
    for _q428 in _chains(ex).values():
        for _q857 in _q428:
            _q880[_q857[0]] = _q880.get(_q857[0], 0) + 1
    return _q880

def pending_plants(ex):
    """{crop: PLANT ops still in the chains}."""
    _q880 = {}
    for _q428 in _chains(ex).values():
        for _q857 in _q428:
            if _q857[0] == 'PLANT' and len(_q857) > 1 and _q857[1]:
                _q880[_q857[1]] = _q880.get(_q857[1], 0) + 1
    return _q880

def seed_shortfall(S, ex):
    """{crop: seeds to buy}: PLANT ops in the chains beyond the seeds held (the fallback buy list while C7 is off)."""
    _q880 = {}
    for c, n in pending_plants(ex).items():
        k = n - int(S.seeds.get(c, 0))
        if k > 0:
            _q880[c] = k
    return _q880

def _base_state(S, xy):
    """'empty' | 'weed' | 'spent' | 'crop' | 'animal' | 'struct' | 'locked' of the observed tile."""
    t = S.tiles[xy[1]][xy[0]]
    if t is None:
        return 'empty'
    if not isinstance(t, dict):
        return 'locked'
    k = t.get('kind')
    if k == 'WEED':
        return 'weed'
    if k == 'PLANT':
        _q458 = S.crops.get(xy)
        return 'spent' if _q458 is not None and _q458.spent else 'crop'
    if t.get('animal'):
        return 'animal'
    return 'struct'

def predict_tiles(S, acts, planted=None):
    """{(x, y): state} of the tiles this step's final commands change (units in engine order): HARVEST of a ripe
    non-ongoing crop -> 'empty'; HARVEST of an ongoing crop with no production left -> 'spent'; DIG -> 'empty';
    PLANT / BUILD on an empty tile -> 'crop' / 'struct' (a seed-blocked PLANT keeps its chain, so the tile is taken
    either way).  planted (optional dict) receives {(x, y): crop} of this step's PLANTs."""
    _q944 = {}
    if not acts:
        return _q944
    units = S.units
    for _q1147, a in enumerate(acts):
        if _q1147 >= len(units) or not a or (not isinstance(a, (list, tuple))):
            continue
        op = a[0]
        if op not in ('HARVEST', 'DIG', 'PLANT') and op not in BUILD_OPS:
            continue
        xy = (int(units[_q1147][0]), int(units[_q1147][1]))
        _q467 = _q944.get(xy)
        if _q467 is None:
            _q467 = _base_state(S, xy)
        if _q467 == 'locked':
            continue
        if op == 'HARVEST':
            if xy in _q944 or _q467 != 'crop':
                continue
            _q458 = S.crops.get(xy)
            if _q458 is None or _q458.units <= 0 or _q458.age < FYD.get(_q458.crop, 99):
                continue
            if not ONGOING.get(_q458.crop, False):
                _q944[xy] = 'empty'
            elif _q458.prods_left == 0:
                _q944[xy] = 'spent'
        elif op == 'DIG':
            if _q467 in ('weed', 'spent', 'crop', 'struct'):
                _q944[xy] = 'empty'
                if planted is not None:
                    planted.pop(xy, None)
        elif op == 'PLANT':
            if _q467 == 'empty':
                _q944[xy] = 'crop'
                if planted is not None and len(a) > 1:
                    planted[xy] = a[1]
        elif _q467 == 'empty':
            _q944[xy] = 'struct'
    return _q944

def wheat_tonight(S, chains, _q944=None, planted=None):
    """Standing wheat tonight: wheat on the board that no chain cuts without a replant and no command of this step
    removes, plus every chain whose last PLANT is WHEAT, plus this step's WHEAT PLANTs (planted, from predict_tiles:
    the executor pops a PLANT when it issues it, and the observation does not show the plant yet) unless the tile's
    chain still holds a PLANT (a seed-blocked op given back by the guard)."""
    _q944 = _q944 or {}
    planted = planted or {}
    n = 0
    for xy, crop in planted.items():
        if crop != 'WHEAT':
            continue
        _q428 = chains.get(xy[1] * B + xy[0])
        if _q428 is None:
            _q428 = chains.get(xy)
        if _q428 and any((_q857[0] in ('PLANT', 'DIG') for _q857 in _q428)):
            continue
        n += 1
    for xy, _q458 in S.crops.items():
        if _q458.crop != 'WHEAT' or xy in planted or _q944.get(xy) in FREE_ST:
            continue
        _q428 = chains.get(xy[1] * B + xy[0])
        if _q428 is None:
            _q428 = chains.get(xy)
        if _q428:
            ops = [_q857[0] for _q857 in _q428]
            if 'PLANT' in ops or 'DIG' in ops:
                continue
            if 'HARVEST' in ops and _q458.age >= FYD['WHEAT']:
                continue
        n += 1
    for _q428 in chains.values():
        _q723 = None
        for _q857 in _q428:
            if _q857[0] == 'PLANT':
                _q723 = _q857[1] if len(_q857) > 1 else None
        if _q723 == 'WHEAT':
            n += 1
    return n

def make_plan_state(S, plan=None, cfg=None):
    """Hour-0 plan state for the Replanter: W*, quota remainder per crop, tiles free / locked at hour 0, logs."""
    c = dict(RP_CFG)
    c.update(cfg or {})
    plan = plan or {}
    day = int(S.day)
    wh = plan.get('wheat') or {}
    wstar = wh.get('wstar')
    if wstar is None:
        owned = B * B - len(S.locked)
        _q813 = sum((1 for _q857 in plan.get('ops') or () if _q857 and _q857[0] == 'PLACE'))
        _q316, _q580, _q457 = c['wstar']
        if day <= int(c['wstar_last']):
            wstar = max(int(round(_q580 * owned)), min(int(round(_q457 * owned)), int(round(_q316 * (len(S.animals) + _q813)))))
        else:
            wstar = 0
    rem = {}
    _q1119 = plan.get('targets') or {}
    for crop, _q1197 in Q_KEY.items():
        t = _q1119.get(_q1197) or {}
        rem[crop] = max(0, int(t.get('quota', 0) or 0) - int(t.get('today', 0) or 0))
    h0_free = set()
    for _q1197 in range(B):
        for x in range(B):
            if _base_state(S, (x, _q1197)) in FREE_ST:
                h0_free.add((x, _q1197))
    return {'day': day, 'wstar': int(wstar), 'rem': rem, 'rem0': dict(rem), 'h0_free': h0_free, 'h0_locked': set(S.locked), 'added': {}, 'log': [], 'fill_log': [], 'n': {'land': 0, 'freed': 0, 'fill': 0}, 'jobs': 0, 'ops': 0}

class Replanter:

    def __init__(_q1052, cfg=None):
        _q1052.cfg = dict(RP_CFG)
        _q1052.cfg.update(cfg or {})
        _q1052.stats = {'steps': 0, 'runs': 0, 'errors': 0, 'jobs': 0, 'ops': 0, 'land': 0, 'freed': 0, 'fill': 0, 'ms_max': 0.0, 'ms_sum': 0.0}
        _q1052.last_error = ''

    def begin_day(_q1052, S, plan=None):
        return make_plan_state(S, plan, _q1052.cfg)

    def choose(_q1052, day, rem, w_tonight, wstar):
        """(crop, why) by the design 6.4 rule."""
        c = _q1052.cfg
        _q1180 = c['windows']
        for crop in c['quota_order']:
            if rem.get(crop, 0) > 0 and day <= int(_q1180.get(crop, -1)):
                return (crop, 'quota')
        if w_tonight < wstar + int(c['w_margin']):
            return ('WHEAT', 'wheat')
        _q421 = c['carrot_days']
        if _q421 and _q421[0] <= day <= _q421[1]:
            return ('CARROT', 'carrot')
        return ('WHEAT', 'wheat')

    def step(_q1052, S, ex, _q925, hour, day, acts=None):
        t0 = time.perf_counter()
        _q1052.stats['steps'] += 1
        _q880 = []
        _q1077 = None
        try:
            plan = _q1052._plan(S, ex, _q925, int(hour), int(day), acts)
            if plan:
                _q1077 = _q1052._snap(_q925)
            for xy, chain, rec in plan:
                ex_add_chain(ex, xy, chain)
                _q880.append((xy, chain))
                _q1052._book(_q925, xy, chain, rec)
        except Exception as _q520:
            _q1052.stats['errors'] += 1
            _q1052.last_error = ('%s/%s %s' % (day, hour, repr(_q520)))[:240]
            _q1052._rollback(ex, _q925, _q1077, _q880)
            _q880 = []
        ms = 1000.0 * (time.perf_counter() - t0)
        _q1052.stats['ms_sum'] += ms
        if ms > _q1052.stats['ms_max']:
            _q1052.stats['ms_max'] = ms
        return _q880

    @staticmethod
    def _snap(ps):
        return (dict(ps['added']), len(ps['log']), len(ps['fill_log']), dict(ps['n']), ps['jobs'], ps['ops'], dict(ps['rem']))

    def _rollback(_q1052, ex, ps, _q1077, _q340):
        """Undo this step's chain additions (an exception in the apply phase): the step makes no chain edits."""
        for xy, chain in _q340:
            t = xy[1] * B + xy[0]
            try:
                _chains(ex).pop(t, None)
                pool = getattr(ex, 'pool', None)
                if pool is not None:
                    pool.discard(t)
                _q1052.stats['jobs'] -= 1
                _q1052.stats['ops'] -= len(chain)
            except Exception:
                pass
        if _q1077 is not None and ps is not None:
            added, _q847, _q843, n, jobs, ops, rem = _q1077
            ps['added'] = added
            del ps['log'][_q847:]
            del ps['fill_log'][_q843:]
            for k in list(_q1052.stats):
                if k in ('land', 'freed', 'fill'):
                    _q1052.stats[k] -= ps['n'].get(k, 0) - n.get(k, 0)
            ps['n'], ps['jobs'], ps['ops'], ps['rem'] = (n, jobs, ops, rem)

    def _book(_q1052, ps, xy, chain, rec):
        kind, crop, why = (rec['kind'], rec['crop'], rec['why'])
        ps['added'][xy] = ps['added'].get(xy, 0) + 1
        ps['log'].append(rec)
        ps['n'][kind] = ps['n'].get(kind, 0) + 1
        ps['jobs'] += 1
        ps['ops'] += len(chain)
        if why == 'quota':
            ps['rem'][crop] = ps['rem'].get(crop, 0) - 1
        _q1052.stats['jobs'] += 1
        _q1052.stats['ops'] += len(chain)
        _q1052.stats[kind] = _q1052.stats.get(kind, 0) + 1

    def _chain(_q1052, crop, st):
        _q428 = [('PLANT', crop), ('WATER', None)]
        if st in ('weed', 'spent') and _q1052.cfg['explicit_dig']:
            _q428.insert(0, ('DIG', None))
        return _q428

    def _plan(_q1052, S, ex, ps, hour, day, acts):
        """Pure planning pass: [(xy, chain, record)] (nothing is written to the executor here)."""
        c = _q1052.cfg
        if ps is None or ps.get('day') != day or day > int(c['last_day']) or (not c['hours'][0] <= hour <= c['hours'][1]):
            return []
        _q1052.stats['runs'] += 1
        chains = _chains(ex)
        planted = {}
        _q944 = predict_tiles(S, acts, planted) if acts and c['predict'] else {}
        _q784 = int(c['max_per_tile'])
        added = ps['added']
        h0_free, h0_locked = (ps['h0_free'], ps['h0_locked'])
        land, freed, rest = ([], [], [])
        _q1097 = {}
        for _q1197 in range(B):
            for x in range(B):
                xy = (x, _q1197)
                if _q1197 * B + x in chains or xy in chains or added.get(xy, 0) >= _q784:
                    continue
                st = _q944.get(xy)
                if st is None:
                    st = _base_state(S, xy)
                if st not in FREE_ST:
                    continue
                _q1097[xy] = st
                if xy in h0_locked:
                    if c['land'] and hour <= int(c['land_last_h']):
                        land.append(xy)
                    else:
                        rest.append(xy)
                elif xy in h0_free:
                    rest.append(xy)
                else:
                    freed.append(xy)
        if not _q1097:
            return []
        units = [(int(_q888[0]), int(_q888[1])) for _q888 in S.units]
        _q409 = int(c['max_per_step'])
        plan = []
        rem = dict(ps['rem'])
        wstar = int(ps.get('wstar') or 0)
        _q1167 = wheat_tonight(S, chains, _q944, planted)

        def rec(xy, kind, crop, why, **_q713):
            _q970 = {'day': day, 'hour': hour, 'xy': xy, 'kind': kind, 'crop': crop, 'why': why, 'w_tonight': _q1167, 'wstar': wstar, 'rem': dict(rem), 'st': _q1097[xy]}
            _q970.update(_q713)
            return _q970

        def _q831(xy):
            return min((_dist(xy, _q888) for _q888 in units), default=0)
        if c['land'] and land and (hour <= int(c['land_last_h'])):
            land.sort(key=lambda xy: (_q831(xy), xy[1], xy[0]))
            crop = c['land_crop']
            for xy in land:
                if len(plan) >= _q409:
                    break
                plan.append((xy, _q1052._chain(crop, _q1097[xy]), rec(xy, 'land', crop, 'land')))
                if crop == 'WHEAT':
                    _q1167 += 1
        _q833 = c['fill'] and c['fill_h'][0] <= hour <= c['fill_h'][1] or (c['freed'] and c['freed_need_slack'])
        slack = {}
        total = 0.0
        _q597 = float(c['fill_turns'])
        if _q833:
            _q1066 = ex_slack(ex)
            slack = {_q1147: s for _q1147, s in _q1066.items() if _q1147 < len(units) and s >= _q597}
            total = sum(slack.values())
        spent = 0.0
        if c['freed'] and freed:
            freed.sort(key=lambda xy: (_q831(xy), xy[1], xy[0]))
            for xy in freed:
                if len(plan) >= _q409:
                    break
                if c['freed_need_slack']:
                    if total - spent < _q597:
                        break
                    spent += _q597
                crop, why = _q1052.choose(day, rem, _q1167, wstar)
                plan.append((xy, _q1052._chain(crop, _q1097[xy]), rec(xy, 'freed', crop, why)))
                if why == 'quota':
                    rem[crop] -= 1
                if crop == 'WHEAT':
                    _q1167 += 1
                _q1097.pop(xy, None)
        if c['fill'] and c['fill_h'][0] <= hour <= c['fill_h'][1] and (len(plan) < _q409):
            _q585 = c['fill_pool_block']
            blocked = False
            if _q585 and _pool_n(ex) > 0:
                if _q585 == 'tight' and acts:
                    blocked = not any((isinstance(a, (list, tuple)) and a and (a[0] == 'PASS') for a in acts))
                else:
                    blocked = True
            if not blocked:
                _q1115 = set((_q888[0] for _q888 in plan))
                _q402 = [xy for xy in rest + freed if xy not in _q1115 and xy in _q1097]
                _q1105 = sum((len(_q888[1]) for _q888 in plan if _q888[2]['kind'] != 'land'))
                _q382 = total - max(spent, float(_q1105))
                _q808 = int(_q382 // _q597) if _q382 > 0 else 0
                if _q402 and _q808 > 0 and slack:
                    _q532 = ex_route_ends(ex, 24 - hour)
                    anchor = {_q1147: _q532.get(_q1147, units[_q1147]) for _q1147 in slack}
                    _q983 = dict(slack)
                    if len(_q402) > int(c['fill_cands']):
                        _q402.sort(key=lambda xy: (min((_dist(xy, a) for a in anchor.values())), xy[1], xy[0]))
                        _q402 = _q402[:int(c['fill_cands'])]
                    charged = {}
                    _q803 = 0
                    while _q808 > 0 and _q402 and (len(plan) < _q409):
                        best = None
                        for _q1147, a in anchor.items():
                            _q1024 = _q983[_q1147]
                            if _q1024 < _q597:
                                continue
                            for xy in _q402:
                                _q475 = _dist(a, xy)
                                _q1104 = 3 if _q1097[xy] in ('weed', 'spent') else 2
                                cost = max(_q597, float(_q475 + _q1104)) if c['fill_charge_travel'] else _q597
                                if cost > _q1024:
                                    continue
                                k = (_q475, xy[1], xy[0], _q1147)
                                if best is None or k < best[0]:
                                    best = (k, _q1147, xy, cost)
                        if best is None:
                            break
                        _, _q1147, xy, cost = best
                        crop, why = _q1052.choose(day, rem, _q1167, wstar)
                        plan.append((xy, _q1052._chain(crop, _q1097[xy]), rec(xy, 'fill', crop, why, unit=_q1147, cost=cost)))
                        if why == 'quota':
                            rem[crop] -= 1
                        if crop == 'WHEAT':
                            _q1167 += 1
                        _q983[_q1147] -= cost
                        charged[_q1147] = charged.get(_q1147, 0.0) + cost
                        anchor[_q1147] = xy
                        _q402.remove(xy)
                        _q808 -= 1
                        _q803 += 1
                    if _q803:
                        ps['fill_log'].append({'day': day, 'hour': hour, 'slack': dict(slack), 'total': total, 'pre_used': max(spent, float(_q1105)), 'n': _q803, 'charged': charged})
        return plan

def classify(S, acts):
    """[(cls, op, eff, target)] per unit - tools/tmp/sys_audit_lib.classify_turn on a FarmState (S = the observation
    before the step, acts = the final commands)."""
    tiles = S.tiles
    pos = S.units
    _q672 = S.inventories
    seeds = S.seeds
    day = S.day
    demand = {}
    for a in acts:
        if isinstance(a, list) and len(a) >= 2 and (a[0] == 'PLANT'):
            demand[a[1]] = demand.get(a[1], 0) + 1
    blocked = {c for c, n in demand.items() if n > int(seeds.get(c, 0) or 0)}
    _q1157 = set()
    _q880 = []
    for _q1147, a in enumerate(acts[:len(pos)]):
        if not isinstance(a, list) or not a:
            _q880.append(('pass', 'NONE', False, None))
            continue
        op = a[0]
        _q888 = (int(pos[_q1147][0]), int(pos[_q1147][1]))
        inv = _q672[_q1147] if _q1147 < len(_q672) else {}
        if op in MOVES:
            _q880.append(('move', 'MOVE', True, None))
            continue
        if op == 'PASS':
            _q880.append(('pass', 'PASS', False, None))
            continue
        _q319 = _q888 in ((4, 4), (5, 4), (4, 5), (5, 5))
        if op == 'PICKUP':
            _q880.append(('pickup', op, _q319, a[1] if len(a) > 1 else None))
            continue
        if op == 'DROP':
            _q880.append(('unload', op, _q319 and any((_q1159 > 0 for _q1159 in inv.values())), None))
            continue
        if op == 'PLACE' and len(a) > 1 and (a[1] not in ANIMALS):
            _q880.append(('unload', 'PLACE_SHED', _q319 and inv.get(a[1], 0) > 0, a[1]))
            continue
        x, _q1197 = _q888
        t = tiles[_q1197][x]
        _q673 = isinstance(t, dict)
        kind = t.get('kind') if _q673 else None
        _q1120 = t.get('crop') or t.get('animal') or kind if _q673 else 'LOCKED' if t == 'LOCKED' else None
        key = (_q888, op)
        eff = False
        if t != 'LOCKED' and key not in _q1157:
            if op == 'WATER':
                eff = kind == 'PLANT' and (not t.get('watered_today'))
            elif op == 'HARVEST':
                eff = _q673 and t.get('yield_units', 0) > 0 and (bool(t.get('animal')) or (kind == 'PLANT' and day - t.get('planted_day', day) >= FYD.get(t.get('crop'), 99)))
            elif op == 'FEED':
                eff = _q673 and bool(t.get('animal')) and (not t.get('fed_today')) and (inv.get('WHEAT', 0) > 0)
            elif op == 'CARE':
                eff = _q673 and bool(t.get('animal')) and (not t.get('cared_today'))
            elif op == 'COLLECT_FERTILIZER':
                eff = _q673 and bool(t.get('animal')) and bool(t.get('fertilizer_available'))
            elif op == 'FERTILIZE':
                eff = kind == 'PLANT' and inv.get('FERTILIZER', 0) > 0
            elif op == 'PLANT':
                eff = t is None and len(a) > 1 and (a[1] not in blocked) and (int(seeds.get(a[1], 0) or 0) > 0)
                _q1120 = a[1] if len(a) > 1 else None
            elif op == 'DIG':
                eff = t is not None and (not (_q673 and t.get('animal')))
            elif op in BUILD_OPS:
                eff = t is None
            elif op == 'PLACE':
                eff = _q673 and kind == STRUCT.get(a[1]) and (not t.get('animal')) and (inv.get(a[1], 0) > 0)
                _q1120 = a[1]
        if eff:
            _q1157.add(key)
        _q880.append(('prod' if op in TILE_OPS or op == 'PLACE' else 'other', op, eff, _q1120))
    return _q880

def _new_day_rec():
    return {'steps': 0, 'hours': [0] * 24, 'unit_turns': 0, 'units_max': 0, 'pass': 0, 'pass_h': [0] * 24, 'busy': 0, 'eff': 0, 'noeff': 0, 'eff_op': {}, 'moves': 0, 'pickups': 0, 'unloads': 0, 'plant_h': [0] * 24, 'seed_blocked': 0, 'pool_seen_h12': 0, 'pool_steps_h12': 0, 'pool_tight_h12': 0, 'missed': None, 'missed_op': {}, 'rp_jobs': 0, 'rp_ops': 0, 'rp_crop': {}, 'rp_kind': {}, 'hires': 0}

class Ledger:

    def __init__(_q1052, cfg=None):
        _q1052.cfg = dict(LEDGER_CFG)
        _q1052.cfg.update(cfg or {})
        _q1052.days = {}
        _q1052.errors = 0
        _q1052.last_error = ''
        _q1052.ms_max = 0.0

    def rec(_q1052, day):
        _q970 = _q1052.days.get(int(day))
        if _q970 is None:
            _q970 = _q1052.days[int(day)] = _new_day_rec()
        return _q970

    def day(_q1052, _q475):
        return _q1052.days.get(int(_q475))

    def step(_q1052, S, acts, pool_n=None, pending=None, rp_added=None, seed_blocked=None):
        """One step: S = FarmState before the step, acts = the final commands, pool_n = len(ex.pool) after the act,
        pending = ex.pending_ops() after the act (read at hour 23 as the missed ops), rp_added = this step's
        Replanter result (list of (xy, chain)) or a job count.  seed_blocked (review fix; None = count the PLANTs of
        the final commands beyond the seeds held): the PLANTs the caller's seed guard turned into PASS this step - the
        final commands never exceed the seeds once a guard ran, so the default count is always 0 behind pd_layer's
        _pd_guard_plants.  Returns the classification (or None on error)."""
        t0 = time.perf_counter()
        try:
            acts = [list(a) if isinstance(a, (list, tuple)) else a for a in acts or []]
            _q437 = classify(S, acts)
            demand = {}
            for a in acts:
                if isinstance(a, list) and len(a) >= 2 and (a[0] == 'PLANT'):
                    demand[a[1]] = demand.get(a[1], 0) + 1
            _q1040 = sum((n for c, n in demand.items() if n > int(S.seeds.get(c, 0) or 0)))
            if seed_blocked is not None:
                _q1040 = int(seed_blocked)
            _q1052.step_cls(int(S.day), int(S.hour), _q437, pool_n=pool_n, pending=pending, rp_added=rp_added, seed_blocked=_q1040, hires=int(getattr(S, 'hires_today', 0) or 0))
        except Exception as _q520:
            _q1052.errors += 1
            _q1052.last_error = repr(_q520)[:240]
            _q437 = None
        ms = 1000.0 * (time.perf_counter() - t0)
        if ms > _q1052.ms_max:
            _q1052.ms_max = ms
        return _q437

    def step_cls(_q1052, day, hour, _q437, pool_n=None, pending=None, rp_added=None, seed_blocked=0, hires=None):
        """The accumulation part of step() for a precomputed classification (e.g. sys_audit_games rows)."""
        _q970 = _q1052.rec(day)
        _q970['steps'] += 1
        if 0 <= hour < 24:
            _q970['hours'][hour] += 1
        n = len(_q437)
        _q970['unit_turns'] += n
        if n > _q970['units_max']:
            _q970['units_max'] = n
        if hires is not None:
            _q970['hires'] = max(_q970['hires'], int(hires))
        for c, op, eff, _q1120 in _q437:
            if c == 'pass':
                _q970['pass'] += 1
                _q970['pass_h'][hour] += 1
                continue
            _q970['busy'] += 1
            if c == 'prod':
                if eff:
                    _q970['eff'] += 1
                    _q970['eff_op'][op] = _q970['eff_op'].get(op, 0) + 1
                    if op == 'PLANT':
                        _q970['plant_h'][hour] += 1
                else:
                    _q970['noeff'] += 1
            elif c == 'move':
                _q970['moves'] += 1
            elif c == 'pickup':
                _q970['pickups'] += 1
            elif c == 'unload':
                _q970['unloads'] += 1
        _q970['seed_blocked'] += int(seed_blocked or 0)
        if pool_n is not None and hour >= int(_q1052.cfg['pool_h']):
            _q970['pool_seen_h12'] += 1
            if int(pool_n) > 0:
                _q970['pool_steps_h12'] += 1
                if not any((x[0] == 'pass' for x in _q437)):
                    _q970['pool_tight_h12'] += 1
        if hour == 23 and pending is not None:
            _q1052._missed(_q970, pending)
        if rp_added:
            _q1052.note_replant(day, rp_added)

    def _missed(_q1052, _q970, pending):
        _q1065 = _q1052.cfg['missed_skip']
        _q781 = {k: int(_q1159) for k, _q1159 in dict(pending).items() if _q1159 and k not in _q1065}
        _q970['missed_op'] = _q781
        _q970['missed'] = sum(_q781.values())

    def note_replant(_q1052, day, added):
        """Replanter additions: a list of (xy, chain) (or of Replanter log records) or a job count."""
        _q970 = _q1052.rec(day)
        if isinstance(added, int):
            _q970['rp_jobs'] += added
            return
        for item in added:
            if isinstance(item, dict):
                chain = [('PLANT', item.get('crop'))]
                crop, kind = (item.get('crop'), item.get('kind'))
            else:
                chain = item[1]
                crop = next((_q857[1] for _q857 in chain if _q857[0] == 'PLANT'), None)
                kind = None
            _q970['rp_jobs'] += 1
            _q970['rp_ops'] += len(chain)
            if crop:
                _q970['rp_crop'][crop] = _q970['rp_crop'].get(crop, 0) + 1
            if kind:
                _q970['rp_kind'][kind] = _q970['rp_kind'].get(kind, 0) + 1

    def end_day(_q1052, day, pending=None):
        """Close a day: the missed ops (pending ops left after its hour-23 act) if step() did not see hour 23."""
        _q970 = _q1052.rec(day)
        if pending is not None and _q970['missed'] is None:
            _q1052._missed(_q970, pending)
        return _q970

    def derived(_q1052, _q475):
        """C8 inputs of day d (None when the day was not seen)."""
        _q970 = _q1052.days.get(int(_q475))
        if _q970 is None:
            return None
        h0, h1 = LAB_CFG['cut_h']
        return {'day': int(_q475), 'complete': _q970['steps'] >= 20, 'eff': _q970['eff'], 'busy': _q970['busy'], 'tpt': _q970['busy'] / float(_q970['eff']) if _q970['eff'] else None, 'pass': _q970['pass'], 'pass_h5_23': sum(_q970['pass_h'][h0:h1 + 1]), 'pool_empty_h12': _q970['pool_seen_h12'] > 0 and _q970['pool_steps_h12'] == 0, 'pool_steps_h12': _q970['pool_steps_h12'], 'pool_tight_h12': _q970['pool_tight_h12'], 'pass_h12_23': sum(_q970['pass_h'][int(_q1052.cfg['pool_h']):24]), 'missed': _q970['missed'], 'rp_jobs': _q970['rp_jobs'], 'rp_ops': _q970['rp_ops'], 'unit_turns': _q970['unit_turns'], 'units_max': _q970['units_max'], 'plantings': sum(_q970['plant_h']), 'plant_h19_22': sum(_q970['plant_h'][19:23]), 'seed_blocked': _q970['seed_blocked']}

def must_do_ops(S, chains):
    """Level-3-like ops in the chains when the task list is not given: roots (PLANT / BUILD / PLACE), the HARVEST /
    DIG that clear a root's tile, the WATER after a PLANT, WATER on a plant that weeds tonight, FEED on an animal that
    escapes tonight, HARVEST of a decaying crop."""
    n = 0
    for k, _q428 in chains.items():
        xy = _xy(k)
        _q458 = S.crops.get(xy) if S is not None else None
        _q336 = S.animals.get(xy) if S is not None else None
        ops = [_q857[0] for _q857 in _q428]
        root = any((op in ('PLANT', 'PLACE') or op in BUILD_OPS for op in ops))
        planted = False
        for op in ops:
            if op in ('PLANT', 'PLACE') or op in BUILD_OPS:
                n += 1
                planted = planted or op == 'PLANT'
            elif op == 'DIG' and root:
                n += 1
            elif op == 'HARVEST' and (root or (_q458 is not None and _q458.decaying)):
                n += 1
            elif op == 'WATER' and (planted or (_q458 is not None and _q458.must_water)):
                n += 1
            elif op == 'FEED' and _q336 is not None and _q336.must_feed:
                n += 1
    return n

class Labour:

    def __init__(_q1052, cfg=None):
        _q1052.cfg = dict(LAB_CFG)
        _q1052.cfg.update(cfg or {})
        _q1052.tpt = float(_q1052.cfg['tpt0'])
        _q1052.seen = set()
        _q1052.last = {}
        _q1052.history = []
        _q1052.errors = 0
        _q1052.last_error = ''

    def update(_q1052, ledger, day):
        """EMA of realised busy turns per effective op over the finished days before `day` not yet used."""
        c = _q1052.cfg
        if not c['ema'] or ledger is None:
            return _q1052.tpt
        for _q475 in sorted(ledger.days):
            if _q475 >= day or _q475 in _q1052.seen or _q475 < int(c['ema_from_day']):
                continue
            _q517 = ledger.derived(_q475)
            if _q517 is None or not _q517['complete']:
                continue
            _q1052.seen.add(_q475)
            if _q517['eff'] < int(c['min_eff']) or _q517['tpt'] is None:
                continue
            a = float(c['alpha'])
            _q1052.tpt = min(float(c['tpt_hi']), max(float(c['tpt_lo']), (1 - a) * _q1052.tpt + a * _q517['tpt']))
        return _q1052.tpt

    def feedback(_q1052, ledger, day):
        """(+1 / -1 / 0, why) from yesterday's Ledger day."""
        c = _q1052.cfg
        if not c['fb'] or ledger is None:
            return (0, '')
        _q517 = ledger.derived(day - 1)
        if _q517 is None or not _q517['complete']:
            return (0, '')
        if c['add_tight']:
            _q778 = _q517['missed'] is not None and _q517['missed'] > int(c['add_missed']) and (_q517['pass_h12_23'] <= int(c['cut_pass']))
            pool = _q517['pool_tight_h12'] >= int(c['add_pool_steps'])
        else:
            _q778 = _q517['missed'] is not None and _q517['missed'] > int(c['add_missed'])
            pool = _q517['pool_steps_h12'] >= int(c['add_pool_steps'])
        if _q778 or pool:
            return (1, 'missed %s pool %d' % (_q517['missed'], _q517['pool_steps_h12']))
        h0, h1 = c['cut_h']
        _q970 = ledger.day(day - 1)
        _q920 = sum(_q970['pass_h'][h0:h1 + 1])
        if _q920 > int(c['cut_pass']) and _q517['pool_empty_h12']:
            return (-1, 'pass %d' % _q920)
        return (0, '')

    def hires(_q1052, S, chains, ledger, day, tasks=None, n_l3=None):
        """(n_h0, n_h1) HIRE orders for today, or None (not decided here: other days / error)."""
        try:
            return _q1052._hires(S, chains, ledger, int(day), tasks, n_l3)
        except Exception as _q520:
            _q1052.errors += 1
            _q1052.last_error = ('%s %s' % (day, repr(_q520)))[:240]
            return None

    def _hires(_q1052, S, chains, ledger, day, tasks, n_l3):
        c = _q1052.cfg
        if not c['days'][0] <= day <= c['days'][1]:
            return None
        tpt = _q1052.update(ledger, day)
        ops = sum((len(_q428) for _q428 in (chains or {}).values()))
        rp_prev = 0
        if ledger is not None:
            _q1202 = ledger.day(day - 1)
            if _q1202 is not None:
                rp_prev = int(_q1202['rp_jobs'])
        load = ops + rp_prev * float(c['rp_ops'])
        lo, hi = (int(c['lo']), int(c['hi']))
        base = int(math.ceil(max(0.0, load * tpt - float(c['far'])) / float(c['hand'])))
        h = max(lo, min(hi, base))
        fb, why = _q1052.feedback(ledger, day)
        _q625 = h + fb
        if not c['fb_below_lo']:
            _q625 = max(lo, _q625)
        _q625 = min(hi, _q625)
        if n_l3 is None:
            if tasks is not None:
                n_l3 = sum((1 for t in tasks if getattr(t, 'level', 0) >= 3))
            else:
                n_l3 = must_do_ops(S, chains or {})
        floor = min(hi, int(math.ceil(float(n_l3) * float(c['floor_tpt']) / float(c['hand']))))
        _q625 = max(_q625, floor)
        _q501 = int(getattr(S, 'hires_today', 0) or 0) if S is not None else 0
        n = max(0, _q625 - _q501)
        _q791 = min(n, int(c['h0_max']))
        _q1052.last = {'day': day, 'ops': ops, 'rp_prev': rp_prev, 'load': load, 'tpt': round(tpt, 3), 'base': base, 'fb': fb, 'fb_why': why, 'n_l3': n_l3, 'floor': floor, 'hands': _q625, 'n_h0': _q791, 'n_h1': n - _q791}
        _q1052.history.append(_q1052.last)
        return (_q791, n - _q791)