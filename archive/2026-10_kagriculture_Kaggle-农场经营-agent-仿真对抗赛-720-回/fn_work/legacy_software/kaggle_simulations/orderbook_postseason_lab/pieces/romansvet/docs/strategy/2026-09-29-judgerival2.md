# JUDGERIVAL2: a flood rival for the closed-loop judge (2026-09-29, 00:15Z-01:42Z)

Stream dir `S/judgerival2/`. Harness only: `S/judgerival1/rcr.py` + `rivals.json` gain new rival cfgs. No src, dist, package, clone-params or trainer change, no upload, no GPU.

## Verdict
- **New rival `flood` (`judge.sh --rival flood`).** It matches the live programme's d18-29 flood on 3 of the 4 target products on the 27 live27 seats: strawberry, tomato and milk within 15 % in units and price. **Melon is not reached** (1.7 units vs 14.0).
- **The income calibration moves the wrong way.**
  - Rival: 71.9k vs g0capsfix 84.3k and live 101.2k.
  - Ours: 119.1k vs g0capsfix 112.2k and live 97.7k.
  - So `flood` is a **price judge for our d18-29 cash crops**, read on **dours**. It is not a margin or flip judge.
- **Recommended use:**
  - late-game product-mix levers (strawberry / tomato / milk volume): `--rival flood`, metric = dours plus the d18-29 ledger;
  - margin / flips: keep `g0capsfix`;
  - read a candidate on both.
  - `S/judgerival1/default_rival` is unchanged (it is not written; the default stays `ctrl` as JUDGERIVAL1 left it).
- **Remaining gap to live**, see section 5.
- **Re-judged cells** (80 games, paired with the PFS vs flood control):
  - PRICEGAP1 rd: dours -894 (t -1.97), dtheirs +173, dmargin -1,066 (t -1.40). vs g0capsfix: -876 / +1,550 / -2,426 (t -4.43).
  - SALESIDE1 ask 0.96: dours -2,374 (t -5.98), dtheirs +1,180, dmargin -3,554 (t -4.88). vs g0capsfix: -854 / +591 / -1,445 (t -2.74).
  - Neither becomes a candidate under the new rival.

## 0. Why (PRICEGAP1)
- PRICEGAP1 found that live, the programme rival sells 147.5 strawberry units in d18-29. Our strawberry price is 87 live vs 134 closed loop (-7.4k). Melon, milk and tomato show the same pattern.
- The clone rival sells only 64-70 strawberry units in that window, so every late-game lever on our body reads as a loss offline.
- `g0capsfix` already reproduces the milk flood, and over-floods it on live27 (our milk price 70 vs live 102).

## 1. Target table: live programme rival vs g0capsfix, d18-29, the 27 live27 seats (original seat, per game)
Sources:
- live = `S/pricegap1/res/live_days.json` (exact engine ledger of the recorded game);
- ctrl = PRICEGAP1 `pfs_l27`;
- g0capsfix = this stream's `res/g0cf_l27` (PFS vs `--rival g0capsfix` on the same 27 seats, remote).

Script `an_flood.py prod`; full product x window tables in `res/prod_l27_d18.txt`.

| product | rival units live / ctrl / g0capsfix | rival price live / ctrl / g0capsfix | our price live / ctrl / g0capsfix |
|---|---|---|---|
| STRAWBERRY | 147.5 / 64.4 / 66.0 | 80 / 154 / 154 | 87 / 134 / 141 |
| MELON | 14.0 / 1.2 / 3.8 | 159 / 226 / 215 | 142 / 181 / 168 |
| MILK | 121.1 / 102.1 / 142.4 | 84 / 104 / 62 | 102 / 124 / 70 |
| TOMATO | 52.0 / 4.8 / 1.4 | 82 / 111 / 148 | 113 / 153 / 155 |
| WHEAT | 567.6 / 310.1 / 271.1 | 37 / 33 / 37 | 35 / 30 / 35 |
| CARROT | 124.7 / 73.1 / 62.8 | 45 / 50 / 53 | 44 / 47 / 49 |
| EGG | 102.9 / 68.7 / 83.3 | 47 / 50 / 48 | 50 / 52 / 50 |
| WOOL | 90.9 / 84.2 / 74.2 | 98 / 100 / 104 | 109 / 120 / 128 |
| FERTILIZER | 140.8 / 65.8 / 104.5 | 23 / 34 / 22 | 26 / 34 / 24 |

