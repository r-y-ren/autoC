# Why the route model cannot bank mid-day, and the smallest change that fixes it

2026-09-04. Worktree `.claude/worktrees/agent-a8dce00ba55b029cc`, branch
`fitness-shaping` off `854b86b`. Probes `S/mp/probe1.py`, `S/mp/probe2.py`,
`S/mp/probe3.py`. Prior reports: `scratchpad/topopen/report.txt` (12 of 72
melon units reached the day-10 market), `scratchpad/topaut/report.txt` (the top
tier dumps 72 melon on day 10 at ~246 where we reach the pot on day 14 at ~161),
`scratchpad/melonlot/report.txt`.

## 0. The question, restated against the engine

The brief asks for melon "planted early enough that the harvest is ready to
sell on day 10". There is no room in the planting: melon's
`CROP_FIRST_YIELD_DAY` is **10** (`src/kagg3/spec.py:47`) and its
`CROP_SATURATE_AGE` is also 10 (`spec.py:73`), and the harvest guard is
`age >= c_first` (`src/kagg3/sim/units.py:143`, engine
`kaggriculture.py` `HARVEST`). A melon planted on day 0 -- the earliest day
there is -- **cannot be harvested before day 10 at all**, and the turn within
day 0 that the PLANT lands on is irrelevant, because age is counted in days
(`age = day - t_day[tile]`, `units.py:120`). Day 0 already plants the twelve
tiles under `MELON_OPEN_ON` / `OPEN_DENY_ON` and they already reach the tape's
own 72 units (`scratchpad/topopen/report.txt`, "d10 h... ours 72u").

So the real question is the one the topopen run actually hit: **can day 10's
own harvest reach day 10's market?** With nothing else done it cannot. The free
banking is `_end_of_day` -> `_drop_inventories_to_shed`
(`src/kagg3/sim/eod.py`, engine `kaggriculture.py:843-892`), which runs after
turn 23, so the harvest is first sellable at day 11 hour 0. Anything sold on
day 10 has to be put in the shed by a unit, mid-day, on purpose.

## 1. Which turn(s) the planner emits a mid-day deposit on

`OP_PLACE` is emitted by exactly one rank kind today: an **animal** onto a free
coop/pasture (`src/kagg3/core/plan.py:4356`, the `m_place` chain row). It is
never emitted as a shed deposit. Mid-day banking is `OP_DROP` only, in two
places inside `_routes`:

* `plan.py:6020-6038` -- the `drop_day` return leg (`DROP_ON`; day 29, and day
  28 under `MIDDAY_DROP_ON`): walk home after the block's **last** rank, DROP,
  stop.
* `plan.py:6040-6066` -- the excursion: walk out, DROP, walk back, carry on.
  Two triggers feed it, `MELON_OPEN_ON`'s crop trigger (`plan.py:5744-5755`)
  and `BANK_BEFORE_LOT_ON`'s time-and-value trigger (`plan.py:5760-5790`), and
  they are mutually exclusive by assertion (`plan.py:1676`).

Measured turns, twelve standing melon on the day they saturate
(`S/mp/probe1.py`, `S/mp/probe2.py`, fixture `tests/test_melon_open.py`
`_melon_view`, `MELON_OPEN_ON` on, `MELON_LOT_TURNS = (11, 13, 15)`):

| board | crew 4 | crew 6 | crew 8 | crew 11 |
|---|---|---|---|---|
| melon on tiles 0..11 (`DIST_SHED` 4..8) | DROP 11, 16 | 11, 16 | 11, 16 | **none** |
| melon on the 12 tiles nearest a shed access (`DIST_SHED` 0..1) | DROP 22, 22 | 22, 22 | 22, 22 | 10, 19, 20 |

Two DROPs on a twelve-tile board, and on the near-shed board -- which is
exactly where `_derive`'s `near_rank` puts the melon under `MELON_OPEN_ON`
(`plan.py:4306-4324`) -- they land on **turn 22**, after every row of the day.
That is the 12-of-72 the topopen run saw, in miniature.

