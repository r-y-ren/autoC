# DITHER + flip-budget sigma: both remedies STAGED, neither run

2026-09-11, agent, 75-minute box, CPU only (the local 3070 is the E3 one-step test's;
nothing was launched on it). New files: `S/dither/` (patches, tests, solver, runners).
`git diff --stat src/` **empty**; both patches are **unapplied** and live only in
`S/dither/*.patch` and in the private tree `/root/tree_dither`.

Reads: consensus §71, `docs/strategy/2026-09-11-web-es-floors.md` §1-§2 and §7 #1/#2,
`docs/strategy/2026-09-11-tie-census.md`, `S/ties/census.json`, `S/ties/brain.patch`,
`S/onestep/run_local_c.sh`, `S/onestep_b/run_main.sh`.

---

## 1. What the two remedies are, in one line each

* **Remedy 1 — DITHER.** Replace `floor(x)` in the decode by `floor(x + u)`,
  `u ~ U(0,1)`, during **fitness evaluation only**. `E_u[floor(x+u)] = x` exactly
  (non-subtractive RPDF dither: Lipshitz/Wannamaker/Vanderkooy, JAES 40(5) 1992), so the
  staircase the ES samples becomes a **ramp in expectation** while every decoded value
  stays an integer the engine can play. This is not the soft decode the tie census §6
  rejected: no backward pass, nothing unplayable, and the shipped `floor(x)` is the
  `u → 0` member of the training mixture.
* **Remedy 2 — per-block sigma.** Stop controlling `||sigma*eps||` and control the
  **flip budget** `E[cells] = sum_j P(tie j crosses)` at 1-2 per decision instead of 34,
  with one sigma per `PO.SHAPES` block so the 2,000x spread of decode gradients does not
  let the coin-scaled heads eat the whole budget.

## 2. Remedy 1 — `S/dither/brain_dither.patch` (383 lines, 255 added, md5 c1242d5e)

Against the tree candidate B was trained in (`S/localarm/tree`, brain.py md5 d02fcd7d =
`.claude/worktrees/arms-next`). Applied only to the private copy `/root/tree_dither`
(`S/dither/stage_tree.sh`).

**Env-gated.** `KAGG3_DITHER=<seed>` turns it on; `KAGG3_DITHER_SITES` (default
`floors,blocks`) selects the kinds:

| kind | sites | treatment | unbiased? |
|---|---|---|---|
| `floors` | the 16 `_qfloor` calls (55 scalar entries) | `floor(x - half + u)` | **yes, exactly** |
| `blocks` | the two `_largest_remainder` calls | randomised (systematic) apportionment | **yes**, and the sum is preserved exactly |
| `ranks` | the 8 `argsort` leftover keys | Gumbel-max on `log(frac)` (Plackett-Luce) | only for `left == 1` — ablation, mutually exclusive with `blocks` |
| `absorb` | the 5 `absorb` thresholds | logistic noise, scale `KAGG3_DITHER_ABSORB_SCALE` | **no** — a threshold has no quantum, so this is a deliberate relaxation; **off by default** |

`land_ok` needs no separate treatment: it is a comparison on `land_frac`, whose floor is
already dithered.

**The three load-bearing details.**

1. **CRN.** `u` is a pure function of `(dither seed, decision site, day, component)` —
   `_dither_u(xp, site, day, shape)` takes **no theta**, no member, no pair, no episode
   and (by default) no board. So the `+eps` and `-eps` members of an antithetic pair see
   the *same* dither field, on every episode they play; a fresh `u` per member would be
   new evaluation noise stacked on the shop re-roll and would destroy the pairing.
   Independence *within* one fitness number comes from the day and the site: 16 floor
   calls x 30 days x 2 seats of independent draws stand behind one game, which is what
   makes the measured fitness an estimate of the **smoothed** objective rather than of one
   shifted staircase. (`KAGG3_DITHER_KEY_BOARD=1` adds a board word, trading a little CRN
   for more averaging; the default is the stricter key the brief specified. The trainer
   cannot hand the decode a *pair index* without plumbing a new field through
   `rollout.episode`; omitting it makes the CRN strictly **stronger** — the field is
   shared by the whole population, not merely by the pair.)
2. **The apportionment is dithered as a BLOCK.** `plant_target` must sum to
   `n_dev - sum(animal_want)`; five independent floors would break that. Systematic
   apportionment applies ONE `u` to the *cumulative* shares:
   `n_i = floor(c_i + u) - floor(c_{i-1} + u)`, `c_i = total * cumsum(w)_i / sum(w)`,
   giving `E[n_i] = total*w_i` and `sum_i n_i = floor(total+u) - floor(u) = total` for
   **every** draw.
