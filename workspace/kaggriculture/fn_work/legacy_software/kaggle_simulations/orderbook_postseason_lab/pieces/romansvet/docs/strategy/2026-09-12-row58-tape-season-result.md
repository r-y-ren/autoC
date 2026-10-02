# Exact captured tape season passes engine parity

Root17719 completed exit0 on2026-09-12 at21:07:05.971758Z after389.291277seconds
of the1200second cap. Helper and independent saved-evidence validator both PASS.
A second Sol saved-only audit also PASS in4.7seconds, with no JAX, simulator or
engine imports and no file changes. The agreed one-case tape gate is complete.

The fixed input has tape episode108100156/table3 at physical0 and the exact-zero
policy at physical1, seed88567952. Candidate placement in the captured evaluator
is overridden by that tape. This is not candidate-action or submitted-B evidence.
The full120-table closure and all24 market hours were retained.

All720 aligned physical states,719 both-seat actions,29 pre/post-EOD pairs,
30 daily money rows, final money and day10 money match the locked engine.
All12 int32 evaluator outputs match between direct and instrumented calls.
The independent audit verifies118 raw arrays, all140 bound input files, stage
source identity,29 parent and18 engine-child imported modules, runtime,
zero-theta identity, package parsing with zero dropped rows, inventory insertion
order, raw replay projection and physical-seat label mapping.

Final physical money is[141865,59347]; day10 is[17396,2172]. These numbers are
fidelity evidence for tape-versus-zero, not a measured competitive improvement.
The old buggy evaluator target was not used as a correctness requirement.
No game was rerun. B/submitted theta MD5 remains7fcf39485bae65ee84171957c5843814.

Frozen implementation commit74e6146; live handoff commit15fab77.
[Prospective plan](2026-09-12-row58-tape-season-plan.md) and
[GPU qualification design](2026-09-12-unit-order-gpu-design.md).

Evidence under S/unitorder/row58_tape_season_20260912 and sibling sidecars:

| Artifact | SHA256 |
| --- | --- |
| execution.json (sibling) | 4570f980efc052038483aeefa01cc3c290982baf6b82efe44b416ee34126b827 |
| log (sibling) | 9c676691294fb4c8dd48a4aeeebceaaa0a3f4fd88018faf6941dc15394007a17 |
| receipt.json | a6ca86260e4f1c18d14154ba4e5b7f089d742e41c3ac660f1ca91aec1af806c7 |
| hourly.npz | e0e9e6b84d4478297205425b9cce7717aa585f099d35078ecc0109c8e4d412da |
| engine_replay.json.gz | 462bc1107e7eb3d11e8aeb7df688a17e0f93b751b542d5e533d0419d8335b1fe |
| engine_snapshots.json.gz | 917324fcabf4cf20f4f44ecb9812311201ab1c80a81e4755b5274f111d98dec0 |
| engine_actions.json.gz | 91eff676a6dcc5e8d1b5e3b462e085f56de5062903e909cda5db0b2026807952 |
| stage_manifest.json | 359512a2bd13c0dbf0e69a025c1c52dfd500c58b46a159169b41ebe6f2f38a31 |

Next is the bounded GPU compile, throughput, memory and repeatability protocol.
Its workload qualification is distinct from ranking and actual population
training. Fresh training and judged behavior must share the intended shipped
seed-room OFF contract. No GPU qualification helper has run, no new training
has started and no promotion/upload occurred. Topfive remains the goal.
