# TURNCENSUS — the 09-14 turn census re-run on the shipped FT2
2026-09-17 13:56-14:20Z, branch `turncensus`, CPU sim only, no engine leg, no src change. Tools `S/turncensus/{instrument.py,report.py}` (= `S/turns/`, out-dir moved); raws `raw_{ft2_eng22,ft2_topleg,b14_eng22}.npz`; full tables `S/turncensus/report_{eng22,topleg,b14_eng22}.md` + `compare_eng22.txt`. **ENG22 44 boards** (22 fidelity-gated engine tapes x2 seats) is the read; **TOPLEG 60** (30 Majkel1337 tapes x2 seats) is a bound only — those tapes desync in the sim (`S/eng22/fidelity.py`): class 14.7 coins/worked turn vs ENG22's 18.7. `b14` = pre-FT2 B (`FERT_TIMING/LOT4/SLOT_PRIORITY` forced off; the rest of the FT2 string is already default-True in src, and **`submission/theta.npy` md5 == `flow193_g100_hr.npy`** — FT2 is B's theta plus switches, with `MELON_GENE_ON`/`CROP_DAY_ON` byte-inert on it). Cross-check: pre-FT2 B here reproduces 09-14's B on a different set — worked 6,016.0 vs 5,986.4, PASS 687.8 vs 687.0.

## 1. Census, unit-turns/game (ENG22, paired)
| op | FT2 d0-9 | d10-19 | d20-29 | **FT2 season** | class | **FT2-cls** | B(pre) | B-cls | 09-14 B (ymg) | TOPLEG FT2-cls |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PLANT | 71.2 | 51.5 | 55.7 | 178.3 | 214.9 | -36.5 | 180.2 | -34.7 | 184.2 | -84.1 |
| WATER | 225.2 | 390.7 | 330.4 | 946.3 | 1,038.8 | -92.5 | 955.6 | -83.2 | 972.2 | -265.0 |
| HARVEST | 44.8 | 161.4 | 228.8 | 435.0 | 470.0 | -34.9 | 437.9 | -32.0 | 448.3 | -47.6 |
| FERTILISE | 0.0 | 72.7 | 83.1 | 155.8 | 170.7 | -14.9 | 185.7 | +15.0 | 169.6 | -24.4 |
| FEED/CARE | 109.6 | 295.6 | 198.1 | 603.3 | 616.7 | -13.5 | 603.9 | -12.8 | 604.3 | +1.7 |
| COLLECT_FERT | 59.9 | 163.3 | 152.7 | 375.9 | 351.6 | +24.3 | 376.2 | +24.6 | 373.2 | +13.8 |
| BUILD/DIG | 11.0 | 6.9 | 29.4 | 47.3 | 60.9 | -13.5 | 47.2 | -13.7 | 42.2 | -7.8 |
| MOVE | 513.0 | 1,157.9 | 1,187.6 | 2,858.5 | 3,011.8 | -153.3 | 2,901.2 | -110.5 | 2,871.9 | -318.7 |
| SHED pickup/drop | 49.3 | 132.3 | 127.3 | 309.0 | 353.8 | -44.8 | 328.0 | -25.8 | 320.4 | -82.1 |
| PASS | 152.8 | 243.5 | 270.7 | 667.0 | 890.1 | -223.1 | 687.8 | -202.3 | 687.0 | +231.7 |
| **ACTIVE** | 1,236.8 | 2,675.7 | 2,663.8 | **6,576.3** | 7,179.2 | **-602.9** t-8.6 | 6,703.8 | -475.5 | 6,673.4 | -582.4 |
| **WORKED** | 1,084.0 | 2,432.2 | 2,393.1 | **5,909.3** | 6,289.1 | **-379.8** t-8.2 | 6,016.0 | -273.1 | 5,986.4 | -814.1 |

BUY/SELL market rows cost no crew turn. Worked by band FT2-class: **d0-9 -198.0 (t -9.4), d10-19 -1.7 (t -0.1), d20-29 -180.0 (t -4.9)**. Hires d0-9 **43.3 vs 64.1**, season 256.7 vs 285.6 (crew-days 244.0 vs 269.1). Day 0/1/2 hires are a constant **4/1/3** on all 44 boards against the class's 5.8/3.8/5.1, while our dawn cash is *higher* than theirs on d1/d4/d6/d8 — the early crew gap is the hire enumeration, not money.

