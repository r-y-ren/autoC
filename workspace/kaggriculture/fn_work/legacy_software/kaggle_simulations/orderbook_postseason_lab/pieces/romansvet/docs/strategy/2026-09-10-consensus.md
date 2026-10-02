# Consensus table: blind second reviews of the 2026-09-10 planner-logic streams

Rule (user, 2026-09-10): every planner-logic review gets a blind independent second reviewer; nothing is acted on until the pair agrees. A = first reviewer, B = blind second reviewer.

## 1. Chain optimisation ("optimise harvesting, depositing, selling, reinvestment together")

| Question | A (`2026-09-10-chain-optimisation-review.md`) | B (`…-review-B.md`) | Agree? |
|---|---|---|---|
| Statement as written | DO NOT RUN — restatement, no falsifier | DO NOT RUN as written | yes |
| Routing evidence | doc says the route is not the wall | doc says the opposite of what it is cited for | yes |
| ES already optimises the four arms jointly | yes, 12 Macro genes | yes, 12 Macro knobs incl. hold/press → sell.allocate | yes |
| Only non-gene step | deposit turn; BANK_BEFORE_LOT fires 0.67×/game, 3.4 units | same numbers; widening it (BANK_LOT=2) loses −1,257 | yes |
| Idle workers | true, cause = cash starvation (RAMP11 −4.3k) | true as census, false as lever (HIRE_ROW −378 t −0.75) | yes |
| Early sale hits empty shed | already priced at hour 0 | 128 engine games: zero shed-starved SELL rows | yes |
| Melon displaces animals | closed nine ways | closed decisively (MELON_D10B −22.1k t −15.5) | yes |
| Tail pair as "starting point" | already measured and shipped | already shipped; still False in arms-next, flipped at package build | yes |
| Narrower experiment | none worth running (deposit-turn gene below noise) | HARVEST_FIRST_ON composed with the pair | **differs** |

**Resolution of the one difference:** B's narrower experiment was already played today in the TOPB switch screen: HARVEST_FIRST_ON on top of g1000+pair on the 20 held-out top-tier boards = −229/game (t −1.0), wins 40 → 35 % (`S/topb/screen_summary.txt`). Negative on the judge that matters; a LIVE62 read is queued only for completeness. **Consensus: DO NOT RUN.**

**Follow-up judged (10:05Z, `2026-09-10-late-sell-review.md`, worktree late-sell b7e2ae4):** LATE_SELL_FILL_ON — the plateau review's "~19 units short on the late sell rows" — built default-OFF (OFF byte-identical on 12 pinned boards, 173 targeted tests green) and judged paired on g1000+pair: TOPB +5/game with 36/40 games identical, LIVE62 head-to-head level. INERT, as the builder's own doubt predicted: the 19 units were DROP's deliberate day-29 over-ask (a projection of units that do not exist), not stranded stock; the switch frees only the d21-28 reservations the route never walks to, worth ~nothing. Closed.

## 2. Intraday market controller

| Question | A (`2026-09-10-intraday-controller-review.md`) | B (`…-review-B.md`) | Agree? |
|---|---|---|---|
| Hour-0 plan replayed all day | TRUE (runtime.py:30-34, render.py:52-60) | TRUE, same lines | yes |
| Mid-day "actual inventory" | FALSE — harvest reaches the shed at end of day | FALSE — unit inventory until eod.py:210, SELL capped by shed | yes |
| Reservations / deposits new info | already priced at hour 0 | netted into avail at dawn | yes |
| Failed purchases to react to | 0.07 % of turns, 0 BUY refusals | same numbers | yes |
| Production-timing features | hour-0 inputs, not intraday | hour-0 macro inputs, judged inert | yes |
| Archive | experiment closed in the plateau review; reactive levers all lost | ~28 levers measured, 3 won and all are hour-0 decisions; minimal mid-day revisit −4,964/game; OPP_SUPPLY −2,972/−3,616 dose-responsive | yes |
| Verdict | DO NOT RUN | DO NOT RUN as written | yes |
| Narrower experiment | flip OPEN_PUMP_TELL_KEEP0_ON | flip OPEN_PUMP_TELL_KEEP0_ON | yes |

**Resolution:** the narrower experiment both proposed was played today: OPEN_PUMP_TELL_KEEP0_ON=True on g1000+pair is byte-identical on all 124 live-board games and all 40 TOPB games (no-op). **Consensus: DO NOT RUN; the intraday family is closed.** B's tree note (arms-next ships the pair False; the pair is applied by switch in the judge and by default in ship-pair/drain-pair) matches how the legs are run.

## 3. Top-tier loss anatomy (g1000pair on TOPB)

| Question | A (`2026-09-10-topb-loss-anatomy-g1000.md`) | B (`…-B.md`, own replays) | Agree? |
|---|---|---|---|
| Replays reproduce the judge csv | 40/40 | 40/40 byte for byte | yes |
| Losses | 12 boards, median −8.8k | 12 boards, 10 structural, worst −22.1k | yes |
| d10-14 melon hole | −19.6k flat tax, bigger on wins, not the discriminator | −20k tax, same size on wins | yes |
| Discriminator | opponent's d15-29 purse (+18.8k), our late revenue level | opponent's late revenue 72.8k → 91.7k; ours identical | yes |
| Product | late WOOL +8.9k, held-back MELON +4.0k | WOOL +8.9k of 18.8k; per-product swing WOOL +6.9k, TOMATO +4.5k, EGG +3.2k | yes |
| Mechanism | denial never taken | we match wool volume and sheep count; we lose PRICE (144 vs 160/unit, sell-day 19.7 vs 18.2, 22 units before d16 vs 46) | B sharper |
| Lever | additive melon (rejected by its own spec) → late-wool contest | late-wool PRICE half: wool-first into the earliest lot when a wool sink is live; volume half closed four ways | converge on late wool |

**Consensus:** the top tier is lost in days 15-29 on the opponent's purse, chiefly late wool; the melon pot is a flat tax. Volume levers are closed; the untested half is wool sell-timing/price. **Action: build `WOOL_FIRST_LOT_ON` (default OFF, byte-identical) and judge paired on TOPB + LIVE55.**

## 4. Planner wall audit ("erroneous logic ES cannot fix")

| Finding | A (`2026-09-10-planner-wall-audit.md`) | B (`…-audit-B.md`, 2,400 real obs) | Agree? |
|---|---|---|---|
| land_bias wall | saturated at −256 on 27/30 days, all 7 thetas; quad 4 never; slope 0 after d10 | decodes to exactly −land_price on 30-71 % of days; zero-gradient half-space; veto form never A/B'd | yes (wall confirmed; A measures the bias value, B the veto-binding days) |
| compact | near wall, 7 of DIST_MAX 8, monotone up | saturated at DIST_MAX 100 % of days for g300/g940/g1000 | yes |
| GROW_MAX | wool touches the 4× cap on 2-5 days only → no wall | on the rail for SOME product 52-55 % of days; purse cannot rank two strong products | **differs in scope** (A checked wool only) |
| melon plant_target | — | 0 in 16,800/16,800 decisions; blocker = proportional mix over clipped scores, not the drain gate | B only |
| animal_defer | inert by design | dead gene | yes |
| hire_bias | monotone down, 84 % of bound, watch | never within 5 % of bound | yes (not a wall) |
| Largest unmeasured constant | cash_reserve = HIRE_BILLS[n_hire+1] | cash_reserve first, then HIRE_BIAS_MAX/CREW_TARGET_PUSH, GROW_MAX, LAND_OWN_DEN | yes |

**Consensus actions:** (1) land veto — build in flight (worktree land-veto), judge paired; (2) cash_reserve scale — build queued; (3) GROW_MAX — cheap inference screen via `brain.GROW_MAX=6/8` overrides on g1000pair (TOPB then LIVE62), no build needed; (4) compact / plant_floor gene — training-arm changes, after the inference reads.

**Shortlist fully measured (12:57Z):** land veto DEAD (3 arms), cash_reserve DEAD, GROW_MAX 6/8 byte-identical (cap binds on the top-ranked product already), COMPACT_SOFT_ON inference read on g1000 padded: TOPB2 −327 (2 drops), LIVE-C22 −162 (+2/−4), LIVE62 89.1 vs 90.9 % → no compact-soft training arm. The wall audit's items are walls of the optimum, not planner defects.

## 5. Rating calibration (judge reads → ladder rating)

