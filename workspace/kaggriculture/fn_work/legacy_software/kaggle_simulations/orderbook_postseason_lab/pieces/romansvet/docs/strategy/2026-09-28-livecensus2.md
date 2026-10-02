# LIVECENSUS2 (2026-09-28, 08:41Z-08:55Z): live rival-h1-cash census over vrp10/vrp12/vrp15 games (evidence only, no upload)

Stream dir: `S/livecensus2/`. No src change, no dist change, no upload. The final decision belongs to the user: a further upload would retire vrp12_pfs 56612145 (FIFO), which is the anchor of the final pair.

## Verdict
- **(a) Live fire share.** v3's whitelist (26|29|2338|2438) matches **52/300 = 17.3 %** of all fetched live games: vrp10 28/157 = 17.8 %, vrp12 21/137 = 15.3 %, vrp15 3/6. The tape estimate was ~9 %. On vrp15 the gate fired on exactly the listed games (3 observed = 3 listed, all at h1 29, **W 3-0**: +24.6k, +20.4k, +64.0k, all against low-rated rivals).
- **(b) The unfired body on whitelisted values: 8-41.** vrp10_esw went 1-27 and vrp12_pfs 7-14 (in the table below, vrp12 plus the unfired vrp15 games). By value: 26 0-8, 29 1-4, 2338 2-7, 2438 5-22; 47/49 of these rivals are MELON. The judge's faithful base win rate on these values was 16/66 = 24 %, so live leaves more to flip than the judge assumed. At the judge's faithful net-flips-per-seat rates, the 49 live games give **+10.2 (GATETABLE2) to +13.4 (JUDGEALL1 mh4v2) net flips = +3.4..+4.5 per 100 games**. The brief projected +1.9..+2.5/100. The gap comes from live frequency: 2438 alone is 9.1 % of games against 5.2 % in the tape weights.
- **(c) Top 3 unlisted values by live losses.** **2854** (n 40, W-L 33-7, V35) and **2867** (n 24, 18-6, V23) had no rows, so this stream ran 20 paired BAND seats with V56 forced on. **V56 lost badly: 17 -> 4 wins, flips +1/-14 = -13 (faithful 12 -> 2, -10/13)**. REJECT. The third is **938** (n 10, 4-6, MELON): GATETABLE2 shows 111 seats / +51 on all seats but only 4 faithful seats / +0, and JUDGEALL1 shows 5 faithful / +0, so there is no faithful support. Next come 2464 (n 6, 0-6; GATETABLE2 faithful 8 / +0, JUDGEALL1 faithful 5 / +1, conflicting) and 118 (n 5, 1-4, V; 0 faithful seats).
- **(d) v3b.** Only **117** (THUNDER THUNDER #100, live 0-4; faithful 2 seats / +2) and **2046** (Dipam Chakraborty #68, live 0-3; faithful 2 / +1) have BOTH live losses AND positive faithful judge rows. v3b = v3 + 117|2046 fires on 18.9 % of games. Expected **+5.3 (GATETABLE2) .. +6.4 (JUDGEALL1) /100**, which is **+1.85/100 over v3**. That gain rests on 2 faithful seats per value and one team per value; the band rows overlap between the two sources, so the evidence is not independent. It is below any ship bar. Adding 2464 adds 0 to +0.4/100.
- **(e) Risks.** Each value is an exact-cash fingerprint of one or two teams, and a resubmission moves the value (Dipam already shows 988/1020/2046). vrp10's h0 is 3 HIRE, not PFS's 4 HIRE, but rival h1 cash matched on all 27 rival subs seen under both. The vrp15 live read so far is 6 games (3 fired). Firing on the V family (2854/2867) is strongly negative, so no widening toward >2,550 values. Any v3b would need a new package and upload, which retires vrp12_pfs. **That decision is the user's.**

## Table A: live rival h1 cash, unfired body (vrp10_esw + vrp12_pfs + unfired vrp15), n 297, W-L 167-130
Marks: "candidate" = at least 3 live losses and not whitelisted; "check" = whitelisted with live losses. GT2 = GATETABLE2 res/seats_real.tsv (band276/faith59/toprival1/topv56_1/pool/self). JA = JUDGEALL1 runs/mh4v2 (v2 arm vs base, JC1 faithful). The two share the band276 seats.

| h1 cash | n | W-L | loss share | vrp10 W-L | vrp12(+15u) W-L | fam | teams (top 3, LB rank) | whitelisted | GT2 evidence n/net (faithful) | JA mh4v2 n/net (faithful) | mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2438 | 27 | 5-22 | 16.9 % | 1-15 | 4-7 | MELON26 V1 | high frequency far#79 x4; Matt Motoki#78 x4; Navier-stokes#80 x3 | YES | 67/+3 (f 30/+5) | 41/+11 (f 26/+5) | check |
| 26 | 8 | 0-8 | 6.2 % | 0-7 | 0-1 | MELON8 | boominginging#109 x3; kuengo#110 x3; huaiyuyoung#83 x1 | YES | 13/+6 (f 6/+3) | 12/+5 (f 6/+3) | check |
| 2854 | 40 | 33-7 | 5.4 % | 22-4 | 11-3 | V35 MELON5 | leave you#116 x4; Haalandspring#221 x3; ZHOU HONGYI#175 x3 | no | - | - | candidate |
| 2338 | 9 | 2-7 | 5.4 % | 0-2 | 2-5 | MELON9 | Yannik Schiffner#182 x2; Christoffer Thimse#62 x2; Alejandro Ayestara#190 x2 | YES | 27/+2 (f 22/+1) | 5/+2 (f 3/+1) | check |
| 2867 | 24 | 18-6 | 4.6 % | 10-4 | 8-2 | V23 MELON1 | sAIzeria Harness#128 x3; automatylicza#188 x2; Knight of Favonius#155 x2 | no | - | - | candidate |
| 938 | 10 | 4-6 | 4.6 % | 3-3 | 1-3 | MELON10 | redblackbst#95 x2; Hamed Vakili#106 x2; Aguacates#82 x2 | no | 111/+51 (f 4/+0) | 7/+0 (f 5/+0) | candidate |
| 2464 | 6 | 0-6 | 4.6 % | 0-1 | 0-5 | MELON6 | RS Turley#113 x3; kwa#117 x2; Hello San Francisc#121 x1 | no | 23/-2 (f 8/+0) | 8/+4 (f 5/+1) | candidate |
| 118 | 5 | 1-4 | 3.1 % | 0-2 | 1-2 | V5 | ActiveMusyoku#86 x5 | no | 4/+3 (f 0/+0) | 1/+1 (f 0/+0) | candidate |
| 29 | 5 | 1-4 | 3.1 % | 0-3 | 1-1 | MELON4 V1 | ready or not here #96 x4; janson#3134 x1 | YES | 8/+2 (f 8/+2) | 8/+2 (f 8/+2) | check |
| 117 | 4 | 0-4 | 3.1 % | 0-1 | 0-3 | MELON4 | THUNDER THUNDER#100 x4 | no | 4/+2 (f 2/+2) | 2/+1 (f 1/+1) | candidate |
| 2630 | 8 | 5-3 | 2.3 % | 2-2 | 3-1 | V8 | Planned Economy#60 x2; Michael Timbs#144 x2; YK#3203 x1 | no | - | - | candidate |
| 34 | 3 | 0-3 | 2.3 % | 0-1 | 0-2 | MELON3 | Fritz Cremer#123 x3 | no | 1/+0 (f 1/+0) | 1/+1 (f 0/+0) | candidate |
| 2600 | 3 | 0-3 | 2.3 % | 0-1 | 0-2 | MELON3 | pensukesan#374 x3 | no | - | - | candidate |
| 2046 | 3 | 0-3 | 2.3 % | 0-1 | 0-2 | MELON3 | Dipam Chakraborty#68 x3 | no | 3/+2 (f 2/+1) | 3/+2 (f 2/+1) | candidate |
| 488 | 17 | 15-2 | 1.5 % | 7-0 | 8-2 | ZERO17 | quantara.cv#145 x4; Joseph Adamski#115 x3; Lakshmanan R#119 x3 | no | 17/-12 (f 10/-8) | - |  |
| 2911 | 10 | 8-2 | 1.5 % | 8-2 | 0-0 | V10 | 3정훈#92 x2; miya#181 x2; yvn kaggriculture#167 x2 | no | - | - |  |
| 3037 | 7 | 5-2 | 1.5 % | 5-2 | 0-0 | V7 | offhand#108 x5; shiiin9#884 x1; A. R. SEKKAT#248 x1 | no | - | - |  |
| 12 | 3 | 1-2 | 1.5 % | 0-2 | 1-0 | MELON3 | Ebi#93 x3 | no | 1/+0 (f 0/+0) | - |  |
| 2485 | 2 | 0-2 | 1.5 % | 0-1 | 0-1 | MELON2 | feles99#63 x1; ra5anchor#1062 x1 | no | 2/+0 (f 1/+0) | 2/+0 (f 1/+0) |  |
| 553 | 2 | 0-2 | 1.5 % | 0-1 | 0-1 | MELON2 | Farmer#101 x2 | no | 2/+1 (f 2/+1) | 2/+1 (f 2/+1) |  |
| 20 | 2 | 0-2 | 1.5 % | 0-0 | 0-2 | MELON2 | lingxiaojun#99 x1; Pico#41 x1 | no | 2/+1 (f 2/+1) | 2/+1 (f 2/+1) |  |
| 2901 | 11 | 10-1 | 0.8 % | 2-0 | 8-1 | V11 | curiosity#177 x2; linmumu009#1196 x1; Matin Urdu#157 x1 | no | - | - |  |
| 2875 | 5 | 4-1 | 0.8 % | 0-1 | 4-0 | V5 | senkin13#250 x3; NayuNayu#304 x1; in blue#189 x1 | no | - | - |  |
| 3 | 4 | 3-1 | 0.8 % | 3-1 | 0-0 | MELON3 ZERO1 | fuxi#105 x1; Tejas#2622 x1; Nkosi Ndwandwe#4329 x1 | no | 1/+1 (f 0/+0) | - |  |
| 2864 | 4 | 3-1 | 0.8 % | 1-0 | 2-1 | V4 | Ghost Rule#139 x2; kyy666#235 x1; Subramanya N#137 x1 | no | - | - |  |
| 2974 | 3 | 2-1 | 0.8 % | 1-0 | 1-1 | V3 | Driz Lo#104 x3 | no | - | - |  |
| 8 | 2 | 1-1 | 0.8 % | 0-1 | 1-0 | MELON2 | by#46 x2 | no | 4/+0 (f 2/-1) | 2/+0 (f 0/+0) |  |
| 4 | 2 | 1-1 | 0.8 % | 1-1 | 0-0 | MELON2 | 吃白饭的大肥鱼#33 x1; Zhanghao Chen69#6061 x1 | no | 4/-3 (f 1/+0) | 1/+0 (f 1/+0) |  |
| 661 | 2 | 1-1 | 0.8 % | 0-1 | 1-0 | MELON2 | chungkuangwen#132 x2 | no | 3/-1 (f 0/+0) | 3/-1 (f 0/+0) |  |
| 964 | 2 | 1-1 | 0.8 % | 0-0 | 1-1 | MELON2 | juliencst#158 x1; Shangshang Zhang#161 x1 | no | 3/+3 (f 0/+0) | - |  |
| 1 | 2 | 1-1 | 0.8 % | 0-0 | 1-1 | MELON2 | istinetz#114 x1; Capitaalgain#143 x1 | no | 2/+1 (f 0/+0) | 2/+1 (f 0/+0) |  |
| 257 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | ZERO1 | Scott Willis#786 x1 | no | - | - |  |
| 33 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | MELON1 | Andrey Tikhomirov#156 x1 | no | - | - |  |
| 5 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | MELON1 | shane18#130 x1 | no | - | - |  |
| 160 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | MELON1 | by#46 x1 | no | 2/+2 (f 0/+0) | 1/+1 (f 0/+0) |  |
| 2492 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | MELON1 | Siyuan Wang#107 x1 | no | 2/+0 (f 2/+0) | 1/+0 (f 1/+0) |  |
| 3056 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | V1 | forever young#47 x1 | no | - | - |  |
| 6 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | MELON1 | Otter Vibe#39 x1 | no | 1/+1 (f 0/+0) | - |  |
| 2415 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | V1 | keiz#40 x1 | no | 2/+0 (f 1/+0) | 2/+0 (f 1/+0) |  |
| 2015 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | V1 | keiz#40 x1 | no | 1/+0 (f 1/+0) | 1/+0 (f 1/+0) |  |
| 2878 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | V1 | Gatswei#162 x1 | no | - | - |  |
| 163 | 1 | 0-1 | 0.8 % | 0-1 | 0-0 | MELON1 | tine.sh agent#111 x1 | no | 1/+1 (f 0/+0) | 1/+1 (f 0/+0) |  |
| 131 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | MELON1 | fshindo#70 x1 | no | - | - |  |
| 1020 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | MELON1 | len8487#66 x1 | no | 2/+0 (f 2/+0) | 1/+0 (f 1/+0) |  |
| 113 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | MELON1 | Tergel Munkhbat#102 x1 | no | 1/+0 (f 1/+0) | - |  |
| 184 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | MELON1 | We wanna be tomato#29 x1 | no | 1/+0 (f 0/+0) | - |  |
| 1464 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | MELON1 | elmo#31 x1 | no | 1/+0 (f 0/+0) | - |  |
| 2859 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | V1 | Erfan Eshratifar#153 x1 | no | - | - |  |
| 2322 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | MELON1 | feel the agi#54 x1 | no | 1/+1 (f 1/+1) | 1/+1 (f 1/+1) |  |
| 39 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | ZERO1 | Ebi#93 x1 | no | 1/+1 (f 0/+0) | 1/+1 (f 0/+0) |  |
| 2885 | 1 | 0-1 | 0.8 % | 0-0 | 0-1 | MELON1 | HayatoFujihara#75 x1 | no | - | - |  |
| 3000 | 5 | 5-0 | 0.0 % | 0-0 | 5-0 | V5 | american gothic#133 x3; aowhite#3869 x1; Musliadi#3894 x1 | no | - | - |  |
| 2828 | 4 | 4-0 | 0.0 % | 3-0 | 1-0 | V4 | fasith 007#151 x4 | no | - | - |  |
| 2906 | 4 | 4-0 | 0.0 % | 4-0 | 0-0 | V4 | chocolat#178 x4 | no | - | - |  |
| 2620 | 3 | 3-0 | 0.0 % | 1-0 | 2-0 | V3 | yomogii#146 x3 | no | - | - |  |

(rows with 0 losses and n < 3 omitted: 19 values, 26 games, all wins)

## Table B: judge evidence for the candidates (V56 kernel vs PFS on the same seat, keyed on real-h0 h1 cash)

| h1 | live n | live L | GT2 seats n / net (faithful) | JUDGEALL1 mh4v2 n / net (faithful) | LIVECENSUS2 new sim | faithful rate/seat (GT2, JA, new) | exp. flips on live games (GT2 / JA) | read |
|---|---|---|---|---|---|---|---|---|
| 26 | 8 | 8 | 13 / +6 (faith 6 / +3; W 3->9) | 12 / +5 (faith 6 / +3; W 3->8) | - | +0.50, +0.50, - | +4.0 / +4.0 | whitelisted |
| 29 | 5 | 4 | 8 / +2 (faith 8 / +2; W 4->6) | 8 / +2 (faith 8 / +2; W 4->6) | - | +0.25, +0.25, - | +1.2 / +1.2 | whitelisted |
| 2338 | 9 | 7 | 27 / +2 (faith 22 / +1; W 4->6) | 5 / +2 (faith 3 / +1; W 0->2) | - | +0.05, +0.33, - | +0.4 / +3.0 | whitelisted |
| 2438 | 27 | 22 | 67 / +3 (faith 30 / +5; W 31->34) | 41 / +11 (faith 26 / +5; W 11->22) | - | +0.17, +0.19, - | +4.5 / +5.2 | whitelisted |
| 2854 | 40 | 7 | - | - | 10 / -7 (faith 6 / -5; W 9->2) | -, -, -0.83 | -33.3 (new) | REJECT: V56 loses |
| 2867 | 24 | 6 | - | - | 10 / -6 (faith 7 / -5; W 8->2) | -, -, -0.71 | -17.1 (new) | REJECT: V56 loses |
| 938 | 10 | 6 | 111 / +51 (faith 4 / +0; W 47->98) | 7 / +0 (faith 5 / +0; W 2->2) | - | +0.00, +0.00, - | +0.0 / +0.0 | no faithful support |
| 2464 | 6 | 6 | 23 / -2 (faith 8 / +0; W 11->9) | 8 / +4 (faith 5 / +1; W 1->5) | - | +0.00, +0.20, - | +0.0 / +1.2 | conflicting / negative |
| 118 | 5 | 4 | 4 / +3 (faith 0 / +0; W 1->4) | 1 / +1 (faith 0 / +0; W 0->1) | - | -, -, - | - / - | no faithful support |
| 117 | 4 | 4 | 4 / +2 (faith 2 / +2; W 0->2) | 2 / +1 (faith 1 / +1; W 0->1) | - | +1.00, +1.00, - | +4.0 / +4.0 | both-positive (thin) |
| 2630 | 8 | 3 | - | - | - | -, -, - | - / - | no faithful support |
| 34 | 3 | 3 | 1 / +0 (faith 1 / +0; W 0->0) | 1 / +1 (faith 0 / +0; W 0->1) | - | +0.00, -, - | +0.0 / - | no faithful support |
| 2600 | 3 | 3 | - | - | - | -, -, - | - / - | no faithful support |
| 2046 | 3 | 3 | 3 / +2 (faith 2 / +1; W 0->2) | 3 / +2 (faith 2 / +1; W 0->2) | - | +0.50, +0.50, - | +1.5 / +1.5 | both-positive (thin) |

- v3 = 26|29|2338|2438: fires on 49/297 = 16.5 % of live games; expected net flips (faithful per-seat rate x live count): GT +3.42/100 (+10.2 on 297); JA +4.53/100 (+13.4 on 297)
- v3b = v3 + 117|2046: fires on 56/297 = 18.9 % of live games; expected net flips (faithful per-seat rate x live count): GT +5.27/100 (+15.7 on 297); JA +6.38/100 (+18.9 on 297)
- v3b + 2464: fires on 62/297 = 20.9 % of live games; expected net flips (faithful per-seat rate x live count): GT +5.27/100 (+15.7 on 297); JA +6.78/100 (+20.1 on 297)
- v3 + 2854|2867: fires on 113/297 = 38.0 % of live games; expected net flips (faithful per-seat rate x live count): GT -13.57/100 (-40.3 on 297); JA -12.47/100 (-37.0 on 297)

New sim (this stream, step 3; 2854 and 2867 each had at least 5 live losses and zero existing rows): 20 BAND seats (10 per value, faithful-first random pick, seed = value). Tree /mnt/e/_work/kagg3_wt_v3branch1/src (kernel2v3 63f74064). Switch `KERNEL2_ON=True,KERNEL2_NOOP_H0=False,KERNEL2_INHERIT=True,KERNEL2_FIRE_CASH=2854|2867`, run through S/judgeall1/ja_leg.py band -w 3. Paired against the banked PFS base (ja_lib.base_rows band = pfs_band2) with the JC1 faithful flag. Every row logged opp_money_h1 at the target value.

```
h1 2854 all: n 10 W PFS->V56 9->2 flips +1/-8 = -7, mean dmargin -5,014, dours -8,842, dtheirs -3,828
h1 2854 faithful: n 6 W PFS->V56 6->1 flips +0/-5 = -5, mean dmargin -9,902, dours -8,893, dtheirs +1,009
h1 2867 all: n 10 W PFS->V56 8->2 flips +0/-6 = -6, mean dmargin -5,940, dours -8,357, dtheirs -2,417
h1 2867 faithful: n 7 W PFS->V56 6->1 flips +0/-5 = -5, mean dmargin -7,085, dours -5,375, dtheirs +1,711
h1 both all: n 20 W PFS->V56 17->4 flips +1/-14 = -13, mean dmargin -5,477, dours -8,600, dtheirs -3,123
h1 both faithful: n 13 W PFS->V56 12->2 flips +0/-10 = -10, mean dmargin -8,386, dours -6,998, dtheirs +1,387
```

## Commands / files
- `python3 S/livecensus2/census.py`: ListEpisodes for 56600971/56612145/56634350 (api/eps_<sub>.json). It fetched only the 6 missing replays (into gz/) and reused the livewatch19/21/22 replay caches. It parses with S/livewatch22/lw22.py `one()` and writes games.tsv (300 games, 0 unparsed, 0 non-completed).
- `python3 S/livecensus2/evidence.py`: evidence.tsv, net flips per (source, h1) from runs/mh4v2 and seats_real.tsv.
- `python3 S/livecensus2/analyze.py`: census.tsv (one row per game: sub, ep, rival, LB rank from S/toprival1/api/lb.json 05:43Z, h1, W/L, margin, whitelisted, fired, rival d2 family), tableA.md, summary.txt, candidates.json.
- `bash S/livecensus2/run_sim.sh` then `python3 S/livecensus2/pair_sim.py`: res/v56x_band.csv and res/v56x_pair.txt.
- `python3 S/livecensus2/tableB.py`: tableB.md.
