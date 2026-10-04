# Ladder calibration refit — two live subs at 152 / 134 games (2026-09-11 ~05:10Z)

Data: full `ListEpisodes` pulls for 56140532 (g940_pair) and 56143250 (g1000_pair_hr), VALIDATION dropped,
covariate = opponent `initialScore`, first 10 games dropped for the fits. Scratch: `S/calib2/` (episodes_*.json,
games_*.csv, fit.py, sim.py, fit.json, kschedule.json, lb.json). Leaderboard now: rank 10 = **2955.8**, rank 5 =
**3015.8**, rank 1 = 3142; our entry 56140532 = 2629.4 rank 340.

## 1. Data table

| file | sub | games | W-L | WR | mean opp (post-drop) | last-30 WR @ mean opp | rating now | r@g40 / g60 / g100 |
|---|---|---|---|---|---|---|---|---|
| g940_pair | 56140532 | 152 | 103-49 | 67.8 % | 2497 (sd 165, max 2762) | 66.7 % @ 2607 | 2629.4 (+44 in 30) | 2476 / 2524 / 2554 |
| g1000_pair_hr | 56143250 | 134 | 102-32 | 76.1 % | 2351 (sd 207, max 2615) | 66.7 % @ 2514 | 2538.4 (+48 in 30) | 2308 / 2349 / 2479 |

Win rate by opponent band (post-drop): g940 <2300 91 %, 2300s 86 %, 2400s 56 %, 2500s 68 %, 2600s 59 % (n 29), 2700+ 0/1;
hr <2300 73 %, 2300s 77 %, 2400s 77 %, 2500s 67 % (n 21), 2600s 1/1. **Inside the 2400-2700 pool the win rate is flat.**

**Rating-update rule recovered (new):** every game is a plain Elo step, `Δ = K·(won − E)`, `E = 1/(1+10^((opp−me)/400))`,
with K decaying per game played: ≈220 for games 1-15, 117 at g20, 41 at g30, 23 at g40, 12 at g60, **floor 8.9 from ~g80**
(both subs, `S/calib2/kschedule.json`). Matchmaking draws opponents at own rating +3 ± 44 (g31+). Consequences: (i) a loss in
games 15-30 costs 40-120 pts that the K=9 regime recovers at only `8.9·(p−0.5)` ≈ **+1.5 pts/game at p = 0.67** — the ramp
lottery, not strength, explains most of the two files' 91-pt gap (hr's ramp sits at the 5th percentile of the simulated
band for its own c, g940's at the 35th); (ii) the ladder asymptote is the crossover c (P(win)=0.5 vs opponents at c),
approached slowly — ~1,500-2,000 games remain before 2026-09-23 at the observed 6.5-9 games/h, so it is reachable.

## 2. Implied strength (crossover c) and CIs

| fit | g940_pair c | hr c | hr − g940 | slope s (pts/logit) |
|---|---|---|---|---|
| solo logistic (c, s free) | 2710 [2593, 3254] | 3496 [2670, ∞) | — | 307 / 1075 (unidentified) |
| shared s, both files | 2848 [2630, 4385] | 2934 [2643, 5129] | +85 [−186, +1057] | **534, profile 95 % [264, 3000]** |
| **s fixed at 298 (calibration-C prior)** | **2705 [2612, 2807]** | **2697 [2579, 2834]** | **−8 (≈ ±160)** | 298 |
| point estimate mean opp + 298·logit(WR), last 30 | 2814 | 2721 | +93 | 298 |

The within-pool slope has become **unidentifiable**: matchmaking caps the opponent spread at ±150 and inside 2400-2700 the
win rate does not fall (the pool is the clone band; its internal ratings are a ±100 lottery). The 298 prior is kept
because it is confirmed by the *judge's* top-tier anchor: LIVE-C (mean opp 2488, 63.2 %) vs TOPB2 (top-10 tapes ≈ 3010,
25 %) gives s = 512 / (0.541 + 1.099) = **312 pts/logit**. With s = 298 both live files are **level at c ≈ 2700 ± 110**,
and the simulated Elo trajectory from 600 with c = 2705 reproduces g940's real path (medians 2552 / 2588 / 2620 / 2649 at
g40 / 60 / 100 / 152 vs actual 2476 / 2524 / 2554 / 2629 — inside the 5-95 band; hr's actual 2308 / 2349 / 2479 sits on the
5 % edge = bad ramp draw). Forward projection at s = 298 (`sim.py`): g940 after +100 / +200 / +400 games 2670 / 2690 /
2703 (90 % band ±55); hr 2623 / 2662 / 2691. **Neither live file approaches 2956 under any slope in [208, 534].**

## 3. Judge difference vs ladder difference (hr vs g940_pair)

Exact paired reads (`S/bank/paired.py`, ALL line, board-level t):

| set | g940_pair | hr | Δlogit | flips | t |
|---|---|---|---|---|---|
| LIVE62 (124 rows, 62 boards; the pair/hr **tuning** set) | 80.6 % | 88.7 % | +0.636 | +10/−0 | 3.03 |
| LIVE-C72 (144 rows) | 63.2 % | 68.1 % | +0.218 | +13/−6 | 4.74 |
| LIVE-C hold-out boards 43-72 (60 rows) | 58.3 % | 63.3 % | +0.210 | — | — |
| TOPB2 (40 rows) | 25.0 % | 25.0 % | 0 | 0/0 | 2.08 (coins only) |

