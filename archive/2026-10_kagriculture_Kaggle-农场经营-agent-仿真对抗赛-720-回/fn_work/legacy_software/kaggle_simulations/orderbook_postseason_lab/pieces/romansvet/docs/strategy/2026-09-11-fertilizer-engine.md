# Fertilizer engine vs the band clone: where the −7.3k/game comes from

**Correction, 2026-09-12:** the early fertilizer-arbitrage claim below is
withdrawn. All thirteen source replays quote fertilizer at 77–100 on days 0–9,
with early BUY requests seeing 81–89; quotes of 30 or less first appear on
days 21–25. The "purchases re-sold" attribution is gross revenue accounting,
not measured net profit or purchased-unit tracing. See
[raw replay correction](2026-09-12-fertilizer-premise-correction.md).

Measurement only, 2026-09-11T10:16Z. 13 live Kaggle replays (10 LOSS10 losses + wins 107744147 / 107743508 /
107735016), both seats read from the replay JSON to the coin (tile flags `fertilizer_available`, `fed_today`,
`fertilized_until_day`; per-seat `private` shed/inventories; sales from the existing per-seat ledgers
`S/bloss/anatomy/led_<id>_{us,opp}.json`). Script `S/bloss/fert/fert_flow.py`, outputs `S/bloss/fert/flow.csv`
(per game/seat totals) and `S/bloss/fert/flow.txt` (per-day collects / animals fed / applications / sales per seat).

## Answer

The gap is **not production and not feeding**. Both seats generate the same fertilizer (we collect 367/game, the
clone 346 — we are *ahead* by ~21 units) and animal-days are level (401 vs 410). The whole −7.3k fertilizer
*revenue* line is (i) **application: −6.5k** — we burn 190 units/game on FERTILIZE (167-207) against the clone's
62 (61 in 12/13 games, 80 in the variant), a 128-unit displacement into crop yield; (ii) **the clone BUYS 46
fertilizer/game and we buy 8: −1.9k** of their sales are re-sold purchases (they buy on d0-d9 at 8-30 coins when
the pool is empty and sell at 43-56 avg); (iii) unsold at end −0.3k (we leave 0-14, they 0); (iv) **price +0.6k in
our favour** (we sell fewer units at 53.9 avg vs their 50.6); (v) production +1.0k in our favour. Sum of the five
terms −7.1k vs the measured −7.3k (residual −0.1k = collects hidden by the hour-23 night tick).

So the fertilizer line is an income-statement artefact of the same kind `2026-09-09-fertilizer.md` established on
LOSS6: the units we do not sell are applied to tiles, and that document's exact census (2,254/2,254 yield
post-states reproduced) valued our ~179 applications at **+24.2k gross crop coins / +16.8k net of the forgone
fertilizer sale** (86 WHEAT, 79 STRAWBERRY, 8 TOMATO ops) against the clone's 79 applications at +15.3k / +12.4k.
On this trade we are ahead, not behind — the −7.3k here is the sale-side half of a +4k net line.

## Engine rule (from the bit-exact JAX port, `src/kagg3/sim/eod.py` / `units.py`; engine
`kaggle_environments 1.32.7 kaggriculture.py`, sha in `vendor/engine.lock.json`)

* Fertilizer is **produced by animals, one unit per animal per day, independent of feeding**: the night tick sets
  `fertilizer_available = 1` on every *alive* animal tile (`eod.refresh_animals`: `t_favail = where(alive, 1, …)`).
  The flag does not stack — an uncollected animal still offers exactly one unit the next day.
* It reaches the shed only through a **COLLECT_FERTILIZER unit-op on the animal's tile** (`units.py:171`:
  `do_coll = op==COLLECT & has_animal & t_favail==1`; +1 FERTILIZER to that unit's inventory). So production =
  animal-days actually visited by a hand; it costs one unit-turn per unit.
* FEED (`units.py:169`) needs 1 WHEAT in the unit's inventory and sets `fed_today`; feeding gates the animal's
  *product* (milk/wool/egg) and survival (2 consecutive unfed days → the animal escapes). **Feeding does not gate
  fertilizer.**
* FERTILIZE (`units.py:168,230`) burns 1 FERTILIZER from the unit's inventory on a PLANT tile and sets
  `fertilized_until_day = max(prev, day+2)`; a watered, fertilized tile grows +2 yield per growth fire instead of
  +1 (`eod.py:93-94`), capped at the crop's max yield.
* Market: FERTILIZER base 100, T 200, linear 0.4 above/below; **zero town drain** (`spec.TOWN_CENTER_CONSUME[FERT]=0`,
  no shop lists it) → the shared pool only ever grows and the quote walks to the floor (1-6 coins) by d25+.
  BUY_PRODUCT is allowed for WHEAT and FERTILIZER only.

## Per-game table (Δ = us − opp; produced = observed collects, lower bound by ≤1/day, see caveats)

