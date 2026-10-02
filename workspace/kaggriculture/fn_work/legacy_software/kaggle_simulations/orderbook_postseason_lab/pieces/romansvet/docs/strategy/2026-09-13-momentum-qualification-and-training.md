# Momentum qualifications, completed training and final-centre validation

## Future training throughput review — 2026-09-13 17:28 UTC

A bounded Sol source/timing review identified a possible saving for future
final-centre-only campaigns. Root reproduced the timing arithmetic from the
original M native `log.jsonl` files under
`S/unitorder/momentum_train_v3_evidence_20260913/`, using `gen` and `secs` only.
Seeds311/312 averaged624.8925/609.42125 seconds for generations2-9; generation10
took1213.35/1131.87 seconds, an additional588.46/522.45 seconds. Generation1
took859.88/852.83 seconds; its excess is consistent with compilation/warmup,
but these aggregate timers are not a profiler attribution.

The population evaluation dominates recurring work:4096 candidates times124
episodes gives507904 full-season rollouts, in62 chunks of8192. The frozen
trainer performs its gradient/update before the absolute/champion measurement
block (`src/kagg3/es/train.py:5188-5286`). That block runs when either cadence
fires, so changing `abs_every` alone would not remove the generation10 cost;
`champ_every` remains10 and currently lacks a CLI option. The timing and source
support investigating deferred measurement, not a measured speedup yet.

A future paired diagnostic should start from identical saved pre-final state
and compare normal versus deferred cadences. Require equal raw update evidence
and exact theta/m/v and sampling RNG state. Full checkpoints would deliberately
differ in best/champion/history/report metadata. This is unsuitable whenever
selection, a gate, a restart, or subsequent training depends on that metadata.
No current H/J source, configuration, remaining arm or selection rule changed.
No diagnostic has been launched and no intermediate checkpoint was selected.

## Decision research and parity preparation — 2026-09-13 17:15 UTC

Two bounded Sol reviews completed the renewed decision-research request,
covering sales and planting. Root checked the sale inequality and head wiring
against the frozen source. No policy, training input or control mode changed.

The strongest sale hypothesis is an integer reservation crossing: in
`core/sell.py:136`, equality is admitted (`best_adj >= hold`). Raising hold
from the adjusted marginal to one coin above it rejects that unit; lowering
it back admits it. Compare actual/zero/lag2 hold and press, then all six plan
arrays and per-product sale quantities by lot. Flag terminal liquidation and
forced overflow because they bypass learned reservation. H's w2/b2 can change
product scores and hold, but cannot directly change the separate w3 gate;
J's mh can change hidden state and hence gate/press (`core/policy.py:650-670`).
Pressure changes may redistribute sales within a day without overnight retention.

The strongest planting hypothesis is a small correction near an existing crop
allocation boundary. A changed grow score must survive maturity/saturation
masks, free-tile limits, seed ownership, shared cash/shed grants, and route/labor
admission (`core/brain.py:962-1067`, `core/plan.py:4445-6143`). Compare exact
BUY_SEED and PLANT rows, then accepted engine events. Owned seeds can permit a
changed planting without any changed seed purchase. Existing command/replay
artifacts do not expose internal budget grants; do not claim to observe them.
The worse tomato maturity forecasts still provide no support for naive price
extrapolation. This hypothesis retains the existing town/pipeline valuation.

For either mechanism, use the existing saved-action reconstruction to separate
direct accepted changes under equal full prestate and opponent action from
no-effect requests and later divergent trajectories. Report full-family own
money and margin unconditionally, separately by seed/family. Failure to observe
direct effects limits the demonstrated mechanism on these cases; it does not
prove momentum can never help elsewhere. Lag2 changes horizon and magnitude.
The 15/11 macro changes with zero complete-plan changes were original M results,
not current H/J evidence. At17:13:42 UTC the watcher reported both original
H/J processes live with generation9 completed; final-centre evidence was absent.

Commit628113b adds `--prepare-from-contract` to the existing parity helper.
It validates the assembled H/J contract, both saved audits, native training
proof, exact fixed census and complete execution dependency hashes before
writing a fresh schema2 manifest. Inline and on-disk contracts must agree.
All38 focused training/assembly tests passed, including dependency corruption
and missing contract-binding rejection; independent Sol review passed.
This preparation performs no policy inference or engine games.
The existing launch record has12 exact preparation argv and collection source.
Assemble strength once, prepare all three history manifests before running the
judge (preparation validates fresh judge paths), then run local GPU parity.
No actual final H/J manifest or result is claimed by those prepared recipes.

## Final-centre handoff prepared — 2026-09-13 16:57 UTC

Both original remote processes remain live with exact commands and error null;
both native logs show generation7 completed. A bounded Sol handoff review found
no schema/path mismatch. Terminal receipts populate the cold/probe fields only
at completion, so their absence in live generation-boundary receipts is expected.

The existing campaign `launch.json` now records exact argv for remote and local
saved audits, all four strength assemblies, six J controlled assemblies, their
execution calls, and12 per-arm history parity recipes. These are explicitly
PREPARED_NOT_EXECUTED. The46 assembly/parity paths and six replay roots are fresh.
After each first arm's terminal PASS and raw evidence collection, require both
independently executed audits to agree before launching its same-seed opposite
arm from the original frozen argv. Native g10 only; each arm starts fresh B.

Generate each schema2 parity manifest from the verified final proof when it
exists; assembly does not perform parity. Use the authorized local GPU after
checking activity, allowing both remote GPUs to continue the second training
pair. The existing parity helper supports actual/zero/lag2 and exact H/J masks.
Its120 snapshots are dawn-seat states from two fixed training episodes, not120
independent episodes. H must be history-invariant and J must agree on day0.

A second Sol review found that existing macro and six-array plan outputs already
expose integer crop quotas/value multipliers, hold/press and planned purchases,
planting and sale timing. Use those arrays first. Equal aggregate counts do not
prove equal plans; all timing, unit positions and arguments matter. Emitted seed
purchases are requests, not accepted fills or a direct view of budget grants.
Raw logits, maturity/absorption gates, budget thresholds and labor-admission
causes are hidden function locals and cannot be inferred from counts alone.
No additional diagnostic code, policy input or training arm was introduced.

## Exact executed-action attribution — 2026-09-13 16:48 UTC

Commit7ed48d8 completes accepted-event attribution in the existing saved auditor;
no additional helper was created. It reconstructs both seats' saved actions
through an isolated copy of the pinned official engine, using the original seed
and schedule selected by the bound staged town loader from the bound town file.
The original end-of-day function runs before the town prefix is applied. All40
control opponents have entries in that schedule. Runtime proof now also pins
the engine's sibling specification JSON, which the Python source hash alone
does not cover. Framework identity remains version/runtime-bound rather than
hashing every framework file.

