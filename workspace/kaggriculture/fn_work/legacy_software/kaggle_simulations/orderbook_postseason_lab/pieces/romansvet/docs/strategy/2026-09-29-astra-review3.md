# ASTRA_REV3 (2026-09-29 17:18Z-17:40Z) — gpt-6-astra code review 3/3 of the shipped tree (master cf68f736): decision, market, sales, animals, parsing, guards

Coordinator: Claude Fable 5.1. Prompt: S/astra_rev3/prompt.md (common header S/astra_rev/common.md). Output verbatim below. Reviews 1 (router/crew) and 2 (tiles/asks) = 2026-09-29-astra-review1.md / -review2.md.

## Prompt

### CODE REVIEW OF THE LIVE KAGGLE AGENT (read-only) — 2026-09-29 17:17Z

You are gpt-6-astra, the third participant of this team. The user (team lead) just said: "PFS skip tiles, crew is lazy, do review for router! ask astra to review all code". PFS = our live body (Kaggle simulation "Kaggriculture": 2 farms per game, 30 days x 24 hours = 720 steps, tiles for crops wheat/carrot/tomato/strawberry/melon, animals cow/sheep/goose in pastures/coops, hired hands, a shared market whose prices walk with both players' sales; final score = coins; rating = Bradley-Terry over wins).

The code under review is the EXACT shipped tree (git master cf68f736 = live submissions vrp20_pfsoff / vrp21_clsearch), copied to `S/astra_rev/mastertree/src/kagg3/` (35k lines; core/plan.py 15,994 lines is the day planner; agent/route_vrp.py the live crew router; core/brain.py the Macro decision; agent/runtime.py the per-turn loop; sim/* the projection engine used for planning). Read code with cat/sed/grep. You may run short read-only python checks. NEVER write to or read from any /dev/* path (no `> /dev/null`, no `2>/dev/null`, no `< /dev/null`, no process substitution) — the user forbids it; NEVER run pytest; NEVER modify files; do not run the simulator for more than 2 boards.

#### The user's three complaints, with the measured evidence (all in this repo)
1. EMPTY TILES. `S/gapcensus2/agg.txt` (104 live games of vrp7/vrp8, same planner): empty tile-days per game d0-27 ours 125.6 vs opponents 72.8; d20-27 ours 75.2 vs 38.7; per-tile map: corner (0,9) = 100 % empty on every game, (9,0) 64.6 %, (0,0) 41 %, the whole outer ring 15-40 % while the centre is 0 %. `docs/strategy/2026-09-26-gapfix1.md`: the cause found was the planner's ask floor `n_dev = _qfloor(dev_frac * n_free)` plus an `n_free-1` rounding, NOT seeds/cash/labour; `docs/strategy/2026-09-26-gapcensus1.md`: replanting stops d19-25 with 61k cash and 0 seeds in stock; 43 more empty tile-days/game than rivals. Every fill patch tried so far (EMPTY1, late ask floor, SLIVER1, IDLETILE1, LATEPLANT1, ROUTEFILL1 — docs/strategy/2026-09-26-*.md, 2026-09-24-routefill1.md) lost coins on the paired judge, mostly because the crew could not serve the extra tiles or the extra wheat moved the shared price. The user does NOT accept the axis as closed: "empty tile is our loss".
2. LAZY CREW. `S/idleops/report.md`: idle unit-turns per game ours 706 (10.5 % of 6,689 unit-ops) vs our opponents 540 (7.9 %) vs the rank-2 team 335 (5.1 %); by hour ours h0-5 = 21 % idle vs opponents 3 %, h18-23 20.7 %; by cause 684 of the 706 are "work exists" of which 326 have work under the unit's feet (dist 0) and 265 at dist 1. `docs/strategy/2026-09-22`-era read: idle 604 unit-turns/game = h0-2 260 (h1 195 = spawn + pickup wait) + h21-23 270 (h23 166). Top-1 read (docs/strategy/2026-09-19-majkel1.md): the leader's idle 52 vs our 296 unit-turns on the same board; his wheat plantings 177 vs our 139. MOVES: 2,891 unit-turns of moves per game vs a minimum-spanning bound of 1,461 (43 % of all unit-turns are moves).
3. ROUTER. `docs/strategy/2026-09-26-routeraudit1.md` + `S/routeraudit1/out/summ2.txt`: the shipped VRP router saves 2,101 coins/game of hand bills vs an oracle 2,823 and an rr150 variant 2,693 (not shipped: p99 wall 1.05 s). `docs/strategy/2026-09-27-crewaudit1.md`, `2026-09-29-crew1.md`, `2026-09-29-crewloss1.md`, `2026-09-29-crewloss2.md`: crew audits on the newest games. `docs/strategy/2026-09-23-crew24.md`, `2026-09-23-crewrelay1.md`, `2026-09-24-routeopt1.md`, `2026-09-24-routeopt2.md`, `2026-09-16-routeeff.md`, `2026-09-16-routeorder.md`: earlier router work.

Other facts you need: hands are hired daily at dawn (HIRE at h0) and paid per day; the planner (`core/plan.py: _derive` -> `_routes` -> `_market`) builds one day plan at h0 from a projection and the router (`agent/route_vrp.py: solve_plan/apply`) turns it into per-hour unit moves; per-turn wall budget matters (Kaggle actTimeout; overflow.py guards). The judge that decides shipping now is the closed loop against the faithful public reacting rival "V56" (`S/vband1/vr.py`, 21 live boards + 40 boards) and against the top-10 programme clone `p48c` (`bash S/reactclone1/judge.sh --rival p48c`); a candidate must not lose late animal-product volume or the d15-17 strawberry supply (docs/strategy/2026-09-29-vcheck2.md).

#### What we need from you
A real code review, not a summary. For EVERY finding: (a) file:line in the mastertree copy, (b) the mechanism in 2-4 sentences, (c) when it fires (days/hours, how often per game, from the evidence or from the code), (d) your estimate of coins/game it costs and the reasoning, (e) the minimal fix, behind a module-level switch that defaults to the current behaviour (byte-identical OFF), with the exact edit described, (f) what could go wrong (price walk, crew overload, timeout). Rank the findings by expected coins/game. Say explicitly for each of the user's three complaints which finding is the ROOT cause and which prior closure (if any) was wrong and why. Do not repeat things already closed unless you show the closure's flaw with a citation. If you find actual BUGS (wrong index, stale state, off-by-one in day/hour, mis-parsed observation, a guard that never fires, dead code that still costs wall time), list them first. End with: the 3 findings to build TODAY (each with the judge bar: margin vs V56 and vs p48c, our own coins, strawberry wall, late animal units) and one line on what you could not check.

Output: markdown, at most 300 lines, a findings table at the top (rank | file:line | title | fires | coins/game | fix size). Write it to the -o file only.

#### YOUR SCOPE (review 3 of 3): EVERYTHING ELSE — decision, market, animals, parsing, guards
Files: `core/brain.py` (Macro decision, all 1,481 lines), `core/policy.py`, `core/valuation.py`, `core/budget.py`, `core/projector.py`, `core/ops.py`, `core/residual_head.py`, `sim/market.py` (the price model used for planning: does it match the real market walk, incl. the rival's sales?), `sim/rollout.py`, `sim/eod.py`, `sim/units.py`, `agent/parse.py`, `agent/tell.py`, `agent/runtime.py`, `agent/overflow.py`, `spec.py`, `precision.py`, and the live use of `es/*` (which of archetypes.py / tape_actions.py / tape_flow.py / train.py runs at inference?). In `core/plan.py` review the sale logic (`_lot_split` 6736 and every SELL construction: grep -n "SELL" core/plan.py | head -120), the animal logic (FEED/CARE/PLACE/BUY_ANIMAL; escapes; feeding wheat vs selling wheat), the fertilizer logic (FERTILIZE/COLLECT_FERTILIZER), and the hire/unhire logic. Questions to answer with code evidence: actual bugs (wrong index into the observation, stale per-day state, off-by-one in day/hour boundaries, a guard that can never fire, an exception swallowed into PASS); every place the agent emits PASS while an action was legal and valuable; whether held product is sold too late/early relative to the price walk the market model predicts vs the real one; whether feed/care schedules leave animals unproductive (escapes, missed CARE) — and how many coins each costs per game.

## Astra's review (verbatim)

| rank | file:line | title | fires | coins/game¹ | fix size |
|---|---|---|---|---|---|
| 1 | [core/sell.py:90](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/core/sell.py:90) | **BUG: floor sales create phantom supply in later lots** | Earlier lot reaches $1; subsequent town drain restores prices | 0–100 | 40–70 lines |
| 2 | [agent/overflow.py:227](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/agent/overflow.py:227) | **BUG: overflow projections ignore yield-changing actions and misclassify animal placement** | d0–28, h10–23, before remaining WATER/HARVEST or animal PLACE | 0–60 | 45–80 lines |
| 3 | [agent/overflow.py:170](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/agent/overflow.py:170) | **BUG: terminal DROP protection can strand the valuable cargo** | d29 h22, mixed cargo exceeds remaining shed room | 0–20 | 25–40 lines |
| 4 | [agent/overflow.py:473](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/agent/overflow.py:473) | **BUG: future planting’s mandatory WATER is valued at zero** | d0–28, h10–23; overflow diversion retains PLANT but removes its WATER | 0–20 | 4–6 lines |

¹ Provisional recoverable **own-coins/game** ranges, ranked by plausible opportunity. These are engineering estimates, **not measured paired gains or statistical bounds**; live trigger counts remain unmeasured. They overlap and must not be added. The reproduced defects establish incorrect behavior, not positive closed-loop expected value.

All code locations below refer to `S/astra_rev/mastertree/src/kagg3/`. No files were modified, no pytest was run, and no full simulator boards were run.

**1. Floor-price sales incorrectly depress later projected quotes**

**Mechanism.** `sell.adjusted_marginals` adds every earlier allocated unit to later inventory through `cumsum(lots)`, then calculates later-lot externalities from that inventory. The engine adds supply only for units sold **above** the floor; `sim/market.py:697` implements that distinction correctly. `projector.py:10` correctly explains why an uninterrupted single sale can still use `price[inv+j]`; that argument does not justify carrying fictitious inventory across a subsequent town drain.

**Reproduced counterexample.** With the default wool table, inventory 10,059 is at the floor. Selling 20 units leaves actual inventory at 10,059; a subsequent 12-unit drain gives 10,047 and a 72-coin quote. The allocator instead carries 10,067 and quotes 1. This can favor premature release or suppress a later allocation.

**When and cost.** Requires a floor-reaching earlier lot and recovery before another lot that day. [MELONAUDIT1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-27-melonaudit1.md:66) reports substantial cheap sales—28 wool, 17 strawberry, 12 milk units/game—but does not count this intersection. I budget **0–100/game**, representing a few affected marginal units at tens of coins; there is no evidence for a thousand-coin repair.

**Exact proposed edit.** Add `FLOOR_IMPACT_ON = False` to `core/sell.py`. At the start of `adjusted_marginals`, dispatch to a new helper only when enabled; leave the existing body unchanged. The helper must:

- Replay lots chronologically, applying the difference between consecutive `inv_lots` rows between sales.
- Advance inventory by `min(quantity, max(0, floor_start − inventory))`, using the actual price table’s first floor inventory.
- Compute each candidate’s marginal as total replayed sale revenue with one extra unit in that lot minus baseline revenue, then subtract its timing pressure. Correcting `before` alone leaves the externality calculation wrong.

**Closure and risk.** [SELLAUDIT1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-26-sellaudit1.md) correctly rejected cross-day holding: even its floor-correct oracle lost heavily when cash and V56 reacted. That closure stands; it did not establish that this allocator arithmetic was correct. Correct arithmetic can still change early cash, rival prices and production adversely. This fix also sits inside repeated allocation rounds, so dawn wall time is a material risk.

**2. Runtime overflow projections replay stale tiles**

**Mechanism.** `_project` reads `tiles = farm['tiles']` at `overflow.py:202`; `_trace` does the same at `:410`. Neither updates tile yield when future WATER/FERTILIZE executes, while later HARVEST reads the observation’s original `yield_units`. Separately, `:252` and `:450` classify animal PLACE by whether the coordinate is outside shed access, whereas actual placement gives a compatible empty structure priority even on a center access tile.

**Reproduced counterexamples.**

- Fertilized wheat, age three, observed yield three; WATER followed by HARVEST: both guards project **three**, while the engine actions produce **five**.
- Sheep cargo at `(4,4)` over an empty pasture; PLACE SHEEP: the guards project a sheep deposited in the shed. The engine places it in the pasture.

The V1 guard already handles the second distinction correctly at `overflow.py:162`; V2/V3 do not.

**When and cost.** These routines run after h10 on nonterminal days. The water error can hide impending overflow until a return trip is no longer feasible; the placement error invents shed occupancy and can provoke unnecessary rescue. [OVERFLOW4](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-22-overflow4.md:32) measured residual destruction of 1.15–1.26 units/game after V3, concentrated around d14 and d26–28. That supports a **0–60/game** investigation budget, not attribution of all residual destruction to this bug.

**Exact proposed edit.** Add `PROJECT_TILE_STATE_ON = False` to `agent/overflow.py`. In both replayers, the enabled branch copies tile dictionaries and applies legal WATER/FERTILIZE effects before subsequent HARVEST; use the same structure-first animal-placement predicate already present at `:162`, updating the projected structure when placement succeeds. Keep the original replay bodies as the OFF branches. This narrow patch fixes the reproduced discrepancies; it should not be described as a complete engine replacement.

**Closure and risk.** OVERFLOW4’s measured shipping benefit remains valid. Its description of replayed crop yields does not cover these counterexamples. More accurate projections can trigger additional sales and diversions, changing shared prices and displacing work; repair finding 4 before enabling this one. Extra tile copying and transitions require wall-time measurement, particularly because V3 replays several times.

**3. Final-turn overflow protection preserves the wrong product**

**Mechanism.** The DROP protection chooses the first carried product in **ascending marginal value** order and replaces DROP with a single-product PLACE. That policy ordinarily preserves expensive cargo for later, but at d29 h22 there is no later opportunity: the retry inserted at h23 never executes. The planner explicitly documents the final executed turn at `plan.py:996`, and `sim/rollout.py:632` runs the final day without h23 or EOD.

**Reproduced counterexample.** At final h22, shed contains 90 carrots; cargo insertion order is ten wool followed by ten wheat; the final market row sells these products. Original DROP admits the wool into the ten free spaces. The guard instead emits PLACE for wheat and strands all wool. At ordinary opening quotes, this can cost roughly **1.5k per occurrence**, not per game.

**When and cost.** One possible hour/game, requiring overflow and mixed cargo. Older [CREWAUDIT1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-27-crewaudit1.md:63) found 103 coins/game of terminal residue in near misses, but [MELONAUDIT1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-27-melonaudit1.md:34) found only 15 coins in hands and zero in the shed in its losses. I therefore estimate **0–20/game** on the newer body; the older 103 is not an attributable saving.

**Exact proposed edit.** Add `TERMINAL_DEPOSIT_VALUE_ON = False` in `overflow.py`. Inside the overflowing-DROP branch, only for d29 h22, compare projected final sale revenue from:

- The unchanged DROP, simulated in actual cargo insertion order.
- Each feasible single-product PLACE.

Choose the best, account for existing shed stock and remaining room in engine unit order, and ensure the corresponding final SELL quantities cover accepted stock. Comparing against unchanged DROP matters: it can admit a more valuable mixture than any single PLACE.

**Closure and risk.** This is not another terminal liquidation-row proposal; ENDROUTE is already enabled. The guard changes what reaches that row. There is no additional crew demand, but simultaneous rival sales can change the price ranking; use the existing quote machinery and test both seats.

**4. Mandatory water after a future planting can be deleted**

**Mechanism.** `_job_cost` receives the observation’s tile and a list of retained preceding operations. For a currently empty tile, its early return prices WATER at zero **before consulting the retained PLANT**. The later protections at `overflow.py:493` and `:519` therefore never run for this case.

**Reproduced counterexample.** At d14 h10, a unit on an empty center tile carries 110 wheat; the remaining plan plants wheat at h22 and waters at h23. V3 retains PLANT and replaces WATER with a ten-wheat deposit/sale, recording zero displaced job cost. A newly planted crop starts with dry counter one and dies at that night’s refresh without water.

**When and cost.** Requires projected overflow, a tile currently represented by `None`, and a diversion that preserves planting but removes its water. The observed historical planting-night deaths were two in 16 games, valued at 19 coins/game in [CREWAUDIT1b](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-27-crewaudit1.md:204). Those deaths have not been traced to this branch; **0–20/game** is a reasonable provisional scale if this explains a subset.

**Exact proposed edit.** Add `PROTECT_PLANT_WATER_ON = False` in `overflow.py`. Immediately before the non-dictionary return at `:473`, insert:

```python
if PROTECT_PLANT_WATER_ON and op == O.OP_WATER and O.OP_PLANT in before:
    return _INF
```

The OFF path remains unchanged.

**Closure and risk.** [OVERFLOW4:21–27](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-22-overflow4.md:21) claims newborn watering is protected; its tests missed a tile that is empty **now** but planted before the displaced water. CREWAUDIT1b’s broad “execute it every time” conclusion also exceeds its own two recorded deaths. The fix can sacrifice overflow recovery to preserve a crop, but it adds negligible wall time and no new planting demand.

**The three complaints: roots and closures**

| Complaint | Root supported by this review | What the prior closure establishes—and does not |
|---|---|---|
| **Empty tiles** | The established upstream cause is `brain.py:1177–1178`: fractional development followed by flooring; distance-ranked placement leaves corners last. Finding 4 is an additional, small execution defect, not the explanation for 125.6 empty tile-days. | [GAPFIX1:14–21](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-26-gapfix1.md:14) attributed 84/103 empty tile-days to the ask, with essentially none to seeds or routing. Its failed fills establish poor economics for those interventions. “It is not the planner” and “at any dose” at `:68–71` overgeneralize those trials. |
| **Lazy crew** | The scoped runtime executes a dawn plan without a general live work-admission pass: `runtime.py:945`, `:1010`; neural dispatchers are disabled. Available work therefore need not become scheduled work. Guard tail rewrites can additionally remove work, including the concrete dependency failure in finding 4. | [Idle census](/mnt/e/_work/kaggriculture3/S/idleops/report.md) distinguishes 232 underfoot jobs done later from 95 never done. “Work exists” is not a measurement of marginal profitable work. [CREWAUDIT1:157](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-27-crewaudit1.md:157) cannot close all scheduling opportunity from a small allocated hire-cost difference. |
| **Router** | The measured remaining issue is packing the admitted work within the available search time; this review does not independently establish its internal algorithmic cause. Findings 2–4 can damage the routed result afterward. | [ROUTERAUDIT1:30](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-26-routeraudit1.md:30) leaves **722/game** oracle bill headroom on its five-board comparison, or **592** for rr150 there. These are residual savings, not the already-earned 2,101. The oracle’s timing makes this an open constrained problem, not a ready shipping gain. |

Any empty-tile intervention must inspect the **final** ask: the residual rewrites the macro at `plan.py:12116`, and ESWORK applies another floor at `:12136`. Changing only `brain.n_dev` does not establish the resulting planting request. I found no basis to recommend another blanket fill or more hires.

**PASS, animal, fertilizer and market audit conclusions**

- **Active PASS creation:** ordinary route padding reaches `render.turn_action` unchanged; V1 clears tails at `overflow.py:130`, V2 at `:334`, V3 cuts at `:636` or clears after deposit at `:649`. A PASS there can coexist with legal work. Its value depends on lost production, capacity, future collection and sale—not legality alone.
- **CARE can be erased:** `_TAIL` includes CARE at `overflow.py:13`; V1 permits such tails, while `_project` excludes CARE from its “last productive” marker at `:224`. Thus a rescue can cancel care of an already-fed animal without charging its full future product value. This behavior was already an overflow tradeoff; I am **not reopening generic CARE completion**: the newest [brainstorm audit](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-astra-brainstorm8.md) measured only **+18/+10 margin** for completion.
- **No live exception-to-PASS handler found.** `runtime.py:972` uses `try/finally` to restore the temporary Q4 release; it does not catch planning exceptions. `render.py:28` maps unknown opcodes to PASS, but all defined live unit opcodes have mappings. Disabled ProgramEngine repair/fallback branches do not explain current idle counts.
- **Hiring:** `plan.py:10457` reserves the hire bill before purchases; `:13104` trims the HIRE row to the highest active hand index. Hands are hired daily. Multiplying all idle turns by a daily wage does not measure avoidable hiring cost.
- **Animal timing is internally consistent:** `sim/eod.py:124` escapes after two consecutive unfed nights; production is capped, the previous care bank is resolved, and today’s care is banked afterward. Consequently `valuation.py:87` starting care’s next eligible fire at `day+2` is correct.
- **Feed versus selling wheat:** `plan.py:10407–10449` values survival, cashable bank and additional care, subtracts already harvestable stock from continuation value, and compares against shed or purchase-curve wheat cost. FEEDKEEP/FEEDNIGHT failures remain valid evidence against feeding indiscriminately; absent feed is not automatically lost net profit.
- **Placement-night feed/care is already enabled**, via `PLACEFEED_ON=True` at `plan.py:7617` and its implementation at `:11514`. Recommending the old placement-night fix would duplicate shipped work. “PFSOFF” disables the kernel takeover; it does not disable PLACEFEED.
- **Fertilizer:** I found no new timing/index defect in its valuation, application or collection logic. The corrected recent audit reports complete watered-strawberry fertilizer coverage through d17 and completion gains of **−3/+8 margin** through d21. The earlier missing-fertilizer count was a snapshot-timing artifact; it is not a build candidate.
- **Sale timing:** `_lot_split` at `plan.py:6736` conserves product quantities, but `LOT_SPLIT_ON=False` at `:9132`; it is not a current trigger. The live allocator uses four lots. Terminal liquidation and h22 handling exist; finding 3 is a subsequent guard error.
- **Market fidelity:** `sim/market.py` resolves both seats’ supply, coupled orders, sell/buy crossings and floor advancement. The live planner’s `core/projector.py:192` is deliberately opponent-free with `OPP_SUPPLY_ON=False`; observed opponent features and learned policy responses do not make it an exact rival forecast. I found no justification for replacing it with an untested forecast under a “simulator bug” label.

**Parsing, state and inference checks**

`parse.py:55–87` correctly converts SERP tile IDs to `[y][x]` and reads fed/cared flags and pending care bank. `runtime.py:945–958` rebuilds by day and rotates dawn market history once per new day. I found no new observation-index or daily-history defect in the live path.

`KERNEL2_ON=True`, but `KERNEL2_FIRE_CASH="99999"` at `plan.py:15827` deliberately prevents takeover; `KERNEL2_NOOP_H0=False` preserves the PFS opening. This is an intentional inactive guard, not unexplained missing work.

None of `es/archetypes.py`, `es/tape_actions.py`, `es/tape_flow.py` or `es/train.py` runs in packaged inference. Learned weights, the residual’s NumPy inference function (`residual_head.py:406`), and `eswork_theta.npy` do. Simulator/tape training costs should not be counted against live action time.

Control identity needs care: this copy enables `REINVEST_DAILY="4:200:CSG"` and `FEED_ALL=True` at `plan.py:9453–9457`; the inspected vrp20 archive lacks those additions. The two named submissions must not be treated as one byte-identical baseline.

**Build TODAY: three small runtime repairs**

Build separately, default OFF; do not bundle the sale allocator rewrite into them.

| Build | Required local evidence | V56 judge bar | p48c judge bar | Production and runtime bar |
|---|---|---|---|---|
| **Finding 4: protect future planting water** | Counterexample preserves WATER; OFF plans/actions identical | Positive paired margin on v21 and m40; own coins ≥ control; no net win regression | Positive paired margin and own coins ≥ control on the fixed 80-game panel | d15–17 strawberry supply and d18–29 egg/milk/wool units each ≥ control; count prevented deaths |
| **Finding 3: terminal deposit value** | Compare DROP and PLACE alternatives; no h23 dependency; OFF identical | Same bar, with gains attributed to executed final deposits/sales | Same bar | Earlier production unchanged; terminal animal sales do not fall; no new timeout |
| **Finding 2: projected tile transitions** | WATER→HARVEST and center animal-placement checks match engine; finding 4 enabled in both compared arms | Same bar, with rescue/displacement ledger | Same bar | Strawberry and each late animal-product volume ≥ control; measure p99 and restored timeouts under the live clock |

These are small correctness candidates, not established large gains. If intervals remain inconclusive, retain OFF; a deterministic microcheck is not a shipping verdict.

Could not check: live trigger frequencies, causal coins, paired V56/p48c outcomes or wall-time changes; router internals belong to the other review scope.