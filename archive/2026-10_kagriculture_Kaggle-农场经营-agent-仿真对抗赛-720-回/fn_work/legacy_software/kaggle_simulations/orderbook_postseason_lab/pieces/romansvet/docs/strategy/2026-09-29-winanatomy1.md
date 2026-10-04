# WINANATOMY1 (2026-09-29): why PFS beats a programme rival live, when it does

Question: when the shipped PFS body beats a MELON-family ("programme") rival live, is it the board and shop draw, the rival's version or bad day, or something PFS did in d10-14 that it does not do in the losses?

Answer: it is the rival's version or the late shop draw, and only once a clear rival bad day. PFS does nothing different. Its d0-2 purchases are identical in all 42 main games. PFS still loses d10-14 in its wins (-19.0k margin, against -22.8k in the losses). The wins are decided in d18-29: +10.5k margin over the losses, t 4.61.
- **Board: 4 of 7 wins.** The shop draw lifted the d18-29 price of a product PFS already holds: wool after YARN_STOREs, milk after an ICE_CREAM_SHOP, or tomato.
- **Rival weaker: 3 of 7 wins.** One was a bad day: goose10, 28.8k below its own median. Two were weaker versions scoring at their own norm: chungkuangwen and loxigicck, with own medians of 95.8k and 96.9k.
- **Rival bad days do not separate wins from losses.** Against each rival sub's own median from ListEpisodes (25 subs, 90-570 games each vs other teams), the rival's day averages -2.8k in wins and -0.3k in losses (t -0.35). What does differ is the rival's level: its own median is 100.1k in wins vs 103.4k in losses (t -1.79).
- **PFS did something: 0 of 7 wins.**

No switch makes a win deliberate. The only PFS difference is a response to the game state: +4 melon tile-days in d0-9, worth about +1k in d15-17 melon sales. That is the MELONTRIAL1 d0-1 plate family, which is already built.

Method. The list comes from the LIVEWATCH23 tsvs (S/livewatch23/lw23_<sub>.tsv): family MELON, rival oppR0 >= 2,450, v56obs 0 (unfired) and pfsid 1 (PFS h0/h1 identity).
- Five subs are included: the four named in the brief plus vrp17_k2hb 56643352. Its unfired games are PFS-identical, and it adds 2 W / 5 L. Without it the main set is 5 W / 30 L.
- All 64 MELON-unfired replays were already local (S/livewatch23/gz, S/livewatch22/gz, S/livewatch21/gz), so there were **0 replay fetches**. The rival norms in section 3 took 25 ListEpisodes calls, 10 s apart, with **0 HTTP 429**.
- Exact engine ledger: S/econcensus census.measure reused file-scoped (as in S/pricegap1/live_ledger.py) on both seats of all 64 games. Cash mismatch was 0 and closure error was 0 on 128/128 seat-ledgers.
- Scripts are in S/winanatomy1: list2.py, ledger.py, analyze.py, perwin.py, board.py, checks.py and q2.py. Results are in S/winanatomy1/res/.
- Welch t compares wins with losses. Margins are two-purse (PFS final minus rival final).

## 1. The list

- **Main set (rival R0 >= 2,450): 7 W / 35 L.**
  - Win rivals: 7 distinct subs, none repeated: Gradient Grazing 56620547, vvs 56638736, goose10 56620389, fog flower 56642047, thisray 56629395, chungkuangwen 56596923 and loxigicck 56637818.
  - Win-rival R0 averages 2,526; loss-rival R0 averages 2,555 (t -1.76).
  - Only thisray 56629395 appears on both sides: PFS beat it in 114689938 and lost to it in 114655920.
  - Loss rivals include istinetz (56546676 ×3, 56618797), Satoshi_SsSs ×2, leave you 56639078 ×3, AI ×2, Planned Economy ×2 subs and ijiiok ×2 subs.
- **Wins by sub:** vrp15_k2fire 5/26, vrp17_k2hb 2/7, vrp19w 0/8, vrp20 0/1. vrp18 had no main-set games.
- **Secondary set (R0 < 2,450): 16 W / 6 L.** vrp20's 6 MELON wins in its first 43 games are all here: the 6-4 MELON record in the brief is against rivals rated below 2,450.


### MAIN rival R0 >= 2,450: 7 W / 35 L

