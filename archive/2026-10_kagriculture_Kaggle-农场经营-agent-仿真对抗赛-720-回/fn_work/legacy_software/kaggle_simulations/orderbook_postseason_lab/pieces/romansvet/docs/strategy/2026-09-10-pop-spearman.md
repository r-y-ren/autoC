# Population vs gradient reproducibility (`--pop`, measured 2026-09-10)

**Question.** `--pop 512` was chosen by elimination: `2026-09-10-es-rate-A.md` records *"no pop-vs-Spearman
measurement exists"*, while review B asserts *"doubling pop or E buys ≤ 0.03 Spearman"* off the on-file 0.93–0.96.
Measure the curve.

**Answer: 512 is not on a plateau — there is no plateau, because there is no curve.** Across two independent
perturbation seeds the gradient's Spearman is **statistically zero at every P from 64 to 1024**; it first clears the
null at **P = 2048 (ρ = 0.015, cos = 0.026, 2.0 sd)** — 78× below 0.9. The on-file "0.93–0.96" is a *different
quantity*: it splits the **episodes** with `eps` held fixed, so under `--pinned-once` (deterministic fitness) it is
near-1 by construction. Nobody had varied `eps`. Spearman reaches 0.9 only at P ≈ 690,000 and 0.95 at P ≈ 1.45 M.

## What was measured

`S/popcurve/popcurve.py` runs the arm's own CLI (`~/stage_hr/scripts/train.py`, md5 `c8c22fb8…`, byte-identical to
`S/localarm/tree`) through `runpy` with the flow187 launcher's own flags (`S/flow187/launch_flow187.sh`, md5
`b5cb30a3…` = the remote `~/launch_flow187.sh`), replaces the first `Trainer.generation()` with a sentinel raise, then
draws the gradient out of the trainer's own pieces — `perturbations`, `shaped_advantage` (which holds
`rank_normalise`), `Trainer._play`, `Trainer.fitness_bonus`, and the line `grad = (adv[:P/2] - adv[P/2:]) @ eps / (P *
sigma)` (train.py:5204). Nothing is re-implemented: estimator, ladder (151 rungs / 147 pinned tapes), masks and centre
θ are the arm's.

* Centre θ `artifacts/kagg2_games/thetas/flow172_g1000.npy`, ‖θ‖ 17.96, σ 0.02, `--chunk 4096`
  (cost only). Remote GPU 1, sharing the card with flow187 throughout. 6789 parameters, **5997 live** (`--train-only
  all:5997/6789`); the 792 dead columns are 0 in every draw.
* One episode batch, built once by the trainer's own methods and reused: the 147
  `--tape-actions` rungs under `--pinned-once --pinned-fixed-seed --shop-crn` at one seat each plus the 6 residual
  carried pairs = **159 episodes** (the arm's own count). Fixed batch + deterministic pinned fitness ⇒ **two draws
  differ in `eps` alone.**
* Two independent eps seeds (9001, 9002) per P, plus the half-split within one draw (first P/4
  pairs vs second P/4, each re-rank-normalised inside its half, so each is the gradient a P/2 run would take).

## The curve

Centre θ = flow172_g1000, σ 0.02, 159 pinned episodes, two eps seeds (9001/9002), one seed pair per P. Correlations
over the 5997 live coordinates. **Null sd of every correlation: 0.0129.**

| P | Spearman(s1,s2) | cosine | half-split Sp (at P/2) | ‖g‖ | secs/draw | ceiling cos |
|---|---|---|---|---|---|---|
| 64 | −0.0278 | −0.0217 | +0.006 | 127.4 | 24.4 | 0.005 |
| 128 | −0.0194 | −0.0161 | +0.002 | 80.8 | 41.1 | 0.011 |
| 256 | −0.0043 | −0.0008 | +0.011 | 54.9 | 81.4 | 0.021 |
| **512** (the arm) | **+0.0029** | **+0.0000** | +0.025 | 40.9 | 163.3 | 0.041 |
| 1024 | +0.0078 | +0.0094 | +0.017 | 28.8 | 327.6 | 0.079 |
| 2048 | **+0.0151** | **+0.0261** | +0.032 | 19.4 | 654.4 | 0.146 |

`secs/draw` is post-compile (the first draw of each invocation carries ~200 s of XLA compile).

**‖g‖ falls as P^−0.500** over the whole 32× range — a pure-noise sum scales as P^−½, a signal-dominated one would
flatten at ‖μ‖. Fitting ‖g‖² = ‖μ‖² + N/P puts ‖μ‖² at −141, i.e. zero to the precision available. The gradient is
noise plus a component too small for this fit to see.

## Reading it

**1. Null through 1024; a real 0.026 at 2048.** Null sd = 1/√5997 = 0.0129. The cosine rises monotonically
(−0.022 → +0.026) and only the last point clears the null (2.0 sd); Spearman tracks it to within 0.011 throughout.
Fitting cos = P/(P+c) to the two positive points gives **c ≈ 76,000–108,000**, so the arm's pop 512 sits at cos
≈ 0.007 — half a null sd, unmeasurable — and **0.9 needs P ≈ 690,000, 0.95 needs P ≈ 1.45 M.**

**2. Not the harness.** `mean_win` at the centre reproduces the arm's gen-1 line (0.546–0.553 vs flow187's 0.5581),
the archetype probe reproduces its per-rung coins to ≤0.05 %, ‖g‖ is
100–130 (not zero), and the two seeds' ‖g‖ differ by 25 % — a sum dominated by its noise term.

