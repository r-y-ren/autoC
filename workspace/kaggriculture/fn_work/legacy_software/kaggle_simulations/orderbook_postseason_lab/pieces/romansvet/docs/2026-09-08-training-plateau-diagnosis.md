# Training plateau near 2,000 leaderboard rating

Code review performed on 2026-09-08. The score discussed here is Kaggle
leaderboard rating, not final in-game money.

## Assessment and evidence limits

There is no demonstrated hard 2,000-rating ceiling in the code. The strongest
explanations for the plateau are limited generalization to stronger opponents,
imperfect candidate selection, and restrictions in the information and actions
available to the learned policy.

This review covered the ES trainer, feature encoding, planner, evaluation gate,
and packaged `dist/submission_flow135_g350.tar.gz`. The package's theta was
verified to match `artifacts/kagg2_games/thetas/flow135_g350.npy`.

Performance figures below are recorded campaign results, not new live
benchmarks. The [build log](strategy/2026-09-05-build-story.md) records g350
reaching 2,144 before falling toward 2,100. Some entries in that log are dated
after this review's environment date; their chronology and live submission
status were not independently verified. Code findings and executable probes
are distinguished from those historical claims below. The active remote
training command and configuration were not verified.

## 1. Recorded opponents only approximate the original agents

Action tapes replay recorded decisions. Their farms, money, purchases, and
inventory evolve under the simulated rules, but their decisions do not adapt
to a different board or to a change in our strategy.

Simulator parity establishes that the simulator reproduces the **tape
opponent** correctly. It does not establish that a tape represents its original
agent on new boards. This distinction matters when interpreting high offline
win rates.

The campaign log reports four gate-approved candidates improving by 4–6 win
percentage points on a small gate panel while performing 2–4 points worse on
the broader evaluation. It also identifies opponent-specific weaknesses:
g350's recorded win rate against `pupen_o` is roughly 20–38%. A strong pooled
average can hide these weaknesses.

**Recommended changes:**

- Split opponents by team or strategy family into training, selection, and
  untouched evaluation sets. Different episodes from the same family should
  not automatically count as independent generalization tests.
- Refresh training with recent opponents while retaining older families to
  prevent regression.
- Include reactive opponents alongside tapes.
- Report performance per family as well as a pooled average.

Sources: [tape_actions.py](../src/kagg3/es/tape_actions.py),
[tape_opponent.py](../scripts/tape_opponent.py), and the
[build log](strategy/2026-09-05-build-story.md).

## 2. Deterministic episode allocation can permanently exclude tapes

`opponent_slots()` allocates the archetype/tape share using deterministic
largest-remainder rounding. With an unchanged configuration, the same rungs
receive the leftover slots every generation. Redrawing board seeds does not
rotate opponent coverage.

An executable probe using four zero-weight archetypes, equally weighted action
tapes, and `arch_frac=0.9` produced:

| Tapes | Episodes per candidate | Tape board pairs per generation | Never sampled | Pairs per tape |
|---|---:|---:|---:|---:|
| 47 | 256 | 115 | 0 | 2–3 |
| 63 | 256 | 115 | 0 | 1–2 |
| 127 | 256 | 115 | 12 | 0–1 |
| 127 | 512 | 230 | 0 | 1–2 |

Each board pair is played in both seats. Therefore, 256 episodes provide 128
distinct board draws before the tape/self-play split, not 256.

This is a concrete coverage defect for larger pools. It does **not** establish
that the current 63-tape run excludes opponents; actual coverage depends on
its weights and configuration. Even when all tapes are covered, deterministic
rounding can distort their requested long-run proportions.

The earlier configuration trap also remains relevant: `arch_frac=0` gives
action tapes zero training slots regardless of their individual weights.

**Recommended changes:**

- Rotate allocations across generations or use randomized allocation with the
  intended long-run proportions.
- Keep the selected opponents and boards identical across candidates within
  each generation to preserve common random numbers.
- Log actual episode counts per opponent and warn or fail when configuration
  silently disables the intended training population.