| W | ep | our sub | rival | rival sub | R0 | d2 plate | PFS final | rival final | margin |
|---|---|---|---|---|---:|---|---:|---:|---:|
| W | 114672177 | 56634350 vrp15_k2fire | Gradient Grazing | 56620547 | 2489 | 8m/10w | 118,605 | 108,929 | +9,676 |
| W | 114713033 | 56634350 vrp15_k2fire | vvs | 56638736 | 2564 | 8m/10w | 102,538 | 96,329 | +6,209 |
| W | 114661796 | 56634350 vrp15_k2fire | goose10 | 56620389 | 2533 | 8m/12w | 72,172 | 66,592 | +5,580 |
| W | 114810325 | 56643352 vrp17_k2hb | fog flower | 56642047 | 2462 | 6m/14w | 127,171 | 123,152 | +4,019 |
| W | 114689938 | 56634350 vrp15_k2fire | thisray | 56629395 | 2563 | 8m/10w | 98,320 | 94,376 | +3,944 |
| W | 114726910 | 56634350 vrp15_k2fire | chungkuangwen | 56596923 | 2548 | 8m/12w | 98,616 | 94,772 | +3,844 |
| W | 114789440 | 56643352 vrp17_k2hb | loxigicck | 56637818 | 2519 | 8m/12w | 98,686 | 97,426 | +1,260 |
| L | 114695876 | 56634350 vrp15_k2fire | Sida Zuo | 56508421 | 2621 | 9m/8w | 80,602 | 80,741 | -139 |
| L | 114698801 | 56634350 vrp15_k2fire | Satoshi_SsSs | 56625604 | 2622 | 8m/12w | 106,047 | 106,279 | -232 |
| L | 114796752 | 56643352 vrp17_k2hb | pensukesan | 56628677 | 2615 | 8m/12w | 94,542 | 96,337 | -1,795 |
| L | 114877065 | 56649892 vrp19w_k2wide | Zhenghongshuang | 56646394 | 2506 | 6m/14w | 108,956 | 110,950 | -1,994 |
| L | 114798383 | 56643352 vrp17_k2hb | Planned Economy | 56640887 | 2522 | 8m/10w | 110,394 | 112,520 | -2,126 |
| L | 114675129 | 56634350 vrp15_k2fire | lingxiaojun | 56561450 | 2551 | 6m/12w | 101,106 | 103,544 | -2,438 |
| L | 114684168 | 56634350 vrp15_k2fire | istinetz | 56546676 | 2593 | 8m/10w | 69,666 | 72,437 | -2,771 |
| L | 114636771 | 56634350 vrp15_k2fire | ijiiok | 56587562 | 2523 | 10m/10w | 68,998 | 72,920 | -3,922 |
| L | 114903300 | 56649892 vrp19w_k2wide | goose10 | 56641668 | 2560 | 8m/12w | 112,271 | 117,043 | -4,772 |
| L | 114802773 | 56643352 vrp17_k2hb | leave you | 56639078 | 2504 | 6m/14w | 93,456 | 98,287 | -4,831 |
| L | 114676374 | 56634350 vrp15_k2fire | Capitaalgain | 56636454 | 2561 | 5m/13w | 118,797 | 124,718 | -5,921 |
| L | 114647096 | 56634350 vrp15_k2fire | yfy | 56610647 | 2516 | 6m/14w | 88,749 | 96,027 | -7,278 |
| L | 114655920 | 56634350 vrp15_k2fire | thisray | 56629395 | 2558 | 8m/10w | 84,145 | 93,090 | -8,945 |
| L | 114786464 | 56643352 vrp17_k2hb | farm pt | 56642049 | 2525 | 8m/10w | 93,478 | 102,832 | -9,354 |
| L | 114682642 | 56634350 vrp15_k2fire | monsaraida | 56636682 | 2483 | 8m/9w | 95,349 | 105,043 | -9,694 |
| L | 114891867 | 56649892 vrp19w_k2wide | Alexander Gremyakov | 56649649 | 2457 | 10m/10w | 150,855 | 160,651 | -9,796 |
| L | 114701777 | 56634350 vrp15_k2fire | istinetz | 56546676 | 2589 | 8m/10w | 97,847 | 108,099 | -10,252 |
| L | 114934555 | 56652418 vrp20_pfsoff | ijiiok | 56587562 | 2497 | 10m/10w | 72,483 | 82,740 | -10,257 |
| L | 114641203 | 56634350 vrp15_k2fire | yjshyfy | 56607718 | 2540 | 6m/14w | 98,518 | 108,900 | -10,382 |
| L | 114676576 | 56634350 vrp15_k2fire | madmax0404 | 56634716 | 2590 | 8m/10w | 100,678 | 111,551 | -10,873 |
| L | 114703239 | 56634350 vrp15_k2fire | Satoshi_SsSs | 56625604 | 2625 | 8m/12w | 76,067 | 87,206 | -11,139 |
| L | 114664852 | 56634350 vrp15_k2fire | ShunkiKyoya | 56634659 | 2672 | 8m/12w | 103,786 | 117,293 | -13,507 |
| L | 114878182 | 56649892 vrp19w_k2wide | leave you | 56639078 | 2531 | 6m/14w | 102,645 | 116,464 | -13,819 |
| L | 114921493 | 56649892 vrp19w_k2wide | Andrey Tikhomirov | 56591619 | 2549 | 10m/10w | 79,013 | 93,926 | -14,913 |
| L | 114667726 | 56634350 vrp15_k2fire | istinetz | 56546676 | 2582 | 8m/10w | 105,925 | 121,076 | -15,151 |
| L | 114686994 | 56634350 vrp15_k2fire | istinetz | 56618797 | 2562 | 8m/10w | 78,856 | 94,812 | -15,956 |
| L | 114639739 | 56634350 vrp15_k2fire | AI是我的豆包 | 56621727 | 2545 | 10m/8w | 84,030 | 100,627 | -16,597 |
| L | 114674700 | 56634350 vrp15_k2fire | keiz | 56637598 | 2567 | 8m/12w | 83,145 | 99,972 | -16,827 |
| L | 114645657 | 56634350 vrp15_k2fire | c0nrad | 56610436 | 2577 | 5m/15w | 97,866 | 115,301 | -17,435 |
| L | 114899625 | 56649892 vrp19w_k2wide | leave you | 56639078 | 2538 | 6m/14w | 107,836 | 125,741 | -17,905 |
| L | 114901197 | 56649892 vrp19w_k2wide | Fourth Quadrant | 56650756 | 2470 | 8m/10w | 58,616 | 77,262 | -18,646 |
| L | 114633798 | 56634350 vrp15_k2fire | Dipam Chakraborty | 56585035 | 2595 | 8m/10w | 132,215 | 151,447 | -19,232 |
| L | 114654661 | 56634350 vrp15_k2fire | AI是我的豆包 | 56621727 | 2554 | 10m/8w | 88,317 | 108,959 | -20,642 |
| L | 114808252 | 56643352 vrp17_k2hb | Planned Economy | 56645933 | 2527 | 8m/10w | 103,174 | 125,453 | -22,279 |
| L | 114890644 | 56649892 vrp19w_k2wide | Crop Dustas | 56642674 | 2586 | 8m/12w | 84,618 | 107,909 | -23,291 |

