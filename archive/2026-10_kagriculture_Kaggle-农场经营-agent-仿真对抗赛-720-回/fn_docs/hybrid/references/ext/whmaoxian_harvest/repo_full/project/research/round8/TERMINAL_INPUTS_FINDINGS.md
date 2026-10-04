# Round 8 terminal input audit: reject as non-improving

2026-09-22. This subtask reviewed busyaprime's seed-float and fertilizer-knockout tail, retained under explicit Apache-2.0 comments in [The 2965 Master Hybrid Engine, notebook v4](https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine). The returned notebook metadata does not separately expose a license field. The source comments and all prior notices were preserved; this is not a claim that the tail or its underlying ideas are original local inventions.

## What can and cannot be concluded

With 24 turns/day and the last executed step718, wheat/carrot planted after step671 cannot mature in time. A seed purchase at step671 occurs after physical actions and therefore cannot fund a productive planting. Dropping purchases after that boundary preserves any productive planting, provided order slots remain unchanged. Before the boundary, a conservative cap may retain enough of EACH seed type for every future potentially productive PLANT opportunity plus queued retries; this does not assume that today's prices will determine all later wheat/carrot conversions.

The public seed-float tail does make that current-price assumption, leaves only a small wheat hedge, and does not count queued PLANT retries. It also removes empty orders, which can move simultaneous trading slots. Those details were not copied.

Unconditionally dropping fertilizer purchases on the final day is not an agronomic guarantee. In an exact-physical-model check, wheat planted on day27 with yield2 grows to yield3 after final-day watering without fertilizer and yield4 with fertilizer. An available final-day crop can still benefit before harvest. Ongoing crops' next overnight production comes after the recorded match, but this does not make all crops equivalent.

## Conservative candidate

`experiments/round8_terminal_inputs.py` appends a new audited layer to the frozen fullfusion candidate; SHA-256 `87d8c0c8d41e2061b7e4c7236e1de45fdaa1387384d5178003b1cb7d37b44890`.

The layer starts at step648, preserves both species for all remaining viable opportunities and pending retries, uses projected actual post-action seed stock, and adjusts the inherited carrot spare bookkeeping when clipping a purchase. Zero-quantity orders become empty lists in their original slots. The fertilizer guard abstains if any visible wheat/carrot still has an incremental fertilizer benefit, a reactive input worker is active, or same-turn fertilizer selling is present. Otherwise it conservatively reserves all remaining native pickup and sale requests before clipping any fertilizer buy. Cash funding is checked without assuming current sale proceeds.

Counters separately expose seed cuts, quoted fertilizer savings, change count, funding/value abstentions, productive seed shortages, productive fertilizer shortages and errors. These are observed shortage indicators, not a proof against all future configurations. Ten focused semantic checks cover fertilizer benefit, crop caps, pending retry reserve and unsupported configuration abstention; see `results/round8_terminal_inputs_semantics.json`.

## Eight-game result

The first four frozen development worlds, candidate seat0, were played against v7 and Master2965, in a single sequential process.

| Seed | Margin vs v7 | Margin vs Master2965 |
|---|---:|---:|
| 1118262502 | -291 | -85 |
| 457648937 | +1295 | +150 |
| 1921079672 | +312 | +146 |
| 733556107 | +3626 | +946 |

All eight games completed normally. Productive seed/fertilizer shortage indicators, stderr and exposed error counters were zero; maximum action time was 0.124 seconds on this host. However, the new layer clipped ZERO units and changed ZERO turns in every game. These wins come from its fullfusion base, not the new terminal guard. Each final-day fertilizer candidate was protected by a value/worker/trading guard.

Recommendation: do not promote this as an improvement. v7's existing E402 already covers the safe seed space encountered here, and the more aggressive public fertilizer knockout lacks a general guarantee. The artifacts are retained for audit and a possible later larger coverage check, but this subtask does not claim incremental gain.

## Files

- Source / separate suffix: `experiments/round8_terminal_inputs.py`, `round8_terminal_inputs_suffix.txt`.
- Attribution supplement: `experiments/round8_terminal_inputs_NOTICE.txt`; inherited full license: `submissions/release_v7/LICENSE.txt`.
- Build and manifest: `research/round8/build_terminal_inputs.py`, `terminal_inputs_manifest.json`.
- Screen and raw diagnostics: `research/round8/screen_terminal_inputs.py`, `results/round8_terminal_inputs_screen.json`.
- Semantic checks: `research/round8/check_terminal_inputs_semantics.py`.

No root main, upstream release, or parent league tool was changed. No online submission was made.
