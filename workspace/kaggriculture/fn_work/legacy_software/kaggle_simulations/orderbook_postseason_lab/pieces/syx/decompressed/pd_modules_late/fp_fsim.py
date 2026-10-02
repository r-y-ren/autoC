"""fsim - fast, exact market simulator for planning (Original work, Shawn404, 28 Sep 2026).

Pure Python (no numpy, no engine import, no file access).  Reproduces the kaggriculture engine's market phase and town
consumption exactly (kaggle_environments/envs/kaggriculture/kaggriculture.py: market_price, _process_market,
_commit_unit, _town_consume, the shop unlock in _end_of_day).  Validated to the dollar on recorded games
(tools/tmp/fp/fsim/, results/portable/fp_fsim.txt).

API
---
    from tools.fp.fsim import MarketSim, price, buy_price, sell_walk, plan_value

    sim = MarketSim.from_obs(obs, drain_mode='expected')      # obs = the agent's observation (dict or object)
    sim = MarketSim(inventory, shops, step, drain_mode='expected', future_shops=None, rng=None)

  Time convention: sim.step = the NEXT processing index = the obs step the agent is acting on.  The agent's orders
  at obs step s run in the market of index s, then the town drains of index s (every shop instance at s % 4 == 0,
  single-product shops x2; the town centre at s % 24 == 0: -1 of every product except FERTILIZER).  After
  sim.advance(to_step) the inventory equals what the observation at to_step shows.

  Shops: `shops` = obs.town.unlocked_shops (instance n, 1-based, is active from step 72 n; at most 8 instances).
  Instances not yet unlocked are unknown to the agent (the engine draws rng.choice(sorted(SHOPS)) with an RNG seeded
  by the hidden episode seed), so `drain_mode` picks the model for them:
      'fixed'    - no further unlocks (the current list forever);
      'expected' - each future instance drains the mean over the 8 shops (fractional inventory; default);
      'sample'   - each future instance drawn uniformly with replacement from `rng` (random.Random) - one scenario;
      'known'    - `future_shops` gives the whole list (validation / what-if).  future_shops may also be passed with
                   any mode: it overrides the model for the instances it covers.

  Quotes / walks (pure functions, also methods using the sim's inventory):
    price(item, inv)                  -> engine quote (int >= 1) at inventory inv (SELL quote)
    warm(lo=8500, hi=12500)           -> pre-fill the quote caches (call once at agent load)
    buy_price(item, inv)              -> BUY_PRODUCT quote = price(item, inv - 1)
    sell_walk(item, units, inv)       -> (revenue, inv_after): the unit-by-unit walk of one lot as the engine executes
                                         it alone (a unit sold at $1 adds no supply)
    sim.quote(item, inv=None), sim.sell_value(item, units, inv=None) -> revenue of a lot sold now (no mutation)

  Market phase of one step (exact engine semantics, both seats, index-by-index lockstep, max 10 orders per seat):
    res = sim.market(orders0, orders1, sheds=None, money=None, hires=None, quads=None, shed_cap=100)
       orders = engine market lists ([["SELL", item, n], ["BUY_PRODUCT", "WHEAT", n], ["HIRE"], ...]) or the plan
       shorthand ({item: units} or [(item, units), ...] = SELL orders in that order).  sheds / money / hires / quads
       are per-seat lists (None = unlimited: every unit executes); sheds are mutated like the engine's.
       res = [{'rev': sales $, 'cost': purchases $, 'trades': {(op, item): [units, value]}}, {...}]
    sim.drain()                        -> apply the town drains of index sim.step and step += 1 (market not run)
    sim.step_once(orders0, orders1, **kw) = market + drain

  Horizon:
    out = sim.advance(to_step, plans=(plan0, plan1), **kw)
        plan = {step: orders} (orders as above); runs market(step) + drains for every index sim.step .. to_step-1.
        out = {'rev': [r0, r1], 'rev_item': [{item: $}, {item: $}], 'units': [{item: n}, {item: n}]}
    plan_value(sim, our_plan, rival_plan, to_step, our_seat=0, **kw)
        -> {'our': $, 'rival': $, 'our_item', 'rival_item', 'inv'}   (sim is not mutated)
    sim.quote_path(item, to_step)      -> quotes at each obs step sim.step+1 .. to_step with no sales (drains only)
    sim.copy()

Engine facts reproduced (all verified on recorded games):
  * quote = max(1, int(round(base +/- amp * f(|inv - 10000|)))) with the MARKET_PARAMS curves;
  * at order index i both seats quote the SAME pre-commit inventory for their current unit, then both commit; a SELL
    unit at $1 adds no inventory; BUY_PRODUCT (WHEAT / FERTILIZER only) pays quote(inv - 1) and removes one unit;
    HIRE / BUY_LAND are handled first at their index (seat order); a failed commit (empty shed / no money / full shed)
    aborts that order; malformed orders are skipped; each seat's list is cut to 10 orders;
  * seat order never changes prices (both quote before either commits), so a plan's value does not depend on seats.
"""
import math
import random
I0 = 10000
PRODUCTS = ['WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER']
MARKET_PARAMS = {'WHEAT': {'base': 25, 'T': 400, 'below_func': 'sqrt', 'below_target': 0.8, 'above_func': 'log', 'above_target': 0.2}, 'CARROT': {'base': 35, 'T': 450, 'below_func': 'hinge', 'below_target': 1.0, 'above_func': 'sqrt', 'above_target': 0.7}, 'TOMATO': {'base': 60, 'T': 200, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'sqrt', 'above_target': 0.6}, 'STRAWBERRY': {'base': 120, 'T': 100, 'below_func': 'sqrt', 'below_target': 0.7, 'above_func': 'linear', 'above_target': 1.6}, 'MELON': {'base': 250, 'T': 300, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.6}, 'EGG': {'base': 50, 'T': 332, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'log', 'above_target': 0.2}, 'MILK': {'base': 160, 'T': 122, 'below_func': 'sqrt', 'below_target': 0.6, 'above_func': 'linear', 'above_target': 1.6}, 'WOOL': {'base': 200, 'T': 105, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.2}, 'FERTILIZER': {'base': 100, 'T': 200, 'below_func': 'linear', 'below_target': 0.4, 'above_func': 'linear', 'above_target': 0.4}}
HINGE_GAIN = 8.0
SHOPS = {'BAKERY': ['EGG', 'WHEAT'], 'PIZZA_SHOP': ['MILK', 'TOMATO', 'WHEAT'], 'BRUNCH_SPOT': ['EGG', 'WHEAT', 'STRAWBERRY'], 'YARN_STORE': ['WOOL'], 'ICE_CREAM_SHOP': ['STRAWBERRY', 'MILK', 'WHEAT'], 'PET_CAFE': ['CARROT'], 'SMOOTHIE_SHOP': ['STRAWBERRY', 'MILK'], 'FARMERS_MARKET': ['WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY']}
SHOP_NAMES = sorted(SHOPS)
TOWN_CENTER = [_q954 for _q954 in PRODUCTS if _q954 != 'FERTILIZER']
MAX_SHOPS = 8
SHOP_SELL_INTERVAL = 4
CENTER_INTERVAL = 24
UNLOCK_STEPS = 72
SEED_PRICE = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
ANIMAL_PRICE = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
LAND_PRICES = [1000, 2000, 4000]
MAX_ORDERS = 10
BUYABLE = ('WHEAT', 'FERTILIZER')
_PRODUCT_SET = frozenset(PRODUCTS)

