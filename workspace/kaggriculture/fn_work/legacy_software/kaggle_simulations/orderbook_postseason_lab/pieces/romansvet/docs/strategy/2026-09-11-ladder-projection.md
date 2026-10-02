---
name: ladder-projection
description: Full-history Elo fit, equilibrium and 50/100-game Monte-Carlo projection for the two live subs (B 56161192, hr 56143250), 2026-09-11 ~16:45Z
metadata:
  type: analysis
---

# Ladder projection for the two live files — 2026-09-11 16:45Z

Data: credential-free `ListEpisodes` full pulls at 2026-09-11T16:44Z (VALIDATION dropped), covariate =
opponent `initialScore` (rating at game time), our rating = `updatedScore`. Scratch (not in the repo):
`<scratchpad>/ladderproj/{ep_B,ep_hr}.json, games_{B,hr}.csv, fit2.py, proj.py, lb.json`.

| file | sub | games | W-L | WR | rating now | mean opp (post-30) | matching band |
|---|---|---|---|---|---|---|---|
| **B** = flow193_g100_hr | 56161192 | 85 | 63-22 | 74.1 % | **2398.8** | 2324 (sd 49) | opp = me **−4.8 ± 43** |
| **hr** = flow172_g1000_pair_hr | 56143250 | 199 | 142-57 | 71.4 % | **2602.8** | 2470 (sd 111) | opp = me **+3.5 ± 47** |

Leaderboard pulled at the same time (competition 147734): rank 1 = 3126.4, **rank 5 = 3002.7, rank 10 = 2966.8**,
rank 20 = 2909.1, rank 50 = 2842.6. Our LB entry = hr, **2608.2, rank 353/8,633**. The brief's "top-10 ≈ 2943"
is stale — the cutoff has moved up ~24 pts since 05:10Z. Pool density: 200 teams ≥ 2700, 89 ≥ 2800, 25 ≥ 2900.

**K schedule re-confirmed on both files** (per-game `Δ / (won − E)`, E from `initialScore`s): ~220 for g1-15,
146/126 at g20, ~40 at g30, ~23 at g40, ~11.6 at g60, **floor 8.6-9.4 from ~g78 on both**. B is already at the
floor (g80-85 = 8.6-9.4), so every projection below uses K = 8.9 for both files.

## 1. Form by opponent-rating bin

**B (56161192), n = 85**

| window | 2200-2400 | 2400-2600 | 2600-2800 | 2800+ | WR | mean opp |
|---|---|---|---|---|---|---|
| ALL (85) | 40/59 = 68 % | 4/4 = 100 % | — 0/0 | — 0/0 | 74.1 % | 2108 |
| **LAST 40** | **26/36 = 72 %** | **4/4 = 100 %** | **0/0** | **0/0** | **75.0 %** | **2338** |
| LAST 60 | 37/54 = 69 % | 4/4 = 100 % | 0/0 | 0/0 | 70.0 % | 2314 |
| post-30 (55) | 34/51 = 67 % | 4/4 = 100 % | 0/0 | 0/0 | 69.1 % | 2324 |

**hr (56143250), n = 199**

| window | 2200-2400 | 2400-2600 | 2600-2800 | 2800+ | WR | mean opp |
|---|---|---|---|---|---|---|
| ALL (199) | 33/46 = 72 % | 74/111 = 67 % | 11/15 = 73 % | — 0/0 | 71.4 % | 2345 |
| **LAST 40** | **0/0** | **18/28 = 64 %** | **9/12 = 75 %** | **0/0** | **67.5 %** | **2564** |
| LAST 60 | 0/0 | 28/46 = 61 % | 10/14 = 71 % | 0/0 | 63.3 % | 2557 |
| post-30 (169) | 30/40 = 75 % | 74/111 = 67 % | 11/15 = 73 % | 0/0 | 69.2 % | 2470 |