Source: `largest_remainder()` and `opponent_slots()` in
[train.py](../src/kagg3/es/train.py).

## 3. The gate treats correlated mirrored seats as independent evidence

`paired_stats()` correctly pairs candidate and incumbent results on
`(seed, opponent, seat)`, but computes standard errors across those rows as if
they were independent. The campaign notes that mirrored seats frequently
produce identical outcomes.

In a synthetic probe with ten independent board outcomes, duplicating each
outcome into both seats increased the reported t statistic from **3.0 to
4.36**, without adding independent evidence. This demonstrates the statistical
issue; it does not quantify the inflation in any particular campaign run.

There is a separate selection problem: repeatedly choosing candidates against
the same opponent panel makes that panel part of the optimization process.
More boards against those same opponents cannot eliminate family overfitting.

**Recommended changes:**

- Keep both seats for fairness, but group them under `(seed, opponent)` when
  estimating uncertainty.
- Use an opponent-family bootstrap or similarly grouped analysis when
  estimating generalization across the field.
- Require fresh boards and held-out opponent families for final promotion.
- Treat the small remote gate as a candidate screen, not sufficient evidence
  for promotion or a reliable basis for repeatedly recentering the search.

Sources: `paired_stats()`, `RealGate`, and `_recentre_on_record()` in
[train.py](../src/kagg3/es/train.py).

## 4. The strategic network lacks production-timing information

The policy has 4,980 stored parameters and **4,188 active parameters**. Its
features primarily describe prices, inventories, cash, and production counts.
It lacks an explicit opponent maturity schedule and recent selling history.
The residual-supply estimate uses steady production rates over the remaining
season.

Equal strawberry counts can mean either a large harvest soon or new plants
that produce much later. A probe confirmed that changing strawberry planting
dates and standing yield can leave all neural features unchanged. Own crop
dates are not universally ignored: they can affect the aggregate free-slot
count for one-time crops. The missing information is a sufficiently detailed
production schedule, especially for opponents.

The detailed planner sees more of our own tile state than the strategic
network does. Consequently, this is a limitation of strategic features, not a
claim that the entire agent ignores crop maturity.

**Recommended changes:**

- Add per-product forecasts of our and their production over the next 1, 3,
  and 7 days.
- Include ready-to-harvest quantities and inferred recent market supply.
- Use observable opponent state and maintain history where needed; do not
  assume access to private opponent inventory.
- Preserve NumPy/JAX equivalence when extending the feature representation.

Sources: `PolicyObs`, `features()`, and `residual_drain()` in
[brain.py](../src/kagg3/core/brain.py), and
[policy.py](../src/kagg3/core/policy.py).

## 5. The packaged agent commits to a full day before observing its outcome

The inspected package builds its plan at hour 0 and replays it for the remaining
turns. General market decisions cannot be revised after an unexpected opponent
sale, failed purchase, or changed quote.

The package has `SELL_TURNS=(3, 10, 18)`, `EARLY_SELL_ON=True`, and
`EARLY_SELL_MODE="A"`. These are the core lot schedule and its adjustment mode,
not a claim that every special-case sale occurs on only those three turns.
`OPP_SUPPLY_ON=False` and `MIDDAY_PLACE_V2_ON=False` in the inspected package.
The price projector therefore omits an explicit opponent-supply forecast.

**Recommended changes:**

- Start with a small market controller that revisits selling decisions after
  relevant events, using actual shed contents, reservations, and quotes.
- Preserve the existing route plan initially to keep the experiment bounded.
- Then evaluate coordinated `HARVEST → DROP → SELL` and reinvestment
  opportunities.
- Measure changes jointly with resource reservations and route timing.
  Selling earlier or hiring more unconditionally is not established to help;
  the campaign records losses from several such interventions.

Sources: packaged `main.py` in
[`submission_flow135_g350.tar.gz`](../dist/submission_flow135_g350.tar.gz),
[runtime.py](../src/kagg3/agent/runtime.py),
[plan.py](../src/kagg3/core/plan.py), and
[projector.py](../src/kagg3/core/projector.py).

