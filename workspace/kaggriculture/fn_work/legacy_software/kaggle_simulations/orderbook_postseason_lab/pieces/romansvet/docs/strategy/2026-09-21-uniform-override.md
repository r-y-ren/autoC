# UNIFORM-OVERRIDE — static LIVE250 residual tables

## Verdict

**No uniform rule.**  Every board-independent table loses net wins on both
train and dev, every table increases the opponent purse on every split, and
all six paired mean-margin shifts are strongly negative.  The least damaging
record is U6 at **97–153**, a loss of **69** wins from the incumbent 166–84.
U1 is the only table to flip any loss to a win: it flips one dev board while
destroying 86 incumbent wins, for net **−85**.

These are killing numbers, not a close selection call.  Across the six total
rows, net flips range from **−69 to −146**, mean margin changes range from
**−4,405 to −16,040**, paired t ranges from **−14.28 to −41.45**, and mean
opponent-purse changes range from **+423 to +2,320** coins/board.  The useful
plant-volume signal in the per-board hindsight programs is board-specific; a
static day/slot table does not capture it without losing many existing wins.

## Protocol

All 250 boards are replayed in chronological LIVE250 order with their exact
`info.seed`, original seat, pinned town, taped opponent, shipped
`theta7659`, and greedy `head_940`.  A table is fixed before any board is seen
and is applied by `live_expert_head.py` on top of the head action.  Results are
paired against the purse pair in `live250_selection.json`, whose incumbent
replay was previously verified exact on 250/250 boards.

The split is chronological: train indices 0–149, dev 150–199, sealed 200–249.
A win is strictly `ours > theirs`.  `+` is incumbent loss to override win and
`−` is incumbent win to override loss.  `Δmargin`, `Δours`, and `Δtheirs` are
override minus incumbent means; SE and t are paired over per-board margin
deltas.  The incumbent records are train 109–41, dev 33–17, sealed 24–26,
and total 166–84.

The v1 decode is `d_plant = categorical_value - 4`, so U4's requested `+2`
is categorical value **6**.  Values 8 in plant slots 0–4 decode to `+4`, and
value 4 in hire slot 8 decodes to `+2`.

## Summary

| variant | static table | total wins | flips +/− | net | Δmargin | SE | t | Δours | Δtheirs |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| U1 | d10–12 all five plants = 8 | 81 | +1/−86 | **−85** | −7,123.36 | 415.40 | −17.15 | −5,130.94 | +1,992.41 |
| U2 | d10–12 wheat/carrot/strawberry = 8 | 83 | +0/−83 | **−83** | −4,852.84 | 334.56 | −14.50 | −4,430.02 | +422.81 |
| U3 | d10–19 all five plants = 8 | 20 | +0/−146 | **−146** | −16,040.03 | 386.98 | −41.45 | −13,719.58 | +2,320.45 |
| U4 | d10–12 all five plants = 6 (`+2`) | 95 | +0/−71 | **−71** | −4,405.44 | 308.57 | −14.28 | −3,411.09 | +994.35 |
| U5 | d10–14 tomato/strawberry/melon = 8 | 60 | +0/−106 | **−106** | −8,425.47 | 315.16 | −26.73 | −6,764.92 | +1,660.55 |
| U6 | U1 plus hire slot 8 = 4 | 97 | +0/−69 | **−69** | −5,239.20 | 344.37 | −15.21 | −3,390.69 | +1,848.52 |

## U1 — d10–12 all five plant slots = 8

| split | wins (incumbent) | flips +/− | net | Δmargin | SE | t | Δours | Δtheirs |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| train | 61 (109) | +0/−48 | −48 | −7,128.61 | 560.71 | −12.71 | −5,235.05 | +1,893.56 |
| dev | 9 (33) | +1/−25 | −24 | −7,695.86 | 880.41 | −8.74 | −5,706.34 | +1,989.52 |
| sealed | 11 (24) | +0/−13 | −13 | −6,535.10 | 852.90 | −7.66 | −4,243.24 | +2,291.86 |
| total | 81 (166) | +1/−86 | −85 | −7,123.36 | 415.40 | −17.15 | −5,130.94 | +1,992.41 |

The lone positive flip is dev index 195, episode `111397797`: margin −1,190
to +1,396 (`Δours +1,423`, `Δtheirs −1,163`).  It does not offset the other
86 crossings in the wrong direction.

## U2 — d10–12 wheat, carrot, and strawberry = 8

