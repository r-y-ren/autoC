# DESIGN — Kaggriculture agent via OpenAI-ES

Ground truth: `kaggle_environments==1.32.7`, env `kaggriculture`,
`kaggriculture.py` sha256 `bc8a548…` (see `vendor/engine.lock.json`).

## D1. Simulate every turn, not every day

GOAL.md leaves the simulator granularity open. Two options were considered:

- **Day-level analytic sim** (30 steps/episode). ~24x cheaper, but the intra-day
  executor outcome must be solved in closed form (routing, turn budgets, market
  lockstep). Every closed form is a fresh chance to diverge from the engine.
- **Turn-level sim** (720 steps/episode). Mirrors `interpreter()` statement for
  statement, so exactness is a transcription problem, not a modelling problem.

**Chosen: turn-level.** The cost argument for day-level does not hold. Per turn
the work is O(units) scatter plus a cheap market/town update; only end-of-day is
O(tiles). Under `vmap` over ~32k environments each of the 720 steps is a
well-fed kernel, so the rollout is launch-bound, not flop-bound, and lands near
the GOAL throughput budget anyway. Exactness is the scarce resource here, not
flops.

"Day-level policy" (GOAL.md) is unchanged and orthogonal: the **network** is
evaluated on hour 0 of each day (30x/episode) and its macro-action is held for
the following 24 turns. That is where the 24x saving actually mattered — on the
net, not the sim.

## D2. One implementation of the policy+executor, two array backends

The training sim is JAX; the submission is numpy. Writing the macro-policy and
the micro-executor twice would create a silent-divergence seam exactly where
GOAL.md's release gate points.

`kagg3/core/` holds pure functions parameterised by an array module `xp`:

    core.policy.macro_action(xp, theta, feats) -> macro
    core.exec.unit_ops(xp, state, macro, hour) -> per-unit op codes + targets

`xp = jnp` inside the vmapped sim, `xp = np` inside `main.py`. Branch-free by
construction (required for JAX; also what makes the numpy path microsecond-scale).
The release gate then only has to check float32 numerics, not two codebases.

## D3. RNG: host-supplied MT19937 word stream

End-of-day randomness is `random.Random((seed * 1_000_003) ^ day)`, consumed as:
weed rolls for player 0 (one `random()` per **empty unlocked tile**, row-major),
then player 1, then `rng.choice(sorted(SHOPS))` on shop-unlock days.

Verified against CPython: `random()` consumes two 32-bit words
(`a=w0>>5, b=w1>>6, (a*2^26+b)/2^53`); `choice` over 8 items consumes one word
per attempt (`w>>28`, reject `>= 8`). So the whole stream is recoverable as raw
words via `getrandbits(32)`.

Emulating MT19937 on-device would cost a 624-step sequential twist per
episode-day — worse than the turn loop it serves. Instead the **host** draws
`stream[episode, day, K]` uint32 once per generation (CRN shares seeds across the
whole population, so this is drawn once and broadcast, ~2 MB) and the device
consumes it with a pointer. Draw count per tile is data-dependent but resolvable
with a cumsum over empty tiles, which is exactly the row-major order the engine
uses.

Result: randomness is bit-exact, not merely distribution-matched.

## D4. Parallel-safe turn application

`interpreter()` applies unit actions sequentially, so two units touching one tile
in the same turn is order-dependent. The executor **assigns disjoint tiles per
turn by construction**, making a parallel scatter exact. Shed operations are
genuinely shared (capacity, availability); those are resolved with a cumsum over
units in fixed index order, which reproduces the sequential result exactly.

## D5. Labour is cheap — size the unit array for it

`HIRE` costs `fib(n)` = 1,1,2,3,5,8,13,21,... per day, reset daily. Eight hands
cost 54 coins for 184 extra unit-turns. A fully worked 100-tile farm needs
~250 unit-turns/day. So `MAX_HANDS = 16` (farmer + 16 = 17 units); the fib tail
(2,583/day for 16) is steep enough that the hire count is a real decision --
made, since PLANNER_V3_1 1.5, by an enumerated argmax over admitted task value
minus the bill rather than by a gene.

