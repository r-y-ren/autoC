# JUDGERIVAL3: a bigger flood rival for the closed-loop judge (2026-09-29, 01:41Z-02:56Z)

Stream dir `S/judgerival3/`. Harness only: `S/judgerival1/rcr.py` + `rivals.json` gain the `big*` rival cfgs, a real-hands mode and a decision-neutral
capacity diagnostic. No src, dist, package, clone-params or trainer change, no upload, no GPU.

## Verdict
- **No `big` variant reaches the income bar.** The best one (`big` = iteration 2) makes the rival bigger but poorer. On the 27 live27 seats:
  - rival income 66.3k (bar >= 95k; flood 71.9k, g0capsfix 84.3k, live 101.2k);
  - ours 115.6k (bar within 10 % of the live 97.7k; flood 119.1k, g0capsfix 112.2k).
  - It has 89 productive tiles at d18 (live programme 75-83, g0capsfix 70) and ~15.7 units on the farm at h12 (g0capsfix 12.1).
- **Flood match.** Strawberry and tomato units stay within 15 % of live, and so do the wheat / carrot / egg / wool volumes and prices. The all-9 price
  error at our live volume falls from 17.4k (flood) to 13.2k. Milk falls short: 91 units vs live 121, and our milk price is 128 vs live 102. Melon is still
  not reached (1.1 units vs 14).
- **`S/judgerival1/default_rival` is NOT written.**
  - `big` is further from the live rival income than g0capsfix (66k vs 84k, live 101k).
  - Its 4-product flood error (9.2k) is worse than flood's (7.7k).
  - **Protocol (unchanged): `g0capsfix` for margin / flips + `flood` for dours** on late product-mix levers.
  - `big` is an optional third read. Its all-9 price error is the lowest (13.2k), so use it for levers that touch wheat / carrot / egg / wool / fertilizer.
- **Harness finding (affects `flood`).**
  - flood's "3 extra hands" were never hired. Its h0 HIRE orders are appended after the clone's own ~10 h0 orders and then cut by the
    10-orders-per-turn cap.
  - The overlay therefore drove the clone's OWN last 3 hands. That hijack is the displaced herd / wheat / fertilizer work JUDGERIVAL2 measured.
  - `flood` is left bit-identical (it is a calibrated price judge whatever its mechanism). `big` uses real hires (`xh_mode: real`).
- **Why the bigger rival is poorer.** The clone's economy converts extra land and hands into strawberry / tomato, and the flood itself collapses their
  price (rival strawberry 154 -> 97). Meanwhile:
  - the hands are Fibonacci-priced: the clone already hires ~11 a day, so hands 12-14 cost 89 / 144 / 233 coins a day;
  - Q4 costs 4,000.
  - Result: rival spend is +10.5k in d10-17 and +10.4k in d18-29 vs g0capsfix, for +6.4k of extra d18-29 gross.
  - The live programme's extra income is its **wheat engine**: d10-29 wheat 1,138 units live vs ~300 for every clone variant. A caretaker cannot build
    that: with a wheat-only fill, the tiles are full (3-5 empty at d15-26), and the variant's wheat units do not rise (`big_v3`).
- **Re-judged cells vs `big`** (80 games, section 4): PRICEGAP1 rd vs big: dours -67 (t -0.13), dtheirs +551 (+0.87), dmargin -618 (t -0.77), flips 0/0.
  - vs g0capsfix: -876 / +1,550 / -2,426 (t -4.43). vs flood: -894 / +173 / -1,066 (t -1.40).
  - D10WAVE1 C (`Q4_PROG_ON=True`) vs big: -4,920 (t -7.43) / +3,213 / -8,133 (t -6.41), flips 0/0. vs g0capsfix: -5,567 / +3,526 / -9,094 (t -9.33), -10 wins.
  - Neither becomes a candidate.
- **m40 PFS control vs `big`** (80 games): ours 118,879, rival 73,062, margin +45,817, W 80/80.
  - vs the g0capsfix control: dours +3,710 (t 3.54), dtheirs -17,155 (t -16.36), flips +5/-0.
  - Ours by window d0-9 / d10-17 / d18-29: 6,074 / 26,961 / 85,844. Rival: 627 / 28,867 / 43,568.
  - The live programme on these 40 seats earns 104.1k.

