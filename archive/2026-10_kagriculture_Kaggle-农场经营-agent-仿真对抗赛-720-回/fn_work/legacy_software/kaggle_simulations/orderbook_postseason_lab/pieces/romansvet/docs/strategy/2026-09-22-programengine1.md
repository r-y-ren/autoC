# PROGRAM_ENGINE1 — KILL / OFF

Date: 2026-09-22. Frozen candidate: `PROGRAM_ENGINE_ON=True`. Shipped default:
`False`. Verdict: **KILL** at reacting-V56 dev100; held-out and tape gates were
not opened.

## Implementation and parity

One per-seat `ProgramEngineState` in `runtime.py` reconciles successful dawn
state, carries committed planting progress, records sales/milestones, and
resets on a new game. One intent owns the final post-residual/post-veto Macro
ask. The existing grant, land, hire, admission, route, and sale machinery
compiles it through one reserve. Opening pump ownership is suppressed ON;
OFF does not enter any new planner expression. The focused test proves complete
six-array byte identity to master on d0/d9/d15 plus ledger conservation,
deadlines, final ownership, and per-seat/per-game reset: **5/5 pass**.

## Executed smoke milestones (three boards)

Values are medians from retained full replays; Q is first dawn observed, so
Q2/Q3 were bought on d7/d11. ENGINE values are the ASTRA14/ENGVSBAND medians.

| milestone | ON | ENGINE | result |
|---|---:|---:|---|
| sheep after d0 | 3 | 3 | match |
| melon planted d0–2 | 11 | 11 | match |
| Q2 / Q3 first dawn | d8 / d12 | d7 / d10 | +1 / +2 days |
| hands peak d10 | 11 | 11.1 | match |
| cash d5 / d10 / d15 | 584 / 1,685 / 2,365 | 457 / 851 / 23,428 | late deficit |
| melon units sold d10–12 | 60 | 57.2 | match |

All three boards executed sheep=3, melon=11, hands=11 and melon sales=60;
all acquired Q3. Evidence: `S/programengine1/smoke_milestones.csv`.

## Gates

| gate | n | b/c/net | mean Δours | mean Δtheirs | verdict |
|---|---:|---:|---:|---:|---|
| OFF parity | 3 | — | 0 bytes | 0 bytes | pass |
| ON smoke | 3 | mechanics 3/3 | — | — | pass |
| reacting V56 dev | 100 | 0/57/−57 | −70,795.86 | +33,294.12 | **kill** |
| held-out start150 | — | — | — | — | sealed |
| tape dev50 | — | — | — | — | sealed |

Baseline dev was 57 wins, ours/theirs 100,843.11/99,268.74; candidate was
0 wins, 30,047.25/132,562.86. Both kill clauses failed.

## Where the coins went

The reconciler made the infeasible independent medians executable by reserving
the 19-cell Q1 opening for five wheat, eleven melon, and three sheep structures.
On d0 it paid 7 hire + 50 wheat seed + 480 melon seed + 1,500 sheep = 2,037,
leaving 963. The melon obligation worked and realised 60 d10–12 units, but Q2/Q3
arrived late, d15 cash was only 10% of ENGINE, and forced herd/crew/phase debt
displaced incumbent production. V56 captured the shared curves: our purse fell
70.8k while theirs rose 33.3k. This is stronger falsification than each killed
piece alone; the mechanisms compose mechanically, not economically.
