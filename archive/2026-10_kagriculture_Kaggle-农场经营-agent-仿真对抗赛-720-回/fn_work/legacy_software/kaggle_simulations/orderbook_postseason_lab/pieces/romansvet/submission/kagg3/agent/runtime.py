"""Submission runtime: obs -> macro -> day plan -> per-turn action dict.

The plan is built once at hour 0 and replayed for the remaining 23 turns, which
is what keeps the per-turn cost negligible. One switch needs a fact hour 0
cannot hold -- `plan.OPEN_PUMP_TELL_KEEP0_ON` reads the other seat's hour-0
wheat draw off the *hour-1* pot -- so it is a patch on the cached plan at the
turn the row is emitted, and not an expression inside `build_day`.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

from .. import spec
from ..core import plan as P
from . import parse, render, route_nn, route_nn3, route_vrp, tell
from .overflow import guard as overflow_guard, guard_v2 as overflow_guard_v2, guard_v3 as overflow_guard_v3


# [SWITCH, KERNEL2 / V56PACK1 2026-09-28] the two-kernel runtime (`plan.KERNEL2_ON`, default OFF).
# Step 0 is the engine no-op below on every seat; at step 1 the rival's cash (public, obs farms[1-player]
# money) latches the kernel for the game: <= `plan.KERNEL2_CASH_MAX` (the MELON-family d0 spend,
# MELONHYBRID2: 49/51 MELON, 0/81 V, 7/7 ZERO, 0/3 OTHER on BAND142) hands the virgin farm to the embedded
# public V56 kernel (`v56kernel.py`, Apache-2.0) for every later turn; otherwise PFS (this Runtime) plans
# its own d0 from h1.  The production form of S/melonhybrid3/hybrid.py HY_MODE=gated.
KERNEL2_NOOP = {"farmer": ["PASS"], "hands": [], "market": []}
#: [SWITCH, RIVALSUPPLY2] diag file (env RIVALSUPPLY2_DIAG): one row per dawn = day, code, family, rival cash, rival quadrants.
FAMDIAG = __import__("os").environ.get("RIVALSUPPLY2_DIAG", "")


def kernel2_load():
    """A fresh V56 kernel callable for one game.

    Loaded exactly as kaggle_environments loads a file agent (`agent.get_last_callable`): the source is
    compiled as "<string>" and exec'd into an empty namespace, and the last callable is the agent.  Exec,
    not import: the kernel keeps its per-game state in module globals, so each game gets its own namespace.
    Anything the source prints while loading is swallowed (the engine's loader buffers it too).
    """
    import io
    import os
    import sys
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v56kernel.py")
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    code = compile(raw, "<string>", "exec")
    env = {}
    out, sys.stdout = sys.stdout, io.StringIO()
    try:
        exec(code, env)
    finally:
        sys.stdout = out
    return [v for v in env.values() if callable(v)][-1]


def kernel2_cash_list(v):
    """[SWITCH, KERNEL2FIRE1] a "|"-separated exact-cash switch value ("33|55|2339|2467") as a set of ints ("" = empty)."""
    return {int(x) for x in str(v).split("|") if x.strip()}


def kernel2_zero_rival(obs):
    """[SWITCH, ZEROGATE1] the rival has 0 MELON plantings and >= plan.KERNEL2_ZERO_MIN_PLANTS plantings on this obs."""
    p = int(obs.get("player", 0) or 0)
    n = m = 0
    for row in (obs.get("farms") or [{}, {}])[1 - p].get("tiles") or []:
        for t in row:
            if t and t != "LOCKED" and t.get("kind") == "PLANT":
                n += 1
                m += t.get("crop") == "MELON"
    return m == 0 and n >= int(P.KERNEL2_ZERO_MIN_PLANTS)


# ASTRA14 table: cumulative herd, daily seed prior, hired hands, end-day land.
PROGRAM_ANIMALS = (
    (3,2,0),(3,2,0),(3,3,0),(3,3,0),(3,3,0),(3,3,0),(3,6,1),(3,6,1),
    (3,7,1),(4,7,2),(4,8,2),(4,8,3),(4,8,4),(4,8,4),(4,8,4),(5,8,4),
    (5,8,4),(6,8,4),(6,8,4),(6,8,4),(6,8,4),(6,8,4),(6,8,4),(6,8,4),
    (6,8,4),(6,8,4),(6,8,4),(6,8,4),(6,8,4),(6,8,4),
)
# PROGFIX1 (2): cumulative herd (S, C, G) = the ENGINE's own mean buy
# schedule over the 59 faithful seat-swap boards (S/progfix1/realsched.py),
# rounded; the ASTRA14 row lagged sheep by 2-3 head from d6 on.
PROGRAM_ANIMALS_REAL = (
    (2,2,0),(2,2,0),(2,3,0),(2,3,0),(2,4,0),(3,4,0),(4,6,1),(4,6,1),
    (5,7,1),(6,7,2),(6,8,3),(7,8,3),(7,8,4),(7,8,4),(7,8,4),(7,8,4),
    (7,8,4),(7,8,4),(8,8,4),(8,8,4),(8,8,4),(8,8,4),(8,8,4),(8,8,4),
    (8,8,4),(8,8,4),(8,8,4),(8,8,4),(8,8,4),(8,8,4),
)
PROGRAM_SEEDS = (
    (10,0,0,0,6),(0,0,0,0,4),(0,0,0,1,0),(0,0,0,3,0),(0,0,0,2,0),
    (0,0,0,0,0),(2,0,0,8,0),(2,0,0,2,0),(6,0,0,0,0),(8,0,0,2,0),
    (7,0,0,0,0),(8,0,0,0,0),(6,0,0,0,0),(6,0,0,0,0),(6,0,0,0,0),
    (5,0,0,0,0),(4,0,1,0,0),(4,0,1,0,0),(5,0,2,0,0),(6,0,0,0,0),
    (6,0,0,0,0),(7,0,0,0,0),(9,1,0,0,0),(8,2,0,0,0),(8,4,0,0,0),
    (7,6,0,0,0),(6,6,0,0,0),(3,3,0,0,0),(0,0,0,0,0),(0,0,0,0,0),
)
PROGRAM_HANDS = (4,3,6,5,6,6,8,8,9,10,11,11,11,11,11,11,11,11,11,11,
                 11,11,11,11,11,11,11,11,10,10)
PROGRAM_LAND = (1,1,1,1,1,1,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3)
PROGRAM_PHASES = ((0, 9, (34,1,1,23,11)),
                  (10, 19, (54,11,10,7,1)),
                  (20, 29, (63,32,0,0,0)))


class ProgramIntent(NamedTuple):
    plant_target: object
    animal_target: object
    hands_target: int
    land_target: int
    reserve: int


class ProgramEngineState:
    """Observation-reconciled committed progress for one seat and one game."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.last_day = -1
        self.planted = np.zeros((30, spec.N_CROPS), np.int32)
        self.melon_sell_requested = np.zeros(30, np.int32)
        self.milestones = {}
        self.last_budget = {}
        self.repair_jobs = {}
        self.intent = None

    def reconcile(self, view):
        day = int(view.day)
        pay_day = int(P.VAL.pay_day())
        if day < self.last_day:
            self.reset()
        if day != self.last_day:
            self.repair_jobs.clear()
        # A dawn observation is authoritative for yesterday's successful
        # placement; retained history preserves plants later harvested/died.
        for d in range(max(0, self.last_day), day + 1):
            for crop in range(spec.N_CROPS):
                n = int(np.sum((np.asarray(view.kind) == spec.KIND_PLANT)
                               & (np.asarray(view.occ) == crop)
                               & (np.asarray(view.t_day) == d)))
                self.planted[d, crop] = max(int(self.planted[d, crop]), n)
        self.last_day = day

        row = np.asarray(PROGRAM_SEEDS[day], np.int32).copy()
        prior = np.zeros(spec.N_CROPS, np.int32)
        for start, end, goals in PROGRAM_PHASES:
            if start <= day <= end:
                done = self.planted[:day].sum(axis=0)
                expected = prior + np.asarray(PROGRAM_SEEDS[start:day + 1],
                                               np.int32).sum(axis=0)
                if start == 0 and day >= 2:
                    expected[spec.I_MELON] += 1  # chosen d2 allocation
                row = np.maximum(row, np.maximum(expected - done, 0))
                # Debt survives phase boundaries.  Each lane becomes due on
                # its last viable planting day, not an unusable phase end.
                cumulative = prior + np.asarray(goals, np.int32)
                for crop in range(spec.N_CROPS):
                    deadline = min(end, pay_day - int(spec.CROP_FIRST_YIELD_DAY[crop]))
                    if deadline < start:
                        continue
                    # Daily medians omit asynchronous carrot/tomato/berry
                    # purchases. Distribute that phase deficit while it can
                    # still grow, rather than dumping it on the final day.
                    scheduled = sum(r[crop] for r in PROGRAM_SEEDS[start:deadline + 1])
                    missing = max(0, goals[crop] - scheduled)
                    span = deadline - start + 1
                    due = (missing * min(day - start + 1, span) + span - 1) // span
                    row[crop] = max(0, min(expected[crop] + due,
                                          cumulative[crop]) - done[crop])
                    if day == deadline:
                        row[crop] = max(row[crop], cumulative[crop] - done[crop])
                break
            prior += np.asarray(goals, np.int32)
        # The chosen opening allocation is a deadline, not a competing switch.
        if day <= 2:
            # Q1 has 25 cells. Preserve the design's ten wheat; the common
            # grant decides which herd/seed obligations are jointly funded.
            row[:] = 0
            row[spec.I_WHEAT] = max(0, 10 - int(self.planted[:day, spec.I_WHEAT].sum()))
            row[spec.I_STRAWBERRY] = PROGRAM_SEEDS[day][spec.I_STRAWBERRY]
            d0 = min(max(int(P.PROGRAM_MELON_D0), 0), 11)
            opening = (d0, max(d0, 10), 11)[day]
            row[spec.I_MELON] = max(0, opening
                                    - int(self.planted[:day, spec.I_MELON].sum()))
        for crop in range(spec.N_CROPS):
            if day + int(spec.CROP_FIRST_YIELD_DAY[crop]) > pay_day:
                row[crop] = 0
        sheep, cow, goose = (PROGRAM_ANIMALS_REAL if P.PROGRAM_HERD_REAL else PROGRAM_ANIMALS)[day]
        # Planner/spec order is GOOSE/COW/SHEEP; the evidence table is S/C/G.
        herd = np.asarray((goose, cow, sheep), np.int32)
        next_h = PROGRAM_HANDS[min(day + 1, 29)]
        crew_reserve = int(P.HIRE_BILLS[min(next_h, spec.MAX_HANDS)])
        animal = ((np.asarray(view.kind) == spec.KIND_COOP)
                  | (np.asarray(view.kind) == spec.KIND_PASTURE)) & (np.asarray(view.occ) >= 0)
        actual_herd = np.asarray(
            [np.sum(animal & (np.asarray(view.occ) == a))
             for a in range(spec.N_ANIMALS)], np.int32)
        land_target = PROGRAM_LAND[day]
        for a in range(spec.N_ANIMALS):
            if day + int(spec.ANIMAL_FIRST_YIELD_DAY[a]) > pay_day:
                herd[a] = actual_herd[a]
        # ``animal_want`` is the shed-side placement/acquisition deficit, not
        # a cumulative herd target.  The planner separately subtracts animals
        # already waiting in the shed; subtract the standing herd here.
        herd = np.maximum(herd - actual_herd, 0).astype(np.int32)
        feed_units = int(np.sum(animal))
        feed_short = max(0, feed_units - int(view.shed[spec.I_WHEAT]))
        feed_reserve = feed_short * int(view.price[spec.I_WHEAT])
        # Unfunded target animals do not eat. Reserve for owned stock here;
        # the common grant reserves tomorrow's feed for each new acquisition.
        projected_feed = feed_units + int(np.asarray(view.shed)[spec.I_GOOSE:].sum())
        tomorrow_feed = projected_feed * int(view.price[spec.I_WHEAT])
        wanted_reserve = crew_reserve + tomorrow_feed
        current_hire = int(P.HIRE_BILLS[min(PROGRAM_HANDS[day], spec.MAX_HANDS)])
        current_melon = int(row[spec.I_MELON]) * int(
            spec.CROP_SEED_COST[spec.I_MELON])
        after_today = max(0, int(view.money) - current_hire
                          - feed_reserve - current_melon)
        reserve = min(wanted_reserve, after_today)
        deployable = max(0, int(view.money) - reserve)
        self.last_budget = {"purse": int(view.money), "reserve": reserve,
                            "crew": crew_reserve, "feed": feed_reserve,
                            "deployable": deployable}
        self.milestones[day] = {
            "animals": tuple(int(np.sum(animal & (np.asarray(view.occ) == a)))
                             for a in range(spec.N_ANIMALS)),
            "melon_planted": int(self.planted[:day + 1, spec.I_MELON].sum()),
            "quadrants": int(view.nquad), "hands_target": PROGRAM_HANDS[day],
            "cash": int(view.money), "melon_sell_requested": int(self.melon_sell_requested[day]),
        }
        self.intent = ProgramIntent(row, herd, PROGRAM_HANDS[day], land_target, reserve)
        return self.intent

    def record(self, day, action):
        # Request telemetry only; exact fills belong to the replay ledger.
        if 0 <= day < 30:
            self.melon_sell_requested[day] += sum(
                int(x[2]) for x in action.get("market", ())
                if len(x) >= 3 and x[0] == "SELL" and x[1] == "MELON")

    @staticmethod
    def repair_decay(obs, action, plan):
        """Keep funded harvest/replant chains executable after observed decay."""
        hour = int(obs['hour'])
        if hour >= spec.TURNS_PER_DAY - 1:
            return action
        farm = obs['farms'][int(obs.get('player', 0))]
        commands = [action['farmer'], *action['hands']]
        changed = False
        for u, (x, y) in enumerate([farm['farmer'], *farm['hands']]):
            tile = farm['tiles'][y][x]
            if (commands[u] == ['HARVEST'] and isinstance(tile, dict)
                    and tile.get('kind') == 'WEED'
                    and int(plan[0][u, hour + 1]) in
                        (P.O.OP_PLANT, P.O.OP_BUILD_COOP, P.O.OP_BUILD_PASTURE)):
                commands[u] = ['DIG']
                changed = True
        return (dict(action, farmer=commands[0], hands=commands[1:])
                if changed else action)

    def repair_sales(self, obs, action, plan):
        """Release deposited funding stock and ripe melon at observed depth."""
        day, hour = int(obs['day']), int(obs['hour'])
        products = (('WOOL', 'MILK', 'EGG', 'FERTILIZER') if day <= 9
                    else ('MELON',))
        market = list(action.get('market') or [])
        shed = obs['private']['shed']
        deposited = dict.fromkeys(spec.ITEMS, 0)
        room = max(0, spec.SHED_CAPACITY - sum(shed.values()))
        commands = [action['farmer'], *action['hands']]
        for command, bag in zip(commands, obs['private'].get('inventories', [])):
            if command != ['DROP']:
                continue
            for item, quantity in bag.items():
                if item not in deposited:
                    continue
                take = min(room, int(quantity))
                deposited[item] += take
                room -= take
        for product in products:
            item = spec.PRODUCTS.index(product)
            pickup = ((np.asarray(plan[0])[:, hour:] == P.O.OP_PICKUP)
                      & (np.asarray(plan[1])[:, hour:] == item))
            reserved = int(np.sum(np.where(pickup, np.asarray(plan[2])[:, hour:], 0)))
            available = max(0, int(shed.get(product, 0)) + deposited[product] - reserved)
            existing = next((i for i, o in enumerate(market) if o[:2] == ['SELL', product]), None)
            if existing is not None:
                market[existing] = ['SELL', product, max(int(market[existing][2]), available)]
                continue
            if not available:
                continue
            if len(market) < spec.MAX_MARKET_ORDERS:
                market.append(['SELL', product, available])
        return dict(action, market=market) if market != action.get('market', []) else action

    @staticmethod
    def owned_reserve(obs):
        farm = obs['farms'][int(obs.get('player', 0))]
        herd = sum(bool(t.get('animal')) for line in farm['tiles']
                   for t in line if isinstance(t, dict))
        shed = obs['private'].get('shed', {})
        herd += sum(int(bag.get(a, 0)) for bag in
                    [shed, *obs['private'].get('inventories', [])] for a in spec.ANIMALS)
        feed = max(0, herd - int(shed.get('WHEAT', 0)))
        return (int(P.HIRE_BILLS[PROGRAM_HANDS[min(int(obs['day']) + 1, 29)]])
                + feed * int(obs['market']['prices']['WHEAT']))

    def repair_hire(self, obs, action, plan):
        """Release a conditional crew slot when an actual fill funds its job."""
        day, hour = int(obs['day']), int(obs['hour'])
        farm = obs['farms'][int(obs.get('player', 0))]
        hired = len(farm['hands'])
        if (hour < 4 or self.intent is None or hired >= self.intent.hands_target
                or not np.all(np.asarray(plan[0])[hired + 1, hour:] == P.O.OP_PASS)):
            return action
        purchases = (P.O.MO_BUY_PRODUCT, P.O.MO_BUY_SEED, P.O.MO_BUY_ANIMAL,
                     P.O.MO_BUY_LAND, P.O.MO_HIRE)
        market = list(action.get('market') or [])
        if (np.isin(np.asarray(plan[3])[hour:], purchases).any()
                or len(market) >= spec.MAX_MARKET_ORDERS
                or any(o[0].startswith('BUY_') or o[0] == 'HIRE' for o in market)):
            return action
        planted = np.zeros(spec.N_CROPS, np.int32)
        for line in farm['tiles']:
            for tile in line:
                if (isinstance(tile, dict) and tile.get('kind') == 'PLANT'
                        and int(tile['planted_day']) == day):
                    planted[spec.CROPS.index(tile['crop'])] += 1
        remaining = np.asarray(plan[0])[:, hour:] == P.O.OP_PLANT
        owed = np.asarray(self.intent.plant_target) - planted - np.asarray([
            np.sum(remaining & (np.asarray(plan[1])[:, hour:] == c))
            for c in range(spec.N_CROPS)])
        free = sum(np.all(row[hour:] == P.O.OP_PASS)
                   for row in np.asarray(plan[0])[:hired + 1])
        if int(np.maximum(owed, 0).sum()) <= free:
            return action
        sx, sy = int(P.SPAWN_X[hired + 1]), int(P.SPAWN_Y[hired + 1])
        space = any(tile is None and abs(x-sx) + abs(y-sy) + 4 <= 24 - hour
                    for y, line in enumerate(farm['tiles']) for x, tile in enumerate(line))
        hire_cost = int(spec.HIRE_COST[hired])
        cash = int(farm['money']) - self.owned_reserve(obs)
        jobs = [c for c in range(spec.N_CROPS) if owed[c] > 0
                and day + int(spec.CROP_FIRST_YIELD_DAY[c]) <= int(P.VAL.pay_day())
                and cash >= hire_cost + int(spec.CROP_SEED_COST[c])
                and int(obs['market']['prices'][spec.CROPS[c]]) * int(spec.CROP_MAX_YIELD[c])
                    > hire_cost + int(spec.CROP_SEED_COST[c])]
        return dict(action, market=market + [['HIRE']]) if space and jobs else action

    def repair_land(self, obs, action, plan):
        """Fund an overdue quadrant after actual fills, for remaining work."""
        day, hour = int(obs['day']), int(obs['hour'])
        if hour <= P.O.SELL_TURNS[0] or day >= 26:
            return action
        seat = int(obs.get('player', 0))
        farm = obs['farms'][seat]
        quads = len(farm['unlocked_quadrants'])
        target = self.intent.land_target if self.intent is not None else PROGRAM_LAND[day]
        if quads >= target:
            return action
        # A cached future purchase already owns its money. Only repair an
        # otherwise completed purchase suffix, with space in this market row.
        purchase_ops = (P.O.MO_BUY_PRODUCT, P.O.MO_BUY_SEED,
                        P.O.MO_BUY_ANIMAL, P.O.MO_BUY_LAND, P.O.MO_HIRE)
        if np.isin(np.asarray(plan[3])[hour:], purchase_ops).any():
            return action
        market = list(action.get('market') or [])
        if any(order[0].startswith('BUY_') or order[0] == 'HIRE' for order in market):
            return action
        if len(market) >= spec.MAX_MARKET_ORDERS:
            return action
        reserve = self.owned_reserve(obs)
        cost = int(spec.LAND_PRICES[quads - 1])
        if int(farm['money']) >= cost + reserve:
            market.append(['BUY_LAND'])
            return dict(action, market=market)
        return action

    def repair_herd(self, obs, action, plan):
        """PROGFIX2 (1): buy the programme herd deficit mid-day, once the
        day's sales (and a repaired quadrant) have landed. The dawn grant sees
        only the dawn purse and dawn tiles, so land bought by `repair_land`
        stood empty and the ENGINE's d6 cows arrived d10-11."""
        day, hour = int(obs['day']), int(obs['hour'])
        if (not P.PROGRAM_HERD_MIDDAY or self.intent is None
                or hour <= P.O.SELL_TURNS[0] or hour >= spec.TURNS_PER_DAY - 2
                or day < 1 or day > P.PROGRAM_HERD_LAST_DAY):
            return action
        purchase_ops = (P.O.MO_BUY_PRODUCT, P.O.MO_BUY_SEED,
                        P.O.MO_BUY_ANIMAL, P.O.MO_BUY_LAND, P.O.MO_HIRE)
        if np.isin(np.asarray(plan[3])[hour:], purchase_ops).any():
            return action
        market = list(action.get('market') or [])
        if any(o[0].startswith('BUY_') or o[0] == 'HIRE' for o in market):
            return action
        farm = obs['farms'][int(obs.get('player', 0))]
        shed = obs['private'].get('shed', {})
        bags = [shed, *obs['private'].get('inventories', [])]
        owned = {a: sum(int(b.get(a, 0)) for b in bags) for a in spec.ANIMALS}
        waiting = sum(owned.values())
        free = 0
        for line in farm['tiles']:
            for tile in line:
                if tile is None:
                    free += 1
                elif isinstance(tile, dict) and tile.get('animal') in owned:
                    owned[tile['animal']] += 1
        sheep, cow, goose = (PROGRAM_ANIMALS_REAL if P.PROGRAM_HERD_REAL
                             else PROGRAM_ANIMALS)[day]
        target = {'SHEEP': sheep, 'COW': cow, 'GOOSE': goose}
        wheat = int(obs['market']['prices']['WHEAT'])
        cash = int(farm['money']) - self.owned_reserve(obs)
        if P.PROGRAM_HERD_MIDDAY_SEEDFIRST:
            # Today's still-owed plantings keep their seed money: the ENGINE
            # plants its d6 strawberry AND buys the herd; buying the herd
            # first moved 6 strawberry plantings from d6 to d11.
            planted = np.zeros(spec.N_CROPS, np.int32)
            for line in farm['tiles']:
                for tile in line:
                    if (isinstance(tile, dict) and tile.get('kind') == 'PLANT'
                            and int(tile['planted_day']) == day):
                        planted[spec.CROPS.index(tile['crop'])] += 1
            pending = np.asarray([np.sum((np.asarray(plan[0])[:, hour:] == P.O.OP_PLANT)
                                         & (np.asarray(plan[1])[:, hour:] == c))
                                  for c in range(spec.N_CROPS)])
            seeds = np.asarray([obs['private'].get('seeds', {}).get(c, 0)
                                for c in spec.CROPS], np.int32)
            owed = np.maximum(np.asarray(self.intent.plant_target) - planted
                              - np.maximum(pending, seeds), 0)
            cash -= int(np.sum(owed * np.asarray(spec.CROP_SEED_COST)))
        room = free - waiting
        for name in ('SHEEP', 'COW', 'GOOSE'):   # the grant's rank order
            a = spec.ANIMALS.index(name)
            if day + int(spec.ANIMAL_FIRST_YIELD_DAY[a]) > int(P.VAL.pay_day()):
                continue
            cost = int(spec.ANIMAL_COST[a]) + wheat
            n = min(max(target[name] - owned[name], 0), room,
                    max(cash, 0) // cost)
            if n <= 0 or len(market) >= spec.MAX_MARKET_ORDERS:
                continue
            market.append(['BUY_ANIMAL', name, int(n)])
            cash -= n * cost
            room -= n
        return dict(action, market=market) if market != action.get('market', []) else action

    def repair_work(self, obs, action, plan):
        """Repair only finished unit suffixes, using unclaimed observed work."""
        day, hour = int(obs['day']), int(obs['hour'])
        if hour < 3 or day >= 29:
            return action
        farm = obs['farms'][int(obs.get('player', 0))]
        positions = [farm['farmer'], *farm['hands']]
        commands = [action['farmer'], *action['hands']]
        free = [u for u in range(len(positions))
                if commands[u] == ['PASS']
                and np.all(np.asarray(plan[0])[u, hour:] == P.O.OP_PASS)]
        if not free:
            return action
        moves = {P.O.OP_NORTH: (0, -1), P.O.OP_SOUTH: (0, 1),
                 P.O.OP_WEST: (-1, 0), P.O.OP_EAST: (1, 0)}
        names = {(0, -1): 'NORTH', (0, 1): 'SOUTH',
                 (-1, 0): 'WEST', (1, 0): 'EAST'}
        # Preserve every task still owned by a cached route. In particular,
        # never steal the harvest that funds another unit's deposit/sale.
        claimed = set()
        passive = (P.O.OP_PASS, P.O.OP_PICKUP, P.O.OP_DROP)
        for u, position in enumerate(positions):
            x, y = map(int, position)
            for op in np.asarray(plan[0])[u, hour:]:
                if int(op) in moves:
                    dx, dy = moves[int(op)]
                    x, y = x + dx, y + dy
                elif int(op) not in passive:
                    claimed.add((x, y))
        inventories = obs['private'].get('inventories', [])
        funding_in_transit = (day <= 9 and any(
            bag.get(p, 0) > 0 for bag in inventories
            for p in ('FERTILIZER', 'MILK', 'WOOL', 'EGG')))
        # Reinvestment may become funded only after a sale. Reserve the
        # untouched cached suffix, then admit a complete plant/water job.
        market = list(action.get('market') or [])
        seeds = np.asarray([obs['private'].get('seeds', {}).get(c, 0)
                            for c in spec.CROPS], np.int32)
        future_plants = np.asarray(plan[0])[:, hour:] == P.O.OP_PLANT
        future_crop = np.asarray(plan[1])[:, hour:]
        pending = np.asarray([np.sum(future_plants & (future_crop == c))
                              for c in range(spec.N_CROPS)])
        planted = np.zeros(spec.N_CROPS, np.int32)
        for line in farm['tiles']:
            for tile in line:
                if (isinstance(tile, dict) and tile.get('kind') == 'PLANT'
                        and int(tile['planted_day']) == day):
                    planted[spec.CROPS.index(tile['crop'])] += 1
        owed = (np.maximum(np.asarray(self.intent.plant_target) - planted - pending, 0)
                if self.intent is not None else np.zeros(spec.N_CROPS, np.int32))
        seeds = np.maximum(seeds - pending, 0)
        shed = obs['private'].get('shed', {})
        reserve = max(self.last_budget.get('reserve', 0), self.owned_reserve(obs))
        cash = max(0, int(farm['money']) - reserve)
        purchases = (P.O.MO_BUY_PRODUCT, P.O.MO_BUY_SEED, P.O.MO_BUY_ANIMAL,
                     P.O.MO_BUY_LAND, P.O.MO_HIRE)
        can_buy = (not np.isin(np.asarray(plan[3])[hour:], purchases).any()
                   and not any(o[0].startswith('BUY_') or o[0] == 'HIRE' for o in market))
        feed_pickups = ((np.asarray(plan[0])[:, hour:] == P.O.OP_PICKUP)
                        & (np.asarray(plan[1])[:, hour:] == spec.I_WHEAT))
        feed_stock = max(0, int(shed.get('WHEAT', 0)) - int(np.sum(
            np.where(feed_pickups, np.asarray(plan[2])[:, hour:], 0))))
        tasks = []
        for y, line in enumerate(farm['tiles']):
            for x, tile in enumerate(line):
                if not isinstance(tile, dict) or (x, y) in claimed:
                    continue
                command, priority = None, 0
                if tile.get('kind') == 'PLANT':
                    crop = spec.CROPS.index(tile['crop'])
                    age = day - int(tile['planted_day'])
                    if day - age + int(spec.CROP_FIRST_YIELD_DAY[crop]) > int(P.VAL.pay_day()):
                        continue
                    bonus = (not spec.CROP_ONGOING[crop]
                             and int(spec.CROP_WINDOW_START[crop]) <= age <= int(spec.CROP_MAX_YIELD_DAY[crop])
                             and int(tile.get('yield_units', 0)) < int(spec.CROP_MAX_YIELD[crop]))
                    if (not tile.get('watered_today')
                            and (tile.get('consecutive_unwatered', 0) >= 1 or bonus)):
                        command = ['WATER']
                        priority = 4
                elif tile.get('animal'):
                    if (day < 27 and not tile.get('fed_today')
                            and tile.get('consecutive_unfed', 0) >= 1):
                        command, priority = ['FEED'], 4
                if command:
                    tasks.append((priority, x, y, command))
        used = set()
        changed = False
        for u in free:
            x, y = map(int, positions[u])
            bag = inventories[u] if u < len(inventories) else {}
            access = min((abs(int(ax)-x) + abs(int(ay)-y), int(ax), int(ay))
                         for ax, ay in spec.SHED_ACCESS_XY)
            feed_fetch = (day <= 9 and (feed_stock > 0 or (can_buy and
                          cash > int(obs['market']['prices']['WHEAT']))))
            feasible = [( -priority, abs(tx-x) + abs(ty-y), ty, tx, cmd)
                        for priority, tx, ty, cmd in tasks
                        if (tx, ty) not in used
                        and abs(tx-x) + abs(ty-y) + 1 <= 24 - hour
                        and (cmd != ['FEED'] or bag.get('WHEAT', 0) > 0
                             or (feed_fetch and access[0] + abs(tx-access[1])
                                 + abs(ty-access[2]) + 3 <= 24 - hour))]
            job = self.repair_jobs.get(u)
            if job is not None:
                tx, ty, c = job
                tile = farm['tiles'][ty][tx]
                if isinstance(tile, dict) and tile.get('kind') == 'PLANT':
                    if tile.get('crop') == spec.CROPS[c] and not tile.get('watered_today'):
                        cmd = ['WATER']
                    else:
                        self.repair_jobs.pop(u)
                        job = None
                elif tile is None:
                    cmd = ['PLANT', spec.CROPS[c]] if seeds[c] > 0 else ['PASS']
                    if (seeds[c] <= 0 and can_buy and cash >= int(spec.CROP_SEED_COST[c])
                            and len(market) < spec.MAX_MARKET_ORDERS):
                        market.append(['BUY_SEED', spec.CROPS[c], 1])
                        cash -= int(spec.CROP_SEED_COST[c])
                else:
                    self.repair_jobs.pop(u)
                    job = None
            if job is None and feasible:
                _, distance, ty, tx, cmd = min(feasible)
            elif job is None:
                reserved_tiles = {(j[0], j[1]) for j in self.repair_jobs.values()}
                vacant = [(abs(tx-x) + abs(ty-y), ty, tx)
                          for ty, line in enumerate(farm['tiles'])
                          for tx, tile in enumerate(line)
                          if tile is None and (tx, ty) not in claimed | used | reserved_tiles
                          and abs(tx-x) + abs(ty-y) + 2 + int(tx == x and ty == y) <= 24 - hour]
                crops = [c for c in range(spec.N_CROPS)
                         if owed[c] > sum(j[2] == c and farm['tiles'][j[1]][j[0]] is None
                                          for j in self.repair_jobs.values())
                         and day + int(spec.CROP_FIRST_YIELD_DAY[c]) <= int(P.VAL.pay_day())
                         and (seeds[c] > 0 or funding_in_transit
                              or (can_buy and cash >= int(spec.CROP_SEED_COST[c])))
                         and (day <= 9 or int(obs['market']['prices'][spec.CROPS[c]])
                              * int(spec.CROP_MAX_YIELD[c]) > int(spec.CROP_SEED_COST[c]))]
                if not vacant or not crops:
                    continue
                _, ty, tx = min(vacant)
                c = min(crops, key=lambda c: (-int(spec.CROP_FIRST_YIELD_DAY[c]), c))
                if seeds[c] <= 0:
                    if (can_buy and cash >= int(spec.CROP_SEED_COST[c])
                            and len(market) < spec.MAX_MARKET_ORDERS):
                        market.append(['BUY_SEED', spec.CROPS[c], 1])
                        cash -= int(spec.CROP_SEED_COST[c])
                    cmd = ['PASS']
                else:
                    cmd = ['PLANT', spec.CROPS[c]]
                self.repair_jobs[u] = (tx, ty, c)
            if u in self.repair_jobs and farm['tiles'][ty][tx] is None and seeds[c] > 0:
                seeds[c] -= 1  # reserve the seed while its owner walks
            distance = abs(tx-x) + abs(ty-y)
            used.add((tx, ty))
            if cmd == ['FEED'] and bag.get('WHEAT', 0) <= 0:
                _, tx, ty = access
                distance = abs(tx-x) + abs(ty-y)
                if feed_stock > 0:
                    cmd = ['PICKUP', 'WHEAT', 1]
                    feed_stock -= 1
                elif len(market) < spec.MAX_MARKET_ORDERS:
                    market.append(['BUY_PRODUCT', 'WHEAT', 1])
                    cash -= int(obs['market']['prices']['WHEAT']) + 1
                    cmd = ['PASS']
                else:
                    continue
            if distance:
                options = []
                if tx != x:
                    options.append((1 if tx > x else -1, 0))
                if ty != y:
                    options.append((0, 1 if ty > y else -1))
                step = next(((dx, dy) for dx, dy in options
                             if 0 <= x + dx < spec.BOARD and 0 <= y + dy < spec.BOARD), None)
                if step is None:
                    continue
                cmd = [names[step]]
            commands[u] = cmd
            changed = True
        return (dict(action, farmer=commands[0], hands=commands[1:], market=market)
                if changed else action)


class Runtime:
    def __init__(self, macro_fn, pass_prev_mkt_inv=False):
        """Cache one plan per day and, when requested, its dawn history.

        Legacy macros take ``(obs, player, view)``.  A momentum-aware macro is
        an explicit opt-in and takes a fourth argument: the previous dawn's
        market inventory in the nine-product order returned by ``parse_market``.
        Its first observed dawn receives the current inventory, hence a zero
        delta.  Keeping the opt-in here avoids signature inspection and leaves
        every existing three-argument caller on its old call path.
        """
        self.macro_fn = macro_fn
        self.pass_prev_mkt_inv = bool(pass_prev_mkt_inv)
        self.plan = None
        self.day = -1
        self.prev_mkt_inv = None
        self.dawn_mkt_inv = None
        # [SWITCH, RIVAL_TELL] the per-turn rival-sale history; built on the
        # first armed turn so a switch set after import still takes.
        self.tell = None
        self.overflow_pending = []
        # [SWITCH, ENGINE_GATE] the per-game rival-class latch.
        self.opp_engine = False
        self.gate_decided = False
        self.program_engine = ProgramEngineState() if P.PROGRAM_ENGINE_ON else None
        # [SWITCH, KERNEL2] per-game kernel latch: None = undecided, "v56" or "pfs"; `k2_fn` = the V56 callable.
        self.k2_mode = None
        self.k2_fn = None

    def _kernel2(self, obs, config):
        """[SWITCH, KERNEL2] the V56 kernel's action, the step-0 no-op, or None (PFS plays this turn)."""
        import copy
        day = int(obs.get("day", 0) or 0)
        step = day * spec.TURNS_PER_DAY + int(obs.get("hour", 0) or 0)
        if step == 0:                               # new game: reset the latch, no-op on every seat
            self.k2_mode = None
            self.k2_buf = None
            self.k2_inh = None
            if not P.KERNEL2_NOOP_H0:               # [SWITCH, MELONHYBRID4] PFS plays its real h0 (master)
                self.k2_fn = kernel2_load() if P.KERNEL2_PRELOAD else None
                return None
            if P.KERNEL2_PFS_H0MERGE:               # [SWITCH, PFSH0MERGE1] PFS plays its master h0 into a buffer
                self.k2_buf = copy.deepcopy(self._pfs_act(obs))
            self.k2_fn = kernel2_load() if P.KERNEL2_PRELOAD else None
            return copy.deepcopy(KERNEL2_NOOP)
        if self.k2_mode is None:                    # first turn after the no-op: latch on the rival's cash
            p = int(obs.get("player", 0) or 0)
            cash = int(obs["farms"][1 - p]["money"])
            if str(P.KERNEL2_FIRE_CASH):            # [SWITCH, KERNEL2FIRE1] h1 exact-cash whitelist (CASH_MAX/ZERO_CASH ignored)
                self.k2_mode = "v56" if cash in kernel2_cash_list(P.KERNEL2_FIRE_CASH) else "pfs"
            else:
                self.k2_mode = "v56" if cash <= int(P.KERNEL2_CASH_MAX) else "pfs"
                if (self.k2_mode == "v56" and str(P.KERNEL2_ZERO_CASH)
                        and cash in kernel2_cash_list(P.KERNEL2_ZERO_CASH)):
                    self.k2_mode = "pfs"            # [SWITCH, ZEROGATE1] h1 exact-cash ZERO exclusion
            if self.k2_mode != "v56":
                self.k2_fn = None
            else:
                self.k2_buf = None                  # [SWITCH, PFSH0MERGE1] V56 seat: the PFS h0 buffer is dropped
            self.k2_back_checked = False
        if (self.k2_mode == "v56" and P.KERNEL2_ZERO_BACK and step >= spec.TURNS_PER_DAY
                and not getattr(self, "k2_back_checked", False)):
            # [SWITCH, ZEROGATE1] d1-dawn switch-back: the rival shows 0 MELON and a full opening field at our
            # first d1 turn = ZERO family; PFS takes the farm for the rest of the game (fresh per-game state).
            self.k2_back_checked = True
            if kernel2_zero_rival(obs):
                self.k2_mode = "back"
                self.k2_fn = None
                self.vrp_saved = 0
                self.vrp_fill = {}
        if self.k2_mode == "v56" and int(P.KERNEL2_HANDBACK_DAY) > 0:
            # [SWITCH, HANDBACK1] at the dawn of day KERNEL2_HANDBACK_DAY the farm V56 built goes back to PFS's planner
            # (fresh VRP bank + fill ledger, as ZERO_BACK); before it, every kernel dawn records the market inventory so
            # PFS's first dawn reads the previous dawn's draw (brain.market_momentum), not a d0-to-dD one.
            if step >= int(P.KERNEL2_HANDBACK_DAY) * spec.TURNS_PER_DAY:
                self.k2_mode = "back"
                self.k2_fn = None
                self.vrp_saved = 0
                self.vrp_fill = {}
                self.k2_back_day = day
                return None
            if int(obs.get("hour", 0) or 0) == 0 and day >= 1 and self.pass_prev_mkt_inv:
                self.prev_mkt_inv = self.dawn_mkt_inv
                self.dawn_mkt_inv = np.asarray(parse.parse_market(obs)[0]).copy()
        if self.k2_mode != "v56":
            return None
        if self.k2_fn is None:
            self.k2_fn = kernel2_load()
        if not P.KERNEL2_NOOP_H0:                   # [SWITCH, MELONHYBRID4] the kernel takes the farm PFS's h0 built
            if P.KERNEL2_INHERIT and step == 1:
                return self._k2_inherit(obs, config)
            return self.k2_fn(obs, config)
        if P.KERNEL2_H0_MERGE and int(obs.get("step", 0) or 0) == 1:
            # The kernel's h0 row (feed-wheat pump + 1 wheat seed) never played at our no-op step 0: show
            # it the h1 obs relabelled step 0 / hour 0 first, then the real step 1, and play the h0 market
            # rows ahead of the h1 ones (cap 10); farmer and hands from the h1 call (MELONHYBRID3 v56h1m).
            o0 = copy.deepcopy(obs)
            o0["step"] = 0
            o0["hour"] = 0
            a0 = self.k2_fn(o0, config)
            a1 = dict(self.k2_fn(obs, config))
            a1["market"] = (list(a0.get("market") or []) + list(a1.get("market") or []))[:10]
            return a1
        return self.k2_fn(obs, config)

    def _k2_inherit(self, obs, config):
        """[SWITCH, MELONHYBRID4 KERNEL2_INHERIT] the V56 kernel's step-1 turn on the farm PFS's real h0 built.

        The kernel is shown its own world: first the h1 obs relabelled step 0 / hour 0 with our farm virgin (its h0 row), then
        the real step-1 obs with our farm as its h0 row would have left it (holding = its h0 net product buys, its h0 seeds,
        no hands, farmer on the spawn tile, cash = ours + the sale of the excess - its seeds).  Its two rows are rewritten onto
        the inherited farm: SELL every product above the kernel's holding (BUY the shortfall), its h0 seed rows, its h1 seed
        and animal rows, HIRE (kernel hands - our hands), in that order and clipped to the projected cash; the farmer is moved
        to the kernel's h2 tile (PASS if already there), the hands PASS.  Record in `self.k2_inh`."""
        import copy
        p = int(obs.get("player", 0) or 0)
        f = obs["farms"][p]
        priv = obs.get("private") or {}
        shed = dict(priv.get("shed") or {})
        seeds = dict(priv.get("seeds") or {})
        inv = dict(obs["market"]["inventory"])
        start = [int(spec.SHED_ACCESS_XY[0][0]), int(spec.SHED_ACCESS_XY[0][1])]
        prods = [k for k in shed if k in spec.PRODUCTS]

        def world(o, money, hold, sd):
            o = copy.deepcopy(o)
            fa = dict(o["farms"][p], money=float(money), farmer=list(start), hands=[], hires_today=0)
            farms = list(o["farms"]); farms[p] = fa; o["farms"] = farms
            pr = dict(o.get("private") or {})
            pr["shed"] = {k: int(hold.get(k, 0)) for k in shed}
            pr["seeds"] = {k: int(sd.get(k, 0)) for k in seeds}
            pr["inventories"] = [{}]
            o["private"] = pr
            return o

        o0 = world(obs, spec.STARTING_MONEY, {}, {})
        o0["step"] = 0
        o0["hour"] = 0
        a0 = self.k2_fn(o0, config)
        hold, sd0, extra0 = {}, {}, []
        for m in a0.get("market") or []:
            if m and m[0] == "BUY_PRODUCT":
                hold[m[1]] = hold.get(m[1], 0) + int(m[2])
            elif m and m[0] == "SELL":
                hold[m[1]] = hold.get(m[1], 0) - int(m[2])
            elif m and m[0] == "BUY_SEED":
                sd0[m[1]] = sd0.get(m[1], 0) + int(m[2])
            elif m:
                extra0.append(list(m))              # (none on the V56 kernel: its h0 row is the wheat pump + 1 seed)
        hold = {k: max(0, v) for k, v in hold.items()}
        # projected cash: sell the excess down the book (engine per-unit quote), buy the shortfall, pay the h0 seeds
        cash = float(f["money"])
        sells, buys = [], []
        for k in prods:
            d = int(shed.get(k, 0)) - int(hold.get(k, 0))
            if d > 0:
                sells.append(["SELL", k, d])
                for _ in range(d):
                    px = spec.market_price(k, inv[k])
                    cash += px
                    if px > 1:
                        inv[k] += 1
            elif d < 0 and k in ("WHEAT", "FERTILIZER"):
                buys.append(["BUY_PRODUCT", k, -d])
                for _ in range(-d):
                    cash -= spec.market_price(k, inv[k] - 1)
                    inv[k] -= 1
        seed_cost = {c: int(spec.CROP_SEED_COST[spec.CROPS.index(c)]) for c in spec.CROPS}
        need0 = {c: max(0, q - int(seeds.get(c, 0))) for c, q in sd0.items()}
        v_money = cash - sum(seed_cost.get(c, 0) * q for c, q in need0.items())
        o1 = world(obs, v_money, hold, {c: int(seeds.get(c, 0)) + need0[c] for c in sd0} | {c: int(seeds.get(c, 0)) for c in seeds if c not in sd0})
        a1 = self.k2_fn(o1, config)
        m1 = [list(m) for m in (a1.get("market") or []) if m]
        seed_rows = [["BUY_SEED", c, q] for c, q in need0.items() if q > 0] + [m for m in m1 if m[0] == "BUY_SEED"]
        animal_rows = [m for m in m1 if m[0] == "BUY_ANIMAL"]
        n_hire = sum(1 for m in (a0.get("market") or []) + m1 if m and m[0] == "HIRE")
        n_hire = max(0, n_hire - len(f["hands"]))
        other = extra0 + [m for m in m1 if m[0] not in ("BUY_SEED", "BUY_ANIMAL", "HIRE")]
        # clip to the projected cash, in order: seeds, animals, hires
        out, dropped = sells + buys, []
        for m in seed_rows + animal_rows:
            unit = (seed_cost.get(m[1], 0) if m[0] == "BUY_SEED"
                    else int(spec.ANIMAL_COST[spec.ANIMALS.index(m[1])]) if m[1] in spec.ANIMALS else 0)
            q = int(m[2]) if unit <= 0 else min(int(m[2]), int(max(0.0, cash) // unit))
            if q > 0:
                out.append([m[0], m[1], q])
                cash -= unit * q
            if q < int(m[2]):
                dropped.append([m[0], m[1], int(m[2]) - q])
        hired = int(f.get("hires_today", 0) or 0)
        for _ in range(n_hire):
            c = int(spec.HIRE_COST[min(hired, spec.MAX_HANDS)])
            if cash < c:
                dropped.append(["HIRE"])
                continue
            out.append(["HIRE"])
            cash -= c
            hired += 1
        out = (out + other)[:spec.MAX_MARKET_ORDERS]
        # farmer: the kernel's h2 tile = spawn tile + its h1 move
        mv = {"NORTH": (0, -1), "SOUTH": (0, 1), "WEST": (-1, 0), "EAST": (1, 0)}
        fc = list(a1.get("farmer") or ["PASS"])
        d = mv.get(fc[0]) if fc else None
        tgt = [start[0] + d[0], start[1] + d[1]] if d else list(start)
        pos = [int(f["farmer"][0]), int(f["farmer"][1])]
        if pos == tgt:
            farmer = ["PASS"]
        elif abs(pos[0] - tgt[0]) + abs(pos[1] - tgt[1]) == 1:
            farmer = [next(k for k, v in mv.items() if (pos[0] + v[0], pos[1] + v[1]) == tuple(tgt))]
        else:
            farmer = fc if pos == start else ["PASS"]
        self.k2_inh = {"a0": a0.get("market"), "a1": a1, "v_money": v_money, "cash_left": cash, "market": out,
                       "dropped": dropped, "farmer": farmer, "pos": pos, "tgt": tgt}
        return {"farmer": farmer, "hands": [["PASS"] for _ in f["hands"]], "market": out}

    def _h0merge(self, obs):
        """[SWITCH, PFSH0MERGE1] PFS's d0 turn h >= 1 on a seat whose h0 was the KERNEL2 no-op.

        PFS runs unshifted on the real obs (its plan was built at step 0 on the real h0 obs, as master), so the
        market row is the plan's row h, on time; at step 1 the buffered h0 market rows go first (cap 10; orders past
        the cap are carried, in order, ahead of the next turn's rows: PFS's h1 row can hold 6 orders).  Each
        unit replays its plan rows from `k2_next[u]`: the farmer (its row 0 not played at step 0) and the hands
        hired by the h0 row (they spawn at the end of step 1, one hour late) start one row behind; a lagging
        unit whose next row is PASS skips it and is back on schedule (the master unit idled that hour)."""
        hour = int(obs.get("hour", 0) or 0)
        a = self._pfs_act(obs)
        buf = self.k2_buf or {"market": []}
        if hour == 1:
            n0 = sum(1 for m in (buf.get("market") or []) if m and m[0] == "HIRE")
            self.k2_next = [0] + [1] * n0           # next plan row per unit (farmer, then the h0 hires)
            self.k2_spill = list(buf.get("market") or [])
        mkt = list(getattr(self, "k2_spill", None) or []) + list(a.get("market") or [])
        a = dict(a, market=mkt[:spec.MAX_MARKET_ORDERS])
        self.k2_spill = mkt[spec.MAX_MARKET_ORDERS:]  # orders past the cap ride the next turn, in order
        unit_op, unit_a, unit_q = self.plan[0], self.plan[1], self.plan[2]
        units = [a["farmer"]] + list(a["hands"])
        for u in range(len(units)):
            if u >= len(self.k2_next) or self.k2_next[u] >= hour:
                continue                            # on schedule (or hired on time): PFS's own row h stands
            r = self.k2_next[u]
            if r < hour and int(unit_op[u, r]) == P.O.OP_PASS:
                r = hour                            # skip the lagging unit's idle row: back on schedule
            units[u] = render.unit_action(unit_op[u, r], unit_a[u, r], unit_q[u, r]) if r < hour else units[u]
            self.k2_next[u] = r + 1
        return dict(a, farmer=units[0], hands=units[1:])

    def _opp_family(self, obs):
        """[SWITCH, RIVALSUPPLY2] per-turn rival-family latch for the family supply curve (plan.OPP_SUPPLY_FAMILY_ON)."""
        day = int(obs.get("day", 0) or 0)
        step = day * spec.TURNS_PER_DAY + int(obs.get("hour", 0) or 0)
        rival = obs["farms"][1 - int(obs.get("player", 0) or 0)]
        if step == 0:
            self.opp_code = None
            fam = None
        else:
            if getattr(self, "opp_code", None) is None:
                self.opp_code = P.opp_supply_code(int(rival["money"]))
            fam = P.opp_supply_family(self.opp_code, day, len(rival.get("unlocked_quadrants") or ["NW"]))
        P.PJ.set_opp_family(fam)
        if FAMDIAG and step % spec.TURNS_PER_DAY == 0:
            crops = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
            own = obs["farms"][int(obs.get("player", 0) or 0)]
            tiles = lambda f: [sum(1 for row in f.get("tiles") or [] for t in row
                                   if isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") == c) for c in crops]
            inv = np.asarray(parse.parse_market(obs)[0]).astype(int).tolist()
            with open(FAMDIAG, "a") as fh:
                fh.write("\t".join(str(x) for x in (day, self.opp_code, fam, int(rival["money"]),
                                                     len(rival.get("unlocked_quadrants") or ["NW"]),
                                                     "|".join(map(str, inv)), "|".join(map(str, tiles(own))),
                                                     "|".join(map(str, tiles(rival))), int(own["money"]))) + "\n")

    def act(self, obs, config=None):
        if FAMDIAG:                                 # [SWITCH, RIVALSUPPLY2] env diag: per-turn wall time, one row per day
            import time as _time
            _t0 = _time.time()
            out = self._act(obs, config)
            h = int(obs.get("hour", 0) or 0)
            if h == 0:
                self.famdiag_t = []
            self.famdiag_t = getattr(self, "famdiag_t", []) + [round(_time.time() - _t0, 4)]
            if h == spec.TURNS_PER_DAY - 1:
                with open(FAMDIAG, "a") as fh:
                    fh.write("T\t" + str(int(obs.get("day", 0) or 0)) + "\t" + "|".join(map(str, self.famdiag_t)) + "\n")
            return out
        return self._act(obs, config)

    def _act(self, obs, config=None):
        if P.OPP_SUPPLY_FAMILY_ON or FAMDIAG:       # [SWITCH, RIVALSUPPLY2] the rival-family supply curve latch (+ env diag)
            self._opp_family(obs)
        if P.KERNEL2_ON:                            # [SWITCH, KERNEL2] V56PACK1 two-kernel runtime
            k2 = self._kernel2(obs, config)
            if k2 is not None:
                return k2
            h = int(obs.get("hour", 0) or 0)
            if P.KERNEL2_PFS_H0MERGE and getattr(self, "k2_buf", None) is not None:
                if int(obs.get("day", 0) or 0) == 0 and h >= 1:
                    return self._h0merge(obs)
            elif P.KERNEL2_NOOP_H0 and P.KERNEL2_PFS_SHIFT and int(obs.get("day", 0) or 0) == 0 and h >= 1:
                # PFS resumes at our h1 on a virgin farm: its d0 plan is built at h1 as its 'dawn' and
                # played one hour late (plan row h-1 at hour h; d0 row 23 is lost), from d1 h0 unchanged.
                # The d1-dawn switch back from V56 to PFS (rival 0 MELON at d1 h0 = ZERO family) is
                # `KERNEL2_ZERO_BACK` in `_kernel2` above (ZEROGATE1); PFS then runs unshifted from d1 h0.
                import copy
                obs = copy.copy(obs)
                obs["hour"] = h - 1
                if "step" in obs:
                    obs["step"] = int(obs["step"]) - 1
        return self._pfs_act(obs)

    def _pfs_act(self, obs):
        """The PFS (master) turn."""
        player = obs.get("player", 0)
        day = int(obs.get("day", 0))
        hour = int(obs.get("hour", 0))
        if P.ROUTE_VRP_ON:                          # [SWITCH, ROUTEOPT1] banked hire saving, hidden from the plan
            if int(obs.get("step", day * spec.TURNS_PER_DAY + hour)) == 0:
                self.vrp_saved = 0
                self.vrp_fill = {}                  # [ROUTEFILL1] per-game fill ledger
            if P.ROUTE_VRP_SHADOW_ON and getattr(self, "vrp_saved", 0):
                obs = dict(obs)
                farms = list(obs["farms"])
                farms[player] = dict(farms[player], money=farms[player]["money"] - self.vrp_saved)
                obs["farms"] = farms
        farm = obs["farms"][player]
        if (self.program_engine is not None
                and int(obs.get("step", day * spec.TURNS_PER_DAY + hour)) == 0
                and self.day >= 0):
            self.program_engine.reset()

        # The turn-time half of the rival-sale tell [SWITCH, RIVAL_TELL]: the
        # pot THIS turn opens on is what closes the previous turn's estimate
        # (`agent/tell.py` has the identity), so the history is rotated on
        # every turn and read at the one the day's plan is built on. Off, this
        # is a Python `and` and the market is not parsed.
        # [SWITCH, ENGINE_GATE] latch once at the dawn of ENGINE_GATE_DAY;
        # before it the base program runs, so a new game resets the latch.
        if P.ENGINE_GATE_ON:
            if day < P.ENGINE_GATE_DAY:
                self.opp_engine = False
                self.gate_decided = False
            elif not self.gate_decided:
                self.opp_engine = P.engine_gate_fires(obs, player)
                self.gate_decided = True
            P.engine_gate_apply(self.opp_engine)

        tell_rate = tell_burst = None
        if P.SELL_SLOT_PRIORITY_ON and (P.RIVAL_TELL_ON
                                        or P.SELL_SLOT_RIVALRANK_ON):
            if self.tell is None:
                self.tell = tell.RivalTell()
            self.tell.observe(int(obs.get("step", day * spec.TURNS_PER_DAY + hour)),
                              parse.parse_market(obs)[0], parse.parse_town(obs))
            if P.RIVAL_TELL_ON:
                tell_rate = self.tell.batch()
            # [SWITCH, SELL_SLOT_RIVALRANK] the same history read as a BURST.
            if P.SELL_SLOT_RIVALRANK_ON:
                tell_burst = self.tell.burst()

        if hour == 0 or self.plan is None or day != self.day:
            view = parse.parse_view(obs, player, opp_rate=tell_rate,
                                    opp_burst=tell_burst)
            if self.pass_prev_mkt_inv:
                current = np.asarray(parse.parse_market(obs)[0]).copy()
                # Rotate exactly once per new day.  The engine normally calls
                # hour zero once, but keeping this separate from the rebuild
                # condition makes repeated hour-zero calls history-safe.
                if self.dawn_mkt_inv is None:
                    self.prev_mkt_inv = current.copy()
                    self.dawn_mkt_inv = current
                elif day != self.day:
                    self.prev_mkt_inv = self.dawn_mkt_inv
                    self.dawn_mkt_inv = current
                macro = self.macro_fn(obs, player, view, self.prev_mkt_inv)
            else:
                macro = self.macro_fn(obs, player, view)
            if P.ROUTE_NN_ON:
                route_nn.arm(obs)                   # [SWITCH, ROUTENN1] dawn obs for the hire head
            program = (self.program_engine.reconcile(view)
                       if self.program_engine is not None else None)
            _tb = __import__("time").time() if P.ROUTE_VRP_ON else 0.0
            q4_rel = 0
            if (P.Q4_VRP_ON and P.ROUTE_VRP_ON and P.Q4_VRP_FUND == "true"   # [SWITCH, Q4VRP1] bank release
                    and int(view.nquad) == 3 and int(P.Q4_VRP_DAY) <= day <= int(P.Q4_VRP_LAST)):
                q4_rel = min(max(int(getattr(self, "vrp_saved", 0)), 0), int(spec.LAND_PRICES[2]))
                P.Q4_VRP_RELEASE = q4_rel
            try:
                self.plan = P.build_day(np, view, macro, program_engine=program)
            finally:
                if q4_rel:
                    P.Q4_VRP_RELEASE = 0
            if q4_rel and (np.asarray(self.plan[3]) == P.O.MO_BUY_LAND).any():
                self.vrp_saved = getattr(self, "vrp_saved", 0) - q4_rel
            if P.ROUTE_VRP_ON:                      # [SWITCH, ROUTEOPT1] day crew VRP, mode ii
                import time as _time
                st = {}
                _t0 = _time.time()
                if not hasattr(self, "vrp_fill"):
                    self.vrp_fill = {}
                self.plan = route_vrp.apply(self.plan, obs, day, st, self.vrp_fill)
                self.vrp_saved = getattr(self, "vrp_saved", 0) + int(st.get("drop_cost", 0))
                if route_vrp.TLOG:
                    with open(route_vrp.TLOG, "a") as _fh:
                        _fh.write(f"{day}\t{_t0 - _tb:.3f}\t{_time.time() - _t0:.3f}\t{int(st.get('drop_cost', 0))}\n")
            self.day = day
            self.overflow_pending.clear()

        # The one thing the day's plan cannot know at hour 0 [SWITCH,
        # OPEN_PUMP_TELL_KEEP0]: whether the other seat drew on the wheat pot
        # at hour 0 too. The pot at hour 1 says so, and `open_pump_tell_keep0`
        # turns that into the sell-back's quantity. Off -- and on every turn
        # but day 0's BUY row -- `open_pump_tell_armed` is a Python `and` and
        # the market is not even parsed.
        if P.open_pump_tell_armed(day, hour):
            self.plan = P.open_pump_tell_keep0(self.plan, day, hour,
                                               parse.parse_market(obs)[0])

        if P.OVERFLOW_GUARD_ON:
            overflow_guard(self.plan, obs, self.overflow_pending)
            if P.OVERFLOW_GUARD_V2:
                overflow_guard_v2(self.plan, obs, self.overflow_pending)
            if P.OVERFLOW_GUARD_V3:
                overflow_guard_v3(self.plan, obs, self.overflow_pending)

        action = render.turn_action(self.plan, hour, len(farm["hands"]))
        if self.program_engine is not None:
            action = self.program_engine.repair_decay(obs, action, self.plan)
            action = self.program_engine.repair_sales(obs, action, self.plan)
            action = self.program_engine.repair_land(obs, action, self.plan)
            action = self.program_engine.repair_herd(obs, action, self.plan)
            action = self.program_engine.repair_hire(obs, action, self.plan)
            action = self.program_engine.repair_work(obs, action, self.plan)
        if P.ROUTE_NN_ON:                           # [SWITCH, ROUTENN1] idle-unit dispatch
            action = route_nn.step(self, obs, action, self.plan)
        if P.ROUTE_NN3_ON:                          # [SWITCH, ROUTENN3] full-task-list crew pointer
            action = route_nn3.step(self, obs, action, self.plan)
        if route_nn.TRACK:                          # training / gate only: day reward + crew metrics
            route_nn.observe(obs, action)
        # Our own side of the identity is the row we ORDER, which is all the
        # observation will ever carry: there is no fill report [RIVAL_TELL].
        if self.tell is not None:
            self.tell.record_orders(action["market"])
        if self.program_engine is not None:
            self.program_engine.record(day, action)
        return action


def make_agent(macro_fn, pass_prev_mkt_inv=False):
    """Wrap a macro function into a kaggle_environments agent callable.

    `KAGG3_OPENING="<tape main.py>:<K>"` splices a recorded opening in front of
    the planner for days `[0, K)` (see `opening.py`); unset -- the default --
    the returned agent is the plain planner, unwrapped.
    """
    rt = {}

    def agent(obs, config=None):
        p = obs.get("player", 0)
        if p not in rt:
            rt[p] = Runtime(macro_fn, pass_prev_mkt_inv=pass_prev_mkt_inv)
        return rt[p].act(obs, config)

    from .opening import from_env
    return from_env(agent)
