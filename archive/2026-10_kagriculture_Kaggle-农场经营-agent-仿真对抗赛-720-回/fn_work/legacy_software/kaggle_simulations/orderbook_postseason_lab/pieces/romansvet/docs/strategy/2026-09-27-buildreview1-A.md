# BUILDREVIEW1-A (2026-09-27 17:19Z-17:57Z): quantitative review of the whole build, and the 8 holes left

**Verdict.** Top 5 is a MELON-cell problem that the build has never measured head-on.
- Where we stand: vrp10 θ 2,633, PFS +36 → ~2,669. The rank-5 bar is ~2,950.
- Reaching it needs a uniform **+20k margin per game on the 51 BAND MELON seats plus +3k on the V seats** (MELON win 27 % → 90 %). A +10k MELON shift gets only 2,765.
- For scale: the largest ship in the record is FERT_TIMING at +2,845/board. All era-B ships sum to +5,335/board.
- 0 of the 5 standard ship legs contain MELON-family rivals. 10 arm-cells (9 mechanisms) out of ~780 arms were ever judged on the BAND leg.
- No standard leg predicts live rating (ρ ≤ +0.40, n ≤ 12). Across 8 contemporaneous package pairs the judge and live agree 4 times.
- The shipped gain came from decoupled axes: router + bugfix = 77 % of era-C flips, with coupling b ≈ 0. The MELON rivals' edge is on the transfer axes: opening b −1.30, land −0.66 (MELONLOGIC1: the melon plate plus the sheep herd carry 73 % of the MELON-loss margin). The hand-lever opening, crop and land families shipped 0 of 173 judged rows.

## 0. Sources and method
- BUILD-STORY.md read in full by three extraction passes → `S/buildreview1/A_bs.tsv`: 1,117 arm×leg rows, 780 arms, every number with its BUILD-STORY line.
- Verdict tables of 261 docs parsed → `A_pairs.tsv`: 1,542 rows with Δours/Δtheirs/flips (`A_pairs.py`). Per-board, per-episode and per-opponent tables are excluded.
- Other inputs:
  - GAPREVIEW1 ledgers (B_ledger 1,132 rows).
  - Ship chain with md5 re-checked → `A_ships.tsv`: 50 uploads, 27 judge-vs-live statements with file:line.
  - Trainer census → `A_trainers.tsv`: 291 rows, ~315 arms.
  - `git log --all`: 2,105 commits, 08-21..09-27. `git worktree list`: 389, of which 130 are `agent-*`. 525 branches.
  - BANDLEG1 per-seat CSVs for the headroom model (`A_headroom.py`).
- Scripts: `A_stats.py`, `A_bs_stats.py`, `A_provenance.py`, `A_effort.py`, `A_timeline.py`, `A_headroom.py`. All are read-only over the repo. No games were run.

## 1. Arm timeline and the shipped chain
Per day (`A_timeline.tsv`). Ledger rows cover 09-10 onward. Commit and worktree days are local (+03:00).

