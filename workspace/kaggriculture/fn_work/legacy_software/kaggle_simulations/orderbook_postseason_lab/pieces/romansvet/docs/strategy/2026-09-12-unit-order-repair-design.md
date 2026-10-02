# Conditional complete unit-order correction: reconciled design

Two independent Sol reviews (postlot_mechanism and rotation_snapshot) agree on
this structure. Implementation remains conditional on the pending step707
complete unit-phase persistence result. The earlier isolated17-group result is
valid via the independent engine reconstruction, with its snapshot bug retained.

Keep the outer seat order. Compute real-unit masking and atomic per-crop PLANT
blocking exactly once from the original full masked action vector and initial
seed stock. Freeze that filtered vector. Replace both the shared shed walk and
parallel tile stage with one scalar unit transition carrying current state
through indices0..MAX_UNITS-1. Read current position/tile/inventory/shed/seeds;
apply movement and engine branch precedence; decide animal PLACE versus shed
fallback from the current tile; commit shed and tile changes immediately.
Update that unit's inv_seq from its own before/after inventory. Preserve DROP
whole-load destruction and insertion-order capacity allocation, PLACE selective
remainder, LOCKED shed access, no-op/resource cases and inactive-unit masking.
Do not retain a shed prepass or use deterministic scatter-winner selection.

Use one scalar transition for both measured candidates: a static Python unroll
and jax.lax.fori_loop. Neither loop form is presumed faster. Compile size/time,
warmed throughput and peak memory must be measured under the actual frozen GPU
runtime; old shed-only timings do not answer the larger carry question. A
collision-based conditional fast path is outside this first implementation,
because vmapped predicates can execute both branches.

Stage only in a hash-bound extraction with unchanged archived modules except
sim/units.py. Preserve the locked engine, production src, submission B and old
source/receipts. Correct the isolated module's now-disproved claim that all
planner-generated actions have disjoint tiles. The existing synthetic60-trial
collision test is not evidence of all real candidate trajectories.

Before any trainer/evaluator throughput run, require exact locked-engine
one-turn differential tests covering both orders of duplicate/mixed tile ops,
WATER/HARVEST, duplicateHARVEST/FEED/CARE/COLLECT, FERTILIZE/WATER,
HARVEST/PLANT, BUILD/PLACE and evolving animal PLACE/shedfallback. Atomic PLANT
cases include insufficient/exact seeds and occupied-tile requests that still
count toward demand. Include DROP/PICKUP both orders, capacity/destruction,
PLACE overflow remainder, LOCKED tile/shed behavior, boundary moves, no resources,
inactive units and insertion order verified by a later constrained DROP.
Use both seats and compare complete active physical/private state plus all
raw metadata invariants. Preserve constructed HARVEST and actual step707
regressions; verify static and loop variants give identical outputs. Add a
frozen bounded random valid-action/state differential set and unchanged
collision-free outputs; do not select only favorable examples after outcomes.

Existing drop/place/sim-equivalence tests hard-insert repository src, so copying
their files into the isolated checkout and asserting actual imported source
paths/hashes is required. PYTHONPATH alone is inadequate. Unit-pickup tests are
planner tests and cannot substitute for action-executor fidelity. The engine
semantic cases must also cover day-end effects and tape-action fidelity before
training. The precise bounded runner/suite recipe must be frozen before launch.

Only after correctness passes, freeze a performance protocol with cold compile,
interleaved synchronized warm measurements, representative batch sizes,
actual evaluator/scan throughput and memory. Report both loop candidates and
run-to-run noise. Do not choose from a single noisy timing or assume matching
microbench speed proves pop4096 feasibility. A new training decision requires
an explicit practical budget and a new source-aligned deterministic baseline;
it cannot waive or reuse the failed old population reference.
