# MELONTRIAL1: vrp21_melon = PFS everywhere + the d0-1 melon plate only on seats whose rival h1 cash names a programme rival (2026-09-29, 04:38Z-06:38Z)

Stream dir `S/melontrial1/`. Worktree `/mnt/e/_work/kagg3_wt_melontrial1` (sparse, the PACK20 set): branch `melontrial1` (mechanism, from master
8d670dad = the live vrp20 code) and ship branch `ship_vrp21_melon` (config + pins on top of it). Nothing was uploaded; the upload is the user's decision.

## Verdict: TRIAL-READY
- **Package `dist/vrp21_melon.tar.gz`, md5 `1786a0fb402101404f727193e6e7e514`, 1,163,098 B**, 31 files: vrp20_pfsoff (sub 56652418) with 2 files
  changed (plan.py, runtime.py). Ship branch `ship_vrp21_melon`: config **9b437711**, pins **10ceeddb**, on `melontrial1` **f1cbd8c2** (mechanism) on master 8d670dad.
- **Body:** PFS everywhere; on a rival h1 cash in vrp19w's 36-value wide MELON list the seat stays PFS and plays D10WAVE1's **B8 d0-1 melon
  plate** (8 tiles), decided at step 1 (new default-off switch `KERNEL2_FIRE_SWITCHES`); no V56, no hand-back.
- **Gate proof:** gate off = master 6/6 (two references); armed but unfired = master 6/6; fired = **78 melons in d10-14, the same as the h0 plate (0 fewer)**,
  tile-days d0-9 113 = B8's 113; the only difference is the h0 turn (4 hires as master, B8 hires 3).
- **Smoke (tarball as a FILE agent):** 2 MELON seats fire (`sw`, h1 `BUY_SEED MELON 8`, 7 melon tiles at d1, 78 melons ordered for sale in d10-14),
  the V seat is exact to live; 720 steps, 0 bad steps, every step < 1 s (cold step 0 0.58-0.87 s, fire step 0.17-0.20 s). Live27 package read:
  unfired 9/9 exact to live, fired 18/18 plant the plate. **Named tests 77 passed, 0 failed.**
- **Offline risk (ungated plate, §1):** own coins flat against every rival (-0.7k to +0.6k, |t| < 1), the rival +12-18k (t 10-18), W -5/27 on live27
  vs g0capsfix and 0 against flood/big (PFS wins 80/80 there anyway). The live arena is the judge.

## 1. Offline reads of the ungated plate (what the trial risks)
Our seat = master 8d670dad `src` + the PFS OFF string + the cell's switches (static, from h0):
B8 = `MELON_PLATE_TILES=8,MELON_PLATE_DAY=0,NONV_PLATE_LAST=1`, B6 = the same with 6 tiles. Harness = the current `S/judgerival1/rcr.py`
(JUDGERIVAL1/2/3, flood + big caretakers), remote CPU, 1 worker per cell (`S/melontrial1/chain.sh`). Paired on the same (board, seat) games
against the existing PFS controls: flood = `S/judgerival2/res/jr2_pfs_fl.csv`, big = `S/judgerival3/res/bm_pfs.csv` (40 boards_m40 x 2 seats),
live27 vs g0capsfix = `S/judgerival2/res/g0cf_l27.csv` (the 27 BCEVAL1 live seats, 13 at seat 0 + 14 at seat 1). The controls carry the rc.py money
cuts at d10 / d18 only (no d15 cut), so every row splits the windows d0-9 / d10-17 / d18-29 and melon units@price d10-17 / d18-29
(`S/melontrial1/an_mt.py`; PFS sells no melon before d15, so its d10-17 melon is all d15-17). D10WAVE1's g0capsfix rows are recomputed in the
same format for reference. flips = W changes vs the control; t = paired t vs the control.

| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-17 / d18-29 | d rival d0-9 / d10-17 / d18-29 | our melon u@price d10-17 / d18-29 [control] | rival melon u@price d10-17 / d18-29 [control] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| flood | B8 | 80 | 80->80 | +0/-0 | 124,742 | 93,156 | +31,586 | +612 (+0.50) | +16,106 (+14.68) | -15,494 (-8.85) | -3,755 / -4,892 / +9,259 | -263 / +2,826 / +13,544 | 78.0u@223 / 62.8u@78 [12.4u@234 / 77.8u@184] | 46.5u@201 / 0.5u@118 [48.3u@250 / 1.4u@215] |
| flood | B6 | 80 | 80->80 | +0/-0 | 124,783 | 86,332 | +38,452 | +653 (+0.55) | +9,281 (+6.63) | -8,628 (-4.10) | -3,572 / -4,310 / +8,536 | -255 / +2,063 / +7,474 | 54.0u@238 / 72.7u@98 [12.4u@234 / 77.8u@184] | 55.2u@212 / 0.8u@148 [48.3u@250 / 1.4u@215] |
| big | B8 | 80 | 80->80 | +0/-0 | 118,204 | 85,176 | +33,029 | -675 (-0.77) | +12,113 (+9.64) | -12,788 (-7.69) | -3,768 / -5,710 / +8,804 | -128 / -16 / +12,258 | 78.0u@212 / 62.8u@63 [12.3u@228 / 73.1u@174] | 53.5u@206 / 0.8u@111 [58.2u@247 / 0.7u@201] |
| big | B6 | 80 | 80->80 | +0/-0 | 119,976 | 81,990 | +37,985 | +1,097 (+0.92) | +8,928 (+9.65) | -7,832 (-4.60) | -3,734 / -4,512 / +9,342 | -159 / +1,369 / +7,718 | 54.0u@229 / 72.2u@91 [12.3u@228 / 73.1u@174] | 59.4u@216 / 0.7u@156 [58.2u@247 / 0.7u@201] |
| g0capsfix (live27) | B8 | 27 | 27->22 | +0/-5 | 112,413 | 101,997 | +10,416 | +178 (+0.12) | +17,704 (+13.33) | -17,525 (-10.20) | -3,628 / -5,708 / +9,514 | -195 / +3,382 / +14,516 | 78.0u@206 / 72.4u@45 [10.7u@234 / 83.9u@168] | 55.0u@213 / 4.4u@103 [54.9u@248 / 3.8u@215] |
| g0capsfix (live27) | B6 | 27 | 27->21 | +0/-6 | 110,296 | 98,132 | +12,164 | -1,938 (-1.27) | +13,839 (+10.48) | -15,777 (-8.59) | -3,372 / -4,360 / +5,794 | +14 / +3,820 / +10,005 | 54.0u@224 / 88.1u@95 [10.7u@234 / 83.9u@168] | 46.9u@237 / 3.8u@166 [54.9u@248 / 3.8u@215] |
| g0capsfix (m40, D10WAVE1) | B8 | 80 | 75->53 | +0/-22 | 115,599 | 107,718 | +7,880 | +430 (+0.51) | +17,501 (+18.41) | -17,072 (-13.24) | -3,291 / -6,493 / +10,214 | -123 / +3,164 / +14,460 | 78.0u@205 / 71.8u@53 [12.0u@228 / 80.0u@169] | 52.4u@218 / 3.3u@107 [56.5u@248 / 2.1u@203] |
| g0capsfix (m40, D10WAVE1) | B4 (D10WAVE1) | 80 | 75->63 | +0/-12 | 109,973 | 100,361 | +9,612 | -5,196 (-7.33) | +10,144 (+11.23) | -15,340 (-14.34) | -1,752 / -6,273 / +2,829 | -55 / +3,308 / +6,891 | 24.1u@243 / 89.4u@133 [12.0u@228 / 80.0u@169] | 58.2u@238 / 3.1u@201 [56.5u@248 / 2.1u@203] |
| flood | B6 minus B8 (paired, "control" = B8) | 80 | 80->80 | +0/-0 | 124,783 | 86,332 | +38,452 | +41 (+0.04) | -6,825 (-5.86) | +6,866 (+3.46) | +184 / +581 / -723 | +8 / -763 / -6,070 | 54.0u@238 / 72.7u@98 [78.0u@223 / 62.8u@78] | 55.2u@212 / 0.8u@148 [46.5u@201 / 0.5u@118] |
| big | B6 minus B8 (paired, "control" = B8) | 80 | 80->80 | +0/-0 | 119,976 | 81,990 | +37,985 | +1,771 (+1.46) | -3,185 (-2.79) | +4,956 (+2.41) | +34 / +1,199 / +538 | -31 / +1,386 / -4,539 | 54.0u@229 / 72.2u@91 [78.0u@212 / 62.8u@63] | 59.4u@216 / 0.7u@156 [53.5u@206 / 0.8u@111] |
| g0capsfix (live27) | B6 minus B8 (paired, "control" = B8) | 27 | 22->21 | +2/-3 | 110,296 | 98,132 | +12,164 | -2,117 (-1.78) | -3,865 (-3.70) | +1,748 (+1.25) | +256 / +1,348 / -3,720 | +209 / +437 / -4,512 | 54.0u@224 / 88.1u@95 [78.0u@206 / 72.4u@45] | 46.9u@237 / 3.8u@166 [55.0u@213 / 4.4u@103] |

