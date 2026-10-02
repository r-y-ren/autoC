**Planner findings — 2026-09-10**

The planner has a useful execution foundation, but purchase, labor, routing, and selling decisions use inconsistent economic objectives. The review establishes reproducible defects and their measured scope; it does not establish a competition-winning configuration.

Read the [detailed review](reviews/planner-2026-09-10/REVIEW.md) for source locations, reproductions, engine semantics, limitations, and the implementation roadmap.

**Reviewed version**

The reviewed source is `.claude/worktrees/ship-pair/src/kagg3/`. Eight relevant source files match `dist/submission_flow172_g940_pair.tar.gz` byte-for-byte. The main checkout is older than this submission. [Provenance and hashes](reviews/planner-2026-09-10/provenance.json) identify the exact source and engine.

**Findings and evidence**

| Finding | Evidence | Practical implication and limits |
|---|---|---|
| Land price is missing from its utility comparison. | A zero-bias probe buys land for 1,000 coins to gain 34 coins of modeled incremental candidate profit. | Subtract the full land cost from incremental utility and recalibrate the learned bias. None of the eight land purchases in the four baseline games failed this break-even comparison. |
| Admitted essential work can remain unexecuted. | A tier-2 survival-watering task is admitted but omitted, although a direct route takes only 10 turns. | Validate essential operations against emitted actions and repair feasible omissions. Frequency in trained play was not measured. |
| Route repair can reduce its own task-value objective. | A capped-yield probe falls from 840 to 720 to 360 completed value over the three rounds. In baseline play, 11 of 120 day-plans finish below an earlier round. | Improve route selection together with its value model. A tested best-round selection intervention worsened mean final score margin by 612.5 coins across four games; it is not a validated improvement. |
| Forecast work can purchase idle temporary workers. | A synthetic immature-melon stress state hires 12 workers for 376 coins while every action is PASS. | Price today's executable work and development against today's wages. Workers disappear nightly. The stress state does not establish incidence under the trained policy. |
| Discretionary purchase allocation lacks a cash-retention alternative. | An allocator probe buys value 6 for cost 80; a full-plan carrot probe buys and plants modeled value 5 for cost 20. | Compare net continuation value with retaining cash, including any explicit strategic value. Changing this baseline may require co-training. |
| Purchases and reservations are finalized against queued work rather than final execution. | In 27 of 120 baseline day-plans, newly purchased seeds exceed scheduled use after existing stock is counted; excess seed cost totals 1,180 coins. Five plans reserve seven fertilizer beyond routed applications. | Reconcile final routes with a resource ledger and value intentional advance inventory explicitly. Persistent inventory means 1,180 coins is not measured lost profit. |

**What to retain and what to change first**

Retain the shared NumPy/JAX implementation, explicit operation order, exact route distances, per-block pickup accounting, purchase cash/shed constraints, marginal market-impact sales, and endgame handling. Neural forecasts already exist in the reviewed version.

1. Add economically meaningful oracle cases for land break-even, cash retention, essential-task feasibility, and temporary-worker wages.
2. Align decisions around incremental continuation cash: input costs, executable labor, sale/deposit timing, price impact, and displaced alternatives. Recalibrate learned residuals when changing their baseline.
3. Evaluate a bounded shortlist of feasible crew sizes and routes, with explicit essential-operation coverage.
4. Reconcile purchases, reservations, and sales with final emitted actions while preserving explicitly valued future inventory.
5. Gate changes through reference-engine comparisons, then co-train and evaluate on broader fresh opponents, boards, and both seats. A better internal task score alone is insufficient evidence.

**Validation and reproducibility**

- Four baseline full games reproduced saved own and opponent cash exactly; instrumentation covered 120 day-plans. These use two opponent tapes in both seats, not four independent opponents.
- Four additional full games tested the route-selection intervention; the negative result is retained.
- 44 focused existing tests passed. This was not the full suite or a new backend-equivalence check.
- Production source was not modified for this review; interventions ran in memory.