The engine caps nothing (`_do_hire` charges and appends until the money runs
out), but `_process_market` truncates each seat's order queue to
`maxMarketOrdersPerTurn` = 10 **per turn**, so a crew past ten needs a second
HIRE turn. `core/ops.py` spends turns 0 and 2 on HIRE, keeps turn 1 for the BUY
row (it has to resolve before any unit picks up its inputs) and moves SELL lot 1
to turn 3. A hand hired in turn t is appended during that turn's market phase,
after its unit actions, so it first acts in turn t+1 -- and because
`_spawn_hand` reads the occupancy of the four shed-access tiles, *every* unit
has to still be on its spawn tile when the turn-2 hires land. A day that uses
the second row therefore starts the whole crew at turn 3 and walks 21 turns a
unit instead of 22, which the enumeration charges to each candidate count.

The day also keeps a **cash reserve** back from its purchases: the fib bill of
tomorrow's crew at the count it just chose, one hand wider
(`plan.cash_reserve`). Labour costing 3% of gross is only cheap if the coins are
there in the morning; before the reserve the greedy spent the purse to zero and
seasons were measured ending with no hands at all for days at a time.

## Opponent pool

Self-play ladder (frozen theta checkpoints) plus the engine's built-in `starter`,
`pass`, and `random`. No third-party or hand-written strategy agents — GOAL.md's
non-goals rule out warm-starting from a planner, and nothing here needs one.

## Release gate (from GOAL.md)

1. JAX sim vs `kaggle_environments` — identical money trajectory, same seed.
2. numpy `main.py` forward pass vs JAX policy — identical argmax on held-out states.
3. `main.py` run inside `kaggle_environments` reproduces the sim's episode return.

---

## Validated findings (2026-08-21)

### The engine plays 719 turns, not 720

`interpreter()` marks agents DONE at `step >= episodeSteps - 2` = 718, and the
framework stops there. So the last processed turn is step 718: day 29 runs hours
0-22 only, hour 23 never happens, and the final end-of-day refresh never runs.
Only the *penultimate* refresh (after step 695) does.

This cannot change the reward -- money only moves on hours 0-2 (market and
hiring), and shed contents do not count toward the score -- but the simulator
reproduces the cut anyway so the whole trajectory is comparable, not just the
final number.

### A parallel scatter must exclude non-writers

`_apply_unit_action` runs sequentially, so the port needs the per-turn tile
writes to be conflict-free. Assigning each unit a disjoint block of the task
sweep is necessary but **not sufficient**: a unit merely standing on (or walking
across) another unit's tile still participates in a naive
`arr.at[tile].set(where(mask, new, old))`. With a duplicated index there is no
defined winner, so the passer-by can write back the stale value and silently
undo the active unit's write.

The fix is to steer non-writers to an out-of-range index and scatter with
`mode="drop"`, removing them from the operation entirely. This was found as a
one-coin divergence on day 5 that compounded to ~13% by day 29 -- exactly the
kind of silent drift GOAL.md's release gate exists to catch.

### RNG word stream: keep it unsigned

The MT19937 words must reach the device as `uint32`. Narrowing to signed `int32`
turns the `>> 5` / `>> 6` / `>> 28` extractions into *arithmetic* shifts for any
word with the top bit set, which flips roughly half of all weed rolls to true.

The weed comparison itself is exact integer arithmetic: `random() < chance` is
`A < chance * 2**53` for the integer A the two words encode, and that product is
exact in float64 because it is only an exponent shift. Rebuilding the double in
float32 on device would lose precision at exactly the comparison boundary.

### Weed tiles carry no plant fields

The engine replaces a dead plant with a bare `{"kind": "WEED"}`. The simulator
clears the plant metadata on every weed transition (daily refresh, decay tick,
and spawn) to keep state canonical. No rule reads those fields on a weed -- every
planner condition that touches `t_cons` / `t_fert` is gated on `KIND_PLANT` --
but leaving them stale makes every future diff noisier for no benefit.

### A lane vector may not be built out of per-lane chains (2026-08-26)

The mixed herd (`budget.N_LISTS` 8 -> 10) introduced three-lane animal vectors
-- what the BUY row's shed-room clamp grants per kind, what the standing
structures take, what gets built -- and each was assembled the obvious way: a
Python loop over the kinds carrying a running scalar, closed with `xp.stack`.
Three *different* expression chains stacked together lower to an XLA
`concatenate`, and when one lands inside a vectorised elementwise fusion the
sm_86 tile emitter rewrites it into an `scf.if` on the lane index whose
branches it then fails to widen:

```
error: loc("min.4155.1"): 'scf.if' op along control flow edge from Operation
scf.yield to parent: successor operand type #0 'tensor<1x1xi32>' should match
successor input type #0 'tensor<4x1xi32>'
```