Every one of720 frames must match before events are returned: both private
states, all other observation fields, actions, rewards and statuses. Only
remainingOverageTime is excluded. Market records carry the original commit's
accepted Boolean and exact one-unit price. All unit calls carry requested and
effective commands, position/tile context, and complete farm/private hashes
before and after; generic accepted effects mean state mutation, so legal no-ops
are retained without claiming an effect. PLANT additionally requires the exact
crop/tile creation and one-seed decrement, preserving atomic same-crop blocking.
Hire/land records retain their mutation and cost evidence.

Comparison separates changed accepted-action identity from price/cost/context
changes. Direct attribution requires equal full prestate and opponent action
before any earlier state divergence; it refers to the entire changed own action
vector. Earlier no-effect requests do not prevent finding a later direct effect.
Later divergent states remain descriptive. Full-family money summaries are
unconditional on whether actions changed, with seeds and families separate.

All80 focused tests pass:26 saved-auditor,23 runtime,10 execution and21 assembler
tests. The pinned-town fixture plays four complete staged B games under
vanilla/actual/zero/lag2 and reconstructs all three controlled replays exactly;
their event hashes agree. Authentic engine fixtures verify tight-cash HIRE
ordering, rejected purchases, duplicate and atomically blocked planting,
movement, one-coin-floor sales, both seats' private-state corruption rejection,
and isolation from a poisoned registered engine. Synthetic comparisons check
no-effect requests followed by direct effects, confounding, incomplete evidence
and price-only changes. An intermediate test incorrectly expected a floor-price
sale to increase inventory; its expectation was corrected to engine semantics.
Independent Sol implementation review passed after expanding unit coverage and
separating action identity from price consequences.

Both original remote training processes were live with exact commands and no
receipt error at16:48:02 UTC; both native logs show generation6 completed. No
final H/J centre or actual controlled/strength result exists yet. All175 frozen
campaign inputs and the campaign manifest were rehashed unchanged. Continue
the original jobs; final-centre audits/parity and the frozen evaluations follow
their terminal completion. These changes establish measurement capability,
not an improvement over B or achievement of the public objective.

## Decision research requested again — 2026-09-13 16:32 UTC

Three bounded Sol reviews completed: `momentum_decision_review` traced planting,
`next_lever` traced trading and purchases, and `scope_protocol_review` assessed
resource and production history. Root checked the cited decision paths and the
frozen decision contract. These are source reviews and hypotheses, with no new
fit, game, policy change or training arm. Reuse the existing snapshot and engine
helpers; preserve the current campaign's actual/zero/lag2 controls and separate
seed/family results.

1. **Sell or retain is the shortest actionable path.** Inventory momentum feeds
   encoder and grow/sell scores (`policy.py:650-659`); the encoder also feeds
   timing pressure and the global outputs (`policy.py:660-675`). Decoded `hold`
   and `press` are integer coin thresholds (`brain.py:1045-1067`). The existing
   allocator sells a unit only when a lot's adjusted marginal clears `hold`,
   except forced liquidation; `press` shifts allocation among existing lots
   (`sell.py:85-138`). Trace changed thresholds through actual lot quantities
   to accepted SELL events. Overnight retention comes from quantity/hold, not
   a later intraday lot. A rising quote cannot cause a useful sale without
   available goods, and changing a request does not prove an accepted trade.
2. **Planting has several discrete filters.** Crop softmax becomes integer
   quotas after maturity and oversupply gates (`brain.py:962-1039`); wants then
   compete for seed room, cash and integer grants (`plan.py:4733-4825`,
   `budget.py:146-247`). Trace final-centre actual/zero differences through
   quota, requested/granted seeds, executable plant count and legal commands.
   A PLANT may use already-owned seeds, so a changed BUY_SEED is not required
   for every planting effect. Boundary-distance or altered-value probes are
   optional future diagnostics requiring a prospective specification; they
   must not become a selected multiplier or change the frozen candidate.
3. **Purchase and labor valuation use different price horizons.** Seed grants
   price output against town-projected maturity inventory and own commitments
   (`plan.py:4802-4825`), while PLANT task admission uses units times today's
   quote, then grow/development multipliers (`plan.py:5698-5727`). This is a
   confirmed code difference, not proof of a bug or profitable replacement.
   First establish cases where funded planting loses specifically at labor
   admission. Any later valuation experiment must include displaced work and
   actual harvest/sale outcomes. The completed tomato 8/11-day diagnostic
   still supplies no support for naive one-day momentum extrapolation.

Additional own-stock history could describe persistent selling/transport
shortfalls, and opponent public-forecast history could describe commitment
changes. Neither is an existing J input. Current shed, production clocks and
opponent +1/+3/+7 forecasts already supply much of that information. A rolling
forecast difference mixes aging, harvest, death and replacement; it is not an
identified supply shock. Incremental value remains unproved. Defer additional
history blocks, acceleration and residual-history controls; do not silently add
a fourth mode to the current campaign.

The strongest existing measurement remains the attenuation result: original M
changed macros on15/120 and11/120 dawns but changed no full plans. Final H/J
centres are still unavailable; whether joint training crosses useful thresholds
is unmeasured. At16:27:47 UTC both original training commands remained live and
their native logs reported generation4 completed. Root's separate initial-state
comparison at16:22:26 UTC passed against each arm's qualification; the executed
source and full comparison are preserved in `qualification_comparison.json`.

The next implementation work is exact event attribution in the existing saved
auditor. Both execution reviewers agree that the older replay profiler cannot
prove exact fills: it accounts for HIRE/BUY_LAND after variable trades, whereas
the official engine executes them at their queue slots. Reconstruct both seats'
saved actions through an isolated pinned engine with the bound original seed
and town schedule; verify every game-state frame before accepting wrappers'
successful trade and planting events. Preserve original end-of-day random draws
before applying the pinned town prefix. Equal pre-state/opponent action permits
attribution to the changed own action vector; coupled sub-actions or subsequent
diverged states require more limited descriptions. This integration is not yet
implemented. The frozen usefulness contract continues to require legal executed
changes and paired own/margin outcomes versus both controls, separately by seed
and family; no sensitivity-only or J-versus-B claim establishes usefulness.

## Engine controls implemented; maturity-horizon result — 2026-09-13 16:12 UTC

Commit438002a extends the existing assembler, execution wrapper, runtime proof
and saved auditor for actual/zero/lag2 history controls on LOSS10 then LIVEC-H30,
the exact order in the frozen training manifest. Candidate identity remains the
native J seed name. The optional paired `--history-mode` and `--replay-root`
arguments create distinct controlled CSV/log/replay paths; the default seven
strength families remain unchanged. No standalone judge/helper was added.

The runtime reuses the frozen evaluator's `seed_lists`, `_play` and `CSV_HEADER`
with the same four-worker fork pool, exact town schedules and shipped switches.
A fresh per-game/per-seat macro wrapper changes only previous market inventory,
records all30 consumed dawn inputs, and restores its hook after the game. It
does not modify frozen training or staged evaluator files. Complete720-frame
replays bind the exact history delivery, terminal money and source identity.
Execution and saved audit reject missing or refused actions/statuses. Saved
comparisons retain both seats, all boards and each family separately, reporting
own/opponent/margin uncertainty and win changes. They distinguish submitted
actions from economic-state changes; exact executed quantities still require
classification from the real changed transitions before a usefulness claim.

