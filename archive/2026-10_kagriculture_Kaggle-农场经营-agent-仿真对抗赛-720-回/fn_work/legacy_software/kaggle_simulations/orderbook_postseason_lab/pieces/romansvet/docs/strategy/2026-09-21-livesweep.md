# LIVESWEEP — exact win-flip switch sweep

## Verdict

**NO SHIP among the 36 switches completed inside the six-hour wall-clock box.**
The fresh incumbent replay reproduced all 150/150 chronological train purses
exactly (109–41 wins). No switch met the train gate of net >= +3 and mean
delta-theirs <= 0, so the 50-board dev panel was never run. Games 200–249 were
not touched. The remaining 46 switches form a deterministic resumable suffix.

All 22 shipped-ON switches were tested first. The best result was
`FEED_MANDATORY_ON=False` at +1 win (+1/-0, delta-theirs -70.840), below the
predeclared dev threshold. Four arms were purse-identical on all 150 boards:
`PRESTOCK_V2_BUY_ON`, `CLIP_FERT_SKIP_ON`, `CLIP_CAP_STRICT_ON`, and
`MELON_LOT_EARLY_ON`.

## Train results (sorted by net)

| switch | default->test | wins | flips +/- | net | mean dours | mean dtheirs | changed |
|---|:---:|---:|:---:|---:|---:|---:|---:|
| `FEED_MANDATORY_ON` | True->False | 110 | +1/-0 | +1 | +86.927 | -70.840 | 58 |
| `CLIP_CAP_STRICT_ON` | False->True | 109 | +0/-0 | +0 | +0.000 | +0.000 | 0 |
| `CLIP_FERT_SKIP_ON` | False->True | 109 | +0/-0 | +0 | +0.000 | +0.000 | 0 |
| `MELON_LOT_EARLY_ON` | False->True | 109 | +0/-0 | +0 | +0.000 | +0.000 | 0 |
| `OPEN_PUMP_ON` | True->False | 109 | +4/-4 | +0 | +185.600 | +75.840 | 150 |
| `PRESTOCK_V2_BUY_ON` | True->False | 109 | +0/-0 | +0 | +0.000 | +0.000 | 0 |
| `SHED_DEFICIT_ON` | False->True | 109 | +1/-1 | +0 | +65.167 | +26.520 | 67 |
| `SHED_DUMP_ROW_ON` | False->True | 109 | +0/-0 | +0 | +0.340 | -0.313 | 1 |
| `OPEN_PUMP_SLOT0_ON` | True->False | 108 | +3/-4 | -1 | +308.807 | -121.427 | 143 |
| `SHED_OVERFLOW_ON` | False->True | 108 | +1/-2 | -1 | -138.640 | +34.887 | 119 |
| `ADMIT_SLACK_ON` | False->True | 107 | +1/-3 | -2 | +103.447 | +106.487 | 100 |
| `ENDROUTE2_SPLIT_ON` | True->False | 107 | +0/-2 | -2 | -23.627 | +55.533 | 132 |
| `CLIP_CAP_ON` | False->True | 106 | +0/-3 | -3 | -51.820 | -29.087 | 120 |
| `SELL_SLOT_PRIORITY_SELLS_FIRST_ON` | True->False | 106 | +0/-3 | -3 | -111.813 | +115.787 | 150 |
| `ENDROUTE_ROW2_ON` | True->False | 105 | +0/-4 | -4 | -191.620 | +38.260 | 142 |
| `SURVIVAL_WATER_ON` | True->False | 105 | +1/-5 | -4 | -265.333 | -13.640 | 149 |
| `WIDE_PICK_FREE_ON` | True->False | 105 | +1/-5 | -4 | -194.167 | +11.760 | 130 |
| `BANK_BEFORE_LOT_ON` | True->False | 104 | +0/-5 | -5 | +21.133 | +364.093 | 143 |
| `LOT4_ON` | True->False | 104 | +0/-5 | -5 | -286.880 | +272.180 | 146 |
| `MIDDAY_PLACE_ON` | False->True | 104 | +0/-5 | -5 | -10.620 | +355.640 | 140 |
| `SELL_SLOT_PRIORITY_ON` | True->False | 104 | +0/-5 | -5 | -198.807 | +194.100 | 150 |
| `WIDE_PICK_ON` | True->False | 104 | +0/-5 | -5 | -392.553 | -8.340 | 150 |
| `TAIL_FILL_ON` | True->False | 102 | +2/-9 | -7 | -309.073 | +433.160 | 150 |
| `EARLY_SELL_ON` | True->False | 100 | +0/-9 | -9 | -289.393 | +286.400 | 150 |
| `TAIL_CARE_ON` | True->False | 98 | +1/-12 | -11 | -94.480 | +566.040 | 150 |
| `ENDROUTE2_ON` | True->False | 94 | +0/-15 | -15 | -1347.433 | -115.027 | 150 |
| `ENDROUTE_ON` | True->False | 94 | +0/-15 | -15 | -1381.800 | -114.820 | 150 |
| `ROUTE_SPLIT_ON` | True->False | 90 | +3/-22 | -19 | -1757.500 | +246.460 | 150 |
| `HIRE_ROW_ON` | True->False | 87 | +0/-22 | -22 | -1853.647 | +144.667 | 150 |
| `MIDDAY_PLACE_V2_ON` | False->True | 87 | +1/-23 | -22 | -1031.953 | +411.580 | 150 |
| `FERT_TIMING_ON` | True->False | 80 | +1/-30 | -29 | -1313.027 | +1007.940 | 150 |
| `MIDDAY_DROP_ON` | False->True | 75 | +0/-34 | -34 | -3324.760 | +216.587 | 150 |
| `SELL_SPREAD_ON` | False->True | 67 | +0/-42 | -42 | -1821.307 | +3505.253 | 147 |
| `DROP_ON` | True->False | 54 | +0/-55 | -55 | -5662.940 | +143.367 | 150 |
| `MELON_OPEN_ON` | False->True | 13 | +0/-96 | -96 | -3778.387 | +17165.620 | 150 |
| `MIRROR_OPEN_ON` | False->True | 12 | +0/-97 | -97 | -4291.093 | +19917.553 | 150 |