## 1. Measurements: what flood displaced (live27 seats, rival = clone seat opposite PFS)
**Capacity diagnostic.**
- Source: env `JR3_LOG` in `rcr.py` `_cap_market`, one row per clone game at h12 of every day. It is decision-neutral: the identity rows below were run
  with it on.
- Summary script: `S/judgerival3/diag.py`. Tables: `S/judgerival3/res/diag_l27.md`.

| rival | games | productive tiles d9 / d18 | animal tiles d18 | units at h12 d10 / d18 | cash dawn d10 / d18 (t240 / t432) | 4 quadrants |
|---|---|---|---|---|---|---|
| g0capsfix | 13 | 53.7 / 69.8 | 16.7 | 11.9 / 12.1 | 626 / 41,783 | 1/13 |
| flood | 3 | 50.0 / 69.7 | 14.3 | 11.0 / 12.7 | 566 / 31,443 | 0/3 |
| big_v1 (hijack hands + Q4) | 13 | 47.6 / 79.6 | 12.2 | 11.4 / 12.7 | 781 / 26,105 | 13/13 (d11-12) |
| **big** (real hands + Q4) | 27 | 51.1 / **89.1** | 13.7 | 10.9 / **15.7** | 410 / 27,834 | 27/27 (d10-12) |
| big_h (5 real hands + Q4) | 13 | 51.5 / 89.5 | 13.5 | 10.6 / 17.3 | 301 / 18,516 | 13/13 (d11) |
| big_v1h (5 hijacked hands + Q4) | 13 | 45.2 / 76.0 | 11.0 | 11.6 / 12.2 | 898 / 18,767 | 13/13 (d11-15) |

The cash columns are the paired rows' window means; the cash columns of the 3-game flood row come from the 27-game rows.

**Displaced work, flood vs g0capsfix** (rival units, 27 games; `S/judgerival2` banked ledgers):

| product | d10-17: g0capsfix -> flood | d18-29: g0capsfix -> flood |
|---|---|---|
| wheat | 72.6 -> 28.1 | 271 -> 164 |
| fertilizer | 90.0 -> 19.6 | 104 -> 54 |
| egg | 37.1 -> 24.6 | 83 -> 50 |
| wool | 39.6 -> 26.6 | 74 -> 59 |
| carrot | - | 63 -> 20 |
| milk | 65.7 -> 61.3 | - |

- Cash at dawn d18 falls 41.8k -> 31.4k.
- The hands per day are unchanged (11.0-12.7 vs 11.0-12.3 at h12), which proves the flood's HIREs never executed.

## 2. The `big` overlay (`rcr.py`, keys in the cfg's `"flood"` block; absent keys = flood behaviour, so flood / flood_v* stay bit-identical)
- **`q4_d` / `q4_end` / `q4_r`: the 4th quadrant.** BUY_LAND is placed first among the non-SELL orders at the first step with d in [10, 17], h <= 20,
  3 quadrants, and cash >= 4,000 + 800.
  - The clone's own LAND overlay (L7t70) stops at 3 quadrants.
  - The rival's cash at dawn d10 is only 0.4-0.6k, so the buy lands on d10-12. Denied steps are logged (`den.q4`, ~20 steps per game).
- **`xh_mode: real`: real extra hands.**
  - `xh` HIREs are ordered at h1 (`xh_hour`), after the clone's own h1 hires.
  - They are ordered only while cash, minus this step's seed / animal / land spend and the clone's hires, covers each Fibonacci price + 300 (`xh_r`).
    Denials are logged (`den.hire`, ~3 per game).
  - Their unit indices (1 + hands + clone hires this step + j) are stored in the game's ledger dict.
  - `_care_units` finds the game's ledger through a successor chain built in `_cap_market`: kh calls `_care_units(b)` while `MAIN._LED` still holds
    game b-1's ledger.
  - Only those hands are overlay-driven. The diagnostic confirms they exist: +3.6 units at h12 from d12.
