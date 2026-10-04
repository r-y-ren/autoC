# RIVALSUPPLY2 - rival-family supply in the price projection (2026-09-29, 18:55-21:55Z box)

**User idea (18:52Z):** "can we add rival supply to price projection? we almost know what he will try to sell (the highest priced
products) so we can adjust our production with this knowledge."

**Verdict: NONE (every arm NOISE, |pooled t| < 1).** The family-conditioned forecast works as built (right family on every game, projected
prices fall 20-60 % on milk / strawberry / wool), but the planner's production does not move: own standing crop tiles stay within
0.3 tile of OFF in every window. It shifts only a few sale units (milk/wool/fertilizer -3..-13, eggs +4..+12), and on the V56 side that
is a timing move, which cannot gain. The family arm at scale 1.0 pools to **-70 (t -0.17, 122 obs)**: V56 +367 (t 1.61, 61 games),
p48c -506 (t -0.66, 61 boards). The p48c v21 read carries a gift signature (rival +1,199 t 2.21, late animal units -7.3). Nothing packaged.

## 1. Build (branch rivalsupply2_0929 on 8d670dad = vrp20_pfsoff; worktree /mnt/e/_work/kagg3_wt_rivalsupply2)
- `plan.OPP_SUPPLY_FAMILY_ON` (default False), `OPP_SUPPLY_FAMILY_FORCE` ("" = live selection; "pop" = the old S_pop curve through the
  same path = the old switch), `OPP_SUPPLY_FAMILY_MEL_CASH` (BRAINSTORM5 whitelist P48-code 938|964|985|992|1020|1100 + PQ4-code
  2438|2464|2485|2492|2097), `OPP_SUPPLY_FAMILY_SPLIT_DAY` = 10, `OPP_SUPPLY_SCALE` (shared with the old switch).
- `projector._opp_switch`: with FAMILY_ON the curve path = `core/opp_supply/S_<family>.npy`. The per-game latch lives in the projector
  module (`set_opp_family`), and the tables are added to `projected_inv` / `inv_at_day` exactly as `opp_supply_to_turn` /
  `opp_supply_over_days` already do. With FAMILY_ON False, not one expression changes.
- `runtime.Runtime._opp_family` (every turn while ON):
  - step 0 -> pop.
  - Step 1 latches the rival code from its h1 cash: on the list = MEL, otherwise V56.
  - A MEL rival becomes PQ4 once it owns 4 quadrants (TOP1WATCH1: h1 cash no longer separates P48 from PQ4; the d10 Q4 buy does). Otherwise it is P48 from d10 and MEL (both pooled) before d10.
  - The plan is built at hour 0, so d0 is planned on S_pop and d1+ on the family curve.
- Env diag `RIVALSUPPLY2_DIAG=<file>` (inert on play: OFF + diag = 40/40 identical on V56 m40): one row per dawn with the family, rival cash,
  rival quadrants, market inventory, and own/rival standing crop tiles, plus one row per day with the wall time of every turn.

## 2. Curves (S/rivalsupply2/build_curves.py + finalize.py; res/curves.md, res/seats.jsonl)
- **Measurement:** EXECUTED net market-inventory units of the rival seat per step, from a pinned engine replay (S/econcensus/census.py, unchanged).
  - +1 per SELL unit at price > 1, -1 per BUY_PRODUCT unit.
  - Floor sales, and rows the engine clipped or refused, add nothing.
  - The old S_pop was the RECORDED tape row: an upper bound including the d29 dump.
- **Seats: 290 replays, 1,190 s.**
  - Live games vs PFS h0: S/livewatch23, 165 seats. The code comes from h1 cash; V = lw23 fam V not on the list, 90 newest.
  - TOPAUDIT3 programme seats from 09-28/29: 125.
  - MEL seats are split by the rival's own quadrant count at d12: 4 = PQ4, otherwise P48.
- **Seat counts per family:** P48 133 (lw23 60, ta3 73), PQ4 67 (lw23 15, ta3 52), MEL 200, V56 90.
- **Cross-check:** P48 melons are 49 d10-14 @229 + 18 d15-17, and strawberry d18-29 is 160 (TARGETS1: 48 @235 + 23, 155).

