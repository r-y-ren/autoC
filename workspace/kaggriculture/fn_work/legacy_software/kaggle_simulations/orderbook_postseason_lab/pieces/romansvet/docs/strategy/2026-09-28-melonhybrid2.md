# MELONHYBRID2 (2026-09-28 22:47Z-23:25Z, box clock): the d0 h1 handover. The gate can be built, the arm cannot

**Verdict: NO SHIP, and there is no gated bot.**
- **The gate works.** A d0 h1 gate separates MELON from V perfectly: `rival money at our d0 h1 <= 2,550` fires on 49/51 MELON seats and 0/81 V seats.
  - It also fires on all 7 ZERO seats, so MELON precision is 49/56 = **0.875**. That is under the 0.90 bar, so the gate as specified is **not buildable**.
  - The MELON-vs-V split itself is clean.
- **The arm fails.** Hybrid (c) lets PFS play d0 h0 only and hands every step from d0 h1 to the V56 kernel. On the 51 MELON seats it goes **17/51**, against PFS 14 and V56 31.
  - Every win it gains over PFS comes from rival-tape breakage.
  - On the 18 JC1-faithful seats it goes **0/18** (PFS 6/18), with Δours −39.0k (t −8.9) and Δtheirs **+30.0k (t 6.9)**.
- **Why the handover breaks the kernel.** The kernel's d0 is an open-loop script.
  - At h1 it hires 5 and buys 2 cows and 2 sheep whatever PFS already did at h0.
  - PFS has already spent 1,602 coins at h0 (53 wheat and 4 hires; V56 spends 140 there), so cash falls to about 86.
  - Every one of its 12 melon-seed orders later on d0 then fails. The farm has 0.8 melon tiles and 2.4 plants at the d1 dawn, against V56's 12 and 20.
- **Q3 not triggered** (17 < 25). The V seats and ZERO seats were not run.

## Harness
- **Runner:** `S/melonhybrid2/hybrid.py` is S/melonhybrid1/hybrid.py with one extra mode.
  - Everything else is the same S/bandleg1 harness: BAND142 tapes, the original seat, pinned seed and town, SAFETY_S 1e9, REPAIR_MS 1e7, actTimeout 600, and master src = vrp12_pfs.
  - The new mode, `HY_MODE=pfs0v56`, runs PFS at engine step 0 (d0 h0) and the V56 kernel (`S/v56leg/main.py`) at every step ≥ 1.
  - The kernel's first call is at d0 h1, so it plans its own d0 from h1 on the farm PFS left. PFS is never called again. No src edit was needed, so no worktree and no branch.
- **Controls (`res/ctl_*.csv`):** on 2 MELON seats (highfrequencyf, kuengo), `off` = pfv1 2/2 and `v56all` = bandfamily1 v56 2/2, byte-identical.
- **Q1:**
  - `q1tape.py` decodes each rival's `_TAPE` (S/pool1/bank) for h0-h5, giving `res/q1_tape.csv`.
  - `q1vis.py` steps the real engine (board seed) for 3 hours. Our seat plays PFS's recorded h0 and the rival plays its tape. It logs the rival's **visible** fields at our h1-h3 (money, hires_today, hands, tiles), giving `res/q1_vis.csv`. Seeds, shed and animals are private.

## Q1. Separability at d0 h1 (`res/q1_tables.md`)
**What the rivals do at d0 h0.**

| rival d0 h0 order (mean, seats >0) | MELON (51) | V (81) | ZERO (7) | OTHER (3) |
|---|---|---|---|---|
| melon seed | 1.8 (16) | 0 (0) | 0 (0) | 0 (0) |
| hires | 2.2 (25) | 0 (0) | 3.9 (7) | 0 (0) |
| cows | 1.3 (44) | 0 (0) | 2.1 (7) | 0 (0) |
| sheep | 1.4 (28) | 0 (0) | 3.0 (7) | 0 (0) |
| wheat bought / sold | 10.6 / 0.4 | 10.0 / 5.6 | 26.1 / 20.6 | 31 / 26 |

- **V rivals** open with the V56 script: buy 20 wheat, sell 15 wheat, buy 1 wheat seed. The herd and the hires come at h1.
- **MELON rivals** buy herd, hires and some seed at **h0**.
- **At h1 nothing is planted anywhere:** rival melon tiles are 0 on 142/142 seats. The tell is therefore **cash**.

**Rival money at our d0 h1, seats per family:**