**Neither file has ever played an opponent rated ≥ 2700** (hr max 2675, B max 2433). The 2800+ bin is
*structurally empty*: matchmaking draws opponents at own rating ± 45 with no tail (|opp − me| > 100 in 2 % of
hr's games, 0 % of B's), so the 2800+ column can only ever fill after our own rating passes ~2760.
Any 2800+ read must come from the judge (TOPB2), not the ladder.

Two secondary reads:
- hr's win rate **declines as it climbs**, the signature of approaching equilibrium: by own-rating slice
  (post-30) 2200-2300 → 74 %, 2300-2400 → 82 %, 2400-2500 → 70 %, **2500-2600 → 64 %**.
- B's 2200-2300 slice is anomalously bad: **8/18 = 44 % post-30** (14/25 = 56 % all-games) against
  26/33 = 79 % at 2300-2400. That inversion is the LOSS10 counter-class band clone, and it is *in the pool
  B is sitting in right now*. hr on the same 2200-2300 slice: 10/14 = 71 %.
- No repeat-opponent structure to exploit: B met 82 distinct teams (one 3×), hr met 193 distinct teams (none 3×).
- Game rate: B 11.8/h over its last 40, hr 6.3/h. To 2026-09-23 that is ~3,400 (B) / ~1,800 (hr) more games —
  the asymptote is reachable in time for both.

## 2. Logistic fit and equilibrium

Model `P(win) = σ((c − opp)/s)` on the **absolute** opponent rating (our own strength is the constant c; Δ =
c − opp). Fitting on Δ = our *rating* − theirs is uninformative here because matchmaking pins Δ to ±45.

Free two-parameter fits are **unidentified**, exactly as the 05:10Z calibration found — B: c = 2622, 95 %
profile [2386, 4000], s = 390 [155, 1975]; hr: c = 2926 [2654, 4000], s = 580 [285, 2000] (both upper bounds
run off the grid). So s is fixed at the calibration-C / judge-anchor prior **s = 298 pts/logit** and reported
with an s-sensitivity row.

| file | window | n | WR | mean opp | **c (s = 298)** | 95 % CI | s = 208 | s = 534 |
|---|---|---|---|---|---|---|---|---|
| B | post-30 | 55 | 69.1 % | 2324 | **2565** | [2400, 2743] | 2493 | 2754 |
| B | last 60 | 60 | 70.0 % | 2314 | 2569 | [2409, 2740] | — | — |
| B | last 40 | 40 | 75.0 % | 2338 | 2667 | [2464, 2896] | — | — |
| B | *2300-2400 slice only* | 33 | 79 % | 2343 | *2738* | [2520, 3020] | — | — |
| hr | post-30 | 169 | 69.2 % | 2470 | **2720** | [2623, 2820] | 2650 | 2907 |
| hr | last 60 | 60 | 63.3 % | 2557 | 2721 | [2568, 2883] | — | — |
| hr | last 40 | 40 | 67.5 % | 2564 | 2784 | [2592, 2990] | — | — |
| hr | *2300-2400 slice only* | 26 | 77 % | 2359 | *2719* | — | — | — |

**Equilibrium.** Solving `r*` such that `E[σ((c − opp)/s)] = E[1/(1+10^((opp−r)/400))]` with
`opp ~ N(r + δ, band sd)` (the measured matching band) gives r* = c to within 3 pts — the band is symmetric
and narrow, so the equilibrium simply *is* the crossover:

| file | **equilibrium r\*** | 95 % CI | at s = 208 | at s = 534 |
|---|---|---|---|---|
| **B** | **2562** | [2397, 2740] | 2492 | 2744 |
| **hr** | **2722** | [2625, 2822] | 2651 | 2914 |

The **matching band is stable and tracks our rating 1:1** with no ceiling up to 2603: by own-rating slice
(post-30), opp − me = +2.6 ± 46 at me 2200-2300, −4.2 ± 41 at 2300-2400, +6.8 ± 37 at 2400-2500,
+1.1 ± 49 at 2500-2600. Regression of opp on our rating over hr's post-30 games: slope 1.015, intercept −33.
So "who we get matched with as we climb" = **ourselves ± 45**, all the way up.

