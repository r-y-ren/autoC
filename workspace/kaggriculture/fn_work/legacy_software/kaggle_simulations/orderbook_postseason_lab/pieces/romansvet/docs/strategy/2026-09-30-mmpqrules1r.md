Stream: MMPQRULES1R (remote-only)
Date: 2026-09-30 (committed by DOCSYNC1; verbatim S/mmpqrules1r/RULEBOOK.md, companions spec.md, tables.md, timetable.txt, literal_orders.txt)
Verdict: READ - MMPQ rulebook reconstructed: 29 rules exact (FOUND), 17 partial, 5 missing; opponent-independent except the d0 wheat count

# MMPQRULES1R: the MMPQ (rank-1, "M & M & P & Q") rulebook

Written 2026-09-30, remote only (/mnt/e was down). Source: the 243 MMPQV1R live replays (subs 56679033 and 56680759), 241 non-mirror MMPQ seats. Re-extracted per step from raw/: ev.jsonl (orders, money, prices, shed, tile events), feat.pkl (per-day features), ani.jsonl (per-animal fed/cared state at h23).

Conventions:
- (d,h) is the DECISION state: the observation at step 24d+h. Its orders are stored in steps[24d+h+1].action. So "step 246" = d10 h6.
- "h0 of dN" = the observation at step 24N.
- n = 241 unless stated. Every number is mean±sd.
- Status labels. FOUND: sd 0, or sd ≤ 0.3 for counts, in every group with n ≥ 5. PARTIAL: the key cuts sd by 2-5x but the within-group sd stays > 0.3. NOT FOUND: the best correlate is given.
- Keys: yarn = the first day YARN_STORE is in town. Milk shops = PIZZA_SHOP/ICE_CREAM_SHOP/SMOOTHIE_SHOP. Egg shops = BAKERY/BRUNCH_SPOT. For a product P, demand-seq = the number of shops consuming P that are open at d3/d6/d9 (for example "012").
- Classes are V/P48/DSM/PQ4/other, with n = 47/83/39/35/37.

Opponent independence (a16.txt). Adding the rival class to the key barely changes the within-key sd: sheep d10 0.25→0.20, cows d13 0.54→0.46, geese d11 1.78→1.70, strawberry d7 2.11→2.03, melon d9 0.85→0.82, hires d10 0.06→0.06. The largest between-class gap inside a key group is ≤1.3 units, except tomato d11 in group 112 (n 3-4 per class) and carrot. Only one rule depends on the opponent: the d0 wheat count. It is cash-limited through the lockstep wheat price: DSM 12.0±0.0 (n39), V 11.3±0.5 (n47).

---

## 1. LAND (a2.txt, a3.txt, a4.txt)

| rule | literal behaviour | key | result (n, mean±sd) | status |
|---|---|---|---|---|
| 1.1 Q2 (1,000) | d6 h3: SELL WOOL 6; d6 h4: SELL WOOL 6; d6 h6: SELL WOOL 6. BUY_LAND is added at h3 or h4 | none for the day | day d6 in 241/241 (sd 0) | FOUND (day) |
| 1.1b Q2 hour | h3 in 50 games, h4 in 191 | not found | best correlates: sheep at d6 r=-0.59, yarn d3 r=-0.59 (yarn-d3 games are h3 in 27/34), wool price at d6h3 r=-0.56 | NOT FOUND |
| 1.2 Q3 (2,000) | d8 h1: SELL MILK 6. d8 h6: SELL MILK 6 + BUY_LAND (twice in 27+ games). If cash is short: d9 h3 SELL WOOL 4 + BUY_LAND, d9 h4 SELL WOOL 4 + BUY_LAND | **yarn day** | yarn ≥ d9 or never: d8 h6 in 196/196 (sd 0). Yarn d3: d9 in 32/34 (0.94±0.24). Yarn d6: d9 in 18/21 (0.86±0.35) | FOUND (Q3 key = yarn ≤ d6) |
| 1.2b Q3 mechanism | Cash at d8 h6 is 1,485±192 (n189) when Q3 lands on d8, against 713-763 (n50) when it slips. Early-yarn games spent the cash on 7-8 extra sheep (sheep at d8: 10.3±1.0 vs 3.1±0.7) | cash after the sale ≥ 2,000 | 16 games d9 h3, 34 games d9 h4, 2 games d8 h9 | FOUND |
| 1.3 Q4 (4,000) | d10 h6: SELL MELON 6. BUY_LAND is tried from h6/h8. d10 h9: SELL MELON 12 + BUY_LAND | none for the day | d10 in 241/241. Hour h9 189, h10 38, h11 14 | FOUND (day) |
| 1.3b Q4 hour | success at the first step where cash ≥ 4,000 | cash. By milk9 0/1/2/3: 9.71±0.53 / 9.17±0.49 / 9.19±0.58 / 9.00±0.00 | yarn d9 10.07±0.77 | PARTIAL |
| 1.4 retry | a failed BUY_LAND is re-issued at the following steps until it succeeds (d8 h7-h14, d9 h3-h20, d10 h6-h8; attempt table in a4.txt) | cash | - | FOUND |

Funding order on land days: the SELL orders come first, then BUY_LAND (SELL before BUY_LAND 837:0).

## 2. CROPS (a5, a6, a9, a14, scan_crops.txt, scan_snap.txt; per-day tables T2a/T2b below)

| rule | behaviour | key | numbers | status |
|---|---|---|---|---|
| 2.1 melon opening | d0: 6 melon tiles (BUY_SEED MELON 2 at d0 h6/h7/h9-h11) | none | 6.00±0.00 | FOUND |
| 2.2 melon top-up | d1-d3: +4 (seeds 2 per step, d1 h7-h12 and d2 h14). Tiles at h0 d4 | none | 10.0±0.4 (planted d0-3 10.03±0.39, s3s6 wsd 0.29) | FOUND (≤0.4) |
| 2.3 melon wave 2 | d6-8: +2.4. Tiles at h0 d9 | s3s6 | d6-8 2.44±0.82 (s3s6 wsd 0.54); tiles d9 12.5±0.9 | PARTIAL |
| 2.4 melon harvest | every melon tile is cleared at yield 6. The d0 tiles are harvested d10 h3-h7 | none | harvested units: d10 36.0±0.06, d11 13.8±3.0, d12 9.6±3.2, d16 10.0±4.7 (the d6 wave), d18 4.4±7.5 | FOUND (d10) |
| 2.5 melon sales | d10 h6 SELL 6 (96 %, sd 0) = step 246. d10 h9 SELL 12 + BUY_LAND (92 %, lot 11.2±2.0) = step 249. d10 h11 SELL 6 (97 %) = step 251. d10 h12 SELL 6 (63 %) = step 252. d11 h0 7.5±2.6, d11 h11 6. d12 h0 8.8±3.5. d13 h0 8.2±2.9 | none (price-independent: price 272→233 across the steps, lot sd 0) | SELL units per day: d10 29.7±2.9, d11 15.2±4.9, d12 7.3±4.7, d13 7.5±3.8, d16 9.6±4.7, d18 3.1±5.7. The shed is empty after 97 % of melon SELLs. Lots: 6 (2,137 orders), 12 (427) | FOUND |
| 2.6 wheat opening | d0: target 12 wheat tiles, 1 seed per step d0 h10-h21 | cash (opponent-dependent through the wheat price) | d0-1: 11.7±0.5; DSM 12.0±0.0, V 11.3±0.5 | PARTIAL |
| 2.7 early strawberry | d2-5: 6 strawberry tiles (BUY_SEED 1 per step d2 h9/h12, d3 h10-13, d4 h11-13) | none | 6.29±0.81 (class means 6.2-6.6) | PARTIAL (sd 0.8) |
| 2.8 strawberry d6 wave | d6 h6-h19: 1-2 seeds per step, planted the same day | **strawberry-demand shops at d3,d6** (and yarn: early yarn gives fewer) | d6 plantings 00: 6.1±2.1 (n48), 01: 14.9±2.3 (60), 11: 16.5±2.0 (72), 12: 20.3±1.3 (61). Tiles at h0 d7 12.2/21.1/22.8/26.7. s3s6 wsd 1.06 | PARTIAL |
| 2.9 strawberry d7-11 | top-up keyed on strawberry demand at d9 | sdem369 | 000 1.2±1.9, 012 6.8±4.3, 123 12.7±3.4 | PARTIAL |
| 2.10 strawberry d12-13 + d15 | refills of freed tiles | not found | d12-13 4.3±3.5, d15 2.1±2.0. No shop key (sdem369 wsd 3.4 / 2.0) | NOT FOUND |
| 2.11 strawberry total | d2-18 plantings scale with strawberry demand at d9 (0/1/2/3 shops) | dem@d9 | 19.1±2.9 / 28.7±3.9 / 37.1±4.7 / 47.0±5.3 | PARTIAL (≈ +9.3 tiles per demanding shop) |
| 2.12 tomato | first tomatoes d8 h13-17. Main block d8-10 (BUY_SEED TOMATO 1 per step d10 h11-18). Second block d15-19 | tomato demand-seq | d8-10: 000 4.4±2.9 (99), 001 8.4±3.1, 011 9.1±3.0, 111 9.6±2.3, 012 14.8±1.8, 112 17.6±3.6, 122 17.6±2.2. d8-21 by dem@d21 0→9.9, 5→35.2 | PARTIAL |
| 2.13 carrot | none unless a carrot shop (PET_CAFE / FARMERS_MARKET) is open. Carrot plantings are back-loaded d19-27 | carrot demand | d8-14 by dem@d9 0/1/2/3: 0.4/7.6/26.4/45.0. d19-28 by dem@d28 0→4.1, 3→42.4, 6→77.8 | PARTIAL |
| 2.14 wheat = filler | every free tile is replanted the day it frees. Demand crops take their share and wheat takes the rest | structural | crops+structures at h0: d12 97.9±2.1, d14 99.1±1.3, d18 97.9±2.2 of 100. Wheat vs other crops slope -0.65..-0.71. Wheat plantings d10-14 13.0±3.5 / 11.8±3.3 / 7.2±3.1 / 7.9±2.7 / 8.2±2.7 (no shop key, s3s6 wsd 2.1-2.6) | FOUND (rule), NOT FOUND (per-day counts) |
| 2.15 end of planting | the last plantings are on d27 (wheat 3.5, carrot 2.2). d28-29: none. Empty tiles at h0 rise 7.9 d27 → 19.4 d28 → 38.8 d29 | none | d28 plantings 0.0±0.1 | FOUND |

## 3. LABOUR (scan_lab.txt, a15.txt, a17.txt; table T3)