The evidence directory contains [synthetic results](reviews/planner-2026-09-10/probes.json), [baseline game traces](reviews/planner-2026-09-10/games.json), [route intervention results](reviews/planner-2026-09-10/route_ab.json), and [test output](reviews/planner-2026-09-10/tests.log). Reproduction scripts are [probe.py](reviews/planner-2026-09-10/probe.py), [games.py](reviews/planner-2026-09-10/games.py), and [route_ab.py](reviews/planner-2026-09-10/route_ab.py). Their current paths assume this workspace and write outputs under `/tmp/kagg3-planner-review/`.

---

**Verification and decisions — 2026-09-10 18:50Z**

Each finding was re-verified by a separate independent session (reports in `strategy/2026-09-10-verify-F1-land-price.md` … `verify-F6-purchase-reconcile.md`; summary table in `strategy/2026-09-10-consensus.md` §14). Every probe reproduced to the coin on the reviewed tree, and every line number transfers to the shipped tree (`ship-pair-hr` differs from `ship-pair` by one line, `HIRE_ROW_ON`). The decision per finding is whether it can move the paired win rate on the 72 target-band boards (`S/livec`), which is what the ladder rating tracks.

| Finding | Verdict | Decisive measurement | Decision |
|---|---|---|---|
| 1. Land price missing from the utility comparison | Partly true | The `land_bias` gene charges the price by design; the trained theta decodes exactly −land price on the probe state and does not buy. Every loosened land gate lost paired today (TOPB −16,640 t −9.4; LIVE55 34.5→15.5 %). | **No change.** The recalibrated fix is a no-op by construction. `LAND_FRAC_SOFT_ON` stays as a training-arm option only. |
| 2. Admitted essential work can remain unexecuted | True in code, not in play | Trained play, 180 day-plans: 0 of 2,240 survival waterings unemitted; 4 of 5,060 mandatory ops unemitted, all on day 29; ≈ 99 planner coins/game (0.13 %). Insertion/exchange oracle (09-08) recovered +429/game against a 1,500 bar. | **No change.** Closed. |
| 3. Route repair reduces its own task-value objective | Partly true | The loop optimises admission-vs-route feasibility, not value. The −612.5 intervention read was 3 distinct games (0.6–1.0 SE). Re-measured paired on 12 boards: Δ −10 coins, t −0.07, no flips, inert. | **No change.** The best-round selection is not built. |
| 4. Forecast work purchases idle temporary workers | True in code, fix refuted | Trained theta hires 0 on the probe; shipped tree has 0.00 idle hand-days/game. Horizon 0 ("price against today's wages") costs −13,037 / −13,676 own coins and flips both test boards to losses; horizon 3 loses too (94.4→65.3 %). | **No change.** The gene sits at an interior optimum; this term is also why the planner cannot ramp like the top tier, so shortening it is the wrong direction. |
| 5. No cash-retention alternative in purchase allocation | Partly true (seed lists only) | Fertilizer, animals and land already gate on cost. Trained play: 14 of 1,215 granted units (1.2 %) below cost, ≈ 361 coins/game ceiling; purse binds on 8 of 120 days. Every hold-cash lever measured today or earlier lost or read level. | **No change.** A strict value > cost eligibility is the only untested form and is not worth a run at a 361-coin ceiling. |
| 6. Purchases finalized against queued work | Partly true | 96.6 % of the 1,180 "excess" seed coins are planted within two days; 1,080 of them are one board counted twice (seats identical). Shipped composition: 99.1 % of seed bought is planted, ≈ 20 dead coins/game; seeds never touch the shed and have a constant price. | **No change.** A reconciliation step cannot be resolved by the judge (1/70 of the LIVE62 SE). |

**What we keep from the review.** The source readings are correct and are now on file with line numbers. Two method corrections are adopted campaign-wide: probes must be evaluated under the trained decode, not at zero bias (the initialisation is not the shipped policy); and under pinned towns most boards return identical money in both seats, so incidence and significance count boards, not games (`S/bank/paired.py` already reports its t on boards; the review's n=4 and 27/120 both need de-duplication).

**What we are doing instead.** The live hypothesis is the ES training population, not the planner: the target band was 0.4 % of the objective. Three arms with the target-band objective are training (flow187, flow188 on the remote 3090s; flow189 on the local 3070), each with a 62-board held-out win-rate gate and the local three-leg paired judge. Stop rule: hold-out LIVE-C must move ≥ +5 win points within 300 generations, or theta arms stop and the planner is treated as the ceiling.