| money at h1 | MELON | V | ZERO | OTHER |
|---|---|---|---|---|
| 0-500 | 19 | 0 | 7 | 0 |
| 500-1,000 | 7 | 0 | 0 | 0 |
| 1,000-2,000 | 0 | 0 | 0 | 0 |
| 2,000-2,550 | 23 | 0 | 0 | 0 |
| 2,550-2,800 | 0 | 4 | 0 | 0 |
| 2,800-2,950 | 2 | 61 | 0 | 3 |
| > 2,950 | 0 | 16 | 0 | 0 |

**Best threshold.** The gate `money <= X` works for any X in [2,492, 2,599).

| | MELON | V | ZERO | OTHER |
|---|---|---|---|---|
| fires | **49/51** | **0/81** | 7/7 | 0/3 |

- **Precision on MELON is 0.875 and recall is 0.961.**
- **The two MELON misses** (leaveyou, aildarsloperna) open V-style (money 2,854 and 2,904 at h1).
- **ZERO confound.** Six of the 7 ZERO seats are one clone (money exactly 488, 4 hires). An exact-value carve-out would lift precision to 49/50, but that is an in-sample fingerprint, not a rule.
- **Hires at h1 do not help.** hires_today is 0 on 26 MELON seats and all 81 V seats.
- **Generalisation caveat.** The 51 MELON seats come from 40 teams but show only 20 distinct h1 money values. The tell is a clone-opening fingerprint.
- **Verdict:** MELON vs V is separable, but against the full band **precision is 0.875 < 0.90, so the gate is not buildable as specified**.

## Q2. Hybrid (c) on the 51 MELON seats (`res/pfs0v56_melon.csv`, `res/sum_pfs0v56_melon.md`, `res/faith_*.txt`)
The kill rule was checked at n = 28: hybrid W 7 vs PFS 4, so the run was not killed and went to 51/51 (0 errors).

