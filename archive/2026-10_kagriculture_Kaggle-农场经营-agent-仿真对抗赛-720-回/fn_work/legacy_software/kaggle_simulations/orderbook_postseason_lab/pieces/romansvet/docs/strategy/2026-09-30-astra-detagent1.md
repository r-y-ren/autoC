# astra DETAGENT1 review (gpt-6-astra, 2026-09-30 17:04Z)

Prompt: scratchpad astra_det1/prompt.md (carrier-role crew split spec, 5-cell fix grid, backup-package invariants and form, the one read). Consumer: DETAGENT1 builder (docs/strategy/2026-09-30-detagent1.md).

**Choose (a) for the required backup: a standalone body on every seat. Package the proven `crewF4Sbcfa` immediately, then improve a separately versioned candidate.** Packaging does not establish that it should replace either live upload; that decision remains yours.

One baseline correction: `crewF4Sbcfa` is HOLD **0.920 coins / 0.822 value**, TUNE **0.817 / 0.818**. Its HOLD sold units are **399 wheat, 192 eggs, 148 milk, 128 wool**. The 457/181/126/112 vector belongs to the preceding body. [Recipe and measurements](/mnt/e/_work/kaggriculture3/S/crewcombo1/BEST.txt)

**Q1. Implement a reserved delivery chain, bypassing both BC heads.**
The following is an untested dispatcher specification, not a demonstrated recovery of 15 tiles with zero animal cost.

- **Eligibility:** for each strawberry, compute `s=d+1-planted_day-10`; tonight ticks iff `s>=0 && s%2==0 && s/2<4`. Prioritize d15/d19, but service the other waves’ actual tick eves too.
- **Count useful service:** water today and `fertilized_until_day>=d`; do not count a redundant fertilizer action. Harvest before a tick if accumulated yield would clip at the four-unit cap.
- **Roster:** the code requests **12 hired hands plus farmer**. At h1–h2, after actual hires appear, reserve hands 1–4 for animals, 5–8 for fertilizer delivery; farmer and hands 9–12 retain crop/build work. Reassign deterministically if hires fail.
- **Animal reservation comes first:** partition animal tiles into four compact routes, balanced by travel plus required FEED, CARE, HARVEST and remaining collection actions. Carry one wheat per planned feed; refill against observed stock.
- Keep FEED→CARE coverage daily through d26, not only on production eves: care accumulates toward later production. Include harvests needed to prevent animal-yield clipping.
- If four animal routes cannot finish by h23, reserve another free hand before allocating carriers. Never silently steal an animal worker to meet the strawberry quota.
- **Carriers:** four routes with quotas **4/4/4/3**, assigned to spatially compact eligible strawberry clusters; deterministic ties `(cost, hand_id, y, x)`.
- **h1–h8:** collect one fertilizer from each assigned animal source until the route’s quota is carried. Choose sources by the complete source→strawberry route cost, not nearest source alone.
- Use existing shed fertilizer through `PICKUP FERTILIZER n` when that shortens the route. Reserve only the delivery shortfall from fertilizer SELLs at h0/h2; release excess after assignments finish.
- **h8–h21:** deliver FERTILIZE→WATER on each assigned berry needing both. Already-watered tiles need only fertilizer; already-fertilized tiles need only water.
- Departure is quota-driven, not clock-driven: leave collection early whenever another collection would make the final delivery miss h23. A carrier with fertilizer must not wait until h8.
- **h18–h23:** finish accepted routes; assign emergency water for plants with one dry day. Release completed carriers immediately.
- Accept a route only if its explicit action count—collection/pickup, Manhattan travel, fertilizer, water and necessary harvest—fits the remaining steps, preferably with **two steps slack**.
- Priority is **hard reservation**, not another `-6`: protect assigned actions and travel before pass 1, remove reserved work from free-hand matching, and skip both BC routing and action replacement for reserved hands.
- Prevent generic shed jobs, wheat fertilizer tasks and DROP from consuming a carrier’s assignment or inventory. Reconcile quantities and completed actions from the next observation.
- Rebuild at dawn: hands disappear and inventories deposit into the shed. Do not persist hand ownership across days. [Simulator](/mnt/e/_work/kaggriculture3/S/harness2/fastenv/sim.hpp:686)

