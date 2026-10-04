"""PD - market module: purchases sequenced by cash, tape-style sales, shed-capacity guard, end-game liquidation
(Original work, Shawn404, 25 Sep 2026).  Pure Python, no engine import, no file access.

    buys, dropped = cap_purchases(orders, money, hires_today, n_quads, prices, floor, shed_room, mult)
    sells = sale_orders(stock, step, reserve, cfg, prices, carried_end=0)
    sells = sale_orders(..., keep=next_morning_keep(n_animals, fert_ops), carried_items=carried)   # room_mode cfg
    sells = sale_orders(..., feeds_left=f, carried_wheat=w, n_animals=a, wheat_median=m)   # wheat_ctl cfg (B6)
    orders, carry = window_orders(sells, buys, step, cfg, cap)                              # h0_window cfg (B6)
    shed1 = shed_after_units(shed, units, invs, cmds)       # the shed at market time (units act before the market)

Engine facts used (kaggriculture 1.32.x):
  * a step runs every unit command first, then the market (orders index by index, lockstep with the rival; at most
    maxMarketOrdersPerTurn per player), then the town consumption (every shop instance every 4 steps: step % 4 == 0),
    then plant decay, then (hour 23) the end-of-day refresh and the drop of every unit inventory into the shed, capped
    at shedCapacity (overflow DISCARDED);
  * SELL executes unit by unit at the current quote while the shed holds the item; BUY_PRODUCT (WHEAT / FERTILIZER)
    at quote(inv - 1) while money covers it and the shed holds < capacity; BUY_SEED / BUY_ANIMAL at fixed prices
    (an animal needs shed room); HIRE costs mult * fib(hires today); BUY_LAND 1000 / 2000 / 4000 in NE, SW, SE order;
  * the last acting step is 718 (hour 22 of day 29): the day-29 end-of-day drop never happens, so whatever is not
    sold by the step-718 market is lost.

Sale policy (tape style, wf31_money / wf31_market):
  * the first market row after each shop tick (step % 4 == 1: hours 1, 5, 9, 13, 17, 21) is the sale row;
  * flat goods (TOMATO, EGG, CARROT, WHEAT, FERTILIZER) sell everything available there; steep goods (STRAWBERRY,
    MILK, WOOL, MELON) in lots of at most cfg['lot'] per row (their curves fall to 11-28% after a 50-unit glut);
  * WHEAT / FERTILIZER keep a reserve (tomorrow's feed / fertilising) - only the excess is sold;
  * hour-23 guard: the shed after this market plus everything the units carry must fit the day-end target
    (cfg['end_target'] <= capacity): extra units are sold, cheapest loss first (flat goods, then steep), reserves last;
  * end game (day 29): every sale row sells flat goods fully and steep goods pro rata over the rows left; from
    cfg['end_step'] every step sells; step 718 sells everything.

Room modes (cfg['room_mode'], CS task B2, 27 Sep 2026; default None = the hour-23 guard above, identical orders):
  * 'protect': the hour-23 guard sells (1) EGG and the WHEAT / FERTILIZER above their PROTECTED level, (2) the
    hinge-held CARROT / TOMATO (and the other carrots / tomatoes), and only if still over the target (3) the protected
    WHEAT / FERTILIZER (cfg['room_dip'] order), (4) the steep goods (cfg['room_reserve_last'] True: steep before the
    reserves).  cfg['room_hinge_last'] (fix R7, 27 Sep; default False = the order above): True = pass (2) moves right
    after the protected WHEAT / FERTILIZER (1, 3, 2, 4; with room_reserve_last 1, 4, 3, 2), 'end' = it goes last
    (1, 3, 4, 2 / 1, 4, 3, 2): the tomatoes / carrots are held for the day 27-29 hinge spike unless the room is needed.
    Protected level = keep[item] (tomorrow's first feed leg / the fertiliser earmarked for tomorrow's FERTILIZE ops;
    argument `keep`, else cfg['room_keep'], else the sale reserve) minus what the units carry into tonight's drop
    (argument `carried_items`: it lands in the shed at the hour-23 refresh).  next_morning_keep() builds `keep`.
    cfg['room_keep_from'] = h: from hour h every sale row also keeps the protected level (default None = off).
  * 'protect_h22': 'protect' + a DSM-like flat clearance at hour 22 (days < 29, before end_step): every item of
    cfg['h22_share'] (DSM h22 share of stock: TOMATO 91%, EGG 87%, CARROT 74%, WHEAT 75%) sells ceil(share x the stock
    above its floor) (floor = max(sale reserve, protected level) for WHEAT / FERTILIZER, the sale reserve otherwise;
    `hold` respected; overrides the hinge hold - drop TOMATO / CARROT from h22_share to keep it); one order per item,
    at most cfg['h22_window'] SELL orders in the hour-22 list (the engine window is 10; the clearance items with the
    smallest value at stake are left out first, earlier sells are never cut).

Market controller (CS task B6, 27 Sep 2026; sys_design 6.8 / 8; defaults off = the orders above, unchanged):
  * cfg['wheat_ctl'] True: WHEAT leaves the tick-row flat rule (days < 29, before end_step) and is sold by a reserve
    controller at EVERY step:
      reserve = max(0, FEEDs left today - wheat carried + leg) + cfg['wc_margin'] (wheat carried x
        cfg['wc_carry_credit'] 1.0, rounded down: a harvester's wheat is not always where the FEEDs are),
        leg = min(animals, cfg['wc_leg_cap'] 15) from hour cfg['wc_leg_from'] 18 on days <= cfg['wc_leg_last_day'] 27
        (tomorrow's first feed leg; the carried units drop into the shed at the hour-23 refresh, so they count;
        at hour 23 the FEEDs still left are missed and count 0);
      surplus = shed wheat at market time - reserve - hold;
      lot = min(surplus, cfg['wc_lot'] 7), or min(surplus, cfg['wc_lot_cheap'] 3) while the quote is below
        cfg['wc_cheap'] 0.8 x the 3-day median quote (argument wheat_median; quote_median() builds it from the
        caller's quote history, None = no cheap rule); at hour cfg['wc_h22'] 22 the rest of the surplus
        (ceil(cfg['wc_h22_share'] 1.0 x surplus)).
    The inputs are explicit keyword arguments of sale_orders: feeds_left (FEED ops still to do today), carried_wheat
    (wheat the units hold at market time), n_animals (animals fed tomorrow), wheat_median.  feeds_left None = the
    caller's WHEAT sale reserve is used as the reserve (fallback, sys_design section 10).  The controller's reserve
    also replaces reserve['WHEAT'] in the hour-23 guard and in the room levels.  wheat_reserve() / wheat_lot() are the
    two pieces as functions.
  * cfg['h0_window'] True:
      - sale_orders at hour 0 (days < 29, before end_step) adds the overnight sells: the FERTILIZER surplus (stock -
        reserve - hold; rows <= cfg['h0_fert_lot'], None = all; not when fert_share is set), the WHEAT surplus (the
        controller's lot when wheat_ctl is on, else stock - reserve - hold when cfg['h0_wheat']) and
        ceil(cfg['h0_straw_share'] 0.2 x the STRAWBERRY stock) (replaces steep_hours[0]; None = leave the steep
        rules alone; <= 0 = no strawberry sale at hour 0);
      - window_orders(sells, buys, step, cfg, cap) builds the list: sells first, then BUY_LAND, then the other buys
        by priority (cfg['win_buy_sort']: feed WHEAT, seeds, animals, other products; stable), then HIRE; <= cap.
        At hour 0 (days <= cfg['h0_last_day']) at most cfg['h0_hires'] 8 HIREs and at least cfg['h0_min_sells'] 2
        SELLs when there are sells (chosen FERTILIZER, WHEAT, STRAWBERRY first, then the sale_orders order); the
        remaining slots go to hires, land, buys, then more sells.  Other hours: the purchases are kept (up to cap,
        cut from the end: hires first) and the sells fill what is left (cfg['win_min_sells'] > 0 guarantees some).
        Returns (orders, carry): carry = the purchases that did not fit, in list order (land, buys, hires), then
        the hires past the hour-0 cap - for the caller to re-issue next step (pd_layer: st['carry_buys']).

P8 market keys (task "market", 28 Sep 2026; race_plannermkt section 5 M1-M3, race_dsm section 7 R1b / R2b; every key
None = the orders above, unchanged).  The new rules act before day 29 and end_step (h0_sells: days <= h0_sell_last_day),
after every rule above and before the hour-22 clearance and the hour-23 guard (which still apply on top):
  * cfg['sell_order'] (list order only): None = the now_items first, then value at stake; 'stake' = every SELL by
    stake (no now_items block; cfg['sell_first'] items, default (), stay in front - M2 suggests ('MELON',));
    'contest' = 'stake' with our sell of the good the rival most likely sells this step at index 0: of our SELL goods in
    cfg['contest_items'] (STEEP) the one with the largest rival_stock (keyword argument {item: units}: the rival's
    visible stock, e.g. rival_tile_stock() of its tiles; >= cfg['contest_min'] 1; ties by stake); no rival_stock =
    'stake'.
  * cfg['tom_tick_min'] = $x: on days < 28 at the first market row after a shop tick (step % 4 == 1) TOMATO sells at
    least the units whose quote stays >= x (after reserve / hold; M3: the tomatoes leave before the hour-23 room guard).
  * cfg['fert_sell'] = {'keep': int (None = the FERTILIZER sale reserve in force: the caller's, raised by
    room_keep_from), 'rows': tuple of step % 4 values, 'min_px': $ (None = no price floor), optional 'lot' (None = the
    whole surplus), 'last_day' (28), 'hold' (False)}:
    on those rows FERTILIZER sells at least the units above 'keep' whose quote stays >= min_px (the anti-DSM
    undercut).  'hold' False: 'keep' replaces the caller's FERTILIZER reserve and hold (pd_layer's C9 holds the whole
    shed), True: they also apply.
  * cfg['wool_rows'] = tuple of step % 4 values: on those rows the cfg['wool_items'] (WOOL, MILK) sell first in the
    list (after h0 / sell_first / contest picks): ceil(share x (stock - reserve - hold)) with cfg['wool_share']
    {item: share | {hour: share}} when it names the item (and hour), else the lot the rules above give, else
    min(avail, lot); cfg['wool_hold'] True (default) = on the other rows they are not sold (R1b: the morning / post-tick
    release instead of every-step sales; the hour-23 guard may still sell them); False = index priority only.
  * cfg['h0_sells'] = N: at hour 0 up to N SELLs of the cfg['h0_items'] (STEEP) in the shed (after reserve / hold; a
    pick overrides the wool_hold hold), ranked by cfg['h0_rank'] 'stake' (or 'value' = units x quote), each worth >=
    cfg['h0_min_value'] (None = any), lot = the rules' sale if any, else min(avail, cfg['h0_lot'] or lot); they go at
    the head of the list, and sale_orders then returns a SellList (a list with .h0 = their count; h0_count() reads it)
    so the layer can place them ahead of the HIREs (M1).  Other steps / no pick: a plain list, as before.
"""
import math
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
STEEP = ('STRAWBERRY', 'MILK', 'WOOL', 'MELON')
FLAT = ('TOMATO', 'EGG', 'CARROT', 'WHEAT', 'FERTILIZER')
ANIMALS = ('GOOSE', 'COW', 'SHEEP')
STRUCT = {'GOOSE': 'COOP', 'COW': 'PASTURE', 'SHEEP': 'PASTURE'}
SEED_PRICE = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
ANIMAL_PRICE = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
LAND_PRICES = (1000, 2000, 4000)
ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
FINAL_STEP = 718
MARKET_PARAMS = {'WHEAT': (25, 400, 'sqrt', 0.8, 'log', 0.2), 'CARROT': (35, 450, 'hinge', 1.0, 'sqrt', 0.7), 'TOMATO': (60, 200, 'hinge', 0.4, 'sqrt', 0.6), 'STRAWBERRY': (120, 100, 'sqrt', 0.7, 'linear', 1.6), 'MELON': (250, 300, 'log', 0.2, 'sq', 3.6), 'EGG': (50, 332, 'hinge', 0.4, 'log', 0.2), 'MILK': (160, 122, 'sqrt', 0.6, 'linear', 1.6), 'WOOL': (200, 105, 'log', 0.2, 'sq', 3.2), 'FERTILIZER': (100, 200, 'linear', 0.4, 'linear', 0.4)}
I0 = 10000
CFG = {'lot': 6, 'lot_rows': (1,), 'end_target': 96, 'end_step': 700, 'floor': 300, 'buy_slack': 2, 'hinge_hold': {'TOMATO': 2.0, 'CARROT': 2.0}, 'hinge_late_day': 28.5, 'hinge_late_mult': 1.0, 'now_items': (), 'now_from': 0, 'end_dump': False, 'steep_hours': None, 'fert_share': None, 'fert_keep_max': 30, 'room_mode': None, 'room_keep': None, 'room_keep_cap': 15, 'room_keep_margin': 0, 'room_dip': ('WHEAT', 'FERTILIZER'), 'room_reserve_last': False, 'room_hinge_last': False, 'room_keep_from': None, 'h22_share': {'TOMATO': 0.91, 'EGG': 0.87, 'CARROT': 0.74, 'WHEAT': 0.75}, 'h22_window': 10, 'wheat_ctl': False, 'wc_lot': 7, 'wc_lot_cheap': 3, 'wc_cheap': 0.8, 'wc_med_min': 12, 'wc_med_len': 72, 'wc_leg_from': 18, 'wc_leg_cap': 15, 'wc_leg_last_day': 27, 'wc_margin': 0, 'wc_carry_credit': 1.0, 'wc_h22': 22, 'wc_h22_share': 1.0, 'h0_window': False, 'h0_hires': 8, 'h0_min_sells': 2, 'h0_last_day': 29, 'h0_straw_share': 0.2, 'h0_fert_lot': None, 'h0_wheat': True, 'win_buy_sort': True, 'win_min_sells': 0, 'sell_order': None, 'sell_first': (), 'contest_items': ('STRAWBERRY', 'MILK', 'WOOL', 'MELON'), 'contest_min': 1, 'tom_tick_min': None, 'fert_sell': None, 'wool_rows': None, 'wool_items': ('WOOL', 'MILK'), 'wool_share': None, 'wool_hold': True, 'h0_sells': None, 'h0_items': ('STRAWBERRY', 'MILK', 'WOOL', 'MELON'), 'h0_lot': None, 'h0_rank': 'stake', 'h0_min_value': None, 'h0_sell_last_day': 28}

