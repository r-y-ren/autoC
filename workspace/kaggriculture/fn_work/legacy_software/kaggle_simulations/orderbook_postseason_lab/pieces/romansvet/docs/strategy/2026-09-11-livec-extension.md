# LIVE-C extension to 102 boards (2026-09-11 00:25-00:35Z)

Purpose: the held-out slice of LIVE-C had shrunk to ids 43-72 (30 boards; 1-42 are training rungs of
flow187/190/191). Thirty more pinned-town boards were cut from our live entry (sub 56140532, g940_pair)
so the auto-judge can add a second hold-out leg (LIVEC-H30B) and read 60 held-out boards.

## Selection (S/livec/eps_new4.json, ListEpisodes pulled 00:25Z, 143 completed games, 97 W)
Rule: opponent updatedScore 2450-2700, id not in any S/*/ids.txt (114 excluded ids), take the LATEST 30
that qualify (49 qualified). No cherry-picking of losses. Result: live 20 W / 10 L, ratings 2512-2685
(median 2599), 2026-09-10 19:12Z .. 2026-09-11 00:08Z. coin-exact = tape_opponent.py verify() passed
for BOTH the drawn tape and the pinned-town tape (opponent replayed to the coin): 30/30.

| # | episode | createTime (UTC) | opponent | opp rating | live g940 | live margin | g1000 hr base margin | coin-exact |
|---|---|---|---|---|---|---|---|---|
| 73 | 107569075 | 2026-09-10 19:12:14 | MCZK | 2569 | W | +2101 | +3990 | yes |
| 74 | 107573857 | 2026-09-10 19:32:13 | JOSHNA ACSHA S 21CS | 2609 | L | -3480 | -2958 | yes |
| 75 | 107578665 | 2026-09-10 19:52:12 | Cường Dược Sĩ | 2543 | W | +2183 | +1117 | yes |
| 76 | 107583491 | 2026-09-10 20:12:14 | Claudex - An | 2634 | L | -879 | +1028 | yes |
| 77 | 107583470 | 2026-09-10 20:12:14 | waticson | 2562 | W | +4570 | +3098 | yes |
| 78 | 107584581 | 2026-09-10 20:16:11 | prvsiyan | 2622 | L | -8133 | -8078 | yes |
| 79 | 107587205 | 2026-09-10 20:28:11 | ToastUz | 2579 | W | +11851 | +13490 | yes |
| 80 | 107588978 | 2026-09-10 20:36:12 | JOSHNA ACSHA S 21CS | 2612 | L | -4411 | -7933 | yes |
| 81 | 107588989 | 2026-09-10 20:36:12 | Héctor Valverde | 2512 | W | +7098 | +10493 | yes |
| 82 | 107593329 | 2026-09-10 20:52:12 | Sirui Zeng | 2603 | W | +11818 | +15032 | yes |
| 83 | 107597391 | 2026-09-10 21:08:11 | yomogii | 2652 | W | +13203 | +13404 | yes |
| 84 | 107600681 | 2026-09-10 21:24:09 | kaggricodex | 2597 | L | -1318 | -636 | yes |
| 85 | 107601374 | 2026-09-10 21:24:11 | 西松大祐 | 2601 | W | +8081 | +10016 | yes |
| 86 | 107605233 | 2026-09-10 21:40:11 | Baidalin Adilzhan [dsml.kz] | 2587 | W | +7649 | +7079 | yes |
| 87 | 107606449 | 2026-09-10 21:48:10 | kaggricodex | 2515 | W | +12968 | +15776 | yes |
| 88 | 107608950 | 2026-09-10 21:56:10 | KARGI | 2529 | W | +9739 | +10867 | yes |
| 89 | 107608938 | 2026-09-10 21:56:10 | yuki0731 | 2622 | W | +13235 | +16299 | yes |
| 90 | 107611867 | 2026-09-10 22:08:10 | nailong alpha | 2602 | W | +5915 | +4725 | yes |
| 91 | 107615824 | 2026-09-10 22:24:10 | Lin | 2633 | W | +8683 | +9006 | yes |
| 92 | 107616563 | 2026-09-10 22:28:09 | r13721 | 2636 | L | -10704 | -5759 | yes |
| 93 | 107620742 | 2026-09-10 22:46:51 | Fih | 2685 | L | -6561 | -6756 | yes |
| 94 | 107623247 | 2026-09-10 23:00:49 | MAC SAHO | 2553 | L | -1824 | -2935 | yes |
| 95 | 107627530 | 2026-09-10 23:16:51 | Joe Muller | 2520 | W | +4868 | +8888 | yes |
| 96 | 107630176 | 2026-09-10 23:28:48 | Abhinav0370 | 2572 | L | -5705 | -4873 | yes |
| 97 | 107632627 | 2026-09-10 23:36:46 | kobq | 2568 | L | -2090 | -1424 | yes |
| 98 | 107636602 | 2026-09-10 23:52:46 | Harris Bashir | 2582 | W | +10910 | +9338 | yes |
| 99 | 107637410 | 2026-09-10 23:56:45 | clouds111 | 2620 | W | +13849 | +11078 | yes |
| 100 | 107638319 | 2026-09-11 00:00:48 | i3 | 2631 | W | +8150 | +10070 | yes |
| 101 | 107637894 | 2026-09-11 00:00:48 | JezzLynn | 2574 | W | +11059 | +12622 | yes |
| 102 | 107639984 | 2026-09-11 00:08:44 | Ne ML Clan | 2638 | W | +24365 | +24762 | yes |

## Base read (shipped composition: theta flow172_g1000 + OPEN_PUMP,TAIL_FILL,BANK_BEFORE_LOT,HIRE_ROW)
- ids 73-102, both seats, seed-shifted (seed_base 777001 + 1000003*72): **21/30 boards won = 70.0 %**
  (42/60 rows), **mean margin +5,694** (sd 8,272, median +7,984).
- Live g940_pair in the same episodes: 20 W / 10 L (66.7 %). Board-level W/L agreement live vs base:
  29/30 (only board 76, Claudex - An, flips: live -879, base +1,028).
- Comparison: the 43-72 hold-out base reads 19/30 = 63.3 %, +2,951 on the same csv; 73-102 reads HIGHER (70.0 %, +5,694) despite the higher-rated
  slice (median opp 2599 vs the 2300-2500 band of the earlier appends) -- the two 30-board reads differ by 2 boards, i.e. within the board lottery.
- Reproduction check: board 107507032 (list index 71) re-run inside the extension run gave 2/2 rows
  byte-identical to the existing csv rows, so seeds and the arms-next tree match the old rows.

## Files created / changed (all append-only)
- S/livec/ids.txt 72 -> 102 lines (backup S/livec/ids.txt.bak72); order is load-bearing, never reorder.
- artifacts/tape_actions_town/<id>.npz, artifacts/panel_opp_town/opponent_tape_<id>/ (30 new, pinned town),
  artifacts/tape_actions/<id>.npz, artifacts/tape_games/<id>.npz, artifacts/panel_opp/opponent_tape_<id>/
  (30 new, drawn), S/ep_<id>.json (raw replays, ~32 MB each), S/merge/tg_<id>.npz.
- S/band2100p/town_schedules.json 352 -> 382 rows (backup .bak_20260911T002846Z; old rows verified intact).
- S/lossflip/g1000pair_hr_livec.csv 144 -> 204 rows (backup .bak72; existing rows untouched, 60 appended).
  Raw extension output: S/livec/ext2/g1000pair_hr_ext2.{csv,log}.
- Scripts: S/livec/cut_one.sh + S/livec/cut_append2.sh (parallel cutter, P=6; ~2.5 min for 30 episodes),
  S/livec/extend_new2.sh (base extension for indices >= 71, WT/OUT/FIRST overridable),
  S/livec/extend_g1000pair_hr_2.sh (the locked driver + repro gate that appended the rows),
  S/livec/run_holdout2.sh (LIVEC-H30B leg: ids 73-102, csv S/lossflip/<name>_livech2.csv,
  log S/livec/<name>_holdout2.log, summary line appended to S/livec/chain_summary.txt).
- S/livec/provenance.txt APPEND #5, S/livec/README.txt one line. S/autojudge/watch.sh NOT edited.

## How to run the new hold-out leg for a theta
    ( flock 9; bash S/livec/run_holdout2.sh <name> <worktree> <theta.npy> "OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True" ) 9>/root/kagg3_judge.lock
It prints the paired.py ALL line vs the g1000pair_hr base (60 rows, 30 boards); the 43-72 leg
(run_holdout.sh) and this one are disjoint, so their rows can be concatenated for a 60-board read.
Do not call it from inside S/autojudge/watch.sh --legs (that already holds the lock).

## Notes / dead ends
- extend_new.sh hard-codes FIRST=62, the arms-next tree and a scratchpad path wiped by the 09-10 reboot,
  so extend_new2.sh is a parameterised copy; the base csv rows came from arms-next (S/livec/g1000pair_hr.log),
  so the extension used arms-next too (not ship-pair-hr) and the byte-exact repro row confirms equivalence
  for this composition. extend_g1000pair.sh's repro gate used `bc` (missing) and had reported a false
  MISMATCH on 09-10; the new driver uses plain integer tests.
- g940pair_livec.csv (72 boards) and g1000pair_livec.csv (63) were NOT extended (out of scope; run
  extend_new2.sh with FIRST=71 / FIRST=62 and the matching switches if a leg needs them).
- Only 49 episodes qualified in the 2450-2700 band; a further append can draw on the 19 older ones or on
  sub 56143250 (g1000_pair_hr) once its band games accumulate.
