# GATECENSUS1: who does the KERNEL2 gate fire on?

2026-09-28, 01:31Z to 02:00Z (box clock). Analysis only; no src change, merge or upload.

**What was tested.** The candidate vrp13_v56gate plays an idle step 0. At step 1 it hands the game to the V56 kernel if the rival's cash is ≤ 2,550; otherwise it plays PFS shifted one hour.

## Verdict
- **No step-1 rule separates the rivals where V56 wins from the ENGINE-class rivals where it loses.** The reason is the 2,467 opener.
  - The opener is buy 1 cow + buy 5 wheat. At h1 it is byte-identical for three groups: the band MELON rivals (42 of BAND2's 276 seats, 18 of them in BAND142), the faithful59 ENGINE/BAND tapes (17 seats), and one V tape.
  - Every visible field matches: money, hires, hands, farmer, tiles, quadrants, and every market inventory and price delta.
  - It also stays identical through d1 dawn: 6 melon and about 15 plantings in all three groups (`res/timeline.tsv`).
  - V56 against PFS on that one vector:

    | group | paired seats | W PFS → V56 | mean dmargin |
    |---|---|---|---|
    | band MELON | 34 | 7 → 20 | +22.5k |
    | faithful ENGINE/BAND | 14 | 4 → 1 | −2.2k (BAND) / −12.7k (ENGINE) |

  - The 14 faithful seats include 6 new engine games (`res/eng6_on.csv`). V56 went 0/6 there and PFS 0/6, mean dmargin ≈ 0.
- **Best rule: R2 = cash ≤ 2,550 minus the exact values {433, 1033} (ZERO) and {19, 303, 1040, 1467} (ENGINE).**
  - It keeps 49/49 BAND142 MELON fires (107/107 across BAND2 MELON).
  - ENGINE fires drop from 41/59 to 17/59; those 17 are exactly the 2,467 seats.
  - ZERO fires drop from 22 to 5 (27, 43, 283 remain).
  - V fires: 8 of 184 (unchanged).
- **The MELON gain survives only if PFSH0MERGE1 succeeds** (variant U below: unfired seats play unshifted PFS).
  - With U, R2 keeps the full MELON gain: BAND142 +19, faithful59 −3 at soft t −1.66. That clears the GATE2 guard (−2) but is still negative, and all −3 is the 2,467 cluster.
  - With the one-hour shift (variant S), no rule avoids the faithful59 kill. Firing on no ENGINE seat at all (R3) still gives soft t −2.15, because the shift alone takes the unfired faithful seats from 10 wins to 5.
- **The 2,467 decision is a bet on the population, not a tell.**
  - Dropping 2,467 (R3) makes faithful59 exactly neutral under U, but costs BAND142 7 flips: +19 becomes +12.
  - 2,467 is the most common MELON h1 in our live games (47/149).
  - Among LB top-50 teams, the 2,467 opener is used by ranks 8, 9, 11, 12, 14, 17, 18, 20, 27, 30 and 44.

## 1. Census (`census.py`, `agents.py`; `res/census.tsv` 1,844 rows, `res/agents.tsv` + `agents_retry.tsv` 540)
- **Method.** Each vector is the rival's visible step-1 state after one engine step of [our no-op, rival's recorded h0]. It covers money, hires_today, hands, farmer, building tiles, quadrants, and market inventory/price deltas per item.
  - Tapes use the board seed.
  - Replays are stream-parsed up to steps 0-24, which also gives the rival's melon/plant tiles at d1 dawn as recorded.
  - Code agents are called once on the step-0 obs.
- **Validation (`res/validate.txt`).** The census matches earlier results exactly:
  - ZEROGATE1 k2 live values: 261/261;
  - ZEROGATE1 BAND142: 142/142;
  - GATE2LEGS1 faithful `opp_money_h1`: 37/37.
