# Top-50 playing templates (2026-09-11 10:07-10:50Z) — leaderboard pull, 56 win replays, template catalogue

Measurement + rung preparation. Fresh leaderboard S/top50/lb.json (GetLeaderboard, 10:08Z); top-50 subs in
S/top50/subs.txt (rank, team, sub id, rating); ListEpisodes per sub (S/top50/eps.json); the 56 episodes read
(2 wins for ranks 1-7, 1 win for ranks 8-50; the most recent WIN of each file that is not already a judge board
or training rung — same exclusion as S/flow198/pick.py, 616 known ids) are in S/top50/rows.json (id, sub, seat,
opponent rating, result, created) and S/top50/eps/ep_<id>.json (32 MB each, 1.8 GB total — replays carry full
observations, so the 400 MB guidance would have bought 12 files; ranks 8-50 got one replay each instead).
Ledgers: S/spataro/tools/ledger.py at the top file's seat -> S/top50/led/led_<id>.{json,txt}; feature rows
S/top50/features.json (S/top50/features.py, run with --ident for the d0-d2 action-stream identity matrix).
Vocabulary as in 2026-09-11-loss10-anatomy.md and 2026-09-11-spataro-vs-ours.md.

## Method

Feature vector per seat: hands d0/d5/d10/max, hire hours, melon tiles planted d0-1 / total, main dump day-units-price,
animals bought (d0 and total), land days, crop tile totals, wheat units bought, sell turns, hour-0 sell share, tomato
tiles within 4 days of PIZZA/BRUNCH/ICE unlock, carrot tiles within 4 days of PET/FARMERS, end-of-day cash d10/d20,
d0 h0/h1 market rows. Clone check = % of byte-identical action steps over d0-d2 (72 steps) between every pair of
seats. 24 of the 50 files are 76-100 % identical to carlos-tagosaku's stream through d2 (the public clone);
the two-replay files show whether a file is open-loop (Otter Vibe 100 %, binghua 100 %, c0nrad 97 %, feel the agi
86 %) or adaptive from step 1 (Majkel1337 36 %, SpaTaro 0 %).

## Templates (13 groups; 50 files)

Legend: hands = d0/d5/d10 (max). melon = tiles d0-1/total; dump day units @price. land = quadrant unlock days.
crops = tiles planted over the game. wb = wheat units bought. sells = sell turns / % units at hour 0.

### T0a — public band clone (24 files) — ALREADY IN RUNGS (flow197/199 band boards; flow198 carlos/mtmr_s1)
Ranks 7 carlos-tagosaku, 9 redblackbst, 10 Gleb Tumanov, 11 mtmr_s1, 15 Syed Asad Ali, 18 Himanshu Kumar,
19 american gothic, 20 Subramanya N, 21 Hiểu Vy, 22 peikopon, 23 datnt114, 24 薄荷喵呜, 27 Michael Shihong Zhang,
28 MINGXI LIU, 29 Terry Luo, 30 chocolat, 32 Sergey Kutepov, 33 kanno, 37 tamura_aicon, 38 Yusuke Hayashi,
40 vasujain7, 42 Ray Roberts, 47 Tomoki Hirose, 49 c-number.
Ledger: d0 h0 micro-pump (BUY 13 / BUY 10 / SELL 10 wheat, variants BUY 5 / SELL 13; Gleb Tumanov BUY 43 / SELL 20+22),
h1 SELL 8 + 5 HIRE + 2 COW + 2 SHEEP; 12 melon d0 h7-h12 (purse to ~530); hands 5/4/11 (11); one hire per day at
h0/h1; land d6 + d11; 160 wheat / 33 strawberry / 31 carrot / 12 melon tiles; 8 cows 6 sheep 3 geese (Syed 12c 2s,
redblackbst 6c 8s, chocolat 9c 5s); wb 130-270 (american gothic 3,544 — a wheat-buy loop, 295 sell turns, 5 % h0);
60 melons dumped d10 h0 @217 (Gleb 72 @200); ~350 fertilizer; sells 200-260 turns, 12-18 % at h0; no tomato, no
shop reaction (0 tomato/carrot tiles inside 4 days of any unlock). Cash d10 13.8-16.9k, d20 33-65k.
Representative WIN ids (seat): 107785243 (0) carlos-tagosaku, 107786170 (1) redblackbst, 107784448 (1) Gleb Tumanov
[CUT, see below — the pump variant], 107787447 (0) Himanshu, 107777698 (0) Ray Roberts.