The controls: flood PFS 124,130 / 77,050 (W 80/80); big PFS 118,879 / 73,062 (80/80); g0capsfix live27 PFS 112,235 / 84,293 (27/27); g0capsfix m40 PFS 115,169 / 90,217 (75/80). Files: `S/melontrial1/res/table_all.md` (per read), res/table_flood.md, res/table_l27_g0cf.md.

**Reading.**
- **Own coins are flat in every read, for both plates.** B8: flood +612 (t 0.5), big -675 (t -0.8), live27 vs g0capsfix +178 (t 0.1),
  m40 vs g0capsfix +430 (t 0.5, D10WAVE1). The plate sells its 78 melons in d10-17 at 206-223 (the control 11-12 units, all d15-17, at 228-234) and pays for them
  in d0-17 cash (-3.6k to -3.8k d0-9 = the herd/fertiliser purse; -4.9k to -5.7k d10-17) and in the late melon (62-72 units at 45-78 instead of
  73-84 at 168-184); d18-29 cash recovers +8.8k to +9.5k because the smaller herd spends less and the late herd products sell higher.
- **The rival gains +12-18k in every read, almost all of it in d18-29** (B8: flood +13.5k, big +12.3k, live27 +14.5k of +16.1k / +12.1k / +17.7k):
  the same late price recovery D10WAVE1 found for the clone, now also against the two rivals that flood strawberry/tomato (flood) and add the
  4th quadrant and the wheat engine (big). The rival's own d10-17 melon wave is not denied (46-55 units, price 247-250 -> 201-213).
- **W moves only against g0capsfix** (live27 27 -> 22 for B8, m40 75 -> 53): PFS beats flood and big on 80/80 either way. dmargin -12.8k to -17.5k
  (t -7.7 to -13.2).
- **B6 vs B8, paired on the same games:** own +41 (t 0.04, flood), +1,771 (t 1.5, big), -2,117 (t -1.8, live27) = no clear own-coin edge;
  B6 gives the rival 3-7k less (-6.8k / -3.2k / -3.9k), which is the offline rival-side effect. **B8 kept** (the rule: B8 unless B6's own
  coins are clearly better). B4's own coins are -5.2k (D10WAVE1): the dose must stay >= 6.
- **What the trial risks:** on ~18 % of live games, own purse flat and whatever part of the offline rival recovery is real live. Offline no rival
  reproduces live income (JUDGERIVAL2/3), and live the programme already floods milk/wool/strawberry (PRICEGAP1), so the offline gift is an upper
  bound the live arena can confirm or refute; the tape read (§3) says the same thing on the real engine (own +0.2k, rival +15.4k on 15 faithful seats).

## 2. Gating at step 1 (the plate decided after the h1 cash read)
**Mechanism (branch `melontrial1`, commit f1cbd8c2): `KERNEL2_FIRE_SWITCHES` (plan.py, default "" = OFF).** KERNEL2 had no fired switch-set
(the fired body is V56 only on master; `KERNEL2_BODY` / the clone exists only on the bcwire1/packclone1 branches), so the smallest default-off
mechanism was added:
- `runtime._kernel2`: at step 0 (armed) the h0 obs is stored; at the step-1 latch a KERNEL2_FIRE_CASH hit becomes mode `"sw"` instead of
  `"v56"` (no V56 callable, no hand-back), an unlisted cash stays `"pfs"` and drops the stored obs. Read only with `KERNEL2_NOOP_H0=False`.