| split | wins (incumbent) | flips +/− | net | Δmargin | SE | t | Δours | Δtheirs |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| train | 61 (109) | +0/−48 | −48 | −4,488.51 | 440.66 | −10.19 | −4,347.12 | +141.39 |
| dev | 11 (33) | +0/−22 | −22 | −5,536.32 | 772.23 | −7.17 | −5,179.76 | +356.56 |
| sealed | 11 (24) | +0/−13 | −13 | −5,262.32 | 674.68 | −7.80 | −3,929.00 | +1,333.32 |
| total | 83 (166) | +0/−83 | −83 | −4,852.84 | 334.56 | −14.50 | −4,430.02 | +422.81 |

## U3 — d10–19 all five plant slots = 8

| split | wins (incumbent) | flips +/− | net | Δmargin | SE | t | Δours | Δtheirs |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| train | 19 (109) | +0/−90 | −90 | −16,112.87 | 531.75 | −30.30 | −13,697.71 | +2,415.17 |
| dev | 1 (33) | +0/−32 | −32 | −16,073.86 | 785.97 | −20.45 | −13,846.86 | +2,227.00 |
| sealed | 0 (24) | +0/−24 | −24 | −15,787.68 | 778.54 | −20.28 | −13,657.94 | +2,129.74 |
| total | 20 (166) | +0/−146 | −146 | −16,040.03 | 386.98 | −41.45 | −13,719.58 | +2,320.45 |

## U4 — d10–12 all five plant slots = 6 (`+2`)

| split | wins (incumbent) | flips +/− | net | Δmargin | SE | t | Δours | Δtheirs |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| train | 70 (109) | +0/−39 | −39 | −4,110.47 | 406.48 | −10.11 | −3,295.71 | +814.76 |
| dev | 12 (33) | +0/−21 | −21 | −5,107.84 | 713.43 | −7.16 | −3,943.26 | +1,164.58 |
| sealed | 13 (24) | +0/−11 | −11 | −4,587.92 | 621.98 | −7.38 | −3,225.04 | +1,362.88 |
| total | 95 (166) | +0/−71 | −71 | −4,405.44 | 308.57 | −14.28 | −3,411.09 | +994.35 |

## U5 — d10–14 tomato, melon, and strawberry = 8

| split | wins (incumbent) | flips +/− | net | Δmargin | SE | t | Δours | Δtheirs |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| train | 47 (109) | +0/−62 | −62 | −8,186.83 | 417.98 | −19.59 | −6,981.97 | +1,204.85 |
| dev | 7 (33) | +0/−26 | −26 | −8,854.86 | 799.97 | −11.07 | −6,511.72 | +2,343.14 |
| sealed | 6 (24) | +0/−18 | −18 | −8,712.00 | 530.15 | −16.43 | −6,366.96 | +2,345.04 |
| total | 60 (166) | +0/−106 | −106 | −8,425.47 | 315.16 | −26.73 | −6,764.92 | +1,660.55 |

## U6 — U1 plus hire slot 8 = 4 (`+2`)

| split | wins (incumbent) | flips +/− | net | Δmargin | SE | t | Δours | Δtheirs |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| train | 72 (109) | +0/−37 | −37 | −4,706.86 | 404.54 | −11.64 | −3,362.67 | +1,344.19 |
| dev | 14 (33) | +0/−19 | −19 | −5,963.04 | 818.56 | −7.28 | −3,752.52 | +2,210.52 |
| sealed | 11 (24) | +0/−13 | −13 | −6,112.40 | 898.16 | −6.81 | −3,112.92 | +2,999.48 |
| total | 97 (166) | +0/−69 | −69 | −5,239.20 | 344.37 | −15.21 | −3,390.69 | +1,848.52 |

## Conditional flip and ledger gate

No table has positive net flips on both train and dev; none has non-positive
mean `Δtheirs` on any split.  Therefore no table reaches the requested gate,
and there is no qualifying flip list or mean ledger delta to report.  The
`--with-ledger` run correctly skipped the expensive ledger pass rather than
extracting an irrelevant mechanism read.

All per-board purse pairs are retained in
`S/actionrl/uniform_override_results.json`.  The primary six passes took
2,903.7 seconds (48.4 minutes) with eight CPU workers.

## Commands

```bash
cd /mnt/e/_work/kaggriculture3

JAX_PLATFORMS=cpu OMP_NUM_THREADS=8 \
  .venv/bin/python -m pytest -q \
  tests/test_live_expert.py tests/test_uniform_override.py

JAX_PLATFORMS=cpu WORKERS=8 OMP_NUM_THREADS=8 \
  .venv/bin/python -u S/actionrl/uniform_override.py \
  --workers 8 --with-ledger
```

## Decision

Do not ship or further tune a board-independent override table from this
family.  The hindsight search's 48 plant commits encode conditional choices
about crop, dawn, and board state.  Repeating those actions uniformly both
cuts our purse sharply and, unlike the constrained expert, gifts the opponent
on average.  Any continuation should learn or specify the board-state
condition, not broaden the static day/slot mask.