### SECONDARY rival R0 < 2,450: 16 W / 6 L

| W | ep | our sub | rival | rival sub | R0 | d2 plate | PFS final | rival final | margin |
|---|---|---|---|---|---:|---|---:|---:|---:|
| W | 114786057 | 56646827 vrp18_k2hb2046 | Thayaparan Kumarakuru | 56527739 | 934 | 6m/10w | 159,851 | 0 | +159,851 |
| W | 114599983 | 56634350 vrp15_k2fire | Accer_sz | 55173726 | 568 | 9m/2w | 186,349 | 90,968 | +95,381 |
| W | 114834348 | 56649892 vrp19w_k2wide | Giba | 55282264 | 687 | 7m/10w | 126,806 | 42,093 | +84,713 |
| W | 114838660 | 56649892 vrp19w_k2wide | Jaivardhan Raahi | 56006208 | 952 | 7m/7w | 135,293 | 66,888 | +68,405 |
| W | 114888460 | 56652418 vrp20_pfsoff | sansh0u0 | 56002897 | 615 | 10m/4w | 147,066 | 78,690 | +68,376 |
| W | 114890014 | 56652418 vrp20_pfsoff | Rosastella | 55275028 | 634 | 7m/0w | 109,480 | 54,240 | +55,240 |
| W | 114835786 | 56649892 vrp19w_k2wide | Robot Farm | 55871786 | 724 | 5m/15w | 86,646 | 42,024 | +44,622 |
| W | 114893155 | 56652418 vrp20_pfsoff | kelly waldeck | 55414343 | 822 | 5m/5w | 85,131 | 51,169 | +33,962 |
| W | 114900836 | 56652418 vrp20_pfsoff | Mohit Rao | 56213172 | 1248 | 9m/8w | 138,250 | 110,504 | +27,746 |
| W | 114809721 | 56646827 vrp18_k2hb2046 | macbook air m4 | 56640252 | 1900 | 9m/10w | 133,803 | 116,654 | +17,149 |
| W | 114837235 | 56649892 vrp19w_k2wide | stpete_ishii | 55882815 | 837 | 5m/5w | 109,639 | 93,437 | +16,202 |
| W | 114871344 | 56646827 vrp18_k2hb2046 | Sho Saga | 56535022 | 2346 | 10m/6w | 109,149 | 97,102 | +12,047 |
| W | 114848100 | 56646827 vrp18_k2hb2046 | IamDiganta.7 | 56620232 | 2188 | 9m/7w | 134,269 | 122,395 | +11,874 |
| W | 114865564 | 56649892 vrp19w_k2wide | Yoshiki_Nakamura | 56617431 | 2427 | 10m/7w | 110,426 | 99,673 | +10,753 |
| W | 114912034 | 56652418 vrp20_pfsoff | Hamed Vakili | 56652313 | 2129 | 8m/11w | 113,408 | 111,168 | +2,240 |
| W | 114926674 | 56652418 vrp20_pfsoff | Hello San Francisco | 56646152 | 2392 | 10m/10w | 125,675 | 124,635 | +1,040 |
| L | 114929695 | 56652418 vrp20_pfsoff | 123456789101112151617181920212 | 56637845 | 2417 | 8m/12w | 108,439 | 108,492 | -53 |
| L | 114931561 | 56649892 vrp19w_k2wide | xiy lin | 56639253 | 2446 | 8m/12w | 156,725 | 159,489 | -2,764 |
| L | 114937683 | 56652418 vrp20_pfsoff | Tergel Munkhbat | 56636017 | 2347 | 8m/11w | 126,713 | 131,333 | -4,620 |
| L | 114869601 | 56646827 vrp18_k2hb2046 | yjshyfy | 56645674 | 2392 | 6m/14w | 100,488 | 107,484 | -6,996 |
| L | 114805243 | 56643352 vrp17_k2hb | Ueddy | 56646169 | 2441 | 8m/11w | 83,243 | 99,662 | -16,419 |
| L | 114922257 | 56652418 vrp20_pfsoff | len8487 | 56640865 | 2407 | 8m/12w | 65,280 | 82,962 | -17,682 |

