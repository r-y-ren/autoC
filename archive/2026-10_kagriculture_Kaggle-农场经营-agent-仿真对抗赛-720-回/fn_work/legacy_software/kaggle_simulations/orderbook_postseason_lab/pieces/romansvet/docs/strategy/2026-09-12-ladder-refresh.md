---
name: ladder-refresh
description: Refreshed Elo fit, equilibrium, convergence and 11-day outlook for the two live subs (B 56161192, hr 56143250) on all games to date, 2026-09-12 ~04:20Z
metadata:
  type: analysis
---

# Ladder refresh — 2026-09-12 04:20Z

Supersedes `docs/strategy/2026-09-11-ladder-projection.md` (16:45Z). Data-only: credential-free
`ListEpisodes` full pulls for both live submissions and `GetLeaderboard` for competition 147734,
taken at 2026-09-12T04:15-04:21Z. Tooling `S/ladder2/{fetch.py,refresh.py}`, per-game rows
`S/ladder2/rows.csv` (426 games), full tables `S/ladder2/refresh.md`, fits `S/ladder2/fit.json`.
Model unchanged: `P(win) = σ((c − opp)/s)`, `s = 298` pts/logit [182, 686] (calibration-C),
Elo `K = 8.9` floor, matchmaking band measured per file.

## Headline

| | B (56161192) | hr (56143250) |
|---|---|---|
| games | **156** (117-39, 75.0 %) | **270** (178-92, 65.9 %) |
| rating now | **2572.6** | **2623.4** |
| mean opponent, last 40 | 2525 | 2639 |
| win rate, last 40 | 72.5 % | 47.5 % |
| **fitted strength c (last 100)** | **2817** [2678, 2968] | **2712** [2603, 2827] |
| **equilibrium r\*** | **2818** [2679, 2969] | **2716** [2607, 2831] — but see §3 |
| direct (model-free) r\*, last 60 | 2857 | **2634** |
| games to within 25 pts of r\* | 311 (~58 h) | 176 (~30 h) |
| status | **still climbing, +1.75 pts/game** | **converged; last 40 is −0.9 pp below par** |

**The 09-11 projection (hr ≈ 2722, B ≈ 2562) was right about hr and wrong about B, in the exact
way it said it might be.** It wrote: *"B's read is taken entirely inside the 2200-2400 pool where
its LOSS10 counter class lives… treat B's c as 2565 pessimistic / ~2740 optimistic and re-read it
after B has 40 games above opponent 2450."* B now has **54 games above opponent 2450 at 74.1 %
(mean opp 2521)**, which reads **c = 2834**. The falsifier fired in B's favour.

## 1. Opponent-rating trajectory

| file | window | n | mean opp | sd | max | WR |
|---|---|---:|---:|---:|---:|---:|
| B | all | 156 | 2282 | 386 | 2631 | 75.0 % |
| B | last 100 | 100 | 2450 | 89 | 2631 | 77.0 % |
| B | **last 40** | 40 | **2525** | 53 | 2631 | **72.5 %** |
| hr | all | 270 | 2421 | 354 | 2770 | 65.9 % |
| hr | last 100 | 100 | 2615 | 56 | 2770 | 58.0 % |
| hr | **last 40** | 40 | **2639** | 55 | 2770 | **47.5 %** |

Matchmaking still pins the opponent to our own rating: band (opp − me, post-30) = **+1.4 ± 50** for
B, **+5.2 ± 47** for hr. B's pool has risen 2324 → 2525 in 24 h; hr's 2470 → 2639.

In 20-game blocks the two files are at opposite ends of their ramps:

| file | block | own rating | mean opp | WR | mean margin |
|---|---|---|---:|---:|---:|
| **B** | g141-156 (its last 16) | 2519 → 2573 | 2542 | **87.5 %** | **+8,438** |
| **hr** | g141-160 (same rung) | 2537 → 2552 | 2547 | **55.0 %** | +3,658 |
| hr | g241-270 (its last 30) | 2615 → 2623 | 2648 | 48.0 % | +1,616 |

**At the same rung of the ladder (own rating ≈ 2540, opponent ≈ 2545) B scores 87.5 % where hr
scored 55 %.** That is the single cleanest like-for-like comparison available.