**Expected effect:** increasing *usefully fertilized* d15 berries from six to fifteen adds approximately **nine units at the next tick**, not eighteen. Against comboSFW’s 32.8–33.9, **about 42–43 st15** is a defensible conditional estimate; **45+ is a stretch target**, requiring enough timely plantings, picks and deliveries.
Expected incremental egg/milk/wool loss is **approximately zero only if animal reservations remain feasible**; no measured estimate establishes that yet. Reject preservation claims if any product falls **>5%** versus the matched control. Emission’s delayed animal purchases are a separate cost.

Print these structured lines to stderr, using observed next-step outcomes rather than treating issued actions as successes:
```text
ROLE ep= seat= d= h= uid= role= pos= target= quota= route_steps= slack= reason=
CARRY ep= seat= d= h= uid= fert_before= wheat_before= op= source= reserved_left= bc_override=
TICK ep= seat= d= h= tile= planted_day= tick_next= yield= water= fert_until= owner= deadline=
EXEC ep= seat= d= h= uid= issued= confirmed= fert_after= water_after= fail_reason=
ANIMAL ep= seat= d= h= tile= owner= fed= cared= unfed= pending_bonus= yield= finish_h=
```
At h23 also print `eligible / watered_and_fertilized / unfunded / unreachable / unfinished`, animal missed feeds/cares, and fertilizer sold/reserved/discarded. At d18 print strawberry **harvested, deposited and sold separately**.

**Q2. Five cells, 45 minutes each = 225 minutes; fifteen minutes remain for selection.**
Each cell runs closed-loop **HOLD20 + TUNE20**, paired against frozen B=`crewF4Sbcfa`; reuse verified B traces and recover its currently unspecified st15/egg18 baseline.
Report per set: coins ratio, value ratio, st15 harvested/sold, egg18, milk/wool full-game and d18–29, paired coin change/t, animal misses and runtime.
The ordering below is a hypothesis about coin upside, not measured forecasts. “Kill” means stop promoting that cell; preserve its diagnostic output.

| Order | Cell | Required mechanism read | Kill number / evidence against mechanism |
|---|---|---|---|
| 1 | **B + ST emission + window pick + reserved animal/carrier split** | ≥20 standing strawberries d8; aim ≥15 useful d15 care completions; st15 ≥40, stretch ≥45 | Kill if st15 <40 or any animal product loses >5%. If ≥15 care completions occur but timely harvested units barely rise, delivery is not the remaining bottleneck. |
| 2 | **B + animal-route reservation only**, d10–26 | Fewer missed FEED/CARE chains; target +10 milk and +10 wool, eggs preserved | Kill if animal value gain <1,500/game at reference prices, or missed service falls <20%. Existing adequate service with low output points to herd timing/caps instead. |
| 3 | **B + local wheat completion chains** | After HARVEST/DIG, reserve the same hand’s next legal PLANT on wheat-assigned tiles; buy only required seeds | Target +60 sold wheat; kill below +30 or >5% strawberry/animal loss. Seed availability improving without fewer empty tile-hours disproves a seed mechanism. |
| 4 | **B + ST emission + window pick + the same animal reservation**, carriers OFF | About **21 strawberry tiles by d7**, d6–7 strawberry funding ahead of incremental animals; compare directly with cell 1 | Kill emission implementation below 20 standing tiles d8. If tiles rise but st15 gains <6, count alone is insufficient. Cell 1−4 isolates carriers. |
| 5 | **B + window pick only** | Permit yield-1 harvests d15–17; route/deposit early enough to reach a sale inside the window | Kill if window sold units gain <3. More harvests without earlier sales exposes deposit/sale timing, not picking. |

For every cell, **pooled coins-ratio loss >0.010** is an additional promotion stop; inspect H/T separately rather than hiding a TUNE regression.
Cell 4 uses `st_nores_d=5;cf_first=6;cf_last=7;st_smin=6;st_smin_d=7`. Fund essential hires/feed first, then the strawberry wave before additional animals.
Do not extend the hold past d7 without evidence: extending to d9 previously left the d8 count unchanged at 20.1.
Do not reopen bulk wheat-seed stocking: it reduced seed shortfall **8.6→1.2**, but empty tiles barely changed **11.5→11.2**.
The corrected B gaps put milk+wool at roughly **9.3k reference value**, wheat **4.5k**, eggs **2.0k** on HOLD; that supports animal coverage ahead of an eggs-only expansion. [Measured comparisons](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-30-crewcombo1.md)

