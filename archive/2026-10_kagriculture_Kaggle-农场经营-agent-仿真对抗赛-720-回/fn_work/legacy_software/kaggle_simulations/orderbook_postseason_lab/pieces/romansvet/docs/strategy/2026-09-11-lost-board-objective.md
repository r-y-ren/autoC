# Lost-board objective: re-weighting the fitness onto the rungs g1000 loses does not un-stick the step

2026-09-11, 23:19-00:00Z. Rig + raw output: `S/popcurve/B/lostw.py`, `summarise_lostw.py`, `lostw.json`,
`lostw.log`, `lostw_summary.txt`, `lostw_overrides.txt` (the W_lost `--rung-weight` list), `lostw_margins.npz`
(per-episode margins of all 25 thetas in-sample), `lostw_holdout_margins.npz`, `grads/g_lostw_p512_s900{1,2}.npy`
(remote copies in `~/popcurve/B/`). Remote GPU1 (22 GB free), `~/stage_hr`, `--chunk 4096`, 1,205 s; both arms untouched.

**Verdict in one line.** Concentrating the objective on the 41 pinned rungs g1000 loses (38 % → 79 % of the mass)
gives the estimator an in-sample gradient it can resolve (κ 0.024/0.037 on the W_lost field, both seeds positive,
vs 0.003/0.005 for the current direction) — but the resulting step **loses held-out on both seeds** (obj −0.034 /
−0.015, margin −956 / −786 coins, win −6.7 / −10 pts on LIVE-C 43-72) and loses **more** than the current
objective's step (−0.006 / −0.012); it beats only 2/16 and 9/16 random steps held-out and flips 10 / 7 won rungs
down in-sample to win 2 / 3 lost ones back. **Pre-check negative → flow192 NOT staged.**

## 1. Design (B's rig, one thing changed: the per-episode weight vector)

