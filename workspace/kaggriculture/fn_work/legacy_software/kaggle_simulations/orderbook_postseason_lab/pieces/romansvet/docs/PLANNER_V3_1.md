# Planner v3.1: value estimation + exact mechanics, corrected

Supersedes `PLANNER_V3.md`. This revision folds in every correction from
`PLANNER_V3_REVIEW.md` that survived independent blind verification
(2026-08-24: seven agents, each given neutral factual questions against the
pinned engine `kaggle_environments/envs/kaggriculture/kaggriculture.py` and
the sim transcription, with no knowledge of what either document claimed).
Twelve of the review's thirteen corrections were confirmed — several with
sharper mechanisms than stated — and one was refuted in its strong form.
Everything below cites what was verified, not what was assumed.
A second, fully independent re-verification (2026-08-24,
`PLANNER_V3_1_REVIEW.md`) confirmed the mechanisms — many to the digit —
and produced the errata now folded in below.

## Claim taxonomy

Every rule and optimizer in this document carries one of four labels. The
review's core process complaint — "correctness language outruns the
mathematics" — is fixed by never letting a claim exceed its label.

- **[LAW]** — strict engine invariant, provable from verified semantics,
  no value model involved. Dominates current behaviour unconditionally.
- **[EXACT-OPT]** — exact optimization *under a stated value model*; the
  argmax is exact, the values may not be.
- **[HEURISTIC]** — deterministic procedure under learned projections;
  labeled approximation, measured empirically.
- **[LEARNED]** — opponent-dependent or multi-day estimate that must remain
  a gene.

## The thesis, correctly stated

Unchanged in substance from V3, corrected in strength (review issue 1,
confirmed): every learned output is re-typed from *decision* to *value
estimate in coins*; decisions are made by deterministic arithmetic over
those values plus the engine's own tables.

> V3.1 is **model-based policy improvement under an approximate learned
> continuation value**. The transition model is exact; the continuation
> values, opponent-free price projections, and decomposed optimizers are
> not. It should eliminate avoidable mechanical losses; net improvement is
> established empirically, never assumed. "Provably no-worse" appears below
> only on narrowly proven [LAW] transformations.

What stays from V3 unchanged: one network eval per day compiled to
shape-static arrays executed verbatim by both backends; needs-derived
provisioning with affordability clamps; integer-exact pairwise/lexicographic
tie-breaking everywhere (packing the tier into the sort key remains
rejected — int32 overflow); network shape and theta layout preserved,
output *semantics* not.

---

## Layer 0 — laws and near-laws

### 0.1 Deadline-clamped one-time harvest **[LAW]** (replaces V3's tightened plant gate)

Verified (engine `:446-473`, sim `units.py:113`): HARVEST requires only
`age >= first_yield_day` and `yield > 0`; `max_yield_day` is never checked;
one-time crops are born with `yield_units = 1`; in-window waterings add
+1/+2 before the harvest in the same-day chain. Early harvest is fully
legal — the current planner just never emits it (`plan.py:280`).

The correct fix is therefore in the **harvest rule**, not the plant gate:

    harvest_age*(c, t_day) = clip(28 − t_day, CROP_FIRST_YIELD_DAY[c],
                                              CROP_SATURATE_AGE[c])
    harvest_one: age >= harvest_age*

- When `28 − t_day >= saturate_age` this is exactly current behaviour.
- When it is smaller, the crop is harvested early with whatever yield the
  in-window waterings built, instead of decaying unsold. Selling *k ≥ 1*
  units strictly dominates the current 0 — [LAW].
- The plant gate **stays** `day + CROP_FIRST_YIELD_DAY <= 28` (the current
  `brain.py:289` gate, now made *consistent* with the harvest rule rather
  than contradicted by it). Verified consequences: wheat d25 → 3 units on
  d28 (5 with fertilizer); **melon d17–18 → up to the full 6-unit cap**
  (five in-window waterings before the age-10/11 harvest) — V3's 0.1 would
  have banned two of the most profitable late plantings in the game.
- Whether a *marginal* late planting pays its seed cost is a valuation
  (projected clipped units × projected price ≥ seed cost) — [HEURISTIC],
  handled in §1.3. The valuation must charge the planting-day watering:
  the engine starts `consecutive_unwatered = 1`, so an unwatered planting
  weeds at its own eod — every late plant costs one mandatory watering
  beyond the in-window ones.
- Harvest-at-cap-saturation **landed 2026-08-26**, and it is the upper
  clamp above. `spec.CROP_SATURATE_AGE = min(max_yield_day, max(first_yield_day,
  window_start + max_yield − 2))` is the age at which daily in-window watering
  has already reached `CROP_MAX_YIELD`, because a one-time crop is born with
  one unit and each in-window watering adds one. Only melon differs from its
  max-yield day (10 vs 12); wheat, carrot and the two ongoing crops are
  unchanged, so nothing but the melon schedule moves.

  Melon is the whole reason it matters. It is the one product with **zero shop
  demand** — the town centre drains one unit a day and nothing else — so its
  curve (`250 − 0.01·(inv − I0)²`, floored at 1 by `inv = I0+158`) is drained
  once per season by whoever reaches it first and never refills. Measured over
  32 games on `obj2/best_abs.npy` (2026-08-26): kagg2 plants 12 melon on day 0,
  harvests them at age **10** and puts 60 units on a virgin curve on day 10 at
  **247 coins a unit**; we planted 5 on day 0, waited for age **12**, and first
  reached the market on day 13 at 197 and falling — 92.4 units for 9,988 coins
  (108/u) against their 119.8 for 20,741 (173/u). Both schedules harvested
  **6.00 units a tile**: the two days bought nothing but the loss of the race.

  The same-turn quoting rule is why only the *day* matters and the turn does
  not. `_process_market` quotes both seats against one pre-commit inventory per
  unit round and then commits in player order, so two seats selling in the same
  slot walk the curve in lockstep at identical prices — there is no first-mover
  edge inside a turn, and no seat order to win. A day is the whole granularity,
  and a harvest reaches the shed at its own eod, so harvest day + 1 is the
  earliest sale day.
- V3's tightened gate (`day + max_yield_day <= 28`) survives only as the
  Phase-0 fallback if the deadline-clamped harvest is deferred; the two
  must never ship separately in the wrong combination.

### 0.2 Animal acquisition: upper-bound value test **[EXACT-OPT]** (was a hard day gate)

Verified (review issue 4 confirmed; numbers re-verified 2026-08-24):
fertilizer has **zero town demand** and its tabulated price spans 1..3,100
(`100 + 0.2 × deficit`; the engine has no inventory floor, so the
span's tail below inventory 0 is a budget bound, not a clamp — driving
inventory to 0 alone costs ~11M coins — and the practically reachable
max is 2,100), so a late animal's fertilizer stream is
state-dependent. A d25 goose collects three sellable
fertilizers (d26–28; the d29 collection and the first egg fire at eod 28
never monetize), so break-even is ~100/unit — the **base price, zero
deficit** — or ~108 (a fertilizer deficit of ~40–45 net purchases)
counting the survival feed. A fixed day cutoff is even further from a
law than V3 assumed. The rule:

    reject acquisition of animal kind a on day d  iff
      UB = (product units sellable by d28, i.e. fires with d_fire+1 <= 28,
              valued at projected prices)
         + (fertilizer collections on days d+1 .. 28, valued at the
              CURRENT projected fertilizer price — optimistic)
         − animal cost − projected feed cost      <=  0

