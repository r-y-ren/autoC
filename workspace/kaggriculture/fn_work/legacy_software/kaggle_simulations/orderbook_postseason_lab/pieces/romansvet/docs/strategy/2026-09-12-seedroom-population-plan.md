# Seed-room population audit: prospective decision and scope

This is a paired, no-update diagnostic of Flow215's training/shipment mismatch.
It is not a continuation of the refused g10 centre or w01. Independent Sol
reviews agree that B's ON/OFF identity and the completed centre's nearly-zero
mean engine effect do not establish population-rank or gradient equivalence.
No result from the new population is known when this plan is recorded.

Use the archived actual Flow215 source, the frozen B, sigma 0.01, 1,191-gene
mask, seed 309, population 4,096, and exactly the first w00 generation's 120
pinned training tapes plus four carried episodes. All four shipped planner
switches stay ON; only `SEED_ROOM_PURSE_ON` differs between two separate
processes. Preserve source/helper/config/tape/centre hashes. This is training
support; no held-out family is read and no evaluation statistics are pooled.

Capture candidates and episode arguments from the actual trainer before its
first `_play` call and abort that generation before updating. The JAX noise
key is the second output of `split(PRNGKey(309))`, not PRNGKey(309) itself.
The CLI also consumes its NumPy RNG during random-theta initialization before
installing B, so merely constructing a fresh RNG is not exact reproduction.
Population order is all positive perturbations, then all matching negatives.
The two arms must have identical candidate, epsilon and complete batch hashes.
Assert that theta, optimizer moments and step counters remain unchanged and
that no trained checkpoint is emitted. Batch-construction RNG/carry movement
is bookkeeping needed to reproduce the first draw, not an optimizer update.

Save raw per-episode money, both pre-rank objective terms, the trainer's
blended advantage, antithetic preferences and the unapplied gradient. Fitness
is 0.6 times the ranks of mean log own coins plus 0.4 times the ranks of mean
sigmoid margin; ranking a blend of the two raw means would be a different
objective. Report tie-aware rank correlation, strict positive-to-negative
antithetic preference reversals separately from ties, gradient cosine and
relative gradient-difference norm. Plan-boundary prevalence is supplementary
and must be scoped to the states actually inspected.

Root may launch only after reviewing staging, passing local CPU zero-game
initialization and comparison tests, matching remote source/tapes/helpers,
and confirming free GPUs. Each arm has a 1,800-second process cap, one GPU,
with no watcher, automatic restart or checkpoint resume. A tool observation
timeout is not a process exit; observe the same process/handle.

## Decision fixed before outcomes

If the paired audit fails input identity, no ranking interpretation is valid.
If a gradient is zero, report that explicitly and review the raw preferences;
do not silently convert undefined cosines into evidence.

For nonzero gradients, stop this mismatch direction if gradient cosine is
at least 0.99 and strict antithetic preference reversals are at most 1% of
the 2,048 pairs. Otherwise one further paired draw may be considered to test
reproducibility, with an independently derived perturbation key and the same
frozen batch. These are experimental-budget criteria, not statistical
significance thresholds. Repetition is not automatic.

Even reproducible disagreement proves only that the training switch changes
the search landscape. It does not prove OFF is better. Any later candidate
step requires a separate concrete review and separate-family evaluation;
this audit never applies a gradient, launches training or promotes a policy.
Production B and the submission payload remain unchanged.