The integration also fixes a real eligibility bug: the momentum-only array
reader would reject H/J changes to the output head. Its candidate-aware mask
now permits only H's130 or J's196 declared coordinates, leaving all others
byte-equal to padded B. H's66 momentum coordinates remain zero; legacy M's
6789-coordinate prefix remains strict. Missing H/J momentum layout is refused.

All67 focused tests pass. Four complete staged B games against its saved file
package are identical under vanilla/actual/zero/lag2, including full engine
steps; all30 history inputs and per-game restoration match. The saved auditor
accepts these real control replays and rejects a deliberately corrupted history.
Independent Sol integration review passed. These are fidelity fixtures, not
H/J candidate results. Both original training processes were verified live at
16:12:40 UTC, and native logs show generation3 completed for each. No native
final H/J centre, final parity or controlled/strength campaign exists yet.

The maturity diagnostic below completed on the exact120 training episodes;
root reproduced its report byte-for-byte and verified episode identities.
All2160 episode/product records and executed source are preserved under
`maturity_horizon_research` in the existing sensitivity JSON. Source SHA256
`d20a708343122f0eeda2f59b881a9660b5eefeac1100271f2ccef6a70f9fbdc1`;
report SHA256 `4983bb2ed482ef1682d831339ac53eca411380350dc5a6dcd31bd87a013bdc8e`.

Tomato mean per-episode quote MAE, in coins:

| Horizon | Hold current inventory | Current town demand | Raw previous draw | Town-corrected draw |
| --- | ---: | ---: | ---: | ---: |
| 8 days | 14.8060 | 5.2810 | 5.9187 | 5.2786 |
| 11 days | 19.1134 | 8.1417 | 8.8194 | 8.1417 |

Raw one-day momentum extrapolation is worse than current known town demand at
both tomato horizons. Correcting shop-demand changes returns essentially to
that baseline. This does not support a naive momentum-driven tomato planting
rule. Product behavior differs: strawberry and fertilizer retain some naive
longer-horizon predictability, while milk/wool do worse than holding the current
inventory in this comparison. Every product/horizon remains in the report;
none becomes a selected rule. Continue prioritizing actual sale and planner
admission changes in the frozen H/J campaign. No new policy or training arm
follows from this descriptive forecasting check.

## Prospective maturity-horizon diagnostic — saved training observations only

Before examining these new targets, freeze a no-fit diagnostic on the existing
120-episode dawn dataset (SHA3793fd2d2fd3d2e1230de9c179708ddd8bd1d7e99d0eb25a72e0dd288d6f1c4d).
Use seat0 only after verifying shared-market rows agree between seats. For each
product and each horizon h in {8,11}, use all current days d>=1 with d+h<=29
within the same episode. Compare next-horizon quote errors from (a) current
inventory held constant, (b) current inventory minus h times currently known
daily town demand, (c) current inventory minus h times the preceding dawn's
stock draw, and (d) the same raw draw corrected by the change in currently known
town demand. Quote each predicted inventory through the existing default price
table. Verify actual future quotes against their recorded stock before scoring.
Retain per-episode/product results and separate horizon/product summaries; fit
no coefficient, choose no product-specific rule, and use no judge observations.
The diagnostic tests naive persistence at planting horizons. It cannot establish
incremental value over all current policy features or counterfactual crop profit.

## Decision research follow-up and live H/J training

At15:44:51 UTC both original training helpers were live with exact commands:
311H PID1191048/session73451 on GPU0, started15:31:10.129154 UTC;
312J PID1191145/session61744 on GPU1, started15:31:18.313510 UTC.
Both receipts had error null and phase `generation1_boundary`; that persistent
phase does not report the current generation. Preserve both10800s runs.
The subsequent311J/312H training arms have not launched.

All four qualifications passed remote and local saved audits, with identical
audit bytes for each arm. Root independently compared every arm to its original
per-seed M probe and full cold/installed snapshots, and checked the exact130/196
mask, RNG keys and all2048 masked noise rows against the saved scope diagnostic.
All58 collected files per qualification and each archive were hash-verified.
The campaign's existing `qualification_comparison.json` retains the executed
comparison/collection sources, raw-member custody and separate results;
`launch.json` records terminal qualifications and current training handles.
The original remote source symlink is retained as metadata, not recreated locally.

Three Sol tasks reviewed decision mechanisms and shared evaluation wiring.
Their main hypothesis is that integer decoding and planner admission attenuate
the continuous momentum signal: macro changes can leave crop quotas, budget
grants and sale thresholds unchanged. This is consistent with the completed
M snapshot results, but individual suppressed boundaries were not yet traced.
H changes grow/sell output weights; these scores also feed the global head.
J adds history-dependent encoder/score changes and can directly change the
per-product sale timing output through the encoder. H cannot directly change
that timing output, though its downstream plans can still change.

Prioritized decision hypotheses and their falsification:

1. **Sale quantity and timing.** `hold` gates total sold units and can retain
   stock overnight. `press` penalizes later lots within the current day; reducing
   it can move sales later, but is not overnight retention. Inspect the existing
   fixed120 dawns for actual/zero/lag2 differences in the marginal-versus-hold
   comparison, allocated SELL quantities and canonical commands. Separate forced
   overflow and terminal liquidation, where learned thresholds can be bypassed.
   Strawberry and milk are plausible products to inspect based on the saved
   one-day forecast comparison; no product-specific policy rule is selected.
2. **Crop quota and admission.** Follow grow scores through integer targets,
   seed wants, candidate value/cost, budget grants and PLANT/BUY-SEED commands.
   A changed target alone is insufficient. A surviving tomato planted on d has
   up to four scheduled production events on d+8 through d+11, subject to the
   season horizon. One-day rising quotes do not establish a payable planting
   opportunity at those dates; known shops, seed/labor costs, displaced crops
   and the price effect of our own future supply must be considered.
3. **Input purchase timing.** Wheat/fertilizer scarcity could change retention
   or purchase timing, but own trades, cash costs and storage strongly confound
   this signal. First establish a canonical BUY_PRODUCT/SELL change; do not add
   another feature or start another training arm on forecast error alone.

Use the existing snapshot helper and shared judge for these checks. H must be
invariant to history controls. J must agree across controls on day0; its trained
H coordinates mean day0 need not equal B. Future replay quotes can check
direction or horizon only under the recorded trajectory: changed candidate
sales/planting alter later stock, price impact and opponent interactions.
Useful action and money claims require the already specified paired engine
controls on complete families. Snapshot counts do not establish such a claim.

Commit2a19be1 routes the four exact H/J candidates through shared assembly/parity
through the frozen campaign proof and binds snapshot history mode. Independent
review found and root fixed acceptance of a single campaign argument on legacy
candidates and insufficient candidate-label closure; runtime now also checks
the label against the audited arm/seed. All40 focused assembly/execution/runtime
tests pass. Actual/zero/lag2 engine outcome routing remains to be implemented in
existing tools before those controlled games can run. All seven strength
families stay unchanged. No real final H/J candidate or end-to-end H/J parity
result exists yet.

