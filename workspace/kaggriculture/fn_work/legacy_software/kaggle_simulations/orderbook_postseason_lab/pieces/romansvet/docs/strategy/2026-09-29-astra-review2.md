# ASTRA_REV2 (2026-09-29 17:18Z-17:35Z) — gpt-6-astra code review 2/3 of the shipped tree (master cf68f736): tiles, planting, seeds, land, asks

Coordinator: Claude Fable 5.1. Prompt: S/astra_rev2/prompt.md (common header S/astra_rev/common.md). Output verbatim below. Reviews 1 (router/crew) and 3 (decision/market/animals/guards) are separate docs.

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

#### YOUR SCOPE (review 2 of 3): TILES, PLANTING, SEEDS, LAND, ASKS in the day planner
Files: `core/plan.py` — `open_tiles` (1775), `_program_seed_room` (1637), `_lot_split` (6736), `_relay_fill` (7865), `_wheat_late_cap` (8018), `_fill_plant` (8051), `_fill_cap` (8118), `_ask_fill` (8151), `_plant_ask` (8187), `_place_split` (8237), `_seed_room` (8259), `_standing_yield` (8657), `_residual_seed_extra` (8820), `_mirror_wheat_ask` (8902), `_pf_wheat` (9245), `_rebuy_ask` (9300), `_eswork_macro` (9625), `_candidates` (9895), `_derive` (10133-13916: the day plan; read it fully), `_market` (15115), `_land_day_cfg` (15953) and the land purchase logic (grep -n "BUY_LAND\|buy_land\|land" core/plan.py | head -80); `core/brain.py` `decide` and the ask floor `n_dev = _qfloor(dev_frac * n_free)` (grep -n "_qfloor\|dev_frac\|plant_target\|n_free" core/brain.py core/plan.py). Questions to answer with code evidence: which floor, rounding, mask or ordering leaves the corner tiles (0,9)/(9,0)/(0,0) and the outer ring unplanted while the centre is full (is it the tile ranking by distance to the shed, a reach/land_reach cap, an ask count that is < n_free by construction, or the router dropping the farthest stops)? why does replanting stop d19-25 with 61k cash and 0 seeds (seed purchase gated by what)? does the planner compute crop-tile capacity from the actual crew throughput or from a fixed constant, and where is that constant? are seeds/land bought at the hour the plan needs them or a day late? where does the plan ask for FEWER plantings than tiles free and why (cite the exact line and the value on a typical d12 / d20 board)? Are there dead switches or duplicated code paths in _derive that cost wall time?

## Astra's review (verbatim)

| Rank¹ | File:line in mastertree | Title | Fires | Estimated coins/game recoverable | Fix size |
|---|---|---|---|---|---|
| 2 | [core/plan.py:9816](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/core/plan.py:9816) | **BUG: stored seeds do not consume ordinary planting capacity** | Dawn, when held seeds and an oversized ask compete for limited slots | **0–100**, low confidence; occurrence not measured | 2–4 lines |
| 4 | [core/plan.py:12460](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/core/plan.py:12460), [13072](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/core/plan.py:13072) | **BUG: unchanged relay and converged routes are recomputed** | Dawn; empty relay on d0–9/d28–29, and any successful admission round | **0 direct**; measured computation savings, unpriced timeout protection | 8–15 lines |
| 1 | [core/plan.py:11440](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/core/plan.py:11440) | Planting location ignores the cost of opening another tile visit | Dawn, when an already-requested planting can reuse a harvest visit | **About +100 hypothesis**, plausible −200 to +300 | 10–15 lines |
| 3 | [core/brain.py:1177](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/core/brain.py:1177), [core/plan.py:11399](/mnt/e/_work/kaggriculture3/S/astra_rev/mastertree/src/kagg3/core/plan.py:11399) | **ROOT: fractional development demand repeatedly excludes the same distant tiles** | Historically d3–20 rounding; larger omissions d20–27 | **No established positive net recovery from another floor**; historical tested fills approximately −200 to +200 own coins | 10–20 lines for a mechanical floor |

¹Confirmed bugs appear first; rank orders estimated recoverable coins. Estimates are not paired-judge results and must not be added together.

**Scope and configuration matter.** I read the requested planner span, helpers, brain decode, and relevant audits. No files were changed, no pytest was run, and no simulator was run; checks used helper calls and two existing dawn fixtures.

