---
name: rating-equilibrium
description: Where g60_pair and g170c_pair would settle on the ladder, and the win rate top-10 (cutoff ~2880) actually requires
metadata:
  type: analysis
---

## Rating-update behaviour from the log

`S/kagwatch/56098262.log` (187+ settled games, current rating 1952.7-1966.5) shows a 1W-6L stretch (2026-09-09 10:11-11:58Z) during which rating rose 1952.7→1966.5. At n≈200 games the per-game K is small enough that short streaks barely move the rating (no per-game before/after deltas are logged, so K isn't separably identifiable from this file); win/loss records for individual games (24 in the window) show avg opponent rating on wins (2001) *higher* than on losses (1983) — rating diffs of ~100 pts carry little signal at this scale. No formula is documented in kaggle-episode-api.md or kagg3-optimisation-log.md beyond "starts at 600, climbs by streak" (kaggle-top-tier-2026-08-28.md). Given this, per-game K/Elo-divisor fitting is unreliable; the equilibrium below is built from **tier win rates**, not single-game deltas — consistent with how a maturing leaderboard rating actually settles (win rate ≈50% against same-rating opponents).

## Model

`p(win|R) = logistic(a + b·R)` fit per candidate from two tier reads (band center 1975 = "1950-2000"; top center 2902 = "2850-2954"), band values calibrated live-theta-board→field via the logit shift measured on live theta (board 34.5%→field 43% vs ≥1800, Δlogit=+0.359, applied to g60/g170c band reads only; top-tier TOP20 reads used raw/in-sample, no field anchor exists there). r* solves p=0.5.

| Candidate | Band (calibrated) | Top (raw) | Fitted D (1/slope) | r* | ±1 SE band (from top-tier N≈20) |
|---|---|---|---|---|---|
| live theta | 43.0% | 20% | 839 | **≈1740** | 1550–1830 |
| g60_pair | 72.2% | 35% | 589 | **≈2540** | 2400–2760 |
| g170c_pair | 73.9% | 30% | 491 | **≈2490** | 2370–2650 |

Sanity check: live theta's fitted r* (≈1740) undershoots its actual stable rating (~1950) by ~200 pts. The gap is the extrapolation itself — a straight line in log-odds over a 927-pt gap, anchored on a thin N≈20 top-tier read, is a poor proxy for the true (likely concave/regime-changing) curve; top-tier play requires the late shop-adaptive mix edge documented in kaggle-top-tier-2026-08-28.md, not a simple extension of band-level strength. Treat r* as order-of-magnitude, biased low by roughly this same ~200 pt margin for all three rows.

## Where the two lead packages settle

Bias-corrected (+~200 pts to match the live-theta sanity check): **g60_pair ≈ 2700-2750, g170c_pair ≈ 2650-2700** (uncorrected central estimates 2540/2490, ±150-250 SE). Both sit below the top-10 cutoff (~2880); neither central estimate nor its 1-SE upper bound (2760/2650, or ~2950/2900 bias-corrected) reliably clears it — g60_pair is the stronger candidate, plausibly borderline top-10 in the optimistic tail, g170c_pair falls short.

## What top-10 (hold r=2880) actually requires

Opponents are matched ±150 around own rating, so holding equilibrium at r means p(win)=50% against opponents centered at r. The task's 2700-2950 tier (center 2825) sits 55 pts below 2880 itself, so using the fitted D≈490-590 (top-tier candidates): **required raw win rate vs the 2700-2950 tier ≈ 52-53%**, not the naive 50%. Current in-sample reads are 30% (g170c) and 35% (g60) — both roughly 17-23 points short of the bar. Reaching top-10 needs a further strength gain equivalent to ~350-400 rating points beyond the current best candidate (g60_pair), concentrated in the same late-game adaptive-mix edge (tomato/carrot/egg sink timing, melon-dump timing) already identified as the top-tier wall, not further band-tier optimisation.