The saved no-fit forecast follow-up is retained inside the existing
`momentum_initial_macro_sensitivity_20260913.json`, including both executed
sources, full per-episode/product reports and hashes. Root independently
reproduced the raw-versus-adjusted report byte-for-byte. The adjustment is
`previous_draw + town_now - town_previous`; it differs from raw momentum only
on960/3360 episode-days with changed known shop demand. Product effects are
small and mixed: median tomato quote MAE .07143 to0, strawberry5.91071 to5.82143,
milk13.69643 to13.46429; wheat and wool worsen, melon and fertilizer tie.
These descriptive training-corpus results do not justify another general
residual feature and do not show improved actions. Preserve the earlier fixed
predictor outputs and the frozen H/J campaign unchanged.

## Prospective H/J comparison — 2026-09-13

The completed scope screen motivates four fresh ten-generation runs, without
changing the agent architecture. Use the original43-file momentum training
source, B, ordered120 tapes and original124-episode configuration. H trains
`w2,b2` (130 coordinates); J trains `mh,ms,w2,b2` (196). Each starts separately
from padded B with zero moments, fresh seed-specific RNG and initial pool.
J never inherits H. Native generation10 is the sole candidate from each run;
do not choose a best intermediate, best seed, or combined result.

| GPU / seed | First arm | Second arm |
| --- | --- | --- |
| GPU0 /311 | H | J |
| GPU1 /312 | J | H |

Each arm first receives a separate actual-CLI zero-update qualification using
the same helper and configuration as its training process. The qualification
stops immediately before generation1. Verify its raw initialization, masked
noise and fixed coordinates before training; qualify/train snapshots must
match exactly. Compare each mask's generation-zero noise with the corresponding
coordinates in the already-saved full scope noise; compare keys and host field
allocation state within seed. Mask changes are expected; baseline initialization
and randomness are not retuned. Fields can diverge after learning changes play;
do not treat different training curves as paired candidate fitness.

Use separate fresh outputs and one process per GPU. Qualification has900s;
each training arm independently has10800s, with kill10 and22000MiB ceiling.
Retain the existing0.05s NVML monitor and0.2s maximum gap, exact compute-PID
coverage, source/input hashes, and terminal cleanup before the next arm. Never
restart because an observation timed out. A refused arm stops that sequence
for diagnosis; no automatic retries, changed limits or reduced evaluations.
Both seeds and all arms keep separate evidence.

Reuse existing `momentum_train_prepare.py`, `momentum_train.py`,
`momentum_train_protocol.py` and `audit_momentum_train.py` with explicit campaign
options. The original M execution mode and immutable source remain available.
Install into a fresh remote project root so earlier run inputs remain intact.
Freeze exact configs/commands/source hashes before any qualification launch.

Before interpreting a native centre, use the existing120 recorded training
dawns with actual, zero and lag2 history. Zero means passing current inventory
as previous, producing `(previous-current)/T == 0`. Lag2 uses the inventory
from two completed dawns earlier and current inventory on days0/1. It uses no
future data or cross-episode history. H must remain invariant to all three modes;
J must retain its day0 zero-history behavior. Require NumPy/CUDA agreement and
report changes in all12 macros and six full-plan arrays separately by seed/arm.
These recorded snapshots establish sensitivity, not realized decisions.

Sol's subsequent scientific review clarifies the fixed lag2 control: if
`x_d=(I[d-1]-I[d])/T`, then lag2 is `x_d+x_{d-1}`. It changes horizon and scale;
it cannot isolate recency. Actual-versus-zero tests history dependence, while
actual-versus-lag2 compares one-day and two-day cumulative encodings. Keep the
frozen campaign unchanged. If later mechanism evidence warrants it, a separate
same-scale stale-flow control could synthesize
`previous=I[d]+I[d-2]-I[d-1]`, yielding exactly the previous day's change.

For outcome attribution, freeze the same J weights under actual/zero/lag2
history and use the existing shared judge on LOSS10 and LIVEC-H30, maintaining
their separate paired boards/seats. Record legal executed action changes and
per-game own/opponent money. Report each control contrast on the complete
predeclared family, including games without changed actions; conditioning the
headline statistic on changed games would bias it. Show board-paired uncertainty
and wins/losses. A usefulness claim requires identifiable executable changes
and positive own/margin evidence against both controls in each seed, rather
than treating sensitivity or an isolated positive mean as proof.

All four native actual-history centres receive the unchanged seven-family
strength comparison against B, with H/J comparisons reported separately.
No result from this campaign alone automatically merges or promotes a model.
The top-five objective, competition rules and no-pooling requirement remain.

## Decision research and completed scope screen — 2026-09-13 14:52 UTC

Both no-update M/H/J diagnostics completed within their original900s bounds,
exit0, at14:40:05 UTC (311) and14:40:10 (312), about510s each and4952MiB peak.
Both root saved audits PASS: exact qualification state/masked noise, shared
field, masks, numerical runtime, raw fitness, scope-local ranks, gradients,
and raw odd interaction. Collection verified each six-member archive before
extraction. Campaign `results.json` embeds the executed collector and auditor,
receipt/input identities, corrections to auditor schema assumptions, and all
separate results. The initial auditor refused an unrecorded bytecode environment
field; the frozen serializer records numerical flags only. The wrapper binds
that bytecode setting. No numerical tolerance, diagnostic input, or run changed.

| Independent seed | J/H money-changing candidate-episodes | J/H differing own / relative components | Odd own / relative RMS | J blended gradient RMS on66 momentum coordinates |
| --- | ---: | ---: | --- | ---: |
| 311 | 1391 /7936 | 64 /64 each | .0009736675 /.0032472185 | 3.2141 |
| 312 | 1290 /7936 | 64 /64 each | .0009608697 /.0043023451 | 4.1196 |

Money counts use only mine/theirs terminal coins, excluding other rollout
metrics. Each raw odd interaction has32/32 nonzero pairs; each J gradient has
66/66 nonzero momentum coordinates. Seeds are not pooled. These observations
meet the prospective training-signal review gate; they do not establish
superiority. A J gradient on momentum coordinates can include noise associated
with H perturbations. This diagnostic saves money/fitness, not plans or actions.

At the user's request, Sol `next_lever` traced momentum to decisions and Sol
`scope_protocol_review` independently reviewed the training mechanism. Their
shared finding is a discrete decision bottleneck: normalized stock change
(`core/brain.py:128`) enters shared hidden/grow/sell paths (`core/policy.py:650`),
then integer crop allocation, holding/pressure/value multipliers
(`core/brain.py:962,1041`), then seed/tile/budget and marginal-sale constraints
(`core/plan.py:4733,4802,6618`). A changed macro can leave the same feasible
plan preferred. The current learned tails showed zero full-plan changes on120
snapshots per seed; even16x changed only one. Larger weights alone are not a
demonstrated solution.