The copied tree’s defaults are `REINVEST_DAILY="4:200:CSG"` and `FEED_ALL=True`, matching the CLSEARCH candidate rather than the original PFS control. [CLSEARCH1’s package comparison](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-clsearch1.md:30) explicitly identifies those differences. Its actual ESWORK array rounds to relay **2/5/3/3**, with **EST_LEAD still 5**; the adjacent comment claiming 2/4/2/3 and lead 3 is stale. The checked `submission/residual_head.npz` is **v1**: its `ask_fill` and `seed_buy` channels do not exist.

**B1 — Stored seed is missing from the ordinary capacity ledger.**

- **Mechanism.** `_wants` subtracts held seeds from purchase demand, then clips those purchases against the entire `seed_cap`. The subtraction of held seeds from capacity exists at lines 9816–9819, but only under `PROGRAM_ENGINE_ON and PROGRAM_PLANT_SHARE`; that path is disabled. Consequently, held seeds plus purchased seeds can exceed the planting slots, and crop-order placement at lines 11440–11448 leaves some purchased seed unused.
- **Reproduction.** Calling the copied `_wants` with one free slot, no animal demand, target `[1 wheat, 1 carrot]`, and one stored wheat seed returns a purchase request for **one carrot seed**. The wheat already occupies the only available planting slot under the ordinary placement order.
- **When.** Any dawn with held seed, insufficient slots for the complete target, and a positive budget grant for the excess purchase. Residual increases and a predicted-but-refused land purchase can create oversized targets. This review established the mechanism, **not its frequency in vrp20/21 games**.
- **Coins.** Estimate **0–100/game**, not a demonstrated loss. One stranded carrot costs 20 immediately; tomato/strawberry cost 50/100, but seed subsequently planted is delayed capital rather than a permanent loss. The latest crew ledger’s small dusk-seed totals argue against a large season-wide leak.
- **Minimal edit.** Add `SEED_STOCK_ROOM_ON = False`. Change the condition at line 9816 to `(PROGRAM_ENGINE_ON and PROGRAM_PLANT_SHARE) or SEED_STOCK_ROOM_ON`, retaining the existing subtraction and ordinary crop-order allocation. OFF takes exactly the current branch; do not enable programme-wide proportional splitting.
- **Risks.** Using existing stock first can change the crop bought under scarcity and the allocation of saved cash to animals or fertilizer. This must be judged on both purses. The v1 head avoids the separate wide-head top-up path; a future wide head would need the same capacity constraint in `_residual_seed_extra`.
- **Prior closure.** This correction already exists for the programme path, but was not applied to the ordinary planner. GAPFIX1’s zero seed-purse attribution does not refute an **overpurchase** bug, and this bug does not explain its zero-stock corner holes.

**B2 — The planner spends wall time repeating unchanged work.**

- **Mechanism.** With ESWORK enabled, final `_derive` creates a relay array even when every entry is false. Line 12460 tests `d.relay is not None`, so it executes the crew adjustment and another full `_derive` when the relay adds no work or hands. Separately, admission performs all three `_routes` calls even after `missed == 0`; the ordinary branch then leaves `n_admit` unchanged, making subsequent rounds identical.
- **When.** The empty-relay case is guaranteed outside d10–27 under the current relay calendar: **12 dawns/game**, plus possible zero-room days. Converged routing can repeat on any dawn; both checked fixtures converged on their first round.
- **Evidence.** Day 0 made four `_derive` calls, including its forward pass; the final two prefixes were equal. Day 22 made three derivations and legitimately changed the final prefix because the relay added hands. Both routed the same admitted count three times: 25 and 70 respectively.
- **Measured shortcut.** An in-memory version skipping an empty relay re-derivation and stopping converged ordinary routing produced **byte-identical six plan arrays and identical stats** on both fixtures. Local timings were **238.1→131.9 ms** on d0 and **180.5→134.2 ms** on d22. These are small local checks, not p99 or Kaggle measurements.
- **Coins.** **Zero direct** when execution completes normally. Avoiding timeouts or funding deeper router search could earn coins, but this review cannot assign that recovery. ROUTERAUDIT1’s approximately 100–150 coins per late fallback day is a conditional exposure, not a measured gain from this edit.
- **Minimal edit.** Add `PLAN_FASTPATH_ON = False`. On NumPy only, skip the relay adjustment block when `not np.any(d.relay & d.task)`; after line 13072, break the ordinary admission loop when `missed == 0`. Keep the programme’s seven-round search and all JAX control flow unchanged. OFF must bypass both shortcuts.
- **Risks.** Retain re-derivation whenever the relay changes the hire bill. Do not apply the convergence shortcut to programme binary search. A larger router budget is a separate behavioral candidate; the first patch should spend less time producing the same plan.
- **Other dead work.** `_residual_override` unconditionally builds `program_selector_features` at line 8776, although the checked v1 `numpy_fn` ignores `macro_fields`. That includes another legacy feature calculation and both `_standing_yield` reductions. This is smaller unmeasured overhead; thousands of default-OFF branches and comments are not themselves evidence of a substantial runtime cost.

