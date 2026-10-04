"""One pin helper: archive a commit, hash the whole plan, prove which tree ran.

Every "byte-identical" test in this suite makes the same claim -- *this* tree's
planner, with one switch set, decodes the same six-array plan as a named
committed tree -- and every one of them used to make it with its own copy of the
same forty lines.  The copies drifted, and two defects rode in on the drift:

1. **Import order.**  A pin module doubles as a `--digests` script: run as
   `python tests/test_x.py --digests <tmp>/src` it prints the digests of the
   *archived* tree.  That only works if `kagg3` is imported after `<tmp>/src`
   goes on `sys.path` and before anything else can import it.  The shared test
   fixtures (`tests/test_budget_order.py:24`) do their own
   `sys.path.insert(0, "src")` and import `kagg3` on the way in, so a module
   that imported a fixture first silently loaded THIS tree's planner into the
   subprocess and compared the tree with itself -- a pin that can never fail.
   `bootstrap()` below imports `kagg3` first and *asserts* where it came from,
   so the failure mode is now a loud one.

2. **Hand-written digest tuples.**  A tuple of hex strings names no tree.  When
   a shipped default was promoted the tuple went stale with no way to say which
   commit had been right.  `tree_digests()` takes the reference from
   `git archive <commit> src` instead, so the pin always names its other end.

Use it like `tests/test_slotprio.py`:

    import _pin
    _pin.bootstrap()                      # kagg3 FIRST, from the right tree
    import numpy as np
    from kagg3.core import plan as P
    from test_budget_order import _macro  # safe now: kagg3 is already loaded
    ...
    if __name__ == "__main__":
        for n, d in _own_digests().items():
            print(n, d)
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

#: The SHIPPED planner: master `c5f68ac`, the ff commit that records Kaggle
#: upload 56284867 (`lot4t17_slotprio_ft2`) and swaps `submission/` to that
#: tarball's payload -- `LOT4_ON = True`, `LOT4_TURN = 17`,
#: `SELL_SLOT_PRIORITY_ON = True`, `FERT_TIMING_ON = True`.  A SHA and not
#: `HEAD`, so a pin taken against it keeps its meaning after master moves on;
#: `git archive HEAD` is self-referential the moment the switch it pins is
#: committed.
#:
#: It moved here from `4054968` (the pre-FT2 tree of upload 56277270) on
#: 2026-09-17: `FERT_TIMING_ON` was promoted `False -> True` at this commit, so
#: the old ref named a tree that no longer ships and every `_pin.SHIPPED` pin
#: was asserting identity against a *superseded* default.  Every module
#: constant in `src/kagg3/core/plan.py` has the same value at `c5f68ac` as on
#: master today (every family merged since is default OFF), so the nine pins
#: below are byte-identical across the move -- measured, not assumed.
#: It moved again on 2026-09-17 (`c5f68ac` -> `cdbd95c`, the `dropharv` ship
#: commit): `ENDROUTE_ON` was promoted `False -> True` there on the POOLED180
#: read of docs/strategy/2026-09-17-dropharv.md §6, so day 29 grows one sell row
#: and every `_pin.SHIPPED` pin with a terminal board -- `test_carrot_hold`,
#: `test_animal_fwd`, `test_fertreserve`, `test_fertengine`, `test_fertdenial`,
#: `test_lot4`, `test_spread6` -- was asserting identity against a *superseded*
#: default.  `cdbd95c` is the tree
#: `artifacts/submission_flow193_g100_hr_ft2_endroute.tar.gz` was built and
#: smoked from; it becomes an upload commit when the user uploads that package,
#: and every module constant other than `ENDROUTE_ON` is equal at both commits.
#: It moved a third time on 2026-09-18 (`cdbd95c` -> `bfe38d0`, the `stack1ship`
#: PUMPCLIP commit): `OPEN_PUMP_ON` was promoted `True -> False` and
#: `CLIP_CAP_ON` `False -> True` there, as ONE arm, on the 241-board read of
#: docs/strategy/2026-09-17-stack1.md §7.  Day 0 loses its hour-0 wheat leg and
#: every day whose haul would overflow the shed loses its cheapest harvests, so
#: a pin taken at `cdbd95c` now names a planner that does not ship.  `bfe38d0`
#: is the tree
#: `artifacts/submission_flow193_g100_hr_ft2_endroute_pumpclip.tar.gz` was built
#: and smoked from; it becomes an upload commit when the user uploads that
#: package, and every module constant other than those two is equal at both
#: commits.
#:
#: Two pin files deliberately do NOT follow it: `tests/test_shedclip.py` and
#: `tests/test_shedclip2.py` carry their own `PRE_SWITCH = c6da7f0`, because
#: their claim is "OFF is the planner without the cap" and this ref is now a
#: tree whose cap is ON.
#:
#: It moved a fourth time on 2026-09-18 (`bfe38d0` -> `c87299c`, the
#: `stack3ship` PES commit): `ENDROUTE2_ON` and `ENDROUTE2_SPLIT_ON` were
#: promoted `False -> True` there, as ONE cell with PUMPCLIP, on the 241-board
#: read of docs/strategy/2026-09-18-stack3.md.  Day 29's turn budget is re-cut
#: to ENDROUTE's row and the day takes TWO shed trips instead of one, so a pin
#: taken at `bfe38d0` now names a planner whose terminal day does not ship.
#: `c87299c` is the tree
#: `artifacts/submission_flow193_g100_hr_ft2_pes.tar.gz` was built and smoked
#: from; it becomes an upload commit when the user uploads that package, and
#: every module constant other than those two is equal at both commits.
#:
#: Two more files deliberately do NOT follow it, for the same reason the two
#: shed-clip files do not: `tests/test_endroute2.py` and
#: `tests/test_endroute2_split.py` carry their own `PRE_SWITCH` (516e6dc,
#: 76e81f0) plus an `OTHER_SHIPPED` pin, because their claim is "OFF is the
#: planner without this row" and this ref is now a tree that runs it.
#: It moved a fifth time on 2026-09-18 (`c87299c` -> `fe6cf65`, the
#: `stack5ship` ESR commit): `ENDROUTE_ROW2_ON` was promoted `False -> True`
#: and, in the SAME cell, PUMPCLIP was REVERSED -- `OPEN_PUMP_ON` back to True
#: and `CLIP_CAP_ON` back to False -- on the 241-board and 60-engine-board read
#: of docs/strategy/2026-09-18-stack5.md.  Day 29 grows a second late sell row,
#: day 0 gets its hour-0 wheat leg back and no day clips its haul again, so a
#: pin taken at `c87299c` names a planner that does not ship on day 0 OR day
#: 29.  `fe6cf65` is the tree
#: `artifacts/submission_flow193_g100_hr_ft2_esr.tar.gz` was built and smoked
#: from; it becomes an upload commit when the user uploads that package, and
#: every module constant other than those three is equal at both commits.
#:
#: The shed-clip pair STILL does not follow it, and now for the opposite
#: reason: `tests/test_shedclip.py` and `tests/test_shedclip2.py` keep
#: `PRE_SWITCH = c6da7f0` because their subject is the cap, and `_pin.SHIPPED`
#: is a moving ref -- the pin has to name one fixed tree without a cap, not
#: "whatever ships".  `tests/test_endroute2.py`,
#: `tests/test_endroute2_split.py` and `tests/test_endroute_row2.py` keep their
#: own `PRE_SWITCH` (516e6dc, 76e81f0, 903bf79) plus an `OTHER_SHIPPED` pin,
#: because their claim is "OFF is the planner without this row" and this ref is
#: now a tree that runs all four.
#: It moved a sixth time on 2026-09-18 (`fe6cf65` -> `2b6c2ce`, the WIDEPICK
#: ship): `plan.WIDE_PICK_ON` was promoted `False -> True` on WIDEJUDGE's
#: BAND250 +185 t +3.87 / ENGINE28 +1,018 t +1.45 / POOLED278 +269 t +3.24
#: read [docs/strategy/2026-09-18-widepick.md].  A wide day's turn 1 now
#: carries a second stationary PICKUP, so a pin taken at `fe6cf65` names a
#: planner whose wide mornings are one turn shorter than the one that ships.
#: `2b6c2ce` is the tree
#: `artifacts/submission_flow193_g100_hr_ft2_esr_wp.tar.gz` was built and
#: smoked from; it becomes an upload commit when the user uploads that package,
#: and every module constant other than that one is equal at both commits.
#: `tests/test_widepick.py` joins the files that do NOT follow this ref: it
#: keeps `PRE_SWITCH = 5c089fb` for its OFF pin, because its claim is "OFF is
#: the planner without this turn" and this ref is now a tree that takes it.
#:
#: It moved a seventh time on 2026-09-18 (`2b6c2ce` -> `09af88b`, the WIDESHIP2
#: commit): `plan.WIDE_PICK_FREE_ON` was promoted `False -> True` on WIDEPICK2's
#: BAND250 +102 t +2.54 / ENGINE28 +245 t +3.10 / POOLED278 +117 t +3.14 read
#: [docs/strategy/2026-09-18-widepick2.md], d0check PASS.  The wide day's
#: granted turn-1 PICKUP now takes a kind today's BUY row does not deliver
#: instead of the block's lowest-indexed one, and the grant fires on 42.3 rather
#: than 34.7 unit-turns a game, so a pin taken at `2b6c2ce` names a planner
#: whose wide mornings pull the wrong kind.  `09af88b` is the tree
#: `dist/submission_flow193_g100_hr_ft2_esr_wp_wpf.tar.gz` was built and smoked
#: from; it becomes an upload commit when the user uploads that package, and
#: every module constant other than that one is equal at both commits.
#:
#: It moved an eighth time on 2026-09-19 (`09af88b` -> `59021db`, the ACTIONRL8
#: commit): the tree gained the residual action-RL splice (`plan._residual_override`
#: / `_residual_hire`, `plan.RESIDUAL_ON` default False = byte-identical) and
#: the package `dist/submission_res940.tar.gz` (md5 536cf1061ecb6cdd3c8087fa9dad678f)
#: arms it from main.py with the self-play head `head_940.npz`: BAND2-233 OOS
#: +325 t 8.15, theirs -26, flips +3/-2 [docs/strategy/2026-09-19-actionrl8.md].
#: Uploaded 2026-09-19 ~19:50Z as sub 56370365.  Module constants are equal at
#: both commits; the pin names the planner with the head OFF (as the tests run).
#:
#: It moved a ninth time on 2026-09-21 (`59021db` -> `e7a8af84`, the
#: res940_vpost package commit) when sub 56421514 was uploaded.  The package
#: keeps RES940 and additionally arms `MELONVETO_POST_ON`; its module default is
#: still False, so ordinary pin tests retain their head-OFF/default semantics.
#:
#: It moved a tenth time on 2026-09-22 (`e7a8af84` -> `e7df5350`, SHIP_CF):
#: `CARE_FILL_ON` was promoted `False -> True` and appended as switch-gene
#: column 19.  The layout moves 7,725 -> 7,758; the res940 package retains the
#: exact theta7659 and head_940 artifacts and arms CARE_FILL by default.
#:
#: It moved an eleventh time on 2026-09-22 (`e7df5350` -> `a7b92972`,
#: SHIP_OG): `OVERFLOW_GUARD_ON` was promoted `False -> True` and appended as
#: switch-gene column 20.  The layout moves 7,758 -> 7,791; theta7659 and
#: head_940 remain unchanged.
#:
#: It moved a twelfth time on 2026-09-22 (`a7b92972` -> `6e844293`,
#: SHIP_OG2): `OVERFLOW_GUARD_V2` was promoted `False -> True`.  It is
#: runtime-only (agent/overflow.py:guard_v2), not a switch gene, so the layout
#: stays 7,791 and every planner digest is unchanged; theta7659 + head_940 kept.
#:
#: It moved a thirteenth time on 2026-09-22 (`6e844293` -> `252575d5`,
#: SHIP_OG3): `OVERFLOW_GUARD_V3` was promoted `False -> True`.  It is
#: runtime-only (agent/overflow.py:guard_v3), not a switch gene, so the layout
#: stays 7,791 and every planner digest is unchanged; theta7659 + head_940 kept.
#:
#: It moved a fourteenth time on 2026-09-23 (`252575d5` -> `6df6635c`,
#: SHIP_LE): `LATE_EXEC_ON` was promoted `False -> True`.  It is a planner
#: switch (plan.py `_final_slots`/`_derive`, brain.n_free_slots), not a switch
#: gene, so the layout stays 7,791; planner digests move only on boards holding
#: a crop on its final harvest day; theta7659 + head_940 kept.
#:
#: It moved a fifteenth time on 2026-09-24 (`6df6635c` -> `ca9232e7`,
#: SHIP_VRP): `ROUTE_VRP_ON` was promoted `False -> True` (shadow on).  It is
#: runtime-only (agent/route_vrp.py, hooked in runtime.py at dawn), not a
#: switch gene, so the layout stays 7,791 and every planner digest is
#: unchanged; theta7659 + head_940 kept.
#:
#: It moved a sixteenth time on 2026-09-24 (`ca9232e7` -> `0769ad8a`,
#: SHIP_VRP2): `ROUTE_VRP_FIX_FROZEN` and `ROUTE_VRP_VERIFY` were promoted
#: `False -> True` (SALEPIN1 routing-bug fix; branch salepin1 with master
#: 99b309a8 merged, ROUTE_FILL_MODE "ii").  Runtime-only (agent/route_vrp.py),
#: not switch genes: layout 7,791, planner digests unchanged; theta7659 +
#: head_940 kept.  Package dist/submission_res940_vrp2.tar.gz.
#: 2026-09-24 (SHIP_VRP3): `ROUTE_VRP_NEEDS_FIX_ON` promoted `False -> True`
#: (VRPFALLBACK1: harvested wheat rides with the route + trim/top-up by the
#: pickup shortfall; NEEDS_TRIM stays True).  Runtime-only (route_vrp.py),
#: layout 7,791, theta7659 + head_940 kept.  Package
#: dist/submission_res940_vrp3.tar.gz.
#: 2026-09-24 (SHIP_VRP4): master 1b011580 = vrpdeadline1 merged: one
#: perf_counter deadline in route_vrp.apply (SAFETY_S 0.75, RESERVE_S 0.10)
#: + checkpointed solutions restored through VERIFY on timeout.  No switch,
#: no default flip; runtime-only (route_vrp.py), layout 7,791, theta7659 +
#: head_940 kept.  Package dist/submission_res940_vrp4.tar.gz.
#: 2026-09-25 (SHIP_VRP5): `ROUTE_VRP_REPAIR_ON` promoted `False -> True`
#: with `route_vrp.REPAIR_LAST_DAY` 29 -> 20 (VRPREPAIR1/3 bounded crew-drop
#: repair, REPAIR_MS 100 / REPAIR_EJECT_K 4, cut after day 20).  Runtime-only
#: (route_vrp.py), layout 7,791, theta7659 + head_940 kept.  Package
#: dist/submission_res940_vrp5.tar.gz (awaiting user waiver).
#: 2026-09-27 (SHIP_VRP12_PFS, SRCSYNC2): `PLACEFEED_ON` and `PF_PUMPSAFE_ON`
#: promoted `False -> True` at the ship commit `dcacbd33` (branch
#: ship_vrp12_pfs, merged into master); dist/submission_res940_vrp12_pfs.tar.gz
#: (md5 2532e456) uploaded ~15:10Z as sub 56612145.  Final pair = vrp10_esw
#: 56600971 + vrp12_pfs 56612145; vrp9_cs 56600958 retired.  The ref is the
#: config commit (as a4c5cc9e was), whose src/kagg3 == the tarball kagg3/.
#: 2026-09-28 (SHIP_VRP14_K2REAL, PACKV2): `KERNEL2_ON`, `KERNEL2_NOOP_H0` (False),
#: `KERNEL2_INHERIT` and `KERNEL2_ZERO_CASH` ("488|1088|1303|1409") promoted at the
#: config commit `ba61be6f` (branch ship_vrp14_k2real = melonhybrid4 79636f64 +
#: the defaults + the gene block); dist/vrp14_k2real.tar.gz (md5 233430d3).  This
#: ship tree records the state AFTER its upload: FIFO retires vrp10_esw 56600971,
#: final pair = vrp12_pfs 56612145 + vrp14_k2real (re-key the row to its sub id at
#: SRCSYNC).  KERNEL2 is runtime-only (agent/runtime.py), so every plan digest at
#: `ba61be6f` equals `dcacbd33`.  NOT uploaded while this line says "vrp14_k2real".
#: 2026-09-28 (SHIP_VRP15_K2FIRE, PACKV3): the v3 whitelist form -- `KERNEL2_ON`,
#: `KERNEL2_NOOP_H0` (False), `KERNEL2_INHERIT`, `KERNEL2_FIRE_CASH` ("26|29|2338|2438")
#: and `KERNEL2_PRELOAD` (False, lazy V56) promoted at the config commit `b78bf1e4`
#: (branch ship_vrp15_k2fire = kernel2v3 63f74064 + k2lazy test + the defaults + the
#: gene block); dist/vrp15_k2fire.tar.gz (md5 1929f224).  vrp15 and vrp14 are
#: ALTERNATIVE candidates for the one upload; this tree records the state AFTER a
#: vrp15 upload: FIFO retires vrp10_esw 56600971, final pair = vrp12_pfs 56612145 +
#: vrp15_k2fire, vrp14_k2real never uploaded (row kept, marked retired).  Plan
#: digests at `b78bf1e4` equal `dcacbd33` (KERNEL2 is runtime-only).  NOT uploaded
#: while this line says "vrp15_k2fire".
#: 2026-09-28 ~08:20Z (user): vrp15_k2fire UPLOADED as sub 56634350 (SHIPSYNC1: master ff
#: 942b46cb -> 796c979d).  The row stays keyed by name (tests read it); its `sub` field
#: carries the id.  Final pair = vrp12_pfs 56612145 + vrp15_k2fire 56634350; no further uploads.
#: 2026-09-28 (SHIP_VRP17_K2HB, PACKHB1): `KERNEL2_HANDBACK_DAY` (18, HANDBACK2 D18: PFS takes a
#: V56-fired farm back at the dawn of day 18) promoted at the config commit `ec2a6042` (branch
#: ship_vrp17_k2hb = handback1 5f29b272 + the default + the gene block; pins a7fcad46);
#: dist/vrp17_k2hb.tar.gz (md5 11fd0f57).  UPLOADED by the user ~14:15Z as sub 56643352
#: (SHIPSYNC2: master ff 19819373 -> a7fcad46).  FIFO retires vrp12_pfs 56612145.  Final pair =
#: vrp15_k2fire 56634350 + vrp17_k2hb 56643352.  The row stays keyed by name (tests read it);
#: its `sub` field carries the id.  HANDBACK is runtime-only, so plan digests at `ec2a6042`
#: equal `b78bf1e4` and `dcacbd33`.
#: 2026-09-28 (SHIP_VRP18_K2HB2046, PACK18): `KERNEL2_FIRE_CASH` += 2046 (LIVEVAL1 CANDIDATE)
#: promoted at the config commit `599f8881` (branch ship_vrp18_k2hb2046 = vrp17_k2hb a7fcad46 +
#: the whitelist + the gene block; pins 0735ea4c); dist/vrp18_k2hb2046.tar.gz (md5 d6ed14d6).
#: UPLOADED by the user ~16:35Z as sub 56646827 (SHIPSYNC3: master merge of 0735ea4c).  FIFO
#: retires vrp15_k2fire 56634350.  Final pair = vrp17_k2hb 56643352 + vrp18_k2hb2046 56646827;
#: a further upload retires vrp17_k2hb.  The row stays keyed by name (tests read it).
#: 2026-09-28 (SHIP_VRP19W_K2WIDE, PACKWIDE1): `KERNEL2_FIRE_CASH` = the WIDE 36-value list
#: (vrp18's 5 + 31 MELON rival h1 values) promoted at the config commit `81090f6a` (branch
#: ship_vrp19w_k2wide = vrp18_k2hb2046 0735ea4c + the list + the gene block; pins 72570ca8);
#: dist/vrp19w_k2wide.tar.gz (md5 e490347d).  UPLOADED by the user ~19:10Z as sub 56649892
#: (SHIPSYNC4: master merge of 72570ca8).  FIFO retires vrp17_k2hb 56643352.  Final pair =
#: vrp18_k2hb2046 56646827 + vrp19w_k2wide 56649892; a further upload retires vrp18_k2hb2046.
#: The row stays keyed by name (tests read it).
#: 2026-09-28 (SHIP_VRP20_PFSOFF, PACK20): `KERNEL2_FIRE_CASH` = "99999" (no live value listed: the
#: step-1 latch never fires, PFS on every seat; FIRELIVE1's OFF arm, FINALPLAN1's last upload)
#: promoted at the config commit `b940d667` (branch ship_vrp20_pfsoff = vrp18_k2hb2046 0735ea4c +
#: the default + the gene block; pins eeea2793); dist/vrp20_pfsoff.tar.gz (md5 e5d84f03).
#: UPLOADED by the user ~21:25Z as sub 56652418 (SHIPSYNC5: master merge of eeea2793).  FIFO
#: retires vrp18_k2hb2046 56646827.  Final pair = vrp19w_k2wide 56649892 + vrp20_pfsoff 56652418;
#: a further upload retires vrp19w_k2wide.  The row stays keyed by name (tests read it).
#: 2026-09-29 (SHIP_VRP21_CLSEARCH, CLSEARCH1): `REINVEST_DAILY` = "4:200:CSG" (from d4 buy PFS's own d14
#: herd as early as the dawn purse allows, reserve 200, cows first) + `FEED_ALL` = True (the feed-wheat list
#: granted first) promoted in plan.py AND the gene block at the config commit `b1835440` (branch
#: ship_vrp21_clsearch = vrp20 master 8d670dad + the default-off CLSEARCH1 / BRAINSTORM2 branches + the two
#: defaults); dist/vrp21_clsearch.tar.gz (md5 d93d6f5c929c5716f3bed77b31b22457, 31 files == b1835440 blobs).
#: UPLOADED by the user ~13:10Z as sub 56676381 (SHIPSYNC6: master ff 8d670dad -> b1835440, then the
#: submission/ mirror refresh cf68f736; its pins landed on selfplay1 58f81ba3, not here).  FIFO retired
#: vrp19w_k2wide 56649892.  RETIRED (FIFO) itself on 09-29 ~19:55Z by the vrp22_pfs_fp upload 56686308.
#: 2026-09-29 ~19:55Z (SHIP_VRP22_PFS_FP, PACK22; SHIPSYNC7): the user made TWO uploads -- dist/vrp20_pfsoff.tar.gz
#: (md5 e5d84f03, unchanged) RE-UPLOADED as sub 56686302 (FIFO retires the first vrp20 upload 56652418), then
#: dist/vrp22_pfs_fp.tar.gz (md5 6cef390cc6b29ff0e259d9de6e13e0b5) as sub 56686308 (FIFO retires vrp21_clsearch
#: 56676381).  vrp22_pfs_fp = the PFS anchor 8d670dad + `PLAN_FASTPATH_ON` = True only (REVFIX1 B2: two NumPy-only
#: early exits in `_plan_and_stats`, plan arrays byte-identical, build_day 202 -> 135 ms), config commit `94f168ae`
#: on pack22_0929 (pins 51d17fd8).  SHIPSYNC7: master = commit-tree of pack22_0929^{tree} with parents
#: cf68f736 + 51d17fd8 (no 3-way merge: the vrp21 config is not carried).  Live/final pair = vrp20_pfsoff
#: 56686302 + vrp22_pfs_fp 56686308 (final = Bradley-Terry over Oct 1-15).  FASTPATH is plan-side but digest-neutral:
#: plan digests at `94f168ae` equal `b940d667` (measured 60/60 build_day md5 in PACK22, 3,150 dawns in REVFIX1).
#: A further upload retires 56686302 first.  The rows stay keyed by name (tests read them).
#: 2026-09-29 ~20:47Z (SHIP_VRP23_PFS_T, REVFIX3; SHIPSYNC8): dist/vrp23_pfs_t.tar.gz (md5 ff0cd4e137f8695b5b0d6d29d90a7626)
#: UPLOADED by the user as sub 56687235 (FIFO retires the vrp20_pfsoff re-upload 56686302).  vrp23_pfs_t = the PFS anchor
#: 8d670dad + REVFIX2's overflow.py / sell.py (4ba97bff, bc04f4ab) with `TERMINAL_DEPOSIT_VALUE_ON` = True only (d29 h22
#: overflowing DROP keeps the most valuable deposit; P and F OFF; no plan fastpath), config commit `08067309` on revfix2_0929.
#: REVFIX3 exact read on 1,057 already-played games: 14 fires, all positive, d_margin +3.12/game t 3.39, 0 flips.
#: SHIPSYNC8: master = commit-tree of 08067309^{tree} with parents 53ff15b1 + 08067309 (no 3-way merge: vrp22's
#: PLAN_FASTPATH_ON plan.py is not carried).  Live/final pair = vrp22_pfs_fp 56686308 + vrp23_pfs_t 56687235 (final =
#: Bradley-Terry over Oct 1-15).  A further upload retires 56686308 first.  The rows stay keyed by name (tests read them).
#: 2026-09-29 ~21:21Z (SHIP_VRP24_PFS_TFP, PACK24; SHIPSYNC9): dist/vrp24_pfs_tfp.tar.gz (md5 ea48ab0e8877a9270aac0a0d0fe888e3)
#: UPLOADED by the user as sub 56687774 (FIFO retires vrp22_pfs_fp 56686308).  vrp24_pfs_tfp = the live vrp23_pfs_t tree
#: (08067309) + the vrp22_pfs_fp plan.py (`PLAN_FASTPATH_ON` = True, pack22 94f168ae); config commit `1d3d3443` on
#: pack24_0929.  PACK24: smoke exact 4/4 money rows == VBAND1 ctl, plan md5 60/60 dawns, build_day median 226 -> 141 ms.
#: SHIPSYNC9: master = commit-tree of 1d3d3443^{tree} with parents d53ab97d + 1d3d3443 (no 3-way merge; only plan.py
#: differs from the vrp23 tree).  Live/final pair = vrp23_pfs_t 56687235 + vrp24_pfs_tfp 56687774 (final = Bradley-Terry
#: over Oct 1-15).  A further upload retires 56687235 first.  The rows stay keyed by name (tests read them).
#: 2026-09-30 ~11:55Z (SHIP_VRP25_HYB_EVE, PACK25; SHIPSYNC10): dist/vrp25_hyb_eve.tar.gz (md5 c6d83507478ca8b18c724744405cb923)
#: UPLOADED by the user as sub 56706557 (FIFO retires vrp23_pfs_t 56687235).  vrp25_hyb_eve = the live vrp24_pfs_tfp tree
#: (b1ffcd36) + RSFIX1 code b4840e5e with `OPP_SUPPLY_FAMILY_ON` = True (the 14-code V56 list, hyb050 curves in
#: kagg3/core/opp_supply/, packed by package_submission.opp_family_include) + `EVE_STOCK_ON` = True; config commit `1f187a4b`
#: on pack25_0930.  STACK1 hA: n219 paired margin +1,577 t 4.23, net flips +9, V56 m40 38/40 v21 15/21, own >= 0 all sets.
#: SHIPSYNC10: master fast-forwarded b1ffcd36 -> 6cbf2012 (1f187a4b + the PACK25 pin row; no merge commit, no rewrite).
#: Live/final pair = vrp24_pfs_tfp 56687774 + vrp25_hyb_eve 56706557 (final = Bradley-Terry over Oct 1-15).  A further
#: upload retires 56687774 first.  The rows stay keyed by name (tests read them).
#: 2026-09-30 ~13:05Z (SHIP_VRP26_HYB_EVE_VRP, PACK26; SHIPSYNC11): dist/vrp26_hyb_eve_vrp.tar.gz (md5 2dcd6d44f1e9fc4a9c006d0dd33dafb3)
#: UPLOADED by the user as sub 56707958 (FIFO retires vrp24_pfs_tfp 56687774).  vrp26_hyb_eve_vrp = the live vrp25_hyb_eve tree
#: (6e2df3af) + `ROUTE_VRP_FIX_ON` = True (ROUTEOPT2 route_vrp unsolved-day retry); config commit `bb4f077b` on pack26_0930.
#: STACK1 hAC: n219 paired margin +1,708 t 4.57, net flips +9 vs live; vs hA/vrp25 +131 t 3.41, own +134 t 3.92, flips 0-0.
#: SHIPSYNC11: master fast-forwarded 6e2df3af -> 85674156 (bb4f077b + the PACK26 pin row; no merge commit, no rewrite).
#: Live/final pair = vrp25_hyb_eve 56706557 + vrp26_hyb_eve_vrp 56707958 (final = Bradley-Terry over Oct 1-15).  A further
#: upload retires 56706557 first.  The rows stay keyed by name (tests read them).
#: 2026-09-30 ~20:58Z (SHIP_VRP27_VM_M3, VRPMISS1; SHIPSYNC12): dist/vrp27_vm_m3.tar.gz (md5 1133b789592a586aaecb9683c56ea3c3)
#: UPLOADED by the user as sub 56718602 (FIFO retires vrp25_hyb_eve 56706557).  vrp27_vm_m3 = the live vrp26_hyb_eve_vrp tree
#: (fe602a07) + VRPMISS1 code a5591819 with `ROUTE_VRP_MISS_ON` = True (cell M3, EXTRA_S 0.15: one more route_vrp solve of a
#: day still unsolved after the search + ROUTEOPT2 retry); config commit `ce0df430` on vrpmiss1_0930.  H-180 faithful n171
#: +262 t 5.54 vs vrp26, flips +3-0; V56 m40 38->38, v21 15->15; fresh 167 W 160->160 +141 t 4.24.
#: SHIPSYNC12: master fast-forwarded fe602a07 -> ce0df430 (a5591819, 98d7be0c, ce0df430; no merge commit, no rewrite) + this
#: pin commit.  Live/final pair = vrp26_hyb_eve_vrp 56707958 + vrp27_vm_m3 56718602 (final = Bradley-Terry over Oct 1-15).
#: A further upload retires 56707958 first.  The rows stay keyed by name (tests read them).
SHIPPED = "ce0df430"   # SHIP_VRP27_VM_M3 (sub 56718602) + vrp26_hyb_eve_vrp (sub 56707958): the final pair

#: Keep both live package pins explicit: the A/B differs by exactly one switch.
SHIPPED_PACKAGES = {
    56370365: {
        "ref": "59021db",
        "switches": {"RESIDUAL_ON": 1, "MELONVETO_POST_ON": 0},
    },
    56421514: {
        "ref": "e7a8af84",
        "switches": {"RESIDUAL_ON": 1, "MELONVETO_POST_ON": 1},
    },
    # 09-27 final pair.  vrp9_cs 56600958 (md5 cd94b334) RETIRED by the 56612145 upload: its row stays, like the
    # retired 56370365 / 56421514 rows above, but "retired": True.
    56600958: {
        "ref": "a4c5cc9e", "md5": "cd94b334", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "CARE_RIDE_ON": 1, "SLIVER_ON": 1},
    },
    56600971: {   # res940_vrp10_esw (ESWORK g30 theta); RETIRED (FIFO) by the vrp15_k2fire upload 56634350
        "ref": "a4c5cc9e", "md5": "73f4af9a", "retired": True,
        "switches": {"RESIDUAL_ON": 1},
    },
    # RETIRED (FIFO) by the vrp17_k2hb upload 56643352 (09-28 ~14:15Z): dist/submission_res940_vrp12_pfs.tar.gz =
    # vrp10_esw + PLACEFEED_ON + PF_PUMPSAFE_ON (PLACEFEED3), ship commit dcacbd33 on ship_vrp12_pfs; uploaded
    # 2026-09-27 ~15:10Z (re-keyed from "vrp12_pfs").
    56612145: {
        "ref": "dcacbd33", "md5": "2532e456", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1},
    },
    # NEVER UPLOADED (PACKV2 candidate; vrp15_k2fire took the slot, 56634350): dist/vrp14_k2real.tar.gz = vrp12_pfs + KERNEL2 v2 (MELONHYBRID4 A4 + ZERO_CASH), config commit
    # ba61be6f on ship_vrp14_k2real.  Keyed by name until the user uploads it; re-key to the sub id at SRCSYNC.
    "vrp14_k2real": {
        "ref": "ba61be6f", "md5": "233430d3", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_ZERO_CASH": "488|1088|1303|1409"},
    },
    # RETIRED (FIFO) by the vrp18_k2hb2046 upload 56646827 (09-28 ~16:35Z).
    # was LIVE (PACKV3, sub 56634350, uploaded 09-28 ~08:20Z; ship commit 796c979d): dist/vrp15_k2fire.tar.gz = vrp12_pfs + KERNEL2 v3 (MELONHYBRID4 A4 + FIRE_CASH whitelist, lazy V56),
    # config commit b78bf1e4 on ship_vrp15_k2fire.  Keyed by name (tests read it); the `sub` field carries the id.
    "vrp15_k2fire": {
        "ref": "b78bf1e4", "md5": "1929f224", "sub": 56634350, "ship": "796c979d", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "26|29|2338|2438", "KERNEL2_PRELOAD": 0},
    },
    # RETIRED (FIFO) by the vrp19w_k2wide upload 56649892 (09-28 ~19:10Z).
    # was LIVE (PACKHB1, sub 56643352, uploaded 09-28 ~14:15Z; ship commit a7fcad46): dist/vrp17_k2hb.tar.gz = vrp15_k2fire + the HANDBACK1 switch
    # KERNEL2_HANDBACK_DAY=18 (HANDBACK2 D18), config commit ec2a6042 on ship_vrp17_k2hb.
    # Keyed by name (tests read it); the `sub` field carries the id.  SHIPPED was ec2a6042 (SHIPSYNC2), now 599f8881 (SHIPSYNC3).
    "vrp17_k2hb": {
        "ref": "ec2a6042", "md5": "11fd0f57", "sub": 56643352, "ship": "a7fcad46", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "26|29|2338|2438", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18},
    },
    # RETIRED (FIFO) by the vrp20_pfsoff upload 56652418 (09-28 ~21:25Z).
    # was LIVE (PACK18, sub 56646827, uploaded 09-28 ~16:35Z; ship commit 0735ea4c): dist/vrp18_k2hb2046.tar.gz = vrp17_k2hb (sub 56643352) with
    # KERNEL2_FIRE_CASH += 2046 (LIVEVAL1 CANDIDATE, Dipam Chakraborty), config commit 599f8881 on ship_vrp18_k2hb2046.
    # Keyed by name (tests read it); the `sub` field carries the id.  SHIPPED was 599f8881 (SHIPSYNC3), then 81090f6a (SHIPSYNC4), now b940d667 (SHIPSYNC5).
    "vrp18_k2hb2046": {
        "ref": "599f8881", "md5": "d6ed14d6", "sub": 56646827, "ship": "0735ea4c", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "26|29|2046|2338|2438", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18},
    },
    # RETIRED (FIFO) by the vrp21_clsearch upload 56676381 (09-29 ~13:10Z).
    # was LIVE (PACKWIDE1, sub 56649892, uploaded 09-28 ~19:10Z; ship commit 72570ca8): dist/vrp19w_k2wide.tar.gz = vrp18_k2hb2046 (sub 56646827)
    # with the WIDE KERNEL2 list: FIRE_CASH += 31 MELON rival h1 values (BOLDSLOT1 wide list minus 20/2464 KEEP-OUT and 2015/2885
    # V-collision), config commit 81090f6a on ship_vrp19w_k2wide.  Keyed by name (tests read it); the `sub` field carries the id.
    # SHIPPED was 81090f6a (SHIPSYNC4), then b940d667 (SHIPSYNC5), then 94f168ae (SHIPSYNC7), then 08067309 (SHIPSYNC8), then 1d3d3443 (SHIPSYNC9), then 1f187a4b (SHIPSYNC10), now bb4f077b (SHIPSYNC11).
    "vrp19w_k2wide": {
        "ref": "81090f6a", "md5": "e490347d", "sub": 56649892, "ship": "72570ca8", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "1|4|8|17|19|23|26|29|34|73|76|117|160|163|182|190|444|456|553|564|620|638|661|938|1616|2046|2322|2338|2438|2477|2485|2492|2511|2593|2600|2904", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18},
    },
    # RETIRED (FIFO) by the vrp23_pfs_t upload 56687235 (09-29 ~20:47Z).
    # was LIVE AGAIN (RE-UPLOAD, sub 56686302, 09-29 ~19:55Z; the same package, md5 e5d84f03; tree 8d670dad): dist/vrp20_pfsoff.tar.gz =
    # vrp18_k2hb2046 (sub 56646827) with KERNEL2_FIRE_CASH = "99999" (no live value listed: the step-1 latch never fires, PFS on every
    # seat = FIRELIVE1's OFF arm, FINALPLAN1), config commit b940d667 on ship_vrp20_pfsoff.  The FIRST upload, sub 56652418 (09-28
    # ~21:25Z), is RETIRED (FIFO) by this re-upload (09-29 ~19:55Z); `prev_sub` keeps its id.  Keyed by name (tests read it); the
    # `sub` field carries the last id.  SHIPPED was b940d667 (SHIPSYNC5), then b1835440 (SHIPSYNC6, selfplay1 only), then 94f168ae (SHIPSYNC7),
    # then 08067309 (SHIPSYNC8), then 1d3d3443 (SHIPSYNC9), then 1f187a4b (SHIPSYNC10), now bb4f077b (SHIPSYNC11).
    "vrp20_pfsoff": {
        "ref": "b940d667", "md5": "e5d84f03", "sub": 56686302, "prev_sub": 56652418, "ship": "eeea2793", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18},
    },
    # RETIRED (FIFO) by the vrp22_pfs_fp upload 56686308 (09-29 ~19:55Z).
    # was LIVE (CLSEARCH1, sub 56676381, uploaded 2026-09-29 ~13:10Z; ship commit b1835440 = master until SHIPSYNC6's mirror refresh
    # cf68f736; FIFO-retired vrp19w_k2wide 56649892): dist/vrp21_clsearch.tar.gz (md5 d93d6f5c929c5716f3bed77b31b22457) = vrp20_pfsoff +
    # BRAINSTORM2's REINVEST_DAILY "4:200:CSG" (from d4 buy PFS's own d14 herd as early as the dawn purse allows, reserve 200, cows first)
    # + FEED_ALL (feed wheat granted first); d0 identical to PFS.  Row ported from selfplay1 58f81ba3 (SHIPSYNC6's pins never reached master).
    "vrp21_clsearch": {
        "ref": "b1835440", "md5": "d93d6f5c", "sub": 56676381, "ship": "b1835440", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "REINVEST_DAILY": "4:200:CSG", "FEED_ALL": 1},
    },
    # RETIRED (FIFO) by the vrp24_pfs_tfp upload 56687774 (09-29 ~21:21Z).
    # was LIVE (PACK22, sub 56686308, uploaded 09-29 ~19:55Z; ship commit 51d17fd8 = pack22_0929 pins; master edd4092b = its tree; FIFO-retires
    # vrp21_clsearch 56676381): dist/vrp22_pfs_fp.tar.gz (md5 6cef390cc6b29ff0e259d9de6e13e0b5) = vrp20_pfsoff (tree 8d670dad) with
    # the REVFIX1 B2 switch PLAN_FASTPATH_ON = True (plan arrays byte-identical on 3,150 closed-loop dawns, build_day 202 -> 135 ms);
    # config commit 94f168ae on pack22_0929 (only kagg3/core/plan.py differs from the vrp20 package).  Was an OPTION row (PACK22 51d17fd8).
    # SHIPPED was 94f168ae (SHIPSYNC7), then 08067309 (SHIPSYNC8), then 1d3d3443 (SHIPSYNC9), then 1f187a4b (SHIPSYNC10), now bb4f077b (SHIPSYNC11); its plan.py lives on in vrp25 56706557 and vrp26 56707958.
    # Keyed by name (tests read it); the `sub` field carries the id.
    "vrp22_pfs_fp": {
        "ref": "94f168ae", "md5": "6cef390c", "sub": 56686308, "ship": "51d17fd8", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "PLAN_FASTPATH_ON": 1},
    },
    # CANDIDATE (MELONTRIAL1, 2026-09-29; NOT uploaded, upload = the user's decision): dist/vrp21_melon.tar.gz = vrp20_pfsoff + KERNEL2_FIRE_SWITCHES:
    # rival h1 cash in vrp19w's 36-value wide MELON list -> the seat STAYS PFS and plays the d0-1 melon plate (MELON_PLATE_TILES=8;MELON_PLATE_DAY=0;NONV_PLATE_LAST=1), its d0 plan
    # rebuilt at step 1 from the stored h0 obs; no V56, no hand-back (HANDBACK_DAY 0); every other seat PFS = vrp20 byte for byte.
    # Config commit 9b437711 on ship_vrp21_melon.  Keyed by name, no sub id; re-key at SHIPSYNC if uploaded.  SHIPPED unchanged (b940d667).
    "vrp21_melon": {
        "ref": "9b437711", "md5": "1786a0fb", "candidate": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "1|4|8|17|19|23|26|29|34|73|76|117|160|163|182|190|444|456|553|564|620|638|661|938|1616|2046|2322|2338|2438|2477|2485|2492|2511|2593|2600|2904", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 0,
                     "KERNEL2_FIRE_SWITCHES": "MELON_PLATE_TILES=8;MELON_PLATE_DAY=0;NONV_PLATE_LAST=1"},
    },
    # CANDIDATE (BRAINSTORM2 round 3, 2026-09-29; NOT uploaded, upload = the user's decision): dist/ship_vrp21_bs2lp.tar.gz = vrp20_pfsoff package
    # with plan.py from worktree kagg3_wt_brainstorm2 whose defaults are the r3 cell G2: BANK_LATE_DAYS="8", REINVEST_DAILY="4:200",
    # REINVEST_ALL_LANES=True, FEED_ALL=True, REINVEST_Q3GUARD=8 (KERNEL2_FIRE_CASH stays "99999").  m76 vs g0capsfix own +3,106 (t 4.23)
    # margin +4,395 (t 4.36) W 80 vs 77; flood 80 g own +2,908 margin +3,192; live27 closed loop W 27 = 27, margin +1,551.
    # Config commit 64a0101f on ship_vrp21_bs2lp.  Keyed by name, no sub id; re-key at SHIPSYNC if uploaded.  SHIPPED unchanged (b940d667).
    "vrp21_bs2lp": {
        "ref": "64a0101f", "md5": "b76283db", "candidate": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "BANK_LATE_DAYS": "8", "REINVEST_DAILY": "4:200", "REINVEST_ALL_LANES": 1, "FEED_ALL": 1,
                     "REINVEST_Q3GUARD": 8},
    },
    # CANDIDATE (ESHEADCL1, 2026-09-29; NOT uploaded, upload = the user's decision): dist/ship_vrp21_esheadcl.tar.gz = vrp20_pfsoff package
    # with kagg3/core/residual_head.py = S/esheadcl1/residual_head.py (optional day-window output offsets `dwin`/`dwin_d0` in numpy_fn;
    # absent = the shipped decode) and residual_head.npz = head_940 + the ES genome g08_03 (npz md5 add7daeb; 20 non-zero gene
    # offsets on d1-19, MELON d5-9 +2 and SHEEP d10-14 -2, the rest one step; d0 and d20-29 untouched).  Every switch = vrp20_pfsoff.  m76 vs g0capsfix own +4,880 (t 8.14) margin +1,498
    # (t 1.76) W 149 vs 148; big 80 g own +718 margin +1,429; live27 faithful W 6 -> 8.  No config commit (the body = master 8d670dad src +
    # the two package files).  Keyed by name, no sub id; re-key at SHIPSYNC if uploaded.  SHIPPED unchanged (b1835440).
    "vrp21_esheadcl": {
        "ref": "8d670dad", "md5": "909e366a", "candidate": True, "residual_head_npz_md5": "add7daeb",
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18},
    },
    # RETIRED (FIFO) by the vrp25_hyb_eve upload 56706557 (09-30 ~11:55Z).
    # was LIVE (REVFIX3, sub 56687235, uploaded 09-29 ~20:47Z; ship commit 08067309 = the config commit; master f10cfb18 = its tree; FIFO-retires
    # the vrp20_pfsoff re-upload 56686302): dist/vrp23_pfs_t.tar.gz (md5 ff0cd4e137f8695b5b0d6d29d90a7626) = vrp20_pfsoff package with
    # kagg3/agent/overflow.py + kagg3/core/sell.py from worktree kagg3_wt_revfix2 (8d670dad + REVFIX2 4ba97bff/bc04f4ab) whose only
    # changed default is TERMINAL_DEPOSIT_VALUE_ON = True (d29 h22 overflowing DROP keeps the most valuable deposit; P, F, F4 OFF).
    # Exact read on already-played games (one engine step from the recorded step-718 state): n 1057, 14 fires all positive,
    # d_margin +3.12/game t 3.39, 0 negative, 0 flips.  Config commit 08067309 on revfix2_0929.  Was a CANDIDATE row (REVFIX3 4fe567c6).
    # SHIPPED was 08067309 (SHIPSYNC8), then 1d3d3443 (SHIPSYNC9), then 1f187a4b (SHIPSYNC10), now bb4f077b (SHIPSYNC11); its overflow.py lives on in vrp25 and vrp26.
    # Keyed by name (tests read it); the `sub` field carries the id.
    "vrp23_pfs_t": {
        "ref": "08067309", "md5": "ff0cd4e1", "sub": 56687235, "ship": "08067309", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1},
    },
    # RETIRED (FIFO) by the vrp26_hyb_eve_vrp upload 56707958 (09-30 ~13:05Z).
    # was LIVE (PACK24, sub 56687774, uploaded 09-29 ~21:21Z; ship commit 1d3d3443 = the config commit; master ebe20a65 = its tree; FIFO-retires
    # vrp22_pfs_fp 56686308): dist/vrp24_pfs_tfp.tar.gz (md5 ea48ab0e8877a9270aac0a0d0fe888e3)
    # = the live vrp23_pfs_t tree (08067309) + the live vrp22_pfs_fp plan.py (PLAN_FASTPATH_ON = True, pack22 94f168ae): members vs vrp23
    # DIFF 1 (kagg3/core/plan.py), vs vrp22 DIFF 2 (overflow.py, sell.py).  Behaviour = vrp23 (smoke 4/4 money rows == VBAND1 ctl, plan md5
    # 60/60 dawns), build_day median 226 -> 141 ms.  Config commit 1d3d3443 on pack24_0929.  Was an OPTION row (PACK24 b2bb704a).
    # SHIPPED was 1d3d3443 (SHIPSYNC9), then 1f187a4b (SHIPSYNC10), now bb4f077b (SHIPSYNC11); its plan.py/overflow.py live on in vrp25 and vrp26.
    # Keyed by name (tests read it); the `sub` field carries the id.
    "vrp24_pfs_tfp": {
        "ref": "1d3d3443", "md5": "ea48ab0e", "sub": 56687774, "ship": "1d3d3443", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1},
    },
    # RETIRED (FIFO) by the vrp27_vm_m3 upload 56718602 (09-30 ~20:58Z).
    # was LIVE (PACK25, sub 56706557, uploaded 09-30 ~11:55Z; ship commit 1f187a4b = the config commit; master 6cbf2012 (fast-forward) = its
    # tree + the PACK25 pin row; FIFO-retires vrp23_pfs_t 56687235): dist/vrp25_hyb_eve.tar.gz (md5 c6d83507478ca8b18c724744405cb923, 37 files = vrp24's 31 +
    # kagg3/core/opp_supply/S_{MEL,OTH,P48,PQ4,V56,pop}.npy) = master b1ffcd36 (vrp24 tree) + RSFIX1 code b4840e5e with RSFIX1 hyb050
    # (OPP_SUPPLY_FAMILY_ON, the 14-code V56 list, hyb050 curves) + EVE_STOCK_ON = STACK1 hA (n219 +1,577 t 4.23, net flips +9).
    # Config commit 1f187a4b on pack25_0930.  Was an OPTION row (PACK25 6cbf2012).  Final pair 56706557 + 56707958 (since 09-30 ~13:05Z).
    # SHIPPED was 1f187a4b (SHIPSYNC10), then bb4f077b (SHIPSYNC11), now ce0df430 (SHIPSYNC12); its code lives on in vrp26 and vrp27.
    # Keyed by name (tests read it); the `sub` field carries the id.
    "vrp25_hyb_eve": {
        "ref": "1f187a4b", "md5": "c6d83507", "sub": 56706557, "ship": "1f187a4b", "retired": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1, "OPP_SUPPLY_FAMILY_ON": 1,
                     "OPP_SUPPLY_FAMILY_V56_CASH": "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106",
                     "EVE_STOCK_ON": 1},
    },
    # LIVE (PACK26, sub 56707958, uploaded 09-30 ~13:05Z; ship commit bb4f077b = the config commit; master 85674156 (fast-forward) = its
    # tree + the PACK26 pin row; FIFO-retires vrp24_pfs_tfp 56687774; final pair vrp25_hyb_eve 56706557 + vrp26): dist/vrp26_hyb_eve_vrp.tar.gz (md5 2dcd6d44f1e9fc4a9c006d0dd33dafb3, 37 files: 36 identical to
    # vrp25 c6d83507, kagg3/core/plan.py differs by one default) = master 6e2df3af (the vrp25 tree) + ROUTE_VRP_FIX_ON = True (ROUTEOPT2
    # route_vrp unsolved-day fixes) = STACK1 hAC (n219 +1,708 t 4.57, net flips +9; paired vs hA/vrp25 +131 t 3.41, own +134 t 3.92, flips 0-0).
    # Config commit bb4f077b on pack26_0930.  Was an OPTION row (PACK26 85674156).  SHIPPED was bb4f077b (SHIPSYNC11), now ce0df430
    # (SHIPSYNC12); stays LIVE (56707958) in the final pair with vrp27_vm_m3 56718602.
    # Keyed by name (tests read it); the `sub` field carries the id.  A further upload retires 56707958 first.
    "vrp26_hyb_eve_vrp": {
        "ref": "bb4f077b", "md5": "2dcd6d44", "sub": 56707958, "ship": "bb4f077b", "retired": False,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1, "OPP_SUPPLY_FAMILY_ON": 1,
                     "OPP_SUPPLY_FAMILY_V56_CASH": "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106",
                     "EVE_STOCK_ON": 1, "ROUTE_VRP_FIX_ON": 1},
    },
    # LIVE (VRPMISS1, sub 56718602, uploaded 09-30 ~20:58Z; ship commit ce0df430 = the config commit; master = ce0df430 (fast-forward from
    # fe602a07) + the SHIPSYNC12 pin commit; FIFO-retires vrp25_hyb_eve 56706557; final pair vrp26_hyb_eve_vrp 56707958 + vrp27): Was an
    # OPTION row (VRPMISS1 9921cefa).  SHIPPED = ce0df430 (SHIPSYNC12).  dist/vrp27_vm_m3.tar.gz (md5 1133b789592a586aaecb9683c56ea3c3, 37 files: 35 identical to
    # vrp26 2dcd6d44; kagg3/agent/route_vrp.py + kagg3/core/plan.py differ) = the vrp26 tree + ROUTE_VRP_MISS_ON (cell M3, +0.15 s on
    # the unsolved day): HARNESS2 H-180 faithful n171 +262 t 5.54 vs vrp26, flips +3-0; V56 m40 38->38, v21 15->15.  Config commit ce0df430.
    "vrp27_vm_m3": {
        "ref": "ce0df430", "md5": "1133b789", "sub": 56718602, "ship": "ce0df430", "retired": False,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1, "OPP_SUPPLY_FAMILY_ON": 1,
                     "OPP_SUPPLY_FAMILY_V56_CASH": "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106",
                     "EVE_STOCK_ON": 1, "ROUTE_VRP_FIX_ON": 1, "ROUTE_VRP_MISS_ON": 1},
    },
    # OPTION (VRPMISS1 M3-P, 09-30 ~20:40Z, not uploaded): dist/vrp27_vm_m3p.tar.gz (md5 c5599634cfff3c4f39ce173c6cbd531b, 37 files: 34
    # identical to vrp26; route_vrp.py, runtime.py, plan.py differ) = vrp27_vm_m3 + ROUTE_VRP_MISS_PROG_ONLY (the retry only on seats whose
    # rival holds 1..10 MELON at d2 h0).  Config commit 2ae7cb31 on vrpmiss1_0930 (NOT on master).  Still an OPTION after SHIPSYNC12.
    "vrp27_vm_m3p": {
        "ref": "2ae7cb31", "md5": "c5599634", "candidate": True,
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1, "OPP_SUPPLY_FAMILY_ON": 1,
                     "OPP_SUPPLY_FAMILY_V56_CASH": "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106",
                     "EVE_STOCK_ON": 1, "ROUTE_VRP_FIX_ON": 1, "ROUTE_VRP_MISS_ON": 1, "ROUTE_VRP_MISS_PROG_ONLY": 1},
    },
    # OPTION / BACKUP (DETAGENT1, 2026-09-30, NOT uploaded; the user decides): dist/det1_base.tar.gz (md5 e7ebb6a744219107f15468dab24d3b8b,
    # 42 files: 35 identical to vrp26 2dcd6d44, kagg3/core/plan.py + kagg3/agent/runtime.py differ, kagg3/prog/ 5 files added incl. the
    # CREWBC1 m1 weights crewbc_w.npz md5 0ac2ff99) = master fe602a07 (vrp26 tree) + the DET1 body code (bae3e7e4) + DET1_BODY = True:
    # the deterministic MMPQ executor body CREWCOMBO1 crewF4Sbcfa (DET1_KNOBS) plays EVERY seat from step 0 (no planner, no macro).
    # Config commit 839e86dd on detagent1_0930.  Closed loop HOLD20 coins 0.920 / TUNE20 0.817 of MMPQ; reacting V56 m40/v21 = PANELPREP1
    # combofa rows (W 2/40, 0/21).  Keyed by name, no sub.
    "det1_base": {
        "ref": "839e86dd", "md5": "e7ebb6a7", "candidate": True, "backup": True, "weights_md5": "0ac2ff99",
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1, "OPP_SUPPLY_FAMILY_ON": 1,
                     "OPP_SUPPLY_FAMILY_V56_CASH": "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106",
                     "EVE_STOCK_ON": 1, "ROUTE_VRP_FIX_ON": 1, "DET1_BODY": 1,
                     "DET1_KNOBS": "crew=1;fy_fert=1;fy_fert_d=4;fy_cf_h=8;fy_cf_pri=-1;fy_stskip=1;bc=3;bclam=1.5;bcani=2;feed_all_until=26"},
    },
    # OPTION / BACKUP (DETAGENT1 hybrid form, NOT uploaded): dist/det1h_h1.tar.gz (md5 f37f4b17119f021fa990561b771fe5d8) = vrp26 (PFS) on every
    # seat; a seat whose rival's d0 h1 cash is in the 41-value programme list (V 0/348) is handed to the det1_base body (bridge) from step 1.
    # Config commit 0b64f848 on detagent1_0930 (DET1_BODY False, DET1_HYB_ON True).  V56: the latch never fires (m40 rows == vrp26);
    # HARNESS2 v4 vs vrp26: fired 109/180, pooled faithful n145 -9,517 (t -8.57), fired+faithful n74 -18,648 (t -11.95).  Keyed by name, no sub.
    "det1h_h1": {
        "ref": "0b64f848", "md5": "f37f4b17", "candidate": True, "backup": True, "weights_md5": "0ac2ff99",
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1, "OPP_SUPPLY_FAMILY_ON": 1,
                     "OPP_SUPPLY_FAMILY_V56_CASH": "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106",
                     "EVE_STOCK_ON": 1, "ROUTE_VRP_FIX_ON": 1, "DET1_BODY": 0, "DET1_HYB_ON": 1,
                     "DET1_HYB_FIRE_CASH": "1|4|8|17|19|23|26|34|73|76|117|160|163|182|190|444|456|553|564|620|638|661|938|964|985|992|1020|1100|1616|2046|2097|2322|2338|2438|2477|2485|2492|2511|2593|2600|2904",
                     "DET1_KNOBS": "crew=1;fy_fert=1;fy_fert_d=4;fy_cf_h=8;fy_cf_pri=-1;fy_stskip=1;bc=3;bclam=1.5;bcani=2;feed_all_until=26"},
    },
    # OPTION / BACKUP (DETAGENT2, 2026-09-30, NOT uploaded; the user decides): dist/det2_place.tar.gz (md5 d4fc94d5b68bccbeb1a939b905ec2ba6;
    # vs det1_base e7ebb6a7: kagg3/agent/runtime.py, kagg3/core/plan.py, kagg3/prog/direct.py differ, weights crewbc_w.npz 0ac2ff99 identical)
    # = det1_base's body + the an2_place animal placement role (a hand carrying an animal walks straight to the nearest free matching
    # structure and places it; the base body carried animals 383 non-move steps/game and picked up 48 for 24 placements).
    # Config commit 38626043 on detagent2_0930 (DET1_BODY True, DET1_HYB_ON False).  Closed loop HOLD20 0.938 / TUNE20 0.835 of MMPQ
    # (paired vs crewF4Sbcfa pooled +0.0178 t 2.77, 28/40); V56 m40+v21 vs det1_base n81 margin +4,007 t 5.16 W 4->9; HARNESS2 v4 P48TAPE172
    # vs det1_base margin +6,432 t 7.00 net +12 (faithful n104 +5,639 t 7.49).  Keyed by name, no sub.
    "det2_place": {
        "ref": "38626043", "md5": "d4fc94d5", "candidate": True, "backup": True, "weights_md5": "0ac2ff99",
        "switches": {"RESIDUAL_ON": 1, "PLACEFEED_ON": 1, "PF_PUMPSAFE_ON": 1, "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0,
                     "KERNEL2_INHERIT": 1, "KERNEL2_FIRE_CASH": "99999", "KERNEL2_PRELOAD": 0, "KERNEL2_HANDBACK_DAY": 18,
                     "TERMINAL_DEPOSIT_VALUE_ON": 1, "PLAN_FASTPATH_ON": 1, "OPP_SUPPLY_FAMILY_ON": 1,
                     "OPP_SUPPLY_FAMILY_V56_CASH": "2630|2802|2854|2864|2867|2873|2875|2884|2901|2906|2911|3029|3037|3106",
                     "EVE_STOCK_ON": 1, "ROUTE_VRP_FIX_ON": 1, "DET1_BODY": 1,
                     "DET1_KNOBS": "crew=1;fy_fert=1;fy_fert_d=4;fy_cf_h=8;fy_cf_pri=-1;fy_stskip=1;bc=3;bclam=1.5;bcani=2;feed_all_until=26;an2_place=1"},
    },
}


def test_vrp12_pfs_pin_row():
    """56612145 names the SHIP_VRP12_PFS commit; after the 09-30 ~20:58Z upload the live (final) pair is vrp26_hyb_eve_vrp 56707958 +
    vrp27_vm_m3 56718602 (vrp25_hyb_eve 56706557, vrp24_pfs_tfp 56687774, vrp23_pfs_t 56687235, vrp22_pfs_fp 56686308, the vrp20_pfsoff re-upload 56686302, vrp21_clsearch 56676381, the first vrp20 upload 56652418, vrp19w_k2wide 56649892,
    vrp18_k2hb2046 56646827, vrp17_k2hb 56643352, vrp15_k2fire 56634350 and 56612145 retired by FIFO, 56600971 and 56600958 before,
    vrp14_k2real never uploaded)."""
    assert SHIPPED_PACKAGES[56612145]["ref"] == "dcacbd33"
    assert SHIPPED_PACKAGES[56612145]["md5"] == "2532e456"
    assert SHIPPED_PACKAGES[56612145]["switches"]["PF_PUMPSAFE_ON"] == 1
    live = {k for k, v in SHIPPED_PACKAGES.items()
            if k in (56600958, 56600971, 56612145, "vrp14_k2real", "vrp15_k2fire", "vrp17_k2hb", "vrp18_k2hb2046",
                     "vrp19w_k2wide", "vrp20_pfsoff", "vrp21_clsearch", "vrp22_pfs_fp", "vrp23_pfs_t", "vrp24_pfs_tfp",
                     "vrp25_hyb_eve", "vrp26_hyb_eve_vrp", "vrp27_vm_m3")
            and not v.get("retired")}
    assert live == {"vrp26_hyb_eve_vrp", "vrp27_vm_m3"}
    assert {SHIPPED_PACKAGES[k]["sub"] for k in live} == {56707958, 56718602}
    assert not any(v.get("sub") and not v.get("retired") for k, v in SHIPPED_PACKAGES.items() if k not in live and isinstance(k, str))
    assert SHIPPED == SHIPPED_PACKAGES["vrp27_vm_m3"]["ref"] == "ce0df430"


def test_vrp14_k2real_pin_row():
    """The candidate row: vrp12_pfs switches + the KERNEL2 v2 four."""
    row = SHIPPED_PACKAGES["vrp14_k2real"]
    assert row["md5"] == "233430d3"
    base = SHIPPED_PACKAGES[56612145]["switches"]
    assert {k: v for k, v in row["switches"].items() if k in base} == base
    assert set(row["switches"]) - set(base) == {"KERNEL2_ON", "KERNEL2_NOOP_H0", "KERNEL2_INHERIT", "KERNEL2_ZERO_CASH"}


def test_vrp15_k2fire_pin_row():
    """The v3 candidate row: vrp12_pfs switches + KERNEL2 ON/NOOP_H0/INHERIT + the FIRE_CASH whitelist + lazy V56."""
    row = SHIPPED_PACKAGES["vrp15_k2fire"]
    assert row["md5"] == "1929f224" and row["ref"] == "b78bf1e4"
    assert row["sub"] == 56634350 and row["ship"] == "796c979d" and row["retired"]   # FIFO-retired by 56646827
    base = SHIPPED_PACKAGES[56612145]["switches"]
    assert {k: v for k, v in row["switches"].items() if k in base} == base
    assert set(row["switches"]) - set(base) == {"KERNEL2_ON", "KERNEL2_NOOP_H0", "KERNEL2_INHERIT", "KERNEL2_FIRE_CASH",
                                                 "KERNEL2_PRELOAD"}


def test_vrp17_k2hb_pin_row():
    """PACKHB1 row, sub 56643352 (FIFO-retired by 56649892): the vrp15_k2fire switches + KERNEL2_HANDBACK_DAY=18."""
    row, v3 = SHIPPED_PACKAGES["vrp17_k2hb"], SHIPPED_PACKAGES["vrp15_k2fire"]
    assert row["md5"] == "11fd0f57" and row["ref"] == "ec2a6042" and "candidate" not in row
    assert row["sub"] == 56643352 and row["ship"] == "a7fcad46"
    assert {k for k in set(row["switches"]) | set(v3["switches"]) if row["switches"].get(k) != v3["switches"].get(k)} == {"KERNEL2_HANDBACK_DAY"}
    assert row["switches"]["KERNEL2_HANDBACK_DAY"] == 18
    assert set(v3["switches"]["KERNEL2_FIRE_CASH"].split("|")) <= set(row["switches"]["KERNEL2_FIRE_CASH"].split("|"))
    assert row["ref"] == "ec2a6042" and SHIPPED != row["ref"] and row["retired"]   # moved on by vrp18 (SHIPSYNC3); FIFO-retired by 56649892 (SHIPSYNC4)


def test_vrp18_k2hb2046_pin_row():
    """PACK18 row, sub 56646827 (FIFO-retired by 56652418): the vrp17_k2hb switches with 2046 added to KERNEL2_FIRE_CASH."""
    row, v17 = SHIPPED_PACKAGES["vrp18_k2hb2046"], SHIPPED_PACKAGES["vrp17_k2hb"]
    assert row["md5"] == "d6ed14d6" and row["ref"] == "599f8881" and "candidate" not in row
    assert row["sub"] == 56646827 and row["ship"] == "0735ea4c"
    assert {k for k in set(row["switches"]) | set(v17["switches"]) if row["switches"].get(k) != v17["switches"].get(k)} == {"KERNEL2_FIRE_CASH"}
    assert set(row["switches"]["KERNEL2_FIRE_CASH"].split("|")) - set(v17["switches"]["KERNEL2_FIRE_CASH"].split("|")) == {"2046"}
    assert row["switches"]["KERNEL2_HANDBACK_DAY"] == 18
    assert row["ref"] == "599f8881" and SHIPPED != row["ref"] and row["retired"]   # moved on by vrp19w (SHIPSYNC4); FIFO-retired by 56652418 (SHIPSYNC5)


def test_vrp19w_k2wide_pin_row():
    """PACKWIDE1 row, sub 56649892 (FIFO-retired by 56676381): the vrp18_k2hb2046 switches with 31 MELON h1 values added to KERNEL2_FIRE_CASH."""
    row, v18 = SHIPPED_PACKAGES["vrp19w_k2wide"], SHIPPED_PACKAGES["vrp18_k2hb2046"]
    assert row["md5"] == "e490347d" and row["ref"] == "81090f6a" and "candidate" not in row
    assert row["sub"] == 56649892 and row["ship"] == "72570ca8"
    assert {k for k in set(row["switches"]) | set(v18["switches"]) if row["switches"].get(k) != v18["switches"].get(k)} == {"KERNEL2_FIRE_CASH"}
    new, old = set(row["switches"]["KERNEL2_FIRE_CASH"].split("|")), set(v18["switches"]["KERNEL2_FIRE_CASH"].split("|"))
    assert old <= new and new - old == {'938', '1', '2492', '2511', '564', '2593', '2600', '34', '620', '456', '638', '23', '8', '160', '2322', '1616', '4', '553', '19', '661', '76', '2904', '17', '182', '2477', '444', '190', '163', '2485', '73', '117'}
    assert not new & {"20", "2464", "2015", "2885", "2854", "2867", "988", "1020"}   # KEEP-OUT / V-collision values stay PFS
    assert row["switches"]["KERNEL2_HANDBACK_DAY"] == 18
    assert row["ref"] == "81090f6a" and SHIPPED != row["ref"] and row["retired"]   # moved on by vrp20 (SHIPSYNC5); FIFO-retired by 56676381


def test_vrp20_pfsoff_pin_row():
    """PACK20 row, re-upload 56686302 (09-29 ~19:55Z; FIFO-retired 09-29 ~20:47Z by 56687235; the first upload 56652418 FIFO-retired
    09-29 ~19:55Z): the vrp18_k2hb2046 switches with KERNEL2_FIRE_CASH = "99999" (no live value -> PFS on every seat)."""
    row, v18 = SHIPPED_PACKAGES["vrp20_pfsoff"], SHIPPED_PACKAGES["vrp18_k2hb2046"]
    assert row["md5"] == "e5d84f03" and row["ref"] == "b940d667" and "candidate" not in row
    assert row["sub"] == 56686302 and row["prev_sub"] == 56652418 and row["ship"] == "eeea2793" and row["retired"]
    assert {k for k in set(row["switches"]) | set(v18["switches"]) if row["switches"].get(k) != v18["switches"].get(k)} == {"KERNEL2_FIRE_CASH"}
    assert row["switches"]["KERNEL2_FIRE_CASH"] == "99999"
    assert not set(row["switches"]["KERNEL2_FIRE_CASH"].split("|")) & set(v18["switches"]["KERNEL2_FIRE_CASH"].split("|") + ["190"])
    assert not set(row["switches"]["KERNEL2_FIRE_CASH"].split("|")) & set(SHIPPED_PACKAGES["vrp19w_k2wide"]["switches"]["KERNEL2_FIRE_CASH"].split("|"))
    assert row["switches"]["KERNEL2_ON"] == 1 and row["switches"]["KERNEL2_HANDBACK_DAY"] == 18
    assert SHIPPED != row["ref"] == "b940d667"   # moved on by vrp22_pfs_fp (SHIPSYNC7); 56686302 FIFO-retired by vrp23_pfs_t 56687235 (SHIPSYNC8)


def test_vrp21_melon_pin_row():
    """MELONTRIAL1 candidate row: vrp20's switches with the wide list, the fired switch-set, no hand-back; no sub id."""
    row, v20 = SHIPPED_PACKAGES["vrp21_melon"], SHIPPED_PACKAGES["vrp20_pfsoff"]
    assert row["md5"] == "1786a0fb" and row["ref"] == "9b437711" and row["candidate"] and "sub" not in row
    assert {k for k in set(row["switches"]) | set(v20["switches"]) if row["switches"].get(k) != v20["switches"].get(k)} == {
        "KERNEL2_FIRE_CASH", "KERNEL2_HANDBACK_DAY", "KERNEL2_FIRE_SWITCHES"}
    assert row["switches"]["KERNEL2_FIRE_CASH"] == SHIPPED_PACKAGES["vrp19w_k2wide"]["switches"]["KERNEL2_FIRE_CASH"]
    assert row["switches"]["KERNEL2_HANDBACK_DAY"] == 0 and row["switches"]["KERNEL2_FIRE_SWITCHES"].startswith("MELON_PLATE_TILES=")
    assert SHIPPED != row["ref"]   # the candidate never moved the shipped pin (vrp21_clsearch did, SHIPSYNC6; now vrp23_pfs_t, SHIPSYNC8)


