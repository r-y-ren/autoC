# CARE / FEED / WATER coverage: engine rules and where the opponent's extra work goes

Worktree `.claude/worktrees/care-cov` (base bdec0e9). Engine read-only at
`.venv/lib/python3.11/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py`
(vendor/engine.lock.json pins package 1.32.7, sha256 bc8a5487..., so this file *is* the vendored engine).

Data: the 3 pinned engine replays under `scratchpad/alloc_review/rep`
(`<seed>_<seat>.json`, 6 games = 3 boards x 2 seats). Episode -> seed map from
`alloc_review/plays.csv`: 106401414 -> 971296733, 106773901 -> 1684350134, 106793159 -> 192465598.
Every tile in `observation.farms[p].tiles` carries `cared_today / fed_today / yield_units /
pending_care_bonus / consecutive_unfed / watered_today`, for **both** seats, so the census below is
exact, not inferred from actions.

## Q1 - what CARE / FEED / WATER actually do (file:line)

`kaggriculture.py`:

| verb | immediate handler | cost | end-of-day effect |
|---|---|---|---|
| CARE | L524-530 | **free** (no item, no money) | L829-830: `if cared_today and fed_today: pending_care_bonus += 1` |
| FEED | L505-513 | **1 WHEAT** from the acting unit's inventory | L813-818 resets `consecutive_unfed`; L819-822 **2 consecutive unfed days -> the animal escapes** (tile reverts to bare COOP/PASTURE, animal lost) |
| WATER | L431-444 | free | L777-783: resets `consecutive_unwatered`; **2 consecutive unwatered days -> tile becomes WEED (crop dies)** |

Production, `_daily_refresh_animals` L823-831:

```
days_since_first = next_day - placed_day - first_yield_day
if days_since_first >= 0 and days_since_first % interval == 0:
    base  = 1
    bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0   # L826
    yield_units = min(max_held, yield_units + base + bonus)                 # L827
    tile["pending_care_bonus"] = 0                                          # L828
```

Consequences, precisely:

1. **A skipped CARE removes product, it does not delay it.** Each (cared AND fed) day adds exactly
   +1 unit to the *next* production tick. There is no catch-up: the day is simply not banked.
2. **A skipped FEED does not reduce base production** - `base = 1` is unconditional on `fed_today`.
   It does two other things: (a) on a *production* day an unfed animal **destroys the whole
   accumulated `pending_care_bonus`** (L826 takes it only `if fed_today`, L828 then zeroes it
   regardless); (b) two unfed days in a row lose the animal outright (L819-822).
3. **The care bonus is capped by `max_held`** (L827) - GOOSE 4, COW 6, SHEEP 6 (L18-22). Carrying
   more banked care than the animal's free head-room at the tick simply burns it.
4. **WATER is the only yield mechanism for non-ongoing crops** (WHEAT/CARROT/MELON, `ongoing: False`
   L11-16): L437-444 adds +1 (+2 if fertilized) per watered day inside
   `[(max_yield_day+1)//2, max_yield_day]`. For ongoing crops (TOMATO/STRAWBERRY) watering adds no
   yield at all - production is the interval tick at L797-800 - but the fertilizer doubling there is
   gated on `was_watered`, and two dry days kill the tile.
5. FERTILIZE (L475-482) costs 1 FERTILIZER and only pays on a *watered* day (L799) or in the
   non-ongoing water window (L442).

## Q2 - per-animal output: LEVEL, despite a 20-30 pt care-coverage gap

`scratchpad/carecov/animal_days.csv` (one row per animal per day, both seats, 6 games).
`prod` = `yield_units(day+1 h0) - yield_units(day h23)` = exactly what the engine tick added.