- **`fill` / `fill_last` / `fill_res` / `fill_r` / `fill_nq`: planting the new tiles.**
  - Once the farm has 4 quadrants, extra hands and idle units plant empty tiles beyond `fill_res`, after the flood targets are met.
  - The mix is wheat : carrot : strawberry 3:1:1 (last days 26 / 26 / 17), choosing the crop with the lowest standing / share.
  - Seeds are bought at h0-1, only while cash - spend >= 600; denials are logged.
  - The extra hands also water and harvest the fill crops.
- **`keepwork`.** An extra hand whose model command is herd work (FEED / CARE / COLLECT_FERTILIZER / BUILD_* / PICKUP WHEAT) keeps it.
- **`sell_keep`.** From d10, the rival sells the shed stock above keep (wheat 40, carrot 0).
- **`harv_min`** (big_v3 only). The overlay harvests wheat / carrot only at full yield.
- Everything else is flood: the strawberry p75 / tomato 0.8 x p75 standing targets, the wheat/carrot -> flood swap through d15, fertilizing from the
  shed, and the full-shed SELL of strawberry / tomato / melon from d10.

**Iterations (all kept in rivals.json):**

| cfg | definition | live27 result |
|---|---|---|
| `big_v1` (tags `big_l27*`) | flood hands (hijack) + Q4 + fill + keepwork | 13 g: rival 64.6k, ours 127.0k. REJECTED |
| `big_v1h` (`bigh_l27*`) | big_v1 + xh 5 | 13 g: rival 48.4k, ours 138.0k. REJECTED |
| **`big`** (`big2_*`) | real hands (3) + Q4 + fill + keepwork | 27 g: rival 66.3k, ours 115.6k. **chosen** (closest to live on ours and on the all-9 prices) |
| `big_h` (`big2h_*`) | big + 2 more real hands (xh 5) | 13 g: rival 35.0k (hands at 1.45k/day). REJECTED |
| `big_v3` (`big3_*`) | big + wheat-only fill beyond 2 tiles through d27 + full-yield wheat/carrot harvest | 13 g: rival 68.6k (big 67.6k on the same 13), ours 114.5k (120.0k); rival wheat 223 vs 261 (tiles full). Not better |

**Identity.** The edited rcr.py reproduces the banked JUDGERIVAL2 rows on every money / cash column (`S/judgerival3/ident.py`):
- g0capsfix: 3/3 bit-identical (`res/id_g0cf.csv`), plus 13/13 (`res/meas_g0cf_a.csv`) with the diagnostic on;
- flood: 3/3 (`res/id_fl.csv`);
- final re-check with the final rcr.py (real-hands mode, harv_min, diagnostic): g0capsfix 2/2 (`res/id2_g0cf.csv`), flood 2/2 (`res/id2_fl.csv`).

## 3. Validation on the 27 live27 seats
PFS = vrp18 tree `S/firebank1/tree/src` + the vrp20 OFF string. Same seed / town / seat as the banked rows. Output from `an_flood.py pair` and `prod`,
in `res/pair_l27.md` and `res/prod_l27.md`.

**Money** (every row is PFS vs the named rival, paired with the g0capsfix rows):

| rival | n | ours | rival | margin | W | dours (t) | dtheirs (t) | dmargin (t) | flips | ours d0-9 / d10-17 / d18-29 | rival d0-9 / d10-17 / d18-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| g0capsfix | 27 | 112,235 | 84,293 | +27,942 | 27 | - | - | - | - | 5,987 / 27,101 / 79,147 | 626 / 41,157 / 42,511 |
| flood | 27 | 119,086 | 71,865 | +47,221 | 27 | +6,851 (+2.91) | -12,428 (-6.50) | +19,280 (+5.64) | +0/-0 | 6,074 / 27,828 / 85,184 | 566 / 30,877 / 40,422 |
| big_v1 | 13 | 126,964 | 64,591 | +62,373 | 13 | +15,103 (+4.38) | -23,729 (-9.87) | +38,832 (+8.84) | +0/-0 | 5,908 / 28,209 / 92,847 | 781 / 25,324 / 38,485 |
| big_v1h | 13 | 138,048 | 48,394 | +89,654 | 13 | +26,187 (+6.69) | -39,926 (-12.37) | +66,112 (+11.30) | +0/-0 | 6,209 / 29,058 / 102,781 | 898 / 17,869 / 29,627 |
| **big** | 27 | **115,574** | **66,342** | +49,232 | 27 | +3,339 (+1.65) | -17,951 (-11.31) | +21,291 (+8.88) | +0/-0 | 6,071 / 27,620 / 81,883 | 410 / 27,424 / 38,508 |
| big_h | 13 | 122,300 | 34,992 | +87,308 | 13 | +10,439 (+3.23) | -53,328 (-16.89) | +63,767 (+16.61) | +0/-0 | 6,118 / 27,922 / 88,260 | 301 / 18,215 / 16,476 |
| big_v3 | 13 | 114,460 | 68,635 | +45,824 | 13 | +2,599 (+0.90) | -19,684 (-8.42) | +22,283 (+6.05) | +0/-0 | 5,995 / 26,913 / 81,552 | 536 / 27,888 / 40,212 |
| live (programme rival) | 27 | 97,678 | 101,185 | -3,507 | 6 | | | | | | |

