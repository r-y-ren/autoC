# The flow209 objective vs the held-out judge — audit of the g20 centre

Dispatched 2026-09-12T00:47Z (consensus §105); reported 2026-09-12T01:5xZ.

**Question.** flow209 moves its centre in a direction that is persistent across
10-gen blocks (§104: block cosine +0.82 against a +0.54 optimiser null) and
aligned across every rung family (§105: FLOW209·FLOW211 disattenuated ρ 0.93),
its in-sample `mean_win` is flat (0.6660 at g1 → 0.6649 at g18), and its g20
centre LOSES to candidate B on the held-out engine judge (00:45Z: LIVEC-H30
−516, LIVEC-H30B −645 W0/L6, TOPB2 −197, LIVE62 −1, NEXT30 −201). Which is it:

* **A** SIM/ENGINE DIVERGENCE — the sim ranks g20 above B where the engine ranks it below;
* **B** WITHIN-BAND MEMORISATION — g20 beats B on its own training rungs, loses on the held out;
* **C** NOISE WALK WITH MOMENTUM — level everywhere, the −516/−645 is the board lottery;
* **D** the objective rewards something the judge penalises.

**Answer: D (weakly), on top of a C′ baseline. A and B are refuted.**
The sim agrees with the engine board for board (**A refuted**, ρ +0.77 on the
held-out boards — the sim is not lying anywhere). The g20 centre does not beat B
on its own LIVE-C training rungs in the sim or the engine, and its net objective
is flat (**B refuted** — nothing was memorised, there is no aggregate in-sample
gain). But the objective is **not** uniformly flat inside: measured on the
trainer's own 166 rungs (§5), the g20 step **gains on TOPTEN (+461, t +2.0, 32.7 %
of the objective) and LOSS10 (+565, t +2.1) and pays for it on the band —
LIVEC42 (−382, t −1.6) and W2band (−249, t −1.3), together 54 % of the weight**.
Net −19.6 weighted coins/episode ≈ flat, which is exactly why `mean_win` shows
nothing. The held-out judge is band-dominated (LIVE-C 43-102 is the same tape
family as LIVEC42+W2band), so a trade that is free inside the objective reads as
a pure −580 loss on the judge. The C′ reading stands underneath it: the step is
tiny (0.086 % of ‖θ‖), its per-board damage does not persist from g10 to g20
(ρ +0.15), and the family t-values are 1.3-2.1σ on a single draw of six
families — suggestive, not established.

Thetas: B = `submission/theta.npy` (md5 7fcf3948, LIVE sub 56161192);
g20 centre = `artifacts/kagg2_games/thetas/flow209_g20s_hr.npy` (md5 5e102d64,
extracted from `S/snr/flow209/state_g00020.npz`).
Tools: `S/objaudit/{audit.py,rungmap.py,obj_rungs.py,run_train42.sh,both_train42.sh,screen.py}`.
`screen.py` is a byte copy of `S/simscreen/screen.py` so the shared tool and its
frozen board files are untouched; the board list is rebuilt at
`S/objaudit/boards_livec102.json` with `--tapes livec --seeds 1 --seed-base 777001`,
which gives every tape **the engine leg's own seed** (opponent index *i* in
`S/livec/ids.txt` → `rng(777001 + 1000003·(i+1))`, verified against the first row
of `flow193_g100_hr_livech.csv`, seed 1196709180 at index 42).

## 0. The board sets are clean, and nothing in the objective is "the judge"

`S/objaudit/rungmap.py` reads flow209's own launcher: 166 pinned rungs,
total rung weight 618.

| family | rungs | weight | share of the pinned objective |
|---|---|---|---|
| TOPTEN (w 10.2) | 20 | 204 | 33.0 % |
| W2 band (w 2) | 85 | 170 | 27.5 % |
| LIVEC42 = LIVE-C 1-42 (w 4) | 42 | 168 | 27.2 % |
| LOSS10 (w 4) | 10 | 40 | 6.5 % |
| TOP50 (w 4) | 9 | 36 | 5.8 % |

**Zero** of the held-out judge ids (LIVE-C 43-102, TOPB2) appear among the 166
training rungs. LIVE-C is therefore the one family that can be read *in sample*
(1-42) and *out of sample* (43-102) on tapes of the same provenance, which is
what this audit uses.

The trainer's own banner (reproduced by `S/objaudit/obj_rungs.py` running
flow209's launcher to the brink of generation 1) reads
`pinned-once: 166 pinned rungs x 1 episode + 13 episodes carried`, i.e. the
self-play half is **13 of 179 episodes** and carries none of the 618 rung
weight. "The self-play episodes" is therefore not a live candidate for D on
weight alone, before any measurement.

