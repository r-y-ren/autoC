# Kaggriculture V35 — Public-response sales and funded sheep expansion

This notebook builds a complete, self-contained submission agent. The full Python source is embedded in a readable cell. **No attached dataset, donor notebook, internet connection, GPU, training or package installation is required to build the archive.**

Import this notebook into Kaggle and run all cells. The output is `submission_competitive_v35.tar.gz`, containing exactly one file: `main.py`. Download that archive, or select it as the competition submission artifact. The integrity cell verifies that the generated source and archive match the qualified version.

The default run only writes, checks and packages the source. It does not repeat the optimization or the large evaluation campaign. An optional final cell plays four complete games when `RUN_GAME_CHECKS = True` and `kaggle-environments==1.32.7` is available. Each game prints progress. Kaggle's **Queued** status occurs before these cells start; the first cell prints `V35 started` as soon as Python executes.

V35 retains the thirteen-route V34 foundation, worker repairs, protected sales, livestock controller and terminal planner. It adds a revised opening market sequence, a cautious extra sale reservation after a matching public cash response, and a six-sheep expansion financed from observed resources. New workers are assigned only after actual hiring is confirmed. Feed and sale quantities use observed stock and credited harvests.

The evaluation below distinguishes earlier development games, new reacting worlds, strong recorded opponents and historical smoke gates. Local performance is evidence for selecting this release; its live ladder rating has not yet been measured.



## Start the build


## Write the complete agent


## Verify source and entry point


## Build the submission archive


## Optional: run complete games


# V35 independent evaluation — EXP178

Source frozen on September 11, 2026 at 12:20:55 UTC, before selection of the new qualification records. SHA-256: `294e7e4d9d4b97413646960d318043e0f9116ce58f42fe02afd4716614a4e96d`.

Both preregistered competitive gates passed against immutable V34: the paired 95% confidence intervals for outcome points and cash margin have positive lower bounds when resampling whole reacting worlds and whole strong teams. Absolute own cash is reported separately. This release has no measured live ladder rating yet.

## Independent strong recorded opponents

The 12:13 UTC official leaderboard snapshot contained 82 teams rated at least 2800. The first 48 eligible teams contributed eight newest unused completed nonself records each, with focal initial rating at least 2800. Selection used no win/loss filter and excluded our account. All 384 original reward pairs were reproduced exactly. None of the selected episode IDs or world seeds overlaps any earlier cohort.

**These opponents replay recorded actions. They are not the private reactive agents used by those teams on the live ladder.**

|Policy / group|W/L/T|Strict winrate|Mean margin|Mean own cash|
|---|---:|---:|---:|---:|
|V35 candidate|178/206/0|46.35416667%|10959.71875000|103203.95833333|
|V34|131/253/0|34.11458333%|-1599.94531250|95950.64322917|
|V25|88/296/0|22.91666667%|-7414.65885417|93233.96354167|
|Opening30 control|167/217/0|43.48958333%|9996.27343750|102919.13020833|

Margin means final own cash minus final rival cash, averaged over all games. Strict winrate counts only wins; paired outcome points count a tie as one half. No failed game is silently removed.

|Comparison|Outcome change|95% team CI|Margin change|95% team CI|Own cash change|Better / worse outcomes|
|---|---:|---|---:|---|---:|---:|
|V35 vs V34|+12.23958333pp|[+4.94791667, +19.79166667]pp|+12559.66406250|[+6917.66145833, +18821.95833333]|+7253.31510417|66 / 19|
|V35 vs V25|+23.43750000pp|[+16.40625000, +30.46875000]pp|+18374.37760417|[+11564.89583333, +25862.39062500]|+9969.99479167|103 / 13|
|V35 vs Opening30 control|+2.86458333pp|[+1.30208333, +4.94791667]pp|+963.44531250|[+644.84635417, +1310.42187500]|+284.82812500|11 / 0|

## Independent reacting worlds

Thirty-two previously unused worlds (147200001–147200032), 25 fixed policy entries and both seats give 1,600 games per version. The panel contains 24 public policy versions plus our immutable V34 internal control. Its 19 related Shop Router entries form one family; Nagata V6 and V6.2 form one family; four other policies form four separate families. The confidence interval resamples whole worlds, not individual games.

