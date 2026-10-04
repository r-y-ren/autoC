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
    _q481 = getattr(ex, 'chains', None)
    return _q481 if isinstance(_q481, dict) else {}

def _pool_n(ex):
    try:
        return len(getattr(ex, 'pool', ()) or ())
    except TypeError:
        return 0

def ex_slack(ex):
    """{unit: free turns}: ex.slack(), else cap - delay - dur of the executor's own routes (present units)."""
    f = getattr(ex, 'slack', None)
    if callable(f):
        return {int(_q1221): float(_q1233) for _q1221, _q1233 in (f() or {}).items()}
    routes = getattr(ex, 'routes', None)
    cap = getattr(ex, 'cap', None)
    if not routes or cap is None:
        return {}
    _q554 = getattr(ex, 'delay', None) or []
    n = int(getattr(ex, 'n_units', len(routes)) or 0)
    return {_q1221: float(cap - (_q554[_q1221] if _q1221 < len(_q554) else 0) - _q1036.dur) for _q1221, _q1036 in enumerate(routes[:n])}

def ex_route_ends(ex, H):
    """{unit: (x, y)} the tile of each unit's last op within H turns: ex.route_ops(H), else the last route tile."""
    f = getattr(ex, 'route_ops', None)
    _q946 = {}
    if callable(f):
        best = {}
        for _q1086 in f(H) or ():
            _q1221, _q591, xy = (_q1086[0], _q1086[1], _q1086[2])
            if _q1221 not in best or _q591 >= best[_q1221]:
                best[_q1221] = _q591
                _q946[_q1221] = _xy(xy)
        return _q946
    for _q1221, _q1036 in enumerate(getattr(ex, 'routes', None) or ()):
        tl = getattr(_q1036, 'tl', None)
        if tl:
            _q946[_q1221] = _xy(tl[-1])
    return _q946

def ex_add_chain(ex, xy, chain):
    """ex.add_chain(xy, chain), else the _pd_fill plumbing."""
    f = getattr(ex, 'add_chain', None)
    if callable(f):
        f(xy, list(chain))
        return
    t = xy[1] * B + xy[0]
    ex.chains[t] = [tuple(_q922) for _q922 in chain]
    if t not in (getattr(ex, 'where', None) or {}):
        ex.pool.add(t)

def ex_pending_ops(ex):
    """{op: count} of the ops still in the chains: ex.pending_ops(), else counted from ex.chains."""
    f = getattr(ex, 'pending_ops', None)
    if callable(f):
        return dict(f() or {})
    _q946 = {}
    for _q481 in _chains(ex).values():
        for _q922 in _q481:
            _q946[_q922[0]] = _q946.get(_q922[0], 0) + 1
    return _q946

def pending_plants(ex):
    """{crop: PLANT ops still in the chains}."""
    _q946 = {}
    for _q481 in _chains(ex).values():
        for _q922 in _q481:
            if _q922[0] == 'PLANT' and len(_q922) > 1 and _q922[1]:
                _q946[_q922[1]] = _q946.get(_q922[1], 0) + 1
    return _q946

def seed_shortfall(S, ex):
    """{crop: seeds to buy}: PLANT ops in the chains beyond the seeds held (the fallback buy list while C7 is off)."""
    _q946 = {}
    for c, n in pending_plants(ex).items():
        k = n - int(S.seeds.get(c, 0))
        if k > 0:
            _q946[c] = k
    return _q946

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
        _q513 = S.crops.get(xy)
        return 'spent' if _q513 is not None and _q513.spent else 'crop'
    if t.get('animal'):
        return 'animal'
    return 'struct'

def predict_tiles(S, acts, planted=None):
    """{(x, y): state} of the tiles this step's final commands change (units in engine order): HARVEST of a ripe
    non-ongoing crop -> 'empty'; HARVEST of an ongoing crop with no production left -> 'spent'; DIG -> 'empty';
    PLANT / BUILD on an empty tile -> 'crop' / 'struct' (a seed-blocked PLANT keeps its chain, so the tile is taken
    either way).  planted (optional dict) receives {(x, y): crop} of this step's PLANTs."""
    _q1011 = {}
    if not acts:
        return _q1011
    units = S.units
    for _q1221, a in enumerate(acts):
        if _q1221 >= len(units) or not a or (not isinstance(a, (list, tuple))):
            continue
        op = a[0]
        if op not in ('HARVEST', 'DIG', 'PLANT') and op not in BUILD_OPS:
            continue
        xy = (int(units[_q1221][0]), int(units[_q1221][1]))
        _q522 = _q1011.get(xy)
        if _q522 is None:
            _q522 = _base_state(S, xy)
        if _q522 == 'locked':
            continue
        if op == 'HARVEST':
            if xy in _q1011 or _q522 != 'crop':
                continue
            _q513 = S.crops.get(xy)
            if _q513 is None or _q513.units <= 0 or _q513.age < FYD.get(_q513.crop, 99):
                continue
            if not ONGOING.get(_q513.crop, False):
                _q1011[xy] = 'empty'
            elif _q513.prods_left == 0:
                _q1011[xy] = 'spent'
        elif op == 'DIG':
            if _q522 in ('weed', 'spent', 'crop', 'struct'):
                _q1011[xy] = 'empty'
                if planted is not None:
                    planted.pop(xy, None)
        elif op == 'PLANT':
            if _q522 == 'empty':
                _q1011[xy] = 'crop'
                if planted is not None and len(a) > 1:
                    planted[xy] = a[1]
        elif _q522 == 'empty':
            _q1011[xy] = 'struct'
    return _q1011