def test_vrp21_clsearch_pin_row():
    """CLSEARCH1 row, sub 56676381 (09-29 ~13:10Z; FIFO-retired 09-29 ~19:55Z by 56686308): vrp20_pfsoff's switches +
    REINVEST_DAILY "4:200:CSG" + FEED_ALL, both plan.py defaults at the config commit (checked against the committed tree)."""
    row, v20 = SHIPPED_PACKAGES["vrp21_clsearch"], SHIPPED_PACKAGES["vrp20_pfsoff"]
    assert row["md5"] == "d93d6f5c" and row["ref"] == "b1835440" and "candidate" not in row
    assert row["sub"] == 56676381 and row["ship"] == "b1835440" and row["retired"]
    assert {k for k in set(row["switches"]) | set(v20["switches"]) if row["switches"].get(k) != v20["switches"].get(k)} == {
        "REINVEST_DAILY", "FEED_ALL"}
    assert row["switches"]["REINVEST_DAILY"] == "4:200:CSG" and row["switches"]["FEED_ALL"] == 1
    src = subprocess.run(["git", "show", f"{row['ref']}:src/kagg3/core/plan.py"], cwd=repo_root(__file__),
                         capture_output=True, text=True, check=True).stdout.splitlines()
    assert 'REINVEST_DAILY = "4:200:CSG"' in src and "FEED_ALL = True" in src
    assert SHIPPED != row["ref"]   # retired; the shipped pin moved to vrp22_pfs_fp (SHIPSYNC7), vrp23_pfs_t (SHIPSYNC8), vrp24_pfs_tfp (SHIPSYNC9)