## 2. Wins against losses, side by side (main set: 7 W / 35 L)

Seat P = PFS, seat R = rival, M = P - R. Cash is the exact dawn-purse difference over each window, from census.measure purse_dXX. The full tables for the main, secondary and pooled sets are in S/winanatomy1/res/table_*.md.

| row (seat) | wins mean (n 7) | losses mean (n 35) | diff | t |
|---|---:|---:|---:|---:|
| M final | +4,933 | -10,718 | +15,651 | +10.43 |
| M cash d0-9 | +3,862 | +4,054 | -192 | -0.41 |
| **M cash d10-14** | -18,962 | -22,825 | +3,863 | **+2.97** |
| M cash d15-17 | +3,367 | +1,933 | +1,434 | +1.31 |
| **M cash d18-29** | +16,666 | +6,121 | +10,545 | **+4.61** |
| P final | 102,301 | 95,230 | +7,071 | +0.97 |
| R final (norm: loss mean 105.9k, median 106.3k) | 97,368 (median 96,329) | 105,947 | -8,579 | -1.19 |
| rival final < 101k | 5/7 | 14/35 | | |
| P cash d10-14 | 2,766 | 2,151 | +615 | +0.53 |
| **R cash d10-14** | 21,728 | 24,976 | -3,248 | **-2.41** |
| P cash d18-29 | 71,883 | 64,707 | +7,177 | +1.16 |
| R cash d18-29 | 55,218 | 58,586 | -3,368 | -0.55 |
| P melon tile-days d0-9 | 10.7 | 6.6 | +4.2 | +2.24 |
| P melon tile-days d10-14 | 42.9 | 37.4 | +5.4 | +1.48 |
| R melon tile-days d0-9 | 83.5 | 90.6 | -7.1 | -2.19 |
| R melon tile-days d10-14 | 17.4 | 26.7 | -9.3 | -1.87 |
| R melon tile-days d15-17 | 3.6 | 9.0 | -5.3 | -2.48 |
| R melon units sold d10-14 | 49.7 | 53.3 | -3.6 | -1.41 |
| R melon revenue d10-14 | 12,427 | 13,241 | -815 | -1.36 |
| R melon revenue d18-29 | 306 | 2,436 | -2,130 | -3.05 |
| P melon revenue d15-17 | 2,214 | 1,224 | +990 | +1.28 |
| R wool revenue d10-14 | 1,575 | 4,527 | -2,952 | -3.88 |
| P plant tile-days d0-9 | 235.1 | 223.4 | +11.7 | +2.35 |
| P spend d10-14 | 7,473 | 8,751 | -1,278 | -1.67 |
| **P d0-2 purchases** | 11 wheat + 8 carrot seeds, goose 1, cow 4, sheep 1, 7 hires | identical | 0 | n/a |
| R d0-2 melon seeds | 8.3 | 9.2 | -0.9 | -2.28 |
| R d0-2 hires / wheat seeds / cows / sheep | 13.4 / 13.0 / 2.7 / 3.0 | 13.3 / 12.4 / 2.5 / 2.9 | ~0 | < 1.5 |
| d0 market prices (all products), d10 melon price 272 | identical in all 42 | identical | 0 | n/a |
| shops d15-24 YARN_STORE (count) | 1.3 | 0.5 | +0.8 | +1.90 |
| d18-29 mean price WOOL | 150 | 86 | +65 | +1.59 |
| d18-29 mean price STRAWBERRY | 54 | 84 | -29 | -2.21 |
| M d18-29 price lift (units x (price - pooled-loss price)) | +7,430 | +3,731 | +3,698 | +1.46 |
| M d18-29 net of price lift | +9,236 | +2,390 | +6,847 | +3.51 |
| rival R0 | 2,526 | 2,555 | -29 | -1.76 |

