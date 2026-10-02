# BRAINSTORM6 (2026-09-29, fresh session) — session doc
Starts from the BRAINSTORM5 session summary: `docs/strategy/2026-09-29-brainstorm5.md` §Round 3 (invariants A1-10, closed lines B, coverage gap C, fresh-session order D, one gate E) and astra's review `docs/strategy/2026-09-29-astra-brainstorm10.md`.
Standing order (BRAINSTORM5 D): PROGFIRE1 (h1 bridge) and SPLITHEAD1 (fired-seat-only head ES) first. **R = OTHERMELON**, data only, reporting before any whitelist change. Then TILELEASE1 + PRICEDASK1 -> C1, the DSM tail, and TURN_COST last.
Rules carried over: paired numbers only where both seats are in one game (unpaired figures marked); no rank projections; no whitelist change without a judged package.
Round 1 = OTHERMELON1 (this section). Stream dir `S/othermelon1`. No code changes, no list changes.

## Round 1 (OTHERMELON1, 20:23Z-21:05Z)

**Verdict (12 lines). No list change, no package.**
1. Other MELON is ONE class: the P48 melon programme under ~50 h0 codes. In band, 77/92 seats run the strict P48 timetable vs 49/50 coded seats. PFS goes 12-66 (-7,781) vs P48-code's 11-26 (-7,441), unpaired.
2. Fired (41 list, 20 in-band seats) and unfired (58) are the same class:
   - Q3 d9 vs d8; 54.6 vs 51.2 melons sold d10-14; herd d9 15.4 vs 16.0; cash gap +4.4k / +3.9k at eod d9 -> -18.9k / -18.3k at eod d14.
   - The list merely picks the stronger rivals: R0 2557 vs 2480; our record 2-18 (-11.9k) vs 10-48 (-6.4k).
3. The 6-22 losses: 14 other MELON (12 off the list: 7 x2, 2885 x2, 3, 33, 3000, 1026, 2854, 526, 2867, 27), 7 listed P48-code, 1 own body. In band, other MELON is 66 of our 145 PFS losses.
4. DECEM and Majkel: 0 live games vs a PFS-h0 sub. Engine-predicted values are 1938 and 1992; neither is on the list. Majkel's older h0 predicts 1761, which is mhiro2's value (3-0 ours).
5. Inside the class, W/L follows the rival's late herd (sheep d9 3.9 vs 5.8, wool 90 vs 130 u), not a PFS action.
6. Judge before any package: fired18 (12/18 of its seats are on-list other MELON) plus om16 (16 tapes, 16/16 exact replays, PFS W 3/16).
   - Bar: om16 on-list margin >= 0 and W >= 1/8, off-list exact identity; 34 pooled seats resolve ~1.4-2.5k.
7. Round-2 build a fresh round could defend: a d2-h0 class latch (rival 1-10 melon tiles, not V) for packages that start at d2 or later (C1). Other-MELON coverage 20/78 -> 78/78. Expected coins: 0 until a package passes.

### Findings (the numbers behind the verdict)
1. **One class.**
   - In band, 77/92 other-MELON seats run the strict P48 timetable (Q2 d5-7, Q3 d8-9, >= 40 melons sold d10-14), against 49/50 coded P48/PQ4 seats. 91/92 pass with Q3 <= d11 and >= 30 melons; the one exception is fuxi (1026), a 1-melon wheat body.
   - PFS's record is the same as vs P48-code: 12-66 at -7,781 vs 11-26 at -7,441 (unpaired).
   - The h1 cash is an h0 fingerprint, not a class: 50 values, 28 of them singletons.
2. **Fired vs unfired: same timetable, same melon wave, same d9 -> d14 cash swing.**
   - Timetable: Q2 d6, Q3 d9 vs d8. Melons sold d10-14: 54.6 vs 51.2 @248-249. Herd d9 15.4 vs 16.0. Cash gap +4.4k / +3.9k at eod d9 -> -18.9k / -18.3k at eod d14.
   - The list's 20 in-band PFS seats are the stronger rivals (R0 2557 vs 2480) and our worse record (2-18 at -11.9k vs 10-48 at -6.4k, unpaired). That is selection, not a different opponent.
3. **The 6-22 (MELONLOSS1 NEW window).** Its 22 losses are:
   - other MELON 14: 12 off the list (7 x2, 2885 x2, 3, 33, 3000, 1026, 2854, 526, 2867, 27), 2 on it (26, 2600);
   - P48-code 7, all listed (938 x5, 1020, 964);
   - one own body (393).
   - In band, other MELON is our largest loss pool: 66 of 145 PFS losses, against V 33.
4. **DECEM and Majkel have never met a PFS-h0 sub** (0/493 games; 0 of 3,646 top-10 games vs us). Engine-predicted values vs PFS's h0: DECEM **1938**; Majkel **1992** (newest), 1860 and **1761**. 1761 is mhiro2's live value, and we are 3-0 (+24.3k) vs mhiro2. None is on the list.
5. **Within the class, wins and losses are decided on d15-29, and mostly on the rival's side.**
   - The d14 cash gap is -16.9k in our 12 wins and -18.7k in our 66 losses.
   - In wins the rival has fewer sheep at d9 (3.9 vs 5.8). It sells less wool (90 vs 130 u), milk and late melons: rival M+W+E revenue -8.2k.
   - Our own animal units are flat (383 vs 357), but priced +4.3k higher; our d15-29 revenue is 106.4k vs 97.1k.
   - The split is a rival draw, not a PFS action.
6. **Judge before any package.** A fired package must pass:
   - fired18 (12 of its 18 seats are on-list other MELON);
   - om16's 8 on-list seats: margin >= 0 and W not below the PFS baseline;
   - om16's 8 off-list seats: exact unfired identity.
   - With paired SD 4.0-7.4k per seat, the 34 pooled seats resolve about 1.4-2.5k.
7. **Round-2 build to defend: a d2-h0 class latch** (rival melon tiles 1-10, not the V pattern; in band V shows 11-12 melons, MELON <= 10). It is for packages whose first deviation is at d2 or later, such as C1 volume from d10.
   - Coverage: other MELON 20/78 -> 78/78 in band; P48/PQ4 unchanged at 100 %.
   - V identity: the latch reads the rule that defines V here. In band the d2 melon counts do not overlap (V 11-12, MELON <= 10); the V56 judge boards must confirm exact identity.
   - Expected coins: **0 until a package passes the gate.**
   - No unpaired ceiling transfers: the within-class d15-29 gap (+9.3k) is the rival's own smaller herd.

### A. Data and method
- **Games.** 493 live games, 09-28 08:14Z .. 09-29 20:27Z, every one with PFS's real h0 (lw23 `h0pfs` 493/493).
  - Subs: vrp15_k2fire 56634350 92, vrp19w 56649892 129, vrp20 56652418 186, vrp21 56676381 70, 56686302 8, 56686308 8.
  - `S/othermelon1/lst.py` imports lw23's list_eps/one/fam and re-points its output directory to S/othermelon1. It fetched 40 new replays at 3 s pacing (0 retries, 0 HTTP 429).
- **Family.** The TOP1WATCH1 q4wl rule: h1 cash code first, then lw23's d2 crop rule.
  - "In band" = rival R0 >= 2,000.
  - "PFS played" = lw23 `pfsid` (unfired PFS identity), with vrp21 excluded (PFS + REINVEST_DAILY + FEED_ALL).
  - The 20 low-rated other-MELON games (R0 median 759, all on vrp21/vrp22 early games) are 19-1 and kept out of every class table.
