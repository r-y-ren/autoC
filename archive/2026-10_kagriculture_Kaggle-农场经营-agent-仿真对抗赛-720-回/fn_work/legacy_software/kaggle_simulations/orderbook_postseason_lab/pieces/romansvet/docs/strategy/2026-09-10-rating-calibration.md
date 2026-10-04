# Rating calibration: local judge reads vs realised Kaggle ladder (2026-09-10)

## Method

`ListEpisodes` for subs 56098262 / 56140532 / 56143250; VALIDATION and non-COMPLETED dropped, our
seat matched by `submissionId`, win = higher `reward` (**0 ties in 375 games**), opponent rating =
its pre-game `initialScore`, first 10 games dropped as ramp. Model `P(win) = σ(s·(R_file − R_opp))`,
shared `s`, per-file `R_file` (max-likelihood). Judge reads: `S/glut/verdicts.log` lines 38/54/75/87.
Judge-set opponent ratings are **exact** — LIVE55 (`S/livewin/live_heldout_ids.txt`) and LIVE-C22
(`S/livec/ids.txt`) ids looked up in the episodes they were cut from. Leaderboard: `GetLeaderboard`
competitionId 147734, 8,515 teams.

## (a) Ladder fits

| sub | file | post-ramp n | WR | settled | fitted crossover | 2300–2600 | >2800 |
|---|---|---|---|---|---|---|---|
| 56098262 | flow135_g350 | 261 | 44.4 % | **1924** | 1923 (SE 39) | no games | none |
| 56140532 | g940pair | 70 | 65.7 % | **2531** | 2612 (SE 85) | **59.6 %** (n=57) | none |
| 56143250 | g1000pair_hr | 14 | 85.7 % | 2184 *(ramping)* | 2460 (SE 252) | no games | none |

Shared slope **s = 0.00368/pt** (scale 625, vs Elo's 400): 100 rating points ≈ 9 win-rate points
near 50 %, not 14. Bands — flow135: 1900-1999 49.2 % (120), 2000-2099 32.6 % (92), 1900-2100 42.0 %.
g940pair: 2400-2499 59.3 % (27), 2500-2599 52.2 % (23); converged (last 20: 50.0 % at mean opp 2533,
drift +14), so its ramp-biased 2612 fit yields to 2531. **No file has ever met an opponent above 2621**: matchmaking pairs us within ~±150 of our own
rating, so the >2800 band is unobservable until we are rated ~2700+.

## (b) Judge-to-ladder offset

Judge-implied rating = `R_opp + logit(p)/0.00368`.

| read | p | mean opp | implied | ladder | offset |
|---|---|---|---|---|---|
| flow135 / LIVE55 | 34.5 % | 1991 | 1817 | 1924 | **+107** |
| g940pair / LIVE55 | 83.6 % | 1991 | 2434 | 2531 | **+97** |
| g940pair / LIVE-C22 | 50.0 % | 2443 | 2443 | 2531 | **+88** |
| flow135 / LIVE-C22 | 25.0 % | 2443 | 2144 | 1924 | −220 |
| flow135 / TOPB2 | 15.0 % | 2990 | 2519 | 1924 | −595 |

**In-band offset = +97 (88–107): the judge reads ~100 rating points pessimistic.** g940pair's
crossover (2531) sits 88 above LIVE-C22's mean opponent (2443) where it reads 50 %; flow135's
plateau (1924) sits 107 above LIVE55's implied 1817. The replay itself is near-exact: on the
*identical* 55 boards the ladder gave 20/55 = 36.4 % vs the judge's 34.5 % (−1.9 pts) — the offset
is the *set*, not the tape.

Independent slope check: the slope making LIVE55 and LIVE-C22 (452 points apart) agree on one file
is 0.00360 (g940pair) / 0.00386 (hr) — the ladder fit, reached without either set. At Elo's 0.00576
those two sets disagree by 169 points.

**Out-of-band reads are worthless.** LIVE-C22 and TOPB2 credit flow135 with 2144 and 2519 when it is
1924. Cause: a ~13-point lottery floor — we win 13-15 % against opponents far above us where the
logistic says 1 %. `p = f + (1−2f)·σ`, f = 0.13, reproduces TOPB2: flow135 14 % (obs 15), g940pair
22 % (obs 25), hr 27 % (obs 25). **TOPB2's 25 % is a floor, not a measurement** — it cannot resolve
a 150-point step at n=40 (SE 6.8).

## (c) What 2960 requires

Top-10 cutoff = 2951.0 (rank 10); 2960 = rank 8; rank 1 3084.0, rank 5 2977.8, rank 20 2913.4,
rank 50 2841.8. A 2960 file must cross 50 % against 2960 opponents, i.e. judge-implied
2960 − 97 = **2863**.

| set | mean opp | required paired win rate |
|---|---|---|
| LIVE-C22 | 2443 | **82–84 %** (63.6 % today) |
| TOPB2 | 2990 | **38–41 %** (25 % today, floor-limited) |
| LIVE55 | 1991 | 96 % — saturated at 90.9 %, blind above ~2600 |

TOPB2 is the binding read: every file we own sits at its 25 % floor, so nothing in the inventory is
above ~2700. LIVE55 is finished as a judge.

## (d) Prediction for 56143250 (g1000_pair_hr)

Three routes agree: LIVE-C22 63.6 % → implied 2596 + 97 = **2693**; head-to-head (+13.6 points over
g940pair at 2443) → 2531 + 148 = **2679**; Elo-slope floor 2606. **Prediction: 2650 ± 60
(2620–2700), rank ~250–320 — not top 10, +120–160 over the live file.**

Falsifiable check on games 11–40 (g940pair's template: 82 % cumulative, 2476 at game 40, mean opp
1963): hr should show **≥ 85 % cumulative, rating ≥ 2520 at game 40, ≥ 60 % vs 2400–2600** (g940pair
56 %, 28/50). Below 78 % cumulative, or under 2430 at game 40, and the +97 offset does not carry.