jaxlib 0.10.2, RTX 3090, driver 580.126.20; there is no flag back to the older
emitter. It is a **codegen** failure, not a numerical one -- the same tree
compiles and passes every gate on CPU, and the GPU refuses the module outright
at `Trainer.__init__`'s archetype probe, which is the first thing a training
run does. The batch of 64 (8 rungs x 4 seeds x 2 seats) is what picks the
4-wide tile; a vmapped `build_day`, or `budget.grant` on its own, does not
reproduce it, because the bad fusion only forms inside the day scan.

`plan._share` is the rule that came out of it: a shared budget walked in list
order is `min(want[i], max(room - sum(want[:i]), 0))`, one expression for
every lane, with the prefix read out of a constant predecessor mask by
`plan._prefix`. It is the running-scalar walk exactly -- integer arithmetic,
non-negative wants -- so both backends stay bit-identical
(`tests/test_mixed_herd.py::test_share_is_the_unrolled_walk_lane_by_lane`).
`tests/test_gpu_tile_emitter.py` is the GPU-only gate and skips without a
device. The rule generalises: **do not build a short lane vector out of one
chain per lane** where the result feeds elementwise arithmetic.

### CARE banks a unit, and only a *fed* animal opens the gate (2026-08-26)

`_daily_refresh_animals` clears `fed_today`/`cared_today` every night and
increments `consecutive_unfed` on any animal that went unfed. The engine's CARE
op refuses an animal that is not `fed_today`, so **feeding is the permission
slip for caring**, and each accepted CARE adds one unit to
`pending_care_bonus`, which the next production fire cashes on top of the base
yield.

The consequence is a cadence, not a containment. A feed rule that fires only on
hunger inherits the engine's own `consecutive_unfed >= 2` escape clock and so
hands CARE the same one-day-in-two ceiling: a cow fed every second night cashes
a bank of 1 at its fire, where a daily cadence cashes 2 -- two units a fire
against three. Measured against kagg2 over 16 real-engine games, the
hunger-only rule ran 0.57 feeds and 0.49 cares per animal-day against kagg2's
0.97 / 0.96, and finished at milk 161 units against 276, wool 79 against 120.
`plan._derive` therefore prices *unlocking today's CARE* as a third reason to
feed (PLANNER_V3_1 §0.11, §1.4); the rule is an engine fact, the pricing is the
planner's.

### A flow rung is not the opponent it was cut from (2026-09-02)

`sim.market.apply_flow` replays a measured seat's whole market day at hour 0 and
pays it for the table's units outright. Both halves of that are wrong against
the engine that produced the tape, and the two errors sit on different rungs:

* **Unbacked sells.** `k` came straight from the table; only the shed *drain*
  was clamped by what the seat held, while the revenue and the market's
  inventory advance used the full `k`. The engine caps a SELL at `shed[item]`,
  so the tape's own farm limits it. On the four `103223493`-family rungs -- a
  clone footprint selling 305 strawberry / 264 milk / 135 wool behind a
  `wheat_clone` board whose shed never holds any of it -- the sim banked the
  tape seat 94.1k where the replayed opponent manages 79.9k: **+14.2k of coins
  the engine never lets it have.**
* **The tape always trading first.** `mask_flow_seat` blanks the seat's own
  market slots and the table lands before the turn scan, so no round of a flow
  episode is ever a coupled one: the tape gets the top of the book every day and
  our sells walk the tail. On `tape_103254816` that is worth ~9.5k a season of
  *our* coins.

Together the per-theta part of the error (sd 1,836) was larger than the whole
in-sim spread the rung ranks with (sd 1,222), and the rung's Spearman against
the real panel was +0.04. `--tape-flow-backed` clamps `k` to the shed before the
revenue and the advance; `--tape-flow-spread` divides the day's row over
`rollout.MARKET_TURNS` (`row // n`, remainder on the last), so the tape trades
at the hours we trade at. Both default **off** and are read at trace time, so an
unflagged run emits the program it always did --
`tests/test_tape_flow_fidelity.py` pins that against a verbatim copy of the
pre-switch arithmetic. Measurement and per-rung tables:
`scratchpad/tapegap/report.md`.