3. **`forward_days` is a ROUND, not a floor** (`_qfloor(16*fwd + 0.5)`). Dithering a round
   means *replacing* the 0.5 with `u`, not adding to it — hence the `half=` argument. Get
   this wrong and the horizon decodes half a day high.

**Inert when unset — measured, not argued.** Every dither is a Python branch taken at
trace time and the untaken branch is the original expression character for character
[LAW]. `S/dither/macro_dump.py` decodes B's `Macro` on **4 boards x 30 days x 2 seats =
240 decisions, 42 integers each**, in the patched tree with `KAGG3_DITHER` unset and in
the pristine tree: **identical, 0 of 10,080 integers differ.**

### Unit tests — `S/dither/test_dither.py` (ALL PASS, ~40 s CPU)

```
JAX_PLATFORMS=cpu .venv/bin/python S/dither/test_dither.py --tree /root/tree_dither
```

| test | result |
|---|---|
| `E[floor(x+u)] - x`, x = 0.1 | 1e4 draws: **-1.0e-4** (MC se 3.0e-3) · 1e6: **-3.1e-4** |
| x = 6.9913 (`animal_count` at B) | 1e4: **+2.1e-3** (MC se 9.3e-4) · 1e6: **+2.4e-5** |
| x = 28.686 (`n_dev` at B) | 1e4: **+1.0e-4** (MC se 4.6e-3) · 1e6: **-5.2e-4** |
| round site (`half=0.5`), x = 2.42 / 3.5 / 0.2 | E = 2.4157 / 3.4966 / 0.1993 (undithered round: 2 / 4 / 0) |
| block sum preserved | **6,000 draws, 0 bad**; counts never negative |
| block unbiased, w = (.41,.33,.17,.06,.03), total 11 | E = (4.510, 3.630, 1.869, 0.663, 0.327) vs want (4.51, 3.63, 1.87, 0.66, 0.33); support = 5 distinct plans, the deterministic one among them |
| gumbel ablation sum preserved | 2,000 draws, 0 bad |
| CRN: same key -> same u | bit-identical; different day / site / component all differ; 15 sites x 3 days all distinct |
| numpy `u` == jax `u` | equal on 15 sites x 30 days; traces through `jit` and `vmap` |
| unset -> bit-identical decode | 240 decisions x 42 ints identical |

**Note on the 1e-3 bar.** At 1e4 draws the Monte-Carlo standard error of the mean is
`sqrt(f(1-f)/n)` = 3.0e-3 at x = 0.1 and 4.6e-3 at x = 28.686 — *larger* than the 1e-3
bar, so the bar is only meaningful at 1e6 draws, where all three pass. The test reports
both and gates 1e4 at 3 MC se.

## 3. Remedy 2 — the flip-budget sigma (`S/dither/blocksigma.py`, `sigma_blocks.npy`)

