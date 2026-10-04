# ASTRA BRAINSTORM 1 — the untested way to the top 5
Date: 2026-09-29 11:53-11:59Z | Model: gpt-6-astra (reasoning high, read-only, ephemeral) | Prompt: S/astra_bs1/prompt.md | Dispatched by the orchestrator after the user re-enabled codex astra for brainstorming (11:50Z).

**Put the remaining effort into reconstructing P48’s executable cash flow. One measurement feeding the “unfundable programme” conclusion is wrong: real P48 earns 14.6k through d9, not 11.3k.** This does not establish a winning body, but it changes what the port must reproduce.

I found one remaining approach with plausible scale for the **+15.9k requirement**, plus four narrower execution experiments. I found no completed tests of the exact changes below; several have tested predecessors.

**1. The incomplete invariant: #6, animal COUNT explains the opening**

Animal count explains production, but **the timing of collection, deposit, sale and reinvestment explains how that count becomes affordable**. A dawn target schedule loses these dependencies.

I compared the completed **56 P48 seats** in the in-flight [PORTGAP ledger](/mnt/e/_work/kaggriculture3/S/portgap1/res/led.jsonl) with the same seats in TOPAUDIT1:

| d0–9 revenue | Exact transition ledger | TOPAUDIT net-flow estimate | Difference |
|---|---:|---:|---:|
| Wool | 5,316 | 3,460 | +1,856 |
| Fertilizer | 6,392 | 4,864 | +1,528 |
| Milk | 2,186 | 2,270 | −84 |
| Wheat | 713 | 702 | +10 |
| **Total** | **14,606** | **≈11,296** | **≈+3,310** |

The exact ledger reports **zero cash-mismatch turns in all 56 seats**.

The defect is in [fpt.py](/mnt/e/_work/kaggriculture3/S/topaudit1/fpt.py): its inventory identity adds crop harvests but omits animal harvests and fertilizer collections. Selling six wool while another worker harvests six can therefore register zero sold. Multiplying by the pre-step quote introduces another, smaller approximation.

**Cheapest decisive read:** finish PORTGAP’s exact transition ledger, then compare the port and teacher **before each successful animal/land purchase**, recording available cash, carried stock, deposited stock and preceding fills. No new full games are required. The missing variable is “cash available when the purchase can still be placed today,” not daily gross revenue.

This challenges the funding explanation, **not** PFS’s measured d0 zero-slack result or the rejection of the tested plates.

**2. Five untested changes**

All coin numbers below are **subjective planning expectations**, not measured gains. `P(pass)` means passing the complete candidate gate before the deadline, not reaching top five. Their gains overlap and must not be added.

For every survivor: an **80-game paired screen**, followed by **152 untouched held-out games**, own ≥+2k with t≥3 and margin≥0; then flood own≥0 and faithful-tape W not lower. Use board-level uncertainty where seat duplicates are symmetric. The stale clone can reject changes; passing it cannot establish transfer to P48/PQ4. Preserve the V result through a paired V56 check.

**A. Compile P48’s action dependencies into a reacting controller**

- **Mechanism:** reconstruct a coherent P48 policy as resource-dependent tasks—collect → deposit → sell → purchase → place—with live affordability and inventory checks.
- **Expected Δown / Δrival:** **+6k / +1k**, with implementation outcomes plausibly spanning −20k to +20k own. The upside comes from recovering the funded opening and d10 wave together, rather than buying the wave by cutting PFS’s herd.
- **Exact test:** `P48_TASKGRAPH={funding_only,full}`; choose one coherent P48 lineage, not median actions across teams. First reproduce 12 existing teacher trajectories through d10, explaining every failed dependency. Then run each controller against reacting PFS and V56 on 40 boards. Require d9 herd within ±2, productive tiles within ±4 and first melon sale within ±3 steps of matched teacher trajectories before full evaluation. Add the PQ4 branch only after P48 works.
- **P(pass): 10%.** The financial sequence is observable; reconstructing routing, branches and the entire late body within 30 hours remains the largest risk.
- **Difference:** PROGRAMME1 copied daily targets into PFS’s executor; BC learned individual actions without the plan. This reconstructs the dependencies that make the targets executable. A repaired fixed tape alone does **not** qualify.

**B. Sell PFS’s first fertilizer on d1**