**`--tape-flow-backed` is measured and not usable as it stands (2026-09-02).**
The shed clamp is the engine's rule only if the seat's board grows what the
table sells, and a flow rung's board does not -- it is `TAPE_PLANNER`, a wheat
clone, whose shed never holds the strawberry / milk / wool / fertilizer the
tapes trade. On flow57's ladder over the same 18 thetas the clamp does not
shrink the opponent, it deletes it: the tape seat banks ~8k against the real
101.8k, our seat 166k against 103.5k, and the classic pool's rank correlation
with the real panel falls from +0.41 to +0.28. It also drops the flow rungs
under `AR.MIN_COINS` (`Trainer._liveness_floor`). The switch becomes meaningful
only once the flow seat is *credited* with the production its table implies --
the table describing what the seat grew as well as what it sold.
`scratchpad/tapefix/results.md` has the tables.

### Gate 1 status: PASSING

`tests/test_sim_equivalence.py` compares **every** state field (all nine tile
arrays for both players, shed, seeds, money, market inventory, quadrants, shop
count) at every day boundary. Exact match across the full season.

## Simulator scope

The market resolution models a SELL and a BUY_PRODUCT landing on the *same item
in the same slot* only under the assumption that the item is not at the $1 floor.
The planner emits an identical slot layout for both seats, so that pairing cannot
occur in self-play, and `market.assert_no_cross` makes the gap loud rather than
silent. Consequently the simulator's opponent pool is policy-driven agents only;
`starter` / `pass` / `random` are benchmarked in the real engine instead.

Two engine branches are absent from `sim/units.py` outright:

* **DROP** (`kaggriculture.py:342-356`) — `apply_units` has no branch. Safe
  unconditionally: `OP_DROP` exists only as an op code and a render label, and
  the planner never emits it, so the branch is unreachable by construction.
* **PLACE's shed-deposit fallthrough** (`:393-410`) — the sim implements only the
  animal-placement branch. Safe for two structural reasons, neither of them the
  obvious one. First, an inventory shortfall does *not* reach the fallthrough:
  the engine's `return` sits inside the tile-match branch, after `_inv_take`, so
  a PLACE onto a matching free structure with nothing to place is a no-op in both
  backends. Second, the planner also emits PLACE on tiles it is building this
  same day (`m_place = place_here | build_here`), which would be a live hazard if
  BUILD could fail — it cannot, since `BUILD_COOP` / `BUILD_PASTURE` cost nothing
  and test only `tile is None`, and `build_op` and `a_item` derive from the same
  `a_struct`, so the structure always matches the animal.

Note what the second argument turns on: the planner's guard is evaluated at day
start, the engine's hours later. They are different claims, and only the two
facts above close the gap. If it ever opened, the damage would be quiet — the
fallthrough fires only on the four shed-access tiles, and the engine would bank
the animal in the shed while the sim discarded it. No same-day reward difference,
just a shed drifting out of sync and compounding through every later sale.

`tests/test_planner_op_coverage.py` pins the op-set half of this: the planner may
not reference an op the simulator does not implement, and a newly added op code
must be explicitly classified rather than silently inheriting "implemented".

## Known levers not yet exposed to the policy

Recorded so they are deliberate omissions rather than oversights.

**Sell timing within the day.** The planner sells on hour 2, always. Two effects
pull in opposite directions, so the optimum is not obvious:

- *Earlier is better* against the opponent. When both seats sell the same item in
  the same slot the walk is coupled and the shared inventory moves two units per
  round, so each player's price falls twice as fast as it would selling alone.
  Selling before the opponent floods the market is strictly better.
- *Later is better* against the town. Shops tick every 4 turns and drain
  inventory, which lifts prices through the day.

Exposing a `sell_turn` head (restricted to a few fixed hours, e.g. {2, 8, 14, 20})
would let ES resolve that trade-off. The cost is that market resolution must then
run on 6 hours per day instead of 3. Restricting it to hours >= 2 also preserves
the property that a SELL and a BUY_PRODUCT can never share a slot, which the
simulator's market model relies on.

**Per-unit route start.** Every unit currently idles through the shared PICKUP
window (`ROUTE_BASE + P`), even units that pick nothing up, costing up to 3 of
each unit's ~21 working turns. Staggering the route start per unit would recover
roughly 5-10% of total labour, but the pickup count depends on the unit's task
block, which depends on its budget, which depends on the pickup count -- so it
needs a two-pass resolution, and a mismatch between the passes would leave an
animal unfed rather than merely wasting a turn.

**Shed overflow.** Harvest lands in unit inventories and is dropped to the shed
at end of day; anything past `shedCapacity` = 100 is discarded. The policy can
see `shed fill` and per-product shed levels and can throttle sales, so the
information needed to avoid this is present, but the penalty arrives a day late
and is hard to attribute. Deciding *which* product to dump to make room is a
strategy call, not actuator logic, so it is deliberately left to ES rather than
hard-coded into the executor.

