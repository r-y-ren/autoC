# Planner v2: keep the compiler, remove the structural losses

A redesign proposal derived from the blind deterministic review in
`docs/PLANNER.md`. Verdict on the current architecture first, then the
alternative in three tiers, ordered by (provable win) / (implementation risk).

## What stays — the architecture is right

The day-compiler is the correct backbone and is **kept**:

- One network eval per day, compiled into shape-static arrays: this is what
  makes ES training throughput and train/serve equivalence possible. A
  per-turn policy (24x evals, stateful within the day) was considered and
  rejected — it destroys throughput and multiplies the equivalence surface.
- Needs-derived provisioning with affordability clamps ("a macro can never
  schedule an op the farm cannot resource") is the right smoothing for ES.
- Integer-exact, tie-broken-everywhere determinism is non-negotiable.

The defects are not in the concept but in **fixed rules that leak coins
deterministically** — and ES cannot fix a rule it has no gene for. The
redesign principle: *every provably-losing behaviour becomes an exact
structural rule; every price-dependent judgement stays a gene.*

## Tier 1 — exact fixes, no new genes, each independently measurable

Each item is a pure ablation against the absolute eval (archetype ladder);
none changes theta layout, so existing checkpoints stay valid.

### 1.1 Sellability gate replaces `can_mature`
`brain.py:289` gates planting on *first* yield by day 28, but one-time crops
are only harvested at `max_yield_day` and must be **in the shed by end of
day 28** to be sold. Gate per class:

    one-time:  day + CROP_MAX_YIELD_DAY  <= 28
    ongoing:   day + CROP_FIRST_YIELD_DAY <= 28

Kills the dead zone (wheat d25–26, carrot d26, melon d17–18 are currently
planted, watered, and never monetized).

### 1.2 Two-tier task ordering (survival is not a preference)
`task_order` currently ranks all tasks by one learned score; when turns run
out, deadline harvests and survival waterings can be dropped, and a dropped
one-time harvest decays to nothing in ~half a day (`rollout.py:70`).
Add a tier bit above the score in the packed key:

    key = tier * TIER_BIG + score * 128 + (127 - idx)

Mandatory tier: harvest-at-deadline (one-time crop at `max_yield_day`,
or any harvest on day 28), survival water (`t_cons >= 1`), survival feed.
The learned score still orders everything *within* each tier, so the gene
keeps its expressiveness; it just can no longer starve an asset to fund
development.

### 1.3 Value-ranked rationing
`want_feed` / `want_fert` clamp by serpentine rank (`plan.py:346-354`): when
wheat is short, which animal escapes is a board coordinate. Rank shortfall
victims by replacement value (animal cost / crop expected revenue),
serpentine as tiebreak. Exact tables, no genes.

### 1.4 Reserve fertilizer from the sale
Mirror `wheat_reserved` (`plan.py:632`) for `n_fert_eff`. Today, when a feed
pickup exists, the fert pickup slides to turn 3 while the fert sell-lot fires
at turn 2 and strips the shed the plan counted on.

### 1.5 `animal_count = 0` must mean zero
`a_want = min(animal_count, n_free) + n_struct_free` (`plan.py:330`)
force-restocks every empty structure of the day's kind — the
buy→starve→escape→re-buy loop is structural. Change to

    a_want = min(animal_count, n_free + n_struct_free)

so exiting animals is a single reachable gene, and partial restock exists.
(Adjust the `n_build` / `place_here` clamp chain to stock frees first.)

### 1.6 Shed-overflow forced sale
End-of-day drop silently destroys everything above capacity 100
(`eod.py:192-194`); nothing checks room. At plan time project the eod shed
(hour-0 shed − sales + unconsumed buys + today's planned harvest inflow +
collected fert + unplaced animals — all computable, conservatively high) and
add `max(projected − 100, 0)` to the sell quantities, cheapest products
first. Destroying stock is never right; selling it at any price dominates.

### 1.7 Price the buy walk with the engine's own curve
The budget walk prices wheat/fert flat at the hour-0 quote (`plan.py:305`),
but the engine walks each unit up the price table *after* the turn-0 town
tick — the plan can be one unit optimistic, the last FEED no-ops, and a
300–500 coin animal escapes over a few coins of drift. The price table and
quote logic (`market.py::_quotes`) already exist: reuse them, including the
turn-0 town tick (deterministic from `shops`). Cross-seat same-turn coupling
remains the only residual, acknowledged, drift source.

## Tier 2 — semantic upgrades, same gene count

### 2.1 Fire-day-aligned cadence
Production fire days are exactly computable (`(day+1 − t_day − first) %
interval == 0`). Currently watering is survival-parity for ongoing crops, so
the fertilizer +2 (paid only when *watered on a fire day*, `eod.py:74-77`)
lands at best every other fire day; and the CARE bank is wiped on any unfed
fire day (`eod.py:112`), making CARE worthless on interval-1 animals unless
`feed_daily` happens to be on.

- extend `want_water` to fertilized fire days of ongoing crops;
- redefine `feed_daily=1` as *feed on fire days* (superset of survival);
- emit CARE only when the animal's next fire day will be a fed day
  (computable given the feed rule).

This decouples the CARE/feed gene trap and roughly doubles fertilizer
efficiency on ongoing crops, at the cost of extra wheat the walk already
prices.

### 2.2 Per-unit pickup scheduling
Pickup turns are global: if any tile needs feed, every unit loses the turn
(`plan.py:485`). `blk` is already per-unit — schedule each unit's own
pickups at `ROUTE_BASE + its own count` and start its route immediately
after. Recovers 1–2 turns for most units on most days (~5–10% labour).

### 2.3 Live re-gating of sell lots 2 and 3
The `sell_min` gate is checked once at hour 0 but lots execute at turns 10
and 18 into a market both seats have moved. Carry the gate into the emitted
market row and have the (shared, deterministic) executor zero a lot whose
turn-price is below the gate — same guard code in `sim/market.py`'s
sell-only path and in the submission renderer. This is the one place the
"arrays only" purity is worth relaxing: the guard is fixed actuator logic,
not policy.

## Tier 3 — the architectural upgrade: generate-and-test

The measured weakness of this project is that ES cannot resolve small
gradients. The current planner asks ES to *learn* numbers the simulator can
*compute*. The upgrade: the network proposes, an exact self-model disposes.

At plan time, build K candidate macros (vary the fragile scalar decisions:
budget `order`, `sell_lots`, gate levels, `fert_buy`, `feed_daily`) and score
each with a deterministic opponent-free day projection:

    projected coins = sell revenue along the own-impact price curve
                    − purchases (walked up the buy curve)
                    + Δassets at conservative valuation

Everything needed exists: the price tables, the town-consumption schedule,
and `build_day` itself. K × (build_day + arithmetic projection) is far
cheaper than the 24-turn day scan, so training throughput survives. The
learned parameters shrink to what the model genuinely cannot compute —
development mix, risk posture, opponent adaptation — which is exactly the
subspace where ES's 1-bit fitness signal is best spent.

Minimal viable version: keep one macro, but choose `order` by marginal
projected value per category, and choose `sell_lots` + per-product gates by
maximizing projected revenue over the three-lot own-impact curve. That
deletes ~15 of the hardest-to-train outputs and replaces them with argmax
over exact arithmetic.

## Explicitly rejected

- **Per-turn policy** — throughput and equivalence costs dwarf the gains.
- **Midday replan** — most of its value is captured far cheaper by 2.3.
- **Limit orders / richer market ops** — the kaggle engine doesn't support
  them; anything conditional must live in shared executor guards (2.3).

## Measurement plan

Tier 1 items land one at a time behind the existing gates: sim-equivalence
suite, then absolute eval vs the archetype ladder (fixed seeds, n >= 16
episodes), predicted sign stated before the run. None of them changes theta
layout, so every comparison is checkpoint-for-checkpoint.
