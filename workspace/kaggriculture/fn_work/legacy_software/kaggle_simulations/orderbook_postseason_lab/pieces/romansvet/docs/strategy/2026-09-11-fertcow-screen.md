# FERTCOW: the "fertilizer −7.3k/game with more cows" open item, screened

Agent, 45-min box, 2026-09-11 (CPU only, no judge lock, no engine legs).  Question inherited from the
counter-class / LOSS10 work: `2026-09-11-loss10-anatomy.md:120` left open *"why our fertilizer output is
100-200 units lower with more cows (not traced to feed hours here)"*, and memory `counter-class-2200-band`
carries it as **open: fertilizer −7.3k/game with more cows**.

## 1. What was actually measured, and what it is

**The −7.3k is a revenue line, not a production line.** Source: `scripts/replay_profile.py`'s market
re-simulation of 13 live Kaggle replays of candidate B (10 ladder losses 2175-2381 + 3 wins), per-seat ledgers
`S/bloss/anatomy/led_<id>_{us,opp}.json`; the per-game fertilizer flows are `S/bloss/fert/flow.csv`
(`S/bloss/fert/fert_flow.py`, both seats read from the replay JSON to the coin — no seed noise, no sim).

Re-read of `flow.csv` for this task (13 games, our seat):

| relation | r |
|---|---|
| cows at d10 vs fertilizer **produced** | **+0.11** |
| whole herd at d10 vs produced | +0.83 |
| **animal-days** vs produced | **+0.98** |
| cows at d10 vs fertilizer **sold** | +0.04 |
| **applications vs units sold** | **−0.85** |
| applications vs fertilizer revenue | **−0.79** |

* The "more cows" premise is false in the data: we average **6.6 cows at d10 to the clone's 7.5**. What is
  larger is our total herd in some games (herd r = 0.83 with production) — and production is one unit per
  *alive* animal per night regardless of species or feeding (`sim/eod.refresh_animals`, engine
  `kaggriculture.py`), so the species mix cannot move the fertilizer line at all.
