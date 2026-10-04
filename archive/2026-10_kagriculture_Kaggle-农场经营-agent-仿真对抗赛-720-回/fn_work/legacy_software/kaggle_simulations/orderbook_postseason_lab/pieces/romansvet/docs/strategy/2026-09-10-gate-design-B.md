# Gate design B (blind): why the remote real gate false-accepts, and the flow186 flag set

Blind, independent review, 2026-09-10 15:07-15:37Z, read-only. Sources: `S/glut/verdicts.log`,
`docs/strategy/2026-09-09-verdicts.txt`, remote `~/stage_leg20/artifacts/{flow172,flow183,flow184,flow184b,flow185b,flow185c}/real_gate.log`,
`~/launch_flow17x/18x.sh`, `~/stage_leg20/src/kagg3/es/train.py` (`_decide_pinned`), `artifacts/town_schedules.json`.
The other gate-design doc was not read.

## 0. What the gate actually does (read off the code, not the memory)

* Pinned mode: every gate opponent is played once per seat on its pinned town; the game is deterministic
  (`sd 0` on nearly every row), so a gate read has NO seed noise -- its only noise is the BOARD SET.
* `--real-gate-metric leg20` (flow172, flow183): ACCEPT iff paired coin delta over the 12 leg-family
  tapes (24 games) > 0 AND all-games delta >= 0. `min_flips` is NOT read; net flips are printed as a screen.
* `--real-gate-metric win` (flow184/184b/185b/185c): ACCEPT iff `flips - drops >= min_flips` AND
  `cand_wins > inc_wins`. Counted in GAMES (2 seats, seats agree on almost every board, so one board
  flip = +2). There is NO margin clause under `win`.
* In pinned mode `--real-gate-paired-t`, `--real-gate-games`, `--real-gate-replicate`,
  `--real-gate-seed-per-opponent` are IGNORED (banner line 4 of every log). A paired-t rule is not
  available without a code change.
* Refused candidates are not saved (`real_gate_cand.npy` is overwritten; `best_abs.npy` = record only).

## 1. Every remote decision that has a local judge read

Gate columns are the remote log's own numbers (wins = games of the field, net = flips - drops in games,
d-margin = coins/game over the whole field, leg = leg20 family delta over 24 games). Local columns are
`S/bank/paired.py` reads as logged (LIVE55/LIVE62 vs base flow135_g350 unless "h2h"; TOPB/TOPB2/LIVE-C
vs the incumbent shipped file). "Judge" = the promotion decision actually taken on those reads.