## Measured throughput (1x RTX 3070, 2026-08-21)

| batch | compile | run   | episodes/s | turn-steps/s |
|-------|---------|-------|------------|--------------|
| 512   | 43.7 s  | 0.35s | 1,474      | 1.06 M       |
| 1024  | 40.7 s  | 0.38s | 2,696      | 1.94 M       |
| 2048  | 42.5 s  | 0.55s | 3,754      | 2.70 M       |

GOAL.md's ~1e7 steps/s target was for 2x RTX 3090. A 3070 is roughly a third of
a 3090, so 2.7 M on one card extrapolates above that estimate rather than below
it -- the risk flagged in GOAL.md ("if the Aug 25 benchmark lands nearer 1e6")
did not materialise.

**What actually mattered was XLA compile time, not flops.** Three changes, all
semantics-preserving, took a generation from minutes to about a second:

1. The ten market order slots became a `lax.scan` instead of a Python loop.
   Unrolling a large body ten times inside a 24-turn scan inside a 29-day scan
   made compilation the dominant cost.
2. `jnp.searchsorted` was replaced with `sum(a <= v)`. For sorted `a` that is the
   same answer, but `searchsorted` lowers to a scan or a sort, and every array
   involved here is at most 100 entries.
3. `argsort` on a 0/1 key was replaced with two cumulative sums and a scatter
   (`_stable_partition`), avoiding a 100-element sorting network.

Together these were a 5.3x throughput win at batch 2048, on top of the compile
saving. At POP 128 x 32 episodes that is ~1.1 s per generation, so 10,000
generations is roughly 3 hours on a single card.

## A note on marketParams domain randomisation

GOAL.md motivates the shared per-product encoder partly as the thing that makes
`marketParams` randomisation "actually bind" -- the encoder has to read `base`,
`T` and `above_target` off its inputs instead of memorising the default table.

Implemented (`spec.sample_market_params`, `--market-jitter`), but the stated
rationale deserves a caveat: **the competition runs the default market.** If the
test-time market never moves, then "memorising the default table" is not
overfitting, it is learning the environment. Randomisation cannot help there.

There is also a wrinkle GOAL.md does not address: `marketParams` is not in the
observation. An agent cannot read the true `base` / `T` at inference, so a policy
that conditions on them would be learning a capability it cannot use. The
implementation therefore perturbs only the *simulator's* market and leaves the
agent's static feature columns at the defaults -- a genuine regulariser that
penalises leaning on exact price levels rather than on the price and inventory
the market reports, and not a claim that the agent can see the perturbation.

The real generalisation risk in this setup is not the market table, it is
overfitting to the self-play opponent distribution, which randomisation does
nothing about. So the flag defaults to 0 and the two settings are compared
empirically on the default market rather than assumed.

## Multi-device sharding

GOAL.md requires the ES population to be sharded across both GPUs of the
training host. The rollout is already `jit(vmap(...))` over a batch axis, so the
population is placed with a `NamedSharding` over a one-axis mesh spanning every
visible device, and `tables` is replicated. XLA then partitions the batch with no
cross-device traffic inside an episode -- the only thing that crosses is the
per-rollout win score.

Training runs on a 2x RTX 3090 host reached over SSH; the workstation that
develops and validates the agent has a single RTX 3070, where the mesh is 1-wide
and the whole thing is a no-op, so the same code runs either way. The path is
also pinned on a two-device CPU mesh
(`XLA_FLAGS=--xla_force_host_platform_device_count=2`) by
`tests/test_shard_chunking.py`, which runs anywhere.

That test exists because the chunker is silent when it is wrong. `_fitness`
flattens `pop x episodes` into one batch, splits it into device-sized chunks and
pads the last one back up to a full chunk -- padding rather than leaving it
ragged, since a short trailing shape compiles a second program and an odd one
cannot be split evenly across the mesh at all. Get that bookkeeping wrong and
nothing crashes; candidates are simply scored against the wrong episodes, which
looks exactly like ES failing to learn. So the evaluator is stubbed with a
function of every batched input and checked against a numpy reference, including
chunk sizes that do not divide the batch.

Antithetic sampling maps onto the split as GOAL.md describes, but the chunking
here is by rollout index rather than by perturbation sign -- the fitness of a
candidate is an average over episodes and seats, so the two halves have to be
recombined on the host regardless, and slicing by rollout keeps every device
equally loaded even when the population is not a multiple of the device count.