About 150 rows were tested with only 7 wins, so a |t| near 2 on a single row is at noise level. The rows that carry the answer are the window margins (t 2.97 and t 4.61) and the zero rows: PFS's purchases, the d0 prices and PFS's d10-14 cash (t 0.53).

- **Secondary set (R0 < 2,450; 16 W / 6 L).** Here the wins are mostly the rival:
  - Rival final: 81.4k vs 114.9k (t -2.38).
  - Rival cash d10-14: -8.8k (t -3.13). Rival cash d15-17: -8.3k (t -2.89).
  - PFS final: +18.9k (t 1.29).
- **Pooled (23 W / 41 L).**
  - Margin by window: d10-14 +8.5k (t 4.01), d15-17 +5.8k (t 3.80), d18-29 +28.6k (t 4.77).
  - Rival final: -21.0k (t -2.88). Rival final below 101k: 16/23 in wins vs 16/41 in losses.
- **PFS Q2 day.** PFS bought Q2 on d6 in 7 games, all losses (0/7 wins). The d6 games carry the same margin as the other main-set losses (-10.5k vs -10.8k, S/winanatomy1/res/q2.txt), so Q2 day is a symptom, not a lever.

## 3. Each win classified (S/winanatomy1/res/perwin_main.md)

Swing = this win's margin minus the loss-mean margin (-10.7k), split into the PFS change and the rival change from their loss means. Z-scores use the SD of the 35 losses: PFS 18.0k, rival 18.8k.