| rows | n | **hybrid W** | PFS W | V56 W | flips vs PFS | Δours vs PFS (t) | Δtheirs vs PFS (t) | flips vs V56 | Δours vs V56 (t) | Δtheirs vs V56 (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| MELON all | 51 | **17** | 14 | 31 | +12/−9 = +3 | −27,570 (−7.9) | −8,878 (−1.5) | +6/−20 = −14 | −35,214 (−9.5) | +10,473 (1.9) |
| rival plate ≤ 8 | 5 | 2 | 5 | 3 | −3 | −43,014 (−4.1) | −10,409 | +1/−2 | −33,667 | +800 |
| rival plate 9-11 | 21 | 9 | 7 | 13 | +7/−5 | −28,196 (−5.8) | −14,381 (−1.6) | +3/−7 | −36,604 (−8.5) | +10,364 (1.2) |
| rival plate ≥ 12 | 25 | 6 | 2 | 15 | +5/−1 | −23,955 (−4.5) | −3,949 (−0.7) | +2/−11 | −34,356 (−5.7) | +12,499 (2.0) |
| **JC1 faithful vs PFS** (units basis, 18/51) | 18 | **0** | 6 | – | +0/−6 | −39,004 (−8.9) | **+30,041 (6.9)** | – | – | – |
| **JC1 faithful vs V56** (base = melonhybrid1 v56all, 14/51) | 14 | **0** | – | 8 | – | – | – | +0/−8 | −35,730 (−7.9) | **+35,486 (9.3)** |

- **Breakage.** The hybrid rival's purse ends below 0.75× PFS's in **16/51** seats (open-loop tape breakage). Against PFS, the unfaithful seats carry −994k of the −453k total Δtheirs (219 %).
- **All 12 up-flips vs PFS are on unfaithful seats.** On faithful seats the arm loses every seat PFS won and gifts the rival +30k.
- **GATE2:** band A and B both fail.

### What PFS does at h0, and what the kernel loses (`res/h0_actions.txt`, `res/trace_h2.txt`, `res/trace_handover.md`)
- **Our d0 h0 orders are identical on all 51 seats:**
  - PFS: farmer NORTH, BUY_PRODUCT WHEAT 53, 4 × HIRE.
  - V56: PASS, BUY_PRODUCT WHEAT 20, SELL WHEAT 15, BUY_SEED WHEAT 1.
  - Cash after h0: PFS **1,398**, V56 2,860.
- **The kernel's h1 block is scripted.** In the hybrid it is byte-identical to its own game: 5 × HIRE, 2 cows, 2 sheep. The block ignores the 4 hands and the 1,602 coins PFS already committed.

| mean over 51 MELON seats | hybrid (c) | V56 kernel | PFS |
|---|---|---|---|
| cash after h1 orders (obs h2) | **86** | 1,048 | 214 |
| hands on d0 | **9** | 5 | 4 |
| animals after h1 | 2.9 (one buy unaffordable) | 4.0 | 6.0 |
| d0 melon-seed orders | 12 | 12 | 0 |
| melon tiles at d1 dawn | **0.8** (0 on 44/51) | 12.0 | 0.0 |
| plants at d1 dawn | **2.4** | 20.0 | 19.0 |
| cash at d1 dawn | 6.8 | 17.7 | 213.5 |
| melon tiles at d7 | 0.3 | 12.0 | 2.4 |
| herd at d10 | 8.0 | 13.7 | 11.0 |
| final ours / theirs | 74,100 / 99,403 | 109,314 / 88,930 | 101,671 / 108,281 |

**Mechanism.**
1. PFS's h0 spends 1,602 coins (53 wheat and 4 hires, hands arriving at h1).
2. The kernel's d0 script then spends another about 1,310 at h1: 5 more hires and the herd.
3. It is left with 86 coins, so the melon and wheat seed orders it issues from h6 to h20 bounce (seed cost > cash).
4. The farm enters d1 with **no plate and no field** (2.4 plants vs 20) and 9 paid hands idle.
5. The kernel never re-plans around cash, so the V56 body inherits a farm with no d10 melon line and no wheat. Its d1-9 cash engine (shed-wheat sales) has nothing to sell.

This is the BANDFAMILY1 finding (the kernel needs its own farm) at the hour level: **even one hour of a foreign opening breaks it.**

## Q3. Not triggered (hybrid 17 < 25). Gated-bot projection from the measured cells (`res/projection.md`)
Gate: `rival money at our d0 h1 <= 2,550` → hybrid (c); otherwise PFS.

| family | n | fired | PFS W | gated W | note |
|---|---|---|---|---|---|
| MELON | 51 | 49 | 14 | 18 (+12/−8; Δours −26.2k, Δtheirs −8.9k) | hybrid measured on the fired seats |
| V | 81 | 0 | 70 | 70 | never fires |
| ZERO | 7 | 7 | 5 | not run | V56 kernel alone is 1/7 here, so the false-positive cost is up to −4..−5 W |
| OTHER | 3 | 0 | 2 | 2 | never fires |

- **All seats:** BAND142 goes from 91 to 95 with ZERO held at PFS (optimistic), or to about 91 with ZERO at the V56-kernel level.
- **Faithful seats (JC1):** the fired MELON seats go 6 → 0, i.e. **−6 flips**, Δtheirs +30k (t 6.9).
- **The apparent +4 is tape breakage.** The honest expectation is negative, so there is no gated bot.

## Verdict
- **Separability:** MELON vs V at h1 is exact on BAND142, with 0/81 V false positives. The gate fails the 0.90 precision bar only because of ZERO (0.875).
- **Hour-level handover:** it breaks the kernel. On faithful seats the hybrid is 0/18, against PFS 6/18 and V56 8/14 on its own faithful set.
- **The V56 MELON edge cannot be borrowed** at d0 h0, d0 h1 (this stream), d1 dawn (BANDFAMILY1) or d0-only (MELONHYBRID1). Taking it means playing the V56 kernel **from h0**, which needs a gate at h0. At h0 nothing of the rival is visible, so no such gate exists (RACERARM).
- **Nothing ships.** The coordinator decides.

## Rules check: V56 kernel licence
`S/v56leg/main.py` is **Apache-2.0**; its header carries the full licence text and contributor notices (lineage in 2026-09-27-melonhybrid1.md §4). It was used here only as a local judge opponent / body. Nothing from it is committed into src or shipped.

## Files
- **S/melonhybrid2/:** run.sh (`q1`, `ctl`, `melon`, `sum`; `vseats` and `zero` are defined but not run), hybrid.py, q1tape.py, q1vis.py, q1tab.py, trace2.py, addunits.py, checkpoint.txt.
- **res/:**
  - q1_tape.csv, q1_vis.csv, q1_tables.md;
  - ctl_off.csv, ctl_v56.csv;
  - pfs0v56_melon.csv (51), pfs0v56_melon_u.csv (+ their_sold);
  - sum_pfs0v56_melon.md, faith_pfs0v56_vs_{pfs,v56}.txt;
  - trace_handover.{csv,md}, trace_h2.txt, h0_actions.txt, projection.md;
  - logs.
- **Not committed:** replays in gz/pfs0v56 (18 MB).