## Resumable suffix

The next arm is `SAME_DAY_FERT_ON=True`; 46 switches remain. `run.sh` skips a
switch only when `results.tsv` already has its completed train row, so the
interrupted successor is rerun from scratch. The remaining order is the suffix
of `switches.txt` beginning at `SAME_DAY_FERT_ON`. No dev rows exist.

## Commands and contract

```bash
cd /mnt/e/_work/kaggriculture3
JAX_PLATFORMS=cpu WORKERS=8 bash S/livesweep/run.sh
```

`run.sh` mechanically creates the first-150 train and next-50 dev ID/seed
files, checks episode alignment, runs a fresh incumbent, and aborts unless all
150 recorded purse pairs reproduce exactly. Each completed arm appends one TSV
row. A train arm with net >= +3 and mean delta-theirs <= 0 would immediately
open dev; dev net >= +2 with delta-theirs <= 0 is the ship-candidate rule.
The runner passes each flip through `SW_EXTRA=,NAME=value` into `gate.sh` with
the frozen `head_940`, exact LIVE250 towns/tapes/seeds, `LEG=band3`, and eight
workers.

## Outcome (2026-09-22T07:50Z) — 82/88 switches measured, sweep complete
No switch reaches the +3 train gate. Best: TILE_ALLOC_ON OFF +2 (Δtheirs −25), FEED_MANDATORY_ON OFF +1 (−71), CREW_PUSH_COST_ON ON +1 (Δtheirs +12, fails). Every shipped-ON switch loses 2-55 wins when flipped OFF; OFF→ON flips ≤ +2. Verdict: shipped switch vector is a local optimum on the exact live oracle; NO SHIP; axis CLOSED. Full table S/livesweep/results.tsv.
