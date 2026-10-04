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

    def __init__(_q1052, op, xy, arg=None, need=None, level=2, value=0.0, deadline=23, not_before=0, after=None, src='state', why=''):
        _q1052.op = op
        _q1052.xy = xy
        _q1052.arg = arg
        _q1052.need = need
        _q1052.level = level
        _q1052.value = float(value)
        _q1052.deadline = deadline
        _q1052.not_before = not_before
        _q1052.root = op in ROOT_OPS
        _q1052.after = after
        _q1052.src = src
        _q1052.why = why

    def command(_q1052):
        return [_q1052.op, _q1052.arg] if _q1052.arg is not None else [_q1052.op]

    def __repr__(_q1052):
        a = ' ' + str(_q1052.arg) if _q1052.arg else ''
        return f'<{_q1052.op}{a} @{_q1052.xy} L{_q1052.level} ${_q1052.value:.0f} <=h{_q1052.deadline} {_q1052.why}>'

def _px(state, item):
    try:
        return float(state.prices.get(item, 0)) or 1.0
    except AttributeError:
        return 1.0

def _future_units(_q458, day):
    """Units this plant will still deliver (current + future productions), DSM husbandry."""
    _q421 = CROPS[_q458.crop]
    if _q458.ongoing:
        return _q458.units + 1.75 * _q458.prods_left
    if _q458.decaying:
        return max(0, _q458.units - 1)
    _q738 = max(0, min(_q421['myd'], FINAL_DAY - _q458.planted_day) - max(_q458.age, (_q421['myd'] + 1) // 2) + 1)
    return min(_q421['max_yield'], _q458.units + _q738 * 1.5)
_OPTS = {'melon_h10': False, 'fert_age2': False, 'wheat_h3': False, 'fert_water': False, 'end_husb': False, 'glut_care_fed': (), 'care_full': False, 'fert_wheat_px': None, 'husb_q': None, 'keep_alive2': (), 'husb_crit': False}

def _fert_marginal(_q458, day):
    """Extra units from a FERTILIZE today (active day..day+2), assuming the plant is watered on its yield days."""
    _q421 = CROPS[_q458.crop]
    _q724 = _q421['fyd'] if _OPTS.get('melon_h10') and _q458.crop == 'MELON' else _q421['myd']
    _q539 = []
    if _q458.ongoing:
        _q574 = _q421['fyd'] - 1
        _q679 = _q421['interval']
        _q723 = _q574 + _q679 * (_q421['max_yield'] - 1)
        for _q475 in (day, day + 1, day + 2):
            a = _q475 - _q458.planted_day
            if _q574 <= a <= _q723 and (a - _q574) % _q679 == 0 and (_q475 < FINAL_DAY) and (_q475 > _q458.fert_until):
                _q539.append(_q475)
        return float(len(_q539))
    _q1190 = (_q421['myd'] + 1) // 2
    _q455 = 0
    _q1150 = 0
    for _q475 in range(day, min(_q458.planted_day + _q724, FINAL_DAY) + 1):
        a = _q475 - _q458.planted_day
        if a < _q1190:
            continue
        if _q475 == day and _q458.watered:
            continue
        if _q475 <= _q458.fert_until:
            _q455 += 1
        elif _q475 <= day + 2:
            _q1150 += 1
    rest = 0
    for _q475 in range(day + 3, min(_q458.planted_day + _q724, FINAL_DAY) + 1):
        if _q475 - _q458.planted_day >= _q1190 and _q475 > _q458.fert_until:
            rest += 1
    base = _q458.units + 2 * _q455
    _q1183 = min(_q421['max_yield'], base + _q1150 + rest)
    _q1181 = min(_q421['max_yield'], base + 2 * _q1150 + rest)
    return float(max(0, _q1181 - _q1183))

def _no_fert(state, crop):
    """P8 fert_wheat_px: no FERTILIZE on this crop today (WHEAT while the fertiliser quote is above the threshold)."""
    _q743 = _OPTS['fert_wheat_px']
    return _q743 is not None and crop == 'WHEAT' and (_px(state, 'FERTILIZER') > _q743)

def _decay_deadline(state, _q458):
    """Last hour a HARVEST still collects >= 1 unit of a decaying (or about to decay) non-ongoing/ongoing crop."""
    if _q458.mls < 0:
        return 23
    _q481 = 24 * state.day
    if _q458.mls > _q481 + 23:
        return 23
    _q1147 = _q458.units
    t = max(_q458.mls, state.step)
    if (t - _q458.mls) % 2:
        t += 1
    while _q1147 > 1 and t <= _q481 + 23:
        _q1147 -= 1
        t += 2
    return max(0, min(23, t - _q481))

class _TileSim:
    """Minimal virtual tile used to chain plan ops (what the tile will be after the ops generated so far)."""
    __slots__ = ('kind', 'crop', 'harv', 'ongoing', 'animal', 'struct', 'planted_today')

    def __init__(_q1052, state, xy):
        _q1052.kind = 'EMPTY'
        _q1052.crop = None
        _q1052.harv = False
        _q1052.ongoing = False
        _q1052.animal = None
        _q1052.struct = None
        _q1052.planted_today = False
        if xy in state.locked:
            _q1052.kind = 'LOCKED'
        elif xy in state.weeds:
            _q1052.kind = 'WEED'
        elif xy in state.crops:
            _q458 = state.crops[xy]
            _q1052.kind = 'PLANT'
            _q1052.crop = _q458.crop
            _q1052.harv = _q458.harvestable()
            _q1052.ongoing = _q458.ongoing
        elif xy in state.animals:
            _q1052.kind = 'STRUCT'
            _q1052.struct = state.animals[xy].kind
            _q1052.animal = state.animals[xy].animal
        elif xy in state.structures:
            _q1052.kind = 'STRUCT'
            _q1052.struct = state.structures[xy]

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
    _q604 = plan.get('fert_wheat_px')
    _OPTS['fert_wheat_px'] = None if _q604 is None else float(_q604)
    _q646 = plan.get('husb_q')
    _OPTS['husb_q'] = None if _q646 is None else float(_q646)
    _OPTS['keep_alive2'] = tuple(plan.get('keep_alive2') or ())
    day = state.day
    tasks = []
    _q563 = _px(state, 'FERTILIZER')
    _q565 = min(_q563, 100.0) * 0.5
    fert_wheat = plan.get('fert_wheat', _q563 <= 55)
    _q586 = bool(plan.get('fert_prod_only', False))
    glut = plan.get('glut') or ()
    _q643 = plan.get('hold_harvest') or ()
    _q720 = {}
    for h, q in plan.get('land', ()):
        _q720.setdefault(q, h)
    _q924 = {}
    for op, xy, arg in plan.get('ops', ()):
        _q924.setdefault(tuple(xy), []).append((op, arg))

    def _q324(t):
        tasks.append(t)
        return len(tasks) - 1
    for xy, ops in _q924.items():
        _q1164 = _TileSim(state, xy)
        _q828 = 0
        if _q1164.kind == 'LOCKED':
            q = quadrant_of(*xy)
            if q not in _q720:
                continue
            _q828 = _q720[q] + 1
            _q1164.kind = 'EMPTY'
        _q458 = state.crops.get(xy)
        _q947 = None
        _q502 = False
        for op, arg in ops:
            if op == 'PLANT' and _q1164.kind == 'PLANT' and (_q1164.crop == arg) and (not _q1164.planted_today) and (_q458 is not None) and (_q458.planted_day == day):
                _q1164.planted_today = True
                _q502 = True
                continue
            if op in ('BUILD_COOP', 'BUILD_PASTURE') and _q1164.kind == 'STRUCT' and (_q1164.struct == ('COOP' if op == 'BUILD_COOP' else 'PASTURE')):
                continue
            if op == 'PLACE' and _q1164.kind == 'STRUCT' and (_q1164.animal == arg):
                continue
            if op == 'CLEAR' and (_q1164.kind == 'EMPTY' or (_q1164.kind == 'PLANT' and (not _q1164.planted_today) and (_q458 is not None) and (_q458.planted_day == day))):
                continue
            _q502 = False
            if op == 'CLEAR' or op in ('PLANT', 'BUILD_COOP', 'BUILD_PASTURE'):
                if _q1164.kind == 'PLANT':
                    if _q1164.harv and (not _q1164.planted_today) and (_q458 is not None) and (not _q458.ongoing) and (not _q458.watered) and (_q458.water_gain(day) > 0) and (op != 'CLEAR'):
                        _q947 = _q324(Task('WATER', xy, level=2, value=_q458.water_gain(day) * _px(state, _q458.crop), after=_q947, not_before=_q828, src='plan', why='water before pre-root harvest'))
                    if _q1164.harv and (not _q1164.planted_today) and (_q458 is not None) and (_q458.units > 0):
                        _q947 = _q324(Task('HARVEST', xy, level=3, value=_q458.units * _px(state, _q458.crop), after=_q947, not_before=_q828, src='plan', why='pre-root harvest'))
                        if not _q1164.ongoing:
                            _q1164.kind = 'EMPTY'
                    if _q1164.kind == 'PLANT':
                        _q947 = _q324(Task('DIG', xy, level=3, value=5, after=_q947, not_before=_q828, src='plan', why='clear plant'))
                        _q1164.kind = 'EMPTY'
                elif _q1164.kind == 'WEED':
                    _q947 = _q324(Task('DIG', xy, level=3, value=5, after=_q947, not_before=_q828, src='plan', why='clear weed'))
                    _q1164.kind = 'EMPTY'
                elif _q1164.kind == 'STRUCT':
                    if _q1164.animal:
                        break
                    _q947 = _q324(Task('DIG', xy, level=3, value=1, after=_q947, not_before=_q828, src='plan', why='clear structure'))
                    _q1164.kind = 'EMPTY'
                _q1164.crop = None
                _q1164.harv = False
                _q1164.struct = None
                if op == 'CLEAR':
                    continue
            if op == 'PLANT':
                if _q1164.kind != 'EMPTY':
                    continue
                _q1159 = UNITS_PER_PLANTING.get(arg, 3) * _px(state, arg) - CROPS[arg]['seed']
                _q947 = _q324(Task('PLANT', xy, arg, level=3, value=max(_q1159, 1), after=_q947, not_before=_q828, src='plan', why='plan'))
                _q947 = _q324(Task('WATER', xy, level=3, value=max(_q1159, 1), after=_q947, not_before=_q828, src='plan', why='planting-day water'))
                if arg in ('WHEAT', 'CARROT') and (not _no_fert(state, arg)):
                    _q324(Task('FERTILIZE', xy, need='FERTILIZER', level=1, value=_px(state, arg) * 1.0 - _q565, after=_q947, not_before=_q828, src='plan', why='early fertiliser'))
                _q1164.kind, _q1164.crop, _q1164.harv, _q1164.ongoing, _q1164.planted_today = ('PLANT', arg, False, CROPS[arg]['ongoing'], True)
            elif op in ('BUILD_COOP', 'BUILD_PASTURE'):
                if _q1164.kind != 'EMPTY':
                    continue
                _q947 = _q324(Task(op, xy, level=3, value=50, after=_q947, not_before=_q828, src='plan', why='plan'))
                _q1164.kind, _q1164.struct, _q1164.animal = ('STRUCT', 'COOP' if op == 'BUILD_COOP' else 'PASTURE', None)
            elif op == 'PLACE':
                if _q1164.kind != 'STRUCT' or _q1164.animal or _q1164.struct != STRUCT_OF.get(arg):
                    continue
                _q1159 = ANIMALS[arg]['cost']
                _q947 = _q324(Task('PLACE', xy, arg, need=arg, level=3, value=_q1159, after=_q947, not_before=_q828, src='plan', why='plan'))
                _q891 = _q324(Task('FEED', xy, need='WHEAT', level=2, value=_px(state, PROD_OF[arg]) * 0.5, after=_q947, not_before=_q828, src='plan', why='placement-day feed (banks care)'))
                _q324(Task('CARE', xy, level=2, value=_px(state, PROD_OF[arg]) * 0.5, after=_q891, not_before=_q828, src='plan', why='placement-day care'))
                _q1164.animal = arg
        if _q502 and _q458 is not None:
            _crop_tasks(state, _q458, _q324, _q565, fert_wheat, _q586)
        if xy not in state.animals:
            continue
        _animal_tasks(state, state.animals[xy], _q324, glut, _q643)
    for xy, _q458 in state.crops.items():
        if xy in _q924:
            continue
        _crop_tasks(state, _q458, _q324, _q565, fert_wheat, _q586)
    for xy, _q336 in state.animals.items():
        if xy in _q924:
            continue
        _animal_tasks(state, _q336, _q324, glut, _q643)
    for xy in state.weeds:
        if xy in _q924:
            continue
        _q324(Task('DIG', xy, level=1, value=2, why='weed'))
    return tasks

def _crop_tasks(state, _q458, _q324, _q565, fert_wheat, fert_prod_only=False):
    day = state.day
    xy = _q458.xy
    px = _px(state, _q458.crop)
    _q421 = CROPS[_q458.crop]
    _q602 = _future_units(_q458, day)
    _q947 = None
    if _q458.decaying or (_q458.ongoing and _q458.prods_left == 0):
        if _q458.units > 0 and _q458.harvestable():
            _q947 = _q324(Task('HARVEST', xy, level=3 if _q458.decaying else 2, value=_q458.units * px, deadline=_decay_deadline(state, _q458), why='finished/decaying'))
        if _q458.ongoing:
            _q324(Task('DIG', xy, level=1, value=3, after=_q947, why='spent plant'))
        elif not _q458.watered and (not (_q458.units > 0 and _q458.harvestable())):
            _q324(Task('WATER', xy, level=1, value=0, why='keep-alive (decaying)'))
        return
    _q548 = _OPTS['fert_age2'] and _q458.crop in ('WHEAT', 'CARROT')
    _q943 = False
    _q850 = _no_fert(state, _q458.crop)
    if _q548 and (not _q850) and (_q458.age == 2) and (not _q458.watered) and (day <= FINAL_DAY - 1) and (_q458.fert_until < day + 2):
        m = _fert_marginal(_q458, day)
        if m >= 1 and (_q458.crop != 'WHEAT' or fert_wheat):
            _q947 = _q324(Task('FERTILIZE', xy, need='FERTILIZER', level=2, value=m * px - _q565, why='+%.0fu age 2' % m))
            _q943 = True
    if not _q458.watered:
        g = _q458.water_gain(day)
        if g <= 0 and _OPTS['fert_water'] and _q458.ongoing and _q458.prod_tonight and (_q458.fert_until < day) and (not _q943) and (day <= FINAL_DAY - 1) and (_fert_marginal(_q458, day) >= 1):
            g = max(0, min(_q421['max_yield'], _q458.units + 2) - min(_q421['max_yield'], _q458.units + 1))
        if _q458.must_water:
            _q947 = _q324(Task('WATER', xy, level=3, value=max(_q602 * px, 1), after=_q947, why='weeds tonight if dry'))
        elif g > 0:
            _q947 = _q324(Task('WATER', xy, level=2, value=g * px, after=_q947, why='yield window' if not _q458.ongoing else 'fertiliser bonus tonight'))
        elif _q458.crop in _OPTS.get('keep_alive2', ()) and _q458.cu == 0 and (day <= FINAL_DAY - 1):
            _q947 = _q324(Task('WATER', xy, level=2, value=0.1 * px, after=_q947, why='keep-alive (takeover)'))
        else:
            _q947 = _q324(Task('WATER', xy, level=1, value=0.1 * px, after=_q947, why='keep-alive'))
    if not _q943 and (not _q850) and (day <= FINAL_DAY - 1) and (_q458.fert_until < day + 2):
        if fert_prod_only and _q458.ongoing and (not (_q458.prod_tonight and _q458.fert_until < day)):
            m = 0.0
        else:
            m = _fert_marginal(_q458, day)
        if m > 0:
            _q1159 = m * px - _q565
            _q758 = 2 if m >= 1 and (_q458.crop != 'WHEAT' or fert_wheat) else 1
            if _q548 and _q458.age != 2:
                _q758 = 1
            _q324(Task('FERTILIZE', xy, need='FERTILIZER', level=_q758, value=_q1159, why='+%.0fu' % m))
    if _q458.units > 0 and _q458.harvestable():
        if _q458.ongoing:
            _q1170 = _q458.prod_tonight and _q458.units + (2 if _q458.fert_until >= day else 1) > _q421['max_yield']
            _q324(Task('HARVEST', xy, level=2, value=_q458.units * px, deadline=23, why='waste tonight' if _q1170 else 'units ready'))
        else:
            g = _q458.water_gain(day)
            _q327 = _q458.units + g
            ripe = _q458.age >= _q421['myd'] or _q327 >= _q421['max_yield'] or day >= FINAL_DAY or (_q458.mls >= 0 and _q458.mls <= 24 * day + 23)
            if not ripe and _OPTS['wheat_h3'] and (_q458.crop == 'WHEAT') and (_q458.age == 3) and (_q458.fert_until >= day):
                ripe = True
            _q324(Task('HARVEST', xy, level=2 if ripe else 1, value=_q327 * px, deadline=_decay_deadline(state, _q458), after=_q947 if g > 0 else None, why='ripe' if ripe else 'early harvest'))

def _animal_tasks(state, _q336, _q324, glut=(), hold_harvest=()):
    xy = _q336.xy
    _q941 = _px(state, _q336.product)
    _q323 = ANIMALS[_q336.animal]
    g = _q336.product in glut
    day = state.day
    end = _OPTS['end_husb']
    if end:
        _q907 = day + (_q323['interval'] if _q336.prod_tonight else _q336.next_prod_in)
        _q414 = _q907 <= FINAL_DAY - 1
        _q954 = day + _q336.next_prod_in <= FINAL_DAY - 1
        _q802 = sum((1 for _q475 in (day + 1, day + 2) if _q475 <= FINAL_DAY))
        _q701 = _q802 * min(_px(state, 'FERTILIZER'), 100.0) * 0.5 >= _px(state, 'WHEAT')
        _q507 = _q336.must_feed and (not _q954) and (not _q701)
    else:
        _q414 = True
        _q507 = False
    if _q336.units > 0:
        _q1170 = _q336.prod_tonight and _q336.units + 1 + _q336.bank > _q323['max_held']
        _q758 = 1 if _q336.product in hold_harvest and day < FINAL_DAY and (not _q507) else 2
        _q324(Task('HARVEST', xy, level=_q758, value=_q336.units * _q941, why='escapes tonight (end)' if _q507 else 'waste tonight' if _q1170 else 'units ready'))
    if _q336.fert_avail:
        _q324(Task('COLLECT_FERTILIZER', xy, level=2, value=_px(state, 'FERTILIZER') * 0.6, why='fertiliser'))
    _q947 = None
    crit = _OPTS['husb_crit']
    _q560 = False
    cf = _OPTS['care_full'] and (not g) and (_q336.animal in ('SHEEP', 'COW')) and (day < FINAL_DAY) and _q414 and (day + (_q323['interval'] if _q336.prod_tonight else _q336.next_prod_in) <= FINAL_DAY - 1)
    if not _q336.fed:
        if _q336.must_feed:
            if not _q507:
                _q947 = _q324(Task('FEED', xy, need='WHEAT', level=3, value=_q323['cost'] + _q941, why='escapes tonight if unfed'))
                _q560 = True
        elif crit and _q336.prod_tonight and (_q336.bank > 0):
            _q947 = _q324(Task('FEED', xy, need='WHEAT', level=3, value=_q941 * (1 + _q336.bank), why='releases care bank tonight (crit)'))
            _q560 = True
        elif _OPTS['husb_q'] is not None and (not g) and _q336.prod_tonight and (_q941 >= _OPTS['husb_q']) and (not end or _q414 or _q336.bank > 0):
            _q947 = _q324(Task('FEED', xy, need='WHEAT', level=3, value=_q941 * (1 + _q336.bank), why='production tonight (husb_q)'))
            _q560 = True
        elif not g and (not end or (_q336.prod_tonight and _q336.bank > 0) or _q414):
            why = 'releases care bank tonight' if _q336.prod_tonight and _q336.bank > 0 else 'banks care bonus'
            _q947 = _q324(Task('FEED', xy, need='WHEAT', level=3 if cf else 2, value=_q941 * (1 + (_q336.bank if _q336.prod_tonight else 0)), why=why + (' (care_full)' if cf else '')))
            _q560 = _q560 or cf
    if not _q336.cared and day < FINAL_DAY and _q414:
        if g:
            if _q336.animal in _OPTS['glut_care_fed'] and (_q336.fed or _q560):
                _q324(Task('CARE', xy, level=2, value=_q941 * 0.9, after=_q947, why='+1 unit at next production (glut, fed)'))
        elif cf and (_q336.fed or _q560):
            _q324(Task('CARE', xy, level=3, value=_q941 * 0.9, after=_q947, why='+1 unit at next production (care_full)'))
        elif (crit or _OPTS['husb_q'] is not None) and _q560:
            _q324(Task('CARE', xy, level=3, value=_q941 * 0.9, after=_q947, why='+1 unit at next production (crit, with FEED)'))
        else:
            _q324(Task('CARE', xy, level=2, value=_q941 * 0.9, why='+1 unit at next production (if fed)'))

def task_turns(tasks, _q775=2, _q783=1.25, _q705=2, n_units=1):
    """Rough unit-turns to do the tasks of level >= min_level (plus all roots and their chains): one turn per command,
    walking ~move_per_task per task (clustered farm), kit pickups per unit."""
    n = sum((1 for t in tasks if t.level >= _q775 or t.src == 'plan'))
    return int(round(n * (1.0 + _q783) + _q705 * n_units))

def needs(tasks, _q775=2):
    """Items the day's tasks consume: {'WHEAT': feeds, 'FERTILIZER': fertilisations, animal: placements}."""
    _q880 = {}
    for t in tasks:
        if t.need and (t.level >= _q775 or t.src == 'plan'):
            _q880[t.need] = _q880.get(t.need, 0) + 1
    return _q880