# DECISION BRIEF (2026-09-28 08:20Z): which package, if any, goes into the final pair

Analysis and docs only (FINALBRIEF1). No games, no src change, no upload. Sources: JUDGE-MH4V2 (v2, closed 8de4cd9b), V3BRANCH1 §3c (v3, bea5f30c),
GATETABLE2, FRESHLIVE1, PACKV2, PACKV3, PKGPOOL1, TOPV56-1, V56WEAK1, FINALSLOT1, RULES1.

## The page (2 minutes)

**Recommendation: upload v3 `dist/vrp15_k2fire.tar.gz` (md5 `1929f224b19f24b16e1d85f1a6740b26`) once, today or tomorrow, and nothing after it.**
The FIFO then retires vrp10_esw (56600971). The final pair becomes vrp12_pfs (56612145) + vrp15_k2fire.

| | **A. keep the live pair** | **B. upload v3 vrp15_k2fire (recommended)** | C. upload v2 vrp14_k2real |
|---|---|---|---|
| what it is | vrp12_pfs + vrp10_esw | PFS, plus the V56 kernel takes the farm at step 1 **only if** the rival's h1 cash is exactly 26, 29, 2,338 or 2,438 | PFS, plus V56 at step 1 if rival h1 cash <= 2,550 and not 488/1088/1303/1409 |
| GATE2 (9 legs) | n/a | **PASS**: band-276 155 -> 177 **+23/-1 = +22**, A z +5.27, pooled B t +4.44, guard OK, gift OK, breakage guard not triggered | **PASS**: band-276 155 -> 198 **+50/-7 = +43**, A z +6.70, B t +5.79, guard OK, gift OK; breakage guard triggered (faithful A still z +4.83) |
| legs that lose | none | faithful59 -2 (soft t -1.30, two 2438 ENGINE tapes); every other leg 0 | faithful59 -1 (+5/-6, own coins t -2.57) |
| fires on | none | **~9 % of our live games** (0 % unmeasured vectors) | ~23 % of our games (50 % of the field), **7-8 % on vectors with no faithful evidence**, incl. 15 V-labelled live rivals (9 never measured) |
| live-weighted net flips / 100 games | 0 | **+1.9 [+1.1, +2.9]** (GATETABLE2), **+2.5** (judge rows) | +2.4 in-sample, **+0.6** with unmeasured filled (GATETABLE2); +3.4 / +1.3 (judge rows) |
| newest 60 live games (FRESHLIVE1) | 16 W | 19 W (+3/-0), **faithful n51: 0 flips, never loses** | 25 W (+10/-1), **faithful n34: -1** (feles99 at 2,485) |
| expected Oct rank (FINALSLOT1 live/GW model) | **~85-90** (p10-p90 75-100) | **~+2-4 ranks** -> ~82-87 | ~+1 rank filled (+4 if every unmeasured vector behaves like the band) |
| package integrity | live | 5/5 coin-exact, 52/52 reacting pool = src tree, submission test 11/11, turn budget OK | 3/3 coin-exact; no pool/submission run on the tarball |

**Why v3 over v2.** v2 wins more band seats, but only on the in-sample band; on fresh live seats it is -1, and a third of its extra fires land on
vectors nobody has measured, where the reacting prior is -0.25/seat. v3 fires only where tape evidence is positive, and every unseen bot gets
plain vrp12_pfs (byte-identical). Its downside is capped at the fired 9 %.

**What neither does.** Top 5 needs ~30 of the 37 band MELON losses flipped (BT θ 2,951); v3 is ~3 rung-equivalents live (~13 on the band, the
optimistic ceiling). Against the top field the V56 kernel equals PFS (TOPV56-1: clean n23 +2/-2; the top teams beat it by 19.6k/game). The V and
ZERO cells do not move.

**Calendar.** Now 09-28 08:20Z. Deadline **09-30 23:59Z** (10-01 02:59 local). Safe latest upload **09-30 21:00Z**; hard latest ~23:30Z.
5 uploads/UTC day. Validation 2-5 min, first public game 4-9 min later. Final = Bradley-Terry over Oct 1-15 games of the last 2 uploads.

---

## 1. The candidates in numbers

### 1.1 GATE2, all 9 legs (paired per board vs the live vrp12_pfs rows)