Reject only on a non-positive *optimistic* bound, so the rejection is safe
**under the opponent-free projection** — opponent (or later own)
fertilizer purchases can lift the price path above the bound, and
opponent wheat *sales* can cheapen the feed below its projection, so a
rejection can in principle forgo a marginal option; the failure direction
is benign, and the residual is the genes' to absorb, the same honesty rule
as §1.1. Acceptance goes through the normal §1.3 valuation. Labour
opportunity cost is deliberately left out of the bound (it would make
rejection unsafe).
The bound is re-derived under DROP behind `plan.HORIZON_DROP_ON` (§4, OFF):
eod-28 production becomes monetizable and every `d28` above reads `d29`, so
the worked example flips — a d25 goose collects **four** sellable fertilizers
and its first egg (eod-28 fire, harvested and DROPped on d29), 375 coins
against a 300-coin bird, and the rejection day moves to d26.

### 0.3 Land: no fixed cutoff; same-day development is real **[LAW + module]**

Verified (review issue 5 confirmed and sharpened): the engine unlocks the
quadrant **synchronously at the turn-1 market**, movement is never blocked
by LOCKED, and units act on turns 2–23 — so 22 same-day development turns
are legal. The quadrant identity (`LAND_ORDER[nquad−1]`) and purchase
success (affordability, already asserted by the walk) are both computable
at hour 0, so **prospective post-purchase tasks** are a deterministic,
open-loop module: when the walk grants land, task derivation adds the new
quadrant's 25 tiles as free slots. **Shipped 2026-08-25** (M1), at
`SELL_TURNS[0]` rather than turn 1 once M2 moved the order there, so a land
day's units idle until the quadrant unlocks -- charged as a floor under the
pickup turns, not on top of them.

Land *valuation* is no longer [LEARNED]. It is **[HEURISTIC] with a [LEARNED]
coin bias**: the quadrant is priced as the seed and animal candidates its 25
tiles admit, on the very arrays the greedy is about to use, against the purse
left after the hire bill, the cash reserve and the price
(`budget.marginal_gain`); the gene is a signed coin bias on that comparison,
zero at z = 0. The labelled approximation is named: the two-way compare of
§1.3 is grant against skip, and only the grant leg is computed -- the skip
leg's displacement term needs a second `budget.grant`, ~+18% episode
throughput, over the gate, and it is a multi-day question that §1.1 assigns to
the genes. The last useful purchase day falls out of the same arithmetic with
no constant anywhere: `new_plant_units` returns 0 for a crop that cannot
mature and `fires_between` empties for a late animal, so a late-season
quadrant prices at zero on its own.

### 0.4 Endgame rules, value-conditional **[LAW where marked]**

Verified: day 29 has no end-of-day (`episodeSteps 720`; step 718 is the
last *executed* step — 719 turns total), so
day-29 harvests never reach the shed; sells draw only on the hour-0 shed.

- **Day 29 [LAW]:** suppress every hire and BUY; liquidate the entire
  hour-0 shed across the three lots ignoring reservation values (terminal
  value of anything unsold is exactly zero); emit no unit ops.
  *Re-derived under DROP (§4): harvest→DROP→sell-at-18 becomes legal and
  this rule is parameterized, not hard-coded.*
  **Errata (Phase 0, 2026-08-24; superseded by Phase 2, Task 3):** Phase 0
  put the whole liquidation in the last lot alone (turn 18). Phase 2 runs the
  liquidation through §1.2's allocator instead, at `hold = sell.LIQUIDATE`:
  *whether* to sell is then unconditional (the LAW), and *where* is the
  allocator's own answer on the projected lot curves — the last lot on a town
  that drains the product between lots, the earliest lot when every lot quotes
  alike (no shops, or a product already at the $1 floor), a genuine split
  under timing pressure. The placement is **[HEURISTIC], opponent-free**, not
  [LAW]: an opponent dumping into the same turn is outside the projection, so
  a coupled measurement could still favour a different split.
  `core/sell.py::allocate` and `plan.py::_market` carry that label.
- **Day 28:** keep HARVEST (including 0.1 deadline harvests), COLLECT, and
  in-window WATER that raises a same-day harvest [LAW]. **FERTILIZE is
  value-conditional, not banned** (review issue 2 confirmed): the same-day
  FERTILIZE→WATER→HARVEST chain is reachable and pays +1 extra unit —
  and +1 is also the day-28 **cap** for every one-time crop: the engine
  allows one watering per day (`watered_today` guard), so the chain holds
  exactly one fertilized watering, and the whole-window clipped caps
  (+2 wheat, +1 carrot, 0 melon watered daily) are reachable only through
  a d29 watering + harvest that this section's own day-29 law rules out.
  Emit day-28 fertilizer only when the horizon-filtered gain (≤ +1 unit;
  0 without yield headroom) × projected price exceeds the fertilizer's
  opportunity cost [EXACT-OPT]; the whole-window caps return under DROP.
  No CARE (payout ≥ eod 29) [LAW]. No survival FEED/WATER, and the feed want leaves the budget (survival
  to day 29 is worthless) [LAW].
- **Generalized horizon predicate:** every op's payoff chain is tested
  against *the last monetizable event*, a parameter — never a day constant.
  It is `valuation.pay_day()`: "shed by eod 28" without `plan.HORIZON_DROP_ON`,
  "sold by day 29's lot 3" with it (§4).

### 0.5 Two-tier labour ordering, lexicographic **[LAW]** (unchanged from V3)