| band | seat | animal-days/g | care% | feed% | prod/g | **prod per animal-day** | cap-loss/g | escapes/g |
|---|---|---|---|---|---|---|---|---|
| d0-4   | ours | 27.7 | 56.6 | 56.6 | 2.0 | 0.072 | 0.00 | 0.67 |
| d0-4   | opp  | 23.7 | 97.2 | 74.6 | 0.0 | 0.000 | 0.00 | 0.00 |
| d5-9   | ours | 35.3 | 92.0 | 92.0 | 46.7 | **1.321** | 0.00 | 0.00 |
| d5-9   | opp  | 48.0 |100.0 | 90.3 | 44.0 | 0.917 | 0.00 | 0.00 |
| d10-19 | ours |134.3 | 80.3 | 85.0 |151.5 | **1.128** | 0.33 | 0.33 |
| d10-19 | opp  |163.0 | 98.4 | 93.7 |201.7 | 1.237 |**13.67**| 0.00 |
| d20-29 | ours |122.0 | 59.4 | 75.3 |139.2 | **1.141** | 0.00 | 1.50 |
| d20-29 | opp  |132.3 | 90.7 | 81.1 |150.7 | 1.139 | **8.67**| 5.67 |

By product (whole season, per game):

| product | seat | animal-days | care% | feed% | made/g | per animal-day | cap-loss/g |
|---|---|---|---|---|---|---|---|
| EGG  | ours | 51.0 | 78.1 | 82.7 | 73.5 | **1.441** | 0.33 |
| EGG  | opp  | 38.0 | 87.7 | 94.7 | 36.7 | 0.965 | **20.67** |
| MILK | ours |141.7 | 72.6 | 80.6 |151.5 | 1.069 | 0.00 |
| MILK | opp  |179.0 | 96.1 | 83.1 |198.0 | 1.106 | 1.67 |
| WOOL | ours |126.7 | 67.8 | 77.2 |114.3 | 0.903 | 0.00 |
| WOOL | opp  |150.0 | 97.3 | 90.9 |161.7 | 1.078 | 0.00 |

**Answer: our per-animal output is essentially level** (d20-29 1.141 vs 1.139; d10-19 1.128 vs 1.237,
-8.8 %). The opponent's near-100 % care coverage does *not* convert into product one-for-one, because
they bank more care than `max_held` head-room and burn **22.3 units/game at the cap** (20.7 of them
eggs). Bonus accounting per game: ours banks 214.2 bonus units and loses 15.5 to unfed production
days; the opponent banks 292.3 and loses 11.3 unfed + 22.3 to the cap. Net realised animal product:
**ours 339.3/game vs opp 396.3/game, +57.0 units for them** - and 28.7 of those +57 come from simply
owning ~28 more animal-days d10-19, not from care coverage.

STATUS: Q1 and Q2 done. Q3 (work-order attribution to coins) and Q4 (lever) in progress.

## Q3 - where the extra work orders go, and what they are worth

Work orders per game from the verbdiff percentages x live unit-turns
(`(1 + hands) * 24 * 10 days`; d10-19 ours 2,863 / opp 2,825; d20-29 ours 2,832 / opp 2,904):

| verb | d10-19 ours | d10-19 opp | d20-29 ours | d20-29 opp | season d10-29 delta |
|---|---|---|---|---|---|
| CARE | 114 | 171 | 82 | 133 | **+108** |
| FEED | 120 | 161 | 96 | 119 | **+64** |
| COLLECT_FERT | 135 | 168 | 136 | 153 | +51 |
| WATER | 386 | 445 | 339 | 463 | **+184** |
| PLANT | 56 | 92 | 59 | 93 | +70 |
| HARVEST | 154 | 163 | 232 | 288 | +65 |
| FERTILIZE | 112 | 37 | 95 | 53 | **-117 (ours)** |
| SHED | 145 | 111 | 131 | 86 | -99 (ours) |

Decomposition of realised animal production (per game, `scratchpad/carecov/agg2.py`):

|  | due-days | base paid | bonus paid | bonus banked | lost to unfed fire | lost to `max_held` |
|---|---|---|---|---|---|---|
| ours | 129.3 | 129.3 | **210.0** | 214.2 | 15.5 | 0.3 |
| opp  | 136.7 | 136.7 | **259.6** | 292.3 | 11.3 | **22.3** |