**Rival d18-29 sales** (units @ price; our price in the last column; 27 games):

| product | live | g0capsfix | flood | **big** | our price live / g0capsfix / flood / **big** |
|---|---|---|---|---|---|
| STRAWBERRY | 147.5 @ 80 | 66.0 @ 154 | 142.9 @ 86 | **146.4 @ 97** | 87 / 141 / 104 / **111** |
| TOMATO | 52.0 @ 82 | 1.4 @ 148 | 49.5 @ 79 | **55.4 @ 80** | 113 / 155 / 138 / **111** |
| MILK | 121.1 @ 84 | 142.4 @ 62 | 111.9 @ 81 | **91.0 @ 102** | 102 / 70 / 93 / **128** |
| MELON | 14.0 @ 159 | 3.8 @ 215 | 1.7 @ 210 | **1.1 @ 229** | 142 / 168 / 180 / **177** |
| WHEAT | 567.6 @ 37 | 271.1 @ 37 | 163.7 @ 42 | **238.9 @ 38** | 35 / 35 / 42 / **37** |
| CARROT | 124.7 @ 45 | 62.8 @ 53 | 20.4 @ 57 | **59.1 @ 51** | 44 / 49 / 55 / **49** |
| EGG | 102.9 @ 47 | 83.3 @ 48 | 50.0 @ 50 | **69.9 @ 50** | 50 / 50 / 52 / **50** |
| WOOL | 90.9 @ 98 | 74.2 @ 104 | 59.0 @ 134 | **68.2 @ 119** | 109 / 128 / 158 / **131** |
| FERTILIZER | 140.8 @ 23 | 104.5 @ 22 | 54.2 @ 41 | **52.3 @ 34** | 26 / 24 / 44 / **34** |

**Price error at our live volume** (coins per game; signed | abs; first pair = the 4 target products, second pair = all 9):
- g0capsfix +9.0k | 15.3k, all 9 +11.1k | 17.8k;
- flood +6.0k | 7.7k, all 9 +15.6k | 17.4k;
- **big +9.0k | 9.2k, all 9 +13.1k | 13.2k**.

**Against the targets:**

| target | bar | big | pass? |
|---|---|---|---|
| rival income | >= 95k | 66.3k | no |
| ours | within 10 % of 97.7k | 115.6k (+18 %) | no |
| strawberry | within 15 % | units -1 %, price +21 % | units only |
| tomato | within 15 % | units +7 %, price -2 % | yes |
| milk | within 15 % | units -25 %, price +21 % | no |
| melon | within 15 % | 1.1 vs 14 | no |

**Where the rival's money goes** (gross = units x price from the ledger, spend = gross - cash change; big vs g0capsfix):

| window | gross | spend |
|---|---|---|
| d10-17 | 43.3k vs 46.6k | 15.9k vs 5.4k |
| d18-29 | 53.7k vs 47.3k | 15.2k vs 4.8k |

- The +20.9k of extra spend comes from:
  - Q4 (4.0k);
  - 3 hands a day at 89-233 coins each (~0.45k/day, d8-27);
  - strawberry / tomato / fill seeds and replants.
- The extra product sells into a book the rival floods itself.

