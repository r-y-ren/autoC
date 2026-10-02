# Planner v3 review

Reviewed 2026-08-24 against `PLANNER_V3.md`, the earlier planner review, the
current planner/simulator implementation, and the pinned Kaggriculture engine.

## Verdict

V3 is the strongest direction so far. Its central idea — learn uncertain
continuation values and compute engine mechanics exactly — is better than the
V1/V2 decision-head design. It should become the target architecture.

It is not ready to implement exactly as written. Several claims labeled
"exact," "provably no-worse," or "law" are actually approximate, and a few
rules would introduce deterministic regressions. V3 should first be revised
into a V3.1 specification that distinguishes:

- strict engine invariants;
- exact optimization under a stated value model;
- deterministic heuristics under learned projections;
- opponent-dependent estimates that must remain learned.

## What V3 improves

- Recasting outputs as value estimates gives ES a cleaner interface.
- Engine-curve purchase pricing, fertilizer reservation, terminal pruning, and
  lexicographic mandatory tiers are strong improvements.
- Separating laws from optimizers makes ablation and testing easier.
- Rejecting packed integer priority keys is correct.
- One daily network evaluation and static action arrays remain the right
  throughput/equivalence backbone.
- The phased migration plan is much safer than a monolithic rewrite.
- The document correctly notes that old checkpoints may load while no longer
  preserving their behavior.

## Blocking corrections

### 1. Remove the policy-improvement guarantee

The claim in `PLANNER_V3.md:35-39` is too strong. An exact transition model does
not provide an exact value function. V3 still uses:

- approximate learned continuation values;
- opponent-free price projections;
- decomposed greedy optimizers;
- incomplete multi-day valuation;
- approximate route and labour opportunity costs.

One-step policy improvement is guaranteed only when the continuation value being
optimized is the correct value of the reference policy and the relevant action
maximization is exact. Neither condition holds here.

Suggested wording:

> V3 is model-based policy improvement under an approximate learned continuation
> value. It should reduce avoidable mechanical errors, but improvement must be
> established empirically.

Use "provably no-worse" only for narrowly proven transformations.

### 2. Day-28 FERTILIZE pruning is wrong

V3 suppresses all day-28 fertilizer, but fertilizer can increase a same-day
one-time harvest:

```text
FERTILIZE -> WATER -> HARVEST
```

For a one-time crop in its bonus window, WATER immediately adds yield and
fertilizer changes the addition from +1 to +2. The correct horizon rule is:

- suppress fertilizer whose earliest marginal yield is after the last
  monetizable harvest;
- retain fertilizer that increases a same-day one-time harvest;
- compare the marginal yield with the fertilizer's purchase or sale opportunity
  cost.

### 3. One-time sellability gates are safe for V1 behavior, not globally optimal

Using `max_yield_day` fixes write-offs created by the current harvest-at-max rule.
Once V3 optimizes value, early harvesting must also be considered.

For example, wheat planted on day 25 can be harvested early on day 28 with
several units under normal watering, deposited at EOD 28, and sold on day 29. It
may be profitable despite not reaching `max_yield_day`.

Phase 0 may keep `max_yield_day <= 28` as a safe current-planner fix. The target
optimizer should evaluate early harvest value versus waiting, particularly near
the terminal horizon and under storage pressure.

### 4. The animal horizon gate is not an exact law

The rule in `PLANNER_V3.md:87-101` ignores fertilizer generated before the first
animal product. A late animal is probably unprofitable at normal prices, but the
claim is not generally guaranteed because fertilizer price is state-dependent.

Evaluate an upper bound:

```text
remaining product value
+ remaining fertilizer value
- animal cost
- feed cost
- labour opportunity cost
```

Reject only when that upper bound is non-positive. Recompute the horizon after
DROP is enabled, because EOD-28 production can then be harvested and sold on day
29.

### 5. The proposed land cutoff is incorrect

Newly purchased land cannot currently be developed on the purchase day: task
construction sees the quadrant as locked at hour 0. With harvest-at-max gates,
the last normal development day is around day 24, so the last useful land
purchase may be day 23 unless prospective post-purchase tasks are implemented.

Land valuation must account for:

