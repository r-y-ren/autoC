# Two next improvement hypotheses after Flow215

**Follow-up:** The first hypothesis failed its specified episode stop test;
therefore the conditional132-coordinate training proposal is not activated.
The existing planner already projects a higher tomato price but still ranks
its return below the requested strawberry/melon streams on days10–14.
Root independently reproduced Sol's full JSON/CSV result exactly.
See [the completed maturity-economics test](2026-09-13-tomato-maturity-economics.md).

Subsequent bounded diagnostics:

- [Forecast usage review](2026-09-13-forecast-usage-review.md): B has connected,
  nonzero production-forecast weights; those blocks are fixed in current training.
- [Price momentum review](2026-09-13-price-momentum-review.md): the user's proposed
  daily history input is representable and has not been directly tested. A
  training-side corpus and forecasting comparison remain unimplemented.
- [Final checkpoint on recorded dawns](2026-09-13-seed309-final-macro-108450468.md):
  macros differ on30/30 observations but complete plans on1/30; no earlier
  tomato request. Root and Sol reproduced the calculation.
- [Completed seed309 judge](2026-09-13-seed309-g10-judge.md): all seven separate
  mean margins are negative; most are small relative to uncertainty. Seed310
  continues independently. No new training arm follows from this result alone.
- [Completed plan-threshold measurement](2026-09-13-plan-crossing-census.md):
  82–179 of256 perturbations change stored plans in each fixed case. This
  measures variation on ten unique observations, not value or training causality.
- [Price-reaction review](2026-09-13-price-reaction-review.md): current prices
  enter at dawn; intraday variants already tested do not establish a gain.
- [Early cash-gap reconstruction](2026-09-13-episode-108450468-early-gap.md):
  exact observed19441 dawn15 cash gap, with17440 gross receipts from the
  opponent's earlier melon cycle. Descriptive timing, no forced-crop pilot.
- [First-population macro reachability](2026-09-13-melon-sigma-reachability.md):
  zero day0 melon targets in both4096-member populations on that one recorded
  observation. Independently reproduced; other states and later updates remain
  outside the test.
- [Older objective-alignment audit](2026-09-13-flow215-objective-alignment.md):
  own-coin and margin ranks conflict on855/2048 antithetic pairs; the configured
  blend follows own coins in622. This is old pre-repair population evidence,
  not a reason to change either live run or automatically ban its objective.

This is a read-only source/evidence review. It proposes no current run, policy
change, transfer, or promotion. The two items are ranked by how cheaply their
premise can be falsified. The fresh sequential-unit seed-309/310 training and
its generic judge are separate live work and are not repeated here.

## 1. Policy: expose the planner's maturity-value signal to the product head

**Hypothesis.** Add a public-state, per-product feature for the marginal gross
return at the product's first yield, then feed it through a new zero-initialized
additive block into the existing product hidden layer and grow/sell scores. A
useful minimal feature is the projected first-yield quote or one-seed stream
return, normalized by today's quote and seed/input cost. It must use only the
current dawn observation, known shop drain, existing committed production, and
the fixed price table. It must not use replay futures or an opponent-action
forecast.

This is a representation alignment change, not another forced-tomato rule. The
planner already projects inventory to every product's first yield and prices a
new unit stream there (`core/plan.py:4054-4063, 4074-4084, 4848-4869`). The
network that supplies `grow_mult` does not receive that result. Its ordinary
product inputs are current inventory, current price, current town demand,
standing production, shed, first-yield lag, and rate
(`core/brain.py:521-552`). Its production forecast reports when units arrive
(`core/brain.py:492-518`), while the global forward-value path explicitly uses
**today's** quote rather than a projected quote (`core/brain.py:444-489`). Thus
the network sees the ingredients but must approximate the planner's nonlinear
price-table calculation through a shallow shared encoder.

Episode 108450468 supplies a concrete failure context. B requested zero tomato
on days 10-14 and only one on days 15 and 16, despite two tomato buyers from day
12, ample seed cash, no opponent tomato, and inventory already falling; tomato
then rose from 68 on day 12 to 166 on day 29
(`2026-09-13-episode-108450468-tomato.md:7-28`). This is mechanism evidence
only. Extra tomato displaces strawberry/melon and adds work, and the prior
forced endgame tomato case lost through displacement
(`2026-09-13-episode-108450468-tomato.md:30-34`).

