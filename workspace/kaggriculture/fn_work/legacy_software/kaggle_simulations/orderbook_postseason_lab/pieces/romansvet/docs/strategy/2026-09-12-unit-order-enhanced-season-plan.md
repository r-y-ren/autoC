# Prospective enhanced hourly season parity gate

The staged wide-crew equivalence season at seed `1164543749` passed after the
isolated unit-order overlay. That existing gate compares many physical fields
only at day boundaries. It does not retain transient unit inventories,
inventory insertion order, positions, hand counts, individual shop identities,
or the final partial day's hourly states.

`S/unitorder/enhanced_season.py` is a prospective integration continuation for
the same fixed wide-crew theta and seed. It is not a B, tape, training, ranking,
or performance test. It must not run until its helper and staged identities are
independently reviewed.

The helper loads the immutable staged extraction. It first runs the staged
`run_day` directly. It then temporarily wraps four call sites: `apply_units`
and `compact_orders` expose the six already-built action arrays, while
`decay_plants` and `end_of_day` expose the real returned State. Every wrapper
calls its original callable and returns that result unchanged. The original
callables are restored in `finally`, and their restoration is a PASS condition.
All callbacks are ordered CPU callbacks. On full days, the pre-EOD state at
hour 23 is replaced in the aligned observation stream by the captured real
post-EOD State, which is the state the locked engine exposes. The direct and
instrumented boundary states must be exactly equal across all 27 fields.

The fixed run compares initial state plus all 719 exposed engine states. It
covers 29 complete days and the final 23-turn partial day. Both seats' complete
farm/private semantic projections are checked hourly: money, every tile field,
positions, hand count, hires, shed, seeds, and unit inventory values and order.
It also compares quadrant count, market inventory, shop identity counts and
shop total. Raw simulator `step` must equal the frame index. The sale-ledger
fields are instrumentation-only with `day_metrics=False` and must remain zero.

The engine has no acquisition timestamp corresponding to `inv_seq`. Exact
numeric equality is therefore not claimed. State validity requires empty items
to carry the sentinel, while canonical inventory order verifies that positive
items sort into the engine dictionary's insertion order; the already-passed
targeted acquisition-then-constrained-DROP test covers its physical effect.

The output is a fresh immutable directory with a receipt, lossless engine state
and action JSON, and a compressed NPZ. The NPZ contains all 27 State arrays for
720 aligned frames, 719 raw post-turn frames, 29 pre/post-EOD pairs, and 31
direct/instrumented boundaries, plus the captured `uop/ua/uq/mop/ma/mq` arrays.
Exact array schemas and dtype/shape/byte digests are recorded. The first parity
failure, path, index, and values are retained. Source, stage, helper, reference
engine, five enabled planner switches, runtime, and imported module identities
are recorded and rechecked. A future reviewed command should use the staged CPU
environment and `timeout -k 10 1200`; there is no automatic retry.

A PASS establishes hourly reference-engine parity for this one wide-crew
policy/seed integration path. It does not establish tape override fidelity,
submitted-B behavior, population ranking, or acceptable GPU compile/runtime.

## Combined launch and audit contract

The only authorized execution of this gate is the root launcher
`S/unitorder/launch_enhanced_season.py`, with a fixed1200second child cap and
kill10, fresh `S/unitorder/enhanced_season_20260912` outputs. A helper PASS alone
is insufficient. The launcher runs `validate_enhanced_evidence.py` on the saved
artifacts, requiring all168 raw arrays, exact schemas/digests, all31 direct and
instrumented boundaries, all719 raw turns and29 EOD substitutions, and all720
saved engine canonical states. It independently decodes all719 both-seat unit
and market actions and compares them with the engine's received actions.

Inventory timestamp invariants cover raw hour23 transitions before EOD, and
EOD must clear inventories, insertion timestamps, hands and daily hire counts.
Every finally loaded kagg3 module path and byte hash must map to the immutable
staged manifest. The four output files are receipt.json, hourly.npz,
engine_snapshots.json.gz and engine_actions.json.gz. The engine snapshots retain
all comparable canonical semantics; they are not full observation dumps.

Root's two pure regression checks cover nested/missing/length difference paths
and rejection of truncated or dtype-changed State comparisons. They passed in
session20254 before the first enhanced season launch. Static reviewer fixes and
these tests execute no game. Any runtime refusal or timeout preserves the
available raw evidence and closes this execution; no automatic rerun or seed
substitution follows. Helper18d6699f, validator6466a39f, launcher0ac805fd are the
final code identities presented for independent review before launch.
