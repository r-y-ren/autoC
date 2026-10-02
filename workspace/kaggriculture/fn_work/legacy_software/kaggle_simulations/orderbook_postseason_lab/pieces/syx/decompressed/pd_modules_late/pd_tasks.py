"""PD - due tile/animal tasks of the day (Original work, Shawn404, 25 Sep 2026).

due_tasks(state, plan=None) -> [Task]: every tile command worth doing today on our farm, derived from the farm state
(crop needs, harvest windows, fertiliser ages, animal feed/care/collect/harvest, weeds, spent plants) plus the day plan
(plantings, builds, placements, clears, land purchases).  Pure Python, no engine import.

Each Task has
  op, xy, arg      the unit command ([op] or [op, arg]) to issue while standing on xy
  need             item the unit must carry ('WHEAT' for FEED, 'FERTILIZER' for FERTILIZE, the animal for PLACE)
  level            3 = critical (plant weeds / animal escapes / root of the plan or a root's precondition)
                   2 = productive (adds units or money today or tonight)
                   1 = optional (legal and harmless but worth little today, e.g. a keep-alive WATER one day early)
  value            rough $ value of doing it today rather than never (for ranking; not a forecast)
  deadline         last hour (0-23) at which it still pays in full (23 = any time today)
  not_before       first hour it can be done (tiles of a quadrant bought today: purchase hour + 1)
  root             True for PLANT / BUILD_* / PLACE (their omission cascades into the next days' tasks)
  after            index (into the returned list) of the task that must be done first on the same tile, or None
  src              'state' or 'plan'
Tasks of one tile are consecutive and in execution order.

Plan format (all keys optional; pd_plan.plan_day returns this shape):
  {'ops':  [(op, (x, y), arg), ...]   op in PLANT (arg crop), BUILD_COOP, BUILD_PASTURE, PLACE (arg animal), CLEAR,
                                      in the order they should happen on each tile,
   'land': [(hour, quadrant), ...]    BUY_LAND orders today,
   'fert_wheat': bool                 R5: fertilise wheat (default: fertiliser quote <= 55),
   'no_water_days': int               skip keep-alive waters on crops whose harvest is past (default 0),
   'fert_prod_only': bool             M2 fix: an ongoing crop is fertilised only on a production day not yet covered
                                      (cr.prod_tonight and cr.fert_until < day): one FERTILIZE covers its day and the
                                      next two, so strawberries need ages 9 / 13 and tomatoes 7 / 10 (default False =
                                      as soon as one uncovered production falls in the next three days),
   'glut': set of animal products     M2 fix: glutted product (the quote after our stock < feed cost of a care-bonus
                                      unit): its animals are fed only when they would escape tonight (every other day)
                                      and get no CARE (production is 1 unit per production day fed or not),
   'hold_harvest': set of products    M2 fix: product quoted near the floor: its animals' HARVEST drops to level 1 (not
                                      scheduled; the units wait on the animal) except on the final day,
   'fert_age2': bool                  CS B1 (27 Sep): WHEAT / CARROT get their FERTILIZE at age 2 only - level 2 at age
                                      2 (m >= 1; wheat still behind fert_wheat), level 1 at every other age - and at
                                      age 2 it comes BEFORE the day's WATER in the tile's order (the engine adds +2 only
                                      to a WATER made while the fertiliser is active: DSM 4.97 u at an age-3 cut).
                                      DSM: 79% of first wheat applications / 82% of carrot ones at age 2 (default False),
   'wheat_h3': bool                   CS B1: a fertilised (fert_until >= day) age-3 WHEAT is ripe - its HARVEST is level
                                      2 instead of 1 (DSM cuts fertilised wheat at age 3: 4.97 u, 1.66 u per tile-day vs
                                      5.81 / 4 = 1.45 at age 4) (default False),
   'end_husb': bool                   R1(b) end game: husbandry only while a production at a refresh <= FINAL_DAY - 1
                                      (the last refresh the game plays) can still pay it - CARE only if the production
                                      that pays today's bank (tonight's +1 is consumed at the NEXT production after
                                      tonight's) comes by then; level-2 FEED only if it releases a bank tonight or banks
                                      a paying CARE; a must-feed FEED is dropped when no production remains (the escape
                                      loses nothing: held units are harvested today at level 2, and the FEED stays when
                                      the fertiliser the survival keeps is worth the wheat) (default False),
   'glut_care_fed': tuple of animals  R5: glutted animals of these kinds (e.g. ('SHEEP',)) still get their CARE (level 2,
                                      after the FEED) when they are fed today anyway (already fed, or a level-3 FEED is
                                      scheduled): one command on the tile, no wheat (default () = no CARE in glut),
   'care_full': bool                  P8 R2 (28 Sep): on non-glut days every SHEEP / COW whose CARE pays (the production
                                      that pays today's bank comes at a refresh <= FINAL_DAY - 1) gets its CARE at level
                                      3, chained right after the day's FEED, and that FEED is raised to level 3 with it
                                      (the engine banks a CARE only on a fed day, and pays the bank only on a FED
                                      production day - a level-3 CARE on an unfed animal is worth nothing).  The pair
                                      shares one level, so the plan's hire model counts it in full (the planner did 272
                                      CAREs / game vs the tape's 351, wool 0.92 vs 1.08 per sheep-day).  Not husb_crit:
                                      that raises only the bank-release FEED (and the CARE riding it); care_full raises
                                      the CARE of every fed day and only where it pays; geese and glut days untouched
                                      (default False),
   'fert_wheat_px': float or None     P8 (28 Sep): no FERTILIZE task at all on WHEAT tiles (state or planting-day) while
                                      the observation's fertiliser quote is above this - the unit sells instead (the
                                      anti-DSM fertiliser undercut); fert_wheat only drops them to level 1 (default None
                                      = off)}
"""
from pd_state import CROPS, ANIMALS, FINAL_DAY, quadrant_of
OPS_TILE = ('PLANT', 'WATER', 'HARVEST', 'FERTILIZE', 'FEED', 'CARE', 'COLLECT_FERTILIZER', 'DIG', 'BUILD_PASTURE', 'BUILD_COOP', 'PLACE')
ROOT_OPS = ('PLANT', 'BUILD_PASTURE', 'BUILD_COOP', 'PLACE')
STRUCT_OF = {'GOOSE': 'COOP', 'COW': 'PASTURE', 'SHEEP': 'PASTURE'}
PROD_OF = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}
UNITS_PER_PLANTING = {'WHEAT': 5.5, 'CARROT': 3.6, 'TOMATO': 7.0, 'STRAWBERRY': 7.4, 'MELON': 6.0}

