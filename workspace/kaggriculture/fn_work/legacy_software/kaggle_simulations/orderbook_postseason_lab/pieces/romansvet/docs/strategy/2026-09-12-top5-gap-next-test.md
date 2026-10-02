# Top-five gap: next falsifiable architectural test (2026-09-12)

## Recommendation: sell, then reinvest on the same day

The highest-value test after flow215 is a **second, post-sale BUY row**. The
current planner commits all ordinary purchases in one morning row
(`src/kagg3/core/plan.py:_market`, the block headed “turn 1 -- the day's
inputs”). The idle-purse experiment established that only 4–108 coins were
available at that row on days 1–6; the cash called “idle overnight” arrives
later from the day's first sale. That experiment could not spend those coins.
A row immediately after lot 1 can. This is a new causal mechanism, rather than
another value, volume, timing or mix scalar: sale quantity, market price,
purchase bundle, pickup route and same-day work must all agree.

The intervention should be called `POSTLOT_REINVEST_ON` in an isolated
worktree. In `plan._plan_and_stats`, after the ordinary budget and lots are
known, enumerate a small portfolio of additional bundles funded only by a
conservative estimate of lot-1 proceeds:

1. fertilizer plus the matching seed for already-admitted empty plant tiles;
2. feed wheat plus an animal only where a free coop/pasture and remaining
   pickup/place/feed turns all exist;
3. seed-only completion of a partially funded crop block;
4. the zero bundle.

Choose one whole bundle by estimated net terminal value after charging its
market slots, per-unit pickup kind and route operations. Do not independently
top up quantities: the point is to cross the purchase-and-work threshold as a
unit. Emit it in `_market` on the first unused turn strictly after lot 1, and
reserve corresponding pickup/use operations in `_routes`. Keep the fixed
within-row category layout, and check crosses against the opposing action row:
a fixed layout alone does not prevent a new BUY row from meeting a foreign
SELL row for the same product. A
failed affordability check must select the zero bundle; relying on the engine
to drop an unaffordable buy would make the route spend turns collecting goods
that never existed.

This is expressible through the existing action interface: the market tensor
already has a row for every turn and `_market` writes several SELL rows. No new
observation is required. At runtime the decision may use our money, shed,
seeds, tiles and the public market/town/shops/opponent board carried by
`brain.PolicyObs` and `plan.DayView`. It may not read the opponent shed, seeds,
future action queue, replay tape, evaluator identity or future shop draws.
Because the opponent can move the sale quote, the funding calculation must use
a documented lower bound derived from current public inventory and our own
lot, or decline the bundle. Offline replay knowledge cannot enter the rule.

## Why this remains open

The closed levers mostly perturb a decision inside the existing daily graph:
sell timing and dose, crop/animal mix, fertilizer volume, hire pressure and
morning purchase ordering. ES changes continuous macro scores but cannot create
another market row or the dependency “sell proceeds fund a coherent purchase
and route later today.” The planner itself acknowledges that its hire argmax is
only exact under a projection and that all purchases are sized before the
day's revenue. Thus “all levers closed” establishes a local result inside the
one-BUY-row architecture, not this intervention.

The objective/record selector defects are lower-value as the next distinct
test. Changed objectives, lost-board weighting, seat swaps, fresh boards and
multiple ES continuations already produced in-sample transfer without held-out
gain. Rotation tests support breadth, but a better selector cannot select a
behavior absent from the representation. The post-lot row adds that behavior.

## Bounded test

Build only the four-bundle enumerator and one post-lot row behind a default-off
switch in a disposable worktree. Do not tune thresholds. Use candidate B's
theta unchanged, so the comparison isolates architecture.

First run an offline screen on each evaluation family separately. For every
board report: post-lot revenue bound, chosen bundle, actual spend, successful
same-day uses, wasted pickup/use turns, end-day idle cash and final margin.
Required structural checks are byte-exact identity when the zero bundle wins,
no more than ten live orders in any row, no cross-category market assertion,
no purchase beyond the conservative funding bound, and every purchased unit
either consumed/placed that day or explicitly valued as inventory at season
end. Refuse the mechanism before engine judging unless it fires on at least
20% of band boards, converts at least 50% of incremental spend into completed
same-day work, and reduces overnight cash without increasing wasted unit turns.

