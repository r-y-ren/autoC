# `test_no_tile_write_collisions`: stale gate, not a planner defect

**Status: re-confirmed independently, 2026-09-10.** The full autopsy is
[`2026-09-11-sim-tile-collision-gate.md`](2026-09-11-sim-tile-collision-gate.md)
(scripts `S/simgate/`); this file records a second, independent pass and the one
new measurement it adds. Do not re-open without new evidence.

## Verdict

**Stale gate. Real collisions, zero coins at stake.** The gate asserts a
disjointness the planner deliberately gave up in `45cb3b1` / `0c8bee8`
(`TAIL_CARE_ON`), and the test predates both — it ships from the initial commit
`35c4c1d` and has never been re-derived against the tail hop.

## What was reproduced

Same 7 hits on `45f8217`, byte-identical to the prior note's table (trials
12/23/46/51/52/56/57). Every hit is one **route block op** against one **tail
care hop**, on an **animal tile**, at turn >= 14. The op pairs are always
*distinct*: CARE against FEED, HARVEST or COLLECT_FERTILIZER. `TAIL_CARE_ON =
False` takes all 7 to zero.

The relaxation is documented in place (`plan.py:~7449`): *"`kneed_f` and
`kneed_c` already strike every tile the day's own route feeds or cares ... and
`care_free` keeps two tails off one tile. Order does not bind either: FEED and
CARE are day flags read once at eod."* That is exactly right, and it is why the
switch pays — `need_care = tc_uncared & ~tc_cared_by_day` is *built* to re-visit
the block's own fed-but-uncared animal.

## Why it is harmless (checked at source, both sides)

Engine (`kaggle_environments/envs/kaggriculture/kaggriculture.py`, pinned
1.32.7 per `vendor/engine.lock.json`): units resolve sequentially, farmer then
hands (`:935-939`), and each animal op writes one private flag and returns —
FEED `fed_today` (`:512`, checked *before* the wheat is taken), CARE
`cared_today` (`:529`), COLLECT_FERTILIZER `fertilizer_available` (`:520`),
animal HARVEST `yield_units`. eod reads `fed_today` and `cared_today` as day
flags (`:816-833`). No animal op reads another's field, so the four are
order-independent.

Sim (`sim/units.py:218-256`): the four write **disjoint arrays** — `t_water`,
`t_cared`, `t_favail`, `t_yield` — and `scat()` steers every non-writer to the
out-of-range index under `mode="drop"`, so no array ever sees a duplicated
index. `h_animal` is deliberately outside `reset_meta`. The dangerous case (a
`reset_meta` writer racing a tail CARE) is structurally unreachable: `reset_meta`
is PLANT/PLACE/BUILD/DIG/one-shot-HARVEST, each of which needs an empty or
plant tile, while the tail hop only ever targets `tc_animal` (an occupied
COOP/PASTURE).

## New evidence: the real-game rate

The gate's board (`_random_obs`) is a synthetic morning with 10-16 hands and
half the animals unfed. Instrumenting `P.build_day` inside real
`kaggle_environments` seasons with `flow172_g1000` (both seats, band2100p town):

| seed | 777001 | 777002 | 777003 | 777004 | 777005 |
|---|---|---|---|---|---|
| collisions / 60 planned days | 0 | 1 (d28) | 2 (d26) | 0 | 6 (d20, d25) |

9 over 300 planned days = **0.03 per planned day**, ~0.9 per seat-season, all
late-season (d20+) where tails are longest — an order of magnitude below the
synthetic gate's rate, and worth **0 coins** either way: both units' actions
succeed in the engine, nothing is refused and nothing is consumed twice.
(FERTILIZE is the engine's only lossy duplicate; the tail hop never emits it and
blocks stay disjoint.)

## Smallest fix

Fix the gate, not the planner. In `tests/test_gates.py:137-141`, key the
duplicate check on `(tile, op)` and exempt distinct animal ops:

```python
ANIMAL_OPS = {O.OP_FEED, O.OP_CARE, O.OP_COLLECT_FERT, O.OP_HARVEST}
keys = [(int(pos[u, h]), int(unit_op[u, h])) for u in acting]
assert len(keys) == len(set(keys))          # same op, same tile: still fails
per_tile = collections.Counter(int(pos[u, h]) for u in acting)
for u in acting:                             # a reset_meta writer sharing a
    if per_tile[int(pos[u, h])] > 1:         # tile: still fails
        assert int(unit_op[u, h]) in ANIMAL_OPS
```

That keeps every case the parallel scatter actually depends on and drops the one
the planner bought on purpose.