| rule | behaviour | numbers | status |
|---|---|---|---|
| 3.1 hand schedule | hands per day: d0 4, d1 3.5±0.6, d2 5.1±0.4, d3 6, d4 6, d5 5.6±0.5, d6 9.0±0.2, d7 7.7±0.5, d8 9.1±0.5, d9 10.2±0.5, **d10 12.0±0.06 (240/241 = 12)**, d11-14 11.5-11.6±0.5, d15-22 12.2-12.6±0.5, d23-26 12.0±0.3, d27 11.7±0.5, d28 10.9±0.8, d29 9.7±1.2 | d0/d3/d4/d10: FOUND (sd 0 / 0.06) |
| 3.1b why 12, ±1 | from d10: 12 in 66 % of days, 11 in 18 %, 13 in 13 %. Best correlates are weak: animals r≈0.5 at d12-14, crop+animal r 0.65 at d28 (the ramp-down) | NOT FOUND (±1) |
| 3.2 hire placement | HIRE orders come right after the dawn SELLs at h0. The h0 list is filled to exactly **10 orders** (the maxMarketOrdersPerTurn cap) in 91 % of d6-28 days. The remaining hires go at h1 (d10: 9 at h0 + 3 at h1; d11-14: 8 + 3.5) | FOUND |
| 3.3 fertiliser | d0-9: every collected unit is SOLD (1-2 per order, all day). From d10: FERTILIZE per day 3.7 (d10), 6.0, 9.8, 10.2, 8.8, 21.1 (d15), 10-19 (d16-21), 13-17 (d22-28). Dawn dump SELL FERTILIZER at h0 d10-13: 8.5 / 13.3 / 13.6 / 10.2. COLLECT_FERTILIZER 22/day d11-19 | FOUND (d0-9 sell rule); per-day FERTILIZE counts PARTIAL |
| 3.4 water | WATER actions per day 41-67 over d8-27 (sd 3-9). No tile dies before d19 (weeds at h0 ≤0.4 until d19, then 1-8) | PARTIAL |
| 3.5 idle | PASS unit-actions per day: d1 39, d3-5 28-35, d6-9 3-13, **d10-28 0.4-1.5**, d29 18.9 | FOUND (d10-28 ≈ 0) |

## 4. ANIMALS (a7, a11, a12, a13; table T4)

| rule | behaviour | key | numbers | status |
|---|---|---|---|---|
| 4.1 opening herd | d0 h0 BUY_ANIMAL COW 1. d0 h1 COW 1 + SHEEP 3. d2 h6/h8: COW +1 | none | h0 d3: cows 3.00±0.00, sheep 3.00±0.00 | FOUND |
| 4.2 sheep | buys start on the YARN_STORE unlock day and are spread over that day and the next ~2 days (yarn d3: +1 d3, +1 d4, +1.4 d5, +4.0 d6; yarn d6: +4.4 d6, +0.9 d7, +2.1 d8; yarn d9: +3.4 d9, +3.1 d10; yarn d12: +4.9±0.2 d12; yarn d15: +2.6 d15; yarn d18: +1.9 d18). No yarn by d18: 3 sheep all game | **yarn unlock sequence** d3/6/9/12 | h0 d10: 000 3.0±0.0 (159), 001 5.8±0.6 (27), 011 9.9±0.2 (18), 111 11.1±0.4 (26), 112 16.5±0.5 (6). h0 d13: 0001 7.9±0.2 (17), 0011 8.8±0.6 (25), 0111 9.9±0.2, 1111 11.1±0.4, 1122 16.6±0.5. Pooled within-key sd 0.25 | FOUND (wsd 0.25; the largest group sd is 0.6) |
| 4.3 cows | buys on milk-shop unlock days and on d2-5 (+2 when a milk shop opens at d3). Last cow buys ~d12 | milk-shop sequence d3/6/9(/12) | h0 d10: 000 4.6±0.8 (49), 001 6.3±0.6 (38), 011 7.2±0.7 (38), 012 9.8±0.8 (32), 111 8.3±0.7 (26), 112 10.0±0.6 (22), 122 11.1±0.5 (21), 123 14.2±0.4 (15). Within-key sd 0.54-0.67 | PARTIAL |
| 4.4 geese | first coop and geese d6. Buys d8 h8-9, d9, and **d10 h7 right after the melon sale** (74 % of games). None after d11 | the herd budget: geese fill it | geese at h0 d11 = 13.0 - 0.46·(cows+sheep) + 1.74·egg9, residual sd 0.85. The full d3/d6/d9 draw: wsd 0.29. Egg-sequence alone: wsd 1.78 | PARTIAL (FOUND given the full draw to d9) |
| 4.5 purchase hour | first BUY_ANIMAL hour on unlock days is spread h0-h9 (sheep: h0 46, h1 16, h3 21, h8 24). Orders repeat until the shed or cash allows | best correlate: pasture/coop completion (just-in-time) | - | NOT FOUND |
| 4.6 herd cap | total animals at h0 d13 22.2±2.5 (= pasture+coop tiles). Cows+sheep+geese at d11 21.6±2.1, flat across egg9 groups (21.3-22.0) | ≈ 22 animals | - | PARTIAL |
| 4.7 feeding | every animal is fed and cared on its **production eve** (the day before a yield day). Other days only when labour allows, and this falls over the game | species × production eve | P(fed \| production eve): cows 1.00 / 0.99 / 0.96 (d0-9 / d10-17 / d18-26), geese 0.99 / 0.91 / 0.83, sheep 1.00 / 0.94 / 0.85. P(fed \| not eve): cows 0.67 / 0.67 / 0.39 (strict alternation "010101" by d18), sheep 0.99 / 0.84 / 0.68. CARE follows FEED | FOUND (production eve), PARTIAL (off days) |
| 4.8 shedding | nothing is sold; animals are let go by not feeding them. Sheep feeding stops d27 (P(fed) 0.12 d27, 0.04 d28), so they escape at the end of d28. Cows are fed only on production eve at d28 (0.82), non-eve 0.00. Geese P(fed) 0.47 at d28. Nobody is fed d29; CARE stops d28 | day | sheep lost d28 3.4±3.5. Sheep h0 d29 0.5±1.2 (d18 6.1). Cows d29 6.4 (d18 8.3). Geese d29 7.1 (d28 7.7) | FOUND (days) |

## 5. SALES (a8.txt, timetable.txt; table T5)

| rule | behaviour | numbers | status |
|---|---|---|---|
| 5.1 fixed-lot schedule d0-d12 | d0 h1/h2/h3/h5 SELL WHEAT 1. d1-9 SELL FERTILIZER 1 per collected unit. d3 h1 WHEAT 6.1±1.5 and d4 h0 WHEAT 6.7±2.0 (the first harvest). **WOOL 6 at d6 h3, h4, h6** (241/241, sd 0). **MILK 6 at d8 h1 and h6** (241/241, sd 0.1). **WOOL 4 at d9 h3, h4, h6** (241/241, 241, 219). **MILK 3 at d10 h3 or h4**. Melon per rule 2.5. WOOL 4 at d12 h3 (185/241) | FOUND (sd 0) |
| 5.2 no price gate | in the fixed steps price varies and lot does not: wool d9 h6 price 135±47, lot 4.0±0.1; milk d8 h6 price 182±26, lot 6.0±0.1; melon d10 h11 price 240±5, lot 6.1±0.6. From d11 the lot is what is in hand: corr(stock before, lot) 0.5-0.99, corr(price, lot) mostly \|r\| < 0.25 (range -0.35..+0.6) | FOUND: lot depends on stock, not price |
| 5.3 cadence | MILK, WOOL and STRAWBERRY are sold every 4 hours at h1/5/9/13/17/21 (strawberry orders at h5/h9/h13/h17/h21: 1,819 / 1,975 / 2,272 / 1,972 / 2,059). WHEAT, CARROT, TOMATO and EGG are sold at dusk h22-23 (wheat h22 3,401 orders) and at dawn h0-2. FERTILIZER is sold all day plus h0/h2/h22. MELON at h0, h6, h9, h11 | FOUND (hours) |
| 5.4 hold | the shed is empty after the step for: melon 97 %, tomato 61 %, fertilizer 59 %, carrot 49 %, milk 46 %, egg 37 %, wheat 35 %, wool 35 %, strawberry 32 % of SELL orders. Units left after a sale: 0.2-6.3 (the dusk h23 sale leaves 9-19 crop units that are sold at dawn h0-1) | PARTIAL (no hold threshold found) |

## 6. ORDER (a10.txt, a17.txt, literal_orders.txt)

| rule | literal list | n | status |
|---|---|---|---|
| 6.1 d0 h0 | `[BUY_ANIMAL COW 1, BUY_PRODUCT WHEAT 5]` | 241/241 | FOUND |
| 6.2 d0 h1 | `[SELL WHEAT 1, HIRE, HIRE, HIRE, HIRE, BUY_ANIMAL COW 1, BUY_ANIMAL SHEEP 3]` | 241/241 | FOUND |
| 6.3 d0 h2-h7 | h2 `[SELL WHEAT 1]`; h3 `[SELL WHEAT 1, BUY_PRODUCT WHEAT 1]`; h4 `[BUY_PRODUCT WHEAT 1]`; h5 `[SELL WHEAT 1, BUY_PRODUCT WHEAT 1]` (92 %); h6 `[BUY_SEED MELON 2, BUY_PRODUCT WHEAT 1]` (92 %, seed first 222/241); h7 `[BUY_SEED MELON 2]` | 100 % / 92 % | FOUND |
| 6.4 d1 h0 / h2 | h0 `[HIRE ×4]` (87 %); h2 `[SELL FERTILIZER 1, BUY_PRODUCT WHEAT 2, BUY_PRODUCT WHEAT 2]` (45 %) or with one wheat (43 %) | | FOUND |
| 6.5 type precedence in every step | **SELL → HIRE → BUY_ANIMAL → BUY_LAND → BUY_SEED → BUY_PRODUCT**. Counts (before : after): SELL<BUY_SEED 15,059:0, SELL<HIRE 10,938:64, SELL<BUY_ANIMAL 3,105:0, SELL<BUY_PRODUCT 2,892:3, HIRE<BUY_ANIMAL 299:3, HIRE<BUY_PRODUCT 1,633:23, BUY_ANIMAL<BUY_PRODUCT 318:1, BUY_ANIMAL<BUY_SEED 1,437:0, BUY_LAND<BUY_PRODUCT 33:0, BUY_LAND<BUY_SEED 37:0. BUY_SEED<BUY_PRODUCT 270:81 (seed first on d0 h6 222/241 and d1 h9; product first only on d6 h5-h16) | 241 games | FOUND |
| 6.6 SELL product order | FERTILIZER last (after wheat 2,886:63, milk 1,063:14, strawberry 985:18). MELON before WHEAT 59:2. MILK before STRAWBERRY 1,660:727. CARROT before WHEAT 1,018:343. EGG vs WHEAT mixed 1,002:1,238 | | PARTIAL (fert-last FOUND) |
| 6.7 typical day d10+ | h0 = `[SELL dawn lots (melon / strawberry / milk / wool / wheat / carrot / tomato), SELL FERTILIZER, HIRE × (10 − #SELL)]` = 10 orders. h1 = `[SELL milk / wool / egg / wheat, HIRE × (12 − h0 hires), BUY_PRODUCT WHEAT ×1-2 (feed)]`. Examples: d8 h0 `[SELL FERTILIZER, HIRE ×8, BUY_PRODUCT WHEAT]` (75 %); d10 h0 `[SELL FERTILIZER, HIRE ×9]` (100 %); d10 h1 `[HIRE ×3, BUY_PRODUCT WHEAT, BUY_PRODUCT WHEAT]` (44 %) | | FOUND (shape) |
| 6.8 seeds | seeds are bought just in time: 1-2 per step, in the step before the hand plants, all day (h6-h21). Never a bulk seed order | | FOUND |