| leg | n | v3 (26\|29\|2338\|2438) | v2 (ZERO_CASH exclusion) | vrp13_v56gate (FAILED 09-28) |
|---|---|---|---|---|
| pool (reacting, 36 notebooks) | 52 | 52 -> 52, 0, soft t -0.96, fires 4 | 52 -> 52, 0, t -0.89, fires 8 | 0, t **-4.28** |
| dev | 20 | 0, fires 0 | 0, fires 0 | -2, t -2.87 |
| faithful59 (ENGINE/BAND tapes) | 59 | 20 -> 18, **-2**, t -1.30, fires 8 | 20 -> 19, -1 (+5/-6), t -0.70, fires 41 | -10, t -2.74 |
| self (live package as rival) | 20 | 0, fires 0 | 0 (1303 excluded) | -7, t -27.4 |
| clone (V48) | 20 | 0, fires 0 | 0, fires 0 | -2, gift t +5.97 |
| **band-276** | 276 | 155 -> **177**, **+23/-1**, t +5.29, fires 53 | 155 -> **198**, **+50/-7**, t +6.92, fires 120 | +32, t +4.84 |
| - MELON / V / ZERO | 116 / 134 / 22 | +21 / +1 / 0 | +39 / +3 / +1 | +41 / 0 / -9 |
| - BAND142 / HOLD104 / NEW2 | | +13 / +6 / +3 | +17 / +19 / +7 | |
| held | 50 | 0, fires 0 | 0, fires 0 | not run |
| tapes50 | 50 | 0, fires 1 | 0, fires 1 | -3 |
| FRESH300 | 300 | 0, fires 0 | 0, fires 0 | n24 -1, t -2.38 |
| **A** band soft dθ | | +50.5 (SE 9.6) z **+5.27** | +99.2 (SE 14.8) z **+6.70** | z +5.67 |
| **B** pooled n807 soft t | | **+4.44** | **+5.79** | +0.26 |
| guard / gift | | OK / OK (reacting dtheirs t -0.82) | OK / OK (t -1.54) | **FAIL** guard |

Every unfired seat on every leg is byte-identical to the live package (v2 677/677; v3 781/781 by construction, 7/7 + 31/31 + 52/52 proven).

### 1.2 Live weight (net flips per 100 of OUR live games; unfired = 0)

| estimate | v3 | v3c (26\|2438) | v2 |
|---|---|---|---|
| GATETABLE2 tape rows, bootstrap [10-90] | **+1.9 [+1.1, +2.9]** (CV +1.4) | +1.6 [+0.7, +2.4] | +2.4 [+1.3, +3.5] |
| same, unmeasured vectors at the reacting rate | +1.9 | +1.6 | **+0.6** |
| judge rows x live OURS % (faithful / all seats) | **+2.48 / +2.86** | +1.69 / +1.97 | +3.39 / +5.82 (filled +1.31) |
| fired share of our games (unmeasured) | 9.2 % (0) | 6.6 % (0) | 23.3 % (7.2-8.3) |

**Rank conversion (FINALSLOT1 k-ladder).** One flipped band MELON seat (of 51) ≈ 0.84 net flips per 100 live games (MELON = 43 % of our games)
≈ 1.2 ranks at our position. v3's +1.9..+2.5 ≈ 2.3-3 rungs ≈ **+2-4 ranks**. v2 filled +0.6 ≈ +1 rank.

### 1.3 Out-of-sample checks
- **FRESHLIVE1 (60 newest live games, TOP46 + 14 after 02:34Z):** v3 16 -> 19 (+3/-0); faithful n51 0 flips, soft t +0.16; fires 14/60.
  v2 16 -> 25 (+10/-1); faithful n34 -1; fires 38/60. GATETABLE2 predicts ~+1 flip for v3 on 51 faithful seats: 0 is inside the noise (1 flip = 2/100).
- **PKGPOOL1 (the tarball itself):** 52/52 coin-exact to the judged src tree vs the reacting pool (4 fired = v2 rows, 48 = OFF rows);
  `tests/test_submission_runs.py` 11/11 against the tarball.

## 2. What each option does NOT do
- **Top 5 is out of reach by this route.** It needs BT θ 2,951 = ~30 of the 37 band MELON losses flipped (86 % MELON wins). v3 is ~3 rungs live,
  ~13 on the in-sample band (BAND142 +13; finalslot1 k=13 ≈ rank ~65 in the live model is the optimistic ceiling, since band flips have never
  transferred 1:1). Top 20 needs ~20-25 flips.