## 2. Win rate by opponent band

| file | window | <2500 | 2500-2599 | 2600-2699 | 2700+ | total |
|---|---|---:|---:|---:|---:|---:|
| B | all | 92/123 = 75 % | 22/30 = 73 % | 3/3 = 100 % | — | 117/156 = 75 % |
| B | last 40 | 9/13 = 69 % | 17/24 = 71 % | 3/3 = 100 % | — | 29/40 = 72 % |
| hr | all | 92/123 = 75 % | 48/77 = 62 % | 34/63 = 54 % | 4/7 = 57 % | 178/270 = 66 % |
| hr | last 40 | — | 5/9 = 56 % | 10/24 = 42 % | 4/7 = 57 % | 19/40 = 48 % |

hr is now the **only** file with a real sample above 2600 (70 games, 25 of them ≥ 2650, 7 ≥ 2700,
max opponent 2770). B's ceiling so far is opponent 2631 (3 games). B's worst band remains
2200-2300 — **14/25 = 56 %** over its whole life against 73-100 % everywhere above 2300 — the
LOSS10 counter class, and B has now climbed out of it.

## 3. Fitted strength, equilibrium, convergence

| file | window | n | WR | mean opp | **c (s=298)** | 95 % CI | c at s=182 | c at s=686 | **r\*** |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| B | post-30 | 126 | 73.0 % | 2418 | 2723 | [2607, 2841] | 2612 | 3105 | 2723 |
| B | **last 100** | 100 | 77.0 % | 2450 | **2817** | [2678, 2968] | 2681 | 3282 | **2818** |
| B | last 60 | 60 | 76.7 % | 2503 | 2861 | [2695, 3078] | 2725 | 3320 | 2862 |
| B | last 40 | 40 | 72.5 % | 2525 | 2816 | [2616, 3051] | 2705 | 3191 | 2817 |
| hr | post-30 | 240 | 63.7 % | 2518 | 2693 | [2608, 2772] | 2633 | 2908 | 2697 |
| hr | **last 100** | 100 | 58.0 % | 2615 | **2712** | [2603, 2827] | 2675 | 2837 | **2716** |
| hr | last 60 | 60 | 50.0 % | 2634 | 2634 | [2473, 2780] | 2634 | 2634 | 2637 |
| hr | last 40 | 40 | 47.5 % | 2639 | 2609 | [2396, 2791] | 2620 | 2570 | 2613 |

**K-weighted convergence** (K = 8.9, measured band, deterministic drift `K·(p − E)`):

| file | c | r now | r\* | gap | games to \|r − r\*\| < 25 | hours at its game rate | +100 g | +200 g | +400 g |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B | 2817 | 2573 | 2818 | +245 | **311** | 58 h (5.4 g/h) | 2699 | 2761 | 2805 |
| hr | 2712 | 2623 | 2716 | +92 | **176** | 30 h (5.8 g/h) | 2672 | 2695 | 2711 |

### The model check that matters

Under a fixed `s`, the local estimate `c_local = mean_opp + s·logit(WR)` must be constant in every
own-rating slice. It is not, and the two files break it in **opposite directions**:

| file | own-rating slice | n | mean opp | WR | c_local (s=298) |
|---|---|---:|---:|---:|---:|
| B | 2200-2300 | 17 | 2286 | 65 % | 2466 |
| B | 2300-2400 | 36 | 2345 | 75 % | 2672 |
| B | 2400-2500 | 43 | 2455 | 74 % | 2773 |
| B | **2500-2600** | 30 | 2529 | 73 % | **2830** |
| hr | 2300-2400 | 22 | 2360 | 82 % | 2809 |
| hr | 2400-2500 | 47 | 2467 | 70 % | 2723 |
| hr | 2500-2600 | 80 | 2547 | 64 % | 2715 |
| hr | **2600-2700** | 72 | 2633 | 51 % | **2650** |

hr's c_local **falls** as it climbs (2809 → 2650); B's **rises** (2466 → 2830). A free two-parameter
fit on hr's 240 post-30 games (opponent range 2111-2770 — wide enough to identify s for the first
time) returns **c = 2732, s = 369**, close to the calibration-C prior; B's free fit is still
unidentified (s runs off to 1554) because B's opponent range is only 2200-2631.

