# Attribution and license

This agent retains Apache-2.0 notices in its source. Modified in EXP-167 on
September 10, 2026 by Ahmed Berat Özer's Kaggriculture project.

- [Dmitrii Gluzdov — Two Coins, One Sheep](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2650): bounded two-turn stock reservations, protection of scheduled pickups, partial future-order deductions and placement after worker repairs. Adapted to our per-player chassis state and preserved terminal planner. Earlier seven-turn physical closure work is also retained through v31.
- [prvsiyan — The Moon Counts Melons](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-moon-counts-melons): the later cattle substitution controller. Earlier fertilizer/feed and tomato production work remains credited in v31's source.
- [yhay81 — Shop Router 0909](https://www.kaggle.com/code/yhay81/shop-router-0909): thirteen public action schedules and ordered shop-pair routing; earlier ShopForge/Fieldbook lineage.
- [aurax7 — Reactive Router](https://www.kaggle.com/code/aurax7/kaggriculture-reactive-router): sale timing and shed projection lineage.
- thomastschinkel: replay-routing research and earlier foundation of this project; tetsutani: market, room and repair mechanisms credited in the retained source.
- [destbreso — X-ray Your Agent](https://www.kaggle.com/code/destbreso/x-ray-your-agent): diagnostic methodology. Its notebook is not bundled as agent runtime.

Other audited Codes appear in SOURCE_AUDIT.md and the evaluation panel; their
presence there does not imply their code was incorporated. Credits do not
imply author endorsement or a verified private-leader implementation.

## EXP-168 changes (v34)

- [lucifer19 — Harvest Nocturne](https://www.kaggle.com/code/lucifer19/harvest-nocturne-the-market-has-a-rhythm): occupied-tile similarity and exact price-loss ordering ideas/code, adapted and independently tested. Per-seat memory/reset replaces its single shared controller state.
- [flexonafft — Most Powerfull Route](https://www.kaggle.com/code/flexonafft/kaggriculture-most-powerfull-route): requested source snapshot; its full executable bundle is byte-identical to Two Coins above. No new route or original capability is attributed to a renamed copy.
- leoprovorov: public-layout comparison lineage credited by Nocturne.
- [Kaggle official implementation](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture): Apache-2.0 market-price functions from version1.32.7; verified against local engine.

All earlier in-source notices and the full Apache-2.0 license remain in main.py.
This list implies no author endorsement. Exact incorporated switches appear
in agent/manifest.json; unselected experiments are not claimed as improvements.

## EXP-175–178 changes (v35, September 11, 2026)

- [yhay81 — Shop Router 0911 Simple](https://www.kaggle.com/code/yhay81/shop-router-0911-simple): revised opening market-sequence idea. Our selected opening uses `BUY_PRODUCT WHEAT 13`, `BUY_PRODUCT WHEAT 30`, `SELL WHEAT 30`; it retains the earlier thirteen routes rather than adopting the donor's complete fourteen-route revision.
- [leoprovorov — Two Coins at High Noon: Small Improvement](https://www.kaggle.com/code/leoprovorov/two-coins-at-high-noon-small-improvement): Mirror Counter's public cash-response mechanism. Adapted to the existing occupied-tile similarity guard and per-player state, requiring positive matching cash changes after a probe. Our fourth-turn reservation is an independently tested modification, not a claim about the donor's reported results.
- [prvsiyan — The Soil Remembers Rain](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-soil-remembers-rain): the already reviewed V234 six-sheep southeast expansion, including financing, confirmed hiring, feed, care and credited production. Adapted to our chassis state, combined telemetry and terminal-planner abstention. This capability is newly integrated here; the September 11 exported donor code itself is unchanged from the earlier reviewed version.
- [lucifer19 — Harvest Nocturne V2](https://www.kaggle.com/code/lucifer19/harvest-nocturne-v2-a-lighter-start): audited startup and runtime packaging reference. Our chassis already shared read-only route data, so no new gameplay gain is attributed to its deep-copy removal.
- [Nagata V6.2](https://www.kaggle.com/code/nagatakengo/kaggriculture): added as a reacting evaluation opponent. Its policy is not bundled in this submission.
- [destbreso — X-Ray Your Agent](https://www.kaggle.com/code/destbreso/x-ray-your-agent) and [Georgy Mamarin — What 2600+ Farms Do Differently](https://www.kaggle.com/code/georgymamarin/kaggriculture-what-2600-farms-do-differently): whole-cohort and economic diagnostic references; no runtime code copied from these notebooks.

Integration, public-response safeguards, experiment design, official-engine accounting checks and release packaging: Ahmed Berat Özer's Kaggriculture project. The complete agent retains its Apache-2.0 license and upstream notices. Exact source hashes and the distinction between incorporated code, evaluated opponents and diagnostics are recorded in `research44/SOURCE_AUDIT.md` and `research47/REPORT.md` in the project workspace.

## EXP179–180 changes (V36, September 11, 2026)

- [Tetsutani — Market Smart Farming](https://www.kaggle.com/code/tetsutani/market-smart-farming-kaggriculture): its updated four-turn configuration motivated this isolated extension of our existing Two Coins stock-reservation layer. V36 applies four turns within V35's physical stock, debt, purchase and terminal guards; farm routes and investment controllers are unchanged.
- [Rayk Kretzschmar — Rank Your Agent](https://www.kaggle.com/code/raykkretzschmar/kaggriculture-rank-your-agent) and [Kunal Desale — Kaggriculture2026V1](https://www.kaggle.com/code/kunaldesale2408/kaggriculture-2026-v1): newly evaluated exported opponents. Their separate sale-order scoring ideas were screened and rejected as standalone modifications; those runtime policies and their route libraries are not incorporated into V36.
- The September11 afternoon Flexon export hashes identically to V35; this differs from the older EXP168 snapshot described above. It supplies no new V36 capability.

All earlier Apache-2.0 notices and the complete license remain in main.py. This 130-byte source extension, experiment design, accounting checks and packaging are by Ahmed Berat Özer's Kaggriculture project. Full provenance: research48/SOURCE_AUDIT.md and research49/REPORT.md. Credits imply no author endorsement.

## EXP182–190 changes (V37, September 12, 2026)

V37 retains V36's route library and all earlier source notices. The finite native-crop fertilizer planner, committed-parent priority guard, projected warehouse guard and exact-spawn cooperative tomato labor scheduler were developed and physically audited in this project. Earlier unsuccessful livestock and rival-flow experiments are not included. The latest public Code review is documented in research56/SOURCE_AUDIT.md; those updated analytical/data notebooks supplied no new executable policy to this release.

All earlier Apache-2.0 notices, including thomastschinkel, yhay81 and destbreso, remain intact in main.py along with the full license. Evaluation, guards and packaging are by Ahmed Berat Özer's Kaggriculture project. Credits imply no author endorsement. See research59/REPORT.md for the mixed evidence and release-candidate status.


## EXP193–217 changes (V38, September 12, 2026)

- [Steven Lee Hans — Lord Momo Returns](https://www.kaggle.com/code/stevenleehans/kaggriculture-rank-580-lord-momo-returns): conceptual reference for comparing feed cost with production value and selling surplus fertilizer. Our implementation independently adds care-value accounting, the following-day feeding schedule check, actual carried-food checks, and a reserve for all remaining native and committed crop inputs. No guarantee about future feeding or monotone fertilizer prices is inherited from the donor narrative. Audited exported source SHA-256: `b5c2e156689b41cea5f2e1a0a1cae2e18fd70423931bbac0885bba8b2142c497`.
- The exact-spawn finite-input tour planner, committed-parent fertilizer queue guard, conservative tomato fertilization margin test, next-day service simulation, whole-animal survival audit and integration are by Ahmed Berat Özer's Kaggriculture project. The source preserves the existing route and chassis lineage; tested mechanisms are identified by the frozen manifest.
- [Pilkwang — Structured Economic Policy](https://www.kaggle.com/code/pilkwang/kaggriculture-structured-economic-policy), the Momo source and four other distinct exports were examined in the September 12 public refresh. Six new distinct policies entered the reacting panel; their inclusion as opponents does not mean their runtime was incorporated. Exact V37 duplicates were deduplicated. Complete review: `research84/SOURCE_AUDIT.md` in the project workspace.

All earlier Apache-2.0 notices, including thomastschinkel, yhay81 and destbreso,
remain in `main.py` with the full license. Credits imply no author endorsement.
The final source, complete raw outcomes and frozen-source confirmation are
documented in `research86/REPORT.md` and `research86/results/release_evidence.json`.


## V39 consolidation — September 13, 2026

Production-calendar feeding, bounded physical wheat replenishment, native-pickup
coverage, stock reservation before saturated market turns and current-liability
funding were developed in Ahmed Berat Özer's Kaggriculture project. V39 selects
the unchanged combined EXP231 source after the requested candidate consolidation.
All earlier credits and Apache-2.0 notices remain in main.py, including
thomastschinkel, yhay81 and destbreso. Credits do not imply endorsement.

The latest public inventory audit covered 485 references. Zhihuan Xue's
Kaggriculture Timed Six Cow was reviewed and retained once as an evaluation
opponent. None of its code was copied into this agent. Results and provenance
are recorded in research100, research101 and research102.
