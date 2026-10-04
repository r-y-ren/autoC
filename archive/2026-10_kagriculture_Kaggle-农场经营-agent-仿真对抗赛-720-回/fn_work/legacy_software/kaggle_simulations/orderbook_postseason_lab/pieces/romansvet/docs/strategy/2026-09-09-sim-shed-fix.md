# Fixing the sim's shed stage: one unit-index walk — 2026-09-09

Applies the "Minimal fix (described, not applied)" of
`docs/strategy/2026-09-09-sim-tape-seat-bug.md`. Working files in `S/shedfix/`
(`tapecheck.py` = 44 pinned-town boards, `bench.py` = rollout speed,
`src_before/` = the pre-fix tree the before column was measured on).

## What changed

`src/kagg3/sim/units.py:apply_units` resolved the shed in two independent prefix
sums — every PICKUP against the hour-start shed, then every DROP / PLACE-to-shed
against the hour-start room. The engine walks `[farmer, *hands]` in list order
and mutates `private["shed"]` inside each unit's branch, so a lower-indexed
unit's DROP is visible to a higher-indexed unit's PICKUP in the same turn.

The two prefix sums are replaced by one `MAX_UNITS`-step walk over the unit
slots carrying the shed level. Each step:

    take   = min(pick_want[j], level)              # PICKUP, against the running level
    level -= take
    room   = max(SHED_CAPACITY - sum(level), 0)    # DROP / PLACE, against the running room
    dep    = prefix-clamped deposit of unit j's items in `inv_seq` order
    level += dep

A unit performs one op per turn, so PICKUP, DROP and PLACE-to-shed are disjoint
over units and a step never has to order two of them against each other. The
within-unit item order (the engine's dict insertion order, which decides who
survives an overflow) is unchanged: it is now `argsort(inv_seq * NI + item)`,
one total key, instead of a stable sort of the flat `(unit, item)` stream.

The walk is written out (17 unrolled steps) rather than run through
`core.loop.repeat`. Both were built and measured: they give **identical** money
on all 44 boards below, and eager cost is the same to within the load on the box
(10 `apply_units` calls: 20.7 s before the change, 22.5 s `lax.fori_loop`,
23.7 s unrolled). The unrolled form keeps `apply_units` free of the loop
dependency and leaves XLA free to fuse the stage.

## The four bad tapes, before and after

`S/shedfix/tapecheck.py`, the `S/simbug/sim_dump.py` board construction (theta
`flow166_g50`, `OPEN_PUMP_ON`, seed base 777001, FAM+L12 stacked, both seats);
the engine column is `S/lossflip/flow166_g50.csv`, which the before column
already reproduces to the coin on the clean control 107079367.

| tape | seat | engine ours/tape | before ours/tape | after ours/tape | tape err before | tape err after |
|---|---|---|---|---|---|---|
| 107072760 | 0 | 131,587 / 128,489 | 132,935 / 122,557 | 131,739 / 128,324 | **−5,932** | −165 |
| 107072760 | 1 | 131,587 / 128,489 | 132,935 / 122,557 | 131,958 / 128,321 | **−5,932** | −168 |
| 107089992 | 0 | 131,011 / 134,543 | 133,577 / 129,371 | 131,040 / 134,222 | **−5,172** | −321 |
| 107089992 | 1 | 131,011 / 134,543 | 133,507 / 129,758 | 131,068 / 133,861 | **−4,785** | −682 |
| 107090008 | 0,1 | 125,188 / 133,488 | 129,127 / 130,683 | 125,730 / 133,166 | **−2,805** | −322 |
| 107095149 | 0,1 | 98,778 / 122,088 | 104,668 / 121,423 | 98,812 / 121,778 | −665 | −310 |

The residual is now inside the shop-draw band the *clean* tapes already sit in
on the same run (107068399 −16, 107070717 +29, 107092814 −33, 107088554 −58,
107081922 ±480, 107056463 +704/−833, 107067869 ±1,217). Our own seat moved with
it: 107089992 seat 1 went from +2,496 over the engine to +57.

## Nothing else moved

44 boards, 34 byte-identical before → after. The 10 changed rows are the four
bad tapes (8 rows) **and 105400600**, a leg-family tape, which went from
137,881 / 115,531 to **137,844 / 115,667 = the engine exactly** (it was −136 out
before). So of the ten leg-family rows: nine unchanged, one corrected onto the
engine. `S/simbug/handoff.py`'s animal-only screen does not catch that one — the
fix also reorders DROP against PICKUP for *room*, which moves non-animal turns.

The clean control 107079367 stays at 101,977 / 117,214 = the engine, both seats.

## Tests

* `tests/test_shed_handoff.py` (new, 4 tests) — the day-7 hand-off (unit 5 DROP,
  unit 6 PICKUP an empty shed → unit 6 holds the cow), the mirror image (unit 6
  DROP, unit 5 PICKUP → the pickup finds nothing and the cow stays in the shed),
  and the two capacity orders (an earlier PICKUP makes room for a later DROP; a
  later PICKUP does **not** save an earlier DROP into a full shed). All four are
  played in `kaggle_environments` and in the simulator from one installed board
  and compared field by field.
* `tests/test_drop_op.py` — the existing engine-equivalence file for this code.
* `tests/test_drain_mix_gene.py` — the `PIN_SEEDS` and 200-state trajectory
  digests.

`pytest tests/test_drain_mix_gene.py tests/test_shed_handoff.py
tests/test_drop_op.py -k "not whole_season"` = **34 passed** (336 s).
`test_a_whole_season_with_drop_on_matches_the_engine` — the season-long
field-by-field equivalence run with `plan.DROP_ON` — was run separately and
passed.

## Speed

One 30-day game, `S/shedfix/bench.py --batch 1 --reps 7`, on a box at load ~29.

| tree | compile + first run | fastest of 7 | median of 7 |
|---|---|---|---|
| before | 400.1 s | 2.044 s | 2.210 s |
| after | 439.8 s | 1.791 s | 2.201 s |

Steady-state rollout is unchanged (median −0.4 %, fastest −12 %: the spread is
the box, not the change). Compile grew 10 %, the whole of it the 17 unrolled
steps. Both trees return the same self-play money `[46811, 9849]` — the fix is
a no-op for our own planner, which never hands an item between units.

## What is not verified

* Only the FAM + L12 tape set (22 tapes, both seats) was re-read; the 42
  held-out pinned tapes and the six drawn legs were not re-run.
* No ES leg was re-run, so the effect on training throughput at batch is
  inferred from the batch-1 compile/run numbers above, not measured.