**P1 — The empty-tile root is the ask; distance ranking makes the omissions persistent.**

The causal chain is explicit:

1. `brain.n_free_slots`, lines 179–196, counts empty/weed tiles, harvestable one-shot crops, and enabled final-slot reuse; prospective land is added when `land_ok` predicts a purchase.
2. At brain lines 1177–1178, `dev_frac = sigmoid(head[5] + aux[2] * n_free / 25)` and `n_dev = _qfloor(dev_frac * n_free)`.
3. At brain line 1215, animal acquisitions consume part of `n_dev`; the remaining crop total is split by largest remainder at line 1320.
4. After residual changes and optional overrides, purchases are bounded by that target. `plant_eff = min(fill_target, seeds + seed_buy)` at plan line 11339 cannot invent demand.
5. `_dev_key` and `_rank_near`, lines 7127–7165, rank free tiles by bucketed shed distance and then serpentine index. Placement takes a prefix at lines 11399 and 11448.

**This is not an explicit `n_free - 1` rule.** A sigmoid below one followed by floor commonly produces that result; `_qfloor`’s small numerical tolerance only rescues products very close to an integer. When development fractions fall further, the omission grows beyond one tile.

The far corners share the maximum shed distance, while serpentine ties favor the earlier indices. `(0,9)` is the last serpentine position, so persistent under-demand repeatedly excludes it; `(9,0)` and `(0,0)` lose less often. `compact` is an ordering, **not a radius mask**. `land_reach` values prospective land; it is not an outer-ring planting prohibition.

**Concrete historical dawn values**, read directly from `S/empty1/trace_0.jsonl`:

| Dawn | Board | Brain free slots | Crop ask | Pre-/post-VRP plantings | Dawn seeds |
|---|---:|---:|---:|---:|---:|
| d12 | 0 | 11 | 9 | 9 / 9 | 0 |
| d20 | 0 | 10 | 8 | 8 / 8 | 0 |
| d12 | five-board mean | 8.8 | 6.8 | 6.6 / 6.6 | 0 |
| d20 | five-board mean | 12.0 | 8.6 | 8.2 / 8.2 | 0 |

These are older baseline observations, not measurements of today’s ESWORK/reinvestment configuration. GAPFIX1’s separately traced live game had d12 **5→4**, and d21–27 asks **9/8/7/8/9/10/8** against free counts **15/14/13/15/22/31/32**. Its placement and VRP stages did not remove those missing asks. [GAPFIX1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-26-gapfix1.md:9)

- **When.** GAPFIX1 attributed 17 empty tile-days to rounding and 67 to the late share rule in one game. GAPCENSUS2’s broader proxy attributed **51.5 late-ask tile-days/game** across 104 games. The current ESWORK relay partly compensates; those historical frequencies cannot be assumed unchanged.
- **Coins.** The empty area is gross production opportunity, not established lost profit. GAPFIX1 recovered only **+116/+194 own coins** with rounding fills, while full late fills returned **−201/−182** and increased wages/displaced other products. I cannot substantiate a positive current net value for an additional unconditional floor.
- **Minimal mechanical fix.** Add `ASK_ROUND_REPAIR_ON=False`. After the final macro overrides, calculate developable slots with the shared slot predicate; where total crop-plus-animal demand is exactly one below that count, add one wheat seed request if it can mature, otherwise carrot if it can mature. Keep the day window explicit and run it before both `_derive` passes. OFF preserves the original macro. **This is a comparator reproducing an already-tested intervention, not a new shipping recommendation.**
- **What goes wrong.** More plants create future water/harvest work and can buy expensive marginal hands. They also move shared prices and displace animal output. The mechanical floor fixes occupancy without establishing profitability.
- **Incorrect closure.** GAPFIX1’s conclusion “It is not the planner” contradicts its own causal attribution: the planner sets the missing demand. Its trials justify rejecting those floors on that configuration, not closing every joint demand/capacity change. ESWORKCHK1 subsequently measured a combined relay/lead candidate at **+637 own coins** on its held set, although every held flip was in the training curriculum; that supports conditional interaction, not a current ship claim. [GAPFIX1 verdict](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-26-gapfix1.md:63), [ESWORKCHK1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-26-esworkchk1.md:1)