|Policy / group|W/L/T|Strict winrate|Mean margin|Mean own cash|
|---|---:|---:|---:|---:|
|V35 candidate|1507/93/0|94.18750000%|43363.56187500|117881.71750000|
|V34|1277/261/62|79.81250000%|21274.93000000|105505.89375000|
|V25|493/1107/0|30.81250000%|13961.67125000|101427.46625000|
|Opening30 control|1411/189/0|88.18750000%|42347.24375000|117596.32250000|

|Comparison|Outcome change|95% world CI|Margin change|95% world CI|Own cash change|Better / worse outcomes|
|---|---:|---|---:|---|---:|---:|
|V35 vs V34|+12.43750000pp|[+9.93750000, +15.18750000]pp|+22088.63187500|[+20031.57937500, +24076.26812500]|+12375.82375000|230 / 0|
|V35 vs V25|+63.37500000pp|[+60.31250000, +65.93750000]pp|+29401.89062500|[+27108.48312500, +31649.91000000]|+16454.25125000|1014 / 0|
|V35 vs Opening30 control|+6.00000000pp|[+4.12500000, +8.06250000]pp|+1016.31812500|[+641.57687500, +1452.88375000]|+285.39500000|96 / 0|

The equally weighted six-family point difference versus V34 is +3.22094298pp. Every family meets the fixed maximum 10pp regression rule.

### Family results

|Policy / group|W/L/T|Strict winrate|Mean margin|Mean own cash|
|---|---:|---:|---:|---:|
|crop_dusta_v65 — V35|64/0/0|100.00000000%|11799.04687500|96308.46875000|
|king_rc4 — V35|62/2/0|96.87500000%|16512.67187500|102928.95312500|
|melon_v4 — V35|64/0/0|100.00000000%|156596.23437500|175541.31250000|
|nagata_v6 — V35|128/0/0|100.00000000%|104556.21093750|150532.09375000|
|preempt_selector — V35|64/0/0|100.00000000%|121722.84375000|149263.00000000|
|related_shop_routes — V35|1125/91/0|92.51644737%|29912.93832237|111680.89555921|

|Family|Points vs V34|Margin vs V34|Better / worse outcomes|
|---|---:|---:|---:|
|crop_dusta_v65|+3.12500000pp|+644.37500000|2 / 0|
|king_rc4|+0.00000000pp|+624.65625000|0 / 0|
|melon_v4|+0.00000000pp|+2525.92187500|0 / 0|
|nagata_v6|+0.00000000pp|+0.00000000|0 / 0|
|preempt_selector|+0.00000000pp|+385.09375000|0 / 0|
|related_shop_routes|+16.20065789pp|+28843.98684211|228 / 0|

### Both reacting seats

|Policy / group|W/L/T|Strict winrate|Mean margin|Mean own cash|
|---|---:|---:|---:|---:|
|Seat 0 — V35 candidate|754/46/0|94.25000000%|43650.11375000|118274.25750000|
|Seat 0 — V34|642/127/31|80.25000000%|21404.06250000|105618.31375000|
|Seat 0 — V25|247/553/0|30.87500000%|14088.19875000|101566.62625000|
|Seat 0 — Opening30 control|707/93/0|88.37500000%|42587.28625000|117901.62250000|
|Seat 1 — V35 candidate|753/47/0|94.12500000%|43077.01000000|117489.17750000|
|Seat 1 — V34|635/134/31|79.37500000%|21145.79750000|105393.47375000|
|Seat 1 — V25|246/554/0|30.75000000%|13835.14375000|101288.30625000|
|Seat 1 — Opening30 control|704/96/0|88.00000000%|42107.20125000|117291.02250000|

### Reacting opponents

