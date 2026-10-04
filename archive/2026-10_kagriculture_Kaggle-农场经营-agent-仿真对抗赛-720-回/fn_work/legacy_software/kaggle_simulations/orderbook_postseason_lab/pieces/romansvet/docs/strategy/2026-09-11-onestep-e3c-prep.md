# E3c prep — the one-step rig with a step-length axis and a permuted-advantage control

Prepared 2026-09-11 (prep agent, CPU only; **nothing launched** — the 3070 was still finishing
E3's σ 0.04 block, and the local ES arm flow198 resumes after it). Staged files:
`S/onestep/sweep_c.py`, `S/onestep/run_local_c.sh`, `S/onestep/test_sweep_c.py`, and the
"E3c (sweep_c.py)" section of `S/onestep/README.md`. Nothing that the running E3 sweep reads or
writes was touched (`sweep_b.py`, `run_local.sh`, `run_local.log`, `sweep_b.json`, `thetas/`,
`grads/`); `git diff --stat src/` is empty.

## 1. What the audit left the rig unable to answer

`docs/strategy/2026-09-11-e3-step-audit.md` (consensus §56) closed three questions about E3's
σ 0.01 cell — the sign is correct, the step is not concentrated, and the **collapse is a
step-scale artefact** — and in doing so disqualified the instrument as it stands:

* **(a) One length is not a reading.** At `R = lr·√n_live = 0.2323` the step loses 16.6 k coins;
  the *same* direction at α 0.1 / 0.03 gains (+140 / +111 on LIVE-C, +286 on the second leg) and
  beats its own mirror on both legs (antisym +396 / +289 LIVE-C, +915 TOPB2). `R` is an *Adam*
  displacement; with β1 = 0.9 one draw contributes ~10 % of it. Every E3 cell is therefore read
  at ~10× the length one generation actually moves, and both branches of the §6 rule are
  unreachable: the cliff dominates `+d` at every σ, and it is not a property of σ.
* **(b) The null is wrong.** ‖g₅₁₂‖/‖g₂₀₄₈‖ = 1.998 ≈ √4 and cos = 0.53 ≈ √¼ — the draws are
  sampling noise at both pops. An isotropic random of length `R` puts ~1/√5997 of itself on the
  axis the population's fitness spread is about; `d` puts all of it there. The randoms calibrate
  the sd of the antisym statistic and nothing else, so "`+d` beat 0/16 randoms" is not evidence
  of a downhill gradient. κ has no interpretable null until a control shares the ε span.
* **(c) The audit's own prescription** (§5.4): "Add the missing control before any arm is re-cut
  on a κ: a direction built from the same ε rows with the advantages permuted."

## 2. The control

One draw gives `eps` [P/2 × n] and the shaped advantages `adv` [P] (antithetic: `adv[i]` and
`adv[half+i]` are the ± halves of ε row `i`). The arm's estimator is one line
(`S/popcurve/popcurve.py::one_draw`):

```
delta[i] = adv[i] - adv[half+i]
g        = delta       @ eps / (pop * sigma)
g_perm   = delta[pi]   @ eps / (pop * sigma)      # pi permutes the PAIR index
```

Permuting the **pair** index (not the 2P samples) keeps each paired difference intact and only
changes which ε row it is charged to. So `g_perm` has: the same estimator, the same ε rows, the
same |adv| multiset, the same length — and no pairing between a perturbation and the fitness
difference it caused. It is the exact null "an aggregate of these ε rows with these advantage
magnitudes, but no selection".

Measured on synthetic data at the rig's size (n 6,789, pop 512, `S/onestep/test_sweep_c.py`):
‖g_perm‖/‖g‖ = **1.007 ± 0.008** over 200 permutations (max deviation 3.1 %), |cos(g_perm, g)|
≤ 0.12. At the toy size the brief specified (n 50, pop 8) the ratio scatters ±20 % (exhaustive
4! ensembles over six seeds: mean 0.88–1.10, range 0.77–1.32) — with 4 pairs, ‖eps_i‖ itself
varies ~10 %, so the 5 % concentration is a large-(n, P) property and the test asserts it only
where the rig runs. The identity permutation reproduces `one_draw`'s gradient **bit for bit**
(max |Δ| = 0.000e+00 at both sizes), which is what licenses reading the two side by side.

Each cell also stores `adv_<cell>.npy`, `pairs_<cell>.npy` and `perms_<cell>.npy` so any further
control (a different permutation, a bootstrap, a rank re-shuffle) can be built offline on CPU
from the same draw; the run itself checks that the saved advantages rebuild the draw's own
gradient (`adv_rebuild_cos`, `adv_rebuild_norm_ratio` in the json) and prints a WARN + marks the
cell void if they do not.

## 3. The rig

| axis | E3 (`sweep_b.py`) | E3c (`sweep_c.py`) |
|---|---|---|
| step length | `R` only | `α·R`, α ∈ {1.0, 0.1, 0.03}; randoms **rescaled**, never re-drawn |
| controls | 8 isotropic randoms ± | the same 8 (bit-identical at α 1.0) **+ 4 permuted-advantage directions per cell** |
| per-cell report | F(c), ±d, antisym, rand sd, z, κ, rand<+d | the same **per α**, plus the perm family's antisym mean/sd, z, κ, and both rank counts (`a>r` of 8, `a>p` of 4) |
| default cells | σ {0.01, 0.02, 0.04} × P {512, 2048} | σ {0.01, 0.02} × P {512, 2048}; σ 0.04 only if `SIGMAS` says so |
| outputs | `sweep_b.json/.txt`, `thetas/`, `grads/` | `sweep_c.json/.txt`, `thetas_c/`, `grads_c/`, `adv_c/` — schema-compatible (the α-1.0 labels are sweep_b's, `stats()` called with sweep_b's signature returns sweep_b's dict) |

Everything else is held fixed and unchanged: the centre (candidate B `flow193_g100_hr`, md5
7fcf3948, LIVE 56161192), the flow193 launcher argv with only `--init-theta`/`--sigma` swapped,
the CRN batch, eps seed 9001, rand seed 777, the 159-episode in-sample block and the LIVE-C
43-72 hold-out played pinned from both seats. Nothing is re-implemented: `perturbations`,
`shaped_advantage`, `_play`, the ladder and the objective all come from the arm's own tree.

## 4. The decision rule (fixed before the run)

A cell **PASSES** only if, at **some α ≤ 0.1**, on the **hold-out** block:

1. `+αd` gains on **both** `obj_w` and `margin`, **and**
2. its antisym beats **≥ 6 of the 8** random pairs, **and**
3. its antisym beats **all 4** permuted-advantage directions.

(2) without (3) is **not** a pass — that combination says the reading is the ε-span aggregate,
not selection, and it is the reading the audit predicts if the cliff (and not a gradient) is
what the rig has been measuring. A **FAIL** verdict may **not** be recorded from α 1.0 alone.
A PASS is replicated at `EPS_SEED=9002`, then confirmed in the engine (`judge.sh` + `kappa.py`
on paired margins) **at the same α**, before an arm is re-cut on it.

Reading guide for the three α at once: α 1.0 is the audit's cliff (expect `+d` to lose at every
σ — diagnostic only, and its *depth* is a proxy for how much of the step lands on the sensitive
axis); α 0.1 is the honest model of one generation's displacement; α 0.03 is the linear-response
check — if the antisym scales roughly linearly from 0.03 to 0.1 and collapses at 1.0, the
direction has a real first-order term and the rig has been reading curvature.

## 5. Cost and launch

109 scored thetas per σ block (vs 21), which is **thetas, not draws** — the permuted directions
re-use the draw already paid for. From E3's measured timings (build 325/457 s, draws
382/423/869/423 s, in-sample 21 thetas in 6.2 s, hold-out block 827/975 s): **~2,370 s per σ
block, ~4,730 s ≈ 1.31 h for σ {0.01, 0.02}** on the 3070; σ 0.04 adds ~40 min.

```bash
JAX_PLATFORMS=cpu python S/onestep/test_sweep_c.py     # CPU unit test, ~2 s
DRYRUN=1 bash S/onestep/run_local_c.sh                 # plan, guards, wall-time estimate
nohup setsid bash /mnt/e/_work/kaggriculture3/S/onestep/run_local_c.sh >/dev/null 2>&1 &
```

The launcher refuses while a `scripts/train.py --run flow*` arm is alive, while another
`sweep_b/sweep_c` driver holds the card, or while > 2,500 MiB is in use (`FORCE=1` overrides) —
**the local arm (flow198 resume) outranks this probe**; E3c goes on the card only in a gap, or
on the remote host with the same argv.