---

## Rules NOT found (best correlate)

1. Q2 hour h3 vs h4 (50/191): sheep at d6 r = -0.59, yarn-d3 r = -0.59, wool price d6h3 r = -0.56.
2. Q4 hour h9/h10/h11: cash (milk9 = 0 → 9.71, milk9 = 3 → 9.00±0; yarn d9 → 10.07).
3. Exact d0 wheat count (11.7±0.5): cash through the lockstep wheat price; opponent class DSM 12.0 vs V 11.3.
4. Strawberry d12-13 (4.3±3.5) and d15 (2.1±2.0): no shop key. These are refills of freed tiles (melon cleared d10-12).
5. Per-day wheat counts after d10 (the filler residual): s3s6 wsd 2.1-3.7.
6. Exact tomato and carrot counts: demand-seq keys leave sd 2-4 (tomato) and 7-14 (carrot). Class adds nothing.
7. Cows ±0.5-0.8 within the milk sequence. Geese ±1.8 within the egg sequence (fit with cows+sheep: resid 0.85).
8. Animal purchase HOUR: spread h0-h9, just-in-time with pasture/coop builds.
9. Hires ±1 around 12 on d11-27: animals r ≈ 0.5 (d12-14); crop+animal r 0.65 at d28.
10. Off-eve feeding share (cows 0.67 → 0.39, sheep 0.84 → 0.68): labour-limited.
11. Sale hold threshold at dusk (units left 9-19 at h23): stock, not price.

Tally (table rows): FOUND 29, PARTIAL 17, NOT FOUND 5 rows. The NOT-FOUND list above has 11 items because it also names the unresolved parts of PARTIAL rows.

## Builder notes (what a copy must implement, in priority order)
1. Order shape: SELL → HIRE (fill h0 to 10 orders, the rest at h1, 12 hands from d10) → BUY_ANIMAL → BUY_LAND → BUY_SEED → BUY_PRODUCT.
2. Fixed early lots: wool 6 ×3 on d6, milk 6 ×2 on d8, wool 4 ×3 on d9, melon 6/12/6/6 on d10 h6/h9/h11/h12. Land on d6 / d8 (d9 if yarn ≤ d6) / d10, each sale followed by BUY_LAND, retried until it succeeds.
3. Herd by shop sequence: sheep by the yarn sequence (sd 0.25), cows by the milk sequence, geese fill up to ~22 animals. No buys after d12. Stop feeding sheep d27; feed only production eves d28; no feeding d29.
4. Land: melon 6+4 by d3 and +2.4 on d6-8. Strawberry about 6 + 9.3 per strawberry-demand shop. Tomato and carrot by demand. Wheat fills every other free tile. No plantings after d27.
5. Sales: milk, wool and strawberry every 4 h at h1/5/9/13/17/21. Crops and eggs at dusk h22-23 and dawn. Lot = stock in hand; no price gate.

## Spec: state a copy must hit at h0 of d9 / d14 / d17 / d20 / d29, per shop-draw group (money at h0; tiles t = tile stock; cum = units sold before that day, from MMPQV1R all.jsonl)

### Spec by YARN_STORE unlock day (21 = d21 or never)

