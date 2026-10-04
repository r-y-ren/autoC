**Planner review — 2026-09-10**

The planner has a sound execution-oriented structure, but its resource safety, task priorities, and economic values are different kinds of guarantees. They must not be treated as interchangeable. This review identifies reproducible counterexamples in the shipped planner, measures their occurrence in a small trained-policy sample, and records a negative intervention result. It does not claim that any untested correction improves tournament win rate.

**Scope and evidence**

Reviewed `.claude/worktrees/ship-pair/src/kagg3/`, not the older main checkout. Compared eight files byte-for-byte with `dist/submission_flow172_g940_pair.tar.gz`: `plan.py`, `budget.py`, `sell.py`, `projector.py`, `valuation.py`, `brain.py`, `policy.py`, and `agent/runtime.py`. All matched. Packaged planner SHA256: `ac731e501427e2e4e77cb61a80d47e5103f0b60553d6f3bfc8f895d025e4df32`.

Validation performed:

- Executable synthetic probes, including exhaustive enumeration of the small route example. Synthetic inputs test the planner's local contract; they are not a demonstration that the trained policy reaches those snapshots from the competition opening.
- Four full reference-engine games: opponent tapes 107233845 and 107244033, both seats, the saved seed and pinned town schedules, `flow172_g940.npy`, shipping planner switches. All four reproduced the saved own and opponent money exactly. This is two boards, not four independent opponents.
- Instrumentation of all 120 day-plans in those games, including the three route-repair rounds.
- Four further reference-engine games testing an in-memory route-selection change. The change was not applied to production source.
- 44 existing focused tests passed: land valuation, operational statistics, purchase allocation, and sale allocation, excluding tests selected by `backend` or `agrees`. This was not a full suite or a new GPU/NumPy equivalence run.

Evidence files are alongside this report: `probes.json`, `games.json`, `route_ab.json`, and the executable scripts that produced them. The scripts currently use the workspace's absolute path and write their results into `/tmp/kagg3-planner-review/`.

**1. What the planner actually optimizes**

The implementation is a sequence of approximate decisions:

1. `brain.decide` supplies crop/animal targets, holding values, sale pressure, development weights, land bias, hiring bias, crew target, and a forward-work horizon.
2. `_derive` identifies tile operations and grants purchases using an initial zero hiring bill and zero reserve.
3. The hire scan compares every crew size using that initial task list, approximate movement/pickup costs, and a cumulative task-value prefix.
4. `_derive` runs again after deducting the chosen wage bill and reserve. This can change purchases and tasks.
5. Admission ranks tiles by mandatory tier and total tile value. Routing traverses the admitted work in spatial order and partitions it into contiguous worker blocks.
6. Three admission/routing rounds reduce the admitted count when routing misses tasks.
7. Sales are allocated from morning inventory, with reservations and later additions for forced overflow sales and deposit excursions.

There is useful engineering here: shared NumPy/JAX planner code; explicit operation ordering; actual per-block pickup costs; exact Manhattan route distances; cash and shed constraints in the purchase allocator; marginal own-market price impact in sales; terminal liquidation and return-to-shed handling. These should be retained.

But there is no single objective consistently optimized by all seven stages. Purchase values use projected marginal streams; planting labor uses gross production at the current quote; hiring reads sums of those task values; selling uses marginal liquidation revenue minus learned pressure and holding values. The learned policy can compensate for some disagreements, which makes changes to one stage risky with frozen weights.

**2. Land's price is missing from its utility comparison — confirmed model defect**

Source: `plan.py:5358–5386`; `budget.py:marginal_gain`.

`marginal_gain` sums the incremental candidates' value minus their seed/animal purchase costs. The caller reduces the available budget by `land_gap`, then accepts land when:

```python
land_value + macro.land_bias > 0
```

The land price is absent from that value comparison. Deducting a cost from the available budget enforces affordability; it does not subtract that cost from profit. The nearby comment arguing that an explicit land charge would count the price twice is incorrect for the quantity `marginal_gain` returns.

Reproduction, zero learned bias, day 27, one empty owned quadrant, 26 requested wheat plantings:

| Quantity | Coins |
|---|---:|
| Quadrant price | 1,000 |
| Computed incremental candidate profit | 34 |
| Learned land bias | 0 |
| Land purchased | Yes |
| Incremental candidate profit minus land price | −966 |

The reference engine subtracts the land cost in `_do_buy_land` and scores final money; it grants no terminal land resale value. The full incremental comparison should be structurally:

`value_with_land − value_without_land − full_land_cost + learned_residual`.

It must also account for the existing purchases displaced by spending on land. Morning sales used to fund the purchase are not free money: without the purchase, that revenue could remain cash.

**Observed scope:** none of the eight actual land purchases in the four instrumented games had `land_value < land_cost`. The trained land bias was strongly negative, and all observed purchases cleared even the full price. Therefore this is a proven foundation error, not a demonstrated explanation of those four losses. Changing its baseline requires recalibrating or retraining the bias.