**P2 — Use an existing harvest visit before opening another planting visit, at unchanged demand.**

- **Mechanism.** `slot_rank` uses shed distance without distinguishing a tile already owed a HARVEST from an empty tile requiring a separate visit. Consequently, the planner can plant a nearer empty tile while harvesting and abandoning another tile that was already in today’s work. Combining HARVEST→PLANT→WATER on the latter can save a visit without adding a planting, changing the seed mix, or raising the ask.
- **When.** At dawn whenever funded planting demand is smaller than the available slots and the distance-selected planting set omits a one-shot harvest tile. The precise current frequency is unmeasured. SLIVER1 establishes that un-replanted harvest stops exist, but its approximately six **additional** same-tile fills/game are not a measurement of this substitution opportunity.
- **Coins.** Working hypothesis **about +100/game**, plausible **−200 to +300**. Ten to twenty-five substitutions saving a few movement turns each could occasionally remove a late marginal hire; most saved turns may simply become PASS. A farther replacement location can also increase subsequent tending travel, hence the negative side of the range.
- **Minimal edit.** Add `PLANT_REUSE_RANK_ON=False`, initially restricted to **d20–25**. Immediately before line 11440, leave structure selection unchanged and replace only the planting rank:

```python
if PLANT_REUSE_RANK_ON:
    slots = free_slot & ~build_here
    reuse = harvest_one & slots
    key = dev_key + (DIST_MAX + 1) * (~reuse).astype(i32)
    reuse_rank = xp.where(slots, _rank_by(xp, slots, -key), -1).astype(i32)
    plant_rank = xp.where((day >= 20) & (day <= 25),
                          reuse_rank, slot_rank - n_build).astype(i32)
else:
    plant_rank = slot_rank - n_build
```

Continue through the existing `p_cum` and placement masks. Use `_rank_by`, **not `_rank_near`**: the latter only enumerates buckets 0–`DIST_MAX`, so feeding it the enlarged key would produce wrong ranks.

- **Risks.** Longer harvest chains can move deposits past sale deadlines; concentrating operations can worsen route packing. Farther replants may require more movement over their remaining lives. Daily funded crop counts stay fixed, but execution and later shared prices can still change.
- **Prior closure.** SLIVER1 and ROUTEFILL1 tested adding plantings and their subsequent workload. This changes **which tiles receive the existing plantings**. Their rejection remains valid, but does not test this intervention. It will not itself eliminate the occupancy deficit: it is a way to lower the cost of the current demand before considering more demand.

**Answers on seeds, land, and capacity.**

