# astra brainstorm15 — executor gap: fertilizer vs acreage vs turnaround (2026-09-30 08:16Z)

Third participant (codex gpt-6-astra) on CREWSCHED1 per-hand trace tables (truth MMPQ hands vs executor c2/c9 on 20 boards d10-20): wheat 580 vs 286 u split, exact per-hand rule set for a 2-hour implementation, the 11:00Z fertilizer-ceiling counterfactual, the noon freeze and upload panel. Prompt: scratchpad astra_bs15/prompt.md.

294 wheat units are missing; roughly 66 are consistent with the measured yield difference, leaving 228 attributable to harvest frequency, occupied acreage, and their interactions. **Fertilizer alone is unlikely to close the body gap.**

1. **Q1 — working allocation, not identified causal effects.**
   - **(c) Idle/weedy acreage: 148 units; 148 × pW reference coins.** Largest working allocation, but inseparable from delayed replanting in these aggregates.
   - **(b) Turnaround: 80 units; 80 × pW coins.** Attribute this to harvest-to-replant delay and missed service, not slower biological growth.
   - **(a) Yield/fertilizer timing: 66 units; 66 × pW coins.** Calculation: `286 × (4.66 / 3.79 − 1) = 65.7`; this includes watering/harvest timing, so it is not a fertilizer-only estimate.
   - **(d) Off-phase watering: zero additional units in that accounting.** Its benefit is mediated through (a–c); adding another allocation double-counts recovered labour.
   - These provisional allocations sum to 294. The reference wheat price is absent from the supplied material; `pW` means that price, and these are gross production values, not net cash.
   - Your detailed table has **3.27 days ours versus 3.46 truth** plant→harvest. The alleged 3.9–5-day cycle must include idle turnaround or use another population.
   - Likewise, `1,666 × 0.89 / 440 = 3.37` excess strawberry waters/game-day under matched exposure—not seven/hand-day. The visit table suggests about 5.6 extra strawberry-only watering visits/day.
   - **First rule: reserve and finish the whole tile visit before moving away:** WATER if productive → HARVEST → PLANT one seed → WATER. Replant on the next legal hand action, not literally the same hour.
   - Do not force every wheat harvest to yield six: truth frequently takes five at age three. Also, c2’s fertilizer flag prevalence is already 0.64 versus 0.66; timing and yield realization matter.

2. **Q2 — the two-hour implementation; 0.90 is a test target, not a promised result.**
   - Preserve existing opening/shop allocations. At every hour keep `SELL → HIRE → BUY_ANIMAL → BUY_LAND → BUY_SEED → BUY_PRODUCT`, respecting ten market orders.
   - On d10, hire twelve total: fill available h0 slots after sales, finish at h1 subject to the cap. Preserve known sale lots, land retries, and later hire/endgame schedules.
   - Every hand `k`, every hour `h`: execute the first applicable priority below; break assignment ties by shortest travel, then tile ID, then hand ID.
   - **P0:** rescue a crop/production-eve animal whose remaining deadline slack is zero; calculate slack from travel plus all required actions.
   - **P1:** finish an already reserved tile bundle. Reserve its seed, consumables, inventory space, and remaining hours before starting; release ownership only on completion.
   - **P2, h0–23:** complete productive work on the current tile before departing: animal HARVEST if ready; FEED if due; CARE if due; COLLECT_FERTILIZER if available.
   - For each such action use the simulator’s required quantity; collect all legally collectible fertilizer. Do not create repeat visits for FEED, CARE, and collection separately.
   - **P3, h0–3:** if an assigned nearby animal route needs wheat, load toward six: `PICKUP WHEAT q=min(6−carried, stock, free capacity)`. No speculative loading without a route.
   - **P4, h0–19:** unfertilized wheat at age two, or age three before its next productive watering: `FERTILIZE 1 → WATER`. Require available fertilizer and actual simulated yield benefit.
   - **P5, h0–20:** harvest-ready wheat: productive WATER first, then HARVEST all, PLANT one scheduled demand seed or wheat filler, WATER once. Skip unnecessary WATER.
   - Start that four-action bundle only with four actions remaining; an already-watered three-action bundle may start at h21. Avoid a blanket extra day waiting for yield six.
   - **P6, h0–21:** free tile → PLANT one → WATER; weed tile → DIG → PLANT one → WATER, requiring three remaining actions. Stop new planting after d27.
   - **P7, h0–23:** remaining production-eve FEED→CARE bundles and productive crop watering; use earliest deadline, then travel distance. Off-eve feeding comes last.
   - Strawberry WATER requires a productive phase or survival need; use the simulator’s phase predicate, not an invented age-parity shortcut. Apply the same marginal-benefit check to wheat age-one watering.
   - At h20–23, promote all unfinished production-eve/survival deadlines above new jobs. Buy seeds one step before reserved planting, in existing one/two-seed lots.
   - One owner per unfinished tile bundle; reassignment requires explicit release. Discard only the minimum cargo blocking a more valuable feasible action—never imitate observed discard totals.
   - Implement bundles/ownership, phase watering, then fertilizer timing. Keep each change separately switchable; c3/c8 already argue against another rigid feed-first crew.

3. **Q3 — by 11:00Z, measure fertilizer’s isolated ceiling.**
   - Run HOLD20 with the frozen baseline action trajectory and a shadow wheat state receiving free fertilizer at its earliest legal useful time; simulate normal WATER/yield transitions and identical harvest times.
   - Keep actual inventory, routes, prices, planting and actions unchanged; record extra shadow wheat and its reference-price value. This is an optimistic yield-only counterfactual, not a deployable agent.
   - **Kill “fertilizer alone gets us to 0.90” if even that ceiling is below the required cash gain:** approximately `0.90×131,621−102,888 = 15,571`.
   - A large gain establishes mechanical headroom; it does not prove affordable collection/application. A small gain kills fertilizer-alone at this schedule, not fertilizer interacting with better timing.

4. **Q4 — freeze at noon; qualify on wins against reacting opponents.**
   - Minimum panel: all V56 m40+v21, 103 P48, 24 PQ4, and OTH56; run candidate and PFS on identical draws and both seats. Bootstrap by board/tape, not individual seat.
   - V56 must react live. P48 gate decisions must be recomputed from candidate-induced state; fixed downstream tape actions cannot certify resistance to gate reactions.
   - Proposed preregistered bars: V56 win score ≥0.50 separately on m40 and v21, with no paired regression against PFS; ties count half.
   - Require positive overall paired win-score improvement over PFS with a 95% lower bound above zero, using weights fixed before results; no other family loses over five percentage points.
   - Require zero invalid-action/runtime failures. Treat small-family bars as screening limits, not statistical proof. A 0.90 HOLD20 ratio alone clears none of these gates.
   - Noon–15:00 panel; 15:00–16:30 investigate failures and validate the frozen artifact; finish uploads by 17:00, preserving time to verify the final two entries.
   - If still below 0.90 at noon: stop reconstructing MMPQ. Spend two hours testing only proven local fixes in PFS, two hours on the paired reactive panel, then package and verify. Preserve the strongest validated second entry if nothing clears the bars.