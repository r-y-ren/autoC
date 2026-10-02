# vrp11_pf upload plan (PKGPF1, prepared 2026-09-27 13:45Z, NOT uploaded)

Package: `dist/submission_res940_vrp11_pf.tar.gz` md5 **d3afb07e2e9fe0c96f54b31e86e22ae0** (531,085 B), built FROM src by
`scripts/package_submission.py` defaults (PKGFIX1: theta7659 94a8ffd2, head_940 769ff15e, eswork_theta g30 6928257a) in worktree
/mnt/e/_work/kagg3_wt_placefeed1, branch `ship_vrp11_pf` (edd34c5c switch, ba13a4ff tests) on top of placefeed1 f67fddc9.
Status: **fallback candidate.** PLACEFEED2 verdict stays NO SHIP by the every-leg rule (faithful-59 net −3); this package exists so
the user can choose it for the second final slot.

## Slot
Replaces **vrp9_cs 56600958** (the weaker of the live pair per LIVEWATCH20: vrp10 > vrp9, P 0.004). vrp10_esw 56600971 stays.

## What changes vs vrp10_esw (56600971)
- One switch: `src/kagg3/core/plan.py` `PLACEFEED_ON = False -> True` (same mechanism as vrp9_cs CARE_RIDE_ON/SLIVER_ON: a module constant).
- Tarball: 30 files, 29 byte-identical to the vrp10_esw tarball; only `kagg3/core/plan.py` differs (the PLACEFEED1 code from f67fddc9
  + the switch). theta.npy / residual_head.npz / eswork_theta.npy / route_vrp_c.so / main.py identical.
- Effect: sheep/goose placed today get FEED + CARE on the placement night (first wool fire 6 not 5, first egg 4 not 3); the wheat is
  reserved/bought on the turn-1 row. Cost: wheat/milk sells displaced (see faithful-59).

## Gate table (docs/strategy/2026-09-27-placefeed2.md, paired A = vrp10_esw, B = + PLACEFEED_ON, both seats)
| leg | n | W A→B | flips | Δours (t) | Δtheirs (t) | Δmargin (t) | rule |
|---|---|---|---|---|---|---|---|
| FRESH300 (sim) | 300 | 265→273 | +12/−4 = +8 | +261 (2.27) | −763 (−9.25) | +1,023 (7.64) | pass |
| V56 tapes dev50 (real engine) | 100 | 90→96 | +6/−0 = +6 | +66 (0.40) | −876 (−5.45) | +941 (4.37) | pass |
| **faithful-59 (real engine)** | 59 | 17→14 | +3/−6 = **−3** | −1,211 (−1.57) | −317 (−0.77) | −894 (−0.84) | **FAIL** |
| VLOSSBED VB 0-12 (reacting) | 52 | 52→52 | 0 | −45 (−0.18) | −444 (−1.88) | +399 (1.59) | pass |
| NEARMISS1 17 tape seats × 2 | 34 | 4→6 | +2/−0 = +2 | −259 (−0.80) | −821 (−4.72) | +562 (1.75) | pass |
| POOL4 10 kernels × LIVE250 0-4 × 2 | 100 | 98→100 | +2/−0 = +2 | −292 (−1.93) | −597 (−4.14) | +305 (1.88) | pass |
| pooled | 645 | 526→541 | +25/−10 = +15 | −42 (−0.42) | −691 (−10.36) | +649 (5.11) | |

## Package smoke (packaged main.py as a file agent vs reacting V56, real engine, live clock, actTimeout 600)
Driver: scratchpad `pkgsmoke.py` (ev._play with me_path = packaged main.py, LIVE250 seeds + pinned towns, run from /root/stage_placefeed2).
- ON package, dev board 0 (ep 110946917) seat 0: **78,340 / 74,613**, act md5 e4e444aa == in-repo PLACEFEED_ON row (ident_on / clk_on) to the coin.
- OFF package (vrp10_esw tarball), same board/seat: **80,321 / 74,385**, act md5 fcc6d067 == clk_off row to the coin.
- 10 games (dev 0-4 × both seats): 10/10 scores and act md5 identical to S/placefeed2/clk_on.tsv.

## Live clock (same 10 games, 2 workers, box load ~11)
Worst turn **0.394 s** (turn ≥ 1; first turn incl. module load max 0.293 s), p99 max 0.274 s. Bar 0.65 s: PASS
(PLACEFEED2 saw 0.654 ON / 0.621 OFF at 6-wide load; that tail was load, not the switch).

## Tests (worktree, branch ship_vrp11_pf)
`pytest tests/_pin.py tests/test_placefeed.py` exit 0 (10 passed). test_placefeed now pins its OFF arm explicitly (the shipped
default is ON) and asserts the ship default; `_pin.SHIPPED_PACKAGES["vrp11_pf"]` = ref edd34c5c. `SHIPPED` NOT moved (a4c5cc9e).
Not run: tests/test_package_defaults.py (asserts byte-equality with vrp10_esw; plan.py now differs by design).

## Upload steps (user)
1. Kaggle: submit `dist/submission_res940_vrp11_pf.tar.gz` (check md5 d3afb07e first). FIFO: it retires the oldest active sub;
   make sure the two final uploads before 09-30 23:59Z are vrp10_esw 56600971 + this one (i.e. vrp9_cs 56600958 is the one displaced).
2. After the sub id <SUB> is known: on ship_vrp11_pf re-key `SHIPPED_PACKAGES["vrp11_pf"]` to <SUB>; merge ship_vrp11_pf into selfplay1
   (conflicts expected only in docs/BUILD-STORY); set `_pin.SHIPPED` to the merge commit that carries PLACEFEED_ON = True; run
   `tests/_pin.py tests/test_placefeed.py tests/test_ship_vrp10_esw.py`.
3. master: fast-forward to that commit (master = latest upload, src == vrp11_pf tarball kagg3/); `submission/` gets the vrp11_pf payload
   + tarball + UPLOAD.md row (sub, date, md5 d3afb07e).
4. Trainers (protocol: train only on the latest shipped code): append `,PLACEFEED_ON=True` to the switch strings in S/eswork1/run_remote.sh,
   S/rlfast1/launch_ra1.sh, S/nvtheta1/nvt.py BASE_SW (or rsync the new master src), re-verify board 0 rows, relaunch by literal PID.
5. `S/livewatch17/api.py eps <SUB>` at the next status; update memory master-branch-rule.

**SUPERSEDED 13:55Z:** this package carries the OPEN_PUMP bug found by PLACEFEED3 (docs/strategy/2026-09-27-placefeed3.md); do NOT upload. Tarball moved to dist/superseded/. Use vrp12_pfs (md5 2532e456), plan docs/strategy/2026-09-27-placefeed3-upload-plan.md.
