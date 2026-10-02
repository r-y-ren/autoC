# Post-lot seed hook: watered H30 engine evaluation

**Current verdict:** the corrected hook produced 44 injected crops across the
complete 60-game H30 evaluation. All 44 were watered, survived, reached yield
six, and were harvested. Its paired H30 margin change versus B was -257 coins
per board (SE 194, t=-1.32), so this family does not support promotion. H30B
has not been run.

`S/postlot/run_engine_pilot.py` is a fail-closed real-engine runner for the
default-off runtime hook being built in the isolated `S/postlot/tree`.

Reproduce the isolated source with `JAX_PLATFORMS=cpu .venv/bin/python
S/postlot/stage_tree.py`. Existing trees are checked, never overwritten. The
36 Python files currently match arms-next byte-for-byte; the stable aggregate
SHA-256 is `f352f55425464a4a0743f8d30fa09d907336dc32de62c6dece7ccc5862720256`.

## Frozen pilot

The pilot uses the first four H30 opponents, LIVE-C indices 42--45, with the
judge's exact shifted seed base `777001 + 1000003*42`, `--seed-per-opponent`,
one seed and both seats. Thus each mode produces eight games on identical
boards. It runs the unchanged `scripts/eval_vs_baselines.py`, B theta md5
`7fcf39485bae65ee84171957c5843814`, the standard HR switches, the pinned town
schedule, and one engine worker. CSVs, engine replays, and per-turn runtime
debug JSONL are retained under `S/postlot/pilot/`.

Preflight refuses unless `S/postlot/runtime_patch.py` exposes both the exact
`install(mode)` interface and `Runtime.last_postlot` debug record. It also
verifies the theta hash and exact four IDs. OFF calls `install(False)`; ON calls
`install(True)` before the source agent is loaded.

Run OFF identity first:

```bash
JAX_PLATFORMS=cpu timeout 1200 .venv/bin/python -u \
  S/postlot/run_engine_pilot.py off > S/postlot/pilot/off.log 2>&1
```

Only after OFF matches the corresponding B rows coin-for-coin and the runtime
owner clears ON:

```bash
JAX_PLATFORMS=cpu timeout 1200 .venv/bin/python -u \
  S/postlot/run_engine_pilot.py on > S/postlot/pilot/on.log 2>&1
```

Compare OFF and ON by exact `(seed, opponent, seat)` keys. This pilot is H30
only; report it as H30 and do not combine it with another family. The debug
JSONL retains `last_postlot` plus the emitted action on every turn so chosen
buys and new-plant completion can be audited against the engine replay.

## Current state

The runner compiles and both mode preflights pass. The OFF engine identity job
completed in 146 seconds with terminal exit code 0. Its eight rows match the
same `(seed, opponent, seat)` rows in `S/lossflip/sell5off_B_livech.csv`
coin-for-coin: `OFF IDENTITY PASS 8/8`. The CSV, eight engine replays, 5,752
per-turn debug records, and durable log are preserved under `S/postlot/pilot/`.

The runtime owner corrected the initial blockers and reported nine focused
tests passing, including engine movement law. Two early ON artifacts (`on` and
`on_smoke`) are invalid: every controlled seat entered `ERROR` at step 1. The
exact cause was in this pilot runner's trace expression, not hook delivery:
`dict.get` eagerly evaluated the fallback `day * 24 + hour` before those locals
were defined, raising `NameError` even when `step` existed. The earlier
worker-delivery hypothesis is retracted. Those artifacts remain preserved and
must never be read as performance.

The trace builder now computes day/hour first. Focused serialization tests pass
with both an explicit step (`99`) and no step (fallback `51`). The traced action
also catches `BaseException`, appends PID/day/hour/step plus a full traceback to
the tagged error log, flushes, and rethrows. Separately, an explicit
`_vendored_imports(True)` structural test confirms the corrected patch retains
`spec` and ops as module globals and render in the installed closure.

The fresh `on_smoke2` real-engine smoke (first H30 board, seat 0) completed with
exit code 0 in 29 seconds: 94,483 own coins, 2,890 moves, one hook firing, and
one requested crop verified as a real plant at its target in the replay.
`ON MECHANISM PASS fired=1 real_plants=1` establishes action validity and the
mechanism on this board.

After that gate passed, the authorized eight-game H30 run under tag `on_valid8`
completed with exit code 0 in 166 seconds. All eight games were action-valid.
The runtime fired six times and all six requested plants were confirmed in the
engine replays (`ON MECHANISM PASS fired=6 real_plants=6`): all bought/planted
MELON, four on day 6 at target `(9,0)` and two on day 4 at `(0,0)`.

This is one small H30 pilot family, not promotion evidence:

| family | games / boards | OFF win | ON win | delta margin | board t | flips W/L/= |
|---|---:|---:|---:|---:|---:|---:|
| H30 pilot | 8 / 4 | 50.0% | 50.0% | **+455** | +0.75 | 0/0/2 |