Model-free equilibrium read — the rating at which each file actually scores par against the pool it
is matched into:

| file | window | own rating over the window | mean opp | WR | Elo-expected | surplus | direct r\* |
|---|---|---|---:|---:|---:|---:|---:|
| B | last 100 | 2319 → 2573 | 2450 | 77.0 % | 49.9 % | **+27.1 pp** | 2810 |
| B | last 60 | 2424 → 2573 | 2503 | 76.7 % | 49.3 % | **+27.3 pp** | 2857 |
| B | last 40 | 2481 → 2573 | 2525 | 72.5 % | 48.8 % | **+23.7 pp** | 2814 |
| hr | last 100 | 2539 → 2623 | 2615 | 58.0 % | 48.8 % | +9.2 pp | 2711 |
| hr | last 60 | 2615 → 2623 | 2634 | 50.0 % | 48.7 % | **+1.3 pp** | 2634 |
| hr | last 40 | 2625 → 2623 | 2639 | 47.5 % | 48.4 % | **−0.9 pp** | 2609 |
| hr | last 20 | 2627 → 2623 | 2651 | 45.0 % | 47.5 % | **−2.5 pp** | 2591 |

**hr has arrived.** Its last 60 games are exactly par and its last 40 are below par; its rating has
been flat at 2615-2640 for 70 games. The honest equilibrium for hr is **2620-2640**, not the 2716
that the 100-game window extrapolates — that window still contains the climb from 2539. B, by
contrast, is **+24 to +27 pp above par in every recent window**, i.e. nowhere near its equilibrium.

## 4. (ii) Does B overtake hr? — YES

Five independent reads, all pointing the same way:

| read | n | B | hr | Δ (B − hr) | t |
|---|---:|---|---|---|---:|
| fitted c, last 100 | 100 / 100 | 2817 | 2712 | **+105 pts** | — |
| fitted c, post-30 | 126 / 240 | 2723 | 2693 | +29 pts | — |
| **matched support, opp 2400-2650** | 66 / 172 | 74.2 % | 64.0 % | **+0.49 ± 0.32 logit = +145 ± 96 pts** | **+1.50** |
| **paired, the 22 opponent TEAMS both files played** | 25 / 24 games | 80.0 % | 58.3 % | **+25.0 ± 11.0 pp** | **+2.27** |
| same band, opp 2500-2600 | 30 / 77 | 73.3 % | 62.3 % | +11.0 pp (+151 pts) | +1.07 |
| same rung, g141-160 (opp ≈ 2545) | 16 / 20 | 87.5 % | 55.0 % | +32.5 pp | — |
| *older* per-bin pooled (post-30, inverse-variance) | | | | +0.14 ± 0.28 logit = +43 ± 83 pts | +0.52 |

The per-bin pooled row is the conservative one and is dragged down entirely by B's 2200-2300 bin
(44 % post-30) — the LOSS10 counter class, a band B has now left and will not re-enter. Every read
restricted to the pool that matters (2400+) puts B ahead by **+105 to +151 rating points**.

**Cross-check against the judge.** The 152-board, five-leg paired read has B − hr = **+802 coins,
SE 230, t +3.48** (consensus §95), and on the 37 LIVE-C boards inside 2550-2750 **+1,104, SE 400**.
At §115's conversion (2,000-2,300 pooled coins per +100 rating) that is **+35 to +55 rating points**
— the same sign as the ladder and inside the ladder's ±96-pt error bar. The judge and the ladder now
agree that B > hr; they disagree only on how much, and the judge is the tighter instrument.

**When does B pass hr on the scoreboard?** B is 51 pts behind and drifting **+1.75 pts/game** at
5.4 games/h while hr is flat. That is ~29 games ≈ **5-6 hours**: B should be the higher-rated file,
and therefore our leaderboard entry, by ~2026-09-12 10:00Z.

### What "a candidate replaces hr, B stays" means now

The rule was written on 09-11 when the fits said hr (2722) > B (2562) and hr was kept as the
better-calibrated measuring instrument. **The rule survives the refresh, but its justification
inverts**: hr is now the *weaker* file on every read that uses the 2400+ pool, so it is also the
right one to retire on the "replace the weaker file" principle. Three consequences:

