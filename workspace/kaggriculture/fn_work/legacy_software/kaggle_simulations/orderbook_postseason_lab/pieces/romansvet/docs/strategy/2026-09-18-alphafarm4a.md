# ALPHAFARM4A — the honest read-out says the distillation moves ~nothing, and moving more is worse

2026-09-18, branch `alphafarm`. [[rljudge2]] benched `af3_60` at POOLED450 **+149 t 2.59**, wins −3 net; the
diagnosis was *labels conflict* (S=4 shop streams, hard argmax). Both halves of the fix were built: **labels v2**
(running past this box) and an **advantage-weighted trainer with a score read-out** (done, on the 3,600 v1 labels).

## 1. Labels v2 — running on remote GPU1, PID 1703105, ETA 22:25Z

`S/alphafarm/run_labels_v2.sh`, `--board-src alljudge --K 8 --robust-select 8 --boards 511` (GPU0/`~/stage_dual`
untouched). New source `alljudge` in `search_probe.py`: EVERY pinned judge board once — BAND250 250 + BAND2 233 +
ENGINE28 28 = **511** — taking per opponent tape the ONE (seed, seat) row the judge actually ran with the **lower**
margin, so the seeds convention is the judge's own and no board is double-counted. S 4 → 8 doubles the drawn shop
worlds behind each candidate's mean. Cost is `nb*K*S`/dawn: 32,704 vs v1's 3,840 = **8.5x**. Measured: baseline
511 eps 325 s, dawn 0 968 s (compile), **dawn 1 293 s** ⇒ 28 dawns ≈ 137 min. Emission needed no change — the npz
already keeps *all* K per-purse means (`ours`, `theirs` [D, B, K]), so per-candidate `d_ours`/`d_theirs` are exact
differences against cand 0.

First two dawns vs v1's, same probe: cand-0 rate **0.49 / 0.94** (v1 0.47 / 0.93) — doubling the shop streams does
**not** collapse the edit rate, so "S=4 was too few" is not, on this evidence, why the labels conflicted. Mean
`gainA` is ~half v1's at matched dawns (2,249 / 187 vs 4,642 / 411), the direction the shop-luck-inflation
hypothesis predicts, but the board set also differs, so that half is not a clean comparison.

## 2. Trainer v2 (`distil.py`)

Target = softmax(margin_k / sd_dawn) **mixture** of the K candidate macros (`soft_jitter`), temperature = that
dawn's own score sd, so a dawn whose K are within noise yields ≈ the policy's own macro and no gradient (`bin_loss`
needs no change: same window, shifted, for a real target). Weight = `max_k margin_k − margin_0`; gift labels
(`d_theirs > 0` at the committed candidate) still dropped (16.2 %); 18 switch genes frozen; pre-`_qfloor` recording
patch untouched. **New read-out — held-out EXPECTED SCORE**: snap the fitted theta's macro to its nearest searched
candidate (L1 over plant/animal/crew/hire/land; `grow_mult` excluded, chaotic at 1e-4) and read that candidate's
**recorded** terminal margin, paired per dawn against cand 0 ⇒ a t. `--eval-theta` prices an existing theta so.

## 3. What it measures (v1 labels, 24 held-out boards / 720 dawns)

Ship **+7,929/dawn**, snap-to-cand0 1.000; depth-1 oracle **+8,538** ⇒ headroom **+609/dawn**.

| theta | Δscore/dawn | t | snap cand0 | snap dist | label acc |
|---|---|---|---|---|---|
| `af3_60` (benched, judge +149) | **−10** | −0.63 | 0.985 | 0.06 | 0.7124 |
| `af3_20` | −19 | −1.48 | 0.994 | 0.04 | 0.7189 |
| `af4_pre_40` (soft, `cd`, lr 2e-4) | **+12** | +0.69 | 0.985 | 0.05 | 0.7157 |
| `af4_pre_20` / `_60` | −23 / −21 | −1.67 / −1.83 | 0.990 / 0.982 | 0.04 / 0.05 | 0.717 / 0.714 |
| B: `cd`, lr 1e-3 | −5 | −0.37 | 0.981 | 0.11 | 0.6931 |
| C: 5 blocks, lr 1e-4 | **−52** | −1.70 | 0.978 | **1.94** | 0.5170 |

**(a)** Every fitted theta still plays the policy's own macro on **98 %** of held-out dawns (displacement 0.05
tiles): `cd` captures ~2 % of the headroom, and advantage weighting does not change that. **(b)** The dose-response
runs the **wrong way** — config C displaces 40x further and loses 52/dawn t −1.70. A theta that leaves the policy
macro lands on a *worse* candidate, because the searched edit is board-specific ([[planselect]], [[mpcfeas]]) and a
theta is not. **Caveat:** at se 13-17/dawn this cannot resolve a +149/board judge effect (it prices `af3_60` at −10
t −0.63). It is a **falsifier, not a gate**: it says only that no configuration captures a *large* share.

## 4. Verdict and hand-off

Advantage weighting alone does not unlock the labels; the binding constraint is the decode's board-blindness, not
label noise. Finish v2 anyway (only it can say whether S=8 over 4.3x the boards
shrinks the tie noise enough to move the snap distance), but the prior is now low, and price the score metric
BEFORE spending a judge leg ([[rljudge2]]'s lesson). Resume: `tail ~/stage_alpha/labels_v2.log`, rsync
`~/stage_alpha/S/alphafarm/labels_v2/af4lab.npz` back, then `JAX_PLATFORMS=cpu .venv/bin/python
S/alphafarm/distil.py --labels <npz> --fit-blocks cd --steps 60 --save-every 20 --tag af4`.