def test_vrp22_pfs_fp_pin_row():
    """PACK22 row, sub 56686308 (09-29 ~19:55Z; FIFO-retired 09-29 ~21:21Z by 56687774): the vrp20_pfsoff switches + PLAN_FASTPATH_ON
    (the packaged plan.py default is True)."""
    from pathlib import Path
    row, v20 = SHIPPED_PACKAGES["vrp22_pfs_fp"], SHIPPED_PACKAGES["vrp20_pfsoff"]
    assert row["md5"] == "6cef390c" and row["ref"] == "94f168ae" and "candidate" not in row and row["retired"]
    assert row["sub"] == 56686308 and row["ship"] == "51d17fd8"
    assert {k for k in set(row["switches"]) | set(v20["switches"]) if row["switches"].get(k) != v20["switches"].get(k)} == {"PLAN_FASTPATH_ON"}
    assert SHIPPED != row["ref"] == "94f168ae"   # moved on by vrp23_pfs_t (SHIPSYNC8); 56686308 FIFO-retired by vrp24_pfs_tfp 56687774 (SHIPSYNC9)
    src = (Path(__file__).resolve().parents[1] / "src/kagg3/core/plan.py").read_text()
    if "PLAN_FASTPATH_ON" in src:   # on the pack22 tree the packaged default is ON
        assert "\nPLAN_FASTPATH_ON = True" in src


