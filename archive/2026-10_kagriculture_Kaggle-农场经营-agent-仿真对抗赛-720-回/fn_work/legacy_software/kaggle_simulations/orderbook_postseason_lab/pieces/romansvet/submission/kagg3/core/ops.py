"""Unit op codes and the market order encoding shared by the sim and the agent."""

from __future__ import annotations

# --- unit ops -------------------------------------------------------------
OP_PASS = 0
OP_NORTH = 1
OP_SOUTH = 2
OP_EAST = 3
OP_WEST = 4
OP_PLANT = 5           # arg = crop index
OP_WATER = 6
OP_HARVEST = 7
OP_FERTILIZE = 8
OP_DIG = 9
OP_BUILD_COOP = 10
OP_BUILD_PASTURE = 11
OP_FEED = 12
OP_COLLECT_FERT = 13
OP_CARE = 14
OP_PICKUP = 15         # arg = item index, qty
OP_DROP = 16
OP_PLACE = 17          # arg = item index, qty
N_OPS = 18

OP_NAMES = {
    OP_PASS: "PASS",
    OP_NORTH: "NORTH",
    OP_SOUTH: "SOUTH",
    OP_EAST: "EAST",
    OP_WEST: "WEST",
    OP_PLANT: "PLANT",
    OP_WATER: "WATER",
    OP_HARVEST: "HARVEST",
    OP_FERTILIZE: "FERTILIZE",
    OP_DIG: "DIG",
    OP_BUILD_COOP: "BUILD_COOP",
    OP_BUILD_PASTURE: "BUILD_PASTURE",
    OP_FEED: "FEED",
    OP_COLLECT_FERT: "COLLECT_FERTILIZER",
    OP_CARE: "CARE",
    OP_PICKUP: "PICKUP",
    OP_DROP: "DROP",
    OP_PLACE: "PLACE",
}

# Ops that move the unit; (dx, dy) with y growing downward, matching FARMER_MOVES.
MOVE_DELTA = {
    OP_NORTH: (0, -1),
    OP_SOUTH: (0, 1),
    OP_EAST: (1, 0),
    OP_WEST: (-1, 0),
}

# --- market orders --------------------------------------------------------
MO_NONE = 0
MO_HIRE = 1
MO_BUY_LAND = 2
MO_BUY_SEED = 3        # arg = crop index
MO_BUY_ANIMAL = 4      # arg = animal index
MO_BUY_PRODUCT = 5     # arg = product index (WHEAT or FERTILIZER only)
MO_SELL = 6            # arg = product index

MO_NAMES = {
    MO_HIRE: "HIRE",
    MO_BUY_LAND: "BUY_LAND",
    MO_BUY_SEED: "BUY_SEED",
    MO_BUY_ANIMAL: "BUY_ANIMAL",
    MO_BUY_PRODUCT: "BUY_PRODUCT",
    MO_SELL: "SELL",
}

