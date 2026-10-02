# A/B of `--margin-scale` on the ES step's alignment κ (B's one-step rig)

2026-09-11. Question (B's §3.7/§4(iv) hypothesis): `--margin-scale 3000` saturates the sigmoid so the
shaped fitness ≈ the win bit; does the ES step's alignment κ to the true gradient improve when g is
computed with a larger scale? Scripts + raw output: `S/popcurve/B/msab.py`, `summarise_msab.py`,
`msab.json`, `msab.log`, `msab_summary.txt`, `rollouts/p512_s900{1,2}.npz` (the `mine`/`theirs` of
every member). Remote copy `~/popcurve/B/`. One foreground ssh, GPU0 shared with flow190, 1283 s.

**Verdict in one line.** No. Saturation at 3000 is real (28 % of member-episodes past ±9k, half the
sigmoid's resolution gone) but re-shaping the *same rollouts* at 30k / 100k / linear-margin moves the
ES direction by only 25-35° (cos 0.91 / 0.87 / 0.86 to the 3000 direction) and the moved part is not
better aligned: κ stays 0.00-0.016 in every cell, se 0.009, no scale separable from any other.
**Recommend no change to `--margin-scale` for flow191+**; the shaping is not where the 1 % alignment
comes from.

## 1. Design

Same rig as `onestep.py` (arm's own CLI via `popcurve.build_trainer/build_batch`, `_play`,
`shaped_advantage`, `fitness_bonus`; nothing re-implemented). Centre `flow172_g1000`, P = 512, seeds
9001 and 9002, ||d|| = 0.003·√5997 = 0.2323, the SAME 8 random ± control directions (`--rand-seed
777`, identical vectors to B's). The one change: each seed's antithetic population is **played once**
(`mine`, `theirs` for 512 × 159), and `shaped_advantage` is evaluated on those rollouts under
`margin_scale ∈ {3000, 30000, 100000, 1e7}` — 1e7 is the linear-margin limit (sigmoid slope 1.000,
i.e. rank-normalised mean coin margin). So the four gradients per seed differ *only* in the shaping.
Scoring: centre + 4 scales × 2 seeds × ±d + 16 randoms = 33 thetas, on the in-sample batch (147
pinned + 12 carried = 159 episodes) and held-out LIVE-C 43-72 pinned from both seats (60 games).
Evaluation metrics fixed: `obj_w` at the arm's 3000, `win_w`, raw `margin`. κ = antisym /
(sd of the 8 random antisyms · √n_live) = z/77.4, exactly as B. Pooled κ over two seeds has se 0.0091.

Reproduction of B: `||g||` 40.9129 / 39.2716 vs B's 40.9004 / 39.2552, cos to B's saved g = 0.9999.
Centre and 16 controls agree with B's `onestep.json` to within ONE game (in-sample win_w max diff
0.0073 ≈ 1/159, held-out 0.0167 = 1/60; margin ≤ 6 coins in-sample). The rig is not bit-exact across
batch sizes (33 vs 21 thetas → different chunk layout on a shared GPU); one flipped game is its floor.

## 2. The shaping itself (same rollouts, both seeds agree to 3 decimals)

| margin_scale | frac \|margin\|>3·ms | twins both saturated same side | mean sigmoid slope (1 = linear) | cos(g, g@3000) s9001 / s9002 | cos(g_9001, g_9002) |
|---|---|---|---|---|---|
| 3000 | **0.282** | **0.198** | 0.500 | 1 / 1 | +0.0001 |
| 30000 | 0.002 | 0.000 | 0.972 | +0.908 / +0.887 | +0.0095 |
| 100000 | 0.000 | 0.000 | 0.997 | +0.870 / +0.843 | +0.0125 |
| 1e7 (linear) | 0.000 | 0.000 | 1.000 | +0.862 / +0.834 | +0.0130 |

Median |margin| 5,209 coins, p90 16,660; 79 % of antithetic twins differ by > 1k coins. B's premise
holds: at 3000 a fifth of the pairs contribute ~nothing and the term carries half its resolution.
But 30k / 100k / linear are nearly the same direction as each other (cos 0.99-0.9997) and 0.83-0.91
from 3000: the shaping decides ≤ 15 % of the direction. Two-seed cosine rises 0.0001 → 0.013 with
scale (null sd 0.0129, z ≤ 1.0) — a hint, not a result, and not what the step test finds below.

## 3. Results — F(±d) − F(centre), antisym, z against the random antisym sd, κ

Random antisym sd (⇒ 2|∇F|·||d||): in-sample obj 0.0138 (1.07), win 0.0125 (0.97), margin 352
(27.3k); held-out obj 0.0299 (2.32), win 0.0657 (5.09), margin 690 (53.5k). Random symmetric
(curvature) mean: in-sample obj −0.0111, win −0.0228; held-out obj −0.0175, win −0.0677.

**IN-SAMPLE** (seed 9001 | seed 9002 | pooled κ)

| ms | obj +d / −d | antisym, z, κ | win +d / −d | antisym, z, κ | margin +d / −d | antisym, z, κ | pooled κ obj / win / margin |
|---|---|---|---|---|---|---|---|
| 3000 | −.0216/−.0295 ¦ −.0161/−.0153 | +.0079 z+.57 κ+.007 ¦ −.0008 z−.06 κ−.001 | −.039/−.051 ¦ −.042/−.037 | +.012 z+.95 κ+.012 ¦ −.005 z−.44 κ−.006 | −306/−763 ¦ −12/−314 | +457 z1.30 κ.017 ¦ +301 z.86 κ.011 | +.003 / +.003 / +.014 |
| 30000 | −.0076/−.0137 ¦ −.0092/−.0082 | +.0061 z+.44 κ+.006 ¦ −.0009 z−.07 κ−.001 | −.017/−.019 ¦ −.016/−.008 | +.002 z+.15 κ+.002 ¦ −.007 z−.58 κ−.008 | +377/−275 ¦ −121/−205 | +652 z1.85 κ.024 ¦ +83 z.24 κ.003 | +.002 / −.003 / +.014 |
| 100000 | −.0174/−.0165 ¦ −.0161/−.0091 | −.0009 z−.06 κ−.001 ¦ −.0071 z−.51 κ−.007 | −.022/−.027 ¦ −.044/**+.011** | +.005 z+.44 κ+.006 ¦ −.055 z−4.4 κ−.056 | +46/−524 ¦ −177/−334 | +570 z1.62 κ.021 ¦ +157 z.45 κ.006 | −.004 / −.025 / +.013 |
| 1e7 | −.0193/−.0131 ¦ −.0142/−.0107 | −.0062 z−.45 κ−.006 ¦ −.0035 z−.26 κ−.003 | −.034/−.024 ¦ −.046/+.003 | −.010 z−.80 κ−.010 ¦ −.048 z−3.9 κ−.050 | +4/−450 ¦ −152/−383 | +454 z1.29 κ.017 ¦ +231 z.66 κ.009 | −.005 / −.030 / +.013 |

**HELD-OUT LIVE-C 43-72, both seats (60 games; 1 game = 0.0167 win)**

| ms | obj +d / −d | antisym, z, κ | win +d / −d | antisym, z, κ | margin +d / −d | antisym, z, κ | pooled κ obj / win / margin |
|---|---|---|---|---|---|---|---|
| 3000 | −.0073/−.0435 ¦ −.0124/−.0176 | +.0362 z1.21 κ.016 ¦ +.0052 z.18 κ.002 | −.033/−.100 ¦ −.067/−.067 | +.067 z1.01 κ.013 ¦ 0 z0 κ0 | −241/−1055 ¦ −449/−717 | +814 z1.18 κ.015 ¦ +267 z.39 κ.005 | +.009 / +.007 / +.010 |
| 30000 | −.0103/−.0413 ¦ −.0006/−.0321 | +.0310 z1.03 κ.013 ¦ +.0315 z1.05 κ.014 | −.067/−.083 ¦ −.033/−.067 | +.017 z.25 κ.003 ¦ +.033 z.51 κ.007 | −256/−1128 ¦ +90/−708 | +872 z1.26 κ.016 ¦ +798 z1.16 κ.015 | **+.014 / +.005 / +.016** |
| 100000 | −.0429/−.0439 ¦ −.0323/−.0361 | +.0010 z.03 κ.000 ¦ +.0038 z.13 κ.002 | −.100/−.100 ¦ −.100/−.067 | 0 z0 κ0 ¦ −.033 z−.51 κ−.007 | −455/−1162 ¦ −367/−759 | +708 z1.03 κ.013 ¦ +392 z.57 κ.007 | +.001 / −.003 / +.010 |
| 1e7 | −.0351/−.0405 ¦ −.0232/−.0344 | +.0055 z.18 κ.002 ¦ +.0112 z.37 κ.005 | −.100/−.100 ¦ −.100/−.067 | 0 ¦ −.033 z−.51 κ−.007 | −284/−1059 ¦ −191/−736 | +775 z1.12 κ.015 ¦ +545 z.79 κ.010 | +.004 / −.003 / +.012 |

Curvature (symmetric part, mean of both seeds, z vs the 8 random symmetric parts): in-sample obj
3000 **z −2.1** (B's "brittle direction" finding, reproduced), 30000 z +0.3, 100000 z −0.8, 1e7
z −0.7; in-sample win 3000 z −2.1, 30000 z +0.8. Held-out obj: 3000 z −0.4, 30000 z −0.5, 100000
**z −2.9**, 1e7 z −2.2 — the linear-ish shapings buy the brittle direction *out of sample* instead.

## 4. Reading

1. **κ does not rise with margin_scale.** Pooled κ on obj: in-sample +0.003 / +0.002 / −0.004 /
   −0.005, held-out +0.009 / +0.014 / +0.001 / +0.004 (3000 / 30k / 100k / linear); se 0.009 each.
   Nothing reaches B's resolution floor 0.031; no pair of scales differs by > 1.2 se on any metric.
2. **The coin signal stays 8/8-positive at every scale and never grows.** margin κ pooled: in-sample
   0.014 / 0.014 / 0.013 / 0.013, held-out 0.010 / 0.016 / 0.010 / 0.012. It is a property of the
   step (it is the same direction to cos 0.83-0.91), not of the shaping — training on the coin
   margin (1e7) does not raise the coin-margin alignment one bit.
3. **30000 is the least-bad cell, not a winner.** In-sample its +d/−d lose 2-3x less than 3000's
   (obj −0.008/−0.014 vs −0.022/−0.029) and its curvature is *random-like* (z +0.3 vs −2.1), and
   held-out it is the only cell with both seeds' antisym positive on all three metrics (pooled κ
   0.014 / 0.005 / 0.016). But every one of those κ is within 1.5 se of 3000's, and 100k/linear —
   which are the same direction as 30k to cos 0.99 — do not share the held-out pattern, which says
   the 30k cell's edge is the one-game lottery (its held-out win antisyms are 1 and 2 games).
4. **The one z beyond ±3** (in-sample win, seed 9002 at 100k and 1e7: −d *gains* +0.011 / +0.003,
   antisym −0.055) is a single direction where stepping *against* the coin-shaped gradient wins
   ~1.7 games in-sample while losing held-out (−0.067) — the in-sample/held-out mismatch of §3.5 in
   B, not a signal for the linear shaping.
5. Saturation at 3000 is a measured fact (28 %, 20 % dead twins, half the slope) and the docstring's
   argument for 100k is right *about the fitness function*; it is simply not the bottleneck. With
   κ ≈ 0.01 from all four shapings, the alignment is set upstream — by the 512-member estimate of a
   5997-dimensional gradient on 159 episodes — exactly as B's §1 dimension argument says.

## 5. Recommendation

**No change to `--margin-scale` for flow191+.** If a scale change is wanted for other reasons
(resolution inside wins, the docstring's own case), 30000 is safe — it keeps 99.8 % of pairs
unsaturated, and nothing here shows it hurts — but it must be sold as hygiene, not as a κ lever: the
measured κ gain is +0.005 ± 0.013 held-out and −0.001 ± 0.013 in-sample. The lever B priced from
measurement (lr 0.003 → ~0.001) stays the only one with evidence; this A/B does not touch it.

## 6. Dead ends recorded

* **"Saturation → win bit → lost coin signal → low κ."** First two links measured true, third false:
  re-shaping the same rollouts changes ≤ 15 % of the direction and none of the alignment. Do not
  re-run this at other scales; the four here span the whole range from half-saturated to linear.
* **Two-seed cosine rising 0.0001 → 0.013 with scale.** z ≤ 1.0 against the 1/√n null, and the
  direct step test contradicts it. Same lesson as B §5: the cosine is the wrong instrument.
* **`frac_pair_drel_lt_1e3` at 1e7 = 0.995** in `msab.json` is an artefact of the absolute 1e-3
  threshold at slope 1/4e7 (rank normalisation is scale-free); ignore that column for that row.
* **Bit-exactness across batch sizes.** 33-theta vs 21-theta batches on the shared GPU differ by
  one game per set; any future cell-vs-cell claim below one game (0.0063 in-sample, 0.0167 held-out
  win) is noise. Baseline 3000 was re-run rather than reused for this reason.