* Production is level-to-ours: **367 collects/game vs their 346** (+976 coins), already established and logged
  as **REFUTED** in `2026-09-10-consensus.md:417` ("we produce less fertilizer with more cows — REFUTED, 1
  unit/animal/night regardless of feeding") from the 10:16Z measurement `2026-09-11-fertilizer-engine.md`.
* What is lower is **units sold**: 192/game vs their 344, because we burn **190 units on FERTILIZE to their 62**.
  The board-level correlation r(applied, sold) = **−0.85** and r(applied, revenue) = **−0.79** is the
  displacement signature stated arithmetically: on our seat the shed identity closes to −6…−19 units/game
  (hour-23 collect masking), so every applied unit is a unit not sold.

**Verdict on item 1: displacement, confirmed twice.** The two-purse price of the trade was already done — the
exact LOSS6 census (`2026-09-09-fertilizer.md`, 2,254/2,254 yield post-states reproduced) values our ~179
applications at **+24.2k gross crop coins / +16.8k net of the forgone fertilizer sale** against the clone's
79 at +15.3k / +12.4k, i.e. **we are +4.4k ahead on the trade whose sale-side half reads −7.3k**, and the
market-curve counterfactual of dropping our 86 wheat applications is **−4,086/game** (+3,098 on the
drain-less fertilizer curve, −7,184 on the scarce-side wheat curve).

## 2. Prior art (archive rule — checked before any new measurement)

| lever | where | verdict |
|---|---|---|
| `FERT_VOLUME_ON` (application must clear NUM/DEN × a fertilizer reference) | `plan.py:3779-3800`; `2026-09-09-fertilizer.md` §Q4; `2026-09-11-fertilizer-engine.md` | 384 paired engine games, best mode `marginal` **+636 t 1.50** (bar is +1,500/t 2), `base` −1,103; 2026-09-10 re-measure on g1000+pair: level on TOPB, +650-750 t 4 on LIVE62 with wins level (denial signature), **composed with HIRE_ROW it drops 3-4 live boards → CLOSED as a package candidate** |
| `FERT_MARGINAL_ON` | `S/fert_marginal/report.md` | −1,745 t −3.09 / 384 games, shelved |
| `FERT_BUY_ON` | `S/fert_buy/report.md` | dominated by `budget.grant`, 0/200 boards move |
| `FERT_CARRY_ON` | `S/fert_carry/report.md` | never built: 0 no-op FERTILIZE in 11,386 ops |
| `FERT_FLOOR_ON` (reserve fertilizer above ½ base) | `plan.py:3588`; `2026-09-09-plateau-review-verdicts.md:282,422` | loses on the pinned screen |
| `SAME_DAY_FERT_ON` | `plan.py:1010`; `2026-09-04-verdicts.txt:11-23` | −27k all-days; LAST_DAY=1 replicates −5,511 / −5,339 → CLOSED in every form |
| feed-hours / collection / sale-timing half | `2026-09-11-fertilizer-engine.md` | level or ours (uncollected animal-days 19 vs 48, realised price 53.9 vs 50.6) — **no lever** |
| herd/cow composition | no switch exists (`ANIMAL_DEFER_ON` only, and it loses — plateau §29) | animal share is a theta gene (`gb2[6]`), not a constant |

So the only *existing* expression of "burn fewer fertilizer units on tiles" is `FERT_VOLUME_ON`, and the only
thing never done with it is the thing this task asks for: **the current candidate B, under the shipped `hr`
switch string, on today's two judge families.** Every prior number is on `flow58_g450` or `flow172_g1000+pair`,
on TOPB/LIVE62/panel24, before B existed. No new switch was written (a default-OFF one would duplicate
`FERT_VOLUME_ON`); `git diff --stat` on `src/` is empty.

## 3. The screen

`S/simscreen/screen.py` (pinned-town action-replay boards, `shop_crn` on, shipped `hr` switch string), CPU,
`S/fertcow/run.sh`; B is the theta in every run and **the switch string is the arm**, paired board-by-board
against the existing hr baselines `S/simscreen/topb2_40.csv` / `full120.csv` (same frozen board files, same
theta, same switches — so the pairing is exact and `shopdiff` verifies it). Pairing `S/fertcow/pair.py`.

Arms (all `FERT_VOLUME_ON=True`; the gate is `fert_val > NUM/DEN × ref`, and ON also re-prices the admit half
`v_fert = max(fert_val − ref, 1)`, `plan.py:5178-5184, 5667-5668`):

| arm | mode | NUM/DEN | what it does |
|---|---|---|---|
| `fc_spot11` | spot | 1/1 | gate bar **unchanged** (OFF's bar is exactly spot×1) → isolates the admit-half re-pricing |
| `fc_spot21` | spot | 2/1 | the documented ON: an application must be worth 2× today's fertilizer quote |
| `fc_marg21` | marginal | 2/1 | the prior best mode (lowest, honest bar: what the next unit would fetch) |

Baselines are the B rows already in `S/simscreen/topb2_40.csv` (40 boards) and `full120.csv` (120 boards),
written under the identical `hr` string (`full120.log:2`, `topb2_40.log:2`), so no baseline re-run was needed.
Honest unit per the screen's own caveat: the action-replay seat makes the two seats the same game on 10-15 of
the 20 TOPB2 tapes, so the `tapes` column (one cell per tape) is the unit to read; the 40/120-row `t` is
optimistic.

## 4. Result

All six runs: `shopdiff 0/40` and `0/120` — every arm saw byte-identical shop sequences to the baseline, so
nothing here is the shop-draw re-roll (`shop-lottery-2026-09-06`); the switch first fires at the FERTILIZE
gate on d10+, well after the day-0 stream.

**TOPB2 (`boards_topb2.json`, 40 rows / 20 honest tapes), paired vs B:**

| arm | d (40 rows) | t (40) | **d (20 tapes)** | **t (20)** | W/L/= | win % |
|---|---|---|---|---|---|---|
| `fc_spot11` | +135 | +1.87 | +135 | +1.37 | 18/12/10 | 32.5 → 32.5 |
| `fc_spot21` | +441 | +1.43 | +441 | +1.09 | 24/16/0 | 32.5 → 32.5 |
| `fc_marg21` | +378 | +1.85 | +378 | +1.45 | 22/18/0 | 32.5 → 32.5 |

**LIVE-C hold-out (`boards.json`, 120 rows / 60 tapes), paired vs B:**

| arm | d (120 rows) | t (120) | **d (60 tapes)** | **t (60)** | W/L/= | win % |
|---|---|---|---|---|---|---|
| `fc_spot11` | +107 | +1.45 | +107 | +1.06 | 46/37/37 | 71.7 → 73.3 |
| `fc_spot21` | **+941** | +6.70 | **+941** | **+4.79** | 88/32/0 | 71.7 → **76.7** |
| `fc_marg21` | **+901** | +6.93 | **+901** | **+4.91** | 88/32/0 | 71.7 → **78.3** |

**Two-purse split** (`S/fertcow/purse.out`, the memory rule: price the marginal unit *and* the displacement):

| arm / family | Δ our money | Δ their money | reading |
|---|---|---|---|
| `fc_spot21` / livec | +260 (t +1.89) | **−681 (t −10.88)**, 105/120 boards down | **72 % denial** |
| `fc_marg21` / livec | +261 (t +2.12) | **−640 (t −12.56)**, 109/120 | 71 % denial |
| `fc_spot21` / topb2 | +71 (t +0.21) | −369 (t −1.73) | denial, n too small |
| `fc_marg21` / topb2 | +224 (t +0.92) | −154 (t −0.72) | mixed, |t| < 1 |
| `fc_spot11` (both) | +111 / +131 | −24 / +25 | admit-half alone ≈ nothing |

Mechanism of the denial half is the one the engine rule makes obvious: fertilizer has **zero town drain**, so
the shared pool only grows; every unit we do *not* burn on a tile is sold into that pool and walks the quote
down under the clone's 344 units. That is the +3,098 half of the 2026-09-09 two-purse walk, now measured in
paired play instead of counterfactually — and the reason the same throttle read "+650-750 t 4 on LIVE62 with
wins level, denial signature" on 2026-09-10. Here the wins are **not** level (71.7 → 76.7 / 78.3, 88/32
boards), which is what differs from that read.

## 5. Decision

**ESCALATE** — `fc_marg21` first (`FERT_VOLUME_ON=True, FERT_VOLUME_MODE="marginal", NUM/DEN 2/1`), `fc_spot21`
second. It meets the pre-registered rule (Δ > 0 with t ≥ 2 on one file — LIVE-C 60 tapes, t 4.9 — and not
negative on the other: TOPB2 +378, t +1.45). **This is worth exactly one paired engine judge (four legs vs B),
not a promotion**, and it is a switch on the *shipped* composition, so the leg must carry the full `hr` string.

Caveats the judge has to settle, all of them reasons the prior engine verdict was CLOSED:
1. **Denial, not production.** 71-72 % of the LIVE-C gain is the opponent's purse falling. Denial edges
   measured against fixed tapes are real in-engine but do not transfer to an opponent that would re-time its
   fertilizer sales; the band clone is open-loop and sells at h0 regardless, so against *this* class it should.
2. **Composition.** The 2026-09-10 closure was specifically "composed with `HIRE_ROW` it drops 3-4 live boards".
   The screen here runs `HIRE_ROW_ON=True` and does not reproduce that, but the screen cannot see the live boards.
3. **Family split.** TOPB2 (the top tier that decides the ladder above 2800) is only +378 at t 1.45 — the gain
   is concentrated on the band-clone family that generated the observation in the first place.
4. `fc_spot11` (admit-half re-pricing only, gate untouched) is ~+110 at |t| ≈ 1 on both files: the gate bar,
   not the `v_fert` bid, is where the effect lives.

## 6. What this does **not** reopen

* The cow / herd / feed-hours half stays **REFUTED** (§1) — no lever, no switch, nothing to screen.
* `FERT_FLOOR_ON`, `SAME_DAY_FERT_ON`, `FERT_MARGINAL_ON`, `FERT_BUY_ON`, `FERT_CARRY_ON`, `ANIMAL_DEFER_ON`
  stay closed; none was re-run.
* The screen exposes no farm ledger (only `mine/theirs/margin/shop_sig`), so fertilizer and cow counts in this
  document are the live-replay census (`S/bloss/fert/flow.csv`), not screen output.

Files: `S/fertcow/{run.sh,pair.py,pair.out,purse.out,fc_*.log}`, per-board rows
`S/simscreen/fc_{spot11,spot21,marg21}_{topb2,livec}.csv`. No file under `src/` was modified
(`git diff --stat -- src/` empty); no engine leg, no judge lock, no GPU.
