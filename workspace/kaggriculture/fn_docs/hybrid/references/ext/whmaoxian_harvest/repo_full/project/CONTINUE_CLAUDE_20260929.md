# Claude continuation 2026-09-29 (night)

Online (user-submitted): R2 resub 56674897 and R3 (id unknown) around 12:15 UTC 2026-09-29; old R2 is 56581759.

LIVE: R4.2 = 56683114 and R3 resub = 56683134. R5 (= R4.3 code, submissions/release_v10_r5) replaces the R3 slot. Use FIXSHOPS=1 in surrogate.py/surrogate2.py: shop draws depend on empty-tile counts (RNG butterfly effect).
- R4 = R3 + night-overflow layer running all day, selling WHEAT/FERTILIZER only, margin 15.
- Surrogate on 195 real online games: R2 114-81, R3 122-73, R4 135-60.

Surrogate tool: research/claude_20260929/surrogate.py (team MauoXX). Episode sets are pool.txt and holdout.txt; all195.txt holds the ids of both.
Kaggle ListEpisodes rate-limits hard (429 for hours) after bursts; the replay download endpoint was not limited.
Details: research/claude_20260929/REPORT.md section 11.