## 2. What blocks an earlier deposit

Six things, in the order they bind. Distance is not the first of them.

1. **The rank rule, and this is the wall.** `MELON_OPEN_ON`'s excursion fires
   after the block's **last** melon rank -- `plan.py:5751`,
   `m_ins = max{ j in [s, end2] : kmel[j] }`. The deposit therefore lands at
   `start_u + cu[m_ins] + DIST_SHED[m_ins]`, i.e. after the *whole prefix of
   the block* up to and including its final melon tile. Moving the melon next
   to the shed makes that prefix cheaper to walk, so the block eats more ranks
   before it reaches its last melon and the deposit lands **later** -- turn 22
   instead of turn 11, which is precisely what the table above shows.
   `MELON_OPEN_ON` has no time rule of any kind.
2. **One excursion per unit per day.** `ins` is a single scalar window per unit
   (`plan.py:5730`), the clock is paused once (`plan.py:5865-5870`) and the
   decode writes one leg (`plan.py:6040-6066`). A unit holding several melon
   tiles banks them in one trip or not at all. This is the "second block per
   unit" the `MIDDAY_DROP_ON` post-mortem named as the prerequisite
   (`plan.py:377-380`) and it is still not there.
3. **The reserve is charged against the whole block.** `res = 2 * DIST_SHED + 1`
   is subtracted from the turn budget and the block is **recut**
   (`plan.py:5747-5749`); the excursion is taken only if the recut still holds
   a melon rank. On a far tile that is up to 17 of a ~22-turn budget, so the
   recut drops the melon and the excursion is refused outright -- which is why
   crew 11 on the far board banks nothing.
4. **OP_DROP dumps the whole inventory** (`units.py:96-105`; engine
   `kaggriculture.py:343-356`) and destroys the part past `SHED_CAPACITY` 100.
   `BANK_BEFORE_LOT_ON` therefore has to refuse any block that still owes a
   PICKUP-fed op after the rank (`plan.py:5772-5777`, `after <= 0`), and its
   own census puts that at 28% of unit-days -> 3% (`plan.py:955-963`).
5. **A deposit needs shed adjacency** (`units.py:96`, engine
   `kaggriculture.py:344` and `:393`) -- there are four shed-access tiles on a
   10x10 board and `DIST_SHED` runs 0..8 (`S/mp/probe2.py`:
   `bincount = [4 8 12 16 20 16 12 8 4]`).
6. **The simulator did not model the engine's PLACE-to-shed path at all.**
   `units.py`'s `do_place` was `(op == OP_PLACE) & free_st & (k == a_struct)`
   -- animal placement only -- so an `OP_PLACE` with a product argument was a
   silent no-op in the simulator while the real engine banked it
   (`kaggriculture.py:377-408`). Nothing could be measured, trained or tested
   in-sim until that branch existed.

Not a blocker, checked and dismissed: `assert_no_cross` / the schedule asserts
(`ops.py:261-337`) say nothing about a unit-phase deposit; the BUY row and the
crew ramp do not gate it (a deposit consumes no market slot and no seed); the
seed arrival timing is a day-0 question and day 0's plant is already the tape's.

## 3. The smallest change: `MIDDAY_PLACE_ON`

Two halves, both local, no new row type and no route-model rewrite.

**(a) The time rule** (`plan.py`, in the `melon is not None` block). A melon
rank is a candidate only if its deposit lands on or before
`O.MELON_LOT_TURNS[MIDDAY_PLACE_LOT]` -- `start_m + cu + DIST_SHED <= 11`,
where `start_m = route_base + d_lead[end] - early_u` is the unit's own first
turn. Among the survivors the excursion still goes after the **largest** rank,
so it banks the most melon the window can hold in front of the row that sells
it. This is `BANK_BEFORE_LOT_ON`'s existing `drop_t <= O.SELL_TURNS[BANK_LOT]`
rule (`plan.py:5771`) moved onto the melon trigger; the melon tuple gains a
third element, the crew's start turn, which is the same quantity `bank` already
passes.

