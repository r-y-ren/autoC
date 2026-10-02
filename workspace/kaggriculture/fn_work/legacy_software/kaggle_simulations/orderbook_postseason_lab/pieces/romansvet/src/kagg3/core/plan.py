"""The day planner: the single source of truth shared by the JAX simulator and
the numpy submission.

Given one player's state at hour 0 and a macro action, it emits the whole day as
arrays:

    unit_op [MAX_UNITS, 24]   op code per unit per turn
    unit_a  [MAX_UNITS, 24]   op argument (crop / item index)
    unit_q  [MAX_UNITS, 24]   op quantity (PICKUP / PLACE only)
    mkt_op  [24, 10]          market order op code per turn per slot
    mkt_a   [24, 10]          market order argument
    mkt_q   [24, 10]          market order quantity

The simulator applies those effects; the submission renders them into
kaggle_environments action dicts. Neither re-derives anything, so the two cannot
drift apart.

Written against an array module `xp` (numpy or jax.numpy) using only
shape-static control flow, so it traces under jit and vmaps cleanly.

Intra-day layout
----------------
    turn 0            market: HIRE x min(H, 10)             units: PASS
                              (none on the terminal day)
    turn 1            market: BUY_PRODUCT x2, BUY_SEED x5,
                              BUY_ANIMAL x1                 units: PASS
                              (none on the terminal day)
    turn 2            market: HIRE x max(H - 10, 0)         units: PASS
    turns 3, 10, 18   market: SELL x9 (lots 1, 2, 3)
                              (the lot allocator decides the split; on the
                               terminal day it runs at zero reservation)
    turn 3            market: ... and BUY_LAND in slot 9, after the sells, so
                              the morning's revenue can fund it [M2]
    turn B .. B+P_u-1                                       unit u: PICKUP, one per kind its block consumes
    turn B+P_u .. 23                                        unit u: walk its route

P_u is 0..3 per unit and is charged inside that unit's block, so a unit with
nothing to pick up walks from turn B. Under `ROUTE_EARLY_ON` such a unit walks
from turn B - 1 instead, while the blocks that do owe the BUY row keep waiting
for it -- the market row itself never moves.

On a day that buys land B moves again, to the turn after `O.SELL_TURNS[0]`:
the quadrant is unlocked in that turn's market phase, which runs after its unit
phase, so every unit idles until then or works a tile that is still LOCKED.

B is `O.ROUTE_BASE` (2), or `O.ROUTE_BASE_WIDE` (3) on a day that uses the
turn-2 hire row -- the engine's market queue is ten orders a turn, so a crew
past ten needs a second HIRE turn, and a hand hired in turn t only exists from
turn t + 1. The wide base applies to the *whole* crew: `SPAWN_SLOT` below is
only the engine's spawn rule while every unit is still on its spawn tile when
a hire resolves. So the day's turn budget is 22 turns per unit up to ten hands
and 21 beyond, which is exactly what the enumeration below charges each
candidate.

Labour: admit, then route
-------------------------
Which tiles get worked is not a gene. Every queued op is priced in coins
(harvests at today's quotes, survival work at what it saves, development at
its stream value), and `build_day` admits tiles by (mandatory tier, value)
against the day's whole turn budget -- each costed at its ops plus a
`EST_MOVES` and the morning walk out of the shed (`EST_LEAD`) -- then routes
the admitted set spatially, as one serpentine sweep of the priced-or-mandatory
work followed by one of the work that is worth nothing (a weed dig on a day
with no planting to protect), so zero-value work can never spend the turns a
priced tile needs. Two groups and not four: a group of m scattered tiles spans
the whole board however small it is, so every populated group costs the crew
another crossing of the worked span. 0.5's LAW is kept by admission, which
still orders by the mandatory flag and only ever drops from the value tail. The
estimate is not a bound, so admit-and-route runs `ADMIT_ROUNDS` times, each
round dropping the tiles the exact route could not reach from the value tail.
`_routes` cuts the resulting order into one contiguous block per unit and
charges the exact Manhattan moves between consecutive tiles.

Hiring: an enumerated argmax
----------------------------
How many hands walk that route is not a gene either, so the day is derived
twice. Pass A (`_derive` on a zero hire bill) prices and orders every tile
once; each hand count h in 0..MAX_HANDS is then scored off that single
ordering -- the value of the prefix (h + 1) units' turns can admit, less h's
fib bill -- and the best affordable h wins, ties to fewer hands. Pass B
re-derives with the winner's bill deducted from the purse, so the purchases
the day commits are ones it can still pay for once turn 0 has hired. It is an
argmax under the planner's own value model, not an exact one: spawn positions,
per-unit pickup turns and purchase interactions sit outside the projection.

The day's **cash reserve** (`cash_reserve`) -- the fib bill of tomorrow's crew
at the count this day chose, one hand wider -- binds both halves of that. A
hand count is a candidate only if its bill *and* that reserve fit `view.money`,
and pass B deducts both before the buy side sees a coin. Without the first the
enumeration spends the reserve on the crew itself; without the second the
greedy spends the purse to the last coin every morning. Either way the farm
wakes up unable to field anybody -- the fib bill is small but it is not zero,
and a day with no hands produces almost nothing to sell, which is a spiral
rather than a bad day. The floor is structural, derived from `HIRE_BILLS`, and
void from `LAST_SHED_DAY` on, where there is no tomorrow to hire for.

Provisioning is the executor's job, not the policy's
----------------------------------------------------
GOAL.md scopes the micro-executor as fixed "don't let things die" actuator logic.
So the planner derives its own input purchases -- feed wheat, fertilizer, the
day's animals -- from what the day actually requires, then clamps every task set
to what the budget really bought. A macro action can therefore never schedule an
op the farm cannot resource, which would otherwise burn a turn for nothing and
put a cliff in the fitness landscape exactly where ES needs a gradient.

Purchases are emitted in a fixed slot order (survival inputs, then seeds, then
animals); land rides the first SELL turn's spare slot. The budget (`core/budget.py`) grants marginal candidates by
value per coin and never commits more than the purse holds, so the engine can
honour the whole row whatever sequence it resolves the slots in.

Operational metrics
-------------------
`build_day_stats` returns section 7's three planner-side metrics -- units the
shed destroys, coins the purse could not grant, queued task value the day's
route does not work -- for the same day `build_day` plans. Both call `_plan_and_stats`, so
the numbers describe the plan that is really walked rather than a second model
of it; `build_day`'s return tuple does not grow to carry them, and under jit
the discarded stats are dead code.
"""

from __future__ import annotations

import sys as _sys
from typing import NamedTuple

import numpy as np

from .. import spec
from . import budget as BUD
from . import ops as O
from . import policy as PO
from . import projector as PJ
from . import sell as SELL
from . import valuation as VAL

N_T = spec.N_TILES
TPD = spec.TURNS_PER_DAY
MU = spec.MAX_UNITS
MO = spec.MAX_MARKET_ORDERS
CHAIN_MAX = 6

#: Moves the admit stage charges a tile on top of its ops [1.6]. Consecutive
#: tiles of one serpentine crossing are adjacent, so one move is what a visit
#: really costs: measured over 32 real-engine games on 2026-08-26, the route
#: walks 0.97 inter-tile moves per tile it visits. It was 2 while the route
#: swept the board in four passes, where a visit cost 1.32 and the allowance
#: was standing in for the crossings; with one crossing (`_plan_and_stats`)
#: the conservative 2 over-charged every tile by one. Still an estimate and
#: not a bound -- see `ADMIT_ROUNDS`.
EST_MOVES = 1

#: Turns the admit stage charges *each unit* for the walk out of the shed
#: [1.6]. The engine clears `farm["hands"]` at every end of day
#: (`kaggriculture.py:880`) and re-spawns the whole crew on the four
#: shed-access tiles at the board's centre, so every unit walks out from the
#: middle every morning and none of it is amortisable across days. It was
#: never modelled, and it is a quarter of the season's whole turn budget:
#: measured over 32 real-engine games on 2026-08-26, 5.09 turns per active
#: unit-day against `starter` and 5.05 against `kagg2` (5.30 / 5.32 before the
#: mixed herd took `_pickup_kinds` from 3 to 5 -- the constant did not move).
#:
#: A measured constant rather than a bound, and that is safe by construction:
#: it only ever *subtracts* from the turn budget, so it can under-admit and
#: never over-admit, and the days it is wrong on are the early ones where one
#: to three units work next to the shed -- which are task-bound anyway (0.90
#: of days 0-11 fit all their queued work, against 0.11 of days 12-26).
#:
#: Both halves of this correction are the same model and neither is safe
#: alone: `EST_MOVES = 1` on its own measured -21,499 +- 10,810 coins against
#: `starter`, and this charge on its own -17,224 +- 8,946. Together they are
#: +11,854 +- 11,233.
EST_LEAD = 5

#: Share of the projected lot-1 revenue a land grant may count on [M2]. The
#: projection is opponent-free by construction (1.1) and the other seat's
#: lockstep sales at the same turn lower the quotes this one receives; a
#: BUY_LAND that then fails leaves every prospective op of the day no-oping on
#: a still-LOCKED tile with its seeds already bought, so the margin is wide and
#: the residual above it is the genes' to absorb.
LAND_REV_NUM, LAND_REV_DEN = 3, 4

#: ... and the hour-0 purse must still carry `1 / LAND_OWN_DEN` of the price on
#: its own [M2]. A quadrant funded *entirely* by a projection is the one whose
#: failure is total rather than marginal: the seeds are bought, the day's ops
#: are queued on tiles that stay LOCKED, and nothing on them can be re-planned.
#: Measured on the archetype ladder (2026-08-25): unguarded, `rusher` -- the
#: rung whose whole identity is buying land early -- fell from 12,749 coins to
#: 8,088 and through the ladder's liveness floor, because revenue it had not
#: banked kept buying it quadrants it could not work. Half in hand puts it back
#: at 10,913 and leaves `expander` (14,656 before M2) at 18,889.
LAND_OWN_DEN = 2

#: Tiles in one quadrant, and how many days of development the land valuation
#: may count a fresh tile's labour over [1.3].
LAND_TILES = spec.N_TILES // 4
DEV_DAYS = 2

#: Pickup turns `land_reach` charges every unit. A conservative constant, and
#: deliberately *not* `O.MAX_PICKUPS`: that is the ceiling one block owes when a
#: day spreads all three animal kinds across the sweep, and charging it to every
#: land valuation would price a crop day's quadrant as a labour overrun for
#: animals the day is not buying. Pinned at three rather than tracking
#: `O.MAX_PICKUPS` so that widening the pickup ceiling -- as the mixed herd did,
#: from three to five -- cannot silently reprice every quadrant on the board.
LAND_PICKUPS = 3

#: How many times `build_day` runs admit -> route [1.6]. The move estimate can
#: undershoot the exact route, which then leaves admitted tiles uncovered; each
#: extra round re-admits without them and routes again. A fixed count, so the
#: day scan stays shape-static.
ADMIT_ROUNDS = 3

# ---- ADMITSLACK: the day's step budget against the day it really spends -----
#
# `labour` below (:9287) cuts the day's turn budget by a PER-UNIT overhead --
# `max(_pickup_kinds, land_lead) + EST_LEAD`, 6.08 steps a unit-day measured
# over ENG22's 22 boards in d20-29 -- and the day then admits the longest
# prefix of the value order whose `cum_est` fits what is left.  Instrumented
# against the realised engine day (`S/admitslack/probe.py`, 22 boards, both
# halves of the same games), that overhead is charged three times over: the
# walk out of the shed really costs **1.25** move-steps a unit-day, the dawn
# wait **0.95** and the pickups **1.00** -- 3.20 against 6.08 -- while the
# per-task half under-charges (est 2.86 steps an admitted task against a
# realised 4.00, `EST_MOVES = 1` against 1.85 realised inter-tile moves).  The
# two errors do not cancel: the day ends with **16.0 tail-idle steps** (1.37 a
# unit-day) on **50.9 %** of its d20-29 days -- every one of which is a day
# admission DECLINED a ranked task on the budget (`n_adm` 56.3 of `n_tasks`
# 59.1).  Slack and declined work on the same day is the mis-calibration.
#
# ON, each unit's budget gets `ADMIT_SLACK_TURNS` back.  That is the safe
# direction by the module's own doctrine (:231): over-admission is what
# `ADMIT_ROUNDS` exists to repair -- each round drops the tiles the exact
# route could not reach, from the VALUE tail -- while an under-admission has
# no repair at all.  Deliberately NOT also given to the hire enumeration's
# `turns_h`, for `ADMIT_PICK_SHARED`'s reason: leaving the crew size where the
# champion put it makes this a test of the idle turns alone and not of a
# bigger payroll.
#
# Ceiling, priced at spot on the landing day with our own units' impact ON and
# nothing past d29 (`S/admitslack/report.py`): filling the measured slack with
# the next-ranked declined tasks, at their own estimate corrected by the
# measured 1.40 est->realised ratio, is **+669 a board (se 105, t 6.35),
# +13.2 ops a game** on ENG22.
ADMIT_SLACK_ON = False

#: Turns per unit `ADMIT_SLACK_ON` hands back to the admit stage.  One, not
#: the 2.9-step over-charge the instrument measured: the realised tail idle is
#: 1.37 steps a unit-day, so one turn a unit is the whole slack the route
#: actually leaves and every step past it would be admitted against work the
#: day has no room for.
ADMIT_SLACK_TURNS = 1

# ---- H5: charge the pickup allowance once, not per unit [SWITCH, OFF] ------
#
# Our units PASS on 18.1% of their actions (1,127 ops a game) against kagg2's
# 9.4%, and kagg2 gets 6,915 unit actions to our 6,231 (2026-08-30 profile,
# 192 real-engine games). The idle turns are not a staffing gap -- `hires_total`
# and `hands_d5/d10/d20` are statistically identical between the games we win
# and the ones we lose -- so they are an admission/routing loss.
#
# The largest asymmetry between what admission *charges* and what the route
# then *spends* is the pickup allowance. `_pickup_kinds(d)` is how many of the
# `N_PICK` kinds have any demand today; the line below charges it to **every**
# unit, while `_routes` charges each unit only the kinds its own contiguous
# block actually consumes (`d_pick[e]`). On a day whose feed, fertilizer and
# animals are concentrated in one or two blocks, that over-charge is up to
# `(n_units - 1) * N_PICK` = 60 turns of admitted work the crew has the time
# for and is never given -- so units run their stripe out and PASS.
#
# The two sides of the error are not symmetric, which is why the fix is to
# under-charge rather than over-charge: `ADMIT_ROUNDS` exists precisely to
# repair an over-admission (each round drops the tiles the exact route could
# not reach, from the value tail, and re-routes), while an under-admission has
# no repair at all -- the loop only ever lowers `n_admit`.
#
# Deliberately *not* also applied to the hire enumeration's `turns_h`, which
# makes the same per-unit charge: leaving the crew size where the champion put
# it is what makes this a test of the idle turns alone rather than of a bigger
# payroll.
#
# MEASURED 2026-08-30, 96 seeds x 2 seats against kagg2 (`--seed-base
# 20260828`), paired with the champion on (seed, seat):
#
#     win 82.8% (champion 78.1) | mean margin +9,171 (champion +9,013)
#     paired diff +158, sd 11,514, t = +0.19
#     discordant: 29 games won that the champion lost, 20 lost that it won
#
# The only one of the three 2026-08-30 interventions that is not negative, and
# the direction of every reading is the hypothesis' own: +4.7 points of win
# rate and a 29:20 discordance, against a paired margin that is flat. Read
# together that is a change which converts near-ties without moving the big
# margins -- which is what filling idle turns *should* look like -- but 29:20
# is p ~ 0.13 and t = +0.19 is nothing, so it stays OFF until a longer run or
# a second seed base separates it from noise. It is the switch to try first.
#
# OFF re-evaluates the original expression and nothing else, so the champion
# decodes byte for byte.
ADMIT_PICK_SHARED = False

# ---- DROP: play day 29 instead of passing it [SWITCH, OFF] -----------------
#
# `O.LAST_SHED_DAY` is 28 because a day-29 harvest goes to the *unit* inventory
# and only end-of-day banks it into the shed -- and day 29 has no end-of-day
# (episodeSteps 720; step 718 is the last executed one). So the terminal law
# suppresses every hire and every unit op, and the whole last day of the season
# is one liquidation of the hour-0 shed.
#
# DROP breaks that (PLANNER_V3_1 section 4). It is the engine's shed-adjacent
# deposit op: it moves the unit's inventory into the shed *in the unit phase*,
# before that turn's market. So the chain
#
#     walk out -> HARVEST -> walk back to a shed-access tile -> DROP -> SELL
#
# closes inside day 29 as long as the DROP lands on or before `SELL_TURNS[-1]`
# (turn 18), whose market resolves after its unit phase. kagg2 uses DROP about
# nine times a game; we have never emitted it.
#
# What the switch changes, and nothing else:
#
#   * day 29 hires again, through the *unchanged* enumeration -- the argmax
#     still has to find the harvest worth the fib bill, it is simply no longer
#     forced to zero;
#   * every unit's turn budget on that day is cut to what leaves room for the
#     return leg, and `_routes` appends `home walk + DROP` to each block, with
#     the exact per-block distance (`NEAR_X` / `NEAR_Y`) rather than a bound;
#   * sell lot 3 additionally offers what the route will actually bank, so the
#     decode sees a mid-day shed and not only the hour-0 one.
#
# Everything else the terminal day does is untouched: no purchases (the day's
# purse is still zeroed), and the shed is still liquidated at zero reservation
# across the three lots, because the terminal value of anything unsold is
# exactly zero either way.
#
# MEASURED 2026-08-30, 96 seeds x 2 seats against kagg2 (`--seed-base
# 20260828`), paired with the champion on (seed, seat):
#
#     win 79.2% (champion 78.1) | mean margin +9,474 (champion +9,013)
#     paired diff +461, sd 581, t = +11.0, 95% CI [+379, +543]
#     171 games gained coins, 17 lost, 4 identical; range -283 .. +2,599
#     discordant: 2 games won that the champion lost, 0 lost that it won
#
# The paired sd is *twenty times* smaller than the unpaired margin sd, which is
# what a change confined to the last day should look like: it adds a lot of
# coins on day 29 and perturbs nothing before it, so almost none of the season's
# variance rides along. The 17 losers are the coupled residue -- our day-29
# sales move the quotes kagg2's own day-29 sales then meet -- and the largest is
# 283 coins against a 2,599-coin best.
#
# Left OFF because the shipped theta is a promotion decision and this branch
# only measures the intervention; flipping the one constant below is the whole
# change.
#
# OFF, every expression below re-evaluates to the one it replaced, so the
# champion theta decodes byte for byte -- verified on 4 seeds x 2 seats against
# `flow38_g25_b28.csv`, every column identical.
DROP_ON = True

# ---- MIDDAY_DROP: bank day 28's harvest before its last market [SWITCH, OFF]
#
# The engine does **not** lose what a hand is still carrying at nightfall.
# `_end_of_day` calls `_drop_inventories_to_shed` for every seat *before* it
# clears `farm["hands"]`, so every unit's inventory is banked into the shed for
# free, wherever the unit is standing (`kaggriculture.py:843-892`,
# `sim/eod.drop_inventories`). What that dump does lose is the part that does
# not fit: the shed holds `SHED_CAPACITY` = 100 and the overflow is destroyed,
# exactly as an explicit DROP destroys it.
#
# MEASURED 2026-08-30 in the real engine (`_drop_inventories_to_shed`
# instrumented, champion theta vs kagg2, 48 games, seed base 20260828):
#
#     73,109 items carried into an end-of-day, 473 destroyed (29/48 games)
#     peak (unit inventory + shed) at an end-of-day: 132 against a 100 cap
#     upper bound on the coins destroyed: 675 a game, 7.2% of the mean margin
#     by day: 28 -> 315 units (67%), 21 -> 55, 16 -> 34, 18 -> 33, rest thin
#
# Two thirds of the season's loss lands on the single day the deadline harvest
# empties the board, `O.LAST_SHED_DAY`. So this switch extends the day-29 DROP
# chain one day back and nowhere else: on day 28 too, each block gains the walk
# home plus a DROP, the turn budget ends at `SELL_TURNS[-1] + 1` and sell lot 3
# offers what the route banks. The day's harvest then reaches the market in two
# instalments -- lot 3 on day 28 and the terminal liquidation on day 29 --
# instead of one dump that the 100-unit cap tops off and the price curve
# punishes.
#
# `K`, the turns a unit keeps back for the return, is not a new constant: it is
# `DIST_SHED` from the block's own last tile plus one for the DROP, which is
# what `_routes` already charges (`EST_HOME` is the admit stage's estimate of
# the same thing).
#
# What is deliberately *not* extended: `terminal` (day 28 still buys, still
# reserves, still has a tomorrow) and `_worth_a_turn` (a task worth nothing
# today can still be worth a turn on a day that has a tomorrow -- that pruning
# stays keyed to `terminal`, which is what it always read).
#
# Needs `DROP_ON`: every expression it touches is inside a `DROP_ON` block.
#
# MEASURED 2026-08-30, 96 seeds x 2 seats against kagg2 (`--seed-base
# 20260828`), paired on (seed, seat) against the same run with the switch off:
#
#     win 75.5% (75.5 against 79.2) | mean margin +8,316 against +9,474
#     paired diff -1,157, sd 1,423, t = -11.3, 95% CI [-1,359, -956]
#     17 games gained coins, 175 lost, 0 identical; range -7,857 .. +1,226
#     discordant: 0 games won that the baseline lost, 7 lost that it won
#
# **Rejected, and the reason is the labour and not the premise.** Day 29 can
# spend the whole return leg for free because every turn after `SELL_TURNS[-1]`
# is worth nothing there. Day 28's are worth a great deal: what a unit harvests
# in turns 19-23 is banked by the very end-of-day this switch is trying to beat
# and sold on day 29 regardless. Ending the route at turn 18 and charging each
# block `DIST_SHED + 1` on top costs a unit roughly ten of its twenty-two
# turns -- on a synthetic day-28 board (`tests/test_midday_drop.py`'s
# `_ripe_view`) twelve harvests fall to two -- against an overflow whose entire
# upper bound is 675 coins a game. The 100-unit ceiling is real, but a
# crew-wide return leg is an order of magnitude too expensive a way to lift it.
#
# What a future attempt would have to change first: let a unit keep working
# *after* its DROP, so the return leg costs the walk and not the tail of the
# day. That is a second block per unit in `_routes`, not a wider `drop_day`.
#
# OFF, `drop_day` is `terminal` and every expression re-evaluates to the one it
# replaced, so the champion theta decodes byte for byte -- verified on 96 seeds
# x 2 seats against `rep/drop_b28.csv`, all 192 rows identical, and pinned by
# `tests/test_midday_drop.py`.
MIDDAY_DROP_ON = False

# ---- HORIZON: re-derive the terminal bounds through DROP [SWITCH, OFF] -----
#
# `O.LAST_SHED_DAY` = 28 carries two different facts that were the same number
# only while day 29 was dead:
#
#   (a) the last day with an **end-of-day**, the last night the engine banks a
#       unit's inventory into the shed for free, and
#   (b) the last day whose **work can still be sold** -- the horizon every
#       terminal rule is actually written against ("is this plant, this animal,
#       this feed, this quadrant still worth anything?").
#
# `DROP_ON` broke the identity. Day 29's HARVEST/COLLECT -> walk home -> DROP
# -> `SELL_TURNS[-1]` chain closes inside the day, so (b) is now 29 while (a)
# stays 28. This switch is that one day, and `valuation.pay_day()` is the only
# place it is spelled: OFF it returns `O.LAST_SHED_DAY` and every expression
# below is the integer it always was.
#
# What moves, and why each bound moves by exactly one day (sim `eod.py`):
#
#   * `cash_reserve` -- was void from day 28 because "day 29 hires nobody by
#     law". Under `DROP_ON` day 29 *does* hire, and `HIRE_TURNS` all resolve
#     before `SELL_TURNS[0]`, so the day-29 crew is paid out of coins carried
#     overnight. Day 28 must hold the bill back like any other day.
#   * `survival_pays` -- a watering or feed on day `d` buys life on `d + 1`.
#     Day 28's now buys a day whose harvest sells, so survival waterings, the
#     survival feeds and the feed want's wheat come back on day 28. A plant
#     that weeds at eod 28 (`refresh_plants`: `cons >= 2`) and an animal that
#     escapes there (`refresh_animals`) have nothing to harvest on day 29.
#   * `harvest_age` -- the deadline clamp `clip(H - t_day, first, sat)` [0.1].
#     One more growing day for the crops the season cuts short: a wheat planted
#     on day 25 harvests 4 units on day 29 instead of 3 on day 28, a day-26
#     wheat 3 instead of 2. Unclamped tiles (`H - t_day >= sat`) do not move.
#     `brain.n_free_slots` reads the same clamp and moves with it.
#   * `can_mature` (`brain`) and `remaining_plant_units`' `can` -- a seed is
#     worth planting iff `day + CROP_FIRST_YIELD_DAY <= H`. Wheat and carrot
#     become plantable on day 27, tomato on 21, strawberry and melon on 19.
#   * the 0.2 animal bound (`ub_units`, `ub_fert`) and `animal_value` /
#     `_pipeline_units` -- a fire at eod 28 is harvestable on day 29 and now
#     sells, and `refresh_animals` re-arms `t_favail` at every eod, so the
#     fertilizer collections left run `day + 1 .. 29`. The doc's own example
#     (0.2: "a d25 goose collects three sellable fertilizers; the d29
#     collection and the first egg fire at eod 28 never monetize") is exactly
#     what this repeals.
#   * `care_ok` / `bank_val` -- a CARE pays at `h_next`, day 29 included.
#   * `fert_marginal_value` / `crop_remaining_value` -- the same horizon on the
#     value side, which is where 0.4's "the whole-window caps return under
#     DROP" lands: a one-time crop's last in-window watering is now day 29's.
#   * land -- no constant of its own [0.3]: a quadrant is priced by
#     `marginal_gain` off `new_plant_units` and `ub_coins`, so its last useful
#     purchase day slides by one on its own.
#
# What deliberately does **not** move, and it is not an oversight:
#
#   * `ub_feeds` stays `O.LAST_SHED_DAY - day`. It is a count of feeds, not a
#     horizon: the animal has to live through eod `H - 1` for its last
#     collection, i.e. be fed on days `day + 1 .. H - 1`. At H = 29 that is
#     exactly `28 - day`, which is what the line already charged -- the old
#     horizon was over-charging by one feed and the new one makes it exact.
#   * `terminal = day > O.LAST_SHED_DAY`. That is "the last day of the season"
#     (`spec.N_DAYS - 1`) wearing the constant, not a monetization horizon --
#     it is what suppresses purchases and liquidates the shed, and `drop_day`
#     is defined off it. Moving it to `> H` would make it never true and
#     delete the DROP module.
#   * the mandatory tier's `(day >= O.LAST_SHED_DAY) & want_harvest`. It is a
#     labour *floor*, not a gate: "from here on a harvest is deadline work".
#     Raising it to day 29 would only demote day-28 harvests, and day 29 is the
#     one day whose crew is capped at `SELL_TURNS[-1] + 1` turns and owes a
#     return leg -- a day-28 harvest deferred into it is not reliably
#     recoverable. Nothing is gained by lowering a floor.
#   * `brain.residual_drain`'s `grow_days`. That is a **network feature**
#     normalisation evaluated from day 0, not a decision bound; moving it
#     rescales an input the shipped theta was fit against across the whole
#     season, which is a retraining question and not this switch's.
#
# MEASURED 2026-08-30 in the real engine against kagg2, champion theta, paired
# on (seed, seat) against the same build with the switch off (`DROP_ON` on in
# both arms, so this measures the horizon and nothing else):
#
#   96 seeds x 2 seats, `--seed-base 20260828` (the discovery base):
#     win 88.0% (79.2 off) | mean margin +12,333 (+9,474 off)
#     paired diff +2,860, sd 7,633, t = +5.19, 95% CI [+1,780, +3,939]
#     157 games up, 35 down, 0 unchanged; range -13,902 .. +76,066
#     discordant: 19 games won that the baseline lost, 2 lost that it won
#
#   96 seeds x 2 seats, `--seed-base 20260830` (held out):
#     win 91.1% (84.9 off) | mean margin +11,317 (+9,356 off)
#     paired diff +1,960, sd 3,089, t = +8.79, 95% CI [+1,523, +2,397]
#     165 games up, 27 down, 0 unchanged; range -12,529 .. +17,635
#     discordant: 15 games won that the baseline lost, 3 lost that it won
#
# Read the sd, not only the t. DROP's own paired sd was 581 because it touched
# one day; this one is 3,089-7,633, and the reason is in the inventory above:
# `ub_fert` and `_pipeline_units` count "one fertilizer per remaining day", and
# that count moves by one on **every** day of a season that owns an animal. So
# the switch reprices the animal candidates from day 0, the trajectory diverges,
# and the season's whole variance rides on the difference -- 192 of 192 rows
# differ in both bases, and the walking route differs in 383 of 384 games. What
# does *not* move much is the lumpy decision: the quadrant count differs in 4
# games of 192 on the first base and 2 of 192 on the second. Both bases agree in
# direction and sign at t > 5, which is what a held-out base is for.
#
# ABLATION 2026-08-30, same 96 x 2 games on `--seed-base 20260828`, splitting
# the switch in two: an arm with `ub_units`, `ub_fert`, `_pipeline_units` and
# `animal_value` pinned back to `O.LAST_SHED_DAY` -- the terms that move on
# *every* day -- and everything else (the deadline clamp, the plant gate,
# `survival_pays`, `cash_reserve`, `care_ok`, the two value functions) at the
# new horizon:
#
#   endgame half alone, against the baseline:
#     +1,507 coins, sd 3,205, t = +6.51, win 84.4% against 79.2%
#     159 games up, 33 down; discordance 13:3
#   the animal/fertilizer stream on top of it:
#     +1,353 coins, sd 6,889, t = +2.72, win 88.0% against 84.4%
#     83 up, 55 down, **54 games untouched**; discordance 7:0
#     range -10,880 .. +71,660 -- the whole tail of the full measurement
#
# The two halves add to the +2,860 exactly. They are not the same quality of
# evidence. The endgame half is a tight, one-sided win with a third of the
# variance -- the horizon really was a day short. The stream half is the noisy
# one: it reprices the animal candidates from day 0, one game in three does not
# move at all, a third of the ones that do move lose coins, and a single game
# carries +71,660 of the mean. A promotion that wanted the safe half of this
# switch could take the endgame terms alone; the numbers for that arm are above.
#
# Left OFF because the shipped theta is a promotion decision and this branch
# only measures the intervention; flipping the one constant below is the whole
# change.
#
# OFF, `pay_day()` is `O.LAST_SHED_DAY` and every expression re-evaluates to
# the one it replaced, so the champion theta decodes byte for byte -- verified
# on 6 seeds x 2 seats against `rep/drop_b28.csv`, every column identical, and
# pinned by `tests/test_horizon_drop.py`.
HORIZON_DROP_ON = True

#: `valuation` reads the switch above through this binding rather than
#: importing this module -- `plan` imports `valuation`, and a lazy import in
#: the other direction is forbidden inside `kagg3/core` (see `valuation._PLAN`
#: for what it costs). Bound to the live module object, so flipping
#: `plan.HORIZON_DROP_ON` at runtime is seen by every horizon expression.
VAL._PLAN = _sys.modules[__name__]

# ---- SHED_OVERFLOW: sell the reservations the route never reaches [SWITCH, OFF]
#
# `_end_of_day` banks every unit's inventory into the shed for free and
# destroys only the part over `SHED_CAPACITY` = 100 -- a **total** over the
# shed's twelve slots, not a per-item cap (`sim/eod.drop_inventories` and
# `sim/units.py` both measure `SHED_CAPACITY - sum(shed[p])`). Measured in the
# real engine (48 games, champion theta vs kagg2): 473 units destroyed, upper
# bound 675 coins a game, 315 of them on `O.LAST_SHED_DAY`.
#
# 0.9's forced sale is already the answer to most of that, and this switch does
# not replace it -- it repairs the one place it is blind. The sale may draw on
# `avail`, the hour-0 shed **net of the day's reservations**, and those
# reservations are sized on the day's *queued* demand: every `want_feed` tile's
# wheat and every application `n_fert_eff` says the shed can supply. The route
# then only picks up what the blocks it actually reached consume (`blk`), which
# is exactly what `proj_eod` charges as `picks_out`. So stock reserved for a
# task the day never walks to is counted as staying in the shed by the
# projection and hidden from the sale by the reservation: it cannot be sold,
# nothing consumes it, and end-of-day destroys it to make room for the harvest.
#
# The block gives that residue -- `shed - picked up - sold` per product, which
# is precisely what nothing today will consume -- back to the same nine-round
# greedy, cheapest projected marginal first, and only as far as the deficit
# 0.9 could not cover. What the route *does* reach keeps its reservation, so no
# feed and no application is ever sold out from under a task the day performs.
#
# **Sell, never drop.** The (b) half of the hypothesis has no content in this
# engine: DROP discards the part of a unit's load that does not fit exactly as
# `_end_of_day` does (`sim/units.py` `d_take`, `sim/eod.py` `take`), so
# explicitly dropping the surplus banks the same coins as letting the night
# take it -- and it costs the walk home on top. The only lever that turns a
# surplus unit into coins is a lot, and a lot draws on the shed. Whatever the
# sale still cannot reach stays where it was, reported by section 7's
# `overflow_destroyed`.
#
# Not measured in the real engine yet: OFF is the default and promotion is a
# separate decision. OFF, `overflow_left` is `deficit - sum(forced)` and `lots`
# is untouched, so the champion theta decodes byte for byte
# (`tests/test_shed_overflow.py`).
OVERFLOW_GUARD_ON = True  # runtime: bank excess carried harvest before nightfall
# OVERFLOW3: also bank the PROJECTED night overflow (plan-simulated yields),
# en-route deposits with PASS slack. Runtime-only; OFF = V1 byte for byte.
OVERFLOW_GUARD_V2 = True  # SHIP_OG2 2026-09-22: promoted (OVERFLOW3 dev +5 ho +3 tape +1, gift-free)
# OVERFLOW4: value-priced deposit trips for the busy-to-dusk residue (displace a
# late job only when it is worth less than the units it saves). Runtime-only.
OVERFLOW_GUARD_V3 = True  # SHIP_OG3 2026-09-22: promoted (OVERFLOW4 dev +3 ho +2 tape +1, gift-free)
OVERFLOW_GUARD_V3_CUT = True  # V3 may also just cut a harvest into destruction (leave it ripe)
OVERFLOW_GUARD_V3_MIN_NET = 20.0  # coins: a trip must save more than it displaces by this much
OVERFLOW_GUARD_V3_DEFER_W = 0.5  # weight of units left ripe on the tile (sold a day later)
SHED_OVERFLOW_ON = False
# REVFIX1 B2 (2026-09-29, gpt-6-astra code reviews 1+2), PACK22: default ON = plan arrays byte-identical on 3,150 closed-loop dawns, build_day median 202 -> 135 ms.
PLAN_FASTPATH_ON = True  # NumPy build_day only: skip an all-empty relay's hire re-derive; stop ordinary admission at missed == 0

# ---- SHED_DEFICIT: the watering bonus the overflow projection forgets -------
#
# `SHED-CLIP` (2026-09-14) counted what the engine destroys at the shed door
# under B's shipped switches: **21.6 units a game-seat on the 68 band boards**
# (t +7.33), 15.4 of them at the nightly dump on days 14-28. The only planner
# guard against that dump is the forced sale below, and it sizes itself on
#
#     inflow = sum(where(covered & has_harv, view.t_yield, 0)) + ...
#
# -- the *pre-watering* yield, and deliberately so ("today's watering bonuses
# excluded", the comment at the block). But a chain that WATERS a tile before
# it HARVESTS it collects the bonus that same evening, and `plan.py` already
# spells the corrected quantity three times over -- `MELON_OPEN`'s `m_units`,
# `MIDDAY_PLACE_V2`'s `mv_units` and `BANK_BEFORE_LOT_ON`'s
# `bl_units = where(bank_mask & has_harv, view.t_yield + 2 * bl_w, 0)`, with
# `bl_w = any(chain_op == OP_WATER)` per tile. So `proj_eod` under-counts
# tonight's shed by two units per reached tile that waters and harvests on one
# chain, `deficit` comes out too small, and the difference is exactly what the
# night destroys.
#
# ON, `inflow` uses the SAME term those three blocks use and nothing else --
# `view.t_yield + 2 * has_water`, one boolean per tile off `d.chain_op`. No new
# heuristic, no new clamp: `deficit` is still `max(proj_eod - SHED_CAPACITY, 0)`
# (never negative), still gated off on the terminal day, and the forced sale
# still draws only on `spare = max(avail - s_qty, 0)`, so a bigger projection
# can never sell stock the day's tasks reserved.
#
# The trade the arm prices: the projection stops being conservative. Every day
# whose bonus does not actually land (the harvest the route misses, the water
# that was already spent) force-sells stock that did not need selling, at the
# day's cheapest marginal quote -- against ~1,272 coins (band) / 1,686 (ymg) of
# nightly clip at dawn quotes, minus the walk a deeper forced sale costs itself.
#
# OFF the expression is literally `view.t_yield`, so the champion theta decodes
# byte for byte (`tests/test_shed_deficit.py` pins the whole plan against a
# pristine `git archive HEAD src` tree).
SHED_DEFICIT_ON = False

# ---- CLIP_CAP: cap the day's carried harvest at the shed [SWITCH, SHIPPED] -
#
# The one route-side lever the shed-clip family left open, and the only one of
# the three the evidence supports. `_end_of_day` -> `_drop_inventories_to_shed`
# banks every unit's inventory into a 100-unit shed and DESTROYS the tail
# (`sim/eod.drop_inventories`). Measured on the shipped pair (LOT4@17 +
# SELL_SLOT_PRIORITY), 30 V45LEG boards, both the real engine and the real
# opponent tapes (`S/shedclip/census.py`, `report.py`):
#
#     clip                 17.80 u/board, 1,415 coins/board at the dawn quote
#     clipping nights       2.90 /board; on one, 104.9 u come home into ~98.8
#                           of room and 6.14 die
#     by item (u, coins)   WHEAT 7.13/281  MELON 2.43/420  CARROT 2.00/111
#                          STRAWBERRY 1.60/109  WOOL 1.60/322  FERT 1.43/37
#                          TOMATO 0.97/89  EGG 0.47/27  MILK 0.17/19
#
# The composition is the whole story. The walk is (unit, first-acquisition
# turn) ordered and the tail dies, so WHICH units die is an accident of the
# serpentine: the clip lands on 1.47 of the night's 11.8 units and takes their
# late, dear ranks. Price the same COUNT of units at the CHEAPEST the seat
# carried home that night and the clip costs **277 coins instead of 1,415** --
# a 1,138 coins/board ceiling that costs no labour at all. Re-ordering cannot
# reach it (inside the clipped units it is worth 212, inside the last unit 475:
# those units are carrying dear goods and little else), and neither can a
# deposit trip: `MIDDAY_DROP_ON` (-1,157) and `BANK_LOT = 2` (-1,257) both
# bought the room with the tail of the block.
#
# So take the ceiling from the other end. The shed's room is the scarce good;
# spend it on the dearest units. A HARVEST whose units the night will destroy
# is not worth its turn -- the yield stays on the tile and is harvested
# tomorrow (`sim/eod.refresh_plants` keeps `t_yield`; only a plant that already
# hit `CROP_MAX_YIELD` decays, and not before the day after) -- so the day's
# admitted harvest is capped at `CLIP_CAP_ROOM` units, **dearest first**:
#
#     unit price = price[crop] (crops) / price[product] (animals)
#     room       = CLIP_CAP_ROOM - one unit per COLLECT_FERT the day takes
#                  (18.80 u of the 104.9 that come home on a clipping night
#                  are collected fertilizer, and a cap blind to them sits at
#                  86 of 100 and never binds -- measured, first arm inert)
#     a tile is suppressed iff the harvests strictly ahead of it in that
#     order already fill the room; the tile that straddles the boundary is
#     KEPT, so the cap is a floor on the carry and never over-suppresses by
#     more than one tile's yield.
#
# What that buys is not the cheap units (they are deferred, not saved) but the
# room they were occupying: the melon and the wool that were dying behind
# 7.13 units of 39-coin wheat and 1.43 of 25-coin fertilizer now fit.
#
# Three costs the model does not carry, which is why this is an engine
# question and not a ledger one: a deferred harvest spends a turn tomorrow
# (though one HARVEST then lifts two days of yield), an ongoing crop at
# `CROP_MAX_YIELD` cannot bank tomorrow's fire, and a spent plant's `t_life`
# decay starts the day after it tops out. The cap only ever binds on the 2.9
# nights a season that overflow -- on every other day the admitted harvest is
# far under 100 units and not one expression changes.
#
# OFF nothing is computed: the three masks are the ones they always were, so
# the plan is byte-identical (`tests/test_shedclip.py`).
#
# SHIPPED 2026-09-17 as the second half of PUMPCLIP
# [docs/strategy/2026-09-17-stack1.md].  It is NOT shipped alone: the cell that
# was judged is `OPEN_PUMP_ON = False` AND `CLIP_CAP_ON = True` together, on top
# of `ENDROUTE_ON`, and the two are read as one arm because that is the only
# form they were ever measured in (PE vs E +391 t +3.01).  The read is 241
# held-out pinned-town boards -- the 169 of POOLED180 plus a FRESH 72 cut from
# our own live games at opponents 1,901-2,281 -- **+418 a board, se 130,
# t +3.22, ours +366, theirs -52**, and inside our own rating band the gain
# RISES with the opponent's rating (2,100-2,281 +596 t +2.23).  It misses the
# §115b +450 coin bar and it ships under the gift-free rule anyway: d > 0 at
# t >= 3 with the rival delta flat.  The honest counter-evidence is in the doc
# and is not small -- the 25-board engine class reads -5,258 on two tapes alone
# (drop them: +224) -- which is why the arm is a gene as well as a constant.
#
# TURNED BACK OFF 2026-09-18 by STACK5 [docs/strategy/2026-09-18-stack5.md].
# The counter-evidence above got its own board: on the 28 gated engine boards
# the CESR cell's ONE remaining bad board (topleg3 109888002 SpaTaro, -18,144)
# is this switch, since the same board is +124 under SPLIT alone.  Drop the cap
# and the class is **+738 se 118 t +6.26 with ZERO negative boards**, and the
# whole price of dropping it on the 241-board pooled read is +88 t +1.82 --
# i.e. the cap buys a fifth of a se on our own band and pays a blow-up against
# the 3,000+ seats we are climbing towards.  The column stays in `SWITCH_GENES`
# -- the catalogue rule is every SHIPPED switch, and a zero gene decodes to
# whatever this constant says -- so if the cap is ever wanted back, the search
# takes it back without a layout change.
CLIP_CAP_ON = False

#: Units of shed room the day's harvest may fill. The engine's `shedCapacity`
#: is the only number here: the measured night shed under the shipped lots is
#: 0.8 units (lot 3 and LOT4@17 clear it), so the room the haul comes home to
#: IS the capacity, and charging a margin against it would suppress harvests on
#: nights that fit.
CLIP_CAP_ROOM = int(spec.SHED_CAPACITY)

# ---- CLIP_CAP refinements: the three items SHED-CLIP left open [SWITCHES] ---
#
# `docs/strategy/2026-09-16-shedclip.md` §6. All three ride on `CLIP_CAP_ON`
# and are inert without it; all three are OFF and OFF is the shipped program.
#
# (a) THE TERMINAL DAY. `terminal = day > O.LAST_SHED_DAY` is day 29: there is
#     no `_end_of_day`, the shed is liquidated whole and nothing carried over
#     is worth protecting, so a cap there only forgoes a harvest the seat
#     would have sold. `SHED_DEFICIT_ON` gates itself on `terminal`; the cap
#     as shipped does not. ON, the whole CLIP_CAP block (the suppression and
#     the fertilizer skip below) stands down on the terminal day.
CLIP_CAP_TERMINAL_OFF = False

# (b) THE COLLECTIONS. Of the 104.9 units that come home on a clipping night
#     18.80 are FERTILIZER -- one per `COLLECT_FERT` -- and at 26 coins a unit
#     it is the cheapest thing in the haul, ahead of 173-coin melon. The
#     shipped cap CHARGES them to the room (`CLIP_CAP_ROOM - n_collect`) and
#     that correction is what made the switch live at all; it does not DROP
#     them. ON, on a night the haul overflows (`cc_binds`: harvest volume plus
#     collections over the room) the COLLECT_FERT ops are suppressed outright,
#     op and value together, and the harvest then competes for the whole room.
#     The risk the shipped comment records is engine-side: `FERTILIZE` takes
#     its unit from the acting unit's own inventory (`kaggriculture.py:478`),
#     so a route that fertilized out of the collect it stands on no-ops. The
#     planner's own `fert_avail` is `shed + bought` and never counted the
#     collections, so nothing plan-side double-books; the census measures the
#     rest.
CLIP_FERT_SKIP_ON = False

# (c) THE STRADDLE. The shipped rule suppresses a tile iff the harvests
#     STRICTLY ahead of it already fill the room, so the tile that straddles
#     the boundary is kept and the cap is a FLOOR on the carry -- which is why
#     6.17 u / 534 coins still die after it. ON, a tile whose own volume would
#     cross the room is suppressed too (a ceiling, never a floor). Note the
#     literal "cheapest-first deferral" of §6 is already what the shipped rule
#     does -- it ranks by unit price DESCENDING and the tail it cuts is the
#     cheapest yield -- so the residue, not the ordering, is what is left.
CLIP_CAP_STRICT_ON = False

# ---- LOT4: a fourth afternoon sell row [SWITCH, OFF] ------------------------
#
# The successor `SHED-CLIP` (2026-09-14) left untested and `SHED-DEFICIT`
# (same day) ranked first of what is still open: **"a row AFTER the harvest
# lands"**, bounded at the whole band nightfall clip, **1,272 coins**.
#
# THE LEAK. `SHED-CLIP` §2: under B's shipped switches our seat destroys 21.6
# units a game-seat on the 68 band boards (t +7.33), **15.4 of them at the
# nightly dump on days 14-28** (`sim/eod.py:210-247` -- whatever `room0 =
# max(SHED_CAPACITY - sum(shed), 0)` cannot take is zeroed). Both planner-side
# repairs to the *forced sale* are now measured zeros: `SHED_OVERFLOW_ON`
# recovers 0.10 units a board and `SHED_DEFICIT_ON` recovers -0.22, because
# both draw on `spare = max(avail - s_qty, 0)` -- hour-0 stock the first pass
# has already drained -- while the units that die are tonight's inflow.
#
# SO THE LEVER IS NOT A BIGGER ASK, IT IS ANOTHER ROW. Every unit the day sells
# is a unit of room at the dump, and the day sells only 0.65-0.87 of its dawn
# shed (`SHED-DEFICIT` §1). Three things hold the residue back and a fourth lot
# moves all three:
#
#   1. **The quote.** `SELL_TURNS = (3, 10, 18)`; a row at `LOT4_TURN` = 21 is
#      three more town ticks recovered (`projector.projected_inv`), so its
#      first unit quotes ABOVE lot 3's and units whose marginal fell short of
#      `hold` in lot 3 can clear it there.
#   2. **Lot depth.** A SELL walks its own quote down unit by unit, so the same
#      volume spread over four rows clears above the same volume in three --
#      the `LOT_SPLIT` mechanism without its cap, and it is free here because
#      the allocator prices the split itself (`sell.adjusted_marginals`'
#      externality term, which now runs over four lots and charges each early
#      unit what it costs the three behind it).
#   3. **Day 29.** The terminal `hold` is `SELL.LIQUIDATE`, so the whole shed
#      goes out; a fourth row divides that dump instead of deepening lot 1.
#
# It cannot reach the day's own harvest (that lands in the *hand* and reaches
# the shed only at `_end_of_day`), and that is not what it is for: it is for
# the room the harvest lands into.
#
# THE COST, priced honestly. Each extra resolved market turn is ~6% of
# simulator throughput (`ops.SELL_TURNS`' own comment, measured) -- so this
# switch is a **measurement** arm, not a free ride: promotion has to clear
# +450 pooled at t >= 2 on the band to be worth 6% of every future training
# run. And the row is not free in coins either: a unit moved from lot 1 to
# lot 4 is a unit the opponent may reach the pot before (`press`), which is
# exactly what `press * lot_ix` charges it.
#
# WHAT ON CHANGES, exhaustively. `early_lot_turns()` returns four turns instead
# of three; `n_lots()` follows it; `sell.allocate` reads its lot count off the
# projection it was handed (`inv_lots.shape[0]`) rather than off `sell.N_LOTS`;
# `sim/rollout` picks the fourth turn up at import, as it already does for
# `MELON_OPEN_ON` and `EARLY_SELL_ON`. Every "day's LAST lot" bulk add
# (`DROP_ON`, `MELON_OPEN`, `MIDDAY_PLACE_V2`, `SAME_DAY_FERT`,
# `ANIMAL_SAME_DAY`) follows `n_lots() - 1` to the new last row, which is
# strictly later than the deposit it sells and so still legal.
#
# OFF, `early_lot_turns()` is the tuple it was, `n_lots()` is 3, and every
# `arange` built off it is the `arange(SELL.N_LOTS)` it was, so the champion
# theta decodes byte for byte (`tests/test_lot4.py` pins the whole plan against
# a pristine `git archive HEAD src` tree).
#
# 2026-09-16 -- SHIPS ON, at `LOT4_TURN` = 17. `docs/strategy/2026-09-16-brv45.md`
# sect.5: the TURN was the whole switch, and it is not the afternoon turn this
# block was written for. The same row at 21 is -831 a board on the band and at
# 14 is +112; at 17 -- the one turn immediately IN FRONT of lot 3, carrying the
# same five town ticks (`ticks_before(17) == ticks_before(18) == 5`,
# `core/projector.py:174-184`) -- it splits the day's deepest lot (turn 18
# carries 497 of our 1,436 units at the day's best realised price) without
# giving up a single tick. The volume barely moves (+0.8 u); the realised price
# of our whole book goes 89.07 -> 89.34 and theirs falls 78.84 -> 78.82, so the
# row earns AND denies. Engine, paired, one variable, theta B `flow193_g100_hr`:
# 30 V45LEG boards +861 (t +5.08, board win 53.3 -> 63.3 %, 3 flips all to us),
# 68 band +689 (t +9.82), and **POOLED180 +791 on 169 boards / 338 games, se 60,
# t +13.19, 16 net outcome flips and not one against us** -- sect.115b PASS. Both
# sect.115 vetoes clear with room (TOPB2 +532, LIVE62 +604) and nothing is
# negative anywhere (ENG22 +303, NEXTHIGH +668, LOSS10 +886, TOPB3R9 +246).
# The row still costs ~6 % of simulator throughput for every future training
# run; that price is now knowingly paid.
LOT4_ON = True

#: The turn the fourth lot stands on [SWITCH, LOT4]. 17 = engine hour 18, and
#: it is NOT behind the last shipped lot: it stands immediately IN FRONT of it.
#: `early_lot_turns()` merges it in time order, so the day's rows are
#: (3, 10, 17, 18), the lot index is still the timing-pressure rank, and every
#: "day's LAST lot" bulk add -- which names `n_lots() - 1` -- still lands on
#: turn 18, exactly where it landed before the switch. 17 is the LATEST turn
#: that keeps lot 3's town ticks (`ticks_before(17) == ticks_before(18) == 5`,
#: `core/projector.py:174-184`), which is why it splits the day's deepest lot
#: for free, and it collides with no row the day already uses.
#: Swept paired on the band: 13 +115, 14 +112, **17 +689 (t +9.82)**, 21 -831
#: (`docs/strategy/2026-09-16-brv45.md` sect.5.1, `2026-09-16-lot4.md`); 15, 16
#: and 19 are untested, so the optimum inside 14-18 is bounded, not located.
#: Any turn in [`O.FULL_MARKET_TURNS`, `spec.TURNS_PER_DAY`) that no other row
#: uses is legal, later is more room and more `press`, and the asserts below
#: are the whole legality rule.
LOT4_TURN = 17

assert O.FULL_MARKET_TURNS <= LOT4_TURN < spec.TURNS_PER_DAY, \
    "the fourth lot takes the sell-only market path, and it is inside the day"
assert O.SELL_TURNS[0] < LOT4_TURN, \
    "the fourth lot is an AFTERNOON row, not a second opening one: it stands\
 after the day's first lot. 2026-09-16 the DEFAULT moved from 21 (behind the\
 last shipped lot, -831 a board) to 17 (immediately in front of it, +689), so\
 either side of `O.SELL_TURNS[-1]` is legal -- `early_lot_turns()` merges\
 whatever a runner sweeps in turn order"
assert LOT4_TURN not in (set(O.SELL_TURNS) | set(O.MELON_LOT_TURNS)
                         | set(O.EARLY_SELL_LATE_TURNS) | {O.TURN_PRESTOCK}), \
    "the fourth lot must not collide with a turn the day already uses"

# ---- SHED_DUMP_ROW: the hour-23 overflow row [SWITCH, OFF] ------------------
#
# The public V45 notebook's `_r148_overflow` (`docs/strategy/2026-09-16-v45-
# notebook.md` sect.2.5 item 4, sect."the three worth testing" item 2), re-derived
# here rather than copied. Their rule, stated in their own source: at hour 23
# every unit's carried inventory is pushed into the shed and the part that does
# not fit is destroyed IN DEPOSIT ORDER, so they sell -- on that same hour 23 --
# exactly the shed units the doomed suffix would replace. The post-dawn shed
# vector is then what it would have been and the doomed units have become cash.
#
# WHY IT IS NOT `LOT4` (2026-09-16-lot4.md, turns 14 and 21, REJECTED at margin
# -831 / +112). LOT4 is a fourth *lot*: a price-driven row that offers whatever
# the allocator's marginal clears, on EVERY day of the season, and it moved
# volume between rows without recovering units (0.07 of 15.4). This row offers
# NOTHING on a day the projection says the deposit fits, and on a day it does
# not fit it offers exactly the overflow -- an amount, not a price.
#
# THE SIZE. `SHED-CLIP` sect.2: 15.4 units a game-seat die at the nightly dump on
# days 14-28 of the 68 band boards, ~1,272 coins at dawn quotes. `overflow_left`
# -- what the forced sale (0.9) and `SHED_OVERFLOW_ON` together could not absorb
# -- is the planner's own estimate of that number, day by day, and it is already
# reported as `DayStats.overflow_destroyed`.
#
# THE SOURCE, and the honest doubt. A market SELL draws on the SHED, and tonight's
# harvest is in the crew's HANDS until `eod.drop_inventories` runs, so this row
# cannot sell the doomed units themselves: it sells the stock standing in the shed
# at hour 23 to make the room they land in. That stock is `shed - the pickups the
# route actually made - everything the day has already offered`, which is
# `SHED_OVERFLOW_ON`'s `spare` net of the bulk adds -- and `SHED_OVERFLOW_ON`
# measured that purse at 0.10 units a board. What this row adds over it is the
# TURN: five more shop ticks of restocked shelf, and a row that stands after the
# day's own tasks have consumed their reservations. If the shed is empty at hour
# 23 the row is a measured zero and the family closes.
#
# WHAT ON CHANGES, exhaustively. `_plan_and_stats` computes `dump` (int[9]) after
# the forced sale and after `SHED_OVERFLOW_ON`'s continuation; `_market` emits it
# on `SHED_DUMP_ROW_TURN` in the same nine product slots every other SELL row
# uses (so both seats still present one layout, `sim/market.py`'s
# `assert_no_cross`); `sim/rollout` picks the turn up at import, as it already
# does for `LOT4_ON` and `MELON_OPEN_ON`. `lots`, `s_qty`, the reservation gate
# and every bulk add are untouched -- this row is strictly additional volume, and
# only on a day the projection says would otherwise destroy it.
#
# OFF, `dump` is `None`, `_market` emits the rows it always emitted and
# `rollout.MARKET_TURNS` is the six turns it always resolved, so the champion
# theta decodes byte for byte (`tests/test_shed_dump.py` pins the whole plan
# against a pristine `git archive HEAD src` tree).
SHED_DUMP_ROW_ON = False

#: The turn the overflow row stands on [SWITCH, SHED_DUMP_ROW]. 23 = the LAST
#: turn of the day (`spec.TURNS_PER_DAY` = 24), so its market resolves with the
#: day's route finished -- every pickup made, every FEED spent -- and immediately
#: before `end_of_day` empties the hands into the shed. Any earlier turn is a
#: `LOT4` (already measured) rather than the dump row.
SHED_DUMP_ROW_TURN = 23

#: Draw the room from the CHEAPEST product first [SWITCH, SHED_DUMP_ROW]. The
#: room is fungible -- one unit of any product is one unit of room -- so the
#: units given up should be the ones cheapest to hold, ranked on the same
#: projected marginal quote the forced sale ranks on. False sells the dearest
#: first, which is the V45 rule read literally ("highest-price-first", their
#: room guard at 1110) and is here only so the sweep can price both.
SHED_DUMP_ROW_CHEAP_FIRST = True

assert O.FULL_MARKET_TURNS <= SHED_DUMP_ROW_TURN < spec.TURNS_PER_DAY, \
    "the overflow row takes the sell-only market path, and it is inside the day"
assert O.SELL_TURNS[-1] < SHED_DUMP_ROW_TURN, \
    "the overflow row stands after the day's last lot: it sells the residue the\
 lots left, not volume the allocator wanted earlier"
assert SHED_DUMP_ROW_TURN not in (set(O.SELL_TURNS) | set(O.MELON_LOT_TURNS)
                                  | set(O.EARLY_SELL_LATE_TURNS)
                                  | {O.TURN_PRESTOCK}), \
    "the overflow row must not collide with a turn the day already uses"

# ---- ENDROUTE: the terminal day's LAST executed row [SWITCH, SHIPPED] -----
#
# WHAT IT IS.  One extra SELL row, on day 29 only, on the last turn the engine
# executes, offering every product without reservation.
#
# THE MEASUREMENT (`S/dropharv/measure.py`, 24 TOPLEG2 leaderboard-top-10
# boards, shipped FT2 theta + the 6 shipped switches, real engine).  The coin
# left on the table over d27-d29 is 431 a board and it is THREE buckets:
#
#   A  futile late work      0.0  -- FT2 never plants a crop that cannot ripen
#                                    and never buys a seed or an animal that
#                                    cannot mature.  The "stop planting when
#                                    days_left < grow time" half of the
#                                    hypothesis is a MEASURED NO-OP: the
#                                    terminal law already does it.
#   B  stock unsold at end 289.6  -- 9.8 units a board, and essentially ALL of
#                                    it FERTILIZER.
#   C  ripe tiles at end   141.1  -- 3.3 units a board left standing.
#   D  shed-overflow loss    0.0  -- nothing dies at the d27-29 dumps.
#
# WHY B SURVIVES, exactly.  The terminal `hold` is `SELL.LIQUIDATE`, so day 29's
# three lots do liquidate -- but they are sized off the **dawn** shed (plus, in
# the day's last lot, the animal harvest `DROP_ON`'s route will bank).  Day 29
# then runs 10.4 COLLECT_FERTILIZER ops and DROPs them into the shed after
# `SELL_TURNS[-1]`.  FERTILIZER is not an `ANIMAL_PRODUCT`, so no lot ever
# offers it, and its terminal value is exactly zero [LAW, 0.4].
#
# THE TURN.  `ENDROUTE_TURN` is 22, not 23: the episode is `episodeSteps` 720
# and step 718 -- day 29 turn 22 -- is the LAST executed one, so a turn-23 row
# would never resolve.  It is also the hour the engine class itself liquidates
# on (`2026-09-17-endsell.md` sect.2: d29 WHEAT and CARROT both median h22).
#
# THE ASK.  `ENDROUTE_ASK` units of every product, flat.  Over-asking is free
# and is what the rest of this section already does: a SELL is clipped to the
# shed unit by unit in the engine (`_commit_unit`) and in the simulator
# (`market._inventory_orders`), a slot with nothing behind it simply does not
# fill, and on day 29 there is no later lot for an over-ask to starve and no
# tomorrow for the quote it walks down.  So the row cannot take a coin off any
# earlier row; it can only convert residue.
#
# SEAT-SYMMETRIC: it is the same nine product slots in the same order as every
# other SELL row, so both seats still present one layout (`sim/market.py`'s
# `assert_no_cross`), and it is emitted from the shared planner, so either seat
# plays it.
#
# WHAT IT DOES NOT REACH: bucket C.  A ripe tile at the end needs HARVEST ->
# walk -> DROP -> SELL, i.e. a route change on day 29, not a row.  This switch
# monetises whatever the route DOES bank and nothing else.
#
# OFF, `endrow` is `None`, `_market` emits the rows it always emitted and
# `rollout.MARKET_TURNS` is the set it always resolved, so the champion theta
# decodes byte for byte (`tests/test_endroute.py` pins the whole plan on five
# boards against a pristine `git archive` tree).
#
# SHIPPED 2026-09-17 [docs/strategy/2026-09-17-dropharv.md sect.6].  POOLED180
# on the shipped FT2 package (169 held-out pinned-town boards, both seats) is the
# read that promoted it, under the gift-free ship rule the lead set for small
# arms ("each coin helps to win"): a positive pooled margin at t >= 3 whose
# rival-purse delta is zero.  It is also a gene, `SWITCH_GENES[10]`,
# so the search can take it back off on a board where it is not worth the row.
ENDROUTE_ON = True

#: The turn the terminal row stands on [SWITCH, ENDROUTE]. 22 = day 29's last
#: EXECUTED turn (step 718 of `episodeSteps` 720). Anything later never runs.
ENDROUTE_TURN = 22

#: Units of each product the terminal row offers [SWITCH, ENDROUTE]. The shed
#: cap is the most that can ever stand there, so this asks for all of it; the
#: engine clips every slot to the stock actually held.
ENDROUTE_ASK = int(spec.SHED_CAPACITY)

assert O.SELL_TURNS[-1] < ENDROUTE_TURN < spec.TURNS_PER_DAY - 1, \
    "the terminal row stands after the day's last lot and on a turn that RUNS"
assert ENDROUTE_TURN not in (set(O.SELL_TURNS) | set(O.MELON_LOT_TURNS)
                             | set(O.EARLY_SELL_LATE_TURNS)
                             | {O.TURN_PRESTOCK, SHED_DUMP_ROW_TURN}), \
    "the terminal row must not collide with a turn the day already uses"

# ---- ENDROUTE_ROW2: the terminal day's SECOND late row [SWITCH, OFF] --------
#
# WHAT IS LEFT, MEASURED (`S/endfamily/run_ledger.sh`, the SPLIT cell, 24+24
# engine-class boards).  Under `ENDROUTE2_SPLIT_ON` the end-of-game residue is
# 0.0 coins a board on TOPLEG2 and 6.0 on TOPLEG3 -- the 431-coin DROPHARV
# ceiling is fully banked.  What the same census shows instead is DEPTH: at day
# 29 turn 22 the crew still CARRIES 1,250-1,565 coins of produce (wheat 12-15
# units, carrot 4-7, fertilizer 3-5 ...), and all of it lands in the shed and is
# sold through ONE row, `ENDROUTE_TURN`.  Nine slots, one turn, one walk down
# the quote: the last lot of the game is the deepest lot of the game.
#
# THE ROW.  A second flat ask on `ENDROUTE_ROW2_TURN`, day 29 only, built and
# emitted exactly like `endrow` (same nine product slots, same order, same
# `ENDROUTE_ASK`, seat-symmetric).  It sells whatever the SECOND trip has
# already DROPped by then, so the turn-22 row meets a shallower shed and both
# rows trade nearer the top of the book.  It is an amount, not a price, and it
# stands after the day's last lot, so it can take nothing off any earlier row.
#
# REQUIRES `ENDROUTE_ON`: without the turn-22 row there is no second trip to
# split, and a row between the last lot and the end of the day on its own is a
# `LOT4` (already measured, `2026-09-17-cliptop.md`).
#
# OFF, `endrow2` is `None`, `_market` emits the rows it always emitted and
# `rollout.MARKET_TURNS` is the set it always resolved, so the champion theta
# decodes byte for byte (`tests/test_endroute_row2.py`).
#
# SHIPPED 2026-09-18 as the fourth member of the ESR cell
# [docs/strategy/2026-09-18-stack5.md], never alone.  The increment this row
# buys over the SPLIT cell is +133 a board on POOLED169 at t +6.05, theirs -40
# [2026-09-18-endfamily.md], and as one cell with `ENDROUTE_ON`,
# `ENDROUTE2_ON` and `ENDROUTE2_SPLIT_ON` on the pump-ON, cap-OFF tree it reads
# **+477 a board, t +13.5, on the 241 held-out pinned-town boards vs FT2** and
# **+738 se 118 t +6.26 on the 28 gated engine boards with zero negatives**.
#
# [SWITCH-GENE] Column 15 of `plan.SWITCH_GENES` per the catalogue rule (USER
# 2026-09-17: the gene block carries EVERY shipped switch).  Its dependency on
# `ENDROUTE_ON` is enforced in the VALUE by `_sw_all`, not by the module assert
# below -- the ES draws all sixteen columns independently, and a draw that
# takes the first terminal row away has to take this one with it instead of
# raising.
ENDROUTE_ROW2_ON = True

#: The turn the second terminal row stands on [SWITCH, ENDROUTE_ROW2]. Strictly
#: between the day's last lot (18) and `ENDROUTE_TURN` (22), so the day keeps
#: its lot order and the last row is still the last one. 19 and 21 are the only
#: free turns there -- 20 is `O.TURN_PRESTOCK` and 23 is the dump row -- and 21
#: is the one the second trip's DROPs have mostly landed by.
ENDROUTE_ROW2_TURN = 21

assert not ENDROUTE_ROW2_ON or ENDROUTE_ON, \
    "the second terminal row splits ENDROUTE's row; without it there is none"
assert O.SELL_TURNS[-1] < ENDROUTE_ROW2_TURN < ENDROUTE_TURN, \
    "the second row stands after the day's last lot and before the last row"
assert ENDROUTE_ROW2_TURN not in (set(O.SELL_TURNS) | set(O.MELON_LOT_TURNS)
                                  | set(O.EARLY_SELL_LATE_TURNS)
                                  | {O.TURN_PRESTOCK, SHED_DUMP_ROW_TURN}), \
    "the second terminal row must not collide with a turn the day already uses"

# ---- ENDROUTE2: the terminal day's turn budget, re-cut to the new row [OFF] --
#
# WHAT IS LEFT.  With `ENDROUTE_ON` the end-of-game residue is measured
# (`S/endroute2/measure2.py`, the same 24 TOPLEG2 boards, real engine) at
#
#   shed  @ end     0.0   -- the terminal row clears the shed to the coin
#   hands @ end     0.0   -- nothing dies in a worker's hands
#   ripe PLANT      103.3 -- 2.2 units (wheat 1.29, carrot 0.71, straw 0.17)
#   ripe ANIMAL      37.8 -- 1.1 units (egg 0.58, wool 0.29, milk 0.25)
#   ------------------------------------------------------------------
#   TOTAL           141.1 coins a board, ALL of it standing on tiles,
#
# and every unit of it is already ripe at day 29's turn 22, so it is reachable
# by a route and by nothing else.  Day 29 also has 53.4 PASS unit-turns.
#
# WHY THE TURNS ARE IDLE, exactly.  `drop_turns` / `turn_budget` cut the
# terminal day at `O.SELL_TURNS[-1] + 1`: a DROP later than turn 18 had no lot
# left to sell into, so the six turns after it were worth nothing and the admit
# stage was told not to spend them.  `ENDROUTE_ON` is precisely a lot later than
# turn 18.  Once that row exists the same reasoning ends the day at
# `ENDROUTE_TURN + 1` instead, which is +4 turns for every unit -- and 53.4 PASS
# turns is about (23 - 18) x the crew, i.e. exactly the slack this frees.
#
# WHAT IT IS, THEREFORE: no new op, no new row, no new task and no new value
# term.  One constant in two places -- the hire enumeration's `per_unit` and the
# day's `turn_budget` -- and only on the TERMINAL day.  The extra budget admits
# a longer prefix of the value order the planner already built, `_routes` cuts
# the blocks against it exactly as it always did, and the DROP still lands
# before its turn's market phase (units act first, `interpreter`), now at turn
# 22 at worst instead of turn 18 at worst.  Day 28 does not move: the gate is
# `terminal`, not `drop_day`, so `MIDDAY_DROP_ON`'s extra DROP day -- which has
# a tomorrow and an end-of-day -- keeps the budget it always had.
#
# IT REQUIRES THE ROW.  Without `ENDROUTE_ON` the turns past 18 bank produce no
# lot can sell, which is a straight loss of the walk; the assert below refuses
# the combination rather than measuring it.
#
# OFF, both expressions are the ones they were, so the champion decodes byte for
# byte (`tests/test_endroute2.py`).
#
# SHIPPED 2026-09-18 inside PES [docs/strategy/2026-09-18-stack3.md].  It is NOT
# shipped alone -- on its own it read POOLED180 +136 se 47 t +2.92, under the
# t >= 3 bar, and the doc left the switch OFF for exactly that.  What ships is
# the CELL: `OPEN_PUMP_ON=False`, `CLIP_CAP_ON`, `ENDROUTE_ON`, `ENDROUTE2_ON`,
# `ENDROUTE2_SPLIT_ON` together, read on 241 held-out pinned-town boards at
# **+638 a board, t +4.93 vs the shipped E** (POOLED169 +733 t +4.68, vs FT2
# +759 t +4.85) -- the first cell of this family to clear the sect.115b +450
# coin bar.  The turns this switch buys are worth nothing without SPLIT's
# second trip to spend them on, which is why the two are one arm.
ENDROUTE2_ON = True

assert not ENDROUTE2_ON or (ENDROUTE_ON and DROP_ON), \
    "ENDROUTE2 spends turns into ENDROUTE's row; without it they bank nothing"

# ---- ENDROUTE2_SPLIT: two trips on day 29, the first one on time [OFF] ------
#
# WHAT ENDROUTE2 COSTS, MEASURED (`2026-09-17-endroute2.md` sect.5-7).  The extra
# turns are worth +272 a board to us, and hand the rival +161: the trace says
# why, and it is not produce.  `ENDROUTE_ON` alone lands day 29's one DROP by
# turn 18, so the whole load sells on lot 3 (engine hour 19) and CRUSHES the
# quote -- STRAWBERRY 103 -> 87, WHEAT 44 -> 42 -- underneath the engine-class
# rival's own h21/h22 sells.  `ENDROUTE2_ON` pushes that same DROP to turn
# 22-23, so at h19 the quote barely moves, the rival sells into an undepressed
# market and banks +46/+441 (109831304) and +82/+398 (109826302).  We buy +272
# of produce and sell back the price denial we used to give away for free.
#
# WHAT THIS IS.  Both, by splitting the terminal day's route into TWO shed
# trips instead of moving the one it had:
#
#   1. the mid-block deposit `BANK_BEFORE_LOT_ON` already builds -- walk to the
#      nearest shed access, DROP, walk back -- fired on the TERMINAL day, with
#      its deadline re-cut from `O.SELL_TURNS[BANK_LOT]` to
#      `ENDROUTE2_SPLIT_TURN` (the day's LAST lot, turn 18).  That is the h19
#      dump, kept at its hour;
#   2. the block then spends `ENDROUTE2_ON`'s four extra turns on the ripe
#      tiles behind it and ends in its ordinary return leg, whose DROP now
#      lands at turn 22 at worst -- `ENDROUTE_ON`'s row, i.e. a SECOND sell of
#      the late harvest alone.
#
# So the split is exactly variant (b) of the ask: the excursion pays the round
# trip (`2 * DIST_SHED + 1`) where the one-way return leg paid `DIST_SHED + 1`,
# so the ranks in front of the deposit are a shorter prefix than `ENDROUTE_ON`
# alone would have taken -- the h19 lot is fed by what is reachable in time and
# the rest sells at 22.  No new op, no new row, no new task: the deposit is the
# shipped `BANK_BEFORE_LOT` excursion and the second sell is `ENDROUTE`'s row.
#
# THE LOTS NEED NOTHING.  `DROP_ON` already adds the block's whole banked yield
# to the day's LAST lot (`gain`, the `last_lot` row) and over-asking is free --
# every SELL is clipped to the shed unit by unit in the engine (`_commit_unit`)
# and the simulator (`market._inventory_orders`).  So lot 3 already offers what
# the excursion deposits, and `BANK_BEFORE_LOT`'s own `bl_gain` -- which adds
# to `BANK_LOT` (lot 2, turn 10) -- is gated OFF on the terminal day, where it
# would only pull the dawn shed forward onto an earlier row.
#
# REQUIRES both halves: `ENDROUTE2_ON` for the turns the second trip spends and
# `ENDROUTE_ON` for the row it sells into, plus the excursion machinery itself.
#
# OFF, `bank_day` is `~terminal & ~drop_day`, the deadline is the Python int it
# was and `bl_gain` is unmasked, so the champion decodes byte for byte
# (`tests/test_endroute2_split.py`).
#
# SHIPPED 2026-09-18 as the other half of the route stack in PES
# [docs/strategy/2026-09-18-stack3.md].  SPLIT alone read +348 t +9.83 -- the
# tightest arm in the family and still 102 coins under the sect.115b bar -- and
# the cell it ships in reads +638 t +4.93 on 241 boards, theirs +89.  The 28
# engine-class boards are neutral (-511 t -0.12) and that whole number is
# PUMPCLIP's two topleg3 tapes; without them the class is +379.  The knobs
# below are the judged ones, unswept and unmoved.
ENDROUTE2_SPLIT_ON = True

#: The turn the terminal day's FIRST deposit must land on or before [SWITCH,
#: ENDROUTE2_SPLIT]. `O.SELL_TURNS[-1]` is the day's last lot and a unit acts
#: before its turn's market, so a DROP on turn 18 itself still sells at h19.
#: Sweepable: a smaller value moves the first dump to an earlier lot.
ENDROUTE2_SPLIT_TURN = O.SELL_TURNS[-1]

#: `BANK_MIN_VALUE` / `BANK_MAX_TURNS` on the terminal day alone [SWITCH,
#: ENDROUTE2_SPLIT]. The shipped pair was tuned for a day whose block ends at
#: the shed anyway; day 29's deposit is the price-denial dump itself, so the
#: value floor is worth sweeping down and the leg budget up.
ENDROUTE2_SPLIT_MIN_VALUE = 400
ENDROUTE2_SPLIT_MAX_TURNS = 9

assert not ENDROUTE2_SPLIT_ON or (ENDROUTE2_ON and ENDROUTE_ON and DROP_ON), \
    "ENDROUTE2_SPLIT is ENDROUTE2's turns spent through BANK_BEFORE_LOT's leg"
assert O.SELL_TURNS[0] <= ENDROUTE2_SPLIT_TURN <= O.SELL_TURNS[-1], \
    "the first dump has to land on a lot the day actually sells"

# ---- SELL_SPREAD: a flat per-day quota over the last days [SWITCH, OFF]
#
# MAJKEL1 (`docs/strategy/2026-09-19-majkel1.md`).  Majkel1337 (3,279) and
# ymg_aq (3,077) play the SAME d0-5 plate; the clean +1,304 of wheat between
# them is not volume but SHAPE -- he sells 13-19 units *every* day d19-24 at
# ~35 while ymg holds and dumps 235 units into d25-29 at 21-30.  Every product
# quotes off a monotone curve in market inventory (`spec.MARKET_ROWS`) and the
# town tick refills it overnight, so N units spread over k days clear strictly
# above the same N units through one row -- the same depth bill LOT_SPLIT
# prices inside a day, read ACROSS days.
#
# THE SWITCH.  From `SELL_SPREAD_DAY0` the day's VOLUNTARY sale of each product
# in `SELL_SPREAD_ITEMS` may draw on at most `max(stock // days_left,
# SELL_SPREAD_MIN)` units, where `days_left = SELL_SPREAD_END - day + 1`
# counts today.  It is a cap on `avail`, i.e. on what `SELL.allocate` is
# greedy over, and not a reservation: the allocator's `hold` still decides
# whether a unit inside the quota is worth selling at all, so a day whose
# quotes are under the reservation still sells nothing.
#
# WHAT IT IS NOT.  LOTDEPTH (`docs/strategy/2026-09-18` BUILD-STORY) rejected
# selling EARLIER inside the day (-1,981): a hand holds harvest until the dusk
# shed drop and the day's sale is cut once at dawn.  This moves no hour -- the
# lots stay on `early_lot_turns()` -- it only refuses to put the whole standing
# stock on today's curve.  The terminal day is exempt by construction
# (`days_left == 1` there, and the call site is gated on `~terminal` besides),
# so the ENDROUTE / ENDROUTE2 / ENDROUTE2_SPLIT / ENDROUTE_ROW2 family, which
# is entirely day 29, is untouched and the residue law still holds.
#
# NOT A GENE.  `SWITCH_GENES` is 18 wide and the shipped layout is 7,692
# floats; appending a 19th column is a layout change every trained theta would
# have to be re-padded against, so this switch is flown by module override
# (`S/drainpin/on2b.py`, `SW_EXTRA=,SELL_SPREAD_ON=1`) only.
SELL_SPREAD_ON = False
#: The first day the quota binds.  19 is Majkel's own first stream day.
SELL_SPREAD_DAY0 = 19
#: The last day the quota counts toward -- the terminal day, where
#: `days_left == 1` and the cap is the whole stock.
SELL_SPREAD_END = O.LAST_SHED_DAY + 1
#: The floor under the quota: below this a "stream" is one unit a day into a
#: curve that has not moved, which is worth less than the row it costs.
SELL_SPREAD_MIN = 12
#: The products the quota is read on.  WHEAT is the measured +1,304;
#: STRAWBERRY is the same code path and Majkel's largest line (+3,160).
SELL_SPREAD_ITEMS = (spec.I_WHEAT, spec.I_STRAWBERRY)

assert 0 <= SELL_SPREAD_DAY0 <= SELL_SPREAD_END, "the window has to have days"
assert SELL_SPREAD_MIN >= 0, "a negative floor is not a floor"

# ---- MELON_OPEN: the recorded top-tier opening, planner-native [SWITCH, OFF]
#
# MELON is the one product with a squared glut curve (`spec.MARKET_ROWS`:
# `above_func="sq"`, `above_target=3.60`, T=300) and a season town drain of 30
# units, so the first seat to reach the market on the day melon saturates books
# its crop at 240+ a unit and every unit behind it meets a curve that never
# refills.  The 2800-tier tapes all play that race; our shipped planner does
# not plant melon on day 0 at all (`brain.decide`'s grow score is a trained
# weight, not an expression), and its melon reaches a lot on day 14.
#
# `MELON_FIRST` v1/v2 (branch `flow69-melon-split`) named the opening and lost
# 17,477 coins a game.  The replay diagnosis that followed
# (`scratchpad/open_vs_melon/report.md`, 4 arms x 8 real-engine games, one of
# them a recorded top-tier opening spliced in front of this very planner) is
# what this switch is built from, and it is worth restating because it inverts
# the objective:
#
#   * the recorded opening wins **+26,722** a game against kagg2 where v2 with
#     the *same twelve melons on day 0* loses 18,626;
#   * our own final coins are **worse** under the winning opening (98,955
#     against 106,016). What it buys is 24,807 coins off the opponent, through
#     the quotes our earlier and larger supply sets.  The scoreboard for an
#     opening is our units sold by day and the quote the opponent meets, never
#     our revenue;
#   * kagg2's first melon lot is day 10 **hour 17** in 8/8 games of every arm.
#     The tape sells 60 melons in six lots at hours 10-16, all of them in front
#     of it; v2 sold one 84-unit line at hour 19, two hours behind, and in 6/8
#     games missed day 10 altogether;
#   * v2's day 0 bought `0 WHEAT + 7 CARROT + 12 MELON`. The tape's is
#     `7 WHEAT + 12 MELON`. `_melon_first` paid the melon debt in crop order
#     and WHEAT is the first crop, so the opening wiped out the animal feed and
#     the four-day rotation: 0 wheat tiles on days 1-2, 0 hires on day 1;
#   * v2's day 10 was 224 of 267 unit-turns PASS, because it forced the whole
#     crew onto the DROP-day route (`turn_budget` cut to `SELL_TURNS[-1] + 1`)
#     to get the crop to the day's *last* lot.
#
# So this switch is four quantities and one mechanism, and nothing else:
#
#   1. **Day 0 buys `MELON_OPEN_TILES` melon and protects the wheat.**
#      `_melon_open` rewrites `macro.plant_target` exactly as `_melon_first`
#      did -- melon raised to `min(tiles, plant_total)`, the total preserved --
#      but the debt is paid in `_MELON_PAY_RANK` order, which is crop order
#      with WHEAT moved to the *back*. On the shipped day-0 mix
#      (10 WHEAT + 9 CARROT) that is the tape's split to the tile: carrot pays
#      nine, wheat pays three, and the day plants 7 WHEAT + 12 MELON.
#   2. **The seed clip sees melon and wheat first.** `seed_cap` clips the seed
#      want prefix-wise in crop order and the day over-asks by two tiles, so
#      the two crops the opening is built around are exactly the ones the clip
#      would drop. Same `_MELON_SEED_RANK` permutation, melon in front.
#   3. **The melon goes on the tiles nearest a shed access** (`_rank_near` on
#      `DIST_SHED`, the key `compact` itself buckets on). v1's melon sat at the
#      far end of the serpentine and its day-10 harvest rode home in the hands'
#      inventories; near the shed the return leg is one or two turns.
#   4. **The dump day banks its melon mid-day and sells it in lots of at most
#      `MELON_OPEN_LOT` before the opponent's hour-17 dump.** This is the
#      mechanism v2 did not have. `_routes` gains a per-unit *excursion*: a
#      block that harvests melon on `MELON_OPEN_HARVEST_DAY` walks to its
#      nearest shed access after its last melon tile, DROPs, walks back and
#      **carries on with the rest of its block**. The day keeps its full
#      `turn_budget`; what the excursion costs is `2 * DIST_SHED + 1` turns of
#      that block and nothing else. It is the "second block per unit" the
#      `MIDDAY_DROP_ON` post-mortem named as the thing a future attempt would
#      have to build, in the one shape that pays for it -- a block whose crop
#      is worth more before hour 17 than the tail of the day is worth.
#      `ops.MELON_LOT_TURNS` are the lots that meet it: melon-only rows, empty
#      on every other day of the season, on the turns whose engine hours are
#      still in front of the opponent's.
#
# What is deliberately *not* in it: no forced DROP day, no `cash_reserve` or
# `crew_target` override, no change to the d10-13 spend. The ramp is the second
# half of the diagnosis and it is a separate switch.
#
# OFF, `_melon_open` is never called, `before` is the cumsum it always was,
# `plant_crop` is the crop-order boundary it always was, `_routes` compiles no
# excursion and `_market` emits no melon row, so the champion theta decodes
# byte for byte (`tests/test_melon_open.py`).
MELON_OPEN_ON = False

#: Move the dump day's three melon rows to `MELON_LOT_EARLY_TURNS` [SWITCH].
#: `ops.MELON_LOT_TURNS = (11, 13, 15)` are engine hours 12/14/16 -- in front
#: of the 2800-tier opponent's hour-17 dump, but mid-pack inside the top-10
#: tapes' own h9-19 window (`scratchpad/blueprint/report.md`: they sell the
#: same 72 melon units on day 10 hours 9-19, we sell ours on days 14-17). The
#: melon curve is squared and never refills, so whoever walks it first takes
#: the pot; (6, 7, 8) are hours 7/8/9, in front of the whole window.
#: Read only when `MELON_OPEN_ON` -- OFF there is no melon row to move.
MELON_LOT_EARLY_ON = False

#: The turns that switch stands the three lots on. Same three-lot shape as
#: `ops.MELON_LOT_TURNS` (`_market` stacks one lot per turn), and it satisfies
#: the same layout law `ops._check_schedule` asserts for the shipped tuple --
#: restated here because `ops` cannot read `plan`.
MELON_LOT_EARLY_TURNS = (6, 7, 8)

assert len(MELON_LOT_EARLY_TURNS) == len(O.MELON_LOT_TURNS), \
    "the early melon lots are the same three lots, on earlier turns"
assert O.FULL_MARKET_TURNS <= min(MELON_LOT_EARLY_TURNS), \
    "every melon lot takes the sell-only market path"
assert max(MELON_LOT_EARLY_TURNS) < O.SELL_TURNS[-1], \
    "a melon lot that is not in front of the last lot is not a melon lot"
assert not (set(MELON_LOT_EARLY_TURNS)
            & (set(O.SELL_TURNS) | set(O.EARLY_SELL_LATE_TURNS)
               | {O.TURN_PRESTOCK})), \
    "a melon lot must not collide with a turn the day already uses"


def melon_lot_turns():
    """The turns the dump day's melon rows stand on [SWITCH].

    One reader for `_market`, `_midday_place_turn` and `sim/rollout`, called at
    trace time so a runner that flips `MELON_LOT_EARLY_ON` after import (the
    campaign harness sets plan attributes with `setattr`) is seen by the
    planner. `ops.MELON_LOT_TURNS` is the shipped layout and the OFF value.
    """
    if MELON_LOT_EARLY_ON:
        return tuple(MELON_LOT_EARLY_TURNS)
    return tuple(O.MELON_LOT_TURNS)


#: Tiles the opening hands MELON. Twelve is the recorded opening's number and
#: the opponent's: 12 tiles x 6 units saturates the top of the curve without
#: pushing past it.
MELON_OPEN_TILES = 12

#: The day the opening runs on. Day 0 is the only day both seats start level.
MELON_OPEN_DAY = 0

#: The day that opening saturates, and so the day its crop must reach a lot.
#: `spec.CROP_SATURATE_AGE[I_MELON]` is 10.
MELON_OPEN_HARVEST_DAY = MELON_OPEN_DAY + int(spec.CROP_SATURATE_AGE[spec.I_MELON])

#: Units a single melon lot offers on the dump day. The recorded opening's six
#: lots are 6/24/12/6/6/6 and its largest is 24: a squared curve is walked, not
#: jumped, and one 84-unit line takes the quote 248 -> 104 by itself.
MELON_OPEN_LOT = 24

# ---- MELON_PLATE: the opening plate as two PROGRAMMABLE floats [MELONGENES]
#
# `MELON_OPEN_ON` is the plate as a fixed PACKAGE -- 12 tiles on day 0 plus its
# own dump-day excursion clock, its `MIDDAY_PLACE` wall and the assert at 3791
# that forbids `BANK_BEFORE_LOT_ON`.  The shipped ESR string carries
# `BANK_BEFORE_LOT_ON=True`, so the package can never be flown on the ship, and
# MELONENG could only ever read it against FT2 minus that switch.
#
# These two floats are the plate's SIZE and DATE alone, with nothing else
# attached: `_melon_plate` rewrites `plant_target` on one day exactly as
# `_melon_open` does, and the crop the plate grows is harvested and sold by the
# ordinary lot allocator (MELONDUMP 3: our dawn melon shed equals that day's
# melon sells on 60/60 board-days, so no dump day has to be written).  Because
# no excursion is compiled, the pair composes with the whole shipped package
# and a trainer can move them as continuous genes.
#
# `MELON_PLATE_TILES = 0` is OFF and is read at TRACE time, so the guard is a
# Python `if` and the expression the planner builds is character for character
# the one it builds today (`tests/test_melon_plate.py`).
MELON_PLATE_TILES = 0.0

#: First (and only) day the plate plants on. Read only when TILES > 0.
MELON_PLATE_DAY = 0.0


def melon_plate_on() -> bool:
    """True when the programmable plate claims any tile [MELONGENES].

    A plain `bool` read at trace time, like `open_board`, so OFF nothing is
    traced and the champion theta decodes byte for byte.
    """
    return float(MELON_PLATE_TILES) > 0.0


# ---- MELON_DENY: arrive before the reacting rival's melon line [SWITCH, OFF]
# The plate is a bounded d0..2 mix rewrite. Its crop saturates at age ten; the
# sell row reserves MELON until the dump/hold release, then sets only MELON's
# reservation to zero. OFF is a Python trace-time gate.
MELON_DENY_ON = False
MELON_DENY_PLATE = 0
MELON_DENY_DUMP_DAY = 10
MELON_DENY_HOLD = 0


def melon_deny_on() -> bool:
    """True when the denial plate and release rule are compiled."""
    return bool(MELON_DENY_ON)


# ---------------------------------------------------------------------------
# The residual action head [SWITCH, ACTIONRL]
# ---------------------------------------------------------------------------
# A learned net sitting ON TOP of the frozen planner: at each dawn it may nudge
# four things the day has already decided, and nothing else.  `brain.decide` is
# still the policy; this is a residual on four of its outputs, clamped so hard
# that the worst a broken head can do is ask for a day the executor already
# knows how to absorb (`ACTIONRL1` section 1: there is no plan validator, and
# over-asking is the designed, silently-absorbed failure mode at `:8099-8106`
# and `plant_eff = min(fill_target, seeds + seed_buy)` at `:9158`).
#
#   d_plant  per crop   -4 .. +4   on days >= RESIDUAL_FIRST_DAY
#   d_animal per kind   -2 .. +2   (GOOSE, COW, SHEEP)
#   d_hire              -2 .. +2   applied to the ENUMERATION's argmax, before
#                                  `n_hire` exists (never after, `:10013`)
#   hold_num per product 0/1/2     -> x0, x0.5, x1 of the gene's reservation
#
# `RESIDUAL_ON = False` is OFF and is read at TRACE time by `residual_on`, so
# the guard is a Python `if`, the expression the planner builds is character
# for character the one it builds today, and a theta trained before the head
# existed decodes byte for byte (`tests/test_residual.py`).
RESIDUAL_ON = False

#: The head: `RESIDUAL_FN(obs_features, macro_fields) -> dict` with keys
#: `d_plant` int[5], `d_animal` int[3], `d_hire` int, `hold_num` int[9].
#: `S/actionrl/head.py::numpy_fn` builds one for the package (numpy, no JAX);
#: `head.jax_fn` builds the traced, sampling one the trainer rolls out.
RESIDUAL_FN = None

#: Path to a `head_<k>.npz` checkpoint, or "". A plain STRING, so the engine's
#: switch string can carry it (`S/drainpin/on2b.py::conv` falls through to str)
#: and `S/actionrl/gate.sh` needs no new plumbing: `RESIDUAL_ON=True,
#: RESIDUAL_HEAD=/abs/head_6.npz`. Installed lazily, the first time a day is
#: planned, so OFF nothing is imported and nothing is read off disk.
RESIDUAL_HEAD = ""

#: Day 0 is the pinned opening [MELONENG, SCRIPTOPEN]: the plate, the pump and
#: the whole d0 package are measured as one and the head does not get a vote on
#: the mix there.  Only `d_plant` is gated -- the roster, the herd and the
#: reservation are ordinary days' business from the first dawn.
RESIDUAL_FIRST_DAY = 1

#: How wide each slot may swing, exactly the ACTIONRL1 action space. Re-asserted
#: here rather than trusted from the head, because a half-trained net writing a
#: negative `plant_target` is a silent invariant break, not an error.
RESIDUAL_PLANT_MAX = 4
RESIDUAL_ANIMAL_MAX = 2
RESIDUAL_HIRE_MAX = 2

# ---- the WIDE-ASK layout [ACTIONRL11] -------------------------------------
#
# The v1 clamps above are the whole action space of `head.py`'s "v1" layout and
# they stay exactly what they were: a v1 override dict has no `ask_fill` key,
# the `if "ask_fill" in o` below is a PYTHON test, and the expression this
# module builds for `head_940` is character for character the shipped one.
#
# The "wide" layout widens two of the clamps and adds two channels, because
# ENGTAIL/VOLUMEHI/OPSCENSUS put the whole high-band tail (-11.6k volume,
# -11.3k price, all d10-19) on ONE number: the Macro plant ASK. `n_free` is
# 26-38 plantable tiles a day and `macro.plant_target` asks for 0-9
# (`brain.py:1061-1094`, `n_dev = _qfloor(dev_frac * n_free)`); nothing refuses
# the ask, the purse idles 15-39k from d16, and a +-4 tile nudge cannot cross a
# 20-tile gap. The two things that FUND a bigger ask -- crew turns and seed --
# were not in the action space at all.
#
#   d_plant   per crop   -6 .. +6
#   d_hire               -4 .. +4
#   ask_fill             0..4 quarters of `n_free`, as a FLOOR on the day's
#                        total ask, on days >= RESIDUAL_ASK_DAY0
#   seed_buy             0/1/2/4 extra seed units per short crop, taken out of
#                        what the day's own budget grant left
RESIDUAL_PLANT_MAX_WIDE = 6
RESIDUAL_HIRE_MAX_WIDE = 4
#: `ask_fill` denominator: the action is k/RESIDUAL_ASK_STEPS of `n_free`.
#: `head.ASK_STEPS` must agree.
RESIDUAL_ASK_STEPS = 4
#: First day `ask_fill` may floor the ask. d10 is where the census gap opens
#: (VOLUMEHI/OPSCENSUS); d0-9 is the opening and EARLYRAMP closed it (-10,278).
RESIDUAL_ASK_DAY0 = 10
#: Most extra seed units `seed_buy` may add to ONE crop's grant.
RESIDUAL_SEED_MAX = 4

# ---- PROGRAM_ENGINE1: one observation-reconciled whole-season owner --------
# OFF is a host-language branch at every seam.  The intent object is created
# per seat by ``agent.runtime.ProgramEngineState`` and contains only current
# public/private observation facts plus committed progress from that Runtime.
PROGRAM_ENGINE_ON = False
#: PROGENG2 (a): melon tiles planted on d0 (ENGINE one-lot d10 sale); any
#: unfunded remainder carries to d1. 6 reproduces the astra14 6/4/1 opening.
PROGRAM_MELON_D0 = 11
#: PROGENG2 (b): through the herd schedule's last acquisition day the
#: programme herd is funded ahead of seed without the post-d9 repay test.
PROGRAM_HERD_FIRST = True
PROGRAM_HERD_LAST_DAY = 17
#: PROGFIX1 (1): programme plantings valued at full stream value (dev_weight
#: floor GROW_ONE) so the labour admission keeps funded plant chains.
PROGRAM_PLANT_FULL = True
#: PROGFIX1 (1b/1c): share scarce planting slots across crops pro rata and
#: net held seed out of the seed-buy room.
PROGRAM_PLANT_SHARE = True
#: PROGFIX1 (2): herd schedule = the ENGINE's mean buy schedule (runtime).
PROGRAM_HERD_REAL = True
#: PROGFIX1 (3): no fertilizer buy-back on d10-19 (applications from own stock stay).
PROGRAM_FERT_SELL = True
#: PROGFIX1 (4c, REJECTED at 16 -> 0): programme d0 wheat pump (ENGINE 15.4 bought, 11.1
#: sold d0); 16 matched it but no-collapse fidelity fell. <= OPEN_PUMP_KEEP disables.
PROGRAM_PUMP_UNITS = 0
#: PROGFIX2 (1): mid-day programme herd buy after sales / land repair (runtime).
PROGRAM_HERD_MIDDAY = True
#: PROGFIX2 (1b, REJECTED 90.7 -> 87.5): the mid-day herd buy leaves today's owed seed money in the purse.
PROGRAM_HERD_MIDDAY_SEEDFIRST = False
#: PROGFIX2 (3, REJECTED: nocollapse 90.7 -> 90.7 (-9 coin), median 89.8 -> 89.4): spent ongoing crops count as dig-and-plant slots (EXPIRY_SLOT predicate, programme only).
PROGRAM_EXPIRY = False


def program_engine_on() -> bool:
    return bool(PROGRAM_ENGINE_ON)


def _program_value(program, name, default=0):
    if program is None:
        return default
    if isinstance(program, dict):
        return program.get(name, default)
    return getattr(program, name, default)


def _program_macro(xp, macro, program):
    """Final crop/herd ask, after the residual and every melon veto."""
    i32 = xp.int32
    plant = xp.maximum(xp.asarray(_program_value(
        program, "plant_target", macro.plant_target), i32), 0).astype(i32)
    herd = xp.maximum(xp.asarray(_program_value(
        program, "animal_target", macro.animal_want), i32), 0).astype(i32)
    return macro._replace(plant_target=plant, animal_want=herd)


def _program_prefix(xp, d, program):
    """Promote funded programme work without changing its quantities."""
    if program is None:
        return d
    i32 = xp.int32
    service_ops = xp.asarray((O.OP_WATER, O.OP_HARVEST, O.OP_FEED,
                              O.OP_CARE, O.OP_COLLECT_FERT), i32)
    service = xp.any(d.chain_op[:, :, None] == service_ops[None, None, :],
                     axis=(1, 2))
    planted = xp.any(d.chain_op == O.OP_PLANT, axis=1)
    # Placement is paid work too. Omitting it stranded purchased animals in
    # the shed behind every new planting (one cow sat there through d29).
    priority = service | planted | d.m_place
    return d._replace(
        tier=(d.tier + priority.astype(i32) * 2).astype(i32),
        tile_value=xp.maximum(d.tile_value, priority.astype(i32)).astype(i32))


def _program_values(xp, costs, day):
    """One grant, ordered by service, opening melon, herd S/C/G, then seeds.

    The grant compares value/cost. Equal values accidentally put cheap seeds
    ahead of the herd; encode the priority as a ratio instead.
    """
    i32 = xp.int32
    rank = xp.asarray((8, 8, 3, 3, 3, 3, 3, 4, 5, 6), i32)
    opening = ((xp.arange(BUD.N_LISTS) == BUD.L_SEED0 + spec.I_MELON)
               & (day <= 2))
    rank = xp.where(opening, 7, rank).astype(i32)
    scale = BUD.VALUE_CAP // (8 * int(max(spec.ANIMAL_COST)))
    return xp.minimum(costs * (rank * scale)[:, None],
                      BUD.VALUE_CAP).astype(i32)


def _program_seed_room(xp, want, room):
    """Apportion scarce planting cells without starving later crop lanes."""
    i32 = xp.int32
    total = xp.sum(want, dtype=i32)
    cap = xp.minimum(xp.maximum(room, 0), total).astype(i32)
    denom = xp.maximum(total, 1)
    scaled = want * cap
    take = (scaled // denom).astype(i32)
    remainder = (scaled % denom).astype(i32)
    left = cap - xp.sum(take, dtype=i32)
    ids = xp.arange(spec.N_CROPS)
    for _ in range(spec.N_CROPS):
        pick = xp.argmax(xp.where(take < want, remainder, -1))
        hit = (ids == pick) & (left > 0)
        take = take + hit.astype(i32)
        remainder = xp.where(hit, -1, remainder)
        left = left - xp.any(hit).astype(i32)
    return take


def _residual_head_module():
    """`S/actionrl/head.py`, wherever this process is running [ACTIONRL].

    Two worlds, one module. In the REPO it is imported off `S/actionrl/head.py`
    by file path (the trainer, the judge, the tests). In the PACKAGE it is the
    copy `scripts/package_submission.py` lays down beside this file as
    `core/residual_head.py` -- the package has numpy and no JAX, and
    `head.numpy_fn` is written for exactly that (`forbidden_imports` would fail
    the build otherwise).
    """
    try:
        from . import residual_head as mod         # the packaged copy
        return mod
    except ImportError:
        pass
    import importlib.util
    import os
    path = os.environ.get("KAGG3_RESIDUAL_HEAD_PY") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "..", "S", "actionrl", "head.py")
    sp = importlib.util.spec_from_file_location("kagg3_residual_head", path)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


def residual_on() -> bool:
    """True when a head is installed [ACTIONRL]. Trace-time, like `open_board`.

    `RESIDUAL_ON` is checked FIRST and short-circuits, so the OFF planner never
    imports a thing, never touches the disk and traces the expression it traced
    before the head existed.
    """
    global RESIDUAL_FN
    if not RESIDUAL_ON:
        return False
    if RESIDUAL_FN is None and RESIDUAL_HEAD:
        mod = _residual_head_module()
        RESIDUAL_FN = mod.numpy_fn(mod.load(RESIDUAL_HEAD))
    return RESIDUAL_FN is not None


#: Crop order the day-0 debt is paid in -- crop order with WHEAT last, so the
#: opening cannot be bought out of the animal feed and the four-day rotation.
_MELON_PAY_RANK = np.array(
    [spec.N_CROPS if c == spec.I_WHEAT else c for c in range(spec.N_CROPS)],
    dtype=np.int32)
#: Order the day-0 seed want is clipped in: MELON first, then WHEAT, then the
#: rest in crop order.
_MELON_SEED_RANK = np.array(
    [0 if c == spec.I_MELON else (1 if c == spec.I_WHEAT else 2 + c)
     for c in range(spec.N_CROPS)], dtype=np.int32)

# ---- MIRROR_OPEN: the engine class's whole opening, as ONE package
# [SWITCH, OFF]
#
# WHY IT EXISTS.  Every PIECE of the top-10 (fertilizer-engine) opening has
# been read alone on our planner and every one of them lost: the day-0 melon
# plate (`MELON_OPEN_ON`, M12 -16,224 with their purse +15,547 --
# `docs/strategy/2026-09-16-meloneng.md`), the forced top opening (94 -> 26 %,
# `2026-09-09-forced-opening*.md`), tiles and hands together
# (-4,835, `2026-09-16-jointlift.md`).  The JOINT program was never read as one
# package, and the MELONENG autopsy named the reason the plate alone loses:
# twelve standing melon VACATE the strawberry/wool output the shared pot pays
# us for, and the vacated tiles are a PRICE GIFT to the opponent.  The engine
# class does not vacate anything -- it carries 6.6 hands a day over d0-9 where
# we carry 4.2, and it buys 242 units of market wheat a game where we buy 157.
# So the hypothesis this switch tests is exactly one sentence: *does keeping
# the LABOUR and the bought FEED up over d0-9 pay for the melon plate?*
#
# WHAT IT IS.  Three module constants over the d0-`MIRROR_LAST_DAY` window and
# nothing else:
#   (a) the day-0 plant mix claims `MIRROR_MELON_TILES` for MELON, through
#       `_melon_open` -- the existing, measured `MELON_OPEN_ON` machinery, at
#       all three `open_board()` sites (mix, seed clip order, placement);
#   (b) `crew_target` is floored at `MIRROR_HANDS_D0_9` on every day of the
#       window (`_mirror_crew`), which is the piece the single-lever tests
#       lacked -- the hire enumeration's ramp term walks the crew up to the
#       target and stops (`CREW_TARGET_PUSH`), so the standing melon does not
#       eat the hands the rest of the board needs;
#   (c) `MIRROR_WHEAT_BUY` extra units of market WHEAT on each window day's
#       BUY row, through `_rebuy_extra` -- the same clipped, purse-walked
#       re-buy the `REBUY_ON` arm uses, so the feed the melon plate displaces
#       (melon pays for its tiles in `_MELON_PAY_RANK` order, wheat last) is
#       bought back rather than starved.  10 days x 9 units is the +85 u/game
#       that separates our 157 from their 242.
#   (d) fertilizer is NOT part of this switch: `FERT_TIMING_ON` (shipped) is
#       already the best-day application the engine class runs.
#   (e) from `MIRROR_LAST_DAY + 1` the policy is the shipped FT2 policy,
#       untouched -- in particular the melon the plate stands up is harvested
#       and sold by the normal lot allocator, NOT by `MELON_OPEN_ON`'s dump-day
#       excursion (this switch touches none of the three sites that read
#       `MELON_OPEN_ON` alone), so it composes with `BANK_BEFORE_LOT_ON` and
#       the shipped FT2 control rows are its control.
#
# OFF, `open_board()` is the disjunction it always was, `open_tiles()` returns
# `MELON_OPEN_TILES`, `_mirror_crew` is never called and the BUY row takes the
# branch it always took, so the champion theta decodes byte for byte
# (`tests/test_mirror_open.py`).
MIRROR_OPEN_ON = False

#: Tiles the opening day hands MELON under `MIRROR_OPEN_ON`.  Twelve is the
#: recorded opening's number (`MELON_OPEN_TILES`) and the top-10 tapes' own
#: d0 count (6-13 tiles).
MIRROR_MELON_TILES = 12

#: Hands the window's days ask the hire ramp for.  The tapes carry 6.6/day
#: over d0-9 against our 4.2; seven is that number rounded the way a crew is.
MIRROR_HANDS_D0_9 = 7

#: Extra units of market WHEAT bought on each window day's BUY row.
MIRROR_WHEAT_BUY = 9

#: Last day of the mirrored opening.  Day 10 is the tapes' first melon sale
#: day and the day their hand count falls level with ours.
MIRROR_LAST_DAY = 9


def open_tiles() -> int:
    """Tiles the opening day's mix claims for MELON [SWITCH].

    `MELON_OPEN_TILES` unless the package switch is the only one asking, in
    which case it is the package's own count.  A plain `int` read at trace
    time, so OFF the expression `_melon_open` builds is the one it always
    built.
    """
    if MIRROR_OPEN_ON and not (MELON_OPEN_ON or OPEN_DENY_ON):
        return int(MIRROR_MELON_TILES)
    return int(MELON_OPEN_TILES)


def mirror_window(xp, day):
    """bool: is `day` inside the mirrored opening [SWITCH]."""
    return day <= xp.asarray(MIRROR_LAST_DAY, xp.int32)

# ---- MIDDAY_PLACE: bank the melon at a rank that still makes the lot
# [SWITCH, OFF]
#
# THE MEASUREMENT that named this switch (`docs/spikes/2026-09-04-midday-place.md`,
# `S/mp/probe2.py`): with `MELON_OPEN_ON` and twelve standing melon on the day
# they saturate, the excursion's DROP lands on turn 11 and turn 16 -- and when
# the twelve tiles are moved onto the tiles *nearest* a shed access
# (`DIST_SHED` 0 and 1, which is where `_derive`'s `near_rank` puts them) it
# lands on turn 22, twice, and nothing else banks at all. Distance is not the
# wall. The wall is one expression: `MELON_OPEN_ON`'s excursion fires after the
# block's **last** melon rank
#
#     m_ins = max{ j in [s, end] : kmel[j] }
#
# so the deposit turn is the whole prefix of the block up to and including its
# final melon tile, `start_u + cu[m_ins] + DIST_SHED[m_ins]`. Putting the melon
# next to the shed only makes that prefix *cheaper to walk*, so the block eats
# more ranks before it reaches its last melon and the DROP lands later still.
#
# `BANK_BEFORE_LOT_ON` already carries the rule that answers it -- "the largest
# rank whose DROP still lands on or before the lot's turn" (`drop_t <=
# O.SELL_TURNS[BANK_LOT]`) -- and `MELON_OPEN_ON` has no time rule whatsoever.
# So half of this switch is that rule, moved onto the melon trigger: the
# candidates are the block's melon ranks whose deposit lands by
# `O.MELON_LOT_TURNS[MIDDAY_PLACE_LOT]`, and the excursion goes after the
# largest of them, which is the most melon the window can bank in front of the
# row that sells it. With no candidate the excursion is not taken and the day
# is `MELON_OPEN_ON`'s.
#
# The other half is the op, and it is the reason the switch is PLACE and not
# DROP. The engine's PLACE (`kaggriculture.py:377-408`) falls through to a
# *selective* shed deposit when the item is not an animal going onto a matching
# free structure: it banks `min(qty, inv[item])` of one item, obeys
# `shedCapacity`, and **leaves the rest on the unit**. OP_DROP dumps the whole
# inventory and destroys what does not fit (`:343-356`). Two things follow:
#
#   * a mid-block deposit no longer voids the block's carried inputs, which is
#     the rule that took `BANK_BEFORE_LOT_ON`'s candidate rate from 28% of
#     unit-days to 3% (`after <= 0`, and the census in its own block above);
#   * the dump day's own 72 melon units cannot destroy the shed's overflow on
#     the way in.
#
# It costs the same one turn as the DROP, so the excursion's price
# (`2 * DIST_SHED + 1`) does not move.
#
# `sim/units.py` did not model the engine's PLACE-to-shed path at all before
# this switch (it only knew animal placement), so an `OP_PLACE` with a product
# argument was a silent no-op in the simulator while the real engine banked it.
# That branch is now there, unconditionally and inert: nothing but this switch
# emits `OP_PLACE` with a product item.
#
# NOT MEASURED in the real engine. This switch is the mechanism only; whether
# the melon opening is worth playing at all is `MELON_OPEN_ON`'s question and
# its answer today is no (-14,289 a game).
#
# OFF, the excursion keeps `MELON_OPEN_ON`'s last-melon rank and its OP_DROP,
# `melon`'s third element is never read, and every expression is the one it
# replaced, so the champion theta decodes byte for byte
# (`tests/test_midday_place.py`).
MIDDAY_PLACE_ON = False

#: Which of `ops.MELON_LOT_TURNS` the deposit has to beat, and so the whole of
#: the time rule. 0 is the first melon row (turn 11, engine hour 12): a deposit
#: that misses it can still be sold by the later rows, but a rank chosen
#: against a later row is a rank chosen behind the opponent's own dump.
MIDDAY_PLACE_LOT = 0

#: Units the PLACE asks for. The engine clips to what the unit is carrying
#: (`n = min(n, inv.get(item, 0))`) and to the shed's room, so an over-ask is
#: exact and costs nothing; `SHED_CAPACITY` is the most that could ever land.
MIDDAY_PLACE_QTY = int(spec.SHED_CAPACITY)

# ---- MIDDAY_PLACE_V2: give the harvest day back to the melon [SWITCH, OFF]
#
# THE MEASUREMENT (`S/mp2/`, seed 899009257 vs the band tape 105442685, real
# engine). `MIDDAY_PLACE_ON` is *inert* on the board `MELON_OPEN_ON` actually
# builds: our seat harvests all 72 melon on day 10, emits zero deposits, and
# sells the lot at day 11 hour 0 at 154.5 into the pot the opponent crushed
# selling 60 of its own at 247 on day 10 hours 9-13. The excursion's own probe
# says why, rank by rank -- every melon deposit turn on the real board is 13
# to 27 against a rule that admits 11, so `in_time` is false everywhere,
# `res` is 0 and the excursion is never taken:
#
#     u0 melon ranks [0, 1]      deposit turns [15, 19]
#     u1 melon ranks [7, 8]      deposit turns [17, 23]
#     u2 melon ranks [11, 12]    deposit turns [16, 20]
#     u4 melon ranks [22, 23]    deposit turns [21, 27]
#     u5 melon ranks [24, 25, 26] deposit turns [14, 18, 22]
#     u6 melon rank  [27]        deposit turn  [13]
#
# Two things make those turns, and neither is the time rule:
#
#   * **the chain.** `_derive` gives a ripe melon tile four ops -- WATER,
#     HARVEST, PLANT, WATER -- because a harvested one-time crop frees its
#     tile and `free_slot` hands it straight back to the day's planting. The
#     deposit fires after a *rank*, so it waits for the replant and its
#     watering: two turns per melon tile, twelve tiles, spent standing on the
#     far side of the walk home.
#   * **the geometry.** The twelve melon tiles are `_derive`'s nearest free
#     tiles, but "nearest" inside one unlocked quadrant is `DIST_SHED` 2 to 5,
#     not the 0-and-1 of the spike's fixture board. The round trip is 5 to 11
#     turns and the crew starts at turn 2.
#
# This switch takes the two turns back. On `MELON_OPEN_HARVEST_DAY` the ripe
# melon tiles leave `free_slot`, so their chain is WATER + HARVEST and nothing
# else -- no build, no placement, no replant. The WATER stays: melon is a
# one-time crop, `_daily_refresh_plants` skips it (`kaggriculture.py:787`) and
# every unit past the first is a watering inside `[window_start, max_yield_day]`,
# so day 10's own watering is the sixth unit of the six. The replant is day
# 11's, which is one day of growth on twelve tiles against the whole day-10
# sale.
#
# The deadline moves with it: a deposit is judged against
# `MIDDAY_PLACE_V2_TURN`, the day's last selling row rather than its first
# melon lot, because the unit acts before its turn's market
# (`_apply_unit_action` then `_process_market`, `kaggriculture.py:935-941`) so
# a PLACE on turn t still sells on turn t's row.
#
# THE SECOND THING IT TAKES BACK: the route order. Two turns off the chain is
# not enough on its own -- measured, 30 of 72 units on day 10 (`S/mp2/`,
# `verify3.sh`). The residue is the *order*: `task_order` sweeps the day by
# tier then value, so the twelve melon ranks land scattered through 0..28 and
# half of them sit late in a block whose end was priced without them. A block
# is a contiguous run of that order, so a melon rank the order leaves late is
# a rank no block can bank in time, however the block sweeps itself -- the
# per-unit reorder that puts melon first inside a block was built and
# measured, and it moved 30 to 39 and no further, because what refuses the
# deposit is the block *cut* (`_cut` walks the unreordered `load`, so the
# 9-to-11-turn reserve the excursion charges eats the very ranks the reorder
# had just pulled forward).
#
# So the reorder is the day's, not the block's: on a day a melon ripens its
# ranks take a tier of their own, one above the priced tiles, in the *route*
# order alone. `task_order` takes any int32 tier [LAW, 0.5] and the route
# order is not the admission order -- `order_v`, `rank_v` and `n_admit` are
# untouched, so no tile loses its place in the value queue -- and every block
# cut, `covered` and the `start` walk downstream then read the melon-first
# order natively. Day 10 goes 30 -> 60 of 72 sold (`S/mp2/verify3.sh`, 2
# seeds x 2 seats vs tape 105442685, ours 60 at 185.8 against their 60 at
# 246.4). The per-unit reorder is then the identity -- melon leads every block
# it is in and keeps its index order -- and was dropped.
#
# AND IT IS NOT THE OPENING'S DAY. `MELON_OPEN_HARVEST_DAY` is where the
# excursion was found, not what it is about: melon's `CROP_FIRST_YIELD_DAY`
# is the reason a mid-day deposit exists at all, and that is a property of
# the crop. The default build plants melon on days 4-6 and harvests it on
# 13-16, and V1 -- nailed to the opening's day, and only compiled in at all
# under `MELON_OPEN_ON` -- leaves every one of those harvests to
# `_end_of_day` and the next morning's opening row. So V2 supplies the
# excursion itself (`melon` is built whenever this switch is on) and triggers
# it off `mel_mask` being non-empty, which is the day any standing melon's
# chain harvests.
#
# AND THE DEPOSIT IS ONLY HALF OF IT. On the default board the excursion
# above works -- traced on the real engine, seed 899009257 seat 0 vs tape
# 105442685, the day's melon ranks lead the route order and the PLACE fires
# on every harvest day: day 13 turn 17 (6 units), day 14 turns 13 and 14 (12),
# day 15 turns 12 and 18 (18), day 16 turn 15 (6) -- and every one of those
# units still sold on the *next* morning's opening row. The reason is the
# other end: `SELL.allocate` runs once at dawn against `avail`, the hour-0
# shed, and on a harvest day the day's melon is still on the vine, so melon's
# slot in all three lots is zero and the day has no row to sell a mid-day
# deposit on. `MELON_OPEN_ON` never hit this because it carries its own
# `melon_lots` rows, and `BANK_BEFORE_LOT_ON` because it adds what it banks to
# its lot in bulk. V2 had neither.
#
# So the banked units are added to the day's LAST lot in bulk, the way both of
# those do it: `MIDDAY_PLACE_V2_TURN` is that lot's turn by construction (the
# assert under `early_lot_turns`), a unit acts before its turn's market, and
# over-asking is free because every SELL is clipped to the shed unit by unit.
# `_routes` reports the ranks the PLACE carried in -- `[s, m_ins]`, the block's
# melon inventory at the deposit -- through the same `banked` output
# `BANK_BEFORE_LOT_ON` uses, the two being mutually exclusive by assert.
#
# AND THE SAME-DAY SALE IS WORTH NOTHING ON THAT BOARD. Real engine, tape
# 105442685, 2 seeds x 2 seats, plan defaults plus this switch. The mechanism
# does exactly what it says: 54 of the season's 72 melon units a game now sell
# on their own harvest day, against 0 without the row (`S/mp3/`). The money
# does not follow it. Melon revenue a game:
#
#     defaults                     0 same-day, 72 next @162.4  ->  11,657
#     + deposit, no row (HEAD)     0 same-day, 72 next @162.4  ->  11,657
#     + deposit + row             54 same @157.9, 18 next @149.3 -> 11,556
#
# The deposit alone is *exactly* the defaults' ledger to the coin -- banking
# at turn 17 and banking at dusk both sell on the next morning's row -- and
# adding the row moves 101 coins a game the wrong way. The reason is the
# curve: melon has no shop demand, so the day's last row and the next
# morning's row quote nearly the same drained inventory, and nothing of ours
# or theirs trades melon in between. Selling 42 units into turn 18 walks our
# own quote down at once (151.9) where the same units spread over the next
# mornings fetched 168.4. There is no third party to beat to the pot on the
# default build -- which is precisely what `MELON_OPEN_ON` manufactures, and
# there (day 10, twelve tiles standing against the opponent's own dump) the
# excursion is worth 60 of 72 units at 185.8 rather than 30. The row is
# therefore mechanism, kept for whatever build does race a pot; it is not a
# lever on this one. Whole-game coins are no help either way: on seed
# 1872559163 the row moves the melon ledger 119 coins and the final score
# 19,098, which is the tape opponent's game diverging on a shared market, not
# our melon [counterfactuals overstate].
#
# OFF, `mel_bank` is all-false, `free_slot` is the expression it was, the
# route tier is `(tile_value > 0)`, `melon` is `MELON_OPEN_ON`'s or nothing,
# `banked` comes back `None` as it always did and no lot moves, and the
# deadline is `MIDDAY_PLACE_LOT`'s, so the planner decodes byte for byte
# -- pinned on `test_route_early`'s digests, and
# `MELON_OPEN_ON=False,MIDDAY_PLACE_ON=True,MIDDAY_PLACE_V2_ON=True` finishes
# on the defaults' coin on both seats of seed 899009257 (74,658 / 75,815).
MIDDAY_PLACE_V2_ON = False

#: The turn a V2 deposit has to land on or before -- the day's LAST row, not a
#: melon lot. Measured deposit turns on the real board are 13 to 18 (`S/mp2/`,
#: the probe table in the block above, with the chain at two ops): a rule cut
#: at the last melon row (15) refuses u0's 12 units and u1's 6 for one and
#: three turns. Every row from `O.MELON_LOT_TURNS[0]` to `O.SELL_TURNS[-1]`
#: sells melon out of the shed, and the last of them still beats the
#: end-of-day drop, which is what puts the units on day 11's opening row
#: behind the opponent's finished dump.
MIDDAY_PLACE_V2_TURN = int(O.SELL_TURNS[-1])

# ---- SAME_DAY_FERT: sell the day's own fertilizer on the day [SWITCH, OFF]
#
# THE DEFECT, measured on the real engine (seed 54306694 seat 0 vs tape
# 105077847, and 831637369 seat 0 vs tape 105442685). `COLLECT_FERTILIZER`
# takes one unit per animal per day into the *hand's* inventory, and nothing
# empties that hand until `_end_of_day` -- so the day's fertilizer reaches the
# shed after the last row and sells on the next morning's. On day 1 that is a
# cash knife edge and not a rounding error: we stand at day-1 dawn on 32-50
# coins, collect six fertilizer, sell none of them, reach day-2 dawn on 2-20
# coins, hire nobody, and day 2 is the farmer alone watering tiles -- no FEED,
# no CARE, no COLLECT, so day 2's fertilizer flag is lost as well and the care
# bonuses with it. The top-tier tapes sell their day-1 fertilizer at hours 6-8
# of day 1, buy feed wheat with the ~100 coins a unit, and hire four hands on
# day 2.
#
# THE MECHANISM IS `MIDDAY_PLACE_V2`'s, with a different item in it. That
# switch already carries every piece: a day-level route tier that sweeps the
# day's ripening ranks to the head of the order (a block is a contiguous run
# of that order, so a rank the order leaves late is a rank no block can bank
# in time), a mid-block excursion that walks to the nearest shed access and
# deposits with OP_PLACE (which banks one item and leaves the block's carried
# feed and fertilizer alone, unlike OP_DROP), a time rule that admits a rank
# only when its deposit lands on or before the row that sells it, and a bulk
# addition of what was banked to the day's LAST lot -- because `SELL.allocate`
# runs once at dawn against the hour-0 shed, where the day's fertilizer does
# not yet exist, and a deposit with no row to stand on sells nothing.
#
# So this switch is that mechanism with `mel_mask` replaced by the day's
# COLLECT_FERTILIZER ranks, `I_MELON` by `I_FERT`, and the deposit quantity
# replaced by a count. The count is the one thing melon did not need: melon is
# never a PICKUP item, so `PLACE MELON 100` can only bank what the block
# harvested, while a block that picked fertilizer up at the route base to
# spread it later is carrying units the shed must not take. The deposit
# therefore asks for exactly the number of COLLECT ranks the block has worked
# since its own first (`[s, m_ins]`, the same span `banked` reports), and
# `PLACE`'s `min(qty, inv[item])` leaves the carried pickup where it is.
#
# Days 1..`SAME_DAY_FERT_LAST_DAY`: day 0 has no animal that has stood
# overnight, and the terminal day liquidates the whole shed anyway.
#
# WHAT IT BUYS, real engine, both games ledgered order by order
# (`scratchpad/sdf/`). Day 1 now sells its own six fertilizer on turn 18 of
# day 1 for 593 coins, and the ramp moves with the cash:
#
#     seed 54306694 seat 0 (tape 105077847)   OFF          ON
#       day-1 fertilizer sold on day 1          0           6
#       day-2 dawn coins                        2         595
#       day-2 hires                             0           3
#       day-2 FEED / CARE / COLLECT         0/0/0       2/2/2
#       day-2 unit ops                         24          97
#       day-3 FEED / CARE / COLLECT         6/6/6       6/6/6
#
#     seed 831637369 seat 0 (tape 105442685)  OFF          ON
#       day-1 fertilizer sold on day 1          0           6
#       day-2 dawn coins                       20         613
#       day-2 hires                             2           3
#       day-2 unit ops                         24          97
#
# Day 2 is the honest residue: the cash and the crew arrive, and the day
# still works only two of the six animals, because the *admission* order is
# the value queue and this switch only moves the *route* order -- a crew of
# four cannot reach nineteen thirsty tiles and six animals, and the top-tier
# tapes bring five hands to it. That is the crew ramp's lever, not this one.
#
# Whole-game coins say nothing either way and are not the claim: 97,495 ->
# 95,623 on the first seed (theirs 153,496 -> 127,327) and 58,946 -> 42,279
# on the second (theirs 59,873 -> 42,267, a 927-coin loss turned into a
# 12-coin win). Those are two tape opponents' games diverging on a shared
# market from day 1 hour 18 onwards [counterfactuals overstate]; the ramp is
# the acceptance and a panel is what would price the switch.
#
# OFF, `melon` is `MELON_OPEN_ON`'s or `None`, the route tier is the
# expression it was, `mel_ranked` is `MIDDAY_PLACE_V2_ON`'s, the deposit op,
# item and quantity are `MIDDAY_PLACE_ON`'s, the deadline is
# `_midday_place_turn`'s and no lot moves -- so the planner decodes byte for
# byte, pinned on `test_route_early`'s digests in `test_same_day_fert.py`.
SAME_DAY_FERT_ON = False

#: The last day the switch applies on; it applies on days 1..this. Default 29
#: (the whole season): the defect is a day-1 one but the flag is lost on every
#: day the fertilizer rides to the next morning, and the terminal day is
#: excluded by `~terminal` regardless.
SAME_DAY_FERT_LAST_DAY = 29

# ---- OPEN_DENY: the opening board without the dump-day rows [SWITCH, OFF]
#
# THE LEDGER (`scratchpad/deny/report.txt`, today). The opening splice
# `KAGG3_OPENING=<open16 tape>:K` is worth +14,148 a game at K=4 and +6,469 at
# K=1 -- day 0 alone -- and paired against kagg2 the whole gain is the
# opponent's loss: their coins fall 16,113 while ours move +2,347. An
# instrumented engine (every fill, hire and land buy logged with its price)
# says where their coins go, and it is not a price collapse: their *unit*
# prices RISE on every product and their *volume* falls a fifth.
#
#     STRAWBERRY  240.0u @127.2 -> 183.5u @135.5   -5,664
#     MELON       119.4u @161.6 ->  74.2u @198.8   -4,556
#     MILK        256.3u @ 91.3 -> 183.4u @106.2   -3,920
#     WOOL        143.4u @129.7 -> 116.2u @140.0   -2,342
#     FERTILIZER  249.5u @ 54.6 -> 192.2u @ 63.1   -1,496
#
# The reason is that kagg2's day-1 board *is* the tape's -- MELO12, WHEA7,
# SHEE2, COW2, five hands, to the tile -- and the top tier's is too. The market
# is one shared, town-replenished demand stream per product, so the season's
# absorbable volume is fixed and the split goes to whoever supplies it first.
# Our shipped day 0 (WHEA10, CARR9, COW3, SHEE2, GOOS1) reaches the melon curve
# on day 14 against their day 10 and the wool and milk curves days behind as
# well; the tape's day 0 puts us level. Level is enough: their day-10 melon
# payday falls 16,311 -> 12,355, their dawn cash on day 12 falls 14,578 ->
# 8,775, and from there they stand thirteen melon tiles at day 10 where they
# stood twenty, buy two fewer cows and grow six weeds.
#
# `MELON_OPEN_ON` already builds that board -- and lost 14,289 a game, because
# it also rewrote the day the crop saturates: an excursion that fires after a
# block's *last* melon rank, so the h12/h14 rows quote an empty shed, and a
# melon row on the dump day that walks our own quote down before the opponent
# arrives. The ledger arm agrees with its post-mortem: on the same twelve
# games the switch leaves our coins alone (107,584 -> 109,662) and hands the
# opponent 18,855 (90,645 -> 109,500), for a margin of +161 against the
# shipped +16,938.
#
# So this switch is `MELON_OPEN_ON` **minus its dump day**. The three parts
# that build the board stay -- the day-0 plant mix, the seed clip that sees
# melon and wheat first, and the melon placed nearest a shed access -- and the
# two that trade on day `MELON_OPEN_HARVEST_DAY` (the `_routes` excursion and
# `_market`'s melon lots) do not fire. There is no new constant: it reads
# `MELON_OPEN_TILES`, `MELON_OPEN_DAY` and the two rank permutations above,
# because the board it is asking for is the same board.
#
# MEASURED and rejected: 64 paired real-engine games, flow58_g450, seed base
# 777001, four opponents, ALL -25,397 a game (t -9.50), every leg negative and
# worse than `MELON_OPEN_ON`'s -14,289 -- so the dump day was not the bill, it
# was paying part of it. The signature is the same gift the melon opening
# always had: our own coins -9,691 and the opponents' +15,706, win 62.5 % ->
# 15.6 %.
#
# What that buys is the answer the ledger could not get from the splice alone.
# The denial is NOT the day-0 board: the planner builds the tape's board (the
# ledger's day-1 tile counts are MELO12, WHEA7, SHEE2 under all three of the
# splice, `MELON_OPEN_ON` and this switch) and still hands the opponent
# fifteen thousand coins. What the splice leaves behind and the planner does
# not is the *crew that keeps twelve melon alive*: the tape hires 5/3/4/5 hands
# on days 0-3 where the planner hires 5/1/3/4, and the day-3 board under a
# one-day splice already reads WEED11, MELO8 -- the field is planted and then
# not watered. So the next arm is the crew ramp against the standing melon
# field, not another way to plant it.
#
# OFF, every site it shares with `MELON_OPEN_ON` takes the branch it always
# took, so the champion theta decodes byte for byte
# (`tests/test_open_deny.py`, the same digests `test_melon_open.py` pins).
OPEN_DENY_ON = False

#: The three `MELON_OPEN_ON` sites `OPEN_DENY_ON` shares: the day-0 plant mix
#: (`_melon_open`), the day-0 seed clip order (`_wants`) and the day-0 melon
#: placement (`_derive`). The dump-day sites read `MELON_OPEN_ON` alone.
def open_board() -> bool:
    """True when the day-0 opening board is being built by any of the three
    switches that build it (`MIRROR_OPEN_ON` is the package [SWITCH])."""
    return MELON_OPEN_ON or OPEN_DENY_ON or MIRROR_OPEN_ON

# ---- OPEN_PUMP: the opening splice's one market order [SWITCH, ON] -------
#
# THE MECHANISM, measured order by order (`scratchpad/curve/report.txt`, a
# per-unit ledger around the engine's `_commit_unit` on 42 games). The K=1
# opening splice's whole 17.6k edge is ONE trade, and it is not a tile:
#
#   day 0 hour 0 (our HIRE row, which otherwise touches no inventory, and the
#   only hour of the game where the class-A tapes are idle):
#       BUY_PRODUCT WHEAT 53   pot 10000 -> 9947, quote 25 -> 32
#       (WHEAT is `below_func` "sqrt" with amp exactly 1, so the quote is
#        `25 + sqrt(10000 - inv)`.)
#
#   day 0 hour 1, the opponent's opening BUY row, whose FIRST order is
#   `BUY_PRODUCT WHEAT 5`. Our sell-back is our own first order in the same
#   turn, so `_process_market`'s lockstep -- which pairs the two seats by
#   queue index and quotes both off one pre-commit inventory -- interleaves
#   their five units with our sells at the drained quote: five wheat for 160
#   coins where an untouched pot charges 134.
#
# Twenty-six coins is the whole payload, and it is enough because the class-A
# opening is cash-critical to the coin: their row ends `BUY_ANIMAL SHEEP 2`
# and they reach it holding 524 off the default and 498 behind the pump, so
# the second 500-coin sheep is refused. SHEEP first-yields on day 6, so their
# day-6 wool halves, their fertilizer stream runs one animal short from day 1,
# their day-8 dawn cash is 4 where it was 49, and the hire bill -- a running
# sum of Fibonacci numbers -- turns that into four hands. 14 of 14 games, both
# tapes, every seed: the day-0 rows of both seats are seed-independent, so the
# denial is deterministic.
#
# IT COSTS US NOTHING. `_commit_unit` quotes a BUY at post-buy inventory and a
# SELL at pre-sell inventory, so a round trip against an unchanged pot nets
# zero by construction; the opponent's five interleaved buys hold the first
# five rungs of our sell ladder up at 32, so the trip is slightly profitable
# and the `OPEN_PUMP_KEEP` units we retain cost ~22 coins each against a
# 25-coin base. It occupies no unit-turn (market orders are free of the
# route), changes no tile and moves no other product's curve.
#
# WHY THE SELL-BACK IS SLOT `B_WHEAT` AND NOT A SPARE SLOT. The engine pairs
# by queue index over the *compacted* row (`render.market_actions` drops a
# `MO_NONE`), so the sell has to be our first live order or our 53 units
# restore the pot before they buy and the denial evaporates; selling at turn 2
# instead keeps the denial but locks ~1,584 coins out of the turn-1 row, which
# on day 0 is the entire 3,000-coin opening. The BUY row's own head slot is
# `B_WHEAT` -- `BUY_PRODUCT WHEAT` -- and day 0 buys no wheat and no
# fertilizer, so the slot is empty and the *fixed layout is not disturbed*:
# one slot changes op, nothing shifts, the row still holds ten. The switch
# refuses to fire on any day that does buy wheat (`wheat_buy == 0` below), so
# the two can never contend for it.
#
# The cross this makes against a foreign seat -- our SELL against their
# BUY_PRODUCT on one item -- is the trade itself, and `sim/market.py` says it
# is unmodelled. It cannot arise in self-play (both seats pump on day 0 and
# both present SELL), and `assert_no_cross` takes an explicit `exempt` for
# this one slot rather than being weakened for every other.
#
# OFF, `pump` is `None` and `_market` emits the rows it always did, so a theta
# trained before it decodes byte for byte (`tests/test_open_pump.py`).
#
# ON by default since 2026-09-04, sized 53/5: real engine, flow58_g450, paired
# on (seed, opponent, seat) against the same theta with the switch off.
# panel24 (24 tapes x 10 seeds x 2 seats, n=480) +20,509 a game at t 12.71,
# win 64.0 -> 86.7 %; the four-opponent ladder (kagg2 + three class-A tapes,
# n=128) +21,692 at t 10.08 and 100 % on every leg; against the blanket K=1
# opening splice +16,518 at t 13.75. 17 of 24 panel legs are positive and no
# negative leg reaches |t| 2.
#
# THE ONE MEASURED REGRESSION, on the record: the current top-10 tapes
# (n=320) are -4,640 at t -6.22, because THEY ALREADY RUN THIS PUMP -- they
# buy 30-43 wheat at hour 0 and sell it back at hour 1 -- so there is nothing
# to deny, our 53 units are quoted behind theirs, and the round trip costs
# ~236 coins against a 220-coin day-0 slack, which refuses our own second
# sheep. Sizing does not fix it (44 units: -6,659; KEEP=0: -14,621). Two
# switches below answer it. `OPEN_PUMP_SLOT0_ON` -- on by default since
# 2026-09-04 -- moves our hour-0 leg to queue index 0 so the two ladders
# interleave instead of ours walking a pot they drained; it is free against a
# seat that does not draw at hour 0, so the class-A denial is untouched.
# `OPEN_PUMP_TELL_KEEP0_ON`, still off and still unmeasured in the engine,
# reads the tell -- at hour 1 a wheat pot below `10000 - OPEN_PUMP_UNITS` says
# the other seat drew at hour 0 too -- and keeps none of the 53 rather than
# paying the top of a deep ladder for five units of feed. This is still judged
# on panel24, which is the population we are ranked against.
#
# TURNED OFF 2026-09-17 as the first half of PUMPCLIP
# [docs/strategy/2026-09-17-stack1.md]: the population moved and panel24 is no
# longer it.  "THE ONE MEASURED REGRESSION" above is now the modal board -- the
# seats we meet at 1,900-2,300 open with this same pump, so there is no denial
# to buy and we pay ~236 coins out of a 220-coin day-0 slack for the privilege.
# Judged as ONE arm with `CLIP_CAP_ON = True` (see that switch) over 241
# held-out boards: +418/board, se 130, t +3.22, theirs -52, and the gain rises
# with the opponent's rating inside our band.  OFF is not a revert to the
# pre-2026-09-04 program only in name: `pump` is `None` again and `_market`
# emits the rows it always did, which `tests/test_open_pump.py` pins.
#
# TURNED BACK ON 2026-09-18 by STACK5 [docs/strategy/2026-09-18-stack5.md], and
# the 09-17 reading above is REVERSED, not refined.  Judged head to head on the
# 60 engine boards, the pump-ON cell beats the pump-OFF one by **+49,342 se
# 7,456 t +6.62** on the 52 doubly-retained line -- ours +19,544, THEIRS
# -29,805, board win 9.6 % -> 65.4 % -- and pump-OFF's two -67k blow-ups (Sida
# Zuo, ymg_aq) come back as +379 and +4,258.  Pooled over the same 241 boards
# the ON cell is +565 t +9.34 vs FT2 at a QUARTER of the OFF cell's noise, with
# the FRESH72 edge rising with the opponent's rating.  So the denial the pump
# buys is not a denial of nobody: it is exactly what stops a 3,000-rated seat
# from taking the opening pot, and turning it off was a pure tax on the
# population we are climbing into.  The column stays a gene.
OPEN_PUMP_ON = True

#: The one day the pump fires. Day 0 is the only hour-0 in the season with an
#: untouched pot and an idle opponent, and the only opening priced to the coin.
OPEN_PUMP_DAY = 0

#: Units bought at hour 0. Near-minimal, not arbitrary: the quote is
#: `base + sqrt(n)` and the opponent buys five units off a 24-coin cushion, so
#: denying the 500-coin animal needs `5 * (sqrt(n) - 1) >= 25`, i.e. n >= 36.
#: Below that the pump is free and useless; far above it we start paying for
#: our own day-0 wheat. 53 is what the recorded tape does.
OPEN_PUMP_UNITS = 53

#: Units kept back from the sell-back -- the tape's five. They are real feed
#: wheat bought at ~22 coins, and they are also ~108 coins out of the day-0
#: purse, which is the one purse in the season with no slack.
OPEN_PUMP_KEEP = 5

#: The purse the hour-0 leg needs. The ladder against a fresh pot is
#: `sum(25 + sqrt(k)) for k in 1..53` = 1,584 coins, measured; we open on
#: 3,000. A day that cannot pay skips both legs rather than half the trade.
OPEN_PUMP_MIN_MONEY = 1584

# ---- OPEN_PUMP_SLOT0: the hour-0 leg at index 0 [SWITCH, ON] -------------
#
# THE RACE, measured order by order against a pumping opponent
# (`scratchpad/pumpracer/counterfactual.txt`, engine-exact ladders on four
# seeds). The shipped hour-0 row is `[HIRE x n, BUY_PRODUCT WHEAT 53]` -- the
# pump at slot `first`. The top-tier tapes now open with `[BUY_PRODUCT WHEAT
# 53]` at index 0 and nothing in front of it, and `_process_market` pairs the
# two seats by queue index over the compacted row, so *their* ladder walks the
# virgin pot and ours walks the drained one:
#
#   shipped  ours 1,796 / theirs 1,584   we pay 212 more
#   index 0  ours 1,690 / theirs 1,690   both ladders interleave, lockstep
#
# 212 coins is the game. Our second SHEEP is refused at hour 1 by 27 coins, and
# their sell-back into the pot our 53 units drained gains them 105 where the
# solo round trip loses 128 -- which buys two extra day-1 hands and a permanent
# extra cow, +13.6k at the final bell.
#
# AGAINST A NON-PUMPER THE INDEX IS FREE. An untouched pot charges the same
# 1,584 for 53 units whichever slot asks for it, and the class-A tapes are idle
# at step 0, so the denial this switch is not aimed at is untouched.
#
# THE HIRES NO LONGER PAY FIRST, AND THAT IS FINE -- but it is a real change,
# not a nicety, so it is stated: `_process_market` resolves the atomic orders
# (HIRE, BUY_LAND) of slot round *i* before that round's lockstep, and the
# rounds run in slot order, so a buy at index 0 commits before a hire at index
# 1. The engine's day-0 hire ladder is Fibonacci -- 1, 1, 2, 3, 5, 8, 13, 21,
# 34 -- so the nine hands this switch admits (`first < MO` keeps the row inside
# the engine's ten with the buy in it) cost 88 coins in total, against a
# 3,000-coin purse with 1,690 taken out of it. No hand of the opening can be
# refused for want of the coins the buy spent first, and the day-0 cash after
# the row is the same however the two are ordered. `sim/market.process_slot`
# resolves HIRE the same way, per slot round and in player order, so the sim's
# day-0 cash is the engine's for either row order
# (`tests/test_open_pump_racer.py`).
#
# OFF, the hour-0 row is the one `OPEN_PUMP_ON` always emitted, slot for slot,
# so a theta trained before this switch decodes byte for byte
# (`tests/test_open_pump_racer.py`).
#
# ON by default since 2026-09-04: real engine, flow58_g450 theta, paired on
# (seed, opponent, seat) against the same theta with the switch off.
# Evidence (2026-09-04, paired at seed base 777001, theta flow58_g450, vs the
# index-5 pump): the 53/48 book -- tape 105400600 win 37.5 -> 81.2 %, +10,451
# t 2.7 (n=32); tape 105421293 win 34.4 -> 82.8 %, +13,767 t 5.7 (n=64);
# the animal-first farmer 105393487 +6,502 t 2.7; the 4-opp panel 128/128
# byte-identical; panel24 -108 t -0.2 (280/480 identical); top10 -1,003
# t -1.4 (n=640). Four of our first six live losses at 1700-2030 were that book.
OPEN_PUMP_SLOT0_ON = True

# ---- OPEN_PUMP_TELL_KEEP0: keep nothing when the pot says we lost the race
#                                                            [SWITCH, OFF] ---
#
# THE TELL. At hour 1 the wheat pot reads `10000 - our 53 - theirs`, and ours
# is known, so `10000 - inv - OPEN_PUMP_UNITS` is exactly the other seat's
# hour-0 draw: 0 against a class-A tape, 30-43 against a top-10 one. It is the
# one bit the plan cannot have at hour 0, when the pot is still virgin.
#
# WHAT IT BUYS. `OPEN_PUMP_KEEP`'s five units are feed wheat at ~22 coins
# against a 25-coin base -- a small win off a *shallow* ladder. Behind a racer
# the ladder is deep: the five we keep cost the top of a 53-unit walk into a
# pot both seats drained, and the measured arm (`keep0_summary.txt`, four
# seeds) has our second SHEEP land -- day-1 SHEEP goes 1 -> 2 -- on 140 coins
# recovered. Keeping nothing is only right when the race was lost; against a
# quiet pot the five units stay, which is why this is a tell and not a resize.
#
# AND WHAT THE PROBE DID NOT SHOW, on the record. The four-seed arm is one
# racer tape, not a measurement: the sheep lands and the round trip goes from
# -235 to -95 on all four, but the finals are mixed -- the margin improves on
# two seeds (+6.4k, +5.4k) and collapses on the other two (-38k, -24k), and our
# own score falls on three of the four. This switch is off until the paired
# protocol prices it on a panel.
#
# WHERE IT LIVES. The day's plan is built once, at hour 0
# (`agent/runtime.Runtime.act`), so no expression inside `build_day` can read
# it: `view.mkt_inv` is the hour-0 pot by construction and the sim builds the
# whole day under one `lax.scan` at dawn. The recovery is therefore a patch on
# the *cached* plan at the turn the BUY row is emitted -- `open_pump_tell_keep0`
# below, called from the runtime's per-turn hook. It is a submission-path
# switch only; the trainer's rollout cannot see the tell and is not changed.
OPEN_PUMP_TELL_KEEP0_ON = False

#: Units of the other seat's hour-0 draw that count as "they pumped too". The
#: measured top-10 openings draw 30-43; a class-A tape draws 0. 40 sits inside
#: the observed band and above every incidental day-0 wheat purchase.
OPEN_PUMP_TELL_MIN = 40

# ---- ENDGAME_TOMATO: the town's tomato lottery, planted [SWITCH, OFF] ----
#
# THE PRICE IS THE TOWN'S, NOT THE BOARD'S. `SHOPS` in the engine draws the
# town's shop instances by lottery, PIZZA_SHOP and FARMERS_MARKET both list
# TOMATO, and a shop drains the shared market every four steps for the rest of
# the season. TOMATO's curve is the only crop's whose below-`I0` half is a
# *hinge* (base 60, T 200, gain 8): the first two hundred units of deficit
# barely move it and every unit after that explodes it.
#
# Measured on the real engine (2026-09-04, flow58_g450, `scratchpad/tomato/`).
# Seed 473956351 seat 0 vs tape 105393487 -- a town that drew three
# FARMERS_MARKETs -- walks the hinge:
#
#     day      0     12     20     25     28
#     TOMATO  60     68     82    148    181
#
# while MELON collapses to 4-28 and STRAWBERRY to 20-30 by days 26-29. No
# opponent in any ledger grows tomato, so the whole deficit is the town's and
# the pot is ours alone. The theta does not see it coming: it reads the price,
# not the shop list, so it plants its first tomato on day 16 and reaches 18
# tiles on day 22 -- 114 units at 162 average, 18,422 coins, off the tail of
# the curve rather than the front of it. The control is seed 242285847 seat 1
# vs tape 105442685, a town of BRUNCH_SPOT x2 + SMOOTHIE_SHOP: no tomato buyer,
# the price sits at 60-64 all season and the theta correctly plants none.
#
# The shops are in the observation from the day they unlock
# (`obs["town"]["unlocked_shops"]`, counted by `agent/parse.parse_town` into
# `view.shops`), so the trigger is a fact the plan already holds -- which is
# why this is a planner switch and not a gene.
#
# WHAT IT DOES. On a firing day the whole crop mix goes to TOMATO: the tiles
# the day plants do not change, only what goes in them, exactly as
# `_wheat_mix` moves a share and `_melon_open` moves the opening's. Melon,
# animals and every sell rule are untouched.
#
# WHAT IT DOES NOT READ. The finding's third clause -- "the opponent grows no
# tomato" -- is not in the rule: `DayView` carries our board only
# (`opp_kind`/`opp_occ` reach `brain.decide`, never the planner), and the
# planner is where the mix has to move so `_wants`, `plant_eff` and
# `plant_crop` agree about it. The clause is a fact about the population, not
# about the day, so it is documented here instead of tested at runtime.
#
# OFF, `_endgame_tomato` is never called and `plant_target` is the mix the
# brain chose, so a theta trained before it decodes byte for byte
# (`tests/test_endgame_tomato.py`, pinned on `test_route_early`'s digests).
#
# OFF BY DEFAULT, AND WHY -- the arm is measured and it LOSES. Paired on the
# finding's own seed (473956351 seat 0 vs tape 105393487, flow58_g450):
#
#                         OFF                    ON
#     TOMATO      114u @162  18,422    264u @ 92  24,165    +5,743
#     STRAWBERRY  229u       32,615    152u       13,989   -18,626
#     WOOL        323u       77,576    217u       48,813   -28,763
#     final          149,536 / 101,042    106,613 / 94,159
#
# The tomato line does exactly what the finding predicted -- 34 tiles by day
# 19 against the theta's 18 by day 22, 150 more units, +5,743 coins -- and the
# game still falls 42,923. Two costs, both real and neither in the finding:
#
#   1. THE HINGE IS THE TOWN'S DEFICIT, AND WE FILL IT. OFF, our 114 units
#      leave the pot at 9,674 by day 28 and the price walks 60 -> 175. ON, our
#      264 go in from day 19, the pot never falls below 9,740, the price peaks
#      at 108 on days 21-22 and slides back to 84-88 by day 26. The explosion
#      the switch was aimed at is the one thing supplying it destroys, so this
#      is a *sizing* problem, not a mix problem [counterfactuals overstate].
#   2. AN ONGOING CROP IS A TWELVE-DAY CLAIM ON THE CREW. A tomato tile has to
#      be watered every other day from planting to day `d+12` or it weeds out,
#      and 34 of them crowd the route: the herd grows (SHEEP 14 -> 16) while
#      the wool sold falls 323u -> 217u. The strawberry the mix gave up is the
#      other half.
#
# The control seed is clean: 242285847 seat 1 vs tape 105442685 draws
# BRUNCH_SPOT x2 + SMOOTHIE_SHOP, the rule never fires and the game finishes
# on 80,280 / 89,850 either way -- so the town gate itself is sound.
#
# WHAT WOULD PRICE IT: a tile budget rather than the whole mix (the town drains
# ~1 unit a tick per buyer, so the season absorbs on the order of a hundred
# units, which is a dozen tiles and not thirty-four), and a panel rather than
# one seed. Until then this is off.
ENDGAME_TOMATO_ON = False

#: First day the rule may fire. A tomato planted on day 10 first yields at the
#: dawn of day 18, which leaves the whole hinge-walking half of the season to
#: sell into; earlier than that and the mix is the midgame's, which the theta
#: already prices against a market that has not moved yet.
ENDGAME_TOMATO_DAY = 10

#: Unlocked tomato-buying instances (PIZZA_SHOP + FARMERS_MARKET, duplicates
#: counted) the town must have drawn. One shop drains 1 unit per tick and the
#: town center another; two are what carried 60 -> 181 on the measured seed,
#: and one alone does not clear the hinge's 200-unit shoulder in a season.
ENDGAME_TOMATO_SHOPS = 2

#: Last day a tomato planted still pays for itself.
#:
#: TOMATO is `first_yield_day 8, interval 1, max_yield 4, ongoing`, so
#: `_end_of_day` adds one unit at the dawn of days `d+8 .. d+11` and the tile
#: is dead after `d+12`: a tile planted on day `d` collects
#: `min(4, 30 - (d + 8))` units, and nothing it does later can add to them.
#:
#:     d = 18   4 units   d = 19   3   d = 20   2   d = 21   1   d >= 22   0
#:
#: Against a *conservative* 100 coins a unit -- the measured season averages
#: 162 and ends at 181 -- day 18 is worth 400 coins against a 50-coin seed and
#: about seven unit-turns (one PLANT, one HARVEST, and a WATER every other day
#: to keep `consecutive_unwatered` under 2; an ongoing crop accrues its units
#: whether or not it was watered, so the water is survival, not yield). That is
#: ~50 coins a turn on top of the seed. Day 19 already drops a quarter of the
#: yield for the same seed and the same twelve days of tile, and day 21 pays
#: 100 for a 50-coin seed plus six turns, which is inside the noise. 18 is the
#: last day that collects the crop's FULL four units, and that is the cut.
ENDGAME_TOMATO_LAST_DAY = 18

#: Tomato tiles the rule may hold at once; 0 = no budget (today's behaviour,
#: the whole mix). THE SIZING IS THE WHOLE ARGUMENT -- see the block above: the
#: measured arm lost 42,923 coins with 34 tiles because 264 units *filled* the
#: town's deficit (the price peaked at 108 on day 21 and slid back to 84 by day
#: 26, so the hinge the rule was aimed at is the thing the rule destroyed) and
#: because twelve days of every-other-day watering per tile crowded the crew
#: off wool and strawberry. A tomato buyer drains ~1 unit a tick and the town
#: centre another, so a season absorbs on the order of a hundred units and a
#: tile yields four: about a dozen tiles, which is the default the arms measure.
#:
#: Counted as tiles HELD, not tiles planted: a live TOMATO plant already on the
#: board (`kind == KIND_PLANT and occ == I_TOMATO`) spends the same crew and
#: sells into the same pot as one planted today, so the budget is against the
#: board and not against the day. A tile that has weeded out is no longer a
#: plant, so the budget frees itself as the crop dies. The budget bounds the
#: rule's own claim and not the gene's: a day whose softmax already wants more
#: tomato than the budget keeps it, exactly as `MELON_OPEN_TILES` can only ever
#: raise melon.
ENDGAME_TOMATO_TILES = 0

# ---- LATE_STRAW_CAP: stop planting the contested crop [SWITCH, OFF] ----
#
# The band loss anatomy (2026-09-05, `scratchpad/lossanat/`): against the six
# 1950-2110 tapes the opponent's book is FIXED -- 350 WHEAT, 264 STRAWBERRY,
# 263 MILK, 176 WOOL, 0 TOMATO, on the boards we win and the boards we lose
# alike. Everything that differs is ours, and 73 % of the win/loss separation
# lands on days 26-29, when our liquidation runs into that book. On the win
# boards we sell 162 units of strawberry and 79 of tomato; on the loss boards
# 255 of strawberry and 17 of tomato, and the strawberry price at day 22 is 60
# against 98. We are dumping 255 units into a market their 264 have already
# taken, and the price we crush is the price on the units we are holding.
#
# The cap is at the PLANTING decision and not at the sale: a tile committed to
# strawberry on day 20 has already spent the seed, the tile and twelve days of
# crew by the time the sell rule could refuse the unit, and refusing the sale
# only hands the units to day 29 at a worse price. From `LATE_STRAW_CAP_DAY`
# the day's mix moves its strawberry share onto the crops the brain also
# chose, in the proportions it chose them; the tiles already carrying
# strawberry are untouched and finish normally.
#
# OFF, `_late_straw_cap` is never called and `plant_target` is the mix the
# brain chose, so a theta trained before it decodes byte for byte.
LATE_STRAW_CAP_ON = False

#: First day the cap applies. STRAWBERRY is `first_yield_day 6, interval 2,
#: ongoing`, so a tile planted on day 15 still collects its units through the
#: back half; the loss boards' 255 units are built by the day-15-20 mix, which
#: is where the anatomy puts the decision ("entered by our day-15-20 crop
#: mix"). Earlier than 15 and the cap is taking the midgame's cash crop away
#: from a market the opponent's book has not reached yet.
LATE_STRAW_CAP_DAY = 15

#: The shop instances that buy TOMATO, read off the engine's demand table
#: rather than named, so a table change cannot silently un-fire the rule.
_TOMATO_SHOPS = (spec.SHOP_CONSUME[:, spec.I_TOMATO] > 0).astype(np.int32)


# ---- MELON_VETO_FLOOD: stop planting into a finished book [SWITCH, OFF] ----
#
# MELONDUMP (`docs/strategy/2026-09-19-melondump.md`): on 8 of the 10 hiband
# loss boards the rival sells its whole melon line into days 10-18 -- 147 units
# walk the book from `I0 - 11` to `I0 + 127` BEFORE our first melon unit exists
# -- and MELON is `base 250, I0 10,000, T 300, above sq 3.6`, so 158 units over
# `I0` is `PRICE_FLOOR` 1. Nothing refills it (NEXTMECH LAW; the largest
# one-day quote recovery observed all season is 6 coins), so the melon quote is
# a ONE-WAY RATCHET: once the rival has walked it down, every melon tile we
# commit after that is labour spent against a price that cannot come back.
#
# OPSCENSUS prices the labour: our 12.3 melon plantings a board eat 75 of our
# 380 d10-19 water turns at 8.75 water turns per paying plant, and MELONDUMP's
# tape has 65 of the 78 units they yield clearing below 60/u. The sale side is
# CLOSED -- we already sell at the first dawn lot on 60/60 board-days and the
# hold counterfactual is negative on the recorded book -- so the only reachable
# decision left is the one MELONDUMP names: do not PLANT into the ratchet.
#
# The veto is a DEVELOPMENT change and not a mix change, on purpose. TURNCOST
# (`docs/strategy/2026-09-19-turncost.md`) re-shared the same tiles onto wheat
# and gifted the rival +316 at the best cell: volume on a shared curve is not
# worth its price on this band. So nothing is redistributed explicitly here --
# `sum(plant_target)` falls by the melon share and the existing decode and
# scheduler spend the freed tiles, seed coins and water turns exactly as they
# already would on a day whose brain asked for no melon.
#
# The gate is the observed dawn book, `view.mkt_inv[I_MELON]`, against the same
# `spec.MARKET_I0` that `_I0_COL` indexes the price table at -- the field the
# sell side reads, not a model of the rival.
#
# OFF, `_melon_veto` is never called: the branch in `_plan_and_stats` is a
# Python `if` on a module global, so the shipped program is the one it was,
# byte for byte (`tests/test_herd_ramp.py` pins the whole-plan sha256).
MELON_VETO_FLOOD_ON = False

# 2026-09-21 MELONVETO_POST: re-apply the flooded-book veto after ACTIONRL.
MELONVETO_POST_ON = False
#: Post-ACTIONRL veto threshold.  Separate from the original veto's gene so a
#: gate can dose the post-head repair without changing the pre-head rule.
MELONVETO_POST_K = 60

#: First day the veto may fire. MELON is `first_yield_day 10`, so a tile
#: planted on day 10 yields on day 20 -- which is exactly where MELONDUMP puts
#: our line's arrival (sell-day centroid us d23.0 vs them d11.3). Before day 10
#: the rival's dump has not happened yet and the d0-9 mix is EARLYRAMP's
#: window, not this gene's.
MELON_VETO_FLOOD_DAY = 10

#: Units over `spec.MARKET_I0` that count as a flooded book. MELONDUMP's
#: representative board crosses `I0 + 60` on day 13 at a quote of 233 and never
#: returns; 158 over `I0` is `PRICE_FLOOR` 1, so 60 is ~38 % of the way to a
#: dead book -- late enough that a quiet board never fires, early enough that
#: the veto still catches the d13-18 half of the dump.
MELON_VETO_FLOOD_K = 60


# ------------------------------------------------------ opponent supply [3.4]
#
# THE HOLE. `projector.py` says it outright: "Opponent impact is absent by
# construction -- that is the genes' job." The genes get two scalars per
# product, `hold` and `press`, and `press` is a straight line in the lot index
# -- it cannot say "wheat is fine all game but on day 21 the other seat dumps
# a hundred units into lot 3". So every quote the planner walks is the quote
# of a pot only we are selling into, and the day the field floods we price our
# last lot at a number that no longer exists.
#
# WHY IT IS FILLABLE. The opponents above us are open-loop scripts.
# `scripts/extract_opp_supply.py` reads the recorded market row out of all 81
# tapes in `artifacts/panel_opp` and finds, over the thirteen teams that
# appear twice or more, 96.6 % agreement on per-turn net units between two
# games of the SAME team -- three teams byte-identical for the whole season,
# and every one of them identical through turn 51. Their supply is a function
# of the turn, not of the board, so it can be tabulated once and forecast.
#
# WHAT THE SWITCH DOES. On, `projector.projected_inv` / `inv_at_day` (and so
# `sell.lot_inventories`, the three lots' quote curves, the BUY row's curve
# and the seed/animal horizon) add the measured mean opponent units expected
# in the pot by the projected turn. Nothing else moves: the allocator, the
# reservations and the pressure term are the ones they were, they simply walk
# a curve that now includes the other seat.
#
# WHAT IT CANNOT DO. The curve is the RECORDED row, so it is an upper bound --
# a SELL the engine clipped for want of stock still counts. And it is a mean
# over a field whose day-29 liquidation alone is 779 units, so the tail is
# dominated by a dump that lands after our last lot anyway.
# `OPP_SUPPLY_SCALE` is the one knob that prices both, and only a paired
# engine leg may set it.
#
# MEASURED 2026-09-05, AND IT LOSES. band6, 192 paired boards, seed base
# 777001, `--seed-per-opponent`, theta flow102_g280, against the live build:
#
#     scale 1.0   win 54.2% -> 46.9%   margin -2,972  sd 10,830  t -3.80  W/L 17/31
#     scale 0.5   win 54.2% -> 43.2%   margin -3,616  sd 10,413  t -4.81  W/L 17/38
#
# Win rate first, and it falls 7 to 11 points on both settings -- the loss is
# dose-responsive in the wrong direction (half the curve is worse than all of
# it), so this is not a scale that wants tuning. Our own coins fall (-1,841 /
# -2,358) and theirs RISE (+1,131 / +1,259): the forecast makes the planner
# duck the later lots, sell earlier and cheaper, and hand the pot back. The
# arithmetic is right and the price sensitivity is real -- 40 units at the
# I0=10,000 shoulder takes wool from 200 to 107 -- which is exactly why a
# forecast that is an upper bound (the RECORDED row, including sales the
# engine clipped) mis-prices the whole day. What a next attempt needs is the
# EXECUTED row (`scripts/replay_flow.py` measures it) and a curve that stops
# at our last lot rather than carrying day 29's 779-unit liquidation.
#
# OFF is byte-identical: `day` is an optional argument on every projector, and
# with the switch off the opponent term is not even looked up. Verified on the
# engine -- eight games on two band6 tapes give the same CSV, md5 785ce124, on
# this tree and on the untouched main tree.
OPP_SUPPLY_ON = False

#: Multiplier on the measured curve. 1.0 = the recorded row verbatim; below 1
#: prices the share of it the engine actually clears.
OPP_SUPPLY_SCALE = 1.0

#: The curve. `S_pop` is the mean over all 81 tapes; `S_band6`, `S_wall6`,
#: `S_top10` and `S_band6_wall6_top10` sit beside it and are the same
#: measurement over one panel -- which is fitting the forecast to the panel it
#: will be graded on, so the default is the field.
OPP_SUPPLY_PATH = "artifacts/opp_supply/S_pop.npy"

# ---- OPP_SUPPLY_FAMILY: the rival's OWN family supply curve [SWITCH, RIVALSUPPLY2 2026-09-29, default OFF]
# The user's idea (09-29 18:52Z): we almost know what the rival will sell, so price it into the projection.
# `OPP_SUPPLY_ON` above priced a population average (every product, every rival) and lost; this prices the
# rival's family.  Curves = EXECUTED net market-inventory units per step (+1 per SELL unit at price > 1, -1 per
# BUY_PRODUCT unit; engine replay, S/rivalsupply2/build_curves.py) averaged over the family's live seats:
# S_P48 (programme, 3 quadrants), S_PQ4 (programme + Q4), S_MEL (both, before the d10 split), S_V56 (V-family
# live seats), S_pop (the old curve, byte copy of artifacts/opp_supply/S_pop.npy), all in core/opp_supply/.
# Selection (agent/runtime `_opp_family`, every turn): step 0 -> pop; step 1 latches the rival's CODE from its
# h1 cash (`OPP_SUPPLY_FAMILY_MEL_CASH`, the BRAINSTORM5 whitelist P48 + PQ4 values keyed to PFS real h0) -> MEL,
# every other value -> V56; a MEL rival is PQ4 once it owns 4 quadrants, else P48 from `OPP_SUPPLY_FAMILY_SPLIT_DAY`
# (TOP1WATCH1: h1 cash no longer separates P48 from PQ4; the Q4 buy on d10 does).  `OPP_SUPPLY_SCALE` scales it.
# `OPP_SUPPLY_FAMILY_FORCE` = one curve all game ("pop" = the old switch through this path).  OFF: not read.
OPP_SUPPLY_FAMILY_ON = True  # SHIP_VRP25_HYB (RSFIX1 hyb050: core/opp_supply = S/rsfix1 curves/hyb050, delta MEL/P48/PQ4/OTH + V56 x0.5)
OPP_SUPPLY_FAMILY_FORCE = ""
OPP_SUPPLY_FAMILY_MEL_CASH = "938|964|985|992|1020|1100|2438|2464|2485|2492|2097"
OPP_SUPPLY_FAMILY_SPLIT_DAY = 10


#: [SWITCH, RSFIX1] V56 h1-cash codes (RIVALSUPPLY2 seats, lw23 V family).  "" = every non-MEL code is V56 (rs2);
#: set, a code on neither list is "NONE" -> no curve at all (the OFF projection).
OPP_SUPPLY_FAMILY_V56_CASH = "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106"  # SHIP_VRP25_HYB (RSFIX1 hyb050, 14 V56 h1 codes)


def opp_supply_family(code, day, rival_nquad):
    """[SWITCH, RIVALSUPPLY2] the curve name for a rival of `code` ("MEL" / "V56" / "NONE") on `day`."""
    if code == "NONE":
        return "NONE"
    if code != "MEL":
        return "V56"
    if int(rival_nquad) >= 4:
        return "PQ4"
    return "P48" if int(day) >= int(OPP_SUPPLY_FAMILY_SPLIT_DAY) else "MEL"


#: [SWITCH, RSFIX1] the projector call sites the family curve reaches (C crop-seed values, A animal values, S sale lots,
#: F feed/wheat buy).
OPP_SUPPLY_FAMILY_SITES = "CSFA"


def _osd(day, site):
    """[SWITCH, RSFIX1] `day` for a projector call at `site`, or None (= the OFF expression) when the family
    curve is ON and `site` is not in OPP_SUPPLY_FAMILY_SITES.  FAMILY_ON False -> `day` untouched."""
    if OPP_SUPPLY_FAMILY_ON and site not in str(OPP_SUPPLY_FAMILY_SITES):
        return None
    return day


def opp_supply_code(cash):
    """[SWITCH, RIVALSUPPLY2] "MEL" iff the rival's h1 cash is on the P48/PQ4-code list, else "V56"."""
    vals = {int(x) for x in str(OPP_SUPPLY_FAMILY_MEL_CASH).split("|") if x.strip()}
    if int(cash) in vals:
        return "MEL"
    vv = {int(x) for x in str(OPP_SUPPLY_FAMILY_V56_CASH).split("|") if x.strip()}
    return "V56" if (not vv or int(cash) in vv) else "NONE"


# `projector` reads the three names above out of this namespace. It has to be
# handed the dict and not left to find the module: `eval_vs_baselines` drops
# every `kagg3.*` entry from `sys.modules` for the length of a tape game, so a
# lookup from inside the planner returns None exactly when the switch is being
# measured (which is how the first band6 leg came back 192/192 identical).
PJ.bind_plan(globals())


# ---- OPP_MIX: price the other seat's book into the plant mix [SWITCH, OFF] --
#
# The band panel's loss signature (`scratchpad/lossanat/report.md`, 2026-09-05):
# nothing separates a win board from a loss board before day 8, 73 % of the
# separation lands on days 26-29, and the event is always the same one -- our
# day-25-29 liquidation running into the opponent's own book. Their book is
# fixed across win and loss boards alike (350 WHEAT, 264 STRAWBERRY, 263 MILK,
# 176 WOOL, **0 TOMATO**); what moves is *ours*. On the boards we win we sold
# 79 u TOMATO and 196 u MILK at 164/u; on the boards we lose we sold 255 u
# STRAWBERRY head-on into their 264 and the shared price paid the bill --
# STRAWBERRY 60/98 at d22, MILK 96/19, TOMATO 149/78 at d25.
#
# `ENDGAME_TOMATO_ON` answers that from the *town* side and with a fixed
# product. This switch answers it from the **opponent** side and with no fixed
# product: the observation carries both farms (`kaggriculture.py` seats
# `obs.farms` whole), so the tiles the other seat has already committed to each
# product are a fact the day already holds -- `view.opp_commit`, one count per
# product, animals mapped through `spec.ANIMAL_PRODUCT`. A product they have
# committed a large share of their farm to is a product whose price our own
# harvest will arrive into after theirs has already sunk it.
#
# It is a **price adjustment, not a ban**. The weight is
#
#     share[p] = opp tiles on p / opp producing tiles          (0 .. 1)
#     w[p]     = clip(1 - STRENGTH * share[p] + SHOP*n_buyers[p], FLOOR, 1)
#
# in `OPP_MIX_ONE` fixed point, and it enters in exactly the two places the
# planting decision reads a value: the k-th seed of each crop and the k-th
# animal in `_candidates` (`v_seed`, `v_anim` -- the same tail the crew ramp's
# `a_keep` rides on), and the day's mix in `_opp_mix`, which moves each crop's
# *share* of the penalty onto the least-contested crop that can still mature.
# Both halves are needed and neither is sufficient: the value term alone makes
# the budget refuse the contested seed and leaves the tile idle, and the mix
# term alone leaves the purchase side pricing a crop the tiles no longer want.
#
# The shop term is the cheap half of the same idea from the town's side: a shop
# that consumes the product drains it every four steps, so it is worth
# `OPP_MIX_SHOP` of the penalty back per buying shop instance. It can only ever
# *offset* the opponent penalty -- the clip's ceiling is exactly 1x -- which is
# what keeps `v * w // ONE` inside int32 at `grow_mult`'s 4x.
#
# OFF nothing here is called: `_candidates` appends the expression it always
# appended and `_plan_and_stats` never rewrites the mix, so a theta trained
# before the switch decodes byte for byte.
#: [SWITCH] Read the other seat's committed tiles into the plant mix.
OPP_MIX_ON = False
#: First day the weight is anything but 1x. Before it the plan is the plan.
#: Day 12 is the last day a STRAWBERRY planted still collects its full run and
#: the first day inside `lossanat`'s day-15-20 mix window; the day-10 melon
#: dump (a constant tax on every board) is already behind us.
OPP_MIX_DAY = 12
#: How much of the opponent's share is taken off the product's value. 1.0 means
#: a seat that had put its whole farm on one product would take that product to
#: the `OPP_MIX_FLOOR`; 0.0 is inert.
OPP_MIX_STRENGTH = 1.0
#: Fixed point for the weight. Powers of two only: `v * ONE // ONE == v` is the
#: exact integer identity the OFF path relies on.
OPP_MIX_ONE = 256
#: The floor a fully contested product is worth. Not zero: a contested product
#: is worth less, never nothing, and a floor of zero would be the hard ban this
#: is deliberately not.
OPP_MIX_FLOOR = 32
#: Penalty given back per shop instance that consumes the product.
OPP_MIX_SHOP = 32
#: Which shop instances buy which product, read off the engine's demand table
#: rather than named -- the same rule `_TOMATO_SHOPS` follows.
_OPP_MIX_SHOP_W = (spec.SHOP_CONSUME > 0).astype(np.int32)      # [N_SHOPS, N_PRODUCTS]


def opp_commitment(xp, kind, occ):
    """int[N_PRODUCTS]: tiles a farm currently devotes to each product.

    The integer twin of `brain._producing`, and deliberately the same shape and
    the same column meanings: crops in crop order, then one column per animal
    product, then FERTILIZER carrying the whole herd (every animal makes it).
    A whole-array reduction, so it does not care what tile order it is handed --
    the submission passes serpentine order and the simulator raw board order
    (`brain.PolicyObs`'s [LAW]).
    """
    i32 = xp.int32
    is_pl = kind == spec.KIND_PLANT
    is_an = ((kind == spec.KIND_COOP) | (kind == spec.KIND_PASTURE)) & (occ >= 0)
    cols = [xp.sum((is_pl & (occ == c)).astype(i32)) for c in range(spec.N_CROPS)]
    per_animal = [xp.sum((is_an & (occ == a)).astype(i32))
                  for a in range(spec.N_ANIMALS)]
    cols += per_animal                                          # EGG, MILK, WOOL
    cols.append(sum(per_animal))                                # FERTILIZER
    return xp.stack(cols).astype(i32)


def opp_ripe_yield(xp, kind, occ, t_yield):
    """int[N_PRODUCTS]: units of each product standing RIPE on a farm.

    `opp_commitment` counts tiles; this counts the units those tiles would
    deliver if they were harvested now -- the engine's own `yield_units`, which
    the observation carries for both seats (`agent/parse.py` reads
    `farms[q]["tiles"]`, the simulator reads `st.t_yield[q]`). A crop tile's
    units land on its crop, an animal tile's on `spec.ANIMAL_PRODUCT`; the
    FERTILIZER column stays zero, because a fed animal's fertilizer is not a
    yield the tile is carrying.

    Only `SELL_SLOT_PRIORITY_ON` reads it, and only as the size of the batch a
    rival could put into the pot ahead of our own units -- so it is a bound on
    contention, not a forecast, and a zero column simply falls back to
    `SELL_SLOT_PRIORITY_BATCH_MIN`.
    """
    i32 = xp.int32
    y = t_yield.astype(i32)
    is_pl = kind == spec.KIND_PLANT
    is_an = ((kind == spec.KIND_COOP) | (kind == spec.KIND_PASTURE)) & (occ >= 0)
    cols = [xp.sum(xp.where(is_pl & (occ == c), y, 0), dtype=i32)
            for c in range(spec.N_CROPS)]
    for a in range(spec.N_ANIMALS):
        cols.append(xp.sum(xp.where(is_an & (occ == a), y, 0), dtype=i32))
    out = cols[:spec.N_CROPS]
    # The animal columns are addressed through `spec.ANIMAL_PRODUCT` rather
    # than appended in animal order, for the reason `opp_commitment` gives:
    # the product columns are the market's, not the herd's. Read off the numpy
    # constant and never `xp.asarray` of it: this is a Python-time layout and
    # `int()` of a tracer is a `ConcretizationTypeError` under `jit`.
    rest = [xp.zeros((), i32) for _ in range(spec.N_PRODUCTS - spec.N_CROPS)]
    for a in range(spec.N_ANIMALS):
        p = int(spec.ANIMAL_PRODUCT[a]) - spec.N_CROPS
        rest[p] = rest[p] + cols[spec.N_CROPS + a]
    return xp.stack(out + rest).astype(i32)


def _opp_mix_strength() -> int:
    """`OPP_MIX_STRENGTH` in `OPP_MIX_ONE` fixed point.

    Read through `float` because the switch harness sets knobs from argv
    strings (`scratchpad/fert2/on2.py`), so `"0.5"` has to mean 0.5.
    """
    return int(round(float(OPP_MIX_STRENGTH) * OPP_MIX_ONE))


def _opp_mix_weight(xp, view):
    """int[N_PRODUCTS] in `OPP_MIX_ONE` fixed point: what one more unit of each
    product is worth once the other seat's standing commitment is priced in.

    Exactly 1x on every product before `OPP_MIX_DAY` and on a board where the
    other seat holds nothing, so the two call sites below are identities there.
    The day gate is a `where` and not an `if`: `view.day` is a tracer under
    `jit` and the plan stays shape-static.
    """
    i32 = xp.int32
    one = OPP_MIX_ONE
    commit = view.opp_commit.astype(i32)
    # An animal is counted twice -- once under its product and once in the
    # FERTILIZER column -- so the denominator drops that column and `share`
    # sums to 1 over the tiles that actually exist.
    tiles = xp.maximum(xp.sum(commit) - commit[spec.I_FERT], 1).astype(i32)
    share = (commit * one // tiles).astype(i32)
    pen = (share * _opp_mix_strength() // one).astype(i32)
    buyers = xp.sum(view.shops.astype(i32)[:, None] * xp.asarray(_OPP_MIX_SHOP_W),
                    axis=0).astype(i32)
    w = xp.clip(one - pen + buyers * OPP_MIX_SHOP, OPP_MIX_FLOOR, one).astype(i32)
    return xp.where(view.day >= OPP_MIX_DAY, w, one).astype(i32)


def _opp_mix(xp, view, macro: Macro) -> Macro:
    """`macro` with the day's crop mix tilted off the other seat's book [SWITCH].

    Each crop gives up its own penalty's share of its tiles -- `t[c] * (1 -
    w[c])`, floored, so a crop the other seat is not on gives up nothing and the
    tilt is proportional and not a ban -- and the tiles all go to the crop with
    the *highest* weight among those that can still mature by `pay_day`
    (`VAL.new_plant_units > 0`), which is the least contested product the day
    can actually plant. `sum(plant_target)` is preserved by construction, like
    `_wheat_mix`, `_melon_open` and `_endgame_tomato`: this is a mix change and
    not a development change, so the day's tile, seed and labour budget is sized
    against the same number.

    Inert before `OPP_MIX_DAY` (the weight is 1x there, so every `give` is 0)
    and on a day whose crops have all run out of season.
    """
    i32 = xp.int32
    t = macro.plant_target.astype(i32)
    w = _opp_mix_weight(xp, view)[:spec.N_CROPS]
    c_ix = xp.arange(spec.N_CROPS, dtype=i32)
    can = VAL.new_plant_units(xp, c_ix, view.day) > 0
    best = xp.argmax(xp.where(can, w, xp.asarray(-1, i32)))
    is_best = (c_ix == best.astype(i32))
    give = xp.where(is_best, 0, t * (OPP_MIX_ONE - w) // OPP_MIX_ONE).astype(i32)
    mix = (t - give + is_best.astype(i32) * xp.sum(give).astype(i32)).astype(i32)
    return macro._replace(plant_target=xp.where(can[best], mix, t).astype(i32))


def open_pump_exempt(turn):
    """bool[MO]: the slots `OPEN_PUMP_ON` is allowed to cross the other seat on.

    One slot on one turn -- the sell-back at the head of the BUY row -- and an
    all-false mask with the switch off, so `sim/market.assert_no_cross` is the
    guard it always was until the switch is on.
    """
    mask = np.zeros(MO, bool)
    if OPEN_PUMP_ON and turn == O.TURN_BUY:
        mask[buy_row_slot(B_WHEAT)] = True
    return mask


def open_pump_tell_armed(day, hour) -> bool:
    """True on the one turn `open_pump_tell_keep0` can do anything.

    A Python-time predicate on Python-time scalars, so the runtime can skip
    parsing the market on the other 719 turns of the season, and so the switch
    off costs exactly one `and`.
    """
    return (OPEN_PUMP_ON and OPEN_PUMP_TELL_KEEP0_ON
            and int(day) == OPEN_PUMP_DAY and int(hour) == O.TURN_BUY)


def open_pump_tell_keep0(plan, day, hour, mkt_inv):
    """The hour-1 recovery [SWITCH, OPEN_PUMP_TELL_KEEP0].

    `plan` is the day's cached six-array plan, `mkt_inv` the market inventory
    of the *hour-1* observation (int[9], `agent.parse.parse_market`). Returns
    `plan` itself -- the same object -- unless every one of these holds:

      * both switches are on and this is day `OPEN_PUMP_DAY`'s BUY turn;
      * the cached plan really carries our sell-back, `OPEN_PUMP_UNITS -
        OPEN_PUMP_KEEP` units of wheat in `B_WHEAT`'s slot (a day the pump
        declined leaves a buy or a hole there, and is left alone);
      * the pot says the other seat drew `OPEN_PUMP_TELL_MIN` units or more at
        hour 0 -- i.e. it pumped too, and the five units we would keep sit at
        the top of a ladder into a pot both seats drained.

    Then the sell-back's quantity becomes `OPEN_PUMP_UNITS`: we keep nothing.
    Nothing else in the plan moves -- one slot's quantity, on a row whose op
    and argument are already SELL WHEAT -- and the array is copied rather than
    written through, so the caller's plan is never mutated under it.
    """
    if not open_pump_tell_armed(day, hour):
        return plan
    w = buy_row_slot(B_WHEAT)
    mkt_op, mkt_a, mkt_q = plan[3], plan[4], plan[5]
    if (int(mkt_op[O.TURN_BUY, w]) != O.MO_SELL
            or int(mkt_a[O.TURN_BUY, w]) != spec.I_WHEAT
            or int(mkt_q[O.TURN_BUY, w]) != OPEN_PUMP_UNITS - OPEN_PUMP_KEEP):
        return plan
    # Our own 53 are known, so what is left of the draw is theirs.
    theirs = (spec.MARKET_I0 - int(np.asarray(mkt_inv)[spec.I_WHEAT])
              - OPEN_PUMP_UNITS)
    if theirs < OPEN_PUMP_TELL_MIN:
        return plan
    qty = np.array(mkt_q, np.int32)
    qty[O.TURN_BUY, w] = OPEN_PUMP_UNITS
    return tuple(plan[:5]) + (qty,) + tuple(plan[6:])

# ---- ANIMAL_SAME_DAY: offer the day's shear on the day's last lot -------
# [SWITCH, OFF, SELL-LOT] Default OFF and measured on 68 band boards before it
# is anything else. The mechanism is in the block itself (`_market_rows`'s
# sale section): the dawn allocator sizes the day's lots against the HOUR-0
# shed, so wool, milk and eggs collected during the day are offered by no row
# of that day and sell on tomorrow's opening instead. Fertilizer and melon
# each have a bespoke patch for the same defect; the animal products have
# none.
ANIMAL_SAME_DAY_ON = False

# ---- BANK_BEFORE_LOT: bank the morning's harvest before lot 2 [SWITCH, OFF]
#
# THE WALL, measured (`scratchpad/hour0b/report.txt`, arm A21). The champion's
# harvests ride home in the units' hands until `_end_of_day` dumps them, so
# every one of the day's own lots sells yesterday's shed and nothing else: lot
# 1 (turn 1 under `EARLY_SELL_ON` mode "A") already carries virtually the whole
# of it, which is why moving lot 2 up to turn 4 was measured *identical* to
# leaving it on turn 10. The sell-hour ledger prices "our goods on the market
# before the opponent's" at 41k a season; `EARLY_SELL` collected 2.2k of it by
# moving yesterday's shed two hours earlier. What is left is today's harvest,
# and the only way it reaches today's market is an explicit mid-day DROP.
#
# Two attempts stand above this one and both are read into the design:
#
#   * `MIDDAY_DROP_ON` cut the whole crew's `turn_budget` to `SELL_TURNS[-1] +
#     1` and gave every block a return leg -- -1,157 a game, t -11. Its own
#     post-mortem names the fix: "let a unit keep working *after* its DROP, so
#     the return leg costs the walk and not the tail of the day."
#   * `MELON_OPEN_ON` built exactly that -- a per-unit *excursion* inside
#     `_routes`, `2 * DIST_SHED + 1` turns out of one block, the day's budget
#     untouched -- but triggered it on a crop and placed it after the block's
#     *last* melon rank, so the drops landed at hours 13-17 and the melon rows
#     at hours 12/14 quoted an empty shed.
#
# So this switch is that machinery with the trigger rewritten from crop to
# **time and value**, which is what the excursion was always about:
#
#   1. **Time.** A rank `j` is a candidate only if the DROP that follows it
#      lands on or before `O.SELL_TURNS[1]` -- `start_u + cu[j] + DIST_SHED[j]
#      <= 10`, where `start_u` is the unit's own first turn (`route_base` plus
#      its pickup lead) and `cu[j]` its block clock. A unit acts before its
#      turn's market [LAW], so a DROP *on* turn 10 is in the shed when lot 2
#      resolves; `drop_turns`' docstring is the same reading one lot later.
#   2. **Value.** The block has to be carrying `BANK_MIN_VALUE` coins of
#      harvest at today's quotes by then -- `cval[j] - cval[s-1]`, the banked
#      yield of the harvest chains in `[s, j]` priced at `view.price`. Below
#      that the walk is not worth its turns.
#   3. **The carry.** OP_DROP dumps the unit's *entire* inventory
#      (`sim/units.py`), so a rank is a candidate only if nothing in `(j, e]`
#      consumes a PICKUP -- otherwise the excursion would dump the feed wheat
#      and the fertilizer the rest of the block was carrying, and every FEED
#      and FERTILIZE after it would no-op. `TAIL_CARE`'s own wheat carry is
#      re-based on the drop for the same reason.
#   4. **The cheap leg only.** `2 * DIST_SHED[j] + 1 <= BANK_MAX_TURNS`. The
#      time rule alone admits a leg of fifteen turns on a far tile, which is
#      `MIDDAY_DROP_ON`'s mistake with extra steps.
#
# Among the candidates the excursion goes after the **largest** rank, i.e. the
# most value the window can bank, and the reserve is priced at that rank alone
# -- `_cut` is re-taken against `bud - res` and the excursion is dropped
# altogether if the recut no longer reaches the rank it was priced for.
#
# The second half is the sale, and without it the first half banks nothing:
# `avail` is the hour-0 shed and `SELL.allocate` runs once at dawn, so a lot
# whose row was sized before the DROP sells what the dawn shed held and leaves
# the banked units standing. What the excursion banks is therefore added to lot
# 2's row in bulk, exactly as `DROP_ON` adds its own return leg's `gain` to lot
# 3's: asking for more than arrives costs nothing (every SELL is clipped to the
# shed unit by unit in both the engine's `_commit_unit` and the simulator's
# `market._inventory_orders`), and a re-run of the allocator over a projected
# shed would cost more throughput than the curve it recovers.
#
# OFF, `bank` is `None`, `_routes` compiles no excursion and returns `banked`
# as `None`, and `lots` is the allocation it always was, so the champion theta
# decodes byte for byte (`tests/test_bank_before_lot.py`, pinned against the
# *current* default -- `EARLY_SELL_ON` included).
#
# MEASURED 2026-09-03, real engine, `flow58_g450`, 48 seeds x 2 seats x
# (kagg2 + three class-A tapes), `--seed-base 777001`, n=384, paired on
# (seed, opponent, seat) against the shipped default:
#
#     ALL   +191 a game, sd 1,800, t 2.07 | win 64.6% -> 64.1%
#     kagg2 +103 (t 2.9) | tapes +66 (t 2.3), +251 (t 1.1), +342 (t 1.2)
#     187 of 384 games IDENTICAL
#
# **Not rejected, and not worth promoting: the trigger cannot fire.** The bar
# was ALL >= +1,500 with t >= 2, and the switch clears the t but misses the
# effect by an order of magnitude, because half the games are the same game.
# The excursion runs 0.67 times a *game* and moves 3.4 units into lot 2.
#
# The ledger says why, and it is a fact about the route and not about this
# switch (810 active unit-days of one real game, every rule counted):
#
#     ranks in a block                                     5.01 mean
#     ... whose DROP still makes turn 10                   0.29  (28% of days)
#     ... and whose leg costs <= BANK_MAX_TURNS            0.29  (28%)
#     ... and owe no PICKUP after them                     0.04  ( 3%)
#     coins in hand at the best surviving rank             0 (max 0)
#     coins in hand at the best time-feasible rank        32 (>=400 on 3.2%)
#     coins the whole block harvests                     505 (>=400 on 49%)
#
# Two walls, and the second is the real one. The crew starts at turn 3 on
# average, so a DROP that makes turn 10 has to leave after one or two ranks --
# and a block that owes a FEED or a FERTILIZE later cannot DROP at all, which
# is 28% -> 3%. What survives is carrying **nothing**: the value is real (505
# coins a block) but it lands in the second half of the block. The day's
# harvest is not in the units' hands before hour 11, so there is nothing to
# put in front of the opponent at that hour, whatever the excursion costs.
#
# The lot ledger from the same replays makes the same point from the market
# side -- units offered a game, ours, OFF: **hour 2 (lot 1) 772.7, hour 11
# (lot 2) 9.3, hour 19 (lot 3) 475.7**. Lot 2 is structurally dead in this
# planner and not only for want of stock: `SELL.allocate`'s pressure term and
# its later-lot externality make the greedy either sell at once or wait for
# the deepest shop recovery, so what it holds back it holds back to lot 3.
#
# `BANK_LOT = 2` is the variant that answers it from the other side: the same
# excursion against lot 3's turn, a window wide enough to hold a whole block.
# It fires 13 times a game instead of 0.67 -- and it **loses**. Same seeds,
# 24 x 2 x 4 = 192 pairs: ALL -1,257 (t -1.30), kagg2 -1,234, no game
# identical. (At n=64 it read +461, t 0.31; the n=192 leg is what it is.)
# Which is `MIDDAY_DROP_ON` again in a cheaper shape: a leg taken late enough
# to be worth banking is a leg taken out of the block that would have earned
# more by carrying on, and hour 19 is behind every opponent anyway.
#
# VERDICT 2026-09-03: OFF. The excursion machinery is correct and inert; what
# has to change first is the route order, so that a block's harvest ranks come
# before its carried-input ranks and the value is in hand while the early lot
# is still ahead.
#
# VERDICT 2026-09-09: **ON**, and only as one half of a pair with
# `TAIL_FILL_ON` -- never alone. The 2026-09-03 read stands (this switch by
# itself is +165 HELD42 / +209 LEG20 / +166 LOSS12 in the sim, all inside the
# noise); what changed is that the two switches do not interfere, so the pair
# is almost exactly their sum and clears the leg-family bar together. Sim
# sweep, 128 pinned held-out boards, both seats, paired
# (`docs/strategy/2026-09-09-switch-sweep.md`): pair HELD42 +817 (t 3.50,
# +2 flips / -0 drops), LEG20 +1,404 (t 2.70), LOSS12 +575. Engine
# confirmation (`docs/strategy/2026-09-09-plateau-review-verdicts.md` Sec. 32):
# HELD-OUT +2/-0, H_dm +801, LEG20 +1,403 a game. This half carries the LOSS12
# side the filler loses (`TAIL_FILL_ON` alone is -354 there). Shipped with
# theta `flow166_g170` (`docs/strategy/2026-09-10-ship-pair.md`).
BANK_BEFORE_LOT_ON = True

#: Coins of harvest a block must be carrying before the excursion is worth its
#: walk, at today's quotes. A wheat tile at a mid-season yield is worth ~60
#: coins, so 400 is roughly "six harvested tiles in hand".
BANK_MIN_VALUE = 400

#: Ceiling on the excursion's own cost, `2 * DIST_SHED + 1` turns. The time
#: rule admits `DIST_SHED` up to 7 on an early rank, and a fifteen-turn leg out
#: of a twenty-two-turn day is `MIDDAY_DROP_ON`'s loss rebuilt. Nine turns is
#: `DIST_SHED <= 4`, a little above the board mean of 3.6.
BANK_MAX_TURNS = 9

#: Which lot the banked units are offered in, and so also the turn the DROP has
#: to beat -- one constant for both, because a row the drop cannot reach is a
#: row that sells nothing. Lot 2 (`O.SELL_TURNS[1]`, turn 10, recorded hour 11)
#: is the earliest row the DROP can reach and the only one still in front of
#: kagg2's hour-17 dump. 2 is the measured and rejected variant: a window wide
#: enough to hold a whole block, at hour 19, behind everyone (verdict below).
BANK_LOT = 1

assert not ENDROUTE2_SPLIT_ON or BANK_BEFORE_LOT_ON, \
    "ENDROUTE2_SPLIT's first dump IS the BANK_BEFORE_LOT excursion, on day 29"

# ---- HARVEST_FIRST: harvest ranks before pickup ranks, inside a block -----
# [SWITCH, OFF]
#
# `BANK_BEFORE_LOT_ON`'s post-mortem (above) found the real wall: a block's
# ranks come off `task_order`'s tier-then-score sweep, which interleaves
# HARVEST/COLLECT ranks (value-producing, hands-filling) with FEED/FERTILIZE/
# PLANT ranks (consume something the BUY row or a PICKUP already loaded) in
# whatever order the value model happens to rank them. So a block's harvest
# sits wherever score put it -- the 810-unit-day census found 0 coins in hand
# at the best rank a DROP could still reach by turn 10, against 505 coins the
# whole block eventually harvests. Nothing is in hand early because nothing
# in the route order says it has to be.
#
# This switch reorders each unit's *already-decided* block -- the tile set
# `[s, e]` `_cut` admits is untouched, so pickup credit, hire credit,
# `covered` and every admission-stage guarantee (`FEED_MANDATORY_ON`,
# `SURVIVAL_WATER_ON`) are unaffected -- into a stable two-group sweep: every
# HARVEST/COLLECT rank first (in the order `task_order` already gave them),
# then everything else, then every FEED/FERTILIZE/PLANT rank last. Ties are
# the block's own order, so a phase that does not move costs nothing and the
# reorder only ever pays for tiles it actually reshuffles.
#
# The reorder is priced honestly against two walls it must not cross. First,
# a block's realized walk under the new visiting order can only ever be
# *longer* than the serpentine's, so a per-unit block takes the new order
# only if its total walk-plus-work still fits inside the turns the block
# already had, `bud - lead` -- the same window `TAIL_CARE_ON` and
# `TAIL_FILL_ON` compete for. A block that cannot afford its own reorder
# keeps the route it always had: no admitted rank is ever dropped to pay for
# this, the extra walk only ever spends turns that would otherwise have gone
# to the tail. Second (added after the first measurement below), the reorder
# also has to leave the block's own *ending* tile no farther from a shed
# access than the unreordered ending was: `task_order`'s index tiebreak
# already keeps a block's last rank close to the shed, and pushing the
# FEED/FERTILIZE/PLANT group to the end tends to end the block on one of
# them instead -- which costs whatever runs after the block (`TAIL_CARE_ON`'s
# walk, a `DROP_ON` return leg) more than the reorder itself ever does. Where
# `BANK_BEFORE_LOT_ON`'s excursion fires on a block this switch also
# reorders, the excursion wins outright -- the two never touch the same
# unit's turns, and `bank`'s own trigger still reads the *unreordered* clock
# (the one entanglement this switch does not attempt).
#
# OFF, `harvest_first` is `None`, `_routes` compiles none of the pairwise
# reorder and every block decodes exactly as it always did, so the champion
# theta decodes byte for byte (`tests/test_harvest_first.py`).
#
# MEASURED 2026-09-03, real engine, `flow58_g450`, 8 seeds x 2 seats x
# (kagg2 + three class-A tapes), `--seed-base 777001`, n=64, paired on
# (seed, opponent, seat) against the shipped default:
#
#     naive (no shed-distance gate)   ALL  -81 a game, sd  407, t -1.60
#     this (shed-distance gated)      ALL  -80 a game, sd  245, t -2.61
#
# The mechanism fires as designed -- one real 30-day season (899009257 vs
# kagg2, `scratchpad/harvest_first/hf_probe.py`) reorders 48% of the 810
# active unit-days once the shed-distance gate is on (66% without it), at a
# mean cost of 0.28 extra turns when it fires (0 on 82%), and the gate holds
# exactly: never leaves a block ending farther from the shed. The variant
# tightens the noise (sd 407 -> 245) without changing the sign: reordering
# a block's *own* turns is close to free, but it is not the whole cost of
# reordering a block, and this switch has not found the rest of it.
#
# VERDICT: NOT CONFIRMED, AND THE SWITCH IS SHIPPED OFF. Both the naive
# reorder and the shed-distance-gated variant lose at n=64 (bar was ALL >= 0
# to continue to n=384); neither reached the ladder's next rung. The reorder
# itself is nearly free in the one dimension this switch prices honestly --
# extra walking turns on the block's own admitted set -- so the loss is not
# a walking-cost story, at least not the block's own walk. The remaining
# candidate is downstream of the block: a FEED or FERTILIZE moved later in
# the day may bank a unit's production later too (a chain re-run after the
# block, TAIL_CARE's own feed/care windows, next-day timing), and this
# switch has no instrument on that. See
# `scratchpad/harvest_first/report.txt` for the full ledger and paired
# tables.
HARVEST_FIRST_ON = False

#: Measurement-only hook (2026-09-03): a list, or `None`. Not `None`, and
#: called with `xp=np` (untraced), `_routes` appends one dict per unit-day to
#: it -- `scratchpad/harvest_first/hf_probe.py`'s ledger. No effect on the
#: compiled (jitted) path, which never runs this branch's Python-level
#: `int(...)` calls; left in place the way `BANK_TRACE` was for the switch
#: above, and dropped before ship.
HF_TRACE = None

# ---- ROUTE_ORDER: sweep a block's own tiles, not the day's rank order ------
#
# ROUTEEFF's per-hand-day STEP ledger (`docs/strategy/2026-09-16-routeeff.md`)
# closed the development-order lever and named what was left: `mid_move`, the
# walk BETWEEN a unit-day's ops, is the largest term of the d20-29 volume gap
# (8.93 moves a unit-day to the engine class's 8.19, +4,290/board at spot) and
# 92.5 % of it is the intra-block VISITING order, which no module constant
# reaches. This switch is that order.
#
# A block's ranks are worked in `order` -- the day's tile ranking, whose job is
# to decide WHICH tiles are worth a turn, not which way round to walk them.
# Measured on the 22 ENG22 boards (`S/routeorder/ceiling.py`, 2,572 d20-29
# unit-days, the ordered op path of every unit of every day, both seats): our
# route spends 10.18 moves a unit-day where the walk-minimal order of the SAME
# tiles, with every shed interaction pinned where it is, spends 8.79 -- 1.39
# moves a unit-day, +7,372/board at spot 1:1 (+3,546 at the measured 2.211
# steps/op). A block-local BOUSTROPHEDON -- the block's own tiles swept in
# rows (or columns), each row taken in the opposite direction to the one
# before it -- recovers 1.25 of those 1.39 (90 %), and that order is a static
# per-rank sort key, which is the one thing the traced route compiler can
# express. A single fixed key recovers nothing (-0.01: the day's order already
# IS a serpentine); the orientation is the whole lever, so the switch computes
# all four (rows/columns x either end) and takes the cheapest.
#
# The saving is spent, not banked: a block that walks `sav` turns less is recut
# against `bud + sav` and the ranks the wider cut admits are worked under the
# same sweep, verified against the real window (`total <= bud - lead`) before
# it is taken -- so no admitted rank is ever unreachable, and a block whose
# extension does not fit keeps the block it had. Every guard `HARVEST_FIRST_ON`
# priced stays: the reorder is refused unless it is strictly shorter than the
# order it replaces, unless it fits the turns the block already had, and unless
# it leaves the block's last tile no farther from a shed access than the
# unreordered ending would have (the 2026-09-03 census: the naive reorder gives
# that up on 36 % of the blocks it touches and erases its own benefit). A block
# an excursion fires on (`MELON_OPEN_ON` / `BANK_BEFORE_LOT_ON`, `ins > 0`) is
# never reordered -- the two mechanisms never touch the same unit's turns.
#
# Pickup-before-use is untouched by construction: a block's PICKUPs are its
# *lead*, charged before its first rank (`d_lead`), so no permutation of the
# ranks can move an op in front of the pickup that loads it.
#
# OFF, `route_order` is `None`, `_routes` compiles none of this and the
# champion theta decodes byte for byte (`tests/test_routeorder.py`).
ROUTE_ORDER_ON = False

#: [ROUTE_CUT] The block ASSIGNMENT rather than the block's visiting order.
#: `_cut` takes the LARGEST rank whose block fits the budget, so the boundary
#: between two adjacent units falls wherever the turn budget happens to run
#: out. That boundary is worth coins on its own: with `s_u` the first rank of
#: unit u, the crew's whole walk for the day is
#:
#:     sum_{j<=E} move[j]  +  sum_u base_move_u  -  sum_{u>=1} move[s_u]
#:
#: -- every hop of the ranked order is walked exactly once EXCEPT the hop into
#: each block's first rank, which the unit replaces by the leg from its own
#: spawn. So for a fixed coverage `E` the only thing the boundary changes is
#: `base_move_u - move[s_u]`: a boundary is cheap where the next unit's spawn
#: is CLOSE to the rank it starts on and the hop it skips is LONG. Nothing
#: today looks at either quantity.
#:
#: The switch pulls a block's end back by at most `ROUTE_CUT_LOOK` ranks when
#: that hands the next unit a strictly cheaper entry AND the entry is worth
#: more than what the pull-back strands. The ranks given up are not lost --
#: `start = end + 1`, so they are the next unit's first ranks -- but the turns
#: THIS block frees are: the greedy cut had nothing else to spend them on, so
#: the whole chain ends `cu[e] - cu[c]` turns earlier. Taking the boundary on
#: the entry term alone therefore LOSES, and by a mile: ENG22 -14,987/board,
#: t -11.6, board win 40.9 -> 13.6 % (2026-09-16, the first arm of this box).
#: The rule below prices the stranded turns against the entry saving, so the
#: recut fires on a long serpentine hop next to the successor's spawn and
#: nowhere else.
#:
#: Every guard of `ROUTE_ORDER_ON` is kept, and the shed gate is kept in its
#: strongest form: the block may only end on a rank no farther from a shed
#: access than the one it ends on today (`hf_dist`), and it can only end
#: EARLIER on the block's own clock (`c <= end`, `cu` monotone), so the DROP
#: leg and any excursion deposit land on the same turn or sooner -- the one
#: direction that cannot be wrong. A block an excursion fired on (`ins > 0`)
#: is never recut, the last working unit is never recut (it has no successor
#: to hand the ranks to), and the intra-block order is untouched.
#:
#: OFF, `route_cut` is `None`, `_routes` compiles none of it and the champion
#: theta decodes byte for byte (`tests/test_routecut.py`).
ROUTE_CUT_ON = False

#: How many ranks a block's end may be pulled back. The boundary term is a
#: single hop, so the window only has to reach the nearest long one.
ROUTE_CUT_LOOK = 3

#: `ROUTE_ORDER_SHED_GATE`'s rule on the assignment: the recut is refused if it
#: ends the block farther from a shed access than today's cut does. `task_order`
#: already keeps a block's last rank near the shed, so this is the gate that
#: does most of the refusing; `False` is the diagnostic arm that says whether
#: the gate or the price is what closes the lever (2026-09-16: neither -- both
#: arms are byte-identical on 44 ENG22 games).
ROUTE_CUT_SHED_GATE = True

#: `HARVEST_FIRST_ON`'s shed-distance gate, inherited: a sweep is refused if it
#: leaves the block's last tile farther from a shed access than the rank order's
#: own ending would have (the 2026-09-03 census measured the naive reorder
#: giving that up on 36 % of the blocks it touches, +0.41 tiles). It is a
#: heuristic, not a law, and it is expensive here: on the 22 ENG22 boards it
#: cuts the reachable sweep saving from 1.250 to 0.169 moves a unit-day
#: (`S/routeorder/gatevar.py`), 50 % of segments improvable down to 9 %.
ROUTE_ORDER_SHED_GATE = True

# ---- TILE_ALLOC: a per-TILE work assignment, not a prefix cut [SWITCH, OFF] -
#
# ROUTEORDER measured the intra-block visiting order (+433/board, ships OFF)
# and ROUTECUT proved the block boundary itself can never buy walk: `_cut`
# hands each unit a CONTIGUOUS PREFIX of the day's ranked `order`, and a
# boundary move gains at most `-sum n_ops` of the ranks it strands
# (`docs/strategy/2026-09-16-routecut.md` section 1).  What the two legs left
# is the assignment at TILE level -- one unit working a tile out of the MIDDLE
# of its neighbour's block -- worth, with every shed interaction pinned to the
# turn it lands on today and only ADJACENT units trading,
# `S/tilealloc/ceiling.py`: +2,915/board with the tile inserted wherever it is
# cheapest, +1,932/board with it inserted where its RANK puts it (0.334 moves
# a unit-day), against +893 at the measured 2.211 steps per prod op.
#
# The mechanism here is the rank-faithful half of that: after the cut, a unit
# with idle turns left over STEALS a pickup-free rank out of the block ahead of
# it and appends it to its own walk, and every later unit skips it.  The
# stealer pays `dist(last tile, j) + n_ops[j]` out of turns the greedy cut
# could not spend; the unit that had `j` saves `seg[j] + move[j+1] -
# dist(j-1, j+1)`, and the transfer is refused unless that saving is strictly
# larger -- so the day always spends strictly FEWER turns on the same work, and
# the turns the loser gets back are recut into more ranks (the same "spend the
# saving" pass `ROUTE_ORDER_ON` runs).  The block a unit works is then a
# contiguous prefix with holes, plus the ranks it stole: `_ro_block`'s mask
# decode takes any subset and a rank key keeps it in `order`, so nothing about
# the emitted route's shape changes.
#
# Guards: only pickup-free ranks move (a carried input is charged as its
# block's LEAD, so `d_pick`, `d_lead` and `blk` are untouched by the
# transfer); never on an excursion day (`MELON_OPEN` / `BANK_BEFORE_LOT` price
# their reserve off the block's own clock); never from the last working unit
# (no successor to take the ranks from); the block's real swept total, return
# leg included, must fit the turns the block already had; and the shed gate in
# `ROUTE_ORDER_SHED_GATE`'s form -- the block may not END farther from a shed
# access than its cut ends today.  `covered` carries the stolen ranks, so the
# admission repair sees the work exactly where it is done.
#
# OFF, `tile_alloc` is `None`, `_routes` compiles none of it and the champion
# theta decodes byte for byte (`tests/test_tilealloc.py`).
TILE_ALLOC_ON = False

#: How many ranks a unit may steal per day. One is the measured shape: the
#: turns the greedy cut leaves over are less than the cost of the next rank.
TILE_ALLOC_PASSES = 1

#: How far ahead of its own block a unit may look for a tile to steal.
TILE_ALLOC_LOOK = 12

#: `ROUTE_ORDER_SHED_GATE` on the transfer: refused if it leaves the block
#: ending farther from a shed access than the cut's own ending.
TILE_ALLOC_SHED_GATE = True

# ---- PRESTOCK: buy tomorrow's shed inputs tonight [SWITCH, OFF] -----------
#
# Measured on 39 real-engine replays: our units PASS 18.5% of their turns
# against 8% for the strong opponents, and a third of ours is the whole crew
# standing on its spawn tiles at hours 0-2 waiting for the BUY row -- 390
# unit-turns a game against an opponent's 34. The cause is structural, not a
# valuation miss: `TURN_BUY` is 1 and a unit acts *before* its turn's market,
# so `ROUTE_BASE` cannot be 1 while the morning's PICKUPs depend on the row.
#
# The row does not have to be in the morning. `_end_of_day` banks the shed
# (`sim/eod`: `drop_inventories` adds to it, nothing clears it) and `seeds` is
# not touched at all, so anything bought tonight is there at hour 0. So on day
# d, at `O.TURN_PRESTOCK` = 20 -- free, after the last lot, before nightfall --
# the day places tomorrow's BUY_PRODUCT row (feed wheat, fertilizer) and, with
# `PRESTOCK_SEEDS`, a BUY_SEED row beside it; day d+1's turn-1 row carries only
# the residual. The seed half is measured and **rejected** -- see the constant
# below -- so v1 prestocks products alone, and a day that buys seed keeps
# today's schedule like a day that buys an animal.
#
# **BUY_ANIMAL stays at turn 1.** An animal *is* stocked -- `_market` buys it
# into the shed and a unit PICKUPs and PLACEs it (`PICK_ITEM`) -- so it could
# be prestocked; it is not, because the herd mix is a same-day policy output
# (`macro.animal_want`) that today cannot forecast, and an animal held
# overnight is 1..n of the 100 shed units the eod dump needs. Days that buy an
# animal keep today's law, and that is most of what this switch does not reach.
#
# Forecast: persistence on what the day itself *realised*, netted against a
# per-product projection of tonight's shed -- `need - (shed + bought - sold -
# picked up + reached inflow)`, clipped at zero. `want_feed` count for wheat,
# `n_fert_eff` for fertilizer, and the seeds the route actually planted.
# Emphatically **not** `macro.plant_target` for the seeds: that is the raw gene
# want before `_wants` clips it to the tiles that will exist and before the
# labour boundary cuts it, so a farm with no free slots and a large target buys
# a full target's seeds every night and plants none -- 0/24 games and -90,845
# mean margin, the purse gone by day 1. Reading the realised plantings instead
# is what the code does and it is still not enough (-90,863, same 24 games),
# which is why the seed row itself is off; `PRESTOCK_SEEDS` has the autopsy.
# Every forecast here is a quantity the day performed, and all are
# self-correcting: over-buying raises
# tomorrow's stock and lowers tomorrow's prestock, under-buying leaves a
# residual row that day d+1 buys at turn 1 exactly as it does today.
#
# Overnight price risk is bounded and *favourable* under the planner's own
# opponent-free model (`projector`): the town drains inventory every tick and
# price is monotone non-increasing in inventory, so a buy quote at turn 20
# is never dearer than the same quote at turn 1 tomorrow. What is not free is
# shed room, so the prestock is clipped to `SHED_CAPACITY - proj_eod`; and
# cash, so it spends only `purse - what the day's own greedy took`, a purse
# already net of the hire bill and `cash_reserve` [LAW, 1.5] -- the reserve can
# therefore not be breached, and a purse that cannot cover the whole want buys
# a prefix of it (wheat, fertilizer, then seeds) rather than nothing.
#
# The schedule law it buys, and the only place the coins come back: on a day
# whose residual BUY row is *empty*, nothing has to resolve at turn 1, so the
# overflow hire row moves from turn 2 to turn 1 and every unit starts a turn
# earlier -- `ROUTE_BASE_PRE` = 1 / `ROUTE_BASE_WIDE_PRE` = 2, +1 worked turn
# per unit-day. Global, not per unit: `route_base` is one traced scalar the
# whole crew's route is laid out from, and `ops.ROUTE_BASE_WIDE`'s comment
# explains why a crew that starts at two different turns re-scatters every
# later hand's spawn tile. Tomorrow's prestock is not known when today's plan
# is built, so the emptiness is read off the day's *own* residual row.
#
# Nothing is prestocked when tomorrow is terminal (`day >= O.LAST_SHED_DAY`):
# past `terminal` no purchase can mature, and day 29 buys nothing at all.
#
# MEASURED 2026-08-30, a 12-seed x 2-seat smoke against kagg2 (`--seed-base
# 20260830`, champion theta, DROP + HORIZON on in both arms), paired on
# (seed, seat) against the same build with the switch off:
#
#     win 83.3% (100% off) | mean coins 103,472 (99,263 off)
#     mean margin +10,367 against +10,702
#     paired diff -334, sd 7,707, t = -0.21, 95% CI [-3,418, +2,749]
#     15 games up, 9 down, 0 unchanged; range -13,654 .. +14,770
#     discordant: 0 games won that the baseline lost, 4 lost that it won
#
# Read that honestly: **indistinguishable from zero at n = 24**, and its two
# halves point opposite ways. Our own coins are up 4,209 a game -- the extra
# turn is real work done -- but so are kagg2's, because the wheat we buy at
# turn 20 drains supply the other seat sells into the next morning, and a
# margin is a difference. The paired sd is 7,707 against DROP's 581: this is a
# whole-season perturbation, not a last-day one, and 24 games cannot resolve a
# few hundred coins of it. A promotion needs the 96 x 2 run on both seed bases
# the other switches were held to.
#
# OFF is the default and promotion is a separate decision. OFF, no order is
# emitted at `TURN_PRESTOCK`, `route_base` is the expression it always was and
# the hire rows are turns 0 and 2, so the champion theta decodes byte for byte
# -- verified on 12 seeds x 2 seats against `rep/hz_b30.csv`, all 24 rows
# identical in every column, and pinned by `tests/test_prestock.py`.
PRESTOCK_ON = False

#: Whether the prestock row also carries BUY_SEED [SWITCH inside a SWITCH, OFF].
#:
#: **Measured and rejected, 2026-08-30**: 12 games x 2 seats against kagg2,
#: `--seed-base 20260830`, champion theta, paired against the same build with
#: `PRESTOCK_ON` off -- win 0.0% against 100%, mean margin -90,863 against
#: +10,702, every one of the 24 games lost. The trace says why (day 0 of seed
#: 480603619): the morning grant buys 10 wheat and 9 carrot seeds out of the
#: 3,000-coin opening purse, the night then buys 10 wheat and 4 carrot more,
#: and day 1 opens on **28 coins**. The farm never recovers.
#:
#: The defect is the forecast and not the schedule. Feed wheat and fertilizer
#: are genuinely recurring -- every animal eats every day, every application
#: renews -- so "tomorrow wants what today wanted" is a real persistence claim.
#: Planting is not: it fills free land once, so today's plantings forecast
#: tomorrow's only while free tiles last, and on the day the farm fills its
#: land the forecast is exactly wrong. Worse, it is wrong in the most expensive
#: direction -- an early coin compounds through the whole season, and
#: `purse_left` is at its largest precisely early, when the greedy has few
#: tiles to want anything for.
#:
#: What a future attempt needs first: a bound on tomorrow's *plantable slots*
#: (`n_free - plant_eff` and what tonight's weeds do to it), so the seed want
#: is the land's and not the day's. Until then the seed row is off and the days
#: that buy seed keep today's schedule -- which is most of the switch's reach,
#: and is stated plainly rather than hidden in the numbers.
PRESTOCK_SEEDS = False

# ---- PRESTOCK_V2: the prestock row without the turn-1 collision [SWITCH, OFF]
#
# `PRESTOCK_ON` above has never been measurable on the shipped tree. Two
# asserts refuse it, and both are about ONE row -- turn 1 -- and none of them
# is about the purchase:
#
#   * `assert not (EARLY_SELL_ON and (MARKET_PACK_ON or PRESTOCK_ON))` (below,
#     module scope). `EARLY_SELL` mode "A" gathers lot 1 into the FREE SLOTS of
#     the turn-1 BUY row (`_market`, "lot 1 behind the BUY row"); `PRESTOCK`
#     moves the overflow HIRE row INTO turn 1 on exactly the days that row is
#     free (`hire_wide_early`, `_market`), and writes the whole row rather than
#     merging. Two writers, one row: the lot would be overwritten in silence.
#   * `assert hire_wide_early is None, "OPEN_PUMP owns turn 1; PRESTOCK's
#     overflow hire row takes it"` (`_market`, trace time). `OPEN_PUMP`'s
#     sell-back leg is index 0 of that same turn-1 row.
#
# Both subjects are `hire_wide_early`, and `hire_wide_early` only ever carries
# anything on a WIDE day: it re-seats `rest = max(n_hire - MO, 0)`, which is
# zero for a crew of ten or fewer. So the minimal legal reconciliation is not
# to delete either assert -- it is to give up the wide day. V2 fires on NARROW
# days only, passes `hire_wide_early=None`, and then neither assert has a
# subject: turn 1 keeps exactly the writers it has today (the BUY row, the
# pump's sell-back, `EARLY_SELL`'s lot 1), and the purchase sits alone at
# `O.TURN_PRESTOCK` = 20, a turn no other row uses.
#
# What is left is the half the coins were ever in (`2026-09-14-turns.md` 7):
# on a day whose residual BUY row is empty the whole crew starts at
# `O.ROUTE_BASE_PRE` = 1 instead of 2 -- one more worked turn per unit-day, and
# the morning PICKUP rows move with it, which is legal precisely because last
# night bought what they pick up. `route_base` moving off the law's own value
# switches `route_split` off for that day by its own gate, so the turn is
# handed over, never taken twice (`2026-09-11-route-early-bug.md`).
#
# Narrow-only costs nothing that was measurable anyway: the wide-day version
# needs `ROUTE_BASE_WIDE_PRE` = 2, and a unit stepping at turn 2 re-scatters
# every hand the turn-2 HIRE row spawns [LAW, ops.ROUTE_BASE_WIDE].
#
# OFF is the default and this is one more default-off switch: off, `pre_*` is
# `None`, `route_base` is the expression it always was, `farmer0` is `None` and
# `_routes` compiles none of the extra cut (`tests/test_prestock_v2.py`).
PRESTOCK_V2_ON = False

#: The farmer's own hour 0, under V2 [SWITCH inside a SWITCH, OFF].
#:
#: Unit 0 is not hired -- no "a hand hired in turn t acts in t+1" law reaches
#: it -- so the only thing holding it at turn 0 is `ops.ROUTE_BASE_WIDE`'s
#: spawn-occupancy law: turn 0's HIRE row resolves AFTER turn 0's unit phase,
#: so a farmer that has STEPPED by then moves every hand `_spawn_hand` places.
#: A PICKUP does not step -- it is taken standing on the shed-access tile and
#: is silently dropped anywhere else -- so a farmer whose block opens with a
#: PICKUP may take that PICKUP at turn 0 and leave the occupancy count exactly
#: as `plan.SPAWN_SLOT` predicts it. That is the op `ymg_aq`'s hour-0 farmer
#: issues (`2026-09-14-turns.md` 0), and B's hour 0 is 100 % PASS, 30.0
#: unit-turns a game.
#:
#: It reuses `_routes`' existing per-unit `early` channel (the one
#: `ROUTE_SPLIT_ON` fills), so the extra turn is a turn of WORK -- the block is
#: cut against `bud + 1` -- and not merely an earlier finish. Gated on the
#: same day predicate as V2 plus `land_lead == 0`: a land day's quadrant does
#: not exist before `SELL_TURNS[0]`'s market phase [M2], and the shift moves
#: the block's first TASK op as well as its pickup.
#:
#: The hire enumeration is NOT credited with this turn (`route_turns` above
#: adds V2's crew turn and nothing else): one unit-turn on a crew of up to
#: eleven is inside the estimate's noise, and under-admission is the safe
#: error -- `ADMIT_ROUNDS` drops what the route cannot reach and nothing ever
#: adds a tile back.
PRESTOCK_V2_FARMER0_ON = False

#: Whether V2 also emits the purchase [SWITCH inside a SWITCH, ON].
#:
#: The switch has two halves that cost and pay separately. The PURCHASE (this
#: one) spends `purse_left` at `O.TURN_PRESTOCK` on every day there is a
#: tomorrow, wide crews included; the SCHEDULE turn is only handed back on a
#: NARROW day whose residual BUY row is empty. B fields eleven hands on roughly
#: half its season (`2026-09-14-turns.md` 5), so the two halves do not cover the
#: same day-rows, and an arm that flips both cannot say which one moved.
#: `PRESTOCK_V2_BUY_ON=False` is the schedule half alone: no order at
#: `TURN_PRESTOCK`, `route_base` still `O.ROUTE_BASE_PRE` on a day the day's own
#: plan already leaves turn 1 empty. It is the falsifier for "the morning turns
#: convert" and it costs nothing to take.
PRESTOCK_V2_BUY_ON = True

# ---- ROUTE_EARLY: start the units the BUY row does not hold [SWITCH, OFF] --
#
# The same 390 idle unit-turns `PRESTOCK` was written for, attacked from the
# other side. That switch moved the *purchase* off turn 1 and was rejected in
# the real engine: buying at `TURN_PRESTOCK` drains the pot the other seat
# sells into next morning, so our coins went up and the margin did not. This
# one moves nothing in the market at all. Not one order changes turn, quantity
# or slot; only which turn a unit's own route starts on.
#
# What actually holds a unit at its spawn tile is not the day, it is the
# *block*: `route_base` is one scalar the whole crew is laid out from, and it
# is 2 because a block whose first act is a PICKUP has to wait for the row that
# resolves in turn 1's market phase. A block that picks nothing up owes that
# row nothing. Its first act is a step out of the shed, which depends on
# neither a coin nor an item, and it can be taken at `O.TURN_BUY` while the
# purchase is still pending -- the day's other blocks keep waiting for it.
#
# So the start is per unit, and the extra turn is a real turn of work: a unit
# that starts at 1 keeps its last turn as well, so `_routes` cuts its block
# against `turn_budget + 1`.
#
# Three conditions, and every one of them is a law rather than a tuning:
#
#   1. **No second hire row** (`~wide`). `ops.ROUTE_BASE_WIDE`'s comment is the
#      reason: `_hire` spawns a hand on the least-occupied shed-access tile, so
#      "hand h lands on access tile (h+1) % 4" only holds while every unit is
#      still standing where it woke. On a narrow day every hire resolves in
#      turn 0's market phase, after a turn 0 on which nothing may act anyway,
#      so a unit that steps at turn 1 cannot move anybody's spawn. On a wide
#      day the overflow row is turn 2 and a unit stepping earlier re-scatters
#      it, so a wide crew keeps `ROUTE_BASE_WIDE` for all of its members.
#   2. **No land** (`land_lead == 0`). BUY_LAND resolves in `SELL_TURNS[0]`'s
#      market phase and a tile op on a LOCKED tile silently no-ops [M2], so on
#      a land day the lead is what it always was and starting earlier only
#      buys a turn inside the lock.
#   3. **The block owes no pickup** (`d_pick[e] == 0`) **and its first act is a
#      step** (`base_move > 0`). The first is the purchase dependency itself --
#      wheat, fertilizer and every animal reach a unit through a PICKUP, and
#      `blk` is zero for exactly the blocks that own none. The second closes
#      the one hole `_buy_row_units` names: a seed bought at turn 1 is credited
#      after that turn's unit phase, so a PLANT standing at turn 1 would plant
#      nothing. A block whose first tile is not its spawn tile spends turn 1
#      walking, and every op it owns lands at turn 2 or later, exactly where it
#      used to.
#
# What is deliberately *not* changed: the hire enumeration still scores every
# candidate at `route_turns(h)`. Which units come out early is a property of
# the block cut, which does not exist until the crew size is chosen, so the
# scan under-credits the crew by up to a turn a unit. That is the conservative
# direction (it can only hire fewer hands, never more) and it keeps the
# argmax's inputs the ones it already has. The admit stage does take the turn
# on -- `labour` grows by `n_units` on a day the flag allows any of it -- since
# admitting nothing extra would leave the new turn with nothing to spend
# itself on; over-admission is what `ADMIT_ROUNDS` exists to repair.
#
# SMOKE 2026-08-31, and it is a smoke and not an evaluation: 6 seasons in the
# *simulator*, champion theta in both seats, both seats carrying the switch, so
# there is no margin in it and the coins are not a result. What it does measure
# is the idle mechanism, and it reproduces the replay number first (18.8% of
# our unit-turns PASS off, against the 18.5% of the 39-replay autopsy):
#
#     PASS unit-turns   1,196.5 off -> 1,135.0 on   (-61.5 a season, -5.1%)
#     idle share           18.8% off ->    17.8% on
#     per season          -48, -23, -305, -3, -29, +39
#
# One season of six idles *more*, which is the honest shape of it: a crew that
# starts earlier re-cuts every block behind it, so this is a whole-season
# perturbation and not a per-day delta. It also means the turn count is the
# wrong thing to gate on -- on the pin boards the switch does all the same work
# in two fewer walking turns on one of them, which a turn count reads as a loss
# -- so `tests/test_route_early.py` gates on `value_dropped` instead. A
# promotion needs the paired real-engine run the other switches were held to.
#
# OFF, `route_early` is `None`, `_routes` compiles none of the trial cut,
# `early` is all zeros and every start and budget is the expression it always
# was, so the champion theta decodes byte for byte
# (`tests/test_route_early.py`).
ROUTE_EARLY_ON = False

# `ROUTE_SPLIT_ON` [SWITCH]: the same day-start wait, taken per *block* rather
# than per crew, and on the two shapes `ROUTE_EARLY_ON` leaves on the table.
# The 39-replay census (2026-09-01) prices the wait at 375 idle unit-turns a
# game against the 2800-tier tape's 11 -- 100% of our unit-days start work at
# hour 2 or later, the tape's mean first hour is 1.21 -- and `ROUTE_EARLY_ON`
# as written recovers 62 of them, because its three gates exclude most of the
# crew. This switch keeps the two gates that are laws and re-reads the third:
#
#   1. **The wide crew.** `ops.ROUTE_BASE_WIDE` is a law about *movement*:
#      hands 11.. are hired in turn 2's market phase, `market._hire` puts each
#      on the least-occupied shed-access tile, and one unit that has walked off
#      its own access tile before that phase changes the occupancy every later
#      hire is measured against -- so `SPAWN_SLOT` stops describing where the
#      late hands land and their routes are laid from the wrong tile. It says
#      nothing about a unit that *stands still*. A PICKUP is stationary, and
#      the BUY row it consumes has resolved since turn 1, so on a wide day
#      every already-hired unit that owes a pickup may take it at turn 2
#      instead of turn 3 and start its walk at turn 3 where it used to stand
#      idle. That is +1 turn for the pickup-owing half of a wide crew, which
#      `ROUTE_EARLY_ON` (`~wide`, and `d_pick == 0`) gives up entirely.
#      The turn-2 hires themselves are untouched: a hand hired in turn t first
#      acts in t + 1 [LAW], so `O.ROUTE_BASE_WIDE` is already their first turn.
#   2. **The land day** (`land_lead == 0`) stays exactly as it was: BUY_LAND
#      resolves in `SELL_TURNS[0]`'s market phase and a tile op on a LOCKED
#      tile silently no-ops [M2].
#   3. **The purchase dependency** is the one re-read. `ROUTE_EARLY_ON` asks
#      for `base_move > 0` -- the block must *walk* before it works -- to keep
#      a PLANT off turn 1, since a seed bought at turn 1 is credited after that
#      turn's unit phase. But PLANT is the only op a pickup-free block can hold
#      that the BUY row feeds: FEED, FERTILIZE and PLACE all reach a unit
#      through a PICKUP (`_pick_masks`), and WATER, CARE, DIG, COLLECT,
#      HARVEST and BUILD carry nothing. So the gate is "the block's first act
#      is a step *or* an op the row does not feed", and a block that opens with
#      a watering on its own spawn tile comes out at turn 1 as well.
#
# What is *not* recovered, and why: a unit that owes a pickup on a narrow day
# cannot walk at turn 1 and collect at turn 2 the way the census proposed --
# `PICKUP` is silently dropped anywhere but a shed-access tile, so a unit that
# has walked has nothing to collect from -- and its pickups already sit at
# `O.ROUTE_BASE` = `TURN_BUY + 1`, the earliest turn the row can feed them.
# Turn 0 stays idle for everyone for the same reason turn 2 does on a wide day:
# turn 0's hire row resolves after turn 0's unit phase.
#
# ON since 2026-09-03, on two independent 384-game reads of the same paired
# tiebreak (flow58_g450, 48 seeds x 4 opponents x 2 seats, each leg's own OFF
# run as the pair):
#
#     seed base 777001   ALL  +1,896 coins a game  t 3.1   win 53.4% -> 53.6%
#       kagg2 +2,781 (t 1.8), tape 103254816 +1,250 (t 1.2),
#       tape 104502967 +754 (t 0.6), tape 104547425 +2,799 (t 3.3)
#     seed base 777002   ALL  +3,393 coins a game  t 4.9   win 59.1% -> 64.3%
#       kagg2 +1,975 (t 2.0), tape 103254816 +4,882 (t 2.5),
#       tape 104502967 +4,737 (t 4.0), tape 104547425 +1,978 (t 1.7)
#
# Eight opponent legs over the two reads and not one of them is below OFF,
# which is the shape a *turn* buys: the switch adds labour to every day the
# laws allow it and takes nothing from any day, so it is not a trade against
# one archetype. Measured untrained-for -- `flow58_g450` was trained with the
# switch off -- so the enumeration has not yet had a chance to re-price the
# crew against the turn it now gets.
#
# OFF, `route_split` is `None`, `_routes` compiles none of the trial cut,
# `early` is all zeros, `pk_turn` is `route_base` and every start and budget is
# the expression it always was (`tests/test_route_split.py`), which is what the
# digest pins of `test_route_early`, `test_prestock` and `test_tail_fill` hold
# the switch to.
ROUTE_SPLIT_ON = True

# `ROUTE_FREEFIRST_ON` [SWITCH]: `ROUTE_SPLIT_ON`'s narrow rule read per *kind*
# instead of per day. `route_split` hands the morning turn to a block the BUY
# row does not feed, and it proves that by the strongest possible test -- the
# block owes no PICKUP at all (`d_pick[e1] == 0`, `_routes`). That test is the
# per-day one `_buy_row_units` names: it asks whether *anything* rides the row,
# so a block that picks up wheat waits for turn 1 even on a day that buys no
# wheat, and B buys seed nearly every day (`2026-09-14-prestock-repair.md` §5).
# The measured cost is the morning: 236.3 of B's 269.5 hour-1 unit-turns are
# PASS and 210.4 units PICKUP at hour 2 (`2026-09-14-turns.md` §"Where the 695
# turns go"), i.e. the held block is the pickup-owing one, not the walking one.
#
# What the row actually feeds is a *kind*. `PICK_ITEM` is wheat, fertilizer and
# one row per animal; the shed a unit collects from at `TURN_BUY` is last
# night's close (`_end_of_day` -> `_drop_inventories_to_shed`), because turn 1's
# market phase runs *after* turn 1's unit phase -- the same ordering
# `_buy_row_units`' docstring gives for the seed. So a block whose every owed
# kind has a purchase of **zero today** consumes nothing the row is about to
# deliver, and its leading PICKUPs may sit at `TURN_BUY` instead of
# `O.ROUTE_BASE`. A block that owes a kind the day *does* buy keeps the turn it
# has: its quantity is the one the purchase makes available.
#
# The two laws are untouched, which is why this is narrow-day only and needs no
# new base constant:
#
#   1. A hand hired in turn t first acts in t + 1 [LAW, ops.ROUTE_BASE]. A
#      narrow crew is hired at `TURN_HIRE` alone, so `TURN_BUY` is already its
#      first legal turn -- this reaches it, it does not go below it.
#   2. A unit that has *walked* off its shed-access tile re-scatters every hand
#      `_spawn_hand` places afterwards [LAW, ops.ROUTE_BASE_WIDE]. A PICKUP is
#      stationary and a narrow day has no later hire row, so nothing observes
#      the unit at turn 1 anyway. The wide branch is left exactly as it is:
#      there the extra turn is already the stationary PICKUP at turn 2 and the
#      turn below it is the turn-2 HIRE row itself.
#
# PLANT stays behind the row whatever happens. `free_first` keeps a block that
# opens on a PLANT at `O.ROUTE_BASE` when it owes no pickup; when it does owe
# one, its route does not start until `TURN_BUY + d_pick >= O.ROUTE_BASE`, so
# the seed has resolved before the first route op either way.
#
# OFF, `freefirst` is `None`, `_routes` compiles none of the per-kind test,
# `narrow_ok` is the expression `ROUTE_SPLIT_ON` always had and `pk_base` is
# the wide-only shift it always had, so the champion theta decodes byte for
# byte (`tests/test_route_freefirst.py`).
ROUTE_FREEFIRST_ON = False

# ---- WIDE_PICK: the wide day's SECOND stationary pickup [SWITCH, OFF]
#
# `ROUTE_FREEFIRST`'s per-kind test, applied to `route_split`'s **wide** branch
# instead of its narrow one.
#
# A wide day (`n_hire > ops.MO`) hires a second row at turn 2, so no unit may
# step before turn 3 [LAW, ops.ROUTE_BASE_WIDE] -- a unit that has walked off
# its shed-access tile re-scatters every hand `_spawn_hand` places afterwards.
# `route_split`'s wide branch already buys the one turn that law leaves: a
# block owing a PICKUP collects it at turn 2, standing still, and the turn-2
# HIRE row's occupancy count is unchanged because the unit never moved.
#
# Turn 1 is the same kind of turn and it is still empty. `S/widespawn/count.py`
# over the three HOURTRACE tapes: on a wide day **every** live turn-0 unit
# PASSes at turn 1 (143 of 143 unit-days a game), and **45.7 unit-days a game
# own a block that owes TWO or more pickup kinds** (`d_pick >= 2`) -- kind A at
# turn 2, kind B at turn 3, walk at turn 4. Such a block can take kind A at
# turn 1 instead: stationary, so the occupancy counts at the turn-2 hire row
# are bit-identical and `plan.SPAWN_SLOT` still describes the placement
# exactly, and its walk then starts at `O.ROUTE_BASE_WIDE` = 3, which is the
# first turn the law allows it.
#
# What makes turn 1 different from turn 2 is the BUY row. Turn 1's market phase
# runs **after** turn 1's unit phase, so a pickup pulled to turn 1 draws last
# night's shed close (`_end_of_day` -> `_drop_inventories_to_shed`) and not
# today's purchase. That is exactly `ROUTE_FREEFIRST`'s per-kind test
# (`2026-09-14-route-freefirst.md`), and it has to hold for the kind that
# actually lands on turn 1 -- `pk_turn` stamps the rows in `PICK_ITEM` order
# (wheat, fertilizer, one per animal), so the kind on turn 1 is the block's
# **lowest-indexed** owed kind and no other. `S/widepick/count.py` prices the
# filter: 41.3 of the 45.7 unit-days own at least one free kind, but only
# **30.7** own a free *first* kind, and 30.7 is the arm.
#
# No quantity moves: `blk` is the same vector, every row is the same PICKUP of
# the same kind and size, and the only thing that changes is which turn each
# one sits on and how many route turns are left behind them.
#
# OFF, `widepick` is `None`, `_routes` compiles none of the second-turn test,
# `early_u` keeps the 0/1 range `ROUTE_SPLIT_ON` always gave it and the whole
# plan hashes to the shipped tree (`tests/test_widepick.py`).
#
# SHIPPED 2026-09-18 by WIDEJUDGE [docs/strategy/2026-09-18-widepick.md §4],
# the first schedule-family arm to clear §115b since the family was declared
# closed by WIDESPAWN.  CRN-paired two-purse against the banked byte-exact ESR
# rows: **BAND250 +185 se 48 t +3.87** (ours +155 t +4.13, THEIRS **−30**),
# **ENGINE28 +1,018 se 701 t +1.45** (ours +837, theirs −180), **POOLED278
# +269 se 83 t +3.24** (ours +224, theirs **−45**).  Every leg positive, no leg
# at t <= −2, and the rival's purse never rises -- because the arm moves NO
# quantity: every market row of every board is byte-identical ON and OFF, so
# the `d0check` shop-re-roll rule has no subject here and the gain is priced
# almost entirely in our own purse.
#
# [SWITCH-GENE] Column 16 of `SWITCH_GENES` per the catalogue rule (USER
# 2026-09-17: the gene block carries EVERY shipped switch).  A zero gene
# decodes to this constant, so the shipped 6,789-parameter theta is still an
# exact prefix of the 7,659 layout and decodes bit for bit with the block ON.
WIDE_PICK_ON = True

# ---- WIDE_PICK_FREE: the wide day's turn-1 kind, chosen FREE-FIRST [SHIPPED]
#
# `WIDE_PICK_ON`'s second arm, named by WIDEJUDGE's "next steps" [§6.2,
# docs/strategy/2026-09-18-widepick.md]: the same grant, with the turn-1 KIND
# picked instead of taken.
#
# The shipped arm stamps its rows in `PICK_ITEM` order -- `pk_turn` is a plain
# cumsum over kinds -- so the kind that lands on turn 1 is the block's
# LOWEST-INDEXED owed kind, and the grant is refused whenever today's BUY row
# happens to deliver that one. On the three HOURTRACE tapes 45.7 unit-days a
# game own a block owing two or more kinds, **41.3** of them own at least one
# kind the row does not deliver, but only **30.7** own one as their FIRST
# kind: the row order, not the shed, refuses the other 10.6.
#
# This switch replaces the cumsum with a stable free-first ordering -- a 5x5
# priority comparison over the `N_PICK` kinds, key `(bought today, index)` --
# applied to the granted column alone, and widens `wide2`'s admission test from
# "the first owed kind is free" to "SOME owed kind is free", which is the same
# question once the ordering can answer it. Nothing else moves: the ordering is
# a permutation of the block's own rows, `blk` is the same vector, every market
# row is untouched and both pickups are still stationary, so the turn-2 HIRE
# row counts the same occupancy [LAW, `ops.ROUTE_BASE_WIDE`].
#
# OFF, `wpfree` is `None`, `_routes` compiles the shipped `first_free` test and
# `pk_turn` keeps the cumsum: bit for bit the pre-switch tree.
#
# SHIPPED 2026-09-18 [WIDESHIP2, USER], stacked on `WIDE_PICK_ON`.  Judged
# CRN-paired two-purse against the banked byte-exact ESR+WIDE_PICK rows
# [docs/strategy/2026-09-18-widepick2.md]: **BAND250 +102 se 40 t +2.54** (ours
# +139 t +4.08, theirs +37 t +1.92), **ENGINE28 +245 se 79 t +3.10** (ours
# +224 t +3.74, theirs −20), **POOLED278 +117 se 37 t +3.14** (ours +148
# t +4.73, theirs +31 t +1.74).  `d0check` PASS: every day-0 market row of both
# seats -- `hr_mop`, `hr_soldn`, `hr_spend`, `hr_money`, all 24 turns -- is
# byte-identical ON and OFF on all three boards, so no shop is re-rolled.  The
# WIDEPICK2 judge box wrote REJECT on its own pre-registered EACH-COIN bar
# (dTheirs <= 0, and the pooled gift is +31); the USER ships it anyway under the
# small-gains rule -- pooled margin +117 at t +3.14 >= 3 clears §115b, our own
# purse read (+148 t +4.73) is the strongest any schedule arm has posted, and
# the gift is negative on the ENGINE class we are climbing towards.
#
# [SWITCH-GENE] Column 17 of `SWITCH_GENES` per the catalogue rule (USER
# 2026-09-17: the gene block carries EVERY shipped switch). A zero gene decodes
# to this constant, so the shipped 6,789-parameter theta is still an exact
# prefix of the 7,692 layout and decodes bit for bit with the block ON -- there
# is no manual switch string.
WIDE_PICK_FREE_ON = True

# ---- EVE_STOCK: tonight's purchase + tomorrow's per-kind start [SWITCH, OFF]
#
# The composition of the two arms above, and it is neither of them. Measured
# cause of our dawn wait (`S/evestock/report.py`, ENG22, 22 real-engine boards,
# d20-29): of 111 lead-PASS unit-turns a game -- the PASS steps before a unit's
# FIRST act, which is ROUTEEFF's `dawn_pass` 0.95/unit-day to the coin --
# **51.6 % is a block owing a PICKUP of an item last night's shed ALREADY
# HOLDS** (`ROUTE_FREEFIRST`'s class), **33.8 % a PICKUP of an item the day's
# own turn-1 BUY row delivers** (this switch's class) and 0.1 % the seed. The
# engine class starts 28 % of its unit-days at turn 1 to our 13 % and holds
# 4.87 seeds at dawn to our 0.66: it buys tomorrow's inputs before tomorrow.
#
# So: `_prestock`'s row at `O.TURN_PRESTOCK` = 20 (products only --
# `PRESTOCK_SEEDS` is measured at -90,863 and stays off) buys tomorrow's feed
# wheat and fertilizer tonight, which lowers tomorrow's own `wheat_buy` /
# `fert_bought` to zero; `ROUTE_FREEFIRST`'s per-KIND block test then reads
# that zero and bases those blocks at `O.TURN_BUY` instead of `O.ROUTE_BASE`.
# Neither half reaches the other's class alone, which is exactly why both
# prior arms missed:
#
#   * `PRESTOCK_V2_ON` (-326, t -1.92) asked the DAY-GLOBAL question
#     (`_buy_row_units(d) == 0`) and its schedule half was byte-identical to
#     OFF on all 80 boards -- seeds and animals ride that row too, so it is
#     never empty. This switch never asks the day question; it asks the block
#     one, per kind.
#   * `ROUTE_FREEFIRST_ON` (+23, t 0.18) asked the block question but bought
#     nothing, so it could only free the blocks the day happened not to buy
#     for -- the 51.6 % class, and only the part of it `route_split` had not
#     already taken.
#
# `hire_wide_early` is untouched (`None` throughout), so neither PRESTOCK
# assert has a subject and turn 1 keeps exactly the writers it has today
# (`OPEN_PUMP`'s sell-back, `EARLY_SELL`'s lot 1, the residual BUY row).
# `route_base` is untouched: the crew's floor is still `O.ROUTE_BASE`/
# `ROUTE_BASE_WIDE` and only a block `_routes` itself cuts early moves, so the
# BANK/LOT ordering and `SELL_SLOT_PRIORITY`'s rows are bit-identical.
#
# OFF, `pre_wheat` is `None` and `freefirst` is `None` -- no order at
# `TURN_PRESTOCK`, `_routes` compiles none of the per-kind test, and the whole
# plan hashes to the shipped tree (`tests/test_evestock.py`).
EVE_STOCK_ON = True  # SHIP_VRP25_HYB (STACK1 hA)

# ---- CREW24: fill the dawn and dusk turns [SWITCHES, OFF] -----------------
# DSMFULL1: rank-1 DSM idles 4 hand-turns d10-29, we idle 440 (197 at h0-2,
# 201 at h21-23). Three independent switches, each OFF byte-identical.
#
# `EVENING_SEED_ON`: the `_prestock` row at `O.TURN_PRESTOCK` carries SEEDS
# ONLY (no feed wheat / fertilizer: EVE_STOCK's product half is shed-bound and
# measured -33). Forecast = the seeds today's route actually planted, per crop,
# net of what tonight still holds, capped at `EVENING_SEED_MAX` a night, only
# on days `EVENING_SEED_DAYS` (the PRESTOCK_SEEDS -90,863 failure was the
# d0 purse), and only out of `purse_left - EVENING_SEED_FLOOR` (purse_left is
# already net of the hire bill and `cash_reserve`). Seed prices are fixed, so
# the evening buy moves no book. Tomorrow's `_derive` nets `view.seeds`.
EVENING_SEED_ON = False
EVENING_SEED_DAYS = (10, 26)
EVENING_SEED_MAX = 12
EVENING_SEED_FLOOR = 1500
# `H1_WORK_ON`: a narrow-day block may start at `O.TURN_BUY` (hour 1) when
# everything it opens with is already on hand: (a) the per-kind pickup test of
# ROUTE_FREEFIRST (every kind it collects has a zero purchase today, so last
# night's shed feeds it) and (b) a PLANT opener when today's BUY row buys no
# seed at all (the seed was bought last night -- `EVENING_SEED_ON`).
H1_WORK_ON = False
# `H23_WATER_ON`: the admit stage charges each unit's day as if routes ended
# early (EST_LEAD 5 + pickups), so on d10-29 it DECLINES ranked water/harvest
# tasks on days whose crew then PASSes through h21-23. ON, from day
# `H23_WATER_DAY0`, each unit gets `H23_WATER_TURNS` turns of admit credit
# back so the declined tasks ride the tail; `ADMIT_ROUNDS` drops whatever the
# exact route still cannot reach (over-admission is the repairable error).
H23_WATER_ON = False
H23_WATER_TURNS = 2
H23_WATER_DAY0 = 10

# `MARKET_PACK_ON` [SWITCH]: the same day-start wait again, and this time the
# schedule moves rather than the route. `ROUTE_SPLIT_ON` takes the turn for the
# blocks the turn-1 BUY row does not hold up; what it cannot reach is the block
# that *does* owe a PICKUP on a narrow day, because that block waits on a row
# which has not resolved yet -- 240 of the census's 375 idle unit-turns a game.
#
# The row does not have to be at turn 1. `_process_market` truncates each
# seat's queue to `maxMarketOrdersPerTurn` = 10 *per turn*
# (`kaggle_environments/envs/kaggriculture/kaggriculture.py:551,557`) and that
# cap is the whole reason the day has two market rows in the morning: ten hire
# slots plus ten purchase slots do not fit one turn. But a day rarely presents
# twenty orders. `n_hire` hires and the purchases the budget actually sized --
# an order per positive quantity, `_buy_row_orders` -- often total ten or
# fewer, and then both rows fit turn 0 and turn 1 has nothing left to resolve.
#
# What that buys is `ops.ROUTE_BASE_PACK`: the whole crew starts at turn 1, the
# pickup-owing blocks included, since the goods reached the shed in turn 0's
# market phase. It is the turn `PRESTOCK` went looking for at turn 20 and did
# not find, taken without moving a coin out of the morning.
#
# Nothing about the purse changes, and that is checkable rather than hoped:
# `SELL_TURNS` starts at 3, so no revenue lands between turn 0 and turn 1
# either way, and no unit acts in between (turn 1's unit phase is all PASS off
# the switch), so money and shed contents at the moment the row resolves are
# the same in both layouts. The hires still resolve first -- the engine handles
# the atomic orders of slot round i in player order and HIRE is one of them, so
# slots 0..n_hire-1 are hired before the purchases in the slots behind them,
# exactly the order the two rows had. Prices can only improve: `ticks_before`
# gives turn 0 zero shop ticks and zero centre ticks against turn 1's one and
# one, price is monotone non-increasing in inventory, and the budget still
# quotes at `O.TURN_BUY` -- so the day pays at most what it budgeted and the
# reserve cannot be breached by the move.
#
# BUY_LAND does not move and cannot: it rides the spare tenth slot of
# `SELL_TURNS[0]` [M2] because the morning's own sale is the only thing that
# can fund it, and it is not part of the BUY row this switch packs. A land day
# is therefore packed like any other -- its ten sell-turn slots are untouched
# -- and `land_lead` still keeps every unit off the new quadrant until
# `SELL_TURNS[0] + 1`, one turn later relative to a base that has moved up.
#
# Two things stay behind on a packed day, both because turn 0's hire row
# resolves after turn 0's unit phase:
#   * nobody acts at turn 0. `route_split`'s own gate is what enforces it --
#     it requires `route_base` to be the one the law fixes, and a packed day's
#     is not -- so the switch supersedes `ROUTE_SPLIT_ON` on the days it fires
#     and there is no turn left for it to take.
#   * a wide crew is never packed: eleven hires do not fit ten slots, so
#     `n_hire + orders <= MO` implies the narrow layout and the turn-2 row is
#     empty.
#
# The admit stage needs no credit of its own, unlike the two switches before
# it: the turn is in `turn_budget` (`TPD - route_base` = 23), and a packed day
# gives up `route_split`'s optimistic `+ n_units` at the same time, so `labour`
# comes out exactly where it was and only the *realised* routes are longer.
# The hire enumeration does take a credit, off pass A's row like `PRESTOCK`'s:
# a candidate crew that still fits ten slots beside the purchases is worth a
# turn a unit more, and one that does not is not -- which is a real part of the
# decision, the seventh hand on a four-order day costing the six before it a
# turn each exactly as the eleventh costs ten.
#
# `PRESTOCK_ON` is the one switch it cannot share a day with: that one moves
# the overflow hire row *into* turn 1, which is the turn this one empties.
# Asserted at import rather than left to the reader.
#
# MEASURED 2026-09-03 and **rejected**. 48 seeds x 4 opponents x 2 seats = 384
# paired games, `flow58_g450`, seed base 777001, each game paired against the
# same board with the switch off (`scratchpad/stack/stack3_777001.abs.csv`,
# reproduced exactly from this tree before the read, all 32 spot-check rows
# identical):
#
#     ALL         -1,366 coins a game   t -2.05   win 57.6% -> 56.5%   68 disc
#       kagg2            -1,717 (t -1.22)   win 88.5% -> 90.6%
#       tape 103254816   +1,025 (t  0.82)   win 57.3% -> 64.6%
#       tape 104502967   -1,015 (t -0.84)   win 52.1% -> 45.8%
#       tape 104547425   -3,757 (t -2.63)   win 32.3% -> 25.0%
#
# The mechanism is not in doubt: over 8 replayed games the switch packs 7.9 of
# the 30 days and the crew's hour-0..2 PASS unit-turns fall 297.4 -> 260.5 a
# game (-12%). What it does not do is pay. **Our own coins fall 1,110 a game**
# (102,081 -> 100,971) while the opponents' barely move (+256) -- so this is
# not `PRESTOCK`'s "we both got richer", it is the extra turn being worth less
# than what the day gives up for it. Nor is it the crew: the hire credit above
# moves the season's hire orders by 2 (270.5 -> 268.4) and the end-of-season
# roster by 0.2 hands, so the argmax is buying the same crew and losing coins
# with it.
#
# Which leaves the two things the packing changes and `ROUTE_SPLIT_ON` does
# not, and a promotion attempt has to answer one of them first: the purchases
# now resolve in the *same slot rounds* as our hires and therefore against
# different orders of the other seat's row than before, and they resolve one
# town tick earlier, at the un-drained hour-0 inventory -- a buy that is
# cheaper for us is also supply taken out from under our own later sale.
# 104547425, the leg that loses most, is the tape that trades hardest into our
# morning.
#
# OFF, `pack` is `None`, `_market` emits the two rows on the two turns it
# always did, `route_base` is the expression it always was and the enumeration
# scores `route_turns(h)`, so the champion theta decodes byte for byte
# (`tests/test_market_pack.py`).
MARKET_PACK_ON = False

assert not (MARKET_PACK_ON and PRESTOCK_ON), \
    "PRESTOCK fills the turn MARKET_PACK empties: one row cannot be in two places"

# `EARLY_SELL_ON` [SWITCH]: sell earlier in the day, and nothing else.
#
# The 2026-09-03 strategy study (docs/strategy, 3.1-3.2) makes the market pot
# shared and price-forming, and reads three facts out of the engine:
# `_process_market` truncates each *seat's* queue to ten orders a turn (HIRE
# and BUY_LAND are queue entries and count against that ten); within one turn
# both seats' SELL/BUY orders are quoted off one pre-commit inventory and
# committed in per-unit lockstep, so two seats selling on the same turn split
# the curve evenly and the only way to be *first* is to sell on an EARLIER
# turn; and everything a unit harvested yesterday is in the shed at hour 0
# (`_end_of_day` -> `_drop_inventories_to_shed`). Its day-level model puts the
# whole-season margin swing between "we sell first every day" and "we sell
# last" at 41,426 coins, half of it taken off the other seat -- the curve is
# conserved, so every coin we gain going first is a coin they do not get.
#
# The shipped schedule sells on turns 3, 10 and 18 (recorded hours 4, 11, 19).
# Every 2800-tier tape's flow lands at hours 10-16 and kagg2's at 17, so only
# lot 1 is in front of them today; lots 2 and 3 meet a curve the opponent has
# already walked, or walk it for them.
#
# What moves is **when**, never what or how much: `core.sell`'s three lots are
# the same arrays in the same order with the same quantities, emitted on
# earlier turns.
#
#   "A"  lot 1 leaves turn 3 for `O.EARLY_SELL_LOT1_TURN` (turn 1), riding
#        behind the day's BUY row in the same turn -- but only on a day the
#        purchases and the lot together fit the engine's ten slots, else the
#        lot stays where it was. Lots 2 and 3 do not move.
#   "A1" A, with the lot in FRONT of the purchases in that row instead of
#        behind them. Both orders are legal and the difference is not
#        cosmetic: the engine walks a turn's queue in slot order against one
#        running market inventory, so behind-the-buys our SELL quotes against
#        an inventory our own BUY_PRODUCT has just drawn down (a higher price
#        for us, a dearer buy), and in front of them the sale floods the
#        shelf first (a cheaper buy, a thinner sale). Mode A's only losing
#        leg was kagg2, the one opponent that buys the same wheat we sell.
#   "A0" lot 1 rides turn 0, packed behind that turn's hires, on a day the
#        two together fit the ten slots -- `n_hire + n_sell <= MO`. Most days
#        hire nobody, so most days the lot goes out at recorded hour 1,
#        in front of every recorded opponent's first order (hours 1-4). A day
#        that hires too many falls back to A's merged BUY row, and a day that
#        cannot hold it there either keeps the shipped `SELL_TURNS[0]`.
#        Nothing merges with a BUY_PRODUCT here, so the buy/sell interaction
#        A and A1 differ over does not arise at all.
#   "A21" A's lot 1, plus lot 2 at `O.EARLY_SELL_LATE_TURNS[0]` (turn 4) and
#        lot 3 left on `O.SELL_TURNS[-1]` (turn 18). The middle ground B
#        overshot: two thirds of the day's flow in front of the opponent,
#        one lot still held back to meet a shop-restocked curve.
#   "Z"  The lot takes turn 0 OUTRIGHT and the morning moves out of its way:
#        HIRE to turn 1, the overflow hire row to turn 2, and the BUY row to
#        the first turn behind the hires with room for it -- turn 1 when
#        `n_hire + n_buy <= 10`, else turn 2 (`O.EARLY_SELL_Z_*`). A0 asked
#        the same question and was refused by the board: it only compacted the
#        lot behind turn 0's hires when the two fit the ten, and the champion
#        re-hires a full crew every day, so the row was already full and the
#        lot fell back to A's on 8 days in 11. Z does not ask -- the lot is
#        first and the hires wait -- so it lands at recorded hour 2, in
#        lockstep with the field's own hour-0 dump (kagg2 sells yesterday's
#        shed at hour 0 on 208 of 224 seat-days) rather than an hour behind it.
#        What it costs is the hire law: a hand hired in turn t first acts in
#        t + 1 [LAW], so the crew's floor is `O.ROUTE_BASE_Z` = 2 instead of
#        the turn-1 start `ROUTE_SPLIT_ON` wins a pickup-free block under A,
#        and a day whose purchases do not fit turn 1 waits for turn 2
#        (`O.ROUTE_BASE_Z_LATE` = 3) before it may PICKUP. A WIDE day (more
#        than ten hires) is not a Z day at all: its overflow row needs turn 2
#        and the purchases would have nowhere to go, so it keeps mode A's
#        layout exactly.
#   "Z1" Z on a day whose hour-0 shed holds `O.EARLY_SELL_Z_MIN_SHED` units or
#        more, and mode A on every other day: turn 0 costs a fixed price
#        (`projector.ticks_before`, below), so a day with little to sell pays
#        it for little, and only a heavy day can be worth it.
#   "B"  A, and lots 2 and 3 move to `O.EARLY_SELL_LATE_TURNS` (turns 4 and 5).
#        The whole day's flow is then out by hour 6, in front of every recorded
#        opponent's. This is the study's "sell as it lands" written the way the
#        engine actually permits: the stock is already in the shed at hour 0,
#        so "as it lands" is "as early as a row can carry it", and a row
#        repeated down the day would have no memory of what the earlier rows
#        already sold and would eat the reserve (feed wheat) the plan holds
#        back.
#
# Simulator cost is nil either way, which is why there is no throughput
# argument against it: mode A resolves the same six market turns the shipped
# schedule does (0,1,2,3,10,18) and mode B resolves six as well (0,1,2,3,4,5),
# so the ~6% of episode throughput an extra SELL turn costs is never charged.
#
# OFF, `early_sell` is `None`, `_market` emits the three lots on
# `O.SELL_TURNS` exactly as it always did and the BUY row is untouched, so the
# champion theta decodes byte for byte (`tests/test_early_sell.py`).
#
# WHY TURN 0 IS NOT FREE, and mode Z lost on it [MEASURED 2026-09-03]: a turn
# runs its unit ops, then its market, then the town tick, so `ticks_before`
# gives turn 0 (0 shop ticks, 0 centre ticks) and turn 1 (1, 1). Between the
# two market phases the town centre takes its once-a-day bite and the first
# shop tick fires, and both DRAIN the shelf -- and a thinner shelf is a dearer
# quote. So the hour-1 row that mode Z buys is quoted off a market one full
# day-tick FULLER than mode A's hour-2 row: the lockstep with the field's own
# first row is bought at a per-unit discount that scales with the lot.
#
# VERDICTS on the zero-row modes [MEASURED 2026-09-03, flow58_g450, real
# engine, 8 seeds x 2 seats x (kagg2 + three class-A tapes), paired on
# (seed, opponent, seat) against mode A at the same seed base 777001,
# n = 64 (scratchpad/hour0c)]:
#
#   Z   ALL  -4,658 a game, t -2.76, win 62.5% -> 56.2%, and NOT ONE of the
#       four legs above A: kagg2 -3,844, 103254816 -4,857, 104502967 -6,093,
#       104547425 -3,839. The ladder's discovery gate (every leg >= 0) is
#       missed on all four, so no n=384 and no 777002 confirmation was run.
#       And it is OUR coins that go: ours -5,553 a game against theirs -894.
#   Z1  turn 0 only on a day whose hour-0 shed holds `O.EARLY_SELL_Z_MIN_SHED`
#       units or more: ALL -773 a game, t -0.64, win 62.5% -> 64.1%, two legs
#       of four still under A (kagg2 -1,850; 104502967 -3,936, t -3.58). It is
#       Z scaled down by how often it fires, which is what a PER-DAY cost
#       looks like -- and it does not clear the gate either.
#
# NEITHER IS PROMOTED. Mode "A" stays the default.
#
# WHAT IT WAS NOT. The hire delay was priced as the cost and it is not the
# cost: over 56 selling seat-days of one replayed game the crew WORKED MORE
# under Z, 198.0 unit-turns a day against A's 196.4, because the enumeration
# re-prices the crew against the schedule it will get and takes the turn back
# elsewhere. Nor is it the lockstep: Z does reach hour 1 on every narrow day
# (first-lot hour 2.00 -> 1.46 over the pooled seat-days, the rest being the
# wide days Z hands back to A) and our share of the shared hour goes 87.0% ->
# 88.0%. The row lands where the mode says it lands.
#
# ON by default since 2026-09-03, mode "A": real engine, flow58_g450, paired
# against the same theta with the switch off, 48 seeds x 2 seats x (kagg2 +
# three class-A tapes) over two seed bases, n=768 -- +2,184/game (t 5.13), win
# 61.5 -> 70.3 %, and the 20-tape panel +1,405 (t 4.9). The kagg2 leg is the
# only negative one (-359, not significant): it is the one opponent that buys
# the wheat we sell, which is what mode "A1" was cut to test and lost on.
EARLY_SELL_ON = True

#: Which of the variants above. Read only when `EARLY_SELL_ON`.
EARLY_SELL_MODE = "A"

#: Modes whose lot 1 tries turn 0's hire row before the BUY row.
EARLY_SELL_MODES_HIRE_ROW = ("A0",)
#: Modes that put lot 1 in front of the purchases in the row they share.
EARLY_SELL_MODES_LOT_FIRST = ("A1",)
#: Modes that give lot 1 turn 0 outright and move the morning's rows behind it.
EARLY_SELL_MODES_ZERO_ROW = ("Z", "Z1")
#: Zero-row modes that take turn 0 only on a day with a lot worth the loss.
EARLY_SELL_MODES_HEAVY_ONLY = ("Z1",)

assert EARLY_SELL_MODE in ("A", "A1", "A0", "A21", "B", "Z", "Z1"), EARLY_SELL_MODE
assert not (EARLY_SELL_ON and (MARKET_PACK_ON or PRESTOCK_ON)), \
    "EARLY_SELL rides the BUY row; PRESTOCK and MARKET_PACK both move it"
assert not (EARLY_SELL_ON and EARLY_SELL_MODE in EARLY_SELL_MODES_ZERO_ROW
            and ROUTE_EARLY_ON), \
    "mode Z's crew floor is the hire law's own turn; ROUTE_EARLY has nothing to give"
assert not (BANK_BEFORE_LOT_ON and (MELON_OPEN_ON or MIDDAY_PLACE_V2_ON)), \
    "one excursion clock per block: BANK_BEFORE_LOT and the melon excursion both own `ins`"
assert not (MIDDAY_PLACE_ON and not (MELON_OPEN_ON or MIDDAY_PLACE_V2_ON)), \
    "MIDDAY_PLACE rewrites the melon excursion's rank and op; without one there is none"
assert 0 <= MIDDAY_PLACE_LOT < len(O.MELON_LOT_TURNS), \
    "the deposit has to beat a row the dump day actually presents"
assert not (MIDDAY_PLACE_V2_ON and not MIDDAY_PLACE_ON), \
    "MIDDAY_PLACE_V2 shortens the chain the MIDDAY_PLACE deposit fires after"
assert O.MELON_LOT_TURNS[0] <= MIDDAY_PLACE_V2_TURN <= O.SELL_TURNS[-1], \
    "the V2 deposit has to beat a row the dump day actually presents"


def _midday_place_turn() -> int:
    """The turn a mid-day melon deposit has to land on or before [SWITCH].

    `MIDDAY_PLACE_LOT`'s row off the shipped switch, `MIDDAY_PLACE_V2_TURN`
    under V2. One reader, called at trace time, so a runner that flips either
    after import is seen by the planner.

    [SAME_DAY_FERT] Under that switch it is the day's last SELL lot as
    `early_lot_turns` currently stands, which is the very row the banked
    fertilizer is added to below -- deadline and row read off one expression,
    so `EARLY_SELL`'s modes cannot move one without the other.
    """
    if SAME_DAY_FERT_ON:                                         # [SWITCH]
        return int(early_lot_turns()[-1])
    if MIDDAY_PLACE_V2_ON:
        return int(MIDDAY_PLACE_V2_TURN)
    return int(melon_lot_turns()[MIDDAY_PLACE_LOT])


def early_sell_zero_row() -> bool:
    """True on a build whose lot 1 owns turn 0 [SWITCH, EARLY_SELL mode "Z"].

    One reader, called at trace time by `_plan_day` and `_market`, so a runner
    that flips `EARLY_SELL_MODE` after import is seen by both.
    """
    return EARLY_SELL_ON and EARLY_SELL_MODE in EARLY_SELL_MODES_ZERO_ROW


def early_lot_turns():
    """The turns the three lots stand on, under the switch as it is set now.

    One reader for `_market` and for `sim/rollout`, which has to know the same
    set at import to compile its sell-only market path. `O.SELL_TURNS[0]` is in
    every variant: it carries the day's BUY_LAND, and it is lot 1's fallback on
    a day no earlier row could hold it.
    """
    # [LOT4] The fourth row, merged in TURN ORDER and not appended: the
    # allocator's lot index IS the timing-pressure rank (`press * lot_ix`) and
    # its externality term telescopes over later lots, so a tuple out of time
    # order would price every lot against the wrong shelf -- and `n_lots() - 1`,
    # which every "day's LAST lot" bulk add uses, would name a row that is not
    # last. Sorting is a no-op off the switch and under every `EARLY_SELL` mode
    # (all of their layouts are already increasing), so OFF returns the tuple it
    # returned, object for object.
    def _out(base):
        return tuple(sorted(base + (LOT4_TURN,))) if LOT4_ON else tuple(base)
    if not EARLY_SELL_ON:
        return _out(tuple(O.SELL_TURNS))
    if EARLY_SELL_MODE == "B":
        return _out((O.SELL_TURNS[0],) + tuple(O.EARLY_SELL_LATE_TURNS))
    if EARLY_SELL_MODE == "A21":
        return _out((O.SELL_TURNS[0], O.EARLY_SELL_LATE_TURNS[0],
                     O.SELL_TURNS[-1]))
    return _out(tuple(O.SELL_TURNS))


def n_lots() -> int:
    """How many lots the day presents, under the switches as they are set now.

    `sell.N_LOTS` is `len(O.SELL_TURNS)` frozen at import; this is the same
    number read at trace time, so a runner that flips `LOT4_ON` after import is
    seen by every row mask in `_plan_day`. Equal to `SELL.N_LOTS` off the
    switch, which is why OFF traces the identical program.
    """
    return len(early_lot_turns())


# ---- SPREAD_ROWS: the day's voluntary sale in per-tick bursts [SWITCH, OFF]
#
# `docs/strategy/2026-09-16-pricevol.md` sect.4.3-4.5 and sect.7 measured the
# largest single reachable line in the whole live census. The engine prices a
# SELL order UNIT BY UNIT and adds +1 to the shared market inventory after every
# unit (`sim/market.py` `_quotes`, `off = +j`), so the n-th unit of a burst is
# quoted off an inventory n-1 higher than the first. B sells **9.73 units a
# burst** and forfeits **7,936 coins a game** between the first unit's quote and
# what it actually takes; the current top five sell **3.73** a burst and forfeit
# **2,554**. At B's own production, on B's own boards, closing that difference
# is worth **+5,382 coins/game** -- an UPPER BOUND, not a promise, because a
# burst spread over later rows sells into an inventory the other seat and the
# shops have moved in the meantime.
#
# THE BID IT HAS TO FIT INTO (pricevol sect.4.4, measured out of the 117
# replays' own unlocked shop lists): the town eats **4.3 wheat / 3.5 strawberry
# / 2.5 milk / 1.8 wool** units PER SHOP TICK in d15-29, and B pushes **18.2 /
# 15.0 / 9.6 / 7.6** of them through ONE tick. Melon (1.0 units a DAY) and
# fertilizer (0.0) have no town bid at all.
#
# THE ROWS ARE FREE IN OPS. `action` has three independent channels
# (`farmer` / `hands` / `market`) and the engine takes ten market orders a turn
# on every turn, so a row out of the shed costs no unit-op and no labour -- the
# overnight lot is already in the shed at hour 0 (`_end_of_day` ->
# `_drop_inventories_to_shed`). What an extra resolved market turn costs is
# ~6 % of SIMULATOR throughput (`ops.SELL_TURNS`' own measured comment), which
# is a training-run bill and not a game one.
#
# WHAT THIS IS NOT. It is **not** a re-schedule of whole lots. That family --
# `docs/strategy/2026-09-10-consensus.md` sect.85-90 (SELL5, SELL21, whole-lot
# re-schedules) and every `EARLY_SELL` mode -- moves the SAME burst to a
# different hour, and closed as a displacement trade: what we take off the
# shared curve early we hand back late, and `LOT4` (2026-09-16) priced the
# newest version of it at band margin **-831 (t -4.87)** because the
# action-replay seat banked +1,139 of the same shelf. Here the day's VOLUME, its
# product mix, its reservation gate and its total `s_qty` are identical to the
# unit; only the NUMBER OF ROWS the same day's volume is cut into changes, and
# the burst size is capped at what the town can actually absorb between two
# rows. LOT4 added a row and moved a quarter of the day three turns LATER;
# this adds five and moves the day's volume-weighted hour only as far as the
# cap forces it to.
#
# WHAT ON CHANGES, exhaustively.  `_plan_and_stats` hands `_market` the
# VOLUNTARY allocation (`vol_lots`, the array `s_qty` is summed from, before a
# single bulk add) cut over `spread_rows_turns()` by `spread_alloc`, and the
# lots array it hands over carries `lots - vol_lots` -- every unit that is NOT
# the gated sale (the forced-overflow continuation, `DROP`, `MELON_OPEN`,
# `SAME_DAY_FERT`, `BANK_BEFORE_LOT`, `ANIMAL_SAME_DAY`), still on the lot it
# chose, on the turn it always stood on. Every one of those sites ADDS to
# `lots`, so the difference is non-negative by construction and the day's total
# is conserved to the unit. `sim/rollout` picks the extra turns up at import,
# as it already does for `MELON_OPEN_ON` and `EARLY_SELL_ON`.
#
# TURN 1 AND TURN 3 KEEP THEIR JOBS. `O.EARLY_SELL_LOT1_TURN` (1) is in the
# default row set, and the row that stands there is merged into lot 1's own
# slot of the `EARLY_SELL` machinery -- behind the day's BUY row, on a day the
# two fit the engine's ten, and falling back to `O.SELL_TURNS[0]` (3) when they
# do not, exactly as the shipped lot 1 does. Turn 3 therefore keeps the
# fallback AND the day's BUY_LAND in its tenth slot.
#
# MEASURED, AND REJECTED [docs/strategy/2026-09-16-spread6.md, 2026-09-16].
# The burst size is delivered and over-delivered -- 9.83 -> 2.83 units a burst on
# the 68 band boards, forfeit 8,409 -> 1,811 (-6,598, t -39.05), past the top
# five's own 3.73 and 2,554 -- and it is NOT MONEY. On frozen volume (-1 unit,
# t -0.56, with `SPREAD_ROWS_SKIP_LAND_DAYS` below) our purse reads
# **-2,465 (t -13.68)** and the paired margin **-1,802 (t -7.05)**; without that
# knob the three variants read -4,605..-6,429 of coins and -12,896..-14,401 of
# margin, because the same cut also starves the day's BUY_LAND. The reason is an
# identity, not a tuning: `gross taken = sum(n * first-unit quote) - forfeit`,
# and cutting the burst moved the first term -8,865 to move the second +6,598.
# The engine prices a unit off the CUMULATIVE inventory, so splitting an order
# only re-labels which unit is called "first"; what a split genuinely buys is
# the town drain between two rows, which `LOT-DEPTH` sect.2 priced at +46..+163
# coins on a 65-unit liquidation. Kept default-off as the measurement it is.
#
# OFF, `spread` is `None`, `_market` emits the three lots on the turns it
# always emitted them and no other row exists, so the champion theta decodes
# byte for byte (`tests/test_spread6.py` pins the whole plan against a pristine
# `git archive HEAD src` tree).
SPREAD_ROWS_ON = False

#: The rows the day's voluntary sale is cut over [SWITCH, SPREAD_ROWS]. The
#: default is the FIRST MARKET PHASE AFTER EACH SHOP TICK: a turn runs its unit
#: ops, then its market, then the town tick, and `spec.SHOP_SELL_INTERVAL` is 4,
#: so a tick fires at the end of turns 0, 4, 8, 12, 16 and 20 and each of turns
#: 1, 5, 9, 13, 17, 21 is quoted off a shelf exactly one tick thinner than the
#: row before it (`projector.ticks_before` gives them 1, 2, 3, 4, 5, 6 shop
#: ticks). `(1, 5, 9, 13)` is the "early" variant: every row in front of the
#: hour-17 dump the band clones play, which is the direction `LOT4` sect.2b
#: found the sign flip on.
#:
#: Accepts a tuple or a dash-joined string ("1-5-9-13") so a runner can sweep
#: it on a comma-separated `--switches` line.
SPREAD_ROWS_TURNS = (1, 5, 9, 13, 17, 21)

#: How wide one row may be, per product [SWITCH, SPREAD_ROWS]:
#:
#:   "tick"   the projector's own per-tick town appetite for that product on
#:            THIS board (`projector.town_tick_units(shops)`, which is the
#:            pricevol sect.4.4 column), floored at 1 so a product with no town
#:            bid at all (melon, fertilizer) still spreads rather than standing
#:            on one row.
#:   "equal"  ceil(volume / n_rows) -- the same day cut into equal rows. The
#:            control: it has no tail by construction.
#:
#: Rows are filled in turn order at `min(cap, what is left)`, and whatever the
#: caps could not place by the LAST row of the day is placed on that last row
#: anyway. Nothing is ever left in the shed: `LOT-DEPTH` measured a tight cap
#: destroying units at the shed door, and `SHED-CLIP` has B's shed sitting at
#: 99 % of its 100-unit cap with 21.6 units a game already clipped.
SPREAD_ROWS_CAP_MODE = "tick"

SPREAD_ROWS_CAP_MODES = ("tick", "equal")

#: Keep the shipped three-lot layout on a day that BUYS LAND [SWITCH,
#: SPREAD_ROWS]. Measured, not guessed: the day's BUY_LAND rides the spare
#: tenth slot of `O.SELL_TURNS[0]` and is *funded by lot 1's own proceeds* --
#: `ops.py:TURN_PRESTOCK`'s comment says it outright ("land is funded by the
#: morning's own lot") -- so a turn-1 row cut down to the town's per-tick
#: appetite leaves the purse short at turn 3 and the engine drops the order in
#: silence. On the 10 TOP5NOW boards that costs the SECOND QUADRANT on day 5:
#: `nquad` 1 -> 2 at d6 OFF, still 1 ON, and our dawn purse at d6 is +1,012
#: (the land bill, unspent). That is a funding accident, not the burst
#: mechanism, so it gets its own knob and its own leg. Default False: the three
#: variants of `docs/strategy/2026-09-16-spread6.md` sect.3 are read with the
#: accident IN, and sect.5 reads it out.
SPREAD_ROWS_SKIP_LAND_DAYS = False


def spread_rows_turns():
    """The turns the day's voluntary sale is cut over, under the switch as it
    is set now.

    One reader for `_market`, for `sim/rollout` (which needs the same set at
    import to resolve those market phases) and for `_spread_check`, so a runner
    that flips the switch after import is seen by all three.
    """
    t = SPREAD_ROWS_TURNS
    if isinstance(t, str):
        t = [x for x in t.replace(",", "-").split("-") if x]
    return tuple(int(x) for x in t)


def spread_merge_row():
    """The index of the row that rides the BUY row, or -1.

    `EARLY_SELL` mode A already merges lot 1 into `O.EARLY_SELL_LOT1_TURN` on a
    day the purchases and the lot together fit the engine's ten slots, and that
    turn is the first post-tick row of the day. When it is in the spread, the
    row that stands there takes lot 1's seat in that machinery instead of being
    emitted on its own -- turn 1 is the BUY row and a second write to it would
    overwrite the day's purchases in silence.
    """
    turns = spread_rows_turns()
    if not (EARLY_SELL_ON and O.EARLY_SELL_LOT1_TURN in turns):
        return -1
    return turns.index(O.EARLY_SELL_LOT1_TURN)


def _spread_check():
    """Every row the day already owns is refused at trace time, not silently
    overwritten. Python-time, like every assert in this file; read through the
    switches as the runner set them, because all of them are set after import.
    """
    turns = spread_rows_turns()
    assert SPREAD_ROWS_CAP_MODE in SPREAD_ROWS_CAP_MODES, SPREAD_ROWS_CAP_MODE
    assert turns and list(turns) == sorted(set(turns)), \
        "the spread rows are distinct and in turn order: a row is quoted off "\
        "the shelf the row before it left"
    assert 0 <= turns[0] and turns[-1] < spec.TURNS_PER_DAY, \
        "every spread row resolves inside the day, before `end_of_day` empties "\
        "the hands into the shed"
    taken = (set(early_lot_turns()) | set(O.HIRE_TURNS)
             | (set(melon_lot_turns()) if MELON_OPEN_ON else set())
             | ({O.TURN_PRESTOCK} if (PRESTOCK_ON or EVE_STOCK_ON or EVENING_SEED_ON
                                     or (CREW_RELAY_ON and CREW_RELAY_EVE)
                                     or (PRESTOCK_V2_ON and PRESTOCK_V2_BUY_ON))
                else set()))
    merge = spread_merge_row()
    for k, t in enumerate(turns):
        if k == merge:
            continue
        assert t not in taken, \
            f"spread row {t} collides with a row the day already uses {sorted(taken)}"
        assert t != O.EARLY_SELL_LOT1_TURN or not EARLY_SELL_ON, \
            "turn 1 is the BUY row; only the merged row may stand on it"
        assert t >= O.FULL_MARKET_TURNS, \
            "a row below FULL_MARKET_TURNS is a full-row turn and is spoken for"


def spread_alloc(xp, s_qty, shops):
    """int[n_rows, 9]: the day's voluntary volume `s_qty`, cut over
    `spread_rows_turns()` at `SPREAD_ROWS_CAP_MODE`'s per-row cap.

    Conserves `s_qty` exactly, per product: rows are filled in turn order at
    `min(cap, left)` and the last row takes whatever is left, cap or no cap. No
    unit is ever dropped and none is ever left in the shed -- `LOT-DEPTH`
    measured a tight cap destroying units at the shed door, and the shed the
    residue would wait in is already at 99 % of its cap (`SHED-CLIP`).
    """
    i32 = xp.int32
    n = len(spread_rows_turns())
    vol = s_qty.astype(i32)
    if SPREAD_ROWS_CAP_MODE == "equal":
        # A true equal split, not a ceil-fill: `volume // n` on every row and
        # the remainder one unit at a time down the first rows, so no row is
        # more than one unit wider than another and there is no tail at all.
        # This is the control the "tick" arm is read against.
        base = (vol // n).astype(i32)
        rem = (vol - base * n).astype(i32)
        return xp.stack([(base + (rem > k).astype(i32)).astype(i32)
                         for k in range(n)]).astype(i32)
    # "tick": the town's own per-tick appetite, filled in turn order -- but
    # never below the equal share, because a cap the volume cannot fit inside
    # `n` rows does not spread the day, it DUMPS the residue on the last row of
    # it. Melon and fertilizer have no town bid at all (`spec.SHOP_CONSUME`
    # columns 4 and 8 are zero on every shop) and B pushes 11.6 melon a burst,
    # so a bare per-tick cap would put the whole melon line on hour 22 -- which
    # is `LOT4`'s turn-21 row, measured at band margin -831. With the floor, the
    # cap binds only where it can be MET: it front-loads to what the town eats
    # while the day's volume fits, and degrades to the equal split when it does
    # not. Whatever is still left at the last row is placed there anyway, so no
    # unit is ever left in a shed that clips.
    n_i = xp.asarray(n, i32)
    cap = xp.maximum(xp.maximum(PJ.town_tick_units(xp, shops), 1),
                     (vol + n_i - 1) // n_i).astype(i32)
    left, rows = vol, []
    for k in range(n):
        take = left if k == n - 1 else xp.minimum(cap, left).astype(i32)
        rows.append(take.astype(i32))
        left = (left - take).astype(i32)
    return xp.stack(rows).astype(i32)


# [MIDDAY_PLACE_V2] The deposit's deadline and the row that sells it are the
# same turn or the deposit sells nothing, so the two are checked against each
# other rather than each against `O.SELL_TURNS[-1]`: `EARLY_SELL` mode "B"
# moves the last lot to turn 5, which is in front of every deposit the rule
# admits. Import-time, like every assert in this file.
assert not MIDDAY_PLACE_V2_ON or early_lot_turns()[-1] == MIDDAY_PLACE_V2_TURN, \
    "MIDDAY_PLACE_V2 banks in front of the day's last SELL lot; that lot has moved"


# [SAME_DAY_FERT] One excursion clock per block, the same law the two asserts
# above state: this switch owns `ins`, `m_ins` and the deposit's item, so it
# cannot share a build with the melon excursion or with `BANK_BEFORE_LOT`.
assert not (SAME_DAY_FERT_ON and (MELON_OPEN_ON or MIDDAY_PLACE_V2_ON
                                  or MIDDAY_PLACE_ON or BANK_BEFORE_LOT_ON)), \
    "SAME_DAY_FERT is the melon excursion with fertilizer in it; one at a time"
assert SAME_DAY_FERT_LAST_DAY >= 1, \
    "day 0 has no animal that has stood overnight; the knob starts at day 1"


# `TAIL_FILL_ON` [SWITCH]: work the turns between the end of a block and the
# end of the day, instead of PASSing them.
#
# `_routes` cuts each block at the last tile whose whole chain the budget
# reaches, so what is left over is the turns the *next* tile did not fit into:
# 555 idle unit-turns a game by the census, 41% of all our idle, a mean 2.5
# turns of day left, and a carry-free task reachable at 81% of them a median 1
# tile away. The filler spends them on a task **the day's route never touches**
# -- a tile at rank >= `n_admit`, which no block can hold, since every block
# ends at `min(jmax, n_tasks - 1)` -- so it can neither double-work a tile nor
# move a tile the admit stage priced.
#
# Three ops and no others, because each has to bank into tile state on the turn
# it is taken and need nothing carried [`sim/units.py`]:
#   COLLECT_FERTILIZER  `has_an & t_favail == 1`   -- a free unit of fertilizer
#   WATER               `is_pl & t_water == 0`     -- +1 yield in window, and
#                                                     a dry plant weeds tonight
#   DIG                 `kind == KIND_WEED`        -- and *only* a weed: the
#                                                     engine's DIG clears any
#                                                     unlocked non-empty tile,
#                                                     a standing crop included.
# HARVEST is out on purpose: it lands in the unit's inventory, which the sale
# cannot draw on, and the DROP day is out with it -- the filler would walk the
# unit off the tile its return leg is measured from. FEED and FERTILIZE need a
# PICKUP; CARE banks nothing on an animal the day does not also feed
# (`eod.refresh_animals`: the bonus is paid `& fed`), and the animals the day
# does feed are admitted tiles.
#
# OFF, `tail_fill` is `None` and every tail turn is the `O.OP_PASS` it was
# (`tests/test_tail_fill.py`).
#
# VERDICT 2026-09-09: **ON**, paired with `BANK_BEFORE_LOT_ON` -- the pair is
# what was measured, and the two ship and get withdrawn together. Sim sweep,
# 128 pinned held-out boards, both seats, paired
# (`docs/strategy/2026-09-09-switch-sweep.md`): this switch alone HELD42 +775
# (t 3.31, +2 flips / -0 drops), LEG20 +1,366, LOSS12 -354; with the bank
# excursion HELD42 +817 (t 3.50, +2/-0), LEG20 +1,404 (t 2.70), LOSS12 +575.
# Engine confirmation (`docs/strategy/2026-09-09-plateau-review-verdicts.md`
# Sec. 32): pair HELD-OUT +2/-0, H_dm +801, LEG20 +1,403 a game (filler alone
# +748 / +1,365) -- the first planner switch to pass the leg-family rule with
# a full standard error of margin. Composed with theta `flow166_g170` on the
# 55 held-out live boards it reads +4,018 a game against +3,145 for the theta
# alone (`docs/strategy/2026-09-10-ship-pair.md`).
TAIL_FILL_ON = True

#: Fill hops one unit's tail may take under `TAIL_FILL_ON`: walk to the nearest
#: free task, take it, and look again from there. Two, because the tail is 2.5
#: turns long on average and a hop costs the walk plus the op -- a third hop
#: would compile a scan no tail can pay for.
TAIL_HOPS = 2

# ---- IDLE_TAIL_HOPS: the tail filler's hop budget [SWITCH, OFF] ------------
#
# The two hops above were sized in 2026-09-03 against a mean tail of 2.5 turns.
# The tail is longer than that now. IDLEOPS re-read it off the engine on 34
# Kaggle replays (`S/idleops/idle.py`, `docs/strategy/2026-09-16-idleops.md`):
# our shipped pair idles **706 unit-ops a game (10.5 %)** against M & M & P & Q's
# 335 (5.1 %), and the split by where the op sits in its unit's own day is
#
#     dawn (before the unit's first act)   ours 297   theirs  76
#     gap  (between two acts)              ours  10   theirs   6
#     TAIL (after the unit's last act)     ours 398   theirs 243
#
# The dawn half is the turn-1 BUY-row law and its family is closed
# (`ROUTE_FREEFIRST_ON`, `PRESTOCK_V2_ON`, both measured and both off). The
# tail half is this constant: `fill_free = (idx >= n_tasks) & (cfill !=
# OP_PASS)` (`_routes`) is read off the MORNING board, where every unadmitted
# plant tile still has `t_water == 0`, so the candidate supply is not what runs
# out at the end of a tail -- the hop count is. 1.36 idle turns are left on an
# average unit-day after the filler, the care hop and `CARE_FILL_HOPS` have all
# had their turn, and 95 idle ops a game are spent STANDING ON an open
# WATER/COLLECT/HARVEST the day never comes back to (against their 50).
#
# ON, the filler loop runs `IDLE_TAIL_HOPS` times instead of `TAIL_HOPS`. That
# is the whole switch: the hop body, its gate (`f_d + 1 <= f_left`, so a hop
# that does not fit is never taken), its candidate mask and its strike-off are
# the ones `TAIL_FILL_ON` ships. Nothing else is credited with the turns --
# the hire enumeration's `route_turns(h)` is untouched, so the crew is the same
# crew and only its tails are longer.
#
# OFF, `tail_hops()` is `TAIL_HOPS`, the loop unrolls exactly as many hops as
# it always did and the champion theta decodes byte for byte
# (`tests/test_idleops.py`).
IDLE_TAIL_HOPS_ON = False

#: Hops the filler may take with the switch ON. Four, not three: the measured
#: tail is 1.36 turns per unit-day AFTER the two it has, and a hop onto a tile
#: the unit already stands on costs one turn, so the reachable work is two more
#: hops deep. A magnitude, a module constant, no gene [LAW, gene-slope].
IDLE_TAIL_HOPS = 4


def tail_hops() -> int:
    """Hops the tail filler unrolls -- a Python int read at trace time."""
    return IDLE_TAIL_HOPS if IDLE_TAIL_HOPS_ON else TAIL_HOPS


# `TAIL_CARE_ON` [SWITCH]: spend the same tail turns on FEED and then CARE,
# which the filler above rules out and which the animal census says is the
# largest single lever the planner has.
#
# The engine pays the pair and neither half alone (`eod.refresh_animals`,
# `kaggriculture.py:810-833`): production fires whether or not the animal ate,
# so a feed buys survival and not units; the care bonus is banked only
# `if cared_today and fed_today` and an unfed production night *wipes* whatever
# was banked. A fed-and-cared animal therefore runs at `(1 + interval)/interval`
# units a day against `1/interval` -- x3 on a cow, x4 on a sheep -- and the
# joint counterfactual over 16 real-engine replays is +8,375 coins a game
# against +1,116 for feeding alone and +1,974 for caring alone.
#
# What the day leaves on the table is exactly what the tail can pick up: 595.9
# idle unit-turns a game in the last six hours, 43.1 animal-days fed but
# uncared (`want_care = want_feed & care_ok` at 2278 drops the care whenever
# today's *spot* quote fails `care_pays`), and 354.8 wheat units already
# sitting in unit inventories at hour 23 -- harvested off our own wheat tiles
# and never dropped. So the tail feeds out of a carry the day already paid for
# and cares out of a turn the day was going to PASS.
#
# Two departures from `TAIL_FILL_ON`, both forced by what these two ops are:
#
#   * A visit is up to **two** turns (FEED then CARE), not one, and the FEED
#     half is gated on the unit's own modelled wheat carry -- a CARE on an
#     unfed animal banks nothing, so a visit with no wheat behind it is only
#     taken when the animal is already fed (or the day's route feeds it).
#   * The "tiles no block holds" rule is dropped outright: the tile a block
#     already ran its ops on is *the* case that pays, since it is the block's
#     own feed whose care `care_pays` refused. Double-work is free here where
#     it is not for the filler -- the engine no-ops a second CARE (`:526`) and
#     a second FEED before it takes the wheat (`:507`) -- and the candidate
#     mask already excludes the tiles the day's own plan feeds or cares, so
#     the relaxation costs no turn it does not buy -- and it is a third of
#     what the switch earns: restricted to the unit's own prefix
#     (`rank <= e`) the hop is worth +179 coins a game against +269 without
#     the restriction, paired over the same 384 games (t 2.65 between the two,
#     and not one game changes hands -- it is margin, not wins).
#
# FEED and CARE are day-flag ops read once at end of day, so unlike the
# filler's WATER/DIG nothing here depends on *when* in the day the turn falls,
# and a tail visit can never race the block that owns the tile.
#
# Independent of `TAIL_FILL_ON` in both directions: the two share the tail
# cursor (`f_t0`, `f_left`) and nothing else, and when both are on the care
# hop runs first, because a banked care bonus outbids any of the filler's
# three ops. Off on a DROP day, whose tail is the return leg.
#
# Measured, ON against OFF, paired on the same games (flow58_g450, 48 seeds
# x 2 seats x kagg2 + the three class-A tapes = 384 games a leg):
#
#     seed base   win OFF -> ON   d margin   t     discordant
#     777001      53.6 -> 55.5%   +269       2.79  13
#     777002      64.3 -> 63.8%   +257       2.46   8
#     both        59.0 -> 59.6%   +263       3.70  21
#
# The coin margin replicates almost exactly and the *win rate* does not move:
# +0.6 points over 768 games on 21 discordant games is a coin flip. On its own
# that is a real gain on the wrong axis -- it makes a won game richer rather
# than turning a lost one -- and on its own it shipped off.
#
# So the census's +8,375 ceiling is not what the tail can reach: what the day
# leaves undone is mostly *unfed* animals, and a tail FEED needs wheat the
# unit is carrying, which most blocks never harvest. What is left is the free
# half -- the CARE on the animal the block itself fed -- and a tail two and a
# half turns long only reaches the ones a step or two away. The cost side is
# small to match: +5 % of planner wall clock (max per-turn 81.0 -> 85.8 ms
# over three real games), against `TAIL_FILL_ON`'s +70 %.
#
# ON since 2026-09-03, **as the third of a stack** -- with `SURVIVAL_WATER_ON`
# and `FEED_MANDATORY_ON`, whose blocks below carry the same reference. The
# three were measured together against the same OFF runs (flow58_g450, 48
# seeds x 2 seats x kagg2 + the three class-A tapes, two seed bases = 768
# paired games). The three singles are +323 / +263 / +82 and the stack is
# +583, not their +668: they overlap, because they are all bidding for the
# same unit-turns. What the *stack* returns:
#
#     opponent        n  win OFF   win ON   d margin       t  disc
#     kagg2         192    92.7%    93.2%        +94    0.52     5
#     103254816     192    58.9%    60.9%       +605    2.10    16
#     104502967     192    50.5%    55.7%       +849    4.17    10
#     104547425     192    33.9%    35.9%       +784    3.28     8
#     ALL           768    59.0%    61.5%       +583    5.03    39
#
#     777001        384    53.6%    57.6%       +609    4.21    21
#     777002        384    64.3%    65.4%       +557    3.07    18
#
# Positive on every one of the four opponents and on both seed bases, and this
# time the **win rate moves with the coins**: +2.5 points over 768 games on 39
# discordant games, which is what the single legs each failed to buy (+0.6,
# +1.0 and +0.8 points, all coin flips). Alone this switch spends the tail
# on care the day's turn budget was already fighting; stacked, the other two
# hand that budget back -- `SURVIVAL_WATER_ON` drops ~15 dead-crop waterings a
# game out of the mandatory tier, and the tail gets longer, which is exactly
# the re-measurement `care_hold/report.md` asked for. (`S/stack/`,
# `S/tail_care/report.md` for this switch's own +263 t 3.7.)
#
# OFF, `tail_care` is `None` and every tail turn is the `O.OP_PASS` it was
# (`tests/test_tail_care.py`), which is what that file's OFF half and the
# digest pins of `test_route_early` hold the switch to.
TAIL_CARE_ON = True

#: Care hops one unit's tail may take under `TAIL_CARE_ON`. One, not
#: `TAIL_HOPS`' two: a visit costs the walk plus up to two ops against the
#: filler's one, the tail is 2.5 turns long on average, and the census counts
#: 1.5 fed-but-uncared animal-days and 2.1 wheat-in-hand unfed animal-days a
#: *day* against ten-odd units offering a tail -- so the first hop already
#: covers the demand and a second would only buy scan time.
TAIL_CARE_HOPS = 1

# `CARE_FILL_ON` [SWITCH]: spend *every* turn a unit would otherwise PASS on a
# CARE, not just the first one `TAIL_CARE_HOPS` buys.
#
# The engine's rule, exactly (`_daily_refresh_animals`,
# `kaggriculture.py:804-833`, ported at `sim/eod.py:94-127`). At each eod, for
# `next_day = day + 1`:
#
#     if tile["cared_today"] and tile["fed_today"]:
#         tile["pending_care_bonus"] += 1                      # :829-830
#
# and on a production night -- `days_since_first = next_day - placed_day -
# first_yield_day`, `>= 0` and `% interval == 0` --
#
#     bonus = pending_care_bonus if tile["fed_today"] else 0   # :826
#     yield_units = min(max_held, yield_units + 1 + bonus)     # :827
#     pending_care_bonus = 0                                   # :828
#
# So a CARE is worth one product unit at the *next fire*, and only if the
# animal is fed on the day the care is taken (the bank never increments
# otherwise) and fed again on the night it fires (an unfed fire wipes the bank
# without paying it). A cow (`interval` 2) cared and fed every day banks 2
# between fires and yields `1 + 2 = 3` milk per two days against the bare 1 --
# the "+50 %" of the loss autopsy read as its whole 3-per-2. `OP_CARE` itself
# is idempotent within the day (`:527`, the sim's `t_cared[tile] == 0` guard at
# `sim/units.py:172`), so the engine's cap is **one CARE per animal per day**
# and a second is a turn spent on a no-op.
#
# What is left on the table (autopsy of Kaggle loss 105393487, seat 1 = sub
# 55920227): on the same 8 COW + 4 SHEEP herd the opponent issued 967 CARE ops
# to our 230 and out-earned us by 11.1k of milk and 6.4k of wool. 1,309 of our
# unit-turns are PASS (20.3 % of our unit actions against their 4.8 %) and 604
# of them sit in hours 18-23 -- the tail, after `_routes` has cut each block at
# the last tile whose whole chain the budget reaches. The mechanism is already
# here: the planner emits `OP_CARE` (230 a game) and `TAIL_CARE_ON` already
# walks one hop of that tail. The gap is **coverage**, and it is a coverage gap
# for one reason: `TAIL_CARE_HOPS` is 1, sized for a mean 2.5-turn tail, while
# the tails that hold the 604 are the long ones -- day 5 of that episode has
# five of ten units PASSing every hour of the day.
#
# ON, the same tail cursor takes up to `CARE_FILL_HOPS` further hops, each of
# them a walk plus one CARE and nothing else. Four rules, and they are the
# engine's:
#
#   * **uncared** -- `t_cared == 0` this morning and the day's own route does
#     not already CARE the tile, so no hop can land on a turn the engine
#     no-ops, and `cf_free` strikes a tile off for every later unit and for
#     this unit's own later hops. That is the cap held at one a day.
#   * **fed** -- already fed this morning (`t_water == 1`) or fed by an
#     admitted rank of the day's route. A CARE on an animal nothing feeds banks
#     nothing at all (`:829`); it is not a cheap care, it is a wasted turn.
#   * **headroom** -- `care_ok`'s own `bank_carry + 2 <= max_held`, with the
#     fire-night wipe in it: `min(max_held, ...)` at `:827` means a bank with
#     nowhere to go pays nothing.
#   * **horizon** -- the fire this care banks for is on or before
#     `VAL.pay_day()`, so the unit it adds can still be sold.
#
# What it may *not* do is the whole of the "no displacement" claim, and it is
# structural rather than measured: every hop is written from `f_t0`, the tail
# cursor, which starts after the block's last turn (and after any
# `MELON_OPEN`/`BANK_BEFORE_LOT` excursion `ins` charges for), and it fires
# only where `active` -- a unit `_routes` gave a block. So it writes into turns
# that were `O.OP_PASS` and into no others; it changes no admission, no block
# cut, no PICKUP row, and no market row -- including `HIRE_ROW_ON`'s
# `n_hire_row`, which counts units that act and cannot learn about a unit that
# already did. Off on a DROP day, whose tail is the return leg.
#
# It is a CARE filler and not a second `TAIL_FILL_ON` on purpose. That switch's
# post-mortem is the reason: an idle-turn filler that puts *new tiles* to work
# plants a marginal tile that sells into our own curve, and the block above
# prices it at +70 % of planner wall clock for the privilege. A CARE is the
# opposite trade -- the animal is already owned, already fed and already
# routed, the turn was going to PASS, and the only thing the extra unit
# displaces is nothing at all. The one thing it does add to the market is the
# milk and wool themselves, which land in the same glutted stream
# `CARE_HOLD_ON`'s report measured; that is why the cap and the headroom test
# are engine-exact and not approximated, and why the fed gate is a hard
# requirement rather than a preference.
#
# Independent of `TAIL_CARE_ON` and `TAIL_FILL_ON` in every direction: the
# three share the tail cursor (`f_t0`, `f_left`, `fx0`, `fy0`) and nothing
# else. Order is care hop, then filler, then this -- `TAIL_CARE_ON` may spend
# two turns on one tile (its FEED unlocks its own CARE) and so outbids a lone
# care, and a tile either of the first two takes is struck out of `cf_free`
# before the fill hops run.
#
# OFF, `care_fill` is `None`, `_routes` compiles none of the hops and every
# tail turn is the `O.OP_PASS` it was (`tests/test_care_fill.py`, whose OFF
# half holds the switch to `test_route_early`'s digests).
CARE_FILL_ON = True

#: Fill hops one unit's tail may take under `CARE_FILL_ON`, on top of whatever
#: `TAIL_CARE_ON` and `TAIL_FILL_ON` have already spent. Four: a lone CARE hop
#: costs the walk plus one turn, the long tails this switch exists for run to
#: twenty-odd turns, and four hops is the most a herd of twelve can use in one
#: tail once `cf_free` has struck the ones the day already cares.
CARE_FILL_HOPS = 4

# `CARE_HOLD_ON` [SWITCH]: price CARE off the forward quote the animal stream
# already trades on, instead of the spot quote of the day the care is taken.
#
# `care_pays` is `price[product] > price[WHEAT]` at hour 0 (`_derive` below).
# Over days 16-29 milk falls 96 -> 33 while wheat climbs to 44, and the
# census's 43.1 fed-but-uncared animal-days a game start at day 15 and peak on
# day 26 -- the same crossover. But a care taken today banks a unit that fires
# at `h_next` and reaches the market days later, when the town has drained the
# glut that crashed the quote; the gate reads the trough and refuses the trade
# on the strength of a price the unit will never be sold at.
#
# ON, the product side of that comparison becomes
#
#     max(spot, price_table[product][inv_at_day(FIRST_YIELD) + pipeline])
#
# which is `_candidates`' `inv_h` -- the *sales-window* curve of section 1.1,
# the hour-0 inventory drained by the town to the product's first fire plus
# every unit our own board has already committed to that market. So it is a
# realised-market read and not `spec.PRICE_BASE`: our own glut is priced into
# it through `_pipeline_units`, and a market we are genuinely flooding does not
# get a forward premium. The `max` is the floor: a banked unit is worth at
# least what the same unit fetches today, and it keeps the switch monotone --
# ON only ever loosens `care_pays`, so the measurement reads "care more" and
# not "care differently".
#
# The forward quote moves the *gate* and nothing else. Three prices stay at
# spot on purpose:
#
#   * the wheat side of the comparison -- the wheat is spent today out of
#     today's shed or today's BUY row, so today is what it costs;
#   * `care_val`, the term `feed_value` carries into the *purchase* test -- a
#     care-only feed still has to clear the wheat's own marginal quote at
#     today's price, which is what keeps the switch off the BUY row;
#   * `v_care`, the op's admitted labour value -- admission is a contest for
#     today's turns, and every other op bids in today's coins. Pricing a care
#     at a forward 267 against a spot 33 made it outbid the ripe tomato beside
#     it: measured that way the switch was worth -234 coins a game (t -1.83,
#     384 paired games at seed base 777001), the `dev_weight` note's failure
#     mode in miniature. It is floored at one coin instead, so the care the
#     forward quote newly buys is admitted but never jumps the queue.
#
# So what ON actually adds is the free half of the census: a one-turn CARE on
# an animal the day is already feeding, banked at no wheat and no detour.
#
# The other two gates are untouched: `care_headroom` (the bank has somewhere to
# go) and `h_next <= VAL.pay_day()` (the fire it banks for is still sellable).
#
# Measured, ON against OFF, paired on the same games (flow58_g450, 48 seeds
# x 2 seats x kagg2 + the three class-A tapes = 384 games, seed base 777001):
#
#     opponent      n   win OFF -> ON   d margin     t   discordant
#     kagg2        96   87.5 -> 87.5%      -457   -2.35    0
#     103254816    96   52.1 -> 53.1%        +4    0.01    3
#     104502967    96   44.8 -> 44.8%      +111    0.44    4
#     104547425    96   30.2 -> 30.2%      -611   -2.52    4
#     ALL         384   53.6 -> 53.9%      -238   -1.86   11
#
# And it works: over twelve replays against tape 103254816 the fed-but-uncared
# animal-days fall 40.3 -> 24.7 a game, the unfed ones 69.2 -> 66.0, the share
# of animal-days banking no bonus 30.3 % -> 24.9 % (the opponent's is 12 %),
# and early starvation deaths 1.00 -> 0.67. The gate was the thing stopping us
# caring, and opening it closes most of the census gap -- for -238 coins.
#
# So the reading is not "the switch does not fire", it is **the care-only
# counterfactual is not recoverable inside the day's turn budget**. The
# autopsy's +1,974 priced the extra units at realised *season mean* prices and
# charged nothing for the turn that banks them; a real CARE costs one turn of a
# block whose tail `_routes` was already cutting, and the milk and wool it adds
# arrive in the markets we are already glutting. That is why the joint
# feed-and-care term is the one worth chasing and the halves are not.
#
# OFF, `care_price` is `view.price[an_prod]` and `care_pays`, `care_val` and
# `v_care` are the three expressions they always were
# (`tests/test_care_hold.py`).
CARE_HOLD_ON = False

# `FEED_FORWARD_ON` [SWITCH, FEEDKEEP1]: price the hungry animal's remaining
# milk/wool/egg stream in the feed-value gate (`keep_val` in `_derive`) off a
# FORWARD quote instead of today's spot. OFF, `VAL.animal_value` reads
# `view.price` -- on a trough (board 59204382 d19-20: milk 36 -> 5) a cow's
# whole remaining stream prices below one wheat and the herd is left to escape
# while the town drains the glut back. ON, the product quote is
#
#     max(spot, price_table[product][inv_at_day(FEED_FORWARD_K) (+ pipeline)])
#
# i.e. the hour-0 book drained `FEED_FORWARD_K` days by today's shops, plus
# (`FEED_FORWARD_PIPE`) every unit our own board has committed to that market
# -- the `CARE_HOLD_ON` / `ANIMAL_BUY_FWD_ON` read. Only the three animal
# products move; fertilizer, the bank term and the wheat side stay at spot.
# The subtracted stock is priced on the same quote so the flow-not-stock rule
# is unchanged. OFF is the identical program (a Python `if` on this global).
FEED_FORWARD_ON = False
#: Days of town drain in the forward quote.
FEED_FORWARD_K = 5
#: Include our own committed pipeline in the forward book.
FEED_FORWARD_PIPE = True

# `ANIMAL_BUY_FWD_ON` [SWITCH]: price the animal-acquisition bound `ub_coins`
# off the sales-window curve the animal's units are actually sold on, instead of
# the spot quote of the day it is bought.  The mechanism, the wool arithmetic
# and the invariant it costs are documented at the use site in `_derive`
# (search `ANIMAL_BUY_FWD_ON`); `docs/strategy/2026-09-16-woolprice.md` carries
# the measurement.  OFF, `ub_coins`, `acquire_ok` and `v_place` are the three
# expressions they always were (`tests/test_animal_fwd.py`).
ANIMAL_BUY_FWD_ON = False

# `FEED_MANDATORY_ON` [SWITCH]: a feed that carries a care goes in the
# mandatory tier with the survival feeds.
#
# `mandatory` below admits `want_feed & must_feed` -- only an animal already
# one day hungry. Every other feed sits in the value tail, and `_routes` cuts
# each block at the last tile whose whole chain the budget reaches, so the tail
# is exactly where a feed and the care riding on it die together. The census
# counts 3.0 of our animals starving mid-season against the opponent's none,
# and 31 % of our animal-days banking no care bonus against their 12 %.
#
# ON, the tier test becomes `want_feed & (must_feed | care_ok)` -- which is
# `must_feed` widened by exactly `want_care`, since `want_care = want_feed &
# care_ok`. So the promoted tile is one the day already decided to feed *and*
# care: the wheat is already bought and rationed (`want_feed` is `feed_pass &
# (feed_rank < wheat_avail)`), so this switch cannot buy or divert a single
# wheat -- it moves nothing but admission order.
#
# The exposure is deliberately the smallest a tier promotion can have. The
# note at the `dev_weight` block records that promoting *development* to this
# tier measured -23,312 +- 9,198 coins, because the route order carries no
# value information inside a tier and anything admitted ahead of a harvest
# spends the turns that harvest needed. A FEED and a CARE are one turn each on
# a tile the block is routed through anyway, against a PLACE or a PLANT that
# drags a build, a pickup and a season of watering behind it.
#
# Measured, ON against OFF, paired on the same games (flow58_g450, 48 seeds
# x 2 seats x kagg2 + the three class-A tapes = 384 games a seed base):
#
#     seed base   win OFF -> ON   d margin    t     discordant
#     777001      53.6 -> 54.7%      +39    0.43     4
#     777002      64.3 -> 64.8%     +124    1.07     6
#     both        59.0 -> 59.8%      +82    1.11    10
#
# Coins are flat and the win rate moves 0.8 points on ten discordant games,
# eight of them ours -- p about 0.06 one-sided, which is a lean and not a
# result. The one consistent term is `kagg2` at -290 a game (t -2.78): our
# oldest opponent is the one the promotion costs, because its games are the
# ones our turn budget is already tightest in. Against the three class-A tapes
# it is +263 / +80 / +272.
#
# On its own that did not clear the bar, and it shipped off -- not because the
# mechanism is wrong: it is the only one of the two levers measured there that
# is not coin-negative, it cannot touch the BUY row, and the census moves the
# right way (fed-but-uncared animal-days 40.3 -> 37.8, unfed 69.2 -> 66.7 over
# twelve replays). The note ended "re-measure it after anything that lengthens
# the block tail -- that is the budget the promotion is really fighting".
#
# ON since 2026-09-03, on exactly that re-measurement: stacked with
# `SURVIVAL_WATER_ON` and `TAIL_CARE_ON`, which is what lengthens the tail and
# what spends it. The stack is +583 coins a game at t 5.03 over 768 paired
# games, win 59.0 -> 61.5 %, positive on all four opponents and both seed
# bases -- the table is at `TAIL_CARE_ON` above, the runs in `S/stack/`. This
# switch's own single leg is the weakest of the three (+82 a game, t 1.11,
# `S/care_hold/report.md`) and it is promoted as part of the stack rather than
# on its own evidence: it is admission order on a tile the day already decided
# to feed and care, so it costs nothing but the turn, and the turn is what the
# other two are buying. Watch `kagg2` if the stack is ever taken apart -- alone
# this switch is -290 a game (t -2.78) there, and it is the only leg of the
# stack that is not comfortably positive against it (+94, t 0.52).
#
# OFF, `mand_feed` *is* `must_feed` and the tier expression is unchanged
# (`tests/test_feed_mandatory.py`), which is what that file's OFF half holds
# the switch to.
FEED_MANDATORY_ON = True

# `SURVIVAL_WATER_ON` [SWITCH]: price the survival watering, and rank it above
# the rest of the mandatory tier when it is worth taking.
#
# The engine kills a planted tile two ways, and only one of them is a watering
# (`kaggle_environments/envs/kaggriculture/kaggriculture.py`):
#
#   * `_daily_refresh_plants`, :782-784 -- `consecutive_unwatered >= 2` at the
#     nightly refresh turns the tile to WEED whatever it is holding. A tile
#     that enters the day at `cons == 1` and is not watered dies tonight.
#   * `_decay_plants`, :752-766 -- a crop past `max_lifespan_step` loses one
#     unit every other *step* and becomes WEED at zero. Ongoing crops are given
#     one of these the moment they fire for the `max_yield`-th time (:801-802),
#     so a spent strawberry decays out on its own two days later. **Watering
#     does nothing to this path**; it is the crop's designed end of life.
#
# Measured over the 32 McGrain replays (`S/survival_water/weedcount.py`), the
# 12.6 WEED tiles the autopsy counts at day 29 are 32.6 decay deaths a game --
# 29.5 of them spent STRAWBERRY -- against **0.56 unwatered deaths**, plus 1.4
# weeds spawned on empty tiles (:836-840). The tail is not neglect.
#
# What the tail *is* costing is the mirror image. From day 21 on, 0.8 -> 5.6
# tiles a day are PLANTs whose `crop_remaining_value` is exactly 0: an ongoing
# crop past its last fire holding nothing, or a one-time crop whose clamped
# harvest day falls past `pay_day()`. `must_water` does not look at that value,
# so each of them still trips the MANDATORY tier every other day and takes a
# unit-turn ahead of priced work -- **30.3 value-0 tile-days, ~15 mandatory
# waterings a game**, all of them in the window where the turn budget is
# tightest and the crop tiles that *can* still sell are being cut.
#
# ON, both halves of that are fixed with the value the day already computes:
#
#   1. a survival watering is mandatory only where the crop's remaining value
#      at its own sale day beats `SURVIVAL_WATER_MIN` -- the turn it costs.
#      Below that the tile leaves `must_water` entirely: no water, no tier, and
#      it weeds tonight, which is what it was going to do anyway.
#   2. the ones that pass go one tier *above* the rest of the mandatory work,
#      so the tile the admit stage cuts from the mandatory tail is never the
#      one that dies for good tonight. That is the 0.56 tiles a game the first
#      rule leaves on the table (23 coins of standing units + 200 coins of
#      forgone ongoing production, at the prices the replays realised).
#
# `crop_remaining_value` (`valuation.py:214`) is the same function `v_water`
# already prices the watering with, and it carries `pay_day()` inside it, so
# "can this still sell before the season pays" is asked per tile rather than by
# the blanket `survival_pays` day test. `harvest_age` is hoisted above the
# water block to feed it; the expression is unchanged and nothing it reads
# moves, so OFF is byte-identical (`tests/test_survival_water.py`).
#
# ON since 2026-09-03. Its own paired leg is the strongest of the three
# animal/tier switches promoted together -- +323 coins a game at t 5.4 over
# 768 games (`S/survival_water/report.md`) -- and it is the one that makes the
# other two affordable, because the ~15 mandatory waterings a game it stops
# spending on already-dead crops are unit-turns handed straight back to the
# block tail. Stacked with `TAIL_CARE_ON` and `FEED_MANDATORY_ON` (the table
# is at `TAIL_CARE_ON` above, the runs in `S/stack/`): +583 a game, t 5.03,
# win 59.0 -> 61.5 % over 768 paired games, positive on every opponent and
# both seed bases. Measured untrained-for -- `flow58_g450` was trained with
# all three off -- so the enumeration has not yet re-priced the tier it now
# ranks above.
SURVIVAL_WATER_ON = True

#: Coins the crop's remaining stream must beat for a survival watering to be
#: mandatory under `SURVIVAL_WATER_ON`. 0 = "it still sells something": the
#: watering costs one unit-turn and the tier promotion is what pays for it.
#: Raise it to charge the turn a real price.
SURVIVAL_WATER_MIN = 0

#: Turns the admit stage charges each unit for the return leg on a DROP day --
#: the walk back to a shed-access tile plus the DROP itself. Like `EST_LEAD`
#: this is an estimate the exact route corrects: `_routes` charges `DIST_SHED`
#: from the block's real last tile, and `ADMIT_ROUNDS` drops whatever that
#: leaves unreachable. Set *under* the mean return (`DIST_SHED` averages 3.6
#: over the board) on purpose -- over-admission is repairable, under-admission
#: is not.
EST_HOME = 3

#: Fixed-point unit of the grow value multiplier: GROW_ONE == x1.0 (`brain`
#: decodes it and aliases this name; the budget scales candidate values by it).
GROW_ONE = 256

#: Fixed-point unit of the early-spend deferral: DEFER_ONE == x1.0, i.e. no
#: deferral (`brain` decodes `macro.animal_defer` against it and aliases this
#: name). A power of two, and applied as `x * keep // DEFER_ONE` on
#: non-negative int32, so the untouched case is *exactly* `x` on both backends
#: and the largest scaled candidate value (`GROW_MAX * VALUE_CAP` = 4.19e6)
#: stays inside int32 at 1.07e9.
DEFER_ONE = 256

# ---- the crew ramp's deferral, forced by a constant [SWITCH] ------------
# `macro.animal_defer` [g10] above is the gene that was supposed to do this,
# and it is inert twice over. (a) It is 0 in all 960 rows under the champion
# theta `flow58_g450` -- the biases-only ES has never turned it on. (b) Even
# set, it is gated on `crew_now < macro.crew_target` and `crew_now` is read
# back off the very hire bill the deferral is meant to protect, so the
# deferral cancels itself the moment it works: the `HIRE_CLAMP` post-mortem
# (block comment near :829) measured `defer 256` and `defer 66` as
# byte-identical plans.
#
# So the question the gene never got to ask is asked here by a constant, on
# the days the diagnosis actually points at. `scratchpad/shortfall/report.txt`
# traced `_derive`'s pass-B locals over 24 real games: `purchase_shortfall`
# is a two-day spike -- days 6-7 carry 75 % of the whole season's shortfall
# coins -- and the starved candidates are cow and sheep (62 % of the coins),
# then strawberry seed and wheat. The median shortfall day holds a purse of
# 616, spends 94 % of it, and is still 2,063 coins short. Netting out the
# "richer board" confound (regress ours on shortfall and theirs together)
# leaves -0.70 of our coins per shortfall coin.
#
# ON, on every day at or before `ANIMAL_DEFER_LAST_DAY`, the animal lists are
# priced at `ANIMAL_DEFER_KEEP / DEFER_ONE` -- straight through, with no
# `crew_now` comparison and no gene -- so the purse the greedy walks reaches
# the crew's own wheat and the seed lists before a cow outbids them. Later
# days keep the gene's expression exactly.
#
# VERDICT: NOT CONFIRMED, AND EMPHATICALLY SO -- THE SWITCH SHIPS OFF AND
# ITS REAL RESULT IS THE MEASUREMENT OF WHAT THE EARLY HERD IS WORTH.
# `flow58_g450`, real engine, four opponents (kagg2 + three class-A tapes),
# `--seed-base 777001`, n=64, paired on (seed, opponent, seat) against the
# shipped default (the OFF arm reproduces `S/hour0b/A48_777001.csv` to the
# coin on all 256 shared rows, so the pairing is exact):
#
#     arm                       d ours   d theirs   d margin       t   win
#     last day 7, keep 128     -11,551   +27,239    -38,790  -11.43  62->9 %
#     last day 9, keep 128     -17,615   +21,666    -39,280  -12.56  62->8 %
#     last day 7, keep  64     -37,242   +48,932    -86,174  -19.28  62->2 %
#     last day 7, keep 384      +2,858    +5,746     -2,888   -1.29  62->66 %
#     last day 10, keep 384     +2,504    +2,897       -393   -0.18  62->67 %
#
# Halving the price of an animal candidate for eight days costs 38,790 coins
# of margin and takes the win rate from 62.5 % to 9.4 %; quartering it costs
# 86,174. Nothing else this campaign has switched moves the game by an order
# of magnitude like this, and the direction is monotone in the knob.
#
# **Where the loss goes is the finding.** Two thirds to four fifths of it is
# not our loss at all -- it is the opponent's gain. `d theirs` is +27,239 on
# the 4-opponent panel (70 % of the margin swing) and +20,078 against
# +(-5,051) of ours on the instrumented 24-game ledger (80 %). We are not
# spending the deferred coins worse; we are handing the milk/wool curve to
# the other seat. The early cow and sheep are a *denial* purchase before they
# are a production one: the shop's animal stock is a shared pot, and the
# milk/wool we do not produce is scarcity the opponent sells into. This is
# the `S/herd/` ledger-gap finding measured from the other side.
#
# The per-day ledger (24 games, 6 seeds x 2 seats x {kagg2, tape 104502967},
# `S/defer/ledger.txt`) says the deferral does not do the thing it was for:
#
#     metric (mean per game)          OFF        ON        d
#     animals standing, day 10       10.1       5.7     -4.4
#     hand-days, days 0-10           58.9      53.8     -5.1   <- goes DOWN
#     strawberry tiles, day 9        19.1      13.2     -5.8   <- goes DOWN
#     wheat bought, season          130.7      68.2    -62.5
#     purchase_shortfall, season   17,882    34,290  +16,408   <- goes UP
#
# The freed purse never reaches the crew: the day's crew is set by the hire
# enumeration's own argmax, not by what the purse can afford, so taking the
# cows away buys *fewer* hand-days, not more. The strawberry seed the
# diagnosis wanted funded is planted on *fewer* tiles, because a farm with
# four fewer animals earns less and the seed is bought out of the earnings.
# And `purchase_shortfall` -- the metric this switch was built to reduce --
# nearly doubles, which retires the whole shortfall thesis: shortfall is a
# measure of how much the farm wanted, and a poorer farm wants more than it
# can pay for on more days, not fewer. `S/shortfall/report.txt`'s regression
# (-0.70 of our coins per shortfall coin, board richness held fixed) does not
# survive the intervention: it was a correlation inside the confound, not a
# lever.
#
# The mechanism also bites harder than the name suggests. `a_keep` scales the
# *structure builds* at :4008 as well as the purchase values, so a day at
# half keep both under-buys animals and under-builds the coop or pasture they
# would stand in: day 0's plan grants the same six animals in both arms, but
# only two of them are standing on day 1 -- the other four sit in the shed
# with nowhere to go. Any future attempt at this window has to separate the
# two channels first.
#
# The other direction is the interesting null. At `keep 384` (animals worth
# 1.5x for the early days) both sides get *richer* -- ours +2,858, theirs
# +5,746 -- and the margin is flat to slightly negative (-2,888 t -1.29 at
# last day 7, -393 t -0.18 at last day 10, with the win rate up 3-5 points on
# 14-17 discordant games). So the champion is already sitting on the top of
# this curve: it cannot buy its way to a bigger early herd without feeding
# the same shared pot it is trying to deny. Bar for either direction was
# ALL >= 0 at n=64 to continue to n=384; nothing reached it, so no arm was
# run at n=384 and no confirmation run at 777002 was taken.
#
# `S/defer/report.txt` has the full ledger and the paired tables.
#
# OFF the `if` is a module-constant Python branch that never runs, `a_keep`
# is the gene's `xp.where` and nothing else, and the plan is byte-identical
# (`tests/test_animal_defer.py`).
ANIMAL_DEFER_ON = False

#: Last day (inclusive) the forced deferral covers. 7 is the far edge of the
#: shortfall spike: days 6-7 are 75 % of the season's shortfall coins and day
#: 8 is already down to 67.
ANIMAL_DEFER_LAST_DAY = 7

#: What an animal candidate is worth on a deferred day, in `DEFER_ONE` fixed
#: point. 128 is half price; `DEFER_ONE` itself is inert.
ANIMAL_DEFER_KEEP = 128

#: Coins per hand the crew-target ramp adds to 1.5's enumerated gain, for every
#: hand up to `macro.crew_target` [g10].
#:
#: Sized off `HIRE_BILLS`, which is a running sum of Fibonacci numbers, so the
#: marginal cost of the h-th hand is `fib(h)`: 377 for the fourteenth and 610
#: for the fifteenth. At 400 every hand up to the target pays for itself
#: against its own fib price through the fourteenth, so the argmax lands on
#: `min(target, what the purse can afford)` -- which is the point of a target
#: as opposed to `hire_bias`' constant tilt. Deliberately *not* larger: past
#: the target the push is flat, so the enumeration is back to arguing from the
#: day's work, and a bigger constant would only buy hands the fib curve has
#: already priced out of reach.
CREW_TARGET_PUSH = 400

# ---- CREW_PUSH_COST: size the crew-target push off the fib bill [SWITCH, OFF]
#
# THE CEILING (`2026-09-11-codex-defects.md:64-98`, census direction #5).
# `crew_push = CREW_TARGET_PUSH * min(h, crew_target)` pays the SAME 400 coins
# for a hand whose own marginal fib price is 1 and for one that costs 233 or
# 377, while `bills[h]` charges the fib price in full. So the ramp's promise --
# "every hand up to the target pays for itself" -- holds only while the
# marginal is under 400, and the enumeration's argmax stops short of the target
# on **46/300 board-days (15.3 %), mean 1.09 hands, at 18.8k cash** (so not a
# purse limit): the refusals sit on the 13th-15th hand, where fib is
# 233/377/610 and a negative `hire_bias` eats what is left of the 400.
#
# WHAT ON CHANGES. The push becomes a CUMULATIVE table read at `min(h,
# crew_target)` instead of a constant times it, built from `spec.HIRE_COST` --
# the h-th hand's own marginal price -- by `crew_push_cum()`:
#
#   `sum`   push(k) = CREW_TARGET_PUSH + HIRE_COST[k-1]: the fib bill inside
#           the target is refunded exactly and the 400 tilt survives on top, so
#           the marginal read is `dvalue + hire_bias + 400` for every hand up
#           to the target, whatever it costs. This is the census's "sized off
#           HIRE_COST[h]" read and the UPWARD direction that was never
#           measured.
#   `max`   push(k) = max(CREW_TARGET_PUSH, HIRE_COST[k-1]): the minimal
#           repair, identical to OFF for every hand through the 14th (fib 377)
#           and only covering the 15th/16th. B's `crew_target` tops out at 13,
#           so this mode is expected INERT on B and is here as the falsifier.
#   `exact` push(k) = HIRE_COST[k-1]: the bill and nothing else. SMALLER than
#           OFF through the 14th hand, so it is the opposite sign -- the
#           never-measured cost-shaped version of the downward sweep (300 ->
#           -1.2k, 200 -> -735 on the hr composition, `lever-ranking.md:67-70`).
#
# Past the target the push is flat in every mode, exactly as OFF: the table's
# last used entry is `crew_target`'s, and `min(h, crew_target)` still caps it,
# so a bigger crew than the ramp asked for is still argued from the day's work.
# Affordability (`bills[h] + cash_reserve <= view.money`) is untouched -- the
# push is a SCORE, not a purse.
#
# OFF the expression is literally `CREW_TARGET_PUSH * min(h, crew_target)` in
# int32, so the champion theta decodes byte for byte (`tests/test_crewpush.py`
# pins whole-plan digests against a pristine `git archive HEAD src` tree).
CREW_PUSH_COST_ON = False

#: Which cost-sized push `CREW_PUSH_COST_ON` installs [SWITCH, CREW_PUSH_COST]:
#: `sum` (bill refund + the 400 tilt, upward), `max` (cover only what 400
#: cannot, minimal), `exact` (the bill alone, downward). Read at trace time, so
#: a runner that sets it after import is honoured.
CREW_PUSH_COST_MODE = "sum"

CREW_PUSH_COST_MODES = ("sum", "max", "exact")


def crew_push_cum(mode=None, on=None):
    """int32[MAX_HANDS + 1]: cumulative push coins for `min(h, crew_target)`.

    Entry `m` is what a crew of `m` hands inside the target is pushed by, in
    total -- `[0] + cumsum(per-hand push)` -- so the site indexes it with the
    clipped count it already computes and the marginal between two counts is
    that hand's own push. OFF this is `CREW_TARGET_PUSH * m` exactly (pinned in
    `tests/test_crewpush.py`), which is what the shipped expression computes.

    `on` is that switch, overridable by the caller, because the switch is also
    a *gene* [SWITCH-GENE]: the site reads `_sw`, which may say ON while the
    module constant says OFF, and a table that re-read the constant here would
    hand the gene the flat push it was trying to leave. `None` -- every other
    caller, and the default -- is the module constant, unchanged.
    """
    marg = np.asarray(spec.HIRE_COST[:spec.MAX_HANDS], np.int64)
    mode = CREW_PUSH_COST_MODE if mode is None else mode
    if not (CREW_PUSH_COST_ON if on is None else on):
        per = np.full(marg.shape, CREW_TARGET_PUSH, np.int64)
    elif mode == "sum":
        per = marg + CREW_TARGET_PUSH
    elif mode == "max":
        per = np.maximum(marg, CREW_TARGET_PUSH)
    elif mode == "exact":
        per = marg
    else:
        raise ValueError(f"CREW_PUSH_COST_MODE {mode!r} not in "
                         f"{CREW_PUSH_COST_MODES}")
    return np.concatenate([[0], np.cumsum(per)]).astype(np.int32)



def drop_turns(h: int) -> int:
    """Turns a DROP day's block cut has, for a crew of `h` hands [section 4].

    A block ending at rank e costs `load(e) + home(e) + 1`, and the DROP then
    lands on turn `route_base + load(e) + home(e)`. That has to be at or before
    `SELL_TURNS[-1]`, because a unit acts before its turn's market and a DROP
    any later has no lot left to sell into. So the cut's budget is
    `SELL_TURNS[-1] + 1 - route_base`, which is 17 turns for a narrow crew and
    16 for one that needs the turn-2 hire row -- against the 22 / 21 a normal
    day gets, the six turns after turn 18 being worth nothing on day 29.
    """
    return O.SELL_TURNS[-1] + 1 - (O.ROUTE_BASE if h <= MO else O.ROUTE_BASE_WIDE)


def end_drop_turns(h: int) -> int:
    """`drop_turns` re-cut to `ENDROUTE_TURN` [SWITCH, ENDROUTE2].

    Same sentence, one lot later: the DROP has to land at or before the last
    turn that still has a market row behind it, and with `ENDROUTE_ON` that is
    `ENDROUTE_TURN` rather than `O.SELL_TURNS[-1]`. A Python int of a Python
    int, like `drop_turns`, so it folds at trace time on both backends.
    """
    return ENDROUTE_TURN + 1 - (O.ROUTE_BASE if h <= MO else O.ROUTE_BASE_WIDE)


def _prestock_ok(xp, day):
    """bool: is there a tomorrow worth stocking for [PRESTOCK, LAW 0.4]?

    `terminal` is `day > O.LAST_SHED_DAY`, so tomorrow is terminal from day
    `O.LAST_SHED_DAY` on -- and a terminal day buys nothing, plants nothing and
    liquidates the shed. Written off the same constant `terminal` reads rather
    than off `VAL.pay_day()`: this is "does day d+1 still shop", which is the
    season's last day and not the last day whose work monetizes, so
    `HORIZON_DROP_ON` must not move it.
    """
    return xp.asarray(day).astype(xp.int32) < O.LAST_SHED_DAY


def _buy_row_units(xp, d: "Prefix"):
    """int: units the day's own turn-1 BUY row still asks for [PRESTOCK].

    `_market` emits an order only where the quantity is positive, so the row is
    empty exactly when this is zero -- and an empty row is what lets the crew
    start at `O.ROUTE_BASE_PRE`. Seeds count even though nothing PICKUPs them:
    a seed bought at turn 1 is credited after that turn's unit phase, so a unit
    that PLANTs at turn 1 would plant nothing.
    """
    i32 = xp.int32
    return (d.wheat_buy + d.fert_bought + xp.sum(d.a_buy, dtype=i32)
            + xp.sum(d.seed_buy, dtype=i32)).astype(i32)


def _buy_row_orders(xp, d: "Prefix"):
    """int: market *orders* the day's turn-1 BUY row presents [MARKET_PACK].

    `_market` emits an order per slot whose quantity is positive and
    `render.market_actions` drops the rest, so this is the length the queue
    actually reaches the engine with -- and `_process_market` truncates that
    queue at `maxMarketOrdersPerTurn` per turn, which is what decides whether
    the row can share turn 0 with the hires.

    Orders and not units, unlike `_buy_row_units`: one BUY_PRODUCT slot buys a
    whole quantity in one order, and it is slots the cap counts.
    """
    i32 = xp.int32
    return ((d.wheat_buy > 0).astype(i32) + (d.fert_bought > 0).astype(i32)
            + xp.sum((d.a_buy > 0).astype(i32), dtype=i32)
            + xp.sum((d.seed_buy > 0).astype(i32), dtype=i32)).astype(i32)


def route_turns(h: int) -> int:
    """Turns each of a crew of `h` hands plus the farmer has for its route.

    A crew past `MAX_MARKET_ORDERS` cannot be hired in one turn's market queue
    and needs the turn-2 HIRE row, which starts *every* unit at
    `O.ROUTE_BASE_WIDE` rather than `O.ROUTE_BASE` (`core/ops.py` explains why
    the late base has to apply to the whole crew and not only the late hires).
    So the eleventh hand does not just cost its own fib price, it costs the ten
    already hired a turn each -- and 1.5's enumeration is where that is paid,
    which is why this is a function of the candidate rather than a constant.

    A Python int of a Python int: every caller indexes it with an unrolled
    loop variable, so it folds at trace time on both backends.

    `PRESTOCK_ON` shifts both bases down a turn on a day whose residual BUY row
    is empty (`O.ROUTE_BASE_PRE` / `ROUTE_BASE_WIDE_PRE`); the enumeration adds
    that turn itself, since the emptiness is a traced scalar and this is a
    Python constant per unrolled candidate.
    """
    return TPD - (O.ROUTE_BASE if h <= MO else O.ROUTE_BASE_WIDE)


# The BUY row's slot groups. The engine commits market orders slot by slot and
# `_market` lays them out in this order; the budget hands out at most what the
# purse holds, so the sequence only decides who is served first, never who gets
# the money (see `_market`).
B_WHEAT, B_FERT, B_SEEDS, B_ANIMAL = 0, 1, 2, 3

#: BUY-row slot layout, fixed. Both seats present the same op in the same slot
#: on every market turn, which is what `sim/market.py::assert_no_cross` stands
#: on, so this is a constant and not a decision.
#:
#: Land is not in it [M2]. It rides the spare tenth slot of `O.SELL_TURNS[0]`,
#: after that turn's nine sells, which is the only place in the day where a
#: purchase can be funded by the morning's own revenue -- and leaving this row
#: is also what gives the mixed herd its three animal slots.
DEFAULT_ORDER = (B_WHEAT, B_FERT, B_SEEDS, B_ANIMAL)

#: Slots each category occupies. One wheat, one fertilizer, one per crop, one
#: per animal kind -- `1 + 1 + 5 + 3` is exactly the engine's ten.
BUY_ROW_WIDTH = {B_WHEAT: 1, B_FERT: 1, B_SEEDS: spec.N_CROPS,
                 B_ANIMAL: spec.N_ANIMALS}


def buy_row_slot(cat: int) -> int:
    """First slot of a BUY-row category under `DEFAULT_ORDER`.

    Read by `_market` and by `OPEN_PUMP_ON`'s `assert_no_cross` exemption, so
    the one place that knows the layout is the layout itself.
    """
    s = 0
    for c in DEFAULT_ORDER:
        if c == cat:
            return s
        s += BUY_ROW_WIDTH[c]
    raise KeyError(cat)


# ---- SELL_SLOT_PRIORITY: the index of a SELL is a contested resource --------
#
# The engine quotes each unit of BOTH seats' same-index orders against the same
# pre-commit inventory and commits both, moving the shared inventory one unit
# per seat per round (`sim/market.py`'s module docstring, transcribed from
# `_process_market` / `_commit_unit`). A SELL therefore earns strictly more at
# a lower index: every unit that clears ahead of it -- ours OR the rival's --
# has already pushed the shelf up and the quote down. `render.market_actions`
# and `sim.rollout.compact_orders` both drop a `MO_NONE` slot, so what the
# engine receives is the LIVE orders in slot order and the nine product slots
# of a SELL row are a free permutation: no new order, no new turn, no unit of
# volume moved. That is the whole cost of this switch.
#
# It is the one mechanism of `docs/strategy/2026-09-16-v45-notebook.md` sect.4
# we lack outright (its sect.3 row 3). Their layer ranks a contiguous block of
# distinct-item sells by *how much revenue the rival could take away* rather
# than by headline value, and bubbles sells ahead of buys. Re-derived here in
# our own arithmetic against our own projection (their file is Apache-2.0 and
# nothing is copied from it -- sect.3.1 of that doc):
#
#     batch[p] = clip(rival's visible ripe yield of p, MIN, MAX)
#     score[p] = sum_{j < q[p]} price(p, inv[p] + j) - price(p, inv[p] + batch[p] + j)
#
# i.e. the coins our own `q[p]` units lose if the rival's harvest lands in the
# pot first. A product with a flat curve at this inventory, or one the rival
# does not grow, scores low and goes to the back; a steep, contested one goes
# to slot 0. `inv` is `sell.lot_inventories`'s own projection for THAT lot's
# turn, so each row is ranked against the shelf it will actually meet.
#
# Two halves, both default-ON under the one switch:
#   (a) sells ahead of non-sells on the merged BUY row (`EARLY_SELL` mode "A"
#       puts lot 1 behind the day's purchases), and only where legal -- the
#       block stops at a BUY of the SAME item, which for our fixed layout means
#       a day that buys wheat and sells wheat, or buys fertilizer and sells
#       fertilizer, keeps the shipped order. `OPEN_PUMP` owns turn 1 on its own
#       day and is never re-ordered.
#   (b) the rank above, applied to every contiguous distinct-item SELL block:
#       the three lot rows and lot 1's block inside the merged row.
#
# Switched OFF, `prio` is `None`, `_market` emits the rows it always emitted
# and `DayView.opp_ripe` is never read -- pinned whole-plan-digest-identical to
# the pre-switch tree in `tests/test_slotprio.py`, which is still one
# `SELL_SLOT_PRIORITY_ON = False` away.
#
# 2026-09-16 -- SHIPS ON, on top of `LOT4_ON` at turn 17
# (`docs/strategy/2026-09-16-combo2.md`). Standalone the arm was REJECTED by 56
# coins (+394, t +6.29, `2026-09-16-slotprio.md`); measured as an INCREMENT on
# the shipped `lot4t17` tree it clears the same bar on its own -- POOLED180
# **+459 on 169 boards, se 63, t +7.31**, 8 row flips for and 0 against (4/0
# boards) -- sect.115b PASS. The pair against B is +1,250 (t +12.92, 24/0 rows,
# board win 71.6 -> 78.7 %), the largest sect.115b read any arm has posted: the
# two levers do not overlap (sum of the solo reads +1,185) because LOT4 makes
# the row bigger and this makes it better ordered. Both purses move the right
# way in every leg (ours +244, theirs -215 on the increment), and nothing is
# negative anywhere (ENG22 +762, V45LEG +1,197 for the pair).
#: [SWITCH] Rank a SELL row's slots by the revenue a rival could take away.
SELL_SLOT_PRIORITY_ON = True
#: Half (a): sells ahead of the day's purchases on the merged BUY row.
SELL_SLOT_PRIORITY_SELLS_FIRST_ON = True
#: Batch floor -- what we assume a rival can put into the pot ahead of us even
#: when we can see no ripe yield of that product on its board. Their layer uses
#: 8 and so does this one: below that the score collapses to the headline
#: marginal and the rank stops being about contention at all.
SELL_SLOT_PRIORITY_BATCH_MIN = 8
#: Batch ceiling. A rival with 60 ripe melons still only gets one turn's worth
#: of orders into the same slot round, and an uncapped batch walks the whole
#: price curve into the floor, where every product scores alike.
SELL_SLOT_PRIORITY_BATCH_MAX = 24
#: Length of the per-unit walk the score sums over. One SELL order moves at
#: most `SHED_CAPACITY` units (`sim/state.MAX_UNITS_PER_ORDER`), so this is the
#: whole order and not a truncation.
_SLOT_PRIO_K = spec.SHED_CAPACITY + 1


# ---- RIVAL_TELL: the batch, MEASURED instead of guessed ---------------------
#
# `SELL_SLOT_PRIORITY` prices contestedness from `opp_ripe` -- what the rival
# *could* put in the pot, standing on its board. What it *did* put in the pot is
# readable from the public market inventory alone, one turn behind, and exactly:
# `agent/tell.py` re-derives the engine identity
#
#     riv_net(t) = inv[t+1] - inv[t] + town(t) - our_sell(t) + our_buy(t)
#
# (precision 1.000 / recall 0.976 on 50 real games, `2026-09-16-rivaltell.md`
# sect.3). ON, the batch term becomes the rival's measured sale rate for that
# item, and the proxy is kept only where the measurement does not fire:
#
#     batch[p] = clip(rate[p] if gated else opp_ripe[p], BATCH_MIN, BATCH_MAX)
#
# The gate is `RIVAL_TELL_MIN_TURNS` of the last `RIVAL_TELL_WINDOW` turns with
# a credited sale of that item. WHEAT and FERTILIZER are excluded outright: the
# estimator is a NET, and those two are the only items a rival trades both ways
# in one turn, carrying 100 % of its misses (ibid. sect.4). The state is the
# runtime's, one `int32[9]` ring per seat rotated per turn beside the
# `OPEN_PUMP_TELL_KEEP0` patch hook (`agent/runtime.py`), and the simulator has
# no per-turn pot history to rotate, so a sim seat keeps the proxy throughout.
#
# OFF -- and on any view built without one -- `opp_rate` is the all-`-1`
# sentinel, `sell_slot_scores` is called with `opp_rate=None` and emits the
# expression it always emitted: pinned digest-identical in
# `tests/test_rivaltell.py`.
#: [SWITCH] Replace the slot-priority batch proxy with the measured sale rate.
#: Requires `SELL_SLOT_PRIORITY_ON`; alone it changes nothing.
RIVAL_TELL_ON = False
#: Turns of history the rate is averaged over.
RIVAL_TELL_WINDOW = 6
#: Turns of that window the rival must have sold the item on for the gate to
#: fire. Their own clone layer gates at 4 of 6; 2 of 6 is where the recall of
#: the estimator is still 0.99.
RIVAL_TELL_MIN_TURNS = 2
#: Items the gate never fires on -- the net cannot split their two legs.
RIVAL_TELL_SKIP = (spec.I_WHEAT, spec.I_FERT)
#: Parity knob: hold the measurement at the sentinel, so an armed seat keeps
#: every other code path and plans exactly `SELL_SLOT_PRIORITY_ON`'s plan.
RIVAL_TELL_FORCE_PROXY = False


def sell_slot_scores(xp, price_table, inv_lots, lots, opp_ripe,
                     opp_rate=None):
    """int[n_lots, 9]: coins each row's own units lose to a rival batch.

    `inv_lots` is `sell.lot_inventories`'s projection (one row per lot, the
    shelf that lot's turn meets), `lots` the allocation, `opp_ripe` the other
    seat's standing ripe yield. Non-negative by construction: the price table
    is non-increasing in inventory, so `now - later >= 0` per unit, and a row
    with no units scores zero.

    `opp_rate` is `RIVAL_TELL_ON`'s measured sale rate, `-1` per item where the
    tell did not fire; `None` -- the switch off, and every caller before it --
    emits not one extra instruction and keeps the proxy everywhere.
    """
    i32 = xp.int32
    q = lots.astype(i32)[:, :, None]                       # [L, 9, 1]
    inv = inv_lots.astype(i32)[:, :, None]
    seen = opp_ripe.astype(i32)
    if opp_rate is not None:                       # [SWITCH, RIVAL_TELL]
        rate = opp_rate.astype(i32)
        seen = xp.where(rate >= 0, rate, seen).astype(i32)
    batch = xp.clip(seen,
                    SELL_SLOT_PRIORITY_BATCH_MIN,
                    SELL_SLOT_PRIORITY_BATCH_MAX)[None, :, None]
    j = xp.arange(_SLOT_PRIO_K, dtype=i32)[None, None, :]
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :, None]

    def at(pos):
        return price_table[pid, xp.clip(pos - spec.PRICE_TABLE_LO,
                                        0, spec.PRICE_TABLE_N - 1)]

    gap = (at(inv + j) - at(inv + batch + j)).astype(i32)
    return xp.sum(xp.where(j < q, gap, 0), axis=2, dtype=i32).astype(i32)


def sell_slot_perm(xp, lot, score):
    """int[9]: the product order one SELL row presents, best slot first.

    Live products first, by `score` descending, ties to the lower product
    index; the empty slots keep product order behind them. Every key is
    distinct by construction, so numpy's unstable `argsort` and JAX's stable
    one return the same permutation -- which the OFF/ON digest pin and the
    engine legs both depend on.
    """
    i32 = xp.int32
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)
    n = spec.N_PRODUCTS
    key = xp.where(lot.astype(i32) > 0,
                   score.astype(i32) * (2 * n) + (n - 1 - pid),
                   -1 - pid).astype(i32)
    return xp.argsort(-key).astype(i32)


def sell_slot_exempt(turn):
    """bool[MO]: the slots half (a) is allowed to cross the other seat on.

    Sells ahead of the purchases means our SELL can meet a self-play twin's
    `BUY_PRODUCT` at the same index on the merged BUY row -- the same cross
    `OPEN_PUMP` makes on purpose, and the one `sim/market._inventory_orders`
    resolves explicitly above the price floor. Off the switch, and on every
    other turn, this is the all-false mask `assert_no_cross` always had.
    """
    mask = np.zeros(MO, bool)
    if SELL_SLOT_PRIORITY_ON and SELL_SLOT_PRIORITY_SELLS_FIRST_ON \
            and EARLY_SELL_ON and turn == O.EARLY_SELL_LOT1_TURN:
        mask[:] = True
    return mask


# ---- SELL_SLOT_RIVALRANK: the rival's MEASURED burst re-ranks the row -------
#
# `SELL_SLOT_PRIORITY` ranks a SELL row by the coins our own units lose if a
# batch of `clip(opp_ripe, 8, 24)` rival units reaches the pot first -- a read
# of what the other seat COULD sell. `agent/tell.py` knows what it DID sell,
# exactly (`docs/strategy/2026-09-16-rivaltell-arm.md` sect.2: precision 1.000
# over 50 real games), and that doc's own closing line says what the next user
# of it has to read: a BURST -- the largest single-turn row of the window --
# and not the per-turn mean, because the mean of a bursty seller is always
# under the clamp's floor and the clamp swallowed it (that arm is dead, and its
# batch term is untouched here).
#
# Why the burst is the right quantity: our row's slot index only decides who
# reaches the shared inventory first WITHIN one slot round of one turn, and a
# rival puts at most ONE turn's orders into that round. So the units that can
# actually get ahead of ours on item `p` are the units the rival sells on its
# biggest turn, `burst[p]` -- not its daily total and not its standing harvest.
#
# Positions are a bijection: a product moved forward moves another back, so the
# only question a ranking answers is which item a slot is worth more to. This
# adds one term to that key, in the same coins as the proxy it corrects,
#
#     rank[p] = sum_{j < q[p]} price(p, inv[p] + j) - price(p, inv[p] + burst[p] + j)
#
# and the switch is
#
#     score[p] = sell_slot_scores[p] + SIGN * SELL_SLOT_RIVALRANK_W * rank[p]
#
# with SIGN chosen by the instrument and not by argument (`S/rivalrank/`):
# `+1` FRONT-RUNS the item the rival is dumping (the measured contention is
# real and the proxy under-prices it), `-1` YIELDS it (the dumped item's shelf
# is already deep, its curve is flat there, and an early slot buys more on an
# item whose price is still intact). The two readings are opposite and both
# are arguable from the shelf alone, which is exactly why the sign is measured:
# `S/rivalrank/instrument.py` prices one slot of priority for the fired items
# against the same-item price of the unfired ones on real engine dawns.
#
# `opp_burst` is all-zero on every view built without the switch -- a zero
# burst gives `at(inv) - at(inv) == 0` for every unit, so the term vanishes
# identically and `prio` is `sell_slot_scores`' own score. Off, the function is
# not called at all and `DayView.opp_burst` is never read.
#: [SWITCH] Re-rank the SELL row with the rival's measured single-turn burst.
SELL_SLOT_RIVALRANK_ON = False
#: `+1` front-run the dumped item, `-1` yield it. Set from the instrument.
SELL_SLOT_RIVALRANK_SIGN = 1
#: Integer weight of the measured term against the proxy score. 1 = the two
#: reads are in the same coins and are simply added.
SELL_SLOT_RIVALRANK_W = 1
#: Turns of the window that must carry a credited sale before an item's burst
#: is believed. 1 = any sale at all; the rate arm needed 2 of 6 because a mean
#: over a window is only meaningful with more than one sample, a MAX is not.
SELL_SLOT_RIVALRANK_MIN_TURNS = 1


def sell_slot_rivalrank(xp, price_table, inv_lots, lots, opp_burst, score):
    """int[n_lots, 9]: `score` corrected by the rival's measured burst.

    `score` is `sell_slot_scores`' proxy read, `opp_burst` the measured
    single-turn maximum per product (zero where the tell did not fire). The
    correction is the same `now - later` walk as the proxy with the measured
    burst in place of the clamped batch, added with `SELL_SLOT_RIVALRANK_SIGN`.

    The result is shifted so every LIVE slot scores non-negative -- a uniform
    per-row shift, so the order `sell_slot_perm` reads is untouched, and the
    empty slots keep their negative keys and stay behind the live block.
    """
    i32 = xp.int32
    q = lots.astype(i32)[:, :, None]                       # [L, 9, 1]
    inv = inv_lots.astype(i32)[:, :, None]
    burst = xp.clip(opp_burst.astype(i32), 0, None)[None, :, None]
    j = xp.arange(_SLOT_PRIO_K, dtype=i32)[None, None, :]
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :, None]

    def at(pos):
        return price_table[pid, xp.clip(pos - spec.PRICE_TABLE_LO,
                                        0, spec.PRICE_TABLE_N - 1)]

    gap = (at(inv + j) - at(inv + burst + j)).astype(i32)
    rank = xp.sum(xp.where(j < q, gap, 0), axis=2, dtype=i32).astype(i32)
    out = (score.astype(i32)
           + i32(SELL_SLOT_RIVALRANK_SIGN * SELL_SLOT_RIVALRANK_W) * rank)
    live = lots.astype(i32) > 0
    lo = xp.min(xp.where(live, out, i32(0)), axis=1, keepdims=True)
    return (out - xp.minimum(lo, i32(0))).astype(i32)


# ---- SELL_SLOT_MIRROR: score the row against a clone of ourselves ----------
#
# `SELL_SLOT_PRIORITY` ranks a SELL row by a PROXY -- the coins our units lose
# if a batch of `clip(opp_ripe, 8, 24)` rival units lands in the pot first --
# and `2026-09-16-slotprio.md` sect.5 measured that proxy's batch window FLAT
# (+/-2x moves the read by at most 33 coins and never up), so the missing coins
# are in the rival model, not in the clamp.
#
# This is the other rival model, and on this ladder it is the true one: the
# band is a population of clones of one public notebook, so the row standing
# against ours is OUR OWN ROW. Model it that way and the slot question stops
# being a ranking and becomes an exact, finite optimisation -- the rival's
# default-order row is fixed, ours is a free permutation, and `sim/market.py`'s
# transcription of `_process_market` / `_commit_unit` says exactly what each
# permutation pays:
#
#   * our product `p` at a slot BEFORE the rival's copy of it -- solo walk,
#     revenue `sum_{j<q} price(inv + j)`;
#   * at the SAME slot -- the coupled walk `M_SELL_PAIR`, both seats quoted at
#     the same inventory and the shelf moving two units a round,
#     `sum_{j<q} price(inv + 2j)`;
#   * AFTER it -- the rival's `q` units have already walked the shelf (only the
#     rounds priced above `PRICE_FLOOR` advance inventory, `market.sell_walk`),
#     so `sum_{j<q} price(inv + adv + j)`.
#
# Each of the nine products appears at most once in a row, so no two slots of
# one row touch the same item and the three cases above are the WHOLE coupling:
# the revenue of a permutation is a sum of nine independent per-product terms,
# each read out of a [9, 3] table computed once per row. The permutation search
# is then free, and it is a real trade rather than a sort -- positions are a
# bijection, so every product pushed ahead of its clone pushes another behind
# its own (`sum_p (ours_p - theirs_p) = 0`), and the identity permutation (the
# row we emit today, every product coupled) is its own baseline.
#
# Bounded 2-swap hill climb, `SELL_SLOT_MIRROR_ROUNDS` rounds of all 36 slot
# pairs, strict improvement only -- so the search can never score below the
# identity row under its own model, and a round that finds nothing leaves the
# row where it is (the fixed loop count is therefore the same answer as early
# stopping, which is what keeps this jittable). Swaps are confined to the live
# block: `sell_slot_perm` puts live products in the first `n_live` slots by
# construction, so a swap that parks a live product behind a dead one would
# score a row the plan cannot emit.
#
# ON, this REPLACES `sell_slot_scores` as the source of `prio`. Everything else
# of `SELL_SLOT_PRIORITY` -- which rows are ranked, half (a)'s sells-ahead-of-
# purchases block move, the turns, the quantities, the `assert_no_cross`
# exemption -- is untouched, and the switch is not read at all unless
# `SELL_SLOT_PRIORITY_ON` is on. `docs/strategy/2026-09-16-slotmirror.md`.
#: [SWITCH] Order the SELL row by an exact lockstep replay against a mirror of
#: our own row, instead of `sell_slot_scores`' `now - later` ranking.
SELL_SLOT_MIRROR_ON = False
#: Hill-climb rounds. Nine slots is 36 pairs a round; the climb is over a
#: bijection of at most nine items and empties long before this.
SELL_SLOT_MIRROR_ROUNDS = 10
#: Length of the per-unit walk. One SELL moves at most `SHED_CAPACITY` units
#: (`sim/state.MAX_UNITS_PER_ORDER`), so this is the whole order.
_SLOT_MIRROR_K = spec.SHED_CAPACITY + 1
#: The 36 slot pairs, Python-time constants (the layout is not a decision).
_SLOT_MIRROR_SI = np.array([i for i in range(spec.N_PRODUCTS)
                            for _j in range(i + 1, spec.N_PRODUCTS)], np.int32)
_SLOT_MIRROR_SJ = np.array([_j for i in range(spec.N_PRODUCTS)
                            for _j in range(i + 1, spec.N_PRODUCTS)], np.int32)

# ---- SELL_SLOT_MIRROR_GATE: reorder only where the model applies -----------
#
# `SELL_SLOT_PRIORITY` fires on every SELL row of every day. Its solo leg lost
# by 56 coins (+394 against the +450 bar) while its INCREMENT on `lot4t17`
# passed at +459, and `2026-09-16-slotprio.md` sect.3 shows the coins are not
# spread evenly at all: +993 on the ten big-round-trip clone boards, +194 on
# V42-V44, +152 on the two V45 boards. 25-40 % of the band is not a clone of
# anything we model, and a reorder priced against a rival that does not exist
# is a free way to lose the slot we already had.
#
# The gate is the cheap half of that: fire the reorder only where the rival's
# board LOOKS like the one our scorer assumes, and only while the game is still
# contested.
#
#   similarity = sum_p min(ours_p / |ours|, theirs_p / |theirs|)
#
# -- the histogram intersection of our own sell row against `view.opp_ripe`,
# the rival read `SELL_SLOT_PRIORITY` already takes, in integer arithmetic
# (`inter * 100 >= PCT * |ours| * |theirs|`). It is 1.0 for a seat growing our
# mix in our proportions and 0 for a seat sharing no product with us; an empty
# rival board scores 0, which is the right answer here and NOT the batch floor
# `sell_slot_scores` falls back to -- a rival with nothing ripe cannot take the
# slot away from anyone.
#
# The money veto is the second half: a seat already ahead by
# `SELL_SLOT_MIRROR_GATE_LEAD` is not fighting for the shelf, and the shipped
# row is the one every other switch was measured on.
#
# OFF, neither term is computed and `view.opp_money` is never read. ON, a
# vetoed day's `prio` is all-zero, which is `sell_slot_perm`'s identity -- live
# products in product order, dead behind them, i.e. the row the plan emitted
# before `SELL_SLOT_PRIORITY` (identical after the `MO_NONE` compaction
# `render.market_actions` and `sim.rollout.compact_orders` both do). Half (a)
# is not a scorer and is item-blind, so it is NOT gated.
#: [SWITCH] Fire the slot reorder only on a clone-similar, still-contested day.
SELL_SLOT_MIRROR_GATE_ON = False
#: Histogram-intersection floor, in percent, between our sell row and the
#: rival's standing ripe yield.
SELL_SLOT_MIRROR_GATE_SIM_PCT = 25
#: Money lead at which the reorder stops firing: ahead by this much, take the
#: shipped row.
SELL_SLOT_MIRROR_GATE_LEAD = 5000


def sell_slot_mirror_revenues(xp, price_table, inv_lots, lots):
    """int[n_lots, 9, 3]: our revenue for a product sold EARLY / COUPLED /
    LATE against a mirror of our own row.

    Column 0 is the solo walk `price(inv + j)`, column 1 the coupled walk
    `price(inv + 2j)` (`sim/market._quotes`' `M_SELL_PAIR`), column 2 the walk
    behind the rival's own `q` units, whose inventory advance counts only the
    rounds priced above `spec.PRICE_FLOOR` (`sim/market.sell_walk`). A product
    with no units in the row scores zero in all three.
    """
    i32 = xp.int32
    q = lots.astype(i32)[:, :, None]                       # [L, 9, 1]
    inv = inv_lots.astype(i32)[:, :, None]
    j = xp.arange(_SLOT_MIRROR_K, dtype=i32)[None, None, :]
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :, None]

    def at(pos):
        return price_table[pid, xp.clip(pos - spec.PRICE_TABLE_LO,
                                        0, spec.PRICE_TABLE_N - 1)]

    mine = j < q
    early = at(inv + j)
    paired = at(inv + 2 * j)
    adv = xp.sum(xp.where(mine & (early > spec.PRICE_FLOOR), 1, 0),
                 axis=2, dtype=i32)[:, :, None]
    late = at(inv + adv + j)
    cols = [xp.sum(xp.where(mine, c, 0), axis=2, dtype=i32)
            for c in (early, paired, late)]
    return xp.stack(cols, axis=-1).astype(i32)


def _mirror_total(xp, rev, theirs, ours):
    """int[...]: the row's revenue under our slots `ours` against the rival's
    fixed slots `theirs`. `rev` is `sell_slot_mirror_revenues`, broadcast to
    the same leading shape; the last axis of all three is the nine products."""
    i32 = xp.int32
    case = xp.where(ours < theirs, 0, xp.where(ours > theirs, 2, 1)).astype(i32)
    k = xp.arange(3, dtype=i32)
    got = xp.sum(xp.where(k == case[..., None], rev, 0), axis=-1, dtype=i32)
    return xp.sum(got, axis=-1, dtype=i32)


def sell_slot_mirror_scores(xp, price_table, inv_lots, lots):
    """int[n_lots, 9]: `sell_slot_perm`-compatible scores whose descending
    order IS the hill climb's permutation.

    The search runs on slot positions; the score handed back is `8 - slot`, so
    `sell_slot_perm`'s `argsort` reproduces it exactly (the positions of the
    live products are distinct by construction, so no tie is ever broken).
    """
    i32 = xp.int32
    n = spec.N_PRODUCTS
    rev = sell_slot_mirror_revenues(xp, price_table, inv_lots, lots)
    live = lots.astype(i32) > 0
    lv = live.astype(i32)
    dead = 1 - lv
    n_live = xp.sum(lv, axis=1, dtype=i32)[:, None]
    # The rival's row is ours in default order: live products in product order,
    # dead behind them -- which is what `sell_slot_perm` emits on a zero score.
    theirs = xp.where(live,
                      xp.cumsum(lv, axis=1) - lv,
                      n_live + xp.cumsum(dead, axis=1) - dead).astype(i32)
    ours = theirs
    si = xp.asarray(_SLOT_MIRROR_SI)[None, :, None]        # [1, 36, 1]
    sj = xp.asarray(_SLOT_MIRROR_SJ)[None, :, None]
    # A swap is legal only inside the live block (see the block comment).
    legal = ((si[:, :, 0] < n_live) & (sj[:, :, 0] < n_live))
    rev_s = rev[:, None, :, :]
    th_s = theirs[:, None, :]
    for _round in range(SELL_SLOT_MIRROR_ROUNDS):
        base = _mirror_total(xp, rev, theirs, ours)        # [L]
        cur = ours[:, None, :]
        cand = xp.where(cur == si, sj, xp.where(cur == sj, si, cur)).astype(i32)
        val = _mirror_total(xp, rev_s, th_s, cand)         # [L, 36]
        val = xp.where(legal, val, base[:, None] - 1)
        best = xp.argmax(val, axis=1)
        hit = (xp.arange(val.shape[1], dtype=i32)[None, :] == best[:, None])
        pick = xp.sum(xp.where(hit[:, :, None], cand, 0), axis=1, dtype=i32)
        take = xp.sum(xp.where(hit, val, 0), axis=1, dtype=i32) > base
        ours = xp.where(take[:, None], pick, ours).astype(i32)
    return (n - 1 - ours).astype(i32)


def sell_slot_gate(xp, lots, opp_ripe, money, opp_money):
    """bool: whether the day's SELL rows may be re-ordered at all
    [SWITCH, SELL_SLOT_MIRROR_GATE].

    Clone-similar (histogram intersection of our own row against the rival's
    standing ripe yield, at least `SELL_SLOT_MIRROR_GATE_SIM_PCT`) AND not
    already ahead by `SELL_SLOT_MIRROR_GATE_LEAD`. Traced, never branched: both
    terms are traced ints.
    """
    i32 = xp.int32
    ours = xp.sum(lots.astype(i32), axis=0, dtype=i32)
    theirs = opp_ripe.astype(i32)
    a = xp.sum(ours, dtype=i32)
    b = xp.sum(theirs, dtype=i32)
    inter = xp.sum(xp.minimum(ours * b, theirs * a), dtype=i32)
    sim = (a > 0) & (b > 0) & (inter * 100 >= SELL_SLOT_MIRROR_GATE_SIM_PCT * a * b)
    lead = (xp.asarray(money).astype(i32)
            - xp.asarray(opp_money).astype(i32)) < SELL_SLOT_MIRROR_GATE_LEAD
    return sim & lead


def land_reach(xp, n_units, worked_pre):
    """int: how many of a fresh quadrant's `LAND_TILES` tiles the day's own
    labour can develop, and so how many of its candidates the valuation may
    count [HEURISTIC, 1.3].

    Tiles the day cannot reach are worth nothing today. A fresh tile's chain is
    PLANT+WATER or BUILD+PLACE -- two ops, which the admit stage charges at
    `n_ops + EST_MOVES` turns -- and the turns available for it are the crew's,
    less what the board the farm already owns has spoken for. `DEV_DAYS` is the
    one place a multi-day view enters: a quadrant bought this morning is worked
    for the rest of the season, not only today, and charging it today's spare
    turns alone would make every purchase look like a labour overrun.

    `n_units` is recovered from the caller's own hire bill (`HIRE_BILLS` is
    strictly increasing), so pass A -- which prices the day on a zero bill --
    values land at one unit. That under-counts, and an under-count can only
    refuse, never over-buy.

    It reads `EST_MOVES` and deliberately not `EST_LEAD`: the shed walk is a
    per-unit-day charge on *today's* labour, and `DEV_DAYS` already says a
    quadrant bought this morning is worked for the rest of the season rather
    than only today, so charging the walk here would double-count the very
    thing that makes a fresh quadrant worth buying. `EST_MOVES` going 2 -> 1
    with the one-crossing route does reprice a quadrant upward, which is the
    same correction the admit stage got and not a separate decision.
    """
    i32 = xp.int32
    turns_free = xp.maximum(
        xp.asarray(n_units).astype(i32) * (TPD - O.ROUTE_BASE - LAND_PICKUPS)
        - xp.asarray(worked_pre).astype(i32) * (1 + EST_MOVES), 0)
    return xp.clip((turns_free // (2 + EST_MOVES)) * DEV_DAYS, 0, LAND_TILES).astype(i32)


def _serpentine() -> np.ndarray:
    """Row-major but alternating direction, so consecutive tiles are adjacent."""
    order = []
    for y in range(spec.BOARD):
        xs = range(spec.BOARD) if y % 2 == 0 else range(spec.BOARD - 1, -1, -1)
        order.extend(y * spec.BOARD + x for x in xs)
    return np.array(order, dtype=np.int32)


SERP = _serpentine()                            # SERP[k] = tile id visited k-th
SERP_INV = np.argsort(SERP).astype(np.int32)    # tile id -> sweep position
SERP_X = spec.TILE_X[SERP].astype(np.int32)
SERP_Y = spec.TILE_Y[SERP].astype(np.int32)
#: Quadrant of each sweep position, so the tiles a purchase unlocks can be
#: named in the planner's own serpentine tile space. `spec.TILE_QUAD` is in raw
#: tile order and is what `brain` reads, whose `PolicyObs.kind` is raw.
SERP_QUAD = spec.TILE_QUAD[SERP].astype(np.int32)

#: Manhattan turns from the nearest shed-access tile to each sweep position.
#: The crew respawns on those four tiles every morning (the engine clears
#: `farm["hands"]` at every end of day), so this is what a tile costs the day
#: that first develops it -- and, through the 12-17 tile-days of watering and
#: harvesting that follow, what it keeps costing. `_rank_near` orders the
#: day's free slots by it when the `compact` gene asks.
DIST_SHED = np.min(
    np.abs(SERP_X[:, None] - spec.SHED_ACCESS_XY[None, :, 0])
    + np.abs(SERP_Y[:, None] - spec.SHED_ACCESS_XY[None, :, 1]), axis=1).astype(np.int32)
DIST_SHED.setflags(write=False)
#: Largest reachable `DIST_SHED`, and so the bucket count `_rank_near` unrolls
#: and the ceiling `brain` decodes `compact` against.
DIST_MAX = int(DIST_SHED.max())

# ---- ROUTE_EFF: a floor under the day's `compact` gene [SWITCH, OFF] -------
# ROUTEEFF (`docs/strategy/2026-09-16-routeeff.md`) measured the per-hand-day
# STEP ledger of both seats.  Every unit step is MOVE / PASS / PROD -- market
# orders are a separate action channel (`kaggriculture.py:555-612`) and cost no
# unit step -- so per unit-day  prod = present - move - pass  EXACTLY, and the
# d20-29 ops-per-hand-day gap decomposes into seven additive terms.  Its
# largest on ENG22 is `mid_move`, the walk BETWEEN the first and last
# productive op of a unit-day: we spend 8.93 move-steps a unit-day to their
# 8.19 (t 6.05) while touching the SAME number of distinct tiles (5.05 vs
# 5.03) that are LESS spread out than theirs (mean pairwise Manhattan 2.37 vs
# 2.62).  Our route is blobby and dear; theirs is path-like and cheap.
#
# `_dev_key`'s docstring names the cause: `compact` is `relu(tanh(dev[0]))`
# (`brain.py:1208`), one-sided and 0 at zero theta, and at `compact == 0`
# `_rank_near` is `_rank` bit for bit -- the day develops in plain serpentine
# order, which "scatters the season's whole labour over the board" (:8090),
# and the 12-17 tile-days of watering and harvesting that follow inherit that
# scatter.  This switch puts a FLOOR under that gene, so development is ranked
# by `DIST_SHED` and the crew's whole season walks a tighter set.  It is a
# constant, not a new mechanism: `ROUTE_EFF_COMPACT == 0` is the shipped plan
# byte for byte, and the gene may always ask for MORE compaction than the
# floor.
ROUTE_EFF_ON = False
#: The floor, in `compact` units (0 .. `DIST_MAX`).  `DIST_MAX` is full
#: compaction -- the tiles nearest a shed access are developed first.
ROUTE_EFF_COMPACT = DIST_MAX

#: The shed-access tile each sweep position walks home to for a DROP -- the walks home to for a DROP -- the
#: `argmin` of the same distance, ties to the lowest access index. Only the
#: coordinates matter: any of the four is shed-adjacent, so the nearest one is
#: strictly the cheapest return leg (PLANNER_V3_1 section 4).
_NEAR_SLOT = np.argmin(
    np.abs(SERP_X[:, None] - spec.SHED_ACCESS_XY[None, :, 0])
    + np.abs(SERP_Y[:, None] - spec.SHED_ACCESS_XY[None, :, 1]), axis=1)
NEAR_X = spec.SHED_ACCESS_XY[_NEAR_SLOT, 0].astype(np.int32)
NEAR_Y = spec.SHED_ACCESS_XY[_NEAR_SLOT, 1].astype(np.int32)
NEAR_X.setflags(write=False)
NEAR_Y.setflags(write=False)

# Unit u's spawn tile. The farmer sits on shed-access tile 0; `_spawn_hand` picks
# the least-occupied shed-access tile with NWSE tie-breaking, which for hires
# made back-to-back -- turn 0's row and then turn 2's -- lands hand h on tile
# (h+1) % 4. "Back-to-back" is the load-bearing word and is why the whole crew
# waits for the last hire turn (`O.ROUTE_BASE_WIDE`): one unit that has walked
# off its spawn tile changes the occupancy every later hire is measured
# against, and this table stops describing where hands land.
SPAWN_SLOT = np.array([u % 4 for u in range(MU)], dtype=np.int32)
SPAWN_X = spec.SHED_ACCESS_XY[SPAWN_SLOT, 0].astype(np.int32)
SPAWN_Y = spec.SHED_ACCESS_XY[SPAWN_SLOT, 1].astype(np.int32)

#: Route-load sentinel: a turn count no block can reach, so a tile past the
#: cut is never selected by `_count_le`. The planner's shared coin ceiling
#: (`spec.COIN_CAP`) doubles as it -- one constant, and far above TPD.
_BIG = np.int32(spec.COIN_CAP)

#: Sentinel that must outrank every packed `(marginal price, product)` key of
#: the forced sale, so a *drained* product is never picked over a stocked one.
#: `_BIG` is far too small for that: the price table tops out at 1,053,252, so
#: `marg * N_PRODUCTS + pid` reaches 9.5e6 -- nine times `_BIG` -- for any
#: product whose market inventory has fallen under 4,887, and the argmin would
#: then buy an empty product, force-sell nothing and let the shed destroy the
#: overflow. Town demand alone never digs that deep: a shop eats at most 2
#: units of one product a tick, 6 ticks a day, and the eighth and last shop
#: only unlocks on day 24, so a whole episode removes under 1,700 units of the
#: 10,000 the market starts with. The sentinel is sized against the *table*
#: rather than against a plausible inventory anyway: 1<<30 clears the real
#: maximum by a factor of 113 and still leaves the key inside int32.
_DRAINED = np.int32(1 << 30)

#: Score of a hire count the purse cannot pay [1.5]. Every reachable gain is a
#: sum of at most 100 tile values, each clipped under 1 << 20, so 1 << 27 is
#: the ceiling and this sits an order of magnitude below it -- still well
#: inside int32, which a plain -inf substitute would not be.
_UNAFFORDABLE = np.int32(-(1 << 30))


#: "every gene switch at the value its module constant ships with" -- the
#: vector a zero `sw`/`swb` block decodes to, and the default for every Macro
#: built by hand. Read-only and shared on purpose: `_sw_macro` tells a rewritten
#: Macro from an untouched one by *identity*, and nothing here ever writes a
#: decoded field.
SWITCH_DEFAULT = np.zeros(PO.N_SWITCH_GENES, np.int32)
SWITCH_DEFAULT.setflags(write=False)


class Macro(NamedTuple):
    """What the policy decides once per day. Integer, already clipped.

    Input purchases are absent on purpose -- the executor derives those.
    """
    plant_target: object    # int[5]  new plantings wanted today, per crop
    animal_want: object     # int[3]  animals to acquire today, per kind (free structures first)
    land_bias: object       # int     signed coins the gene adds to a quadrant's computed value
    hold: object            # int[9]  reservation value: coins one unit is worth kept until tomorrow
    press: object           # int[9]  opponent timing pressure: coins a unit loses per lot of delay
    grow_mult: object       # int[9]  value multiplier on new plantings/animals, GROW_ONE = x1
    compact: object         # int     0..DIST_MAX: how tightly the day develops around the shed
    dev_weight: object      # int     labour weight on development, GROW_ONE = x1
    hire_bias: object       # int     coins per hand the gene adds to 1.5's enumerated gain
    crew_target: object     # int     hands the ramp asks the day for [g10]
    animal_defer: object    # int     0..DEFER_ONE: how hard animals wait for the crew [g10]
    forward_days: object    # int     0..FWD_DAYS_MAX: days 1.5's hire scan projects [g11]
    #: int 0..FERT_DEFER_MAX: days the fertilizer site looks ahead [g12]. Zero
    #: (the default, for callers that build a Macro by hand) is the shipped plan.
    fert_defer: object = np.int32(0)
    #: int[N_SWITCH_GENES] or None: 1 where the day wants `SWITCH_GENES[i]`
    #: at the opposite of its module value [sw/swb]. `None` is every theta
    #: written before the block, and every caller that builds a Macro by
    #: hand -- both mean "the module constants rule", which is what the
    #: planner did before gene switches existed, and it is what
    #: `SWITCH_DEFAULT` -- this field's default -- says.
    switches: object = SWITCH_DEFAULT


class Prefix(NamedTuple):
    """Everything a day's plan needs that does not depend on how many hands
    are hired -- computed once per candidate hire bill [1.5]. The bill itself
    is the one channel the hire count has into it: it is deducted from the
    purse the purchase walk spends."""
    task: object            # bool[100]  tiles carrying at least one queued op
    n_ops: object           # int[100]   ops queued on each tile
    chain_op: object        # int[100, CHAIN_MAX]
    chain_a: object         # int[100, CHAIN_MAX]
    chain_q: object         # int[100, CHAIN_MAX]
    tile_value: object      # int[100]   what the tile's chain is worth [1.6]
    tier: object            # int[100]   the mandatory flag [LAW, 0.5]
    want_feed: object       # bool[100]  the three pickup masks
    want_fert: object       # bool[100]
    m_place: object         # bool[100]
    place_kind: object      # int[100]   which animal kind each placement takes
    wheat_buy: object       # int        the day's purchases, already granted
    fert_bought: object     # int
    seed_buy: object        # int[5]
    a_buy: object           # int[3]
    buy_land: object        # int        0/1
    rev1: object            # int        discounted lot-1 revenue the land grant counted on
    n_fert_eff: object      # int        applications the shed can supply
    purchase_shortfall: object  # int    coins the greedy wanted and could not grant [7]
    purse_left: object      # int        coins the day's greedy left in the purse [PRESTOCK]
    relay: object = None    # bool[100]  [WHEATMIX1/ESWORK1] today's relay plantings (None = off)


class DayStats(NamedTuple):
    """The planner's three operational metrics for one day [section 7].

    Diagnostics, not decisions: `build_day` computes them from locals it
    already holds and drops them, `build_day_stats` returns them instead of
    the plan. int32 scalars, like everything else the planner counts.
    """
    overflow_destroyed: object   # int  units end-of-day destroys after the forced sale
    purchase_shortfall: object   # int  coins of wanted candidates the greedy did not grant
    value_dropped: object        # int  coins of queued task value today's route does not do


#: [SWITCH] Hire only the hands the day's route actually loads.
#:
#: The crew size `1.5`'s enumeration picks is an *intent*: `n_hire` sets
#: `n_units`, `wide`, `route_base`, the bill and reserve `_derive` spends
#: against, `turn_budget`, `land_lead` and the admit stage's labour, and
#: `_routes` then cuts the day's ranks across that many units. The cut
#: routinely runs out of ranks before it runs out of units -- 17.06 hand-days
#: a game under `flow58_g450` are hands whose whole route `_routes` emitted as
#: PASS (`S/allday_idle/report.md`, 960 exactly re-planned day-rows; the cause
#: is `start >= n_tasks` on 100 % of them, never an unreachable first tile).
#: They are bought by `macro.hire_bias * h` and `CREW_TARGET_PUSH` continuing
#: to climb after the work term `n_adm` has gone flat, plus a ~28 % model-vs-
#: route gap in the pooled turn estimate.
#:
#: ON, the HIRE market row alone is clamped to the hands that carry a route.
#: Nothing else moves -- and that decoupling is the point. `HIRE_CLAMP_ON`
#: (retired) clamped the *intent*, at the saturation of `n_adm` over pass A's
#: pre-purchase board, so on 2.38 day-rows a game it hired **fewer** hands than
#: `_routes` could load and destroyed 4.31 productive hand-days a game on
#: exactly the ramp days d5/d8/d9/d10: -3,203 a game. Clamping the row instead
#: cannot do that, because the count is read *off the finished route*.
#:
#: An inactive unit is inactive for free: `active` gates `working`, `blk`, the
#: pickup rows and both tail cursors (`f_can`), and an active unit always emits
#: at least its `base >= 1` opening op, so "route is all PASS" is exactly
#: "`_routes` gave this unit nothing" and needs nothing new out of `_routes`.
#: `crew_now` (:2177) therefore still reads the crew the plan intends, and the
#: g10 animal deferral is byte-identical -- which matters for a future theta,
#: `macro.animal_defer` being 0 in all 960 rows under `flow58_g450`.
#:
#: The count is taken as *the smallest prefix of hands that holds every acting
#: one* rather than a bare population count, because the rendered plan is
#: sliced by the engine's real hand count (`render.turn_action`): unit `u`'s
#: route belongs to hand `u`, so a hand that acts must be inside the row. In
#: the 960 measured rows the idle hands are always the trailing indices and the
#: two agree; the prefix form is the guard for the case they do not (`active`
#: also carries `load[s] <= bud`, which spawn distance makes per-unit).
#:
#: Off those 960 rows it takes 256.4 hires a game to 239.3, idle hand-days
#: 17.06 to 0.00 exactly, and +889 coins of hire bill, with no turn given up --
#: the hands did nothing. The real engine does not pay it: 768 paired games,
#: two seed bases x four panel opponents, come to -378 a game (se 506,
#: t -0.75, win 61.5 -> 61.2 %), and +889 is outside that interval. The saved
#: coins re-enter the next day's purse and the season re-plans around them, so
#: ON is a different trajectory and not the same one minus a bill. Hence OFF,
#: and pinned on the invariant rather than a t-test
#: (`tests/test_hire_row.py`, `S/hire_row/report.md`). OFF is byte-identical.
HIRE_ROW_ON = True

# ---- FORWARD_ADMIT: price the crew against the work that is coming ----------
#
#: Hire enumeration scores every candidate `h` against *today's* derived task
#: set (:1.5), and a field whose crops are all outside their bonus window emits
#: no task at all: `spec.CROP_WINDOW_START[I_MELON]` is 6, so the twelve melon
#: tiles of the recorded top-tier opening (`MELON_OPEN_ON`) are silent for the
#: first six days. The argmax then reads an empty board, hires nobody, and the
#: farm wakes on day 7 with one hand against the opponent's eight -- measured
#: at band6 win 94 % -> 26 % when the opening is forced onto our planner
#: (`S/forced/arms.csv`), with the day-1 crew at 0-1 hands against the top
#: field's 4 and the herd frozen at 4 animals while theirs doubles by day 8.
#:
#: ON, the enumeration -- and only the enumeration -- is handed a second,
#: *projected* prefix: `_derive(forward=True)` widens the bonus-water window
#: and the one-time harvest age by `FORWARD_ADMIT_DAYS`, so a planted tile that
#: will emit a WATER or a HARVEST within the horizon carries that op now, at
#: today's estimated turns and today's price. Nothing else moves: pass B, the
#: route, the admission and the market row all read the unwidened `_derive`, so
#: the day still walks exactly the work it has. What changes is the *count* of
#: hands the day is willing to buy for the work it is about to have.
#:
#: The planner carries no day discount (`dev_weight` scales development against
#: today's turns, not against a horizon), so the projected ops are valued flat.
#:
#: OFF -- and at `FORWARD_ADMIT_DAYS <= 0`, which skips the second `_derive`
#: outright -- the enumeration reads `d0` exactly as it always did, so every
#: shipped theta decodes byte for byte (`tests/test_forward_admit.py`).
#:
#: **This knob is a manual override, not the strategy.** Measured as a fixed
#: switch it loses -- band6, 72 paired boards, flow135_g350: win 94.4 -> 65.3 %,
#: -9,224 coins a game -- because a theta's `hire_bias` and crew ramp are
#: priced for today-only admission and a wider window double-counts them. The
#: horizon that ships is `macro.forward_days`, the `g11` gene, which the ES
#: moves *with* the rest of the head (`tests/test_forward_gene.py`).
#:
#: Precedence, and it is one line of code: ON, `FORWARD_ADMIT_DAYS` is the
#: horizon and the gene is ignored, which is what makes the A/B above
#: repeatable against any theta. OFF -- the default -- the gene rules.
FORWARD_ADMIT_ON = False

#: How far ahead the projected prefix looks, in days, **when the override above
#: is ON**. A tile is admitted to the hire score when `age + FORWARD_ADMIT_DAYS`
#: reaches its window start (or its harvest age), i.e. when the op lands within
#: the next N days. 0 is OFF. Dead weight while `FORWARD_ADMIT_ON` is False;
#: the gene carries its own horizon.
FORWARD_ADMIT_DAYS = 3

#: [SWITCH] Drop `macro.hire_bias` out of 1.5's enumeration -- the *other* half
#: of a forward horizon, and the reason the hand override above loses.
#:
#: `FORWARD_ADMIT_ON` was measured as an ADD: the horizon widens the work the
#: argmax sees while the trained tilt that was fitted to a today-only scan is
#: still on the gain line, so the board pays for the same crew twice (HELD42
#: -8,676, `docs/strategy/2026-09-10-forward-admit.md`; the quiet-tile,
#: discounted shape still read -2,628). The two channels are the same claim in
#: different coordinates: `hire_bias` is a constant coins-per-hand tilt the ES
#: fitted *because* the day could not see tomorrow's melon, and the horizon is
#: that same "hire earlier" said explicitly.
#:
#: ON, the tilt is zero and the horizon is the only thing arguing for the hand,
#: so the switch is a REPLACE rather than an ADD. It is meant to be set WITH
#: `FORWARD_ADMIT_ON`; alone it is a pure ablation of the gene.
#:
#: `crew_target` (`g10`, the ramp) is deliberately left alone -- it is a
#: different shape (a target, not a tilt) and zeroing it too would ablate two
#: genes at once and say nothing about which one double-counted.
#:
#: OFF -- the default -- the gene rules and every shipped theta decodes byte
#: for byte (`tests/test_fwdhire.py`).
HIRE_BIAS_ZERO_ON = False


def _static_horizon(x):
    """`x` as a Python int if it is a concrete value, else `None`.

    The projected pass is worth building only when the horizon is nonzero, and
    "is it nonzero" is a question about a *value* -- which under `jax.jit` is a
    tracer nothing may branch on. So: on the numpy path (`agent/runtime`, the
    submission, every numpy test) the answer is known and the day skips the
    pass it does not need; under a trace it is not, and the pass is built with
    the traced horizon. Both compute the same plan, because a zero horizon
    widens nothing -- `age + 0 >= window` is `age >= window` in integers -- so
    the two paths differ in cost and never in outcome
    (`test_forward_gene.py::test_numpy_and_a_trace_agree_at_a_zero_horizon`).
    """
    try:
        return int(x)
    except TypeError:                       # a tracer, under jit or vmap
        return None


#: HIRE_BILLS[h] = what hiring h hands in one day costs, so 1.5's enumeration
#: reads a candidate's whole fib bill with a static index. MAX_HANDS + 2 long:
#: `HIRE_COST` prices MAX_HANDS + 1 hires, so the last entry is a count the
#: planner never emits and nothing indexes.
HIRE_BILLS = np.concatenate([[0], np.cumsum(spec.HIRE_COST)]).astype(np.int32)


def cash_reserve(xp, n_hire, day):
    """int: coins today holds back from its purchases for tomorrow's crew.

    `HIRE_BILLS[n_hire + 1]`: enough to re-field the crew this day's own
    enumeration chose, plus the marginal fib price of one more hand. Two
    properties are what make it the right floor rather than an arbitrary
    margin:

    * It is **structural**. Nothing here is learned -- it reads the engine's
      own fib table at the count the day already decided [1.5], so it costs no
      gene and cannot be tuned into uselessness. A day that hires nobody still
      keeps `HIRE_BILLS[1]`, which is the single coin that stops a zero-hand
      day from being self-perpetuating.
    * It is **paid for by tomorrow, not today**. The bill is per day and
      `hires_today` resets nightly, so holding back one day's bill is the whole
      guarantee: today's sale lands at turns 3/10/18, well before tomorrow's
      hire row, so the reserve is what tomorrow can hire on even if the sale
      fetches nothing at all.

    Void from `VAL.pay_day()` on: the last payable day has no tomorrow to
    hire for, so a coin held past it is a coin thrown away. Without
    `HORIZON_DROP_ON` that is day 28 -- day 29 hires nobody by law [0.4]; with
    it day 29 hires again through the DROP module's enumeration, and every
    `HIRE_TURNS` row resolves before `SELL_TURNS[0]`, so day 29's crew is paid
    out of coins day 28 carried overnight.

    `n_hire` is the count, not the bill, so the caller cannot pass an index
    that has already been through `HIRE_BILLS`.
    """
    i32 = xp.int32
    idx = xp.clip(xp.asarray(n_hire).astype(i32) + 1, 0, spec.MAX_HANDS)
    bill = xp.asarray(HIRE_BILLS)[idx]
    return xp.where(xp.asarray(day).astype(i32) < VAL.pay_day(), bill, 0).astype(i32)


# ---- H2: a floor under the fertilizer reservation [SWITCH, default OFF] ----
#
# Fertilizer is the one market with a whole-season town drain of exactly zero
# (`brain.expected_drain`: 0 units), so every unit either seat sells sits in
# that market for the rest of the game and lowers every later quote. Its curve
# is `linear` at `above_target = 0.40` over `T = 200`, i.e. 0.2 coins per unit
# above I0, and both seats between them push it 435-468 units above I0 -- the
# quote floors at 6 coins in the games we lose and 13 in the games we win
# (2026-08-30 profile, t = +5.06). Measured over 192 real-engine games we book
# 205 units for 11,234 coins, **54.7 coins against a base of 100**, and
# `corr(sellrev_FERTILIZER, margin) = -0.003`: the channel is a pure wash.
#
# The gate is a *reservation*, not a new decision: `sell.allocate` already
# sells a unit only when its adjusted marginal clears `hold`, so raising the
# fertilizer entry of `hold` stops the sale exactly where the quote stops
# paying. Everything downstream follows for free -- unsold fertilizer stays in
# the shed, so `_derive`'s `fert_avail = shed + bought` rises and `n_fert_eff`
# spreads it on our own tiles, which is the direction the wins already take
# (`op_FERTILIZE` 169 in wins against 158 in losses, `buyprod_FERTILIZER` 4.5
# against 2.2) -- and the shed-overflow forced sale stays the safety valve, so
# a held unit is never a destroyed one.
#
# The floor is read off the *price table*, not off `spec.DEFAULT_MARKET_PARAMS`:
# `market_price` returns exactly `base` at `inventory == I0` for any params, so
# `price_table[I_FERT, I0 - PRICE_TABLE_LO]` is this game's own base even under
# the training randomisation (`spec.sample_market_params`).
#
# MEASURED 2026-08-30, and the hypothesis is WRONG -- the switch stays OFF.
# 96 seeds x 2 seats against kagg2 (`--seed-base 20260828`), paired with the
# champion on (seed, seat):
#
#     floor        win %   mean margin   paired diff        t   cand-only wins
#     champion      78.1        +9,013            --       --        --
#     base / 2      62.0        +4,123        -4,890   -13.01    0 (31 lost)
#     base / 5      77.6        +7,786        -1,227    -7.11    0  (1 lost)
#
# Monotone in the floor and negative at every setting, with **zero** games won
# that the champion lost at either. The profile's "pure wash" reading was of
# the *correlation*, and a correlation of zero across seeds is not a marginal
# value of zero within one: those 11,234 coins are real revenue, the held
# fertilizer does not buy back its price in yield (`n_fert_want` is bounded by
# the plant tiles that want it, not by the shed), and holding it eats the
# 100-unit shed that wheat, feed and animals also need -- so the overflow
# forced sale dumps it at the same quote a day later, minus the room.
#
#: OFF ships the champion's decode byte for byte -- `_sell_hold` returns its
#: argument unchanged and no array is touched. Kept, switched off, because the
#: measurement above is the answer to a hypothesis that will be asked again.
FERT_FLOOR_ON = False
#: The floor as a fraction of fertilizer's base quote, in integers so both
#: backends agree. 1/2 of base = 50 coins, a little under the 54.7 we realise.
FERT_FLOOR_NUM = 1
FERT_FLOOR_DEN = 2


# ---- FERT_RESERVE: the sale draws on the surplus over the REMAINING plan's
#      fertilizer demand, not over today's [SWITCH, OFF]
#
# MECHANISM, read off the public V45 agent's `_r85_fertilizer` layer
# (`docs/strategy/2026-09-16-v45-notebook.md` sect.2.7, mechanics only -- their
# number is a backward walk of their own frozen tape, ours is re-derived here
# from the board): fertilizer is not an ordinary product, it is an INPUT the
# plan will need again on the days ahead. Their sale holds a reserve against
# the applications still to come and sells only what is over it; ours reserves
# exactly `n_fert_eff` -- TODAY's applications -- and hands the rest to the lot
# greedy (`fert_reserved`, sect."what the sale may draw on").
#
# THE RECURRENCE. Over the days `day+1 .. day+FERT_RESERVE_DAYS`, walked
# BACKWARDS so a shortfall on a later day is carried onto the earlier ones:
#
#     R(last+1) = 0
#     R(k)      = max(demand(k) - supply(k) + R(k+1), 0)
#
# `demand(k)` is the applications the plan's own crop/day decisions will want on
# day k: a standing plant tile whose fertilizer coverage has lapsed by k, on the
# three-day cycle the engine's `fertilized_until_day = day + 2` sets
# (`kaggriculture.py:480`), and still standing on k (one-time crops to
# `t_day + harvest_age`, ongoing crops to `pay_day`). Tiles the day is already
# fertilizing carry `day + 2`; every other tile carries its own `t_fert`.
# `supply(k)` is the fertilizer the days ahead produce for free: the engine
# re-arms EVERY animal tile's `fertilizer_available` at every end of day
# (`kaggriculture.py:831`), so a herd of `n` animals yields `n` units a day and
# `FERT_RESERVE_SUPPLY_NUM/DEN` discounts that for the collections the crew has
# no turn for.
#
# `R(day+1)` is then added to `n_fert_eff` at the one site that decides what the
# lots may draw on, so the greedy sells the SURPLUS above the reserve.
#
# WHAT THE INSTRUMENT SAYS BEFORE THE ENGINE IS ASKED (`S/fertreserve/probe.py`,
# 5 ENG22 boards, our seat, the shipped pair, `2026-09-16-fertreserve.md`):
# the seat COLLECTS 401 units a game off the herd, wants 183 applications, sells
# 218 units and buys 8; 913 of 917 applications find their unit-held unit and 4
# do not. So `supply` runs at 2.2x `demand` all season, and this reserve is
# expected to bind on almost no day -- which is the point of measuring it with
# the supply term and then again with `FERT_RESERVE_SUPPLY_NUM = 0`, the
# literal V45 form, which reserves against demand alone.
#
#: OFF nothing below is built and `fert_reserved` is the expression it always
#: was, so every incumbent checkpoint decodes byte for byte.
FERT_RESERVE_ON = False
#: How far ahead the recurrence walks. 3 = fertilizer's own coverage window
#: (`day, day+1, day+2`), i.e. exactly one cycle of the tiles standing today.
FERT_RESERVE_DAYS = 3
#: The share of the herd's daily free unit the recurrence counts as supply,
#: in integers so both backends agree. 1/1 = the whole herd produces and the
#: crew collects it; 0/1 = the V45 form, demand against stock alone.
FERT_RESERVE_SUPPLY_NUM = 1
FERT_RESERVE_SUPPLY_DEN = 1


# ---- CARROT_EARLY_HOLD: the early carrot lot is sold under base [SWITCH, OFF]
#
# MECHANISM (`docs/strategy/2026-09-16-tomato15.md` sect.2, measured on the
# ENG22/NEXTHIGH/TOPB2 ledgers `S/eng22/raw_B.npz` + `S/melon_decomp/raw_B.npz`,
# tool `S/tomato15/mech.py`, B = flow193_g100_hr with the four shipped `hr`
# switches). B sells CARROT in two blocks and they are priced 18-24 coins a
# unit apart, on every opponent class:
#
#     set             d0-9 units @ px      d15-29 units @ px
#     ENG22             26 @ 33.5             84 @ 51.8
#     NEXTHIGH          26 @ 33.2             96 @ 53.2
#     TOPB2-clone       25 @ 33.0             90 @ 56.9
#     TOPB2-engine      26 @ 33.3             67 @ 51.5
#
# CARROT is `first_yield_day 2`, so the d0-9 block is the opening rotation
# banking its first harvests into a market that has not moved yet: 33.5 is
# *under* the 35 base, while the town's carrot sinks (PET_CAFE, FARMERS_MARKET)
# drain the pool all season and carry the quote to 49-50 by d25. The engine
# class plants its whole carrot programme at d14.7 and sells 117 units at 50.1;
# ours starts on d1 in 100 % of games (`mech.py`, "day of first tile").
#
# WHY A RESERVATION AND NOT A TILE RULE. The carrot *tile count* is closed
# twice and both times the loss was labour, not ground: `CARROT_SINK_ON`
# (2026-09-07 12:40Z, PER=20 band6 51.6 -> 27.8 %, t -25; PER=3 -1,608) and the
# season-rotation arm (2026-09-06 20:20Z, -947 t -3.19, "the rotation displaces
# no crop and the seed clip never bites; the loss is LABOUR"). The verdict line
# that closed them left exactly one residue open -- *"Tile count closed; carrot
# sell-timing still open"* (`docs/strategy/2026-09-09-verdicts.txt:499`) -- and
# this is that residue and nothing else: no tile, no seed, no crew and no mix
# moves, so the displacement that killed both tile arms has no surface here.
#
# THE KNOWN RISK, stated before the measurement. (i) The 100-unit shed is a
# TOTAL cap and `TOMATO_HOLD` died on it (2026-09-05 18:34Z, band6 54.2 ->
# 47.9 %, t -10.3: "any hold push wool/milk/strawberry out at overflow
# prices"); 26 carrot units is a quarter of that cap held from d2 to d15.
# (ii) The d0-9 purse is the tightest in the game (`2026-09-14-macro-extract.md`
# sect.2: the top five hold 350-1,355 coins at dawn d5/d10 on purpose) and this
# withholds ~870 coins of it. Both are reasons the arm can lose; neither is a
# reason not to read it.
#
# OFF BY DEFAULT, AND WHY -- the arm is measured and it LOSES, hard, on every
# set (`docs/strategy/2026-09-16-tomato15.md` sect.5.2; paired CRN, both seats,
# action-replay opponent seat, `S/tomato15/launch.sh`):
#
#     leg           our coins d        margin d          their coins d   flips
#     44 ENG22           -3,297   -10,515 (t -10.4)             +7,218      10
#     68 band            -5,165   -13,174 (t -15.7)             +8,008      25
#     40 TOPB2           -4,671   -11,757                       +7,086       9
#     28 LIVE-C          -5,871   -15,198  (win 57.1 -> 0.0 %)  +9,326      16
#
# Both predeclared risks fired and they compound:
#
#   1. THE SHED WAS ALREADY FULL. B's peak shed is 99.0-99.3 of the engine's
#      100-unit TOTAL cap before the switch; 26 held carrot units take it to
#      99.8-99.9 and evict 103-138 units of everything else (MILK -25..-30,
#      FERTILIZER -30..-34, WOOL -18..-20, WHEAT -16..-22, EGG -7..-20). This
#      is `TOMATO_HOLD`'s 2026-09-05 failure on a different product.
#   2. THE EVICTED UNITS ARE HANDED OVER. Their coins go +7,218/+8,008 --
#      MILK +3,480, STRAWBERRY +1,845, WOOL +1,181, FERTILIZER +506 -- the
#      denial-handed-back signature that closed the wool and herd families.
#   3. AND THE TRANSFER ITSELF IS A WASH. The 876 coins withheld from d0-9 come
#      back as +443 in d10-14 and +153 in d15-29 while the late carrot price
#      falls 51.8 -> 49.1, so the whole carrot line moves -280 on ENG22. The
#      ledger ceiling of +476 was a price we could not have kept
#      [counterfactuals overstate].
#
# Carrot sell-timing -- the one residue `2026-09-09-verdicts.txt:499` left open
# when the two carrot tile arms closed -- is spent. Kept, switched off, because
# the measurement above is the answer to a hypothesis that will be asked again.
#
# OFF, `_sell_hold` returns its argument unchanged and no array is touched, so
# a theta trained before it decodes byte for byte (`tests/test_carrot_hold.py`,
# whole-plan digests against a pristine `git archive HEAD src` tree).
CARROT_EARLY_HOLD_ON = False

#: First day the carrot reservation is released -- the first day of the d15-29
#: band the mechanism table splits on, and the day the engine class starts its
#: own carrot programme (d14.7). Before it the floor stands; from it the sale
#: is the decode's own `hold` again.
CARROT_EARLY_HOLD_DAY = 15

#: The floor as a fraction of carrot's base quote, in integers so both backends
#: agree, read off the *price table* and not off `spec.DEFAULT_MARKET_PARAMS`
#: for the reason `FERT_FLOOR` reads it there: `market_price` returns exactly
#: `base` at `inventory == I0` for any params, so `price_table[I_CARROT, I0]`
#: is this game's own base even under the training randomisation.
#: 5/4 of base = 43 coins against a d0-9 realised 33.5 and a d15-29 realised
#: 51.8: it refuses the early block outright and never binds on the late one.
CARROT_EARLY_HOLD_NUM = 5
CARROT_EARLY_HOLD_DEN = 4


# ---- H3: the fertilizer unit's opportunity cost [SWITCH, default False] ----
#
# The fertilizer channel is a *volume* leak, and the volume goes onto our own
# tiles. Measured over four real-engine games (champion `flow58_g450` vs kagg2,
# seed base 777001, both seats), per game:
#
#                       animal-days  collected  FERTILIZE  sold  end shed
#     ours                    428.8      399.8      173.8  221.5      2.5
#     kagg2                   333.5      296.8       58.2  238.5      0.0
#
# We out-produce kagg2 by 95 animal-days and we collect 93 % of what the herd
# arms (`want_collect` reaches almost every tile; only 29 animal-days a game go
# uncollected, 11 of them on day 29 where the terminal PASS is correct). The
# shed ends empty, so nothing is held back either. The whole gap is the middle
# column: **we spread 174 units a game and kagg2 spreads 58**, and 116 units at
# our own realised 54.8 coins is 6.4k -- the live study's median FERTILIZER
# revenue gap is +7,306.
#
# What lets it happen is that the application is priced against the *spot*
# quote alone. `fert_cand` admits a tile when `fert_val > price[I_FERT]`, and
# from day 13 on the fertilizer quote is walking down its own curve (0.2 coins
# a unit, no town drain at all) while `fert_val` is a crop's marginal units at
# an un-depressed crop price -- so the test passes on almost every plant tile
# and the day spends 10-15 units on the farm instead of the market. Two things
# it does not charge for:
#
#   * The unit's own sale is the *alternative*, not the threshold. Once the
#     test passes at all, `v_fert` bids the application's **gross** value into
#     `_admit`, so a marginal application outranks the watering or harvest it
#     evicts by the whole `fert_val`, when what it actually buys over selling
#     the unit is `fert_val - price`. Same double-count `v_care` records.
#   * A FERTILIZE costs a unit-turn and drags a WATER behind it (`crop_fire`
#     waters a fertilized tile that fires tonight whether or not it is
#     thirsty); a sale costs no turns at all.
#
# ON charges both: the gate asks the application to clear `NUM/DEN` times the
# unit's quote rather than one times it, and the admit value is the *net* gain
# over selling, floored at a coin so an admitted application still ranks ahead
# of the worth-nothing group. Everything downstream is already wired to it --
# `n_fert_want` falls, so `fert_reserved` falls, so `avail[I_FERT]` rises and
# `SELL.allocate` puts the freed units in the day's lots.
#
# MEASURED 2026-09-03, and it does not clear the bar -- the switch ships OFF.
# 48 seeds x 2 seats x 4 opponents at `--seed-base 777001` (kagg2 and the three
# session_kit_20260901 tapes), paired with its own OFF leg on (seed, opponent,
# seat); the OFF leg reproduces `stack3_777001` row for row, so the baseline is
# the shipped champion exactly:
#
#     opponent          n   win OFF   win ON   paired margin      t   discordant
#     kagg2            96     88.5%    90.6%            -408  -0.41            4
#     tape 103254816   96     57.3%    60.4%            +332  +0.49           13
#     tape 104502967   96     52.1%    52.1%          +1,208  +1.51            8
#     tape 104547425   96     32.3%    40.6%            +773  +0.93           16
#     ALL             384     57.6%    60.9%            +476  +1.15           41
#
# The win rate rises 3.3 points on every opponent but one and the margin does
# not move (+476 at t 1.15; our own coins +142, theirs -334). That is the shape
# of a channel that pays a small, certain amount in every game: it flips the
# close ones and changes nothing about the wide ones.
#
# And it recovers only 15 of the 116 units, because the bar is a *multiple of a
# collapsing quote*. It bites days 12-16 (FERTILIZE 10/8/9/10.5 -> 0.5/1.5/3.5/6)
# and from day 17 the quote has fallen far enough that even two quotes is a low
# bar and 11-16 units a day still go on our own tiles.
#
# Raising the multiple does not fix that, because the thing it multiplies is
# still the collapsing quote. The same 384 games at `NUM/DEN = 4/1`:
#
#     kagg2            96     88.5%    89.6%          -1,145  -1.00           13
#     tape 103254816   96     57.3%    63.5%          +1,753  +2.38           14
#     tape 104502967   96     52.1%    52.1%            +839  +0.93           16
#     tape 104547425   96     32.3%    28.1%            +118  +0.11           16
#     ALL             384     57.6%    58.3%            +391  +0.80           59
#
# Flat against 2/1 on the margin (+391 against +476) and *worse* on the win rate
# (58.3 % against 60.9 %), with 59 discordant games against 41 -- a blunter gate
# buying more variance for the same expectation. So 2/1 is the knob this switch
# is documented at.
#
# `FERT_VOLUME_MODE` is the third cut: price the application against something
# that does *not* fall with the thing it is pricing. Same 384 games, same OFF
# reference, same 2/1 knob, 2026-09-03:
#
#     mode "base" -- the bar is 2x this game's *base* quote, all season
#     kagg2            96     88.5%    85.4%          -2,671  -2.16            7
#     tape 103254816   96     57.3%    56.2%            +571  +0.59           15
#     tape 104502967   96     52.1%    44.8%          -1,122  -1.29           15
#     tape 104547425   96     32.3%    29.2%          -1,190  -1.17           17
#     ALL             384     57.6%    53.9%          -1,103  -2.14           54
#
#     mode "marginal" -- the bar is 2x what the *next* unit would fetch
#     kagg2            96     88.5%    90.6%            -645  -0.59            4
#     tape 103254816   96     57.3%    63.5%          +1,010  +1.42           10
#     tape 104502967   96     52.1%    47.9%          +1,376  +1.68            8
#     tape 104547425   96     32.3%    42.7%            +803  +1.12           14
#     ALL             384     57.6%    61.2%            +636  +1.50           36
#
# VERDICT, and it settles the question the "recovers only 15 of 116 units" note
# above left open: the other 101 units are NOT a leak. `"base"` recovers 80 % of
# them -- 170.5 applications a game fall to 78.1, against kagg2's 58.6, and 82.8
# more units go to market for +1,557 of fertilizer revenue -- and it *loses*
# 4,503 of strawberry and 2,481 of tomato revenue doing it, for -3,525 of season
# revenue and -2,149 of end money (4 seeds x 2 seats vs kagg2). The applications
# our planner makes are buying crop yield at better than the unit's own sale
# price; the gap to kagg2 is a different crop mix, not a mispriced unit.
#
# `"marginal"` -- the honest opportunity cost, always at or below the spot, so
# the *loosest* of the three bars -- is the best of the three (+636 at t 1.50,
# win rate 57.6 -> 61.2 %, the fewest discordant games at 36) and still short of
# the +1,500 / t 2 gate. It says the same thing from the other side: the value
# left in this expression is in the admit half (`v_fert` net of the unit), not
# in fertilizing less.
#
#: OFF every expression re-evaluates to the one it replaced, so a theta trained
#: before this switch decodes byte for byte. Kept, switched off, because the
#: measurement above is the answer to a question that will be asked again.
FERT_VOLUME_ON = False
#: The bar an application must clear, as a multiple of the reference price the
#: mode below picks. Integers so both backends agree. 2/1 = the application
#: must be worth twice what the unit fetches.
FERT_VOLUME_NUM = 2
FERT_VOLUME_DEN = 1
#: *Which* price the application is charged, ON [SWITCH `FERT_VOLUME_ON`].
#: Read at trace time, so it costs nothing on the backends.
#:
#:   "spot"     the unit's own quote today, `view.price[I_FERT]`. The mode the
#:              48-game table above measured; kept as the default so ON is the
#:              behaviour that block documents.
#:   "base"     this game's *base* quote, `price_table[I_FERT, MARKET_I0]` --
#:              the same number `_sell_hold` reads under `FERT_FLOOR_ON`. The
#:              point of it: fertilizer has zero town drain, so its spot only
#:              ever walks down and a multiple of it stops binding after ~day
#:              16, while the base does not move all season.
#:   "marginal" what the next unit would actually fetch, i.e. the lot-1 quote
#:              after the units already in the shed have gone. The honest
#:              opportunity cost, and always <= spot, so it is the *lowest* of
#:              the three bars.
FERT_VOLUME_MODE = "spot"

# ---- FERT_DUMP: the unit's sale is worth more than its price [SWITCH, OFF] --
#
# The opposite sign of the fertilizer-hold family (`2026-09-16-fertreserve.md`
# section 4). FERTILIZER is the one product the town never drains
# (`kaggriculture.py:114`), so its market inventory is a pure running total of
# net sells and its quote is exactly linear in it:
#
#     price(inv) = max(1, round(100 - 0.2 * (inv - MARKET_I0)))
#
# One extra unit dumped therefore takes 0.2 coins off EVERY later fertilizer
# quote for the rest of the game -- the rival's and OURS. So a dumped unit is
# worth its own sale plus a denial term, and the denial term's SIGN is the
# difference of the two remaining schedules:
#
#     denial(day) = 0.2 * (their units sold after `day` - OUR units sold after)
#
# MEASURED, 10 real-engine boards, both schedules read off the engine
# (`S/fertdenial/`, `docs/strategy/2026-09-16-fertdenial.md`), per game:
#
#     leg           our units sold   theirs   denial at d20    their fert % purse
#     5 ENG22                218.4    211.2    -6.7 / unit                 12.3 %
#     5 V45LEG clones        199.2    397.2   +21.9 / unit                 17.3 %
#
# The fertilizer-ENGINE cluster sells no more fertilizer than we do, so against
# it dumping harder is SELF-denial; the clone sells twice what we sell, so
# against it the term is real and large. This switch prices that term and
# nothing else.
#
# ON, from `FERT_DUMP_DAY`, an application must beat the unit's quote by
# `FERT_DUMP_BONUS` coins instead of merely beating it -- the same bar
# `FERT_VOLUME` raises, raised by an ADDITIVE denial value rather than a
# multiple, because the thing being added is a count of the rival's remaining
# units and not a fraction of the collapsing quote (the multiple's defect, H3
# above: at 2/1 the bar stops binding after day 16). The freed units need no
# further plumbing -- `n_fert_want` falls, `fert_reserved` falls,
# `avail[I_FERT]` rises and `SELL.allocate` puts them in the day's lots.
#
#: OFF `fert_bar` is the expression it always was and no array is built, so
#: every incumbent checkpoint decodes byte for byte.
FERT_DUMP_ON = False
#: First day the denial bonus applies. 20 = the start of the band where our own
#: remaining sales have run out (the ENG22 self-denial term collapses from
#: -6.7 to -1.4 coins a unit between d20 and d24) while the clone still has
#: 109 units to sell. Before it, dumping mostly denies our own later lots.
FERT_DUMP_DAY = 20
#: The denial value of one dumped unit, in coins, added to the bar the
#: application must clear. 20 = the measured clone-leg denial at d20 (+21.9),
#: rounded down. 0 re-evaluates to the OFF expression at every day.
FERT_DUMP_BONUS = 20

# ---- FERT_TIMING: spend the unit on the day it buys the most [SWITCH, OFF] --
#
# An application sets `fertilized_until_day = day + 2`
# (`kaggriculture.py:481`), so it covers three end-of-days and what it buys
# depends entirely on WHEN in the tile's life it lands:
#
#   * one-time crop -- each in-window watering inside the coverage scores +2
#     instead of +1 (`kaggriculture.py:440`). WHEAT's window is ages 2..4, so
#     an application at age 2 buys 3 units and one at age 0 buys 1.
#   * ongoing crop -- each fire inside the coverage scores +2 instead of +1
#     (`kaggriculture.py:799`). STRAWBERRY fires every 2 days, so an
#     application on the EVE of a fire catches two fires (`day+1`, `day+3`)
#     and one a day earlier catches one.
#
# `fert_marginal_value` already prices all of this exactly, and `fert_rank`
# already orders by it. What the shipped site never asks is whether the SAME
# unit on the SAME tile would buy more TOMORROW. It does not, because
# `fert_cand` is a bar test (`fert_val > fert_bar`) and both the good day and
# the mediocre one clear a 37-70 coin bar. FERTENGINE measured the cost on the
# 22 ENG22 boards, both seats, real engine (`S/fertengine/`): of our 185.1
# applications a game 132.2 (71 %) land off the best day -- 44.9 wheat and 18.3
# carrot before their yield window opens, 62.4 strawberry and 6.6 tomato on a
# day with no fire to double -- against 14.5 of 170.7 (8.5 %) for the
# fertilizer-ENGINE class this file's `FERT_DUMP` note is aimed at. Same
# collection stream, 1.56 covered events per application against their 1.98.
#
# ON, an application waits while a later day inside the look-ahead is strictly
# better. Nothing downstream needs plumbing, for `FERT_DUMP`'s reason:
# `n_fert_want` falls, `fert_reserved` falls, `avail[I_FERT]` rises and
# `SELL.allocate` puts the deferred units in the day's lots -- the unit is not
# lost, it is spent a day or two later or sold.
#
#: OFF the horizon is `macro.fert_defer`, the `g12` gene, which is 0 on every
#: theta trained before the block -- and a zero horizon skips the projected
#: valuation outright, so `fert_cand` is the expression it always was.
#: `FERT_TIMING_ON` exists so the behaviour can be A/B'd against a theta that
#: has not trained the gene, exactly as `FORWARD_ADMIT_ON` does for `g11`.
FERT_TIMING_ON = True
#: Days of look-ahead the module override names, ON.
FERT_TIMING_DAYS = 2
#: Static loop bound for the projected valuation. MUST equal
#: `brain.FERT_DEFER_MAX`, which clips the gene -- `plan` cannot import `brain`
#: (`brain` imports `plan`), so the two are pinned by
#: `tests/test_fertengine.py::test_gene_cap_matches_the_plan_loop_bound`.
FERT_TIMING_MAX = 3

# ---- STRAW_SWAP1: one fixed-count fertilizer target swap [SWITCH, OFF] ----
# On days 10..24, if the budget-selected set contains wheat while an eligible
# strawberry candidate was left outside it, replace the lowest-value selected
# wheat with the highest-value unselected strawberry. Purchases and the number
# of applications are unchanged. This is deliberately a target-allocation
# ablation, not a fertilizer-volume or labour-policy change.
STRAW_SWAP1_ON = False


#: Static column of `price_table` whose entry is the quote at the opening
#: inventory, i.e. `base` for whatever market params this game drew.
_I0_COL = int(spec.MARKET_I0 - spec.PRICE_TABLE_LO)


def _lot_split(xp, lots, day):
    """int[3, 9]: `lots` with no product standing more than `LOT_SPLIT_MAX`
    units in one lot, the excess moved to the lots that have room.

    Total units per product are preserved exactly -- the caller's `s_qty` must
    not move, because the shed-overflow deficit and every downstream bulk add
    are computed off it. Spare capacity is filled earliest lot first, so a
    product the greedy already spread keeps as much of its own shape as the
    cap allows; whatever still does not fit (more than `N_LOTS *
    LOT_SPLIT_MAX` units, which only the day-29 liquidation reaches) goes on
    the LAST lot, the one the town tick has drained furthest.

    Read only under `LOT_SPLIT_ON`. `LOT_SPLIT_MAX <= 0` returns the argument
    unchanged, and an empty `LOT_SPLIT_DAYS` is every day -- both decided at
    Python time, so the traced graph off the switch is the one it always was.
    """
    i32 = xp.int32
    cap = int(LOT_SPLIT_MAX)
    lots = lots.astype(i32)
    if cap <= 0:
        return lots
    capped = xp.minimum(lots, cap).astype(i32)
    spill = xp.sum(lots - capped, axis=0, dtype=i32)
    rows = []
    for l in range(n_lots()):
        room = xp.maximum(cap - capped[l], 0).astype(i32)
        take = xp.minimum(spill, room).astype(i32)
        rows.append((capped[l] + take).astype(i32))
        spill = (spill - take).astype(i32)
    rows[-1] = (rows[-1] + spill).astype(i32)
    split = xp.stack(rows).astype(i32)
    if not LOT_SPLIT_DAYS:
        return split
    on = None
    for dd in LOT_SPLIT_DAYS:
        hit = _as(xp, day) == xp.asarray(int(dd), i32)
        on = hit if on is None else (on | hit)
    return xp.where(on, split, lots).astype(i32)


def _sell_hold(xp, price_table, hold, terminal, day=None):
    """The reservation the day's lots are greedy against [H2, CARROT_EARLY_HOLD].

    `hold` comes in already carrying the terminal law (`SELL.LIQUIDATE` on day
    29). Every floor is applied only off the terminal day, because day 29 must
    sell whatever the reservation says [LAW, 0.4].

    `day` is only read by `CARROT_EARLY_HOLD_ON`; it is a tracer under `jit`,
    so the gate is a scalar predicate applied with `where` and the plan stays
    shape-static. With both switches off the argument is returned untouched and
    no array is built, which is what pins the OFF-path digests.
    """
    if not (FERT_FLOOR_ON or CARROT_EARLY_HOLD_ON or melon_deny_on()
            or PROGRAM_ENGINE_ON or (WOOL_FIRST_ON and WOOL_FIRST_SELL)):
        return hold
    i32 = xp.int32
    j = xp.arange(spec.N_PRODUCTS, dtype=i32)
    gated = hold
    if FERT_FLOOR_ON:
        base = price_table[spec.I_FERT, _I0_COL].astype(i32)
        floor = ((base * FERT_FLOOR_NUM) // FERT_FLOOR_DEN).astype(i32)
        e_fert = (j == spec.I_FERT)
        gated = xp.where(e_fert, xp.maximum(gated, floor), gated).astype(i32)
    if CARROT_EARLY_HOLD_ON:
        base = price_table[spec.I_CARROT, _I0_COL].astype(i32)
        floor = ((base * CARROT_EARLY_HOLD_NUM) // CARROT_EARLY_HOLD_DEN).astype(i32)
        early = _as(xp, 0 if day is None else day) < xp.asarray(
            int(CARROT_EARLY_HOLD_DAY), i32)
        e_car = (j == spec.I_CARROT) & early
        gated = xp.where(e_car, xp.maximum(gated, floor), gated).astype(i32)
    if melon_deny_on():
        now = _as(xp, 0 if day is None else day)
        ripe = int(spec.CROP_SATURATE_AGE[spec.I_MELON])
        release = max(int(MELON_DENY_DUMP_DAY), ripe + int(MELON_DENY_HOLD))
        e_melon = j == spec.I_MELON
        melon_hold = xp.where(now >= xp.asarray(release, i32), 0,
                              xp.asarray(spec.COIN_CAP, i32))
        gated = xp.where(e_melon, melon_hold, gated).astype(i32)
    if PROGRAM_ENGINE_ON:
        # One compiled obligation: retain the opening crop until its primary
        # d10--12 sale window, then release without a fixed price floor.
        now = _as(xp, 0 if day is None else day)
        e_melon = j == spec.I_MELON
        in_window = (now >= xp.asarray(10, i32)) & (now <= xp.asarray(12, i32))
        before = now < xp.asarray(10, i32)
        melon_hold = xp.where(before, xp.asarray(spec.COIN_CAP, i32),
                              xp.where(in_window, 0, gated[spec.I_MELON]))
        gated = xp.where(e_melon, melon_hold, gated).astype(i32)
    if WOOL_FIRST_ON and WOOL_FIRST_SELL:
        # [WOOLFIRST1] no wool reservation: the shed's wool sells as produced.
        gated = xp.where(j == spec.I_WOOL, 0, gated).astype(i32)
    return xp.where(terminal, hold, gated).astype(i32)


def _sell_spread_cap(xp, avail, day, terminal):
    """int[N_PRODUCTS]: `avail` with the `SELL_SPREAD_ITEMS` lines capped at a
    flat per-day quota from `SELL_SPREAD_DAY0` [SWITCH `SELL_SPREAD_ON`].

    quota = max(avail[p] // days_left, SELL_SPREAD_MIN), days_left counting
    today through `SELL_SPREAD_END`.  `avail` is already net of the feed and
    fertilizer reservations, so the quota is cut on what the day could
    actually have sold, and the cap is a `minimum` -- it never hands the
    allocator a unit the shed does not hold.

    Traced-safe: `day` is a tracer under `jit`, so the window and the terminal
    exemption are `where`s on a shape-static array.  Never called with the
    switch off, so the OFF plan builds none of it.
    """
    i32 = xp.int32
    avail = avail.astype(i32)
    d = _as(xp, day).astype(i32)
    left = xp.maximum(xp.asarray(int(SELL_SPREAD_END), i32) - d + 1,
                      xp.asarray(1, i32)).astype(i32)
    quota = xp.maximum(avail // left, xp.asarray(int(SELL_SPREAD_MIN), i32))
    capped = xp.minimum(avail, quota).astype(i32)
    j = xp.arange(spec.N_PRODUCTS, dtype=i32)
    on = None
    for p in SELL_SPREAD_ITEMS:
        hit = j == xp.asarray(int(p), i32)
        on = hit if on is None else (on | hit)
    if on is None:
        return avail
    # The window, and the terminal day is the ENDROUTE family's -- left alone.
    live = ((d >= xp.asarray(int(SELL_SPREAD_DAY0), i32))
            & (_as(xp, terminal) == xp.asarray(0, i32)))
    return xp.where(on & live, capped, avail).astype(i32)


def _fert_reference(xp, view, price_table):
    """int32 scalar: the price one fertilizer unit is charged at, ON
    [SWITCH `FERT_VOLUME_ON`, mode `FERT_VOLUME_MODE`].

    The gate asks for `NUM/DEN` of this and `v_fert` bids the value net of it,
    so this one number is the whole opportunity cost the switch prices.

    `"base"` is `price_table[I_FERT, MARKET_I0]`, the quote at the opening
    inventory -- exactly what `_sell_hold` reads under `FERT_FLOOR_ON`. It is
    a constant of the game's market draw, which is the point: fertilizer is the
    one product with no town drain, so its spot only ever walks down and a
    multiple of the spot stops binding once the quote collapses.

    `"marginal"` is what the *next* unit fetches: the lot-1 quote walked down
    by the fertilizer already in the shed. APPROXIMATION, deliberate and
    labelled. The exact number would be the marginal revenue of the day's real
    allocation, which depends on `avail[I_FERT]`, which depends on
    `n_fert_want`, which is what this bar decides -- a cycle. Walking the
    lot-1 curve down by `shed[I_FERT]` breaks it with the largest queue the day
    can have (the reservation only ever shrinks what is sold), so this is a
    *lower* bound on the marginal quote and therefore a conservative bar. It
    ignores the two later lots and the opponent's orders, both of which push
    the quote further down, and the `hold` reservation, which pushes it up.
    """
    i32 = xp.int32
    if FERT_VOLUME_MODE == "base":
        return price_table[spec.I_FERT, _I0_COL].astype(i32)
    if FERT_VOLUME_MODE == "marginal":
        quotes = PJ.sell_quotes(xp, price_table, PJ.projected_inv(
            xp, view.mkt_inv, view.shops, O.SELL_TURNS[0], view.day))
        e_fert = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_FERT)
        sold = xp.where(e_fert, view.shed[:spec.N_PRODUCTS].astype(i32), 0)
        return PJ.marginal_quote(xp, quotes, sold)[spec.I_FERT].astype(i32)
    return view.price[spec.I_FERT]


def _fert_future_reserve(xp, view, fert_today):
    """int32 scalar: units of fertilizer the days ahead need and the herd does
    not make, by backward recurrence [SWITCH `FERT_RESERVE_ON`].

    `fert_today` is the bool[100] mask of tiles this day is fertilizing -- their
    coverage runs to `day + 2` and the rest keep their own `t_fert`. Callers
    that run BEFORE the day's applications are decided must pass an all-false
    mask: the reserve is then at its largest, which is what keeps a provisional
    lot-1 revenue a lower bound on the real one.

    Never called with the switch off, so the OFF plan builds none of it.
    """
    i32 = xp.int32
    day = _as(xp, view.day).astype(i32)
    kind, occ = view.kind, view.occ
    is_plant = kind == spec.KIND_PLANT
    crop = xp.clip(occ, 0, spec.N_CROPS - 1)
    has_animal = ((kind == spec.KIND_COOP) | (kind == spec.KIND_PASTURE)) & (occ >= 0)
    c_ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    c_first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    c_sat = xp.asarray(spec.CROP_SATURATE_AGE)[crop]
    pay = xp.asarray(int(VAL.pay_day()), i32)
    # The last day this tile is still worth an application: a one-time crop is
    # harvested at `t_day + harvest_age`, an ongoing one runs to `pay_day`.
    harvest_age = xp.clip(pay - view.t_day, c_first, c_sat)
    last = xp.where(c_ongoing == 1, pay,
                    xp.minimum(view.t_day + harvest_age, pay)).astype(i32)
    # Coverage end after today: `day + 2` where the day fertilizes, else the
    # standing `fertilized_until_day`.
    cover = xp.where(fert_today, day + 2, view.t_fert.astype(i32)).astype(i32)
    # The herd's free unit a day (engine re-arms every animal every dawn),
    # discounted for the collections the crew has no turn for.
    herd = xp.sum(has_animal.astype(i32), dtype=i32)
    supply = ((herd * int(FERT_RESERVE_SUPPLY_NUM))
              // max(int(FERT_RESERVE_SUPPLY_DEN), 1)).astype(i32)
    # A tile's next application is the first day its coverage has lapsed -- but
    # never before tomorrow, because today's is already counted in `n_fert_eff`
    # -- and then every third day, fertilizer's own window. Anchoring on
    # `cover + 1` alone would put a never-fertilized tile (`t_fert = -1`) on a
    # cycle counted from day 0 rather than from the day it is actually free.
    anchor = xp.maximum(cover + 1, day + 1).astype(i32)
    res = xp.zeros((), i32)
    for j in range(int(FERT_RESERVE_DAYS), 0, -1):
        k = (day + j).astype(i32)
        lapsed = k - anchor
        want = (is_plant & (lapsed >= 0) & (lapsed % 3 == 0) & (k <= last))
        demand = xp.sum(want.astype(i32), dtype=i32)
        res = xp.maximum(demand - supply + res, 0).astype(i32)
    return res

# `REPLANT_SAME_TURN_ON` [SWITCH]: keep the ROTATION whole -- a tile a harvest
# frees today is replanted today, with the crop it just carried, in the same
# chain the harvest is in.
#
# MEASURED FIRST (REPLANT, 2026-09-18, `S/replant/trace.py` on the gated engine
# boards under ESR + FT2's theta, both seats): the *latency* hypothesis is
# FALSE. `free_slot = is_empty | is_weed | harvest_one` (above) and
# `brain.n_free_slots` already count the day's ripe one-time crops, so the
# replant the planner does emit is in the harvest's own chain, one hour behind
# it -- REPLANT-SCOPE (2026-09-14) measured that gap as exactly 1 h on 95 of
# 95. What the trace *does* find is that of 146.5 harvest-frees a season only
# 55.8 % are replanted at all that day (theirs 80.3 %), 35 % are never
# replanted, and the reason is on one line: our seed shed is EMPTY at every
# dawn of the season (`seed_dawn` 0.0-0.5, `seed_left` 0.0, `planted ==
# seed_bought` day for day) while theirs banks 15-32 seeds from d14 on. The
# planting is capped by `plant_eff = min(plant_target, seeds + seed_buy)` and
# `macro.plant_target = floor(dev_frac * n_free) - animals` is a FRACTION of
# the free pool -- so the tile the farmer is standing on loses its own seed to
# the day's development ration.
#
# The arm is therefore a FLOOR on the seed want, not a new tile and not a new
# crop: for every tile a harvest frees inside the window the day may buy back
# that crop's seed out of the coins its own grant did not want (the second
# `budget.grant` `PLANT_FILL` established, seed lists only, funded from the
# leftover), and the extra seeds are planted ONLY on those freed tiles, with
# the crop they just carried.
#
# What it deliberately does not do, because both are closed families:
#   * it never plants an empty or weeded tile -- `PLANT_FILL_LATE` is the arm
#     that does that and it is HARD REJECT -3,917 t -7.60, at 1.5 ops per
#     added tile, because each of those tiles needs a route of its own. A
#     replant costs ONE op (plus its watering) on a tile the route already
#     walks to for the harvest;
#   * it never moves the crop mix -- the replant crop is `crop`, the tile's own
#     outgoing crop, so `macro.plant_target`'s softmax split is untouched
#     (CROPMIX / PRICEAWARE are closed).
#
# The known hazard, and why the window is a knob: `PLANT_FILL`'s v1 autopsy is
# that a tile planted today is not free tomorrow, so `n_free` falls and
# `n_dev`, `animal_count` and every future placement fall with it -- the idle
# tiles are the herd's build reserve. A replant is milder than a fill (the tile
# was not free yesterday either; the rotation is simply not broken) but it is
# the same channel, so the cell is judged with a day floor.
#
# OFF: `rp_here` is never constructed, no second grant runs, `plant_eff`,
# `plant_crop` and the chain are the OFF program's, object for object -- the
# candidate list is built from `plant_here`/`plant_crop` themselves, not from a
# `| zeros` of them [LAW].
REPLANT_SAME_TURN_ON = False
#: First day a harvest may be replanted under the switch.
REPLANT_FROM_DAY = 0
#: Last day. A replant after `VAL.pay_day()` cannot mature, and `can_mature`
#: already zeroes the gene's want there; this is the switch's own clamp.
REPLANT_TO_DAY = 24


# The three DayView defaults below are singletons shared, by identity, with
# every view that omits them, and `default_price_table`'s cache is shared with
# every `build_day` that passes no table. All four are read-only, so an
# accidental in-place write raises instead of silently rewriting every other
# caller's view.
_FRESH_MKT_INV = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
_FRESH_MKT_INV.setflags(write=False)
_NO_SHOPS = np.zeros(spec.N_SHOPS, np.int32)
_NO_SHOPS.setflags(write=False)
_NO_BANK = np.zeros(spec.N_TILES, np.int32)
_NO_BANK.setflags(write=False)
_NO_OPP_MONEY = np.int32(0)
_NO_OPP = np.zeros(spec.N_PRODUCTS, np.int32)
_NO_RATE = np.full(spec.N_PRODUCTS, -1, np.int32)
_NO_OPP.setflags(write=False)
_NO_RATE.setflags(write=False)
#: `DayView.opp_burst` default [SWITCH, SELL_SLOT_RIVALRANK]: no measurement.
#: Zero, and a zero burst makes `sell_slot_rivalrank`'s term identically 0.
_NO_BURST = np.zeros(spec.N_PRODUCTS, np.int32)
_NO_BURST.setflags(write=False)
_NO_TILES = np.zeros(spec.N_TILES, np.int32)
_NO_TILES.setflags(write=False)


class DayView(NamedTuple):
    """One player's state at hour 0, with tile arrays in serpentine order."""
    day: object
    kind: object        # int[100]
    occ: object         # int[100]  crop idx / animal idx / -1
    t_day: object       # int[100]  planted_day / placed_day
    t_water: object     # int[100]  watered_today / fed_today
    t_cons: object      # int[100]  consecutive_unwatered / unfed
    t_yield: object     # int[100]
    t_fert: object      # int[100]  fertilized_until_day
    t_cared: object     # int[100]
    t_favail: object    # int[100]
    shed: object        # int[12]
    seeds: object       # int[5]
    money: object       # float scalar
    nquad: object       # int  number of unlocked quadrants (1..4)
    price: object       # int[9]  current market prices
    # Hour-0 market, for the planner's own price projection (projector.py).
    # Defaulted to a fresh market so hand-built views stay valid.
    mkt_inv: object = _FRESH_MKT_INV   # int[9]
    shops: object = _NO_SHOPS          # int[8]
    # Pending CARE bonus per animal tile (engine `pending_care_bonus`); zero
    # for plants. Defaulted so hand-built views stay valid.
    t_bank: object = _NO_BANK          # int[100]
    # The OTHER seat's standing commitment per product -- tiles per crop and
    # animals through `spec.ANIMAL_PRODUCT` (`opp_commitment` builds it, the
    # simulator and `agent/parse.py` fill it). The observation carries both
    # farms, so this is a fact the day already holds. Defaulted to an empty
    # farm, which is the identity for every rule that reads it, so hand-built
    # views stay valid and `OPP_MIX_ON` OFF cannot see it at all.
    opp_commit: object = _NO_OPP       # int[9]
    # The OTHER seat's standing RIPE yield per product [SWITCH,
    # SELL_SLOT_PRIORITY]. `opp_ripe_yield` builds it and only
    # `sell_slot_scores` reads it, so it is an empty farm on every view built
    # with the switch off -- which is the batch floor, the same number a board
    # with no rival harvest gives.
    opp_ripe: object = _NO_OPP         # int[9]
    # The OTHER seat's money [SWITCH, SELL_SLOT_MIRROR_GATE]. `policy_obs`
    # already hands the network `st.money[q]`, so this is a fact the day holds;
    # only the gate's money-lead veto reads it, and it is supplied only when
    # that switch is on, so a hand-built view and an ungated rollout keep the
    # default. Zero is a rival with nothing, i.e. the widest possible lead --
    # the veto errs towards the shipped row, never towards the reorder.
    opp_money: object = _NO_OPP_MONEY  # int scalar
    # The rival's MEASURED sale rate per product [SWITCH, RIVAL_TELL], `-1`
    # where the tell did not fire. Only `sell_slot_scores` reads it and only
    # under `RIVAL_TELL_ON`, so every other view carries the all-`-1` sentinel
    # -- which is "keep the `opp_ripe` proxy", the shipped behaviour.
    opp_rate: object = _NO_RATE        # int[9]
    # The rival's MEASURED single-turn sale BURST per product [SWITCH,
    # SELL_SLOT_RIVALRANK], zero where the tell did not fire. Only
    # `sell_slot_rivalrank` reads it and only under that switch, so every other
    # view carries the all-zero default -- which makes the correction term
    # identically zero, i.e. the shipped `sell_slot_scores` ranking.
    opp_burst: object = _NO_BURST      # int[9]
    # Public opponent tile fields and the physical learner seat.  These are a
    # separate PROGRAM1 selector channel: the frozen residual head continues
    # to receive only `_residual_features`' original 64 values.
    opp_kind: object = _NO_TILES       # int[100]
    opp_occ: object = _NO_TILES        # int[100]
    opp_t_day: object = _NO_TILES      # int[100]
    opp_t_yield: object = _NO_TILES    # int[100]
    program_opp_money: object = _NO_OPP_MONEY  # actual public rival purse
    seat: object = np.int32(0)         # physical learner seat, 0 or 1

    # money is int32: the engine stores a float but every delta is an integer
    # price or cost, so it stays exactly integral all season.


def _rank(xp, mask):
    """Exclusive rank of each True entry among the True entries preceding it."""
    m = mask.astype(xp.int32)
    return xp.cumsum(m) - m


def _rank_near(xp, mask, key):
    """Exclusive rank of each `mask` entry by ascending `key`, exact ties to
    the lower index (serpentine position) [R3].

    `key == 0` everywhere reproduces `_rank` bit for bit, which is what makes
    the `compact` gene inert at zero theta and every incumbent checkpoint's
    plan unchanged by it.

    Not `_rank_by`: that is a [100, 100] pairwise compare and `task_order`
    already runs five of those a day. `key` is a bucket index in
    `0 .. DIST_MAX`, so a static unrolled pass over the buckets -- nine [100]
    cumsums and nine [100] reduces -- costs far less and ties break by index
    for free, because `cumsum` is already in index order.
    """
    i32 = xp.int32
    m = mask.astype(i32)
    lt = xp.zeros(N_T, i32)         # masked entries in a strictly lower bucket
    same = xp.zeros(N_T, i32)       # masked entries in this bucket, lower index
    for b in range(DIST_MAX + 1):
        inb = (key == b).astype(i32) * m
        cum = (xp.cumsum(inb, dtype=i32) - inb).astype(i32)
        same = same + (key == b).astype(i32) * cum
        lt = lt + (key > b).astype(i32) * xp.sum(inb, dtype=i32)
    return (lt + same).astype(i32)


def _dev_key(xp, compact):
    """int[100]: the `_rank_near` bucket of every sweep position under the
    day's `compact` gene [R3].

    `compact` is 0 .. `DIST_MAX`: 0 puts every tile in bucket 0, so the rank is
    the plain sweep rank; `DIST_MAX` reproduces `DIST_SHED` itself, so the day
    develops the tiles nearest the shed first. In between the distance is
    banded, and the sweep still orders inside a band -- which is the gradient
    ES needs, and the reason this is a scale and not a flag.
    """
    return (xp.asarray(DIST_SHED) * xp.asarray(compact).astype(xp.int32)) // DIST_MAX


def _inverse(xp, perm):
    """rank[perm[k]] = k."""
    n = perm.shape[0]
    ranks = xp.arange(n, dtype=xp.int32)
    if hasattr(perm, "at"):
        return xp.zeros(n, xp.int32).at[perm].set(ranks)
    out = np.zeros(n, np.int32)
    out[np.asarray(perm)] = ranks
    return out


def _rank_by(xp, mask, value):
    """Exclusive rank of each `mask` entry by descending `value` among the
    masked entries, exact ties to the lower index (serpentine position).
    Pairwise, like `task_order`, so both backends agree on every tie."""
    both = mask[None, :] & mask[:, None]
    v = value.astype(xp.int32)
    idx = xp.arange(mask.shape[0], dtype=xp.int32)
    ahead = both & ((v[None, :] > v[:, None])
                    | ((v[None, :] == v[:, None]) & (idx[None, :] < idx[:, None])))
    return xp.sum(ahead.astype(xp.int32), axis=1, dtype=xp.int32)


def _count_le(xp, a, v):
    """`searchsorted(a, v, side="right")` for sorted `a`, as a plain comparison.

    Both arrays here are tiny (<= 100 entries), and `searchsorted` lowers to a
    scan or a sort in XLA, which dominates compile time when it sits inside the
    24-turn / 29-day nested scans. Counting `a <= v` is the same answer for
    sorted `a` and compiles to a single broadcast reduce.
    """
    a = xp.asarray(a)
    v = xp.asarray(v)
    if getattr(v, "ndim", 0) == 0:
        return xp.sum((a <= v).astype(xp.int32))
    return xp.sum((a[None, :] <= v[:, None]).astype(xp.int32), axis=1)


def _pick_masks(xp, d):
    """bool[N_PICK, 100]: which tiles consume each pickup kind [0.12].

    Feed wheat, fertilizer, then one row per animal kind: a day that places
    geese, cows and sheep owes three animal pickups, not one, and the engine
    charges every one of them."""
    return xp.stack([d.want_feed, d.want_fert]
                    + [d.m_place & (d.place_kind == a) for a in range(spec.N_ANIMALS)])


def _pickup_kinds(xp, d):
    """int: how many of the `N_PICK` pickup kinds have any demand at all
    [LAW, 0.12].

    `_routes` charges a unit one turn per kind *its own block* consumes, so
    the admit stage's turn budget has to subtract the allowance from every
    unit, not once from the day. This is the per-unit upper bound: a block can
    owe at most the kinds the whole day wants, and owes exactly that whenever
    the demand is spread across the sweep."""
    masks = _pick_masks(xp, d)
    return xp.sum((xp.sum(masks.astype(xp.int32), axis=1, dtype=xp.int32) > 0).astype(xp.int32),
                  dtype=xp.int32)


def _cum_take(xp, cum, k):
    """cum[k-1]: the total over the first k entries of a cumulative sum (0 when
    k == 0) -- a quote walk's coins, an admitted prefix's task value."""
    return xp.where(k > 0, cum[xp.clip(k - 1, 0, cum.shape[0] - 1)], 0)


#: Longest per-candidate unit stream `_stream_rev` prices (a goose's whole
#: season of eggs or fertilizer is under 32).
STREAM_MAX = 32

#: Days from planting or placing to the first yield, per market product: the
#: sales window each candidate's stream is priced against [1.3]. Static -- both
#: tables it reads are -- and it names all three animal products now that a day
#: can buy all three. Fertilizer stays at 0: an animal makes it from day one.
_FIRST_P = np.concatenate([
    spec.CROP_FIRST_YIELD_DAY,
    np.zeros(spec.N_PRODUCTS - spec.N_CROPS, np.int32)]).astype(np.int32)
for _a in range(spec.N_ANIMALS):
    _FIRST_P[int(spec.ANIMAL_PRODUCT[_a])] = int(spec.ANIMAL_FIRST_YIELD_DAY[_a])
_FIRST_P.setflags(write=False)

#: Pickup kinds a unit's block can consume: feed wheat, fertilizer, and one per
#: animal kind [0.12].
N_PICK = 2 + spec.N_ANIMALS
#: What each pickup kind picks up, in that order. Fully static since the mixed
#: herd: there is one row per animal, not one dynamic row for "the day's kind".
PICK_ITEM = np.array([spec.I_WHEAT, spec.I_FERT]
                     + [spec.I_GOOSE + a for a in range(spec.N_ANIMALS)], np.int32)


def _stream_rev(xp, price_table, inv0, u, k):
    """int[len(k)]: coins the k-th block of `u` units of one product fetches
    when sold `k*u` units down the curve from inventory `inv0` -- straight
    table reads, so a hundred candidates of six units each price correctly
    (a K-long cumsum would clip every unit past the shed's worth to zero).

    `price_table` is the product's own row.
    """
    m = xp.arange(STREAM_MAX, dtype=xp.int32)[None, :]
    idx = xp.clip(inv0 + k[:, None] * u + m - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    return xp.sum(xp.where(m < u, price_table[idx], 0), axis=1).astype(xp.int32)


def _pipeline_units(xp, view, is_plant, has_animal, day):
    """int[9]: own supply already committed by `VAL.pay_day()` -- every planted
    tile's remaining units (as if watered daily), every placed animal's
    remaining fires, one fertilizer per animal-day, and the shed. An upper
    bound on what the farm itself will push into each product's market before
    the season ends: conservative for valuing one more seed of it."""
    i32 = xp.int32
    crop = xp.clip(view.occ, 0, spec.N_CROPS - 1)
    kind = xp.clip(view.occ, 0, spec.N_ANIMALS - 1)
    t_units = xp.where(is_plant, VAL.remaining_plant_units(xp, crop, view.t_day, day), 0)
    a_units = xp.where(has_animal, VAL.fires_between(
        xp, view.t_day, xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[kind],
        xp.maximum(xp.asarray(spec.ANIMAL_INTERVAL)[kind], 1), day + 1, VAL.pay_day()), 0)
    prod = xp.where(is_plant, crop, xp.asarray(spec.ANIMAL_PRODUCT)[kind])
    live = (is_plant | has_animal)[:, None]
    onehot = (prod[:, None] == xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :]) & live
    pipe = xp.sum(onehot.astype(i32) * (t_units + a_units)[:, None], axis=0, dtype=i32)
    fert = xp.sum(has_animal.astype(i32), dtype=i32) * xp.maximum(VAL.pay_day() - day, 0)
    pipe = pipe + xp.where(xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_FERT, fert, 0)
    return (pipe + view.shed[:spec.N_PRODUCTS].astype(i32)).astype(i32)


def task_order(xp, task, score, tier=None):
    """Indices listing every `task` tile first, by descending `tier`, then
    descending `score`, exact ties by ascending index (serpentine position);
    idle tiles follow in index order.

    `tier` is an ordinal rank taken before the score: a higher-tier task
    outranks every lower-tier one whatever its score, so the value only orders
    within a tier. The admission order passes 0.5's mandatory flag (0 or 1);
    the route order passes the two-group route rank of 1.6 (0 or 1,
    priced-or-mandatory over worthless). Any int32 tier works --
    tiers are compared pairwise as (tier, key), never packed into one integer
    [LAW, 0.5]: the key spends 7 of its bits on the index, so a score at the
    coin ceiling (1 << 20, section 2) reaches 1 << 27 -- a sixteenth of int32,
    room a tier field would technically fit in. It stays out of the key
    anyway, because the pairwise compare orders (tier, key) lexicographically
    for free, packing would tie a LAW to whatever bound `tile_value` happens
    to clip at, and no packing constant has to be revisited when a caller
    grows its tier range.

    Ranked pairwise rather than sorted: both backends then agree on every tie,
    and a 100x100 compare is far cheaper to compile than a sorting network.
    """
    n = task.shape[0]
    idx = xp.arange(n, dtype=xp.int32)
    t = task.astype(xp.int32)
    if tier is None:
        tier = xp.zeros(n, xp.int32)
    tr = tier.astype(xp.int32)
    # One unique integer key per tile: score first, lower index wins a tie.
    # |score| stays under the coin ceiling 1 << 20 (`tile_value` clips to it),
    # so 128 x score cannot wrap int32.
    key = score.astype(xp.int32) * 128 + (127 - idx)
    ahead = ((tr[None, :] > tr[:, None])
             | ((tr[None, :] == tr[:, None]) & (key[None, :] > key[:, None]))) & task[None, :]
    rank_t = xp.sum(ahead.astype(xp.int32), axis=1)
    n_true = xp.sum(t)
    rank_f = xp.cumsum(1 - t) - (1 - t) + n_true
    dest = xp.where(task, rank_t, rank_f)
    if hasattr(idx, "at"):
        return xp.zeros(n, xp.int32).at[dest].set(idx)
    out = np.zeros(n, np.int32)
    out[np.asarray(dest)] = np.arange(n, dtype=np.int32)
    return out


def _set1(xp, arr, i, v):
    if hasattr(arr, "at"):
        return arr.at[i].set(v.astype(arr.dtype) if hasattr(v, "astype") else v)
    out = arr.copy()
    out[i] = v
    return out


def _as(xp, v):
    return v.astype(xp.int32) if hasattr(v, "astype") else xp.asarray(v, xp.int32)


def _row(xp, arr, r, vals):
    """arr[r] = vals for a static row index."""
    if hasattr(arr, "at"):
        return arr.at[r].set(vals.astype(arr.dtype))
    out = arr.copy()
    out[r] = vals
    return out


_DEFAULT_TABLE = None


def default_price_table() -> np.ndarray:
    """The engine's default price table, built once. The sim passes its own
    (possibly market-randomised) `tables.price`; the submission and hand-built
    views use this."""
    global _DEFAULT_TABLE
    if _DEFAULT_TABLE is None:
        _DEFAULT_TABLE = spec.build_price_table()
        _DEFAULT_TABLE.setflags(write=False)
    return _DEFAULT_TABLE


#: True where the kind needs a coop rather than a pasture, so a per-kind room
#: is a `where` over two scalars instead of a three-way stack (see `_share`).
NEEDS_COOP = (spec.ANIMAL_STRUCT == spec.KIND_COOP)
#: Lane i's predecessors in list order, as a strictly-lower matrix of ones:
#: `_prefix` reads the running total out of it in one reduction per lane.
BEFORE_ALL = np.tril(np.ones((spec.N_ANIMALS, spec.N_ANIMALS), np.int32), -1).astype(np.int32)
#: The same, restricted to the kinds ahead that need the *same* structure --
#: cow and sheep share the pastures, the goose's coops are its own.
BEFORE_STRUCT = (BEFORE_ALL
                 * (spec.ANIMAL_STRUCT[:, None] == spec.ANIMAL_STRUCT[None, :])).astype(np.int32)


def _prefix(xp, want, before):
    """int[n]: `sum(want[j] for j where before[i, j])`, lane by lane.

    A running scalar would do the same arithmetic, but it builds each lane out
    of a *different* expression chain and the vector is then a `stack`. That
    lowers to an XLA `concatenate`, and inside a vectorised elementwise fusion
    the sm_86 tile emitter turns a concatenate into an `scf.if` on the lane
    index that it then fails to widen -- jaxlib 0.10.2 miscompiles the
    three-animal walks below with `'scf.if' op ... 'tensor<1x1xi32>' should
    match ... 'tensor<4x1xi32>'`. One reduction against a constant mask gives
    every lane the same expression, so the fusion stays uniform. The
    arithmetic is integer and exact, so both backends are bit-identical to the
    running-scalar form.
    """
    i32 = xp.int32
    mask = xp.asarray(before).astype(i32)
    return xp.sum(mask * want[..., None, :].astype(i32), axis=-1, dtype=i32).astype(i32)


def _share(xp, want, room, before):
    """int[n]: `want`, each lane clipped to what a room shared in list order
    still holds once the lanes `before` it have taken theirs. `room` is a
    scalar when one budget is shared by every lane and an int[n] when the
    budget is per kind (`sfree`), which broadcasts either way.

    The unrolled walk -- clip, subtract, clip the next -- leaves
    `max(room - sum(want[:i]), 0)` for lane i whenever the wants are
    non-negative, because the remainder after a clip is exactly
    `max(remainder - want, 0)`. Every caller here passes counts, so the closed
    form is the walk, not an approximation of it.
    """
    i32 = xp.int32
    want = want.astype(i32)
    room = xp.asarray(room).astype(i32)
    return xp.minimum(want, xp.maximum(room - _prefix(xp, want, before), 0)).astype(i32)


# `PLANT_FILL_ON` [SWITCH]: put the day's *surplus* idle tiles to work, and
# leave the herd's reserve standing.
#
# `brain.decide` sizes the day's development blind to what a tile is worth:
# `n_dev = _qfloor(dev_frac * n_free)` (brain.py:622) with `dev_frac` a sigmoid
# of `head[5]`, and `plant_total = n_dev - animals` is the *hard* cap on the
# day's plantings -- `_wants` below clips the seed want to it, `plant_eff`
# clips the PLANT ops to it. Measured over 32 real-engine games against the
# McGrain tape (S/autopsy_mcgrain), our board carries **196.6 idle tile-days a
# game**; 83.1 of them are planted inside three days and 11.8 are taken by a
# pasture or a coop, which leaves **101.6 tile-days that are still EMPTY three
# days later**. At our own realised wheat -- 2.87 units a planting at 41 coins
# over a 3.1-3.9 day life, 25-30 coins a tile-day -- those tile-days are worth
# **+2,400 to +2,700 a game** gross of the ~330 coins of seed, on a board where
# wheat's shared inventory never once climbs back to I0.
#
# The v1 of this switch (b0185b2, kept on its own branch) scaled the target up
# to *every* one of those tiles in the gene's own proportions and lost -20,315
# a game at t -5.0: wool fell 234 units to 97 and fertilizer 200 to 84 because
# a tile planted today is not free tomorrow -- `n_free` fell 383 free-tile-days
# to 263 and `n_dev`, `animal_count` and every future placement fell with it.
# The idle tiles are the reserve the herd is built out of, and our herd's
# supply is worth more as the thing holding the opponent's prices down than as
# revenue of our own.
#
# v2 is that fill with the reserve priced, in the two ways the failure named:
#
#   (a) **the placements that are due.** The fill may only take the tiles left
#       once the next `PLANT_FILL_RESERVE_DAYS` days' animal acquisitions have
#       taken theirs, at today's rate -- `PLANT_FILL_RESERVE_DAYS *
#       sum(macro.animal_want)`, the brain's own per-day acquisition, on top of
#       the fresh tiles `_seed_room` already charges today's builds for.
#
#   (b) **the tile comes back.** The fill is planted in WHEAT alone whenever
#       the gene already wants wheat today: a wheat tile is `free_slot` again
#       in three to four days (`harvest_one`), so the pool it borrows from is
#       returned inside the reserve window, where v1's share of 17-day
#       strawberry and 10-day melon took tiles out of it for the rest of the
#       season. Only when wheat is not on today's menu at all -- late enough
#       that `can_mature` has masked it out -- does the fill fall back to the
#       gene's own proportions (`_fill_plant`).
#
# The extra seed is bought **out of the coins the day's own grant did not
# want** -- a second `budget.grant` over the seed lists alone, on the purse
# less everything the first grant spent outside them. That funding rule is
# v1's and it was learned the hard way: a first cut raised the seed want inside
# `_wants`, so the extra candidates entered the one greedy alongside the
# animals and won it (a wheat seed is ~16x value per coin against a 250-coin
# cow's ~8x), the herd stopped being bought outright and the leg scored 0/32.
#
# Everything else still prices the extra seeds as before: `budget.grant` reads
# each one at its own rank in `_stream_rev`'s supply stream, so a saturated
# crop's k-th candidate is refused exactly as it always was; the route admits
# the extra PLANT/WATER chains against the same turn budget; `plant_here` is
# still masked by `free_slot`; and the land valuation is differenced over the
# *unfilled* want, so a quadrant is worth what it was worth.
#
# **It works, and it still loses, and it ships off.** Paired over 48 seeds x 2
# seats at seed base 777001 against its own OFF leg at this sha (four
# opponents, the same command, `--workers 6`):
#
#     kagg2           88.5% -> 44.8%   paired  -12,828  t  -7.63
#     tape 103254816  57.3% -> 33.3%   paired   -6,700  t  -4.05
#     tape 104502967  52.1% -> 31.2%   paired   -7,331  t  -3.79
#     tape 104547425  32.3% -> 22.9%   paired   -9,482  t  -5.14
#     ALL (n=384)     57.6% -> 33.1%   paired   -9,085  t -10.13
#     McGrain (n=32)  46.9% -> 18.8%   paired   -8,694  t  -3.98
#
# The reserve did what it was built to do. Over the 32 McGrain replays the
# herd survives the fill -- WOOL 152 units sold to 136 and FERTILIZER 191 to
# 144, against v1's 234 to 97 and 200 to 84; COW 7.6 to 7.1, SHEEP 8.6 to 7.4,
# GOOSE 1.2 to 1.7 -- and the fill is real: wheat plantings 76.8 to 97.7 and
# wheat sold 236 to 307 units, at a 3.9-day life that hands the tile back.
#
# What it does not price is that **the scarce thing is the unit-turn, not the
# tile.** A filled tile costs one PLANT and then a WATER every day it lives,
# and the op census over the same 32 games says exactly where those come from:
# PLANT +22.3 and WATER +80.8 a game, paid for with COLLECT_FERTILIZER -47.3,
# FEED -33.2, CARE -31.1 and HARVEST -12.2. PASS *rises* 72.7, so the 18.7 %
# idle unit-turns the McGrain autopsy measured are not fungible labour -- they
# are turn-1 BUY-row waits and position-bound turns (idle-turn diagnosis
# 2026-08-30), and no amount of free land converts them into work. The animal
# cadence is what pays: FERTILIZER sold falls 47 units, which is the
# opponent's single biggest revenue line handed back, and EGG falls 50.6 to
# 20.9 on a line we sell alone. Money at d20 falls 41,855 to 37,131.
#
# So the two diagnoses now stand together and both are about a price the fill
# does not pay: v1's, that the idle tiles are the herd's build reserve, and
# v2's, that even with that reserve held, an extra crop tile is bought with
# animal labour at a worse rate than the crop returns. Any third cut has to
# price the *route* it displaces -- a PLANT admitted only where it beats the
# CARE/FEED/COLLECT chain it evicts, which is `_admit`'s question and not this
# one -- rather than the land it stands on.
#
# OFF, `_fill_wheat` is never called, no second grant is run and
# `macro.plant_target` reaches the plant clip unchanged, byte for byte.
PLANT_FILL_ON = False
#: Days of animal acquisition, at today's rate, the fill must leave standing.
PLANT_FILL_RESERVE_DAYS = 3

# `PLANT_FILL_LATE_ON` [SWITCH]: the v2 fill above, refused until the herd is
# bought.  Ported from the `board-fill` worktree (`cd8a040`), whose measurement
# is `docs/strategy/2026-09-09-board-fill.md` sect.4 and which never reached a
# paired run.
#
# v2's whole loss is priced in the herd (WOOL 152 units to 136, FERTILIZER 191
# to 144, EGG 50.6 to 20.9), and that damage can only be done on the days the
# herd is still being *acquired*, because the channel is `n_free`: a tile the
# fill plants today is not free tomorrow, and `brain.decide` sizes tomorrow's
# `n_dev = dev_frac * n_free` and `animal_count = animal_share * n_dev` off
# exactly that count.  `_fill_cap`'s forward reserve is priced at *today's*
# `macro.animal_want`, itself a fraction of today's `n_free`, so the reserve
# shrinks with the pool it is meant to protect.
#
# ON, the fill is the v2 fill from `PLANT_FILL_FROM_DAY` and nothing at all
# before it: `fill_target` is `macro.plant_target` on those days, so `w_fill`
# is zero, `grant` over an all-zero want returns zeros, `n_buy` and `wants`
# merge with their own maxima and `plant_eff`/`plant_crop` are the OFF
# program's, day for day.  Both switches OFF, the `if` is the `if
# PLANT_FILL_ON` it was and the whole block is dead, byte for byte.
PLANT_FILL_LATE_ON = False
#: First day the late fill may take a tile.  12 is the first day of the traced
#: boards on which the plan builds no structure again (`n_build == 0` from 12
#: on both), i.e. the first day an idle tile has no other claimant.
PLANT_FILL_FROM_DAY = 12

# `NOOP_FIX_ON` [SWITCH, NOOPAUDIT 2026-09-23]: the planner is blind to the
# engine's intra-day decay (`_decay_plants`, kaggriculture.py:752-766). A spent
# ongoing crop (final fire lands at the eod of day `last - 1`) gets
# `max_lifespan_step = (last + 1) * 24` (:801-802): its units must be harvested
# on day `last`, and from the dawn of `last + 1` it loses one unit every other
# step and is WEED by hour 2*(y-1). The mandatory tier's premise "a deadline
# harvest keeps its units on the tile until tomorrow" is false for exactly these
# tiles, and the census (S/noopaudit) finds ~1.4 HARVESTs and ~6 WATERs a game
# landing on the resulting WEED (dev100: all at hour >= 7 on tiles dead by
# hour 2). ON, (1) the last-day harvest of a spent ongoing crop joins the
# mandatory tier (`_derive`), and (2) `agent/parse.py` hands the planner a tile
# that is WEED before hour `NOOP_DOA_H` as holding nothing and already watered,
# so no route is sent to it. No new work: (1) only reorders an existing harvest
# into the tier, (2) only removes orders the engine is certain to reject.
NOOP_FIX_ON = False
NOOP_DOA_H = 3
NOOP_FIX_EXPIRE = True   # part (1) under NOOP_FIX_ON
NOOP_FIX_DOA = True      # part (2) under NOOP_FIX_ON

# `LATE_EXEC_ON` [SWITCH, ENDFIX1 2026-09-23]: dig a spent ongoing crop on its
# FINAL harvest day and replant the tile the same day. The engine fires an
# ongoing crop for the last time at the eod of day `last - 1` (`last` = planted
# + first + (max_yield - 1) * interval); on day `last` the harvest empties it
# and from the dawn of `last + 1` it decays to WEED (kaggriculture.py:752-802).
# OFF the planner sees that tile as an occupied PLANT on `last` and on the dawn
# of `last + 1`, so the slot comes back as a WEED a DIG away one to two days
# later (PREFIX leg, ENGINE's own d20 state: WEED 9.6-12.2 tiles d23-24 vs 1.3,
# wheat tiles 15-18 vs 25-29). The ENGINE digs these tiles on `last` itself
# (17.2 strawberry + 6.1 tomato digs/board d18-29, all age == last, y0).
# ON, from `LATE_EXEC_DAY0`, such a tile (a) counts as a free slot for the
# day's plant ask (`_derive` and `brain.n_free_slots`) and (b) gets a DIG
# between its HARVEST and its PLANT whenever the day assigns it a planting or
# a build -- and only if the harvest it holds is admitted, so no unit is ever
# dug under. No new work beyond the one DIG a later WEED would have cost.
# `WHEAT_CYCLE_ON` [SWITCH, WHEATCYCLE1 2026-09-23]: rank-1 DSM's short grain
# cycle (DSMLOGIC1 rules F1/V1/P1). Engine (sim/units.py): FERTILIZE sets
# fertilized_until = day + 2, an in-window WATER adds +2 while it holds, a
# plant starts at 1 unit. WHEAT window ages 2-4: fert@1 or fert@2 -> 6 u at
# age 4; either -> 5 u at age 3 (1 + 2 + 2). CARROT window 2-3: 4 u at age 3.
#   WHEAT_CYCLE_ON         fertilize WHEAT at age >= 2 only (rides the age-2
#                          water stop instead of an age-1 trip);
#   WHEAT_CYCLE_CARROT_ON  the same for CARROT;
#   WHEAT_CYCLE_H3_ON      harvest WHEAT at age 3 when the fertilizer covers the
#                          age-3 watering (t_fert >= t_day + 3) and the age-2
#                          watering was fertilized (dawn yield >= 3); the tile is a
#                          free slot that day (FERT -> WATER -> HARVEST -> PLANT
#                          -> WATER chain on one stop).
# OFF: three Python-false branches, byte-identical.
WHEAT_CYCLE_ON = False
WHEAT_CYCLE_CARROT_ON = False
WHEAT_CYCLE_H3_ON = False
#: With H3: replant the tiles the age-3 harvest frees on the same stop (the
#: REPLANT_SAME_TURN machinery restricted to those wheat tiles, seed bought on
#: top of the day's own ask), while an age-3 wheat can still mature by pay_day.
WHEAT_CYCLE_RP_ON = True
LATE_EXEC_ON = True  # SHIP_LE 2026-09-23: promoted (ENDFIX1 dev +2 ho +11 tape +3 ENGINE +1, gift-free)

# `PLACEFEED_ON` [SWITCH, PLACEFEED1 2026-09-27, default OFF]: feed and care a
# sheep or goose on the night it is placed. CREWAUDIT1: 100 % of our placements
# go unfed+uncared on the placement night -- the feed/care plan is built from
# dawn's animal tiles, so today's placements never enter it -- and the engine
# (kaggriculture.py L826-830) pays the first production `1 + pending`, with
# pending accrued only on fed+cared nights: a sheep's first wool fire is 5 not
# 6, a goose's first egg fire 3 not 4 (a cow caps at max_held anyway). ON, a
# placement tile of a sheep/goose whose first fire is harvested by `pay_day()`
# and whose product quotes above wheat gets FEED + CARE chained AFTER its PLACE
# (same tile, same unit), one wheat each; the wheat rides the day's feed pickup
# (`Prefix.want_feed`) and any shortfall is re-bought on the turn-1 row out of
# the room and purse the grant left (`_pf_wheat`). OFF nothing is traced.
PLACEFEED_ON = True  # SHIP_VRP12_PFS (PLACEFEED3): with PF_PUMPSAFE_ON
# PLACEFEED3 2026-09-27 fix knobs (read only when PLACEFEED_ON). PLACEFEED2's
# faithful-59 failure is a BUG, not a dose: on day 0 the placement feed made
# `wheat_buy` 0 -> 2, and the opening pump fires only on `wheat_buy == 0`
# (`_market`: "holds on day 0 by construction -- nothing to feed"), so ON
# killed the 53/48 pump in 59/59 games. `PF_PUMPSAFE_ON`: on the pump day buy
# nothing for the placement feed and feed it from the pump's OPEN_PUMP_KEEP
# units instead. `PF_NOBUY_ON`: never buy for it on any day (stock only).
# `PF_DAY_MIN`/`PF_DAY_MAX`: the placement days it may fire on. `PF_HERD_MAX`:
# fire only while the dawn sheep+goose head count is below it.
PF_PUMPSAFE_ON = True  # SHIP_VRP12_PFS (PLACEFEED3)
PF_NOBUY_ON = False
PF_DAY_MIN = 0
PF_DAY_MAX = 99
PF_HERD_MAX = 999

# `V15_DODGE_ON` [SWITCH, V15LOSS1 2026-09-23, default OFF]: on days
# V15_DODGE_DAY0..V15_DODGE_DAY1 the dusk lot (LOT4, turn 17 = engine h18) is
# emitted at turn V15_DODGE_TURN instead. v15stack's ADV layer (V12, "sell cash
# products up to three turns before the inherited route sells them") pulls its
# tape h19-h21 animal-product sales to h16-h18, one turn ahead of our fixed h18
# lot (docs/strategy/2026-09-23-v15loss1.md). Same units, earlier row only.
V15_DODGE_ON = False
V15_DODGE_DAY0 = 20
V15_DODGE_DAY1 = 28
V15_DODGE_TURN = 14
#: move only MILK + WOOL (the leapfrogged products) when True.
V15_DODGE_MW = False

# `DRIP_SELL_ON` [SWITCH, DRIPSELL1 2026-09-23, default OFF]: on days
# DRIP_SELL_DAY0..DRIP_SELL_DAY1 the dusk lot (LOT4, turn 17) of each product in
# DRIP_SELL_PRODUCTS is split: up to DRIP_SELL_LOT units go out on each turn of
# DRIP_SELL_TURNS (default the first sale turn after every shop draw, which the
# engine fires on turns 0/4/8/12/16/20 AFTER that turn's sales), in turn order,
# merged into whatever row stands on that turn (same-product SELL or a free
# slot; no free slot = nothing moves). The remainder stays on turn 17. SELL
# draws on the shed (engine `_commit_unit`), so no hand trip is involved.
# Rank-1 DSM rule 17 (docs/strategy/2026-09-23-dsmlogic1.md).
DRIP_SELL_ON = False
DRIP_SELL_DAY0 = 10
DRIP_SELL_DAY1 = 28
DRIP_SELL_LOT = 1
#: ":"-separated turns (switch strings split on ","), e.g. "1:5:9:13:21".
DRIP_SELL_TURNS = "1:5:9:13:21"
#: letters S = STRAWBERRY, M = MILK, W = WOOL.
DRIP_SELL_PRODUCTS = "SMW"
_DRIP_NAMES = {"S": "STRAWBERRY", "M": "MILK", "W": "WOOL"}
LATE_EXEC_DAY0 = 0
#: Crew cap under LATE_EXEC from `LATE_EXEC_HIRE_DAY0` (0 = no cap).
LATE_EXEC_HIRE_CAP = 0
LATE_EXEC_HIRE_DAY0 = 20


def _final_slots(xp, view):
    """Ongoing crops on (or past) the day of their final harvest [LATE_EXEC]."""
    c = xp.clip(view.occ, 0, spec.N_CROPS - 1)
    last = (view.t_day + xp.asarray(spec.CROP_FIRST_YIELD_DAY)[c]
            + (xp.asarray(spec.CROP_MAX_YIELD)[c] - 1)
            * xp.asarray(spec.CROP_INTERVAL)[c])
    return ((view.kind == spec.KIND_PLANT)
            & (xp.asarray(spec.CROP_ONGOING)[c] == 1)
            & (view.day >= last) & (view.day >= LATE_EXEC_DAY0))


# `RELAY_FILL_ON` [SWITCH, RELAYFILL1 2026-09-23]: DSM's d20-27 relay on the
# tiles our ask leaves empty. Cause (S/relayfill1 trace, 3 V56 dev boards):
# `brain.decide` asks `dev_frac * n_free` (~0.5 of the free slots d20-27) and
# `_derive` funds ALL of it (shortfall 0, purse 19k-60k idle); seeds and cash
# never bind. ON, on `RELAY_DAYS`, the free slots the funded ask and the day's
# builds leave (`_fill_cap`) are planted, `RELAY_FRAC` of them, split by
# `RELAY_W_*` (int weights per crop) over the crops that still mature by
# `RELAY_LAST_HARVEST` at full yield (tomato only to `RELAY_TOMATO_LAST`), seed bought directly out of the
# purse the grant left above `RELAY_FLOOR`. `RELAY_SELL_NOW` zeroes the crop
# reservation (`macro.hold`) from `RELAY_DAYS[0]`, so the relay sells daily.
# OFF: two Python-false branches, byte-identical.
RELAY_FILL_ON = False
RELAY_DAYS = (20, 25)
RELAY_FRAC = 1.0
RELAY_W_WHEAT = 1                 # int crop weights of the relay split
RELAY_W_CARROT = 1
RELAY_W_TOMATO = 0
RELAY_TOMATO_LAST = 20
RELAY_LAST_HARVEST = 28
RELAY_FLOOR = 1000
RELAY_SELL_NOW = False
#: Relay only in the final pass (after the crew is chosen): the relay uses the
#: chosen crew's idle turns and never buys a hand (the +8 hand-days at the
#: fib price 89-233 were the ON-dev loss).
RELAY_PASS_B = False
#: Spare-turn gate: crew turns charged per relay tile (0 = no gate).
RELAY_TURNS = 0
# `CREW_RELAY_ON` [SWITCH, CREWRELAY1 2026-09-23]: the RELAYFILL1 relay staffed
# by the CREW24 dawn/dusk turns instead of new hands. ON (RELAY_FILL_ON need not
# be set; RELAY_DAYS / RELAY_FRAC / RELAY_W_* are read):
#  (d) the relay runs in the final `_derive` pass only, so the hire enumeration
#      (pass A) never sees today's relay work: the day's crew is the OFF crew;
#      the relay is sized to the chosen crew's spare turns (`CREW_RELAY_TURNS`
#      per tile, h21-23 credit included) -- unstaffable tiles are not planted;
#  (a) the evening `_prestock` row buys the relay crops' seed only (days
#      RELAY_DAYS shifted -1, <= EVENING_SEED_MAX, above EVENING_SEED_FLOOR);
#  (b) on RELAY_DAYS a PLANT-opening block may start at hour 1 when today's BUY
#      row buys no seed (H1_WORK's seed half only; its pickup half gifted);
#  (c) d RELAY_DAYS[0]..RELAY_LAST_HARVEST the admit stage gets
#      `H23_WATER_TURNS`/unit of h21-23 credit (after the crew is chosen).
# OFF: Python-false branches, byte-identical.
CREW_RELAY_ON = False
# [SWITCH, ROUTENN1] trained crew policy (`agent/route_nn.py`): a hire delta on the dawn argmax (numpy path only)
# and a per-turn dispatcher for the units the day plan leaves idle. OFF = byte-identical.
ROUTE_NN_ON = False
ROUTE_NN_PARAMS = ""
ROUTE_NN_HIRE_FN = None     # set by agent/route_nn at import (no lazy import inside a game)
# [SWITCH, ROUTENN3] per-hour pointer over the day plan's FULL task list (`agent/route_nn3.py`): every unit
# (h0-2 incl.) may keep the plan, take another unit's planned stop or an unplanned legal job. OFF = byte-identical.
ROUTE_NN3_ON = False
#: [ROUTEOPT1] day crew VRP (`agent/route_vrp.py`): at dawn the built day table is re-routed as a vehicle-routing
#: problem over the planner's own task set and a greedily reduced crew that completes every task is written back
#: (the last HIRE rows are removed; greedy heuristic, not a proven minimum crew). Runtime-only (the engine `Runtime` and the SIMGAP1 guard seat); OFF = untouched.
ROUTE_VRP_ON = True
#: [ROUTEOPT1] the hire bill the VRP saved is hidden from the planner (its purse = real purse - saved), so every
#: later decision is the OFF plan's and the saving is banked, not spent (dev100 unshadowed: theirs +591 t 3.2 gift).
ROUTE_VRP_SHADOW_ON = True
#: [SALEPIN1] sub-switches of ROUTE_VRP_ON (OFF = the ROUTEOPT1 / res940_vrp ship byte for byte; SHIP_VRP2 promoted
#: FIX_FROZEN + VERIFY to default ON = res940_vrp2).
#: FIX_FROZEN: the spawn fixed point counts FROZEN hands (the planner's own positions) in the access-tile occupancy
#: and requires their planner spawns to hold (bug: a frozen hand was invisible, the next hire got the wrong spawn,
#: its whole route ran one tile off -> FEEDs missed -> animals escaped -> less milk/wool -> rival price gift).
ROUTE_VRP_FIX_FROZEN = True
#: VERIFY: after the write-back, replay the new table with the engine spawn rule: every planner (tile, op) must be
#: done on its tile, every PICKUP/DROP on an access tile, and the shed must cover every PICKUP no worse than the
#: planner's own table (unit actions before market rows); else the day keeps the planner's table.
ROUTE_VRP_VERIFY = True
#: PIN_PICKUP: a product is picked up no earlier than the planner's own first PICKUP hour of it.
ROUTE_VRP_PIN_PICKUP = False
#: [VRPFALLBACK1] NEEDS_FIX: the VRP's pickup model counts the wheat a planner HARVEST stop yields (ripe wheat
#: tile, dawn yield_units) as carried by the unit that harvests it (like COLLECT_FERTILIZER's fertilizer), so a
#: route that harvests wheat and then FEEDs no longer picks that wheat up from the shed (the planner feeds from
#: same-day harvested wheat; the extra PICKUP came up short and VERIFY threw the day back, ~2.9 days/game).
ROUTE_VRP_NEEDS_FIX_ON = True
#: [VRPFALLBACK1] under NEEDS_FIX: where the rewritten routes still pick up more of a product than the shed holds
#: after the planner's early SELL rows, sell that many fewer (or buy that many more in its BUY_PRODUCT row).
ROUTE_VRP_NEEDS_TRIM = True
#: [ROUTEFILL1] what the VRP does with the turns it frees: "ii" = drop hires (ROUTEOPT1, byte-exact default),
#: "i_fill" = keep the planner's crew and admit up to ROUTE_FILL_CAP fill plantings of ROUTE_FILL_CROP per day
#: (PLANT + same-day WATER, DIG first on a weed tile) into the solved routes while every stop still fits and the
#: fill ledger's later-day tending load (ROUTE_FILL_TEND turns/planting/day) stays <= ROUTE_FILL_FRAC x today's
#: gross spare turns; "hybrid" = i_fill, then mode ii drops the hands the fills could not use; "ii_fill" = mode ii
#: drops first, then fills into the (greedy) reduced crew's spare turns.
ROUTE_FILL_MODE = "ii"
ROUTE_FILL_CAP = 3
ROUTE_FILL_CROP = "WHEAT"
ROUTE_FILL_DAYS = (10, 25)
ROUTE_FILL_TEND = 3.0
ROUTE_FILL_FRAC = 0.5
ROUTE_FILL_WEED = True
ROUTE_FILL_SCAN = 16
# [SWITCH, ROUTEOPT2] Optional tail tasks: under ROUTE_VRP_OPT_ON the planner tags the ops its tail
# switches add (TAIL_CARE / TAIL_FILL / CARE_FILL) in unit_a (ROUTE_VRP_OPT_MARK + 1/2/3; unit_a is
# unused by every one of those ops) and route_vrp's mode ii may leave them undone when their summed
# value (overflow._job_cost) is below the fib cost of the hand kept only for them.
ROUTE_VRP_OPT_ON = False
ROUTE_VRP_OPT_MARK = 90
# [SWITCH, ROUTEOPT2] unsolved-day fixes in route_vrp (sequential spawn fixed point, per-unit split of
# merged same-tile stops, pickup window +1).
ROUTE_VRP_FIX_ON = True  # SHIP_VRP26 (STACK1 hAC: vrp25 + ROUTEOPT2 route_vrp fixes)
# [SWITCH, VRPMISS1] a day still unsolved after the search + ROUTEOPT2 retry (the planner's rows would play) gets one
# more solve in route_vrp._miss_retry: M1 = construct misses repaired (regret-2 + ejection), M2 = spawn-robust re-solve
# (hires searched from start + 2, sequential spawns re-checked), M3 = M1 then M2, M4 = M3 + freeze fallback; the apply
# deadline is raised by ROUTE_VRP_MISS_EXTRA_S on that day only. OFF = vrp26 byte for byte.
ROUTE_VRP_MISS_ON = True  # SHIP_VRP27_VM_M3 (VRPMISS1: vrp26 + the unsolved-day retry M3, +0.15 s on that day)
ROUTE_VRP_MISS_CELL = "M3"
ROUTE_VRP_MISS_EXTRA_S = 0.15
#: [VRPREPAIR1] mode ii: a failed crew drop (the last hire's stops do not all re-insert in their current order) gets
#: a bounded repair (route_vrp.Solver._repair: regret-2 insertion order + 1-step ejection chain, REPAIR_MS /
#: REPAIR_EJECT_K, inside the apply() deadline) before the reduction stops. OFF = byte-identical.
ROUTE_VRP_REPAIR_ON = True   # SHIP_VRP5 (res940_vrp5), with route_vrp.REPAIR_LAST_DAY = 20
# [ROUTERJIT1] RRDEPTH1 deep VRP search, affordable on the compiled router kernels (route_vrp_c.so); without the
# library (route_vrp.DEEP_NEEDS_JIT) the router keeps the shipped (30, 8, off) search.
ROUTE_VRP_RR_ITERS = 150
ROUTE_VRP_RR_K = 10
ROUTE_VRP_RR_RESOLVE_ON = True
ROUTE_VRP_RR_DEEP_LAST_DAY = None
ROUTE_VRP_RR_WALL_S = None
ROUTE_VRP_JIT_ON = True
EMPTY_ROUTE_UNHIRE_ON = True   # SHIP_VRP6 [LABOUR1/SHIPUA1] drop the HIRE of a kept hand whose final VRP route is empty (route_vrp._unhire_empty)
ROUTE_NN3_PARAMS = ""
CREW_RELAY_TURNS = 6
CREW_RELAY_EVE = True
CREW_RELAY_H1 = True
CREW_RELAY_H23 = True
#: Later-day half of (d): the relay tiles still growing are credited to the
#: hire enumeration at `CREW_RELAY_CREDIT` turns each (water + move), so their
#: work never buys a hand either. Host-side memory (numpy runtime only: the
#: planner runs once a day per game in order; a day <= the last seen resets).
CREW_RELAY_CREDIT = 2
_CR_MEM = {'last': -1, 'plants': {}}
# `FILL_WORK_ON` [SWITCH, FILLWORK1 2026-09-24]: more WORK with the hire count
# held fixed. On `FILL_WORK_DAYS` the final `_derive` pass (after the crew is
# chosen) plants up to `FILL_WORK_MAX` extra tiles of `FILL_WORK_CROP`
# ("wheat" = the cheapest seed, or "carrot" = the shortest life), sized to the
# chosen crew's spare turns at `FILL_WORK_TURNS` per tile (PLANT + waterings +
# harvest + moves, FILLWORK1 census) with the h21-23 idle turns credited
# (`H23_WATER_TURNS`/unit), seed bought from the grant's leftover. Later days:
# the fill tiles still growing are credited to the hire enumeration at
# `FILL_WORK_CREDIT` turns each (xp-pure estimate: young fill-crop tiles, capped
# at FILL_WORK_MAX x days since the window opened), so their water never buys a
# hand; the admit stage gets the h21-23 credit over the fill's life.
# No evening seed row, no hour-1 opening (CREWRELAY1 costs). OFF: Python-false
# branches, byte-identical.
FILL_WORK_ON = False
FILL_WORK_MAX = 2
FILL_WORK_CROP = "wheat"
FILL_WORK_DAYS = (10, 26)
FILL_WORK_TURNS = 6
FILL_WORK_H23 = True
FILL_WORK_CREDIT = 2


def _fw_alive(xp, view):
    """Estimated fill tiles still growing (xp-pure) [FILLWORK1]."""
    i32 = xp.int32
    c = spec.I_CARROT if str(FILL_WORK_CROP) == "carrot" else spec.I_WHEAT
    life = int(spec.CROP_MAX_YIELD_DAY[c])
    age = view.day - view.t_day
    young = (view.kind == spec.KIND_PLANT) & (view.occ == c) & (age >= 1) & (age < life)
    n = xp.sum(young.astype(i32), dtype=i32)
    since = xp.clip(xp.asarray(view.day, i32) - int(FILL_WORK_DAYS[0]), 0, life - 1)
    return xp.minimum(n, int(FILL_WORK_MAX) * since).astype(i32)


def _cr_note(xp, day, eff):
    """Record today's relay plantings per crop [CREWRELAY1, numpy only]."""
    if xp is not np:
        return
    d = int(np.asarray(day))
    if d < _CR_MEM['last']:
        _CR_MEM['plants'] = {}
    _CR_MEM['last'] = d
    _CR_MEM['plants'][d] = np.asarray(eff, np.int64).copy()


def _cr_alive(xp, day):
    """Relay tiles planted before `day` and not yet at full yield [CREWRELAY1]."""
    if xp is not np:
        return 0
    d = int(np.asarray(day))
    if d < _CR_MEM['last']:
        _CR_MEM['plants'] = {}
    _CR_MEM['last'] = d
    n = 0
    for d0, eff in _CR_MEM['plants'].items():
        if d0 < d:
            n += int(np.sum(eff * ((d0 + spec.CROP_MAX_YIELD_DAY.astype(np.int64)) >= d)))
    return n


def _relay_fill(xp, view, macro, fill_target, n_buy, costs, purse, seed_cap,
                n_units=None, worked_pre=None):
    """`(fill_target, n_buy)` with the relay added on the spare slots [RELAYFILL1]."""
    i32 = xp.int32
    day = view.day
    seed = n_buy[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS].astype(i32)
    fund = xp.minimum(fill_target.astype(i32), view.seeds + seed).astype(i32)
    cap = _fill_cap(xp, macro, seed_cap)
    room = xp.maximum(cap - xp.sum(fund, dtype=i32), 0).astype(i32)
    r_turns = CREW_RELAY_TURNS if CREW_RELAY_ON else RELAY_TURNS
    if FILL_WORK_ON:
        r_turns = int(FILL_WORK_TURNS)
    if r_turns and n_units is not None:
        # Turn gate (`land_reach`'s numerator, less the funded ask's own PLANT
        # ops): the relay may only take the crew's spare turns, `RELAY_TURNS`
        # per tile (PLANT + its waterings + moves).
        spare = (xp.asarray(n_units).astype(i32) * (TPD - O.ROUTE_BASE - LAND_PICKUPS)
                 - (xp.asarray(worked_pre).astype(i32) + xp.sum(fund, dtype=i32))
                 * (1 + EST_MOVES))
        if CREW_RELAY_ON and CREW_RELAY_H23:
            # [CREWRELAY1] the h21-23 credit the admit stage will get today
            spare = spare + xp.where(
                (day >= int(RELAY_DAYS[0])) & (day <= int(RELAY_LAST_HARVEST)),
                xp.asarray(n_units).astype(i32) * int(H23_WATER_TURNS), 0).astype(i32)
        if FILL_WORK_ON and FILL_WORK_H23:
            # [FILLWORK1] the h21-23 credit the admit stage will get today
            spare = spare + xp.where(
                (day >= int(FILL_WORK_DAYS[0])) & (day <= int(RELAY_LAST_HARVEST)),
                xp.asarray(n_units).astype(i32) * int(H23_WATER_TURNS), 0).astype(i32)
        room = xp.minimum(room, xp.maximum(spare, 0) // int(r_turns)).astype(i32)
    live = (day >= int(RELAY_DAYS[0])) & (day <= int(RELAY_DAYS[1]))
    extra = xp.where(live, (room * int(round(RELAY_FRAC * 100))) // 100, 0).astype(i32)
    ix = xp.arange(spec.N_CROPS, dtype=i32)
    # Full yield by `RELAY_LAST_HARVEST` (a d26-27 relay tile is harvested at 1 unit on d29).
    mature = (day + xp.asarray(spec.CROP_MAX_YIELD_DAY, i32) <= int(RELAY_LAST_HARVEST))
    mature = mature & ((ix != spec.I_TOMATO) | (day <= int(RELAY_TOMATO_LAST)))
    w = xp.where(mature, xp.asarray(np.asarray([RELAY_W_WHEAT, RELAY_W_CARROT, RELAY_W_TOMATO, 0, 0], np.int32)), 0).astype(i32)
    if FILL_WORK_ON:                        # [FILLWORK1] one crop, capped per day
        live = (day >= int(FILL_WORK_DAYS[0])) & (day <= int(FILL_WORK_DAYS[1]))
        extra = xp.where(live, xp.minimum(room, int(FILL_WORK_MAX)), 0).astype(i32)
        fwc = spec.I_CARROT if str(FILL_WORK_CROP) == "carrot" else spec.I_WHEAT
        w = xp.where(mature & (ix == fwc), 1, 0).astype(i32)
    tot = xp.maximum(xp.sum(w, dtype=i32), 1)
    add = (extra * w // tot).astype(i32)
    add = (add + (ix == xp.argmax(w)).astype(i32)
           * (extra - xp.sum(add, dtype=i32)) * (xp.sum(w) > 0)).astype(i32)
    spare = xp.maximum(view.seeds + seed - fund, 0).astype(i32)
    need = xp.maximum(add - spare, 0).astype(i32)
    left = xp.maximum(purse - BUD.spend(xp, costs, n_buy) - int(RELAY_FLOOR), 0).astype(i32)
    j = xp.arange(PJ.K, dtype=i32)
    got_v = xp.zeros(spec.N_CROPS, i32)
    for c in range(spec.N_CROPS):
        l = BUD.L_SEED0 + c
        cum = xp.cumsum(xp.maximum(costs[l].astype(i32), 1), dtype=i32)
        base = n_buy[l]
        at_base = xp.where(base > 0, cum[xp.clip(base - 1, 0, PJ.K - 1)], 0)
        ext = xp.where(j >= base, cum - at_base, BUD.VALUE_CAP)
        ok = (ext <= left) & (j < base + need[c])
        got = xp.sum(ok.astype(i32), dtype=i32).astype(i32)
        spent = xp.where(got > 0, cum[xp.clip(base + got - 1, 0, PJ.K - 1)] - at_base, 0)
        left = (left - spent).astype(i32)
        got_v = got_v + got * (ix == c).astype(i32)
    eff = xp.minimum(add, spare + got_v).astype(i32)
    if CREW_RELAY_ON:
        _cr_note(xp, day, eff)
    fill_target = xp.where(xp.sum(eff) > 0, fund + eff, fill_target.astype(i32)).astype(i32)
    n_buy = (n_buy + xp.concatenate([xp.zeros(BUD.L_SEED0, i32), got_v,
                                     xp.zeros(spec.N_ANIMALS, i32)])).astype(i32)
    return fill_target, n_buy


def _relay_sell_now(xp, view, macro):
    """`macro` with the crop reservation zeroed from `RELAY_DAYS[0]` [RELAYFILL1]."""
    crop = xp.arange(macro.hold.shape[0]) < spec.N_CROPS
    live = view.day >= int(RELAY_DAYS[0])
    return macro._replace(hold=xp.where(live & crop, 0, macro.hold).astype(macro.hold.dtype))


# EXPIRY1: independent, default-OFF dawn slot and funded-ask corrections.
EXPIRY_SLOT_ON = False
ASK_FILL_ON = False

# `PLANT_ASK_ON` [SWITCH]: raise the Macro ask itself, rather than filling
# whatever the ordinary purchase walk happened to leave behind [PLANTASK1].
# VOLUMEHI found 26--38 developable tiles on every d10--19 dawn while the
# Macro asked for 0--9.  A fill buys seed outside that decision and therefore
# creates work the hire/land valuation never saw.  This switch instead floors
# `macro.plant_target` at a fraction of the very `n_free` `_wants` is about to
# price.  The added tiles are assigned one at a time by `_candidates`' own
# marginal seed ratio, and stop when their seed bill would cross the purse
# already net of the hire bill and `cash_reserve`.
#
# Pre-land and post-land asks are derived separately.  Thus
# `wants_land - wants_pre` contains the extra demand and the ordinary land
# valuation can pay for it.  `PLANT_ASK_QUAD` is the narrow escape hatch for
# the observed fourth-quadrant tie: only quadrant four, only when
# `land_reach` values all 25 tiles, and only when the post-reserve purse still
# holds the full 4,000 coins.  It removes the strict-positive value test; all
# physical, terminal and funding gates remain.
#
# OFF is a Python branch around every new expression, so the shipped graph and
# numpy plan are byte-identical.
PLANT_ASK_ON = False
PLANT_ASK_FRAC = 0.5
PLANT_ASK_DAYS = (10, 19)
PLANT_ASK_QUAD = False

# `WHEAT_LATE_ASK` [FREE FLOAT]: a DOSED, WATER-GATED wheat-only fill, d10-19.
#
# VOLUMEHI/OPSCENSUS measured the d10-19 half of the 15 hiband ship losses and
# named two facts that the two fills above do not separate.  (1) The cap is the
# ASK: the planner sees `n_free` 26-38 plantable tiles a day and asks for 0-9
# (`macro.plant_target`); nothing refuses it -- seeds never veto, tiles never
# fail, the purse idles 15k-39k from d16.  (2) The scarce thing behind the ask
# is the UNIT-TURN, not the tile: our totals are level with theirs (2,715 vs
# 2,694 turns) and their +34 plantings are funded out of PASS idle (+66), carry
# (+40) and FERTILIZE (+36) -- and they are funded in WHEAT, 83 % of their
# plantings at 3.82 water turns each, against our 8.75 for a melon.
#
# `PLANT_FILL_LATE_ON` is the same cell without either qualifier: it takes
# EVERY tile `_fill_cap` leaves, from d12 to the last day, with no turn
# accounting at all.  On this band it is -871 at t -3.01 (VOLUMEHI sect.3), and
# the read there is that the extra tiles cost more labour than they return.
# This float is that fill with the labour PRICED and the size DOSED:
#
#   * a dose, not a fill.  At most `WHEAT_LATE_ASK * n_free` tiles above the
#     gene's own ask -- their whole d10-19 surplus is +3.4 plantings a day, so
#     the interesting doses are small and the knob is continuous through zero.
#   * a turn gate.  The added tiles may not exceed what the day's SPARE crew
#     turns can water, charged at `WHEAT_LATE_TURNS` each -- one PLANT plus the
#     ~4.06 WATER turns OPSCENSUS measured over a wheat planting's life, plus
#     the move.  The spare-turn estimate is the scheduler's own, `land_reach`'s
#     numerator verbatim (crew turns less what the board already owes), which
#     is the one labour clamp this planner runs before the greedy.
#   * wheat only, d10-19 only.  `_fill_wheat` already puts the whole fill in
#     wheat when the gene has wheat live today, for the reason the tile comes
#     back in 3-4 days; the window ends at 19 because d20+ plantings are the
#     ones IDLEWORK measured dying on the vine.
#
# At 0.0 the site is closed: the `if` below is the `if PLANT_FILL_ON` it was,
# `_fill_wheat` is never called, no second grant is run and `fill_target` is
# `macro.plant_target`, byte for byte.  Flown by module override only --
# `SW_EXTRA=,WHEAT_LATE_ASK=0.5` -- because `SWITCH_GENES` is 18 wide and the
# shipped layout 7,692 floats, so a 19th column is a layout move [SELLSPREAD1].
WHEAT_LATE_ASK = 0.0
#: The window.  d10 is where the census gap opens, d19 where it closes.
WHEAT_LATE_DAY0 = 10
WHEAT_LATE_DAY1 = 19
#: Crew turns one added wheat tile is charged: PLANT + the 4.06 WATER turns a
#: wheat planting takes over its life (OPSCENSUS sect.2) + `EST_MOVES`.
WHEAT_LATE_TURNS = 6


def _wheat_late_cap(xp, view, macro, n_free, n_units, worked_pre, cap):
    """`(cap, live)`: the fill cap the dose and the turn gate allow [FREE FLOAT].

    `cap` in is `_fill_cap`'s -- the tiles the day physically has once the
    herd's forward reserve is held.  Out it is that, clipped to the gene's own
    total plus `extra`, and outside the window it is the total itself, which
    `_fill_wheat` returns as `target` unchanged.

    `live` is False on any day the gate hands back zero tiles, so the second
    grant is never run on such a day: with `fill_target == macro.plant_target`
    the seed want below is the ORDINARY want, and a second walk over the seed
    lists alone can only grant MORE of it than the first walk did (it does not
    compete with the animals), which would spend coins on seed the day cannot
    plant.  Zero extra tiles therefore means the OFF program, exactly.
    """
    i32 = xp.int32
    tot = xp.sum(macro.plant_target.astype(i32), dtype=i32)
    # The scheduler's own spare-turn estimate (`land_reach`): the crew's turns
    # for the day, less what the tiles the morning already owes work on take at
    # one op plus its move.
    turns_free = xp.maximum(
        xp.asarray(n_units).astype(i32) * (TPD - O.ROUTE_BASE - LAND_PICKUPS)
        - xp.asarray(worked_pre).astype(i32) * (1 + EST_MOVES), 0).astype(i32)
    room = (turns_free // WHEAT_LATE_TURNS).astype(i32)
    ask = xp.floor(xp.asarray(n_free).astype(xp.float64) * WHEAT_LATE_ASK
                   + 1e-9).astype(i32)
    extra = xp.maximum(xp.minimum(ask, room), 0).astype(i32)
    live = ((view.day >= WHEAT_LATE_DAY0) & (view.day <= WHEAT_LATE_DAY1)
            & (extra > 0))
    return (xp.where(live, xp.minimum(cap.astype(i32), tot + extra), tot).astype(i32),
            live)


def _fill_plant(xp, target, cap):
    """int[5]: `target` scaled up to `cap` tiles in its own proportions [SWITCH].

    Largest remainder over `target` itself as the weight vector, so the mix the
    softmax chose is preserved exactly and the only thing that moves is the
    total. Two identities make it safe to call unconditionally under the
    switch: at `cap <= sum(target)` the room is `sum(target)` and every
    quotient is `target` with a zero remainder, so the answer *is* `target`;
    and at `sum(target) == 0` -- a day on which nothing can mature or every
    market is saturated -- the fill is refused outright rather than inventing a
    crop the gene ruled out.

    Integer throughout: `target` is bounded by the 100 tiles of the board and
    so is `cap`, so the `target * room` numerator stays under 10,000 and the
    tie-break is the repo's usual pairwise compare (higher remainder first,
    exact ties to the lower crop index) rather than a sort.
    """
    i32 = xp.int32
    t = target.astype(i32)
    tot = xp.sum(t, dtype=i32)
    room = xp.maximum(xp.asarray(cap).astype(i32), tot)
    den = xp.maximum(tot, 1)
    num = t * room
    q = num // den
    rem = num - q * den
    extra = room - xp.sum(q, dtype=i32)
    j = xp.arange(spec.N_CROPS, dtype=i32)
    ahead = xp.sum(((rem[None, :] > rem[:, None])
                    | ((rem[None, :] == rem[:, None]) & (j[None, :] < j[:, None]))
                    ).astype(i32), axis=1, dtype=i32)
    filled = (q + (ahead < extra).astype(i32)).astype(i32)
    return xp.where(tot > 0, filled, t).astype(i32)


def _fill_wheat(xp, target, cap):
    """int[5]: `target` grown to `cap` tiles, in WHEAT wherever wheat is live.

    The whole of the difference between this and `_fill_plant` is *which* tile
    the fill borrows and for how long. Wheat is the one crop whose tile comes
    back inside the reserve window -- 3.1 days to the opponent's turnover, 3.9
    to ours -- so a wheat fill borrows from the herd's pool and returns it,
    where a proportional fill spends a share of it on 17-day strawberry and
    10-day melon and never gives those tiles back. It is also the one crop
    whose shared inventory never climbs back to I0 in these games, so the
    marginal unit meets very nearly the price the last one did.

    `target[I_WHEAT] > 0` is the gene's own statement that wheat is live today:
    it carries `can_mature` (nothing is planted that cannot be harvested by
    `pay_day`) and the drain mask through from `brain.decide`, so a wheat fill
    is never invented on a day the gene has ruled wheat out. On such a day the
    fill falls back to the proportions the gene did choose, which is exactly
    v1's `_fill_plant`.

    The identity `cap <= sum(target)` -> `target` holds down both branches
    (`room` is floored at the total in each), so the helper is safe to call on
    any day and the switch's OFF leg is the switch's ON leg on a full board.
    """
    i32 = xp.int32
    t = target.astype(i32)
    tot = xp.sum(t, dtype=i32)
    room = xp.maximum(xp.asarray(cap).astype(i32), tot)
    is_wheat = (xp.arange(spec.N_CROPS, dtype=i32) == spec.I_WHEAT).astype(i32)
    to_wheat = (t + is_wheat * (room - tot)).astype(i32)
    return xp.where(t[spec.I_WHEAT] > 0, to_wheat,
                    _fill_plant(xp, t, room)).astype(i32)


def _fill_cap(xp, macro, seed_cap):
    """int: the tiles the fill may take, `seed_cap` less the herd's reserve.

    `seed_cap` already charges the day for the fresh tiles *today's* builds
    take (`_seed_room`). What it does not charge for is the next few days':
    `macro.animal_want` is the brain's per-day acquisition, and holding
    `PLANT_FILL_RESERVE_DAYS` days of it free is the worst case in which every
    one of those animals has to have a pasture or a coop built for it on a
    fresh tile. That is the reserve v1 spent -- and the floor at
    `sum(plant_target)` lives in the fill helpers themselves, so a day whose
    reserve swallows the whole board still plants exactly what the gene asked.
    """
    i32 = xp.int32
    reserve = PLANT_FILL_RESERVE_DAYS * xp.sum(macro.animal_want.astype(i32), dtype=i32)
    return xp.maximum(seed_cap - reserve.astype(i32), 0).astype(i32)


def _expiry_slots(xp, view):
    """Zero-held ongoing crops whose final firing was before this dawn.

    The engine starts decay at h0 of the day after the final firing. Routes
    start later, when these tiles are weeds and require DIG before PLANT.
    Shared by the macro slot counter and the task builder.
    """
    c = xp.clip(view.occ, 0, spec.N_CROPS - 1)
    last = (view.t_day + xp.asarray(spec.CROP_FIRST_YIELD_DAY)[c]
            + (xp.asarray(spec.CROP_MAX_YIELD)[c] - 1)
            * xp.asarray(spec.CROP_INTERVAL)[c])
    return ((view.kind == spec.KIND_PLANT)
            & (xp.asarray(spec.CROP_ONGOING)[c] == 1)
            & (view.t_yield == 0) & (view.day > last))


def _ask_fill(xp, view, target, cap, values, costs, n_buy, purse):
    """Extend the funded ask using the normal marginal seed ranking.

    Only the ledger's unspent purse is available: hires, reserve, land and
    every existing grant have already been charged. Stored seeds cost zero.
    Existing grants and crop asks are preserved; no additional hires or land
    are requested. Nonproductive (including past-horizon) seeds are refused.
    """
    i32 = xp.int32
    start, end = BUD.L_SEED0, BUD.L_SEED0 + spec.N_CROPS
    bought = n_buy[start:end].astype(i32)
    funded = xp.minimum(target, view.seeds + bought).astype(i32)
    left = xp.maximum(purse - BUD.spend(xp, costs, n_buy), 0).astype(i32)
    seed_v, seed_c = values[start:end], costs[start:end]
    ix = xp.arange(spec.N_CROPS, dtype=i32)
    mature = view.day + xp.asarray(spec.CROP_FIRST_YIELD_DAY) <= VAL.pay_day()
    for _ in range(N_T):
        rank = xp.clip(bought, 0, PJ.K - 1)
        val = xp.take_along_axis(seed_v, rank[:, None], axis=1)[:, 0]
        cost = xp.take_along_axis(seed_c, rank[:, None], axis=1)[:, 0]
        need = funded >= view.seeds + bought
        cash = xp.where(need, cost, 0).astype(i32)
        ratio = (xp.clip(val, 0, BUD.VALUE_CAP) << BUD.RATIO_SHIFT) // xp.maximum(cost, 1)
        can = ((xp.sum(funded, dtype=i32) < cap) & mature & (val > 0)
               & (funded < PJ.K) & (~need | (bought < PJ.K)) & (cash <= left))
        key = xp.where(can, ratio, -1)
        best = xp.argmax(key)
        take = key[best] >= 0
        hit = (ix == best).astype(i32) * take.astype(i32)
        funded = (funded + hit).astype(i32)
        bought = (bought + hit * need.astype(i32)).astype(i32)
        left = (left - xp.where(take, cash[best], 0)).astype(i32)
    result = xp.concatenate([n_buy[:start], bought, n_buy[end:]]).astype(i32)
    return xp.maximum(target, funded).astype(i32), result


def _plant_ask(xp, view, macro, n_free, values, costs, purse):
    """Return `macro` with a funded, marginal-ranked plant ask [PLANTASK1].

    `purse` has already paid the day's hire bill and tomorrow's crew reserve;
    on the post-land leg the caller also removes the land gap.  Existing seeds
    cost no cash, while every shortage is charged at the same seed-list cost
    `_candidates` hands to `budget.grant`.  The helper only raises the ask and
    never changes its existing mix.
    """
    i32 = xp.int32
    target = macro.plant_target.astype(i32)
    live = ((view.day >= int(PLANT_ASK_DAYS[0]))
            & (view.day <= int(PLANT_ASK_DAYS[1])))
    floor = xp.floor(xp.asarray(n_free).astype(xp.float64)
                     * float(PLANT_ASK_FRAC) + 1e-9).astype(i32)
    desired = xp.maximum(xp.sum(target, dtype=i32), floor).astype(i32)

    seed_v = values[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS]
    seed_c = costs[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS]
    seed_ix = xp.arange(spec.N_CROPS, dtype=i32)
    # The base ask gets first claim on the seed envelope.  This is only an
    # affordability cap; the shared grant below remains the executor and may
    # still prefer a more valuable feed, fertilizer or animal candidate.
    base_short = xp.maximum(target - view.seeds.astype(i32), 0)
    base_rank = xp.clip(base_short - 1, 0, PJ.K - 1)
    base_cost = xp.where(
        base_short > 0,
        xp.take_along_axis(xp.cumsum(seed_c, axis=1, dtype=i32),
                           base_rank[:, None], axis=1)[:, 0], 0)
    left = xp.maximum(xp.asarray(purse).astype(i32)
                      - xp.sum(base_cost, dtype=i32), 0).astype(i32)

    for _ in range(N_T):
        rank = xp.clip(target, 0, PJ.K - 1).astype(i32)
        val = xp.take_along_axis(seed_v, rank[:, None], axis=1)[:, 0]
        cost = xp.take_along_axis(seed_c, rank[:, None], axis=1)[:, 0]
        cash_cost = xp.where(target < view.seeds.astype(i32), 0, cost).astype(i32)
        ratio = xp.where(val > 0, (val << BUD.RATIO_SHIFT) // xp.maximum(cost, 1), -1)
        can = (live & (xp.sum(target, dtype=i32) < desired)
               & (target < PJ.K) & (cash_cost <= left) & (ratio >= 0))
        key = xp.where(can, ratio, -1)
        best = xp.argmax(key)
        take = key[best] >= 0
        hit = (seed_ix == best).astype(i32) * take.astype(i32)
        target = (target + hit).astype(i32)
        left = (left - xp.where(take, cash_cost[best], 0)).astype(i32)

    return macro._replace(plant_target=target)


def _place_split(xp, want, n_free, sfree):
    """`(structures, fresh tiles)` each animal kind claims, as int[3] each.

    One pass in list order -- goose, cow, sheep -- and not three independent
    clips, because **cow and sheep compete for the same pastures** [LAW]: clip
    each against its own free-structure count and two kinds claim the same
    tile. The order is the candidate lists' own, so the tie rule is `grant`'s:
    the lower list index is served first.

    Standing structures are taken before fresh tiles are built on [0.8], and
    the fresh tiles are then walked the same way over what is left of
    `n_free`. Both walks are `_share` against a constant predecessor mask --
    `sfree` is already per kind, so the structure pass only charges a kind for
    the kinds ahead of it that want the same structure.
    """
    i32 = xp.int32
    want = want.astype(i32)
    from_struct = _share(xp, want, sfree, BEFORE_STRUCT)
    from_tiles = _share(xp, (want - from_struct).astype(i32), n_free, BEFORE_ALL)
    return from_struct.astype(i32), from_tiles.astype(i32)


def _seed_room(xp, macro, n_free, sfree, a_have):
    """`(a_want, seed_cap)`: the day's animal acquisition per kind, and the
    free tiles left for planting once its builds have taken theirs.

    Lifted out of `_wants` verbatim so `_derive` can ask the same question of
    the *post-land* board when `PLANT_FILL_ON` scales the target against it;
    every line is integer, so the two callers agree bit for bit.
    """
    i32 = xp.int32
    # `animal_want` is the day's acquisition per kind, structures free or not
    # [LAW, 0.8]: zero restocks nothing. Standing structures are stocked before
    # new ones are built (`place_here`), and stock already in the shed is
    # placed regardless -- placing is not an acquisition. The three kinds are
    # clipped **jointly** against the tiles and structures that exist, in list
    # order, so they cannot claim the same pasture twice.
    fs, ft = _place_split(xp, macro.animal_want.astype(i32), n_free, sfree)
    a_want = (fs + ft).astype(i32)
    # Builds take their tiles before plantings do (`n_build`), so the planting
    # capacity is what is left of `n_free` after the most builds this day can
    # want: `a_avail = a_have + a_buy` with `a_buy <= max(a_want - a_have, 0)`,
    # so `max(a_want, a_have)` bounds the placements.
    _, ft_ub = _place_split(xp, xp.maximum(a_want, a_have), n_free, sfree)
    seed_cap = xp.maximum(n_free - xp.sum(ft_ub, dtype=i32), 0).astype(i32)
    return a_want, seed_cap


# `WHEAT_VOLUME_ON` [SWITCH]: buy the wheat line with tile *turnover*, not
# with tiles.
#
# The 2026-09-03 live study prices WHEAT at +4,806 a loss in the opponents'
# favour (372 units a season against our 246, at the identical realised 42
# coins). The flow ledger over four real-engine games against the class-A tape
# `opponent_tape_104502967`, both seats, reproduces it -- +4,429 of revenue and
# +4,507 net of what each side spends buying wheat back -- and closes to an
# identity that says exactly one thing:
#
#     units             ours    theirs   diff
#     harvested        479.1     553.0   +73.9
#     bought           131.9     140.5    +8.6
#     fed to animals   331.4     326.0    -5.4
#     destroyed         15.5       0.0   -15.5   (a DROP into a full shed)
#     SOLD             264.1     367.5  +103.4
#
# Every unit is accounted for on both sides (`sold + fed + destroyed ==
# harvested + bought`, end-of-season shed zero on both). We do not sell less of
# what we grow -- we feed the same herd, we buy the same wheat, we realise the
# same price and our first fill is at hour 3 against their mean hour 12. **We
# grow less.** 71 % of their extra sale is extra harvest, and the harvest comes
# off tiles: they stand 13.0 wheat tiles on day 10 to our 3.8 and 23.0 on day
# 20 to our 12.8, and they put 187.0 plantings in the ground over the season
# against our 92.9.
#
# `PLANT_FILL_ON` above already tested the obvious answer -- more tiles -- and
# lost 9,085 a game at t -10.13, because a filled tile is bought with the
# animal cadence's unit-turns (PLANT +22.3 and WATER +80.8 a game, paid with
# COLLECT_FERTILIZER -47.3, FEED -33.2, CARE -31.1). That objection is about
# the *number* of tiles the day plants. This switch does not move it.
#
# What it moves is the *mix*. `brain.decide` sizes `plant_total = n_dev -
# animal_want` and splits it across the five crops by grow score; wheat is the
# only crop whose tile comes back inside the week (`first_yield_day` 2,
# `max_yield_day` 4, `ongoing` False -- the tile is freed on the harvest), so a
# tile spent on wheat is re-plantable three or four days later while the same
# tile spent on 17-day strawberry or 10-day melon is not. Shifting a constant
# fraction of the day's non-wheat target onto WHEAT therefore raises the
# season's plantings without raising a single day's plantings: `sum(
# plant_target)` is preserved exactly, so `n_dev`, `animal_want`, every
# placement, the seed room and the labour budget all see the number they saw.
#
# The knobs are a fraction and not a count so the ES can learn them:
# `WHEAT_VOLUME_NUM / WHEAT_VOLUME_DEN` of the non-wheat target moves, in the
# gene's own proportions (largest remainder over the crops it did choose), and
# `plant_target[I_WHEAT] > 0` guards the whole thing -- that is the gene's own
# statement that wheat is live today, carrying `can_mature` and the drain mask
# through from `brain.decide`, so the shift is never invented on a day the gene
# has ruled wheat out and never plants a crop that cannot be harvested by
# `pay_day`.
#
# **It grows the wheat, and it still loses, and it ships off.** Paired over 24
# seeds x 2 seats at seed base 777001 against the shipped champion's own OFF leg
# (four opponents, `--workers 6`, at `NUM/DEN = 1/3`):
#
#     kagg2           95.8% -> 72.9%   paired  -8,870  t -3.36
#     tape 103254816  62.5% -> 45.8%   paired    -968  t -0.38
#     tape 104502967  50.0% -> 41.7%   paired    +215  t +0.05
#     tape 104547425  33.3% -> 12.5%   paired  -9,398  t -2.59
#     ALL (n=192)     60.4% -> 43.2%   paired  -4,755  t -2.83
#
# The mechanism is not in doubt -- over the four kagg2 replays measured both
# ways it does exactly what it was built to do, at no extra plantings a day:
# wheat tiles standing on day 10 rise 3.2 to 9.0, season plantings 76.2 to
# 105.4, harvest 387.5 to 513.6 units, wheat sold 182.6 to 232.9 and the wheat
# line's net of its own purchases 1,938 to 4,690 coins.
#
# What it does not price is that **wheat is a shared market and the herd's
# products are not.** The coin split over the 192 games is our own coins -2,312
# a game against the opponents' +2,443: every tile the mix takes off strawberry
# or tomato is a unit off a line we sell into a curve of our own, and every
# wheat unit it adds walks the one curve both seats quote off -- so it hands the
# opponent a cheaper feed bill at the same time as it thins our own basket.
# `PLANT_FILL_ON`'s v2 note said any third cut has to price the route it
# displaces; this one says the mix has to price the *market* it displaces into,
# and the day's grow score (`brain.decide`) is where that belongs, not here.
#
# OFF, `_wheat_mix` is never called and `macro.plant_target` reaches `_derive`
# exactly as `brain.decide` wrote it, byte for byte
# (`tests/test_wheat_volume.py`).
WHEAT_VOLUME_ON = False
#: Fraction of the day's non-wheat plant target that moves onto WHEAT.
WHEAT_VOLUME_NUM = 1
WHEAT_VOLUME_DEN = 3


def _take_lr(xp, v, cap):
    """int[5]: `v` cut down to `cap` tiles in its own proportions.

    `_fill_plant`'s largest remainder without the `max(cap, sum)` floor, so it
    scales down instead of up: `sum(_take_lr(v, cap)) == cap` exactly for any
    `0 <= cap <= sum(v)`, and `sum(v) == 0` returns `v` (the numerator is zero
    and so is `cap`, which is what makes the caller safe on a day the gene
    planted nothing). Integer throughout -- `v` and `cap` are both bounded by
    the 100 tiles of the board, so `v * cap` stays under 10,000 -- and the
    tie-break is the repo's usual pairwise compare, higher remainder first and
    exact ties to the lower crop index.
    """
    i32 = xp.int32
    t = v.astype(i32)
    den = xp.maximum(xp.sum(t, dtype=i32), 1)
    num = t * xp.asarray(cap).astype(i32)
    q = num // den
    rem = num - q * den
    extra = xp.asarray(cap).astype(i32) - xp.sum(q, dtype=i32)
    j = xp.arange(spec.N_CROPS, dtype=i32)
    ahead = xp.sum(((rem[None, :] > rem[:, None])
                    | ((rem[None, :] == rem[:, None]) & (j[None, :] < j[:, None]))
                    ).astype(i32), axis=1, dtype=i32)
    return (q + (ahead < extra).astype(i32)).astype(i32)


def _wheat_mix(xp, macro: Macro) -> Macro:
    """`macro` with `plant_target` re-weighted onto WHEAT [SWITCH].

    `NUM/DEN` of the non-wheat tiles move; the crops that keep theirs keep them
    in the proportions the softmax chose. The total is preserved by
    construction -- the tiles WHEAT gains are exactly the tiles `_take_lr` did
    not keep -- which is the whole point: this is a mix change and not a
    development change, so nothing that reads `sum(plant_target)` moves.
    """
    i32 = xp.int32
    t = macro.plant_target.astype(i32)
    is_w = (xp.arange(spec.N_CROPS, dtype=i32) == spec.I_WHEAT).astype(i32)
    others = (t * (1 - is_w)).astype(i32)
    tot = xp.sum(others, dtype=i32)
    keep = ((tot * (WHEAT_VOLUME_DEN - WHEAT_VOLUME_NUM))
            // WHEAT_VOLUME_DEN).astype(i32)
    kept = _take_lr(xp, others, keep)
    moved = (tot - xp.sum(kept, dtype=i32)).astype(i32)
    mix = (kept + is_w * (t[spec.I_WHEAT] + moved)).astype(i32)
    return macro._replace(
        plant_target=xp.where(t[spec.I_WHEAT] > 0, mix, t).astype(i32))


# ---- CROP-SCARCE: price the mix at the day the tile sells [SWITCH, OFF] ----
#
# WHAT IS MISSING. `brain.decide` picks the day's crop mix from a softmax over
# the head's per-product `grow` score (`brain.py:1048-1064`), and the only
# price the head ever sees is the **dawn quote**: `price / base` and
# `(inv - I0) / T`, hour 0, today (`brain.py:552-553`). Two hard gates follow
# it -- `can_mature` and `absorb` (`brain.py:1080`, `:1122`) -- and both are
# quantity tests, not price tests. The *money* the planner has for a seed is
# priced somewhere else entirely: `_candidates` walks the k-th planting's
# units down the **sales-window** curve, the hour-0 inventory drained forward
# to that crop's own first-yield day plus every unit this farm has already
# committed (`plan.py:6919-6935`). So the tree already computes what a crop
# will fetch on the day its tile sells -- and the mix never reads it. The
# budget can only *refuse* a want the mix already sized; it can never move a
# tile from a crop that will be cheap to one that will be dear.
#
# WHY IT MIGHT MATTER (`docs/strategy/2026-09-16-cropmix.md` sect.2, 20
# replays of M & M & P & Q, both seats, 2,360 crop-days). The dawn level is a
# good forecast of the first-yield-day level for the two fast crops and a poor
# one for the slow ones -- `r(now, fut)` WHEAT 0.91, CARROT 0.95, TOMATO 0.63,
# MELON 0.68, STRAWBERRY **-0.18** -- and the *mean* moves as well as the
# rank: MELON is planted at 0.94 of base and harvested at **0.64**, while
# STRAWBERRY goes 1.45 -> 1.55 and TOMATO 1.07 -> 1.16. A mix that reads the
# dawn quote is systematically long the crop whose price is about to fall.
#
# WHAT THIS DOES. One multiplicative, bounded re-share of `plant_target` by
# `fwd / spot` per crop -- the forward quote the budget already trusts over
# the dawn quote the head already saw -- and nothing else:
#
#   * `fwd / spot`, not `fwd / base`: the *level* is already an input to the
#     head, so re-weighting on it would double-count a signal the policy is
#     trained on. The ratio is the part of the forward quote the head cannot
#     see, and it is exactly 1.0 on a market that will not move.
#   * clipped to [`CROP_SCARCE_LO`, `CROP_SCARCE_HI`] / `CROP_SCARCE_ONE` =
#     [0.75, 1.33], so no crop's share can move by more than a third
#     relatively. This is the one lesson of `PLANT_MIX_DRAIN_ON`, which put a
#     raw `share` logit of order 1 against a learned sharpness of order 1 and
#     lost -11,906 at t = -15.4 (`brain.py:876-891`): "a gain an order of
#     magnitude smaller is the only version of this worth another run".
#   * `t * ratio`, so a crop the softmax, `can_mature` or `absorb` zeroed
#     stays at zero. The gate can re-rank what the brain asked for; it can
#     never invent a crop the brain ruled out.
#   * `_take_lr` against `sum(plant_target)`, so the total is preserved to the
#     tile: this is a MIX change and not a development change, and nothing
#     that reads `sum(plant_target)` -- `n_dev`, `animal_want`, `_seed_room`,
#     the land valuation -- moves at all.
#
# NOT `OPP_SUPPLY_ON` and not `OPP_MIX_ON`. Both of those put the *other
# seat's* stream into the curve and both were refused (`plan.py:1810-1829`,
# 192 paired boards, -2,972 at t -3.80, dose-responsive). This reads only the
# town's own drain and this farm's own committed pipeline -- the identical
# expression `ANIMAL_BUY_FWD_ON` and `CARE_HOLD_ON` already read.
#
# OFF, `_crop_scarce` is never called: the branch in `_plan_and_stats` is a
# Python `if` on a module global, so the shipped program is the one it was,
# byte for byte (`tests/test_cropmix.py` pins the whole-plan sha256).
CROP_SCARCE_ON = False
#: Fixed-point unit of the forward/spot ratio. 64 is a 1.6 % resolution on a
#: quantity that is clipped to a 0.58-wide band, and keeps `t * ratio * cap`
#: (<= 100 * 85 * 100) three orders of magnitude inside int32.
CROP_SCARCE_ONE = 64
#: Clip band on the ratio, 0.75x to 1.33x. Deliberately narrow: see above.
CROP_SCARCE_LO = 48
CROP_SCARCE_HI = 85


def _crop_scarce(xp, view, macro: Macro, price_table) -> Macro:
    """`macro` with `plant_target` re-shared by the forward/spot ratio [SWITCH].

    `sum(plant_target)` is preserved exactly by `_take_lr`, and a crop at zero
    stays at zero, so the two gates above this one (`can_mature`, `absorb`)
    remain the last word on what may be planted at all.
    """
    i32 = xp.int32
    t = macro.plant_target.astype(i32)
    tot = xp.sum(t, dtype=i32)
    is_plant = view.kind == spec.KIND_PLANT
    has_animal = (((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE))
                  & (view.occ >= 0))
    inv_h = (PJ.inv_at_day(xp, view.mkt_inv, view.shops, xp.asarray(_FIRST_P),
                           view.day)
             + _pipeline_units(xp, view, is_plant, has_animal, view.day))
    idx = xp.clip(inv_h - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    fwd = xp.take_along_axis(price_table, idx[:, None], axis=1)[:, 0]
    spot = xp.maximum(view.price.astype(i32), 1)
    ratio = xp.clip((fwd[:spec.N_CROPS].astype(i32) * CROP_SCARCE_ONE)
                    // spot[:spec.N_CROPS],
                    CROP_SCARCE_LO, CROP_SCARCE_HI).astype(i32)
    mix = _take_lr(xp, (t * ratio).astype(i32), tot)
    return macro._replace(plant_target=xp.where(tot > 0, mix, t).astype(i32))


def _melon_open(xp, view, macro: Macro) -> Macro:
    """`macro` with the opening day's plant mix rebalanced onto MELON [SWITCH].

    Only `MELON_OPEN_DAY` is touched and only `plant_target` changes: MELON is
    raised to `min(MELON_OPEN_TILES, plant_total)` and the tiles it gains come
    off the other crops in `_MELON_PAY_RANK` order -- crop order with WHEAT
    last -- so `sum(plant_target)`, the number the day's whole tile, seed and
    labour budget is sized against, is preserved exactly and the wheat is the
    last thing the opening spends.  The switch can only ever *raise* melon: a
    day the network already wants more melon than the knob asks for keeps its
    own mix.

    See the `MELON_OPEN_ON` block for what the pay order is worth: v2 paid in
    plain crop order, wheat paid first, and the opening bought itself out of
    the feed and the rotation.
    """
    i32 = xp.int32
    tgt = macro.plant_target.astype(i32)
    total = xp.sum(tgt, dtype=i32).astype(i32)
    is_melon = xp.arange(spec.N_CROPS, dtype=i32) == spec.I_MELON
    others = xp.where(is_melon, 0, tgt).astype(i32)
    debt = xp.maximum(xp.minimum(xp.asarray(open_tiles(), i32), total)
                      - tgt[spec.I_MELON], 0).astype(i32)
    # What the crops ahead of `c` in the pay order have already given up. A
    # pairwise compare rather than a cumsum, because the order is a
    # permutation of crop order and both backends have to agree on it.
    rank = xp.asarray(_MELON_PAY_RANK)
    paid = xp.sum(xp.where(rank[None, :] < rank[:, None], others[None, :], 0),
                  axis=1, dtype=i32).astype(i32)
    give = xp.clip(debt - paid, 0, others).astype(i32)
    mix = xp.where(is_melon, tgt[spec.I_MELON] + xp.sum(give, dtype=i32),
                   others - give).astype(i32)
    return macro._replace(
        plant_target=xp.where(view.day == MELON_OPEN_DAY, mix, tgt).astype(i32))


def _melon_plate(xp, view, macro: Macro) -> Macro:
    """`macro` with `MELON_PLATE_DAY`'s mix rebalanced onto MELON [MELONGENES].

    The same rewrite `_melon_open` performs, with the tile count and the day
    read from the two programmable floats instead of the package's constants:
    MELON is raised to `min(MELON_PLATE_TILES, plant_total)`, the tiles come off
    the other crops in `_MELON_PAY_RANK` order (wheat last), `sum(plant_target)`
    is preserved exactly, and a day whose own mix already wants more melon keeps
    it.  Nothing else is touched -- no dump day, no excursion, no crew floor --
    so the plate composes with every shipped switch.
    """
    i32 = xp.int32
    tgt = macro.plant_target.astype(i32)
    total = xp.sum(tgt, dtype=i32).astype(i32)
    is_melon = xp.arange(spec.N_CROPS, dtype=i32) == spec.I_MELON
    others = xp.where(is_melon, 0, tgt).astype(i32)
    want = xp.asarray(int(MELON_PLATE_TILES), i32)
    debt = xp.maximum(xp.minimum(want, total) - tgt[spec.I_MELON], 0).astype(i32)
    rank = xp.asarray(_MELON_PAY_RANK)
    paid = xp.sum(xp.where(rank[None, :] < rank[:, None], others[None, :], 0),
                  axis=1, dtype=i32).astype(i32)
    give = xp.clip(debt - paid, 0, others).astype(i32)
    mix = xp.where(is_melon, tgt[spec.I_MELON] + xp.sum(give, dtype=i32),
                   others - give).astype(i32)
    mp_on = view.day == int(MELON_PLATE_DAY)
    if NONV_PLATE_LAST is not None:  # [SWITCH, NONV2] the rewrite on every day DAY..LAST
        mp_on = (view.day >= int(MELON_PLATE_DAY)) & (view.day <= int(NONV_PLATE_LAST))
    return macro._replace(
        plant_target=xp.where(mp_on, mix, tgt).astype(i32))


def _melon_deny_plate(xp, view, macro: Macro) -> Macro:
    """Rebalance the d0..2 crop mix onto the requested MELON plate."""
    i32 = xp.int32
    tgt = macro.plant_target.astype(i32)
    total = xp.sum(tgt, dtype=i32).astype(i32)
    is_melon = xp.arange(spec.N_CROPS, dtype=i32) == spec.I_MELON
    others = xp.where(is_melon, 0, tgt).astype(i32)
    want = xp.asarray(int(MELON_DENY_PLATE), i32)
    debt = xp.maximum(xp.minimum(want, total) - tgt[spec.I_MELON], 0).astype(i32)
    rank = xp.asarray(_MELON_PAY_RANK)
    paid = xp.sum(xp.where(rank[None, :] < rank[:, None], others[None, :], 0),
                  axis=1, dtype=i32).astype(i32)
    give = xp.clip(debt - paid, 0, others).astype(i32)
    mix = xp.where(is_melon, tgt[spec.I_MELON] + xp.sum(give, dtype=i32),
                   others - give).astype(i32)
    early = (view.day >= 0) & (view.day <= 2)
    return macro._replace(plant_target=xp.where(early, mix, tgt).astype(i32))


#: Width of `_residual_features`. `S/actionrl/head.py::N_FEAT` must match, and
#: a head trained against a different width is a different head.
RESIDUAL_N_FEAT = 64
PROGRAM_N_FEAT = 115
#: [SWITCH, RIVALPURSE1] feature 2 (rival purse) reads the real public rival
#: purse `view.program_opp_money`. OFF = `view.opp_money`, which both the
#: engine parse and the simulator fill only under `SELL_SLOT_MIRROR_GATE_ON`,
#: so every head trained before RIVALPURSE1 (head_940 included) saw 0 there.
RESIDUAL_RIVAL_PURSE_ON = False


def _residual_features(xp, view):
    """float32[RESIDUAL_N_FEAT]: everything the head is allowed to see.

    **Whole-array reductions only** [LAW, `brain.PolicyObs`]: the tile arrays
    carry no canonical order -- the simulator hands the head raw board order
    and the submission hands it serpentine `DayView` order -- so anything that
    indexed a per-tile table here would read a different board in training
    than in the package, a silent train/serve divergence rather than an error.
    Counting `occ == c` over the whole board is order-free; `SERP_QUAD[i]` is
    not, and must never appear below.

    The list is ACTIONRL1 section 4's: day, both purses, both boards' standing
    commitment, shed, seeds, `mkt_inv`, `price`, `shops`. Scales are fixed
    constants (not batch statistics) so the package computes the same vector
    the trainer did.
    """
    f32 = xp.float32
    kind = view.kind
    occ = view.occ
    is_pl = kind == spec.KIND_PLANT
    is_an = ((kind == spec.KIND_COOP) | (kind == spec.KIND_PASTURE)) & (occ >= 0)
    crop = [xp.sum((is_pl & (occ == c)).astype(f32)) / 20.0
            for c in range(spec.N_CROPS)]
    animal = [xp.sum((is_an & (occ == a)).astype(f32)) / 10.0
              for a in range(spec.N_ANIMALS)]
    n_free = xp.sum((kind == spec.KIND_EMPTY).astype(f32)) / 40.0
    parts = [
        xp.reshape(xp.asarray(view.day, f32) / 29.0, (1,)),
        xp.reshape(xp.asarray(view.money, f32) / 1e4, (1,)),
        xp.reshape(xp.asarray(view.program_opp_money
                              if RESIDUAL_RIVAL_PURSE_ON else view.opp_money,
                              f32) / 1e4, (1,)),
        xp.stack(crop),
        xp.stack(animal),
        xp.reshape(n_free, (1,)),
        view.shed.astype(f32) / 50.0,
        view.seeds.astype(f32) / 20.0,
        view.mkt_inv.astype(f32) / float(spec.MARKET_I0),
        view.price.astype(f32) / 300.0,
        view.shops.astype(f32),
        view.opp_commit.astype(f32) / 20.0,
    ]
    feats = xp.concatenate([xp.reshape(p, (-1,)) for p in parts])
    assert feats.shape == (RESIDUAL_N_FEAT,), feats.shape
    return feats.astype(f32)


def _standing_yield(xp, kind, occ, tile_yield):
    """Public standing yield per product; whole-board and order invariant."""
    f32 = xp.float32
    out = []
    for product in range(spec.N_PRODUCTS):
        crop = ((kind == spec.KIND_PLANT) & (occ == product)
                if product < spec.N_CROPS else xp.zeros_like(kind, dtype=bool))
        animals = xp.zeros_like(kind, dtype=bool)
        for animal in range(spec.N_ANIMALS):
            if int(spec.ANIMAL_PRODUCT[animal]) == product:
                animals = animals | (((kind == spec.KIND_COOP)
                                      | (kind == spec.KIND_PASTURE))
                                     & (occ == animal))
        out.append(xp.sum(xp.where(crop | animals, tile_yield, 0),
                          dtype=f32))
    return xp.stack(out).astype(f32)


def program_selector_features(xp, view):
    """float32[115] public dawn features for the complete-program selector.

    The first 64 values are the frozen head vector byte-for-byte.  The rest
    are actual rival purse and purse difference, crop-age histograms for both
    farms (crop-major, age bins 0--2/3--5/6+), standing yields for both farms
    in product order, and learner seat.  Every tile operation is a reduction,
    so simulator raw order and submission serpentine order are equivalent.
    """
    f32 = xp.float32

    def ages(kind, occ, planted):
        age = xp.asarray(view.day) - planted
        vals = []
        for crop in range(spec.N_CROPS):
            live = (kind == spec.KIND_PLANT) & (occ == crop)
            vals.extend((
                xp.sum((live & (age <= 2)).astype(f32)),
                xp.sum((live & (age >= 3) & (age <= 5)).astype(f32)),
                xp.sum((live & (age >= 6)).astype(f32)),
            ))
        return xp.stack(vals).astype(f32) / 20.0

    legacy = _residual_features(xp, view)
    money = xp.stack((xp.asarray(view.program_opp_money, f32) / 1e4,
                      (xp.asarray(view.money, f32)
                       - xp.asarray(view.program_opp_money, f32)) / 1e4))
    parts = (
        legacy, money,
        ages(view.kind, view.occ, view.t_day),
        ages(view.opp_kind, view.opp_occ, view.opp_t_day),
        _standing_yield(xp, view.kind, view.occ, view.t_yield) / 50.0,
        _standing_yield(xp, view.opp_kind, view.opp_occ,
                        view.opp_t_yield) / 50.0,
        xp.reshape(xp.asarray(view.seat, f32), (1,)),
    )
    feats = xp.concatenate([xp.reshape(p, (-1,)) for p in parts])
    assert feats.shape == (PROGRAM_N_FEAT,), feats.shape
    return feats.astype(f32)


def _residual_pref_crop(xp, t):
    """int32[5] one-hot on the crop the day already wants most [ACTIONRL11].

    Ties to the LOWER crop index, by first-occurrence over the equality mask --
    no argmax scatter, so it reads the same on both backends. This is the
    "planner's preferred crop" `ask_fill` pours its tiles into: the fill is a
    VOLUME move, not a mix move, and inventing a crop the gene ruled out is the
    thing `_fill_plant` refuses on purpose (CARROTBID: tile reallocation gifts
    thousands). On a day whose ask is all zero there is no preferred crop and
    `_residual_override` refuses the fill outright, for the same reason.
    """
    i32 = xp.int32
    t = t.astype(i32)
    hit = (t == xp.max(t)).astype(i32)
    first = xp.cumsum(hit, dtype=i32) == 1
    return (hit * first.astype(i32)).astype(i32)


def _residual_override(xp, view, macro: Macro):
    """`(macro, d_hire, d_seed)` with the head's clamped nudges written in.

    Splice site, after the whole `_sw_macro` mix chain and before `day` is read
    [ACTIONRL1 section 1]: `_derive`'s two passes, `_wants`, `plant_eff`,
    `plant_crop`, `_place_split`, the seed room, the land valuation, the budget
    grant, the cash reserve, `_routes` and `_market` all run BELOW this line
    and all re-derive off the rewritten `Macro`, so no invariant is carried
    across it. The one field the head touches that is not a `Macro` field is
    the crew, and that is returned rather than applied: the hire count is an
    enumerated argmax further down and clamping `n_hire` after `:10013` would
    desync the bill, the reserve and the route base.

    Every clamp is re-asserted here, not trusted from the net:
      * `d_plant` is clipped to +-4 and the result floored at 0, on days
        `>= RESIDUAL_FIRST_DAY` only (day 0 is the pinned opening);
      * `d_animal` is clipped to +-2 and floored at 0;
      * `hold` is scaled by `hold_num/2` in integer arithmetic, so it stays a
        non-negative int and `hold_num == 2` is the identity;
      * `d_hire` is clipped to +-2 here and to the affordable prefix below.

    [ACTIONRL11] A "wide" override dict carries two more keys and `d_seed` is
    the third return value. The switch is `"ask_fill" in o`, a PYTHON `in` on
    the dict the head returned, so under the v1 layout none of the wide block
    is traced and the expression is the shipped one, byte for byte; `d_seed` is
    then `None` and `_derive` never sees the seed channel either.

      * `ask_fill` is a FLOOR on the day's TOTAL ask: `k/4 * n_free` tiles,
        poured into `_residual_pref_crop`, clipped to `n_free`, on days
        `>= RESIDUAL_ASK_DAY0` and only when the day already wants something.
        `n_free` is the hour-0 empty-tile count -- the same order-free
        whole-board reduction `_residual_features` shows the head, and the
        conservative one (a bought quadrant's tiles are added further down at
        the grant, never here). Over-asking is the designed, silently-absorbed
        failure mode (`_fill_cap`, `plant_eff = min(fill_target, seeds + ...)`).
      * `seed_buy` is carried down like `d_hire`, for the same reason: the
        seed row is granted by the budget walk hundreds of lines below, and a
        seed count written here would not be paid for.
    """
    i32 = xp.int32
    fields = dict(macro._asdict())
    fields["day"] = view.day
    fields["program_features"] = program_selector_features(xp, view)
    o = RESIDUAL_FN(_residual_features(xp, view), fields)
    wide = "ask_fill" in o

    d_plant = xp.clip(xp.asarray(o["d_plant"], i32),
                      -(RESIDUAL_PLANT_MAX_WIDE if wide else RESIDUAL_PLANT_MAX),
                      RESIDUAL_PLANT_MAX_WIDE if wide else RESIDUAL_PLANT_MAX
                      ).astype(i32)
    tgt = macro.plant_target.astype(i32)
    moved = xp.maximum(tgt + d_plant, 0).astype(i32)
    plant_target = xp.where(view.day >= RESIDUAL_FIRST_DAY, moved, tgt).astype(i32)

    d_seed = None
    if wide:
        n_free = xp.sum((view.kind == spec.KIND_EMPTY).astype(i32),
                        dtype=i32).astype(i32)
        af = xp.clip(xp.asarray(o["ask_fill"], i32), 0, RESIDUAL_ASK_STEPS).astype(i32)
        tot = xp.sum(plant_target, dtype=i32).astype(i32)
        floor_t = xp.minimum(n_free * af // RESIDUAL_ASK_STEPS, n_free).astype(i32)
        live = ((af > 0) & (tot > 0)
                & (view.day >= RESIDUAL_ASK_DAY0)
                & (view.day >= RESIDUAL_FIRST_DAY))
        extra = xp.where(live, xp.maximum(floor_t - tot, 0), 0).astype(i32)
        plant_target = (plant_target
                        + _residual_pref_crop(xp, plant_target) * extra).astype(i32)
        d_seed = xp.clip(xp.asarray(o["seed_buy"], i32),
                         0, RESIDUAL_SEED_MAX).astype(i32)

    d_animal = xp.clip(xp.asarray(o["d_animal"], i32),
                       -RESIDUAL_ANIMAL_MAX, RESIDUAL_ANIMAL_MAX).astype(i32)
    animal_want = xp.maximum(macro.animal_want.astype(i32) + d_animal, 0).astype(i32)

    # {0, .5, 1} without leaving int32: `hold` is a coin count, and a float
    # reservation would round differently on the two backends.
    num = xp.clip(xp.asarray(o["hold_num"], i32), 0, 2).astype(i32)
    hold = xp.maximum(macro.hold.astype(i32) * num // 2, 0).astype(i32)

    d_hire = xp.clip(xp.asarray(o["d_hire"], i32),
                     -(RESIDUAL_HIRE_MAX_WIDE if wide else RESIDUAL_HIRE_MAX),
                     RESIDUAL_HIRE_MAX_WIDE if wide else RESIDUAL_HIRE_MAX).astype(i32)
    return macro._replace(plant_target=plant_target, animal_want=animal_want,
                          hold=hold), d_hire, d_seed


def _residual_seed_extra(xp, seed_buy, costs, n_buy, purse, fill_target, seeds,
                         d_seed):
    """`(seed_buy, spent)`: the grant's seed row topped up by `d_seed` units.

    [ACTIONRL11] The same shape as `_rebuy_extra`'s wheat re-buy, and for the
    same reason: the budget walk has already ranked and paid for what it wants,
    so an extra unit must be charged the price the row's LATER slots really
    meet (`costs` is the per-list quote curve the grant itself walked) and paid
    out of what the walk LEFT, never out of the reserve. A crop is topped up
    only where the day is actually short -- `fill_target` above what the seeds
    in hand plus the granted buy can plant -- because `plant_eff = min(
    fill_target, seeds + seed_buy)` and a unit past that is dead money.

    The crops are walked in index order and each one's spend is deducted before
    the next is priced, so the answer is deterministic and the purse is never
    double-spent. `d_seed` is already clipped to `RESIDUAL_SEED_MAX`.
    """
    i32 = xp.int32
    k = xp.clip(xp.asarray(d_seed, i32), 0, RESIDUAL_SEED_MAX).astype(i32)
    left = xp.maximum(purse - BUD.spend(xp, costs, n_buy), 0).astype(i32)
    j = xp.arange(PJ.K, dtype=i32)
    spent = xp.asarray(0, i32)
    out = []
    for c in range(spec.N_CROPS):
        row = xp.maximum(costs[BUD.L_SEED0 + c].astype(i32), 1).astype(i32)
        cum = xp.cumsum(row, dtype=i32)
        n0 = xp.clip(seed_buy[c].astype(i32), 0, PJ.K).astype(i32)
        base = xp.where(n0 > 0, cum[xp.clip(n0 - 1, 0, PJ.K - 1)], 0).astype(i32)
        short = xp.maximum(fill_target[c].astype(i32)
                           - (seeds[c].astype(i32) + n0), 0).astype(i32)
        want = xp.minimum(xp.minimum(k, short), PJ.K - n0).astype(i32)
        n_aff = xp.sum(((j >= n0) & (cum - base <= left)).astype(i32),
                       dtype=i32).astype(i32)
        take = xp.clip(xp.minimum(want, n_aff), 0, PJ.K - n0).astype(i32)
        cost = xp.where(take > 0,
                        cum[xp.clip(n0 + take - 1, 0, PJ.K - 1)] - base,
                        0).astype(i32)
        left = xp.maximum(left - cost, 0).astype(i32)
        spent = (spent + cost).astype(i32)
        out.append((n0 + take).astype(i32))
    return xp.stack(out).astype(i32), spent


def _residual_hire(xp, h_star, d_hire, affords):
    """The enumeration's argmax, nudged by `d_hire` and re-clipped to the
    affordable prefix -- `min(h_star + d_hire, max affordable)` [ACTIONRL].

    The same arithmetic `MACRO_EXEC` site 5 uses (`:9996-10006`): `HIRE_BILLS`
    is non-decreasing in `h`, so `afford` is a prefix and counting its members
    under the ask IS the clip. Affordability is the one thing no head repeals:
    a crew the purse cannot field and re-field tomorrow ends the season
    (`test_cash_reserve.py`).
    """
    i32 = xp.int32
    ask = xp.clip(h_star.astype(i32) + d_hire, 0, spec.MAX_HANDS).astype(i32)
    ok = xp.stack([xp.logical_and(affords[h], xp.asarray(h, i32) <= ask).astype(i32)
                   for h in range(1, spec.MAX_HANDS + 1)])
    return xp.sum(ok, axis=0, dtype=i32).astype(i32)


def _mirror_crew(xp, view, macro: Macro) -> Macro:
    """`macro` with the opening window's crew floor written in [SWITCH].

    Only `crew_target` changes and only on days 0-`MIRROR_LAST_DAY`, and it is
    a FLOOR: a day whose own ramp already asks for more keeps its own number.
    `crew_target` is the hire enumeration's ramp channel -- every hand up to it
    is worth `CREW_TARGET_PUSH` coins, which beats its own marginal fib bill,
    so the argmax walks up to the floor and stops.  It is not a forced hire:
    the affordability test and the reserve are still the planner's, so a day
    that cannot pay the bill still hires what it can.  That is deliberate --
    the FORWARD_ADMIT postmortem's failure mode was a FORCED board the crew
    then could not work, and this switch's whole claim is the other direction
    (carry the crew, keep the output that pays for the melon plate).
    """
    i32 = xp.int32
    want = xp.asarray(MIRROR_HANDS_D0_9, i32)
    tgt = xp.asarray(macro.crew_target, i32)
    return macro._replace(
        crew_target=xp.where(mirror_window(xp, view.day),
                             xp.maximum(tgt, want), tgt).astype(i32))


def _mirror_wheat_ask(xp, day):
    """int32: the package's extra WHEAT units on `day` [SWITCH]."""
    return xp.where(mirror_window(xp, day), xp.int32(MIRROR_WHEAT_BUY),
                    xp.int32(0))


# `MACRO_EXEC_ON` [SWITCH]: execute a per-day macro schedule instead of the
# day's own enumeration.
#
# Why it exists. The FORWARD_ADMIT postmortem (build story 2026-09-09) showed
# that the top files' opening is unreachable from our planner *as a plan*, not
# as a preference: hire enumeration prices hands against TODAY's derived task
# set, and a melon tile emits no task until `CROP_WINDOW_START`, so forcing the
# top's board collapses the crew to 0-1 while the top hires four on day 1.
# `FORWARD_ADMIT_ON` lifted the crew to 2/3/3 and still lost, because "the
# top's ramp is hands, animals and tiles bought together; the animal budget and
# the plant cap do not see the projection". This switch is the executability
# experiment that follows from that sentence: give the planner the whole ramp
# as data -- hands, animals and tiles per day -- and measure whether the
# machinery can put it on the board at all. It is an EXECUTOR, not a strategy:
# no fitness term, no gene, no claim that the schedule is good.
#
# Four sites, and only four:
#   1. `_macro_targets` rewrites `plant_target` and `animal_want` AFTER every
#      other mix rewrite, so the schedule is the last word on the mix, and the
#      `plant_total = n_dev - sum(animal_want)` coupling (`brain.py:992`) that
#      made an unexecuted animal want cost tiles (`2026-09-14-herd-growth-
#      screen.md` §3) cannot reach the schedule's tiles.
#   2. `_derive`'s land gate takes `land_target[day]` when the schedule has
#      one, since tiles the farm does not own cannot be planted.
#   3. `_derive` scales the three animal lists' candidate values so the shared
#      `budget.grant` walk serves the herd ahead of the seed lists -- the
#      exact displacement `2026-09-14-melon-animal-mechanism.md` §3 traced
#      (twelve melon seeds at 80 outranking a 500-coin SHEEP inside one greedy).
#   4. `_plan_and_stats` replaces the hire argmax with `hands_target[day]`,
#      clipped to the largest crew the purse can field and still re-field
#      tomorrow -- the affordability test the enumeration already applies.
#
# OFF, every one of the four sites is the branch it always took: the module
# globals below are read only inside `if MACRO_EXEC_ON:` and the schedule is
# `None` until `macro_load` is called.
MACRO_EXEC_ON = False
#: Environment variable naming the schedule JSON (`S/macro_exec/extract.py`
#: writes it). Read once by `macro_load`; never read at import time, so an
#: unset environment and an OFF switch are the same program.
MACRO_ENV = "KAGG3_MACRO_JSON"
#: Multiplier on the animal lists' candidate values inside the shared greedy
#: when the schedule is executing. Large enough that the dearest animal
#: outranks the dearest seed on value per coin, clipped to `BUD.VALUE_CAP`.
MACRO_ANIMAL_PRIORITY = 64
#: The decoded schedule: `None`, or a dict of numpy arrays
#: `hands[ND] anim[ND,N_ANIMALS] tiles[ND,N_CROPS] land[ND]`.
MACRO_SCHEDULE = None
#: [SWITCH, MACRO_EXEC] Which of the six sites fire while `MACRO_EXEC_ON` is
#: True. `"full"` is the original executor and the EXEC-SCOPE gate's subject:
#: the schedule is the whole development plan, calendar included, and it lost
#: -37,821 coins/board to B because a fixed per-day planting calendar
#: desynchronises from our own harvest cadence (44 idle tiles at dawn d10
#: against B's 1.1; `docs/strategy/2026-09-14-macro-exec.md` §4). The other
#: three modes are that report's remaining question -- *what is the ramp worth
#: without the calendar?* -- and each leaves `plant_target` to `brain.decide`,
#: so the tile line stays closed-loop:
#:
#:   "full"            sites 1-6; site 1 writes `plant_target` AND `animal_want`
#:   "hands"           sites 5, 6 only: the crew is the schedule's, nothing else
#:   "hands_herd"      sites 1, 3, 4, 5, 6, site 1 writing `animal_want` ONLY
#:   "hands_herd_land" "hands_herd" + site 2 (the land calendar)
#:
#: MACRO-CHANNELS adds three herd-as-a-FLOOR modes and three sale-timing ones.
#: MACRO-RAMP §5.2 found the herd ceiling to be a build defect rather than a
#: finding: site 1 wrote `animal_want` on all 30 days, including the 24 the
#: schedule says nothing about, so the schedule silenced B's own herd growth
#: (B reaches 17.0 head by d16; under `"hands_herd"` the herd freezes at 5.9
#: from d8) and the -18,645 confounded "the top's opening plate" with "stop
#: growing the herd". The floor modes separate them -- the schedule's row is a
#: LOWER BOUND on the want and the decode keeps whatever it asked for above it:
#:
#:   "herd_floor"       sites 1, 3, 4 with `animal_want = max(decode, sched)`
#:                      and NO hands sites: the herd plate alone
#:   "plate0"           `"herd_floor"` masked to DAY 0 -- d1-29 untouched, the
#:                      executable version of "is the top's day-0 plate free?"
#:   "hands_herd_floor" `"hands"` + `"herd_floor"`
#:   "sell"             site 7 alone: the schedule's sale TIMING, nothing else
#:   "sell_late"        site 7 as a HOLD only -- a lot already at or after the
#:                      schedule's hour keeps its units, so the arm carries the
#:                      delay half of the timing channel and not the pull-
#:                      forward half
#:   "sell_hands"       `"sell"` + `"hands"`
#:
#: SELL-LOT adds three OWN-CLOCK lot modes. MACRO-CHANNELS §6 read a live
#: gradient out of the sale channel's wreckage: `"sell"` lost -1,595 coins on
#: EGG alone by dumping the day's whole egg sale into lot 1, which prices lot
#: placement of a daily-output product at over a thousand coins a board in the
#: WRONG direction. These three arms sweep the same knob in OUR clock -- no
#: schedule hour is read at all, only the mode:
#:
#:   "sheep13"          a SHEEP-STOCK floor on `SHEEP_FLOOR_DAYS` alone: the
#:                      herd sites fire on those days only and ask for
#:                      `SHEEP_FLOOR_N` head of sheep, the decode's own want
#:                      everywhere else. No schedule row is read -- SELL-LOT
#:                      §2 measured the wool gap as PRODUCTION (we sell 100 %
#:                      of what we shear) and two thirds of it as sheep-days
#:                      the top has in d0-9 and we do not, and MACRO-CHANNELS
#:                      §2.2 measured the day-0 version of the same ask
#:                      cash-refused, so the window starts at d1.
#:
#:   "lot1" / "lot2" / "lot3"   every voluntary unit of every product in
#:                      `SELL_LOT_PRODUCTS` resolves on that one lot, with the
#:                      allocator's own QUANTITIES unchanged (the arms move
#:                      volume between lots, they never sell a unit the
#:                      reservation refused). Site 8, so site 7's schedule
#:                      arithmetic is untouched.
#:
#: Set with `setattr` before the first trace, exactly like `MACRO_EXEC_ON`.
#: OFF (`MACRO_EXEC_ON False`) the mode is never read: every site's outer
#: `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:` short-circuits first.
MACRO_MODE = "full"
#: Site -> the modes it fires under. Sites 5 (the hire argmax) and 6 (the
#: `HIRE_ROW_ON` trim, excluded by exclusion) are the ramp itself; they fire
#: under every mode that owns the crew, and MACRO-CHANNELS mode-gates them so
#: a herd-only or sell-only arm leaves the enumeration's crew alone.
MACRO_MODES = ("full", "hands", "hands_herd", "hands_herd_land",
               "herd_floor", "plate0", "hands_herd_floor",
               "sell", "sell_late", "sell_hands",
               "lot1", "lot2", "lot3", "sheep13", "rebuy")
#: The modes whose site 1 writes a FLOOR (`max(decode, schedule)`) instead of
#: the schedule's row whole. `"plate0"` is `"herd_floor"` masked to day 0.
_MACRO_FLOOR = ("herd_floor", "plate0", "hands_herd_floor")
#: The modes that own the crew (sites 5 and 6).
_MACRO_CREW = ("full", "hands", "hands_herd", "hands_herd_land",
               "hands_herd_floor", "sell_hands")
#: The modes that own the herd (sites 1, 3, 4).
#: The sheep-floor mode [SELL-LOT §3]: herd sites, windowed, sheep column.
_MACRO_SHEEP = ("sheep13",)
#: SHEEP's column in the animal vectors (`spec.ANIMALS`), which is not
#: `spec.I_SHEEP` -- that is the ITEM index.
_A_SHEEP = spec.ANIMALS.index("SHEEP")
#: [SELL-LOT, SWITCH] The stock floor `"sheep13"` asks for and the inclusive
#: day window it asks on. Read ONLY inside the herd sites and only while that
#: mode is set, so the shipped path never sees either.
SHEEP_FLOOR_N = 3
SHEEP_FLOOR_DAYS = (1, 3)
#: [SHEEPFIRST1, SWITCH] Force an opening sheep stock target through day 2.
#: ``"swap"`` pays for added sheep by reducing the decoded cow target;
#: ``"add"`` leaves the decoded herd intact.  The OFF branch is host-side, so
#: the shipped graph never reads either parameter.
SHEEP_FIRST_ON = False
SHEEP_FIRST_N = 3
SHEEP_FIRST_MODE = "swap"
#: [WOOLFIRST1, SWITCH] DSM's opening herd: through day 2 the final planner
#: ask is exactly WOOL_FIRST_COWS cows and WOOL_FIRST_SHEEP sheep (geese as
#: decoded); both lanes pass the spot-value gate and are served first by the
#: budget (purse, shed and placement still bind).  WOOL_FIRST_SELL voids the
#: wool reservation on every non-terminal day, so wool sells as produced.
#: OFF is a host-side Python branch: the shipped graph never reads these.
WOOL_FIRST_ON = False
WOOL_FIRST_COWS = 2
WOOL_FIRST_SHEEP = 3
#: d0-2 goose ask under WOOL_FIRST (DSM opens with none; -1 keeps the decoded ask).
WOOL_FIRST_GEESE = 0
WOOL_FIRST_SELL = True
_MACRO_HERD = (("full", "hands_herd", "hands_herd_land")
               + _MACRO_FLOOR + _MACRO_SHEEP)
#: The own-clock lot modes [SELL-LOT]: site 8, and no schedule row at all.
_MACRO_LOT = ("lot1", "lot2", "lot3")
#: [WHEAT-REBUY] The market-PURCHASE channel -- site 9 alone. The schedule's
#: `buy_target[day][WHEAT]` is a LOWER BOUND on the day's turn-1 BUY row, so
#: the feed the decode wanted is still bought and the arm only ever adds the
#: units the tape bought on top. The hour granularity is lost: ymg_aq buys at
#: 22 distinct hours of the day and our market rows exist at turns 0/1/2 and
#: `SELL_TURNS` only, so a day's whole purchase resolves on the turn-1 row
#: (`S/rebuy/PATCH_NEEDED.md`).
_MACRO_BUY = ("rebuy",)
#: [SELL-LOT, SWITCH, default None] Which products the lot modes move. `None`
#: is every product; a tuple of `spec.I_*` indices restricts the arm to those
#: and leaves the allocator's placement for the rest, which is how a
#: per-product profile is read without the cross-product confound. Read ONLY
#: inside site 8, i.e. only while `MACRO_EXEC_ON` and a lot mode are both set,
#: so the shipped path never sees it.
SELL_LOT_PRODUCTS = None
#: [WHEAT-REBUY, SWITCH, default OFF] The own-clock re-buy arm: buy `REBUY_N`
#: extra units of market WHEAT on the day's turn-1 BUY row, on every day in
#: the inclusive window `REBUY_DAYS`, over and above the feed the budget walk
#: granted. Nothing sells them here -- they sit in the shed overnight and
#: tomorrow's `avail` (`view.shed`, hour 0, less the feed reservation) offers
#: them to the lot allocator at the day's best lot like any other stock, which
#: is the whole arm: *does a round trip through the shared pot pay?*
#:
#: Read ONLY inside `if REBUY_ON:`, so with the switch off (the shipped state)
#: the expression at the site is the one it always was, `MACRO_EXEC_ON` or
#: not. Set with `setattr` before the first trace like every other switch.
REBUY_ON = False
REBUY_N = 0
REBUY_DAYS = (10, 25)
#: [LOT-DEPTH, SWITCH, default OFF] Cap the units of ONE product that may
#: stand in ONE sell lot, and spread what the cap refuses over the day's other
#: lots.
#:
#: WHY. Every one of the nine products quotes off `25 + amp * f(I0 - inv)`
#: with `f` monotone (`spec.py:111-169`), so a SELL of `q` units walks its own
#: quote DOWN unit by unit (`sim/market.py:69-76`, `_quotes`: `off = +j`) --
#: the walking-price structure is universal, fertilizer's linear shape
#: included. A lot is ONE market order of `lots[l][p]` units (`_market`), so a
#: lot's depth is exactly what it costs itself. `SELL.allocate` already prices
#: that walk (`adjusted_marginals`' `nxt`), but it also charges `press *
#: lot_index` and the whole later-lot externality to the earlier lot, and a
#: large decoded `press` collapses the day into lot 1 whatever the walk says.
#: This switch is the counter-experiment: force the spread and pay whatever
#: the pressure term was buying.
#:
#: WHAT IT MOVES, AND WHAT IT DOES NOT. Only the VOLUNTARY allocation, and
#: only its shape: `s_qty` (the day's total per product) is identical before
#: and after, so the shed-overflow deficit, the forced sale, the prestock
#: projection and every bulk add downstream (`DROP_ON`, `MELON_OPEN_ON`,
#: `MIDDAY_PLACE_V2_ON`, `SAME_DAY_FERT_ON`, `BANK_BEFORE_LOT_ON`,
#: `ANIMAL_SAME_DAY_ON`, `SHED_OVERFLOW_ON`) see the numbers they always saw
#: and place their own units where they always placed them -- which is also
#: why those bulk adds can still stand a lot above the cap. No unit is ever
#: dropped: what does not fit under the cap anywhere (a liquidation of more
#: than `N_LOTS * LOT_SPLIT_MAX` units) rides the LAST lot, the one the town
#: has drained furthest.
#:
#: `LOT_SPLIT_MAX` is units per lot per product; `<= 0` is "no cap" and the
#: switch is inert. `LOT_SPLIT_DAYS` is the days the cap applies on -- `()`
#: is every day, `(29,)` is the terminal liquidation alone. Read ONLY inside
#: `if LOT_SPLIT_ON:`, so the shipped program never evaluates any of it.
LOT_SPLIT_ON = False
LOT_SPLIT_MAX = 0
LOT_SPLIT_DAYS = ()
_MACRO_SITES = {
    1: _MACRO_HERD,                                 # mix rewrite
    2: ("full", "hands_herd_land"),                 # land gate
    3: _MACRO_HERD,                                 # candidate values
    4: _MACRO_HERD,                                 # `_wants` animal want
    5: _MACRO_CREW,                                 # hire argmax
    6: _MACRO_CREW,                                 # HIRE_ROW trim excluded
    7: ("sell", "sell_late", "sell_hands"),         # sale timing
    8: _MACRO_LOT,                                  # own-clock lot placement
    9: _MACRO_BUY,                                  # market purchase channel
}


def _macro_site(n: int) -> bool:
    """True when site `n` fires under the current `MACRO_MODE` [SWITCH].

    Host-side and read at trace time, like every other switch in this module:
    the mode is a module constant by the time `build_day` is traced, so the
    branch is baked into the graph and costs nothing at runtime. Callers are
    already inside `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:`, so this
    never runs with the switch OFF.
    """
    if MACRO_MODE not in MACRO_MODES:
        raise ValueError(f"unknown MACRO_MODE {MACRO_MODE!r}; "
                         f"expected one of {MACRO_MODES}")
    return MACRO_MODE in _MACRO_SITES[n]


def _macro_plate0() -> bool:
    """True when the current mode masks the herd sites to day 0 [SWITCH].

    Host-side like `_macro_site`: the mask itself is a traced `day == 0`, but
    *whether* to apply it is a module constant, so the other modes keep the
    graph they had.
    """
    return MACRO_MODE == "plate0"


def _macro_window():
    """The inclusive `(lo, hi)` day window the herd sites are masked to, or
    `None` when the mode asks on every day [SWITCH].

    Host-side like `_macro_site`: the mask itself is a traced compare on
    `view.day`, but *whether* there is one is a module constant, so every
    other mode keeps the graph it had. `"plate0"` is the day-0 window (the
    form MACRO-CHANNELS shipped, value for value) and `"sheep13"` is
    `SHEEP_FLOOR_DAYS`.
    """
    if _macro_plate0():
        return (0, 0)
    if MACRO_MODE in _MACRO_SHEEP:
        return (int(SHEEP_FLOOR_DAYS[0]), int(SHEEP_FLOOR_DAYS[1]))
    return None


def macro_load(path=None):
    """Decode the macro schedule JSON into `MACRO_SCHEDULE` and return it.

    `path` defaults to `os.environ[MACRO_ENV]`. Pure host-side numpy: the
    arrays are module constants by the time any traced code reads them, so
    both backends see plain ints and `jit` bakes them in. Re-loading a
    different schedule inside a live `jit` cache would be stale, so a runner
    loads once, before the first trace.
    """
    import json as _json
    import os as _os
    import numpy as _np
    global MACRO_SCHEDULE
    if path is None:
        path = _os.environ.get(MACRO_ENV)
    if not path:
        MACRO_SCHEDULE = None
        return None
    d = _json.load(open(path))
    nd = spec.N_DAYS

    def _pad(a, shape):
        out = _np.zeros(shape, _np.int32)
        a = _np.asarray(a, _np.int32)
        n = min(shape[0], a.shape[0])
        out[:n] = a[:n]
        return out

    MACRO_SCHEDULE = dict(
        hands=_pad(d["hands_target"], (nd,)),
        anim=_pad(d["animals_target"], (nd, spec.N_ANIMALS)),
        tiles=_pad(d["tiles_target"], (nd, spec.N_CROPS)),
        land=_pad(d.get("land_target", [0] * nd), (nd,)),
        # [MACRO_EXEC site 7] `sell_hour[day][product]`: the first TURN a SELL
        # row for that product resolved on the tape, -1 where the tape sold
        # none. `_pad` pads with 0, which would read as "sell at turn 0", so
        # the missing-key default and the pad both have to be -1.
        # `_pad` zero-fills, so the row is shifted +1 before padding and
        # shifted back: a day past the end of the JSON reads -1 ("no sale"),
        # not "sell at turn 0".
        sell=_pad([[h + 1 for h in row]
                   for row in d.get("sell_hour",
                                    [[-1] * spec.N_ITEMS] * nd)],
                  (nd, spec.N_ITEMS)) - 1,
        # [WHEAT-REBUY site 9] `buy_target[day][item]`: MO_BUY_PRODUCT units
        # the tape bought that day. Absent from a schedule written before
        # WHEAT-REBUY, and `_pad`'s zero fill is exactly "bought nothing", so
        # an old JSON decodes to an all-zero row and every other mode is
        # unaffected.
        buy=_pad(d.get("buy_target", [[0] * spec.N_ITEMS] * nd),
                 (nd, spec.N_ITEMS)),
        tag=d.get("tag", ""))
    return MACRO_SCHEDULE


def _pf_wheat(xp, view, price_table, wheat_buy, cap, left, ask):
    """(wheat_buy + extra, cost of the extra) [SWITCH, PLACEFEED1]: `ask` more
    wheat on the turn-1 row, clipped to `cap` total and to the `left` coins the
    grant did not commit, priced up the same opponent-free buy walk as
    `_rebuy_extra`."""
    i32 = xp.int32
    ask = xp.maximum(xp.asarray(ask, i32), 0).astype(i32)
    want = xp.minimum(wheat_buy + ask, cap).astype(i32)
    quotes = PJ.buy_quotes(xp, price_table,
                           PJ.projected_inv(xp, view.mkt_inv, view.shops,
                                            O.TURN_BUY, _osd(view.day, "F")))
    cum = xp.cumsum(quotes[spec.I_WHEAT], dtype=i32)
    base = xp.where(wheat_buy > 0, cum[xp.clip(wheat_buy - 1, 0, PJ.K - 1)], 0)
    j = xp.arange(PJ.K, dtype=i32)
    n_aff = xp.sum(((j >= wheat_buy) & (cum - base <= left)).astype(i32),
                   dtype=i32).astype(i32)
    extra = xp.minimum(xp.maximum(want - wheat_buy, 0), n_aff).astype(i32)
    new = (wheat_buy + extra).astype(i32)
    cost = xp.where(extra > 0, cum[xp.clip(new - 1, 0, PJ.K - 1)] - base, 0).astype(i32)
    return new, cost


def _rebuy_extra(xp, view, price_table, wheat_buy, room, purse, costs, n_buy,
                 ask):
    """`wheat_buy` plus as much of `ask` as the shed and the purse allow.

    [WHEAT-REBUY] Called from exactly two guarded sites -- `if REBUY_ON:` and
    macro site 9 -- and from nowhere else, so the shipped path never evaluates
    it. The two clips are the engine's own: the market clips BUY_PRODUCT to
    the shed room slot by slot (`sim/market.py:666`) and stops at the first
    unit the buyer cannot pay for (`buy_walk`, `sim/market.py:98`). Charging
    them here as well keeps the planner's `purse_left` and `wheat_avail`
    truthful about a row the engine would have truncated.

    The quote walk is `PJ.buy_quotes` off the opponent-free projection at
    `O.TURN_BUY`, the same one the grant priced the feed wheat with, and the
    extra units are the walk's units `wheat_buy ..`, so they are charged the
    prices the row's later slots really meet -- a re-buy walks UP the curve.
    """
    i32 = xp.int32
    ask = xp.maximum(xp.asarray(ask, i32), 0).astype(i32)
    want = xp.minimum(wheat_buy + ask, room).astype(i32)
    left = xp.maximum(purse - BUD.spend(xp, costs, n_buy), 0).astype(i32)
    quotes = PJ.buy_quotes(xp, price_table,
                           PJ.projected_inv(xp, view.mkt_inv, view.shops,
                                            O.TURN_BUY, _osd(view.day, "F")))
    cum = xp.cumsum(quotes[spec.I_WHEAT], dtype=i32)
    base = xp.where(wheat_buy > 0, cum[xp.clip(wheat_buy - 1, 0, PJ.K - 1)], 0)
    j = xp.arange(PJ.K, dtype=i32)
    n_aff = xp.sum(((j >= wheat_buy) & (cum - base <= left)).astype(i32),
                   dtype=i32).astype(i32)
    extra = xp.minimum(xp.maximum(want - wheat_buy, 0), n_aff).astype(i32)
    return (wheat_buy + extra).astype(i32)


def _rebuy_ask(xp, day):
    """int32: the own-clock arm's extra units on `day` [WHEAT-REBUY]."""
    lo, hi = REBUY_DAYS
    return xp.where((day >= lo) & (day <= hi), xp.int32(REBUY_N), xp.int32(0))


def _macro_row(xp, day, key):
    """The schedule's row for `day`, as an `xp` int32 array (gather-safe)."""
    a = xp.asarray(MACRO_SCHEDULE[key])
    return a[xp.clip(day, 0, a.shape[0] - 1)].astype(xp.int32)


# `GEESE_TARGET` [FREE FLOAT, EGG]: a STOCK floor on the GOOSE lane of
# `macro.animal_want`, from `GEESE_DAY0` on.
#
# MAJKEL1 read the ladder leader's own ledger and found the one line he does
# not farm: EGG = 0 units in all 60 sampled games, and in 10 of his 20 losses
# the winner's single biggest lead IS the egg line (+4,962 .. +16,259).
# GEESE1 then priced how the egg winners run it, over the 48 seats of those 60
# episodes that sell more than 4,000 coins of egg (`S/majkel/eggscan.py`):
# **4 geese** (p10 3, p90 7), bought d4-d6 (0 head on d0-d3, median 3 by d6, 4
# from d9 and FLAT to d29), first egg SALE on d11 (p10 10, p90 13), ~162 units
# over 17 sale days -- 8-12 a day, every day -- at a price that does NOT move:
# 50-53/u through d18 and 47-48/u to the end, against melon's 244 -> 95 and
# wool's 159 -> 24 on the same boards.  The egg book is the one product line
# on this band that a second seller does not crash, which is why it is worth
# asking whether OUR body can carry it without paying the rival.
#
# Ours is nearly a goose-free program too: the PLANT_FILL census above reads
# GOOSE 1.2 head and EGG 50.6 units a game.  A goose costs 300 and a coop, and
# `brain.decide` splits the day's `animal_count` across the three species by a
# softmax of the product grow scores (`brain.py:1172`), which carries no target
# and no day term -- so the head count is whatever the trained theta's tilt
# leaves, and nothing in the program can ask for a stock of geese.
#
# `GEESE_TARGET` is that ask, and it is a *stock* want exactly like every other
# `animal_want` lane: `_wants` differences the standing head off it
# (`max(a_want - a_have, 0)`), `_seed_room`/`_place_split` clip it to the
# structures and the free tiles, `budget.grant` still prices the bird against
# every other candidate, and the coop, the FEED and the COLLECT_FERTILIZER it
# owes all go through the herd path that is already there.  Nothing is
# reallocated by hand: if the day cannot afford a goose it does not buy one.
#
# At the 0 default the two sites are Python-false and NOT ONE NODE is traced,
# so the shipped program is byte-identical.  This is a free module float in the
# HERD_TILT / MELON_PLATE_TILES pattern -- no `SWITCH_GENES` column, no layout
# move (7,692), every banked pairing stays CRN -- flown with
# `SW_EXTRA=,GEESE_TARGET=4`.
GEESE_TARGET = 0
#: First day the floor asks.  2, not 0: the egg winners hold 0 head through d3
#: and our own day-0 purse is the melon/strawberry plate's, and a goose bought
#: on d2 still lays from d6 (`first` 4, `interval` 1) against a first egg sale
#: the ledger puts at d11.
GEESE_DAY0 = 2
#: [EGGDOSE1] first day of the goose floor; None = `GEESE_DAY0` (the shipped
#: behaviour).  A separate name so the EGGDOSE1 grid flies it explicitly.
GEESE_FIRST_DAY = None


def _geese_day0() -> int:
    return int(GEESE_DAY0 if GEESE_FIRST_DAY is None else GEESE_FIRST_DAY)


def _geese_deficit(xp, view):
    """[EGGDOSE1] `GEESE_TARGET` minus the geese STANDING on coops (int, may be
    negative).  `animal_want` is the day's ACQUISITION (`a_have` is the shed),
    not a stock, so the pre-EGGDOSE1 floor bought up to GEESE_TARGET birds
    EVERY day; the dose is a stock: ask only for the head the board lacks."""
    i32 = xp.int32
    head = xp.sum((view.kind == spec.KIND_COOP) & (view.occ == _A_GOOSE), dtype=i32)
    return (xp.asarray(int(GEESE_TARGET), i32) - head).astype(i32)
#: GOOSE's column in the animal vectors (`spec.ANIMALS`), which is not
#: `spec.I_GOOSE` -- that is the ITEM index.
_A_GOOSE = spec.ANIMALS.index("GOOSE")


def _geese_floor(xp, view, macro: Macro) -> Macro:
    """`macro` with the GOOSE lane of `animal_want` floored at `GEESE_TARGET`
    from `GEESE_DAY0` [FREE FLOAT, EGG].

    A floor and not a write: `max(decode, target)`, so a theta that already
    wants more geese than the target keeps its want, and the other two lanes
    are untouched -- the arm adds a bird, it does not take a cow.
    """
    i32 = xp.int32
    floor = xp.where(xp.arange(spec.N_ANIMALS, dtype=i32) == _A_GOOSE,
                     xp.maximum(_geese_deficit(xp, view), 0),
                     xp.zeros((), i32)).astype(i32)
    floor = xp.where(view.day >= xp.asarray(_geese_day0(), i32),
                     floor, xp.zeros_like(floor)).astype(i32)
    return macro._replace(
        animal_want=xp.maximum(macro.animal_want.astype(i32), floor).astype(i32))


def _macro_targets(xp, view, macro: Macro) -> Macro:
    """`macro` with the schedule's tiles and herd written over the decode
    [SWITCH, MACRO_EXEC].

    The last mix rewrite of the day, so `_derive`'s two passes, `_wants`,
    `plant_eff` and `plant_crop` all read the schedule's vector. Unlike
    `_melon_open` this does NOT preserve `sum(plant_target)`: the whole point
    is that the schedule sizes the development, not the decode.

    `MACRO_MODE` splits the write in two. Under `"full"` both vectors are the
    schedule's -- the calendar EXEC-SCOPE measured. Under the three ramp modes
    only `animal_want` is, and `plant_target` stays whatever `brain.decide`
    sized against the board it can actually see, which is the whole point of
    those modes: the herd is a stock the schedule can name a day for, the
    planting is a flow that has to follow our own harvest clock.
    """
    i32 = xp.int32
    anim = _macro_row(xp, view.day, "anim").astype(i32)
    if MACRO_MODE in _MACRO_SHEEP:
        # [SELL-LOT] The sheep floor. A STOCK want, like every other
        # `animal_want` (site 4 differences the standing head off it), on the
        # sheep column alone and on `SHEEP_FLOOR_DAYS` alone; the schedule is
        # not read at all. Everything else -- the purse clip, the placement,
        # the pasture the head needs -- still binds, which is the whole point:
        # MACRO-CHANNELS §2.2 found the same ask cash-refused on day 0.
        lo, hi = _macro_window()
        floor = xp.where(xp.arange(spec.N_ANIMALS, dtype=i32) == _A_SHEEP,
                         xp.asarray(int(SHEEP_FLOOR_N), i32),
                         xp.zeros((), i32)).astype(i32)
        floor = xp.where((view.day >= lo) & (view.day <= hi),
                         floor, xp.zeros_like(floor)).astype(i32)
        return macro._replace(
            animal_want=xp.maximum(macro.animal_want.astype(i32), floor).astype(i32))
    if MACRO_MODE in _MACRO_FLOOR:
        # FLOOR, not ceiling [MACRO-CHANNELS]. `max(decode, schedule)` on the
        # days the schedule names an animal and the decode's own want on the
        # other 24 -- which is what keeps B's herd line (17.0 head by d16)
        # alive under a schedule whose rows are all zero after d6. Under
        # `"plate0"` even the named days are masked away except day 0, so the
        # arm is exactly "the top's opening plate, then B".
        if _macro_plate0():
            anim = xp.where(view.day == 0, anim, xp.zeros_like(anim)).astype(i32)
        return macro._replace(
            animal_want=xp.maximum(macro.animal_want.astype(i32), anim).astype(i32))
    if MACRO_MODE != "full":
        return macro._replace(animal_want=anim)
    return macro._replace(
        plant_target=_macro_row(xp, view.day, "tiles").astype(i32),
        animal_want=anim)


def _sheep_first(xp, view, macro: Macro) -> Macro:
    """Apply the SHEEPFIRST1 d0--2 sheep stock target to ``animal_want``.

    This is the own-clock form of ``sheep13``: the target uses the same stock
    lane and downstream herd machinery, but needs no external macro schedule.
    In swap mode only the newly requested sheep are taken from the cow lane.
    """
    if SHEEP_FIRST_MODE not in ("swap", "add"):
        raise ValueError("SHEEP_FIRST_MODE must be 'swap' or 'add'")
    if int(SHEEP_FIRST_N) < 0:
        raise ValueError("SHEEP_FIRST_N must be non-negative")
    i32 = xp.int32
    want = macro.animal_want.astype(i32)
    live = view.day <= xp.asarray(2, i32)
    target = xp.asarray(int(SHEEP_FIRST_N), i32)
    extra = xp.where(live, xp.maximum(target - want[_A_SHEEP], 0), 0).astype(i32)
    sheep = (want[_A_SHEEP] + extra).astype(i32)
    cow_i = spec.ANIMALS.index("COW")
    cow = want[cow_i]
    if SHEEP_FIRST_MODE == "swap":
        cow = xp.maximum(cow - extra, 0).astype(i32)
    lanes = xp.arange(spec.N_ANIMALS, dtype=i32)
    out = xp.where(lanes == _A_SHEEP, sheep, want).astype(i32)
    out = xp.where(lanes == cow_i, cow, out).astype(i32)
    return macro._replace(animal_want=out)


def _wool_first(xp, view, macro: Macro) -> Macro:
    """[WOOLFIRST1] d0--2: the herd ask is WOOL_FIRST_COWS cows + WOOL_FIRST_SHEEP sheep."""
    i32 = xp.int32
    want = macro.animal_want.astype(i32)
    live = view.day <= xp.asarray(2, i32)
    cow_i = spec.ANIMALS.index("COW")
    lanes = xp.arange(spec.N_ANIMALS, dtype=i32)
    out = xp.where(live & (lanes == _A_SHEEP), xp.asarray(int(WOOL_FIRST_SHEEP), i32), want)
    out = xp.where(live & (lanes == cow_i), xp.asarray(int(WOOL_FIRST_COWS), i32), out)
    if int(WOOL_FIRST_GEESE) >= 0:
        out = xp.where(live & (lanes == _A_GOOSE), xp.asarray(int(WOOL_FIRST_GEESE), i32), out)
    return macro._replace(animal_want=out.astype(i32))


#: [ESWORK1] WORK levers for ES over a FROZEN theta7659 + head_940: how much work
#: the farm does AFTER admission (docs/strategy/2026-09-26-eswork1.md). float[10]:
#:   0-3  relay wheat plantings per day on d10-14 / d15-19 / d20-24 / d25-27
#:        (rounded, clipped 0..6; free Q1-3 tiles the day's funded ask leaves;
#:        mandatory tier; relay hands sized from the relay's tasks on top of
#:        h_star = WHEATMIX1 cell g: planner water + planner fert on relay wheat)
#:   4    late ask floor d20-27: plant ask += round(clip(g,0,1) x (empty tiles -
#:        ask)) into WHEAT (d20-25) / CARROT (d26-27), priced by the planner
#:   5    EST_LEAD cut on d10-29: clip(EST_LEAD - round(g), 0, 10) in the hire
#:        scan and the admission labour
#:   6-9  Q4 buy band / Q4 relay density (NOT ported to this package: no Q4 relay; 0 in the shipped centre)
#: [ESSHIP1] shipped = the ESWORK1 run2 generation-30 candidate on the vrp8_jit base (kagg3/core/eswork_theta.npy, md5 6928257a):
#: relay 2/4/2/3 plantings/day on d10-14/15-19/20-24/25-27, EST_LEAD 5 -> 3 on d10+, genes 4 and 6-9 at 0.
#: `None` is Python-false: the vrp7 graph byte for byte.
ESWORK_D = 10
ESWORK_THETA = np.load(__import__("os").path.join(__import__("os").path.dirname(__file__), "eswork_theta.npy")).astype(np.float32)


def _ew_g(xp):
    return xp.asarray(ESWORK_THETA, xp.float32).reshape(ESWORK_D)


def _eswork_macro(xp, view, macro: Macro) -> Macro:
    """[ESWORK1] gene 4: the late (d20-27) short-crop ask floor on the FINAL macro."""
    i32 = xp.int32
    g = _ew_g(xp)
    day = xp.asarray(view.day, i32)
    t = macro.plant_target.astype(i32)
    tot = xp.sum(t, dtype=i32)
    n_empty = xp.sum((view.kind == spec.KIND_EMPTY).astype(i32), dtype=i32)
    gap = xp.maximum(n_empty - tot, 0).astype(xp.float32)
    extra = xp.round(xp.clip(g[4], 0.0, 1.0) * gap).astype(i32)
    extra = xp.where((day >= 20) & (day <= 27), extra, 0).astype(i32)
    crop = xp.where(day >= 26, spec.I_CARROT, spec.I_WHEAT)
    one = (xp.arange(spec.N_CROPS, dtype=i32) == crop).astype(i32)
    return macro._replace(plant_target=(t + one * extra).astype(i32))


def _est_lead(xp, day):
    """[ESWORK1] gene 5: EST_LEAD on d10-29 (Python EST_LEAD when the block is off)."""
    if ESWORK_THETA is None:
        return EST_LEAD
    i32 = xp.int32
    eff = xp.clip(EST_LEAD - xp.round(_ew_g(xp)[5]).astype(i32), 0, 10).astype(i32)
    return xp.where(xp.asarray(day, i32) >= 10, eff, EST_LEAD).astype(i32)


def _mr_want(xp, view):
    """[ESWORK1] genes 0-3: relay wheat plantings wanted today (d10-27, 0 if the wheat cannot yield by pay day)."""
    i32 = xp.int32
    day = _as(xp, view.day)
    want = xp.clip(xp.round(_ew_g(xp)[0:4]), 0, 6).astype(i32)[xp.clip((day - 10) // 5, 0, 3)]
    mat = day + int(spec.CROP_FIRST_YIELD_DAY[spec.I_WHEAT]) <= VAL.pay_day()
    return xp.where((day >= 10) & (day <= 27) & mat, want, 0).astype(i32)


ESWORK_RELAY_OPH = 12           # relay ops (incl. one move each) per added hand (= selfplay1 RL_ACT_OPH)
ESWORK_RELAY_MAX_E = 3          # most hands the relay adds in a day (= selfplay1 RL_ACT_MAX_E)
MR_LAST = [0, 0, 0]             # numpy-path census of the last day: relay planned, relay routed, hires


def _endgame_tomato(xp, view, macro: Macro) -> Macro:
    """`macro` with the day's crop mix moved onto TOMATO, up to the tile
    budget [SWITCH].

    Fires on `ENDGAME_TOMATO_DAY .. ENDGAME_TOMATO_LAST_DAY` and only in a town
    whose lottery drew at least `ENDGAME_TOMATO_SHOPS` tomato buyers; every
    other day keeps the mix the brain chose. Like `_wheat_mix` this is a mix
    change and not a development change -- `sum(plant_target)` is preserved by
    construction, so the tile, seed and labour budget the day is sized against
    does not move, only which crop the tiles get.

    `ENDGAME_TOMATO_TILES` caps the tomato tiles the rule holds AT ONCE: the
    live tomato plants already on the board are counted first and the day may
    only claim the difference. What the claim leaves goes back to the crops the
    brain chose, in the proportions it chose them (`_take_lr`, the same cut
    `_wheat_mix` uses), so the total is still exact. At the 0 default the room
    is the whole day and the answer is `is_tom * total` -- the pre-budget rule,
    value for value.

    The budget lowers the *rule's own claim* and never the brain's: `take` is
    floored at the tomato the softmax already asked for. That floor is what
    keeps the give-back exact -- the tiles handed back are precisely the ones
    the rule did not take, so `_take_lr` is always cutting a vector down and
    never scaling one up, and a mix that is tomato and nothing else (no other
    crop to hand a tile to) keeps its total instead of inventing crops the gene
    ruled out. The same shape of guarantee as `MELON_OPEN_TILES`, which can
    only ever raise melon.

    Scalar predicate, `where`-applied: `view.day` is a tracer under `jit` and
    the plan has to stay shape-static.
    """
    i32 = xp.int32
    t = macro.plant_target.astype(i32)
    total = xp.sum(t, dtype=i32).astype(i32)
    is_tom = (xp.arange(spec.N_CROPS, dtype=i32) == spec.I_TOMATO).astype(i32)
    if ENDGAME_TOMATO_TILES > 0:
        held = xp.sum(((view.kind == spec.KIND_PLANT)
                       & (view.occ == spec.I_TOMATO)).astype(i32),
                      dtype=i32).astype(i32)
        room = xp.maximum(xp.asarray(ENDGAME_TOMATO_TILES, i32) - held, 0)
        take = xp.maximum(xp.minimum(total, room), t[spec.I_TOMATO]).astype(i32)
    else:
        take = total
    kept = _take_lr(xp, (t * (1 - is_tom)).astype(i32),
                    (total - take).astype(i32))
    mix = (kept + is_tom * take).astype(i32)
    n_shop = xp.sum(view.shops * xp.asarray(_TOMATO_SHOPS), dtype=i32).astype(i32)
    fire = ((view.day >= ENDGAME_TOMATO_DAY)
            & (view.day <= ENDGAME_TOMATO_LAST_DAY)
            & (n_shop >= ENDGAME_TOMATO_SHOPS))
    return macro._replace(plant_target=xp.where(fire, mix, t).astype(i32))


def _late_straw_cap(xp, view, macro: Macro) -> Macro:
    """`macro` with STRAWBERRY out of the day's mix from `LATE_STRAW_CAP_DAY`
    [SWITCH].

    The share strawberry would have taken goes to the crops the brain also
    chose, in the proportions it chose them (`_fill_plant` over the other four,
    scaled back up to the day's own total), so this is a mix change and not a
    development change and `sum(plant_target)` does not move. A day whose mix
    is strawberry and nothing else keeps it: there is no proportion to fill
    into, and dropping the tiles outright would be a development change made by
    a mix rule.

    The tiles already carrying strawberry are not touched -- this is the
    planting decision, not the sell rule -- so they water, yield and sell out
    exactly as before.
    """
    i32 = xp.int32
    t = macro.plant_target.astype(i32)
    total = xp.sum(t, dtype=i32).astype(i32)
    is_str = (xp.arange(spec.N_CROPS, dtype=i32) == spec.I_STRAWBERRY).astype(i32)
    others = (t * (1 - is_str)).astype(i32)
    fire = (view.day >= LATE_STRAW_CAP_DAY) & (xp.sum(others, dtype=i32) > 0)
    return macro._replace(
        plant_target=xp.where(fire, _fill_plant(xp, others, total), t).astype(i32))


def _melon_veto(xp, view, macro: Macro, flood_k=None) -> Macro:
    """`macro` with MELON out of the day's mix while the book is flooded
    [SWITCH].

    Two scalar predicates, both facts the day already holds: the day is at or
    past `MELON_VETO_FLOOD_DAY`, and the dawn melon inventory stands at least
    `MELON_VETO_FLOOD_K` units over `spec.MARKET_I0` -- the same opening
    inventory `_I0_COL` indexes the price table at, and the same `view.mkt_inv`
    the sell side's projection reads. Applied with `where`, so the plan stays
    shape-static and the gate is a tracer under `jit`.

    Nothing is redistributed. `sum(plant_target)` falls by the melon share and
    the day is sized against the smaller number, exactly as it would be on a
    day whose brain asked for no melon: the freed tiles, seed coins and water
    turns go wherever the existing decode and scheduler already send them. That
    is the whole point -- TURNCOST moved the same tiles onto wheat and gifted
    the rival on the shared curve.

    The tiles already carrying melon are not touched: this is the planting
    decision, not the sell rule, so a melon already in the ground waters,
    yields and sells out exactly as before.
    """
    i32 = xp.int32
    flood_k = MELON_VETO_FLOOD_K if flood_k is None else flood_k
    t = macro.plant_target.astype(i32)
    late = _as(xp, view.day) >= xp.asarray(int(MELON_VETO_FLOOD_DAY), i32)
    flood = (_as(xp, view.mkt_inv)[spec.I_MELON]
             >= xp.asarray(int(spec.MARKET_I0 + flood_k), i32))
    is_melon = xp.arange(spec.N_CROPS, dtype=i32) == spec.I_MELON
    return macro._replace(
        plant_target=xp.where(late & flood,
                              xp.where(is_melon, 0, t), t).astype(i32))


def _wants(xp, view, macro, n_free, sfree, a_have, acquire_ok,
           wheat_short, fert_short):
    """int[N_LISTS]: how many of each candidate list the day would take if the
    purse allowed, on a board with `n_free` developable tiles.

    Split out of `_candidates` because it is the only part of the candidate
    model a land purchase moves -- `values` and `costs` do not read the tile
    count at all -- so the marginal worth of a quadrant is this vector
    evaluated twice and differenced [1.3].
    """
    i32 = xp.int32
    a_want, seed_cap = _seed_room(xp, macro, n_free, sfree, a_have)
    # The seed want, clipped to the tiles that will exist [M1]. `plant_target`
    # used to be bounded by construction -- `brain.decide` sized it against the
    # very `free_slot` predicate `_derive` uses -- but M1 made that predicate
    # depend on a land grant `brain` can only predict: it knows neither the
    # hire bill nor the cash reserve, so it can ask for 25 tiles the planner
    # then refuses. Over-asking is harmless on the placement side (`plant_here`
    # is masked by `free_slot`) but not on the purchase side, so the want is
    # clipped here -- prefix-wise in crop order, the same cumulative-boundary
    # trick `plant_crop` uses.
    want_raw = xp.maximum(macro.plant_target - view.seeds, 0)
    if open_board():
        # MELON and WHEAT take their tiles off the *front* of the prefix on the
        # opening day [SWITCH]. Melon is the last crop in `spec.CROPS`, so the
        # default cumsum charges it every other crop's want before `seed_cap`
        # reaches it -- and the want does over-ask (`brain.decide` sizes
        # `plant_total` against a land grant it cannot price: 21 tiles on a
        # 19-tile board on day 0), so the two crops the opening is built around
        # are exactly the ones the clip would drop. Same pairwise compare
        # `_melon_open` pays the debt with. OFF this is the cumsum it was.
        srank = xp.asarray(_MELON_SEED_RANK)
        m_before = xp.sum(
            xp.where(srank[None, :] < srank[:, None], want_raw[None, :], 0),
            axis=1, dtype=i32).astype(i32)
        before = xp.where(view.day == MELON_OPEN_DAY, m_before,
                          xp.cumsum(want_raw, dtype=i32) - want_raw).astype(i32)
    else:
        before = xp.cumsum(want_raw, dtype=i32) - want_raw
    if PROGRAM_ENGINE_ON and PROGRAM_PLANT_SHARE:
        # PROGFIX1 (1c): held seed already claims its tiles; the buy room is
        # what is left, or the day buys seed it has no tile for.
        seed_cap = xp.maximum(seed_cap - xp.sum(xp.minimum(view.seeds, macro.plant_target)), 0).astype(i32)
    w_seed = (_program_seed_room(xp, want_raw, seed_cap) if PROGRAM_ENGINE_ON
              else xp.clip(want_raw, 0, xp.maximum(seed_cap - before, 0)))
    w_anim = xp.where(acquire_ok, xp.maximum(a_want - a_have, 0), 0)
    if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:
        # [SWITCH, MACRO_EXEC] `acquire_ok` (`ub_coins > ANIMAL_COST`) is the
        # last *value* gate on the herd, and it prices the animal off the
        # board the day already has -- the same today-only reading of the farm
        # that priced the top's day-1 crew at zero. A schedule that names the
        # herd has already made that judgement, so the want passes; the purse
        # and the placement clip below still bind. Site 4: off under "hands",
        # whose only claim is the crew.
        if _macro_site(4):
            w_new = xp.maximum(a_want - a_have, 0).astype(i32)
            # `"plate0"` opens the gate on day 0 only and `"sheep13"` on
            # `SHEEP_FLOOR_DAYS`; every other mode keeps the graph it had.
            _w = _macro_window()
            w_anim = (xp.where((view.day >= _w[0]) & (view.day <= _w[1]),
                               w_new, w_anim).astype(i32)
                      if _w is not None else w_new)
    if GEESE_TARGET > 0:
        # [FREE FLOAT, EGG] `acquire_ok` (`ub_coins > ANIMAL_COST`) is the last
        # *value* gate on the herd and it prices the bird off the board the day
        # already has -- the same today-only reading that priced the top's
        # day-1 crew at zero.  A target that names a stock has made that
        # judgement, so the GOOSE lane passes the gate from `GEESE_DAY0`; the
        # purse (`budget.grant`), the placement and the coop still bind, which
        # is what keeps the ask honest.
        # [EGGDOSE1 bug fix] only the FLOOR (stock deficit - shed) skips
        # the gate; before, the whole decoded goose want did (`a_want` is
        # `max(decode, target)`), so GEESE1/KNOBV56 measured an ungated goose
        # lane, not a dose.  The rest of the want stays gated like every lane.
        g_ok = ((xp.arange(spec.N_ANIMALS, dtype=i32) == _A_GOOSE)
                & (view.day >= xp.asarray(_geese_day0(), i32)))
        g_floor = xp.maximum(xp.minimum(a_want, _geese_deficit(xp, view))
                             - a_have, 0).astype(i32)
        w_anim = xp.where(g_ok, xp.maximum(w_anim, g_floor).astype(i32),
                          w_anim).astype(i32)
    if WOOL_FIRST_ON:
        # [WOOLFIRST1] the named d0-2 cow and sheep stock bypasses the spot gate.
        wf_open = (((xp.arange(spec.N_ANIMALS, dtype=i32) == _A_SHEEP)
                    | (xp.arange(spec.N_ANIMALS, dtype=i32) == spec.ANIMALS.index("COW")))
                   & (view.day <= xp.asarray(2, i32)))
        w_anim = xp.where(wf_open, xp.maximum(a_want - a_have, 0).astype(i32),
                          w_anim).astype(i32)
    if SHEEP_FIRST_ON:
        # [SHEEPFIRST1] A named opening stock bypasses the spot-value gate on
        # its sheep lane only; purse, shed room and pasture placement remain.
        sheep_open = ((xp.arange(spec.N_ANIMALS, dtype=i32) == _A_SHEEP)
                      & (view.day <= xp.asarray(2, i32)))
        w_anim = xp.where(sheep_open,
                          xp.maximum(a_want - a_have, 0).astype(i32),
                          w_anim).astype(i32)
    if PROGRAM_ENGINE_ON:
        # A committed stock deficit bypasses only the spot-value veto; room,
        # purse, structures and the shared grant still bind.
        w_anim = xp.maximum(a_want - a_have, 0).astype(i32)
    return xp.stack([wheat_short, fert_short]
                    + [w_seed[c] for c in range(spec.N_CROPS)]
                    + [w_anim[a] for a in range(spec.N_ANIMALS)]).astype(i32)


def _candidates(xp, view, day, price_table, buy_q, grow_mult, u_new, is_plant, has_animal,
                feeds, ferts, animal, a_keep):
    """`(values, costs)`: `budget.grant`'s eight candidate lists [1.3].

    One wheat per passing feed, one fertilizer per application, the k-th seed
    of each crop and the k-th animal -- each priced in coins against its
    engine-curve cost, and each list ordered so value per coin does not rise
    along it, which is what makes the greedy a threshold.

    Neither array depends on how many tiles the day has -- only `_wants` above
    does, which is the fact that makes the land valuation cheap.

    Lifted out of `_derive` verbatim, so everything it reads is passed in:
    `feeds` is `(pass mask, value rank, value)`, `ferts` is `(candidate mask,
    value rank, value)`, and `animal` is `(ub_units, ub_fert, ub_feeds)` -- what
    0.2's upper-bound test derived, one entry per animal kind.

    `a_keep` is the crew ramp's deferral scale in `DEFER_ONE` fixed point
    [g10]: the animal lists are worth `a_keep / DEFER_ONE` of what they price
    at while the day's crew is under the ramp's target, and exactly what they
    price at (`DEFER_ONE`) otherwise.
    """
    i32 = xp.int32
    feed_pass, feed_rank, feed_value = feeds
    fert_cand, fert_rank, fert_val = ferts
    ub_units, ub_fert, ub_feeds = animal
    j = xp.arange(PJ.K, dtype=i32)
    # feeds and applications in value order; the shed covers the first ranks free
    sorted_feed = xp.sum(((feed_rank[:, None] == j[None, :]) & feed_pass[:, None]).astype(i32)
                         * feed_value[:, None], axis=0, dtype=i32)
    v_wheat = sorted_feed[xp.clip(j + view.shed[spec.I_WHEAT], 0, PJ.K - 1)]
    sorted_fert = xp.sum(((fert_rank[:, None] == j[None, :]) & fert_cand[:, None]).astype(i32)
                         * fert_val[:, None], axis=0, dtype=i32)
    v_fert = sorted_fert[xp.clip(j + view.shed[spec.I_FERT], 0, PJ.K - 1)]
    # the k-th planting's units sell k*u further down the curve, priced by
    # direct table reads (not a K-long cumsum: K = 101 would value every
    # melon past the 16th and every wheat past the 25th at zero) -- and the
    # curve is the SALES-WINDOW one [HEURISTIC, gap review 2026-08-24]: the
    # hour-0 inventory drained by the town to the product's first fire, plus
    # everything the farm has already committed to that market. Opponent
    # supply is absent by construction; `press`/`grow_mult` carry it.
    inv_h = (PJ.inv_at_day(xp, view.mkt_inv, view.shops, xp.asarray(_FIRST_P),
                           _osd(view.day, "C"))
             + _pipeline_units(xp, view, is_plant, has_animal, day))
    # [SWITCH, RSFIX1] the animal lists read their own window: the family curve only when site "A" is on.
    inv_ha = inv_h
    if OPP_SUPPLY_FAMILY_ON and (("A" in str(OPP_SUPPLY_FAMILY_SITES)) != ("C" in str(OPP_SUPPLY_FAMILY_SITES))):
        inv_ha = (PJ.inv_at_day(xp, view.mkt_inv, view.shops, xp.asarray(_FIRST_P),
                                _osd(view.day, "A"))
                  + _pipeline_units(xp, view, is_plant, has_animal, day))
    # Every stream is clipped to the ratio arithmetic's coin ceiling before the
    # multiplier: `grow_mult` reaches 4x and a stream read off the table's dear
    # end would otherwise leave int32 (section 2's `< 2**20` rule).
    # The other seat's standing commitment, priced into the same two lists the
    # planting decision reads [SWITCH, OPP_MIX]. Exactly 1x OFF -- the branch
    # is a Python `if` on a module global, so OFF the expressions below are the
    # ones they always were, character for character.
    mix_w = _opp_mix_weight(xp, view) if OPP_MIX_ON else None
    v_seed, c_seed = [], []
    for c in range(spec.N_CROPS):
        rev = _stream_rev(xp, price_table[c], inv_h[c], u_new[c], j)
        v_c = grow_mult[c] * xp.clip(rev, 0, BUD.VALUE_CAP) // GROW_ONE
        v_seed.append(v_c * mix_w[c] // OPP_MIX_ONE if OPP_MIX_ON else v_c)
        c_seed.append(xp.full((PJ.K,), int(spec.CROP_SEED_COST[c]), i32))
    # One block per animal kind [1.3]: the k-th goose, the k-th cow and the
    # k-th sheep are three separate candidate lists, each walking its own
    # product's curve. The three-way `where` chain this replaces existed to
    # avoid a *dynamic* `price_table[a_prod]` row index -- under `vmap` that
    # materialises an 85,001-wide row per lane before the [K, 32] read it
    # actually wants -- and the loop keeps that property: the row index is a
    # Python int in every iteration. Same three `_stream_rev` calls, one fewer
    # select.
    #
    # [HEURISTIC] All three price their fertilizer stream off the same
    # `inv_h[I_FERT]`, so a day buying all three over-values the herd's
    # fertilizer by the cannibalisation between the lists. The grant is a
    # threshold and not a sequence, so the offset is not knowable at pricing
    # time; the bound is three lists x ~25 units on one curve, and `press` /
    # `grow_mult` are the residual's owners [1.1].
    # One shared stream: `ub_fert` is the days left in the season and so is the
    # same for every kind, and a fertilizer is a fertilizer whoever made it.
    fert_stream = _stream_rev(xp, price_table[spec.I_FERT], inv_ha[spec.I_FERT],
                              xp.minimum(ub_fert[0], STREAM_MAX), j)
    v_anim, c_anim = [], []
    for a in range(spec.N_ANIMALS):
        p_a = int(spec.ANIMAL_PRODUCT[a])
        rev_a = (_stream_rev(xp, price_table[p_a], inv_ha[p_a],
                             xp.minimum(ub_units[a], STREAM_MAX), j)
                 + fert_stream - ub_feeds[a] * view.price[spec.I_WHEAT])
        # The deferral rides on the end of the existing expression rather than
        # on the value that goes into it, so at `a_keep == DEFER_ONE` the whole
        # of it is `x * 256 // 256 == x` -- an exact integer identity, not an
        # approximation [g10]. The intermediate is at most `GROW_MAX *
        # VALUE_CAP` = 4.19e6, so the product stays inside int32.
        v_a = (grow_mult[p_a] * xp.clip(rev_a, 0, BUD.VALUE_CAP) // GROW_ONE
               * a_keep // DEFER_ONE)
        # The mix weight rides on the very end for the same reason `a_keep`
        # does: at 1x it is the exact integer identity `x * ONE // ONE == x`,
        # and the ceiling of 1x keeps the product inside int32 [OPP_MIX].
        v_anim.append(v_a * mix_w[p_a] // OPP_MIX_ONE if OPP_MIX_ON else v_a)
        c_anim.append(xp.full((PJ.K,), int(spec.ANIMAL_COST[a]), i32))

    values = xp.stack([v_wheat, v_fert] + v_seed + v_anim)
    costs = xp.stack([buy_q[spec.I_WHEAT], buy_q[spec.I_FERT]] + c_seed + c_anim)
    return values, costs


# ============================== GENE SWITCHES ==============================
#
# [SWITCH-GENE 2026-09-16, docs/strategy/2026-09-16-geneswitch.md] The module
# constants above are a 66-wide binary vector the lead sets by hand and judges
# one arm at a time, at roughly two reads a day against a ladder that moves
# daily. The ones listed here are read from the *theta* instead: `brain.decide`
# decodes one flip bit per name off the global head and the planner takes the
# module default XOR that bit, so the search moves the vector with the rest of
# the policy and a gene-switch may additionally depend on the board, which the
# constant never could.
#
# Only value-level switches are here. Most of the 66 are structural -- they
# change how many rows, turns or route blocks the program has, and those are
# read at trace-construction time by `early_lot_turns`, `route_turns` and
# `_routes` -- and a traced bit cannot move a shape (`S/geneswitch/switches.md`
# classifies all 66).

#: The layout. Column `i` of `sw`/`swb` is `SWITCH_GENES[i]` for the life of
#: every theta trained under it, so this tuple may never be reordered or have a
#: name removed from the middle; widening it is an append at the end plus a
#: raise of `policy.N_SWITCH_GENES` (asserted equal in `tests/test_geneswitch`).
SWITCH_GENES = (
    "FEED_MANDATORY_ON",        # [A] the mandatory tier's feed half
    "SURVIVAL_WATER_ON",        # [B] the tier above mandatory, and `must_water`
    "ANIMAL_DEFER_ON",          # [A] the early-day animal price
    "CARE_HOLD_ON",             # [B] what a banked care unit is worth
    "FERT_VOLUME_ON",           # [B] the fertilizer bar and `v_fert`
    "SHED_DEFICIT_ON",          # [A] the watering bonus in the shed inflow
    "CREW_PUSH_COST_ON",        # [A] the crew-target push term
    "WHEAT_VOLUME_ON",          # [B] the wheat line's share of the mix
    "LATE_STRAW_CAP_ON",        # [B] strawberry out of the late mix
    "ENDGAME_TOMATO_ON",        # [B] the endgame tomato claim
    "ENDROUTE_ON",              # [A] the terminal day's last executed row
    "OPEN_PUMP_ON",             # [A] the day-0 hour-0 wheat pump (SHIPPED OFF)
    "CLIP_CAP_ON",              # [A] the shed's room, spent dearest-first
    "ENDROUTE2_ON",             # [A] day 29's turn budget, re-cut to the row
    "ENDROUTE2_SPLIT_ON",       # [A] day 29's two shed trips
    "ENDROUTE_ROW2_ON",         # [A] day 29's SECOND late row (needs ENDROUTE)
    "WIDE_PICK_ON",  # [A] the wide day's turn-1 stationary second PICKUP
    "WIDE_PICK_FREE_ON",  # [A] ... and its turn-1 kind chosen free-first
    "MELONVETO_POST_ON",  # [A] flooded-melon veto after the residual head
    "CARE_FILL_ON",  # [A] fill otherwise-idle tail turns with useful CARE
    "OVERFLOW_GUARD_ON",  # [A] bank/sell excess carry before destruction
)
SWITCH_GENE_INDEX = {n: i for i, n in enumerate(SWITCH_GENES)}
#: What each name ships as, captured at import -- i.e. before any runner has
#: touched the module. The override rule below is a comparison against this.
SWITCH_GENE_DEFAULTS = {n: bool(globals()[n]) for n in SWITCH_GENES}


def _sw(macro: Macro, name: str):
    """The effective value of gene-switch `name`: a Python `bool` when it is
    concrete, else a traced 0/1 the caller must `where` on.

    **Precedence, and it is one comparison** [same rule as `FORWARD_ADMIT_ON`]:
    a module constant the lead has moved off the value it ships with is a
    manual override and wins outright, so `S/drainpin/on2b.py` and every
    paired A/B runner still pin a switch against any theta. Otherwise the
    theta's gene rules, and a zero gene is the shipped default itself -- which
    is what makes the whole block inert and the pair ship identically.

    A zero flip -- the untrained block, a theta from before it, or a Macro
    built by hand -- is that same default, and on the numpy path it is a
    *concrete* zero, so the site takes its original Python branch and no
    `where` is built at all: the shipped program is the one it always was.
    """
    cur = bool(globals()[name])
    if cur != SWITCH_GENE_DEFAULTS[name]:
        return cur                              # the lead's override
    flip = macro.switches
    if flip is None:
        return cur
    flip = flip[SWITCH_GENE_INDEX[name]]
    try:
        return cur != bool(int(flip))           # concrete: the host path
    except TypeError:                           # a tracer, under jit or vmap
        return (flip == 0) if cur else (flip != 0)


def _sw_pick(xp, on, on_value, off_value):
    """`on_value()` under `on`, `off_value` otherwise.

    `on_value` is a thunk so the concrete-OFF path -- the shipped one for every
    switch that defaults OFF -- never builds the branch it does not take, and
    the program is the one that was there before the gene existed.
    """
    if on is False:
        return off_value
    v = on_value()
    return v if on is True else xp.where(on, v, off_value)


def _sw_all(*ons):
    """The effective value of a gene switch that REQUIRES other switches.

    `ENDROUTE2_ON` spends turns into `ENDROUTE_ON`'s row and
    `ENDROUTE2_SPLIT_ON` spends `ENDROUTE2_ON`'s turns; without what they stand
    on they buy a walk that sells nothing, which the module-level asserts refuse
    outright.  A gene block cannot refuse: the search draws all four columns
    independently, so the dependency has to live in the VALUE rather than in an
    assert -- a draw that takes the row away takes its dependants with it, and
    the ES sees the ENDROUTE-off program instead of an exception.

    Concrete beats traced, the same precedence `_sw` has: any concrete `False`
    makes the whole thing concretely off (so the site builds no branch at all
    and the shipped program stays untraced), all-`True` is `True`, and anything
    left is `&`-ed on the vector.
    """
    if any(o is False for o in ons):
        return False
    rest = [o for o in ons if o is not True]
    if not rest:
        return True
    out = rest[0]
    for o in rest[1:]:
        out = out & o
    return out


def _sw_macro(xp, on, rewrite, macro: Macro) -> Macro:
    """A Macro rewrite (`_wheat_mix` and friends) under a gene switch.

    Field-wise, and only the fields the rewrite actually replaced: the mix
    rules return `macro._replace(plant_target=...)`, so everything else is the
    *same object* and stays out of the graph.
    """
    if on is False:
        return macro
    new = rewrite()
    if on is True:
        return new
    moved = {f: xp.where(on, getattr(new, f), getattr(macro, f))
             for f in Macro._fields
             if getattr(new, f) is not getattr(macro, f)}
    return macro._replace(**moved)


def _derive(xp, view: DayView, macro: Macro, price_table, hire_bill, terminal, reserve,
            rev1=None, forward=None, seed_extra=None, ask_fill=False,
            program_engine=None):
    """The day's whole plan except how many hands walk it -- section 1.5's
    "cheap prefix", run once per candidate hire bill.

    Everything here reads the view and the macro; the only ways the hire count
    reaches it are `hire_bill`, the coins the two HIRE rows have already spent
    by the time the BUY row resolves, and `reserve`, the coins tomorrow's crew
    needs kept back (`cash_reserve`). `terminal` is passed in rather than
    recomputed so both passes share the one flag. `rev1` likewise: it is the
    same number in both passes (nothing it reads depends on the hire count), so
    pass A computes it and pass B is handed the answer rather than paying for a
    second allocator walk.

    `forward` is the projection horizon in days, `None` (or a Python 0) for the
    unwidened pass every caller but the hire scan wants [FORWARD_ADMIT]. It may
    be a traced scalar: only the *presence* of the widening is a Python-level
    decision, the number of days is arithmetic.

    Returns a `Prefix`; `build_day` turns it into a route and a market row.
    """
    i32 = xp.int32
    day = view.day
    kind, occ = view.kind, view.occ
    zero = xp.zeros(N_T, i32)
    one = xp.ones(N_T, i32)

    # ---- the crew ramp's deferral [g10] ----------------------------------
    # The Kaggle losses are all the same shape: the opponent has 12 hands and
    # 9k on day 10 and we have 6 and 3.3k, with the difference already spent on
    # animals and coops. Hiring first is only half the fix -- the purse the
    # crew needs has to still be there when the BUY row resolves -- so while
    # this day's crew is under the ramp's target the animal channel is demoted:
    # its candidate values (the purchase) and its structure builds (the coop or
    # pasture the placement needs) are both scaled by `keep / DEFER_ONE`.
    #
    # The crew is read off the bill this pass was handed, which is the one
    # channel the hire count has into `_derive`: pass A runs on a zero bill and
    # so prices the day as the *unstaffed* farm, which is conservative in the
    # right direction (it demotes animals in the pass whose value order the
    # enumeration then reads), and pass B runs on the winner's bill and lifts
    # the deferral the moment the crew has actually been hired.
    #
    # Integer throughout and exactly inert at zero theta: `crew_target` is 0,
    # so `crew_now < 0` is false, `keep` is `DEFER_ONE`, and every scaled
    # quantity is `x * DEFER_ONE // DEFER_ONE == x` for the non-negative int32
    # values this touches.
    crew_now = (_count_le(xp, xp.asarray(HIRE_BILLS), hire_bill) - 1).astype(i32)
    a_keep = xp.where(crew_now < macro.crew_target,
                      DEFER_ONE - macro.animal_defer, DEFER_ONE).astype(i32)
    sw_defer = _sw(macro, "ANIMAL_DEFER_ON")
    if sw_defer is not False:
        # The forced deferral (`ANIMAL_DEFER_ON` at :1850): the early days do
        # not ask `crew_now` at all -- that comparison is the one the hire
        # bill cancels -- they just price animals at `ANIMAL_DEFER_KEEP`.
        # Past `ANIMAL_DEFER_LAST_DAY` the gene's own expression stands.
        fires = ((day <= ANIMAL_DEFER_LAST_DAY) if sw_defer is True
                 else sw_defer & (day <= ANIMAL_DEFER_LAST_DAY))
        a_keep = xp.where(fires,
                          xp.asarray(ANIMAL_DEFER_KEEP, i32), a_keep).astype(i32)

    is_plant = kind == spec.KIND_PLANT
    is_coop = kind == spec.KIND_COOP
    is_struct = is_coop | (kind == spec.KIND_PASTURE)
    has_animal = is_struct & (occ >= 0)
    free_struct = is_struct & (occ < 0)
    a_idx = xp.clip(occ, 0, spec.N_ANIMALS - 1)
    is_weed = kind == spec.KIND_WEED
    is_empty = kind == spec.KIND_EMPTY
    if EXPIRY_SLOT_ON or (PROGRAM_ENGINE_ON and PROGRAM_EXPIRY):
        # PROGFIX2 (3): the programme reuses spent strawberry/tomato tiles the
        # dawn they expire (the ENGINE digs 31 tiles d20-29, the port 17 and
        # it left 20 spent tiles standing as weeds while plantings ran short).
        expired = _expiry_slots(xp, view)
        is_weed = is_weed | expired
        is_plant = is_plant & ~expired
    final_slot = _final_slots(xp, view) if LATE_EXEC_ON else None   # [SWITCH]

    crop = xp.clip(occ, 0, spec.N_CROPS - 1)
    c_ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    c_first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    c_mxd = xp.asarray(spec.CROP_MAX_YIELD_DAY)[crop]
    c_sat = xp.asarray(spec.CROP_SATURATE_AGE)[crop]
    c_ws = xp.asarray(spec.CROP_WINDOW_START)[crop]
    age = day - view.t_day

    # ---- survival and yield ops, and the quotes 1.4 prices a feed at ------
    # Survival pays only if what survives can still sell [LAW, 0.4]: on the
    # last payable day nothing that lives into tomorrow is worth a turn or a
    # wheat, so survival waterings and feeds stop and the feed want leaves
    # the budget's wheat list. In-window waterings that raise a same-day harvest stay.
    # `HORIZON_DROP_ON` moves that day from 28 to 29: a crop watered on day 28
    # is alive for a day-29 harvest that the DROP chain sells, and an animal
    # fed on day 28 is there to collect from.
    survival_pays = day < VAL.pay_day()

    # Engine-curve buy pricing [LAW, 0.10]: BUY_PRODUCT walks the curve one
    # unit at a time from the hour-0 inventory advanced by the turn-0 town
    # tick, and stops at the first unit the purse cannot pay. A flat hour-0
    # price over-commits by the curve's rise, and the engine then drops
    # whatever sits in the last BUY slot. Cross-seat same-turn coupling is the
    # acknowledged residual. The quotes depend on the view alone, so they are
    # priced here rather than in the budget's grant: 1.4's feed test needs the
    # per-unit wheat price before it knows how much wheat the day wants.
    inv_buy = PJ.projected_inv(xp, view.mkt_inv, view.shops, O.TURN_BUY, _osd(view.day, "F"))
    buy_q = PJ.buy_quotes(xp, price_table, inv_buy)

    # One-time crops are harvested at the age their yield saturates -- or on
    # the last payable day when the season ends first. HARVEST needs only
    # age >= first_yield_day and yield > 0, so the harvest age is the age the
    # crop will have on `VAL.pay_day()`, clamped into its yield window: a wheat
    # planted on day 25 sells 3 units on day 28 instead of decaying unsold at
    # age 4 on day 29 -- and with `HORIZON_DROP_ON` it waits one more day and
    # sells 4 on day 29, because the DROP chain banks that harvest.
    #
    # The upper clamp is `CROP_SATURATE_AGE`, not `CROP_MAX_YIELD_DAY`: for
    # every crop but melon they are the same age, and for melon the last two
    # days of the window add no units (WATER is already capped at
    # CROP_MAX_YIELD by age 10) while costing two days of market position and
    # two waterings a tile. Melon is the one product with no shop demand, so
    # its curve is drained by whoever reaches it first and never refills;
    # harvesting at 12 put our first melon on the market on day 13 behind the
    # opponent's day-10 dump, at 108 coins a unit against their 173.
    harvest_age = xp.clip(VAL.pay_day() - view.t_day, c_first, c_sat)
    if WHEAT_CYCLE_H3_ON:                                        # [SWITCH, WHEATCYCLE1]
        # age-3 harvest only when today's fertilized watering lands it on 5 u:
        # dawn yield >= 3 means the age-2 watering was fertilized too (1+2);
        # a tile fertilized after its age-2 water (yield 2) waits for 6 at age 4.
        _wc_h3 = (is_plant & (crop == spec.I_WHEAT) & (view.t_fert >= view.t_day + 3)
                  & (view.t_yield >= 3))
        harvest_age = xp.where(_wc_h3, xp.minimum(harvest_age, 3), harvest_age).astype(harvest_age.dtype)
        _wc_early = _wc_h3 & (age >= 3) & (age < c_sat)

    # Water when the plant would otherwise weed tonight, or when watering still
    # buys yield (one-time crops inside their bonus window). Ongoing crops gain
    # nothing from watering beyond survival, so they get it every other day --
    # except on a fertilized fire night, where the water turns the fertilizer
    # into +2 instead of +1; that case is added in the clamp section below.
    must_water = (view.t_cons >= 1) & survival_pays
    # [SWITCH `SURVIVAL_WATER_ON`] charge the survival watering for its turn.
    # `crop_remaining_value` is `v_water`'s own price for this watering, read
    # here so the *tier* sees it too: a tile whose stream is spent (an ongoing
    # crop past its last fire, a one-time crop whose harvest lands past
    # `pay_day()`) is 30.3 tile-days a game of mandatory work that buys nothing
    # -- and it dies to `_decay_plants` whatever we do. `survives_water` is
    # also the promoted tier below.
    sw_surv = _sw(macro, "SURVIVAL_WATER_ON")
    if sw_surv is not False:
        survives_water = must_water & (
            VAL.crop_remaining_value(xp, view.price, view.t_day, view.t_yield,
                                     crop, day, harvest_age) > SURVIVAL_WATER_MIN)
        must_water = (survives_water if sw_surv is True
                      else xp.where(sw_surv, survives_water, must_water))
    bonus_water = (c_ongoing == 0) & (age >= c_ws) & (age <= c_mxd)
    want_water = is_plant & (view.t_water == 0) & (must_water | bonus_water)

    harvest_one = is_plant & (c_ongoing == 0) & (age >= harvest_age)
    if program_engine is not None:
        # Programme turnover needs cells before grain saturates. Harvest
        # only ripe grain needed to release the requested planting space.
        ripe_grain = (is_plant & (crop <= spec.I_CARROT)
                      & (age >= c_first) & ~harvest_one)
        free_now = xp.sum((is_empty | is_weed | harvest_one).astype(i32))
        long_work = xp.sum(macro.plant_target[spec.I_TOMATO:]) + xp.sum(macro.animal_want)
        release = xp.maximum(long_work - free_now, 0)
        early_grain = (ripe_grain & (_rank_near(xp, ripe_grain, xp.asarray(DIST_SHED)) < release)
                       & (day <= 9))
        harvest_one = harvest_one | early_grain
    harvest_ong = is_plant & (c_ongoing == 1) & (view.t_yield > 0) & (age >= c_first)
    if forward is not None:
        # [FORWARD_ADMIT] The same two windows, `forward` days wide: a
        # one-time crop whose bonus window opens within the horizon emits its
        # watering now, and one that saturates within it emits its harvest.
        # Both are supersets of the unwidened masks (`age + F >= c_ws` is
        # implied by `age >= c_ws` for `F >= 0`), so this pass's task set
        # contains today's and the enumeration can only read *more* work.
        # The upper clamps stay where they are: past `c_mxd` a watering buys no
        # unit whatever the horizon says, and `harvest_age` is the age the crop
        # is worth taking at, not a window.
        #
        # The *branch* is Python-level and taken at trace time, so the shipped
        # (`forward=None`) prefix is compiled from the identical expressions
        # under NumPy and JAX alike; the horizon itself is a value and may be a
        # tracer, which is what lets a theta state it. At `forward == 0` the
        # three expressions below are the three above them term for term --
        # integer arithmetic, so "equal" here means byte-equal.
        f = xp.asarray(forward, i32)
        bonus_water = (c_ongoing == 0) & (age + f >= c_ws) & (age <= c_mxd)
        want_water = is_plant & (view.t_water == 0) & (must_water | bonus_water)
        harvest_one = is_plant & (c_ongoing == 0) & (age + f >= harvest_age)

    # [MIDDAY_PLACE_V2] The ripe melon of the opening, on the one day it is
    # ripe. The tile keeps its WATER (worth one unit of the six -- melon is a
    # one-time crop, so `_daily_refresh_plants` skips it and every unit past
    # the first is a watering) and its HARVEST, and loses the rest of the day:
    # no BUILD, no PLACE and no replant-plus-water. Two ops instead of four is
    # what puts the deposit that follows in front of the row that sells it.
    mel_bank = xp.zeros((N_T,), bool)
    if MIDDAY_PLACE_V2_ON:                                       # [SWITCH]
        mel_bank = harvest_one & (view.occ == spec.I_MELON)

    # Production fires whether or not the animal was fed, so feeding buys
    # survival, the payout of a pending CARE bank on a fire day (0.11: the
    # bank is consumed only on a fed production day), and today's CARE.
    an_first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a_idx]
    an_int = xp.asarray(spec.ANIMAL_INTERVAL)[a_idx]
    an_held = xp.asarray(spec.ANIMAL_MAX_HELD)[a_idx]
    an_prod = xp.asarray(spec.ANIMAL_PRODUCT)[a_idx]
    fires_tonight = has_animal & VAL.fires_on(xp, view.t_day, an_first, an_int, day + 1) & survival_pays
    must_feed = (view.t_cons >= 1) & survival_pays
    bank_feed = fires_tonight & (view.t_bank > 0)
    # CARE is the third reason to feed [0.11 + 1.4, gap review 2026-08-26].
    # The bank increments only on a day the animal was *both* fed and cared,
    # so a feed rule that waits for hunger inherits the engine's starvation
    # cadence -- `consecutive_unfed >= 2` means every other day is enough to
    # keep the animal -- and hands CARE the same 0.5/day ceiling. The cow's
    # every-second-night fire then cashes a bank of 1 where a daily cadence
    # would cash 2, which is 2 units a fire against 3. Measured against kagg2
    # over 16 real-engine games: 0.56 feeds and 0.49 cares per animal-day
    # against its 0.97 / 0.96, and 178 milk units against 256.
    #
    # The conditions are exactly `want_care`'s, hoisted to here so the feed
    # can be bought for the care it enables; `want_care` reads them back
    # rather than restating them. `bank_carry` is the bank still standing when
    # tonight's care is added: a fire consumes (fed) or wipes (unfed) it
    # first, so on a fire night it is 0 (eod.py: fire -> bank = 0 -> bank +=
    # 1). Substituting `fires_tonight` for a bare `fires_on` only changes
    # tiles with no animal (`t_bank` is 0 there) and days past the horizon
    # (`survival_pays` already zeroes `care_ok`).
    h_next = VAL.next_fire_after(xp, view.t_day, an_first, an_int, day)
    bank_carry = xp.where(fires_tonight, 0, view.t_bank)
    care_headroom = bank_carry + 2 <= an_held
    # What one banked unit is worth [SWITCH `CARE_HOLD_ON`]. Off, the spot
    # quote of the day the care is taken; on, that quote floored by the
    # sales-window curve `_candidates` prices the animal stream on, so a care
    # is not refused on a trough the unit is never sold into.
    care_price = view.price[an_prod]
    sw_hold = _sw(macro, "CARE_HOLD_ON")
    if sw_hold is not False:
        inv_hold = (PJ.inv_at_day(xp, view.mkt_inv, view.shops,
                                  xp.asarray(_FIRST_P), view.day)
                    + _pipeline_units(xp, view, is_plant, has_animal, day))
        idx_hold = xp.clip(inv_hold - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
        # One [9] read, never a per-tile row index: `price_table[an_prod]`
        # would materialise an 85,001-wide row per tile under `vmap`, the
        # hazard `_candidates`' per-kind loop exists to avoid.
        fwd_price = xp.take_along_axis(price_table, idx_hold[:, None], axis=1)[:, 0]
        held_price = xp.maximum(care_price, fwd_price.astype(i32)[an_prod])
        care_price = (held_price if sw_hold is True
                      else xp.where(sw_hold, held_price, care_price))
    care_pays = care_price > view.price[spec.I_WHEAT]
    care_ok = (has_animal & (view.t_cared == 0) & (h_next <= VAL.pay_day())
               & care_headroom & care_pays & survival_pays)
    feed_want = has_animal & (view.t_water == 0) & (must_feed | bank_feed | care_ok)
    # Feeding as a value decision [EXACT-OPT, 1.4]: feed iff what the animal
    # can still sell -- capped at a replacement's cost, plus a pending CARE
    # bank cashable at a monetizable fire -- beats this feed's wheat price:
    # the hour-0 quote for shed wheat, the curve price for bought wheat. One
    # that fails is left to escape and (0.8) not replaced.
    #
    # The bank rides *outside* the replacement cap (the cap prices the animal,
    # not the bonus) and a bank of b pays min(b, max_held - 1) extra units: a
    # fed fire yields min(max_held, yield + 1 + bank) and the planner harvests
    # whenever units are held. A bank-only feed -- the animal lives either way
    # -- is worth that payout alone: it does not pass on the animal's remaining
    # production, so it cannot outrank an *equally valuable* hungry animal for
    # the last wheat on production it is not buying. It can outrank a less
    # valuable one, and should: a bank-only cow's payout really can exceed a
    # hungry goose's replacement-capped value, and each number is the coins
    # that feed actually buys.
    #
    # `bank_h` is the *harvest day* of the first fire whose end-of-day is at or
    # after today's, which is the fire a bank standing this morning pays on.
    bank_h = VAL.next_fire_after(xp, view.t_day, an_first, an_int, day - 1)
    bank_val = (xp.where(bank_h <= VAL.pay_day(), xp.minimum(view.t_bank, an_held - 1), 0)
                * view.price[an_prod])
    # Flow, not stock [gap review, 1.4]: `animal_value` counts the units the
    # animal already holds and today's available fertilizer, and the planner
    # harvests and collects those whether or not it feeds (`want_harv_animal`
    # and `want_collect` below do not read the feed). Charging a feed for stock
    # it does not buy would feed a spent animal for the units already in its
    # hands. Subtract today's harvestable stock before the replacement cap --
    # the cap prices a *replacement*, and a replacement does not come with the
    # incumbent's held units either -- and never let the remainder go negative.
    keep_price = view.price
    if FEED_FORWARD_ON:                                          # [SWITCH, FEEDKEEP1]
        inv_ff = PJ.inv_at_day(xp, view.mkt_inv, view.shops,
                               xp.asarray(int(FEED_FORWARD_K), i32), view.day)
        if FEED_FORWARD_PIPE:
            inv_ff = inv_ff + _pipeline_units(xp, view, is_plant, has_animal, day)
        idx_ff = xp.clip(inv_ff - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
        fwd_ff = xp.take_along_axis(price_table, idx_ff[:, None], axis=1)[:, 0].astype(i32)
        _pr = xp.arange(spec.N_PRODUCTS, dtype=i32)
        _anp = (_pr == spec.I_EGG) | (_pr == spec.I_MILK) | (_pr == spec.I_WOOL)
        keep_price = xp.where(_anp, xp.maximum(view.price, fwd_ff), view.price).astype(i32)
    stock_today = (view.t_yield * keep_price[an_prod]
                   + view.t_favail * view.price[spec.I_FERT]).astype(i32)
    keep_val = xp.minimum(
        xp.maximum(
            VAL.animal_value(xp, keep_price, view.t_day, view.t_yield, view.t_favail, a_idx, day)
            - stock_today, 0),
        xp.asarray(spec.ANIMAL_COST)[a_idx])
    # The care the feed unlocks is the third term [gap review, 1.4]: one more
    # unit at `h_next`, and on a quiet day the *whole* of what the feed buys.
    # Priced at the product and not net of the wheat -- the wheat is what
    # `feed_pass` weighs the value against -- and booked exactly once for the
    # labour: `v_feed` below hands this unit to the CARE op, which is the op
    # that earns it. The headroom and horizon tests are already in `care_ok`.
    care_val = xp.where(care_ok, view.price[an_prod], 0).astype(i32)
    feed_value = (xp.where(must_feed, keep_val + bank_val, bank_val)
                  + care_val).astype(i32)
    feed_rank0 = _rank_by(xp, feed_want, feed_value)
    shed_wheat = view.shed[spec.I_WHEAT]
    feed_price = xp.where(feed_rank0 < shed_wheat, view.price[spec.I_WHEAT],
                          buy_q[spec.I_WHEAT][xp.clip(feed_rank0 - shed_wheat, 0, PJ.K - 1)])
    feed_pass = feed_want & (feed_value > feed_price)
    feed_rank = _rank_by(xp, feed_pass, feed_value)
    want_collect = has_animal & (view.t_favail == 1)
    want_harv_animal = has_animal & (view.t_yield > 0)

    # ---- what the day can spend, and on what -----------------------------
    # Two deductions before anything is priced.
    #
    # The hire bill, because TURN_HIRE resolves before TURN_BUY and hiring is
    # not one of the budget's candidate lists -- so the row must be priced
    # against what the day will still have, not against `view.money`. Left out,
    # the row over-commits by exactly the hire bill and the engine drops
    # whatever sits in the last BUY slot, which the fixed layout makes
    # BUY_LAND. Measured on order1's gen-650 champion: land lost for four
    # coins. *Which* bill it is, is the caller's candidate [1.5]: pass A
    # prices the day on a zero bill so the enumeration can score every hand
    # count against a common task list, pass B on the winner's, so the purse
    # this walk spends is the one the day is really left with. The turn-2 hire
    # row is in that bill too, and resolving *after* the BUY row does not make
    # it optional: coins the BUY row spends at turn 1 are coins the turn-2
    # hires then cannot pay, and a hand the engine refuses leaves a unit whose
    # whole route the engine silently discards.
    #
    # The cash reserve, because the greedy spends whatever it is handed
    # (`cash_reserve`): tomorrow's crew has to survive today's shopping.
    if program_engine is not None:
        # Today’s service is senior to expansion and tomorrow’s reserve.
        # Use the same marginal quotes as the grant, not spot-price times
        # units: even a two-coin underestimate can drop an entire melon seed.
        feed_short_now = xp.maximum(xp.sum(feed_pass.astype(i32), dtype=i32)
                                    - shed_wheat, 0)
        program_service_cost = xp.sum(xp.where(
            xp.arange(PJ.K) < feed_short_now, buy_q[spec.I_WHEAT], 0), dtype=i32)
        opening_seed_cost = xp.where(day <= 2, xp.maximum(
            macro.plant_target[spec.I_MELON] - view.seeds[spec.I_MELON], 0)
            * int(spec.CROP_SEED_COST[spec.I_MELON]), 0)
        reserve = xp.minimum(reserve, xp.maximum(
            view.money - hire_bill - program_service_cost - opening_seed_cost, 0))
    money = xp.where(terminal, 0,
                     xp.maximum(view.money - hire_bill - reserve, 0)).astype(i32)

    # Free slots as the board stands. The land grant is decided further down,
    # against the very candidate lists these size, and `free_slot` is then
    # re-derived with the bought quadrant's tiles in it [M1].
    free_slot = is_empty | is_weed | harvest_one
    if final_slot is not None:                                   # [SWITCH]
        free_slot = free_slot | final_slot
    if MIDDAY_PLACE_V2_ON:                                       # [SWITCH]
        # A melon tile the day banks is not a slot the day develops: the
        # replant is tomorrow's, and it is the two turns it costs that the
        # excursion needs. OFF `mel_bank` is all-false and this is a no-op.
        free_slot = free_slot & ~mel_bank
    n_free = xp.sum(free_slot.astype(i32))
    # Shed room caps every shed-bound buy at turn 1 [LAW]: the market clips
    # BUY_PRODUCT and BUY_ANIMAL to SHED_CAPACITY - sum(shed) slot by slot,
    # and lot 1 only fires at turn 3, so no same-day sale makes room. Seeds
    # and land are not shed items. `budget.grant` carries the room itself
    # [LAW, 0.10], so `sum(n[SHED_LISTS]) <= room` already holds on the way
    # out; the clamp below walks the same room down the slot order the engine
    # clips in as a backstop, and on a granted row it never binds.
    room = xp.maximum(spec.SHED_CAPACITY - xp.sum(view.shed.astype(i32)), 0).astype(i32)

    feed_need = xp.sum(feed_pass.astype(i32), dtype=i32)
    wheat_short = xp.maximum(feed_need - shed_wheat, 0)
    # Value-ranked fertilizer targeting [0.11]: one application is worth its
    # exact clipped marginal units at today's price -- 0 for a crop that
    # saturates anyway (melon watered daily), up to +3 for a tomato with three
    # fires in the window. Fertilize, and buy the shortfall, iff that beats the
    # unit's own price (what a shed unit sells for, what a bought one costs).
    # Never renew an active application: waiting for it to lapse covers
    # strictly more days. Simplification: the threshold is the flat hour-0
    # quote although the purchase itself walks the curve (0.10); the gap is
    # one unit's rise per bought unit and the shortfall is bounded by the
    # candidates, so it is labelled, not modelled.
    fert_val = VAL.fert_marginal_value(xp, view.price, view.t_day, view.t_yield, crop, day, harvest_age)
    # The bar is what the unit the application spends would fetch [H3]. OFF
    # that is one times its own quote, which is the expression this switch was
    # cut into; ON it is `NUM/DEN` times whichever price `FERT_VOLUME_MODE`
    # names, so the application has to beat the sale by a margin and not merely
    # tie it -- and, in the two non-spot modes, has to beat a bar that does not
    # fall away with the quote it is pricing.
    sw_fvol = _sw(macro, "FERT_VOLUME_ON")
    if sw_fvol is True:
        fert_ref = _fert_reference(xp, view, price_table)
        fert_bar = ((fert_ref * FERT_VOLUME_NUM) // FERT_VOLUME_DEN).astype(i32)
    elif sw_fvol is False:
        fert_ref = view.price[spec.I_FERT]
        fert_bar = view.price[spec.I_FERT]
    else:
        v_ref = _fert_reference(xp, view, price_table)
        fert_ref = xp.where(sw_fvol, v_ref, view.price[spec.I_FERT])
        fert_bar = xp.where(sw_fvol,
                            ((v_ref * FERT_VOLUME_NUM) // FERT_VOLUME_DEN).astype(i32),
                            view.price[spec.I_FERT])
    if FERT_DUMP_ON:
        # [SWITCH, FERT_DUMP] From `FERT_DUMP_DAY` the unit's sale is worth its
        # quote PLUS what dumping it takes off the rival's remaining fertilizer
        # revenue, so the application has to clear both. `day` is a tracer under
        # `jit`, so the gate is a scalar predicate applied with `where` and the
        # plan stays shape-static.
        _late = _as(xp, day) >= xp.asarray(int(FERT_DUMP_DAY), i32)
        fert_bar = xp.where(
            _late, fert_bar + xp.asarray(int(FERT_DUMP_BONUS), i32),
            fert_bar).astype(i32)
    fert_cand = is_plant & (view.t_fert < day) & (fert_val > fert_bar)
    if WHEAT_CYCLE_ON or WHEAT_CYCLE_CARROT_ON:                 # [SWITCH, WHEATCYCLE1]
        _wc_c = xp.zeros_like(is_plant)
        if WHEAT_CYCLE_ON:
            _wc_c = _wc_c | (crop == spec.I_WHEAT)
        if WHEAT_CYCLE_CARROT_ON:
            _wc_c = _wc_c | (crop == spec.I_CARROT)
        fert_cand = fert_cand & ~(_wc_c & (age < 2))
    # [SWITCH, FERT_TIMING] Hold the unit while a day inside the look-ahead
    # buys strictly more on this same tile. `_static_horizon` is the
    # `FORWARD_ADMIT` idiom: on the numpy path a zero horizon is known and the
    # projected valuation is never built, under a trace it is not and the
    # `where` makes every projected day past `ft_days` a no-op, so the two
    # paths differ in cost and never in outcome.
    ft_days = (xp.asarray(int(FERT_TIMING_DAYS), i32) if FERT_TIMING_ON
               else macro.fert_defer)
    if _static_horizon(ft_days) != 0:
        best = fert_val
        for _k in range(1, int(FERT_TIMING_MAX) + 1):
            _v = VAL.fert_marginal_value(xp, view.price, view.t_day, view.t_yield,
                                         crop, day + _k, harvest_age)
            best = xp.where(xp.asarray(_k, i32) <= ft_days,
                            xp.maximum(best, _v), best).astype(i32)
        fert_cand = fert_cand & (fert_val >= best)
    n_fert_want = xp.sum(fert_cand.astype(i32), dtype=i32)
    fert_rank = _rank_by(xp, fert_cand, fert_val)
    fert_short = xp.maximum(n_fert_want - view.shed[spec.I_FERT], 0).astype(i32)
    # Tiles this morning already owes work on, for the land valuation's labour
    # clamp [1.3]. Every mask here is fixed before the budget runs, which is
    # what lets the valuation run ahead of the greedy: the clamp cannot depend
    # on what the day buys, because what the day buys depends on it.
    pre_work = (feed_pass | want_water | want_collect | want_harv_animal
                | harvest_one | harvest_ong | fert_cand | is_weed)

    # ---- lot-1 revenue a land grant may count on [HEURISTIC, M2] ---------
    # BUY_LAND rides the spare tenth slot of `SELL_TURNS[0]`, after that turn's
    # nine sells, so the morning's own revenue can fund it. That is the only
    # same-day funding anything in this planner has: the whole BUY row resolves
    # at turn 1, ahead of every sale.
    #
    # It has to be *safe*. The provisional allocation runs on the largest
    # reservations the walk can possibly make -- every passing feed's wheat,
    # every wanted application's fertilizer -- so the final allocation reserves
    # no more and lot 1 really does sell at least this much. That is safe
    # against the farm's own reservations only: 1.1's projection is
    # opponent-free, and the other seat's lockstep sales at the same turn lower
    # the quotes this one receives. A BUY_LAND that then fails is not a
    # marginal price miss -- every prospective op of the day no-ops on a
    # still-LOCKED tile with its seeds and animals already bought -- so only
    # LAND_REV_NUM/LAND_REV_DEN of the projection is counted.
    if rev1 is None:
        e_wheat = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_WHEAT).astype(i32)
        e_fert = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_FERT).astype(i32)
        fert_prov = n_fert_want
        if FERT_RESERVE_ON:
            # [SWITCH, FERT_RESERVE] The provisional allocation has to stay a
            # LOWER bound on lot 1, so it reserves at least what the real sale
            # will. The day's applications are not decided yet, so the mask is
            # all-false, which is the largest reserve the recurrence can
            # return -- and `n_fert_want >= n_fert_eff` on the near term.
            fert_prov = (n_fert_want + _fert_future_reserve(
                xp, view, xp.zeros(N_T, bool))).astype(i32)
        avail_prov = xp.maximum(view.shed[:spec.N_PRODUCTS].astype(i32)
                                - e_wheat * feed_need - e_fert * fert_prov, 0)
        # Gated with the same floor as the real sale below [H2]: the
        # provisional allocation has to stay a *lower* bound on lot 1, so a
        # reservation the day will honour must be honoured here too or a
        # BUY_LAND could be funded out of a sale that never happens.
        hold_prov = _sell_hold(
            xp, price_table,
            xp.where(terminal, SELL.LIQUIDATE, macro.hold).astype(i32), terminal,
            day=view.day)
        lots_prov = SELL.allocate(xp, price_table, view.mkt_inv, view.shops,
                                  avail_prov, hold_prov, macro.press,
                                  day=_osd(view.day, "S"))
        q1 = PJ.sell_quotes(xp, price_table, PJ.projected_inv(
            xp, view.mkt_inv, view.shops, O.SELL_TURNS[0], _osd(view.day, "S")))
        rev1 = ((xp.sum(PJ.sell_revenue(xp, q1, lots_prov[0]), dtype=i32)
                 * LAND_REV_NUM) // LAND_REV_DEN).astype(i32)

    # Per animal kind from here down [1.3]: two structure kinds and three
    # animals, so cow and sheep share the pastures and nothing may be clipped
    # per kind on its own (`_place_split`).
    struct_kind = xp.where(is_coop, spec.KIND_COOP, spec.KIND_PASTURE)
    st_free = [free_struct & (struct_kind == int(k))
               for k in (spec.KIND_COOP, spec.KIND_PASTURE)]
    # Per kind, the free structures of the kind it needs. A `where` over the
    # two room totals rather than a stack of three: see `_prefix` on why no
    # three-lane vector down here is built out of three separate chains.
    sfree = xp.where(xp.asarray(NEEDS_COOP),
                     xp.sum(st_free[0].astype(i32), dtype=i32),
                     xp.sum(st_free[1].astype(i32), dtype=i32)).astype(i32)
    a_have = view.shed[spec.I_GOOSE:spec.I_GOOSE + spec.N_ANIMALS].astype(i32)

    # Animal acquisition: upper-bound value test [EXACT-OPT, 0.2]. A new
    # animal is placed today and hungry on day+1, day+3, ...; it must live
    # through eod `pay_day() - 1` for its last collection. Reject only on a
    # non-positive *optimistic* bound (today's prices, no labour), so the
    # rejection is safe under the opponent-free projection; acceptance goes
    # through the marginal-unit budget below. Stock already in the shed is
    # placed regardless.
    a_prod = xp.asarray(spec.ANIMAL_PRODUCT)
    ones_a = xp.ones(spec.N_ANIMALS, i32)
    ub_units = xp.stack([
        VAL.fires_between(xp, day, int(spec.ANIMAL_FIRST_YIELD_DAY[a]),
                          xp.maximum(xp.asarray(int(spec.ANIMAL_INTERVAL[a]), i32), 1),
                          day + 1, VAL.pay_day())
        for a in range(spec.N_ANIMALS)]).astype(i32)
    ub_fert = (ones_a * xp.maximum(VAL.pay_day() - day, 0)).astype(i32)
    # One feed a day, not one every two [gap review 2026-08-26]: the cadence
    # the feed rule above actually runs, so this is the wheat an animal really
    # costs. The *units* stay at one a fire on purpose. Adding the care bonus
    # here -- `min(max_held, 1 + interval)` a fire, which is what a daily
    # cadence really yields -- measured -5,946 +- 2,664 coins a game against
    # kagg2 over 16 real-engine games with the old feed rule and -9,743
    # against this section's own C variant with the new one: the bound also
    # sizes `v_place` and the k-th animal's candidate value, and a herd priced
    # three units a fire is bought faster than the day's turns and wheat can
    # service it. Charging the true feed and counting only the base unit
    # leaves the bound conservative on the unit side, which costs 0.2 nothing
    # it was relying on -- rejections stay rare and late-season.
    #
    # This one line keeps `O.LAST_SHED_DAY` under `HORIZON_DROP_ON` and it is
    # deliberate: it counts *feeds*, not payable days. The animal must live
    # through eod `pay_day() - 1` to be collected from on `pay_day()`, so the
    # feeds it needs are days `day + 1 .. pay_day() - 1`, which at the new
    # horizon is exactly `LAST_SHED_DAY - day`. The old horizon over-charged
    # this bound by one feed; the new one makes it exact.
    ub_feeds = (ones_a * xp.maximum(O.LAST_SHED_DAY - day, 0)).astype(i32)
    # The animal's product priced where it is actually SOLD [SWITCH
    # `ANIMAL_BUY_FWD_ON`].  OFF, `ub_coins` is the expression it always was:
    # today's spot quote times the fires the animal has left.  That is the
    # quote of the day we BUY, and an animal's first unit does not reach the
    # market for `first_yield_day` days -- six for a sheep -- by which time our
    # own committed stream has already walked the curve down.  WOOL is the
    # product where that matters: its glut arm is quadratic
    # (`above_func "sq"`, `above_target 3.20`, `T 105`), so the town's wool pot
    # floors at PRICE_FLOOR after ~59 net units across BOTH seats and the last
    # units before the floor cost ~6 coins of quote each.  Measured on live
    # episode 109698269 (`docs/strategy/2026-09-16-woolprice.md`): the quote is
    # 187 on day 10 when the fifth sheep is placed, 1 from day 17 to the end of
    # the season, and the 43 wool units that herd produced after the floor
    # realised 2.02 coins each.
    #
    # ON, the product term reads the *sales-window* curve instead -- the same
    # `inv_h` `_candidates` already prices the k-th animal's stream on and that
    # `CARE_HOLD_ON` reads for its gate: hour-0 inventory drained by the town to
    # the product's first fire, plus every unit this farm has already committed
    # (`_pipeline_units`).  It is a `min` against the spot quote, not the `max`
    # `CARE_HOLD_ON` uses, because the two switches move opposite gates: a CARE
    # is refused on a trough the unit is never sold into, so its price wants a
    # floor; a PURCHASE is accepted on a peak the unit is never sold at, so its
    # price wants a ceiling.
    #
    # NOTE: this weakens the invariant the block above states -- OFF, `ub_coins`
    # is an optimistic bound and `acquire_ok` can only reject an animal that
    # cannot pay under ANY schedule.  ON it is a forecast, and a forecast can be
    # wrong in both directions.  The opponent's stream is still absent from it
    # (`OPP_SUPPLY_ON` / `OPP_MIX_ON` are the two attempts at that and both were
    # refused: `docs/strategy/2026-09-11-oppsupply-screen.md`), so ON is
    # strictly the own-supply half of the correction.
    #
    # Only the animal's OWN product moves.  The fertilizer term stays at spot on
    # purpose: every animal earns the same fertilizer stream, so haircutting it
    # changes the herd's SIZE without changing its MIX, and the mix is what the
    # wool curve is an argument about.
    a_price = view.price[a_prod]
    if ANIMAL_BUY_FWD_ON:
        inv_ab = (PJ.inv_at_day(xp, view.mkt_inv, view.shops,
                                xp.asarray(_FIRST_P), view.day)
                  + _pipeline_units(xp, view, is_plant, has_animal, day))
        idx_ab = xp.clip(inv_ab - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
        # One [9] read, never a per-tile row index -- the `CARE_HOLD_ON` note on
        # why `price_table[a_prod]` must not be materialised under `vmap`.
        fwd_ab = xp.take_along_axis(price_table, idx_ab[:, None], axis=1)[:, 0]
        a_price = xp.minimum(a_price, fwd_ab.astype(i32)[a_prod])
    ub_coins = (ub_units * a_price + ub_fert * view.price[spec.I_FERT]
                - ub_feeds * view.price[spec.I_WHEAT]).astype(i32)
    acquire_ok = ub_coins > xp.asarray(spec.ANIMAL_COST)

    # ---- marginal-unit budget [HEURISTIC, 1.3] ---------------------------
    # Purchases are marginal candidates -- one wheat per passing feed, one
    # fertilizer per application, the k-th seed of each crop, the k-th animal
    # -- each with a value in coins and an engine-curve cost, granted by
    # value per coin down the purse (core/budget.py). Land is lumpy, so it is
    # not one of the lists: it is priced in the same coins by `marginal_gain`
    # and compared two ways -- grant if it pays, else skip -- ahead of the
    # greedy, with the gene reduced to a coin bias on that comparison.
    grow_mult = macro.grow_mult.astype(i32)
    if program_engine is not None:
        # Programme repayment is measured in coins, before policy mix weights.
        grow_mult = xp.full(spec.N_PRODUCTS, GROW_ONE, i32)
    u_new = VAL.new_plant_units(xp, xp.arange(spec.N_CROPS, dtype=i32), day)
    values, costs = _candidates(
        xp, view, day, price_table, buy_q, grow_mult, u_new, is_plant, has_animal,
        (feed_pass, feed_rank, feed_value),
        (fert_cand, fert_rank, fert_val),
        (ub_units, ub_fert, ub_feeds), a_keep)
    if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:
        # [SWITCH, MACRO_EXEC] The herd ahead of the seed lists in the ONE
        # `budget.grant` walk that holds both (`2026-09-14-melon-animal-
        # mechanism.md` §3). `grant` is a threshold on value per coin, so a
        # multiplier on the animal lists' values -- clipped to the same cap
        # `_candidates` builds under -- lifts every animal above every seed
        # without changing the order *within* the animal lists, which is what
        # prices the mix. Nothing else about the walk moves: the wants are the
        # schedule's, the costs are the market's, the purse is the day's.
        # Site 3: off under "hands", which asks for no herd to prioritise.
        if _macro_site(3):
            a_sel = ((xp.arange(BUD.N_LISTS, dtype=i32) >= BUD.L_ANIMAL0)
                     & (xp.arange(BUD.N_LISTS, dtype=i32)
                        < BUD.L_ANIMAL0 + spec.N_ANIMALS))
            _w = _macro_window()
            if _w is not None:
                a_sel = a_sel & (day >= _w[0]) & (day <= _w[1])
            # A floor, not a multiplier: the k-th animal's own price is what
            # the greedy would rank it by, and on a board whose tasks have not
            # appeared yet that price is often zero -- the FORWARD_ADMIT
            # reading again. The list stays a legal `grant` input because value
            # is constant along it while cost is non-decreasing, so value per
            # coin still does not rise.
            values = xp.where(a_sel[:, None], xp.asarray(BUD.VALUE_CAP, i32),
                              values).astype(i32)
    if WOOL_FIRST_ON:
        # [WOOLFIRST1] cow + sheep lists served before competing seeds on d0-2.
        wf_list = ((xp.arange(BUD.N_LISTS, dtype=i32) == (BUD.L_ANIMAL0 + _A_SHEEP))
                   | (xp.arange(BUD.N_LISTS, dtype=i32)
                      == (BUD.L_ANIMAL0 + spec.ANIMALS.index("COW"))))
        wf_list = wf_list & (day <= xp.asarray(2, i32))
        values = xp.where(wf_list[:, None], xp.asarray(BUD.VALUE_CAP, i32),
                          values).astype(i32)
    if SHEEP_FIRST_ON:
        # [SHEEPFIRST1] The sheep target is served before competing seeds on
        # d0--2, exactly as the sheep13 herd-priority site, but lane-specific.
        sheep_list = xp.arange(BUD.N_LISTS, dtype=i32) == (BUD.L_ANIMAL0 + _A_SHEEP)
        sheep_list = sheep_list & (day <= xp.asarray(2, i32))
        values = xp.where(sheep_list[:, None], xp.asarray(BUD.VALUE_CAP, i32),
                          values).astype(i32)
    if program_engine is not None:
        # Spend aggressively through d9. Thereafter a phase target must not
        # turn an acquisition with negative lifetime return into a paid order.
        # Owned inputs remain usable; only new purchases face this test.
        repays = values > costs
        limits = xp.sum(repays.astype(i32), axis=1, dtype=i32)
        macro = macro._replace(
            plant_target=xp.where(day <= 9, macro.plant_target,
                xp.minimum(macro.plant_target,
                           view.seeds + limits[BUD.L_SEED0:BUD.L_ANIMAL0])).astype(i32),
            animal_want=xp.where((day <= 9) | (PROGRAM_HERD_FIRST
                                              & (day <= PROGRAM_HERD_LAST_DAY)),
                                 macro.animal_want,
                xp.minimum(macro.animal_want,
                           a_have + limits[BUD.L_ANIMAL0:])).astype(i32))
        service_list = xp.arange(BUD.N_LISTS) < BUD.L_SEED0
        animal_list = xp.arange(BUD.N_LISTS) >= BUD.L_ANIMAL0
        # The extra capital stays in cash when the market pays only the
        # animal's sticker price: it is tomorrow's feed for the funded stock.
        costs = (costs + animal_list[:, None].astype(i32)
                 * view.price[spec.I_WHEAT]).astype(i32)
        priority_values = _program_values(xp, costs, day)
        funded_values = xp.where((day <= 9) | service_list[:, None],
                                  priority_values, values)
        herd_first = xp.zeros(BUD.N_LISTS, bool)
        if PROGRAM_HERD_FIRST:
            herd_first = animal_list & (day <= PROGRAM_HERD_LAST_DAY)
        values = xp.where((day <= 9) | service_list[:, None] | repays
                          | herd_first[:, None],
                          funded_values, 0).astype(i32)
        if PROGRAM_FERT_SELL:
            # PROGFIX1 (3): the ENGINE buys ~4 fertilizer on d10-19 while it
            # sells 106; the port bought 22 back. No d10-19 fertilizer buy.
            no_fert = ((xp.arange(BUD.N_LISTS) == BUD.L_FERT)
                       & (day >= 10) & (day <= 19))
            values = xp.where(no_fert[:, None], 0, values).astype(i32)

    # ---- land: a priced, lumpy purchase [HEURISTIC, 1.3 / 0.3 / M1] ------
    # A quadrant is 25 tiles for 1,000 / 2,000 / 4,000 coins, and the candidates
    # it admits are exactly the seed and animal ranks past each list's pre-land
    # want: `values` and `costs` do not depend on the tile count at all (only
    # `wants` does), so the marginal worth of 25 more tiles is a re-read of the
    # same arrays at higher ranks and not a re-pricing. Hence the want vector
    # twice -- as the board stands, and as it would stand with the quadrant --
    # and `marginal_gain` over the difference.
    #
    # The horizon comes out of this for free, with no day constant anywhere
    # (0.3): `new_plant_units` returns 0 for a crop that cannot mature and
    # `fires_between` empties for an animal placed too late, so late in the
    # season every candidate behind the wall prices at zero and the valuation
    # collapses on its own.
    #
    # [HEURISTIC] The two-way compare of 1.3 is *grant* against *skip*; this
    # computes the grant leg exactly and omits the skip leg's displacement term
    # -- what the last `land_cost` coins would otherwise have bought on the
    # tiles the farm already owns. That leg needs a second `budget.grant`, and
    # three grants per `_derive` across two passes is ~+18% episode throughput
    # on its own, over the 15% gate. It is also a multi-day question (tomorrow's
    # purse re-buys what today's land displaced), and 1.1 assigns multi-day
    # residue to the genes: `land_bias` is scaled to `land_cost` precisely so a
    # gene that has learned "land displaces too much early" can demand up to a
    # full quadrant price of margin before the purchase clears.
    next_quad = xp.asarray(spec.LAND_ORDER)[xp.clip(view.nquad - 1, 0, 2)]
    is_pros = (xp.asarray(SERP_QUAD) == next_quad) & (kind == spec.KIND_LOCKED)
    n_pros = xp.sum(is_pros.astype(i32), dtype=i32)
    land_cost = xp.asarray(spec.LAND_PRICES)[xp.clip(view.nquad - 1, 0, 2)]
    # What the hour-0 purse still has to find [M2]. The reserve is held against
    # `view.money` alone and never against `rev1` [LAW, 1.5]: projected revenue
    # may fund the land *gap*, whose failure costs one purchase, but not the
    # reserve, whose whole purpose is to be certain. `money` is already net of
    # the hire bill and the reserve, so this is the coin order of 1.5 --
    # bill, reserve, land, greedy -- with the gap in land's place.
    land_gap = xp.maximum(land_cost - rev1, 0).astype(i32)
    if PLANT_ASK_ON:
        # Two asks, because the ask is the quantity land changes.  The
        # post-land leg may spend only the purse left after the land gap; both
        # purses are already net of the hire bill and tomorrow's crew reserve.
        macro_pre = _plant_ask(xp, view, macro, n_free, values, costs, money)
        macro_land = _plant_ask(
            xp, view, macro, n_free + n_pros, values, costs,
            xp.maximum(money - land_gap, 0).astype(i32))
        wants_pre = _wants(xp, view, macro_pre, n_free, sfree, a_have,
                           acquire_ok, wheat_short, fert_short)
        wants_land = _wants(xp, view, macro_land, n_free + n_pros, sfree,
                            a_have, acquire_ok, wheat_short, fert_short)
    else:
        wants_pre = _wants(xp, view, macro, n_free, sfree, a_have, acquire_ok,
                           wheat_short, fert_short)
        wants_land = _wants(xp, view, macro, n_free + n_pros, sfree, a_have,
                            acquire_ok, wheat_short, fert_short)
    # Priced against the post-reserve purse [LAW, 1.5]: a quadrant whose tiles
    # the farm could only stock by eating tomorrow's crew is worth less, and
    # the valuation must see that rather than being corrected afterwards. The
    # discount belongs on the funding side, never on the value -- a quadrant
    # paid for out of revenue that has not landed yet is still worth exactly
    # what its tiles will produce.
    n_units = _count_le(xp, xp.asarray(HIRE_BILLS), hire_bill)
    n_eff = land_reach(xp, n_units, xp.sum(pre_work.astype(i32), dtype=i32))
    land_value = BUD.marginal_gain(xp, values, costs, wants_pre,
                                   xp.maximum(wants_land - wants_pre, 0), n_eff,
                                   money - land_gap, BUD.LAND_LISTS)
    # `land_value` is the gain the quadrant's own tiles buy, computed against a
    # purse the price has already come off, so the comparison is to zero and
    # not to `land_cost` -- charging the price twice is the old bug in reverse.
    # `money >= land_gap` is exactly `money + rev1 >= land_cost`, and the
    # terminal gate is explicit rather than inherited from a zeroed purse:
    # `rev1` liquidates the whole shed on day 29 and would otherwise pay for a
    # quadrant with no day left to work it [LAW, 0.4].
    buy_land = ((view.nquad < 4) & (~terminal) & (money >= land_gap)
                & (money >= land_cost // LAND_OWN_DEN)
                & (land_value + macro.land_bias > 0)).astype(i32)
    if program_engine is not None:
        q_target = xp.asarray(_program_value(
            program_engine, "land_target", view.nquad), i32)
        due = view.nquad < q_target
        buy_land = xp.where(
            due, ((view.nquad < 4) & (~terminal)
                  & (money >= land_gap + program_service_cost)).astype(i32),
            xp.zeros_like(buy_land)).astype(i32)
    if PLANT_ASK_ON and PLANT_ASK_QUAD:
        in_window = ((day >= int(PLANT_ASK_DAYS[0]))
                     & (day <= int(PLANT_ASK_DAYS[1])))
        quad4 = ((view.nquad == 3) & (~terminal) & in_window
                 & (n_eff >= LAND_TILES) & (money >= land_cost))
        buy_land = xp.maximum(buy_land, quad4.astype(i32)).astype(i32)
    if Q4_PROG_ON:  # [SWITCH, Q4PROG1] DSM's d10 fourth quadrant
        # First day in the window whose post-bill, post-reserve purse (plus the
        # day's projected revenue, the `land_gap` law) covers the price. The
        # own-purse `land_value` / `land_bias` compare is bypassed: Q4 pays
        # through the shared book (DSMLAND2), which that compare cannot see.
        q4_win = ((day >= int(Q4_BUY_DAYS[0])) & (day <= int(Q4_BUY_DAYS[1])))
        q4_buy = ((view.nquad == 3) & (~terminal) & q4_win
                  & (money >= land_gap + int(Q4_BUY_KEEP)))
        buy_land = xp.maximum(buy_land, q4_buy.astype(i32)).astype(i32)
    q4v_fund = 0
    if Q4_VRP_ON:  # [SWITCH, Q4VRP1] Q4 funded by the VRP's banked hire saving
        # From Q4_VRP_DAY to Q4_VRP_LAST, buy the fourth quadrant when the purse
        # plus the bank release (runtime sets Q4_VRP_RELEASE = min(bank, price)
        # at dawn; 0 under Q4_VRP_FUND="visible") covers the land gap plus the
        # reserve. The released coins pay the land first and nothing else.
        rel = Q4_VRP_RELEASE if Q4_VRP_FUND == "true" else 0
        q4v = ((view.nquad == 3) & (~terminal) & (day >= int(Q4_VRP_DAY))
               & (day <= int(Q4_VRP_LAST))
               & (money + rel >= land_gap + int(Q4_VRP_RESERVE)))
        buy_land = xp.maximum(buy_land, q4v.astype(i32)).astype(i32)
        q4v_fund = xp.where((buy_land > 0) & (view.nquad == 3),
                            xp.minimum(rel, land_gap), 0).astype(i32)
    if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:
        # [SWITCH, MACRO_EXEC] The schedule says which day the quadrant is
        # bought; tiles the farm does not own cannot carry `tiles_target`. The
        # two hard gates stay -- a quadrant that does not exist or cannot be
        # paid for is not bought whatever the schedule asks -- so this replaces
        # the *valuation*, not the law. Site 2: on only under "full" and
        # "hands_herd_land" -- a quadrant calendar is a calendar too, and the
        # ramp modes exist to price it separately from the crew and the herd.
        if _macro_site(2):
            buy_land = xp.where(
                _macro_row(xp, day, "land") > 0,
                ((view.nquad < 4) & (~terminal)
                 & (money >= land_gap)).astype(i32),
                xp.zeros_like(buy_land)).astype(i32)
    purse = (money - buy_land * land_gap + q4v_fund).astype(i32)

    # The tiles the purchase makes free today [LAW, 0.3 / M1]. The engine
    # unlocks the quadrant synchronously inside the market phase of the
    # purchase's own turn (`_do_buy_land` charges `LAND_PRICES[nquad - 1]`,
    # appends `LAND_ORDER[nquad - 1]` and rewrites that quadrant's LOCKED tiles
    # to empty) and units act on every later turn, so its tiles are free slots
    # *today* -- 22 unit-turns per purchase were thrown away for want of this,
    # because `free_slot` read the hour-0 `kind` where the quadrant is LOCKED.
    prospective = is_pros & (buy_land > 0)
    free_slot = free_slot | prospective
    n_free = (n_free + buy_land * n_pros).astype(i32)
    wants = xp.where(buy_land > 0, wants_land, wants_pre)
    if PLANT_ASK_ON:
        macro = macro._replace(plant_target=xp.where(
            buy_land > 0, macro_land.plant_target,
            macro_pre.plant_target).astype(i32))
    # Shed room is passed *into* the greedy [LAW, 0.10], not clipped off its
    # answer. Wheat, fertilizer and animals all land in the shed and share one
    # room, so a grant made against unbounded wants and clipped afterwards
    # spends coins on units the shed cannot hold and strands them -- with all
    # three wanting the room at once, up to three times the room in units. The
    # old category walk never lost that money: it deducted only what it bought
    # and the next category got the rest. `grant` therefore carries the room
    # through both of its thresholds and its top-ups and returns a grant that
    # already satisfies it.
    n_buy = BUD.grant(xp, values, costs, wants, purse, room)
    if ENGINE_HERD_DEFER and ENGINE_GATE_ON:  # [SWITCH, ENGHERD1] herd defer
        # Latched ENGINE game only (the value is written through
        # `ENGINE_GATE_SET`): no BUY_ANIMAL on days
        # `ENGINE_HERD_FROM..ENGINE_HERD_FROM+K`. The first walk still grants
        # the animal lists (so every other list gets exactly the OFF answer),
        # then the animal buys and wants are dropped: the coin they held stays
        # in the purse, where only `ENGINE_PLATE_ADD`'s melon walk (which
        # spends purse less `keep_ep`) can reach it on the plate day. The herd
        # target stands, so purchases resume on day FROM+K+1 (delayed, never
        # cancelled); feed/care/fertilizer of owned animals do not move.
        hd_on = ((day >= int(ENGINE_HERD_FROM))
                 & (day <= int(ENGINE_HERD_FROM) + int(ENGINE_HERD_DEFER)))
        is_an = ((xp.arange(BUD.N_LISTS, dtype=i32) >= BUD.L_ANIMAL0)
                 & (xp.arange(BUD.N_LISTS, dtype=i32)
                    < BUD.L_ANIMAL0 + spec.N_ANIMALS))
        n_buy = xp.where(hd_on & is_an, 0, n_buy).astype(i32)
        wants = xp.where(hd_on & is_an, 0, wants).astype(i32)
    if program_engine is not None:
        # Unfunded animal asks must not leave empty cells reserved all day.
        # Keep the first grant intact; use only its remaining cash and the
        # cells left by animals actually funded, including owned shed stock.
        funded_macro = macro._replace(animal_want=a_have + n_buy[BUD.L_ANIMAL0:])
        seed_room = _seed_room(xp, funded_macro, n_free, sfree, a_have)[1]
        have = xp.minimum(macro.plant_target,
                           view.seeds + n_buy[BUD.L_SEED0:BUD.L_ANIMAL0])
        extra_seed = _program_seed_room(xp, xp.maximum(macro.plant_target - have, 0),
                                        xp.maximum(seed_room - xp.sum(have), 0))
        extra_want = xp.concatenate((xp.zeros(BUD.L_SEED0, i32), extra_seed,
                                      xp.zeros(spec.N_ANIMALS, i32)))
        remaining = xp.maximum(purse - BUD.spend(xp, costs, n_buy), 0)
        n_buy = n_buy + BUD.grant(xp, values, costs, extra_want, remaining, room)
        wants = xp.maximum(wants, n_buy)
    fill_target = macro.plant_target
    if PLANT_FILL_ON or PLANT_FILL_LATE_ON or WHEAT_LATE_ASK:
        # [SWITCH] see `_fill_wheat` above; [FREE FLOAT] see `WHEAT_LATE_ASK`.
        # The fill, funded by what the day's own grant left. `n_free` here
        # already carries a bought quadrant's tiles and `sfree`/`a_have` are
        # hour-0 facts a purchase does not move, so this is the `_wants` branch
        # the grant above actually used, asked for the tiles it left idle --
        # less the herd's forward reserve (`_fill_cap`).
        fill_cap = _fill_cap(xp, macro, _seed_room(xp, macro, n_free, sfree, a_have)[1])
        wl_live = None
        if WHEAT_LATE_ASK:                  # [FREE FLOAT] the dosed, gated arm
            # One mechanism with the two fills above: they are never measured
            # together and never compile together [LAW, as ROUTE_ORDER].
            assert not (PLANT_FILL_ON or PLANT_FILL_LATE_ON), \
                "WHEAT_LATE_ASK and the PLANT_FILL switches are one mechanism"
            fill_cap, wl_live = _wheat_late_cap(
                xp, view, macro, n_free, n_units,
                xp.sum(pre_work.astype(i32), dtype=i32), fill_cap)
        fill_target = _fill_wheat(xp, macro.plant_target, fill_cap)
        # Seed lists only: every other entry is a want of zero, so the second
        # walk cannot buy a hand's wheat, a fertilizer or an animal, and the
        # first walk's answer for those stands.
        if PLANT_FILL_LATE_ON:              # [SWITCH] see `PLANT_FILL_FROM_DAY`
            # The ramp keeps every tile it has.  Before `PLANT_FILL_FROM_DAY`
            # the fill is refused outright rather than merely capped: with
            # `fill_target` back at `macro.plant_target` the want below is
            # zero, `grant` over an all-zero want returns zeros, the
            # `xp.maximum` merges nothing into `n_buy` and `wants` is its own
            # maximum -- so `plant_eff`, `plant_crop` and every market row are
            # the OFF program's, day for day.
            live = view.day >= PLANT_FILL_FROM_DAY
            fill_target = xp.where(live, fill_target, macro.plant_target).astype(i32)
        w_fill = xp.maximum(fill_target - view.seeds, 0).astype(i32)
        if PLANT_FILL_LATE_ON:              # [SWITCH]
            w_fill = xp.where(live, w_fill, 0).astype(i32)
        if WHEAT_LATE_ASK:                  # [FREE FLOAT] see `_wheat_late_cap`
            # Same refusal, for the same reason: off the window, or on a day
            # the turn gate hands back nothing, the second grant must not run.
            w_fill = xp.where(wl_live, w_fill, 0).astype(i32)
        wants_fill = xp.concatenate([xp.zeros(BUD.L_SEED0, i32), w_fill,
                                     xp.zeros(spec.N_ANIMALS, i32)]).astype(i32)
        # The purse the fill may spend: everything the first grant committed
        # *outside* the seed lists comes off first, so the two walks together
        # never pass `purse` -- the seed lists are simply re-solved over the
        # coins they had plus the leftover, and `grant` is a threshold on a
        # list whose value per coin does not rise, so the re-solve can only
        # extend the first walk's answer, never undo it.
        keep = xp.concatenate([n_buy[:BUD.L_SEED0], xp.zeros(spec.N_CROPS, i32),
                               n_buy[BUD.L_SEED0 + spec.N_CROPS:]]).astype(i32)
        purse_fill = xp.maximum(purse - BUD.spend(xp, costs, keep), 0).astype(i32)
        n_fill = BUD.grant(xp, values, costs, wants_fill, purse_fill, room)
        is_seed = ((xp.arange(BUD.N_LISTS, dtype=i32) >= BUD.L_SEED0)
                   & (xp.arange(BUD.N_LISTS, dtype=i32) < BUD.L_SEED0 + spec.N_CROPS))
        n_buy = xp.where(is_seed, xp.maximum(n_fill, n_buy), n_buy).astype(i32)
        wants = xp.maximum(wants, wants_fill).astype(i32)
    if ENGINE_PLATE_ADD and ENGINE_GATE_ON:   # [SWITCH, ENGPLATE1] additive plate
        # N extra MELON plantings on day `ENGINE_PLATE_DAY`, on top of the
        # day's own mix: the tiles are the free ones left after builds and the
        # day's own ask (`_seed_room` less the herd reserve, `_fill_cap`), the
        # seed is a second walk over the MELON list only, funded from what the
        # first walk left (every other list keeps its grant), and melon is the
        # last crop in `plant_crop`'s prefix, so the added plantings take the
        # tiles AFTER every other crop's and move none of them.
        is_mel = (xp.arange(spec.N_CROPS, dtype=i32) == spec.I_MELON).astype(i32)
        ep_cap = _fill_cap(xp, macro, _seed_room(xp, macro, n_free, sfree, a_have)[1])
        # Free = not taken by what the day's own plan can actually plant (its
        # funded ask, `plant_eff`'s formula), not by the raw ask.
        ep_fund = xp.minimum(fill_target.astype(i32), view.seeds
                             + n_buy[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS]).astype(i32)
        ep_room = xp.maximum(ep_cap - xp.sum(ep_fund, dtype=i32), 0)
        ep_on = view.day == int(ENGINE_PLATE_DAY)
        ep_add = xp.where(ep_on, xp.minimum(int(ENGINE_PLATE_ADD), ep_room), 0).astype(i32)
        fill_target = xp.where(ep_on & (is_mel > 0), ep_fund + ep_add,
                               fill_target.astype(i32)).astype(i32)
        # Off the plate day the melon want is zero, so the second walk buys
        # nothing and the day is the OFF program's.
        w_ep = xp.where(ep_on, is_mel * xp.maximum(fill_target - view.seeds, 0),
                        0).astype(i32)
        wants_ep = xp.concatenate([xp.zeros(BUD.L_SEED0, i32), w_ep,
                                   xp.zeros(spec.N_ANIMALS, i32)]).astype(i32)
        l_mel = BUD.L_SEED0 + spec.I_MELON
        keep_ep = xp.where(xp.arange(BUD.N_LISTS, dtype=i32) == l_mel,
                           0, n_buy).astype(i32)
        purse_ep = xp.maximum(purse - BUD.spend(xp, costs, keep_ep), 0).astype(i32)
        n_ep = BUD.grant(xp, values, costs, wants_ep, purse_ep, room)
        n_buy = xp.where(xp.arange(BUD.N_LISTS, dtype=i32) == l_mel,
                         xp.maximum(n_ep, n_buy), n_buy).astype(i32)
        wants = xp.maximum(wants, wants_ep).astype(i32)
    if ASK_FILL_ON and ask_fill:
        # Only pass B, after the planner has selected and funded its crew.
        animals = a_have + n_buy[BUD.L_ANIMAL0:BUD.L_ANIMAL0 + spec.N_ANIMALS]
        stocked = _share(xp, animals, sfree, BEFORE_STRUCT)
        builds = (xp.minimum(xp.maximum(animals - stocked, 0), macro.animal_want)
                  * a_keep // DEFER_ONE).astype(i32)
        seed_cap = n_free - xp.sum(_share(xp, builds, n_free, BEFORE_ALL), dtype=i32)
        fill_target, n_buy = _ask_fill(
            xp, view, fill_target, seed_cap, values, costs, n_buy, purse)
        wants = xp.maximum(wants, n_buy).astype(i32)
    if Q4_PROG_ON:  # [SWITCH, Q4PROG1] the fourth quadrant's crop program
        # Target census of the Q4 quadrant per crop per day (`_q4_table`); the
        # deficit against what Q4 already carries is ADDED to the day's funded
        # mix on the free tiles the day's own plan leaves (`_fill_cap` less the
        # funded ask), and its seeds are bought from what the grant left. Wheat
        # and carrot are one-shot crops, so a harvest drops the census and the
        # tile is re-planted: the 4-day relay. Every other list keeps its grant.
        q4_tile = xp.asarray(SERP_QUAD) == int(spec.LAND_ORDER[2])
        q4_have = xp.stack([xp.sum((is_plant & q4_tile & (crop == c)).astype(i32),
                                   dtype=i32) for c in range(spec.N_CROPS)]).astype(i32)
        q4_tgt = xp.asarray(_q4_table(), i32)[xp.clip(day, 0, 29)]
        q4_mat = (day + xp.asarray(spec.CROP_FIRST_YIELD_DAY, i32) <= VAL.pay_day())
        q4_live = (((view.nquad >= 4) | ((view.nquad == 3) & (buy_land > 0))) & (~terminal)
                   & (day >= int(Q4_BUY_DAYS[0])) & (day <= int(Q4_PLANT_LAST_DAY)))
        q4_add = xp.where(q4_live & q4_mat, xp.maximum(q4_tgt - q4_have, 0), 0).astype(i32)
        q4_seed = n_buy[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS]
        q4_fund = xp.minimum(fill_target.astype(i32), view.seeds + q4_seed).astype(i32)
        q4_cap = _fill_cap(xp, macro, _seed_room(xp, macro, n_free, sfree, a_have)[1])
        q4_room = xp.maximum(q4_cap - xp.sum(q4_fund, dtype=i32), 0).astype(i32)
        q4_before = xp.cumsum(q4_add, dtype=i32) - q4_add
        q4_add = xp.clip(q4_add, 0, xp.maximum(q4_room - q4_before, 0)).astype(i32)
        q4_spare = xp.maximum(view.seeds + q4_seed - q4_fund, 0).astype(i32)
        q4_need = xp.maximum(q4_add - q4_spare, 0).astype(i32)
        q4_left = xp.maximum(purse - BUD.spend(xp, costs, n_buy), 0).astype(i32)
        q4_j = xp.arange(PJ.K, dtype=i32)
        q4_got = []
        for c in Q4_SEED_ORDER:
            l = BUD.L_SEED0 + c
            cum = xp.cumsum(xp.maximum(costs[l].astype(i32), 1), dtype=i32)
            base = n_buy[l]
            at_base = xp.where(base > 0, cum[xp.clip(base - 1, 0, PJ.K - 1)], 0)
            extra = xp.where(q4_j >= base, cum - at_base, BUD.VALUE_CAP)
            ok = (extra <= q4_left) & (q4_j < base + q4_need[c])
            got = xp.sum(ok.astype(i32), dtype=i32).astype(i32)
            spent = xp.where(got > 0, cum[xp.clip(base + got - 1, 0, PJ.K - 1)] - at_base, 0)
            q4_left = (q4_left - spent).astype(i32)
            q4_got.append((c, got))
        q4_buy_v = xp.zeros(spec.N_CROPS, i32)
        for c, got in q4_got:
            q4_buy_v = q4_buy_v + got * (xp.arange(spec.N_CROPS, dtype=i32) == c).astype(i32)
        q4_eff = xp.minimum(q4_add, q4_spare + q4_buy_v).astype(i32)
        fill_target = xp.where(xp.sum(q4_eff) > 0, q4_fund + q4_eff,
                               fill_target.astype(i32)).astype(i32)
        n_buy = (n_buy + xp.concatenate([xp.zeros(BUD.L_SEED0, i32), q4_buy_v,
                                         xp.zeros(spec.N_ANIMALS, i32)])).astype(i32)
        wants = xp.maximum(wants, n_buy).astype(i32)
    mr_eff = None
    if ESWORK_THETA is not None and ask_fill:  # [WHEATMIX1 / ESWORK1] relay wheat count + its seed, OUTSIDE the asks
        # Today's relay plantings = the gene cadence (`_mr_want`) capped by the free
        # Q1-3 tiles the day's own funded ask leaves (`_fill_cap` less the
        # funded fill, as ENGPLATE/Q4PROG); the seed is a second walk over the
        # wheat list from what the grant left, exactly the Q4 relay's.
        mr_fund = xp.minimum(fill_target.astype(i32), view.seeds
                             + n_buy[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS]).astype(i32)
        mr_cap = _fill_cap(xp, macro, _seed_room(xp, macro, n_free, sfree, a_have)[1])
        mr_room = xp.maximum(mr_cap - xp.sum(mr_fund, dtype=i32), 0).astype(i32)
        mr_add = xp.where(terminal, 0, xp.minimum(_mr_want(xp, view), mr_room)).astype(i32)
        l_w = BUD.L_SEED0 + spec.I_WHEAT
        mr_spare = xp.maximum(view.seeds[spec.I_WHEAT] + n_buy[l_w] - mr_fund[spec.I_WHEAT], 0)
        mr_need = xp.maximum(mr_add - mr_spare, 0).astype(i32)
        mr_left = xp.maximum(purse - BUD.spend(xp, costs, n_buy), 0).astype(i32)
        mr_j = xp.arange(PJ.K, dtype=i32)
        mr_cum = xp.cumsum(xp.maximum(costs[l_w].astype(i32), 1), dtype=i32)
        mr_b0 = n_buy[l_w]
        mr_at = xp.where(mr_b0 > 0, mr_cum[xp.clip(mr_b0 - 1, 0, PJ.K - 1)], 0)
        mr_ex = xp.where(mr_j >= mr_b0, mr_cum - mr_at, BUD.VALUE_CAP)
        mr_got = xp.sum(((mr_ex <= mr_left) & (mr_j < mr_b0 + mr_need)).astype(i32),
                        dtype=i32).astype(i32)
        mr_eff = xp.minimum(mr_add, mr_spare + mr_got).astype(i32)
        n_buy = (n_buy + (xp.arange(BUD.N_LISTS, dtype=i32) == l_w).astype(i32)
                 * mr_got).astype(i32)
        wants = xp.maximum(wants, n_buy).astype(i32)
    if (CREW_RELAY_ON and ask_fill) or (FILL_WORK_ON and ask_fill) or (  # [SWITCH, CREWRELAY1/FILLWORK1] final pass only
            RELAY_FILL_ON and not CREW_RELAY_ON and (ask_fill or not RELAY_PASS_B)):  # [SWITCH, RELAYFILL1]
        fill_target, n_buy = _relay_fill(xp, view, macro, fill_target, n_buy, costs, purse,
                                         _seed_room(xp, macro, n_free, sfree, a_have)[1],
                                         n_units, xp.sum(pre_work.astype(i32), dtype=i32))
        wants = xp.maximum(wants, n_buy).astype(i32)
    rp_cand = None
    _wc_rp = WHEAT_CYCLE_H3_ON and WHEAT_CYCLE_RP_ON and not REPLANT_SAME_TURN_ON
    if REPLANT_SAME_TURN_ON or _wc_rp:     # [SWITCH] see the block above
        # The tiles a harvest frees today, inside the window, whose crop can
        # still mature. `harvest_one & free_slot` is `harvest_one & ~mel_bank`
        # by construction -- a melon tile the banking switch holds back is not
        # a slot the day develops and is not one the day replants either.
        rp_win = ((view.day >= REPLANT_FROM_DAY)
                  & (view.day <= REPLANT_TO_DAY))
        rp_mature = (view.day + xp.asarray(spec.CROP_FIRST_YIELD_DAY, i32)
                     <= VAL.pay_day())
        rp_cand = harvest_one & free_slot & rp_win & rp_mature[crop]
        if _wc_rp:                         # [SWITCH, WHEATCYCLE1] early wheat tiles only
            rp_cand = (harvest_one & free_slot & _wc_early
                       & (view.day + 3 <= VAL.pay_day()))
        rp_n = xp.stack([xp.sum((rp_cand & (crop == c)).astype(i32), dtype=i32)
                         for c in range(spec.N_CROPS)]).astype(i32)
        # The seed floor, funded exactly as `PLANT_FILL`'s second walk is: seed
        # lists only, over the purse less everything the first grant committed
        # outside them, so the two walks together never pass `purse` and the
        # herd's own candidates keep the answer the first walk gave them.
        w_rp = xp.maximum(xp.maximum(macro.plant_target, rp_n)
                          - view.seeds, 0).astype(i32)
        if _wc_rp:                         # on top of the day's own ask
            w_rp = xp.maximum(macro.plant_target + rp_n - view.seeds, 0).astype(i32)
        wants_rp = xp.concatenate([xp.zeros(BUD.L_SEED0, i32), w_rp,
                                   xp.zeros(spec.N_ANIMALS, i32)]).astype(i32)
        keep_rp = xp.concatenate([n_buy[:BUD.L_SEED0], xp.zeros(spec.N_CROPS, i32),
                                  n_buy[BUD.L_SEED0 + spec.N_CROPS:]]).astype(i32)
        purse_rp = xp.maximum(purse - BUD.spend(xp, costs, keep_rp), 0).astype(i32)
        n_rp = BUD.grant(xp, values, costs, wants_rp, purse_rp, room)
        is_seed_rp = ((xp.arange(BUD.N_LISTS, dtype=i32) >= BUD.L_SEED0)
                      & (xp.arange(BUD.N_LISTS, dtype=i32)
                         < BUD.L_SEED0 + spec.N_CROPS))
        n_buy = xp.where(is_seed_rp, xp.maximum(n_rp, n_buy), n_buy).astype(i32)
        wants = xp.maximum(wants, wants_rp).astype(i32)
    # Backstop only: `grant` guarantees wheat + fertilizer + animals <= room,
    # so this never binds. It is kept because it is the engine's own rule --
    # the market clips BUY_PRODUCT and BUY_ANIMAL to the room left, slot by
    # slot, in this fixed BUY-row order -- and a future candidate list that
    # forgot to declare itself shed-bound would be caught here rather than
    # over-committing the shed.
    wheat_buy = xp.minimum(n_buy[BUD.L_WHEAT], room).astype(i32)
    if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:
        # [SWITCH, MACRO_EXEC] Site 9, the market-PURCHASE channel
        # [WHEAT-REBUY]: the schedule's whole day of BUY_PRODUCT WHEAT, as a
        # floor on the row the budget walk granted, resolved on the one buy
        # row our action interface has.
        if _macro_site(9):
            wheat_buy = _rebuy_extra(
                xp, view, price_table, wheat_buy, room, purse, costs, n_buy,
                _macro_row(xp, view.day, "buy")[spec.I_WHEAT] - wheat_buy)
    if REBUY_ON:                       # [SWITCH, WHEAT-REBUY] own-clock arm
        wheat_buy = _rebuy_extra(xp, view, price_table, wheat_buy, room, purse,
                                 costs, n_buy, _rebuy_ask(xp, view.day))
    if MIRROR_OPEN_ON:                 # [SWITCH, MIRROR_OPEN] the feed leg
        # The melon plate pays for its tiles with WHEAT last (`_MELON_PAY_RANK`)
        # but it still pays, and the animals eat either way.  Same clipped,
        # purse-walked re-buy as the own-clock arm: what the shed and the purse
        # refuse is simply not bought.
        wheat_buy = _rebuy_extra(xp, view, price_table, wheat_buy, room, purse,
                                 costs, n_buy, _mirror_wheat_ask(xp, view.day))
    fert_bought = xp.minimum(n_buy[BUD.L_FERT], room - wheat_buy).astype(i32)
    seed_buy = n_buy[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS]
    if seed_extra is not None:          # [ACTIONRL11] the wide head's seed ask
        seed_buy, seed_spent = _residual_seed_extra(
            xp, seed_buy, costs, n_buy, purse, fill_target, view.seeds, seed_extra)
    # The three animal slots walk the room in the engine's own slot order, one
    # after another, exactly as the market clips them (`_share`).
    a_left = xp.maximum(room - wheat_buy - fert_bought, 0).astype(i32)
    a_buy = _share(xp, n_buy[BUD.L_ANIMAL0:BUD.L_ANIMAL0 + spec.N_ANIMALS],
                   a_left, BEFORE_ALL)
    # Section 7's purchase shortfall: what the wanted-but-ungranted candidates
    # were worth. `grant` never grants past a list's want, so the ungranted
    # candidates are exactly ranks n_buy..wants of each list -- and they are
    # priced at the values the greedy itself saw, which is the capped ones.
    # Eight lists of at most K capped values stay far inside int32.
    j = xp.arange(PJ.K, dtype=i32)
    ungranted = (j[None, :] >= n_buy[:, None]) & (j[None, :] < wants[:, None])
    purchase_shortfall = xp.sum(xp.where(ungranted, xp.clip(values, 0, BUD.VALUE_CAP), 0),
                                dtype=i32).astype(i32)
    # What the walk did not spend [PRESTOCK]. `purse` is already net of the
    # hire bill, `cash_reserve` and the land gap, so this is the one pot a
    # purchase moved a day earlier may draw on without touching the reserve --
    # and it is the *grant's* leftover, so tonight's buy can never displace a
    # candidate today wanted more. Coins the day's own lots fetch are
    # deliberately not counted: they land at turns 3/10/18, before
    # `TURN_PRESTOCK`, but they are a projection and the reserve's whole value
    # is that it is certain (the same reasoning as `land_gap` vs `rev1`).
    purse_left = xp.maximum(purse - BUD.spend(xp, costs, n_buy), 0).astype(i32)
    if seed_extra is not None:
        # The top-up was paid out of exactly this pot, so the pot must know.
        purse_left = xp.maximum(purse_left - seed_spent, 0).astype(i32)

    # `fill_target` is `macro.plant_target` itself with the switch off, so this
    # is the expression it always was.
    plant_eff = xp.minimum(fill_target, view.seeds + seed_buy)
    wheat_avail = shed_wheat + wheat_buy
    fert_avail = view.shed[spec.I_FERT] + fert_bought
    a_avail = (a_have + a_buy).astype(i32)

    # ---- clamp every task set to what the budget actually bought ----------
    # Feed rationing by replacement value [EXACT-OPT, 0.6]: only the feeds that
    # cleared 1.4's value test compete, and when the wheat the walk actually
    # bought falls short of them the animals worth most are fed first --
    # `feed_rank` ranks `feed_pass` by `feed_value` above, serpentine position
    # breaking exact ties.
    want_feed = feed_pass & (feed_rank < wheat_avail)
    # CARE [0.11]: banks +1 only when cared and fed today, so it rides a feed
    # -- and `care_ok` above is what put that feed on the list, so the two can
    # never disagree about whether the care pays. It cashes on the first fire
    # after today's eod, if fed that day (`bank_feed` feeds every fire day
    # with a bank waiting), is worth min(max_held, yield + 1 + bank), and the
    # animal is harvested whenever it holds units. The CARE op's own labour is
    # priced in coins by `v_care` below and admitted against the turn budget
    # like any other task [1.6].
    want_care = want_feed & care_ok

    n_fert_eff = xp.minimum(n_fert_want, fert_avail)
    want_fert = fert_cand & (fert_rank < n_fert_eff)
    if STRAW_SWAP1_ON:
        _swap_day = ((_as(xp, day) >= xp.asarray(10, i32))
                     & (_as(xp, day) <= xp.asarray(24, i32)))
        _sel_wheat = want_fert & (crop == spec.I_WHEAT)
        _free_straw = fert_cand & ~want_fert & (crop == spec.I_STRAWBERRY)
        _drop = _sel_wheat & (_rank_by(xp, _sel_wheat, -fert_val) == 0)
        _add = _free_straw & (_rank_by(xp, _free_straw, fert_val) == 0)
        _do_swap = (_swap_day & xp.any(_sel_wheat) & xp.any(_free_straw))
        want_fert = xp.where(_do_swap, (want_fert & ~_drop) | _add,
                             want_fert)

    # An ongoing crop fires whether or not it is watered; only the fertilized
    # case pays (+2 instead of +1), so a fertilized crop firing tonight is
    # watered even when it is not thirsty. FERTILIZE precedes WATER in the
    # chain, so today's application counts.
    crop_fire = (is_plant & (c_ongoing == 1) & survival_pays
                 & VAL.crop_fires_on(xp, view.t_day, crop, day + 1))
    want_water = want_water | (crop_fire & (view.t_water == 0) & ((view.t_fert >= day) | want_fert))

    # *Where* the day develops [R3]. `slot_rank` chooses which free tiles get
    # built on and planted, and the 12-17 tile-days of watering and harvesting
    # that follow inherit that choice -- so a sweep-ordered rank scatters the
    # season's whole labour over the board. `compact` orders the same tiles by
    # distance from the shed-access spawn instead; at `compact = 0` `_rank_near`
    # is `_rank` bit for bit and nothing moves.
    compact_eff = macro.compact
    if ROUTE_EFF_ON:
        # [SWITCH, ROUTE_EFF] a floor, never a cap: the gene keeps every day it
        # already asks to compact harder than `ROUTE_EFF_COMPACT`.
        compact_eff = xp.maximum(xp.asarray(macro.compact).astype(i32),
                                 i32(ROUTE_EFF_COMPACT))
    dev_key = _dev_key(xp, compact_eff)
    slot_rank = _rank_near(xp, free_slot, dev_key)
    # Structures already standing are stocked before new ones are built [0.8],
    # and the three kinds are assigned in **one pass per structure kind**, in
    # list order: cow and sheep both want a free pasture, so ranking them
    # independently would hand two animals the same tile.
    place_here = xp.zeros(N_T, dtype=bool)
    place_kind = xp.zeros(N_T, i32)
    # `sfree` is the very room this walks -- the free structures of the kind
    # each animal needs, off the same `st_free` masks -- so the counts come
    # out of one `_share` and only the per-tile rank window is unrolled. The
    # kind's first tile is the rank its predecessors of the *same* structure
    # left standing, i.e. their prefix clipped to the room.
    n_place = _share(xp, a_avail, sfree, BEFORE_STRUCT)
    p_start = xp.minimum(_prefix(xp, a_avail, BEFORE_STRUCT), sfree).astype(i32)
    for _si, _k in enumerate((spec.KIND_COOP, spec.KIND_PASTURE)):
        mask = st_free[_si]
        rank = _rank_near(xp, mask, dev_key)
        for a in range(spec.N_ANIMALS):
            if int(spec.ANIMAL_STRUCT[a]) != _k:
                continue
            hit = mask & (rank >= p_start[a]) & (rank < p_start[a] + n_place[a])
            place_here = place_here | hit
            place_kind = xp.where(hit, a, place_kind)

    # What the standing structures could not take is built, in the same list
    # order, over what is left of the free tiles. Capped at the day's own
    # acquisition per kind [LAW, 0.8]: shed stock is placed, not built for.
    # ... and demoted by the same scale the purchase side is [g10]: a build
    # takes a free tile ahead of every planting (`plant_rank` below) as well as
    # the coins, so deferring the purchase alone would still let a day with
    # stock in the shed put a coop where the crew's wheat should go. Standing
    # structures are still stocked (`n_place`), which is free.
    b_want = (xp.minimum(xp.maximum(a_avail - n_place, 0), macro.animal_want)
              * a_keep // DEFER_ONE).astype(i32)
    nb = _share(xp, b_want, n_free, BEFORE_ALL)
    n_build = xp.sum(nb, dtype=i32).astype(i32)
    build_here = free_slot & (slot_rank < n_build)
    build_kind = xp.clip(_count_le(xp, xp.cumsum(nb, dtype=i32), slot_rank),
                         0, spec.N_ANIMALS - 1)
    place_kind = xp.where(build_here, build_kind, place_kind).astype(i32)

    plant_rank = slot_rank - n_build
    p_cum = xp.cumsum(plant_eff)
    if program_engine is not None and PROGRAM_PLANT_SHARE:
        # PROGFIX1 (1b): crop order handed every scarce slot to wheat, so the
        # carrot/tomato seed the programme bought sat in the shed. Share the
        # slots across crops in proportion to the funded plantings instead.
        slots = xp.maximum(xp.sum(free_slot.astype(i32)) - n_build, 0).astype(i32)
        p_cum = xp.cumsum(_program_seed_room(xp, plant_eff.astype(i32), slots))
    plant_here = free_slot & (plant_rank >= 0) & (plant_rank < p_cum[-1])
    if open_board():
        # The opening's melon goes on the tiles *nearest the shed* [SWITCH].
        # `plant_rank` is the `compact` sweep order, and melon is the last crop
        # in `spec.CROPS`, so the shipped boundary puts the whole opening at
        # the far end of the walk -- which is what made v1 miss its lot, and
        # what makes the day-10 excursion cheap or dear here. `DIST_SHED` is
        # the key `compact` itself buckets on, so this is the same ordering the
        # router already understands, applied to the crop choice rather than to
        # which tiles get developed. Which tiles are planted does not move
        # (`plant_here` is untouched); only which crop each planted tile gets.
        near_rank = _rank_near(xp, plant_here, xp.asarray(DIST_SHED))
        is_mel = plant_here & (near_rank < plant_eff[spec.I_MELON])
        # The other crops keep the shipped order among themselves: a tile's
        # rank is its sweep rank less the melon tiles that outrank it, and the
        # boundary it is cut against is `plant_eff` with melon taken out.
        mel_before = xp.sum((is_mel[None, :]
                             & (plant_rank[None, :] < plant_rank[:, None])).astype(i32),
                            axis=1).astype(i32)
        p_cum_o = xp.cumsum(xp.where(xp.arange(spec.N_CROPS, dtype=i32) == spec.I_MELON,
                                     0, plant_eff))
        crop_o = xp.clip(_count_le(xp, p_cum_o, xp.maximum(plant_rank - mel_before, 0)),
                         0, spec.N_CROPS - 1)
        plant_crop = xp.where(
            view.day == MELON_OPEN_DAY,
            xp.where(is_mel, spec.I_MELON, crop_o),
            xp.clip(_count_le(xp, p_cum, xp.maximum(plant_rank, 0)),
                    0, spec.N_CROPS - 1)).astype(i32)
    else:
        plant_crop = xp.clip(_count_le(xp, p_cum, xp.maximum(plant_rank, 0)),
                             0, spec.N_CROPS - 1)

    # ---- REPLANT_SAME_TURN: the rotation's own plantings [SWITCH] ---------
    # The seeds the base plan did not spend -- and under the switch those are
    # exactly the ones the floor above bought -- are put back on the tiles the
    # day's harvests free, one crop at a time, with the crop the tile carried.
    # Never on an empty or weeded tile (`rp_cand` is `harvest_one`), never on a
    # tile the base plan already plants or a build takes, and never more per
    # crop than that crop's leftover seed.  `pl_mask`/`pl_crop` are the OFF
    # names themselves when the switch is off, so the candidate list below is
    # built from the same two objects it always was [LAW].
    pl_mask, pl_crop = plant_here, plant_crop
    if REPLANT_SAME_TURN_ON or _wc_rp:                           # [SWITCH]
        rp_seed = xp.maximum(view.seeds + seed_buy - plant_eff, 0).astype(i32)
        rp_new = rp_cand & ~plant_here & ~build_here & ~place_here
        rp_here = xp.zeros(N_T, dtype=bool)
        for _c in range(spec.N_CROPS):
            _m = rp_new & (crop == _c)
            rp_here = rp_here | (_m & (_rank_near(xp, _m, dev_key) < rp_seed[_c]))
        pl_mask = plant_here | rp_here
        pl_crop = xp.where(rp_here, crop, plant_crop).astype(i32)

    mr_here = None
    if mr_eff is not None:  # [WHEATMIX1 / ESWORK1] relay wheat on the Q1-3 free tiles the day's own plan leaves
        mr_seed = xp.maximum(view.seeds[spec.I_WHEAT] + seed_buy[spec.I_WHEAT]
                             - plant_eff[spec.I_WHEAT], 0).astype(i32)
        mr_n = xp.minimum(mr_eff, mr_seed).astype(i32)
        mr_slot = (free_slot & ~pl_mask & ~build_here & ~place_here
                   & (xp.asarray(SERP_QUAD) != int(spec.LAND_ORDER[2])))
        mr_here = mr_slot & (_rank_near(xp, mr_slot, dev_key) < mr_n)
        pl_mask = pl_mask | mr_here
        pl_crop = xp.where(mr_here, spec.I_WHEAT, pl_crop).astype(i32)

    m_place = place_here | build_here

    pf_feed = None
    if PLACEFEED_ON:   # [SWITCH, PLACEFEED1] feed+care the placement night
        pf_prod = a_prod[place_kind]
        pf_ok = (m_place & (place_kind != (spec.I_COW - spec.I_GOOSE))
                 & (day + xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[place_kind] <= VAL.pay_day())
                 & (view.price[pf_prod] > view.price[spec.I_WHEAT]) & ~xp.asarray(terminal, bool))
        pf_ok = pf_ok & (day >= PF_DAY_MIN) & (day <= PF_DAY_MAX)
        if PF_HERD_MAX < 999:   # [PLACEFEED3] dawn sheep+goose head count gate
            pf_an = ((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE)) & (view.occ >= 0)
            pf_herd = xp.sum((pf_an & (view.occ != spec.I_COW - spec.I_GOOSE)).astype(i32),
                             dtype=i32).astype(i32)
            pf_ok = pf_ok & (pf_herd < PF_HERD_MAX)
        pf_n = xp.sum(pf_ok.astype(i32), dtype=i32).astype(i32)
        pf_fed = xp.sum(want_feed.astype(i32), dtype=i32).astype(i32)
        pf_room = xp.maximum(room - wheat_buy - fert_bought
                             - xp.sum(a_buy, dtype=i32), 0).astype(i32)
        pf_left = purse_left   # the grant's leftover, net of any seed top-up
        pf_ask = pf_n - xp.maximum(wheat_avail - pf_fed, 0)
        pf_keep = xp.asarray(0, i32)
        if PF_PUMPSAFE_ON:   # [PLACEFEED3] never break the opening pump's `wheat_buy == 0`
            _pon = ((PROGRAM_PUMP_UNITS > OPEN_PUMP_KEEP) if PROGRAM_ENGINE_ON
                    else _sw(macro, "OPEN_PUMP_ON"))
            if _pon is not False:
                pf_pump = (xp.asarray(_pon, bool) & (day == OPEN_PUMP_DAY)
                           & (_as(xp, view.money) >= OPEN_PUMP_MIN_MONEY) & (wheat_buy == 0))
                pf_ask = xp.where(pf_pump, 0, pf_ask)
                pf_keep = xp.where(pf_pump, OPEN_PUMP_KEEP, 0).astype(i32)
        if PF_NOBUY_ON:
            pf_ask = xp.zeros_like(pf_ask)
        wheat_buy, pf_cost = _pf_wheat(
            xp, view, price_table, wheat_buy, wheat_buy + pf_room, pf_left, pf_ask)
        wheat_avail = shed_wheat + wheat_buy
        purse_left = xp.maximum(purse_left - pf_cost, 0).astype(i32)
        pf_rank = (xp.cumsum(pf_ok.astype(i32), dtype=i32) - pf_ok.astype(i32)).astype(i32)
        pf_feed = pf_ok & (pf_rank < wheat_avail + pf_keep - pf_fed)

    # ---- pack the per-tile op chain --------------------------------------
    # Ordering inside a tile matters:
    #   FEED/CARE before end-of-day production is banked,
    #   COLLECT before FERTILIZE (this tile's animal may supply it),
    #   FERTILIZE before WATER (the water bonus reads fertilized_until_day),
    #   WATER before HARVEST (watering still adds yield on the harvest day),
    #   HARVEST/DIG before PLANT (both free the tile),
    #   PLANT then WATER (a fresh seed weeds tonight if left dry).
    a_item = (xp.asarray(spec.I_GOOSE, i32) + place_kind).astype(i32)
    build_op = xp.where(xp.asarray(spec.ANIMAL_STRUCT)[place_kind] == spec.KIND_COOP,
                        O.OP_BUILD_COOP, O.OP_BUILD_PASTURE).astype(i32)

    # ---- CLIP_CAP: the shed's room, spent dearest-first [SWITCH] ---------
    # Computed here, before the chain is packed, because the suppression has to
    # remove the HARVEST op itself and not merely its value: a tile admitted
    # for a harvest it will not take spends a turn for nothing. OFF the three
    # names below are the masks they always were and nothing else is traced.
    # [SWITCH-GENE] The cap is a MASK, so the gene rides on the vector: the three
    # admission masks are `& ~cc_sup` under it and the masks they always were
    # without it, so a gene that asks for OFF packs the chain the OFF day packs,
    # op for op.  Concrete OFF (a tree with the constant pinned back) still
    # computes nothing at all.
    h_one_a, h_ong_a, h_anim_a = harvest_one, harvest_ong, want_harv_animal
    col_a = want_collect
    _cc_on = _sw(macro, "CLIP_CAP_ON")
    if _cc_on is not False:
        cc_any = harvest_one | harvest_ong | want_harv_animal
        # What the tile banks tonight and what one of those units is worth.
        # `bonus_water` is the extra unit an in-window watering adds, the same
        # term `v_harvest` books below; an animal banks its held yield.
        cc_bonus = (want_water & bonus_water).astype(i32)
        cc_qty = (xp.where(harvest_one | harvest_ong, view.t_yield + cc_bonus, 0)
                  + xp.where(want_harv_animal, view.t_yield, 0)).astype(i32)
        cc_px = xp.where(want_harv_animal, view.price[an_prod], view.price[crop]).astype(i32)
        # Exclusive cumulative volume in descending unit-price order, ties to
        # the lower (serpentine) index -- `_rank_by`'s own ordering, summed over
        # quantities instead of counted, which a rank cannot do.
        cc_idx = xp.arange(N_T, dtype=i32)
        cc_both = cc_any[None, :] & cc_any[:, None]
        cc_ahead = cc_both & ((cc_px[None, :] > cc_px[:, None])
                              | ((cc_px[None, :] == cc_px[:, None])
                                 & (cc_idx[None, :] < cc_idx[:, None])))
        cc_cum = xp.sum(xp.where(cc_ahead, cc_qty[None, :], 0), axis=1, dtype=i32)
        # Strictly-ahead volume, so the tile that straddles the boundary keeps
        # its harvest: the cap is a floor on the carry, never a ceiling.
        # The room the harvest actually competes for. Measured on a clipping
        # night the crew comes home with 104.9 units, of which **18.80 are
        # FERTILIZER** -- one unit per COLLECT_FERT, the cheapest thing in the
        # haul at 26 coins a unit -- so a cap that counted harvests alone sat
        # at 86 of 100 and never bound (the first arm read the clip 17.80 u /
        # 1,419 coins against 17.80 / 1,415 OFF: inert). The collections are
        # charged rather than suppressed (unless [SWITCH `CLIP_FERT_SKIP_ON`]
        # below, which measured -454 on the ENG22 kill gate and -13 on
        # POOLED180 -- `docs/strategy/2026-09-16-shedclip2.md`): `_candidates`
        # may source a FERTILIZE from the very animal the COLLECT stands on, so
        # dropping the op can silently no-op the application behind it.
        cc_ncol = xp.sum(want_collect.astype(i32), dtype=i32).astype(i32)
        cc_room = xp.asarray(CLIP_CAP_ROOM, i32)
        cc_charge = cc_ncol
        if CLIP_FERT_SKIP_ON:
            # [SWITCH (b)] A clipping night is one whose whole haul -- the
            # admitted harvest volume plus one unit per collection -- will not
            # fit. On such a night drop the collections instead of charging
            # them, and hand the room they were holding to the harvest.
            cc_binds = ((xp.sum(xp.where(cc_any, cc_qty, 0), dtype=i32).astype(i32)
                         + cc_ncol) > cc_room)
            if CLIP_CAP_TERMINAL_OFF:
                cc_binds = cc_binds & ~terminal
            col_a = _sw_pick(xp, _cc_on, lambda: want_collect & ~cc_binds,
                             want_collect)
            cc_charge = xp.where(cc_binds, xp.asarray(0, i32), cc_ncol).astype(i32)
        cc_budget = xp.maximum(cc_room - cc_charge, 0).astype(i32)
        # [SWITCH (c)] strictly-ahead volume keeps the straddling tile (a floor
        # on the carry); `cc_cum + cc_qty` cuts it (a ceiling).
        cc_sup = cc_any & ((cc_cum + cc_qty > cc_budget) if CLIP_CAP_STRICT_ON
                           else (cc_cum >= cc_budget))
        if CLIP_CAP_TERMINAL_OFF:               # [SWITCH (a)]
            cc_sup = cc_sup & ~terminal
        h_one_a = _sw_pick(xp, _cc_on, lambda: harvest_one & ~cc_sup, harvest_one)
        h_ong_a = _sw_pick(xp, _cc_on, lambda: harvest_ong & ~cc_sup, harvest_ong)
        h_anim_a = _sw_pick(xp, _cc_on, lambda: want_harv_animal & ~cc_sup,
                            want_harv_animal)

    dig_mask = is_weed
    if final_slot is not None:                                   # [SWITCH, LATE_EXEC]
        # Dug only under a planting or a build, and never under units the
        # day does not harvest (CLIP_CAP may have dropped the HARVEST).
        dig_mask = is_weed | (final_slot & (pl_mask | build_here)
                              & ~(harvest_ong & ~h_ong_a))
    cands = [
        (want_feed,     xp.full((N_T,), O.OP_FEED, i32),         zero, zero),
        (want_care,     xp.full((N_T,), O.OP_CARE, i32),         zero, zero),
        (col_a,         xp.full((N_T,), O.OP_COLLECT_FERT, i32), zero, zero),
        (want_fert,     xp.full((N_T,), O.OP_FERTILIZE, i32),    zero, zero),
        (want_water,    xp.full((N_T,), O.OP_WATER, i32),        zero, zero),
        (h_one_a | h_ong_a | h_anim_a,
                        xp.full((N_T,), O.OP_HARVEST, i32),      zero, zero),
        (dig_mask,      xp.full((N_T,), O.OP_DIG, i32),          zero, zero),
        (build_here,    build_op,                                zero, zero),
        (m_place,       xp.full((N_T,), O.OP_PLACE, i32),      a_item,  one),
        (pl_mask,       xp.full((N_T,), O.OP_PLANT, i32),     pl_crop, zero),
        (pl_mask,       xp.full((N_T,), O.OP_WATER, i32),        zero, zero),
    ]
    if pf_feed is not None:   # [SWITCH, PLACEFEED1] after PLACE: the animal must stand there first
        cands[9:9] = [(pf_feed, xp.full((N_T,), O.OP_FEED, i32), zero, zero),
                      (pf_feed, xp.full((N_T,), O.OP_CARE, i32), zero, zero)]

    masks = xp.stack([c[0] for c in cands]).astype(i32)
    opv = xp.stack([c[1] for c in cands]).astype(i32)
    argv = xp.stack([c[2] for c in cands]).astype(i32)
    qtyv = xp.stack([c[3] for c in cands]).astype(i32)

    # Pinned int32 at the source, not at the consumers: `np.cumsum`/`np.sum`
    # widen an int32 input to int64 while their jnp counterparts do not (the
    # hazard projector.py documents), and `n_ops`/`chain_*` are `Prefix`
    # fields several callers index and stack with.
    slot = xp.cumsum(masks, axis=0, dtype=i32) - masks
    n_ops = xp.minimum(xp.sum(masks, axis=0, dtype=i32), CHAIN_MAX).astype(i32)
    live = masks * (slot < CHAIN_MAX)
    sel = (live[:, :, None] *
           (xp.arange(CHAIN_MAX, dtype=i32)[None, None, :] == slot[:, :, None])).astype(i32)
    chain_op = xp.sum(sel * opv[:, :, None], axis=0, dtype=i32)
    chain_a = xp.sum(sel * argv[:, :, None], axis=0, dtype=i32)
    chain_q = xp.sum(sel * qtyv[:, :, None], axis=0, dtype=i32)

    # ---- task values [1.6 admit stage] -------------------------------------
    # Every op's worth in coins under the day's value model: harvests at
    # today's price (plus the unit an in-window watering adds first),
    # survival waterings at the crop's remaining value, bonus waterings at one
    # unit, feeds at 1.4's value, care at the unit net of its wheat,
    # fertilizer at 0.11's marginal table, collections at the fertilizer
    # price, plantings and placements at their stream value under the grow
    # multiplier. A weed dig is worth what gets planted on it, which is the
    # planting's own value.
    want_harvest = h_one_a | h_ong_a | h_anim_a
    p_crop = view.price[crop]
    # The extra unit today's watering banks is `bonus_water`'s, not any
    # watering's: a one-time crop past its bonus window (`age > c_mxd`) is
    # watered for survival alone and the engine adds no yield for it, so
    # gating on `c_ongoing == 0` booked a phantom unit on exactly the tiles
    # `harvest_one` is about to harvest.
    bonus_today = (want_water & bonus_water).astype(i32)
    harvesting = h_one_a | h_ong_a
    v_harvest = (xp.where(harvesting, (view.t_yield + bonus_today) * p_crop, 0)
                 + xp.where(h_anim_a, view.t_yield * view.price[an_prod], 0))
    crop_val = VAL.crop_remaining_value(xp, view.price, view.t_day, view.t_yield, crop, day, harvest_age)
    # A survival watering buys the crop's whole remaining stream, net of what
    # today's harvest already books [gap review, 1.6]. Netting matters on the
    # tiles that both harvest and must be watered: an ongoing crop harvested
    # today keeps firing only if it lives through tonight, and pricing that
    # watering at 0 made its future invisible to admission -- the tile could be
    # dropped for work worth less than the fires it was protecting. A *bonus*
    # watering on a harvest tile stays 0: its one unit is already in
    # `v_harvest` above, and `crop_val - booked` is 0 there by construction.
    booked_today = xp.where(harvesting, (view.t_yield + bonus_today) * p_crop, 0)
    v_water = xp.where(want_water,
                       xp.where(must_water, xp.maximum(crop_val - booked_today, 0),
                                xp.where(harvesting, 0, p_crop)), 0)
    # `feed_value` carries the care unit for the *purchase* test; the tile
    # must not book it twice, and `v_care` right below is where it belongs --
    # the CARE op is the one that would be dropped if the turns ran out.
    # `care_val` is non-zero only where `want_care` holds, so this is the old
    # value wherever no care rides along.
    v_feed = xp.where(want_feed, feed_value - care_val, 0)
    # The CARE op's own labour stays at the *spot* net, floored at a coin
    # [SWITCH `CARE_HOLD_ON`]. `care_pays` reads the forward quote because the
    # unit is sold forward, but admission is a contest for today's turns and
    # `tile_value` is the currency every other op bids in at today's prices --
    # a care priced at a forward 267 against a spot 33 would outbid the ripe
    # tomato beside it and spend the turn that harvest needed, which is the
    # failure mode the `dev_weight` note records. The floor is what keeps the
    # newly-admitted care out of the route's worth-nothing group; OFF it is
    # inert, since `care_pays` there guarantees `price[prod] > price[WHEAT]`
    # and the difference is already at least one coin.
    v_care = xp.where(want_care,
                      xp.maximum(view.price[an_prod] - view.price[spec.I_WHEAT], 1), 0)
    # Net of the unit the application spends [H3]: `_admit` is a contest for
    # today's turns and the fertilizer in hand is sellable without spending
    # one, so what the FERTILIZE op earns is the gain *over* that sale. Floored
    # at a coin, like `v_care`, so an admitted application still outranks the
    # worth-nothing group. OFF it is the gross value it always was.
    if sw_fvol is True:
        v_fert = xp.where(want_fert, xp.maximum(fert_val - fert_ref, 1), 0)
    elif sw_fvol is False:
        v_fert = xp.where(want_fert, fert_val, 0)
    else:
        v_fert = xp.where(sw_fvol,
                          xp.where(want_fert, xp.maximum(fert_val - fert_ref, 1), 0),
                          xp.where(want_fert, fert_val, 0))
    v_collect = xp.where(col_a, view.price[spec.I_FERT], 0)
    # Clipped to the coin ceiling *before* the multiplier, like the budget's
    # own streams: `grow_mult` reaches 4x, so a raw stream near 2**20 would
    # otherwise leave int32 (section 2's `< 2**20` rule).
    rev_plant = xp.clip(u_new[pl_crop] * view.price[pl_crop], 0, BUD.VALUE_CAP)
    rev_place = xp.clip(ub_coins, 0, BUD.VALUE_CAP)[place_kind]
    v_plant = xp.where(pl_mask, grow_mult[pl_crop] * rev_plant // GROW_ONE, 0)
    v_place = xp.where(m_place,
                       xp.maximum(grow_mult[a_prod[place_kind]] * rev_place // GROW_ONE, 0), 0)
    # *How much* of the day's labour development is worth [R4]. `grow_mult` is
    # per product and also sizes the purchase budget, so nothing before this
    # could say "spend more of today's turns on development" without also
    # buying more seed. `dev_weight` scales the value alone, never the tier:
    # promoting development into the mandatory tier measured -23,312 +- 9,198
    # coins against `starter` (2026-08-26), because the route order carries no
    # value information *inside* a tier, so anything admitted ahead of a
    # harvest spends the turns the harvest needed. Development has to win the
    # labour on coins.
    #
    # Clipped to `VALUE_CAP` on the way in as well as out, so the product
    # stays inside int32 (`VALUE_CAP` < 2**20 and `dev_weight` <= 4 x
    # `GROW_ONE` = 2**10, hence < 2**30). The inbound clip cannot change a
    # decision: every term of `tile_value` is non-negative and the sum is
    # clipped to the same cap, so a term at or above it already saturates it.
    dev_w = xp.asarray(macro.dev_weight).astype(i32)
    if program_engine is not None and PROGRAM_PLANT_FULL:
        # PROGFIX1 (1): a programme planting is a committed, already-funded
        # obligation (its seed is bought); the theta's development discount
        # priced it at ~10 coins, so the labour admission dropped every
        # dig/plant chain behind bonus waterings and stranded the seed.
        dev_w = xp.maximum(dev_w, GROW_ONE).astype(i32)
    if mr_here is not None:  # [WHEATMIX1 / ESWORK1] the relay planting's undiscounted worth
        mr_vfull = xp.clip(v_plant, 0, BUD.VALUE_CAP).astype(i32)
    v_plant = xp.clip(xp.clip(v_plant, 0, BUD.VALUE_CAP) * dev_w // GROW_ONE,
                      0, BUD.VALUE_CAP)
    v_place = xp.clip(xp.clip(v_place, 0, BUD.VALUE_CAP) * dev_w // GROW_ONE,
                      0, BUD.VALUE_CAP)
    tile_value = xp.clip(v_harvest + v_water + v_feed + v_care + v_fert + v_collect + v_plant + v_place,
                         0, BUD.VALUE_CAP).astype(i32)
    if pf_feed is not None:   # [SWITCH, PLACEFEED1] one first-fire unit, net of its wheat
        tile_value = xp.clip(tile_value + xp.where(
            pf_feed, xp.maximum(view.price[a_prod[place_kind]] - view.price[spec.I_WHEAT], 1), 0),
            0, BUD.VALUE_CAP).astype(i32)

    # Mandatory tier [LAW, 0.5]: whatever the value says, work that is lost
    # for good if skipped today goes first -- deadline harvests, survival
    # waterings, survival feeds that passed 1.4's test.
    # [SWITCH `FEED_MANDATORY_ON`] widens the feed half of the tier from the
    # survival feeds to the survival *and* care-bearing ones; off it is
    # `must_feed` itself and the expression is the one it always was.
    mand_feed = _sw_pick(xp, _sw(macro, "FEED_MANDATORY_ON"),
                         lambda: must_feed | care_ok, must_feed)
    if NOOP_FIX_ON and NOOP_FIX_EXPIRE:
        # [SWITCH, NOOP_FIX] the spent ongoing crop's final units rot from
        # tomorrow's dawn: harvest them today like any other deadline.
        nf_last = (view.t_day + c_first + (xp.asarray(spec.CROP_MAX_YIELD)[crop] - 1)
                   * xp.asarray(spec.CROP_INTERVAL)[crop])
        nf_expire = h_ong_a & (c_ongoing == 1) & (day == nf_last)
    else:
        nf_expire = False
    mandatory = (h_one_a | nf_expire
                 | ((day >= O.LAST_SHED_DAY) & want_harvest)
                 | (is_plant & must_water & (view.t_water == 0))
                 | (want_feed & mand_feed))
    tier = mandatory.astype(i32)
    # [SWITCH `SURVIVAL_WATER_ON`] a second tier above the first, holding the
    # one op in the day that is lost *for good* if the turns run out: the
    # watering on a tile that weeds tonight without it and still has a stream
    # to sell. Everything else in the mandatory tier survives being cut -- a
    # deadline harvest keeps its units on the tile until tomorrow, a survival
    # feed's animal is replaceable -- so this is the tile the admit stage's
    # tail must never be allowed to reach. `task_order` compares (tier, key)
    # pairwise and takes any int32 tier, so no other stage changes.
    if sw_surv is True:
        tier = tier + (is_plant & survives_water & (view.t_water == 0)).astype(i32)
    elif sw_surv is not False:
        tier = tier + xp.where(
            sw_surv, (is_plant & survives_water & (view.t_water == 0)).astype(i32), 0)
    # A mandatory tile is never "worth nothing" [LAW, 0.5]. The route's last
    # group is the work that is worth nothing (`_plan_and_stats`), and a
    # survival watering on a crop whose remaining stream prices at zero must
    # not fall into it. One coin is enough: ordering *inside* a group is
    # serpentine and the admission order reads `tier` separately, so the floor
    # only decides which of the two route groups the tile belongs to -- so it
    # is the mandatory *flag*, not the tier ordinal, that floors the value
    # (identical while the tier is 0/1, i.e. everywhere but `SURVIVAL_WATER_ON`).
    if mr_here is not None:
        # [WHEATMIX1 / ESWORK1] Q4ROOT1: the relay's plantings lost the labour
        # admission at dev_weight (~10 coins). Full units x quote, and the
        # mandatory tier, so they are admitted ahead of the optional tail;
        # the hands that do them are added in `_plan_and_stats`.
        tile_value = xp.where(mr_here, xp.clip(tile_value + mr_vfull - v_plant, 0,
                                               BUD.VALUE_CAP), tile_value).astype(i32)
        tier = xp.where(mr_here, xp.maximum(tier, 1), tier).astype(i32)
    tile_value = xp.maximum(tile_value, xp.minimum(tier, 1))

    return Prefix(task=n_ops > 0, n_ops=n_ops,
                  chain_op=chain_op, chain_a=chain_a, chain_q=chain_q,
                  tile_value=tile_value, tier=tier,
                  want_feed=want_feed if pf_feed is None else (want_feed | pf_feed),
                  want_fert=want_fert, m_place=m_place,
                  wheat_buy=wheat_buy, fert_bought=fert_bought, seed_buy=seed_buy,
                  a_buy=a_buy, buy_land=buy_land, rev1=rev1, place_kind=place_kind,
                  n_fert_eff=n_fert_eff, purchase_shortfall=purchase_shortfall,
                  purse_left=purse_left,
                  **({"relay": mr_here} if mr_here is not None else {}))


def build_day(xp, view: DayView, macro: Macro, price_table=None,
              program_engine=None):
    """Whole-day plan. See the module docstring for the returned shapes.

    `price_table` is int32 [N_PRODUCTS, PRICE_TABLE_N] -- `tables.price` in the
    simulator so the planner projects with the very table the market prices
    with; None selects the engine default.
    """
    return _plan_and_stats(xp, view, macro, price_table,
                           program_engine=program_engine)[0]


def build_day_stats(view: DayView, macro: Macro, price_table=None) -> DayStats:
    """The section-7 metrics of the day `build_day` would plan from the same
    arguments -- the very plan, not a second model of it.

    numpy only, on purpose: this is a diagnostic replay path (see
    `scripts/plan_stats.py`), never a traced one.
    """
    return _plan_and_stats(np, view, macro, price_table)[1]


def _worth_a_turn(xp, d: "Prefix", no_tomorrow):
    """Drop the tasks that are worth nothing, on the terminal day only [4].

    Keyed to `terminal`, not to `drop_day`: the two are the same scalar unless
    `MIDDAY_DROP_ON` moves the DROP a day back, and day 28 *does* have a
    tomorrow -- day 29 harvests what day 28 waters and sells what day 28 grows.

    Off the terminal day zero-value work is real work -- a weed dig protects
    tomorrow's planting -- and the route already keeps it out of the priced
    tiles' way by sweeping it in its own last group. A DROP day has no tomorrow:
    a coop built at hour 0 never houses a fire, a placed goose never lays, and
    `_derive` prices both at exactly 0 already. Leaving them queued is not free
    even in the last group, because a PLACE puts its animal in `_pickup_kinds`
    and so costs *every* unit in the crew a pickup turn out of the sixteen the
    day has. `tile_value` carries a one-coin floor on the mandatory tier
    (`_derive`), so this can never cut a deadline harvest.
    """
    worth = ~no_tomorrow | (d.tile_value > 0)
    return d._replace(task=d.task & worth, m_place=d.m_place & worth,
                      want_feed=d.want_feed & worth, want_fert=d.want_fert & worth)


def _prestock(xp, view, macro, price_table, d, day, terminal, lots,
              blk, covered, has_harv, has_coll, proj_eod):
    """int, int, int[5]: tonight's BUY_PRODUCT and BUY_SEED for tomorrow [SWITCH].

    Persistence on what today itself realised, netted against a per-product
    projection of tonight's shed, then clipped by shed room and by the coins
    today's purchase walk left standing (`Prefix.purse_left`, already net of
    the hire bill and `cash_reserve`). Every clip is a `minimum`, so a want the
    farm cannot afford or cannot house is bought as a prefix and day d+1's own
    turn-1 row buys whatever is left -- which is exactly today's behaviour.

    `macro` is unused and kept in the signature so a future forecast that wants
    a gene has the same call shape; nothing here reads a policy output, which
    is the point (see the seed forecast's comment).
    """
    i32 = xp.int32
    ok = _prestock_ok(xp, day) & ~terminal

    # Tonight's shed, per product, from the quantities the day already holds:
    # hour-0 stock, plus this morning's buy, less the sale and the pickups the
    # reached blocks consume, plus the inflow those same blocks bank.
    sold = xp.sum(lots, axis=0).astype(i32)
    is_wheat_plant = (view.kind == spec.KIND_PLANT) & (view.occ == spec.I_WHEAT)
    harv_w = xp.sum(xp.where(covered & has_harv & is_wheat_plant, view.t_yield, 0),
                    dtype=i32).astype(i32)
    coll_f = xp.sum((covered & has_coll).astype(i32), dtype=i32).astype(i32)
    stock_w = (view.shed[spec.I_WHEAT].astype(i32) + d.wheat_buy - sold[spec.I_WHEAT]
               - xp.sum(blk[0], dtype=i32) + harv_w).astype(i32)
    stock_f = (view.shed[spec.I_FERT].astype(i32) + d.fert_bought - sold[spec.I_FERT]
               - xp.sum(blk[1], dtype=i32) + coll_f).astype(i32)
    planted = xp.stack([
        xp.sum(((d.chain_op == O.OP_PLANT) & (d.chain_a == c)
                & covered[:, None]).astype(i32), dtype=i32)
        for c in range(spec.N_CROPS)]).astype(i32)
    stock_s = (view.seeds.astype(i32) + d.seed_buy.astype(i32) - planted).astype(i32)

    # Tomorrow wants about what today *did*: one wheat per granted feed,
    # `n_fert_eff` applications, and as many seeds as the route actually
    # planted. Deliberately not `macro.plant_target` -- that is the raw gene
    # want before `_wants` clips it to the tiles that will exist and before the
    # labour boundary cuts it, so a farm with no free slots and a large target
    # would buy a full target's seeds every night and never plant one. Every
    # forecast here is therefore a quantity the day itself realised, and all
    # three are self-correcting: an over-buy raises tonight's stock and shrinks
    # tomorrow's prestock.
    want_w = xp.maximum(xp.sum(d.want_feed.astype(i32), dtype=i32) - stock_w, 0).astype(i32)
    want_f = xp.maximum(d.n_fert_eff - stock_f, 0).astype(i32)
    want_s = xp.maximum(planted - stock_s, 0).astype(i32)
    crew_eve = CREW_RELAY_ON and CREW_RELAY_EVE and not EVENING_SEED_ON
    if not (PRESTOCK_SEEDS or EVENING_SEED_ON or crew_eve):
        want_s = xp.zeros(spec.N_CROPS, i32)
    products = PRESTOCK_ON or EVE_STOCK_ON or (PRESTOCK_V2_ON and PRESTOCK_V2_BUY_ON)
    if crew_eve:
        # [SWITCH, CREWRELAY1] relay crops only, the evenings before RELAY_DAYS.
        dd = xp.asarray(day).astype(i32)
        in_win = (dd >= int(RELAY_DAYS[0]) - 1) & (dd <= int(RELAY_DAYS[1]) - 1)
        rw = xp.asarray(np.asarray([RELAY_W_WHEAT, RELAY_W_CARROT, RELAY_W_TOMATO, 0, 0], np.int32) > 0)
        want_s = xp.where(rw, want_s, 0).astype(i32)
        cum_s = xp.cumsum(want_s).astype(i32)
        want_s = xp.clip(xp.minimum(cum_s, EVENING_SEED_MAX)
                         - (cum_s - want_s), 0, None).astype(i32)
        want_s = xp.where(in_win, want_s, 0).astype(i32)
        if not products:
            want_w = xp.zeros((), i32)
            want_f = xp.zeros((), i32)
    if EVENING_SEED_ON:
        # [SWITCH, CREW24] Seeds-only evening row: the day window, the nightly
        # cap (a prefix in crop order), and the purse floor below.
        dd = xp.asarray(day).astype(i32)
        in_win = (dd >= EVENING_SEED_DAYS[0]) & (dd <= EVENING_SEED_DAYS[1])
        cum_s = xp.cumsum(want_s).astype(i32)
        want_s = xp.clip(xp.minimum(cum_s, EVENING_SEED_MAX)
                         - (cum_s - want_s), 0, None).astype(i32)
        want_s = xp.where(in_win, want_s, 0).astype(i32)
        if not products:
            want_w = xp.zeros((), i32)
            want_f = xp.zeros((), i32)

    # Shed room [LAW, 0.10]. Wheat and fertilizer sit in the shed all night and
    # compete with the eod dump for `SHED_CAPACITY`; seeds are a separate array
    # the shed does not hold, so they are not charged. `proj_eod` is the same
    # conservative-low projection 0.9's forced sale is sized against.
    room = xp.maximum(spec.SHED_CAPACITY - proj_eod, 0).astype(i32)
    n_w = xp.minimum(want_w, room).astype(i32)
    n_f = xp.minimum(want_f, xp.maximum(room - n_w, 0)).astype(i32)

    # Cash, walked in the BUY row's own order so the engine's slot-by-slot
    # clip agrees with the planner's. Quoted at `TURN_PRESTOCK` off the
    # opponent-free projection: the town drains inventory every tick and price
    # is monotone non-increasing in it, so tonight's quote is never dearer than
    # the same order's quote at turn 1 tomorrow.
    quotes = PJ.buy_quotes(xp, price_table,
                           PJ.projected_inv(xp, view.mkt_inv, view.shops,
                                            O.TURN_PRESTOCK, _osd(view.day, "F")))
    purse = d.purse_left
    if (EVENING_SEED_ON or crew_eve) and not products:
        purse = xp.maximum(_as(xp, purse) - EVENING_SEED_FLOOR, 0).astype(i32)

    def _afford(cum, n, purse):
        k = xp.minimum(n, xp.sum((cum <= purse).astype(i32), dtype=i32)).astype(i32)
        k = xp.clip(k, 0, PJ.K - 1).astype(i32)
        cost = xp.where(k > 0, cum[xp.maximum(k - 1, 0)], 0).astype(i32)
        return k, xp.maximum(purse - cost, 0).astype(i32)

    n_w, purse = _afford(xp.cumsum(quotes[spec.I_WHEAT], dtype=i32), n_w, purse)
    n_f, purse = _afford(xp.cumsum(quotes[spec.I_FERT], dtype=i32), n_f, purse)
    n_s = []
    for c in range(spec.N_CROPS):
        cum = (xp.arange(1, PJ.K + 1, dtype=i32) * int(spec.CROP_SEED_COST[c])).astype(i32)
        k, purse = _afford(cum, want_s[c], purse)
        n_s.append(k)

    z = xp.zeros((), i32)
    return (xp.where(ok, n_w, z).astype(i32),
            xp.where(ok, n_f, z).astype(i32),
            xp.where(ok, xp.stack(n_s), xp.zeros(spec.N_CROPS, i32)).astype(i32))


def _plan_and_stats(xp, view: DayView, macro: Macro, price_table,
                    program_engine=None):
    """`(plan tuple, DayStats)`. One body, because the metrics are locals of
    the plan and re-deriving them would be a second, drifting model of it.

    The plan tuple is what `build_day` returns and the simulator consumes; it
    must not grow. Under `jit` the discarded stats cost nothing (XLA drops
    them); on the numpy path they are three reductions over arrays the day has
    already built.
    """
    i32 = xp.int32
    if price_table is None:
        price_table = xp.asarray(default_price_table())
    # The opening's melon claim, before anything reads the mix [SWITCH]: both
    # `_derive` passes, `_wants`, `plant_eff` and `plant_crop` have to agree
    # about the day's plant_target or the seeds the budget buys are not the
    # ones the tiles plant.
    if open_board():
        macro = _melon_open(xp, view, macro)
    # The programmable plate, in the same place and for the same reason
    # [MELONGENES]: it is the same `plant_target` rewrite, so every reader of
    # the day's mix has to see it before `_derive` prices the day. OFF
    # (`MELON_PLATE_TILES == 0`) this `if` is false at trace time and nothing
    # below can tell the switch exists.
    if melon_plate_on():
        macro = _melon_plate(xp, view, macro)
    if melon_deny_on():
        macro = _melon_deny_plate(xp, view, macro)
    # The opening window's crew floor, in the same place and for the same
    # reason [SWITCH, MIRROR_OPEN]: the hire enumeration below reads
    # `macro.crew_target`, and `_derive` prices the day against the bill it
    # picks, so the floor has to be written before either of them runs.
    if MIRROR_OPEN_ON:
        macro = _mirror_crew(xp, view, macro)
    # The wheat line's share of the day's mix, in the same place and for the
    # same reason [SWITCH]: `_wants`, `plant_eff` and `plant_crop` all have to
    # agree about `plant_target`, and the land valuation prices the want vector
    # this rewrite produces.
    macro = _sw_macro(xp, _sw(macro, "WHEAT_VOLUME_ON"),
                      lambda: _wheat_mix(xp, macro), macro)
    # The late strawberry cap, before the tomato claim [SWITCH]: it hands its
    # share to the crops the brain chose, and the tomato budget below has to be
    # the last word on how many tiles tomato ends up with.
    macro = _sw_macro(xp, _sw(macro, "LATE_STRAW_CAP_ON"),
                      lambda: _late_straw_cap(xp, view, macro), macro)
    # The endgame's tomato claim, last of the mix rewrites and for the same
    # reason [SWITCH]: it is a claim on the *whole* mix, so it has to see what
    # the ones above left, and everything that reads `plant_target` --
    # `_derive`'s two passes, `_wants`, `plant_eff`, `plant_crop` -- has to
    # read the same vector.
    macro = _sw_macro(xp, _sw(macro, "ENDGAME_TOMATO_ON"),
                      lambda: _endgame_tomato(xp, view, macro), macro)
    # The other seat's book, last of the mix rewrites and for the same reason
    # [SWITCH, OPP_MIX]: it is a proportional tilt of whatever the three above
    # left, and `_derive`'s two passes, `_wants`, `plant_eff` and `plant_crop`
    # all have to read the one vector. `_candidates` prices the same weight
    # onto the seed and animal lists, so the purchase side agrees with it.
    if OPP_MIX_ON:
        macro = _opp_mix(xp, view, macro)
    # The forward/spot re-share, after every claim above and before the
    # schedule [SWITCH, CROP_SCARCE]: it is a proportional tilt of whatever the
    # rewrites above left, so it has to see their answer, and `_derive`'s two
    # passes, `_wants`, `plant_eff` and `plant_crop` all read the one vector it
    # produces. `sum(plant_target)` is preserved, so the land valuation and the
    # seed room above are unaffected.
    if CROP_SCARCE_ON:
        macro = _crop_scarce(xp, view, macro, price_table)
    # The flooded-book melon veto, after every claim and re-share above
    # [SWITCH, MELON_VETO_FLOOD]: it has to be the LAST word on melon, because
    # the rewrites above can each hand melon tiles it would otherwise never
    # see (`_melon_open` raises melon outright, `_late_straw_cap` and
    # `_crop_scarce` can tilt into it). Unlike them it is a development change
    # -- `sum(plant_target)` falls -- so it sits ahead of the seed room, the
    # land valuation and `_derive`'s two passes, all of which must price the
    # day against the smaller ask.
    if MELON_VETO_FLOOD_ON:
        macro = _melon_veto(xp, view, macro)
    # The macro schedule, last of the mix rewrites and by construction [SWITCH,
    # MACRO_EXEC]: it is the whole development plan for the day, so nothing may
    # rewrite it afterwards and everything that reads `plant_target` or
    # `animal_want` -- `_derive`'s two passes, `_wants`, `plant_eff`,
    # `plant_crop`, `_place_split` -- has to read the schedule's vectors.
    if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:
        # Site 1: off under "hands"; under the two herd modes it writes
        # `animal_want` and leaves `plant_target` to the decode.
        if _macro_site(1):
            macro = _macro_targets(xp, view, macro)
    # The goose floor, after every herd rewrite above [FREE FLOAT, EGG]: it is
    # a floor on a stock, so it has to see whatever the rewrites left, and
    # everything that reads `animal_want` -- `_seed_room`, `_wants`,
    # `_place_split`, the land valuation -- reads the floored vector.  At the 0
    # default the `if` is Python-false and the block does not exist.
    if GEESE_TARGET > 0:
        macro = _geese_floor(xp, view, macro)
    # The learned residual, LAST of the mix rewrites and for the same reason
    # the schedule is [SWITCH, ACTIONRL]: it is the only rewrite that is not a
    # rule, so it has to see the day every rule has finished with, and nothing
    # below may rewrite what it decides. Everything that reads `plant_target`,
    # `animal_want` or `hold` -- `_derive`'s two passes, `_wants`, `plant_eff`,
    # `plant_crop`, `_place_split`, the seed room, the budget grant, the cash
    # reserve, `_routes`, `_market` -- runs below this line and re-derives.
    # `d_hire` is carried down to the hire argmax rather than applied here.
    d_hire = None
    # [ACTIONRL11] `d_seed` is the wide layout's seed channel, carried down to
    # the budget's seed row for the same reason `d_hire` is carried to the hire
    # argmax: the row is granted and PAID far below this line. `None` under the
    # v1 layout and OFF, and `_derive` then builds the shipped expression.
    d_seed = None
    if residual_on():
        macro, d_hire, d_seed = _residual_override(xp, view, macro)
    # SHEEPFIRST1 is a stock target, so it is applied after the learned delta:
    # through d2 the final planner ask, not merely the pre-residual decode, is
    # N sheep. OFF is a Python-false branch and leaves the shipped graph exact.
    if SHEEP_FIRST_ON:
        macro = _sheep_first(xp, view, macro)
    if WOOL_FIRST_ON:
        macro = _wool_first(xp, view, macro)
    macro = _sw_macro(xp, _sw(macro, "MELONVETO_POST_ON"),
                      lambda: _melon_veto(xp, view, macro,
                                          MELONVETO_POST_K), macro)
    if RELAY_FILL_ON and RELAY_SELL_NOW:  # [SWITCH, RELAYFILL1] no crop reservation
        macro = _relay_sell_now(xp, view, macro)
    if ESWORK_THETA is not None:  # [ESWORK1] late ask floor (gene 4)
        macro = _eswork_macro(xp, view, macro)
    # PROGRAM_ENGINE1 is the sole final owner, after residual and veto.
    pe = program_engine if PROGRAM_ENGINE_ON else None
    if pe is not None:
        macro = _program_macro(xp, macro, pe)
    day = view.day
    # Terminal day [LAW, 0.4]: past LAST_SHED_DAY nothing a unit does can
    # still monetize, purchases are dead money, and the hour-0 shed is all
    # there is left to sell. One scalar, applied with `where` so the plan
    # stays shape-static.
    terminal = day > O.LAST_SHED_DAY
    # DROP splits that law in three [SWITCH, section 4]. "No purchases" and
    # "liquidate the shed at zero reservation" hold either way -- nothing bought
    # on day 29 can mature and nothing left in the shed is worth a coin. "No
    # unit acts" is the part DROP repeals: with a shed-adjacent deposit op the
    # day's harvest reaches the shed before turn 18's market, so the crew has
    # something to do again and the hire enumeration gets to say whether it is
    # worth the fib bill.
    if DROP_ON:
        drop_day = terminal
        if MIDDAY_DROP_ON:
            # One day back, and only one [SWITCH]. `terminal` itself does not
            # move: day 28 keeps its purchases, its reservations and its
            # tomorrow. What it gains is the route's return leg, the turn
            # budget that leaves room for it, and lot 3's offer of the load.
            drop_day = drop_day | (day == O.LAST_SHED_DAY)
        idle = terminal & ~drop_day
    else:
        drop_day = None
        idle = terminal

    # ---- hiring: an enumerated argmax [EXACT-OPT under the model, 1.5] -----
    # How many hands to hire is not a gene: it is the h whose admitted task
    # value pays for its fib bill by the most (plus `macro.hire_bias` per hand,
    # which is zero unless a theta writes the `g8` block). Pass A derives the day on a
    # zero bill and prices and orders every tile once; each h is then scored
    # off that one ordering -- (h + 1) units' turns, less the pickup allowance,
    # admit a prefix of the value order, and the prefix's cumulative value less
    # `HIRE_BILLS[h]` is the candidate's gain. A bill the purse cannot cover is
    # not a candidate at all, and `argmax` takes the first maximum, so ties go
    # to the lower index -- fewer hands.
    #
    # Pass B re-derives with the winner's bill deducted, because the prefix's
    # purchases are sized against the purse: scoring on the zero-bill purse and
    # then routing on it would let the BUY row commit coins turn 0 has spent
    # (`test_hire_bill.py`). It deducts the cash reserve too, so what the day
    # buys is what it can afford *and still field a crew tomorrow*.
    #
    # A candidate past `MAX_MARKET_ORDERS` hands needs the turn-2 HIRE row and
    # so starts the whole crew one turn later [LAW, ops.ROUTE_BASE_WIDE]: the
    # scan charges each h its own budget, `route_turns(h)`, which is a Python
    # constant per unrolled candidate and costs nothing at trace time. It is a
    # real part of the decision, not bookkeeping -- the eleventh hand buys
    # 21 turns and costs the ten already hired one turn each.
    #
    # Argmax under the planner's *model*, not an exact one: spawn positions,
    # per-unit pickup turns and the interaction between a hand's turns and what
    # the day buys all sit outside the projection, which charges every tile its
    # ops plus `EST_MOVES` and nothing else.
    bills = xp.asarray(HIRE_BILLS)
    pe_reserve = (xp.maximum(xp.asarray(
        _program_value(pe, "reserve", 0), i32), 0)
        if pe is not None else xp.asarray(0, i32))
    d0 = _derive(xp, view, macro, price_table, xp.asarray(0, i32), terminal,
                 pe_reserve, seed_extra=d_seed, program_engine=pe)
    if DROP_ON:
        d0 = _worth_a_turn(xp, d0, terminal)
    # [FORWARD_ADMIT] The prefix the *scan* prices its candidates against. At a
    # zero horizon it is `d0` itself and the four lines below are the ones they
    # always were; past that it is the projected pass, derived on the same zero
    # bill and the same zero reserve so the two differ in the horizon alone.
    # `rev1` is handed over rather than recomputed -- nothing it reads moves
    # with the window -- and the DROP filter is applied to it for the same
    # reason `d0` gets it: a task worth nothing on a terminal day is not work a
    # hand should be bought for, today or in three days.
    #
    # The horizon is `macro.forward_days`, the `g11` gene, unless the module
    # override says otherwise; `FORWARD_ADMIT_ON` exists so the switch can be
    # A/B'd against a theta that has not trained the gene.
    #
    # Everything below the value order still reads `d0`: the pickup allowance
    # (`n_kinds0`) is today's real demand, and `pre_early0` / `pack_orders0` /
    # `z_orders0` are today's real BUY row. Only the value/turn curve moves.
    fwd_days = xp.asarray(FORWARD_ADMIT_DAYS, i32) if FORWARD_ADMIT_ON \
        else macro.forward_days
    d_sc = d0
    if _static_horizon(fwd_days) != 0:
        d_sc = _derive(xp, view, macro, price_table, xp.asarray(0, i32), terminal,
                       pe_reserve, rev1=d0.rev1, forward=fwd_days,
                       seed_extra=d_seed, program_engine=pe)
        if DROP_ON:
            d_sc = _worth_a_turn(xp, d_sc, terminal)
    n_tasks0 = xp.sum(d_sc.task.astype(i32), dtype=i32)
    order0 = task_order(xp, d_sc.task, d_sc.tile_value, d_sc.tier)
    cum_est0 = xp.cumsum((d_sc.n_ops + EST_MOVES)[order0], dtype=i32)
    cum_val0 = xp.cumsum(d_sc.tile_value[order0], dtype=i32)
    # The pickup allowance is *per unit*, not per day [LAW, 0.12]: every unit
    # whose own block consumes a kind pays a turn for it, so a day that needs
    # wheat and fertilizer costs each of h + 1 units two turns, not two turns
    # between them. `n_kinds` is how many of the `N_PICK` kinds have any demand
    # today -- an upper bound on what one block can owe, and exact when the
    # demand is spread across the sweep. `EST_LEAD` is per unit for the same
    # reason and for a stronger one: every unit spawns on a shed-access tile
    # at the board's centre every morning and walks out to its own block, and
    # the eleventh hand buys 21 turns of which five are that walk.
    n_kinds0 = _pickup_kinds(xp, d0)
    scores = []
    affords = []
    if pe is not None:
        feed_quotes = PJ.buy_quotes(xp, price_table, PJ.projected_inv(
            xp, view.mkt_inv, view.shops, O.TURN_BUY, _osd(day, "F")))[spec.I_WHEAT]
        service_bill = xp.sum(xp.where(xp.arange(PJ.K) < d0.wheat_buy, feed_quotes, 0), dtype=i32)
    if PRESTOCK_ON:
        # The enumeration's own estimate of the schedule below [SWITCH]. Pass
        # A's residual row, not pass B's: the winner's bill is not known yet,
        # and a zero-bill purse buys *more*, so this reads the emptiness
        # conservatively -- it can only under-credit the extra turn.
        pre_early0 = _prestock_ok(xp, day) & (_buy_row_units(xp, d0) == 0)
    if PRESTOCK_V2_ON:
        # [SWITCH, PRESTOCK_V2] The same pass-A estimate, and the same honesty:
        # a zero-bill purse buys more, so this reads the emptiness
        # conservatively and can only under-credit the turn. The narrow test is
        # Python-time below, `h` being the unrolled candidate.
        pre_v2_0 = _prestock_ok(xp, day) & (_buy_row_units(xp, d0) == 0)
    if MARKET_PACK_ON:
        # [SWITCH] Pass A's purchase row, for the same reason and with the same
        # honesty as `PRESTOCK`'s above: the winner's hire bill is not known
        # yet, and a zero-bill purse buys *more* orders, so a candidate this
        # reads as packable is packable on the smaller pass-B row too. The
        # other direction -- a row pass B shrinks into the cap -- only
        # under-credits the crew, which is the safe error.
        pack_orders0 = _buy_row_orders(xp, d0)
    z_row = early_sell_zero_row()
    z_heavy = None
    if z_row and EARLY_SELL_MODE in EARLY_SELL_MODES_HEAVY_ONLY:
        # [SWITCH, EARLY_SELL Z1] The hour-0 shed, which is what the day's lots
        # are cut from and the one reading of "how much is there to sell"
        # available before the routes are laid (`O.EARLY_SELL_Z_MIN_SHED`).
        z_heavy = (xp.sum(view.shed[:spec.N_PRODUCTS].astype(i32), dtype=i32)
                   >= O.EARLY_SELL_Z_MIN_SHED)
    if z_row:
        # [SWITCH, EARLY_SELL Z] Pass A's purchase row, for `MARKET_PACK`'s
        # reason and with its honesty: the winner's hire bill is not known
        # yet, and a zero-bill purse buys *more* orders, so a candidate this
        # reads as fitting turn 1 fits it on the smaller pass-B row too --
        # and the other direction only under-credits the crew, which is the
        # safe error.
        z_orders0 = _buy_row_orders(xp, d0)
    cr_credit = 0
    if CREW_RELAY_ON:                       # [SWITCH, CREWRELAY1] relay work is not hire work
        cr_credit = _cr_alive(xp, day) * int(CREW_RELAY_CREDIT)
    elif FILL_WORK_ON:                      # [SWITCH, FILLWORK1] fill work is not hire work
        cr_credit = _fw_alive(xp, view) * int(FILL_WORK_CREDIT)
    for h in range(spec.MAX_HANDS + 1):
        per_unit = xp.asarray(route_turns(h), i32)
        if PRESTOCK_ON:
            per_unit = xp.where(pre_early0, per_unit + 1, per_unit).astype(i32)
        if PRESTOCK_V2_ON and h <= MO:
            # [SWITCH, PRESTOCK_V2] `ops.ROUTE_BASE_PRE`'s turn, on the narrow
            # candidates only -- V2 declines the wide day, so an eleventh hand
            # is priced against the base it actually gets.
            per_unit = xp.where(pre_v2_0, per_unit + 1, per_unit).astype(i32)
        if DROP_ON:
            # A DROP day's turns run out at `SELL_TURNS[-1]`, not at 23, and
            # every unit owes the return leg on top (`drop_turns`, `EST_HOME`).
            per_unit = xp.where(drop_day, drop_turns(h) - EST_HOME, per_unit).astype(i32)
            _e2_on = _sw_all(_sw(macro, "ENDROUTE2_ON"),
                             _sw(macro, "ENDROUTE_ON"))
            if _e2_on is not False:
                # [SWITCH, ENDROUTE2] The terminal day alone, and only because
                # `ENDROUTE_ON` put a lot on `ENDROUTE_TURN`: the candidate is
                # priced against the turns it really has, so the hire argmax
                # sees the longer prefix before it picks `h`.
                # [SWITCH-GENE] A PRICE, so the gene rides the vector: a gene
                # that asks for OFF hands the candidate back the `drop_turns`
                # price it had before the switch, which is the OFF day's own.
                per_unit = _sw_pick(
                    xp, _e2_on,
                    lambda: xp.where(drop_day & terminal,
                                     end_drop_turns(h) - EST_HOME,
                                     per_unit).astype(i32),
                    per_unit)
        if MARKET_PACK_ON:
            # [SWITCH] The turn a packed day buys, and it is charged against
            # the candidate rather than the day: `h` hires plus the row's
            # orders have to fit one turn's ten slots, so the hand that breaks
            # the cap costs every hand already hired a turn -- the same shape
            # as the eleventh hand's turn-2 row, and priced in the same place.
            # After the DROP branch, since a packed DROP day gains the turn
            # too (`turn_budget` is `SELL_TURNS[-1] + 1 - route_base` either
            # way).
            per_unit = xp.where(h + pack_orders0 <= MO, per_unit + 1, per_unit).astype(i32)
        if z_row and h <= MO:
            # [SWITCH, EARLY_SELL Z] Mode Z hires at turn 1, so this candidate
            # starts at `ops.ROUTE_BASE_Z` (2) -- the same 2 `route_turns`
            # already gives it -- and at `ROUTE_BASE_Z_LATE` (3) on a day its
            # purchases do not fit turn 1 behind its own hires. That is the
            # whole cost of selling first, and it is charged against the
            # CANDIDATE and not the day, exactly like the eleventh hand's
            # turn-2 row: the hand that pushes the BUY row off turn 1 costs
            # every hand already hired a turn. `h > MO` is not a Z day at all
            # (its overflow row owns turn 2), so it keeps `route_turns(h)`.
            # After the DROP branch, since a DROP day's budget is
            # `SELL_TURNS[-1] + 1 - route_base` and moves with the base too.
            late = h + z_orders0 > MO
            if z_heavy is not None:
                late = xp.logical_and(late, z_heavy)       # [Z1] heavy days only
            per_unit = xp.where(late, per_unit - 1, per_unit).astype(i32)
        turns_h = (h + 1) * (per_unit - n_kinds0 - _est_lead(xp, day))
        if CREW_RELAY_ON or FILL_WORK_ON:
            turns_h = turns_h + cr_credit
        n_adm = xp.minimum(_count_le(xp, cum_est0, turns_h), n_tasks0).astype(i32)
        # `hire_bias` is the gene's only channel into the crew size, and it is
        # a bias on this gain rather than a count [brain.HIRE_BIAS_MAX]: the
        # argmax, the affordability test and the value order are all still the
        # planner's. Linear in `h`, so against the fib bill it reads as a crew
        # target -- every hand whose own marginal cost is under the bias pays
        # for itself. Exactly 0 at zero theta, and `x + 0 * h == x` in int32,
        # so a theta written before the gene enumerates what it always did.
        # `crew_target` is the second channel and a different shape: a *ramp*
        # rather than a tilt [g10]. Every hand up to the target is worth
        # `CREW_TARGET_PUSH` coins, which beats its own marginal fib bill, so
        # the argmax walks up to the target and stops -- past it the term is
        # flat and the day is back to arguing from its work. Exactly 0 at zero
        # theta (`min(h, 0) == 0`), so the enumeration is the one it always was.
        # [SWITCH, CREW_PUSH_COST] ON the flat coin becomes a cumulative
        # table read at the same clipped count, built from the hand's own fib
        # marginal (`crew_push_cum`, read at trace time). OFF this is the
        # shipped `CREW_TARGET_PUSH * min(h, crew_target)` in int32.
        crew_clip = xp.minimum(xp.asarray(h, i32), macro.crew_target)
        crew_push = _sw_pick(
            xp, _sw(macro, "CREW_PUSH_COST_ON"),
            lambda: xp.asarray(crew_push_cum(on=True))[crew_clip].astype(i32),
            (CREW_TARGET_PUSH * crew_clip).astype(i32))
        # [SWITCH, HIRE_BIAS_ZERO] the tilt, or nothing. A module-level bool,
        # so the branch is taken at trace time and the jit path never sees it.
        hire_tilt = xp.asarray(0, i32) if HIRE_BIAS_ZERO_ON \
            else (macro.hire_bias * h)
        gain = (_cum_take(xp, cum_val0, n_adm) - bills[h]
                + hire_tilt + crew_push).astype(i32)
        # Affordable means "and still re-fieldable tomorrow" [LAW, 1.5]. The
        # reserve is held back from the *purchases* (`_derive`), so without
        # this the enumeration would spend it on the crew itself: a farm down
        # to its reserve hires the largest crew that reserve exactly pays for,
        # wakes on nothing and never hires again. Measured on the
        # spend-everything replay of `test_cash_reserve.py`: 7 coins on day 2
        # bought four hands for exactly 7 and the season ended there.
        reserve_h = cash_reserve(xp, h, day)
        if pe is not None:
            reserve_h = pe_reserve + service_bill
        afford = bills[h] + reserve_h <= view.money
        scores.append(xp.where(afford, gain, _UNAFFORDABLE).astype(i32))
        affords.append(afford)
    h_star = xp.argmax(xp.stack(scores)).astype(i32)
    if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:
        # [SWITCH, MACRO_EXEC] The crew the schedule asks for, not the crew
        # today's derived task set pays for. This is the FORWARD_ADMIT lesson
        # taken to its end (build story 2026-09-09): the enumeration cannot
        # price a hand against work that does not exist yet, so under a
        # schedule it does not get to vote on the count at all.
        #
        # The one thing the schedule cannot repeal is affordability, so the
        # ask is clipped to the largest crew the purse can field and still
        # re-field tomorrow -- `afford` is exactly the enumeration's own test,
        # and `HIRE_BILLS` is non-decreasing in `h`, so `afford` is a prefix
        # and counting its members under the ask IS `min(ask, max affordable)`.
        #
        # Site 5: on only under the modes that own the crew. A herd-only or
        # sell-only arm has to leave the enumeration's own argmax standing,
        # or it is not measuring one channel.
        if _macro_site(5):
            ask = _macro_row(xp, day, "hands")
            ok = xp.stack([xp.logical_and(
                affords[h], xp.asarray(h, i32) <= ask).astype(i32)
                for h in range(1, spec.MAX_HANDS + 1)])
            h_star = xp.sum(ok, axis=0, dtype=i32).astype(i32)
    # [SWITCH, ACTIONRL] The head's crew nudge, here and nowhere else: this is
    # the last line on which the count is still an INTENT. One line further
    # down `n_hire` sizes the bill `_derive` spends against, the cash reserve,
    # `n_units`, `wide` and `route_base` -- clamping there would desync all
    # four (ACTIONRL1 section 1's named trap).
    if d_hire is not None:
        h_star = _residual_hire(xp, h_star, d_hire, affords)
    if ROUTE_NN_ON and xp is np and ROUTE_NN_HIRE_FN is not None:   # [SWITCH, ROUTENN1] crew head's count
        h_star = _residual_hire(xp, h_star, np.int32(ROUTE_NN_HIRE_FN(int(h_star))), affords)
    if Q4_PROG_ON and Q4_HIRE_CAP > 0:  # [SWITCH, Q4PROG1] crew cap on Q4 days
        # The fib bill makes hand 13 cost 377/day and hand 15 987 (DSM runs
        # 11-12): the Q4 work has to come out of idle turns, not a bigger crew.
        q4_c = ((view.nquad >= 4) & (day >= int(Q4_HIRE_DAYS[0]))
                & (day <= int(Q4_HIRE_DAYS[1])))
        h_star = xp.where(q4_c, xp.minimum(h_star, int(Q4_HIRE_CAP)),
                          h_star).astype(i32)
    if Q4_PROG_ON and Q4_EXTRA_HANDS > 0:  # [SWITCH, Q4PROG1] +hands on Q4 days
        q4_h = ((view.nquad >= 4) & (day >= int(Q4_HIRE_DAYS[0]))
                & (day <= int(Q4_HIRE_DAYS[1])))
        for _k in range(int(Q4_EXTRA_HANDS)):
            up = xp.minimum(h_star + 1, spec.MAX_HANDS).astype(i32)
            ok_up = xp.stack(affords)[up] & (up > h_star)
            h_star = xp.where(q4_h & ok_up, up, h_star).astype(i32)
    if pe is not None:
        ask = xp.clip(xp.asarray(_program_value(pe, "hands_target", h_star), i32),
                      0, spec.MAX_HANDS)
        ok = xp.stack([xp.logical_and(
            affords[h], xp.asarray(h, i32) <= ask).astype(i32)
            for h in range(1, spec.MAX_HANDS + 1)])
        h_star = xp.sum(ok, axis=0, dtype=i32).astype(i32)
    if LATE_EXEC_ON and LATE_EXEC_HIRE_CAP > 0:                 # [SWITCH, LATE_EXEC]
        # The crew cap from `LATE_EXEC_HIRE_DAY0`: the n-th hand of a day
        # costs fib(n) (12th 144, 13th 233), and from the ENGINE's d20 state
        # our d20-29 hires 12.2/day for 3.8k against its 11.1/day for 2.5k with
        # 224 vs 106 PASS unit-turns -- the marginal hand is idle.
        h_star = xp.where(_as(xp, day) >= xp.asarray(LATE_EXEC_HIRE_DAY0, i32),
                          xp.minimum(h_star, xp.asarray(LATE_EXEC_HIRE_CAP, i32)),
                          h_star).astype(i32)
    # Nothing a hand does on the terminal day monetizes [LAW, 0.4], so the
    # bill would be pure loss -- the units all PASS below anyway.
    n_hire = xp.where(idle, 0, h_star).astype(i32)
    n_units = (xp.asarray(1, i32) + n_hire).astype(i32)
    wide = n_hire > MO
    route_base = xp.where(wide, O.ROUTE_BASE_WIDE, O.ROUTE_BASE).astype(i32)
    d = _derive(xp, view, macro, price_table, bills[n_hire], terminal,
                pe_reserve if pe is not None else cash_reserve(xp, n_hire, day),
                rev1=d0.rev1, seed_extra=d_seed, ask_fill=True, program_engine=pe)
    if ESWORK_THETA is not None and d.relay is not None and not (
            PLAN_FASTPATH_ON and xp is np and not np.any(d.relay & d.task)):   # [SWITCH, REVFIX1 B2] empty relay: same bill
        # [WHEATMIX1 / ESWORK1] the relay's hands, sized from the relay's own
        # tasks (ops + a move each, ESWORK_RELAY_OPH per hand) and added ON TOP
        # of the planner's crew. The day is then re-derived against the bigger bill.
        mr_ops = xp.sum(xp.where(d.relay & d.task, d.n_ops + EST_MOVES, 0), dtype=i32)
        mr_oph = int(ESWORK_RELAY_OPH)
        mr_mx = int(ESWORK_RELAY_MAX_E)
        mr_e = xp.minimum((mr_ops + mr_oph - 1) // mr_oph, mr_mx).astype(i32)
        mr_h = h_star
        for _k in range(mr_mx):
            up = xp.minimum(mr_h + 1, spec.MAX_HANDS).astype(i32)
            ok_up = xp.stack(affords)[up] & (up > mr_h) & (mr_e > _k)
            mr_h = xp.where(ok_up, up, mr_h).astype(i32)
        h_star = mr_h
        n_hire = xp.where(idle, 0, h_star).astype(i32)
        n_units = (xp.asarray(1, i32) + n_hire).astype(i32)
        wide = n_hire > MO
        route_base = xp.where(wide, O.ROUTE_BASE_WIDE, O.ROUTE_BASE).astype(i32)
        d = _derive(xp, view, macro, price_table, bills[n_hire], terminal,
                    pe_reserve if pe is not None else cash_reserve(xp, n_hire, day),
                    rev1=d0.rev1, seed_extra=d_seed, ask_fill=True, program_engine=pe)
    if pe is not None:
        d = _program_prefix(xp, d, pe)
    if DROP_ON:
        d = _worth_a_turn(xp, d, terminal)
    if PRESTOCK_ON:
        # [SWITCH] The residual BUY row is empty, so turn 1 has nothing to
        # resolve: the overflow hire row moves up into it and the whole crew
        # walks a turn earlier (`ops.ROUTE_BASE_PRE`). One scalar for the whole
        # crew, because a crew that starts at two different turns re-scatters
        # every later hand's spawn tile (`ops.ROUTE_BASE_WIDE`).
        buy_row_empty = _prestock_ok(xp, day) & (_buy_row_units(xp, d) == 0)
        route_base = xp.where(
            buy_row_empty,
            xp.where(wide, O.ROUTE_BASE_WIDE_PRE, O.ROUTE_BASE_PRE),
            route_base).astype(i32)
    pre_v2 = None
    if PRESTOCK_V2_ON or PRESTOCK_V2_FARMER0_ON:
        # [SWITCH, PRESTOCK_V2] The day predicate, narrow crews only. `~wide`
        # is what keeps `hire_wide_early` out of this switch entirely (there is
        # no overflow row on a narrow day), and so what keeps turn 1's writers
        # exactly the ones they are today -- see the switch's own comment.
        pre_v2 = (_prestock_ok(xp, day) & (_buy_row_units(xp, d) == 0) & (~wide))
    if PRESTOCK_V2_ON:
        route_base = xp.where(pre_v2, O.ROUTE_BASE_PRE, route_base).astype(i32)
    z_buy_t1 = None
    if z_row:
        # [SWITCH, EARLY_SELL Z] The morning is one turn later than it was:
        # the hires resolve at `O.EARLY_SELL_Z_HIRE_TURN` (1), so nothing may
        # act before turn 2 whatever the purchases do, and the purchases
        # themselves take turn 1 behind the hires or turn 2 alone. A wide day
        # is not a Z day (`_market`'s `z_fires`) and keeps the base it had.
        z_day = (~wide) if z_heavy is None else ((~wide) & z_heavy)
        z_buy_t1 = z_day & ((n_hire + _buy_row_orders(xp, d)) <= MO)
        route_base = xp.where(
            z_day, xp.where(z_buy_t1, O.ROUTE_BASE_Z, O.ROUTE_BASE_Z_LATE),
            route_base).astype(i32)
    pack = None
    if MARKET_PACK_ON:
        # [SWITCH] The whole day's market row -- `n_hire` hires and the orders
        # the budget sized -- against the engine's ten-slot per-turn cap. It
        # fits, so both rows go out at turn 0, turn 1 resolves nothing and the
        # whole crew's floor is `ops.ROUTE_BASE_PACK`: the pickup-owing blocks
        # too, since the goods reached the shed in turn 0's market phase.
        #
        # `n_hire <= MO` follows rather than being asked for -- eleven hires do
        # not fit ten slots -- so a packed day is always narrow and the turn-2
        # hire row is empty. And `route_base` moving off the law's own value is
        # what switches `route_split` off below, which is the rule that keeps
        # turn 0 idle for everyone [`ops.ROUTE_BASE_PACK`].
        pack = (n_hire + _buy_row_orders(xp, d)) <= MO
        route_base = xp.where(pack, O.ROUTE_BASE_PACK, route_base).astype(i32)
    turn_budget = (TPD - route_base).astype(i32)
    if DROP_ON:
        # Turns past `SELL_TURNS[-1]` are worthless on a DROP day -- there is no
        # later lot to sell into and no end-of-day to bank into -- and a DROP on
        # turn 18 itself still counts, because units act before their turn's
        # market. So the budget ends one turn *after* the last sell turn, which
        # is exactly what `_routes` needs to place the tail on turn 18 at worst.
        turn_budget = xp.where(drop_day, O.SELL_TURNS[-1] + 1 - route_base,
                               turn_budget).astype(i32)
        _e2_on = _sw_all(_sw(macro, "ENDROUTE2_ON"),
                         _sw(macro, "ENDROUTE_ON"))
        if _e2_on is not False:
            # [SWITCH, ENDROUTE2] The same sentence against `ENDROUTE_TURN`.
            # Keyed to `terminal` and not to `drop_day`: day 28 under
            # `MIDDAY_DROP_ON` has a tomorrow and an end-of-day, and the
            # terminal row stands on day 29 only.
            # [SWITCH-GENE] A BUDGET -- an int32 array every downstream site
            # compares against (`labour`, `walk_u`, `_cut`'s `bud`), never a
            # Python shape -- so the gene rides the vector and a gene-OFF day
            # carries the `SELL_TURNS[-1] + 1` budget the DROP branch set.
            turn_budget = _sw_pick(
                xp, _e2_on,
                lambda: xp.where(drop_day & terminal,
                                 ENDROUTE_TURN + 1 - route_base,
                                 turn_budget).astype(i32),
                turn_budget)
    # No unit may work before the quadrant exists [LAW, M2]. BUY_LAND resolves
    # in the market phase of `SELL_TURNS[0]`, which runs *after* that turn's
    # unit phase, so a prospective tile is still LOCKED for anything acting
    # earlier -- and a tile op on a LOCKED tile silently no-ops, so the turn is
    # spent for nothing. It applies to every unit and not to the farmer alone:
    # three of the four shed-access spawn tiles lie outside NW
    # (`spec.SHED_ACCESS_XY`), so a hand can spawn inside the new quadrant.
    #
    # Charged as a *floor under the pickup turns*, not on top of them, because
    # a unit's PICKUPs need the shed and not the land: they run from
    # `route_base` either way, and only a unit with fewer pickup kinds than the
    # lead idles at all. Measured on the archetype ladder (2026-08-25): charged
    # additively the seven rungs lost 15% of their coins between them; as a
    # floor they gain 13%, because the days that buy land are exactly the days
    # with animals to place and feed to carry.
    land_lead = (d.buy_land * xp.maximum(O.SELL_TURNS[0] + 1 - route_base, 0)).astype(i32)

    farmer0 = None
    if PRESTOCK_V2_FARMER0_ON:
        # [SWITCH, PRESTOCK_V2] The farmer's hour 0. `land_lead == 0` on top of
        # the day predicate: the shift moves the block's first task op too, and
        # a prospective quadrant is LOCKED until `SELL_TURNS[0]`'s market phase
        # [M2]. `_routes` decides the rest per block -- it hands the turn over
        # only where unit 0's block opens with a PICKUP, which is the one op
        # that does not step off the spawn tile.
        farmer0 = pre_v2 & (land_lead == 0)

    route_early = None
    if ROUTE_EARLY_ON:
        # [SWITCH] The day-level half of the per-unit start: the three
        # conditions that belong to the morning rather than to a block. A wide
        # crew's overflow hire row is turn 2 and a unit that steps before it
        # re-scatters every later hand's spawn tile
        # (`ops.ROUTE_BASE_WIDE`); a land day's quadrant does not exist until
        # `SELL_TURNS[0]`'s market phase [M2]; and a base `PRESTOCK` has
        # already moved to `O.TURN_BUY` has nowhere earlier to go, the turn-0
        # hire row being the next thing in the way. `_routes` decides the rest,
        # per unit, off the block it cuts.
        route_early = ((~wide) & (land_lead == 0)
                       & (route_base == O.ROUTE_BASE))

    route_split = None
    if ROUTE_SPLIT_ON:
        # [SWITCH] The day-level half of the per-block start, and the wide crew
        # is *in* it: what a wide day forbids is walking before its turn-2 hire
        # row resolves, and `_routes` gives such a unit its extra turn as a
        # stationary PICKUP at turn 2 rather than as a step. What is left at
        # this level is the land day [M2] and the requirement that the base is
        # the one the law fixes -- `PRESTOCK` moves it, and there is nothing
        # earlier than `O.ROUTE_BASE_PRE` to move it to.
        route_split = ((land_lead == 0)
                       & (route_base == xp.where(wide, O.ROUTE_BASE_WIDE,
                                                 O.ROUTE_BASE)))
        if z_buy_t1 is not None:
            # [SWITCH, EARLY_SELL Z] The same rule read against Z's morning. A
            # narrow Z day that bought at turn 2 has a step to give a block the
            # BUY row does not feed -- turn 2, one turn after the hires
            # resolved and one before the base. A narrow Z day that bought at
            # turn 1 has none: turn 1 IS the hire row, and a unit that steps
            # before it resolves re-scatters every hand `_spawn_hand` places
            # [LAW, ops.ROUTE_BASE_WIDE]. A wide day is not a Z day and keeps
            # the gate above, wide-day pickup branch included.
            route_split = xp.where(z_day, (land_lead == 0) & (~z_buy_t1),
                                   route_split)

    freefirst = None
    widepick = None
    _wp_on = _sw(macro, "WIDE_PICK_ON")
    if _wp_on is not False and route_split is not None:
        # [SWITCH, WIDE_PICK] The same per-kind vector, read by the *wide*
        # branch instead of the narrow one. Kept separate from `freefirst` so
        # that turning this switch on never widens `narrow_ok`: the two arms
        # are independent and are judged independently.
        widepick = xp.stack([d.wheat_buy > 0, d.fert_bought > 0]
                            + [d.a_buy[a] > 0 for a in range(spec.N_ANIMALS)])
        if _wp_on is not True:
            # [SWITCH-GENE] OFF by a TRACED gene: the shape is the ON one --
            # the trace cannot drop a branch -- so the switch is carried in the
            # VALUE. Every kind reads "today's BUY row delivers it", hence no
            # block ever owns a free FIRST kind, `first_free` is False and
            # `wide2` never fires: bit for bit the OFF program.
            widepick = widepick | (~xp.asarray(_wp_on))
    wpfree = None
    if widepick is not None:
        # [SWITCH, WIDE_PICK_FREE] Only the granted column's row ORDER moves, so
        # the arm has no subject at all unless `widepick` exists. A traced-off
        # draw is carried in the VALUE (`wpfree` False widens nothing and keys
        # every kind the same, so the 5x5 comparison collapses back onto the
        # cumsum) -- bit for bit the shipped program, without a branch the
        # trace cannot drop.
        _wpf_on = _sw(macro, "WIDE_PICK_FREE_ON")
        if _wpf_on is not False:
            wpfree = True if _wpf_on is True else xp.asarray(_wpf_on) != 0
    if (ROUTE_FREEFIRST_ON or EVE_STOCK_ON or H1_WORK_ON) and route_split is not None:
        # [SWITCH, ROUTE_FREEFIRST] Which of the `N_PICK` kinds today's BUY row
        # is about to deliver, in `PICK_ITEM` order (wheat, fertilizer, one per
        # animal). Seeds are deliberately absent: nothing PICKUPs a seed, and
        # the PLANT that consumes one is held by `free_first` instead. A block
        # owing only kinds with a zero here draws last night's shed and may
        # collect at `TURN_BUY`; `_routes` reads it per block.
        freefirst = xp.stack([d.wheat_buy > 0, d.fert_bought > 0]
                             + [d.a_buy[a] > 0 for a in range(spec.N_ANIMALS)])
    seedfree = None
    if H1_WORK_ON and route_split is not None:
        # [SWITCH, CREW24] Today's BUY row buys no seed: every PLANT draws
        # seed already held at dawn, so a PLANT opener may take hour 1.
        seedfree = xp.sum(_as(xp, d.seed_buy).astype(i32), dtype=i32) == 0
    elif CREW_RELAY_ON and CREW_RELAY_H1 and route_split is not None:
        # [SWITCH, CREWRELAY1] the seed half of H1_WORK, relay days only.
        seedfree = ((xp.sum(_as(xp, d.seed_buy).astype(i32), dtype=i32) == 0)
                    & (_as(xp, day) >= int(RELAY_DAYS[0]))
                    & (_as(xp, day) <= int(RELAY_DAYS[1])))

    tail_fill = None
    if TAIL_FILL_ON:
        # [SWITCH] The one op each tile offers a unit that has turns left and
        # nothing of its own to do, read off the morning board and off nothing
        # the day's plan changes: `_routes` only ever fills a tile no block
        # holds. `O.OP_PASS` where the tile offers none.
        is_struct = ((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE))
        has_animal = is_struct & (view.occ >= 0)
        tail_fill = xp.where(
            has_animal & (view.t_favail == 1), O.OP_COLLECT_FERT,
            xp.where((view.kind == spec.KIND_PLANT) & (view.t_water == 0), O.OP_WATER,
                     xp.where(view.kind == spec.KIND_WEED, O.OP_DIG,
                              O.OP_PASS))).astype(i32)

    tc_animal = tc_unfed = tc_uncared = tc_starving = tc_wheat = None
    tc_plan_feed = tc_plan_care = None
    if TAIL_CARE_ON:
        # [SWITCH] Everything the care hop reads that does not depend on the
        # admitted set, off the morning board. `t_water` is `fed_today` and
        # `t_cared` is `cared_today` on an animal tile (`agent/parse.py`), and
        # the engine clears both at every eod, so on a live board these are
        # `tc_animal` -- but the plan is written against the view it is handed,
        # not against that invariant.
        tc_struct = ((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE))
        tc_animal = tc_struct & (view.occ >= 0)
        tc_unfed = tc_animal & (view.t_water == 0)
        tc_uncared = tc_animal & (view.t_cared == 0)
        # One more unfed night and the animal escapes (`:817`), so a bare FEED
        # with no care behind it is still worth the walk on this tile alone.
        tc_starving = tc_animal & (view.t_cons >= 1)
        # The unit's own wheat carry, tile by tile: a HARVEST on a wheat plant
        # puts its whole `yield_units` into the acting unit's inventory
        # (`:469`) and `DROP` runs eight times a game, which is why 354.8 units
        # ride in unit hands to hour 23. The feed pickup nets to zero against
        # the FEEDs the block spends it on, so this is the whole of the carry.
        tc_wheat = xp.where(
            (view.kind == spec.KIND_PLANT) & (view.occ == spec.I_WHEAT)
            & (xp.sum((d.chain_op == O.OP_HARVEST).astype(i32), axis=1) > 0),
            view.t_yield, 0).astype(i32)
        # What the day's own route already does, so the hop never spends a turn
        # the engine would no-op. `want_care` is not a `Prefix` field; it is
        # exactly the tiles whose chain carries a CARE.
        tc_plan_feed = d.want_feed
        tc_plan_care = xp.sum((d.chain_op == O.OP_CARE).astype(i32), axis=1) > 0

    cf_static = cf_fed_now = cf_plan_feed = cf_plan_care = None
    if CARE_FILL_ON:
        # [SWITCH] Everything the fill hops read that the admitted set does not
        # move. The three static gates are the engine's own
        # (`kaggriculture.py:826-830`): the animal has not been cared today, a
        # bank added tonight still has somewhere to go, and the fire it banks
        # for is still inside the horizon a sale can reach. The fourth gate --
        # fed -- is half static (`t_water`) and half the round's, below.
        cf_struct = ((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE))
        cf_animal = cf_struct & (view.occ >= 0)
        cf_a = xp.clip(view.occ, 0, spec.N_ANIMALS - 1)
        cf_first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[cf_a]
        cf_int = xp.asarray(spec.ANIMAL_INTERVAL)[cf_a]
        cf_held = xp.asarray(spec.ANIMAL_MAX_HELD)[cf_a]
        # `care_ok`'s own headroom, verbatim: a fire tonight consumes or wipes
        # the bank before today's care is added, so the carry is 0 there
        # (`eod.refresh_animals`), and `+ 2` is tonight's care plus the base
        # unit the fire pays whatever happens.
        cf_fires = cf_animal & VAL.fires_on(xp, view.t_day, cf_first, cf_int, day + 1)
        cf_head = xp.where(cf_fires, 0, view.t_bank) + 2 <= cf_held
        cf_horizon = (VAL.next_fire_after(xp, view.t_day, cf_first, cf_int, day)
                      <= VAL.pay_day())
        cf_static = cf_animal & (view.t_cared == 0) & cf_head & cf_horizon
        # Fed this morning already; the day's own feeds are added per round.
        cf_fed_now = view.t_water == 1
        cf_plan_feed = d.want_feed
        cf_plan_care = xp.sum((d.chain_op == O.OP_CARE).astype(i32), axis=1) > 0

    # ---- admit, then route [HEURISTIC, 1.6] --------------------------------
    # Admit tiles by (tier, value) against the day's whole turn budget, each
    # costed at its ops plus EST_MOVES; then route the admitted set as a
    # serpentine sweep -- `_routes` cuts it into contiguous stripes per unit.
    #
    # The route order is (route group, serpentine), not serpentine alone.
    # `_routes` drops whatever its budget cannot reach off the *end* of the
    # order it is given, so anything that sweeps early spends turns that
    # whatever sweeps late will not get. **Two** route groups therefore sweep
    # in succession, each in serpentine order within itself:
    #
    #   1  priced-or-mandatory: a harvest, a development watering, a feed, and
    #      -- through `_derive`'s one-coin floor on `tile_value` -- every
    #      mandatory tile whatever its stream prices at.
    #   0  optional and worth nothing: a weed dig on a day with no planting to
    #      protect. Zero-value work is real work the day may still do, but it
    #      must never be the reason a priced tile goes unreached -- and it
    #      swept first while it merely *tied* the valued tiles on (tier,
    #      serpentine): 40 weeds ahead of a ripe tomato took the whole budget
    #      and harvested nothing. Worse, the count-based re-admission below
    #      cannot repair that, because it drops from the VALUE tail -- the very
    #      tiles the sweep failed to reach -- so the loop never converged.
    #
    # Each populated group past the first costs one extra traversal of the
    # worked span, and a group of m scattered tiles spans the whole board
    # however few of them there are. The four groups this used to build
    # (mandatory-priced, mandatory-worthless, optional-priced,
    # optional-worthless) therefore crossed the board up to four times, at
    # 1.32 inter-tile moves per visit against a single sweep's 1.00 -- 48.6% of
    # the season's unit-turns spent walking. Those crossings also made a liar
    # of `cum_est`'s `EST_MOVES` charge, so admission let in tiles the route
    # could not reach and the shortfall came off the value tail where the new
    # plantings sit (measured 2026-08-26: 305 plantings queued, 141 done).
    #
    # 0.5's LAW does not live here any more -- it lives in `order_v` below,
    # which still ranks by `d.tier` first and from whose *tail* the
    # re-admission drops. A mandatory tile is therefore never the tile cut,
    # and the worthless group still sweeps last, which is the protection the
    # forty-weed boards of `test_mandatory_tier.py` exist for.
    #
    # The estimate is not a bound: when the exact route leaves admitted tiles
    # uncovered, the shortfall is re-admitted from the *value* tail (the
    # mandatory tier sits at the head of `order_v`, so a deadline harvest or
    # survival watering is never the tile that goes [LAW, 0.5]) and the route
    # is rebuilt -- ADMIT_ROUNDS times, shape-static. `n_admit` falls by the
    # uncovered count each round, so a shortfall deeper than ADMIT_ROUNDS - 1
    # tiles still ends on a route that leaves admitted work undone: that
    # residue is section 7's "task value dropped at the labour boundary".
    n_tasks = xp.sum(d.task.astype(i32), dtype=i32)
    melon = None
    if MELON_OPEN_ON or MIDDAY_PLACE_V2_ON:
        # [MELON_OPEN] The tiles the dump day has to bank before the
        # opponent's lot: a standing melon whose chain this day harvests.
        mel_mask = ((xp.sum((d.chain_op == O.OP_HARVEST).astype(i32), axis=1) > 0)
                    & (view.kind == spec.KIND_PLANT) & (view.occ == spec.I_MELON))
        mel_day = day == MELON_OPEN_HARVEST_DAY
        if MIDDAY_PLACE_V2_ON:                                   # [SWITCH]
            # [MIDDAY_PLACE_V2] Every day a melon ripens, not only the
            # opening's. Melon's `CROP_FIRST_YIELD_DAY` is the reason the
            # excursion exists at all -- the harvest does not exist before
            # that day and `_end_of_day` banks it after the last row -- and
            # that reason is a property of the crop, not of
            # `MELON_OPEN_HARVEST_DAY`. The default build plants melon on
            # days 4-6 and harvests it on 13-16; without this those harvests
            # ride to the next morning and sell at ~150 instead of ~200.
            # `mel_mask` is empty on every other day, so the trigger is the
            # crop's own ripening and costs nothing where there is none.
            mel_day = xp.sum(mel_mask.astype(i32), dtype=i32) > 0
        # The third element is `MIDDAY_PLACE_ON`'s alone -- the turn the crew
        # starts on, which is what turns a rank into a deposit turn. It is the
        # same quantity `BANK_BEFORE_LOT_ON` passes as `bank`'s third element.
        melon = (mel_day, mel_mask, route_base)
    if SAME_DAY_FERT_ON:                                         # [SWITCH]
        # [SAME_DAY_FERT] The same excursion, with the day's fertilizer in it.
        # The candidate ranks are the animals this day collects from -- the
        # chain the `want_collect` tier put there, which is exactly
        # `has_animal & t_favail == 1` -- and the trigger is that there is one
        # of them, on any day from the first that can have any (day 0 has no
        # animal that has stood overnight) to the knob. `terminal` is out
        # because there the whole shed liquidates on its own rows anyway and
        # the route is a PASS override. The third element is the crew's start
        # turn, as it is for melon: what turns a rank into a deposit turn.
        fert_mask = xp.sum((d.chain_op == O.OP_COLLECT_FERT).astype(i32), axis=1) > 0
        fert_day = ((~terminal) & (day >= 1) & (day <= SAME_DAY_FERT_LAST_DAY)
                    & (xp.sum(fert_mask.astype(i32), dtype=i32) > 0))
        melon = (fert_day, fert_mask, route_base)
    bank = None
    if BANK_BEFORE_LOT_ON:
        # [BANK_BEFORE_LOT] What a tile's harvest is worth in the hands that
        # carry it, at today's quotes: the same banked yield `DROP_ON` prices
        # its return leg off (the watering bonus included, since a chain that
        # waters before it harvests collects it), times the product's price.
        # Off on a DROP day -- every block there already ends in a return leg
        # and the budget is cut to match -- and off past the last shed day,
        # where the whole shed liquidates anyway.
        bk_w = xp.sum((d.chain_op == O.OP_WATER).astype(i32), axis=1) > 0
        bk_h = xp.sum((d.chain_op == O.OP_HARVEST).astype(i32), axis=1) > 0
        bk_an = xp.asarray(spec.ANIMAL_PRODUCT)[xp.clip(view.occ, 0, spec.N_ANIMALS - 1)]
        bk_p = xp.where(view.kind == spec.KIND_PLANT,
                        xp.clip(view.occ, 0, spec.N_CROPS - 1), bk_an).astype(i32)
        bk_units = xp.where(bk_h, view.t_yield + 2 * bk_w.astype(i32), 0).astype(i32)
        bank_val = (bk_units * view.price[:spec.N_PRODUCTS][bk_p]).astype(i32)
        bank_day = ~terminal
        _e2s_on = _sw_all(_sw(macro, "ENDROUTE2_SPLIT_ON"),
                          _sw(macro, "ENDROUTE2_ON"),
                          _sw(macro, "ENDROUTE_ON"))
        if DROP_ON:
            bank_day = bank_day & ~drop_day
            if _e2s_on is not False:
                # [SWITCH, ENDROUTE2_SPLIT] The terminal day back in, and it
                # alone: `ENDROUTE2_ON` gave the day turns past the last lot,
                # so the block's own return leg no longer lands in front of
                # it, and this excursion is what keeps the h19 dump.
                # [SWITCH-GENE] A MASK, so the gene rides the vector: gene-OFF
                # is `~terminal & ~drop_day`, the mask it always was.
                bank_day = _sw_pick(xp, _e2s_on,
                                    lambda: bank_day | (drop_day & terminal),
                                    bank_day)
        bank = (bank_day, bank_val, route_base)
        if _e2s_on is not False:
            # [SWITCH, ENDROUTE2_SPLIT] The deposit deadline and the two gates,
            # as traced scalars: the terminal day's dump has to beat the day's
            # LAST lot, not `BANK_LOT`'s, and it is the price-denial dump
            # rather than an opportunistic top-up, so its value floor and leg
            # budget are its own knobs. Every other day reads the shipped
            # constants and nothing moves.
            # [SWITCH-GENE] Three SCALARS, so the gene rides the vector: a gene
            # that asks for OFF puts `O.SELL_TURNS[BANK_LOT]` / `BANK_MIN_VALUE`
            # / `BANK_MAX_TURNS` in all three slots, which is exactly the three
            # numbers `_routes`' `bank_late is None` arm compares against, so
            # the gene-OFF day gates the excursion the way it always did.
            # Concrete OFF still hands `_routes` a 3-tuple, so the arity -- the
            # one part of this that is shape and not value -- is untraced.
            bank = bank + (
                _sw_pick(xp, _e2s_on,
                         lambda: xp.where(terminal, ENDROUTE2_SPLIT_TURN,
                                          O.SELL_TURNS[BANK_LOT]).astype(i32),
                         xp.asarray(O.SELL_TURNS[BANK_LOT], i32)),
                _sw_pick(xp, _e2s_on,
                         lambda: xp.where(terminal, ENDROUTE2_SPLIT_MIN_VALUE,
                                          BANK_MIN_VALUE).astype(i32),
                         xp.asarray(BANK_MIN_VALUE, i32)),
                _sw_pick(xp, _e2s_on,
                         lambda: xp.where(terminal, ENDROUTE2_SPLIT_MAX_TURNS,
                                          BANK_MAX_TURNS).astype(i32),
                         xp.asarray(BANK_MAX_TURNS, i32)))
    harvest_first = True if HARVEST_FIRST_ON else None
    # [ROUTE_ORDER] The two intra-block reorders are one mechanism and never
    # compile together.
    assert not (HARVEST_FIRST_ON and ROUTE_ORDER_ON)
    route_order = True if ROUTE_ORDER_ON else None
    # [ROUTE_CUT] The assignment and the visiting order are one mechanism's two
    # halves and are never measured together.
    assert not (ROUTE_CUT_ON and (ROUTE_ORDER_ON or HARVEST_FIRST_ON))
    route_cut = True if ROUTE_CUT_ON else None
    # [TILE_ALLOC] The assignment at tile level owns the same block arrays the
    # two reorders above do, so it is one mechanism with them and never
    # compiles alongside one.
    assert not (TILE_ALLOC_ON and (ROUTE_ORDER_ON or HARVEST_FIRST_ON
                                   or ROUTE_CUT_ON))
    tile_alloc = True if TILE_ALLOC_ON else None
    # [MIDDAY_PLACE_V2] The melon tier rides on the excursion, so it is
    # offered only where there is one: `melon` is `None` when neither switch
    # asked for it, and the deposit it moves is `MIDDAY_PLACE_ON`'s.
    # [SAME_DAY_FERT] The tier is the half that makes the deposit reachable, so
    # it rides that switch too: the COLLECT ranks sweep to the head of the day
    # for the same reason the ripe melon does.
    melon_first = True if ((melon is not None and MIDDAY_PLACE_ON
                            and MIDDAY_PLACE_V2_ON) or SAME_DAY_FERT_ON) else None
    order_v = task_order(xp, d.task, d.tile_value, d.tier)
    rank_v = _inverse(xp, order_v)
    cum_est = xp.cumsum((d.n_ops + EST_MOVES)[order_v], dtype=i32)
    pick_masks = _pick_masks(xp, d)
    # Per-unit pickup allowance and per-unit shed walk, as in the hire scan
    # above [LAW, 0.12]. Both stay comfortably inside the budget they reduce:
    # `turn_budget` is 21 at worst, the pickup/land lead at most `N_PICK` = 5,
    # and `EST_LEAD` 5.
    labour = n_units * (turn_budget - xp.maximum(_pickup_kinds(xp, d), land_lead)
                       - _est_lead(xp, day))
    if ADMIT_PICK_SHARED:                       # [H5] see the block above
        labour = (n_units * (turn_budget - land_lead - _est_lead(xp, day))
                  - xp.maximum(_pickup_kinds(xp, d) - land_lead, 0))
    if DROP_ON:
        # The return leg, charged per unit like the outbound one. Deliberately
        # under the true mean: `_routes` charges the exact distance from each
        # block's real last tile and `ADMIT_ROUNDS` drops what that leaves
        # unreachable, so over-admitting here is repaired and under-admitting
        # is not.
        labour = labour - xp.where(drop_day, n_units * EST_HOME, 0)
    if ROUTE_EARLY_ON:
        # [SWITCH] The turn the early start buys, credited to the admit stage
        # optimistically -- for every unit, on every day the flag allows any of
        # them. Which units actually come out early is a property of the block
        # cut and does not exist here; and of the two errors only one is
        # repairable, since `ADMIT_ROUNDS` drops what the exact route cannot
        # reach and nothing ever adds a tile back. Without this the new turn has
        # nothing admitted to spend itself on.
        labour = labour + xp.where(route_early, n_units, 0)
    if ROUTE_SPLIT_ON:
        # [SWITCH] The same optimistic credit `ROUTE_EARLY_ON` takes, for the
        # same reason: which units come out early is a property of the block
        # cut and does not exist here, and of the two errors only over-admission
        # is repairable (`ADMIT_ROUNDS` drops what the exact route cannot
        # reach; nothing ever adds a tile back).
        labour = labour + xp.where(route_split, n_units, 0)
    if ADMIT_SLACK_ON:
        # [SWITCH, ADMITSLACK] The over-charged shed walk, handed back per
        # unit -- see the constant.  After every other budget correction, so
        # it is the last word on the day's labour and reads the same whichever
        # of them fired; and before the repair loop, which is what makes the
        # error it can introduce the repairable one.
        labour = labour + n_units * ADMIT_SLACK_TURNS
    if H23_WATER_ON:
        # [SWITCH, CREW24] The h21-23 tail, credited to the admit stage from
        # `H23_WATER_DAY0` (never the terminal day, whose routes end at the
        # last row); `ADMIT_ROUNDS` below repairs any over-admission.
        labour = labour + xp.where(
            (_as(xp, day) >= H23_WATER_DAY0) & ~terminal,
            n_units * H23_WATER_TURNS, 0)
    elif CREW_RELAY_ON and CREW_RELAY_H23:
        # [SWITCH, CREWRELAY1] the h21-23 credit over the relay's life only.
        labour = labour + xp.where(
            (_as(xp, day) >= int(RELAY_DAYS[0])) & (_as(xp, day) <= int(RELAY_LAST_HARVEST))
            & ~terminal, n_units * H23_WATER_TURNS, 0)
    elif FILL_WORK_ON and FILL_WORK_H23:
        # [SWITCH, FILLWORK1] the h21-23 credit over the fill's life only.
        labour = labour + xp.where(
            (_as(xp, day) >= int(FILL_WORK_DAYS[0])) & (_as(xp, day) <= int(RELAY_LAST_HARVEST))
            & ~terminal, n_units * H23_WATER_TURNS, 0)
    n_admit = xp.minimum(_count_le(xp, cum_est, labour), n_tasks).astype(i32)
    route_tier = (d.tile_value > 0).astype(i32)
    program_return = None
    if pe is not None:
        ripe_melon = ((view.kind == spec.KIND_PLANT)
                      & (view.occ == spec.I_MELON)
                      & xp.any(d.chain_op == O.OP_HARVEST, axis=1))
        funding_collect = ((day <= 9)
                           & xp.any(d.chain_op == O.OP_COLLECT_FERT, axis=1))
        return_work = (ripe_melon | funding_collect) & ~terminal
        route_tier = xp.where(return_work, 2, route_tier).astype(i32)
        funding_count = xp.sum(funding_collect.astype(i32))
        carriers = xp.maximum(n_units - 1, 1)
        funding_batch = xp.where(day <= 9,
            xp.maximum((funding_count + carriers - 1) // carriers, 1), N_T)
        program_return = (return_work, route_base,
                          xp.where(day <= 9, O.SELL_TURNS[-1], spec.TURNS_PER_DAY - 1).astype(i32), funding_batch)
    if melon_first is not None:                                  # [SWITCH]
        # [MIDDAY_PLACE_V2] The day's ripe melon sweeps first, one tier above
        # the priced tiles. This is the *day's* reorder rather than a block's,
        # and it is the one that works: a block is a contiguous run of this
        # order, so a melon rank the order leaves late is a rank no block can
        # bank in time however the block sweeps itself. `task_order` takes any
        # int32 tier [LAW, 0.5]; the route order is not the admission order
        # (`order_v`, `rank_v` and `n_admit` are untouched, so no tile loses
        # its place in the value queue); and every block cut, `covered` and
        # the `start` walk downstream read the new order natively, which is
        # what a per-unit reorder could not give -- there the cut still walked
        # the unreordered `load` and spent the excursion's reserve on the very
        # ranks the reorder had pulled forward. Measured 30 -> 60 of 72 units
        # sold on the dump day (`S/mp2/`).
        route_tier = xp.where(melon[0] & melon[1], 2, route_tier).astype(i32)
    if pe is not None:
        admit_low, admit_high = xp.asarray(0, i32), n_tasks
        best_routes = None
        best_score = xp.asarray(-1, i32)
        best_admit = xp.asarray(0, i32)

        def choose_routes(take, new, old=None):
            if new is None:
                return None
            if isinstance(new, tuple):
                return tuple(choose_routes(take, a, None if old is None else old[j])
                             for j, a in enumerate(new))
            return xp.where(take, new, xp.zeros_like(new) if old is None else old)

    for _ in range(7 if pe is not None else ADMIT_ROUNDS):
        admitted = d.task & (rank_v < n_admit)
        order = task_order(xp, admitted, xp.zeros(N_T, i32), route_tier)
        tail_care = None
        if TAIL_CARE_ON:
            # [SWITCH] The admitted set is the round's own, so the candidate
            # masks are built here and not with the static half above: a feed
            # the admit stage dropped is a feed the day does not do, and its
            # tile is back in play for the tail.
            tc_fed_by_day = tc_plan_feed & admitted
            tc_cared_by_day = tc_plan_care & admitted
            tail_care = TailCare(
                need_feed=tc_unfed & ~tc_fed_by_day,
                need_care=tc_uncared & ~tc_cared_by_day,
                fed_anyway=tc_animal & (~tc_unfed | tc_fed_by_day),
                starving=tc_starving,
                wheat=tc_wheat)
        care_fill = None
        if CARE_FILL_ON:
            # [SWITCH] The round's own half: a feed the admit stage dropped is
            # a feed the day does not do, so its animal is not fed tonight and
            # a CARE on it would bank nothing; and a care the round *does* plan
            # is a tile the engine would no-op on a second visit.
            care_fill = (cf_static & ~(cf_plan_care & admitted)
                         & (cf_fed_now | (cf_plan_feed & admitted)))
        routed = _routes(
            xp, d.chain_op, d.chain_a, d.chain_q, d.n_ops, order, n_admit, pick_masks,
            n_units, turn_budget, land_lead, drop_day=drop_day,
            route_early=route_early, route_split=route_split, wide=wide,
            farmer0=farmer0, freefirst=freefirst, seedfree=seedfree, widepick=widepick,
            wpfree=wpfree,
            tail_fill=tail_fill, tail_care=tail_care, care_fill=care_fill,
            melon=melon, bank=bank, harvest_first=harvest_first,
            route_order=route_order, route_cut=route_cut,
            tile_alloc=tile_alloc, program_return=program_return)
        covered = routed[4]
        missed = xp.sum((admitted & ~covered).astype(i32), dtype=i32)
        if pe is not None:
            # A short failed route is not proof that all its missing work
            # must be discarded. Search the admitted prefix and retain the
            # candidate with the most completed priority/value, even when
            # one unreachable task would otherwise discard useful paid work.
            fits = missed == 0
            score = xp.sum(xp.where(covered & d.task,
                d.tier * (BUD.VALUE_CAP + 1) + d.tile_value, 0), dtype=i32)
            better = score > best_score
            best_routes = choose_routes(better, routed, best_routes)
            best_score = xp.maximum(best_score, score)
            best_admit = xp.where(better, n_admit, best_admit).astype(i32)
            admit_low = xp.where(fits, n_admit, admit_low).astype(i32)
            admit_high = xp.where(fits, admit_high, n_admit - 1).astype(i32)
            n_admit = ((admit_low + admit_high + 1) // 2).astype(i32)
        else:
            n_admit = (n_admit - missed).astype(i32)
            if PLAN_FASTPATH_ON and xp is np and int(missed) == 0:   # [SWITCH, REVFIX1 B2] converged: later rounds repeat it
                break
    if pe is not None:
        routed, n_admit = best_routes, best_admit
        admitted = d.task & (rank_v < n_admit)
    (route_op, route_a, route_q, blk, covered, n_pick, lead, early,
     bank_mask) = routed
    if ESWORK_THETA is not None and xp is np and d.relay is not None:   # [WHEATMIX1] census: relay planned / routed / hands
        MR_LAST[:] = [int(np.sum(d.relay)), int(np.sum(d.relay & covered)), int(n_hire)]
    if program_return is not None:
        bank_mask, program_bank_mask = bank_mask

    # The hands the HIRE row asks for, which is `n_hire` and only `n_hire` off
    # this switch. ON it is the hands `_routes` actually loaded: `route_op[1:]`
    # is the crew (row 0 is the farmer, who is never hired), a unit `_routes`
    # left inactive is all-PASS by construction and an active one always emits
    # its opening op, so `acts` is exact. Taken as the smallest prefix holding
    # every acting hand -- hand `u` runs unit `u`'s route, so an acting hand
    # must be inside the row -- which is the population count whenever the idle
    # hands are the trailing ones, as they were on all 960 measured day-rows.
    n_hire_row = n_hire
    if HIRE_ROW_ON and not (MACRO_EXEC_ON and MACRO_SCHEDULE is not None
                            and _macro_site(6)):
        # [SWITCH] ... and the fifth MACRO_EXEC site, by exclusion. This trim
        # is the last task-set gate on the crew: a hand whose route is all PASS
        # is not hired at all. Programme targets are conditional on real work;
        # a hand hired today does not persist into tomorrow. That is right when the enumeration chose the
        # count off today's work, and wrong under a schedule, whose whole
        # premise is that the ramp is bought before the work exists
        # (build story 2026-09-09: the top hires four on day 1 onto twelve
        # melon tiles that emit no task until day 6). Under a schedule the
        # HIRE row asks for the crew the schedule asked for, and the idle
        # hands' fib bill is part of what the executability gate measures.
        acts = xp.any(route_op[1:] != O.OP_PASS, axis=1)
        hand_ix = xp.arange(1, MU, dtype=i32)
        n_act = xp.max(xp.where(acts, hand_ix, xp.asarray(0, i32))).astype(i32)
        n_hire_row = xp.minimum(n_hire, n_act).astype(i32)

    t = xp.arange(TPD, dtype=i32)[None, :]
    # Where each unit's route sits in the day: it starts at the base plus its
    # own leading idle turns and runs to the end of the day's budget.
    start_u = (route_base + lead).astype(i32)
    walk_u = (turn_budget - lead).astype(i32)
    if ROUTE_EARLY_ON:
        # [SWITCH] One turn earlier and one turn longer, for the units
        # `_routes` found nothing in the BUY row to wait for. `lead` is 0 for
        # every one of them by construction (no pickup, and the flag is off on
        # a land day), so this is the whole of the per-unit start.
        start_u = (start_u - early).astype(i32)
        walk_u = (walk_u + early).astype(i32)
    if ROUTE_SPLIT_ON:
        # [SWITCH] One turn earlier and one turn longer, for the units
        # `_routes` found a turn for -- a narrow-day block the BUY row does not
        # feed, or a wide-day block whose first turn is a stationary PICKUP.
        # `lead` already holds the pickup turns, so this shifts the whole
        # schedule and the pickup rows below go with it.
        start_u = (start_u - early).astype(i32)
        walk_u = (walk_u + early).astype(i32)
    if PRESTOCK_V2_FARMER0_ON and not ROUTE_SPLIT_ON:
        # [SWITCH, PRESTOCK_V2] The same one shift, when `ROUTE_SPLIT_ON` is
        # not there to apply it. ONE application whatever is on: `early` is one
        # vector and applying it twice is what cost `ROUTE_EARLY` a season
        # (`2026-09-11-route-early-bug.md`).
        start_u = (start_u - early).astype(i32)
        walk_u = (walk_u + early).astype(i32)
    r = t - start_u[:, None]
    on_route = (r >= 0) & (r < walk_u[:, None])
    rc = xp.clip(r, 0, TPD - 1) + xp.zeros((MU, 1), i32)
    unit_op = xp.where(on_route, xp.take_along_axis(route_op, rc, axis=1), O.OP_PASS).astype(i32)
    unit_a = xp.where(on_route, xp.take_along_axis(route_a, rc, axis=1), 0).astype(i32)
    unit_q = xp.where(on_route, xp.take_along_axis(route_q, rc, axis=1), 0).astype(i32)

    # ---- morning PICKUPs --------------------------------------------------
    # Each unit picks up what its own block consumes, one kind per turn from
    # the day's route base, before it leaves its shed-access spawn tile (PICKUP
    # is silently dropped anywhere else). The base is never earlier than
    # TURN_BUY + 1, so the shed already holds what the BUY row bought -- and
    # `route_base` and not `start_u` is still the right turn under
    # `ROUTE_EARLY_ON` [SWITCH]: a unit only starts early when its block owes
    # no pickup at all, so `blk` is zero down its whole column and none of
    # these rows can fire for it.
    pk_active = (blk > 0).astype(i32)                                # [N_PICK, MU]
    pk_base = route_base
    if ROUTE_SPLIT_ON:
        # [SWITCH] The one place a pickup row moves. On a *wide* day the turn
        # `_routes` hands a unit is the stationary one it spends collecting, so
        # its rows start at `O.ROUTE_BASE_WIDE - 1` = `TURN_BUY + 1` -- still
        # after the BUY row resolves, and still on the unit's spawn tile, which
        # is what the turn-2 hire row's occupancy count needs [`market._hire`].
        # On a narrow day an early unit owes no pickup at all (`blk` is zero
        # down its column), so the shift is inert there and the expression is
        # written as the law rather than as the arithmetic.
        pk_base = (route_base - xp.where(wide, early, 0)).astype(i32)
        if ROUTE_FREEFIRST_ON or EVE_STOCK_ON or H1_WORK_ON:
            # [SWITCH, ROUTE_FREEFIRST] A narrow-day early block may now owe
            # pickups, so its rows move with its start exactly as a wide one's
            # do -- to `TURN_BUY`, where the shed still holds last night's
            # close and the kinds the block collects were not bought today.
            # Identical to the line above on a wide day (`early` is the same
            # vector) and on every day this switch declines (`early` is zero
            # wherever `narrow_ok` was not widened).
            pk_base = (route_base - early).astype(i32)
    if PRESTOCK_V2_FARMER0_ON:
        # [SWITCH, PRESTOCK_V2] The farmer's pickup rows move with its start --
        # which is the whole of the turn it bought, the block behind them being
        # unchanged in shape. Narrow only (V2's day predicate is), so this
        # never doubles `ROUTE_SPLIT`'s wide-day shift above.
        is_u0 = (xp.arange(MU, dtype=i32) == 0)
        pk_base = (pk_base - xp.where(is_u0 & (~wide), early, 0)).astype(i32)
    # `.astype(i32)`: numpy's cumsum widens int32 to int64, JAX does not.
    pk_turn = (xp.cumsum(pk_active, axis=0) - pk_active + pk_base).astype(i32)
    if wpfree is not None:
        # [SWITCH, WIDE_PICK_FREE] The cumsum above is exactly "kind i sits
        # behind every active kind of lower index", i.e. a stable sort on the
        # key `index`. Re-key it `(delivered by today's BUY row, index)` and the
        # same stable sort puts a FREE kind on the block's first row -- turn 1,
        # whose market phase has not run yet -- while leaving the bought kinds
        # in their shipped relative order behind it. `key` is `widepick & wpfree`,
        # so an OFF value keys every kind 0 and `pos` collapses onto `pk_turn`
        # term for term.
        #
        # Applied to the granted column ALONE (`early == 2` is `wide2` and
        # nothing else, `_routes` writing that 2 only there): every other unit
        # starts at `O.ROUTE_BASE` or later, where the row has resolved and the
        # order is worth nothing, so re-ordering it would only move plans.
        _key = widepick & wpfree if wpfree is not True else widepick
        _pos = []
        for i in range(N_PICK):
            acc = xp.zeros_like(pk_active[i])
            for j in range(N_PICK):
                if j == i:
                    continue
                before = ((~_key[j]) & _key[i]) | ((_key[j] == _key[i])
                                                   & bool(j < i))
                acc = (acc + pk_active[j] * before.astype(i32)).astype(i32)
            _pos.append(acc)
        pk_free = (xp.stack(_pos).astype(i32) + pk_base).astype(i32)
        pk_turn = xp.where((early == 2)[None, :], pk_free, pk_turn).astype(i32)
    # Fully static since the mixed herd: one row per animal kind, rather than
    # the one dynamic `I_GOOSE + a_kind` row a single-kind day needed.
    pk_item = xp.asarray(PICK_ITEM)
    for i in range(N_PICK):
        hit = (pk_active[i][:, None] > 0) & (t == pk_turn[i][:, None])
        unit_op = xp.where(hit, O.OP_PICKUP, unit_op)
        unit_a = xp.where(hit, pk_item[i], unit_a)
        unit_q = xp.where(hit, blk[i][:, None], unit_q)

    unit_op = xp.where(idle, O.OP_PASS, unit_op).astype(i32)
    unit_a = xp.where(idle, 0, unit_a).astype(i32)
    unit_q = xp.where(idle, 0, unit_q).astype(i32)

    # ---- what the sale may draw on ----------------------------------------
    # Shed contents only: the day's harvest reaches the shed at end-of-day and
    # is sold tomorrow morning, so the hour-0 stock is exactly what the lots
    # can draw on. Feed wheat and the day's fertilizer are held back. On the
    # terminal day every reservation is void and the whole shed goes.
    wheat_reserved = xp.where(terminal, 0, xp.sum(d.want_feed.astype(i32))).astype(i32)
    avail = view.shed[:spec.N_PRODUCTS].astype(i32)
    avail = _set1(xp, avail, spec.I_WHEAT,
                  xp.maximum(avail[spec.I_WHEAT] - wheat_reserved, 0))
    # The day's FERTILIZE tasks pick their fertilizer up from the route base
    # on, which straddles sell lot 1 at turn 3 [LAW, 0.7] -- a unit that picks
    # up at turn 3 does so before that turn's market resolves, and one that
    # picks up later takes what the sale left. Reserve it like feed wheat.
    fert_reserved = d.n_fert_eff
    if FERT_RESERVE_ON:
        # [SWITCH, FERT_RESERVE] Fertilizer is an INPUT, not a product: what the
        # lots may sell is the surplus over the applications the REMAINING plan
        # will want, by backward recurrence over the days ahead net of the herd's
        # own daily unit (`_fert_future_reserve`). OFF this line is the one
        # `d.n_fert_eff` above and nothing is built.
        fert_reserved = (fert_reserved + _fert_future_reserve(
            xp, view, d.want_fert)).astype(i32)
    fert_reserved = xp.where(terminal, 0, fert_reserved).astype(i32)
    avail = _set1(xp, avail, spec.I_FERT,
                  xp.maximum(avail[spec.I_FERT] - fert_reserved, 0))
    # [SWITCH, SELL_SPREAD] The last days' stock is a stream, not a dump: cap
    # what the VOLUNTARY sale may draw on at `stock // days_left`.  The cap is
    # on `avail_vol` alone -- the hours, the reservation, the pressure term and
    # the whole day-29 route family are the ones that were there, and the
    # forced-overflow sale below keeps reading the UNCAPPED `avail`, so a
    # quota can never hold back stock the night would then destroy.  OFF the
    # name is the same array and nothing is built.
    avail_vol = avail
    if SELL_SPREAD_ON:
        avail_vol = _sell_spread_cap(xp, avail, view.day, terminal)
    # ---- the sale [HEURISTIC, 1.2] ----------------------------------------
    # Whether to sell is the reservation value; when is the timing pressure
    # against the projected lot curves. The terminal value of anything unsold
    # on day 29 is exactly zero, so the reservation is void there [LAW, 0.4]
    # -- `LIQUIDATE`, not 0: an adjusted marginal (net of pressure and the
    # externality) can be negative, and day 29 must sell regardless.
    hold = _sell_hold(xp, price_table,
                      xp.where(terminal, SELL.LIQUIDATE, macro.hold).astype(i32),
                      terminal, day=view.day)
    # Projected once and handed to both allocator passes below: the lot curves
    # depend on the view alone, and the forced-overflow continuation must see
    # the very same ones the voluntary allocation was greedy over.
    # [EARLY_SELL] On the turns the lots are actually emitted on (`_rows` reads
    # the same `early_lot_turns()`), not on `O.SELL_TURNS` regardless of mode:
    # a lot priced against a shelf drained by turns it never waits for is a lot
    # the greedy will not use, which is how mode "B" left lot 2 empty and its
    # volume in the hour-19 residue. Inert under the shipped mode "A", whose
    # lot turns *are* `O.SELL_TURNS`.
    # [OPP_SUPPLY] `view.day` rides along so each lot can carry the other
    # seat's forecast supply; inert while `OPP_SUPPLY_ON` is off.
    inv_lots = SELL.lot_inventories(xp, view.mkt_inv, view.shops,
                                    early_lot_turns(), _osd(view.day, "S"))
    lots = SELL.allocate(xp, price_table, view.mkt_inv, view.shops, avail_vol, hold, macro.press,
                         inv_lots=inv_lots)
    if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:
        # [SWITCH, MACRO_EXEC] Site 7, the sale-timing channel: each product's
        # whole voluntary sale resolves on the LOT THAT CARRIES THE HOUR THE
        # SCHEDULE SOLD IT ON.
        #
        # What the schedule actually holds. `extract.py` records
        # `sell_hour[day][product]` -- the first turn a SELL row for that
        # product resolved on the tape -- and *nothing about the quantity*, so
        # "sell up to q at hour h" is not expressible here and "sell at h" is.
        # ymg_aq's hours are early: median 0-1 for wheat, carrot, egg and
        # fertilizer, 5 for straw, against our three lots on turns 3/10/18
        # (`early_lot_turns()`). So this rule mostly pulls volume FORWARD out
        # of lots 2 and 3 into lot 1, which is the half of the channel a pure
        # hold could not test.
        #
        # The mapping, per product: the target lot is the first whose turn is
        # at or after the hour; every voluntary unit of that product moves
        # there. A product whose hour is past the last lot (`straw` on three
        # days, `wool` on two) sells nothing voluntarily today -- there is no
        # row left to carry it. `-1` (the tape sold none of it that day) is no
        # constraint rather than a ban: the channel under test is WHEN, and a
        # day the top holds a product is a day our own reservation still
        # decides. The shed law is downstream and untouched -- whatever a hold
        # overflows tonight is still force-sold below, at the overflow's own
        # lot.
        if _macro_site(7):
            hour = _macro_row(xp, view.day, "sell")[:spec.N_PRODUCTS].astype(i32)
            l_turn = xp.asarray(list(early_lot_turns()), i32)[:, None]
            late = (l_turn >= hour[None, :])
            first = xp.argmax(late.astype(i32), axis=0).astype(i32)
            l_ix = xp.arange(n_lots(), dtype=i32)[:, None]
            # `"sell_late"` splits the channel in half: it keeps whatever the
            # allocator already placed at or after the hour and only carries
            # the units that would have resolved too early, so the arm is the
            # DELAY alone. `"sell"` moves the whole sale onto the hour's lot,
            # delay and pull-forward together.
            keep = xp.where(late, lots, 0).astype(i32)
            if MACRO_MODE == "sell_late":
                base, move = keep, xp.sum(lots - keep, axis=0, dtype=i32)
            else:
                base, move = xp.zeros_like(lots), xp.sum(lots, axis=0, dtype=i32)
            move = xp.where(xp.any(late, axis=0), move, 0).astype(i32)
            timed = (base + (l_ix == first[None, :]).astype(i32)
                     * move[None, :]).astype(i32)
            lots = xp.where((hour >= 0)[None, :], timed, lots).astype(i32)
        if _macro_site(8):
            # [SELL-LOT] Site 8, own-clock lot placement. The schedule is not
            # read here at all -- the mode alone names the lot -- and the arm
            # exists because MACRO-CHANNELS §3.1 priced the same knob from the
            # wrong end: obeying ymg_aq's hours cost -1,595 on EGG by dumping
            # the day's whole egg sale into lot 1, so lot placement of a
            # daily-output product is a live gradient and these three arms
            # sweep it.
            #
            # QUANTITIES are the allocator's: `move` is exactly what the
            # value-gated greedy already decided to sell today, so nothing the
            # reservation refused is sold and nothing it accepted is held --
            # only the row it stands on changes. The shed law downstream is
            # untouched, and so is `s_qty` in total, so the overflow deficit
            # is the same number it was.
            #
            # `SELL_LOT_PRODUCTS` restricts the move to a subset (None = all),
            # which is how one product's lot can be priced without the other
            # eight moving underneath it.
            k_lot = _MACRO_LOT.index(MACRO_MODE)
            l_ix = xp.arange(n_lots(), dtype=i32)[:, None]
            move = xp.sum(lots, axis=0, dtype=i32)
            pinned = ((l_ix == k_lot).astype(i32) * move[None, :]).astype(i32)
            if SELL_LOT_PRODUCTS is None:
                lots = pinned.astype(i32)
            else:
                # A bare int is one product, so a runner can name it on a
                # `--switches` line without a literal tuple.
                _ids = (tuple(SELL_LOT_PRODUCTS)
                        if isinstance(SELL_LOT_PRODUCTS, (list, tuple))
                        else (int(SELL_LOT_PRODUCTS),))
                sel = xp.asarray([p in _ids for p in range(spec.N_PRODUCTS)])
                lots = xp.where(sel[None, :], pinned, lots).astype(i32)
    if LOT_SPLIT_ON:
        # [LOT-DEPTH, SWITCH] Lot depth is what a lot costs itself: a lot is
        # one market order and a SELL walks its own quote down unit by unit,
        # so 64 units in one row clear below 3 rows of 21 whenever the town
        # tick has moved the shelf between the turns. The cap reshapes the
        # VOLUNTARY allocation alone and conserves `s_qty` exactly, so the
        # overflow deficit below and every bulk add above are untouched.
        lots = _lot_split(xp, lots, day)
    s_qty = xp.sum(lots, axis=0).astype(i32)
    # [SPREAD_ROWS] The VOLUNTARY allocation, snapshotted where `s_qty` is
    # summed from it -- before a single bulk add. Off the switch nothing reads
    # it. See the switch's own block for why the difference against the final
    # `lots` is non-negative by construction.
    vol_lots = lots

    # ---- shed overflow: forced sale [LAW, 0.9] ---------------------------
    # End-of-day destroys whatever the shed cannot hold. Project tonight's
    # shed conservatively-LOW -- only inflow that is certain: the banked yield
    # of harvests the route reaches (today's watering bonuses excluded), one
    # fertilizer per reached COLLECT, this morning's buys -- against every
    # certain outflow: the planned sale and the pickups the reached tasks
    # consume. Whatever still does not fit is sold today on top of the gated
    # sale, cheapest marginal unit first. Forced sales draw only on the
    # hour-0 stock net of reservations, so a day whose certain inflow alone
    # exceeds the shed still overflows (harvest batching: open, section 5).
    has_harv = xp.sum((d.chain_op == O.OP_HARVEST).astype(i32), axis=1) > 0
    has_coll = xp.sum((d.chain_op == O.OP_COLLECT_FERT).astype(i32), axis=1) > 0
    # [SWITCH, SHED_DEFICIT] The watering bonus, on the same term
    # `BANK_BEFORE_LOT_ON` (`bl_units`), `MELON_OPEN` (`m_units`) and
    # `MIDDAY_PLACE_V2` (`mv_units`) already use: a chain that waters a tile
    # before harvesting it banks `t_yield + 2` tonight, not `t_yield`. OFF the
    # expression is `view.t_yield` unchanged, so nothing is evaluated at all.
    def _sd_yield():
        sd_w = xp.sum((d.chain_op == O.OP_WATER).astype(i32), axis=1) > 0
        return (view.t_yield + 2 * sd_w.astype(i32)).astype(i32)

    sd_yield = _sw_pick(xp, _sw(macro, "SHED_DEFICIT_ON"), _sd_yield, view.t_yield)
    inflow = (xp.sum(xp.where(covered & has_harv, sd_yield, 0).astype(i32))
              + xp.sum((covered & has_coll).astype(i32)))
    buys_in = (d.wheat_buy + d.fert_bought
               + xp.sum(d.a_buy, dtype=i32)).astype(i32)   # <= hour-0 room by the grant's clamp
    picks_out = xp.sum(blk).astype(i32)           # wheat fed, fertilizer spread, animals placed
    proj_eod = xp.sum(view.shed.astype(i32)) - xp.sum(s_qty) - picks_out + buys_in + inflow
    deficit = xp.maximum(proj_eod - spec.SHED_CAPACITY, 0).astype(i32)
    # Non-terminal only: `covered`, `blk` and `chain_op` are the day the route
    # *would* have walked, computed before the terminal PASS override above, so
    # past LAST_SHED_DAY they describe a day that never happens -- and there is
    # no end-of-day left to destroy anything anyway. Gate it here rather than
    # leaning on `spare == 0` holding after the liquidation.
    deficit = xp.where(terminal, 0, deficit).astype(i32)

    # Rank by the projected marginal price after the planned sale (lot-1
    # inventory). Quotes fall as a product is sold down, so the cheapest
    # product stays cheapest until it is spent: draining products in ascending
    # marginal quote is the unit-by-unit greedy, in nine static rounds. Two
    # ranking-only approximations, both bounded by one lot's worth of curve:
    # the lot-1 inventory is the town-tick projection alone -- it ignores the
    # drain this same plan's turn-1 BUY_PRODUCT does to those very products, so
    # a heavily bought one ranks a little cheap -- and `marg` charges the whole
    # voluntary sale `s_qty` against that lot-1 curve although the allocator
    # may have spread it over turns 10 and 18, where the town has drained the
    # inventory further, so a product sold late ranks a little dear. The forced
    # *quantity* is the deficit either way -- this ranking only decides which
    # products give the units up, and the placement below then reads the real
    # lot curves.
    spare = xp.maximum(avail - s_qty, 0).astype(i32)
    inv_lot1 = PJ.projected_inv(xp, view.mkt_inv, view.shops, O.SELL_TURNS[0],
                                _osd(view.day, "S"))
    marg = PJ.marginal_quote(xp, PJ.sell_quotes(xp, price_table, inv_lot1), s_qty)
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)
    forced = xp.zeros(spec.N_PRODUCTS, i32)
    left = deficit
    for _ in range(spec.N_PRODUCTS):
        key = xp.where(spare > 0, marg * spec.N_PRODUCTS + pid, _DRAINED)  # ties: lower index
        pick = xp.argmin(key)
        amt = xp.where(spare[pick] > 0, xp.minimum(left, spare[pick]), 0).astype(i32)
        hit = (pid == pick).astype(i32)
        forced = forced + hit * amt
        spare = spare - hit * spare[pick]
        left = left - amt
    # Forced overflow units bypass the reservation and take the lot whose
    # adjusted marginal is highest after the value-gated allocation [0.9], in
    # bulk.
    #
    # Bulk placement is a *measured* choice, not the ideal one. Continuing the
    # greedy instead -- `SELL.allocate(..., avail=s_qty + forced,
    # hold=where(forced > 0, LIQUIDATE, hold), lots0=lots,
    # rounds=SHED_CAPACITY)`, which is exactly what `allocate`'s `lots0` and
    # `rounds` arguments exist for -- prices every forced unit on the curve the
    # ones before it left, and is worth real coins: on a one-yarn-store town
    # with `press` = 3, ten forced wool fetch 2,163 placed unit by unit against
    # 2,091 placed in bulk, 3.4% (`test_sell_allocator.py`). It costs a second
    # 100-round allocator pass inside the day scan, measured at **-5.2%**
    # episode throughput (1,137 -> 1,079 eps/s, B = 1024), over the 5% gate
    # this placement was benchmarked against, so the bulk answer ships and the
    # continuation stays available for a cheaper formulation.
    forced_lot = xp.argmax(
        SELL.adjusted_marginals(xp, price_table, inv_lots, lots, macro.press.astype(i32)),
        axis=0).astype(i32)
    lot_ix = xp.arange(n_lots(), dtype=i32)[:, None]
    lots = (lots + (lot_ix == forced_lot[None, :]).astype(i32) * forced[None, :]).astype(i32)

    if DROP_ON:
        # The mid-day shed [section 4]. Lots 1 and 2 draw on the hour-0 stock
        # alone, which is all the shed holds when they resolve; the DROP lands
        # by turn 18, so lot 3 -- and only lot 3 -- may also offer what the
        # route banks. Asking for more than arrives costs nothing: a SELL is
        # clipped to the shed unit by unit in both the engine (`_commit_unit`)
        # and the simulator (`market._inventory_orders`), so the two extra
        # units charged for a possible in-window watering are free insurance
        # against asking for too few, while a product with nothing coming keeps
        # its slot empty and the two seats' rows compact as they always did.
        h_water = xp.sum((d.chain_op == O.OP_WATER).astype(i32), axis=1) > 0
        an_p = xp.asarray(spec.ANIMAL_PRODUCT)[xp.clip(view.occ, 0, spec.N_ANIMALS - 1)]
        prod_of = xp.where(view.kind == spec.KIND_PLANT,
                           xp.clip(view.occ, 0, spec.N_CROPS - 1), an_p).astype(i32)
        banked = xp.where(covered & has_harv,
                          view.t_yield + 2 * h_water.astype(i32), 0).astype(i32)
        oh = (xp.arange(spec.N_PRODUCTS, dtype=i32)[:, None] == prod_of[None, :]).astype(i32)
        gain = xp.where(drop_day, xp.sum(oh * banked[None, :], axis=1, dtype=i32), 0)
        gain = xp.minimum(gain, spec.SHED_CAPACITY).astype(i32)
        last_lot = (xp.arange(n_lots(), dtype=i32) == n_lots() - 1).astype(i32)
        lots = (lots + last_lot[:, None] * gain[None, :]).astype(i32)

    if program_return is not None:
        # These dedicated blocks end at the shed by the final ordinary lot.
        pr_mask = program_bank_mask
        pr_prod = xp.where(view.kind == spec.KIND_PLANT, view.occ,
                           xp.asarray(spec.ANIMAL_PRODUCT)[xp.clip(
                               view.occ, 0, spec.N_ANIMALS - 1)])
        pr_oh = xp.arange(spec.N_PRODUCTS)[:, None] == pr_prod[None, :]
        pr_units = xp.sum(pr_oh * xp.where(pr_mask & has_harv,
                                           view.t_yield + 2, 0)[None, :],
                          axis=1, dtype=i32)
        pr_units += (xp.arange(spec.N_PRODUCTS) == spec.I_FERT).astype(i32) * xp.sum(
            (pr_mask & has_coll).astype(i32), dtype=i32)
        pr_row = (xp.arange(n_lots()) == n_lots() - 1).astype(i32)
        lots = (lots + pr_row[:, None]
                * xp.minimum(pr_units, spec.SHED_CAPACITY)[None, :]).astype(i32)

    melon_lots = None
    if MELON_OPEN_ON:
        # [MELON_OPEN] What the excursion banks, offered in lots of at most
        # `MELON_OPEN_LOT` on the turns whose engine hours are still in front
        # of the opponent's dump, and once more on the day's own last lot so
        # nothing the early rows could not reach is carried into a day-11
        # quote the opponent has already crushed. Asking for more than arrives
        # costs nothing: every SELL is clipped to the shed unit by unit in both
        # the engine (`_commit_unit`) and the simulator
        # (`market._inventory_orders`), and a row with nothing behind it keeps
        # its slot empty exactly as the DROP branch above relies on.
        is_mel_p = (view.kind == spec.KIND_PLANT) & (view.occ == spec.I_MELON)
        m_units = xp.sum(xp.where(covered & has_harv & is_mel_p,
                                  view.t_yield + 2 * h_water.astype(i32), 0),
                         dtype=i32).astype(i32)
        m_units = xp.where(day == MELON_OPEN_HARVEST_DAY,
                           xp.minimum(m_units, spec.SHED_CAPACITY), 0).astype(i32)
        cap = xp.asarray(MELON_OPEN_LOT, i32)
        melon_lots = xp.stack(
            [xp.clip(m_units - k * cap, 0, cap) for k in range(len(melon_lot_turns()))]
        ).astype(i32)
        last_lot = (xp.arange(n_lots(), dtype=i32) == n_lots() - 1).astype(i32)
        is_m = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_MELON).astype(i32)
        lots = (lots + last_lot[:, None] * is_m[None, :] * m_units).astype(i32)

    if MIDDAY_PLACE_V2_ON:                                       # [SWITCH]
        # [MIDDAY_PLACE_V2] The second half of the deposit, and the half
        # without which the first sells nothing. `avail` above is the hour-0
        # shed and the greedy allocated against it at dawn, so on a harvest
        # day melon's slot in every lot is *empty* -- the crop is still on the
        # vine -- and the PLACE lands in a shed no row of the day offers.
        # Measured: the excursion fires and banks (day 13 turn 17, day 14
        # turns 13 and 14, day 15 turns 12 and 18, day 16 turn 15, seed
        # 899009257 seat 0), and every one of those units then sits until
        # `_end_of_day` and sells on the next morning's opening row, which is
        # the very thing the switch exists to beat.
        #
        # So the banked units are added to the day's LAST lot in bulk, exactly
        # as `DROP_ON`'s return leg and `BANK_BEFORE_LOT_ON`'s DROP add theirs
        # and for the same reasons: `MIDDAY_PLACE_V2_TURN` is that lot's turn
        # by construction, so it is the only row a deposit judged in time can
        # reach; a unit acts before its turn's market, so a PLACE on turn 18
        # still sells on turn 18's row; and over-asking is free, since every
        # SELL is clipped to the shed unit by unit in the engine
        # (`_commit_unit`) and the simulator (`market._inventory_orders`).
        #
        # Melon alone, because melon alone is what the PLACE banks
        # (`u_a = spec.I_MELON` in `_routes`): the rest of the block's load
        # stays on the unit, which is the whole point of PLACE over DROP.
        mv_w = xp.sum((d.chain_op == O.OP_WATER).astype(i32), axis=1) > 0
        mv_mel = (view.kind == spec.KIND_PLANT) & (view.occ == spec.I_MELON)
        mv_units = xp.sum(xp.where(bank_mask & has_harv & mv_mel,
                                   view.t_yield + 2 * mv_w.astype(i32), 0),
                          dtype=i32).astype(i32)
        mv_units = xp.minimum(mv_units, spec.SHED_CAPACITY).astype(i32)
        mv_row = (xp.arange(n_lots(), dtype=i32) == n_lots() - 1).astype(i32)
        mv_is_m = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_MELON).astype(i32)
        lots = (lots + mv_row[:, None] * mv_is_m[None, :] * mv_units).astype(i32)

    if SAME_DAY_FERT_ON:                                         # [SWITCH]
        # [SAME_DAY_FERT] The row the deposit stands on. `avail` above is the
        # hour-0 shed and the greedy allocated against it at dawn, where the
        # day's fertilizer does not exist yet -- it is still under the animals
        # -- so fertilizer's slot in every lot is sized without it and a
        # mid-day PLACE would sit in the shed until `_end_of_day` and sell on
        # the next morning's row, which is the very thing the switch exists to
        # beat. One unit per COLLECT rank the excursion carried in
        # (`bank_mask` is `[s, m_ins]` per banking block, `has_coll` picks the
        # ranks that actually produce), added to the day's LAST lot in bulk:
        # that lot's turn is `_midday_place_turn()` by construction, a unit
        # acts before its turn's market, and over-asking is free because every
        # SELL is clipped to the shed unit by unit in the engine
        # (`_commit_unit`) and the simulator (`market._inventory_orders`).
        sf_units = xp.sum((bank_mask & has_coll).astype(i32), dtype=i32).astype(i32)
        sf_units = xp.minimum(sf_units, spec.SHED_CAPACITY).astype(i32)
        sf_row = (xp.arange(n_lots(), dtype=i32) == n_lots() - 1).astype(i32)
        sf_is_f = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_FERT).astype(i32)
        lots = (lots + sf_row[:, None] * sf_is_f[None, :] * sf_units).astype(i32)

    if BANK_BEFORE_LOT_ON:
        # [BANK_BEFORE_LOT] The second half, and the half without which the
        # first banks nothing: `avail` above is the hour-0 shed and the greedy
        # ran once at dawn, so lot 2's row was sized before the excursion's
        # DROP and would sell the dawn shed and leave the banked units
        # standing. Add them to that row in bulk, exactly as the DROP branch
        # adds its return leg's `gain` to lot 3's and for the same reason --
        # over-asking is free (every SELL is clipped to the shed unit by unit
        # in the engine's `_commit_unit` and the simulator's
        # `market._inventory_orders`), and a second allocator pass over a
        # projected shed costs more throughput than the curve it recovers.
        bl_w = xp.sum((d.chain_op == O.OP_WATER).astype(i32), axis=1) > 0
        bl_an = xp.asarray(spec.ANIMAL_PRODUCT)[xp.clip(view.occ, 0, spec.N_ANIMALS - 1)]
        bl_p = xp.where(view.kind == spec.KIND_PLANT,
                        xp.clip(view.occ, 0, spec.N_CROPS - 1), bl_an).astype(i32)
        bl_units = xp.where(bank_mask & has_harv,
                            view.t_yield + 2 * bl_w.astype(i32), 0).astype(i32)
        bl_oh = (xp.arange(spec.N_PRODUCTS, dtype=i32)[:, None] == bl_p[None, :]).astype(i32)
        bl_gain = xp.minimum(xp.sum(bl_oh * bl_units[None, :], axis=1, dtype=i32),
                             spec.SHED_CAPACITY).astype(i32)
        _e2s_on_bl = _sw_all(_sw(macro, "ENDROUTE2_SPLIT_ON"),
                             _sw(macro, "ENDROUTE2_ON"),
                             _sw(macro, "ENDROUTE_ON"))
        if _e2s_on_bl is not False:
            # [SWITCH, ENDROUTE2_SPLIT] Not on the terminal day. `DROP_ON`'s
            # `gain` above already offers the whole block's banked yield on the
            # day's LAST lot -- which is the very row this excursion deposits
            # in front of -- so the row is covered; adding it to `BANK_LOT`
            # (turn 10) as well would only pull day 29's dawn shed onto an
            # earlier lot, which is `ENDSELL`'s measured -68.
            # [SWITCH-GENE] An AMOUNT on a row, so the gene rides the vector:
            # gene-OFF leaves `bl_gain` unmasked, the amount it always was.
            bl_gain = _sw_pick(
                xp, _e2s_on_bl,
                lambda: xp.where(terminal, 0, bl_gain).astype(i32),
                bl_gain)
        bank_row = (xp.arange(n_lots(), dtype=i32) == BANK_LOT).astype(i32)
        lots = (lots + bank_row[:, None] * bl_gain[None, :]).astype(i32)

    if ANIMAL_SAME_DAY_ON:                                       # [SWITCH]
        # [ANIMAL_SAME_DAY] The row the day's shear stands on. `avail` above
        # is the HOUR-0 shed, so the fleece a hand takes off a sheep at hour 9
        # is not in the vector the allocator sized the day against, and no lot
        # of today offers it: it sits until `_end_of_day` and sells on
        # tomorrow's opening row. SELL-LOT §3 measured exactly that shape --
        # every wool batch we shear on d6/d9/d12 sells on d7/d10/d13, on every
        # board of both sets, while the tape's sells the same day, across a
        # night in which the quote falls 218 -> 202.
        #
        # Fertilizer has this patch already (`SAME_DAY_FERT_ON`), melon has
        # two (`MELON_OPEN`, `MIDDAY_PLACE_V2`), and `BANK_BEFORE_LOT_ON`'s
        # `bl_gain` above covers whatever the EXCURSION banks -- animal tiles
        # included. This is the same offer widened from `bank_mask` to
        # `covered`: every animal harvest the route actually reaches, on the
        # day's LAST lot, in bulk.
        #
        # Over-asking is free, as everywhere else in this section: every SELL
        # is clipped to the shed unit by unit in the engine (`_commit_unit`)
        # and the simulator (`market._inventory_orders`), so a fleece whose
        # unit has not reached the shed by that turn simply does not sell, and
        # a product with nothing coming keeps its slot empty and both seats'
        # rows compact. `s_qty` is not re-read after this point, so the
        # overflow deficit is the number it already was.
        ad_k = ((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE))
        ad_p = xp.asarray(spec.ANIMAL_PRODUCT)[
            xp.clip(view.occ, 0, spec.N_ANIMALS - 1)].astype(i32)
        ad_units = xp.where(covered & has_harv & ad_k, view.t_yield, 0).astype(i32)
        ad_oh = (xp.arange(spec.N_PRODUCTS, dtype=i32)[:, None] == ad_p[None, :]).astype(i32)
        ad_gain = xp.minimum(xp.sum(ad_oh * ad_units[None, :], axis=1, dtype=i32),
                             spec.SHED_CAPACITY).astype(i32)
        ad_row = (xp.arange(n_lots(), dtype=i32) == n_lots() - 1).astype(i32)
        lots = (lots + ad_row[:, None] * ad_gain[None, :]).astype(i32)

    # ---- shed overflow: the reservations the route never reaches [SWITCH] --
    # What 0.9's pass could not absorb is what end-of-day destroys.
    overflow_left = xp.maximum(deficit - xp.sum(forced, dtype=i32), 0).astype(i32)
    if SHED_OVERFLOW_ON:
        # `avail` above is the hour-0 shed net of the *queued* reservations --
        # one wheat per `want_feed` tile, `n_fert_eff` applications -- while
        # `picks_out` charges only the pickups the reached blocks make (`blk`).
        # Stock reserved for a task the day never walks to is therefore counted
        # as staying in the shed and hidden from the sale at the same time.
        # Offer it: `shed - picked up - sold` is exactly what nothing today
        # consumes, so what the route does reach keeps its reservation.
        used = xp.zeros(spec.N_PRODUCTS, i32)
        for i in range(2):                            # feed wheat, fertilizer
            used = used + ((pid == PICK_ITEM[i]).astype(i32)
                           * xp.sum(blk[i], dtype=i32))
        spare = xp.maximum(view.shed[:spec.N_PRODUCTS].astype(i32) - used - s_qty - forced,
                           0).astype(i32)
        # The same greedy, continued: the first pass drained every product it
        # was allowed to touch, so this one starts where it stopped.
        extra = xp.zeros(spec.N_PRODUCTS, i32)
        for _ in range(spec.N_PRODUCTS):
            key = xp.where(spare > 0, marg * spec.N_PRODUCTS + pid, _DRAINED)
            pick = xp.argmin(key)
            amt = xp.where(spare[pick] > 0, xp.minimum(overflow_left, spare[pick]), 0).astype(i32)
            hit = (pid == pick).astype(i32)
            extra = extra + hit * amt
            spare = spare - hit * spare[pick]
            overflow_left = (overflow_left - amt).astype(i32)
        # Placed in bulk in the same lot the first pass chose, for the same
        # reason [0.9]: a second 100-round allocator pass costs more throughput
        # than the curve it would recover.
        lots = (lots + (lot_ix == forced_lot[None, :]).astype(i32) * extra[None, :]).astype(i32)

    # ---- the hour-23 overflow row [SWITCH, SHED_DUMP_ROW] ----------------
    # Sized from the projection above and from nothing else: `overflow_left` is
    # what `0.9`'s forced sale and `SHED_OVERFLOW_ON`'s continuation together
    # could not absorb, which is exactly the number `eod.drop_inventories` is
    # projected to destroy tonight. Zero on every day the deposit fits, and on
    # the terminal day (`deficit` is gated off there -- day 29 has no eod).
    dump = None
    if SHED_DUMP_ROW_ON:
        # What still STANDS in the shed when the row resolves: the dawn stock,
        # less the pickups the reached blocks actually made (`blk`, the same two
        # kinds `SHED_OVERFLOW_ON` charges -- animals are items the shed holds
        # but no lot sells), less every unit the day has already offered. The
        # day's own BUY row and any mid-day deposit are deliberately NOT added:
        # a SELL is clipped to the shed unit by unit in both the engine
        # (`_commit_unit`) and the simulator (`market._inventory_orders`), so
        # asking short costs a few units of recovery while asking long would
        # offer stock that may not be there when the row resolves.
        dm_used = xp.zeros(spec.N_PRODUCTS, i32)
        for i in range(2):                            # feed wheat, fertilizer
            dm_used = dm_used + ((pid == PICK_ITEM[i]).astype(i32)
                                 * xp.sum(blk[i], dtype=i32))
        dm_stand = xp.maximum(view.shed[:spec.N_PRODUCTS].astype(i32) - dm_used
                              - xp.sum(lots, axis=0).astype(i32), 0).astype(i32)
        # One unit of any product is one unit of room, so the ranking decides
        # only which units are given up -- the same nine static greedy rounds
        # the forced sale runs, over the same projected marginal `marg`.
        dm_rank = (marg * spec.N_PRODUCTS + pid).astype(i32)
        if not SHED_DUMP_ROW_CHEAP_FIRST:
            dm_rank = (-dm_rank).astype(i32)
        dump = xp.zeros(spec.N_PRODUCTS, i32)
        dm_left = overflow_left
        for _ in range(spec.N_PRODUCTS):
            key = xp.where(dm_stand > 0, dm_rank, _DRAINED)
            pick = xp.argmin(key)
            amt = xp.where(dm_stand[pick] > 0,
                           xp.minimum(dm_left, dm_stand[pick]), 0).astype(i32)
            hit = (pid == pick).astype(i32)
            dump = dump + hit * amt
            dm_stand = dm_stand - hit * dm_stand[pick]
            dm_left = (dm_left - amt).astype(i32)

    # ---- the terminal day's last executed row [SWITCH, ENDROUTE] ---------
    # Day 29 only, and a flat ask: everything still standing in the shed when
    # turn `ENDROUTE_TURN` resolves is worth exactly zero a turn later, and an
    # over-ask is clipped unit by unit, so there is no quantity to compute.
    # [SWITCH-GENE] The row is an AMOUNT, so the gene rides on the vector and
    # not on the branch: a gene that asks for the flip zeroes `endrow`, every
    # slot stays `MO_NONE` and the day is the OFF day byte for byte.  The lead's
    # constant still wins outright, and OFF by constant removes the row from
    # `rollout.MARKET_TURNS` too -- which a traced bit could never do.
    endrow = None
    _er_on = _sw(macro, "ENDROUTE_ON")
    if _er_on is not False:
        endrow = _sw_pick(
            xp, _er_on,
            lambda: (xp.ones(spec.N_PRODUCTS, dtype=i32)
                     * xp.asarray(ENDROUTE_ASK, i32)
                     * _as(xp, terminal).astype(i32)).astype(i32),
            xp.zeros(spec.N_PRODUCTS, i32))
    # [SWITCH, ENDROUTE_ROW2] The same vector on an earlier late turn, so the
    # deepest lot of the game is met by two rows instead of one.
    # [SWITCH-GENE] The second row is the same AMOUNT, so it rides the vector
    # exactly as `endrow` does, and its dependency on `ENDROUTE_ON` lives in
    # `_sw_all` and not in a module assert: a draw that takes the first row
    # away zeroes the second, and the ES sees the ENDROUTE-off program rather
    # than an exception.
    endrow2 = None
    _er2_on = _sw_all(_sw(macro, "ENDROUTE_ROW2_ON"), _er_on)
    if _er2_on is not False:
        endrow2 = _sw_pick(
            xp, _er2_on,
            lambda: endrow, xp.zeros(spec.N_PRODUCTS, i32))

    # ---- prestock: tomorrow's inputs, bought tonight [SWITCH] -------------
    if (PRESTOCK_ON or EVE_STOCK_ON or EVENING_SEED_ON
            or (CREW_RELAY_ON and CREW_RELAY_EVE)
            or (PRESTOCK_V2_ON and PRESTOCK_V2_BUY_ON)):
        # [SWITCH, EVE_STOCK] The same row, and only the row: EVE_STOCK adds no
        # schedule half of its own here -- what it buys tonight is read
        # tomorrow by `freefirst`, off tomorrow's own `wheat_buy`.
        pre_wheat, pre_fert, pre_seed = _prestock(
            xp, view, macro, price_table, d, day, terminal, lots,
            blk, covered, has_harv, has_coll, proj_eod)
    else:
        pre_wheat = pre_fert = pre_seed = None

    # ---- the opening pump's size [SWITCH, OPEN_PUMP] ---------------------
    # The day and the purse, and nothing else: `_market` owns the two slots and
    # the `wheat_buy == 0` fact the layout stands on. Zero is "do not fire", so
    # off the switch the argument is `None` and the rows do not move at all.
    # [SWITCH-GENE] The pump is a SIZE, so the gene rides on the vector and not
    # on the branch: `pump_fires` is `n_pump > OPEN_PUMP_KEEP`, so a gene that
    # asks for OFF hands `_market` a zero and every `where` in the hour-0 and
    # sell-back legs takes the branch it took before the switch existed -- the
    # OFF day byte for byte.  Concrete OFF (the shipped default with a zero
    # gene) still passes `None`, so the row is not merely equal but untraced and
    # the three Python-time asserts `_market` owns are not armed at all.
    pump = None
    # PROGFIX1 (4c): the ENGINE's own d0 wheat round trip (buys 15.4 u on
    # d0, sells 11.1 back, keeps the rest as feed) at its own size.
    _op_on = ((PROGRAM_PUMP_UNITS > OPEN_PUMP_KEEP) if PROGRAM_ENGINE_ON
              else _sw(macro, "OPEN_PUMP_ON"))
    _op_units = PROGRAM_PUMP_UNITS if PROGRAM_ENGINE_ON else OPEN_PUMP_UNITS
    if _op_on is not False:
        pump = _sw_pick(
            xp, _op_on,
            lambda: xp.where((day == OPEN_PUMP_DAY)
                             & (_as(xp, view.money) >= OPEN_PUMP_MIN_MONEY),
                             _op_units, 0).astype(i32),
            xp.zeros((), i32))
    # ---- the day's voluntary sale, in per-tick bursts [SWITCH, SPREAD_ROWS]
    # The gated sale leaves the three lots and is cut over `spread_rows_turns()`
    # instead; what stays on the lots is every unit that is NOT the gated sale,
    # on the lot and the turn it always stood on. `s_qty` is untouched, so the
    # shed projection, the forced sale and every bulk add above read the numbers
    # they always read.
    spread = None
    if SPREAD_ROWS_ON:
        spread = spread_alloc(xp, s_qty, view.shops)
        resid = (lots - vol_lots).astype(i32)
        if SPREAD_ROWS_SKIP_LAND_DAYS:
            # A land day keeps the shipped layout, whole: the spread carries
            # nothing and the lots keep every unit they had. A traced `where`
            # and not a Python branch -- `d.buy_land` is a traced int and the
            # turn a row stands on cannot be.
            land = _as(xp, d.buy_land) > 0
            spread = xp.where(land, 0, spread).astype(i32)
            lots = xp.where(land, lots, resid).astype(i32)
        else:
            lots = resid
    # ---- the SELL rows' slot order [SWITCH, SELL_SLOT_PRIORITY] ----------
    # `inv_lots` is the projection the allocator itself priced the lots on, so
    # each row is ranked against the shelf its own turn meets; `view.opp_ripe`
    # is the rival's standing harvest, an empty farm on every view built with
    # the switch off. `None` off, and `_market` emits the rows it always did.
    prio = None
    if SELL_SLOT_PRIORITY_ON:
        if SELL_SLOT_MIRROR_ON:
            # [SWITCH, SELL_SLOT_MIRROR] The exact lockstep replay against a
            # mirror of our own row, in place of the `now - later` ranking. It
            # needs no rival read at all -- the mirror IS our row.
            prio = sell_slot_mirror_scores(xp, price_table, inv_lots, lots)
        else:
            prio = sell_slot_scores(xp, price_table, inv_lots, lots, view.opp_ripe,
                                    view.opp_rate if RIVAL_TELL_ON else None)
        if SELL_SLOT_RIVALRANK_ON:
            # [SWITCH, SELL_SLOT_RIVALRANK] The measured burst's correction to
            # the proxy rank. An all-zero burst -- every view built without the
            # switch, days 0-1, a gap in the stream -- adds exactly zero.
            prio = sell_slot_rivalrank(xp, price_table, inv_lots, lots,
                                       view.opp_burst, prio)
        if SELL_SLOT_MIRROR_GATE_ON:
            # [SWITCH, SELL_SLOT_MIRROR_GATE] A vetoed day keeps the shipped
            # row: all-zero scores are `sell_slot_perm`'s identity.
            prio = xp.where(sell_slot_gate(xp, lots, view.opp_ripe, view.money,
                                           view.opp_money),
                            prio, 0).astype(xp.int32)
    mkt = _market(xp, d.wheat_buy, d.fert_bought, d.seed_buy, d.a_buy,
                  d.buy_land, lots, n_hire_row,
                  pre_wheat=pre_wheat, pre_fert=pre_fert, pre_seed=pre_seed,
                  hire_wide_early=(buy_row_empty if PRESTOCK_ON else None),
                  pack=pack, melon_lots=melon_lots, z_heavy=z_heavy, pump=pump,
                  spread=spread, prio=prio, dump=dump, endrow=endrow,
                  endrow2=endrow2,
                  dodge=(((view.day >= V15_DODGE_DAY0) & (view.day <= V15_DODGE_DAY1))
                         if V15_DODGE_ON else None),
                  drip=(((view.day >= DRIP_SELL_DAY0) & (view.day <= DRIP_SELL_DAY1))
                        if DRIP_SELL_ON else None))

    # ---- section 7's operational metrics ----------------------------------
    # What the forced sale could not absorb is what end-of-day destroys: the
    # sale draws on the hour-0 product stock net of reservations, so a day
    # whose certain inflow overshoots that stock loses the remainder. Read off
    # `deficit` rather than `proj_eod` so the terminal gate applies -- past
    # LAST_SHED_DAY there is no end-of-day left to destroy anything.
    # Value dropped at the labour boundary is every queued tile the day does
    # not actually work -- both the tiles admission never let in and the ones
    # the final route could not reach, which the admit loop's last round
    # leaves standing in `admitted` but absent from `covered`. `~(admitted &
    # covered)` is exactly "not worked today"; `task & ~admitted` alone would
    # miss the route residue this section is most interested in.
    stats = DayStats(
        overflow_destroyed=overflow_left,
        purchase_shortfall=d.purchase_shortfall,
        value_dropped=xp.sum(xp.where(d.task & ~(admitted & covered), d.tile_value, 0),
                             dtype=i32).astype(i32))
    return (unit_op, unit_a, unit_q) + mkt, stats


class TailCare(NamedTuple):
    """What `TAIL_CARE_ON` hands `_routes`: five view-space arrays [100].

    All five are read at the tail and change nothing the admit stage priced.
    `need_feed`/`need_care` are the tiles whose FEED/CARE the day's own route
    does *not* do -- the animal is unfed/uncared this morning and either the
    op is not in its chain or its tile did not survive admission. `fed_anyway`
    is the animal that ends the day fed without the tail's help, which is what
    makes a lone CARE worth a turn. `starving` is `consecutive_unfed >= 1`,
    the animal a lone FEED saves from tonight's escape. `wheat` is the wheat
    each tile hands the unit that works it, which `_routes` cumulates into the
    per-unit carry the tail FEED spends."""
    need_feed: object       # bool[100]
    need_care: object       # bool[100]
    fed_anyway: object      # bool[100]
    starving: object        # bool[100]
    wheat: object           # int[100]


def _ro_block(xp, i32, idx, key, inblk, n_in, tx, ty, tn, sx, sy):
    """[ROUTE_ORDER] One candidate visiting order for a block, and its clock.

    `key` is a static per-rank sort key in [0, N_T): the block's ranks take the
    first `n_in` local positions in key order and every other rank follows in
    its own, which is the layout `harvest_first`'s pairwise count builds by
    hand. `key * N_T + idx` is distinct by construction, so the sort's
    stability does not matter (`_rank`, :4353). Returns the permutation, its
    per-position move and segment costs, its cumulative clock, the block's
    total turns under it and the rank it ends on.
    """
    skey = xp.where(inblk, key * N_T + idx, N_T * N_T + idx).astype(i32)
    rank_at = xp.argsort(skey).astype(i32)
    rtx, rty, rtn = tx[rank_at], ty[rank_at], tn[rank_at]
    prtx = xp.concatenate([rtx[:1], rtx[:-1]])
    prty = xp.concatenate([rty[:1], rty[:-1]])
    base2 = xp.abs(sx - rtx[0]) + xp.abs(sy - rty[0])
    gen2 = (xp.abs(rtx - prtx) + xp.abs(rty - prty)).astype(i32)
    move2 = xp.where(idx == 0, base2, gen2).astype(i32)
    seg2 = (move2 + rtn).astype(i32)
    cum2 = xp.cumsum(seg2).astype(i32)
    return (rank_at, move2, seg2, cum2, _cum_take(xp, cum2, n_in),
            rank_at[xp.clip(n_in - 1, 0, N_T - 1)])


def _routes(xp, chain_op, chain_a, chain_q, n_ops, order, n_tasks, pick_masks, n_units,
            turn_budget, land_lead, drop_day=None, route_early=None,
            route_split=None, wide=None, farmer0=None, freefirst=None, seedfree=None,
            widepick=None, wpfree=None, tail_fill=None, tail_care=None,
            care_fill=None, melon=None, bank=None, harvest_first=None,
            route_order=None, route_cut=None, tile_alloc=None, program_return=None):
    """Split the task sweep across units and expand it into per-turn ops.

    Tiles are visited in `order`, the first `n_tasks` of which carry work;
    whatever the turn budget cannot reach is left undone. A unit's pickup
    turns are charged inside its block [LAW, 0.12]:
    with D(s, e) the number of pickup kinds a block [s, e] consumes, the block
    costs L(e) = base + cum[e] - cum[s] + max(D(s, e), land_lead) turns,
    monotone in e, and ends at the largest e with L(e) <= turn_budget.

    `land_lead` is the turns no unit may work in because the day's quadrant has
    not unlocked yet (M2). It is a *floor* under the pickup turns rather than a
    term added to them: a PICKUP needs the shed, not the land, so a unit that
    owes as many pickups as the lead idles for nothing extra.

    `drop_day` compiles in the DROP return leg (`DROP_ON`, PLANNER_V3_1
    section 4). It is a traced scalar, not a Python flag, because the leg is
    wanted on one day of the season and the day scan is one program: on the
    day it is true every block gains a tail -- the walk back to the nearest
    shed-access tile, then a DROP -- so a block ending at rank e costs
    `L(e) + DIST_SHED(e) + 1`. That tail is **not** monotone in e, so the cut
    cannot use the `_count_le` walk L(e)'s monotonicity buys; it takes the
    largest satisfying rank directly. On a day the tail is zero the two agree
    exactly (`load` is monotone, so "the largest rank that fits" is the last of
    the prefix `_count_le` counts), which is what lets one program serve both.
    `None` compiles none of it and leaves every expression as it always was.

    `route_early` compiles in the per-unit start (`ROUTE_EARLY_ON`). It is a
    traced day-level bool -- "nothing this morning forbids an early step" -- and
    the per-unit half is decided here, where the block is: a block that owes no
    PICKUP and whose first act is a step out of the shed depends on nothing the
    turn-1 BUY row delivers, so it may start at `O.TURN_BUY` and is cut against
    one more turn. The trial cut at `bud + 1` is what decides it, and it is
    exact rather than optimistic: `d_pick` is monotone in the block end, so a
    block that owes no pickup at the *wider* budget owes none at the narrower
    one either. `None` compiles none of it and leaves every cut as it was.

    `route_split` compiles in the same per-unit start under `ROUTE_SPLIT_ON`,
    off a wider reading of what the turn-1 BUY row actually holds up, and
    supersedes `route_early` where both are on. It takes the same trial cut and
    then splits on `wide`, which it needs for that and takes as an argument:
    on a narrow day the extra turn is a *step* and the block has to owe no
    pickup and open with something the row does not feed (a move, or any op but
    PLANT); on a wide day the extra turn is a stationary *PICKUP* at
    `TURN_BUY + 1`, so the block has to owe one and the unit has to be one of
    the turn-0 hires (`u <= MO`) -- a turn-2 hire cannot act at turn 2 at all
    [LAW]. Either way the unit is credited one turn, and the caller shifts its
    start, its budget and, on a wide day, its pickup rows by it.

    `tail_fill` compiles in the tail filler (`TAIL_FILL_ON`): int[100], one
    carry-free op per tile in view space, `O.OP_PASS` where a tile offers none.
    A unit whose block ends before its budget does walks to the nearest tile
    that offers one and takes it, up to `TAIL_HOPS` times. Only ranks at or
    past `n_tasks` are eligible -- no block can reach them, since every block
    ends at `min(jmax, n_tasks - 1)` -- and a tile one unit fills is struck off
    for the units after it. Off on a DROP day, whose tail is the return leg.
    `None` compiles none of it and every tail turn stays `O.OP_PASS`.

    `tail_care` compiles in the care hop (`TAIL_CARE_ON`), a `TailCare` of
    five view-space arrays. A unit whose block ends early walks to the nearest
    animal the day leaves undone and spends up to two turns on it -- FEED, if
    it still carries wheat and the animal is unfed; then CARE, if the animal
    ends the day fed. Unlike the filler it may revisit a tile any block
    already ran, which is where the fed-but-uncared animals live, and
    like the filler a tile one unit takes is struck off for the units after
    it. It runs before the filler, whose turns it therefore has first refusal
    on. Off on a DROP day. `None` compiles none of it.

    `care_fill` compiles in the CARE filler (`CARE_FILL_ON`): a view-space
    bool[100] of the animals the day leaves uncared that a lone CARE actually
    pays on -- uncared this morning, fed tonight, with bank headroom and a fire
    inside the horizon. It runs last on the shared tail cursor and takes up to
    `CARE_FILL_HOPS` hops of walk-plus-CARE, striking each tile off for every
    later unit and for its own later hops, which is the engine's one-CARE-a-day
    cap (`:527`). Off on a DROP day. `None` compiles none of it.

    `melon` compiles in the mid-day excursion (`MELON_OPEN_ON`): a pair
    `(melon_day, mask)` of a traced day-level bool and a view-space bool[100]
    naming the tiles whose harvest has to be banked before the market rather
    than at nightfall. A block that holds one walks to its nearest shed access
    after its **last** such rank, DROPs, walks back and carries on with the
    rest of its block; the day's `turn_budget` does not move, so what the
    excursion costs is `2 * DIST_SHED + 1` turns of that one block. The cut is
    taken twice, the first time to price the reserve: the reserve is the
    dearest return leg among the melon ranks the *full* budget would admit, so
    the recut against `bud - reserve` can only ever land on a cheaper one and
    the excursion always fits the window it was charged for (any slack is
    PASS). Every other block, and every other day, is the program it was.
    `None` compiles none of it. Under `MIDDAY_PLACE_V2_ON` the excursion also
    reports what it banked -- the ranks `[s, m_ins]`, which is the block's
    melon inventory at the deposit -- through the `banked` output below, so
    the caller can put those units in front of the row that sells them.

    `bank` compiles in the same excursion under a time-and-value trigger
    (`BANK_BEFORE_LOT_ON`): a triple `(bank_day, value, route_base)` of a
    traced day-level bool, a view-space int[100] of the coins each tile's
    harvest chain banks at today's quotes, and the turn the crew starts on. The
    excursion goes after the largest rank of the block whose DROP still lands
    on or before that lot's turn, whose running block value has reached
    `BANK_MIN_VALUE`, whose own leg costs at most `BANK_MAX_TURNS` and after
    which nothing in the block still consumes a PICKUP -- OP_DROP dumps the
    whole inventory, so a block that still owes a FEED or a FERTILIZE cannot
    bank in the middle of itself. The reserve is priced at that one rank and
    the recut has to still reach it, or the excursion is not taken at all.
    `None` compiles none of it and `banked` comes back `None`.

    `harvest_first` compiles in the intra-block reorder (`HARVEST_FIRST_ON`):
    a block's tile set `[s, e]` is untouched, but the turn-by-turn *decode*
    visits its HARVEST/COLLECT_FERT ranks first, then everything else, then
    its FEED/FERTILIZE/PLANT ranks last, each group in the order `order`
    already gave it. Priced against a wall: a block takes the new visiting
    order only if its walk-plus-work under it still fits `bud - lead`, the
    same window the tail competes for, so no admitted rank is ever dropped
    to pay for the extra walk and a block that cannot afford the reorder
    keeps the one it had. A block `BANK_BEFORE_LOT_ON`'s excursion actually
    fires on never reorders -- the two mechanisms never touch the same
    unit's turns. `None` compiles none of it and every block decodes exactly
    as it always did.

    Returns (route_op, route_a, route_q, blk, covered, n_pick, lead, early,
    banked):
    per-unit route arrays [MU, TPD], pickup quantities per kind [N_PICK, MU],
    the reached-tile mask in view space, each unit's pickup turns [MU], each
    unit's leading idle turns [MU], 1 [MU] where the unit starts a turn early
    (all zero with `route_early` `None`), and the view-space mask of the tiles
    whose harvest a mid-day excursion banks (`None` unless `bank` is given or
    `MIDDAY_PLACE_V2_ON` / `SAME_DAY_FERT_ON` compiled the melon excursion --
    the latter with the day's COLLECT ranks in it and `I_FERT` at the deposit).
    """
    i32 = xp.int32
    idx = xp.arange(N_T, dtype=i32)

    tx = xp.asarray(SERP_X)[order]
    ty = xp.asarray(SERP_Y)[order]
    if drop_day is not None or program_return is not None:
        near_x = xp.asarray(NEAR_X)[order]
        near_y = xp.asarray(NEAR_Y)[order]
        # Walk back plus the DROP itself, and zero on every other day.
        home = xp.where(False if drop_day is None else drop_day,
                        xp.asarray(DIST_SHED)[order] + 1, 0).astype(i32)
    if program_return is not None:
        pr_mask, pr_base, pr_deadline = program_return[:3]
        pr_batch = program_return[3] if len(program_return) > 3 else N_T
        pr_rank = xp.asarray(pr_mask)[order] & (idx < n_tasks)
        pr_end = xp.sum(pr_rank.astype(i32), dtype=i32)
        pr_banked = xp.zeros(N_T, bool)
    if melon is not None or bank is not None:
        # The excursion's own geometry, shared by both triggers: how far the
        # rank is from a shed access and which access tile that is.
        kdist = xp.asarray(DIST_SHED)[order]
        mnx = xp.asarray(NEAR_X)[order]
        mny = xp.asarray(NEAR_Y)[order]
    if melon is not None:
        mel_day, mel_mask, mel_base = melon
        kmel = xp.asarray(mel_mask)[order]
    # [MIDDAY_PLACE_V2] The excursion's deposit has to be *sold*, and the
    # day's SELL rows were sized at dawn off a shed with no melon in it, so
    # the caller has to be told which ranks the PLACE puts there -- exactly
    # what `BANK_BEFORE_LOT_ON` needs `bank_rank` for, and the same channel.
    # The two never coexist (the `BANK_BEFORE_LOT_ON` assert above), so one
    # `banked` output carries whichever excursion the switches compiled.
    mel_ranked = melon is not None and (MIDDAY_PLACE_V2_ON
                                        or SAME_DAY_FERT_ON)   # [SWITCH]
    if mel_ranked:
        mel_rank = xp.zeros(N_T, bool)
    if bank is not None:
        # [BANK_BEFORE_LOT] The running coin value of what a block has
        # harvested, and the crew's start turn -- the excursion's trigger is
        # the clock and the load, not the crop.
        if len(bank) == 6:                                       # [SWITCH]
            # [ENDROUTE2_SPLIT] Three more traced scalars: the deadline and the
            # two gates, which are the day's own on day 29 and the shipped
            # constants everywhere else.
            # [SWITCH-GENE] Keyed to the tuple the caller packed and not to the
            # module constant: `_plan_and_stats` packs the wide `bank` whenever
            # the gene is live (traced or True) and the narrow one when the
            # switch is concretely OFF, so this stays a Python-time arity read
            # and never a traced branch.
            (bank_day, bank_val, bank_base,
             bank_late, bank_minv, bank_maxt) = bank
        else:
            bank_day, bank_val, bank_base = bank
            bank_late = bank_minv = bank_maxt = None
        kbval = xp.cumsum(xp.asarray(bank_val)[order].astype(i32),
                          dtype=i32).astype(i32)
        bank_rank = xp.zeros(N_T, bool)
    tn = n_ops[order]
    cop, ca, cq = chain_op[order], chain_a[order], chain_q[order]
    if SAME_DAY_FERT_ON:                                         # [SWITCH]
        # [SAME_DAY_FERT] How much the deposit may ask for. Melon needed no
        # such count -- `PLACE MELON 100` can only bank what the block
        # harvested, melon being no PICKUP item -- but a block that picked
        # fertilizer up at the route base to spread it later carries units the
        # shed must not take, and OP_PLACE would hand them over. So the
        # deposit asks for exactly the COLLECT ranks the block has worked
        # since its own first, and `min(qty, inv[I_FERT])` leaves the carried
        # pickup on the unit.
        kcoll = xp.sum((cop == O.OP_COLLECT_FERT).astype(i32), axis=1) > 0
        kccol = xp.cumsum(kcoll.astype(i32), dtype=i32).astype(i32)
    if harvest_first is not None:
        # [HARVEST_FIRST] Every rank's phase, order-indexed and static for
        # the whole day: 2 for a rank whose chain produces (HARVEST or
        # COLLECT_FERT), 0 for one that only consumes (FEED, FERTILIZE or
        # PLANT), 1 for everything else (WATER, CARE, DIG, BUILD, PLACE).
        # Descending phase is the sweep order the per-unit reorder below
        # asks `task_order`'s own pairwise technique for.
        hf_produces = ((xp.sum((cop == O.OP_HARVEST).astype(i32), axis=1) > 0)
                       | (xp.sum((cop == O.OP_COLLECT_FERT).astype(i32), axis=1) > 0))
        hf_consumes = ((xp.sum((cop == O.OP_FEED).astype(i32), axis=1) > 0)
                       | (xp.sum((cop == O.OP_FERTILIZE).astype(i32), axis=1) > 0)
                       | (xp.sum((cop == O.OP_PLANT).astype(i32), axis=1) > 0))
        hf_phase = xp.where(hf_produces, 2, xp.where(hf_consumes, 0, 1)).astype(i32)
        hf_key = (127 - idx).astype(i32)
        hf_dist = xp.asarray(DIST_SHED)[order]
    if route_order is not None:
        # [ROUTE_ORDER] The four boustrophedon keys, order-indexed and static
        # for the whole day: sweep rows (`major_y`) or columns, from either
        # end (`flip`), each line taken in the opposite direction to the one
        # before it. A block's own tiles in key order is the sweep; which of
        # the four is cheapest is decided per block, below, on its own walk.
        ro_keys = []
        for major_y in (True, False):
            for flip in (False, True):
                a = ty if major_y else tx
                b = tx if major_y else ty
                if flip:
                    a = (spec.BOARD - 1) - a
                b2 = xp.where(a % 2 == 0, b, (spec.BOARD - 1) - b)
                ro_keys.append((a * spec.BOARD + b2).astype(i32))
        hf_dist = xp.asarray(DIST_SHED)[order]
    if route_cut is not None:
        # [ROUTE_CUT] The shed gate's own geometry, and the next unit's spawn
        # leg per rank -- both static for the whole day, both order-indexed.
        hf_dist = xp.asarray(DIST_SHED)[order]
    if tile_alloc is not None:
        # [TILE_ALLOC] The day's transfer geometry, order-indexed and static:
        # the shed gate's distance, which ranks may change hands, and what the
        # unit that would have walked a rank saves by not walking it.
        hf_dist = xp.asarray(DIST_SHED)[order]
        # Only a rank that owes no carried input may move: a PICKUP is charged
        # as its own block's lead, so a transfer of a pickup-free rank leaves
        # `d_pick`, `d_lead` and `blk` exactly as the cut computed them.
        ta_free_rank = xp.sum(pick_masks[:, order].astype(i32), axis=0) == 0
        ta_taken = xp.zeros(N_T, bool)
        # Never on a day an excursion can fire: `MELON_OPEN` / `BANK_BEFORE_LOT`
        # price their reserve and their deposit turn off the block's own
        # (contiguous) clock, which a hole would move under them.
        # -- and never on a DROP day: the return leg is the block's own last
        # shed interaction, and a block that works one more tile drops LATER.
        # Every gate this campaign priced says the same thing (ROUTEORDER
        # -1,864 ungated, ROUTECUT -14,987 on the unpriced boundary): where the
        # day ends relative to a shed access is load-bearing, and the ceiling
        # this rule is priced against pins every shed anchor at its own turn
        # (`S/tilealloc/ceiling.py`).  So no shed op ever moves: the PICKUPs
        # are the block's lead and only pickup-free ranks change hands.
        ta_day = xp.asarray(True)
        if drop_day is not None:
            ta_day = ta_day & ~xp.asarray(drop_day)
    if tail_fill is not None:
        cfill = xp.asarray(tail_fill)[order]
        # Tiles no block can hold, struck off as the units take them.
        fill_free = (idx >= n_tasks) & (cfill != O.OP_PASS)
    if tail_care is not None:
        # [TAIL_CARE] The same four masks in route order, plus the running
        # wheat carry a block picks up along its own stripe.
        kneed_f = xp.asarray(tail_care.need_feed)[order]
        kneed_c = xp.asarray(tail_care.need_care)[order]
        kfed = xp.asarray(tail_care.fed_anyway)[order]
        kstarve = xp.asarray(tail_care.starving)[order]
        kwheat = xp.cumsum(xp.asarray(tail_care.wheat)[order].astype(i32)).astype(i32)
        # Struck off as the units take them, exactly like `fill_free`.
        care_free = kneed_f | kneed_c
    if care_fill is not None:
        # [CARE_FILL] The animals a lone CARE pays on, in route order, struck
        # off as the units take them -- and struck by the care hop above too,
        # so no two tails ever land on one tile's single daily CARE.
        cf_free = xp.asarray(care_fill)[order]
    cpick = xp.cumsum(pick_masks[:, order].astype(i32), axis=1)      # [3, 100]

    move = xp.concatenate([xp.zeros(1, i32),
                           xp.abs(tx[1:] - tx[:-1]) + xp.abs(ty[1:] - ty[:-1])]).astype(i32)
    seg = move + tn
    cum = xp.cumsum(seg)
    if tile_alloc is not None:
        # [TILE_ALLOC] What the block that holds rank `j` gives back by not
        # holding it: its own segment, plus the hop out of it, less the
        # shortcut across it -- the triangle inequality makes this >= 0, and it
        # is exact for a hole with both neighbours in the same block, which is
        # every hole the rule takes (the transfer is refused at the boundary
        # rank itself, and the real swept clock is priced below regardless).
        ta_next_x = xp.concatenate([tx[1:], tx[-1:]])
        ta_next_y = xp.concatenate([ty[1:], ty[-1:]])
        ta_prev_x = xp.concatenate([tx[:1], tx[:-1]])
        ta_prev_y = xp.concatenate([ty[:1], ty[:-1]])
        ta_mv_next = xp.concatenate([move[1:], xp.zeros(1, i32)]).astype(i32)
        ta_cross = xp.where(idx == N_T - 1, 0,
                            xp.abs(ta_next_x - ta_prev_x)
                            + xp.abs(ta_next_y - ta_prev_y)).astype(i32)
        ta_skip = xp.maximum(seg + ta_mv_next - ta_cross, 0).astype(i32)
        ta_home = home if drop_day is not None else xp.zeros(N_T, i32)
    prev_x = xp.concatenate([tx[:1], tx[:-1]])
    prev_y = xp.concatenate([ty[:1], ty[:-1]])

    route_op, route_a, route_q, blk, n_pick, n_lead, n_early = [], [], [], [], [], [], []
    start = xp.asarray(0, i32)
    for u in range(MU):
        sx, sy = xp.asarray(SPAWN_X[u], i32), xp.asarray(SPAWN_Y[u], i32)
        bud = xp.where(u < n_units, turn_budget, xp.asarray(0, i32)).astype(i32)

        s = xp.minimum(start, N_T - 1)
        unit_drop = drop_day
        task_limit = n_tasks
        lo = xp.maximum(s - 1, 0)
        prev = xp.where(s > 0, cpick[:, lo], 0)                              # [3] owed before this block
        d_pick = xp.sum((cpick > prev[:, None]).astype(i32), axis=0).astype(i32)   # [100] D(s, e)
        # The block's leading turns: its pickups, or the land lead, whichever
        # is larger. Monotone in e because `d_pick` is, so the `_count_le` walk
        # below stays exact.
        d_lead = xp.maximum(d_pick, land_lead).astype(i32)
        base_move = xp.abs(sx - tx[s]) + xp.abs(sy - ty[s])
        base = base_move + tn[s]
        load = base + cum - cum[s] + d_lead                                   # L(e), sorted in e
        if program_return is not None:
            # A missed delivery deadline must not block the work queue.
            # Service a distant tile normally if its first complete bundle
            # cannot get home in time, and let its load bank overnight.
            pr_budget = xp.minimum(bud, pr_deadline + 1 - pr_base)
            pr_dist = xp.asarray(DIST_SHED)[order]
            pr_unit = (pr_rank[s] & (start < n_tasks)
                       & (load[s] + pr_dist[s] + 1 <= pr_budget))
            unit_drop = xp.asarray(False if drop_day is None else drop_day) | pr_unit
            home = xp.where(unit_drop, pr_dist + 1, 0).astype(i32)
            bud = xp.where(pr_unit, pr_budget, bud).astype(i32)
            task_limit = xp.where(pr_unit, xp.minimum(pr_end, s + pr_batch), n_tasks).astype(i32)
        if route_early is None and route_split is None and farmer0 is None:
            early_u = xp.asarray(0, i32)
        else:
            # [ROUTE_EARLY] Cut the block once against the turn the early start
            # would buy, and keep that turn only if the block it buys still owes
            # no pickup and still walks before it works. `d_pick` is monotone in
            # `e`, so this cannot be wrong in the unsafe direction: a block with
            # no pickup at `bud + 1` has none at `bud`.
            if drop_day is None:
                j1 = _count_le(xp, load, bud + 1) - 1
                fit1 = load[s] <= bud + 1
            else:
                f1 = (idx >= s) & (idx < n_tasks) & (load + home <= bud + 1)
                j1 = xp.max(xp.where(f1, idx, xp.asarray(-1, i32)))
                fit1 = j1 >= s
            e1 = xp.clip(xp.minimum(j1, n_tasks - 1), 0, N_T - 1)
            if route_split is None and route_early is not None:
                early_u = (xp.asarray(route_early) & fit1 & (bud > 0)
                           & (base_move > 0) & (d_pick[e1] == 0)).astype(i32)
            elif route_split is None:
                early_u = xp.asarray(0, i32)
            else:
                # [ROUTE_SPLIT] The same trial cut, read per shape. A narrow
                # day buys a step, so the block must owe the BUY row nothing:
                # no pickup, and either a walk first or an opening op the row
                # does not feed -- PLANT is the only one it does, every other
                # carried input arriving through a PICKUP.
                free_first = (base_move > 0) | (cop[s, 0] != O.OP_PLANT)
                if seedfree is not None:           # [SWITCH, CREW24 H1_WORK]
                    free_first = free_first | seedfree
                narrow_ok = (~wide) & (d_pick[e1] == 0) & free_first
                if freefirst is not None:
                    # [ROUTE_FREEFIRST] The same question per kind. `owed1` is
                    # the trial block's own demand per pickup kind (the value
                    # `blk` takes below), so `free_pick` is "every kind this
                    # block collects has a zero purchase today" -- last night's
                    # shed feeds it and turn 1's market row is irrelevant to
                    # it. A block owing nothing has `owed1` all zero and comes
                    # through unchanged, so this is a widening and never a
                    # narrowing. `free_first` still guards the block that owes
                    # no pickup, whose route op *is* its first turn; a block
                    # that owes one starts its route at `TURN_BUY + d_pick`,
                    # which is `O.ROUTE_BASE` or later, so the seed has
                    # resolved before it plants.
                    owed1 = (cpick[:, e1] - prev).astype(i32)
                    free_pick = xp.sum(((owed1 > 0) & freefirst).astype(i32),
                                       dtype=i32) == 0
                    narrow_ok = ((~wide) & free_pick
                                 & ((d_pick[e1] > 0) | free_first))
                # A wide day buys a stationary PICKUP at `TURN_BUY + 1`, so the
                # block must owe one -- and the unit must be a turn-0 hire, a
                # turn-2 hire's first turn being `O.ROUTE_BASE_WIDE` by law.
                wide_ok = wide & (d_pick[e1] > 0) & bool(u <= MO)
                early_u = (xp.asarray(route_split) & fit1 & (bud > 0)
                           & (narrow_ok | wide_ok)).astype(i32)
                if widepick is not None:
                    # [WIDE_PICK] A SECOND stationary turn for the wide-day
                    # block that owes two or more pickup kinds: kind A at
                    # `O.TURN_BUY`, kind B at `TURN_BUY + 1`, walk at
                    # `O.ROUTE_BASE_WIDE` -- the first turn the spawn law
                    # allows it [LAW, ops.ROUTE_BASE_WIDE]. Both pickups are
                    # stationary, so the turn-2 HIRE row counts the same
                    # occupancy it counts today and every hand lands where
                    # `SPAWN_SLOT` says.
                    #
                    # Cut against `bud + 2`, not `bud + 1`: with two turns the
                    # block `_cut` actually takes is `_cut(bud + 2)` = `e2`,
                    # and the test has to be asked of the block that runs. A
                    # longer block owes a superset of kinds, so asking it at
                    # `e1` could put a kind on turn 1 that `e2` does not own.
                    #
                    # The kind that lands on turn 1 is the block's
                    # lowest-indexed owed kind -- `pk_turn` stamps the rows in
                    # `PICK_ITEM` order -- so it is that kind, and only that
                    # kind, which must be absent from today's BUY row.
                    if drop_day is None:
                        j2 = _count_le(xp, load, bud + 2) - 1
                        fit2 = load[s] <= bud + 2
                    else:
                        f2 = (idx >= s) & (idx < n_tasks) & (load + home <= bud + 2)
                        j2 = xp.max(xp.where(f2, idx, xp.asarray(-1, i32)))
                        fit2 = j2 >= s
                    e2 = xp.clip(xp.minimum(j2, n_tasks - 1), 0, N_T - 1)
                    owed2 = (cpick[:, e2] - prev).astype(i32)
                    seen = xp.asarray(False)
                    first_free = xp.asarray(False)
                    for _k in range(N_PICK):
                        is_first = (owed2[_k] > 0) & (~seen)
                        first_free = first_free | (is_first & (~widepick[_k]))
                        seen = seen | (owed2[_k] > 0)
                    if wpfree is not None:
                        # [SWITCH, WIDE_PICK_FREE] With the rows re-ordered
                        # free-first, the question the grant has to answer is
                        # no longer "is the LOWEST-INDEXED owed kind free" but
                        # "is SOME owed kind free" -- the ordering puts that one
                        # on turn 1. `first_free` implies `any_free`, so this is
                        # a widening and never a narrowing, and an OFF value
                        # leaves the shipped test exactly as it stands.
                        any_free = xp.asarray(False)
                        for _k in range(N_PICK):
                            any_free = any_free | ((owed2[_k] > 0)
                                                   & (~widepick[_k]))
                        first_free = first_free | (any_free & wpfree)
                    wide2 = (wide & bool(u <= MO) & fit1 & fit2 & (bud > 0)
                             & xp.asarray(route_split)
                             & (d_pick[e2] >= 2) & first_free)
                    early_u = xp.maximum(early_u,
                                         2 * wide2.astype(i32)).astype(i32)
            if farmer0 is not None:
                # [PRESTOCK_V2] The farmer's turn, and the farmer's alone. Same
                # trial cut, and the block must OWE a pickup (`d_pick[e1] > 0`)
                # -- the turn it buys is spent standing still on the
                # shed-access tile, which is the only turn-0 op the spawn law
                # allows [LAW, ops.ROUTE_BASE_WIDE]. `route_split`'s narrow
                # branch wants the opposite (`d_pick[e1] == 0`), so the two can
                # never both claim unit 0 and the `maximum` is a union of
                # disjoint sets.
                f0_u = (xp.asarray(farmer0) & fit1 & (bud > 0)
                        & (d_pick[e1] > 0)).astype(i32)
                early_u = xp.maximum(early_u,
                                     f0_u * int(u == 0)).astype(i32)
            bud = (bud + early_u).astype(i32)
        def _cut(b):
            if unit_drop is None:
                jm = _count_le(xp, load, b) - 1
                act = (start < task_limit) & (load[s] <= b) & (b > 0)
                return act, xp.where(act, xp.minimum(jm, task_limit - 1), s - 1)
            # Largest rank whose block *and its return leg* fit. `load` is
            # monotone and `home` is bounded, so the feasible set is a prefix
            # with at most a few holes at its end; taking the largest member is
            # both correct and the most work the budget admits.
            fits = (idx >= s) & (idx < task_limit) & (load + home <= b)
            jm = xp.max(xp.where(fits, idx, xp.asarray(-1, i32)))
            act = (start < task_limit) & (jm >= s) & (b > 0)
            return act, xp.where(act, jm, s - 1)

        active, end = _cut(bud)
        # The block's own clock, needed by the BANK trigger below and by the
        # route decode further down: `cu[j]` is the turn the block finishes
        # rank `j` on, counted from its own first turn.
        cu = base + cum - cum[s]
        ins = xp.asarray(0, i32)
        m_ins = xp.asarray(0, i32)
        dep_q = MIDDAY_PLACE_QTY
        bank_u = xp.asarray(False)
        if melon is not None:
            # [MELON_OPEN] Price the excursion off the full-budget cut, recut
            # against what it leaves, and take it only if the shortened block
            # still holds a melon rank. `res` is the *dearest* leg among the
            # candidates, so the rank the recut actually lands on can only be
            # cheaper and the window is never short.
            in0 = (idx >= s) & (idx <= end) & kmel
            if MIDDAY_PLACE_ON or SAME_DAY_FERT_ON:              # [SWITCH]
                # [MIDDAY_PLACE] The time rule, and the whole of the switch's
                # first half: a melon rank is a candidate only if the deposit
                # that follows it lands on or before the row that sells it.
                # `start_m` is the unit's own first turn, priced off the
                # *full* cut for `BANK_BEFORE_LOT_ON`'s reason -- `d_lead` is
                # monotone in the block end, so the recut's lead can only be
                # smaller and the deposit can only land earlier than the rule
                # admitted, which is the one direction that cannot be wrong.
                # `cu` does not depend on the cut at all.
                start_m = (mel_base + d_lead[xp.maximum(end, 0)] - early_u).astype(i32)
                # [MIDDAY_PLACE_V2] The last melon row rather than the first:
                # a unit acts before its turn's market, so a deposit that
                # lands on the row's own turn still sells on it, and on the
                # real board nothing at all lands by turn 11.
                in_time = (start_m + cu + kdist) <= _midday_place_turn()
                in0 = in0 & in_time
            res = xp.where(xp.asarray(mel_day) & active,
                           xp.max(xp.where(in0, 2 * kdist + 1, 0)), 0).astype(i32)
            act2, end2 = _cut((bud - res).astype(i32))
            in1 = (idx >= s) & (idx <= end2) & kmel
            if MIDDAY_PLACE_ON or SAME_DAY_FERT_ON:              # [SWITCH]
                in1 = in1 & in_time
            take = act2 & (res > 0) & (xp.sum(in1.astype(i32), dtype=i32) > 0)
            m_ins = xp.max(xp.where(in1, idx, xp.asarray(0, i32))).astype(i32)
            active = xp.where(take, act2, active)
            end = xp.where(take, end2, end)
            ins = xp.where(take, res, 0).astype(i32)
            if SAME_DAY_FERT_ON:                                 # [SWITCH]
                # [SAME_DAY_FERT] The COLLECT ranks in `[s, m_ins]`, which is
                # the span the deposit carries in and the span `banked`
                # reports, so the row added below and the quantity asked for
                # are the same units counted twice.
                dep_q = (kccol[m_ins] - kccol[s] + kcoll[s].astype(i32)).astype(i32)
            if mel_ranked:                                       # [SWITCH]
                # [MIDDAY_PLACE_V2] What the deposit carries in: the engine's
                # PLACE banks `min(qty, inv[MELON])`, and the block's melon
                # inventory at `m_ins` is every melon rank it has worked since
                # its first, so the ranks `[s, m_ins]` are the tiles whose
                # units reach the shed in front of the row that sells them.
                mel_rank = mel_rank | (take & (idx >= s) & (idx <= m_ins))
        if bank is not None:
            # [BANK_BEFORE_LOT] The four rules, read off the full-budget cut.
            #
            # `start_b` is the unit's own first turn of the day, which is what
            # the caller lays the route down from (`route_base + lead`, less
            # the early start). It is priced off the full cut deliberately:
            # `d_lead` is monotone in the block end, so the recut's lead can
            # only be smaller and the DROP can only land *earlier* than the
            # rule admitted -- the one direction that cannot be wrong.
            e0 = xp.maximum(end, 0)
            start_b = (bank_base + d_lead[e0] - early_u).astype(i32)
            drop_t = (start_b + cu + kdist).astype(i32)
            val = (kbval - xp.where(s > 0, kbval[lo], 0)).astype(i32)
            # Pickup-consuming tiles still ahead of the rank: the DROP empties
            # the unit's hands, so there must be none.
            after = xp.sum(cpick[:, e0][:, None] - cpick, axis=0, dtype=i32)
            if bank_late is None:
                b_time = drop_t <= O.SELL_TURNS[BANK_LOT]
                b_val = val >= BANK_MIN_VALUE
                b_leg = 2 * kdist + 1 <= BANK_MAX_TURNS
            else:
                # [SWITCH, ENDROUTE2_SPLIT] The same three rules against the
                # day's own numbers.
                b_time = drop_t <= bank_late
                b_val = val >= bank_minv
                b_leg = 2 * kdist + 1 <= bank_maxt
            ok = ((idx >= s) & (idx <= end) & active & xp.asarray(bank_day)
                  & b_time & b_val & b_leg
                  & (after <= 0))
            if program_return is not None:
                ok = ok & ~pr_unit
            jb = xp.max(xp.where(ok, idx, xp.asarray(-1, i32)))
            jbc = xp.maximum(jb, 0)
            # Priced at the chosen rank alone, and taken only if the recut
            # still reaches it -- the window is then exactly what was charged.
            res_b = xp.where(jb >= 0, 2 * kdist[jbc] + 1, 0).astype(i32)
            act_b, end_b = _cut((bud - res_b).astype(i32))
            bank_u = (jb >= 0) & act_b & (end_b >= jb)
            active = xp.where(bank_u, act_b, active)
            end = xp.where(bank_u, end_b, end)
            ins = xp.where(bank_u, res_b, ins).astype(i32)
            m_ins = xp.where(bank_u, jbc, m_ins).astype(i32)
            bank_rank = bank_rank | (bank_u & (idx >= s) & (idx <= jbc))
        if route_order is not None:
            # [ROUTE_ORDER] Pass 1 -- the cheapest boustrophedon sweep of the
            # block the cut just took, refused unless it is strictly shorter
            # than the rank order it replaces, fits the turns the block
            # already had, and ends no farther from a shed access.
            free_r = active & (ins == 0)
            e_r = xp.maximum(end, 0)

            def _ro_best(e_b, win, cue):
                """Cheapest of the four sweeps of `[s, e_b]`, or none."""
                inb = (idx >= s) & (idx <= e_b) & free_r
                nb = xp.sum(inb.astype(i32), dtype=i32).astype(i32)
                tot_b = xp.asarray(_BIG, i32)
                ok_b = xp.asarray(False)
                ra_b, mv_b, sg_b, cm_b, ef_b = idx, move, seg, cum, e_b
                for key in ro_keys:
                    ra, mv, sg, cm, tot, ef = _ro_block(
                        xp, i32, idx, key, inb, nb, tx, ty, tn, sx, sy)
                    ok = (free_r & (nb > 0) & (tot < cue) & (tot <= win)
                          & ((hf_dist[ef] <= hf_dist[e_b])
                             if ROUTE_ORDER_SHED_GATE else True))
                    better = ok & (tot < tot_b)
                    tot_b = xp.where(better, tot, tot_b).astype(i32)
                    ra_b = xp.where(better, ra, ra_b).astype(i32)
                    mv_b = xp.where(better, mv, mv_b).astype(i32)
                    sg_b = xp.where(better, sg, sg_b).astype(i32)
                    cm_b = xp.where(better, cm, cm_b).astype(i32)
                    ef_b = xp.where(better, ef, ef_b).astype(i32)
                    ok_b = ok_b | better
                return ok_b, tot_b, ra_b, mv_b, sg_b, cm_b, ef_b, nb

            ok1, tot1, ra1, mv1, sg1, cm1, ef1, n1 = _ro_best(
                e_r, (bud - d_lead[e_r]).astype(i32), cu[e_r])
            # Pass 2 -- spend the saving. The recut is taken against the day's
            # own (unreordered) `load`, so it may be optimistic; the sweep of
            # the wider block is then priced against the REAL window
            # (`total <= bud - lead`) and the extension is taken only if it
            # fits, so no admitted rank is ever one the route cannot reach.
            sav = xp.where(ok1, cu[e_r] - tot1, 0).astype(i32)
            act_r, end_r = _cut((bud + sav).astype(i32))
            e_r2 = xp.maximum(end_r, 0)
            ok2, tot2, ra2, mv2, sg2, cm2, ef2, n2 = _ro_best(
                e_r2, (bud - d_lead[e_r2]).astype(i32), xp.asarray(_BIG, i32))
            take2 = ok1 & ok2 & act_r & (end_r > end) & (sav > 0)
            end = xp.where(take2, end_r, end).astype(i32)
            ro_use = take2 | ok1
            ro_tot = xp.where(take2, tot2, tot1).astype(i32)
            ro_rank = xp.where(take2, ra2, ra1).astype(i32)
            ro_move = xp.where(take2, mv2, mv1).astype(i32)
            ro_seg = xp.where(take2, sg2, sg1).astype(i32)
            ro_cum = xp.where(take2, cm2, cm1).astype(i32)
            ro_ef = xp.where(take2, ef2, ef1).astype(i32)
            ro_n = xp.where(take2, n2, n1).astype(i32)
        if route_cut is not None:
            # [ROUTE_CUT] Pull the boundary back to the cheapest entry for the
            # NEXT unit. `cost(c + 1)` is exactly the term the assignment owns
            # (the constants block above): the leg unit u+1 walks from its own
            # spawn to the rank it starts on, less the hop into that rank that
            # nobody then walks. Ties keep today's cut, and the gates are the
            # block's own: no excursion on it, a successor to hand the ranks
            # to, and a new end no farther from a shed access (`hf_dist`) than
            # today's -- with `c <= end` and `cu` monotone, the DROP leg and
            # every deposit therefore land on the same turn or sooner.
            nsx = xp.asarray(SPAWN_X[min(u + 1, MU - 1)], i32)
            nsy = xp.asarray(SPAWN_Y[min(u + 1, MU - 1)], i32)
            cost = (xp.abs(nsx - tx) + xp.abs(nsy - ty) - move).astype(i32)
            e_c = xp.maximum(end, 0)
            free_c = (active & (ins == 0) & (end > s) & (n_units > u + 1)
                      & (end + 1 < n_tasks))
            cost0 = cost[xp.minimum(e_c + 1, N_T - 1)]
            cut_e = e_c
            cut_g = xp.asarray(0, i32)
            for k in range(1, ROUTE_CUT_LOOK + 1):
                c = xp.maximum(e_c - k, s)
                # The ranks given up are worked by the next unit, but the turns
                # THIS block frees are dead -- the greedy cut had nothing else
                # to spend them on -- so the whole chain ends `cu[e] - cu[c]`
                # turns earlier. The recut is taken only where the entry it
                # buys is worth strictly more than that, which is why it fires
                # on a long serpentine hop and nowhere else.
                gain = (cost0 - cost[c + 1] - (cu[e_c] - cu[c])).astype(i32)
                ok = (free_c & (c < e_c) & (gain > cut_g)
                      & ((hf_dist[c] <= hf_dist[e_c])
                         if ROUTE_CUT_SHED_GATE else True))
                cut_e = xp.where(ok, c, cut_e).astype(i32)
                cut_g = xp.where(ok, gain, cut_g).astype(i32)
            end = xp.where(free_c & (cut_g > 0), cut_e, end).astype(i32)
        ta_use = xp.asarray(False)
        if tile_alloc is not None:
            # [TILE_ALLOC] The block this unit really works: the cut's prefix
            # less the ranks an earlier unit stole out of it, plus the ranks
            # this one steals out of the block ahead.  Both are decoded by
            # `_ro_block`'s mask with a RANK key, so the tiles stay in `order`
            # and only the SET changes.
            def _ta_eval(e_b, mine, soft=False):
                """The real swept clock of `[s, e_b] - taken + mine`."""
                inb = ((((idx >= s) & (idx <= e_b) & ~ta_taken) | mine)
                       & active & (idx < n_tasks))
                nb = xp.sum(inb.astype(i32), dtype=i32).astype(i32)
                ra, mv, sg, cm, tot, ef = _ro_block(
                    xp, i32, idx, idx, inb, nb, tx, ty, tn, sx, sy)
                fit = (nb > 0) & (tot + ta_home[ef] <= bud - d_lead[e_b])
                if TILE_ALLOC_SHED_GATE:                         # [SWITCH]
                    fit = fit & (hf_dist[ef] <= hf_dist[e_b])
                return fit, tot, ra, mv, sg, cm, ef, nb

            e_t = xp.maximum(end, 0)
            inh = (idx >= s) & (idx <= e_t) & ta_taken
            # Pass 1 -- spend what the holes freed, exactly as `ROUTE_ORDER_ON`
            # spends the saving of its sweep: recut against the day's own
            # `load` (an over-estimate for a block with a hole in it, so the
            # recut is never optimistic about the ranks it admits) and take the
            # wider block only if its REAL swept total still fits the window.
            sav_h = xp.sum(xp.where(inh, ta_skip, 0), dtype=i32).astype(i32)
            act_h, end_h = _cut((bud + sav_h).astype(i32))
            zero_m = xp.zeros(N_T, bool)
            f_b, t_b, ra_b, mv_b, sg_b, cm_b, ef_b, nb_b = _ta_eval(e_t, zero_m)
            e_h = xp.maximum(end_h, 0)
            f_h, t_h, ra_h, mv_h, sg_h, cm_h, ef_h, nb_h = _ta_eval(e_h, zero_m)
            take_h = act_h & (end_h > end) & (sav_h > 0) & f_h & (ins == 0)
            end = xp.where(take_h, end_h, end).astype(i32)
            cur_e = xp.maximum(end, 0)
            ta_fit = xp.where(take_h, f_h, f_b)
            ta_tot = xp.where(take_h, t_h, t_b).astype(i32)
            ta_rank = xp.where(take_h, ra_h, ra_b).astype(i32)
            ta_move = xp.where(take_h, mv_h, mv_b).astype(i32)
            ta_seg = xp.where(take_h, sg_h, sg_b).astype(i32)
            ta_cum = xp.where(take_h, cm_h, cm_b).astype(i32)
            ta_ef = xp.where(take_h, ef_h, ef_b).astype(i32)
            ta_n = xp.where(take_h, nb_h, nb_b).astype(i32)
            # Pass 2 -- the steal.  A pickup-free rank ahead of this block,
            # never the boundary rank itself and never next to a hole (so the
            # shortcut `ta_skip` prices is the one the loser really walks),
            # appended to this block's walk out of the turns the greedy cut
            # had nothing left to spend, and only where the loser gives back
            # strictly more turns than the appendix costs.
            mine = zero_m
            free_t = (active & (ins == 0) & ta_day & ta_fit
                      & (n_units > u + 1) & (end + 1 < n_tasks))
            # An excursion block neither steals nor spends: its reserve and its
            # deposit turn are priced off the block's own clock, and the recut
            # below would hand the reserve back.  It may still INHERIT a hole
            # (a hole only ever shortens the clock, so the deposit the rule
            # admitted can only land sooner -- the one direction that cannot be
            # wrong), and the deposit's turn is read off the real clock below.

            nb_taken = ((xp.concatenate([ta_taken[1:], ta_taken[-1:]]))
                        | (xp.concatenate([ta_taken[:1], ta_taken[:-1]])))
            for _ in range(TILE_ALLOC_PASSES):
                cx, cy = tx[ta_ef], ty[ta_ef]
                ta_cost = (xp.abs(tx - cx) + xp.abs(ty - cy) + tn).astype(i32)
                ok = (free_t & (idx > cur_e + 1) & (idx < n_tasks)
                      & (idx <= cur_e + TILE_ALLOC_LOOK)
                      & ta_free_rank & ~ta_taken & ~nb_taken & ~mine
                      & (ta_skip > ta_cost)
                      & (ta_tot + ta_cost + ta_home <= bud - d_lead[cur_e]))
                if TILE_ALLOC_SHED_GATE:                         # [SWITCH]
                    ok = ok & (hf_dist <= hf_dist[cur_e])
                # Dearest transfer first, ties to the lower rank -- the same
                # (key, index) argmin the tail filler's hops use.
                ta_key = xp.where(ok, (ta_cost - ta_skip) * N_T + idx,
                                  xp.asarray(_BIG, i32)).astype(i32)
                bj = xp.argmin(ta_key).astype(i32)
                hit = ok[bj]
                mine2 = mine | (hit & (idx == bj))
                f2, t2, ra2, mv2, sg2, cm2, ef2, n2 = _ta_eval(cur_e, mine2)
                hit = hit & f2
                mine = xp.where(hit, mine2, mine)
                ta_tot = xp.where(hit, t2, ta_tot).astype(i32)
                ta_rank = xp.where(hit, ra2, ta_rank).astype(i32)
                ta_move = xp.where(hit, mv2, ta_move).astype(i32)
                ta_seg = xp.where(hit, sg2, ta_seg).astype(i32)
                ta_cum = xp.where(hit, cm2, ta_cum).astype(i32)
                ta_ef = xp.where(hit, ef2, ta_ef).astype(i32)
                ta_n = xp.where(hit, n2, ta_n).astype(i32)
                nb_taken = nb_taken | (xp.concatenate([mine[1:], mine[-1:]])
                                       | xp.concatenate([mine[:1], mine[:-1]]))
            # A block that INHERITED a hole has no choice: decoding it against
            # the contiguous clock would walk it into a tile another unit has
            # already worked, so the mask decode is used even where the gate
            # would have refused it (`must`).  A hole only ever shortens the
            # walk, so the window it had is still met; what the gate is
            # refusing there is the block's last tile, not its turns.
            must = xp.sum(inh.astype(i32), dtype=i32) > 0
            # Nothing to decode differently unless the block really changed:
            # a unit that neither stole, inherited a hole nor spent one keeps
            # the contiguous decode it always had.
            changed = (take_h | must
                       | (xp.sum(mine.astype(i32), dtype=i32) > 0))
            ta_use = active & (ta_n > 0) & changed & (ta_fit | must)
            ta_taken = (ta_taken | (mine & ta_use))
        e = xp.maximum(end, 0)
        p_u = xp.where(active, d_pick[e], 0).astype(i32)
        l_u = xp.where(active, d_lead[e], 0).astype(i32)

        use_reorder = xp.asarray(False)
        e_final = e
        block_end = cu[e]
        if tile_alloc is not None:
            # [TILE_ALLOC] The same five arrays `harvest_first` hands the
            # decode, over the block the transfer pass settled on.
            use_reorder = ta_use
            n_in, rank_at = ta_n, ta_rank
            move2, seg2, cum2 = ta_move, ta_seg, ta_cum
            e_final = xp.where(ta_use, ta_ef, e).astype(i32)
            block_end = xp.where(ta_use, ta_tot, cu[e]).astype(i32)
        if route_order is not None:
            # [ROUTE_ORDER] The block the passes above settled on, and the
            # sweep it is worked under -- the same five arrays `harvest_first`
            # hands the decode below.
            use_reorder = ro_use
            n_in, rank_at = ro_n, ro_rank
            move2, seg2, cum2 = ro_move, ro_seg, ro_cum
            e_final = xp.where(ro_use, ro_ef, e).astype(i32)
            block_end = xp.where(ro_use, ro_tot, cu[e]).astype(i32)
        if harvest_first is not None:
            # [HARVEST_FIRST] The tile set is `[s, e]`, untouched by any of
            # this; only the local visiting order is a candidate for reorder,
            # and only where an excursion has not already claimed the
            # block's turns (`ins == 0` -- `MELON_OPEN`/`BANK_BEFORE_LOT`
            # both route through `ins`, so this reads either).
            inblk = (idx >= s) & (idx <= e) & active
            n_in = xp.sum(inblk.astype(i32), dtype=i32).astype(i32)
            ahead_in = (((hf_phase[None, :] > hf_phase[:, None])
                        | ((hf_phase[None, :] == hf_phase[:, None])
                           & (hf_key[None, :] > hf_key[:, None])))
                       & inblk[None, :])
            pos_in = xp.sum(ahead_in.astype(i32), axis=1).astype(i32)
            pos_out = (xp.cumsum(1 - inblk.astype(i32)) - (1 - inblk.astype(i32))
                      + n_in).astype(i32)
            pos_of = xp.where(inblk, pos_in, pos_out).astype(i32)
            if hasattr(idx, "at"):
                rank_at = xp.zeros(N_T, i32).at[pos_of].set(idx)
            else:
                rank_at = np.zeros(N_T, np.int32)
                rank_at[np.asarray(pos_of)] = np.asarray(idx)
            rtx, rty, rtn = tx[rank_at], ty[rank_at], tn[rank_at]
            prtx = xp.concatenate([rtx[:1], rtx[:-1]])
            prty = xp.concatenate([rty[:1], rty[:-1]])
            base_move2 = xp.abs(sx - rtx[0]) + xp.abs(sy - rty[0])
            move2_gen = (xp.abs(rtx - prtx) + xp.abs(rty - prty)).astype(i32)
            move2 = xp.where(idx == 0, base_move2, move2_gen).astype(i32)
            seg2 = (move2 + rtn).astype(i32)
            cum2 = xp.cumsum(seg2).astype(i32)
            total2 = _cum_take(xp, cum2, n_in)
            e_final_cand = rank_at[xp.clip(n_in - 1, 0, N_T - 1)]
            # Only if the reorder's own walk still fits the turns the block
            # already had -- no admitted rank is ever dropped to pay for it
            # -- and only if it does not leave the block's tail cursor (and
            # any drop-day return leg) farther from a shed access than the
            # unreordered ending would have: `task_order`'s index tiebreak
            # already keeps a block's *last* rank close to the shed, and the
            # 899009257 census below found the naive reorder giving that up
            # on 36% of the blocks it touches, +0.41 tiles on average --
            # enough on its own to erase the reorder's benefit (measured).
            use_reorder = (active & (n_in > 0) & (ins == 0)
                          & (total2 <= bud - l_u)
                          & (hf_dist[e_final_cand] <= hf_dist[e]))
            e_final = xp.where(use_reorder, e_final_cand, e)
            block_end = xp.where(use_reorder, total2, cu[e])
            if HF_TRACE is not None and bool(np.asarray(active)):
                HF_TRACE.append(dict(
                    n_in=int(np.asarray(n_in)),
                    used=bool(np.asarray(use_reorder)),
                    total2=int(np.asarray(total2)),
                    orig_total=int(np.asarray(cu[e])),
                    window=int(np.asarray(bud - l_u)),
                    e=int(np.asarray(e)), e_final=int(np.asarray(e_final)),
                    dist_shed_e=int(np.asarray(xp.asarray(DIST_SHED)[order])[int(np.asarray(e))]),
                    dist_shed_ef=int(np.asarray(xp.asarray(DIST_SHED)[order])[int(np.asarray(e_final))])))

        cu_prev = cu - xp.where(idx == s, base, seg)
        cu_masked = xp.where(idx < s, xp.asarray(-1, i32),
                             xp.where(idx <= end, cu, _BIG)).astype(i32)

        r = xp.arange(TPD, dtype=i32)
        if melon is None and bank is None:
            rr, t_ins = r, None
        else:
            # [MELON_OPEN] The block's own clock, paused for the excursion: the
            # turns before it map to ranks as they always did, the `ins` turns
            # of the excursion map to nothing, and every turn after it is the
            # rank the block would have been on `ins` turns earlier.
            cu_ins = cu[m_ins]
            if tile_alloc is not None:
                # [TILE_ALLOC] The block's own clock is `cum2` when a transfer
                # changed the set: the deposit fires after the local POSITION
                # of rank `m_ins`, which is how many of the block's ranks are
                # below it.
                pos_ins = xp.sum(((ta_rank < m_ins) & (idx < ta_n)).astype(i32),
                                 dtype=i32).astype(i32)
                cu_ins = xp.where(ta_use, ta_cum[xp.clip(pos_ins, 0, N_T - 1)],
                                  cu_ins).astype(i32)
            t_ins = xp.where(ins > 0, cu_ins, xp.asarray(_BIG, i32)).astype(i32)
            rr = (r - xp.where(r >= t_ins, ins, 0)).astype(i32)
        j0 = xp.clip(_count_le(xp, cu_masked, rr), 0, N_T - 1)
        within0 = rr - cu_prev[j0]
        mv0 = xp.where(j0 == s, base_move, move[j0])
        px0 = xp.where(j0 == s, sx, prev_x[j0])
        py0 = xp.where(j0 == s, sy, prev_y[j0])
        if harvest_first is None and route_order is None and tile_alloc is None:
            j, within, mv, px, py = j0, within0, mv0, px0, py0
        else:
            # [HARVEST_FIRST] The same decode, against the reordered block's
            # own local clock `cum2` instead of the day's `cu` -- `p1` is the
            # local position `rr` falls in, `rank_at[p1]` the tile it names.
            cu2_masked = xp.where(idx < n_in, cum2, xp.asarray(_BIG, i32))
            p1 = xp.clip(_count_le(xp, cu2_masked, rr), 0, N_T - 1)
            j1 = rank_at[p1]
            cu2_prev = cum2 - seg2
            within1 = rr - cu2_prev[p1]
            mv1 = move2[p1]
            prev_p1 = rank_at[xp.maximum(p1 - 1, 0)]
            px1 = xp.where(p1 == 0, sx, tx[prev_p1])
            py1 = xp.where(p1 == 0, sy, ty[prev_p1])
            j = xp.where(use_reorder, j1, j0)
            within = xp.where(use_reorder, within1, within0)
            mv = xp.where(use_reorder, mv1, mv0)
            px = xp.where(use_reorder, px1, px0)
            py = xp.where(use_reorder, py1, py0)
        dx, dy = tx[j] - px, ty[j] - py
        step_op = xp.where(within < xp.abs(dx),
                           xp.where(dx > 0, O.OP_EAST, O.OP_WEST),
                           xp.where(dy > 0, O.OP_SOUTH, O.OP_NORTH)).astype(i32)
        k = xp.clip(within - mv, 0, CHAIN_MAX - 1)

        working = active & (rr < block_end) & (rr < bud - l_u)
        is_step = within < mv
        u_op = xp.where(working, xp.where(is_step, step_op, cop[j, k]), O.OP_PASS).astype(i32)
        u_a = xp.where(working & ~is_step, ca[j, k], 0).astype(i32)
        u_q = xp.where(working & ~is_step, cq[j, k], 0).astype(i32)

        if tail_fill is not None or tail_care is not None or care_fill is not None:
            # [TAIL] The turns between `cu[e]` and the end of the unit's
            # window, which `working` leaves as PASS: the unit stands on its
            # block's last tile with `f_left` turns of day left. Both tail
            # switches walk this one cursor forward, `TAIL_CARE_ON` first --
            # a banked care bonus is worth more than any op the filler offers.
            fx0, fy0 = tx[e_final], ty[e_final]
            # The excursion's turns are real turns of the day, so the tail's
            # cursor starts behind them (`ins` is 0 on every other day).
            f_t0 = (xp.where(active, block_end, 0) + ins).astype(i32)
            f_left = (bud - l_u - f_t0).astype(i32)
            f_can = active & (bud > 0)
            if unit_drop is not None:
                f_can = f_can & ~unit_drop

        if tail_care is not None:
            # [TAIL_CARE] The nearest animal the day leaves undone, and up to
            # two turns on it: FEED while the unit still carries wheat, then
            # CARE if the animal ends the day fed. A lone CARE is taken only
            # where the animal is fed anyway (it banks nothing otherwise,
            # `:829`) and a lone FEED only where the animal escapes tonight
            # without it (`:817`) -- production fires unfed, so a feed that
            # buys neither survival nor a care buys no units at all.
            #
            # `carry` is the block's own wheat harvest: the feed pickup nets
            # to zero against the FEEDs the block spends it on, so what is
            # left in the unit's hands at the tail is what it picked up off
            # its wheat tiles.
            carry_base = xp.where(s > 0, kwheat[lo], 0).astype(i32)
            if bank is not None:
                # [BANK_BEFORE_LOT] The excursion dumped everything the block
                # was holding, so the tail's carry starts again at the drop.
                carry_base = xp.where(bank_u, kwheat[m_ins], carry_base).astype(i32)
            carry = xp.where(active, kwheat[e] - carry_base, 0).astype(i32)
            for _ in range(TAIL_CARE_HOPS):
                w_ok = carry > 0
                do_f = kneed_f & w_ok
                do_c = kneed_c & (kfed | do_f)
                n_here = (do_f.astype(i32) + do_c.astype(i32)).astype(i32)
                # Every rank is eligible, which is the whole of the filler's
                # "tiles no block holds" rule relaxed away: the fed-but-uncared
                # animal is the block's own feed whose care `care_pays`
                # refused, and re-running its tile is exactly what pays. The
                # rule the filler needs it for does not bind here -- `kneed_f`
                # and `kneed_c` already strike every tile the day's own route
                # feeds or cares, so no tail turn can land on an op the engine
                # would no-op, whichever unit's block owns the rank; and
                # `care_free` keeps two tails off one tile. Order does not
                # bind either: FEED and CARE are day flags read once at eod
                # (`:829`), so a tail visit can never race the block.
                c_d = (xp.abs(tx - fx0) + xp.abs(ty - fy0)).astype(i32)
                c_ok = (care_free & (do_c | (do_f & kstarve))
                        & (c_d + n_here <= f_left))
                c_key = xp.where(c_ok, c_d * N_T + idx, _BIG).astype(i32)
                b = xp.argmin(c_key).astype(i32)
                hit = f_can & (c_key[b] < _BIG)
                nb = n_here[b]
                bx, by = tx[b], ty[b]
                bdx, bdy = bx - fx0, by - fy0
                bwalk = xp.abs(bdx) + xp.abs(bdy)
                w2 = r - f_t0
                care_step = xp.where(w2 < xp.abs(bdx),
                                     xp.where(bdx > 0, O.OP_EAST, O.OP_WEST),
                                     xp.where(bdy > 0, O.OP_SOUTH, O.OP_NORTH)).astype(i32)
                in_care = hit & (w2 >= 0) & (w2 < bwalk)
                at_one = hit & (w2 == bwalk)
                at_two = hit & (w2 == bwalk + 1) & (nb == 2)
                op_one = xp.where(do_f[b], O.OP_FEED, O.OP_CARE).astype(i32)
                u_op = xp.where(in_care, care_step,
                                xp.where(at_one, op_one,
                                         xp.where(at_two, O.OP_CARE, u_op))).astype(i32)
                u_a = xp.where(in_care | at_one | at_two,
                               (ROUTE_VRP_OPT_MARK + 1) if ROUTE_VRP_OPT_ON else 0,
                               u_a).astype(i32)
                if ROUTE_VRP_OPT_ON:
                    u_a = xp.where(in_care, 0, u_a).astype(i32)
                u_q = xp.where(in_care | at_one | at_two, 0, u_q).astype(i32)
                # Struck off for every later unit, and for this unit's next hop.
                care_free = care_free & ~(hit & (idx == b))
                if care_fill is not None:
                    # [CARE_FILL] and off the fill hops' own list: this visit
                    # either cared the tile (a second CARE is an engine no-op,
                    # `:527`) or spent a lone survival FEED on it, and taking
                    # the second reading conservatively costs at most the one
                    # care a starving animal's tile would have paid.
                    cf_free = cf_free & ~(hit & (idx == b))
                carry = (carry - xp.where(hit & do_f[b], 1, 0)).astype(i32)
                fx0 = xp.where(hit, bx, fx0).astype(i32)
                fy0 = xp.where(hit, by, fy0).astype(i32)
                f_t0 = xp.where(hit, f_t0 + bwalk + nb, f_t0).astype(i32)
                f_left = xp.where(hit, f_left - bwalk - nb, f_left).astype(i32)

        if tail_fill is not None:
            # [TAIL_FILL] The turns the care hop left, if any: each hop walks
            # to the nearest tile that offers a carry-free op and takes it,
            # which costs the walk plus one. Ties on distance go to the lower
            # rank, i.e. to the serpentine order the day already sweeps in.
            for _ in range(tail_hops()):
                f_d = (xp.abs(tx - fx0) + xp.abs(ty - fy0)).astype(i32)
                f_ok = fill_free & (f_d + 1 <= f_left)
                # `_BIG` is far above any (distance, rank) key: the board is 10
                # wide, so the key tops out at 18 * N_T + 99.
                f_key = xp.where(f_ok, f_d * N_T + idx, _BIG).astype(i32)
                b = xp.argmin(f_key).astype(i32)
                hit = f_can & (f_key[b] < _BIG)
                bx, by = tx[b], ty[b]
                bdx, bdy = bx - fx0, by - fy0
                bwalk = xp.abs(bdx) + xp.abs(bdy)
                w2 = r - f_t0
                fill_step = xp.where(w2 < xp.abs(bdx),
                                     xp.where(bdx > 0, O.OP_EAST, O.OP_WEST),
                                     xp.where(bdy > 0, O.OP_SOUTH, O.OP_NORTH)).astype(i32)
                in_fill = hit & (w2 >= 0) & (w2 < bwalk)
                at_fill = hit & (w2 == bwalk)
                u_op = xp.where(in_fill, fill_step,
                                xp.where(at_fill, cfill[b], u_op)).astype(i32)
                u_a = xp.where(in_fill, 0, xp.where(
                    at_fill, (ROUTE_VRP_OPT_MARK + 2) if ROUTE_VRP_OPT_ON else 0, u_a)).astype(i32)
                u_q = xp.where(in_fill | at_fill, 0, u_q).astype(i32)
                # Struck off for every later unit, and for this unit's next hop.
                fill_free = fill_free & ~(hit & (idx == b))
                fx0 = xp.where(hit, bx, fx0).astype(i32)
                fy0 = xp.where(hit, by, fy0).astype(i32)
                f_t0 = xp.where(hit, f_t0 + bwalk + 1, f_t0).astype(i32)
                f_left = xp.where(hit, f_left - bwalk - 1, f_left).astype(i32)

        if care_fill is not None:
            # [CARE_FILL] Whatever tail the two switches above left: each hop
            # walks to the nearest animal a lone CARE still pays on and spends
            # one turn on it, which is the walk plus one. Ties on distance go
            # to the lower rank, i.e. to the serpentine order the day already
            # sweeps in, exactly as the filler's do.
            #
            # Every gate the engine imposes is already in `cf_free`
            # (`_plan_and_stats`): uncared today, fed tonight, bank headroom,
            # and a fire inside the horizon. What is left here is the clock --
            # the visit has to fit the turns the tail still has -- and the
            # one-CARE-a-day cap, which is `cf_free` being struck at the end of
            # the hop.
            for _ in range(CARE_FILL_HOPS):
                cf_d = (xp.abs(tx - fx0) + xp.abs(ty - fy0)).astype(i32)
                cf_ok = cf_free & (cf_d + 1 <= f_left)
                cf_key = xp.where(cf_ok, cf_d * N_T + idx, _BIG).astype(i32)
                b = xp.argmin(cf_key).astype(i32)
                hit = f_can & (cf_key[b] < _BIG)
                bx, by = tx[b], ty[b]
                bdx, bdy = bx - fx0, by - fy0
                bwalk = xp.abs(bdx) + xp.abs(bdy)
                w2 = r - f_t0
                cf_step = xp.where(w2 < xp.abs(bdx),
                                   xp.where(bdx > 0, O.OP_EAST, O.OP_WEST),
                                   xp.where(bdy > 0, O.OP_SOUTH, O.OP_NORTH)).astype(i32)
                in_cf = hit & (w2 >= 0) & (w2 < bwalk)
                at_cf = hit & (w2 == bwalk)
                u_op = xp.where(in_cf, cf_step,
                                xp.where(at_cf, O.OP_CARE, u_op)).astype(i32)
                u_a = xp.where(in_cf, 0, xp.where(
                    at_cf, (ROUTE_VRP_OPT_MARK + 3) if ROUTE_VRP_OPT_ON else 0, u_a)).astype(i32)
                u_q = xp.where(in_cf | at_cf, 0, u_q).astype(i32)
                # Struck off for every later unit, and for this unit's next
                # hop: one CARE an animal a day is all the engine banks.
                cf_free = cf_free & ~(hit & (idx == b))
                fx0 = xp.where(hit, bx, fx0).astype(i32)
                fy0 = xp.where(hit, by, fy0).astype(i32)
                f_t0 = xp.where(hit, f_t0 + bwalk + 1, f_t0).astype(i32)
                f_left = xp.where(hit, f_left - bwalk - 1, f_left).astype(i32)

        if unit_drop is not None:
            # The return leg: walk from the block's last tile to its nearest
            # shed-access tile, then DROP the whole load into the shed. The
            # walk is the same axis-ordered decode the inter-tile steps use, so
            # a unit that is already standing on an access tile walks zero
            # turns and drops immediately.
            t0 = (xp.where(active, block_end, 0) + ins).astype(i32)
            hx, hy = near_x[e_final], near_y[e_final]
            hdx, hdy = hx - tx[e_final], hy - ty[e_final]
            walk = xp.abs(hdx) + xp.abs(hdy)
            w = r - t0
            in_walk = active & unit_drop & (w >= 0) & (w < walk)
            at_drop = active & unit_drop & (w == walk)
            home_op = xp.where(w < xp.abs(hdx),
                               xp.where(hdx > 0, O.OP_EAST, O.OP_WEST),
                               xp.where(hdy > 0, O.OP_SOUTH, O.OP_NORTH)).astype(i32)
            u_op = xp.where(in_walk, home_op, xp.where(at_drop, O.OP_DROP, u_op)).astype(i32)
            u_a = xp.where(in_walk | at_drop, 0, u_a).astype(i32)
            u_q = xp.where(in_walk | at_drop, 0, u_q).astype(i32)

        if melon is not None or bank is not None:
            # [MELON_OPEN / BANK_BEFORE_LOT] Written over the window the clock
            # above skipped -- one leg, whichever trigger asked for it:
            # out to the nearest shed access on the same axis order every other
            # walk uses, the DROP, then the same walk back to the tile the
            # block was standing on. Any turn of the reserve the leg does not
            # need is PASS.
            mx, my = tx[m_ins], ty[m_ins]
            hdx = mnx[m_ins] - mx
            hdy = mny[m_ins] - my
            walk_m = (xp.abs(hdx) + xp.abs(hdy)).astype(i32)
            wm = (r - t_ins).astype(i32)
            out_op = xp.where(wm < xp.abs(hdx),
                              xp.where(hdx > 0, O.OP_EAST, O.OP_WEST),
                              xp.where(hdy > 0, O.OP_SOUTH, O.OP_NORTH)).astype(i32)
            wb = (wm - walk_m - 1).astype(i32)
            back_op = xp.where(wb < xp.abs(hdx),
                               xp.where(hdx > 0, O.OP_WEST, O.OP_EAST),
                               xp.where(hdy > 0, O.OP_NORTH, O.OP_SOUTH)).astype(i32)
            live = active & (ins > 0) & (wm >= 0) & (wm < ins)
            at_bank = live & (wm == walk_m)
            # [MIDDAY_PLACE] The deposit op. OP_DROP dumps the unit's whole
            # inventory and destroys the overflow; the engine's OP_PLACE banks
            # `min(qty, inv[item])` of one item and leaves the rest on the
            # unit, so a mid-block deposit stops voiding the block's carried
            # feed and fertilizer. Same one turn either way.
            bank_op = (O.OP_PLACE if (MIDDAY_PLACE_ON or SAME_DAY_FERT_ON)
                       else O.OP_DROP)                           # [SWITCH]
            u_op = xp.where(live & (wm < walk_m), out_op,
                            xp.where(at_bank, bank_op,
                                     xp.where(live & (wm > walk_m) & (wm < 2 * walk_m + 1),
                                              back_op,
                                              xp.where(live, O.OP_PASS, u_op)))).astype(i32)
            if MIDDAY_PLACE_ON or SAME_DAY_FERT_ON:              # [SWITCH]
                # [SAME_DAY_FERT] The item the excursion banks, and the only
                # place the two builds differ: melon's whole harvest against a
                # counted number of fertilizer.
                dep_item = spec.I_FERT if SAME_DAY_FERT_ON else spec.I_MELON
                u_a = xp.where(at_bank, dep_item,
                               xp.where(live, 0, u_a)).astype(i32)
                u_q = xp.where(at_bank, dep_q,
                               xp.where(live, 0, u_q)).astype(i32)
            else:
                u_a = xp.where(live, 0, u_a).astype(i32)
                u_q = xp.where(live, 0, u_q).astype(i32)

        route_op.append(u_op)
        route_a.append(u_a)
        route_q.append(u_q)

        blk.append(xp.where(active, cpick[:, e] - prev, 0))
        n_pick.append(p_u)
        n_lead.append(l_u)
        # A unit the cut left inactive spends no turn at all, so it starts
        # nowhere and the early flag has to go with it.
        n_early.append(xp.where(active, early_u, 0).astype(i32))
        if program_return is not None:
            pr_banked = pr_banked | (pr_unit & active & (idx >= s) & (idx <= end))

        # Gated on `active`: an inactive unit takes `end = s - 1`, so a bare
        # `end + 1` walks `start` *back* one rank -- and once it has, the next
        # unit with budget re-works that tile and double-counts its pickups in
        # `blk`. For an active unit this is already the value.
        start = xp.where(active, end + 1, start).astype(i32)

    # Tiles the day's labour actually reaches: ranks below `start`, mapped
    # back to view (serpentine) tile space so the caller can read chains and
    # yields off it directly.
    cov_rank = xp.arange(N_T, dtype=i32) < start
    if tile_alloc is not None:
        # [TILE_ALLOC] A stolen rank is worked by the unit that stole it, which
        # may be past the prefix the day's last block reaches -- the day did
        # that tile, so the caller has to read its chain off `covered` like any
        # other.
        cov_rank = cov_rank | ta_taken
    if hasattr(order, "at"):
        covered = xp.zeros(N_T, bool).at[order].set(cov_rank)
    else:
        covered = np.zeros(N_T, bool)
        covered[np.asarray(order)] = np.asarray(cov_rank)
    banked = None
    if bank is not None or mel_ranked:
        # [BANK_BEFORE_LOT / MIDDAY_PLACE_V2] The ranks the excursions banked,
        # in view space so the caller can price them off the same yield arrays
        # `covered` reads. Whichever trigger is compiled owns the channel; the
        # two are mutually exclusive by the `BANK_BEFORE_LOT_ON` assert.
        exc_rank = bank_rank if bank is not None else mel_rank
        if hasattr(order, "at"):
            banked = xp.zeros(N_T, bool).at[order].set(exc_rank)
        else:
            banked = np.zeros(N_T, bool)
            banked[np.asarray(order)] = np.asarray(exc_rank)
    if program_return is not None:
        if hasattr(order, "at"):
            pr_deposited = xp.zeros(N_T, bool).at[order].set(pr_banked)
        else:
            pr_deposited = np.zeros(N_T, bool)
            pr_deposited[np.asarray(order)] = np.asarray(pr_banked)
        banked = (banked, pr_deposited)
    return (xp.stack(route_op), xp.stack(route_a), xp.stack(route_q),
            xp.stack(blk, axis=1), covered, xp.stack(n_pick),
            xp.stack(n_lead), xp.stack(n_early), banked)   # blk -> [N_PICK, MU]


def _market(xp, wheat_buy, fert_buy, seed_buy, a_buy, buy_land, lots, n_hire,
            pre_wheat=None, pre_fert=None, pre_seed=None, hire_wide_early=None,
            pack=None, melon_lots=None, z_heavy=None, pump=None, spread=None,
            prio=None, dump=None, endrow=None, endrow2=None, dodge=None,
            drip=None):
    """Fixed market schedule (see the module docstring). `lots` is int[3, 9]:
    units of each product in each SELL lot, already gated and reserved.

    `pre_*` and `hire_wide_early` are `plan.PRESTOCK_ON`'s and are `None` with
    the switch off, so off this emits exactly the rows it always did.

    `pack` is `plan.MARKET_PACK_ON`'s: a traced bool, true on a day whose hires
    and purchases together fit one turn's ten slots, where both go out at
    `O.TURN_HIRE` and `O.TURN_BUY` is left empty. The caller owns the
    predicate, and owns it alone -- it is the same scalar that moved the crew's
    start to `ops.ROUTE_BASE_PACK`, so a second reading of it here could put
    the units in front of the row they are picking up from. `None` off, and
    then neither row moves.

    `spread` is `plan.SPREAD_ROWS_ON`'s: int[n_rows, 9], the day's VOLUNTARY
    sale cut over `spread_rows_turns()`, and then `lots` carries only what is
    not that sale. `None` off the switch, and then `lots` is the whole day and
    the rows are the ones this function always emitted.

    `dump` is `plan.SHED_DUMP_ROW_ON`'s: int[9], the units of each product to
    sell on `SHED_DUMP_ROW_TURN` to make room for tonight's deposit, a traced
    vector that is zero on every day the projection says the deposit fits.
    `None` off the switch, and then no row is emitted on that turn at all.

    `pump` is `plan.OPEN_PUMP_ON`'s: units of wheat to buy at hour 0 and sell
    back at the head of the BUY row, a traced int that is zero on every day
    the switch declines. `None` off, and then the two rows are byte-identical
    to the ones this function always emitted. `plan.OPEN_PUMP_SLOT0_ON` moves
    the hour-0 leg to index 0 and the hires behind it; off, the hour-0 row is
    slot for slot the one the pump always emitted.

    `prio` is `plan.SELL_SLOT_PRIORITY_ON`'s: int[n_lots, 9], `sell_slot_scores`
    for each lot -- the coins that lot's own units lose if the rival's batch
    lands in the pot first. It permutes the nine product slots of each SELL
    row and, on the merged BUY row, may put the lot in front of the day's
    purchases. `None` off the switch, and then every row is byte-identical to
    the one this function always emitted.
    """
    i32 = xp.int32
    op = xp.zeros((TPD, MO), dtype=i32)
    arg = xp.zeros((TPD, MO), dtype=i32)
    qty = xp.zeros((TPD, MO), dtype=i32)
    slot = xp.arange(MO, dtype=i32)

    # ---- [SPREAD_ROWS] which row rides the BUY row ------------------------
    # `O.EARLY_SELL_LOT1_TURN` is the first post-tick row of the day and the
    # BUY row's turn at once, so the spread row that stands there takes lot 1's
    # seat in the `EARLY_SELL` merge below rather than being written over the
    # day's purchases. It inherits lot 1's fallback with it: a day the ten slots
    # cannot hold both sells that row on `O.SELL_TURNS[0]` instead.
    sp_turns, sp_merge = (), -1
    if spread is not None:
        _spread_check()
        sp_turns, sp_merge = spread_rows_turns(), spread_merge_row()
        if sp_merge >= 0:
            lots = xp.concatenate(
                [(lots[0] + spread[sp_merge]).astype(i32)[None, :],
                 lots[1:].astype(i32)], axis=0)

    # turns 0 and 2 -- hire the day's hands, ten to a turn.
    #
    # `_process_market` truncates each seat's queue to `maxMarketOrdersPerTurn`
    # (10) *per turn*, so the eleventh hand of a day has to be asked for in a
    # second turn. Turn 1 is the BUY row's, which has to resolve before any
    # unit picks its inputs up, so the overflow row is turn 2 and SELL lot 1
    # sits at turn 3. HIRE is an atomic order: the engine handles it in player
    # order at the head of its slot round and drops it from the lockstep, so a
    # HIRE never pairs with the other seat's SELL or BUY_PRODUCT however the
    # two seats' rows compact (`sim/market.py`, `assert_no_cross`).
    first = xp.minimum(n_hire, MO).astype(i32)
    rest = xp.maximum(n_hire - MO, 0).astype(i32)
    for turn, n in ((O.TURN_HIRE, first), (O.TURN_HIRE_WIDE, rest)):
        op = _row(xp, op, turn, xp.where(slot < n, O.MO_HIRE, O.MO_NONE))
        qty = _row(xp, qty, turn, xp.where(slot < n, 1, 0))
    if hire_wide_early is not None:
        # [PRESTOCK] The residual BUY row is empty on this day, so turn 1 is
        # free and the overflow hire row moves into it -- which is the whole
        # reason `ROUTE_BASE_WIDE_PRE` may be 2. Written as a `where` over both
        # rows rather than a moved constant: the emptiness is a traced scalar,
        # and the turn a row is emitted on cannot be.
        early = xp.asarray(hire_wide_early)
        n_late = xp.where(early, 0, rest).astype(i32)
        op = _row(xp, op, O.TURN_HIRE_WIDE, xp.where(slot < n_late, O.MO_HIRE, O.MO_NONE))
        qty = _row(xp, qty, O.TURN_HIRE_WIDE, xp.where(slot < n_late, 1, 0))

    # ---- the opening pump, hour-0 leg [SWITCH, OPEN_PUMP] -----------------
    # Behind the day's hires, so the crew is paid first: HIRE is atomic and the
    # engine resolves a slot round's atomic orders before *that round's*
    # lockstep, so this order commits with the hire bill already out of the
    # purse -- and only because the hires stand in earlier slot rounds, which
    # is the fact `OPEN_PUMP_SLOT0_ON` gives up on purpose. Nothing else
    # in the game has an order at this hour -- our own turn 0 is the hire row
    # and the class-A tapes are idle at step 0 -- so the 53 units come out of
    # an untouched pot and move the quote alone.
    pump_fires = None
    if pump is not None:
        # The pump owns the shape of turns 0 and 1. Every switch that moves
        # those rows is refused at Python time rather than silently overwriting
        # a leg: `MARKET_PACK` empties turn 1, `PRESTOCK`'s overflow hire row
        # takes it, and the `A0`/`A1`/`Z` sell modes put a lot in front of the
        # sell-back or on top of the hire row.
        assert pack is None, "OPEN_PUMP owns turn 1; MARKET_PACK empties it"
        assert hire_wide_early is None, \
            "OPEN_PUMP owns turn 1; PRESTOCK's overflow hire row takes it"
        assert EARLY_SELL_MODE not in (EARLY_SELL_MODES_HIRE_ROW
                                       + EARLY_SELL_MODES_LOT_FIRST
                                       + EARLY_SELL_MODES_ZERO_ROW), \
            "OPEN_PUMP needs the sell-back at index 0 of the BUY row"
        n_pump = _as(xp, pump)
        # `wheat_buy == 0` is the fact the layout stands on: the sell-back
        # takes the `B_WHEAT` slot, so a day that buys wheat cannot pump. It
        # holds on day 0 by construction (no shed, no herd, nothing to feed)
        # and is checked rather than assumed. `first < MO` is the engine's
        # ten-orders-a-turn truncation on an eleven-hand opening.
        pump_fires = ((n_pump > OPEN_PUMP_KEEP) & (_as(xp, wheat_buy) == 0)
                      & (first < MO))
        if OPEN_PUMP_SLOT0_ON:
            # [SLOT0] The pump at index 0 and the day's hires behind it, for
            # the race against a seat that draws at hour 0 too: the engine
            # pairs the two queues by index, so index 0 is the only slot whose
            # ladder is quoted off a pot nobody has drained first. `first < MO`
            # is already in `pump_fires`, so slots 1..first exist and the row
            # still holds the engine's ten. Written over the whole row rather
            # than as one more `hit`: every hire moves one slot along, and a
            # scatter that shifted a live order past the tenth slot would be
            # eaten in silence.
            shifted = (slot >= 1) & (slot <= first)
            h_op = xp.where(shifted, O.MO_HIRE, O.MO_NONE).astype(i32)
            h_qty = xp.where(shifted, 1, 0).astype(i32)
            at0 = slot == 0
            p_op = xp.where(at0, O.MO_BUY_PRODUCT, h_op).astype(i32)
            p_arg = xp.where(at0, xp.asarray(spec.I_WHEAT, i32), 0).astype(i32)
            p_qty = xp.where(at0, n_pump, h_qty).astype(i32)
            op = _row(xp, op, O.TURN_HIRE,
                      xp.where(pump_fires, p_op, op[O.TURN_HIRE]))
            arg = _row(xp, arg, O.TURN_HIRE,
                       xp.where(pump_fires, p_arg, arg[O.TURN_HIRE]))
            qty = _row(xp, qty, O.TURN_HIRE,
                       xp.where(pump_fires, p_qty, qty[O.TURN_HIRE]))
        else:
            hit = pump_fires & (slot == xp.minimum(first, MO - 1))
            op = _row(xp, op, O.TURN_HIRE,
                      xp.where(hit, O.MO_BUY_PRODUCT, op[O.TURN_HIRE]))
            arg = _row(xp, arg, O.TURN_HIRE,
                       xp.where(hit, xp.asarray(spec.I_WHEAT, i32), arg[O.TURN_HIRE]))
            qty = _row(xp, qty, O.TURN_HIRE, xp.where(hit, n_pump, qty[O.TURN_HIRE]))

    # turn 1 -- the day's inputs, in the fixed slot layout.
    #
    # The op and argument columns are Python ints and stay Python ints until
    # the row is assembled: they are module constants, the layout is static,
    # and `xp.asarray` of a constant is a *tracer* inside `jax.jit`, which
    # would put the layout's own identity out of reach of a Python-time check
    # (the pump's `B_WHEAT` assert below reads this list).
    per_cat = {
        B_WHEAT: ([O.MO_BUY_PRODUCT], [spec.I_WHEAT],
                  [_as(xp, wheat_buy)]),
        B_FERT: ([O.MO_BUY_PRODUCT], [spec.I_FERT],
                 [_as(xp, fert_buy)]),
        B_SEEDS: ([O.MO_BUY_SEED] * spec.N_CROPS,
                  list(range(spec.N_CROPS)),
                  [seed_buy[c].astype(i32) for c in range(spec.N_CROPS)]),
        # One slot per animal kind [1.3]: `BUY_ANIMAL` is one item per slot in
        # the engine (`_commit_unit`), there is no quantity-vector form, so a
        # mixed herd needs three. 1 + 1 + 5 + 3 is exactly the engine's ten,
        # which is why land had to leave this row first (M2).
        B_ANIMAL: ([O.MO_BUY_ANIMAL] * spec.N_ANIMALS,
                   list(range(spec.N_ANIMALS)),
                   [a_buy[a].astype(i32) for a in range(spec.N_ANIMALS)]),
    }
    # The slot layout is **fixed**, and can be: the budget grants at most what
    # the purse holds, so the quantities in this row always total at most the
    # money on hand and the engine can honour them in any slot sequence. A row
    # permuted per policy would give the two seats different layouts as soon as
    # their strategies differed -- and `sim/market.py` models a slot round on
    # the standing assumption that both seats present the same op there (see
    # its `assert_no_cross`). Nothing is lost: value per coin decides *who gets
    # the money*, which is the strategy; the slot sequence only decides who is
    # served first out of a purse already known to cover everything. Shed room
    # is a second resource with the same property: `build_day` clips the
    # shed-bound grants against `SHED_CAPACITY - sum(shed)` in this very order,
    # so however the engine sequences the row every one of those buys fits.
    ops_, args_, qtys_ = [], [], []
    for _cat in DEFAULT_ORDER:
        o_, a_, q_ = per_cat[_cat]
        ops_ += o_; args_ += a_; qtys_ += q_
    # A Python-time check on a static layout, so it costs nothing and traces
    # fine. The engine truncates each seat's queue at ten orders a turn and
    # says nothing about it: the eleventh is simply lost, and that has already
    # cost a land purchase once.
    assert len(ops_) <= MO, f"the BUY row is {len(ops_)} orders and the engine takes {MO}"
    pad_n = MO - len(ops_)
    b_op = xp.concatenate([xp.asarray(ops_, dtype=i32),
                           xp.full((pad_n,), O.MO_NONE, dtype=i32)])
    b_arg = xp.concatenate([xp.asarray(args_, dtype=i32), xp.zeros(pad_n, i32)])
    b_qty = xp.concatenate([xp.stack(qtys_).astype(i32), xp.zeros(pad_n, i32)])
    # ---- the opening pump, sell-back leg [SWITCH, OPEN_PUMP] --------------
    # One slot changes op and nothing shifts. `B_WHEAT` is the row's head slot
    # and it already carries `spec.I_WHEAT` as its argument, so a day that buys
    # no wheat -- which is the only day the switch fires on -- hands the
    # sell-back the head of the compacted row for free. That is the whole
    # mechanism: the engine pairs the two seats by queue index over the
    # compacted row, so index 0 is what interleaves with the opponent's own
    # first order and meets the quote the hour-0 leg drained.
    if pump_fires is not None:
        w_slot = buy_row_slot(B_WHEAT)
        # A Python-time claim about a Python-time layout: `ops_` and `args_`
        # are the module's own constants (see `per_cat`), never traced values,
        # so this reads the same under numpy and under `jax.jit`.
        assert ops_[w_slot] == O.MO_BUY_PRODUCT and args_[w_slot] == spec.I_WHEAT, \
            "the pump's sell-back assumes B_WHEAT's slot carries the wheat argument"
        hit = pump_fires & (slot == w_slot)
        b_op = xp.where(hit, O.MO_SELL, b_op).astype(i32)
        b_qty = xp.where(hit, _as(xp, pump) - OPEN_PUMP_KEEP, b_qty).astype(i32)
    op = _row(xp, op, O.TURN_BUY, xp.where(b_qty > 0, b_op, O.MO_NONE))
    arg = _row(xp, arg, O.TURN_BUY, b_arg)
    qty = _row(xp, qty, O.TURN_BUY, b_qty)
    if hire_wide_early is not None:
        # The overflow hire row, when it lands here instead [PRESTOCK]. It only
        # ever does so on a day this row is empty, so the two can be selected
        # between rather than merged -- and HIRE is atomic in the engine (it
        # resolves at the head of its slot round, outside the SELL/BUY
        # lockstep), so a seat presenting hires here against a seat presenting
        # its BUY row cannot cross (`sim/market.assert_no_cross`).
        n_early = xp.where(early, rest, 0).astype(i32)
        h_op = xp.where(slot < n_early, O.MO_HIRE, O.MO_NONE).astype(i32)
        op = _row(xp, op, O.TURN_BUY, xp.where(early, h_op, op[O.TURN_BUY]))
        arg = _row(xp, arg, O.TURN_BUY, xp.where(early, 0, arg[O.TURN_BUY]))
        qty = _row(xp, qty, O.TURN_BUY,
                   xp.where(early, xp.where(slot < n_early, 1, 0), qty[O.TURN_BUY]))

    # ---- lot 1 behind the BUY row [SWITCH, EARLY_SELL] --------------------
    # The day's first lot, moved out of turn 3 and into the free slots of the
    # turn the purchases already use. `render.market_actions` and
    # `sim.rollout.compact_orders` both drop a `MO_NONE` slot, so what the
    # engine receives is the live orders in slot order: the buys compacted to
    # the front, the lot compacted directly behind them. Behind and not in
    # front, so every BUY_PRODUCT meets the inventory it always met.
    #
    # `fits` is the engine's ten-orders-a-seat-a-turn truncation, checked here
    # and not assumed: the BUY row is ten slots wide (1 wheat + 1 fertilizer +
    # 5 seeds + 3 animals) and a lot is nine, so a busy day genuinely cannot
    # hold both and the lot stays on `SELL_TURNS[0]`. Gather and not scatter,
    # for `MARKET_PACK`'s reason: a live order shifted past the tenth slot is
    # eaten in silence.
    early_fits = None
    if EARLY_SELL_ON:
        b_live = b_qty > 0
        n_b = xp.sum(b_live.astype(i32), dtype=i32)
        pad_e = xp.zeros(MO - spec.N_PRODUCTS, i32)
        lot1_q = lots[0].astype(i32)
        lot1_p = xp.arange(spec.N_PRODUCTS, dtype=i32)
        if prio is not None:
            # [SELL_SLOT_PRIORITY] (b) The lot's own block, ranked. It rides
            # inside the merged row, so the permutation has to happen before
            # `_pack` compacts it -- `_pack` keeps slot order, and slot order
            # is exactly what this switch is choosing.
            lot1_p = sell_slot_perm(xp, lot1_q, prio[0])
            lot1_q = lot1_q[lot1_p]
        lot1 = xp.concatenate([lot1_q, pad_e])
        s_live = lot1 > 0
        n_s = xp.sum(s_live.astype(i32), dtype=i32)
        e_arg = xp.concatenate([lot1_p.astype(i32), pad_e])

        def _pack(live, off):
            """Slot the k-th live entry lands in, `off` slots along. Gather
            and not scatter, for `MARKET_PACK`'s reason: numpy and JAX read a
            10x10 match alike, and a scattered live order shifted past the
            tenth slot is eaten in silence."""
            dest = (xp.cumsum(live.astype(i32)) - live.astype(i32) + off).astype(i32)
            hit = live[None, :] & (dest[None, :] == slot[:, None])
            src = xp.sum(xp.where(hit, slot[None, :], 0), axis=1).astype(i32)
            return src, xp.any(hit, axis=1)

        # [A0] Behind turn 0's hires, on a day the two fit the ten. HIRE is
        # atomic -- the engine resolves it at the head of its slot round, in
        # player order, outside the SELL/BUY lockstep -- so a lot behind the
        # hires is the earliest a row can carry it, recorded hour 1, and no
        # BUY_PRODUCT shares the turn with it at all. `rest > 0` (an
        # eleven-hand day) cannot fit and is caught by the same predicate.
        hire_fits = None
        if EARLY_SELL_MODE in EARLY_SELL_MODES_HIRE_ROW:
            hire_fits = (first + n_s) <= MO
            src_h, take_h = _pack(s_live, first)
            h_op = xp.where(slot < first, O.MO_HIRE,
                            xp.where(take_h, O.MO_SELL, O.MO_NONE)).astype(i32)
            h_arg = xp.where(take_h, e_arg[src_h], 0).astype(i32)
            h_qty = xp.where(slot < first, 1,
                             xp.where(take_h, lot1[src_h], 0)).astype(i32)
            ht = O.TURN_HIRE
            op = _row(xp, op, ht, xp.where(hire_fits, h_op, op[ht]))
            arg = _row(xp, arg, ht, xp.where(hire_fits, h_arg, arg[ht]))
            qty = _row(xp, qty, ht, xp.where(hire_fits, h_qty, qty[ht]))

        # The merged BUY row. `lot_first` decides which side of the purchases
        # the lot compacts to; the engine walks the turn's queue in slot order
        # against one running inventory, so the two are not the same trade.
        lot_first = EARLY_SELL_MODE in EARLY_SELL_MODES_LOT_FIRST
        off_b, off_s = (n_s, xp.zeros((), i32)) if lot_first else (xp.zeros((), i32), n_b)
        if prio is not None and SELL_SLOT_PRIORITY_SELLS_FIRST_ON and not lot_first:
            # [SELL_SLOT_PRIORITY] (a) Sells ahead of the day's purchases --
            # "where legal", which for this fixed layout is a Python-time list
            # of two: `B_WHEAT` and `B_FERT` are the only `BUY_PRODUCT` slots
            # the row can hold, so a block move is illegal exactly when the day
            # buys one of those two items AND lot 1 sells it. (A BUY_SEED or
            # BUY_ANIMAL never touches product inventory -- `sim/market.
            # _inventory_orders` -- so a sell may pass it freely.)
            #
            # Traced, not branched: `b_qty` and the lot are traced ints and the
            # slot a row stands in cannot be.
            same_item = xp.zeros((), bool)
            for _cat, _it in ((B_WHEAT, spec.I_WHEAT), (B_FERT, spec.I_FERT)):
                _sl = buy_row_slot(_cat)
                same_item = same_item | ((b_qty[_sl] > 0) & (lots[0][_it] > 0))
            sells_first = xp.logical_not(same_item)
            if pump_fires is not None:
                # `OPEN_PUMP` owns index 0 of this row on its own day and says
                # so in an assert; leave its day exactly as it was.
                sells_first = xp.logical_and(sells_first,
                                             xp.logical_not(pump_fires))
            off_b = xp.where(sells_first, n_s, 0).astype(i32)
            off_s = xp.where(sells_first, 0, n_b).astype(i32)
        src_b, take_b = _pack(b_live, off_b)
        src_s, take_s = _pack(s_live, off_s)
        m_op = xp.where(take_b, b_op[src_b],
                        xp.where(take_s, O.MO_SELL, O.MO_NONE)).astype(i32)
        m_arg = xp.where(take_b, b_arg[src_b],
                         xp.where(take_s, e_arg[src_s], 0)).astype(i32)
        m_qty = xp.where(take_b, b_qty[src_b],
                         xp.where(take_s, lot1[src_s], 0)).astype(i32)
        row_fits = (n_b + n_s) <= MO
        # Only where the hire row did not already take the lot.
        buy_fits = (row_fits if hire_fits is None
                    else xp.logical_and(row_fits, xp.logical_not(hire_fits)))
        # [Z] A wide day is not a Z day -- turn 2 is its overflow hire row and
        # the purchases would have nowhere to stand -- so it keeps mode A's
        # merged row and the block below leaves it alone. Every other day is a
        # Z day and the merge is the one thing it must NOT do.
        z_fires = None
        if EARLY_SELL_MODE in EARLY_SELL_MODES_ZERO_ROW:
            # [Z1] and heavy enough to be worth the tick turn 0 sells in front
            # of. The caller owns the predicate -- it fixed `route_base` on it
            # -- so a second reading of it here could disagree with the routes.
            z_fires = rest == 0
            if z_heavy is not None:
                z_fires = xp.logical_and(z_fires, xp.asarray(z_heavy))
            buy_fits = xp.logical_and(buy_fits, xp.logical_not(z_fires))
        et = O.EARLY_SELL_LOT1_TURN
        op = _row(xp, op, et, xp.where(buy_fits, m_op, op[et]))
        arg = _row(xp, arg, et, xp.where(buy_fits, m_arg, arg[et]))
        qty = _row(xp, qty, et, xp.where(buy_fits, m_qty, qty[et]))
        early_fits = (buy_fits if hire_fits is None
                      else xp.logical_or(buy_fits, hire_fits))

        # ---- [Z] the lot first, and the morning behind it -----------------
        # Turn 0 is the lot's, the whole ten slots of it: nine products is all
        # a lot can ever be, so unlike A there is no `fits` predicate and no
        # fallback -- every narrow day sells at recorded hour 2, in lockstep
        # with the field's own hour-0 dump. The hires it displaces go to turn
        # 1, their overflow row is empty by `z_fires`, and the BUY row takes
        # the first turn behind the hires with room for it: turn 1 when the
        # ten slots hold both, else turn 2 on its own. Hires stay in front of
        # the purchases inside turn 1 -- HIRE is atomic and the engine runs a
        # slot round's atomic orders first, so the crew is hired before the
        # row behind it spends a coin, exactly as it was on turn 0.
        if z_fires is not None:
            z_buy_t1 = xp.logical_and(z_fires, (first + n_b) <= MO)
            z_buy_t2 = xp.logical_and(z_fires, xp.logical_not(z_buy_t1))
            zt_lot, zt_hire = O.EARLY_SELL_Z_LOT_TURN, O.EARLY_SELL_Z_HIRE_TURN
            zt_wide = O.EARLY_SELL_Z_HIRE_WIDE_TURN
            # turn 0 -- lot 1 alone, in the nine fixed product slots every
            # other SELL row uses, so both seats still present one layout.
            z0_op = xp.where(lot1 > 0, O.MO_SELL, O.MO_NONE).astype(i32)
            op = _row(xp, op, zt_lot, xp.where(z_fires, z0_op, op[zt_lot]))
            arg = _row(xp, arg, zt_lot, xp.where(z_fires, e_arg, arg[zt_lot]))
            qty = _row(xp, qty, zt_lot, xp.where(z_fires, lot1, qty[zt_lot]))
            # turn 1 -- the hires, and the purchases behind them on a day the
            # ten slots hold both. Gather and not scatter, for the reason the
            # merge above gives: a live order shifted past the tenth slot is
            # eaten in silence.
            src_zb, take_zb = _pack(b_live, first)
            z1_op = xp.where(slot < first, O.MO_HIRE,
                             xp.where(take_zb, b_op[src_zb], O.MO_NONE)).astype(i32)
            z1_arg = xp.where(take_zb, b_arg[src_zb], 0).astype(i32)
            z1_qty = xp.where(slot < first, 1,
                              xp.where(take_zb, b_qty[src_zb], 0)).astype(i32)
            h_op = xp.where(slot < first, O.MO_HIRE, O.MO_NONE).astype(i32)
            h_qty = xp.where(slot < first, 1, 0).astype(i32)
            op = _row(xp, op, zt_hire,
                      xp.where(z_fires, xp.where(z_buy_t1, z1_op, h_op), op[zt_hire]))
            arg = _row(xp, arg, zt_hire,
                       xp.where(z_fires, xp.where(z_buy_t1, z1_arg, 0), arg[zt_hire]))
            qty = _row(xp, qty, zt_hire,
                       xp.where(z_fires, xp.where(z_buy_t1, z1_qty, h_qty), qty[zt_hire]))
            # turn 2 -- the purchases when turn 1 had no room. The row is the
            # fixed ten-slot layout it always was, holes and all, so nothing
            # can be shifted past the tenth slot and no packing is needed.
            # `z_buy_t2` implies `z_fires` implies an empty overflow hire row.
            op = _row(xp, op, zt_wide,
                      xp.where(z_buy_t2, xp.where(b_qty > 0, b_op, O.MO_NONE), op[zt_wide]))
            arg = _row(xp, arg, zt_wide, xp.where(z_buy_t2, b_arg, arg[zt_wide]))
            qty = _row(xp, qty, zt_wide, xp.where(z_buy_t2, b_qty, qty[zt_wide]))
            early_fits = xp.logical_or(early_fits, z_fires)

    # ---- the packed row [SWITCH, MARKET_PACK] -----------------------------
    # Both morning rows on turn 0, and turn 1 left empty. The caller has
    # already checked that `n_hire` plus the row's live orders fit the ten
    # slots `_process_market` truncates each seat's queue to, and has moved the
    # crew's start to `ops.ROUTE_BASE_PACK` on the strength of it.
    if pack is not None:
        pk = xp.asarray(pack)
        # The purchases compacted to the front. `render.market_actions` drops a
        # `MO_NONE` slot, so what reaches the engine is the *live* orders --
        # but the array is a fixed ten-slot layout with holes, and shifting it
        # behind the hires without closing the holes first would push a live
        # BUY_ANIMAL in the last slot past the tenth, where the truncation eats
        # it in silence. Gather, not scatter, so numpy and JAX read alike: a
        # 10x10 match picks out the slot holding the k-th live order.
        live = b_qty > 0
        n_live = xp.sum(live.astype(i32), dtype=i32)
        dest = (xp.cumsum(live.astype(i32)) - live.astype(i32)).astype(i32)
        hit = live[None, :] & (dest[None, :] == slot[:, None])
        src = xp.sum(xp.where(hit, slot[None, :], 0), axis=1).astype(i32)
        c_op, c_arg, c_qty = b_op[src], b_arg[src], b_qty[src]
        # Hires first, which is the order the two rows already had: the engine
        # resolves slot round i's atomic orders (HIRE among them) in player
        # order before the round's lockstep, and rounds run in slot order, so
        # slots 0..n_hire-1 hire before anything behind them spends a coin.
        k = xp.clip(slot - first, 0, MO - 1)
        buy_here = (slot >= first) & (slot - first < n_live)
        p_op = xp.where(slot < first, O.MO_HIRE,
                        xp.where(buy_here, c_op[k], O.MO_NONE)).astype(i32)
        p_arg = xp.where(buy_here, c_arg[k], 0).astype(i32)
        p_qty = xp.where(slot < first, 1,
                         xp.where(buy_here, c_qty[k], 0)).astype(i32)
        op = _row(xp, op, O.TURN_HIRE, xp.where(pk, p_op, op[O.TURN_HIRE]))
        arg = _row(xp, arg, O.TURN_HIRE, xp.where(pk, p_arg, arg[O.TURN_HIRE]))
        qty = _row(xp, qty, O.TURN_HIRE, xp.where(pk, p_qty, qty[O.TURN_HIRE]))
        op = _row(xp, op, O.TURN_BUY, xp.where(pk, O.MO_NONE, op[O.TURN_BUY]))
        arg = _row(xp, arg, O.TURN_BUY, xp.where(pk, 0, arg[O.TURN_BUY]))
        qty = _row(xp, qty, O.TURN_BUY, xp.where(pk, 0, qty[O.TURN_BUY]))

    # ---- the prestock row [SWITCH, PRESTOCK] ------------------------------
    # Tomorrow's feed wheat, fertilizer and seeds, seven of the ten slots, at a
    # turn no other row uses. No BUY_ANIMAL and no BUY_LAND: the herd mix is a
    # same-day policy output and land is funded by the morning's own lot.
    if pre_wheat is not None:
        p_op = xp.asarray([O.MO_BUY_PRODUCT, O.MO_BUY_PRODUCT]
                          + [O.MO_BUY_SEED] * spec.N_CROPS, dtype=i32)
        p_arg = xp.asarray([spec.I_WHEAT, spec.I_FERT] + list(range(spec.N_CROPS)),
                           dtype=i32)
        p_qty = xp.concatenate([xp.stack([_as(xp, pre_wheat), _as(xp, pre_fert)]),
                                pre_seed.astype(i32)])
        pad_p = MO - int(p_op.shape[0])
        p_op = xp.concatenate([p_op, xp.full((pad_p,), O.MO_NONE, dtype=i32)])
        p_arg = xp.concatenate([p_arg, xp.zeros(pad_p, i32)])
        p_qty = xp.concatenate([p_qty, xp.zeros(pad_p, i32)])
        op = _row(xp, op, O.TURN_PRESTOCK, xp.where(p_qty > 0, p_op, O.MO_NONE))
        arg = _row(xp, arg, O.TURN_PRESTOCK, p_arg)
        qty = _row(xp, qty, O.TURN_PRESTOCK, p_qty)

    # SELL turns. The split across the three lots is `core.sell`'s allocation
    # [HEURISTIC, PLANNER_V3_1 1.2]: each unit goes to the lot whose adjusted
    # marginal -- the projected own quote net of timing pressure and of the
    # externality on the later lots -- is highest, and only if that marginal
    # clears the product's reservation value. Every lot's row keeps the same
    # nine product slots in the same order whatever it carries, so both seats
    # present an identical layout on every SELL turn (`sim/market.py`'s
    # `assert_no_cross`).
    pad = xp.zeros(MO - spec.N_PRODUCTS, i32)
    arg_row = xp.concatenate([xp.arange(spec.N_PRODUCTS, dtype=i32), pad])
    # [EARLY_SELL] Mode "B" moves lots 2 and 3 to `O.EARLY_SELL_LATE_TURNS`
    # and "A21" moves lot 2 alone; lot 1 keeps `SELL_TURNS[0]` as the turn it
    # falls back to on a day no earlier row could hold it, and as the turn that
    # carries the day's BUY_LAND.
    _lot_turns = early_lot_turns()
    dodge_row = None
    if dodge is not None and LOT4_ON:
        # [SWITCH, V15_DODGE] the d20-28 dusk lot (product-indexed, before any slot
        # permutation) moves to V15_DODGE_TURN: merged into the lot standing on that
        # turn if there is one, else emitted as its own row after the lots.
        k4 = list(_lot_turns).index(LOT4_TURN)
        p_ix = xp.arange(spec.N_PRODUCTS, dtype=i32)
        mask = ((p_ix == spec.I_MILK) | (p_ix == spec.I_WOOL)) if V15_DODGE_MW \
            else (p_ix >= 0)
        moved = xp.where(dodge & mask, lots[k4], 0).astype(i32)
        l_ix = xp.arange(lots.shape[0], dtype=i32)[:, None]
        lots = (lots - (l_ix == k4).astype(i32) * moved[None, :]).astype(i32)
        if V15_DODGE_TURN in tuple(_lot_turns):
            kt = list(_lot_turns).index(V15_DODGE_TURN)
            lots = (lots + (l_ix == kt).astype(i32) * moved[None, :]).astype(i32)
        else:
            dodge_row = moved
    for k, turn in enumerate(_lot_turns):
        lot = lots[k].astype(i32)
        if k == 0 and early_fits is not None:
            lot = xp.where(early_fits, 0, lot).astype(i32)
        row_arg = arg_row
        if prio is not None:
            # [SELL_SLOT_PRIORITY] (b) The row is the same nine products with
            # the same nine quantities; only which one is quoted first changes.
            # The argument column moves with the quantities -- both seats no
            # longer present the same product in the same slot, which is the
            # invariant `sim/market.py::assert_no_cross` guarded, and SELL
            # against SELL is not the cross that guard is about (it flags SELL
            # against BUY_PRODUCT, and a pure SELL row holds none).
            perm = sell_slot_perm(xp, lot, prio[k])
            lot = lot[perm]
            row_arg = xp.concatenate([perm.astype(i32), pad])
        op = _row(xp, op, turn,
                  xp.concatenate([xp.where(lot > 0, O.MO_SELL, O.MO_NONE).astype(i32), pad]))
        arg = _row(xp, arg, turn, row_arg)
        qty = _row(xp, qty, turn, xp.concatenate([lot, pad]))

    if dodge_row is not None:
        op = _row(xp, op, V15_DODGE_TURN,
                  xp.concatenate([xp.where(dodge_row > 0, O.MO_SELL, O.MO_NONE).astype(i32), pad]))
        arg = _row(xp, arg, V15_DODGE_TURN, arg_row)
        qty = _row(xp, qty, V15_DODGE_TURN, xp.concatenate([dodge_row, pad]))

    # ---- the spread rows [SWITCH, SPREAD_ROWS] ----------------------------
    # The same nine product slots in the same order as every other SELL row, so
    # both seats still present one layout on every turn (`sim/market.py`'s
    # `assert_no_cross`), and a row with nothing behind it keeps its slots
    # `MO_NONE`. The merged row is not emitted here -- it went out behind the
    # BUY row above, or fell back onto `O.SELL_TURNS[0]` with lot 1.
    for k, turn in enumerate(sp_turns):
        if k == sp_merge:
            continue
        s_row = spread[k].astype(i32)
        op = _row(xp, op, turn,
                  xp.concatenate([xp.where(s_row > 0, O.MO_SELL, O.MO_NONE).astype(i32),
                                  pad]))
        arg = _row(xp, arg, turn, arg_row)
        qty = _row(xp, qty, turn, xp.concatenate([s_row, pad]))

    if melon_lots is not None:
        # [MELON_OPEN] The dump day's own rows, one product wide, on the turns
        # `ops.MELON_LOT_TURNS` reserves. Zero on every other day of the
        # season, and then `MO_NONE` in every slot -- the same "a lot with
        # nothing behind it keeps its slot empty" the SELL rows above rely on,
        # so both seats still present an identical layout on every turn.
        m_slot = xp.arange(MO, dtype=i32) == spec.I_MELON
        for k, turn in enumerate(melon_lot_turns()):
            q = melon_lots[k].astype(i32)
            op = _row(xp, op, turn,
                      xp.where(m_slot & (q > 0), O.MO_SELL, O.MO_NONE).astype(i32))
            arg = _row(xp, arg, turn,
                       xp.where(m_slot, xp.asarray(spec.I_MELON, i32), 0).astype(i32))
            qty = _row(xp, qty, turn, xp.where(m_slot, q, 0).astype(i32))

    if dump is not None:
        # [SHED_DUMP_ROW] The hour-23 row, in the same nine product slots in the
        # same order as every other SELL row, so both seats still present one
        # layout on every turn (`sim/market.py`'s `assert_no_cross`) -- and a
        # day whose deposit fits keeps every slot `MO_NONE`, which is the same
        # "a lot with nothing behind it is an empty row" the SELL rows above
        # rely on.
        d_row = dump.astype(i32)
        op = _row(xp, op, SHED_DUMP_ROW_TURN,
                  xp.concatenate([xp.where(d_row > 0, O.MO_SELL, O.MO_NONE).astype(i32),
                                  pad]))
        arg = _row(xp, arg, SHED_DUMP_ROW_TURN, arg_row)
        qty = _row(xp, qty, SHED_DUMP_ROW_TURN, xp.concatenate([d_row, pad]))

    if endrow is not None:
        # [ENDROUTE] Day 29's last EXECUTED row, in the same nine product slots
        # in the same order as every other SELL row.  Off the terminal day the
        # vector is all-zero, so every slot stays `MO_NONE` and the day's
        # layout is the one it always was.
        e_full = xp.concatenate([endrow.astype(i32), pad]).astype(i32)
        e_hit = e_full > 0
        op = _row(xp, op, ENDROUTE_TURN,
                  xp.where(e_hit, xp.asarray(O.MO_SELL, i32),
                           op[ENDROUTE_TURN]).astype(i32))
        arg = _row(xp, arg, ENDROUTE_TURN,
                   xp.where(e_hit, arg_row, arg[ENDROUTE_TURN]).astype(i32))
        qty = _row(xp, qty, ENDROUTE_TURN,
                   xp.where(e_hit, e_full, qty[ENDROUTE_TURN]).astype(i32))

    if endrow2 is not None:
        # [ENDROUTE_ROW2] The same row, one turn set earlier, so the terminal
        # day's late harvest is sold over two lots rather than one.  Off the
        # terminal day the vector is all-zero and the layout is unchanged.
        e2_full = xp.concatenate([endrow2.astype(i32), pad]).astype(i32)
        e2_hit = e2_full > 0
        op = _row(xp, op, ENDROUTE_ROW2_TURN,
                  xp.where(e2_hit, xp.asarray(O.MO_SELL, i32),
                           op[ENDROUTE_ROW2_TURN]).astype(i32))
        arg = _row(xp, arg, ENDROUTE_ROW2_TURN,
                   xp.where(e2_hit, arg_row, arg[ENDROUTE_ROW2_TURN]).astype(i32))
        qty = _row(xp, qty, ENDROUTE_ROW2_TURN,
                   xp.where(e2_hit, e2_full, qty[ENDROUTE_ROW2_TURN]).astype(i32))

    # BUY_LAND in the spare tenth slot of the first SELL turn [M2]. The engine
    # resolves a turn's slots in order and BUY_LAND is atomic -- `_do_buy_land`
    # runs at the head of its slot round, in player order, outside the
    # SELL/BUY lockstep -- so the nine sells ahead of it have already banked
    # their coins when it commits, and it can never pair with the other seat's
    # order. Nine SELL slots plus this one is exactly the engine's ten.
    land_turn = O.SELL_TURNS[0]
    land_slot = xp.arange(MO, dtype=i32) == MO - 1
    bl = _as(xp, buy_land)
    op = _row(xp, op, land_turn,
              xp.where(land_slot & (bl > 0), O.MO_BUY_LAND, op[land_turn]))
    qty = _row(xp, qty, land_turn, xp.where(land_slot, bl, qty[land_turn]))
    if drip is not None and LOT4_ON:
        op, arg, qty = _drip_sell(xp, op, arg, qty, drip)
    return op, arg, qty


def _drip_sell(xp, op, arg, qty, gate):
    """[SWITCH, DRIP_SELL] move up to DRIP_SELL_LOT units per product per drip
    turn out of the LOT4 row (turn 17), post hoc on the finished rows."""
    i32 = xp.int32
    slot = xp.arange(op.shape[1], dtype=i32)
    g = xp.asarray(gate)
    turns = sorted(int(x) for x in str(DRIP_SELL_TURNS).split(":") if x != "")
    for ch in str(DRIP_SELL_PRODUCTS):
        p = spec.PRODUCTS.index(_DRIP_NAMES[ch])
        m4 = (op[LOT4_TURN] == O.MO_SELL) & (arg[LOT4_TURN] == p)
        rem = xp.where(g, xp.sum(xp.where(m4, qty[LOT4_TURN], 0)), 0).astype(i32)
        tot = rem
        for t in turns:
            if t == LOT4_TURN:
                continue
            take = xp.minimum(rem, DRIP_SELL_LOT).astype(i32)
            same = (op[t] == O.MO_SELL) & (arg[t] == p)
            has = xp.any(same)
            free = op[t] == O.MO_NONE
            f = xp.argmax(free).astype(i32)
            can = has | xp.any(free)
            put = xp.where(can, take, 0).astype(i32)
            new = (~has) & (slot == f) & (put > 0)
            op = _row(xp, op, t, xp.where(new, O.MO_SELL, op[t]).astype(i32))
            arg = _row(xp, arg, t, xp.where(new, p, arg[t]).astype(i32))
            qty = _row(xp, qty, t, xp.where(new, put,
                                            xp.where(same, qty[t] + put, qty[t])).astype(i32))
            rem = (rem - put).astype(i32)
        moved = (tot - rem).astype(i32)
        q4 = xp.where(m4, qty[LOT4_TURN] - moved, qty[LOT4_TURN]).astype(i32)
        qty = _row(xp, qty, LOT4_TURN, q4)
        op = _row(xp, op, LOT4_TURN,
                  xp.where(m4 & (q4 <= 0), O.MO_NONE, op[LOT4_TURN]).astype(i32))
    return op, arg, qty


# ---- ENGINE_GATE: a rival-class gate for d2-29 volume switches [SWITCH, OFF]
# ENGGATE1 (2026-09-23). The band clone (V-series notebook, reacting V56 too)
# holds exactly 12 MELON tiles from d1 to d10 (200/200 LIVE250 boards read 12
# at d2); the top-10 ENGINE class commits 1-10 (REPLANTGATE census 59/60).
# At the dawn of `ENGINE_GATE_DAY` the runtime reads the other farm's melon
# tiles once and latches `opp_engine` for the rest of the game; while the latch
# is set, `engine_gate_apply(True)` writes `ENGINE_GATE_SET` ("NAME=value,..."
# -- the SW_EXTRA syntax, `;` also separates so the set rides inside an
# SW_EXTRA string, `brain.` prefix for brain names) into the modules,
# and `engine_gate_apply(False)` restores the values they held on the first
# call. Nothing moves before `ENGINE_GATE_DAY`, so a game whose gate does not
# fire -- every band game -- plays the byte-identical OFF program
# (`tests/test_engine_gate.py`). OFF, the runtime never calls either function.
# [SHIPNV1, res940_vrp7] ON: the NONV2 "M20z" arm -- latch at the d1 dawn on a
# rival with 0 MELON and >= 1 planting (V opens 12 melon: 0 fires on V56
# dev/held/FRESH300, the reacting bank and live V), then the MELONGENES plate
# rewrite of 20 tiles on d1..6.
# ---- KERNEL2: the two-kernel runtime [SWITCH, V56PACK1 2026-09-28, default OFF]
# Read only by `agent/runtime.Runtime.act` (see `runtime.kernel2_load`): step 0 = engine no-op; at step 1
# rival money <= `KERNEL2_CASH_MAX` hands the game to the embedded public V56 kernel (`agent/v56kernel.py`),
# else PFS plans its d0 from h1.  OFF, `act` is one attribute test and the planner is untouched.
KERNEL2_ON = True  # SHIP_VRP15_K2FIRE (KERNEL2 v3): with NOOP_H0=False, INHERIT=True, FIRE_CASH 26|29|2338|2438, PRELOAD=False
KERNEL2_CASH_MAX = 2550      # rival money at our step 1 (MELONHYBRID2: MELON family <= 2,550 on BAND142)
KERNEL2_H0_MERGE = True      # V56 sees a relabelled h0 obs at step 1, its h0 market rows ride step 1 (MELONHYBRID3 v56h1m)
KERNEL2_PFS_SHIFT = True     # PFS d0 plan built at h1 and played one hour late (MELONHYBRID3 pfsh1); False = pfsh1n
KERNEL2_PRELOAD = False  # SHIP_VRP15_K2FIRE: lazy V56 (STEP0TIME1); True = exec the V56 source at the step-0 no-op
# [SWITCH, STEP0TIME1 2026-09-28] KERNEL2_PRELOAD=False = LAZY V56: step 0 execs nothing V56 (PFS h0 only); the
# kernel is exec'd at step 1 only when the cash latch fires (MELON seats), never on V / ZERO-excluded seats.  Coin-exact
# either way (stdlib-only source, private RNG, fresh namespace per game).  Ship-tree gene line: KERNEL2_PRELOAD=False.
# [SWITCH, ZEROGATE1 2026-09-28, default OFF] keep the V56 kernel off ZERO-class rivals (0 melon / ~19 wheat openers).
# ZERO_BACK: at the first step >= 24 (our d1 dawn) of a game the step-1 latch gave to V56, a rival with 0 MELON plantings
# and >= ZERO_MIN_PLANTS plantings (ZERO 19-20 on BAND142 + live; the 2 flagged MELON seats that are 0m at d1 show 6/8) hands
# the farm back to PFS for the rest of the game (PFS plans d1 on the farm V56 built on d0; its ENGINE_GATE latch fires at d1).
# ZERO_CASH: an h1 exact-cash exclusion list, "|"-separated ("433|1033": the standard 0m/19w notebook opener at our no-op h0); a listed
# rival cash sends the step-1 latch to PFS.  Fingerprint only (no structural h1 tell exists: ZEROGATE1 step 1).
KERNEL2_ZERO_BACK = False
KERNEL2_ZERO_MIN_PLANTS = 12
KERNEL2_ZERO_CASH = ""
# [SWITCH, PFSH0MERGE1 2026-09-28, default OFF] remove the idle-h0 cost of KERNEL2 on seats the gate leaves to PFS.
# At the step-0 no-op PFS still runs its d0 h0 exactly as master (same plan, same per-game state) and its h0 action is
# buffered.  At step 1 on a PFS seat the buffered h0 market rows ride ahead of the plan's h1 market rows (cap 10, the excess
# carried to the next turn) and every later d0 market row plays on time; the units, which lost their h0 turn (farmer) or spawn one hour late (h0 hires), replay
# their plan rows one hour late until their first PASS row, which is skipped (unit back on schedule).  From d1 PFS is master.
# On V56 seats the buffer is dropped.  Overrides KERNEL2_PFS_SHIFT on PFS seats.
KERNEL2_PFS_H0MERGE = False
# [SWITCH, MELONHYBRID4 2026-09-28] KERNEL2_NOOP_H0 (default True = the candidate's step-0 no-op).  False: PFS plays its REAL
# d0 h0 (master; unfired seats byte-identical to master, no shift, no buffer) and the step-1 rival-cash gate hands the farm PFS
# built to the V56 kernel.  KERNEL2_INHERIT (default False; read only when NOOP_H0 is False): the kernel's step-1 turn is
# computed on a doctored obs of its own world (virgin h0 farm, then its post-h0 farm) and rewritten onto the inherited farm:
# products above the kernel's h0 net holding are sold back (PFS's 53-wheat pump -> SELL 48, the kernel keeps 5), its h0 seed
# rows are bought, hires = the kernel's hand count minus the hands on hand, its animals bought; order SELL, seeds, animals,
# hires, each clipped to the projected cash; the farmer is re-aimed at the kernel's h2 tile, existing hands PASS.  From step 2
# the kernel plays unchanged.  False: the kernel is first called at step 1 on the real obs (MELONHYBRID2 hybrid (c)).
KERNEL2_NOOP_H0 = False  # SHIP_VRP15_K2FIRE: PFS plays its real d0 h0
KERNEL2_INHERIT = True  # SHIP_VRP15_K2FIRE: the V56 kernel inherits PFS's h0 farm at step 1
# [SWITCH, KERNEL2FIRE1 2026-09-28, default OFF] the whitelist form of the step-1 gate (GATETABLE1 evidence rule E4/+1).
# "" = OFF: the legacy latch (v56 iff rival h1 cash <= KERNEL2_CASH_MAX and not in KERNEL2_ZERO_CASH), byte-identical.  Set: a
# "|"-separated list of exact rival cash values at our step 1 ("33|55|2339|2467"; conservative "55|2339|2467"); the V56 kernel fires
# iff the rival's cash is in the list, every other value (an unseen bot included) goes to PFS; CASH_MAX and ZERO_CASH are ignored.
# The values are keyed to our h0: under KERNEL2_NOOP_H0=False (real PFS h0) use the GATETABLE2 real-h0 list "26|29|2338|2438" (V3BRANCH1).
KERNEL2_FIRE_CASH = "99999"  # SHIP_VRP20_PFSOFF: no live value listed -> the latch never fires, every seat plays PFS (FIRELIVE1 OFF arm, FINALPLAN1; vrp18 = 26|29|2046|2338|2438; vrp15/vrp17 = 26|29|2338|2438; CASH_MAX / ZERO_CASH ignored)
# [SWITCH, HANDBACK1 2026-09-28, default 0 = OFF] the hand-BACK: on a seat the step-1 latch gave to the V56 kernel, at the dawn
# of day KERNEL2_HANDBACK_DAY (step D*24) the runtime stops calling the kernel and PFS's planner takes the farm V56 built
# (herd, crops mid-growth, hands, cash) for the rest of the game.  PFS replans from the observed state every dawn; the only
# runtime history it reads is the previous dawn's market inventory (brain.market_momentum), which the kernel turns record
# at each dawn while this is set, and the VRP bank/fill ledger, reset at the hand-back (as ZERO_BACK).  0 = never (byte-identical).
KERNEL2_HANDBACK_DAY = 18  # SHIP_VRP17_K2HB (PACKHB1, HANDBACK2 D18): PFS takes a V56-fired farm back at the dawn of day 18

ENGINE_GATE_ON = True
ENGINE_GATE_DAY = 1
ENGINE_GATE_MELON_MIN = 0
ENGINE_GATE_MELON_MAX = 0
ENGINE_GATE_SET = "MELON_PLATE_TILES=20;MELON_PLATE_DAY=1;NONV_PLATE_LAST=6"
#: [NONV2] the latch also needs this many rival PLANT tiles (0 = OFF, the
#: melon-only ENGGATE1 test). The d1 tell sets 1: a rival that has planted
#: nothing by the d1 dawn is undecided, not non-V.
ENGINE_GATE_MIN_PLANTS = 1
#: [ENGPLATE1] extra MELON plantings on `ENGINE_PLATE_DAY`, ADDED to the day's
#: own mix on free tiles (see `_derive`). 0 = OFF; written only through
#: `ENGINE_GATE_SET`, so it is live only in a game whose gate has latched.
ENGINE_PLATE_ADD = 0
ENGINE_PLATE_DAY = 4
#: [ENGHERD1] K: no animal purchase on days ENGINE_HERD_FROM..FROM+K (the herd
#: target stands, so they resume on FROM+K+1). 0 = OFF; written only through
#: `ENGINE_GATE_SET`, so it is live only in a game whose gate has latched.
ENGINE_HERD_DEFER = 0
ENGINE_HERD_FROM = 2
#: [NONV2] last day of the MELONGENES plate rewrite (`_melon_plate`): with
#: `MELON_PLATE_TILES` > 0 the mix of every day MELON_PLATE_DAY..NONV_PLATE_LAST
#: moves onto MELON (None = the single day, as MELONGENES). Written only through
#: `ENGINE_GATE_SET` (d1 latch), so live only in a latched game.
NONV_PLATE_LAST = None
_ENGINE_GATE_BASE = None


def engine_gate_fires(obs, player) -> bool:
    """The latch decision: `MIN <= rival melon tiles <= MAX` on this obs."""
    farms = obs.get("farms") or []
    q = 1 - int(player)
    if not (0 <= q < len(farms)):
        return False
    n = 0
    p = 0
    for row in farms[q].get("tiles") or []:
        for t in row:
            if t and t != "LOCKED" and t.get("kind") == "PLANT":
                p += 1
                if t.get("crop") == "MELON":
                    n += 1
    # [NONV2] a rival with fewer than MIN_PLANTS plantings has shown no opening
    # yet (an empty d1 farm is undecided, not non-V).
    return ENGINE_GATE_MELON_MIN <= n <= ENGINE_GATE_MELON_MAX and p >= ENGINE_GATE_MIN_PLANTS


_ENGINE_GATE_SELF = _sys.modules[__name__]


def _engine_gate_items():
    # This module is bound at import time: a file-agent opponent's
    # `_vendored_imports` swaps `sys.modules` while the engine runs.
    mod = _ENGINE_GATE_SELF
    out = []
    for item in str(ENGINE_GATE_SET).replace(";", ",").split(","):
        item = item.strip()
        if not item:
            continue
        name, sep, raw = item.partition("=")
        if name.startswith("brain."):
            from . import brain as m
        else:
            m = mod
        name = name.removeprefix("brain.")
        if not hasattr(m, name):
            raise AttributeError(name)
        val = True
        if sep:
            if raw in ("True", "False"):
                val = raw == "True"
            else:
                try:
                    val = int(raw)
                except ValueError:
                    try:
                        val = float(raw)
                    except ValueError:
                        val = raw
        out.append((m, name, val))
    return out


def engine_gate_apply(on: bool) -> None:
    """Write the ENGINE-mode values (on) or restore the base ones (off)."""
    global _ENGINE_GATE_BASE
    items = _engine_gate_items()
    if _ENGINE_GATE_BASE is None:
        _ENGINE_GATE_BASE = [(m, n, getattr(m, n)) for m, n, _ in items]
    if on:
        for m, n, v in items:
            setattr(m, n, v)
    else:
        for m, n, v in _ENGINE_GATE_BASE:
            setattr(m, n, v)


# ---- Q4_VRP: fourth quadrant funded by the VRP bank [SWITCH, Q4VRP1, OFF] ---
# The runtime (runtime.Runtime.act / S/simgap1/ourseat) sets Q4_VRP_RELEASE =
# min(banked VRP saving, Q4 price) at dawn while nquad == 3 in the window, and
# takes the released coins off the bank on the day the plan carries BUY_LAND.
Q4_VRP_ON = False
Q4_VRP_DAY = 10                 # first day of the buy window
Q4_VRP_LAST = 20                # last day of the buy window
Q4_VRP_RESERVE = 0              # coins the funded purse must keep after the land
Q4_VRP_FUND = "true"            # "true" = visible purse + bank release; "visible" = visible purse only
Q4_VRP_RELEASE = 0              # set per dawn by the runtime (traced scalar in the sim)

# ---- Q4_PROG: DSM's fourth-quadrant program [SWITCH, Q4PROG1, OFF] ---------
# DSMLAND2 (2026-09-23): the rank-1 sub buys Q4 on d10 (126/126) and works ~17
# of its 25 tiles with a wheat relay + strawberry/carrot/tomato, +1 hand d10-26.
# OFF, none of the three `if Q4_PROG_ON` blocks exists (tests/test_q4_prog.py).
Q4_PROG_ON = False
Q4_BUY_DAYS = (10, 15)          # buy window (first day the purse covers it)
Q4_PLANT_LAST_DAY = 26          # last day the program plants
Q4_BUY_KEEP = 0                 # coins the purse must keep after the land
Q4_EXTRA_HANDS = 0              # hands above the argmax while Q4 is owned
Q4_HIRE_CAP = 12                # max hires/day while Q4 is owned (0 = no cap)
Q4_HIRE_DAYS = (10, 26)
#: target Q4 census (WHEAT, CARROT, TOMATO, STRAWBERRY, MELON) from a day on
Q4_TARGETS = ((10, (4, 1, 0, 0, 0)), (11, (6, 1, 0, 0, 0)), (12, (8, 2, 0, 2, 0)),
              (13, (8, 3, 1, 3, 0)), (14, (8, 3, 2, 3, 0)), (15, (8, 3, 3, 3, 0)))
#: named variants, selectable as `Q4_TARGETS=<name>` through the switch string
Q4_PRESETS = {
    "DSM": Q4_TARGETS,
    "LAND": ((10, (0, 0, 0, 0, 0)),),
    "W8": ((10, (4, 0, 0, 0, 0)), (11, (6, 0, 0, 0, 0)), (12, (8, 0, 0, 0, 0))),
    "W4C2": ((10, (4, 1, 0, 0, 0)), (12, (4, 2, 0, 0, 0))),
    "W8C3": ((10, (4, 1, 0, 0, 0)), (11, (6, 1, 0, 0, 0)), (12, (8, 2, 0, 0, 0)),
             (13, (8, 3, 0, 0, 0))),
}
Q4_SEED_ORDER = (spec.I_WHEAT, spec.I_CARROT, spec.I_STRAWBERRY, spec.I_TOMATO,
                 spec.I_MELON)


def _q4_table():
    """int[30, N_CROPS]: the Q4 target census per day (0 before the first row)."""
    t = np.zeros((30, spec.N_CROPS), np.int32)
    rows = Q4_PRESETS[Q4_TARGETS] if isinstance(Q4_TARGETS, str) else Q4_TARGETS
    for d0, row in sorted(rows):
        t[int(d0):] = np.asarray(row, np.int32)
    return t
