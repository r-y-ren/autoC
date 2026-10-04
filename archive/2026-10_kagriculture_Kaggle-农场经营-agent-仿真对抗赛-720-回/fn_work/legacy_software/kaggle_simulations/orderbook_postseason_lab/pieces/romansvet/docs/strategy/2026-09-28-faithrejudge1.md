# FAITHREJUDGE1 (2026-09-27 22:33Z-23:00Z): JC1 re-judge of the MELON-seat rejects that changed our early tiles

Replay-only. No games were run, no engine was re-applied, and nothing under src/ was touched. Every number comes from the existing leg csvs plus the MELONDUMP1 engine-commit logs (`S/melondump1/ext/{A_n20dump,base}`, the MELONWIN1 commit hook that JUDGECLEAN1 `livetrace.py` also uses). Faithfulness and the paired rows are JUDGECLEAN1's `faith.py` / `pair_faith.py`, unchanged.

**Verdict: no reject flips under JC1.** Every rival-purse gift that was the reason for a reject survives on the faithful seats, and in most cells it gets sharper. The breakage share of Σdtheirs is small where the gift is large: MELONDUMP1 13 %, NONV2 M20 −3 %, MELONCOUNTER2 Tn 0 %. Where the breakage share is large, it is negative: the broken seats carried rival **losses**, and the "noise-board" flips sat on those seats. **The breakage guard does not fire on any cell.** **No re-run is recommended.**

- **MELONDUMP1 A: the +19.3k gift is real and it is PRICE, not breakage.**
  - The units basis is available here from the engine-commit logs. The arm keeps the rival tape faithful on 47/51 seats (base 48/51), and the rival's units sold are within ±5 % of live on 47/51.
  - On the 45 faithful seats dtheirs is +18,952 (t 12.2), against +19,295 on all 51.
  - Split of the rival's SELL on the faithful seats (A − base): **price +19.4k**, volume +0.6k.
    - By item, price: STRAWBERRY +10.2k, WOOL +5.2k, MILK +4.8k, FERTILIZER +2.0k, MELON −3.5k.
  - The rival sells the same units at better prices, because our plate takes supply off strawberry, milk and wool.
- **The cash proxy cannot flag an upward break.** The NONV2 and MELONCOUNTER2 grids keep no units, so faith.py uses the cash basis, which only catches a rival purse falling more than 5 % below live.
  - The NONV2 M20 / QM20H2 rival sits +21-26k above live. That is the same plate mechanism as MELONDUMP1, where the units test shows it is real. So these gifts are read as real, not as breakage.

## 1. Cell table (ALL seats vs FAITHFUL seats = base AND arm faithful)

Column notes:
- **Basis:** "units" means rival units vs live (|du| ≤ 5 % and purse ≥ ½ live). "cash" means rival purse ≥ −5 % of live.
- **rvl:** rival-vs-live purse, as mean (t), on the FAITHFUL seats (arm / base).
- **Guard:** JC1 rule 3, n_f(arm) < n_f(base) − max(3, 10 % of n).