- **Sources:**
  - BAND2 276 (BAND142 + HOLD104 + NEW2);
  - gate2legs1 faithful59 (engcheck 09-11, opp_class ENGINE 23 / BAND 36) and tapes50;
  - 1,201 real episodes under S/*/gz. That is 1,459 rival seats: livewatch17-21, finalslot1, melonswap1, toploss1, lossmap17, bandhold1 and bandleg1. 464 of them carry our family label.
  - 540 S/pool1 bank entries: 37 public code agents plus the tape pools.
- **Not covered:** the gate2legs1 clone20 tapes (V48 clone) use a different tape format and are V-class. dev/held/FRESH are all S/v56leg/main.py = 2,857/0/0.

## 2. Class × h1-cash, with measured V56 vs unshifted PFS on the same seat (`res/table_class_cash.md`, `res/seats.tsv`)

| class | h1 cash | n | fired | paired | W PFS → V56 | mean dmargin |
|---|---|---|---|---|---|---|
| MELON (band) | 0-60 | 30 | 30 | 20 | 7 → 14 | +23.2k |
| MELON | 61-350 / 451-1000 | 24 | 24 | 13 | 4 → 10 | +27-49k |
| MELON | 2,001-2,466 (2,339/2,046/2,440) | 9 | 9 | 6 | 0 → 4 | +9.9k |
| MELON | **2,467** | 42 | 42 | 34 | **7 → 20** | **+22.5k** |
| ENGINE/BAND (faithful59) | 19 (5 hires, 1 tile) | 10 | 10 | 6 | 1 → 1 | −1.0k |
| ENGINE/BAND | 303 (3 hires) | 9 | 9 | 0 | – (PFS 2/9) | – |
| ENGINE/BAND | 1,040 / 1,467 | 5 | 5 | 5 | 2 → 0 | +37.8k (1,040: −52k → −11k, still L) / −10.7k (1,467) |
| ENGINE/BAND | **2,467** | 17 | 17 | 14 | **4 → 1** | **−6.7k** |
| ENGINE/BAND | ≥ 2,614 | 18 | 0 | – | – | – |
| ZERO | 433 | 16 | 16 | 10 | 7 → 1 | −19.5k |
| ZERO | 27 / 43 / 283 / 1,033 | 6 | 6 | 4 | 2 → 3 | – |
| V (band + tapes50) | ≥ 2,551 / < 2,551 | 176 / 8 | 8 | 2 | 0 → 1 | – |

Ratings are not visible to the bot. The 2,467 rivals in faithful59 were rated 2,990-3,046 at 09-11; the band's 2,467 rivals are rated 2,576-2,782.

## 3. Gate rules (`rules.py`, `res/rules.md`)
**How to read the table:**
- Counts are over all tape rivals.
- "live" is our 464 labelled real games.
- The projection gives each fired seat its measured V56 row. Unfired seats get the measured shifted-PFS row (S) or the unshifted PFS row (U).
- Flips are counted against the unshifted PFS base. Soft t is at seat level (s = 3,000).
- The R0 S row reproduces BANDGATED1 exactly (91 → 102, +25/−14) and GATE2LEGS1's faithful kill (17 → 7, +2/−12).
- Faithful S only covers seats that have a shifted row: 32 of 59 for R2, 18 for R3.

| rule | band MELON kept (116) / BAND142 (51) | ENG fired /59 | ZERO /22 | V /184 | live flagged | BAND142 S | BAND142 U | faithful59 S | faithful59 U |
|---|---|---|---|---|---|---|---|---|---|
| R0 cash ≤ 2,550 (candidate) | 107 / 49 | 41 | 22 | 8 | 180/464 (39 %) | 91→102 **+11** | 91→105 +14 | 17→7 −10 (t −2.71) | 17→12 −5 (t −2.03, n43) |
| R1 R0 − {433,1033} | 107 / 49 | 41 | 5 | 8 | 160 (34 %) | 91→104 +13 | 91→110 +19 | 17→7 −10 (t −2.71) | 17→12 −5 (t −2.03) |
| **R2 R1 − {19,303,1040,1467}** | **107 / 49** | **17** | 5 | 8 | 158 (34 %) | 91→104 **+13** | 91→110 **+19** (t 4.37) | 14→6 −8 (t −2.46, n32) | 20→17 **−3 (t −1.66, n56)** |
| R3 R2 − 2,467 | 65 / 31 | 0 | 5 | 6 | 110 (24 %) | 88→94 +6 (n124) | 91→103 +12 | 10→5 −5 (t −2.15, n18) | 20→20 0 |
| R4 cash ≤ 2,450 − ZERO − ENG | 64 / 30 | 0 | 5 | 6 | 108 (23 %) | +6 | +12 | as R3 | as R3 |
| R5 R1 − (5 hires & 1 tile) | 105 / 48 | 31 | 5 | 8 | 156 (34 %) | +13 | +19 | −10 | −5 (t −2.12) |
| R6 cash ≤ 2,000 − ZERO − ENG | 55 / 26 | 0 | 5 | 3 | 92 (20 %) | +4 | +10 | as R3 | 0 |
| R7 cash ≤ 1,000 − ZERO − {19,303} | 54 / 26 | 0 | 5 | 2 | 88 (19 %) | +4 | +10 | as R3 | 0 |

**BAND2-276 (partial arm rows):**
- R0: U +22, S +20.
- R1/R2: U +30 (146 → 176, n232), S +25.
- R3: U +20.

**Live flag share by class under R2:** MELON 136/149, ZERO 5/25, V 15/285, OTHER 2/5.

**Caveat: the exact values are fingerprints.** 19/303/1,040/1,467 are the 09-11 engcheck tapes. In the current top-50 only two appear: THIRD FARM CLUB (rank 22) at 19/5/1 and elmo (rank 29) at 1,467/0/1. 303 is never seen live. So R2's live effect is small, and the live question is 2,467.

## 4. The field we must beat (`res/top50.md`; LB 09-27 09:46Z, 562 top-50 rival seats, 41 teams)
- **Nearly the whole top 50 opens under 2,550.** R0 fires on 547/562 (97 %), and on 251/252 top-5 seats.
- **Top-5 h1 openers:**
  - DSM (#1): 967/0/0 (53/55);
  - Boey (#2): 2,339/5/0;
  - M & M & P & Q (#3): 1,967/0/0 and 967/0/0;
  - Majkel1337 (#4): 1,816/5/0 and 1,844/5/0;
  - Vadim Vasilenko (#5): 967/0/0.
  - #6-7 (DECEM, Mother-Goose) also open 967/0/0.
- **2,467 teams:** ranks 8, 9, 11, 12, 14, 17, 18, 20, 27, 30 and 44.
- **Only teams ≥ 2,857 (V):** #16, #41, #45.
- R2 fires on 542/562. R3 fires on 426/562; it spares only the 2,467 teams.
- **Measured V56 on these openers (band seats only):**
  - 967: n4, 0 → 2 W, +53k;
  - 2,339: n4, 0 → 3 W, +13.5k;
  - 1,816 and 1,967: never measured.
- **melonswap1 tapes:** 160 top-team MELON rivals, mostly 967, 2,467 and 2,339. PFS wins 85/160 of them. V56 has never been run on them.
- **Public code agents (`res/agents.md`):** 13/37 fire (cash 2-282). 24 open at ≥ 2,643 (V-like).

## 5. What this means for the ship decision
1. Take ZEROGATE1's {433, 1033}. Adding {19, 303, 1040, 1467} is free on BAND142 (0 MELON seats at those values) but only matters against the 09-11 tapes.
2. The faithful59 kill is **mostly the one-hour shift**, not the gate. Under U, R2 gives faithful −3 with t −1.66; under S, even a gate that never fires on ENGINE gives t −2.15. PFSH0MERGE1 decides whether any gated package can pass GATE2.
3. 2,467 is unresolvable at h1 and at d1 dawn. Keep firing on it (R2) if the live field is the band: 47/149 live MELON, V56 +13 W on 34 band seats. Drop it (R3) only if the top-10 ENGINE teams matter more than band rating.
4. **Follow-up measurement:** the gated candidate on the melonswap1 160 top-team tapes (V56 vs PFS 85/160). These are the 967/2,339/1,816/1,967/2,467 openers of the top-50, and V56 has never been run on them.

## Files
- **S/gatecensus1/:**
  - run.sh, with modes census / agents / timeline / rules / eng6;
  - census.py, agents.py, agentsum.py, timeline.py, rules.py;
  - leg.py, a copy of the gate2legs1 runner;
  - boards/faithful.json;
  - checkpoint.txt.
- **res/:**
  - census.tsv, agents*.tsv, seats.tsv, timeline.tsv, eng6_on.csv, validate.txt;
  - table_class_cash.md, rules.md, live_flags.md, top50.md, agents.md;
  - logs.