# --- intra-day schedule layout (see docs/DESIGN.md) -----------------------
# turn 0 : HIRE x min(H, 10)
# turn 1 : BUY_PRODUCT x2, BUY_SEED x5, BUY_ANIMAL x1
# turn 2 : HIRE x max(H - 10, 0)
# turn 3 : SELL x9 (lot 1) + BUY_LAND in slot 9
# turn 20: nothing, or -- under `plan.PRESTOCK_ON` -- tomorrow's BUY_PRODUCT x2
#          (and BUY_SEED x5 under `plan.PRESTOCK_SEEDS`, which is off and
#          measured), bought tonight so tomorrow's crew can PICKUP at turn 1
#          instead of waiting on turn 1's BUY row (`TURN_PRESTOCK`)
# turns 10, 18 : SELL x9 (lots 2, 3)
# turns B .. B+P-1 : units PICKUP (P = 0..MAX_PICKUPS pickup ops needed today)
# turns B+P .. 23  : units walk their route
#
# B is ROUTE_BASE, or ROUTE_BASE_WIDE on a day that uses the turn-2 hire row,
# and SELL_TURNS[0] + 1 on a day that buys land -- the quadrant unlocks in that
# turn's market phase, after its unit phase, so nothing can work it earlier.
#
# Under `plan.MARKET_PACK_ON` a day whose HIRE and BUY orders together fit one
# turn's ten slots presents both at turn 0 and leaves turn 1 empty, and B is
# ROUTE_BASE_PACK; every other day keeps the layout above exactly.
#
# BUY_LAND is last in the day's purchase order and it is there on purpose
# [M2]: it is the only order the morning's own sale can fund, because the whole
# BUY row resolves at turn 1 ahead of every sell turn. It is atomic (the engine
# resolves it at the head of its slot round, outside the SELL/BUY lockstep), so
# slot 9 of a SELL turn is safe opposite anything the other seat presents.
#
# Two HIRE turns, not one [LAW]: the engine caps hands at nothing, but
# `_process_market` truncates each seat's queue to `maxMarketOrdersPerTurn`
# (10) a turn, so a crew past ten has to be hired over more than one turn. Turn
# 1 is not available -- the BUY row's nine slots have to resolve before any
# unit picks its inputs up -- so the overflow row is turn 2, and SELL lot 1
# moves to turn 3 to leave it empty.  Moving lot 1 costs nothing: the shops
# tick every four turns and the centre once a day, so the market the sale meets
# at turn 3 is the one it met at turn 2 (`projector.ticks_before`).
TURN_HIRE = 0
TURN_BUY = 1
#: Where `plan.PRESTOCK_ON` puts tomorrow's BUY_PRODUCT (and, under
#: `plan.PRESTOCK_SEEDS`, BUY_SEED) row. It has
#: to sit after `SELL_TURNS[-1]` (nothing earlier is free) and before the last
#: turn of the day, and among the free turns 19..23 the choice is arbitrary in
#: price: `projector.ticks_before` gives 19 and 20 the same tick count, and the
#: day is over either way. 20 is taken so 19 stays free for a future fourth
#: lot. OFF nothing is emitted here and the row is all MO_NONE.
TURN_PRESTOCK = 20
#: Where hires 11..MAX_HANDS go. Must stay below `SELL_TURNS[0]` and inside
#: `FULL_MARKET_TURNS`.
TURN_HIRE_WIDE = 2
HIRE_TURNS = (TURN_HIRE, TURN_HIRE_WIDE)
# SELL turns, seven then eight steps apart: the shops restock every four steps,
# so each later lot sells into a market two ticks recovered from the previous
# one. Every extra SELL turn costs a full market resolution in the simulator
# (~6% of episode throughput each), which is why there are three and not six.
SELL_TURNS = (3, 10, 18)
#: Where `plan.MELON_OPEN_ON`'s dump day offers its melon [SWITCH]. Melon-only
#: rows, empty on every other day of the season, and their engine hours (t + 1)
#: are 12, 14 and 16 -- all three in front of the hour 17 at which every
#: 2800-tier opponent's own melon dump lands, in 8/8 replayed games
#: (`scratchpad/open_vs_melon/report.md`). Three of them and not one, because
#: the melon curve is squared (`spec.MARKET_ROWS`) and the recorded opening
#: walks it in six lots of at most 24 rather than jumping it in one line: 84
#: units in a single order take the quote 248 -> 104 by themselves. They cost
#: what any SELL turn costs -- a full market resolution each, ~6% of simulator
#: throughput -- which is why they are behind a switch and not in `SELL_TURNS`.
MELON_LOT_TURNS = (11, 13, 15)
#: Where `plan.EARLY_SELL_ON` puts the day's lots [SWITCH]. The strategy study
#: of 2026-09-03 (docs/strategy, 3.1-3.2) reads the engine this way: a market
#: order costs no unit-turn, `_process_market` truncates each *seat's* queue to
#: ten orders a turn (HIRE and BUY_LAND count against that ten -- they are
#: queue entries like any other, only atomic once parsed), and within one turn
#: the two seats' SELL/BUY orders are quoted off one pre-commit inventory and
#: committed in per-unit lockstep. So two seats selling in the same turn split
#: the curve evenly and the only way to be *first* is to sell in an earlier
#: turn. Everything a unit harvested yesterday is already in the shed at hour 0
#: (`_end_of_day` -> `_drop_inventories_to_shed`), and with the DROP switches
#: off nothing else reaches the shed during the day, so the whole of what the
#: day means to sell exists before the first order goes out: "as it lands" is
#: "as early as the row layout allows".
#:
#: `EARLY_SELL_LOT1_TURN` is `TURN_BUY`, not `TURN_HIRE`: turn 0's row can be a
#: full ten hires and the eleventh order would be dropped in silence, while the
#: BUY row's ten slots are seldom more than a quarter live, so lot 1 rides
#: behind the day's purchases in the same turn -- and only on a day the two
#: together fit the ten (`plan._market`'s `fits`, which falls the lot back to
#: `SELL_TURNS[0]`). Behind the purchases and not in front of them so every buy
#: meets the inventory it always met.
EARLY_SELL_LOT1_TURN = TURN_BUY
#: Lots 2 and 3 under `EARLY_SELL_MODE = "B"`: the first two free turns after
#: `SELL_TURNS[0]`, which is as early as a lot can stand on its own row. Every
#: recorded 2800-tier opponent's flow lands at hours 10-17 and kagg2's at 17,
#: so a day that is finished selling by hour 6 is in front of all of them.
#: They cost nothing in the simulator: mode B resolves six market turns
#: (0,1,2,3,4,5) against the shipped schedule's six (0,1,2,3,10,18), so the
#: usual ~6% of episode throughput per extra SELL turn is not charged here.
EARLY_SELL_LATE_TURNS = (4, 5)
#: Mode "Z"'s day layout [SWITCH, EARLY_SELL]. Mode "A" rides the lot behind
#: the BUY row because turn 0 can be a full ten hires; mode Z answers the same
#: reading the other way round -- it gives the LOT turn 0 outright, with the
#: whole ten slots to itself if it wants them, and moves the morning's own rows
#: one turn later:
#:
#:   turn 0  SELL lot 1 (9 slots at most, so it always fits)
#:   turn 1  HIRE x min(H, 10), and the BUY row behind them when the two
#:           together fit the ten (`n_hire + n_buy <= MAX_MARKET_ORDERS`)
#:   turn 2  HIRE x max(H - 10, 0), or the BUY row when turn 1 had no room
#:
#: A hand hired in turn t first acts in t + 1 [LAW], so the whole crew's floor
#: is turn 2 rather than turn 1 -- that is what mode Z costs, and it is charged
#: in `plan`'s crew enumeration (`route_turns` plus the Z correction) rather
#: than assumed away. A day whose crew needs the overflow row (`n_hire > 10`)
#: has no free turn left for the purchases at all, so it is NOT a Z day: it
#: falls back to mode A's layout, which is the one thing turn 2 can carry
#: alongside eleven-plus hires.
EARLY_SELL_Z_LOT_TURN = 0
EARLY_SELL_Z_HIRE_TURN = 1
EARLY_SELL_Z_HIRE_WIDE_TURN = 2
#: The two turns mode Z's BUY row may stand on: turn 1 behind the hires when
#: the ten slots hold both, else turn 2 on its own.
EARLY_SELL_Z_BUY_TURNS = (1, 2)
#: Mode "Z1"'s gate: the hour-0 shed, in units over the nine products, at or
#: past which the day is worth taking turn 0 for. Read off the SHED and not off
#: the lot, and that is forced rather than chosen: `_plan_day` fixes
#: `route_base` before `core.sell` has cut the lots, so a lot-sized predicate
#: could not be the one the routes were laid out under. The shed at hour 0 is
#: what the lots are cut FROM (`_end_of_day` -> `_drop_inventories_to_shed`,
#: and with the DROP switches off nothing else reaches it during the day), so
#: it is the same quantity one step earlier.
EARLY_SELL_Z_MIN_SHED = 40
#: Turns 0 .. FULL_MARKET_TURNS-1 carry the day's whole market row (both HIRE
#: rows and the BUY row); every later market turn carries SELL and nothing else,
#: which is what lets `sim/rollout.py` compile the cheap sell-only path for them.
FULL_MARKET_TURNS = 3
#: First turn a unit may act on. A hand hired in turn t is appended during turn
#: t's market phase, which runs *after* that turn's unit actions, so it first
#: acts in turn t+1 and has 24-(t+1) actions left. ROUTE_BASE is turn 1's
#: hires' first turn; ROUTE_BASE_WIDE is turn 2's.
#
# The wide base applies to the *whole* crew, not just the late hires, and that
# is a LAW rather than tidiness: `_spawn_hand` puts a new hand on the least
# occupied shed-access tile, so `plan.SPAWN_SLOT`'s "hand h lands on access tile
# (h+1) % 4" only holds while every unit is still standing on its spawn tile
# when the hire resolves. One unit that walked at turn 2 moves every later
# hand's spawn, and a route laid out from the wrong start tile works the wrong
# tiles for the rest of the day.
ROUTE_BASE = 2
ROUTE_BASE_WIDE = 3
#: The same two under `plan.PRESTOCK_ON`, on a day whose residual BUY row is
#: empty. Nothing has to resolve at turn 1 then -- last night bought what the
#: morning's PICKUPs consume -- so the day's second hire row moves up from turn
#: 2 to turn 1 and every unit starts a turn earlier. Both still obey the one
#: law that fixes them: a hand hired in turn t first acts in turn t+1, so a
#: narrow crew (hired at TURN_HIRE alone) may walk from turn 1 and a wide one
#: (whose overflow row is then turn 1) from turn 2.
ROUTE_BASE_PRE = 1
ROUTE_BASE_WIDE_PRE = 2
#: The crew's first turn on a day `plan.MARKET_PACK_ON` packs [SWITCH]. When
#: the whole day's market row -- its hires and its purchases together -- fits
#: the ten slots `maxMarketOrdersPerTurn` allows one turn, all of it is
#: presented at `TURN_HIRE` and `TURN_BUY` carries nothing. Then nothing has to
#: resolve at turn 1 and the only law left is the hire one: a hand hired in
#: turn t first acts in t + 1, so the whole crew -- the blocks that owe a
#: PICKUP included, since the row they wait on has already resolved -- starts
#: at turn 1. Turn 0 stays idle for everyone whatever the packing, for the
#: reason `ROUTE_BASE_WIDE` gives: turn 0's hire row resolves *after* turn 0's
#: unit phase, so a unit that has stepped off its shed-access tile by then
#: moves every hand `_spawn_hand` places.
ROUTE_BASE_PACK = 1
#: The crew's first turn on a mode "Z" day [SWITCH, EARLY_SELL]. Z hires at
#: `EARLY_SELL_Z_HIRE_TURN`, so no unit may act before turn 2 whatever else the
#: morning does -- the hire law again, and `ROUTE_BASE_WIDE`'s spawn-occupancy
#: reason on top of it. `ROUTE_BASE_Z` is the base of a day whose BUY row fit
#: turn 1 behind the hires; `ROUTE_BASE_Z_LATE` is a day whose purchases went
#: to turn 2, so every PICKUP waits one more turn. `ROUTE_SPLIT_ON` hands the
#: turn back, per block, to a block the BUY row does not feed (`plan`).
ROUTE_BASE_Z = 2
ROUTE_BASE_Z_LATE = 3
#: The five pickup kinds a unit's block can consume -- feed wheat, fertilizer,
#: and one per animal kind -- and so the most PICKUP turns one block can hold
#: [0.12]. Five and not three because a day may place geese, cows and sheep at
#: once, and the engine charges a PICKUP turn for each: that is the true cost
#: of spreading three kinds across one sweep, and the day admits fewer tiles
#: accordingly rather than pretending otherwise.
#: Documentation only: the planner charges the exact count the day wants
#: (`plan._pickup_kinds`, 0..5) to every unit's route budget; nothing reads
#: this constant.
MAX_PICKUPS = 5