| group | day | n | money | Q | hires | sheep | cow | goose | wheat t | straw t | tomato t | carrot t | melon t | cum melon | cum straw | cum milk | cum wool | cum egg | cum wheat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| yarn d12 | d9 | 17 | 235.4±162.4 | 3.0±0.0 | 9.9±0.3 | 3.0±0.0 | 7.1±1.9 | 5.1±2.2 | 13.5±2.7 | 25.5±4.8 | 3.0±2.5 | 0.0±0.0 | 12.3±0.7 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 21.3±3.2 |
| yarn d12 | d14 | 17 | 12686.5±1932.6 | 4.0±0.0 | 11.7±0.5 | 7.9±0.2 | 8.1±2.2 | 9.4±2.7 | 28.1±4.2 | 30.2±4.6 | 11.1±6.0 | 2.1±5.2 | 2.3±0.7 | 59.5±1.4 | 1.1±1.6 | 44.2±3.9 | 30.2±0.9 | 18.4±12.8 | 70.5±16.4 |
| yarn d12 | d17 | 17 | 32877.7±3344.4 | 4.0±0.0 | 12.4±0.5 | 8.2±1.0 | 8.0±2.2 | 9.4±2.7 | 20.9±5.1 | 34.5±6.6 | 14.4±6.8 | 1.5±4.0 | 0.5±0.8 | 70.5±4.5 | 42.9±7.7 | 72.7±21.2 | 47.4±4.0 | 65.9±26.5 | 132.4±23.7 |
| yarn d12 | d20 | 17 | 55983.4±4515.1 | 4.0±0.0 | 12.4±0.5 | 8.2±1.0 | 7.6±2.0 | 9.4±2.7 | 21.6±5.1 | 29.8±7.8 | 15.9±7.2 | 2.7±6.2 | 0.0±0.0 | 73.6±3.9 | 108.1±16.8 | 91.0±28.9 | 81.7±7.6 | 111.1±40.6 | 183.7±29.7 |
| yarn d12 | d29 | 17 | 104683.2±14272.4 | 4.0±0.0 | 10.4±0.9 | 0.1±0.2 | 5.1±3.0 | 8.4±2.7 | 13.8±6.4 | 5.2±3.2 | 3.7±2.5 | 9.5±5.7 | 0.0±0.0 | 73.6±3.9 | 225.9±46.8 | 164.0±56.8 | 159.2±21.9 | 234.2±77.0 | 474.9±75.1 |
| yarn d15 | d9 | 10 | 250.3±205.7 | 3.0±0.0 | 9.7±0.5 | 3.0±0.0 | 7.7±2.3 | 4.7±2.3 | 14.0±3.1 | 24.8±5.3 | 2.6±2.1 | 0.0±0.0 | 12.7±1.1 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 22.6±2.3 |
| yarn d15 | d14 | 10 | 16338.0±1547.4 | 4.0±0.0 | 11.5±0.5 | 3.0±0.0 | 8.6±2.9 | 9.2±2.6 | 29.8±7.2 | 30.9±5.6 | 8.6±4.9 | 6.2±8.8 | 2.8±1.0 | 58.1±4.7 | 1.1±0.8 | 45.3±5.8 | 34.2±1.9 | 21.2±15.1 | 81.6±16.5 |
| yarn d15 | d17 | 10 | 34780.7±4896.4 | 4.0±0.0 | 12.4±0.5 | 5.6±0.9 | 8.3±3.3 | 9.2±2.6 | 23.7±5.4 | 31.9±6.0 | 12.4±3.3 | 4.1±4.8 | 1.3±1.7 | 67.1±8.8 | 41.5±10.9 | 78.6±28.1 | 36.8±2.0 | 65.3±26.6 | 160.1±51.7 |
| yarn d15 | d20 | 10 | 55045.7±10979.2 | 4.0±0.0 | 12.5±0.5 | 6.2±2.1 | 8.2±3.3 | 9.1±2.7 | 18.9±7.0 | 27.7±6.2 | 16.0±4.2 | 9.5±9.5 | 0.0±0.0 | 76.1±6.7 | 103.3±21.6 | 107.5±44.4 | 51.2±7.0 | 108.6±40.6 | 209.3±62.4 |
| yarn d15 | d29 | 10 | 106690.2±22395.0 | 4.0±0.0 | 9.1±3.1 | 0.0±0.0 | 6.0±3.8 | 7.3±3.6 | 17.3±8.4 | 5.2±4.5 | 4.8±2.9 | 7.2±5.5 | 0.0±0.0 | 76.1±6.7 | 216.1±54.5 | 199.3±88.2 | 129.6±19.7 | 240.5±83.4 | 461.4±105.8 |
| yarn d18 | d9 | 15 | 209.9±139.7 | 3.0±0.0 | 10.0±0.0 | 3.0±0.0 | 7.5±2.3 | 4.9±2.5 | 14.0±3.1 | 25.1±3.8 | 2.5±1.9 | 0.0±0.0 | 12.7±0.9 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 21.0±2.6 |
| yarn d18 | d14 | 15 | 16388.4±2305.8 | 4.0±0.0 | 11.5±0.5 | 3.0±0.0 | 8.5±2.6 | 9.2±2.5 | 29.7±4.3 | 31.2±4.3 | 9.4±5.4 | 5.5±7.4 | 2.7±0.9 | 60.0±0.0 | 0.7±0.9 | 47.3±8.5 | 35.5±1.6 | 18.9±14.2 | 74.8±15.1 |
| yarn d18 | d17 | 15 | 35494.7±3903.7 | 4.0±0.0 | 12.1±0.2 | 3.0±0.0 | 8.5±2.6 | 9.2±2.5 | 22.2±6.1 | 33.0±5.3 | 15.1±6.2 | 5.3±7.3 | 1.3±1.3 | 68.8±6.1 | 42.7±7.0 | 78.3±24.3 | 39.3±1.9 | 70.6±28.9 | 150.5±33.8 |
| yarn d18 | d20 | 15 | 53512.8±7364.3 | 4.0±0.0 | 12.2±0.5 | 4.9±0.2 | 7.9±3.0 | 9.2±2.5 | 20.5±7.4 | 27.9±7.2 | 16.9±6.8 | 8.1±10.0 | 0.0±0.0 | 76.4±5.6 | 106.8±13.6 | 101.5±40.5 | 42.1±3.4 | 115.6±42.5 | 211.8±46.6 |
| yarn d18 | d29 | 15 | 98773.1±15368.4 | 4.0±0.0 | 9.8±1.0 | 0.0±0.0 | 5.9±3.8 | 7.9±2.7 | 13.5±5.1 | 5.7±4.5 | 3.8±2.3 | 9.6±3.8 | 0.0±0.0 | 76.4±5.6 | 216.5±51.0 | 177.2±81.1 | 99.1±5.2 | 250.1±80.6 | 467.3±108.8 |
| yarn d21 | d9 | 117 | 192.0±160.8 | 3.0±0.0 | 9.9±0.3 | 3.0±0.0 | 7.7±2.3 | 4.7±2.7 | 13.8±3.3 | 24.3±5.7 | 3.2±2.6 | 0.2±1.3 | 12.6±0.9 | 0.0±0.0 | 0.0±0.0 | 12.0±0.1 | 18.0±0.0 | 0.0±0.0 | 21.1±2.7 |
| yarn d21 | d14 | 117 | 16345.6±2057.8 | 4.0±0.0 | 11.5±0.6 | 3.0±0.0 | 9.0±2.7 | 8.8±2.5 | 28.2±6.5 | 31.7±8.1 | 11.4±6.4 | 4.8±8.5 | 2.6±0.9 | 59.7±1.7 | 0.8±0.9 | 46.1±5.8 | 35.0±1.7 | 19.9±15.3 | 77.0±20.1 |
| yarn d21 | d17 | 117 | 35389.9±3932.6 | 4.0±0.0 | 12.1±0.4 | 3.0±0.0 | 9.0±2.7 | 8.8±2.5 | 21.1±6.1 | 35.4±8.6 | 15.7±7.6 | 4.4±7.0 | 1.0±1.3 | 69.6±5.5 | 39.4±8.6 | 83.1±25.3 | 38.7±2.5 | 66.3±29.0 | 157.8±34.0 |
| yarn d21 | d20 | 117 | 54975.2±8124.8 | 4.0±0.0 | 12.1±0.6 | 3.0±0.1 | 8.7±2.9 | 8.7±2.5 | 19.8±6.8 | 31.5±9.8 | 17.5±7.6 | 6.8±9.8 | 0.0±0.2 | 75.8±5.1 | 101.8±21.8 | 108.7±37.2 | 40.4±3.5 | 112.8±41.8 | 212.0±45.9 |
| yarn d21 | d29 | 117 | 104911.4±21424.2 | 4.0±0.0 | 9.6±1.1 | 0.0±0.1 | 7.3±3.7 | 8.0±2.7 | 13.6±6.3 | 7.7±4.4 | 4.3±3.4 | 8.6±6.0 | 0.0±0.0 | 76.0±5.2 | 238.6±72.5 | 206.2±77.7 | 48.7±10.0 | 251.2±85.5 | 492.1±98.7 |
| yarn d3 | d9 | 34 | 1238.8±417.6 | 2.1±0.2 | 11.1±0.2 | 11.3±1.2 | 4.2±1.6 | 1.2±1.5 | 5.1±4.8 | 16.6±4.5 | 0.1±0.5 | 0.0±0.0 | 12.0±0.5 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 29.0±7.5 |
| yarn d3 | d14 | 34 | 22880.8±1912.4 | 4.0±0.0 | 11.8±0.5 | 12.5±2.6 | 6.9±2.6 | 5.6±1.6 | 30.9±5.2 | 25.6±7.2 | 11.2±4.3 | 3.4±5.8 | 2.0±0.5 | 59.8±1.0 | 0.2±0.6 | 31.9±1.9 | 87.0±6.4 | 3.4±4.4 | 70.5±18.0 |
| yarn d3 | d17 | 34 | 44467.0±4277.2 | 4.0±0.0 | 12.4±0.5 | 12.2±2.8 | 7.0±2.6 | 5.6±1.6 | 25.9±5.0 | 27.7±7.7 | 14.6±5.7 | 3.3±5.4 | 0.1±0.6 | 71.1±2.9 | 25.0±7.2 | 51.4±13.3 | 136.2±18.6 | 27.8±13.0 | 154.6±27.7 |
| yarn d3 | d20 | 34 | 63982.9±7061.9 | 4.0±0.0 | 12.4±0.5 | 11.4±3.3 | 6.8±2.7 | 5.6±1.6 | 23.3±5.9 | 24.2±8.4 | 18.4±6.4 | 5.1±7.0 | 0.0±0.2 | 72.1±3.1 | 73.1±23.1 | 75.0±30.7 | 171.2±32.6 | 57.3±20.0 | 218.3±38.2 |
| yarn d3 | d29 | 34 | 111198.0±14109.7 | 4.0±0.0 | 9.7±0.7 | 1.3±1.5 | 5.2±3.2 | 5.3±1.7 | 19.0±7.1 | 6.2±4.0 | 3.6±2.5 | 6.8±5.7 | 0.0±0.0 | 72.5±3.7 | 176.0±64.1 | 144.1±69.4 | 278.3±73.3 | 146.2±48.5 | 479.3±81.0 |
| yarn d6 | d9 | 21 | 867.3±417.9 | 2.1±0.3 | 10.8±0.4 | 9.7±0.7 | 5.8±1.0 | 0.9±1.3 | 6.0±7.6 | 17.6±5.0 | 0.6±1.5 | 0.0±0.0 | 11.9±0.6 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 26.5±6.3 |
| yarn d6 | d14 | 21 | 19533.2±2867.7 | 4.0±0.0 | 11.8±0.4 | 11.0±2.1 | 7.5±2.3 | 5.7±2.4 | 32.9±5.1 | 26.2±7.8 | 11.0±6.1 | 1.9±4.1 | 2.2±1.1 | 59.1±2.1 | 0.6±0.8 | 44.0±7.0 | 65.0±7.3 | 2.4±3.8 | 71.9±28.3 |
| yarn d6 | d17 | 21 | 40807.3±5165.0 | 4.0±0.0 | 12.2±0.4 | 10.8±2.2 | 7.5±2.4 | 5.6±2.4 | 25.8±5.8 | 28.6±9.2 | 15.0±8.2 | 2.9±5.5 | 0.4±1.3 | 70.2±5.0 | 28.8±8.6 | 65.6±20.4 | 109.7±16.0 | 25.9±16.8 | 168.1±39.7 |
| yarn d6 | d20 | 21 | 58790.9±9236.1 | 4.0±0.0 | 12.3±0.5 | 10.6±2.8 | 7.3±2.6 | 5.5±2.4 | 24.3±6.3 | 24.9±9.9 | 17.7±8.1 | 3.9±5.3 | 0.3±0.9 | 71.4±3.7 | 76.9±23.7 | 87.9±32.7 | 137.1±24.0 | 58.4±30.9 | 234.1±49.8 |
| yarn d6 | d29 | 21 | 103234.4±12850.6 | 4.0±0.0 | 9.5±1.1 | 1.4±1.8 | 4.9±3.2 | 5.5±2.4 | 19.9±6.6 | 7.0±4.3 | 3.2±2.5 | 5.3±5.2 | 0.0±0.0 | 73.0±5.5 | 187.7±72.9 | 161.9±65.0 | 236.8±54.9 | 152.1±73.6 | 531.9±103.6 |
| yarn d9 | d9 | 27 | 186.4±126.7 | 3.0±0.0 | 10.0±0.0 | 3.0±0.0 | 7.9±2.1 | 4.8±2.6 | 13.8±4.0 | 23.8±6.0 | 3.3±2.7 | 0.9±4.3 | 12.6±0.9 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 21.8±2.8 |
| yarn d9 | d14 | 27 | 15227.3±2428.4 | 4.0±0.0 | 11.9±0.3 | 9.2±1.6 | 7.9±2.2 | 6.1±1.9 | 30.4±4.5 | 28.2±7.2 | 9.9±5.0 | 4.6±6.6 | 2.6±0.9 | 59.5±1.6 | 0.7±0.9 | 45.5±7.1 | 36.6±3.6 | 17.3±14.2 | 72.3±17.1 |
| yarn d9 | d17 | 27 | 39395.9±4677.9 | 4.0±0.0 | 12.4±0.6 | 9.5±1.8 | 7.7±2.3 | 6.1±1.9 | 24.1±4.5 | 30.4±8.1 | 14.5±5.6 | 3.4±4.7 | 1.0±1.6 | 69.5±6.2 | 39.6±9.8 | 79.2±27.2 | 79.3±5.5 | 48.1±25.5 | 156.4±30.6 |
| yarn d9 | d20 | 27 | 57307.8±9033.7 | 4.0±0.0 | 12.0±0.4 | 9.9±2.6 | 7.4±2.6 | 6.0±2.0 | 21.7±7.0 | 25.9±9.2 | 16.2±5.1 | 7.0±7.8 | 0.0±0.0 | 75.6±5.5 | 93.6±26.6 | 97.9±35.0 | 107.9±11.8 | 77.3±34.5 | 218.5±38.6 |
| yarn d9 | d29 | 27 | 102673.1±18841.5 | 4.0±0.0 | 9.6±0.9 | 1.8±1.6 | 6.6±2.5 | 5.6±2.2 | 16.8±6.9 | 6.0±3.6 | 4.3±2.8 | 7.7±5.1 | 0.0±0.0 | 75.6±5.5 | 199.3±67.8 | 180.5±61.2 | 198.3±47.5 | 170.3±66.2 | 492.4±82.3 |

### Spec by milk shops open at d9