The step itself is tiny: the same probe reports `centre == B: True`,
**‖g20 − B‖ = 0.0155** against **‖B‖ = 18.112** — 0.086 % of the centre, over
20 generations, in the 1,191-coordinate trained subspace. (Twenty fully
coherent steps at the recipe's priced length of 0.002 would be 0.04, so the
walk is ~39 % coherent — consistent with §104's block cosine.) That 0.086 %
displacement is what costs 580 coins of held-out margin.

## 1. The table: sim vs engine × training vs held out

g20 centre minus B, paired per board (a board = one pinned tape; the two seats
of a tape are the same pinned game played from both sides, so they are averaged
before the SE — `n` is rows, `boards` is the honest unit).

| set | source | rows | B win% | g20 win% | Δmargin | SE (board) | t (board) | flips |
|---|---|---|---|---|---|---|---|---|
| **TRAIN42 (LIVE-C 1-42, IN SAMPLE)** | engine | 84 | 88.1 | 76.2 | **−71** | 263 | **−0.27** | +0/−10 |
| **TRAIN42 (LIVE-C 1-42, IN SAMPLE)** | sim | 84 | 88.1 | 81.0 | **−187** | 273 | **−0.68** | +0/−6 |
| H30 (LIVE-C 43-72, held out) | engine | 60 | 63.3 | 63.3 | −516 | 172 | −2.99 | +0/−0 |
| H30 (LIVE-C 43-72, held out) | sim | 60 | 63.3 | 63.3 | −597 | 157 | −3.81 | +0/−0 |
| H30B (LIVE-C 73-102, held out) | engine | 60 | 83.3 | 73.3 | −645 | 278 | −2.32 | +0/−6 |
| H30B (LIVE-C 73-102, held out) | sim | 60 | 80.0 | 76.7 | −698 | 298 | −2.34 | +2/−4 |
| TOPB2 (held out) | engine | 40 | 32.5 | 25.0 | −197 | 471 | −0.42 | +0/−3 |

Pooled (seat-averaged boards):

| | engine | sim |
|---|---|---|
| held-out 60 boards (43-102) | **−580 SE 162, t −3.58** | **−647 SE 167, t −3.88** |
| training 42 boards (1-42) | **−71 SE 263, t −0.27** | **−187 SE 273, t −0.68** |
| out-of-sample minus in-sample | −509 SE 309, t −1.65 | −460 SE 320, t −1.44 |

Three readings fall straight out.

1. **The sim is not lying (A is refuted).** On every set the sim reproduces the
   engine's sign, size and t to well inside the noise: −187 vs −71, −597 vs
   −516, −698 vs −645. Per board the two agree at Spearman **+0.774** (Pearson
   +0.813, sign agreement 82 %) over the 120 held-out rows, +0.779 on the 84
   training rows, +0.883 on H30B. `sim = engine` (the 2026-09-06 standing claim)
   survives this test, so nothing about shop draw, town, seat or self-play
   needs hunting: whatever the ES is doing, the sim is telling it the truth.
2. **There is no NET in-sample gain (B is refuted; D survives only as the
   internal transfer of §5).** g20 does not beat B on
   LIVE-C 1-42 in the sim (−187 t −0.68) or in the engine (−71 t −0.27); its
   board win rate there actually FALLS (88.1 % → 76.2 %, ten games flipped down,
   none up). Memorisation requires something memorised; there is nothing. The
   same holds for the two other in-sample families already measured:
   TOPTEN in sample −224 SE 247 t −0.91 (§101, `S/topb2/run_insample.sh`) and
   LOSS10 in sample −49 t −0.19 (00:45Z autojudge, B's own ten ladder-loss
   boards ARE the LOSS10 rungs). That is 66.7 % of the objective's weight, all
   level or slightly negative, and the trainer's own `mean_win` is flat. The
   aggregate is therefore not where the answer is: §5 opens the objective up
   and finds that TOPTEN and LOSS10 DID rise while the band fell.
3. **The held-out loss is broad, not three boards (C in its naive form is also
   wrong).** On H30 the worst three boards carry 27.9 % of the deficit and the
   mean is still −391 after dropping them; on H30B, 32.0 % and −461. 19/30
   boards are negative on each leg (38/60 pooled, sign test p ≈ 0.03), median
   −350 and −366. The −580 is a shift of the whole distribution, not a tail.
   Contrast TOPB2, where the "deficit" IS a tail (worst three = 266 % of the
   total, +353 after dropping them) — which is why TOPB2 reads level.

## 2. What the g10 → g20 comparison adds

| leg (boards, seat-averaged) | g10 − B | g20 − B | ρ(per-board g10, g20) |
|---|---|---|---|
| H30 (30) | −32 SE 123 | −516 | +0.07 |
| H30B (30) | +202 SE 400 | −645 | +0.18 |
| pooled (60) | **+85 SE 208** | **−580 SE 162** | **+0.15** (r +0.28) |

g20 − g10 = **−665 SE 226 (t −2.9)** on the held-out boards. So the second
10-gen block did the damage, and it did it on *different* boards from the first
(ρ +0.15): the per-board incidence of the loss does not persist even though the
step direction does (§104's +0.82 is a cosine between centre *displacements* in
1,191-dim theta space, not between board-level effects). Ten boards that g10
had improved are among the ones g20 has hurt and vice versa.

This is the qualifier on C. Two things are simultaneously true:

* for **this theta**, −580 SE 162 is a real deficit against B (t −3.6, and the
  sim confirms it at t −3.9 on independent noise), so "g20 is level with B" is
  false; but
* the **trajectory** is not yet shown to be monotonically descending: g10 was
  +85 SE 208, g20 is −580 SE 162, and the boards carrying each are nearly
  uncorrelated. A third point (g30) is what separates "the direction walks
  steadily downhill on held-out play" from "each centre is a fresh draw around
  a mean a few hundred coins below B".

## 3. Mechanism: a step that costs without buying

Put the three measurements together:

* the ES's own objective is FLAT from g1 to g18 (`mean_win` 0.6660 → 0.6649);
* on 66.7 % of the objective's weight, measured directly in the engine and the
  sim, g20 is level with B (LIVEC42 −71/−187, TOPTEN −224, LOSS10 −49);
* on boards of the same provenance that the objective never sees, g20 is
  −580 SE 162 (sim −647 SE 167).

So the direction the ES is walking is not an improvement direction at all. It
is a direction along which the CRN-paired, rank-normalised in-sample fitness is
*indifferent* — the ES cannot distinguish it from zero (§72: disjoint-draw
cosine 0.039, dimension-limited; §77: κ ≈ 0.01-0.03) — and along which a tuned
centre's out-of-sample play degrades, because B is a strict local optimum in its
own lattice (§76) and any displacement off it is, in expectation, worse
everywhere; in sample the ES's selection keeps the loss from showing, out of
sample nothing does. `sgd --optimizer sgd` with β₁ 0.9 then makes that
indifferent direction *persistent*: the momentum buffer integrates 20
generations of a gradient whose per-generation SNR is ~0.01, so the walk is
smooth (cos 0.82) without being informative. §104's persistence test and this
audit are therefore consistent: the direction is reproducible AND worthless.

## 4. Implication for the recipe

Nothing here says "rotate the training set" (that would be the fix if the answer
were B) and nothing says "the sim is lying" (the fix if it were A). The binding
facts are two: **(i)** flow209's net objective is flat, so the step is
indistinguishable from noise in aggregate and costs ~580 coins of held-out
margin per 10 generations; and **(ii)** it is flat because it is a *transfer*
out of the band (LIVEC42 −382, W2band −249, 54 % of the weight) into TOPTEN
(+461, 32.7 %) and LOSS10 (+565) — and the judge only sees the side that was
sold. Concretely:

1. **flow209's g30 read is the decision point, and it should now be read on the
   HELD-OUT margin, not only on the block cosine.** §104's rule ("persistence
   at g30 keeps the GPU") is not sufficient: persistence has been demonstrated
   and is compatible with a worthless direction. The additional falsifier is
   cheap: if g30 − B on the 60 LIVE-C held-out boards is again ≤ −300 with the
   per-board pattern again uncorrelated with g20's, the arm is walking, not
   learning, and it should be retired on the third loss as the standing rule
   says. If g30 − B returns to level, the g20 reading was the draw and C′ holds
   in its weakest form.
2. **Do not raise the lr on a persistence reading alone.** §104 floated "raise
   its lr only after a g40 engine read"; this audit sharpens that to: a larger
   step along an indifferent direction buys a proportionally larger held-out
   loss (g10 ≈ half the displacement, +85; g20, −580). lr goes up only after a
   checkpoint that is *positive* out of sample, never after one that is merely
   consistent.
3. **flow211's top-ten cut now has a direct reason, different from the one
   §103 falsified.** §101 read the 32.7 % clause as "buys −224 coins, releases
   no stored gain"; §5 here reads it as the clause the g20 step is *spending
   into* (+461, t +2.0) at the band's expense (−382/−249). Cutting 32.7 % → 10 %
   would remove the transfer's destination, which is a coherent reason to run
   flow211 — but it is one draw at 2σ, and §105's ρ 0.93 still says the step
   DIRECTION would barely move. Before launching on this, repeat §5 on 3-4 batch
   seeds (~10 min GPU each); if both band families stay negative and TOPTEN
   stays positive, the cut is justified as a *support* change, not a direction
   change. Re-pointing weights still cannot fix an SNR of 0.01.
4. **The sim screen is now validated as the cheap judge for ES centres**
   (ρ +0.77 per board, Δmargin within ~80 coins of the engine on three sets, 697 s
   for 408 episodes vs ~22 min of engine legs). Future centre reads can be
   screened in the sim first and only promoted to engine legs when the sim
   Δ clears zero — that is a 20× cheaper g30/g40 read than the four standard legs.

## 5. The objective itself: B vs g20 on all 166 rungs, the trainer's own boards

`S/objaudit/obj_rungs.py` runs flow209's launcher to the brink of generation 1
(so ladder, tapes, pinned slots, masks and `--pinned-once --pinned-fixed-seed`
seeding are the arm's own), builds one generation's batch, and pushes B and the
g20 centre through the trainer's own `_play` as a 2-row population. This IS the
quantity the ES optimises — not a proxy. One draw, 178 episodes (166 pinned +
12 self-play).

| family | eps | rung weight | B margin | g20 margin | Δmargin | SE | t | Δwin |
|---|---|---|---|---|---|---|---|---|
| **TOPTEN (w 10.2)** | 20 | 408 (32.7 %) | −70 | +391 | **+461** | 232 | **+1.99** | +0.050 |
| **LOSS10 (w 4)** | 10 | 80 (6.4 %) | −3,500 | −2,935 | **+565** | 264 | **+2.14** | 0.000 |
| **LIVEC42 (w 4)** | 42 | 336 (26.9 %) | 6,636 | 6,255 | **−382** | 237 | **−1.61** | −0.071 |
| **W2 band (w 2)** | 85 | 340 (27.2 %) | 5,271 | 5,023 | **−249** | 186 | **−1.34** | 0.000 |
| TOP50 (w 4) | 9 | 72 (5.8 %) | 548 | 18 | −531 | 957 | −0.55 | 0.000 |
| self-play | 12 | 12 (1.0 %) | 0 | −543 | −543 | 1,216 | −0.45 | −0.167 |
| ALL | 178 | 1,248 | 3,906 | 3,717 | −189 | | | |

`mean_win` (unweighted, train.py:5009) B 0.6742 → g20 0.6517 (−0.0225);
objective-weighted win B 0.5904 → g20 0.5859 (**−0.0045**). Weighted margin:
+188,088 (TOPTEN) + 45,200 (LOSS10) − 128,352 (LIVEC42) − 84,660 (W2band)
− 38,232 (TOP50) − 6,516 (self-play) = **−24,472 / 1,248 = −19.6 coins per
weighted episode** — flat, which is why the training curve shows nothing.

**This is the answer to D, and the rung subset is named.** The step is a
*transfer*: it buys top-ten margin (+461 on the 20 w-10.2 rungs that are 32.7 %
of the objective, B's weakest family at −70) and hard-board margin (+565 on
LOSS10, where B is −3,500) by giving up band margin (−382 LIVEC42, −249 W2band,
54 % of the weight and the families B is already winning by 5-6.6k). Inside the
objective that trade is free — rank-normalised advantage does not care that it
moved coins from a family it is winning to a family it is losing. The judge is
not indifferent: LIVEC-H30/H30B, LIVE62 and NEXT30 are all band tapes of the
same provenance as LIVEC42+W2band, and TOPB2 is a *different* set of top-tier
tapes from the 20 trained TOPTEN rungs, so none of the purchased top-ten gain
is visible to it while all of the sold band margin is.

Caveats, stated plainly: one draw, six families, |t| 1.3-2.1 — with six
comparisons one |t| > 2 is expected by chance, so the individual cells are
suggestive. What is robust is the *sign pattern* (both band families down, both
non-band families up) and its agreement with the independent engine/sim reads in
§1 (LIVEC42 in the engine −71, in the sim −187, here −382 on the trainer's own
boards: same sign, all inside each other's noise).

## 6. What was not done

* TOPB2 was not screened in the sim (engine already reads level, t −0.42, and
  its deficit is a three-board tail).
* The §5 draw is a single episode batch. Repeating it on 3-4 batch seeds would
  turn the family signs into a measurement; that is ~10 min of GPU each
  (`--chunk 64`, 5 min of it XLA compile).
