# Gate design A: why the remote real gate false-accepts, and the flow186 flag set

2026-09-10 ~15:30Z. Blind review A (B is written independently). Read-only: no engine runs, no
edits, no remote writes. Time-boxed 30 min; §5 lists what the data cannot settle.

Sources: `S/glut/verdicts.log` (lines 2-144), `docs/strategy/2026-09-10-verdicts.txt`,
`docs/strategy/2026-09-09-judge-calibration.md`, `2026-09-09-gate-leg20.md`, remote
`~/stage_leg20/artifacts/{flow172,flow183,flow184,flow184b,flow185b,flow185c}/real_gate.log`
(+ `real_gate.json`, `real_gate.csv`, `train.log`), `~/launch_flow18{3,4,4b,5,5b,5c,6}.sh`,
`~/stage_leg20/src/kagg3/es/train.py` (`RealGate._decide_pinned`, `_leg20_verdict`, `beats`),
`~/stage_leg20/artifacts/town_schedules.json` (331 pinned towns).

## 0. TL;DR

* The gate that agreed with the local judge is the **leg20** gate (flow172): 4 of 4 locally judged
  ACCEPTs were confirmed (g60, g300, g940, g1000), 1 refusal (g170) was consistent. Both
  false accepts of the day (flow184 g10, flow185c g10) came from the **`--real-gate-metric win`
  flip-count rule**, which has **no margin condition at all**: net flips >= 3 (= 1.5 boards,
  because the two pinned seats return the same outcome) and cand_wins > inc_wins.
* On this data the statistic that separates judge-confirmed from judge-refused thetas is the
  **paired all-games coin margin per game on the gate's own boards**, not the flip count:
  confirmed accepts read +274…+782/game, the false accepts +59 and +269/game, and g940 -- the
  largest live gain of the campaign -- read **0 net flips**. Flips are the 15-coin lottery the
  09-09 calibration already documented; they must be a *floor* (no net drop), never the *signal*.