| ep / rival | margin | swing = PFS - rival | class | named cause |
|---|---:|---|---|---|
| 114672177 Gradient Grazing | +9,676 | +20.4k = +23.4k (z +1.30) - (+3.0k) | **BOARD** | ICE_CREAM_SHOP at d15 lifted d18-29 MILK to 203 (norm 70). PFS milk +25.3k over norm, rival +17.4k. M price lift +10.5k. The margin was won in d18-29: +18.7k vs norm. |
| 114713033 vvs | +6,209 | +16.9k = +7.3k - (-9.6k) | **BOARD (rival also -10.0k vs its own median 106.4k)** | YARN_STORE at d9, d18, d21 and d24 lifted d18-29 WOOL to 233 (norm 86). PFS sold 187 wool units vs 97 in the norm: +34.0k, against the rival's +9.2k. M price lift +13.0k. |
| 114661796 goose10 | +5,580 | +16.3k = -23.1k (z -1.28) - (-39.4k, z -2.10) | **RIVAL WEAKER (bad day: -28.8k vs own median 95.4k)** | The rival bought Q4 on d10 and ran almost no second melon wave (6.7 tile-days vs 26.7 in d10-14). It sold 0 eggs d18-29 and its d15-29 cash was -36.6k vs norm. A poor board for both seats: PFS was -23k too. |
| 114810325 fog flower | +4,019 | +14.7k = +31.9k (z +1.78) - (+17.2k) | **BOARD** | YARN_STORE at d9 and d15 lifted WOOL to 228: PFS wool +31.1k, rival +24.4k, both seats rich. M price lift +12.4k. |
| 114689938 thisray | +3,944 | +14.7k = +3.1k - (-11.6k) | **BOARD** | TOMATO d18-29 averaged 164 (norm 74): PFS sold 182 units vs 34 in the norm, +28.5k. M price lift +11.5k. The same rival sub beat PFS in 114655920 with a 93.1k final, so 94.4k here is its own norm, not a bad day. |
| 114726910 chungkuangwen | +3,844 | +14.6k = +3.4k - (-11.2k) | **RIVAL WEAKER (version: at its own median 95.8k, day -1.0k)** | No second melon wave: 4.5 tile-days vs 26.7 in d10-14, and 8 melon seeds in d0-9 vs 12.2. Rival d10-14 cash -5.0k vs norm; the d10-14 margin was +8.4k vs norm. |
| 114789440 loxigicck | +1,260 | +12.0k = +3.5k - (-8.5k) | **RIVAL WEAKER (version: at its own median 96.9k, day +0.5k)** | Its own variant: 1,495 wheat units resold in d10-14 and Q4 on d13. Rival d10-14 cash -7.5k vs norm. The board was against PFS (M price lift -2.5k). |

**Counts: RIVAL WEAKER 3 (1 bad day, 2 weaker versions), BOARD 4, PFS DID SOMETHING 0.**

**Rival's own norm (S/winanatomy1/res/rivnorm.txt).** Each rival sub's median reward over its COMPLETED episodes against other teams, from 25 ListEpisodes calls with n 90-570 games per sub, compared with its final against PFS.

| | wins (n 7) | losses (n 26 covered) | t |
|---|---:|---:|---:|
| rival day (final minus own median), mean | -2,752 | -317 | -0.35 |
| rival day, median | -1,028 | -1,692 | |
| rival below own median | 4/7 | 14/26 | |
| rival own median | 100,120 | 103,371 | -1.79 |

Per win, the rival's day was: goose10 -28.8k, vvs -10.0k, thisray -5.7k, chungkuangwen -1.0k, loxigicck +0.5k, Gradient Grazing +4.0k, fog flower +21.8k.

In several losses the rival had a worse day than any win rival except goose10, and PFS still lost: istinetz 114684168 -29.0k, ijiiok 114636771 -28.8k, Sida Zuo 114695876 -22.6k. PFS fell as well in those games (finals 69.7k, 69.0k, 80.6k), so a bad board hits both seats. A rival's bad day is not enough; the wins need a lower-level rival version or a draw that pays PFS's herd.

In all four BOARD wins the M price lift is more than half the swing: +10.5k of 20.4k, +13.0k of 16.9k, +12.4k of 14.7k and +11.5k of 14.7k. Two of them also show a rival shortfall against the group norm: vvs -9.6k and thisray -11.6k, though thisray is at its own-sub norm. PFS's gain is priced into products it already holds at d18: sheep and cows (main-win means 6.4 and 6.1 tile-days per day) and tomatoes. Shops are revealed only as they unlock (town.unlocked_shops is empty at d0); the price-setting shops here unlocked between d9 and d24.

## 3b. The board condition that predicts a win: YARN_STORE count (S/winanatomy1/res/shopprice.txt, shopwin.txt)