1. **The promotion bar belongs against B, not hr.** The autojudge already runs candidates vs B; keep
   it that way. A candidate that beats hr but not B is not worth the slot, because the slot's
   occupant is about to be out-rated by B anyway.
2. **hr's remaining value is its 2600-2770 sample** — 70 games above 2600, the only ladder evidence
   we have in the band the climb must cross, and the only file that identifies `s` (free fit
   s = 369). B will supply that itself within ~2 days as it climbs past 2650, after which hr's
   instrument value is gone.
3. **Do not "promote" B into the hr slot.** B is already live and already climbing; moving it buys
   nothing and restarts a 30-game, ±100-pt ramp lottery.

## 5. (iii) Leaderboard now and the 24 h trend

Competition 147734, 8,691 teams, pulled 2026-09-12T04:15Z.

| rank | 1 | 3 | **5** | **10 (cutoff)** | 15 | 20 | 50 | 100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rating | 3198.2 | 3046.0 | **3020.2** | **2951.9** | 2932.9 | 2914.8 | 2832.7 | 2777.8 |

Our LB entry: hr, **2623.3, rank 330 / 8,691**. Density: 206 teams ≥ 2700, 75 ≥ 2800, 24 ≥ 2900,
7 ≥ 2967.

| pulled (UTC) | source | rank 1 | rank 5 | **rank 10** | rank 20 | teams |
|---|---|---:|---:|---:|---:|---:|
| 09-11 02:03Z | `S/calib2/lb.json` | 3142.3 | 3015.8 | **2955.8** | 2906.5 | 8,589 |
| 09-11 07:43Z | `S/flow198/lb.json` | 3107.1 | 3006.8 | **2950.6** | 2898.9 | 8,607 |
| 09-11 10:09Z | `S/top50/lb.json` | 3099.2 | 3012.9 | **2943.1** | 2903.9 | 8,619 |
| 09-11 22:39Z | `S/nextband/lb.json` | 3152.9 | 2998.0 | **2970.0** | 2913.4 | 8,674 |
| 09-12 02:19Z | `S/band40/lb.json` | 3179.5 | 3025.0 | **2953.2** | 2919.5 | 8,686 |
| 09-12 03:31Z | `S/nexthigh/lb.json` | 3193.0 | 3022.4 | **2951.9** | 2913.9 | 8,688 |
| **09-12 04:15Z** | `S/ladder2/lb.json` | **3198.2** | **3020.2** | **2951.9** | 2914.8 | **8,691** |

**The cutoff is not trending — it is oscillating.** Over 26 h it has gone
2955.8 → 2950.6 → 2943.1 → 2970.0 → 2953.2 → 2951.9, i.e. **2955 ± 13 with no drift**
(+1.5 pts/day over the last 21 h, well inside the swing). The earlier "2943 → 2967" reading was two
samples of that oscillation, not a rise. Rank 5 is up **+13** (3006.8 → 3020.2) over 21 h, also
inside its own ±14 swing. The one real trend is **rank 1: 3099 → 3198 in 18 h (+99)**, a single team
on a streak, which does not move the cutoff.

**Planning number: treat the top-10 cutoff as 2952 ± 15 and rank 5 as 3020 ± 15**, flat.

## 6. (iv) The honest 11-day outlook to 2026-09-23

10.8 days left = ~1,400 more games for B, ~1,510 for hr. Both files reach their equilibrium in
~2-3 days, so the 09-23 rating **is** the equilibrium; the remaining 8 days add nothing.

| file | c | r now | games left | **rating at 2026-09-23** | c at CI low | CI high | rank at the point estimate |
|---|---:|---:|---:|---:|---:|---:|---|
| **B** | 2817 | 2573 | ~1,394 | **2818** | 2679 | 2969 | **~63** |
| **hr** | 2712 | 2623 | ~1,508 | **2716** (honest: **2620-2640**, §3) | 2607 | 2831 | ~179 (honest: ~330) |

Neither file reaches the 2952 cutoff. B's point estimate is **134 short**; only the top of B's CI
(2969) touches rank ~8, and that CI edge is an 8-game-per-bin artefact. **P(top-10 with the files we
have now) ≈ 0.**