def test_vrp23_pfs_t_pin_row():
    """REVFIX3 row, sub 56687235 (09-29 ~20:47Z; FIFO-retired 09-30 ~11:55Z by 56706557): the vrp20_pfsoff switches + TERMINAL_DEPOSIT_VALUE_ON (the packaged
    overflow.py default is True; P / F stay OFF)."""
    from pathlib import Path
    row, v20 = SHIPPED_PACKAGES["vrp23_pfs_t"], SHIPPED_PACKAGES["vrp20_pfsoff"]
    assert row["md5"] == "ff0cd4e1" and row["ref"] == "08067309" and "candidate" not in row and row["retired"]
    assert row["sub"] == 56687235 and row["ship"] == "08067309"
    assert {k for k in set(row["switches"]) | set(v20["switches"]) if row["switches"].get(k) != v20["switches"].get(k)} == {
        "TERMINAL_DEPOSIT_VALUE_ON"}
    assert SHIPPED != row["ref"] == "08067309"   # moved on by vrp24_pfs_tfp (SHIPSYNC9); 56687235 FIFO-retired by vrp25_hyb_eve 56706557 (SHIPSYNC10)
    src = (Path(__file__).resolve().parents[1] / "src/kagg3/agent/overflow.py").read_text()
    if "TERMINAL_DEPOSIT_VALUE_ON" in src:   # on the vrp23 tree (master) the packaged default is ON
        assert "\nTERMINAL_DEPOSIT_VALUE_ON = True" in src


