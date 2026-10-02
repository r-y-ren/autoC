# Other temporal signals for reaction

2026-09-13. Two Sol source reviews, followed by a fixed training-replay incidence
check. No momentum feature implementation, model fit, game or coefficient search
was performed.

## Result

Beyond the already reviewed previous-dawn market movement, the reviewers rank
**change in the opponent's public production forecast** as the strongest
conditional candidate for a saved-data check. Cash pace is legal but hard to
interpret. Market-flow acceleration needs a second lag before the first lag has
shown incremental value. Shop and expansion “momentum” mostly re-encode facts
already present in the current observation.

History can still matter in a Markov game because the opponent's shed, seeds and
unit inventories are private. Past public states can update a belief about that
hidden state or the opponent's behavior. None of the signals below is a direct
measurement of hidden stock, income, or future action.

## Ranked signals

### 1. Opponent public-forecast revision — conditional first choice

- **Past/public state:** at each dawn save the opponent half of
  `brain.board_forecasts`, computed from public `kind`, `occ`, `t_day` and
  `t_yield`. Compare its per-product +1-day forecast with the next dawn's
  corresponding public forecast. Start with the +1-day column only; normalize
  with the existing `_FCAST_SCALE` used by `production_forecast`.
  These are rolling forecasts for different calendar windows, not revisions
  of a prediction for the same target date. Ordinary aging/maturation can
  explain their difference; it must not be called an unexpected supply shock.
- **Sign and use:** positive means the opponent's near-term visible production
  outlook grew since yesterday; negative means it contracted. The relevant
  response horizon is today's crop/animal mix, hold, and sale schedule. The
  existing +3/+7 forecasts remain the right horizons for longer-maturity
  planting.
- **New information:** the current forecast says what the visible board can
  produce now and later. Its revision says how that outlook has been changing,
  including recently removed or replaced commitments, which a current aggregate
  does not recover. This may help infer whether the opponent repeatedly
  maintains, harvests, abandons, or reallocates production.
- **Limit:** call this a *public forecast revision*, not forecast error or
  realized supply. A harvest resets standing yield and moves goods into private
  inventory; plant death, harvest, replacement and maintenance failure can have
  the same sign. Forecasted production is not a sale. Matching individual tile
  indices is unsafe until simulator raw order and submission serpentine order
  are explicitly canonicalized; whole-board product summaries avoid that trap.
- **Plumbing:** medium-high. Retain one prior `[2,9]` summary in simulator state
  and one `[9]` summary per submission seat, with a zero first-day/handover
  convention. Append a zero-initialized product input block rather than widening
  existing matrices. Update both seats only after their dawn inputs are formed.

This is partly redundant with the current opponent +1/+3/+7 forecasts, which
are already connected through nonzero `fh/fs` weights. It advances only if a
training-side saved-data check shows incremental information.

### 2. Cash-gap velocity — legal, global, and ambiguous

- **Past/public state:** previous and current public money for both seats.
  Candidate features are `delta_own / 20000`, `delta_opp / 20000`, and
  `(delta_own - delta_opp) / 20000` over one day.
- **New information:** current money and the current money gap are already
  global features. Their change distinguishes a stable lead from a rapidly
  changing one and can update a belief about opponent tempo or hidden stock.
- **Confounders:** a money delta is net cash movement, not income. Sales, product
  and seed purchases, land, animals and hires all contribute. It must never be
  labeled opponent revenue or productivity without an exact ledger. Existing
  transfer work found no useful cross-sectional explanation from current
  opponent money, which does not test velocity but lowers the prior.
- **Plumbing:** medium. Two previous scalars per seat still require the full
  simulator/runtime/package history contract. A global zero-initialized path is
  cheaper in parameters than a product block, but not in fidelity work.

### 3. Product commitment change — genuine only for removals

- **Past/public state:** per-product counts of visible crops and animals on both
  farms at consecutive dawns; `(count[d] - count[d-1]) / 25` over one day.