- **Mechanism:** keep d0 unchanged, but collect, bank and sell d1 fertilizer before the next investment decision instead of waiting for overnight banking.
- **Expected Δown / Δrival:** **+1.5k / −0.3k**. Roughly six units at ≈100 release ≈600 coins one day earlier; final gain must come from earlier productive investment, not counting those 600 twice.
- **Exact test:** `FERT_PAYDAY_D1={h8,h12}` with at most one additional cheap hand; preserve every baseline feed, care and crop task. First verify that ≥400 spendable coins arrive early enough to buy **and place** an animal without displacing existing commitments. Then 80 paired games per cell.
- **P(pass): 15%.** The liquidity exists; a profitable feasible destination for it is unproven.
- **Difference:** FERT_DUMP changed fertilizer allocation from d5. This changes **transport and availability on d1**, keeping applications and d0 composition fixed. It also precedes LUMP9’s d8 milk intervention.

**C. Execute purchases after actual fills within the day**

- **Mechanism:** admit a previously unfunded development task immediately after a sale clears, instead of waiting for tomorrow’s dawn plan.
- **Expected Δown / Δrival:** **+1k / 0**. Earlier placement produces extra animal-days or crop-days; no new product-price assumption is needed.
- **Exact test:** `POST_FILL_EXEC={animals,animals+seeds}`, restricted initially to **d2–7**. Reserve all remaining baseline expenses and feed first; require a complete pickup/build/place route before submitting the purchase. Grid maximum **one/two additional completed tasks per day**. Reject any cell that merely accumulates purchased stock.
- **P(pass): 8%.** It may discover that every useful surplus is already committed.
- **Difference:** REINVEST_DAILY changes dawn priority and crowds out cows/seeds. This spends only verified residual cash after actual fills and proves same-day execution. It excludes the in-flight d8 milk change.

**D. Minimize maintenance cost while preserving the production schedule**

- **Mechanism:** solve each animal’s short feed/care calendar exactly, removing actions only when survival and all baseline production quantities/dates remain unchanged.
- **Expected Δown / Δrival:** **+0.4k / 0** before any reinvestment effect. Savings come from wheat and occasionally wages, with unchanged sale volume.
- **Exact test:** `MAINT_CALENDAR={through_first_yield,rolling_6days}`. State includes consecutive-unfed count, pending bonus, held yield, next production and planned harvest. First run the counterfactual over existing replays; stop if realizable savings before d8 are <300/game and total savings <1k. Only then run 80 paired games.
- **P(pass): 2%.** PFS already skips several economically redundant feeds; remaining headroom may be zero.
- **Difference:** FEED_ALL adds feeds; CARE_HOLD/FEED_FORWARD alter valuation gates. This searches for an **identical-output, lower-cost schedule**, rather than buying more output or preserving otherwise unprofitable animals.

**E. Complete FEEDROOM’s unbuilt purchase-and-pickup half**

- **Mechanism:** after a sale frees shed space, buy missing survival wheat and route its pickup before the animal’s second unfed night.
- **Expected Δown / Δrival:** **+0.3k / −0.1k**, consistent with the existing +0.1–0.4k average bound; individual tail games can move several thousand.
- **Exact test:** `POST_SALE_FEED={survival_only,baseline_feed_completion}`, triggered only by a recorded shed-room clip. Recount prevalence on current MELON losses first; stop below **0.2 preventable escapes/game**. Otherwise run 80 paired games, including every triggering board.
- **P(pass): 2%.** Frequency, rather than efficacy on a triggering game, probably kills it.
- **Difference:** [FEEDROOM1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-27-feedroom1.md) tested feed reordering. Its post-sale wheat purchase plus router pickup was explicitly left unbuilt.

**A is the only top-five-scale proposal. B–E are bounded experiments, not four additional stories for a 15.9k gain.**

**3. What PQ4 should change next**

I would expect PQ4 to optimize **whether and how it fills Q4**, conditional on visible shops and the opponent’s committed production—not enlarge its opening melon plate.

The pooled Q4 comparison is approximately **−7.3k by d15, +7.5k afterward**, only +0.4k net. Meanwhile, mirror wins derive about **3.4k from d15–29**, including strawberry +1.2k, eggs +0.7k and carrot +0.5k. That makes conditional Q4 expenditure and its crop allocation the next experiment with relevant scale. This is an inference, not observed unpublished development. [TOPAUDIT1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-topaudit1.md)

