# The flow209 step ladder: is the learning rate the binding constraint?

2026-09-12, 00:22-01:14Z.  Follows section 104 of `2026-09-10-consensus.md` and
`2026-09-11-snr-reader.md`.

## The question

flow209 (seed = candidate **B**, `submission/theta.npy` md5 `7fcf3948`; sgd lr 1.8e-4,
sigma 0.01, pop 4,096, 1,191 trained genes) has moved its centre in a **consistent**
direction over g0 -> g10 -> g20: block cosine +0.82 against a momentum-null p95 of
+0.54.  But the step is minute (section 93) and the g10 engine legs were level vs B.
Consistency is not profit.  So: walk further along the SAME direction and see whether
it pays.

    theta(alpha) = theta_B + alpha * (theta_g20 - theta_B),  theta_g20 = S/snr/flow209/state_g00020.npz['theta']

alpha = 1 *is* the g20 centre (the arm the judge is running as `flow209_g20s_hr`).
alpha = -4 is the antisymmetric control of the one-step protocol (sections 56 / 72):
a real descent direction gains at +alpha and loses at -alpha; noise does neither; a
**cliff** loses at both.

## The delta, in sigma-draws

`theta_g20 - theta_B` is nonzero on **exactly 1,191 of 6,789** genes -- the trained
block named by `config.json` (`train_only gp,dh,ds,g5,gb5,w3,b3,b1`), verified, no
leakage into the 5,598 frozen genes.  `||Delta|| = 0.015491`, `max|Delta| = 0.004413`.
`||theta_g10 - theta_B|| = 0.007098`, so generations 10-20 moved as far as 0-10.

One perturbation draw over the trained block is `sigma*sqrt(d) = 0.01*sqrt(1191) =
0.3451`.  **The whole 20-generation move is 0.045 of ONE draw.**

| alpha | \|\|alpha*D\|\| | in sigma-draws | rms/coord / sigma | max\|alpha*D\| / sigma |
|---:|---:|---:|---:|---:|
|  1 | 0.0155 | 0.045 | 0.045 | 0.44 |
|  2 | 0.0310 | 0.090 | 0.090 | 0.88 |
|  4 | 0.0620 | 0.180 | 0.180 | 1.77 |
|  8 | 0.1239 | 0.359 | 0.359 | 3.53 |
| 16 | 0.2479 | 0.718 | 0.718 | 7.06 |
| -4 | 0.0620 | 0.180 | 0.180 | 1.77 |

**alpha = 16 is 0.72 of a full sigma draw**, i.e. 0.72 sigma rms per trained
coordinate.  The top of the ladder is still *inside* the cloud the ES samples every
single generation -- nothing here extrapolates outside the region the search itself
already visits, so a loss at alpha = 16 cannot be dismissed as "too far out".

Cross-check that the reconstruction is exact: `theta_a1` matches the judge's own
`artifacts/kagg2_games/thetas/flow209_g20s_hr.npy` to 5.8e-11 (2 genes differ in the
last float32 bits) and its NEXT30 csv is **row-for-row identical** to the judge's
independent `flow209_g20s_hr` NEXT30 leg.

## Step 1 -- sim screen (`S/simscreen/screen.py`, hr switches, unmodified)