- The live programme out-produces the clone on **every** product: wheat is 2x in d18-29 and 4.6x in d10-17 (333.7 vs 72.6), plus melon d10-17 (64 vs 55).
- It is a larger engine: more land, crew and fertilizer. It is not only a different crop mix.

## 2. The flood overlay (`S/judgerival1/rcr.py`, cfg key `"flood"` in `rivals.json`)
**Wiring.**
- A cfg whose `BCB_CAP` is `"_fix+flood"` runs `caps_fix` (the `_fix` path, unchanged) plus the FLOOD caretaker on that clone seat.
- Its parameters come from the cfg's `"flood"` block.
- The caretaker wraps `MAIN._care_units` (after CARE's unit overlay) and `MAIN._care_market` (after CARE's market overlay). Both are installed only when the chosen cfg has a `"flood"` block.
- ctrl / g0 / capsfix / g0capsfix definitions are untouched.

**Elements** (all on the rival seat):
- **Standing-tile targets.** Strawberry uses the teacher's `cum_PLANT_STRAWBERRY` (median or p75 from `S/programme1/schedule_*.json`, copied into rivals.json as a 30-day list), planted through d15-19. Tomato uses `cum_PLANT_TOMATO` (p75 x 0.8) through d21. Melon is optional.
- **Swap.** While below target, the clone's own `PLANT WHEAT/CARROT` is re-targeted to the flood crop. This is tile-neutral: the overlay uses the tiles the clone chose.
- **Idle units** (PASS only) carry flood goods home, plant to target (keeping `reserve` empty tiles) and harvest ripe flood tiles.
- **Extra hands** (`xh`): xh HIRE orders appended every day at h0 (d8-27). The last xh units are overlay-driven:
  - carry home anything;
  - fertilize strawberry/tomato from the shed's fertilizer (PICKUP at the access tile) when `xf`;
  - plant, water the flood crops, harvest.
- **Market.**
  - At h0-1 it buys the seed deficit: target(d+1) - standing - seeds - ordered.
  - From d10 it SELLs the full shed stock of strawberry / tomato / melon every step (no holding).

**Iterations** (all kept in rivals.json):

| cfg | definition | result |
|---|---|---|
| `flood_v1` | median strawberry, p75 tomato, PASS **and moving** units hijacked to plant / harvest / carry | smoke, 1 seat: rival 28.1k vs g0capsfix-class 63-69k. The herd broke (eggs 373 -> 29): overlay plantings took coop / pasture tiles and feeding units. REJECTED |
| `flood_v2` (tags `fl2_*`, run under the name `flood`) | swap wheat/carrot -> strawberry (median) / tomato (p75) all game, PASS-only units, reserve 6 | iteration 1, live27 below |
| `flood_v3` | no swap, strawberry p75, 2 extra hands that plant | smoke, 1 seat: rival 55.0k. The diagnostic (`JR2_LOG`) shows **tiles are binding**: 0-2 empty tiles from d5 except right after the d7-9 land buy. REJECTED without a full run |
| `flood_v4` (tags `fl4_*`) | v2 with swap through d15, tomato 0.8 x p75, + 2 extra hands d8-27 that fertilize / water / harvest / carry | iteration 2, live27 below |
| **`flood`** (= iteration 2b, tags `fl4b_*`) | v4 with strawberry p75 and 3 extra hands | iteration 2b, live27 below; **chosen** |

## 3. Validation on the 27 live27 seats (PFS = vrp18 tree `S/firebank1/tree/src` + the vrp20 OFF string, original seat; paired, same seed/town/seat)
**Rival d18-29 sales** (units @ price; our price in the last column):