An existing test explicitly expects a zero-bias purchase for one extra tile worth approximately 120 coins behind a 1,000-coin quadrant. It verifies current behavior rather than the claimed break-even principle (`tests/test_land_value.py:test_a_saturated_negative_bias_refuses_a_quadrant_zero_bias_buys`).

**3. Admission priority does not guarantee execution — confirmed feasibility defect**

Source: `plan.py:6440–6521`, `_routes`.

Admission orders by `(tier, value)`. Routing then groups all priced or mandatory work together and orders it spatially. When routing misses a tile, repair subtracts the number missed from the admitted count. It does not remove the particular route obstruction, optimize an exchange, or verify that mandatory operations were executed after the final round.

A survival-watering probe places a thirsty, immature tomato at serpentine position 99 and three harvest opportunities elsewhere. The tomato has no premature yield, needs watering to avoid its second unwatered night, and is assigned tier 2. The final plan reports:

```text
survival tile 99: admitted=True, covered=False
time to reach and water it directly: 10 turns
```

The farmer instead harvests an earlier spatial tile and uses a later tail action elsewhere. The engine turns a plant into a weed after its second consecutive unwatered night. A feasible watering exists; the failure is the admission/routing interface.

**Change required:** verify essential operations against emitted routes, not against the admitted mask. A repair should be able to drop optional additions from a tile's chain, exchange optional work, or reserve a feasible route for an essential operation. Simply putting mandatory tiles first in every spatial sweep can add expensive crossings, so this needs a bounded route-feasibility repair, not another unconditional ordering flag.

The probe establishes the possibility. The four-game instrumentation was not an animal-death or plant-death census, so no prevalence claim is made for this failure in trained play.

**4. Route repair can worsen its own objective — confirmed; simple correction failed the game test**

Source: `plan.py:6489–6521`; `tests/test_day_stats.py`.

On a four-strawberry board, the repair rounds complete:

| Repair rounds used | Completed task value |
|---|---:|
| 1 | 840 |
| 2 | 720 |
| 3, shipping default | 360 |
| 4 or 5 | 480 |

The final probe uses standing yields 1, 3, 3, and 4, respecting the engine's four-unit strawberry cap. The older test that inspired it uses yields above that cap; its original 1,320-to-600 counterexample was reproduced too, but is not the basis of the final realistic-quantity example.

The farmer completes one 360-coin harvest. Exhaustive enumeration of this small task set finds 840 coins feasible; one such route visits positions 91 and 99 in 19 route turns. Thus more repair rounds are not monotonically better, even under the planner's own values.

**Observed scope:** final-round value was below an earlier round on 11/120 instrumented day-plans. Differences totaled 693 planner-value coins across the four games, not 693 final-profit coins.

I tested a scratch change that retains the best round, comparing covered tier-2 count, then tier-1 count, then covered task value. All route outputs, pickups, coverage, banking masks, and admitted masks were retained together. Full-engine results with the same frozen theta:

| Tape | Seat | Final margin change |
|---|---:|---:|
| 107233845 | 0 | +75 |
| 107233845 | 1 | −67 |
| 107244033 | 0 | −1,229 |
| 107244033 | 1 | −1,229 |

Mean change: **−612.5 coins/game**. All four remained losses. The mirrored results are correlated and the sample is tiny, but it is enough to reject claiming this patch as a demonstrated improvement.

This exposes a second problem: improving `tile_value` does not necessarily improve eventual cash or margin. More work can change sale timing, inventories, prices, and future policy decisions. Retaining the best route is sensible under a correctly specified objective; the current proxy has not established that objective. Do not ship the scratch patch on the toy result alone.

**5. Future work can buy today's entirely idle workforce — confirmed model defect**

Source: `plan.py:5980–6008`, `plan.py:6074–6143`; engine `_end_of_day`.

The learned `forward_days` widens watering/harvest windows in the task list used to score hiring. Actual execution is re-derived from today's unwidened tasks. Workers disappear every night (`farm['hands'] = []`); they are not a persistent capital asset.

On a synthetic day-3 board of immature melons, with no current tasks or requested development, enough cash, and all other macro controls fixed:

| Forward horizon | Hires | Wages | Non-PASS unit actions |
|---|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 3 | 12 | 376 | 0 |
| 6 | 12 | 376 | 0 |

This is a stress-state counterexample, not a claim that g940 builds 100 melons by day 3. It isolates the hiring formula: future watering makes a temporary worker appear profitable today even when no action can realize that value.

Future production can justify hiring for *present development that creates it*. Future work alone cannot justify present wages. The hiring model should score today's executable state changes and the future returns those changes cause, not simply import tomorrow's task list into today's crew argmax.

**Change required:** distinguish present executable work from future demand, and re-evaluate a small shortlist of crew counts after their wage bills, reserves, purchases, and actual routes are known. A final idle-worker check must respect unit IDs, spawn ordering, hire-row timing, and the learned policy's co-adaptation; simply deleting arbitrary hire orders is unsafe.

