# Post-sale cash decomposition after restart

The preserved OFF replays cover only the first four H30 boards. Comparing them
with the corrected `h30_water` games establishes that the opponent's submitted
actions are identical on all eight games, while its cash proceeds change.
This is a descriptive mechanism check, not another performance screen and not
an explanation of the full 30-board result.

`S/postlot/explain_cash.py` pairs by seed and seat, checks opponent identity,
requires complete 720-step replays, checks final replay money against both CSVs,
and requires the sum of all cash-transition differences to equal the final
paired money difference. The run passed. Outputs are preserved in
`S/postlot/pilot/cash_decomposition.json` and `.log`.

| seed | own delta, seat 0 / 1 | opponent delta, seat 0 / 1 |
|---|---:|---:|
| 1166044943 | 0 / 0 | 0 / 0 |
| 1196709180 | -1575 / -1575 | +122 / +122 |
| 2079139712 | +417 / +383 | +54 / +54 |
| 2097576449 | +466 / -322 | +70 / +79 |

There are 560 changed opponent cash transitions. Every one has an identical
opponent market-order list between OFF and ON; 536 also have at least one
different displayed pre-action market price. The unchanged engine's
`_process_market` quotes and commits individual units using the shared market
inventory, so our changed sales can alter the proceeds of an unchanged
opponent order, including within a turn whose initial displayed prices match.
The output preserves both players' market rows for inspection.

Opponent physical state (farm excluding money, plus its private inventory)
also matches at every compared step in six of the eight games. There are 24
differing steps for seed 1196709180 seat 0 and 48 for seed 2079139712 seat 0.
Do not characterize all eight games as a pure price-only change without
decomposing these differences. Their opponent action sequences still match.

The largest own loss in this subset is -1575 despite a harvested extra crop.
The extra seed therefore cannot be valued as sale proceeds minus seed cost:
subsequent replanning, sales, and shared-market effects matter. These four
boards do not explain the full H30 average opponent gain of +391.70, and no
variant or H30B run is justified by this limited decomposition alone. The next
useful diagnostic would preserve matching B replays for the remaining H30
boards and decompose the largest adverse outcomes before changing the hook.

That baseline capture started after restart under tag `off_h30_cash`, using the
unchanged B policy, the exact 30 H30 boards, both seats, one worker, and a
1,800-second process limit. It must finish and pass the existing OFF identity
check before its replays are interpreted. Then run:

```bash
JAX_PLATFORMS=cpu .venv/bin/python S/postlot/explain_cash.py --off-tag off_h30_cash
```

The helper requires all 60 frozen seed/seat keys and writes a separate
`cash_decomposition_h30.json`, preserving the four-board diagnostic. Its
four-board mode was rerun successfully after this extension; the full-family
decomposition is pending the baseline capture.
