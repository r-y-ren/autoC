"""fp.rival - forecast the RIVAL's future market SALES per item from public observations only (Kaggriculture).

Pure Python (no numpy, no engine import, no file access at call time except the optional params JSON loaded once).
Fitted tables come from tools/fp/rival_fit.py (offline, numpy) and live in tools/fp/rival_params.json; a submission
can embed them and pass params=dict.

MODEL (per rival TYPE in TYPES = v2 / v1 / other / v46 / gen):
  shed stock  S_t   (units in the rival's private shed at decision time t; estimated online, see observe())
  inflow      F_t   (units entering the shed during step t) = harvests of the public tiles (engine production rules,
                    tile_supply()) spread over the day by the type's inflow hour profile + a type prior for supply
                    not yet visible on the tiles (future plantings / purchases), fertilizer from animals.
  sales       E[x_t] = min(S_t, S_t * h)   h = hazard(type, item, hour, price/base bin, day bin, held bin)
                    = a multiplicative Poisson-rate model fitted by IPF on logged games (held units as exposure).
  S_{t+1} = S_t - x_t + F_t ; market inventory projected with the town drains + the expected rival sales (+ our own
  planned sales if given) to price the later steps.
  expected rival BUYS of WHEAT / FERTILIZER (type table by day bin x hour, scaled by the rival's observed / expected
  buys) enter the shed too (wash / feed traders).
Type detection online: naive-Bayes prior from public opening features (step-2 money, day-0/1 melon count, NE / SW
land purchase steps) x a tempered Poisson likelihood of the rival sales observed so far (per type hazard).
Per-rival calibration online: observed vs model-predicted sales per item and per (item, hour) (gamma-Poisson
shrinkage, K = 8 / 3 units) multiply the hazard -> the forecast adapts to this rival's own schedule.
Persistence blend (params['blend'], fitted on train games): WHEAT 0.3 / FERTILIZER 0.4 model weight, the rest = the
rival's same-hour sales of the last day (trade-driven items); goods use the structural model only.
No look-ahead: everything at step t uses observations up to t (the offline emulation rival_fit.history_state too).

ONLINE SALES / STOCK ACCOUNTING (observe):
  rival net units into the market at step t-1 = inv_t - inv_{t-1} + drain(t-1) - our executed net units (from our
  own market orders capped by our own shed; or passed exactly as own_sold / own_bought).  $1-floor sales add no
  inventory: invisible (as for every public-data method).
  harvests: per rival tile between consecutive observations (yield drop / crop removed, not weeded); the harvested
  units ride with the rival unit standing on the tile and enter the shed when that unit stands on a shed-access tile
  (or at the end of the day); fertilizer collected (+1 when fertilizer_available flips off) / used (fertilized_until
  day raised: -1); wheat fed (fed_today flips on: -1 wheat); rival buys of WHEAT / FERTILIZER add to the shed.

API
  m = RivalModel(params=None, rival_type=None, player=None)
      params: dict (rival_params.json content) or None (load tools/fp/rival_params.json next to this file).
      rival_type: fix the type ('v2' | 'v1' | 'other' | 'v46' | 'gen'); None = online detection.
  m.observe(obs, own_sold=None, own_bought=None, own_orders=None)
      call once per turn with the current observation (dict or Kaggle Struct) BEFORE acting.
      own_orders = our market order list submitted at the previous step (to split the market flow exactly);
      own_sold / own_bought = {item: units} executed at the previous step (overrides own_orders).
  m.forecast(obs=None, H=24, own_plan=None) -> {step: {item: expected units}}   steps t .. t+H-1 (t = last observed
      step, capped at 718).  own_plan = {step: {item: units we plan to sell}} for the price projection (optional).
  m.forecast_daily(obs=None, H=720) -> {day: {item: units}}
  m.sample(obs=None, H=24, rng=None, own_plan=None) -> one sampled scenario {step: {item: units}} (type drawn from the
      posterior, binomial sales), for search.
  m.type_posterior() -> {type: probability};  m.stock() -> {'shed': {...}, 'transit': {...}}
  m.sold_history -> list of (step, {item: units}) observed rival sales (net > 0; negative nets = buys kept separately)
  tile_supply(tiles, day, hour, params=None, rtype='gen') -> {'now': {item: u}, 'days': {day: {item: u}}}
      expected harvestable units from the public tiles (engine rules; harvest ages from the type table).
  hazard(params, rtype, item, hour, ratio, day, step, held) -> per-unit sale probability for one step.
  m.set_state(step, tiles, inv, px, shops, shed=None, carry=None, tiles_step=None): offline evaluation hook.
  m.recent_pattern(t0) -> [24 dicts] rival sales of the last day by hour.
Timing (CPython, laptop): observe ~0.15 ms/turn; forecast H=24 ~3 ms, H=720 ~7 ms per active type (mixture of 2-3
types ~30 ms): call the full horizon at most every few turns (cache), H<=72 per turn (results/portable/fp_rival.txt).
Validation (647 held-out seats, results/portable/fp_rival.txt): next-day GOODS sales error 0.377 of volume vs
sell-on-harvest 0.756 and last-day average 0.777; WHEAT+FERT 0.453 vs 1.093 / 0.477; hour-profile TVD 0.571 vs
yesterday's pattern 0.614 / uniform 0.792.
"""
import json
import math
import os
import random
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
GOODS = ('CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL')
TYPES = ('v2', 'v1', 'other', 'v46', 'gen')
BASE = {'WHEAT': 25, 'CARROT': 35, 'TOMATO': 60, 'STRAWBERRY': 120, 'MELON': 250, 'EGG': 50, 'MILK': 160, 'WOOL': 200, 'FERTILIZER': 100}
CROPS = {'WHEAT': {'fyd': 2, 'myd': 4, 'interval': 0, 'max_yield': 6, 'ongoing': False}, 'CARROT': {'fyd': 2, 'myd': 3, 'interval': 0, 'max_yield': 4, 'ongoing': False}, 'TOMATO': {'fyd': 8, 'myd': 8, 'interval': 1, 'max_yield': 4, 'ongoing': True}, 'STRAWBERRY': {'fyd': 10, 'myd': 10, 'interval': 2, 'max_yield': 4, 'ongoing': True}, 'MELON': {'fyd': 10, 'myd': 12, 'interval': 0, 'max_yield': 6, 'ongoing': False}}
ANIMALS = {'GOOSE': {'fyd': 4, 'interval': 1, 'max_held': 4, 'product': 'EGG'}, 'COW': {'fyd': 8, 'interval': 2, 'max_held': 6, 'product': 'MILK'}, 'SHEEP': {'fyd': 6, 'interval': 3, 'max_held': 6, 'product': 'WOOL'}}
SHOPS = {'BAKERY': ('EGG', 'WHEAT'), 'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'), 'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'), 'YARN_STORE': ('WOOL',), 'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'), 'PET_CAFE': ('CARROT',), 'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'), 'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY')}
MP = {'WHEAT': (25, 400, 'sqrt', 0.8, 'log', 0.2), 'CARROT': (35, 450, 'hinge', 1.0, 'sqrt', 0.7), 'TOMATO': (60, 200, 'hinge', 0.4, 'sqrt', 0.6), 'STRAWBERRY': (120, 100, 'sqrt', 0.7, 'linear', 1.6), 'MELON': (250, 300, 'log', 0.2, 'sq', 3.6), 'EGG': (50, 332, 'hinge', 0.4, 'log', 0.2), 'MILK': (160, 122, 'sqrt', 0.6, 'linear', 1.6), 'WOOL': (200, 105, 'log', 0.2, 'sq', 3.2), 'FERTILIZER': (100, 200, 'linear', 0.4, 'linear', 0.4)}
ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
LAST_STEP = 718
TPD = 24
P_EDGES = (0.5, 0.8, 1.0, 1.2, 1.5, 2.0)
H_EDGES = (2, 4, 8, 16, 32)
N_PB, N_HB, N_DB = (7, 6, 8)
LEAD_EDGES = (2, 4, 7, 11)