def test_vrp24_pfs_tfp_pin_row():
    """PACK24 row, sub 56687774 (09-29 ~21:21Z; FIFO-retired 09-30 ~13:05Z by 56707958): vrp23_pfs_t's switches + PLAN_FASTPATH_ON = the union of vrp22_pfs_fp's and
    vrp23_pfs_t's changes over vrp20_pfsoff (the packaged plan.py and overflow.py defaults are True)."""
    from pathlib import Path
    row, v22, v23 = SHIPPED_PACKAGES["vrp24_pfs_tfp"], SHIPPED_PACKAGES["vrp22_pfs_fp"], SHIPPED_PACKAGES["vrp23_pfs_t"]
    assert row["md5"] == "ea48ab0e" and row["ref"] == "1d3d3443" and "candidate" not in row and row["retired"]
    assert row["sub"] == 56687774 and row["ship"] == "1d3d3443"
    assert {k for k in set(row["switches"]) | set(v23["switches"]) if row["switches"].get(k) != v23["switches"].get(k)} == {"PLAN_FASTPATH_ON"}
    assert {k for k in set(row["switches"]) | set(v22["switches"]) if row["switches"].get(k) != v22["switches"].get(k)} == {
        "TERMINAL_DEPOSIT_VALUE_ON"}
    assert SHIPPED != row["ref"] == "1d3d3443" != v23["ref"]   # moved on by vrp25_hyb_eve (SHIPSYNC10); 56687774 FIFO-retired by vrp26 56707958 (SHIPSYNC11)
    root = Path(__file__).resolve().parents[1]
    plan = (root / "src/kagg3/core/plan.py").read_text()
    ovf = (root / "src/kagg3/agent/overflow.py").read_text()
    if "PLAN_FASTPATH_ON" in plan and "TERMINAL_DEPOSIT_VALUE_ON" in ovf:   # on the vrp24 tree (master) both packaged defaults are ON
        assert "\nPLAN_FASTPATH_ON = True" in plan and "\nTERMINAL_DEPOSIT_VALUE_ON = True" in ovf