| family | window | WHE | CAR | TOM | STR | MEL | EGG | MLK | WOL | FRT |
|---|---|---|---|---|---|---|---|---|---|---|
| P48 (n 133) | d10-14 u | 67 | 3 | 0 | 8 | 49 | 35 | 44 | 16 | 59 |
| P48 (n 133) | d10-14 net | 22 | 3 | 0 | 8 | 49 | 35 | 44 | 16 | 58 |
| P48 (n 133) | d15-17 u | 34 | 7 | 0 | 46 | 18 | 34 | 26 | 19 | 28 |
| P48 (n 133) | d15-17 net | 29 | 7 | 0 | 46 | 18 | 34 | 25 | 18 | 28 |
| P48 (n 133) | d18-29 u | 323 | 143 | 47 | 160 | 3 | 148 | 106 | 87 | 93 |
| P48 (n 133) | d18-29 net | 291 | 143 | 47 | 155 | 3 | 148 | 102 | 76 | 80 |
| P48 (n 133) | d10-29 u | 424 | 152 | 47 | 213 | 71 | 218 | 175 | 122 | 180 |
| P48 (n 133) | d10-29 net | 342 | 152 | 47 | 209 | 71 | 218 | 171 | 111 | 166 |
| PQ4 (n 67) | d10-14 u | 123 | 6 | 0 | 9 | 57 | 30 | 38 | 19 | 61 |
| PQ4 (n 67) | d10-14 net | 20 | 6 | 0 | 9 | 57 | 30 | 38 | 19 | 61 |
| PQ4 (n 67) | d15-17 u | 96 | 17 | 1 | 45 | 8 | 43 | 25 | 20 | 26 |
| PQ4 (n 67) | d15-17 net | 57 | 17 | 1 | 45 | 8 | 43 | 25 | 20 | 26 |
| PQ4 (n 67) | d18-29 u | 559 | 163 | 108 | 177 | 5 | 170 | 102 | 84 | 82 |
| PQ4 (n 67) | d18-29 net | 402 | 163 | 108 | 175 | 5 | 170 | 100 | 79 | 71 |
| PQ4 (n 67) | d10-29 u | 777 | 185 | 109 | 231 | 71 | 242 | 165 | 123 | 169 |
| PQ4 (n 67) | d10-29 net | 479 | 185 | 109 | 229 | 71 | 242 | 163 | 118 | 158 |
| MEL (n 200) | d10-14 u | 86 | 4 | 0 | 8 | 52 | 33 | 42 | 17 | 60 |
| MEL (n 200) | d10-14 net | 21 | 4 | 0 | 8 | 52 | 33 | 42 | 17 | 59 |
| MEL (n 200) | d15-17 u | 55 | 10 | 1 | 46 | 15 | 37 | 26 | 19 | 27 |
| MEL (n 200) | d15-17 net | 38 | 10 | 1 | 46 | 15 | 37 | 25 | 19 | 27 |
| MEL (n 200) | d18-29 u | 402 | 149 | 67 | 166 | 4 | 156 | 104 | 86 | 89 |
| MEL (n 200) | d18-29 net | 328 | 149 | 67 | 162 | 4 | 156 | 101 | 77 | 77 |
| MEL (n 200) | d10-29 u | 542 | 163 | 68 | 219 | 71 | 226 | 172 | 122 | 176 |
| MEL (n 200) | d10-29 net | 388 | 163 | 68 | 216 | 71 | 226 | 168 | 113 | 163 |
| V56 (n 90) | d10-14 u | 319 | 2 | 0 | 0 | 72 | 5 | 40 | 22 | 72 |
| V56 (n 90) | d10-14 net | -24 | 2 | 0 | 0 | 72 | 5 | 39 | 22 | 59 |
| V56 (n 90) | d15-17 u | 233 | 2 | 0 | 38 | 0 | 17 | 30 | 29 | 39 |
| V56 (n 90) | d15-17 net | 18 | 2 | 0 | 38 | 0 | 17 | 27 | 24 | 32 |
| V56 (n 90) | d18-29 u | 876 | 114 | 24 | 202 | 3 | 62 | 125 | 102 | 165 |
| V56 (n 90) | d18-29 net | 253 | 114 | 24 | 171 | 2 | 62 | 115 | 82 | 94 |
| V56 (n 90) | d10-29 u | 1429 | 119 | 25 | 240 | 75 | 84 | 194 | 153 | 276 |
| V56 (n 90) | d10-29 net | 247 | 119 | 25 | 209 | 75 | 84 | 182 | 128 | 185 |
| old S_pop (recorded) | d0-9 net | -50 | 0 | 0 | 0 | 0 | 0 | 10 | 24 | 58 |
| old S_pop (recorded) | d10-14 net | -20 | 0 | 0 | 1 | 63 | 1 | 41 | 20 | 60 |
| old S_pop (recorded) | d15-17 net | 13 | 2 | 0 | 40 | 2 | 2 | 42 | 28 | 35 |
| old S_pop (recorded) | d18-29 net | 346 | 113 | 49 | 334 | 83 | 57 | 258 | 189 | 242 |
| old S_pop (recorded) | d10-29 net | 339 | 115 | 49 | 375 | 149 | 60 | 341 | 238 | 337 |