Ladder, pool-controlled (s = 298): **Δc = −8, ≈ ±160**; shared-s fit +85 [−186, +1057]. Raw ladder ratings say −91 (2538 vs
2629) for the judge-stronger file — that raw sign is **entirely opponent pool + ramp history** (hr's post-drop pool averaged
2351 vs 2497; controlling for it removes the deficit but does not produce a surplus). Implied ladder-per-judge-logit:
LIVE62 −13 [≈ −250, +250]; hold-out −38 [≈ −760, +720] — the pair cannot measure the slope. What it can say: the LIVE62
gain (+0.64 logit → +190 pts predicted at s = 298) **did not appear** (observed −8), consistent with LIVE62 being the set the
switches were tuned on; the hold-out gain (+0.21 → +63 predicted) is within the noise of the observed −8 ± 160. So the
"hr predictions tracked high" of calibration A/B/C was two effects: LIVE62 selection (≈ +150-200 pts of phantom) and the
hr ramp lottery (≈ −100 pts of rating at fixed strength). Hold-out reads only, from here on.

## 4. flow187_g160_hr — prediction and falsifier

Paired reads: vs hr — LIVE62 88.7 → 90.3 % (+0.17, t 2.8), hold-out livech 63.3 → 66.7 % (+0.15, t 0.5), livech2 70.0 → 80.0 %
(+0.54, t 2.1), pooled 60 hold-out boards **66.7 → 73.3 % (+0.32 logit)**, TOPB2 25 → 25 % (0, −518 coins t 1.6). vs g940 —
LIVE62 80.6 → 90.3 % (+0.81, +12/−0 t 6.0), hold-out 58.3 → 66.7 % (+0.36, t 3.5), TOPB2 level.

Prediction (hold-out only; base c ~ 2700 ± 55 SE, Δlogit 0.32 ± 0.25, s log-normal 298 [182, 686]):
**asymptotic c ≈ 2795, 95 % [2610, 3030]; P(c ≥ 2956 top-10) = 7 %; P(stronger than the live pair) = 84 %.**
Vs g940's read alone it is 2705 + 0.36·298 ≈ 2810 — same answer. Not a top-10 file; a +100-pt file if the hold-out holds.

Falsifier bands (Elo simulation from 600, K schedule above, matchmaking +3 ± 44, s = 298; 5 % / median / 95 %):

| games | c = 2700 (level with live pair) | **c = 2800 (prediction)** | c = 2950 (top-10 strength) |
|---|---|---|---|
| 40 | 2367 / 2549 / 2720 | **2439 / 2626 / 2794** | 2537 / 2728 / 2892 |
| 60 | 2432 / 2586 / 2724 | **2514 / 2667 / 2805** | 2625 / 2780 / 2916 |
| 100 | 2498 / 2616 / 2727 | **2583 / 2704 / 2815** | 2704 / 2825 / 2935 |

Decision rule: at game 100 a rating **> 2730** rejects "level"; **< 2700** rejects "top-10 strength"; 2583-2815 is
consistent with the prediction. The ramp lottery makes the rating bands overlap, so add the sharper read: cumulative
post-ramp win rate vs opponents rated 2500-2700 should be **≈ 66 % (c = 2800)** vs 58 % (2700) vs 76 % (2950); SE ≈ 6 pp at
60 such games. Falsified low if that read is ≤ 58 % at 60 games AND rating < 2620 at g100; falsified high (better than
predicted) if ≥ 74 % and > 2760.

## 5. What the cutoffs require (refit)

Required *judge-scale* win rate on LIVE-C (the file's own unfiltered ≥2300 pool, mean opponent 2488; format cost ≈ 2 pp):

| target | s = 182 | s = 208 | **s = 298** | s = 534 | TOPB2 (opp ≈ 3010, s = 298) | from c ≈ 2700 |
|---|---|---|---|---|---|---|
| top-10 = 2956 (brief 2946) | 92.9 % | 90.5 % | **82.8 %** | 70.6 % | 45.5 % | +256 pts = **+0.86 logit** |
| top-5 = 3016 (brief 2997) | 94.8 % | 92.7 % | **85.5 %** | 72.9 % | 50.5 % | +316 pts = +1.06 logit |

Today: g940 63.2 %, hr 68.1 % on LIVE-C72; the candidate 73.3 % on 30 hold-out boards (66.7 % on livech). TOPB2 25 % for all
three (needs 45-50 %). The requirement is unchanged from calibration-C (≈ 81-83 %): a further **+0.85 logit on every set**,
about the whole distance the pair switches plus flow187 have moved so far, twice over.

## 6. Dead ends and caveats

- Within-file logistic slope: unidentifiable now and forever under ±150 matchmaking inside the clone band (profile CI
  264-3000; the hr solo fit diverges). Do not re-fit it; use the judge's TOPB2-vs-LIVE-C anchor (312) or the 298 prior.
- Per-game K was recovered exactly but the opponent's own K (their game count) is not in the episode record — the
  simulator uses our K only, so its bands are slightly narrow; the reproduction of g940's path is the check.
- The candidate's hold-out Δ rests on 60 boards with t 0.5 and 2.1 on the two halves — the +0.32 logit has SE ≈ 0.25.
- Not done (time box): pulling the top-10 files' own game histories to measure the top tier's c directly (would fix s).