### What a replacement candidate in the hr slot would need

A new submission starts at **600** and runs the measured K schedule (`S/calib2/kschedule.json`:
~220 for g1-15, ~40 at g30, ~11.6 at g60, floor 8.9 from ~g78). At hr's rate it gets ~1,509 games
before 09-23 — **5× more than the ~260-315 it needs to converge**, so the deadline is not binding
and the target rating is simply the candidate's equilibrium.

| target by 09-23 | required c | vs **hr** (2712) | pooled band Δmargin vs hr (§115: 2,000-2,300 coins per +100) | vs **B** (2817) | **pooled band Δmargin vs B** | t on the 90-board leg (SE 218) |
|---|---:|---:|---:|---:|---:|---:|
| 2750 (rank ~130) | **2746** | +34 | +690 … +790 coins | **−71** | **−1,420 … −1,630** (B already clears it) | — |
| 2850 (rank ~40) | **2846** | +134 | +2,690 … +3,090 coins | **+29** | **+580 … +670 coins** | **+2.7 … +3.1** |
| 2967 (rank ~8) | **2963** | +251 | +5,030 … +5,780 coins | **+146** | **+2,920 … +3,360 coins** | **+13.4 … +15.4** |

The "vs B" column is the operative one, because the autojudge measures candidates against B and
because B is the file that will define our position by tonight.

**Read that table against what has ever been measured.** The largest pooled judge gain we have
produced in the whole campaign is B over hr: **+802 coins (t +3.48) over 152 boards**, on the
90-board band subset **+1,104 (SE 400)**. So:

- **2750 is already done** — B's own equilibrium is 2818, 68 pts past it.
- **2850 needs +580-670 pooled coins over B (t ≈ +2.7-3.1)** — *one more promotion of the same size
  as the entire B-over-hr step*. This is the realistic 11-day target. It is rank ~40.
- **2967 needs +2,920-3,360 pooled coins over B (t ≈ +13-15)** — **3.6× the whole B-over-hr
  improvement, in 11 days**, and t +13 has never been observed on any leg. The §115 promotion rule's
  own resolution floor (t = 2 at ±436 coins ≈ ±27 rating) means we could not even *certify* such a
  jump in one step; it would take ~5 sequential promotions each at the current best size.

**Verdict on the 2026-09-23 top-10 goal: not reachable on the current rate of improvement.** The
binding constraint is not ladder mechanics (K = 8.9 is fine — a candidate converges in 2 days and
has 11), and it is not the cutoff moving away (it is flat at 2952 ± 15). It is strength: we need
+146 rating = ~+3,000 pooled band coins over B, and the campaign's best single step to date is
+802. The honest 11-day plan is **B to ~2818 (rank ~63) by 09-14 on its own, plus one or two
promotions of B-over-hr size to reach 2850-2900 (rank ~25-40)**.

## Caveats

1. **s = 298 is a prior, not a measurement.** hr's free fit (240 games, opponent range 2111-2770)
   now returns s = 369, the first genuinely identified estimate; at s = 369 every Δ in rating points
   above scales up by 24 %. B's range (2200-2631) still cannot identify s.
2. **B's c is a 100-game read on a rising pool** and its own-rating slices rise monotonically
   (2466 → 2830), which is exactly the shape a *still-unconverged* file makes; it is also the shape
   a file makes if the low-rating LOSS10 band is a genuine counter-class rather than noise. Both
   stories predict the same thing going forward (B climbs); they differ on the CI, not the sign.
   Re-read B once it has 40 games above opponent 2600 (it has 3).
3. **B has never met an opponent above 2631, hr never above 2770.** Everything said about 2800+ play
   is judge extrapolation (TOPB2), not ladder evidence. The 2967 row of the table above is the
   weakest row in this document.
4. **The §115 coins-per-rating conversion (2,000-2,300 per +100) is itself derived from s = 298** and
   from the margin→win slopes in `S/bandgrad/rows.csv`. It is a one-significant-figure instrument.
5. **Leaderboard snapshot times are file mtimes**, accurate to the minute but pulled opportunistically
   by other tools, so the trend is unevenly spaced.
6. B's "Δ24h" is its whole life — B's first game was 2026-09-11T07:33Z, 21 h before this pull.
