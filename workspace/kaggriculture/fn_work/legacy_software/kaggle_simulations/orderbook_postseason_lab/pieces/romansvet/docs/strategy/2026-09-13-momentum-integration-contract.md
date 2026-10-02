# Previous-dawn market inventory: prospective integration contract

This is an implementation-feasibility contract, not an experiment result. It
does not change a captured tree, production source, a theta, or a game. The
feature is the nine-product dawn-to-dawn stock movement

```text
momentum[p] = (previous_dawn_market_inventory[p]
               - current_dawn_market_inventory[p]) / product_scale[p]
```

so positive means net market draw. It preserves information that the current
price cannot: prices are a rounded, floor-censored function of current stock.
The normalization should reuse `brain._T`, the existing per-product stock
scale, and stay `float32` in NumPy and JAX.

## Source boundary

The semantic baseline for this review is the captured seed-309 OFF training
tree under
`S/unitorder/off_train_20260913/loop-train/private_stage/src/kagg3`, with its
repaired unit-order overlay and exact shipped planner. Relevant captured files
and SHA-256 values are:

| File | SHA-256 |
|---|---|
| `agent/runtime.py` | `28767cc1392489b1102d446959c3065fdd9b2ef797dbaf2c8cd8d5f48cbbd26e` |
| `agent/opening.py` | `57a86d5a5b6184bfeaee78d43f126bb78bf06858a684388ae9a7ab0b5e4ead68` |
| `core/brain.py` | `4f0ba8728aeb7d02b51e2d1134e9a6af4ef2b7f88c4fb100976e4e2f179bcfd7` |
| `core/policy.py` | `45e1fcb34ec43011495549a94b3a8eee6cdf48c635b1985f05ba602702ce151a` |
| `sim/rollout.py` | `a315783f131603560f08aa524073f0f8ca1860ee18a6a421d519d0ba778a7b53` |
| `sim/state.py` | `96c52c4feacb699f4c190c552a637d5c0b7e6b9c6660e9d7e873716fb2ad5591` |

The actual submitted B archive is
`submission/submission_flow193_g100_hr.tar.gz`, SHA-256
`ebad35c6d8eb4da4affb5ca5c075e350680219f4383e640e5392f4a3d312e050`.
The current repository and its package builder are separate identities. In
particular, current `scripts/package_submission.py` is SHA-256
`a5b99ff80c09d6a091a9f84810ec7e23cea3fd24489a5a765b412c5b6ff150d1`;
it is tooling to pin and review, not evidence that the captured or submitted
tree has the same bytes. An implementation should start from a copied frozen
tree, bind every baseline file, and permit only the declared overlay files
below. It must not claim whole-tree equivalence from this per-file analysis.

## Required code path

The submission currently has one `Runtime` per physical player
(`agent/runtime.py:18-34,53-63`). It builds the complete day plan at hour zero
and retains only `plan` and `day`. That is the right persistent boundary:

* Add previous/current dawn inventory state to each `Runtime`; do not use a
  module-global vector. Rotate it once when a **new day** reaches the planner,
  before calling the macro, and retain it through hours 1-23. A repeated call
  to hour zero for the same day must not rotate history again.
* Extend the macro interface explicitly to receive the previous dawn vector,
  or another equally explicit immutable dawn context. The captured call is
  `macro_fn(obs, player, view)` at `runtime.py:32`; all constructors and tests
  of `Runtime` must therefore be enumerated. Avoid putting mutable history in
  `DayView`: it is a current-observation parser used throughout the planner.
* Current package glue manually builds `PolicyObs` in
  `scripts/package_submission.py:125-142` and creates one runtime per seat at
  lines 147-155. It must pass current and previous inventory to `PolicyObs`,
  and the built archive must contain the modified runtime, brain, policy and
  widened theta. Package generation is a separate hash-bound step.
* `OpeningSplice` bypasses the runtime on days before `K`
  (`agent/opening.py:17-28`). The first planner-controlled dawn after such a
  splice has no prior dawn observed by that runtime, so its momentum is zero.
  The statement in that module that the planner carries no cross-day state
  must be revised if this feature is implemented.

Append a `prev_mkt_inv` (or already normalized `market_momentum`) field to
`core/brain.PolicyObs` after its existing defaulted fields. `features` already
reads current `mkt_inv` and price at `brain.py:521-552`; expose momentum as a
separate nine-vector so the old 12-column product encoder remains unchanged.
`brain.decide` (`brain.py:860-870`) should pass it separately to
`policy.forward`.

In `core/policy.py`, append, in this order, `("mh", (1, 64))` and
`("ms", (1, 2))` to `SHAPES` and to `Params`. This grows the flat layout from
6,789 to 6,855 parameters without moving an old coordinate. Apply the feature
as two outer residuals:

```text
hidden_pre = (the exact existing hidden pre-expression)
             + momentum[:, None] @ mh
scores = (the exact existing score expression)
         + momentum[:, None] @ ms
```

Keep the existing expression parenthesization intact, for the reason documented
at `policy.py:600-617`. Let direct legacy callers omit momentum and skip these
products. `unpack` and `pad` already append a missing tail with zeros
(`policy.py:499-571`), but `init_theta` initializes every matrix randomly
(`policy.py:574-582`): it must explicitly initialize `mh` and `ms` to zero, or
fresh runs would activate an untested feature immediately. Any train mask that
intends a momentum-only fit must name precisely these two blocks.

The least invasive simulator implementation does **not** add a history field to
the widely used `sim.state.State`. Instead, make the `episode` scan carry
`(State, previous_dawn_inventory)`, initialized with `initial_state.mkt_inv`.
Extend `run_day`/`policy_obs` with an optional previous-inventory argument whose
legacy default is the current inventory. At each dawn:

1. Freeze `current = st.mkt_inv` and `previous` before either policy call.
2. Give both physical seats the identical `(previous, current)` pair. Planning
   order must not mutate it.
3. Execute the day, then carry `current` as the next day's `previous` value.

This preserves day-0 zero momentum, warm-start zero momentum, and the final
partial day-29 convention. Tape mode still builds both macros before replacing
the selected plan (`sim/rollout.py:207-245`), and market flow happens later in
the day; both therefore affect the next dawn rather than one seat in the
current dawn. A direct caller of `run_day` that supplies no history deliberately
gets a zero feature. If an implementation instead widens `State`, every State
constructor, raw evidence schema, checkpoint fixture and fidelity translator
must be migrated; that is unnecessary for this feature.

## First-day and ordering rules

* A runtime's first observed planner dawn is zero, whether it is engine day 0,
  a warm start, or an opening-splice handoff.
* History belongs to physical seat runtime identity, although the underlying
  market vector is public and normally equal for both seats.
* Product order is exactly the existing nine-entry market/product order used by
  `PolicyObs.mkt_inv`, `brain._T`, and the policy score rows. Never sort names.
* `previous - current` is the signed convention: draw is positive, restocking
  is negative.
* Only a transition to a new day rotates history. Intraday calls read the
  cached plan and do not alter dawn history. This feature does not reopen the
  already closed intraday-replanning direction.

## Minimum gates before fitting or gameplay claims

1. **Layout and initialization.** Assert `N_PARAMS == 6855`; padding B preserves
   its first 6,789 float32 values byte-for-byte and appends exactly 66 zeros.
   Test the same trailing-axis operation for every checkpoint-shaped array
   (centre, optimizer buffers, champion, pool and archetypes). Assert fresh
   `init_theta` also zeros exactly `mh` and `ms`.
2. **Zero-weight decode.** On frozen real dawn observations covering day 0,
   later days and both seats, compare the old 6,789 decoder with padded B under
   NumPy and JAX. Macro fields and all six built-plan arrays must be byte-exact.
   This is the behavioral compatibility claim; matching dimensions alone is
   insufficient.
3. **Runtime state.** Feed two physical runtimes interleaved synthetic dawn
   sequences. Assert first-dawn zero, the signed day-1/day-2 vectors, no
   cross-seat contamination, no intraday update, no double rotation on a
   repeated hour-zero observation, and zero at opening-splice handoff.
4. **Simulator cadence.** With capture-only policies, assert both seats receive
   one identical frozen history per dawn, that history advances only after both
   policies, and day 0, warm start, tape/flow and partial day 29 follow the
   rules above. This checks plumbing without a game outcome claim.
5. **Nonzero sentinel.** On two otherwise identical observations with different
   previous inventories, set one diagnostic `mh` or `ms` coefficient. Require
   only its corresponding product path to change and require NumPy/JAX decoded
   plans to agree. This proves the new signal is live; it is not evidence that
   the feature helps.
6. **Frozen zero-feature trajectory.** Before any fit, run one separately
   authorized frozen source case through old B and padded B and require exact
   evaluator outputs and action/state trajectories. Existing enhanced-season
   and row58 receipts bind the old source and do not automatically validate a
   modified tree.
7. **Package custody.** Rebuild from a prospective immutable manifest; verify
   the generated archive contains only the declared source changes and a
   6,855-value theta; then repeat the zero-weight package action check. Bind the
   builder and the submitted archive independently.

These gates establish compatibility and signal plumbing only. They do not
authorize fitting on the seven judge families, pooling their results, or
claiming that dawn inventory movement improves play.