`u` = units sold per game, `net` = the curve (sold at price > 1 minus bought). V56 is the only family that dumps wheat (1,429 sold d10-29,
net 247) and it floods strawberry late (171 net d18-29). P48/PQ4 flood eggs (218/242) and carrots. PQ4's tomato is 108-109 vs P48 47.

## 3. Identity
- **OFF vs V56** (vr.py, m40 seat 0, 4 boards): 4/4 exact = S/vband1/res/v56_ctl_m40 rows (97,037/93,046, 125,669/122,307, 99,069/78,209, 85,653/82,259).
- **OFF + env diag** (V56 m40, 40 games): 40/40 identical.
- **p48c control** = S/judgerival1/res/p48c/pfs.csv. It is the same rival cfg (REFRESH3 P48 clone, params sha d993498e) and equals REVFIX2's OFF tree 4/4.
  - The v21 control is REVFIX2's rf2_off_v21_p48 (42 rows, same sha; copied to S/rivalsupply2/ctl/).
  - NOTE: S/judgerival2/res/jr2_pfs_fl.csv is an OLDER rival cfg. Pairing the p48c tag against it shows a spurious -17,120 margin (rival 77k vs 88k).

## 4. Diag (S/rivalsupply2/diag.py on res/*_diag.tsv)
- **Family chosen:**
  - V56 judge: V56 on 400/400 d10-29 dawns (V56 h1 cash 2901).
  - p48c judge: MEL d1-9, then P48 on every dawn d10-29. The clone never buys Q4, h1 cash 938.
  - d0 dawn: pop.
- **Projected price change**, next 3 days of the chosen curve at every d10-29 dawn inventory (mean %):
  - V56 x1.0: MLK -48, STR -39, WOL -28, FRT -15, WHE -5, CAR -4, MEL -2, EGG -2, TOM -1.
  - P48 x1.0 (v21): MLK -58, WOL -31, STR -22, FRT -10, WHE -7, CAR -5, EGG -4.
  - The old pop curve x1.0: MLK -62, STR -49, WOL -34, FRT -29, MEL -17.
- **What the planner changed vs OFF** (V56 m40 fam10):
  - Own standing crop tiles d2-9 / d10-14 / d15-17 / d18-29 all within 0.3 tile. For example STR 27.9|27.9 at d15-17, WHE 20.7|20.6 at d18-29. **The crop ask does not move.**
  - Sale mix moves a few units: milk -4, wool -3, fertilizer -4, eggs +4, wheat +4. Prices of the held products are +2..+5 c/u.
  - Same direction on p48c. On p48c v21: eggs +12, wool -13, fertilizer -10, milk -6.
  - Our strawberry wall moves -0.4..+2.5 u (V56 d15-17 +1.4 m40 / +2.5 v21; p48c d10-17 -0.4 / 0.0).
- **Timing** (remote wall s, under load 4-11; all inside the bars):
  - Turn p99 0.17-0.37 s (bar 0.65 s).
  - Dawn p99 0.27-0.59 s vs OFF-diag dawn p99 0.588 s.

