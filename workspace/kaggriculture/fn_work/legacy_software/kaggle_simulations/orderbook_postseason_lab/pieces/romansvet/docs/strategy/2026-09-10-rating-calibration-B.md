# Rating calibration B — independent second read (2026-09-10)

Blind of `2026-09-10-rating-calibration.md` (disclosure: I saw its one-line summary in
`S/glut/verdicts.log:95` while grepping for board ids; all below is from raw episode JSON).
`ListEpisodes` for 56098262/56140532/56143250 + leaderboard 147734. Covariate = opponent
**initialScore** (rating *entering* the game); `updatedScore` is post-game, contaminated by
the result, and shifts crossovers 25–35 pts.

## (a) Win rate vs opponent rating

`P(win) = 1/(1+exp((opp − c)/s))`, shared `s`, per-file `c`, first 10 games dropped, n=352.
**s = 272 pts/logit** (95 % profile CI 170–620) → **slope 9.2 pp per 100 rating pts** (4.0–14.7).

- 56098262 flow135_g350: n 261, WR 44.4 %, mean opp 1985, **c = 1923** (90 % 1864–1981), score 1924, c−score +21.
- 56140532 g940pair: n 73, WR 67.1 %, mean opp 2416, **c = 2636** (2519–2752), score 2542, c−score +113.
- 56143250 g1000pair_hr: n 18, WR 77.8 %, mean opp 1977, c = 2381 (2145–2799), still ramping.

Bins/100 — 56098262: 1800s 59, 1900s 52, 2000s 28, 2100s 40 %; 56140532: 2300s 86, 2400s 62,
2500s 58, 2600s 67 %.

**The crossover is the plateau.** The converged file (271 games) fits c = 1923 against a final
score of 1924. 56140532 still climbs (2429→2498→2515→2542 at games 30/50/70/83), so its +113 is
unclosed convergence, not bias.

## (b) Judge → ladder offset

The pinned two-seat judge **reproduces live play on the same boards**: LIVE55's 55 source
episodes went 20 W/55 = 36.4 % live, and the judge scores that theta 34.5 % — a 1.9 pp (≈23-pt)
format cost. The rest is **board selection**, derivable without any fitted `c`:

* **LIVE55 +110** — career 44.4 % → judge 34.5 %; `s·[logit .444 − logit .345]` = +113 (+107 if
  anchored on the model at mean opp 1991).
* **LIVE-C22 +188** — the cut is engineered: 33 eligible ≥2300 episodes were 11 L/22 W = 66.7 %,
  re-based to 11 L + 11 W = 50.0 %; `272 × 0.693`.

Converted, both land on the realised plateau: LIVE55 34.5 % → 1817+110 = **1927** (realised 1924);
LIVE-C22 50 % → 2443+188 = **2631** (fitted 2636). The map holds at both tiers.

**TOPB2 does not map.** The curve puts flow135 at 1.9 % against its 2989-mean tapes; TOPB2 reads
15 % (6/40 where 0.8 expected, p = 1.2e-4) — a real floor, the tape being open-loop and unable to
punish. g940pair reads 25 % vs 21.4 % predicted. At n=40 SE = 6.8 pp, so 15 vs 25 % is 1.1 σ, and
g1000pair / g1000pair_hr both sit on 25 % while LIVE55 separates them 89.1→90.9 %.

## (c) What a 2960 file must show (2951 = rank 10, 2960 = rank 9)

- LIVE-C22 (mean opp 2443): true-play 87.0 % → **judge-scale target 77 %** (73–80); today 63.6 %.
- TOPB2 (2989): true-play 47.3 % → **target 47–60 %**; today 25 % for every pair file.
- LIVE55 (1991): 96 %; today 90.9 % — saturated and uninformative.

LIVE-C22 is the usable target: 63.6 → 77 % is **+177 rating points** of real gain. Slope-sensitive
(s=170 → 87 %; s=620 → 63 %); re-fit `s` as games accumulate.

## (d) Where 56143250 settles

c(hr) = c₉₄₀ + 152 (LIVE-C22) or +183 (LIVE55) → **c ≈ 2790**; bootstrap over (s, c₉₄₀, 14/22
boards): median 2778, 80 % [2606, 2977]. Netting the half-closed convergence lag:

**Prediction: settles at 2730, 80 % [2620, 2860] → rank ≈170 (90–330). Not top-10.**

**Falsifier, games 29–58:** expect 72–82 % cumulative against a mean opponent ≥2350, and ≥2480 at
game 58. **≤60 % (≤18/30), or below 2380 at game 58**, means c(hr) ≤ 2600 and the +188 offset is
too generous — re-derive. ≥24/30 and ≥2600 would put c over 2850.

## (e) Caveats

1. **Matchmaking caps the evidence.** Opponent − our rating: mean +3, p10/p90 −71/+74; while
   56140532 sat above 2400 the strongest opponent it drew was 2621. Our win rate vs 2950 agents is
   **unobservable on the ladder** until we are ~2850.
2. **TOPB2 is twice-selected**: the seat is a top-ten agent and every cut episode is one it *won* —
   winner's curse on top of the open-loop floor.
3. **LIVE-C22 is loss-matched by construction**; its absolute number is meaningless without the
   +188, and only file-to-file deltas on it are clean.
4. **n.** c₉₄₀ rests on 73 games (±115), c(hr) on 22 boards, `s` on 352; the 170–620 CI on `s`
   dominates every target. Both live subs were still rising, so every plateau is a lower bound.