- **V56 is not a better bot against the top field.** TOPV56-1: on clean seats V56 = PFS (JC1 n23 +2/-2), and the top teams beat it by 19.6k/game
  (5 W vs 38 W on 59 faithful seats). V56WEAK1: V56 is a script; it loses 20/20 to our reacting PFS (strawberry book collision -19.9k).
  The kernel wins only against specific MELON openers that do not react.
- **V and ZERO do not move.** v3 fires on 1 V seat of 134 and 0 ZERO seats. The V >= 2,600 cell (2-3 live) and all non-MELON losses stay.
- **Option A (as is)** keeps ~85-90 (p10-p90 75-100); the pair is a statistical tie and vrp12 dominates vrp10 in every θ source, so FIFO-retiring
  vrp10 costs nothing.

## 3. Risks
1. **Tape-only evidence for the whitelist.** No whitelisted value has a positive *reacting* measurement; the only reacting seats (4 pool seats at
   29, reyhanksatria) are 0 flips with own coins -13.5k..-21.0k. Per-value faithful n is small: 26 n6 (+3), 29 n8 (+2), 2338 n22 (+1; judge n3),
   2438 n30 (+5; judge n26). 2438 carries ~half the estimate, and the faithful59 -2 also sits on 2438 (ENGINE tapes). Split-half CV +1.4.
2. **Exact-cash fingerprints of specific notebooks.** The latch fires on the rival's exact h1 cash after our real h0 (GATETABLE2, 547/547 mapping):

   | value | LB teams (live census) |
   |---|---|
   | 26 | boominginging #113, kuengo #80, mhw #186, liminhai #77, huaiyuyoung #57 (MELON 55-openers) |
   | 29 | ready or not here i come #63 (33-opener); **collision**: janson / James Holland / public best-market-agent family (25-opener, public-notebook family, all ranked below #2,000) |
   | 2338 | **Boey #2** (47 of 61 field rows), Yannik Schiffner #33, Christoffer Thimsen #50, Excluding #48 |
   | 2438 | Just A game on your lips #12, Azat Akhtyamov #9, Densike #30, Matt Motoki #73, mtmr_s1 #18, Navier-stokes #70, DECEM #6 (4 rows), high frequency farming #126 |

   - If one of these teams re-orders its h0 (e.g. [COW, WHEAT 5] -> [WHEAT 5, COW] moves 2438 -> 2464) the latch silently stays PFS = vrp12.
     That failure mode is safe.
   - The live risk is a *new* bot landing on a listed value: it gets V56 with no evidence. 29 already collides (pool 0/4, dmargin -9.5k).
   - 2338 means v3 plays V56 against Boey #2 (evidence +1 on n22 ≈ neutral) and 2438 against DECEM #6 and Azat #9. That is exposure to the
     top field, where TOPV56-1 finds V56 = PFS at best.
3. **First-turn time.** Step 0 on a loaded box: 1.18-1.57 s on 5/52 cold starts (PKGPOOL1), 1.52 s once (PACKV3). The live vrp12 package measured
   1.30 s under the same load (STEP0TIME1), so this is PFS h0 + load, not V56. Cost ≤ 0.57 s of the 60 s per-game overage; no forfeit.
   Every later turn ≤ 0.57 s; fired step 1 155-245 ms. Measured on our box, not Kaggle hardware.
4. **Only one of the two may be uploaded.** The FIFO keeps the 2 newest: uploading v3 retires vrp10_esw. A second upload (v2 after v3, or anything)
   retires **vrp12_pfs**, leaving the final pair without our anchor. Undoing v3 costs two further uploads (e.g. two vrp12 re-uploads).
5. **Field drift.** FINALSLOT1's rank model holds the field at 09-27 22:59Z; top teams are still uploading, which pushes every option down equally.

## 4. Calendar and exact upload steps (the upload is the user's)

