# Failure probe: measured evidence (auto-generated)

- generated: 2026-08-28 18:42:28 by scripts/analyze_failure_modes.py
- probe: submission (p0) vs each pool opponent, seeds 201..208, full 720-step episodes
- games: 64 in 0s; replay log: exports/logs/failure_probe_log.jsonl

## Per-opponent summary (most threatening first)

| opponent | W-L-T | win rate | avg margin | min margin | closest seed | days behind (worst) | FERT $<=5 crash day |
|---|---|---|---|---|---|---|---|
| melon_hoarder | 0-8-0 | 0.0 | -5460 | -6659 | 203 | 29 | - |
| cow_baron | 1-7-0 | 0.125 | -15920 | -33272 | 202 | 28 | - |
| expansionist | 8-0-0 | 1.0 | +11012 | +9421 | 204 | 10 | - |
| baseline_wheat | 8-0-0 | 1.0 | +17575 | +16194 | 205 | 13 | - |
| greedy_carrot | 8-0-0 | 1.0 | +23521 | +20120 | 207 | 13 | - |
| starter | 8-0-0 | 1.0 | +27566 | +25976 | 205 | 12 | - |
| pass | 8-0-0 | 1.0 | +28129 | +26916 | 205 | 11 | - |
| random | 8-0-0 | 1.0 | +31701 | +30060 | 201 | 10 | - |

## Closest / lost games (evidence detail)

### submission vs cow_baron seed=202 -- LOSS (margin -33272)
- final: 27281 vs 60553; min gap -33272 on day 29; days behind: 28 (d2-d29)
- market: FERT<=5 from day None; MELON floor 232 (0 days < gate 150); EGG floor 41
- money gap by day (sub - opp): [740, -355, -1422, -5838, -12023, -10746, -19803, -24184, -29840, -29659] (every 3rd day)

### submission vs cow_baron seed=205 -- LOSS (margin -30112)
- final: 27550 vs 57662; min gap -30473 on day 25; days behind: 28 (d2-d29)
- market: FERT<=5 from day None; MELON floor 231 (0 days < gate 150); EGG floor 42
- money gap by day (sub - opp): [740, -355, -1422, -5635, -11389, -9874, -18451, -22389, -28252, -25834] (every 3rd day)

### submission vs cow_baron seed=206 -- LOSS (margin -25034)
- final: 27775 vs 52809; min gap -25034 on day 29; days behind: 28 (d2-d29)
- market: FERT<=5 from day None; MELON floor 232 (0 days < gate 150); EGG floor 41
- money gap by day (sub - opp): [740, -355, -1423, -5379, -10403, -7971, -15652, -18836, -22932, -21374] (every 3rd day)

### submission vs cow_baron seed=201 -- LOSS (margin -20207)
- final: 27349 vs 47556; min gap -20853 on day 25; days behind: 28 (d2-d29)
- market: FERT<=5 from day None; MELON floor 232 (0 days < gate 150); EGG floor 41
- money gap by day (sub - opp): [740, -355, -1422, -5360, -10356, -7518, -14337, -16634, -19681, -17062] (every 3rd day)

### submission vs cow_baron seed=208 -- LOSS (margin -7668)
- final: 29377 vs 37045; min gap -11574 on day 25; days behind: 28 (d2-d29)
- market: FERT<=5 from day None; MELON floor 232 (0 days < gate 150); EGG floor 44
- money gap by day (sub - opp): [740, -355, -1423, -4810, -6233, -321, -5138, -7726, -11185, -6180] (every 3rd day)

### submission vs cow_baron seed=204 -- LOSS (margin -7486)
- final: 29132 vs 36618; min gap -11445 on day 25; days behind: 26 (d2-d13; d16-d29)
- market: FERT<=5 from day None; MELON floor 232 (0 days < gate 150); EGG floor 47
- money gap by day (sub - opp): [740, -355, -1398, -4627, -5899, 246, -4572, -7276, -11071, -5948] (every 3rd day)
