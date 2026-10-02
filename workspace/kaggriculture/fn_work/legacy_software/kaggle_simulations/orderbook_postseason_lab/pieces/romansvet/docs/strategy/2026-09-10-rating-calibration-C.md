# Rating calibration C — re-fit after +90/+60 ladder games (2026-09-10 15:00Z)

Method as in A/B: `ListEpisodes`, VALIDATION dropped, covariate = opponent `initialScore`,
first 10 games dropped, **0 ties in 422 games**. Leaderboard re-pulled: **rank 10 = 2943.2**
(down 8), rank 9 = 2964.9 — 2960 is rank 9.

## (a) Shared-slope fit — the interval did not close

`P(win)=σ((c_file−opp)/s)`, shared `s`, per-file `c`, n = 392.

| file | sub | n | WR | mean opp | fitted c | ladder score |
|---|---|---|---|---|---|---|
| flow135_g350 | 56098262 | 261 | 44.4 % | 1985 | 1918 | 1923.9 settled |
| g940pair | 56140532 | 80 | 65.0 % | 2426 | **2631** (2493–2775) | 2535.8, +16/20 games |
| g1000pair_hr | 56143250 | 51 | 72.5 % | 2181 | 2506 (2324–2703) | 2354.3, climbing |

**s = 298 pts/logit, 95 % profile CI 182–686** → 8.4 pp per 100 pts (3.6–13.7); B had 272
(170–620) at n = 352, so **40 games moved it +26 and narrowed nothing.** With per-file
intercepts `s` is identified only by *within-file* opponent spread, capped at ±150 pts by
matchmaking — more 2500+ games cannot fix that while we are matched near our own rating.
Subsets stay wide (169–670). Solo fit for 56140532: **s = 208, c = 2583 (2485–2685)**.

## (b) 56140532 by band, and its crossover

| band | n | W | WR | SE |
|---|---|---|---|---|
| <2300 | 11 | 10 | 90.9 % | 8.7 |
| 2300–2399 | 7 | 6 | 85.7 % | 13.2 |
| 2400–2499 | 29 | 17 | 58.6 % | 9.1 |
| 2500–2599 | 30 | 17 | 56.7 % | 9.0 |
| 2600+ | 3 | 2 | 66.7 % | 27.2 |

Above 50 % in every band met; last 20 games 60.0 % at mean opp 2537. **Crossover 2631
(2493–2775)**; the realised 2536 is an unconverged floor. No opponent above 2621 has ever been
drawn — 2700+ is unobservable.

## (c) LIVE-C63 target for 2960

**63 boards, 39 W = 61.9 % (SE 6.1), mean opponent 2488** — the brief's "~2440" is 48 pts low;
the pool is now 69 games (60.9 %, 2490). **Offset = 0**: it is the file's own *unfiltered* ≥2300
pool, so B's re-basing term (`272·ln(22/11)`, for the loss-matched C22 cut) and any selection
term vanish. Check: 2488 + 298·logit(.619) = **2585**, between realised 2536 and fitted 2631.

Required read for c = 2960, `σ((2960−2488)/s)`:

| s | 182 | 208 solo | 298 | 686 |
|---|---|---|---|---|
| target | 93.0 % | 90.2 % | **83.0 %** | 66.6 % |

**≈ 83 % live-scale, 95 % interval 67–93 %.** Anchoring on 2536 instead of the implied 2585
gives 87 % (74–94) — dwarfed by `s`. Net of B's 1.9 pp format cost the **judge-scale target is
≈ 81 % (65–91 %) vs 61.9 % today**: +21 pp, ≈ +470 rating pts.

## (d) 56143250 vs its predictions

61 games, rating **2354.3**, post-ramp 72.5 % (n = 51). Bands: <2300 27/37, 2300–2399 9/13
(69.2 %), 2400–2499 1/1, **none above 2500**.

| falsifier | required | actual | verdict |
|---|---|---|---|
| A: cum. WR at g40 | ≥ 85 % | 82.5 % (33/40) | marginal miss |
| A: rating at g40 | ≥ 2520 | 2308 | **miss** |
| B: g29–58 WR | 72–82 % | 73.3 % (22/30) | pass, low end |
| B: g29–58 mean opp | ≥ 2350 | 2287 | miss |
| B: rating at g58 | ≥ 2480 | 2362 | **miss** |

Its fitted c (2506) sits *below* g940pair's (2631), CIs overlapping. A's 2650 ± 60 and B's
2730 [2620, 2860] track high: hr is 120–210 pts behind on rating milestones, though still
climbing (+55 in its last 10) and never yet matched above 2500.