| product | live | g0capsfix | flood_v2 | flood_v4 | **flood** | our price live / g0capsfix / v2 / v4 / **flood** |
|---|---|---|---|---|---|---|
| STRAWBERRY | 147.5 @ 80 | 66.0 @ 154 | 99.3 @ 112 | 115.9 @ 97 | **142.9 @ 86** | 87 / 141 / 117 / 109 / **104** |
| MELON | 14.0 @ 159 | 3.8 @ 215 | 1.4 @ 218 | 1.9 @ 215 | **1.7 @ 210** | 142 / 168 / 176 / 177 / **180** |
| MILK | 121.1 @ 84 | 142.4 @ 62 | 134.5 @ 66 | 113.6 @ 82 | **111.9 @ 81** | 102 / 70 / 72 / 97 / **93** |
| TOMATO | 52.0 @ 82 | 1.4 @ 148 | 68.7 @ 77 | 54.1 @ 78 | **49.5 @ 79** | 113 / 155 / 109 / 119 / **138** |
| WHEAT | 567.6 @ 37 | 271.1 @ 37 | 143.9 @ 42 | 234.7 @ 39 | 163.7 @ 42 | 35 / 35 / 42 / 38 / 42 |
| CARROT | 124.7 @ 45 | 62.8 @ 53 | 22.3 @ 59 | 31.9 @ 55 | 20.4 @ 57 | 44 / 49 / 54 / 53 / 55 |
| EGG | 102.9 @ 47 | 83.3 @ 48 | 78.1 @ 48 | 52.2 @ 49 | 50.0 @ 50 | 50 / 50 / 50 / 51 / 52 |
| WOOL | 90.9 @ 98 | 74.2 @ 104 | 72.1 @ 115 | 63.4 @ 122 | 59.0 @ 134 | 109 / 128 / 133 / 143 / 158 |
| FERTILIZER | 140.8 @ 23 | 104.5 @ 22 | 109.1 @ 25 | 51.9 @ 39 | 54.2 @ 41 | 26 / 24 / 24 / 42 / 44 |

**Price error at our live volume.** This is the sum over products of our live units x (our closed price - our live price), in coins per game; the first pair is signed | abs over the 4 target products, the second over all 9:
- ctrl +14.2k | 14.2k, all 9 +15.1k | 17.6k;
- g0capsfix +9.0k | 15.3k, all 9 +11.1k | 17.8k;
- flood_v2 +4.2k | 10.5k, all 9 +9.4k | 16.1k;
- flood_v4 +6.2k | **7.1k**, all 9 +12.7k | **13.6k**;
- **flood +6.0k | 7.7k**, all 9 +15.6k | 17.4k.

**Money** (paired vs g0capsfix, `an_flood.py pair`; `res/pair_l27.txt`). Every row is PFS vs the named rival, 27 games:

| rival | ours | rival | margin | W | dours (t) | dtheirs (t) | dmargin (t) | flips | ours d0-9 / d10-17 / d18-29 | rival d0-9 / d10-17 / d18-29 |
|---|---|---|---|---|---|---|---|---|---|---|
| g0capsfix | 112,235 | 84,293 | +27,942 | 27 | - | - | - | - | 5,987 / 27,101 / 79,147 | 626 / 41,157 / 42,511 |
| ctrl (PRICEGAP1 pfs_l27) | 119,133 | 86,279 | +32,853 | 27 | +6,898 (+3.02) | +1,986 (+1.37) | +4,912 (+1.76) | +0/-0 | 6,155 / 27,951 / 85,028 | 1,481 / 39,876 / 44,922 |
| flood_v2 | 110,229 | 82,514 | +27,715 | 27 | -2,006 (-1.73) | -1,780 (-1.66) | -226 (-0.14) | +0/-0 | 5,768 / 26,661 / 77,799 | 846 / 39,754 / 41,914 |
| flood_v4 | 115,996 | 79,432 | +36,565 | 27 | +3,761 (+2.22) | -4,862 (-2.94) | +8,623 (+3.67) | +0/-0 | 6,097 / 27,581 / 82,318 | 632 / 35,761 / 43,038 |
| **flood** | 119,086 | 71,865 | +47,221 | 27 | +6,851 (+2.91) | -12,428 (-6.50) | +19,280 (+5.64) | +0/-0 | 6,074 / 27,828 / 85,184 | 566 / 30,877 / 40,422 |
| live (programme rival) | 97,678 | 101,185 | -3,507 | 6 | | | | | | |

The window columns are the cash deltas between dawn d10 (o240), dawn d18 (o432) and the final, as in `S/programme1/rc/phase.py`.

**Why the rival's income falls while its flood rises:**
- The rival is tile- and cash-bound (d5 cash 284-395, 0-2 empty tiles). Every flood unit displaces something else:
  - swapped wheat/carrot plantings (wheat d10-17: 72.6 -> 28.1);
  - shed fertilizer spent on strawberries instead of sold (fertilizer d10-17: 90 -> 19.6);
  - the extra hands' Fibonacci hire cost;
  - model-assigned herd jobs lost when the extra units are overridden (eggs 83 -> 50, wool 74 -> 59 in d18-29).
