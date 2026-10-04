## Measured results

W/L/T means wins, losses and ties. Win rate counts outright wins. Mean margin is our final cash minus the opponent’s final cash. Every comparison keeps opponents, worlds and seats matched.

| Cohort / agent | W/L/T | Win rate | Mean margin |
|---|---:|---:|---:|
| Recorded development (1,136) — V38 | 762/374/0 | 67.08% | 11,622.16 |
| Recorded development (1,136) — V39 | 793/343/0 | 69.81% | 12,041.05 |
| Public development (736) — V38 | 663/59/14 | 90.08% | 35,927.46 |
| Public development (736) — V39 | 695/41/0 | 94.43% | 36,370.47 |
| Original independent records (256) — V38 | 145/111/0 | 56.64% | 11,380.84 |
| Original independent records (256) — V39 | 147/109/0 | 57.42% | 11,781.90 |
| Additional reacting stress (1,472) — V38 | 1387/57/28 | 94.23% | 36,537.56 |
| Additional reacting stress (1,472) — V39 | 1433/39/0 | 97.35% | 36,868.80 |

### Original independent result

The source was fixed before selecting 256 unused records from 16 teams rated at least 2900, with sixteen records per team and no outcome filter. Both recorded rewards reproduced exactly in all 256 cases. The source remains unchanged.

V39 gained 3 wins and lost 1 previously won game(s): **0.78 percentage points** more match points. Mean final cash increased by **477.04** and margin by **401.06**. The whole-team 95% bootstrap interval for the points change is **[-0.78, 2.34] percentage points**.

The original requirements of at least one percentage point and a strictly positive points-confidence bound were not met. V39 is provided as a submission candidate with that uncertainty disclosed; this result has not been relabeled as a passed statistical promotion gate.

### Additional reacting stress

After selecting this unchanged candidate for packaging, all 46 fixed public policies were tested on 16 additional unused worlds in both seats: 1,472 games per agent. These worlds were fixed before execution and exclude all previously used or reserved worlds. This stress test does not replace the original independent result.

The stress comparison changes match points by **2.17 percentage points**, with a whole-world 95% interval of [1.15, 3.53]. Mean cash changes by **+291.58** and margin by **+331.24**. Aggregate and policy-family regression checks pass.

Recorded opponents replay their original actions; the separate public panels respond to changed game state. Reused development cohorts and technical replays do not add independent statistical sample weight.

## Physical and runtime validation

The consumed development cohort has 2,502 paired physical records. The entire 256-record independent cohort additionally passes 768 instrumented runs of V39, V38 and the preceding calendar control. Cash and product ledgers reconcile, original rewards match, crop forecasts reconcile per game, and native input, animal survival and parent crop checks pass.

Against the preceding calendar control, early input delivery was restored in 82 development games across 40 teams: 120 failed feeds and 122 missing wheat pickup units were restored. No additional native input or animal-loss violations were found.

The actual official-loader entry matches the tested policy. All thirteen routes are covered, observations and shared routes remain unchanged, and shared/separate self-play and starter games finish with DONE status. Timing uses fresh processes with normal garbage collection.

| Isolated timing | Maximum callback |
|---|---:|
| Windows observation replay | 42.356 ms |
| Linux observation replay | 20.383 ms |
| Windows complete-game stress | 20.186 ms |
| Linux replay of complete-game stress | 20.033 ms |

All measured maxima are below 50 ms on the test machine.

## Historical regression checks

| Gate | W/L/T | Win rate | Mean margin |
|---|---:|---:|---:|
| Top field (120) | 115/5/0 | 95.83% | 21,186.14 |
| Opponent field (150) | 147/3/0 | 98.00% | 24,705.51 |
| Arena (108) | 108/0/0 | 100.00% | 14,071.44 |
| Thomas 95.5 subset (12) | 12/0/0 | 100.00% | 8,310.00 |

The reused 32-world mirror against V37 is a regression check, in both seats.

| Against V37 | W/L/T | Win rate | Mean margin |
|---|---:|---:|---:|
| V38 | 54/10/0 | 84.38% | 1,289.67 |
| V39 | 56/8/0 | 87.50% | 1,728.58 |

Agent SHA-256: `708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8`.
