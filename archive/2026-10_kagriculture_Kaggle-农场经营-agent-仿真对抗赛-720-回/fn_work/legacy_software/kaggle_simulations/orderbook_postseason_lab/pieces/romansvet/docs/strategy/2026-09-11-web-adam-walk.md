# Adam on a zero-SNR ES gradient: what the literature says, and what to change here

Web-research agent, 2026-09-11, 45-minute box. WebSearch/WebFetch only + read-only numpy on
`S/onestep/grads/*.npy`. No training, no lock, no ssh, `git diff --stat src/` empty.
Inputs read: `docs/strategy/2026-09-11-{insample-vs-holdout,e3-step-audit,lr3e-4-restage}.md`,
consensus §56-§62 (and §63-§69, which landed during the box and change the reading).

## 0. A new measurement made inside this box (zero cost, from the saved draws)

The §60 statistic (`‖g_512‖/‖g_2048‖ = 2.0`, `cos(g_512,g_2048) = 0.53`) cannot separate "zero mean
gradient" from "small mean gradient", because at any signal fraction below ~10 % both statistics read
their zero-signal values. The statistic that *can* separate them is the cosine between two **disjoint**
draws, and it can be reconstructed from the two saved files without re-running anything: with the
2048-draw sharing its first 256 pairs with the 512-draw,

```
g_rem = (1024*g_2048 - 256*g_512) / 768      # the 768 pairs that only the big draw saw
```

| σ | ‖g‖ P512 | ‖g‖ P2048 | ratio | cos(512,2048) | **cos(512, rem) = disjoint draws** | null sd 1/√n |
|---|---|---|---|---|---|---|
| 0.01 | 105.90 | 52.99 | 1.998 | +0.532 | **+0.0386 (3.0 σ)** | 0.0129 |
| 0.02 | 34.24 | 16.89 | 2.027 | +0.527 | **+0.0236 (1.8 σ)** | 0.0129 |
| 0.04 | 23.18 | 11.63 | 1.993 | +0.512 | **+0.0159 (1.2 σ)** | 0.0129 |

(Caveat: ranks are computed *within* each population, so the shared 256 pairs contribute a residual
`Σ(adv_2048 − adv_512)ε`; since corr(adv,adv) < 1 with equal variances that residual correlates
**negatively** with `g_512`, so +0.039 is a lower bound, not an upward bias. One seed, one centre.)

**+0.0386 at σ 0.01 is, to two digits, the textbook noiseless value for a Gaussian-smoothing estimator:
`ρ = P/(P+d) = 256/(256+5997) = 0.041`** (P = antithetic pairs, d = live coords; Nesterov & Spokoiny
2017; Berahas et al. 2022). So the honest reading is **not** "the gradient is pure noise" — it is
"the estimator is at its theoretical *dimension-limited* SNR, with essentially no evaluation noise left
after CRN at σ 0.01". 96 % of each draw is directional sampling noise because d ≫ P, not because the
landscape is flat. The signal fraction falls with σ (0.041 → 0.024 → 0.016), consistent with §67's
tie census: larger σ smooths across more integer cells and shrinks the usable slope.

Everything below is written against that reading.

---

## 1. Adam / sign-SGD under zero or low gradient SNR