* `--real-gate-paired-t` is **ignored in pinned mode** (the log banner says so), so a paired t
  cannot be requested from the trainer as-is. The nearest available rule is
  `--real-gate-metric margin --real-gate-min-gain G --real-gate-win-floor 0` on a large enough
  field that `G` is ~2 SE. With per-board sd ~2,500 coins (the local judge's sd column) that
  means >= ~140 boards at one seat.
* Recommended flow186 gate: the **138-board union LIVE55 + LIVE-C63 + TOPB2 at 1 seat**, metric
  margin, min-gain 400, win-floor 0, every 100 gens. On the six judged decisions it gives 0
  false accepts, refuses the two bad ones, and would have delayed (not lost) g300 and g1000.
* Second-order cause, could not be verified in the time box: the gate plays **raw thetas** while
  the judge and the shipped file play **theta + pair defaults + HIRE_ROW_ON**. flow185c g10 was
  +269/game on the gate's 42 boards but -1,090/game on the same 20 TOPB2 boards under the judge.
  Stage flow186 in the pair/hire-row tree (flow180/181b already had one) so the gate measures the
  composition that ships.

## 1. Every remote decision that has a local judge read

Gate columns are the gate's own paired numbers (candidate minus incumbent on the pinned rows).
`net` = flips - drops in games (2 seats => 2 games per board). `dM/g` = margin delta per game.
Local columns are `S/bank/paired.py ALL` lines or the verdict-log summaries (win_off -> win_on,
dmargin, t, flips/drops). "Judge" = the local win-rate-first verdict.

| arm / gen | gate field, n games | gate metric | gate delta (wins, dM/g, flips/drops, net) | gate verdict | local LIVE62 / LIVE55 | local LIVE-C | local TOPB / TOPB2 | judge | agree? |
|---|---|---|---|---|---|---|---|---|---|
| flow172 g60 | leg20 field (60 opp), 120 | leg20 | 44->53, **+782**, +9/-0, +9 | ACCEPT | g60pair vs base 34.5->64.5 % (LIVE55) | - | - | accept (vs base; incumbent g0 not read) | yes (weak: vs base only) |
| flow172 g170 | same, 120 | leg20 | 51->67, +646, **+16/-0, +16**; leg -954 | **refuse** (leg delta < 0) | g170c LIVE55 65.5 % = g60's 64.5 % (level) | - | - | level vs the lineage | consistent (a +16-net-flip candidate the judge read as level) |
| flow172 g300 | same, 120 | leg20 | 61->68, **+274**, +9/-2, +7; leg +14,834/24 | ACCEPT | g300pair vs base 70.9 % +6,753 t 9.95 47/53 | - | TOPB +3,730 t 2.1 | accept | yes |
| flow172 g940 | same, 120 | leg20 | 76->76, **+551**, +2/-2, **0**; leg +9,196 | ACCEPT | g940pair vs base 83.6 % (+54/-0) +9,130 t 14.2; vs g300pair +2.4k/g (LOSS20 t 10.4 vs 5.6) | LIVE-C63 62.7 % (= live pool 61.9 %) | TOPB 25->35 % (+4/-0) +5,578 t 3.3 | accept (largest read of the campaign) | yes -- **with zero net flips** |
| flow172 g1000 | same, 120 | leg20 | 76->80, **+429**, +6/-2, +4; leg +8,350 | ACCEPT | h2h vs g940pair LIVE62 wins 80.6->87.1 %, +191 t 0.65 (level margin) | LIVE-C22 -67 (50->50 %); LIVE-C63 61.1 vs 62.7 % (level) | TOPB 35->40 % (+2/-0) +5,758 t 3.3 vs base | accept on wins (band), level on margin | yes (marginal) |
| flow184 g10 (plant-floor gene) | same 60-opp field, 120 | **win**, min_flips 3 | 80->84, **+59**, +4/-0, +4 | ACCEPT | vs hr file: LIVE62 88.7->88.7 %, +20, 0/0, **102/124 identical** | LIVE-C22 63.6->59.1 %, +133 t 1.3, 0/2 | TOPB2 -69, 0/0, 31/40 identical | **REFUSE** (= shipped file with the floor off) | **NO -- false accept** |
| flow185c g10 | LIVE-C22+TOPB2, 84 | **win**, min_flips 3 | 29->32, **+269**, +8/-5, +3 | ACCEPT | vs hr file: LIVE62 88.7->**82.3 %**, -781 sd 2,729 t -2.25, **0/8** | LIVE-C63 68.3->68.3 %, -560 sd 2,570 t -1.73, 6/6 | TOPB2 25->30 %, **-1,090** sd 2,465 t -1.98, 2/0 | **REFUSE** | **NO -- false accept** |

Decisions with NO local read (refused candidates are never saved; listed for the statistic only):

| arm / gen | field, n | metric | gate delta | verdict |
|---|---|---|---|---|
| flow172 g600 / g630 / g650 | 120 | leg20 | +6 / +6 / +5 net flips, margin -104 / -92 / -27 per game, leg -8,380 / +5,362 / +3,142 | refuse (all-games delta < 0) |
| flow172 g800 / g900 / g1100 / g1110 / g1200 | 120 | leg20 | net -3 / +2 / -3 / +1 / -3; leg +1,786 / -8,288 / -17,722 / -15,176 / -16,362 | refuse |
| flow183 g10 / g20 / g60 | 120 | leg20 | net -4 / -2 / -4; dM/g -953 / -507 / -191; leg -10.9k / -30.3k / -14.8k | refuse (arm killed, rule 4) |
| flow184b g10 | 120 | win | 12->22, +10/-0, dM/g +3,117 vs a crippled melon-floor seat | ACCEPT (candidate = the floor turned down; not judged, arm killed) |
| flow185b g10 | LIVE-C63+TOPB2, 166 | win, min_flips 3 | 83->82, +2/-3, net -1, dM/g -72 | refuse |
| flow181b g10 / g60 / g100 | 96 (pair tree) | win, min_flips 3 | 63.5 / 64.6 / 68.8 % vs bar 65.6 %/+5,157; g100 +4,794 | refuse x3 (arm killed) |

Also in the record: flow180 (winfirst gate, min_flips 6 on family boards) refused 16 candidates in
a row with net +10 boards on the 96-game bar (g500 71.9 %/+5,287 vs 61.5 %/+1,530) and re-centred
the theta to its init on every third refusal; the fetched "g500" was the incumbent, so that arm has
no local read either. It is the mirror image of the false accepts: a flip floor set high enough to
be safe stops the search.

## 2. False-accept / false-refuse counts and the separating statistic

* **Local-judged decisions: 7** (5 leg20, 2 win-metric).
* **False accepts: 2 of 3 win-metric accepts judged** (flow184 g10, flow185c g10; flow184b g10
  unjudged). **0 of 4 leg20 accepts.**
* **False refuses: 0 demonstrated.** g170 (refused with +16 net flips) read level locally. Every
  other refusal was never judged, so the false-refuse rate of leg20 is unmeasured (§5).
* Kaggle: g940pair (leg20 accept) 64W-28L ~2545; g1000pair_hr (leg20 accept + hire row) 51W-14L
  ~2381 mid-ramp at 78 % -- consistent with the judge's "level or slightly better" head-to-head.
  No file from a win-metric accept has been uploaded, so Kaggle cannot score the false accepts.

Which gate statistic separates the judge-confirmed from the judge-refused thetas:

| statistic | confirmed accepts (g60, g300, g940, g1000) | judge-refused (flow184 g10, flow185c g10) | separates? |
|---|---|---|---|
| net flips (games) | +9, +7, **0**, +4 | +4, +3 | **no** -- g940 is the best theta and the lowest count; the false accepts sit inside the confirmed range |
| flips - drops as a share of n | 7.5 %, 5.8 %, 0 %, 3.3 % | 3.3 %, 3.6 % | no |
| all-games margin delta per game | **+782, +274, +551, +429** | **+59, +269** | yes for flow184 (+59); flow185c (+269) ties g300 (+274) -- see next row |
| approximate paired t on the margin delta (per-board sd 2,500 from the local judge; SE = 2,500/sqrt(boards)) | 60 boards: 2.4, 0.85, 1.7, 1.3 | 60 boards: 0.18; 42 boards: **0.70** | a threshold of t >= ~1.0 (min-gain ~ +330/game at 60 boards) refuses both false accepts and keeps g60, g940, g1000; **g300 (t 0.85) is lost** -- delayed, not lost, because the same lineage produced g940 |
| leg20 family delta | +? (g60), +14,834, +9,196, +8,350 | n/a (different boards) | the leg20 rule *is* what refused g600/g630/g650 (+5…+6 net flips, margin down) -- the "all-games delta >= 0" floor did that work |
| a win-floor on the band boards (LIVE62 part, no net drop) | g1000: +8 boards; others vs base only | flow184: 0/2 on LIVE-C; **flow185c: 0/8 on LIVE62** | yes -- flow185c's damage was on the 1900-2100 band, which its 42-board gate never played |

Reading: the two false accepts share a signature -- **tiny or subset-only margin gain bought with
losses on boards the gate did not play** -- and the rule that admitted them reads only a count on
the 15-coin outcome-unstable boards (09-09 calibration: net flips sd 3.1 across 24 arms, 0 true
positives; mean +2.8, i.e. "+3" is the arm-to-arm *average*). The threshold that separates this
data is a paired margin delta of about **+300…+400 coins/game with ~2 SE behind it, plus a no-net-
drop floor**; the flip count should be demoted to that floor.

Note on seats: `_decide_pinned` documents that both seats of a pinned tape return the same outcome,
so `--real-gate-min-flips 3` at 2 seats is 1.5 boards and an odd count (flow185c +8/-5) means at
least one seat-disagreeing board -- exactly an outcome-unstable one.

## 3. Cost of a gate evaluation on the remote

From `real_gate.log` ("N games in Ss", 10 workers) and `train.log` (s/gen):

| field | games/leg | seconds/leg (typical / when both GPUs gate at once) | round = candidate + incumbent re-play |
|---|---|---|---|
| flow172/183/184 60-opp field, 2 seats | 120 | 217-224 s / 350-430 s | ~440 s (7-8 min) |
| flow185c 42 boards, 2 seats | 84 | 156-157 s | ~315 s |
| flow185b 83 boards, 2 seats | 166 | 304-334 s | ~640 s |

That is **~1.85 s per game per leg at 10 workers (~18.5 worker-seconds/game)**, linear in games.
The incumbent is **re-played every round** although a pinned game is deterministic (the log's own
banner says "the seed decides nothing"), so a round costs twice what it needs to; a cache is a
source change (out of scope here) and would halve every figure below.

Training runs at **55-61 s/gen** (flow185b/c, flow172), so `--real-gate-every 100` is one
periodic gate per ~95 min, plus a record gate whenever `--abs-every 10` nominates one (a gen-10
candidate was decided at gen 16-18, i.e. the gate is asynchronous and cost the training loop
nothing visible). Budgeting the gate at <= 1/3 of the periodic interval (~1,900 s per round, so
two arms can gate simultaneously without the 430-s stalls):

* at 2 seats: 1,900 / 2 legs / 1.85 s = ~510 games = **~255 boards**;
* at 1 seat (`--real-gate-pinned-seats 1`; the second seat is a duplicate outcome): **~510 boards**.

The remote has 331 pinned towns, of which the held-out judge boards are 62 + 63 + 20 = 145
(all present with tapes; verified). So **the entire local judge (138 boards after dropping the 7
LIVE62 training rungs) fits in one gate round at 1 seat (~255 s/leg, ~8.5 min/round)** and at 2
seats (~510 s/leg, ~17 min/round) -- both inside the budget for a gate every 100 gens, and still
tolerable for record gates every 10 gens at 1 seat.

## 4. Recommendation: the flow186 gate

Field (all ids exist in `~/stage_leg20/artifacts/town_schedules.json` and
`artifacts/panel_opp_town/opponent_tape_<id>/main.py`; checked 15:20Z):

* **LIVE55** = `S/live62/ids.txt` minus the 7 training rungs `106945656 106947016 106948946
  106957848 106963001 106963950 106964777` (they are `tape_act_*` rungs in `launch_flow186.sh`,
  so they must not be judge boards). Keep `107088554` / `107095149` in the field (played, non-
  byte-exact; the local judge excludes them from its t but they are 2 of 138).
* **LIVE-C63** = lines 1-63 of `S/livec/ids.txt` (the 9 ids appended by the 63->72 growth stream
  are NOT on the remote yet -- do not list them until pushed append-only).
* **TOPB2** = `S/topb2/ids.txt` (20).

Total **138 boards**, none in any training rung (the 42 + 41 pushes were verified "0 of 83 in any
rung"; LIVE55 is the flow172 gate's own held-out band set).

Flags (replace the `--real-gate-*` block of `~/launch_flow186.sh`; everything else unchanged):

```
--real-gate --real-gate-every 100 --real-gate-seed-base 20260904 \
--real-gate-pinned artifacts/town_schedules.json --real-gate-pinned-seats 1 \
--real-gate-metric margin --real-gate-min-gain 400 --real-gate-win-floor 0 \
--real-gate-min-flips 0 --real-gate-recentre 3 --real-gate-workers 10 \
--real-gate-opponent <138 main.py paths: LIVE55 (55), then LIVE-C63 lines 1-63, then TOPB2 (20)>
```

What each choice buys, on the evidence above:

* `--real-gate-metric margin` + `--real-gate-min-gain 400`: accept iff the paired mean coin
  margin over the 138 games beats the incumbent's by >= 400/game. With sd ~2,500/board that is
  SE ~213 -> **t ~1.9**. Replayed on the seven judged decisions: g60 (+782) accept, g940 (+551)
  accept, g1000 (+429) accept, g300 (+274) refuse, flow184 g10 (+59) refuse, flow185c g10
  (+269) refuse, g170 (+646 on its own field) accept -- 5/7 with the judge, the two misses being a
  delayed true positive (g300) and g170, which the judge read as level and the leg20 gate refused
  on the family delta. **0 false accepts on this data; expected false-accept rate under the rule
  ~1-2 in 20 at t ~1.9 if the candidates are null, vs 2 of 2 (judged) for the flip-count rule.**
* `--real-gate-win-floor 0`: `beats()` refuses any candidate whose pinned win count is below the
  incumbent's. This is the win-rate-first veto: it alone would have refused flow185c g10 (-8 on
  LIVE62) and flow184 g10 (-2 on LIVE-C). It cannot refuse a net-zero candidate, which is what
  `min_gain` is for.
* `--real-gate-min-flips 0`: not read under metric margin (the trainer refuses a non-1 value
  without `--real-gate-pinned`, so 0 is legal here and documents the intent); flips/drops are
  still logged per tape id, which is what the operator reads.
* `--real-gate-pinned-seats 1`: halves the cost with no loss (duplicate outcomes) and makes the
  logged flip count a board count.
* Field = the local judge: the gate then reads what the judge reads -- the band (LIVE55, where
  regressions show as drops), the target band (LIVE-C63) and the top tier (TOPB2) -- rather than
  a 42-board subset that let flow185c trade band losses for two top-tier flips.
* `--real-gate-recentre 3` unchanged: with a stricter gate, re-centring after three refusals
  keeps the ES near the last confirmed record instead of drifting (the flow180 failure was
  min_flips 6, not recentre).

Two things that are NOT flags and matter as much:

1. **Stage flow186 in the tree where the tail pair and HIRE_ROW_ON are defaults** (flow180's
   commit b906407 tree + hire row, or ship-pair-hr). Every gate number today is raw-theta;
   every judge number and the shipped file carry the switches. flow185c g10 read +269/game on the
   raw gate and -1,090/game with switches on the *same 20 TOPB2 boards*: either the gate's 42-board
   read was the seed-set lottery or the candidate interacts with the switches -- in both cases the
   gate should be measuring the composition that ships. The seat gate at gen 0 will then read
   ~89/68/25 % on the three sub-fields instead of 66.7/50/34.5 %.
2. Keep the local judge as the promotion gate anyway. The remote gate's job is to stop the ES
   re-centring onto lottery winners; at min-gain 400 it will refuse more often, and a refused
   theta is never saved -- so pair it with `--keep-candidates` (the flag exists, see
   `setup_real_gate`) if the operator wants to hand-judge near misses like g300.

If the operator prefers the stricter reading of the judge's own rule (t >= 2 on the margin AND no
net drop), use `--real-gate-min-gain 450`; at 300 the rule accepts g300 but flow185c (+269) sits 31
coins under it and that is not a separation the data supports.

