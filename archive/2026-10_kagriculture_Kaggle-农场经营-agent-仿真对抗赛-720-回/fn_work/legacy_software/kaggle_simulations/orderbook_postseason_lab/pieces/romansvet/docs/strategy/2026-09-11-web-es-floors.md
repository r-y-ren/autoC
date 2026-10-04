# What the literature does about floors between theta and a black-box simulator

2026-09-11, web research only (no training, no locks, nothing under `src/`).
Reads: `docs/strategy/2026-09-11-tie-census.md`, consensus §59–§69.
Our numbers, held fixed throughout: 6,789 theta, antithetic Gaussian σ 0.02, pop 512,
rank-normalised `sigmoid(margin/3000)`, Adam lr 0.003, CRN on ~200 boards; 68
discretisations per `decide`, 46 inside σ, 33.9/55 floor cells and 27.4/42 `Macro`
integers crossed per member, **0/64 members decode B's plan**, ~60 decisions/game ⇒ ~10³
cell draws behind one fitness number.

---

## 0. The headline: the literature's failure mode is the MIRROR IMAGE of ours

Every mixed-integer ES paper is about σ being **too small** relative to the
discretisation granularity: the sampled standard deviation of an integer coordinate falls
below one grid step, every member decodes the same integer, the objective is a plateau,
and the step size shrinks further ("stagnation" — Hansen 2011; Hamano et al. 2022). The
fixes are all **lower bounds**: integer mutation, a floor on the marginal flip
probability, σ_LB.

We are at the other end. Our σ is **too large**: 46 of 68 ties sit inside one σ, so a
member does not decode a nearby plan, it decodes a **fresh random plan**. The paper that
names this regime is the 2026 convergence analysis:

> Hamano, Uchida, Shirakawa, *Convergence Analysis of Evolution Strategies for
> Mixed-Integer Optimization*, arXiv:2605.21000 (2026).
> (1+1)-**LB**-ES — lower bound only — still stalls as the integer dimension `d_in` grows,
> because the probability that a mutation lands the integers correctly is
> `p_succ = (1 − p_mut)^{d_in}`, exponentially small in the number of integer coordinates.
> Linear convergence `Θ(d_co·log(1/ε))` is recovered only by **(1+1)-LUB-ES**, which adds
> an **upper** bound on σ⟨D⟩, under `s > 2/p_succ`.

Read against our census: `p_mut` ≈ 0.8 (27.4 of 42 `Macro` integers flip) and `d_in` = 42
per decision × ~60 decisions ⇒ `p_succ` ≈ 0 to any precision we can measure. **0/64 is
the prediction, not a surprise.** The generic prescription for us is therefore an
**upper** bound on the per-tie step, not a lower one — and because 68 ties with gradient
norms spanning 2.18 … 1,803 cannot share one isotropic σ, the upper bound has to be
**per-block/anisotropic**.

The right step-size variable is not `‖σε‖` (1.65) and not lr; it is the **expected number
of cells crossed**, which the census already lets us compute in closed form:

    E[cells] = Σ_j 2·Φ( −r_j / σ_j ),   r_j = gap_j / ‖∇_j‖   (the census radius)

At σ 0.02 this sums to ≈ 34 per decision (measured 33.9 — the formula is validated). A
usable ES wants **E[cells] ≈ 1–3**.

---

## 1. Mixed-integer CMA-ES and integer handling

