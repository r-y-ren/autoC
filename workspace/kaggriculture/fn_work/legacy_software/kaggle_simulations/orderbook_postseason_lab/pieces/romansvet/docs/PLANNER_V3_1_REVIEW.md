# Planner v3.1 review

Reviewed 2026-08-24 against `PLANNER_V3_1.md`, its lineage (`PLANNER_V3.md`,
`PLANNER_V3_REVIEW.md`), the pinned engine
(`kaggle_environments/envs/kaggriculture/kaggriculture.py`), and
`src/kagg3/{core,sim,agent,es}`. Method: seven independent verification
passes, one per factual cluster (harvest/plant, animal/fert/CARE,
land/market schedule, sell timing/prices, genome/ES, DROP/DIG/endgame,
pickups/labour), each checking the document's claims against code and
*executing* the computation wherever the claim was numeric.

## Verdict

V3.1 is fit to be the implementation specification. The claim-taxonomy
discipline it introduces largely holds up: re-verification confirmed
essentially every [LAW] mechanism, many to the digit (the 20-wool
4,313/4,735 split reproduces exactly; the "later is weakly better" sell
ordering survived a 103,140-configuration brute force with zero
violations; the 165-param dead block is exact; the ~0.23·lr random-walk
constant is the correct Adam RMS ratio √((1−β1)/(1+β1)) ≈ 0.229). The
review-correction folding is faithful: all thirteen dispositions match
what the code supports.

What needs fixing is short and none of it is architectural: two numeric
slips (§0.2's goose break-even, §0.11's tomato +4), one off-by-one in the
dead-head slice that would corrupt the §2 parameter mask if transcribed
literally, a genome table whose own arithmetic does not reconcile, one
overstated test claim (§6.4), one unstated renderer prerequisite (§3),
and phase-dependency gaps (§8). Correct these in place; no V3.2 is
needed.

## Independently confirmed, sharper than stated

- **§0.1 in full.** Engine HARVEST (`kaggriculture.py:446-473`) checks
  only `yield_units > 0` and `age >= first_yield_day`; one-time crops are
  born with `yield_units = 1` (`:223`); the same-day
  FERTILIZE→WATER→HARVEST chain works and the planner already orders it
  correctly (`plan.py:412-426`). The arithmetic is exact: wheat d25 → 3
  units (5 fertilized, window ages 2–4, cap 6); melon d17 (age 10 or 11)
  and d18 (age 10) both reach the 6-unit cap with five in-window
  waterings (window ages 6–12). The current planner really never
  early-harvests (`plan.py:277-280`, `age >= max_yield_day`), and the
  current plant gate really is `day + first <= 28` (`brain.py:289`).
- **§0.3 and M1.** `_do_buy_land` unlocks in place during the same
  turn's market (`kaggriculture.py:712-726`); movement is deliberately
  never blocked by LOCKED (`:324-331`, with an explanatory comment);
  `LAND_ORDER`/`LAND_PRICES` make the next quadrant computable at hour 0
  (`:95-97`, sim `market.py:110-113`). The purchase day is confirmed a
  dead day today: `build_day` runs once on the hour-0 snapshot and
  `KIND_LOCKED` tiles never enter `free_slot` (`plan.py:257-267`).
- **M2 end-to-end.** The engine truncates the raw order list to 10 and
  resolves slots strictly in order with money committed between slots
  (`kaggriculture.py:551-580`, `:658`); the sim's `_market_turn` is a
  `lax.scan` over the ten slots carrying the full state, so a turn-2
  slot-9 BUY_LAND sees the nine sells' proceeds and the affordability
  check runs against updated money (`rollout.py:110-127`,
  `market.py:114,169-172`). "Legally funded by lot-1 revenue with no sim
  change" is literally true. (Order compaction shifts the slot index but
  preserves ordering — harmless.)
- **§1.1/§1.2 facts.** Price monotone non-increasing in inventory for
  all 9 products across all 85,001 tabulated entries (0 violations;
  verified against the engine's `market_price` on 2,700 random points
  with 0 mismatches); floor sales pay without adding supply
  (`kaggriculture.py:658-661`); town cadence and fertilizer exclusion as
  stated. The wool example reproduces exactly (turn-2 4,313, turn-18
  4,735, splits monotone between), and a brute force over 103,140
  opponent-free configurations found **no** case where any split beats
  all-at-18 — the doc's caution that greedy needs a fallback check is
  honest but the opponent-free ordering is even more solid than claimed.
- **§3 zero-quantity SELL.** Verified by direct engine execution:
  `_parse_order` returns `None` for qty ≤ 0 (`kaggriculture.py:639-648`),
  the slot keeps its index (truncation precedes parsing, pairing is
  positional, `:560-570`), cross-seat coupled resolution measurably
  changes when the placeholder is removed, and the inert order does
  consume one of the 10 slots.
