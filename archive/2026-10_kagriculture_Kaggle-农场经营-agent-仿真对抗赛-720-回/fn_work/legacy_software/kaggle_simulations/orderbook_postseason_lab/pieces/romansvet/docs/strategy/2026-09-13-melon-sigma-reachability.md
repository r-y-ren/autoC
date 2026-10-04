# Flow215 day-0 melon sigma reachability

## September 13 review: what to repeat or redesign

The historical results do not justify repeating a fixed melon opening. They
also do not establish that every learned crop allocation must avoid early melon.
The evidence has several different scopes:

| Experiment | Actual scope and result | Consequence for the next experiment |
|---|---|---|
| Forced `MELON_OPEN`, 4/6/8/12 tiles | Older lineages; repeated negative pinned evaluations. The 12-tile g350 arm lost 19,557 mean margin on 130 tapes. | Do not repeat the fixed opening merely because new losses show early melon revenue. |
| Delayed `MELON_FIRST_DAY=1/2` | Recovered timing-sweep report: zero crop claim on those days; the observed loss came from a forced DROP day. Disabling that DROP reproduced OFF. | These losses do not test successful delayed planting. |
| Funded `MELON_D1` | Separate flow58_g450 experiment reserved cash and nearby tiles, successfully planted earlier, and lost each of four engine opponent legs. | The inert timing sweep is not grounds to rerun the later funded opening. |
| `m0p1`, one extra day-0 melon target | B `flow193_g100_hr`, relative integer offset in a patched simulator; TOPB2 −14,435 and LIVE-C development −15,117. Integer-search §6 explicitly says engine confirmation was **not run**. | Negative coupled intervention: reproduced plans add land, four crop tasks and remove two animals. Not isolated one-tile value or a modern engine judge. |
| Learned floor, Flow184/184b | Separate 165-coordinate `g12,gb12` floor head on g1000. Flow184 learned to suppress non-wheat floors; the biased restart also lost. | Learned melon was tested. Do not describe the archive as only forced 12-tile experiments or repeat this floor unchanged. |
| Additive melon | Land/cash arithmetic and a proposed build; the additive doc explicitly says no arm was run. | “All additive variants failed” overstates the evidence. No new additive build is selected. |
| Flow215 sigma probe below | Two exact first populations, 1,191-coordinate mask, one dawn observation; zero melon targets. | Does not measure wins, the current H mask, or later updates. It is not an additional acceptance gate. |

Sources: [integer search](2026-09-11-integer-search.md),
[Flow184 check](2026-09-10-flow184-gene-check.md),
[independent check](2026-09-10-flow184-gene-check-B.md),
[September 10 verdicts](2026-09-10-verdicts.txt),
[September 9 verdicts](2026-09-09-verdicts.txt), and
[additive proposal](2026-09-11-additive-melon.md).
The old `S/melonroute` and `S/melonadd` raw directories are absent from this
checkout; their historical sim figures are documentary evidence, not newly
reproduced results. The route doc also contains inconsistent averages and an
unsupported causal interpretation of a cross-arm receipt difference, noted there.
Recovered helpers exist at `S/_recovered/melonroute/probe.py` and
`S/_recovered/melonadd/{land_probe,tape_land}.py`; the route helper's exact
original temporary output directory is also absent. Recovered reports at
`S/_recovered/melon_sweep/report.md`, `S/_recovered/melon_d0/report.md`,
`S/_recovered/melon_d1/report.md`, and `S/_recovered/melon_open3/report.md`
separate failed expressions, executed planting substitutions, and route repairs.
Their historical pooled summaries are not the current acceptance protocol.

The six fresh B losses in `S/ladder2/snapshot_20260913T203300Z/summary.json`
repeat the early production gap. A frozen-B day-0 trace locates the first
suppression in grow-score softmax allocation and integer rounding: the target
is `[11,11,0,0,0]` before the planner, with maturity and absorption gates open.
Actual planting is 11 wheat and 8 carrot. This does not show that substituting
melon would win: planting can change seed spending, later production, and the
opponent's proceeds.

**Decision:** complete the already frozen pure-relative H seed311/312 runs and
their existing seven-family judges. H directly trains `w2,b2`, the grow-score
channel implicated here. Keep these runs unchanged. The proposed H plus mixture
sharpness `g2[:,7],gb2[7]` (163 coordinates total) is **withdrawn under the same
sigma0.01 / SGDlr0.00018 / ten-generation recipe** after the scale review below.
No new crop-allocation arm is selected. Do not substitute a forced melon target,
a new benchmark, or a macro-expression gate for the existing judge.
H already influences sharpness indirectly: `policy.forward` sends product
scores through `summary @ gp` into `gh` and then all global heads. Frozen B has
864 nonzero `gp` entries and 32 nonzero entries in `g2[:,7]`. The proposed 33
extra coordinates would add a directly trainable sharpness readout, not the
first connection to that decision.

