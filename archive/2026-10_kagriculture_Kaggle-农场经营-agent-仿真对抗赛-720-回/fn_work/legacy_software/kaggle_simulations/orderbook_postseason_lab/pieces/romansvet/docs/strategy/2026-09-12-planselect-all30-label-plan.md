# Frozen all-30 day-5 label plan

The next label run is frozen to all 60 ordered rows in
`S/isearch/boards_dev.json`: the first 30 distinct H30-development tapes and
both recorded tape seats. Its only candidates are unchanged B and the same
day-5 `compact + 1` edit clipped to `DIST_MAX`. Both branches return to ordinary
unchanged B on days 6–29. Day 29 uses exactly 23 turns and no end-of-day step.
No H30B, NEXT, or other evaluation family is read.

The completed four-tape pilot remains preserved under the legacy
`day5_labels_*` artifact names. It found per-tape mean margin deltas of +626,
+549, +144, and -1777 coins, for a four-tape mean of -114.5. Choosing the
better branch after seeing each result would give +329.75, but that is a
hindsight maximum and supplies no predictor evidence. Because these outcomes
were seen before this feature bank and calibration recipe were frozen, the
all-30 analysis is exploratory development calibration rather than pristine
out-of-fold evidence.

## Inputs and fixed calibration

The selector feature bank contains only current `PolicyObs` reductions and
candidate-plan differences: own/opponent money and quadrant counts; canonical
whole-board crop counts, standing-yield sums, and crop-age sums for both seats;
market inventory, prices, shops, own shed and seeds; and fixed operation-count
differences between the two complete plans. Raw tile positions are never used.
Tape, seed, RNG word, full-state hashes, file hashes, and plan hashes remain in
audit/provenance fields and are excluded from this bank.

`flatten_selector_feature` fixes the numeric order explicitly: named scalar
order; own then opponent crop vectors in crop-index order; market, shop, shed,
and seed vectors in their native schema order; plan scalars; then unit and
market operation deltas in numeric operation-code order. JSON key sorting does
not define or change this order.

The fixed model recipe uses one row per controlled seat, target
`alternative_minus_base_coin_margin`, and leave-one-tape-out folds that keep
both seats of the held-out tape together. Each fold standardizes from its 58
training rows, drops zero-variance columns, fits ridge with intercept and fixed
alpha 10.0, and chooses compact+1 only when predicted margin delta is positive.
Results are reported as the two-seat mean realized margin delta for each tape.
No alternate feature set, threshold, transform, or alpha will be selected from
the new labels.

A held-out engine pilot is justified only if the learned gate's mean realized
margin delta across the 30 two-seat board means is positive and its board-level
t statistic is at least 2. The report must show B, always-compact+1, the learned
gate, and the hindsight oracle separately. Failure stops this direction without
retuning. This threshold is a conservative resource-allocation rule and cannot
be read as unbiased significance because the first four development outcomes
were already observed.

## Isolation and validation

Mode `--tapes 4` retains the old paths. Mode `--tapes 30` writes only
`day5_labels_all30_dawn.pkl` and `day5_labels_all30_day6.pkl`; their identities
include the arms-next source tree, runner, branch helper, complete frozen config,
stage, and job layout. Existing four-tape checkpoints cannot satisfy the
all-30 identity or paths. The first all-30 state retains injected-B versus
ordinary-B and duplicate-B equality checks.

The detailed NumPy/JAX macro and plan identity proof remains scoped to the
reviewed original eight states. Repeating eager JAX plan construction 60 times
would add substantial cost. Every all-30 candidate is still built as and
injected from a NumPy plan. Before any labels are interpreted, the runner must
match all 60 B terminal own coins, opponent coins, and margins exactly against
the keyed `base` rows in `S/isearch/lc.csv`, where `seat` is the recorded tape
seat. A mismatch aborts output.

Proposed first command, after review and index clearance:

```bash
JAX_PLATFORMS=cpu timeout 600 .venv/bin/python -u S/planselect/day5_labels.py --tapes 30 > S/planselect/day5_labels_all30.json.tmp 2> S/planselect/day5_labels_all30.log && mv S/planselect/day5_labels_all30.json.tmp S/planselect/day5_labels_all30.json
```

If that bounded process times out after writing a valid all-30 checkpoint, the
unchanged restart command is:

```bash
JAX_PLATFORMS=cpu timeout 600 .venv/bin/python -u S/planselect/day5_labels.py --tapes 30 --resume > S/planselect/day5_labels_all30.json.tmp 2>> S/planselect/day5_labels_all30.log && mv S/planselect/day5_labels_all30.json.tmp S/planselect/day5_labels_all30.json
```

The output and log names are separate from the four-tape artifacts. These runs
generate exploratory labels only; they do not train a gate or support policy
promotion.
