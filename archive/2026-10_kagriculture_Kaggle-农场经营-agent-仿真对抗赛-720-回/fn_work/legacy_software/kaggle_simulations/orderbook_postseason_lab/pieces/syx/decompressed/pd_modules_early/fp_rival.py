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

def pbin(_q979):
    for _q652, _q520 in enumerate(P_EDGES):
        if _q979 < _q520:
            return _q652
    return len(P_EDGES)

def hbin(held):
    for _q652, _q520 in enumerate(H_EDGES):
        if held < _q520:
            return _q652
    return len(H_EDGES)

def dbin(step):
    if step >= 712:
        return 7
    _q475 = step // TPD
    if _q475 <= 9:
        return 0
    if _q475 <= 14:
        return 1
    if _q475 <= 19:
        return 2
    if _q475 <= 24:
        return 3
    if _q475 <= 27:
        return 4
    if _q475 == 28:
        return 5
    return 6

def leadbin(_q735):
    for _q652, _q520 in enumerate(LEAD_EDGES):
        if _q735 < _q520:
            return _q652
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
        _q1147 = x / T
        return _q1147 + 8.0 * max(0.0, _q1147 - 1.0) ** 2
    return x
_AMP = {}
for _q250, (_b, _q242, _q245, _q246, _q243, _q244) in MP.items():
    _AMP[_q250] = (_q246 * _b / _shape(_q245, _q242, _q242), _q244 * _b / _shape(_q243, _q242, _q242))

def price(item, inv):
    base, T, _q360, _q379, _q326, _q344 = MP[item]
    if inv < 10000:
        _q888 = base + _AMP[item][0] * _shape(_q360, 10000 - inv, T)
    else:
        _q888 = base - _AMP[item][1] * _shape(_q326, inv - 10000, T)
    return max(1, int(round(_q888)))

def drain(shops, step):
    """Town consumption of engine step `step` with the unlocked shop list `shops` -> {item: units}."""
    _q475 = {}
    if step % 4 == 0:
        for sh in shops or ():
            _q955 = SHOPS.get(sh, ())
            m = 2 if len(_q955) == 1 else 1
            for _q675 in _q955:
                _q475[_q675] = _q475.get(_q675, 0) + m
    if step % 24 == 0:
        for _q675 in PRODUCTS:
            if _q675 != 'FERTILIZER':
                _q475[_q675] = _q475.get(_q675, 0) + 1
    return _q475

def _get(_q857, k, _q475=None):
    if isinstance(_q857, dict):
        return _q857.get(k, _q475)
    g = getattr(_q857, 'get', None)
    if callable(g):
        try:
            return g(k, _q475)
        except TypeError:
            pass
    return getattr(_q857, k, _q475)
_PARAMS = None

def load_params(_q906=None):
    global _PARAMS
    if _q906 is None:
        if _PARAMS is not None:
            return _PARAMS
        _q906 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rival_params.json')
    with open(_q906, encoding='utf-8') as _q567:
        _q888 = json.load(_q567)
    _PARAMS = _q888
    return _q888

def _harvest_age_dist(params, _q1023, crop):
    """-> list of (age, prob) of the harvest day relative to planting for a non-ongoing crop."""
    if params:
        t = params.get('hage', {}).get(_q1023, {}).get(crop) or params.get('hage', {}).get('gen', {}).get(crop)
        if t:
            return [(int(a), float(_q888)) for a, _q888 in t]
    return [(CROPS[crop]['myd'], 1.0)]

def _iter_tiles(tiles):
    """Accept a 10x10 engine grid (dicts / None / 'LOCKED') or an iterable of (x, y, dict)."""
    if tiles and isinstance(tiles, (list, tuple)) and tiles and isinstance(tiles[0], (list, tuple)) and (len(tiles[0]) == 0 or not isinstance(tiles[0][0], int)):
        for _q1197, _q1018 in enumerate(tiles):
            for x, t in enumerate(_q1018):
                if isinstance(t, dict):
                    yield (x, _q1197, t)
    else:
        for x, _q1197, t in tiles or ():
            yield (x, _q1197, t)