## 5. What could not be determined from the data

* **False-refuse rate of any gate.** Refused candidates are never written to disk, so none of
  flow172 g600/g630/g650 (+5…+6 net flips, refused on margin), flow183 g10-g60, flow185b g10 or
  flow181b g10-g100 has a local read. The leg20 gate's "0 false accepts in 4" is therefore
  one-sided; the calibration's warning that its 24-game family sum has SE ~18k stands.
* **Whether flow185c g10 is a switch interaction or a seed-set lottery.** Resolving it needs one
  engine run: raw g10 vs raw g1000 on TOPB2 locally (should reproduce the gate's +269/game if the
  sim=engine claim holds) and then with switches. Not run (read-only task).
* **The per-board sd on the gate's own fields.** The gate writes only the mean per leg
  (`real_gate.csv` holds the last leg's rows: 84 rows for flow185c, 121 for flow172, not the
  history), so the "t ~1.9 at min-gain 400" uses the local judge's sd (2,465-2,729 per board on
  TOPB2/LIVE-C63/LIVE62). The pooled 138-board sd may differ; the lopsided TOPB2 boards
  (+54.5k, +21.2k) will inflate it. A first periodic round of flow186 will show the actual
  candidate-vs-incumbent spread and the threshold should be re-read then.
* **Whether the 100-gen periodic gate is the binding cost.** Record gates fire whenever
  `--abs-every 10` nominates (gen 10 in every arm today); at 138 games/leg and 1 seat that is
  ~8.5 min per nomination, fine at today's cadence but not measured under two arms gating at once.
* **The g170 case**: +16 net flips, +646/game on the gate, refused by the family delta (-954),
  and read locally at 65.5 % vs g60's 64.5 % against the *base*, never head-to-head against its
  incumbent g90. It may be a true positive the leg20 gate lost; the margin rule above would have
  accepted it. Unresolvable without the head-to-head.
* **Kaggle validation of any false accept** -- none was uploaded, by design.
