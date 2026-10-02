# ENGOPENLOOP1 — ENGINE program open-loop feasibility gate (2026-09-22)

## Method

Selected 100 harvested ENGINE-vs-BAND episodes from leaderboard ranks 1–3, requiring the BAND
opponent's observed d2 plate to contain at least 10 melon. Seats are 50/50; source submissions are
34/36/30. Each raw episode supplied its own `info.seed` and town; `tape_opponent.py` replayed the
ENGINE seat byte-for-byte against reacting V56. The same first 30 boards are 15/15 seats and
10/10/10 submissions; packaged `submission_res940_cf` replaced the tape there.

## Results

| seat in ENGINE slot | W-L | win rate | mean purses (seat / V56) | mean margin |
|---|---:|---:|---:|---:|
| ENGINE open-loop, all 100 | 36-64 | 36.0% | 81,878 / 123,387 | -41,509 |
| ENGINE open-loop, same 30 | 11-19 | 36.7% | 83,116 / 122,319 | -39,202 |
| ours reacting, same 30 | 19-11 | 63.3% | 100,920 / 99,688 | +1,232 |

ENGINE's open-loop purse drift versus its recorded live purse is **-27,641/game** (live 109,519).
V56 is **+21,977/game** versus the recorded BAND purse (123,387 vs 101,410).

No whole turn was invalid. Every tape game had ignored/rejected work: 152,357 events total,
1,524/game (range 128–7,232). Totals are 99,906 ineffective unit actions, 24,934 refused market
orders, 23,848 non-PASS hand actions truncated after roster drift, 2,661 refused hires, 627
malformed market rows (25 games), 307 atomic plant vetoes and 74 refused land buys. Per-game counts
are in `S/engopenloop1/results.tsv`; `selection.tsv`, `summary.json`, `towns.json`, and `run.py`
make the cohort and gate reproducible. All town-prefix assertions passed.

## Verdict

**NOT open-loop robust (36% < 60%) → BC clone not viable by this feasibility gate.** The live
ENGINE advantage depends materially on reacting to state; cloning only the recorded program is unsafe.