- Its d10-17 cash falls 41.2k -> 30.9k.
- **Only more land / crew / fertilizer (the programme's larger engine) moves both flood and income.** A caretaker on a fixed-capacity clone can re-shape the mix, not the size.

## 4. The boards_m40 read (40 MELON band boards x 2 seats = 80 games, PFS vs flood) and the re-judged cells
PFS here is the vrp18 tree `S/firebank1/tree/src` + the vrp20 OFF string, the same body as JUDGERIVAL1 / PRICEGAP1 / SALESIDE1, so the banked g0capsfix rows pair. All rows are paired on the same 80 games; `an_flood.py pair`.

| rows | rival | n | ours | rival | margin | W | dours (t) | dtheirs (t) | dmargin (t) | flips | ours d0-9 / d10-17 / d18-29 | rival d0-9 / d10-17 / d18-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PFS control | g0capsfix (JUDGERIVAL1 banked) | 80 | 115,169 | 90,217 | +24,952 | 75 | - | - | - | - | 5,670 / 26,796 / 82,703 | 906 / 41,393 / 47,919 |
| **PFS control** | **flood** (vs the g0capsfix control) | 80 | **124,130** | **77,050** | +47,080 | 80 | +8,961 (+7.49) | -13,167 (-10.38) | +22,128 (+10.95) | +5/-0 | 5,936 / 27,612 / 90,583 | 695 / 29,696 / 46,659 |

- The live programme rival on these 40 seats earns 104,125 (JUDGERIVAL1). On boards_m40 `flood` moves the rival **away** from live, as on live27.
- d18-29 rival sales on boards_m40 (units @ price; our price in brackets):

| product | g0capsfix | flood |
|---|---|---|
| strawberry | 69.2 @ 167 (150) | **149.5 @ 101 (121)** |
| tomato | 2.2 @ 121 (118) | **51.2 @ 77 (98)** |
| milk | 127.1 @ 82 (94) | 100.4 @ 112 (123) |
| melon | 2.1 @ 203 (169) | 1.4 @ 215 (184) |
| wool | 90.3 @ 120 (134) | 67.9 @ 144 (160) |
| fertilizer | 95.3 @ 25 (26) | 54.3 @ 43 (45) |
| wheat | 256.7 @ 37 (35) | 148.2 @ 42 (42) |

**Re-judged cells, each paired with its own rival's PFS control:**

| cell | switches on the OFF string | rival | n | ours | rival | dours (t) | dtheirs (t) | dmargin (t) | flips |
|---|---|---|---|---|---|---|---|---|---|
| PRICEGAP1 rd | WHEAT_LATE_ASK=0.5,GEESE_TARGET=4,GEESE_FIRST_DAY=10 | g0capsfix (PRICEGAP1 banked) | 80 | 114,293 | 91,767 | -876 (-1.97) | +1,550 (+2.92) | -2,426 (-4.43) | +2/-1 |
| PRICEGAP1 rd | same | **flood** | 80 | 123,236 | 77,223 | **-894 (-1.97)** | **+173 (+0.33)** | **-1,066 (-1.40)** | +0/-0 |
| SALESIDE1 best (ask 0.96, d10-29) | SALE_TOP5=0\|0.96\|10\|29 (tree kagg3_wt_saleside1/src; its off = the PFS rows 80/80) | g0capsfix (SALESIDE1 banked) | 80 | 114,315 | 90,808 | -854 (-3.01) | +591 (+1.56) | -1,445 (-2.74) | +1/-1 |
| SALESIDE1 best | same | **flood** | 80 | 121,757 | 78,231 | **-2,374 (-5.98)** | **+1,180 (+2.80)** | **-3,554 (-4.88)** | +0/-0 |

- **Reading of the SALESIDE1 cell.** Holding back sales into a flooded curve costs more (own coins -0.85k -> -2.4k), and the rival still collects more of the curve (+1.2k). The cell stays CLOSED and reads worse under flood.
  - The run was split: 40 games local, 20 + 20 remote. It is bit-identical across hosts.

- **Reading of rd.** Own coins are identical under both rivals (-0.9k, t -2.0): the eggs do not pay for the geese, feed and displaced milk whichever rival floods strawberry.
  - What the flood removes is the rival-side gift. vs g0capsfix, the rival's strawberry / milk sold into the curve rd no longer drains (+1.55k, t 2.9). vs flood, the rival is already flooding strawberry and milk at the live volume (+0.17k, t 0.3).
  - The margin loss halves (-2.4k -> -1.1k), still negative. rd stays NO SHIP on either rival.


## 5. Recommended default and the remaining gap to live
**Recommended default rival: keep `g0capsfix` for the margin / flip read, and ADD `--rival flood` as the second read for every late-game product-mix lever.**
- Read it on **dours**, plus the d18-29 ledger (`an_flood.py prod`), never on margin or flips.
- Commands:
  - `bash S/reactclone1/judge.sh --rival flood <tree_src> <tag>`, then `bash S/reactclone1/judge.sh collect <tag>`. The collect finds no banked flood baselines under `S/judgerival1/res/flood/`, so pair with `S/judgerival2/res/jr2_pfs_fl.csv` via `python3 S/judgerival2/an_flood.py pair S/judgerival2/res/jr2_pfs_fl.csv <tag>.csv`.
  - On the one local worker: `bash S/judgerival2/run_local.sh flood <tag> <boards> 0,1`.
- `default_rival` is not written by this stream. The judge.sh default remains whatever `S/judgerival1/default_rival` says (absent = `ctrl`).

**What `flood` fixes vs g0capsfix (live27, d18-29):**
- rival strawberry 66 -> 143 units (live 148), price 154 -> 86 (80); our strawberry price 141 -> 104 (live 87);
- rival tomato 1.4 -> 49.5 (52.0); our tomato price 155 -> 138 (113);
- the milk over-flood is undone: our milk price 70 -> 93 (live 102).
- The 4-product price error at our live volume falls from 15.3k to 7.7k abs (flood_v4: 7.1k).

**Remaining gap to live:**
1. **Income.**
   - Rival: 71.9k live27 / 77.1k m40, vs live 101.2k / 104.1k (g0capsfix 84.3k / 90.2k).
   - Ours: 119.1k live27 / 124.1k m40, vs live 97.7k on live27 (g0capsfix 112.2k / 115.2k).
   - The flood is bought with the rival's own capacity: wheat / carrot tiles, shed fertilizer, herd jobs and hire cost. The rival's d10-17 cash falls from 41.2k to 30.9k.
   - Consequence: our wool (158 vs live 109), fertilizer (44 vs 26) and wheat (42 vs 35) prices are now too high. The all-9 price error does not fall (17.4k vs 17.8k).
2. **Melon.**
   - d18-29 rival melon 1.7 vs live 14.0; our melon price 180 vs 142 (-3.2k live term). Melon d10-17: 51.7 vs 64.1.
   - The overlay's melon target was not in the chosen cfg: tiles are binding.
3. **The programme's size.**
   - Wheat: 568 vs 164 units in d18-29, and 334 vs 28 in d10-17.
   - Fertilizer 141 vs 54, eggs 103 vs 50.
   - Closing this needs a rival with more land / crew / fertilizer, not a re-shaped clone:
     - the FQ d10 Q4 + crew of BEATPROG1;
     - a clone trained on the elite subset (BCBODY7);
     - or `flood` + a land / hire block that adds tiles instead of swapping them.
   - Next step (not run, box over): `flood` + `BUY_LAND` Q4 at d10 + the extra hands planting on the new tiles (no swap).
- **Middle option `flood_v4`** (strawberry median, 2 hands): the best all-9 price error (13.6k abs) and a smaller income distortion (rival -4.9k, ours +3.8k vs g0capsfix on live27). Its strawberry is 116 @ 97 (-21 % units, +21 % price vs live), so it misses the 15 % bar on strawberry.


## Files
- `S/judgerival1/rcr.py` (flood caretaker; ctrl / g0 / capsfix / g0capsfix untouched), `S/judgerival1/rivals.json` (+ flood_v1, flood_v2, flood_v3, flood_v4, flood).
- `S/judgerival2/`:
  - `an_flood.py` (product x window tables vs live; paired money rows);
  - `rl.sh` (remote launcher, one worker per call, nice 19);
  - `run_local.sh` (the one local worker, nice 19 / ionice idle);
  - `fetch.sh`, `sm.py`;
  - `res/*.csv` + `*_sal.jsonl` (rows and ledgers), `res/prod_l27_d18.txt`, `res/pair_l27.txt`;
  - `logs/diag_smoke*.jsonl` (target-reach diagnostic);
  - `checkpoint.txt`.
- Identity: `res/id_g0cf.csv` = JUDGERIVAL1 `res/g0capsfix/pfs.csv` on tape_highfrequencyf_114080894, both seats, every money / cash column (2/2), run with the edited rcr.py. The final-file re-check is in `res/id2_g0cf.csv`.
- Local vs remote runs are bit-identical (smoke2 = fl2_l27a row, smoke4 = fl4_l27a row).
