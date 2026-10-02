# JUDGECLEAN1 (2026-09-27 21:59Z-22:40Z): the BAND judge now reports rival-tape faithfulness

Replay-only. No games were run and nothing under src/ was touched. The stream re-applied the 51 live MELON replays through the pinned engine (51/51 fid True) and read the kept band replays (`S/melonaudit1/gz` = pfv1, `S/melonhybrid1/gz/{v0pfs,v56all}`). Every other number comes from existing leg CSVs.

**Verdict.**
- **The PFS base is faithful on 134/142 BAND seats:** MELON 48/51, V 78/81, ZERO 6/7, OTHER 2/3.
  - MELON is judged on the units rule. The other families are judged on the cash proxy, because no replays of them are kept.
  - On a strict reading (the rival's farm is identical to live until at least d10) MELON is 34/51.
- **No past ship/reject verdict flips on the faithful subset.** This covers 17 arm cells from MELONHYBRID1, MELONVOL1, BANDREJUDGE1, CARROTFILL-MELON1 and master.
  - **One kill verdict changes.** MELONVOL1 `tf` was KILLED as a gift at dtheirs t 2.21 (n 27). On its 26 faithful seats the t is 1.90, so the kill would not have fired. It was not a ship either way: soft t +0.88, +1 flip.
  - **V56 (v56all):** 75 % of its Σdtheirs sits on broken seats. It still passes GATE2 A and B on its 27 faithful seats (dtheirs −9.1k, t −6.4; flips +8/−1).
  - **MELONHYBRID1 v0pfs:** its all-seat dtheirs of +5.0k (t 1.3) is the net of a −276k breakage sum and a real rival gain. On faithful seats the gain is +14.4k (t 8.4), so the NO SHIP is sharper.
- **Recommended rule (JC1):**
  - Keep GATE2's W, flips, soft win, dours and family Δθ (branches A and B) on **all** seats.
  - Judge every **dtheirs** decision on **faithful** seats only: gift rule, MELON kill, denial claims.
  - Add a **breakage guard.** If the arm keeps the rival tape faithful on fewer seats than the base by more than max(3, 10 % of seats run), the arm must also pass GATE2 A or B on the faithful subset.
  - Why not faithful-only everywhere: BAND at the faithful count lowers power for +2 flips/100 on all legs from 0.93 to ~0.90, and for BAND-only from 0.42 to ~0.31-0.35. The transfer-fail false pass rises from 0.075 to 0.10-0.12.
- **Correction to MELONBODY1.** Its "tape rival vs its LIVE purse" used `live[1]`, which is our live purse on the 29 seat-0-tape MELON seats. The right index is `live[tape_seat]`:
  - V56: **−22.6k (t −6.5)**, not −15.1k;
  - PFS: **−3.2k (t −3.4)**, not +4.2k;
  - v0pfs: +1.8k, not +9.3k.
  - The direction and the verdict stand: V56 breaks the tape far more than PFS. Its clean-11 subset was defined V56 vs PFS and is unaffected.

## 1. Harness (`S/judgeclean1/`)
**`livetrace.py`** (engine, 51 MELON seats, ~4 min at 2 workers)
- Re-applies each LIVE replay (`S/bandleg1/gz` or `S/livewatch*/gz`, 142/142 found) with the MELONHYBRID1 `trace.py` hook. It writes the live rival's engine-committed SELL units per item and its purse to `res/live_units.tsv`. Fidelity is 51/51.
- Walks each kept replay against live step by step and records the first step where the tape rival's farm (money excluded) or its private inventories/shed/seeds differ → `res/diverge_live.tsv` (arm, label, day, hour, field).

**`units_sold.py`**
- Computes rival units sold with the **leg's own metric** (`S/melonvol1/units.py` `sold()`: SELL orders clipped to the shed) for live, pfv1, v0pfs and v56all.
- Output `res/units_sold.tsv`.
- Matches `S/melonvol1/res/base_units.csv` their_sold on 51/51.

**`faith.py <leg.csv> [arm] [src]`** → `res/faith_<arm>.tsv`. Columns: label, fam, faithful, basis, rival_du_pct, rival_cash_pct, diverge_day, our_seat, ours, theirs, live_theirs, rival_units, live_units.
- **units basis** (the MELONSWAP1 FAITH rule): faithful iff |rival_du_pct| ≤ 5 and theirs ≥ 0.5 × the live rival purse.
  - The units come from the csv `their_sold` column (MELONVOL1 and CARROTFILL legs) or from a kept replay (pfv1/v0pfs/v56all).
- **cash basis** (no units kept, e.g. `S/bandleg1/leg.py` deletes its replays): faithful iff rival_cash_pct ≥ **−5 %**, which is `JC_CASH_LO`, calibrated in §2.
- **Cross-check against engine-committed units:** agreement 49/51 (pfv1), 49/51 (v0pfs), 47/51 (v56all) (`res/diag.txt`).

**`pair_faith.py`** has the MELONVOL1 `pair.py` interface. For each cell it prints an ALL row and a FAITHFUL row (base AND arm faithful):
- W, flips, dours (t), dtheirs (t), soft t;
- BAND soft family Δθ (SE, z) with GATE2 branch A and branch B (band-only);
- the **breakage share** = the part of Σdtheirs carried by unfaithful seats.

**Usage (one line):** `cd S/<stream> && python3 ../judgeclean1/pair_faith.py <cells...>`
- Cells are `res/<cell>.csv` or csv paths.
- `PF_BASE=<base.csv>` changes the base (default `S/bandleg1/res/pfv1.csv`).
- `PF_GATE=MELON`: seats outside the family count as base.

## 2. Cash proxy calibration (`res/calib.txt`)
The proxy "rival_cash_pct ≥ CASH_LO" is scored against the units rule on 486 band (arm, seat) pairs where units are known, 430 of them faithful. Those arms are pfv1, v0pfs, v56all, the 4 MELONVOL1 cells and the 3 CARROTFILL cells.

| CASH_LO | TP | FP | FN | precision | recall | accuracy |
|---|---|---|---|---|---|---|
| −3 % | 327 | 6 | 103 | 0.98 | 0.76 | 0.78 |
| **−5 %** | 374 | 7 | 56 | **0.98** | **0.87** | 0.87 |
| −10 % | 394 | 18 | 36 | 0.96 | 0.92 | 0.89 |

- Precision stays high (0.98): a seat the proxy keeps is almost always truly faithful.
- The cost is recall. The proxy drops about 1 in 8 faithful seats, and those are seats where price denial pushes the rival below −5 %. So on cash-basis arms the faithful dtheirs is **conservative** (slightly less negative).
- **On MELONSWAP1 (top team vs PFS, a large body change) precision is only 0.75.** Use the units basis whenever an arm keeps replays or a their_sold column.

## 3. Is the PFS base itself faithful? (`res/faith_pfv1.tsv`, `res/diag.txt`)
| family | seats | faithful | basis | notes |
|---|---|---|---|---|
| MELON | 51 | **48** | units | strict (farm == live until ≥ d10): 34 (never diverges 22, d10-19 10, d20+ 2); broken: chungkuangwen_114121343 (du −16 %, d7), mhw_113480538 (−32 %, d9), sidazuo_113430197 (−5.2 %, d9) |
| V | 81 | **78** | cash | drizlo_114109602 −6.2 %, offhand_113431194 −5.6 %, yizhou_113294919 −6.4 % |
| ZERO | 7 | **6** | cash | lucasboesen_113352913 −6.4 % |
| OTHER | 3 | **2** | cash | evilmango_113255966 −5.0 % |
| **all** | 142 | **134** | | the live body (master = vrp10) scores 140/142 (cash) |

Units-rule counts by body on MELON, with the strict "clean until ≥ d10" count in brackets:

| body | units-faithful | clean until ≥ d10 |
|---|---|---|
| pfv1 | 48/51 | 34 |
| v0pfs | 40/51 | 21 |
| v56all | 28/51 | 7 |

- The rival's live purse vs its tape purse is −3.2k (t −3.4) under pfv1, +1.8k under v0pfs and −22.6k (t −6.5) under v56all.
- **A farm divergence is not a unit break.** Most early divergences are a single weed or tile timing that the rival's later ops absorb. Of v0pfs's 25 d0-4 divergences, 15 stay within ±5 % units.

## 4. Arm table: ALL seats vs FAITHFUL seats (`res/pair_*.txt`)
Soft Δθ z is GATE2 branch A. "G2" means band-only branch A or B.

| stream / arm | base | basis | ALL: n, W b→a, flips, dtheirs (t), soft dth z, G2 | FAITHFUL: n, W, flips, dtheirs (t), z, G2 | breakage share of Σdtheirs | verdict change |
|---|---|---|---|---|---|---|
| MELONHYBRID1 v0pfs | pfv1 | units | 51, 14→9, +5/−10, +5,025 (+1.26), −1.94, fail | 37, 8→2, +0/−6, **+14,377 (+8.36)**, −18.9 (clamped), fail | −108 % (broken seats −276k) | no (NO SHIP sharper) |
| MELONHYBRID1 v56all (V56) | pfv1 | units | 51, 14→31, +20/−3, −19,351 (−5.78), +4.40, PASS | 27, 5→12, +8/−1, **−9,082 (−6.39)**, +2.44, PASS | **75 %** | no (real edge ≈ half) |
| MELONVOL1 tf | pfv1 | units | 27, 4→5, +1/−0, +776 (**+2.21**, KILLED gift), +0.93, fail | 26, 3→4, +1/−0, +647 (**+1.90**), +0.90, fail | 20 % | **kill would not fire**; ship verdict unchanged |
| MELONVOL1 rf | pfv1 | units | 51, 14→12, +1/−3, +172 (+1.41), −2.00, fail | 48, +1/−3, +165 (+1.27), −1.95, fail | 10 % | no |
| MELONVOL1 cr | pfv1 | units | 51, 14→13, +0/−1, −65 (−0.63), −0.69, fail | 48, +0/−1, −105 (−1.00), −0.61, fail | −52 % | no |
| MELONVOL1 wr | pfv1 | units | 51, 14→13, +0/−1, +177 (+1.18), −1.71, fail | 48, +0/−1, +178 (+1.12), −1.59, fail | 5 % | no |
| BANDREJUDGE1 a (NONV4-a2, MELON-gated) | pfv1 | cash | 142, 91→89, +1/−3, +550 (+1.65), +0.24, fail | 129, 81→78, +0/−3, **+790 (+4.10)**, −1.10, fail | −30 % | no (gift sharper) |
| BANDREJUDGE1 b (MELONCOUNTER2-Cf, gated) | tfoff | cash | 36, 3→4, +2/−1, +1,730 (+2.16) KILL, −1.53, fail | 35, 2→4, +2/−0, +1,646 (+2.01), −1.12, fail | 7 % | no (kill holds) |
| BANDREJUDGE1 c (CARE_FED_ON) | pfv1 | cash | 44, 11→10, +0/−1, −285 (−3.50), −0.04, fail | 38, 8→8, 0/0, −256 (−2.97), −0.10, fail | 23 % | no |
| BANDREJUDGE1 e (MELONVETO_POST_ON) | pfv1 | cash | 51, 14→15, +1/−0, +5 (+0.09), +0.20, fail | 44, 9→10, +1/−0, −9 (−0.17), −0.09, fail | n/a (Σ≈0) | no |
| BANDREJUDGE1 f (VRPREPAIR1 100,4) | pfv1 | cash | 142, 91→92, +1/−0, +23 (+1.22), −0.03, fail | 130, 81→82, +1/−0, +22 (+1.07), −0.01, fail | 12 % | no |
| CARROTFILL-MELON1 c17_3 | pfv1 | units | 51, 14→13, +1/−2, +79 (+1.26), −0.57, fail | 48, +1/−2, +58 (+0.98), −0.45, fail | 30 % | no |
| CARROTFILL-MELON1 c17_8 | pfv1 | units | 51, 14→13, +1/−2, +78 (+1.26), −0.57, fail | 48, +1/−2, +58 (+0.98), −0.45, fail | 30 % | no |
| CARROTFILL-MELON1 c20_8 | pfv1 | units | 51, 14→13, +1/−2, +72 (+1.16), −0.36, fail | 48, +1/−2, +51 (+0.87), −0.24, fail | 33 % | no |
| master (vrp10) vs PFS | pfv1 | cash | 142, 91→83, +2/−10, +1,569 (+4.27), −5.34 | 133, 82→77, +2/−7, +1,126 (+3.62), −3.71 | 33 % | no (the PFS ship holds on faithful seats) |

**Notes on the table.**
- **CARROTFILL-MELON1** was read at 22:15Z while that agent was still running, 51/51 rows per cell.
- **BANDREJUDGE1's GATE2 B also used V legs** (pooled). The band-only B shown here is stricter, and no BAND verdict differs.
- **Breakage share below 0 or above 100 %** means the broken seats move dtheirs in the opposite direction to the total.
- **"clamped" (v0pfs z −18.9):** the MELON win rate hits 0 in the family formula, so the bootstrap SE collapses.
- **Breakage-guard triggers (JC1 §5):**
  - v56all: 28 faithful vs the base's 48;
  - v0pfs: 40 vs 48;
  - CARE_FED_ON (c): 38 vs 43.
  - v56all passes on its faithful subset. The other two fail anyway.

## 5. Power, and the rule
GATE2 power model (`S/gate2/power.py`, `BANDN` = the number of BAND seats kept, nsim 1000, MC SE ≈ 0.01):

| BAND seats | null | +2 flips/100 all legs | +2 BAND-only | transfer fail (false pass) |
|---|---|---|---|---|
| 142 (GATE2 doc, nsim 2000) | 0.038 | **0.928** | 0.418 | 0.075 |
| 129 (≈ faithful count of a PFS-like arm) | 0.040 | 0.903 | 0.314 | 0.122 |
| 107 (≈ 75 %, a body change like v0pfs) | 0.032 | 0.896 | 0.347 | 0.096 |

**What faithful-only would cost:**
- It keeps the all-leg power at about 0.90, which is borderline against the ≥ 0.9 target.
- It costs about 0.08-0.10 on the BAND-only (MELON-cell) path, which is already underpowered.
- It weakens the transfer-fail guard.
- The model is pessimistic in one respect: it does not credit that broken seats add noise to dtheirs. For arm a, the faithful subset's soft SE fell from 8.3 to 6.3.
- But W and soft-win are our own outcome and are only mildly contaminated. V56's per-seat flip rate is +33 % on all seats vs +26 % on faithful seats. So they do not need the cut. dtheirs is where breakage lives: 75 % for V56 and 5-33 % for PFS-like arms.

**Rule JC1 (recommended for GATE2 on BAND):**
1. W, hard flips, soft win, dours, family Δθ and GATE2 branches A/B: **all seats**, unchanged.
2. **dtheirs on faithful seats only** (base AND arm faithful, `pair_faith.py` FAITHFUL row) for every rival-purse decision:
   - the GATE2 gift rule's BAND part;
   - the MELON kill rule (dtheirs t ≥ 2);
   - any "denial" or "gift" claim in a stream doc.
   - Report the breakage share next to it.
3. **Breakage guard.** Let n_f(arm) be the arm's faithful seat count and n_f(base) the base's. If n_f(arm) < n_f(base) − max(3, 0.10 × n_run), GATE2 A or B must also pass on the FAITHFUL row.
4. **Units basis whenever possible.** Legs should add the `their_sold` column (MELONVOL1 `leg.py` does this) or keep replays. Otherwise the −5 % cash proxy applies (precision 0.98, recall 0.87).

## 6. Exact commands (`S/judgeclean1/run.sh`)
```
cd S/judgeclean1
nice -n 10 python3 livetrace.py 2 MELON > res/livetrace.log 2>&1      # live-tape engine trace + divergence (51 seats, ~4 min)
nice -n 10 python3 units_sold.py MELON                                 # leg-metric rival units: live/pfv1/v0pfs/v56all
python3 faith.py ../bandleg1/res/pfv1.csv pfv1                         # -> res/faith_pfv1.tsv (and every arm, see run.sh)
python3 calib.py > res/calib.txt; python3 diag.py > res/diag.txt
python3 pair_faith.py ../melonhybrid1/res/v0pfs_melon.csv ../melonhybrid1/res/v56all_melon.csv
(cd ../melonvol1 && python3 ../judgeclean1/pair_faith.py tf rf cr wr)
(cd ../bandrejudge1 && PF_GATE=MELON python3 ../judgeclean1/pair_faith.py a && python3 ../judgeclean1/pair_faith.py c e f)
(cd ../bandrejudge1 && PF_BASE=../bandleg1/res/tfoff.csv PF_GATE=MELON python3 ../judgeclean1/pair_faith.py b)
(cd ../carrotfillmelon1 && python3 ../judgeclean1/pair_faith.py c17_3 c17_8 c20_8)
BANDN=129 python3 ../gate2/power.py 1000 > res/power_band129.txt
```