## 4. The boards_m40 read (40 MELON band boards x 2 seats = 80 games) and the re-judged cells
PFS here is the vrp18 tree `S/firebank1/tree/src` + the vrp20 OFF string, the same body as in JUDGERIVAL1 / 2, PRICEGAP1 and SALESIDE1, so the banked
rows pair. The run was split into 4 x 20-game chunks (`--nw 4 --N 20`) over the remote (w0/w1) and the one local worker (w2/w3); the rows are
host- and batch-independent. Tables: `res/pair_m40.md` and `res/prod_m40.md`.

**PFS control rows**, paired with the JUDGERIVAL1 g0capsfix control:

| rows | rival | n | ours | rival | margin | W | dours (t) | dtheirs (t) | dmargin (t) | flips | ours d0-9 / d10-17 / d18-29 | rival d0-9 / d10-17 / d18-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PFS control | g0capsfix (JUDGERIVAL1 banked) | 80 | 115,169 | 90,217 | +24,952 | 75 | - | - | - | - | 5,670 / 26,796 / 82,703 | 906 / 41,393 / 47,919 |
| PFS control | flood (JUDGERIVAL2 banked) | 80 | 124,130 | 77,050 | +47,080 | 80 | +8,961 (+7.49) | -13,167 (-10.38) | +22,128 (+10.95) | +5/-0 | 5,936 / 27,612 / 90,583 | 695 / 29,696 / 46,659 |
| **PFS control** | **big** | 80 | **118,879** | **73,062** | +45,817 | 80 | +3,710 (+3.54) | -17,155 (-16.36) | +20,865 (+12.01) | +5/-0 | 6,074 / 26,961 / 85,844 | 627 / 28,867 / 43,568 |

- The window columns are the cash deltas between dawn d10 (o240), dawn d18 (o432) and the final, as in `S/programme1/rc/phase.py`.
- **big vs flood** on the same 80 games: ours -5,251 (t -5.88), rival -3,988 (t -4.20).
  - `big` pulls our income 5.3k closer to live.
  - The rival is 4.0k further from live: it earns 73.1k against the live programme's 104.1k on these 40 seats.

**d18-29 rival sales on boards_m40** (units @ price, our price in brackets; `S/judgerival3/prod40.py`):

| product | g0capsfix | flood | **big** |
|---|---|---|---|
| strawberry | 69.2 @ 167 (150) | 149.5 @ 101 (121) | **146.7 @ 104 (120)** |
| tomato | 2.2 @ 121 (118) | 51.2 @ 77 (98) | **57.3 @ 74 (93)** |
| milk | 127.1 @ 82 (94) | 100.4 @ 112 (123) | **83.8 @ 129 (140)** |
| melon | 2.1 @ 203 (169) | 1.4 @ 215 (184) | **0.7 @ 201 (174)** |
| wheat | 256.7 @ 37 (35) | 148.2 @ 42 (42) | **222.5 @ 39 (38)** |
| carrot | 70.2 @ 54 (52) | 25.0 @ 63 (60) | **72.6 @ 54 (53)** |
| egg | 76.0 @ 47 (48) | 53.6 @ 47 (50) | **64.4 @ 47 (49)** |
| wool | 90.3 @ 120 (134) | 67.9 @ 144 (160) | **79.7 @ 137 (144)** |
| fertilizer | 95.3 @ 25 (26) | 54.3 @ 43 (45) | **54.5 @ 35 (36)** |

**Re-judged cells**, each paired with its own rival's PFS control on the same 80 games:

| cell | switches on the OFF string | rival | n | ours | rival | dours (t) | dtheirs (t) | dmargin (t) | flips |
|---|---|---|---|---|---|---|---|---|---|
| PRICEGAP1 rd | WHEAT_LATE_ASK=0.5,GEESE_TARGET=4,GEESE_FIRST_DAY=10 | g0capsfix (PRICEGAP1 banked) | 80 | 114,293 | 91,767 | -876 (-1.97) | +1,550 (+2.92) | -2,426 (-4.43) | +2/-1 |
| PRICEGAP1 rd | same | flood (JUDGERIVAL2 banked) | 80 | 123,236 | 77,223 | -894 (-1.97) | +173 (+0.33) | -1,066 (-1.40) | +0/-0 |
| PRICEGAP1 rd | same | **big** | 80 | 118,812 | 73,613 | **-67 (-0.13)** | **+551 (+0.87)** | **-618 (-0.77)** | +0/-0 |
| D10WAVE1 C (best-margin cell: FQ tail) | Q4_PROG_ON=True | g0capsfix (D10WAVE1 banked, master 8d670dad tree = firebank1 tree) | 80 | 109,602 | 93,743 | -5,567 (-14.64) | +3,526 (+4.74) | -9,094 (-9.33) | +0/-10 |
| D10WAVE1 C | same (firebank1 tree) | **big** | 80 | 113,959 | 76,275 | **-4,920 (-7.43)** | **+3,213 (+3.79)** | **-8,133 (-6.41)** | +0/-0 |