| game | result | fert produced (collects) us/opp | bought us/opp | APPLIED us/opp | sold us/opp | revenue us/opp (k) | avg px us/opp | unsold us/opp | animal-days us/opp | fed animal-days us/opp | uncollected animal-days us/opp | hands d5/d10/d20 us ; opp | herd d10 c/s/g us ; opp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 107764944 | loss -677 | 391/348 | 6/46 | **188/61** | 214/347 | 11.1/16.4 (-5.2) | 52.1/47.2 | 4/0 | 426/412 | 348/366 | 17/48 | 5/9/12 ; 4/11/11 | 6/10/1 ; 8/6/2 |
| 107766829 | loss -1468 | 406/358 | 4/36 | **177/61** | 245/341 | 11.7/14.9 (-3.3) | 47.6/43.8 | 1/0 | 441/412 | 338/366 | 17/38 | 5/9/12 ; 4/11/12 | 6/11/1 ; 6/10/0 |
| 107769126 | loss -3530 | 367/343 | 11/46 | **198/61** | 186/342 | 10.5/17.4 (-6.8) | 56.7/50.8 | 4/0 | 402/412 | 287/366 | 21/53 | 5/10/10 ; 4/11/11 | 5/7/3 ; 8/6/2 |
| 107769991 | loss -4661 | 366/343 | 7/46 | **187/61** | 195/342 | 10.1/17.6 (-7.5) | 52.0/51.5 | 5/0 | 404/412 | 327/366 | 24/53 | 5/8/12 ; 4/11/11 | 10/3/3 ; 8/6/2 |
| 107771992 | loss -8544 | 374/343 | 0/46 | **180/61** | 193/342 | 9.6/17.7 (-8.1) | 49.7/51.8 | 14/0 | 404/412 | 330/366 | 16/53 | 5/8/13 ; 4/11/11 | 12/2/1 ; 8/6/2 |
| 107777972 | loss -3451 | 375/345 | 7/46 | **193/61** | 191/345 | 10.0/17.8 (-7.8) | 52.4/51.5 | 12/0 | 410/412 | 320/366 | 18/51 | 5/8/11 ; 4/11/11 | 7/4/4 ; 8/6/2 |
| 107779009 | loss -917 | 371/348 | 6/46 | **195/61** | 188/347 | 9.9/17.8 (-7.9) | 52.8/51.2 | 8/0 | 408/412 | 340/366 | 23/48 | 5/8/11 ; 4/11/11 | 8/4/4 ; 8/6/2 |
| 107779976 | loss -5365 | 409/350 | 6/46 | **180/61** | 244/356 | 11.1/16.6 (-5.5) | 45.3/46.5 | 4/0 | 448/412 | 347/366 | 20/46 | 5/9/12 ; 4/11/11 | 5/9/3 ; 6/6/4 |
| 107780983 | loss -4655 | 325/348 | 10/46 | **202/61** | 131/347 | 8.4/19.2 (-10.8) | 64.0/55.3 | 9/0 | 345/412 | 254/366 | 8/48 | 5/9/11 ; 4/11/11 | 5/6/3 ; 8/6/2 |
| 107781955 | loss -3203 | 331/348 | 11/46 | **207/61** | 152/347 | 9.0/18.9 (-9.8) | 59.5/54.3 | 2/0 | 371/412 | 271/366 | 25/48 | 5/9/11 ; 4/11/11 | 7/4/4 ; 8/6/2 |
| 107744147 | WIN +16342 | 349/343 | 12/46 | **197/61** | 172/349 | 9.9/18.1 (-8.2) | 57.3/51.9 | 2/0 | 387/412 | 269/366 | 24/53 | 5/10/11 ; 4/11/11 | 6/5/4 ; 8/6/2 |
| 107743508 | WIN +8548 | 371/342 | 8/56 | **167/80** | 228/326 | 11.9/15.3 (-3.4) | 52.1/46.9 | 0/0 | 410/392 | 339/340 | 23/35 | 5/9/12 ; 4/11/13 | 5/11/1 ; 6/9/0 |
| 107735016 | WIN +1967 | 336/343 | 17/46 | **198/61** | 151/347 | 9.0/19.3 (-10.4) | 59.4/55.7 | 10/0 | 359/412 | 290/366 | 9/53 | 5/10/12 ; 4/11/11 | 4/5/4 ; 8/6/2 |

Means (13 games), us / opp: produced 367 / 346 · bought 8 / 46 · applied **190 / 62** · sold 192 / 344 · revenue
10,169 / 17,454 (−7,285) · avg price 53.9 / 50.6 · unsold 5.8 / 0.0 · animal-days 401 / 410 · fed animal-days
312 / 364 · uncollected animal-days 19 / 48 · FEED events 312 / 364.

### Feed / idle-animal / hand picture (per day, `flow.txt`)

* Both seats collect nearly every animal every day from d1 (our uncollected animal-days 19/game, theirs 48 — we
  are the more thorough collector). Production tracks herd size, not hands: the clone runs 16-17 animals from d10
  (8 cows 6 sheep 2-3 geese, all bought d0-d10), we 12-20 from d10 (4 cows 1 sheep 1 goose at d0, then a
  variable sheep/goose build d9-12 that is partly sold off by d29: e.g. 6/13/1 at d12 → 6/1/1 at d29 in 107764944).
