## 26. Fresh paired experiment · 22 September 2026

### Policy changes and why they might help

1. **Sale lookahead 4:** sell already available cash products up to four turns before their scheduled sale, keeping the inherited funding and field-action protections.
2. **Seed hedge 0:** after the final useful planting window, buy only the remaining planned seed requirement rather than an extra two wheat seeds.
3. **Stable queue compaction:** use the visible own-state simulation to close empty or provably dead market slots, preserving the order of live operations. A purchase makes later same-item stock uncertain, so the compactor keeps those orders. Its advantage is earlier execution against competing sales; its risk is purchasing before a rival lowers a commodity price.
4. **Explicit final entrypoint:** Kaggle's source loader must select the intended policy. We caught an unsealed prototype selecting a helper instead; the exact deployed source ends with a verified final entrypoint.

### Discovery and genuinely unseen confirmation

A frozen six-arm discovery used 672 games: eight seeds, seven opponents, both seats. The selected combination improved paired mean margin by +224.813. Its win-point gains in that screen came from facing the unchanged public source; all six other opponent groups were already at a win ceiling. These discovery rows called the intended exported agent. They were selection evidence, not a deployment test for the unsealed file.

A separately frozen **448-game holdout** tested the final sealed source through the actual Kaggle loader. It used **16 new seeds × 7 opponents × 2 seats × 2 arms**. Every game finished DONE/DONE with 720 states and 719 measured calls per agent. All frozen source, engine, runner and coverage checks passed.

| Held-out arm | Games | Wins | Ties | Losses | Mean money margin | Worst margin |
|---|---:|---:|---:|---:|---:|---:|
| Current combination | 224 | 196 | 0 | 28 | +716.161 | -1,135 |
| Unchanged public source | 224 | 157 | 30 | 37 | +629.402 | -857 |

Counting a tie as half a win, the paired gain is **+10.714 percentage points**, with **+86.759 mean money margin**. Directly against the public source, the new policy wins **28/32** games. It gains 12 wins across the other six controls combined, with no opponent group losing win rate.

### Limits and counterexamples

This is a candidate for an official experiment, not a top-10 prediction. Against public2945 the mean margin falls by 14.063 while the 30W/2L result is unchanged. Across individual matched games, 100/224 margins decrease; seven of sixteen seed-group means decline. The worst seed-group mean change is -655.143. The worst game margin is also worse than the baseline's. Descriptive whole-seed bootstrap 95% intervals include zero: approximately -4.46 to +27.68 percentage points for win-point gain and -100.26 to +281.91 for margin gain. Mirrored seats must not be counted as independent evidence.

The opponents are executable public policies, not the private current top-ten agents. The observations used by the extension are legal visible state; it has no identity, hidden seed, network or file inputs. Upstream source and Apache notices are retained. A later experiment should test commodity-timing anchors and final-day liquidation, without silently changing this source.

Run the next cell to reconstruct all matched rows, reproduce the per-opponent and per-seed plots, and export `paired_evidence.csv`. The exported `main.py` is the exact source tested in this holdout. The current candidate has no official score yet.


Full terminal receipt SHA256: `cdcf078fbbd8d78b5b01a9936a03cdd40214311613d90896f96205ed55c28ead`. The executable rows below are derived from this receipt.