| day | commits | docs | worktrees | ledger rows: reject (gift) / closed / ship+pkg / analysis+infra | trainer arms started | uploads (packages) |
|---|---|---|---|---|---|---|
| 08-21 | 9 | 0 | 0 | – |  |   |
| 08-22 | 4 | 0 | 0 | – |  |   |
| 08-23 | 12 | 0 | 0 | – |  |   |
| 08-24 | 18 | 0 | 0 | – |  |   |
| 08-25 | 49 | 0 | 2 | – |  |   |
| 08-26 | 42 | 0 | 26 | – | 13 |   |
| 08-27 | 29 | 0 | 16 | – | 11 | 1 (flow9_g15975) |
| 08-28 | 18 | 0 | 4 | – | 10 | 1 (flow13_g19110) |
| 08-29 | 21 | 0 | 2 | – | 12 | 1 (flow25_g135) |
| 08-30 | 27 | 0 | 0 | – | 14 | 4 (flow30d_g2520, flow38_g25, flow38_g25_drop, flow38_g25_HORIZON) |
| 08-31 | 3 | 0 | 3 | – | 6 | 3 (flow49b_g450, flow51_g900, unconfirmed) |
| 09-01 | 6 | 0 | 0 | – | 7 | 1 (flow54_g700) |
| 09-02 | 35 | 0 | 15 | – | 7 | 2 (flow58_g450, flow58_g450_split) |
| 09-03 | 79 | 0 | 24 | 0 (0) / 1 / 0 / 0 | 8 | 2 (flow58_g450_stack, flow58_g450_earlysell) |
| 09-04 | 41 | 0 | 0 | – | 11 | 2 (flow58_g450_pump, flow58_g450_slot0) |
| 09-05 | 23 | 1 | 2 | – | 8 | 1 (flow102_g280) |
| 09-06 | 40 | 0 | 31 | – | 4 |   |
| 09-07 | 0 | 0 | 0 | – | 4 |   |
| 09-08 | 10 | 1 | 6 | – | 10 |   |
| 09-09 | 51 | 33 | 18 | – | 20 | 1 (flow135_g350) |
| 09-10 | 14 | 64 | 8 | 2 (0) / 8 / 1 / 26 | 22 | 3 (flow172_g60_pair, flow172_g940_pair, flow172_g1000_pair_hr) |
| 09-11 | 17 | 89 | 1 | 13 (0) / 8 / 1 / 21 | 13 | 1 (flow193_g100_hr) |
| 09-12 | 177 | 79 | 0 | 6 (0) / 1 / 0 / 9 | 4 |   |
| 09-13 | 122 | 40 | 0 | 3 (0) / 1 / 0 / 1 | 2 |   |
| 09-14 | 139 | 42 | 0 | 15 (0) / 1 / 0 / 25 | 6 |   |
| 09-15 | 7 | 0 | 0 | – | 5 |   |
| 09-16 | 116 | 62 | 14 | 43 (2) / 16 / 7 / 25 | 4 | 4 (flow193_g100_hr_pumpof, flow193_g100_hr_lot4t1, flow193_g100_hr_lot4t1, flow193_g100_hr_lot4t1) |
| 09-17 | 201 | 59 | 14 | 36 (11) / 25 / 4 / 35 | 11 | 3 (flow193_g100_hr_lot4t1, flow193_g100_hr_lot4t1, flow193_g100_hr_ft2) |
| 09-18 | 153 | 25 | 52 | 32 (9) / 20 / 13 / 25 | 12 | 3 (flow193_g100_hr_ft2_es, flow193_g100_hr_ft2_es, flow193_g100_hr_ft2_es) |
| 09-19 | 85 | 33 | 7 | 31 (8) / 5 / 3 / 24 | 17 | 1 (res940) |
| 09-20 | 14 | 12 | 0 | 10 (3) / 0 / 0 / 2 | 8 |   |
| 09-21 | 41 | 30 | 0 | 23 (1) / 3 / 2 / 16 | 9 | 1 (res940_vpost) |
| 09-22 | 77 | 40 | 9 | 38 (6) / 10 / 12 / 19 | 3 | 4 (res940_cf, res940, res940_cfog, res940_cfog2) |
| 09-23 | 88 | 39 | 20 | 51 (6) / 8 / 4 / 23 | 7 | 2 (res940_cfog3, res940_cfog3le) |
| 09-24 | 91 | 33 | 26 | 49 (7) / 10 / 13 / 10 | 11 | 3 (res940_vrp, res940_vrp2, res940_vrp3) |
| 09-25 | 112 | 7 | 43 | 6 (0) / 1 / 3 / 8 | 6 | 1 (res940_vrp5) |
| 09-26 | 62 | 84 | 21 | 127 (17) / 39 / 12 / 58 | 3 | 2 (res940_vrp7, res940_vrp8_jit) |
| 09-27 | 72 | 44 | 14 | 25 (7) / 4 / 5 / 33 | 3 | 3 (res940_vrp9_cs, res940_vrp10_esw, res940_vrp12_pfs) |
| 09-28 | 0 | 0 | 0 | 0 (0) / 1 / 0 / 1 |  |   |

**Phases.**
- **Era A, 08-21..09-11: ES-theta hill-climb.** 180 trainer arms, 13 of them shipped. 23 uploads, from flow9 (~1,172) to B `flow193_g100_hr` (56161192, landed 2,516, peak 2,773). The judges were drawn panels (kagg2, panel24, LIVE55/62), and "no local read has ever predicted a Kaggle improvement that materialised" (2026-09-09-kaggle-calibration.md:53-58).
- **Era B, 09-12..09-21: switch campaign on POOLED180/278, BAND250 and ENGINE legs.** 9 mechanism ships worth +5,335 coins/board, 61 trainer arms (1 ship, head_940), 12 uploads.
- **Era C, 09-22..09-27: V56 legs** (dev100/held100/FRESH300/tapes50/faithful-59), then the VRP router, then BAND142 (from 09-27 13:00Z). 14 ship packages worth +195 net flips over the 5 legs, 50 trainer arms (1 ship, ESWORK g30), 15 uploads.
- **Activity peaks:** 09-17 (201 commits, 49 negative verdicts) and 09-26 (127 reject rows, 39 closed, 84 docs). 09-26 is the densest rejection day in the record; it uploaded 2 packages (vrp7, vrp8_jit).

Shipped chain since B (`A_chain.md`). The live score is the Kaggle μ at the last read before the next upload replaced the sub. θ MLE is given where a doc fits it.