### Why the sharpness follow-up was withdrawn

Holding the recorded day0 grow scores and plant_total22 fixed, root reproduced
the current decoder at two nearby multipliers:

- `2.5138` gives targets `[10,11,0,1,0]`;
- `2.5136` gives targets `[10,10,0,1,1]`.

The boundary near2.5137 corresponds to head7≈−0.49624, versus B's+0.93873:
about−1.435 in the head logit. Direct isotropic noise on the proposed33
coordinates has standard deviation at most `0.01*sqrt(33)=0.05745`, since
every `gh` activation is bounded by one. If their total learned displacement
were comparable to the old H/J centres'≈0.014 L2, the direct head change would
be bounded by≈0.0804. This makes the unchanged proposal poorly supported for
its stated day0-melon purpose.

These are one-state, fixed-score calculations, not a bound on the full H-plus-
sharpness policy or on future learned trajectories. H also changes crop scores
and global activations; smaller changes can affect other days and win games.
No new population was drawn and no outcome evaluation or acceptance gate was
added. Historical coarse head7 offsets and larger sigma trials are further
caution, not a universal impossibility proof: see
[day0-switch §5.1](2026-09-11-day0-switch.md) and
[ES-rate review](2026-09-10-es-rate-A.md).

The current selector accepts whole blocks, but the existing, unapplied
`S/switch0/trainer.patch` already sketches an `@mask.npy` selector. Extending
that existing code would be possible; this implementation detail is not a
protocol prohibition and is not the reason to reject the current recipe.

### Current H population and rounding check

Following the user's allocation/rounding question, Sol decoded the actual
stored first-generation H perturbations from each passing qualification on
episode108450468's dawn. Root validated source/config/state identities and
reproduced the calculation on the local RTX3070. GPU noise regeneration was
byte-exact; GPU and CPU crop-target arrays matched exactly.

| H seed | Candidates | Any crop-target change | Positive melon target |
|---|---:|---:|---:|
| 311 | 4096 | 1940 | 0 |
| 312 | 4096 | 1948 | 0 |

All changes are confined to wheat/carrot targets. Some totals change to21 or23,
so these are not all conserved reallocations. This establishes absent day0
melon exploration in these two initial populations on this observation; it
does not cover other states, later centres, executed plans or winning value.
It is explanatory evidence, not a training or promotion gate.

The known oversized index tie-break is a real defect, but it does not cause
this dawn's melon zero. Correct Hamilton allocation and the shipped allocator
both return `[11,11,0,0,0]`. The two leftover tiles go to carrot and wheat
(fractions0.9461 and0.7599); melon's0.0778 ranks fourth. Maturity and absorption
gates are open, and normalization and crop indices are correct on this input.
The historical tie-break fix was already engine-judged with mixed outcomes
([consensus §78](2026-09-10-consensus.md)); no unchanged rerun is selected.
Reproduction source, inputs and full results are embedded in current
`launch.json` under `melon_review.current_H_initial_population` and
`melon_review.rounding_code_check`.

### Current training already encounters early melon

Root read all120 action tapes bound by the frozen relative-H manifest and
verified every file hash. Of these,118 request12 melon plants on day0, one
requests one, and one first requests melon on day11. Thus119/120 already
contain a day0 melon opening. These are recorded orders, not newly simulated
successful planting or receipts.

The six unit/market command arrays have29 distinct day0 sequences; the largest
identical group contains44 tapes. Across all30days there are118 distinct
sequences: one group of three matches exactly, but its three town schedules
differ. Matching orders do not establish identical opponent code, and shared
openings do not make the later games or their market conditions equivalent.
Per-tape counts and command hashes are preserved in the current campaign's
`launch.json` under `melon_review.training_tape_coverage`.

**Implication:** the training pool is not missing examples of early-melon
opponents. Merely collecting more tapes with that opening does not address
the observed allocation problem. This census does not establish that deduping,
reweighting, or rotating the pool would improve wins; no data change is selected
and the active120-tape field remains frozen.

## Original fixed-population diagnostic

The early-gap review proposed one no-game stop test: can the actual Flow215
generation-0 population move B's day-0 melon target above zero on the fixed
episode 108450468 dawn observation? `S/unitorder/melon_sigma_reachability.py`
answers that question without building a plan or calling the simulator or
engine.

The helper extracts the exact archived Flow215 source, loads its frozen
`flow193_g100_hr.npy` initial theta, applies the archived `train_mask`, and
recreates `generation()`'s first JAX key split and antithetic perturbation order
for seeds 309 and 310. Both use population 4,096, sigma 0.01, and the 1,191 live
coordinates named by `gp,dh,ds,g5,gb5,w3,b3,b1`. The centre decode agrees
between NumPy and JAX at `[11 WHEAT, 11 CARROT, 0 TOMATO, 0 STRAWBERRY,
0 MELON]`.