**B vs hr on common support.** On the only pool both have played (opp 2200-2400, post-30): B 34/51 = 66.7 %,
hr 30/40 = 75.0 %, Δlogit = **−0.41 ± 0.47 (t −0.86)** = −121 ± 140 rating pts for B. On the 2300-2400
sub-slice they are level (B 79 %, hr 77 %); the whole gap sits in 2200-2300 where B meets the LOSS10 counter
class (44 % on 18 games). **The ladder cannot yet distinguish B from hr**, and B's point estimate is
depressed by a band it will leave. Treat B's c as **2565 [2400, 2743] pessimistic / ~2740 optimistic** and
re-read it after B has 40 games above opponent 2450.

## 3. Monte-Carlo projection (1,000 runs, K = 8.9, measured matching band)

Each run draws c ~ N(point, SE from the profile CI) and s log-normal(298; 95 % [182, 686]), then plays games
with opp = r + δ + N(0, band sd), win ~ σ((c−opp)/s), Elo update K = 8.9. Percentiles 10/50/90:

| file | from | +50 games | +100 games | +200 | +400 |
|---|---|---|---|---|---|
| **B** (c = 2565, full uncertainty) | 2399 | **2401 / 2451 / 2505** | **2406 / 2484 / 2564** | 2418 / 2527 / 2623 | 2443 / 2553 / 2674 |
| B (c = 2565 point, game noise only) | 2399 | 2415 / 2449 / 2480 | 2441 / 2482 / 2524 | 2479 / 2526 / 2571 | 2508 / 2552 / 2602 |
| B (optimistic c = 2738 from its 2300-2400 slice) | 2399 | 2466 / 2496 / 2526 | 2524 / 2567 / 2610 | 2608 / 2654 / 2696 | 2668 / 2714 / 2761 |
| **hr** (c = 2720, full uncertainty) | 2603 | **2599 / 2641 / 2682** | **2611 / 2666 / 2721** | 2625 / 2691 / 2759 | 2638 / 2713 / 2786 |
| hr (c = 2720 point, game noise only) | 2603 | 2606 / 2639 / 2674 | 2626 / 2668 / 2708 | 2652 / 2696 / 2741 | 2668 / 2716 / 2764 |

P(either file ever reaches 2967 inside 400 games) = **0.000 (B) / 0.001 (hr)**. At the current game rates
+100 games is ~8 h for B, ~16 h for hr, so both numbers are same-day falsifiable.

Drift arithmetic behind this: at K = 8.9 the gain per game is `8.9·(p − 0.5)` = **+1.6 pts at p = 0.68,
+0.9 pts at p = 0.60, +0.4 pts at p = 0.55**. The last 300 rating points to top-10 cost ~350-800 games *even
at the required strength*, which is why the asymptote, not the climb, is the binding constraint.

## 4. The top-10 question

**(a) What c reaches the 2966.8 cutoff within 150 games from hr's 2603** (MC, s = 298, K = 8.9):

| true strength c | rating at g150 (10/50/90) | P(≥ 2967) |
|---|---|---|
| 2800 | 2695 / 2740 / 2779 | 0.00 |
| 2900 | 2756 / 2802 / 2846 | 0.00 |
| **2967** (exactly top-10 strength) | 2798 / **2843** / 2885 | **0.00** |
| 3050 | 2853 / 2893 / 2934 | 0.01 |
| **3150** | 2909 / **2950** / 2991 | **0.30** |
| 3250 | 2964 / 3004 / 3044 | 0.89 |

A file that is *exactly* top-10 strength does **not** get there in 150 games — K = 8.9 leaves it at ~2843.
To be *at* 2967 by g150 you need **c ≈ 3250**, i.e. rank-1-to-2 strength; to be there by g400 you need
c ≈ 3000-3050. Equivalently: 150 games from 2603 to 2967 requires a **sustained 77.3 % win rate** against a
pool that follows you up the whole way (75.5 % for the stale 2943 target).