The four real games used forward horizons ranging from 0 to 6. This review did not measure how often their forward horizon specifically caused idle hires.

**6. The purchase allocator has no explicit cash-retention alternative — confirmed under its own value model**

Source: `budget.py:164`, `plan.py:4768–4866`, `plan.py:5409`.

An item is eligible when its value is positive, not when its value exceeds cost. Ratio ranking and affordability decide order and feasibility, but they do not establish profitability.

A full planner probe uses the normal price table, carrot inventory at the start of its one-coin floor, zero learned land bias, and a one-carrot target. It buys and schedules planting the seed despite:

```text
modeled candidate value = 5 coins
seed cost = 20 coins
```

A simpler allocator-only probe likewise grants an 80-coin purchase with value 6. These demonstrate that the allocator can spend on negative modeled net value when cash is available. They do not show the frequency of such purchases under the trained macro.

**Change required:** compare discretionary acquisitions to retaining cash. Any intentional strategic benefit, such as opponent-price suppression, needs to be represented in the marginal value or an explicit learned residual. Merely requested quantity plus positive gross production is not a break-even test. The policy has learned around the current convention, so a new threshold must be validated and co-trained, not assumed to be a free improvement.

**7. Purchases and reservations are not reconciled to the final route — observed interface mismatch**

Purchases are finalized before admission (`plan.py:5409`), while market orders still emit those quantities after routing. Sale reservations use the queued feed count and fertilizer applications (`plan.py:6606–6614`), although actual pickup quantities are already available in `blk`.

In the four baseline games:

- 27/120 day-plans bought seeds beyond the amount needed for the day's scheduled plant actions after accounting for seed stock already held.
- Those excess purchases totaled 37 wheat, 22 carrot, 1 tomato, and 4 melon seeds: 1,180 coins of purchases across four games.
- Five day-plans reserved seven fertilizer units beyond routed applications.
- There were no excess wheat reservations in this sample.

Unplanted seeds persist and can be used later. The 1,180 coins are therefore cash committed ahead of scheduled use, not a measured profit loss. Similarly, holding fertilizer can be sensible. The defect in the interface is that these are implicit consequences of dropped tasks, not separately valued inventory decisions.

**Change required:** finalize purchases and reservations from a time-indexed resource ledger after a feasible route is selected. Retain explicit desired future stock when worthwhile. Any released budget must be reconsidered jointly with hiring and development rather than silently left as an incidental result.

**8. Economic valuation is the central architectural limitation**

The evidence does not support declaring route geometry or the neural network alone the limiting factor. It supports reviewing what each stage calls value:

- `_candidates` prices new production using an inventory projected to first yield, plus the farm's remaining season supply (`plan.py:4809`). This compresses a time-varying supply stream into one pricing position.
- Planting labor is valued using total prospective units times the spot quote and learned multipliers (`plan.py:5701–5726`), which differs from the purchase model.
- Hiring initially scores a zero-wage, zero-reserve task set and may include future operations; the final purchase plan is derived afterward.
- Sales model own market impact and town drain, but the shipping `OPP_SUPPLY_ON=False` path has no explicit opponent supply curve. Neural `hold` and `press` provide corrections; intraday observations normally cannot revise the cached plan.

These are inspected approximations, not new measured estimates of their tournament cost. The negative route intervention is direct evidence that the task-value proxy alone is inadequate for promotion.

A stronger common basis is marginal continuation cash:

`expected future cash with decision − expected future cash without decision`.

That comparison needs purchase costs, executable labor, delivery time to the shed, liquidation timing, own price impact, and displaced work. Opponent response remains uncertain; use learned residuals or scenarios for it rather than calling the entire estimate exact. Production forecasts already present in `brain.py` should be reused, not reinvented.

**Recommended implementation sequence**

1. Add economically meaningful oracle checks: a modest positive crop gain cannot alone justify a more expensive quadrant; a negative-net discretionary purchase must compete with cash; future-only work cannot justify all-idle temporary hires; essential feasible operations must survive routing; repair must report the feasible candidates it discards.
2. Establish a consistent marginal-value convention and correct land/cash comparisons behind experimental controls. Recalibrate the learned residuals when their baseline changes.
3. Repair essential-operation feasibility and evaluate a small crew/route shortlist on finalized resource and sale schedules. Preserve the shared NumPy/JAX implementation and benchmark throughput before expanding the shortlist.
4. Reconcile purchases and reservations to selected routes, with explicitly valued future inventory.
5. Compare full-season engine results with frozen weights first, then co-train promising structural changes. Keep wins, own cash, opponent cash, and route diagnostics separate. Use fresh boards and a larger opponent sample for promotion.

No source change from this review is a proven winning configuration. In particular, the tested best-round patch failed its small engine check and remains a diagnostic artifact only.