```
rs2v_offd wall per turn p99 0.318 s max 0.724; dawn p99 0.588 s mean 0.271
rs2_smoke wall per turn p99 0.169 s max 0.383; dawn p99 0.272 s mean 0.154
rs2v_fam05 wall per turn p99 0.226 s max 0.430; dawn p99 0.347 s mean 0.186
rs2v_pop10 wall per turn p99 0.232 s max 0.409; dawn p99 0.342 s mean 0.192
rs2v_pop05 wall per turn p99 0.237 s max 0.441; dawn p99 0.350 s mean 0.197
rs2v_fam10_v21 wall per turn p99 0.373 s max 0.788; dawn p99 0.590 s mean 0.334
rs2p_fam10 wall per turn p99 0.236 s max 0.411; dawn p99 0.350 s mean 0.184
rs2p_fam05 wall per turn p99 0.240 s max 0.488; dawn p99 0.345 s mean 0.196
rs2p_pop10 wall per turn p99 0.352 s max 1.906; dawn p99 0.580 s mean 0.307
rs2p_pop05 wall per turn p99 0.295 s max 2.311; dawn p99 0.449 s mean 0.259
rs2p_fam10_v21 wall per turn p99 0.272 s max 0.596; dawn p99 0.369 s mean 0.239
```

## 5. Grid (paired vs PFS controls; V56 = vr.py seat 0 vs ahmedberatozer v56; p48c = rcr.py both seats, 80 rows)
Arms: fam = live family curve; pop = FORCE pop, the old switch re-read on today's judge. 05/10 = OPP_SUPPLY_SCALE 0.5/1.0.
*p48c has no step-360 ledger, so its strawberry column is d10-17.

| read | n | d ours (t) | d rival (t) | d margin (t) | W ctl->arm | flips | our STR d15-17* arm/ctl | our late animal d18-29 arm/ctl |
|---|---|---|---|---|---|---|---|---|
| V56_m40_fam10 | 40 | +664 (2.44) | +216 (1.03) | **+449 (1.39)** | 38->37 | +0/-1 | 49.9/48.5 (d15-17) | 270.8/271.6 |
| V56_m40_fam05 | 40 | +81 (0.52) | +63 (0.43) | **+19 (0.11)** | 38->38 | +0/-0 | 48.6/48.5 (d15-17) | 271.4/271.6 |
| V56_m40_pop10 | 40 | +566 (2.02) | +280 (1.26) | **+286 (0.87)** | 38->38 | +0/-0 | 49.8/48.5 (d15-17) | 272.1/271.6 |
| V56_m40_pop05 | 40 | +54 (0.34) | -53 (-0.44) | **+107 (0.56)** | 38->37 | +0/-1 | 48.5/48.5 (d15-17) | 271.6/271.6 |
| V56_v21_fam10 | 21 | +386 (1.23) | +174 (0.64) | **+212 (0.83)** | 13->15 | +2/-0 | 53.4/50.9 (d15-17) | 260.0/259.4 |
| p48c_m40_fam10 | 80 | +365 (0.68) | +174 (0.31) | **+191 (0.25)** | 78->77 | +0/-1 | 53.2/53.6 (d10-17) | 275.7/277.4 |
| p48c_m40_fam05 | 80 | +123 (0.28) | +88 (0.19) | **+35 (0.06)** | 78->77 | +0/-1 | 53.8/53.6 (d10-17) | 275.9/277.4 |
| p48c_m40_pop10 | 80 | +390 (0.76) | +1,028 (2.07) | **-638 (-1.00)** | 78->76 | +0/-2 | 54.9/53.6 (d10-17) | 274.5/277.4 |
| p48c_m40_pop05 | 80 | +1,290 (2.19) | +712 (1.21) | **+578 (0.78)** | 78->76 | +0/-2 | 53.9/53.6 (d10-17) | 276.3/277.4 |
| p48c_v21_fam10 | 42 | -636 (-0.91) | +1,199 (2.21) | **-1,835 (-1.73)** | 41->42 | +1/-0 | 57.1/57.1 (d10-17) | 270.7/278.0 |

Per product d10-29, units / c/u, arm | PFS control (per game):