def test_vrp25_hyb_eve_pin_row():
    """PACK25 row, sub 56706557 (09-30 ~11:55Z; FIFO-retired 09-30 ~20:58Z by 56718602): vrp24_pfs_tfp's switches + the RSFIX1 hyb050
    pair + EVE_STOCK_ON; the upload moved SHIPPED to the config commit 1f187a4b (SHIPSYNC10), vrp26 moved it on to bb4f077b (SHIPSYNC11),
    vrp27_vm_m3 to ce0df430 (SHIPSYNC12)."""
    from pathlib import Path
    row, v24 = SHIPPED_PACKAGES["vrp25_hyb_eve"], SHIPPED_PACKAGES["vrp24_pfs_tfp"]
    assert row["md5"] == "c6d83507" and row["ref"] == "1f187a4b" and "candidate" not in row and row["retired"]
    assert row["sub"] == 56706557 and row["ship"] == "1f187a4b"
    assert {k for k in set(row["switches"]) | set(v24["switches"]) if row["switches"].get(k) != v24["switches"].get(k)} == {
        "OPP_SUPPLY_FAMILY_ON", "OPP_SUPPLY_FAMILY_V56_CASH", "EVE_STOCK_ON"}
    assert len(row["switches"]["OPP_SUPPLY_FAMILY_V56_CASH"].split("|")) == 14
    assert SHIPPED != row["ref"] == "1f187a4b" != v24["ref"]   # moved on by vrp26_hyb_eve_vrp (SHIPSYNC11); 56706557 FIFO-retired by vrp27_vm_m3 56718602 (SHIPSYNC12)
    root = Path(__file__).resolve().parents[1]
    plan = (root / "src/kagg3/core/plan.py").read_text()
    if "\nOPP_SUPPLY_FAMILY_ON = True" in plan:   # on the vrp25 tree (master, pack25_0930) the three packaged defaults are ON
        assert "\nEVE_STOCK_ON = True" in plan
        assert '\nOPP_SUPPLY_FAMILY_V56_CASH = "%s"' % row["switches"]["OPP_SUPPLY_FAMILY_V56_CASH"] in plan
        assert all((root / "src/kagg3/core/opp_supply" / f).exists() for f in ("S_OTH.npy", "S_V56.npy", "S_MEL.npy", "S_P48.npy", "S_PQ4.npy", "S_pop.npy"))


