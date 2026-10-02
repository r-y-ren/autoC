# The sim tape-seat bug: pickup-before-drop — 2026-09-09

Resolves the open item in `docs/strategy/2026-09-09-loss12-sim-validation.md` §Fix 3
("root cause of the 4-tape gap is still open"). Working files in `S/simbug/`.

## Verdict

**A SIM BUG, not a tape-cut defect.** `sim/units.py:apply_units` resolves **every unit's
PICKUP before every unit's DROP / PLACE-into-shed**; the engine walks the units in index
order. When a recorded seat hands an item from one hand to another *through the shed in a
single turn* — a lower-indexed unit DROPs it, a higher-indexed unit PICKUPs it — the sim's
pickup finds an empty shed, the receiving unit gets nothing, and the item is stranded in the
shed for the rest of the season. The four bad tapes all do this with an **ANIMAL**; every
clean tape does it only with WHEAT / FERTILIZER, which the shed already holds, so the
mis-ordering is invisible there.

The defect is documented in the sim as a known limitation and dismissed as unreachable:

    src/kagg3/sim/units.py:89-96
    # The one place this ordering is not the engine's is a turn in
    # which a *lower*-indexed unit DROPs while a higher-indexed one PICKUPs:
    # the sim resolves every pickup first. The planner keeps its pickup turns
    # and its drop turn disjoint (`plan._route`) ...

That invariant is a property of OUR planner. A tape seat does not honour it.

## First divergence — 107089992 (−7,510 margin)

Engine baseline reproduces `S/lossflip/flow166_g50.csv` to the coin (ours 131,011 / tape
134,543); the sim on the same board, theta, tree, knobs and seed ends 133,507 / 129,758.

