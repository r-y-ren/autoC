# Conditional GPU qualification for the unit-order repair

This is a prospective performance and repeatability protocol. It must not run
until the exact row58 tape-season gate and its independent evidence audit pass.
It does not authorize training, select a policy, or repair any production tree.

## Frozen subject and workload

Build two otherwise byte-identical private extractions of the reviewed archive
plus the reviewed `S/unitorder/units.py`. In one extraction bind
`apply_units = apply_units_loop`; in the other bind
`apply_units = apply_units_unrolled`. Refuse any other source difference. Pin the
archive, overlay, helper, driver, window manifest, all 120 tapes, B theta,
configuration and imported-module hashes before and after every process.

Use the actual Flow215 Trainer CLI initialization and intercept the same first
`_probe_archetypes` call as `S/seedrank/liveness_repro.py`. The fixed workload is
pop4096, 124 episodes (120 frozen w00 tapes plus four carried archetype
episodes), seed309, sigma0.01, mask1191/width6789, SGD, chunk8192 and the existing
Flow215 flags. The captured initialization call has 992 rows (`124 * 8`) and a
12-column `int32` result. Require exact input-tree hashes in every arm.

Make a synthetic repeated evaluator chunk using the explicit captured call
schema and frozen map `arange(8192) % 992`. Keep tables and their price array
[9,85001] shared; index candidate theta, opponent theta, words, seat,
start_nquad, start_money and tape_ctl together. Require flow=None, all seven
batched leaves to have992 source rows and8192 expanded rows, and exact
output8192 == output992[index]. Record the map and both input-tree hashes.
Pinned-once gives120 one-seat tape episodes plus4 carried episodes, so the
4096*124=507904-row generation divides into62 chunks without padding.
This measures the evaluator shape; it does not exercise real perturbed
population diversity, Trainer._play slicing/shard_batch/concatenation, ranking,
gradient or optimizer work. The62-call cost is an evaluator-only projection.

The benchmark remains on the frozen source setting
`SEED_ROOM_PURSE_ON=True`, solely because that is the source-bound captured
case. OFF is the intended fresh training and shipped evaluation contract.
Existing B dawn-plan and four-board OFF
matches do not establish universal ON/OFF fidelity, and this timing protocol
must not authorize ON-trained/OFF-judged training. Before training, record one
explicit intended training/judging switch contract and satisfy its separate
source-fidelity prerequisite. Run the selected implementation's final
confirmation arm under OFF. That establishes its OFF source binding and cost;
it does not establish relative OFF speed between both implementations.

## Exact program

Use one otherwise idle RTX 3090, JAX/JAXLIB 0.10.2, highest matmul precision,
x64 disabled, the frozen deterministic XLA flags and a fresh process per arm.
Require the selected physical UUID, no other compute process and at most 64 MiB
used before each arm. Disable persistent compilation caches. Sample process GPU
memory at 200 ms or faster and synchronize (`block_until_ready`) around every
timed evaluator call.
Capture cold992 timing inside the initialization wrapper around the original
_eval call, ending only after synchronization; record full CLI initialization
wall time separately. Synchronize both sides of the cold8192 call as well.
Materialize and synchronize every expanded device input before starting that
timer, then hash the ready arguments. Index/gather or transfer work must not
be charged to the evaluator-only cost.

Run four arms in the fixed order `loop-1, unrolled-1, unrolled-2, loop-2` so
each implementation appears once early and once late. Each arm performs:

1. Actual CLI initialization, including the first cold 992-row evaluation.
2. Two synchronized cached 992-row calls on the identical captured arguments.
3. One cold 8192-row call on the frozen expansion.
4. Five synchronized warm 8192-row calls, retaining every time without outlier
   deletion.
5. A no-update check over theta, optimizer state, keys, counters and checkpoint
   outputs, followed by all source/input post-hash checks.

The second fresh process for each implementation is the retrace/restart repeat;
do not add an in-process cache-clear run. Persist raw outputs, per-call wall
times, output/input digests, compiler/backend/device metadata, sampled peak
memory and a PASS/REFUSED receipt even on a late failure. The program performs
zero generations, gradients, optimizer updates, checkpoint writes or ranking.

## Qualification gates and budgets

Stop the whole protocol on a source/input/config mismatch, wrong backend or
device, OOM, non-finite result, shape/dtype mismatch, state mutation, missing
receipt, timeout, or any cached/restart output difference. Require:

- exact outputs within each input shape in an arm and across the two fresh
  processes for that implementation, plus the stated8192-to992 index mapping;
- exact loop-versus-unrolled outputs for both 992 and 8192 rows;
- peak process GPU memory no greater than 12,000 MiB in every arm;
- each arm at most900seconds with `timeout -k 10 900`; the four child budgets
  sum to3600seconds, with an outer3660second cap plus kill10 for wrapper and
  termination overhead. No automatic retry;
- for each implementation, both warm runs have five samples, and the two arm
  medians differ by at most 10%;
- for the eventual choice, using the maximum of all ten warm8192 samples,
  `cold_992_max + cold_8192_max + 10 * 62 * warm_max <= 9000 seconds`.

The last bound reserves at least1800seconds inside a proposed fresh
10-generation/10800second launch cap for host-side ranking, optimizer,
checkpoint and log work. This is a prospective budget, not a trainer config
field or a measured whole-generation cost. Bind the new timeout wrapper in the
future training plan; the old launch script itself contains no10800second cap.

All four arms must pass; do not select a surviving implementation after another
arm fails. Select unrolled only if its8192 warm median is lower in both
order-reversed pairs and `1 - gm(unrolled_medians)/gm(loop_medians) >= .05`,
where gm is the geometric mean of the two arm medians. Otherwise retain loop.
A timing tie cannot justify extra experiments. After selection and the
explicit switch/fidelity decision, allow
one final fresh-process confirmation arm for that exact intended mode, capped
at900seconds. Require its within-process repeats/index mapping, source binding,
memory and budget gates. This single OFF arm does not establish two-process
OFF repeatability or loop-versus-unrolled OFF parity/speed. Before a fresh
training process enters its first generation, its actual992-row initialization
must exactly reproduce the saved selected-OFF output and arguments, supplying
the second-process OFF check without another standalone benchmark arm.

Passing establishes that one reviewed repair is deterministic and fits the
bounded Flow215 evaluator workload on the target GPU. Fresh training still
requires a separately reviewed immutable source, exact actual zero-generation
Trainer initialization under the declared switch, a fresh run name/output and
the normal launch guards. No old failed population result becomes a baseline or
promotion result.