| arm / gen | gate field | gate decision | gate wins | net (flips/drops) | d-margin /game | leg20 | local reads | judge | agree? |
|---|---|---|---|---|---|---|---|---|---|
| flow172 g60 | 60 band tapes, 120 g | ACCEPT | 44->53 | +9 (9/0) | +782 | +41,942 | LIVE55 34.5->58.2 % (+28/-2) +4,834 t 8.35 47/53; LOSS20 0->25 % | promote (over flow166_g170 52.7 %) | YES |
| flow172 g90 | same | ACCEPT | 53->51 | -2 (2/4) | +172 | +6,744 | LIVE55 58.2 % (+28/-2) +4,966 t 7.63 = same flip set as g60 | level, not promoted | NO (false accept, harmless) |
| flow172 g170 | same | REFUSE (leg -4,210) | 51->67 | +16 (16/0) | +646 | -4,210 | LIVE55 34.5->65.5 % (+36/-2) +5,930 t 8.87 48/53; LOSS20 35 % | best read of the campaign, packaged (g170c) | NO (false refuse) |
| flow172 g200 | same | ACCEPT | 51->63 | +12 (16/4) | +922 | +1,532 | LIVE55 65.5 % (+36/-2) +5,850 t 9.02; veto clear; TOPB 20 % | accept (= g170c) | YES |
| flow172 g260/g300 | same | ACCEPT/ACCEPT | 63->61 / 61->68 | -2 (4/6) / +7 (9/2) | +359 / +274 | +11,774 / +14,834 | (read as the g300 theta) LIVE55 69.1 % (+40/-2) +6,158 t 9.1; TOPB 30 % +3,730 t 2.1 (pair) | promote (g300pair shipped) | YES for g300; g260 has no separate read |
| flow172 g400 (periodic) | same | ACCEPT | 68->65 | -3 (4/7) | +74 | +12,266 | LIVE55 65.5 % (+36/-2) +6,455; LIVE-B 59.1 %; "WINS LOWER on every leg" vs g300 | g300 stays lead | NO (false accept) |
| flow172 g940 | same | ACCEPT | 76->76 | 0 (2/2) | +551 | +9,196 | LIVE55 81.8 % (+52/-0) +8,734 t 15; pair 83.6 %; TOPB 35 % +5,578 t 3.3; LOSS20 65 % | promote, shipped (sub 56140532, 64W-28L ~2545) | YES (cumulative g300->g940; the single step read net 0) |
| flow172 g1000 (periodic) | same | ACCEPT | 76->80 | +4 (6/2) | +429 | +8,350 | LIVE55 89.1 % (+60/-0); h2h vs g940pair on LIVE62 80.6->87.1 % +191 t 0.65 (level margin); TOPB 40 % +5,758 | accept (HOLD, then shipped as hr, sub 56143250 51W-14L ~2381 mid-ramp) | YES (marginal) |
| flow172 g1100/g1110/g1200 | same | REFUSE x3 | 80->77/81/77 | -3/+1/-3 | -152/-212/-576 | all < 0 | ES mean at g1230 (not the candidates): TOPB -903 (2 drops), LIVE-C22 +281 (6 drops), LIVE62 +406 (+4/-4) | not ahead | consistent (indirect) |
| flow183 g10/g20/g60 | same | REFUSE x3 | 80->76/78/76 | -4/-2/-4 | -953/-507/-191 | all < 0 | none (refused thetas not saved) | - | n/a |
| flow184 g10 (plant-floor gene) | same 60, metric win, min_flips 3 | ACCEPT | 80->84 | +4 (4/0) | +59 | - | TOPB2 -69 (31/40 identical); LIVE-C22 63.6->59.1 % (0/2) +133 t 1.3; LIVE62 88.7->88.7 % +20 (102/124 identical) | = shipped file with the floor off; arm killed | NO (false accept, level theta) |
| flow184b g10 (melon +0.30 seat) | same | ACCEPT | 12->22 | +10 (10/0) | +3,117 | - | not judged (seat itself 10 %/-12.8k on the band; family closed) | - | n/a |
| flow185b g10 | 83 = LIVE-C63+TOPB2, 166 g | REFUSE | 83->82 | -1 (2/3) | -72 | - | none (not saved) | - | n/a |
| flow185c g10 | 42 = LIVE-C22+TOPB2, 84 g | ACCEPT | 29->32 | +3 (8/5) | +269 | - | TOPB2 25->30 % (+2/0) -1,090 t -2.0; LIVE-C63 68.3->68.3 % (6/6) -560 t -1.7; LIVE62 88.7->82.3 % (0/8) -781 t -2.25 | REFUSED | NO (false accept, worse on all three) |

Also on record (different arm, same leg20 currency, from `2026-09-10-winfirst-gate.md`): flow168 refused a
candidate that took the 56-board held-out live family from 98 to 108 wins (+14/-4) because the family
margin read -608/game -- a second false refuse of the leg20 metric.

## 2. Counts, and the statistic that separates

Decisions with a local read: 10 (9 accepts, 1 refuse).

* False accepts: 4 of 9 -- g90 (level), g400 (wins lower), flow184 g10 (level), flow185c g10 (worse).
  Two are "level" (harmless but they move the bar and burn a judge slot); two are real regressions.