| group | day | n | money | Q | hires | sheep | cow | goose | wheat t | straw t | tomato t | carrot t | melon t | cum melon | cum straw | cum milk | cum wool | cum egg | cum wheat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| milk9=0 | d9 | 49 | 582.6±578.9 | 2.6±0.5 | 10.3±0.6 | 6.1±4.0 | 4.5±0.9 | 5.2±2.9 | 11.7±6.2 | 20.2±6.4 | 2.0±2.3 | 0.5±3.3 | 12.4±0.7 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 25.0±6.2 |
| milk9=0 | d14 | 49 | 16757.5±4414.6 | 4.0±0.0 | 11.5±0.6 | 8.0±4.9 | 4.8±0.6 | 9.6±2.8 | 29.7±6.5 | 26.8±7.1 | 10.3±4.6 | 7.0±8.3 | 2.2±0.6 | 59.8±1.9 | 0.9±0.9 | 36.1±4.4 | 53.4±24.4 | 24.1±17.2 | 80.7±22.8 |
| milk9=0 | d17 | 49 | 35728.3±6683.6 | 4.0±0.0 | 12.2±0.5 | 8.2±4.7 | 4.7±0.8 | 9.6±2.8 | 24.3±6.0 | 29.2±8.9 | 14.7±5.7 | 5.7±7.0 | 0.4±0.9 | 71.5±5.0 | 37.3±12.5 | 42.1±5.1 | 82.1±47.0 | 73.7±30.9 | 165.1±46.5 |
| milk9=0 | d20 | 49 | 51787.6±7989.8 | 4.0±0.0 | 12.1±0.5 | 7.9±4.4 | 4.3±1.3 | 9.6±2.8 | 22.7±7.9 | 24.7±9.7 | 16.8±6.7 | 9.0±10.3 | 0.0±0.1 | 74.3±4.3 | 84.6±27.7 | 49.5±9.4 | 103.1±63.1 | 124.3±46.1 | 227.4±57.1 |
| milk9=0 | d29 | 49 | 96298.4±15705.3 | 4.0±0.0 | 9.8±1.2 | 0.8±1.4 | 3.2±2.1 | 9.0±2.7 | 16.8±7.6 | 6.6±4.0 | 3.6±3.2 | 8.1±5.9 | 0.0±0.0 | 74.6±4.5 | 188.5±68.9 | 90.7±35.3 | 173.5±112.2 | 276.7±90.4 | 502.0±105.4 |
| milk9=1 | d9 | 102 | 433.7±452.0 | 2.8±0.4 | 10.1±0.6 | 4.8±3.3 | 6.4±1.7 | 4.5±2.6 | 12.3±5.3 | 22.3±5.9 | 2.6±2.4 | 0.2±1.4 | 12.4±0.8 | 0.0±0.0 | 0.0±0.0 | 12.0±0.1 | 18.0±0.0 | 0.0±0.0 | 22.7±5.1 |
| milk9=1 | d14 | 102 | 17128.6±3471.7 | 4.0±0.0 | 11.6±0.5 | 6.3±3.9 | 7.5±0.9 | 8.5±2.6 | 29.6±6.8 | 28.5±6.7 | 10.7±4.8 | 5.5±8.5 | 2.4±0.8 | 59.7±1.4 | 0.7±1.0 | 43.7±7.0 | 45.1±19.8 | 18.9±14.2 | 73.3±16.4 |
| milk9=1 | d17 | 102 | 36036.0±5175.5 | 4.0±0.0 | 12.2±0.4 | 6.3±3.9 | 7.5±0.9 | 8.5±2.6 | 22.7±6.5 | 31.7±7.1 | 15.0±6.1 | 4.9±6.8 | 0.6±1.1 | 70.7±4.4 | 38.4±10.5 | 68.6±11.7 | 64.6±36.8 | 63.2±29.0 | 155.0±31.5 |
| milk9=1 | d20 | 102 | 54177.1±7155.5 | 4.0±0.0 | 12.1±0.6 | 6.4±3.8 | 7.2±1.1 | 8.4±2.6 | 20.6±6.8 | 27.4±7.9 | 17.4±6.6 | 7.6±9.2 | 0.0±0.2 | 74.6±4.9 | 95.7±24.0 | 87.8±14.1 | 80.0±49.9 | 106.6±41.9 | 213.1±44.7 |
| milk9=1 | d29 | 102 | 99852.4±14617.4 | 4.0±0.0 | 9.9±0.7 | 0.5±1.1 | 5.4±2.5 | 7.7±2.6 | 14.6±6.8 | 6.6±4.2 | 4.3±2.9 | 9.1±5.7 | 0.0±0.0 | 74.7±5.0 | 207.6±60.3 | 164.0±36.8 | 133.0±93.3 | 237.3±82.2 | 477.0±94.4 |
| milk9=2 | d9 | 75 | 301.8±353.8 | 2.9±0.4 | 10.1±0.5 | 4.2±2.7 | 8.5±1.8 | 2.8±2.3 | 11.5±5.3 | 24.3±5.6 | 2.6±2.5 | 0.0±0.0 | 12.6±1.0 | 0.0±0.0 | 0.0±0.0 | 12.0±0.1 | 18.0±0.0 | 0.0±0.0 | 22.1±4.0 |
| milk9=2 | d14 | 75 | 17434.6±2961.8 | 4.0±0.0 | 11.8±0.4 | 5.1±3.4 | 10.6±0.7 | 6.4±2.0 | 28.9±4.7 | 32.5±7.8 | 11.6±6.8 | 1.6±4.5 | 2.8±1.1 | 59.1±2.3 | 0.6±0.9 | 47.3±6.7 | 40.7±14.6 | 8.6±9.5 | 74.2±22.1 |
| milk9=2 | d17 | 75 | 39328.2±4161.1 | 4.0±0.0 | 12.3±0.5 | 5.2±3.3 | 10.6±0.8 | 6.4±2.0 | 22.2±5.3 | 35.8±8.7 | 15.4±7.5 | 1.6±4.2 | 1.2±1.6 | 68.2±6.2 | 35.9±8.5 | 96.4±15.0 | 55.4±29.6 | 40.4±21.1 | 153.9±29.5 |
| milk9=2 | d20 | 75 | 61531.9±6931.3 | 4.0±0.0 | 12.3±0.5 | 5.4±3.6 | 10.4±0.9 | 6.4±2.0 | 20.9±6.0 | 32.1±10.1 | 17.2±7.5 | 3.4±6.4 | 0.1±0.5 | 75.5±5.9 | 101.0±21.6 | 131.9±14.4 | 66.6±41.7 | 73.4±29.8 | 208.0±37.5 |
| milk9=2 | d29 | 75 | 114239.4±19233.1 | 4.0±0.0 | 9.3±1.6 | 0.4±1.1 | 8.7±2.9 | 5.8±2.3 | 15.6±7.2 | 7.4±4.7 | 3.9±3.1 | 6.7±5.6 | 0.0±0.0 | 75.9±6.2 | 241.4±73.4 | 248.4±37.5 | 106.3±83.3 | 170.4±62.6 | 499.4±89.5 |
| milk9=3 | d9 | 15 | 137.4±80.6 | 3.0±0.0 | 10.0±0.0 | 3.0±0.0 | 11.5±0.5 | 0.9±1.0 | 12.3±3.4 | 25.9±6.9 | 2.7±4.0 | 0.0±0.0 | 12.3±0.7 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 20.4±2.3 |
| milk9=3 | d14 | 15 | 17383.9±1355.6 | 4.0±0.0 | 11.7±0.5 | 3.3±1.2 | 14.2±0.4 | 4.7±0.6 | 29.0±3.4 | 34.6±9.5 | 11.3±9.6 | 0.0±0.0 | 2.5±0.7 | 59.9±0.3 | 0.7±0.9 | 50.8±1.2 | 34.9±2.2 | 1.3±2.3 | 67.4±15.2 |
| milk9=3 | d17 | 15 | 42420.8±1428.7 | 4.0±0.0 | 12.3±0.5 | 3.5±1.3 | 14.2±0.4 | 4.7±0.6 | 20.3±4.1 | 37.5±9.7 | 15.3±11.5 | 1.1±3.2 | 1.5±1.3 | 65.5±5.0 | 32.1±8.1 | 126.3±4.4 | 39.4±2.9 | 20.0±6.1 | 142.3±21.5 |
| milk9=3 | d20 | 15 | 67717.4±7588.5 | 4.0±0.0 | 12.5±0.5 | 3.5±1.3 | 14.0±0.7 | 4.7±0.6 | 18.8±5.8 | 34.6±9.6 | 18.1±9.6 | 2.3±5.7 | 0.1±0.2 | 73.9±4.3 | 101.9±27.3 | 175.1±12.2 | 44.3±11.5 | 46.5±6.8 | 197.3±32.1 |
| milk9=3 | d29 | 15 | 123470.2±23265.8 | 4.0±0.0 | 9.7±0.8 | 0.0±0.0 | 12.2±2.4 | 4.2±1.1 | 15.3±4.4 | 6.2±2.7 | 4.2±2.9 | 7.2±4.4 | 0.0±0.0 | 74.7±4.4 | 264.3±82.4 | 328.9±40.8 | 62.2±32.8 | 116.9±15.7 | 487.9±93.8 |

### Spec by egg shops open at d9

| group | day | n | money | Q | hires | sheep | cow | goose | wheat t | straw t | tomato t | carrot t | melon t | cum melon | cum straw | cum milk | cum wool | cum egg | cum wheat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| egg9=0 | d9 | 126 | 443.5±465.5 | 2.8±0.4 | 10.2±0.5 | 5.1±3.6 | 7.6±2.7 | 2.9±2.5 | 10.8±5.6 | 22.8±6.2 | 2.7±2.9 | 0.3±2.4 | 12.4±0.9 | 0.0±0.0 | 0.0±0.0 | 12.0±0.1 | 18.0±0.0 | 0.0±0.0 | 22.8±5.0 |
| egg9=0 | d14 | 126 | 17835.1±3435.5 | 4.0±0.0 | 11.6±0.5 | 6.4±4.2 | 9.3±2.7 | 6.1±1.9 | 26.5±5.5 | 30.4±8.2 | 11.7±6.4 | 6.2±8.8 | 2.4±0.9 | 59.7±1.8 | 0.5±0.9 | 45.1±7.8 | 46.6±20.6 | 9.7±12.1 | 70.9±18.7 |
| egg9=0 | d17 | 126 | 38938.0±5421.1 | 4.0±0.0 | 12.3±0.5 | 6.5±4.2 | 9.3±2.7 | 6.1±1.9 | 20.8±5.6 | 33.3±9.1 | 15.8±7.2 | 5.0±6.9 | 0.8±1.3 | 69.4±5.8 | 35.4±9.9 | 83.7±26.6 | 68.1±38.9 | 39.6±24.5 | 142.2±28.3 |
| egg9=0 | d20 | 126 | 59762.9±8866.9 | 4.0±0.0 | 12.3±0.6 | 6.5±4.1 | 9.1±2.8 | 6.0±1.9 | 18.7±6.4 | 29.6±9.9 | 17.9±7.4 | 7.7±9.8 | 0.0±0.4 | 74.2±5.3 | 95.8±25.4 | 112.9±37.6 | 84.3±53.8 | 70.4±32.2 | 194.5±37.3 |
| egg9=0 | d29 | 126 | 110493.0±20198.2 | 4.0±0.0 | 9.7±1.4 | 0.6±1.4 | 7.3±3.7 | 5.4±2.0 | 14.9±7.2 | 7.0±4.3 | 4.1±3.2 | 8.6±5.7 | 0.0±0.0 | 74.5±5.4 | 223.9±75.8 | 210.9±76.1 | 137.7±101.0 | 161.6±61.8 | 459.9±93.2 |
| egg9=1 | d9 | 84 | 390.1±491.2 | 2.8±0.4 | 10.1±0.6 | 4.7±3.2 | 6.5±2.1 | 4.5±2.7 | 12.5±5.2 | 22.7±6.1 | 2.1±2.0 | 0.0±0.0 | 12.6±0.8 | 0.0±0.0 | 0.0±0.0 | 12.0±0.1 | 18.0±0.0 | 0.0±0.0 | 23.0±5.3 |
| egg9=1 | d14 | 84 | 16918.3±3395.6 | 4.0±0.0 | 11.6±0.5 | 6.3±4.2 | 7.6±2.3 | 8.8±1.8 | 31.9±4.4 | 29.7±7.7 | 10.1±5.3 | 2.0±4.4 | 2.6±0.9 | 59.5±1.9 | 0.8±1.0 | 42.5±7.2 | 44.8±19.5 | 18.4±14.1 | 77.1±19.7 |
| egg9=1 | d17 | 84 | 37097.7±5113.1 | 4.0±0.0 | 12.1±0.4 | 6.3±4.0 | 7.6±2.4 | 8.7±1.8 | 24.1±5.6 | 32.8±8.3 | 14.2±6.6 | 2.6±5.0 | 0.9±1.4 | 70.1±5.1 | 37.7±10.7 | 70.4±23.3 | 64.5±39.3 | 64.0±23.5 | 164.6±28.7 |
| egg9=1 | d20 | 84 | 55659.0±6983.1 | 4.0±0.0 | 12.2±0.5 | 6.4±3.9 | 7.3±2.6 | 8.7±1.8 | 22.8±6.1 | 28.5±9.5 | 16.9±6.7 | 4.4±6.3 | 0.1±0.3 | 75.5±5.0 | 95.6±25.2 | 90.0±33.4 | 79.4±52.6 | 109.1±31.0 | 225.7±37.6 |
| egg9=1 | d29 | 84 | 102448.1±15064.6 | 4.0±0.0 | 9.7±0.9 | 0.5±1.0 | 5.9±3.2 | 8.0±1.6 | 15.8±6.5 | 7.0±4.4 | 4.3±2.9 | 7.8±5.9 | 0.0±0.0 | 76.0±5.3 | 216.1±70.3 | 169.2±69.9 | 130.7±97.3 | 246.9±56.4 | 504.7±81.1 |
| egg9=2 | d9 | 27 | 301.1±267.9 | 2.9±0.3 | 10.0±0.3 | 3.5±1.8 | 6.0±1.2 | 6.5±2.0 | 14.9±3.7 | 21.6±6.3 | 2.5±2.3 | 0.0±0.0 | 12.5±0.7 | 0.0±0.0 | 0.0±0.0 | 12.0±0.0 | 18.0±0.0 | 0.0±0.0 | 22.9±4.6 |
| egg9=2 | d14 | 27 | 15481.0±2622.0 | 4.0±0.0 | 11.7±0.5 | 4.1±2.3 | 6.3±1.2 | 12.2±0.9 | 33.6±5.5 | 27.1±5.6 | 10.7±4.4 | 2.6±6.4 | 2.5±0.8 | 59.3±1.9 | 1.1±0.9 | 42.3±6.3 | 37.6±11.5 | 31.9±13.1 | 81.7±19.6 |
| egg9=2 | d17 | 27 | 32040.6±1814.1 | 4.0±0.0 | 12.1±0.4 | 4.3±2.7 | 6.3±1.2 | 12.2±0.9 | 25.7±5.4 | 30.1±6.9 | 15.3±6.5 | 2.5±5.8 | 0.6±1.1 | 70.6±4.8 | 40.5±9.9 | 58.0±13.9 | 44.2±16.6 | 95.8±18.7 | 185.8±38.6 |
| egg9=2 | d20 | 27 | 47677.7±4371.0 | 4.0±0.0 | 12.0±0.6 | 4.4±2.5 | 6.0±1.6 | 12.2±0.9 | 24.8±6.9 | 25.2±8.3 | 16.5±6.6 | 6.3±10.1 | 0.0±0.0 | 74.9±4.4 | 91.6±23.1 | 71.0±18.7 | 51.0±22.8 | 162.3±23.6 | 252.7±49.6 |
| egg9=2 | d29 | 27 | 89599.9±13515.2 | 4.0±0.0 | 9.4±1.1 | 0.0±0.0 | 4.4±2.7 | 11.5±1.2 | 16.0±7.0 | 5.5±3.7 | 3.1±2.3 | 6.3±5.1 | 0.0±0.0 | 74.9±4.4 | 191.7±49.4 | 133.1±49.4 | 81.8±56.7 | 355.7±43.7 | 560.3±79.9 |