**Opening for us: none bankable today.** A shift toward strawberry/eggs/carrot could leave more tomato demand, but unconditional tomato expansion already failed. An opening would require observing PQ4 actually reduce committed tomato supply and then pricing an incremental response. If PQ4 simply avoids its losing Q4 expenditures, our opposition improves.

**4. The concrete cash source the ports miss**

The strongest answer is **early fertilizer liquidity followed by same-day first wool liquidation**, not wheat arbitrage.

Across the exact 56-seat P48 ledger:

| Day | Sale | Units | Mean realized price | Revenue |
|---|---|---:|---:|---:|
| d1 | Fertilizer | 5.0 | 99.2 | 496 |
| d2 | Fertilizer | 5.0 | 97.2 | 486 |
| d6 | Wool | 18.0 | 196.3 | 3,533 |
| d8 | Milk | 12.0 | 182.1 | 2,186 |
| d9 | Wool | 12.1 | 146.8 | 1,782 |

The **d6 wool sale** is the main lump financing expansion; the **d1–4 fertilizer stream** finances reaching it.

A concrete cached example, episode **115010875, seat 1**:

- **d2 h8:** cash 480; two fertilizer sales yield 193; a 400-coin cow purchase leaves **273**.
- **d6 h3:** cash 144; six wool yield **1,271**; Q2 costs 1,000; cash ends **415**. The action simultaneously drops the wool and another worker harvests more wool—exactly the situation the net-flow estimator mishandles.

Verify from [the replay](/mnt/e/_work/kaggriculture3/S/topaudit1/cache/rp/115010875.json.gz) by replaying each transition from its recorded pre-state and logging successful `_commit_unit` calls. Reconcile:

`post_money − pre_money = successful sales − successful purchases − hires − land`

Then compare the port’s **harvest → bank → sale → purchase → placement timestamps**. The evidence establishes the real funding sequence and the measurement omission; it does **not yet establish which dependency the port misses most**.

**5. Verdict**

**Concentrate the remaining compute on a cash-conserving, reacting P48 reconstruction, with exact transaction-and-task fidelity as the first gate.** Give it a six-hour checkpoint: reproduce the d1 fertilizer financing, d6 wool-funded Q2, d8 milk-funded Q3 and d9 build on recorded trajectories without subsidies or failed-order amnesia. If it cannot, stop that reconstruction before spending thousands of games scoring it. **Stop undifferentiated BC refresh/retraining and broad searches scored against the under-built clone**: they cannot presently distinguish a top-family improvement from exploiting missing rival production. Keep PFS in one slot; nothing here has earned the second slot or demonstrated the required +15.9k margin shift.

## Prompt

## ASTRA BRAINSTORM 1 (2026-09-29 ~11:55Z) — find the untested way to the top 5

You are an independent strategist. Repo: /mnt/e/_work/kaggriculture3 (read-only). Kaggle "kaggriculture" (30-day farm sim, 2 seats, shared market: price = f(shared inventory) per product; melon/fertilizer/wool never recover in-game so the first seller takes the rent; only WHEAT and FERTILIZER can be bought; shops unlock on days 2,5,...,23 by a hidden-seeded random draw; town center absorbs 1 unit/product/24 turns; animals escape after 2 unfed days). Final ranking = Bradley-Terry over Oct 1-15 games of our LAST 2 uploads (deadline 2026-09-30 21:00Z safe). Our body PFS (vrp20) sits ~2,430-2,460; top 10 ≈ 2,860-3,055. Requirement (not a forecast): vs rivals 2,400-2,800 we need ~+15.9k mean margin per game (today ~0), i.e. flipping most of our losses to the MELON family (live 12-33) while keeping V (57-13).