* False refuses: 1 of 1 (g170; plus flow168's, off this arm). Under leg20 the refuse count is 15 of 27
  decisions on flow172, and the only refused candidate ever read locally was the best theta of its day.

Gate statistic vs judge verdict (the two "cumulative" accepts g940/g1000 are marked *, their single-step
gate deltas are not what the judge read):

| stat | judge-TRUE {g60, g170, g200, g300, g940*, g1000*} | judge-FALSE {g90, g400, flow184, flow185c} |
|---|---|---|
| net flips (games) | +9, +16, +12, +7, 0*, +4* | -2, -3, +4, +3 |
| d-margin /game (all field) | +782, +646, +922, +274, +551*, +429* | +172, +74, +59, +269 |
| leg20 family delta | +41.9k, -4.2k, +1.5k, +14.8k, +9.2k, +8.4k | +6.7k, +12.3k, -, - |
| sign-test z = net/sqrt(flips+drops) | 3.0, 4.0, 2.7, 2.1, 0, 1.4 | -0.8, -0.9, 2.0, 0.8 |

* leg20 does not separate at all (it refused the +16 step and accepted the -3 step): the currency is wrong
  (12 tapes x 2 seats = 12 boards of coins, SE ~18k on 24 games per the 09-09 note).
* d-margin separates only at a hair (+269 vs +274) -- not usable on its own at n = 84-120 games (paired
  per-game sd ~2.5k coins from the local reads => SE ~230/game at 120 games; +269 is t ~1.2).
* NET FLIPS with a threshold of >= +5 games on the 60-board field is the best single separator on this data:
  4/4 genuine single-step accepts pass (+7..+16), 0/4 false accepts pass (max +4). Equivalently a sign-test
  z >= 2 (passes 4/4 true, 1/4 false: flow184 z 2.0 exactly, a level theta on 4 games).
* Why min_flips 3 fails: on the 42-board field flow185c's step touched 13 games (8/5) -> under the null
  the net is ~ N(0, sqrt(13) ~ 3.6 games); +3 is 0.8 sd, i.e. a ~20 % false-accept per nomination. On the
  60-board field (flow184: 4/0) the same. The remote logs show 8-20 unstable games per 10-gen step on
  60 boards (~5-10 % of boards); the threshold has to scale with that.

## 3. Cost per gate evaluation (remote, 10 workers, `games in Ns` lines)

| field | games | seconds (uncontended) | seconds when the other GPU gates at the same time |
|---|---|---|---|
| 42 boards (flow185c) | 84 | 156-157 | - |
| 60 boards (flow172/183/184) | 120 | 217-224 | 348-430 |
| 83 boards (flow185b) | 166 | 304-334 | - |

=> 1.85 s/game flat (~0.19 s/game/worker). Training runs at 55-61 s/gen for the flow172/185 recipes
(flow172 g1288 55.4 s; flow185c 61 s; flow185b 55 s), so 100 gens = 92-102 min.
Budget a gate at <= 15 % of that (<= 900 s) -> <= 486 games = 243 boards uncontended; at 10 % -> 162 boards.
The remote schedule holds 331 pinned towns: LIVE62 (62/62 present), LIVE-C63 (63/63), TOPB2 (20/20),
the flow172 60-board band field (14 of which are LIVE62 ids, 0 in LIVE-C), and ~130 older family/rung ids.
So the largest OUT-OF-RUNG field available today is 46 band (flow172 field minus its 14 LIVE62 ids)
+ 62 LIVE62 + 63 LIVE-C63 + 20 TOPB2 = 191 boards = 382 games ~ 12 min (~12 % overhead) -- fits, but it
eats every local held-out set (see 4).

## 4. Recommendation for flow186

Principle from the data: (i) drop leg20; (ii) the win metric already has the right currency and the right
second clause (cand_wins > inc_wins), its only defect is the threshold at the field size; (iii) the field
must contain the BAND (flow185c's false accept was caught by LIVE62's 8 drops, which no target-band gate
plays) as well as the target tiers; (iv) keep one held-out band set for the local judge.

Field = 129 boards / 258 games (~8 min uncontended, ~8 % of a 100-gen block):
* 46 band boards = the flow172 `--real-gate-opponent` list (60 ids in `~/launch_flow172.sh`) minus the 14
  that are LIVE62 ids (`S/live62/ids.txt`) -- all already in `town_schedules.json`;
* 63 LIVE-C63 ids (`S/livec/ids.txt`, all in the schedule);
* 20 TOPB2 ids (`S/topb2/ids.txt`, all in the schedule).
* LIVE62 stays OUT of the gate = the local judge's only remaining held-out set; the LIVE-C growth beyond 63
  (69 in flight) and the next fresh top-ten cut are the held-out mid/top sets from now on. LIVE-C63 and
  TOPB2 become IN-SAMPLE for flow186 candidates and must be read as such.

Flags (everything else = `~/launch_flow185c.sh`, init flow172_g1000, seed 288):

```
--real-gate --real-gate-every 100 --real-gate-seed-base 20260904 \
--real-gate-metric win \
--real-gate-pinned artifacts/town_schedules.json --real-gate-pinned-seats 2 \
--real-gate-min-flips 10 \
--real-gate-recentre 3 --real-gate-workers 10 \
--real-gate-opponent <46 band + 63 LIVE-C63 + 20 TOPB2 = 129 main.py paths>
```
(no `--real-gate-leg-family`; `--real-gate-min-gain`/`--real-gate-paired-t`/`--real-gate-win-floor` are
inert or refused in pinned `win` mode, so do not pass them.)

Accept rule this yields: net game flips >= +10 (= 5 boards net) on 258 games AND more wins than the incumbent.
Calibration of the 10: the true single-step accepts on the 60-board field were +7..+16 games; scaled by
129/60 = 2.15 they read +15..+34 and all pass; the four false accepts scale to -4, -6, +9, +6 and all fail.
Under the null (5-10 % of boards unstable per step -> 13-26 unstable games on 258) the net sd is 3.6-5.1
games, so +10 is 2.0-2.8 sd: expected false-accept rate 0.3-2.5 % per nomination, ~0.1-0.3 false accepts
per 1,000 gens (~10-12 nominations), against the observed 4 of 9 today. Expected false refuses: the
g940/g1000-type "level" steps (net 0/+4 on 60 boards) will be refused -- they were level head-to-head
locally too, and the judge only accepted them on cumulative reads, so nothing the judge would have shipped
is lost, PROVIDED refused candidates are kept for the auto-judge: pass `--keep-candidates` (present in
`scripts/train.py`, requires `--real-gate`; verify its file naming in the stage before relying on it) --
the g170 lesson is that a refused candidate can be the best theta.

If `--keep-candidates` cannot be used, min_flips 8 (1.6-2.2 sd, ~1-5 % FA) is the loosest defensible
setting on 129 boards; never below the field's sqrt(unstable games).

## 5. What could not be determined

* No local reads exist for flow172 g500/g510/g580/g700/g740/g850 (accepted, best_abs only) or for any
  refused candidate other than g170 (refused thetas are overwritten). The false-refuse rate rests on 1 (+1
  off-arm) observation; the 15 leg20 refusals on flow172 are unread.
* The local judge compares COMPOSITIONS (candidate + TAIL_FILL/BANK pair + HIRE_ROW) against the shipped file,
  the gate compares raw thetas in the training tree (flow185b's seat 50 % vs g1000pair_hr 68 % on the same
  boards). Whether a gate-level step survives the switches is unmeasured; flow184/flow185c may partly be
  composition effects.
* The paired per-game sd on the gate field was not computed (no per-game csv was read); 2.5k coins/game is
  taken from the local reads of comparable steps.
* Whether the 46 flow172 band-field ids are among the 147 pinned training rungs of the flow185 recipe was
  not checked (the 09-10 notes say 0 of the 83 target-band boards are in a rung; nothing is said about the
  band field).
* The two Kaggle results (g940pair 64W-28L ~2545, g1000pair_hr 51W-14L ~2381 mid-ramp) differ in
  composition and ramp stage and cannot rank g940 vs g1000 -- they confirm only that both leg20 accepts
  were genuine.
* `~/launch_flow186.sh` already exists on the remote (15:05Z, metric win, 54 opponents = the 42 + the 12
  leg-family tapes, min_flips 3); it was not used for this review and, on the numbers above, 54 boards at
  min_flips 3 keeps the ~20 % per-nomination false-accept rate.