def _shape(_q656, x, T):
    x = max(0.0, x)
    if _q656 == 'linear':
        return x
    if _q656 == 'sq':
        return x * x
    if _q656 == 'sqrt':
        return math.sqrt(x)
    if _q656 == 'log':
        return math.log(1.0 + x)
    if _q656 == 'log10':
        return math.log10(1.0 + x)
    if _q656 == 'hinge':
        if not T or T <= 0:
            return x
        _q1221 = x / T
        return _q1221 + HINGE_GAIN * max(0.0, _q1221 - 1.0) ** 2
    return x

def _raw_price(item, inventory):
    """Bit-for-bit copy of the engine's market_price (same float operation order)."""
    _q954 = MARKET_PARAMS[item]
    base = _q954['base']
    T = _q954['T']
    if inventory < I0:
        f = _q954['below_func']
        _q387 = _q954['below_target'] * base / _shape(f, T, T)
        _q1009 = base + _q387 * _shape(f, I0 - inventory, T)
    else:
        f = _q954['above_func']
        _q387 = _q954['above_target'] * base / _shape(f, T, T)
        _q1009 = base - _q387 * _shape(f, inventory - I0, T)
    return max(1, int(round(_q1009)))
_CACHE = {it: {} for it in PRODUCTS}

def price(item, inv):
    """Engine SELL quote at inventory inv (int or float)."""
    c = _CACHE[item]
    q = c.get(inv)
    if q is None:
        q = _raw_price(item, inv)
        if len(c) < 200000:
            c[inv] = q
    return q