| Question | A (`2026-09-10-rating-calibration.md`) | B (`…-B.md`, blind, anchored on initialScore) | Agree? |
|---|---|---|---|
| Ladder slope | 0.00368/pt (625-pt scale; 9 pp per 100) | 272 pts/logit (= 0.00368/pt; 9.2 pp per 100) | yes, identical |
| flow135 crossover | 1923 (realised 1924) | 1923 (realised 1924) | yes |
| g940pair crossover | 2531 (last-20 read) / 2612 fit | 2636 fit (still rising at 2542) | fit agrees; A discounts the ramp |
| Judge offset | +97 (88-107) on both LIVE55 and LIVE-C22 | +110 LIVE55; +188 LIVE-C22 (from the cut's own 66.7 → 50 % re-basing: 272·ln 2) | same sign and order; B's LIVE-C offset is larger and structurally derived |
| TOPB2 | a lottery floor (p = 0.13 + 0.74σ), cannot resolve 150 pts | a real open-loop-tape floor (15 % where 1.9 % expected), cannot resolve 10 pp | yes |
| LIVE-C22 needed for 2960 | 82-84 % | 77 % (73-80) | overlap 80-84 %; both say ≈ +180 real points from today's 63.6 % |
| TOPB2 needed | 38-41 % | 47-60 % | disagree in level, agree it is not the instrument |
| Prediction 56143250 | 2650 ± 60 | 2730, 80 % [2620, 2860] | overlapping; both NOT top-10 |
| Falsifier | games 11-40 ≥ 85 %, ≥ 2520 at game 40 | games 29-58 72-82 %, ≥ 2480 at game 58; ≤ 18/30 breaks it | compatible |

**Consensus:** the judge reads 100-190 rating points low; the instrument for the top-10 push is LIVE-C22, target ~80 % (today 63.6 %); TOPB2 is a floor, not a gauge; the hire-row file settles ~2650-2730. B's extra point stands: the slope's own uncertainty (170-620 pts/logit) moves the LIVE-C22 target between 63 and 87 %, so games at 2500+ that narrow the slope are worth more than another judge board.

**Update C (`2026-09-10-rating-calibration-C.md`, third fit with ~150 more games, 15:05Z):** slope 298 pts/logit (95 % 182-686; per-file intercepts identify it only from within-file opponent spread, which matchmaking caps at ±150, so more games will not narrow it); g940pair crossover 2631 (2493-2775) vs realised 2536 and rising; LIVE-C63 target for 2960 ≈ 83 % live / 81 % judge-scale (67-93 %) with offset 0 (the set is the file's own unfiltered ≥2300 pool, mean opponent 2488); hr file fitted crossover 2506 (2324-2703), below g940's, and it missed both rating falsifiers (2308 at g40, 2362 at g58) while sitting at the low end of the win-rate bands → A's 2650 and B's 2730 are both tracking high. Three-way consensus: the target band on LIVE-C63 is 77-83 % live; the hr file is not a top-10 file; the ladder is now rank 10 = 2943.

## 6. flow184 plant-floor gene verdict

| Question | A (`2026-09-10-flow184-gene-check.md`) | B (`…-B.md`, blind) | Agree? |
|---|---|---|---|
| Gene alive? | yes, L2 0.197, all coords moving | yes, norm = the undirected walk's (distance proves nothing) | yes |
| Selected against? | yes, −7.6σ drift below the decode threshold | yes, melon logit z −3.64, four crops jointly 0/200,000 null draws; wheat (already planted) untouched = the control | yes |
| Population expression | melon 19 % → 0.12 % | melon 18.7 → 0.54 %, carrot/tomato/strawberry collapse 30×, wheat unchanged | yes |
| The relaunch (gb12[melon]=+0.30 + top-ten rungs at 40 %) | proposed as a re-centre alternative | UNSOUND as a search: hard-codes the corner (member spread 0.073 vs bias 0.30), moves the start not the gradient; archive predicts it is switched off again | **differs** |

**Resolution:** keep flow184b running as a deliberately short, falsifiable test of the OTHER half of the change — whether the gradient's sign flips when the top tier carries 40 % of the budget (B did not weigh that half). The +0.30 start only makes the sign observable. Falsifier: by gen 50 the mean gb12[melon] must be ≥ +0.10 and rising or the arm is killed and the melon family is closed inside the ES as well as outside it. If it holds, that is the first evidence the corner pays on any rung population.

**§6 outcome (14:25Z):** the falsifier was met at gen 1, not gen 50 — flow184b's seat (g1000 + a 2/16 melon floor) scored 10.0 %/−12,824 on its 120-game band gate against g1000's 66.7 %/+4,294, and its first candidate reached 18.3 % only by turning the floor down. B's prediction held exactly. The melon family is closed inside the ES as well as outside it; flow184b was killed and GPU0 given to a second target-band-gate seed (flow185c).

**Provenance note (audit 15:50Z):** flow184 followed the builder's launch prescription (`--train-only g12,gb12`, sigma 0.02, wd 0) with two deliberate deviations not recorded at the time: init from g1000 (the best record) rather than g300, and the default optimizer (adam) rather than its suggested `--optimizer sgd`. B's null test (signed drift, 0/200,000 draws) shows the "selected against" verdict is not an Adam-diffusion artefact, so neither deviation changes §6. The builder's other concerns were enforced (auto-judge routes 6,954-width thetas to the slope-repair tree with the floor ON; COMPACT_SOFT judged separately, 12:57Z, no arm).

## 7. LIVE-C63 loss anatomy (24 losses / 39 wins, live theta)

| Question | A (`2026-09-10-livec63-loss-anatomy.md`) | B (`…-B.md`, blind) | Agree? |
|---|---|---|---|
| Replays reproduce the csv | 126/126 | 126/126 byte-exact | yes |
| Where the split is | d15-29 only (t −8.9), 62 % our purse; d10-14 flat tax | d15-29 only (t −8.94), 62 % ours; d10-14 flat | yes, identical |
| Products that separate | WOOL (t −4.0), TOMATO (t −3.7) of 27 buckets; fert/melon level | WOOL (t −3.9), TOMATO (t −3.7); fert/melon level taxes | yes |
| Clustering | town draw (tomato sink 170 vs 270, strawberry sink); no pre-d10 predictor in OUR state | town draw (tomato sink, FARMERS_MARKET, ICE_CREAM, SMOOTHIE); the d3/d6/d9 unlock sink index predicts a loss (t −3.9) while our d10 state does not | yes (B adds the town-unlock predictor) |
| The own-purse wool bucket | PRICE at equal units after regressing out sinks (≈4.3k/board, t −2.4) | VOLUME: our sheep herd is a step function (3.7/6.6/11.2) vs their flat 6-8.6 at each YARN count; coins/unit ties (8.9k gross on YARN≥1 losses, 2-3k net) | **differs on mechanism** |
| Smallest experiment | WOOL_SPLIT_CAP (split sales across days) on the 29 thin-wool boards | SHEEP_FLOOR (≥1 YARN_STORE → sheep want ≥ 8) on LIVE-C63 + LIVE55/TOPB veto | complementary |

**Resolution:** both switches get built and judged paired on LIVE-C63 (and the shipped file's sets): the split-cap tests A's price reading, the sheep floor tests B's volume reading. Both agree the town draw dominates the losses and that fert/melon are flat taxes. If both read level, these losses are a board draw and the next target is the flat fert/hire tax.

**Judged (15:12Z):** WOOL_SPLIT_CAP=8 on the live theta, LIVE-C72: 63.2 → 52.1 %, −2,780/game t −3.8, 0 flips / 16 drops (ours −857, theirs +1,923) — A's price reading DEAD in the engine, displacement signature; its hr legs were cancelled; the builder's report shows cap 8 sits below the late herd rate (shed overflow then dumps 41-unit lots), so cap 12 is queued as the fair test of A's reading. SHEEP_FLOOR=8 binds only d0-11 on this theta (16 sheep from d15 already) — an early-ramp test, not B's late-volume reading. SHEEP_FLOOR=8 judged 15:22Z on the live theta, LIVE-C72: 63.2 → 61.1 %, −381 t −1.1, 3 flips / 6 drops, 52/72 identical — DEAD; it binds only d0-11 here, so B's late-volume reading stays untested by a herd floor (the live theta already holds 16 sheep from d15). Cap 12 judged 15:35Z: 63.2 → 56.2 %, −1,684 t −3.5, 0 flips / 10 drops, dose-responsive with cap 8 — A's price reading refuted in the engine. **WOOL FAMILY CLOSED** (five switches: turn, hold, split cap 8/12, sheep floor; every one a displacement loss). What remains of the LIVE-C loss anatomy is the town draw itself, which neither seat controls.

## 8. Hire row on the hr file's own boards (LIVE-D, 12 boards, base = hr composition, 15:06Z)

Single-stream paired read, no reviewer pair (a judge leg, not a planner-logic claim): HIRE_ROW removed = 83.3 → 83.3 %, −664/board, t −3.9, 12/12 boards negative; g940 theta under the hire row = −82, t −0.2 (level). Third independent set confirming HIRE_ROW_ON (LIVE62 +453 t 3.6, LIVE-C63 +990 t 5.0, LIVE-D +664 t 3.9); theta g940 vs g1000 is level on every set.

## 9. Remote real-gate design (why the gate false-accepts) — A + B blind, landed 15:25Z

| Question | A (`2026-09-10-gate-design-A.md`) | B (`…-B.md`, blind) | Agree? |
|---|---|---|---|
| Decisions with a local read | 7: leg20 4/4 true accepts (g60/g300/g940/g1000), g170 refusal level; win-metric 2/3 false (flow184 g10, flow185c g10) | 10: 9 accepts, 1 refuse; false accepts 4/9 (g90, g400, flow184 g10, flow185c g10); false refuse g170 (+16/−0, best local read of its day) | overlap on the two win-metric false accepts; B counts two more leg20 accepts as false |
| Why `min_flips 3` fails | rule is flips−drops ≥ 3 AND cand wins > inc wins, no margin term; at 2 seats 3 flips = 1.5 boards | a 10-gen step touches 8-20 games, +3 net ≈ 0.8 sd → ~20 % false-accept per nomination | yes |
| Separating statistic | paired margin delta per game (confirmed +274…+782 vs +59/+269), threshold +330-400/game; net flips does NOT separate (g940 had 0) | net game flips ≥ +5 on a 60-board field (true +7…+16, false −3…+4); margin delta separates by a hair only | DISAGREE on the statistic; both thresholds refuse all historical false accepts |
| Cost | 1.85 s/game, 100 gens ≈ 95 min, ≤255 boards at 2 seats | 1.85 s/game, 100 gens ≈ 95 min, ≤243 boards | yes |
| Field | LIVE55 + LIVE-C63 + TOPB2 = 138 at 1 seat | 46 band (flow172 field minus 14 LIVE62 ids) + LIVE-C63 + TOPB2 = 129 at 2 seats; LIVE62 stays held out for the judge | B keeps the local band judge uncontaminated |
| Flags | `--real-gate-metric margin --real-gate-min-gain 400 --real-gate-win-floor 0 --real-gate-min-flips 0 --real-gate-pinned-seats 1` | `--real-gate-metric win --real-gate-min-flips 10 --real-gate-pinned-seats 2`, `--keep-candidates` | paired-t inert in pinned mode (both) |
| Tree | stage flow186 in the pair + HIRE_ROW tree: the gate plays the RAW theta while the judge and the shipped file carry the switches (flow185c g10 +269/game raw, −1,090 with switches on the same TOPB2 boards) | gate/judge composition mismatch listed as unresolved | A's point adopted |

**Resolution (15:30Z):** flow186 = B's field and rule (LIVE62 must stay held out; 129 boards / 258 games, ~8 min per gate, min_flips 10 at 2 seats, `--keep-candidates` if the flag exists) staged in a pair + HIRE_ROW tree (A's point). A's margin rule is kept as the local judge's own bar (win rate first, then margin), not as the remote gate, because the remote's `min_gain` only works in margin mode and B showed margin separates poorly on the gate field. Unresolvable from the data: the false-refuse rate (refused thetas are never saved) — `--keep-candidates` fixes that going forward.

**Staged (15:20Z):** `~/stage_hr` (stage_leg20 trainer + ship-pair-hr planner defaults, all four switches True) and `~/launch_flow186.sh` v3. The staging found all 46 of B's band ids inside flow185c's 147 training rungs, so the band third was dropped: field = LIVE-C 1-63 + TOPB2 (83 held-out boards), `--real-gate-min-flips 7`, `--keep-candidates` (saves every nomination, closing the false-refuse blind spot). Not launched; queued for the first idle GPU or third refusal.

## 10. ES progress rate and the flow187 recipe — A + B blind, landed 15:40Z

| Question | A (`2026-09-10-es-rate-A.md`) | B (`…-B.md`, blind) | Agree? |
|---|---|---|---|
| Throughput | 55.4 s/gen, 61 gens/h, pinned rungs 95 % of wall clock, gate ≈ 0 % GPU | 55.5 s/gen, 65 gens/h, 92 % of episodes pinned, JIT 25 min/launch, gate 0 % | yes |
| Local-judge rate | +2,800/100 gens (g0-60), ≈ +440 (g60-940), level g940-1000, 0 after g1000 (4 arms, 482 gens, 0 accepts) | +800 (g60-300), +371 (g300-940), level, 0 after (357 gens, 0 records) | yes: decelerating, dead after g1000 |
| Why it stalled | transfer stall: in-sim win still rising, refused candidates −18…−69k on the gate | overfit to the 147 fixed boards: in-sim record at g1110, every engine read negative | same phenomenon, two names |
| Is sigma/pop/E binding | no (Spearman 0.96) | no (0.93-0.96); 0.03/0.04 walked or collapsed in flow152/flow2 | yes |
| Optimiser | Adam moves the centre one sigma per ~30 gens | displacement = lr·√G exactly → diffusion; ‖θ‖ 15.8 → 18.5 at wd 0 = the gene walls | B adds the norm-inflation mechanism |
| Restart / recentre | 1500 never fired → 150-200 | never fired; the 3-refusal recentre never fired either → ≈150 | yes |
| Remedy | change the objective: LIVE-C63 + TOPB2 into training, fresh 20-40 cut held out, ≤300-gen arms | rotate the pinned draw every ~200 gens; hold the norm (wd 1e-4 or SGD) | compatible, both adopted |
| Projection to 09-23 | current 0…+1 pt; proposed +7…+20 LIVE-C pts | current 0; proposed 0…+10 pts | both: current recipe is dead |

**Resolution:** flow187 = flow186 tree and gate rule, with (1) the objective moved to the target band (LIVE-C 1-63 + TOPB2 as pinned training rungs — this is also rung-strength B's proposal; awaiting rung-strength A), (2) the gate on the 21 fresh held-out boards (LIVE-C 64-72 + LIVE-D 1-12, being synced) plus whatever fresh cut lands, (3) `--restart-sigma-on-stall 150`, (4) weight decay 1e-4 (B's equilibrium value; A silent, not opposed), (5) sigma 0.02 / pop 512 / E 160 / lr 0.003 unchanged, (6) short arms: judge at ≤300 gens and re-cut. Flag check (15:45Z, `train.py --help` in ~/stage_hr): `--weight-decay`, `--optimizer {adam,sgd}`, `--restart-sigma-on-stall`, `--stall-sigma-mult` all exist; there is NO periodic board-refresh flag — the only rotation available is dropping `--pinned-fixed-seed` (per-generation seed draw on the pinned rungs, which trades away the CRN reproducibility that gives Spearman 0.96). Decision: keep `--pinned-fixed-seed`; the rotation is the re-cut between short arms (A's remedy).

## 11. Training-population strength (is the ES trained on the opponents we lose to?) — A + B blind, landed 15:55Z

| Question | A (`2026-09-10-rung-strength-A.md`) | B (`…-B.md`, blind) | Agree? |
|---|---|---|---|
| Weight → exposure | pinned-once: 1 episode per rung per gen; weight scales fitness only, share = 2w/929 | same: episode share = rungs/160, gradient share = Σw/458 | yes, identical mechanics |
| Target band (2300-2700) in training | 1 rung, 0.4 % of the objective | 1 rung, 0.6 % of episodes / 0.4 % of gradient | yes |
| Where the live losses are | LIVE-C72: 36/36 boards in 2300-2500 / 2500-2700 (66.7 % / 58.3 %) | 72/94 games and 27/27 losses in 2300-2700; below 2300 the file wins 20/21 | yes |
| Where the gradient goes | 46.5 % sub-2300 (beaten ~89 %), ~49 % ≥2700 | 108/147 rungs are own losses to 1628-2339 (median 1981) + 30 top-tier | yes |
| Move into training | LIVE-C 1-42 at w4; drop the 42 lowest <1900 (keep the family whole: drop 106773901 not 105400600) | LIVE-C 1-63 (w3 losses / w1 wins); drop 49 <1900 + 8 family + 6 weakest 1900-2100; top-ten 10.2 → 4 | differ in dose |
| Gate | LIVE-C 43-72 + TOPB2 = 50 boards, min_flips 4 | TOPB2 + LIVE-C 64-72 + LIVE-D 1-12 = 41 boards | differ; both keep LIVE62 held out |
| Alarm | LIVE-C 1-42 vs 43-72 divergence = overfit; LIVE62 ≥ 85 % veto | LIVE-C63 baselines become in-sample for the auto-judge | compatible |

**Resolution (flow187, 16:00Z):** A's dose (the smaller move, keeps a 30-board LIVE-C hold-out), B's held-out additions: training = current rungs − the 42 lowest <1900 (family kept whole) + LIVE-C 1-42 at w4, top-ten at 10.2; gate = LIVE-C 43-72 + LIVE-D 1-12 + TOPB2 = 62 boards / 124 games, `--real-gate-min-flips 5` (B's +5 on 60 boards), 2 seats, `--keep-candidates`; tree ~/stage_hr (shipped switch composition); §10's `--restart-sigma-on-stall 150 --stall-sigma-mult 1.0 --weight-decay 1e-4`; short arm — judge at ≤300 gens. Local judge for flow187 records: LIVE-C 43-72 only (S/livec/run_holdout.sh, seed-shifted so rows pair against the 72-board bases), LIVE-D, TOPB2, LIVE62; the 1-42 vs 43-72 divergence is the overfit alarm.


## 12. Forward-horizon planner feasibility ("can the planner be made to express the top-tier ramp?") — single read-only spike, landed 16:10Z

| Question | `2026-09-10-forward-horizon-feasibility.md` |
|---|---|
| Sites pricing against TODAY's task set | `_derive` runs 3×/day; only the hire value curve (plan.py:6028-6031, cap :6108) sees `forward`; animal wants (:4722), plant cap `n_dev` (brain.py:922), admit (:6444/:6472), route (:6490-6516, `_routes` :6939), sell (:6607) do not |
| Can the projection feed the route? | No: projected harvests/waterings are refused by the engine (`sim/units.py:180/185`) → idle hands become refused ops; only pull-forward of ops legal today is executable |
| Build size | ~180-260 lines + tests, 24-33 eng-hours; route riskiest, phases to 14-18 h without it |
| Identity trap | `k=0` does not protect the shipped theta: `forward_days` decodes mean 0.9, ceiling on ~30 % of days → needs a new zero-init gene with a measured slope, or its own switch |
| Precedent | `JOINT_PLATE` (3839aed) was this change: band6 54.2 → 1.0 %, −41.9k, t −27; hands-only `FORWARD_ADMIT_ON` 94.4 → 65.3 % (d-ours −13,157); `+MELON_OPEN` 15.3 % (d-theirs +6,806); idle hands worth −378 (t −0.75) |
| **Verdict** | **Do not build**: P(≥ +5 LIVE-C points) ≈ 10-15 % |
| Alternative | pumper-aware hour-0 row / sweep of `OPEN_PUMP_UNITS/KEEP/MIN_MONEY` (53/5/1584, never swept); 0.5-1 day; accept on TOPB2 and LIVE-C ≥ +3 points each, kill on any positive d-theirs |
| Dead ends | forward-value observation feature already trained (theta[6405:6789] L2 2.25); melon-seed pump dead (`CROP_SEED_COST` constant) |

**Consensus action:** planner-ramp rewrite CLOSED as a campaign item (structural, low odds, 3+ days). The ES-side hypothesis (target-band objective, flow187) remains the live one with the ≥ +5 LIVE-C hold-out stop rule. Next inference stream: the OPEN_PUMP constant sweep on the shipped composition.

**Blind second opinion (`2026-09-10-planner-ceiling-B.md`, behavioural/reachability angle, landed 16:30Z):**

| Question | A (forward-horizon design) | B (reachability, blind) | Agree? |
|---|---|---|---|
| Is the planner the ceiling? | ramp inexpressible via projected tasks; do not build | 5 of 6 coin-carrying classes reachable under some theta; melon reached from theta alone (`ds[1,0]=−3`: 8 melon tiles d10, 23 by d16) → wall-audit-B's "plant_target 0/16,800" describes the incumbent theta, not the envelope | differ on mechanism, agree on the number |
| Forced opening 94→26 % | structural | a bad trade, not inexpressibility: melon-in-theta on the probe board 50.7k vs 109.1k (base 81.0k vs 75.9k); FORWARD_ADMIT built and lost; g11 decodes forward_days 0 | yes (both: do not chase the opening) |
| By-construction walls | route cannot place projected ops (engine-refused) | sell row count (`SELL_TURNS=(3,10,18)`, `N_LOTS=3`, lots head dead-masked; top files 389 rows × 3.95 u vs our 152 × 9.39 u) and the herd buy hour (`FULL_MARKET_TURNS=3`) | complementary |
| Not walls | — | crew ceiling (forced 16 hands: −24k, 30 empty tiles d10), land rail (coins not there), d10 melon pot (flat tax, we still win the probe board 81.0k–75.9k) | — |
| P(theta in the current planner reaches LIVE-C ≈ 80 %) | ~10-15 % for the build | 10-15 % | **yes** |
| Best single change | OPEN_PUMP constants (sweep running: UNITS 40/70, KEEP 0 all level or worse) | `LOT_SLICE`: split each row's lot into ≤S-unit sub-orders, same row | — |

**Engine check on LOT_SLICE (16:35Z, `sim/market.py:84 sell_walk`):** a SELL order of n units is paid `cumsum(quotes(inv))[n]` and advances inventory by the units sold, so two sub-orders in the same turn walk the same curve as one order — **slicing within a row is inert by construction**. The top tier's 3.95-unit rows earn their price from being spread over 7-9 hours (restock every 4 steps), i.e. the ROW COUNT, which B correctly marks unreachable by any theta. Row count was "closed" on 2026-09-09 (§10 sell cadence: SELL_CADENCE_ON N_SELL_ROWS 4/6, +0/−0, d-margin −324/−348) — but on the 42-board judge that §11 the same day found to be a 15-coin lottery (zero true positives over 7 arms), and −324 at n=84 is ~1.2 SE. **Consensus action:** re-read SELL_CADENCE_ON (6 then 4 rows) on today's judge (TOPB2 + LIVE-C72 + LIVE62, hr composition) after porting e07bb3b onto the ship-pair-hr tree; LOT_SLICE itself is not built. Planner-ramp rewrite stays CLOSED.

**Sell-cadence re-read on today's judge (17:35Z, worktree `sell-cadence-hr` c366a31, identity exact):** N_SELL_ROWS 6 → LIVE-C72 68.1→63.9 % (+2/−8, −447, t −5.9), LIVE62 88.7→85.5 % (0/−4, +7), TOPB2 level (−118); N_SELL_ROWS 4 identical to the coin; diagnostic layout 5 (lots 1+2 split, lot 3 whole) exactly level. The entire loss is the one row behind the DROP (turn 21), and it is the two-purse signature (d-theirs +554 on 134/144 rows). **Verdict: the 3-row sell schedule is a wall of the optimum, not a defect; sell-hour levers closed on a real judge.** With this, every item from the planner-ceiling question (A, B, wall audits, pump constants) is measured: no planner change on file moves the target band; the ES objective (flow187, launched 17:31Z) is the live hypothesis.

## 13. Board-schedule determinism (H2, single agent, landed 18:12Z) — `2026-09-10-board-schedule-losses.md`

| Question | Finding |
|---|---|
| Is the outcome board-determined? | Yes: 61/72 boards coin-identical across seats, 0 winner flips; margin sd 8,155 |
| Does the schedule classify W/L? | **No** (max \|t\| 2.42, family-wise p 0.43; LOO below the always-W baseline) |
| Does it move the margin? | Yes: `straw_share` r −0.51 (p 0.003), ≈ ±4.8k; top coins: n_single_shops +5.5k, dem_STRAWBERRY −4.5k, nshop_CARROT +4.3k, demrate_d10_WOOL +4.2k |
| Opponent strength? | Not the axis (L 2,501 vs W 2,488; rating-only LOO R² −0.015) |
| Who adapts to the shops? | **We do; the band clone does not** (fixed plant book on 67/72 tapes, 12 melon d0 72/72, 0 tomato 72/72; its one reaction is wool-sink → sheep) |
| Where do we lose on strawberry towns? | We win strawberry (+8.8…+17.1k) and lose WOOL (−3.8…−18.5k) and FERTILIZER (−8.5…−11.2k) |
| Lever | `LATE_STRAW_CAP_ON` (plan.py:1438): byte-level no-op at DAY 15 on both screens → read DAY 8 / 11 on LIVE-C72, split by straw_share |

**Consensus action:** H2 falsified as a classifier; the "clone is shop-adaptive" premise in the 09-08/09-09 notes is wrong for the band clone. Straw-cap day read running (S/strawcap/).

## 14. Verification of `docs/2026-09-10-planner-findings.md` (six independent verifiers, one per finding)

| # | Finding | Verdict | Key fact | Could it move LIVE-C? |
|---|---|---|---|---|
| F1 | Land price missing from the utility comparison | **PARTLY** (`verify-F1-land-price.md`) | literally true at bias 0, but the `land_bias` gene charges the price by design and the trained theta decodes −1000 on the probe state (no buy); loosening arms all DEAD | no (fix is a no-op by construction) |

**Straw-cap read (18:15Z, `S/strawcap/`):** LATE_STRAW_CAP_DAY 8 → LIVE-C 68.1→50.7 % (−3,511, t −7.3; d-theirs +3,869); DAY 11 → 61.1 % (−670, t −2.5; d-theirs +802); DAY 15 no-op. Dose-responsive denial hand-back → **strawberry-cap family CLOSED**. §13 leaves no lever: the schedule moves the margin, but every way of not contesting the crop pays the clone more than it saves us.
| F2 | Admitted essential work can remain unexecuted | **CONFIRMED as code / REFUTED as lever** (`verify-F2-admitted-unexecuted.md`) | probe exact; in trained play 0/2,240 survival waterings unemitted, 4/5,060 mandatory ops unemitted, all on day 29, ≈ 99 planner coins/game (0.13 %) | no (already reviewed 09-08: oracle +429 vs 1,500 bar) |
| F6 | Purchases finalized against queued work, 1,180 excess seed coins | **PARTLY** (`verify-F6-purchase-reconcile.md`) | mechanism and counts exact; 96.6 % of the "excess" is planted within 2 days; 1,080 of 1,180 coins is one board counted twice (seat 0 ≡ seat 1); shipped composition: 99.1 % of seed planted, ≈ 20 dead coins/game; seeds never touch the shed | no (1/70 of the judge SE; ours ≤ +20, theirs 0) |
| F5 | No cash-retention alternative in purchase allocation | **PARTLY** (`verify-F5-cash-retention.md`) | true for the five seed lists only (fert/animals/land gate on cost); probes reproduce but are contract tests; trained play: 1.2 % of granted units below cost, 361 coins/game ceiling, purse binds on 8/120 days | no (every hold-cash lever measured and dead) |
| F4 | Forecast work buys idle temporary workers | **CONFIRMED as code / IMPLICATION REFUTED** (`verify-F4-idle-workers.md`) | probe exact; trained theta hires 0 on it; shipped tree (HIRE_ROW_ON) has 0.00 idle hand-days/game; horizon 0 costs −13k own coins per board, horizon 3 loses too → interior optimum | no (both endpoints lose; g11 already holds the optimum) |
| F3 | Route repair reduces its own task-value objective | **PARTLY / CONFIRMED-immaterial / PARTLY** (`verify-F3-route-repair.md`) | the loop optimises feasibility (n_admit only falls), not value; 11/120 exact but 3-148 planner coins per plan; the −612.5 intervention read was n=3 distinct games (0.6-1.0 SE) — re-measured paired on 12 boards: Δ −10, t −0.07, inert | no (family closed 09-08: shrink earns +2,224; oracle +429 vs 1,500 bar) |

**Conclusion (18:45Z):** all six findings describe real properties of the code and every probe reproduces to the coin, but none survives contact with the trained policy or the paired judge: the trained theta already compensates (F1, F4), the incidence in trained play is ~0.1-0.4 % of final coins (F2, F5, F6) or inert (F3), and every implied fix that has a direction was measured before and lost or read level. Two methodological corrections propagate: (1) probes at zero bias measure the initialisation, not the shipped policy — evaluate under the trained decode; (2) under pinned towns most boards are seat-identical, so n is boards, not games (S/bank/paired.py already reports t on boards). No planner change from this review is queued; the ES objective (flow187/188/189) remains the live hypothesis.

## 15. Gate false-refuse tally (H4) — refused candidates judged locally

| Candidate | Remote gate (124 games, min_flips 5) | Local TOPB2 | Local LIVE-C hold-out 43-72 | Local LIVE62 | Verdict |
|---|---|---|---|---|---|
| flow187 g70 | 69→71, net +2 → refuse | 25→30 % (+740, t 1.5) | 63.3→60.0 % (+4/−6, −325, t −0.5) | 88.7→87.1 % (+231) | refusal correct |
| flow187 g160 | 69→71, net +2 → refuse (margin +2692, arm best) | 25→25 % (+610, t 1.3) | 63.3→66.7 % (+6/−4, +218, t 0.4) | 88.7→90.3 % (+4/−2, +614, t 2.0) | **PASSED 00:37Z on the 60-board rule**: fresh 73-102 70→80 % (+6/−0), pooled hold-out +6.7 pts (+12/−4); vs live g940_pair LIVE62 +12/−0 t 4.3 → packaged `submission_flow187_g160_hr.tar.gz` md5 3ec658f2, smoke 124/124, handed to the user 00:57Z |
| flow187 g10 | 69→67, net −2 → refuse | 25→25 % (−620, t −1.0) | 63.3→60.0 % (+4/−6, −269) | 88.7→83.9 % (0/−6, +266) | refusal correct |
| flow188 g10 | 69→67, net −2 → refuse | 25→25 % (−141) | 63.3→60.0 % (+4/−6, −600, t −1.2) | 88.7→86.3 % (+4/−7, −337) | refusal correct |
| flow188 g20 | 69→68, net −1 → refuse | 25→30 % (−38) | 63.3→60.0 % (+2/−4, −163) | 88.7→87.9 % (+4/−5, −62) | refusal correct |
| flow188 g60 | 69→65, net −4 → refuse | 25→25 % (−607, t −1.3) | 63.3→58.3 % (+2/−5, +96) | 88.7→82.3 % (+2/−10, −37) | refusal correct |
| flow190 g10 (lr 0.001) | refused | 25→25 % (−1083, t −1.7) | 63.3→60.0 % (+2/−4, −187) | 88.7→88.7 % (+4/−4, +194) | level-to-down; too early for the lr A/B |
| flow189f g10 (local, lr 0.001) | local gate | 25→25 % (−477, t −1.1) | 63.3→60.0 % (+2/−4, −68) | 88.7→87.1 % (+2/−4, +170) | level-to-down; too early for the lr A/B |
| flow190 g50 (lr 0.001) | refused | 25→30 % (−749) | 63.3→58.3 % (+2/−5, −13) | 88.7→87.1 % (+4/−6, −107) | level-to-down |
| flow191 g10 (g940 init, lr 0.001) | vs own g940 seat | 25→25 % (−293) | 63.3→60.0 % (+2/−4, −608) | 88.7→82.3 % (+2/−10, −655) | below the g1000 base as expected at g10; read at g100/g200 |
| flow191 g20 (g940 init, lr 0.001) | vs own g940 seat | 25→25 % (−705) | 63.3→58.3 % (+2/−5, −60) | 88.7→90.3 % (+6/−4, +358, t 1.5) | LIVE62 recovered from −10 boards (g10) to +2; hold-out still down |
| flow190 g150 (lr 0.001) | refused | 25→20 % (−261) | 43-72 ≈ +2/−6; 73-102 70→76.7 % (+4/−0) | 88.7→83.9 % (+4/−10) | level-to-down; lr 0.001 from g1000 no better than lr 0.003 |
| flow187 g200p / g300p / g313 (checkpoints after the g160 pass) | — | 30 / 30 / 25 % | 43-72: 60.0 / 61.7 / 58.3 %; 73-102: 70 / 70 / 66.7 % | 83.9 / 83.9 / 83.9 % | the arm walked off its g160 peak within 40 gens (review B's diffusion) → not resumed; flow193 re-seeded from g160 |
| flow193 g10 (g160 seed, lr 0.003) | vs g160 seat | 25→30 % | 43-72 56.7 % (+4/−8); 73-102 76.7 % (+6/−2) → pooled level | 88.7 % (+4/−4) | level; seat read 44/60 pooled → −4 boards in 10 gens |
| flow194 g10 (local, g160 seed, lr 0.003) | vs g160 seat | 25→25 % | 43-72 65.0 % (+4/−3); 73-102 70 % (+2/−2) → pooled +1 | 83.9 % (+2/−8, informational) | level on the rule's sets |
| **flow193 g100** (g160 seed + 100 gens) | net +0 → refuse (margin +3028) | **25→32.5 % (+3/−0, +903)** | 43-72 63.3 % (+4/−4, +772); 73-102 **83.3 % (+8/−0, +1031)** → pooled +6.7 pts | 85.5 % (+4/−8, informational) | **PASSES**; head-to-head vs g160: hold-out wins equal, TOPB2 +3, margins up → candidate B, recommended for the slot |
| flow195 g10 (g160 seed, seed 298) | net −3 | 25→22.5 % (+1/−2) | 43-72 66.7 % (+6/−4); 73-102 80 % (+6/−0) → pooled +6.7 | 87.1 % | hold-out passes, TOPB2 down 1 → not promotable; ≈ the seat |
| **flow194 g100** (local, g160 seed + 100 gens) | net +0 → refuse | 25→27.5 % (+1/−0) | 43-72 66.7 % (+6/−4); 73-102 **83.3 % (+8/−0, +1,330)** → pooled **+8.3 pts** (45/60) | 87.9 % | **PASSES**; vs B: hold-out +1, TOPB2 −2 → candidate C, B still recommended |
| flow191 g200p (g940 init, 200 gens) | — | 25 % (−989) | 43-72 63.3 % (+2/−2); 73-102 66.7 % (0/−2) → pooled −1 | 82.3 % (+2/−10) | climbed from the g940 level back to LEVEL with g1000 = retraced the hilltop (agent's counterfactual confirmed) |
| flow196 g10 (candidate-B seed +10 gens) | logger | 27.5 % (+2/−1 vs hr; **vs B +0/−2, −1,414 t −1.44**) | 43-72 63.3 % (+4/−4; vs B 0/0); 73-102 76.7 % (+4/−0; **vs B +0/−4**) → vs hr pooled +4, vs B pooled −4 | 85.5 % (+4/−8; vs B +4/−4) | BELOW B on every leg (first read against the live theta B; flow196 loss 1) |
| flow196 g60 (candidate-B seed +60 gens) | logger | 30.0 % (+2/−0 vs hr; **vs B +0/−1, −1,087**) | 43-72 66.7 % (+6/−4; vs B +2/−0 but −638/game); 73-102 73.3 % (+4/−2; **vs B +0/−6**) → vs B pooled −4 | 85.5 % (vs B +4/−4, −325) | BELOW B (loss 2) |
| flow197 g10 (rotation arm, B seed +10 gens) | logger | 27.5 % (+1/−0 vs hr; vs B: TOPB2 ALL 40 32.5% 27.5% -1643 3503 -2.19 -949 694 0 2 0 20 -2.97) | 43-72 66.7 % (+6/−4; vs B +2/−0 but −563/game); 73-102 73.3 % (+4/−2; **vs B +0/−6, −1,062**) | 83.9 % (vs B +4/−6, −1,108) | BELOW B; opponent +1k/game on every leg (loss 1) |

**Tally 21:58Z (backfill complete): 6 refusals correct, 0 false refusals, 1 level-to-up record (flow187 g160) below the +5 rule.** Hold-out base (shipped file, 30 boards) = 63.3 %; the flow187/188/189 stop rule (≥ +5 points) is read against it. Bug fixed 19:20Z: `S/livec/run_holdout.sh` passed `--out`; the evaluator takes `--csv`, so no hold-out leg had run before this read.
## 16. Population size vs gradient reproducibility (user: "why not run the test?") — `2026-09-10-pop-spearman.md`, landed 20:35Z

| P | Spearman (2 seeds) | cosine | half-split | ‖g‖ | s/draw | linear-fitness ceiling P/(P+2n) |
|---|---|---|---|---|---|---|
| 64 | −0.028 | −0.022 | 0.006 | 127 | 24 | 0.005 |
| 128 | −0.019 | −0.016 | 0.002 | 81 | 41 | 0.011 |
| 256 | −0.004 | −0.001 | 0.011 | 55 | 81 | 0.021 |
| 512 | +0.003 | 0.000 | 0.025 | 41 | 163 | 0.041 |
| 1024 | +0.008 | +0.009 | 0.017 | 29 | 328 | 0.079 |
| 2048 | +0.015 | +0.026 | 0.032 | 19 | 654 | 0.146 |

Null sd 0.013. ‖g‖ ∝ P^−0.50 (the scaling of a zero-mean sum). **The on-file 0.93-0.96 "half-split Spearman" varied episodes with eps fixed — under pinned-once that is ≈ 1 by construction and says nothing about the estimator; retired.** Agent's reading: the cosine is monotone in P and first clears the null at 2048 (2.0 sd); fit cos = P/(P+c) with c ≈ 76-108k → Spearman 0.9 at P ≈ 0.7 M. The curve runs ~5× below the linear-fitness ceiling, so non-linearity at sigma 0.02 is a second wall beside dimension. Pop is not the lever.

**Blind review B (landed 2026-09-10 21:05Z, `2026-09-10-pop-spearman-B.md`, `S/popcurve/B/`).** A's numbers reproduce (‖g‖ to 0.05 %) but the two-seed cosine is the wrong instrument: E[g] ∝ μ at any noise level (Stein), so ρ ≈ 0 bounds one draw's SNR, not progress, and rank normalisation makes ‖g‖(P) blind to ‖μ‖. **Decisive one-step test** (22 batch evaluations on the remote with the arm's own trainer; P = 512, two seeds; step ‖d‖ = 0.2323 = one Adam generation; 8 random ± pairs as controls; in-sample = the 159-episode batch, held-out = LIVE-C 43-72 both seats, 0/30 training overlap):

| | F(centre) | 16 random steps | ES 9001 +d / −d | ES 9002 +d / −d |
|---|---|---|---|---|
| in-sample win | 0.610 | **−0.023** (sd 0.011) | −0.039 / −0.051 | −0.042 / −0.038 |
| held-out win | 0.667 | **−0.071** (sd 0.035) | −0.033 / −0.083 | −0.067 / −0.067 |

Every direction loses; +d and −d both lose (curvature-dominated, predicted by corr(a⁺,a⁻) = +0.385). The ES step is no better than random in-sample (19 %/38 % percentile; its curvature part is *worse*, z −3.0/−1.1) and marginally better held-out (69 %/62 %) while still a net loss. Alignment κ = +0.004 ± 0.009 in-sample, +0.011 ± 0.009 held-out (κ ≥ 0.031 excluded). Yet |∇F|·‖d‖ = 0.53 / 1.16: the objective is steep and the estimate finds ~1 % of it. flow172_g1000 is a sharp local maximum of the flow187 objective even on held-out boards. The |g|-ranked `--train-only` subspace is selection on noise (measured: no concentration at any scale). **Decision (21:15Z): lr 0.003 → 0.001** — net gain per step h(κ|∇F| − Ch) peaks at h* = 0.024-0.083, i.e. lr 0.0003-0.0011; 0.003 is justified only at κ's 95 % upper bound. Implemented as **flow190** (flow188 verbatim, lr 0.001, seed 292; flow188 stopped on its third straight refusal), with flow187 (lr 0.003) kept as the control. **Hypothesis under test:** `--margin-scale 3000` saturates the sigmoid past ±9k → the objective is the win bit; the raw-coin antisymmetric signal was the only 4/4-consistent one → margin_scale A/B on the same 22-evaluation rig (agent, 21:25Z) before any further arm. **Result (21:52Z, `2026-09-11-margin-scale-AB.md`): saturation is real (28 % of member-episodes past ±9k at 3000; 0.2 % at 30k) but re-shaping the same rollouts leaves the ES direction (cos 0.84-0.91) and κ unchanged — obj κ held-out +0.009 / +0.014 / +0.001 / +0.004 for 3000 / 30k / 100k / linear, se 0.009; coin κ flat 0.010-0.016 in 8/8 cells. Not a lever; no change for flow191+.** **Sigma A/B (22:22Z, `2026-09-11-sigma-AB.md`): σ 0.01/0.02/0.04/0.08 — held-out κ +0.012/+0.008/−0.002/−0.005, every +d step loses held-out win rate; σ 0.01's in-sample antisym (z 4-5) is the −d side losing, not the +d side gaining; keep 0.02.**

## 17. Assumption inventory (user question, 20:50Z) — what is load-bearing but unmeasured

| # | Assumption | Status | Measurement |
|---|---|---|---|
| 1 | The ES step makes progress at the current centre | **MEASURED 21:05Z: it does not at g1000; §20: it DOES at g940 (κ 0.040, +d beats 16/16 randoms held-out)** — one Adam generation loses in every direction (random −2.3 / −7.1 pts, ES step no better in-sample, marginally better held-out); κ ≤ 0.03 | §16 (review B) |
| 2 | sigma 0.02 / lr 0.003 / Adam are right | **lr PRICED 21:05Z: 0.003 is 3-10× past the optimum** (h* 0.024-0.083 → lr 0.0003-0.0011) → flow190 at lr 0.001 vs flow187 control; sigma/optimizer still by argument | margin_scale A/B 21:52Z and sigma A/B 22:22Z (`2026-09-11-sigma-AB.md`) both NOT levers: κ flat across margin_scale 3000-linear and σ 0.01-0.08 (held-out |z| ≤ 1.45, all +d steps lose); ‖g‖·σ scale-free; direction = lottery at every σ. **Row closed: lr is the only priced lever; pop/margin_scale/sigma measured non-levers at this centre.** **lr A/B CLOSED 01:55Z: lr 0.001 gave no record ≥ base in 210 (flow190) + 118 (flow189f) gens; lr 0.003 gave the passing g160 → keep 0.003 (B's pricing assumed a fixed κ; the arm's gains come from gate-filtered draws, which favour larger steps).** |
| 3 | The in-sim abs probe (64 seed pairs) selects real records | known to diverge from engine reads after g1000; hit rate unmeasured | from logs: abs value of every record vs its gate/judge outcome (running) |
| 4 | Stop rule "+5 hold-out points" has power | 30 boards, seats identical → +5 pts = 1.5 boards; level candidates scatter ±1.5 pts on 72 boards | **rule widened to three held-out sets** (LIVE-C 1-42 are training rungs for flow187/188/189, so the 72-board read is in-sample): require hold-out 43-72 ≥ +5 points AND LIVE62 (62 boards, 124 games) win rate ≥ base AND TOPB2 not down — 112 independent boards instead of 30 **00:50Z: LIVE-C extended to 102 boards (`2026-09-11-livec-extension.md`, 30 fresh coin-exact tapes of the live entry's latest games, base 70.0 % / +5,694 on 73-102); the auto-judge runs a fourth leg LIVEC-H30B; the hold-out line is 60 boards / 120 games and the rule reads the pooled 43-102.** **02:25Z RULE RESTATED after §24: promotion = pooled hold-out 43-102 ≥ +5 pts AND TOPB2 not down; LIVE62 is informational only (tuning set of the shipped lineage).** |
| 5 | Gate calibration (min_flips 5 / 124 games) | false-accept ≈ 20 % from 9 decisions at min_flips 3; false-refuse 0/1 | from logs + bootstrap of the flip count under the null (running) |
| 6 | Judge→ladder slope holds above 2700 | 298 pts/logit, CI 182-686, fitted on 2300-2600 games | needs ladder games at 2700+ (only the entry itself can supply them) |
| 7 | Generality matters on this ladder | principle; the matched pool is one clone family | untested; a family-specialist read vs the ladder would settle it |
| 8 | A rate exists that reaches +19 LIVE-C points by 09-23 | last measured +2 pts/100 gens, then 0 | follows from 1-3 |

Measured and trusted: sim = engine on pinned towns (99.5 %, coin-exact), tape fidelity, two-purse signatures, board-determined outcomes, band clone fixed-book, every planner closure (paired engine reads).

## 18. Record selector and gate calibration — `2026-09-10-record-gate-calibration.md` (53 decisions), landed 20:55Z

| Question | Finding |
|---|---|
| Does the in-sim abs probe pick real records? | No size signal (Δabs_score vs gate net: Pearson −0.02, n 25); weak sign signal (64 % net>0 vs 44 % null); 0/4 on today's judge; abs_score rises monotonically after g1000 while gate margin falls (overfit signature) |
| Gate at min_flips 5 / 124 games | 124 games ≈ 62 boards (89.6 % of changes move both seats); P(false accept) 16.7 %; 5 % needs net ≥ 9; power 50 % at +4.8 pts, 80 % at +8.1 pts |
| The three false accepts today | net +3/+3/+4 — all inside the null |
| The shipped theta (flow172 g940) | net **+0** on a flips read; its gain was margin. A flips gate would have refused it |

**Decision:** the remote gate becomes a logger; every record (accepted or refused, saved under `cands/`) goes through the local three-leg paired judge (TOPB2, hold-out LIVE-C, LIVE62; 224 games, margin + win rate). For flow190+: gate on 240 boards or on paired Δmargin with a t-threshold. The abs probe stays as the record trigger only because nothing cheaper exists in-sim; its weak sign signal is acknowledged.

## 19. Judge-lock deadlock and the flow188 → flow190 swap — 2026-09-10 21:10-21:25Z

* The flow187 g160 judge and both backfills blocked for 30 minutes with zero legs running. **Root cause: nested flock** — `S/gatecal/backfill.sh` wrapped `watch.sh --legs` in `( flock 9; … ) 9>judge.lock` while `--legs` takes the same lock inside, so the wrapper held the lock and its own child waited forever; the watcher's g160 judge queued behind it. (First diagnosed as a leaked 9p handle because 9p locks do not appear in `/proc/locks`; the stall recurred on an ext4 lock and cleared when the outer flock was removed.) Fixes: backfill scripts call `watch.sh --legs` directly; the lock file moved to `/root/kagg3_judge.lock` anyway; watcher restarted (pid 9123, ARMS flow187/flow188/flow190); backfill v3 running (flow187 g160 → g10 → flow188 g10/g20/g60). **Rule: never wrap a self-locking script in the same lock.**
* flow188 reached three straight gate refusals (g10 −2, g20 −1, g60 −4) → stopped at g178 under the loop rule, replaced by flow190 (lr 0.001, §16). flow187 at g182: g10 −2, g70 +2, g160 +2 (refused at min_flips 5) with margin +1948 → +2692 rising; local judge decides on g160.

## 20. Re-centre one-step test and the flow187 → flow191 swap — `2026-09-11-recentre-onestep.md`, landed 23:20Z

| centre | held-out win | in-sample κ (z) | net ES step F(+d)−F(c) in / held-out | beats randoms in / held-out | random steps losing in-sample |
|---|---|---|---|---|---|
| flow172_g400 | 50.0 % | 0.019 | +0.005 / −0.008 | — | 44 % |
| flow172_g940 | 60.0 % | **0.040 (+3.1)**; seed 9002 **0.037 (+2.9)** | **+0.0067 / +0.0043**; seed 9002 **+0.0069 / +0.0102** (pooled held-out +0.0073 ± 0.003, margin +541 ± 75) | 16/16 / 16/16 both seeds (32/32 held-out) | 94 % |
| flow172_g1000 | 66.7 % | 0.009 (+0.7) | −0.019 / −0.007 | 3/16 / 11/16 | 100 % |

|∇F|·‖d‖ is 0.4-0.6 at all three centres: the objective is as steep at g1000 as before, but the P=512 estimate stops resolving it there (curvature term 3× larger). **The no-signal finding (§16) is a property of the g1000 peak, not of the estimator; the pop / sigma / margin_scale A/Bs were measured where there was nothing to find.** **Replicated 00:35Z with seed 9002 (pooled κ +0.029 ± 0.007 held-out vs g1000 ≤ 0.014; the cross-seed cosine test has no power at κ ≈ 0.04).** Agent's recommendation: keep init g1000 (it leads g940 by 6.7 held-out points; one g940 step recovers 1.7) and change the objective field. Decision: flow187 (lr 0.003 control, g313, over budget, three refusals) was replaced on GPU1 by **flow191** = flow190 recipe from **flow172_g940** (seed 294): the empirical test of "retraces to the same hilltop" vs "a different, higher point under the target-band objective", read at its g100/g200 records against the shipped base. Next stream: an objective field where g1000 is not already a peak (weight the boards it loses). **Outcome 03:45Z: flow191's g200 checkpoint read level with the g1000 base on the hold-out and below on LIVE62/TOPB2 after 200 generations — the climb retraced to the same hilltop, as the agent predicted; no record after g20. flow191 retired at g229; GPU1 → flow195 (third g160 lottery seed).**

## 21. Lost-board objective — `2026-09-11-lost-board-objective.md`, landed 23:50Z — NEGATIVE

| step at g1000 | in-sample net (cur objective) 9001 / 9002 | held-out obj | held-out margin | held-out win | randoms beaten held-out |
|---|---|---|---|---|---|
| current objective | −0.019 / +0.001 | −0.006 / −0.012 | −219 / −447 | −3.3 / −6.7 pt | 11-12 / 9-10 of 16 |
| W_lost (lost ×4, barely ×2, won ×0.5) | −0.026 / +0.001 | **−0.034 / −0.015** | **−956 / −786** | **−6.7 / −10.0 pt** | 2 / 3-9 of 16 |

The 41 lost rungs already carry 38 % of the objective; re-weighting turns the ES direction 26° and resolves an in-sample gradient on the new field, but the step generalises worse than the current one and pays for 2-3 recovered rungs with 7-10 lost ones (random-like displacement). **flow192 not staged.** Rule going forward: a changed field means new boards, opponents or seats where g1000 is not tuned, never a re-weighting of the boards it was tuned on; any re-weighting ≤ ×2 and judged on the held-out line only.

## 22. Seat-swap objective — `2026-09-11-seat-swap-objective.md`, landed 00:45Z — NEGATIVE

The trainer already alternates the pinned seat each generation (`pinned_seats = (t + i) % 2`), so the "other seat" is the same field: g1000 loses 42 vs 41 of 147 rungs from the two phases, per-rung margins correlate 0.994 across seats, and cos(g_seat0, g_seat1) = +0.98 on both seeds. Every seat-1 / pooled step loses held-out (win −3…−10 pt, κ ≤ 0.010, 0 losses flip up). **flow192 not staged.** Together with §21: neither re-weighting nor re-seating the boards g1000 was tuned on gives the estimator a resolvable gradient; only new boards or new opponents can (the LIVE-C extension, ids 73-102, is the first such field).

## 23. Fresh-board objective — `2026-09-11-fresh-board-objective.md`, landed 01:55Z — NEGATIVE; field-change ledger closed

| field at g1000 | cos to current g | held-out 43-72 step: obj / margin / win | randoms beaten (obj / margin) |
|---|---|---|---|
| A = current 147 rungs | 1 | −0.007 / −232 / −3.3 pt | 11/16 / 12/16 |
| B = A + 30 fresh LIVE-C 73-102 at w4 | 0.983 | −0.012 / −186 / −6.7 pt | 10/16 / 12/16 |

Adding real new boards of the live band rotates the estimate 11° and leaves the step inside the curvature loss; on the fresh boards themselves the g1000 direction already generalises (both directions gain margin on won boards). **Ledger: re-weighting (§21), re-seating (§22) and fresh boards (§23) all negative → the g1000 objective is not to be changed further.** What has worked is the gate-filtered lottery at lr 0.003 from a good seat (flow187 g160 passed); the arms now run that: flow193 (GPU0) and flow194 (local) from g160, flow191 from g940. lr A/B closed against 0.001 (§17 row 2).

## 24. Ladder calibration refit — `2026-09-11-ladder-calibration.md`, landed 02:20Z

| file | games | implied strength c [95 %] | pool mean opp | current rating |
|---|---|---|---|---|
| g940_pair (56140532) | 152 | 2705 [2612, 2807] | 2497 | 2633 |
| g1000_pair_hr (56143250) | 134 | 2697 [2579, 2834] | 2351 | 2543 |
| flow187_g160_hr (candidate) | — | **≈ 2795 [2610, 3030]** predicted from the hold-out reads | — | — |

Kaggle's rating is plain Elo with K decaying to 8.9 after ~80 games, so the 91-point gap between the two live files is ramp lottery plus opponent pool, not strength. The hr file's +0.64 logit on LIVE62 never reached the ladder: **LIVE62 is a tuning set for the shipped lineage and is dropped from promotion decisions; the hold-out 43-102 and TOPB2 carry the rule.** Falsifier for the candidate: rating at g40 / g60 / g100 inside 2439-2794 / 2514-2805 / 2583-2815; above 2730 at g100 rejects "level with the live pair", below 2700 rejects "top-10 strength". Top-10 (2956) needs LIVE-C 82.8 % and TOPB2 45.5 % judge-scale; top-5 (3016) needs 85.5 % / 50.5 %. P(candidate ≥ top-10 strength) = 7 %.

## 25. Training-board rotation arm flow197 — staged 2026-09-11 07:33Z; read-out pending (paired control flow196)

**Claim under test (§10):** the ES stall on every lineage is overfit to the fixed 147 pinned boards, so a lineage re-seeded from a passing record on a re-cut band set should walk toward the hold-out instead of the memorised boards.

**Design:** launch_flow197.sh = launch_flow196.sh with exactly one change: the 42 LIVE-C 1-42 rungs (w4) are replaced by 42 fresh target-band boards (S/flow197/train_ids.txt) cut from the last five hours of live ladder games of both subs against opponents rated 2300-2700 (27 W / 15 L, opp 2426-2693, median 2571; natural mix, the 42 most recent of 69 qualifying). None of the 42 is a judge board (LIVE-C 43-102, LIVE62, TOPB2, LIVE-D untouched); ids.txt unchanged at 102. 84/84 cuts byte-exact; town_schedules 382→424 on both hosts (remote backup kept). Seed theta = candidate B flow193_g100, --seed 300, GPU1. **Paired control = flow196** (same seed theta, same recipe, the old 42, GPU0). Both arms are judged on the same four legs; the comparison is record-vs-record on the pooled 43-102 hold-out plus TOPB2.

**Read-out rule:** rotation is confirmed only if a flow197 record beats candidate B on the paired hold-out by the standing promotion rule while flow196's record at a comparable generation does not; a single passing record on either arm is a lottery ticket, not evidence for or against §10. Two 300-gen budgets with no flow197 record and a flow196 record = rotation rejected for this seed.

**Status:** staged and verified on the remote (md5 03cf5547); replaces flow195 (g160 seed, no record since g10) at its 300-gen budget via S/flow197/swap.sh; watcher ARMS includes flow197.

## 26. Time projection at the current pace — 2026-09-11 07:45Z (answer to the user's question)

Slope 298 pts/logit (§24). Candidate B: hold-out 73 %, projected asymptote ≈ 2795. Gaps from B: top 10 (2956) = 82.8 % hold-out = +160 pts ≈ 6 boards of 60; top 5 (3016) = 85.5 % = +220 ≈ 8 boards; top 1 (3090) ≈ 88 % = +300 ≈ 10 boards.
Measured pace: three passing records in 36 h (A/B/C) but overlapping — net hold-out movement since g1000 ≈ +4 pts (2-3 boards); every lineage plateaus (flow187 after g160, flow193 g100→g300 nothing, flow195 nothing after g10) → ≈ 1 useful board per day across three arms, harder per board (logistic).
Projection: top 10 in 8-12 days (09-19 … 09-23), P ≈ 30 %; top 5 in 10-16 days, P ≈ 10-15 %; top 1 not reachable by this mechanism. Add ~1 day per promotion for Kaggle convergence (~80 games at ~90 games/day).
Levers on the projection: upload B (LB has not moved since 09-10); pace scales ~linearly with arms (a second GPU pair ≈ halves time to top 10); flow197 rotation (§25) decides whether the per-lineage plateau is fixable — read-out ≈ 1 day.

## 27. Top-tier rotation arm flow198 — staged 2026-09-11 07:47Z (user: "can we use more strong opponents in our training?")

**Answer:** yes, by rotation, not by weight. The 20 top-ten rungs already carry 37 % of the objective mass at w10.2 (§11); they have been the same 20 boards for every lineage since flow183, so the ES has memorised them (TOPB2, the held-out twin, sits at 25-32.5 %). The lever left is fresh top-tier boards.

**Design:** launch_flow198.sh = the flow196 control recipe (candidate-B seed) with exactly the 20 top-ten rungs replaced by 20 fresh boards: 2 wins per CURRENT top-10 team (SpaTaro 3107 … carlos-tagosaku 2951) against opponents rated ≥ 2850, played 06:21-07:43Z today, tape = the top player's seat (S/flow198/rows_sel.json). Same weight (10.2), same budget (147 rungs). None is a judge board or in the gate field. The 42 LIVE-C mid-band rungs stay so the change is isolated: flow196 control, flow197 mid-band rotation, flow198 top-tier rotation. Runs on the local 3070 after flow194's budget (~11:00Z); --abs-pairs 32.

**Read-out rule:** the top-tier rotation is confirmed only if a flow198 record beats candidate B on TOPB2 (held-out top tier) with the pooled 43-102 hold-out not down, while flow196 at a comparable generation does not. TOPB2 is the primary leg for this arm; a hold-out-only gain says nothing about the hypothesis.

## 28. SpaTaro vs ours — replay ledger, landed 2026-09-11 08:41Z (`2026-09-11-spataro-vs-ours.md`)

Measurement only (n=2 SpaTaro wins, 3 wins + 1 loss of ours vs 2500-2700). SpaTaro: 6 hands at day-0 hour 0-1 and six per day through d5, purse at 0-100 coins every evening d0-d9 (70 hand-days d0-9 vs our 46); 10-11 melon tiles on d0 dumped d10 at ~253; 2 cows + 2 sheep at hour 0, 8 cows / 8-14 sheep by d10, fed with 452-476 bought wheat (16-18k over the game) so fertilizer (217-231 units) and milk/wool run from d2-6; six products sold across 232-242 sell turns spread over all 24 hours. Ours: 4 hands d0 → 5 by d3-7, 165-2,076 coins idle overnight, melons planted d9-13 and dumped d22-25 at 112-209, one bulk animal buy on d0, eggs/tomato/carrot after shops, 49-56 sell turns at hours 1 and 18 only. Cash d10: 9.6k vs 3.0k; d20: 71k vs 48k; d21-29 earned: 29-34k (SpaTaro) vs 42-70k (ours); finals level (101-104k vs 94-114k). Read: SpaTaro's edge is entirely a d0-d20 labour + herd compounding line; its late game is weaker than ours. Together with the record (§ verdict 08:50Z: rank 1 = 30-0 streak artefact, 0-5 vs 3050+), SpaTaro is the incumbent template, not the form leader; the follow-up ledger is how Majkel1337 beats it.

## 29. Majkel1337 vs SpaTaro — replay ledger, landed 2026-09-11 08:57Z (`2026-09-11-majkel-vs-spataro.md`)

Six games, Majkel 6-0 (+1.8…+18.4k). Same farm template as SpaTaro (§28) — the top tier is ONE line — but Majkel wins on the cost side, not the revenue side: bought wheat 117-190 units (4-7k) vs SpaTaro's 375-535 (14-22k) explains the whole spend gap (−8.8k median, 6/6), while gross revenue is lower in 4/6. Revenue is re-mixed: less wheat/carrot, more strawberry held off the d20-24 price collapse and sold d27-29, 12 melon tiles, tomato in every game, 2 geese, 3 sheep on d0. Behind at d10 in all six, ahead in d11-20 and d21-29 in all six. Market interaction between the two seats is negligible (~20-coin pumps, shared d10 melon dump costs each ~10/unit). Majkel's opening is byte-identical across games (1 cow + 5 wheat d0h0; 4 hands + 1 cow + 3 sheep d0h1; hand vector 4/4/6/6/6/6/8/9/9/10 → 11 flat).
**Read for us:** the 3000+ tier is decided by (i) the d0-d9 labour/herd compounding line that both share and we lack (§28) and (ii) spend discipline on feed plus a late strawberry hold — not by market attacks. Labour-compounding research (agent, 45-min box) is in flight; measurement only so far, no lever proposed.

## 30. Labour compounding — research landed 2026-09-11 09:01Z (`2026-09-11-labour-compounding.md`)

**Mechanics (bit-exact port, cited):** the (n+1)-th hire of the day costs fib(n) (4 hands = 7, 6 = 20, 10 = 143, 12 = 376, 16 = 2,583); no wage; hands and the hire counter reset nightly; one op per hand per turn (~21 productive turns per hand-day); SELL/BUY/HIRE cost no labour; a melon tile emits no task for its first 6 days.
**Measurement (SpaTaro n=2, Majkel n=3, ours n=4):** labour does not compound, capital does. SpaTaro's six day-0 hands PASS 41-47 % on d0-5 and earn less in-window than our four; ours are the busiest hands of the three files. Marginal hand-day ≈ 0 coins on d0-5, 0-80 on d6-10. The d11-20 gap is coins per productive hand-hour (57-62 vs 33-48) = more standing capital (56-62 tiles vs 46.5; 16-22 animals). Our slack is idle CASH overnight on d2-9 (0.6-5.7k vs 0-200 for both top files).
**History (§4 of the doc):** FORWARD_ADMIT dead ×3 (−9.2k t −6.7; −8.7k t −12; −2.6k t −8); crew floor, hand ramp, N_SELL_ROWS 4/6, LOT_SLICE all dead; hire_bias/horizon/crew_target are theta-reachable and sit at an ES interior optimum.
**Candidates ranked (coins × P(real) ÷ cost):** (1) IDLE_PURSE_TOPUP_ON d0-9 — after the budget grant, spend purse − reserve − land hold on the cheapest positive-value plantings legal today, hands enumerated after so the crew follows; +3-6k by d20 if it does not displace the d5/d10 quads; (2) COW_DAILY_ON d3-9 (+1 cow/day floor while affordable; +1-2k); (3) HORIZON_CHARGED_ON (discount projected rungs by distance; ≤ +1k). Not candidates: FORWARD_ADMIT + purse-to-zero (dead ×3), hour-0 herd (already ours), 24-h sell spread (market effect, dead as tested).
**Decision:** build IDLE_PURSE_TOPUP_ON as a switch (default OFF, identity byte-exact), judge paired on 43-72 + 73-102 + TOPB2 against candidate B's theta, read d-ours vs d-theirs before win rate; kill on d-theirs > 0 (denial handed back) or d-ours < 0 with win rate down. Positive → a zero-init plant-floor gene for the ES (gene-slope rule).

## 31. IDLE_PURSE_TOPUP_ON — built, identity-exact, judged, KILLED (2026-09-11 09:28Z, `2026-09-11-purse-topup.md`)

Switch = a second budget grant over the seed lists on purse − hold − KEEP after the hour-1 grant, feeding seed_buy / fill_target so both hire passes price the enlarged task list (worktree `purse-topup`, commit 6548777; identity byte-exact OFF). Paired against candidate B's own csvs: KEEP 200 → pooled hold-out 73.3 → 70.0 % (0/−4), d-margin −361, d-theirs > 0 on every leg; KEEP 0 → −4.4…−5.2k/game at t −3.5…−5.8, flips +0/−35, opponent +2.9-3.1k (displacement + denial handed back, the PLANT_FILL v2 signature).
**Why the premise was wrong (§30 corrected):** the end-of-day purse of 0.6-5.7k on d2-9 is revenue that lands at turns 3/10/18, after the day's single BUY row; at the BUY row itself the leftover is 4-108 coins on d1-6 (290-390 on d7-8), and free tiles are 0-3 on d0-4 and d6-9. Idle cash that is really spendable appears only from d10 (1.9-4.8k) against 1-3 free tiles — a land/plate question, not a cash one.
**Closed:** the labour/capital hand-lever family in full (FORWARD_ADMIT ×3, crew floor, hand ramp, purse top-up). COW_DAILY_ON (§30 #2) inherits the same constraint (one BUY row, cash arrives after it) and is not worth a leg. **Residual worth a look, not now:** one BUY row per day leaves the day's revenue idle ~23 h — the PRESTOCK / intraday-market family (2026-08-30) — but it needs free tiles to matter.

## 32. LOSS10 — a counter class in the 2200-2400 band (2026-09-11 09:56Z, S/bloss/)

Candidate B (live sub 56161192) went 11W-10L against 2150-2400 opponents where the hold-out judge predicted ~73 %. All ten losses re-cut as pinned-town tapes and re-played at a fresh seed base from both seats: B 1/20, hr (flow172_g1000) 0/20, A 2/20, C 2/20; margins −3.2k to −4.2k per game. Not the shop draw: these opponents beat every theta of ours at any draw. Nine are established files with stable 2175-2381 ratings; two have losing overall records yet beat us 20/20 — a strategy class that counters our planner specifically while losing to the field. None of the judge sets (LIVE-C 43-102 cut from our 2450-2700 games, TOPB2, LIVE62) contains it, which is why the judge→ladder calibration (§24) read high and the g40 falsifier is failing.
**Consequences:** (1) LOSS10 becomes a judge leg (informational at first; 20 games, base = B's own csv S/bloss/B.csv); (2) the ten tapes go into training at high weight in the next arm (flow199, B seed) unless the anatomy (`2026-09-11-loss10-anatomy.md`) shows a planner-level exploit that a switch fixes faster; (3) the B asymptote projection (≈2795) is withdrawn pending the anatomy; the 2200-2400 band is a gate B must pass through and currently loses half its games in.

## 33. LOSS10 anatomy — no counter class; the town decides (2026-09-11T10:05Z, docs/strategy/2026-09-11-loss10-anatomy.md)

Corrects §32. The ten 2175-2381 opponents that beat B 19/20 on pinned towns are one file: the public open-loop band clone (5 hires h1, 12 melon d0 → 60-melon dump d10h0 at 247, 2 cows + 2 sheep, land d6/d11, ≈160 wheat, all sales at h0), the same clone B beat three times this morning under 2500-2600 names. Our seat is identical to ±0.5k through d9 in all 13 games; the −16.4k d10 step (their melon pot) and the −16…−28k d14-16 trough appear in wins and losses alike. The games are decided by the d15-29 recovery, which follows the town's shop sequence: PIZZA_SHOP on d8 in both big wins (tomato +30.0k / +4.1k; the clone never plants tomato), d14 or later or absent in every loss (tomato 0-3.6k). Structural, present in every game: fertilizer −7.3k (they sell 340-356 units, we 131-245 with more cows), melon pot −3.3k, hire spend +1…+4k against us, wool −4.6k in 8/10. OPEN_PUMP is a −177-coin wash against this clone.

| claim | reading | consequence |
|---|---|---|
| counter class in the 2200 band | REFUTED — same clone, loss-selected tomato-poor towns | LOSS10 leg kept, INFORMATIONAL (it is the coin-flip half of the ladder vs the clone) |
| B's g40 falsifier (floor 2439) | FAILED — 30W-10L 2284 at g40 | recalibrate on B's live curve at g60/g100; hr read ~2400 at g70 → 2557 at g178, so not yet decisive |
| planner exploit to switch off | none — nothing they do targets us | no switch build from this anatomy |
| training answer | flow199 re-weighted: 10 tapes w10.2 → w4 (band weight), md5 b78196de, next queued arm | launch on flow196's third loss or an idle GPU |
| open question | fertilizer engine: 131-245 vs 350 units with more cows | one 20-min measurement agent (feed hours / tile application / sell timing; check the 09-06 fert closure first) |

## 34. Fertilizer engine — the −7.3k is displacement (2026-09-11T10:17Z, docs/strategy/2026-09-11-fertilizer-engine.md)

| claim | reading | consequence |
|---|---|---|
| we produce less fertilizer with more cows | REFUTED — 1 unit/animal/night regardless of feeding; we collect 367 vs 346 (+976) | no feed-hour lever |
| the −7.3k sale gap | 89 % = we APPLY 190 units vs 62 (−6,490), valued +16.8k net vs their +12.4k on the 09-09 census | application-throttle family stays CLOSED (09-06) |
| claimed cheap early fertilizer resale | REFUTED by the original 13 raw replays: d0–9 quotes 77–100, early BUY pre-row quotes 81–89; the −1.9k is gross revenue allocation, not profit | no storage-buy pilot from this premise; see `2026-09-12-fertilizer-premise-correction.md` |

## 35. Top-50 playing templates → flow200 (2026-09-11T10:26Z, docs/strategy/2026-09-11-top50-patterns.md)

13 templates across the top 50 (56 win replays, 1.8 GB). 24/50 files are the public band clone we already train on; nine new templates/members were cut as pinned-town tapes (T0b clone + 4th quadrant and tomato d18; T0c wool-herd clone; two new T0d "feel the agi" derivatives; T6 QQ Farming; T7 Xiangyu Liu; T8 keiz; a T0a pump variant). Only Majkel1337 and SpaTaro are adaptive from step 1; the field does not react to the shop sequence.

| item | value | consequence |
|---|---|---|
| new tapes | 9, byte-exact drawn + pinned-town; towns 454 → 463 everywhere (local, artifacts, remote) | training rungs only, never judge boards |
| flow200 | flow199 + 9 tapes at w4, 166 tape rungs, --episodes 179, seed 303, md5 ff2a457e | NEXT QUEUED ARM; flow199 fallback |
| caveat | ranks 8-50 read from one replay each; weights unmeasured | first records judged on the five legs vs B like every arm |

## 36. Control arm exhausted → flow200 launched (2026-09-11T10:49Z, S/glut/verdicts.log RULE 4 line)

**Claim tested.** Does B's own recipe, continued from B (flow196 = flow193 recipe verbatim, seed 299, GPU0), produce a theta above B?

**Evidence (paired real-engine, five legs vs the live candidate B):** three reads, all below B — g10 record, g60 record, and the g100 periodic snapshot judged by hand at 10:44Z (TOPB2 0/1 flips −784; LIVEC-H30 0/2 −755, t −3.9; LIVEC-H30B 2/6 −24; LIVE62 4/6 −460). The remote gate refused every candidate up to g172 (g100: net −3, margin +3028 → +2310).

**Decision.** Rule 4 (three straight losses) fired at 10:46Z: flow196 stopped at g172 by exact pid (artifacts kept), flow200 launched on GPU0 (control + 10 LOSS10 towns at w4 + 9 new-template top-50 tapes at w4, 166 tape rungs, B seed, seed 303; md5 ff2a457e verified before launch). Watcher restarted (pid 68566) with flow200 in ARMS. flow199 stays the fallback.

**Reading.** Plain continuation from B at lr 0.003 is flat for 172 generations; the live levers are the rung-mix arms: flow197 (mid-band rotation, GPU1, g70), flow200 (new-template rungs, GPU0), flow198 (top-tier rotation, local, swap at flow194 g300).

**Open.** Kaggle B sits at 37W-16L / 2294 after 53 games (Elo equilibrium ≈ 2440 vs a ~2300 pool) while hr holds 2555; the B-ladder paired study (S/bladder/, Opus agent, in flight) tests whether the judge tracks the ladder.

## 37. B on its own ladder boards — the judge is not falsified (2026-09-11T10:59Z, docs/strategy/2026-09-11-b-ladder-paired.md)

**Claim tested.** B's ladder rating (2269-2311 after 50-55 games) trails the hr file (2555). Is the paired-leg judge that promoted B over hr miscalibrated?

**Evidence (real engine, paired, all 50 of B's Kaggle boards — wins and losses).** Opponents' own pinned-town action tapes, our thetas in B's seat. Fidelity: B reproduces the Kaggle result on 50/50 boards (score coin-exact on 25/50). hr 31W-19L vs B 34W-16L, flips +0/−3 (both seats +0/−6, sign test p = 0.031), paired margin −1,339 coins/game (t −3.7). A 36W-14L, +4/−2, +43/game (t 0.1). By band: <2100 (17 placement games) B 17-0 / hr 16-1 / A 17-0; 2100-2299 B 12-11 / hr 10-13 / A 13-10; 2300-2499 B 5-5 / hr 5-5 / A 6-4; no 2500+ opponent met yet.

**Decision.** The judge stands; hr would have done worse on the same boards and A is level. B's rating gap to hr is Elo history (17 unpaid placement wins, 50 games vs 185) plus lagging opponent ratings for the clone files, not agent strength. The 10:35Z "equilibrium ≈ 2440" reading is withdrawn. B stays the live candidate; no upload change.

**Caveat.** Open-loop replays flatter the counterfactual columns (hr/A play against a script that cannot react), so hr's deficit is a floor and A's parity is optimistic.

**Side effect.** 40 new pinned-town tapes of B's ladder opponents (S/bladder/, towns 463→503 locally, remote untouched) — a rung set for a later rotation arm.

## 38. Rotation arm read #2; flow201 queued (2026-09-11T11:28Z)

**flow197 g100 (periodic, judged by hand) vs B:** TOPB2 0/3 flips (−685); LIVEC-H30 −904/game (t −3.05, no flips); LIVEC-H30B 0/10 flips (83.3 → 66.7 %); LIVE62 +8/−2 boards but −250/game. Second loss vs B (g10, g100). The pattern — gain on the LIVE62 tuning set, loss on the hold-out — is drift toward the trained distribution.

**Queue.** flow201 staged (docs/strategy/2026-09-11-flow201-staging.md): flow200 + the 40 pinned-town tapes of B's actual ladder opponents at w4 (206 tape rungs, 219 episodes, seed 304, md5 d4d70b31; remote towns 503). NEXT queued arm ahead of flow199. Rule 4 fires it on flow197's third loss or an idle GPU.

## 39. Rotation arm exhausted → flow201 launched (2026-09-11T12:12Z)

**flow197 g140 (record) vs B:** TOPB2 −1,704/game (t −2.9, no flips); LIVEC-H30 −1,061 (t −3.65); LIVEC-H30B 0/8 flips (83.3 → 70.0 %); LIVE62 +6/−8, −1,170 (t −3.6). Third straight loss (g10, g100 periodic, g140). **Decision.** Rule 4: flow197 stopped by exact pid (artifacts kept), flow201 launched on GPU1 (flow200 + 40 B-ladder opponent tapes at w4, md5 d4d70b31, verified 12:11Z). **Reading.** Replacing the 42 LIVE-C training boards with 42 fresh band boards did not generalise: gains on LIVE62, losses on the hold-outs — the same drift signature as the control arm's flatness. Arms: GPU0 flow200 (1 loss), GPU1 flow201, local flow198. Queue: flow199 fallback only; flow202 (flow201 + 60 hr-ladder top-tier tapes) is the natural next stage.

## 40. B on hr's ladder boards — B is the stronger file at the 2500+ tier too (2026-09-11T12:12Z, docs/strategy/2026-09-11-hr-ladder-paired.md)

**Claim tested.** B had never met a 2500+ opponent; is hr (2584) still the better leaderboard file against the tier it faces? **Evidence (real engine, paired, hr's 60 most recent ladder boards, opponents 2426-2657, wins and losses).** hr reproduces its Kaggle result on 56/60 (coin-exact 31/60; 3 of 4 misses are shop-draw coin flips). hr 35W-25L (+3,552) · B 43W-17L (+5,131) · A 40W-20L (+4,390). B vs hr +10/−2 flips (p 0.039), +1,579/board (t 3.5), both seats +20/−3 (p 0.0005). A vs hr +7/−2 (+838). B vs A +5/−2 (+741, t 2.6). Per band B leads hr in every band, most at 2600+ (7/9 vs 4/9). **Decision.** Ordering B > A > hr on identical frozen opponents, boards and seeds. B stays live; when the next candidate is packaged, the slot to free is hr's (sub 56143250), not B's. B's ladder rating (2387 at g77) should overtake hr's as its placement history washes out; this is now a live falsifier: B ≥ hr's rating by ~g200. **Caveat.** Counterfactual margins are upper bounds (open-loop tapes). **Side product.** 60 top-tier pinned opponent tapes (S/hladder/, towns 538 locally) = rung set for flow202.

## 41. Judge md5 audit — every verdict judged the right bytes (2026-09-11T12:50Z, docs/strategy/2026-09-11-judge-md5-audit.md)

**Claim tested.** `watch.sh --judge` fetches best_abs.npy (= the seat for --keep-candidates arms) instead of cands/gNNNNN_record.npy; did any verdict that drove a Rule 4 kill judge the seat or a stale record?

**Evidence.** All 11 verdicts (flow194 g10/g100, flow196 g10/g60/g100p, flow197 g10/g100p/g140, flow198 g10, flow200 g10) match the remote cands/index.jsonl md5 for their gen; theta mtimes precede their csvs; all topb2/live62 csvs are byte-distinct from B's. The single `--judge flow200 30` firing fetched the seat, hit the duplicate-md5 guard, logged NOT judged and deleted the theta file; the real g30 candidate (13b7a6b0) was re-fetched by path and is being judged.

**Decision.** No verdict re-runs; flow196/flow197 retirements stand. `--judge` is unusable for stage_hr arms (the guard is empty on a fresh arm); fix staged as S/autojudge/watch.sh.next for the next watcher restart; gap-judging = scp the cand + `--legs` by path.

## 42. Lever ranking — training-free thetas first (2026-09-11T13:02Z, docs/strategy/2026-09-11-lever-ranking.md)

**Claim.** Every arm since B varies one thing (the rung mix) and all eight paired reads are below B; the untested cheap axes are the theta itself. **Shortlist.** E1 soup (B+C)/2 and (B+C+seat)/3; E2 extrapolation of B's accepted 100-gen step (k = 0.5 / 1.5 / 2.5 from the g160 seat); P3 PRESTOCK screened with EARLY_SELL_ON=False (its lock-out concession now reads level); E3 one-step σ/P test at B; P4-lite EARLY_SELL_MODE B/A0 and OPEN_PUMP_UNITS 90/120. **Odds.** 2950 by 09-23 ≈ 20-25 %. **Decisive result.** A training-free theta clearing B by ≥ +5 pooled hold-out points with TOPB2 not down → directed search; all level or down + κ ≈ 0 at B → B is a peak like g1000. **Status.** soup2 / k0.5 / k1.5 queued on the judge 2026-09-11T13:02Z; soup3 / k2.5 held for the first reads.

## 43. ROUTE_EARLY_ON is a double-subtraction, not a lever; P3 dropped (2026-09-11T13:25Z, docs/strategy/2026-09-11-route-early-bug.md)

**Mechanism.** `_routes` returns one early vector; `build_day` subtracts it under ROUTE_EARLY_ON and again under ROUTE_SPLIT_ON (shipped True), so early units start two turns before the base route: the farmer steps off the shed tile before turn-0 HIRE and every hand is re-scattered (−142k/board, 0 % identical). PRESTOCK/MARKET_PACK's −155k reads were a different failure: the seat crashed at import and sat on its 3,000 starting coins. **Decision.** ROUTE_EARLY closed — ROUTE_SPLIT_ON is the repaired version already shipped. P3 (PRESTOCK re-screen) dropped: it also asserts under OPEN_PUMP_ON, and trading the pump away for a level-prior switch is not worth judge time. Harness lesson: add a coins-floor void detector so a crashed seat is never recorded as a margin.

## 44. OPEN_PUMP constants — closed against B (2026-09-11T13:43Z, docs/strategy/2026-09-11-open-pump-sweep.md)

**Claim tested.** Are the opening-pump constants (53/5/1584) mis-set against the live candidate B, and does a pumper-aware hour-1 row help vs the top tier? **Evidence (paired, B's own csvs, TOPB2 + LIVEC-H30).** UNITS 35 −916 (t −2.0), 70 +556 (t 1.0) / −292, 90 −1,686 (t −2.0, kill); MIN_MONEY is compared with the flat 3,000 opening purse, so 1200/2000 are byte-identical to B and 3001 is byte-identical to pump-off; pump-off −228 (t −0.4) / +20; the hour-1 row was built 2026-09-05 and is inert because SLOT0 already clears the row; SLOT0 off +349/−293. **Decision.** P1, P2 closed; no promotion. **Lesson.** Two unrelated day-0 changes replay the 60 hold-out games to within 2.2 coins: day-0 legs read the shop-draw re-roll (§ shop lottery), so they can falsify a constant but never select one — do not sweep day-0 constants on these legs again.

## 45. Ladder projection — hr ≈ 2722, B ≈ 2562 on the band pool; cutoff now 2967 (2026-09-11T13:53Z, docs/strategy/2026-09-11-ladder-projection.md)

**Evidence (Kaggle episode API, all games of both files).** Matchmaking is me ± 45 and tracks our rating 1:1; neither file has played a ≥ 2700 opponent. Logistic-Elo equilibria: hr 2722 [2625, 2822], B 2562 [2397, 2740] (B's read is the 2200-2400 pool with its LOSS10 slice at 44 %; on common support B − hr = −0.41 ± 0.47 logit). Monte-Carlo at K 8.9, +100 games: B 2406/2484/2564, hr 2611/2666/2721 (10/50/90 %). Top-10 cutoff has moved to 2967 (rank 5 = 3003); a file of exactly top-10 strength reaches ~2843 in 150 games. **Decision.** hr stays live (LB entry, only file with games above 2500) until a candidate clears the hold-out bar; the ladder is a 100-game falsifier of a predicted equilibrium, never the judge. Top-10 remains a +250-pt strength problem on every judge set.

## 46. Training-free thetas: soup and extrapolation both below B (2026-09-11T14:16Z)

**Claim tested (lever ranking E1/E2).** Does averaging B with its independent twin C, or scaling B's accepted 100-gen step from the g160 seat, yield a theta above B without training? **Evidence (paired, B's csvs).** (B+C)/2: TOPB2 +76, LIVEC-H30 −236 (0/2), LIVEC-H30B −170 (0/8, 83.3 → 70.0 %), LIVE62 +188 (10/2) — the drift signature. k = 0.5: TOPB2 −279 (0/3), H30 −475 (t −1.3), H30B +276, LIVE62 +17. k = 1.5: TOPB2 −867 (0/4), H30 −735 (t −2.5), H30B −2 (0/6), LIVE62 −621 (t −2.2). **Decision.** E1 and E2 closed; k = 2.5 and the 3-way soup not run. **Reading.** B is a local peak along both directions; accepted ES displacements do not contain re-usable signal. Per §42 this is the symmetric result: the remaining path is E3 (is there any gradient at B's centre?) and, failing that, a different seat or objective, not more rung-mix arms.

## 47. EARLY_SELL_MODE B / A0 — closed; refused switch combos play 0 moves (2026-09-11T14:17Z, docs/strategy/2026-09-11-early-sell-mode.md)

**Evidence (paired vs B).** Mode "B" (all six market turns): TOPB2 −7,976 (t −9.8, 0/7), LIVEC-H30 −7,284 (t −20.5, 0/18) — every board worse; end-of-game unsold 7.7 → 90.4 units. Mode "A0": +432 / −9 / −119 (|t| ≤ 2.1) = level, and plan.py:7752 refuses it while OPEN_PUMP_ON is live. **Decision.** P4-lite closed; EARLY_SELL_MODE stays "A". **Harness rule.** A refused combination does not crash the eval: the seat plays 0 moves for 3,000 coins (margin −154,609, exit 0). S/bank/paired.py now flags VOID rows (moves = 0 or mine < 5,000) so a crashed seat is never read as a margin.

## 48. E3 staged and launched on the local card (2026-09-11T14:30Z, docs/strategy/2026-09-11-onestep-prep.md, S/onestep/)

**What.** The validated one-step antisymmetric gradient test (§17-§20 rig, S/popcurve) driven at candidate B's centre over σ ∈ {0.01, 0.02, 0.04} × P ∈ {512, 2048}, fixed step length R = 0.2323, +d / −d / 8 signed randoms scored on the flow193 rungs and the 30 LIVE-C 43-72 hold-out tapes (0 overlap with training), then the real-engine judge (TOPB2 + LIVEC-H30, paired vs B's csvs) on the saved directions. **Cost.** ~2.7 h on the 3070 (chunk-bound ~4 GB, no generation, no abs probe); local flow198 (g80, 1 loss) stopped cleanly and resumes from state.npz afterwards. **Decision rule (fixed).** PASS = hold-out κ > 0.03 and +d ≥ 14/16 vs randoms and net +d gain > 0 → continue ES from B at that σ/P after engine confirmation and an EPS_SEED repeat. FAIL = all cells κ ≤ 0.015 → B is a peak for this estimator; change the field (W_lost objective at B, seat swap, fresh top-tier rungs), not the knobs. Mixed (in-sample only) = FAIL for knobs.

## 49. Sim theta screen rebuilt; a refuser/orderer, not a promoter (2026-09-11T14:37Z, docs/strategy/2026-09-11-simscreen-rebuild.md, S/simscreen/)
- Pre-wipe source survived at S/_recovered/simscreen/screen.py; rebuilt on pinned-town tapes with shop_crn, frozen LIVE-C hold-out boards 43-102 (120 cells), multi-theta CSV out, 463 s for 10 thetas.
- Defect fixed: TAIL_FILL_ON / BANK_BEFORE_LOT_ON / HIRE_ROW_ON default False in the worktree but True in the judge and the shipped package; screening on worktree defaults flipped the validation sign (+312 vs −528). screen.py now applies the S/livec/run.sh switch string before importing sim.
- Validation vs engine: sign and order agree on every pair with an engine read (flow200_g30 above B = LEVEL, flow201_g10 below = LOSS, seat below B). Resolution ≈ ±400 coins/board (SE ≈ 180); six of ten rows level with B → ranks the queue, cannot settle promotion. Blind spot: plays only the LIVE-C family, so a TOPB2-shaped loss reads −174 instead of −1,815.
- New facts: extrap_k25_hr is broken (30.8 % win, t −22; extrapolation monotone-bad in k: +185 / −402 / −13,734); soup3_BCS −238 would not have re-opened E1. No k25/soup3 judge legs were queued, nothing to cancel.
- Use: pre-rank candidate records before spending judge lock; never promote from it. Follow-up: add a TOPB2 board file (dispatched 2026-09-11T14:37Z).

## 50. Sim screen gains a TOPB2 board file; blind spot closed (2026-09-11T14:47Z, docs/strategy/2026-09-11-simscreen-topb2.md)
- S/simscreen/boards_topb2.json = the engine's own 40 TOPB2 rows (20 pinned-town tapes × 2 seats × first --seed-per-opponent draw), 40/40 identical to S/lossflip/flow193_g100_hr_topb2.csv. screen.py --board-file selects it; default file unchanged.
- Validation vs B: sign 6/6, max Δ error 45 coins, Spearman 0.94, win % digit-exact on 7 thetas, per-board sign 97.9 %. flow201_g10_hr reads −1,837 (engine −1,815). 252 s CPU for 7 thetas.
- Honest unit = 20 boards (seat pairs are the same game on 10-15 tapes): SE 600-850/board; refuse at 20-board |t| ≳ 2.5. Rule: the screen refuses on both families now; promotion still requires the four paired engine legs.

## 51. flow203 staged = the E3 FAIL-branch arm (2026-09-11T14:48Z, docs/strategy/2026-09-11-flow203-staging.md, S/flow203/)
- Recipe: flow199 base (flow196 control + 10 LOSS10 tapes w4) with the 157 --rung-weight tokens set W_lost-MILD from B's own per-rung margins (lost ×2, barely-won ×1.5, won ×1, 15 % mass cap); σ 0.02, lr 0.003, pop 512, seed 306; no trainer patch (--rung-weight exists). Replaces flow199 in the queue.
- Rejected on evidence: seat swap (per-rung margin correlation across seats 0.994), fresh top-tier rungs (= flow202, already queued), ×4 W_lost (lost held-out on both seeds).
- Gate before launch: ~/flow203_precheck.sh <gpu> (~20 min GPU) measures the weights at B's centre and re-runs the lost-board one-step test AT B; launch only if held-out net +d gain > 0 on obj and margin and ≥12/16 randoms beaten on both seeds. Launcher exits 2 without a valid 157-token weight file.
- Staged on the remote 2026-09-11T14:48Z: ~/stage_hr/launch_flow203.sh (51a4fb72), ~/stage_hr/flow203_rungs.txt, ~/flow203_precheck.sh (3431a8cc), ~/launch_flow199.sh (b78196de). Queue: flow202 (fresh top-tier rungs) on the next freed GPU; flow203 only after E3 FAIL + precheck PASS.

## 52. flow204 staged = the E3 PASS-branch arm (2026-09-11T14:58Z, docs/strategy/2026-09-11-flow204-staging.md, S/flow204/)
- launch_flow200.sh (B-seeded control) with σ/pop taken from the E3 winning cell (SIGMA=… POP=… required, exit 2 otherwise), lr mapped in-script (σ 0.01→0.001, 0.02→0.003, 0.04→0.003), seed 307, --run flow204; everything else identical (init B, 166 pinned rungs, episodes 179, chunk 8192, 62-board gate min_flips 5, --keep-candidates).
- Memory fit: peak is chunk-bound; pop 2048 adds ≈ +80 MB → ≈ 5.0 GB of 24 GB, no chunk/episode change. Cost is wall: P 2048 ≈ 3.7 min/gen (~19 h / 300 gens) → prefer a passing P 512 cell.
- Coordinator's gate before launch (launcher cannot check it): E3 PASS cell confirmed by the EPS_SEED=9002 repeat and the engine judge.sh/kappa.py read (§48 rule).
- Staged on the remote 2026-09-11T14:58Z: ~/launch_flow204.sh (ef6191ca), DRYRUN verified remotely. Launch: ssh user@remote-host 'SIGMA=<σ> POP=<P> GPU=<gpu> nohup bash ~/launch_flow204.sh >/dev/null 2>&1 &'

## 53. FERTCOW screen: premise false, FERT_VOLUME re-opened for ONE engine judge (2026-09-11T14:59Z, docs/strategy/2026-09-11-fertcow-screen.md, S/fertcow/)
- The −7.3k "fertilizer with more cows" line was revenue displacement, not production: we run fewer cows than the clone at d10 (6.6 vs 7.5), r(applied, sold) −0.85, production = 1 unit per alive animal per night. Cow/herd/feed half stays CLOSED.
- Smallest expression = existing FERT_VOLUME_ON (plan.py:3779-3800). Screened on B with the shipped hr string, paired vs B: spot 1/1 +135/+107 (level); spot 2/1 TOPB2 +441 t 1.1, LIVE-C +941 t 4.8 (88/32); marginal 2/1 TOPB2 +378 t 1.5, LIVE-C +901 t 4.9 (88/32). 71 % of the LIVE-C gain is the opponent's purse falling (denial signature), but wins are not level this time (71.7→78.3 %).
- Decision: ESCALATE to one paired engine judge (marginal 2/1 first, spot 2/1 second; 4 legs vs B, full hr string). Prior closure (2026-09-10: composed with HIRE_ROW it dropped 3-4 live boards) is exactly what the screen cannot see, so the engine decides. No promotion from the screen.

## 54. B's top-tier ledger on pinned towns: d10-14 tax + d15-29 denial (2026-09-11T15:13Z, docs/strategy/2026-09-11-b-toptier-ledger.md, S/topledger/)
- Tool S/topledger/ledger.py = the screen's sim with per-day sale/tile/idle ledgers; 40/40 TOPB2 boards reproduce 32.5 % / −1,472 digit-exact.
- Hole opens d10, deepest d14 (−17.5k), B out-earns the top tier every day from d17, finishes −2.2k. All 41 games (28 TOPB2 + 13 fresh) carry the d10-14 hole; the whole win/loss variance is the d15-29 recovery.
- Mechanisms: (1) d10-14 melon pot −19.5k/game, flat tax, win/loss swing +70 → not a discriminator; structural (hire enumeration prices today's tasks, deposit chain 12/72). (2) d15-29 recovery ±17.7k = THE discriminator; two thirds is their purse: their realised late price 65 c/u on our wins vs 81 on our losses at flat volume → denial of THEIR price; no opponent-supply term in the sell genes (plan.py THE HOLE) → not theta-reachable. (3) carry/slice partly theta (hold/press), lot turns constants; wide EARLY_SELL already lost.
- New: B realises a HIGHER late price per unit than the top tier on both families (118/79 vs 99/61) → late gap is denial, not our pricing. Fresh top-tier tapes: same mechanisms, same magnitudes.
- Top test: OPP_SUPPLY_ON (plan.py:1507) on PINNED legs paired vs B — its −3k closure was on drawn boards (voided by tape fidelity); only pinned read HELD42 +617 t 2.5 never confirmed. Screen first, refuse at 20-board |t| ≳ 2.5. Caveat: ledger animal columns read 0 (indexing bug, one-line fix, pending).

## 55. OPP_SUPPLY_ON REFUSED on pinned boards; family closed (2026-09-11T15:33Z, docs/strategy/2026-09-11-oppsupply-screen.md, S/oppsupply/)
- Screen vs B (engine-exact pinned towns, shopdiff 0/160): TOPB2 −430/−752/−3,166 at scale 0.5/1/2 (20-board t −1.9/−2.3/−3.0); LIVE-C −251/−444/−3,986. Dose-responsive down on both files → HELD42 +617 not reproduced; the drawn/pinned distinction does not rescue it.
- Two-purse: our purse falls, theirs RISES (handed-back, not denial). Ledger: opponent d15-29 c/u on loss boards 80.2 → 80.2 (predicted 80 → 65); their units identical (tape seat, fixed SELL rows) — the switch only prices the forecast into OUR lot sizing, and pulling our lots back hands the shared price to them. The §54 discriminator (their late price) cannot be moved by our sell book against a fixed tape.
- Ledger animal columns fixed (S/topledger/ledger.py:101). Herd, ours|theirs d10/d15/d20: COW 6.5|7.1, 6.6|7.4, 6.5|7.2 — ~0.7 fewer cows all game, the one animal the top tier is ahead on; geese/sheep we lead. Recorded as an observation only (herd-deferral/ANIMAL_DEFER families are CLOSED; no hand lever launched).

## 56. E3 audit: sign OK, cliff = step-length artefact, PASS/FAIL rule void at α 1.0 (2026-09-11T15:35Z, docs/strategy/2026-09-11-e3-step-audit.md, S/onestep_audit/)
- Sign chain verified file:line against the tree the sweep imports (adv = rank_normalise(obj_w), grad = (adv[:half]−adv[half:])@eps, step = θ+δ): NOT inverted. Hold-out uses the same score_batch.
- No concentration: top coord 0.3-0.4 % of ‖d‖², max per-coord 0.012-0.015 = the random controls' profile; ‖g512‖/‖g2048‖ = 1.998 (√4), cos 0.53 (√¼) ⇒ the draw is sampling noise at both pops. ‖d‖ 0.232 is 3.3× SHORTER than ‖σε‖ 0.774 (my "outside the radius" premise was inverted).
- Scale test (engine-exact screen, paired vs B): α 1.0 −16.6k (win 15 %) but α 0.1 +140 / α 0.03 +111 / P512 α 0.1 +286 t 2.3, mirrors −256/−178 ⇒ antisym +396/+289 LIVE-C, +915 TOPB2 (correct sign). Adam-like 0.003·sign at full length also loses ⇒ length along the selected axis is the problem, not per-coord size. α 1.0 loss is a denial signature (ours −4.9k, theirs +11.3k).
- Rule change: the §48 PASS/FAIL rule cannot be applied at α 1.0 (both branches unreachable, cliff independent of σ). σ 0.02/0.04 cells are read for ‖g‖ pop-ratio, cliff depth, in/held-out agreement only. E3b (dispatched 2026-09-11T15:35Z): every cell re-read at α 0.1/0.03 on the screen with same-length random controls; the permuted-advantage control is added to the rig before any arm is cut on a κ. flow203/flow204 launches wait for E3b.

## 57. FERT_VOLUME on B: margin up on all 8 legs, wins level → NOT PASS, family closed (2026-09-11T15:50Z, docs/strategy/2026-09-11-fertvolume-engine.md, S/fertcow/engine.out)
- Engine paired vs B, shipped hr string: marginal 2/1 TOPB2 +376 t 1.4 | H30 +502 t 2.8 | H30B +940 t 4.0 (W0/L2) | LIVE62 +816 t 4.8; spot 2/1 TOPB2 +466 t 1.2 | H30 +397 t 1.9 | H30B +1,141 t 5.3 | LIVE62 +836 t 5.4, no net flips lost. Pooled LIVE-C wins 44/60 → 44/60 (marg) / 45/60 (spot). Denial-led 82 % (their purse falls on 27/30, 26/30, 52/62 boards).
- Verdict: NOT PASS (TOPB2 t < 1.5; wins level everywhere). Kaggle scores wins; a +800 denial margin with level wins is the 2026-09-10 signature reproduced. B ships unchanged. Spot > marginal in the engine (screen ordering inverted).
- Screen calibration: TOPB2 exact for a switch arm (+378/+441 vs +376/+466, ρ 0.9); LIVE-C ~20 % optimistic on margin and its WIN-RATE gain (71.7 → 78 %) does NOT transfer (44 → 44-45/60). Rule: never read win rates off the screen; margin ranks, engine decides.

## 58. E3c rig staged: permuted-advantage control + step-length axis (2026-09-11T16:03Z, docs/strategy/2026-09-11-onestep-e3c-prep.md, S/onestep/sweep_c.py, run_local_c.sh)
- sweep_c = sweep_b + --alphas 1.0,0.1,0.03 (randoms rescaled, α 1.0 thetas bit-identical to sweep_b's) + 4 permuted-advantage directions per cell (same ε rows, shuffled pairs; identity permutation reproduces one_draw bit for bit; ‖g_perm‖/‖g‖ within 0.8 % at rig size, |cos| ≤ 0.12) + saved advantages/pairs per cell.
- Rule in code: PASS only if at some α ≤ 0.1 the held-out +αd gains on obj_w AND margin, beats ≥ 6/8 randoms AND all 4 permuted directions; no FAIL from α 1.0 alone. Wall ≈ 1.3 h for σ {0.01, 0.02} × P {512, 2048}.
- Launch is CONDITIONAL on E3b: a candidate cell at α 0.1 → run E3c on that σ before cutting flow204; nothing at α 0.1 anywhere → E3c adds no information, go to flow203's precheck. The 3070 returns to flow198 after E3 either way; E3c would pause it again. judge.sh needs TH=${TH:-$O/thetas} before it can judge thetas_c.

## 59. IN-SAMPLE DIAGNOSTIC: the B-seeded ES arms are a NOISE WALK, not an overfit (2026-09-11T16:31Z, docs/strategy/2026-09-11-insample-vs-holdout.md, S/insample/)
- Paired vs B on each record's OWN training rungs at the exact pinned seed/seat the ES scored (206 rungs, shopdiff 0): flow200 g10 −646 t −3.8 | g30 +35 | g100p −318 t −2.0; flow201 g10 −511 t −3.4 | g20 −240 | g100p −38 (trimmed −289 t −2.0) | g140 +107; flow196 g100p −551 t −3.1. Mean −270; NONE reaches +300 at t ≥ 2; the trainer's own objective Δobj_w is negative on 5/8. In-sample vs hold-out Δ: Pearson 0.66 — no in/out gap to explain.
- Mechanism (with §56): the gradient draw at pop 512-2048 is sampling noise; Adam normalises every coordinate to ±lr regardless → lr 0.003 × 5997 coords = an isotropic random walk of ‖δ‖ ≈ 0.23/gen, and E3 showed that length along ANY selected direction is downhill-to-cliff while α 0.1 is slightly uphill.
- Consequence: board rotation / regularisation / new objectives (flow203) cannot help an optimiser that does not climb in-sample; the fix is STEP LENGTH + estimator variance: lr 0.003 → 3e-4 (or clip ‖δ‖ to the α 0.1 scale) at the same σ/pop. Every queued launcher (flow202/203/204) and the local flow198 resume carry lr 0.003 → re-staged at 3e-4 before launch (2026-09-11T16:31Z). flow198 resume chain cancelled.
- Falsifier (dispatched 2026-09-11T16:31Z, CPU): screen B + α(record − B), α ∈ {1, 0.3, 0.1, 0.03}, in-sample; verdict predicts the maximum at α ≤ 0.1 and no α reaching +300 t ≥ 2; falsified if any α = 1.0 record reads ≥ +300 t ≥ 2 in-sample.

## 60. E3b: no decodable gradient at B at any σ; the landscape at B is a plateau + ONE day-0 switch (2026-09-11T16:34Z, docs/strategy/2026-09-11-e3b-small-step.md, S/onestep_b/)
- All 6 cells (σ 0.01/0.02/0.04 × P 512/2048) FAIL the pre-registered small-step rule on all three clauses. Best: s0p01_p512 LIVE-C +286 at α 0.1 (t 1.7) but TOPB2 −703.
- Mechanism: 14 of 56 step thetas move 100 % of the boards — the SAME 14 on both families (disjoint tapes) = a board-independent day-0 switch. The objective along any ray at B is piecewise constant with one dominating discontinuity; every large antisym (ES and random) is that crossing (σ0.01's +396/+915 = its minus side crossing and losing; σ0.04's −1,738 = its plus side crossing). κ at B is a Bernoulli readout of one switch, honest n = 1. Same-length randoms are not neutral (TOPB2 −668 ± 977; four of eight randoms give A +1,434…+2,378 with zero gradient content).
- p512/p2048 agreement (cos 0.53, ‖g‖ ratio 2.0 at every σ) = the shared-prefix value for a ZERO mean gradient. The §56 reading "correctly signed but tiny → lower the step" is WITHDRAWN; "B is a peak" is not recorded either — the rig measures neither. E3c is NOT launched.
- What stands: §59 (records lose in-sample) is a separate measurement and holds; lr 3e-4 re-stage proceeds as the direct test of it (expectation: slower wandering on a plateau, i.e. level records, not gains). The lever E3b exposes: WHICH day-0 decision do the 14 perturbations flip, which genes carry it, which side is B on → freeze/clip those genes so the ES sees a smooth objective, or flip it if B is on the losing side (dispatched 2026-09-11T16:34Z).

## 61. lr 3e-4 re-stage: flow206 (control) + flow205 (fresh rungs) remote, flow207 local (2026-09-11T16:41Z, docs/strategy/2026-09-11-lr3e-4-restage.md)
- Only lr changes (0.003 → 3e-4) vs the retired arms; Adam's lr is the sole step-length control (train.py:4974), no schedule/warmup; stall/recentre clear adam_t so the first step after a clear is lr, not 3.16×. flow204b's LR override refuses > 3e-4.
- Weight decay is NOT lr-scaled (upd = (1−wd)·step): at lr 3e-4 the wd pull (1.6e-3/gen, coherent) exceeds the 0.023 isotropic walk over 300 gens (−3 % ‖θ‖). Left at 1e-4 for a one-variable test; if records read as B uniformly shrunk → companion arm at wd 1e-6. Never move wd and lr together.
- Expectation (§59/§60): level records, not gains; the test is whether the in-sample decline stops. flow204b/flow203b staged, not launched.

## 62. Alpha falsifier: noise walk NOT falsified; shortening a record direction does not rescue it (2026-09-11T16:49Z, docs/strategy/2026-09-11-alpha-falsifier.md, S/alpha/)
- Best α 1.0 in-sample read +107 t 0.6 (flow201_g140); four of six records −466…−646 at t −3.1…−3.8; no cell reaches +300 at t ≥ 2. §59 stands.
- Shape: cliff, not slope — α 0.03 is behaviourally B (0-2 flips, Δ ≈ 0) while α 0.1 already carries the full loss (worst cell for 3/6 records). A lr cut is therefore NOT predicted to rescue a direction; the lr-3e-4 arms are judged only as fresh arms (in-sample decline stops or not).
- Pre-rank: unscaled in-sample Δ vs pooled hold-out Δ Pearson +0.85 (n 6); scaling destroys the ordering → screen records UNSCALED (206 episodes, ~2 min CPU) before any engine leg.

## 63. SWITCH0: one dense day-0 switch at radius 0.003 from B; B is on the good side; no gene carries it (2026-09-11T16:49Z, docs/strategy/2026-09-11-day0-switch.md, S/switch0/)
- One switch (crossings' Δ vectors correlate +0.87 TOPB2 / +0.65 LIVE-C vs +0.27 for non-crossings). Crossing costs −1,774/board on TOPB2 (28/40 lost, none gains) and −74/board on LIVE-C where it is a coin flip (58 gain / 62 lose, best +3.6k) → no board-independent lever; a board-CONDITIONAL choice would be worth ≈ +530/board on LIVE-C.
- λ ladder on the σ0.01 minus ray: moved % = 2.5, 2.5, 17.5, 17.5, 100… at α 0.0025…0.075 → switch radius ‖θ−B‖ ∈ (0.0023, 0.0035). One coordinate moving by one lr (0.003) IS the radius; the trainer step R 0.23 is 67-100× it; even lr 3e-4 (‖δ‖ 0.023/gen) crosses every generation; σ 0.02 members cross with probability ≈ ½.
- Dense: zero coordinates separate 14/42; separator energy per block = block share of live coords; freeze mask is EMPTY by measurement. --train-only exists for whole blocks; S/switch0/trainer.patch adds @mask.npy (not applied, no mask worth passing).
- Consequence: at B the smooth region is smaller than any useful ES step at any σ/pop/lr. Routes: (i) NAME the decision (two runs still executing: S/switch0/only_topb2.log, S/topledger switch0_{B,X}) and make it robust — recentre B a margin off the knife edge along the switch normal, or set the planner tie-break explicitly; (ii) board-conditional side choice as a planner rule (LIVE-C +530/board); (iii) discrete engine-judged search over switch sides, not κ-driven ES.

## 64. SWITCH0 NAMED: the 11th day-0 wheat tile; carried by the encoder + global head blocks (2026-09-11T16:55Z, docs/strategy/2026-09-11-day0-switch.md §SWITCH0-B)
- Day-0 ledger diff B vs crossing theta on 6/6 TOPB2 boards, identically: planted 19→18, WHEAT tiles 11→10, idle 0→1, money +10; opponent rows bit-identical → not the pump, not denial. B plants the tile; skipping it costs −1,774/board on TOPB2 by d29 (28/40 games), coin flip on LIVE-C.
- Block-only screen (one PO.SHAPES block moved at a time): w1, g1, g2 each flip 6/6 boards with byte-identical damage; dh 2/6; all 27 other blocks 0 coins → a subspace, not a step length; §63's "dense/no gene" is corrected. The three blocks share only the global head output → the switch is a threshold on one decoded head value (prior: head[1] land bias in coins). gb2 ±0.3 single-gene screen crossed many ties (90× the radius) and names nothing; all five live head biases sit within 0.3 of a discontinuity; fine ladder δ 0.002…0.05 + the day-0 row fingerprint is the identification method (in flight).
- Freeze mask rewritten = w1+g1+g2 (3,648 coords, 54 % of the theta), usable today via --train-only, NOT recommended (freezes encoder + head; removes one tie of an uncounted number). Radius (0.0023-0.0035) vs step 0.23 unchanged: the smooth region at B is smaller than any ES step.
- Route: name the head output, then recentre B by moving ONLY that head bias a margin onto B's side (play unchanged, population stops crossing) — the recentre agent's Test 2 decides; census of other ties along random rays before any ES relaunch.

## 65. OPP_FRONTRUN design: GO for one switch leg, front-running their row is dead, ORDER within the day is the lever (2026-09-11T17:03Z, docs/strategy/2026-09-11-oppsell-design.md, S/oppsell/)
- Observability: the hour is unobservable (DayView built once at dawn); the DAY is inferable to the unit from mkt_inv deltas (sales +1/u, buys −1, deterministic town tick) — the tree already does this at plan.py:1729 for the pump; view.opp_commit tells which products are theirs. One optional mkt_inv_prev field (4 lines) for phase 2.
- Cadence (6,383 rows, 30 pinned tapes, d15-29): no cadence — every tape sells every late day in ~23/24 hours; 449/450 tape-days open with a SELL at h0-2, before our first turn → "step in front of their row" is DEAD. But 45 % of their units land h18-23, after our lot 3; 131 u/day after our lot 1.
- Mechanism: mkt_inv is a monotone stock with no intraday recovery (town drain ≤ 8-16 u per tick) → ORDER is the whole lever. Our 40 u ahead of their 30: WOOL +3,125, MILK +2,347, STRAWBERRY +2,215 per pot, symmetric on their side. Priced: lot 3→lot 1 +2,254 c/day, sell-vs-carry overnight +4,120 c/day vs a 1,250 c/day target on their revenue.
- Patch S/oppsell/plan.patch (+163 lines, plan.py only, NOT applied; constants, theta decodes byte for byte): OPP_FRONTRUN_ON with two halves — frontrun_inv adds a measured per-product day vector to the LATE lots only (lot 1 untouched, so best_adj stays bounded below by the true lot-1 marginal and the allocation shifts instead of shrinking = the OPP_SUPPLY failure fixed), frontrun_hold charges the overnight reservation price(inv) − price(inv+NIGHT) on today's real pot.
- Test: 5 arms (identity, each half, both, half dose) on the screen first, then TOPB2 → H30/H30B → LIVE62 vs B. TOPB2 + fresh ten are the FIT set for the vectors → LIVE-C is the only honest read. Falsifiers: d_ours ≤ d_theirs (two-purse), our late units falling (the OPP_SUPPLY/EARLY_SELL-B failure mode), a win only at SCALE 50 (tuning artefact). Kaggle scores wins: PASS needs flips, not margin.

## 66. SWITCH NAMED at the code line; recentre refuted; the lever is a planner defect (2026-09-11T17:08Z, docs/strategy/2026-09-11-switch-named.md, S/switch0/tie.py, S/recentre/)
- Decision: brain.py:624 animal_count = _qfloor(animal_share·n_dev). At B the product is 6.991294 vs the floor boundary 6.999900 (gap 0.0086; ‖∇θ‖ 31.9 → perpendicular radius 0.00027, along E3b's ray 0.0024 = inside the measured bracket). The crossing theta WANTS a 7th animal it never buys (herd identical every day); plan.py:4373 _seed_room reserves a tile for max(a_want, a_have) before the purse prices anything, and plan.py:4667 clips the 11th wheat seed out. Opponent rows byte-identical.
- Recentre REFUTED: along −∇ B's day-0 plan holds only to c ≈ 0.012, then the next tie (n_dev 28.69 → 29, brain.py:622) fires by 0.02; c = 0.02/0.05/0.1 flip 100 % of boards on both families (TOPB2 −84/−3,065/−16,517; win 71.7 → 4.2 %). B_0.1 is smooth (0/8 randoms cross) and plays at 5 % — never stage an arm from it. B sits in a cell ~0.012-0.02 wide bounded by MANY floor ties; there is no margin direction.
- Lever (planner, board-independent): purse-aware _seed_room — do not evict a wheat tile for an animal the day cannot buy → plants 11 wheat on both sides and REMOVES the switch. Build + paired screen + engine legs with the two-purse displacement check (dispatched 2026-09-11T17:08Z).
- ES consequence: the decode's floors make fitness piecewise constant in cells narrower than one member perturbation; a "pin the integers at B" mode (hold the decoded integer quantities at B's values as constants, ES only on the continuous remainder) is the smoothing to test, after a census of the ties tie.py records (dispatched 2026-09-11T17:08Z).

## 67. TIE CENSUS at B: 68 discretisations, 46 within σ 0.02; no population member decodes B's plan; pinned mode designed (2026-09-11T17:27Z, docs/strategy/2026-09-11-tie-census.md, S/ties/)
- 55 floor entries + 5 absorb thresholds + 8 argsort keys (+ land_ok). Radius gap/‖∇‖: ≤0.003 → 33, ≤0.01 → 41, ≤0.02 → 46, ≤0.1 → 56; six fields have exactly zero gradient (press ×5, animal_defer; dead behind max(tanh,0)). §66 to the digit: n_dev 28.686 vs 29 (r 3.4e-3), animal_count 6.9913 vs 7 (r 2.7e-4).
- Correct flip scale is σ (∇·σε ~ N(0, σ²‖∇‖²)), not ‖σε‖. Cells per member: σ 0.02 → 33.9/55 floor cells and 27.4/42 Macro integers flip; 0/64 members decode B's plan; σ 0.005 → 25/55, still 0/64. ×~60 decisions per game ⇒ ~10³ cell draws behind one fitness number. §59 mechanism CONFIRMED.
- Macro (the whole theta→plan interface) is 42 integers; "pin every integer" leaves zero genes. Usable split: 12 coarse fields (tiles/hands/days; 429 genes) pinned via KAGG3_PIN_INTS=<npz> (S/ties/brain.patch, unapplied; env unset = inert, verified), 30 coin-scaled fields (6,360 genes) free. Soft/straight-through decode REJECTED (cannot play; breaks sim-equals-engine).
- GO: pinned one-step test at B (σ 0.02, P 512/2048), directions restricted to the free subspace, self-check B-pinned = B to the coin; PASS = κ ≥ 0.03 and antisym +d win on both legs at α 0.1/0.03 and +d beats ≥ 12/16 randoms; NO-GO falsifies ties-as-the-binding-constraint → shop re-roll or seat. Any pinned-trained theta must replay UNPINNED and reproduce B's counts before a judge leg. Local flow207 stopped for it (2026-09-11T17:27Z).

## 68. OPP_FRONTRUN phase 1: LEVEL, refused (2026-09-11T17:47Z, docs/strategy/2026-09-11-oppfrontrun-engine.md, S/oppsell/)
- Identity byte-exact OFF and at SCALE 0. Screen: inv-half A1 TOPB2 +191, LIVE-C +285 t 2.7 (dtheirs −719); hold-half A2 refused (LIVE-C −179, hands them +76); both/half-dose diluted A1.
- Engine A1 vs B: TOPB2 +223 t 0.7 (0/1) | H30 +247 t 1.6 (2/0) | H30B +250 t 1.7 (0/2) | LIVE62 −365 t −3.4 with dours −633 < dtheirs −268. Pooled LIVE-C +248 t 2.3 but wins 44/60 → 44/60. Moves flat (shifts, does not shrink). A4 half dose: +38 / +181, 0 flips → monotone dose response: real lever, too small.
- Ledger: their d15-29 c/u falls only 0.5-0.8 (99.0→98.5, 61.1→60.3) vs a 16 c/u target; on B's LOSS boards d_ours −806 < d_theirs −699 (two-purse falsified where it matters); our late c/u never rises.
- Closed on B. Only phase 2 (mkt_inv_prev per-board inference firing on loss boards) could reopen it; expectation low given the 0.5 c/u movement.

## 69. SEED_ROOM_PURSE_ON: the day-0 tie's damage removed, B untouched, engine-confirmed (2026-09-11T18:06Z, docs/strategy/2026-09-11-seedroom-fix.md, S/seedroom/plan.patch 79128386)
- First shape (purse bound inside _seed_room) inert: the 7th animal is affordable in isolation, unaffordable only against the wheat/seed the greedy ranks above it. Shipped shape: after BUD.grant, re-derive the seed room from animals actually bought (a_have + a_got) and re-solve the seed lists with the leftover coins (PLANT_FILL's second-walk machinery). Default OFF.
- OFF byte-identical to B (0/160 screen rows). Crossing theta: TOPB2 −3,548 → −1,779 (+1,769/board, t 4.2; 85 % of the switch gone), day-0 row 18/10/1 → 19 planted / 0 idle. B ON vs OFF: byte-identical on 160 screen rows and every ledger day; engine 284 games all ties (0 flips, dmargin 0).
- ES implication: the E3b crossing set does NOT collapse (13/14 still cross; mean penalty −1,111 → −783): the animal_count tie was one leg of the cliff. Keep OFF in the shipped tree; turn ON for training arms (free for B, removes the largest day-0 discontinuity). Not promotable on its own (no coins for B); it is infrastructure for the search.

## 70. WALL IMITATION: the planner reproduces the wall's opening to the tile — and loses 24k/board (2026-09-11T18:35Z, docs/strategy/2026-09-11-wall-imitation.md, S/wall/)
- Tool: KAGG3_PIN_INTS extended (private tree) to literal per-day Macro tables (sentinel −999 = keep) → any "what if the planner did X on tiles/animals/hands/timing" is a 12-min engine-exact screen.
- (a) With plant_target d0 = 7 W + 12 M, the wall's animal buys and hires (5,3,4,5,4,4,… 21 by d4), B plants 7 wheat + 12 melon, holds the plate to d9 and cuts all 72 melon units on d10 — the clone's 72. The planner CAN execute the wall's opening (planner-ceiling-B confirmed; the incumbent theta simply never decodes it).
- (b) Paired vs B on the honest unit: joint −24,209/board t −8.7 (TOPB2 30 → 5 %), Δours −4,717 / Δtheirs +19,492; planting-only −21,214; labour-only −580 (level, free); full d0-12 plate −27,687; + MIDDAY_PLACE_V2 −30,667. Joint is 3k WORSE than the melon piece alone → jointness was not what the prior forcings were missing. (c) LIVE-C −31,417 (71.7 → 1.7 %).
- Mechanism: the d10-14 gap closes (18.7k → 16.9k) and the season is then lost by 44.6k over d15-29, +21.4k of it in THEIR purse (their d29 purse 90.5k → 111.8k; our cows d20 6.3 → 3.0; season units 1,446 → 1,251). Our 11 wheat + 8 carrot opening is a DENIAL asset, not a deficiency; "move d10-14 income" (residual-loss20 §5) is falsified as a target. Residual execution gaps are real but secondary: pot banks 153/u vs their 198 (≈3.3k), budget.grant refuses cows from a plate-drained purse (2.7 vs 4.7 at d7), idle tiles d5-9 9.6 vs 1.6.
- Consequence: the wall's program is NOT the target; B's configuration is a local optimum of a different kind (deny their late purse). Next: direct coordinate search over B's OWN coarse integers with the per-day pin tables (codex c), screen-ranked on development boards, engine-confirmed on held-out legs.

## 71. Web research: ES through floors — our regime is σ TOO LARGE for the lattice; three remedies (2026-09-11T18:36Z, docs/strategy/2026-09-11-web-es-floors.md)
- Mixed-integer ES literature (Hansen 2011; CMA-ESwM 2022; LUB-ES / Hamano-Uchida-Shirakawa 2026) treats σ too small vs granularity; ours is the mirror image: with p_mut ≈ 0.8 per tie and ~42 ties per decision, p_succ = (1−p_mut)^d ⇒ 0/64 members decoding B's plan is PREDICTED. Rank shaping / mirrored sampling / sigmoid(margin) create no signal on a staircase (NES 2014; Brockhoff 2010). Population needed ≈ K·(sd/Δ)² with K ≈ 34 × 60 → 3-4 orders above 512.
- Remedy 1 — DITHER the decode in fitness evaluation only, ship the plain floor: ⌊x⌋ → ⌊x+u⌋, u ~ U(0,1) as a common random number shared by the antithetic pair (Lipshitz 1992; LOTION 2025 Lemma 2: grid minima preserved). E[F] becomes piecewise-linear in the decoded value; plays integers; no backward pass; bit-identical when unset. NOT the §67-rejected soft decode. Largest-remainder blocks dither jointly; argsort keys via Gumbel. Test = KAGG3_DITHER shim + the one-step rig at the pre-registered κ ≥ 0.03 bar (~2 h GPU).
- Remedy 2 — per-block σ so the expected flip budget Σ 2Φ(−r_j/σ_j) is 1-3 per decision (the formula reproduces the measured 33.9 at σ 0.02); equalises the 2,000× gradient spread across blocks. CPU solve in census.py then the one-step rig. If the solved σ lands inside the α 0.03 "behaviourally B" shell, ES over this parameterisation is CLOSED — a clean falsification either way.
- Remedy 3 — race the 12 coarse integers (24 arms of ±1 through KAGG3_PIN_INTS, CRN screen, successive halving, Holm-corrected → engine leg): ParamILS 2009, irace 2016, "round inside the model, never search inside a cell" (Garrido-Merchán 2020). = the ISEARCH stream dispatched 2026-09-11T18:36Z.
- Also: mirrored pairs carry per-tie signal we average away — attribute each pair to the ties it straddles and estimate 68 scalars, not 6,789 coordinates. Depth-over-fidelity inverts above ~0.12 misranking (ours ~0.5): more boards / tighter CRN beat more generations.

## 72. Web research: Adam walk — the gradient at B is NOT zero-mean; it is dimension-limited (d ≫ P) (2026-09-11T18:37Z, docs/strategy/2026-09-11-web-adam-walk.md)
- New measurement from the saved E3 draws: the DISJOINT-draw cosine g_rem = (1024·g2048 − 256·g512)/768 vs g512 reads +0.039 at σ0.01 (3× the 1/√n null 0.013), +0.024 at σ0.02, +0.016 at σ0.04. +0.039 equals the noiseless dimension-limited value ρ = P/(P+d) = 256/6253 = 0.041. The shared-prefix statistics of §60 (cos 0.53, ‖g‖ ratio 2.0) cannot distinguish zero-mean from dimension-limited; §60's "zero mean gradient" reading is CORRECTED: a real but tiny-SNR gradient exists, CRN leaves almost no evaluation noise, and the binding constraint is d = 5,997 ≫ P = 256 pairs (plus the lattice noise of §67/§71).
- Adam's update is ≈ lr per coordinate regardless of ‖g‖ (Kingma-Ba §2.1) → the walk; ARS rejects ranks+Adam for this reason. Our weight decay is (1−wd)·step, not lr-scaled → at lr 3e-4 the coherent decay pull (1.6e-3/gen) is 8× the 2e-4/gen signal: flow205/flow206 will measure "B shrunk", not "B moved". Under our form wd must scale as lr².
- Remedies, ranked: (1) cut d before lr: --train-only to ~1,000 genes gives ρ 0.04 → 0.20 (5× SNR at equal compute; ARS 2018, Choromanski 2018, Nesterov-Spokoiny 2017) — test = per-block disjoint cosine vs P/(P+d_block) on the saved .npy (10 CPU-min, dispatched 2026-09-11T18:37Z); (2) --optimizer sgd (exists) with a ‖g‖-proportional step: lr ≈ 1.3e-4 puts ‖δ‖ ≈ 0.001 inside the 0.0023 tie radius, wd scaled as lr²; (3) per-generation SNR gate: split-half cosine, skip/scale the step below 3/√d = 0.039, plus the CSA path scalar; (4) block-elitist acceptance against the engine-exact screen every 10 gens. Not recommended: Adam moment reset, more episodes per board, larger σ, AdaBelief/large-ε Adam (= automatic lr cut).
- Recipe for the next arm (after the block test): train-only on the signal-carrying blocks, sgd lr ~1e-4 with wd ∝ lr², SNR-gated steps, elitist screen acceptance, dither-in-evaluation (§71) — every element measured before launch.

## 73. BLOCK-SNR: per-block gradient signal on the saved E3 draws — no block survives multiplicity; leaders = the cliff (2026-09-11T18:52Z, docs/strategy/2026-09-11-block-snr.md)
- §72 reproduced exactly (+0.0386/+0.0236/+0.0159 at σ 0.01/0.02/0.04). Better estimator: g lies in the eps row space, so per-pair advantages recover by least squares (resid 9e-8) → truly disjoint remainder cosine +0.041/+0.028/+0.033, sign-flip null sd 0.0133 = 1/√5997.
- Two corrections to §72: (1) ρ for 256-vs-768 pairs is 0.068, not P/(P+d) = 0.041, so measured/predicted = 0.60/0.41/0.48 → effective dimension 10–16k vs d 5,997: evaluation noise is still ≈1× the dimensional noise ("no eval noise after CRN" withdrawn). (2) "signal falls with σ" was an artefact of the shared-pair residual.
- Per block: NO block survives multiplicity (90 tests, max |z| 2.81, Bonferroni p 0.45); energy is isotropic (1.00 ± 0.05 for every block ≥ 64 genes). σ 0.01 leaders g1/gb1/g2/gb2/g5 are EXACTLY the SWITCH0 day-0 cliff subspace (§64/§66) and their cosine collapses 1/σ (g1 0.097→0.040→0.007) = a smoothed step, not a slope. gp and dh sit outside the switch subspace, fine-decode, flat/rising in σ = slope signature.
- Recommendation: `--train-only gp,dh,ds,g5,gb5,w3,b3,b1` (d_train 1,191 = 19.9 % of live), lr 1.8e-4 at σ 0.01 (sgd, ‖g‖ 47.5 on the subspace, ‖δ‖ 0.002), wd 4e-7 (∝ lr²). Not g1/gb1/g2/gb2 despite ρ 0.094: that is the cliff and belongs to engine-judged side selection. Honest risk: the whole gain rests on 1.4–2.8σ cosines from ONE eps draw; 1.2–1.7× is not a fix for a 4 % estimator; raising P 512→4,096 buys 8× and composes with it.
- Decision: the next arm = train-only on that block list + sgd + P 4,096 (rungs halved to fit) seeded TWICE (B on GPU0, hr = flow172_g1000_pair on GPU1, user's ancestor question), replacing flow206/flow205 once the dither one-step test on the 3070 has read out. Settling test before launch: rebuild both draws from the 42 non-crossing pairs and re-read the per-block cosines (S/snr/blocksnr.py supports it).

## 74. CODEX BLIND REVIEW 1: is the gene set enough? — gene count ranked last, action interface first, three decoder defects (2026-09-11T18:52Z, docs/strategy/2026-09-11-codex-blind-genes.md)
- Provenance: gpt-6-astra, read-only, given the question + code pointers only (no diagnosis, no prior briefs). It reviewed the MAIN checkout src/ (4,980-gene policy.py); the arms use .claude/worktrees/arms-next (6,789). Review 2 on arms-next is running; §74 records only the claims that do not depend on the layout.
- Verdict: gene COUNT is the least likely bottleneck (rank 4); rank 1 = the action interface (one Macro per day; sell = one reservation + one linear lot pressure per product, fixed product order, no intraday branch on the opponent's dump); rank 2 = fixed planner logic (purchase valuation, mandatory maintenance tiers, hire admission); rank 3 = observation (no hour/history, opponent crop ages absent, t_yield carried but unused).
- Defects it reproduced: (a) `_largest_remainder` tie-break key -(frac·2n + (n−1−i)/n): the index term (≤0.8) dominates fraction differences < 0.08 → plant_target among near-equal crops is decided by crop INDEX (confirmed here: [.19,.20,.20,.20,.21] total 1 → [1,0,0,0,0]); (b) CREW_TARGET_PUSH 400 < marginal hire 987 → crew_target cannot force a hand (g10 block partially dead, consistent with §73's weak g10); (c) terminal liquidation / overflow forced sales discard the learned hold. Audit + binding-frequency count on B dispatched (CODEX-DEFECTS).
- Review 2 (18:58Z, arms-next, fresh session): REPRODUCES review 1 on the right tree — same ranking, same three defects ([.30,.32,.38] → [1,0,0]; push 400 + bias 400 < 987; forced sales drop hold), plus one new cap: the market-curve feature columns are DEFAULT_MARKET_PARAMS constants, not observed (brain.py:25/539). 792 dead / 5,997 live confirmed; ≥288 redundant directions from duplicated inputs.
- Its first parameterisation change: replace the linear lot pressure with independent signed offsets for lots 2 and 3 (+65 genes, exact baseline (−press, −2press) retained), freeze the rest, train only that head. Our record says every HAND sell-timing lever moved margin and left wins level (§65/§68, wool family), but a 130-gene head trained from B is a d=130 arm (ρ ≈ 0.8) and the cheapest learnable test of "genes not enough" we have. Queued behind the §73 arm; falsifier = the standard paired legs.

## 75. DITHER + PER-BLOCK σ staged: block-σ lands INSIDE the do-nothing shell, only the dither arm deserves the card (2026-09-11T18:56Z, docs/strategy/2026-09-11-dither-staging.md)
- Remedy 1 (dither, S/dither/brain_dither.patch, unapplied, live only in /root/tree_dither): `KAGG3_DITHER=<seed>` adds a CRN uniform field keyed by (site, day) only — no theta/member/pair/episode/board in the key (signature-asserted), so ± members share the field; `_largest_remainder` dithered as a block by systematic apportionment (sum exact), `forward_days` half replaced not added. Tests all pass: E[⌊x+u⌋]−x ≤ 5e−4 at 1e6 draws, block sums 6,000/6,000, numpy == jax on 15 sites × 30 days, and INERT unset (B's Macro identical on 240 decisions × 42 ints).
- Remedy 2 (flip-budget σ_b): σ_b = min(c/G_b, 0.02) from the measured gene→gap slopes; 11 blocks at the cap, 7 dead at this obs; 37.5 % of members decode B exactly (vs 0/64 at σ 0.02). But the resulting step ‖σε‖ over the binding blocks = 0.045 (budget 1: 0.032), which is INSIDE the α-falsifier's do-nothing shell (0.026–0.085 at α 0.03, §58). The σ that keeps the plan intact is the σ that does nothing → ES over the unchanged decode is closed by the literature's own bound; only a DECODE change (dither) can open it.
- Decision: run S/dither/run_onestep_dither.sh on the 3070 as soon as the pinned replication cell exits (auto-chained); block-σ and combined scripts stay staged. Bar pre-registered: PASS = κ ≥ 0.03 and +d beats ≥ 12/16 randoms on both CPU families and all 4 permuted controls, antisymmetric, at α 0.1 or 0.03; NO-GO at κ ≤ 0.015 → the coarse-integer race (ISEARCH), not another σ.

## 76. ISEARCH: B is a strict local optimum in its own integer lattice (radius 1–2), 8/24 edits are slack, one melon tile at d0 costs 14k (2026-09-11T19:00Z, docs/strategy/2026-09-11-integer-search.md)
- Method: `KAGG3_OFF_INTS` offsets relative to B's decode (clip(B + off)) in /root/wt_isearch; 25 variants in ONE XLA compile via a spare theta slot; variant 0 reproduces S/wall/t2_base.csv to the coin on all 40 boards. Screened on TOPB2 (40) and LIVE-C 43-72 (30), engine-exact sim.
- Result: 0/24 edits gain > 302 coins on either family; the best per family (c13p1 +302 TOPB2, crw59p1 +22 LIVE-C) is negative on the other → no finalist, hold-out unspent, engine legs written but not run.
- Landscape: 8/24 edits move ZERO coins on every game although the decoded Macro changed — the want is slack where it is not executed (carrot want 11 vs 8 planted; tomato/straw lose the priority contest; crew_target decodes 0 on d0-d5 so it is not the hiring channel; animal defer clipped at 0; cow+1 ≡ sheep+1 board-for-board). This is the d0-d5 face of §74's "crew target unenforceable" and of the dead/slack gene picture.
- Biggest single number: m0p1 (one melon tile at d0) = −14.4k/−15.1k, win 30→10 % and 63→7 %, of which +11.0k goes to THEIR purse — B's d0 basket is a denial asset priced through the opponent (hypothesis: an 80-coin melon seed against ~150 coins of d0 slack shortens OPEN_PUMP's 53-wheat buy). The melon dose curve has no gentle start.
- Consequence: §75's NO-GO fallback "→ the coarse-integer race" is closed BEFORE the dither read-out: radius-1/2 integer moves at B do not gain. If dither is NO-GO, the remaining moves are new decision dimensions (LOTS head §74, in build), the §73 slope-block arm, or a different seat/objective — not the lattice around B.

## 77. PINNED-E3 NO-GO: with the 41 integers pinned the noise falls 20×, and there is STILL no gradient at B — two draws are orthogonal (2026-09-11T19:07Z, docs/strategy/2026-09-11-pinned-onestep.md)
- Rig: /root/tree_pinned + S/ties/brain.patch, KAGG3_PIN_INTS=S/ties/pin_B.npz; B pinned reproduces B unpinned 10/10 byte-identical on TOPB2. Freeze set 429 coarse-only genes (panel-confirmed over 12 obs), free subspace 5,568 of 5,997.
- Positive: the pin kills the cell lottery — 0/8 randoms move 100 % of boards (E3b unpinned 5/8), random signed-gain sd 107→4 (LIVE-C) and 977→44 (TOPB2), antisym sd 184→6 / 1,527→84. The ±25k the arms average over is NOT the integer cells.
- Negative: σ 0.02 P 512 eps 9001: κ 0.027 (obj_w α 0.1), never ≥ 0.03, +d LOSES at every α (margin −22); engine-exact pinned screen −2/−196 at α 0.1, antisym negative, beats 0/8 randoms and 0/4 permuted controls. Replicated at eps 9002: κ 0.012, +d loses again, and cos(d_9001, d_9002) = +0.014 vs null 0.013 → the ES direction at B is not a reproducible feature of the objective even with the lattice removed.
- Consequence: do not re-cut a pinned arm; another σ/pop/lr/freeze set is not the move. Together with §76 (lattice closed) and §73 (no block survives), the remaining levers are: a decode change (dither, running), NEW decision dimensions (LOTS head, in build), the shop re-roll (§ shop lottery), or a changed seat/objective.

## 78. CODEX-DEFECTS audit on B: tie-break binds 6 % of board-days (wheat takes one tile), crew push covers hands ≤14, forced sales are the law, observation claim mostly refuted (2026-09-11T19:12Z, docs/strategy/2026-09-11-codex-defects.md)
- Claim 1 `_largest_remainder` index tie-break: VERIFIED (brain.py:850, index term 0.8 vs frac·2n). On B (10 TOPB2 boards × 30 days): 18/300 board-days have a tile placed by crop index, exactly 1 tile each, all d3–d15, one-sided — WHEAT takes all 14 plant tiles from STRAWBERRY (8) / MELON (4) / CARROT (2); 4 animal cases. Fix staged (S/defects/fix_tiebreak.patch, index term ×1e-6) and its paired engine legs vs B LAUNCHED (S/defects/engine.sh all, tree /root/wt_defects). Result (19:23Z, paired vs B): TOPB2 −488 t −1.35 (10/40 boards changed, wins 13→12), LIVEC-H30 +20, H30B +24 (−2 wins), LIVE62 −192 t −1.21 (+2 wins) → LEVEL. B does not lean on the bug, and correct rounding gains nothing; the fix is not shipped and not put into the B-seeded arm trees (it reads −488 on TOPB2 at the seed). Kept staged for a from-scratch arm.
- Claim 2 CREW_TARGET_PUSH 400: VERIFIED but narrower — HIRE_COST = fib(n), so 400 covers every hand through the 14th (377), not the 15th (610)/16th (987); crew_target > enumerated hires on 46/300 board-days (15 %, mean 1.1 hands, d11–d20); HIRE_ROW_ON already clamps intent on 50 % of days. Not a d0-d5 channel (§76).
- Claim 3 forced/terminal sales: VERIFIED and by design (d29 liquidation, shed overflow): d25–29 ≤85 % of units not hold-governed; B's hold there ≈ 9 coins. No test.
- Claim 4 observation: MOSTLY REFUTED — features() ignores t_yield but decide() feeds board_forecasts with own AND opponent t_day/t_yield (B's fh/fs/fv blocks 100 % non-zero); no hour/history is by design (one decide per day).

## 79. flow209 (seed B) / flow210 (seed hr) STAGED on the §73 recipe; the settling test cannot clear the block list (2026-09-11T19:40Z, docs/strategy/2026-09-11-flow209-staging.md)
- Launchers S/flow209/launch_flow209.sh (md5 3d2df5f0, GPU0, seed flow193_g100_hr) and S/flow210/launch_flow210.sh (md5 87a7cba6, GPU1, seed flow172_g1000 = the shipped hr theta, verified against the tarball), byte-derived from flow206: `--train-only gp,dh,ds,g5,gb5,w3,b3,b1` (d_train 1,191 measured), `--sigma 0.01 --optimizer sgd --lr 1.8e-4 --weight-decay 4e-7` (pull 0.11 % of the step vs 28 % at flow206), `--pop 4096` with rungs unchanged (chunk-bound memory; cost = 8× wall-clock per generation). No SEED_ROOM_PURSE_ON flag exists in the trainer; both scripts guard busy GPU / missing theta / existing log. Not launched.
- Settling test (§73's "rebuild from the 42 non-crossing pairs"): its instrument does not exist — the census labels step directions, not eps pairs; 0/1,024 pairs preserve B's day-0 Macro at any σ. Under the narrow wall label the §73 blocks and the cliff blocks are indistinguishable (cos/ρ 0.63 vs 0.66) and gp/dh flip sign at σ 0.02. So the block list stands on §73's 1.4–2.8σ cosines only.
- Decision: launch flow209/flow210 only after the dither read-out (a PASS adds KAGG3_DITHER to both launchers; a NO-GO launches them as staged, since they are the last optimiser-side lever with any measured signal); they replace flow206/flow205.
- Incident: the staging agent's stray `ln -sf … /dev/null` took the session's shell down 19:29–19:37Z and killed the first dither hold-out (relaunched 19:37Z). Rule added to every agent prompt: nothing under /dev is ever a target.

## 80. DITHER NO-GO: the dithered decode opens no held-out gradient at B (2026-09-11T20:14Z, S/dither/sweep_dither.txt, docs/strategy/2026-09-11-dither-staging.md)

E3c one-step test on the 3070, KAGG3_DITHER decode (dither=20260911), σ 0.02, pop 512, eps seed 9001, pre-registered bar (§75): PASS only if at some α ≤ 0.1 on the HELD-OUT block (LIVE-C 43-72 × 2 seats) +αd gains on both obj_w and margin, antisym beats ≥ 6/8 random pairs AND 4/4 permuted directions. Result: α 0.1 obj_w −0.00165 (antisym −0.0008, 6/8 randoms but 2/4 permuted), margin −107 (+d loses, 7/8, 3/4); α 0.03 obj_w −0.0248, margin −910, 0/8 and 0/4 everywhere. Only α 1.0 (diagnostic, the cliff) reads +0.076 / +1,591 with 8/8 and 4/4, exactly the day-0 switch artefact §56 identified. κ at α ≤ 0.1 ≈ 0 < the 0.015 NO-GO line. The first, aborted in-sample draw (α 0.03 +0.0088, 8/8, 4/4) was the eps aggregate on the training block and does not transfer. VERDICT: dither does not open the lattice; it is not added to any launcher. §79 stands: flow209/flow210 launch as staged, replacing flow206/flow205. Remaining levers: new decision dimensions (LOTS, §81), shop-draw CRN for the drawn rungs (§82), seat/objective change.

## 81. LOTS STAGED: two signed per-product sell-lot offsets, 130 genes, inert on B, slope 27 % at σ 0.01 (2026-09-11T20:14Z, docs/strategy/2026-09-11-lots-build.md, S/lots/)

Codex's blind review (§74) ranked the sell interface first: one hold + one linear press per product. LOTS appends block ("lots", (65, 2)) = 6,789 → 6,919 genes, decode off = round(8·z) clipped to ±COIN_CAP on lots 1 and 2 (lot 0 pinned; a common offset is hold). Inertness 20/20: candidate B padded decodes byte for byte (300 decisions × every Macro int + 3 self-play seasons, 19 arrays, 0 diffs). Slope: 27.3 % of 2.2 M cells move ≥ 1 coin at σ 0.01 (per-board p10/p50/p90 0.23/0.27/0.32; gene-slope rule satisfied, unlike flow151). Launcher S/lots/launch_flow208.sh (md5 749f7a85): --train-only lots, sgd lr 2e-3, wd 0, patch S/lots/policy_lots.patch (db2fe4ef) against arms-next. Deviations: Macro.lot_off is int[3,9]; init zeroed. Flags: test_backend_agreement fails identically in untouched arms-next (hire_bias numpy 33 vs jax 32 on a 4,848 theta) — pre-existing; the judge toolkit hard-codes 6,789 and must pad before it can judge a flow208 record. Queue: flow208 takes the first free GPU after flow209/210.

## 82. SHOP-DRAW CRN BUILT: the end-of-day shop word is indexed by our tile count; --shop-crn already existed, env face added (2026-09-11T20:14Z, docs/strategy/2026-09-11-shopcrn-build.md, S/shopcrn/)

sim/eod.py: each day's Random((seed·1000003)^day); spawn_weeds eats 2 words per EMPTY tile per seat, so the shop draw's index = our planting (65.6 % of ±1-tile steps change the day's shop; B vs a σ 0.02 perturbation differs on 40/42 boards, 1,038 board-days). --shop-crn (Config.shop_crn, a85b008, unused by any arm) pins the base at word 400; KAGG3_SHOP_CRN env face built (S/shopcrn/sim_shopcrn.patch). Inert unset (coin-exact, 42 boards × 29 days); marginal unchanged (χ² p 0.82, KS p 1.0); fitness level (Δ −2,368, t −0.74); ON → 0/42 boards differ. CAVEAT: pinned-town boards override the draw in unlock_shop, so the treatment only acts on rungs whose shop is actually drawn — count those rungs before costing it. Not launched; S/dither/stage_tree.sh takes SHOPCRN=1.

## 83. JUDGE PAD STAGED + DRAWN-RUNG CENSUS: SHOP_CRN NOT WORTH A RUN (2026-09-11T20:41Z, docs/strategy/2026-09-11-judge-pad.md, S/lots/judge_pad.patch, S/shopcrn/census.md)

- **Judge pad (S/lots/judge_pad.patch, 5,947 B, staged, NOT applied):** the theta's width picks the judge tree and nothing else does. 6,789 → arms-next byte-for-byte (every baseline csv stays reproducible); 6,919 → $LOTSWT (/root/wt_lots); any other width → FAILED, never a guess. Only watch.sh (worktree_for/switches_for arms) and simscreen/screen.py (header-only width reader, KAGG3_WT override, mixed-width hard error) change; every leg runner already takes the tree as $2. test_judge_pad.sh passes on a scratch mirror: padded B (6,919, S/lots/theta_B_pad6919.npy, 130 zero genes) through the LOTS tree is coin-identical to B through arms-next (tape 107463847 seed 4674845: 94698/98435, margin −3737, shop_sig 132). Hazard named: a 6,919 theta read by arms-next is SILENTLY truncated by policy.unpack, every leg looks plausible while judging a different agent. Apply only when flow208 produces a record: stop the watcher, patch -p1, add "flow208 stage_hr" to ARMS, relaunch.
- **Census (S/shopcrn/census.py, live Trainer rung construction on the flow209 recipe):** 178 episodes/gen = 166 pinned tapes (w4 61, w10.2 20, w2 85; weight 1,236 = 99.04 %) + 12 self-play (drawn shop, weight 12 = 0.96 %). Bar was ≥25 % → **SHOP_CRN gets no run**. launch_flow209.sh already passes --shop-crn, a no-op on 99 % of the objective. Consequence: on the pinned recipe the ±25k YARN_STORE re-roll (§82 caveat) cannot be the ES noise floor for the flow209/210 family; whatever floor they show is board-set variance and the cliff, not the shop lottery.
- Decision: SHOP_CRN CLOSED for pinned recipes; judge pad waits for the LOTS one-step verdict (§81 → flow208).

## 84. SNR READER BUILT: the §73 reading rule is re-based on the momentum null (0.51, not 0.029) (2026-09-11T20:51Z, docs/strategy/2026-09-11-snr-reader.md, S/snr/step_cosine.py)

- Tool: `export JAX_PLATFORMS=cpu; python S/snr/step_cosine.py --run flow209 --host user@remote-host --fetch` fetches cands records + log.jsonl + config.json into S/snr/<run>/, derives the trained set from the run's own train_only (1,191 of 6,789 for flow209/210, via train_mask × live_mask), prints block-delta cosines on the trained genes, per-gene-block cosines, and a VERDICT against three nulls.
- **Correction of §73:** Trainer.step (train.py:4754) applies m = 0.9 m + 0.1 g for BOTH optimizers; --optimizer sgd only drops the Adam denominator. Momentum e-folds over ~9.5 gens, so consecutive 10-gen block deltas overlap by construction. Pure-noise gradients pushed through the run's own optimizer and record schedule give the real null: mean +0.51, p95 +0.55 (flow209/210 schedule). 1/sqrt(d) = 0.029 applies only at β1 = 0.
- Calibration on the Adam arms that had no held-out gain: flow201 0.4375 vs null 0.4241 and 0.1561 vs 0.1557; flow200 0.3257 vs 0.3350. Both sit ON the momentum null to two decimals → their steps carried no direction beyond momentum overlap, which is the §59 noise-walk reading measured directly. Untrained genes byte-identical across records (held genes take no decay).
- **Reading rule at g30 (three records, two consecutive pairs):** mean consecutive cos > ~0.55 = PERSISTENT (first evidence of a usable gradient at B; then read which of gp/dh/ds/g5/gb5/w3/b3/b1 carries it); 0.45–0.55 = NOISE; < 0.45 = anti-correlated blocks, lr overshoot. Require ~0.05 margin over p95 before acting (null-mean sd ~0.02 with two pairs). Promotion still only via the paired legs vs B; this reading decides whether the arms keep running or the campaign moves to new dimensions (§81 LOTS).

## 85. EXPRESSIBILITY CENSUS: the hole is the MARKET ROW CADENCE, not the verb set or the gene count; LOTS covers 0 % of it (2026-09-11T20:58Z, docs/strategy/2026-09-11-expressibility.md, S/express/census.py)

- 29 top-tier tapes, 23,806 market rows, 184,309 unit actions, classified against the decoder's row set written down before any tape was opened. Shipped switches: 17.9 % of opponent coin expressible; 78.3 % inexpressible by TIME; order 2.8 %; type 1.0 %. Union over every switch setting: still 49.6 %. Unit actions 93.9 % expressible (96.7 % union): the engine vocabulary is exactly ours (18 unit verbs, 6 market verbs), every discriminator is turn/count/order.
- One family = 81.9 % of the inexpressible coin: sales on turns we hold no lot. Mid-day turns 38.3 %, evening tail 19-23 23.7 %, turn-0 dump 19.9 %. Shops restock every 4 turns = six price windows a day; our lots 1/3/10/18 reach windows 0, 2, 4 with 1 and 3 doubled in window 0. 42.0 % of opponent sell coin lands in windows 1/3/5 we never quote into.
- LOTS (flow208, §81) covers 0 % of this by construction: it re-splits the three lots we already present and adds no turn. Its reach is the 20.2 % of opponent sell coin already on our turns. flow208 stays queued as a cheap block but is no longer the answer to the user's "remake the decoder" question; the measured answer is MORE SELL TURNS (windows 1, 3, 5) and a HIRE row after the morning lot.
- Judgement: order of magnitude closer to 500 points than 50, with the coin figure an upper bound (we sell the same goods; the prize is the price delta between ticks). Caveats: reference pricing not live quotes; 851 dump-all rows priced at zero; only top-tier tapes (the 2200-band clone not measured).
- Coupling found for the falsifier: N_LOTS = len(ops.SELL_TURNS) flows through sell.py and plan.py; SELL_TURNS[-1] anchors TURN_PRESTOCK (20), the DROP-day turn budget, MIDDAY_PLACE_V2_TURN and the day-29 chain, so window 5 needs the prestock row moved; windows 1 and 3 (turns 7 and 14) leave both anchors untouched. Falsifier dispatched 2026-09-11T20:58Z: KAGG3_SELL5 env switch, sim screen then paired real-engine legs at B (see §86 when it lands).
- Side finding: BUY_PRODUCT WHEAT/FERTILIZER-only is the engine's rule (kaggriculture.py:598/606, sha256 bc8a548 verified against vendor/engine.lock.json), not our narrowing.

## 86. LEFTOVER-STORAGE AUDIT: what we leave in the shed is 47 coins/game of fertilizer, never the loss; the fertilizer gap is §57's closed family (2026-09-11T21:04Z, docs/strategy/2026-09-11-leftover-audit.md, S/leftover/audit.py)

- 96 live replays (48 per sub, 24 W + 24 L each, through 2026-09-11T20:40Z), executed sells recomputed engine-exact via scripts/replay_profile.py::_simulate_market. Our end-of-game leftover: mean 52/61 coins (B W/L), 36/39 (hr W/L), max 260, always FERTILIZER only (699 units over 96 games). Unit inventories at the whistle: 0 units in all 96 games (DROP_ON already banks the day-29 harvest). Opponents: mean 18, one holding 1,129 of WOOL.
- Mechanism (ep 107922863): lot 1 at d29 h0 sells the whole shed including the 14 fertilizer; hands then COLLECT 13 more; DROPs bank them; lot 3 at h18 is composed from hour-0 stock so it carries no FERTILIZER row (5 of 10 slots used); turns 19-23 have no market row. Not law, not cap, 100 % lot composition. Opponents mask the same property with blanket SELL-6000 rows on ~15 of day 29's turns vs our 3.
- Upper bound at the final price: 47 coins/game mean, 260 max; covers the margin in 0/48 losses (loss margin mean 5,186, min 99). NOT A LEVER (0.04 % of a game). Free tidy-up (re-offer the shed on the last two d29 turns, 4 idle rows) only if the day-29 decode is opened for another reason, e.g. by the SELL5 work (§85).
- Fertilizer allocation: we collect 388/game, apply 188, sell 200 (10,200 coins); opponents collect 370, apply 66, buy 47, sell 345 (~17,300) → ~+7,100 coins/game of fertilizer revenue over us, identical in their wins and losses. This is the FERT_VOLUME family (§57): the 2/1 cut on B raised margin +400-1,100 on every leg, denial-led (their purse fell), wins level → NOT PASS, family closed by the two-purse rule. The audit sets the family's upper bound; it does not reopen it. Left open for the ES: the fert/apply genes are in the flow209/210 train-only set (gp, dh, ds...), so if the allocation is worth wins the arms can find it.
- Answers the user's question: when we lose, the opponent's storage is almost always empty too (median 0); OUR leftover is one day's collected fertilizer that lot 3 never lists, worth tens of coins; fertilizer is "not used all" because we choose to sell 200 of 388, and selling more (§57) buys margin, not wins.

## 87. LOTS ONE-STEP: NO-GO, flow208 PARKED — the block is reachable but not profitable at B; with §85 it stays off the queue (2026-09-11T21:25Z, docs/strategy/2026-09-11-lots-onestep.md, S/lots/sweep_lots.txt, sweep_lots9002.txt)

- Pre-registered bar (S/lots/onestep_prereg.md, E3c clause 1): +d must gain on BOTH obj_w and margin held-out (LIVE-C 43-72 × 2 seats) at some α ≤ 0.1. Result at α 0.1: obj_w +0.0016 but margin −189; at α 0.03 both negative and every control beats it. In-sample +d gains (8/8, 4/4) and loses held-out = the usual signature.
- Replicate at eps seed 9002: α 0.1 fails identically (margin −161); α 0.03 flips sign between seeds on a near-degenerate control null (r_sd 0.0007); the centre itself drifts 0.0013 obj_w between builds, larger than the gains adjudicated.
- Genuinely new: at α 0.1 the lots direction beats 8/8 randoms and 4/4 permuted-advantage controls on obj_w, win_w and margin held-out (dither managed 6/8, 2/4). But the antisymmetry is carried by −d (−0.0196 / −561), not by +d: the ES can see the block, the block does not pay. flow208's own first sgd step (lr 2e-3) lands at 0.41× the α 0.1 step, inside the flat-to-negative band.
- Protocol: step unit R = lr·√n_live at lr 0.1 (lr 0.003 is decode-inert at d 130; round(8·z) needs ‖δθ‖ ≳ 0.12), so α 0.1 = exactly one σ-perturbation; popcurve.one_draw masks draw/direction/randoms to the block (off-mask ‖g‖ 0). Padded centre reproduces E3's centre (obj_w 0.64928 vs 0.64932, margin 3980 vs 3981) = inert confirmed. κ held-out +0.32/+0.19 is above the 0.015 NO-GO floor but κ at n_live 130 is 6.8× easier than at 5,997 (z +3.7/+2.2).
- DECISION: flow208 is NOT queued. Agent's cheaper follow-ups (pop 2048, block seeded off zero) are declined: §85 shows LOTS covers 0 % of the inexpressible coin, so even a profitable re-split buys the 20 % slice; the GPU slot after flow209/210 goes to whatever the SELL5 falsifier (§85) says. S/lots/judge_pad.patch stays staged (needed only if a 6,919-wide theta is ever judged). 3070 is FREE.

## 88. LOSS-BAND CENSUS: same hole, shifted toward the evening tail; SELL5 (turns 7/14) is valid against our losses but window 5 (turn 21) is the largest block on the band we lose to (2026-09-11T21:30Z, docs/strategy/2026-09-11-expressibility-band.md, S/express/census_band.md)

- Classifier unchanged (29-tape run reproduces §85 line for line). Sets: LOSS10 (10, S/bloss/loss_ids.txt), BAND85 (the 85 weight-2 pinned rungs flow209/210 train on; S/band2100p/town_schedules.json is the 538-tape registry, not a band list), LIVE48 (opponent seat of B's and hr's 48 live losses, converted from S/ep_*.json), POOLED 137.
- Sale timing outside our four lot turns = 81-85 % of inexpressible coin on every set (LOSS10 84.5, LIVE48 81.8, BAND85 81.0, TOP29 81.9); farm half 92-94 % expressible; union over switches still leaves ~half unreachable (LOSS10 45.5 % expressible). The interface claim is not a top-tier artefact; the band we lose to is marginally further outside the decoder.
- Windows 1/3/5 share of sell coin: TOP29 42.0, LOSS10 48.5, BAND85 38.5, LIVE48 43.3, POOLED 41.0. Loss band is NOT a turn-0 dumper (8.9 % vs 19.3 %); its coin is in window 5 (25.3 % vs 20.2; turn 21 alone 12.1 % vs 6.6 = the d13-21 wool/melon dump the LOSS10 anatomy named) and window 3 (15.7 % vs 12.1). Window 1 is the only window where the loss band is quieter (7.5 vs 9.7).
- SELL5's turns 7+14 reach 23.2 % of LOSS10 sell coin (21.8 % of TOP29): valid falsifier, not misaimed. But window 5 (25.3 %, a floor because dump-all rows are priced at zero) is bigger than both windows SELL5 buys → if SELL5 buys anything, the next interface step is a TURN-21 LOT (needs TURN_PRESTOCK 20 → 22 and the SELL_TURNS[-1] anchors re-checked), not a richer function on existing lots. LOTS covers 0 % on every set.
- Open: the coin share is an exclusion measure, not the prize. Pricing stream dispatched 2026-09-11T21:30Z: value the timing hole engine-exact on the 48 live losses (our goods at their windows' quotes vs ours).

## 89. TIMING PRIZE PRICED ENGINE-EXACT: later pays, earlier does not; the exclusion framing of §85/§88 is an accounting artefact; one free move = lot 3 h18 → h21 (2026-09-11T21:41Z, docs/strategy/2026-09-11-timing-prize.md, S/timing/price_timing.py)

- 96 live replays (48 B/hr losses + 48 wins), 14,085 of our lots × 24 target hours, first-order pricing against the recorded market state at the alternative turn with our own units removed (exact for quantity orders; opponent reaction not re-simulated). Reconstruction reproduces §86's sell revenue to the coin. Engine facts: _town_consume fires at step % 4 == 0 AFTER the market phase, so windows are A h1-4, B h5-8, C h9-12, D h13-16, E h17-20, F h21-23; town ticks REMOVE inventory so later is structurally richer; no spoilage or storage cost; 0/14,085 lots would overflow the shed if deferred.
- Variants (coins/game, losses | wins): (a) +4 turns +759 | +1,049 (t 3.4), 5/48 losses covered; (b) −4 turns = SELL5's 7/14: −346 | −508 (t −4.0), 0/48 covered → SELL5 FALSIFIED AS A REVENUE PLAY on the ledger; (c) half/half +247 | +332. Best fixed re-schedule (h1→h13, h18→h21, h10→h17) +1,876 | +1,783 (t 8.0, 1.5 % of sell revenue), 13/48 losses (8/14 narrow) — a 93-coin loss/win gap = LEVEL UPLIFT, not what decides games. Hindsight per-lot oracle +2,988 but +2,806 on wins = 94 % selection.
- Bands/products: d15-29 carries ~100 %; d0-9 exactly 0 (market at I0); d10-14 slightly negative. WOOL +677, STRAWBERRY +284, MILK +72; WHEAT/CARROT/FERTILIZER lose by waiting (flat curves).
- Symmetric control: forcing the opponent's ~292 lots/game onto OUR four turns would have paid them MORE (+3,288 lost games, +3,309 won; biased upward). The 78-85 % coin share in windows we skip is an accounting artefact; their edge is volume and mix, not the turn they quote on. §85's "closer to 500 than 50" is withdrawn as a prize estimate; the census stands as an exclusion census only.
- The single free move: h18 → h21 (+911/game overall, +1,096 on losses, t 6.8; WOOL +523, MILK +373). Free because every buy order sits at h0-h3 and h21 cash lands before the next day's buys; h1 → h13 (+881) would starve the morning buy row it funds. Recommendation adopted: build SELL21 (SELL_TURNS (3, 10, 21), TURN_PRESTOCK 20 → 22, anchors re-checked) as a switch and judge it paired in the engine; close the sell-timing family for anything larger. The running SELL5 engine legs stay as the engine test of this ledger (counterfactuals-overstate: a ledger never decides, paired legs do).

## 90. SELL21 REFUSED ON THE SCREEN: lot 3 at turn 18 is denial; moving it to turn 21 hands the opponent +1,383/game — SELL-TIMING FAMILY CLOSED (2026-09-11T22:19Z, docs/strategy/2026-09-11-sell21-build.md, S/sell21/sell21.patch)

- Built as KAGG3_SELL21 (env prefix, never in the switch string; on2b.py asserts switch names against plan) in /root/tree_sell21 from the pristine arms-next branch head: SELL_TURNS (3,10,18) → (3,10,21), TURN_PRESTOCK 20 → 22. Turn 21 confirmed from the engine: unit ops → _process_market → _town_consume, ticks on step % 4 == 0 (turns 0,4,…,20), so turn 21 is the first market phase after the day's last tick; projector.ticks_before agrees ((18)=5, (21)=6). §89's "h" IS our turn index (price_timing.py reads the pre-turn observation), not turn+1. Inert: 32/32 boards coin-identical OFF (107463847: 94698/98435, −3737, sig 132); ON changes 120/120; 62 unit tests pass; throughput free (232.9 s → 228.6 s per 64 episodes). Side effect: with DROP_ON shipped, drop_turns 17/16 → 20/19 (day-29 crew gains three route turns).
- Screen at B (S/simscreen copy, tree overridden): LIVE-C 120 boards −1,134/game, t −8.87, wins 71.7 → 65.8 %, 22/98 boards; TOPB2 40 boards −451, t −1.68. Seat split: OUR money +249 (t 2.7) / +560 (t 2.6) = the ledger's prediction; THEIR money +1,383 (t 16.7) / +1,011 (t 5.8). The 24-hour sweep ignored the opponent's revenue by construction; our ~531 units at turn 18 were depressing the price they sell into. Two-purse signature (counterfactuals-overstate), fifth time.
- DECISION: refused on the screen (§49-50: the screen is the refuser; t −8.9 is far beyond ±400/board). No engine legs spent. Variant (c) (split lot 3 to keep the turn-18 denial) is the only unrefuted member; declined — every sell-timing member is now a displacement/denial trade and the ES already owns the split genes. SELL-TIMING FAMILY CLOSED. SELL5 legs (in flight) finish as the last engine word on the family.
- Note: theta B md5 is 7fcf3948 (submission/theta.npy = artifacts/kagg2_games/thetas/flow193_g100_hr.npy byte-identical); 41b87adc quoted earlier was wrong.

## 91. SELL5 IN THE ENGINE: LEVEL — +35/+44/+52 coins, 0 flips in 320 paired games; the allocator declines the windows it is given; no SELL5 arm (2026-09-11T22:27Z, docs/strategy/2026-09-11-sell5-falsifier.md, S/sell5/sell5.patch)

- KAGG3_SELL5 built (SELL_TURNS (3,7,10,14,18); v1 raw ramp, v2 ramp rescaled 2/4 so B's press genes keep their meaning; v3 turn-21 sixth lot NOT built — moves SELL_TURNS[-1] and with it the DROP-day turn_budget and MIDDAY_PLACE_V2_TURN). Inert: OFF control legs byte-identical to B's csvs across all 160 games; reference board 94698/98435/−3737/sig 132 exact.
- Paired real-engine legs at B (hr switches, --seed-per-opponent), v2: TOPB2 +35 (SE 28, t 1.24), LIVEC-H30 +44 (SE 20, t 2.24), LIVEC-H30B +52 (SE 38, t 1.38); wins unchanged 32.5 / 63.3 / 83.3 %; 0/0 flipped on every leg. v1: +50 / +9 / −15, all noise. Sim screen agrees (v2 TOPB2 +26, LIVE-C +43 t 2.9).
- Mechanism (S/sell5/lotprobe.py): the two new rows take 52 of 1,441 season units (3.6 %), all out of turns 10 and 18; 63 % of volume already leaves on turn 1 and 31 % on turn 18. sell.allocate's press+externality preference declines the windows when offered them: the row count was never the constraint. Reconciles §89 (which moved 100 % of a lot) and §90 (turn-18 row is denial). Sell-timing is closed at B's genes in both directions.
- Throughput −2.5 %/gen (4.10 → 4.00 eps/s, symmetric contention), not the ~6 % per sell turn the ops.py comment claims.
- DECISION: VERDICT LEVEL; no SELL5 training arm; patch archived at S/sell5/sell5.patch, arms-next worktree restored to clean. The user's "remake the decoder to express all plays" question is now answered on four measurements (§85, §88, §89, §90, §91): the decoder's missing turns are not where the points are; the ES arms (flow209/210) and their g30 SNR read remain the path.

## 92. STRATEGIST REVIEW: the objective and the judge are bimodal in opponent strength with a hole at 2550-2800, exactly where the next 450 points live (2026-09-11T22:37Z, docs/strategy/2026-09-11-strategist-next.md)

- Objective mass (S/flow209/launch_flow209.sh:140,149): top-ten rungs 37.2 % (TOPB2 opponents 2953-3081), 2300-2700 30.6 %, 1900-2100 17.9 %. Gate = LIVE-C hold-out (opponents ≤ ~2500) + TOPB2. Matchmaking draws own rating ± 45 with no tail (ladder-projection §1): B's pool 2324 ± 49 (max opponent ever met 2433), hr's 2470 (max 2675). Neither file has ever played a ≥ 2700 opponent; the 2550-2800 band is 0 % of the objective and 0 % of the gate.
- Ranked: (1) NEXT-BAND: ~30 pinned-town tapes of 2550-2750 teams, one paired leg B vs hr, no GPU, ~4 h. Bar: B > hr at |t| ≥ 1.5 → judge band-invariant, NEXT30 becomes a free fifth leg; hr ≥ B at t ≥ 1.5 → judge band-dependent and both the incumbent (B) and the seed choice (flow209 over flow210) were made on the wrong band. DISPATCHED 2026-09-11T22:37Z. (2) GATE-vs-LADDER: of the last 13 AUTOJUDGE-vsB reads, 12 lost wins on TOPB2 while 8 gained on LIVE62 (flow206_g10, flow205_g10 +6/−0, flow198_g10 +10/−2) = a band gradient; falsifier = upload the best refused record into a slot and read at g80. NEEDS THE USER (upload; the standing rule is that a candidate replaces hr and B stays) — presented, not acted. (3) flow211 = launch_flow209.sh with NEXT30 at w10.2 and top-ten rungs cut 10.2 → 4, seeded by (1)'s winner; gated on the §84 g30 SNR read.
- (d) Run the arms only: EV ≈ +10-25 points (§79 settling test, §60/§77 level records). (1) and (2) beat it because they repair the instrument every decision is read through; (3) does not until g30 says the arms carry a direction.
- Closed for free: codex's "market-curve feature columns use DEFAULT_MARKET_PARAMS, not observation" is void — spec.py:371 / es/archetypes.py:297: sample_market_params is a training-only regulariser and the competition runs the defaults. With §78 the observation/opponent-model class is empty.

## 93. G10 DECODE DIFF: both arms move decodable knobs at the margin (step 2-3.5 % of one σ draw, ~6-8 coarse knob changes per 240 decisions); the §76 lattice reading holds at the edge; the g30 read is purely about persistence (2026-09-11T22:43Z, docs/strategy/2026-09-11-g10-decode-diff.md, S/snr/g10_diff.py)

- Untrained 5,598 genes byte-identical to the seed in both arms. flow209 (seed B): ‖Δ‖ 0.0071 = 2.1 % of one σ-0.01 draw, loaded on gp 35 % + dh 31 %. flow210 (seed hr): ‖Δ‖ 0.0122 = 3.5 %, loaded on w3 33 % + dh 32 %; b3 (sell head's global lot-count bias) moved 10.6 % of its own value. The two arms did not pick the same direction; dh (residual town drain) is the only block both load.
- Decoded on 8 LIVE-C hold-out boards (240 decisions, 42 integer knobs): flow209 14 coarse changes (plant_target ±1 on d11/d24, one animal_want swap d9, crew_target 11 → 12 d22); flow210 20 changes, all plant_target ±1. Fixed-point ratio churn (press, grow_mult ±1-2 units) on nearly every decision. Corroborated by the engine: flow210 g10 LEVEL vs its own seed, 0 flips on 284 games.
- In-sample: all 166 rungs are pinned-town tapes (archetypes drew zero episodes despite arch_frac 0.9; no per-rung win field in the log). flow209 mean_win 0.6660 → 0.6675 (best_win DOWN 0.7360 → 0.7303); flow210 0.6059 → 0.6198 near-monotone (best_win up). real_gate next at g100. step_cosine: 2 records → PENDING.
- Reading for g30: ~0.6 coarse knob changes per board-day per 10 gens → a g30 candidate differs on 15-20 % of board-days, so decode will not bind; the question is persistence vs the momentum null (§84: 0.51, p95 0.55). Base rate (§72/§77) says NOISE. Watch flow210 over flow209: larger step, monotone in-sample curve, the b3 move — if either carries a direction it is the hr seed, i.e. the recipe finds slack hr has and B does not (consistent with §92's band question).

## 94. RUNG ALLOCATION AUDIT: zero archetype episodes is the intended launcher override, not a defect; the objective is 99 % pinned tapes with the 2550-2800 band absent (2026-09-11T22:52Z, docs/strategy/2026-09-11-rung-allocation.md)

- Verdict (c): launch_flow209.sh:186 sets --rung-weight expander/rusher/rancher/patient_grower = 0 (inherited from flow128/129); under --pinned-once the 166 pinned rungs each get exactly one episode regardless of weight (es/train.py:4413-4429), the residual 6 pairs see an all-zero weight vector and the trainer takes its "every rung pinned → residual is self-play" branch (:4547-4551), so arch_frac 0.9 is never read. Only rounding artefact: 178 of 179 episodes play (floor at :4926); not material (0.96 → 1.12 % drawn).
- The objective per candidate per generation (weight share): w2 old loss-tape band ~1900-2100: 27.2 %; w4 LIVE-C 1-42 (2300-2615): 26.9 %; w4 LOSS10 (2175-2381): 6.4 %; w4 top-50 templates (~2700+): 5.8 %; w10.2 top-ten (2821-2954): 32.7 %; self-play 0.96 % (6 eps vs the frozen --init-theta seed = B for flow209 / hr for flow210, 6 vs the current centre; never the population at pool 1). Confirms §92's hole: nothing between 2615 and ~2700 except 9 top-50 tapes at 5.8 %.
- No fix required now; a flow211 recipe (§92 #3) would put NEXT30 in the w10.2 slot and cut top-ten to w4 — that is a --rung-weight change only, no trainer edit.

## 95. BAND GRADIENT ON EXISTING LEGS: the judge is NOT band-dependent; B beats hr flat across 1827-3081 and already on 37 boards inside 2550-2750; GATE-vs-LADDER has no candidate class (2026-09-11T23:05Z, docs/strategy/2026-09-11-band-gradient.md, S/bandgrad/bandgrad.py)

- B − hr: 152 boards / 304 games over five legs (LIVE62 1827-2070, LOSS10 2175-2381, LIVEC-H30 2440-2615, H30B 2519-2682, TOPB2 2953-3081), 0 boards without a rating. Positive on every leg (+644…+1,031), pooled +802 SE 230 t +3.48; slope +36 coins per +100 rating (SE 65, t 0.56), Spearman 0.044, within-leg slopes null. The 37 LIVE-C boards inside 2550-2750 give B − hr +1,104 (SE 400, t +2.76): the band is interpolation, not extrapolation. §92's "never measured at 2550-2750" is true of the Kaggle pool, false of the judge; the incumbent and the flow209-over-flow210 seed choice stand.
- Records − B (19 AUTOJUDGE-vsB records, 2,868 board rows): pooled −477 t −10.4; slope −42/100 driven entirely by TOPB2 (+16/100 with it dropped); the "LIVE62 gains" are 62-coin flips on a leg the base wins 85.5 % and 8 of 9 gaining records are negative in LIVE62 coins. Real and opposite: records lose hard to the 3000+ tapes (−2,991, t −9.4). Keep the TOPB2 clause. GATE-vs-LADDER (§92 #2) is dead as specified: 0/19 records gain net TOPB2 wins and none is coin-positive on both LIVE62 and TOPB2 — no candidate exists to upload. The option held for the user is withdrawn.
- NEXT30 (in flight): prior B − hr +901 on the 60 boards at 2400-2800 → expected t +2.1, P(pass) 0.72, P(hr ≥ B) ≈ 0. It re-confirms; its lasting value is the tapes themselves (the 2615-2700 band is absent from the objective, §94) as flow211 rungs and a fifth leg. Let it finish; pre-commit to 60 boards if the first 30 read inconclusive.

## 96. NEXT30 BUILT AND READ: B > hr at t +1.93 on 30 pinned-town tapes rated 2550-2750 → judge band-invariant confirmed in the engine; B's edge decays inside the band (2026-09-11T23:07Z, docs/strategy/2026-09-11-nextband.md, S/nextband/)

- 44 pinned-town tapes (30 NEXT30 + 14 extension), one per team, stratified 2567-2750 from the live leaderboard (344 in-band teams), each the team's seat in a win of theirs from the last hour; 44/44 drawn and town cuts byte-exact (tape_opponent.verify, 719 steps, 8 unlocks). Registry: S/nextband/town_schedules.json = superset of S/band2100p (538 → 582 rows); the shared registry was NOT rewritten while judge legs read it (S/nextband/town_append.sh merges atomically). run.sh refuses to start on a missing id because town_inject falls back to a drawn town silently.
- Paired leg (arms-next, hr switches, --seed-per-opponent, WORKERS=4): NEXT30 60 games, hr 63.3 % → B 68.3 %, +697/board, sd 1,961, t +1.93, W3/L0; NEXT44 +557, t 1.94, W7/L1. By half: 2550-2650 +1,377 (t 2.20); 2650-2750 +102 (t 0.29, level). Cross-leg: hr 63.3/70.0/63.3/25.0 vs B 63.3/83.3/68.3/32.5 on H30/H30B/NEXT30/TOPB2.
- VERDICT: bar met (|t| ≥ 1.5), judge band-invariant (agrees with §95's prediction t +2.1). Incumbent B and the flow209 seed choice stand. NEXT30 becomes the fifth judge leg (~5 min at WORKERS=4; base csvs S/lossflip/nextband_{hr,B}.csv exist) — staged into watch.sh via patch, applied at the next quiet window. Ordering is band-invariant, size is not: B is level at 2650-2750, which argues for flow211 (rungs re-pointed at the band we face), staging in flight.

## 97. NEXT30 APPLIED AS THE SIXTH JUDGE LEG (informational); watcher relaunched pid 14846 (2026-09-11T23:15Z, S/nextband/judge_leg.patch, apply_judge_leg.sh, test_judge_leg.sh)

- Patch (44 lines, one file S/autojudge/watch.sh) tested 18/18 on a scratch copy with every leg stubbed: AUTOJUDGE line gains "| NEXT30 ALL 60 63.3% 68.3% 697 1961 1.93 … 3 0 0 30" against the hr base, AUTOJUDGE-vsB gains the same column against S/lossflip/nextband_B.csv (B vs itself: d 0, t nan); LOSS10 line intact; promotion logic byte-identical (four paired legs decide).
- Applied 2026-09-11T23:15Z in the quiet window (0 legs running; g20 records due ~00:10Z): watcher stopped by process group, backup S/autojudge/watch.sh.bak_*_prenext30, registry merged (S/band2100p/town_schedules.json 538 → 582 rows via town_append.sh), patched, relaunched: new pid 14846, 31-process group, watch.sh md5 d541242c (was c0d38803). Cost ~5 min per judged record.

## 98. flow211 STAGED = NEXT QUEUED ARM: the §73 recipe with NEXT30 at w10.2 (38 % of the objective) and top-ten cut to w4; --episodes 200; precheck ALL PASS; on the host (2026-09-11T23:37Z, docs/strategy/2026-09-11-flow211-staging.md, S/flow211/launch_flow211.sh md5 a3d7c543)

- Objective shares flow209 → flow211: w2 old band 27.2 → 21.2 %; LIVE-C 1-42 26.9 → 21.0 %; LOSS10 6.4 → 5.0 %; top-50 5.8 → 4.5 %; top-ten 32.7 → 10.0 %; NEXT30 (2550-2750) 0 → 38.2 %; self-play 0.96 → 0.25 %. 200 rungs, 200 episodes/gen.
- Pinned count: 166 + 30 = 196 pinned; a weight-0 pinned rung still consumes its episode by design (es/train.py:4413-4429), so the w2 tapes cannot be zeroed out cheaply; chosen --episodes 200 (196 + 2 residual pairs), +12.4 % wall-clock per gen, no memory change. Launcher refuses above 198 pinned; NEXT60 would need --episodes 230.
- Precheck: 196/196 tapes local and remote (30 NEXT tapes rsynced to ~/stage_hr/artifacts/tape_actions_town/, all carry the town key), next_ids.txt = S/nextband/ids.txt, disjoint from the 166, seed B 7fcf3948 on the host, train-only decodes to 1,191/6,789 in flow209's blocks, CPU dry run of the launcher's own argument list prints "196 pinned rungs x 1 episode + 4 carried", rungs=200, no budget warning. Host train.py identical past line 4000.
- Launch (GPU n freed by the §84 g30 read or by Rule 4): ssh user@remote-host 'cd ~/stage_hr && mkdir -p artifacts/flow211 && CUDA_VISIBLE_DEVICES=<n> nohup bash S/flow211/launch_flow211.sh > artifacts/flow211/launch.out 2>&1 &'. The launcher refuses on a busy GPU. Judge: the watcher's ARMS list must gain "flow211 stage_hr" before launch (stage a one-line patch via the S/nextband/apply_judge_leg.sh pattern).

## 99. NEXT30 ANATOMY: the 2650-2750 opponent is the mistake-free clone, not a different play; d15-29 decides; no open knob — a judge finding (2026-09-11T23:44Z, docs/strategy/2026-09-11-nextband-anatomy.md, S/nextband/anatomy.py)

- Opponent tapes by half (16 upper / 14 lower): no column separates the halves in the mean (max |Welch t| 1.43 over 46 columns; hires 5/3, 11 hands d10, 38/20/12 tiles d10, ~7.7 cows / 6.6 sheep, 72 melon sold from d10, fertilizer applied 65-72 / sold 334-346, ~55/31/166 sell rows by band). The separation is dispersion: every upper team hires exactly 5 on d0, plants exactly 12 melon and 20 strawberry by d10, holds zero melon after d14 (sd 0 vs 0.27 / 1.40 / 6.06 / 22.4); 18 of 30 teams share one d0-10 fingerprint. Our +1,377 on the lower half is straggler-punishing with no target above 2650.
- Where the margin is decided (pinned-town sim, 30 boards, cross-checked vs the engine leg): d0-9 +3,029, d10-14 −20,705 (flat tax, corr 0.18 with the final margin), d15-29 +21,786 (corr +0.93). B's 9 losses recover +15,058 in d15-29 vs +24,670 on its 21 wins; d10-14 differs by only −2,166; d0-9 lead is larger on losses. Upper half costs us on the upside (mean win +6,195 vs +8,963), not in the losses.
- Levers: none open. The trained blocks (gp, dh, ds, w3, b3, g5, gb5, b1) are sell-price/lot/town-drain knobs and do not touch opening, hiring, mix or animals — the columns identical across the band; every sell-side family is closed (§55, §57/§86, §68, §70, §76, §85-§91). DECISION: judge future arms on the NEXT30 UPPER half specifically (the mistake-free clone is the only opponent class not already measured by LIVE-C); flow211's objective (§98) already carries the whole set at 38 %.

## 100. flow211 BLIND REVIEW: FIX-BEFORE-LAUNCH — abs probe is one unsplit jit call that grows with the rung count; NEXT30 judge column would be in-sample; seed 311 breaks CRN pairing (2026-09-11T23:50Z, docs/strategy/2026-09-11-flow211-review.md)

- D0 HIGH: es/train.py:5510 uses max(chunk, total), so the abs probe (2 × abs_pairs × r rows, r = 4 archetypes + every tape rung) runs unsplit: flow209 21,760 rows, flow211 25,600 (+17.6 %), 3.1× the main loop's 8,192-row step, allocated next to the live arrays, first at gen 10. "--chunk sets memory" is true for the main loop only. Live cards are at 17,974 of 24,576 MiB with one arm each. FIX: --abs-pairs 64 → 54 (rows 21,600 ≤ flow209's) or accept the risk knowingly.
- D1 HIGH: S/flow211/next_ids.txt = S/nextband/ids.txt = the NEXT30 judge leg → flow211's NEXT30 column is 30/30 in-sample, printed unlabelled. Promotion legs unaffected. FIX: judge flow211 records on the 14-board extension (S/nextband/ids_ext.txt, bases S/lossflip/nextband_{hr,B}_ext.csv, held-out) via the watcher patch.
- D2 HIGH procedural: judge_arm.patch needs the watcher relaunch; never mid-leg (partial csv reads as done). D3 MED-HIGH: --seed 311 → 309 (boards are name-derived, reuse gives CRN pairing with flow209). D4 MED: mean_win is unweighted (ep_weight reaches only the gradient) → NEXT30 is 15 % of the log line, not 38 %; flow211's curve is not comparable to flow209's 0.667. D5 MED: precheck greps a warning branch that cannot fire (carried = 4); check train.py:196-201's shape instead. D6 MED: busy-GPU guard dies silently under set -e if nvidia-smi fails. D7-D10 LOW (hard-coded 166/198/200; min-flips 5 unreachable at seats 2, inherited; arch-frac inert).
- 21 checks passed (remote md5, seed B, tapes on host with town keys, 196 + 2 pairs = 200, exact multiple of chunk, residual self-play 0.25 %, 2× rung weight, gate 124 games disjoint from all 196 rungs, mask 1,191, watcher name/fetch/csv coverage). Fixer dispatched 2026-09-11T23:50Z; launch still waits for a GPU (§84 g30 read or Rule 4).

## 101. TOP-TIER OVERFIT TEST: records are level on the 20 top-ten tapes they train on and worse on the held-out 3000+ tapes; the damage tracks step size and subspace, not rung weight (2026-09-11T23:59Z, docs/strategy/2026-09-11-toptier-overfit.md, S/topb2/run_insample.sh)

- Four records paired vs B (both seats): IN-SAMPLE top-ten (20 trained tapes) pooled −224 SE 247 t −0.91 (best flow209_g10 +28, worst flow205_g10 −481); HELD-OUT TOPB2 pooled −1,274 SE 348 t −3.66, flips +0/−12. Gap +1,050 (t +2.46). No in-sample gain anywhere → not tape memorisation; 22.7 points of objective mass buy nothing against the opponents they weight.
- Mechanism on the two worst boards: openings level or ahead through d9; 107460230 lost inside d15-29 (−9…−12k, OUR money falls from d18, the record under-realises its own late crop; opponent untouched for flow209); 107465299 lost inside d10-14 (THEIR money rises +3.2-4.1k, denial failure). Shared decoded direction: grow_mult[0..2] up / grow_mult[8] down on 22-30 of 30 days, press[4]/press[7]/hold[6-7]/hire_bias drifting. Full-mask arms also cross SWITCH0 (plant_target[0] 11 → 10); flow209 does not and still loses 107460230 by 8.7k, so the day-0 switch is not the cause. Sim reproduces all eight engine games to the coin.
- For flow211: cutting top-ten 32.7 → 10 % removes a target paying nothing but releases no stored gain; TOPB2 damage tracks step size and subspace (full-mask −1,721/−1,910 vs train-only −385), not rung mix. TOPB2 stays fully held out and remains the leg where records separate from B at |t| > 2.

## 102. flow211 REVIEW FIXES APPLIED: --abs-pairs 54 (probe 21,600 rows ≤ flow209), --seed 309 (CRN pairing), precheck asserts the real banner, robust GPU guard, held-out NEXT14 judge column; precheck ALL PASS; launcher md5 f1d71dee local = remote (2026-09-12T00:08Z, docs/strategy/2026-09-11-flow211-staging.md §8)

- Argument diff vs flow209 is now exactly: --run flow211, the 30 NEXT tapes at w10.2, top-ten 10.2 → 4, --episodes 179 → 200, --abs-pairs 64 → 54. Watcher patch S/flow211/judge_arm.patch (against live d541242c): ARMS gains flow211; names matching ^flow211 run the NEXT leg on the 14 held-out extension boards (FIRST=30, absolute IDS, bases nextband_{hr,B}_ext.csv, label NEXT14); every other arm unchanged (flow209's line byte-identical patched vs unpatched). test_judge_arm.sh PASS (NEXT14 column reproduces +258 t 0.54 W4/L1).
- Applied 2026-09-12T00:08Z via S/flow211/apply_judge_arm.sh in the quiet window before the g20 legs (see the verdict line). Launch line unchanged (§98), GPU index chosen when an arm frees. Watch the gen-10 abs probe on flow211 explicitly (the only OOM candidate).

## 103. CODEX BLIND REVIEW OF §85-§102: four valid objections — corrections to §89, §93, §99, §101; flow211's re-point rationale is underpowered; two cheap gates before launch (2026-09-12T00:22Z, docs/strategy/2026-09-12-codex-review-chain.md, S/codex/review_20260912.txt)

- CORRECTION §99 (source error): the trained blocks DO reach hiring and crew — policy.py:635 puts b1/dh in the shared encoder, :643-650 feed w3/b3 through gp into crew, head, prio and lots; §93's own decode showed crew_target 11 → 12 and an animal_want swap. "No open knob" in §99 is withdrawn as stated; what stands is that every hand-built family is closed and the ES owns those knobs.
- CORRECTION §93 arithmetic: 14 coarse changes / 240 decisions = 0.058 per board-day, not 0.6; the "15-20 % of board-days at g30" extrapolation is 10× too high — expect ~2 % and flips to stay rare at g30.
- CORRECTION §101 statistics: the pooled "80 board-cells" are 4 correlated records on the same 20 boards; with dependence the held-out TOPB2 pooled t is ≈ −2.05 (SE ~621), not −3.66. Conclusion (worse out of sample, level in sample) stands at reduced strength.
- CORRECTION §89 inference: "+3,288 if their lots sat on our turns" is an UPPER bound (opponent revenue ignored), so it cannot prove their window choice is worth ≤ 0 to them; the exclusion framing is merely unproven, not disproven. §90's SELL21 refusal survives (board-level t ≈ −6.3 with seats pooled honestly, above the §50 bar of 2.5). SELL5: inverse-variance pooled +43 coins SE 15 t 2.85 — reproducibly positive and negligible; decision stands, "LEVEL" is the wrong word.
- VALID on process: §90 closed the sell-timing FAMILY on a screen refusal plus one frozen allocator; variant (c) (split lot 3, keep the turn-18 denial) is unrefuted and an ES arm under SELL21 would be the fair test (sell21-build.md:212-220). Left closed for now on cost; reopened only if the arms stay level.
- VALID on flow211: the rationale "B's edge decays by 2700" is an underpowered null (halves differ by +1,275 SE 719, t 1.77); the staged weights (38 % band / 10 % top-ten) drifted from §92 #3's sketch (~20 % / 15 %); and flow211 cannot be promoted on its own hypothesis (promotion = the four standard legs; NEXT14 is informational) — acceptable because §95/§96 showed those legs are band-invariant. GATES before launch, both cheap: (2) run flow209_g10 and flow210_g10 on the NEXT14 panel (56 games, CPU) — started 2026-09-12T00:22Z; (1) objective ablation at B (family gradients, S/famgrad in flight).

## 104. SNR READER ON CHECKPOINTS: records = centre thetas byte-for-byte; flow209 g0→g10→g20 block cosine +0.82 vs momentum-null p95 +0.54 — the first to clear the null, one pair, PENDING until g30 (2026-09-12T00:27Z, docs/strategy/2026-09-11-snr-reader.md §Checkpoint series, S/snr/keep_state.sh, S/snr/step_cosine.py --source states)

- state.npz (every --ckpt-every 10 gens, overwritten) keys: theta = the ES centre (the series), m = momentum buffer (1,191 nonzero = d_train; next step = lr·m), champion and best_abs_theta are not the centre. flow209's g10 record is byte-identical to theta in state_g00010 (‖diff‖ 0): records and states are the same object, states are the better-sampled view. keep_state.sh archives S/snr/<run>/state_gNNNNN.npz idempotently; a checkpoint overwritten before it is copied is gone.
- flow201 reproduces exactly on the extended tool (0.4375 / 0.1561 vs optnull 0.4241 / 0.1557). flow210 states [g0, g20]: one block, PENDING; cos(block, m) +0.92 vs isotropic null 0.63 but a heteroscedastic null reaches 0.78-0.98, so not signal. flow209 states [g0, g10, g20]: cos(k, k+1) = +0.8168 vs optimizer-null p95 +0.5443 (perm95 0.2466; scaled null p95 0.6068); all eight trained blocks above their own nulls (gp 0.72 … b3 1.00). PENDING (one pair). Reading rule §84 needs the g30 pair: if the mean consecutive cosine stays > ~0.6 with a 0.05 margin over p95, flow209 is PERSISTENT and keeps its GPU; a level or falling second pair says noise.
- Note the in-sample view is flat (mean_win 0.6649 at g18 vs 0.6660 at g1, best_win unchanged) and the g10 engine legs were level: a persistent direction with no measurable gain yet is consistent with §93's small step (2 % of one σ draw per 10 gens); persistence at g30 would argue for letting flow209 run and for raising its lr only after a g40 engine read.
- g30 read armed 2026-09-12T00:27Z: S/snr/wait_g30.sh (nohup) archives both g30 checkpoints as they land (~01:50Z flow210, ~02:15Z flow209), runs step_cosine --source both, appends the verdict lines.

## 105. FAMILY GRADIENTS AT B: all rung families ALIGNED; flow209 and flow211 objectives agree at ρ 0.93 — the re-weighting is cosmetic for direction; with §104/flow209 g20 LOSS the objective's own direction hurts held-out play (2026-09-12T00:47Z, docs/strategy/2026-09-12-family-gradients.md, S/famgrad/)

- One pop-512 rollout at B on flow211's 196-rung ladder, 4 eps seeds, σ 0.01, train-only 1,191: family gradients from the same (advantage, eps) with ep_weight zeroed outside the family (FLOW211 reproduces the trainer's one_draw at cos 1.0000). Cross-seed cosine matrix (SE 0.018; diagonal = two-seed reliability 0.068-0.112, vs §72's 0.039 on the full objective and the P/(P+d) ceiling 0.177): W2·LIVEC42 0.068, LIVEC42·NEXT30 0.083, W2·NEXT30 0.080, TOPTEN·NEXT30 0.043, TOPTEN·W2 0.054, TOP50·all ≤ 0.02, LOSS10·W2 0.004; FLOW209·FLOW211 0.100 vs reliabilities 0.105/0.112. Disattenuated: band families 0.82-0.98, TOPTEN·NEXT30 0.44, FLOW209·FLOW211 0.93. No pair significantly negative; top-ten opposes nothing. Norms carry no information (rank_normalise).
- Consequence: flow211 is a sampling/support A/B, not a direction A/B; "the ES is pointed at the wrong band" is false. §101 explained from inside the objective: there is no separate top-ten direction in this subspace.
- With flow209's g20 centre LOSS 2/3 (00:45Z: H30 −516 t −3.0, H30B −645 W0/L6) along a direction consistent across blocks (§104 cos 0.82) and across families, the objective's gradient at B points away from the held-out engine judge while the in-sample curve stays flat. Audit dispatched 2026-09-12T00:47Z: does the g20 centre beat B IN THE SIM on its own training rungs (LIVE-C 1-42) and on the held-out 43-102, and in the ENGINE on the same boards — sim/engine divergence vs within-band memorisation vs plain noise walk with momentum. flow211's launch is HELD until that audit and the step ladder (in flight) report; flow209 retires on a third loss regardless.

## 106. STEP LADDER ALONG flow209's DIRECTION: loss at BOTH signs, monotone in |α| — B sits in a lattice cell; the persistent direction is momentum drift, not gain; do NOT raise lr (2026-09-12T01:15Z, docs/strategy/2026-09-12-step-ladder.md, S/stepladder/)

- θ(α) = B + α(θ_g20 − B): delta on exactly the 1,191 trained genes, ‖Δ‖ 0.0155 = 0.045 of one σ draw (σ√d = 0.345); α 16 = 0.72 draws. α 1 reproduces the judge's flow209_g20s theta to 6e-11 and its NEXT30 csv row for row.
- Screen (LIVE-C 120 / TOPB2 40, Δ/game): α1 −413/−212; α2 −291/−682; α4 −538/−812; α8 −1,371/−1,645; α16 −5,942/−6,654; α−4 −381/−1,288. Engine (paired vs B, pooled NEXT30 + LIVEC-H30B 60 boards): α1 −423 t −2.38; α2 −238 t −1.06; α−4 −485 t −1.74; α8 NEXT30 −1,606 t −5.1 (W1/L6); α16 −7,329 t −9.1 (W0/L20). Engine reproduces the screen cliff to ~20 %.
- Reading: §60/§66/§76 cell signature — every extrapolation walks off B's cell; +α and −α lose alike; no gradient that pays. §104's cos 0.82 is real as motion only. §59's lr 0.003 "noise walk" is retroactively the α ≈ 16 cliff (0.7σ per 20 gens), not a noise floor.
- DECISIONS: keep lr 1.8e-4 (the ladder peaks at α ≈ 1, i.e. losing least); "persistent direction" CLOSED as a source of expected gain; flow209/210 retire on their g30 reads if they lose again (both at 2/3), and no arm on this objective/subspace from B is worth a GPU unless the objective-vs-judge audit (in flight) finds a sim defect. Binding constraint remains the action interface / lattice (§60/§66/§76). SELL21 variant (c) (split lot 3, keep the turn-18 denial) is the only unrefuted interface member — build + screen dispatched 2026-09-12T01:15Z.

## 107. OBJECTIVE-VS-JUDGE AUDIT: sim = engine (ρ 0.77 per board); the ES step is a TRANSFER — top-ten and LOSS10 margin bought with band margin — and the judge sees only the sold side (2026-09-12T01:52Z, docs/strategy/2026-09-12-objective-vs-judge.md, S/objaudit/obj_rungs.py)

- g20 centre − B, paired: TRAIN42 (LIVE-C 1-42, in sample) engine −71 t −0.27 / sim −187; held-out H30 engine −516 / sim −597; H30B −645 / −698; TOPB2 −197 (tail-driven). Pooled held-out 60 boards: engine −580 SE 162 t −3.58, sim −647 t −3.88. Per-board sim vs engine ρ +0.774 (sign agreement 82 %). Case A (sim defect) REFUTED; case B (memorisation) REFUTED (in-sample is not better); the loss is broad (19/30 boards negative per leg, worst-3 < 32 %), and does not persist board by board (ρ(g10, g20) 0.15; g10 +85 → g20 −580: the loss scales with the step).
- Case D: B and g20 through the trainer's own _play on all 166 pinned rungs (one draw, 178 eps): TOPTEN (w10.2, 32.7 %) +461 t +2.0; LOSS10 +565 t +2.1; LIVEC42 (26.9 %) −382 t −1.6; W2 band (27.2 %) −249 t −1.3; TOP50 −531; self-play −543; objective-weighted win 0.5904 → 0.5859 (flat, −19.6 weighted coins/episode). The rank-normalised advantage is indifferent to the trade; the judge (LIVE-C hold-outs, LIVE62, NEXT30 = band provenance; TOPB2 = a different top-tier set) is not.
- Consequences: (1) read g30 on the held-out margin, never on the block cosine alone; (2) lr stays (§106); (3) flow211's top-ten cut 32.7 → 10 % and NEXT30 38 % now has a direct rationale — it removes the transfer's destination and enlarges its source — distinct from the one §103 falsified; GATE: repeat obj_rungs.py on 3-4 batch seeds and require both band families negative and TOPTEN positive (dispatched 2026-09-12T01:52Z); (4) the sim screen is validated as the cheap centre judge (ρ 0.77, within ~80 coins on three sets, 697 s vs ~22 min).
- Plan: if the gate holds, flow211 replaces the first arm to reach its third loss (flow209 g30 ~02:15Z, flow210 ~01:50Z); the other arm follows on its own third loss.

## 108. SELL21 VARIANT (c) — split lot 3, keep the turn-18 denial: REFUSED at f ½ and 1, LEVEL at f ¼; a thin market is thin for both seats; SELL-TIMING FAMILY CLOSED with no unrefuted member (2026-09-12T01:54Z, docs/strategy/2026-09-12-sell21c.md, S/sell21c/sell21c.patch)

- Built in /root/tree_sell21c as KAGG3_SELL21C=1|2|3 (f = ½, ¼, 1 of lot 3's WOOL/MILK/STRAWBERRY moved to a turn-21 lot; SELL_TURNS (3,10,18,21), N_LOTS 4, TURN_PRESTOCK 22). Pure split: the greedy can never choose turn 21 (−2^24 on its row), lots 1-3 see the exact three-lot arithmetic; new anchors O.DROP_LOT / O.DROP_DEADLINE_TURN keep drop_turns 17/16 in every mode (SELL21's day-29 side effect removed). Inert 32/32 coin-identical (107463847: 94698/98435/−3737/sig 132); 62 tests pass; throughput +1.1 % (f ½) / +2.7 % (f 1).
- Screen at B, seat split (LIVE-C 120 / TOPB2 40): f ½ Δ −301 t −5.9 (ours +83, theirs +384) / +252; f ¼ Δ −60 t −1.9 (ours +41, theirs +101) / +139 t 2.6; f 1 Δ −946 t −9.6 (ours +90, theirs +1,036) / +233. Three of nine products carry 83 % of SELL21's whole loss; our purse saturates (+41/+83/+90) while theirs is dose-responsive (+101/+384/+1,036).
- Verdict: f ½ and f 1 REFUSED; f ¼ LEVEL on the screen (positive on TOPB2 only) — engine legs (NEXT30 + LIVEC-H30B, S/sell21c/run_legs.sh 2, log legs_m2.log) finish ~02:15Z and are informational; even a positive read is "SELL21 turned down until the loss is under the noise". No ES arm: press/hold price OUR curve, the loss is THEIR curve rising, invisible to our fitness at fixed f; the data asks for a per-opponent-class f = an opponent model (§78/§92: class empty). SELL-TIMING FAMILY CLOSED, no unrefuted member (answers §103's process objection).

## 109. flow210 RETIRED (3 losses) → flow211 LAUNCHED on GPU1 (pid 1006600, 02:09:46Z); flow212 (band-only objective) STAGED as the GPU0 candidate when flow209's third read lands (2026-09-12T02:12Z, docs/strategy/2026-09-12-flow212-staging.md, S/flow212/)

- flow210 g30 centre vs B: TOPB2 −1,886 W0/L5, H30 −595, H30B −548 W0/L8, LIVE62 −921, NEXT30 −421 = LOSS 3/3; killed by pid after the /proc cmdline check; GPU1 released (1 MiB). flow211 launched from ~/stage_hr/S/flow211/launch_flow211.sh (md5 f1d71dee verified on the host): GUARDS OK gpu=1, 30 NEXT rungs at w10.2, pinned 196, --episodes 200; compiling at 1.3 GB. Watch its gen-10 abs probe (§100 D0). Watcher already lists flow211 with the held-out NEXT14 column.
- flow212 staged (launcher md5 de043b0f local = remote): flow211 with LOSS10, top-50 and top-ten at --rung-weight 0 — still played (pinned block holds composition, 19.5 % of wall clock is a free read of the zeroed families), contributing exactly 0 to every candidate's score before ranking (shaped_advantage collapses episodes with w = ep_weight/Σw before rank_normalise); shares: W2 26.3 %, LIVEC42 26.0 %, NEXT30 47.4 %, self-play 0.3 %. Precheck PASS (banner, abs probe 21,600, mask 1,191, weight census). Judge patch S/flow212/judge_arm.patch (ARMS + NEXT14 case) tested PASS, NOT applied. flow211 vs flow212 = a pure weight A/B under the shared seed-309 CRN draw. TOPB2 stays the promotion veto for both.
- Decision rule: the four-seed objective gate (S/objaudit, in flight) says whether the transfer is robust (band families down, TOPTEN up). If yes, flow212 takes GPU0 when flow209 retires (third read at its g30 centre, ~02:20Z); if the gate fails, flow209's slot goes to flow212 anyway as the only remaining objective hypothesis, and both arms are read at g10/g20 on the held-out band margin (§107 rule), not persistence.

## 110. OBJECTIVE GATE (4 word offsets): per-family bar FAIL, aggregate transfer ESTABLISHED (band −259 t −2.1; bought +536 t +3.9); NEXT30 is on the BOUGHT side → flow212 is the sharper GPU0 test (2026-09-12T02:17Z, docs/strategy/2026-09-12-objective-gate.md, S/objaudit/run_gate.sh)

- Seed knob: --batch-seed is a near no-op under --pinned-once --pinned-fixed-seed (pinned_seeds overwrites 196/198 words with blake2b(tape name)); the replicate used is --word-offset K = blake2b(name#K), which re-rolls the pinned words — but --with-town tapes pin the SHOPS, so only weeds re-roll: four draws are one board set measured four times (weed SD 400-510/rung vs board SD ~1,350). More seeds cannot make the 196 boards independent; |t| ≥ 2 per family needs 59 LIVEC42 boards (have 42) and 166 W2 (have 85).
- Board-level pooled (g20 centre − B): LIVEC42 −344 t −1.70 (4/4 −); W2 −216 t −1.43 (4/4 −); LOSS10 +597 t +2.41; TOPTEN +506 t +2.99; TOP50 −624 (n 9); NEXT30 +183 t +0.90 (4/4 +); self-play +391. Aggregate: BAND (LIVEC42 + W2, 127 boards) −259 SE 121 t −2.14; BOUGHT (TOPTEN + LOSS10, 30 boards) +536 SE 138 t +3.90. Objective-weighted win +0.0068 (flat); all 196 rungs −86 coins/episode.
- Reading: the transfer is real in aggregate; the gate as written (each family |t| ≥ 2) is underpowered by construction. NEXT30 was NOT sold by the step — it sits on the bought side — so flow211's 38 % NEXT30 enlarges a bought family while its top-ten cut removes a bought destination: a mixed change. flow212 (top-ten, LOSS10, TOP50 at weight 0; W2 + LIVEC42 52 %, NEXT30 47 %) removes every bought destination except NEXT30 and is the sharper test of "stop selling the band". DECISION: GPU0 → flow212 when flow209 takes its third loss (g30 centre legs running); flow211 stays on GPU1; both read at g10/g20 with S/snr/centre_read.sh (per-family + held-out screen) and judged on the standard legs.

## 111. flow209 RETIRED (3 losses) → flow212 LAUNCHED on GPU0 (pid 1011377, 02:30:17Z); the §73 arms are over: both seeds drifted away from the held-out judge on the original objective (2026-09-12T02:31Z)

- flow209 g30 centre vs B: H30 −470 t −2.95, H30B −627 t −2.14 W0/L6, TOPB2 −178, LIVE62 −28, NEXT30 −116 = LOSS 3/3 (g10 level, g20 −516/−645, g30 −470/−627: the loss is stable in size from g20, matching §106's α ≈ 1 reading). Killed by pid after the /proc cmdline check; GPU0 released.
- Watcher relaunched pid 38398 (watch.sh md5 5974ffcc) with flow212 in ARMS and the NEXT14 held-out column (S/flow212/apply_judge_arm.sh in the quiet window, 0 legs running). flow212 launched from ~/stage_hr/S/flow212/launch_flow212.sh (md5 de043b0f verified): GUARDS OK gpu=0, 196 pinned, --episodes 200, band-only weights (W2 26 %, LIVEC42 26 %, NEXT30 47 %; top-ten/LOSS10/TOP50 played at weight 0). flow211 (GPU1, pid 1006600) at 9.1 GB, training; its g0 record = the seed (watcher SKIP).
- Post-mortem of §73: flow209 (seed B) and flow210 (seed hr) each lost three reads; the recipe's direction was consistent (§104) and unprofitable at every step size (§106) because the objective trades band margin for top-ten/LOSS10 margin (§107, §110). The two live arms test the objective, not the step: flow211 (top-ten 10 %, NEXT30 38 %) vs flow212 (bought families at 0) under the same seed-309 CRN draw. Reading rule: S/snr/centre_read.sh at every 10-gen checkpoint (held-out screen + per-family), judge legs on any record, held-out band margin decides; the first arm whose g10/g20 centre gains on LIVEC-H30/H30B is the first sign the objective was the problem; if both still sell band margin with the destinations removed, the transfer story is wrong and the ES from B is closed outright.

## 112. BAND40 CUT: 48 pinned-town tapes at 2374-2599 (mean 2483), 48/48 byte-exact; B vs hr LEVEL there (+117 t 0.33), continuing NEXT30's gradient down; band support now 82 boards for per-family reads and the next objective arm (2026-09-12T02:44Z, docs/strategy/2026-09-12-band40.md, S/band40/)

- Selection from a 02:19Z leaderboard snapshot (8,686 teams; 593 in 2350-2650), disjoint by episode id (772 known), team name (261) and teamId (54) before the pick; 48 wins from the last two hours; 40 in ids.txt + 8 ext. Registry S/band40/town_schedules.json = 630 rows (shared 582 + 48; shared file not rewritten); tapes on the host with --ignore-existing (568 → 616). Three team-name spellings differ between the leaderboard and ListEpisodes (appear in the corpus only as opponents; 0 episode collisions).
- B vs hr on BAND40 (80 games, WORKERS=4): +117/board t +0.33, W1/L1; upper 2500-2650 +251, lower 2350-2500 +18. B's edge over hr lives above ~2550 (NEXT30 +1,377 at 2550-2650) and vanishes in the LIVE-C band. Incumbent unchanged. Base csvs S/lossflip/band40_{B,hr}.csv.
- Use: (a) per-family objective reads now have LIVEC42 + BAND40 = 82 band boards (§110 needed ~59); (b) flow213 candidate = flow212 + BAND40 at w4 — via the launcher's NEXT_IDS_FILE/NEXT_W_VALUE hooks, but N_PINNED 206 > 198 trips the guard, so --episodes ≥ 208 (or drop a block) in the same edit; (c) a BAND40 judge leg (S/band40/run.sh) is available but NOT added to the watcher (informational; adding legs costs ~5 min per record).

## 113. flow213 STAGED = NEXT QUEUED ARM: flow212 + BAND40 at w4 (236 pinned, --episodes 240, --abs-pairs 45); precheck ALL PASS; launcher md5 33152e42 local = remote (2026-09-12T03:00Z, docs/strategy/2026-09-12-flow213-staging.md, S/flow213/)

- Shares: W2 21.1 %, LIVEC42 20.8 %, BAND40 19.9 %, NEXT30 38.0 %, zeroed families 0 (39 rungs still played = 16 % of wall clock), self-play 0.25 %. Cost +20 % wall clock per gen vs flow212 (983,040 rollouts). abs probe 2 × 45 × 240 = 21,600 ≤ 21,760.
- Judge patch S/flow213/judge_arm.patch (ARMS + NEXT14 column; BAND40 in-sample, no column) tested PASS, NOT applied; apply via S/flow213/apply_judge_arm.sh in a quiet window before launch. Launch: ssh user@remote-host 'cd ~/stage_hr && mkdir -p artifacts/flow213 && CUDA_VISIBLE_DEVICES=<n> nohup setsid bash S/flow213/launch_flow213.sh > artifacts/flow213/launch.out 2>&1 < /dev/null &'.
- Queue order: flow213 replaces whichever of flow211/flow212 first takes three losses or reads worse at its g20 centre; if both centres gain on the held-out band, flow213 waits.

## 114. TRANSFER MECHANISM: the ES re-aims the late price attack (milk/wool/tomato/strawberry up, fertilizer/melon/egg/wheat down, press softened) — floors the top tier's milk, but drops B's day-29 carrot/wool dump against the band clone; a genuine tier difference (c), and the Kaggle ladder is on the losing side (2026-09-12T03:01Z, docs/strategy/2026-09-12-transfer-mechanism.md, S/transfer/)

- Two-purse per family (g20 − B, 4-replicate mean): LOSS10 +597 = 92 % denial (theirs −548); TOPTEN +506 = 55 % denial / 45 % ours; NEXT30 +183 denial; W2 −216 = OUR purse falls (−282); LIVEC42 −344 = 75 % THEIR purse rises (+257) = denial we stop performing. No covariate explains the split (opponent money, our money, B's margin, 16 town-shop features, 40 opponent-play features: |ρ| ≤ 0.13).
- Decode (B vs g30, 8 boards × 30 days, uniform on winning and losing boards): grow_mult FERTILIZER down 99.6 %, MELON 95 %, WHEAT 92 %, EGG unanimously down; TOMATO up 86 %, WOOL up, STRAWBERRY 74 %, MILK 65 %; press down on nearly every product; hire_bias and dev_weight up; forward_days 2 → 3 on day 0 on all 8 boards; one WHEAT → STRAWBERRY tile d3-15.
- Mechanism: vs the top tier (fertilizer-and-mixed-crop engine) extra milk volume floors the milk price they still sell into at d20-29 (107014447: +22 milk, price 118 → 72, −4,864 off them for −2,140 of ours; all of it d15-29). Vs the band clone (pure wheat/carrot, one d29 liquidation) the softened press cancels B's best move: B dumps 54 extra carrot on d29 (96 → 79, +2,292 and −1,657 off the clone); g30 does not (−4,019, all on day 29); same in wool (B floors to 1, g30 leaves 11). Same policy, opposite sign, because the tiers liquidate through different products.
- Verdict (c): not conditionable on anything observable (§78 stands); not a board lottery (fresh-word falsifier S/transfer/freshword.py: LIVEC42-worst pinned −1,556 → fresh −1,405 t −7.6; TOPTEN +294 → +239); attached to the opponent tapes, and the top-tier gain does not reach fresh top-tier opponents (TOPB2 −197, held-out −1,274). The ladder (2400-2700) is on the losing side: NEXT30 level, band −344/−216. The objective's 33 % TOPTEN weight buys a denial the ladder charges us for → flow211/flow212's re-weighting is the right response; the arms' g10/g20 centre reads must show press/grow_mult NOT drifting this way and the band families gaining.

## 115. HR-SLOT PROMOTION RULE ADOPTED: the slot's pool is 2570-2705 (0/205 games vs ≥ 2800); band legs pooled decide, TOPB2/LIVE62 become vetoes; no judge leg covers 2750-2950 (2026-09-12T03:30Z, docs/strategy/2026-09-12-promotion-rule-hr-slot.md, S/promo/)

- hr's opponents (205 rated games; last 40: mean 2637, p10 2568, p90 2705, max 2721; matching opp − me = +4 ± 44). Leg coverage of the last-100 pool: NEXT30 66 %, LIVEC-H30B 75 %, LIVEC-H30 52 %, TOPB2 0 %, LIVE62 0 %, LOSS10 0 %. Per-leg rating correlations over the 4 uploads with both numbers are not identifiable (n 2-4; signs are B's 2200-2400 pool artefact) — rejected. Substitute: on hr's own 60 ladder boards B > hr +1,579 t 3.56 (+10/−2), same sign and scale as the judge legs.
- Elo arithmetic (slope 298 pts/logit, band centred on own rating): +50/+100/+200 rating ≈ +3.9/+7.6/+14.4 pp ≈ +1,000-1,200 / +2,000-2,300 / +4,000-4,600 coins of paired band margin; pooled H30 + H30B + NEXT30 (90 boards, SD 2,066, SE 218): t = 2 at ±436 coins ≈ ±27 rating. A −1,400 TOPB2 loss costs −0 rating at 2630-2820 and −7 at 2900; the same loss on H30B/NEXT30 costs −75/−82 today.
- RULE (adopted, applies to candidates for sub 56143250; B stays): win the slot band — LIVEC-H30 + LIVEC-H30B + NEXT30 pooled as one 90-board leg — with pooled Δmargin ≥ +450 and board-t ≥ +2.0, net flips ≥ 0, no single band leg worse than −400; TOPB2 and LIVE62 are VETOES, not required wins: veto at Δ ≤ −1,400 (TOPB2) / ≤ −700 (LIVE62) (t ≤ −2) or net flips ≤ −4/20 (TOPB2) / ≤ −8/62 (LIVE62); LOSS10 and NEXT14 informational; a candidate advertised as +100 rating must show ≥ +2,000 pooled; a TOPB2 loss between −700 and −1,400 is accepted only with pooled band ≥ +1,200. Re-read at 2750 (P(opp ≥ 2800) = 0 % now, 1.4 % at 2700, 14.7 % at 2750, 71 % at 2820), above which TOPB2 becomes required. Coordinator's decision; the user may veto.
- Gap: no leg covers 2750-2950 (NEXT30 tops at 2750, TOPB2 starts at 2953) = the whole remaining climb. NEXT-HIGH (pinned-town tapes at 2800-2950 via S/nextband/pick.py) dispatched 2026-09-12T03:30Z. NEXT30's margin-to-win slope is borrowed from H30B; measure it on the first candidate judged there.

## 116. NEXT-HIGH CUT (30 tapes, 2782-2946) and APPLIED as the seventh judge column: the ladder is monotone — B 76/68/53/33 % vs hr 76/63/47/25 % across BAND40 / NEXT30 / NEXTHIGH / TOPB2 (2026-09-12T03:57Z, docs/strategy/2026-09-12-nexthigh.md, S/nexthigh/)

- 34 cut from 82 in-band teams (03:31Z snapshot), 34/34 byte-exact; 4 refused by a second disjointness pass on the ListEpisodes spelling (already TOP50 tapes) → 30 boards, 30 unique teams, 0 collisions. Registry superset merged into the shared file (612 rows), tapes on the host (650).
- B vs hr on NEXTHIGH (60 games): +177/board, t +0.38, +2/−0 flips; upper 2865-2950 (n 9) +402, lower 2780-2865 (n 21) +81. B is just above even against the band that contains the cutoff; hr is below even.
- Watcher relaunched with NEXTHIGH as an informational column after NEXT30/NEXT14 (S/nexthigh/apply_judge_leg.sh, quiet window). Cost ~5 min per judged record. Per §115 the promotion decision stays on the pooled band legs with TOPB2/LIVE62 vetoes; NEXTHIGH is the early warning for the 2750 re-read.

## 117. PRESS SCALE SCREEN: B's sell pressure sits at a margin local optimum — softer hands back their price (§114 from the other side), harder is mutual destruction we pay for; scalar press dose CLOSED, no re-centred arm (2026-09-12T04:10Z, docs/strategy/2026-09-12-press-scale.md, S/press/press.patch)

- Switch KAGG3_PRESS_SCALE=<k> (all days) / KAGG3_PRESS_SCALE_LATE=<k> (days ≥ 25) at the decode (brain.py:1053, before floor and cast; inert 32/32, reference 94698/98435/−3737/sig 132). Screen at B, 16 cells, win rate bit-identical to OFF in every cell. ALL 0.75: ours +12 ns / theirs +49 t 3.0 (TOPB2 ours +67 / theirs +178 t 3.3) = softening hands the denial back. ALL 1.25: +21 t 1.3 with ours −16 t −2.5 / theirs −38 = the §57 signature; ALL 2.0: ours −68 / theirs −71 = mutual destruction; LATE 2.0: ours −46 t −3.8 / theirs −5 = past day 25 there is no opponent liquidation left to deny, a harder tail dump is self-harm. Gate for engine legs (LIVE-C positive at t ≥ 1.5 with our purse up) not met; none run.
- §114 confirmed in direction (softening loses), refuted in dose (hardening earns nothing). A scalar cannot separate the per-product mechanism (carrot/wool floor vs the band; milk floor vs the top tier). Recommendation adopted for the training recipe: PIN press in future arms rather than re-centre it (flow210 walked press up on 8/9 products along an axis priced at zero); a per-product probe is possible but not queued.

## 118. NEXTHIGH ANATOMY: the 2780-2950 opponents are the band clone (30/30 in the clone cluster, 0 engine); d15-29 decides (r 0.98); the band-only objective trains against the build the climb faces; the fertilizer engine is a 2953+ phenomenon and only half of that population (2026-09-12T04:13Z, docs/strategy/2026-09-12-nexthigh-anatomy.md, S/nexthigh/anatomy.py)

- 100 opponent tapes (NEXT30 30, NEXTHIGH 30, TOPTEN 20, TOPB2 20), 23 build columns, 2-means: cluster 0 "band clone" n 78 (2567-3000; fert ops 74, fert sold 341, sell rows 250, tomato d29 1.5) includes all 30 NEXTHIGH; cluster 1 "fertilizer engine" n 22 (2577-3081; fert ops 171, fert sold 219, sell rows 156, tomato d29 10.8) = TOPB2 10/20 + TOPTEN 11/20 + 1 NEXT30. NEXTHIGH: 30/30 hire 5 on d0, 11 hands d10, exactly 12 melon → 72 units from d10, 0 melon after d14, 0.0 carrot/tomato tiles by d10; within the band a rating gradient toward the engine (fert ops r +0.57, wheat units r +0.61; 97.6 ops in the upper half vs 128 for the engine).
- B on NEXTHIGH (pinned-town sim reproduces the 53.3 % engine leg): d15-29 decides (r 0.984; wins recover +28,002 vs losses +14,442, t 6.3); d10-14 melon pot is a flat tax (−22.4k on both). B's d29 dump still fires (+9,938 ours vs +9,748 theirs) but nets only +190/board (vs +809 on NEXT30) and −730 on the boards B loses.
- Implication: flow212/flow213's band-only objective (W2/LIVEC42/BAND40/NEXT30) trains against the same build class the 2700 → 2950 climb faces; weighting NEXTHIGH would not reintroduce the §114 transfer (it pushes press the same way as LIVEC42/NEXT30) and is not needed. NEXTHIGH stays the informational column. Above 2953 the population is half engine: the engine answer (milk floor) is owed after the band arm, not instead of it — the 2750 re-read in §115.

## 119. LADDER REFRESH: B's equilibrium is ~2818 (the 2562 projection refuted by B's 54 games above opponent 2450 at 74 %), hr has converged at 2620-2640 and is the WEAKER file; cutoff 2952 ± 15 and flat; top-10 by 09-23 not reachable at the current rate (2026-09-12T04:28Z, docs/strategy/2026-09-12-ladder-refresh.md, S/ladder2/)

- 426 games pulled credential-free. B (156, 117-39): last 40 vs mean opp 2525 at 72.5 %; fitted c (last 100, s 298) 2817 [2678, 2968]; model-free r* last 60 = 2857; c_local rises 2466 → 2830; +24-27 pp above par in every recent window; converges in ~311 games (~58 h). hr (270, 178-92): last 40 vs 2639 at 47.5 % (below par); c 2712 [2603, 2827] but rating flat 2615-2640 for 70 games, honest r* 2620-2640; its free two-parameter fit gives s = 369 (the first identified slope; +24 % on every rating Δ if adopted).
- B overtakes hr on five reads (fitted c +105; matched support 2400-2650 +145 ± 96; paired on 22 common opponents +25.0 ± 11.0 pp t 2.3; same rung 87.5 vs 55.0 %; judge +802 coins t 3.5). Rating crossover in ~29 games ≈ 5-6 h (~10:00Z). RULE IMPLICATION: "a candidate replaces hr, B stays" stands with its justification inverted — hr is the weaker file and the right one to retire; candidates are barred against B (the judge already does); do not move B into the hr slot.
- Leaderboard: cutoff (rank 10) 2951.9, rank 5 3020.2, rank 1 3198; hr rank 330 / 8,691; the cutoff oscillates 2955 ± 13 over 26 h with no drift (the earlier "2943 → 2967" was two samples of the swing). Planning numbers: cutoff 2952 ± 15, rank 5 3020 ± 15.
- 11-day outlook: both files converge within 2-3 days, so 09-23 = equilibrium: B → ~2818 (rank ~63), hr → 2620-2640. P(top-10 with current files) ≈ 0. A replacement in the hr slot needs, vs B: 2850 (rank ~40) ≈ +580-670 pooled band coins (t 2.7-3.1) = one more B-over-hr-sized step; 2967 (rank ~8) ≈ +2,920-3,360 coins (t 13-15) = 3.6× the whole B-over-hr gain, a t never observed on any leg. HONEST VERDICT: top-10 by 2026-09-23 is not reachable at the current rate of improvement; the constraint is strength, not ladder mechanics or a receding cutoff. Realistic plan: B to ~2818 on its own by 09-14, plus one or two B-sized promotions for 2850-2900 (rank ~25-40). Caveats: every 2800+ statement is TOPB2 extrapolation (B has never met > 2631, hr > 2770).

## 120. flow213 PRESS PINNED: press = w3 (64) + b3 (1) whole blocks → --train-only gp,dh,ds,g5,gb5,b1 = 1,126 genes; precheck PASS; launcher md5 b79716c5 local = remote; flow211 gen-10 abs probe survived and wrote a record (2026-09-12T04:31Z, docs/strategy/2026-09-12-flow213-staging.md §8)

- press = h @ w3 + b3 → Outputs.gate → brain.py:1053 _qfloor(base·max(tanh(gate),0)); nothing else decodes from gate; hold does NOT share the head (w2/b2 + ds/fs col 1). No per-gene mask facility exists in the trainer (train_mask takes block names only), so the pin is the --train-only change. Residual: b1/dh still move h, so press can move jointly with grow/sell (priced), never along the free axis §117 priced at zero.
- flow211 gen 10: 1,351 s including the abs probe at 200 rungs / abs-pairs 54; no OOM (§100 D0 cleared); abs 99,187 vs hold 99,203; g00010_record.npy written → the watcher judges it after the remote gate line. The centre read for flow211 g10 (screen + families + cosine + drift incl. press rows) is running via S/snr/wait_centre.sh (its first attempt failed on a missing S/snr/flow211 directory, fixed 04:30Z).
- Queue: flow213 (press pinned) is the next arm; flow214 (a local 3070 twin of flow213's recipe, sized for 8 GB) is being staged as a third band-objective arm.

## 121. BAND WIN/LOSS LEDGER: B's d15-29 gap vs the clone is a SHOP LOTTERY (SMOOTHIE_SHOP keeps the clone's fixed strawberry dump at 122 vs 75) and B reacts to it in the WRONG direction; the strawberry press is the most separating knob → flow213's press pin REVERTED (2026-09-12T05:08Z, docs/strategy/2026-09-12-band-winloss-ledger.md, S/bandledger/ledger.py)

- 120 games (60 NEXT30 + NEXTHIGH boards × 2 seats), pinned-town sim reproducing the anatomy files to the coin. d15-29 margin gap wins − losses +11,439 (t 11.4): OURS −4,395 (t −1.1; B earns MORE on the boards it loses), THEIRS −15,834 (t −4.1). Per product (margin Δ): WOOL +4,927, TOMATO +3,773, MILK +2,550, CARROT +2,415, STRAWBERRY −3,330 — the clone sells the same 248-250 strawberry units at 75 (our wins) vs 122 (our losses): 92 % price effect. d0-14 flat unit-for-unit.
- Covariate: SMOOTHIE_SHOP (strawberry + milk sink) in town → margin −8,339, win rate 80.0 → 41.7 % (ρ −0.30 win, −0.48 margin), holds inside each family; weeds, seed word, opponent rating all |ρ| < 0.3. Mostly board luck.
- B's response (same theta): press3 (strawberry) Δ +16.6 t +5.1, grow_mult3 −66.5 t −4.2 — it tilts the late board INTO strawberry on smoothie towns (tiles 19.3 vs 16.9, grow_mult3 235 vs 190) and out of tomato (2.3 vs 4.8) and sheep (6.4 vs 7.3): +675 strawberry for −3,252 tomato, −2,745 wool, −1,567 carrot, −1,133 egg. Reachable pool ≈ 1.9-3.9k per smoothie board ≈ +475…+975 pooled band coins if half is captured (vs the §119 +600 bar); the knobs reach it (g5/gb5 on items 2/3/7, sheep via gb5/b1; st.shops is in PolicyObs) — a shop-CONDITIONAL per-product response, not the scalar dose §117 priced at zero.
- DECISION: flow213's press pin (§120) REVERTED to the free 1,191-gene set (precheck re-run, host re-synced); flow214 (local) to be launched with the free set too; flow211/212 already free. Read press3/grow_mult3 rows in the drift tables for a shop-conditional move. Caveat: cross-section = selection; +700 is a ceiling on where to look, not a predicted gain.

## 122. Campaign resumed for TOP FIVE with Sol workers and separate-family evidence (2026-09-12)

- Active user goal supersedes the historical Opus dispatch preference: use time-boxed Sol subagents; root coordinates. User also requires each completed code change to be committed with explanatory comments/messages. Interpret "No pooling" as no combined evaluation-family promotion statistic; retain the operational no-polling-loop practice as well.
- Official competition rules were read through the public PageService (rules page 742993): public replay use and accessible external tools/data permitted, no runtime ingress/egress, no private cross-team sharing. Full operational note: `2026-09-12-campaign-resumption.md`.
- Fresh observed fifth-place rating 3015.0; B 2598.06 after 172 completed games, hr 2626.90 after 288. These are observed ratings, not equilibrium fits. Top five remains unachieved.

## 123. Rotating support needs checkpoint conversion: direct resume keeps the old ladder (2026-09-12)

- `load_resume` restores old archetypes/names, and reprobe appends absent requested tapes. Swapping the launcher list therefore accumulates tapes and memory rather than replacing them.
- `S/flow215/rotate_checkpoint.py` writes a new directory preserving trajectory state, removes saved ladder state, and invalidates objective-dependent records. Three tests pass, including the actual loader on archived flow211 g20; full Trainer/GPU rotation is still unverified. See `2026-09-12-flow215-resume-audit.md`, commit 55f4881.
- `flow215_w00` is staged fresh from B for ten generations on 120 verified ROTBAND tapes, 124 episodes, 15,872 absolute-probe rows, 1,191 live genes. NEXT30 stays held out. No real gate is configured: evaluate the generation-10 centre after completion, separately by family. Four checkpoint/window tests pass; data and GPU execution remain pending. Commit 242a648.

## 124. Smoothie guard recovered and REFUSED (2026-09-12)

- Original no-op failure was a day-15-only label even though the guard can activate through day 29. Repaired label and conservative never-smoothie checks pass; bounded OFF identity is coin-exact. This does not establish improvement.
- Existing mode-1 engine evidence versus B, separately: NEXT30 +87 coins (board t +0.49), LIVEC-H30B -60 (t -0.95), NEXTHIGH -81 (t -0.62). All three variants have negative means on both screen families. Close these variants; no promotion. See `2026-09-12-smoothie-recovery.md`, commit 9ded763.

## 125. flow213 launched as a ten-generation fixed-support trial (2026-09-12T07:59:08Z)

- Local full CPU initialization and remote static/file prechecks both passed: 236 pinned tapes plus four carried episodes, 1,191 live genes including press, probe 21,600 rows, remote launcher md5 79f9f215501b7017ac66da7684fd370f and B seed md5 7fcf3948.
- Remote GPU0, process group/launcher 1027375, trainer PID 1027398; actual command line and GUARDS OK verified around 08:00Z. The launch SSH tool session is 20345. Do not duplicate a launch after an observation timeout; inspect the same remote process and artifacts.
- Default generation cap is now ten (874b43b). Judge registration is committed (37fc8e5), routing this arm to held-out NEXT14. The watcher remains stopped; generation-10 centre evaluation is owed even if no record is selected. No trained result is available yet.
- This is an additional-support trial, not a matched comparison with ROTBAND: the latter uses different support. flow214 remains unlaunched.

## 126. Archived g20 centres fail the separate held-out screen (2026-09-12)

- Recovered objective-family reads completed for both arms on 200 episodes each. flow211 W2 -489 and NEXT30 +391; flow212 W2 -406 and NEXT30 +240. These are reused training-family diagnostics, not independent or held-out gains.
- One CPU screen evaluated B and both centres on the exact frozen H30 and H30B games. Reference B reproduces the prior g10 screen's money, margin and shop signatures exactly on all 120 selected games. Full per-theta board coverage was validated before summarizing.
- H30 (30 boards): flow211 g20 -925 coins, SE 231, t=-4.00, flips +0/-0; flow212 g20 -674, SE 240, t=-2.81, flips +0/-2. H30B (30 boards): flow211 -737, SE 293, t=-2.52, flips +0/-4; flow212 -465, SE 396, t=-1.17, flips +0/-4. No family statistics are combined for assessment.
- Both g20 centres are REFUSED by the existing H30 screen threshold. No engine promotion checks or further TOPB2 screen are owed for these refused centres; TOPB2 g20 remains unmeasured. The arms were already stopped. Detail and artifacts: `2026-09-12-g20-holdout.md`, `2026-09-12-g20-recovery.md`.

## 127. ROTBAND raw-cache exclusion audit leaves 32 eligible tapes (2026-09-12)

- Offline reuse found no admissible new tapes: 100 additional cached episodes were own-game or existing evaluation provenance. No HTTP request or corpus import was made.
- Raw-only caches were missing from the original exclusion builder. Root-bound replay info parsing now covers 444 cache IDs, producing 956 excluded episode IDs and 449 team names. Malformed or nested-only provenance is refused.
- All 48 action-verified cuts remain archived with checksums. Sixteen conflict with selected-team provenance and are recorded in `S/rotband/rejections.json`; only 32 enter the private registry. No 120-tape window exists. Stale acquisition lists and launch windows now recheck current team exclusions.
- flow215 remains unlaunched. More eligible public tapes are needed after the acquisition endpoint's deliberate cooldown; do not lower the window threshold or reuse evaluation provenance. Detail: `2026-09-12-rotband-cache-audit.md`.

## 128. B post-sale census supports a seed-only engine pilot (2026-09-12)

- Corrected replay alignment: an action is stored with its resulting observation, so cash delta uses the preceding observation. Exact B seat mappings come from submission metadata, not team labels. On twelve cached B replays, 46/60 early sale-days increase net row cash (median +425); 20/60 also have loose free-tile and idle-slot capacity. Net row cash is not gross sale revenue.
- A separate conservative geometry check uses actual coordinate-list positions at each unit's trailing PASS suffix and shortest paths through unlocked owned cells. It finds seed-only capacity on 19/60 sale-days and fertilizer-plus-seed capacity on zero. Seeds are global; fertilizer needs pickup and FERTILIZE. Four regression tests pass, and root independently reproduces both censuses.
- These are necessary capacity bounds. Seed shortfall, settled affordability, crop value, purchase-before-plant timing and conflicts with other units' remaining targets still need checking. Zero observed fertilizer/animal cases do not close either family.
- Next implementation: default-off seed-only intraday prototype at the existing runtime plan-patch hook, using current permitted observation and our cached plan. Test directly against the unchanged real engine; simulator results cannot assess an unimplemented runtime patch. Full design and exact sample IDs: `2026-09-12-top5-gap-next-test.md`, `2026-09-12-postlot-feasibility.md`. Production remains unchanged.

## 129. flow213 g10 completes without a held-out improvement over B (2026-09-12)

- Ten-generation training exited 0; remote trainer PID 1027398 is absent and both GPUs report 1 MiB. The centre is archived at `S/snr/flow213/state_g00010.npz`, SHA-256 `b05057206c1ddee5e6f5961a094cab49de625a033081fb84b57af6558347272b`; extracted theta MD5 `7401152d1a73e4565571c02042d947e7`, 6,789 finite parameters.
- The manual judge completed with exit 0. Separate margins versus B: TOPB2 -435 (t=-0.83), H30 -59 (t=-0.38), H30B +110 (t=+0.35), LIVE62 -299 (t=-1.62), LOSS10 -381 (t=-1.26), held-out NEXT14 -284 (t=-0.50), NEXTHIGH -272 (t=-0.75). No family effects or statistics are combined.
- No promotion or further training budget is justified by this checkpoint. Preserve all artifacts. Additional fixed support did not produce a demonstrable gain; the rotating-support experiment remains pending sufficient independent tapes. Detailed strict coverage audit: `2026-09-12-flow213-g10-judge.md`.

## 130. Post-sale placement alone is insufficient: watering fixes immediate crop death (2026-09-12)

- The default-off experimental hook preserves remaining base work, target reservations, cash liabilities and global seed reservations. Independent review corrected the seed condition to exact zero balance: an additional seed cannot fund both a base deficit and an extra plant. The isolated source has 36 byte-identical Python files versus arms-next; production source and submitted B theta are unchanged.
- The original eight-game H30 pilot was action-valid and produced six exact purchase/plant transitions. Its +455 margin (four-board t=+0.75, unchanged 50% wins) did **not** demonstrate productive reinvestment: all six plants died as WEED at their first day boundary, with no harvest. Two earlier runs also had a trace NameError; those are invalid execution artifacts, not policy results.
- The corrected hook budgets WATER immediately after PLANT. Tests exercise actual unchanged engine unit/market/day-refresh functions. The verifier now requires purchase settlement, the exact unit's plant transition, watering and next-morning crop identity for every firing. A corrected one-game smoke passed and the injected day-6 MELON at (9,0) produced a successful six-unit harvest on day 16. This establishes the mechanism on one board, not a promotion.
- Full H30 evaluation of the watered hook is running under fresh tag `h30_water`, one worker and 1,800-second cap. The earlier full-run tag `h30_final` was stopped before correction and has no CSV; exclude it. No H30B result exists yet. Details: `2026-09-12-postlot-pilot.md`. Commits 01e9f14, 6931c76, 0920db1, 22d2c16.

## 131. Bounded public replay acquisition reaches 45 eligible tapes (2026-09-12T11:55Z)

- After the deliberate cooldown, one normal-endpoint request supplied episode 108106946; a later 12-request batch accepted and verified twelve more. Current totals: 61 archived drawn-and-town fidelity cuts, 45 eligible selected teams/tapes, 16 retained provenance rejections, zero judge overlap, and no windows. Root's full verifier reproduces these counts and all 48 previously committed checksum records remain unchanged.
- Commit 55bf544 adds the thirteen records and enforces at least five seconds between all picker attempts, including after ordinary HTTP errors. Request-budget, append-only provenance, and immediate 429-stop tests pass. No error bypass or corpus threshold reduction was used.
- The current 180-team acquisition list still has 94 eligible unselected targets. A larger batch is authorized for at most 80 requests, with a 720-second request cap and bounded two-worker download/cutting stages. The cached leaderboard has 441 eligible distinct teams if later expansion is needed. flow215 remains unlaunched until a real 120-tape window is fully verified.

## 132. Terminal restart: all work stopped and preserved (2026-09-12T12:09Z)

- The user explicitly requested shutdown for a terminal restart. All three Sol agents stopped; root's host scan found no campaign process. Remote Flow213 remained terminal exit 0 with both GPUs at 1 MiB. Resume only after the user returns; the top-five goal is unfinished.
- Watered post-sale H30 completed 60 games / 30 boards: margin -256.83, SE 194.02, t=-1.32, own +134.87, opponent +391.70, flips 0/2 and win rate 63.3% to 60.0%. All 44 injected melons reached a six-unit harvest. Four hour-23 WATER verifier false negatives were corrected (679c60c); the preserved games need no rerun. H30B remains unrun and promotion unsupported.
- Interrupted ROTBAND acquisition saved 58 new selections. Totals are 119 selected, 61 downloaded/verified, 45 eligible, 16 rejected, zero windows. Process those 58 before making more requests. If all pass, 103 eligible tapes still require at least 18 more for the normal 121-tape pool. Commit 3c2bc3d preserves selections and small pilot CSVs.
- The final Flow213 g10 seed-room diagnostic finished during shutdown despite a stale child report: ON and OFF were coin-identical on four H30 boards / eight games. Both CSVs are saved under `S/seedroom/`. This is not a full-family invariance proof. The actual remote training source archive is saved locally under `S/flow215/`; use it for the pending real-window initialization check.
- Authoritative continuation instructions: `2026-09-12-HANDOFF-RESTART.md`. The original HANDOFF points there. No new training, watchers, evaluations or network jobs should be launched during shutdown.

## 133. Restart resumed: full ROTBAND window verified; actual initialization catches a gate-only flag (2026-09-12T12:38Z)

- The user resumed work. Host inspection found no campaign process, and remote GPUs were idle. All 37 remote trainer Python files matched the saved actual-source snapshot. The 58 saved selections were downloaded and passed both fidelity modes; a further 24-request, five-second-paced batch supplied 24 more. Both download batches and both cutting batches exited 0. No 403/429 occurred.
- The normal verifier now reports 143 archived fidelity cuts, 127 eligible selected teams/tapes, 16 retained exclusions, five full 120-tape windows, and zero judge overlap. All 61 original checksum records and all 16 exclusions remain unchanged. Window provenance is frozen in `S/flow215/w00_manifest/`, with checksums; later mutable-corpus expansion must not change these first-run inputs. Commit 3a4ccd7.
- Static prechecks pass on the real window. Actual-source CPU initialization reached 120 pinned plus four carried episodes, then refused because the staged `--keep-candidates` flag requires a real gate. Flow215 intentionally has none. Commit 8214f4e removes the flag from launcher and dry-run arguments and adds a static guard against the conflict. A fresh actual CPU initialization is running under its 1,200-second child limit. No GPU training has launched yet; explicit g10 centre archiving/judging remains required.
- Sol's preserved four-board post-sale review reproduces both opponent weed relocations via shared end-of-day RNG indexing. On the -1575 own-coin board, later changes after the injected crop's bundled sale cost -3737; 517 controlled action rows and 58 market rows differ. This establishes broad replanning feedback, not isolated crop return. Commits cae2569, 5c28456, 30870ed; detailed scope and limitations are in `2026-09-12-postlot-cash-decomposition.md` and `2026-09-12-postlot-mechanism-review.md`.
- A one-worker, 1,800-second B-only H30 capture under `off_h30_cash` is collecting the missing baseline replays for a full decomposition. It must pass the existing exact OFF identity check before interpretation. Production B and all submission payloads remain unchanged. Top-five attainment remains unverified.

## 134. Flow215 first window launched; full-H30 post-sale loss decomposed (2026-09-12T12:50Z)

- Corrected actual-source CPU initialization passed at 12:42Z: 120 exact ordered pinned tapes, four carried episodes, 1,191 live genes and B identity. Remote checks then matched 51 source/helper/manifest files, all 120 selected tape hashes, and current exclusions; both GPUs were idle. Actual launched config matches the frozen window and recipe. Launch/config evidence: commit 83558b6 and `2026-09-12-flow215-w00.md`.
- `flow215_w00` started on remote GPU 0 at 12:45:18Z, timeout PID 1033269, trainer PID 1033296, with ten generations and a 10,800-second outer limit. The remote liveness checks and expected trainer banner passed; no generation-10 outcome exists yet. GPU 1 remains idle. Observe this run rather than launching another. Archive/judge its g10 centre explicitly with NEXT30 held out; no watcher or real gate was started.
- Full H30 B capture `off_h30_cash` exited 0 and reproduced all 60 original B games coin-for-coin. Full replay decomposition checks complete coverage and cash closure, recovering own +134.8667, opponent +391.7, margin -256.8333, board SE 194.0151. Opponent actions are identical in all 60 pairs. Three worst-margin boards contribute -7,176 of the board-summed net -7,705; the three largest opponent-gain boards contribute 59.1% of its additional revenue. This is the same H30 result explained, not another performance screen.
- Sol's detailed analysis shows later controlled production/liquidation changes and persistent shared-price effects under unchanged opponent actions; the worst three margin boards have no opponent physical-state change. See `2026-09-12-postlot-h30-cash.md`. This supports no promotion or new variant. All local download, cutting, initialization and baseline-capture jobs are complete. Production B remains unchanged; top-five attainment remains unverified.

## 135. Real 90/30 successor staged; post-sale target displacement identified (2026-09-12T13:12Z)

- A further bounded 32-selection batch completed under normal acquisition pacing and two-worker limits. The normal verifier now reports 175 archived fidelity-verified cuts, 159 eligible tapes, the same 16 rejections, six full windows, and zero judge overlap. All 143 previous checksum records, exclusion bytes, and the frozen w00 seal remain unchanged. No 403/429 occurred.
- Reviewed helper `ee0addf` and ten passing focused tests support immutable successor staging. Root's actual invocation and independent manifest validation passed: `S/flow215/w01_manifest/` keeps exactly 90 launched tapes and adds 30 new tapes, while preserving the full 175-archive evidence and 159-entry eligible registry. Corpus/snapshot commit `026a7fc`; detailed hashes and checks are in `2026-09-12-flow215-w01-staging.md`. Mutable window indices are not substitutes for this anchored membership.
- The existing GPU 0 trainer remains active, PID 1033296; generation 2 is complete at the 13:12Z observation. GPU 1 is idle. Training scores do not establish promotion. No second run, watcher, checkpoint conversion or judge was started. Still require successful w00 g10 completion and explicit centre judgment, with NEXT30 held out, before deciding on the staged successor.
- H30-only replay diagnostic `e5d84b6` finds all 44 injected targets used by OFF B before the melon's first harvest ten days after planting, median first reuse two days after injection. Chronology uses the first firing in each of 40 games: median first SELL divergence four days later. This supports displacement risk and broad replanning feedback, not an isolated causal assignment or a promotion. See `2026-09-12-next-lever-review.md`. A bounded read-only census of the existing metadata-selected twelve public B replays is checking forward vacancy without consulting outcomes or using future state in a policy.
- Production and submitted B remain MD5 `7fcf39485bae65ee84171957c5843814`. Top-five attainment is still unverified.

## 136. Public B12 census finds no forward-vacant planting capacity (2026-09-12T13:16Z)

- The fixed twelve metadata-selected public B replays reproduce 60 sale-days and 46 positive-net-cash first-sale rows on days 1–6. Corrected geometry, current-day target reservations and immediate watering leave six route opportunities in six distinct episodes. All six targets are reused before the ten-day melon horizon: three after two days, one after three, two after five; four strawberry and two melon. Each opportunity has only one feasible target, so the alternative-target upper bound is also zero.
- This is a separate descriptive public replay corpus, not a pooled H30 statistic or a performance screen. Remaining same-day replay actions substitute for the cached plan and may omit the runtime's current BUY-turn reservation; funding, seed balance and exact hook eligibility remain unproven. The fixed twelve-episode sample supports no population confidence claim. Future occupancy is retrospective evidence only and cannot enter a runtime policy.
- Root reproduced the result and four focused tests passed. Commit `96e3fef` preserves helper, tests and the report with all thirteen input SHA-256 identities: `2026-09-12-forward-vacancy-public.md`. No further post-sale planting pilot is justified by these data. This does not claim that every possible crop substitution or reinvestment policy is closed.
- At 13:16:28Z Flow215 w00 remains active on GPU 0, trainer PID 1033296, with generation 3 complete (433.6 seconds for that generation). GPU 1 is idle. No g10 centre or judgment exists yet; continue observing this run and then perform the explicit separate-family judge. Next 90/30 data are staged, but the successor has not launched. All local acquisition, cutting and census jobs are complete; production B is unchanged and top-five attainment remains unverified.

## 137. Premise corrections and guarded rotation prerequisites (2026-09-12T13:52Z)

- The fertilizer arbitrage premise in §34 is refuted by its original thirteen raw replays: day 0–9 quotes span 77–100, early BUY request quotes 81–89, and quotes first reach 30 on days 21–25. All public quotes match the existing pricing function; reference-engine hash matches the lock. The approximately 1,915-coin term allocated gross sale revenue and never subtracted costs or traced purchased units. No storage-buy pilot follows. Commit `1186a27`, `2026-09-12-fertilizer-premise-correction.md`.
- The fixed public-B12 convenience corpus overlaps ten of those original, historically loss-selected replays. Its metadata-only selector does not remove source-cache selection bias. Earlier vacancy counts stand, but do not treat this corpus as an independent or representative ladder sample.
- Post-sale hire census `003a434` finds twelve priority routes on seven episode-days on days 1–9, all day-5 wheat WATER, with twelve immediate tile-yield units. The broader days 1–26 subset has 21 routes. Omitted legal FEED/CARE/early-HARVEST/other-WATER remains unvalued; the priority subset is not a bound on total labor value. Root fixed coordinate/alignment issues and confirmed that hired hands automatically deposit before day-end removal. Two focused tests and full root census reproduction pass. No hire pilot is justified by the immediate watering channel alone.
- Commits `84e773d` and `762cc2b` provide converted-resume identity checks, a real zero-generation CPU initialization path, and a guarded fresh w01 launcher. The loader uses actual source `load_resume` with an instrumented state holder: its passing fixture tests are loader-unit proof, not full Trainer initialization. Six focused successor tests pass. Actual w00 g10 conversion, full resume initialization, remote synchronization and successor launch are still unrun; the immutable 90/30 successor manifest remains ready.
- Complete-day-plan conditional selection is distinct from previously refused unconditional macro offsets. Saved ISEARCH hindsight maxima show ranking reversals but not predictable gains. Any selector must use current permitted observations and pass leave-tape-out calibration; hidden/future states may only form offline labels. See `2026-09-12-runtime-plan-selection.md`, commit `75d9229`. NumPy cost measurement and minimal offline branch plumbing are bounded tasks in progress, with no production change.
- At 13:52:44Z Flow215 w00 is active on GPU 0, trainer PID 1033296, generation 8 complete, GPU memory 9,036 MiB. GPU 1 is idle. Require successful g10 completion, explicit centre archive, and all seven separate judge families with NEXT30 held out. No new training, automatic watcher, promotion or upload has occurred. B is unchanged and top-five attainment remains unverified.

## 138. Complete-plan branch identity established; rotation budget rule fixed before outcomes (2026-09-12T14:10Z)

- NumPy planner benchmark `d473668` measures twelve H30 baseline dawn states, three fixed boards at days 0/5/15/25. Total median/p95 latency is 90.469/95.414 ms for one plan, 180.998/191.952 for two, and 363.865/391.613 for four; four-call maximum 522.309 ms. All repeat builds, direct-versus-runtime cached plans, and hour-1 tuple reuse agree. This is local build cost only, excluding decode, candidate generation, scoring and competition-host differences. It is not the public-B12 corpus or a performance result. See `2026-09-12-numpy-plan-timing.md`.
- Offline fixture `8a1ce68` constructs the first fixed ISEARCH development board's day-5 dawn. NumPy and JAX decoded macros/plans agree; injecting the frozen B plan reproduces unmodified simulator advance, and duplicate B branches are state-exact. Compactness +1 changes fourteen plan elements and the resulting full-state hash, while immediate money/shed values remain identical. The first crew+1 candidate deduplicated; its already-inspected equality and reconstructed evidence are disclosed. This is exploratory correctness plumbing, not an oracle/predictor performance estimate. Full state, tape/seed and future RNG/action hashes are audit-only, outside permitted selector inputs. See `2026-09-12-planselect-branch-fixture.md`.
- Root recorded a prospective bounded w01 decision before any g10 judge outcome, commit `486aa01`, `2026-09-12-flow215-continuation-rule.md`. A valid level/mildly mixed endpoint can justify one actual 90/30 rotation; H30 <=-300, TOPB2 <=-1400 or net flips <=-4, LIVE62 <=-700 or net flips <=-8, or any separate family's negative board t <=-2 stops this trajectory. These are experimental-budget guards, not a newly claimed old promotion rule or pooled statistic. All actual conversion, full CPU initialization, source/tape checks and free-GPU prerequisites remain required. No automatic w02 follows.
- Last remote observation at 14:09:26Z: existing trainer PID 1033296 remains active, generation 9 complete; no final g10 centre or judge result exists. The final generation includes an absolute probe. GPU 1 stays idle. Do not restart or substitute best_abs for the explicitly owed centre. A new bounded development diagnostic is extending B/compact+1 branches to season end on the first four fixed H30-development tapes, both seats; no policy or selector has been trained. B remains unchanged and top-five attainment is unverified.

## 139. Flow215 w00 g10 completes; explicit centre judge launched (2026-09-12T14:13Z)

- By 14:11:38Z the existing remote run completed generation 10, `done` and `EXIT=0`. Trainer/timeout PIDs are absent and both GPUs report 1 MiB / 0%. The final generation took 891.0 seconds including its absolute probe. No restart occurred.
- Root fetched and hash-verified the checkpoint, centre, config and logs under `S/snr/flow215_w00/g10/`. State SHA-256 `456b0b1934fad2ad904cd832bda1e8bddef69525fc46ea6f5bf2b6faacd2bf1e`; launched config hash unchanged. Generation/t/Adam counters are all 10; theta/m/v finite. Explicit `state.npz["theta"]` equals the trainer's centre array.
- Candidate `artifacts/kagg2_games/thetas/flow215_w00_g10s_hr.npy` has MD5 `6585b78e3ed8bee29a3cfe59f717c3a3`, 6,789 parameters, exactly 1,191 changed from B and L2 distance 0.0141138872. This is centre identity, not a best-absolute or promotion claim.
- A host scan found no existing judge and ample CPU memory. Root started the explicit seven-family judge with four CPU workers, a 7,200-second cap and `/tmp` lock, tool session `96175`. NEXT30 remains held out. Await the same handle, then run the strict complete-coverage audit; no candidate outcome is known yet. No conversion/full resume initialization or successor launch has occurred. Production B remains unchanged and top-five attainment is unverified.

## 140. Flow215 g10 H30 crosses the prospective continuation guard (2026-09-12T14:18Z)

- The same explicit judge remains active under session `96175`. TOPB2 and H30 individually pass strict canonical coverage, both seats, finite/non-void values and no duplicates. TOPB2: 20 boards, margin -677.575, board t -1.16454, own +65.375 and opponent +742.950, seat-game flips 0/5. H30: 30 boards, margin -868.6167, t -2.56038, own -55.0833 and opponent +813.5333, flips 0/0. These are separate effects; no pooling.
- H30 alone crosses the predeclared -300 margin and negative t<=-2 continuation guards. This checkpoint does not justify the staged w01 rotation. Continue all five remaining judge families and final strict audit; no successor training or rescue run starts. `paired.py` flip counts are seat-games, while the older promotion note's denominator is imprecise; this H30 refusal does not depend on interpreting flips. See `2026-09-12-flow215-g10-judge.md` for current partial coverage.
- The separate first-four-development-tapes, both-seat day-5 compactness branch diagnostic remains bounded and in progress. No selector has been trained or promoted. B remains unchanged and top-five attainment is unverified.

## 141. Flow215 full judge refuses shipped settings; seed-room mismatch is newly active (2026-09-12T14:35Z)

- Judge session 96175 is terminal exit 0 at 14:33:14Z; strict audit passes all seven separate families. Margins versus B: TOPB2 -678 (t=-1.16), H30 -869 (-2.56), H30B -715 (-2.82), LIVE62 -200 (-0.74), LOSS10 -595 (-1.14), held-out NEXT30 -426 (-1.41), NEXTHIGH -495 (-1.70). H30/H30B independently refuse the staged w01 continuation. Full exact results, CSV hashes and report: `S/snr/flow215_w00/g10/judge_audit.json`, `2026-09-12-flow215-g10-judge.md`. No family rerun or GPU extension is owed.
- Sol diagnostic `97b62a4` finds actual-source OFF matches arms-next on all ninety sampled B-generated dawn states for both B and Flow215 g10. B ON/OFF is 90/90 identical. Flow215 differs on day0 of all three starts: requests [1,5,1] animals but plans to buy [1,4,1]; OFF seeds [10W,8C], ON [10W,9C], planned PLANT/WATER 18 to 19. C is CARROT, not strawberry; root corrected an initial verbal mislabel against `spec.CROPS`. This is planned-action evidence only, scoped to these states, not whole-trajectory performance or an explanation of every loss.
- A bounded four-H30-board ON/OFF actual-engine pilot is running with two workers and exact OFF-versus-main-judge identity required. It tests a distinct source-aligned policy; the shipped-switch refusal and no-w01 decision remain intact. No promotion or upload is ready.
- The first eight-state delayed-label run timed out at 600 seconds with zero labels. Reviewed runner `724687a` adds flushed stage logs, atomic dawn/day6 checkpoints, strict hash/stage identity and overwrite protection; six checkpoint-only tests pass. Root's revised 600-second run is live under session 26093 and has saved eight dawn states. No terminal-label or selector gain has been established. B is unchanged; top-five attainment remains unverified.

## 142. Seed-room pilot supplies no rescue; eight delayed labels validate (2026-09-12T14:43Z)

- Four-board seed-room engine pilot `036b2e1` completed both arms within 240-second caps, two workers. Actual-source OFF is identical to the completed Flow215 main judge in all fields on 8/8 games. ON−OFF margin +41.5, board t +0.04, no flips; per-board effects +156, -1755, -884, +2649. ON−B margin -1703.8 (t=-2.90). No full-family expansion or training rescue is justified. This is whole-season outcome evidence, not a trace-isolated extra-carrot return. B is unchanged.
- Revised delayed-label runner `724687a` completed within 600 seconds, root session 26093 terminal exit 0. All eight B terminal own/opponent/margin results exactly match the preserved ISEARCH simulator baseline by tape/seed/tape-seat keys. The fixed day5 compactness alternative changes paired-board margins by +626, +549, +144, -1777. Mean -114.5; hindsight max with B +329.75. This four-board exploratory slice supplies no predictor or promotion estimate. It does show that equal next-day cash/inventory can hide later effects. Exact artifact/hash report: `2026-09-12-planselect-day5-labels.md`.
- The next bounded staging task generalizes only to the full thirty-tape H30-development family, both seats, same single alternative, with distinct artifacts and frozen observation-only feature/calibration choices before the remaining labels. H30B/NEXT30 stay outside fitting; no family pooling. No full run or learned gate has started. All preceding jobs are complete, GPUs idle, top-five attainment still unverified.

## 143. Full development labels validate; frozen day-5 selector fails (2026-09-12T15:04Z)

- Reviewed runner `2178a6d` completed the full thirty H30-development tapes, both seats, under root session 1881, exit 0, 14:54:54Z–15:01:46Z within 600 seconds. It ran 60 B branches, 42 distinct alternatives and one duplicate B. All 60 terminal B own/opponent/margin values exactly reproduce the preserved simulator baseline; the eight original target rows are identical. Root independently verified coverage, targets and checkpoint hashes. No resume or real-engine alternative run occurred.
- Frozen calibrator `5cfeb92` completed under root session 55291, exit 0. Both seats are held out together in every fold; scaling and zero-variance removal use only the other 58 rows, ridge alpha is 10 with intercept, and prediction >0 selects compact+1. Eleven focused tests pass in agent/root runs, including held-out feature/target leakage exclusion and baseline/target corruption refusal. Root independently recomputed all decisions, board aggregation and fold membership.
- Gate mean margin -130.25, SE 110.77, board t=-1.18; own -172.48, opponent -42.23. It chooses the alternative on 28/60 rows, changing twenty plans. Always-alt margin -192.00 (t=-1.14); per-seat hindsight maximum +187.63 is descriptive and cannot select at runtime. The predeclared positive-mean/t>=2 threshold fails. Stop this exact fixed day-5 selector without feature/alpha/threshold/transform retuning or a held-out engine pilot. This does not close all complete-plan selection approaches.
- All data are the single H30-development family, with the first four outcomes seen before recipe freezing; this is exploratory calibration, not pristine OOF inference. H30B/NEXT were not read for fitting, and no family statistics are pooled. Exact artifacts, hashes and scope: `2026-09-12-planselect-all30-result.md`. Preserve labels, fold reports, logs and ignored checkpoints. No local campaign job remains live, Flow215 w01 stays refused, production B is unchanged and top-five attainment is unverified.

## 144. Ladder advances slowly; population source-alignment audit staged (2026-09-12T15:22Z)

- Three read-only public API requests, at least five seconds apart, completed 15:07:51Z–15:08:03Z without 403/429. B: 205 completed games, 149 wins, latest 2639.4678, team rank 362; fifth place 3016.3. B's last 40 games contain 26 wins and +54.16 rating. hr: 317 games, 201 wins, 2619.0649; last 40 rating -8.68. Per-file observations are kept separate, with no strength fit. Exact raw responses/hash receipts and reproducer: `32ef9f9`, `2026-09-12-ladder-1508.md`. No replay import or upload occurred.
- Independent Sol reviews agree that B's seed-room invariance and g10's mixed ON/OFF mean do not establish perturbation-rank/gradient equivalence. Existing boundary-theta evidence proves a changed nearby landscape, but no campaign artifact measures actual population preferences ON versus OFF. Root recorded an exact generation 0 no-update audit and budget stop rule before outcomes, `dfeae9e`, `2026-09-12-seedroom-population-plan.md`.
- Staging under `S/seedrank/` captures the actual archived trainer immediately before its first `_play`, preserving the real JAX split-key, NumPy initialization consumption and +half/-half order. Root/independent review caught the wrong mutable tape-window default (already different from frozen w00), tie changes incorrectly counted as strict reversals, missing fitness-weight hashes, and the need for actual CPU capture-only validation. These are being corrected before launch. No population result or optimizer update exists. Root owns any later reviewed two-GPU, 1,800-second-per-arm diagnostic. This is distinct from the refused g10 rescue and w01 continuation; it supplies no automatic training authorization.

## 145. Population audit code reviewed; instrumented CPU preflight active (2026-09-12T15:33Z)

- Committed `8674216` implements the exact real-generation capture, guarded no-update boundary, paired source/config/tape/mask/fitness-weight identity, actual pre-rank fitness inputs, strict antithetic reversals distinct from tie changes, and the prospective dfeae9e decision. Six focused root tests pass. Raw ON results must also reproduce the original first-generation mean/best win read; failures preserve evidence and cannot enter comparison. No population result exists.
- First CPU preflight session 9300 terminated exit 124 without a capture receipt. The imported driver's SIGTERM handler prevented ordinary timeout 240 from enforcing its cap; root verified probe PID 44310 still live beyond the limit and killed that specific process. All further wrappers use `timeout -k 10`. This failed initialization is preserved, not interpreted as a passing preflight.
- Root session 8537 is the single live retry, beginning 15:30:33Z with a 900-second cap plus 10-second hard-kill grace. It uses actual CLI initialization, including built-in archetype liveness evaluations, then stops before the population rollout or optimizer. Flushed phases prove source archive and all 120 frozen tapes validated; actual CLI initialization remains active. Source is frozen while this process lives. Observe the same handle; no duplicate or automatic restart.
- All 132 remote input files matched local SHA-256 values after committed-helper/source staging. Both GPUs remain unused by this diagnostic. Successful actual capture review and a fresh GPU/process check are required before either 1,800-second population arm. Preserve remote-input manifest/receipt and preflight log; no trained checkpoint, promotion or upload exists. B remains unchanged and top five is unachieved.

## 146. Population capture guard fixed after actual initialization (2026-09-12T15:45Z)

- Root session 8537 is terminal exit 1. The actual CLI completed its 992 archetype liveness episodes, then the helper failed on a nonexistent Trainer.save method before capture. This is not a preflight pass or population result. Preserve preflight_retry.log and preflight_guard_failure.json. The earlier timeout remains separately recorded.
- Root removed only the invalid guard; apply_gradient/_snapshot guards and theta/m/v/t/adam_t checks remain. The CLI checkpoint writer is after generation and unreachable once StopSetup unwinds the driver. Seven focused tests pass, including an interface test against the hash-bound actual Trainer AST. Independent Sol review agrees on the fix and exact rung allocation and finds no further capture blocker.
- Both modes now clear JAX caches after selecting the switch, preserving RNG/state and forcing their own population trace. Receipts and comparison require this provenance; exact ON reproduction of original first-generation mean/best is still mandatory. Additional config assertions bind margin scale, chunk, carry allocation, warm fraction and zero market jitter.
- Corrected CPU session 2368 started 15:43:18Z under timeout -k 10 900, with output S/seedrank/preflight_corrected and its separate log. It remains in actual initialization; no cached-liveness shortcut, population rollout or optimizer step. Observe the same handle. Two GPUs remain idle at 15:44:43Z. Root-owned launch_pair.sh has independent review, including an added receipt-to-remote hash check before its two once-only, 1,800-second arms. It has not run; updated helpers still require synchronization and a successful capture.

## 147. Actual CPU capture passes; paired no-update audit launched (2026-09-12T15:51Z)

- Corrected root session 2368 exited 0 by 15:49:04Z. Real CLI initialization and exact generation-0 capture pass: eps 2048×6789, candidates 4096×6789, 120 pinned tapes plus expander2/rusher2, unchanged theta/m/v/t/Adam and no checkpoint. Receipt SHA d57363d528b0324c7e7a51cbcb0b8d5571476d19ddb42abe728dcbf30719c239; source fix/launcher 0be388c. Root rechecked both B MD5 values.
- All 133 updated remote hashes match; old manifest preserved separately (d2cb16a). Successful CPU receipt copied and launcher binds it to remote archive, manifest, B and tapes. Both GPUs were idle immediately before launch. No source/tape mismatch was waived.
- Root SSH session 18616 launched the pair once at 15:50:38Z. Remote launcher1040183; ON GPU0 timeout1040190/probe1040192, OFF GPU1 timeout1040191/probe1040193. Each is capped at 1800 seconds with forced kill after10 and explicit CUDA backend. Output artifacts/seedrank_pair_20260912, separate logs/results. Initial observation confirms both actual CLI initializations. Observe these same processes; no automatic retry/update/training/promotion. Frozen dfeae9e comparison remains owed after complete paired outputs and exact ON reference validation.

## 148. Missing hiring census reconciled; exact suffix fixture staged (2026-09-12T15:58Z)

- Independent Sol reviews agree the existing B12 census leaves legal existing-asset work unvalued. They reconciled to the frozen B12 d1–9 scope, exact observed cash, post-unit-action spawn, all later hire liabilities, protected reserve/feed inventory, no same-day target overlap and one conflict-free itinerary. Future work is diagnostic-only. Proposed modeled-value thresholds are withdrawn; no automatic pilot.
- The current static Manhattan helper cannot prove execution/overflow. Root assigned one bounded missing baseline/alternative own-seat suffix fixture under S/hireasset, twelve-minute development and 180-second CPU smoke caps, followed by independent review. No full census, policy change or performance run yet. Cases changing EOD topology need actual weed RNG or UNVALUED classification; a zero restricted subset cannot close the full channel. Details: 2026-09-12-post-sale-existing-assets-review.md.
- Existing GPU pair root18616 remains live; at 15:57:26Z both arms had completed actual initialization and exact generation-0 capture, with no output receipt yet. Observe same PIDs and 1800-second caps. No rank interpretation, training or promotion follows from partial logs.

## 149. Fresh ladder observation remains below top five (2026-09-12T16:01Z)

- Exactly three paced first-attempt public requests completed 15:59:56Z–16:00:06Z, all 200, max30 seconds each under cap120. No 403/429/retries/import/upload. Raw hashes and summaries preserved under S/ladder2/snapshot_20260912T1600; root reproduced the summary exactly.
- B211 completed/153 wins, latest2647.7103, teamrank349/display2647.7; fifth3025.8. Since15:08, six more games/+8.24rating/rank362→349. B last40W26, oppmean2628.07, rating+54.06. hr322/202wins,2605.3682, last40W18,opp2642.21,delta-16.41. Files remain separate, no fit/pooling. Top five unachieved; no candidate is ready for promotion.
- Existing GPU pair root18616 remains active at16:01:08Z, both evaluating the captured populations, memory about8950MiB each/util95–100%. The bounded own-seat hiring fixture is still staging; no full census/pilot.

## 150. Population audit refuses original ON; upstream numerical variation found (2026-09-12T16:14Z)

- Root18616 is terminal, pairfinished16:05:31Z ONexit1/OFFexit0; GPUs idle. ONmean .6280547380447388 differs from original .6280192732810974, best exact. Saved integer outcomes imply +36 halfpoints (18wins equivalent), not reductionrounding. Allrawarray/remotehashes and paired input fingerprints pass. Comparisonwritesvalidfalse and refuses; no rank/gradient interpretation, training/promotion or rerun.
- Independent review plus root reproduction finds rounded initialization variation before toggle/cacheclear: currentON/OFF differ19/124 rows(sumabsolute855,max76); original/currentON20/124(sum623,max116). This needs exact rawinput/execution reproducibility work, not an expected-score waiver. Detailedfailure/receipts preserved under S/seedrank/seedrank_pair_20260912 and 2026-09-12-seedroom-population-reference-failure.md.
- Bounded ON-only liveness diagnostic staging captures actual initialization inputs/rawmoney then compares cached and retraced992-row repeats on oneGPU, with no population/optimizer. No newGPUrun yet. Separate hiringfixture v5 addresses independentreview corrections; root tests8956/replay37845 active, no census/pilot.

## 151. Hiring fixture reproduced; ON-only liveness diagnostic launched (2026-09-12T16:23Z)

- Exact seeded hiringfixture v5 passes root tests8956 (five tests) and full replay37845, both exit0. Root receipt byte-equals agent v5, SHA f0983ea1b86229918f10e6d7248c96c199de2ae0424fd14b75e681b111955ae8. Independentreview fixes cover exact declared tilefields, targetoverlap, fixedcase and all input/helper identities. Commit07f5e46. This is two-case plumbing including already-known priorityWATER, not fundedcensus/terminalgain; reserve/allliability checks and broader coverage remain pending.
- Liveness helper1ee5de8 has independentreview and six focusedroot tests passing. All136 remoteinput hashes match. Root51198 launched once16:22:20Z on GPU1, timeout1047223/probe1047224, cap900 pluskill10. Original initialization is live; GPU0idle. It captures raw992×12 money and exactinputs, repeats cached then afterJAXcacheclear, allON/no generationpopulation/nooptimizer.
- Observe same handle/PIDs and preserve finalrawreceipts/logs. Cached/retrace evidence is limited to this livenessprogram; no populationrank interpretation follows and the failed originalONcheck is unchanged. No automaticrestart/training/promotion. B/topfive state remains the16:00 snapshot.

## 152. Cached identical-input liveness differs (2026-09-12T16:36Z)

- Root51198 finished16:28:58Z exit0, diagnostic verdict cached_repeat_mismatch. Root verifies remote/local NPZ/receipt/raw digests and identical inputs. Cached173 changed elements/32 rows; retraced183/34, int32 money, maximum609coins each. No population/update/checkpoint. Execution instability precedes cacheclear; exact backend cause unresolved. Original failed population comparison remains invalid.
- Both GPUs idle and all136 staged inputs match at16:35:36Z. One unchanged-harness deterministic-XLA control is frozen in 2026-09-12-liveness-repeatability.md and undergoing independent review before launch. No automatic population run/training or historical-reference waiver follows any outcome.
- Funding census author is addressing blind-review provenance, exhaustive108-row and later-hire capacity guards. Exact shipped-plan replay and original h_star/cash_reserve recovery are reviewed sound. Full census remains unrun; two-case exact suffix fixture is the existing proof.

## 153. Funding census complete; deterministic control live (2026-09-12T16:42Z)

- Reviewed funding_census fixes complete, including selector hash-beforeimport, final dependency drift checks,108unique keys, full future-hand capacity and later-hire identity refusal. Five root tests pass. Root32928 terminalexit0 undercap180:108/108 whole-day plans exact,84FUNDED/24UNAVAILABLE,13futureBUY_LAND/no laterHIRE or unvalued orders. Root independently checks hashes/arithmetic and raworder counts. Receipt b953f660cd1feed1973b73524e0cd1954561c89b5ef225e586f08c2c42d39914. Funding only, not productivework/terminalgain; B12 convenience bias remains.
- Deterministic-XLA control13744 started16:37:17Z GPU1 timeout1050470/probe1050471 undercap900+kill10 after independentreview and same136input checks/freeGPUs. Flags disableautotune/excludenondeterministicops, JAX/JAXLIB0.10.2/driver580.126.20, persistentcache env unset. Actual initialization live; original failedpopulation reference unchanged. Stable scatter could still differ from sequentialengine semantics; sourceaudit underway.
- Two Sol agents independently propose remaining observation-safe existing-asset itineraries/actualsuffix coverage on84funded rows. No new fullopportunitycensus/performancepilot or productionchange.

## 154. Deterministic smallbatch repeats; constructed tile fidelity defect proved (2026-09-12T16:48Z)

- Deterministic control13744 terminalexit0 at16:45:24Z, allthree992×12 rawarrays bitwiseexact. Root verifies raw/file hashes and old/newinput/source/config/B/window equality. Flagged/unflaggedoriginal differs1161elements/221rows, max609coins. Both GPUsidle. This proves only flagged same-process smallbatch repeatability; originalpopulation reference remainsinvalid, no training orpopulationcomparison follows.
- Independently reviewed structuralfixture42447 terminalexit0 CPUcap60. Lockedengine duplicateHARVEST gives farmer3/hand0; archivedsim farmer3/hand3; HARVEST/PASS control exact, targetyield0 allcases. Actualimportedarchive paths andprepublish sourcehashes checked. Receipt4bccea7567d826bec6c4c51384fd4a41af906354ea90b4df3644e1828526921e. Preserve agentfirst displaymap failure separately. Constructed counterexample does not prove relevant collisions in actual tapes or cause of nondeterminism. TwoSol reviews planning bounded realtapetrace, unrun.
- Hiring scope reconciled: STATIC84FUNDED legalop ledger, single-target directWATER/HARVEST/CARE orFEED(+CARE), deterministicturns/y/x/ops order, every omittedlegal/combo UNVALUED. Wheat recomputed from predicted post-hire-hour-unit shed minusfuture withdrawals, because priorfundingfield omittedsamehourunitactions. Authorimplementingbounded10min, tests60; fullstaticrun and any suffix/EODcampaign awaitreview. No productionchange orpromotion.

## 155. Static opportunities enumerated; exact changed-row inputs captured (2026-09-12T17:01Z)

- Root54813 terminalexit0 cap180 afterfourroot tests/independentreview:84fundedrows,17STATIC_SELECTED_ARRIVAL_UNVERIFIED(allHARVEST),67NO_RANKED_VISIT_FITS. Acrossincompatiblevariants35HARVEST/12WATERfit, noFEED/CARE;5909ledgerentries/2409nonpriorityunvalued. Exactdependency/funding/routehash/time/target/selection audits pass. No proposedroute/EOD executed, no gain claim. Receiptc6a27459cd1ea48e5570e7d73044be0cfba84f3d04f5cc0d8388654e6d354aa1. Firstselected107764944s0d8hire11,target[5,2],NORTH,NORTH,HARVEST requires seededtopology-aware fixture before physicalproof.
- Root24129 terminalexit0 cap120 afterthreeroot tests/finalindependentreview: actualCLI inputs intercepted insideinitial_probe before_eval, fulltree exactbothremote runs, no evaluator/episode/population/update/checkpoint. Row58/tape108100156/pair1/seat0/seed88567952/tape_ctl[0,3] bound to actualwords andraw target. Receipt84954905ab51606944cce39dd8f45508d42a7f89e1cd084a9b61c7d05ecd7473,NPZ07454686620365bd8f06a0d6d0b2a5ef548bb1d91b87c0b087f4dbed7a096a49. Preserveinitialconfig-abspath mismatch andsupersededpreguard capture. Currentproofexplicitlydoesnotclaim local/remotebyteconfigequality.
- BothGPUsidle/allcurrentrootjobsterminal/agentsidle. B MD5recheckedunchanged. Proposedfixedrow58exactarchivetrace andfirstselectedHARVESTseededfixture remainunimplemented/unrun, eachneedsboundedcodereview. Originalfailedpopulationcomparison remainsinvalid; no training/promotion/upload/topfiveclaim.


## 156. First selected harvest executes; exact archived row58 trace launched (2026-09-12T17:24Z)

- Fresh17:05 public ladder snapshot57d330c: B218/159wins,2668.8355,teamrank308; fifth3019.2, gap350.4. Three paced first attempts all200 and root hash/summary reproduction. B last40W26/+52.32rating; hr328/205wins,2604.8793,last40W17/-27.39rating. No pooling or promotion; topfive remains unachieved.
- Exact first static-selected harvest fixture9887606: root24343 exit0 cap180, four root tests and independent review. Fixed107764944s0d8seed1408844682, hire11 and NORTH,NORTH,HARVEST12–14: newhand gains3WHEAT and banks all3, no overflow, hiringcost21. Both-seat undeclared physical state exact beforeEOD. Removedcrop alters shared RNG and thirdtownshop YARN_STORE to PET_CAFE. No net/terminalgain inference; future yield, prices, replanning and opponent effects remain unmeasured. Receipt5c01725ac8e5aa73bdb87ebd8e5d0c7ed09225095342d04f3356481457951e54. No full17/84case campaign.
- Reviewed row58 helper3fa9d8c and launcher/141-input manifest6b6567e committed; three root tests pass. All remote hashes matched17:22:37Z, both GPUs idle. Root39301 launched once17:23:52Z GPU1, timeout1057096/python1057097, cap300+kill10. Same captured inputs/exact archive/full120tape union and deterministic flags. Direct and instrumented outputs must match exact12-int32 target and trace cover719steps before classification is interpretable. No host episode transcription or repaired simulator. Preserve invalid outputs, no othercase retry.
- Original failed population reference remains invalid. Event-level locked-engine/sequential/singleton comparison remains a separately reviewed pending gate. No optimizer, new training, production modification or upload.


## 157. Row58 direct identity passes; instrumented phase reaches fixed timeout (2026-09-12T17:31Z)

- Root39301 terminalexit124 at17:28:52Z, exactly300sec. Direct archived result exact12-int32 target, atomiccheckpoint SHAe38841aedd975f6198036ada089632130afcd961298248baf6165804e0d7c979. Instrumented phase has no traceNPZ/finalreceipt. No collision result, identity-mismatch claim or cause inference follows. Six remote/local artifacthashes match root audit; timeout/python absent, bothGPUs1MiB. No automatic retry/othercase/source repair/training.
- Independent next-stage designs reconciled: full collision census descriptive; first supported duplicateHARVEST causal fixture only, allothergroupsUNVALUED. Singleton archive/locked and collision-only maskedsequential/locked must agree before parallel mismatch interpretation. Semantic physical projection plus inactive-field invariance; fullturn additionally refuses atomicPLANT overdraw ambiguity. No valid trace means this postprocess cannot run. Any new execution plan must account for measured compilation cost and retain this timeout.
- Completed evidence and restartnotes saved. All agents idle. Production/submission B MD5 both7fcf39485bae65ee84171957c5843814. Topfive remains unachieved;17:05rank308 remains latest. Original failed population reference unchanged.


## 158. Measured compilation budget justifies one unchanged trace follow-up (2026-09-12T17:37Z)

- Independent blind reviews agree on one900sec follow-up: prior directcheckpoint timestamp17:27:42.805070097Z means230.805sec direct stage, only69.195sec left for instrumented compile. This changes computational allowance only, not target/source/input/evaluator/identity719coverage or scientific gates. Prior timeout retained; no further automatic retry/case substitution. Plan/launcher d04d075 frozen before outcome.
- All141 remoteinputs match17:33:59Z; helper065269eb... unchanged, bothGPUsidle. Root57303 launched17:35:22Z GPU1, timeout1059692/python1059693, cap900+kill10, fresh artifacts/row58_trace_budget900_20260912. Direct phase active. Observe same handle.
- Conditional event fixture code staging only; no event execution without valid complete trace, root audit and independent review. Original population reference remains invalid, no source repair/training/promotion/upload.


## 159. Exact direct repeats; CUDA-only callback dispatch fails before tracing (2026-09-12T17:46Z)

- Root57303 terminalexit1 at17:43:12Z after470seconds within900cap. Direct12-int32 target exact and checkpointbyte-identical prior. Instrumented JAX0.10.2 debugcallback requires CPU localdevice, unavailable under frozen JAX_PLATFORMS=cuda. Actualerror and atexit tokenerrors preserved. Zero callbacks, emptyNPZ, instrumented:null, valid_trace:false. This is runtime instrumentation failure, not negative collision evidence or computed output mismatch.
- All8remote/local artifacthashes match root audit; PIDsabsent, bothGPUs1MiB. Receipt6815b48d2eac6fd0bb56a60df5c4a56d1f90a5598e1239464f96c8373c326299. No further retry/case substitution under this plan; no eventpostprocess. CPU-only callback smoke did not cover GPU callback dispatch and cannot validate this launch environment.
- Conditional event-helper finalreview fixes include raw evidence, precise allState/inv_seq invariance, semantic projections, source/input/runtime proof, distinct outcomes and isolated-collision-only claim/fullturnUNVALUED. No trace/kernel/episode run. Independentreview readiness ea3bb6e agrees full unit-index actionfold after atomicPLANT validation is correct semantic boundary; unroll/JAXloopperformance undecided. No source repair, optimizer/training/promotion or upload; original failedpopulation reference remainsinvalid.


## 160. Actual GPU callback plumbing qualified before new episode runtime (2026-09-12T18:07Z)

- Probe40549 terminal1 in2s: all3callbacks/93rawarrays/fixedmath exact but erroneous NumPy-onlyleafguard refused CPUjax.Array. Source JAXdebugimplementation explicitly api.device_put onCPU. Originalreceipt preserved. Reviewedv2 requires actualnp.ndarray or actualjax.Array with nonempty allCPUdevices; rejects ducktypedimpostors and retains allpayload/output/source/runtime/orderguards.
- V2root9461 terminal0 at17:59:53Z in2s cap60. Three CPUcallbacks/93rawarrays/direct-instrumented-fixedmath exact, defaultGPU remains soleRTX3090. All7remote/localhashes and root audit pass, fourfocusedroot tests. Receipt60d74c5996fa1ade03bbed20c57be24c451c52a80620c37d2aefc18920023a45, rawNPZbbb17f496bdfcbac049c51e70aedce70a9906c770b046b4601947c38c1b34a6f byteidenticalfirstprobe. No game/simulatorstep. Commits7132d90/32c9f0a/69d7cb5.

## 161. Corrected dual-platform exact trace launched (2026-09-12T18:07Z)

- Twoindependent reviews agree corrected runtimecuda,cpu is justified by explicit callbackfailure, without evaluator/source/input/target changes. Newhelper3ff5f92... adds CPU/GPUavailability andstrictCUDA1/cacheenv/provenance; oldhelperrefusesnewenv and staysimmutable. Rootthree inheritedtests pass. Plan69d7cb5/finalsidecarguard74335dc committedbeforelaunch.
- All150remotehashes ac9502428aa38debbd36dd8d326f3e930526906e1ac090b4b758c8268d65d30b match18:05:04Z, bothGPUsidle. Root26261 launched18:05:19Z, timeout1065322/python1065323, cap900+kill10. Actual processGPUUUID maps tophysicalGPU1. Freshoutput row58_trace_gpu_cpu_20260912, directphase active.
- Probeproof onlyqualifiesruntime. Freshdirect must equal12-int32 originaltarget/bothpriorcheckpoints; instrumentedmustequal+719orderedstates. Preserveinvalidoutputs/noautomaticretry/othercase. Eventchecker newhelperbinding requires deliberate review aftervalidtrace; no source repair, population/training/promotion/upload. Original failedpopulationreference unchanged.


## 162. Ladder remains below target; corrected-runtime direct identity verified (2026-09-12T18:11Z)

- Root52821 publicsnapshot18:08 terminal0: B223/160wins,2656.69245,teamrank339/display2656.6; fifth3022.9/gap366.3. B last40W25/+39.05rating,oppmean2640.40. hr332/208wins,2612.92018,last40W18/-24.92rating,oppmean2624.03. Threefirstattempt responses200, rootrawhash/summary reproduction. No pooling/import/upload. Commitd128e28.
- Existingmonotonic5secguard ran, recordedUTCgaps5.000134/4.998759s. RootstrictUTCgapassertionrefused and remainsnotpassed; no requestrerun. Futurehelperbuffer5.1sec avoids clock/read jitter nearboundary. Exactoriginaltimestampsretained.
- Root26261 stillactiveinstrumentedphase. Newcuda,cpu direct checkpoint420a5e31edb65d8af485ff3d93c3934707f62ee42da7651297366ae60fb77fda at18:09:16.838Z matches originaltarget andbothpriorCUDA-onlydirectvalues exactly shape12/int32. Rootchecks GPUdefault/CPUavailable/exactnewhelper/env. This is freshdirect identityonly; no completeinstrumentedtrace or eventproofyet.


## 163. Exact trace completes and exhaustive isolated collision audit finds one defect (2026-09-12T18:36Z)

- Corrected trace26261 completed18:13:19Z exit0,480seconds/cap900. Direct/instrumented exact frozen12-int32 target; all719steps/31arrays/27State schemas/source/input/census verified. All17groups seat0, zero duplicateHARVEST. Original HARVEST fixture has no eligiblecase and staysunrun. Trace a69c6b5; B unchanged.
- New all17 post-trace plan dfde64e frozen before event outcomes, both independent designs agree. Reviewed helper8894df8/threepuretests; root38344 CPUcap180 exit0 in85seconds. Originalreceipt cab0622b54efec07e8a7b338535a92b3b11d1323cc5be560c703c5a0be5b0f88 reports16match/1difference but root32623 rejects serialized intermediate engine snapshots: canonical_engine retains tile references and13earlier snapshots mutate later. Raw simulator arrays remain preserved. No silent receipt rewrite.
- Independently reviewed verifier9dc596f runs only lockedengine controls, no U.apply_units/episode repeat. Root83044exit0/cap60:3077rawarrays verified,34singleton+34carried controls exact, every mask/State/inv_seq invariant and fullsource/input/B hash pass. Deepcopy snapshots validate16matches/1difference anew. Verification ce0d5966250eb30e45399f41016d81c0c3dde520474b60f627d0a07b76a6a2bc. Original snapshot failure remainspartofevidence.
- Isolated difference atstep707/day29h11/seat0tile80:unit4WATER thenunit7HARVEST. Carrotyield2 becomes3 before sequentialharvest; parallelreads2. Unit7inventory5vs4, sole semanticdifference. Candidate theta differsfromB. This establishes requested-action/prestate fidelity only, not fullturn/terminalimpact, population/laddergain or previousGPU nonrepeatabilitycause. Two independent next-step reviews considering completecapturedvector; no repair/training/promotion/upload. Topfiveunachieved.


## 164. Complete unit-vector persistence gate agreed before execution (2026-09-12T18:38Z)

- Both independent Sol reviews choose one step707 complete unit vector from the same trace. Seat0live0..11 opcodes[1,3,6,3,6,2,7,7,3,3,1,4], seat1farmerPASS; no PLANT/shedoperation. Assert those facts, use exact unmasked2x17arrays, compare one archived apply_units with every live lockedengine action in seat/unitorder. Deepcopy all reference snapshots.
- Both-seat fullsemantic/rawinvariance checks distinguish clean soleCARROT5vs4 persistence, ambiguous additionaldifferences, and no persistence. Any technicalgatefailure refuses; no newcase/retry. This is unitphaseonly, not market/town/EOD/fullturn/terminalproof. Plan2026-09-12-row58-full-unit-phase-plan.md, CPUcap180, freshoutput, helperunimplemented/unrun.
- A clean result would justify preparing an isolated simulator correction plus fidelity/performancegates, not training orpromotion. Prior fullfold/atomicPLANT repair boundary remains; no sourcechange has been made.


## 165. Actual complete unit-phase discrepancy persists; isolated repair staging begins (2026-09-12T18:47Z)

- Fullvector helper65bcd90/fivepuretests/independent review pass. Root85369exit0 in25seconds18:44:32–18:44:57/cap180. Root69518 verifies58rawarrays/13engine snapshots, exacttrace707fullvector/prestate, all invariants/source/input/B identities. CLEAN_PERSISTENCE: only unit7CARROT4archivevs5engine remains, all other both-seat semanticpaths exact. Receipt a3225703dbea67dd6c3d71acb85ade55f611ca3af4127af002946ae60d3af35a. No root simulatorrerun.
- Independent blind repair designs agree full scalar unitfold after one real-mask/atomicPLANT pass, including sharedshed/evolvingPLACE and inv_seq. Staticunroll andJAXforiloop sharetransition, performance must be measured. Production/reference/submissionunchanged. Isolatedoverlay and comprehensive fixture suite now beingauthored; no amendedkernel/test executionyet. Source-bound stager/testrunner ensure existingtests importisolatedsrc.
- Unitphaseproof does not establish complete-turn/EOD/terminal/Bexposure/livenesscause or populationrank benefit. Original failedpopulationreference and closedFlow215continuation remain unchanged. No training/promotion/upload.


## 166. Isolated ordered executor passes focused and disjoint gates (2026-09-12T20:03Z)

- Overlay b5aeeb2c implements the complete scalar unit fold after atomic planting validation. Both forms pass40 focused tests including exact trace707;32 unchanged scripted DROP/PLACE tests also pass, no skips. Stage/engine provenance is retained; production and submission remain unchanged.
- Root82784 exits0 in40.01seconds undercap180:688 input-selected disjoint vectors give exact27-field archived/loop/unrolled outputs.31 conservative exclusions remain outside this gate. Root87739 independently verifies selection,81arrays and all recorded hashes without rerunning a simulator. Receipt ef11aca023b860217806d5962726fa17dd371ab1ed9dbd191ecadd3600e237c6.
- Both independent Sol reviews agree on the first whole-season integration smoke: unchanged wide-crew node seed1164543749, CPUcap1200+kill10,29EOD+lastpartialday and>=12hands. Explicit private-state coverage gaps; enhanced full-state/tape parity still needs its own reviewed implementation. Plan unit-order-season-plan.md, staged/unrun at this checkpoint.
-19:43 ladder snapshot c4485c1: B228/162wins,2654.3704,teamrank349; fifth3028.2,gap373.9. Three public responses200 with5.1second pacing and independent summary/hash audit. No pooling or topfive claim. No new training/promotion/upload; original failed population reference remainsinvalid.

Wide-crew launch update: root45712 is live after4187c9f/d5cced9. Final independent static review passes; launcher pins all staged sources/tests and engine lock and requires exactly one passing named case, no skips and both source/engine markers. CPUcap1200+kill10, same-handle observation only. No result yet.

## 167. Repaired loop passes the first complete-season integration gate (2026-09-12, after20:08Z)

Root45712 completed exit0 at20:08:27Z in166.655seconds/cap1200. The exact fixed
wide-crew test passes with no skips and both source/engine binding markers.
Root37824 and independent Sol review recomputed all185 bound paths and the
one-case JUnit evidence without running another game. Execution SHA256
49679a194c3ca5413e69981f7c3d078c36969758a7979da669b4fc8d81b1f40c.
See [result and scope](2026-09-12-unit-order-season-result.md).

The loop default matches both seats at29 EOD boundaries and final partialday
on the existing test fields and satisfies the>=12hands assertion. This leaves
hourly state, private inventories/order, positions/counts/hires, shop identities,
tape parity, B behavior and GPU performance unresolved. Enhanced hourly helper
is being prepared with independent design review; no game/training launch yet.
No pooling, production changes, promotion or upload. Topfive remains unachieved.

## 168. Reviewed hourly parity gate launched after full-season smoke PASS

Commitff3393e freezes the enhanced helper18d6699f, validator6466a39f and
launcher0ac805fd. Root20254 two pure regression tests pass; independent final
Sol review finds no launch blocker. Root82935 is LIVE, one CPUcap1200+kill10,
fixed wide-crew seed1164543749. Observe samehandle, preserve anyfailure, no retry.
The combined gate retains and validates720 aligned states,719 rawturn states,
29 EODpairs,31 direct/instrumented boundaries, all720 canonical engine states
and719 both-seat rendered actions. Runtime/source/import and rawschema/hash
checks are mandatory, including rawhour23 inventory timestamps before EOD.
No result yet. This closes hourly integration gaps only if it passes; row58tape
parity, B/seedroomOFF and GPU performance/repeatability remain separate work.
No training, pooling, promotion or upload. Topfive remains unachieved.

## 169. Full hourly state/action parity verified; stay focused on top five

Root82935 completed20:33:08Z: child0/helperPASS,265.103seconds/cap1200,16hands,
720canonicalframes and719both-seat actions exact. Original launcherexit1 is
retained: validator ops.py import lacked package context. New reviewed adapter
ac4a283 plus import regression; root82857 saved-only auditPASS, independent Sol
saved-only auditPASS,188boundfiles/168rawarrays/31boundaries exact. No game rerun.
Executiona2e7e718, receipt91416bc1, rawdb602089;
[complete result](2026-09-12-unit-order-enhanced-season-result.md).

User explicitly steered: do not drift from top-five objective. Keep validation
bounded to one exact captured tape case, GPU performance/repeatability, then
fresh bounded training and separate-family evaluation against B if gatespass.
Do not grow a general simulator campaign absent a concrete blocker. Exact next
row58 orientation is tapephysical0 versus zero-policyphysical1, despite
inputseat0/candidate placement: tapectl[0,3] overrides that candidate's actions.
Recorded seat0 collisions are tape-replayed, not candidate-generated or B.
No training/promotion/upload; submitted B unchanged and topfive unachieved.

## 170. One exact tape gate launched; GPU preparation stays conditional

Commit74e6146 freezes helper e7309970, auditor d8f8246d, launcher3d355f43 and
planf6158c62 after independent Sol static review found no launch blocker.
Root62258 two pure regressions PASS; root45517 verifies all120 frozen inputs
without JAX/engine imports. Root17719 launched one CPUcap1200+kill10 at about
21:00Z, fresh S/unitorder/row58_tape_season_20260912 and sidecars. Observe that
same session; no retry/mirror/extra case. Initial preflight passes; result pending.
Only this tape0/zero1 orientation is valued. B MD5 remains7fcf39485bae65ee84171957c5843814.
Next GPU qualification design is static and conditional; no remote job,
training, pooling, promotion or upload. Topfive remains unachieved.

## 171. Exact tape parity PASS; proceed to GPU qualification

Root17719 completed21:07:05.971758Z, exit0/helperPASS/root auditPASS in389.291277s.
Independent Sol saved-only audit alsoPASS,4.7seconds; no JAX/game/engine imports
or data changes.720frames719actionpairs118rawarrays140boundfiles exact; final
physical tape0/zero1 money[141865,59347], day10[17396,2172]. Source/runtime,
package-parser, zero-policy, state/action/EOD and seat-label checks allpass.
Execution4570f980, receipta6ca8626, raw e0e9e6b8. One case, no retry or mirror.
[Result and hashes](2026-09-12-row58-tape-season-result.md).

The agreed tape fidelity gate is complete. Next is implementation of the bounded
GPU qualification design, reviewed with explicit batched input expansion,
realistic8192 shape, exact cold/warm timing, replicated loop comparisons,
memory/repeatability limits and an evaluator-only cost projection. Training and
judging must share the intended shipped seed-room OFF contract. The captured
ON source remains timing/fidelity evidence, not an ON-trained/OFF-judged waiver.
No new GPU job/training/promotion/upload. Topfive remains unachieved.

## 172. GPU qualification implemented; first performance arm live

Commit e1ee159 froze the four-arm protocol. Initial launch exit1 at21:35:47Z
stopped before Monitor/JAX/arms: artifact directory is a symlink and the manifest
used its logical path. Preserve that zero-arm SETUP_REFUSED evidence under
S/unitorder/gpu_setup_failure_20260913 (receiptf5ea8884). No performance result
exists from that attempt. Reviewed e8b6405 moves the root guard into durable
refusal handling and freezes fresh v2 canonical paths; seven pure tests PASS.

V2 manifest e696b0ee,141 exact files, helper2a6b649d, protocold7ca66f5,
launcheraba9ea6c. Remote path/hash/idle checks passed21:43:03Z. Root98842 now
LIVE, loop-1 GPU helperPID1070516, actualCLI cold992 phase,522MiB first process
memory observation. Four fixed arms,900each/3660+kill10 outer. No result yet;
observe samehandle and preserve every failure. No actual performance-arm retry.
After PASS, OFF confirmation and new training remain separate required work.
No pooling/training/promotion/upload; topfive remains unachieved.

## 173. GPU v2 refused; repair only the observed monitor overhead

Root98842 terminal exit1 at21:51:13Z,473.161s. Loop-1 helper exit0/PASS with
exact raw outputs, source/state/config/runtime invariants. Frozen outer audit
refuses82 monitor gaps>200ms,max0.248824s; independent saved-only Sol audit
reproduces that refusal. Three remaining arms never started. No selecting the
survivor, resuming the closed protocol or using its diagnostic times to qualify.
Executionc79edd84, receipt5721927e, rawa1379161, monitor4f3c3fae saved unchanged;
[complete result](2026-09-13-unit-order-gpu-v2-result.md). Both GPUs idle after exit.

New persistent NVML monitor addresses that specific subprocess overhead. Its
idle-only API proof has41samples/max0.050109s; it does not prove loaded cadence.
A separate prospective four-arm protocol must retain every original gate and
exclude the refused arm. Exact shipped/OFF source substitution is being prepared
in parallel, with no new games. Next training stays conditional on qualification
and matching shipped-source initialization. No pooling/training/promotion/upload;
B unchanged and topfive remains unachieved.

## 174. Targeted monitor repair reviewed; fresh qualification live

Commit403a16d freezes a separate prospective protocol after the concrete v2
monitor refusal. Persistent NVML monitor a5ca2e61 uses documented v2 allocated
memory, retaining idle<=64MiB and reporting reserved memory separately. The
original d7ca66f5 protocol and2a6b649d arm stay exact; adapterbce47f1d changes
only monitor and strengthens input binding. Root93408 fourteen pure testsPASS,
independent Sol launch reviewPASS. Corrected idle proof21samples/max0.0500923s,
allocated1MiB/empty processes; prior API proof and v2 refusal remain untouched.

Manifest888b4e2f binds155files/131unchanged arm inputs. Bundlea1ff5d2d verified
on the named remote host, all155hashes/canonical output/idleGPU PASS22:11:54Z.
Root SSH session92254 launched22:12:07.740567Z, loop-1 helperPID1084782.
First55seconds:1086samples,maxgap0.053130s,zero gaps>200ms,solePID1084782.
Four fixed arms900each/3660+kill10 outer; no result yet. Observe that same
process; do not reuse the closed refused arm, duplicate or retry. Remoteoutput
/home/user/kagg3/artifacts/unitorder_gpu_nvml_20260913. [Plan](2026-09-13-unit-order-gpu-nvml-plan.md).

Exact shipped/OFF source construction alsoPASS, receipt3db9c2bc: packagedplan
19ad2816 plus selectedunits is the only intended two-source replacement;
16other shared modules/main/theta exact B. No extra games. Prospective OFF
confirmation/fresh-training design requires exact full992 inputs/output and
state/source match beforegeneration1, with fixed canonical dataset paths and
only run/gens normalized between processes. Training remains conditional.
No pooling/training/promotion/upload. Topfive remains unachieved.

## 175. Two qualification arms pass; OFF implementation prepared

Same root92254 execution remains live. At22:30:29Z loop-1 and unrolled-1 each
completed child0/helper/outer armPASS. Raw outputs botha1379161; receipts161e5caf
and8d26aa16. Loop peak4962MiB/maxgap0.057651s; unrolled5030MiB/maxgap0.060532s.
Unrolled-2 PID1099113 has started; loop-2 remains unstarted. No complete four-arm
qualification or selected variant yet. No restart or substitute measurement.

Commitdbb1e73 freezes OFF helper26e118a5/protocol836858b5/launcher3f91de4b/
plan212e916d. Root54160 eight pure testsPASS; independent Sol reviewPASS after
binding exact992/8192 inputs to the completed qualification's first selected
arm receipt before eitherOFF evaluation. No ON/OFF output comparison. Exact
packagedplan+units source, rawinput/index audit, canonical121externalB+tape map,
all source/config/state/runtime/monitor/cost guards and Btheta/best_abs_theta/
pool[0] identities required. One900secchild/960+kill10outer, no retries.

No OFF manifest, transfer or launch yet: full qualification and independent
saved audit must pass first. B remains unchanged. Static training-boundary draft
is in progress under bounded Sol task; no generations/updates/checkpoints,
family pooling, promotion or upload. Goal remains top five.

## 176. Qualification passed; reviewed OFF bundle awaits transfer approval

All four new NVML arms passed; execution ended22:48:41.807289Z, wrapperexit0,
elapsed2194.066737s. Root61187 and independent Sol saved audits are identical
94fd559b. Frozen comparison selects loop: warm8192 medians10.891108/10.903538s;
unrolled advantage-0.021919 fails the required5percent improvement. Evaluator-only
ten-generation projection7171.768403s<=9000. All raw outputs a1379161 exact.
Remote helper PIDs absent and both GPUs idle; lingering SSH92254 is a transport
handle, not a running qualification. Do not rerun. Result/evidence commit6ddf80f.

Reviewed OFF manifest768b8bed binds173local files/135arm inputs/121external B+tapes.
Bundle /tmp/unitorder-off-bundle-20260913.tar.gz,2612514bytes,SHAba4c9989 is ready
locally, not transferred or run. Automatic review rejected the identical scp
twice; it recognizes the host/task but requires explicit approval for this
private payload to user@remote-host:/tmp/unitorder-off-bundle-20260913.tar.gz.
User approval question is pending. No bypass or retry without an actual answer.
After approval: unchanged transfer, exact preflight, one selected OFF execution,
root and independent saved audit, then conditional fresh training.

Training helper7e3584cb/protocol26423a82/launchercac41b07 are committed a8b7142;
root21821 six pure tests and independent Sol final static reviewPASS. Exact
audited OFF initialization/state/input boundary precedes native generation1;
ten generations/updates required with10800/10860s caps. No training manifest or
launch yet. Remain on the bounded route to separate-family evaluation against B.
No pooling, production change, promotion or upload; top five remains unachieved.

## 177. Approved OFF execution passed; exact training bundle prepared

User explicitly approved the quoted OFF private bundle transfer; scp exit0 and
remote preflight06:02:11Z passed173local/121external hashes, fresh paths and idleGPU.
RootSSH77568 singleloop-off completed exit0/fullPASS06:10:15.046967Z in469.214404s.
Root88923 and independent Sol saved audits335adbd0 are identical. SystemPython3.10
initial audit attempts stopped on trailing-Z timestamp parsing; the unchanged
auditor passes under projectPython3.11. No GPU rerun, source or evidence rewrite.
Execution46ec9f3c, receiptef5cb4cb, outputs4ea0f79e, rawinputs8f0fee66. Full input,
state, shipped-source, repeatability, monitor and cleanup gatesPASS. Peak4952MiB,
maxgap0.087961s/9326samples; evaluator-only10gen6426.002564s. See completedOFFresult.

Training manifest8197e1a5 committed51dea16:187local/140arm/121external, exact
audited OFF proof. Saved training auditor9e1a5b63 reviewed/committed590af75 before
manifest. Bundlef85acef7,3276205bytes,188safe regular members independentlyPASS.
Automatic review rejected its transfer once because the explicit user approval
covered the previous exact OFF bundle/path. Approval is now pending for the
training bundle at user@remote-host:/tmp/unitorder-train-off-bundle-20260913.tar.gz.
No transfer bypass or retry without approval. After approval, exact remote
preflight precedes the single10800/10860s ten-generation training execution.
No live GPU job or training launch. B unchanged, no pooling/promotion/upload.
Use explicit separate-family judge runners against the candidate private_stage;
old watcher worktree routing and pooled promotion rules must not override this.

## 178. Training transfer approved broadly; exact initialization gate passed

User explicitly approved ALL training bundle transfers in this work. The
unchangedf85acef7 training bundle transferred; remote preflight06:28:50Z passed
187local/140arm/121external hashes, complete OFF proof, fresh paths and idleGPU1.
RootSSH83690 started the single ten-generation protocol06:29:10.029737Z,
helperPID1121008. At06:42Z its generation1 guard has passed exact OFF input,
output, cold/post-B state, config/source and final input rehash. Nativegeneration1
is running; no positive generation log yet. Monitor through06:39:03Z11870samples,
maxgap0.063985670s,no cadence violations,solePID1121008,peak9048MiB<=12000.
One10800s child/10860s outer cap plus kill grace, no duplicate/retry/resume.

Judge plan now accounts for the concrete archive layout: only scripts/train.py
is archived. The eventual local judge must use a fresh adapter linking immutable
candidate private_stage/src and the hash-bound local evaluator scripts. Saved
auditor334e48c1 reviewed; root31550 eleven pure testsPASS, including exact saved
Flow215 seven-family metric reproduction. Prospective source/keys/theta/base
manifest and later output-hash audit manifest remain distinct, with exact
family counts and no pooled statistic. No judge or promotion has run; B and
submission unchanged. Topfive remains unachieved.

## 179. First native generation completed; fixed judge inputs reviewed

At06:52Z helperPID1121008 and rootSSH83690 remained live. Native generation1
completed in802.44s, training mean_win0.6131768823; this is not a B comparison.
GPU process9048MiB, wrapper exit absent. Same single bounded run continues.
All187 locally bound training inputs were independently rehashed unchanged.

Sol and root verified judge inventory647b8b19:231 input hashes,424 exact row
keys, seven separately checked B subsets and empty training-ID intersections.
CPU environment review resolved candidate-versus-opponent import scope; the
plan now records concrete CPU settings and limited preflight/log attestation.
No candidate or game output was fabricated and no judge has launched.

User asked about24GB versus12,000MiB: the latter is our conservative stop
threshold, not a throttle or hardware/competition requirement. Preserve this
frozen run; revisit the cap before future training. User also asked whether
rising tomato prices affect planting. Shipped brain/plan/runtime bytes match
local source: daily crop decisions receive current price, stock, town demand
and production; no direct historical price-trend input. Tomato first yield is
eight days. A specific replay is needed to distinguish sensible resource
allocation from late/weak response. Record this question for interpretation
after the current candidate evaluation; do not divert the live experiment.

## 180. User-requested tomato replay review; third training generation complete

Sol reviewed exact Kaggle submission56161192/episode108450468, completed
06:44:56Z. Root independently checked the full720frames/30dawn table and
reconstructed B crop targets on the exact recorded observations. Seat1 B
finished100280 against113447. Four successful tomato plantings occurred
days15/16/19/21, matching the four requests; days10–14 requested none despite
requesting strawberries/melons. Tomato rose73(day15) to166(day29), while the
opponent grew none and already led19441 atday15. Evidence supports late/small
allocation, not a proven missed win. Demand/stock/production inputs could
support learned anticipation even without explicit price history; no altered
policy or counterfactual engine game was run. See the dated episode review.

At07:07:46Z the same training helperPID1121008 is live with3 completed native
generations:802.44s,610.03s,611.06s; cumulative2023.5s. Latest training mean_win
0.6137133837, process9048MiB, wrapper exit absent. This is not a B comparison.
Continue the same bounded run, final saved audits, then separate-family judge.

## 181. Both remote GPUs active; audited seed310 trajectory launched

User explicitly authorized both remote GPUs, continuous Sol research, localGPU
for fast evaluation, and all training bundle transfers. Original seed309 remains
unchanged: PID1121008/rootSSH83690, six native generations at07:46:34Z,9048MiB.
New seed310 initializer passed216.564110s, root/Sol audit a3f119dd byte-identical,
peak980MiB,maxgap0.064046s. Seed-specific full state is distinct despite fixed
raw probe equality; exact new full-state proof gates training generation1.

Reviewed seed310 manifestb3fc988a and bundle0a14861b preserve206local/141arm/
121external including all187original inputs. Commitbc9b3c6; authorizedtransfer
and07:51:24Z remote fresh-path/idleGPU0 preflightPASS. RootSSH59892 started
07:51:44.058052Z,helper1130257 confirmedalive07:52:19Z duringcoldinit. One fresh
10gen run,22000MiB threshold,10800s child/10860s outer pluskill10. Final native
centre only, dual saved audits then each seven-family campaign kept separate.

Read-only research falsified the maturity-value-input premise in the selected
replay: tomato's projected stream ranked below requested alternatives. No new
feature/training branch follows. Exact early-gap reconstruction instead locates
17440 gross melon receipts before B's later melon cycle in a19441 dawn15gap;
rotation reproduced both artifacts byte-exact. This timing evidence does not
reopen previously losing forced-melon interventions. First-population macro
reachability diagnostic reports zero day0 melon targets across8192perturbations;
independent Sol reproduction matched byte-for-byte. No policy promotion, upload or topfive claim.

## 182. Nine original generations; fresh rank249; objective evidence corrected

At08:08:25Z original helper1121008 is live with9native generations complete,
last609.07s/cumulative5684.5s,9048MiB. Independent seed310 helper1130257 is live
withfirstgenerationrunning and full initialization guardPASS. Same bounded jobs.

Fresh public snapshot08:07Z passed3pacedHTTP200 reads after a sandboxDNS failure
was resolved through network escalation. Rawhashes and leaderboard row membership
verified by root: existing B rank249/display2684.1, fifth3030.1, gap346.0. B has
286completed/195wins and latestepisode2684.192606. No new trained submission has
been uploaded; the topfive goal remains unachieved.

Root/Sol older population audit found objective signconflict855/2048pairs,
blend followsown622 versusrelative233, cosineblend-own0.926/relative0.561.
Independent review corrected aggregation: pinned_once weights120tapes at2 and
four scripted episodes at1, denominator244. Final helperpinscapture/archive/
trainer and reconstructs rawweightedfitness/savedgradient; root outputf4fb4c48
matches exactly. This old pre-repair descriptive evidence neither changes the
live objective nor authorizes a replacement or an automatic training ban.

## 183. Seed309 dual-audited; clean seven-family judge running

Original ten-generation run completed08:25:48Z,6998.612s,outerPASS. Complete
archive0b1f01a9 downloadedwith70-membercustody; root/Sol savedaudits3bc626c6
areidentical. Finalthetae22562d0 andstate2c6dc8ad;1191livecoords changed and
all5598outside-maskbytes identicalB. Gen10includesnewshape16128absoluteeval;
peak9702MiB/maxgap0.075428s. SSHobservation83690lingeredafteralljobprocesses
exited, but terminalsidecars/processabsence establishcompletion.

Firstjudgepreflightrefusedbeforeanygames becauseanindependentmaskimport wrote
fiveCPython310cachefiles toauditedstage. Source39files remainedbyte-exact;
rootpreservedcaches+failure, restoredexactfilemap andpreparedfresh r1. No engine
result or policy change occurred. Allfuturestageimports requireprojectPython
and bytecodeoff. Freshmanifest4b0ce554/contract235e9fe3/eligibilityb38da1e6
root/SolreviewPASS300inputs/424fixedkeys, committed9a2372e.

r1 judge started08:40:44.787056Z,exec57266/parent30727, pre-runtimePASS,
firstfamilyTOPB2 running with4verifiedworkers. One7200sboundedcampaign,
allsevenfamilies separate, no promotion/upload. Seed310independenttraining
continuesPID1130257 with4gensverified08:41:39Z. Bothtrainedcentresrequiretheir
ownseparatefamilyevidence; topfivegoalstillunmet.

## 184. Seed309 completed judge does not establish improvement; seed310 continues

The fixed final seed309 checkpoint completed all424 games in1188.221s at
09:00:32.943509Z. Outer execution PASS, unchanged runtime and300 prospective
inputs, all16 dynamic hashes exact, lock released. Campaign/root/Sol saved
audits are identical7449dfeb; saved manifestbb5300b8, execution5593a0a7.

Seven separate mean margin changes: TOPB2 -124.7, H30 -395.2, H30B -40.2,
LIVE62 -215.0, LOSS10 -911.5, NEXT30 -109.0, NEXTHIGH -713.5. Most effects
are small relative to uncertainty; NEXTHIGH descriptive t=-2.048. Own money
rises in six groups and opponent money in all seven. Win flips are mixed,
including LIVE62 eight gained/two lost. No pooled score, checkpoint selection,
promotion, upload or seed309 continuation follows. Full result and uncertainty
are in 2026-09-13-seed309-g10-judge.md.

Independent seed310 remains live09:00:34Z, helper1130257/SSH59892, six native
generations complete and9048MiB. Finish the same run and audit its exact final
centre before its own separate judge. Current topfive goal remains unmet.

The recorded-dawn diagnostic changed macros30/30 and complete plans1/30;
unit10/turn7 day14 substitutes wheat for strawberry and tomatoes still first
appear onday15. Root reproduced strengthened source-pinned JSON0642f661.
This is fixed-state behavior, not a candidate-generated game trajectory.
Sol action-threshold note is a prospective unrun measurement; previous integer
and optimizer closures remain intact. User localGPU authorization persists.

## 185. Complete-plan census expresses variation; seed310 at eight generations

The fixed CPU census ran once under900s cap, exit0, 09:13:10–09:18:19Z,
calculation288.888s. It used the first128 antithetic pairs from saved seed309
OFF noise, B centre, sigma.01 and mask1191 on the original12 timing cases.
There are10 unique observations because the three day0 states are identical.
Separate changed-plan counts range82–179/256; distinct plans2–23. Every member
changes a macro, but77–174 per case map back to B's stored plan. No pooled
statistic, game outcome, value estimate or remedy follows.

All12 centre hashes reproduce the old timing benchmark; fresh/reverse checks
and input immutability pass. Root checked all row/pair/histogram arithmetic.
Independent Sol reconstructed pair0 in all12 cases and checked histogram
membership plus rendered-action differences. Every differing spot plan changed
a rendered turn; the audit does not prove future candidate execution or saved
member-index identity. Result6c500cfa, spot audit0568e974, helper70573024 and
manifestec33ba2a are preserved with launch/progress receipts and report.

Source review confirms dawn price awareness and a cached intraday plan. Prior
intraday/revisit/pump-tell experiments already have negative or identical
paired evidence; the current final-money CSVs establish no new stale-plan bug.
Shared-market externalities remain a plausible interpretation, not proved
causation. No third training arm or policy edit was started.

Seed310 remains live09:20:41Z, helper1130257/SSH59892, eight generations,
last611.20s/cumulative5106.6s and9048MiB. Complete the existing run and its
audits before its separate fixed-final-checkpoint judge. Topfive remains unmet.
