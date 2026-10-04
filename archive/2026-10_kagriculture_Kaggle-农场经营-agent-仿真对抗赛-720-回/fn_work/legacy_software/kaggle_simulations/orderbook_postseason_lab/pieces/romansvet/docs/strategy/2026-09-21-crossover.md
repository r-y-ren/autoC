# Head/policy/opponent crossover

Fixed CRN, seed 266940; 96 boards x both seats = 192 episodes/cell. Reference within each opponent is head_940 greedy. `KAGG3_HEAD_LAYOUT=v1`.

| opponent | head | policy | tie-win | paired Δwin | mean ours | mean theirs | gift vs ref |
|---|---|---:|---:|---:|---:|---:|---:|
| BAND tapes | head_940 | sampled | 94.79% | -1.04 pp | 111900.8 | 94746.4 | +521.8 |
| BAND tapes | head_940 | greedy | 95.83% | +0.00 pp | 111662.0 | 94224.7 | +0.0 |
| BAND tapes | head_500 | sampled | 95.31% | -0.52 pp | 111974.6 | 94627.2 | +402.5 |
| BAND tapes | head_500 | greedy | 95.83% | +0.00 pp | 111844.3 | 94224.0 | -0.7 |
| incumbent head_940 | head_940 | sampled | 50.00% | +0.00 pp | 107199.3 | 107454.1 | +34.1 |
| incumbent head_940 | head_940 | greedy | 50.00% | +0.00 pp | 107419.9 | 107419.9 | +0.0 |
| incumbent head_940 | head_500 | sampled | 52.34% | +2.34 pp | 107343.8 | 107328.9 | -91.1 |
| incumbent head_940 | head_500 | greedy | 50.52% | +0.52 pp | 107404.0 | 107527.4 | +107.5 |

| head | BAND disagreement | incumbent disagreement | pooled |
|---|---:|---:|---:|
| head_940 | 20.23% | 21.93% | 21.08% |
| head_500 | 27.90% | 27.55% | 27.72% |

A — not supported: head_500 sampled Δs are -0.52/+2.34 pp and greedy Δs are +0.00/+0.52 pp (BAND/incumbent); not sampled-only.
B — supported (weak): head_500 greedy Δ is +0.52 pp vs incumbent and +0.00 pp vs BAND, consistent with opponent targeting.
C — not supported: the B pattern appears, so residual exhaustion is not the point-estimate diagnosis.

Runtime: 1515.7 s.
