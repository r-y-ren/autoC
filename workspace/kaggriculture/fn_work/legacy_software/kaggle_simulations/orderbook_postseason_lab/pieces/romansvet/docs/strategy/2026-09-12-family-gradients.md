# Family gradients at candidate B: the six rung families do NOT pull in different directions

2026-09-12. **S/famgrad/** (`run.sh`, `run_b.sh`, `famgrad.py`, `analyse.py`,
`famgrad.md`, `famgrad*.json/npz`). Local RTX 3070, released on completion.

**Question (§94, §98, §101).** The ES objective is a weighted sum over six rung
families — w2 old band (85 rungs, ~1900-2100), LIVE-C 1-42 (42, 2300-2615), LOSS10
(10, 2175-2381), top-50 templates (9, ~2700+), top-ten (20, 2821-2954) and NEXT30
(30, 2550-2750). flow211 re-weights them (top-ten 32.7 → 10.0 %, NEXT30 0 → 38.2 %).
Do the families pull the gradient at B in different directions — i.e. is flow211 a
real A/B, or does it follow flow209's direction?

**ANSWER: aligned. The re-weighting is cosmetic in direction.** The true (noise-
corrected) cosine between flow209's and flow211's gradients at B is **0.93** — not
distinguishable from 1. No family pair anywhere in the matrix is significantly
negative; the top-ten family **opposes nothing**. The two genuine exceptions are the
two smallest families: **TOP50 (9 rungs, 4.5 %) is orthogonal to every other family**,
and **LOSS10 is orthogonal to W2 specifically**.

## 1. What was measured

At B (`submission/theta.npy` md5 `7fcf3948`), σ 0.01, pop 512 (256 antithetic pairs),
train-only subspace `gp,dh,ds,g5,gb5,w3,b3,b1` = 1,191 of 6,789 coordinates,
`--pinned-once --pinned-fixed-seed --shop-crn`, the flow211 ladder (196 pinned-town
rungs + 4 self-play episodes — the only ladder containing every family).

The ES advantage is `rank_normalise` of a per-episode **weighted mean**
(`es/train.py:584-668`), so the objective restricted to a family is the same estimator
with `ep_weight` zeroed outside it. **Every family gradient, flow209's weighted
gradient and flow211's weighted gradient therefore come from ONE rollout** — byte-
identical perturbations, boards, shops, seats and centre (true CRN, not merely a shared
seed). `FLOW211` reproduces the trainer's own `one_draw` gradient at cos `1.0000000`,
ratio `1.0000000`. Four independent perturbation seeds (9001-9004); the weight shares
printed by the rig reproduce §98's table to 0.01 pt.

**The trap, and the statistic that avoids it.** Cosines between two family gradients
*from the same draw* are inflated: both are `delta @ eps` through the same `eps`, so
they share the eps Gram's off-diagonal — exactly the artefact `sweep_c.py`'s permuted-
advantage control exists to catch. The same-seed matrix reads 0.06-0.93; it is
reported below as a diagnostic only. The artefact-free statistic is the **cross-seed**
cosine `S(F,G) = cos(g_F^s, g_G^s')`, s ≠ s' (6 seed pairs): the two draws share every
board, shop, seat and the centre but not the perturbation, so their noise is
independent. Its diagonal is each family's reproducibility r_F, and
`rho(F,G) = S(F,G)/sqrt(S(F,F)S(G,G))` estimates the cosine between the families' TRUE
gradients.

Null: SE per entry **0.018** (empirical, the spread of the 8 TOP50/LOSS10 off-diagonal
entries; the analytic isotropic null is 1/√1191 = 0.029 per seed pair). Reliability
ceiling at 256 pairs: ρ_dim = P/(P+d) = 256/1447 = **0.177** (§72's dimension-limited
reading — at flow209/flow211's real pop 4096 it would be 0.63).

## 2. The cross-seed cosine matrix S(F,G) — mean of 6 seed pairs, SE 0.018

|  | W2 | LIVEC42 | LOSS10 | TOP50 | TOPTEN | NEXT30 | FLOW209 | FLOW211 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **W2** | **0.092** | 0.068 | 0.004 | 0.020 | 0.054 | 0.080 | 0.086 | 0.089 |
| **LIVEC42** | 0.068 | **0.068** | 0.047 | 0.018 | 0.035 | 0.083 | 0.078 | 0.089 |
| **LOSS10** | 0.004 | 0.047 | **0.096** | −0.013 | 0.036 | 0.041 | 0.049 | 0.046 |
| **TOP50** | 0.020 | 0.018 | −0.013 | **0.075** | −0.002 | 0.004 | 0.025 | 0.018 |
| **TOPTEN** | 0.054 | 0.035 | 0.036 | −0.002 | **0.093** | 0.043 | 0.075 | 0.056 |
| **NEXT30** | 0.080 | 0.083 | 0.041 | 0.004 | 0.043 | **0.105** | 0.086 | 0.105 |
| **FLOW209** | 0.086 | 0.078 | 0.049 | 0.025 | 0.075 | 0.086 | **0.105** | 0.100 |
| **FLOW211** | 0.089 | 0.089 | 0.046 | 0.018 | 0.056 | 0.105 | 0.100 | **0.112** |

Diagonal = reliability (all 3.8-5.8 σ above zero, all ≈ 0.4-0.6 of the 0.177 ceiling —
the same 0.6 shortfall §98 measured for the full objective).

**Disattenuated `rho(F,G)` — the estimated cosine between the TRUE family gradients**
(SE ≈ 0.2-0.3; read as "near 1 / near 0", not as a point value):

|  | W2 | LIVEC42 | LOSS10 | TOP50 | TOPTEN | NEXT30 | FLOW209 | FLOW211 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **W2** | 1 | 0.86 | 0.04 | 0.24 | 0.59 | 0.82 | 0.87 | 0.88 |
| **LIVEC42** | 0.86 | 1 | 0.58 | 0.26 | 0.45 | 0.98 | 0.93 | 1.03 |
| **LOSS10** | 0.04 | 0.58 | 1 | −0.16 | 0.39 | 0.41 | 0.49 | 0.44 |
| **TOP50** | 0.24 | 0.26 | −0.16 | 1 | −0.03 | 0.05 | 0.29 | 0.20 |
| **TOPTEN** | 0.59 | 0.45 | 0.39 | −0.03 | 1 | 0.44 | 0.76 | 0.55 |
| **NEXT30** | 0.82 | 0.98 | 0.41 | 0.05 | 0.44 | 1 | 0.82 | 0.97 |
| **FLOW209** | 0.87 | 0.93 | 0.49 | 0.29 | 0.76 | 0.82 | 1 | **0.93** |
| **FLOW211** | 0.88 | 1.03 | 0.44 | 0.20 | 0.55 | 0.97 | **0.93** | 1 |

Same-seed (eps-shared, **inflated, diagnostic only**): W2·LIVEC42 0.57, W2·NEXT30 0.71,
TOPTEN·NEXT30 0.32, TOPTEN·TOP50 0.06, FLOW209·FLOW211 0.89. The inflation is uniform
and does not change any ordering — which is why the same-seed reading and the cross-seed
reading give the same verdict.

## 3. Gradient norms carry no information here

‖g_F‖ per seed: W2 54.2/55.7/55.1/55.0 · LIVEC42 52.0/47.6/50.3/50.7 · LOSS10
53.7/54.2/54.9/55.4 · TOP50 49.3/52.9/49.9/49.9 · TOPTEN 54.6/52.0/53.5/55.0 · NEXT30
55.2/59.0/54.6/55.5 · FLOW209 54.6/54.5/56.0/56.9 · FLOW211 55.2/58.2/56.7/57.9.

**All eight are the same to ±8 %.** `rank_normalise` puts every advantage vector on the
same fixed scale whatever the family, so ‖g‖ is set by the rank scale and the 256-pair
noise floor, not by how hard a family pulls. *A family's norm is not evidence of its
strength, and a re-weighting cannot be justified or refused on one.* The magnitude
information the raw margins carry is discarded before the gradient is formed.

## 4. Reading

* **The band families are one direction.** W2 (~1950), LIVEC42 (2460) and NEXT30 (2650)
  are mutually aligned at S = 0.068-0.083 against their own reliabilities of
  0.068-0.105 — i.e. **ρ 0.82-0.98, indistinguishable from identical directions**
  (W2·NEXT30 4.4 σ, LIVEC42·NEXT30 4.6 σ, W2·LIVEC42 3.8 σ). Opponent rating from 1950
  to 2650 does not change what the gradient in this subspace wants. This corroborates
  §95 (the judge is not band-dependent) and §99 (the NEXT30 opponent is the mistake-free
  clone, not a different play) from inside the objective.
* **Top-ten opposes nothing.** Its only non-positive entries are TOP50 −0.002 and
  nothing else; it is *positively* aligned with W2 (0.054, 3.0 σ, ρ 0.59), NEXT30
  (0.043, 2.4 σ), LOSS10 (0.036) and LIVEC42 (0.035, 1.9 σ). There is no
  "top-ten pulls one way, the band pulls the other" conflict to relieve. §101's finding
  — 22.7 points of objective mass on top-ten buy nothing against those opponents — is
  therefore **not** a conflict between families but an absence of a *separate* top-ten
  direction in this subspace: whatever the top-ten rungs ask for, the band rungs were
  already asking for.
* **The two exceptions are the two smallest families.** TOP50 (9 rungs) is orthogonal
  to everything (|S| ≤ 0.020, all ≤ 1.1 σ) — nine hand-picked new-template boards that
  agree with nothing else in the ladder. LOSS10's alignment with W2 is exactly zero
  (0.004) while it is positive with LIVEC42 (0.047, 2.6 σ) and NEXT30 (0.041) — a
  second, weak reading of the LOSS10 anatomy (a band clone on tomato-poor towns, not
  an old-band opponent). Together they carry 10.3 % of flow209's weight and 9.5 % of
  flow211's, too little to rotate either objective.
* **flow209's direction is not its heaviest family's.** flow209 puts 32.7 % on top-ten
  but its gradient is closest to LIVEC42 (ρ 0.93) and W2 (0.87), and only ρ 0.76 to
  top-ten. flow211's is closest to LIVEC42 (1.03) and NEXT30 (0.97). The weight share
  and the direction share are different things, because the aligned families outvote
  the heavy one.

## 5. Verdict

**ALIGNED — flow211 would follow flow209's direction.** cos(true g209, true g211) =
0.93 (cross-seed 0.100 against reliabilities 0.105 and 0.112 — the two objectives agree
as well as either agrees with itself). flow211 is **not** a direction A/B; it is a
*sampling* A/B — it buys 30 boards at 2550-2750 in-sample and, per §100/D1, must be
judged on the 14-board extension. If the reason to launch flow211 is "the ES is pointed
at the wrong band", this measurement says the premise is false: the band families
already point the same way, and flow211 will move B along the same ray flow209 is
already on, one third as fast on the top-ten component. If the reason is coverage of
the 2550-2750 hole in the *objective's support* (§92/§94), that reason survives —
but expect the g10-g30 records to look like flow209's, not different from them.

**Caveats.** (1) Local, at B, in the 1,191-gene train-only subspace, at pop 512; the
arms run at pop 4096 where the same directions are measured 2.5× more sharply, but the
true directions are a property of the objective and do not move with pop. (2) An
alignment at B says nothing about divergence after many steps. (3) The flow209
reconstruction uses flow211's 4 self-play episodes rather than flow209's 12
(0.32 % vs 0.96 % of weight — 0.6 pt, immaterial). (4) ρ > 1 for LIVEC42·FLOW211 is
sampling error in the denominator and should be read as "1".
