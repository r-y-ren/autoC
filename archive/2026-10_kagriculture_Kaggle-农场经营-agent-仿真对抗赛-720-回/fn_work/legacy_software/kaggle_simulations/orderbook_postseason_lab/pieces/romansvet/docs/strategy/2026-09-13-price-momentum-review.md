# Price momentum as a policy input (read-only review)

2026-09-13. This is an architectural and prior-evidence review. It does not
change the policy, run a game, or recommend another training arm.

## Answer

A lagged market signal is representable and has not been directly tested. The
current network sees each product's dawn inventory and quote, current shops,
town demand, both farms' standing production, and forward production timing,
but it sees no earlier quote or inventory. A previous-dawn delta would therefore
add realized path information. It would not add a new price *level*: under a
fixed market table, the current quote is a deterministic function of current
inventory.

The cleanest signal is previous-to-current **inventory movement**, with quote
movement available as a derived companion. Quote delta alone is lossy because
prices are rounded to integers and clipped at the one-coin floor. Either delta
is aggregate market pressure, not an identified opponent action: both players'
sells and buys and the town's consumption move inventory, and a new shop drawn
at end of day changes the demand regime. This makes the feature plausible but
noisy. It does not reveal future shop draws or future prices.
Sales at the price floor may stop advancing inventory, so even raw stock
movement need not reveal the volume offered into a saturated market.

## Existing code and evidence

`spec.market_price` computes, for product parameters `(base, I0, T)`,

```
base + below_target * base / shape(f, T, T) * shape(f, I0 - inventory, T)
```

below `I0`, and the corresponding subtraction with `above_target` above it;
the result is rounded and floored at one coin
(`src/kagg3/spec.py:154-169`). The policy already receives `mkt_inv[9]` and
`price[9]` (`src/kagg3/core/brain.py:80-122`). Its product encoder includes
normalized current inventory, current price, current town demand, own and
opponent producing-tile counts, shed inventory, first-yield time and production
rate (`brain.py:521-552`). Board clocks also feed explicit forward production
features. The global head receives day, cash, free land, shops and mean price
ratio (`brain.py:571-597`). These inputs describe the current state and expected
production; they do not identify whether the current stock was reached by a
rising or falling path.

The only matching prior proposal is phase 2 of
`docs/strategy/2026-09-11-oppsell-design.md`: retain `mkt_inv_prev` and infer a
previous day's net market flow. The phase-1 opponent-front-run experiment used
fixed per-product averages, current inventory and current opponent commitment;
it did not add history. Phase 1 was level/refused, while its report explicitly
left `mkt_inv_prev` as the only untested follow-up
(`docs/strategy/2026-09-11-oppfrontrun-engine.md:127-129`; consensus sections
65 and 68). Current source has no previous-market field, and the strategy record
contains no later phase-2 result. The cached-plan, intraday pump/tell, sell
timing, production-forecast, and crop-maturity experiments test different
mechanisms. Their negative results do not close a day-over-day temporal input.

The tomato episode is consistent with a reason to measure this input, not with
proof it helps. B saw tomato inventory, current price, shops and production and
eventually requested four tomato tiles, but allocated none on days 10-14 while
the later quote rose. A lag could expose persistent realized draw. The existing
shop/demand and maturity features can already support implicit anticipation,
and the opponent in that loss grew no tomato, so the episode does not isolate a
missing momentum feature.

## Minimal faithful path

Use one per-product feature, preferably
`(mkt_inv[d-1] - mkt_inv[d]) / T` so positive means recent net draw. Record the
previous dawn quote too and report `(price[d] - price[d-1]) / base` for audit,
but do not spend a second learned channel until saved data shows that rounded
quote movement contributes information beyond stock movement. Day 0, and the
first planner day after an opening splice, must use zero delta.

Checkpoint compatibility requires a separate appended input block rather than
widening the existing `w1`, `dh`, or `fh` matrices. A minimal learned path is an
appended `mh: (1, 64)` into the product encoder pre-activation and
`ms: (1, 2)` into grow/sell scores, initialized to zero and added outside the
existing expressions like `fh/fs` (`src/kagg3/core/policy.py:367-379,600-639`).
That is 66 new coordinates. A padded B must decode byte-for-byte with the block
zero, in both NumPy and JAX, before training is considered.

The state plumbing is the material part:

- The submission runtime needs one previous-dawn vector per seat and must pass
  it through the packaged `_macro` construction. `Runtime` currently retains
  only the cached plan and day (`src/kagg3/agent/runtime.py:18-34`), while the
  package constructs `PolicyObs` directly (`scripts/package_submission.py:
  125-142`).
- The simulator must retain the previous dawn inventory or quote in `State`,
  expose the same delta in `policy_obs`, and update it once per day only after
  both seats' dawn observations have been formed. `run_day` currently computes
  one quote from the current stock and immediately calls both policies
  (`src/kagg3/sim/rollout.py:207-212`). Updating between seats would be a silent
  asymmetry.
- Every direct `PolicyObs` constructor, warm start, state serializer, raw-state
  fidelity schema, package builder, and NumPy/JAX agreement test must receive
  the same first-day convention. The existing simulator qualification cannot
  simply be assumed after `State` is widened.

Tracking raw price delta needs no opponent hidden state and uses only past public
observations. Inferring the opponent's net contribution would require accounting
for known town consumption and our own executed market contribution, along with
floor effects. Requested actions are not enough when orders clip, and end-of-day shop changes must be assigned to the
correct interval. The first feature should therefore remain explicitly
aggregate.

## Cheapest prerequisite before implementation

First identify and freeze an existing training-side replay corpus disjoint from
the seven judge groups. Do not fit or select a forecasting model on H30 judge
replays. Those existing replays can illustrate the idea, but do not supply an
untouched validation set after fitting or feature selection on them. No suitable
training-side corpus has been bound for this proposed test yet.

On the selected corpus, keep every board and product visible. For days1–28
(day29 has history but no recorded next dawn in a30-day replay):

1. verify the recorded quote equals the frozen price table at recorded market
   inventory;
2. record inventory delta, quote delta, current shops, current own/opponent
   production and the next dawn's inventory delta;
3. count per product how often stock moves while rounded/clipped price does not;
4. compare a fixed current-state predictor of next-day inventory movement with
   the same predictor plus the one-day stock delta, with board-separated
   validation fixed before fitting and reporting every product separately.

This uses no engine, policy mutation, or future input at runtime; the next-day
value is an audit label only. Failure would be evidence against that tested
predictor, target and horizon, not every use of history. The baseline should
include the existing production-timing forecast, not just standing tile counts.
For planting decisions, maturity-relevant horizons also need a prospective test;
next-day forecasting alone is not sufficient. Predictive improvement would
support further investigation but would not establish a policy gain. No model
fit, new feature implementation or training run was started in this review.