- **New information:** it records product-level churn and removals. New surviving
  placements are already derivable from current public planting/placement dates,
  and current counts plus production clocks already enter the network and its
  forecast. The historical residue is therefore narrower than the name suggests.
- **Confounders:** one-time harvest, death, weeds, land unlock and replacement
  all alter counts. A negative count does not imply liquidation. A current-state
  `OPP_MIX` rule was previously inert, but that result did not test history.
- **Plumbing:** medium for saved prior `[2,9]` counts; low if restricted to
  current-state “newly placed” counts, which would no longer be a momentum
  feature and would mostly duplicate the clock-aware forecast.

### 4. Market-flow acceleration — defer

- **Past/public state:** three dawn inventories. For product `p`,
  `((I[d-1]-I[d]) - (I[d-2]-I[d-1])) / T[p]`; positive means aggregate net draw
  is accelerating. Do not use rounded price acceleration when exact stock is
  public.
- **New information:** this distinguishes persistent pressure from a turn in
  pressure after first-difference momentum is established.
- **Confounders:** both seats' sells and buys, deterministic town consumption,
  shop changes, and price-floor censoring. It doubles warm-up/history needs and
  amplifies day-to-day noise. The independent review recommends no second lag
  before the first lag shows value.
- **Plumbing:** high: two prior vectors in both training and submission, two
  zero-history days, opening handover semantics, and broader state schemas.

### 5. Shop-demand onset and expansion pace — deprioritize

- **Past/public state:** `demand[d]-demand[d-1]`, `nquad[d]-nquad[d-1]`, or a
  newly placed structure count.
- **Why little is new:** current shop identities already feed exact
  product-specific daily demand and residual drain; current `nquad`, free land,
  tile kinds, planting dates, both farms' forecasts and land affordability are
  also present. History can identify which cumulative shop instance is newest
  or that land was bought yesterday, but the current causal demand/capacity is
  already visible.
- **Confounders and cost:** random shop unlocks create sparse jumps; land has at
  most three changes; placement is sparse and partly current-derived. Each true
  lag still incurs runtime and simulator state plumbing. Prior shop sensitivity
  showed B already reacts strongly to current shop identity, so onset is a weak
  representation case.

## Relationship to prior closures

The forecast blocks are present and nonzero; their assumptions include perfect
watering/feeding and sufficiently frequent harvest, so their revisions have not
been tested as inputs. `OPP_SUPPLY` and opponent-front-run phase 1 tested fixed
or current-state supply assumptions, not forecast revisions. `OPP_MIX` tested a
current commitment rule. Intraday pump/tell and cached-plan experiments tested
within-day timing. None closes a legal day-over-day history signal. Conversely,
their failures warn that better state description does not guarantee a useful
action or score gain.

## At most two cheap next checks

Use only a frozen training-side replay corpus that is disjoint from all seven
judge families. Bind its identity before calculation and keep products and
source families separate.

1. **Redundancy/incidence ledger, no fit.** For the forecast-revision and cash
   velocity signals, record per-product/day variance, repeated-current-state
   disagreements, missing/first-day rows, and aliases caused by harvest/removal.
   Also show the current forecast and current cash features beside them. Stop a
   signal if it is deterministic from the existing current features or has no
   usable variation.
2. **One fixed incremental prediction check.** With a predeclared linear model
   and leave-one-board-out folds, compare current features alone against adding
   the opponent +1-day forecast revision when predicting the next dawn's public
   opponent forecast. Do not sweep coefficients or features. The next-dawn
   target is an offline audit label, never a runtime input. A positive result
   supports only representational plumbing; it does not predict crop-maturity
   returns, game score, or justify training.

Price/stock first-difference analysis should finish before any acceleration
check. Cash velocity remains descriptive unless the first ledger overcomes its
spending ambiguity. No policy arm follows automatically from either check.

## Completed incidence check

