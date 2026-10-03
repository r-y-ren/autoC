## Validation against V37

Every comparison uses the same opponents, worlds and seats. W/L/T means
wins, losses and ties. Win rate counts outright wins; points count a tie
as half a win. Mean margin is our final cash minus the opponent's cash.

| Cohort and policy | W/L/T | Win rate | Points | Mean margin |
|---|---:|---:|---:|---:|
| Recorded development (648) — V37 | 440/208/0 | 67.90% | 67.90% | 13,226.63 |
| Recorded development (648) — V38 | 477/171/0 | 73.61% | 73.61% | 14,288.46 |
| Whole V37 live cohort (97) — V37 | 63/28/6 | 64.95% | 68.04% | 7,601.19 |
| Whole V37 live cohort (97) — V38 | 80/17/0 | 82.47% | 82.47% | 8,824.08 |
| Reacting development (704) — V37 | 609/67/28 | 86.51% | 88.49% | 33,991.22 |
| Reacting development (704) — V38 | 646/58/0 | 91.76% | 91.76% | 35,048.32 |
| New elite records (144) — V37 | 85/59/0 | 59.03% | 59.03% | 11,154.53 |
| New elite records (144) — V38 | 96/48/0 | 66.67% | 66.67% | 12,241.33 |
| New reacting worlds (2,816) — V37 | 2562/124/130 | 90.98% | 93.29% | 33,727.85 |
| New reacting worlds (2,816) — V38 | 2718/98/0 | 96.52% | 96.52% | 34,885.51 |

The source was frozen before selecting 144 unused elite
records from 18 current teams rated at least 2900. Each team
contributes eight completed, non-self-play records selected without an
outcome filter. Previously used records and worlds were excluded.

On those records, the points gain is **7.64 percentage points**
with a team-clustered 95% bootstrap interval of [2.08,
16.67] percentage points. The mean-margin gain
is **1,086.81**.

Outcome gains occur in 6 of the 18 teams,
with 0 teams losing points. Mean cash margin
improves against all 18 teams in this sample.

A separate confirmation uses all 44 fixed public policies on 32 previously
unused worlds in both seats: 2,816 games per agent. The world-clustered
95% interval for the points gain is [2.24,
4.23] percentage points, with a mean-margin gain
of **1,157.66**. Equal-weight family checks also pass.

V38 retains 2,562 V37 wins in this reacting sample,
converts 50 losses and 106 ties into wins,
and turns 24 former ties into losses. World-level points improve
in 27 worlds, stay equal in 1,
and decline in 4. The aggregate gain is not a promise
of improvement in every individual game.

Recorded opponents replay their original actions, so the separate reacting
panel is essential. Development results are reused research data and are
not counted as independent confirmation. Local results do not establish
a guaranteed live rating.

## Physical and operational checks

- Complete paired accounting across 745 development cases: cash, products,
  crop output, hire locations and worker arrivals reconcile with the engine.
- 312,065 original-animal comparisons show no additional animal loss.
- 13,310 checks preserve or improve the original tomato output.
- The actual official-loader entry point matches the tested policy;
  observations and shared route data remain unchanged, all thirteen routes
  are covered, and malformed inputs return a safe action.
- Complete self-play and starter games finish with DONE status.
- Isolated timing uses a fresh process per game and normal garbage collection.

| Timing check | Maximum callback |
|---|---:|
| Windows observation replay | 41.585 ms |
| Linux observation replay | 26.373 ms |
| Windows complete-game stress cases | 25.665 ms |
| Linux replay of complete-game stress cases | 23.030 ms |

All measured callback maxima are below 50 ms on the test machine.

| Historical regression gate | W/L/T | Win rate | Points | Mean margin |
|---|---:|---:|---:|---:|
| Top-rated recorded field (120) | 115/5/0 | 95.83% | 95.83% | 20,764.65 |
| Opponent recorded field (150) | 146/4/0 | 97.33% | 97.33% | 24,373.15 |
| Nine-policy arena (108) | 108/0/0 | 100.00% | 100.00% | 13,788.44 |
| Thomas 95.5 subset (12) | 12/0/0 | 100.00% | 100.00% | 8,081.33 |

Frozen agent SHA-256: `a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e`.
Source and archive hashes are checked by the executable cells above.