| read | who | WHE | CAR | TOM | STR | MEL | EGG | MLK | WOL | FRT |
|---|---|---|---|---|---|---|---|---|---|---|
| V56_m40_fam10 | ours | 350/35 \| 346/35 | 131/53 \| 129/53 | 34/107 \| 32/109 | 217/123 \| 217/123 | 88/159 \| 88/159 | 105/51 \| 101/51 | 155/112 \| 159/110 | 145/154 \| 148/149 | 160/40 \| 164/39 |
| V56_m40_fam10 | rival | 567/37 \| 569/38 | 128/48 \| 127/49 | 9/123 \| 9/127 | 248/87 \| 248/88 | 72/242 \| 72/242 | 75/49 \| 75/49 | 186/104 \| 187/101 | 162/139 \| 162/139 | 274/40 \| 274/39 |
| V56_m40_fam05 | ours | 348/35 \| 346/35 | 129/53 \| 129/53 | 33/108 \| 32/109 | 217/123 \| 217/123 | 88/159 \| 88/159 | 101/51 \| 101/51 | 160/110 \| 159/110 | 147/151 \| 148/149 | 163/40 \| 164/39 |
| V56_m40_fam05 | rival | 567/37 \| 569/38 | 128/49 \| 127/49 | 9/126 \| 9/127 | 248/88 \| 248/88 | 72/242 \| 72/242 | 75/49 \| 75/49 | 186/101 \| 187/101 | 162/139 \| 162/139 | 274/39 \| 274/39 |
| V56_m40_pop10 | ours | 349/35 \| 346/35 | 129/53 \| 129/53 | 34/107 \| 32/109 | 216/124 \| 217/123 | 88/159 \| 88/159 | 106/51 \| 101/51 | 156/111 \| 159/110 | 145/153 \| 148/149 | 161/40 \| 164/39 |
| V56_m40_pop10 | rival | 566/37 \| 569/38 | 128/48 \| 127/49 | 9/123 \| 9/127 | 248/87 \| 248/88 | 72/242 \| 72/242 | 75/49 \| 75/49 | 186/104 \| 187/101 | 162/138 \| 162/139 | 274/40 \| 274/39 |
| V56_m40_pop05 | ours | 348/35 \| 346/35 | 130/53 \| 129/53 | 32/109 \| 32/109 | 217/123 \| 217/123 | 88/159 \| 88/159 | 102/51 \| 101/51 | 160/109 \| 159/110 | 146/152 \| 148/149 | 163/40 \| 164/39 |
| V56_m40_pop05 | rival | 569/37 \| 569/38 | 127/48 \| 127/49 | 9/128 \| 9/127 | 248/88 \| 248/88 | 72/242 \| 72/242 | 75/49 \| 75/49 | 186/101 \| 187/101 | 162/138 \| 162/139 | 274/39 \| 274/39 |
| V56_v21_fam10 | ours | 350/35 \| 346/35 | 133/50 \| 129/51 | 21/118 \| 20/119 | 247/136 \| 248/135 | 87/159 \| 87/159 | 122/50 \| 122/50 | 155/95 \| 156/93 | 114/129 \| 117/125 | 138/44 \| 142/43 |
| V56_v21_fam10 | rival | 298/37 \| 299/37 | 125/47 \| 124/48 | 7/173 \| 7/170 | 248/105 \| 248/106 | 72/242 \| 72/242 | 91/49 \| 91/49 | 199/94 \| 198/92 | 134/122 \| 133/122 | 269/43 \| 270/43 |
| p48c_m40_fam10 | ours | 323/37 \| 323/37 | 135/55 \| 135/56 | 32/118 \| 32/120 | 219/159 \| 217/158 | 98/181 \| 97/180 | 110/48 \| 104/48 | 158/107 \| 160/107 | 142/158 \| 148/153 | 151/40 \| 158/40 |
| p48c_m40_fam10 | rival | 302/38 \| 299/38 | 34/56 \| 33/56 | 2/100 \| 1/116 | 96/171 \| 97/172 | 53/247 \| 53/247 | 133/48 \| 136/48 | 178/110 \| 179/109 | 125/157 \| 122/157 | 184/45 \| 183/44 |
| p48c_m40_fam05 | ours | 319/37 \| 323/37 | 133/55 \| 135/56 | 32/121 \| 32/120 | 217/158 \| 217/158 | 97/181 \| 97/180 | 108/47 \| 104/48 | 157/110 \| 160/107 | 147/155 \| 148/153 | 160/40 \| 158/40 |
| p48c_m40_fam05 | rival | 295/38 \| 299/38 | 35/57 \| 33/56 | 1/78 \| 1/116 | 96/171 \| 97/172 | 54/247 \| 53/247 | 135/47 \| 136/48 | 178/112 \| 179/109 | 124/155 \| 122/157 | 180/44 \| 183/44 |
| p48c_m40_pop10 | ours | 326/37 \| 323/37 | 136/55 \| 135/56 | 32/118 \| 32/120 | 221/158 \| 217/158 | 98/181 \| 97/180 | 109/47 \| 104/48 | 158/111 \| 160/107 | 141/154 \| 148/153 | 147/40 \| 158/40 |
| p48c_m40_pop10 | rival | 290/38 \| 299/38 | 37/56 \| 33/56 | 1/80 \| 1/116 | 96/173 \| 97/172 | 53/247 \| 53/247 | 146/47 \| 136/48 | 176/113 \| 179/109 | 126/155 \| 122/157 | 190/45 \| 183/44 |
| p48c_m40_pop05 | ours | 322/37 \| 323/37 | 135/55 \| 135/56 | 33/117 \| 32/120 | 219/160 \| 217/158 | 98/180 \| 97/180 | 110/47 \| 104/48 | 157/112 \| 160/107 | 143/157 \| 148/153 | 154/40 \| 158/40 |
| p48c_m40_pop05 | rival | 292/38 \| 299/38 | 37/56 \| 33/56 | 1/81 \| 1/116 | 98/171 \| 97/172 | 53/247 \| 53/247 | 145/47 \| 136/48 | 173/114 \| 179/109 | 125/155 \| 122/157 | 185/44 \| 183/44 |
| p48c_v21_fam10 | ours | 316/36 \| 315/37 | 132/53 \| 131/54 | 20/131 \| 18/135 | 250/174 \| 248/175 | 96/188 \| 96/187 | 137/46 \| 125/47 | 154/100 \| 160/99 | 112/153 \| 125/144 | 137/45 \| 147/44 |
| p48c_v21_fam10 | rival | 344/37 \| 319/38 | 41/53 \| 30/54 | 1/135 \| 3/75 | 116/181 \| 118/182 | 49/250 \| 50/249 | 139/46 \| 150/46 | 199/102 \| 190/102 | 86/151 \| 86/148 | 162/49 \| 163/48 |