So of the +57.0 unit animal gap, **+7.4 is base (more animal-days) and +49.6 is the care bonus.**
The +108 extra CARE orders and the +64 extra FEED orders are the whole of it; the +184 WATER / +70
PLANT / +65 HARVEST orders are a **wheat rotation** (their 532 wheat crop-days vs our 257, 361.7 vs
275.2 wheat units made) whose product is the feed those cares need, not coins.

Whole-season units made per game and their value at observed mean prices
(`scratchpad/carecov/px.py`; prices are the replays' own quotes):

| product | ours | opp | delta (opp-ours) | mean price d10-29 | delta coins |
|---|---|---|---|---|---|
| EGG | 73.5 | 36.7 | -36.8 | 49.7 | **-1,829** (ours) |
| MILK | 151.5 | 198.0 | +46.5 | 143.7 | **+6,682** |
| WOOL | 114.3 | 161.7 | +47.4 | 100.8 | **+4,778** |
| STRAWBERRY | 273.3 | 248.7 | -24.6 | 154.9 | -3,811 (ours) |
| CARROT | 131.3 | 58.3 | -73.0 | 53.5 | -3,906 (ours) |
| MELON | 77.5 | 60.0 | -17.5 | 181.2 | -3,171 (ours) |
| TOMATO | 17.3 | 0.0 | -17.3 | 77.3 | -1,337 (ours) |
| WHEAT (feed input, not sold) | 275.2 | 361.7 | +86.5 | - | - |

**Attribution: the 0.06 work/unit-turn gap is animal husbandry, worth about +9.6k coins/game to them
(milk +6.7k, wool +4.8k, less eggs -1.8k), bought with ~172 extra CARE+FEED orders and financed by
~319 extra wheat-rotation orders.** Our own turns go the other way - FERTILIZE (117 more orders,
24.8 fertilised tiles vs their 11.9) and SHED - and buy us a *larger* crop stream (+12.2k coins of
strawberry/carrot/melon/tomato units). Net product value across the whole board is close to level,
which is what the 6 replay outcomes show (we win 1 of 4 distinct games, margins -30k..+19k).

## Q4 - the smallest lever

**The lever already exists and is off: `CARE_FILL_ON` (`src/kagg3/core/plan.py:2795`, hops
`CARE_FILL_HOPS = 4` at :2802, test `tests/test_care_fill.py`).** Nothing needs building; its four
admission rules are exactly the engine rules derived in Q1 (uncared today, fed today, bank headroom
`bank_carry + 2 <= max_held`, fire lands on or before `VAL.pay_day()`), it writes only into turns
that were `OP_PASS`, and it changes no admission, no market row and no block cut.

Sizing it from the census rather than from the opponent, which is the honest ceiling:

* Our animals are **fed** on 254.2 animal-days a game (0.827*51 EGG + 0.806*141.7 MILK +
  0.772*126.7 WOOL) but **cared** on only 214.2 of them. Every one of those 40.0 fed-but-uncared
  days is a **free** +1 product unit - the animal is already owned, already fed, already routed,
  and our `max_held` waste is 0.3 units a game, so the headroom is genuinely there.
* 40.0 units at our marginal animal mix (milk 143.7 / wool 100.8 at d10-29 quotes) is
  **+4.8k to +5.2k coins a game**, i.e. rather more than half of the entire attributed animal gap.
* The turns are free: we PASS 17.40 % of unit-turns at d10-19 and 16.41 % at d20-29 - about 960
  idle unit-turns a game against their ~430.
* Raising care beyond 254 would need FEED coverage to rise too (a care on an unfed animal banks
  nothing, `:829-830`), and that is a *different*, non-free lever - it costs a wheat.

Two engine facts that should gate any future care push, both new here:

1. **The opponent's own care push is already past its optimum.** They burn 22.3 units a game at
   `max_held` (20.7 of them eggs: GOOSE `interval` 1, `max_held` 4, so a fully-cared goose fires
   1+1=2 a day and overflows in two days unless harvested daily). Copying their 98 % coverage
   without a harvest cadence to match buys nothing. `CARE_FILL_ON`'s headroom rule already handles
   this; a naive "care everything" rule would not.
2. **Care coverage is not what makes per-animal output differ** - ours is 1.128 / 1.141 per
   animal-day against their 1.237 / 1.139. The gap is the *bank*, and the bank is capped by the
   product of (fed days) x (headroom at the fire).

### Not built

No new switch was written: a second, smaller version of `CARE_FILL_ON` would duplicate a switch
that is already engine-exact and already has an OFF-path digest test. The next step is a paired
engine measurement of `CARE_FILL_ON` (not a sim screen - `S/simscreen` cannot price the glut this
lands in), on pinned held-out boards, against the 40.0-unit ceiling above.

## Q4 addendum - `CARE_FILL_ON` measured, and it is inert on these boards

`scratchpad/carecov/planab.py` replays each of the 180 (game, day) hour-0 states from the three
pinned boards through `plan.build_day` with the live theta, once with `CARE_FILL_ON = False` and once
with it True, and counts the ops the planner emits. Nothing engine-side, so there is no shop lottery
in it; the arm delta is exact. (Note: hands are cleared at each end of day, so hour-0 `farms[p].hands`
is always 0 - the crew is the one the plan itself hires, hence the "rows with any non-PASS op"
roster below. The resulting PASS% 16.7 matches the engine census's 16.4-17.4, so the roster is right.)

| band | arm | unit-turns/g | PASS% | CARE/g | FEED/g | WATER/g |
|---|---|---|---|---|---|---|
| d10-19 | OFF | 2712 | 16.70 | 109.2 | 114.2 | 369.8 |
| d10-19 | ON  | 2712 | 16.65 | 109.8 | 114.2 | 369.8 |
| d20-29 | OFF | 2716 | 16.82 | 78.5 | 91.8 | 320.5 |
| d20-29 | ON  | 2716 | 16.67 | 79.8 | 91.8 | 320.5 |

**Season: CARE 235.8 -> 237.8 (+2.0), PASS 1,123.2 -> 1,117.8 (-5.3).** Out of 1,123 idle unit-turns
a game the filler finds five. It is not the coverage lever it was written to be: its hops start at the
tail cursor `f_t0` of units `_routes` already gave a block, capped at `CARE_FILL_HOPS = 4`, and the
fed-but-uncared animals are not within four hops of those tails.

### Where the 40 units actually are

Lining the planner's op counts up against the engine census closes the books:

| quantity | per game |
|---|---|
| FEED ops the planner emits | 254.2 |
| animal-days the engine records as `fed_today` | 254.2 |
| CARE ops the planner emits | 235.8 |
| animal-days the engine records as `cared_today` | 228.6 |
| animal-days that are **both** (`pending_care_bonus` actually banked) | **214.2** |

So the planner already cares 93 % of what it feeds; only ~18 planned FEEDs carry no CARE, and a
further ~21 planned CAREs land on an animal that ends the day unfed - the FEED *failed*, because
`FEED` takes its wheat from the acting unit's own inventory (`kaggriculture.py:509-511`), not the
shed, and our wheat production (275.2 units a game) barely covers 254.2 feeds. The opponent runs
361.7 wheat against 305 feeds.

**Corrected answer to Q4: the binding constraint on the care bonus is FEED supply, not CARE
coverage or idle turns.** Their bank is 292.3 to our 214.2 because they are fed on 321.1 animal-days
to our 254.2; the care-per-fed-day ratio is 0.91 for them and 0.84 for us. The smallest lever is
therefore *not* a care admission rule - it is wheat-per-unit at the FEED site (a bigger PICKUP of
wheat per routed unit, or a wheat-shortfall guard that refuses to admit a FEED+CARE pair the
inventory cannot fund, so the CARE is not wasted). Both touch the admission/pickup stage, are well
over 60 lines, and were not built here.

**No switch was built.** Building a fifth care switch would have measured 0; the measurement above is
the deliverable.