class Task:
    __slots__ = ('op', 'xy', 'arg', 'need', 'level', 'value', 'deadline', 'not_before', 'root', 'after', 'src', 'why')

    def __init__(_q1120, op, xy, arg=None, need=None, level=2, value=0.0, deadline=23, not_before=0, after=None, src='state', why=''):
        _q1120.op = op
        _q1120.xy = xy
        _q1120.arg = arg
        _q1120.need = need
        _q1120.level = level
        _q1120.value = float(value)
        _q1120.deadline = deadline
        _q1120.not_before = not_before
        _q1120.root = op in ROOT_OPS
        _q1120.after = after
        _q1120.src = src
        _q1120.why = why

    def command(_q1120):
        return [_q1120.op, _q1120.arg] if _q1120.arg is not None else [_q1120.op]

    def __repr__(_q1120):
        a = ' ' + str(_q1120.arg) if _q1120.arg else ''
        return f'<{_q1120.op}{a} @{_q1120.xy} L{_q1120.level} ${_q1120.value:.0f} <=h{_q1120.deadline} {_q1120.why}>'

def _px(state, item):
    try:
        return float(state.prices.get(item, 0)) or 1.0
    except AttributeError:
        return 1.0

def _future_units(_q513, day):
    """Units this plant will still deliver (current + future productions), DSM husbandry."""
    _q474 = CROPS[_q513.crop]
    if _q513.ongoing:
        return _q513.units + 1.75 * _q513.prods_left
    if _q513.decaying:
        return max(0, _q513.units - 1)
    _q800 = max(0, min(_q474['myd'], FINAL_DAY - _q513.planted_day) - max(_q513.age, (_q474['myd'] + 1) // 2) + 1)
    return min(_q474['max_yield'], _q513.units + _q800 * 1.5)
_OPTS = {'melon_h10': False, 'fert_age2': False, 'wheat_h3': False, 'fert_water': False, 'end_husb': False, 'glut_care_fed': (), 'care_full': False, 'fert_wheat_px': None, 'husb_q': None, 'keep_alive2': (), 'husb_crit': False}

def _fert_marginal(_q513, day):
    """Extra units from a FERTILIZE today (active day..day+2), assuming the plant is watered on its yield days."""
    _q474 = CROPS[_q513.crop]
    _q786 = _q474['fyd'] if _OPTS.get('melon_h10') and _q513.crop == 'MELON' else _q474['myd']
    _q594 = []
    if _q513.ongoing:
        _q629 = _q474['fyd'] - 1
        _q741 = _q474['interval']
        _q785 = _q629 + _q741 * (_q474['max_yield'] - 1)
        for _q530 in (day, day + 1, day + 2):
            a = _q530 - _q513.planted_day
            if _q629 <= a <= _q785 and (a - _q629) % _q741 == 0 and (_q530 < FINAL_DAY) and (_q530 > _q513.fert_until):
                _q594.append(_q530)
        return float(len(_q594))
    _q1265 = (_q474['myd'] + 1) // 2
    _q510 = 0
    _q1224 = 0
    for _q530 in range(day, min(_q513.planted_day + _q786, FINAL_DAY) + 1):
        a = _q530 - _q513.planted_day
        if a < _q1265:
            continue
        if _q530 == day and _q513.watered:
            continue
        if _q530 <= _q513.fert_until:
            _q510 += 1
        elif _q530 <= day + 2:
            _q1224 += 1
    rest = 0
    for _q530 in range(day + 3, min(_q513.planted_day + _q786, FINAL_DAY) + 1):
        if _q530 - _q513.planted_day >= _q1265 and _q530 > _q513.fert_until:
            rest += 1
    base = _q513.units + 2 * _q510
    _q1258 = min(_q474['max_yield'], base + _q1224 + rest)
    _q1256 = min(_q474['max_yield'], base + 2 * _q1224 + rest)
    return float(max(0, _q1256 - _q1258))

def _no_fert(state, crop):
    """P8 fert_wheat_px: no FERTILIZE on this crop today (WHEAT while the fertiliser quote is above the threshold)."""
    _q805 = _OPTS['fert_wheat_px']
    return _q805 is not None and crop == 'WHEAT' and (_px(state, 'FERTILIZER') > _q805)

def _decay_deadline(state, _q513):
    """Last hour a HARVEST still collects >= 1 unit of a decaying (or about to decay) non-ongoing/ongoing crop."""
    if _q513.mls < 0:
        return 23
    _q536 = 24 * state.day
    if _q513.mls > _q536 + 23:
        return 23
    _q1221 = _q513.units
    t = max(_q513.mls, state.step)
    if (t - _q513.mls) % 2:
        t += 1
    while _q1221 > 1 and t <= _q536 + 23:
        _q1221 -= 1
        t += 2
    return max(0, min(23, t - _q536))

class _TileSim:
    """Minimal virtual tile used to chain plan ops (what the tile will be after the ops generated so far)."""
    __slots__ = ('kind', 'crop', 'harv', 'ongoing', 'animal', 'struct', 'planted_today')

    def __init__(_q1120, state, xy):
        _q1120.kind = 'EMPTY'
        _q1120.crop = None
        _q1120.harv = False
        _q1120.ongoing = False
        _q1120.animal = None
        _q1120.struct = None
        _q1120.planted_today = False
        if xy in state.locked:
            _q1120.kind = 'LOCKED'
        elif xy in state.weeds:
            _q1120.kind = 'WEED'
        elif xy in state.crops:
            _q513 = state.crops[xy]
            _q1120.kind = 'PLANT'
            _q1120.crop = _q513.crop
            _q1120.harv = _q513.harvestable()
            _q1120.ongoing = _q513.ongoing
        elif xy in state.animals:
            _q1120.kind = 'STRUCT'
            _q1120.struct = state.animals[xy].kind
            _q1120.animal = state.animals[xy].animal
        elif xy in state.structures:
            _q1120.kind = 'STRUCT'
            _q1120.struct = state.structures[xy]

def due_tasks(state, plan=None):
    plan = plan or {}
    _OPTS['melon_h10'] = bool(plan.get('melon_h10', False))
    _OPTS['fert_age2'] = bool(plan.get('fert_age2', False))
    _OPTS['wheat_h3'] = bool(plan.get('wheat_h3', False))
    _OPTS['husb_crit'] = bool(plan.get('husb_crit', False))
    _OPTS['fert_water'] = bool(plan.get('fert_water', False))
    _OPTS['end_husb'] = bool(plan.get('end_husb', False))
    _OPTS['glut_care_fed'] = tuple(plan.get('glut_care_fed') or ())
    _OPTS['care_full'] = bool(plan.get('care_full', False))
    _q660 = plan.get('fert_wheat_px')
    _OPTS['fert_wheat_px'] = None if _q660 is None else float(_q660)
    _q706 = plan.get('husb_q')
    _OPTS['husb_q'] = None if _q706 is None else float(_q706)
    _OPTS['keep_alive2'] = tuple(plan.get('keep_alive2') or ())
    day = state.day
    tasks = []
    _q618 = _px(state, 'FERTILIZER')
    _q620 = min(_q618, 100.0) * 0.5
    fert_wheat = plan.get('fert_wheat', _q618 <= 55)
    _q641 = bool(plan.get('fert_prod_only', False))
    glut = plan.get('glut') or ()
    _q703 = plan.get('hold_harvest') or ()
    _q782 = {}
    for h, q in plan.get('land', ()):
        _q782.setdefault(q, h)
    _q990 = {}
    for op, xy, arg in plan.get('ops', ()):
        _q990.setdefault(tuple(xy), []).append((op, arg))

    def _q376(t):
        tasks.append(t)
        return len(tasks) - 1
    for xy, ops in _q990.items():
        _q1239 = _TileSim(state, xy)
        _q892 = 0
        if _q1239.kind == 'LOCKED':
            q = quadrant_of(*xy)
            if q not in _q782:
                continue
            _q892 = _q782[q] + 1
            _q1239.kind = 'EMPTY'
        _q513 = state.crops.get(xy)
        prev = None
        _q557 = False
        for op, arg in ops:
            if op == 'PLANT' and _q1239.kind == 'PLANT' and (_q1239.crop == arg) and (not _q1239.planted_today) and (_q513 is not None) and (_q513.planted_day == day):
                _q1239.planted_today = True
                _q557 = True
                continue
            if op in ('BUILD_COOP', 'BUILD_PASTURE') and _q1239.kind == 'STRUCT' and (_q1239.struct == ('COOP' if op == 'BUILD_COOP' else 'PASTURE')):
                continue
            if op == 'PLACE' and _q1239.kind == 'STRUCT' and (_q1239.animal == arg):
                continue
            if op == 'CLEAR' and (_q1239.kind == 'EMPTY' or (_q1239.kind == 'PLANT' and (not _q1239.planted_today) and (_q513 is not None) and (_q513.planted_day == day))):
                continue
            _q557 = False
            if op == 'CLEAR' or op in ('PLANT', 'BUILD_COOP', 'BUILD_PASTURE'):
                if _q1239.kind == 'PLANT':
                    if _q1239.harv and (not _q1239.planted_today) and (_q513 is not None) and (not _q513.ongoing) and (not _q513.watered) and (_q513.water_gain(day) > 0) and (op != 'CLEAR'):
                        prev = _q376(Task('WATER', xy, level=2, value=_q513.water_gain(day) * _px(state, _q513.crop), after=prev, not_before=_q892, src='plan', why='water before pre-root harvest'))
                    if _q1239.harv and (not _q1239.planted_today) and (_q513 is not None) and (_q513.units > 0):
                        prev = _q376(Task('HARVEST', xy, level=3, value=_q513.units * _px(state, _q513.crop), after=prev, not_before=_q892, src='plan', why='pre-root harvest'))
                        if not _q1239.ongoing:
                            _q1239.kind = 'EMPTY'
                    if _q1239.kind == 'PLANT':
                        prev = _q376(Task('DIG', xy, level=3, value=5, after=prev, not_before=_q892, src='plan', why='clear plant'))
                        _q1239.kind = 'EMPTY'
                elif _q1239.kind == 'WEED':
                    prev = _q376(Task('DIG', xy, level=3, value=5, after=prev, not_before=_q892, src='plan', why='clear weed'))
                    _q1239.kind = 'EMPTY'
                elif _q1239.kind == 'STRUCT':
                    if _q1239.animal:
                        break
                    prev = _q376(Task('DIG', xy, level=3, value=1, after=prev, not_before=_q892, src='plan', why='clear structure'))
                    _q1239.kind = 'EMPTY'
                _q1239.crop = None
                _q1239.harv = False
                _q1239.struct = None
                if op == 'CLEAR':
                    continue
            if op == 'PLANT':
                if _q1239.kind != 'EMPTY':
                    continue
                _q1233 = UNITS_PER_PLANTING.get(arg, 3) * _px(state, arg) - CROPS[arg]['seed']
                prev = _q376(Task('PLANT', xy, arg, level=3, value=max(_q1233, 1), after=prev, not_before=_q892, src='plan', why='plan'))
                prev = _q376(Task('WATER', xy, level=3, value=max(_q1233, 1), after=prev, not_before=_q892, src='plan', why='planting-day water'))
                if arg in ('WHEAT', 'CARROT') and (not _no_fert(state, arg)):
                    _q376(Task('FERTILIZE', xy, need='FERTILIZER', level=1, value=_px(state, arg) * 1.0 - _q620, after=prev, not_before=_q892, src='plan', why='early fertiliser'))
                _q1239.kind, _q1239.crop, _q1239.harv, _q1239.ongoing, _q1239.planted_today = ('PLANT', arg, False, CROPS[arg]['ongoing'], True)
            elif op in ('BUILD_COOP', 'BUILD_PASTURE'):
                if _q1239.kind != 'EMPTY':
                    continue
                prev = _q376(Task(op, xy, level=3, value=50, after=prev, not_before=_q892, src='plan', why='plan'))
                _q1239.kind, _q1239.struct, _q1239.animal = ('STRUCT', 'COOP' if op == 'BUILD_COOP' else 'PASTURE', None)
            elif op == 'PLACE':
                if _q1239.kind != 'STRUCT' or _q1239.animal or _q1239.struct != STRUCT_OF.get(arg):
                    continue
                _q1233 = ANIMALS[arg]['cost']
                prev = _q376(Task('PLACE', xy, arg, need=arg, level=3, value=_q1233, after=prev, not_before=_q892, src='plan', why='plan'))
                _q957 = _q376(Task('FEED', xy, need='WHEAT', level=2, value=_px(state, PROD_OF[arg]) * 0.5, after=prev, not_before=_q892, src='plan', why='placement-day feed (banks care)'))
                _q376(Task('CARE', xy, level=2, value=_px(state, PROD_OF[arg]) * 0.5, after=_q957, not_before=_q892, src='plan', why='placement-day care'))
                _q1239.animal = arg
        if _q557 and _q513 is not None:
            _crop_tasks(state, _q513, _q376, _q620, fert_wheat, _q641)
        if xy not in state.animals:
            continue
        _animal_tasks(state, state.animals[xy], _q376, glut, _q703)
    for xy, _q513 in state.crops.items():
        if xy in _q990:
            continue
        _crop_tasks(state, _q513, _q376, _q620, fert_wheat, _q641)
    for xy, _q388 in state.animals.items():
        if xy in _q990:
            continue
        _animal_tasks(state, _q388, _q376, glut, _q703)
    for xy in state.weeds:
        if xy in _q990:
            continue
        _q376(Task('DIG', xy, level=1, value=2, why='weed'))
    return tasks

def _crop_tasks(state, _q513, _q376, _q620, fert_wheat, fert_prod_only=False):
    day = state.day
    xy = _q513.xy
    px = _px(state, _q513.crop)
    _q474 = CROPS[_q513.crop]
    _q658 = _future_units(_q513, day)
    prev = None
    if _q513.decaying or (_q513.ongoing and _q513.prods_left == 0):
        if _q513.units > 0 and _q513.harvestable():
            prev = _q376(Task('HARVEST', xy, level=3 if _q513.decaying else 2, value=_q513.units * px, deadline=_decay_deadline(state, _q513), why='finished/decaying'))
        if _q513.ongoing:
            _q376(Task('DIG', xy, level=1, value=3, after=prev, why='spent plant'))
        elif not _q513.watered and (not (_q513.units > 0 and _q513.harvestable())):
            _q376(Task('WATER', xy, level=1, value=0, why='keep-alive (decaying)'))
        return
    _q603 = _OPTS['fert_age2'] and _q513.crop in ('WHEAT', 'CARROT')
    _q1010 = False
    _q914 = _no_fert(state, _q513.crop)
    if _q603 and (not _q914) and (_q513.age == 2) and (not _q513.watered) and (day <= FINAL_DAY - 1) and (_q513.fert_until < day + 2):
        m = _fert_marginal(_q513, day)
        if m >= 1 and (_q513.crop != 'WHEAT' or fert_wheat):
            prev = _q376(Task('FERTILIZE', xy, need='FERTILIZER', level=2, value=m * px - _q620, why='+%.0fu age 2' % m))
            _q1010 = True
    if not _q513.watered:
        g = _q513.water_gain(day)
        if g <= 0 and _OPTS['fert_water'] and _q513.ongoing and _q513.prod_tonight and (_q513.fert_until < day) and (not _q1010) and (day <= FINAL_DAY - 1) and (_fert_marginal(_q513, day) >= 1):
            g = max(0, min(_q474['max_yield'], _q513.units + 2) - min(_q474['max_yield'], _q513.units + 1))
        if _q513.must_water:
            prev = _q376(Task('WATER', xy, level=3, value=max(_q658 * px, 1), after=prev, why='weeds tonight if dry'))
        elif g > 0:
            prev = _q376(Task('WATER', xy, level=2, value=g * px, after=prev, why='yield window' if not _q513.ongoing else 'fertiliser bonus tonight'))
        elif _q513.crop in _OPTS.get('keep_alive2', ()) and _q513.cu == 0 and (day <= FINAL_DAY - 1):
            prev = _q376(Task('WATER', xy, level=2, value=0.1 * px, after=prev, why='keep-alive (takeover)'))
        else:
            prev = _q376(Task('WATER', xy, level=1, value=0.1 * px, after=prev, why='keep-alive'))
    if not _q1010 and (not _q914) and (day <= FINAL_DAY - 1) and (_q513.fert_until < day + 2):
        if fert_prod_only and _q513.ongoing and (not (_q513.prod_tonight and _q513.fert_until < day)):
            m = 0.0
        else:
            m = _fert_marginal(_q513, day)
        if m > 0:
            _q1233 = m * px - _q620
            _q820 = 2 if m >= 1 and (_q513.crop != 'WHEAT' or fert_wheat) else 1
            if _q603 and _q513.age != 2:
                _q820 = 1
            _q376(Task('FERTILIZE', xy, need='FERTILIZER', level=_q820, value=_q1233, why='+%.0fu' % m))
    if _q513.units > 0 and _q513.harvestable():
        if _q513.ongoing:
            _q1245 = _q513.prod_tonight and _q513.units + (2 if _q513.fert_until >= day else 1) > _q474['max_yield']
            _q376(Task('HARVEST', xy, level=2, value=_q513.units * px, deadline=23, why='waste tonight' if _q1245 else 'units ready'))
        else:
            g = _q513.water_gain(day)
            _q379 = _q513.units + g
            ripe = _q513.age >= _q474['myd'] or _q379 >= _q474['max_yield'] or day >= FINAL_DAY or (_q513.mls >= 0 and _q513.mls <= 24 * day + 23)
            if not ripe and _OPTS['wheat_h3'] and (_q513.crop == 'WHEAT') and (_q513.age == 3) and (_q513.fert_until >= day):
                ripe = True
            _q376(Task('HARVEST', xy, level=2 if ripe else 1, value=_q379 * px, deadline=_decay_deadline(state, _q513), after=prev if g > 0 else None, why='ripe' if ripe else 'early harvest'))

def _animal_tasks(state, _q388, _q376, glut=(), hold_harvest=()):
    xy = _q388.xy
    _q1008 = _px(state, _q388.product)
    _q375 = ANIMALS[_q388.animal]
    g = _q388.product in glut
    day = state.day
    end = _OPTS['end_husb']
    if end:
        _q973 = day + (_q375['interval'] if _q388.prod_tonight else _q388.next_prod_in)
        _q467 = _q973 <= FINAL_DAY - 1
        _q1020 = day + _q388.next_prod_in <= FINAL_DAY - 1
        _q866 = sum((1 for _q530 in (day + 1, day + 2) if _q530 <= FINAL_DAY))
        _q763 = _q866 * min(_px(state, 'FERTILIZER'), 100.0) * 0.5 >= _px(state, 'WHEAT')
        _q562 = _q388.must_feed and (not _q1020) and (not _q763)
    else:
        _q467 = True
        _q562 = False
    if _q388.units > 0:
        _q1245 = _q388.prod_tonight and _q388.units + 1 + _q388.bank > _q375['max_held']
        _q820 = 1 if _q388.product in hold_harvest and day < FINAL_DAY and (not _q562) else 2
        _q376(Task('HARVEST', xy, level=_q820, value=_q388.units * _q1008, why='escapes tonight (end)' if _q562 else 'waste tonight' if _q1245 else 'units ready'))
    if _q388.fert_avail:
        _q376(Task('COLLECT_FERTILIZER', xy, level=2, value=_px(state, 'FERTILIZER') * 0.6, why='fertiliser'))
    prev = None
    crit = _OPTS['husb_crit']
    _q615 = False
    cf = _OPTS['care_full'] and (not g) and (_q388.animal in ('SHEEP', 'COW')) and (day < FINAL_DAY) and _q467 and (day + (_q375['interval'] if _q388.prod_tonight else _q388.next_prod_in) <= FINAL_DAY - 1)
    if not _q388.fed:
        if _q388.must_feed:
            if not _q562:
                prev = _q376(Task('FEED', xy, need='WHEAT', level=3, value=_q375['cost'] + _q1008, why='escapes tonight if unfed'))
                _q615 = True
        elif crit and _q388.prod_tonight and (_q388.bank > 0):
            prev = _q376(Task('FEED', xy, need='WHEAT', level=3, value=_q1008 * (1 + _q388.bank), why='releases care bank tonight (crit)'))
            _q615 = True
        elif _OPTS['husb_q'] is not None and (not g) and _q388.prod_tonight and (_q1008 >= _OPTS['husb_q']) and (not end or _q467 or _q388.bank > 0):
            prev = _q376(Task('FEED', xy, need='WHEAT', level=3, value=_q1008 * (1 + _q388.bank), why='production tonight (husb_q)'))
            _q615 = True
        elif not g and (not end or (_q388.prod_tonight and _q388.bank > 0) or _q467):
            why = 'releases care bank tonight' if _q388.prod_tonight and _q388.bank > 0 else 'banks care bonus'
            prev = _q376(Task('FEED', xy, need='WHEAT', level=3 if cf else 2, value=_q1008 * (1 + (_q388.bank if _q388.prod_tonight else 0)), why=why + (' (care_full)' if cf else '')))
            _q615 = _q615 or cf
    if not _q388.cared and day < FINAL_DAY and _q467:
        if g:
            if _q388.animal in _OPTS['glut_care_fed'] and (_q388.fed or _q615):
                _q376(Task('CARE', xy, level=2, value=_q1008 * 0.9, after=prev, why='+1 unit at next production (glut, fed)'))
        elif cf and (_q388.fed or _q615):
            _q376(Task('CARE', xy, level=3, value=_q1008 * 0.9, after=prev, why='+1 unit at next production (care_full)'))
        elif (crit or _OPTS['husb_q'] is not None) and _q615:
            _q376(Task('CARE', xy, level=3, value=_q1008 * 0.9, after=prev, why='+1 unit at next production (crit, with FEED)'))
        else:
            _q376(Task('CARE', xy, level=2, value=_q1008 * 0.9, why='+1 unit at next production (if fed)'))

def task_turns(tasks, _q837=2, _q846=1.25, _q767=2, n_units=1):
    """Rough unit-turns to do the tasks of level >= min_level (plus all roots and their chains): one turn per command,
    walking ~move_per_task per task (clustered farm), kit pickups per unit."""
    n = sum((1 for t in tasks if t.level >= _q837 or t.src == 'plan'))
    return int(round(n * (1.0 + _q846) + _q767 * n_units))

def needs(tasks, _q837=2):
    """Items the day's tasks consume: {'WHEAT': feeds, 'FERTILIZER': fertilisations, animal: placements}."""
    _q946 = {}
    for t in tasks:
        if t.need and (t.level >= _q837 or t.src == 'plan'):
            _q946[t.need] = _q946.get(t.need, 0) + 1
    return _q946