The next candidate comparison should reuse `--train-only` for H=`w2,b2`
versus J=`mh,ms,w2,b2`, with native centres and existing B/M references. H is
essential because it changes decisions without history. Before launch, freeze
run bounds and the comparison, and specify matched actual-history versus
zero-history and past-only mismatched-history checks. Those checks must identify
legal executable BUY/PLANT/SELL changes and their own/relative money outcomes;
more changes or J beating B alone cannot attribute improvement to momentum.
Evaluate each seed and each existing judge family separately. This is a research
recommendation, not a launched training campaign or promotion decision.

Feature proposals were challenged against existing code to avoid duplication:

- Separate previous-price carry is redundant under known default market
  parameters: the existing price table maps previous inventory to quote. A
  quote-delta transform may improve conditioning but adds no new information.
  Hidden randomized training market parameters require separate consideration;
  they do not justify adding a feature for the default competition setting.
- Stock momentum includes town consumption and player activity. Existing
  `inv_at_day` already models town/shop demand, while `board_forecasts` and
  `production_forecast` model public production timing. Adding the full observed
  stock delta to those forecasts can double count their baseline effects.
- A bounded research alternative is a completed-day player-flow residual:
  current stock minus previous stock plus actual completed-day town consumption,
  with the engine's caps/floors respected. First compare the existing one-day
  baseline with a past-only residual correction by episode/product. Only a
  predictive improvement justifies testing longer crop-maturity horizons or
  connecting it to planner valuation. It is not yet a validated feature.

The residual must not be labeled opponent demand: after exact town/shop drain
is accounted for, it still combines both seats' effective inventory changes.
Floor-priced sales do not add inventory, and buys/sells depend on affordability
and simultaneous quote walks. Isolating opponent flow would require subtracting
our actual committed inventory changes, not requested orders. It decomposes
the existing stock delta rather than supplying independent demand evidence.

No new model code, full training run, merge, or submission follows this screen.
B remains incumbent and the top-five goal remains unmet.

Both original ten-generation runs completed successfully on 2026-09-13.
Seed312's complete engine evaluation passed execution and independent audit,
but its sparse, mixed differences do not establish stronger play than B.
Seed311's evaluation and independent audit also passed. B remains incumbent; the feature branch is
unmerged and the top-five objective remains unmet.

Seed312 completed at 13:50:31.809760 UTC in 1178.652 seconds. Each of its seven
runners exited zero without timeout or cleanup actions. Inputs and runtime
identity remained exact; the shared lock was released. The existing saved
auditor's output and Sol's independent rerun are byte-identical, SHA256
`00077f232b57d776f4d6498131d5bd90cf798bd6a14fd3c08021d0617fc75e30`.
The terminal execution SHA256 is
`a09ddfd2105b5dd98f62c97e3fe54252b38e8316e7fcaec4e5c0420e952a7e28`;
the saved-audit manifest SHA256 is
`9dd8219cfa1d167580ad241e5111152b2a9aa2507ab44d196210ec9d2bc6a27c`.
Receipts, CSVs and runner logs are retained at their original campaign paths.

| Seed312 family | Boards / games | Own coin delta | Opponent delta | Margin delta | Board SE | t | Identical margins |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TOPB2 | 20 / 40 | 0.00 | 0.00 | 0.00 | 0.00 | — | 40 |
| LIVEC-H30 | 30 / 60 | +47.37 | -3.20 | +50.57 | 50.57 | 1.00 | 58 |
| LIVEC-H30B | 30 / 60 | -3.65 | -1.13 | -2.52 | 2.52 | -1.00 | 59 |
| LIVE62 | 62 / 124 | +29.94 | +2.94 | +27.01 | 20.86 | 1.29 | 121 |
| LOSS10 | 10 / 20 | -103.05 | -23.50 | -79.55 | 79.55 | -1.00 | 18 |
| NEXT30 | 30 / 60 | +1.13 | +0.60 | +0.53 | 0.53 | 1.00 | 58 |
| NEXTHIGH | 30 / 60 | 0.00 | 0.00 | 0.00 | 0.00 | — | 60 |

Every family has zero won/lost flips under the auditor's strict-win definition.
Each row compares the candidate with pinned B on that family's paired boards;
there is no pooled result or newly selected promotion threshold. These outcomes
are consistent with the sparse plan sensitivity recorded below, but do not
identify the cause of training's limited response.

Seed311 completed at 14:11:36.641961 UTC in 1216.775 seconds, original session
`36628`, PID `79093`, exit zero. All seven runners and both runtime preflights
passed; inputs remained exact and the shared lock was released. Campaign and
independent Sol saved audits are byte-identical, SHA256
`867f59ec4fcceb693f1382d9cc40203c9d76e44fc03f5f2bcd09c25868d44f53`.
Terminal execution SHA256:
`c544b2d1bde0db4ed819981bd2b0e267fa6b6adfd0ed531f16a99dfca51e52b8`;
saved-audit manifest SHA256:
`42b52d97219174d02e2ada322924ab98735e665e8025118e0ac2cf34f6f87f1b`.

| Seed311 family | Boards / games | Own coin delta | Opponent delta | Margin delta | Board SE | t | Identical margins |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TOPB2 | 20 / 40 | 0.00 | 0.00 | 0.00 | 0.00 | — | 40 |
| LIVEC-H30 | 30 / 60 | +47.37 | -3.20 | +50.57 | 50.57 | 1.00 | 58 |
| LIVEC-H30B | 30 / 60 | -3.65 | -1.13 | -2.52 | 2.52 | -1.00 | 59 |
| LIVE62 | 62 / 124 | +29.94 | +2.94 | +27.01 | 20.86 | 1.29 | 121 |
| LOSS10 | 10 / 20 | -103.05 | -23.50 | -79.55 | 79.55 | -1.00 | 18 |
| NEXT30 | 30 / 60 | +1.13 | +0.60 | +0.53 | 0.53 | 1.00 | 58 |
| NEXTHIGH | 30 / 60 | 0.00 | 0.00 | 0.00 | 0.00 | — | 60 |

Every seed311 family also has zero won/lost flips. Root additionally compared
the raw candidate CSV files: seed311 and seed312 are byte-identical within
each of the seven families, despite distinct trained theta files and separate
executions. These are separate reports, not pooled measurements. Neither
candidate establishes an improvement over B; no promotion or merge follows.
No additional full training arm has been launched.

| Seed | Finished UTC | Training seconds | Peak MiB | Monitor samples | Maximum gap seconds |
| --- | --- | ---: | ---: | ---: | ---: |
| 311 | 13:19:20 | 7334.307 | 9702 | 146687 | 0.06988638 |
| 312 | 13:15:50 | 7123.846 | 9702 | 142477 | 0.06485392 |

Each wrapper exited0, execution and training receipts passed, all ten updates
completed, input hashes remained exact, and the expected helper was the sole
GPU compute process. Both process groups and terminal GPU app lists were empty.
No timeout, restart, changed limit or intermediate-model selection occurred.
Generation10 includes the configured absolute/champion measurement before its
log row:126 opponents ×64 pairs ×2 seats =16128 evaluator rows. Its new shape
can compile separately, explaining the observed CPU-heavy tail as a source
inference; checkpoint serialization occurs after the log.