The fixed120 Flow215 training episodes produced7200 current-dawn seat records.
The extraction validates actual replay hashes, current observation schemas and
64800 market quotes. It contains no action, reward or outcome arrays. Episode
and source IDs are grouping metadata, not candidate runtime inputs. All seven
judge groups have empty replay-ID intersections with this training sample.

The first extraction refused before completing any episode because root added
an incorrect inventory/hand-count guard. Inventories include the farmer plus
hired hands. The preserved fresh r1 corrects that schema, keeps the same120
episodes and completed in90.441 seconds within the original overall deadline.
No failed sample was replaced. The copied core/agent/spec bytes match the
audited policy; the copy is not claimed to match the entire training tree.

Sol independently re-read all120 replay files and compared all7200 raw dawn
rows with their actual observations, including both boards and private resource
inventories. Its saved audit passed; derived feature floats were bound by source
and output hashes, not independently recomputed by that review.

The deterministic ledger has6960 day1–29 seat rows. Day0 is explicitly missing;
each lag stays within its episode and seat. Shared-market distributions use
one row per episode; player-specific distributions use both perspectives, which
remain dependent. It reports each product and day separately across this fixed
training corpus; source submissions are not stratified, so this is not evidence
of generalization to different opponents. Root independently checked every
market/forecast/cash lag and the symmetry between the two seats.

| Signal | Observed incidence | Interpretation |
| --- | --- | --- |
| Shared market stock movement | At days1,15,29, each non-fertilizer product changes in81.7–100% of episodes | Frequent history signal; town demand and both players contribute |
| Opponent +1-day forecast change | Tomato changes on0%,0%,17.9% of seat rows at those days; milk on0%,95.8%,94.2% | Strong product/lifecycle dependence; not an unexpected-supply measure |
| Crop/animal commitment change | Melon changes on99.2%,0.4%,1.2% of seat rows at those days | Often a planting or removal boundary; current clocks already explain part |
| Cash-gap change | Nonzero on57.5%,82.5%,97.5% of seat rows at those days | Variable but spending-confounded; mean is zero by seat symmetry |

Current input relationships were verified exactly: product column0 encodes
current stock relative to initial stock, column1 current price, and the opponent
+1-day forecast input equals the raw public forecast divided by32. The ledger
establishes usable variation, not that history adds predictive information over
the existing current inputs. It does not perform the proposed redundancy test,
identify harvest/removal causes, or measure score gain.

Prioritize first-difference market history for the next fixed prediction check;
opponent near-term forecast change is the first additional history candidate.
Keep cash velocity descriptive and defer acceleration. Bind the prediction
target, baseline, model and episode-grouped split before fitting. Both seats
of a replay must share a fold, and results must retain product/board detail.

Evidence:

- Dataset `S/unitorder/momentum_dataset_r1_20260913/dawns.npz`, SHA
  `3793fd2d2fd3d2e1230de9c179708ddd8bd1d7e99d0eb25a72e0dd288d6f1c4d`.
- Dataset manifest SHA
  `2ac4637f37742e6833565758848aeccc16cea9e3f3f5688de8852e32d05e7e94`.
- Dataset independent audit SHA
  `324afa6f3a84b46bd8d2c2dc143e658778137ec88fccc40cc1535b60bbc589c6`.
- Ledger helper `S/unitorder/momentum_incidence.py`, SHA
  `05c2688fb51c4370c201091cce51310bfd88a7317455ea25d46fa4a9a82c9170`.
- Ledger manifest SHA
  `4c590ddf8786c53ee514619c63adadfb10f0191440be1f23eaf0260142e3b77d`.
- `S/unitorder/momentum_incidence_20260913/ledger.npz`, SHA
  `3080944cdc060b6920a261ebf28605465e4398b9ff2d907f99f74b35c8951d2e`.
- Summary SHA
  `9e600ae9c6783d489c3aa4e49890b651b38c75d4cf0bf8ed38c3dd96a2d7dbca`.
- Receipt SHA
  `db051746cff87b6a41a4a27c3f412c735eedefd09100febebcabacdb29121d00`.