**3. The ceiling is dimension, not noise.** The estimator sums m = P/2 antithetic pairs, so `g` lies in the span of m
random vectors inside an n = 5997-dimensional live subspace. Even with a *perfectly linear, noiseless* fitness,
writing εᵢ = zᵢu + wᵢ about the true direction u gives

    cos(ĝ, u) = 1 / √(1 + n/m)      and      cos(ĝ₁, ĝ₂) = m / (m + n) = P / (P + 2n)

(tabulated with the cost below; 4096 → 0.255.) At pop 512 the *best case* is 0.041 (3.2 sd), and even that ceiling
only reaches 0.9 at P ≈ 18n ≈ 108,000. The measured curve runs **~5× below the ceiling** (0.026 vs 0.146 at 2048), so
the fitness is not linear in ε at σ 0.02 either: dimension sets the wall, curvature and rank saturation take a further
factor of five.

**4. What the points can separate.** At P ≤ 256 the ceiling (≤0.021) is inside the noise, so those points prove
nothing alone. P = 512 (ceiling 3.2 sd) and 1024 (6 sd) discriminate, and both read zero — the component is *weaker
than the perfect-linearity ideal*, not merely under-sampled. The ten half-split readings (P/2 = 32…1024) average
+0.014 ± 0.005, agreeing with the two-seed column at the same P; implied cos(ĝ, truth) ≈ 0.16 at P = 2048.

## Cost

Post-compile the rate is flat at **0.32 s per member-generation** (~2.0 ms/episode with flow187 contending): linear in
P, no economies of scale. The arm's uncontended anchor is **57.3–62 s/gen at pop 512**
(`artifacts/flow187/train.log`), so

| P | 64 | 128 | 256 | 512 | 1024 | 2048 |
|---|---|---|---|---|---|---|
| gens/hour (uncontended, extrapolated from 57.3 s at 512) | 503 | 251 | 126 | **63** | 31 | 16 |
| ceiling cos | 0.005 | 0.011 | 0.021 | 0.041 | 0.079 | 0.146 |
| measured cos | −0.022 | −0.016 | −0.001 | 0.000 | 0.009 | 0.026 |

**Marginal value of doubling pop: +0.005 to +0.008 Spearman per doubling, on a number that is 0.015 at 2048.**
The product (ceiling cos) × (gens/hour) is constant at ~2.5 down the whole table,
because the accumulated signal-to-noise per unit *wall-clock* — √(G·m/n) over G generations — is **invariant to pop**.
Doubling the population buys exactly what halving it buys. Pop is not a lever on gradient quality; it trades step
count against step cleanliness at a fixed product.

## Recommendation

**Keep `--pop 512`. Change nothing.** Not because it is on a plateau — it is not — but because wall-clock
signal-to-noise is invariant to pop, so every alternative ties on the only axis that matters and 512 has 1,000+
generations of arms behind it. 1024 halves gens/hour (63 → 31) for a reproducibility still ≤0.08 in the best case and
0.01 measured; 128 quadruples gens/hour on steps individually 4× noisier, which under Adam's per-coordinate
normalisation is 4× the random walk in ‖θ‖ that `--weight-decay 1e-4` was added to flow187 to contain.

