# MELONHYBRID4 — KERNEL2 with PFS's real h0 and a V56 kernel that inherits the farm

2026-09-28, 03:14Z-03:55Z (box clock). Root fix for the KERNEL2 candidate (vrp13_v56gate): no idle h0 anywhere.

**Verdict: the idle hour is gone and the MELON gain survives.**
- Unfired seats are **byte-identical to the live package** (proven 6/6 V+OTHER, 2/2 unfired MELON, 6/6 ZERO excluded, 2/2 selfplay vs vrp12).
- A4 (NOOP_H0=False + INHERIT) on the 51 BAND142 MELON seats: **30/51** (PFS 14, V56 31, candidate 32); JC1-faithful n29 **5 -> 14 (+10/-1 = +9)**, soft dth +71.6 (z 2.86), GATE2 band A+B PASS.
- **v2 = A4 + `KERNEL2_ZERO_CASH=488|1088|1303|1409`: BAND142 91 -> 108** (candidate 102, H0MERGE+ZERO_CASH 105). ZERO 6/7, V 70/81 = PFS exactly (the GATE2LEGS1 guard failure was the idle hour on V seats; it no longer exists).

## 1. Cash plan (step 1)
- PFS's real h0 (identical on every seat): farmer NORTH, BUY_PRODUCT WHEAT 53, 4 × HIRE -> **cash 1,409, 53 wheat, 4 hands at h1** (the wheat is a pump: PFS sells 48 back at h1).
- V56's own game: h0 BUY 20 / SELL 15 wheat + 1 wheat seed -> 2,863, 5 wheat; h1 farmer NORTH, 5 × HIRE, 2 COW, 2 SHEEP -> 1,051 at h2; 12 melon seeds bought h6-h17 (~960).
- MELONHYBRID2's hybrid (c) broke because the kernel never sold the 48 pump wheat: 1,409 - 1,812 of h1 buys -> 86 coins, seeds bounce.
- **Rewrite:** SELL WHEAT 48 (quoted down the book: ~+1,450, cash ~2,860 = V56's), BUY_SEED WHEAT 1, BUY_ANIMAL COW 2 + SHEEP 2, HIRE × (5 - 4) = 1 (the 5th hire of the day costs 5 = V56's 12 total). **Every order fits; 0/56 fired seats dropped any unit.**
- Farmer: PFS's h0 NORTH already put it on V56's h2 tile (4,3) -> PASS. The 4 h0 hands PASS; the one new hire spawns on (4,4) -> hand layout at h2 = V56's own ((4,4),(5,4),(4,5),(5,5),(4,4)).

## 2. Switches (branch `melonhybrid4` 79636f64 = pfsh0merge1 2791f8c0 + this; defaults keep the candidate byte-identical)
- `KERNEL2_NOOP_H0 = True` (plan.py). False: step 0 = `_pfs_act` (master h0; kernel preloaded), step 1 latch unchanged, PFS seats continue unshifted (SHIFT/H0MERGE bypassed).
- `KERNEL2_INHERIT = False`. True (with NOOP_H0=False): `Runtime._k2_inherit` shows the kernel its own world twice at step 1 (virgin farm relabelled h0, then its post-h0 farm: holding = net h0 product buys, seeds, no hands, farmer on spawn, cash = ours + sale of the excess - seeds) and rewrites the two rows onto our farm as in §1 (order SELL, seeds, animals, hires; each clipped to projected cash). From step 2 the kernel plays unchanged.
- Step time: step 0 (PFS h0 + kernel preload) mean 411 / max 563 ms; step 1 max 7 ms; later max 0.56 s.