- **Mechanism.** In the engine's SHOPS table, YARN_STORE is the only consumer of WOOL. Across all 64 games, the mean d18-29 wool price rises with the number of YARN_STOREs unlocked d9-d24:

  | YARN_STOREs unlocked d9-d24 | 0 | 1 | 2 | 3-4 |
  |---|---:|---:|---:|---:|
  | games (n) | 26 | 26 | 8 | 4 |
  | mean wool price d18-29 | 30 | 113 | 169 | 225 |

  Correlation r +0.77. Milk rises with ICE_CREAM_SHOP (57, 80, 101 at 0, 1, 2) and SMOOTHIE_SHOP (r +0.48). Tomato follows FARMERS_MARKET (r +0.41).
- **Main set.** Wins and mean margin by YARN_STOREs unlocked d9-d24:

  | YARN_STOREs | 0 | 1 | 2+ |
  |---|---:|---:|---:|
  | wins / games | 2/16 | 1/16 | 4/10 |
  | mean margin | -10.0k | -9.3k | -3.2k |

  Correlation of margin with the count: r +0.34, n 42. In the secondary set the count does not predict (r +0.04); there the wins are the rival.
- **PFS already follows the draw.** Across all 64 games, by YARN_STOREs unlocked d9-d24:

  | YARN_STOREs | 0 | 1 | 2+ |
  |---|---:|---:|---:|
  | PFS sheep tile-days d18-29 | 69 | 78 | 105 |
  | rival sheep tile-days d18-29 | 61 | 79 | 92 |
  | PFS coins per sheep-day | 43 | 148 | 257 |

  At 2+ YARN_STOREs, PFS out-earns the rival on wool: 27.1k vs 21.4k in d18-29.
- **Not predictable.** Shops are drawn with replacement and appear in town.unlocked_shops only when they unlock, every 3 days from d3. The draw cannot be known at d0.

## 4. Answer

1. **PFS does nothing different in its wins.**
   - Its d0-2 purchases are the same in all 42 main games (PFS identity).
   - Its d10-14 cash is equal: +0.6k, t 0.53.
   - It still loses d10-14 in its wins by -19.0k.
   - The one PFS row that moves is d0-9 melon: +4.2 tile-days (t 2.24) and +1.7 melon seeds. It is worth +1.0k in d15-17 melon sales (t 1.28). The main-set slope is +484 coins per melon tile-day (r 0.33, n 42), about +2k for the observed gap, set against a +15.7k swing.
   - That behaviour responds to the game state (PFS's planner is deterministic given the state). Making it deliberate is the d0-1 melon plate, MELONTRIAL1's vrp21_melon: offline own coins flat, rival +12-18k. Nothing new to switch.
2. **The wins are the rival's version (2/7), one clear rival bad day (goose10), or late-draw luck (4/7).** Measured against each rival's own median, the rival's day does not separate wins from losses (-2.8k vs -0.3k, t -0.35). Its level does: own median 100.1k vs 103.4k, t -1.79.
   - The margin is made in d18-29: +10.5k, t 4.61. About +3.7k of that (t 1.46) is the price lift on the products each seat sells. The rest is the rival selling less (strawberry price 54 vs 84, rival melon revenue d18-29 -2.1k) plus PFS's volume in the lifted products.
   - The rival's d10-14 is 3.2k weaker (t -2.41): a smaller plate (8.3 vs 9.2 d0-2 melon seeds) and a smaller second wave (d10-14 melon tile-days 17.4 vs 26.7).
3. **Can a board condition be made deliberate?** The predictor is the YARN_STORE draw: 2+ unlocked d9-d24 gives 4/10 main wins, 0-1 gives 3/32. It cannot be chosen, and PFS's planner already tilts sheep toward it: +36 sheep tile-days d18-29 at 2+. A deliberate version would push that price-reactive herd tilt harder. That is the herd-tilt family, closed by HERDTILT (two-sided tilt gifts -5,181) and HERDTILT2 (price hinge, pooled +23, t 0.5, NO). The coins in the BOARD wins came from PFS's existing tilt; there is no marginal coin estimate for a harder one. No switch is proposed.
4. **Consequence for the top-5 plan.** The wins do not contain a transferable PFS behaviour. Every win needs a weaker-level rival version, a rival bad day, or a late shop draw that favours PFS's herd. This confirms TOPMECH1, LOSSBODY1 and BEATPROG1: only a body that earns the d10-14 wave itself moves the margin.

Rule slips: none. Local work was one process at a time, nice 19 and ionice 3. There were 0 replay fetches, 25 ListEpisodes API calls 10 s apart with 0 HTTP 429 (S/winanatomy1/api), no remote runs, no GPU, and nothing read from or written to /dev.
