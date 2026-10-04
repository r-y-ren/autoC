"""Observed-stock overflow rescue; uses the planner's forced-sale price ranking.

Harvest goes to unlimited hand inventories, not the shed. Only DROP and the
nightly transfer destroy stock. Return finished workers with excess cargo and
sell that cargo on the PLACE turn (unit actions precede the market).
"""
from __future__ import annotations

import numpy as np
from .. import spec
from ..core import ops as O, plan as P

_TAIL = (O.OP_PASS, O.OP_CARE, O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)

# [REVFIX2 2026-09-29, docs/strategy/2026-09-29-astra-review3.md] default OFF = the shipped behaviour byte for byte.
#: finding 3: at the last executed turn (d29 h22) an overflowing DROP keeps the deposit (unchanged DROP in cargo
#: insertion order, or one single-product PLACE) that maximises the final SELL row's revenue.
TERMINAL_DEPOSIT_VALUE_ON = True
#: finding 2: _project/_trace replay the tile effects of WATER/FERTILIZE (+ the PLANT/DIG/BUILD they depend on) before a
#: later HARVEST and use the engine's structure-first animal PLACE predicate (V1's) instead of "outside shed access".
PROJECT_TILE_STATE_ON = False
#: finding 4, PRIVATE COPY of REVFIX1's edit (same name) for paired arms only: V3 never displaces the WATER of a tile
#: that is empty now but planted earlier in the retained plan.
PROTECT_PLANT_WATER_ON = False
FIRES = {'term': 0, 'term_changed': 0}  # diagnostics only
_ACCESS = tuple((x, y) for x in (spec.BOARD // 2 - 1, spec.BOARD // 2)
                for y in (spec.BOARD // 2 - 1, spec.BOARD // 2))


def _sale_slot(plan, hour, product):
    op, arg, _ = plan[3:]
    same = np.flatnonzero((op[hour] == O.MO_SELL) & (arg[hour] == product))
    empty = np.flatnonzero(op[hour] == O.MO_NONE)
    return int(same[0]) if len(same) else int(empty[0]) if len(empty) else None


def _add_sale(plan, hour, product, units):
    slot = _sale_slot(plan, hour, product)
    if slot is None:
        return False
    op, arg, qty = plan[3:]
    old = int(qty[hour, slot]) if op[hour, slot] == O.MO_SELL else 0
    op[hour, slot], arg[hour, slot], qty[hour, slot] = O.MO_SELL, product, old + units
    return True


def guard(plan, obs, pending):
    """Patch this day's numpy plan; ``pending`` tracks only outstanding rescues.

    A worker is diverted only after its last productive operation. Existing
    sales against shed stock and our outstanding deliveries reduce the deficit;
    no crop/animal harvest, feed, watering or planting chain is truncated.
    """
    hour = int(obs['hour'])
    if hour < 10:
        return
    player = int(obs.get('player', 0))
    farm, private = obs['farms'][player], obs['private']
    shed, inventories = private['shed'], private['inventories']
    positions = [farm['farmer'], *farm['hands']]
    uop, ua, uq, mop, ma, mq = plan
    pending[:] = [(t, p, n) for t, p, n in pending if t >= hour]
    total = sum(shed.values()) + sum(sum(v.values()) for v in inventories)
    if total <= spec.SHED_CAPACITY:
        return
    # Inputs still assigned to FEED/FERTILIZE/animal PLACE disappear before night. Preserve
    # their queued shed pickups as well as the inputs already in each hand.
    reserved_shed = np.zeros(spec.N_ITEMS, np.int32)
    consumed = 0
    for p, operation in ((spec.I_WHEAT, O.OP_FEED), (spec.I_FERT, O.OP_FERTILIZE),
                         (spec.I_GOOSE, O.OP_PLACE), (spec.I_COW, O.OP_PLACE),
                         (spec.I_SHEEP, O.OP_PLACE)):
        need_shed = 0
        for u, cargo in enumerate(inventories[:len(positions)]):
            uses = uop[u, hour:] == operation
            if operation == O.OP_PLACE:
                uses = uses & (ua[u, hour:] == p)
            need = int(np.count_nonzero(uses))
            held = min(need, cargo.get(spec.ITEMS[p], 0))
            consumed += held
            pickup = int(np.sum(np.where(
                (uop[u, hour:] == O.OP_PICKUP) & (ua[u, hour:] == p), uq[u, hour:], 0)))
            reserved_shed[p] += pickup
            need_shed += min(max(0, need - held), pickup)
        consumed += min(shed.get(spec.ITEMS[p], 0), need_shed)
    asked = np.zeros(spec.N_PRODUCTS, np.int32)
    for t in range(hour, spec.TURNS_PER_DAY):
        for s in range(spec.MAX_MARKET_ORDERS):
            if mop[t, s] == O.MO_SELL:
                asked[int(ma[t, s])] += int(mq[t, s])
    deliveries = np.zeros(spec.N_PRODUCTS, np.int32)
    for _, p, n in pending:
        deliveries[p] += n
    covered = sum(min(max(0, int(asked[p] - deliveries[p])), max(0, shed.get(name, 0) - int(reserved_shed[p])))
                  for p, name in enumerate(spec.PRODUCTS))
    excess = max(0, total - consumed - covered - sum(n for _, _, n in pending) - spec.SHED_CAPACITY)

    # Exactly LAW 0.9's cheapest-marginal-first ranking, using the planner's
    # existing table and quote machinery. No independent price approximation.
    inv = np.array([obs['market']['inventory'][p] for p in spec.PRODUCTS], np.int32)
    marginal = P.PJ.marginal_quote(np, P.PJ.sell_quotes(
        np, P.default_price_table(), inv), asked)
    order = sorted(range(spec.N_PRODUCTS), key=lambda p: (int(marginal[p]), p))
    if excess:
        # Stock already in the shed needs no worker. Leave everything already
        # offered by the day's sale rows alone; only add uncovered units.
        for p in order:
            n = min(excess, max(0, shed.get(spec.PRODUCTS[p], 0) - max(0, int(asked[p] - deliveries[p])) - int(reserved_shed[p])))
            if n and _add_sale(plan, hour, p, n):
                excess -= n
                asked[p] += n
            if not excess:
                break

    # Terminal routes already bank their harvest. Protect their DROP below,
    # but don't replace those routes or retime their planned liquidation.
    if excess and int(obs['day']) < spec.N_DAYS - 1:
        candidates = []
        for u, (pos, cargo) in enumerate(zip(positions, inventories)):
            if not np.isin(uop[u, hour:], _TAIL).all():
                continue
            x, y = map(int, pos)
            hx, hy = min(_ACCESS, key=lambda a: abs(a[0]-x) + abs(a[1]-y))
            distance = abs(hx-x) + abs(hy-y)
            arrival = hour + distance
            if arrival >= spec.TURNS_PER_DAY:
                continue
            care = int(np.count_nonzero(uop[u, hour:] == O.OP_CARE))
            for p in order:
                n = min(excess, cargo.get(spec.PRODUCTS[p], 0))
                if n and _sale_slot(plan, arrival, p) is not None:
                    candidates.append((care, distance, int(marginal[p]), -n, u, p, hx, hy))
        used = set()
        for _, distance, _, _, u, p, hx, hy in sorted(candidates):
            if u in used or not excess:
                continue
            n = min(excess, inventories[u].get(spec.PRODUCTS[p], 0), spec.SHED_CAPACITY)
            arrival = hour + distance
            if not _add_sale(plan, arrival, p, n):
                continue
            x, y = map(int, positions[u])
            uop[u, hour:] = O.OP_PASS
            ua[u, hour:] = 0
            uq[u, hour:] = 0
            t = hour
            while x != hx:
                uop[u, t] = O.OP_EAST if hx > x else O.OP_WEST
                x += 1 if hx > x else -1
                t += 1
            while y != hy:
                uop[u, t] = O.OP_SOUTH if hy > y else O.OP_NORTH
                y += 1 if hy > y else -1
                t += 1
            uop[u, arrival], ua[u, arrival], uq[u, arrival] = O.OP_PLACE, p, n
            pending.append((arrival, p, n))
            used.add(u)
            excess -= n

    # DROP destroys overflow BEFORE this hour's SELL. PLACE clips safely and
    # retains the rest in the hand. Track shared room in engine unit order.
    projected_shed = dict(shed)
    room = max(0, spec.SHED_CAPACITY - sum(projected_shed.values()))
    for u, (pos, cargo) in enumerate(zip(positions, inventories)):
        if tuple(pos) not in _ACCESS:
            continue
        op = int(uop[u, hour])
        if op == O.OP_PICKUP:
            item = spec.ITEMS[int(ua[u, hour])]
            take = min(int(uq[u, hour]), projected_shed.get(item, 0))
            projected_shed[item] = projected_shed.get(item, 0) - take
            room += take
        elif op == O.OP_PLACE:
            item = spec.ITEMS[int(ua[u, hour])]
            tile = farm['tiles'][pos[1]][pos[0]]
            structure = 'COOP' if item == 'GOOSE' else 'PASTURE'
            if (item in spec.ANIMALS and isinstance(tile, dict)
                    and tile.get('kind') == structure and 'animal' not in tile):
                continue  # animal placement consumes cargo; it doesn't fill the shed
            take = min(room, int(uq[u, hour]), cargo.get(item, 0))
            projected_shed[item] = projected_shed.get(item, 0) + take
            room -= take
        elif op == O.OP_DROP:
            load = sum(cargo.values())
            if load > room and TERMINAL_DEPOSIT_VALUE_ON and int(obs['day']) == spec.N_DAYS - 1 \
                    and hour == spec.TURNS_PER_DAY - 2:
                room = _terminal_deposit(plan, obs, u, hour, cargo, room, projected_shed, order)
                continue
            if load > room:
                p = next((p for p in order if cargo.get(spec.PRODUCTS[p], 0)), None)
                uop[u, hour] = O.OP_PASS if p is None else O.OP_PLACE
                if p is not None:
                    n = min(room, cargo[spec.PRODUCTS[p]])
                    ua[u, hour], uq[u, hour] = p, n
                    room -= n
                    item = spec.PRODUCTS[p]
                    projected_shed[item] = projected_shed.get(item, 0) + n
                    # Retry at the same position only when the original next
                    # turn was idle. Never insert a deposit into a moving route.
                    if hour + 1 < spec.TURNS_PER_DAY and uop[u, hour + 1] == O.OP_PASS:
                        uop[u, hour + 1] = O.OP_DROP
            else:
                room -= load
                for item, n in cargo.items():
                    projected_shed[item] = projected_shed.get(item, 0) + n


# --- OVERFLOW3 (plan.OVERFLOW_GUARD_V2): project tonight's stock from the plan ---
_MOVE = {O.OP_NORTH: (0, -1), O.OP_SOUTH: (0, 1), O.OP_EAST: (1, 0), O.OP_WEST: (-1, 0)}


def _project(plan, obs, hour):
    """Simulate the rest of today's plan on the observed farm (crop/animal yields,
    feed/fertilize/pickup/deposit); return per-unit end cargo, end position and
    last productive hour, plus the projected shed after today's sale rows."""
    if PROJECT_TILE_STATE_ON:
        return _replay_ts(plan, obs, hour, False)
    player = int(obs.get('player', 0))
    farm, private = obs['farms'][player], obs['private']
    uop, ua, uq, mop, ma, mq = plan
    tiles = farm['tiles']
    positions = [farm['farmer'], *farm['hands']]
    cargo = [np.array([inv.get(p, 0) for p in spec.ITEMS], np.int64)
             for inv in private['inventories'][:len(positions)]]
    while len(cargo) < len(positions):
        cargo.append(np.zeros(len(spec.ITEMS), np.int64))
    shed = np.array([private['shed'].get(p, 0) for p in spec.ITEMS], np.int64)
    pos = [list(map(int, p)) for p in positions]
    last = [hour - 1] * len(pos)
    at_last = [tuple(p) for p in pos]
    taken = set()
    fert_taken = set()
    for t in range(hour, spec.TURNS_PER_DAY):
        for u in range(len(pos)):
            op = int(uop[u, t])
            x, y = pos[u]
            if op in _MOVE:
                dx, dy = _MOVE[op]
                nx, ny = x + dx, y + dy
                if 0 <= nx < spec.BOARD and 0 <= ny < spec.BOARD:
                    pos[u] = [nx, ny]
                continue
            if op in (O.OP_PASS, O.OP_CARE):
                continue
            last[u], at_last[u] = t, (x, y)
            tile = tiles[y][x]
            if op == O.OP_HARVEST and isinstance(tile, dict) and (x, y) not in taken:
                n = int(tile.get('yield_units', 0) or 0)
                if n > 0:
                    taken.add((x, y))
                    if tile.get('kind') == 'PLANT':
                        cargo[u][spec.ITEMS.index(tile['crop'])] += n
                    elif 'animal' in tile:
                        prod = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}[tile['animal']]
                        cargo[u][spec.ITEMS.index(prod)] += n
            elif op == O.OP_COLLECT_FERT and isinstance(tile, dict) and tile.get('fertilizer_available') \
                    and (x, y) not in fert_taken:
                fert_taken.add((x, y))
                cargo[u][spec.I_FERT] += 1
            elif op == O.OP_FEED:
                if cargo[u][spec.I_WHEAT] > 0:
                    cargo[u][spec.I_WHEAT] -= 1
            elif op == O.OP_FERTILIZE:
                if cargo[u][spec.I_FERT] > 0:
                    cargo[u][spec.I_FERT] -= 1
            elif op == O.OP_PICKUP and (x, y) in _ACCESS:
                i = int(ua[u, t]); n = min(int(uq[u, t]), int(shed[i]))
                shed[i] -= n; cargo[u][i] += n
            elif op == O.OP_PLACE:
                i = int(ua[u, t])
                if spec.ITEMS[i] in spec.ANIMALS and (x, y) not in _ACCESS:
                    cargo[u][i] = max(0, cargo[u][i] - 1)
                elif (x, y) in _ACCESS:
                    n = min(int(uq[u, t]), int(cargo[u][i]), max(0, spec.SHED_CAPACITY - int(shed.sum())))
                    shed[i] += n; cargo[u][i] -= n
            elif op == O.OP_DROP and (x, y) in _ACCESS:
                room = max(0, spec.SHED_CAPACITY - int(shed.sum()))
                for i in range(len(spec.ITEMS)):
                    take = min(room, int(cargo[u][i]))
                    shed[i] += take; room -= take
                cargo[u][:] = 0
        for s in range(spec.MAX_MARKET_ORDERS):
            if mop[t, s] == O.MO_SELL:
                i = int(ma[t, s]); n = min(int(mq[t, s]), int(shed[i]))
                shed[i] -= n
    return cargo, pos, last, at_last, shed


def _route(uop, ua, uq, u, start, frm, dest):
    x, y = frm; hx, hy = dest; t = start
    while x != hx:
        uop[u, t] = O.OP_EAST if hx > x else O.OP_WEST
        ua[u, t] = uq[u, t] = 0
        x += 1 if hx > x else -1; t += 1
    while y != hy:
        uop[u, t] = O.OP_SOUTH if hy > y else O.OP_NORTH
        ua[u, t] = uq[u, t] = 0
        y += 1 if hy > y else -1; t += 1
    return t


def guard_v2(plan, obs, pending):
    """Bank tonight's PROJECTED overflow (V1 only sees the observed stock).

    1. Finished carriers: a unit whose remaining plan after its last productive
       op is idle walks to the nearest access tile, PLACEs its cheapest-marginal
       projected cargo and the same hour's SELL row liquidates it; extra idle
       hours after arrival PLACE further products.
    2. En-route deposit: a unit standing on an access tile with cargo and a
       later PASS gets one PLACE inserted now; its remaining ops shift one hour
       and exactly one later PASS is dropped. No productive op is removed.
    Terminal day is left to the end routes.
    """
    hour = int(obs['hour'])
    if hour < 10 or int(obs['day']) >= spec.N_DAYS - 1:
        return
    uop, ua, uq, mop, ma, mq = plan
    cargo, end_pos, last, at_last, shed_end = _project(plan, obs, hour)
    total = int(shed_end.sum()) + int(sum(c.sum() for c in cargo))
    excess = total - spec.SHED_CAPACITY
    if excess <= 0:
        return
    asked = np.zeros(spec.N_PRODUCTS, np.int32)
    for t in range(hour, spec.TURNS_PER_DAY):
        for s in range(spec.MAX_MARKET_ORDERS):
            if mop[t, s] == O.MO_SELL:
                asked[int(ma[t, s])] += int(mq[t, s])
    inv = np.array([obs['market']['inventory'][p] for p in spec.PRODUCTS], np.int32)
    marginal = P.PJ.marginal_quote(np, P.PJ.sell_quotes(np, P.default_price_table(), inv), asked)
    order = sorted(range(spec.N_PRODUCTS), key=lambda p: (int(marginal[p]), p))
    player = int(obs.get('player', 0))
    farm, private = obs['farms'][player], obs['private']
    positions = [farm['farmer'], *farm['hands']]

    # 1. finished carriers (plan already committed: only idle ops after `last`)
    cands = []
    for u in range(len(positions)):
        start = max(hour, last[u] + 1)
        if start >= spec.TURNS_PER_DAY or not np.isin(uop[u, start:], _TAIL).all():
            continue
        frm = at_last[u] if last[u] >= hour else tuple(map(int, positions[u]))
        dest = min(_ACCESS, key=lambda a: abs(a[0]-frm[0]) + abs(a[1]-frm[1]))
        arrival = start + abs(dest[0]-frm[0]) + abs(dest[1]-frm[1])
        load = int(cargo[u][:spec.N_PRODUCTS].sum())
        if arrival >= spec.TURNS_PER_DAY or not load:
            continue
        care = int(np.count_nonzero(uop[u, start:] == O.OP_CARE))
        cands.append((care, arrival, -load, u, start, frm, dest))
    for care, arrival, _, u, start, frm, dest in sorted(cands):
        if excess <= 0:
            break
        t = _route(uop, ua, uq, u, start, frm, dest)
        uop[u, t:] = O.OP_PASS; ua[u, t:] = 0; uq[u, t:] = 0
        for p in order:
            if excess <= 0 or t >= spec.TURNS_PER_DAY:
                break
            n = min(excess, int(cargo[u][p]))
            if n and _add_sale(plan, t, p, n):
                uop[u, t], ua[u, t], uq[u, t] = O.OP_PLACE, p, n
                pending.append((t, p, n))
                excess -= n
                t += 1

    # 2. en-route deposit at the current hour
    if excess <= 0:
        return
    inventories = private['inventories']
    for u, pos in enumerate(positions):
        if excess <= 0:
            break
        if tuple(map(int, pos)) not in _ACCESS or u >= len(inventories):
            continue
        later = np.flatnonzero(uop[u, hour + 1:] == O.OP_PASS)
        if not len(later):
            continue
        k = hour + 1 + int(later[0])
        if np.isin(uop[u, hour:k], (O.OP_PLACE, O.OP_DROP, O.OP_PICKUP)).any():
            continue  # never retime a shed transaction tied to a sale row
        held = inventories[u]
        p = next((p for p in order if held.get(spec.PRODUCTS[p], 0)), None)
        if p is None:
            continue
        n = min(excess, held[spec.PRODUCTS[p]])
        if not _add_sale(plan, hour, p, n):
            continue
        for arr in (uop, ua, uq):
            arr[u, hour + 1:k + 1] = arr[u, hour:k].copy()
        uop[u, hour], ua[u, hour], uq[u, hour] = O.OP_PLACE, p, n
        pending.append((hour, p, n))
        excess -= n


# --- OVERFLOW4 (plan.OVERFLOW_GUARD_V3): value-priced displacement of late jobs ---
# V2's residue is crew busy to dusk: every unit works until hour 23 and carries
# the day's harvest into the night transfer (the plan never visits the shed).
# V3 cuts a deposit trip into ONE unit's day when the jobs it displaces are
# worth less than the units the trip saves from tonight's destruction:
#   mode A: from hour t walk to the shed, DROP/PLACE, idle (displaces ops t..23);
#   mode B: detour at t (walk in, deposit, walk back), later ops shift 2d+1
#           hours, displacing the day's LAST 2d+1 ops.
# Job prices (engine rules, src/kagg3/sim/units.py + eod.py):
#   WATER   0 when the tile is already watered today / emptied earlier; INF when
#           planted today or consecutive_unwatered >= 1 (the tile dies tonight);
#           one-time crop in its watering window below max yield: bonus x price;
#           fertilized ongoing crop that fires tonight: 1 x price; else a 0.25
#           risk price (one dry day is survivable, two kill).
#   HARVEST one-time crop younger than its max-yield day stays ripe -> 0; at or
#           past it the crop rots from tomorrow's hour 0 -> n x price. Ongoing
#           crops/animals: only the units the per-tile cap would clip.
#   COLLECT_FERT uncollected fertilizer resets nightly -> fert price.
#   PLANT   one day of the crop cycle (full yield if it could no longer mature).
#   CARE    half a unit of the animal product. FEED/FERTILIZE/shed ops/DIG/BUILD: INF.
# Saved value = units no longer destroyed (sold on the deposit hour, cheapest-
# marginal first like V1/V2, or left ripe on the tile) at the marginal quote.
# A candidate is taken only when saved value > displaced value.
_INF = float('inf')
_SHED_OPS = (O.OP_PLACE, O.OP_DROP, O.OP_PICKUP)
_BAD = (O.OP_FEED, O.OP_FERTILIZE, O.OP_DIG, O.OP_BUILD_COOP, O.OP_BUILD_PASTURE) + _SHED_OPS
_ANIMAL_PROD = {'GOOSE': spec.I_EGG, 'COW': spec.I_MILK, 'SHEEP': spec.I_WOOL}
V3_LOG = None  # diagnostics: a list here collects (day, hour, unit, mode, t0, displaced ops, value, cost)


def _trace(plan, obs, hour):
    """_project, recorded: pos/cargo/shed at the START of every hour t in
    [hour, 24] (index t - hour) and the tile each unit acts on at t."""
    if PROJECT_TILE_STATE_ON:
        return _replay_ts(plan, obs, hour, True)
    player = int(obs.get('player', 0))
    farm, private = obs['farms'][player], obs['private']
    uop, ua, uq, mop, ma, mq = plan
    tiles = farm['tiles']
    positions = [farm['farmer'], *farm['hands']]
    cargo = [np.array([inv.get(p, 0) for p in spec.ITEMS], np.int64)
             for inv in private['inventories'][:len(positions)]]
    while len(cargo) < len(positions):
        cargo.append(np.zeros(len(spec.ITEMS), np.int64))
    shed = np.array([private['shed'].get(p, 0) for p in spec.ITEMS], np.int64)
    pos = [tuple(map(int, p)) for p in positions]
    P_, C_, S_, A_ = [], [], [], []
    taken, fert_taken = set(), set()
    for t in range(hour, spec.TURNS_PER_DAY):
        P_.append(list(pos)); C_.append([c.copy() for c in cargo]); S_.append(shed.copy()); A_.append(list(pos))
        for u in range(len(pos)):
            op = int(uop[u, t]); x, y = pos[u]
            if op in _MOVE:
                dx, dy = _MOVE[op]
                if 0 <= x + dx < spec.BOARD and 0 <= y + dy < spec.BOARD:
                    pos[u] = (x + dx, y + dy)
                continue
            tile = tiles[y][x]
            if op == O.OP_HARVEST and isinstance(tile, dict) and (x, y) not in taken:
                n = int(tile.get('yield_units', 0) or 0)
                if n > 0:
                    taken.add((x, y))
                    if tile.get('kind') == 'PLANT':
                        cargo[u][spec.ITEMS.index(tile['crop'])] += n
                    elif 'animal' in tile:
                        cargo[u][_ANIMAL_PROD[tile['animal']]] += n
            elif op == O.OP_COLLECT_FERT and isinstance(tile, dict) and tile.get('fertilizer_available') \
                    and (x, y) not in fert_taken:
                fert_taken.add((x, y)); cargo[u][spec.I_FERT] += 1
            elif op == O.OP_FEED and cargo[u][spec.I_WHEAT] > 0:
                cargo[u][spec.I_WHEAT] -= 1
            elif op == O.OP_FERTILIZE and cargo[u][spec.I_FERT] > 0:
                cargo[u][spec.I_FERT] -= 1
            elif op == O.OP_PICKUP and (x, y) in _ACCESS:
                i = int(ua[u, t]); n = min(int(uq[u, t]), int(shed[i]))
                shed[i] -= n; cargo[u][i] += n
            elif op == O.OP_PLACE:
                i = int(ua[u, t])
                if spec.ITEMS[i] in spec.ANIMALS and (x, y) not in _ACCESS:
                    cargo[u][i] = max(0, cargo[u][i] - 1)
                elif (x, y) in _ACCESS:
                    n = min(int(uq[u, t]), int(cargo[u][i]), max(0, spec.SHED_CAPACITY - int(shed.sum())))
                    shed[i] += n; cargo[u][i] -= n
            elif op == O.OP_DROP and (x, y) in _ACCESS:
                room = max(0, spec.SHED_CAPACITY - int(shed.sum()))
                for i in range(len(spec.ITEMS)):
                    take = min(room, int(cargo[u][i])); shed[i] += take; room -= take
                cargo[u][:] = 0
        for s in range(spec.MAX_MARKET_ORDERS):
            if mop[t, s] == O.MO_SELL:
                i = int(ma[t, s]); shed[i] -= min(int(mq[t, s]), int(shed[i]))
    P_.append(list(pos)); C_.append([c.copy() for c in cargo]); S_.append(shed.copy())
    return P_, C_, S_, A_


def _job_cost(op, arg, tile, day, before, marginal):
    """Value of one displaced job; ``before`` = ops kept on this tile earlier today."""
    if op in _TAIL and op != O.OP_CARE:
        return 0.0
    if op in _BAD:
        return _INF
    if not isinstance(tile, dict):
        if PROTECT_PLANT_WATER_ON and op == O.OP_WATER and O.OP_PLANT in before:
            return _INF
        return 0.0 if op in (O.OP_WATER, O.OP_HARVEST, O.OP_COLLECT_FERT, O.OP_CARE) else _INF
    kind = tile.get('kind')
    if op == O.OP_CARE:
        a = tile.get('animal')
        return 0.5 * float(marginal[_ANIMAL_PROD[a]]) if a and not tile.get('cared_today') else 0.0
    if op == O.OP_COLLECT_FERT:
        return float(marginal[spec.I_FERT]) if tile.get('fertilizer_available') \
            and O.OP_COLLECT_FERT not in before else 0.0
    if op == O.OP_PLANT:
        c = int(arg)
        if day + 1 + int(spec.CROP_MAX_YIELD_DAY[c]) > spec.N_DAYS - 1:
            return float(spec.CROP_MAX_YIELD[c]) * float(marginal[c])
        return float(marginal[c]) * float(spec.CROP_MAX_YIELD[c]) / (int(spec.CROP_MAX_YIELD_DAY[c]) + 1)
    if kind == 'PLANT':
        c = spec.CROPS.index(tile['crop'])
        age = day - int(tile.get('planted_day', day))
        n = int(tile.get('yield_units', 0) or 0)
        ongoing = bool(spec.CROP_ONGOING[c])
        if op == O.OP_WATER:
            if O.OP_PLANT in before:
                return _INF
            if O.OP_HARVEST in before and not ongoing:
                return 0.0
            if tile.get('watered_today') or O.OP_WATER in before:
                return 0.0
            if age <= 0 or int(tile.get('consecutive_unwatered', 0)) >= 1:
                return _INF
            fert = int(tile.get('fertilized_until_day', -1)) >= day
            if not ongoing:
                if int(spec.CROP_WINDOW_START[c]) <= age <= int(spec.CROP_MAX_YIELD_DAY[c]) \
                        and n < int(spec.CROP_MAX_YIELD[c]):
                    return (2.0 if fert else 1.0) * float(marginal[c])
            elif fert:
                return float(marginal[c])
            return 0.25 * float(marginal[c])
        if op == O.OP_HARVEST:
            if O.OP_HARVEST in before or n <= 0:
                return 0.0
            if not ongoing:
                if age >= int(spec.CROP_MAX_YIELD_DAY[c]):
                    return n * float(marginal[c])          # rots from tomorrow's hour 0
                # stays ripe; the tile's next cycle starts a day later
                return float(marginal[c]) * float(spec.CROP_MAX_YIELD[c]) / (int(spec.CROP_MAX_YIELD_DAY[c]) + 1)
            return max(0, n + 2 - int(spec.CROP_MAX_YIELD[c])) * float(marginal[c])
        return _INF
    if op == O.OP_WATER:
        return 0.0 if O.OP_PLANT not in before else _INF
    if op == O.OP_HARVEST and tile.get('animal'):
        a = spec.ANIMALS.index(tile['animal'])
        n = int(tile.get('yield_units', 0) or 0)
        if O.OP_HARVEST in before or n <= 0:
            return 0.0
        return max(0, n + 2 - int(spec.ANIMAL_MAX_HELD[a])) * float(marginal[spec.ANIMAL_PRODUCT[a]])
    return 0.0 if op == O.OP_HARVEST else _INF


def guard_v3(plan, obs, pending, max_trips=3):
    """Value-priced deposit trips for the busy-to-dusk overflow (after V1/V2)."""
    hour, day = int(obs['hour']), int(obs['day'])
    if hour < 10 or day >= spec.N_DAYS - 1:
        return
    player = int(obs.get('player', 0))
    tiles = obs['farms'][player]['tiles']
    uop, ua, uq, mop, ma, mq = plan
    min_net = float(getattr(P, 'OVERFLOW_GUARD_V3_MIN_NET', 0.0))
    defer_w = float(getattr(P, 'OVERFLOW_GUARD_V3_DEFER_W', 1.0))
    for _ in range(max_trips):
        P_, C_, S_, A_ = _trace(plan, obs, hour)
        excess = int(S_[-1].sum()) + int(sum(c.sum() for c in C_[-1])) - spec.SHED_CAPACITY
        if excess <= 0:
            return
        asked = np.zeros(spec.N_PRODUCTS, np.int32)
        for t in range(hour, spec.TURNS_PER_DAY):
            for s in range(spec.MAX_MARKET_ORDERS):
                if mop[t, s] == O.MO_SELL:
                    asked[int(ma[t, s])] += int(mq[t, s])
        inv = np.array([obs['market']['inventory'][p] for p in spec.PRODUCTS], np.int32)
        marginal = P.PJ.marginal_quote(np, P.PJ.sell_quotes(np, P.default_price_table(), inv), asked)
        marginal = np.maximum(np.asarray(marginal, np.float64), 0.0)
        order = sorted(range(spec.N_PRODUCTS), key=lambda p: (int(marginal[p]), p))
        # every kept job per tile, in engine order (hour, unit)
        H, U = spec.TURNS_PER_DAY - hour, len(P_[0])
        jobs = {}
        for k in range(H):
            for u in range(U):
                op = int(uop[u, hour + k])
                if op not in _MOVE and op != O.OP_PASS:
                    jobs.setdefault(A_[k][u], []).append((k, u, op))
        best = None
        for u in range(U):
            ops_u = [int(uop[u, hour + k]) for k in range(H)]
            for k in range(H):
                frm = P_[k][u]
                dest = min(_ACCESS, key=lambda a: abs(a[0]-frm[0]) + abs(a[1]-frm[1]))
                d = abs(dest[0]-frm[0]) + abs(dest[1]-frm[1])
                cargo = C_[k][u]
                tail_ops = ops_u[k:]
                later_feed = tail_ops.count(O.OP_FEED); later_fert = tail_ops.count(O.OP_FERTILIZE)
                for mode in (('A', 'B', 'C') if getattr(P, 'OVERFLOW_GUARD_V3_CUT', True) else ('A', 'B')):
                    a = k + d
                    if mode in 'AC':
                        if mode == 'A' and a >= H:
                            continue
                        gone = list(range(k, H))
                        reserve = np.zeros(len(spec.ITEMS), np.int64)
                    else:
                        if d > 3 or a + d + 1 >= H or any(o in _SHED_OPS for o in tail_ops):
                            continue
                        gone = list(range(H - (2 * d + 1), H))
                        reserve = np.zeros(len(spec.ITEMS), np.int64)
                        reserve[spec.I_WHEAT], reserve[spec.I_FERT] = later_feed, later_fert
                    gone_set = {(g, u) for g in gone}
                    cost = 0.0; tail = np.zeros(len(spec.ITEMS), np.int64)
                    for g in gone:
                        op = ops_u[g]
                        x, y = A_[g][u]
                        before = [o for (kk, uu, o) in jobs.get((x, y), ())
                                  if (kk, uu) < (g, u) and (kk, uu) not in gone_set]
                        cost += _job_cost(op, ua[u, hour + g], tiles[y][x], day, before, marginal)
                        if cost == _INF:
                            break
                        if op in (O.OP_HARVEST, O.OP_COLLECT_FERT):
                            tail += np.maximum(0, C_[g + 1][u] - C_[g][u])
                    if cost == _INF:
                        continue
                    # displaced harvests stay on the tile (tail); A/B also deposit
                    avail = np.maximum(0, cargo - reserve)[:spec.N_PRODUCTS]
                    if mode == 'C':
                        avail[:] = 0; a = k
                    room = spec.SHED_CAPACITY - int(S_[min(a, H)].sum())
                    animals = int(cargo[spec.N_PRODUCTS:].sum())
                    if not reserve.any() and not animals and room >= int(cargo.sum()):
                        dep = avail.copy(); how = 'DROP'
                    else:
                        p = int(np.argmax(avail)); dep = np.zeros_like(avail)
                        dep[p] = min(int(avail[p]), max(0, room)); how = 'PLACE'
                    left = excess; value = 0.0
                    for p in range(spec.N_PRODUCTS):  # left on the tile: sold a day later
                        n = min(left, int(tail[p])); value += n * float(marginal[p]) * defer_w; left -= n
                    sells = []
                    for p in order:
                        n = min(left, int(dep[p]))
                        if n > 0:
                            sells.append((p, n)); value += n * float(marginal[p]); left -= n
                    free = int(np.count_nonzero(mop[hour + a] == O.MO_NONE))
                    need = sum(1 for p, _ in sells if not np.any(
                        (mop[hour + a] == O.MO_SELL) & (ma[hour + a] == p)))
                    if (mode != 'C' and not sells) or (mode == 'C' and left == excess) \
                            or need > free or value - cost <= min_net:
                        continue
                    key = (value - cost, k, -u)
                    if best is None or key > best[0]:
                        best = (key, u, k, mode, d, dest, frm, how, dep, sells)
        if best is None:
            return
        (net, _, _), u, k, mode, d, dest, frm, how, dep, sells = best
        t0 = hour + k
        if V3_LOG is not None:
            g0 = k if mode in 'AC' else H - (2 * d + 1)
            V3_LOG.append((day, hour, u, mode, t0, [O.OP_NAMES.get(int(o), o) for o in uop[u, hour + g0:]],
                           round(float(net), 1), [(int(p), int(n)) for p, n in sells]))
        if mode == 'C':  # cut: the displaced jobs only fed tonight's destruction
            uop[u, t0:] = O.OP_PASS; ua[u, t0:] = 0; uq[u, t0:] = 0
            continue
        old = [arr[u].copy() for arr in (uop, ua, uq)]
        t = _route(uop, ua, uq, u, t0, frm, dest)
        if how == 'DROP':
            uop[u, t], ua[u, t], uq[u, t] = O.OP_DROP, 0, 0
        else:
            p = int(np.argmax(dep))
            uop[u, t], ua[u, t], uq[u, t] = O.OP_PLACE, p, int(dep[p])
        for p, n in sells:
            _add_sale(plan, t, p, n)
            pending.append((t, p, n))
        if mode == 'A':
            uop[u, t + 1:] = O.OP_PASS; ua[u, t + 1:] = 0; uq[u, t + 1:] = 0
        else:
            back = _route(uop, ua, uq, u, t + 1, dest, frm)  # walk back x then y: any Manhattan path
            n = spec.TURNS_PER_DAY - back
            for arr, o in zip((uop, ua, uq), old):
                arr[u, back:] = o[t0:t0 + n]


# --- REVFIX2 (finding 3): the last executed turn's deposit, valued on the final SELL row ---
def _terminal_deposit(plan, obs, u, hour, cargo, room, projected_shed, order):
    """d29 h22 is the last executed turn (h23 never resolves): stock left in a hand is worth zero and the
    same turn's SELL row liquidates the shed. Compare the unchanged DROP (engine deposit in cargo insertion
    order, the rest destroyed) with each single-product PLACE on the final row's revenue (planner quote walk
    from the observed market inventory, on top of the shed as projected for the earlier units); ties keep
    DROP. The chosen deposit is booked in ``projected_shed``/room for the later units and the row is
    topped up so its SELL quantities cover the accepted stock. Returns the remaining room."""
    uop, ua, uq, mop, ma, mq = plan
    FIRES['term'] += 1
    inv = np.array([obs['market']['inventory'][p] for p in spec.PRODUCTS], np.int32)
    quotes = P.PJ.sell_quotes(np, P.default_price_table(), inv)
    base = np.array([projected_shed.get(p, 0) for p in spec.PRODUCTS], np.int32)

    def revenue(dep):
        after = base + np.array([dep.get(p, 0) for p in spec.PRODUCTS], np.int32)
        return int(np.sum(P.PJ.sell_revenue(np, quotes, np.minimum(after, P.PJ.K - 1)), dtype=np.int64))

    left, drop = room, {}
    for item, n in cargo.items():   # the engine deposits a DROP in cargo insertion order
        take = min(left, int(n))
        if take > 0:
            drop[item] = take
            left -= take
    best = (revenue(drop), None, drop)
    for p in order:
        n = min(room, int(cargo.get(spec.PRODUCTS[p], 0)))
        if n > 0:
            dep = {spec.PRODUCTS[p]: n}
            r = revenue(dep)
            if r > best[0]:
                best = (r, p, dep)
    _, p, dep = best
    if p != next((q for q in order if cargo.get(spec.PRODUCTS[q], 0)), None):
        FIRES['term_changed'] += 1    # differs from the shipped cheapest-product PLACE
    if p is not None:
        uop[u, hour], ua[u, hour], uq[u, hour] = O.OP_PLACE, p, dep[spec.PRODUCTS[p]]
    for item, n in dep.items():
        projected_shed[item] = projected_shed.get(item, 0) + n
    for q, item in enumerate(spec.PRODUCTS):
        if dep.get(item, 0):
            asked = int(np.sum(np.where((mop[hour] == O.MO_SELL) & (ma[hour] == q), mq[hour], 0)))
            short = int(projected_shed.get(item, 0)) - asked
            if short > 0:
                _add_sale(plan, hour, q, short)
    return room - sum(dep.values())


# --- REVFIX2 (finding 2): replay with the tile state the plan itself changes ---
_STRUCT_OF = {'GOOSE': 'COOP', 'COW': 'PASTURE', 'SHEEP': 'PASTURE'}


def _replay_ts(plan, obs, hour, trace):
    """_project (trace=False) / _trace (trace=True) with a copy-on-write tile view: WATER adds the engine's
    in-window yield (x2 when fertilized), FERTILIZE marks the tile (and needs a plant), PLANT/DIG/BUILD
    change the tile a later op reads, HARVEST needs age >= first-yield day and empties a one-time crop,
    and an animal PLACE goes to a compatible empty structure first (V1's predicate, engine precedence),
    else to the shed from an access tile, else nothing. Everything else is the original replay."""
    player = int(obs.get('player', 0))
    day = int(obs['day'])
    farm, private = obs['farms'][player], obs['private']
    uop, ua, uq, mop, ma, mq = plan
    tiles = farm['tiles']
    view = {}
    positions = [farm['farmer'], *farm['hands']]
    cargo = [np.array([inv.get(p, 0) for p in spec.ITEMS], np.int64)
             for inv in private['inventories'][:len(positions)]]
    while len(cargo) < len(positions):
        cargo.append(np.zeros(len(spec.ITEMS), np.int64))
    shed = np.array([private['shed'].get(p, 0) for p in spec.ITEMS], np.int64)
    if trace:
        pos = [tuple(map(int, p)) for p in positions]
        P_, C_, S_, A_ = [], [], [], []
    else:
        pos = [list(map(int, p)) for p in positions]
        last = [hour - 1] * len(pos)
        at_last = [tuple(p) for p in pos]
    taken, fert_taken = set(), set()
    for t in range(hour, spec.TURNS_PER_DAY):
        if trace:
            P_.append(list(pos)); C_.append([c.copy() for c in cargo]); S_.append(shed.copy()); A_.append(list(pos))
        for u in range(len(pos)):
            op = int(uop[u, t])
            x, y = pos[u]
            if op in _MOVE:
                dx, dy = _MOVE[op]
                nx, ny = x + dx, y + dy
                if 0 <= nx < spec.BOARD and 0 <= ny < spec.BOARD:
                    pos[u] = (nx, ny) if trace else [nx, ny]
                continue
            if not trace:
                if op in (O.OP_PASS, O.OP_CARE):
                    continue
                last[u], at_last[u] = t, (x, y)
            tile = view[(x, y)] if (x, y) in view else tiles[y][x]
            if op == O.OP_HARVEST and isinstance(tile, dict) and (x, y) not in taken:
                n = int(tile.get('yield_units', 0) or 0)
                if n > 0:
                    if tile.get('kind') == 'PLANT':
                        c = spec.CROPS.index(tile['crop'])
                        if day - int(tile.get('planted_day', day)) >= int(spec.CROP_FIRST_YIELD_DAY[c]):
                            taken.add((x, y))
                            cargo[u][spec.ITEMS.index(tile['crop'])] += n
                            view[(x, y)] = dict(tile, yield_units=0) if spec.CROP_ONGOING[c] else None
                    elif 'animal' in tile:
                        taken.add((x, y))
                        cargo[u][_ANIMAL_PROD[tile['animal']]] += n
                        view[(x, y)] = dict(tile, yield_units=0)
            elif op == O.OP_WATER:
                if isinstance(tile, dict) and tile.get('kind') == 'PLANT' and not tile.get('watered_today'):
                    c = spec.CROPS.index(tile['crop'])
                    new = dict(tile, watered_today=True)
                    age = day - int(tile.get('planted_day', day))
                    if not spec.CROP_ONGOING[c] and int(spec.CROP_WINDOW_START[c]) <= age <= int(spec.CROP_MAX_YIELD_DAY[c]):
                        bonus = 2 if int(tile.get('fertilized_until_day', -1)) >= day else 1
                        new['yield_units'] = min(int(spec.CROP_MAX_YIELD[c]), int(tile.get('yield_units', 0) or 0) + bonus)
                    view[(x, y)] = new
            elif op == O.OP_COLLECT_FERT and isinstance(tile, dict) and tile.get('fertilizer_available') \
                    and (x, y) not in fert_taken:
                fert_taken.add((x, y)); cargo[u][spec.I_FERT] += 1
            elif op == O.OP_FEED:
                if cargo[u][spec.I_WHEAT] > 0:
                    cargo[u][spec.I_WHEAT] -= 1
            elif op == O.OP_FERTILIZE:
                if isinstance(tile, dict) and tile.get('kind') == 'PLANT' and cargo[u][spec.I_FERT] > 0:
                    cargo[u][spec.I_FERT] -= 1
                    view[(x, y)] = dict(tile, fertilized_until_day=max(int(tile.get('fertilized_until_day', -1)), day + 2))
            elif op == O.OP_PLANT:
                c = int(ua[u, t])
                if tile is None and 0 <= c < spec.N_CROPS:
                    view[(x, y)] = {'kind': 'PLANT', 'crop': spec.CROPS[c], 'planted_day': day, 'watered_today': False,
                                    'consecutive_unwatered': 1, 'yield_units': 0 if spec.CROP_ONGOING[c] else 1,
                                    'fertilized_until_day': -1}
            elif op == O.OP_DIG:
                if isinstance(tile, dict) and 'animal' not in tile:
                    view[(x, y)] = None
            elif op in (O.OP_BUILD_COOP, O.OP_BUILD_PASTURE):
                if tile is None:
                    view[(x, y)] = {'kind': 'COOP' if op == O.OP_BUILD_COOP else 'PASTURE'}
            elif op == O.OP_PICKUP and (x, y) in _ACCESS:
                i = int(ua[u, t]); n = min(int(uq[u, t]), int(shed[i]))
                shed[i] -= n; cargo[u][i] += n
            elif op == O.OP_PLACE:
                i = int(ua[u, t])
                item = spec.ITEMS[i]
                if item in spec.ANIMALS and isinstance(tile, dict) and tile.get('kind') == _STRUCT_OF[item] \
                        and 'animal' not in tile:
                    if cargo[u][i] > 0:   # engine: the structure takes precedence over the shed
                        cargo[u][i] -= 1
                        view[(x, y)] = {'kind': tile['kind'], 'animal': item, 'yield_units': 0}
                elif (x, y) in _ACCESS and int(uq[u, t]) > 0:
                    n = min(int(uq[u, t]), int(cargo[u][i]), max(0, spec.SHED_CAPACITY - int(shed.sum())))
                    shed[i] += n; cargo[u][i] -= n
            elif op == O.OP_DROP and (x, y) in _ACCESS:
                room = max(0, spec.SHED_CAPACITY - int(shed.sum()))
                for i in range(len(spec.ITEMS)):
                    take = min(room, int(cargo[u][i])); shed[i] += take; room -= take
                cargo[u][:] = 0
        for s in range(spec.MAX_MARKET_ORDERS):
            if mop[t, s] == O.MO_SELL:
                i = int(ma[t, s]); shed[i] -= min(int(mq[t, s]), int(shed[i]))
    if trace:
        P_.append(list(pos)); C_.append([c.copy() for c in cargo]); S_.append(shed.copy())
        return P_, C_, S_, A_
    return cargo, pos, last, at_last, shed