def pbin(_q1045):
    for _q712, _q575 in enumerate(P_EDGES):
        if _q1045 < _q575:
            return _q712
    return len(P_EDGES)

def hbin(held):
    for _q712, _q575 in enumerate(H_EDGES):
        if held < _q575:
            return _q712
    return len(H_EDGES)

def dbin(step):
    if step >= 712:
        return 7
    _q530 = step // TPD
    if _q530 <= 9:
        return 0
    if _q530 <= 14:
        return 1
    if _q530 <= 19:
        return 2
    if _q530 <= 24:
        return 3
    if _q530 <= 27:
        return 4
    if _q530 == 28:
        return 5
    return 6

def leadbin(_q797):
    for _q712, _q575 in enumerate(LEAD_EDGES):
        if _q797 < _q575:
            return _q712
    return len(LEAD_EDGES)

def _shape(f, x, T):
    x = max(0.0, x)
    if f == 'linear':
        return x
    if f == 'sq':
        return x * x
    if f == 'sqrt':
        return math.sqrt(x)
    if f == 'log':
        return math.log(1.0 + x)
    if f == 'hinge':
        _q1221 = x / T
        return _q1221 + 8.0 * max(0.0, _q1221 - 1.0) ** 2
    return x
_AMP = {}
for _q300, (_b, _q274, _q277, _q278, _q275, _q276) in MP.items():
    _AMP[_q300] = (_q278 * _b / _shape(_q277, _q274, _q274), _q276 * _b / _shape(_q275, _q274, _q274))

def price(item, inv):
    base, T, _q412, _q432, _q378, _q396 = MP[item]
    if inv < 10000:
        _q954 = base + _AMP[item][0] * _shape(_q412, 10000 - inv, T)
    else:
        _q954 = base - _AMP[item][1] * _shape(_q378, inv - 10000, T)
    return max(1, int(round(_q954)))

def drain(shops, step):
    """Town consumption of engine step `step` with the unlocked shop list `shops` -> {item: units}."""
    _q530 = {}
    if step % 4 == 0:
        for sh in shops or ():
            _q1021 = SHOPS.get(sh, ())
            m = 2 if len(_q1021) == 1 else 1
            for it in _q1021:
                _q530[it] = _q530.get(it, 0) + m
    if step % 24 == 0:
        for it in PRODUCTS:
            if it != 'FERTILIZER':
                _q530[it] = _q530.get(it, 0) + 1
    return _q530

def _get(_q922, k, _q530=None):
    if isinstance(_q922, dict):
        return _q922.get(k, _q530)
    g = getattr(_q922, 'get', None)
    if callable(g):
        try:
            return g(k, _q530)
        except TypeError:
            pass
    return getattr(_q922, k, _q530)
_PARAMS = None

def load_params(_q972=None):
    global _PARAMS
    if _q972 is None:
        if _PARAMS is not None:
            return _PARAMS
        _q972 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rival_params.json')
    with open(_q972, encoding='utf-8') as _q622:
        _q954 = json.load(_q622)
    _PARAMS = _q954
    return _q954

def _harvest_age_dist(params, _q1091, crop):
    """-> list of (age, prob) of the harvest day relative to planting for a non-ongoing crop."""
    if params:
        t = params.get('hage', {}).get(_q1091, {}).get(crop) or params.get('hage', {}).get('gen', {}).get(crop)
        if t:
            return [(int(a), float(_q954)) for a, _q954 in t]
    return [(CROPS[crop]['myd'], 1.0)]

