# JUDGEFAITH1 (2026-09-29, 20:47Z-): which offline judge predicts a REAL P48 / PQ4 seat when our late volume falls?

Audit, data only: no judge games, no remote, one local worker at nice 19. Stream dir `S/judgefaith1/` (checkpoint.txt; led.py, judge.py,
jshops.py, om.py, strength.py, charge.py, charge2.py, decomp.py, melon.py, phase.py, transfer.py, hetero.py; res/ + logs/).

**Data.**
- **Live:** exact engine ledgers (S/melonloss1/led.py imported unchanged: census.measure + the led30 snapshot wrapper), both seats, on every PFS-h0 game
  (lw23 h0pfs=1, subs 56634350 / 56643352 / 56646827 / 56649892 / 56652418 vrp20 / 56676381 vrp21) vs a programme-CODE rival (h1 cash in
  RIVALSUPPLY2's P48C {938,964,985,992,1020,1100} | PQ4C {2438,2464,2485,2492,2097}):
  - 88 games: 33 MELONLOSS1 ledgers reused, 55 new, 0 cash/stock mismatches.
  - Family by the rival's Q4 day (<= d11 -> PQ4, the RIVALSUPPLY2 rule): **P48 71, PQ4 17**. vrp20 (pure PFS) alone: 25 + 12.
  - Robustness set: OTHERMELON1's 86 in-band off-code seats with P48 behaviour. The adapter om.py is exact: 0 mismatches on 13 fields x 47 overlapping games.
- **Judge:** the t3 env books of the PFS control rows vs p48c (b5 screen40 x 2 seats, 80 g; JUDGERIVAL1 tape boards, 80 g), pq4c (pf1 screen40 s0, 40 g;
  JUDGERIVAL1, 80 g) and big (b5 screen40 s0, 40 g), plus PROGFIRE1's b9r arm rows. All index-aligned with 0 unaligned.
  - Each judge board's town is the recorded replay's shop draw. `sim.eod.unlock_shop` reads fixed rng words of the seed; the csv seed equals the replay seed on 240/240 boards.
- Windows: d0-9 / d10-14 / d15-29 (steps 0-240-360-end). Units = sold units. Unpaired medians and means are marked as such.

## Verdict (<= 12 lines)
1. No judge is faithful as it stands. PFS wins 96-100 % vs every clone, but live it wins 27 % vs the real P48 (n 71; vrp20 28 %) and 29 % vs PQ4 (n 17).
2. The infidelity is d15-29: revenue R-O is -42..-48k in the judges vs -7k live. The d10-14 melon wave is reproduced within 10 % in coins.
3. For fired reads, trust p48c's CHARGE mechanism. It is a price externality: the rival's milk stays 155 -> 155 u at +38 c/u, and the clone's milk/wool volumes match live (106 % / 103 %).
4. Apply a price-level correction to it: rival gain x0.70 (milk), x0.87 (wool), x1.4 (strawberry, where the real P48 sells 2x the units); our late losses x0.7-0.9.
5. Do not trust big on d15-29. Its rival cuts its own milk/wool sales when prices rise (-1.8k / -3.2k), which cancels the charge; nothing live shows that.
6. No live regression can measure the charge. On the clone the demand-controlled slope reads +11 where the paired causal value is -176.
7. The live signature equals the clone's (milk +12 vs +11, wool +55 vs +56, strawberry +49 vs +93), so live shows no smaller charge.
8. PROGFIRE1 b9r on REAL P48 seats: -3.5k +- 2.8k (range -5.4..-1.7k; -4.1k with the other-MELON seats), vs the clone's -9.4k. The clone's own live-like price tercile reads -5.0k (t -2.1).
9. The 2 faithful P48-code tapes read -2.0k. PQ4 seats: +5.4k +- 2.0k (n 17). Mix-weighted per fired game: -1.8k +- 2.3k, NOT a win, so the fired programme line is dead on real seats too.
10. The real P48 wins on its d10-14 wave (+15.9k) plus a neutral late game (-0.9k). When it loses, d15-29 swings -27.9k on PRICE (town demand and its herd), not on our units.
11. REFRESH4 bar vs PFS on live boards: PFS W 27 % (17-40 %), rival final ~105k, d15-29 R-O ~ -7k, strawberry 211 / tomato 51 / carrot 148 u (P48).
12. For PQ4 the bar adds wheat 1,458 u; for both, melon d10-14 51-58 u at 228-244 c/u and a paired charge that stays a price effect (details §5).

## 1. Strength: the clones vs the real family (PFS in both)

Judge = PFS control rows (closed-loop, reacting clone). LIVE = exact engine ledgers of PFS-h0 subs vs programme-CODE rival seats (h1 cash in P48C|PQ4C), family by the rival's Q4 day (<= d11 -> PQ4, RIVALSUPPLY2 rule). Units = sold units per game (rival seat). Unpaired medians / means (different boards).

| set | n | PFS W % | margin median | rival final median | our final median | rival d10-29 u WHE / CAR / TOM / STR / MEL / EGG / MLK / WOL / FRT | rival melon d10-14 u / coins | rival d10-29 revenue |
|---|---|---|---|---|---|---|---|---|
| judge p48c (screen40 x2, PROGFIRE1 ctl) | 80 | 99 | +32,200 | 89,708 | 124,694 | 326 / 29 / 3 / 101 / 52 / 133 / 190 / 123 / 177 | 42 / 10,516 | 102,214 |
| judge p48c (JUDGERIVAL1 tape boards) | 80 | 98 | +29,026 | 86,254 | 119,544 | 299 / 33 / 1 / 97 / 53 / 136 / 179 / 122 / 183 | n/a (no d14 book) | 96,467 |
| judge pq4c (screen40 s0, PROGFIRE1 ctl) | 40 | 98 | +30,589 | 90,118 | 123,302 | 321 / 62 / 8 / 111 / 56 / 113 / 176 / 123 / 173 | 53 / 13,171 | 106,653 |
| judge pq4c (JUDGERIVAL1 tape boards) | 80 | 96 | +27,404 | 89,258 | 117,816 | 297 / 89 / 4 / 103 / 58 / 116 / 157 / 138 / 170 | n/a (no d14 book) | 101,755 |
| judge big (screen40 s0, PROGFIRE1 ctl) | 40 | 100 | +45,872 | 73,655 | 120,242 | 302 / 60 / 55 / 182 / 58 / 91 / 154 / 112 / 104 | 47 / 11,867 | 106,569 |
| LIVE real P48 vs PFS-h0 subs (all) | 71 | 27 | -8,106 | 105,150 | 100,692 | 415 / 148 / 51 / 211 / 70 / 179 / 179 / 119 / 175 | 51 / 11,620 | 119,256 |
| LIVE real P48 vs vrp20 (pure PFS) | 25 | 28 | -7,620 | 107,523 | 100,692 | 389 / 152 / 46 / 217 / 75 / 195 / 195 / 103 / 185 | 51 / 12,810 | 120,407 |
| LIVE real PQ4 vs PFS-h0 subs (all) | 17 | 29 | -6,104 | 104,523 | 97,397 | 1458 / 199 / 104 / 236 / 62 / 204 / 175 / 109 / 164 | 58 / 14,257 | 162,660 |
| LIVE real PQ4 vs vrp20 (pure PFS) | 12 | 25 | -7,642 | 106,115 | 96,444 | 1763 / 196 / 90 / 244 / 63 / 217 / 180 / 106 / 172 | 59 / 14,542 | 174,828 |
| LIVE all programme-code seats | 88 | 27 | -7,986 | 105,096 | 100,310 | 617 / 158 / 61 / 216 / 69 / 184 / 178 / 117 / 173 | 52 / 12,129 | 127,641 |
| LIVE other-MELON seats, P48 behaviour (OTHERMELON1 in-band, off-code) | 86 | 14 | -8,316 | 106,336 | 100,386 | 1113 / 133 / 55 / 195 / 79 / 143 / 180 / 152 / 256 | 53 / 12,734 | 151,047 |
| LIVE real P48 coded + other-MELON | 157 | 20 | -8,215 | 105,321 | 100,692 | 797 / 140 / 53 / 202 / 75 / 159 / 179 / 137 / 219 | 52 / 12,230 | 136,670 |
| RIVALSUPPLY2 real P48 curve (all opponents, n 133) | | | | | | 424 / 152 / 47 / 213 / 71 / 218 / 175 / 122 / 180 | 49 / - | - |
| RIVALSUPPLY2 real PQ4 curve (all opponents, n 67) | | | | | | 777 / 185 / 109 / 231 / 71 / 242 / 165 / 123 / 169 | 57 / - | - |

### Clone output as % of the real family (vs PFS live; RIVALSUPPLY2 all-opponent curve in brackets)

| clone vs family | melon d10-14 u | melon d10-14 coins | tomato d10-29 u | milk d10-29 u | wool d10-29 u | strawberry d10-29 u | wheat d10-29 u | egg d10-29 u | d10-29 revenue | final coins |
|---|---|---|---|---|---|---|---|---|---|---|
| p48c (screen40 x2, PROGFIRE1 ctl) vs real P48 | 82 % (85 %) | 90 % | 6 % (6 %) | 106 % (109 %) | 103 % (101 %) | 48 % (48 %) | 78 % (77 %) | 74 % (61 %) | 86 % | 85 % |
| p48c (JUDGERIVAL1 tape boards) vs real P48 | n/a (no d15 book) | n/a | 2 % (2 %) | 100 % (102 %) | 102 % (100 %) | 46 % (46 %) | 72 % (71 %) | 76 % (63 %) | 81 % | 82 % |
| pq4c (screen40 s0, PROGFIRE1 ctl) vs real PQ4 | 90 % (93 %) | 92 % | 8 % (8 %) | 100 % (106 %) | 113 % (100 %) | 47 % (48 %) | 22 % (41 %) | 55 % (47 %) | 66 % | 86 % |
| pq4c (JUDGERIVAL1 tape boards) vs real PQ4 | n/a (no d15 book) | n/a | 3 % (3 %) | 89 % (95 %) | 126 % (112 %) | 44 % (45 %) | 20 % (38 %) | 57 % (48 %) | 63 % | 85 % |
| big (screen40 s0, PROGFIRE1 ctl) vs real PQ4 | 81 % (83 %) | 83 % | 53 % (50 %) | 88 % (93 %) | 102 % (91 %) | 77 % (79 %) | 21 % (39 %) | 45 % (38 %) | 66 % | 70 % |
| big (screen40 s0, PROGFIRE1 ctl) vs real P48 | 93 % (97 %) | 102 % | 108 % (117 %) | 86 % (88 %) | 94 % (92 %) | 87 % (86 %) | 73 % (71 %) | 51 % (42 %) | 89 % | 70 % |

**Where each clone under-produces, vs the real family against the same PFS:**
- **p48c vs real P48:**
  - melon d10-14: 42 vs 51 u (82 %), 10.5k vs 11.6k coins (90 %; the clone sells fewer units at a higher price, 252 vs 228 c/u)
  - tomato: 3 vs 51 u (6 %)
  - carrot: 29 vs 148 (20 %)
  - strawberry: 101 vs 211 (48 %)
  - wheat: 326 vs 415 (78 %)
  - egg: 133 vs 179 (74 %)
  - milk 190 vs 179 (106 %) and wool 123 vs 119 (103 %) are right.
- **pq4c vs real PQ4:**
  - melon: 90 % of the units, 92 % of the coins
  - tomato: 8 %
  - wheat: 321 vs 1,458 (22 %)
  - strawberry: 47 %
  - egg: 55 %
  - milk 100 % and wool 113 %
- **big vs real PQ4:**
  - melon: 81 % of the units, 83 % of the coins
  - tomato: 53 %
  - strawberry: 77 %
  - wheat: 21 %
  - egg: 45 %
  - milk 88 %, wool 102 %
  - final coins: 70 %

## 2. The charge

Per-game rows: `S/judgefaith1/res/charge_games.tsv` (live = exact ledgers, both seats; judge = t3 env books). Slopes are coins per unit, +- 1 SE, with r and n. A NEGATIVE slope = the rival earns more when we sell less (the charge). Natural variation (across boards) is confounded by town demand (a rich town raises both our units and its coins); the demand-controlled column adds the consumer-shop counts of P unlocked by d18 and d24 (MELONLOSS1 DEM map). The judge rows have no shop book, so the like-for-like comparison is the simple slope, and the clone's own paired arm shows how far the simple slope sits from the causal one.

### (a) Natural-variation slopes, live vs judge (same method)

| set | MLK simple | WOL simple | STR simple | MEL simple | MLK + demand | WOL + demand | STR + demand |
|---|---|---|---|---|---|---|---|
| LIVE all programme-code seats | +143 +- 17 (r +0.68, n 88) | +178 +- 11 (r +0.87, n 88) | +199 +- 21 (r +0.72, n 88) | +30 +- 8 (r +0.38, n 88) | +12 +- 18 (R2 0.74, n 88) | +55 +- 18 (R2 0.86, n 88) | +49 +- 18 (R2 0.81, n 88) |
| LIVE real P48 | +142 +- 20 (r +0.66, n 71) | +180 +- 12 (r +0.87, n 71) | +192 +- 23 (r +0.70, n 71) | +39 +- 7 (r +0.53, n 71) | +17 +- 21 (R2 0.71, n 71) | +47 +- 21 (R2 0.87, n 71) | +57 +- 20 (R2 0.80, n 71) |
| LIVE real PQ4 | +162 +- 31 (r +0.80, n 17) | +162 +- 24 (r +0.87, n 17) | +227 +- 46 (r +0.78, n 17) | +14 +- 23 (r +0.15, n 17) | -30 +- 30 (R2 0.93, n 17) | +51 +- 29 (R2 0.91, n 17) | -26 +- 47 (R2 0.91, n 17) |
| LIVE vrp20 only (pure PFS) | +132 +- 21 (r +0.73, n 37) | +194 +- 13 (r +0.93, n 37) | +182 +- 25 (r +0.78, n 37) | -0 +- 38 (r -0.00, n 37) | +16 +- 23 (R2 0.80, n 37) | +104 +- 27 (R2 0.92, n 37) | +49 +- 27 (R2 0.85, n 37) |
| judge p48c ctl (80) | +201 +- 21 (r +0.73, n 80) | +116 +- 11 (r +0.77, n 80) | +118 +- 7 (r +0.88, n 80) | -20 +- 12 (r -0.19, n 80) | - | - | - |
| judge pq4c ctl (40) | +217 +- 31 (r +0.76, n 40) | +115 +- 17 (r +0.73, n 40) | +157 +- 12 (r +0.91, n 40) | +4 +- 14 (r +0.05, n 40) | - | - | - |
| judge big ctl (40) | +153 +- 18 (r +0.82, n 40) | +110 +- 14 (r +0.78, n 40) | +141 +- 15 (r +0.84, n 40) | +25 +- 24 (r +0.17, n 40) | - | - | - |
| judge p48c ARM b9r (80) | +498 +- 56 (r +0.71, n 80) | +178 +- 20 (r +0.72, n 80) | +141 +- 10 (r +0.85, n 80) | -7 +- 6 (r -0.14, n 80) | - | - | - |

### (a2) Aggregate crowding: rival d15-29 revenue (all 9 products) on OUR d15-29 revenue (coins per coin)

| set | simple | + demand (shops unlocked by d18) |
|---|---|---|
| LIVE all programme-code seats | +0.55 +- 0.17 (r +0.33, n 88) | +0.55 +- 0.17 (R2 0.11, n 88) |
| LIVE real P48 | +0.35 +- 0.11 (r +0.37, n 71) | +0.35 +- 0.11 (R2 0.14, n 71) |
| LIVE real PQ4 | +1.18 +- 0.62 (r +0.44, n 17) | +1.18 +- 0.64 (R2 0.19, n 17) |
| judge p48c ctl | +0.69 +- 0.06 (r +0.80, n 80) | - |
| judge pq4c ctl | +0.68 +- 0.07 (r +0.83, n 40) | - |
| judge big ctl | +0.45 +- 0.06 (r +0.76, n 40) | - |

### (b) The clone's PAIRED causal charge (PROGFIRE1 arm b9r - PFS control, same board and seat)

| rival | n | d our MLK u | d our WOL u | d our STR u | d our MEL u | d rival MLK coins | d rival WOL coins | d rival STR coins | d rival MEL coins | implied MLK coins/u | implied WOL coins/u | implied STR coins/u | d our late rev | d rival late rev | coins per coin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p48c | 80 | -33.7 | -42.6 | -20.3 | -22.9 | +5,942 | +2,618 | +2,045 | -1,480 | -176 | -62 | -101 | -13,652 | +10,077 | -0.74 |
| big | 40 | -31.4 | -34.6 | -10.6 | -23.6 | +3,733 | -167 | +2,513 | -1,197 | -119 | +5 | -236 | -6,699 | +3,360 | -0.50 |
| pq4c | 40 | -31.4 | -40.6 | +3.3 | -25.2 | +4,295 | +2,604 | +715 | -313 | -137 | -64 | +215 | -8,644 | +8,142 | -0.94 |

### (c) Demand-controlled slopes on live AND judge (judge towns from the recorded replays, seeds 240/240 equal)

Model M2: rival d15-29 coins of P ~ our d15-29 units of P + consumer shops of P by d18 + by d24. Model M3 (price channel): rival d15-29 price of P ~ our units of P + rival units of P + the two demand counts. Coefficient on OUR units, +- 1 SE, R2, n. Judge rows averaged per board.

| set | MLK M2 coins/u | WOL M2 coins/u | STR M2 coins/u | MLK M3 rival c/u per our unit | WOL M3 rival c/u per our unit | STR M3 rival c/u per our unit |
|---|---|---|---|---|---|---|
| LIVE all programme-code seats (88 g) | +12 +- 18 (R2 0.74, n 88) | +55 +- 18 (R2 0.86, n 88) | +49 +- 18 (R2 0.81, n 88) | +0.12 +- 0.10 (R2 0.77, n 87) | -0.05 +- 0.12 (R2 0.79, n 86) | +0.24 +- 0.07 (R2 0.76, n 87) |
| LIVE real P48 (71 g) | +17 +- 21 (R2 0.71, n 71) | +47 +- 21 (R2 0.87, n 71) | +57 +- 20 (R2 0.80, n 71) | +0.17 +- 0.12 (R2 0.75, n 70) | +0.05 +- 0.13 (R2 0.80, n 70) | +0.28 +- 0.08 (R2 0.74, n 70) |
| LIVE vrp20 only (37 g) | +16 +- 23 (R2 0.80, n 37) | +104 +- 27 (R2 0.92, n 37) | +49 +- 27 (R2 0.85, n 37) | +0.05 +- 0.16 (R2 0.77, n 37) | -0.03 +- 0.23 (R2 0.82, n 36) | +0.12 +- 0.11 (R2 0.85, n 37) |
| judge p48c ctl (40 boards) | +11 +- 32 (R2 0.82, n 40) | +56 +- 20 (R2 0.73, n 40) | +93 +- 19 (R2 0.79, n 40) | -0.23 +- 0.16 (R2 0.87, n 40) | -0.27 +- 0.13 (R2 0.82, n 40) | -0.02 +- 0.09 (R2 0.89, n 40) |
| judge pq4c ctl (40 boards) | +15 +- 26 (R2 0.88, n 40) | +48 +- 21 (R2 0.70, n 40) | +93 +- 16 (R2 0.90, n 40) | -0.16 +- 0.11 (R2 0.91, n 40) | -0.44 +- 0.14 (R2 0.83, n 40) | +0.25 +- 0.12 (R2 0.84, n 40) |
| judge big ctl (40 boards) | +54 +- 20 (R2 0.84, n 40) | +56 +- 15 (R2 0.79, n 40) | +54 +- 13 (R2 0.91, n 40) | -0.16 +- 0.11 (R2 0.93, n 40) | -0.12 +- 0.11 (R2 0.82, n 40) | +0.29 +- 0.07 (R2 0.92, n 40) |
| judge p48c ARM b9r (40 boards) | +16 +- 79 (R2 0.84, n 40) | +72 +- 40 (R2 0.65, n 40) | +92 +- 23 (R2 0.77, n 40) | +0.11 +- 0.25 (R2 0.91, n 40) | -0.38 +- 0.16 (R2 0.83, n 40) | +0.07 +- 0.08 (R2 0.87, n 40) |
| **clone CAUSAL (paired b9r - ctl, p48c)** | -176 | -62 | -101 | -1.12 (+38 c/u for -33.7 u) | -0.47 (+20 for -42.6) | -0.59 (+12 for -20.3) |
| **clone CAUSAL (paired, pq4c)** | -137 | -64 | (our STR +3) | -1.08 (+34 for -31.4) | -0.74 (+30 for -40.6) | - |
| **clone CAUSAL (paired, big)** | -119 | +5 | -236 | -1.46 (+46 for -31.4) | -0.92 (+32 for -34.6) | -1.51 (+16 for -10.6) |

### (d) Decomposition of the clone paired charge (d15-29, arm - ctl): PRICE effect on the rival's control volume vs VOLUME reaction

| rival | product | rival u ctl -> arm | rival c/u ctl -> arm | d rival coins | = price effect | + volume reaction | our u ctl -> arm | our c/u ctl -> arm |
|---|---|---|---|---|---|---|---|---|
| p48c (n 80) | MILK | 155 -> 155 | 116 -> 154 | +5,942 | +5,863 | +79 | 141 -> 107 | 115 -> 150 |
| p48c (n 80) | WOOL | 103 -> 106 | 135 -> 155 | +2,618 | +2,044 | +574 | 131 -> 89 | 141 -> 155 |
| p48c (n 80) | STRAWBERRY | 101 -> 106 | 182 -> 194 | +2,045 | +1,191 | +854 | 229 -> 209 | 176 -> 186 |
| p48c (n 80) | WHEAT | 304 -> 336 | 38 -> 39 | +1,541 | +261 | +1,280 | 305 -> 270 | 37 -> 38 |
| p48c (n 80) | EGG | 112 -> 99 | 47 -> 46 | -747 | -170 | -577 | 88 -> 161 | 48 -> 46 |
| p48c (n 80) | MELON | 10 -> 5 | 232 -> 170 | -1,480 | -619 | -861 | 90 -> 67 | 183 -> 133 |
| p48c (n 80) | TOMATO | 3 -> 5 | 208 -> 169 | +234 | -109 | +344 | 36 -> 29 | 190 -> 190 |
| big (n 40) | MILK | 122 -> 111 | 132 -> 178 | +3,733 | +5,557 | -1,825 | 142 -> 111 | 144 -> 174 |
| big (n 40) | WOOL | 93 -> 75 | 147 -> 179 | -167 | +3,033 | -3,200 | 145 -> 110 | 147 -> 178 |
| big (n 40) | STRAWBERRY | 179 -> 176 | 131 -> 147 | +2,513 | +2,884 | -371 | 212 -> 201 | 151 -> 163 |
| big (n 40) | WHEAT | 274 -> 271 | 39 -> 40 | +272 | +394 | -122 | 336 -> 289 | 38 -> 40 |
| big (n 40) | EGG | 78 -> 60 | 48 -> 46 | -1,045 | -177 | -869 | 94 -> 213 | 49 -> 46 |
| big (n 40) | MELON | 10 -> 7 | 228 -> 160 | -1,197 | -697 | -500 | 84 -> 61 | 184 -> 126 |
| big (n 40) | TOMATO | 55 -> 56 | 85 -> 83 | -32 | -150 | +118 | 42 -> 32 | 119 -> 123 |
| pq4c (n 40) | MILK | 147 -> 143 | 137 -> 171 | +4,295 | +5,022 | -727 | 142 -> 110 | 134 -> 160 |
| pq4c (n 40) | WOOL | 103 -> 101 | 133 -> 163 | +2,604 | +3,061 | -457 | 137 -> 97 | 141 -> 171 |
| pq4c (n 40) | STRAWBERRY | 108 -> 107 | 181 -> 189 | +715 | +885 | -170 | 218 -> 221 | 172 -> 180 |
| pq4c (n 40) | WHEAT | 291 -> 334 | 38 -> 38 | +1,519 | -125 | +1,644 | 323 -> 273 | 37 -> 36 |
| pq4c (n 40) | EGG | 100 -> 81 | 48 -> 45 | -1,180 | -307 | -874 | 95 -> 222 | 48 -> 46 |
| pq4c (n 40) | MELON | 3 -> 3 | 225 -> 140 | -313 | -271 | -42 | 91 -> 66 | 183 -> 115 |
| pq4c (n 40) | TOMATO | 8 -> 10 | 132 -> 124 | +195 | -66 | +261 | 35 -> 35 | 178 -> 149 |

### (e) Live quasi-experiment (UNPAIRED): real P48 seats vs our older PFS-h0 subs that sold >= 20 melons d10-14 vs subs that sold < 5 (see melon.md phase table)

With our wave (n 27): d10-14 rev R-O -4.4k, d15-29 R-O +3.2k, our d15-29 revenue 89.3k, rival d15-29 92.5k, final R-O +4.1k, W 26 %. Without (n 43): +19.9k, -11.9k, 99.5k, 87.7k, +3.3k, W 26 %. Late charge = rival +4.8k for our -10.2k late revenue (-0.47 coin per coin) vs the clone paired -0.74 (p48c). Different bodies (the older subs kept a larger late herd: our d15-29 milk/wool 141/120 vs 124/104) and different weeks; indicative only.

**Reading.**
- **Natural variation is demand-driven in both worlds.**
  - Simple slopes are strongly positive live (milk +143, wool +178, strawberry +199 coins/u; r 0.68-0.87, n 88) and on the clone (+201 / +116 / +118, n 80).
  - With the town's consumer shops as controls, live and clone agree: milk +12 +- 18 vs +11 +- 32, wool +55 +- 18 vs +56 +- 20. Only strawberry differs: +49 +- 18 vs +93 +- 19, and there live is the MORE negative.
- **The method cannot find the causal charge, even on the clone.** There the paired arm measures -176 / -62 / -101 coins per unit.
  - Its price-channel form (M3) also stays near 0: -0.23 vs the causal -1.12 c/u per unit.
  - So live data can neither confirm nor refute the magnitude. It shows the same market signature as the clone, not a weaker charge.
- **The clone's charge is a price effect.**
  - p48c: milk +5,863 of +5,942 comes from price (+38 c/u on an unchanged 155 u); wool +2,044 of +2,618; strawberry +1,191 of +2,045.
  - It is a market property of the engine that real seats share. Its size scales with the rival's late units and the late price level, which live we measure directly.
- **big's volume reaction is the odd one out.** big: milk -1,825, wool -3,200. pq4c: -727 / -457. p48c: +79 / +574.
- **The live quasi-experiment (older subs with a d10-14 melon wave, unpaired) points the same way.** The rival earns +4.8k late for our -10.2k late revenue (-0.47 coin per coin), vs the clone's -0.74.

## 3. The melon wave (live, MELONLOSS1 style) and the clones' d10-14

Signs are RIVAL minus OURS (positive = the programme is ahead). gap d9 = money at d9 h23; phase d10-14 = change of the gap d9 -> d14 h23; phase d15-29 = final margin - gap d14. Revenue columns are R-O sales coins by book; spend R-O by window. Means per game (unpaired sets).

| set | n | gap end d9 | d10-14 phase | d15-29 phase | final (R-O) | d10-14 melon rev R-O | d10-14 other rev R-O | d10-14 spend R-O | d15-29 herd rev R-O (MLK/WOL/EGG/FRT) | d15-29 STR rev R-O | d15-29 melon rev R-O | d15-29 WHE/CAR/TOM rev R-O | d15-29 spend R-O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P48 programme WINS (our L) | 52 | -3,513 | +15,888 | -900 | +11,475 | +5,767 | +6,348 | -3,820 | +2,597 | -816 | -5,345 | +4,590 | +1,998 |
| P48 programme LOSES (our W) | 19 | -3,465 | +9,759 | -27,895 | -21,602 | +4,788 | +1,284 | -3,777 | -10,237 | -7,529 | -6,698 | -4,292 | -770 |
| PQ4 programme WINS (our L) | 12 | -4,122 | +19,151 | +1,130 | +16,159 | +13,174 | +15,275 | +9,303 | +5,975 | -1,403 | -13,496 | +31,066 | +21,006 |
| PQ4 programme LOSES (our W) | 5 | -4,817 | +20,782 | -18,437 | -2,472 | +13,649 | +24,916 | +17,693 | -917 | -13,684 | -14,901 | +60,125 | +49,150 |
| ALL programme WINS (our L) | 64 | -3,627 | +16,500 | -519 | +12,353 | +7,156 | +8,022 | -1,359 | +3,230 | -926 | -6,873 | +9,554 | +5,562 |
| ALL programme LOSES (our W) | 24 | -3,747 | +12,055 | -25,925 | -17,617 | +6,634 | +6,208 | +696 | -8,295 | -8,811 | -8,407 | +9,128 | +9,630 |
| OM-P48 programme WINS (our L) | 74 | -3,529 | +19,153 | -4,466 | +11,158 | +10,022 | +13,444 | +4,157 | +3,991 | -1,411 | -6,427 | +18,099 | +18,962 |
| OM-P48 programme LOSES (our W) | 12 | -4,273 | +18,733 | -26,939 | -12,479 | +10,898 | +22,862 | +14,804 | -9,087 | -5,589 | -10,325 | +41,047 | +43,283 |

### Units: the same programme when PFS keeps its wall and herd (our W) vs when it wins (our L)

| set | n | rival melon d10-14 u / coins (c/u) | our melon d10-14 u | STR d15-17 u O / R | d15-29 u O vs R: MLK | WOL | EGG | STR | MEL | d15-29 price O vs R: MLK | WOL | STR | herd d14 C/S/G O vs R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P48 programme WINS (our L) | 52 | 53 / 11,928 (227) | 27.7 | 45 / 46 | 128 vs 137 | 115 vs 111 | 95 vs 160 | 230 vs 204 | 63 vs 21 | 81 vs 80 | 80 vs 76 | 109 vs 121 | 6.8/7.5/3.4 vs 7.9/6.6/5.5 |
| P48 programme LOSES (our W) | 19 | 47 / 10,778 (230) | 26.8 | 47 / 40 | 149 vs 144 | 98 vs 78 | 96 vs 133 | 243 vs 198 | 57 vs 15 | 106 vs 93 | 102 vs 91 | 129 vs 126 | 7.5/5.8/3.4 vs 8.2/4.7/4.4 |
| PQ4 programme WINS (our L) | 12 | 60 / 14,510 (242) | 6.0 | 51 / 39 | 108 vs 139 | 106 vs 89 | 145 vs 188 | 222 vs 217 | 86 vs 5 | 61 vs 64 | 68 vs 74 | 105 vs 105 | 6.2/7.2/5.1 vs 8.8/6.3/6.8 |
| PQ4 programme LOSES (our W) | 5 | 55 / 13,649 (248) | 0.0 | 60 / 39 | 136 vs 142 | 91 vs 92 | 122 vs 171 | 295 vs 233 | 75 vs 0 | 110 vs 116 | 106 vs 108 | 181 vs 175 | 7.4/6.0/4.2 vs 9.0/6.2/6.4 |
| ALL programme WINS (our L) | 64 | 54 / 12,412 (230) | 23.6 | 46 / 44 | 124 vs 138 | 113 vs 107 | 104 vs 165 | 228 vs 206 | 68 vs 18 | 77 vs 77 | 77 vs 76 | 108 vs 118 | 6.7/7.5/3.7 vs 8.0/6.5/5.7 |
| ALL programme LOSES (our W) | 24 | 49 / 11,376 (234) | 21.2 | 50 / 40 | 146 vs 144 | 97 vs 81 | 102 vs 141 | 254 vs 205 | 61 vs 12 | 107 vs 98 | 103 vs 95 | 140 vs 136 | 7.5/5.8/3.5 vs 8.3/5.0/4.8 |
| OM-P48 programme WINS (our L) | 74 | 53 / 12,610 (239) | 11.8 | 47 / 38 | 134 vs 149 | 131 vs 133 | 88 vs 120 | 215 vs 186 | 79 vs 28 | 89 vs 90 | 96 vs 97 | 104 vs 111 | 7.1/8.3/3.0 vs 8.0/8.1/4.2 |
| OM-P48 programme LOSES (our W) | 12 | 56 / 13,497 (241) | 12.0 | 45 / 38 | 145 vs 133 | 151 vs 106 | 88 vs 146 | 208 vs 186 | 78 vs 11 | 94 vs 90 | 115 vs 105 | 115 vs 112 | 7.7/8.3/3.0 vs 7.5/5.8/5.6 |

### Does the clone reproduce the real d10-14 melon receipts? (rival seat, vs PFS)

| set | n | rival melon d10-14 u | coins | c/u | rival melon d15-29 u | our melon d10-14 u | PFS W % |
|---|---|---|---|---|---|---|---|
| judge p48c ctl | 80 | 41.7 | 10,516 | 252 | 10.0 | 3.9 | 99 |
| judge pq4c ctl | 40 | 52.9 | 13,171 | 249 | 3.2 | 0.0 | 98 |
| judge big ctl | 40 | 47.3 | 11,867 | 251 | 10.2 | 0.0 | 100 |
| judge p48c ARM b9r s0 (our wave) | 40 | 41.5 | 9,904 | 239 | 5.3 | 47.9 (ours 11,119 coins, 232 c/u) | 98 |
| judge p48c ARM b9r s1 (our wave) | 40 | 41.5 | 9,911 | 239 | 4.5 | 47.9 (ours 11,121 coins, 232 c/u) | 95 |
| judge big ARM b9r | 40 | 47.2 | 11,029 | 234 | 7.1 | 47.9 (ours 11,067 coins, 231 c/u) | 100 |
| judge pq4c ARM b9r | 40 | 52.9 | 12,196 | 231 | 2.9 | 47.9 (ours 10,909 coins, 228 c/u) | 98 |
| LIVE real P48 vs PFS | 71 | 51.0 | 11,620 | 228 | 19.4 | 27.5 | 27 |
| LIVE real PQ4 vs PFS | 17 | 58.5 | 14,257 | 244 | 3.2 | 4.2 | 29 |

### Revenue R-O by phase, clone judges vs live real seats (both vs PFS; sales coins only, spend excluded)

| set | n | PFS W % | d0-9 rev R-O | d10-14 rev R-O | of which melon | d15-29 rev R-O | of which MLK+WOL | of which STR | rival d10-14 rev | rival d15-29 rev | our d15-29 rev | final R-O mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| judge p48c ctl | 80 | 99 | -256 | +15,590 | +9,573 | -47,882 | -3,008 | -21,968 | 26,632 | 75,582 | 123,464 | -32,209 |
| judge pq4c ctl | 40 | 98 | -1,219 | +17,159 | +13,171 | -45,781 | -4,427 | -17,894 | 28,156 | 78,497 | 124,278 | -30,283 |
| judge big ctl | 40 | 100 | -1,882 | +15,915 | +11,867 | -41,751 | -12,016 | -8,546 | 26,555 | 80,014 | 121,765 | -48,243 |
| judge p48c ARM b9r (fired us) | 80 | 96 | +287 | -1,609 | -1,213 | -24,154 | +10,524 | -18,262 | 25,606 | 85,658 | 109,812 | -22,776 |
| LIVE real P48 (all PFS-h0 subs) | 71 | 27 | +153 | +10,498 | +5,505 | -6,943 | -3,377 | -2,612 | 29,596 | 89,660 | 96,603 | +2,623 |
| LIVE real P48 vs vrp20 | 25 | 28 | +390 | +20,915 | +12,751 | -13,108 | -1,963 | -5,044 | 31,293 | 89,114 | 102,222 | +3,629 |
| LIVE real PQ4 (all) | 17 | 29 | +1,343 | +31,425 | +13,314 | +24,636 | +1,933 | -5,015 | 43,096 | 119,564 | 94,928 | +10,679 |
| LIVE other-MELON P48-behaviour (OTHERMELON1, off-code) | 86 | 14 | +2,489 | +24,902 | +10,144 | +14,503 | -802 | -1,994 | 39,035 | 112,012 | 97,509 | +7,860 |
| LIVE P48, our d10-14 melon >= 20 u (older subs) | 27 | 26 | -361 | -4,411 | -5,308 | +3,184 | -1,475 | -2,455 | 28,344 | 92,499 | 89,315 | +4,116 |
| LIVE P48, our d10-14 melon < 5 u | 43 | 26 | +536 | +19,945 | +12,285 | -11,879 | -4,352 | -1,735 | 30,644 | 87,652 | 99,531 | +3,283 |

**Reading.**
- **Where the real P48 makes its winning margin** (programme wins = our L, n 52): d0-9 -3.5k, **d10-14 +15.9k**, d15-29 -0.9k, final +11.5k.
  - The d10-14 phase breaks down into melon revenue R-O +5.8k, other revenue +6.3k and spend -3.8k. Against vrp20, which sells no melons d10-14, the melon R-O is +12.8k (phase table).
- **When PFS keeps its wall and herd** (our W, n 19), the same programme still takes d10-14 (+9.8k) with the same melon wave (47 u @230 vs 53 u @227). It loses d15-29 by -27.9k: herd -10.2k, strawberry -7.5k, melon -6.7k, wheat/carrot/tomato -4.3k.
  - Our late units differ little between our wins and losses, with mixed signs: milk 149 vs 128, wool 98 vs 115, strawberry 243 vs 230.
  - Our late prices do: milk 106 vs 81, wool 102 vs 80, strawberry 129 vs 109. So does the rival's herd at d14 (sheep 4.7 vs 6.6, geese 4.4 vs 5.5).
  - W/L is decided by town demand and the rival's herd, not by our volume (MELONLOSS1 and OTHERMELON1 agree).
- **The other-MELON P48 seats show the same split:** d10-14 +19.2k / +18.7k, d15-29 -4.5k / -26.9k.
- **Clone melon receipts:**
  - p48c: 41.7 u / 10.5k at 252 c/u vs real 51.0 u / 11.6k at 228 c/u.
  - pq4c: 52.9 / 13.2k vs 58.5 / 14.3k.
  - The clones' d10-14 revenue R-O (+15.6k / +17.2k) sits inside the live range (+10.5k all subs, +20.9k vs vrp20).
  - The clones fail in d15-29: R-O -47.9k vs -6.9k live. Strawberry alone is -22.0k vs -2.6k, and our late revenue is 123.5k vs 96.6k live.

## 4. PROGFIRE1 b9r transferred to real seats

Clone read: d-own -559, d-rival +8,874, **d-margin -9,433**.

| book (d15-29) | clone rival u / c/u (ctl) | live real P48 rival u / c/u | clone d-rival: price + volume | transferred d-rival (kappa 1 / kappa 0) | clone d-ours | our c/u clone ctl -> live | transferred d-ours |
|---|---|---|---|---|---|---|---|
| WHEAT | 304 / 38 | 356 / 36 | +261 + +1,280 | +1,496 / +288 | -970 | 37 -> 36 | -960 |
| CARROT | 29 / 56 | 147 / 49 | +33 + +322 | +355 / +355 | +381 | 52 -> 51 | +376 |
| TOMATO | 3 / 208 | 51 / 97 | -109 + +344 | +234 / +234 | -1,477 | 190 -> 142 | -1,101 |
| STRAWBERRY | 101 / 182 | 202 / 127 | +1,191 + +854 | +2,256 / +1,660 | -1,661 | 176 -> 122 | -1,144 |
| MELON | 10 / 232 | 19 / 187 | -619 + -861 | -1,480 / -1,480 | -7,610 | 183 -> 151 | -6,281 |
| EGG | 112 / 47 | 152 / 44 | -170 + -577 | -765 / -219 | +3,167 | 48 -> 45 | +2,982 |
| MILK | 155 / 116 | 139 / 91 | +5,863 + +79 | +4,173 / +4,112 | -194 | 115 -> 103 | -173 |
| WOOL | 103 / 135 | 102 / 118 | +2,044 + +574 | +2,275 / +1,772 | -4,777 | 141 -> 128 | -4,336 |
| FERTILIZER | 118 / 33 | 119 / 33 | -194 + -238 | -432 / -195 | -510 | 34 -> 33 | -506 |

**d10-14 melon.** Our wave in the clone arm: +44 u, +10,177 coins at 232 c/u. Live, our older subs that sold >= 20 melons d10-14 (n 27, unpaired) got 223 c/u -> our wave +9,747 (adj -430). The rival's d10-14 melon book in the clone arm: -608; live the rival's melon price is 196 c/u when we sell >= 20 vs 250 when we sell < 5 (n 27 / 43, unpaired) -> 51 u x -54 = -2,744 (adj to our margin +2,136; carried as a range 0 .. this, unpaired).

**Transferred d-margin on real P48 seats:** kappa 1 (the real programme reacts like the clone), no live melon externality: **-5,391**; kappa 0 (scripted, price effect only) + the live melon externality: **-1,671**; central (kappa 0.5, half the externality): **-3,531**. Clone read -9,433. d15-29 adjustments: kappa 1 +4,472, kappa 0 +6,056.

Sampling SE of the clone d-margin (board-clustered, 40 boards): 2,093. Uncertainty of the transfer = the kappa / externality range above (+- half-range 1,860) and the sampling SE, combined ~ +-2,800.

### Robustness: P48 incl. OTHERMELON1 off-code P48-behaviour seats (n 157)

**Transferred d-margin on real P48 seats:** kappa 1 (the real programme reacts like the clone), no live melon externality: **-5,928**; kappa 0 (scripted, price effect only) + the live melon externality: **-2,210**; central (kappa 0.5, half the externality): **-4,069**. Clone read -9,433. d15-29 adjustments: kappa 1 +4,003, kappa 0 +5,592.
Sampling SE of the clone d-margin (board-clustered, 40 boards): 2,093. Uncertainty of the transfer = the kappa / externality range above (+- half-range 1,859) and the sampling SE, combined ~ +-2,799.

### PQ4 seats (pq4c read -30)

Clone read: d-own +6,002, d-rival +6,033, **d-margin -30**.

| book (d15-29) | clone rival u / c/u (ctl) | live real P48 rival u / c/u | clone d-rival: price + volume | transferred d-rival (kappa 1 / kappa 0) | clone d-ours | our c/u clone ctl -> live | transferred d-ours |
|---|---|---|---|---|---|---|---|
| WHEAT | 291 / 38 | 1159 / 36 | -125 + +1,644 | +1,075 / -465 | -2,081 | 37 -> 33 | -1,871 |
| CARROT | 61 / 52 | 192 / 40 | -48 + +844 | +536 / -117 | +244 | 49 -> 41 | +204 |
| TOMATO | 8 / 132 | 104 / 68 | -66 + +261 | +195 / +195 | -1,108 | 178 -> 74 | -459 |
| STRAWBERRY | 108 / 181 | 221 / 126 | +885 + -170 | +1,141 / +1,259 | +2,366 | 172 -> 135 | +1,857 |
| MELON | 3 / 225 | 3 / 212 | -271 + -42 | -313 / -313 | -9,085 | 183 -> 177 | -8,771 |
| EGG | 100 / 48 | 183 / 46 | -307 + -874 | -1,387 / -541 | +5,548 | 48 -> 46 | +5,307 |
| MILK | 147 / 137 | 140 / 88 | +5,022 + -727 | +2,612 / +3,080 | -1,364 | 134 -> 94 | -960 |
| WOOL | 103 / 133 | 90 / 113 | +3,061 + -457 | +1,869 / +2,256 | -2,790 | 141 -> 95 | -1,886 |
| FERTILIZER | 118 / 35 | 105 / 37 | -28 + -461 | -521 / -27 | -373 | 34 -> 33 | -364 |

**d10-14 melon.** Our wave in the clone arm: +48 u, +10,909 coins at 228 c/u. Live, our older subs that sold >= 20 melons d10-14 (n 28, unpaired) got 223 c/u -> our wave +10,650 (adj -259). The rival's d10-14 melon book in the clone arm: -975; live the rival's melon price is 196 c/u when we sell >= 20 vs 249 when we sell < 5 (n 28 / 59, unpaired) -> 58 u x -53 = -3,117 (adj to our margin +2,141; carried as a range 0 .. this, unpaired).

**Transferred d-margin on real PQ4 seats:** kappa 1 (the real programme reacts like the clone), no live melon externality: **+4,348**; kappa 0 (scripted, price effect only) + the live melon externality: **+6,369**; central (kappa 0.5, half the externality): **+5,358**. Clone read -30. d15-29 adjustments: kappa 1 +4,637, kappa 0 +4,517.

Sampling SE of the clone d-margin (board-clustered, 40 boards): 1,758. Uncertainty of the transfer = the kappa / externality range above (+- half-range 1,010) and the sampling SE, combined ~ +-2,028.

**Mix.** At the live coded family shares, P48 71 : PQ4 17: 0.807 x (-3.5k) + 0.193 x (+5.4k) = **-1.8k +- 2.3k per fired game**. The fire decision is made at h1, by code, before the family shows at d11. PQ4C codes are mostly P48 behaviour live (PQ4C 38 seats, PQ4 family 17), so PQ4-only firing does not exist.

**Model risk not in the +- band:**
- the proportional price response;
- the unpaired live melon externality: the rival's price is 196 vs 249 c/u when our older subs sold >= 20 melons d10-14, against 252 -> 239 in the clone arm;
- the d10-14 non-melon books, kept at the clone values.

### 4b. Within-clone check of the price-level transfer (no live data): the paired read by tercile of the control's late price level
Price index of a board = the control game's rival d15-29 revenue / units over milk+wool+strawberry (c/u). Live real P48 = 107 c/u (milk 91, wool 118, strawberry 127 weighted by units); clone p48c ctl = 146.

| rival | tercile of ctl price index | n | ctl price index | rival d15-29 d coins (MLK+WOL+STR) | d rival milk c/u (ctl c/u) | d our MLK+WOL u | d-own | d-rival | d-margin | W ctl -> arm |
|---|---|---|---|---|---|---|---|---|---|---|
| p48c | low (live-like) | 26 | 104 | +7,059 | +15 (45) | -58 | +691 | +5,728 | -5,036 | 25 -> 26 |
| p48c | mid | 26 | 128 | +9,920 | +40 (76) | -76 | -1,183 | +9,394 | -10,576 | 26 -> 26 |
| p48c | high | 28 | 170 | +14,535 | +40 (171) | -93 | -1,140 | +11,314 | -12,454 | 28 -> 25 |
| p48c | all | 80 | 135 | +10,605 | +32 (99) | -76 | -559 | +8,874 | -9,433 | 79 -> 77 |
| pq4c | low (live-like) | 13 | 107 | +8,284 | +11 (57) | -53 | +8,569 | +6,417 | +2,151 | 13 -> 13 |
| pq4c | mid | 13 | 134 | +8,524 | +52 (94) | -60 | +7,797 | +6,926 | +871 | 13 -> 13 |
| pq4c | high | 14 | 186 | +6,148 | +25 (190) | -101 | +1,953 | +4,845 | -2,893 | 13 -> 13 |
| pq4c | all | 40 | 143 | +7,614 | +29 (116) | -72 | +6,002 | +6,033 | -30 | 39 -> 39 |
| big | low (live-like) | 13 | 96 | +6,489 | +9 (73) | -36 | +8,153 | +2,275 | +5,878 | 13 -> 13 |
| big | mid | 13 | 127 | +8,105 | +52 (108) | -89 | +9,217 | +4,003 | +5,213 | 13 -> 13 |
| big | high | 14 | 175 | +3,816 | +40 (179) | -72 | +7,201 | -2,630 | +9,831 | 14 -> 14 |
| big | all | 40 | 133 | +6,079 | +34 (121) | -66 | +8,166 | +1,120 | +7,046 | 40 -> 40 |

The clone's own live-like price tercile agrees with the transfer:
- **p48c low tercile:** d-margin **-5.0k** per game, -6.0k +- 2.8k board-clustered (14 boards, t -2.12). Mid is -10.6k and high is -12.5k. The rival's late gain there is +7.1k, against +14.5k in the high tercile.
- **pq4c low tercile:** +2.2k +- 2.4k (t 0.90).

So the charge falls with the late price level, as the transfer assumes. On P48 seats the sign stays negative at live-like prices.

## 5. What REFRESH4 must hit before a clone judge is trusted for fired reads
Targets are live real seats vs PFS (P48 n 71, of which vrp20 n 25; PQ4 n 17). The p48c / pq4c value today is in brackets.

**P48 clone**
- PFS W: **27 %** (accept 17-40 %) [99 %].
- Margin median: -8.1k [+32.2k].
- Rival final median: **~105k** [89.7k]. Our final: ~101k [124.7k].
- d15-29 revenue R-O: **-7k** (vrp20 -13k) [-47.9k]. Rival d15-29 revenue 89.7k [75.6k]; our d15-29 revenue 96.6k [123.5k].
- Rival d10-29 units: strawberry **211** [101], tomato **51** [3], carrot **148** [29], wheat 415 [326], egg 179 [133]. Keep milk 179 [190] and wool 119 [123].
- Melon d10-14: **51 u / 11.6k at 228 c/u** [42 / 10.5k at 252].
- Our d15-29 c/u against it: milk 103 / wool 128 / strawberry 122 [115 / 141 / 176].

**PQ4 clone**
- PFS W: 29 % [98 %].
- Wheat d10-29: **1,458** [321]. Tomato 104 [8], carrot 199 [62], strawberry 236 [111], egg 204 [113].
- Melon d10-14: 58.5 u / 14.3k [52.9 / 13.2k].
- Rival d10-29 revenue: 163k [107k]. Rival final: 104.5k [90.1k].

**Protocol checks**
- The paired charge must stay a price effect: the rival's volume reaction <= 25 % of its late delta. big fails this.
- The two faithful P48-code tapes (-2.0k for b9r) are the external check: a trusted clone must read the fired arm within +-3k of them on those seats.