### All games

| group | day | n | money | Q | hires | sheep | cow | goose | wheat t | straw t | tomato t | carrot t | melon t | cum melon | cum straw | cum milk | cum wool | cum egg | cum wheat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | d9 | 241 | 404.5±456.6 | 2.8±0.4 | 10.2±0.5 | 4.8±3.3 | 7.0±2.4 | 3.9±2.8 | 11.9±5.4 | 22.7±6.2 | 2.5±2.6 | 0.2±1.7 | 12.5±0.9 | 0.0±0.0 | 0.0±0.0 | 12.0±0.1 | 18.0±0.0 | 0.0±0.0 | 22.9±5.0 |
| all | d14 | 241 | 17164.3±3459.5 | 4.0±0.0 | 11.6±0.5 | 6.1±4.1 | 8.3±2.7 | 7.8±2.8 | 29.4±6.0 | 29.8±7.8 | 10.9±5.9 | 4.3±7.5 | 2.5±0.9 | 59.6±1.9 | 0.7±1.0 | 43.7±7.6 | 44.8±19.5 | 15.7±14.9 | 74.7±19.9 |
| all | d17 | 241 | 37395.4±5478.7 | 4.0±0.0 | 12.2±0.4 | 6.2±4.0 | 8.3±2.7 | 7.8±2.8 | 22.7±6.0 | 32.8±8.6 | 15.1±7.0 | 3.8±6.3 | 0.8±1.3 | 69.8±5.5 | 37.0±10.4 | 75.5±26.0 | 63.7±37.7 | 55.5±30.6 | 155.9±34.5 |
| all | d20 | 241 | 56822.9±8694.3 | 4.0±0.0 | 12.2±0.6 | 6.2±4.0 | 8.0±2.9 | 7.8±2.8 | 21.0±6.8 | 28.8±9.6 | 17.3±7.1 | 6.2±8.8 | 0.0±0.3 | 74.8±5.1 | 95.5±25.1 | 99.2±37.8 | 78.3±51.5 | 96.1±44.5 | 213.4±45.6 |
| all | d29 | 241 | 105077.1±19073.4 | 4.0±0.0 | 9.7±1.2 | 0.5±1.2 | 6.4±3.6 | 7.1±2.8 | 15.4±7.0 | 6.8±4.3 | 4.0±3.0 | 8.0±5.8 | 0.0±0.0 | 75.1±5.3 | 217.7±71.6 | 185.6±76.9 | 128.5±96.5 | 217.0±89.2 | 489.7±95.9 |

## Per-day tables

### T2a. New plantings per day (tile became PLANT) (n=241, mean±sd per day)

| day | melon | wheat | strawberry | tomato | carrot |
|---|---|---|---|---|---|
| d0 | 6.0±0.0 | 11.7±0.6 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 |
| d1 | 2.3±0.5 | 0.0±0.2 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 |
| d2 | 1.6±0.5 | 1.2±0.5 | 1.0±0.2 | 0.0±0.0 | 0.0±0.0 |
| d3 | 0.1±0.4 | 0.4±0.7 | 2.6±1.0 | 0.0±0.0 | 0.0±0.0 |
| d4 | 0.0±0.0 | 0.0±0.1 | 2.1±1.2 | 0.0±0.0 | 0.0±0.0 |
| d5 | 0.0±0.0 | 0.0±0.0 | 0.7±0.7 | 0.0±0.0 | 0.0±0.0 |
| d6 | 1.7±0.8 | 2.4±3.0 | 15.0±5.2 | 0.0±0.0 | 0.0±0.0 |
| d7 | 0.0±0.2 | 0.5±0.9 | 0.5±0.9 | 0.0±0.0 | 0.0±0.0 |
| d8 | 0.7±1.2 | 10.5±4.9 | 1.0±1.6 | 2.5±2.6 | 0.2±1.7 |
| d9 | 0.0±0.1 | 4.5±4.7 | 1.2±2.1 | 1.6±2.6 | 0.1±0.6 |
| d10 | 0.0±0.2 | 13.0±3.5 | 1.3±2.3 | 4.3±3.3 | 1.3±4.1 |
| d11 | 0.0±0.1 | 11.8±3.3 | 0.3±0.8 | 1.2±1.4 | 1.7±3.5 |
| d12 | 0.0±0.0 | 7.2±3.1 | 2.8±3.0 | 1.0±1.6 | 1.5±3.2 |
| d13 | 0.0±0.0 | 7.9±2.7 | 1.5±1.3 | 0.4±0.9 | 1.5±2.8 |
| d14 | 0.0±0.0 | 8.2±2.7 | 0.9±1.1 | 0.6±1.2 | 1.8±3.1 |
| d15 | 0.0±0.0 | 4.8±2.5 | 2.1±2.0 | 1.4±1.8 | 1.2±2.5 |
| d16 | 0.0±0.0 | 5.8±2.6 | 0.1±0.5 | 2.2±2.0 | 1.1±2.1 |
| d17 | 0.0±0.0 | 6.3±2.8 | 0.1±0.5 | 1.9±1.9 | 1.8±3.2 |
| d18 | 0.0±0.0 | 5.1±2.9 | 0.0±0.3 | 1.7±1.8 | 1.8±3.3 |
| d19 | 0.0±0.0 | 6.4±3.0 | 0.0±0.1 | 0.7±1.2 | 2.9±4.1 |
| d20 | 0.0±0.0 | 8.6±3.7 | 0.0±0.0 | 0.1±0.4 | 3.8±4.6 |
| d21 | 0.0±0.0 | 9.2±4.2 | 0.0±0.0 | 0.0±0.3 | 4.3±4.7 |
| d22 | 0.0±0.0 | 12.0±4.8 | 0.0±0.0 | 0.0±0.1 | 4.3±4.6 |
| d23 | 0.0±0.0 | 11.2±3.7 | 0.0±0.0 | 0.0±0.0 | 4.8±4.5 |
| d24 | 0.0±0.0 | 10.4±4.4 | 0.0±0.0 | 0.0±0.0 | 6.1±5.1 |
| d25 | 0.0±0.0 | 8.0±4.3 | 0.0±0.0 | 0.0±0.0 | 7.2±5.3 |
| d26 | 0.0±0.0 | 7.8±4.2 | 0.0±0.0 | 0.0±0.0 | 8.2±5.4 |
| d27 | 0.0±0.0 | 3.5±2.3 | 0.0±0.0 | 0.0±0.0 | 2.2±2.6 |
| d28 | 0.0±0.0 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 | 0.0±0.2 |
| d29 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 |

### T2b. Tile stock at h0 (n=241, mean±sd per day)

