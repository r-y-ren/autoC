# First complete-season integration gate

The repair passes 40 focused cases, 32 existing scripted cases and exact raw
identity on all 688 conservatively disjoint vectors from the fixed trace.
Next, run one existing staged test unchanged:
`tests/test_sim_equivalence.py::test_sim_matches_engine_with_a_wide_crew[1164543749]`.
Both independent Sol reviewers agree this is a useful first integration smoke.

One CPU process, timeout1200 plus kill10, fresh `wide_season_20260912` files.
Preserve the frozen stage and source-bound runner; wrapper verifies the actual
imported reference engine against its lock before and after execution. The
isolated overlay is b5aeeb2ca2563f8af64c87ea0a811f852776c4153abd0d6b111419b7a99f1e07.
Archived planner switches, including seed-room ON, remain exactly as staged.
This test uses its fixed synthetic wide-crew theta, not submitted B.

Require exactly one collected case passing without skips, final source and
engine binding markers, unchanged helper/plan files, and normal process exit.
The existing node asserts that at least 12 hands are actually hired and compares
both seats' money, market stock, land/shop counts, shed/seeds and all tile/meta
fields at 29 end-of-day boundaries plus the final partial day. Any divergence,
timeout or refusal is preserved. No automatic retry or alternate seed follows.

Coverage gaps remain explicit: shop identities, unit positions and counts,
hires today, private inventories/insertion order, and final partial-day carried
state are omitted by this unchanged node. Its PASS alone is not full State or
action-tape fidelity. Next design is an enhanced full-state season/tape gate,
prefer the captured row58 input with its exact open-loop packaged opponent and
matching town injection; that needs a separate implementation and review.
The old trace alone lacks market action vectors for a fixed-action replay.

Only after correctness gates should separately bounded GPU loop/unroll compile,
warmed evaluator throughput, memory and population4096 feasibility be measured.
Training needs a corrected-source baseline and repeatability qualification;
the failed historical population reference stays invalid. No policy gain,
submission change or promotion follows from this integration smoke.
