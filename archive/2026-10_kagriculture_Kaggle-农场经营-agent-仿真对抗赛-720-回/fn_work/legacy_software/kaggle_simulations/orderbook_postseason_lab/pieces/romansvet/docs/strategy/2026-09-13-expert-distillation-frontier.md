# Expert-replay initialization: frontier review

## Status

Replay-supervised initialization has not been run. The trainer can initialize
from an arbitrary theta and can copy an existing encoder trunk, but its update
is still ES fitness from simulated money (`scripts/train.py:813-845,2614-2633`;
`src/kagg3/es/train.py:4912-4999`). Public top-player action tapes are already
used as opponents, which changes the fitness field; no code or preserved run
uses their actions as supervised policy targets. Repository searches find the
idea only as E7 in `2026-09-11-lever-ranking.md`, where it was ranked low and
unexecuted.

That makes behavior initialization technically distinct from objective
reweighting, fresh-board fields, integer ISEARCH, and forced crop switches: it
would choose the starting theta by matching observed actions rather than by
game return or a fixed macro offset. This distinction does not yet make it an
evidence-backed experiment.

## Existing evidence against the broad version

One particular intervention based on a dominant top-tier template has already
received a direct game test. The joint wall-imitation
fixture pinned B's per-day crop, animal, and crew macros; the planner reproduced
7 wheat plus 12 melon on day 0, held the plate, and harvested all 72 melon units.
It then lost 24,209 coins per TOPB2 board and 31,417 on LIVE-C, largely by
raising the opponent's purse (`2026-09-11-wall-imitation.md`). Repeating that
opening alone has negative evidence. This does not test every expert, full
expert trajectory, partial imitation method or learned initialization.

The remaining expert action stream also lacks a clean target in the current
planner. On the already-fixed 29 top-tier tapes, shipped row support covers
93.9% of unit actions but only 17.9% of reference market coin. Even the union
of all implemented switch layouts covers 49.6% of market coin. The missing
mass is chiefly sales on turns the planner cannot emit
(`2026-09-11-expressibility.md`). Later SELL5/SELL21 experiments showed that
adding those turns did not yield a meaningful policy gain, so the old
expressibility census does not reopen sell timing. It does show that exact
complete-plan labels from expert tapes are frequently outside the current
output support.

Macro labels are not present in a replay and generally are not identifiable
from actions. `plant_target`, `animal_want`, and `crew_target` are requests;
budget, capacity, admission, and routing may reduce or reorder their realized
actions. Many macro values therefore map to the same six plan arrays, while an
expert market row can map to none. Treating realized plant or hire counts as
the hidden macro would silently manufacture labels.

The policy is also dawn-state based. Its public features include the current
day, both purses and boards, market, shops, own shed and seeds
(`src/kagg3/core/brain.py:521-597`), but no persistent opponent identity or
action history. Distillation can only learn distinctions present in that
current observation. This is a representation boundary, not evidence that a
history feature would improve play.

## A possible no-game test for exact reconstruction

To test a claim that expert actions can be reconstructed exactly, use a deterministic
**target round-trip audit** on the same 29 tapes already frozen by the
expressibility census; do not select another expert set. For every dawn:

1. pack the expert's next 24 recorded actions into the exact six plan arrays;
2. derive only explicitly declared, action-observable macro targets, recording
   ambiguous fields as unknown rather than filling them from B or the future;
3. build the plan from that dawn with those targets and compare every active
   `(turn, unit/slot, op, arg, qty)` to the expert tensor;
4. report separately exact round trips, unsupported market timing/order,
   planner constraint differences, and ambiguous macro fields, by tape and
   day. Preserve the expert tensor even on refusal.

This checks exact reconstruction, not performance. A failure would invalidate
that exact-target claim; it would not rule out approximate imitation, targets
for individual action components, or fitting latent macros through a declared
action loss. Macro non-identifiability must be handled explicitly in those
methods. An exact subset would establish representability only, not strength
when executed by our planner. No such test or training run was started here.

## Conclusion

Expert initialization is untried as an optimizer operation, but the available
evidence does not justify running it now. The dominant behavior we can imitate
has already lost in one specific intervention, and much of the remaining complete
plan is outside or non-identifiable in the current policy interface. The target
round-trip audit is one falsifiable test of exact reconstruction and needs no game,
download, new benchmark selection, or theta fit.