If it passes, run paired real-engine games against B, same boards and both
seats, on these disjoint reads without pooling promotion statistics:

- LIVEC-H30;
- LIVEC-H30B;
- NEXT14 (or another held-out ROTBAND-excluded band set);
- LIVE62;
- TOPB2 as the top-tier veto.

Stop after those existing legs; this needs no training run. Continue only if
both LIVE-C families have positive margin, at least one reaches board-t 2,
neither NEXT14 nor LIVE62 has negative margin beyond one standard error, net
flips are nonnegative in every band family, and TOPB2 stays above its standing
veto. Refuse on a two-purse signature: apparent gain accompanied mainly by
lower opponent coins, with our coins/spend/productive actions flat.

Implementation includes `src/kagg3/core/plan.py` around `_plan_and_stats`,
`_routes` and `_market`, plus the isolated experiment's simulator scheduling
and focused route/market tests. The screen is one B-versus-switch pass;
the engine stage is the existing board inventory, roughly 156 boards and 312
seat-games if NEXT14 is included. Memory is inference-scale: four static bundle
candidates and fixed 24-by-10 action arrays, no ES population and no new tape
bank. A competent implementation and structural tests should fit one day; the
engine read should fit the established judge runtime.

### Simulator prerequisite found during source review

`sim/rollout.py` builds `MARKET_TURNS` at import and uses a full market path only
for the opening rows and the optional prestock row. Ordinary later sale rows
take a path that skips purchases. A new post-sale row therefore needs explicit
registration as a full market turn in the isolated experiment, including the
tape-enabled union of market hours. It must work when an opponent tape has no
order at that hour; otherwise a busy tape could accidentally mask a skipped
candidate purchase. Verify this with the switch both off and on before reading
any screen result. Do not change the reference engine or evaluation rules.

`sim/market.py:process_slot` handles same-product SELL/BUY crossings above the
price floor, but its floor case falls through to sequential solo walks. The
existing `assert_no_cross` remains stricter. A new row must not assume this gap
is irrelevant simply because its own categories are fixed. Check the actual
proposed action schedules against the engine, including a floor-price cross;
if the screen cannot reproduce the new interaction, use real-engine evidence
to assess it rather than treating simulator gains or refusals as valid.

## Scale and interpretation

The refreshed B score of 2,598 is about 417 rating below the observed fifth-place
score of 3,015. The campaign calibration says even 2,967 needs roughly +3,000
held-out band coins versus B; reaching top five plausibly needs on the order of
+4,000 coins, with large uncertainty. A single post-lot row is therefore a
speculative high-upside test, not a forecast. Its credible route to that scale
is repeated early-season capital deployment: proceeds earned after the morning
row buy productive assets one day earlier, and those assets yield across many
remaining days. If it merely shifts a few hundred coins on sale day or fires
mostly after day 20, it has not established a route to closing the top-five gap.
A separately validated incremental improvement can still be useful; its value
must not be confused with evidence that the full goal is achieved.

## Next implementation after the B-specific route census

The corrected public replay census (`2026-09-12-postlot-feasibility.md`) finds
19 of 60 sampled B sale-days with positive net row cash and observed idle-route
capacity for a seed-only planting; none meets the fertilizer route predicate.
Start with a default-off seed-only pilot, while keeping the full reinvestment
hypothesis open. These are capacity bounds, not measured extra plantings.

Inspect `agent/runtime.py:Runtime.act` as the engine-prototype insertion point:
it already caches the day plan and supports a switch-specific intraday patch.
An intraday prototype can use our actual settled cash and global seed inventory
instead of forecasting opponent-dependent sale proceeds. It must preserve
existing queued work, exclude targets reserved by any remaining unit route,
allow the BUY row to settle before PLANT, value the new crop through season
end, and keep the zero bundle byte-identical. It may inspect our plan and
current permitted observation only. A runtime-only prototype needs direct
engine evaluation; the existing simulator cannot assess behavior it does not
execute. Port and validate simulation support only if the engine pilot warrants
further work. No production or uploaded agent code has changed.