### What today established (read these docs first; do not re-derive them)
- docs/strategy/2026-09-29-brainstorm1.md "Session summary" (six invariants: live gap −8.1k = fertilizer −5.2k + melon −4.3k + wool −4.2k + egg −1.0k; PFS d0 purse has ZERO SLACK (201 coins at dawn d1 = feed reserve, nine d0 bodies lost 10-22k); our late volume is our only denial tool; seats couple only via the 9 market books; PFS already sells late products at h17 post-drain; the programme's d0-9 lead = animal COUNT via daily reinvestment).
- 2026-09-29-topaudit1.md: the top 10 = ONE skeleton, TWO bodies: P48 (DSM's own code, 5 teams: 48 melons sold from d10 h6 @240 + 23 more d15-29, no Q4) and PQ4 (P48 + Q4 bought d10, 97 productive tiles at d18, 119-159 tomatoes d18-29); wheat relay gone; mirror games decided in d15-29 by +3.4k (strawberry, eggs, carrot).
- 2026-09-29-judgecal1.md + rivalp48.md: our closed-loop judge rival (a learned clone) is ~25 % UNDER-BUILT vs the real seats (d9 animals 13.7 vs 19.4, productive tiles 55 vs 74, no tomato book, half the strawberries; same-board final −23k below the live MELON seat); the scripted programme port is also unfaithful (10.4 animals at d9, out of cash d2-7). NO faithful programme rival exists today; REFRESH1 (retraining the clone on the newest 1,416 seats) made it worse (−23k vs the old clone). The public V56 agent IS faithful for the V band (vband1.md).
- 2026-09-29-melonpre1.md, brainstorm2.md, drawreact2.md, lateloss1.md, crewloss2.md, dagger1.md, trainreview1.md, vloss1.md, realloc1.md, platenoland1.md, combo1.md, gametheory1.md, arb1.md, riskwin1.md: a d3-4 melon plate (P8d3) gains +3.2k own but loses the margin because it withholds d1-9 animal buys (herd d9 5.2/2.6/1.2 vs 6.1/3.4/1.7); pre-emption has no target (the plate ripens after the rival sold 42/45 wave melons); daily reinvestment raises own +4.8k but the rival wins it back in milk (margin +1.0k, flood −8.6k); PFS already scales volume with the shop draw exactly like the programme; crew is a consequence not a cause (0 labour-bound days / 1,160); the d20-29 loss deepening is spread over books; V losses = town draw; every d0 reallocation, plate-on-starting-tiles, herd floor, market-making, variance bet and game-theory channel is closed on evidence; DAgger distillation of PFS stalls at ratio 0.21; ES on theta and PPO on the head are flat/plateaued; a 20-game screen overstates cells by 2.5-4.7k, only 80-game paired reads vs the reacting rival count.
- In flight: CLSEARCH1 (closed-loop successive-halving over d1-9 switches; rung-1 leader = daily reinvest 4:600 × a herd window that keeps the cows: margin +3.3k t 2.6, own +2.0k, W 35→39 on 40 g), COMBO2 (P8d3 plate + reinvest), BRAINSTORM2 r2 (LUMP9 = move the d10 animal lump to d9 by selling the d8 milk), ESHEADCL1 (ES on the RL head's day-windowed output biases with closed-loop own-coin fitness), PORTGAP1 (day-by-day d0-9 cash ledger: real P48 vs port vs PFS — where does the programme's d1-9 funding come from), REFRESH1 (ablation on the newest seats).
- docs/strategy/BUILD-STORY.md (tail 300 lines) = the ship/reject log.

### Rules of evidence
Two-purse rule: only PAIRED reads (same boards, both purses) count; tape reads inflate deviations ~9x; a cell is a CANDIDATE only at own ≥ +2k (t ≥ 3) with margin ≥ 0 vs the reacting rival on 152 held-out games, then flood own ≥ 0, then faithful live tapes W not lower. Uploads: 2 slots, one is PFS; a bold body earns the second slot only if its own mean rating ≥ PFS's (two copies of PFS = +10..+14 rating points). Time left: ~30 h of compute (remote 8 cores + 2 GPUs, judge ~0.16 games/s).

### Deliver (markdown, ≤ 2,500 words, numbers not adjectives)
1. Which of the six invariants is most likely WRONG or incomplete, and the single cheapest read (≤ 80 games or a ledger over existing replays) that would show it.
2. The 5 boldest ideas consistent with the invariants that NOBODY has tested (check BUILD-STORY and the docs so you do not repeat a closed cell), each with: mechanism in one sentence, expected own/rival coins and where they come from, the exact test (switch or change, grid, games, bar), P(pass) and why, and what makes it different from the closest closed cell.
3. What the top-1 team (PQ4) would change next, and whether it creates an opening for us.
4. Given the port and the clone both fail to fund the d1-9 build, the most likely cash source the real P48 uses that our ports miss (be concrete: which sale, which day, which price), and how to verify it from the replays in S/topaudit1/cache (per-step money is recorded).
5. A one-paragraph verdict: the single line to put all remaining compute on, and the line to stop.
