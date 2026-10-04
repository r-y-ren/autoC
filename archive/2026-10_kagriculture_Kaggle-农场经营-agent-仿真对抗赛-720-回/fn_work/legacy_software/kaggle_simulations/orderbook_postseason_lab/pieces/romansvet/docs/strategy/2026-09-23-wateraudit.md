# WATERAUDIT — zero-value op census of the shipped tree (2026-09-23)

Branch wateraudit (worktree kagg3_wt_wateraudit, from master 3ee9b785 = res940_cfog3, OVERFLOW_GUARD V1/V2/V3 ON).
Harness: `S/wateraudit/run.sh` (OVERFLOW4 reacting-V56 leg; dev100 result byte-equal to OVERFLOW4 `dev_v3.csv`, 67-33),
`audit.py` (read-only engine hooks: pre/post snapshot of EVERY op of our seat, hour-23 census before `_end_of_day`),
`census.py` (engine-rule classification). Outputs `S/wateraudit/census.tsv` (game×band×who×class) + `summary.txt`.

## Classification (engine rules, kaggriculture.py l.312-835)
NOOP = engine ignored the op (state byte-identical). WATER zero if no yield gain AND (crop harvested later that day /
never harvested again / day 29 / cu=0 and harvested tomorrow); SLACK = cu=0 and watered or harvested tomorrow
(alternation; evaluated on the pruned schedule so only droppable ones count). FEED: survival (unfed night ≥1), care
(cared by dusk or pending bonus on a production night) else slack/d29. CARE zero if unfed at dusk or d29.
COLLECT zero = fertilizer still held at game end or destroyed. FERTILIZE zero if no fert-bonus water/production in window.
PASS_WORKLEFT = PASS on a day that ends with a dying plant / escaping animal.

## Census, dev100 (per game; 1 op = 1 unit-hour)
| | all | farmer | hand | d0-9 | d10-19 | d20-29 |
|---|---:|---:|---:|---:|---:|---:|
| executed ops | 6,603 | | | | | |
| moves / pass / work | 2,869 / 593 / 3,141 | | | | | |
| **zero-value ops** | **56.5** | 3.2 | 53.3 | 11.0 | 15.9 | 29.6 |
| WATER_SLACK (alternation) | 29.3 | 2.3 | 27.0 | 11.0 | 15.5 | 2.8 |
| COLLECT_UNUSED (end hold) | 14.8 | 0.2 | 14.6 | 0 | 0 | 14.8 |
| WATER_NOOP (already watered) | 8.2 | 0.6 | 7.6 | 0 | 0 | 8.2 |
| other NOOP (harvest/care/drop…) | 3.0 | | | | | |
| WATER_NOFUTURE/HARV_TODAY/TMRW | 1.0 | | | | | |
| FEED_SLACK / FERT_WASTED / CARE_UNFED | 0.2 | | | | | |
| PASS_IDLE (no work left) | 556.8 | 72.6 | 484.2 | 154.0 | 228.7 | 174.2 |
| PASS_WORKLEFT | 36.1 | 5.2 | 30.8 | 0.1 | 1.7 | 34.3 |
Zero-value = **0.86 % of all ops, 1.80 % of work ops** (hard zero excl. slack 27.1/game = 0.41 %). Destroyed 1.3 u/game.
Water ops: 943/game effective, 566 yield-gain, 369 survival-required; the plan ALREADY alternates (wheat 0,2,3,4;
melon 0,2,4,6-10; strawberry every other day) — the V3 `_job_cost` WATER=0 cases are dusk-displacement pricing, not waste.

## Verdict — NO BUILD (below the 5 % bar)
Zero-value ops are < 1 % of executed ops, and the freed turns have nowhere to go: hands already PASS 484 turns/game
(557 total, 8.4 % of all unit-hours) on days that end with no dying plant or unfed animal. Crew time is not the binding
constraint (consistent with TURNCENSUS / IDLEWORK); ZERO_OP_SKIP_ON not implemented, no gate run.
Residual threads (not worth a switch): 8 u/game fertilizer held at d29 (~15 collects), 8 no-op waters on d20-29.