Turn-by-turn (`S/simbug/diff.py`, sim per-turn trace vs the engine's 720 observations), the
**first** state disagreement of any kind is **day 7, hour 11**, and it is one coin-free unit:

| | sim | engine |
|---|---|---|
| tape seat shed after d7 h11 | `WHEAT 3, COW 1` | `WHEAT 3` |

The action at that turn (tape seat, unit slots 0..7):

    farmer NORTH | 1 SOUTH  2 SOUTH  3 NORTH  4 WEST  5 DROP  6 PICKUP COW  7 EAST

Slot 5 drops the COW it is carrying into the shed; slot 6 — **higher-indexed** — picks it
straight back up. The engine applies them in that order, so slot 6 leaves the turn holding
the cow and PLACEs it on a pasture three turns later (`d7 h14: ... 6 PLACE COW`). The sim
runs slot 6's PICKUP first against a shed with no cow, takes nothing, then banks slot 5's
cow — the shed's `COW 1` never moves again and the `PLACE COW` at h14 is a silent no-op.

One cow ≈ 22 days of MILK. The market ledger shows it: from day 15 the sim's MILK inventory
runs 3-9 units below the engine's every day and the tape's purse falls away —
d15 −1,605, d20 −2,501, d25 −3,962, d29 **−4,785** — while ours *rises* to +2,496, because
the milk the tape never sells is supply our seat's own sales no longer have to walk down.
Theta-dependence follows: whether the shed happens to hold a spare COW at that turn, and what
the missing supply is worth, are both functions of our seat's play.

## Verified across the set

`S/simbug/handoff.py` counts turns where a lower-indexed unit DROPs/PLACEs while a
higher-indexed one PICKUPs, over all 12 loss12 + 10 family tapes:

| tape | violations | **of an ANIMAL** | first animal one |
|---|---|---|---|
| **107072760 / 107089992 / 107090008 / 107095149** (all four BAD) | 8 | **3** (2 COW, 1 SHEEP) | d7 h9, unit 5, COW |
| every other loss12 tape (8 clean) | 5-8 | **0** | — |
| family tapes (10, sim-clean) | 7-17 | **0**, except 105232167 = 1 SHEEP | — |

Perfect separation on the animal column. The WHEAT / FERTILIZER violations are harmless
because the shed is already carrying those, so the pickup succeeds from stock and the drop
merely lands a moment later — which is also why 105232167's single SHEEP hand-off costs it
nothing (its shed held a bought SHEEP at that turn) and why the four bad tapes' *first*
animal violation (d7 h9) is also free: the cow bought at d7 h8 was still in the shed. It
bites at the **next** one, d7 h11, when the shed is empty.

## Code

* Sim: `src/kagg3/sim/units.py:65-78` (PICKUP stage, `cum = cumsum(per_item)` against the
  hour-start shed) runs before `:79-127` (DROP / PLACE-into-shed stage, `d_cum` against the
  hour-start room). Two independent prefix sums, two independent baselines.
* Engine: `kaggle_environments/envs/kaggriculture/kaggriculture.py:935-939` walks
  `[farmer, *hands]` in list order through `_apply_unit_action`, whose DROP (`:343`),
  PICKUP (`:358`) and PLACE-into-shed (`:377`) branches all mutate `private["shed"]`
  immediately.

## Ruled out

* **Tape-cut defect.** `S/simbug/recut_check.py` rebuilds `TapeActions` from each engine
  package's `_TAPE`/`_TOWN` and compares to `artifacts/tape_actions_town/<id>.npz`:
  all 22 tapes byte-identical, towns included.
* **Row / unit caps.** Max units in a frame 12-13 (`MAX_UNITS` 17), max market row exactly 10
  (`MAX_MARKET_ORDERS` 10) — `TapeActions.dropped` empty everywhere (`S/simbug/capcheck.py`).
* **Quote-walk length.** `market.K = MAX_UNITS_PER_ORDER + 1`; SELL/BUY are pre-capped by
  shed / room ≤ `SHED_CAPACITY`.
* **Town.** Every npz `town` equals the `S/band2100p/town_schedules.json` row `town_inject`
  gives the engine.
* **Same-tile collisions.** Present on every tape (29-55), so not the discriminator.
* **Market slot ordering.** `_process_market` pairs raw queue positions and the sim's
  `compact_orders` + uncompacted tape row reproduce it; both sides agree to the coin on the
  control tape 107079367 for all 720 steps (sim 101,977 / 117,214 = engine exactly).

## Minimal fix (described, not applied)

Make the shed stage of `apply_units` a single **unit-index-ordered** walk instead of two
passes. A unit performs one op per turn, so droppers and pickers are disjoint sets and the
closed form survives: give the two prefix sums one shared unit axis, so that

* a PICKUP by unit `j` sees `shed_start + deposits(i<j) - takes(i<j)`, and
* a DROP / PLACE by unit `i` sees `CAP - (shed_start + deposits(<i) - takes(<i))`

rather than each seeing the untouched hour-start shed. (Equivalently, and simpler to get
right: replace the two `cumsum`s with one `lax.scan` over the 17 unit slots for the shed
stage only — that is literally the engine's walk, and 17 steps a turn is cheap next to the
10-slot market scan already inside the same turn body.)

Until it is fixed, the sim's LOSS12 column stays unreadable on 107072760 / 107089992 /
107090008 / 107095149, exactly as `2026-09-09-loss12-sim-validation.md` §Fix 1 says. Note the
same defect can bite ANY future tape rung whose recorded seat hands an animal between hands —
it is not specific to the loss12 cut, and `S/simbug/handoff.py` is the screen for it.

## Confirmation on the other bad tapes

`S/simbug/predict.py` takes an engine dump and reports the first turn where a higher-indexed
unit PICKUPs item X with a lower-indexed DROP/PLACE in the same turn **and** the seat's shed
held zero X going in — the exact trigger. On 107089992 it returns the observed first
divergence to the turn and the unit, and on the clean control it returns nothing:

| tape | engine (ours / tape) | predicted first blocked hand-off |
|---|---|---|
| 107089992 (bad) | 131,011 / 134,543 | **d7 h11, unit 6 PICKUP COW, dropper unit 5** (= measured) |
| 107090008 (bad) | 125,188 / 133,488 | **d7 h11, unit 6 PICKUP COW, dropper unit 5** |
| 107095149 (bad) | 98,778 / 122,088 | **d7 h11, unit 6 PICKUP COW, dropper unit 5** |
| 107072760 (bad) | 131,587 / 128,489 | **d7 h11, unit 6 PICKUP COW, dropper unit 5** |
| 107079367 (clean control) | 101,977 / 117,214 | none — and the sim matches to the coin, all 720 steps |

Every engine figure reproduces `S/lossflip/flow166_g50.csv` exactly, so the dumps are the
right baseline. The four bad tapes are one author's build and all stage the same day-7
cow hand-off; the predictor is the cheap screen for the same defect on any future rung.