- the current one-day unlock/development delay;
- whether same-day post-purchase development is supported;
- early harvesting;
- DROP-enabled terminal harvests.

Derive this from the generated schedule rather than using a shared day cutoff.

### 6. The sell optimizer omits the main timing uncertainty

The opponent-free water-fill proposal in `PLANNER_V3.md:263-293` does not solve
sell timing. In an opponent-free monotone market, selling later is generally no
worse because town consumption improves the market. The strategic reason to sell
early is the opponent flooding the product before the later lot.

A single reservation price answers "sell or hold," but not "sell at turn 2, 10,
or 18." Retain a learned per-product timing estimate, for example:

- expected opponent supply before each lot;
- an early-sale premium or timing-risk value;
- a per-lot opponent-impact adjustment.

The existing per-product gate head could be re-typed for this purpose instead of
made inert. Optimize adjusted marginal prices:

```text
projected own marginal price - learned opponent-impact adjustment
```

Monotone per-lot curves are also insufficient by themselves to prove naive
water-filling optimal: an early sale changes inventory and therefore the prices
of all later lots.

### 7. Turn-time sell guards should cap quantity, not cancel the whole lot

At turns 10/18 the executor observes the current market. It can walk the current
quote curve and calculate the maximum quantity whose marginal price clears the
planned floor. This is stronger than canceling an entire lot based only on its
first observed price.

The zero-quantity behavior requested for verification is already confirmed:

- the renderer emits a zero-quantity SELL;
- the engine parser treats non-positive quantity as inert;
- the queue position remains present, preserving cross-seat alignment.

Add a dedicated engine/simulator equivalence test before relying on it.

### 8. Category value-per-coin ordering is not an exact budget optimizer

Ranking five categories and granting each category's whole want remains
structurally suboptimal:

- feed value differs per animal;
- fertilizer value differs per plant;
- the first seed may be valuable while the tenth is not;
- product purchase cost changes per unit;
- land is indivisible;
- purchases compete for labour, tiles, cash, and shed capacity.

Construct individual marginal purchase candidates instead:

```text
feed animal i
fertilize plant j
buy seed/crop increment k
buy animal increment k
buy land
```

Give each a marginal net value and marginal cost, then use a bounded resource
allocator, a small enumeration around lumpy choices, or a documented greedy
approximation. Calling the category walk a computed heuristic is acceptable;
calling it exact is not.

### 9. Fertilizer and CARE semantics need correction

Fertilizer is active on `day`, `day+1`, and `day+2`: three days inclusive, not a
two-day window. Fertilizer valuation must include:

- ongoing crop watered fire days;
- one-time crop bonus-window watering;
- same-day FERTILIZE/WATER/HARVEST;
- the opportunity cost of selling collected fertilizer.

CARE requires feeding on the day CARE is performed, because the bank increments
only when both `cared_today` and `fed` are true. A correct CARE plan requires:

1. feed on the CARE day;
2. a sellable future production fire;
3. feed on the payout fire day;
4. enough held-yield capacity for the bonus;
5. marginal product value above wheat and labour cost.

### 10. Replace the fixed pickup passes with a direct block constraint

The pickup/block circularity can be solved directly. For each unit block and
candidate endpoint, compute:

```text
movement turns
+ operation turns
+ number of distinct pickup types required by the block
<= 22
```

Prefix counts for feed, fertilizer, and animal tasks make the distinct pickup
cost available for every candidate endpoint. Choose the largest endpoint that
satisfies the inequality. This avoids an arbitrary three-pass freeze that may
not produce a consistent assignment.

### 11. Hiring is enumeration under an approximate value model

Enumerating all 11 possible hire counts is promising, but

```text
sum(task values) - hire bill
```

does not by itself represent final value. The comparison must account for:

- purchase costs and unspent money;
- retained inventory and continuation value;
- exact route/spawn effects;
- per-unit pickups;
- storage and market interactions;
- tasks displaced by development.

Call it an "enumerated argmax under the planner's value model," not an exact
argmax. Benchmark it: eleven 100x100 pairwise rankings per in-game day across
every rollout may materially affect JAX compilation and throughput.

### 12. Labour selection and routing remain conflated

