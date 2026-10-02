# Blind review of "the ES gradient is noise at every pop" — and a decisive one-step test

Reviewer B, 2026-09-10/11. Written **blind**: `2026-09-10-pop-spearman.md` and consensus §16
were opened only after §4. Data: `S/popcurve/results.csv`. Scripts + raw output: `S/popcurve/B/`
(`onestep.py`, `fit.py`, `concentration.py`, `summarise.py`, `onestep.json`, `onestep.log`,
`summary.txt`, `grads/`).

**Verdict in one line.** A's *measurement* reproduces exactly and its conclusion is **right but for
an incomplete reason**; the decisive test tightens the bound 5x and finds the real blocker is not
that the gradient is absent — the local gradient is large — but that **`lr 0.003` is 3-10x past the
step size at which the estimate's 1 % alignment can pay for the curvature it buys.**

Assumptions. (1) `--abs-weight 0.0`, so `shaped_advantage` = `rank_normalise(rung-weighted mean_e
sigmoid((mine-theirs)/3000))`; that weighted mean **is** `F`. (2) Adam's update is ~`lr` per
coordinate, so the arm's real per-gen displacement is `||d|| = 0.003*sqrt(5997) = 0.2323`.
(3) Centred ranks ~uniform on [-1/2,1/2], `Var(a) = 1/12`. Live-confirmed at setup: `n 6789 live
5997 sigma 0.02 margin_scale 3000 abs_weight 0.0 ||theta|| 17.964 ||sigma*eps|| 1.549 episodes 159`.

## 1. Is two-seed direction correlation the right statistic? No — it is the blunt one.

`m = P/2` pairs, `eps_i ~ N(0,I_n)`, `da_i = a_i+ - a_i-`, `g = (1/(P sigma)) sum_i da_i eps_i`.

**Linear, noise-free.** `f(theta+sigma eps) = f0 + sigma mu.eps` makes `da_i = phi(mu.eps_i)` for an
odd non-decreasing `phi`. Gaussian integration by parts (Stein) gives `E[phi(mu.eps) eps] = E[phi'] mu`, so `E[g] = (E[phi']/(2 sigma)) mu = c mu` **for every m >= 1**.

**With a nonlinear part.** `E[g] = (1/(2 sigma)) E[da eps]`, which by the same identity is the
gradient of the *sigma-smoothed* shaped fitness. So `E[g] ∝ mu` no matter how nonlinear `da` is:
**noise moves the variance of `g`, never its mean.** Hence

* `E[g]` is P-independent and `Var(g) ∝ 1/P`, so `rho(P) = ||Eg||^2/(||Eg||^2 + A/P)` **rises to 1 with P for any nonzero signal**. `rho = 0` at one P bounds one draw's SNR; it does not bound `E[g]`.
* The step's alignment is `kappa = cos(g, mu) = sqrt(rho)` — the cosine understates direction quality by a square root (`rho = 0.005` is `kappa = 0.07`).
* Progress compounds: drift `T kappa ||d||` vs walk `||d|| sqrt(T)`, so signal wins once `T > 1/kappa^2`; `kappa = 0.05` needs ~460 gens — the length of these arms, not a refutation.
* **Rank normalisation is scale-free in the fitness**: `phi` saturates, `E[phi'] ∝ 1/||mu||`, so `||E g||` is independent of `||mu||`. **`||g||(P)` cannot bound `||mu||` in objective units at all**; any progress claim must measure `Delta F` (§3). *Dead end, recorded.*

## 2. What the csv actually supports

Null sd of a cosine is `1/sqrt(5997) = 0.0129`. The five values give pooled mean `-0.0058 +- 0.0058` (z = -1.01); the apparent rise with P is `+0.0078 +- 0.0041` per doubling but the 64-1024 difference is 1.7 sd, and fitting the correct shape gives `chi2(S^2=0) - chi2(best) = 0.15`. **No evidence of a signal and none against one.** Bounds on `kappa(512)`: from the `||g||^2 = S^2 + A/P` fit, `||Eg|| <= 11.4` (weighted) or `31.1` (unweighted) — useless, ten noisy points cannot separate a constant from `1/P`. From the cosines, profile 95 % `S^2 <= 20`, i.e. **`kappa(512) <= 0.115`**, point 0.047. `||g|| ∝ P^-0.5` is confirmed (`||g||^2` ratios 2.24 / 1.98 / 1.87 / 2.01 vs 2.00) but is *not* evidence of zero signal — it is what small `kappa` looks like.