|Policy / group|W/L/T|Strict winrate|Mean margin|Mean own cash|
|---|---:|---:|---:|---:|
|seven_rescue|64/0/0|100.00000000%|78825.50000000|140596.48437500|
|aurax_room|64/0/0|100.00000000%|68216.00000000|137500.56250000|
|thomas955|58/6/0|90.62500000%|6433.85937500|97055.03125000|
|crop_dusta_v65|64/0/0|100.00000000%|11799.04687500|96308.46875000|
|soil_v229|58/6/0|90.62500000%|4416.26562500|96222.09375000|
|market_new|54/10/0|84.37500000%|1907.98437500|94793.81250000|
|king_rc4|62/2/0|96.87500000%|16512.67187500|102928.95312500|
|wheat_q45|64/0/0|100.00000000%|14405.26562500|95088.17187500|
|moon_v226|60/4/0|93.75000000%|4632.70312500|96247.53125000|
|v49_trackp|64/0/0|100.00000000%|78020.29687500|139547.17187500|
|v49_bandit|64/0/0|100.00000000%|74056.37500000|140056.29687500|
|nagata_v6|64/0/0|100.00000000%|103026.93750000|148222.25000000|
|moon_cattle|64/0/0|100.00000000%|4671.48437500|96126.53125000|
|soil_combined|64/0/0|100.00000000%|3822.42187500|95021.48437500|
|flexon_two_coins|60/4/0|93.75000000%|2948.78125000|95398.64062500|
|kaggricult_man|64/0/0|100.00000000%|78837.14062500|140578.01562500|
|melon_v4|64/0/0|100.00000000%|156596.23437500|175541.31250000|
|harvest_nocturne|56/8/0|87.50000000%|2290.84375000|95086.20312500|
|shop0911|25/39/0|39.06250000%|3477.10937500|96548.68750000|
|preempt_selector|64/0/0|100.00000000%|121722.84375000|149263.00000000|
|herd_safe|54/10/0|84.37500000%|1907.98437500|94793.81250000|
|structured_fixed|64/0/0|100.00000000%|88117.26562500|146237.92187500|
|our_v34|64/0/0|100.00000000%|48942.54687500|129952.59375000|
|mirror_counter|60/4/0|93.75000000%|2416.00000000|95085.96875000|
|nagata_v62|64/0/0|100.00000000%|106085.48437500|152841.93750000|

### Strong teams

All 48 selected teams are shown; each has eight paired records.

