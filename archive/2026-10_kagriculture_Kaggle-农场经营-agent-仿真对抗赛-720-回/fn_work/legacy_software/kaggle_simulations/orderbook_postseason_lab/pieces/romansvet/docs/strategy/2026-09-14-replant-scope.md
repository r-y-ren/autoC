# REPLANT-SCOPE: does B replant inside the day, and what does the idle cost?

**VERDICT: B ALREADY same-day replants, 95.0 tiles/season (12 ymg_aq boards)
and 94.2 (20 band boards), against the tape opponent's 159.0 (ymg_aq) and
147.6 (band clone) — the planner's own free-slot set is `is_empty | is_weed |
harvest_one` (`plan.py:5501`) and `brain.n_free_slots` counts the same
`harvest_one` tiles (`brain.py:186`), so a tile the day will harvest is
developable at that dawn and the harvest→replant pair is scheduled one hour
apart (B's gap is *exactly* 1 h on 95 of 95; ymg_aq's mean is 2.20 h).  B's
post-harvest idle is 4,124 tile-hours/board (ymg set) and 4,641 (band) against
the opponent's 2,460 / 2,682 — but 92 % of it is d20-29 (3,808 / 4,253); over
d0-d19 B idles 316 / 388 tile-hours against the opponent's 661 / 549, i.e. B is
*tighter* than both tapes before d20.  Hands and cash are both available: 10.3 %
of unit-turns are PASS (hours 4-12 are 0.0-0.6 % — fully booked; the slack is
hours 19-23), and at h=12 on d20-27 B holds 59,791 coins against a 136-coin
wheat bill for every tile it frees and does not replant.  **Do not build the
default-off second development pass**: the freed-but-not-same-day-replanted
tiles are 46.2/season, of which only 10.0 fall in d0-d19 and 22.6 fall on d28-29
where replanting is correctly dead. The two sites that hold the real tiles are
`plan.py:5313` / `brain.py:185` (`harvest_age = clip(VAL.pay_day() - t_day,
c_first, c_sat)` — ymg_aq takes wheat at age 2 and B at 3-4, which is the whole
of DEV-SLOPE's "11.3 tiles from a 6-tile dawn" on d2) and the late-season
planting stop (B plants 53.6 tiles on d20-27 against ymg_aq's 82.7).**

All sim-descriptive: CRN sim, tape-action opponent seat, pinned towns,
`shop_crn`, theta `flow193_g100_hr` (= B), the same runner as DEV-SLOPE /
MACRO-EXEC. No engine game, no ES arm, no promotion gate, and **no coin claim**
— this leg measures tile-cycles, hand-turns and coins-on-hand only.

Tools: `S/replant/{instrument.py,tape_replant.py,report.py}`; raws
`raw_ymg.npz` (12 ymg_aq boards, both seats), `raw_band.npz` (20 of the 68
TOPB2/LIVEC band boards, both seats), `tape_ops.npz`; full output
`S/replant/report_ymg.md`, `report_band.md`, `tape_replant.log`.

**Method.** `S/replant/instrument.py` is `S/dev_slope/ledger.py` with one
addition: `kagg3.sim.units.apply_units` is wrapped (nothing under `src/` is
edited), so every turn of every day is observed *inside* the day for both
seats. Per-turn tile ids are not recorded by the tape (a unit acts on the tile
it stands on and the tape carries only ops), so PLANT and HARVEST are derived
from the tile-state transition across the unit fold: a tile whose `kind`
becomes `KIND_PLANT` during turn h was planted at h, one that stops being
`KIND_PLANT` was freed at h (an *ongoing* crop — tomato, strawberry — keeps its
tile on harvest and is correctly not counted as freeing one). Tiles freed
between turns (`decay_plants`, eod) are counted separately. A **same-day
replant** is a tile planted at hour h that was freed at an hour < h the same
day. `S/replant/tape_replant.py` reads the tapes directly
(`artifacts/tape_actions_town/<ep>.npz`, the files `S/macro_exec/extract.py`
reads) as an op-level cross-check.

## 1. Same-day replanting (Q1)

Board means. "OPP" is the tape seat: ymg_aq on the ymg set, the band clone on
the band set.

| set | B freed | B planted | **B same-day replants** | OPP freed | OPP planted | **OPP same-day** |
|---|---:|---:|---:|---:|---:|---:|
| 12 ymg_aq boards | 141.2 | 184.2 | **95.0** | 220.5 | 240.4 | **159.0** |
| 20 band boards | 147.7 | 184.3 | **94.2** | 206.1 | 229.8 | **147.6** |

B's decay-freed tiles (crops lost to eod/weeds rather than harvested) are 32.2 /
31.3 against the opponent's 11.8 / 20.6. Op-level counts agree with the tape:
`tape_replant.py` reads 241.3 OP_PLANT per ymg_aq season against the sim's
240.4 tiles actually put down, and 212.7 of those plants fall after the day's
first harvest.

Harvest→replant gap, same-day replants only (season totals, board mean):

| gap (h) | B (ymg set) | ymg_aq | B (band set) | band clone |
|---|---:|---:|---:|---:|
| 1 | **95.0** | 126.2 | **94.2** | 125.0 |
| 2-7 | 0.0 | 24.6 | 0.0 | 5.7 |
| 8-22 | 0.0 | 8.2 | 0.1 (at h 19) | 16.9 |
| **mean** | **1.00** | **2.20** | **1.02** | **2.66** |

**Every one of B's same-day replants is exactly one hour after the harvest.**
That is the signature of the dawn plan, not of a re-plan: `_derive` puts the
HARVEST and the PLANT of the same tile in consecutive turns of the route it
builds at dawn. ymg_aq's spread gap is the signature of a live re-plan. The
full harvest→replant latency (any replant, not just same-day) is B 9.36 h vs
ymg_aq 4.76 h, and B's tail is the 9.4 replants/season at 47 h+ — tiles left
for the next dawn or later.

Per-day, the ymg set (the days DEV-SLOPE §2 flagged):

| day | B freed | B planted | B same-day | ymg freed | ymg planted | ymg same-day |
|---|---:|---:|---:|---:|---:|---:|
| d0 | 0.00 | 19.00 | 0.00 | 0.00 | 14.00 | 0.00 |
| **d2** | **0.00** | **0.00** | **0.00** | **12.00** | **11.33** | **11.00** |
| d3 | 8.00 | 7.00 | 7.00 | 0.00 | 6.00 | 0.00 |
| d4 | 11.00 | 10.67 | 10.67 | 11.33 | 9.83 | 9.83 |
| d6 | 0.00 | 5.17 | 0.00 | 6.83 | 20.08 | 6.67 |
| d8 | 5.67 | 5.75 | 3.17 | 0.00 | 9.67 | 0.00 |
| d10 | 0.67 | 11.17 | 0.50 | 8.50 | 11.33 | 7.67 |

**This is the correction to DEV-SLOPE §5.2.** Its d2 line ("ymg_aq plants 11.3
tiles from a 6-tile dawn — no theta value can express that, it is a planner
change") is right about the coins and wrong about the mechanism. On d2 ymg_aq
frees 12 tiles and replants 11 of them; B frees **zero** on d2 — not because it
cannot see a mid-day tile, but because its own wheat is not ripe by its own
rule. `harvest_age = clip(VAL.pay_day() - t_day, c_first, c_sat)`
(`plan.py:5313`, mirrored at `brain.py:185`) is 4 for wheat away from the
horizon; ymg_aq harvests at `CROP_FIRST_YIELD_DAY` = 2. B's d0 planting of 19
tiles comes free on d3 (8) and d4 (11) and is replanted the same hour both
times. So the gap on d2 is a **turnover-vs-yield** choice, and the tiles it
would free *are* visible to the dawn census the moment `harvest_age` moves,
because `brain.n_free_slots` reads the identical clamp (`brain.py:182-186`,
whose own comment says it has to stay the same one).

## 2. Idle tile-hours and the cycles they are worth (Q2)

Post-harvest idle = tiles that held a crop this season and are `EMPTY`/`WEED`,
summed over all 24 turns of each day (so a tile freed at hour h and never
replanted contributes 24-h that day and 24 the next).

| tile-hours/board | d0-d9 | d10-d19 | d20-d29 | **season** |
|---|---:|---:|---:|---:|
| B, ymg set | 216 | 100 | **3,808** | **4,124** (sd 1,182) |
| ymg_aq | 143 | 518 | 1,800 | 2,460 |
| B, band set | 290 | 99 | **4,253** | **4,641** (sd 478) |
| band clone | 243 | 306 | 2,133 | 2,682 |

**B is tighter than both tapes for two thirds of the season and then stops
planting.** d0-d19 B idles 316 (ymg) / 388 (band) tile-hours against 661 / 549.
The whole difference is the last ten days: B's crop tiles fall 55.9 → 15.7
(mean tiles in crop per turn) over d19→d29 while the opponent keeps replanting
to d27.

Crop-cycles those hours are worth (idle tile-hours / 24 × cycle days, where the
cycle is `CROP_SATURATE_AGE`):

| crop | cycle | B (ymg) | ymg_aq | B (band) | band clone |
|---|---:|---:|---:|---:|---:|
| WHEAT | 4 d (96 h) | 43.0 | 25.6 | 48.3 | 27.9 |
| CARROT | 3 d (72 h) | 57.3 | 34.2 | 64.5 | 37.3 |
| TOMATO | 8 d (192 h) | 21.5 | 12.8 | 24.2 | 14.0 |
| STRAWBERRY / MELON | 10 d (240 h) | 17.2 | 10.3 | 19.3 | 11.2 |

Restricted to the reachable window (d20-d27; a crop planted on d28 or d29
cannot pay) the idle is 2,306 (ymg) / 2,558 (band) tile-hours = **24.0 / 26.6
wheat cycles or 32.0 / 35.5 carrot cycles per board**. d28-d29 alone hold
1,502 / 1,695 tile-hours, and those are correctly dead.

## 3. What the planner would need (Q3)

**Is the day fixed at dawn?** Yes, and completely. `rollout.run_day` calls
`brain.decide` then `plan.build_day` once per day, which emits `uop/ua/uq` of
shape `[MU, TPD]` — the whole day's route for every unit. There is no hook of
any kind after a harvest resolves. But the dawn plan is *not* blind to the
day's harvests: `free_slot = is_empty | is_weed | harvest_one`
(`plan.py:5501`), the plant walk ranks over that set (`slot_rank`,
`plant_here`, `plan.py:5886-5929`), and the seed want is sized from the same
`n_free` — which is why the 95 same-day replants exist at all.

**Do hands have spare turns?** Season-wide 687.0 of 6,673.4 unit-turns are PASS
(10.3 %; band 676.8 / 6,673.9 = 10.1 %). By hour (ymg set, per board per
season):

| hour | 0 | 1 | 2-3 | 4-12 | 13-16 | 17-19 | 20-21 | 22 | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PASS % of active | 100 | 88 | 4-9 | **0.0-0.6** | 1.0-2.9 | 4.0-7.2 | 9-14 | 25 | 59 |

The crew is **fully booked from hour 4 to hour 12** and the slack is all at the
end of the day (and hour 1, the market/hire turn). Per day the PASS share is
7.7-12.6 % from d4 on (d29 is 26 %). Over d20-d27 there are **93.0 spare
unit-turns** at h ≥ 12 out of 1,161 active (8.0 %; band 95.1 of 1,182.6). A
replant costs two turns (walk + PLANT, plus a WATER to be worth anything), so
that slack is worth on the order of 30-45 extra plantings per board over the
eight days — it is not zero, and it is not large.

**Is the seed cash there?** Yes, everywhere after d3. Board-mean coins at h=12
against the wheat bill (10/tile) for every tile freed that day:

| day | d4 | d8 | d12 | d16 | d20 | d24 | d27 |
|---|---:|---:|---:|---:|---:|---:|---:|
| coins at h=12 | 1,217 | 2,114 | 3,949 | 13,263 | 44,462 | 61,519 | 75,135 |
| freed tiles | 11.00 | 5.67 | 3.83 | 5.00 | 5.17 | 5.42 | 8.58 |
| wheat bill | 110 | 57 | 38 | 50 | 52 | 54 | 86 |
| melon bill | 880 | 453 | 307 | 400 | 413 | 433 | 687 |

Only d3-d4 are anywhere near tight (741-1,217 coins against an 80-110 coin
wheat bill, or 640-880 at melon prices) and those are exactly the days B
already replants everything it frees. **Cash is not the constraint.**

## 4. Upper bound under the TWO-PURSE rule (Q4)

No coin claim. Tile-cycles and the cash they need, board means:

| | ymg set | band set |
|---|---:|---:|
| freed but **not** same-day replanted, season | 46.2 | 53.4 |
| — of it, d0-d19 | **10.0** | **10.0** |
| — of it, d20-d27 | 13.6 | 17.0 |
| — of it, d28-d29 (dead by construction) | 22.6 | 26.4 |
| idle tile-hours d20-d27 | 2,306 | 2,558 |
| wheat-cycles in that idle | 24.0 | 26.6 |
| seed cash for one extra pass over the d20-27 gap tiles | 136 (wheat) / 1,087 (melon) | 170 / 1,360 |
| B's coins at h=12 on d20-27 | 59,791 | 64,860 |
| spare hand-turns h ≥ 12 on d20-27 | 93.0 of 1,161 | 95.1 of 1,183 |
| B tiles planted d20-d27 | 53.6 | 60.0 |
| OPP tiles planted d20-d27 | 82.7 | 90.7 |

**The ceiling on a second development pass is 10 tiles per season before d20
and 13.6-17.0 tiles on d20-27**, against 22.6-26.4 on the two days where a
replant cannot mature. A pass that perfectly closed the d0-d27 gap would put
down 23.6-27.0 extra tiles a season on top of B's 184.2 — a 13-15 % tile
increase — and it would cost 236-270 coins in wheat seed and roughly half of the
93-95 spare afternoon unit-turns d20-27 has. The opponent's 56-57 tile lead (240.4 vs 184.2)
is **not** in that pass: 29 tiles of it are d20-d27 plantings B's dawn plan
never wants, and the rest is upstream of replanting altogether (earlier
harvest age, more land).

## 5. Build recommendation

**Do not build the default-off second development pass.** It would re-run the
development allocation for tiles the dawn allocation already had
(`free_slot` already contains `harvest_one`), and the residue it could catch is
10 tiles/season before d20. The measurement says the tiles are somewhere else,
and both places are one-scalar switches on paths that already exist:

1. **`plan.py:5313` + `brain.py:185` — the harvest age.**
   `harvest_age = clip(VAL.pay_day() - t_day, c_first, c_sat)`: away from the
   horizon this is `c_sat` (wheat 4 d, carrot 3 d), and ymg_aq harvests wheat at
   `c_first` = 2 d. A switch that lowers the one-time-crop harvest age by k days
   (`c_sat - k` floored at `c_first`) moves `free_slot`, `n_free_slots` and the
   seed want **together**, which is precisely what makes the freed tiles visible
   to the dawn census — no new pass, and the existing 1-hour harvest→replant
   pairing carries the replant for free. It trades yield per tile for cycles per
   tile, so it must be run as a paired CRN ledger (k = 1, 2 and the `+1`
   control) on the same 12 + 68 boards, exactly as DEV-SLOPE was.
2. **The late-season planting stop (d20-d27).** B plants 53.6 tiles there and
   ymg_aq 82.7; B's idle over the window is 2,306 tile-hours = 24 wheat cycles,
   with 60k coins and 8 % spare afternoon hand-turns. The gate is the value
   horizon (`VAL.pay_day()` / `plan.HORIZON_DROP_ON`) and the plant candidates'
   `tile_value`, not the dawn/mid-day distinction. Same paired ledger.

If the lead still wants the second pass for its own sake, the site is
`plan._plan_and_stats` immediately after `free_slot`/`n_free` are formed
(`plan.py:5501-5507`, before the `[M1]` land re-derive at 5768) — but it would
have to be fed by a *larger* `harvest_one`, which is item 1, so item 1 comes
first either way.

## UNVERIFIED

* Sim only. No engine game, no ES arm, no promotion gate, no coin claim.
* 20 of the 68 band boards (`S/replant/boards_band20.json`, the first 20 of
  `S/seed_screen/boards_BAND.json`), not the full 68; the ymg set is all 12.
* A tile harvested and replanted **within one turn** (unit A harvests, unit B
  plants, same h) is invisible to the tile-transition method — `kind` never
  leaves `KIND_PLANT`. The op-level cross-check bounds it: B issues 184.2
  OP_PLANT and the transition method sees 184.2 tiles planted, so on our seat
  there are none; on the ymg_aq tape 241.3 ops against 240.4 transitions, so at
  most ~1 tile/season is hidden there.
* The idle measure counts a tile from the first time it holds a crop; tiles
  converted to COOP/PASTURE are excluded (they are not `EMPTY`/`WEED`), and
  never-planted tiles never enter it.
* "Crop-cycles lost" divides tile-hours by `CROP_SATURATE_AGE`; it is a capacity
  statement, not a revenue statement — the two-purse rule applies and no coins
  are claimed from it.
* d29 runs 23 turns (`n_turns = TPD - 1`, no eod), so its hour-23 column is
  empty by construction.
* Switch state as measured: the runner's four (`OPEN_PUMP_ON`, `TAIL_FILL_ON`,
  `BANK_BEFORE_LOT_ON`, `HIRE_ROW_ON`) plus the shipped defaults —
  `MIDDAY_PLACE_V2_ON = False`, so the `mel_bank` exclusion at `plan.py:5506`
  ("a melon tile the day banks is not a slot the day develops") is **not** in
  play and does not explain any of the unreplanted tiles; `HORIZON_DROP_ON =
  True`, so `VAL.pay_day()` = 29 and `harvest_age` is `c_sat` for every crop
  planted before ~d25.