Complete84-member archives are retained in `/tmp` and safely extracted to
`S/unitorder/momentum_train_v3_evidence_20260913/`, preserving both raw roots,
six adjacent sidecars per root and the exact remote source-link targets.
Remote/local archive identities and every member agree. Existing top-level
launch records were preserved by choosing this fresh collection parent after
the extraction guard refused an initial path collision before writing.

Root local and independent Sol remote saved audits are byte-identical per
seed:311 `2a172a4c5dc8be13e1c259d0a6d084f1caed12dd188bcb35d1926ab17df8a0fa`,
312 `4969594ccacb00ba5938b25af947822b2efc83944f09771ed0384d64de7f9e28`.
They use the unchanged frozen auditor. Both final native float32[6855]
centres retain B's first6789 coordinates exactly; all66 momentum coordinates
are finite and nonzero. Exact final hashes and collection/source custody are
in the saved audit and download-custody JSON files alongside the roots.

The existing `momentum_zero_compat.py` then checked each native centre on the
same120 recorded training dawns, with exact audited source, real previous-dawn
history and the training numerical environment. All12 macro fields and six
full-plan arrays agree byte-for-byte between NumPy and CUDA. Seed311 took
267.019s, seed312260.687s, within the600s per-worker bound. Their independent
manifests, metadata and receipts are under the same evidence parent. This
closes final-centre inference fidelity; it does not establish agent strength.

Both shared judge assemblies passed Sol review with the frozen seven families
and424 expected keys, exact source and history-aware evaluator scripts, and
unchanged four-worker/7200s settings. Seed312 completed in root session
32574; seed311 completed in session 36628. No promotion or merge yet.

Root and Sol independently compared the saved final NumPy outputs against
the exact B output from `momentum_zero_compat_r3_20260913/numpy_old.npz`
(SHAd15043f051b7fdd7e46b0ce08af538f377cfa4e6515615b05890fa37d216a4b9).
All120 ordered cases and current/previous market hashes agree, with identical
18 field names, int32 dtypes and shapes. Seed311 changes macros on15 dawns
(grow_mult14, hire_bias1, land_bias1; overlapping counts); seed312 changes
macros on11 dawns (grow_mult10, hire_bias1). Both change zero of the six plan
arrays on all120 dawns. This is a limited training-snapshot characterization,
not a trajectory or strength result. Inputs, exact comparison source and counts
extend the existing sensitivity artifact under `final_centre_comparison`.

Both fixed initialization qualifications passed, and the two ten-generation
training runs started at 11:17:06 UTC on 2026-09-13. This establishes valid
initialization and a live experiment; it does not establish stronger play.

| Seed | GPU | Qualification duration | Peak process memory | Maximum monitor gap |
| --- | --- | ---: | ---: | ---: |
| 311 | RTX3090 GPU0 | 260.569 s | 980 MiB | 0.082576 s |
| 312 | RTX3090 GPU1 | 259.339 s | 980 MiB | 0.070653 s |

The qualifications began at 10:58:29 UTC. Seed311 finished at 11:02:50 UTC;
seed312 finished at 11:02:48 UTC. Both wrappers exited zero and left no child
process group or GPU compute process. They stopped at the first-generation
boundary before a native generation or optimizer update.

The raw audit verifies the original 6,789 float32 B coordinates,66 appended
zeroes,exactly66 trainable coordinates,zero optimizer state,and identical cold
state before and after evaluator execution. It reconstructs the124 archetype
identities from saved evaluator input groups and their mean coins from the raw
output,then checks the rounded log values. The probe completes after the cold
snapshot;only its two result fields and the three documented B-install fields
may differ at the installed boundary. Every other full snapshot field agrees.

Both seeds use the same frozen source,configuration apart from seed/run,and
ordered120 action tapes plus four scripted opponents. Their raw RNG keys,
split keys,host RNG states,and masked perturbations differ. Source closure,
effective CUDA/JAX settings,process ownership,memory,cadence,and cleanup also
pass. Root and two Sol auditors produced identical deterministic audit bytes:

`255b838676310658b1b58767dacf0debabda7caf8fb37081f263e6f0473b1700`.

The final auditor is `audit_momentum_raw_qualifications.py`, SHA
`b107877a9f0b5b683f1d08e93739b7c266ab1ac285f35cd43bb15b4b77dbc5f4`.
Earlier auditor refusals incorrectly assumed only four probe entries and an
incomplete probe/install transition. Those failures and their diagnoses are
preserved. The source and successful qualification runs were not changed or
rerun to address these auditor errors.

The complete evidence archive is retained locally at
`/tmp/unitorder-momentum-qual-v3-evidence-20260913.tar.gz`, SHA
`6487a380021eb12e5eb38457afa539ab42ccd16a935dc6a8b26e33262ad5a319`,
108,511,499 bytes. Its154 collection nodes match after safe extraction under
`S/unitorder/momentum_qual_seed{311,312}_v3_20260913`. Exact remote source-link
targets were retained as metadata and never followed during extraction.

Training uses those seeds' own qualified states,original B,only `mh,ms`,
population4096,sigma0.01,SGD learning rate0.00018,and the existing objective.
Each process has a three-hour child limit and a22,000MiB memory ceiling.
The fixed ten-generation count and final-centre selection remain unchanged.
At12:40:02 UTC, both original jobs had seven completed generations, no receipt
error and no exit sidecar. Exact wrapper/helper commands were verified at
12:39:29 UTC, with both GPUs at100% and9058MiB each.
Their immutable inputs remain exact. No intermediate centre is
selected; the remaining work is completion, saved training audits, and judging
each native generation-ten centre separately.

The shared judge now supports candidate6855 versus baseline6789 and loads
policy and history-aware scripts from the persisted momentum stage. Commit
`87e8ae7` consolidated the duplicate implementations; `cfc9987` corrected its
assumption that the frozen auditor emits an auditor hash field. The executable
is instead verified through the exact training manifest bound by execution.
Twenty-one focused tests and an independent Sol source review pass. Actual
completed-candidate eligibility and evaluation remain pending training.

The incumbent B also passes the maintained NumPy/JAX CPU comparison on all
2,400 recorded fixture dawns (`cb79c62`), with zero history on that older fixture.
This does not validate nonzero final momentum weights. The two historical hire
bias differences affect a different legacy theta and reproduce before the
branch. No Kaggle submission or promotion has occurred.

Commit `2b80ac6` adds a maintained nonzero-momentum complete-plan test to
`tests/test_forward_value.py`. Separate mh/ms perturbations and changed MILK
history agree byte-for-byte across NumPy and CUDA for every macro field and
all six plan arrays (local RTX3070,250.88s). Actual generation-ten centres
still require their own inference checks after completion and saved audits.