The proposed `value - lambda * walk_cost` score still does not solve route
locality:

- lambda needs units of coins per turn;
- route cost depends on the previously visited task;
- after value sorting, serpentine-adjacent distance is not actual route cost;
- a static per-tile score cannot capture route interactions;
- global value order can still jump repeatedly across the board.

Use two stages:

1. admit tasks by tier and marginal value;
2. spatially assign and route the admitted tasks.

A deterministic quadrant/stripe clustering or greedy-insertion route addresses
the locality problem more directly.

### 13. Genome counts and ES savings are overstated

The learned-output table in section 7 sums to 22, not approximately 13:

```text
9 + 9 + 1 + 1 + 1 + 1 = 22
```

Keeping 4,386 parameters while making many heads inert also does not eliminate
their ES cost. Isotropic perturbations still include inactive coordinates, and
finite-sample estimates inject noise into them.

Either:

- mask inactive parameter blocks out of perturbations and optimizer updates;
- compact the V3 network;
- reuse heads for useful estimates such as opponent timing pressure.

Define value output transforms explicitly:

- grow multiplier: positive bounded exponential or softplus;
- reservation price: non-negative, base-scaled softplus or bounded value;
- stable integer conversion and cross-backend quantization.

Raw linear outputs are not automatically calibrated coin values.

## Omissions remaining from the earlier review

V3 still does not fully address:

- spatial placement of animals and high-touch crops near the shed;
- developing newly purchased land on the same day;
- selling before buying when liquidity-constrained;
- handling multiple animal kinds in one day;
- explicit fertilizer-collection value;
- harvest batching near held-yield capacity;
- empty-structure conversion;
- cash reservation.

The demolition rejection in `PLANNER_V3.md:446` is factually wrong. There is no
dedicated DEMOLISH opcode, but DIG removes plants, weeds, and empty structures in
both the engine and simulator. It cannot remove a structure containing an animal.

## DROP is already verified

The pinned engine semantics have been checked:

- DROP requires a shed-access position;
- it moves unit inventory to the shed;
- shed capacity is enforced;
- inventory that does not fit is deleted;
- unit actions run before the same turn's market orders.

DROP should remain conditional on simulator implementation, equivalence tests,
route economics, and capacity safety — not on uncertainty about engine behavior.

A DROP/Sell plan must provide shed room before DROP executes, because DROP occurs
before the same-turn SELL. Once DROP is enabled, rederive all terminal laws:

- banked day-29 harvest can be harvested, dropped, and sold;
- EOD-28 production can become monetizable on day 29;
- crop and animal horizons change;
- "no day-29 unit operations" becomes false.

## Measurement plan changes

The phased approach is good, but `n >= 16` fixed seed pairs is too weak for
architectural decisions. Use:

- paired confidence intervals;
- separate discovery and held-out evaluation seeds;
- multiple training seeds;
- equal rollout and wall-clock budgets;
- current V2 champions, a broad frozen policy pool, archetypes, and real-engine
  baselines;
- operational metrics: walking turns, no-ops, overflow, unsold terminal
  inventory, purchase shortfall, and task value dropped;
- throughput and compile-time measurements for every optimizer.

Animal horizon pruning and unconditional day-28 fertilizer suppression must not
be classified as guaranteed non-negative Phase-0 changes.

## Recommended V3.1 architecture

Retain V3's core idea with these refinements:

1. Layer 0 contains only strictly proven engine invariants.
2. Layer 1 contains deterministic optimizers under learned projections.
3. Every optimizer is explicitly labeled exact or heuristic.
4. Network outputs estimate:
   - grow continuation multiplier;
   - reservation value;
   - expected opponent supply/timing pressure;
   - development and land continuation value.
5. Budgeting operates on marginal units rather than whole categories.
6. Labour selection and spatial routing are separate operations.
7. DROP is implemented before final terminal rules are frozen.
8. Inactive genome blocks are masked or removed.

## Bottom line

V3 is the right architectural direction and substantially better than V2, but
its correctness language outruns the actual mathematics. Correct the terminal
contradictions, opponent-sensitive sell timing, marginal budget allocation,
cadence rules, pickup block calculation, route locality, and inactive-parameter
handling before using it as the implementation specification.
