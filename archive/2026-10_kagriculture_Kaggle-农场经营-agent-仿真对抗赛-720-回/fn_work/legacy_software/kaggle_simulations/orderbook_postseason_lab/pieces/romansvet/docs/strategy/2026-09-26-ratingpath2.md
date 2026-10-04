# RATINGPATH2 (2026-09-26): what our live rating needs to reach the top-5 bar
Data: S/livewatch15 (ListEpisodes for our 4 subs, 432 rated games, both seats' initial and updated scores; LB of 9,987 rows, fetched 09-25 ~03:50Z). Scripts and output are in S/ratingpath2/{model,sim,elo_b,lb}.py and out/.

## 1. Fitted update rule (out/elofit.txt)
- `d = K(n) * (win - E)`, `E = 1/(1+10^((oppR-mu)/400))`: this is plain Elo with a 400 scale. The best S on a grid from 250 to 700 is 400. RMSE is 6.7 over all 432 updates and 0.2 once n >= 80. Every sub starts at mu = 600.
- K(n) by game count: 219 (n<10), 199 (10-15), 135 (15-20), 64 (20-25), 41 (25-30), 26 (30-40), 18 (40-50), 14 (50-60), 11 (60-70), then **8.9 flat from n = 70** (a sigma floor). In the settled regime a win against an equal opponent is +4.5 and a loss is -4.5.
- The pure TrueSkill form (sigma0/beta/tau) fits worse (RMSE 17.5, out/tsfit.txt). Updates are close to zero-sum (median |d_us + d_opp|/|d_us| = 0.08).
- Matchmaking picks opponents near our own rating: opp - us has mean -5 and sd 52 once n >= 20.
- **vrp3 (83-13) sits 290 below vrp2 (79-18)** for two reasons:
  - Early losses at high K: vrp3 lost 5 games before n = 30 for -310 in total, vrp2 lost 3 for -126.
  - Opponent mix: vrp3 met a 2,232 average field (vrp2 met 2,570), so its wins count for less.
  - Measured strength theta is **vrp2 2,818 +-50, vrp3 2,598 +-60** (Elo MLE on n >= 20).
  - Both subs are still climbing: +2.0 and +3.0 per game over their last 30.

## 2. Plateau (+200 games, 2,000 futures)
Model B is the Elo-consistent one. For vrp2 on its own, a free-slope logistic P(win | oppR) has slope -0.53 per 100 against Elo's -0.58 (LR chi2 0.02), so the Elo curve is not rejected. Pooling vrp2 with vrp3 gives a flat slope of -0.14, but that is a confound: the two subs have different theta and met different fields. Model A extrapolates that flat slope and lands at 3,034 from vrp2. It is rejected and kept only as out/sim.txt.

| sub | now | theta | plateau p10/p50/p90 | P(>= 2,980) |
|---|---|---|---|---|
| vrp2 | 2,709 (n96) | 2,818 +-50 | 2,744 / 2,809 / 2,877 | 0.00 |
| vrp3 | 2,419 (n95) | 2,598 +-60 | 2,502 / 2,583 / 2,663 | 0.00 |

The vrp2 p50 of 2,809 is about rank 38 today. Game noise alone gives +-35 (p10 to p90) around theta.

## 3. Sensitivity: loss rate against the observed 2,300-2,700 opponent set
This is the set of 99 vrp2/vrp3 games against opponents rated 2,300-2,700 (mean 2,501). Observed loss rate is 17.2 %.

| loss rate | theta | P(win) vs 2,900 / 3,000 | plateau p10/p50/p90 (vrp2 +200 games) | P(>= 2,980) | games to 2,980 (median) |
|---|---|---|---|---|---|
| 18 % (now) | 2,790 | 0.35 / 0.23 | 2,748 / 2,784 / 2,819 | 0.00 | never |
| 12 % | 2,877 | 0.47 / 0.33 | 2,825 / 2,863 / 2,899 | 0.00 | never |
| 8 % | 2,958 | 0.58 / 0.44 | 2,900 / 2,937 / 2,971 | 0.05 | never |
| 5 % | 3,047 | 0.70 / 0.57 | 2,980 / 3,018 / 3,052 | 0.90 | 132 |
| 3 % | 3,141 | 0.80 / 0.69 | 3,062 / 3,096 / 3,132 | 1.00 | 94 |

**A theta of 2,980 needs a 7.1 % loss rate against the 2,300-2,700 band.** That means cutting the current rate to about 40 % of what it is now, or equivalently winning 44 % against 3,000-rated opponents. A p50 of 2,980 or better needs about 6.5 %. Holding the bar at p90 needs about 5 %.

## 4. Fresh start for the final (Oct 1-15, model B)
- Cadence: a new sub plays 16 games/h for its first 70 games (70 games in 3.7-4.4 h), then 3.7-5.5 games/h (vrp2 3.9, vrp3 5.5, cfog3le 3.7). Over 15 days that is **about 1,300-2,000 games per sub**.
- The rating reaches plateau within about 200 games (L 17 %: 2,775 after 200 games against a 2,800 plateau). Starting fresh therefore costs nothing by Oct 15. The final is decided entirely by theta.

| games | L 17 % (now) | L 12 % | L 8 % | L 5 % | L 3 % |
|---|---|---|---|---|---|
| 200 | 2,734/2,775/2,814 | 2,805/2,844/2,884 | 2,874/2,917/2,959 | 2,951/2,997/3,037 | 3,026/3,075/3,120 |
| 1,314-2,025 | 2,765/2,800/2,835 | 2,841/2,877/2,913 | 2,921/2,959/2,994 | 3,012/3,047/3,084 | 3,106/3,141/3,178 |

## 5. Leaderboard crowding (out/lb.txt)
- Score by rank: r1 3,126.0, r2 3,005.6, r5 2,980.5, r10 2,932.6, r20 2,858.2, r50 2,751.8, r84 2,709.0 (this is us, vrp2), r100 2,676.7.
- 13 teams sit within +-100 of 2,980. Ranks 4-7 are packed into 2,977-2,982.
- 6 teams are at >= 2,980, 14 at >= 2,900, 36 at >= 2,800 and 88 at >= 2,700.
- A 2,809 plateau is rank ~38 and 2,877 is rank ~16. Top-5 needs theta 2,980 plus luck: the p10-p90 spread is +-35, and rank 4-7 are 5 points apart.

## Caveats
- Model B treats opponents' current ratings as their true strength and assumes the field stands still. If the top teams keep improving, the bar moves up.
- vrp2's record against opponents rated 2,700-2,800 is only 3-3. P(win) against 2,900 or higher is extrapolated from the Elo curve, not observed.
- theta has a standard error of 50, so the 18 % row is really somewhere between 2,740 and 2,870.

**Verdict: at the current 17-18 % band loss rate, the plateau is about 2,810 (rank ~38) whether the sub keeps running or starts fresh. Top-5 (2,980) needs the loss rate against 2,300-2,700 opponents to drop to about 7 % (p50) or about 5 % (p90). That is 7 losses per 100 games there, not 17.**