`lostw.py` builds the arm's trainer/batch from `~/launch_flow187.sh` (rung weights byte-identical to flow190's,
checked; lr/seed do not enter this rig) → the same 159-episode in-sample batch B/msab/recentre scored
(`F_in obj_w 0.5953, win 0.6102` reproduce B's 0.5952 / 0.6102 to 4 dp). Steps: (1) play the centre once →
per-rung margin for the 147 pinned rungs; (2) classify lost (< 0) / barely (< +1,500) / won, build W_lost =
w × {4, 2, 0.5}, cap 15 % per rung (never binds: max share 3.8 %); (3) reuse msab's saved P=512 rollouts
(`rollouts/p512_s900{1,2}.npz`), regenerate eps from the seed, recompute the arm's own `shaped_advantage` with
`ep_weight` = 2·W_lost on the pinned block (the trainer's `pinned_weights` rule, 1.0 on the 12 carried episodes) →
`g_lost`; the current-weight gradient from the same rollouts reproduces B's saved gradient to cos 0.99994 /
0.99993, so the rollouts are the ones B used; (4) 25 thetas — centre, es{9001,9002}_{cur,lost}±d at
‖d‖ 0.2323, B's 8 random ± controls (rng 777) — scored in ONE play in-sample (per-episode money kept, so
both objectives and the per-rung displacement come from identical rollouts) and on LIVE-C 43-72 from both seats
(60 games, uniform weights). Statistics as B: antisym = F(+d)−F(−d), z against the 8 random antisyms,
κ = z/√5997.

`cos(g_cur, g_lost)` = 0.895 / 0.871: the re-weighting moves the direction by ~26°, not into a new subspace.

## 2. What g1000 loses (centre's own outcome, pinned rungs, one seat each as the arm plays them)

| class | n | top-ten (w 10.2) | LIVE-C 1-42 (w 4) | w2 rungs | current mass | W_lost mass |
|---|---|---|---|---|---|---|
| lost (margin < 0) | 41 | 13 | 11 | 17 | 38.4 % | 78.6 % |
| barely (0 … +1,500) | 12 | 0 | 7 | 5 | 6.9 % | 7.1 % |
| won (≥ +1,500) | 94 | 7 | 24 | 63 | 53.5 % | 13.7 % |

Pinned win rate 72.1 % (106/147), mean margin +4,118 (the 12 carried self-play episodes are 0 / ±3.6k / ±1.0k
pairs). **The current objective already puts 38 % of its mass on boards g1000 loses** — 13 of the 20 top-ten
rungs (35 % win there) and 11 of 42 LIVE-C. Worst lost rungs (coins): 106859327 −40.5k · 107014984 (top) −29.9k ·
106802502 −27.0k · 107004705 (top) −12.7k · 107460905 (C) −11.5k · 107014989 (top) −9.5k · 106812518 −9.1k · 106851135
−8.8k · 107014951 (top) −8.7k · 106803087 −8.0k · 106630344 −7.4k · 107429978 (C) −7.3k · 107446132 (C) −7.0k · 107005822
(top) −6.8k … 107442209 (C) −6; full 53-row table with W_lost weights in `lostw_summary.txt`. Median loss −4.8k.
28 of the 41 losses sit inside ±9k = the sigmoid's live range at margin_scale 3000; the 13 top-ten losses average −7.6k.

**W_lost** (`lostw_overrides.txt`, 147 `--rung-weight` tokens): lost top-ten 40.8, lost LIVE-C 16, lost w2 8;
barely 8 / 4; won 5.1 / 2 / 1; archetypes 0 (they hold no pinned episode). Total mass 1,096 → 2,142.

## 3. The one-step test (‖d‖ 0.2323, P 512, σ 0.02; `+d gain` = F(+d)−F(c); `rand<+d` = random steps beaten)

**IN-SAMPLE, scored under the CURRENT objective (obj_w, ms 3000)** — F(c) 0.5953, random step −0.0112 (16/16 lose)

| step | +d gain | −d gain | antisym | rand asym sd | z | κ | ES_sym | rand<+d |
|---|---|---|---|---|---|---|---|---|
| es9001_cur (= B) | −0.0217 | −0.0293 | +0.0076 | 0.0137 | +0.55 | +0.007 | −0.0255 | 2/16 |
| es9001_lost | −0.0261 | −0.0230 | −0.0031 | 0.0137 | −0.23 | −0.003 | −0.0246 | 0/16 |
| es9002_cur (= B) | −0.0162 | −0.0157 | −0.0005 | 0.0137 | −0.04 | −0.000 | −0.0160 | 5/16 |
| es9002_lost | **+0.0011** | −0.0278 | +0.0288 | 0.0137 | **+2.11** | +0.027 | −0.0133 | **16/16** |

**IN-SAMPLE, scored under W_lost** — F(c) 0.3200 (win_w 0.2107), random step −0.0113 (14/16 lose)

| step | +d gain | −d gain | antisym | rand asym sd | z | κ | ES_sym | rand<+d |
|---|---|---|---|---|---|---|---|---|
| es9001_cur | −0.0201 | −0.0240 | +0.0039 | 0.0148 | +0.26 | +0.003 | −0.0220 | 3/16 |
| es9001_lost | −0.0055 | −0.0331 | +0.0276 | 0.0148 | +1.87 | +0.024 | −0.0193 | 11/16 |
| es9002_cur | −0.0109 | −0.0167 | +0.0058 | 0.0148 | +0.39 | +0.005 | −0.0138 | 7/16 |
| es9002_lost | **+0.0119** | −0.0306 | +0.0425 | 0.0148 | **+2.88** | +0.037 | −0.0094 | **16/16** |

(win_w under W_lost: es_lost antisym z +2.20 / +4.42, κ 0.028 / 0.057; +d gain −0.007 / +0.014. Weighted margin: every ES step loses 190-820 coins, antisym ≤ 0 for es_lost.)

**HELD-OUT (LIVE-C 43-72, 30 boards × 2 seats, uniform weights)** — F(c) obj 0.6158, win 0.6667, margin +3,177;
random step −0.0169 obj / −7.0 pt / −482 coins (13/16, 15/16, 14/16 lose)

| step | obj +d | obj −d | antisym | z | κ | rand<+d | win +d | margin +d | margin antisym (z) | rand<+d (margin) | flips −/+ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| es9001_cur | −0.0059 | −0.0423 | +0.0364 | +1.20 | +0.016 | 11/16 | −3.3 pt | −219 | +818 (+1.18) | 12/16 | −2/+0 |
| es9001_lost | **−0.0338** | −0.0143 | −0.0195 | −0.64 | −0.008 | **2/16** | −6.7 pt | **−956** | −865 (−1.25) | 2/16 | −4/+0 |
| es9002_cur | −0.0121 | −0.0161 | +0.0040 | +0.13 | +0.002 | 10/16 | −6.7 pt | −447 | +247 (+0.36) | 9/16 | −4/+0 |
| es9002_lost | −0.0151 | −0.0176 | +0.0025 | +0.08 | +0.001 | 9/16 | **−10.0 pt** | −786 | −268 (−0.39) | 3/16 | −6/+0 |

**Displacement (in-sample pinned rungs; centre wins 106, loses 41; a random step flips 7.2 ± 2.1 won rungs down
and 2.4 ± 0.6 lost rungs up):** es9001_lost+ −10 / +2 (mass 68 / 16), es9002_lost+ −7 / +3 (32 / 20);
es9001_cur+ −10 / +2, es9002_cur+ −11 / +2. Net flips −8 / −4 for the W_lost steps vs −8 / −9 for the current
ones — the W_lost step is not cheaper on the won rungs than a random step (7.2), and buys back ≤ 3 of 41.

## 4. Reading

1. **The re-weighting does create a resolvable in-sample gradient.** On the W_lost field the W_lost direction's
   antisym is positive on both seeds (z +1.9 / +2.9 obj, +2.2 / +4.4 win_w; κ 0.024-0.057) where the current
   direction on the current field gives z +0.55 / −0.04. That is the mechanism the re-centre doc predicted: on a
   field where the centre is not at a peak, the estimator finds the slope.
2. **But the linear gain does not survive the step.** Under the CURRENT objective in-sample the W_lost step nets
   +0.0011 (seed 9002, 16/16) and −0.026 (seed 9001, 0/16) — one seed's win is the seed lottery B and the recentre
   doc already flagged (their 9001/9002 disagreement was the same size). Under W_lost itself the +d gains are
   −0.0055 / +0.0119, i.e. the curvature cost (ES_sym −0.019 / −0.009) still eats most of the antisym.
3. **Held-out it is a loss on both seeds, and worse than doing nothing new.** obj −0.034 / −0.015 vs the current
   step's −0.006 / −0.012; margin −956 / −786 vs −219 / −447; win −6.7 / −10.0 vs −3.3 / −6.7. Antisym on
   held-out is negative or ~0 for both W_lost steps (z −0.64 / +0.08) where the current step has +1.20 / +0.13.
   The in-sample flips it buys (2-3 boards of 41) are board-specific: 0 of the 30 held-out losses flip on either
   seat, and 4-6 held-out wins flip down (random: 4.2). The task's two staging conditions — held-out net gain > 0
   and ≥ 12/16 random steps beaten — both fail on both seeds.
4. **Why.** The 41 lost boards are lost by −0.1k … −40k with median −4.8k; 28 sit inside the sigmoid's live band
   and already carry 38 % of the objective. Quadrupling them does not add information about how to win them — the
   same 512 rollouts, re-ranked — it only changes which rollouts' noise the estimator loads on, and `cos(g_cur,
   g_lost)` 0.87-0.90 says the direction barely moved. Winning a board g1000 loses by 5-40k against a fixed tape is
   not a σ-0.02 perturbation away; the pinned-board objective is a step function of θ at that scale.

## 5. Verdict / recommendation

**Negative. flow192 is not staged (no `~/launch_flow192.sh`, no `S/flow192/`).** The lost-board re-weighting is
not the changed objective field the re-centre doc called for: the field is the *same boards*, and the centre is at
a peak on them too (every direction loses under W_lost as well: 14/16 random steps lose). A changed field means
new boards/opponents where the centre is not already tuned — the flow190-style widened rungs, fresh top-tier tapes
inside the fitness, or the 2-seat play of every pinned rung (the arm plays one seat per rung per generation; the
other seat is a different board-outcome). If any re-weighting is tried, keep it mild (≤ ×2) and judge it by the
held-out line only; the in-sample flips are selection, exactly as `counterfactuals-overstate` warns.

## 6. Dead ends / caveats

* `centre_reproduced False`: the centre played alone (pop 1) vs inside the 25-theta stack differs on 4 of 159
  episodes (max 449 coins; a chunk-shape effect in the sim), no class or barely-threshold flips — the W_lost
  classification stands; the one-step tables all use the stack play. Any future rig should classify from the
  stack, not a separate play.
* One rollout pair (seeds 9001/9002), the same rollouts B/msab/sigma_ab used — the re-weighting re-ranks existing
  play, it does not sample the lost boards more; that is the design (cheap, paired), and also its limit.
* Held-out win_w is quantised at 1/60; obj/margin carry the comparison. Not tried: ×2 mild re-weighting; W_lost on the flow172_g940 centre (where the current field still has a slope);
  a second-seat evaluation of the lost boards (the seat the arm did not play this generation).
