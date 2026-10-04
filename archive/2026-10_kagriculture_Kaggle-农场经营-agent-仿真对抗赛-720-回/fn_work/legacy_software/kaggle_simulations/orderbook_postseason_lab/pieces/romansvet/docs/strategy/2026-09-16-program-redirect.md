# 2026-09-16 14:22Z — PROGRAM REDIRECT: from switch-by-switch to switch vectors, genes, and the action interface

**USER DECISION (2026-09-16 ~14:10Z).** Asked why we cannot move up, the lead
answered: (1) the band is one clone lineage re-released daily while our upload
is frozen (B margin vs fresh clones +2,045 09-11 → +1,103 09-15 → −514 09-16);
(2) §115b passes are +460..+800 coins/board against a ±25k shop lottery and a
~50 % win rate vs the band; (3) B is a strict local optimum, every large lever
lost paired; (4) the top 5 above ~2950 is the fertilizer-ENGINE economy, a
different class, not a better B.

The user then asked: why not remake the planner/executor; why manual switches
instead of training; implement all actions and let training decide, since
switch-by-switch cannot see "3 on, 2 off". Lead's view, accepted by the user
("run the plan as you proposed"):

* switch-by-switch is coordinate ascent; interactions are proven
  (SELL_SLOT_PRIORITY rejected alone, passed stacked on LOT4). ~50 module
  switches exist, most default OFF, fewer than 20 combinations ever judged.
* training only chooses among actions the planner can express; the ES plateau
  (2026-09-16-es-plateau.md: true effect of every ES-from-B candidate −124 ± 47)
  and the Codex review both say the action interface is the bottleneck.
* a from-scratch rewrite is the wrong bet with 7 days to target; rewrite the
  capping modules and expose them as GENES, not flags.

**Correction to the lead's own claim:** FORWARD_ADMIT is NOT unbuilt. It exists
as a manual override (plan.py:4739, loses −9,224 as a fixed switch) and as gene
g11 macro.forward_days, which the ES already moves (tests/test_forward_gene.py).
MACRO-RAMP (2026-09-14) showed the top's crew is not the top's edge (−4,860).
So "early ramp" is a closed row; the open structural row is the fertilizer /
bought-wheat economy of the 2950+ class.

## Plan (in cost order)

1. **SWITCHVEC** — treat the merged switches as one binary vector; fractional
   factorial screen on the lottery-free sim (S/simscreen/screen.py --switches,
   pinned-town boards incl. a fresh V45LEG2 board file), fit main effects +
   pairwise interactions, confirm the top vectors on POOLED180 vs the pair.
2. **GENESWITCH** — make switch bits genes appended to the theta head (zero =
   OFF = byte-identical decode; gene-slope check at training sigma per
   2026-09-10-gene-slope-g170.md), so ES co-adapts switches with the 41-int
   head instead of the lead flipping them by hand.
3. **FERTENGINE** — extract the 2950+ class's fertilizer / bought-wheat
   mechanics from top-tier tapes and express the smallest option as a gene
   (dispatch when a stream frees; FERTDENIAL in flight covers the denial side).
4. **ES restart** over the enlarged gene vector with fresh V45 clone tapes in
   the opponent seat (GPUs idle), after GENESWITCH lands.
5. **Daily re-ship** as part of the loop; a frozen upload depreciates.

Caveat carried: the 09-07 sim constant sweep did not transfer to the engine
(selection on shop-lottery noise, not sim error); paired CRN screening + the
POOLED180 gate stays the protocol.

## 14:48Z USER: next strategic step = PRICE-AWARE PRODUCTION

User (2026-09-16 14:48Z): "our agent should be smart enough to stop production for
product with no value." Marked as the NEXT STRATEGIC STEP after the switch-vector
and gene work: production targets (herd `animal_want`, tiles `plant_target`) are
decoded open-loop from the theta head by day bucket; price enters only at SELL
time. The agent must retarget production when a product's price collapses
(wool at 1 while sheep keep being bought is the motivating case). Inputs:
WOOLPRICE box (docs/strategy/2026-09-16-woolprice.md) answers the mechanics and
whether any price feature reaches the head; then a PRICEAWARE box builds the
lever as a gene-driven option (per-product price/glut feature into the head or
a plan-side production veto), judged paired on POOLED180 vs the pair.