### T0b — clone + 4th quadrant d18 + 10 tomato d18, 13-14 hands (6 files) — NEW
Ranks 17 デワンシュ, 31 Bantam, 39 senkin13, 45 Hello San Francisco, 46 farmin time, 48 junxing peng.
Same clone ledger through d17 (97-100 % identical streams; デワンシュ 26 % = different action serialisation, same
ledger, wb 329), then a third land buy on d18 (quad 4) and 10 tomato tiles planted d18 (sold d24-29), crew grows to
13-14 (junxing/farmin/Hello SF/senkin 14). Not a shop reaction (tomato d18 regardless of PIZZA day). Finals 100-142k.
Representative WIN ids: 107785390 (1) デワンシュ, 107780056 (0) Bantam [both CUT], 107780536 (0) senkin13,
107766674 (1) Hello San Francisco, 107783189 (1) farmin time, 107780502 (1) junxing peng.

### T0c — clone with wool herd: 6 cows + 11 sheep, no geese (6 files) — NEW
Ranks 25 que la cuenten como quieran, 35 한밭대학교, 36 insuperabilehart, 41 Jingxiang, 43 PeriwinkleBlueOvO (4c 13s),
44 cooked. Clone opening and melon (que la cuenten pumps BUY 13 + BUY 60 / SELL 60 at h0; cooked BUY 5 / SELL 5 x2),
same land d6/d11, 162-165 wheat / 33 straw / 24-31 carrot, but the herd is 6 cows + 11 sheep bought in blocks (no
geese, 0 eggs) -> wool 26-70k (PeriwinkleBlueOvO 70.4k with YARN d2, cooked 42.4k), fertilizer 311-341; sells 159-220
turns, 10-21 % h0; insuperabilehart plants 28 carrot in the 4 days after PET/FARMERS (the only clone-family seat with
a shop-reaction signature; Jingxiang 0). Finals 90-133k.
Representative WIN ids: 107782373 (1) cooked [CUT], 107786342 (1) que la cuenten, 107783529 (0) PeriwinkleBlueOvO,
107788451 (1) 한밭대학교, 107783506 (0) insuperabilehart, 107777670 (1) Jingxiang.

### T0d — "feel the agi" derivative: clone opening, heavy herd/wheat buying, few sell turns (6 files) — PARTLY IN RUNGS
Ranks 3 feel the agi, 8 3정훈, 12 Mengfei Li (all three in flow198), 14 Tarang222, 34 Suliman Tadros,
50 🌽 High Frequency Farming (NEW).
Opening BUY_PRODUCT WHEAT 13 at h0 only; h1 SELL 8-9 + BUY_SEED WHEAT 7 (+ MELON 12 at h1 for Mengfei/High Frequency)
+ 5 HIRE + 2 COW + 2 SHEEP; 12 melon d0; 60 dump d10 @208-238; land d6/d11 (High Frequency d6/d8); hands 5/5/11
(12-13). Differences from T0a: wb 150-430 (feel the agi 417-427 = herd feed, milk 49k), geese 4-10 (feel the agi 10 in
one game, eggs 14.8k), Mengfei 12 cows + 85 wheat / 58 strawberry tiles (strawberry 90k), High Frequency 4c 12s +
79 carrot + 24 tomato d12-18 (13 hands d10), Tarang222 opening BUY 2 COW at h0 then 5 hires + 1 sheep at h1, 86 sell
turns with 68 % at h0 (one big h0 dump per day). Sells 86-152 turns, 20-68 % h0. Cash d10 13-17k.
Representative WIN ids: 107782433 (1) / 107785473 (0) feel the agi, 107783462 (1) 3정훈, 107778490 (0) Mengfei Li,
107784403 (0) High Frequency [CUT], 107786235 (0) Tarang222 [CUT], 107785093 (1) Suliman Tadros.

### T1 — Majkel1337 (#1, 3099) — IN RUNGS (flow198) — adaptive
h0 BUY 1 COW + 5 wheat; h1 SELL 1 wheat + 4 HIRE + 1 COW + 3 SHEEP (purse 3000 -> 585 by h2); 10 melon d0 h6-h10 (12
total); hands 4/6/11 (11), two hire rows/day; purse run to 1-2 coins (max end-of-day cash d0-9 1.7-2.8k only on d9);
land d6 + d9; 10-11 cows (one a day) + 4-5 sheep + 1-2 geese; 196-204 wheat / 21-30 straw / 23-52 carrot / 12 melon;
wb 129-154; 30-31 melons dumped d10 @244 (or d16 @202 when the opponent dumped first — price-reactive); fertilizer 204;
231-253 sell turns, 17-18 % h0; tomato 1-6. Streams 36 % identical between its two games from step 1 -> not open-loop.
Ids: 107773713 (0), 107779556 (0).

