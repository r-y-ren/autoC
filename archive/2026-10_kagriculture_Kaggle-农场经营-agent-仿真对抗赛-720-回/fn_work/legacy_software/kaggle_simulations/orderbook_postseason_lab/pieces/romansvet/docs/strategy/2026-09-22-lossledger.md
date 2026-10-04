# LOSSLEDGER — corrected reacting-V56 losses (2026-09-22)

The corrected 143–107 run has 107 losses: 80 of the invalid run's 115 loss labels remain losses,
35 old losses become wins, and 27 old wins become corrected losses. `S/v56leg/loss_ledger.tsv`
contains 64,200 day × product × seat rows. Engine market operations were replayed unit by unit;
all **214/214** seat ledgers close exactly (`3000 + successful cash events = final purse`).

| deficit axis | dominates losses | mean positive deficit / loss |
|---|---:|---:|
| realised sale volume, valued at V56 realised price | **107 / 107** | **32,644 coins** |
| realised sale price on common volume | 0 / 107 | 763 coins |
| excess input + hire + land cost | 0 / 107 | 251 coins |

The volume number is a positive-shortfall decomposition across products, not the final purse margin;
our surplus products are intentionally not netted against deficient products when assigning cause.

| phase / product | mean V56−ours units | volume-value gap | common-volume price gap |
|---|---:|---:|---:|
| d10–19 / MELON | **+72.0** | **+17,440** | 0 |
| d10–19 / WOOL | +14.9 | +2,653 | +171 |
| d10–19 / FERTILIZER | +38.6 | +2,327 | +5 |
| d10–19 / MILK | +17.5 | +1,953 | +63 |
| d10–19 / WHEAT | +43.0 | +1,685 | +67 |
| d19–24 / WHEAT | **+82.4** | **+3,316** | +1 |

Labour agrees with a production-volume diagnosis: V56 has 31.4 more effective work operations in
d10–19 (68/107 losses) and 50.9 more in d19–24 (80/107). Ours has 83.4 and 64.9 more idle unit
turns respectively (101/107 and 98/107). Fertilizer is not a blanket shortage: ours leads total
covered crop-tile dawns by 54.1 in d10–19. In d19–24 V56 leads strawberry coverage by 5.84 tile
dawns (65/107), despite ours leading wheat coverage by 12.36. This late crop-allocation difference,
not total early fertilizer volume, motivates the one-target STRAW_SWAP1 audit.

Successful cash events and effective unit-action records (day/hour/sequence, operation and target)
are retained in `S/v56leg/loss_events.jsonl`; the complete source observations/actions remain in
`S/gatefidelity/replays_v56/`.