- **Exact ledgers.** `led.py` (a copy of S/dsmloss1/led.py; S/econcensus measure() unchanged) ran on 142 games, both seats: all 92 in-band other-MELON games and 50 in-band PFS-played P48/PQ4 reference games. **0 cash and 0 stock mismatches.**
- **h1 prediction.** `h1sim.py` is a one-step engine run of PFS's h0 against a given rival h0. It reproduces all 6 live-observed codes (938, 964, 1100, 2438, 2464, 700) on 3 seeds x 2 seats. It is used only for DECEM and Majkel, and marked as a prediction.

### B. Composition
Family mix (live finals; in-band margins unpaired):

| family | all 493: n (W-L) | in band, PFS played: n | W-L | margin mean (se) | share of in-band PFS losses |
|---|---|---|---|---|---|
| V | 272 (212-60) | 162 | 129-33 | +4,526 (537) | 33/145 |
| other MELON | 112 (33-79) | 78 | 12-66 | -7,781 (1,448) | 66/145 |
| P48 | 47 (14-33) | 37 | 11-26 | -7,441 (2,944) | 26/145 |
| PQ4 | 31 (7-24) | 13 | 3-10 | -6,578 (1,902) | 10/145 |
| other | 29 (21-8) | 26 | 18-8 | +3,401 (2,207) | 8/145 |
| own bodies | 2 (0-2) | 2 | 0-2 | -19,945 (1,299) | 2/145 |

Other MELON by h1 value (values with >= 2 in-band seats, plus every on-list value; `res/composition.tsv` has all 50):

| h1 | list | n all 493 | families at this value | n other MELON | n in-band PFS | W-L (in-band PFS) | margin mean | teams | rival d2 | rival Q3 day / melon u d10-14 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ON | 8 | other MELON 8 | 8 | 5 | 0-5 | -10,010 | 2: istinetz x7; Capitaalgain x1 | 8m/10w x7; 5m/13w x1 | d9 / 64 |
| 26 | ON | 7 | other MELON 7 | 7 | 2 | 0-2 | -18,872 | 4: huaiyuyoung x3; mhw x2; kuengo x1 | 9m/6w x7 | d11 / 52 |
| 2338 | ON | 4 | other MELON 4 | 4 | 3 | 1-2 | -5,956 | 4: Alejandro Ayestaran x1; Azamaro x1; Yannik Schiffner x1 | 7m/13w x4 | d8 / 60 |
| 2600 | ON | 2 | other MELON 2 | 2 | 1 | 0-1 | -583 | 2: Azathoth x1; lzeee x1 | 8m/12w x2 | d8 / 48 |
| 638 | ON | 2 | other MELON 2 | 2 | 0 | 0-0 | +0 | 1: Koba x2 | 7m/7w x1; 9m/9w x1 | - / - |
| 564 | ON | 2 | other MELON 2 | 2 | 2 | 0-2 | -18,620 | 1: AI是我的豆包 x2 | 10m/8w x2 | d9 / 42 |
| 661 | ON | 2 | other MELON 2 | 2 | 1 | 1-0 | +3,844 | 1: chungkuangwen x2 | 8m/12w x2 | d9 / 48 |
| 73 | ON | 1 | other MELON 1 | 1 | 1 | 0-1 | -13,507 | 1: ShunkiKyoya x1 | 8m/12w x1 | d8 / 48 |
| 2511 | ON | 1 | other MELON 1 | 1 | 1 | 0-1 | -12,112 | 1: ymg_aq x1 | 10m/9w x1 | d9 / 65 |
| 2097 | ON | 1 | other MELON 1 | 1 | 1 | 0-1 | -35,398 | 1: My second life x1 | 10m/10w x1 | d9 / 60 |
| 19 | ON | 1 | other MELON 1 | 1 | 1 | 0-1 | -139 | 1: Sida Zuo x1 | 9m/8w x1 | d8 / 52 |
| 117 | ON | 1 | other MELON 1 | 1 | 0 | 0-0 | +0 | 1: THUNDER THUNDER x1 | 9m/10w x1 | - / - |
| 2046 | ON | 1 | other MELON 1 | 1 | 1 | 0-1 | -19,232 | 1: Dipam Chakraborty x1 | 8m/10w x1 | d8 / 54 |
| 190 | ON | 1 | other MELON 1 | 1 | 1 | 0-1 | -17,435 | 1: c0nrad x1 | 5m/15w x1 | d9 / 32 |
| 2854 | off | 54 | V 44; other MELON 10 | 10 | 10 | 0-10 | -10,242 | 6: Satoshi_SsSs x2; yjshyfy x2; leave you x2 | 6m/14w x7; 8m/12w x3 | d8 / 56 |
| 20 | off | 7 | other MELON 7 | 7 | 7 | 3-4 | -760 | 2: goose10 x6; lingxiaojun x1 | 8m/12w x6; 6m/12w x1 | d8 / 46 |
| 3 | off | 6 | other MELON 6 | 6 | 2 | 0-2 | -39,864 | 5: shane18 x2; stpete_ishii x1; Sandeep063 x1 | 5m/5w x4; 8m/12w x2 | d11 / 49 |
| 2885 | off | 7 | other MELON 6; V 1 | 6 | 6 | 1-5 | -12,274 | 5: DASH村 x2; Kucing Garong x1; Joseph Ayanda x1 | 8m/12w x6 | d8 / 48 |
| 7 | off | 4 | other MELON 4 | 4 | 4 | 0-4 | -10,855 | 1: TX x4 | 10m/7w x4 | d8 / 58 |
| 2867 | off | 71 | V 68; other MELON 3 | 3 | 3 | 0-3 | -2,425 | 2: Justin Yang x2; trantrikien239 x1 | 10m/9w x1; 8m/12w x1 | d8 / 54 |
| 700 | off | 3 | other MELON 3 | 3 | 3 | 0-3 | -2,688 | 2: 123456789101112151617181920212 x2; xiy lin x1 | 8m/12w x3 | d8 / 48 |
| 1761 | off | 3 | other MELON 3 | 3 | 3 | 3-0 | +24,255 | 1: mhiro2 x3 | 10m/7w x3 | d9 / 64 |
| 1026 | off | 2 | other MELON 2 | 2 | 2 | 0-2 | -4,998 | 1: fuxi x2 | 1m/15w x2 | d8 / 12 |
| 27 | off | 2 | other MELON 2 | 2 | 2 | 0-2 | -9,832 | 1: Alexander Gremyakov x2 | 10m/10w x2 | d10 / 60 |
| 33 | off | 2 | other MELON 2 | 2 | 2 | 0-2 | -12,291 | 2: Andrey Tikhomirov x1; Luca x1 | 10m/10w x1; 8m/7w x1 | d8 / 60 |
| 3037 | off | 6 | V 4; other MELON 2 | 2 | 2 | 1-1 | +9,417 | 1: offhand x2 | 7m/13w x2 | d8 / 48 |
| 113 | off | 2 | other MELON 2 | 2 | 2 | 0-2 | -5,502 | 1: Tergel Munkhbat x2 | 8m/11w x2 | d9 / 48 |

- **Singletons off the list, in band:** 526 L, 1808 L, 427 L, 2864 W, 2869 W, 3000 L, 1464 L, 85 L, 731 L, 2015 L.
- **On-list values with no other-MELON seat:** 938 (P48 33), 964 (6), 992 (3), 1020 (3), 985 (1), 1100 (1), 2438 (PQ4 24), 2492 (2).
- **Unseen in 493 games:** 19 of the 41 values.
- **Coverage.** The 41 list fires on 34/112 other-MELON games (all subs), 20/78 in band PFS-played, and 18/79 on the current three subs (vrp19w/vrp20/vrp21).
- **DECEM** (TOP1WATCH1 body: h0 AN COW 1, AN SHEEP 1, BP WHEAT 5; Q4 d10 on 33/33 seats):
  - Predicted value vs PFS h0 **1938**. The replays vs other opponents read 1961-1967, +23..+29, the same offset as MMPQ's 2461-2467 vs the live 2438.
  - n live = 0. Our record: none. Not on the list.
