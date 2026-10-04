# The `lots` block, one-step tested at candidate B (E3c) — 2026-09-11

**Question.** Candidate B is a strict local optimum for the ES in its 6,789-gene
space (consensus §72–§80: no block survives multiplicity, the integer lattice is
closed, pinned ints and dithered decode are both NO-GO). The remaining lever is a
NEW decision dimension. `S/lots/` stages one: 130 genes (`("lots", (65, 2))`,
6,789 → 6,919) giving two independently signed sell-lot coin offsets per product,
inert at zero and decodable at σ 0.01 (27 % of cells move ≥ 1 coin). Before a
remote GPU is spent on flow208, the same one-step antisymmetric test that refused
the dither remedy was run on the lots block.

Pre-registration: `S/lots/onestep_prereg.md`, written before the launch.

## What ran

| | |
|---|---|
| Driver | `S/lots/run_onestep_lots.sh` → `S/onestep/sweep_c.py` (UNMODIFIED; no copy made) |
| Log | `S/lots/run_onestep_lots.log`, `S/lots/run_onestep_lots.out` |
| Tree | `/root/tree_lots` = `S/localarm/tree` (the tree B was trained in, the dither run's base) + `S/lots/policy_lots.patch` on `core/{policy,brain,sell,plan}.py`, no rejects. `N_PARAMS 6919`, `offset("lots") == 6789` |
| Centre | `S/lots/theta_B_pad6919.npy` — B (`flow193_g100_hr.npy`, md5 41b87adc) zero-padded through `PO.pad`; head byte-identical, tail 130 all zero. The run confirms `matches-file True` |
| Launcher | `S/lots/launch_onestep_lots.sh` = `S/flow193/launch_flow193.sh` with `--train-only all` → `--train-only lots`. Run line: `n 6919 live 130` |
| Restriction to the block | `popcurve.one_draw` builds `eps = perturbations(...) * tr.mask`, so the trainer's own `--train-only lots` mask restricts the draw, the ES direction and the 8 random controls to the 130 coordinates. **No `--coord-mask` option was needed and `S/onestep/sweep_c.py` / `S/dither/` were not touched** |
| Cell | σ 0.01, pop 512 (`s0p01_p512`), eps seed 9001, 8 randoms (rng 777), 4 permuted-advantage controls (rng [4242, σ, pop]) |
| Blocks | IN-SAMPLE = the arm's own batch (159 episodes, 147 pinned). HELD-OUT = LIVE-C 43–72 × 2 seats, `S/onestep/heldout_ids.txt`, 32 episodes — the dither run's block, unchanged |
| Screen | skipped (not part of the E3c verdict) |

## Deviation from the dither protocol, and why

One, pre-registered: **the step-length unit**. The dither run's ladder is
`R = lr·sqrt(n_live)` at `lr 0.003`, `n_live 5997` → `R = 0.2323`. Carried over
literally at `n_live = 130` that is `R = 0.0342`, and every α on the ladder would
be **decode-inert**: the lots decode is `round(8·z)` and B's block is exactly
zero, so a step only changes a decision once `|8·δz| ≥ 0.5`, i.e. `‖δθ‖ ≳ 0.12`
(`sd(δz) ≈ 0.50·‖δθ‖`, from ‖h‖ = 5.63 in `S/lots/slope.json`). `+d`, `−d` and
the centre would score identically and the test would read pure noise.

So `--lr 0.1` was used, making the ladder a multiple of the natural unit of this
block — the norm of one σ-perturbation:

    R = 0.1*sqrt(130) = 1.1402 = 10 x ||sigma*eps||        (||sigma*eps|| = 0.1140, as printed)
    alpha 0.03 -> ||step|| 0.0342 = 0.3 perturbations   (expected near-inert)
    alpha 0.1  -> ||step|| 0.1140 = 1.0 perturbation    <- the verdict alpha
    alpha 0.3  -> ||step|| 0.3421 = 3   perturbations
    alpha 1.0  -> ||step|| 1.1402 = 10  perturbations   (diagnostic / cliff)

This keeps the E3c rule's text ("at SOME α ≤ 0.1") intact and makes it a
*tighter* claim than it was for dither: a pass must come from a step no longer
than the noise the gradient was estimated in.

## Cost and integrity

`1,381 s` wall (draw 369 s, in-sample 105 thetas, hold-out both seat phases),
GPU 0 alone, no arm on the card. Integrity lines from `run_onestep_lots.log`:

    [draw s0p01 pop 512 369s] ||g|| 23.6816  off-mask ||g|| 0.00e+00  win 0.7323
                              adv-rebuild cos 1.000000 ratio 1.000000
    [perm s0p01_p512] ||g_perm||/||g|| [0.6699, 0.6121, 0.6565, 0.6282]
                      cos(g_perm, g)   [-0.1777, -0.1157, -0.0082, -0.0768]

`off-mask ||g|| = 0` is the proof the whole reading lives in the 130 new
coordinates: B's other 6,789 numbers are untouched by every theta scored.

**The centre is B.** `matches-file True`, and its scores reproduce E3's
*undithered* centre (`S/onestep/sweep_b.txt`, same tree, same launcher, same
hold-out) to within the rig's own build-to-build spread — held-out
`obj_w +0.64928` vs `+0.64932`, `win_w +0.63333` vs `+0.63333` (exact),
`margin +3980` vs `+3981`; in-sample `+0.63144` vs `+0.63066`, inside the
`0.63060–0.63146` spread sweep_b's own three cells show at that same centre.
That is an inertness check on the real objective, on top of the 20/20
simulator-level proof in `S/lots/README.md`.

## The table, verbatim (`S/lots/sweep_lots.txt`)

```
E3c one-step test at candidate B (flow193_g100_hr)   n_live 130  nrand 8 (16 signed)  nperm 4  alphas 1,0.3,0.1,0.03  R 1.1402

--- IN-SAMPLE (the arm's own batch)
cell         alpha metric       F(c)   +d gain   -d gain   antisym   | r_mean     r_sd    z_r     k_r   a>r   | p_mean     p_sd    z_p     k_p   a>p  rand<+d
s0p01_p512       1 obj_w    +0.63144  -0.14759  -0.01294  -0.13466   +0.00690 +0.00825 -16.32 -1.4312   0/8   -0.00526 +0.00500 -26.95 -2.3640   0/4     0/16
s0p01_p512       1 win_w    +0.65036  -0.18978  -0.01423  -0.17555   +0.00652 +0.01152 -15.24 -1.3365   0/8   -0.01058 +0.01477 -11.88 -1.0424   0/4     0/16
s0p01_p512       1 margin      +4559     -4093      -723     -3371       +208     +213 -15.83 -1.3884   0/8        -15     +585  -5.77 -0.5057   0/4     0/16
s0p01_p512     0.3 obj_w    +0.63144  -0.01265  -0.01256  -0.00010   +0.00077 +0.00651  -0.01 -0.0013   3/8   -0.00296 +0.00464  -0.02 -0.0018   3/4     0/16
s0p01_p512     0.3 win_w    +0.65036  +0.00584  -0.01423  +0.02007   -0.00666 +0.01314  +1.53 +0.1340   8/8   -0.00830 +0.01713  +1.17 +0.1028   4/4    13/16
s0p01_p512     0.3 margin      +4559      -341      -646      +305         +9     +250  +1.22 +0.1072   7/8        +81     +530  +0.58 +0.0506   2/4     1/16
s0p01_p512     0.1 obj_w    +0.63144  +0.00182  -0.00525  +0.00706   +0.00006 +0.00368  +1.92 +0.1684   8/8   -0.00400 +0.00607  +1.16 +0.1020   4/4    15/16
s0p01_p512     0.1 win_w    +0.65036  -0.00182  -0.02372  +0.02190   -0.00490 +0.00930  +2.35 +0.2064   8/8   -0.00443 +0.01676  +1.31 +0.1146   4/4     5/16
s0p01_p512     0.1 margin      +4559      +124      -495      +619        -89     +158  +3.91 +0.3428   8/8         -2     +380  +1.63 +0.1429   4/4    15/16
s0p01_p512    0.03 obj_w    +0.63144  +0.00356  -0.00458  +0.00814   -0.00004 +0.00023 +35.95 +3.1533   8/8   +0.00022 +0.00026 +30.87 +2.7072   4/4    16/16
s0p01_p512    0.03 win_w    +0.65036  +0.01314  -0.00182  +0.01496   +0.00000 +0.00000   +nan    +nan   8/8   +0.00000 +0.00000   +nan    +nan   4/4    16/16
s0p01_p512    0.03 margin      +4559       +64      -246      +310         -1       +2+167.52+14.6928   8/8         +1       +2+149.92+13.1487   4/4    16/16

--- HELD-OUT (LIVE-C 43-72 x 2 seats)  <-- THE VERDICT
cell         alpha metric       F(c)   +d gain   -d gain   antisym   | r_mean     r_sd    z_r     k_r   a>r   | p_mean     p_sd    z_p     k_p   a>p  rand<+d
s0p01_p512       1 obj_w    +0.64928  -0.10983  -0.01687  -0.09296   +0.00433 +0.01068  -8.70 -0.7634   0/8   +0.00068 +0.01609  -5.78 -0.5068   0/4     0/16
s0p01_p512       1 win_w    +0.63333  +0.03333  +0.00000  +0.03333   +0.00417 +0.01179  +2.83 +0.2481   7/8   +0.00000 +0.00000   +nan    +nan   4/4    16/16
s0p01_p512       1 margin      +3980     -3463      -668     -2795       +170     +270 -10.37 -0.9092   0/8       +143     +421  -6.64 -0.5826   0/4     0/16
s0p01_p512     0.3 obj_w    +0.64928  -0.01406  -0.01580  +0.00174   -0.00090 +0.00711  +0.25 +0.0215   5/8   -0.00459 +0.01132  +0.15 +0.0135   3/4     1/16
s0p01_p512     0.3 win_w    +0.63333  +0.00000  +0.00000  +0.00000   -0.00417 +0.01179  +0.00 +0.0000   1/8   +0.00000 +0.00000   +nan    +nan   0/4     0/16
s0p01_p512     0.3 margin      +3980      -537      -616       +80        +41     +255  +0.31 +0.0274   4/8        +12     +347  +0.23 +0.0202   3/4     1/16
s0p01_p512     0.1 obj_w    +0.64928  +0.00164  -0.01959  +0.02123   -0.00420 +0.00576  +3.68 +0.3230   8/8   +0.00299 +0.00365  +5.82 +0.5102   4/4    14/16
s0p01_p512     0.1 win_w    +0.63333  +0.03333  +0.00000  +0.03333   +0.00000 +0.00000   +nan    +nan   8/8   +0.00000 +0.00000   +nan    +nan   4/4    16/16
s0p01_p512     0.1 margin      +3980      -189      -561      +372       -141     +168  +2.21 +0.1939   8/8       +136     +120  +3.11 +0.2724   4/4     3/16
s0p01_p512    0.03 obj_w    +0.64928  -0.00658  -0.00011  -0.00648   +0.00039 +0.00074  -8.72 -0.7649   0/8   +0.00029 +0.00064 -10.11 -0.8870   0/4     0/16
s0p01_p512    0.03 win_w    +0.63333  +0.00000  +0.00000  +0.00000   +0.00000 +0.00000   +nan    +nan   0/8   +0.00000 +0.00000   +nan    +nan   0/4     0/16
s0p01_p512    0.03 margin      +3980      -347       -21      -326         +5      +10 -34.29 -3.0077   0/8         +3       +7 -44.31 -3.8859   0/4     0/16
```

## VERDICT: **NO-GO** on the pre-registered bar

The rule needs, at SOME α ≤ 0.1 on the HELD-OUT block, all three of
(1) `+α·d` gains on **both** `obj_w` and `margin`, (2) `a>r ≥ 6/8`,
(3) `a>p = 4/4`.

| held-out α | (1) obj_w | (1) margin | (2) a>r | (3) a>p | pass? |
|---|---|---|---|---|---|
| **0.1** (= 1 σ-perturbation) | **+0.00164** ✅ | **−189** ❌ | 8/8 ✅ | 4/4 ✅ | **NO** — (1) fails on margin |
| **0.03** (= 0.3 σ-perturbations) | −0.00658 ❌ | −347 ❌ | 0/8 ❌ | 0/4 ❌ | **NO** |
| 0.3 (diagnostic) | −0.01406 | −537 | 5/8, 4/8 | 3/4 | no |
| 1.0 (diagnostic, the cliff) | −0.10983 | −3463 | 0/8 | 0/4 | no |

So: **NO-GO. flow208 is not authorised by this test.** Clause 5 of the
pre-registration (replication at EPS_SEED 9002) is moot — it gates a PASS, and
there is no PASS to gate; a second seed cannot convert a failed (1).

### κ against the pre-registered floor (κ ≤ 0.015 at α ≤ 0.1 = NO-GO)

| block | α | κ(obj_w) | κ(win_w) | κ(margin) |
|---|---|---|---|---|
| HELD-OUT | 1.0 | −0.7634 | +0.2481 | −0.9092 |
| HELD-OUT | 0.3 | +0.0215 | 0.0000 | +0.0274 |
| **HELD-OUT** | **0.1** | **+0.3230** | n/a (r_sd 0) | **+0.1939** |
| HELD-OUT | 0.03 | −0.7649 | n/a | −3.0077 |
| IN-SAMPLE | 0.1 | +0.1684 | +0.2064 | +0.3428 |
| IN-SAMPLE | 0.03 | +3.1533 | n/a | +14.6928 |

The κ clause is **cleared by a wide margin at α 0.1** (+0.32 and +0.19 vs a
floor of 0.015) — but κ was written as a NO-GO-*if*, not a PASS-*if*, and the
E3c conditions are the binding ones. Two readings of κ here need care:

- κ = z/√n_live and n_live is 130, not 5,997, so the same κ is ~6.8× easier to
  reach here than in the dither run. The comparable quantity across blocks is
  **z**: +3.68 (obj_w) and +2.21 (margin) at α 0.1 held-out.
- The α 0.03 κ's (±3, ±14) are **artefacts**: the random controls are
  decode-inert at ‖step‖ 0.0342 (`r_sd` 0.0002 / 2 coins), so z divides by
  almost zero. Do not read them as signal.

## What the reading actually says

1. **The block is not dead, and it is not dither.** At α 0.1 the antisymmetric
   statistic is positive on all three metrics and beats **8/8 randoms and 4/4
   permuted-advantage controls** on `obj_w`, `win_w` and `margin`,
   held-out. The dither remedy at its own α 0.1 managed 6/8 and 2/4 with
   κ −0.0009. This is the first block at B whose one-step direction beats the
   permuted control on the hold-out.
2. **But the antisymmetry is carried by `−d`, not by `+d`.** At α 0.1
   held-out, `+d` is +0.00164 obj_w / −189 margin (i.e. flat), while `−d` is
   −0.01959 / −561. The direction identifies a way to get *worse*; it does not
   yet buy anything. That is exactly what condition (1) exists to refuse.
3. **The sign flips with step length, which is the cliff signature again.**
   Held-out `+d`: −0.0066 at 0.03, +0.0016 at 0.1, −0.0141 at 0.3, −0.1098 at
   1.0. A smooth descent direction does not change sign twice over one decade
   of step length.
4. **In-sample → held-out leak at the smallest live step.** At α 0.03 in-sample
   `+d` gains on everything (+0.00356 obj_w, +64 margin, 8/8, 4/4) while
   held-out `+d` loses on everything (−0.00658, −347, 0/8, 0/4). 512 members on
   130 dimensions still overfits the training block.
5. **The ES direction is ~30× more "decode-active" per unit norm than an
   isotropic one.** At α 0.03 the eight random directions move the held-out
   objective by `r_sd 0.00074` while `d` moves it by 0.0066 — `d` concentrates
   on the coordinates whose `round(8·z)` is near a boundary. The block is
   genuinely reachable by the ES; the problem is the sign of what it reaches.
6. **Where flow208's own first step would land.** `‖g‖ = 23.68`, and the
   staged arm is `--lr 2e-3 --optimizer sgd`, so its first step is
   `0.047 = 0.41 ×` the α 0.1 step measured here — between the α 0.03 row
   (held-out −0.0066, 0/8) and the α 0.1 row (flat). The arm would open inside
   the band this test says is flat-to-negative on held-out boards.

## Recommendation

Do not launch flow208 ahead of the queue on the strength of the gene being
expressible. The one-step screen says the lots direction at B is *measurable*
(8/8 and 4/4, unlike every previous block) but **not yet profitable**: `+d`
does not buy a held-out coin at any step length, and the in-sample gain at the
smallest live step does not transfer.

Two cheap follow-ons are better value than the arm, in this order:

1. **Re-read at pop 2048 on the same 130 dimensions** (d/pop = 0.06). The
   estimator's disjoint cosine is P/(P+d); at d = 130 the population is already
   4× the dimension, so if the direction is still `+d`-flat at pop 2048 the
   block's gradient is genuinely flat at B, not under-sampled. One cell, ~35 min.
2. **The same test with the block seeded away from zero.** Every reading here
   is taken at `lots = 0`, where `round(8·z)` is a *rounding boundary for every
   product at once*: half the block's local geometry is the discreteness of the
   decode, not the sell side. A centre at a small random non-zero lots block
   (or after 20 generations of flow208) is a different, fairer question.

Nothing in this report says the sell interface is the wrong bottleneck; it says
the one-step gradient of this parameterisation of it, at B, at σ 0.01, pop 512,
does not pay on held-out boards.

## The EPS_SEED 9002 replicate (run anyway) — it hardens the NO-GO

Started 20:57Z, finished 21:23Z, same rig, only the perturbation seed changed
(`S/lots/sweep_lots9002.txt`, `S/lots/run_onestep_lots9002.log`). Draw:
`||g|| 24.5770  off-mask ||g|| 0.00e+00  win 0.7319`.

The pre-registration makes 9002 *confirmatory*: it gates a PASS at 9001, and
9001 did not pass, so the verdict does not depend on it. It is reported because
it answers a different question — is the α-ladder reading seed-stable?

| held-out | metric | seed 9001 `+d` | seed 9002 `+d` | agree? |
|---|---|---|---|---|
| α 0.1 | obj_w | +0.00164 (8/8, 4/4) | +0.00308 (8/8, **3/4**) | yes on sign, (3) fails on 9002 |
| α 0.1 | margin | **−189** (8/8, 4/4) | **−161** (8/8, 4/4) | yes — **(1) fails on both seeds** |
| α 0.03 | obj_w | **−0.00658** (0/8, 0/4) | **+0.00347** (8/8, 4/4) | **NO — opposite sign** |
| α 0.03 | margin | **−347** (0/8, 0/4) | **+57** (8/8, 4/4) | **NO — opposite sign** |
| α 0.3 | obj_w | −0.01406 | −0.02353 | yes (both lose) |
| α 1.0 | obj_w | −0.10983 | −0.10871 | yes (the cliff, both seeds) |

Read it in order:

- **The verdict alpha is stable and it is a fail.** At α 0.1 (one
  σ-perturbation) both seeds put `+d` flat-to-positive on `obj_w` and
  **negative on margin**. Condition (1) fails twice, the same way. On 9002 the
  permuted control also catches `obj_w` (3/4), so (3) fails too.
- **The α 0.03 row is a coin flip.** Seed 9001: −0.0066 / −347, beaten by
  every control (0/8, 0/4). Seed 9002: +0.0035 / +57, beating every control
  (8/8, 4/4). Same centre, same block, same α — opposite sign and opposite
  verdict. Taken alone the 9002 α 0.03 row satisfies all three E3c clauses;
  that is precisely why the pre-registration demands two seeds, and why this
  reading is **not** a pass. Note also that its control null is nearly
  degenerate there (`r_sd` 0.00067 obj_w / 10 coins; `p_sd` 0.00005): at
  ‖step‖ 0.0342 the *random* directions barely move the decode, so "8/8" is
  beating an almost-zero null.
- **The in-sample side flips too** at α 0.03 (9001 +0.00356, 9002 −0.00150),
  while α 0.1 in-sample agrees on both seeds (+0.0018 / +0.0026 obj_w,
  +124 / +113 margin, 8/8, 4/4). The block's *training* gradient at one
  perturbation-norm is real and reproducible; what does not reproduce is any
  held-out coin.
- **Scale check on the centre itself.** The same B_pad centre scores
  `obj_w 0.64928 / margin 3980` in one run and `0.64797 / 3963` in the other
  (`win_w` identical). Build-to-build drift of ~0.0013 obj_w is *larger than
  the α 0.1 `+d` gains being adjudicated*. Within a run the comparison is
  CRN-paired and therefore still valid — but nothing at this effect size
  survives being carried between builds, which is one more reason not to spend
  a 30,000-generation arm on it.

**Verdict unchanged: NO-GO.** The lots direction at B is measurable (it beats
the permuted control on the hold-out at α 0.1, which no block has done here
before) and it is not profitable (it never buys both `obj_w` and `margin` at a
step ≤ one perturbation, on either seed).