Two readings the first review did not take:

* **Within-pair rank correlation `+0.385`.** `A = n E[da^2]/(2 sigma^2)` gives `E[da^2] = 0.1025`; independent ranks give `1/6`, a linear landscape (`a- = -a+`) gives `1/3`. Observed is **below independence**, so `corr(a+, a-) = +0.385` — 38 % of a member's rank is shared with its own antithetic twin, i.e. even in `eps`, i.e. curvature, and the pair difference throws it away. This predicted §3's result before §3 ran.
* **How far below perfect linearity.** With `R^2` = the share of `Var(da)` one coherent direction explains, `rho = P R^2/(2n + P R^2)` and `R^2 = 0.955` for the rank map on a linear landscape. Observed vs that ceiling: z = -2.07, -2.03, -1.61, -3.03, -5.11 at P = 64…1024, **combined Z = -6.20**; inverting, `R^2 <= 0.13` (95 %) against 0.955.

## 3. Decisive test: one step, ES direction vs random directions

`S/popcurve/B/onestep.py` reuses `S/popcurve/popcurve.py`'s `build_trainer` / `build_batch` / `one_draw` — the arm's own CLI, ladder, batch and `_play`; nothing re-implemented. Remote GPU0, `~/stage_hr`, `--chunk 4096`, foreground ssh, 1331 s. P = 512, seeds 9001/9002, `d_s = 0.2323 * g_s/||g_s||`, plus 8 random unit directions in the live subspace at the same length, each at `+r` and `-r` (16 controls, 21 thetas per batch). Reproduction check: `||g||` came out
**40.9004 / 39.2552** against A's 40.88095 / 39.2682 — 0.05 %, i.e. the two harnesses agree.

**IN-SAMPLE** = the arm's own batch (147 pinned x 1 episode + 12 carried = 159). **HELD-OUT** = LIVE-C ids 43-72 (`S/livec/ids.txt` 43-72 = 107463847…107507032), verified **0/30 overlap with flow187's 147 training rungs** and all 30 are flow187's own gate field, played as pinned rungs from **both seats** (batch rebuilt at `t=0` and `t=1`) = 60 games.

**The statistic.** The antisymmetric part isolates the linear term: for isotropic `r`,
`F(+r)-F(-r)` has sd `2|gradF| ||d|| / sqrt(n)`; for the ES direction it is `2|gradF| ||d|| kappa`. So `z = kappa sqrt(n) = kappa * 77.4` against 8 randoms (7 dof) — **the test resolves `kappa >= 0.031`, where the two-seed cosine only resolves `kappa >= 0.161`. It is 5x the instrument.** The symmetric part `(F(+r)+F(-r))/2 - F(theta)` is the curvature control.

### Results (primary metric `obj_w`; full table in `S/popcurve/B/summary.txt`)

| | `F(centre)` | 16 random steps | ES 9001 `+d` / `-d` | ES 9002 `+d` / `-d` |
|---|---|---|---|---|
| IN-SAMPLE obj | 0.5952 | **-0.0111** sd 0.0078 | -0.0194 / -0.0284 | -0.0158 / -0.0158 |
| IN-SAMPLE win | 0.6102 | **-0.0228** sd 0.0110 | -0.0392 / -0.0511 | -0.0420 / -0.0383 |
| HELD-OUT obj | 0.6164 | **-0.0173** sd 0.0163 | -0.0069 / -0.0449 | -0.0113 / -0.0229 |
| HELD-OUT win | 0.6667 | **-0.0708** sd 0.0352 | -0.0333 / -0.0833 | -0.0667 / -0.0667 |