| stream / cell | base, bed, basis | ALL: n, W b→a, flips, dours (t), dtheirs (t) | FAITHFUL: n, W b→a, flips, dours (t), dtheirs (t) | breakage share | rvl arm / base (faithful) | guard | verdict before → after |
|---|---|---|---|---|---|---|---|
| **MELONDUMP1 A** (d2 latch, N20 plate, dump) | pfv1, 51 BAND MELON, units | 51, 14→5, +2/−11, +3,413 (2.14), **+19,295 (13.49)** | 45, 9→4, +2/−7, +3,624 (2.37), **+18,952 (12.22)** | 13 % | +17,173 (10.1) / −1,778 (−3.0) | no (47 vs 48) | REJECT gift → **REJECT gift (real, price)** |
| MELONDUMP1 B (N20 plate, default timing) | pfv1, 5 seats, cash | 5, 1→0, 0/−1, +5,974 (0.96), +13,321 (2.54) | 5, same | 0 % | +11,789 (2.1) / −1,532 | no | same sign → unchanged |
| MELONCOUNTER2 Wf | vrp7 OFF, 18 of 26 tape seats in BAND142, cash | 18, 0→1, +1/−0, +585 (0.55), −197 (−0.23) | 17, 0→1, +1/−0, +104 (0.10), +440 (0.75) | 311 % (broken = rival −11k) | +439 / −1 | no | noise → noise |
| MELONCOUNTER2 **Wn** | same | 18, 0→2, +2/−0, +287 (0.20), +1,919 (1.33) | 16, 0→2, +2/−0, +230 (0.15), **+3,301 (2.67)** | −53 % | +3,300 / −1 | no | gift → **gift sharper** |
| MELONCOUNTER2 Tf | same | 18, 0→2, +2/−0, +2,389 (3.11), −842 (−0.60) | 17, 0→1, **+1/−0**, +2,124 (2.77), +470 (0.92) | 153 % (mhw_113480538 flip = rival −27 %) | +469 / −1 | no | noise flips, reacting gift → one flip was breakage; BAND Tf (next row) gifts |
| BANDLEG1 (3') Tf, full MELON cell | tfoff (same tree), 51 BAND MELON, cash | 51, 6→7, +3/−2, +1,236 (2.34), +1,006 (1.57) | 49, 5→6, +2/−1, +1,294 (2.54), **+1,400 (3.29)** | −34 % | +1,505 (3.3) / +105 | no (49 vs 50) | GIFT (vrp10 seats) → **gift sharper (t 3.29)** |
| MELONCOUNTER2 **Tn** | vrp7, 18, cash | 18, 0→0, 0/0, +1,422 (1.31), **+6,782 (5.91)** | 18, same | 0 % | +6,781 / −1 | no | gift → gift |
| MELONCOUNTER2 Sf | same | 18, 0→0, 0/0, −709 (−1.35), −403 (−0.91) | 18, same | 0 % | −404 / −1 | no | loss → loss |
| MELONCOUNTER2 **Sn** | same | 18, 0→0, 0/0, −4,771 (−4.08), +3,428 (1.65) | 16, 0/0, −4,763 (−4.00), **+5,422 (3.13)** | −41 % | +5,421 / −1 | no | gift → gift sharper |
| MELONCOUNTER2 Cf (tapes; BAND Cf = BANDREJUDGE1 b, skipped) | same | 18, 0→3, +3/−0, +1,124 (1.42), −1,718 (−1.01) | 15, 0→1, **+1/−0**, +48 (0.09), +856 (1.35) | 142 % (2 of 3 flips on broken seats) | +855 / −1 | no (15 vs 18, bar 15) | noise flips → 2 of 3 flips were breakage |
| MELONCOUNTER2 **Cn** | same | 18, 0→1, +1/−0, −3,677 (−3.13), +1,943 (0.79) | 16, 0/0, −4,270 (−5.08), **+4,730 (3.13)** | −116 % | +4,729 / −1 | no | gift → gift sharper, flip was breakage |
| MELONCOUNTER2 Mf | same | 18, 0→0, 0/0, −541 (−1.43), +554 (1.50) | 18, same | 0 % | +553 / −1 | no | loss → loss |
| NONV2 **M20** (d1-6 plate 20) | own base (= live body), 9 BAND seats (8 MELON, 1 ZERO), cash | 9, 0→1, +1/−0, +5,222 (3.17), **+22,818 (5.34)** | 8, 0→0, 0/0, +5,473 (2.96), **+26,374 (9.79)** | −3 % (flip = lucasboesen ZERO, rival −6.6 %) | +26,374 (9.8) / 0 | no | gift → gift sharper |
| NONV2 **QM20H2** | same | 9, 0→0, 0/0, +3,195 (1.52), **+21,128 (5.98)** | 9, same | 0 % | +21,128 (6.0) / 0 | no | gift → gift |
| NONV2 Q | same | 9, 0/0, +269 (0.14), +5,939 (4.04) | 9, same | 0 % | +5,939 / 0 | no | gift → gift |
| NONV2 H2 / M4 | same | H2 9, +1/−0, dtheirs −504 (−1.53); M4 9, +1/−0, +1,494 (0.95) | same (9/9 faithful) | 0 % | | no | noise → noise |
| ENGHERD1 v1 k5n8d4 | arm_B, ENGINE leg (100, not BAND142), cash vs live_eng | 100, 44→41, 0/−3, −1,070 (−2.77), +1,515 (3.29) | JC1 53, 4→2, 0/−2, −927 (−2.15), **+1,304 (2.81)** | 54 % | +4,287 (3.9) | no | gift → gift |
| ENGHERD1 v1 k8n12d5 | same | 100, 0/−3, −1,182 (−1.88), +4,639 (7.06) | 53, 0/−2, +670 (0.90), **+5,459 (6.47)** | 38 % | +8,443 (6.2) | no | gift → gift |
| ENGHERD1 v2 h5n8d4 / h8n12d5 / h3n8d5 (doc table K5N8D4 / K8N12D5 / K3N8D5) | same | dtheirs +1,551 (3.44) / +5,107 (7.74) / +1,075 (2.33); flips −3/−4/−2 | JC1 52/54/54: **+1,225 (3.50) / +6,455 (7.05) / +887 (3.00)**; flips −2/−2/−1 | 59 / 32 / 55 % | +4.3k / +9.3k / +3.7k | no | gift → gift |
| ENGHERD1 v1 k3n8d3 / v2 h3n8d3 (doc v2 K3N8D3) | same | dtheirs +542 (2.01) / +724 (2.54); flips 0 | JC1 54: +131 (0.45) / +398 (1.14); flips 0, dours t −0.75 / +0.59 | 87 / 70 % | | no | "gifts" → **not a gift on faithful seats**, but 0 flips and dours ≈ 0 (bar net ≥ +4) → still NO SHIP |
| ENGPLATE1 N8D3 (best cell) | same | 100, 44→46, +2/−0, +259 (0.69), +543 (1.08) | JC1 53, 5→7, +2/−0, +735 (2.14), −27 (−0.11) | 103 % | +3,003 | no | gift-free, too small → unchanged (net +2 < bar +4; JC1 keeps dours on all seats: t 0.69) |

- **MELONGENES1: skipped, csv incompatible.** Its plate floats ran on the panel_opp_town tapes (eps ~1105xxxxx). The csv is keyed seed/opponent/seat, with no BAND142 label and no live rival purse.
- **ENGPLATE1/ENGHERD1 are not on BAND142** (0/100 eps overlap). They are judged on their own ENGINE leg:
  - base: `S/engcheck/arm_B.csv`;
  - live purse: `S/engcontrast1/boards.tsv` live_eng.
  - Their "faithful-59" was base-only (≥ −8k). JC1 here adds arm-faithful (cash, −5 %) on the held 73.
  - The faith-59 rows reproduce the ENGHERD1 doc exactly. Its v2 table rows "K…" are the `arm_h*` files, and the v1 reference line is the `arm_k*` files.

## 2. Findings
1. **Plate gifts are price effects, and they survive JC1.**
   - MELONDUMP1 is the only cell here with rival units. Its rival sells the same units (du within ±5 % on 47/51) for +19.4k more on the faithful seats.
   - The gain comes from our own displaced supply: strawberry, milk/wool and fertilizer. Melon is −3.5k, which is the only denial.
   - NONV2 M20/QM20H2 (+21-26k, t 6-10) and ENGHERD1 (+0.9-6.5k, t 2.8-7.1) are the same shape. The plate-by-latch family stays CLOSED.
2. **The noise-board flips were mostly breakage.**
   - MELONCOUNTER2's flips all sat on noise boards; on faithful seats they drop as follows:
     - Tf +2 → +1: mhw_113480538, where the tape rival fell 85.5k → 62.4k;
     - Cf +3 → +1;
     - Cn +1 → 0;
     - NONV2 M20 +1 → 0: lucasboesen, rival −6.6 %.
   - These were the cells' only "wins". The re-judge therefore removes up-side from the rejects; it does not add any.
3. **Next-tile counters gift harder on faithful seats.**
   - Wn t 1.33 → 2.67, Sn 1.65 → 3.13, Cn 0.79 → 3.13.
   - Their broken seats carried rival losses, which diluted the gift.
4. **Tf, the "gift-free" tape cell, gifts on the full MELON cell.**
   - BANDLEG1 (3') on 49 faithful seats: dtheirs +1,400 (t 3.29), flips +1.
   - The 17-seat tape grid reads +470 (t 0.92) only because it is small.
5. **ENGHERD1 k3n8d3 (v1) / h3n8d3 (v2)** are the only cells whose "gift" label disappears on faithful seats (t 2.01/2.54 → 0.45/1.14). They still move no game (0 flips, dours t ≤ 0.6), so the verdict does not change.

## 3. Re-run recommendation (item 4): none
- No cell meets "dtheirs t < 2 and flips ≥ 0 on faithful seats" among the cells that were rejected **on dtheirs**. Those are MELONDUMP1 A/B, Wn, Tn, Sn, Cn, M20, QM20H2, Q and ENGHERD1 k5n8d4/k8n12d5/h5n8d4/h8n12d5/h3n8d5, and all of them keep t ≥ 2.54 (MELONDUMP1 B, n 5; every other cell ≥ 2.67).
- k3n8d3 / h3n8d3 meet the dtheirs half, but they were rejected on net 0 (bar +4). That is unchanged, so they are not a sign change.
- Borderline, listed so that nobody re-derives it:
  - **ENGPLATE1 N8D3** reaches dours t 2.14 with +2 flips and no gift on the JC1-53 subset.
  - JC1 rule 1 keeps dours on all seats, where it is t 0.69. The plate structurally funds about 1 tile.
  - The code lives on the engcontrast1-era branch `engplate1`, so a BAND run would need a src port.
  - **Not recommended.** If it is ever wanted, the run would be `ENGINE_PLATE_ADD=8;ENGINE_PLATE_DAY=3` ported onto PFS master (942b46cb), on the 51 BAND142 MELON seats vs `S/bandleg1/res/pfv1.csv`, 2 workers nice 10. It passes only if it shows GATE2 A/B, plus JC1 faithful dtheirs t < 2.

## 4. Commands (`S/faithrejudge1/run.sh`, about 1 min, no engine)
```
cd S/faithrejudge1 && bash run.sh
```
- **`mk_units.py`:**
  - `md <arm> <csv>`: writes their_sold from the arm's engine-commit log. It takes the arm's engine-metric du and applies it to the live leg-metric count, so faith.py's |du| ≤ 5 test sees the engine du.
  - `mc2 <cells>` / `nonv2 <cells>`: convert the grid csvs to the leg format, orig side, BAND142 labels.
- **`md_ledger.py`:** the rival price/volume split for MELONDUMP1.
- **`eng.py`:** the ENGINE-leg JC1 rows.
- **`rvl.py`:** rival-vs-live purse.
- **Outputs** are in `res/`: pair_melondump1.txt, ledger_melondump1.txt, faith_md_A_n20dump.tsv, purse_md_*.tsv, pair_meloncounter2.txt, pair_bandleg1_tf.txt, pair_nonv2.txt, pair_eng.txt, rvl.txt, and the converted csvs.
- **Purse-divergence day** (first day the rival's dawn purse differs from live, `purse_md_*.tsv`) is **not a faithfulness signal**. It is d2-3 on 31/51 seats for the PFS base too, because the shared market book moves the rival's purse as soon as our body differs from live.