| sub | package | uploaded | md5 | change (class) | live W-L (g) | live score | LB rank |
|---|---|---|---|---|---|---|---|
| 56161192 | flow193_g100_hr (B) | 2026-09-11 07:50 | adf27cb0 | theta flow193_g100 (g160 seed + 100 ES gens), hr switches unchanged (trainer) |  (628) | 2546.2 | 720 |
| 56273500 | flow193_g100_hr_pumpoff | 2026-09-16 (befo | 890b489d | OPEN_PUMP_ON True->False on B (day-0 wheat pump off) (tuning) | 41-13 (54) | 2007 |  |
| 56276165 | flow193_g100_hr_lot4t17 | 2026-09-16 (~11: | 0ff30cea | LOT4_ON, LOT4_TURN=17 (4th sell row one turn before lot 3); OPEN_PUMP_ (newrule) | 18-4 (22) | 1801.5 |  |
| 56277270 | flow193_g100_hr_lot4t17_slotprio ( | 2026-09-16 (~11: | b3c33bbf | SELL_SLOT_PRIORITY_ON (order own sells inside emitted rows) (newrule) | 105-37 (142) | 1900 |  |
| 56284867 | flow193_g100_hr_lot4t17_slotprio_f | 2026-09-16 ~17:5 | ab1acb76 | FERT_TIMING_ON (DAYS=2) + gene g12 fert_defer: fertilize only on tile  (newrule) | 71-8 (79) | 1754 |  |
| 56298238 | flow193_g100_hr_lot4t17_slotprio ( | 2026-09-17 07:51 | b3c33bbf | none: same tarball re-uploaded for a fresh first-20 draw (reupload) | 61-17 (78) | 1921.6 | ~1745 (implied; no LB  |
| 56298246 | flow193_g100_hr_lot4t17_slotprio_f | 2026-09-17 07:51 | ab1acb76 | none: same tarball re-uploaded for a fresh first-20 draw (reupload) | 124-51 (175) | 2231.9 |  |
| 56313436 | flow193_g100_hr_ft2 + ENDROUTE (FT | 2026-09-17 20:55 | 1802da15 | ENDROUTE_ON: one nine-slot sell row on day 29 last executed turn (22) (newrule) | 68-32 (100) | 2254.4 |  |
| 56323661 | flow193_g100_hr_ft2_esr (FT2+ESR) | 2026-09-18 07:07 | 6fa5fec4 | ENDROUTE2_ON + ENDROUTE2_SPLIT_ON + ENDROUTE_ROW2_ON (day-29 route fam (newrule) | 86-19 (105) | 2514.8 | 925 (09-18 12:12Z @2,4 |
| 56329775 | flow193_g100_hr_ft2_esr_wp (ESR+WI | 2026-09-18 12:12 | 65b78869 | WIDE_PICK_ON: wide-day turn-1 stationary second PICKUP (newrule) | 131-73 (204) | 2859.0 | 77 (LB 09-19 09:13Z 28 |
| 56335778 | flow193_g100_hr_ft2_esr_wp_wpf (sh | 2026-09-18 17:10 | 9df145d9 | WIDE_PICK_FREE_ON: turn-1 second pickup takes the owed kind the BUY ro (newrule) | 225-136 (361) | 2526.2 |  |
| 56370365 | res940 (theta7659 + self-play PPO  | 2026-09-19 ~19:5 | 536cf106 | RESIDUAL_ON + self-play PPO residual action head head_940 on shipped t (trainer) | 219-137 (356) | 2757.5 | 151 (LB 09-22 06:44Z 2 |
| 56421514 | res940_vpost | 2026-09-21 (~07: | 47e2088d | MELONVETO_POST_ON (K=60 flooded-melon veto re-applied after head_940) (newrule) | 71-44 (115) | 2312.2 |  |
| 56464803 | res940_cf | 2026-09-22 12:55 | 79b6ed12 | CARE_FILL_ON (switch gene 19) (newrule) | 56-13 (69) | 1753.1 |  |
| 56464997 | res940 (RE-UPLOAD) | 2026-09-22 ~13:0 | 536cf106 | none: res940 re-uploaded as live A/B control for res940_cf (reupload) | 54-11 (65) | 1663.1 | 2287 (LB 09-22 18:43Z  |
| 56471380 | res940_cfog | 2026-09-22 18:23 | 82a91ad1 | OVERFLOW_GUARD_ON (bank excess carry, safe partial PLACE; destroyed un (bugfix) | 65-43 (108) | 2317.0 |  |
| 56472823 | res940_cfog2 | 2026-09-22 19:45 | f415f8c0 | OVERFLOW_GUARD_V2 (plan-aware night-transfer guard) (bugfix) | 78-44 (122) | 2154.6 | 1427 (LB 09-23 06:25Z  |
| 56482921 | res940_cfog3 | 2026-09-23 04:51 | 1a5f9ad7 | OVERFLOW_GUARD_V3 (value-priced deposit trips; destroyed 861->126 u) (bugfix) | 69-23 (92) | 1932.7 |  |
| 56489764 | res940_cfog3le | 2026-09-23 09:55 | 2bd79408 | LATE_EXEC_ON (same-day dig+replant spent straw/tomato; ENDFIX1) (bugfix) | 116-52 (168) | 2310.7 | 1338 (LB 09-23 14:51Z  |
| 56520903 | res940_vrp | 2026-09-24 12:16 | b462a81a | ROUTE_VRP_ON (+SHADOW): dawn crew VRP router (RR_ITERS 30) (router) | 61-12 (73) | 2091.0 |  |
| 56525116 | res940_vrp2 | 2026-09-24 15:46 | db994f5a | ROUTE_VRP_FIX_FROZEN + ROUTE_VRP_VERIFY (SALEPIN1 frozen-hand spawn /  (bugfix) | 79-17 (96) | 2709.1 | 84 (LB 09-25 00:52Z 27 |
| 56527550 | res940_vrp3 | 2026-09-24 17:36 | c3eac8dc | ROUTE_VRP_NEEDS_FIX_ON (VERIFY fallback 3.1->0.4 days/game) (bugfix) | 181-52 (233) | 2660.0 | ~95 (equiv; not LB ent |
| 56542089 | res940_vrp5 | 2026-09-25 06:30 | 10577930 | vrp4 router deadline+checkpoint (VRPDEADLINE1) + VRPOBJ1 comparator +  (router) | 128-64 (192) | 2680.7 | 69 (LB 09-26 00:26Z 2, |
| 56572961 | res940_vrp7 | 2026-09-26 ~07:3 | 2a43b8aa | vrp6 EMPTY_ROUTE_UNHIRE_ON (unhire empty-route hands) + NONV2 M20z zer (mixed) | 137-25 (162) | 2503.5 | 320 (LB 09-27 00:32Z @ |
| 56580780 | res940_vrp8_jit | 2026-09-26 ~13:5 | ad9b5b2f | compiled C VRP router kernels (route_vrp_c.so) + deep ruin-recreate 15 (router) | 124-12 (136) | 2097.9 |  |
| 56600958 | res940_vrp9_cs | 2026-09-27 06:48 | cd94b334 | CARE_RIDE_ON + SLIVER_ON (newrule) | 71-8 (79) | 2227.4 |  |
| 56600971 | res940_vrp10_esw | 2026-09-27 06:48 | 73f4af9a | ESWORK1 run2 g30 work-gene theta (eswork_theta.npy: relay wheat bands, (trainer) | 62-36 (98) | 2595.8 | 115 (LB 09-27 12:58Z 2 |
| 56612145 | res940_vrp12_pfs | 2026-09-27 ~15:1 | 2532e456 | PLACEFEED_ON + PF_PUMPSAFE_ON (feed placement + fix of the d0 OPEN_PUM (newrule) | 26-4 (30) | 2551.9 |  |

θ MLE reads: vrp2 **2,818 ± 50**, vrp3 2,598 ± 60 (RATINGPATH2). vrp5 2,741 over 146 g, vrp9_cs 2,418, vrp10 **2,633 ± 44** (LIVEWATCH20). **Live θ fell 2,818 → 2,741 → 2,633 across three ships that each passed every gate.** LIVEWATCH20 traces this to the field mix: MELON is 22/71 of vrp5's 2600+ games and 21/27 of vrp10's. At equal family × band, vrp10 ≥ vrp5.

## 2. Judge-leg predictiveness (ship → live)
Consecutive era-C ships are paired: Δ live score vs the predecessor, both with ≥ 69 games. vrp10 is paired with vrp8, its parent (`A_predictive.txt`).

| leg | n ships | Spearman ρ(leg net flips, Δlive) | sign agreement |
|---|---|---|---|
| dev100 (V56) | 12 | −0.32 | 4/9 |
| held100 (V56) | 12 | −0.05 | 5/10 |
| FRESH300/600 (own live boards) | 8 | +0.22 | 4/8 |
| tapes50 (V56) | 12 | +0.29 | 5/8 |
| faithful-59 (ENGINE tapes) | 9 | **+0.40** | **7/9** |
| sum of 5 legs | 12 | +0.23 | 6/12 |
| Δours (primary coins) | 10 | −0.27 | 5/10 |

- **Noise floor.** Consecutive Δ live has sd ≈ 350 (cfog → cfog2 → cfog3 → cfog3le read 2,317 → 2,155 → 1,933 → 2,311 on +1 to +17 flip increments). A ship's predicted effect is +2 to +75 θ, so power is ≈ 0.
- **No leg is significant.** faithful-59 is the only leg with 7/9 sign agreement (P = 0.09 under a coin flip), and it is the only leg built from top-class rivals.
- **Contemporaneous pairs** (same day, and replay where one exists):

| pair | judge said | live / exact replay said | agree |
|---|---|---|---|
| ENDROUTE vs FT2 | +25 t 8.58 | same strength (2,254 vs 2,232) | yes (tiny) |
| ESR vs ENDROUTE | +450 (241 b) | +96 at g30-35 | yes |
| WIDE_PICK vs ESR | +178 POOLED278 / +185 BAND250 | +344 | yes |
| res940 vs headless | +325 BAND2-233 | +364 at equal game count | yes |
| WIDE_PICK_FREE vs WIDE_PICK | +117 t 3.14 | −583 at matched g87 | **no** |
| vpost vs res940 | BAND2 +3 flips | LIVE250 exact replay −3 (+4/−7) | **no** |
| vrp3 vs vrp2 | +10 flips over 5 legs | θ −220 (2.8 σ) | **no** |
| vrp9_cs vs vrp10 (both on vrp8) | vrp9 ≥ vrp10 (tapes +6 vs +2, FRESH +7 vs +6) | θ 2,418 vs 2,633; BAND −1 | **no** |

- **Reading.** Every non-trivial agreement is an increment of **≥ +178 coins/board on ≥ 233 boards** (ENDROUTE's +25 agreed only as "no difference"). Every reversal is a small flip increment. The only leg with a replay-exact link to live is BAND142: 46/46 byte-exact, and it matches the vrp10 > vrp9 read. It is the one leg that can carry a rating claim, and it was built only today (13:04-14:55Z).

## 3. Market coupling: Δtheirs = a + b·Δours
Source: `A_coupling_docs.tsv`, 1,436 deduplicated verdict-table rows with |Δ| ≤ 60k. The BUILD-STORY cross-check is `A_bs_coupling.txt`, 145 rows. Small = the |Δours|, |Δtheirs| ≤ 3k regime, where ship candidates live.

| axis | n | b (OLS) | r | ρ | b Theil-Sen | b small (n) | r small | P(Δtheirs>0) | P(theirs↑ \| ours↑) | BUILD-STORY b / r (n) |
|---|---|---|---|---|---|---|---|---|---|---|
| opening | 61 | **−1.30** | **−0.70** | −0.64 | −1.28 | +0.22 (18) | +0.19 | **0.87** | 1.00 | −1.34 / −0.85 (11) |
| land | 50 | −0.66 | **−0.75** | −0.74 | −0.65 | +0.39 (17) | +0.76 | 0.58 | – (0 ours↑) | – (3) |
| herd/feed | 114 | −0.89 | −0.41 | −0.02 | −0.01 | +0.23 (100) | +0.14 | 0.42 | 0.51 | −0.87 / −0.64 (29) |
| crew | 49 | −0.63 | −0.47 | −0.12 | −0.04 | −0.33 (47) | −0.49 | 0.57 | 0.58 | +0.36 / +0.45 (14) |
| sell | 128 | +0.15 | +0.12 | −0.17 | −0.21 | −0.39 (115) | −0.45 | 0.42 | 0.38 | −1.45 / −0.98 (18) |
| crop | 112 | −0.04 | −0.06 | +0.04 | +0.03 | +0.07 (93) | +0.06 | 0.56 | 0.58 | −1.18 / −0.87 (16) |
| endgame | 138 | +0.08 | +0.20 | +0.05 | −0.00 | +0.08 (138) | +0.20 | 0.52 | 0.52 | – |
| router | 148 | +0.01 | +0.02 | +0.24 | +0.11 | +0.02 (145) | +0.03 | 0.66 | 0.71 | −0.07 / −0.44 (11) |
| opp-conditioned | 119 | +0.07 | +0.07 | +0.11 | +0.10 | +0.12 (80) | +0.15 | 0.56 | 0.69 | **+0.99 / +0.91 (10)** |
| trainer | 324 | −0.89 | −0.83 | +0.08 | +0.07 | +0.00 (278) | +0.00 | 0.63 | 0.65 | +0.47 / +0.23 (30) |
| **pooled** | 1,436 | −0.64 | −0.51 | +0.01 | +0.02 | **+0.07 (1,210)** | **+0.08** | 0.57 | 0.61 | +0.04 / +0.03 (145) |

- **Transfer axes** (b < 0, |r| > 0.5, on both OLS and ranks): **opening −1.30 and land −0.66.** On the opening, each coin the arm costs us hands the rival 1.3. 87 % of opening rows raise the rival's purse, and every opening row that raised ours raised theirs too.
- **Structural gift** by the brief's definition (b > 0 with r > 0.5): only **opp-conditioned in BUILD-STORY** (+0.99, r +0.91, n 10, the MELON-counter/plate cells). In the docs sample, opp-conditioned has r +0.07, so this is not robust.
- **Decoupled axes** (|r| ≤ 0.2): router, endgame, crop (docs sample), and the pooled small regime. The full-range trainer b of −0.89 is carried by scratch-ES collapses (ESSCRATCH1: −48k/+50k and −40k/+48k); small regime 0.00.
  - These are the axes that shipped. Router + bugfix = 77 % of era-C flips. In era B, the decoupled sell/endgame/logistics rules gave 38 % of coins, and the rule-miss FT2 gave 53 %.
- **Gift share** (B_ledger): 107 of 645 rejects (17 %) name the gift. By axis: opening 0.33, crew 0.25, herd 0.22, crop 0.21, endgame 0.17, trainer 0.14, land 0.12, routing 0.12, sell 0.11, opp 0.06.
- **Ships by axis** (B_ledger judged rows): **opening 0/51, land 0/26, crop_mix 0/96** (FT2 is filed under herd_feed_care and LATE_EXEC under endgame), routing 29/94, endgame 13/31, sell 9/82.

## 4. Coins per flip
Coins per flip = total paired margin moved (Δmargin × games) per net flip, fitted through the origin. Sources: `A_cpf_docs.txt` (docs tables) and `A_bs_cpf.txt` (BUILD-STORY).

| leg | coins/flip (docs; rows, games) | coins/flip (BUILD-STORY; rows, games) | fit r |
|---|---|---|---|
| loss beds (loss25/50, LOSSBANK) | 8.4k (6, 198) | 3.9k (2, 78) | – |
| VLOSSBED / beds | 17.1k (7, 486) | 9.2k (11, 673) | +0.4 |
| tapes (V56 tapes50) | 10.4k (5, 126) | 12.7k (7, 293) | +0.6 |
| held100 (V56) | 17.7k (25, 2,634) | 12.1k (11, 1,148) | +0.9 |
| **BAND (142 / BAND250 / HIBAND)** | **17.2k (36, 4,255)** | **14.3k (28, 5,082)** | +0.8 |
| pooled (POOLED169-354) | 21.5k (8, 1,928) | 21.5k (17, 4,847) | – |
| POOL kernels | 24.2k (32, 8,322) | 13.6k (1, 100) | +0.8 |
| FRESH300/600 | 35.7k (28, 6,318) | 38.5k (5, 1,750) | +0.9 |
| **dev100 (V56)** | **44.6k (29, 2,110)** | **29.4k (34, 3,150)** | +0.95 |
| faithful-59 | 138k (11, 649) | 44.5k (9, 531) | +0.3-0.8 |
| ENGINE22/28/TOPLEG | 109k (51, 1,552) | 156k (3, 219) | +0.9 |

- **Close-game legs** (loss, bed, tapes, held, BAND) turn 4-18k coins into one flip. **dev and FRESH need 29-45k; ENGINE and faithful 44-156k.** The same +300/board arm shows **2.0-2.6× more flips on BAND than on dev.**
- BAND per family under PFS (BANDLEG1 per-seat CSVs):
  - **MELON:** 14-37, median loss −11.3k. A uniform shift of +3k/+5k/+10k/+20k flips 5/7/15/32.
  - **V:** 70-11, median loss −3.0k. +3k flips 7; +10k flips all 11.
- So one flip costs ~3k on a V seat and ~10k+ on a MELON seat.

## 5. Ship provenance

| era | class | ships | size | share |
|---|---|---|---|---|
| B (coins/board on the primary gate) | rule-miss (FERT_TIMING, class comparison 91 % vs 29 % best-day fert) | 1 | +2,845 | **53 %** of +5,335 |
| B | new rule (LOT4, SLOTPRIO, ENDROUTE, ESR, WIDE_PICK, WPF, vpost) | 7 | +2,165 | 41 % |
| B | trainer (head_940) | 1 | +325 | 6 % |
| C (net flips, 5 V56 legs) | **router** (VRP +65, REPAIR +7, UNHIRE/M20z +2, JIT +8) | 4 | +82 (+3.4/100 g) | **42 %** of +195 |
| C | **bug fix** (OVERFLOW V1-3 +1/+9/+6, LATE_EXEC +17, VRP2 +26, VRP3 +10) | 6 | +69 (+3.0/100 g) | **35 %** |
| C | new rule (CARE_RIDE+SLIVER) | 1 | +17 (+1.9/100) | 9 % |
| C | trainer (ESWORK g30) | 1 | +13 (+2.1/100) | 7 % |
| C | rule-miss (CARE_FILL +3; PFS +11 on 5 legs, **+8 on BAND142**) | 2 | +14 | 7 % |

Per-ship sizes are in `A_provenance.tsv`.
- Largest: FERT_TIMING (+2,845), ROUTE_VRP (+65 flips, +10.7/100, Δours +2.2-2.7k on every leg), VRP2 bug fix (+26), LATE_EXEC (+17), CARE_RIDE+SLIVER (+17).
- Two results that were later lost:
  - vpost was KILLED by exact replay.
  - M20z fires on 0/1,600 bank kernels, is worth ≤ 0.3 wins/100 live, and costs tine.sh −23.5k (LATCH1).
- **Comparison censuses produced the largest ships.** FERT_TIMING (ENGINE best-day fert 91 % vs our 29 %) is the largest era-B ship. PLACEFEED (CREWAUDIT1: we skip 100 % of placement nights, the rival 34 %) is the only BAND-passing arm.
- **Hand-lever families on opening, crop and land shipped 0 of 173 judged rows.**

## 6. Leg disagreements
- **Flip-sign agreement between legs, arms with both legs non-zero** (`A_bs_disagree.txt`, `A_legagree_docs.txt`):
  - dev~held **17/35 (49 %)**. Both are V56; this is a coin flip.
  - dev~faithful 8/14, dev~tapes 9/13, FRESH~dev 10/14, FRESH~held 13/17.
  - held~tapes 12/14, **FRESH~tapes 11/12**, faithful~tapes 9/11.
- **Δours agrees where flips do not.** Δours correlates at r +0.84 (dev~held, 18 tables), +0.81 (dev~faithful), +0.88 (held~FRESH) and +0.67-0.78 against BAND, with sign agreement 14/14 on dev~FRESH.
- **Disagreement count:** 37 arms have ≥ 1 of tapes/FRESH and ≥ 1 of held/faithful.
  - **9 are tapes/FRESH + but held/faithful −:** WHEAT_CYCLE, ESV56 ×3, ROUTEOPT2, VRPFALLBACK1 (shipped, vrp3), TOMATOFILL1, ROUTERJIT1 (shipped, vrp8), PLACEFEED2.
  - **1 is the reverse:** ESSTEP1 k0.5.
- **Re-judged on BAND:**
  - WHEAT_CYCLE → −1 (sides with held/faithful).
  - PLACEFEED → +8 after PF_PUMPSAFE (the faithful −3 was a d0 pump-kill bug, fixed in PLACEFEED3).
  - vrp9_cs (all legs +) → −1 on BAND, which matches live.
  - BANDSTACK1 found SLIVER −2, CARE_RIDE −1, CARE_RIDE+SLIVER −1 and latch-off −2 (so the shipped M20z latch is worth +2 on BAND, all from ZERO seats).
  - **Of the 2 disagreement arms re-judged on BAND, one sides with each group.** WHEAT_CYCLE follows held/faithful (−1). PLACEFEED follows FRESH/tapes (+8), once its faithful failure was traced to a bug. The all-positive vrp9_cs reads −1.

## 7. Trainers (`A_trainers.tsv`, `A_trainers_era.txt`; eras by arm start date)

| era | arms | ships | killed (flat / bug / early) | completed | notes |
|---|---|---|---|---|---|
| A 08-26..09-11 | 180 (ES-theta 175) | **13** | 28 / 13 / 2 | 2 (134 unstated) | flow9 → B: live ~1,172 → 2,516; the largest cumulative gain in the project |
| B 09-12..09-19 | 61 (ES-theta 37, ES-head 10, PPO 6) | 1 (head_940) | 24 / 6 / 5 | 18 | head_940: ~1.02M sim episodes (derived), BAND2-233 +3/−2, live +364 at equal g |
| C 09-20..09-27 | 50 (PPO-head 18, ES-gene 8, ES-head 6) | 1 (ESWORK g30) | 16 / 1 / 1 | 20 | g30: ~15.8k games (derived), +13 flips / 609; ESSTEP1: g30 is at the ridge (k0.5 −, k1.5 −508) |

- **Since 09-12: 111 trainer arms → 2 ships (1.8 %).**
- **Stated games:** 63,285 (RLFAST2 61,440; ESPOOL1 1,125; RLPOOL1 720). Derived sim episodes: 7.68M (5 PPO arms).
- **Games per net ship flip:**
  - head_940 ≈ 1.02M / +1 (BAND2).
  - ESWORK ≈ 15.8k / +13 ≈ **1.2k games per flip.** It is the only trainer family whose fitness was the exact engine on the ship legs.
- **MELON seats in any trainer fitness before ESBAND1 (09-27 15:18Z): 0.**
- **Killed 98 vs completed 40.** The 09-26 law (never kill for flat) holds for the 3 arms now running: ESBAND1, RLFAST run2s and run3g1. RLFAST gates so far are 0 flips (u10/u20) and −5 (u10).

## 8. Effort vs yield by axis (`A_effort.tsv`)

| axis | docs | judged rows (B_ledger) | named worktrees | BUILD-STORY arms | shipped gain | yield per 10 judged rows |
|---|---|---|---|---|---|---|
| router / logistics | 45 | 94 | 39 | 49 | era C **+118 flips** (VRP family + JIT); era B WIDE_PICK(+F) +295 | **3.1 ship rows** |
| endgame | 14 | 31 | 7 | 23 | era B +475 (ENDROUTE, ESR) | 4.2 |
| sell / shed | 67 | 82 | 18 | 59 | era B +1,250 (LOT4, SLOTPRIO); era C OVERFLOW +16 | 1.1 |
| crop / fert care | 49 | 96 | 24 | 96 | era B **+2,845** (FT2); era C LATE_EXEC +17 | 0 (FT2 filed under herd, LATE_EXEC under endgame) |
| herd / feed / care | 38 | 64 | 22 | 61 | era C +31 (CARE_FILL, CARE_RIDE+SLIVER, PFS) | 0.9 |
| crew / hires | 27 | 53 | 2 | 61 | UNHIRE (in vrp7) ~+2 | 0.4 |
| opp-conditioned | 33 | 54 | 20 | 84 | M20z (≤ 0.3 wins/100), vpost (killed) | 0.7 |
| **opening** | 31 | 51 | 16 | 45 | **0** | **0** |
| **land / Q4** | 15 | 26 | 6 | 31 | **0** | **0** |
| trainer | 178 | 134 | 44 | 154 (+~315 census) | era A 13 ships; since 09-12 head_940 +325, ESWORK +13 flips | 0.5 |
| infra / judge / analysis | 215 | 40 | 52 | 117 | enabling only | – |

Agent worktrees: 130 `agent-*` (08-25..09-17) + 258 named. Commits could not be axis-mapped (1,353 of 2,105 subjects carry no axis keyword).
- **Router and endgame yield 3.1-4.2 ship rows per 10 judged rows; opening, land, crop and opp yield 0-0.7.** Those four absorb 227 judged rows and 128 docs, for **0 lasting ships** apart from FT2 (a rule-miss) and LATE_EXEC (a bug).

## 9. Verdict: the 8 holes, ranked by expected rating

Rating arithmetic: `A_headroom.txt`, Elo/400 MLE on vrp10's 84 live games using the BANDLEG1 family method (it reproduces PFS +36).
- MELON uniform +1k/+3k/+5k/+10k/+20k → **+11/+30/+42/+96/+249 θ** over PFS.
- V +3k → +16. All V seats won → +25.
- Field mix: at the 2600+ mix (MELON 78 %), PFS θ is **2,598**, vs 2,668 at the current band mix (**−70**). An all-MELON band gives 2,521.

| # | hole | evidence line | probe (cost) | expected Δθ |
|---|---|---|---|---|
| 1 | **MELON-cell headroom never measured.** No oracle or seat-swap on MELON boards. | Top 5 needs +20k/game on MELON seats (§9 arithmetic). Every oracle ran on V56 boards: PLANSELECT +3.2k, BESTRESP6 robust ~+1k, SELLAUDIT1 +165, ROUTERAUDIT1 +722. The DSM seat-swap (ours 49-51 vs DSM 100-0, +19k/board) was on DSM's boards, pre-VRP. | **MELONSWAP1**: fetch ~20 recent live games from each of 8 MELON-family top-100 teams (the LIVEWATCH20 list). Put PFS in their seat vs their opponents' tapes. Compare W and per-product/day sales on identical boards. (~160 eps fetch + 160 real-engine games ≈ 1.5 CPU-h.) | 0 direct. It decides whether +300 is reachable by this body, and it yields the per-product gap on identical boards. |
| 2 | **Judge mix ≠ live mix.** The ship gate is blind to 57-78 % of the band. | 0 of 5 standard legs holds MELON rivals. 10 arm-cells of ~780 judged on BAND. Leg→live ρ ≤ +0.40 (n ≤ 12). Contemporaneous pairs 4/8. θ fell 2,818 → 2,633 over 3 all-pass ships. | Make **BAND142 family-weighted Δθ** the ship gate (dev0-9 as a no-regression guard only). Re-judge the positive-own near-misses not yet on BAND: NONV4-a2 (tapes +4, Δours +1,445, Δtheirs −508; pool 0 with Δtheirs +639) and MELONCOUNTER2-Cf (tapes +3, Δours +373). (2 × 142 = 284 games.) | +0..+20 per surviving arm. It stops false ships (vrp3 −220, WPF −583, vpost −3). |
| 3 | **BAND leg under-powered.** | Family Δθ SE ±17 at 142 seats. 51 MELON seats from 45 opponent subs (40 teams). 14 of 17 new vrp10 losses are unbanked (10 NO + 4 author-only, LIVEWATCH20). BAND is 2.6× more flip-sensitive than dev (17k vs 45k coins/flip). | **BANDBANK2**: bank every new vrp10/vrp12 band game (+~10/day) plus the 14 listed subs. 142 → ~300 seats by 10-01. (0 arm games; fidelity check only.) | 0 direct. SE 17 → ~11, so +20 θ arms become resolvable. |
| 4 | **Field drift is not in the plan.** | θ −70 if the band reaches the 2600+ MELON mix (78 %). vrp5 → vrp10 fell 108 θ at equal skill (LIVEWATCH20 standardisation). The final is Oct 1-15 against the final top field. | **MIXTRACK1**: re-weight every BAND result to the latest 2600+ family mix, once a day. Report θ at mix and at the projected Oct mix. (0 games.) | Guards against −70. Re-ranks candidates toward MELON-cell gains. |
| 5 | **Rule-miss censuses vs the top class are under-invested.** They are the highest-yield class. | The two comparison-census ships are FERT_TIMING (+2,845, 91 % vs 29 %) and PLACEFEED (the only BAND pass, +8). Hand-lever families shipped 0/173. The only MELON census is MELONAUDIT1 (17 categories, 1 flag: sale walk 8.9k vs 4.9k/g, 70 vs 45 floor units). | **FLOORHOLD1** (wool/milk/straw floor in `_sell_hold`) on BAND142. Then an op-by-op census of us vs the MELON rival on the MELONSWAP1 boards (hole 1): same board, same day, op-type counts. (142 games + 0.) | +5..+15 |
| 6 | **Trainer fitness has held 0 MELON seats until today.** | 111 trainer arms since 09-12 → 2 ships (1.8 %). ESWORK ≈ 1.2k games per flip is the best trainer rate. It was fitted on V56 dev plus V-clone legs plus 6-12 live-loss tapes. ESBAND1 (MELON weight .565) started 15:18Z. | Keep ESBAND1 running (the 09-26 law). Judge g10/g20 on the held-out 71-seat half with family Δθ. Give RLFAST run3g1 the same 136-group band bank. (0 extra; ~61 min/gen.) | +0..+30 |
| 7 | **The volume gap was only judged on V legs.** | MELON losses: rival sells 2,231 vs 1,594 u/g (d10-19: 866 vs 462); in wins the two are equal (MELONAUDIT1). All volume arms (RELAYFILL1, CREWRELAY1, TOMATOFILL1, GAPFIX1, WHEATLATE1, EARLYRAMP) were rejected on dev/held/FRESH, where land/crop coupling is transfer (b −0.66). None was judged on MELON seats. P10 on MELON was still a gift (+8.3k theirs). | Re-run the least-gift volume cells (TOMATOFILL ii_fill tapes +1, RELAYFILL FRAC 1.0, CREWRELAY1) on the 51 MELON seats only, paired vs PFS. Kill at Δtheirs t ≥ 2. (3 × 51 = 153 games.) | +0..+30 if any cell is gift-free on MELON (P ≈ 0.2 given P10) |
| 8 | **Ship gates count flips on 20-100-game legs.** | dev~held flip-sign agreement is 17/35 (49 %). Flip sd ≈ √(changed boards) ≈ 3-4 per leg. The FRESH600 bar (+6) is ≈ 1.7 σ. Δours agrees across legs (r 0.7-0.9, sign 14/14 dev~FRESH). | Replace per-leg flip bars with pooled Δmargin t plus family Δθ (hole 2). Re-score the 14 era-C ships from existing CSVs. (0 games.) | Prevents −50..−200 θ false ships like vrp3. Cost 0. |

**What the numbers rule out.**
- **Another router or bugfix round** cannot reach top 5: the whole era-C sum is +195 flips / ~5,000 games ≈ +4/100 on V-heavy legs.
- **Closing all V losses** is worth +25 θ.
- **The opening as a single lever** is out: b −1.30, 0/51 rows shipped, P10 still a gift on BAND.
- **The remaining distance (+280 θ) is the MELON cell at ~+20k/game.** Holes 1-4 cost ≤ 2 CPU-h plus re-analysis. They decide whether that distance exists for this body before any further arm is spent.

## Files
- `S/buildreview1/A_bs.tsv` (+ `A_bs_p1..3.tsv`): BUILD-STORY arm × leg extraction. `A_pairs.tsv`: docs verdict tables. `A_ships.tsv`: ship chain + live + judge-vs-live notes. `A_trainers.tsv`: trainer census.
- Derived tables:
  - `A_timeline.tsv` / `.md`, `A_chain.md`
  - `A_coupling_docs.tsv`, `A_bs_coupling.txt`
  - `A_cpf_docs.txt`, `A_bs_cpf.txt`
  - `A_legagree_docs.txt`, `A_bs_disagree.txt`
  - `A_predictive.txt`, `A_provenance.tsv`, `A_effort.tsv`, `A_headroom.txt`, `A_trainers_era.txt`
- Re-run: `python3 S/buildreview1/A_pairs.py && python3 S/buildreview1/A_stats.py {coupling|cpf|legagree}`; `cd S/buildreview1 && python3 A_bs_stats.py {merge|coupling|cpf|disagree|verdicts}`; `python3 A_provenance.py {prov|pred}`; `python3 S/buildreview1/A_headroom.py`.
