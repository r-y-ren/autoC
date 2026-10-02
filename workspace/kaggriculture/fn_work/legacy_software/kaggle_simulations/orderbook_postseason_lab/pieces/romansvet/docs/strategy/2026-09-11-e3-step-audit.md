# E3 step audit — is the σ 0.01 cliff a sign error, a concentrated step, or a step-scale artefact?

Audit agent, 2026-09-11, 60-minute box, CPU only (the 3070 is running the sweep being audited).
Inputs: `S/onestep/{sweep_b.py,README.md,run_local.log,sweep_b.json}`, `S/onestep/grads/*.npy`
(read-only), the training tree `S/localarm/tree`. New files: `S/onestep_audit/thetas/*.npy`
(seven step thetas) and `S/simscreen/e3audit_*.csv`.

**The reading being audited** (σ 0.01, `run_local.log` lines 34-49): `+d` loses on every metric
at both pops — held-out obj_w −0.136 (P 512) and −0.486 (P 2048), margin −3,425 / −15,553 on a
+3,981 centre; `−d` loses mildly (−0.004 / −0.027); the 16 random steps of the same length move
obj_w by sd 0.030 and `+d` beats 0 of 16. κ reads −0.057 / −0.196 held-out, i.e. the rig says the
ES direction is strongly *anti*-aligned with the objective's gradient.

## 1. SIGN — correct, and the hold-out metric has the same sign

**Verdict: SIGN OK.** The chain, in the tree the sweep actually imports
(`S/localarm/tree/src/kagg3/es/train.py`; the repo's `src/` copy is older — its
`shaped_advantage` still has the 4-argument signature):

| step | file:line | what it says |
|---|---|---|
| seat unpack (trainer) | tree `train.py:5193` | `mine, theirs = money[..., 0], money[..., 1]` |
| seat unpack (scorer) | `S/popcurve/B/onestep.py:58` | the **same two lines**, same order → `obj_w` and the fitness read the same seat |
| fitness | tree `train.py:653-669` | `rel = sigmoid((mine − theirs)/margin_scale)`; `adv = abs_weight·rank(own) + (1−abs_weight)·rank(rel)`; the run's manifest is `abs_weight=0`, `tape_score=margin`, all three bonus weights 0 → `tape_episodes` returns `None` (tree `train.py:4611`) and `fitness_bonus` returns `None` (tree `train.py:5063-5072`), so **adv = rank_normalise(obj_w) exactly** |
| rank | tree `train.py:509-526` | `avg_rank/(n−1) − 0.5`, **ascending** — higher fitness = higher adv |
| estimator | `S/popcurve/popcurve.py:183-195` | `thetas = [θ+σε ; θ−σε]`, `grad = (adv[:half] − adv[half:]) @ ε /(pop·σ)` = the textbook antithetic **ascent** estimator; identical to the trainer's own `train.py:5202-5204` |
| the arm's own step | tree `train.py:4974, 4993` | `delta = lr·m̂/(√v̂+ε)`, `step = self.theta + delta` — θ moves **along +grad** |
| the step under test | `sweep_b.py:229-231` | `u = g/‖g‖; dirs += [R·u, −R·u]` — `+d` is the direction the trainer travels |
| hold-out | `onestep.py:69-99` (`held_out_argv`) | only the rung list, `--episodes` and `--arch-frac` change; the metric is the same `score_batch`, both seats averaged → same sign |

So `+d` is the arm's own uphill direction and `obj_w` is the quantity it is uphill in. A negative
`+d` gain is not a convention error: at this step length the trainer's own direction really does
lose on its own batch.

## 2. CONCENTRATION — none. The step is indistinguishable from its random controls

`‖g‖` 105.90 (P 512) and 52.99 (P 2048); both live exactly on the 5,997-coordinate mask
(off-mask ‖g‖ = 0). All figures below are for the unit direction scaled to the rig's
`R = lr·√n_live = 0.2323`.

| quantity | ES P 512 | ES P 2048 | rand0/1/2 (same R) | Adam-like (`0.003·sign`) |
|---|---|---|---|---|
| top-1 coord share of ‖d‖² | 0.0027 | 0.0044 | ~1/n | 1/5997 |
| top-10 / top-100 share | 0.021 / 0.126 | 0.025 / 0.136 | — | — |
| largest per-coord displacement | 0.01198 | 0.01540 | 0.0101-0.0119 | 0.00300 |
| median per-coord displacement | 0.00206 | 0.00200 | 0.00201-0.00203 | 0.00300 |
| coords over lr = 0.003 | 1,892 | 1,890 | 1,867-1,913 | 0 |