def tile_supply(tiles, day, hour=23, params=None, _q1023='gen', last_day=29):
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
        pf = float(params.get('fert_cont', {}).get(_q1023, params.get('fert_cont', {}).get('gen', 0.5)))

    def _q324(_q475, _q675, _q1147):
        if _q1147 <= 0:
            return
        if _q475 <= day:
            now[_q675] = now.get(_q675, 0.0) + _q1147
        elif _q475 <= last_day:
            _q484 = days.setdefault(_q475, {})
            _q484[_q675] = _q484.get(_q675, 0.0) + _q1147
    for x, _q1197, t in _iter_tiles(tiles):
        kind = t.get('kind')
        if kind == 'PLANT':
            crop = t.get('crop')
            _q421 = CROPS.get(crop)
            if _q421 is None:
                continue
            _q922 = int(t.get('planted_day', day))
            _q1204 = float(t.get('yield_units', 0) or 0)
            _q598 = int(t.get('fertilized_until_day', -1))
            _q540 = _q598 >= _q922
            watered = bool(t.get('watered_today'))
            if not _q421['ongoing']:
                _q329 = day - _q922
                _q1190 = (_q421['myd'] + 1) // 2
                dist = [(a, _q888) for a, _q888 in _harvest_age_dist(params, _q1023, crop) if a >= _q329]
                if not dist:
                    dist = [(_q329, 1.0)]
                _q1206 = sum((_q888 for _, _q888 in dist))
                for a, _q888 in dist:
                    _q1147 = _q1204
                    for g in range(_q329, a + 1):
                        if g < _q1190 or g > _q421['myd']:
                            continue
                        if g == _q329 and watered:
                            continue
                        _q493 = _q922 + g
                        fert = 1.0 if _q598 >= _q493 else pf if _q540 else 0.0
                        _q1147 += 1.0 + fert
                    _q1147 = min(float(_q421['max_yield']), _q1147)
                    _q324(_q922 + a, crop, _q1147 * _q888 / _q1206)
            else:
                if _q1204 > 0:
                    _q324(day, crop, _q1204)
                for _q520 in range(day, last_day):
                    k = _q520 + 1 - _q922 - _q421['fyd']
                    if k < 0 or k % _q421['interval']:
                        continue
                    _q442 = k // _q421['interval'] + 1
                    if _q442 > _q421['max_yield']:
                        break
                    fert = 1.0 if _q598 >= _q520 else pf if _q540 else 0.0
                    _q324(_q520 + 1, crop, 1.0 + fert)
        elif t.get('animal'):
            a = ANIMALS.get(t.get('animal'))
            if a is None:
                continue
            prod = a['product']
            _q930 = int(t.get('placed_day', day))
            _q1204 = float(t.get('yield_units', 0) or 0)
            if _q1204 > 0:
                _q324(day, prod, _q1204)
            bank = float(t.get('pending_care_bonus', 0) or 0)
            _q413 = 1.0 if t.get('cared_today') or bank > 0 else 0.0
            for _q520 in range(day, last_day):
                k = _q520 + 1 - _q930 - a['fyd']
                if k >= 0 and k % a['interval'] == 0:
                    _q324(_q520 + 1, prod, min(float(a['max_held']), 1.0 + bank))
                    bank = 0.0
                c = (1.0 if t.get('cared_today') else _q413) if _q520 == day else _q413
                bank += c
    return {'now': now, 'days': days}

def count_animals(tiles):
    n = 0
    for x, _q1197, t in _iter_tiles(tiles):
        if t.get('animal'):
            n += 1
    return n

class _Haz:
    """Flattened hazard tables of one type: base[item], A[item][hour], B[item][pb], C[item][db], D[item][hb]."""
    __slots__ = ('base', 'A', 'B', 'C', 'D', 'prof', 'prior', 'frate', 'buyt')

    def __init__(_q1052, params, _q1023):
        _q651 = params['haz'].get(_q1023) or params['haz']['gen']
        _q1052.base = {_q675: float(_q651[_q675]['base']) for _q675 in _q651}
        _q1052.A = {_q675: [float(_q1159) for _q1159 in _q651[_q675]['hour']] for _q675 in _q651}
        _q1052.B = {_q675: [float(_q1159) for _q1159 in _q651[_q675]['pb']] for _q675 in _q651}
        _q1052.C = {_q675: [float(_q1159) for _q1159 in _q651[_q675]['db']] for _q675 in _q651}
        _q1052.D = {_q675: [float(_q1159) for _q1159 in _q651[_q675]['hb']] for _q675 in _q651}
        _q942 = params.get('prof', {})
        _q1052.prof = _q942.get(_q1023) or _q942.get('gen') or {}
        _q1052.prior = params.get('prior', {}).get(_q1023) or params.get('prior', {}).get('gen') or {}
        _q1052.frate = float(params.get('frate', {}).get(_q1023, params.get('frate', {}).get('gen', 0.0)))
        _q1052.buyt = params.get('buy', {}).get(_q1023) or params.get('buy', {}).get('gen') or {}

    def buy(_q1052, _q675, db, hour):
        t = _q1052.buyt.get(_q675)
        if not t:
            return 0.0
        return float(t[db][hour])

    def h(_q1052, _q675, hour, pb, db, hb):
        b = _q1052.base.get(_q675)
        if b is None:
            return 0.0
        _q1159 = b * _q1052.A[_q675][hour] * _q1052.B[_q675][pb] * _q1052.C[_q675][db] * _q1052.D[_q675][hb]
        return 1.0 if _q1159 > 1.0 else _q1159
