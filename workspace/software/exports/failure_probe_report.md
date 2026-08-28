# Failure probe: measured evidence (auto-generated)

- generated: 2026-08-28 20:24:03 by scripts/analyze_failure_modes.py
- probe: submission (p0) vs each pool opponent, seeds 201..208, full 720-step episodes
- games: 64 in 178s; replay log: exports/logs/failure_probe_log.jsonl

## Per-opponent summary (most threatening first)

| opponent | W-L-T | win rate | avg margin | min margin | closest seed | days behind (worst) | FERT $<=5 crash day |
|---|---|---|---|---|---|---|---|
| cow_baron | 6-2-0 | 0.75 | +3996 | -3587 | 206 | 27 | - |
| melon_hoarder | 7-1-0 | 0.875 | +21091 | -1413 | 208 | 22 | - |
| greedy_carrot | 8-0-0 | 1.0 | +38123 | +14747 | 207 | 10 | - |
| expansionist | 8-0-0 | 1.0 | +40138 | +14949 | 207 | 7 | - |
| baseline_wheat | 8-0-0 | 1.0 | +42727 | +12984 | 202 | 12 | - |
| starter | 8-0-0 | 1.0 | +49867 | +17823 | 204 | 10 | - |
| random | 8-0-0 | 1.0 | +55814 | +30823 | 207 | 9 | - |
| pass | 8-0-0 | 1.0 | +63875 | +49527 | 207 | 10 | - |

## Closest / lost games (evidence detail)

### submission vs cow_baron seed=206 -- LOSS (margin -3587)
- final: 16248 vs 19835; min gap -4759 on day 9; days behind: 27 (d3-d29)
- market: FERT<=5 from day None; MELON floor 256 (0 days < gate 150); EGG floor 50
- money gap by day (sub - opp): [1199, -455, -1447, -4759, -4717, -2529, -2156, -2373, -2818, -3004] (every 3rd day)

### submission vs cow_baron seed=204 -- LOSS (margin -3213)
- final: 16732 vs 19945; min gap -4887 on day 9; days behind: 27 (d3-d29)
- market: FERT<=5 from day None; MELON floor 256 (0 days < gate 150); EGG floor 50
- money gap by day (sub - opp): [1199, -455, -1105, -4887, -4858, -2087, -2125, -2826, -3368, -2772] (every 3rd day)

### submission vs melon_hoarder seed=208 -- LOSS (margin -1413)
- final: 34096 vs 35509; min gap -12600 on day 13; days behind: 22 (d0-d9; d13-d22; d26-d26; d29-d29)
- market: FERT<=5 from day None; MELON floor 120 (1 days < gate 150); EGG floor 50
- money gap by day (sub - opp): [-12, -1363, -1726, -1078, 2741, -9864, -5269, -1082, 3601, 461] (every 3rd day)

### submission vs cow_baron seed=201 -- WIN (margin +1796)
- final: 29799 vs 28003; min gap -6605 on day 12; days behind: 17 (d3-d19)
- market: FERT<=5 from day None; MELON floor 256 (0 days < gate 150); EGG floor 50
- money gap by day (sub - opp): [1199, -455, -1447, -4760, -6605, -4978, -558, 2597, 2138, 461] (every 3rd day)

### submission vs cow_baron seed=208 -- WIN (margin +4458)
- final: 35348 vs 30890; min gap -6849 on day 15; days behind: 20 (d3-d22)
- market: FERT<=5 from day None; MELON floor 256 (0 days < gate 150); EGG floor 50
- money gap by day (sub - opp): [1199, -455, -1447, -4759, -6651, -6849, -4959, -1616, 2617, 3444] (every 3rd day)

### submission vs cow_baron seed=205 -- WIN (margin +5134)
- final: 31224 vs 26090; min gap -5007 on day 11; days behind: 15 (d3-d17)
- market: FERT<=5 from day None; MELON floor 256 (0 days < gate 150); EGG floor 50
- money gap by day (sub - opp): [1199, -455, -1447, -4758, -4605, -2361, 776, 1959, 2302, 4368] (every 3rd day)