**(b) Required per-bin win rates (s = 298):**

| target c | 2200-2400 | 2400-2600 | 2600-2800 | **2800-3000** |
|---|---|---|---|---|
| 2720 (hr today) | 80 % | 68 % | 52 % | 35 % |
| 2800 | 84 % | 73 % | 58 % | 42 % |
| 2900 | 88 % | 79 % | 66 % | 50 % |
| **2967 (top-10)** | **90 %** | **83 %** | **71 %** | **56 %** |
| 3100 | 94 % | 88 % | 79 % | 66 % |

So the **2800+ bin needs 56 %** to hold 2967 (and ~65-70 % to *arrive* there in 150 games). The judge's
TOPB2 set (top-10 tapes, opp ≈ 3010) reads **25 %** for hr, g940 and the candidate alike — the ladder's
requirement (56 % at 2800-3000, ~46 % at TOPB2's 3010) and the judge's best read are still **~1.0 logit apart**,
unchanged from the 05:10Z calibration.

**(c) hr's 2600-2800 form vs what it needs:** hr is **11/15 = 73 % all-games, 9/12 = 75 % last 40, 10/14 = 71 %
last 60** — SE ≈ 11 pp on 15 games. The top-10 requirement in that bin is **71 %**, so *this bin alone looks
already on target*. It is a small-n mirage: the same file's **2400-2600 bin is 67 % on 111 games (SE 4.5 pp)
against the 83 % that 2967 requires** — a 0.88-logit shortfall with 7× the sample. The binding read is
2400-2600, and it says hr is a ~2720 file, not a 2967 file.

**(d) Games against ≥ 2800 opponents: hr 0, B 0.** Against ≥ 2700: hr 0, B 0. hr's ten highest-rated
opponents all sit 2620-2675 (11/15 = 73 % in 2600-2700); B's highest is 2433. Neither file has any ladder
evidence at all about top-tier play.

## 5. Conclusion

1. **Equilibria: hr ≈ 2722 [2625, 2822]; B ≈ 2562 [2397, 2740] on its face, but B's read is taken entirely
   inside the 2200-2400 pool where its LOSS10 counter class lives (44 % on the 2200-2300 slice vs 79 % at
   2300-2400); on common support B − hr = −0.41 ± 0.47 logit, i.e. indistinguishable.** Expect hr to plateau
   ~2700-2730 and B ~2560-2740, converging near 2700 if its 2300-2400 form is the true read.
2. **Projections:** hr 2641 (10/90: 2599/2682) after 50 games and 2666 (2611/2721) after 100; B 2451
   (2401/2505) after 50 and 2484 (2406/2564) after 100. Neither reaches 2967 with probability > 0.1 % in 400
   games. The live top-10 cutoff has risen to **2966.8** (rank 5 = 3002.7); our LB entry is hr at 2608, rank 353.
3. **Keeping hr live still makes sense, but only as a measuring instrument, not as a ladder asset.** It is the
   only file with games above 2500 (126 of them) and above 2600 (15), it is our LB entry, and it is still
   climbing ~+0.9/game toward ~2720. Replacing it costs that 199-game calibration baseline and restarts a
   ramp whose 15-30-game lottery is worth ±100 pts of rating at fixed strength.
4. **But replace it the moment a candidate clears the hold-out bar** — hr's ceiling (~2722) is 245 pts below
   top-10 and the K = 8.9 floor means hr cannot close that even with 2,000 games. Nothing is lost by keeping
   it live *until* the next promotion, and nothing is gained by keeping it after.
5. **Top-10 is not a ladder-mechanics problem, it is a strength problem of ~+250 pts = +0.85 logit on every
   judge set** (LIVE-C 82.8 %, TOPB2 45.5 %, 2400-2600 ladder bin 83 %) — and because K = 8.9 makes the climb
   asymptotic, a file that is merely *at* 2967 strength needs ~400 games to show it. Promote on hold-out
   judge reads; use the ladder only as a 100-game falsifier of the predicted c.