- **Majkel** (h0 HIREx5, AN COW 1, AN SHEEP 1, BP WHEAT 3/7/10 by sub):
  - Predicted values: 56663513 **1992** (reads 2005/2007 vs others); 56629366 1860; 56629362 **1761**.
  - 1761 = mhiro2 (R0 2,492), 3 live games vs PFS, all won by us, +24,255 mean. A cash extension for Majkel's older sub would fire on it.
  - n live = 0. Not on the list.

### C. Fired (on the 41 list) vs unfired, PFS played, in band (unpaired; `res/fired_vs_unfired.md`)

| metric | FIRED (on 41) (n 20) | UNFIRED (off 41) (n 58) | fired LIVE (our seat V56; rival class only) (n 14) |
|---|---|---|---|
| W-L, margin mean (se), median | 2-18, -11,873 (se 2,224), med -13,931 | 10-48, -6,370 (se 1,761), med -6,092 | 2-12, -9,002 (se 2,155), med -9,020 |
| rival R0 median | 2557 | 2480 | 2541 |
| cash gap eod d9 / d14 (ours - rival, mean) | +4,411 / -18,892 | +3,867 / -18,322 | +1,765 / +984 |
| rival Q2 bought, median day | 20/20 d6 | 58/58 d6 | 14/14 d6 |
| rival Q3 | 20/20 d9 | 58/58 d8 | 14/14 d9 |
| rival Q4 | 1/20 d10 | 6/58 d10 | 0/14 |
| our Q2 / Q3 / Q4 | 20/20 d5 / 20/20 d10 / 0/20 | 58/58 d5 / 58/58 d10 / 0/58 | 14/14 d6 / 14/14 d11 / 3/14 d12 |
| rival melon planted d0-9 (mean) | 12.3 | 11.7 | 10.1 |
| rival melon u sold d10-14 (mean) @ price | 54.6 @ 248 | 51.2 @ 249 | 57.8 @ 198 |
| our melon u sold d10-14 @ price | 0.3 @ 247 | 0.1 @ 246 | 72.0 @ 218 |
| rival strawberry planted d0-9 / ours | 23.5 / 24.8 | 19.5 / 21.9 | 23.7 / 20.0 |
| rival herd d9 c/s/g (mean) | 6.9/5.6/2.9 | 7.6/5.4/3.0 | 6.1/6.2/1.7 |
| herd d9 / d14 / d20 rival | ours | 15.4/19.9/19.9 | 11.2/18.8/18.6 | 16.0/20.1/20.3 | 11.4/18.4/18.3 | 14.1/19.6/19.4 | 13.0/18.3/17.8 |
| crew d9 / d14 rival | ours | 10.8/11.8 | 5.5/11.7 | 10.7/11.7 | 5.8/11.9 | 11.6/11.6 | 9.4/10.6 |
| rival late units d15-29 | ours | 2092 | 1270 | 1866 | 1267 | 1619 | 1274 |
| rival animal-product u d18-29 (E+M+W) | ours | 323 | 265 | 323 | 274 | 303 | 271 |
| strawberry u d15-17 rival | ours | 40.1 | 51.9 | 34.4 | 46.2 | 47.6 | 40.0 |
| wheat u d10-29 rival | ours | 1360 | 342 | 1140 | 349 | 882 | 451 |
| revenue d0-9 / d10-14 / d15-29 rival (k) | 22.6/47.0/118.3 | 14.5/37.8/111.4 | 16.1/34.7/109.9 |
| revenue d0-9 / d10-14 / d15-29 ours (k) | 14.0/10.5/94.1 | 14.2/11.1/100.1 | 14.0/30.8/88.8 |
| rival land / hire spend (k) | 3.2 / 5.6 | 3.4 / 5.9 | 3.0 / 6.3 |

Other MELON vs the coded families (same ledger, same filters):

| metric | other MELON all (n 78) | P48-code (n 37) | PQ4-code (n 13) |
|---|---|---|---|
| W-L, margin mean (se), median | 12-66, -7,781 (se 1,448), med -7,775 | 11-26, -7,441 (se 2,944), med -9,694 | 3-10, -6,578 (se 1,902), med -6,067 |
| rival R0 median | 2500 | 2483 | 2497 |
| cash gap eod d9 / d14 (ours - rival, mean) | +4,006 / -18,468 | +4,463 / -18,980 | +4,702 / -16,622 |
| rival Q2 bought, median day | 78/78 d6 | 37/37 d6 | 13/13 d6 |
| rival Q3 | 78/78 d8 | 37/37 d8 | 13/13 d9 |
| rival Q4 | 7/78 d10 | 7/37 d10 | 9/13 d10 |
| our Q2 / Q3 / Q4 | 78/78 d5 / 78/78 d10 / 0/78 | 37/37 d5 / 37/37 d10 / 0/37 | 13/13 d5 / 13/13 d10 / 0/13 |
| rival melon planted d0-9 (mean) | 11.9 | 11.9 | 10.4 |
| rival melon u sold d10-14 (mean) @ price | 52.1 @ 249 | 49.2 @ 250 | 60.9 @ 247 |
| our melon u sold d10-14 @ price | 0.2 @ 246 | 0.2 @ 247 | 0.0 @ 0 |
| rival strawberry planted d0-9 / ours | 20.5 / 22.6 | 21.6 / 24.7 | 21.3 / 25.5 |
| rival herd d9 c/s/g (mean) | 7.4/5.5/3.0 | 7.5/5.5/5.5 | 8.8/4.3/3.8 |
| herd d9 / d14 / d20 rival | ours | 15.8/20.1/20.2 | 11.4/18.5/18.4 | 18.5/20.3/20.2 | 11.0/17.4/17.0 | 16.9/20.8/20.0 | 10.5/17.9/17.8 |
| crew d9 / d14 rival | ours | 10.7/11.7 | 5.7/11.8 | 10.9/11.6 | 5.6/11.8 | 11.1/12.5 | 5.5/12.0 |
| rival late units d15-29 | ours | 1924 | 1268 | 1362 | 1239 | 2363 | 1268 |
| rival animal-product u d18-29 (E+M+W) | ours | 323 | 272 | 339 | 261 | 308 | 272 |
| strawberry u d15-17 rival | ours | 35.9 | 47.6 | 41.8 | 51.0 | 41.3 | 53.9 |
| wheat u d10-29 rival | ours | 1196 | 348 | 461 | 301 | 1687 | 327 |
| revenue d0-9 / d10-14 / d15-29 rival (k) | 16.5/40.2/113.2 | 15.0/31.1/92.4 | 15.0/45.7/120.2 |
| revenue d0-9 / d10-14 / d15-29 ours (k) | 14.2/10.9/98.6 | 13.9/10.1/100.2 | 13.9/10.8/92.6 |
| rival land / hire spend (k) | 3.4 / 5.8 | 3.8 / 6.0 | 5.8 / 6.6 |

Wins vs losses inside other MELON (unpaired):