## 3. Proofs (S/melonhybrid4/k2run.py = S/pfsh0merge1 runner + inherit record; BAND142 harness)
| proof | seats | reference | match |
|---|---|---|---|
| new switches OFF (KERNEL2_ON only) | highfrequencyf (MELON), team (V) | MH3 v56h1m 128,661/26,573; pfsh1 149,471/137,923 | **2/2 exact** |
| NOOP_H0=False, gate not firing | 3 V + 3 OTHER (`res/proof_pfsv.txt`) | pfv1 (unshifted PFS) | **6/6 exact** |
| A4, 2 unfired MELON (leaveyou 2,854, aildarsloperna 2,904) | 2 | pfv1 | **2/2 exact** |
| v2, 6 ZERO at 488 (`res/proof_v2.txt`) | 6 | pfv1 | **6/6 exact** |
| v2, Pico (10) + 2 MELON | 3 | A4 rows | **3/3 exact** |
| v2 selfplay vs vrp12 pkg (GATE2LEGS1 leg, board 0 both seats) | 2 | self_off 91,237/91,407 | **2/2 exact** (rival h1 1,303 excluded) |
| final committed code | highfrequencyf, team | A4 / pfv1 | 2/2 exact |

- Gate under the REAL h0 (MH2 `q1_vis.csv` h1 rows; `res/gate_realh0_q1vis.txt`): MELON 49/51, **V 0/81 (min 2,599)**, OTHER 0/3, ZERO 7/7 (488 ×6, Pico 10). So V/OTHER are PFS exactly on BAND142.

## 4. A4 on the 51 BAND142 MELON seats (`res/a4.csv`, `res/sum_a4.txt`, `res/faith_a4_*.txt`, `res/flips_a4.txt`)
Kill rule not hit: n28 W 14 (pro-rata 25.5 > 20).

| vs | n | W base -> A4 | flips | dours (t) | dtheirs (t) |
|---|---|---|---|---|---|
| PFS (pfv1) | 51 | 14 -> **30** | +19/-3 = **+16** | +4,145 (1.62) | -13,928 (-5.64) |
| candidate (MH3 v56h1m) | 51 | 32 -> 30 | +1/-3 = -2 | -1,500 (-0.62) | +2,633 (0.77) |
| V56 from h0 | 51 | 31 -> 30 | +1/-2 = -1 | -3,499 (-1.50) | +5,423 (1.46) |

| JC1 (units basis) | n | W | flips | dours (t) | dtheirs (t) | soft | GATE2 band |
|---|---|---|---|---|---|---|---|
| A4 vs PFS, all | 51 | 14 -> 30 | +19/-3 | +4,145 (1.62) | -13,928 (-5.64) | t +4.31, dth +85.4 (z 4.16) | A+B PASS |
| A4 vs PFS, **faithful** | 29 | 5 -> 14 | **+10/-1 = +9** | -2,227 (-1.34) | -9,280 (-6.78) | t +3.11, dth +71.6 (z 2.86) | A+B PASS |
| candidate vs PFS, faithful (reference) | 29 | 6 -> 17 | +12/-1 = +11 | -557 | -9,961 (-6.91) | dth +91.8 (z 3.43) | A+B PASS |
| A4 vs candidate, faithful | 26 | 14 -> 13 | +0/-1 | -385 (-0.62) | +40 (0.31) | dth -7.1 (z -0.74) | – |

- **Inherited farm = V56's farm** (fired seats, means): cash at h2 1,069 (V56 1,051), 5 hands, 4 animals; **melon tiles at d1 dawn 12.0 (49/49 = 12)**, plants 20.0 (V56 20), cash d1 39; **herd at d10 13.7** (V56 13.7, hybrid (c) 8.0).
- Margins track V56-from-h0 to within a few hundred coins on most seats (akmr 18,285 vs 18,266; snorlax 80,269 vs 80,238).
- The 3 losses vs candidate: artemthefarmer (candidate +161,886 = rival breakage; A4 -12,293 = V56 -12,317), yannikschiffne_114131636 (-13,732 vs +25,255), yumizu (-5,161 vs +7,384). The rival sees our real h0 wheat buy in its h0 book (h1 cash 2,438 vs 2,467), so its open-loop tape diverges differently. On faithful seats A4 vs candidate is -1 flip, dtheirs +40.