def test_vrp26_hyb_eve_vrp_pin_row():
    """PACK26 row, LIVE as sub 56707958 (09-30 ~13:05Z): vrp25_hyb_eve's switches + ROUTE_VRP_FIX_ON; the upload moved SHIPPED to the
    config commit bb4f077b (SHIPSYNC11); vrp27_vm_m3 moved it on to ce0df430 (SHIPSYNC12); 56707958 stays LIVE."""
    from pathlib import Path
    row, v25 = SHIPPED_PACKAGES["vrp26_hyb_eve_vrp"], SHIPPED_PACKAGES["vrp25_hyb_eve"]
    assert row["md5"] == "2dcd6d44" and row["ref"] == "bb4f077b" and "candidate" not in row and not row["retired"]
    assert row["sub"] == 56707958 and row["ship"] == "bb4f077b"
    assert {k for k in set(row["switches"]) | set(v25["switches"]) if row["switches"].get(k) != v25["switches"].get(k)} == {"ROUTE_VRP_FIX_ON"}
    assert SHIPPED != row["ref"] == "bb4f077b" != v25["ref"]   # moved on by vrp27_vm_m3 (SHIPSYNC12); vrp26_hyb_eve_vrp stays LIVE (56707958)
    root = Path(__file__).resolve().parents[1]
    plan = (root / "src/kagg3/core/plan.py").read_text()
    if "\nROUTE_VRP_FIX_ON = True" in plan:   # on the vrp26 tree (master, pack26_0930) the vrp25 defaults stay ON and the one new default is ON
        assert "\nOPP_SUPPLY_FAMILY_ON = True" in plan and "\nEVE_STOCK_ON = True" in plan


def test_det1_base_pin_row():
    """DETAGENT1 BACKUP row (not uploaded): vrp26's switches + DET1_BODY (the frozen crewF4Sbcfa body on every seat); SHIPPED unchanged."""
    import hashlib
    from pathlib import Path
    row, v26 = SHIPPED_PACKAGES["det1_base"], SHIPPED_PACKAGES["vrp26_hyb_eve_vrp"]
    assert row["md5"] == "e7ebb6a7" and row["ref"] == "839e86dd" and row["candidate"] and row["backup"] and "sub" not in row
    diff = {k for k in set(row["switches"]) | set(v26["switches"]) if row["switches"].get(k) != v26["switches"].get(k)}
    assert diff == {"DET1_BODY", "DET1_KNOBS"}
    assert SHIPPED != v26["ref"] == "bb4f077b" and SHIPPED == "ce0df430"   # the backup does not move the shipped pin (vrp27_vm_m3 did, SHIPSYNC12)
    root = Path(__file__).resolve().parents[1]
    plan = (root / "src/kagg3/core/plan.py").read_text()
    if "\nDET1_BODY = True" in plan:   # on a DET1 body tree: the recipe string is a pinned backup row's and the m1 weights are the pinned ones
        assert any('\nDET1_KNOBS = "%s"\n' % SHIPPED_PACKAGES[k]["switches"]["DET1_KNOBS"] in plan for k in ("det1_base", "det2_place"))
        w = root / "src/kagg3/prog/crewbc_w.npz"
        assert hashlib.md5(w.read_bytes()).hexdigest()[:8] == row["weights_md5"]
        assert "\nROUTE_VRP_FIX_ON = True" in plan and "\nEVE_STOCK_ON = True" in plan


