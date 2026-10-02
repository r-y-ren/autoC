# PRESTOCK-REPAIR — the switch is legal now, and it does not reach the turns

**VERDICT — NOT PROMOTABLE, and for a reason that closes the family rather than
the arm. The 68-band pooled Δcoins is −326 (t −1.92), Δmargin −355 (t −1.60):
NOT ≥ +450 at t ≥ 2, and negative.** The repair itself works — `PRESTOCK_V2_ON`
runs beside the shipped `EARLY_SELL_ON` and `OPEN_PUMP_ON` with no assert
deleted and no assert fired, so the family finally has a real read instead of
the 2026-09-10 VOID lines. What that read says is that the schedule half is
**unreachable**: the arm that keeps the crew-start law and drops the purchase
(`PRESTOCK_V2_BUY_ON=False`) is **byte-identical to OFF on all 80 boards, max
|delta| = 0 over every recorded array**, because the day's residual BUY row is
never empty — *seeds and animals ride that row too* and B buys seed nearly every
day. With the purchase on, the row empties on ≈0.3 day-rows a game: **h0-h1 PASS
falls 266.3 → 263.7, 2.6 of the 266.3 turns TURNS priced at 4,665 coins, 1 %.**
The switch pays 1,040 coins/game of extra wheat and buys 6.3 worked turns.