## 5. ZERO and v2 (`res/a4_zero.csv`, `res/v2.csv`, `res/h1cash.txt`)
- **Under our real h0 the exclusion values move:** the ZERO clone's h1 cash is **488** (433 under the no-op), techno coven **1,088** (1,033), Pico 10 (27). These are the zerogate1 live tells, which were recorded with our real PFS h0: 488 ×11, 1,088 ×2.
- **Own lineage:** PFS h0 vs PFS h0 in lockstep gives **1,303** (engine, `h1cash.py`; GATE2LEGS1 self_off also shows 1,303). 1,409 only occurs under our no-op, so it is harmless in the list. A V56 rival shows 2,901, not fired.
- MELON false positives: 0/51 band (h1 values 8 .. 2,492) and 0/73 live fired MELON at 488/1,088/1,303/1,409.

| ZERO (7) | W | note |
|---|---|---|
| PFS | 5 | |
| candidate | 1 | gate false positive |
| A4 (no list) | 1 | = candidate row by row |
| **v2** | **6** | 6 at 488 -> PFS (pfv1 exact, 5 W); Pico -> V56 W |

## 6. BAND142 (v2)
| family | n | PFS | candidate | H0MERGE+ZERO_CASH | **v2** |
|---|---|---|---|---|---|
| MELON | 51 | 14 | 32 | 32 | **30** |
| V | 81 | 70 | 67 | 65 | **70** (= PFS, 0 fire) |
| ZERO | 7 | 5 | 1 | 6 | **6** |
| OTHER | 3 | 2 | 2 | 2 | **2** (= PFS) |
| total | 142 | 91 | 102 | 105 | **108** |

- JC1 over the changed seats (`res/faith_v2_band.txt`; V/OTHER = 0 change): all n58 19 -> 36 (+20/-3), soft dth +85.4 (z 4.07), A+B PASS. **Faithful n34: 9 -> 18 (+10/-1 = +9)**, dtheirs -7.9k (t -6.10), soft dth +71.6 (z 2.91), A+B PASS.

## 7. Hand-off (not run here)
- src: branch `melonhybrid4` @ 79636f64, tree /mnt/e/_work/kagg3_wt_melonhybrid4/src (sparse).
- Switches: `KERNEL2_ON=True,KERNEL2_NOOP_H0=False,KERNEL2_INHERIT=True,KERNEL2_ZERO_CASH=488|1088|1303|1409`
- JUDGEALL1: `bash S/judgeall1/judgeall.sh mh4v2 /mnt/e/_work/kagg3_wt_melonhybrid4/src "KERNEL2_ON=True,KERNEL2_NOOP_H0=False,KERNEL2_INHERIT=True,KERNEL2_ZERO_CASH=488|1088|1303|1409" 3`
- Expected on the GATE2 legs: every unfired seat = the off arm exactly, so the guard's idle-hour failures (pool/dev/FRESH/faithful59) reduce to the fired seats only. The open risk is what the gate fires on outside BAND142. Live tells under our real h0 fire on 9/164 live V-labelled rivals, and the guard legs' non-MELON fired openers (GATETABLE1) remain.
- `KERNEL2_PFS_H0MERGE` and `KERNEL2_PFS_SHIFT` are irrelevant under NOOP_H0=False (bypassed).

## Files
- **S/melonhybrid4/:**
  - run.sh, with modes `off`, `pfsv`, `smoke`, `a4`, `zero`, `v2`, `self` and `final`;
  - k2run.py, summ.py, addunits.py, trace.py, h1cash.py, checkpoint.txt.
- **res/:**
  - off, pfsv, a4 (+_u), a4_zero (+_u), v2 (+_u), v2_band_u, self_v2 and final (csv and log);
  - proof_*.txt, sum_*.txt, faith_*.txt, flips_a4.txt, mech_*.csv (per-seat cash h2 / d1 melon / herd d10 / inherit orders);
  - gate_realh0_q1vis.txt, h1cash.txt, timing.txt, trace_hf_v56_pfs.txt, steps_*.json.
- **Licence:** the V56 kernel source (Apache-2.0) is untouched. Only the runtime wrapper changed.
