# Day-5 complete-plan labels: bounded timeout

The first bounded CPU execution of `S/planselect/day5_labels.py` ended at its
600-second process timeout with exit code 124. It emitted no stderr exception or
assertion and produced zero terminal labels. Therefore it supports no claim
about compactness, delayed crop value, or policy performance. The ignored
`S/planselect/day5_labels.json` preserves that failure record.

The frozen scope remains the first four distinct tapes in
`S/isearch/boards_dev.json`, both recorded seats per tape, and exactly two day-5
candidates: unchanged B and `compact + 1` clipped to `DIST_MAX`. No result was
available to influence those choices. The intended outputs keep current-state
features separate from tape/seed/RNG provenance and terminal own coins,
opponent coins, and margin. Per-tape means average its two seats; there is no
cross-family pooled statistic.

## Restart plumbing

The runner now writes flushed UTC stage messages to stderr and atomically saves
host-state checkpoints after the eight day-5 dawns and after the deduplicated
day-5 plan branches reach day 6. `--resume` accepts a checkpoint only when its
arms-next source-tree hash, runner script hash, frozen configuration hash, stage,
job layout, and state digest all match. Checkpoint file hashes are recorded in a
successful final artifact.

Days 6 through 28 now use one reusable jitted and vmapped one-day advance in a
host loop. Day 29 remains a separate exact terminal call with `TPD - 1` turns
and no end-of-day processing, matching the preserved H30 evaluator boundary.
This avoids compiling the whole remaining season as one scanned graph and lets
a later terminal-stage timeout restart from the day-6 branch checkpoint.

No simulation was rerun while making these changes. `py_compile` only confirms
that the Python syntax is valid; it does not validate JAX tracing, checkpoint
round trips, branch identity, terminal values, or agreement with the preserved
`S/isearch/lc.csv` base rows. The next bounded execution should run the unchanged
script once, retain its stderr progress log, then use `--resume` only if a later
stage times out. Exact base-row comparison remains required before interpreting
any labels.

Root review additionally bound the configuration to `branch_fixture.py`, made
dawn resume require the exact `dawn_day5` stage and eight-state count, and
refused accidental fresh overwrite of saved checkpoints. Six focused tests
pass: checkpoint round trip, source/script/config/stage drift refusal, and
state-tamper detection. These tests run no game and do not establish that the
revised simulation finishes or produces accurate labels.