| metric | WINS (n 12) | LOSSES (n 66) | LOSSES >= 10k (n 33) |
|---|---|---|---|
| W-L, margin mean (se), median | 12-0, +12,539 (se 2,768), med +10,566 | 0-66, -11,476 (se 1,155), med -10,060 | 0-33, -18,652 (se 1,374), med -16,597 |
| rival R0 median | 2468 | 2505 | 2540 |
| cash gap eod d9 / d14 (ours - rival, mean) | +4,588 / -16,937 | +3,900 / -18,746 | +4,082 / -19,713 |
| rival Q2 bought, median day | 12/12 d6 | 66/66 d6 | 33/33 d6 |
| rival Q3 | 12/12 d8 | 66/66 d8 | 33/33 d8 |
| rival Q4 | 2/12 d10 | 5/66 d10 | 2/33 d10 |
| our Q2 / Q3 / Q4 | 12/12 d5 / 12/12 d10 / 0/12 | 66/66 d5 / 66/66 d10 / 0/66 | 33/33 d5 / 33/33 d10 / 0/33 |
| rival melon planted d0-9 (mean) | 10.7 | 12.1 | 13.1 |
| rival melon u sold d10-14 (mean) @ price | 54.9 @ 248 | 51.5 @ 249 | 54.2 @ 248 |
| our melon u sold d10-14 @ price | 0.0 @ 0 | 0.2 @ 246 | 0.0 @ 0 |
| rival strawberry planted d0-9 / ours | 21.6 / 20.9 | 20.3 / 23.0 | 19.5 / 22.8 |
| rival herd d9 c/s/g (mean) | 7.4/3.9/3.2 | 7.4/5.8/3.0 | 7.2/7.0/2.1 |
| herd d9 / d14 / d20 rival | ours | 14.5/17.6/18.0 | 11.7/18.6/18.6 | 16.1/20.5/20.6 | 11.3/18.5/18.3 | 16.3/21.5/21.4 | 11.7/19.2/19.1 |
| crew d9 / d14 rival | ours | 10.9/11.5 | 5.8/12.4 | 10.7/11.8 | 5.7/11.7 | 10.5/11.5 | 5.8/11.7 |
| rival late units d15-29 | ours | 2189 | 1278 | 1876 | 1266 | 2182 | 1265 |
| rival animal-product u d18-29 (E+M+W) | ours | 288 | 290 | 330 | 269 | 328 | 266 |
| strawberry u d15-17 rival | ours | 36.1 | 45.1 | 35.9 | 48.1 | 34.2 | 48.5 |
| wheat u d10-29 rival | ours | 1633 | 315 | 1117 | 353 | 1494 | 356 |
| revenue d0-9 / d10-14 / d15-29 rival (k) | 18.3/45.4/117.5 | 16.2/39.2/112.4 | 16.7/45.4/126.1 |
| revenue d0-9 / d10-14 / d15-29 ours (k) | 14.7/11.7/106.4 | 14.1/10.8/97.1 | 14.1/10.7/93.5 |
| rival land / hire spend (k) | 3.7 / 6.0 | 3.3 / 5.8 | 3.2 / 5.9 |

- **Old V56 kernel fired live (14 in-band seats on vrp15/vrp19w):** 2-12 at -9,002 (unpaired).
  - V56 sells 72 melons d10-14 @218. That holds the d14 cash gap at +1.0k (PFS: -18.9k), yet the game is lost in d15-29.
  - Mirroring the melon wave closes the d10-14 swing, not the game.
- **d15-29 by product, wins vs losses** (per game; our rev | rival rev):
  - WOOL +2,027 | -4,036 (rival 90 vs 130 u)
  - MILK +1,655 | -2,809
  - EGG +605 | -1,307
  - MELON +1,594 | -3,022
  - STRAWBERRY +2,588 | -1,123
  - WHEAT -1,425 | +14,053 (relay seats; rival spend 46.3k vs 29.0k)
- **Wheat-relay variant.** 15 of 78 seats have rival wheat units d10-29 >= 1,500 (2885, 1, 2338, 73, 85, 2869, 2046). These rivals buy wheat and sell it back.
  - The variant inflates the rival's late units (3.5-5.4k) and revenue.
  - Its melon wave (50-61 @246-250), Q days and d14 gap (-21.2k/-21.8k) are the class's.

### D. The otherMELON tape set `S/othermelon1/tapes/` (om16; boards `S/othermelon1/boards_om16.json`, boards_live27 format)
- **Built with the S/bceval1/build.py recipe:** `scripts/tape_opponent.py` extract_tape + render_main + verify, live finals, JC1 rival units.
- **Label:** `tape_h<h1>_<team>_<ep>`.
- **Seats:**
  - All are in-band other-MELON games where our seat played PFS live: 15 vrp20, plus 1 vrp15 unfired seat (2511).
  - 8 on-list seats, none already in fired18: 2338 x3, 26 x2, 2600, 2097, 2511.
  - 8 off-list seats: 2854 x2, 2885 x2, 7, 20, 1761, 700.
- **Tape checker** (TO.verify, recorded pre-states fed to the emitted agent): **0 disagreements on 16/16.**
- **PFS baseline** (dist/vrp20_pfsoff, md5 e5d84f03, the 56686302 bytes). Its own kagg3 image (`pkg_pfs/kagg3/agent/runtime.py`, FIRE_CASH 99999) played as a FILE agent vs each tape, 20:56Z-21:04Z, one worker at nice 19. Exact = both final purses equal live. **16/16 exact** (harness = live purses), baseline W 3/16 (on-list 1/8, off 2/8), rival h1 in the harness = live h1 on 16/16.
  - **Every om16 seat is JC1-faithful:** the harness replays the live game exactly, so any candidate's paired delta on om16 is exact against PFS.

| label | list | live margin (W) | harness ours / theirs | exact | rival h1 harness | sec |
|---|---|---|---|---|---|---|
| tape_h2338_azamaro_115388032 | ON | +934 (1) | 88,824 / 87,890 | True | 2338 | 23 |
| tape_h2338_yannikschiffne_115050572 | ON | -18,468 (0) | 126,025 / 144,493 | True | 2338 | 21 |
| tape_h2338_yusukehayashi_114978773 | ON | -333 (0) | 87,569 / 87,902 | True | 2338 | 21 |
| tape_h26_boominginging_115324560 | ON | -14,355 (0) | 113,253 / 127,608 | True | 26 | 22 |
| tape_h26_mhw_115337927 | ON | -23,388 (0) | 77,420 / 100,808 | True | 26 | 26 |
| tape_h2600_lzeee_115326453 | ON | -583 (0) | 75,412 / 75,995 | True | 2600 | 26 |
| tape_h2097_mysecondlife_115006822 | ON | -35,398 (0) | 86,158 / 121,556 | True | 2097 | 28 |
| tape_h2511_ymgaq_114748497 | ON | -12,112 (0) | 101,829 / 113,941 | True | 2511 | 26 |
| tape_h2854_yjshyfy_115023335 | off | -1,324 (0) | 136,892 / 138,216 | True | 2854 | 28 |
| tape_h2854_zhenghongshuan_115293787 | off | -11,057 (0) | 77,311 / 88,368 | True | 2854 | 23 |
| tape_h2885_alexoranov_115238868 | off | -9,448 (0) | 84,580 / 94,028 | True | 2885 | 24 |
| tape_h2885_dash_115284410 | off | -23,488 (0) | 74,312 / 97,800 | True | 2885 | 24 |
| tape_h7_tx_115177238 | off | -14,494 (0) | 84,401 / 98,895 | True | 7 | 24 |
| tape_h20_goose10_115243853 | off | +1,714 (1) | 100,326 / 98,612 | True | 20 | 24 |
| tape_h1761_mhiro2_115102803 | off | +20,197 (1) | 126,669 / 106,472 | True | 1761 | 28 |
| tape_h700_12345678910111_114974782 | off | -5,247 (0) | 81,047 / 86,294 | True | 700 | 27 |

