Stream: LIVEHEALTH2 (local, 1 worker; remote replay caches read-only)
Date: 2026-09-30 11:18-~11:55Z. Tools and outputs in S/livehealth2 (agg.txt, lbsum.txt, loss20.txt.out, loss20.tsv, id.jsonl, cls.tsv, eps.tsv). Replays and unpacked packages are local only, not committed.
Verdict: both live subs HEALTHY (297/297 games are 720 steps DONE/DONE with 0 errors; identity is 23/24 exact, 1 divergence at d21 from wall-clock-bounded routing; the fastpath is byte-identical 6/6). 56687235 (vrp23_pfs_t) is 82-76, rank 269 at 2,318.1. 56687774 (vrp24_pfs_tfp) is 125-14 at 2,039.2, below the team entry. The 20 newest losses of 56687235 are 12 P48, 5 V, 2 PQ4 and 1 other. None is decided in the d10-14 wave; every one is decided d15-29.

# LIVEHEALTH2: pre-selection audit of the live pair 56687235 + 56687774

## Data
- **Listings.** ListEpisodes (11:18Z) gives 56687235 158 completed public games and 56687774 139, plus 1 validation game each (excluded).
- **Leaderboard.** GetLeaderboard (11:18Z) gives 10,202 teams.
- **Replays.** 292 replays came from the remote caches (livehealth1r, refresh5/6/7, pq4tape1r, p48loss1r). 5 were fetched new through the episode API.
- **Health signals.** The 224 LIVEHEALTH1R games reuse its sig.jsonl. The 73 new games were parsed here.
- **Family tag.** The tag is agg.py from LIVEHEALTH1R (rival h0/h1 market plus d1 melon), unchanged:
  - V: 11-13 melon d1 + COW2/SHEEP2 + 4 or more hires.
  - PQ4: COW1 + WHEAT5 at h0, with rival cash 2408-2467.
  - P48: rival cash 961-967 or 2438, or 5-7 melon d1.
  - other: everything else. No DSM seat was drawn.
- **Band.** The rival's rating before the game (initialScore).

## 1. Health
| sub | games | 720 steps | DONE/DONE | ERROR/TIMEOUT/INVALID | min overage left | h0 PFS identity | h1 PFS identity |
|---|---|---|---|---|---|---|---|
| 56687235 | 158 | 158 | 158 | 0 | 59.79 / 60 s | 158 | 158 |
| 56687774 | 139 | 139 | 139 | 0 | 59.87 / 60 s | 139 | 139 |