## 2. Decomposition of the -379.8 worked turns (identity: worked = active - PASS)
| | turns/game | t | @17.52 (09-14) | @19.45 (FT2's own) |
|---|---:|---:|---:|---:|
| **(a) fewer hands** — active turns; = -25.1 crew-days, **78 % of it d0-9** | **-602.9** | -8.6 | -10,563 | -11,727 |
| **(b) PASS/idle of hired hands** — h2-19 +229.7, h20-23 +157.3: we idle LESS | **+387.0** | +7.2 | +6,780 | +7,527 |
| **(c) market-row wait h0-1** — our PASS 265.2 vs their 101.4 | **-163.8** | -11.5 | -2,870 | -3,186 |
| **= worked** | **-379.8** | -8.2 | **-6,653** | **-7,387** |
| **(d) moves** — 2,858.5 vs 3,011.8; 0.94 vs 0.92 ops/task: level, not a sink | -153.3 | -4.6 | — | — |

**The class's own marginal crew converts badly**: their extra ACTIVE turns buy worked turns at **0.43 in d0-9** (+464.8 active -> +198.0 worked; their d0-9 PASS share 24.7 % vs our 12.4 %), **0.05 in d10-19**, **1.73 in d20-29** (only +104 active but +180 worked — their *tail is busier, not bigger*). So a d0-9 crew lever's honest ceiling is 465 x 0.43 = **~198 turns = +3,850 coins**, not 12,150, and d20-29 is work availability (JOINTLIFT's unwatered tiles), not hiring.
**Directions.** *DAWNBUNDLE* supported and untouched by FT2: at h0-1 our roster is *larger* than theirs (active 297.6 vs 252.1) and PASSes anyway; worked h0-1 **32.4 vs 150.7** (TOPLEG class 254.9) = **+118..+223 turns (+2.3k..+4.3k)** — the only component where the hands already stand there and the class proves the hours fillable (FT2 h0-1 PASS 265.2 vs B 269.3: the 09-14 sink is intact). *TURNBUDGET* partly — the gap *is* crew size, but at 0.43 conversion its own +300-worked-turn gate needs d20-29 work availability, not hires. *OPENGATE* confirmed inert by construction: d0-9 hires and d0-9 worked turns are **identical** FT2 vs B, and the early marginal hand is 57 % idle. *SCHEDSEARCH* not discriminated here.

## 3. VERDICT
**Shortfall NOT closed — -379.8 worked turns/game (t -8.2) against the gated engine class, worth 6.7-7.4k at 09-14 pricing, located in (a) crew size (-602.9 active turns, 78 % of it d0-9) net of a +387 idle credit, plus (c) -163.8 at hours 0-1.** FT2 made it *wider*: -106.6 worked turns vs pre-FT2 B (t -12.5), season hires -5.9.
**But the 09-14 identity is dead.** FT2 beat pre-FT2 B by **+2,465 coins (t +8.4)** on these boards while working **107 fewer** turns, at 19.45 vs 18.93 net-market coins per worked turn; and the residual ENG22 margin is **-763 (t -0.5)** — near parity — against that -380-turn gap, with net market only -3,027 (t -1.6). Worked turns no longer price at 17.52 on the margin: "the whole top-five gap is inside the crew-turn budget" was true of B on the ymg set and is **false of FT2 on the engine class**. There is no 12k target here; the readable labour ceiling is **~+4k** and it sits in the **dawn hours**, not in hiring.
**One falsifier next — DAWNBUNDLE's census read.** Run the 2x2 `EARLY_SELL_ON x PRESTOCK_ON` (the `assert plan.py:2478` cell nobody has paid for) through `S/turncensus/instrument.py` on these same 44 ENG22 boards, CPU ~15 min. Gate: **worked turns at hours 0-1 rise >= +80/game with season PASS falling, not merely relocating to h2-23**. If h0-1 will not fill while the roster is already standing there, the crew-turn axis is closed and PLANNER2 #1-#3 fall with it.