All sim-descriptive: CRN sim, tape-action opponent seat, pinned towns,
`shop_crn`, theta `flow193_g100_hr` (= B), switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON`, 12 ymg_aq boards +
68 band boards (TOPB2 40 + LIVE-C 28), both seats of every town. **No engine
game, no ES arm, no promotion gate.** Baselines are the on-disk OFF raws
(`raw_headOFF.npz`, `raw_melOFF.npz`).

## 1. Why each assert exists, and the minimal legal reconciliation

Neither assert is about the purchase. **Both subjects are `hire_wide_early`.**

| assert | file:line | what breaks |
|---|---|---|
| `not (EARLY_SELL_ON and (MARKET_PACK_ON or PRESTOCK_ON))` | `plan.py:2584` | `EARLY_SELL` mode "A" **gathers lot 1 into the free slots of the turn-1 BUY row** (`_market`, "lot 1 behind the BUY row", `plan.py:8740+`). `PRESTOCK` moves the overflow HIRE row **into turn 1** on exactly the days that row is free, and writes the whole row rather than merging (`_market`'s `hire_wide_early` branch, `plan.py:8727+`: `op = _row(..., O.TURN_BUY, where(early, h_op, op[O.TURN_BUY]))`). Two writers, one row; the lot would be overwritten in silence. |
| `not (MARKET_PACK_ON and PRESTOCK_ON)` | `plan.py:2435` | `MARKET_PACK` **empties** turn 1 (both rows go out at turn 0) and `PRESTOCK` **fills** it. One row cannot be in two places, and both move `route_base` off the law's value. |
| `assert hire_wide_early is None, "OPEN_PUMP owns turn 1"` | `plan.py:8612` (trace time) | `OPEN_PUMP`'s **sell-back leg is index 0 of that same turn-1 row** (`plan.py:8705+`). `pump` is never `None` with the switch on (set unconditionally, zero-valued on days it declines) and `hire_wide_early` is never `None` with `PRESTOCK_ON`, so this fires on **day 0 of every game** and the seat idles on 3,000 coins. That is the −154,871 "read" in `S/topb/screen_summary.txt:15,18`. |

**The turn-20 purchase row collides with nothing.** `ops._check_schedule`
(`ops.py:290-304`) already pins `SELL_TURNS[-1] < TURN_PRESTOCK < TPD-1`, out of
`SELL_TURNS`, out of `MELON_LOT_TURNS`.

**The minimal legal reconciliation is not to move the prestock row behind the
early-sell/pump rows, and not to reserve a purse — it is to give up the wide
day.** `hire_wide_early` re-seats `rest = max(n_hire - MO, 0)`, which is **zero
for a crew of ten or fewer**: on a narrow day there is no overflow row and
nothing to move. So V2 gates the whole switch on `~wide` and passes
`hire_wide_early=None`. Turn 1 then keeps exactly the writers it has today (the
BUY row, the pump's sell-back, `EARLY_SELL`'s lot 1), both asserts lose their
subject, and **no assert is deleted or weakened**. The cost is the wide-day
version of the law (`ROUTE_BASE_WIDE_PRE` = 2), which was never safe anyway: a
unit stepping at turn 2 re-scatters every hand the turn-2 HIRE row spawns
[LAW, `ops.ROUTE_BASE_WIDE`] — the mechanism that cost `ROUTE_EARLY` −142,588
(`2026-09-11-route-early-bug.md`).

`route_base` moving to `O.ROUTE_BASE_PRE` switches `route_split` off for that
day by `route_split`'s own gate (`plan.py:6907`, `route_base == where(wide,
ROUTE_BASE_WIDE, ROUTE_BASE)`), so the turn is **handed over, never taken
twice** — the `early` vector is applied once, which is the whole of the
`ROUTE_EARLY` defect.

## 2. What was built (default-off, `plan.py`)

| site | line | what |
|---|---|---|
| `PRESTOCK_V2_ON = False` | `plan.py:2144` | master switch, new constant; `PRESTOCK_ON` untouched |
| `PRESTOCK_V2_FARMER0_ON = False` | `plan.py:2171` | the farmer's hour 0 |
| `PRESTOCK_V2_BUY_ON = True` | `plan.py:2185` | sub-switch: `False` = the schedule half alone, no order at `TURN_PRESTOCK` |
| day predicate `pre_v2` | `plan.py:6812` | `_prestock_ok(day) & (_buy_row_units(d) == 0) & (~wide)`; `route_base = where(pre_v2, O.ROUTE_BASE_PRE, route_base)` |
| `farmer0` | `plan.py:6874` | `pre_v2 & (land_lead == 0)` |
| `_routes` early cut | `plan.py:8036` | unit 0 only, and the block must **owe** a PICKUP (`d_pick[e1] > 0`): the turn it buys is spent **standing still** on the shed-access tile, the one turn-0 op the spawn law allows. `route_split`'s narrow branch wants `d_pick[e1] == 0`, so the two sets are disjoint and the `maximum` is a union |
| one shift | `plan.py:7243` | `start_u -= early` / `walk_u += early` applied **once**, whichever switch produced `early`; `pk_base` follows for unit 0 |
| purchase | `plan.py:7697` | `if PRESTOCK_ON or (PRESTOCK_V2_ON and PRESTOCK_V2_BUY_ON)`, reusing `_prestock` unchanged (wheat + fertilizer, `PRESTOCK_SEEDS` still off) |
| `sim/rollout.py:67,389` | | `TURN_PRESTOCK` joins the full-market-row set under V2 too, else the sim drops the row in silence |

Hire enumeration credited with V2's crew turn on the **narrow candidates only**
(`h <= MO`, a Python-time test). The farmer's turn is deliberately **not**
credited: one unit-turn is inside the estimate's noise and under-admission is
the repairable error.

**Tests.** `JAX_PLATFORMS=cpu python -m pytest tests/test_macro_exec.py
tests/test_rebuy.py tests/test_prestock_v2.py -q` → **43 passed** (37 + 6 new).
`tests/test_prestock_v2.py` has six: nothing at `TURN_PRESTOCK` off; **the whole
plan tuple hashed against a pristine `git archive HEAD src` tree built in a
subprocess** on four boards (this is the OFF-identity receipt); the morning
schedule off; ON runs beside `EARLY_SELL_ON` + `OPEN_PUMP_ON` and puts no HIRE
in turn 1; h0-h1 PASS drops on the `stocked` board (4 → 2 with V2, → 1 with
FARMER0); the row's cost never exceeds the day's money at money ∈ {0, 120, 600,
3k, 20k}.

*Pre-existing, not mine:* `tests/test_route_split.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner`
and `::test_on_leaves_every_market_row_untouched` fail **at HEAD** too (verified
on the pristine archive: `2 failed, 10 passed, 3 skipped`).

## 3. The paired ledger (ON − OFF, same CRN boards, both seats)

| arm | set | n | our coins Δ (t) | margin Δ (t) | their coins Δ (t) | wins | flips |
|---|---|---:|---:|---:|---:|---:|---:|
| **V2** | ymg_aq | 12 | **−789** (−1.33) | **−870** (−1.96) | +81 (+0.25) | 0→0 | +0/−0 |
| **V2** | **band pooled** | **68** | **−326** (−1.92) | **−355** (−1.60) | +28 (+0.21) | 29→27 | +2/−4 |
| V2 | band TOPB2 | 40 | −327 (−1.17) | −323 (−0.88) | −4 (−0.02) | 13→11 | +2/−4 |
| V2 | band LIVE-C | 28 | −326 (−3.05) | −400 (−3.04) | +74 (+0.45) | 16→16 | +0/−0 |
| **V2 + FARMER0** | ymg_aq | 12 | −789 (−1.33) | −870 (−1.96) | +81 (+0.25) | 0→0 | +0/−0 |
| **V2 + FARMER0** | band pooled | 68 | −326 (−1.92) | −355 (−1.60) | +28 (+0.21) | 29→27 | +2/−4 |
| **V2 schedule half only** | ymg + band | 80 | **+0** | **+0** | **+0** | — | +0/−0 |

**The 68-band pooled Δcoins is −326 with t −1.92. It is NOT ≥ +450 at t ≥ 2.**

The two halves were measured separately (task item 4) and the answer is that
only one of them exists:

* **V2 + FARMER0 is byte-identical to V2** on all 80 boards. The farmer's hour-0
  PICKUP **never fires on a real board**: it needs a `pre_v2` day (narrow, empty
  residual row) whose unit-0 block owes a pickup, and there are ≈0.3 `pre_v2`
  day-rows a game to begin with. It is demonstrably live in the planner —
  `tests/test_prestock_v2.py` moves unit 0's first act 2 → 1 → 0 and h0-h1 PASS
  4 → 2 → 1 on the `stocked` fixture — so this is a reachability result, not a
  dead gene.
* **The schedule half alone changes nothing at all**, max |delta| = 0 over every
  recorded array on both board sets. Without the prestock purchase the residual
  BUY row is **never** empty on a narrow day.

## 4. Turns recovered: 2.6 of 266.3 (`S/turns` instrument, 12 ymg_aq boards)

| arm | worked turns/game | active turns/game | h0-h1 PASS | h0 PASS | h1 PASS | h2 PASS |
|---|---:|---:|---:|---:|---:|---:|
| OFF (B) | 5,986.4 | 6,673.4 | **266.3** | 30.0 | 236.3 | 24.1 |
| V2 + FARMER0 | 5,992.7 | 6,675.5 | **263.7** | 30.0 | 233.7 | 23.8 |

**+6.3 worked turns/game.** TURNS priced the block at 4,665 coins and 266.3
turns; V2 reaches 1 % of it. The 6.3 turns at B's realised 17.52 coins/turn are
worth +110, against −326 of measured loss, so **the turns do not even have the
chance to convert** — the loss is the purchase.

**Where the purchase goes (68 band boards, per game):** wheat bought 145.7 →
171.9 units, 4,973 → 6,013 coins — **+26.2 units, +1,040 coins a game** for
+6.3 turns. Their coins move +28 (t +0.21), so this is not the 2026-08-30
"we both got richer" externality; it is our own purse, spent a day early at a
quote the projection said was cheaper and a day of compounding said was not.

## 5. Why the schedule law is unreachable — the mechanism, stated

`_buy_row_units` (`plan.py:3306`) counts **wheat + fertilizer + animals +
seeds**, and its docstring says why seeds must count: *"a seed bought at turn 1
is credited after that turn's unit phase, so a unit that PLANTs at turn 1 would
plant nothing."* `PRESTOCK_SEEDS` is **off and measured-rejected** (−90,863 mean
margin, 0/24 games, `plan.py:2102`+): planting fills free land once, so
"tomorrow plants what today planted" is exactly wrong on the day the land fills.

So the prestock can empty the wheat and fertilizer slots and **never** the seed
slot, on any day B plants — which is nearly every day. Add the narrow gate and
the reachable set is ≈0.3 day-rows a game:

* **45.9 % of B's day-rows hire more than 10 hands** (measured here off
  `raw_headOFF`/`raw_melOFF` `hire_n` diffs: mean 8.72 hires/day, 11.0-12.0 from
  day 12 on) — every one of those is a wide day V2 declines.
* Of the narrow rest, a day is only `pre_v2` if it buys **no seed and no
  animal** either.

**That is the family's blocker, and it is not an assert.** The 266 morning turns
are not behind `PRESTOCK`; they are behind the **seed row**, and the seed row
has its own measured refusal.

## 6. Next

1. **Do not spend an engine leg on V2.** It is default-off and reconciled; leave
   it in the tree as the legal read the family never had.
2. **The 266 turns are still open, and `PRESTOCK` is the wrong lever for them.**
   The reachable attack is the one `_buy_row_units` names: a **per-kind** morning
   wait instead of a per-day one. `route_split` already starts a block that owes
   the BUY row nothing; what is missing is the block that owes it **only seed**
   (PLANT is the one op the row feeds, `plan.py:8028`, `free_first`). A
   `SEED_LEAD`-style rule — blocks whose first op is not PLANT start at
   `TURN_BUY` even on a day that buys seed — needs no purchase, no purse and no
   turn-1 row, and it is the 88 %-of-hour-1 that `ROUTE_SPLIT_ON` already proves
   safe. Cost: one gate widening at `plan.py:6907`, one paired ledger.
3. **The smaller crew (350.6 turns) is the larger half of the 695** and is
   untouched by any of this: `2026-09-14-turns.md` §5 prices three hands at d10
   at ~1,150 coins/day of net market against a 239-coin bill. The binding thing
   is the hire enumeration's value model, not the wage.
4. If anyone re-opens `PRESTOCK_SEEDS`, the prerequisite is still the one the
   2026-08-30 autopsy names: **a bound on tomorrow's plantable slots**, not on
   today's plantings.

## 7. Files

Scripts/logs `S/prestock/{launch.sh,launch2.sh,report.py,turns_cmp.py,
pv2.log,pv2_band.log,pv2f.log,pv2f_band.log,pv2s.log,pv2s_band.log,
turns_pv2_ymg.log}`; raws `S/macro_exec/raw_prestock_{pv2,pv2_band,pv2f,
pv2f_band,pv2s,pv2s_band}.npz` and `S/turns/raw_pv2_ymg.npz`; code
`src/kagg3/core/plan.py`, `src/kagg3/sim/rollout.py`,
`tests/test_prestock_v2.py`.