Per-tie, per-block decode gradients `g_{j,b}` recomputed with the census instrument
(`sqrt(sum_b g_{j,b}^2)` reproduces `S/ties/census.json`'s `gnorm` to 2.7e-16).

**The web doc's formula is wrong by up to 2x.** `2*Phi(-gap/s)` puts both walls at `gap`;
for a floor the near wall is at `gap` and the far one at `1 - gap`. Kind-aware:

| scalar sigma | `2Phi` shorthand | exact | census **measured** |
|---|---|---|---|
| 0.02 | 36.71 | **32.73** | 33.91 |
| 0.005 | 29.69 | **25.16** | 24.98 |

The exact form is what was solved with (floor: `Phi(-gap/s) + Phi(-(1-gap)/s)`; absorb
one-sided; rank keys `2Phi`). 62 of 68 ties are usable; the 6 excluded are the
zero-gradient ones (`press[0,2,3,6,7]`, `animal_defer`), which can never cross.

**Principle** (stated so it can be argued with): `G_b = sqrt(mean_j (g_{j,b}/gap_j)^2)`,
`sigma_b = min(c/G_b, 0.02)`, with `c` bisected to `E[cells] = 2` (c = 9.34e-2) and
`= 1` (6.65e-2). The 0.02 cap is today's training sigma and is how the 7 blocks that are
**dead at this obs** (`g3, gb3, g4, gb4, fh, fs, fv`) are treated; it also binds on 4
near-insensitive live blocks (`g7, gb7, g10, gb10`).

| block | n | G_b | sigma@2 | | block | n | G_b | sigma@2 |
|---|---|---|---|---|---|---|---|---|
| w1 | 2304 | 3986 | 2.34e-5 | | g8 | 128 | 567 | 1.65e-4 |
| gp | 864 | 772 | 1.21e-4 | | dh | 128 | 1817 | 5.14e-5 |
| g1 | 768 | 692 | 1.35e-4 | | w2 | 128 | 2743 | 3.41e-5 |
| g2 | 576 | 307 | 3.04e-4 | | g10 | 128 | 1.42 | 2.0e-2 (cap) |
| fh/fv/g3 | 512/384/288 | dead | cap | | g5 | 96 | 23.4 | 4.00e-3 |
| | | | | | gb5 | 3 | 10.9 | 8.60e-3 |

**Verification, 64 fresh draws at the budget-2 sigma** (the falsifier of the closed-form
solve): floor cells crossed **1.33 (sd 1.02)** of 55 against the closed form's 1.46 —
inside one sd. `Macro` integers changed **0.95** of 42 (scalar sigma 0.02: 27.4), and
**37.5 % of members decode B's `Macro` exactly** against **0/64** at sigma 0.02. The
budget is a real handle on the cell count.

### The headline: the flip-budget step is INSIDE the "behaviourally B" shell

`||sigma*eps||` at budget 2 / budget 1: **0.045 / 0.032** over the blocks the budget
actually binds (live, uncapped); 0.261 / 0.259 including the capped live blocks; 0.752 /
0.751 over the whole vector, the remainder sitting entirely in blocks with zero or
near-zero decode sensitivity at this obs — norm that moves theta without moving the plan.

The brief's "alpha 0.03 shell is `||Delta theta|| ~ 0.007`" is **not** what the
falsifier records: `docs/strategy/2026-09-11-alpha-falsifier.md` line 97 says **0.026 -
0.085** on `||B|| = 18.1`, where every record reads Delta ~ 0 (-30…+47 coins, |t| <= 0.9,
0-2 board flips) because "a 0.03-scaled step is behaviourally B". **0.045 and 0.032 are
inside 0.026-0.085.** So, plainly:

> **The sigma that keeps the plan intact is the sigma that does nothing.** A step short
> enough to cross 1-2 decode cells has the norm of a step §62 measured as behaviourally
> indistinguishable from B, and a step long enough to change behaviour crosses ~34 cells
> and draws a fresh plan. **ES over this parameterisation is closed by the literature's
> own bound** (Hamano/Uchida/Shirakawa 2026's `p_succ = (1-p_mut)^{d_in}`), unless the
> DECODE is changed — which is exactly what remedy 1 does, and why the dither arm, not the
> sigma arm, is the one worth the card.

The sigma solve remains worth running as the **control**: if the dither also reads
Delta ~ 0, the two together say the objective, not the step, is the constraint.

**Caveat for any launch** (from the tie census §7 step 0): these radii are ONE obs on a
day-0 board where 3,241 genes are dead, and the 11 capped blocks are an artefact of that.
Re-run the solve over a day x board panel before an *arm* is cut on it. The one-step test
is unaffected — it is measured at the same day-0-seeded centre.

`S/dither/train_blocksigma.patch` (47 lines, md5 f333b456, unapplied, `git apply --check`
clean): `sigma_blocks(n)` next to `perturbations`, `self.sigma_vec` in `Trainer.__init__`,
and two lines in `generation()` folding the vector into `eps` **before** the scalar
multiply, so the perturbation and the gradient contraction stay on the same vector.
Unset `KAGG3_SIGMA_BLOCKS` -> `None` -> today's behaviour bit-identical. **The trainer has
no per-block sigma today**: `src/kagg3/es/train.py:3749-3750` perturbs with a Python float
`self.sigma` (`Config.sigma` :211, `scripts/train.py:1217`), divides by `cfg.pop *
self.sigma` at :3786, and `perturbations()` (:410) takes no scale; `S/onestep/sweep_c.py`
(`grad_from_adv`, :111) is scalar too.
**Consequence for the runner:** the vector multiplies `eps` and the scalar multiplies the
product, so `--sigmas 1.0` is mandatory in blocksigma mode or the effective sigma is
scaled twice.

## 4. The staged test (NOT run)

`S/onestep/run_local_c.sh`'s recipe and guards, against the private patched tree, writing
only into `S/dither/` (it never touches `sweep_c.json`, `thetas_c/` or any other agent's
outputs). Phase 1 is the GPU estimator (`S/onestep/sweep_c.py`), phase 2 is the CPU
read-out on both families **with the same treatment** — a theta selected under the dither
and read out undithered is scored on a different objective. Phase 2 uses
`S/dither/screen_dither.py`, regenerated from `S/simscreen/screen.py` at stage time with
its `WORKTREE` line pointed at the patched tree (`S/simscreen` is never edited).

Staging also runs the self-check before the card is touched: `stage_tree.sh` re-applies
the patch to a fresh copy and `test_dither.py` must pass, **including the unset-inertness
leg**, or the runner refuses.

```
nohup setsid bash /mnt/e/_work/kaggriculture3/S/dither/run_onestep_dither.sh      >/dev/null 2>&1 &
nohup setsid bash /mnt/e/_work/kaggriculture3/S/dither/run_onestep_blocksigma.sh  >/dev/null 2>&1 &
nohup setsid bash /mnt/e/_work/kaggriculture3/S/dither/run_onestep_combined.sh    >/dev/null 2>&1 &
```

One at a time — each takes the whole card, and the guard refuses while an ES arm or
another one-step driver holds it (`FORCE=1` overrides, `DRYRUN=1` prints the plan,
`PHASE=sweep|screen|both`, `POPS=512,2048` adds the second population).
Defaults: sigma **0.02** (dither) / **1.0** with the vector (blocksigma), **P 512**,
alphas **1.0, 0.1, 0.03**, **8 randoms + 4 permuted**, eps-seed 9001, hold-out on,
`KAGG3_DITHER=20260911`, `KAGG3_DITHER_SITES=floors,blocks`.

**Wall time**, from the E3 measured constants (build 390 s, draw 525 s/pop, 0.30 s/theta
in-sample, hold-out 880 s + 0.12 s/theta; screen 0.41 s/episode/process, episodes =
thetas x boards, families in parallel): 79 thetas per cell ->
**sweep 0.51 h (GPU) + screen 1.09 h (CPU) = ~1.6 h** per treatment at P 512;
**~2.3 h** with `POPS=512,2048`. Three treatments back to back: ~5 h.

### PRE-REGISTERED BAR (fixed here, before any run)

**PASS** requires all three, at alpha **0.1 or 0.03** (alpha 1.0 is diagnostic only — the
E3 audit read the cliff there):

1. **kappa >= 0.03** — i.e. >= 3x the 0.004-0.011 the unpinned E3 sweep measured at this
   same centre (`S/onestep/kappa.py`, `z = antisym/sd(randoms)`, `kappa = z/sqrt(n_live)`);
2. **+d beats >= 12 of the 16 random +/- control thetas** on Delta-margin vs B, **on both
   families of the CPU read-out** (LIVE-C 120 and TOPB2 40) — the tie census's bar, which
   the g940 positive control cleared 16/16;
3. **+d beats ALL 4 permuted-advantage controls**, and the gain is **antisymmetric**
   (`Delta(+d) ~ -Delta(-d)`): a one-sided gain is curvature or a lottery, not a gradient.

**NO-GO**: kappa <= 0.015, or +d still loses. That falsifies "the ties are the binding
constraint" for the treatment tested; after a NO-GO the next move is a changed objective
(§6 of the web doc: race the 12 coarse integers directly), **not** a changed sigma.
A PASS must be replicated at `EPS_SEED=9002` before an arm is cut on it, and any theta
trained under either treatment must be replayed **undithered / unscaled** for every judge
leg — the existing promotion rule, unchanged.

## 5. Standing

* `git diff --stat src/` empty. Both patches unapplied. Nothing launched; the card was
  never touched; no judge lock, no engine leg, no ssh.
* Files: `S/dither/{brain_dither.patch, train_blocksigma.patch, sigma_blocks.npy,
  blocksigma.py, blocksigma.json, test_dither.py, macro_dump.py, stage_tree.sh,
  screen_stage.sh, run_onestep.sh, run_onestep_{dither,blocksigma,combined}.sh}`.
  Private tree: `/root/tree_dither` (rebuilt by `stage_tree.sh` on every run).
* md5: brain_dither.patch c1242d5e, train_blocksigma.patch f333b456,
  sigma_blocks.npy 8c700604.
