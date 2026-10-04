# Round 8 market research: keep v7 unchanged after a rejected candidate

2026-09-22. Scope: only the six `split=study` episodes in `research/round7/top2/index.json` were used for the market diagnostics. The six held-out episodes were not used. No upstream release or root main.py was changed.

## Findings

The frozen v7 Orderbook layer never fills `_CXD_MODELS`. It therefore assumes that the rival submits our own order list. `_v44y_factor_margin` also supplies our own projected shed as the rival's stock. That is a useful mirror-match model, not a general rival model. DSM and Vadim have different production layouts, so its claimed relative-profit gain is not reliable against them.

Simply replacing that assumption with repeated sale cycles is also unreliable. On actual successful sales from six exactly reconstructed study replays, a milk sale forecast based on sales one and two 48-turn cycles earlier matched within one turn only 27%–71% of the time. Wool's corresponding 72-turn recurrence matched only 8%–74%. Egg recurrence was much better (79%–100% in five producing examples), but low-price eggs alone are not the main rating gap. These rates count overlapping forecast windows, not independent events, and are diagnostic rather than calibrated probabilities.

## How much can order sorting alone gain?

For each historical own action, hold production and selling time fixed and permute only existing SELL slots, without disturbing purchase chains. The diagnostic uses the rival's actual same-turn actions and private stock as an omniscient oracle. Those inputs are forbidden to the deployed candidate and appear only in the offline audit. Its immediate margin calculation ignores shared cash limits, as does the inherited order model; it is not a forecast of final match winnings.

| Team / study episode | Best oracle immediate margin improvement summed over the trajectory | Mirror model's claimed improvement | Mirror model's actual improvement under the oracle |
|---|---:|---:|---:|
| Vadim / 111917373 | 70 | 97 | -7 |
| Vadim / 111910148 | 191 | 158 | 16 |
| Vadim / 111903848 | 220 | 177 | 69 |
| DSM / 111918050 | 96 | 146 | -107 |
| DSM / 111915821 | 62 | 110 | 17 |
| DSM / 111910412 | 326 | 147 | 110 |

This quantifies a real model weakness, but the conditional improvement is only 62–326 coins in these six historical trajectories. It does not bound the value of moving sales across turns or changing production. It does indicate that priority should go to production and cross-turn supply timing rather than a much larger permutation search.

## Candidate and paired screening

`round8_market_recurrence.py` is frozen v7 plus a separately auditable suffix. It uses only current-match public market deltas already inferred by v7. For visibly non-mirror farms, two repeated biological sale cycles create rival scenarios at unknown order slots 0, 1 and 2. Scenarios use their own estimated stock rather than our shed. Only existing SELL orders can exchange slots. An alternative is rejected if it sacrifices the inherited mirror-model margin, so no new sale, purchase or physical action is introduced.

Candidate SHA-256: `605e17eb4e006054453f7859ef01885a85954339b982be92cd0dbb8f9f3db1fb`.

Exactly 12 full simulations were run sequentially: v7 and candidate each played seeds 81000, 81001, 81002 in both seats against `effective_111918050.py`. The opponent is a reactive execution program compiled from a DSM public historical production route; it is not DSM's private live agent. This is six paired results from three worlds, not twelve independent worlds.

| Seed | v7 money margin in each seat | Candidate money margin in each seat | Paired improvement |
|---|---:|---:|---:|
| 81000 | +22144 | +22144 | 0 |
| 81001 | +37143 | +37143 | 0 |
| 81002 | -7413 | -7413 | 0 |

Both versions finished 4 wins / 2 losses. The added model was invoked 24 times over six candidate games but accepted zero order changes. All games reached DONE / DONE, both sides had no stderr, all exposed top-level error/fallback counters and chassis counters were zero. Slowest recorded action over all 12 games was 0.184 seconds on this host. The candidate should be rejected as non-improving, not marketed as a stronger new version.

## Artifacts and reproduction

- Build: `experiments/round8_market_build.py`; suffix: `experiments/round8_market_recurrence_suffix.txt`.
- Successful-trade recurrence audit: `experiments/round8_market_audit.py`; `results/round8_market_recurrence_audit.json`.
- Offline order ceiling: `experiments/round8_market_oracle_audit.py`; `results/round8_market_oracle_audit.json`.
- Paired full-game screening: `experiments/round8_market_screen.py`; `results/round8_market_screen.json`.

Run the relevant script using the existing `.venv/Scripts/python.exe`. Candidate construction asserts the exact frozen v7 hash before appending the suffix. It inherits and retains all v7 source/license attribution. No online submission was made.