def warm(lo=8500, hi=12500):
    """Pre-fill the quote caches for integer inventories lo..hi (all items; ~25 ms for the default range).
    Call once at agent load so no live turn pays the cold-cache cost."""
    for it in PRODUCTS:
        c = _CACHE[it]
        for inv in range(lo, hi + 1):
            if inv not in c:
                c[inv] = _raw_price(it, inv)

def buy_price(item, inv):
    """Engine BUY_PRODUCT quote (post-buy inventory)."""
    return price(item, inv - 1)

def sell_walk(item, units, inv):
    """Sell `units` of item alone, unit by unit, from inventory inv -> (revenue, inventory after)."""
    c = _CACHE[item]
    rev = 0
    k = 0
    while k < units:
        q = c.get(inv)
        if q is None:
            q = price(item, inv)
        if q <= 1:
            rev += units - k
            break
        rev += q
        inv += 1
        k += 1
    return (rev, inv)

def shop_drain(_q1130):
    """{item: units} drained at one shop tick by these shop instances."""
    _q530 = {}
    for s in _q1130:
        _q1021 = SHOPS[s]
        m = 2 if len(_q1021) == 1 else 1
        for it in _q1021:
            _q530[it] = _q530.get(it, 0) + m
    return _q530

def expected_instance_drain():
    """Mean drain of one unknown shop instance (uniform draw over the 8 shops)."""
    _q530 = {}
    for s in SHOP_NAMES:
        for it, n in shop_drain([s]).items():
            _q530[it] = _q530.get(it, 0.0) + n / len(SHOP_NAMES)
    return _q530
_EXP_DRAIN = expected_instance_drain()

def _norm_orders(orders):
    """Plan shorthand -> engine order list, 1:1 (malformed entries kept: they still occupy an index slot)."""
    if not orders:
        return []
    if isinstance(orders, dict):
        return [['SELL', it, n] for it, n in orders.items() if n]
    if not isinstance(orders, (list, tuple)):
        return []
    _q946 = []
    for _q922 in orders:
        if isinstance(_q922, (list, tuple)) and len(_q922) == 2 and (_q922[0] in _PRODUCT_SET):
            _q946.append(['SELL', _q922[0], _q922[1]])
        else:
            _q946.append(_q922)
    return _q946

def _parse(_q938):
    """Engine _parse_order + the malformed-sub-op filter -> (op, item, n) or None."""
    if not isinstance(_q938, (list, tuple)) or not _q938:
        return None
    op = _q938[0]
    if op == 'HIRE' or op == 'BUY_LAND':
        return (op, None, 1)
    if op in ('BUY_SEED', 'BUY_PRODUCT', 'BUY_ANIMAL', 'SELL'):
        if len(_q938) < 3:
            return None
        try:
            n = int(_q938[2])
        except (TypeError, ValueError):
            return None
        if n <= 0:
            return None
        item = _q938[1]
        if op == 'SELL' and item not in _PRODUCT_SET:
            return None
        if op == 'BUY_PRODUCT' and item not in BUYABLE:
            return None
        if op == 'BUY_SEED' and item not in SEED_PRICE:
            return None
        if op == 'BUY_ANIMAL' and item not in ANIMAL_PRICE:
            return None
        return (op, item, n)
    return None

def _fib(n):
    a, b = (1, 1)
    for _ in range(n):
        a, b = (b, a + b)
    return a

def _get(_q922, k, _q530=None):
    if isinstance(_q922, dict):
        return _q922.get(k, _q530)
    return getattr(_q922, k, _q530)