def wheat_tonight(S, chains, _q1011=None, planted=None):
    """Standing wheat tonight: wheat on the board that no chain cuts without a replant and no command of this step
    removes, plus every chain whose last PLANT is WHEAT, plus this step's WHEAT PLANTs (planted, from predict_tiles:
    the executor pops a PLANT when it issues it, and the observation does not show the plant yet) unless the tile's
    chain still holds a PLANT (a seed-blocked op given back by the guard)."""
    _q1011 = _q1011 or {}
    planted = planted or {}
    n = 0
    for xy, crop in planted.items():
        if crop != 'WHEAT':
            continue
        _q481 = chains.get(xy[1] * B + xy[0])
        if _q481 is None:
            _q481 = chains.get(xy)
        if _q481 and any((_q922[0] in ('PLANT', 'DIG') for _q922 in _q481)):
            continue
        n += 1
    for xy, _q513 in S.crops.items():
        if _q513.crop != 'WHEAT' or xy in planted or _q1011.get(xy) in FREE_ST:
            continue
        _q481 = chains.get(xy[1] * B + xy[0])
        if _q481 is None:
            _q481 = chains.get(xy)
        if _q481:
            ops = [_q922[0] for _q922 in _q481]
            if 'PLANT' in ops or 'DIG' in ops:
                continue
            if 'HARVEST' in ops and _q513.age >= FYD['WHEAT']:
                continue
        n += 1
    for _q481 in chains.values():
        _q785 = None
        for _q922 in _q481:
            if _q922[0] == 'PLANT':
                _q785 = _q922[1] if len(_q922) > 1 else None
        if _q785 == 'WHEAT':
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
        _q877 = sum((1 for _q922 in plan.get('ops') or () if _q922 and _q922[0] == 'PLACE'))
        _q366, _q634, _q512 = c['wstar']
        if day <= int(c['wstar_last']):
            wstar = max(int(round(_q634 * owned)), min(int(round(_q512 * owned)), int(round(_q366 * (len(S.animals) + _q877)))))
        else:
            wstar = 0
    rem = {}
    _q1192 = plan.get('targets') or {}
    for crop, _q1272 in Q_KEY.items():
        t = _q1192.get(_q1272) or {}
        rem[crop] = max(0, int(t.get('quota', 0) or 0) - int(t.get('today', 0) or 0))
    h0_free = set()
    for _q1272 in range(B):
        for x in range(B):
            if _base_state(S, (x, _q1272)) in FREE_ST:
                h0_free.add((x, _q1272))
    return {'day': day, 'wstar': int(wstar), 'rem': rem, 'rem0': dict(rem), 'h0_free': h0_free, 'h0_locked': set(S.locked), 'added': {}, 'log': [], 'fill_log': [], 'n': {'land': 0, 'freed': 0, 'fill': 0}, 'jobs': 0, 'ops': 0}