## Result

| seed | macros differing from centre | wheat target distribution | carrot target distribution | strawberry | tomato | melon |
|---:|---:|---|---|---|---|---|
| 309 | 2,302 / 4,096 | 9:9, 10:1,344, 11:2,540, 12:203 | 9:3, 10:772, 11:2,940, 12:379, 13:2 | 0:4,092, 1:4 | 0:4,096 | **0:4,096** |
| 310 | 2,311 / 4,096 | 9:11, 10:1,335, 11:2,537, 12:213 | 9:3, 10:798, 11:2,896, 12:396, 13:3 | 0:4,095, 1:1 | 0:4,096 | **0:4,096** |

The complete joint five-crop distributions and target-array hashes are in
`S/unitorder/episode_108450468/melon_sigma_reachability.json`. Seed 309 and seed
310 each produced zero earlier-melon targets in both antithetic halves. This is
not an inert-policy artifact: 56.2% and 56.4% of macros changed at least one
crop target, principally along wheat/carrot boundaries.

## Interpretation

The 1,191-coordinate mask is structurally connected to crop allocation through
`b1`/`dh`/`ds`, but its current local sigma does not cross the melon integer
boundary from this theta on this observed state. The evidence is exact for the
two frozen first draws. It does not prove melon is unreachable after an update,
at a larger sigma, on another state, or through excluded coordinates. It also
says nothing about outcome value. In particular, it does not rehabilitate the
failed melon interventions: forced `MELON_OPEN` lost pinned evaluations and
the one-tile `m0p1` intervention lost its paired simulator development screen.
The latter did not proceed to engine confirmation (integer-search §6).

This stop test rejects the narrow expectation that the current generation-0
population explores the observed opponent's day-0 melon timing. No source,
feature, sigma, or training change follows from this diagnostic. The actual 124 training boards and their other dawn states are outside this
probe. Selection can still respond to melon decisions there, to other crops,
or to development decisions; a later update can cross this observed boundary.
An improved lineage therefore requires its own behavioral explanation.

Pinned inputs:

- archived source `520619b2ab7c7395ffcd214e27b0d3b41c2b0f1a10e6394129fb7d2b20264169`
- config `80ec22d89a5c9a6db6d03559f4130c6e40f4f9abbdedaa15ad47315ecd19354f`
- initial theta `2cde727e56af3e95958a02bcc3236c6147579d3117e4ff9272815b9f3dab62c3`
- replay `5f8cfbd958edc029b614f6d089e6ad499dd2c16a50da0550d41b64077b4c1449`

The run used JAX/JAXLIB 0.10.2 on CPU. The helper records the exact archived
module hashes, PRNG words, masked-epsilon hashes, candidate-theta hashes, and
decoded-target hashes for reproduction.

Independent Sol reproduction matched the complete JSON byte-for-byte
(`d8cf476f` prefix). It also checked both frozen initializer key states, B,
sigma, the exact1191-coordinate mask, and archived brain/parser/policy hashes.


## Completed relative-H centres and allocation follow-up (September 14)

The final abs0 H311/H312 centres still reproduce B's opening on all six saved
loss states: crop targets11W/11C/0T/0S/0M and herd1goose/4cow/1sheep. Their six
plan arrays match each other on all180 B-trajectory dawns and match B on160;
all20 changed plans occur after day0. Both frozen43-file source inventories,
replay hashes and final-theta identities were verified. Source and complete
results are embedded in the relative campaign's `saved_plan_trace.json.gz`;
launch.json binds its hashes. These are counterfactual plans on B states, not
candidate trajectories or outcome evidence. Both standard judges remain required.

Prices enter both policy features and planner economics: normalized quotes plus
base-price scale, market inventory/curve, demand and production are observed;
forward-value features also multiply forecast units by absolute current prices.
The planner values purchase candidates in coins, but learned target counts cap
which candidates it can buy. This proves price information is present, not that
the learned response is sufficient or that risk aversion explains the behavior.

Do not restore the old seed-room patch from its earliest favorable report.
The later Flow215 pilot had mixed effects and no win flips, and the population
comparison failed its reference reproduction. Review also disproved its claim
that taking the componentwise maximum of two grants preserves affordability:
root reproduced old/new spends37/34 and merged spend45 on purse39 using valid
monotone synthetic lists. Full inputs are in launch.json. This is an arithmetic
counterexample to the archived patch, not a demonstrated active B failure.

Naive proportional clipping also needs more than replacing one expression.
Existing `_take_lr` maps target[0,3,1,34,62] at caps39/64 to
[0,1,1,13,24]/[0,2,0,22,40]:25 extra tiles remove one tomato allocation.
Land valuation currently prices only positive want differences, so it would
omit that displaced crop. No proportional-cap candidate is selected. The next
research compares a full learned crop-mix readout with existing-head exploration,
including actual seed-cap integration and an explicit ES scale calculation.