## 6. ES cannot learn actions outside the planner's representation

The network provides targets and valuation adjustments to a prescribed
planner. It does not directly choose arbitrary unit actions. More generations
cannot discover a behavior that the action generator cannot express.

Hiring is scored against a derived task list. Extra workers do not
automatically create additional useful work. The campaign reports one forced
crew-ramp experiment increasing PASS from 15% to 37% of unit-turns. That is
consistent with buying capacity without admitting enough useful tasks.

Search scale also matters because the decoded decisions contain floors,
thresholds, clips, and discrete choices. For isotropic perturbations over the
4,188 active coordinates, the expected perturbation norm is approximately:

| Sigma | Approximate perturbation L2 norm |
|---:|---:|
| 0.020 | 1.29 |
| 0.015 | 0.97 |
| 0.010 | 0.65 |

The campaign records gains from reducing sigma to 0.015, followed by another
plateau. This supports tuning search scale; it does not establish that reducing
sigma indefinitely will help.

**Recommended changes:**

- Measure perturbations by the fraction and importance of decoded decisions
  they change, not just by parameter-space sigma.
- Tune sigma and learning rate together, using additional boards when the
  measured signal requires them.
- Preserve joint optimization across heads; isolated bias changes can miss
  coordinated strategy improvements.
- For structural planner experiments, evaluate purchases, crew, task
  admission, and routing together.

Sources: `generation()` and `apply_gradient()` in
[train.py](../src/kagg3/es/train.py), hiring enumeration in
[plan.py](../src/kagg3/core/plan.py), and the
[campaign account](strategy/2026-09-08-how-we-built-the-agent.md).

## 7. Audit the actual objective and defaults before launching more runs

The default fitness gives **60% weight to ranked own-money performance** and
40% to ranked smoothed margin. Logged win rate is not the same quantity as the
gradient's objective. The default weight decay is **0.003 per generation**.

Those defaults differ from the later documented successful recipe, which
explicitly disables weight decay. This review did not establish that active
remote jobs use the defaults. These are configuration checks, not confirmed
causes of the current run's plateau.

Record the effective objective, decay, trainable mask, opponent mixture, gate
metric, and initialization in a reproducible run manifest. If objective
misalignment remains a concern, compare a small number of win-oriented and
own-money/margin blends on the same training and held-out protocol. Increasing
our income and suppressing the opponent's income can both improve wins;
neither mechanism should be rejected without measurement.

Sources: `Config`, `shaped_advantage()`, and `apply_gradient()` in
[train.py](../src/kagg3/es/train.py), and argument defaults in
[scripts/train.py](../scripts/train.py).

## Recommended implementation order

1. **Repair measurement and coverage.** Fix opponent allocation, report actual
   counts, group mirrored seats in uncertainty estimates, and establish
   opponent-family holdouts.
2. **Rebaseline the current champion.** Measure per-family wins on fresh boards
   and inspect recurring losses. Report our money and the opponent's money
   separately, alongside margin and win rate.
3. **Improve strategic information.** Add production-timing features and
   observed supply history, then retrain jointly from the verified champion.
4. **Expand market responsiveness.** Test limited intraday market revisions
   before attempting a general replanning or routing rewrite.
5. **Tune search against the repaired protocol.** Adjust sigma, learning rate,
   and evaluation budget based on measured decision changes and signal.

A larger network or a longer run is not the first priority: neither repairs
missing opponent coverage, biased selection confidence, or unavailable actions.
These recommendations are experiments to test, not a guarantee of a particular
leaderboard rating.

## Validation performed

- Inspected the packaged g350 source and confirmed its theta equals the saved
  g350 checkpoint.
- Executed the opponent-allocation, mirrored-seat significance, and neural
  feature probes described above.
- Passed five focused existing tests covering paired-statistic arithmetic and
  the active parameter mask.
- Started a broader test selection but stopped it before its expensive CPU
  rollout completed; no full simulator or training benchmark was completed.
- No source code was changed during the review.