class Replanter:

    def __init__(_q1120, cfg=None):
        _q1120.cfg = dict(RP_CFG)
        _q1120.cfg.update(cfg or {})
        _q1120.stats = {'steps': 0, 'runs': 0, 'errors': 0, 'jobs': 0, 'ops': 0, 'land': 0, 'freed': 0, 'fill': 0, 'ms_max': 0.0, 'ms_sum': 0.0}
        _q1120.last_error = ''

    def begin_day(_q1120, S, plan=None):
        return make_plan_state(S, plan, _q1120.cfg)

    def choose(_q1120, day, rem, w_tonight, wstar):
        """(crop, why) by the design 6.4 rule."""
        c = _q1120.cfg
        _q1255 = c['windows']
        for crop in c['quota_order']:
            if rem.get(crop, 0) > 0 and day <= int(_q1255.get(crop, -1)):
                return (crop, 'quota')
        if w_tonight < wstar + int(c['w_margin']):
            return ('WHEAT', 'wheat')
        _q474 = c['carrot_days']
        if _q474 and _q474[0] <= day <= _q474[1]:
            return ('CARROT', 'carrot')
        return ('WHEAT', 'wheat')

    def step(_q1120, S, ex, _q991, hour, day, acts=None):
        t0 = time.perf_counter()
        _q1120.stats['steps'] += 1
        _q946 = []
        _q1147 = None
        try:
            plan = _q1120._plan(S, ex, _q991, int(hour), int(day), acts)
            if plan:
                _q1147 = _q1120._snap(_q991)
            for xy, chain, rec in plan:
                ex_add_chain(ex, xy, chain)
                _q946.append((xy, chain))
                _q1120._book(_q991, xy, chain, rec)
        except Exception as _q575:
            _q1120.stats['errors'] += 1
            _q1120.last_error = ('%s/%s %s' % (day, hour, repr(_q575)))[:240]
            _q1120._rollback(ex, _q991, _q1147, _q946)
            _q946 = []
        ms = 1000.0 * (time.perf_counter() - t0)
        _q1120.stats['ms_sum'] += ms
        if ms > _q1120.stats['ms_max']:
            _q1120.stats['ms_max'] = ms
        return _q946

    @staticmethod
    def _snap(ps):
        return (dict(ps['added']), len(ps['log']), len(ps['fill_log']), dict(ps['n']), ps['jobs'], ps['ops'], dict(ps['rem']))

    def _rollback(_q1120, ex, ps, _q1147, _q392):
        """Undo this step's chain additions (an exception in the apply phase): the step makes no chain edits."""
        for xy, chain in _q392:
            t = xy[1] * B + xy[0]
            try:
                _chains(ex).pop(t, None)
                pool = getattr(ex, 'pool', None)
                if pool is not None:
                    pool.discard(t)
                _q1120.stats['jobs'] -= 1
                _q1120.stats['ops'] -= len(chain)
            except Exception:
                pass
        if _q1147 is not None and ps is not None:
            added, _q911, _q907, n, jobs, ops, rem = _q1147
            ps['added'] = added
            del ps['log'][_q911:]
            del ps['fill_log'][_q907:]
            for k in list(_q1120.stats):
                if k in ('land', 'freed', 'fill'):
                    _q1120.stats[k] -= ps['n'].get(k, 0) - n.get(k, 0)
            ps['n'], ps['jobs'], ps['ops'], ps['rem'] = (n, jobs, ops, rem)

    def _book(_q1120, ps, xy, chain, rec):
        kind, crop, why = (rec['kind'], rec['crop'], rec['why'])
        ps['added'][xy] = ps['added'].get(xy, 0) + 1
        ps['log'].append(rec)
        ps['n'][kind] = ps['n'].get(kind, 0) + 1
        ps['jobs'] += 1
        ps['ops'] += len(chain)
        if why == 'quota':
            ps['rem'][crop] = ps['rem'].get(crop, 0) - 1
        _q1120.stats['jobs'] += 1
        _q1120.stats['ops'] += len(chain)
        _q1120.stats[kind] = _q1120.stats.get(kind, 0) + 1

    def _chain(_q1120, crop, st):
        _q481 = [('PLANT', crop), ('WATER', None)]
        if st in ('weed', 'spent') and _q1120.cfg['explicit_dig']:
            _q481.insert(0, ('DIG', None))
        return _q481

    def _plan(_q1120, S, ex, ps, hour, day, acts):
        """Pure planning pass: [(xy, chain, record)] (nothing is written to the executor here)."""
        c = _q1120.cfg
        if ps is None or ps.get('day') != day or day > int(c['last_day']) or (not c['hours'][0] <= hour <= c['hours'][1]):
            return []
        _q1120.stats['runs'] += 1
        chains = _chains(ex)
        planted = {}
        _q1011 = predict_tiles(S, acts, planted) if acts and c['predict'] else {}
        _q847 = int(c['max_per_tile'])
        added = ps['added']
        h0_free, h0_locked = (ps['h0_free'], ps['h0_locked'])
        land, freed, rest = ([], [], [])
        _q1168 = {}
        for _q1272 in range(B):
            for x in range(B):
                xy = (x, _q1272)
                if _q1272 * B + x in chains or xy in chains or added.get(xy, 0) >= _q847:
                    continue
                st = _q1011.get(xy)
                if st is None:
                    st = _base_state(S, xy)
                if st not in FREE_ST:
                    continue
                _q1168[xy] = st
                if xy in h0_locked:
                    if c['land'] and hour <= int(c['land_last_h']):
                        land.append(xy)
                    else:
                        rest.append(xy)
                elif xy in h0_free:
                    rest.append(xy)
                else:
                    freed.append(xy)
        if not _q1168:
            return []
        units = [(int(_q954[0]), int(_q954[1])) for _q954 in S.units]
        _q462 = int(c['max_per_step'])
        plan = []
        rem = dict(ps['rem'])
        wstar = int(ps.get('wstar') or 0)
        _q1242 = wheat_tonight(S, chains, _q1011, planted)

        def rec(xy, kind, crop, why, **_q775):
            _q1036 = {'day': day, 'hour': hour, 'xy': xy, 'kind': kind, 'crop': crop, 'why': why, 'w_tonight': _q1242, 'wstar': wstar, 'rem': dict(rem), 'st': _q1168[xy]}
            _q1036.update(_q775)
            return _q1036

        def _q895(xy):
            return min((_dist(xy, _q954) for _q954 in units), default=0)
        if c['land'] and land and (hour <= int(c['land_last_h'])):
            land.sort(key=lambda xy: (_q895(xy), xy[1], xy[0]))
            crop = c['land_crop']
            for xy in land:
                if len(plan) >= _q462:
                    break
                plan.append((xy, _q1120._chain(crop, _q1168[xy]), rec(xy, 'land', crop, 'land')))
                if crop == 'WHEAT':
                    _q1242 += 1
        _q897 = c['fill'] and c['fill_h'][0] <= hour <= c['fill_h'][1] or (c['freed'] and c['freed_need_slack'])
        slack = {}
        total = 0.0
        _q653 = float(c['fill_turns'])
        if _q897:
            _q1136 = ex_slack(ex)
            slack = {_q1221: s for _q1221, s in _q1136.items() if _q1221 < len(units) and s >= _q653}
            total = sum(slack.values())
        spent = 0.0
        if c['freed'] and freed:
            freed.sort(key=lambda xy: (_q895(xy), xy[1], xy[0]))
            for xy in freed:
                if len(plan) >= _q462:
                    break
                if c['freed_need_slack']:
                    if total - spent < _q653:
                        break
                    spent += _q653
                crop, why = _q1120.choose(day, rem, _q1242, wstar)
                plan.append((xy, _q1120._chain(crop, _q1168[xy]), rec(xy, 'freed', crop, why)))
                if why == 'quota':
                    rem[crop] -= 1
                if crop == 'WHEAT':
                    _q1242 += 1
                _q1168.pop(xy, None)
        if c['fill'] and c['fill_h'][0] <= hour <= c['fill_h'][1] and (len(plan) < _q462):
            _q640 = c['fill_pool_block']
            blocked = False
            if _q640 and _pool_n(ex) > 0:
                if _q640 == 'tight' and acts:
                    blocked = not any((isinstance(a, (list, tuple)) and a and (a[0] == 'PASS') for a in acts))
                else:
                    blocked = True
            if not blocked:
                _q1187 = set((_q954[0] for _q954 in plan))
                _q455 = [xy for xy in rest + freed if xy not in _q1187 and xy in _q1168]
                _q1176 = sum((len(_q954[1]) for _q954 in plan if _q954[2]['kind'] != 'land'))
                _q435 = total - max(spent, float(_q1176))
                _q872 = int(_q435 // _q653) if _q435 > 0 else 0
                if _q455 and _q872 > 0 and slack:
                    _q587 = ex_route_ends(ex, 24 - hour)
                    anchor = {_q1221: _q587.get(_q1221, units[_q1221]) for _q1221 in slack}
                    _q1051 = dict(slack)
                    if len(_q455) > int(c['fill_cands']):
                        _q455.sort(key=lambda xy: (min((_dist(xy, a) for a in anchor.values())), xy[1], xy[0]))
                        _q455 = _q455[:int(c['fill_cands'])]
                    charged = {}
                    _q867 = 0
                    while _q872 > 0 and _q455 and (len(plan) < _q462):
                        best = None
                        for _q1221, a in anchor.items():
                            _q1092 = _q1051[_q1221]
                            if _q1092 < _q653:
                                continue
                            for xy in _q455:
                                _q530 = _dist(a, xy)
                                _q1175 = 3 if _q1168[xy] in ('weed', 'spent') else 2
                                cost = max(_q653, float(_q530 + _q1175)) if c['fill_charge_travel'] else _q653
                                if cost > _q1092:
                                    continue
                                k = (_q530, xy[1], xy[0], _q1221)
                                if best is None or k < best[0]:
                                    best = (k, _q1221, xy, cost)
                        if best is None:
                            break
                        _, _q1221, xy, cost = best
                        crop, why = _q1120.choose(day, rem, _q1242, wstar)
                        plan.append((xy, _q1120._chain(crop, _q1168[xy]), rec(xy, 'fill', crop, why, unit=_q1221, cost=cost)))
                        if why == 'quota':
                            rem[crop] -= 1
                        if crop == 'WHEAT':
                            _q1242 += 1
                        _q1051[_q1221] -= cost
                        charged[_q1221] = charged.get(_q1221, 0.0) + cost
                        anchor[_q1221] = xy
                        _q455.remove(xy)
                        _q872 -= 1
                        _q867 += 1
                    if _q867:
                        ps['fill_log'].append({'day': day, 'hour': hour, 'slack': dict(slack), 'total': total, 'pre_used': max(spent, float(_q1176)), 'n': _q867, 'charged': charged})
        return plan

def classify(S, acts):
    """[(cls, op, eff, target)] per unit - tools/tmp/sys_audit_lib.classify_turn on a FarmState (S = the observation
    before the step, acts = the final commands)."""
    tiles = S.tiles
    pos = S.units
    _q735 = S.inventories
    seeds = S.seeds
    day = S.day
    demand = {}
    for a in acts:
        if isinstance(a, list) and len(a) >= 2 and (a[0] == 'PLANT'):
            demand[a[1]] = demand.get(a[1], 0) + 1
    blocked = {c for c, n in demand.items() if n > int(seeds.get(c, 0) or 0)}
    _q1231 = set()
    _q946 = []
    for _q1221, a in enumerate(acts[:len(pos)]):
        if not isinstance(a, list) or not a:
            _q946.append(('pass', 'NONE', False, None))
            continue
        op = a[0]
        _q954 = (int(pos[_q1221][0]), int(pos[_q1221][1]))
        inv = _q735[_q1221] if _q1221 < len(_q735) else {}
        if op in MOVES:
            _q946.append(('move', 'MOVE', True, None))
            continue
        if op == 'PASS':
            _q946.append(('pass', 'PASS', False, None))
            continue
        _q369 = _q954 in ((4, 4), (5, 4), (4, 5), (5, 5))
        if op == 'PICKUP':
            _q946.append(('pickup', op, _q369, a[1] if len(a) > 1 else None))
            continue
        if op == 'DROP':
            _q946.append(('unload', op, _q369 and any((_q1233 > 0 for _q1233 in inv.values())), None))
            continue
        if op == 'PLACE' and len(a) > 1 and (a[1] not in ANIMALS):
            _q946.append(('unload', 'PLACE_SHED', _q369 and inv.get(a[1], 0) > 0, a[1]))
            continue
        x, _q1272 = _q954
        t = tiles[_q1272][x]
        _q736 = isinstance(t, dict)
        kind = t.get('kind') if _q736 else None
        _q1193 = t.get('crop') or t.get('animal') or kind if _q736 else 'LOCKED' if t == 'LOCKED' else None
        key = (_q954, op)
        eff = False
        if t != 'LOCKED' and key not in _q1231:
            if op == 'WATER':
                eff = kind == 'PLANT' and (not t.get('watered_today'))
            elif op == 'HARVEST':
                eff = _q736 and t.get('yield_units', 0) > 0 and (bool(t.get('animal')) or (kind == 'PLANT' and day - t.get('planted_day', day) >= FYD.get(t.get('crop'), 99)))
            elif op == 'FEED':
                eff = _q736 and bool(t.get('animal')) and (not t.get('fed_today')) and (inv.get('WHEAT', 0) > 0)
            elif op == 'CARE':
                eff = _q736 and bool(t.get('animal')) and (not t.get('cared_today'))
            elif op == 'COLLECT_FERTILIZER':
                eff = _q736 and bool(t.get('animal')) and bool(t.get('fertilizer_available'))
            elif op == 'FERTILIZE':
                eff = kind == 'PLANT' and inv.get('FERTILIZER', 0) > 0
            elif op == 'PLANT':
                eff = t is None and len(a) > 1 and (a[1] not in blocked) and (int(seeds.get(a[1], 0) or 0) > 0)
                _q1193 = a[1] if len(a) > 1 else None
            elif op == 'DIG':
                eff = t is not None and (not (_q736 and t.get('animal')))
            elif op in BUILD_OPS:
                eff = t is None
            elif op == 'PLACE':
                eff = _q736 and kind == STRUCT.get(a[1]) and (not t.get('animal')) and (inv.get(a[1], 0) > 0)
                _q1193 = a[1]
        if eff:
            _q1231.add(key)
        _q946.append(('prod' if op in TILE_OPS or op == 'PLACE' else 'other', op, eff, _q1193))
    return _q946

def _new_day_rec():
    return {'steps': 0, 'hours': [0] * 24, 'unit_turns': 0, 'units_max': 0, 'pass': 0, 'pass_h': [0] * 24, 'busy': 0, 'eff': 0, 'noeff': 0, 'eff_op': {}, 'moves': 0, 'pickups': 0, 'unloads': 0, 'plant_h': [0] * 24, 'seed_blocked': 0, 'pool_seen_h12': 0, 'pool_steps_h12': 0, 'pool_tight_h12': 0, 'missed': None, 'missed_op': {}, 'rp_jobs': 0, 'rp_ops': 0, 'rp_crop': {}, 'rp_kind': {}, 'hires': 0}

class Ledger:

    def __init__(_q1120, cfg=None):
        _q1120.cfg = dict(LEDGER_CFG)
        _q1120.cfg.update(cfg or {})
        _q1120.days = {}
        _q1120.errors = 0
        _q1120.last_error = ''
        _q1120.ms_max = 0.0

    def rec(_q1120, day):
        _q1036 = _q1120.days.get(int(day))
        if _q1036 is None:
            _q1036 = _q1120.days[int(day)] = _new_day_rec()
        return _q1036

    def day(_q1120, _q530):
        return _q1120.days.get(int(_q530))

    def step(_q1120, S, acts, pool_n=None, pending=None, rp_added=None, seed_blocked=None):
        """One step: S = FarmState before the step, acts = the final commands, pool_n = len(ex.pool) after the act,
        pending = ex.pending_ops() after the act (read at hour 23 as the missed ops), rp_added = this step's
        Replanter result (list of (xy, chain)) or a job count.  seed_blocked (review fix; None = count the PLANTs of
        the final commands beyond the seeds held): the PLANTs the caller's seed guard turned into PASS this step - the
        final commands never exceed the seeds once a guard ran, so the default count is always 0 behind pd_layer's
        _pd_guard_plants.  Returns the classification (or None on error)."""
        t0 = time.perf_counter()
        try:
            acts = [list(a) if isinstance(a, (list, tuple)) else a for a in acts or []]
            _q491 = classify(S, acts)
            demand = {}
            for a in acts:
                if isinstance(a, list) and len(a) >= 2 and (a[0] == 'PLANT'):
                    demand[a[1]] = demand.get(a[1], 0) + 1
            _q1108 = sum((n for c, n in demand.items() if n > int(S.seeds.get(c, 0) or 0)))
            if seed_blocked is not None:
                _q1108 = int(seed_blocked)
            _q1120.step_cls(int(S.day), int(S.hour), _q491, pool_n=pool_n, pending=pending, rp_added=rp_added, seed_blocked=_q1108, hires=int(getattr(S, 'hires_today', 0) or 0))
        except Exception as _q575:
            _q1120.errors += 1
            _q1120.last_error = repr(_q575)[:240]
            _q491 = None
        ms = 1000.0 * (time.perf_counter() - t0)
        if ms > _q1120.ms_max:
            _q1120.ms_max = ms
        return _q491

    def step_cls(_q1120, day, hour, _q491, pool_n=None, pending=None, rp_added=None, seed_blocked=0, hires=None):
        """The accumulation part of step() for a precomputed classification (e.g. sys_audit_games rows)."""
        _q1036 = _q1120.rec(day)
        _q1036['steps'] += 1
        if 0 <= hour < 24:
            _q1036['hours'][hour] += 1
        n = len(_q491)
        _q1036['unit_turns'] += n
        if n > _q1036['units_max']:
            _q1036['units_max'] = n
        if hires is not None:
            _q1036['hires'] = max(_q1036['hires'], int(hires))
        for c, op, eff, _q1193 in _q491:
            if c == 'pass':
                _q1036['pass'] += 1
                _q1036['pass_h'][hour] += 1
                continue
            _q1036['busy'] += 1
            if c == 'prod':
                if eff:
                    _q1036['eff'] += 1
                    _q1036['eff_op'][op] = _q1036['eff_op'].get(op, 0) + 1
                    if op == 'PLANT':
                        _q1036['plant_h'][hour] += 1
                else:
                    _q1036['noeff'] += 1
            elif c == 'move':
                _q1036['moves'] += 1
            elif c == 'pickup':
                _q1036['pickups'] += 1
            elif c == 'unload':
                _q1036['unloads'] += 1
        _q1036['seed_blocked'] += int(seed_blocked or 0)
        if pool_n is not None and hour >= int(_q1120.cfg['pool_h']):
            _q1036['pool_seen_h12'] += 1
            if int(pool_n) > 0:
                _q1036['pool_steps_h12'] += 1
                if not any((x[0] == 'pass' for x in _q491)):
                    _q1036['pool_tight_h12'] += 1
        if hour == 23 and pending is not None:
            _q1120._missed(_q1036, pending)
        if rp_added:
            _q1120.note_replant(day, rp_added)

    def _missed(_q1120, _q1036, pending):
        _q1135 = _q1120.cfg['missed_skip']
        _q844 = {k: int(_q1233) for k, _q1233 in dict(pending).items() if _q1233 and k not in _q1135}
        _q1036['missed_op'] = _q844
        _q1036['missed'] = sum(_q844.values())

    def note_replant(_q1120, day, added):
        """Replanter additions: a list of (xy, chain) (or of Replanter log records) or a job count."""
        _q1036 = _q1120.rec(day)
        if isinstance(added, int):
            _q1036['rp_jobs'] += added
            return
        for item in added:
            if isinstance(item, dict):
                chain = [('PLANT', item.get('crop'))]
                crop, kind = (item.get('crop'), item.get('kind'))
            else:
                chain = item[1]
                crop = next((_q922[1] for _q922 in chain if _q922[0] == 'PLANT'), None)
                kind = None
            _q1036['rp_jobs'] += 1
            _q1036['rp_ops'] += len(chain)
            if crop:
                _q1036['rp_crop'][crop] = _q1036['rp_crop'].get(crop, 0) + 1
            if kind:
                _q1036['rp_kind'][kind] = _q1036['rp_kind'].get(kind, 0) + 1

    def end_day(_q1120, day, pending=None):
        """Close a day: the missed ops (pending ops left after its hour-23 act) if step() did not see hour 23."""
        _q1036 = _q1120.rec(day)
        if pending is not None and _q1036['missed'] is None:
            _q1120._missed(_q1036, pending)
        return _q1036

    def derived(_q1120, _q530):
        """C8 inputs of day d (None when the day was not seen)."""
        _q1036 = _q1120.days.get(int(_q530))
        if _q1036 is None:
            return None
        h0, h1 = LAB_CFG['cut_h']
        return {'day': int(_q530), 'complete': _q1036['steps'] >= 20, 'eff': _q1036['eff'], 'busy': _q1036['busy'], 'tpt': _q1036['busy'] / float(_q1036['eff']) if _q1036['eff'] else None, 'pass': _q1036['pass'], 'pass_h5_23': sum(_q1036['pass_h'][h0:h1 + 1]), 'pool_empty_h12': _q1036['pool_seen_h12'] > 0 and _q1036['pool_steps_h12'] == 0, 'pool_steps_h12': _q1036['pool_steps_h12'], 'pool_tight_h12': _q1036['pool_tight_h12'], 'pass_h12_23': sum(_q1036['pass_h'][int(_q1120.cfg['pool_h']):24]), 'missed': _q1036['missed'], 'rp_jobs': _q1036['rp_jobs'], 'rp_ops': _q1036['rp_ops'], 'unit_turns': _q1036['unit_turns'], 'units_max': _q1036['units_max'], 'plantings': sum(_q1036['plant_h']), 'plant_h19_22': sum(_q1036['plant_h'][19:23]), 'seed_blocked': _q1036['seed_blocked']}

def must_do_ops(S, chains):
    """Level-3-like ops in the chains when the task list is not given: roots (PLANT / BUILD / PLACE), the HARVEST /
    DIG that clear a root's tile, the WATER after a PLANT, WATER on a plant that weeds tonight, FEED on an animal that
    escapes tonight, HARVEST of a decaying crop."""
    n = 0
    for k, _q481 in chains.items():
        xy = _xy(k)
        _q513 = S.crops.get(xy) if S is not None else None
        _q388 = S.animals.get(xy) if S is not None else None
        ops = [_q922[0] for _q922 in _q481]
        root = any((op in ('PLANT', 'PLACE') or op in BUILD_OPS for op in ops))
        planted = False
        for op in ops:
            if op in ('PLANT', 'PLACE') or op in BUILD_OPS:
                n += 1
                planted = planted or op == 'PLANT'
            elif op == 'DIG' and root:
                n += 1
            elif op == 'HARVEST' and (root or (_q513 is not None and _q513.decaying)):
                n += 1
            elif op == 'WATER' and (planted or (_q513 is not None and _q513.must_water)):
                n += 1
            elif op == 'FEED' and _q388 is not None and _q388.must_feed:
                n += 1
    return n

class Labour:

    def __init__(_q1120, cfg=None):
        _q1120.cfg = dict(LAB_CFG)
        _q1120.cfg.update(cfg or {})
        _q1120.tpt = float(_q1120.cfg['tpt0'])
        _q1120.seen = set()
        _q1120.last = {}
        _q1120.history = []
        _q1120.errors = 0
        _q1120.last_error = ''

    def update(_q1120, ledger, day):
        """EMA of realised busy turns per effective op over the finished days before `day` not yet used."""
        c = _q1120.cfg
        if not c['ema'] or ledger is None:
            return _q1120.tpt
        for _q530 in sorted(ledger.days):
            if _q530 >= day or _q530 in _q1120.seen or _q530 < int(c['ema_from_day']):
                continue
            _q572 = ledger.derived(_q530)
            if _q572 is None or not _q572['complete']:
                continue
            _q1120.seen.add(_q530)
            if _q572['eff'] < int(c['min_eff']) or _q572['tpt'] is None:
                continue
            a = float(c['alpha'])
            _q1120.tpt = min(float(c['tpt_hi']), max(float(c['tpt_lo']), (1 - a) * _q1120.tpt + a * _q572['tpt']))
        return _q1120.tpt

    def feedback(_q1120, ledger, day):
        """(+1 / -1 / 0, why) from yesterday's Ledger day."""
        c = _q1120.cfg
        if not c['fb'] or ledger is None:
            return (0, '')
        _q572 = ledger.derived(day - 1)
        if _q572 is None or not _q572['complete']:
            return (0, '')
        if c['add_tight']:
            _q840 = _q572['missed'] is not None and _q572['missed'] > int(c['add_missed']) and (_q572['pass_h12_23'] <= int(c['cut_pass']))
            pool = _q572['pool_tight_h12'] >= int(c['add_pool_steps'])
        else:
            _q840 = _q572['missed'] is not None and _q572['missed'] > int(c['add_missed'])
            pool = _q572['pool_steps_h12'] >= int(c['add_pool_steps'])
        if _q840 or pool:
            return (1, 'missed %s pool %d' % (_q572['missed'], _q572['pool_steps_h12']))
        h0, h1 = c['cut_h']
        _q1036 = ledger.day(day - 1)
        _q986 = sum(_q1036['pass_h'][h0:h1 + 1])
        if _q986 > int(c['cut_pass']) and _q572['pool_empty_h12']:
            return (-1, 'pass %d' % _q986)
        return (0, '')

    def hires(_q1120, S, chains, ledger, day, tasks=None, n_l3=None):
        """(n_h0, n_h1) HIRE orders for today, or None (not decided here: other days / error)."""
        try:
            return _q1120._hires(S, chains, ledger, int(day), tasks, n_l3)
        except Exception as _q575:
            _q1120.errors += 1
            _q1120.last_error = ('%s %s' % (day, repr(_q575)))[:240]
            return None

    def _hires(_q1120, S, chains, ledger, day, tasks, n_l3):
        c = _q1120.cfg
        if not c['days'][0] <= day <= c['days'][1]:
            return None
        tpt = _q1120.update(ledger, day)
        ops = sum((len(_q481) for _q481 in (chains or {}).values()))
        rp_prev = 0
        if ledger is not None:
            _q1277 = ledger.day(day - 1)
            if _q1277 is not None:
                rp_prev = int(_q1277['rp_jobs'])
        load = ops + rp_prev * float(c['rp_ops'])
        lo, hi = (int(c['lo']), int(c['hi']))
        base = int(math.ceil(max(0.0, load * tpt - float(c['far'])) / float(c['hand'])))
        h = max(lo, min(hi, base))
        fb, why = _q1120.feedback(ledger, day)
        _q682 = h + fb
        if not c['fb_below_lo']:
            _q682 = max(lo, _q682)
        _q682 = min(hi, _q682)
        if n_l3 is None:
            if tasks is not None:
                n_l3 = sum((1 for t in tasks if getattr(t, 'level', 0) >= 3))
            else:
                n_l3 = must_do_ops(S, chains or {})
        floor = min(hi, int(math.ceil(float(n_l3) * float(c['floor_tpt']) / float(c['hand']))))
        _q682 = max(_q682, floor)
        done = int(getattr(S, 'hires_today', 0) or 0) if S is not None else 0
        n = max(0, _q682 - done)
        _q854 = min(n, int(c['h0_max']))
        _q1120.last = {'day': day, 'ops': ops, 'rp_prev': rp_prev, 'load': load, 'tpt': round(tpt, 3), 'base': base, 'fb': fb, 'fb_why': why, 'n_l3': n_l3, 'floor': floor, 'hands': _q682, 'n_h0': _q854, 'n_h1': n - _q854}
        _q1120.history.append(_q1120.last)
        return (_q854, n - _q854)