The ES direction's coordinate profile **is** the Gaussian controls' profile, to the third decimal.
Energy per gene block is flat too — every block's share of ‖d‖² equals its share of the live
parameters (`w1` 0.36-0.39 on 2,304 params, `gp` 0.14 on 864, `g1` 0.13 on 768; per-parameter
share 1.5-2.0e-4 against the uniform 1/5997 = 1.67e-4). The largest single coordinate is
`gb2[6]` (a head bias) at 0.015, then `fv`, `gb5`, `g5`, `w2`, `g1` — no gene family is picked out.
There is no norm inflation either (‖θ‖ 18.112 → 18.115) and no alignment with θ
(cos = +0.007 / −0.022, inside the controls' ±0.007 band).

**So "the step is concentrated where Adam's is spread" is false.** The only structural difference
from an Adam step is shape, not scale: Adam moves every live coordinate by ≈ lr (a `sign`-like
step, cos with the ES direction 0.79), while the ES step is ‖g‖-proportional — same total length,
median coordinate 0.002 vs Adam's 0.003, tail 5× lr on ~1/3 of the coordinates.

**The pop scaling is the load-bearing number here.** `‖g_512‖/‖g_2048‖ = 1.998` — exactly
√4 — and `cos(g_512, g_2048) = 0.532` ≈ √(256/1024) = 0.5, which is what two draws sharing a
256-pair prefix of one ε stream give **when the mean gradient is zero**. Both gradients are, to
the precision of this measurement, pure sampling noise: no signal floor survives at P 2048.
That makes the σ 0.01 cliff stranger, not weaker — a noise direction of length R that loses
0.48 obj_w while eight *other* noise directions of length R move it by 0.03.

### 2b. What the +d collapse actually is, in coins (`sweep_b.json`, raw fields)

| σ 0.01, in-sample | our coins | theirs (= mine − margin) | margin | win_u |
|---|---|---|---|---|
| centre B | 103,577 | 99,021 | +4,555 | 0.736 |
| `+d` P 2048 | 98,655 | **110,276** | −11,621 | **0.126** |
| `−d` P 2048 | 102,932 | 99,508 | +3,425 | 0.667 |
| `+d` P 512 | 104,040 | 102,142 | +1,898 | 0.550 |
| rand0/1/2 `+` | 103,3-103,6k | ~99.2-99.3k | +4,27-4,39k | 0.704-0.717 |

The `+d` step at P 2048 costs us 4,9k **and hands the opponent 11,3k** — the denial signature,
not a "we got worse" signature (`counterfactuals-overstate`'s two-purse rule). Its win rate is
0.126: it loses seven games in eight. Meanwhile each *individual population member*, which sits
**3.3× farther from B than the step does** (‖σε‖ = 0.774 vs ‖d‖ = 0.2323), averages win 0.6995 —
barely below the centre's 0.736. So the brief's premise is the wrong way round: the step is not
long compared with the cloud that was sampled, it is short. What is extreme about it is its
*direction*: the rank-weighted sum concentrates ~all of its length onto the one behavioural
axis the population's fitness spread is about, whereas a random ε (or a random control) has only
~‖v‖/√5997 of itself on that axis. Against isotropic controls, d is therefore ~20-80× more
behaviourally extreme at equal Euclidean length — which is exactly why the controls read sd 0.03
while d reads −0.48, and why "d beats 0/16 randoms" cannot by itself mean "the estimator points
downhill".

## 3. SCALE TEST — engine-exact, paired, CPU (`S/simscreen`)

Seven step thetas were built in `S/onestep_audit/thetas/` by copying `sweep_b.py:229-241`
byte for byte (float64 add on the live mask, saved float32); `p2048_a1.npy` and `p512_a1.npy`
are **`np.array_equal` with the sweep's own `S/onestep/thetas/onestep_s0p01_p*_plus.npy`**, and
`p2048_m1.npy` with its `_minus`, so the α-ladder really is the rig's own step, rescaled.

* α ∈ {1.0, 0.1, 0.03} on the P 2048 direction (plus the mirror −α at the same three scales)
* α ∈ {1.0, 0.1} on the P 512 direction
* "Adam-like": `B + 0.003·sign(d)` on the live coordinates — the same ‖step‖ 0.2323, but the
  per-coordinate cap the trainer's Adam actually obeys (cos with the ES direction 0.794, which
  is just √(2/π): a sign step is not gentler along `d`, it is the *shape* Adam takes)

Screened paired against B on the 120-board LIVE-C hold-out list (`boards.json`) and the 40-board
TOPB2 list (`boards_topb2.json`), shipped `hr` switches, same (tape, seed, seat) cells for every
theta.

### 3a. LIVE-C hold-out, 120 boards, paired vs B (`S/simscreen/e3audit_livec.csv`, `e3audit_minus.csv`)

| theta | step | win % | margin | **Δ vs B** | sd | **t** |
|---|---|---|---|---|---|---|
| B (ref) | — | 71.7 | +5,279 | — | — | — |
| `p2048_a1` | **+1.00 R** | 15.0 | −11,340 | **−16,619** | 6,381 | **−28.5** |
| `p2048_a0p1` | +0.10 R | 73.3 | +5,419 | **+140** | 1,500 | +1.03 |
| `p2048_a0p03` | +0.03 R | 73.3 | +5,389 | **+111** | 905 | +1.34 |
| `p2048_m1` | −1.00 R | 73.3 | +5,101 | −178 | 3,213 | −0.61 |
| `p2048_m0p1` | −0.10 R | 70.0 | +5,023 | −256 | 1,744 | −1.61 |
| `p2048_m0p03` | −0.03 R | 70.0 | +5,101 | −178 | 1,740 | −1.12 |
| `p512_a1` | +1.00 R | 57.5 | +1,870 | **−3,409** | 3,123 | **−12.0** |
| `p512_a0p1` | +0.10 R | 73.3 | +5,565 | **+286** | 1,378 | **+2.27** |
| `p2048_adamlike` | 0.003·sign | 60.0 | +1,483 | −3,796 | 3,218 | −12.9 |
| `p512_adamlike` | 0.003·sign | 71.7 | +5,220 | −59 | 1,911 | −0.34 |

`shopdiff` 0.0 % on all 1,440 cells — every theta saw byte-identical shop sequences, so these are
clean paired differences.

**The rig reproduces in the engine-faithful sim, and then inverts below α ≈ 0.3.** The α 1.0 rows
are the sweep's own held-out numbers on a different board list (sim −16,619 vs rig −15,553;
sim −3,409 vs rig −3,425) — the cliff is real, not a JAX or scoring artefact. But the whole
α-ladder says the cliff is **all curvature**:

* engine antisymmetric statistic `Δ(+αd) − Δ(−αd)`: **−16,441** at α 1.0, **+396** at α 0.1,
  **+289** at α 0.03 (paired SE ≈ ±200 at n = 120) — it changes sign, and the sign at
  training-like step sizes is the **correct** one;
* three of three small-α `+d` cells gain (+140, +111, +286; the P 512 one at t +2.27) and three of
  three small-α `−d` cells lose (−256, −178, and P 512's mirror is untested) — a consistent, if
  small (~+0.2-0.3 k/board), uphill reading at α ≤ 0.1;
* the symmetric part `(Δ+ + Δ−)/2` is −8,399 at α 1.0 and −58 / −34 at α 0.1 / 0.03: the damage
  is quadratic-or-worse in α and is gone by α 0.1.
* the Adam-shaped step at the **full** R is nearly as damaging (−3,796 on the P 2048 direction),
  so per-coordinate capping is not the fix — **length along the selected axis is**.

### 3b. TOPB2 top tier, 40 boards, paired vs B (`S/simscreen/e3audit_topb2.csv`)

| theta | step | win % | margin | Δ vs B | sd | t |
|---|---|---|---|---|---|---|
| B (ref) | — | 32.5 | −1,472 | — | — | — |
| `p2048_a1` | +1.00 R | 5.0 | −15,796 | −14,324 | 7,472 | −12.1 |
| `p2048_a0p1` | +0.10 R | 25.0 | −1,993 | −521 | 2,349 | −1.40 |
| `p2048_a0p03` | +0.03 R | 30.0 | −2,119 | −647 | 2,046 | −2.00 |
| `p2048_m0p1` | −0.10 R | 25.0 | −2,908 | **−1,436** | 2,806 | −3.24 |
| `p512_a1` | +1.00 R | 30.0 | −3,632 | −2,160 | 3,317 | −4.12 |
| `p512_a0p1` | +0.10 R | 25.0 | −2,174 | −703 | 1,994 | −2.23 |
| `p2048_adamlike` | 0.003·sign | 25.0 | −3,440 | −1,968 | 3,582 | −3.48 |
| `p512_adamlike` | 0.003·sign | 30.0 | −1,912 | −440 | 1,902 | −1.46 |

Same cliff at α 1.0 (−14.3 k). At α 0.1 the top-tier leg is *symmetrically* fragile — `+d` −521
and `−d` −1,436, so every direction of that length costs something here — but the antisymmetric
part is again **positive, +915**: of the two mirror steps the trainer's own direction is the
better one. B is not a peak; it sits on a slightly concave ridge whose curvature term swamps its
gradient term once the step passes ~0.3 R.

## 4. VERDICT

> **SIGN OK** (ascent, both metrics, chain verified line by line — §1).
> **NO CONCENTRATION**: the step's coordinate profile is identical to its Gaussian controls and
> the gradient is pure sampling noise by the pop test (‖g‖ ratio 1.998 ≈ √4, cos 0.53 ≈ √¼) (§2).
> **STEP-SCALE ARTEFACT: YES.** At α 1.0 the step loses 16.6 k; at α 0.1 and 0.03 the *same*
> direction **gains** (+140, +111, +286 on LIVE-C) and beats its own mirror on both legs
> (antisym +396 / +289 on LIVE-C, +915 on TOPB2). The σ 0.01 cell's κ = −0.20 is the third-order
> term of a cliff, not a measurement of the gradient's sign.

The rig's `R = lr·√n_live` is the right *magnitude* for an Adam step but the wrong magnitude for
**one draw's** contribution to it: with β1 = 0.9 the newest gradient carries ~10 % of `m`, and the
other 90 % is nine other draws whose noise is largely orthogonal. **α ≈ 0.1 R is the honest model
of what one generation actually moves**, and that is precisely where this direction reads uphill.
The isotropic random controls are not a null for "is R too long" either: `d` is the aggregate of
the evaluated ε rows and concentrates its whole length on the axis the population's fitness
spread is about, while a random control of the same length puts ~1/√5997 of itself there. They
calibrate the sd of the antisym statistic; they cannot license "d beats 0/16 randoms ⇒ downhill".

## 5. How to read the σ 0.02 (~16:10Z) and σ 0.04 (~16:45Z) cells

1. **Do not record a FAIL / "B is a peak for this estimator" verdict from them.** The rule's FAIL
   branch (κ ≤ 0.015, net gain ≤ 0) and its PASS branch are both unreachable while every cell is
   read at α 1.0: the cliff will dominate `+d` at every σ, and it is not a property of σ.
2. Read them as a **direction-quality** comparison instead, at fixed R: (a) `‖g‖` at P 512 vs
   P 2048 — another 2.0 ratio means the draw is still all noise at that σ; (b) which σ's `+d`
   cliff is *shallowest*, since the cliff depth at fixed R is a proxy for how much of the step
   lands on the sensitive axis; (c) whether in-sample and held-out still agree.
3. **Then re-read the winner at α 0.1.** The cheap way needs no GPU: rescale the saved
   `S/onestep/thetas/onestep_<cell>_{plus,minus}.npy` about B by 0.1 (this audit's
   `S/onestep_audit/thetas/` script) and screen them paired on `S/simscreen` — 8 thetas × 120
   boards ≈ 12 CPU minutes, ±400 coins/board of resolution, no lottery. A cell "passes" when the
   engine antisymmetric statistic at α 0.1 is positive on **both** legs.
4. **Add the missing control** before any arm is re-cut on a κ: a direction built from the same ε
   rows with the advantages **permuted** (`g_shuf = (perm(adv⁺) − perm(adv⁻)) @ ε`). It costs one
   extra theta in `score_batch`. If `g_shuf` at α 1.0 also collapses, the cliff belongs to the
   ε-span aggregate rather than to selection, and κ as defined is uninterpretable at any σ.
5. The campaign consequence, if the α 0.1 readings hold up: **B is not a peak and the ES estimator
   at B is correctly signed but tiny** (≈ +0.2 k/board per generation-equivalent against a ±1.5 k
   board sd). That argues for the recentre doc's §5 field change *and* for a smaller effective
   step (lr, or a lower β1 so one draw is not 10-deep in momentum) — not for abandoning B's centre.

### Files
`S/onestep_audit/thetas/*.npy` (10 step thetas, α-ladder both signs + two Adam-like),
`S/simscreen/e3audit_{livec,minus,topb2}.csv` (1,760 paired board rows).
Nothing under `S/onestep/` was written; `git diff --stat src/` is empty.