Commit `fe2e2d1` extends the existing compatibility runner for those final
centres, reusing shared preflight and the fixed120 training dawns. Fifteen
assembly/parity tests and Sol's source review pass. Use a fresh manifest and
directories per seed, NumPy/CUDA backends and a declared600s worker timeout.
The helper enforces training numerical settings and records exact macro/plan
agreement. Historical zero manifests stay frozen and require their historical
Git helper revision for replay. No actual final centre has been checked yet;
the existing seven separate evaluation families remain unchanged.

Terminal collection was checked against the producer/auditor by root and Sol.
For each seed, wait for its `.exit` and `.finished` sidecars, zero exit, absent
original wrapper/helper/process group, and terminal execution/receipt PASS.
Collect the complete root and six adjacent sidecars: `.launch.json`,
`.launcher.log`, `.started`, `.log`, `.finished`, `.exit`. Preserve all cold,
installed, generation1/10, native artifact, private-stage, log and monitor
files; a final-theta-only download cannot satisfy the existing saved auditor.

Record remote type/size/SHA/link targets before and after packing and require
an unchanged tree. Archive without dereferencing. Before extraction, validate
unique contained member names, regular files/directories only except the sole
`train/work/src` symlink to that exact remote root's `train/private_stage/src`;
reject hard links, special files and descendants beneath the symlink. Extract
regular members into a fresh workspace location and preserve that symlink as
metadata. Keep the six sidecars adjacent to the root. Verify archive identity
and every extracted member against the remote manifest. Do not reuse the
OFF309/310-specific temporary collector without adapting its different layout.

Run the existing `audit_momentum_train.py` separately per seed under bytecode-off
Python, passing its own local qualification root, complete training evidence
root, `--seed`, and a fresh `--output`. Root and Sol must produce two distinct,
agreeing saved audit files. All191 frozen inputs and the e3c7 auditor remain
exact. At12:43Z the live roots each contained72 nodes and about208MB; only
their expected source symlink was present, and remote/local space was adequate.
This was a layout check; no mutable training evidence was collected.

At12:49:15 UTC both original wrapper/helper command pairs remained live with
eight completed generations, no receipt error and no exit sidecar. A separate
18.74s NumPy diagnostic used each seed's first16 saved initial noise vectors,
both signs, the fixed sigma0.01, and the existing120 recorded training dawns
with their real prior-day history. No games, plans, fitness, fitting or weight
selection were involved. The exact executed source, input hashes and detailed
counts are saved in `S/unitorder/momentum_initial_macro_sensitivity_20260913.json`.

| Decoded change versus zero-tail B | Seed311 /3840 | Seed312 /3840 |
| --- | ---: | ---: |
| Any macro field | 2472 | 2491 |
| Growth multiplier | 2230 | 2286 |
| Pressure | 382 | 330 |
| Hire bias | 288 | 256 |
| Hold | 185 | 180 |
| Development weight | 62 | 43 |
| Land bias | 60 | 42 |
| Plant target | 15 | 15 |

Animal deferral/want, compact, crew target and forward days were unchanged in
this sample. These field counts overlap and must not be summed. Every day0
macro was unchanged, as expected from zero first-dawn momentum and the frozen
B prefix. The data reject the blanket explanation that the nominal sigma
cannot change decoded macros. They do not establish actual action changes,
useful fitness signal, final-centre strength or a reason to change sigma.

Sol's code review confirms a stronger day0 invariant: every finite mh/ms tail
is multiplied by zero on the first observed dawn. With B's prefix frozen,
this experiment cannot alter B's opening macro or plan. That is a scope
constraint, not evidence that the opening causes losses. The adapter weights
are shared across products; different responses rely on the existing hidden
state and nonlinearities rather than nine independent learned directions.

If both final centres fail, Sol proposes researching the existing
`train_only=mh,ms,w2,b2` scope (196 coordinates) before any broader retraining.
The extra grow/sell output map can affect day0 and adapt the hidden product
state's response. It also changes B without history, creating a confound.
A prospective training-only decomposition would need B, momentum-only,
output-map-only and joint perturbations, separate seeds, both own/relative
fitness components, and executable-plan effects. The proposed interaction
contrast is F(joint)-F(momentum)-F(output-map)+F(B); exact sample sizes,
antithetic treatment and decision criteria remain undesigned. This is a
conditional research suggestion, not an approved experiment specification or
reason to change either current run. No new training arm has been launched.

The complete-plan diagnostic now covers that same first16-noise prefix, both
signs and120 dawns, with four NumPy workers (195.44s,600s bound). Every variant
reproduced its earlier macro-change count exactly. Results remain separate:

| Result /3840 fixed perturbation-dawn cases | Seed311 | Seed312 |
| --- | ---: | ---: |
| Changed macro | 2472 | 2491 |
| Changed complete plan | 15 | 15 |
| Changed rendered hour0 action | 0 | 0 |
| Variants with any plan change /32 | 14 | 15 |

The initial noise0 pilot had one changed plan per seed across its two signs;
the extension reused the original16-vector sample, without selecting vectors
by plan result. Exact sources, input hashes, changed-case plan hashes and
command details extend the existing sensitivity JSON. All15 changed plans per
seed contain different canonical PLANT and market commands, rather than only
ignored operands. Seed311 substitutions were MELON to STRAWBERRY/WHEAT;
seed312 substitutions were MELON to STRAWBERRY and STRAWBERRY to CARROT.
They occur later in the day; some unit rows do not exist at the recorded dawn.
Future hiring, legality, evolving state/history and game outcomes were not
simulated. Rendering respects the23-hour final day; hour0 uses the actual
recorded hand count. Day0 plans remain unchanged.

Sol's source review explains why macro changes can disappear: grow_mult
rescales integer candidate revenue, while purchases and routes change only
when a budget/admission/order/hire boundary is crossed. Pressure likewise
changes adjusted sale marginals, which may preserve the selected lots. Nearly
all observed plan crossings occurred at episode108089821 day11seat0. This is
sparse response on the fixed training snapshots, not proof of zero population
fitness signal: candidate trajectories can encounter different states. It
does not justify changing either live run or its sigma.

A further fixed training-snapshot diagnostic on 2026-09-13 measured the size
of the learned update before proposing a wider trainable mask. At generation
10, the 66-coordinate tail RMS was 0.000576758 for seed311 and 0.000508335
for seed312: respectively 5.77% and 5.08% of the fixed 0.01 exploration sigma.
Generation1 RMS values were 0.0000180815 and 0.0000148898. The existing trainer
intentionally applies momentum SGD without bias correction (`beta1=0.9`,
`lr=0.00018`); this observation identifies small movement, not an optimizer bug.

Before execution, the diagnostic fixed tail multipliers 1, 4 and 16, the same
120 training dawns, and actual-history versus zero-history controls. It reused
the existing compatibility parser and planner with two NumPy workers, finished
in 89.403 seconds inside a 600-second bound, and ran no games or fitness tests.
Its source, input hashes, checkpoint geometry and complete changed-case plan
hashes extend the existing sensitivity JSON under `final_scale_sensitivity`.
Raw report SHA256:
`5888199c304bb3cb18e805ec367518210700816621d05c2efae1a47cad829758`.