The margin change splits into +218 own coins and -237 opponent coins per game.
By board the deltas were +2,157, +351, -688, and 0. The mixed signs and four
boards are too small for a strategy conclusion. No other family was evaluated
or combined with this one. The valid tagged CSV, 5,752 debug rows, eight engine
replays, and log are preserved under `S/postlot/pilot/`.

## Coordinator review after the pilot

The original verifier merely searched later observations for a matching plant.
It has been replaced with exact purchase settlement, emitted-unit-action,
position, and empty-to-plant transition checks, plus complete replay/trace and
controlled-seat status checks. Root revalidated all six archived pilot events
with this stricter verifier; Sol's independent replay audit agrees. Future
events record the planned plant hour explicitly. Existing debug/replay/error
artifacts now prevent tag reuse even when the CSV is absent.

Review also found a negative seed-balance bug. The purchase guard now requires
the held seed count minus remaining base plants to equal exactly zero; one new
seed cannot fund both a base deficit and an incremental plant. The eight-game
results above precede that correction and are not a measurement of the final
guard. A fresh engine evaluation is required. Thirteen focused tests pass,
including the unchanged engine's actual unit/market functions, the negative
seed deficit, failed purchase rejection, and unrelated later plant rejection.

The geometry census used an intentionally restricted route graph; actual
engine movement allows crossing LOCKED cells and sharing unit coordinates.
The runtime follows that engine law while requiring an owned empty/weed target.
Planting alone does not demonstrate harvesting or profit; only paired final
engine outcomes can assess the intervention's value.

## Crop-survival failure and correction

Root and an independent Sol review followed each injected crop beyond its
successful placement. All six received no WATER, HARVEST, or DIG while alive:
seeds 1196709180 and 2097576449, both seats, became WEED at replay step 168
(day 7 hour 0); seed 2079139712, both seats, became WEED at step 120
(day 5 hour 0). The engine initializes `consecutive_unwatered=1`; planting-day
refresh increments it to two and kills an unwatered plant.

The correction reserves one additional idle turn and issues WATER immediately
after PLANT. The exact engine-function test now checks watering and next-day
survival. The runner requires every event's watering action and continued
PLANT/crop/planted_day identity at the next morning. Later daily replanning,
harvesting, and final economic value still require real-engine evidence.

The prematurely started full H30 tag `h30_final` was stopped with exit 130.
Its partial trace/replay are retained, with no completed CSV; it is excluded
from evaluation. Fresh post-correction tags must be used.

## Watered smoke and complete H30 result

The one-game `water_smoke` gate completed with exit code 0. Its injected MELON
at target `(9,0)`, planted on day 6, was watered, survived, reached yield six,
and was harvested by hand 1 on day 16. The runner's strict causal checks passed
with `fired=1 real_plants=1 watered_survived=1`.

The gated `h30_water` job then completed all 30 frozen H30 boards and both
seats: 60 CSV rows, 60 complete 720-step replays, and 43,140 action-trace rows.
Exact normalized `(seed, opponent tape, seat)` coverage matches all 60 B rows.
There were 44 hook firings and real injected plants. Replay lineage tracking by
`(target, crop, planted_day)` found 44 successful harvests at yield six, with
zero deaths, replacements, or unharvested injected crops.

The process itself exited 1 because the strict survival verifier asserted
`watered_today` immediately after four hour-23 WATER actions. At the day
boundary the engine had already reset `watered_today` to false. In all four
cases the same MELON lineage remained alive and `consecutive_unwatered` changed
from 1 to 0; each was later harvested at yield six. The affected games were
seed 1219841551, seats 0 and 1, target `(9,0)`, and seed 213120026, seats 0 and
1, target `(9,1)`. Thus this is a verifier boundary error, not an invalid action
or crop-survival failure. The archived data are complete; no rerun was made.

Paired H30 results, averaging the two seats within each frozen board, are:

| family | games / boards | B win | ON win | delta margin | SE | board t | flips W/L |
|---|---:|---:|---:|---:|---:|---:|---:|
| H30 | 60 / 30 | 63.3% | 60.0% | **-256.83** | 194.02 | -1.32 | 0/2 |

Own coins increased by 134.87 per game while opponent coins increased by
391.70, yielding the negative margin change. These are H30-only results; they
are not pooled with the earlier pilot or any other family. H30B remains unrun.

Root confirmed exact coverage after normalizing absolute versus relative
opponent paths, all 44 purchase/plant transitions, 40 ordinary watering checks,
and the four boundary cases above. Twenty game margins are exactly unchanged;
58 win/loss outcomes are unchanged. The verifier now handles hour-23 refresh
using next-day crop identity and `consecutive_unwatered=0`. Its six focused
evidence tests pass, including a regression for the daily flag reset. No engine
rerun is required to reinterpret the preserved results.