- **D10WAVE1 C** has no flood read: D10WAVE1's flood table holds only ctl / A10 (20 games). It is the least-bad non-null D10WAVE1 cell on margin; A10 is
  the control to the coin, and no cell reached its bar.
- **Reading of C.** It reads the same against `big` as against g0capsfix: own -4.9k vs -5.6k, rival +3.2k vs +3.5k, margin -8.1k vs -9.1k. The flips
  vanish because every game is a win vs `big`.
  - A Q4 bolted onto PFS loses its land / hands / seed spend (our d10-17 cash -6.0k) against both rivals.
  - C stays NONE.
- **Reading of rd.**
  - vs `big`, rd's own coins are flat (-0.07k, t -0.1), where they were -0.9k (t -2.0) under both older rivals.
  - The rival still gains (+0.55k), and the margin is still negative (-0.6k).
  - The product ledger of the rd-vs-big cell was not decomposed (box).
  - rd stays NO SHIP on all three rivals.


## 5. Protocol
- **Margin / flips: `--rival g0capsfix`.** `bash S/reactclone1/judge.sh --rival g0capsfix <tree_src> <tag>`, then `bash S/reactclone1/judge.sh collect <tag>`.
- **dours on late product-mix levers: `--rival flood`.** Pair with `S/judgerival2/res/jr2_pfs_fl.csv` via `python3 S/judgerival2/an_flood.py pair`.
- **Optional third read: `--rival big`.** Use it for levers that touch wheat / carrot / egg / wool / fertilizer, where `big` has the lowest all-9 price error.
  Pair with `S/judgerival3/res/bm_pfs.csv` (m40) or `res/big2_l27.csv` (live27): `python3 S/judgerival2/an_flood.py pair S/judgerival3/res/bm_pfs.csv <tag>.csv`.
- **On the one local worker:** `bash S/judgerival3/run_local.sh big <tag> <boards> 0,1`.
- `default_rival` stays unwritten (absent = `ctrl`).
- **What a live-sized rival needs:** the programme's wheat engine (d10-29 wheat 1,138 units, d10-17 334) and fertilizer (115 d10-17). A caretaker on the
  r5a3 clone cannot supply these: its tiles are full at d15 and its hands are Fibonacci-priced. They need a clone trained on the elite subset (BCBODY7/8)
  or a scripted programme body (PROGRAMME1) as the rival seat.

## Files
- `S/judgerival1/rcr.py`:
  - big keys: `q4_*`, `xh_mode` / `xh_hour` / `xh_r`, `fill*`, `keepwork`, `sell_keep`, `harv_min`;
  - the `JR3_LOG` diagnostic.
  - ctrl / g0 / capsfix / g0capsfix / flood* are untouched and bit-identical.
- `S/judgerival1/rivals.json`: + big_v1, big_v1h, big, big_h, big_v3. The old entries are content-identical; the file was re-serialised one entry per line.
- `S/judgerival3/`:
  - `rl.sh` (remote launcher, one worker per call, `JR3_LOG` on);
  - `run_local.sh`;
  - `fetch.sh`;
  - `diag.py` (capacity table), `prod40.py` (d18-29 product table on any board set);
  - `ident.py` (identity check);
  - `res/*.csv` + `*_sal.jsonl`;
  - `res/pair_l27.md`, `res/prod_l27.md`, `res/diag_l27.md`, `res/pair_m40.md`;
  - `logs/*.diag.jsonl`;
  - `checkpoint.txt`;
  - `rcr_before.py` / `rivals_before.json` (the pre-edit copies).