Pinned-town action-seat screen, `shop_crn` on, paired against B on frozen boards.
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON` all True.  `shopdiff 0.0 %`
on every row: no theta re-rolled a shop, so these are clean paired comparisons.

### LIVE-C hold-out, 120 boards

| alpha | win % | mean margin | d-margin/game vs B | sd | t |
|---:|---:|---:|---:|---:|---:|
| B (ref) | 71.7 | +5,279 | +0 | - | - |
|  1 | 73.3 | +4,866 | **-413** | 1,893 | -2.39 |
|  2 | 72.5 | +4,988 | **-291** | 1,875 | -1.70 |
|  4 | 66.7 | +4,741 | **-538** | 2,543 | -2.32 |
|  8 | 63.3 | +3,908 | **-1,371** | 2,334 | -6.43 |
| 16 | 46.7 | -663 | **-5,942** | 3,450 | -18.87 |
| **-4** | 73.3 | +4,898 | **-381** | 2,317 | -1.80 |

### TOPB2 top tier, 40 boards

| alpha | win % | mean margin | d-margin/game vs B | sd | t |
|---:|---:|---:|---:|---:|---:|
| B (ref) | 32.5 | -1,472 | +0 | - | - |
|  1 | 25.0 | -1,684 | **-212** | 2,298 | -0.58 |
|  2 | 30.0 | -2,154 | **-682** | 2,721 | -1.58 |
|  4 | 30.0 | -2,283 | **-812** | 2,850 | -1.80 |
|  8 | 20.0 | -3,117 | **-1,645** | 3,113 | -3.34 |
| 16 | 10.0 | -8,125 | **-6,654** | 4,929 | -8.54 |
| **-4** | 30.0 | -2,760 | **-1,288** | 2,849 | -2.86 |

Shape: **monotone decay in |alpha| on both sets, and +4 and -4 lose alike**
(LIVE-C -538 vs -381; TOPB2 -812 vs -1,288).  There is no alpha at which the
extrapolation is worth more than B, not even at 0.09 of a draw.  The best cell on the
ladder is alpha 1-2, and it is still negative.

## Step 2 -- paired real-engine legs vs B

NEXT30 (30 pinned-town boards of the 2550-2750 band, both seats = 60 games,
`S/nextband/run.sh`, WORKERS=4, hr switches, arms-next worktree).  Statistic =
`S/bank/paired.py` board-level t (two seats averaged into one observation).

| alpha | games | B win % | arm win % | d/board | board sd | SE | t | flips W/L |
|---:|---:|---:|---:|---:|---:|---:|---:|:--|
|  1 | 60 | 68.3 | 70.0 | **-201** | 1,195 | 218 | **-0.92** | 1 / 0 |
|  2 | 60 | 68.3 | 70.0 | **-379** | 1,262 | 230 | **-1.64** | 1 / 0 |
|  8 | 60 | 68.3 | 60.0 | **-1,606** | 1,731 | 316 | **-5.08** | 1 / 6 |
| 16 | 60 | 68.3 | 35.0 | **-7,329** | 4,406 | 804 | **-9.11** | 0 / 20 |
| -4 | 60 | 68.3 | 71.7 | **-414** | 2,167 | 396 | **-1.05** | 3 / 1 |

alpha 8 and 16 were added after the fact to test the screen's cliff in the REAL engine
rather than the proxy, and they reproduce it: -1,606 (t -5.08) and -7,329 (t -9.11),
against the screen's LIVE-C -1,371 and -5,942.  The engine and the sim agree on the
cliff's position and size to within ~20 %, and alpha 16 turns twenty of B's thirty-
board wins into losses (68.3 % -> 35.0 %).  The ladder is not a screen artefact.

LIVEC-H30B (LIVE-C ids 73-102, 30 pinned boards x 2 seats = 60 games,
`S/livec/run_holdout2.sh`, WORKERS=4).  B's own reference leg `sl_B` was re-run here
and reproduces the archived plain-B line to the coin (+1,031 vs hr, 83.3 %, 8/0).

| alpha | games | B win % | arm win % | d/board | board sd | SE | t | flips W/L |
|---:|---:|---:|---:|---:|---:|---:|---:|:--|
|  1 | 60 | 83.3 | 73.3 | **-645** | 1,521 | 278 | **-2.32** | 0 / 6 |
|  2 | 60 | 83.3 | 76.7 | **-98** | 2,139 | 391 | **-0.25** | 0 / 4 |
| -4 | 60 | 83.3 | 80.0 | **-555** | 2,189 | 400 | **-1.39** | 2 / 4 |

Pooled over both engine families (60 independent boards per alpha):

| alpha | boards | d/board | SE | t |
|---:|---:|---:|---:|---:|
|  1 | 60 | **-423** | 177 | **-2.38** |
|  2 | 60 | **-238** | 226 | **-1.06** |
| -4 | 60 | **-485** | 279 | **-1.74** |

On LIVEC-H30B the flip ledger is one-directional: alpha 1 turns SIX of B's wins into
losses and flips none back; alpha 2 loses four and wins none back.  A step that only
ever costs boards is a step off a cell, not a step down a slope.

Same shape as the screen: alpha 1 is the shallowest loss, alpha 2 is worse, and
alpha -4 -- the antisymmetric control that a REAL direction must make *worse* -- is
indistinguishable from alpha +4's screen loss and no better than alpha +2 on the
engine.  Nothing here is significant on its own; what is significant is that nothing
on the ladder is positive, and the ladder's *slope* in |alpha| is unmistakable on the
1,120 screened boards (t -18.9 at alpha 16).

## The three answers

**(i) Shape of the screen: LOSS AT BOTH SIGNS, monotone in |alpha|.**  Not "monotone
gain" (the direction is not lr-limited) and not "flat" (the direction is not merely
unprofitable-but-harmless).  Both signs of a step along the g20 direction cost coins,
and the cost grows smoothly with the step, reaching -5,942/game on LIVE-C at 0.72 of a
sigma draw.  That is the section 60 / 66 signature: **B sits in a cell of the decode
lattice and every extrapolation walks off it**.  The g0->g20 centre motion is real as
motion (cosine +0.82) but it is drift *inside* B's cell -- the consistency comes from
the optimiser's own momentum over a flat, switch-bounded region, not from a gradient
that pays.

Corroborating detail: the screen's `shopdiff` is 0.0 % for every alpha, so this is not
the +/-25k shop-draw lottery.  And alpha 1 and alpha 2 score -413 / -291 with t -2.4 /
-1.7 on 120 boards -- the sub-cell wobble is *already* bigger than the signal, which is
exactly what a 0.045-draw step into a flat cell should look like.

**(ii) Engine confirmation.**  The chosen alphas (best-by-screen alpha 1 and 2, plus
the antisymmetric alpha -4) come back NEGATIVE on every one of the six legs run:
NEXT30 -201 / -379 / -414 (t -0.92 / -1.64 / -1.05) and LIVEC-H30B -645 / -98 / -555
(t -2.32 / -0.25 / -1.39).  Pooled over the 60 independent boards each alpha played:
**-423 (t -2.38), -238 (t -1.06), -485 (t -1.74)** for alpha 1, 2, -4.  The g20 centre
itself (alpha 1) is the one arm that reaches the -2 sigma mark, and it does so on the
LOSING side -- so the engine does not merely fail to confirm a gain, it reads the
20-generation move as a small real cost.  The +alpha / -alpha asymmetry a real
direction owes us is absent: -4 is as bad as +1.  **No profitable step exists along
this direction at any scale up to 0.72 sigma.**

**(iii) Recommendation for flow209: do NOT raise the lr.  Keep it (or stop the arm).**

The step ladder's peak is alpha ~ 1, i.e. the lr flow209 is already using.  Reading
the recipe the mechanical way the brief asks -- "the alpha that peaked x 1.8e-4 over
20 gens" -- gives **1 x 1.8e-4 = 1.8e-4, the current lr**.  Raising lr moves flow209
DOWN the ladder we just measured: lr 3.6e-4 would land it near alpha 2 (-291 / -682 on
the screens), lr 7.2e-4 near alpha 4, and lr 2.9e-3 -- the lr the arms ran before
section 59 cut it -- near alpha 16, which is the -5,942/game cliff.  That retroactively
explains the lr-0.003 "noise walk" of section 59: it was not noise-limited, it was
walking off the cell at ~0.7 sigma per 20 generations.

So: **keep lr 1.8e-4**, and understand that what flow209 is doing is not slow descent
that a bigger step would speed up -- it is drift across a flat cell whose every exit is
downhill.  More generations at this lr buy consistency, not coins.  The section 104
"consistent direction" finding survives as a statement about the optimiser, and is
hereby **closed as a source of expected gain**.  The live constraint is the one section
60 / 66 / 76 keep naming: B is a strict local optimum of its decode lattice, and the
lever is the ACTION INTERFACE (what the genes can express), not the step size with
which we walk the genes we have.

## Caveats

* Each engine alpha has 60 independent boards (NEXT30 30 + LIVEC-H30B 30), pooled
  SE 177-279 coins/board: the legs cannot resolve anything smaller than about
  +/-400/board at 2 sigma.  They rule out a *large* gain at alpha 1-2, not a 100-coin
  one.  The screen (120 + 40 boards, sd 4.6x lower than an engine leg) is what carries
  the ladder's shape at the SMALL end; at the top end the engine measured alpha 8 and
  16 itself and agreed with it.
* LIVEC-H30B overlaps the family flow209 trains on far more than NEXT30 does, and it
  is the harsher of the two legs for alpha 1 (-645, t -2.32).  Read the pooled number,
  not either leg alone; the two legs disagree on which of alpha 1 and alpha 2 is worse
  (NEXT30 says 2, LIVEC-H30B says 1), which is exactly the +/-200-coin leg lottery the
  board counts predict and is why neither is called significant on its own.
* The screen is an action-replay opponent seat on pinned towns; it equals the engine
  to 99.5 % on this family (`sim-equals-engine-2026-09-06`) but it is still a proxy.
  Its verdict and the engine's agree in sign on all three alphas measured both ways.
* alpha = -4 is a control, not a candidate: nobody proposes running flow209 backwards.
  Its only job was to break the tie between "real direction, too small a step" and
  "cliff".  It came back a loss, so: cliff.
* Only ONE lineage and ONE 20-generation window was extrapolated.  A different seed
  (flow210, seed hr) could in principle sit somewhere with a real slope; this says
  nothing about it.  It does, however, kill the general hope that the lr is what stands
  between the section-104 cosine and a candidate.
* The whole ladder is linear extrapolation.  If the true improving path curves away
  from the g0->g20 chord within 0.045 of a draw, no linear alpha would find it -- but
  a path that curves that fast is not something a larger lr along the chord would find
  either, which is the question that was asked.