| day | melon | wheat | strawberry | tomato | carrot | empty | weed |
|---|---|---|---|---|---|---|---|
| d0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 25.0±0.0 | 0.0±0.0 |
| d1 | 6.0±0.0 | 11.7±0.6 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 2.3±0.6 | 0.0±0.1 |
| d2 | 8.3±0.5 | 11.7±0.5 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 |
| d3 | 9.9±0.3 | 7.9±0.5 | 1.0±0.2 | 0.0±0.0 | 0.0±0.0 | 0.3±0.5 | 0.0±0.0 |
| d4 | 10.0±0.4 | 3.7±0.8 | 3.6±1.0 | 0.0±0.0 | 0.0±0.0 | 0.6±0.6 | 0.0±0.1 |
| d5 | 10.0±0.4 | 0.7±0.8 | 5.6±1.3 | 0.0±0.0 | 0.0±0.0 | 0.3±0.6 | 0.0±0.0 |
| d6 | 10.0±0.4 | 0.0±0.1 | 6.3±0.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.1 | 0.0±0.0 |
| d7 | 11.7±0.9 | 2.4±3.0 | 21.3±5.4 | 0.0±0.0 | 0.0±0.0 | 1.4±1.8 | 0.0±0.1 |
| d8 | 11.7±0.9 | 2.8±3.5 | 21.8±5.2 | 0.0±0.0 | 0.0±0.0 | 0.1±0.4 | 0.0±0.0 |
| d9 | 12.5±0.9 | 11.9±5.4 | 22.7±6.2 | 2.5±2.6 | 0.2±1.7 | 4.4±2.8 | 0.0±0.1 |
| d10 | 12.5±0.9 | 15.2±3.7 | 23.9±6.2 | 4.0±3.2 | 0.3±2.0 | 0.4±1.0 | 0.0±0.0 |
| d11 | 6.5±0.9 | 27.0±5.3 | 25.3±7.5 | 8.3±5.2 | 1.5±5.0 | 9.7±2.8 | 0.1±0.3 |
| d12 | 4.2±1.0 | 34.0±6.2 | 25.5±7.3 | 9.5±5.6 | 3.0±7.2 | 2.1±2.1 | 0.0±0.2 |
| d13 | 2.6±0.9 | 31.1±6.5 | 28.3±7.8 | 10.6±5.8 | 4.1±8.1 | 1.1±1.2 | 0.0±0.2 |
| d14 | 2.5±0.9 | 29.4±6.0 | 29.8±7.8 | 10.9±5.9 | 4.3±7.5 | 0.8±1.2 | 0.1±0.4 |
| d15 | 2.5±0.9 | 27.5±6.2 | 30.6±8.1 | 11.5±6.0 | 4.5±7.6 | 1.0±1.3 | 0.1±0.4 |
| d16 | 2.5±0.9 | 23.3±5.9 | 32.7±8.4 | 12.9±6.4 | 4.2±7.0 | 1.7±1.7 | 0.2±0.5 |
| d17 | 0.8±1.3 | 22.7±6.0 | 32.8±8.6 | 15.1±7.0 | 3.8±6.3 | 2.1±1.9 | 0.3±0.8 |
| d18 | 0.8±1.3 | 21.1±6.5 | 32.8±8.9 | 16.9±7.4 | 4.0±6.5 | 1.8±1.9 | 0.3±0.8 |
| d19 | 0.1±0.4 | 19.9±6.5 | 31.8±9.2 | 18.6±7.5 | 4.6±7.1 | 2.0±1.8 | 0.4±0.8 |
| d20 | 0.0±0.3 | 21.0±6.8 | 28.8±9.6 | 17.3±7.1 | 6.2±8.8 | 3.2±2.1 | 1.1±1.6 |
| d21 | 0.0±0.1 | 23.8±7.5 | 26.3±9.7 | 15.6±6.6 | 8.2±9.9 | 3.0±2.2 | 1.1±1.4 |
| d22 | 0.0±0.0 | 26.3±8.6 | 24.7±10.0 | 11.7±5.7 | 10.4±10.5 | 3.2±2.3 | 1.6±2.0 |
| d23 | 0.0±0.0 | 33.0±9.8 | 16.0±8.8 | 10.1±5.5 | 11.9±10.9 | 5.4±2.7 | 1.9±2.0 |
| d24 | 0.0±0.0 | 35.7±9.6 | 10.8±6.5 | 9.1±5.1 | 12.6±11.0 | 5.5±2.8 | 4.9±2.6 |
| d25 | 0.0±0.0 | 36.6±9.2 | 9.9±6.1 | 8.6±4.9 | 14.3±11.1 | 5.9±3.2 | 3.7±2.4 |
| d26 | 0.0±0.0 | 35.1±9.5 | 8.9±5.5 | 8.1±4.7 | 17.5±11.7 | 6.3±3.2 | 3.7±2.4 |
| d27 | 0.0±0.0 | 33.0±10.0 | 7.8±4.8 | 6.9±4.1 | 20.8±12.9 | 7.9±4.0 | 4.1±2.7 |
| d28 | 0.0±0.0 | 26.2±9.3 | 7.2±4.4 | 5.7±3.6 | 16.8±10.4 | 19.4±6.1 | 5.4±3.1 |
| d29 | 0.0±0.0 | 15.4±7.0 | 6.8±4.3 | 4.0±3.0 | 8.0±5.8 | 38.8±7.3 | 7.6±3.5 |

### T3. Labour per day (n=241, mean±sd per day)

| day | hands (executed) | HIRE orders | PASS unit-actions | WATER | FERTILIZE | COLLECT_FERT | HARVEST |
|---|---|---|---|---|---|---|---|
| d0 | 4.0±0.0 | 4.0±0.0 | 3.5±1.2 | 17.7±0.6 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 |
| d1 | 3.5±0.6 | 4.3±1.0 | 39.1±8.8 | 2.4±0.8 | 0.0±0.0 | 5.0±0.1 | 0.0±0.0 |
| d2 | 5.1±0.4 | 5.1±0.4 | 15.1±7.8 | 22.6±1.8 | 0.0±0.0 | 5.0±0.0 | 5.0±0.7 |
| d3 | 6.0±0.0 | 6.0±0.0 | 32.6±6.5 | 12.2±2.0 | 0.0±0.0 | 6.0±0.1 | 4.5±0.6 |
| d4 | 6.0±0.0 | 6.0±0.0 | 28.4±8.7 | 14.6±1.8 | 0.0±0.0 | 7.1±0.4 | 3.1±0.6 |
| d5 | 5.6±0.5 | 5.7±0.5 | 34.5±13.2 | 9.6±2.2 | 0.0±0.0 | 8.4±0.5 | 0.7±0.8 |
| d6 | 9.0±0.2 | 9.1±0.4 | 8.0±5.8 | 28.9±2.7 | 0.0±0.0 | 8.7±0.8 | 3.0±0.1 |
| d7 | 7.7±0.5 | 8.4±1.4 | 12.5±8.1 | 29.1±4.5 | 0.0±0.0 | 13.3±1.3 | 0.0±0.0 |
| d8 | 9.1±0.5 | 9.2±0.5 | 3.9±4.0 | 41.4±5.1 | 0.0±0.1 | 13.7±1.4 | 3.4±2.2 |
| d9 | 10.2±0.5 | 10.2±0.7 | 3.2±3.6 | 44.5±3.4 | 0.0±0.2 | 15.8±1.4 | 4.3±1.7 |
| d10 | 12.0±0.1 | 12.0±0.1 | 0.4±1.0 | 50.1±5.0 | 3.7±1.8 | 18.7±1.9 | 11.8±2.2 |
| d11 | 11.5±0.5 | 11.5±0.5 | 0.5±0.9 | 60.2±3.7 | 6.0±1.8 | 21.5±2.1 | 9.7±3.0 |
| d12 | 11.5±0.7 | 11.5±0.7 | 1.0±1.1 | 59.7±5.5 | 9.8±2.4 | 21.6±2.1 | 21.7±3.2 |
| d13 | 11.6±0.5 | 11.6±0.5 | 0.6±1.0 | 66.1±4.9 | 10.2±2.3 | 22.2±2.5 | 18.6±3.4 |
| d14 | 11.6±0.5 | 11.6±0.5 | 1.2±1.5 | 60.0±5.5 | 8.8±2.4 | 22.2±2.5 | 24.3±3.2 |
| d15 | 12.3±0.5 | 12.3±0.5 | 0.8±1.1 | 61.9±5.9 | 21.1±4.5 | 22.2±2.4 | 21.6±3.3 |
| d16 | 12.5±0.5 | 12.5±0.5 | 0.7±1.0 | 50.6±5.3 | 10.5±2.5 | 22.0±2.4 | 35.7±5.0 |
| d17 | 12.2±0.4 | 12.2±0.4 | 0.6±0.9 | 67.3±5.7 | 12.4±3.2 | 22.1±2.4 | 25.0±3.2 |
| d18 | 12.5±0.6 | 12.5±0.6 | 0.7±1.0 | 48.3±6.9 | 9.4±3.5 | 21.6±2.4 | 38.8±5.3 |
| d19 | 12.6±0.5 | 12.6±0.5 | 0.5±0.8 | 62.0±6.1 | 19.5±5.2 | 21.9±2.4 | 27.4±4.2 |
| d20 | 12.2±0.6 | 12.2±0.6 | 0.6±0.9 | 48.8±8.7 | 10.6±2.9 | 21.3±2.4 | 35.7±5.8 |
| d21 | 12.2±0.4 | 12.2±0.4 | 0.6±0.9 | 61.4±6.9 | 13.4±3.1 | 21.2±2.3 | 26.8±3.9 |
| d22 | 12.2±0.4 | 12.2±0.4 | 0.6±0.8 | 51.5±7.8 | 14.0±3.4 | 20.4±2.4 | 32.4±4.8 |
| d23 | 12.0±0.3 | 12.0±0.3 | 0.9±1.0 | 58.7±5.9 | 16.2±3.2 | 20.4±2.2 | 25.1±3.3 |
| d24 | 12.0±0.3 | 12.0±0.3 | 0.8±1.0 | 61.1±7.2 | 17.4±3.2 | 19.8±2.3 | 28.3±3.8 |
| d25 | 12.0±0.2 | 12.0±0.2 | 0.7±0.9 | 61.0±6.2 | 16.4±2.9 | 18.9±2.3 | 28.9±3.1 |
| d26 | 12.1±0.4 | 12.1±0.4 | 0.9±0.9 | 62.4±7.0 | 15.4±2.8 | 18.2±2.7 | 30.6±3.8 |
| d27 | 11.7±0.5 | 11.7±0.5 | 1.2±1.2 | 52.1±6.3 | 15.4±3.2 | 18.4±2.9 | 35.0±4.5 |
| d28 | 10.9±0.8 | 10.9±0.8 | 1.5±2.2 | 43.7±5.8 | 14.3±3.5 | 17.8±3.6 | 40.6±5.6 |
| d29 | 9.7±1.2 | 9.7±1.2 | 18.9±10.7 | 23.3±5.2 | 3.1±3.8 | 10.9±4.0 | 38.9±6.5 |

### T4. Herd at h0 and feeding per day (n=241, mean±sd per day)