|Policy / group|W/L/T|Strict winrate|Mean margin|Mean own cash|
|---|---:|---:|---:|---:|
|Majkel1337 — V35|8/0/0|100.00000000%|67373.37500000|143398.50000000|
|SpaTaro — V35|8/0/0|100.00000000%|28555.50000000|115925.62500000|
|feel the agi — V35|6/2/0|75.00000000%|7496.50000000|128605.12500000|
|c0nrad — V35|3/5/0|37.50000000%|-3004.50000000|99775.75000000|
|Otter Vibe — V35|6/2/0|75.00000000%|11173.37500000|106397.12500000|
|Unknown Mother-Goose — V35|5/3/0|62.50000000%|14791.00000000|109029.62500000|
|ymg_aq — V35|5/3/0|62.50000000%|3059.37500000|101559.50000000|
|carlos-tagosaku — V35|4/4/0|50.00000000%|219.75000000|97979.00000000|
|binghua — V35|5/3/0|62.50000000%|911.12500000|95303.37500000|
|Gleb Tumanov — V35|4/4/0|50.00000000%|-1048.62500000|95900.62500000|
|redblackbst — V35|1/7/0|12.50000000%|-4913.75000000|81019.50000000|
|3정훈 — V35|3/5/0|37.50000000%|1736.62500000|108041.75000000|
|mtmr_s1 — V35|5/3/0|62.50000000%|2570.12500000|101026.62500000|
|Mengfei Li — V35|5/3/0|62.50000000%|11205.25000000|101931.37500000|
|charmq — V35|1/7/0|12.50000000%|-2876.25000000|94104.87500000|
|Xiangyu Liu — V35|2/6/0|25.00000000%|-4655.12500000|73632.00000000|
|QQ Farming — V35|3/5/0|37.50000000%|-2929.87500000|95876.62500000|
|american gothic — V35|6/2/0|75.00000000%|41023.00000000|120366.62500000|
|Syed Asad Ali — V35|5/3/0|62.50000000%|37314.62500000|121419.37500000|
|デワンシュ — V35|1/7/0|12.50000000%|-5593.25000000|93990.87500000|
|Subramanya N — V35|1/7/0|12.50000000%|-1496.25000000|81849.62500000|
|薄荷喵呜 — V35|4/4/0|50.00000000%|23557.37500000|97662.37500000|
|Hiểu Vy — V35|2/6/0|25.00000000%|-2506.87500000|108709.62500000|
|Tarang222 — V35|3/5/0|37.50000000%|-834.12500000|108596.87500000|
|que la cuenten como quieran — V35|6/2/0|75.00000000%|5434.25000000|107505.62500000|
|Le Viet — V35|1/7/0|12.50000000%|-2928.62500000|91962.50000000|
|keiz — V35|3/5/0|37.50000000%|-3330.87500000|97197.87500000|
|한밭대학교 — V35|6/2/0|75.00000000%|59854.12500000|133846.50000000|
|Michael Shihong Zhang — V35|6/2/0|75.00000000%|42756.12500000|114326.00000000|
|Terry Luo — V35|4/4/0|50.00000000%|474.00000000|101475.37500000|
|chocolat — V35|2/6/0|25.00000000%|-779.62500000|99315.75000000|
|🌽 High Frequency Farming 🌽 — V35|2/6/0|25.00000000%|-4305.37500000|85970.25000000|
|senkin13 — V35|3/5/0|37.50000000%|307.50000000|104138.12500000|
|datnt114 — V35|2/6/0|25.00000000%|-215.62500000|98751.62500000|
|Suliman Tadros — V35|3/5/0|37.50000000%|3236.25000000|89477.37500000|
|MINGXI LIU — V35|0/8/0|0.00000000%|-1795.37500000|79992.00000000|
|Himanshu Kumar — V35|5/3/0|62.50000000%|45239.37500000|131330.25000000|
|Sergey Kutepov — V35|2/6/0|25.00000000%|-1683.00000000|100430.00000000|
|Bantam — V35|2/6/0|25.00000000%|-1161.37500000|87542.87500000|
|THIRD FARM CLUB — V35|8/0/0|100.00000000%|79183.75000000|141516.50000000|
|tamura_aicon — V35|3/5/0|37.50000000%|-668.87500000|99737.12500000|
|kanno — V35|2/6/0|25.00000000%|1111.37500000|87214.75000000|
|PeriwinkleBlueOvO — V35|4/4/0|50.00000000%|6270.75000000|107805.87500000|
|Jingxiang — V35|6/2/0|75.00000000%|40010.75000000|114581.50000000|
|insuperabilehart — V35|1/7/0|12.50000000%|-1359.62500000|93943.50000000|
|local — V35|4/4/0|50.00000000%|31650.12500000|115169.37500000|
|kitsada — V35|4/4/0|50.00000000%|7006.00000000|96047.87500000|
|Ray Roberts — V35|3/5/0|37.50000000%|632.12500000|92409.00000000|

## Historical gates and execution checks

The historical panels below are consumed regression data. Their high winrates are not substituted for the independent strong-team results above.

|Policy / group|W/L/T|Strict winrate|Mean margin|Mean own cash|
|---|---:|---:|---:|---:|
|Top120, rating>=2900, sample seed3|112/8/0|93.33333333%|19033.90000000|105541.47500000|
|Opp150|145/5/0|96.66666667%|22362.61333333|103434.71333333|
|Arena9 policies, six worlds, both seats|106/2/0|98.14814815%|11894.57407407|98896.98148148|
|Thomas95.5 arena subset|12/0/0|100.00000000%|6604.41666667|93122.08333333|

The official export equals the frozen prototype over 58,958 callbacks in 80 full scenarios. All 13 route IDs are covered. Observations and source routes remain unchanged; the source and embedded modules import only the standard library. Shared-state self-play, separate self-play and starter games all finish DONE.

An instrumented official-engine check covers 62 complete games: 4,559 protected or additional sale-order slots and 23,551 units execute exactly; all 124 bank ledgers reconcile. Every one of the 306 daily expanded-herd checks finds six living, fed sheep. Investment confirmation and delivery telemetry also passes across every new qualification game.