| when (UTC) | what |
|---|---|
| 09-28 now -> 09-30 21:00Z | upload window for v3 (safe latest 21:00Z = 10-01 00:00 local; one failed-validation retry still fits) |
| upload + 2-5 min | validation COMPLETE (8/8 of our uploads) |
| upload + 6-14 min | first public game of the new sub; vrp10_esw 56600971 stops getting games |
| 09-30 23:59Z (10-01 02:59 local) | deadline; the last 2 uploads are the final pair |
| 10-01 .. 10-15 | final Bradley-Terry over the pair's October games (team = better sub) |

Steps:
1. `md5sum dist/vrp15_k2fire.tar.gz` must print `1929f224b19f24b16e1d85f1a6740b26` (1,161,399 B, 31 files). Re-verified 09-28 08:12Z.
2. Upload that file as-is on the competition's Submit page. Suggested description:
   `vrp15_k2fire: vrp12_pfs + KERNEL2 v3 FIRE_CASH=26|29|2338|2438 md5 1929f224`.
3. Wait for COMPLETE. Note the new submission id.
4. Check the FIFO with `python3 S/livewatch21/api.py eps 56600971` (vrp10 must stop receiving games) and `... eps <new id>` (games appear).
   If validation FAILS, re-upload the same file once; nothing is displaced by a failed sub (verify the same way).
5. **Do not upload anything else before the deadline**, v2 included.
6. Hand me the sub id. SRCSYNC (mine, per PACKV3 §Upload checklist): re-key the `_pin` row `vrp15_k2fire` to the id, merge `ship_vrp15_k2fire`
   (2d959515 + b78bf1e4 + 796c979d on kernel2v3 63f74064) into master, rsync master src to the trainers, BUILD-STORY ship entry.

**How LIVEWATCH will read it (LIVEWATCH22 = the livewatch21 scripts pointed at the new id; read-only API + replays).**
- Per game from the replay: our step-0 action must be the PFS h0 (farmer NORTH, `BUY_PRODUCT WHEAT 53`, 4 x `HIRE`); the rival's step-1 money
  gives the latch (fired iff in {26, 29, 2338, 2438}); status ERROR/TIMEOUT count must be 0.
- **Integrity bar, not an A/B:** fire rate ≈ 9 % (roughly 4-15 % over 100 games), 0 errors, no fired game on a value outside the list.
  At ~8-12 games/h that is ~500-600 games and ~50 fired games by 09-30 21:00Z if uploaded today.
- The fired games are reported descriptively (W-L per listed value next to vrp12's live record against the same values). The band rows imply
  roughly +1 win per 4 fired games (2438: +11 on n41), but ~50 games against a noisy baseline cannot confirm or refute that.
  Undoing the upload is justified only by an integrity failure (errors, wrong h0, fires off-list).

## 5. BUILD-STORY entry (appended to docs/strategy/BUILD-STORY.md)
> **2026-09-28 08:20Z FINALBRIEF1: the final-pair decision brief (KERNEL2 v3 recommended, not uploaded).** JUDGE-MH4V2 closed: v2
> (ZERO_CASH=488|1088|1303|1409) GATE2 PASS on all 9 legs, band-276 +43, A z +6.70, B t +5.79, but -1 on fresh faithful live seats and +0.6/100
> once its 7-8 % unmeasured fires are filled. V3BRANCH1 final re-score: v3 (FIRE_CASH=26|29|2338|2438) GATE2 PASS, band +22 (+23/-1), A z +5.27,
> B t +4.44, faithful59 -2, fires on 9 % of our games, live-weighted +1.9..+2.5/100 ≈ +2-4 October ranks, 0 flips (never loses) on the 60
> newest live games, package = src tree 52/52. Recommendation: upload dist/vrp15_k2fire.tar.gz (md5 1929f224) once by 09-30 21:00Z; the FIFO
> retires vrp10_esw and the final pair is vrp12_pfs + vrp15_k2fire. Neither candidate reaches top 5 (~30 MELON flips needed); V56 = PFS vs the
> top field. Doc 2026-09-28-decision-brief.md.

**Executed (SHIPSYNC1):** the user uploaded option B, dist/vrp15_k2fire.tar.gz (md5 1929f224), at ~2026-09-28 08:20Z as sub **56634350**. The final pair is vrp12_pfs 56612145 + vrp15_k2fire 56634350, and vrp10_esw 56600971 was retired by FIFO. No second upload. master = 19819373 (ff to ship 796c979d plus the submission/ sync). Watch it with `python3 S/livewatch22/lw22.py 56634350`.