def hinge_late_price(item, _q734, _q561, day, stock, cfg=None):
    """Projected quote of the marginal unit if our whole `stock` is sold at cfg['hinge_late_day']: the town drains
    drain_per_day units a day until then (rival sales ignored), then our stock goes back in."""
    c = cfg or CFG
    days = max(0.0, c['hinge_late_day'] - day)
    return market_price(item, int(round(_q734 - _q561 * days)) + int(stock))

def fib(n):
    a, b = (1, 1)
    for _ in range(max(0, n)):
        a, b = (b, a + b)
    return a

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
    if _q656 == 'hinge':
        _q1221 = x / T
        return _q1221 + 8.0 * max(0.0, _q1221 - 1.0) ** 2
    return x

def market_price(item, inv):
    """Engine market_price with the default parameters (floor $1)."""
    base, T, _q412, _q432, _q378, _q396 = MARKET_PARAMS[item]
    if inv < I0:
        _q387 = _q432 * base / _shape(_q412, T, T)
        _q954 = base + _q387 * _shape(_q412, I0 - inv, T)
    else:
        _q387 = _q396 * base / _shape(_q378, T, T)
        _q954 = base - _q387 * _shape(_q378, inv - I0, T)
    return max(1, int(round(_q954)))

def sale_value(item, inv, n):
    """Revenue of selling n units now into market inventory inv (our units only)."""
    _q1233 = 0
    for k in range(n):
        _q954 = market_price(item, inv + k)
        _q1233 += _q954
    return _q1233