class MarketSim:
    __slots__ = ('inv', 'shops', 'step', 'drain_mode', 'future', '_drains')

    def __init__(_q1120, inventory, shops=(), step=0, drain_mode='expected', _q659=None, rng=None):
        _q1120.inv = {it: inventory.get(it, I0) for it in PRODUCTS}
        _q1120.shops = list(shops or [])
        _q1120.step = int(step)
        _q1120.drain_mode = drain_mode
        _q658 = []
        _q650 = list(_q659 or [])
        for n in range(len(_q1120.shops), MAX_SHOPS):
            if n < len(_q650) and _q650[n] is not None:
                _q658.append(_q650[n])
            elif drain_mode == 'sample':
                _q658.append((rng or random).choice(SHOP_NAMES))
            elif drain_mode == 'fixed':
                _q658.append(False)
            else:
                _q658.append(None)
        _q1120.future = _q658
        _q1120._drains = _q1120._build_drains()

    @classmethod
    def from_obs(_q491, _q928, **_q775):
        market = _get(_q928, 'market', {}) or {}
        town = _get(_q928, 'town', {}) or {}
        inv = _get(market, 'inventory', {}) or {}
        step = _get(_q928, 'step', None)
        if step is None:
            step = 24 * int(_get(_q928, 'day', 0) or 0) + int(_get(_q928, 'hour', 0) or 0)
        return _q491(dict(inv), list(_get(town, 'unlocked_shops', []) or []), int(step), **_q775)

    def copy(_q1120):
        s = MarketSim.__new__(MarketSim)
        s.inv = dict(_q1120.inv)
        s.shops = _q1120.shops
        s.step = _q1120.step
        s.drain_mode = _q1120.drain_mode
        s.future = _q1120.future
        s._drains = _q1120._drains
        return s

    def _build_drains(_q1120):
        _q946 = []
        _q369 = {}
        _q946.append([])
        for n in range(MAX_SHOPS):
            if n < len(_q1120.shops):
                _q530 = shop_drain([_q1120.shops[n]])
            else:
                f = _q1120.future[n - len(_q1120.shops)]
                if f is False:
                    _q530 = {}
                elif f is None:
                    _q530 = _EXP_DRAIN
                else:
                    _q530 = shop_drain([f])
            for it, _q1233 in _q530.items():
                _q369[it] = _q369.get(it, 0) + _q1233
            _q946.append([(it, _q1233) for it, _q1233 in _q369.items() if _q1233])
        return _q946

    def n_active(_q1120, t):
        """Shop instances draining at processing index t."""
        k = t // UNLOCK_STEPS
        if k > MAX_SHOPS:
            k = MAX_SHOPS
        if k < len(_q1120.shops):
            k = len(_q1120.shops)
        return k

    def quote(_q1120, item, inv=None):
        return price(item, _q1120.inv[item] if inv is None else inv)

    def buy_quote(_q1120, item, inv=None):
        return price(item, (_q1120.inv[item] if inv is None else inv) - 1)

    def sell_value(_q1120, item, units, inv=None):
        return sell_walk(item, units, _q1120.inv[item] if inv is None else inv)[0]

    def quote_path(_q1120, item, _q1202):
        s = _q1120.copy()
        _q946 = []
        while s.step < _q1202:
            s.drain()
            _q946.append(price(item, s.inv[item]))
        return _q946

    def drain(_q1120):
        t = _q1120.step
        inv = _q1120.inv
        if t % SHOP_SELL_INTERVAL == 0:
            for it, _q1233 in _q1120._drains[_q1120.n_active(t)]:
                inv[it] -= _q1233
        if t % CENTER_INTERVAL == 0:
            for it in TOWN_CENTER:
                inv[it] -= 1
        _q1120.step = t + 1

    def market(_q1120, _q940=None, _q941=None, _q1129=None, money=None, hires=None, quads=None, _q1127=100):
        """Run the market phase of index self.step (does not advance the step).  See module docstring."""
        inv = _q1120.inv
        q = [[_parse(_q922) for _q922 in _norm_orders(_q940)[:MAX_ORDERS]], [_parse(_q922) for _q922 in _norm_orders(_q941)[:MAX_ORDERS]]]
        _q1060 = [{'rev': 0, 'cost': 0, 'trades': {}}, {'rev': 0, 'cost': 0, 'trades': {}}]
        n = max(len(q[0]), len(q[1]))
        for _q712 in range(n):
            st = [q[_q954][_q712] if _q712 < len(q[_q954]) else None for _q954 in (0, 1)]
            for _q954 in (0, 1):
                _q922 = st[_q954]
                if _q922 is None:
                    continue
                if _q922[0] == 'HIRE':
                    cost = _fib(hires[_q954] if hires is not None else 0)
                    if money is None or money[_q954] >= cost:
                        if money is not None:
                            money[_q954] -= cost
                        if hires is not None:
                            hires[_q954] += 1
                        _q1060[_q954]['cost'] += cost
                        _acc(_q1060[_q954], ('HIRE', None), 1, cost)
                    st[_q954] = None
                elif _q922[0] == 'BUY_LAND':
                    k = quads[_q954] - 1 if quads is not None else 0
                    if k < len(LAND_PRICES):
                        cost = LAND_PRICES[k]
                        if money is None or money[_q954] >= cost:
                            if money is not None:
                                money[_q954] -= cost
                            if quads is not None:
                                quads[_q954] += 1
                            _q1060[_q954]['cost'] += cost
                            _acc(_q1060[_q954], ('BUY_LAND', None), 1, cost)
                    st[_q954] = None
            a, b = st
            if a is None and b is None:
                continue
            if a is not None and b is not None and (a[1] == b[1]) and (a[0] in ('SELL', 'BUY_PRODUCT')) and (b[0] in ('SELL', 'BUY_PRODUCT')):
                _q1120._lockstep(a, b, _q1060, _q1129, money, _q1127)
            else:
                if a is not None:
                    _q1120._solo(0, a, _q1060, _q1129, money, _q1127)
                if b is not None:
                    _q1120._solo(1, b, _q1060, _q1129, money, _q1127)
        return _q1060

    def _solo(_q1120, _q954, _q922, _q1060, _q1129, money, _q1127):
        op, item, n = _q922
        inv = _q1120.inv
        shed = _q1129[_q954] if _q1129 is not None else None
        if op == 'SELL':
            if shed is not None:
                _q688 = shed.get(item, 0)
                if _q688 < n:
                    n = max(0, _q688)
                shed[item] = _q688 - n
            if n <= 0:
                return
            rev, new = sell_walk(item, n, inv[item])
            inv[item] = new
            if money is not None:
                money[_q954] += rev
            _q1060[_q954]['rev'] += rev
            _acc(_q1060[_q954], (op, item), n, rev)
            return
        if op == 'BUY_PRODUCT':
            _q522 = inv[item]
            _q1206 = 0
            k = 0
            room = None
            if shed is not None and _q1127 is not None:
                room = _q1127 - sum(shed.values())
            while k < n:
                _q1009 = price(item, _q522 - 1)
                if money is not None and money[_q954] < _q1009:
                    break
                if room is not None and room <= 0:
                    break
                if money is not None:
                    money[_q954] -= _q1009
                if room is not None:
                    room -= 1
                _q522 -= 1
                _q1206 += _q1009
                k += 1
            inv[item] = _q522
            if k:
                if shed is not None:
                    shed[item] = shed.get(item, 0) + k
                _q1060[_q954]['cost'] += _q1206
                _acc(_q1060[_q954], (op, item), k, _q1206)
            return
        _q1009 = SEED_PRICE[item] if op == 'BUY_SEED' else ANIMAL_PRICE[item]
        k = 0
        room = None
        if op == 'BUY_ANIMAL' and shed is not None and (_q1127 is not None):
            room = _q1127 - sum(shed.values())
        while k < n:
            if money is not None and money[_q954] < _q1009:
                break
            if room is not None and room <= 0:
                break
            if money is not None:
                money[_q954] -= _q1009
            if room is not None:
                room -= 1
            k += 1
        if k:
            if op == 'BUY_ANIMAL' and shed is not None:
                shed[item] = shed.get(item, 0) + k
            _q1060[_q954]['cost'] += _q1009 * k
            _acc(_q1060[_q954], (op, item), k, _q1009 * k)

    def _lockstep(_q1120, a, b, _q1060, _q1129, money, _q1127):
        """Both seats trade the same item at the same index: unit-by-unit lockstep (engine _process_market)."""
        item = a[1]
        inv = _q1120.inv
        rem = [a[2], b[2]]
        ops = [a[0], b[0]]
        _q383 = [True, True]
        _q670 = [[0, 0], [0, 0]]
        while True:
            _q1035 = [None, None]
            for _q954 in (0, 1):
                if _q383[_q954] and rem[_q954] > 0:
                    _q1035[_q954] = price(item, inv[item]) if ops[_q954] == 'SELL' else price(item, inv[item] - 1)
            if _q1035[0] is None and _q1035[1] is None:
                break
            _q500 = False
            for _q954 in (0, 1):
                _q1009 = _q1035[_q954]
                if _q1009 is None:
                    continue
                shed = _q1129[_q954] if _q1129 is not None else None
                if ops[_q954] == 'SELL':
                    if shed is not None and shed.get(item, 0) <= 0:
                        _q383[_q954] = False
                        continue
                    if shed is not None:
                        shed[item] -= 1
                    if money is not None:
                        money[_q954] += _q1009
                    if _q1009 > 1:
                        inv[item] += 1
                else:
                    if money is not None and money[_q954] < _q1009:
                        _q383[_q954] = False
                        continue
                    if shed is not None and _q1127 is not None and (sum(shed.values()) >= _q1127):
                        _q383[_q954] = False
                        continue
                    if money is not None:
                        money[_q954] -= _q1009
                    if shed is not None:
                        shed[item] = shed.get(item, 0) + 1
                    inv[item] -= 1
                rem[_q954] -= 1
                _q670[_q954][0] += 1
                _q670[_q954][1] += _q1009
                _q500 = True
            if not _q500:
                break
        for _q954 in (0, 1):
            if _q670[_q954][0]:
                if ops[_q954] == 'SELL':
                    _q1060[_q954]['rev'] += _q670[_q954][1]
                else:
                    _q1060[_q954]['cost'] += _q670[_q954][1]
                _acc(_q1060[_q954], (ops[_q954], item), _q670[_q954][0], _q670[_q954][1])

    def step_once(_q1120, _q940=None, _q941=None, **_q775):
        _q1036 = _q1120.market(_q940, _q941, **_q775)
        _q1120.drain()
        return _q1036

    def advance(_q1120, _q1202, _q992=(None, None), **_q775):
        _q955, _q956 = _q992 if _q992 is not None else (None, None)
        _q955 = _q955 or {}
        _q956 = _q956 or {}
        rev = [0, 0]
        rev_item = [{}, {}]
        units = [{}, {}]
        inv = _q1120.inv
        while _q1120.step < _q1202:
            t = _q1120.step
            _q923 = _q955.get(t)
            _q924 = _q956.get(t)
            if _q923 or _q924:
                _q1036 = _q1120.market(_q923, _q924, **_q775)
                for _q954 in (0, 1):
                    rp = _q1036[_q954]
                    rev[_q954] += rp['rev']
                    for (op, it), (_q1221, _q1233) in rp['trades'].items():
                        if op == 'SELL':
                            rev_item[_q954][it] = rev_item[_q954].get(it, 0) + _q1233
                            units[_q954][it] = units[_q954].get(it, 0) + _q1221
            if t % SHOP_SELL_INTERVAL == 0:
                for it, _q1233 in _q1120._drains[_q1120.n_active(t)]:
                    inv[it] -= _q1233
            if t % CENTER_INTERVAL == 0:
                for it in TOWN_CENTER:
                    inv[it] -= 1
            _q1120.step = t + 1
        return {'rev': rev, 'rev_item': rev_item, 'units': units}

def _acc(_q1036, key, _q1221, _q1233):
    t = _q1036['trades'].get(key)
    if t is None:
        _q1036['trades'][key] = [_q1221, _q1233]
    else:
        t[0] += _q1221
        t[1] += _q1233

def plan_value(_q1133, _q943, _q1075, _q1202, _q944=0, **_q775):
    """Revenue of a sale plan pair over [sim.step, to_step) (sim is not mutated; seats never change prices)."""
    s = _q1133.copy()
    _q992 = (_q943, _q1075) if _q944 == 0 else (_q1075, _q943)
    _q946 = s.advance(_q1202, _q992, **_q775)
    _q922, _q1036 = (0, 1) if _q944 == 0 else (1, 0)
    return {'our': _q946['rev'][_q922], 'rival': _q946['rev'][_q1036], 'our_item': _q946['rev_item'][_q922], 'rival_item': _q946['rev_item'][_q1036], 'inv': s.inv}