Pooled (S/rivalsupply2/pool.py; the two p48c seats of a board are averaged into one observation; 59/41 = newest band V vs rest):
```
fam10: pooled -70 (t -0.17, n 122) | V56 +367 (t 1.61, n 61) | p48c -506 (t -0.66, n 61 boards) | 59/41 weighted +9
fam05: pooled +27 (t 0.07, n 80)   | V56 +19 (t 0.11)          | p48c +35 (t 0.04)                  | +25
pop10: pooled -176 (t -0.42, n 80) | V56 +286 (t 0.87)         | p48c -638 (t -0.82)                | -93
pop05: pooled +343 (t 0.71, n 80)  | V56 +107 (t 0.56)         | p48c +578 (t 0.60)                 | +300
```
Bars:
- No arm reaches pooled t >= 2.
- fam10 fails gift-free on p48c v21 (rival +1,199, t 2.21) and has late animal units below control there (-7.3).
- pop10 carries the old handed-back signature on p48c (rival +1,028, t 2.07).
- The old switch's 09-05 loss (-2,972 t -3.8) does NOT reproduce on today's planner (V56 +286, p48c -638). The curve's effect is now small in both forms.

## 6. Why it cannot work in this form, and the one next step
- The projection enters PFS in the lot allocator, the hold/press quotes, the BUY row and the seed/animal horizon.
  - PFS production (tiles, herd, hires) is fixed by the theta genes, plate floors and capacity, not by these quotes.
  - A 40 % lower projected milk price therefore changes WHEN milk is sold (a few units), not how much we produce.
- Vs V56 our margin is volume, and timing moves alone gain nothing (BRAINSTORM4 / VCHECK2 invariant). The grid reproduces that.
- To use the rival forecast for production, the forecast has to be an input of the ASK itself: the plant mix and herd targets per product, d10-29.
  - For example, a family-conditioned mix table read at the d1/d10 dawns (what to plant into the P48 egg flood or the V56 strawberry wave), judged closed-loop.
  - The projector path is closed.

Files: S/rivalsupply2/ (build_curves.py, finalize.py, apply_patch.py, chain.sh, vchain.sh, an.py, pool.py, diag.py, res/, ctl/, checkpoint.txt).
Remote rows: ~/stage_reactclone1/S/rivalsupply2/res + S/reactclone1/res/rs2p_*.