**Cheapest discriminating test (about 1-2 CPU hours, no games).** On the
preserved dawn observations for days 10-16, compute the planner's pre-multiplier
one-seed stream return for every crop exactly as `_candidates` does. Freeze the
formula before reading the values. Report whether the tomato return ranks above
the strawberry/melon replacement actually requested on days 12-14, together
with the displaced crop's return, tile lifetime, and task count. Then repeat the
same descriptive calculation on a fixed, outcome-blind public-B dawn corpus to
measure incidence; do not aggregate it into promotion evidence.

**Falsification.** Stop if the exact planner economics also rank tomato below
the chosen replacement crops on days 12-14, or if the disagreement is absent or
vanishingly rare in the frozen corpus. That result would locate the episode in
ordinary displacement economics rather than a missing policy input. If the
disagreement is real, the next test is one predeclared branch from a fixed dawn
through season end, with the feature allowed to change the complete plan and
with own, opponent, and margin effects reported. No coefficient sweep follows.

The fixed day-5 `compact+1` selector does not cover this hypothesis: that gate
lost 130 margin and was correctly stopped, but it changed a single compactness
macro on one day and contained no maturity-value candidate
(`2026-09-12-planselect-all30-result.md:1-29`). ISEARCH also does not cover it:
it applied unconditional radius-1/2 integer offsets; zero of 24 cleared its
development rule (`2026-09-11-integer-search.md:134-175`).

## 2. Training: isolate the new value path instead of reopening the 1,191-gene arm

**Hypothesis.** If hypothesis 1's disagreement census passes, append an inert
two-feature path analogous to `dh/ds` and train only that new path from B. Two
features into the 64-unit product hidden layer plus the two product scores would
be 132 coordinates (2x64 + 2x2). Zero initialization must reproduce B's NumPy
and JAX macros, complete plans, and a small engine identity fixture exactly.
The first experiment is a replicated generation-zero gradient/readout, not a
ten-generation arm.

The current Flow215 search cannot discover this mapping. Its mask contains
exactly 1,191 coordinates: `gp` 864, `dh` 128, `ds` 4, the two live columns of
`g5/gb5` 66, `w3/b3` 65, and `b1` 64. `gp` alone is 72.5% of the search. The
mask gates both perturbations and updates (`es/train.py:890-938`); the existing
forecast blocks `fh/fs` and every other block are held byte-exact. The completed
Flow215 centre changed exactly those 1,191 coordinates and lost margin on all
seven separately reported families, including H30 -869 and H30B -715
(`2026-09-12-flow215-g10-judge.md:3-22`). It often raised own coins while raising
the opponent's purse more, so in-simulator progress cannot substitute for the
separate-family judge.

This narrow new-block test addresses a measured failure of prior appended-input
training. The 264-coordinate residual-drain block was live and moved 14% of
plant decisions, but after 54 joint-search generations its magnitude and
decoded effects were indistinguishable from random drift; the report explicitly
identified weak selection inside the 7,053-coordinate joint search
(`2026-09-10-gene-decode-flow168.md:57-108`). At 132 dimensions and population
4,096, the new path gets far more perturbation pairs per coordinate while the
shipped champion remains fixed outside the path.

**Cheapest discriminating test (two approximately 12-minute GPU evaluations,
about 0.4 GPU-hours if parallel, plus under one CPU-hour of audit).** After the
representation census passes, run two independently seeded, no-update
generation-zero populations on the same frozen repaired-simulator training
field. Preserve raw advantages and compute the cross-seed gradient cosine
against a predeclared sign-flip/permutation null. Confirm that perturbations
actually vary the projected-value response and the relevant complete plans.
Only if the cosine clears the null should one fixed small step be screened;
report evaluation families separately and keep promotion authority with the
ordinary judge.

**Falsification.** Do not train if either population is behaviorally inert, if
the cross-seed cosine does not clear its frozen null, or if the fixed step fails
to improve its own training objective before any held-out family is opened.
After a training-objective pass, any separately evaluated family with a clear
adverse margin or opponent-purse transfer refuses continuation. This is not a
request to average seed centres, retune the old mask, alter the rung weights, or
revive Flow215 w01.

Existing closures matter. Block-SNR found no old block surviving multiplicity,
the unchanged-decode block-sigma fell inside the do-nothing shell, dithering did
not open a useful gradient, and ISEARCH found B locally optimal
(`2026-09-10-consensus.md:640-676`). Objective reweighting, fresh-board fields,
and theta soup were also measured and closed. The proposal is conditional on a
new observable feature with a specific source-level disagreement; without that
disagreement, there is no training proposal here.
