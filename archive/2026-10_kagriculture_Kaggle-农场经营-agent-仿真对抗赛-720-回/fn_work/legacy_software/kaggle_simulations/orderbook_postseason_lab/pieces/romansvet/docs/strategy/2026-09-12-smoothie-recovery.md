# Smoothie guard recovery (2026-09-12)

## Verdict

**REFUSE modes 1--3.**  Mode 1 is the only variant with real-engine evidence,
and it does not improve any evaluated engine family convincingly.  Its two
screen families regress strongly.  No pooled statistic is used here.

## Failed no-op diagnosis and repair

The reported non-smoothie screen failures were a labeling error, not leakage
from the conditional guard.  `screen_tree.py` labeled `smoothie` from day 15
alone, while the code activates whenever `SMOOTHIE_SHOP` is present on any day
15--29.  Shops rotate.  Every changed row in the saved screens has
`smoothie_any=1`; zero changed rows occur on towns that never contain the shop:

| screen family | mode | changed rows | changed on never-smoothie towns |
|---|---:|---:|---:|
| LIVE-C | 1 | 70 | 0 |
| LIVE-C | 2 | 70 | 0 |
| LIVE-C | 3 | 19 | 0 |
| TOPB2 | 1 | 28 | 0 |
| TOPB2 | 2 | 28 | 0 |
| TOPB2 | 3 | 11 | 0 |

`screen_tree.py` now records the exact day-15--29 condition for new CSVs, and
`table.py` uses the conservative `smoothie_any == 0` no-op check so old CSVs
remain valid.  `test_inert.sh` now exports `arms-next` fresh under `/tmp`; its
previous attempt to refresh `/root/tree_smoothie_base` failed because that
recovery tree is read-only.  The repaired test passes coin-identically on the
reference board 107463847 (seed 4674845, seat 0): both builds score
94,698--98,435, margin -3,737, shop signature 132.  Source inspection also
establishes why OFF identity is structural: the pristine export is
byte-identical to `arms-next`, and the entire added
graph block is behind the import-time Python branch `if SMOOTHIE_GUARD`, whose
unset/empty/0/false/no/off values all decode to zero.

## Screens (each family reported separately)

These are paired mode-vs-OFF simulator screens, retained as refusal evidence,
not promotion evidence.

| family | mode | games | margin delta/game | row t | result |
|---|---:|---:|---:|---:|---|
| LIVE-C hold-out | 1 | 120 | -215 | -4.17 | regress |
| LIVE-C hold-out | 2 | 120 | -119 | -1.92 | regress |
| LIVE-C hold-out | 3 control | 120 | -23 | -1.48 | weak regress |
| TOPB2 | 1 | 40 | -691 | -4.62 | regress |
| TOPB2 | 2 | 40 | -724 | -4.45 | regress |
| TOPB2 | 3 control | 40 | -117 | -2.20 | regress |

## Mode 1 real-engine legs (each family reported separately)

Paired with the corresponding B CSV on `(seed, opponent, seat)`; decision t is
computed over 30 independent boards after averaging the mirrored seats.

| family | games / boards | B win% | mode-1 win% | margin delta/game | board t | flips W/L/= |
|---|---:|---:|---:|---:|---:|---:|
| NEXT30 | 60 / 30 | 68.3 | 70.0 | +87 | +0.49 | 3/2/26 |
| LIVEC-H30B | 60 / 30 | 83.3 | 83.3 | -60 | -0.95 | 0/0/28 |
| NEXTHIGH | 60 / 30 | 53.3 | 53.3 | -81 | -0.62 | 0/0/24 |

W/L count individual games whose win status changes. `=` counts games with
identical margins, not the remaining win statuses; these columns do not sum
to the number of boards or games.

The small NEXT30 gain is noisy and accompanied by losses on both other engine
families.  Together with the clear screen regressions, this does not merit
spending more engine budget on modes 2 or 3 and cannot be promoted.

## Next action

Close this hand guard.  Preserve its files as negative evidence.  If smoothie
town behavior is revisited, derive a new response from action-level engine
traces and screen it first on both LIVE-C and TOPB2; do not extend these clamp
or acreage-hold modes.