def _iter_tiles(tiles):
    """Accept a 10x10 engine grid (dicts / None / 'LOCKED') or an iterable of (x, y, dict)."""
    if tiles and isinstance(tiles, (list, tuple)) and tiles and isinstance(tiles[0], (list, tuple)) and (len(tiles[0]) == 0 or not isinstance(tiles[0][0], int)):
        for _q1272, _q1086 in enumerate(tiles):
            for x, t in enumerate(_q1086):
                if isinstance(t, dict):
                    yield (x, _q1272, t)
    else:
        for x, _q1272, t in tiles or ():
            yield (x, _q1272, t)

def tile_supply(tiles, day, hour=23, params=None, _q1091='gen', last_day=29):
    """Expected harvestable units from the public tiles of one farm.
    -> {'now': {item: units on the tiles harvestable today}, 'days': {d: {item: units becoming available on day d}}}
    Engine rules: non-ongoing crops (+1 per watering on ages [(myd+1)//2, myd], +2 while fertilised; harvested at the
    type's harvest age); ongoing crops produce at the end of day e (+1, +2 fertilised) and are available on e+1;
    animals produce 1 + banked care on production days (care assumed to continue when cared today / banked > 0),
    available the next day.  Assumes the rival keeps watering / feeding (no weeds, no escapes)."""
    now = {}
    days = {}
    pf = 0.0
    if params:
        pf = float(params.get('fert_cont', {}).get(_q1091, params.get('fert_cont', {}).get('gen', 0.5)))

    def _q376(_q530, it, _q1221):
        if _q1221 <= 0:
            return
        if _q530 <= day:
            now[it] = now.get(it, 0.0) + _q1221
        elif _q530 <= last_day:
            _q539 = days.setdefault(_q530, {})
            _q539[it] = _q539.get(it, 0.0) + _q1221
    for x, _q1272, t in _iter_tiles(tiles):
        kind = t.get('kind')
        if kind == 'PLANT':
            crop = t.get('crop')
            _q474 = CROPS.get(crop)
            if _q474 is None:
                continue
            _q988 = int(t.get('planted_day', day))
            _q1279 = float(t.get('yield_units', 0) or 0)
            _q654 = int(t.get('fertilized_until_day', -1))
            _q595 = _q654 >= _q988
            watered = bool(t.get('watered_today'))
            if not _q474['ongoing']:
                _q381 = day - _q988
                _q1265 = (_q474['myd'] + 1) // 2
                dist = [(a, _q954) for a, _q954 in _harvest_age_dist(params, _q1091, crop) if a >= _q381]
                if not dist:
                    dist = [(_q381, 1.0)]
                _q1281 = sum((_q954 for _, _q954 in dist))
                for a, _q954 in dist:
                    _q1221 = _q1279
                    for g in range(_q381, a + 1):
                        if g < _q1265 or g > _q474['myd']:
                            continue
                        if g == _q381 and watered:
                            continue
                        _q548 = _q988 + g
                        fert = 1.0 if _q654 >= _q548 else pf if _q595 else 0.0
                        _q1221 += 1.0 + fert
                    _q1221 = min(float(_q474['max_yield']), _q1221)
                    _q376(_q988 + a, crop, _q1221 * _q954 / _q1281)
            else:
                if _q1279 > 0:
                    _q376(day, crop, _q1279)
                for _q575 in range(day, last_day):
                    k = _q575 + 1 - _q988 - _q474['fyd']
                    if k < 0 or k % _q474['interval']:
                        continue
                    _q497 = k // _q474['interval'] + 1
                    if _q497 > _q474['max_yield']:
                        break
                    fert = 1.0 if _q654 >= _q575 else pf if _q595 else 0.0
                    _q376(_q575 + 1, crop, 1.0 + fert)
        elif t.get('animal'):
            a = ANIMALS.get(t.get('animal'))
            if a is None:
                continue
            prod = a['product']
            _q996 = int(t.get('placed_day', day))
            _q1279 = float(t.get('yield_units', 0) or 0)
            if _q1279 > 0:
                _q376(day, prod, _q1279)
            bank = float(t.get('pending_care_bonus', 0) or 0)
            _q466 = 1.0 if t.get('cared_today') or bank > 0 else 0.0
            for _q575 in range(day, last_day):
                k = _q575 + 1 - _q996 - a['fyd']
                if k >= 0 and k % a['interval'] == 0:
                    _q376(_q575 + 1, prod, min(float(a['max_held']), 1.0 + bank))
                    bank = 0.0
                c = (1.0 if t.get('cared_today') else _q466) if _q575 == day else _q466
                bank += c
    return {'now': now, 'days': days}

def count_animals(tiles):
    n = 0
    for x, _q1272, t in _iter_tiles(tiles):
        if t.get('animal'):
            n += 1
    return n