**Identity reruns** (rerun.py)
- **Method.** The real shipped package (dist tarball unpacked, main.py agent) plays our seat in the real kaggle env (1.32.7, the replay's seed) against the rival's recorded actions. Every action is compared to the recorded one, along with the final rewards. Sample: the 12 newest games of each sub, run with the sub's own package. The 3 newest of each are also run with the other package, which is the fastpath byte-identity test: vrp24 = vrp23 + PLAN_FASTPATH_ON.
- **Byte-identity results:**
  - 56687774 with vrp24_pfs_tfp (ea48ab0e, FASTPATH ON, TDV ON): 12/12 exact.
  - 56687235 with vrp23_pfs_t (ff0cd4e1, TDV ON): 11/12 exact.
  - Cross runs: vrp24 on 3 games of 56687235 is 3/3 exact, and vrp23 on 3 games of 56687774 is 3/3 exact. The fastpath is byte-identical on all 6 cross runs, and the 2 packages also agree on the one non-exact game.
- **The one non-exact game, 115728888** (56687235, seat 1, vs "thanks" at 2,243):
  - The live game was a WIN, +15,897.
  - The first divergence is step 506 (d21 h1), in hand routing (fertilizer pickup order); 211 actions differ after it.
  - Local rerun money: ours 110,657 vs live 108,012; rival 92,635 vs 92,115.
  - The local rerun is deterministic (2/2 identical re-reruns), with both packages equal.
  - Live overage stayed at 60 s all game. The likely cause is the wall-clock-bounded route search in route_vrp.py (improve/ruin_recreate budgets, SAFETY_S 0.75 s) cutting differently on the Kaggle host. It is not the fastpath, and not an error.
- **TERMINAL_DEPOSIT_VALUE:** fired in 1/24 own-package reruns (115730483, 56687774, term 1, term_changed 1, exact to the live tape, a win: 128,902 vs 123,341). LIVEHEALTH1R counted 0/224.

## 2. Records
Ratings are the latest updatedScore from ListEpisodes. The LB lists only the team's best entry.
- **56687235:** 2,318.1 = team rank 269 of 10,202. It was 2,391.5 at 00:00Z and 2,334.9 at 06:30Z.
- **56687774:** 2,039.2, which would sit at position 641 if it were listed. It was 1,624.0 at 00:00Z and 1,906.0 at 06:30Z.
- **Team counts by rating:** 208 teams are at 2,400 or above, 67 at 2,600 or above and 15 at 2,800 or above.
- **Top 10 by rating:**
  1. M & M & P & Q 3,101.9
  2. DECEM 2,979.4
  3. DSM 2,966.0
  4. Victor @ Tufa Labs 2,949.2
  5. CDE 2,895.4
  6. Unknown Mother-Goose 2,889.2
  7. Vadim Vasilenko 2,856.3
  8. Majkel1337 2,836.4
  9. Luca 2,830.5
  10. Anton Tikhonov 2,826.5

Records are W-L with the mean margin in coins:

| sub | window | all | V | P48 | PQ4 | other | band <2400 | band 2400-2600 | 2600+ |
|---|---|---|---|---|---|---|---|---|---|
| 56687235 | all (since 20:47Z 09-29) | 82-76 (-239) | 59-9 (+7,402) | 13-50 (-8,212) | 1-10 (-7,725) | 9-7 (+3,828) | 76-41 (+3,830) | 6-35 (-11,849) | 0 games |
| 56687235 | since 00:00Z | 38-55 (-4,115) | 25-8 (+4,871) | 7-38 (-10,906) | 1-5 (-8,416) | 5-4 (-240) | 35-35 (-520) | 3-20 (-15,055) | 0 |
| 56687235 | since 06:30Z | 14-17 (-2,361) | 11-5 (+4,500) | 2-11 (-10,672) | 0-1 (-13,208) | 1-0 (+6,757) | 13-15 (-1,674) | 1-2 (-8,774) | 0 |
| 56687774 | all (since 21:18Z 09-29) | 125-14 (+8,705) | 116-8 (+8,510) | 5-5 (+9,069) | 0-1 (-16,962) | 4-0 (+20,229) | 125-14 (+8,705) | 0 | 0 |
| 56687774 | since 00:00Z | 89-5 (+8,260) | 85-3 (+8,367) | 2-1 (+12,760) | 0-1 (-16,962) | 2-0 (+9,404) | 89-5 (+8,260) | 0 | 0 |
| 56687774 | since 06:30Z | 32-1 (+8,611) | 31-1 (+8,432) | 0 | 0 | 1-0 (+14,325) | 32-1 (+8,611) | 0 | 0 |

Finer rival-rating split (all games):

| sub | rival rating | W-L | P48+PQ4 seats | family mix |
|---|---|---|---|---|
| 56687235 | <1900 | 15-0 | 3 / 15 | V 11, P48 3, other 1 |
| 56687235 | 1900-2100 | 3-1 | 1 / 4 | V 3, P48 1 |
| 56687235 | 2100-2300 | 20-3 | 1 / 23 | V 21, PQ4 1, other 1 |
| 56687235 | 2300-2400 | 38-37 | 36 / 75 | P48 32, V 30, other 9, PQ4 4 |
| 56687235 | 2400-2600 | 6-35 | 33 / 41 | P48 27, PQ4 6, other 5, V 3 |
| 56687774 | <1900 | 90-12 | 10 / 102 | V 88, P48 10, other 4 |
| 56687774 | 1900-2100 | 35-2 | 1 / 37 | V 36, PQ4 1 |

## 3. Loss ledger: the 20 newest losses of 56687235 (05:50-11:10Z)
- **Books.** Exact engine rerun (P48LOSS1R ledger.py, kaggle_environments 1.32.7). All 20 reproduce the recorded rewards (div None, rewards equal).
- **Phases.** Phase margins are ours minus theirs, revenue minus spend: early d0-9, wave d10-14, late d15-29. They add up to the final margin.
- **Deficits.** dWave and dLate are the phase margin minus the win-class reference: our wins in S/p48loss1r/games.json of the same family (V n 172, P48 n 29, OTH n 36). PQ4 uses the PQ4TAPE1R W phase means with the P48 W prices.
- **Late price loss.** Our d15-29 units x (our price - win-class price), over all products and over strawberry+wool+milk+egg.
- **Units.** straw d15-17 = strawberry units sold d15-17, ours/theirs. anim d18-29 = milk+wool+egg units sold d18-29, ours/theirs.
- **Block rule.**
  - The block is the phase with the largest deficit.
  - A late block with price loss at least 50 % of the late deficit is labelled "late price glut".
  - Any other late block is labelled "late volume/other": the rival's late revenue or our late units.

| ep | UTC | rival | R | fam | margin | early | wave | late | dWave | dLate | late price loss all / S+W+M+E | our / their late rev | straw d15-17 o/t | anim d18-29 o/t | block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 115743488 | 11:10 | high frequency far | 2354 | PQ4 | -13,208 | 6,497 | -21,877 | 2,172 | 642 | -21,606 | -40,189 / -25,787 | 81.8k / 83.8k | 46/34 | 287/223 | late price glut |
| 115742802 | 11:05 | Ghost Rule | 2355 | P48 | -14,684 | 5,300 | -25,561 | 5,577 | -5,338 | -28,039 | -26,576 / -21,796 | 80.9k / 76.0k | 40/34 | 276/357 | late price glut |
| 115725607 | 10:22 | yfy | 2384 | V | -6,509 | 2,474 | -20,629 | 11,646 | -1,119 | -15,047 | -18,141 / -8,866 | 86.0k / 74.5k | 38/24 | 249/276 | late price glut |
| 115715890 | 09:58 | kuro0315 | 2343 | P48 | -20,679 | 4,007 | -27,959 | 3,273 | -7,736 | -30,343 | -25,009 / -13,282 | 89.9k / 88.7k | 52/46 | 217/244 | late price glut |
| 115715101 | 09:53 | LS | 2278 | V | -2,126 | 3,538 | -21,828 | 16,164 | -2,318 | -10,529 | -1,300 / -3,411 | 98.9k / 83.2k | 60/40 | 273/272 | late volume/other |
| 115709174 | 09:37 | ZKH-Harness | 2369 | P48 | -20,969 | 5,532 | -11,066 | -15,435 | 9,157 | -49,051 | 13,009 / 20,265 | 148.1k / 170.3k | 50/52 | 363/437 | late volume/other |
| 115701375 | 09:17 | chungkuangwen | 2323 | P48 | -9,074 | 6,466 | -22,502 | 6,962 | -2,279 | -26,654 | 442 / 466 | 120.8k / 117.0k | 64/50 | 246/362 | late volume/other |
| 115695337 | 09:02 | Alperen Aydın | 2311 | P48 | -11,931 | 5,575 | -30,710 | 13,204 | -10,487 | -20,412 | 5,916 / 8,486 | 131.8k / 115.7k | 58/50 | 316/328 | late volume/other |
| 115689352 | 08:46 | Kazuo Watanabe | 2310 | P48 | -2,989 | 5,240 | -25,242 | 17,013 | -5,019 | -16,603 | -34,509 / -20,733 | 87.7k / 71.3k | 38/32 | 281/290 | late price glut |
| 115684026 | 08:33 | pensukesan | 2364 | P48 | -15,053 | 3,767 | -25,110 | 6,290 | -4,887 | -27,326 | -32,563 / -25,766 | 86.4k / 82.1k | 56/52 | 225/386 | late price glut |
| 115681670 | 08:25 | Shawn404 | 2336 | V | -3,323 | 3,325 | -22,445 | 15,797 | -2,935 | -10,896 | 52,196 / 52,753 | 155.8k / 138.9k | 50/40 | 305/305 | late volume/other |
| 115676460 | 08:14 | Eesh saxena | 2281 | V | -462 | 2,543 | -16,130 | 13,125 | 3,380 | -13,568 | -28,862 / -21,312 | 62.6k / 146.5k | 38/40 | 244/271 | late price glut |
| 115675530 | 08:10 | Krzysztof Gonia | 2327 | P48 | -6,258 | 3,017 | -20,544 | 11,269 | -321 | -22,347 | -19,513 / -14,077 | 99.0k / 86.9k | 48/42 | 251/280 | late price glut |
| 115667629 | 07:50 | PrasadChopade213 | 2467 | P48 | -15,979 | 3,541 | -22,900 | 3,380 | -2,677 | -30,236 | -27,169 / -20,033 | 83.5k / 79.3k | 57/46 | 241/442 | late price glut |
| 115655255 | 07:18 | Ilya & Yurnero | 2315 | V | -502 | 2,571 | -21,478 | 18,405 | -1,968 | -8,288 | -6,860 / -12,105 | 91.7k / 178.1k | 62/40 | 171/240 | late price glut |
| 115647485 | 06:57 | liyupengli | 2427 | P48 | -21,320 | 2,975 | -16,879 | -7,416 | 3,344 | -41,032 | -7,527 / -5,480 | 103.1k / 121.5k | 64/58 | 217/315 | late volume/other |
| 115638148 | 06:34 | zzzz | 2381 | P48 | -6,308 | 3,076 | -10,923 | 1,539 | 9,300 | -32,077 | -15,982 / 642 | 106.7k / 110.9k | 38/40 | 288/273 | late volume/other |
| 115631790 | 06:17 | Sida Zuo | 2433 | other | -10,977 | 5,538 | -19,139 | 2,624 | -10,221 | -36,672 | -14,009 / -15,951 | 96.5k / 94.2k | 52/41 | 275/289 | late volume/other |
| 115621299 | 05:54 | Driz Lo | 2356 | P48 | -16,303 | 4,036 | -21,251 | 912 | -1,028 | -32,704 | 11,302 / 7,847 | 120.8k / 121.0k | 62/58 | 237/321 | late volume/other |
| 115620888 | 05:50 | misis biznessmenlb | 2393 | PQ4 | -6,037 | 4,829 | -20,392 | 9,526 | 2,127 | -14,252 | -12,774 / -9,656 | 98.9k / 91.0k | 54/37 | 313/270 | late price glut |
rerun exact 20 / 20

**Summary**

| family | n | mean margin | wave | late | late price loss (all / S+W+M+E) | our / their late revenue | blocks |
|---|---|---|---|---|---|---|---|
| P48 | 12 | -13,462 | -21,721 | +3,881 | -13,182 / -6,955 | 104.9k / 103.4k | glut 6, volume/other 6 |
| V | 5 | -2,584 | -20,502 | +15,027 | -593 / +1,412 | 99.0k / 124.2k | glut 3, volume/other 2 |
| PQ4 | 2 | -9,622 | -21,134 | +5,849 | -26,482 / -17,722 | 90.4k / 87.4k | glut 2 |
| other | 1 | -10,977 | -19,139 | +2,624 | -14,009 / -15,951 | 96.5k / 94.2k | volume/other 1 |

- **All 20 losses:**
  - Mean margin -10,235.
  - Phase margins: early +4,192, wave -21,228, late +6,801.
  - Deficit vs the win class: dWave -1,519, dLate -24,384.
  - Late price loss: -11,406 over all products, -6,390 over strawberry+wool+milk+egg.
- **Decisive block:** the d10-14 wave decides 0/20. Late price glut decides 11/20 and late volume/other 9/20.
- **Units:**
  - Strawberry d15-17: ours 51.4, theirs 42.8.
  - Animal units d18-29: ours 263.8, theirs 309.1.
- **Families:** P48 12, V 5, PQ4 2, other 1.
- **Bands:** <2400 17, 2400-2600 3.
- **The five V losses** are lost on the rival's late revenue (124.2k vs our 99.0k), not on our price.
- **The P48 and PQ4 losses** are lost on our late prices (S+W+M+E -7.0k and -17.7k per game).

## 4. Exposure of the final pair (last 24 h = every game of both subs)
- **Both subs:** 297 games. P48+PQ4 (programme) seats are 85/297 = 28.6 % (P48 73, PQ4 12). V is 192 (64.6 %), other 20 and DSM 0. Rivals rated 2,400-2,600 are 41/297 = 13.8 %, and 0/297 are above 2,600.
- **56687235:** at 2,318-2,392 it drew rivals with median 2,349.5 (max 2,485).
  - Its programme share is 74/158 = 46.8 %: 54.8 % of the 93 games since 00:00Z and 45.2 % of the 31 since 06:30Z.
  - 41/158 = 25.9 % of its rivals were 2,400-2,600, and 80 % of those seats (33/41) were programme.
  - Rivals at 2,300-2,400 were 36/75 programme.
- **56687774:** at 1,624-2,039 it drew rivals with median 1,782 (max 2,052).
  - Its programme share is 11/139 = 7.9 %: 0/33 since 06:30Z.
  - 0 of its rivals were at 2,400 or above.
- **Where the programme sits:** below 2,300 our subs met 16 programme seats in 181 games; at 2,300-2,600 they met 69 in 116.
- **Who has played the high seats:** only 56687235 has played rivals at 2,300 or above. 56687774's 125-14 contains no such seat.