**(1a) Adam's update norm is ≈ lr per coordinate whatever the gradient is — by design, not by accident.**
Kingma & Ba state it as a feature: "the effective magnitude of the steps taken in parameter space at each
timestep are approximately bounded by the stepsize setting α", `Δt = α·m̂t/√v̂t`, and the update is
invariant to rescaling of the gradient (Adam, ICLR 2015, §2.1, https://arxiv.org/abs/1412.6980). Under a
zero-mean gradient `m̂/√v̂` is an O(1) random sign per coordinate, so ‖δ‖ → lr·√n — exactly our
0.003·√5997 = 0.232. *Applies directly.* The "trust region" that makes Adam robust in supervised
learning is precisely what converts our 4 %-signal draw into a 96 %-noise isotropic walk, and §63's
measured smooth-cell radius (0.0023-0.0035) is 70-100× smaller than that trust region.

**(1b) sign-SGD is the same pathology, and its theory names the governing quantity.**
Bernstein et al., signSGD (ICML 2018, arXiv:1802.04434; majority-vote version
https://arxiv.org/pdf/1810.05291) show the failure probability of each sign bit is governed by the
per-coordinate SNR `S_i = |g_i|/σ_i`; as S_i → 0 the bit is a coin and the step is a walk. Our E3 audit
already measured that Adam's step at B is a sign step (cos with the ES direction 0.794 = √(2/π)), so the
signSGD analysis is the right model of our optimiser. *Applies.*

**(1c) Known fixes that make the step shrink when the gradient is noise.**
- **AdaBelief** (Zhuang et al., NeurIPS 2020, https://arxiv.org/abs/2010.07468): denominator is
  `s_t = EMA((g_t − m_t)²)` instead of `EMA(g_t²)`. Under pure noise `m→0` and `s→Var(g)`, so the update
  → 0 rather than → lr. This is the single smallest code change that removes the pathology while keeping
  an adaptive method. *Applies.* Concrete: `--optimizer adabelief` = replace
  `self.v = β2·v + (1−β2)·grad**2` with `β2·v + (1−β2)·(grad − m)**2` at `train.py:4971`.
  Risk: at our ρ = 0.04 the belief term is ~`Var(g)` in *every* coordinate, so the step shrinks roughly
  uniformly — it behaves like an automatic lr cut, not like a direction fix.
- **Adam with ε raised** until `√v̂ ≪ ε`: then `δ ≈ (lr/ε)·m̂`, i.e. proportional to the gradient again.
  Choi et al. 2019 (arXiv:1910.05446, id from memory) show large-ε Adam approximates momentum SGD and
  that ε must be tuned. *Applies*, and is a one-token change (`--eps-adam`), but it is exactly equivalent
  to (1d) with lr/ε as the step size — prefer (1d), which is already implemented.
- **Plain SGD + momentum, which is what the ES literature uses.** OpenAI's ES code exposes
  `{'sgd': SGD, 'adam': Adam}` (openai/evolution-strategies-starter `es_distributed/es.py`) and
  Salimans et al. 2017 (https://arxiv.org/abs/1703.03864) fix σ rather than adapt it. **ARS is explicit
  about *rejecting* our exact configuration**: "Salimans et al. 2017 address this issue by transforming
  the rewards into rankings and then using the adaptive optimization algorithm Adam … Both of these
  techniques change the direction of the updates, obfuscating the behavior of the algorithm"; ARS instead
  divides the raw step by σ_R, the standard deviation of the 2b rewards used in that update
  (Mania, Guy & Recht 2018, https://arxiv.org/abs/1803.07055, Alg. 2 line 7). *Applies directly.*
- **lr scaled by ‖g‖ or by an SNR estimate.** The adaptive-sampling literature gives the test form: the
  **norm test** (Byrd et al. 2012) and the **inner-product test** (Bollapragada, Byrd & Nocedal 2018,
  arXiv:1710.11258, id from memory) increase the sample size until the sampled gradient is a descent
  direction with high probability; McCandlish et al. 2018's **gradient noise scale**
  `B_noise = tr(Σ)/‖G‖²` (https://arxiv.org/abs/1812.06162) is the same quantity as a batch-size
  predictor. For us `B_noise ≈ d/ρ`-ish and the prescription is "raise P, or cut d", not "lower lr".
  *Applies* — and it is measurable for free from two half-populations (see §6).
- **CMA-ES step-size control (CSA).** Hansen & Ostermeier, *Completely Derandomized Self-Adaptation in
  Evolution Strategies*, Evol. Comput. 9(2) 2001
  (http://www.cmap.polytechnique.fr/~nikolaus.hansen/cmaartic.pdf): accumulate an evolution path
  `p ← (1−c)p + √(c(2−c)μ_eff)·(step)`; if successive steps are *uncorrelated* the path length equals its
  random-walk expectation and σ is left alone; if they are anti-correlated σ **shrinks**; only a path
  longer than the walk expectation grows σ. This is literally a random-walk detector for step lengths and
  is the single most on-point classical mechanism for our failure. *Applies.* The (1+1) analogue is
  Rechenberg's **1/5 success rule** (multiply by F on success, F^(−1/4) on failure).
- **Noise handling in ES**: for noisy fitness the standard levers are re-evaluation and population-size
  adaptation (PSA-CMA-ES, Nishida & Akimoto GECCO 2018; adaptive re-evaluation
  https://arxiv.org/abs/2409.16757; UH-CMA-ES rank-change measurement). *Partly applies*: our σ 0.01
  measurement says evaluation noise is already small under CRN — our noise is **dimensional**, so
  re-evaluation buys nothing and population size buys ρ linearly.

## 2. Weight decay: decoupled, lr-coupled, and holding the equilibrium norm

- Loshchilov & Hutter, *Decoupled Weight Decay Regularization*, ICLR 2019
  (https://arxiv.org/abs/1711.05101): L2-in-the-gradient and weight decay are equivalent for SGD but not
  for Adam; decoupling "decouples the optimal choice of weight decay factor from the setting of the
  learning rate". **Note the direction of the fix**: AdamW still multiplies the decay by the schedule
  multiplier (`θ ← θ − η_t(lr·m̂/√v̂ + λθ)`), so decay and step scale *together*.
- Our trainer does neither convention: `upd = (1 − wd)·(θ + δ)` (tree `train.py:4994`), i.e. decay is
  decoupled **and lr-independent**. Balancing coherent contraction against the isotropic walk gives
  `‖θ‖* = lr·√(n/(2·wd))` (the trainer's own help text says this) versus AdamW's `‖θ‖* = √(lr·n/(2λ))`.
  So **under our convention the equilibrium norm scales as lr, and holding it fixed requires wd ∝ lr²**
  (lr 0.003→3e-4 ⇒ wd 1e-4→1e-6); under the AdamW convention it would require wd ∝ lr⁰ — nothing.
  Kosson et al., *Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks*
  (https://arxiv.org/abs/2305.17212) is the modern reference for this balance and for expressing it as an
  equilibrium *angular update per step*, which is the quantity to hold fixed across an lr change.
- **Numbers for the live arms**: at lr 3e-4, wd 1e-4, ‖θ_B‖ = 15.8, the decay pull is
  `wd·‖θ‖ = 1.6e-3` per generation and is perfectly coherent; the *signal* part of the step is
  `ρ^½·‖δ‖ ≈ 0.2 × 0.023 = 4.6e-3` at best and the isotropic part 0.023. Over 300 generations decay moves
  θ by 0.47 (−3 % of the norm) toward the origin. It is not fatal at lr 3e-4 but it is the largest
  systematic displacement in flow206/flow205, and at any lr below ~1e-4 (which §1's analysis wants) it
  **dominates the signal outright**. *Applies — this is a correctness issue, not a tuning preference.*

## 3. Statistical tests for "is this ES gradient signal?"

- **Disjoint-draw cosine (done above).** Null: `cos ~ N(0, 1/√d)`. Signal reference for a *noiseless*
  objective: `ρ = P/(P+d)`. This one test distinguishes "no signal", "dimension-limited signal" and
  "evaluation-noise-limited signal" (which would read *below* P/(P+d)). Our σ 0.01 draw sits on the
  noiseless line ⇒ CRN is doing its job and **d is the binding constraint**.
- **Split-half / bootstrap**: bootstrap the pairs of one generation into two halves, report the cosine
  distribution — same statistic with error bars, free. Beware the retraction already on file
  (memory `es-noise-floor-2026-09-05`): splitting *episodes* with ε fixed is trivially self-correlated;
  the split must be over **ε rows**.
- **Paired sign test on antithetic pairs**: by symmetry `sign(f(θ+σε) − f(θ−σε))` is a fair coin under
  H0 for a *random* ε, so the useful version is the projected one — sign of `(f⁺−f⁻)·(ε·u)` for a fixed
  reference direction u (e.g. last generation's m). A binomial test on P = 256 pairs detects ρ ≈ 0.04 only
  at ~1.3 σ, so **one generation can never certify a step**; this is the quantitative reason the
  "one-step / κ" rig at B was underpowered (consensus §60's "honest n = 1").
- **Nesterov & Spokoiny 2017** (*Random Gradient-Free Minimization of Convex Functions*, FoCM 17:527-566,
  https://link.springer.com/article/10.1007/s10208-015-9296-2): zeroth-order methods need **O(n) times
  more iterations** than gradient methods and the Gaussian-smoothing estimator's second moment carries an
  explicit factor of the dimension n. That is the theoretical statement of `ρ ≈ P/(P+d)`.
  Berahas et al. 2022 (FoCM, arXiv:1905.01332, id from memory) gives the finite-difference/Gaussian/
  orthogonal comparison with the same n/P scaling.
- **Population-size rule of thumb**: CMA-ES's default is λ = 4 + ⌊3 ln n⌋ for *unimodal noiseless*
  problems and the standard advice under noise is to multiply it; for ES-as-gradient the sharper rule is
  the one above — `ρ ≈ P/(P+d)`, so the population needed for a fixed SNR is **linear in d**.
  Zhang, Clune & Stanley 2017 (https://arxiv.org/abs/1712.06564) is the empirical version: they measure
  the ES-vs-SGD gradient correlation as a function of population size and build an SGD proxy that
  predicts ES performance per population size.

## 4. What ES-for-RL papers actually do for step control

| paper | step control | stop / reduce rule | relevance here |
|---|---|---|---|
| Salimans et al. 2017 (arXiv:1703.03864) | centred ranks; Adam **or** SGD (code `es.py`); σ fixed, "no benefit from adaptation"; L2 folded into the gradient `optimizer.update(-g + l2coeff*θ)` — so their decay *is* normalised by Adam and bounded by lr, unlike ours | none; fixed lr, virtual batch norm to make the objective sensitive to perturbation | their d/P was ~1e6/1e4; they lived at ρ ≈ 0.01 and still climbed — because their per-step *displacement* was small relative to the smooth region, which is exactly what B lacks |
| Mania, Guy & Recht 2018 ARS (arXiv:1803.07055) | plain SGD, step `α/(bσ_R)·Σ[r⁺−r⁻]δ`; **top-b directions only** (V2-t); states ranks+Adam "obfuscate the behavior" | no stop rule; they report success is as sensitive to seeds as to hyperparameters | directly recommends our fix: ‖g‖-proportional step, normalised by the *spread of returns*, no adaptivity |
| Such et al. 2017 Deep GA (arXiv:1712.06567, id from memory) | no gradient at all: elitist truncation selection | elitism = accept-only-if-better | the (1+1)/elitist family, see §5 |
| PGPE (Sehnke et al. 2010) / NES, xNES (Wierstra et al., JMLR 15, 2014, https://www.jmlr.org/papers/volume15/wierstra14a/wierstra14a.pdf) | natural gradient; xNES **separates a scalar step size σ from the shape B** with independent learning rates; learning-rate adaptation for NES: arXiv:2112.10680 | shape/scale separation is the principled version of "shrink the step but keep the direction" | a scalar step-size learning rate is exactly the knob we are missing |
| Lehman et al. 2018 safe mutations (https://arxiv.org/abs/1712.06563) | perturb each weight in inverse proportion to the **sensitivity of the network's outputs** to it (SM-G) | — | *high relevance to §66/§67*: our damage is caused by perturbations that flip integer decodes; SM-G is the published way to shape the perturbation covariance so behaviour is preserved |
| Lehman et al. 2018, *ES is more than a finite-difference approximator* (https://arxiv.org/abs/1712.06568) | — | — | ES optimises the **smoothed** objective `E_ε f(θ+σε)`; with 46/68 ties inside σ 0.02 (§67), the smoothed objective at B is genuinely different from f(B) and "B is best" and "B is an ES optimum" are different claims |
| Choromanski et al. 2018 (ICML, https://arxiv.org/abs/1804.02395) | structured **orthogonal** perturbation matrices + **compact architectures** | — | orthogonal ε at fixed P is a free variance cut; compact policies attack d, the binding constraint |
| Depth over Fidelity in Fixed-Budget Noisy ES (2026, https://arxiv.org/abs/2606.06555) | probabilistic elite membership instead of hard ranks | prefer more generations over more evaluations per candidate | our noise is dimensional rather than evaluative, so this argues *against* spending more episodes/board |

## 5. Is "reset Adam after a plateau" or "(1+1) accept-if-improves" the standard remedy?

- **Resetting the optimizer** is a real, published practice, but for a different disease: non-stationarity.
  Asadi et al., *Resetting the Optimizer in Deep RL* (https://arxiv.org/abs/2306.17833) reset Adam's
  moments (especially the second moment, stale at β2 = 0.999) at each new iteration of a changing
  objective. *Does not apply as a cure here*: resetting m and v does not change the fact that the next
  step is again lr·√n of noise. Our trainer already clears m, v and adam_t on `_restart_from_record`.
- **Elitist acceptance is the standard remedy in the EA literature**, and it is what the (1+1)-ES with the
  1/5 rule does: accept the offspring only if it is at least as good, expand the step on success, shrink
  it by F^(−1/4) otherwise (Rechenberg; see Global Convergence of the (1+1)-ES,
  https://arxiv.org/abs/1706.02887). With noisy fitness naive elitism latches onto lucky evaluations —
  which is *precisely* what our `--real-gate`/`best_abs` machinery already suffers from — so the
  literature's answer is elitism **plus** a paired/re-evaluated comparison. We have the strongest possible
  version of that available: `S/simscreen` is engine-exact (sim = engine 99.5 %) and lottery-free, 120
  boards in ~12 CPU-minutes. A block-elitist trainer (accept the last k generations' accumulated
  displacement only if the paired screen Δ > 0, else halve the step and roll back) is a defensible,
  citable design and cannot random-walk downhill.

---

## 6. Ranked top-3 for our trainer, with the cheapest test for each

### 1. Cut d before touching lr: train a subspace, not all 5,997 coordinates
`ρ ≈ P/(P+d)` is measured, not assumed (§0). At P = 256 pairs, d = 5,997 ⇒ ρ = 0.041. Training only the
global-head + policy blocks (d ≈ 1,000) gives ρ ≈ 0.20 — a **5× SNR gain at identical compute**, and the
same lever the ES-RL literature reaches for (ARS's linear policies; Choromanski's "compact
architectures"; Nesterov's O(n) iteration penalty).
*Change*: `--train-only <blocks>` already exists (used by §64's mask work); run the arm on the subspace
that carries the levers rather than on w1+g1+g2 (which §64 shows carry the day-0 switch — freezing them
also removes the largest cliff, and pairs naturally with `SEED_ROOM_PURSE_ON` from §69).
*Expected*: disjoint-draw cosine rises from 0.04 to 0.1-0.25; per-generation displacement along the true
gradient rises ~5× at equal step length. *Risk*: the subspace may not contain the levers — measure first.
**Cheapest experiment (free, ~10 min, CPU):** restrict the §0 cosine to each `PO.SHAPES` block using the
existing offset map and check `ρ_block ≈ P/(P+d_block)`. If a block's ρ is *above* its dimensional
prediction, that block carries the signal; train only it.

### 2. Make the step proportional to ‖g‖ and size it against the tie radius; fix the decay convention
Adam's `|Δ| ≲ α` guarantee (Kingma & Ba §2.1) is the mechanism of the walk; ARS explicitly rejects
ranks+Adam and scales by σ_R instead (Mania et al. 2018); AdaBelief is the adaptive method that shrinks
under noise (Zhuang et al. 2020).
*Change (already implemented, no code edit)*: `--optimizer sgd` ⇒ `δ = lr·m`. With `‖m‖ ≈ ‖g‖·√((1−β1)/(1+β1))`
= 0.229‖g‖ and the measured ‖g‖ (σ 0.02, P 512) = 34.2, a target ‖δ‖ = 0.001 (≈ ⅓ of §63's 0.0023-0.0035
smooth-cell radius) gives **lr ≈ 1.3e-4**; at σ 0.01, ‖g‖ = 105.9 ⇒ lr ≈ 4e-5. The walk then also shrinks
as 1/√P automatically (‖g‖ halved when pop quadrupled — measured), which Adam's step never does.
*Companion, mandatory*: `wd` must move as lr² under our `upd = (1−wd)·step` convention (AdamW would have
made it lr¹): at lr 1.3e-4, `wd = 1e-4·(1.3e-4/0.003)² ≈ 2e-7`, i.e. effectively 0 for a ≤300-gen arm.
Leaving wd at 1e-4 makes the coherent decay pull (1.6e-3/gen) 8× the signal component (2e-4/gen) — the arm
would measure "B, shrunk", not "B, moved". *Expected*: coherent displacement accumulates ∝ k while the
walk grows ∝ √k, so the signal overtakes the noise after ~1/ρ ≈ 25 generations. *Risk*: 300 generations at
this step length only travel ~0.06 along the gradient — deliberately slow; and `--optimizer sgd` keeps
`v` stale in the checkpoint (harmless, documented at `train.py:4963`).
**Cheapest experiment:** one 60-generation local arm (`--optimizer sgd --lr 1.3e-4 --weight-decay 0`),
then screen g20/g40/g60 **unscaled** on `S/simscreen` (§62 pre-rank rule, ~2 CPU-min each). Pass = a
monotone in-sample trend and no record worse than B by more than the screen's ±400/board; contrast with
flow206's Adam records, which lost on their own rungs by g10.

### 3. Instrument and gate on the SNR every generation — free, and it is the missing control loop
The norm/inner-product tests (Bollapragada et al. 2018), the gradient noise scale (McCandlish et al.
2018) and CSA's evolution path (Hansen & Ostermeier 2001) are three versions of one idea: measure whether
consecutive/independent estimates agree, and shrink the step (or grow the sample) when they do not.
*Change*: split each generation's population into two disjoint halves, form `g_A`, `g_B`, log
`ρ̂ = cos(g_A, g_B)` and scale the step by `clip(ρ̂/ρ_target, 0, 1)` (skip the generation when
`ρ̂ < 3/√d = 0.039`). Add the CSA scalar `‖Σ_k δ_k‖ / Σ_k ‖δ_k‖` over a 20-generation window: ≈ 1/√20
means pure walk, ≥ 0.5 means real travel. Both are ~5 lines and cost nothing (the halves are already
evaluated).
*Expected*: at B the gate reads ρ̂ ≈ 0.04 and automatically shortens the step by ~an order of magnitude —
the same prescription as §59 but self-tuning, and it re-opens when a subspace or a smoothed field raises ρ.
*Risk*: a gate that is never satisfied silently stops training — log it, do not make it fatal.
**Cheapest experiment:** already half-done — §0 is this statistic computed post-hoc. Repeat it at 3 fresh
seeds (`S/popcurve` style, one short probe) to put an error bar on ρ = 0.04 before wiring the gate.

**Runner-up (4th):** block-elitist acceptance — every 10 generations, screen the accumulated displacement
paired on `S/simscreen`; accept if Δ > 0, else roll back and halve the step (Rechenberg's 1/5 rule with an
engine-exact, lottery-free comparison). This is the only option on the list that *cannot* lose ground, and
our screen is cheap enough to afford it (12 CPU-min per 10 generations).

**Explicitly not recommended:** resetting Adam's moments on plateau detection (Asadi et al. 2023 — right
fix for non-stationarity, no effect on a dimension-limited gradient); more episodes per board (our σ 0.01
draw already sits on the noiseless ρ line, so evaluation noise is not the binding constraint — and the
2026 fixed-budget work argues for depth over fidelity anyway); raising σ (ρ fell monotonically with σ:
0.041 → 0.024 → 0.016).

## Sources
Adam (Kingma & Ba, ICLR 2015) https://arxiv.org/abs/1412.6980 ·
signSGD (Bernstein et al., ICML 2018) arXiv:1802.04434, majority vote https://arxiv.org/pdf/1810.05291 ·
AdaBelief (Zhuang et al., NeurIPS 2020) https://arxiv.org/abs/2010.07468 ·
Choi et al. 2019 arXiv:1910.05446 (id from memory) ·
AdamW (Loshchilov & Hutter, ICLR 2019) https://arxiv.org/abs/1711.05101 ·
Rotational Equilibrium (Kosson et al. 2023) https://arxiv.org/abs/2305.17212 ·
OpenAI ES (Salimans et al. 2017) https://arxiv.org/abs/1703.03864 + code
https://github.com/openai/evolution-strategies-starter/blob/master/es_distributed/es.py ·
ARS (Mania, Guy & Recht 2018) https://arxiv.org/abs/1803.07055 ·
Deep GA (Such et al. 2017) arXiv:1712.06567 (id from memory) ·
NES/xNES (Wierstra et al., JMLR 15, 2014) https://www.jmlr.org/papers/volume15/wierstra14a/wierstra14a.pdf ·
NES learning-rate adaptation https://arxiv.org/abs/2112.10680 ·
Safe mutations (Lehman et al., GECCO 2018) https://arxiv.org/abs/1712.06563 ·
ES ≠ finite differences (Lehman et al., GECCO 2018) https://arxiv.org/abs/1712.06568 ·
ES vs SGD (Zhang, Clune & Stanley 2017) https://arxiv.org/abs/1712.06564 ·
Structured evolution / compact architectures (Choromanski et al., ICML 2018) https://arxiv.org/abs/1804.02395 ·
CSA/CMA-ES (Hansen & Ostermeier, Evol. Comput. 2001)
http://www.cmap.polytechnique.fr/~nikolaus.hansen/cmaartic.pdf ·
(1+1)-ES global convergence https://arxiv.org/abs/1706.02887 ·
Adaptive re-evaluation under noise (GECCO 2025) https://arxiv.org/abs/2409.16757 ·
Depth over Fidelity in Fixed-Budget Noisy ES (2026) https://arxiv.org/abs/2606.06555 ·
Gradient noise scale (McCandlish et al. 2018) https://arxiv.org/abs/1812.06162 ·
Norm/inner-product tests (Bollapragada, Byrd & Nocedal 2018) arXiv:1710.11258 (id from memory) ·
Random gradient-free minimization (Nesterov & Spokoiny, FoCM 2017)
https://link.springer.com/article/10.1007/s10208-015-9296-2 ·
Gradient approximations in DFO (Berahas et al., FoCM 2022) arXiv:1905.01332 (id from memory) ·
Resetting the optimizer in deep RL (Asadi et al. 2023) https://arxiv.org/abs/2306.17833
