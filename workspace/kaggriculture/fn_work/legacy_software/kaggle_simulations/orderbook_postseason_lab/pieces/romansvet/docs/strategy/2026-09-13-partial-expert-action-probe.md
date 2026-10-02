# Partial expert imitation: development-action representation probe

## Decision and boundary

Replay-supervised initialization remains untried. The first bounded experiment
should be a **development-action representation probe**, not an attempt to
invent the experts' latent macros. It asks whether the current dawn feature
bank contains enough information to predict a small, planner-relevant summary
of the recorded expert's submitted actions. It does not modify a policy or
measure game strength.

This is distinct from the closed wall intervention. The wall fixed one crop,
animal and crew template and lost heavily. This probe learns across all 120
already-frozen Flow215 window-0 recordings and tests unseen episodes; it does
not force that opening, use outcomes, add sell turns, alter the ES objective or
revisit momentum.

The inputs are already qualified and disjoint from the seven judge families:

- `momentum_dataset_r1_20260913/dawns.npz`, SHA-256
  `3793fd2d2fd3d2e1230de9c179708ddd8bd1d7e99d0eb25a72e0dd288d6f1c4d`;
- its manifest, SHA-256
  `2ac4637f37742e6833565758848aeccc16cea9e3f3f5688de8852e32d05e7e94`,
  and receipt, SHA-256
  `1afe32c553a9c0d30c2a319381f242bde238f3e13341b9daf0612557c9e1735f`;
- the exact ordered-120 config, SHA-256
  `80ec22d89a5c9a6db6d03559f4130c6e40f4f9abbdedaa15ad47315ecd19354f`,
  and tape checksums, SHA-256
  `9c4fe29ae683650a0f00a28f7c6d9935ee3c5a951d02139bbc7a1338c161bba7`.

Use only the one row per `(episode, day)` whose `seat` equals
`recorded_tape_seat`: 120 episodes times 30 dawns, before any incidence or
model result is read. This row contains the recorded agent's own private shed
and seeds. Never duplicate it through the opposite-seat view.

## Exact labels and features

Decode labels from each matching town-aware action tape, whose day-major
alignment is the contract in `es/tape_actions.py` (SHA-256
`18a6dc2962508c2bf979085c11ebd7a64057a7804acdd15c13ea806888b5fda6`).
For every day preserve this fixed 18-vector of **submitted requests**:

1. requested `BUY_SEED` quantity for each of five crops;
2. requested `BUY_ANIMAL` quantity for each of three animals;
3. number of `BUY_LAND` and `HIRE` rows;
4. number of `PLANT` unit rows for each of five crops;
5. number of animal-item `PLACE` unit rows for each of three animals.

Use the encoded op and argument constants from the pinned `core/ops.py`
(SHA-256 `6bd6b78b85413beb58687b9f643091135dc66109454402eec7992a6e8929357f`)
and the pinned item mapping; do not parse names heuristically. Preserve all raw
per-day counts before fitting. Assert all 120 tape hashes, shapes
`uop/ua/uq=(30,17,24)` and `mop/ma/mq=(30,24,10)`, integer domains, episode
IDs and dataset joins. A replay/tape disagreement refuses the run rather than
dropping the episode.

The fixed input is the existing 234 current-state neural columns in this
order: `prod_features` 108, `global_features` 24, `drain_features` 18,
`production_forecast` 72, and `forward_value` 12. No previous-market feature,
future dawn, action, source ID, seed, terminal money, reward, rank or judge
field enters the model. Episode/source IDs are split and audit metadata only.

## Frozen no-game fit

Assign fold `episode_index % 5`; the ordered 120 episodes therefore give five
held-out groups of 24. Both the split and all label definitions must be written
to a prospective manifest before extraction. The dataset has 120 unique
environment seeds and 120 unique source submission IDs, so no episode or
submission appears on both sides of a fold. This does not establish team-level
disjointness.

For each fold, standardize inputs and `log1p` labels with training-fold means
and standard deviations (replace only zero standard deviations by one). Fit a
fixed full-batch MLP `234 -> 64 ReLU -> 18` for 2,000 Adam steps, learning rate
`1e-3`, L2 `1e-4` on its two weight matrices, seed `20260913 + fold`; do not
tune epochs, width, loss or labels after results. Its objective is

`mean((prediction_standardized - label_standardized)^2) + 1e-4*(||W1||²+||W2||²)`.

The comparator is the training-fold mean `log1p` label separately for each
day and output, so merely learning the common season schedule earns nothing.
Save every held-out prediction and target. Average squared error over days
within each episode first, then average the 24 episode errors in that fold;
report the acquisition block (first 10 labels), deployment block (last 8),
and every label separately. Do not count days or outputs as independent
replicates.

The prospective continuation rule is deliberately demanding: both blocks
must beat the day-conditioned comparator in each of the five held-out folds.
Failure stops this distillation path at the representation prerequisite.
Passing would establish only that present dawn features predict these coarse
expert action summaries across the frozen episodes. It would justify designing
a separate, source-aligned supervised initialization and a no-game behavior
audit; it would not justify a policy or engine pilot by itself.

## Ambiguities that the probe cannot remove

These labels are exact submitted requests, not successful purchases,
plantings, placements, profit or latent macro values. Market orders can fail
for cash, inventory, shop or opponent interaction; unit requests can be
illegal. Summing a day discards turn, order, position and routing, and experts
can react during the day to states our dawn-only planner has not seen. Several
different hidden goals produce the same summary, and the same goal can produce
different requests after constraints. The auxiliary 18-output head has no
declared mapping back into `plant_target`, `animal_want` or `crew_target`.

One episode per source submission also means the held-out test measures
cross-submission prediction, not repeated behavior by a stable expert. The
120 recordings were selected as a training window rather than a representative
sample of all strong play. Even a clean prediction gain would show
recoverability and partial imitation only; it would not show that the imitated
behavior causes higher coins or margin.
