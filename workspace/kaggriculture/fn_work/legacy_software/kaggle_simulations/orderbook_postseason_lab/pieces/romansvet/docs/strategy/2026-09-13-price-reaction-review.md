# Shipped OFF price-reaction cadence review (2026-09-13)

## Finding

The shipped OFF agent reacts to the live price and market state once per day,
at hour 0. It then replays a cached 24-turn plan. It does not revise that plan
in response to later price changes during the day.

This is visible in the exact source used for the seed-309 run and judge under
`S/unitorder/off_train_20260913/loop-train/private_stage/src`:

- `kagg3/agent/parse.py:82-93` copies the current product prices and market
  inventory into `DayView`.
- `kagg3/core/brain.py:521-549` feeds normalized prices and inventory into the
  policy. `brain.py:478-489` also values forward production at the current spot
  prices.
- `kagg3/core/plan.py:4850,4998,5073-5220,5647-5701` uses `view.price` when
  valuing crop, animal, feed, fertilizer, route, and sale decisions.
  `plan.py:5771-5778` builds the resulting whole-day plan.
- `kagg3/agent/runtime.py:30-34` builds that plan only at hour 0, when no plan
  exists, or when the day changes. `runtime.py:46` and
  `kagg3/agent/render.py:52-60` subsequently select the cached row for the
  current hour. Rendering adjusts the number of hand actions to the hands that
  actually exist; it does not reprice or replan their actions.

The sole per-turn market-read hook is the hour-1 pump tell at
`runtime.py:36-44`. Its gate, `OPEN_PUMP_TELL_KEEP0_ON`, is false in the shipped
source (`kagg3/core/plan.py:1270-1276`). `OPEN_PUMP_ON=True` at
`plan.py:1173` schedules a day-0 opening trade from the dawn plan; it is not an
intraday feedback controller.

## Prior closure

The missing intraday reaction is known and has already been tested as a lever.
[The plateau review](2026-09-09-plateau-review-verdicts.md#2-let-it-revise-market-decisions-during-the-day--not-binding-closed)
records a 0.07% order-refusal rate, with no refused BUY, HIRE, LAND, PLACE,
DROP, PICKUP, or MOVE action in the measured sample. It also records that the
reactive and same-day excursion variants lost or were level.

[The independent intraday review](2026-09-10-intraday-controller-review-B.md)
collects the paired engine results: the minimal mid-day revisit lost 4,964
coins per board; the two OPP_SUPPLY doses lost 2,972 and 3,616; and the
same-day-sale family was closed after four builds. The remaining hour-1 pump
tell was subsequently measured and was byte-identical to its control on all
124 live-board games and all 40 TOPB games because it never changed a row
([consensus record](2026-09-10-consensus.md), section 2 resolution;
`2026-09-10-verdicts.txt:18`). No intraday price-response experiment remains
open on this evidence.

## Seed-309 interpretation

The independent saved judge audit at
`S/unitorder/judge_seed309_g10_20260913_r1/judge_evidence/sol_saved_audit.json`
(SHA-256
`7449dfebf08e7744b1f55353cc641d6694ff364c7e0672a12a5d1066fa12c92a`)
shows that seed 309 increased its own final money relative to B in six of seven
families, while the opponent-money change was positive in all seven. Those
final-money aggregates contain no action timing or counterfactual market
trace. A changed supply or denial pattern in the shared market is a plausible
interpretation, consistent with earlier paired failures in which our changed
selling behavior benefited the other seat. It is not a causal attribution
established by these CSVs.

The source behavior and prior paired measurements therefore support closure:
the agent is dawn-price-aware, intraday-static, and the intraday-replanning
family should not be reopened from the seed-309 final-money result alone.