Pairwise compare `(tier, key)` in `task_order`; packing the tier into
the existing key is rejected. **Errata (Phase 2, 2026-08-24):** the ±1.15e9
bound quoted here was wrong. `task_order`'s key is `score * 128 + (127 - idx)`
with `|score| < 2^20` (§2's coin ceiling, `spec.COIN_CAP`), so it reaches
2^27 — a sixteenth of int32, and one tier bit would technically fit. The
conclusion is unchanged for reasons that are not about the bound: the
pairwise compare orders `(tier, key)` lexicographically for free, packing
would tie a LAW to whatever ceiling `tile_value` happens to clip at, and no
packing constant has to be revisited when a caller grows its tier range (the
route stage's own rank is a separate one, §1.6).
Mandatory tier: deadline harvests (0.1 clamp day, any day-28 harvest),
`must_water` survival waterings, survival feeds that pass §1.4's value
test (Phase-0 interim, until §1.4 ships: *all* survival feeds are
mandatory).

**Errata (2026-08-26, the one-crossing route).** The LAW is enforced at
**admission** and no longer in the route order. The route used to sweep
`tier * 2 + (tile_value > 0)` — four groups, concatenated — and a group of *m*
scattered tiles spans the whole board however small it is, so every populated
group cost the crew a further traversal: measured 1.32 inter-tile moves per
tile visited against a single sweep's 1.00, 48.6 % of the season's unit-turns
spent walking, and an admit estimate that no longer described the route it was
admitting for. Two groups now — priced-or-mandatory, then worthless — worth
+13,061 ± 7,932 coins against `starter` and +11,212 ± 9,228 against `kagg2`
over 16 paired games each.

What survives, and what the LAW now says exactly: a mandatory tile is admitted
ahead of every optional one (`order_v` still ranks by `tier` first), and
re-admission only ever drops from the *value* tail, so a mandatory tile is
never the tile cut. `_derive` floors `tile_value` at `tier` so that a survival
watering whose crop has no stream left cannot fall into the worthless group.
What the LAW no longer buys is a board crossing of its own: on a board whose
mandatory work sits at the far end of the sweep and whose budget runs out
first, that work is admitted and not walked, and it shows up in §7's
`value_dropped` — which fell 21,302 → 5,303 coins a season under this change,
because one crossing reaches 23 % more tiles.

### 0.6 Value-ranked rationing **[EXACT-OPT]** (unchanged; refs `plan.py:384-390`)

Shortfall victims ranked by replacement value (animal: remaining sellable
production capped at cost; crop: remaining projected revenue), serpentine
as final tiebreak.

### 0.7 Fertilizer reserved from the sale **[LAW]** (unchanged)

`n_fert_eff` deducted from sell availability, mirroring `wheat_reserved`.
Verified race: with a feed pickup the fert pickup slides to turn 3 while
sell lot 1 fires at turn 2.

### 0.8 `animal_want = 0` means zero **[LAW]**, with the compat caveat

`a_want` is per animal kind and clipped jointly (`plan._place_split`), stocking
frees first. **Shipped 2026-08-25**: `animal_count` became `animal_want[3]` when
the herd stopped being one kind a day; cow and sheep share the pastures, so the
three kinds are clipped in one pass in list order and never independently.
Changes a live gene's decode semantics: frozen checkpoints may regress
until retrained — predicted sign stated before the run, not discovered by
it. Composes with §1.4's feed-exit rule.

### 0.9 Shed-overflow forced sale: conservative-LOW, post-gate **[LAW]** (unchanged)

Project end-of-day shed counting only *certain* inflow; force-sell lowest
marginal value first; the forced quantity bypasses reservation values
(they gate exactly what accumulates). Forced sales draw only on the hour-0
shed — a day whose certain inflow alone exceeds 100 still overflows, and
the projector reports it so harvest batching can react.

**Errata (Phase 0, 2026-08-24) — morning buys are clipped to shed room
[LAW]:** the engine caps `BUY_PRODUCT` and `BUY_ANIMAL` at
`SHED_CAPACITY − sum(shed)`, measured at turn 1 before lot 1 fires
(`sim/market.py:176-210`), so a shed-bound purchase that would not fit is
simply never made — never bought and then destroyed. The budget walk must
therefore clamp its shed-bound buys against a **running room** exactly as it
clamps them against the running purse; seeds and land are exempt (neither
is a shed item). This section's sign-safety depends on it: uncapped, the
projection books morning inflow the engine never delivers and force-sells
against a deficit that does not exist. It also bounds §0.10's buy walk —
the walk prices at most that many units.

### 0.10 Engine-curve buy pricing **[LAW]** (unchanged, plus packaging)

Walk `tables.price` cumsums from the hour-0 inventory advanced by the
turn-0 town tick (both intervals divide 24 — verified). `DayView` grows
`mkt_inv` and `shops`; the table builder moves to shared JAX-free code.
Cross-seat same-turn coupling stays the acknowledged residual.

### 0.11 Cadence, corrected **[LAW mechanics, EXACT-OPT emission]**

Verified corrections (review issue 9 confirmed):

- Fertilizer is active **day, day+1, day+2 — three days inclusive**
  (`fertilized_until_day = max(old, day+2)`, read with `>= day`; a `max`,
  so re-fertilizing extends, never stacks — and the item is consumed
  before the `max`, so a re-fertilize that extends nothing still pays
  full price; the per-application valuation below prices this correctly
  by construction).
- CARE conditions, complete: the bank increments only when **cared AND fed
  on the same day** (the planner already enforces this — `want_care ⊆
  want_feed`, keep it); payout requires feeding on the fire day; the bank
  is wiped unconditionally on any fire day; a fire-day CARE banks toward
  the **next** fire; `max_held` clips oversized banks. Emit CARE only when
  all of: the payout fire day is ≤ the horizon, the feed rule guarantees
  that day is fed, yield headroom exists under `max_held`, and the marginal
  product unit clears wheat + labour cost. `feed_daily` and `care_on` genes
  deleted.
- **The feed rule has to make the cadence daily** (correction, gap review
  2026-08-26). `want_care ⊆ want_feed` is a containment, not a cadence: a
  feed rule that fires only on hunger inherits the engine's
  `consecutive_unfed >= 2` and hands CARE the same one-day-in-two ceiling,
  so a cow's every-second-night fire cashes a bank of 1 where a daily
  cadence cashes 2 — two units a fire against three. Measured against
  kagg2 over 16 real-engine games: 0.57 feeds and 0.49 cares per
  animal-day against its 0.97 / 0.96, milk 161 units against 276 and wool
  79 against 120. So *unlocking today's CARE is a third reason to feed*,
  priced at the product unit it banks and admitted like any other value:
  measured +5,278 ± 3,249 coins of margin a game (16 games, route1 theta),
  0.79 feeds and 0.70 cares per animal-day.
- Water ongoing crops on *fertilized* fire days (production fires
  regardless of watering; only the fertilized case pays), plus survival
  and one-time-bonus watering.
- **Value-ranked fertilizer targeting** (new — verification finding): the
  current `want_fert` ranks by tile index and will fertilize melons
  (marginal value 0 under daily watering) ahead of tomatoes (up to +3 per
  application via the eod path — one 3-day window covers at most 3 of the
  4 fires, so +4 needs a second application) — the mechanistic explanation
  for the recorded
  "raising the fertilize gene measured strictly worse". Rank fertilizer
  targets by exact clipped marginal value **per application**: ongoing
  crops' fire days inside the 3-day window that the watering rule will
  actually cover (each eod bonus requires watered-that-eod), one-time
  crops' clipped in-window gains, the same-day-harvest case from 0.4. Fertilize (and buy the shortfall)
  iff that value exceeds the fertilizer's sale/purchase opportunity price.
  Deletes `n_fertilize` and `fert_buy`.

### 0.12 Per-unit pickups: the direct block constraint **[LAW]** (replaces V3's multi-pass)

Verified (review issue 10 confirmed and strengthened): charging the pickup
turns *inside* the block cost dissolves the circular dependency V3
iterated around. With `D(s,e) = Σ_i [cpick[i,e] > cpick[i,s−1]]` (a
compare-and-reduce over the existing prefix arrays):

    L(e) = base_u + (cum[e] − cum[s]) + D(s, e)   — monotone in e
    endpoint: largest e with L(e) <= 22           — one _count_le pass

Budget is the fixed constant 22; the chosen block is self-consistent by
construction. Verified change set: move `prev` above the cut; add `D` to
the `_count_le` argument; include `D_at_s` in the one-tile feasibility
check; per-unit route budget `22 − p_u` in `working`; `pk_active = blk>0`
with a per-unit exclusive-prefix `pk_turn`. Three verified caveats:
pickups must stay before the unit's first movement turn (shed adjacency is
a silent-drop precondition); shed-contention tie-breaks shift from
unit-index to turn order when stock is short (totals stay covered by the
walk's clamps — only tie identity changes, determinism preserved); a
boundary splitting one pickup type across two units makes both pay a turn.

---

## Layer 1 — the optimizers

### 1.1 The price projector **[LAW facts, HEURISTIC use]**

Verified facts it stands on: price is monotone non-increasing in inventory
for **all 9 products over the entire table** (0 violations in 85,001
entries/row; plateaus and the $1 floor make it non-strict); town
consumption strictly raises prices (shops every 4 steps, center once a
day, fertilizer excluded from both); sales at the $1 floor pay the seller
but do **not** add to supply; buys always drain supply. Own-impact revenue
and cost for any planned quantity at any turn are exact table arithmetic.
Opponent impact is absent by construction — it is the genes' job.

### 1.2 The sell side: reservation value + learned timing **[HEURISTIC]** (corrected)

Verified (review issue 6 confirmed, quantified): opponent-free, selling
later within the day is uniformly weakly better — all-at-18 > split >
all-at-2 on every town-consumed product (e.g. 20 wool: 4,735 vs 4,313 —
magnitudes from a maximal 8-yarn-store town; a default 1-store town gives
4,160 vs 3,940, and the weak ordering holds at every consumption level,
collapsing to equality at zero shops because the center tick fires before
lot 1), exactly indifferent for fertilizer — so V3's opponent-free water-fill
degenerates to "dump everything in lot 3" and answers *whether* to sell,
never *when*. The design:

- **Reservation value** `hold[p]` [LEARNED, 9]: the value of keeping one
  unit until tomorrow (re-typed encoder sell score).
- **Opponent timing pressure** `press[p]` [LEARNED, 9]: expected
  opponent-impact on this product's later lots — the per-product gate head
  is **re-typed for this instead of going inert** (review's suggestion,
  adopted). Allocation optimizes *adjusted* marginal prices:
  `projected own marginal − press[p] × (lots remaining before the lot)`.
- Allocator: marginal-price greedy over the three adjusted lot curves,
  lot-2/3 inventories advanced by town ticks and own earlier lots; ties to
  the earlier lot, then lower product. Labeled [HEURISTIC]: monotone
  per-lot curves do not by themselves prove greedy optimal once early
  sales shift later curves; a bounded exhaustive split check per product is
  the verification-mode fallback.
- Constraints folded in: wheat/fert reservations (0.7), forced overflow
  floor (0.9), day-29 liquidation (0.4).
- One niche channel, noted honestly: dumping *to the $1 floor* early keeps
  supply lower for tomorrow (floor sales don't add inventory) — real but
  dominated in every measured case; the allocator may ignore it.
- Cash sequencing fact (corrected from one agent's stale-comment slip, per
  the code): the whole BUY row executes at turn 1, before every sell turn,
  so **no same-day sale can fund any purchase** under the current
  schedule. Lot proceeds carry to tomorrow. See module M2 for the legal
  resequencing option.

Deletes `sell_qty[9] + sell_min[9] + sell_lots` as decisions (19 outputs);
adds no new heads — both value vectors reuse existing ones.

### 1.3 The buy side: marginal units, not categories **[HEURISTIC]** (corrected)

Verified (review issue 8 confirmed): whole-category grants are structurally
suboptimal — feed value differs per animal, the tenth seed is worth less
than the first, land is indivisible. V3.1 budgets over **marginal purchase
candidates**:

    feed animal i          value: remaining production (0.6's table)
    fertilize plant j      value: 0.11's clipped marginal table
    seed increment (c, k)  value: projected clipped units × projected price
                                  × grow multiplier [LEARNED], declining in k
    animal increment       value: §0.2's stream valuation × grow multiplier
    land                   value: land logit [LEARNED], gated by 0.3

granted greedily by marginal value per coin down the purse, engine-curve
priced (0.10), lumpy land handled by a two-way comparison (grant vs skip)
at its position. Explicitly labeled a **documented greedy approximation**
— not exact: purchases still compete for labour, tiles, and shed room
outside the model. The category walk survives only as the Phase-A
fallback. Deletes `order[5]`.

### 1.4 Feeding as a value decision **[EXACT-OPT]**

Feed a hungry animal iff remaining conservatively-projected sellable
production (capped at replacement cost) exceeds the feed's engine-curve
wheat price. Remaining production **includes any pending care bank**
cashable at a monetizable fire — payout requires fed-on-fire-day and the
bank is wiped unconditionally at every fire, so a feed test that ignores
it can silently destroy a bonus 0.11 paid labour to build. An animal that fails the test is not fed and — with 0.8 —
not replaced: the exact exit rule that finally prices the
buy→starve→re-buy loop. Survival feeds that pass join 0.5's mandatory
tier.

Three things a feed can buy, then: survival, a standing bank at tonight's
fire, and **today's CARE** (0.11). The third is the whole value of a feed
on a quiet day and is priced at one product unit at the care's payout
fire — booked once, by handing it to the CARE op for the labour admission
while the FEED keeps it for the wheat purchase test. `ub_feeds` in 0.2
follows the same cadence — one wheat a day, not one every two — but the
matching *units* side deliberately does not: pricing the acquisition
bound at `min(max_held, 1 + interval)` units a fire measured −5,946 ±
2,664 coins a game, because the bound also sizes `v_place` and the k-th
animal's candidate value and a herd priced three units a fire is bought
faster than the day's turns and wheat can service it.

### 1.5 Hiring: enumerated argmax under the planner's value model **[EXACT-OPT, benchmark-gated]**

(Review issue 11 confirmed on labeling.) For each h ∈ 0..10, run the cheap
prefix (budget, tasks, `task_order`, cumulative block values); pick the h
maximizing in-model day value minus the fib hire bill; route once with the
winner. The label is exact-argmax-under-the-model, **not** exact: spawn
effects, per-unit pickups, and purchase interactions sit outside the
projection. Gate: measured JAX compile time and throughput before
adoption — the codebase already documents compile-cost sensitivity inside
the day scan. Deletes `n_hire`.

### 1.6 Labour: admit, then route **[HEURISTIC]** (corrected)

(Review issue 12 partially confirmed — `_routes` does charge the true
Manhattan move between consecutively-ordered tasks; the cost is *paid*,
never *minimized*, so a global value sort can thrash the board.) Two
stages:

1. **Admit** tasks by tier (0.5) and marginal value against the turn
   budget — value in coins from §§1.2–1.4, development from the grow
   multipliers.
2. **Route** the admitted set spatially: deterministic serpentine-stripe
   clustering of admitted tiles into per-unit blocks, greedy
   nearest-insertion within a block, serpentine index as every tiebreak.
   Shape-static, integer, no TSP.

Deletes `prio[9]`. The admit stage's value threshold is computed (marginal
admitted value at the boundary), not learned.

**Errata (2026-08-26).** Three corrections, all measured on the real engine
over 32 games:

* The route rank is `(tile_value > 0)` — **two** groups, one crossing of the
  worked span. See §0.5's errata for where the mandatory tier went.
* `EST_MOVES` 2 → **1**. One serpentine crossing costs 1.00 inter-tile moves
  per visit (measured 0.97); the conservative 2 was silently standing in for
  the crossings the four-group route paid.
* `EST_LEAD` = **5**, new. Every unit walks out of the shed-access block every
  morning — the engine clears `farm["hands"]` at every end of day — and that
  walk is 5.09 turns per active unit-day, a quarter of the season's whole turn
  budget, which the admit model did not charge at all. It subtracts from each
  unit's budget, so it can only ever under-admit.

  Both halves of that correction are one model and neither is safe alone:
  `EST_MOVES = 1` by itself measured −21,499 ± 10,810 coins against `starter`,
  the lead charge by itself −17,224 ± 8,946, and together +11,854 ± 11,233.

Two genes ride on the same stage and decode to a no-op at zero theta, so no
incumbent checkpoint's plan moves: `compact` (`_rank_near`) orders the day's
free slots by distance from the shed-access block rather than by sweep
position, and `dev_weight` scales `v_plant`/`v_place` — the value, never the
tier. Promoting development into the mandatory tier instead measured
−23,312 ± 9,198 coins.

---

## 2. The genome, corrected accounting

Verified baseline (review issue 13's count confirmed, and V3's own count
was also wrong): `brain.decide` consumes **52** scalar outputs today
(sell 9, gate 9, grow 8 of 9, prio 9, order 5, head[0:8] 8, lots 1,
aux 3), and 6 more are computed dead: the **five** head outputs
`head[13:18]` plus grow-of-fertilizer.

| Learned output | Scalars | Label | Transform (exact — review requirement adopted) |
|---|---|---|---|
| grow value multiplier | 8 | [LEARNED] | `min(softplus(z)/softplus(0), 4)` — 1 at z = 0; the fertilizer slot stays dead (no §1.3 candidate consumes it, and the shared encoder has no per-product column to mask) |
| reservation value | 9 | [LEARNED] | `0.8 × base_p × softplus(z)/softplus(0)` — 0.8·base at z = 0, so the initial policy *sells* (that day-1 projected marginals actually clear 0.8·base is asserted at init — see Phase 2) |
| opponent timing pressure | 9 | [LEARNED] | `base_p × relu(tanh(z))` — 0 at z = 0 = ignore timing |
| `dev_frac` + free-tile aux | 2 | [LEARNED] | sigmoid, as today |
| `animal_share` | 1 | [LEARNED] | sigmoid, as today |
| land coin bias + afford aux | 2 | [LEARNED] | `land_price × tanh(z)` — **0 at z = 0**, so the planner buys land iff its own valuation says land pays (§1.3); saturated it is one quadrant price either way, so the gene can neither force a worthless quadrant nor refuse an arbitrarily valuable one. Quantized as a 256-step *fraction* before it is scaled to coins: float32 agreement is relative, and flooring a product near 4,000 put numpy and XLA on different integers |
| plant-mix sharpness | 1 | [LEARNED] | as today |
| animal-mix sharpness | 1 | [LEARNED] | `head[2]`, reactivated 2026-08-25 — dead since 0.11 priced fertilizer, and it now sharpens the three-way herd split |

**33 decoded outputs, down from 52** (the same counting convention on
both sides: aux slots counted as scalars). Deleted as decisions (20):
`order` 5, `prio` 9, `n_hire`, `n_fertilize`, `fert_buy`, `feed_daily`,
`care_on`, `sell_lots`; `sell_qty`/`sell_min` (18) are folded into the
two re-typed 9-vectors, not deleted. 52 − 20 = 32, and the animal-mix
sharpness `head[2]` came back with the mixed herd — 33 — which is also why it
left §2's masking list. Every transform passes through `_qfloor`/`QUANT_EPS`
quantization where it becomes an integer — raw linear outputs are never
treated as calibrated coins.

**Inert parameters** (review issue 13, strong form refuted; hygiene
adopted): verified from the update rule — elementwise Adam, decoupled
per-coordinate decay, no clipping, no norm coupling — dead-parameter
perturbations change no candidate's fitness and cannot alter live
coordinates' updates. They do random-walk at ~0.23·lr on noise, bounded by
decay. Therefore: **mask the parameter columns feeding deleted outputs out
of perturbation and update** — `g3/gb3` (prio, 297 params), `g4/gb4`
(`sell_lots`, 33), the `g5` column for `fert_buy` (33), and the `g2`
columns for `head[0]`, `head[2:5]`, `head[8:13]` plus the already-dead
`head[13:18]` block (that block alone is 165: `g2[:,13:18]` 160 +
`gb2[13:18]` 5) — as cheap hygiene protecting future reactivation —
claimed as hygiene, not as an ES speedup.

**The plant mix's market-saturation gate** (`g7`/`gb7`, 33 params, 4,584 ->
4,617; added 2026-08-26). `can_mature` already asks whether a seed reaches the
shed before the deadline; `absorb` asks the other half — whether there is
anyone left to sell it to. It reads `residual_drain`'s `share` column (the
fraction of the town's *whole remaining* appetite for a product that the supply
already on both boards has not claimed) and drops a crop from the mix when that
column sits at its clip floor, i.e. when every further unit is oversupply by
construction.

Melon is the case it exists for. Its season drain is the 30 town-centre ticks
and its `above` curve is `sq` at 3.6x, so 158 units past `I0` take the quote to
the $1 floor — and the two seats between them commit 213. kagg2 harvests first
and books 120 units at 0.77x base; kagg3 arrived on day 13 and booked 96 at
0.32x, ~37 of them at or under 16 coins. The loss is committed at *planting*
time, because `valuation.py` prices a tile's whole future output at today's
hour-0 quote (271 for melon on day 10, against a realized 84). The threshold is
the clip floor and not zero: over a season melon's `share` is pinned at
`-DRAIN_CLIP` from day 1 while wheat, carrot, tomato, strawberry and egg sit
between -0.2 and +1.2 and cross zero freely, so a `share > 0` gate is a knife
edge on the five crops that are fine and measured -5,250 coins a game in lost
planting.

Unlike every other appended block this one's zero decode is **not** a no-op:
`tanh(0) == 0` leaves the gate at the clip-floor test, which is the shipped
default. Older checkpoints still unpack byte for byte (`policy.unpack` and
`train._fit_layout` zero-extend), but they decode a different plant mix on the
days their market is already oversupplied — deliberately. ES walks the bias
anywhere in `(-2*DRAIN_CLIP, 0]`. Crops only: the herd's three products are
drained markets where the same test is slack until day 21.

Checkpoint semantics do not survive the re-typing: v3.1 is a fresh
lineage (optionally warm-starting the encoder trunk), compared
lineage-vs-lineage, never checkpoint-for-checkpoint.

---

## 3. Executor exceptions, verified

**Turn-time lot guard — walk-and-cap, not cancel** (review issue 7
confirmed, adopted): at turns 10/18 the executor observes the live market;
it walks the current quote curve and caps the lot at the largest quantity
whose marginal price clears the lot's planned adjusted floor — strictly
stronger than zeroing on the first quote. The zero-quantity mechanism is
now **verified on both sides**: the engine parses `SELL … 0` as an inert
no-op that keeps its list index (pairing is purely positional), and the
sim's compaction + resolution agree exactly — *provided the zeroed lot is
emitted as a kept `SELL item 0` placeholder with `op = MO_SELL`*. Today an
empty lot is encoded `MO_NONE` and the renderer drops it (`render.py:35`),
compacting the list — exactly the alignment-shifting case the mechanism
exists to avoid. Note also that the executor is fully open-loop today
(`runtime.py` builds the plan at hour 0 and replays it; at turns 10/18 it
reads nothing from the observation but the hand count). The observation
carries live prices every turn, so the wiring is cheap — but the guard is
the one place v3.1 grows the executor beyond verbatim replay.
Preconditions downgraded from engine archaeology to engineering: the
renderer placeholder, a dedicated engine/sim equivalence test for capped
and zeroed lots, plus the sim-side guard in the sell-only path.
One verified footnote: an inert order still counts against the 10-order
turn cap.

## 4. DROP: verified, promoted to an implementation module

**Status 2026-08-30 — the simulator half shipped, the planner half is behind
`plan.DROP_ON` (OFF), measured positive.**

- `sim/units.py` implements DROP with the engine's exact discard semantics.
  `tests/test_drop_op.py` installs one board in both backends and steps them on
  a hand-written script, comparing shed, per-unit inventories, money, positions,
  tile yields and market inventory after every turn: the same-turn
  harvest/drop/sell chain, a DROP away from the shed, five overflow cuts at
  different points of the walk, and a drop-then-refill that would fail on a
  stale `inv_seq`. `tests/test_planner_op_coverage.py` no longer excludes it.
- The **day-29 chain** is behind `plan.DROP_ON`. It repeals only the third of
  the three things `terminal` does -- "no unit acts". The crew comes back
  through the *unchanged* hire enumeration, the day's turn budget ends one turn
  after `SELL_TURNS[-1]` (`plan.drop_turns`), `_routes` appends the exact
  return leg and cuts each block on `L(e) + home(e) + 1`, `_worth_a_turn` drops
  the tasks that day prices at zero, and sell lot 3 alone offers what the route
  banks. Measured 96 seeds x 2 seats against kagg2, paired: **win 79.2% against
  78.1, paired margin diff +461, sd 581, t = +11.0**, 171 games up / 17 down,
  discordance 2:0. OFF is byte-identical to the champion.
- **Mid-day drops on days < 29 — measured and rejected (`plan.MIDDAY_DROP_ON`,
  OFF).** The motivating hypothesis, that a hired hand's load is lost at
  nightfall, is **false**: `_end_of_day` runs `_drop_inventories_to_shed` for
  every seat before it clears `farm["hands"]`, so every unit's inventory is
  banked into the shed for free, wherever the unit stands. What the dump does
  destroy is the part over `shedCapacity`. Instrumented in the real engine
  (champion theta vs kagg2, 48 games, seed base 20260828): **73,109 items
  carried into an end-of-day, 473 destroyed** across 29 of 48 games, peak load
  132 against the 100 cap, upper bound 675 coins a game — and **315 of the 473
  (67%) on day 28** alone, where the deadline harvest empties the board.
  Extending the day-29 chain to `LAST_SHED_DAY` therefore looks right and is
  not: 96 seeds x 2 seats paired, **−1,157 coins, sd 1,423, t = −11.3**, 175
  games of 192 worse, win 75.5% against 79.2%. Day 29 spends the return leg for
  free because turns past `SELL_TURNS[-1]` are worthless there; day 28's are
  worth a great deal, since what a unit harvests in turns 19-23 is banked by
  that very end-of-day and sold on day 29 anyway. A crew-wide return leg costs
  about ten of a unit's twenty-two turns to save at most 675 coins. The lever
  that would have to move first is `_routes` giving a unit a **second block
  after its DROP**, not a wider `drop_day`.
- **The horizon re-derivation landed 2026-08-30 behind `plan.HORIZON_DROP_ON`
  (OFF, measured positive on two seed bases).** `valuation.pay_day()` is the
  one place the last *payable* day is spelled -- `O.LAST_SHED_DAY` stays the
  last *end-of-day* -- and every bound that meant the former moves by one:
  `cash_reserve` (day 29 hires, so day 28 must carry its bill), `survival_pays`
  (day-28 waterings and feeds buy a day-29 harvest), the 0.1 deadline clamp
  `harvest_age` and `brain.n_free_slots` with it, `can_mature` /
  `remaining_plant_units` (wheat and carrot plantable on day 27, tomato on 21,
  strawberry and melon on 19), the 0.2 animal bound `ub_units` / `ub_fert`
  (0.2's own d25 goose now pays: the d29 fertilizer and the eod-28 egg both
  monetize, 375 against a 300-coin bird), `animal_value`, `_pipeline_units`,
  `care_ok` / `bank_val`, `fert_marginal_value` and `crop_remaining_value`.
  Land needs no constant: 0.3's quadrant price is `marginal_gain` over
  `new_plant_units` and `ub_coins`, so its last useful day slides on its own.
  Three things deliberately do **not** move: `ub_feeds` (a count of feeds, and
  the old horizon over-charged it by one -- the new one makes it exact),
  `terminal` (that is `N_DAYS - 1`, the day that buys nothing and liquidates,
  not a monetization horizon) and the mandatory tier's `day >= LAST_SHED_DAY`
  (a labour floor; raising it would only demote day-28 harvests into the one
  day whose crew is turn-capped). `brain.residual_drain`'s `grow_days` also
  stays: it is a network feature normalisation read from day 0, and moving it
  is a retraining question. Measured paired on (seed, seat), both arms with
  `DROP_ON`: **+2,860 coins, t = +5.19, win 88.0% against 79.2%** (seed base
  20260828) and **+1,960, t = +8.79, win 91.1% against 84.9%** (held-out base
  20260830). The paired sd is 3,089-7,633 rather than DROP's 581 because
  `ub_fert` and `_pipeline_units` count one fertilizer per remaining day and
  that count moves on every day of a season with animals -- the switch reprices
  the animal candidates from day 0, so the whole season's variance rides along.
- **The shed-overflow guard landed 2026-08-30 behind `plan.SHED_OVERFLOW_ON`
  (OFF, not yet measured in the real engine).** The 675 coins a game the night
  destroys are not all reachable, but one slice of them is a bookkeeping gap
  rather than a labour problem, and it needs no return leg. §0.9's forced sale
  may draw only on `avail`, the hour-0 shed **net of the day's reservations**,
  and those reservations are sized on the day's *queued* demand: one wheat per
  `want_feed` tile, every application `n_fert_eff` says the shed can supply.
  The route then picks up only what the blocks it actually reached consume
  (`blk`) -- which is exactly what `proj_eod` charges as `picks_out`. So stock
  reserved for a task the day never walks to is counted as staying in the shed
  by the projection and hidden from the sale by the reservation at the same
  time: nothing consumes it, nothing may sell it, and end-of-day destroys it to
  make room for the harvest. The guard is one block after the DROP module's
  mid-day shed: it offers `shed - picked up - sold` per product -- precisely
  what nothing today consumes -- to a continuation of 0.9's own nine-round
  greedy, cheapest projected marginal first, and only as far as the deficit
  0.9 could not cover, placed in bulk in the lot 0.9 chose. What the route
  *does* reach keeps its reservation, so no feed and no application is ever
  sold out from under a task the day performs. **The law is sell, never drop:**
  DROP discards the part of a load that does not fit exactly as `_end_of_day`
  does (`sim/units.py` `d_take`, `sim/eod.py` `take`), so explicitly dropping
  the surplus banks the same coins as letting the night take it and costs the
  walk home on top -- the only lever that turns a surplus unit into coins is a
  lot, and a lot draws on the shed. Whatever the sale still cannot reach is
  left where it was and reported by §7's `overflow_destroyed`, which is what
  harvest batching (§5) would have to read. Note the cap this whole section
  turns on is a **total** over the shed's twelve slots and not a per-item one
  (`_drop_inventories_to_shed(private, shedCapacity)` against `sum(shed)`,
  pinned against the real engine in `tests/test_shed_overflow.py`). OFF,
  `overflow_left` is `deficit - sum(forced)` and `lots` is untouched, so the
  champion theta decodes byte for byte.
- **Still open:** the PLACE shed-deposit fallthrough.

Engine semantics now confirmed (no longer conditional on archaeology):
shed-adjacent only; dumps the unit's **entire** inventory; capacity
enforced at drop time; **overflow is destroyed** (unlike PLACE-to-shed,
which keeps the excess in inventory — also unimplemented in the sim);
units act before the same turn's market, so same-turn DROP→SELL works.
The sim has no DROP branch and `tests/test_planner_op_coverage.py` pins
that statically.

Module contents: implement DROP (and the PLACE shed fallthrough) in
`sim/units.py` with the exact discard semantics; extend the equivalence
suite (and add the missing PLACE-to-shed pin — see §6.4); add the return
leg to routing; **capacity law** — the plan must
guarantee shed room before a DROP executes, because DROP destroys what
does not fit; then **re-derive every terminal rule** through the 0.4
horizon parameter: day-29 harvest→DROP→sell-at-18 becomes legal, eod-28
production becomes monetizable, crop/animal/land horizons all shift.
Terminal laws are frozen only after DROP's fate is decided (review's
ordering, adopted).