**Hansen, *A CMA-ES for Mixed-Integer Nonlinear Optimization*, INRIA RR-7751 (2011)**
(https://inria.hal.science/inria-00629689). Integer coordinates whose sampled standard
deviation falls below the discretisation granularity receive an *additional integer
mutation*; that mutation updates the **mean only** and is excluded from the covariance and
step-size updates, and those coordinates are dropped from the global step-size update
altogether so the step size does not fluctuate randomly. Modern `pycma` supersedes it with
a concise lower bound on the variances plus "integer centering"
(`cma.integer_centering.centering_on`, `{'integer_variables': [...]}`; the sampled integer
coordinates are rounded at the end of `ask`).

**Hamano, Saito, Nomura, Shirakawa, *CMA-ES with Margin: Lower-Bounding Marginal
Probability for Mixed-Integer Black-Box Optimization*, GECCO '22 / arXiv:2205.13482.**
Keeps each integer variable's **marginal probability of taking a different value** above a
margin **α = 1/(N·λ)** by correcting the mean `m` and the diagonal `A` in
`v_i = m + σ·A·y_i` (affine invariance preserved). Extended to single/multi-objective in
ACM TELO (2024), doi 10.1145/3632962, and to categorical variables in *CatCMA with
Margin*, arXiv:2504.07884 (2025). Simpler PPSN XVIII variants exist (LB+IC-CMA-ES,
doi 10.1007/978-3-031-70068-2_18, 2024).

**Native-integer ES.** Rudolph, *An evolutionary algorithm for integer programming*,
PPSN III (1994): the **double-geometric** distribution is the maximum-entropy mutation on
ℤ. Revived as **INES** — de Nobel, Vermetten, Wang, Shir, Emmerich, Bäck,
*Integer Natural Evolution Strategies*, arXiv:2608.23714 (2026): coordinate-wise expected
absolute step sizes `δ_i = E|Z_i|` updated by a Fisher-scaled natural gradient, motivated
precisely by the fact that *"vectors lying on the same ℓ₂ shell can correspond, after
rounding, to a large range of different effective ℓ₁ mutation lengths"* — our 2,000×
gradient spread, exactly. Also Shir et al., *Correlated Geometric Mutations for Integer
Evolution Strategies*, GECCO '25 / arXiv:2506.22526.

**Does it apply to a shipped deterministic integer policy?** Partly. All of this machinery
assumes a **1:1 coordinate → integer** map, so the margin can be imposed per coordinate.
Ours is 6,789 continuous genes → 42 integers **per decision** through a nonlinear head,
many-to-many, with the integers themselves board-dependent (`n_dev` is a share of
`n_free`). The *mechanism* transfers (control the per-integer flip probability); the
*implementation* does not (we cannot address an integer by coordinate index).

**Recommendation (trainer).** Replace the scalar σ with a **per-block σ vector chosen so
the flip budget is met**: precondition theta by the decode jacobian (`S/ties/census.py`
already produces `‖∇_j‖` per tie and `jacrev` gives the block attribution), i.e. whiten so
the coin-scaled heads with `‖∇‖` 1,196–1,803 do not eat the entire budget while `compact`
(`‖∇‖` 2.18) never moves. Then solve `Σ_j 2Φ(−r_j/σ_j) = 2`. This is CMA's diagonal `A`
and pycma's integer centering, hand-built for our decode.
**Expected effect:** members decode plans within 1–3 integers of B's, which is the
precondition for any gradient at all; `p_succ` climbs from ~0 to O(1).
**Risk:** at that σ we are close to the α 0.03 shell that §62 measured as *behaviourally
B* (0–2 flips, Δ ≈ 0). If the whitened solve also lands at Δ ≈ 0, the honest conclusion is
that **no σ makes this objective both smooth and informative**, and §6 (direct integer
search) is the only route. That is a valuable falsification and costs one CPU hour.

---

## 2. Stochastic rounding / dithering — the smoothing that still ships a hard floor

**What it is.** Round `z` down with probability `⌈z⌉ − z` and up with probability
`z − ⌊z⌋`; equivalently **non-subtractive dither**: add `u ~ U(0,1)` and floor. Classical
theory: Lipshitz, Wannamaker, Vanderkooy, *Quantization and Dither: A Theoretical Survey*,
J. Audio Eng. Soc. 40(5), 355–375 (1992)
(https://hajim.rochester.edu/ece/sites/zduan/teaching/ece472/reading/Lipshitz_1992.pdf);
Wannamaker, Lipshitz, Vanderkooy, Wright, *A Theory of Non-Subtractive Dither*, IEEE Trans.
Signal Processing 48(2) (2000). The theorem that matters: with an RPDF dither the
**expected output is an exact affine function of the input** and the error's first moment
is input-independent — `E_u[⌊x + u⌋] = x` exactly. The staircase becomes a **ramp**, with
no approximation and no temperature parameter.

**Modern instance.** Kwun et al., *LOTION: Smoothing the Optimization Landscape for
Quantized Training*, arXiv:2510.08757 (2025): train on the **expectation of the quantized
loss under unbiased randomized rounding**, which is differentiable a.e.; their Lemma 2
shows the global minima of the smoothed loss coincide with those of the hard-quantized
loss, because a point already on the grid has rounding probability 1. QSGD (Alistarh et
al., NeurIPS 2017) is the same unbiasedness argument for gradient compression.

**Does it apply to a shipped deterministic integer policy? YES — and it is NOT the
soft decode we rejected in §67.** The three rejection reasons do not bite:
1. *"ES is gradient-free"* — irrelevant here; dithering does not need a backward pass, it
   changes what the **forward** fitness measures.
2. *"It cannot play"* — a dithered decode **does** play: `⌊x+u⌋` is an integer, the engine
   takes it, 10.76 tiles becomes 10 or 11 with the right frequencies, never 10.76.
3. *"sim-equals-engine"* — `decide` stays one arithmetic program; the only addition is an
   RNG stream, and with `u ≡ 0` the graph is bit-identical to today's floor (the same
   inert-when-unset discipline as `KAGG3_PIN_INTS`).

The **train/deploy gap** is real but small and one-sided: training optimises the mean of a
±1-jittered policy, deployment plays the floor. Two mitigations, both free: (a) use
`u ~ U(0,1)` with `⌊x+u⌋` so the *expected* decode equals the real-valued decode (our
deterministic `⌊x⌋` is then the `u→0` draw, i.e. the shipped policy is one member of the
training mixture, not outside it); (b) our existing promotion rule already replays every
candidate **undithered** on TOPB2/LIVE-C/LIVE62, so a theta that only wins jittered never
ships. LOTION's Lemma-2 argument says a theta sitting mid-cell is not a fixed point of the
dithered objective, which is a feature: the smoothed optimum is pushed *toward* grid
points, i.e. toward margins, which is precisely the "recentre B off the knife edge" that
§66 refuted by hand.

**Implementation caveats, both load-bearing:**
- **Share the dither across the antithetic pair.** `u` must be a *common random number*
  keyed by (board, seat, day, tie) and identical for `+ε` and `−ε`, or the dither becomes
  fresh evaluation noise and the pairing that CRN buys us is destroyed. Same discipline as
  the shop-draw seed.
- **`_largest_remainder` must be dithered as a block.** `plant_target` sums to
  `n_dev − Σ animal_want`; dithering its five floors independently breaks the sum. The
  standard unbiased-and-sum-preserving replacement is randomised/systematic apportionment
  (one `U(0,1)` offset applied to the cumulative shares) — unbiased per component,
  total exactly preserved. The 8 `argsort` rank keys have the same fix via Gumbel noise on
  the keys (§5). The 5 `absorb` tanh thresholds dither with logistic noise.

**Recommendation:** this is the **cheapest high-value change in the whole report** — a
~5-line shim in the same `brain.decide` wrapper that `S/ties/brain.patch` already builds,
env-gated (`KAGG3_DITHER=<seed>`, unset = today's graph exactly).

---

## 3. Gaussian smoothing: when is `E_ε F(θ+σε)` smooth enough, and at what population

**Nesterov & Spokoiny, *Random Gradient-Free Minimization of Convex Functions*,
Foundations of Computational Mathematics 17:527–566 (2017)** (preprint CORE 2011/1). The
Gaussian-smoothed `f_σ(x) = E_ε f(x+σε)` is smooth even when `f` is not, and zeroth-order
schemes need **~n times more iterations** than gradient methods (`n` = dimension), with
accelerated `O(n²/k²)` for smooth problems and `O(n/√k)` for the stochastic case. At
n = 6,789 the dimension factor alone is ~7·10³ generations before any noise is counted.

**Berahas, Cao, Choromanski, Scheinberg, *A Theoretical and Empirical Comparison of
Gradient Approximations in Derivative-Free Optimization*, FoCM 22:507–560 (2022),
arXiv:1905.01332.** Gives explicit bounds on **the number of samples and the sampling
radius** needed for finite differences / linear interpolation / Gaussian smoothing /
sphere smoothing to satisfy a common accuracy condition guaranteeing descent — and, for
the random schemes, only *with some probability* each iteration. The operative content for
us: the required radius grows with the noise floor `ε_f`, and our `ε_f` is **not
measurement noise** — it is the ±25k shop re-roll plus the ~10³ cell draws, i.e. the same
order as the signal. Where the noise is that large the condition is unsatisfiable at any
affordable sample count.

**Salimans, Ho, Chen, Sidor, Sutskever, *Evolution Strategies as a Scalable Alternative to
RL*, arXiv:1703.03864 (2017)**; **Lehman, Chen, Clune, Stanley, *ES Is More Than Just a
Traditional Finite-Difference Approximator*, arXiv:1712.06568 (2018)**; **Raisbeck et al.,
*Evolution Strategies Converges to Finite Differences*, arXiv:2001.01684 (2020)** (the
two gradients converge as dimension grows — at n = 6,789 we are firmly in the FD regime,
so no "ES optimises robustness" defence is available). Lehman's point still bites the
other way: at large σ ES optimises **the distribution**, i.e. it rewards theta whose
*entire ±1-integer-jittered neighbourhood* plays well. That is not what we ship, and it is
a second, independent statement of the §59 gap.

**The variance statement to record for our case.** Model one tie as
`F(θ+σε) = F₀ + Δ_j·1[∇_j·σε > gap_j]`. The antithetic estimator's signal about tie `j`
is `∝ Δ_j·φ(r_j/σ)`, while `K` simultaneously-flipping ties each contribute an
independent `Δ` to the *variance*. So

    SNR per generation  ~  |Δ| / ( sd_board · sqrt(K) ) · sqrt(P)
    P_required          ~  K · (sd_board/|Δ|)²

With `K ≈ 34` per decision and ~60 decisions per game (≈ 2·10³ independent cell draws),
`Δ` per tie of order a few hundred coins and `sd_board` ≈ 2,500–3,000 (our own judge
tables), P_required is **3–4 orders of magnitude above 512**. This is the quantitative
form of the observed κ 0.004–0.011 and of the "pop 512 vs 2048 agree like two halves of
zero-mean noise" reading in §60. *Lowering K is the only lever with the right exponent* —
which is §1 (flip budget) and §2 (dither, which removes the discontinuity so `Δ_j` per
crossing shrinks to the marginal coin value instead of a whole strategy change).

**Budget allocation.** Wang & Lu, *Depth over Fidelity in Fixed-Budget Noisy Evolution
Strategies*, arXiv:2606.06555 (2026): under a fixed budget `T ≈ B/(λ + E[K_t])`, spending
evaluations on **more generations** normally beats spending them on reevaluation — *except*
above a misranking threshold (their single-crossing point ≈ 0.12), where denoising wins.
Our misranking rate is essentially 0.5 (0/64 members decode B's plan; records lose
in-sample, §59). **We are deep in the regime where the default advice inverts**: more
boards / tighter CRN / fewer generations, not more generations.

---

## 4. Rank shaping and mirrored sampling on a staircase

**Wierstra, Schaul, Glasmachers, Sun, Peters, Schmidhuber, *Natural Evolution Strategies*,
JMLR 15:949–980 (2014), arXiv:1106.4487** — rank-based fitness shaping makes the update
invariant under any monotone transform of fitness and robust to outliers.
**Brockhoff, Auger, Hansen, Arnold, Hohm, *Mirrored Sampling and Sequential Selection for
Evolution Strategies*, PPSN XI, LNCS 6238 (2010)** — mirrored (antithetic) pairs cancel the
even part of the perturbation and cut variance.

**On a staircase, rank shaping buys nothing.** Invariance to monotone transforms of the
fitness *scale* is not our problem; our fitness is a *random draw over integer plans*, and
ranking a noisy score just produces a noisy rank. Two concrete corollaries for our trainer:
- `sigmoid(margin/3000)` **followed by** rank normalisation is a no-op (the sigmoid is
  monotone, the ranks are unchanged). It is neither helping nor hurting — but it means the
  "fitness shaping" knob in our recipe has zero degrees of freedom, and any hope pinned on
  re-shaping it should be dropped.
- Mirrored sampling *does* carry exactly the information we want, but only in a form we
  are currently averaging away. For a tie of radius `r < σ`, the pair `±ε` **straddles the
  wall**, so `F(+ε) − F(−ε)` is a clean paired read of *that tie's* Δ. Our E3b already saw
  this: 14 of 56 step thetas move 100 % of boards, the same 14 on disjoint tape families.
  **Recommendation:** stop projecting the pairs onto a 6,789-vector and instead attribute
  each pair to the ties it straddles (the census shim records them), estimating **68
  scalars** with paired t-tests instead of 6,789 gradient coordinates. That is a ~4,000×
  reduction in the number of estimated quantities at fixed sample count, and it turns the
  ES into the bandit of §6.

---

## 5. Quantisation-aware training and argmax policies: sample in training, greedy at deploy

**Bengio, Léonard, Courville, *Estimating or Propagating Gradients Through Stochastic
Neurons*, arXiv:1308.3432 (2013)** — the straight-through estimator: hard in the forward
pass, identity in the backward. **Jang, Gu, Poole, *Categorical Reparameterization with
Gumbel-Softmax*, ICLR 2017, arXiv:1611.01144** and **Maddison, Mnih, Teh, *The Concrete
Distribution*, ICLR 2017, arXiv:1611.00712** — relax `argmax` to `softmax_τ(logits + G)`
with Gumbel noise `G`; **Straight-Through Gumbel-Softmax** takes the hard sample forward
and the soft gradient backward. **Fan et al., *Training Discrete Deep Generative Models
via Gapped Straight-Through Estimator*, arXiv:2206.07235 (2022)** quantifies the residual
forward/backward gap; decoupled-temperature variants trade bias against fidelity.

**How do they avoid the plateau?** By making the *training* policy stochastic — the action
is **sampled**, so the expected return is a smooth function of the logits — and taking
`argmax` only at deployment. RL does this by default (categorical policy trained, mode
played at inference); the accepted train/deploy gap is measured empirically, never argued
away. **Chrabaszcz, Loshchilov, Hutter, *Back to Basics: Benchmarking Canonical Evolution
Strategies for Playing Atari*, IJCAI 2018, arXiv:1802.08842** is the existence proof that
plain ES *can* train a pure-argmax discrete policy — but note the scale: **one** argmax
over ≤18 actions per frame, with the smoothing supplied by environment variety. We flip
~27 integers per decision on 42 fields; that is two to three orders of magnitude more
discreteness per fitness sample.

**Does it apply to us?** The STE half does **not** (§67's reason 1 stands: ES never runs a
backward pass). The **sampling half does, and is exactly §2**: "sample the discrete choice
during training, play the mode at deployment" *is* stochastic rounding of the decode, and
the Gumbel machinery is the right tool for the 8 `argsort` keys specifically — adding
i.i.d. Gumbel noise to the rank keys makes the allocation order a Plackett–Luce sample
whose expectation is smooth in the keys, while still producing a hard permutation the
planner can execute.

**Recommendation:** treat `S/ties/brain.patch`'s wrapper as the single place where all
three noise types enter — `U(0,1)` before the 55 floors, Gumbel on the 8 argsort keys,
logistic on the 5 `absorb` thresholds — all keyed by one CRN stream and all inert when the
env var is unset. **Risk:** a policy that is stochastic in the ordering of the plant/animal
allocation may be genuinely worse than B's deterministic order; watch the undithered
replay, and if the dithered-at-B fitness is materially below B's own, reduce the dither to
the floors only.

---

## 6. Direct search over the integers — the alternative when the interface is small

Our coarse interface is **12 integers** (`plant_target[5]`, `animal_want[3]`,
`crew_target`, `compact`, `forward_days`, `land_bias`), the half where "one unit is a
different strategy". That is a small enough discrete design space to search directly, and
this is a mature, well-tooled area:

- **ParamILS** — Hutter, Hoos, Leyton-Brown, Stützle, *ParamILS: An Automatic Algorithm
  Configuration Framework*, JAIR 36:267–306 (2009): iterated local search over discrete
  parameter configurations with adaptive capping under noisy, instance-based evaluation.
- **F-Race / iterated F-race / irace** — Birattari, Stützle, Paquete, Varrentrapp (2002);
  Balaprakash, Birattari, Stützle (2007); **López-Ibáñez, Dubois-Lacoste, Pérez Cáceres,
  Stützle, Birattari, *The irace package: Iterated racing for automatic algorithm
  configuration*, Operations Research Perspectives 3:43–58 (2016)**
  (https://iridia.ulb.ac.be/irace/): race candidate configurations over *instances*,
  eliminate statistically-dominated ones early, resample the survivors. Our boards are
  instances and our paired seeds are CRN — the structure is already ours.
- **Successive halving / Hyperband** — Karnin, Koren, Somekh, ICML 2013; Jamieson &
  Talwalkar, AISTATS 2016; Li, Jamieson, DeSalvo, Rostamizadeh, Talwalkar, JMLR 18 (2018):
  uniform budget, keep the best `1/η`, repeat; exponentially more evaluations on the
  survivors. Directly implementable on `S/simscreen` (200 boards → 40 → engine leg).
- **Bayesian optimisation over integers** — **Garrido-Merchán & Hernández-Lobato, *Dealing
  with categorical and integer-valued variables in Bayesian Optimization with Gaussian
  processes*, Neurocomputing 380:20–35 (2020)**, arXiv:1706.03673: the naive fix (round the
  proposal before evaluation) misbehaves; instead **round inside the kernel**, so the model
  never distinguishes two inputs that evaluate identically. This is the sharpest
  third-party statement of our disease: *our ES spends its entire step budget moving theta
  inside a cell the objective cannot see.*

**Does it apply to a shipped deterministic integer policy?** Best of all six — it searches
the very object we ship. Its limit is that the 12 coarse fields are **board- and
day-conditional** (`n_dev` tracks `n_free`, `crew_target` is a sigmoid in the day), so the
arms must be *offsets/rules* applied to B's decode, not constants — which is exactly the
shape `KAGG3_PIN_INTS` already implements.

**Recommendation:** replace the pinned-mode ES with a **race over integer neighbours of
B**: 12 coarse fields × {−1, +1} = 24 arms, each an offset applied through the pin wrapper,
screened with CRN on 200 boards, successive-halving to the survivors, engine leg vs B.
Cost ≈ **one ES generation at pop 512**. Note this is what §63/§64/§68/§69 have been doing
by hand, one lever at a time, with hand-chosen arms — the change is to make it systematic
and statistically-gated rather than hand-directed.

---

## 7. Ranked top-3, and the cheapest experiment for each

### #1 — Dither the decode during fitness evaluation only; ship the plain floor
*(§2; Lipshitz–Wannamaker–Vanderkooy 1992; Kwun et al. 2025 arXiv:2510.08757; Jang 2017 /
Maddison 2017 for the argsort keys)*
The one change that attacks the mechanism (`E[F]` becomes piecewise-**linear** in the
decoded value instead of piecewise-constant) without changing what the engine plays, without
a backward pass, and without breaking sim-equals-engine.
**Cheapest experiment:** add `KAGG3_DITHER=<seed>` to the existing `S/ties/brain.patch`
wrapper — `⌊x⌋ → ⌊x + u⌋`, `u ~ U(0,1)` from a stream keyed by (board, seat, day, tie) and
**shared between `+d` and `−d`** — then re-run the already-staged `S/onestep_b` one-step
rig at B, σ ∈ {0.02, 0.005}, with the same pre-registered bar as the pinned test
(κ ≥ 0.03, antisymmetric `+d` win on both legs at α 0.1/0.03, `+d` beats ≥ 12/16 randoms).
Self-check first: `u ≡ 0` must reproduce B's csv **to the coin**. Cost: identical to the
pinned one-step test; ~2 h. **Expected:** κ rises by an order of magnitude if ties are the
binding constraint; a NO-GO here falsifies §67 as cleanly as the pinned test does.
**Risk:** the trained theta is optimal for a ±1-jittered policy — bounded by our existing
rule that every candidate replays undithered for the judge legs; and the
`_largest_remainder` sum invariant must be dithered as a block (randomised apportionment),
not per-floor.

### #2 — Make the flip budget the step size: anisotropic σ with an UPPER bound
*(§1; Hansen 2011 RR-7751; Hamano et al. GECCO '22 arXiv:2205.13482; Hamano/Uchida/
Shirakawa 2026 arXiv:2605.21000 — lower bound alone stalls, the upper bound is what
restores convergence; de Nobel et al. 2026 arXiv:2608.23714 on ℓ₂ shells ≠ ℓ₁ steps)*
Stop controlling `‖σε‖` and lr; control `E[cells] = Σ_j 2Φ(−r_j/σ_j)` at 1–3 per decision,
with a per-block σ that equalises radii across the 2,000× gradient spread.
**Cheapest experiment:** pure CPU, no training — extend `S/ties/census.py` to evaluate
`Σ_j 2Φ(−r_j/σ)` for a *diagonal* σ over the PO.SHAPES blocks, solve for the σ vector that
puts the budget at 2, verify against a fresh 64-draw count, then feed that σ to the
existing one-step rig. ~1 h. **Expected:** either a σ vector that gives members plans 1–3
integers from B's (then relaunch one arm at it) or the demonstration that such a σ is
already inside the α 0.03 "behaviourally B" shell — in which case **ES over this
parameterisation is closed** and #3 becomes the programme.
**Risk:** the census radii are measured at one obs on a day-0 board; 3,241 genes are dead
there and wake on a planted board, so the σ solve must be re-run over the day × board panel
(§7 step 0 of the tie census) before any launch.

### #3 — Race the 12 coarse integers directly instead of training them
*(§6; Hutter et al. JAIR 2009 ParamILS; López-Ibáñez et al. ORP 3:43–58 2016 irace;
Jamieson & Talwalkar AISTATS 2016 / Li et al. JMLR 18 2018 successive halving;
Garrido-Merchán & Hernández-Lobato Neurocomputing 380:20–35 2020 — round inside the model,
never search inside a cell)*
The coarse half is a 12-dimensional integer design; ES is the wrong instrument for it, and
`KAGG3_PIN_INTS` already gives us the handle to set it.
**Cheapest experiment:** 24 arms (12 fields × ±1, as offsets through the pin wrapper),
CRN-screened on the 200 training boards, successive halving 200 → 40 → engine leg vs B,
with the two-purse displacement check we apply to every planner lever. Cost ≈ one ES
generation at pop 512. **Expected:** a direct, statistically-gated read on whether any
single coarse integer at B is on the wrong side — the same question §63–§66 answered by
hand for one tie, asked of all 12 at once. **Risk:** 24 paired screens is 24 chances to
find a false positive; pre-register the engine-leg bar (flips, not margin) and apply a
Holm correction over the 24 before promoting anything.

---

## 8. What the literature does NOT support

- **Rank shaping / mirrored sampling as a fix.** Both are variance tools, neither creates
  signal where the objective is a random draw over plans (§4). Our `sigmoid(margin/3000)`
  before rank normalisation is provably a no-op.
- **Lowering lr alone.** The mixed-integer analyses say the binding constraint is the
  *relation between σ and the granularity*, not the step length — consistent with §62's
  measured cliff (α 0.03 behaviourally B, α 0.1 carries the full loss) and with the
  flow206 lr 3e-4 control losing at g10.
- **A soft/straight-through decode.** §67's rejection is correct and the literature agrees
  on the reason: STE exists to carry a *backward* pass, and ES has none. What the QAT/RL
  literature actually supplies is the **forward sampling** half (§5 → §2).