**Q3. Package invariants and choice.**

- Build `dist/detagent1_base.tar.gz` from the frozen recipe now; include m1 weights, inference, feature code, rulebook and entrypoint. No scratch paths, environment-dependent knobs or external downloads.
- Pin m1 checksum **`0ac2ff9962234c5a91e12327dc205b0a`**; include source/package hashes and baked configuration in a manifest.
- Unpack into a clean directory and run the actual submission entrypoint. **Zero exceptions/timeouts**, p99 **<0.65 s including BC**; measure cold loading separately against the runtime limit.
- Verify all 720 steps, both seats, roster changes, refused HIRE/animal/seed/land purchases, shed saturation and both normal/adverse market trajectories.
- Emit exactly the observed live roster. Retry unmet purchases from observed deficits; do not assume an issued buy succeeded or duplicate fulfilled purchases.
- Apply the PLANT atomicity guard **after all overrides**, including the literal opening: per crop, total requested PLANTs cannot exceed current seeds. Same-step seed purchases cannot fund those unit actions.
- Opening identity: d0h0 **COW 1 + WHEAT 5**; d0h1 **SELL WHEAT 1, HIRE×4, COW 1, SHEEP 3**. New research knobs must not alter successful baseline d0 traces.
- A matching roster alone does not validate the literal opening after a refusal: check positions, carried animals and required inventory; otherwise execute observation-based repairs.
- Repeat identical games in fresh processes with different hash seeds: require **byte-identical serialized action streams and final states**. Sort ties explicitly; reset per-game role state.
- Verify the packaged artifact reproduces the frozen source’s full action traces and results. Keep the baseline artifact while building `detagent1_candidate.tar.gz`.

**Pick (a) for the backup artifact.** It directly satisfies the standalone deterministic requirement. Neither hybrid has earned preference: h1×f4sbcfa is **−16,514 on faithful P48**, and pooled faithful **−16,887, t −9.33, net −8**.
Option (c) is a new state-transfer experiment, not a demonstrated repair. PFS→body must derive all assignments from the actual farm and disable the literal opening.
Against V’s d0 melon plate, the standalone body continues its own programme and handles changed prices/refusals. Farms are separate; V does not exhaust a shared seed allocation. Do **not** add an emergency d1 PFS handback: the earlier programme→PFS bridge scored **0/40** against V56.
The existing standalone body’s **2/40 and 0/21 V56 wins** remain a performance liability even after packaging safety passes.

**Qualifying (b) or (c):** freeze one bridge/day before confirmation, paired against the actual prospective retiring package, with vrp26 alongside.
Use H-v4 **P48TAPE172 + PQ4TAPE26 = 180 unique programme games**, plus **OTH56** and reacting **V56 m40+v21 =61**; deduplicate overlaps before pooling.
Require programme paired margin **t≥2**, board-clustered win-score **95% lower bound >0**, own-coin change ≥0 per set, OTH nonnegative, and no paired V win regression.
For (b), require unfired action identity and V identity; for (c), test both-seat handover states and preserve strawberry/late-animal supply.
Check rival production faithfulness per product, not total units dominated by wheat; unresolved rival collapse disqualifies the read rather than becoming an excluded winning row.
H-v4 reports an estimated **+2.3k/game deviation bias, SE≈1.2k**. A marginal H gain alone is insufficient: require agreement across tape-anchor directions or genuinely reacting programme validation. [Harness calibration](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-30-harness2.md)

**Q4. The one read: the joint deadline-feasibility ledger.**
On the same 40 boards, enumerate each d15 berry’s useful fertilizer deficit and construct explicit routes using actual hands, fertilizer and animal-service obligations.
Report **maximum found feasible completions**, remaining animal misses, and the resulting window-yield ceiling; distinguish this constructive schedule from an unproved optimum.
If ≥15 berry completions fit while preserving animals but the dispatcher achieves six, carrier reservation stays first.
If complete care still leaves the window-yield ceiling <40, move emission/timely harvest ahead of carrier tuning.
If berry completion requires sacrificing animal service worth more than its incremental output, move animal-route repair first.

**First 45 minutes:** package and clean-run frozen B first; instrument the joint ledger; implement cell 1 with hard role locks and run HOLD20/TUNE20. Preserve the baseline package regardless of cell 1’s result. This review made no repository or dist changes.