|Timing check, normal GC|Callbacks|Maximum callback, ms|
|---|---:|---:|
|80 isolated scenarios, Windows Python3.13|58958|28.72060001|
|80 isolated scenarios, Linux Python3.12|58958|18.51026100|
|16 slowest new-cohort fixtures, fresh full official Windows games|11504|19.05300000|
|Those16 scenarios replayed in isolated Windows processes|11504|29.82510000|
|Those16 scenarios replayed in isolated Linux processes|11504|19.68489400|

The 50ms gate uses these isolated measurements. Wall-clock callback times in the 24-worker batch can be substantially larger under host contention; those raw times remain in the evaluation receipts. Garbage collection stays enabled. Prior pool-job garbage is collected before each new game, equally for every compared version. No in-game collection is disabled.

## What changed and what was rejected

V35 combines the opening30 sequence on the unchanged thirteen-route foundation, a fourth-turn sale reservation after a matching positive public cash response, and the financed six-sheep southeast controller. It retains confirmed hiring, actual stock accounting, route obligations and the existing tomato/cattle controllers. A sheep commitment also makes the incompatible terminal shadow planner abstain.

The incremental source review covered eight new or updated Code references, excluding our account. Renamed references and byte-identical exports were deduplicated. Mirror Counter and Nagata V6.2 were added as reacting opponents. The Soil sheep capability was already present in a previously reviewed export and is newly integrated into our agent; it is not misrepresented as newly published executable code.

Whole-cohort development tested larger opening quantities, altered initial wheat reserves, inferred market-supply sale windows, alternative routes, and removal of existing production controllers. The selected six-sheep candidate has 197/123/0 over 320 consumed strong records and 388/12/0 over 400 consumed reacting games. It adds four better outcomes and one worse versus the cash-probe parent on the strong development cohort. Removing the tomato investment loses nine outcomes with no improved outcome. Unselected variants are not bundled.

The earlier opening30-only EXP173 failed its original own-cash gate. EXP174 explicitly revised the primary metric to outcome points and relative margin, then still failed its additional strong confidence gate. Those failures remain failures. EXP178 keeps the revised gates unchanged, freezes a modified candidate, and prospectively increases the new strong cohort to 48 teams before collecting or testing its records. No threshold changed after the present results.

## Reproduction and packaging

The project workspace keeps PLAN.md, candidate and opponent hashes, selection timestamps, all raw game rows, original-pair parity, overlap audit, both paired comparisons, family/team/seat rows, market execution and normal-GC timings under research47/. Development and Code provenance are preserved under research44–46/. The complete candidate is in agent/main.py. The official engine used for comparisons is kaggle-environments 1.32.7.

This notebook writes that exact frozen source and builds a deterministic GNU-format tar in gzip, containing only main.py. It verifies both hashes and the final callable selected by Kaggle. Its default five code cells do not train, fetch donors or run full games. The optional last cell runs four official-engine smoke games when enabled. Notebook/archive validation receipts are saved separately by the release workflow. No automatic competition submission is performed.

### Fixed gate receipt

```json
{
  "strong": {
    "strong_team_points_ci_positive": true,
    "strong_team_margin_ci_positive": true,
    "actual_errors_and_delivery_clean": true,
    "original_rewards_match": true,
    "new_records_no_overlap": true
  },
  "reacting": {
    "reacting_world_points_ci_positive": true,
    "reacting_world_margin_ci_positive": true,
    "equal_family_points_nonnegative": true,
    "no_family_regression_over_10pp": true,
    "actual_errors_and_delivery_clean": true
  },
  "technical": {
    "exact_export_and_readonly": true,
    "all13_routes": true,
    "stdlib_only": true,
    "actual_market_herd_and_banks": true,
    "strong_callbacks_and_delivery": true,
    "reacting_callbacks_and_delivery": true,
    "original_windows_runtime": true,
    "original_linux_runtime": true,
    "fresh_fullgame_runtime": true,
    "fresh_windows_runtime": true,
    "fresh_linux_runtime": true,
    "historical_top": true,
    "historical_opp": true,
    "arena": true,
    "thomas": true,
    "original_artifacts_unchanged": true
  }
}
```


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