- **Why 61k cash and zero seeds?** Seed stock follows the ask. `_wants` at line 9798 requests `max(plant_target - seeds, 0)`; physical capacity and the shared budget then clip that request. The ordinary path has no “cash is abundant, buy seed for every remaining tile” rule. Replanting does not stop globally on d19–25: it continues at a restricted daily quantity while empty slots accumulate.
- **Maturity is not the broad late stop.** Brain lines 1265–1267 permit wheat/carrot through d27 under `pay_day=29`; tomato through d21. `_candidates` uses horizon-truncated `new_plant_units`. LATEPLANT1 measured only **16 coins/game** of doomed seed waste, so its narrow closure remains supported; cutting all partial late crops would remove useful output.
- **No single fixed crop-tile ceiling exists.** Physical capacity is free slots minus potential animal builds in `_seed_room`. The development quota comes from the network. Hiring/admission then use approximate throughput: **`EST_MOVES=1`**, **`EST_LEAD=5`**, and pickup deductions, at lines 150, 172, 12233 and 12936.
- **Land has a separate heuristic.** `land_reach`, lines 5884–5914, uses `LAND_PICKUPS=3`, `DEV_DAYS=2`, and **two operations plus one estimated move per new tile**. Existing work is charged as one operation plus one move per worked tile, even where a tile has several operations. This is not an exact crew-throughput calculation.
- **The shipped relay also uses a constant.** Lines 12464–12467 charge current relay chains plus estimated movement against **`ESWORK_RELAY_OPH=12`**, capped at three added hands. It does not measure the current VRP’s spare capacity or the complete future tending schedule. The alternative `_relay_fill`/`_wheat_late_cap` estimators are disabled by default.
- **Purchases are not generally one day late.** `_market` buys seeds at **h1**, making them available for later unit turns. BUY_LAND is emitted at **h3**, line 15720; prospective tiles enter that day’s free-slot mask at line 11015, and `land_lead` prevents work before **h4**. Purchase-day holes therefore do not imply delayed unlocking or seed delivery.
- **Land prediction is approximate.** Brain `land_ok` requires the full land price at dawn, while `_derive` can count discounted first-lot revenue. That admits a possible underprediction, but all ten land purchases in the inspected historical trace were anticipated. It is not established as this complaint’s root, and LAND1’s failed early-land intervention should not be reopened without new evidence.
- **Helper names can mislead.** `open_tiles()` controls an optional opening melon allocation; it does not enumerate empty tiles. `_program_seed_room` serves the disabled programme path. `_fill_plant`, `_ask_fill`, `_plant_ask`, `_mirror_wheat_ask`, and `_rebuy_ask` are not unconditional recovery mechanisms.

**The three complaints and the prior closures.**

- **EMPTY TILES — root established:** P1’s fractional ask, followed by persistent distance/serpentine selection. Seeds, reach masks, and router drops are not the demonstrated cause of the historical corner pattern. Rejecting prior fills was justified; declaring the planner/ask axis universally closed was not.
- **LAZY CREW — no complete root established within this scope:** under-requested development contributes to a short task list, while approximate admission and fixed schedules can strand capacity. The `work@dist0` count is not a count of distinct profitable missed operations: IDLEOPS reports 232 underfoot-work idle turns whose work was done later that day. Conversely, CREWLOSS1 counts a day as labour-bound only if a work sign exists **and the whole day has zero idle turns**; one compulsory dawn wait excludes it. Its “zero labour-bound days” therefore cannot prove scheduling has no cost. The failed bigger-crew experiments remain valid. [Audit predicate](/mnt/e/_work/kaggriculture3/S/crewloss1/extra.py:35)
- **ROUTER — this review establishes a wall-time contributor, not the assignment root:** B2 wastes time before routing improvements can be used; P2 changes the task geography presented to the router. ROUTERAUDIT1’s within-hand TSP comparison concerns a fixed task set and cannot bound gains from changing planting locations or demand. Its assignment/search-depth diagnosis belongs to the router review; the measured finite-time savings remain useful, but do not prove a general planner-plus-router ceiling.

**The three findings to build TODAY — candidates for judging, not shipment.**

| Build | Margin versus reacting V56 | Margin versus p48c | Our own coins | Strawberry wall | Late animal units |
|---|---|---|---|---|---|
| **B2: NumPy computation shortcuts** | Unlimited-clock actions and margins **exactly equal**; live-clock margin nonnegative | Same equality requirement | Exactly equal without deadline effects | Exact d15–17 equality | Exact per-product equality |
| **B1: stock-aware seed capacity** | Positive paired Δmargin on m40; no v21 margin regression | Positive paired Δmargin on m40×2 | Nonnegative on both rivals | No reduction in d15–17 sales | No reduction in d18–29 milk, wool, egg or fertilizer units |
| **P2: unchanged-count harvest reuse, d20–25** | Target **≥+200 Δmargin**, paired t≥2 on m40; v21 Δmargin≥0 | Target **≥+200 Δmargin**, paired t≥2 on m40×2 | Nonnegative on both rivals | Exact equality before d20 | No reduction in any of the four late animal books |

For behavioral candidates, retain the published V56 minimums **12/21 and 37/40 wins** as additional floors, require no net p48c win regression, and measure total-act p99 under the live deadline. Compare separately against the correct PFS and CLSEARCH configurations; do not pool their controls.

Could not check: current-game firing frequencies, closed-loop coin gains, or Kaggle p99; validation was limited to static review, historical ledger reads, helper reproduction, and two recorded dawn fixtures.