### E. Whitelist question (report only; `res/whitelist_report.md`)
- **Keep all 14 on-list other-MELON values on the isolation criterion.**
  - 0 V hits in 493 games (0/348 in BRAINSTORM5's window), and every in-band seat on the programme timetable.
  - Per-value margins (n 1-8) cannot decide anything. Unpaired in-band margin SD is 12.8k, so +3k at t >= 2 would need ~73 live games per value.
  - 2097 is a PQ4 team (My second life, Q4 d10). Count it with PQ4 when judging.
- **Never cash-listable (V collisions in these 493):** 2854 (V 44), 2867 (V 68), 3037 (V 4), 2885 (V 1), 2864, 2869.
  - 2854 alone is 0-10 at -10.2k, and 2885 is 1-5. Only a behavioural latch (d2 crops) reaches them.
- **Cash-listable off-list losers (0 V hits, n 2-4):** 7 (TX 0-4), 700 (0-3), 27, 33, 113, 3, 1026.
  - A live check needs >= 3 observations of the value, 0 V hits, every seat on the timetable, and the package's paired margin >= 0 on a faithful tape of that value.
- **Must not fire:** 1761 (mhiro2 3-0) and 20 (goose10 3-4, -760: 3 of our 12 in-band other-MELON wins).
- **Two-sided bar for any extension:** pooled paired margin >= 0 on the added values' tapes, and no added value with d-margin < 0 at t >= 2.
- **DECEM / Majkel:** >= 3 live games against a PFS-h0 sub each before their predicted values (1938 / 1992) are even considered. 1761 is excluded (mhiro2).

### F. Round-2 build a fresh round could defend
- **d2 class latch.** Fire from d2 h0 when the rival has 1-10 melon tiles and not the V pattern (lw23 fam == MELON). The candidate client is C1 (volume from d10), or any package whose first deviation is at d2 or later.
  - It cannot serve an h1 package such as PROGFIRE1's bridge (closed NONE, BUILD-STORY).
- **What it changes.** In-band other-MELON coverage goes 20/78 -> 78/78. P48/PQ4 stay at 100 %.
  - V identity: the latch reads the same d2 rule that defines the V family here, so it holds on every seat the rule calls V. In band the counts do not overlap: V 11-12 melons at d2 (162 seats), MELON <= 10 (168). The independent check is the V56 m40 + v21 judge boards, which must read V at d2 (exact-identity leg).
  - The low-rated MELON seats (19-1) would also fire. The gate must include them, or the latch needs a d9 cash-gap guard.
- **Expected coins now: 0.** No fired package has a positive paired margin on any MELON judge (BRAINSTORM5 B, PROGFIRE1).
  - Wins vs losses (unpaired) differ on the rival's late herd (wool 90 vs 130 u, milk -2.8k, eggs -1.3k), not on ours. The only PFS-side lever left is denying those prices by our own late volume, the line D10F lost on (-4,215 on fired18).
- **Gate for the latch's first client:**
  - BRAINSTORM5 E legs 1-7;
  - om16 on-list 8: paired margin >= 0 and W >= baseline;
  - om16 off-list 8: margin >= 0 under the latch (they fire under it);
  - V56 m40 + v21: exact identity;
  - low-rated MELON: W not lower.



## Round 2 (EARLYLAND1, 21:17Z-~22:35Z)

**Verdict: NONE. Every arm fails astra's stage 1 (dose) on the programme boards; the gate ends there. No stage 2-5, no package, no `_pin` row, no upload slot used.**
- **The rule has one funding source on PFS.** PFS holds no output at dawn d6-10: its shed is feed wheat plus at most ten egg/fertilizer/wool units, all sold in lot 1 the same morning, and the day's harvest stays with the hands until dusk. So "sell available output earlier" has nothing to sell. The land is paid in PFS's own coin order (crew bill, tomorrow's reserve, land, then the greedy), with the day's seed and feed protected. What it displaces is the day's **herd purchase**.
- **Dose (stage 1).** Q3 by d8 h6 on **8/8** V56 screen games (all arms), but only **13/16** programme boards. The 3 misses are short 29, 67 and 241 coins at the d8 land slot (post-bill purse + 3/4 of lot 1 < 2,000 + the day's seed and feed). Q4 by d10 h9: 7/8 V56, **11/16** programme. Bar >= 14/16 and >= 7/8: **L3, L3H, L4, L4H all FAIL.**
- **Mechanism (diagnostic, the same stage-1 games).** The d8 land takes the d8 herd purchase: herd d9 **-3.25 (t -13) on V56**, -2.31 on the programme boards. L3 recovers to -1.1 by d18; L4 does not (-1.9 / -2.8).
  - L3/L3H: plantings d10-27 +3.6 (V56) / -2.0 (programme); d8-9 plantings **-1.6 on V56**, so the early Q3 tiles sit empty on d8-9. Harvested units d10-29 -58 (t -5.1), eggs -33.
  - L4/L4H: plantings d10-27 **+41** (V56) / +31-34 (programme), hands +1.6/day, but harvested units only +29 / +5 (V56) and +9 / -20 (programme). Tomato +54, strawberry +29, melon +25; egg -28, milk -9..-12, wool -14. Spend d10-29 **+12.3k** against sale revenue +5.1k. Rival milk + wool revenue **+2.7k / +3.4k** (V56) and +2.6k / +4.1k (programme).
  - That is astra's watched failure signature exactly: timely Q4, weak harvest growth, rival milk/wool revenue up.
- **Coins (diagnostic, not a gate read).** V56 screen 8 margin: L3 **-2,568 (t -7.0)**, L3H -2,824 (-5.2), L4 -8,893 (-3.4), L4H -10,339 (-4.3); W 4/8 -> 3, 2, 2, 2. Programme 16 (p48c): L3 -782 (-0.5), L3H +481 (+0.3), L4 -4,787 (-1.9), L4H -5,106 (-2.0). The rival gains +1.3k..+4.4k in every cell.

### A. Build, identity, harness
- `LAND_FUND_ON` (default OFF) in `core/plan.py`, commit 0ab9ee07 on `earlyland1_0929` (worktree `kagg3_wt_earlyland1`, base 8d670dad = the PFS anchor). Patch script `S/earlyland1/patch.py`.
  - `LAND_FUND_SCHED` = preset `L3` ((8, 3)) or `L4` ((8, 3), (10, 4)): the deadline day of the purchase that makes the next quadrant count. The purchase is forced on that day's land slot (turn 3, h3-4) only if `purse + 3/4 lot 1 >= land price + g0_sf`, where `g0_sf` = the seed + feed-wheat + fertilizer part of the grant PFS makes that day without land. Otherwise it is a missed dose: no later forced buy (the deadline is past), so an arm never degrades into the late-Q4 cell.
  - `LAND_FUND_HANDS=12` (L3H/L4H): crew = max(PFS argmax, the largest affordable crew <= 12) on d10-28, under PFS's own affordability test (bill + tomorrow's reserve). It is skipped on a day whose scheduled land is still pending (L4H: from d11), because the land comes first in the coin order.
  - `LAND_FUND_FROM` (default 99 = off): a diagnostic hold of pre-deadline animal purchases. Smoke on 2 boards: identical with 6, because the d9 purse after Q3@d8 is 9-130 coins.
- **Identity OFF: 8/8 exact** (the V56 screen's 4 m40 + 4 v21 games, 10 money columns == `S/vband1/res/v56_ctl_*` rows).
- Harness `S/earlyland1/h/el_rc.py` = `S/brainstorm5/t5/t5_rc.py` plus read-only hooks: dawn cash, quadrant hours, all market rows d5-12 with the hour's money, shed per product d5-12, per-day production and new plantings for both farms, and the plan's `LF_DIAG` rows. V56 runs local (`lchain.sh`, `S/vband1/vr.py`); p48c runs remote (`rchain.sh`, `S/judgerival1/rcr.py --rival p48c`, 2 workers, nice 19).

### B. Stage 1 — dose, wall, escapes, funding waterfall (`res/stage1.md`)
### V56 screen 8 (4 m40 + 4 v21) (control ctl_s8)
| arm | n | Q3 by d8h6 | Q4 by d10h9 | straw tiles d6/d7/d8/d9/d10 (arm-ctl mean) | boards with |d10 diff|>1 | escapes/g arm vs ctl | herd d9/d14/d18 (arm-ctl) | d8 land slot: view money / post-bill money / rev1 (3/4) / g0 seed+feed / fundable | d10 (Q4): view / money / rev1 / g0 / fundable |
|---|---|---|---|---|---|---|---|---|---|
| L3 | 8 | 8/8 | 0/8 | +0.0 / +0.0 / +0.0 / -0.8 / -0.5 | 2/8 | 3.38 vs 2.75 | -3.2 / -1.2 / -1.1 | 2118 / 2048 / 587 / 144 / 8/8 | 5258 / 4508 / 1100 / 485 / 7/8 |
| L3H | 8 | 8/8 | 0/8 | +0.0 / +0.0 / +0.0 / -0.8 / -0.5 | 2/8 | 3.12 vs 2.75 | -3.2 / -1.1 / -1.0 | 2118 / 2048 / 587 / 144 / 8/8 | 5258 / 3815 / 1100 / 485 / 5/8 |
| L4 | 8 | 8/8 | 7/8 | +0.0 / +0.0 / +0.0 / -0.8 / +0.0 | 2/8 | 2.38 vs 2.75 | -3.2 / -2.4 / -1.9 | 2118 / 2048 / 587 / 144 / 8/8 | 5258 / 4414 / 1100 / 485 / 7/8 |
| L4H | 8 | 8/8 | 7/8 | +0.0 / +0.0 / +0.0 / -0.8 / +0.0 | 2/8 | 1.25 vs 2.75 | -3.2 / -2.9 / -2.2 | 2118 / 2048 / 587 / 144 / 8/8 | 5258 / 4414 / 1100 / 485 / 7/8 |

### programme boards 16 (p48c clone, S/p48graph1 boards_p48_16) (control ctl_p16s0_w0,ctl_p16s1_w1)
| arm | n | Q3 by d8h6 | Q4 by d10h9 | straw tiles d6/d7/d8/d9/d10 (arm-ctl mean) | boards with |d10 diff|>1 | escapes/g arm vs ctl | herd d9/d14/d18 (arm-ctl) | d8 land slot: view money / post-bill money / rev1 (3/4) / g0 seed+feed / fundable | d10 (Q4): view / money / rev1 / g0 / fundable |
|---|---|---|---|---|---|---|---|---|---|
| L3 | 16 | 13/16 | 0/16 | +0.0 / +0.0 / +0.4 / -0.1 / -0.2 | 0/16 | 4.81 vs 4.31 | -2.3 / -0.1 / -0.3 | 2020 / 1942 / 598 / 246 / 13/16 | 5302 / 4702 / 816 / 239 / 16/16 |
| L3H | 16 | 13/16 | 0/16 | +0.0 / +0.0 / +0.4 / -0.1 / -0.3 | 1/16 | 4.75 vs 4.31 | -2.3 / -0.4 / -0.8 | 2020 / 1942 / 598 / 246 / 13/16 | 5302 / 4279 / 816 / 239 / 15/16 |
| L4 | 16 | 13/16 | 11/16 | +0.0 / +0.0 / +0.4 / -0.1 / -0.1 | 1/16 | 2.88 vs 4.31 | -2.3 / -3.4 / -2.8 | 2020 / 1942 / 598 / 246 / 13/16 | 5302 / 4497 / 816 / 239 / 14/16 |
| L4H | 16 | 13/16 | 11/16 | +0.0 / +0.0 / +0.4 / -0.1 / -0.1 | 1/16 | 3.06 vs 4.31 | -2.3 / -4.6 / -3.3 | 2020 / 1942 / 598 / 246 / 13/16 | 5302 / 4383 / 816 / 239 / 14/16 |

### C. Unit and purse books (`res/books_stage1.md`, arm minus control, board-clustered t)
### V56 screen 8: n=8, arm minus control (t board-clustered)

| book | control | L3 | L3H | L4 | L4H |
|---|---|---|---|---|---|
| own | 104,368.0 | -556 (-1.0) | -818 (-1.2) | -7,254 (-4.7) | -7,745 (-4.2) |
| rival | 101,916.1 | +2,013 (+3.8) | +2,006 (+3.8) | +1,639 (+1.1) | +2,594 (+2.0) |
| margin | 2,451.9 | -2,568 (-7.0) | -2,824 (-5.2) | -8,893 (-3.4) | -10,339 (-4.3) |
| W | 0.5 | -0.12 (-1.0) | -0.25 (-1.5) | -0.25 (-1.5) | -0.25 (-1.5) |
| plantings d8-9 | 12.1 | -1.62 (-2.2) | -1.62 (-2.2) | -1.62 (-2.2) | -1.62 (-2.2) |
| plantings d10-27 | 146.8 | +3.62 (+2.2) | +3.25 (+1.7) | +41 (+6.7) | +41 (+7.0) |
| hands/day d10-28 | 9.6 | -0.14 (-2.7) | -0.11 (-1.5) | +1.59 (+5.8) | +1.55 (+5.3) |
| harvested u d10-29 (all) | 1,650.5 | -58 (-5.1) | -57 (-4.7) | +29 (+1.1) | +5.25 (+0.2) |
|   wheat | 533.8 | -7.12 (-1.1) | -8.12 (-1.0) | -2.12 (-0.1) | -11 (-1.0) |
|   carrot | 109.0 | +5.25 (+1.6) | +4.25 (+1.0) | +10 (+1.4) | +5.00 (+0.7) |
|   tomato | 36.6 | +3.62 (+1.6) | +2.62 (+1.3) | +54 (+3.0) | +54 (+3.0) |
|   strawberry | 250.8 | +2.25 (+0.8) | +2.00 (+0.8) | +29 (+2.4) | +33 (+2.7) |
|   melon | 87.8 | +1.50 (+0.8) | +1.50 (+0.8) | +25 (+4.0) | +22 (+4.1) |
|   egg | 126.1 | -33 (-4.1) | -33 (-4.1) | -28 (-2.3) | -38 (-2.4) |
|   milk | 171.1 | -3.62 (-0.9) | -3.75 (-0.9) | -9.38 (-2.0) | -12 (-2.1) |
|   wool | 86.8 | -6.00 (-1.6) | -3.62 (-0.9) | -14 (-1.3) | -10 (-0.8) |
| straw u sold d15-17 | 48.5 | -0.50 (-1.0) | -0.25 (-1.0) | -0.50 (-1.0) | -0.75 (-1.4) |
| E+M+W u sold d18-29 | 254.5 | -24 (-2.8) | -21 (-2.1) | -20 (-1.5) | -23 (-1.4) |
|   milk u d18-29 | 111.2 | -0.75 (-0.2) | -1.00 (-0.2) | -6.50 (-1.4) | -6.12 (-1.4) |
|   wool u d18-29 | 56.4 | -2.12 (-0.7) | +0.75 (+0.2) | -2.38 (-0.2) | +1.50 (+0.1) |
|   egg u d18-29 | 86.9 | -21 (-3.6) | -21 (-3.6) | -11 (-1.1) | -18 (-1.5) |
| herd d9 | 11.8 | -3.25 (-13.0) | -3.25 (-13.0) | -3.25 (-13.0) | -3.25 (-13.0) |
| herd d14 | 16.0 | -1.25 (-3.0) | -1.12 (-2.3) | -2.38 (-3.1) | -2.88 (-4.5) |
| herd d18 | 16.0 | -1.12 (-2.8) | -1.00 (-2.2) | -1.88 (-2.5) | -2.25 (-3.0) |
| escapes | 2.8 | +0.62 (+1.4) | +0.38 (+1.2) | -0.38 (-0.3) | -1.50 (-1.5) |
| rival milk rev d10-29 | 19,658.5 | +522 (+1.6) | +532 (+1.6) | +936 (+2.3) | +1,847 (+2.9) |
| rival wool rev d10-29 | 13,127.8 | +547 (+2.8) | +532 (+2.9) | +1,775 (+1.2) | +1,521 (+1.1) |
| spend d0-9 | 12,057.6 | +121 (+0.4) | +121 (+0.4) | +121 (+0.4) | +121 (+0.4) |
| spend d10-17 | 7,450.0 | -280 (-0.7) | -241 (-0.5) | +4,673 (+4.4) | +4,407 (+4.0) |
| spend d18-29 | 4,482.5 | -81 (-0.3) | -24 (-0.1) | +7,673 (+5.7) | +7,905 (+4.8) |
| sale rev d0-9 | 14,334.4 | +151 (+4.8) | +151 (+4.8) | +151 (+4.8) | +151 (+4.8) |
| sale rev d10-17 | 32,170.2 | -1,969 (-7.4) | -2,154 (-5.1) | -4,225 (-3.5) | -4,936 (-4.2) |
| sale rev d18-29 | 78,853.5 | +1,022 (+1.3) | +1,042 (+1.4) | +9,287 (+3.9) | +9,473 (+3.6) |
| cash d9 dawn | 1,939.2 | -1,248 (-5.0) | -1,248 (-5.0) | -1,248 (-5.0) | -1,248 (-5.0) |
| cash d11 dawn | 3,857.2 | +1,216 (+6.4) | +1,282 (+6.6) | -1,297 (-2.7) | -1,297 (-2.7) |
| cash d14 dawn | 7,493.1 | +173 (+1.5) | +135 (+1.0) | -2,791 (-4.0) | -2,646 (-3.7) |

### programme 16 (p48c): n=16, arm minus control (t board-clustered)

| book | control | L3 | L3H | L4 | L4H |
|---|---|---|---|---|---|
| own | 113,008.6 | +517 (+0.6) | +1,790 (+1.8) | -1,551 (-0.7) | -706 (-0.4) |
| rival | 86,697.7 | +1,298 (+1.3) | +1,309 (+1.2) | +3,237 (+3.2) | +4,400 (+3.1) |
| margin | 26,310.9 | -782 (-0.5) | +481 (+0.3) | -4,787 (-1.9) | -5,106 (-2.0) |
| W | 1.0 | +0.00 (-) | +0.00 (-) | +0.00 (-) | -0.06 (-1.0) |
| plantings d8-9 | 7.8 | +2.56 (+3.9) | +2.56 (+3.9) | +2.56 (+3.9) | +2.56 (+3.9) |
| plantings d10-27 | 147.1 | -2.00 (-2.4) | -1.19 (-1.5) | +31 (+5.5) | +34 (+5.7) |
| hands/day d10-28 | 10.0 | -0.06 (-0.6) | -0.06 (-0.7) | +0.69 (+3.7) | +0.54 (+3.1) |
| harvested u d10-29 (all) | 1,705.7 | -26 (-2.3) | -35 (-2.9) | +8.69 (+0.8) | -20 (-1.6) |
|   wheat | 538.5 | -1.81 (-0.3) | -6.38 (-1.3) | +9.25 (+1.1) | +1.44 (+0.1) |
|   carrot | 143.9 | -1.19 (-0.3) | +5.19 (+1.6) | +8.88 (+2.6) | +16 (+2.7) |
|   tomato | 34.6 | +1.62 (+0.9) | +2.25 (+1.4) | +48 (+3.4) | +47 (+3.4) |
|   strawberry | 214.1 | +2.50 (+1.5) | +5.19 (+2.6) | +17 (+2.6) | +15 (+2.5) |
|   melon | 99.4 | +1.50 (+1.5) | -0.75 (-0.5) | +16 (+5.1) | +17 (+4.4) |
|   egg | 111.6 | -13 (-2.3) | -14 (-2.5) | -23 (-2.4) | -27 (-2.4) |
|   milk | 155.6 | -7.06 (-1.7) | -9.69 (-3.6) | -8.56 (-1.4) | -18 (-2.4) |
|   wool | 141.3 | +6.50 (+1.2) | +5.06 (+0.9) | -17 (-2.5) | -20 (-2.8) |
| straw u sold d15-17 | 46.8 | +2.19 (+2.9) | +0.56 (+1.0) | +1.00 (+1.6) | +1.56 (+2.7) |
| E+M+W u sold d18-29 | 271.8 | -4.19 (-0.5) | -7.00 (-0.9) | -16 (-1.7) | -30 (-3.1) |
|   milk u d18-29 | 96.2 | -5.38 (-1.4) | -7.12 (-2.6) | -5.69 (-1.1) | -15 (-2.1) |
|   wool u d18-29 | 99.6 | +8.31 (+1.5) | +7.19 (+1.4) | +1.56 (+0.3) | -1.44 (-0.3) |
|   egg u d18-29 | 76.0 | -7.12 (-1.8) | -7.06 (-1.7) | -12 (-1.9) | -14 (-1.8) |
| herd d9 | 10.6 | -2.31 (-6.6) | -2.31 (-6.6) | -2.31 (-6.6) | -2.31 (-6.6) |
| herd d14 | 18.3 | -0.12 (-0.5) | -0.44 (-1.8) | -3.44 (-6.6) | -4.56 (-6.6) |
| herd d18 | 18.4 | -0.31 (-1.2) | -0.75 (-2.8) | -2.81 (-5.5) | -3.31 (-5.3) |
| escapes | 4.3 | +0.50 (+0.7) | +0.44 (+0.7) | -1.44 (-2.3) | -1.25 (-1.3) |
| rival milk rev d10-29 | 20,170.2 | +940 (+1.6) | +1,241 (+2.4) | +913 (+1.2) | +1,775 (+1.7) |
| rival wool rev d10-29 | 15,451.5 | -345 (-0.4) | +93 (+0.1) | +1,682 (+1.4) | +2,374 (+1.8) |
| spend d0-9 | 11,220.1 | +794 (+5.2) | +794 (+5.2) | +794 (+5.2) | +794 (+5.2) |
| spend d10-17 | 10,057.8 | -1,054 (-4.6) | -1,126 (-6.5) | +1,316 (+2.5) | +1,013 (+1.9) |
| spend d18-29 | 4,453.2 | +219 (+0.8) | +85 (+0.3) | +4,342 (+4.1) | +4,148 (+4.3) |
| sale rev d0-9 | 14,282.9 | +75 (+3.2) | +75 (+3.2) | +75 (+3.2) | +75 (+3.2) |
| sale rev d10-17 | 37,034.2 | -1,594 (-4.3) | -1,735 (-4.9) | -5,028 (-4.4) | -5,054 (-4.3) |
| sale rev d18-29 | 84,422.4 | +1,995 (+2.1) | +3,203 (+3.2) | +9,855 (+3.9) | +10,228 (+4.2) |
| cash d9 dawn | 1,809.9 | -904 (-3.1) | -904 (-3.1) | -904 (-3.1) | -904 (-3.1) |
| cash d11 dawn | 2,570.2 | +540 (+3.9) | +702 (+4.9) | -425 (-1.9) | -425 (-1.9) |
| cash d14 dawn | 5,943.1 | -226 (-1.8) | -288 (-2.5) | -1,290 (-4.4) | -957 (-3.2) |

### D. Round-3 proposal (<= 10 lines)
(not saved before the /mnt/e outage; the session's round 3 = the astra brainstorm12 session summary below.)


## Round 3 (session summary, astra brainstorm12, 2026-09-30)

Verbatim from gpt-6-astra (also `docs/strategy/2026-09-30-astra-brainstorm12.md`).

1. Established: PFS remains the anchor: 42–1 against V-family seats, approximately 27% against live P48, and no demonstrated MMPQ win.
2. Established: learned programme clones are invalid selection judges; their 95–99% PFS loss rate contradicts live results.
3. Established: MMPQ is an opponent-independent, shop-conditioned rulebook across 241 observed games; 29 rules are exact, 17 partial, five missing.
4. Established: the corrected tape reproduces MMPQ’s opening on 16/16 boards, including expansion timing and 71 productive tiles at d9.
5. Established: opening fidelity alone fails: the best tape/PFS continuation scored 21/40 and −9.8k against V56; quotas worsened it.
6. Established: that executor moves from +6.9k cash at d18 to −3.8k at the finish relative to control; inspect the complete asset ledger before attributing the entire reversal to operating losses.
7. Established: MMPQ’s observed V-class advantage centers on late eggs and early strawberries; wool denial is not its general explanation.
8. Closed: early land expansion inside PFS, sale-timing-only repairs on examined P48 losses, and clone victories as evidence of programme strength.
9. Open: PROGRAMME2R’s economic fidelity and tournament strength; P48RULES1R’s faithful rival; P48LOSS1R’s supply-sensitive loss mechanisms.
10. Open: packaging depends on drive recovery. Preserve the live PFS pair unless a validated replacement is uploadable before 18:00Z.
11. My implementation priority is **(d) economic completion of PROGRAMME2R, then (a), then (c), then (b)**. This orders development paths, not leaderboard outcomes.
12. (d) means complete the standalone rulebook’s revenue-critical rules, replay them through d30, and defer harmless action-level mismatches. Reuse the running implementation; do not start another architecture.
13. Expected incremental coins versus PFS: **unidentified numerically on both V56 and P48**. The supplied +32.4k is MMPQ versus V-class seats, not a measured PROGRAMME2R-minus-PFS effect.
14. For (d), my directional expectation is positive on V56 if production fidelity holds; P48 remains uncertain. Principal failure: apparent replay fidelity hides a resource dependency or an untested shop branch.
15. For (a), expected coins should converge toward (d) if both reproduce the same economy; neither has a supported numeric delta yet. Principal failure: spending the remaining window matching inconsequential rules while delaying evaluation.
16. For (c), the late egg component offers upside on V56, but its size and P48 effect are unknown. Principal failure: PFS lacks the earlier herd, feed, labor, or cash required to realize the copied late schedule.
17. For (b), both deltas remain unknown; the existing opening/PFS splice’s −9.8k is a warning, not an estimate for this new hybrid. Principal failure: the substituted middle hands the late rulebook an incompatible farm.
18. Thus (c) is a bounded diagnostic if capacity remains; (b) should receive no new implementation budget before PROGRAMME2R’s result.
19. Calculate candidate value from matched boards: Δcoins = terminal candidate coins − terminal PFS coins, separately for V56 and P48. Report wins alongside it; coins alone do not establish competitive strength.
20. The production opportunity to explain is 136 additional late eggs and ten additional early strawberries in the supplied comparison; price them at realized sales and subtract feed, acquisition, labor, and displaced output.
21. The identities of the five missing and 17 partial rules were not supplied. The following is an economic audit order, not a claim that these exact rules are unresolved.
22. First: goose acquisition, production calendar, and feed-before-production execution. Proxy: observed shop-conditioned purchase lots plus exact simulator production eligibility; never substitute a target herd count for productive animals.
23. Second: feed procurement and allocation across the whole herd. Proxy: fund the next production obligations before discretionary purchases; replay shortages explicitly.
24. Third: sale cadence, sale ordering, and terminal liquidation. Proxy: the observed four-hour sell-all schedule after d12, with transaction ordering checked against the engine.
25. Fourth: strawberry planting, labor, and harvest timing around d15–17. Proxy: observed cohorts and their resource requirements, not a terminal strawberry quota.
26. Fifth: middle-game animal mix and shop-conditioned sheep/cow spending. Proxy: observed branches by shop draw; preserve their downstream cash and feed obligations.
27. Sixth: expansion funding and action priority. Proxy: the verified opening and cash-triggered Q4 rule; a milk sale and a sheep purchase cannot be reordered casually.
28. Seventh: melon/wheat occupancy and labor allocation. Proxy: reproduce the 60-melon phase and fill genuinely available capacity with wheat; reserve inputs needed for scheduled production.
29. Eighth: endgame planting, harvesting, feeding, and liquidation. Proxy: no planting after d27, harvest existing crops when worthwhile, and fund animal feed only when its production can count before termination.
30. Last: ties and cosmetic action differences without downstream resource effects. Proxy: a deterministic legal tie-breaker; promote it only if paired traces reveal a coin consequence.
31. No proxy is “safe” merely because it sounds plausible. Safety here means preserving production, cash feasibility, and terminal value on held-out traces.
32. The **one decisive read by 15:00Z** is a frozen-candidate, held-out acceptance panel for PROGRAMME2R, with matched PFS controls and full-game ledgers.
33. Require the stated replay bar, then V56 m40 ≥37/40 with ≥+6k margin and v21 ≥12/21, using the established margin definition.
34. Require programme-board mean margin ≥0 and improvement over matched PFS; show results separately for P48 and any available MMPQ boards.
35. Programme evidence must use actual programme bodies or rivals validated against their real full-game traces. Passing another unfaithful clone does not satisfy the gate.
36. Inspect late eggs, strawberries, feed failures, unsold terminal stock, and worst losses within that same panel; averages must not conceal a broken shop branch.
37. If it passes, package and use the one bold slot beside PFS. Begin drive recovery and packaging preparation now; leave the final three hours for artifact verification and upload.
38. If it fails—or faithful programme evidence or packaging is unavailable—retain PFS. Do not promote an untested hybrid because time is expiring.
39. Fresh-session prompt: “You are a participant in BRAINSTORM7; use numbered lines, distinguish measurements from hypotheses, and give no rank forecasts.
40. Deadline: uploads close 2026-09-30 18:00Z; selection gate 15:00Z; report current time and packaging availability.
41. Preserve PFS as anchor: 42–1 versus V-family, approximately 27% versus live P48, no demonstrated MMPQ win.
42. Early-land PFS is closed; learned programme clones are invalid judges; sale-timing-only P48 repairs have not helped.
43. MMPQ is a shop-conditioned deterministic rulebook: 29 exact rules, 17 partial, five missing across 241 games.
44. Its opening reproduces on 16/16 boards; opening plus PFS continuation fails, with the major deterioration after d18.
45. Its observed V-class edge centers on late eggs and early strawberries; one P48 replay also exposes a large wool-supply effect.
46. Obtain PROGRAMME2R, P48RULES1R, and P48LOSS1R results; include exact artifacts, evaluated boards, and unresolved rule identities.
47. Prioritize a complete feasible production economy in PROGRAMME2R; audit feeding, herd acquisition, sales, strawberries, and shop-conditioned cash.
48. Report matched terminal-coin deltas versus PFS separately from candidate-versus-opponent margins and wins.
49. Acceptance: replay fidelity; V56 m40 ≥37/40 and ≥+6k; v21 ≥12/21; faithful programme-board margin ≥0 with improvement over PFS.
50. Recommend one concrete bold artifact only if validated and packageable by cutoff; otherwise retain PFS and identify the failed gate.”