_HAZ_CACHE = {}

def _haz(params, _q1023):
    k = (id(params), _q1023)
    _q1206 = _HAZ_CACHE.get(k)
    if _q1206 is None:
        _q1206 = _Haz(params, _q1023)
        _HAZ_CACHE[k] = _q1206
    return _q1206

def hazard(params, _q1023, item, hour, _q979, day, step, held):
    """Per-unit probability that a held unit of `item` is sold at this step (type table)."""
    return _haz(params, _q1023).h(item, hour, pbin(_q979), dbin(step), hbin(held))

class RivalModel:

    def __init__(_q1052, params=None, _q1008=None, player=None, _q1118=0.25):
        _q1052.params = params if params is not None else load_params()
        _q1052.fixed = _q1008
        _q1052.player = player
        _q1052.temper = _q1118
        _q1052.step = None
        _q1052._prev = None
        _q1052.shed = {_q675: 0.0 for _q675 in PRODUCTS}
        _q1052.carry = {}
        _q1052.sold_history = []
        _q1052.bought_history = []
        _q1052.loglik = {t: 0.0 for t in TYPES}
        _q1052.cal = {}
        _q1052.bcal = {}
        _q1052.cal_k = (8.0, 3.0)
        _q1052.feat = {'m2': None, 'mel': 0, 'ne': None, 'sw': None, 'nland': 1}
        _q1052._tiles = None
        _q1052._inv = None
        _q1052._px = None
        _q1052._shops = []
        _q1052._day = 0
        _q1052._hour = 0
        _q1052._tstamp = None

    def observe(_q1052, _q863, _q887=None, _q884=None, own_orders=None):
        me = _get(_q863, 'player', _q1052.player)
        me = int(me or 0) if _q1052.player is None else _q1052.player
        _q1052.player = me
        opp = 1 - me
        step = _get(_q863, 'step', None)
        day = int(_get(_q863, 'day', 0) or 0)
        hour = int(_get(_q863, 'hour', 0) or 0)
        step = int(step) if step is not None else TPD * day + hour
        farms = _get(_q863, 'farms', None) or []
        _q998 = farms[opp] if len(farms) > opp else {}
        tiles = _get(_q998, 'tiles', None) or []
        market = _get(_q863, 'market', None) or {}
        inv = dict(_get(market, 'inventory', None) or {})
        px = dict(_get(market, 'prices', None) or {})
        town = _get(_q863, 'town', None) or {}
        shops = list(_get(town, 'unlocked_shops', None) or [])
        _q950 = _get(_q863, 'private', None) or {}
        myshed = dict(_get(_q950, 'shed', None) or {})
        mycarry = {}
        for _q475 in _get(_q950, 'inventories', None) or []:
            for k, _q1159 in dict(_q475).items():
                mycarry[k] = mycarry.get(k, 0) + int(_q1159 or 0)
        units = [tuple(_get(_q998, 'farmer', None) or (4, 4))] + [tuple(h) for h in _get(_q998, 'hands', None) or []]
        _q1011 = float(_get(_q998, 'money', 0.0) or 0.0)
        _q467 = {'step': step, 'tiles': tiles, 'inv': inv, 'shops': shops, 'myshed': myshed, 'mycarry': mycarry, 'units': units, 'day': day, 'hour': hour, 'px': px}
        _q947 = _q1052._prev
        if _q947 is not None and step == _q947['step'] + 1 and inv and _q947['inv']:
            _q1052._account_market(_q947, _q467, _q887, _q884, own_orders)
            _q1052._account_tiles(_q947, _q467)
        elif _q947 is not None and step != _q947['step']:
            _q1052._account_tiles(_q947, _q467)
        _q1052._features(step, day, tiles, _q1011)
        _q1052._prev = _q467
        _q1052.step, _q1052._day, _q1052._hour = (step, day, hour)
        _q1052._tiles, _q1052._inv, _q1052._px, _q1052._shops = (tiles, inv, px, shops)
        _q1052._tstamp = (day, hour)

    def _account_market(_q1052, _q947, _q467, _q887, _q884, own_orders):
        s = _q947['step']
        _q505 = drain(_q947['shops'], s)
        _q991, _q990 = ({}, {})
        for _q857 in (own_orders or [])[:10]:
            try:
                if len(_q857) >= 3 and int(_q857[2]) > 0:
                    if _q857[0] == 'SELL':
                        _q991[_q857[1]] = _q991.get(_q857[1], 0) + int(_q857[2])
                    elif _q857[0] == 'BUY_PRODUCT':
                        _q990[_q857[1]] = _q990.get(_q857[1], 0) + int(_q857[2])
            except Exception:
                continue
        sold, _q375 = ({}, {})
        for _q675 in PRODUCTS:
            if _q675 not in _q467['inv'] or _q675 not in _q947['inv']:
                continue
            _q1133 = int(_q467['inv'][_q675]) - int(_q947['inv'][_q675]) + _q505.get(_q675, 0)
            if _q887 is not None or _q884 is not None:
                _q777 = int((_q887 or {}).get(_q675, 0)) - int((_q884 or {}).get(_q675, 0))
            else:
                cap = int(_q947['myshed'].get(_q675, 0)) + int(_q947['mycarry'].get(_q675, 0))
                ms = min(_q991.get(_q675, 0), cap)
                if price(_q675, int(_q947['inv'][_q675])) <= 1:
                    ms = 0
                _q777 = ms - _q990.get(_q675, 0)
            _q970 = _q1133 - _q777
            if _q970 > 0:
                sold[_q675] = _q970
            elif _q970 < 0 and _q675 in ('WHEAT', 'FERTILIZER'):
                _q375[_q675] = -_q970
        if sold:
            _q1052.sold_history.append((s, sold))
        if _q375:
            _q1052.bought_history.append((s, _q375))
        _q1052._bayes(s, _q947, sold, _q375)
        for _q675, _q1147 in sold.items():
            _q1114 = min(_q1052.shed.get(_q675, 0.0), float(_q1147))
            _q1052.shed[_q675] = _q1052.shed.get(_q675, 0.0) - _q1114
            rest = float(_q1147) - _q1114
            if rest > 0:
                for c in _q1052.carry.values():
                    k = min(c.get(_q675, 0.0), rest)
                    if k > 0:
                        c[_q675] -= k
                        rest -= k
        for _q675, _q1147 in _q375.items():
            _q1052.shed[_q675] = _q1052.shed.get(_q675, 0.0) + _q1147

    def _bayes(_q1052, s, _q947, sold, _q375=None):
        """Tempered Poisson log-likelihood of the observed sales per type (GOODS; exposure = estimated shed) and the
        per-rival calibration accumulators: observed vs predicted sales per item and per (item, hour), observed vs
        expected buys of WHEAT / FERTILIZER (gamma-Poisson shrinkage in _mult())."""
        _q32 = _q1052.params
        hour = s % TPD
        db = dbin(s)
        _q1146 = TYPES if _q1052.fixed is None else (_q1052.fixed,)
        _q433 = {}
        for c in _q1052.carry.values():
            for _q675, _q1147 in c.items():
                _q433[_q675] = _q433.get(_q675, 0.0) + _q1147
        for t in _q1146:
            _q651 = _haz(_q32, t)
            _q399 = _q1052.cal.setdefault(t, {})
            _q746 = 0.0
            for _q675 in PRODUCTS:
                held = _q1052.shed.get(_q675, 0.0) + _q433.get(_q675, 0.0) * 0.5
                x = sold.get(_q675, 0)
                if held < 0.5 and x == 0:
                    continue
                _q979 = int(_q947['px'].get(_q675, BASE[_q675]) or BASE[_q675]) / float(BASE[_q675])
                _q520 = max(held, float(x))
                lam = _q520 * _q651.h(_q675, hour, pbin(_q979), db, hbin(_q520))
                c = _q399.get(_q675)
                if c is None:
                    c = _q399[_q675] = [0.0, 0.0, [0.0] * 24, [0.0] * 24]
                c[0] += x
                c[1] += lam
                c[2][hour] += x
                c[3][hour] += lam
                if _q675 in GOODS and _q1052.fixed is None:
                    lam = max(0.001, lam)
                    _q746 += x * math.log(lam) - lam
            _q1052.loglik[t] += _q1052.temper * _q746
            _q353 = _q1052.bcal.setdefault(t, {})
            for _q675 in ('WHEAT', 'FERTILIZER'):
                _q525 = _q651.buy(_q675, db, hour)
                b = _q353.get(_q675)
                if b is None:
                    b = _q353[_q675] = [0.0, 0.0]
                b[0] += (_q375 or {}).get(_q675, 0)
                b[1] += _q525

    def _mult(_q1052, _q1023):
        """-> ({item: [24 hazard multipliers]}, {item: buy multiplier}) from the calibration accumulators."""
        K, k = _q1052.cal_k
        _q880 = {}
        for _q675, c in _q1052.cal.get(_q1023, {}).items():
            mi = (c[0] + K) / (c[1] + K)
            _q880[_q675] = [min(5.0, max(0.2, (c[2][h] + k * mi) / (c[3][h] + k))) for h in range(24)]
        _q372 = {}
        for _q675, b in _q1052.bcal.get(_q1023, {}).items():
            _q372[_q675] = min(5.0, max(0.1, (b[0] + 20.0) / (b[1] + 20.0)))
        return (_q880, _q372)

    def _account_tiles(_q1052, _q947, _q467):
        _q958 = {}
        for x, _q1197, t in _iter_tiles(_q947['tiles']):
            _q958[x, _q1197] = t
        _q461 = {}
        for x, _q1197, t in _iter_tiles(_q467['tiles']):
            _q461[x, _q1197] = t
        _q842 = _q467['day'] != _q947['day']
        _q1152 = {}
        for _q652, _q1147 in enumerate(_q467['units']):
            _q1152.setdefault(_q1147, _q652)
        _q629 = []
        for xy, a in _q958.items():
            b = _q461.get(xy)
            _q1200 = float(a.get('yield_units', 0) or 0)
            if a.get('kind') == 'PLANT':
                crop = a.get('crop')
                _q421 = CROPS.get(crop)
                if _q421 is None:
                    continue
                _q1037 = b is not None and b.get('kind') == 'PLANT' and (b.get('crop') == crop) and (b.get('planted_day') == a.get('planted_day'))
                if _q1037 and int(b.get('fertilized_until_day', -1)) > int(a.get('fertilized_until_day', -1)):
                    _q629.append((xy, 'FERTILIZER', -1.0))
                if not _q421['ongoing']:
                    replant = b is not None and b.get('kind') == 'PLANT' and (int(b.get('planted_day', -1)) == _q467['day']) and (_q467['day'] != int(a.get('planted_day', -1)))
                    if not _q1037 and _q1200 > 0 and (b is None or replant):
                        _q629.append((xy, crop, _q1200))
                elif _q1037:
                    _q1201 = float(b.get('yield_units', 0) or 0)
                    if _q842:
                        k = _q467['day'] - int(a.get('planted_day', 0)) - _q421['fyd']
                        prod = 0.0
                        if k >= 0 and k % _q421['interval'] == 0 and (k // _q421['interval'] + 1 <= _q421['max_yield']):
                            prod = 1.0
                        if _q1200 > 0 and _q1201 <= prod + 1.0 and (_q1201 < _q1200 + prod):
                            _q629.append((xy, crop, _q1200))
                    elif _q1200 > 0 and _q1201 == 0 and (_q1200 >= 2):
                        _q629.append((xy, crop, _q1200))
                    elif _q1200 == 1 and _q1201 == 0:
                        if xy in _q1152:
                            _q629.append((xy, crop, _q1200))
                elif _q1200 > 0 and b is None:
                    _q629.append((xy, crop, _q1200))
            elif a.get('animal'):
                _q336 = ANIMALS.get(a.get('animal'))
                if _q336 is None:
                    continue
                _q1037 = b is not None and b.get('animal') == a.get('animal') and (b.get('placed_day') == a.get('placed_day'))
                if not _q1037:
                    continue
                _q1201 = float(b.get('yield_units', 0) or 0)
                if not _q842:
                    if _q1200 > 0 and _q1201 == 0:
                        _q629.append((xy, _q336['product'], _q1200))
                    if b.get('fed_today') and (not a.get('fed_today')):
                        _q629.append((xy, 'WHEAT', -1.0))
                    if a.get('fertilizer_available') and (not b.get('fertilizer_available')):
                        _q629.append((xy, 'FERTILIZER', 1.0))
                elif _q1200 > 0 and _q1201 < _q1200:
                    _q629.append((xy, _q336['product'], _q1200))
        for xy, _q675, _q1147 in _q629:
            if _q1147 < 0:
                _q652 = _q1152.get(xy)
                c = _q1052.carry.get(_q652) if _q652 is not None else None
                if c is not None and c.get(_q675, 0.0) >= 1.0:
                    c[_q675] -= 1.0
                else:
                    _q1052.shed[_q675] = max(0.0, _q1052.shed.get(_q675, 0.0) - 1.0)
                continue
            _q652 = _q1152.get(xy, 0)
            c = _q1052.carry.setdefault(_q652, {})
            c[_q675] = c.get(_q675, 0.0) + _q1147
        if _q842:
            for c in _q1052.carry.values():
                for _q675, _q1147 in c.items():
                    _q1052.shed[_q675] = _q1052.shed.get(_q675, 0.0) + _q1147
            _q1052.carry = {}
        else:
            for _q652, _q1147 in enumerate(_q467['units']):
                if _q1147 in ACCESS and _q652 in _q1052.carry:
                    for _q675, _q1159 in _q1052.carry[_q652].items():
                        _q1052.shed[_q675] = _q1052.shed.get(_q675, 0.0) + _q1159
                    del _q1052.carry[_q652]
        _q1133 = sum(_q1052.shed.values())
        if _q1133 > 100:
            f = 100.0 / _q1133
            for _q675 in _q1052.shed:
                _q1052.shed[_q675] *= f

    def _features(_q1052, step, day, tiles, _q1011):
        f = _q1052.feat
        if step == 2 and f['m2'] is None:
            f['m2'] = _q1011
        if day <= 1:
            n = 0
            for x, _q1197, t in _iter_tiles(tiles):
                if t.get('crop') == 'MELON' and int(t.get('planted_day', 9)) <= 1:
                    n += 1
            f['mel'] = max(f['mel'], n)
        _q847 = 1
        _q1050 = set()
        for _q1197, _q1018 in enumerate(tiles or []):
            for x, t in enumerate(_q1018):
                if t != 'LOCKED':
                    _q1050.add(('N' if _q1197 < 5 else 'S') + ('W' if x < 5 else 'E'))
        _q847 = max(1, len(_q1050))
        if _q847 >= 2 and f['ne'] is None:
            f['ne'] = step - 1
        if _q847 >= 3 and f['sw'] is None:
            f['sw'] = step - 1
        f['nland'] = _q847

    def _feature_loglik(_q1052, t):
        _q32 = _q1052.params.get('typefeat', {})
        tf = _q32.get(t)
        if not tf:
            return 0.0
        f = _q1052.feat
        _q746 = 0.0
        if f['m2'] is not None:
            _q746 += math.log(tf['m2lo'] if f['m2'] < 1000 else 1.0 - tf['m2lo'])
        if _q1052.step is not None and _q1052.step >= 47:
            _q746 += math.log(tf['mel12'] if f['mel'] >= 12 else 1.0 - tf['mel12'])
        for key in ('ne', 'sw'):
            _q639 = tf[key]
            if f[key] is not None:
                b = min(71, f[key] // 10)
                _q746 += math.log(_q639[b])
            elif _q1052.step is not None:
                _q348 = min(72, _q1052.step // 10 + 1)
                _q746 += math.log(max(1e-06, sum(_q639[_q348:])))
        return _q746

    def type_posterior(_q1052):
        if _q1052.fixed is not None:
            return {_q1052.fixed: 1.0}
        _q948 = _q1052.params.get('typeprior', {})
        _q740 = {}
        for t in TYPES:
            _q740[t] = math.log(_q948.get(t, 0.2)) + _q1052._feature_loglik(t) + _q1052.loglik[t]
        m = max(_q740.values())
        w = {t: math.exp(_q1159 - m) for t, _q1159 in _q740.items()}
        _q1206 = sum(w.values())
        w = {t: max(0.0001, _q1159 / _q1206) for t, _q1159 in w.items()}
        _q1206 = sum(w.values())
        return {t: _q1159 / _q1206 for t, _q1159 in w.items()}

    def set_state(_q1052, step, tiles, inv, px, shops, shed=None, carry=None, _q1127=None):
        """Offline evaluation hook: install a public state (and optionally a known shed) without observe().
        tiles_step = the step at which the tile snapshot was observed (default: step)."""
        _q1052.step, _q1052._day, _q1052._hour = (int(step), int(step) // TPD, int(step) % TPD)
        ts = int(step) if _q1127 is None else int(_q1127)
        _q1052._tstamp = (ts // TPD, ts % TPD)
        _q1052._tiles, _q1052._inv, _q1052._px, _q1052._shops = (tiles, dict(inv), dict(px), list(shops))
        if shed is not None:
            _q1052.shed = {_q675: float(shed.get(_q675, 0)) for _q675 in PRODUCTS}
        if carry is not None:
            _q1052.carry = carry

    def stock(_q1052):
        _q1138 = {}
        for c in _q1052.carry.values():
            for _q675, _q1147 in c.items():
                _q1138[_q675] = _q1138.get(_q675, 0.0) + _q1147
        return {'shed': dict(_q1052.shed), 'transit': _q1138}

    def _inflows(_q1052, _q1023, t0, _q1106):
        """-> {step: {item: expected shed inflow}} for steps t0..t1-1 of one type (tile supply + prior + transit)."""
        _q32 = _q1052.params
        _q651 = _haz(_q32, _q1023)
        _q481 = t0 // TPD
        h0 = t0 % TPD
        _q1117, _q1122 = _q1052._tstamp if _q1052._tstamp is not None else (_q481, h0)
        sup = tile_supply(_q1052._tiles, _q1117, _q1122, _q32, _q1023)
        _q880 = {}

        def _q1083(_q475, _q675, _q1147, _q648=0):
            if _q1147 <= 0:
                return
            prof = _q651.prof.get(_q675)
            if not prof:
                prof = [1.0 / 24] * 24
            _q1206 = sum(prof[_q648:])
            if _q1206 <= 0:
                prof = [1.0 / 24] * 24
                _q1206 = sum(prof[_q648:])
            for h in range(_q648, 24):
                s = _q475 * TPD + h
                if s < t0 or s >= _q1106:
                    continue
                _q1159 = _q1147 * prof[h] / _q1206
                if _q1159 > 0:
                    _q857 = _q880.setdefault(s, {})
                    _q857[_q675] = _q857.get(_q675, 0.0) + _q1159
        for _q675, _q1147 in sup['now'].items():
            prof = _q651.prof.get(_q675) or [1.0 / 24] * 24
            m = min(1.0, sum(prof[_q1122:]))
            _q1083(_q1117, _q675, _q1147 * m, _q1122)
            _q1083(_q1117 + 1, _q675, _q1147 * (1.0 - m))
        for _q475, _q484 in sup['days'].items():
            for _q675, _q1147 in _q484.items():
                _q1083(_q475, _q675, _q1147)
        _q942 = _q651.prior
        _q825 = count_animals(_q1052._tiles)
        last_day = min(29, (_q1106 - 1) // TPD)
        for _q475 in range(_q481, last_day + 1):
            _q731 = str(leadbin(_q475 - _q481))
            for _q675 in PRODUCTS:
                _q1018 = _q942.get(_q675)
                if not _q1018:
                    continue
                _q1159 = _q1018.get(str(_q475), {}).get(_q731)
                if _q1159:
                    _q1135 = sup['days'].get(_q475, {}).get(_q675, 0.0) + (sup['now'].get(_q675, 0.0) if _q475 == _q481 else 0.0)
                    _q1159 = max(-_q1135, float(_q1159))
                    if _q475 == _q481:
                        _q1159 *= sum((_q651.prof.get(_q675) or [1.0 / 24] * 24)[h0:])
                    if _q1159 > 0:
                        _q1083(_q475, _q675, _q1159, h0 if _q475 == _q481 else 0)
                    elif _q1159 < 0:
                        _q1044 = (_q1135 + _q1159) / _q1135 if _q1135 > 0 else 1.0
                        for h in range(h0 if _q475 == _q481 else 0, 24):
                            s = _q475 * TPD + h
                            _q857 = _q880.get(s)
                            if _q857 and _q675 in _q857:
                                _q857[_q675] *= _q1044
            if _q651.frate > 0 and _q825:
                _q1083(_q475, 'FERTILIZER', _q651.frate * _q825, h0 if _q475 == _q481 else 0)
        for c in _q1052.carry.values():
            for _q675, _q1147 in c.items():
                for k, f in ((t0, 0.5), (t0 + 1, 0.5)):
                    if k < _q1106:
                        _q857 = _q880.setdefault(k, {})
                        _q857[_q675] = _q857.get(_q675, 0.0) + _q1147 * f
        return _q880

    def _run(_q1052, _q1023, t0, _q1106, _q886=None, rng=None):
        _q32 = _q1052.params
        _q651 = _haz(_q32, _q1023)
        _q664 = _q1052._inflows(_q1023, t0, _q1106)
        _q788, _q373 = _q1052._mult(_q1023)
        _q390 = [_q675 for _q675 in ('WHEAT', 'FERTILIZER') if _q651.buyt.get(_q675)]
        held = {_q675: max(0.0, _q1159) for _q675, _q1159 in _q1052.shed.items()}
        inv = {_q675: int(_q1159) for _q675, _q1159 in (_q1052._inv or {}).items()}
        shops = list(_q1052._shops or [])
        _q880 = {}
        for s in range(t0, _q1106):
            hour = s % TPD
            db = dbin(s)
            _q1018 = {}
            op = _q886.get(s) if _q886 else None
            for _q675 in PRODUCTS:
                _q650 = held.get(_q675, 0.0)
                if _q650 > 1e-06:
                    _q679 = inv.get(_q675, 10000)
                    _q970 = price(_q675, _q679) / float(BASE[_q675])
                    h = _q651.h(_q675, hour, pbin(_q970), db, hbin(_q650))
                    mi = _q788.get(_q675)
                    if mi is not None:
                        h = min(1.0, h * mi[hour])
                    if rng is None:
                        x = _q650 * h
                    else:
                        n = int(_q650)
                        if rng.random() < _q650 - n:
                            n += 1
                        x = float(sum((1 for _ in range(n) if rng.random() < h))) if n < 60 else float(max(0, int(round(rng.gauss(n * h, math.sqrt(max(1e-09, n * h * (1 - h))))))))
                    if x > 0:
                        _q1018[_q675] = x
                        held[_q675] = _q650 - x
                        if price(_q675, _q679) > 1:
                            inv[_q675] = _q679 + int(round(x)) if rng is not None else _q679 + x
                if op and _q675 in op:
                    inv[_q675] = inv.get(_q675, 10000) + op[_q675]
            f = _q664.get(s)
            if f:
                for _q675, _q1159 in f.items():
                    held[_q675] = max(0.0, held.get(_q675, 0.0) + _q1159)
            for _q675 in _q390:
                _q1159 = _q651.buy(_q675, db, hour) * _q373.get(_q675, 1.0)
                if _q1159 > 0:
                    held[_q675] = held.get(_q675, 0.0) + _q1159
                    inv[_q675] = inv.get(_q675, 10000) - _q1159
            _q505 = drain(shops, s)
            for _q675, _q1159 in _q505.items():
                inv[_q675] = inv.get(_q675, 10000) - _q1159
            if hour == 23 and (s + 1) // TPD % 3 == 0 and (len(shops) < 8):
                shops = shops + ['_']
            if _q1018:
                _q880[s] = _q1018
        return _q880

    def forecast(_q1052, _q863=None, H=24, _q886=None):
        if _q863 is not None and (_q1052.step is None or int(_get(_q863, 'step', -1) or -1) != _q1052.step):
            _q1052.observe(_q863)
        t0 = min(_q1052.step if _q1052.step is not None else 0, LAST_STEP)
        _q1106 = min(LAST_STEP + 1, t0 + int(H))
        _q940 = _q1052.type_posterior()
        _q992 = {}
        for t, w in _q940.items():
            if w < 0.03:
                continue
            _q857 = _q1052._run(t, t0, _q1106, _q886)
            for s, _q1018 in _q857.items():
                _q970 = _q992.setdefault(s, {})
                for _q675, _q1159 in _q1018.items():
                    _q970[_q675] = _q970.get(_q675, 0.0) + w * _q1159
        _q1206 = sum((w for w in _q940.values() if w >= 0.03))
        if _q1206 > 0 and abs(_q1206 - 1.0) > 1e-09:
            for _q970 in _q992.values():
                for _q675 in _q970:
                    _q970[_q675] /= _q1206
        return _q1052._blend(_q992, t0, _q1106)

    def recent_pattern(_q1052, t0, n=24):
        """-> [24 dicts] of the rival sales observed in steps t0-n .. t0-1 by hour of day (per day of history)."""
        _q905 = [dict() for _ in range(24)]
        days = max(1.0, n / 24.0)
        for s, _q1018 in reversed(_q1052.sold_history):
            if s < t0 - n:
                break
            if s >= t0:
                continue
            _q475 = _q905[s % 24]
            for _q675, _q1147 in _q1018.items():
                _q475[_q675] = _q475.get(_q675, 0.0) + _q1147 / days
        return _q905

    def _blend(_q1052, _q992, t0, _q1106):
        """Persistence blend per item (weights fitted offline, params['blend']): forecast = w * model +
        (1 - w) * the rival's sales at the same hour over the last day (strong for trade-driven WHEAT / FERTILIZER)."""
        _q366 = _q1052.params.get('blend')
        if not _q366 or t0 < 24:
            return _q992
        items = [_q675 for _q675 in PRODUCTS if float(_q366.get(_q675, 1.0)) < 0.999]
        if not items:
            return _q992
        _q905 = _q1052.recent_pattern(t0)
        for s in range(t0, _q1106):
            _q888 = _q905[s % 24]
            _q970 = _q992.get(s)
            for _q675 in items:
                w = float(_q366[_q675])
                _q1159 = (_q970.get(_q675, 0.0) if _q970 else 0.0) * w + (1.0 - w) * _q888.get(_q675, 0.0)
                if _q1159 > 0:
                    if _q970 is None:
                        _q970 = _q992.setdefault(s, {})
                    _q970[_q675] = _q1159
                elif _q970 is not None and _q675 in _q970:
                    del _q970[_q675]
        return _q992

    def forecast_daily(_q1052, _q863=None, H=720, _q886=None):
        f = _q1052.forecast(_q863, H, _q886)
        _q880 = {}
        for s, _q1018 in f.items():
            _q475 = _q880.setdefault(s // TPD, {})
            for _q675, _q1159 in _q1018.items():
                _q475[_q675] = _q475.get(_q675, 0.0) + _q1159
        return _q880

    def sample(_q1052, _q863=None, H=24, rng=None, _q886=None):
        if _q863 is not None and (_q1052.step is None or int(_get(_q863, 'step', -1) or -1) != _q1052.step):
            _q1052.observe(_q863)
        rng = rng or random.Random()
        _q940 = _q1052.type_posterior()
        _q970 = rng.random()
        _q319 = 0.0
        _q921 = TYPES[-1]
        for t, w in _q940.items():
            _q319 += w
            if _q970 <= _q319:
                _q921 = t
                break
        t0 = min(_q1052.step if _q1052.step is not None else 0, LAST_STEP)
        _q1106 = min(LAST_STEP + 1, t0 + int(H))
        return _q1052._blend(_q1052._run(_q921, t0, _q1106, _q886, rng=rng), t0, _q1106)