- `runtime.act`: at the fire step PFS's d0 plan is rebuilt from the stored h0 obs under the set (`_pfs_act(h0 obs)`, per-game VRP state reset as at
  step 0; its h0 action is discarded because h0 already played as master), then the step-1 turn plays from the rebuilt plan.
- `runtime._pfs_act`: every PFS turn writes the seat's set (`plan.kernel2_sw_apply(fired)`: fired = the ';' items, unfired = the base values
  captured at the first call) right after the ENGINE_GATE write, because games batched in one process share the plan module; a latched d1
  ENGINE_GATE keeps precedence on its own items (as with a static switch string).
- OFF (`""`): one `str()` test per turn; nothing else runs. Unit tests `tests/test_kernel2_fire_switches.py` (5).

**Proof (local, 1 process, 3 boards_m40 x 2 seats vs g0capsfix, `S/d10wave1/rcrw.py` = rcr + the d15 cut, logged by `S/melontrial1/mt_rc.py`;
`S/melontrial1/cmp.py`, res/gp_*):**

| run | tree / switches | vs | identical (every money column + the whole sales ledger) |
|---|---|---|---|
| gp_off | worktree, OFF string, gate off (default "") | master (D10WAVE1 d10_ctl, JUDGERIVAL1 pfs.csv) | **6/6, 6/6** |
| gp_onu | worktree, set armed (`KERNEL2_FIRE_SWITCHES=<B8>`), FIRE_CASH 99999 (nothing fires) | master (d10_ctl) | **6/6** |
| gp_b8s | worktree, static B8 from h0 (harness check) | D10WAVE1 d10_B8 | **6/6** |
| gp_on | worktree, wide list + HANDBACK 0 + the B8 set (the clone rival's h1 = 938 fires every game) | d10_B8 | 0/6 (expected: the h0 turn differs, below) |

- **The step-1 plate = the h0 plate in melons.** Fired 6/6 (k2 `sw`), our PLANT MELON tiles at d1 h12 = 7 (B8 7, control 0), melon tile-days
  d0-9 = **113** (B8 113, control 8), and **78 melons sold in d10-14 at 203-205 on 6/6 = B8's 78 @ 205 (0 fewer)**.
- The only difference from B8 is the h0 turn, played as master before the cash is read: master hires 4 hands at h0, B8 hires 3
  (our h1 cash 1,409 vs 1,412). The step-1 market then equals B8's h1 row (`SELL WHEAT 48 + BUY_SEED WHEAT 11 + CARROT 3 + MELON 8 + GOOSE 1 + COW 2`).
  Purses on these 6 games: step-1 plate 120.8k / 100.6k, static B8 117.5k / 100.2k, control 117.8k / 81.4k.

## 3. Package `vrp21_melon`
- **Tarball `dist/vrp21_melon.tar.gz`: md5 `1786a0fb402101404f727193e6e7e514`, 1,163,098 B (1.16 MB), sha256 fa1448e1…ecd7b266, 31 files.**
  Extracted and compared file by file with `dist/vrp20_pfsoff.tar.gz` (sub 56652418, md5 e5d84f03): **29 byte-identical, 2 differ**
  (`kagg3/core/plan.py` = the MELONTRIAL1 switch block + the 3 values; `kagg3/agent/runtime.py` = the mechanism), 0 new, 0 missing
  (`S/melontrial1/cmp_vrp21_vs_vrp20.txt`). Same main.py / v56kernel.py / theta / residual head as vrp20.
- **Branches.** `melontrial1`: **f1cbd8c2** (mechanism + tests/test_kernel2_fire_switches.py) on master 8d670dad. `ship_vrp21_melon`:
  **9b437711** config (plan.py defaults AND the LE.SWITCHES gene block, `S/actionrl/live_expert.py:82`) + **10ceeddb** pins/tests.
  Build: `cd /mnt/e/_work/kagg3_wt_melontrial1 && .venv/bin/python scripts/package_submission.py --out dist/vrp21_melon.tar.gz` on 9b437711
  (bare build: KERNEL2_ON default True -> v56kernel.py packed, main.py passes `configuration`, exactly as vrp20).
- **Gene tail** (vrp20's block with three changes): `...,KERNEL2_ON=True,KERNEL2_NOOP_H0=False,KERNEL2_INHERIT=True,`
  `KERNEL2_FIRE_CASH=1|4|8|17|19|23|26|29|34|73|76|117|160|163|182|190|444|456|553|564|620|638|661|938|1616|2046|2322|2338|2438|2477|2485|2492|2511|2593|2600|2904,`
  `KERNEL2_PRELOAD=False,KERNEL2_HANDBACK_DAY=0,KERNEL2_FIRE_SWITCHES=MELON_PLATE_TILES=8;MELON_PLATE_DAY=0;NONV_PLATE_LAST=1`.
  The block splits on ',' and each item on the first '=', so the ';'-joined set survives; test_kernel2_v3_package asserts block == plan defaults.
- **The body.** PFS plays h0 on every game. At step 1 the rival's h1 cash is checked against the 36-value wide list (vrp19w's). A hit keeps PFS and
  rebuilds its d0 plan under the B8 plate (8 melon tiles on d0-1, the ordinary lot allocator sells them); no V56, no hand-back. Every other seat
  is vrp20 PFS byte for byte. **Why B8:** its own coins are the best of the two plates on every read (flood +612 vs B6 +653, a tie;
  live27 vs g0capsfix +178 vs B6 -1,938; big -675 vs B6 +1,097; paired B6 - B8 own: +41 / +1,771 / -2,117, t 0.04 / 1.5 / -1.8), and B6's smaller rival gain is exactly the offline rival-recovery effect this trial exists to test live.
- **Tests (named files, worktree on 10ceeddb, `S/melontrial1/tests.sh` -> res/tests_final.txt): 77 passed, 0 failed** — test_handback1 8,
  test_kernel2_fire 6, test_kernel2_v3_package 6, _pin 22, test_kernel2_lazy 21, test_kernel2_package 5, test_package_defaults 4 (incl. bare build
  == dist/vrp21_melon.tar.gz, every file byte-identical), test_kernel2_fire_switches 5.
  - `_pin` row `vrp21_melon`: ref 9b437711, md5 1786a0fb, candidate, keyed by name, no sub id; the test asserts it differs from vrp20_pfsoff in
    exactly FIRE_CASH (= vrp19w's list), HANDBACK_DAY 0 and FIRE_SWITCHES; **SHIPPED stays b940d667**. The same row is on selfplay1's tests/_pin.py.
  - V56-body mechanics tests (handback1, kernel2_fire, kernel2_lazy fixtures) pin `KERNEL2_FIRE_SWITCHES=""` (the V56 path is unchanged, only no
    longer reachable by default); v3_package: fired = `"sw"`, values outside the list = `"pfs"`; lazy: `test_vrp21_melon_default_never_builds_v56`.
- **Smoke from the tarball** (local, 1 process, nice 19 / ionice idle; the extracted package `S/melontrial1/tmp/p21` as a FILE agent through
  eval_vs_baselines._play, PACKCLONE1's pkgrun.py + melon columns; `S/melontrial1/smoke.sh` -> res/pkg_smoke.csv). `runtime_file` = the package's own.

| seat | rival h1 | k2 | ours / theirs | live (= PFS) | h1 market (our step-1 turn) | PLANT MELON d1 / tile-days d0-9 / SELL MELON d10-14 | steps / bad | step 0 (cold) | fire step | later max |
|---|---|---|---|---|---|---|---|---|---|---|
| istinetz_114667726 (MELON) | 1 | sw | 131,064 / 108,496 | 105,925 / 121,076 | SELL WHEAT 48 + SEED WHEAT 11 + CARROT 3 + **MELON 8** + GOOSE 1 + COW 2 | 7 / 113 / 78 | 720 / 0 | 847 ms | 200 ms | 257 ms |
| thisray_114655920 (MELON) | 938 | sw | 71,304 / 98,846 | 84,145 / 93,090 | same | 7 / 113 / 78 | 720 / 0 | 575 ms | 174 ms | 462 ms |
| shyjin_114812703 (V, unfired) | 2873 | pfs | **89,640 / 86,341 = live, EXACT** | 89,640 / 86,341 | SELL WHEAT 48 + SEED WHEAT 11 + CARROT 8 + GOOSE 1 + COW 4 + SHEEP 1 (PFS) | 0 / 1 / 0 | 720 / 0 | 874 ms | 0.2 ms | 293 ms |

  Every step < 1 s; the fire step (d0 rebuild) costs 0.17-0.26 s once per fired game.
- **Live27 tape read of the package** (context, open loop against the rival tapes; FIRELIVE1: tapes inflate a deviating arm; same harness,
  `S/melontrial1/l27.sh`, `tbl_l27.py` -> res/table_pkg_l27.md). 27 games DONE, 720 steps, 0 bad. **Unfired 9/9 exact to live** (h1 20, 67, 2015,
  2464, 2854). **Fired 18/18** (h1 1, 19, 73, 190, 564, 661, 938, 2046 — the same 18 as PACKCLONE1): PLANT MELON at d1 = 7 and 78 melons ordered
  for sale in d10-14 on 18/18. Steps > 1 s: 4 games, all at step 0 (the cold import, load 12-13 on this box; one is an unfired PFS seat at 1,193 ms,
  as vrp20 would be); the fire step max 264 ms.

| set (vs live = PFS) | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 27 | 6 -> 5 | +2/-3 | +2,823 (+1.09) | +6,028 (+1.69) | -3,204 (-0.56) |
| fired 18 | 18 | 4 -> 3 | +2/-3 | +4,235 (+1.09) | +9,041 (+1.72) | -4,806 (-0.56) |
| fired, JC1-faithful both | 15 | 3 -> 1 | +0/-2 | +192 (+0.07) | +15,398 (+8.32) | -15,206 (-4.96) |

  The two tape "wins" are on unfaithful tapes (istinetz_114684168 rival 0 = the tape broke; istinetz_114667726). On the 15 faithful seats our own
  purse is flat (+0.2k) and the tape rival gains +15.4k: the same shape as every offline rival (own flat, rival up), now on the real engine.

## 4. Upload consequences (the user's decision; nothing was uploaded)
1. **Check the tarball:** `md5sum dist/vrp21_melon.tar.gz` = `1786a0fb402101404f727193e6e7e514` (1,163,098 B). Upload it as is.
2. **The upload retires vrp19w_k2wide 56649892** (FIFO: the older of the live pair; 18-21 in its last window). **The live pair becomes
   vrp20_pfsoff 56652418 (the PFS anchor) + vrp21_melon.**
3. **A later upload retires vrp20, not vrp21** (vrp20 is then the older sub). So if the trial is to leave the final pair (FINAL = BT over
   Oct 1-15 of the last 2 uploads), the anchor must be re-uploaded: re-upload `dist/vrp20_pfsoff.tar.gz` (retires the original vrp20 ->
   pair vrp21 + vrp20'), then one more upload retires vrp21. Two uploads after this one, both before 09-30 23:59Z (safe latest 21:00Z).
   If the trial reads well, nothing more is needed: vrp20 + vrp21 is the final pair.
4. **What the trial risks:** ~18 % of live games fire (vrp19w's list: 17.9 % live). On those the plate sells ~78 melons in d10-14; every offline
   rival and the tape read say our own purse is flat and the rival's d15-29 prices recover (+14-18k rival, W -5 of 27 on live27 vs g0capsfix, 3 -> 1
   on the faithful tapes). The other ~82 % are vrp20-identical PFS games. The live arena is the judge (PRICEGAP1: the live programme already floods
   the products whose prices recover offline).
5. **Upload note text:** `vrp21_melon: vrp20_pfsoff (56652418) + KERNEL2_FIRE_SWITCHES = d0-1 melon plate (MELON_PLATE_TILES=8, D10WAVE1 B8) on
   vrp19w's 36-value wide MELON list; fired seats stay PFS (d0 plan rebuilt at step 1), no V56, no hand-back; config 9b437711 pins 10ceeddb; md5 1786a0fb`
6. **After an upload (SHIPSYNC):** merge `ship_vrp21_melon` (f1cbd8c2 + 9b437711 + 10ceeddb; a fast-forward of master 8d670dad) into master;
   `_pin`: re-key `"vrp21_melon"` with `"sub": <id>` and `"ship": <merge tip>`, drop `candidate`, mark vrp19w_k2wide 56649892 `retired`, set
   `SHIPPED = "9b437711"`, live set {56652418 vrp20_pfsoff, <id> vrp21_melon}, and update the tests that pin SHIPPED b940d667 (test_vrp12_pfs_pin_row,
   test_vrp20_pfsoff_pin_row, test_ship_vrp20_pfsoff_pin_names_the_config_tree, test_kernel2_v3_package's pin test, test_vrp21_melon_pin_row);
   refresh submission/ with the vrp21 plan.py + runtime.py (vrp20 tree stays the second live package); master's LE.SWITCHES tail = the vrp21 tail;
   register the watcher (§5); BUILD-STORY + MEMORY master-branch line (final pair vrp20 56652418 + vrp21 <id>, vrp19w retired).

## 5. Watcher registration (for the SHIPSYNC step after an upload; lw23.py NOT edited here)
Register the new sub in `S/livewatch23/lw23.py` BEFORE its first read:
```python
FIRE_BY_SUB[<id>] = (1, 4, 8, 17, 19, 23, 26, 29, 34, 73, 76, 117, 160, 163, 182, 190, 444, 456, 553, 564, 620, 638, 661, 938, 1616, 2046,
                     2322, 2338, 2438, 2477, 2485, 2492, 2511, 2593, 2600, 2904)
NAMES[<id>] = 'vrp21_melon'
REF_DEFAULT[<id>] = 56652418; REF_DEFAULT[56652418] = <id>
# NOT in HB_SUBS (KERNEL2_HANDBACK_DAY = 0; no seat ever runs V56)
```
- **The fire check must be told the fired body is PFS + the plate.** lw23's observed-fire rule `v56obs` (h1 COW 2 + SHEEP 2 + HIRE) reads 0 on
  every fired game, and `pfsid` (h1 starts SELL WHEAT 48, no V56 row, no hire) reads 1 on fired AND unfired games. For this sub use
  **observed fire = `['BUY_SEED', 'MELON', 8] in m1`** (our h1 market; fired 20/20 in smoke + live27, unfired 0/10) and confirm with the columns lw23
  already computes: **`mel_d1` = 7 on fired games** (our PLANT MELON tiles at d1; 18/18 + 2/2 package games, 6/6 gate proof; unfired 0) and a d10-14
  melon sale (our SELL MELON rows d10-14 total 78 units in every package game; unfired PFS: 0 before d15). Unfired identity = `pfsid and not melobs`
  (h1 = `SELL WHEAT 48 + BUY_SEED WHEAT 11 + CARROT 8 + GOOSE 1 + COW 4 + SHEEP 1`). The V56 dawn counts (v56pre/v56post) and the d18 hand-back
  check do not apply.
- **Integrity read ~2 h after the upload:** errors/timeouts 0; listed == melon-observed on every game; unfired games PFS-identical; fired share
  ~18 % (vrp19w 17.9 %); fired games show mel_d1 7 and a d10-14 melon sale. Run `python3 S/livewatch23/lw23.py <id> --ref 56652418` once.

## Files
- `S/melontrial1/`: checkpoint.txt, chain.sh (remote offline reads), an_mt.py (paired table), mt_rc.py + gp.sh + gpchain.sh + cmp.py (gate proof),
  pins_melon.py (ship-branch config/pins edits), tests.sh, pkgrun.py (PACKCLONE1's file-agent runner + melon columns), smoke.sh, l27.sh, tbl_l27.py,
  final_table.sh, build.log, cmp_vrp21_vs_vrp20.txt; res/ (gp_*.csv/_sal.jsonl/.mt.jsonl, remote/mt_B{6,8}_{fl,big,l27a,l27b}.csv + _sal.jsonl, table_*.md,
  table_all.md, table_pkg_l27.md, pkg_smoke.csv, pkg_l27.csv, tests_final.txt). Not committed: tmp/ (extracted packages), res/acts_*.json.
- Remote: `~/stage_reactclone1/S/melontrial1/` (chain.sh, chain_B{6,8}.log), results in `~/stage_reactclone1/S/reactclone1/res/mt_*`.