1. **Every direction loses, everywhere.** All 16 random steps lose in-sample (max -0.0005); 15/16 lose held-out. One generation of Adam displacement in a *random* direction costs 2.3 pts of in-sample win rate and **7.1 pts of held-out win rate** (60 games, direction-to-direction sem 0.9 pt). `flow172_g1000` is a sharp local maximum of flow187's objective *as re-weighted*.
2. **`+d` and `-d` both lose: curvature-dominated, not linear** — exactly what `corr(a+,a-) = +0.385` predicted.
3. **The ES step does not beat random in-sample; it is *worse*.** `+d` beats 19 % / 38 % of random steps, and its symmetric (curvature) part is -0.0239 / -0.0158 against random -0.0111 sd 0.0043 (z = -3.0 / -1.1): the estimator preferentially loads onto brittle, high-curvature directions.
4. **Held-out it is marginally better than random**: `+d` beats 69 % / 62 %, antisym positive for both seeds (+0.0381, +0.0117; z +1.27, +0.39).
5. **`kappa` measured directly**: in-sample `+0.0043 +- 0.0091` (95 % CI -0.014…+0.022), held-out `+0.0107 +- 0.0091` (-0.007…+0.029). Both **exclude `kappa >= 0.031`**, an order of magnitude below §2's point estimate 0.047 and its 0.115 ceiling.
6. **But the true gradient is large.** From the random antisymmetric spread, `|gradF| ||d|| = 0.53` in-sample and **1.16 held-out** — a perfectly aligned step of this length would gain more than the objective's whole range. The objective is *not* flat; the estimate finds 1 % of it.
7. **The only 4/4-consistent signal is on raw coins, not on the objective.** Antisym z on `margin` is +1.19 / +0.94 in-sample and +1.33 / +0.57 held-out (positive in all four cells, `kappa` 0.012-0.017) while on `obj_w` it is 2/4. Note `obj_w 0.5952` vs `win_w 0.6102`: at `--margin-scale 3000` the sigmoid saturates past +-9k, so the ES ranks on a near-binary win bit — the exact failure `shaped_advantage`'s own docstring argues 100k exists to avoid.

## 4. Verdict

**(i) A's conclusion: supported as stated, and its reason is incomplete.** "Indistinguishable from
noise at every pop" is correct for the estimate (I reproduce `||g||` to 0.05 % and every cosine),
and my direct test tightens `kappa(512)` from `<= 0.115` to `<= 0.03`. What does *not* follow from
the cosine is "therefore no progress" — §1 shows `E[g] ∝ mu` regardless, and A's own doc leans on
the cosine for a conclusion the cosine cannot carry. The *load-bearing* fact is §3.6-3.1: the local
gradient is large (`|gradF| ||d||` = 0.53-1.16) and the per-step curvature cost (0.011-0.017) beats
the realisable linear gain (`kappa * |gradF| ||d||` = 0.002-0.012).

**(ii) Does the ES step beat random? In-sample no** (19 %/38 % percentile, curvature z -3.0/-1.1).
**Held-out marginally yes** (69 %/62 %, antisym positive both seeds) but well inside noise and still
a net loss in absolute terms.