def _check_schedule():
    """The layout's own consistency, asserted at import rather than assumed.

    Every one of these is a place the schedule can be edited into something the
    engine silently mangles -- a hire row past the queue, a hire that lands
    after a unit has walked, a SELL turn the simulator's cheap path skips.
    """
    from .. import spec
    assert TURN_HIRE < TURN_BUY < TURN_HIRE_WIDE, "the BUY row must resolve before pickups"
    assert max(HIRE_TURNS) < FULL_MARKET_TURNS <= min(SELL_TURNS), \
        "every hire turn takes the full market path; every SELL turn the sell-only one"
    assert ROUTE_BASE == TURN_BUY + 1 and ROUTE_BASE_WIDE == TURN_HIRE_WIDE + 1, \
        "a hand hired in turn t first acts in turn t+1"
    # The same law under `plan.PRESTOCK_ON` [SWITCH]. The BUY row is what
    # forces `ROUTE_BASE` past `TURN_HIRE + 1`, so when it is empty the only
    # constraint left is the hire one -- stated here as the hire turns the two
    # prestock bases actually stand on, rather than as `ROUTE_BASE - 1`, which
    # would be a coincidence of today's numbers and not a rule.
    assert ROUTE_BASE_PRE == TURN_HIRE + 1 and ROUTE_BASE_WIDE_PRE == TURN_BUY + 1, \
        "on an empty-BUY day the overflow hire row is TURN_BUY and the law is still t+1"
    assert ROUTE_BASE_PRE <= ROUTE_BASE and ROUTE_BASE_WIDE_PRE <= ROUTE_BASE_WIDE, \
        "prestock may only move a unit's start earlier"
    # The same law under `plan.MARKET_PACK_ON` [SWITCH]: a packed day presents
    # its whole market row at `TURN_HIRE`, so the crew's floor is that row's
    # own -- one turn after the hires resolve, and never turn 0.
    assert ROUTE_BASE_PACK == TURN_HIRE + 1, \
        "a packed day's whole market row is TURN_HIRE's, and the law is still t+1"
    assert TURN_HIRE < ROUTE_BASE_PACK <= ROUTE_BASE, \
        "packing may only move a unit's start earlier, and never onto the hire turn"
    assert SELL_TURNS[-1] < TURN_PRESTOCK < spec.TURNS_PER_DAY - 1, \
        "the prestock row needs a free market turn after the last lot"
    assert TURN_PRESTOCK >= FULL_MARKET_TURNS and TURN_PRESTOCK not in SELL_TURNS, \
        "the prestock row must not collide with a turn the day already uses"
    assert spec.MAX_HANDS <= len(HIRE_TURNS) * spec.MAX_MARKET_ORDERS, \
        "the crew does not fit the hire rows' market slots"
    assert spec.N_PRODUCTS <= spec.MAX_MARKET_ORDERS, "a SELL lot must fit one turn"
    # The melon opening's extra lots [SWITCH]. Asserted unconditionally --
    # `ops` cannot read `plan` (it is `plan` that imports `ops`) and the layout
    # has to be consistent whichever way the switch is set.
    assert FULL_MARKET_TURNS <= min(MELON_LOT_TURNS), \
        "every melon lot takes the sell-only market path"
    assert max(MELON_LOT_TURNS) < SELL_TURNS[-1], \
        "a melon lot that is not in front of the last lot is not a melon lot"
    assert not (set(MELON_LOT_TURNS) & (set(SELL_TURNS) | {TURN_PRESTOCK})), \
        "a melon lot must not collide with a turn the day already uses"
    # `plan.EARLY_SELL_ON`'s turns [SWITCH], asserted unconditionally for the
    # same reason the melon lots are: `ops` cannot read `plan`.
    assert EARLY_SELL_LOT1_TURN < FULL_MARKET_TURNS, \
        "lot 1's early turn rides a full-row turn, so it needs no market resolution of its own"
    assert EARLY_SELL_LOT1_TURN not in HIRE_TURNS, \
        "a hire row can be a full ten orders; a lot behind it would be truncated away"
    assert min(EARLY_SELL_LATE_TURNS) > SELL_TURNS[0], \
        "the early late-lots must leave SELL_TURNS[0] to lot 1's fallback and the land slot"
    assert max(EARLY_SELL_LATE_TURNS) < SELL_TURNS[1], \
        "an early lot that is not in front of the shipped one is not an early lot"
    assert not (set(EARLY_SELL_LATE_TURNS) & (set(MELON_LOT_TURNS) | {TURN_PRESTOCK})), \
        "an early lot must not collide with a turn the day already uses"
    # Mode "Z"'s layout [SWITCH], asserted here for the same reason.
    assert (EARLY_SELL_Z_LOT_TURN < EARLY_SELL_Z_HIRE_TURN
            < EARLY_SELL_Z_HIRE_WIDE_TURN), \
        "Z sells first, then hires, then overflows"
    assert EARLY_SELL_Z_LOT_TURN == TURN_HIRE and EARLY_SELL_Z_HIRE_TURN == TURN_BUY \
        and EARLY_SELL_Z_HIRE_WIDE_TURN == TURN_HIRE_WIDE, \
        "Z re-uses the three morning turns; it does not add one"
    assert EARLY_SELL_Z_HIRE_WIDE_TURN < FULL_MARKET_TURNS <= SELL_TURNS[0], \
        "every Z row takes the full market path, and none of them is a SELL turn"
    assert EARLY_SELL_Z_BUY_TURNS == (EARLY_SELL_Z_HIRE_TURN,
                                      EARLY_SELL_Z_HIRE_WIDE_TURN), \
        "the Z BUY row stands on a hire turn, behind the hires, or on the next one"
    assert spec.N_PRODUCTS <= spec.MAX_MARKET_ORDERS, \
        "Z's turn-0 lot has the whole row and still has to fit it"
    assert ROUTE_BASE_Z == EARLY_SELL_Z_HIRE_TURN + 1, \
        "a hand hired in turn t first acts in turn t+1"
    assert ROUTE_BASE_Z_LATE == EARLY_SELL_Z_BUY_TURNS[1] + 1, \
        "a unit may not PICKUP before the BUY row it waits on resolves"
    assert ROUTE_BASE <= ROUTE_BASE_Z <= ROUTE_BASE_Z_LATE, \
        "Z may only move a unit's start later"


_check_schedule()

# --- horizon ---------------------------------------------------------------
# The last day whose end-of-day still banks production into the shed. Day 29
# has no end-of-day (episodeSteps 720; step 718 is the last one executed), so
# a day-29 harvest never reaches the shed and the day-29 sale draws only on
# the hour-0 stock. Every terminal rule derives from this one number -- work
# is worth planning only if its payoff lands by this day's eod -- and DROP
# (PLANNER_V3_1 section 4) is the change that would move it.
LAST_SHED_DAY = 28