**(b) The op.** The deposit becomes `OP_PLACE(MELON, qty)` instead of
`OP_DROP`. The engine's PLACE banks `min(qty, inv[item])` of one item, obeys
`shedCapacity`, and **leaves the remainder on the unit**; DROP dumps everything
and destroys the overflow. So a mid-block deposit stops voiding the block's
carried feed wheat and fertilizer -- rule (4) above disappears -- and the dump
day's 72 units cannot destroy shed stock on the way in. It costs the same one
turn, so the excursion's price does not move. `agent/render.py:26-27` already
renders `["PLACE", item, qty]`, so nothing changes on the wire.

**(c) The simulator's PLACE-to-shed branch** (`sim/units.py`), unconditional
and inert -- nothing but this switch emits `OP_PLACE` with a product item. The
animal branch is decided once, in the shed stage, and re-used by the tile
stage, so the two are exactly complementary as they are in the engine; the
per-(unit, item) taken amounts are scattered back out of the capacity cumsum
because DROP loses the whole load whether it fit and PLACE loses only what fit.

### What it buys, measured at the planner (`S/mp/probe3.py`)

Twelve standing melon, `MELON_OPEN_ON` on, deposits by turn (the first melon
row is turn 11 / engine hour 12):

| board | crew | OFF | ON |
|---|---|---|---|
| far (`DIST_SHED` 4..8) | 4 / 6 / 8 | DROP 11, 16 | PLACE 11 |
| far | 11 | none | none |
| **near (`DIST_SHED` 0..1)** | 4 / 6 / 8 | DROP **22, 22** | PLACE **9, 11** |
| **near** | 11 | DROP 10, 19, 20 | PLACE **10, 10, 11** |

On the board `MELON_OPEN_ON` actually builds, every deposit moves in front of
the first melon row: 0 of 2 become 2 of 2, and 1 of 3 becomes 3 of 3. On the
far board the switch trades the late second DROP for one on-time PLACE, which
is the rule doing what it says -- a deposit that cannot make the row is not
taken.

### What it does NOT buy, and what would

It does not give a unit a **second** trip. Blocker (2) stands: one melon lot of
twelve tiles spread over three or four blocks still banks at most one trip's
worth per unit, and the twelve tiles are not all banked before hour 12. Getting
all 72 units in front of the top tier's hour-8 dump needs a melon-dedicated
route tier -- one block per melon tile, or a per-rank excursion -- which is the
route-model rewrite the brief allowed me to stop at, and it is where the next
attempt should start. Estimate: `_routes`' per-unit loop (`plan.py:5669`) would
have to carry a list of `(t_ins, ins)` windows instead of the scalar pair it
carries now, and `t_ins`/`rr` (`plan.py:5860-5866`) would become a cumulative
shift rather than a single step -- roughly the size of `BANK_BEFORE_LOT_ON`
itself, plus a re-pricing of the reserve, so a day of work rather than an hour.

And it says nothing about whether the melon opening is worth playing: that is
`MELON_OPEN_ON`'s question and today's answer is -14,289 a game
(`plan.py`'s `OPEN_DENY` block), with the whole of the top tier's measured edge
on our four-opponent panel already collected by `OPEN_PUMP_ON`
(`scratchpad/topopen/report.txt` section 2c).

### Measured in the simulator (`tests/test_midday_place.py::_sim_shed_by_turn`)

Twelve ripe melon (72 units) on the near-shed board, the planner's own day-10
route played through `sim.units.apply_units` for the 24 unit turns, no market
and no end-of-day. Our shed's melon count at the first melon row (turn 11,
engine hour 12):

| crew | OFF | ON |
|---|---|---|
| 4 | **0** | **30** |
| 6 | **0** | **30** |
| 8 | **0** | **30** |
| 11 | 12 | **36** |

Out of 72. The remainder rides in the hands to `_end_of_day` in both arms, as it
always did; what changes is how much of it is sellable while day 10's rows are
still open. Blocker (2) is exactly the gap between 30 and 72.
