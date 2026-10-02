# Conditional simulator repair readiness

Two independent read-only Sol reviews agree on the semantic boundary if actual
trajectory exposure is established: preserve full-vector real-unit masking and
atomic PLANT demand validation once, then apply each player's units in index
order against the current carried physical state. No repair is implemented or
authorized by this note; the actual row58 trace is still pending at17:40Z.

The archived `sim/units.py` computes shared shed operations at lines65–153 and
tile operations at155–279. A tile-only scatter correction leaves PLACE wrong:
an earlier DIG/BUILD/PLACE may change whether a later PLACE puts an animal on
the farm or falls through to a shed deposit. Duplicate FEED/CARE/COLLECT and
HARVEST-to-PLANT chains also depend on updated tile state. A deterministic
scatter winner alone does not implement sequential legality or inventories.

A replacement unit-index fold must preserve MOVE/PASS precedence, shared shed
DROP/PICKUP/PLACE ordering and overflow, per-unit inventory insertion order,
LOCKED behavior, and all tile operation branches. Plant over-demand is decided
from the original full action vector and seed inventory, not re-evaluated after
masking or earlier units. No HARVEST-only patch is proposed.

The reviewers differ on initial loop form: one favors the existing static
unroll pattern, the other a compact JAX loop followed by a measured comparison.
This is unresolved implementation/performance work, not semantic disagreement.
The larger stateful loop's compile time and throughput must be measured; old
shed-only timings cannot select it. A conditional fast path under vmap cannot
be presumed cheap because both branches may execute.

Before training, staged validation would need locked-engine differential cases
for both unit orders of duplicate/mixed tile ops; atomic PLANT over-demand;
HARVEST-to-PLANT and BUILD-to-PLACE; shared shed handoffs and PLACE fallthrough;
no-op/resource cases; and inventory order tested by subsequent constrained DROP.
Existing starting points include tests/test_drop_op.py, test_place_op.py,
test_unit_pickups.py, test_sim_equivalence.py, test_tape_flow_fidelity.py,
scripts/check_tape_actions.py, scripts/validate_trained.py and scripts/bench_sim.py.
Those tests must run against the actual isolated amended source, without
altering the locked reference engine or evaluation semantics. Current native
suite imports alone do not bind the archived training source.

If the trace succeeds, preserve its first supported exact event as a regression;
actual exposure is distinct from the constructed HARVEST counterexample and
from causality for the liveness mismatch. Full field/private-state and day-end
parity, unchanged-case outputs, compilation cost, warmed evaluator/generation
throughput and memory all require evidence before a new training plan.
The original failed population reference is not waived by a simulator repair.
