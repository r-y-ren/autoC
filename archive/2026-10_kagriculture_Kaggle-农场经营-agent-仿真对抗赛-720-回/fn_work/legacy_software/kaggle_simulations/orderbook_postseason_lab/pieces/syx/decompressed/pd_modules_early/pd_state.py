BOARD = 10
HALF = 5
ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
QUADS = ('NW', 'NE', 'SW', 'SE')
LAND_ORDER = ('NE', 'SW', 'SE')
LAND_PRICES = (1000, 2000, 4000)
CROPS = {'WHEAT': {'seed': 10, 'fyd': 2, 'myd': 4, 'interval': 0, 'max_yield': 6, 'ongoing': False}, 'CARROT': {'seed': 20, 'fyd': 2, 'myd': 3, 'interval': 0, 'max_yield': 4, 'ongoing': False}, 'TOMATO': {'seed': 50, 'fyd': 8, 'myd': 8, 'interval': 1, 'max_yield': 4, 'ongoing': True}, 'STRAWBERRY': {'seed': 100, 'fyd': 10, 'myd': 10, 'interval': 2, 'max_yield': 4, 'ongoing': True}, 'MELON': {'seed': 80, 'fyd': 10, 'myd': 12, 'interval': 0, 'max_yield': 6, 'ongoing': False}}
ANIMALS = {'GOOSE': {'cost': 300, 'structure': 'COOP', 'fyd': 4, 'interval': 1, 'max_held': 4, 'product': 'EGG'}, 'COW': {'cost': 400, 'structure': 'PASTURE', 'fyd': 8, 'interval': 2, 'max_held': 6, 'product': 'MILK'}, 'SHEEP': {'cost': 500, 'structure': 'PASTURE', 'fyd': 6, 'interval': 3, 'max_held': 6, 'product': 'WOOL'}}
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
BASE_PRICE = {'WHEAT': 25, 'CARROT': 35, 'TOMATO': 60, 'STRAWBERRY': 120, 'MELON': 250, 'EGG': 50, 'MILK': 160, 'WOOL': 200, 'FERTILIZER': 100}
SHOPS = {'BAKERY': ('EGG', 'WHEAT'), 'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'), 'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'), 'YARN_STORE': ('WOOL',), 'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'), 'PET_CAFE': ('CARROT',), 'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'), 'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY')}
SHOP_TYPES = ('BAKERY', 'PIZZA_SHOP', 'BRUNCH_SPOT', 'YARN_STORE', 'ICE_CREAM_SHOP', 'PET_CAFE', 'SMOOTHIE_SHOP', 'FARMERS_MARKET')
FINAL_DAY = 29

def fib(n):
    a, b = (1, 1)
    for _ in range(n):
        a, b = (b, a + b)
    return a

def hire_cost(_q795, _q809=1):
    """Cost of n_new more hires after n_already today (engine: fib(k) for the k-th hire of the day, k from 0)."""
    return sum((fib(k) for k in range(_q795, _q795 + _q809)))

def quadrant_of(x, _q1197):
    return ('N' if _q1197 < HALF else 'S') + ('W' if x < HALF else 'E')

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def nearest_access(xy):
    return min(ACCESS, key=lambda t: (dist(t, xy), t))

def access_dist(xy):
    return min((dist(t, xy) for t in ACCESS))
QUAD_TILES = {q: tuple(((x, _q1197) for _q1197 in range(BOARD) for x in range(BOARD) if quadrant_of(x, _q1197) == q)) for q in QUADS}

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