## 5. New modules from verified findings

- **M1 — Prospective post-purchase land tasks** (0.3): **shipped
  2026-08-25**. A bought quadrant is developed the same day, on both the
  decision side (`brain.n_free_slots(..., land=)`) and the derivation side
  (`plan._derive`'s `prospective`). The 22 wasted turns per purchase are back.
  Two things it forced: `PolicyObs`' tile arrays carry **no canonical order**
  (raw for the simulator, serpentine for the submission), so nothing in `brain`
  may index a per-tile table against them; and the seed want is clipped to the
  tiles that will exist, because `brain` can only *predict* the grant.
- **M2 — Liquidity resequencing**: **shipped 2026-08-25**, at
  `SELL_TURNS[0]` rather than turn 2 — the wide HIRE row took turn 2 when
  `MAX_HANDS` went to 16. BUY_LAND rides that turn's spare tenth slot after the
  nine sells, which is the only same-day funding anything in this planner has,
  and it is what frees the BUY row for three animal slots. The simulator needed
  one addition after all (`market.apply_land_row`), because the cheap sell-only
  path compiles no atomic branch; it is exact rather than approximate, since
  BUY_LAND is atomic and seat-local. Guarded twice: 3/4 of the projection, and
  the hour-0 purse must still carry half the price itself. Moving more of the
  buy row after the sells still requires extending the sim's market schedule
  (see §6) — a measured, gated change.
- **M4 — PRESTOCK: tomorrow's shed inputs, bought tonight** (`plan.PRESTOCK_ON`,
  **OFF**, 2026-08-30). Measured on 39 real-engine replays: our units PASS
  18.5% of their turns against 8% for the strong opponents, and 34% of ours is
  the whole crew standing on its spawn tiles at hours 0–2 waiting for the BUY
  row — 390 unit-turns a game against an opponent's 34. That is the schedule
  and not a valuation miss: a unit acts *before* its turn's market, so while
  the morning's PICKUPs depend on a row that resolves at `TURN_BUY` = 1,
  `ROUTE_BASE` cannot be 1.

  The row does not have to be in the morning. `_end_of_day` banks the shed and
  never touches `seeds`, so on day *d* at `ops.TURN_PRESTOCK` = 20 — free,
  after the last lot, before nightfall — the day places tomorrow's
  BUY_PRODUCT row (feed wheat, fertilizer), and day *d+1*'s turn-1 row carries
  only the residual. BUY_ANIMAL stays at turn 1: an animal *is* stocked in the
  shed, but the herd mix is a same-day policy output today cannot forecast and
  a beast held overnight is shed room the eod dump wants.

  **BUY_SEED is measured and rejected** (`plan.PRESTOCK_SEEDS`, OFF): 12 games
  × 2 seats against kagg2 on `--seed-base 20260830` lost every game, mean
  margin −90,863 against +10,702. Feed and fertilizer are genuinely recurring —
  every animal eats every day — so "tomorrow wants what today wanted" is a real
  persistence claim; planting is not, it fills free land once, and on the day
  the land fills the forecast is exactly wrong. It is also wrong in the most
  expensive direction: `purse_left` is largest early, when the greedy has few
  tiles to want anything for, and an early coin compounds all season. Day 0 of
  seed 480603619 bought 19 seeds in the morning and 14 more at night out of a
  3,000-coin purse and opened day 1 on 28 coins. A future attempt needs a bound
  on tomorrow's *plantable slots* first, not on today's plantings.

  **The new schedule law**, which is where the coins come back: on a day whose
  residual BUY row is *empty*, nothing has to resolve at turn 1, so the
  overflow HIRE row moves from turn 2 into turn 1 and every unit starts a turn
  earlier — `ROUTE_BASE_PRE` = 1 / `ROUTE_BASE_WIDE_PRE` = 2, +1 worked turn
  per unit-day (22/21 → 23/22). Both still obey the one law that fixes them, "a
  hand hired in turn t first acts in turn t+1", which is how `ops._check_
  schedule` states them; the old `ROUTE_BASE == TURN_BUY + 1` invariant is kept
  for the live-row case and joined by the two prestock ones rather than
  deleted. The base is one traced scalar for the whole crew, not per unit:
  `_spawn_hand` puts a new hand on the least occupied shed-access tile, so one
  unit walking early re-scatters every later hand's spawn (`ops.ROUTE_BASE_
  WIDE`). A day that still has to buy at turn 1 keeps today's law exactly.

  **Forecast**: persistence on what the day itself *realised* — `want_feed`
  count for wheat, `n_fert_eff` for fertilizer, the seeds the route actually
  planted — netted against a per-product projection of tonight's shed (`shed +
  bought − sold − picked up + the inflow the reached blocks bank`). Not
  `macro.plant_target`: that is the raw gene want before `_wants` clips it to
  the tiles that will exist and before the labour boundary cuts it, and a farm
  with no free slots and a large target buys a full target's seeds every night
  and plants none — 0/24 games and −90,845 mean margin. Bounding the forecast
  by the *realised* plantings instead, which is what the code does, is still
  not enough (−90,863 on the same 24 games), which is why the seed row itself
  is off. Self-correcting both ways: an over-buy
  raises tomorrow's stock and shrinks tomorrow's prestock, an under-buy leaves
  a residual the morning row buys as it does today.

  **Overnight price risk is bounded and favourable** under the planner's own
  opponent-free model (§1.1): the town drains inventory every tick and price is
  monotone non-increasing in inventory, so a buy quote at turn 20 is never
  dearer than the same quote at turn 1 tomorrow. Shed room is not free, so the
  product half is clipped to `SHED_CAPACITY − proj_eod` (seeds live outside the
  shed and are not charged); cash is not free either, so the row spends only
  `Prefix.purse_left`, the coins the day's own greedy left in a purse already
  net of the hire bill and `cash_reserve` — the reserve therefore cannot be
  breached, and a short purse buys a prefix of the want rather than nothing.
  Nothing is prestocked when tomorrow is terminal (`day >= LAST_SHED_DAY`).

  The simulator needed the schedule extension §6.1 has always gated: `run_day`
  now takes the full market path at `TURN_PRESTOCK` too, under the same Python
  constant, so with the switch off the device program is the one it always was.
  Pinned by `tests/test_prestock.py`, and OFF verified end to end: 12 seeds ×
  2 seats re-run against `rep/hz_b30.csv` are identical in every column.

  **Measured 2026-08-30**, that same 12 × 2 smoke against kagg2 with the switch
  on (`--seed-base 20260830`, champion theta, DROP + HORIZON on in both arms),
  paired on (seed, seat): win 83.3% against 100%, mean coins 103,472 against
  99,263, mean margin +10,367 against +10,702 — paired diff −334, sd 7,707,
  t = −0.21, 95% CI [−3,418, +2,749]; 15 games up, 9 down; discordance 0:4.
  **Indistinguishable from zero at n = 24**, and its two halves point opposite
  ways: our own coins are up 4,209 a game (the extra turn is real work) but so
  are kagg2's, because the wheat we buy at turn 20 drains supply the other seat
  sells into the next morning. The paired sd is 7,707 against DROP's 581 — a
  whole-season perturbation, not a last-day one — so a promotion decision needs
  the 96 × 2 run on both seed bases the other switches were held to.
- **M3 — Structure conversion via DIG** (review's demolition correction
  confirmed): DIG removes living plants, weeds, and **empty structures**
  in both engine and sim (an escaped animal leaves its structure
  diggable); only an occupied structure resists; there is no other
  demolition op. Coop↔pasture conversion and dead-structure reclamation
  are 2-turn operations the planner has never had. V3's "no demolition
  exists" is retracted.
- **Open (the review's list, plus one from re-verification):** spatial
  placement of high-touch tiles near the shed; multi-kind animal days;
  harvest batching near `max_held`; cash reservation across days.
  Harvest-at-cap-saturation for one-time crops landed 2026-08-26 (see 0.1).
  Still open on the melon race, and both need the shed model to change: a
  same-day harvest -> shed-drop -> sell chain (§4 DROP), which is how kagg2
  sells 60 melon on the day it harvests them, and a day-0 melon plant target
  large enough to contest the virgin curve.

## 6. Equivalence-surface registry (verified constraints)

New hard facts any change must respect, found during verification:

1. The sim resolves the market **only** on hours 0–2 (full path) and
   10/18 (sell-only); the engine processes every turn. An order on any
   other hour is honoured by the engine and silently dropped by the sim —
   this gates M2 and any schedule change. M4 is the first change to spend
   that gate: under `plan.PRESTOCK_ON` the sim also takes the full path at
   `ops.TURN_PRESTOCK` = 20, decided at trace time so the off program is
   unchanged.
2. `core/ops.py:73-79`'s schedule comment is stale twice over (BUY_LAND
   is turn 1, and BUY_ANIMAL is ×1, not ×3); fix the comment, trust
   `plan.py`.
3. The sim scatters same-turn unit ops in parallel; cross-unit same-tile
   same-turn composition differs from the engine's sequential loop —
   upheld today by disjoint blocks, must remain an invariant of §1.6's
   router.
4. PLACE's shed-deposit fallthrough and DROP are the two unimplemented
   engine behaviours. Only DROP is test-pinned
   (`test_planner_op_coverage.py`); the PLACE fallthrough is guarded at
   plan time only — the test's own docstring says it pins the op *set*,
   not the guard. Adding that pin belongs to §4.
5. CARE is currently emitted on pre-maturity animals; the 0.11 value test
   subsumes this. (Not pure waste today: the bank pays at the first fire,
   clipped by `max_held` — at most 3 useful pre-maturity cares for a
   goose. Don't book it as a loss in the ablation prediction.)

## 7. Measurement plan, upgraded (review adopted)

`n ≥ 16` fixed seed pairs is sufficient for Layer-0 ablation smoke tests
only. Architectural decisions use: paired confidence intervals on matched
seeds; disjoint discovery vs held-out seed sets; multiple training seeds
for lineage comparisons; equal rollout and wall-clock budgets; an opponent
panel of current champions, a frozen historical pool, the archetype
ladder, and real-engine replays. Operational metrics logged per run:
walking turns, forced no-ops, units destroyed by overflow, unsold terminal
inventory, purchase shortfall vs plan, and task value dropped at the
labour boundary. **Reading note (Phase 2, 2026-08-25):**
`scripts/eval_vs_baselines.py --csv` reports "walking turns" as two columns,
because the two readings differ by an order of magnitude on an eleven-unit
day: `moves` sums MOVE ops over the seat's units, `move_turns` counts the
turns in which at least one unit walked. The turn is the resource, so
`move_turns` is this metric; `unsold` sums the nine market products only
(livestock in the shed is stock, not inventory that failed to sell).

Every optimizer lands with a compile-time and throughput
measurement (the day scan already pays ~6% per extra market turn; size
Phase-2 lineage runs against the pop × episodes = 32,768 zero-padding
ceiling).

**Headline prediction.** The measured land drain (−77.5k on a *free*
quadrant, dominated by buy→starve→escape→re-buy animal churn) is the
single most expensive known behaviour, and the 0.8 + 1.4 + 1.3 chain is
its direct antidote. The flagship Phase-1/2 claim, stated before the
runs: once the churn is priced, land value flips sign — and the kagg2
matchup, which hinges on quadrants 2–4, moves. Falsify this early; it is
the success metric beyond "no regression".

Reclassifications from V3 (per the confirmed corrections): the animal
gate (0.2) and day-28 fertilizer rule (0.4) are **not**
guaranteed-non-negative Phase-0 items — they carry value models and are
measured like any [EXACT-OPT]/[HEURISTIC].

## 8. Phases

- **Phase 0 — pure [LAW], sign-safe, no gene interaction:** the §1.1
  price projector (pure table arithmetic, `sell_walk`/`buy_walk` already
  exist in `sim/market.py` — required by 0.9's value ranking and 0.4's
  day-29 lot split), 0.1 deadline-clamped harvest (with its plant-gate
  consistency), 0.5 lexicographic tiers (all survival feeds mandatory
  until §1.4), 0.7 fert reservation, 0.9 overflow forced sale
  (conservative-low), day-29 endgame from 0.4, stale-comment fix (§6.2).
- **Phase 1 — laws touching live-gene behaviour + near-laws:** 0.6
  rationing, 0.8 animal-count semantics (predicted frozen-theta
  regression stated up front), 0.10 engine-curve pricing, 0.11 cadence +
  value-ranked fertilizer, 0.12 per-unit pickups, 0.2 animal bound, 0.4
  day-28 value-conditional rules. 0.11 already deletes four genes
  (`n_fertilize`, `fert_buy`, `feed_daily`, `care_on`): the current
  lineage keeps training with those heads decoded-but-ignored (unmasked
  and random-walking — harmless per §2), and Phase-1 frozen-theta
  ablations carry predicted sign changes beyond 0.8's wherever theta had
  learned compensations through them; state each sign before the run.
- **Phase 2 — optimizers + genome re-type (fresh lineage):** 1.2 sell
  (reservation + timing), 1.3 marginal-unit budget, 1.4 feed values, 1.5
  hire enumeration (benchmark-gated), 1.6 admit-then-route; parameter
  masking; an init-posture assertion that the z = 0 reservation
  (0.8·base) clears day-1 projected marginals — "the initial policy
  sells" is tested, not assumed.
- **Phase 3 — modules:** §4 DROP (then terminal re-derivation), M1
  prospective land, M2 liquidity resequencing, M3 DIG structure
  conversion, §3 walk-and-cap guard, per-parameter sigma trial
  (SNES/sep-CMA class — complement, not substitute).

The invariant, restated with its corrected strength: the planner emits
arrays both executors run verbatim, all integer, all ties broken; nothing
in the genome is a number the simulator could have computed; and no claim
in this document is stronger than its label.