**(iii) For flow187/188/189 and the subspace idea.** These arms are not descending a gradient; they
are (1+lambda) hill-climbing whose proposal happens to cost 512 rollouts, and every accepted record
comes from the gate, not the step — A's phrase "gate-filtered lottery" is right and now measured.
The `--train-only`-by-`|g|` proposal (A's §Recommendation, "rank the 5997 coordinates by `|g|`
pooled over the ten draws already saved") **is selection on noise, and I tested it**
(`S/popcurve/B/concentration.py`): rank by `|g|` from seed 9001, then measure agreement with the
independent seed 9002 on that set — null-centred at 0/0.5 however the set is chosen. Over 5 pops x
top-{100, 10, 5, 1, 0.2} %, pooled Z is `-1.01…+1.03` (cosine) and `-1.03…+0.62` (sign). **No
concentration at any scale.** With `E[g]` spread over all n, one coordinate's SNR is `kappa ~ 0.01`,
so an honest mask needs `1/kappa^2 ~ 10^4` draws; the ten saved draws give SNR 0.03. A's *dimension*
argument (`cos = 1/sqrt(1+n/m)`, symmetric in m and n) is sound and I derived the same identity —
cutting n is a real lever. `|g|` is simply not a way to find the subspace.

**(iv) The one change with evidence behind it: `--lr 0.003 -> 0.001`.** Net gain per step is
`h(kappa |gradF| - C h)`, and 22 direct evaluations fix all three terms: `|gradF| = 2.28`
(in-sample) / 4.99 (held-out), `C = 0.205 / 0.321`, `kappa = 0.0043 / 0.0107`. Break-even `h` is
`kappa|gradF|/C` and the optimum is half that: **`h* = 0.024` (in-sample) to `0.083` (held-out),
i.e. lr 0.0003-0.0011, against 0.003 today.** Only if `kappa` sits at its 95 % upper bound is the
present lr justified (`h* = 0.22`). The curvature cost scales `h^2` while the gain scales `h`, so
this is the cheapest available factor — no extra rollouts, unlike the `P ~ 1900` that the same
arithmetic would need (`kappa ∝ sqrt(P)`, 3.6x pop to reach in-sample break-even). Caveat: Adam
momentum makes the realised per-gen displacement along a persistent direction larger than `lr`, and
a smaller lr slows travel; but travel in a losing direction is not progress. **Secondary, hypothesis
only:** `--margin-scale 3000` makes the objective the win bit (§3.7) and the coin signal is the one
that replicates 4/4 — worth one A/B of `margin_scale` on this same 22-evaluation rig before any arm.

## 5. Dead ends recorded

* **Bounding `||mu||` from `||g||(P)`.** Impossible in principle: rank normalisation saturates. Do not repeat.
* **`||g||^2 = S^2 + A/P` as a signal detector.** Bounds `||Eg||` to `<= 11-31` where the cosines give `<= 4.5` and the step test gives an outright estimate. Report it only as the `P^-0.5` check.
* **`|g|`-ranked `--train-only` subspace.** Measured, no concentration at any scale (above).
* **Reading the negative cosines at P = 64/128 as a bias.** Pooled z = -1.01. Nothing there.
* **The two-seed cosine as the primary instrument.** It resolves `kappa >= 0.161`; the one-step antisymmetric test resolves `kappa >= 0.031` for 22 batch evaluations against A's ~2,900 member-generations. The step test should have been first.

## 6. Agreement / disagreement with `2026-09-10-pop-spearman.md` and consensus §16

**Agree.** Every number in A's table reproduces (`||g||` to 0.05 %). The retirement of the on-file
"half-split Spearman 0.93-0.96" is correct and important — it varied *episodes* with `eps` fixed. A's
dimension ceiling `cos(g1,g2) = m/(m+n) = P/(P+2n)` is exactly my `rho = P R^2/(2n + P R^2)` at
`R^2 = 0.955`; I confirm the curve runs below it (combined Z = -6.20) and identify the mechanism as
`corr(a+,a-) = +0.385`. "The arm advances by gate-filtered lottery, not by descending a gradient" is
confirmed directly. Consensus §16's open item ("a near-zero Spearman does not by itself show zero
progress per step") is exactly right and is what §1 proves and §3 answers; §16's pre-emptive
"`--train-only` subspace selection is NOT to be built on `|g|` ranking from noise draws" is now
measured, not assumed.

**Disagree.** (a) A's headline "there is no curve" over-reads a null: the same data are consistent
with `kappa` up to 0.115, and it took the step test to rule that out — the cosine is the wrong
instrument, not merely an underpowered one. (b) A's extrapolation "Spearman 0.9 at P ~ 690,000" is
a fit of `cos = P/(P+c)` to two points, one of them 2.0 sd; with `R^2 <= 0.13` the same form gives a
different `c`, and neither is worth quoting. (c) A's recommendation **"Keep `--pop 512`, change
nothing"** rests on wall-clock SNR being pop-invariant (`ceiling x gens/hour` constant). That
invariance ignores the per-step curvature cost, which is paid `G` times and scales `h^2`: in a
curvature-dominated regime fewer, cleaner steps strictly win, so the product is *not* invariant and
"change nothing" does not follow from it. The lever it misses is not pop at all — it is `lr`, which
A never varied and which §4(iv) prices from measurement.