- **§4/M3.** DROP destroys overflow (`:343-356`, unconditional
  `del inv[item]` after the partial take); PLACE-to-shed keeps the excess
  (`:393-410`); units act before the same turn's market (`:935-941`);
  DIG removes plants, weeds, and empty structures but not an occupied one
  (`:484-491`), sim agrees (`units.py:125`); no other demolition op
  exists. Escape is two consecutive unfed days (`:817-819`).
- **§0.11/§0.12 code contact.** `want_fert` really is serpentine-
  positional (`plan.py:388-390` via `_rank`, a pure prefix count) — the
  mechanistic story for "raising the fertilize gene measured worse"
  stands. The §0.12 change-set names the actual variables: `cum`
  (`plan.py:524`), `cpick` (`:519`), `prev` currently *below* the cut
  (`:566` vs cut at `:537-539`), global `pk_turn` shape [3] (`:485`),
  shared budget `22 − n_pickup` (`:452-453`). `D(s,e)` is buildable from
  `cpick` exactly as described, and `L(e)` is monotone.
- **§2 mechanics.** `brain.decide` consumes exactly 52 scalars of the
  network's 58; the dead-parameter block is exactly 165
  (`g2[:,13:18]` = 160 + `gb2[13:18]` = 5); the update rule is pure
  elementwise Adam with decoupled scalar decay and no norm coupling
  (`train.py:346-363`), so the strong-form refutation of review issue 13
  is mathematically right — dead-coordinate noise cannot leak into live
  updates, and masking is correctly claimed as hygiene only. The ~0.23·lr
  figure is the right RMS constant and is sigma-independent as claimed
  (simulated 0.221·lr with the trainer's exact rule).
- **§6.1.** The sim resolves the market only at hours 0–2 (full) and
  10/18 (sell-only, non-SELL ops filtered) — `rollout.py:159-172`,
  `market.py:159-161`; the engine processes every turn.

## Errors to correct

### 1. §2: the dead head slice is `head[13:18]`, not `head[13:17]`

Five head outputs are dead (13, 14, 15, 16, 17), not four: `head` reads
stop at `head[8:13]` (`brain.py:309`, `ORDER_HEAD0 = 8`, width 5) and
`N_HEAD_OUT = 18`. The doc's own totals prove it — "6 more are computed
dead" only sums with 5 head slots + grow-of-fertilizer, and 165 = 32×5 + 5
only works for five columns. As a Python slice, "head[13:17]" is four.
This matters because §2 turns the slice into a perturbation/update mask:
transcribed literally it leaves `g2[:,17]`/`gb2[17]` (33 params) live.
Write `head[13:18]` everywhere (and note `policy.py:69` uses the
inclusive "head[13..17]" naming that likely caused the slip).

### 2. §2: the genome table does not reconcile with itself

The baseline 52 counts `aux[3]` as three separate scalars (sell 9 +
gate 9 + grow-crops 5 + grow-animals 3 + prio 9 + order 5 + head[0:8] 8 +
lots 1 + aux 3 = 52 — verified itemization). Under that same convention:

- kept/re-typed: reservation 9 (ex-sell) + press 9 (ex-gate) + grow 8
  (see below) + dev_frac + its free-tile aux 2 + animal_share 1 +
  buy_land + afford aux 2 + sharpness 1 = **32**;
- deleted: order 5 + prio 9 + n_hire + n_fertilize + fert_buy +
  feed_daily + care_on + sell_lots = **20**, and 52 − 20 = 32. ✓

The doc says "31 decoded outputs" and "Deleted as decisions (21)" — the
deletion list it prints sums to 20, and 31 is reachable only by also
deleting one aux (which one is never said). Separately, the table row
"grow value multiplier | 9" implies reviving grow-of-fertilizer, but no
§1.3 candidate consumes a fertilizer grow value (fertilizer is valued by
§0.11's clipped-marginal table), so grow stays effectively 8-wide — and
since the encoder is shared across products there is no fertilizer column
to mask either way. Given review issue 13 was precisely "the counts are
wrong," §2 should print the full itemization (which slot maps to which
new output, including both aux slots and the grow-of-fert status) rather
than a summary count. The ES conclusion is unaffected.

### 3. §0.2: the goose worked example overstates the break-even

Verified against the engine: a d25 goose gets fertilizer collections on
d26–d29, of which **3** are sellable (a d-day collection reaches the shed
at eod d; the d29 one is worthless), and eggs contribute 0 (first fire
eod d28, harvestable only d29). Cost 300 → break-even fert price is
**100/unit — the base price, i.e. zero net purchases** — or ~108 (~40–45
net purchases) including the one survival feed. At the doc's 118 the
goose is already ~50 coins ahead. The doc's number appears to solve
3 × p = 354 rather than 300. The correction *strengthens* the section's
point — a fixed day cutoff is even further from a law than stated — but
the printed 118/~90 pair is wrong.

### 4. §6.4: only DROP is pinned by tests

`test_planner_op_coverage.py` sets `UNIMPLEMENTED = frozenset({O.OP_DROP})`
and regex-pins plan.py against it (`:39-40`, `:61-63`). The PLACE-to-shed
fallthrough is **not** test-pinned — the test's own docstring says so
explicitly ("these tests pin the op *set*; they do not prove the guard
still holds hours later in the day", `:20-25`); PLACE safety is a
plan-time structural argument. "Both pinned by tests until §4 ships"
overstates it; §4's module list should include adding that missing pin
(or the equivalence test) rather than assuming it exists.

### 5. §0.11: tomato "+4" is a two-fertilize ceiling

Simulated through the engine's WATER and eod paths: one fertilize's
3-day window covers at most 3 of tomato's 4 fires (interval 1, fires at
ages 8–11), so a single application yields at most **+3**; +4 needs two
applications, and every eod bonus additionally requires `was_watered` on
that same eod (`kaggriculture.py:799`) — which the current planner does
not guarantee (it waters ongoing crops every other day). Since §0.11
ranks fertilizer targets by "exact clipped marginal value," the table
must be per-application (tomato ≤ +3 per fertilize) and must count only
fire days the watering rule will actually cover. Wheat +2, carrot +1,
melon 0 are all confirmed exact.

## Label corrections

### 6. §0.2's rejection bound is safe only opponent-free

Fertilizer's price rises with the purchase deficit and has no town
demand, so the "CURRENT projected fertilizer price — optimistic" is an
upper bound only if nobody buys fertilizer later. Opponent purchases
(or own future planned ones) raise the price path above the projection,
so a rejection can, in principle, discard a profitable animal. The
failure direction is benign (a foregone marginal option, not a loss),
but a [LAW]-adjacent "the rejection is safe" needs the opponent-free
qualifier — the same honesty §1.1 already applies to the projector.

### 7. §1.4's value must include the pending care bank

The care bank pays only if the animal is fed on the fire day and is
wiped unconditionally at every fire (`kaggriculture.py:826-828`,
verified empirically). An animal carrying a banked bonus into a
monetizable fire day therefore has feed value = remaining base
production + the bank; §1.4 as written ("remaining conservatively-
projected sellable production") doesn't say the bank is included, and a
literal implementation could fail the feed test and silently wipe a
bonus §0.11 paid labour to build. One clause fixes it.

### 8. §0.1's clamp is the minimal dominant fix, not the optimal harvest day

For a crop whose yield cap saturates before the clamp day (melon d17
saturates at age 10, the clamp says age 11), harvesting at saturation
gives the same units one day earlier — freeing the tile, saving a
clipped watering, and moving the sale a day forward. The [LAW] label is
honest as written (the clamp strictly dominates *current* behaviour, and
"exactly current behaviour" otherwise), but a one-line acknowledgement
that harvest-at-cap-saturation is the stronger rule (valuation-gated,
so [HEURISTIC]) belongs in §1.3's open items.

## Specification gaps

### 9. Phase 0 depends on machinery no phase provides

- §0.9 (Phase 0) force-sells "lowest marginal value first" and §0.4's
  day-29 rule liquidates "across the three lots" — both need the §1.1
  price projector, which has no phase assignment at all.
- §0.5 (Phase 0) puts "survival feeds that pass §1.4's value test" in
  the mandatory tier — §1.4 is Phase 2.

Either assign §1.1 to Phase 0 (it is pure table arithmetic and
`sell_walk`/`buy_walk` already exist in `sim/market.py`), or state the
interim rules explicitly (e.g. Phase-0 mandatory tier takes *all*
survival feeds; day-29 liquidation splits lots naively — still
sign-safe vs holding). As written, a faithful Phase-0 implementer has to
invent unstated behaviour inside items labeled "pure [LAW]".

### 10. §3's guard needs the renderer to emit the zeroed lot

Today an empty lot is encoded `MO_NONE` (`plan.py:643-648`) and the
renderer *drops* it (`render.py:35-37`), compacting the list — exactly
the alignment-shifting case the zero-quantity mechanism exists to avoid.
Walk-and-cap therefore requires the executor to emit `SELL item 0` as a
kept placeholder (and the plan/compaction path to carry qty-0 SELLs
with `op = MO_SELL`, which `compact_orders` preserves). Also worth
stating: the current executor is fully open-loop (`runtime.py:24-34`
builds the plan at hour 0 and replays it; at turns 10/18 it reads
nothing from the observation but the hand count), so "the executor
observes the live market" is new wiring on both backends, not a tweak —
the observation does carry live prices every turn, so it is cheap, but
it is the one place V3.1 grows the executor beyond verbatim replay and
deserves its own equivalence test entry (the doc's §3 test list is
right; the renderer prerequisite is the unstated part).

### 11. §2's transforms are directions, not formulas

"softplus(z) scaled to [0, 4] around 1" is unbounded as written;
`base_p × softplus(z)/softplus(0)` puts the reservation price exactly at
the base price at z = 0 — i.e. a fresh lineage starts out holding
essentially everything (press starts at 0, so no timing offset either).
That may be a bad opening posture for training (no revenue → starved
budget walk). Pin the exact formulas, their clips, and the intended
z = 0 posture (e.g. scale reservation init to ~0.8 × base so the initial
policy sells), and note the `_qfloor` quantization point for each.

### 12. Phase 1 deletes four genes before the fresh lineage exists

§0.11 (Phase 1) deletes `n_fertilize`, `fert_buy`, `feed_daily`,
`care_on`; the fresh lineage and masking arrive in Phase 2. State the
Phase-1 treatment explicitly: the current lineage presumably continues
training with those heads decoded-but-ignored (unmasked, random-walking
— harmless per §2's own analysis), and Phase-1 frozen-theta ablations
carry predicted sign changes beyond §0.8's (any theta that had learned
compensations through the deleted genes regresses). The doc demands
"predicted sign stated before the run" for 0.8; the same discipline is
owed here.

## Minor notes

- §1.1's "1..3,100" fertilizer span is the *tabulated* range including
  the negative-inventory tail (`PRICE_TABLE_LO = -5000`); the
  game-reachable maximum from inventory 0 is 2,100. Fine as written,
  worth a parenthetical.
- §6.2's stale `ops.py:73-79` comment has a second error the doc
  doesn't mention: it says BUY_ANIMAL ×3, the actual row is ×1
  (`plan.py:600`). Fix both while in there.
- §6.5: pre-maturity CARE is not pure waste — the bank pays at the
  first fire, clipped by `max_held` (≤3 useful pre-maturity cares for a
  goose). §0.11's value test handles this correctly; just don't book the
  current behaviour as a loss in the ablation prediction.
- §0.4's "cut at 718": 718 is the last *executed* step (719 turns,
  0..718); the sim matches exactly (29×24 + 23). Phrasing is fine, an
  implementer counting turns should mind the off-by-one.
- "Day-29 harvests never reach the shed" is a statement about the
  sim/current planner; the engine allows day-29 DROP→SELL — which is
  exactly §4's re-derivation clause, so no change needed, but the [LAW]
  is conditional on DROP staying unemitted, as the op-coverage test
  enforces.
- Agent-2/6 cross-check of §0.2's sellability bound: a fire at eod d is
  monetizable iff d ≤ 27 (harvest d+1, shed eod d+1, sell d+2 ≤ 29) —
  the doc's `d_fire + 1 <= 28` is the same bound. Correct as printed.

## Strategic notes (non-blocking)

- **Say out loud that the land-toxicity autopsy is the target.** The
  measured drain on a *free* quadrant (−77.5k, dominated by the
  buy→starve→escape→re-buy animal churn) is the single most expensive
  known behaviour, and V3.1's §0.8 + §1.4 + §1.3 chain is precisely its
  antidote — but the doc never names it. The headline Phase-1/2
  prediction should be: once the churn is priced (feed-exit rule +
  no-restock semantics + marginal animal valuation), land value flips
  sign, and the kagg2 matchup — which hinges on quadrants 2–4 — moves.
  That is the empirical claim most worth falsifying early, and it gives
  the phases a success metric beyond "no regression."
- **Throughput gates are well-placed.** §1.5's 11 prefix passes and
  §1.6's nearest-insertion both sit inside the compiled day scan, where
  the codebase has already measured ~6% per extra market turn; the
  per-optimizer compile/throughput gate in §7 is the right control.
  Budget-wise, remember the zero-padding ceiling (pop × episodes =
  32,768) when sizing Phase-2 lineage runs.
- **The measurement upgrade in §7 is the review's best adoption.**
  Paired CIs on matched seeds, disjoint discovery/held-out seed sets,
  and per-run operational metrics (forced no-ops, overflow losses,
  unsold terminal inventory) directly instrument the failure modes the
  optimizers claim to fix. Endorsed as written.

## Bottom line

V3.1 does what it promises: no claim materially exceeds its label, the
folded corrections are faithful to what the code supports, and the two
deepest mechanisms it stakes the design on — the deadline-clamped
harvest and the marginal-value re-typing of the genome — are verified
exact. Fix the §2 accounting and slice notation before anyone builds
the mask, correct the two worked numbers, add the missing PLACE pin and
renderer prerequisite, and give Phase 0 its projector. Then implement.