def shed_after_units(shed, units, _q735, _q495, cap=100):
    """The shed at market time: `shed` run through this turn's unit commands (farmer first, then hands) with the
    engine's shed rules (PICKUP / DROP / shed PLACE from a shed-access tile, capacity).  Returns (shed dict, carried
    dict = what the units hold after their commands, not counting HARVEST gains)."""
    sh = {k: int(_q1233) for k, _q1233 in shed.items() if _q1233}
    carried = {}
    for _q1221, _q493 in enumerate(_q495):
        inv = dict(_q735[_q1221]) if _q1221 < len(_q735) else {}
        pos = tuple(units[_q1221]) if _q1221 < len(units) else None
        if isinstance(_q493, list) and _q493 and (pos in ACCESS):
            op = _q493[0]
            if op == 'PICKUP' and len(_q493) >= 2:
                n = int(_q493[2]) if len(_q493) >= 3 else 1
                n = min(max(0, n), sh.get(_q493[1], 0))
                if n > 0:
                    sh[_q493[1]] = sh.get(_q493[1], 0) - n
                    inv[_q493[1]] = inv.get(_q493[1], 0) + n
            elif op == 'DROP':
                for item, n in list(inv.items()):
                    room = max(0, cap - sum(sh.values()))
                    _q1186 = min(n, room)
                    if _q1186 > 0:
                        sh[item] = sh.get(item, 0) + _q1186
                    del inv[item]
            elif op == 'PLACE' and len(_q493) >= 2 and (_q493[1] not in ANIMALS):
                n = int(_q493[2]) if len(_q493) >= 3 else 1
                n = min(max(0, n), inv.get(_q493[1], 0), max(0, cap - sum(sh.values())))
                if n > 0:
                    inv[_q493[1]] -= n
                    sh[_q493[1]] = sh.get(_q493[1], 0) + n
        for k, _q1233 in inv.items():
            if _q1233 > 0:
                carried[k] = carried.get(k, 0) + _q1233
    return ({k: _q1233 for k, _q1233 in sh.items() if _q1233 > 0}, carried)