| day | sheep | cow | goose | sheep placed | cow placed | goose placed | sheep lost | cow lost | goose lost | FEED | CARE | wheat bought |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 3.0±0.0 | 2.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 3.0±0.0 | 3.0±0.0 | 8.9±0.3 |
| d1 | 3.0±0.0 | 2.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 5.0±0.0 | 5.2±0.4 | 6.1±0.6 |
| d2 | 3.0±0.0 | 2.0±0.0 | 0.0±0.0 | 0.0±0.0 | 1.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 3.0±0.1 | 3.0±0.1 | 0.0±0.0 |
| d3 | 3.0±0.0 | 3.0±0.0 | 0.0±0.0 | 0.1±0.3 | 0.9±0.5 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 6.2±0.4 | 6.3±0.5 | 0.0±0.0 |
| d4 | 3.1±0.3 | 3.9±0.5 | 0.0±0.0 | 0.1±0.3 | 1.1±0.6 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 6.9±0.8 | 7.0±0.8 | 0.7±1.1 |
| d5 | 3.3±0.7 | 5.0±1.0 | 0.0±0.0 | 0.1±0.3 | 0.2±0.4 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 8.0±1.0 | 8.0±1.0 | 5.4±3.6 |
| d6 | 3.4±1.0 | 5.2±1.2 | 0.0±0.0 | 0.9±1.8 | 1.5±1.5 | 2.2±2.4 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 8.2±2.3 | 8.3±2.3 | 8.6±4.7 |
| d7 | 4.4±2.6 | 6.7±2.2 | 2.2±2.4 | 0.1±0.3 | 0.1±0.3 | 0.2±0.4 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 13.0±1.4 | 13.1±1.4 | 16.5±5.0 |
| d8 | 4.4±2.8 | 6.8±2.2 | 2.3±2.4 | 0.3±0.8 | 0.2±0.5 | 1.6±1.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 11.5±2.9 | 11.6±2.9 | 12.6±8.9 |
| d9 | 4.8±3.3 | 7.0±2.4 | 3.9±2.8 | 0.5±1.3 | 1.0±1.3 | 1.5±1.6 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 16.2±1.8 | 16.3±1.9 | 30.4±12.4 |
| d10 | 5.3±3.7 | 8.0±2.7 | 5.5±3.2 | 0.4±1.0 | 0.1±0.3 | 2.4±1.3 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 17.0±2.7 | 17.0±2.7 | 29.3±12.7 |
| d11 | 5.7±4.0 | 8.1±2.7 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 19.4±2.4 | 19.5±2.4 | 33.2±22.9 |
| d12 | 5.7±4.0 | 8.1±2.7 | 7.8±2.8 | 0.4±1.4 | 0.2±0.6 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 17.0±3.7 | 16.9±3.6 | 0.3±4.1 |
| d13 | 6.1±4.1 | 8.3±2.7 | 7.8±2.8 | 0.0±0.0 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 | 0.0±0.1 | 0.0±0.0 | 21.1±2.7 | 21.0±2.7 | 0.1±1.2 |
| d14 | 6.1±4.1 | 8.3±2.7 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 19.2±3.2 | 19.1±3.3 | 0.7±3.9 |
| d15 | 6.1±4.1 | 8.3±2.7 | 7.8±2.8 | 0.2±0.7 | 0.0±0.2 | 0.0±0.0 | 0.0±0.3 | 0.0±0.1 | 0.0±0.0 | 17.8±3.7 | 17.6±3.7 | 1.3±5.7 |
| d16 | 6.2±4.0 | 8.3±2.7 | 7.8±2.8 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 | 0.0±0.1 | 0.0±0.2 | 0.0±0.1 | 16.8±3.8 | 15.4±4.1 | 0.7±3.0 |
| d17 | 6.2±4.0 | 8.3±2.7 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.2 | 0.0±0.2 | 0.0±0.0 | 18.7±3.2 | 18.3±3.2 | 1.2±3.9 |
| d18 | 6.1±4.0 | 8.3±2.7 | 7.8±2.8 | 0.2±0.9 | 0.0±0.2 | 0.0±0.0 | 0.1±0.4 | 0.1±0.4 | 0.0±0.1 | 14.0±4.3 | 12.7±4.2 | 0.7±3.0 |
| d19 | 6.3±4.0 | 8.2±2.8 | 7.8±2.8 | 0.0±0.1 | 0.0±0.1 | 0.0±0.0 | 0.1±0.4 | 0.2±0.5 | 0.0±0.1 | 18.3±3.5 | 16.8±3.8 | 4.3±8.5 |
| d20 | 6.2±4.0 | 8.0±2.9 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.2 | 0.1±0.3 | 0.0±0.1 | 16.1±4.1 | 15.1±4.3 | 1.7±4.6 |
| d21 | 6.2±3.9 | 8.0±2.9 | 7.8±2.8 | 0.1±0.5 | 0.0±0.0 | 0.0±0.0 | 0.1±0.4 | 0.2±0.5 | 0.0±0.0 | 16.9±3.8 | 15.7±3.7 | 4.1±6.5 |
| d22 | 6.1±3.9 | 7.8±3.1 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.3±0.7 | 0.1±0.4 | 0.0±0.1 | 15.4±4.2 | 14.3±4.3 | 1.3±4.7 |
| d23 | 5.8±3.7 | 7.6±3.0 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.1±0.3 | 0.2±0.4 | 0.0±0.2 | 18.1±3.4 | 17.1±3.6 | 3.8±6.1 |
| d24 | 5.7±3.8 | 7.5±3.2 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.5±0.8 | 0.1±0.4 | 0.0±0.1 | 13.9±4.4 | 13.4±4.4 | 1.5±5.8 |
| d25 | 5.2±4.1 | 7.4±3.2 | 7.8±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.7±1.1 | 0.3±0.8 | 0.0±0.1 | 16.8±3.7 | 15.9±3.8 | 0.7±3.6 |
| d26 | 4.5±4.1 | 7.1±3.4 | 7.7±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.2±0.5 | 0.1±0.3 | 0.0±0.2 | 14.4±4.3 | 12.2±4.5 | 0.9±3.6 |
| d27 | 4.3±4.2 | 7.0±3.4 | 7.7±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.4±0.8 | 0.3±1.0 | 0.0±0.2 | 12.9±3.5 | 8.8±4.4 | 1.0±4.4 |
| d28 | 3.9±4.3 | 6.7±3.6 | 7.7±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 3.4±3.5 | 0.3±0.6 | 0.6±1.1 | 5.5±3.2 | 0.1±0.3 | 0.2±1.4 |
| d29 | 0.5±1.2 | 6.4±3.6 | 7.1±2.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 |

### T5. SELL-ordered units per day (n=241, mean±sd per day)

| day | wheat | carrot | tomato | strawberry | melon | egg | milk | wool | fertilizer |
|---|---|---|---|---|---|---|---|---|---|
| d0 | 5.9±0.4 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 |
| d1 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 5.0±0.0 |
| d2 | 0.7±0.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 5.0±0.0 |
| d3 | 6.8±1.6 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 6.0±0.0 |
| d4 | 6.7±1.9 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 7.1±0.3 |
| d5 | 0.2±0.4 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 8.3±0.5 |
| d6 | 1.0±1.8 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 18.0±0.0 | 8.3±0.9 |
| d7 | 0.1±0.3 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 12.1±1.8 |
| d8 | 1.6±4.2 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 12.0±0.1 | 0.0±0.0 | 11.3±1.9 |
| d9 | 0.1±1.3 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 12.8±2.2 | 10.6±2.6 |
| d10 | 0.8±4.2 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 29.6±2.9 | 0.0±0.0 | 7.0±4.1 | 0.0±0.0 | 9.9±2.7 |
| d11 | 13.4±13.5 | 0.0±0.1 | 0.0±0.0 | 0.0±0.0 | 15.2±4.9 | 2.5±4.3 | 5.6±3.9 | 0.7±2.2 | 14.6±3.1 |
| d12 | 16.3±9.4 | 0.4±3.9 | 0.0±0.0 | 0.0±0.0 | 7.3±4.7 | 6.1±7.5 | 12.0±6.5 | 10.2±13.1 | 16.3±3.0 |
| d13 | 21.2±9.3 | 1.1±4.6 | 0.0±0.0 | 0.7±1.0 | 7.5±3.8 | 7.1±6.4 | 7.1±5.1 | 3.0±4.7 | 10.9±2.8 |
| d14 | 27.1±12.9 | 3.2±8.8 | 0.0±0.0 | 4.5±2.5 | 0.6±2.1 | 12.5±8.8 | 16.0±11.3 | 4.9±5.5 | 12.1±3.3 |
| d15 | 28.4±13.4 | 4.3±8.8 | 0.0±0.0 | 6.9±2.8 | 0.0±0.4 | 13.2±7.5 | 5.5±4.3 | 8.8±12.6 | 4.4±5.5 |
| d16 | 25.8±12.2 | 4.0±8.1 | 0.0±0.1 | 24.9±9.5 | 9.6±4.7 | 14.2±7.3 | 10.3±8.8 | 5.2±7.4 | 9.6±3.4 |
| d17 | 16.4±10.5 | 4.2±7.6 | 2.8±3.9 | 14.3±6.3 | 0.5±1.7 | 14.6±7.6 | 8.4±7.1 | 3.8±4.8 | 10.4±4.1 |
| d18 | 25.9±12.9 | 4.7±8.2 | 7.8±6.7 | 31.0±13.2 | 3.1±5.7 | 14.1±7.0 | 8.8±7.2 | 6.6±9.6 | 10.7±3.7 |
| d19 | 15.2±9.9 | 3.4±7.1 | 13.3±10.7 | 13.2±7.3 | 1.4±3.4 | 11.9±7.2 | 6.5±5.0 | 4.2±5.5 | 5.8±5.5 |
| d20 | 16.7±10.1 | 3.9±7.2 | 18.8±10.9 | 23.0±14.4 | 0.2±1.3 | 12.7±7.5 | 9.3±7.0 | 4.8±5.8 | 9.0±3.5 |
| d21 | 17.9±11.9 | 5.7±9.4 | 14.1±9.7 | 13.9±8.1 | 0.0±0.4 | 12.4±7.4 | 8.0±5.8 | 5.5±7.4 | 8.6±4.4 |
| d22 | 18.7±12.7 | 6.9±11.0 | 13.7±8.5 | 15.3±10.2 | 0.1±0.6 | 13.2±8.4 | 8.6±5.8 | 5.0±5.9 | 7.8±3.9 |
| d23 | 21.3±11.6 | 10.1±13.3 | 5.6±5.7 | 14.5±7.7 | 0.0±0.0 | 13.3±8.5 | 8.6±6.1 | 4.8±5.2 | 5.1±4.0 |
| d24 | 31.6±16.4 | 13.6±14.9 | 6.4±7.1 | 10.5±7.4 | 0.0±0.0 | 13.4±8.2 | 9.1±7.0 | 6.9±8.8 | 3.6±3.0 |
| d25 | 32.0±18.2 | 14.1±14.7 | 8.0±7.6 | 10.6±6.7 | 0.0±0.0 | 12.4±8.1 | 9.9±5.8 | 5.3±6.4 | 3.4±3.0 |
| d26 | 37.0±18.2 | 13.7±13.9 | 10.6±8.3 | 10.9±6.9 | 0.0±0.0 | 13.0±8.5 | 10.6±7.3 | 5.8±5.7 | 3.3±2.6 |
| d27 | 45.2±19.6 | 19.8±17.7 | 13.7±9.8 | 11.7±6.8 | 0.0±0.0 | 13.1±9.3 | 10.4±6.1 | 6.7±8.3 | 3.1±2.7 |
| d28 | 55.9±22.1 | 26.7±20.5 | 14.0±9.3 | 11.7±8.4 | 0.0±0.0 | 17.4±10.3 | 11.9±7.2 | 5.4±5.7 | 3.6±2.7 |
| d29 | 94.1±42.1 | 44.5±27.1 | 11.4±8.8 | 17.1±10.2 | 0.0±0.1 | 24.9±11.7 | 12.1±6.2 | 7.9±7.7 | 11.2±5.1 |