**Retire the "the estimator is fine, Spearman is 0.96" argument** (`2026-09-10-es-rate-A.md` "doubling pop or E buys ≤
0.03 Spearman", and review B's identical claim): both rest on an episode-split that cannot see perturbation-sampling
noise. The correct statement is *the ES gradient's reproducible fraction at pop 512 is ≤ 4 % of its energy in the best
case and measures 0 %; the arm advances by gate-filtered lottery, not by descending a gradient* — the same conclusion
the 2026-09-06 one-step audits reached from the other side ("no step beats random on fresh boards", memory
`es-noise-floor-2026-09-05`). This supplies the mechanism.

**The lever is dimension, not population.** cos(ĝ,u) = 1/√(1 + n/m) is symmetric in m and n: cutting the trained
subspace from 5997 to ~600 coordinates does at pop 512 what pop 5120 would do, for free. `--train-only` already is
that mask, and the one subspace tried (biases, 535 coords) lost −1.6k coins — but it was picked by hand, not by
measured gradient mass. **Next: rank the 5997 coordinates by |g| pooled over the ten draws already saved in
`~/popcurve/grads/`, keep the top ~600, re-run this same script under `--train-only` on them.** If the two-seed cosine
at 512 climbs from 0.00 toward its 0.30 ceiling, the ES has a gradient for the first time. Same script, ~15 minutes.

## Dead ends and assumptions

1. **159 episodes, not 160** — the arm's own count (147 pinned × 1 seat + 6 residual pairs);
   `--episodes 160` is the budget. Measured on the arm's whole batch, not the 147 pinned alone.
2. **The batch is frozen across all draws** (seeds, opponents, market draw, warm starts, seat
   rotation `t = 0`), so two draws differ in `eps` alone. The arm re-draws its 6 residual pairs
   each generation, so its own gen-to-gen reproducibility is if anything *lower* than this.
3. **`--chunk 4096`; the arm runs 8192.** Cost only, but the reduction order changes — the
   archetype probe reproduces the arm's per-rung coins to ≤0.05 % (124,902 vs 124,858), not
   bit-exactly. Irrelevant at the scale of these correlations.
4. **`--real-gate*` and `--keep-candidates` dropped** (engine workers; they touch neither `eps`,
   the fitness, nor the gradient). Everything else — rungs, weights, σ, lr, `--pinned-once
   --pinned-fixed-seed --shop-crn`, `--train-only all`, `--init-theta`, `--seed 289` — is the
   launcher's, parsed out of the launcher file itself.
5. **One seed pair per P** (sd 0.013): enough to test the ceiling at P ≥ 512, not to resolve
   0.01 between adjacent P — the 2048 reading is 2.0 sd and wants a second pair before it is leaned on.
   Correlations are over the 5997 live coordinates; the 6789 versions (`sp_seeds_all`) differ by ≤0.002.

**Dead ends.** `importlib.util.spec_from_file_location` + forcing `__name__` fails (`ImportError: loader for
kagg3_cli_main cannot handle __main__`): `scripts/train.py` keeps its whole body under `if __name__ == "__main__"`, so
it needs `runpy.run_path(..., run_name= "__main__")`. Rebuilding `cfg` by hand from `artifacts/flow187/config.json`
was rejected — it would re-derive rung weights, tape paths and flow scales, the exact drift this cannot afford. One
process per P (the original plan) costs 442 s of setup plus ~200 s of compile each time, more than the measurement: P
= 64 ran alone (end-to-end validation), 128–2048 in one process with the csv flushed after each P.

**Files.** `S/popcurve/popcurve.py` (reusable as-is for the `--train-only` probe above), `S/popcurve/analyse.py`,
`S/popcurve/results.csv` (raw, both runs merged; `results2.csv` is the 128–2048 run's own copy); per-draw gradients remote at `~/popcurve/grads/g_p<P>_s<seed>.npy`;
throwaway run dirs `~/stage_hr/artifacts/popcurve_probe{,2}/`.