def order_cost(_q922, h, n_quads, prices, _q851=1, slack=2):
    """(cost, hires added, quads added) of one order under the engine's prices (BUY_PRODUCT: quote + slack)."""
    op = _q922[0]
    if op == 'HIRE':
        return (_q851 * fib(h), 1, 0)
    if op == 'BUY_LAND':
        if n_quads >= 4:
            return (0, 0, 0)
        return (LAND_PRICES[n_quads - 1], 0, 1)
    n = int(_q922[2]) if len(_q922) >= 3 else 0
    if op == 'BUY_SEED':
        return (SEED_PRICE.get(_q922[1], 100) * n, 0, 0)
    if op == 'BUY_ANIMAL':
        return (ANIMAL_PRICE.get(_q922[1], 500) * n, 0, 0)
    if op == 'BUY_PRODUCT':
        return ((int(prices.get(_q922[1], 100)) + slack) * n, 0, 0)
    return (0, 0, 0)

def cap_purchases(orders, money, hires_today, n_quads, prices, floor, shed_room, _q851=1, slack=2):
    """Walk the purchase orders in list order and keep what money - floor covers (quantities trimmed; animals and
    products also need shed room).  Returns (kept, dropped) lists; dropped = [(order, reason)]."""
    kept, _q565 = ([], [])
    h = int(hires_today)
    q = int(n_quads)
    m = float(money)
    room = int(shed_room)
    for _q922 in orders:
        if not isinstance(_q922, (list, tuple)) or not _q922:
            continue
        _q922 = list(_q922)
        op = _q922[0]
        if op in ('HIRE', 'BUY_LAND'):
            c, _q549, _q559 = order_cost(_q922, h, q, prices, _q851, slack)
            if op == 'BUY_LAND' and q >= 4:
                _q565.append((_q922, 'all_land'))
                continue
            if m - c < floor:
                _q565.append((_q922, 'cash'))
                continue
            m -= c
            h += _q549
            q += _q559
            kept.append(_q922)
            continue
        if op not in ('BUY_SEED', 'BUY_ANIMAL', 'BUY_PRODUCT') or len(_q922) < 3:
            _q565.append((_q922, 'malformed'))
            continue
        n = int(_q922[2])
        unit = order_cost([op, _q922[1], 1], h, q, prices, _q851, slack)[0]
        k = n
        if unit > 0:
            k = min(k, int((m - floor) // unit))
        if op in ('BUY_ANIMAL', 'BUY_PRODUCT'):
            k = min(k, room)
        if k <= 0:
            _q565.append((_q922, 'cash' if room > 0 else 'room'))
            continue
        if k < n:
            _q565.append(([op, _q922[1], n - k], 'cash' if (m - floor) // max(1, unit) < n else 'room'))
        m -= unit * k
        if op in ('BUY_ANIMAL', 'BUY_PRODUCT'):
            room -= k
        kept.append([op, _q922[1], k])
    return (kept, _q565)

def is_sale_row(step, cfg=None):
    c = cfg or CFG
    return step % 4 in c['lot_rows'] or step >= c['end_step'] or step >= FINAL_STEP

def rows_left(step, cfg=None):
    """Sale rows from step to 718 inclusive (step 718 always counts)."""
    c = cfg or CFG
    n = 0
    for s in range(step, FINAL_STEP + 1):
        if s >= c['end_step'] or s % 4 in c['lot_rows'] or s == FINAL_STEP:
            n += 1
    return max(1, n)

def next_morning_keep(n_animals, _q617=0, cfg=None):
    """`keep` for the room modes: WHEAT = tomorrow's first feed leg = min(animals, cfg['room_keep_cap']) +
    cfg['room_keep_margin']; FERTILIZER = the units earmarked for tomorrow's FERTILIZE ops."""
    c = cfg or CFG
    return {'WHEAT': min(int(c.get('room_keep_cap', 15)), max(0, int(n_animals))) + int(c.get('room_keep_margin', 0)), 'FERTILIZER': max(0, int(_q617))}

def room_levels(reserve, keep=None, carried_items=None, cfg=None):
    """Shed units the room modes protect, per item: WHEAT / FERTILIZER = keep[item] (else cfg['room_keep'][item], else
    reserve[item]) minus what the units carry into tonight's drop (it lands in the shed at the hour-23 refresh), >= 0;
    the other goods = their sale reserve."""
    c = cfg or CFG
    _q1060 = reserve or {}
    _q774 = keep or {}
    _q488 = c.get('room_keep') or {}
    _q464 = carried_items or {}
    _q946 = {}
    for it in PRODUCTS:
        if it in ('WHEAT', 'FERTILIZER'):
            k = _q774[it] if it in _q774 else _q488[it] if it in _q488 else _q1060.get(it, 0)
            _q946[it] = max(0, int(k) - int(_q464.get(it, 0)))
        else:
            _q946[it] = max(0, int(_q1060.get(it, 0)))
    return _q946

def _stake(item, n, mi):
    """Value at stake of selling n units into market inventory mi (the output order key of sale_orders)."""
    return (market_price(item, mi) - market_price(item, mi + min(n, 10))) * n

class SellList(list):
    """sale_orders' return value when cfg['h0_sells'] picked hour-0 sells: the order list, whose first .h0 entries
    are those sells (the layer places them ahead of the HIREs).  Any list operation returns a plain list."""
    h0 = 0

def h0_count(sells):
    """Leading hour-0 sells of a sale_orders result (0 for a plain list)."""
    return int(getattr(sells, 'h0', 0) or 0)
CROP_FIRST_YIELD = {'WHEAT': 2, 'CARROT': 2, 'TOMATO': 8, 'STRAWBERRY': 10, 'MELON': 10}
ANIMAL_PRODUCT = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}

def rival_tile_stock(tiles, day):
    """'contest' input from a public tile grid (rows of tile dicts): {item: harvestable units on the tiles} - crops
    at least first_yield_day old (a young non-ongoing crop already shows yield_units 1), animal products held."""
    _q946 = {}
    for _q1086 in tiles or []:
        for t in _q1086 or []:
            if not isinstance(t, dict):
                continue
            n = int(t.get('yield_units', 0) or 0)
            if n <= 0:
                continue
            if t.get('kind') == 'PLANT':
                it = t.get('crop')
                if it not in CROP_FIRST_YIELD or int(day) - int(t.get('planted_day', day)) < CROP_FIRST_YIELD[it]:
                    continue
            else:
                it = ANIMAL_PRODUCT.get(t.get('animal'))
            if it:
                _q946[it] = _q946.get(it, 0) + n
    return _q946

def _units_at_least(item, mi, n, px):
    """Units of n sold one by one into market inventory mi while each unit's quote is >= px."""
    k = 0
    while k < n and market_price(item, mi + k) >= px:
        k += 1
    return k

def wheat_reserve(hour, day, feeds_left, carried_wheat, n_animals, cfg=None):
    """Shed WHEAT the controller keeps (wheat_ctl): max(0, FEEDs left today - wheat carried + leg) + wc_margin, leg =
    tomorrow's first feed leg min(animals, wc_leg_cap) from hour wc_leg_from on days <= wc_leg_last_day.  At hour 23
    the FEEDs still left are missed (the units acted before the market and no step of the day follows): they count 0."""
    c = cfg or CFG
    _q801 = 0
    if int(hour) >= int(c.get('wc_leg_from', 18)) and int(day) <= int(c.get('wc_leg_last_day', 27)):
        _q801 = min(int(c.get('wc_leg_cap', 15)), max(0, int(n_animals or 0)))
    _q633 = 0 if int(hour) >= 23 else int(feeds_left or 0)
    cw = int(carried_wheat or 0)
    _q513 = c.get('wc_carry_credit', 1.0)
    if _q513 is not None and float(_q513) != 1.0:
        cw = int(math.floor(float(_q513) * cw + 1e-09))
    return max(0, _q633 - cw + _q801) + max(0, int(c.get('wc_margin', 0) or 0))

def wheat_lot(_q1173, hour, quote=None, _q834=None, cfg=None):
    """WHEAT units the controller sells this step out of `surplus` (shed - reserve - hold): lots <= wc_lot, <=
    wc_lot_cheap while quote < wc_cheap x median (median None = no cheap rule), the rest at hour wc_h22."""
    c = cfg or CFG
    _q1173 = int(_q1173)
    if _q1173 <= 0:
        return 0
    if int(hour) == int(c.get('wc_h22', 22)):
        return min(_q1173, int(math.ceil(float(c.get('wc_h22_share', 1.0)) * _q1173 - 1e-09)))
    lot = int(c.get('wc_lot', 7))
    if _q834 is not None and quote is not None and (float(quote) < float(c.get('wc_cheap', 0.8)) * float(_q834)):
        lot = int(c.get('wc_lot_cheap', 3))
    return max(0, min(_q1173, lot))

def carried_wheat_after(carried, _q495, _q1252=0):
    """wheat_ctl input from the layer's data: the WHEAT the units hold at market time = shed_after_units' carried
    WHEAT (shed ops only) - this step's FEED commands (each eats 1 wheat before the market; the executor issues FEED
    only with wheat in hand and pops the op from its chains) + wheat_gain (this step's wheat HARVEST units), >= 0."""
    _q865 = sum((1 for a in _q495 or [] if isinstance(a, (list, tuple)) and a and (a[0] == 'FEED')))
    return max(0, int((carried or {}).get('WHEAT', 0)) - _q865) + max(0, int(_q1252 or 0))

def push_quote(_q699, quote, cfg=None):
    """Append this step's quote to the caller's history list (kept at wc_med_len entries); returns hist."""
    c = cfg or CFG
    _q699.append(float(quote))
    n = int(c.get('wc_med_len', 72))
    if len(_q699) > n:
        del _q699[:len(_q699) - n]
    return _q699

def quote_median(_q699, cfg=None):
    """Median of the quote history (the 3-day median of wheat_ctl); None while it holds < wc_med_min quotes."""
    c = cfg or CFG
    h = [float(x) for x in _q699 or []][-int(c.get('wc_med_len', 72)):]
    if len(h) < max(1, int(c.get('wc_med_min', 12))):
        return None
    h.sort()
    m = len(h) // 2
    return h[m] if len(h) % 2 else 0.5 * (h[m - 1] + h[m])

def sale_orders(stock, step, reserve, prices, market_inv=None, carried_end=0, cfg=None, hold=None, drain=None, keep=None, carried_items=None, feeds_left=None, carried_wheat=None, n_animals=None, wheat_median=None, rival_stock=None):
    """SELL orders for this step.  stock = shed at market time; reserve = {item: units kept} (WHEAT / FERTILIZER);
    carried_end = units the farm will still add to the shed at tonight's drop (hour 23: what the units carry after
    their commands).  hold = {item: units not to sell now} (optional).  keep / carried_items: only read when
    cfg['room_mode'] is set (see "Room modes" above): keep = {item: units wanted after tonight's drop} (WHEAT:
    tomorrow's first feed leg, FERTILIZER: tomorrow's FERTILIZE earmark), carried_items = {item: units the units carry
    into the drop}.  feeds_left / carried_wheat / n_animals / wheat_median: only read when cfg['wheat_ctl'] is set
    (see "Market controller" above).  rival_stock = {item: the rival's visible units}: only read when
    cfg['sell_order'] == 'contest' (see "P8 market keys" above).  Returns [['SELL', item, n], ...] ordered by value at
    stake (biggest first); a SellList when cfg['h0_sells'] placed hour-0 sells at its head."""
    c = cfg or CFG
    hour = step % 24
    day = step // 24
    _q626 = day >= 29
    room_mode = c.get('room_mode')
    protect = room_mode in ('protect', 'protect_h22')
    _q1247 = bool(c.get('wheat_ctl')) and (not _q626) and (step < c['end_step']) and (step < FINAL_STEP)
    if _q1247 and feeds_left is not None:
        reserve = dict(reserve or {})
        reserve['WHEAT'] = wheat_reserve(hour, day, feeds_left, carried_wheat, n_animals, c)
    _q819 = room_levels(reserve, keep, carried_items, c) if protect else None
    _q766 = c.get('room_keep_from') if protect else None
    if _q766 is not None and hour >= int(_q766) and (not _q626):
        reserve = dict(reserve or {})
        for it in ('WHEAT', 'FERTILIZER'):
            reserve[it] = max(int(reserve.get(it, 0)), int(_q819[it]))
    avail = {}
    for it in PRODUCTS:
        n = int(stock.get(it, 0)) - int((reserve or {}).get(it, 0) if not _q626 else 0) - int((hold or {}).get(it, 0))
        if n > 0:
            avail[it] = n
    _q1121 = {}
    inv = market_inv or {}
    hinge = c.get('hinge_hold') or {}
    _q788 = _q626 or step >= c['end_step']
    if step >= FINAL_STEP:
        for it in PRODUCTS:
            if stock.get(it, 0) > 0:
                _q1121[it] = int(stock[it])
    elif is_sale_row(step, c):
        _q799 = rows_left(step, c) if _q626 or step >= c['end_step'] else None
        for it, n in avail.items():
            if _q1247 and it == 'WHEAT':
                continue
            if it in STEEP:
                k = min(n, c['lot'])
                if _q799 is not None:
                    k = max(k, int(math.ceil(n / float(_q799))))
                _q1121[it] = k
            elif it in hinge:
                thr = hinge[it] * MARKET_PARAMS[it][0]
                mi = inv.get(it, I0)
                if drain and (not _q788):
                    thr = max(thr, c.get('hinge_late_mult', 1.0) * hinge_late_price(it, mi, float(drain.get(it, 0)), step / 24.0, int(stock.get(it, 0)), c))
                k = 0
                while k < n and market_price(it, mi + k) >= thr:
                    k += 1
                if _q788:
                    k = max(k, int(math.ceil(n / float(_q799))))
                if k > 0:
                    _q1121[it] = min(n, k)
            else:
                _q1121[it] = n
    sh = c.get('steep_hours')
    if sh and step < FINAL_STEP and (not (_q626 or step >= c['end_step'])) and (hour in sh):
        for it, n in avail.items():
            if it in STEEP:
                _q1121[it] = min(n, int(sh[hour]))
    _q650 = c.get('fert_share')
    if _q650 is not None and (not (_q626 or step >= c['end_step'])) and (step < FINAL_STEP):
        _q596 = avail.get('FERTILIZER', 0)
        k = max(0, _q596 - int(c.get('fert_keep_max', 30)))
        if hour == min((h for h in range(24) if h % 4 in c['lot_rows']), default=1):
            k = max(k, int(float(_q650) * _q596))
        if k > 0:
            _q1121['FERTILIZER'] = k
        else:
            _q1121.pop('FERTILIZER', None)
    if _q1247:
        k = wheat_lot(avail.get('WHEAT', 0), hour, (prices or {}).get('WHEAT'), wheat_median, c)
        if k > 0:
            _q1121['WHEAT'] = k
    if c.get('h0_window') and hour == 0 and (not (_q626 or step >= c['end_step'])) and (step < FINAL_STEP):
        if _q650 is None and avail.get('FERTILIZER', 0) > 0:
            k = int(avail['FERTILIZER'])
            if c.get('h0_fert_lot') is not None:
                k = min(k, int(c['h0_fert_lot']))
            if k > _q1121.get('FERTILIZER', 0):
                _q1121['FERTILIZER'] = k
        if not _q1247 and c.get('h0_wheat', True) and (avail.get('WHEAT', 0) > 0):
            _q1121['WHEAT'] = max(_q1121.get('WHEAT', 0), int(avail['WHEAT']))
        _q1157 = c.get('h0_straw_share')
        if _q1157 is not None:
            if float(_q1157) > 0 and avail.get('STRAWBERRY', 0) > 0:
                _q882 = int(avail['STRAWBERRY'])
                _q1121['STRAWBERRY'] = min(_q882, max(1, int(math.ceil(float(_q1157) * _q882 - 1e-09))))
            else:
                _q1121.pop('STRAWBERRY', None)
    if _q626 and c.get('end_dump') and (step < FINAL_STEP):
        for it, n in avail.items():
            _q1121[it] = int(n)
    now_items = tuple(c.get('now_items') or ()) if hour >= int(c.get('now_from', 0) or 0) else ()
    if now_items and step < FINAL_STEP:
        for it in now_items:
            if avail.get(it, 0) > 0:
                _q1121[it] = int(avail[it])
    _q579 = not _q788 and step < FINAL_STEP
    _q1214 = c.get('tom_tick_min')
    if _q1214 is not None and _q579 and (day < 28) and (step % 4 == 1) and (avail.get('TOMATO', 0) > 0):
        k = _units_at_least('TOMATO', inv.get('TOMATO', I0), int(avail['TOMATO']), float(_q1214))
        if k > _q1121.get('TOMATO', 0):
            _q1121['TOMATO'] = k
    _q652 = c.get('fert_sell')
    if _q652 and _q579 and (day <= int(_q652.get('last_day', 28))) and (step % 4 in tuple(_q652.get('rows') or ())):
        _q774 = _q652.get('keep')
        _q774 = int((reserve or {}).get('FERTILIZER', 0)) if _q774 is None else int(_q774)
        k = int(stock.get('FERTILIZER', 0)) - max(0, _q774)
        if _q652.get('hold'):
            k = min(k, int(avail.get('FERTILIZER', 0)))
        if _q652.get('lot') is not None:
            k = min(k, int(_q652['lot']))
        if k > 0 and _q652.get('min_px') is not None:
            k = _units_at_least('FERTILIZER', inv.get('FERTILIZER', I0), k, float(_q652['min_px']))
        if k > _q1121.get('FERTILIZER', 0):
            _q1121['FERTILIZER'] = k
    _q1263 = c.get('wool_rows')
    _q1260 = ()
    if _q1263 is not None and _q579:
        _q1241 = tuple(c.get('wool_items') or ())
        if step % 4 in tuple(_q1263):
            _q1265 = c.get('wool_share') or {}
            for it in _q1241:
                n = int(avail.get(it, 0))
                if n <= 0:
                    continue
                _q1098 = _q1265.get(it)
                if isinstance(_q1098, dict):
                    _q1098 = _q1098.get(hour)
                if _q1098 is not None:
                    k = min(n, max(0, int(math.ceil(float(_q1098) * n - 1e-09))))
                elif _q1121.get(it, 0) > 0:
                    k = int(_q1121[it])
                else:
                    k = min(n, int(c['lot']))
                if k > 0:
                    _q1121[it] = k
                else:
                    _q1121.pop(it, None)
            _q1260 = _q1241
        elif c.get('wool_hold', True):
            for it in _q1241:
                _q1121.pop(it, None)
    _q679 = []
    _q680 = c.get('h0_sells')
    if _q680 and hour == 0 and (step < FINAL_STEP) and (day <= int(c.get('h0_sell_last_day', 28))):
        _q455 = []
        for it in tuple(c.get('h0_items') or ()):
            n = int(avail.get(it, 0))
            if n <= 0 or it not in PRODUCTS:
                continue
            k = int(_q1121.get(it, 0)) or min(n, int(c.get('h0_lot') or c['lot']))
            mi = inv.get(it, I0)
            if c.get('h0_min_value') is not None and sale_value(it, mi, k) < float(c['h0_min_value']):
                continue
            key = -k * market_price(it, mi) if c.get('h0_rank') == 'value' else -_stake(it, k, mi)
            _q455.append((key, PRODUCTS.index(it), it, k))
        _q455.sort()
        for _, _, it, k in _q455[:max(0, int(_q680))]:
            _q1121[it] = k
            _q679.append(it)
    if room_mode == 'protect_h22' and hour == 22 and (not _q788) and (step < FINAL_STEP):
        _q1060 = reserve or {}
        _q692 = hold or {}
        added = []
        for it in PRODUCTS:
            s = float((c.get('h22_share') or {}).get(it, 0) or 0)
            if s <= 0:
                continue
            base = int(stock.get(it, 0)) - int(_q692.get(it, 0)) - max(int(_q1060.get(it, 0)), int(_q819.get(it, 0)))
            if base <= 0:
                continue
            k = min(base, int(math.ceil(s * base - 1e-09)))
            if k > _q1121.get(it, 0):
                if _q1121.get(it, 0) <= 0:
                    added.append(it)
                _q1121[it] = k
        _q1255 = max(0, int(c.get('h22_window', 10)))
        _q880 = sum((1 for _q1233 in _q1121.values() if _q1233 > 0))
        if _q880 > _q1255 and added:
            for _, _, it in sorted(((_stake(it, _q1121[it], inv.get(it, I0)), PRODUCTS.index(it), it) for it in added)):
                if _q880 <= _q1255:
                    break
                del _q1121[it]
                _q880 -= 1
    if hour == 23 and (not _q626) and protect:
        after = sum((int(_q1233) for _q1233 in stock.values())) - sum(_q1121.values())
        _q947 = after + int(carried_end) - int(c['end_target'])
        if _q947 > 0:
            _q551 = tuple((it for it in c.get('room_dip') or () if it in ('WHEAT', 'FERTILIZER')))
            _q551 += tuple((it for it in ('WHEAT', 'FERTILIZER') if it not in _q551))
            _q969 = [[(it, _q819.get(it, 0)) for it in ('EGG', 'FERTILIZER', 'WHEAT') if it not in hinge], [(it, 0) for it in ('CARROT', 'TOMATO', 'EGG') if it in hinge] + [(it, 0) for it in ('CARROT', 'TOMATO') if it not in hinge], [(it, 0) for it in _q551], [(it, 0) for it in ('MELON', 'WOOL', 'MILK', 'STRAWBERRY')]]
            if c.get('room_reserve_last'):
                _q969[2], _q969[3] = (_q969[3], _q969[2])
            _q701 = c.get('room_hinge_last')
            if _q701:
                _q705 = _q969.pop(1)
                if _q701 == 'end':
                    _q969.append(_q705)
                else:
                    _q969.insert(3 if c.get('room_reserve_last') else 2, _q705)
            for _q671 in _q969:
                for it, level in _q671:
                    if _q947 <= 0:
                        break
                    _q688 = int(stock.get(it, 0)) - _q1121.get(it, 0) - int(level)
                    k = min(max(0, _q688), _q947)
                    if k > 0:
                        _q1121[it] = _q1121.get(it, 0) + k
                        _q947 -= k
    elif hour == 23 and (not _q626):
        after = sum((int(_q1233) for _q1233 in stock.values())) - sum(_q1121.values())
        _q947 = after + int(carried_end) - int(c['end_target'])
        if _q947 > 0:
            _q1060 = reserve or {}
            _q969 = [[(it, True) for it in ('EGG', 'FERTILIZER', 'WHEAT') if it not in hinge], [(it, False) for it in ('WHEAT', 'FERTILIZER')], [(it, False) for it in ('CARROT', 'TOMATO', 'EGG') if it in hinge] + [(it, False) for it in ('CARROT', 'TOMATO') if it not in hinge], [(it, False) for it in ('MELON', 'WOOL', 'MILK', 'STRAWBERRY')]]
            for _q671 in _q969:
                for it, _q368 in _q671:
                    if _q947 <= 0:
                        break
                    _q688 = int(stock.get(it, 0)) - _q1121.get(it, 0)
                    if _q368:
                        _q688 -= int(_q1060.get(it, 0))
                    k = min(max(0, _q688), _q947)
                    if k > 0:
                        _q1121[it] = _q1121.get(it, 0) + k
                        _q947 -= k
    so = c.get('sell_order')
    _q629 = tuple(c.get('sell_first') or ()) if so else ()
    _q480 = None
    if so == 'contest' and rival_stock:
        best = None
        for it, n in _q1121.items():
            _q1040 = int(rival_stock.get(it, 0) or 0)
            if n > 0 and it in tuple(c.get('contest_items') or ()) and (_q1040 >= int(c.get('contest_min', 1))):
                key = (_q1040, _stake(it, n, inv.get(it, I0)), -PRODUCTS.index(it))
                if best is None or key > best[0]:
                    best = (key, it)
        _q480 = best[1] if best else None
    _q946 = []
    for it, n in _q1121.items():
        if n <= 0:
            continue
        mi = inv.get(it, I0)
        stake = market_price(it, mi) - market_price(it, mi + min(n, 10))
        _q672 = (_q679.index(it) if it in _q679 else len(_q679), 0 if it in _q629 else 1, 0 if it == _q480 else 1, 0 if it in _q1260 else 1)
        now = 0 if so is None and it in now_items else 1
        _q946.append((now, -(stake * n), PRODUCTS.index(it), ['SELL', it, int(n)], _q672))
    _q946.sort(key=lambda x: (x[4], x[0], x[1], x[2]))
    orders = [x[3] for x in _q946]
    if _q679:
        orders = SellList(orders)
        orders.h0 = len(_q679)
    return orders

def cap_orders(sells, _q444, cap=10):
    """Final list: sells first (cash before the buys), buys always kept (at most cap), sells trimmed to fit."""
    _q444 = list(_q444)[:cap]
    room = max(0, cap - len(_q444))
    return list(sells)[:room] + _q444
H0_SELL_RANK = {'FERTILIZER': 0, 'WHEAT': 1, 'STRAWBERRY': 2}

def _buy_rank(_q922):
    """window_orders' priority of a non-land, non-hire purchase: feed WHEAT, seeds, animals, other products, rest."""
    op = _q922[0] if isinstance(_q922, (list, tuple)) and _q922 else None
    if op == 'BUY_PRODUCT':
        return 0 if len(_q922) > 1 and _q922[1] == 'WHEAT' else 3
    return {'BUY_SEED': 1, 'BUY_ANIMAL': 2}.get(op, 4)

def window_orders(sells, _q444, step, cfg=None, cap=10):
    """The step's market list and the purchases left for the next step: (orders, carry).
    cfg['h0_window'] off: (cap_orders(sells, buys, cap), buys[cap:]) - the old list.
    On (CS B6): sells first, then BUY_LAND, then the other buys by priority (cfg['win_buy_sort']), then HIRE, <= cap.
    Hour 0 (days <= cfg['h0_last_day']): <= cfg['h0_hires'] HIREs and >= cfg['h0_min_sells'] SELLs when sells exist
    (FERTILIZER, WHEAT, STRAWBERRY first, then the given order); the remaining slots go to hires, land, buys, then
    more sells.  Other hours: purchases kept up to cap (cut from the end), sells fill the rest (cfg['win_min_sells']
    SELL slots kept).  Selected sells keep their given relative order.  carry = purchases left out, in list order."""
    c = cfg or CFG
    sells = list(sells or [])
    _q444 = list(_q444 or [])
    cap = max(0, int(cap))
    if not c.get('h0_window'):
        return (cap_orders(sells, _q444, cap), _q444[cap:])
    hour = int(step) % 24
    day = int(step) // 24
    _q717 = range(len(_q444))
    land = [_q712 for _q712 in _q717 if isinstance(_q444[_q712], (list, tuple)) and _q444[_q712] and (_q444[_q712][0] == 'BUY_LAND')]
    hires = [_q712 for _q712 in _q717 if isinstance(_q444[_q712], (list, tuple)) and _q444[_q712] and (_q444[_q712][0] == 'HIRE')]
    other = [_q712 for _q712 in _q717 if not (isinstance(_q444[_q712], (list, tuple)) and _q444[_q712] and (_q444[_q712][0] in ('BUY_LAND', 'HIRE')))]
    if c.get('win_buy_sort', True):
        other = sorted(other, key=lambda _q712: (_buy_rank(_q444[_q712]), _q712))
    h0 = hour == 0 and day <= int(c.get('h0_last_day', 29))
    _q790 = []
    if h0:
        _q909 = max(0, int(c.get('h0_hires', 8)))
        hires, _q790 = (hires[:_q909], hires[_q909:])

        def _q1154(_q712):
            _q922 = sells[_q712]
            return (H0_SELL_RANK.get(_q922[1] if isinstance(_q922, (list, tuple)) and len(_q922) > 1 else '', 3), _q712)
        _q1042 = sorted(range(len(sells)), key=_q1154)
        g = min(max(0, int(c.get('h0_min_sells', 2))), len(sells), cap)
        _q1025 = hires + land + other
    else:
        _q1042 = list(range(len(sells)))
        g = min(max(0, int(c.get('win_min_sells', 0))), len(sells), cap)
        _q1025 = land + other + hires
    _q484 = set(_q1042[:g])
    _q1140 = cap - g
    _q1186 = set(_q1025[:_q1140])
    _q1140 -= len(_q1186)
    for _q712 in _q1042[g:]:
        if _q1140 <= 0:
            break
        _q484.add(_q712)
        _q1140 -= 1
    _q946 = [sells[_q712] for _q712 in sorted(_q484)]
    _q946 += [_q444[_q712] for _q712 in land + other + hires if _q712 in _q1186]
    carry = [_q444[_q712] for _q712 in land + other + hires if _q712 not in _q1186] + [_q444[_q712] for _q712 in _q790]
    return (_q946, carry)