### T2 — SpaTaro (#2, 3091) — IN RUNGS (flow198) — adaptive, all-in labour
h0 4-5 HIRE + BUY_SEED MELON 7 (+WHEAT 7) + BUY_PRODUCT WHEAT 6 + 2 COW + 2 SHEEP; h1 1-2 more HIRE and unfilled
BUY_PRODUCT probes (CARROT/TOMATO/STRAWBERRY); hands 6-7/6/11 (12); purse 0-1 every evening d0-9 (max eod cash 195-486);
8-10 melon d0 (9-13 total), 35-48 dumped d10 @247-250; land d6 + d9; 2-6 cows + 20-22 sheep; wb 347-436 (herd feed,
16-18k); 166-192 wheat / 7-19 straw / 10-68 carrot; fertilizer 341-366; 230-253 sell turns, 30-31 % h0; 0 tomato,
carrot 9 tiles inside 4 days of a PET/FARMERS unlock in one game. 0 % stream identity between its two games.
Ids: 107762721 (0), 107784471 (0).

### T3 — Otter Vibe (#4, 3014) — IN RUNGS (flow198) — open-loop geese/tomato build
h0 5 HIRE + 2 SHEEP + 2 GOOSE + 1 COW + 6 MELON seed + 5 wheat; h1 14 WHEAT seed; hands 5/2-3/12 (14-15) — the crew is
cut to 2-3 on d3-d6 and rebuilt from d7; 6 melon d0 + 11-12 more d5-d9 (17-18), 36 dumped d10 @205-236; land d5 + d10;
10 geese + 4 cows + 2-5 sheep; 72-140 wheat / 15-21 straw / 21-102 carrot / 22-31 tomato (16 tomato inside 4 days of
BRUNCH in one game); wb 193-283; fertilizer 218-228; only 86-92 sell turns, 44-48 % h0. Finals 79-81k (lowest of the
top 10). 100 % identical d0-d2 across games.
Ids: 107756423 (0), 107784468 (0).

### T4 — c0nrad (#5, 3013) — IN RUNGS (flow198) — open-loop, 800-unit wheat buyer
h0 BUY 2 wheat + 3 COW + 2 SHEEP + 4 HIRE + 5 MELON + 15 WHEAT seed (all in one h0 row; HIRE serialised with
arguments); hands 4/1/8-13 (13) — crew drops to 1 on d5; 5 melon d0 (15 total, d8-d12), 30 dumped d10 @239-249;
land d6 + d9; 4-9 cows + 13-17 sheep + 3 geese; wb 823-850 (!) — daily 20-40 unit wheat buys as feed; 108-121 wheat /
33-61 carrot / 23-41 tomato / 11-17 straw; fertilizer 318-342; 103-110 sell turns, 38-39 % h0. 97 % identical.
Ids: 107779563 (1), 107785475 (1).

### T5 — binghua (#6, 2975) — IN RUNGS (flow198) — open-loop early-land labour build
h0 7 HIRE + 5 COW + 1 SHEEP + 1 MELON seed; h1 18 WHEAT seed; hands 7/7/12 (12); land d3 + d8 (earliest of all 50);
1 melon d0, 11-13 total planted d6-d12, 12-24 dumped d16-17 @178-187 (no d10 pot); 5-7 cows 3-4 sheep 2-5 geese;
wb 99-116; 123-129 wheat / 37-46 straw / 39-68 carrot; fertilizer 214-271; 177-185 sell turns, 52-54 % h0.
100 % identical. Ids: 107774526 (1), 107782380 (1).

### T6 — QQ Farming (#13, 2923) — NEW — slow-hire tomato build
h0 BUY 6 wheat + 3 COW + 3 SHEEP + 3 WHEAT seed + 2 HIRE (nothing at h1); hands 2/3/9 (14): 2 hands d0-d4, 3 d5,
4 d6, 6-7 d7-d9, 9 d10, 14 by the end; land d7 + d9; melon 0 d0 — 17 tiles planted d2-d9 (2-6 a day), dumped d19 36 @96
(no pot race); 9 cows 4 sheep 5 geese; 90 wheat / 34 tomato (d3-d17, PIZZA d2) / 29 carrot / 16 straw; wb 192;
fertilizer 210; 101 sell turns, 13 % h0. Cash d10 2.3k (lowest), d20 40k, final 68.7k (+9.5k win). Tomato revenue 15.2k.
Id: 107783403 (0) [CUT].