* We leave ~90 animal-days/game **unfed** (312 fed of 401) where the clone feeds 364 of 410; this costs
  milk/wool product, not fertilizer, and is a separate line (the anatomy's milk −3…−6k / wool −4.6k).
* Hands: we 5 / 8-10 / 10-13 at d5/d10/d20 vs their 4 / 11 / 11-13. Neither seat is labour-bound on collection.

### Application (b)

We apply from d10 (3/4/9/17 on d10-13, then 10-20/day through d28); the clone applies 0 until d14 and then ~4/day
(61 total, on STRAWBERRY). Value of the applications: not re-censused here (time box); the 2026-09-09 exact census
on LOSS6 (same seat build, same clone) is +24.2k gross / +16.8k net per game for ours vs +15.3k / +12.4k for
theirs, positive per crop for every crop either seat fertilizes. Our per-day sales table shows the displacement
directly: from d13 our fertilizer sales fall to 0-8/day while applications run 10-20/day; the clone sells 13-17/day
at h0.

### Sales (c)

The clone sells its whole collect the next morning (h0, from d1, first 3 units at 100.0); we start d2 and sell in
late hours. Realised average price is nonetheless **higher for us** (53.9 vs 50.6) because we sell fewer units into
the shared, drain-less pool; timing is worth +0.6k to us, not against us. Unsold at end 0-14 units (−0.3k). There
is no sale-timing loss to recover.

## Attribution of the −7,285/game (coins, at the clone's realised average price)

| term | Δ units (us − opp) | coins |
|---|---|---|
| production (collects) | +21 | **+976** |
| purchases re-sold by the clone | −38 | **−1,915** |
| application (FERTILIZE burn) | +128 | **−6,490** |
| unsold at end | +5.8 | −300 |
| realised price (ours 53.9 vs 50.6, on our 192 units) | — | +581 |
| residual (hour-23 collects hidden by the tick) | | −137 |
| **total** | | **−7,285** |

Application is 89 % of the gap; the clone's fertilizer purchases are the rest; production, feeding and sale timing
are level or in our favour. Per-game rows in `S/bloss/fert/run.out` (columns prod$/bought$/appl$/unsold$/price$).

## Comparison with the 2026-09-06 "fert/wheat volume" closure

What was closed (memory `dominant-strategy-2026-09-03.md` 2026-09-04 13:00Z/13:15Z; `2026-09-09-switch-sweep.md`
row 26; archive 2026-09-10): `FERT_VOLUME_ON` (`plan.py:3739-3870`, "an application must be worth NUM/DEN × the
fertilizer unit it burns", modes spot/base/marginal) and `WHEAT_VOLUME_ON`. Measured: 384 paired engine games
best mode +636 t 1.5 (below the +1,500/t 2 bar), base −1,103; vs the 2450+ band book +2.6k t 3.3 then pooled
+1.8k t < 2 → "not a component"; 2026-09-10 re-measure on g1000+pair: level on TOPB, +650-750 t 4 on LIVE62 with
wins level (denial signature), and composed with HIRE_ROW it drops 3-4 live boards → CLOSED as a package
candidate. The 2026-09-09 two-purse counterfactual on the sale schedules: removing our 86 wheat applications
+3,098 on the fertilizer market, −7,184 on the wheat market = **−4,086/game** (displacement).

**Same lever.** The gap measured here is the application volume itself (128 units/game more burned than the
clone), i.e. exactly the quantity `FERT_VOLUME_ON` throttles. It is not a feed-hours, collection, idle-animal or
sale-timing lever — those are level or ours. Nothing new is opened by this measurement; the −7.3k line should be
read as the sale-side of an application trade already judged (net positive for us at gross crop value, and the
throttle judged level/negative in paired engine play). The one genuinely different item is the clone's **46-unit
early fertilizer BUY** (−1.9k of the line): it buys at 8-30 when the pool is near-empty on d0-d9 and re-sells at
43-56 — a market arbitrage, not a farm lever; what a switch would have to change is a BUY_PRODUCT FERTILIZER row on
d0-d9 while the quote is below ~30, sized to the d10-20 sale window (untested, and it hands the pool 46 more units).

## Caveats

* "Produced" counts `fertilizer_available` True→False transitions between consecutive steps; a collect in the hour-23
  step is masked by the night tick re-setting the flag, so collects are under-counted by ≤1/animal/day (balance
  residuals −2…−29 units/game/seat). The attribution's residual term (−137 coins) carries this.
* Application value is taken from the 2026-09-09 exact census on the LOSS6 games (same clone, same seat build),
  not re-run on these 13 replays.
* The animal-days census reads hour-22 state (before the tick); d0 rows therefore count animals placed by h22 only.
* Prices in the attribution are the clone's realised average; a unit-by-unit walk of the market curve (as in the
  2026-09-09 doc) would shift the application/price split by a few hundred coins, not the ranking of the terms.
* n = 13 live games against one open-loop file; nothing here is seed noise (both seats read from the same replay).