class Crop:
    """A standing plant.  age = day - planted_day (0 on the planting day)."""
    __slots__ = ('xy', 'crop', 'planted_day', 'age', 'watered', 'cu', 'units', 'fert_until', 'mls', 'ongoing', 'prods_done', 'prods_left', 'prod_tonight', 'decaying', 'spent', 'must_water')

    def __init__(_q1052, xy, t, day, step):
        c = t.get('crop')
        _q421 = CROPS[c]
        _q1052.xy = xy
        _q1052.crop = c
        _q1052.planted_day = int(t.get('planted_day', day))
        _q1052.age = day - _q1052.planted_day
        _q1052.watered = bool(t.get('watered_today'))
        _q1052.cu = int(t.get('consecutive_unwatered', 0) or 0)
        _q1052.units = int(t.get('yield_units', 0) or 0)
        _q1052.fert_until = int(t.get('fertilized_until_day', -1) if t.get('fertilized_until_day') is not None else -1)
        mls = t.get('max_lifespan_step', -1)
        _q1052.mls = int(mls if mls is not None else -1)
        _q1052.ongoing = _q421['ongoing']
        _q1052.decaying = _q1052.mls >= 0 and step >= _q1052.mls
        _q1052.must_water = not _q1052.watered and _q1052.cu >= 1
        if _q1052.ongoing:
            _q574 = _q421['fyd'] - 1
            _q679 = _q421['interval']
            _q723 = _q574 + _q679 * (_q421['max_yield'] - 1)
            _q501 = 0 if _q1052.age <= _q574 else min(_q421['max_yield'], (_q1052.age - 1 - _q574) // _q679 + 1)
            _q1052.prods_done = _q501
            _q1052.prods_left = _q421['max_yield'] - _q501
            _q1052.prod_tonight = _q574 <= _q1052.age <= _q723 and (_q1052.age - _q574) % _q679 == 0 and (day < FINAL_DAY)
            _q1052.spent = _q1052.prods_left == 0 and _q1052.units == 0
        else:
            _q1052.prods_done = 0
            _q1052.prods_left = 0
            _q1052.prod_tonight = False
            _q1052.spent = False

    def harvestable(_q1052):
        return _q1052.units > 0 and _q1052.age >= CROPS[_q1052.crop]['fyd']

    def water_gain(_q1052, day):
        """Units a WATER today adds (non-ongoing: window gain, capped; ongoing: the fertiliser bonus tonight)."""
        _q421 = CROPS[_q1052.crop]
        if _q1052.watered:
            return 0
        if not _q1052.ongoing:
            _q1190 = (_q421['myd'] + 1) // 2
            if _q1190 <= _q1052.age <= _q421['myd']:
                return max(0, min(_q421['max_yield'], _q1052.units + (2 if _q1052.fert_until >= day else 1)) - _q1052.units)
            return 0
        if _q1052.prod_tonight and _q1052.fert_until >= day:
            return max(0, min(_q421['max_yield'], _q1052.units + 2) - min(_q421['max_yield'], _q1052.units + 1))
        return 0

class Animal:
    __slots__ = ('xy', 'animal', 'kind', 'placed_day', 'age', 'fed', 'cared', 'cuf', 'units', 'fert_avail', 'bank', 'prod_tonight', 'product', 'must_feed', 'next_prod_in')

    def __init__(_q1052, xy, t, day):
        a = t.get('animal')
        _q323 = ANIMALS[a]
        _q1052.xy = xy
        _q1052.animal = a
        _q1052.kind = t.get('kind')
        _q1052.placed_day = int(t.get('placed_day', day))
        _q1052.age = day - _q1052.placed_day
        _q1052.fed = bool(t.get('fed_today'))
        _q1052.cared = bool(t.get('cared_today'))
        _q1052.cuf = int(t.get('consecutive_unfed', 0) or 0)
        _q1052.units = int(t.get('yield_units', 0) or 0)
        _q1052.fert_avail = bool(t.get('fertilizer_available'))
        _q1052.bank = int(t.get('pending_care_bonus', 0) or 0)
        _q1052.product = _q323['product']
        k = _q1052.age + 1 - _q323['fyd']
        _q1052.prod_tonight = k >= 0 and k % _q323['interval'] == 0 and (day < FINAL_DAY)
        if k >= 0:
            _q1052.next_prod_in = -k % _q323['interval']
        else:
            _q1052.next_prod_in = -k
        _q1052.must_feed = not _q1052.fed and _q1052.cuf >= 1

class RivalView:
    __slots__ = ('money', 'quads', 'crop_tiles', 'animals', 'n_units', 'planted_by_day', 'placed_by_day', 'weeds', 'empty')

    def __init__(_q1052):
        _q1052.money = 0.0
        _q1052.quads = 1
        _q1052.crop_tiles = {}
        _q1052.animals = {}
        _q1052.n_units = 1
        _q1052.planted_by_day = {}
        _q1052.placed_by_day = {}
        _q1052.weeds = 0
        _q1052.empty = 0

class FarmState:
    """Derived view of one observation (own farm in full, rival farm as a census).  Never mutates the observation."""
    __slots__ = ('step', 'day', 'hour', 'me', 'opp', 'money', 'tiles', 'crops', 'animals', 'structures', 'weeds', 'empty', 'locked', 'units', 'inventories', 'shed', 'shed_total', 'shed_room', 'seeds', 'quadrants', 'n_quads', 'next_land_price', 'next_land_quad', 'hires_today', 'n_hands', 'shops', 'shop_counts', 'n_shops', 'prices', 'market_inv', 'rival', 'shed_capacity')

    def census(_q1052):
        """{'P_WHEAT': n, ..., 'A_COW': n, ...} standing own tiles / animals."""
        c = {}
        for _q458 in _q1052.crops.values():
            k = 'P_' + _q458.crop
            c[k] = c.get(k, 0) + 1
        for _q336 in _q1052.animals.values():
            k = 'A_' + _q336.animal
            c[k] = c.get(k, 0) + 1
        return c

    def crop_tiles(_q1052, crop):
        return sum((1 for _q458 in _q1052.crops.values() if _q458.crop == crop))

    def n_animals(_q1052, animal=None):
        return sum((1 for a in _q1052.animals.values() if animal is None or a.animal == animal))

    def demand(_q1052, item):
        """Number of open shop instances that buy `item`."""
        return sum((n for s, n in _q1052.shop_counts.items() if item in SHOPS.get(s, ())))

    def demand_units_per_day(_q1052, item):
        """Shop consumption of `item` per day (6 per multi-product shop instance, 12 per single-product one)."""
        _q1147 = 0
        for s, n in _q1052.shop_counts.items():
            _q677 = SHOPS.get(s, ())
            if item in _q677:
                _q1147 += n * (12 if len(_q677) == 1 else 6)
        return _q1147 + (1 if item != 'FERTILIZER' else 0)

    def owned(_q1052, xy):
        return xy not in _q1052.locked

    def free_tiles(_q1052):
        """Tiles that can take a PLANT / BUILD today without clearing a live plant: empty, weeds, spent crops."""
        _q880 = list(_q1052.empty) + list(_q1052.weeds)
        _q880 += [xy for xy, c in _q1052.crops.items() if c.spent]
        return _q880

    def next_hire_cost(_q1052):
        return fib(_q1052.hires_today)

    def planted_in(_q1052, crop, _q476, _q477):
        return sum((1 for c in _q1052.crops.values() if c.crop == crop and _q476 <= c.planted_day <= _q477))

    def placed_in(_q1052, animal, _q476, _q477):
        return sum((1 for a in _q1052.animals.values() if a.animal == animal and _q476 <= a.placed_day <= _q477))

    def tile(_q1052, xy):
        return _q1052.tiles[xy[1]][xy[0]]

def _rival_view(_q552, day):
    _q970 = RivalView()
    _q970.money = float(_get(_q552, 'money', 0.0) or 0.0)
    _q970.quads = len(_get(_q552, 'unlocked_quadrants', ['NW']) or ['NW'])
    _q970.n_units = 1 + len(_get(_q552, 'hands', []) or [])
    tiles = _get(_q552, 'tiles', None) or []
    for _q1018 in tiles:
        for t in _q1018:
            if t is None:
                _q970.empty += 1
                continue
            if not isinstance(t, dict):
                continue
            k = t.get('kind')
            if k == 'PLANT':
                c = t.get('crop')
                _q970.crop_tiles[c] = _q970.crop_tiles.get(c, 0) + 1
                _q911 = int(t.get('planted_day', day))
                key = (c, _q911)
                _q970.planted_by_day[key] = _q970.planted_by_day.get(key, 0) + 1
            elif k == 'WEED':
                _q970.weeds += 1
            elif t.get('animal'):
                a = t.get('animal')
                _q970.animals[a] = _q970.animals.get(a, 0) + 1
                key = (a, int(t.get('placed_day', day)))
                _q970.placed_by_day[key] = _q970.placed_by_day.get(key, 0) + 1
    return _q970

def parse_obs(_q864, shed_capacity=100):
    """observation (dict or Kaggle Struct) -> FarmState for the observing player."""
    s = FarmState()
    me = int(_get(_q864, 'player', 0) or 0)
    day = int(_get(_q864, 'day', 0) or 0)
    hour = int(_get(_q864, 'hour', 0) or 0)
    step = _get(_q864, 'step', None)
    step = int(step) if step is not None else 24 * day + hour
    s.step, s.day, s.hour, s.me, s.opp = (step, day, hour, me, 1 - me)
    s.shed_capacity = shed_capacity
    farms = _get(_q864, 'farms', None) or []
    _q552 = farms[me] if len(farms) > me else {}
    s.money = float(_get(_q552, 'money', 0.0) or 0.0)
    tiles = _get(_q552, 'tiles', None) or [[None] * BOARD for _ in range(BOARD)]
    s.tiles = tiles
    s.crops, s.animals, s.structures = ({}, {}, {})
    s.weeds, s.empty, s.locked = (set(), set(), set())
    for _q1197 in range(BOARD):
        _q1018 = tiles[_q1197]
        for x in range(BOARD):
            t = _q1018[x]
            xy = (x, _q1197)
            if t is None:
                s.empty.add(xy)
            elif t == 'LOCKED' or not isinstance(t, dict):
                s.locked.add(xy)
            else:
                k = t.get('kind')
                if k == 'PLANT':
                    s.crops[xy] = Crop(xy, t, day, step)
                elif k == 'WEED':
                    s.weeds.add(xy)
                elif t.get('animal'):
                    s.animals[xy] = Animal(xy, t, day)
                else:
                    s.structures[xy] = k
    _q587 = _get(_q552, 'farmer', None) or list(ACCESS[0])
    s.units = [tuple(_q587)] + [tuple(h) for h in _get(_q552, 'hands', None) or []]
    s.n_hands = len(s.units) - 1
    _q950 = _get(_q864, 'private', None) or {}
    _q672 = _get(_q950, 'inventories', None) or [{}]
    s.inventories = [dict(_q652) for _q652 in _q672] + [{} for _ in range(len(s.units) - len(_q672))]
    s.shed = {k: int(_q1159) for k, _q1159 in (_get(_q950, 'shed', None) or {}).items() if _q1159}
    s.shed_total = sum(s.shed.values())
    s.shed_room = max(0, shed_capacity - s.shed_total)
    s.seeds = {k: int(_q1159) for k, _q1159 in (_get(_q950, 'seeds', None) or {}).items() if _q1159}
    s.quadrants = list(_get(_q552, 'unlocked_quadrants', None) or ['NW'])
    s.n_quads = len(s.quadrants)
    if s.n_quads < 4:
        s.next_land_price = LAND_PRICES[s.n_quads - 1]
        s.next_land_quad = LAND_ORDER[s.n_quads - 1]
    else:
        s.next_land_price = None
        s.next_land_quad = None
    s.hires_today = int(_get(_q552, 'hires_today', 0) or 0)
    town = _get(_q864, 'town', None) or {}
    s.shops = list(_get(town, 'unlocked_shops', None) or [])
    _q1043 = {}
    for sh in s.shops:
        _q1043[sh] = _q1043.get(sh, 0) + 1
    s.shop_counts = _q1043
    s.n_shops = len(s.shops)
    market = _get(_q864, 'market', None) or {}
    s.prices = dict(_get(market, 'prices', None) or BASE_PRICE)
    s.market_inv = dict(_get(market, 'inventory', None) or {})
    opp = farms[1 - me] if len(farms) > 1 - me else {}
    s.rival = _rival_view(opp, day)
    return s