class _Haz:
    """Flattened hazard tables of one type: base[item], A[item][hour], B[item][pb], C[item][db], D[item][hb]."""
    __slots__ = ('base', 'A', 'B', 'C', 'D', 'prof', 'prior', 'frate', 'buyt')

    def __init__(_q1120, params, _q1091):
        _q711 = params['haz'].get(_q1091) or params['haz']['gen']
        _q1120.base = {it: float(_q711[it]['base']) for it in _q711}
        _q1120.A = {it: [float(_q1233) for _q1233 in _q711[it]['hour']] for it in _q711}
        _q1120.B = {it: [float(_q1233) for _q1233 in _q711[it]['pb']] for it in _q711}
        _q1120.C = {it: [float(_q1233) for _q1233 in _q711[it]['db']] for it in _q711}
        _q1120.D = {it: [float(_q1233) for _q1233 in _q711[it]['hb']] for it in _q711}
        _q1009 = params.get('prof', {})
        _q1120.prof = _q1009.get(_q1091) or _q1009.get('gen') or {}
        _q1120.prior = params.get('prior', {}).get(_q1091) or params.get('prior', {}).get('gen') or {}
        _q1120.frate = float(params.get('frate', {}).get(_q1091, params.get('frate', {}).get('gen', 0.0)))
        _q1120.buyt = params.get('buy', {}).get(_q1091) or params.get('buy', {}).get('gen') or {}

    def buy(_q1120, it, db, hour):
        t = _q1120.buyt.get(it)
        if not t:
            return 0.0
        return float(t[db][hour])

    def h(_q1120, it, hour, pb, db, hb):
        b = _q1120.base.get(it)
        if b is None:
            return 0.0
        _q1233 = b * _q1120.A[it][hour] * _q1120.B[it][pb] * _q1120.C[it][db] * _q1120.D[it][hb]
        return 1.0 if _q1233 > 1.0 else _q1233
_HAZ_CACHE = {}

def _haz(params, _q1091):
    k = (id(params), _q1091)
    _q1281 = _HAZ_CACHE.get(k)
    if _q1281 is None:
        _q1281 = _Haz(params, _q1091)
        _HAZ_CACHE[k] = _q1281
    return _q1281

def hazard(params, _q1091, item, hour, _q1045, day, step, held):
    """Per-unit probability that a held unit of `item` is sold at this step (type table)."""
    return _haz(params, _q1091).h(item, hour, pbin(_q1045), dbin(step), hbin(held))