### T7 — Xiangyu Liu (#16, 2909) — NEW — 8-hand d0 wool/carrot build
h0 13 WHEAT seed + 2 wheat + 1 COW + 1 SHEEP + 6 HIRE; h1 1 WHEAT seed + 2 HIRE -> 8 hands from d0 (8/8/10, max 12),
hires also mid-day (d2 h14, h20); land d6 + d9; melon 0 d0 — 11 tiles d4-d19 (6 on d10), 36 dumped d20 @184;
4 cows + 10 sheep (wool 65.6k with YARN d2); 157 wheat / 107 carrot / 18 straw; wb 311; fertilizer 295; 196 sell
turns, 38 % h0; 0 tomato. Cash d10 5.8k, d20 62k, final 110k. Id: 107776180 (1) [CUT].

### T8 — keiz (#26, 2891) — NEW — own implementation of the clone plan, 12 cows, tomato d12-18
h0 BUY 20 wheat; h1 SELL 15 + 2 COW + 2 SHEEP + 5 HIRE + 7 WHEAT seed + 12 MELON seed (12 melon d0); hands 5/5/11 (12);
land d6 + d10; 12 cows + 4 sheep + 3 geese; wb 534 (feed); 162 wheat / 27 straw / 15 tomato (d11-d18) / 12 melon /
9 carrot; 60 dumped d10 @214; fertilizer 269; 289 sell turns (most of any file), 17 % h0; milk 49.4k, wheat 30.8k.
0 % stream identity with every other file. Id: 107784521 (1) [CUT].

## Coverage summary

| template | files | in rungs? | source of rung |
|---|---|---|---|
| T0a public clone | 24 | yes | flow197/199 band boards (2300-2700 opponents), flow198 carlos-tagosaku + mtmr_s1 |
| T0b clone + quad-4 d18 + tomato d18 | 6 | NO | cut here: 107785390, 107780056 |
| T0c clone, 6 cows + 11 sheep wool | 6 | NO | cut here: 107782373 |
| T0d feel-the-agi derivative | 6 | 3 of 6 (feel the agi, 3정훈, Mengfei Li in flow198) | cut here: 107784403 High Frequency, 107786235 Tarang222 |
| T1 Majkel1337 | 1 | yes (flow198) | — |
| T2 SpaTaro | 1 | yes (flow198) | — |
| T3 Otter Vibe | 1 | yes (flow198) | — |
| T4 c0nrad | 1 | yes (flow198) | — |
| T5 binghua | 1 | yes (flow198) | — |
| T6 QQ Farming | 1 | NO | cut here: 107783403 |
| T7 Xiangyu Liu | 1 | NO | cut here: 107776180 |
| T8 keiz | 1 | NO | cut here: 107784521 |
| (T0a pump variant Gleb Tumanov) | — | ledger in rungs, pump not | cut here: 107784448 |

Shop reaction: none of the 50 files plants tomato inside 4 days of a PIZZA/BRUNCH/ICE unlock except Otter Vibe once
(16 tiles) and QQ Farming (2); carrot inside 4 days of PET/FARMERS: insuperabilehart 28, SpaTaro 9, binghua 5,
한밭대학교 4. The field is open-loop on the shop draw; the top two (Majkel1337, SpaTaro) are the only adaptive
streams, and their adaptation is to the opponent/market (melon dump day, hire rows), not to shops.

## Caveats
One replay per file for ranks 8-50 (pattern = that game; T0a membership is confirmed by the 76-100 % stream identity,
the singles T6-T8 by ledger only). Rung weights below are suggestions, not measured. The 400 MB download guidance was
exceeded (1.8 GB) because a replay is 32 MB, not 1-3 MB.

## Tapes cut (10:21Z) and files
9 episodes cut at the top file's seat with S/top50/cut_one.sh (copy of S/flow198/cut_one.sh, S/top50 paths only), 18/18
drawn + pinned-town cuts verified byte-exact (S/top50/cut2/<id>.out): 107783403 T6, 107776180 T7, 107784521 T8,
107785390 + 107780056 T0b, 107782373 T0c, 107784403 + 107786235 T0d, 107784448 T0a-pump. Seats, templates and suggested
rung weights: S/top50/train_ids_patterns.txt. Towns appended by S/top50/town_append.sh (= S/livec/cut_append2.sh append
body): S/band2100p/town_schedules.json 454 -> 463 (backup .bak_20260911T102334Z); artifacts/town_schedules.json (the file
the launchers pass as --real-gate-pinned) is still 454 rows — superset sync owed before these ids enter a launcher.
Provenance: S/livec/provenance.txt TOWN APPEND #7. Scripts: S/top50/{pick.py,pick2.py,dl.py,dl1.py,ledall.sh,features.py}.