def test_det1h_h1_pin_row():
    """DETAGENT1 hybrid BACKUP row (not uploaded): vrp26's switches + DET1_HYB_ON (h1 latch -> the det1_base body); SHIPPED unchanged."""
    row, v26, base = SHIPPED_PACKAGES["det1h_h1"], SHIPPED_PACKAGES["vrp26_hyb_eve_vrp"], SHIPPED_PACKAGES["det1_base"]
    assert row["md5"] == "f37f4b17" and row["ref"] == "0b64f848" and row["candidate"] and row["backup"] and "sub" not in row
    diff = {k for k in set(row["switches"]) | set(v26["switches"]) if row["switches"].get(k) != v26["switches"].get(k)}
    assert diff == {"DET1_BODY", "DET1_HYB_ON", "DET1_HYB_FIRE_CASH", "DET1_KNOBS"}
    assert row["switches"]["DET1_KNOBS"] == base["switches"]["DET1_KNOBS"] and row["switches"]["DET1_BODY"] == 0
    assert SHIPPED != v26["ref"] == "bb4f077b"


def test_det2_place_pin_row():
    """DETAGENT2 BACKUP row (not uploaded): det1_base + the an2_place placement role (DET1_KNOBS only); SHIPPED unchanged."""
    import hashlib
    from pathlib import Path
    row, d1 = SHIPPED_PACKAGES["det2_place"], SHIPPED_PACKAGES["det1_base"]
    assert row["md5"] == "d4fc94d5" and row["ref"] == "38626043" and row["candidate"] and row["backup"] and "sub" not in row
    diff = {k for k in set(row["switches"]) | set(d1["switches"]) if row["switches"].get(k) != d1["switches"].get(k)}
    assert diff == {"DET1_KNOBS"} and row["switches"]["DET1_KNOBS"] == d1["switches"]["DET1_KNOBS"] + ";an2_place=1"
    assert row["weights_md5"] == d1["weights_md5"]
    assert SHIPPED == "ce0df430"   # the backup does not move the shipped pin (vrp27_vm_m3 moved it, SHIPSYNC12)
    root = Path(__file__).resolve().parents[1]
    plan = (root / "src/kagg3/core/plan.py").read_text()
    if '\nDET1_KNOBS = "%s"\n' % row["switches"]["DET1_KNOBS"] in plan:   # on the det2 tree (detagent2_0930)
        assert "\nDET1_BODY = True" in plan and "\nDET1_HYB_ON = False" in plan
        w = root / "src/kagg3/prog/crewbc_w.npz"
        assert hashlib.md5(w.read_bytes()).hexdigest()[:8] == row["weights_md5"]
        assert 'K("an2_place", 0)' in (root / "src/kagg3/prog/direct.py").read_text()


def test_live_packages_differ_only_by_melonveto_post():
    """The second live slot is the RES940 package with one switch added."""
    assert SHIPPED_PACKAGES[56421514]["ref"] == "e7a8af84"
    assert SHIPPED_PACKAGES[56370365]["ref"] == "59021db"
    res940 = SHIPPED_PACKAGES[56370365]["switches"]
    vpost = SHIPPED_PACKAGES[56421514]["switches"]
    assert res940["RESIDUAL_ON"] == vpost["RESIDUAL_ON"] == 1
    assert {k for k in res940 if res940[k] != vpost[k]} == {
        "MELONVETO_POST_ON"
    }


def test_ship_le_pin_names_the_promoted_late_exec_tree():
    assert SHIPPED != "6df6635c"  # moved on by SHIP_VRP; LATE_EXEC_ON still True there


def test_ship_vrp_pin_names_the_promoted_route_vrp_tree():
    assert SHIPPED != "ca9232e7"  # moved on by SHIP_VRP2; ROUTE_VRP_ON still True there


def test_ship_vrp3_pin_names_the_needs_fix_tree():
    assert SHIPPED != "d6c64188"  # moved on by SHIP_VRP4; NEEDS_FIX still True there


def test_ship_vrp4_pin_names_the_deadline_tree():
    assert SHIPPED != "1b011580"  # moved on by SHIP_VRP5; the deadline is still there


def test_ship_vrp5_pin_names_the_repair_tree():
    assert SHIPPED != "d55fc4d5"  # moved on by SHIP_VRP10_ESW / vrp9_cs (09-27 pair)


def test_ship_final_pair_pin_names_the_upload_tree():
    assert SHIPPED != "a4c5cc9e"  # moved on by SHIP_VRP12_PFS; vrp10_esw 56600971 still live, vrp9_cs 56600958 retired


def test_ship_vrp12_pfs_pin_names_the_upload_tree():
    assert SHIPPED != "dcacbd33"  # moved on by SHIP_VRP14_K2REAL; vrp12_pfs 56612145 stays live, vrp10_esw 56600971 retired


def test_ship_vrp14_k2real_pin_names_the_config_tree():
    assert SHIPPED != "ba61be6f"  # superseded on this tree by SHIP_VRP15_K2FIRE (alternative candidate, never uploaded here)


def test_ship_vrp15_k2fire_pin_names_the_config_tree():
    assert SHIPPED != "b78bf1e4"  # moved on by SHIP_VRP17_K2HB; vrp15_k2fire 56634350 retired (FIFO) by vrp18 56646827


def test_ship_vrp17_k2hb_pin_names_the_config_tree():
    assert SHIPPED != "ec2a6042"  # moved on by SHIP_VRP18_K2HB2046; vrp17_k2hb 56643352 retired (FIFO) by vrp19w 56649892


def test_ship_vrp18_k2hb2046_pin_names_the_config_tree():
    assert SHIPPED != "599f8881"  # moved on by SHIP_VRP19W_K2WIDE; vrp18_k2hb2046 56646827 retired (FIFO) by vrp20 56652418


def test_ship_vrp19w_k2wide_pin_names_the_config_tree():
    assert SHIPPED != "81090f6a"  # moved on by SHIP_VRP20_PFSOFF; vrp19w_k2wide 56649892 stays live, vrp18_k2hb2046 56646827 retired


def test_ship_vrp20_pfsoff_pin_names_the_config_tree():
    assert SHIPPED != "b940d667"  # moved on by SHIP_VRP22_PFS_FP; the vrp20 re-upload 56686302 retired (FIFO) by vrp23_pfs_t 56687235


def test_ship_vrp21_clsearch_pin_names_the_config_tree():
    assert SHIPPED != "b1835440"  # vrp21_clsearch 56676381 retired (FIFO) by vrp22_pfs_fp 56686308


def test_ship_vrp22_pfs_fp_pin_names_the_config_tree():
    assert SHIPPED != "94f168ae"  # moved on by SHIP_VRP23_PFS_T; vrp22_pfs_fp 56686308 retired (FIFO) by vrp24_pfs_tfp 56687774


def test_ship_vrp23_pfs_t_pin_names_the_config_tree():
    assert SHIPPED != "08067309"  # moved on by SHIP_VRP24_PFS_TFP; vrp23_pfs_t 56687235 retired (FIFO) by vrp25_hyb_eve 56706557


def test_ship_vrp24_pfs_tfp_pin_names_the_config_tree():
    assert SHIPPED != "1d3d3443"  # moved on by SHIP_VRP25_HYB_EVE; vrp24_pfs_tfp 56687774 retired (FIFO) by vrp26_hyb_eve_vrp 56707958


def test_ship_vrp25_hyb_eve_pin_names_the_config_tree():
    assert SHIPPED != "1f187a4b"  # moved on by SHIP_VRP26_HYB_EVE_VRP; vrp25_hyb_eve 56706557 stays live


def test_ship_vrp26_hyb_eve_vrp_pin_names_the_config_tree():
    assert SHIPPED != "bb4f077b"  # moved on by SHIP_VRP27_VM_M3; vrp26_hyb_eve_vrp 56707958 stays live, vrp25_hyb_eve 56706557 retired


def test_ship_vrp27_vm_m3_pin_names_the_config_tree():
    assert SHIPPED == "ce0df430"  # vrp27_vm_m3 56718602 + vrp26_hyb_eve_vrp 56707958 (09-30 ~20:58Z final pair)


_FLAG = "--digests"


def src_path() -> str:
    """The `sys.path` entry this process must import `kagg3` from."""
    if _FLAG in sys.argv:
        return os.path.abspath(sys.argv[sys.argv.index(_FLAG) + 1])
    return "src"


def bootstrap():
    """Put the right tree on `sys.path`, import `kagg3`, and prove it.

    Call this at the TOP of a pin module, before `numpy`, before the shared
    fixtures, before anything.  Returns the `kagg3` module."""
    os.environ.setdefault("JAX_PLATFORMS", "cpu")
    path = src_path()
    sys.path.insert(0, path)
    import kagg3
    got = os.path.abspath(kagg3.__file__)
    want = os.path.abspath(path)
    assert got.startswith(want + os.sep), \
        f"the pin loaded {got}, not the tree under {want}"
    return kagg3


def digest(plan) -> str:
    """sha256 of the WHOLE plan tuple -- every array, not a summary of one."""
    import numpy as np
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def repo_root(module_file: str) -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(module_file)))


def tree_digests(module_file: str, ref: str = SHIPPED, env: dict | None = None):
    """Run `module_file` as a script against a pristine `git archive <ref> src`.

    `env` travels to the subprocess, which is how a knob reaches a tree whose
    own module default is the thing under test: the subprocess applies it after
    ITS import, exactly as every measured runner does."""
    e = dict(os.environ)
    e.update(env or {})
    e["PYTHONPATH"] = ""            # never let an inherited PYTHONPATH=src win
    root = repo_root(module_file)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {ref} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(module_file), _FLAG,
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True, env=e)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


def test_vrp27_vm_m3_pin_rows():
    """VRPMISS1 rows: vrp26's switches + ROUTE_VRP_MISS_ON (M3-all, LIVE as sub 56718602 since 09-30 ~20:58Z, SHIPPED = ce0df430,
    SHIPSYNC12) / + ROUTE_VRP_MISS_PROG_ONLY (M3-P, OPTION, not uploaded)."""
    from pathlib import Path
    v26, m3, m3p = (SHIPPED_PACKAGES[k] for k in ("vrp26_hyb_eve_vrp", "vrp27_vm_m3", "vrp27_vm_m3p"))
    assert m3["md5"] == "1133b789" and m3["ref"] == "ce0df430" and "candidate" not in m3 and not m3["retired"]
    assert m3["sub"] == 56718602 and m3["ship"] == "ce0df430" and SHIPPED == m3["ref"]
    assert m3p["md5"] == "c5599634" and m3p["ref"] == "2ae7cb31" and m3p["candidate"] and "sub" not in m3p
    diff = lambda a, b: {k for k in set(a["switches"]) | set(b["switches"]) if a["switches"].get(k) != b["switches"].get(k)}
    assert diff(m3, v26) == {"ROUTE_VRP_MISS_ON"} and diff(m3p, m3) == {"ROUTE_VRP_MISS_PROG_ONLY"}
    assert SHIPPED != v26["ref"] == "bb4f077b"
    plan = (Path(__file__).resolve().parents[1] / "src/kagg3/core/plan.py").read_text()
    if "\nROUTE_VRP_MISS_ON = True" in plan:   # on the vrp27 tree (master, vrpmiss1_0930) the vrp26 defaults stay ON
        assert "\nROUTE_VRP_FIX_ON = True" in plan and "\nEVE_STOCK_ON = True" in plan and '\nROUTE_VRP_MISS_CELL = "M3"' in plan