class RivalModel:

    def __init__(_q1120, params=None, _q1076=None, player=None, _q1191=0.25):
        _q1120.params = params if params is not None else load_params()
        _q1120.fixed = _q1076
        _q1120.player = player
        _q1120.temper = _q1191
        _q1120.step = None
        _q1120._prev = None
        _q1120.shed = {it: 0.0 for it in PRODUCTS}
        _q1120.carry = {}
        _q1120.sold_history = []
        _q1120.bought_history = []
        _q1120.loglik = {t: 0.0 for t in TYPES}
        _q1120.cal = {}
        _q1120.bcal = {}
        _q1120.cal_k = (8.0, 3.0)
        _q1120.feat = {'m2': None, 'mel': 0, 'ne': None, 'sw': None, 'nland': 1}
        _q1120._tiles = None
        _q1120._inv = None
        _q1120._px = None
        _q1120._shops = []
        _q1120._day = 0
        _q1120._hour = 0
        _q1120._tstamp = None

    def observe(_q1120, _q928, _q953=None, _q950=None, own_orders=None):
        me = _get(_q928, 'player', _q1120.player)
        me = int(me or 0) if _q1120.player is None else _q1120.player
        _q1120.player = me
        opp = 1 - me
        step = _get(_q928, 'step', None)
        day = int(_get(_q928, 'day', 0) or 0)
        hour = int(_get(_q928, 'hour', 0) or 0)
        step = int(step) if step is not None else TPD * day + hour
        farms = _get(_q928, 'farms', None) or []
        _q1066 = farms[opp] if len(farms) > opp else {}
        tiles = _get(_q1066, 'tiles', None) or []
        market = _get(_q928, 'market', None) or {}
        inv = dict(_get(market, 'inventory', None) or {})
        px = dict(_get(market, 'prices', None) or {})
        town = _get(_q928, 'town', None) or {}
        shops = list(_get(town, 'unlocked_shops', None) or [])
        _q1016 = _get(_q928, 'private', None) or {}
        myshed = dict(_get(_q1016, 'shed', None) or {})
        mycarry = {}
        for _q530 in _get(_q1016, 'inventories', None) or []:
            for k, _q1233 in dict(_q530).items():
                mycarry[k] = mycarry.get(k, 0) + int(_q1233 or 0)
        units = [tuple(_get(_q1066, 'farmer', None) or (4, 4))] + [tuple(h) for h in _get(_q1066, 'hands', None) or []]
        _q1079 = float(_get(_q1066, 'money', 0.0) or 0.0)
        _q522 = {'step': step, 'tiles': tiles, 'inv': inv, 'shops': shops, 'myshed': myshed, 'mycarry': mycarry, 'units': units, 'day': day, 'hour': hour, 'px': px}
        prev = _q1120._prev
        if prev is not None and step == prev['step'] + 1 and inv and prev['inv']:
            _q1120._account_market(prev, _q522, _q953, _q950, own_orders)
            _q1120._account_tiles(prev, _q522)
        elif prev is not None and step != prev['step']:
            _q1120._account_tiles(prev, _q522)
        _q1120._features(step, day, tiles, _q1079)
        _q1120._prev = _q522
        _q1120.step, _q1120._day, _q1120._hour = (step, day, hour)
        _q1120._tiles, _q1120._inv, _q1120._px, _q1120._shops = (tiles, inv, px, shops)
        _q1120._tstamp = (day, hour)

    def _account_market(_q1120, prev, _q522, _q953, _q950, own_orders):
        s = prev['step']
        _q560 = drain(prev['shops'], s)
        _q1059, _q1058 = ({}, {})
        for _q922 in (own_orders or [])[:10]:
            try:
                if len(_q922) >= 3 and int(_q922[2]) > 0:
                    if _q922[0] == 'SELL':
                        _q1059[_q922[1]] = _q1059.get(_q922[1], 0) + int(_q922[2])
                    elif _q922[0] == 'BUY_PRODUCT':
                        _q1058[_q922[1]] = _q1058.get(_q922[1], 0) + int(_q922[2])
            except Exception:
                continue
        sold, _q428 = ({}, {})
        for it in PRODUCTS:
            if it not in _q522['inv'] or it not in prev['inv']:
                continue
            _q1206 = int(_q522['inv'][it]) - int(prev['inv'][it]) + _q560.get(it, 0)
            if _q953 is not None or _q950 is not None:
                _q839 = int((_q953 or {}).get(it, 0)) - int((_q950 or {}).get(it, 0))
            else:
                cap = int(prev['myshed'].get(it, 0)) + int(prev['mycarry'].get(it, 0))
                ms = min(_q1059.get(it, 0), cap)
                if price(it, int(prev['inv'][it])) <= 1:
                    ms = 0
                _q839 = ms - _q1058.get(it, 0)
            _q1036 = _q1206 - _q839
            if _q1036 > 0:
                sold[it] = _q1036
            elif _q1036 < 0 and it in ('WHEAT', 'FERTILIZER'):
                _q428[it] = -_q1036
        if sold:
            _q1120.sold_history.append((s, sold))
        if _q428:
            _q1120.bought_history.append((s, _q428))
        _q1120._bayes(s, prev, sold, _q428)
        for it, _q1221 in sold.items():
            _q1186 = min(_q1120.shed.get(it, 0.0), float(_q1221))
            _q1120.shed[it] = _q1120.shed.get(it, 0.0) - _q1186
            rest = float(_q1221) - _q1186
            if rest > 0:
                for c in _q1120.carry.values():
                    k = min(c.get(it, 0.0), rest)
                    if k > 0:
                        c[it] -= k
                        rest -= k
        for it, _q1221 in _q428.items():
            _q1120.shed[it] = _q1120.shed.get(it, 0.0) + _q1221

    def _bayes(_q1120, s, prev, sold, _q428=None):
        """Tempered Poisson log-likelihood of the observed sales per type (GOODS; exposure = estimated shed) and the
        per-rival calibration accumulators: observed vs predicted sales per item and per (item, hour), observed vs
        expected buys of WHEAT / FERTILIZER (gamma-Poisson shrinkage in _mult())."""
        _q32 = _q1120.params
        hour = s % TPD
        db = dbin(s)
        _q1220 = TYPES if _q1120.fixed is None else (_q1120.fixed,)
        _q487 = {}
        for c in _q1120.carry.values():
            for it, _q1221 in c.items():
                _q487[it] = _q487.get(it, 0.0) + _q1221
        for t in _q1220:
            _q711 = _haz(_q32, t)
            _q452 = _q1120.cal.setdefault(t, {})
            _q808 = 0.0
            for it in PRODUCTS:
                held = _q1120.shed.get(it, 0.0) + _q487.get(it, 0.0) * 0.5
                x = sold.get(it, 0)
                if held < 0.5 and x == 0:
                    continue
                _q1045 = int(prev['px'].get(it, BASE[it]) or BASE[it]) / float(BASE[it])
                _q575 = max(held, float(x))
                lam = _q575 * _q711.h(it, hour, pbin(_q1045), db, hbin(_q575))
                c = _q452.get(it)
                if c is None:
                    c = _q452[it] = [0.0, 0.0, [0.0] * 24, [0.0] * 24]
                c[0] += x
                c[1] += lam
                c[2][hour] += x
                c[3][hour] += lam
                if it in GOODS and _q1120.fixed is None:
                    lam = max(0.001, lam)
                    _q808 += x * math.log(lam) - lam
            _q1120.loglik[t] += _q1120.temper * _q808
            _q405 = _q1120.bcal.setdefault(t, {})
            for it in ('WHEAT', 'FERTILIZER'):
                _q580 = _q711.buy(it, db, hour)
                b = _q405.get(it)
                if b is None:
                    b = _q405[it] = [0.0, 0.0]
                b[0] += (_q428 or {}).get(it, 0)
                b[1] += _q580

    def _mult(_q1120, _q1091):
        """-> ({item: [24 hazard multipliers]}, {item: buy multiplier}) from the calibration accumulators."""
        K, k = _q1120.cal_k
        _q946 = {}
        for it, c in _q1120.cal.get(_q1091, {}).items():
            mi = (c[0] + K) / (c[1] + K)
            _q946[it] = [min(5.0, max(0.2, (c[2][h] + k * mi) / (c[3][h] + k))) for h in range(24)]
        _q424 = {}
        for it, b in _q1120.bcal.get(_q1091, {}).items():
            _q424[it] = min(5.0, max(0.1, (b[0] + 20.0) / (b[1] + 20.0)))
        return (_q946, _q424)

    def _account_tiles(_q1120, prev, _q522):
        _q1024 = {}
        for x, _q1272, t in _iter_tiles(prev['tiles']):
            _q1024[x, _q1272] = t
        _q516 = {}
        for x, _q1272, t in _iter_tiles(_q522['tiles']):
            _q516[x, _q1272] = t
        _q906 = _q522['day'] != prev['day']
        _q1226 = {}
        for _q712, _q1221 in enumerate(_q522['units']):
            _q1226.setdefault(_q1221, _q712)
        _q687 = []
        for xy, a in _q1024.items():
            b = _q516.get(xy)
            _q1275 = float(a.get('yield_units', 0) or 0)
            if a.get('kind') == 'PLANT':
                crop = a.get('crop')
                _q474 = CROPS.get(crop)
                if _q474 is None:
                    continue
                _q1105 = b is not None and b.get('kind') == 'PLANT' and (b.get('crop') == crop) and (b.get('planted_day') == a.get('planted_day'))
                if _q1105 and int(b.get('fertilized_until_day', -1)) > int(a.get('fertilized_until_day', -1)):
                    _q687.append((xy, 'FERTILIZER', -1.0))
                if not _q474['ongoing']:
                    replant = b is not None and b.get('kind') == 'PLANT' and (int(b.get('planted_day', -1)) == _q522['day']) and (_q522['day'] != int(a.get('planted_day', -1)))
                    if not _q1105 and _q1275 > 0 and (b is None or replant):
                        _q687.append((xy, crop, _q1275))
                elif _q1105:
                    _q1276 = float(b.get('yield_units', 0) or 0)
                    if _q906:
                        k = _q522['day'] - int(a.get('planted_day', 0)) - _q474['fyd']
                        prod = 0.0
                        if k >= 0 and k % _q474['interval'] == 0 and (k // _q474['interval'] + 1 <= _q474['max_yield']):
                            prod = 1.0
                        if _q1275 > 0 and _q1276 <= prod + 1.0 and (_q1276 < _q1275 + prod):
                            _q687.append((xy, crop, _q1275))
                    elif _q1275 > 0 and _q1276 == 0 and (_q1275 >= 2):
                        _q687.append((xy, crop, _q1275))
                    elif _q1275 == 1 and _q1276 == 0:
                        if xy in _q1226:
                            _q687.append((xy, crop, _q1275))
                elif _q1275 > 0 and b is None:
                    _q687.append((xy, crop, _q1275))
            elif a.get('animal'):
                _q388 = ANIMALS.get(a.get('animal'))
                if _q388 is None:
                    continue
                _q1105 = b is not None and b.get('animal') == a.get('animal') and (b.get('placed_day') == a.get('placed_day'))
                if not _q1105:
                    continue
                _q1276 = float(b.get('yield_units', 0) or 0)
                if not _q906:
                    if _q1275 > 0 and _q1276 == 0:
                        _q687.append((xy, _q388['product'], _q1275))
                    if b.get('fed_today') and (not a.get('fed_today')):
                        _q687.append((xy, 'WHEAT', -1.0))
                    if a.get('fertilizer_available') and (not b.get('fertilizer_available')):
                        _q687.append((xy, 'FERTILIZER', 1.0))
                elif _q1275 > 0 and _q1276 < _q1275:
                    _q687.append((xy, _q388['product'], _q1275))
        for xy, it, _q1221 in _q687:
            if _q1221 < 0:
                _q712 = _q1226.get(xy)
                c = _q1120.carry.get(_q712) if _q712 is not None else None
                if c is not None and c.get(it, 0.0) >= 1.0:
                    c[it] -= 1.0
                else:
                    _q1120.shed[it] = max(0.0, _q1120.shed.get(it, 0.0) - 1.0)
                continue
            _q712 = _q1226.get(xy, 0)
            c = _q1120.carry.setdefault(_q712, {})
            c[it] = c.get(it, 0.0) + _q1221
        if _q906:
            for c in _q1120.carry.values():
                for it, _q1221 in c.items():
                    _q1120.shed[it] = _q1120.shed.get(it, 0.0) + _q1221
            _q1120.carry = {}
        else:
            for _q712, _q1221 in enumerate(_q522['units']):
                if _q1221 in ACCESS and _q712 in _q1120.carry:
                    for it, _q1233 in _q1120.carry[_q712].items():
                        _q1120.shed[it] = _q1120.shed.get(it, 0.0) + _q1233
                    del _q1120.carry[_q712]
        _q1206 = sum(_q1120.shed.values())
        if _q1206 > 100:
            f = 100.0 / _q1206
            for it in _q1120.shed:
                _q1120.shed[it] *= f

    def _features(_q1120, step, day, tiles, _q1079):
        f = _q1120.feat
        if step == 2 and f['m2'] is None:
            f['m2'] = _q1079
        if day <= 1:
            n = 0
            for x, _q1272, t in _iter_tiles(tiles):
                if t.get('crop') == 'MELON' and int(t.get('planted_day', 9)) <= 1:
                    n += 1
            f['mel'] = max(f['mel'], n)
        _q911 = 1
        _q1118 = set()
        for _q1272, _q1086 in enumerate(tiles or []):
            for x, t in enumerate(_q1086):
                if t != 'LOCKED':
                    _q1118.add(('N' if _q1272 < 5 else 'S') + ('W' if x < 5 else 'E'))
        _q911 = max(1, len(_q1118))
        if _q911 >= 2 and f['ne'] is None:
            f['ne'] = step - 1
        if _q911 >= 3 and f['sw'] is None:
            f['sw'] = step - 1
        f['nland'] = _q911

    def _feature_loglik(_q1120, t):
        _q32 = _q1120.params.get('typefeat', {})
        tf = _q32.get(t)
        if not tf:
            return 0.0
        f = _q1120.feat
        _q808 = 0.0
        if f['m2'] is not None:
            _q808 += math.log(tf['m2lo'] if f['m2'] < 1000 else 1.0 - tf['m2lo'])
        if _q1120.step is not None and _q1120.step >= 47:
            _q808 += math.log(tf['mel12'] if f['mel'] >= 12 else 1.0 - tf['mel12'])
        for key in ('ne', 'sw'):
            _q699 = tf[key]
            if f[key] is not None:
                b = min(71, f[key] // 10)
                _q808 += math.log(_q699[b])
            elif _q1120.step is not None:
                _q400 = min(72, _q1120.step // 10 + 1)
                _q808 += math.log(max(1e-06, sum(_q699[_q400:])))
        return _q808

    def type_posterior(_q1120):
        if _q1120.fixed is not None:
            return {_q1120.fixed: 1.0}
        _q1014 = _q1120.params.get('typeprior', {})
        _q802 = {}
        for t in TYPES:
            _q802[t] = math.log(_q1014.get(t, 0.2)) + _q1120._feature_loglik(t) + _q1120.loglik[t]
        m = max(_q802.values())
        w = {t: math.exp(_q1233 - m) for t, _q1233 in _q802.items()}
        _q1281 = sum(w.values())
        w = {t: max(0.0001, _q1233 / _q1281) for t, _q1233 in w.items()}
        _q1281 = sum(w.values())
        return {t: _q1233 / _q1281 for t, _q1233 in w.items()}

    def set_state(_q1120, step, tiles, inv, px, shops, shed=None, carry=None, _q1200=None):
        """Offline evaluation hook: install a public state (and optionally a known shed) without observe().
        tiles_step = the step at which the tile snapshot was observed (default: step)."""
        _q1120.step, _q1120._day, _q1120._hour = (int(step), int(step) // TPD, int(step) % TPD)
        ts = int(step) if _q1200 is None else int(_q1200)
        _q1120._tstamp = (ts // TPD, ts % TPD)
        _q1120._tiles, _q1120._inv, _q1120._px, _q1120._shops = (tiles, dict(inv), dict(px), list(shops))
        if shed is not None:
            _q1120.shed = {it: float(shed.get(it, 0)) for it in PRODUCTS}
        if carry is not None:
            _q1120.carry = carry

    def stock(_q1120):
        _q1211 = {}
        for c in _q1120.carry.values():
            for it, _q1221 in c.items():
                _q1211[it] = _q1211.get(it, 0.0) + _q1221
        return {'shed': dict(_q1120.shed), 'transit': _q1211}

    def _inflows(_q1120, _q1091, t0, _q1177):
        """-> {step: {item: expected shed inflow}} for steps t0..t1-1 of one type (tile supply + prior + transit)."""
        _q32 = _q1120.params
        _q711 = _haz(_q32, _q1091)
        _q536 = t0 // TPD
        h0 = t0 % TPD
        _q1190, _q1195 = _q1120._tstamp if _q1120._tstamp is not None else (_q536, h0)
        sup = tile_supply(_q1120._tiles, _q1190, _q1195, _q32, _q1091)
        _q946 = {}

        def _q1153(_q530, it, _q1221, _q708=0):
            if _q1221 <= 0:
                return
            prof = _q711.prof.get(it)
            if not prof:
                prof = [1.0 / 24] * 24
            _q1281 = sum(prof[_q708:])
            if _q1281 <= 0:
                prof = [1.0 / 24] * 24
                _q1281 = sum(prof[_q708:])
            for h in range(_q708, 24):
                s = _q530 * TPD + h
                if s < t0 or s >= _q1177:
                    continue
                _q1233 = _q1221 * prof[h] / _q1281
                if _q1233 > 0:
                    _q922 = _q946.setdefault(s, {})
                    _q922[it] = _q922.get(it, 0.0) + _q1233
        for it, _q1221 in sup['now'].items():
            prof = _q711.prof.get(it) or [1.0 / 24] * 24
            m = min(1.0, sum(prof[_q1195:]))
            _q1153(_q1190, it, _q1221 * m, _q1195)
            _q1153(_q1190 + 1, it, _q1221 * (1.0 - m))
        for _q530, _q539 in sup['days'].items():
            for it, _q1221 in _q539.items():
                _q1153(_q530, it, _q1221)
        _q1009 = _q711.prior
        _q889 = count_animals(_q1120._tiles)
        last_day = min(29, (_q1177 - 1) // TPD)
        for _q530 in range(_q536, last_day + 1):
            _q793 = str(leadbin(_q530 - _q536))
            for it in PRODUCTS:
                _q1086 = _q1009.get(it)
                if not _q1086:
                    continue
                _q1233 = _q1086.get(str(_q530), {}).get(_q793)
                if _q1233:
                    _q1208 = sup['days'].get(_q530, {}).get(it, 0.0) + (sup['now'].get(it, 0.0) if _q530 == _q536 else 0.0)
                    _q1233 = max(-_q1208, float(_q1233))
                    if _q530 == _q536:
                        _q1233 *= sum((_q711.prof.get(it) or [1.0 / 24] * 24)[h0:])
                    if _q1233 > 0:
                        _q1153(_q530, it, _q1233, h0 if _q530 == _q536 else 0)
                    elif _q1233 < 0:
                        _q1112 = (_q1208 + _q1233) / _q1208 if _q1208 > 0 else 1.0
                        for h in range(h0 if _q530 == _q536 else 0, 24):
                            s = _q530 * TPD + h
                            _q922 = _q946.get(s)
                            if _q922 and it in _q922:
                                _q922[it] *= _q1112
            if _q711.frate > 0 and _q889:
                _q1153(_q530, 'FERTILIZER', _q711.frate * _q889, h0 if _q530 == _q536 else 0)
        for c in _q1120.carry.values():
            for it, _q1221 in c.items():
                for k, f in ((t0, 0.5), (t0 + 1, 0.5)):
                    if k < _q1177:
                        _q922 = _q946.setdefault(k, {})
                        _q922[it] = _q922.get(it, 0.0) + _q1221 * f
        return _q946

    def _run(_q1120, _q1091, t0, _q1177, _q952=None, rng=None):
        _q32 = _q1120.params
        _q711 = _haz(_q32, _q1091)
        _q726 = _q1120._inflows(_q1091, t0, _q1177)
        _q851, _q425 = _q1120._mult(_q1091)
        _q443 = [it for it in ('WHEAT', 'FERTILIZER') if _q711.buyt.get(it)]
        held = {it: max(0.0, _q1233) for it, _q1233 in _q1120.shed.items()}
        inv = {it: int(_q1233) for it, _q1233 in (_q1120._inv or {}).items()}
        shops = list(_q1120._shops or [])
        _q946 = {}
        for s in range(t0, _q1177):
            hour = s % TPD
            db = dbin(s)
            _q1086 = {}
            op = _q952.get(s) if _q952 else None
            for it in PRODUCTS:
                _q710 = held.get(it, 0.0)
                if _q710 > 1e-06:
                    _q741 = inv.get(it, 10000)
                    _q1036 = price(it, _q741) / float(BASE[it])
                    h = _q711.h(it, hour, pbin(_q1036), db, hbin(_q710))
                    mi = _q851.get(it)
                    if mi is not None:
                        h = min(1.0, h * mi[hour])
                    if rng is None:
                        x = _q710 * h
                    else:
                        n = int(_q710)
                        if rng.random() < _q710 - n:
                            n += 1
                        x = float(sum((1 for _ in range(n) if rng.random() < h))) if n < 60 else float(max(0, int(round(rng.gauss(n * h, math.sqrt(max(1e-09, n * h * (1 - h))))))))
                    if x > 0:
                        _q1086[it] = x
                        held[it] = _q710 - x
                        if price(it, _q741) > 1:
                            inv[it] = _q741 + int(round(x)) if rng is not None else _q741 + x
                if op and it in op:
                    inv[it] = inv.get(it, 10000) + op[it]
            f = _q726.get(s)
            if f:
                for it, _q1233 in f.items():
                    held[it] = max(0.0, held.get(it, 0.0) + _q1233)
            for it in _q443:
                _q1233 = _q711.buy(it, db, hour) * _q425.get(it, 1.0)
                if _q1233 > 0:
                    held[it] = held.get(it, 0.0) + _q1233
                    inv[it] = inv.get(it, 10000) - _q1233
            _q560 = drain(shops, s)
            for it, _q1233 in _q560.items():
                inv[it] = inv.get(it, 10000) - _q1233
            if hour == 23 and (s + 1) // TPD % 3 == 0 and (len(shops) < 8):
                shops = shops + ['_']
            if _q1086:
                _q946[s] = _q1086
        return _q946

    def forecast(_q1120, _q928=None, H=24, _q952=None):
        if _q928 is not None and (_q1120.step is None or int(_get(_q928, 'step', -1) or -1) != _q1120.step):
            _q1120.observe(_q928)
        t0 = min(_q1120.step if _q1120.step is not None else 0, LAST_STEP)
        _q1177 = min(LAST_STEP + 1, t0 + int(H))
        _q1007 = _q1120.type_posterior()
        _q1060 = {}
        for t, w in _q1007.items():
            if w < 0.03:
                continue
            _q922 = _q1120._run(t, t0, _q1177, _q952)
            for s, _q1086 in _q922.items():
                _q1036 = _q1060.setdefault(s, {})
                for it, _q1233 in _q1086.items():
                    _q1036[it] = _q1036.get(it, 0.0) + w * _q1233
        _q1281 = sum((w for w in _q1007.values() if w >= 0.03))
        if _q1281 > 0 and abs(_q1281 - 1.0) > 1e-09:
            for _q1036 in _q1060.values():
                for it in _q1036:
                    _q1036[it] /= _q1281
        return _q1120._blend(_q1060, t0, _q1177)

    def recent_pattern(_q1120, t0, n=24):
        """-> [24 dicts] of the rival sales observed in steps t0-n .. t0-1 by hour of day (per day of history)."""
        _q971 = [dict() for _ in range(24)]
        days = max(1.0, n / 24.0)
        for s, _q1086 in reversed(_q1120.sold_history):
            if s < t0 - n:
                break
            if s >= t0:
                continue
            _q530 = _q971[s % 24]
            for it, _q1221 in _q1086.items():
                _q530[it] = _q530.get(it, 0.0) + _q1221 / days
        return _q971

    def _blend(_q1120, _q1060, t0, _q1177):
        """Persistence blend per item (weights fitted offline, params['blend']): forecast = w * model +
        (1 - w) * the rival's sales at the same hour over the last day (strong for trade-driven WHEAT / FERTILIZER)."""
        _q418 = _q1120.params.get('blend')
        if not _q418 or t0 < 24:
            return _q1060
        items = [it for it in PRODUCTS if float(_q418.get(it, 1.0)) < 0.999]
        if not items:
            return _q1060
        _q971 = _q1120.recent_pattern(t0)
        for s in range(t0, _q1177):
            _q954 = _q971[s % 24]
            _q1036 = _q1060.get(s)
            for it in items:
                w = float(_q418[it])
                _q1233 = (_q1036.get(it, 0.0) if _q1036 else 0.0) * w + (1.0 - w) * _q954.get(it, 0.0)
                if _q1233 > 0:
                    if _q1036 is None:
                        _q1036 = _q1060.setdefault(s, {})
                    _q1036[it] = _q1233
                elif _q1036 is not None and it in _q1036:
                    del _q1036[it]
        return _q1060

    def forecast_daily(_q1120, _q928=None, H=720, _q952=None):
        f = _q1120.forecast(_q928, H, _q952)
        _q946 = {}
        for s, _q1086 in f.items():
            _q530 = _q946.setdefault(s // TPD, {})
            for it, _q1233 in _q1086.items():
                _q530[it] = _q530.get(it, 0.0) + _q1233
        return _q946

    def sample(_q1120, _q928=None, H=24, rng=None, _q952=None):
        if _q928 is not None and (_q1120.step is None or int(_get(_q928, 'step', -1) or -1) != _q1120.step):
            _q1120.observe(_q928)
        rng = rng or random.Random()
        _q1007 = _q1120.type_posterior()
        _q1036 = rng.random()
        _q369 = 0.0
        _q987 = TYPES[-1]
        for t, w in _q1007.items():
            _q369 += w
            if _q1036 <= _q369:
                _q987 = t
                break
        t0 = min(_q1120.step if _q1120.step is not None else 0, LAST_STEP)
        _q1177 = min(LAST_STEP + 1, t0 + int(H))
        return _q1120._blend(_q1120._run(_q987, t0, _q1177, _q952, rng=rng), t0, _q1177)