| Seed | Tail multiplier | Changed macro dawns /120 | Changed full plans /120 | Changed hour0 actions /120 |
| --- | ---: | ---: | ---: | ---: |
| 311 | 1 | 15 | 0 | 0 |
| 311 | 4 | 43 | 0 | 0 |
| 311 | 16 | 92 | 1 | 0 |
| 312 | 1 | 11 | 0 | 0 |
| 312 | 4 | 36 | 0 | 0 |
| 312 | 16 | 83 | 1 | 0 |

All zero-history controls reproduce B's macros and plans exactly. The 1x
results independently reproduce the saved final-centre comparison. Each 16x
plan difference occurs in episode108089821, day11, seat0. Multiplying the
learned direction changes many more macros, but complete plans remain sparse
on these snapshots. This weakens a simple small-update explanation for the
observed planning response; it does not rule out learning-rate effects during
training or establish the value of any scaled weights. No scaled candidate
has been selected, saved as a submission, or evaluated on judge families.

The next proposed no-update diagnostic has the following prospective scope.
Implementation and its tests are in progress in the existing trainer/CLI;
execution waits for implementation tests and review. Both judges are now complete.

- Start independently from each seed's original generation-zero B and its
  exact configuration and training randomness. Reconstruct the full 2048-row
  noise draw from the saved JAX key, then take the first 32 rows. Its masked
  momentum coordinates must match that seed's qualification preview exactly.
- Keep sigma 0.01 and compare M=`mh,ms`, H=`w2,b2`, and J=`mh,ms,w2,b2`.
  Candidate order is 32 M+, 32 M-, 32 H+, 32 H-, 32 J+, 32 J-: 192 candidates
  per seed. All scopes share the ordinary first-generation field: the 120
  pinned training tapes plus the same four residual training episodes, their
  exact seats, words, opponents, starts, tables, flows and tape controls.
  The four residual episodes need not represent four distinct scripted agents.
- Reuse the trainer's field construction, evaluator and fitness functions.
  Save raw per-candidate/per-episode money, full noise, masks and field identity.
  No optimizer step, absolute/holdout/champion evaluation, checkpoint selection
  or persistent trainer/RNG mutation is allowed. Ordinary initialization's
  training-rung probe is required to reconstruct the existing initial state.
- Compute own and relative raw fitness with the existing episode weights,
  clipping and tape treatment. Report the 32 antithetic differences, tie counts
  and RMS per scope, plus within-scope tied ranks, the configured 0.6/0.4 blend,
  and blockwise ES gradients. Seeds and scopes retain separate records.
- Compare J with H to distinguish history interaction from generic output-head
  retuning. For raw own and relative fitness, report the odd interaction
  `D_J - D_H - D_M`, where D is the positive-minus-negative difference for the
  same noise row. B cancels in this contrast; it does not measure even-order
  interaction. Do not interpret differences of separately ranked blends as a
  causal interaction: each scope has its own rank reference population.
- If J and H give identical raw money and fitness on both seeds, this sample
  supplies no evidence for researching the joint scope. A nonzero difference
  and added-coordinate gradient in each seed justifies training-signal review,
  not promotion or an automatic training launch. Disagreement is inconclusive.
  More sensitivity alone does not establish a better search direction.
- Use one bounded process per remote GPU, 900 seconds plus 10 seconds for
  termination, with the established numerical settings and 22,000 MiB ceiling.
  Freeze exact commands/source/input hashes after implementation review and
  before launch. Preserve raw results and execution/cleanup evidence. A timeout
  is an inconclusive diagnostic; do not retry with a larger limit or subset
  selected from partial results.

This specification replaces the earlier undefined sample-size suggestion;
it does not authorize a new full training arm or select any policy weights.

The no-update implementation reuses `Trainer.prepare_generation_field`,
`play_generation_field`, and `fitness_components` in the existing trainer.
The ordinary `generation` method uses the same factored path. The existing
CLI adds `--antithetic-scope-diagnostic`, requires an initial theta and the
fixed population4096/episodes124/sigma0.01 configuration, writes into a fresh
run directory, and returns before gates, training logs, updates or checkpoints.
Raw noise/keys/field controls, masks, money, fitness, ranks and gradients are
saved in one NPZ with a JSON metadata/state/runtime receipt.

Sol's focused tests passed: eight diagnostic/component cases, all16 existing
fitness-shaping cases, and14 remaining masking cases. Root separately replayed
the frozen original generation function against the refactored method with
real RNG/allocation/SGD but stubbed rollout money, using124-episode pinned and
unpinned fields and64 candidates. Evaluator inputs, return values and full
recorded post-state matched byte-for-byte in both cases (4.383 seconds).
Exact executed source/input hashes/results extend the existing sensitivity
JSON under `scope_refactor_equivalence`; raw report SHA256
`ef3d5b67e8cd939dba5a80bf65e4243c443df71ed4eb85cb52c7630e5c9bac79`.
This validates the refactor's orchestration and update behavior under those
fixtures; it is not a new simulator/engine or full-population CUDA proof.

Root's additional maintained checks passed for CLI refusal of an existing
output and promotion, independent within-scope ranks and the64-candidate
ES denominator, and pickle-free serialized raw paired differences/summaries.
The JSON now records the actual blend weights, separate per-scope tie/nonzero
counts, means and RMS, and raw odd-interaction summaries. State mismatch
refuses serialization before publication. The launcher review also added a
terminal peak-memory check, closing a final-poll-interval escape from the
22,000 MiB ceiling. These changes do not alter the trained models or judges.

Prelaunch review passed for the frozen scope manifest
`S/unitorder/momentum_scope_diagnostic_20260913/manifest.json`, SHA256
`b9f53eb2e0a46238a71c0d815b49ea2926b134bf73d61d9c29eff4dd8f3b23bc`.
It binds170 remote inputs:43 source files,120 ordered tapes, B, the existing
protocol/NVML monitor, and four qualification artifacts. Source commit is
`7a3bfe2`; only the existing trainer and CLI overlay the frozen source stage.
The688,547-byte bundle SHA256 is
`2e90c7864e838f8dabfdb1afa2deb42efca401a94815e71a93eb423fc247ecdb`.
Transfer and safe44-member extraction into the fresh remote source root
`/home/user/kagg3/artifacts/momentum_scope_source_20260913` completed, and
all170 remote input hashes matched. Sol verified the exact commands, ordered
tapes, environment, bounds and cleanup before launch. The inline execution
source is retained in the manifest; it adds no standalone repository helper.

Both scope diagnostics launched from that frozen manifest on their assigned
remote GPUs. Seed311: wrapper1170494, child1170497, original SSH session23352,
start14:31:34.724605 UTC. Seed312: wrapper1170591, child1170594, session34230,
start14:31:41.095665 UTC. Both exact processes were verified live; at roughly
one minute each GPU used532MiB during initialization/compilation. Preserve
these original runs and their900s bounds. Launch/installation records are in
`S/unitorder/momentum_scope_diagnostic_20260913/launch.json`; terminal results
have not yet been collected or interpreted.
