# BUILDREVIEW1-B (2026-09-27, structural reviewer B): the build log's logic, its standing laws, its judges, and the holes left for top 5

Read-only review, no games run. Blind to reviewer A.

**Sources read.**
- `docs/strategy/BUILD-STORY.md` lines 1-3,346, in 12 chunks from the first entry.
- `S/gapreview1/A_decisions.tsv`, `S/gapreview1/B_ledger.tsv` (1,133 rows), `S/gapreview1/A_ledger.tsv` (336 rows), `docs/strategy/2026-09-27-gapreview1-B.md`.
- `git log --all` (2,105 commits, 08-21 → 09-27), `git worktree list` (389 worktrees).
- `docs/TRAINING-PROTOCOL.md`, `2026-09-26-selfplay-guide.md`, `2026-09-26-rules1.md`, `2026-09-26-ratingpath2.md`, `2026-09-27-bandleg1.md`, `-latch1.md`, `-melonwin1.md`, `-esband1.md`, `-bandstack1.md`, `-livewatch20.md`.
- `src/kagg3/core/plan.py` switch list (31 ON, 91 OFF module switches; 21 `SWITCH_GENES`), `src/kagg3/spec.py`, the engine `kaggriculture.py` (1,086 lines).
- Every 09-10..09-27 closure doc, through two census sub-agents (`B_flag_early.tsv`, `B_flag_late.tsv`) and one engine-rule sub-agent (`B_engine_rules.tsv`).

**Outputs.**
- `S/buildreview1/B_flagged.tsv`: every closure with its flag codes (§1).
- `S/buildreview1/B_engine_rules.tsv` + `B_engine_notes.txt`: engine rules vs our audits (§4).
- This doc.

**Goal as briefed.** Top 5 = θ ≈ 2,950. Live θ of vrp10_esw is 2,633 (SE 44); PFS adds +36 (SE 17) on the band model [bandleg1 Part C]. The shortfall is +281..+321 θ.

---

## 0. The five findings that matter most (each is expanded below)

1. **The ship gate optimises the family we already beat.** The ship bar in `TRAINING-PROTOCOL §1.7` is dev100, held100 and FRESH300 against reacting V56, plus V-band tapes and faithful-59 (09-22 ENGINE tapes). The BAND leg is not in it. In the band, V is 66-15 and MELON is 7-44 [bandleg1 Part A]. From vrp5 to vrp10 every package read net ≥ 0 on the V56 legs over its predecessor, yet the MELON loss rate at 2,600+ went 91 % → 90 % [livewatch20], and live θ went vrp2 2,818 → vrp5 2,747 → vrp10 2,633 [ratingpath2, livewatch20].
2. **No judge contains an opponent at the rating we need to beat.** The BAND leg's 142 seats have oppR0 2,550-2,849: 80 seats at 2,550-2,649, 54 at 2,650-2,749, 8 at 2,750-2,849 and **0 at ≥ 2,850** (`S/bandleg1/sel.tsv`). Under PFS the MELON cell reads 7-14, 6-17, 1-6 across those three bins (computed from `res/pfv1.csv`). faithful-59 is 09-22 ENGINE subs; all 20 top-20 ids changed since 09-19, 16 of them on 09-26/27 [nbintel6].
3. **Every MELON-family verdict is either open-loop or judged against the wrong family.** The reacting legs are V56, V57, v15stack and a pool that is 60/66 V-series [pool1]. The bank's 6 reacting non-V openers lose every game to us (72-0, median +32k [nonv4, meloncounter2]), so they cannot measure the MELON cell; NONV3 found no reacting zero-melon agent (0/1,280 games); POOL3 found no public kernel for the 4 non-V blow-out opponents. The one law about open-loop bias, "tapes overstate denial", was measured on one V48 clone and one arm (the melon plate) [MELONGENES1].
4. **The "opening/program as a package loses" closures tested executors that could not run the package.** PROGRAM_ENGINE reached 88.0 → 90.7 % of REAL own purse and needed 114 % to break even [progfidelity1, progfix2]. BOEY2 ran 3.0 hires on d3-9 against a floor of 7 and 3.7 cows at d12 against 7.2 [boey2]. OPENPKG1's d0 package cost 3,060 against a 3,000 purse and its crew floor went 3.87 → 2.79 [openpkg1]. MIRROROPEN hands fell 4.5 → 3.2 [BS §8]. The named causes are in our executor: the hire trims (HIRE_ROW, EMPTY_ROUTE_UNHIRE), the funding order in `_derive`, and for PROGRAM_ENGINE an idle PASS rate 3× REAL's at equal hires [progfix2]. None of these verdicts measures the program itself.
5. **The two trainers now train on the only band judge.** ESBAND1 trains on 71-seat halves of the 142 BAND seats and accepts on the full 142 [esband1 §1]. RLFAST run3g1 trains with 110 POOL6-BAND seats, which are 110 of the same 142 [trainfix4]. Any candidate they produce has no held-out band read. The project paid for this twice: flow148 flipped +30/−11 on its own training tapes and transferred to nothing [BS §3], and af3_60 shrank +398 → +149 once its label boards were removed [BS §RLJUDGE].

---

## 1. Chronology of the project's logic

Each phase names the hypothesis that drove it, what closed it, and what the closing evidence shows against what was concluded. Flag codes follow the brief:
(a) one leg only; (b) V-family or clone only, never the band / MELON family; (c) one-sided counterfactual; (d1) pre-VRP code (< 09-24 12:05Z), (d2) post-VRP but pre-PFS (< 09-27 14:14Z); (e) < 50 games in the deciding leg; (f) mechanism or trace argument with no paired run.

| # | dates | driving hypothesis | what shipped | what closed it | evidence shows | concluded | flags on the closure |
|---|---|---|---|---|---|---|---|
| P0 | 08-21 → 09-08 | ES over the full theta in a bit-exact sim finds the policy | B = flow193_g100_hr, 2,715-2,767 | ES-PLATEAU (22 judged checkpoints: true effect −124 ± 47, spread = judge se) [09-16 es-plateau]; shop lottery ±25k/game [09-06] | full-theta ES against clone tapes is noise at σ ≥ 0.001 | "ES closed; move to the action interface" | b, d1. Re-opened later: ESWORK g30 (10-gene block) shipped at FRESH300 +6 [esship1] |
| P1 | 09-09 → 09-14 | levers exist in our own ledger | – | TWO-PURSE rule after one-seat levers lost 2-24k three times [memory counterfactuals-overstate]; pinned-town tapes reproduce live to ≤ 65 coins, 0/96 [tape-fidelity] | one-sided ledgers mislead | judge = pinned held-out tapes, two purses | kept; sound |
| P2 | 09-16 → 09-17 | the gap to the ENGINE class is switches in our plan | LOT4 +791, SLOTPRIO +459, FERT_TIMING +2,845 (FT2), ENDROUTE +25 | ~60 families "closed at mechanism" [BS §5] | ENG22 = 22 tapes × 2 seats; POOLED180 = 169 boards; all open-loop | melon plate, market rows, rival models, town play, route, admission, clip, volume all closed | a, b (open-loop), d1, often e (ENG22 44 games) |
| P3 | 09-17 | evolution never found reactivity | – | REACTIVITY: "every quantity direction gifts in a shared pot, 93 % price"; SELLRACE hour ceiling −308 on 82 tapes; SELLDAY hindsight; BOARDSELECT (d0 obs byte-identical) | a fixed tape cannot re-price or re-time, so any rival gain on a tape is price | "sell hour/order/day closed at ceiling; the plate is a gift" | b, c (fixed rival), d1 |
| P4 | 09-18 | no-quantity arms are gift-free; search can beat the policy | ESR (+477 on 241), WIDE_PICK (+185 BAND250), WIDE_PICK_FREE (+117, user override of its own gift bar) | PLANNER3/4 (idle unreachable), MPCFEAS + ALPHAPROBE3 (68 % of search gain = shop hindsight), LOTDEPTH "law", IDLEWORK "law" | search is a lottery unless the shop schedule is candidate-independent (engine-true) | "search closed; hands hold harvest till dusk; admit only reachable chains" | IDLEWORK rests on a projection (85.7 % die) that DRYDEATH1 falsified on 09-23 (executed fills survive) — f |
| P5 | 09-19 → 09-21 | volume is the gap (VOLUMEHI: the ask is the cap) | head_940 self-play residual (BAND2 +325 t 8.15) = res940 | HERDTILT, TURNCOST, PLANT_FILL_LATE, WHEATLATE1 (gift or own loss); MELONGENES1; 10 PPO/ES/distil continuations NO SHIP; HEADOFF-BAND3 | volume bought on a shared curve returns to the rival on open-loop and on the V48 clone | "volume gifts; tapes overstate denial; gates cannot resolve rating-relevant gains" | b (V48 / open-loop), d1, HIBAND 56 boards (e for sub-cells) |
| P6 | 09-22 → 09-23 | reacting V56 is the right gate; DSM's program is the target | CARE_FILL, OVERFLOW_GUARD V1-V3, LATE_EXEC | PROGRAM_ENGINE 1-4 "closed at every scale"; Q4PROG1 −48; CREW24, RELAYFILL1, CREWRELAY1, WOOLFIRST1, DRIPSELL1 | the ENGINE port runs at 88-90.7 % of REAL; the arms were judged on V56 dev100 (WOOLFIRST1 on faithful-59) | "imitation closed; Q4 replaces Q1-3; idle is structural" | b, d1; the port-fidelity caveat is (f)-class for the imitation verdict |
| P7 | 09-23 → 09-24 | crew routing and oracle labels | ROUTE_VRP (dev +7, held +13, FRESH300 +35, faithful +4) + SALEPIN1 fix | ROUTENN1-3 (KEEP), BESTRESP1-6 (oracle +953..+4k real, labels unlearnable) | the router is the largest post-FT2 gain; distillation of board-specific edits fails | "distillation closed" | b, d1 |
| P8 | 09-24 → 09-26 | with the VRP freeing crew, closed volume arms may now pay | vrp2 → vrp8_jit (6 router increments), EMPTY_ROUTE_UNHIRE, M20z | KNOBV56/KNOBVRP1 (coordinate optimum), Q4 closed 6 more times, HERDVRP1, EGGDOSE1, FEEDKEEP1, COSTAUDIT1, LABOUR1, fills, ENDGAME1, ENDWAVE1, RESWEEP1 (47 arms re-judged on the deep router) | all on V56 dev 50/100 in the exact sim; RESWEEP1 re-judged against V56 only | "rejected-arm backlog CLOSED on the deep router" | b, d2, e (dev50 cells) |
| P9 | 09-26 → 09-27 | the loss is the non-V MELON opener (LIVEWATCH16, LOSSMAP17) | vrp10_esw (ESWORK g30), vrp9_cs, vrp12_pfs (PFS) | NONV1-4, MELONCOUNTER2, OPENPKG1, BOEY1-2, MELONLOGIC1, TOPLOSS1, MELONDENY1, BANDSTACK1, MELONAUDIT1, MELONWIN1 | the MELON cell is 14-37 under PFS; rivals with ≥ 12 plate tiles are 1-23 and cap band θ ≈ 2,778 [melonwin1] | "board (opponent) driven; nothing to probe" | MELONWIN1 is one-sided on a fixed tape (c, f) and misstates an engine rule (§2 L1) |

**Target drift.** The opponent the project optimised against moved five times: ENGINE top-10 tapes (09-16/17) → the V-series band clone (09-17..21) → reacting V56 (09-22..26, still 3 of the 5 ship legs) → non-V melon openers (09-26) → the 2,550+ BAND (09-27). The ship bar was not re-cut at the last two moves.

**Offline-to-live transfer, measured.** Live θ (Elo MLE, n ≥ 20): vrp2 2,818 ± 50, vrp3 2,598 ± 60, vrp5 2,747, vrp10 2,633 ± 44 [ratingpath2 §1, livewatch16, livewatch20]. Each package after vrp2 read net ≥ 0 on its V56 legs over its predecessor (vrp5 went up on a user waiver of held 0). The MELON loss rate at 2,600+ is 91 % for vrp5 and 90 % for vrp10, with the family × band cells matched [livewatch20]. The offline gains landed on V, where we already win 81 % in the band.

**Build metrics (git and docs).**
- 2,105 commits from 08-21 to 09-27; the busiest days are 09-17 (201), 09-12 (177) and 09-18 (153).
- 389 worktrees; 525 branches, 331 merged into master and 194 not merged.
- 835 strategy docs; the gapreview1 ledger has 1,133 arm rows, 653 of them paired.
- Commit subjects: 383 carry NO SHIP / REJECT / KILL / CLOSED and 100 carry SHIP_ / PACKAGED / UPLOAD.
- At least 26 of our submission ids appear in BUILD-STORY (56161192 → 56612145).
- Learned layers: 208 RL/ES ledger rows. Since B (flow193, ES), two trained artefacts shipped: head_940 (09-19) and ESWORK g30 (09-27).

### 1.1 Flagged closures (`S/buildreview1/B_flagged.tsv`)
509 closures: 351 dated 09-03..09-22 (`B_flag_early.tsv`; 64 of them from the ledgers only) and 158 dated 09-23..09-27 (`B_flag_late.tsv` + FLOORHOLD1). Columns: arm, axis, verdict, flags, n_core_flags (excluding d1/d2), date, deciding legs, n games, opponent class, paired, key number, doc.

| flag | rows | share |
|---|---|---|
| b: V-family / clone / open-loop only, never a reacting MELON agent | 409 | 80 % |
| d1: pre-VRP code | 398 | 78 % |
| a: one leg decided it | 331 | 65 % |
| f: mechanism / trace / premise, no paired run | 135 | 27 % |
| e: < 50 games in the deciding leg | 132 | 26 % |
| d2: post-VRP, pre-PFS | 107 | 21 % |
| c: one-sided counterfactual | 81 | 16 % |

- Paired Y 352, N 157. Only 4 rows carry no flag besides d1/d2.
- Only 4 closures ran on PFS code (BANDSTACK1, MELONAUDIT1, MELONWIN1, FLOORHOLD1), and those 4 are the only ones judged on the BAND leg. BANDLEG1's own P10/Tf cells add two band reads.
- Opponents: open-loop tapes 316 (62 %), V-family reacting 159 (31 %), none or self 34 (7 %). **Closures judged against a reacting MELON-family agent that beats us: 0** (the 6 reacting non-V bank agents lose 72-0).

**The named CLOSED axes, by their flags** (rows matching the axis in `B_flagged.tsv`):

| axis | closures | a | b | c | e | f | on BAND | on non-V tapes |
|---|---|---|---|---|---|---|---|---|
| MELON PLATE | 12 | 9 | 7 | 5 | 6 | 1 | 0 (+ BANDLEG1 P10) | 3 |
| Q4 | 14 | 12 | 10 | 4 | 5 | 3 | 0 | 2 |
| HERD | 20 | 13 | 14 | 2 | 3 | 2 | 0 | 1 |
| EGG | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| FEED | 9 | 5 | 6 | 5 | 3 | 3 | 0 | 1 |
| SELL / SALE (timing, lots, day, floor) | 52 | 23 | 45 | 11 | 14 | 12 | 1 | 2 |
| OPENING (package, Boey, wool-first, mirror) | 24 | 15 | 19 | 2 | 4 | 5 | 0 | 1 |
| ENGINE IMITATION | 14 | 8 | 10 | 5 | 3 | 2 | 0 | 2 |
| DISTILLATION / SEARCH | 15 | 12 | 15 | 1 | 6 | 4 | 0 | 0 |
| HEAD PPO / ES | 36 | 28 | 29 | 1 | 3 | 5 | 0 | 1 |
| CREW / LABOUR / HIRE / IDLE | 56 | 45 | 49 | 8 | 19 | 17 | 0 | 1 |
| FILL / VOLUME / RELAY / ASK | 63 | 41 | 54 | 7 | 9 | 9 | 0 | 3 |

**The weakest axis-level closures** (most core flags; all ranked by the two census agents):

| axis | arm | flags | deciding evidence | doc |
|---|---|---|---|---|
| FERTILIZER DENIAL | FERTDENY | a b c d1 e f | engine source + 30-tape census, no paired run | 2026-09-17-fertdeny.md |
| H1 WAIT / ROUTE LAW | H1_START_ON | a b c d1 e f | sim census, 22 ENG22 boards | 2026-09-17-h1wait.md |
| REACTIVE MELON | MELONREACT sell-earlier / no-late-melon | a b c d1 e f | 16-board counterfactual | 2026-09-17-melonreact.md |
| ROLLOUT PLANNER | MPCFEAS | a b c d1 e f | 24 rank-stability rollouts | 2026-09-18-mpcfeas.md |
| MELON SALE SIDE | MELONDUMP hold/withhold | a b c d1 e f | 10-board order trace | 2026-09-19-melondump.md |
| FEED | FEEDFIRE | b c d1 e f | 27-board spot-priced ceiling (+204 ENG22 / +50 V45, closed by the +450 bar) | 2026-09-16-feedfire.md |
| CARE/HARVEST DAY | CARETIMING | b c d1 e f | same 27-board ceiling | 2026-09-16-caretiming.md |
| DAWN / SELL ORDER | turn-0 lot | b c d1 e f | 22-board trace | 2026-09-17-dawnsell-trace.md |
| IDLE-TAIL ADMIT | IDLEWORK | a b d1 e f | 3 boards; premise (85.7 % die) falsified by DRYDEATH1 | BUILD-STORY:815 |
| ROUTER | RLROUTER1 | a b c d2 f | headroom bound, no run | 2026-09-27-rlrouter1-design.md |
| Q4 via non-V blow-outs | POOL3 | a c d2 e f | 4 tape seats | 2026-09-25-pool3.md |
| FEED axis | FEEDNIGHT1 | a c d2 f | trace, −325/g counterfactual | 2026-09-26-feednight1.md |
| HIRE LEVELLING | HIRELEVEL1 | a c d2 f | replay bound 189-226/board | 2026-09-24-hirelevel1.md |
| SELL (cross-day) | SELLAUDIT1 | b c d2 e | causal bound + 20-board replay | 2026-09-26-sellaudit1.md |
| M20z LATCH | LATCH1 | a c d2 e | 7 tape seats; BANDSTACK1 then kept the latch | 2026-09-27-latch1.md |
| MELON PLATE (VRP era) | MELONVRP1 | a b d2 | V56 dev100 only | 2026-09-26-melonvrp1.md |

Axes whose closure was later reopened by new code: ROUTER DEPTH ("closed by clock", RRSPEED1 → ROUTERJIT1 shipped it), ES (ES-PLATEAU on the full theta → ESWORK g30 on a 10-gene block shipped), PLACEFEED (Δours bar → PFS shipped), Q4 "no opponent buys it" (MMPQ → DSMLAND2).

---

## 2. Assumptions ledger: the standing laws and premises

"Re-verified" means re-measured on the current code (VRP router, and PFS where it matters) **and** on a leg that contains the MELON family. "Engine" means I checked the rule in `kaggriculture.py` for this review.

| # | law / premise (as written) | first stated | evidence it rests on | re-verified on current code / leg? | what would falsify it |
|---|---|---|---|---|---|
| L1 | Shop lottery: the day's shop draw is moved by empty tiles, ±25k/game | 09-06; MPCFEAS 09-18 | engine: `_spawn_weeds` draws `rng.random()` for every empty unlocked tile of **both** farms, then `rng.choice(SHOPS)` (kaggriculture.py 836-839, 870-891) | engine-true today. MELONWIN1 (09-27) states the town draw is "independent of both players"; that sentence is wrong, its conclusion does not depend on it | none: engine code |
| L2 | Pinned-town tapes reproduce live to the coin | 09-11 | 0/96 jitter ≤ 65 [tape-fidelity]; band 46/46 + 96/96 byte-exact [bandleg1] | yes, 09-27, band | a tape seat whose replay of our own recorded actions misses the live purse |
| L3 | Two-purse / gift-free rule (Δtheirs t < 2) | 09-16/17 | one-seat levers lost 2-24k ×3 [counterfactuals-overstate]; MELONGIFT 93 % price | it is a bar, not a law: WIDEPICK2 lead ruling [BS 09-18]; PLACEFEED1 rejected on Δours with flips +6/−2 | a gift-positive arm that gains BT wins on a held band leg |
| L4 | "In a shared pot every quantity direction gifts (93 % price)" | REACTIVITY 09-17 | open-loop ENGINE / V45 tapes; later V48 and V56 reacting | partly contradicted: VRP (volume via fewer hires) passed every leg; PFS moves volume with Δtheirs −1,569 (t −4.3) on band | any volume arm with Δtheirs < 0 on a reacting non-V leg |
| L5 | "Tapes overstate denial" | MELONGENES1 09-19 | one opponent (live V48 clone), one arm (melon plate): tape +10,448, reacting = gift; PROGENG3 wool-line artefact; ENGOPENLOOP1 (ENGINE tapes vs V56 36-64) | no; V-family only. BOEY1 found Boey open-loop ("every rule fires with the same count against both pools"), DSMLOGIC1 found DSM reacts to the book, not the rival board | a reacting MELON-family agent (Boey/DSM rule port) vs its own tape on the same boards: Δtheirs gap < 20 % |
| L6 | "The melon plate is a gift" | MELONENG 09-16 | ENG22 −16,224 (open-loop, theirs +15,547); V48 reacting 89 % → 7 % wins; MELONVRP1 V56 87 → 3-12 wins; OPENPKG1 V56 20-0 → 0-20, ml16 −1; P10 on band MELON +1 flip, Δtheirs +8.3k (tape) | on band only open-loop (P10, OPENPKG1 ml16). Never vs a reacting MELON agent that beats us | a plate cell with Δtheirs ≤ 0 vs a reacting non-V opener |
| L7 | "Q4 replaces Q1-3; Q4 closed" | Q4PROG1 09-23 | Q1-3 −236 units, dev100 −48; Q4DIG1 Q1-3 wheat −106 u; 13 arms, all V56 dev50/100 or ENGINE-59 | no band read. V56 buys Q4 on 28/100 boards [dsmland1]; MELONWIN1's 7 wheat-relay rivals are all losses | FOURTHQ1 says FQ nets ≈ +8k from Q4 at our hire bill; a Q4 cell with Q1-3 units flat on the band MELON seats |
| L8 | "Idle is structural" (h0-2 hire/spawn + h21-23) | Q4PROG1 09-23, FILLWORK1 09-24 | 437 PASS = 204 + 196 + 38 midday; daylight idle 0.8-2.5/day | CREWAUDIT1 09-27 on 16 live V games: idle 578 vs 479 = +34/g. Not on MELON games. DSM PASSes 4/game [dsmfull1] | a DSM-style filler dispatcher (PASS → 0) with Δours > 0 |
| L9 | "Hands hold harvest till dusk; the sale is cut once at dawn" | LOTDEPTH 09-18 | 28 gated ENGINE tapes −1,981 t −2.18 (pre-VRP, open-loop) | partially: OVERFLOW_GUARD V1-V3 now walk-and-sell mid-day; DRIPSELL1 (V56) and SLIP1 (engine demo, no paired run) keep the sale side closed. MELONAUDIT1 flags walk 8.9k vs 4.9k/g on band MELON seats | a mid-day DROP+SELL arm with Δours > 0 on the band |
| L10 | "Melon rent is a first-mover allocation, unbuyable" | MELONGIFT 09-17 | shared-stock arithmetic; MELONRACE +396..+1,726 vs −1,777/tile | MELONDENY1 09-27: lever real (−59/u), reach ≤ 20 u by h8, seed row funds N ≤ 3; MELONWIN1: rival sells first 51/51 | a funded early-sell of ≥ 40 melon before h8 on d10 |
| L11 | Engine-gate tells (d2 1-10 melon; d1 zero-melon) separate classes | ENGGATE1 09-22, NONV2 09-26 | V56 0/100, ENGINE 54/73; bank 0/1,600, tapes 7/75, live 2/99 | yes, 09-27 [latch1] | a live V-family game that fires the tell |
| L12 | "Episodes start byte-identical; d0 carries zero seed bits" | MPCFEAS 09-18 | `_new_farm/_new_market` take no rng | engine-true | none |
| L13 | "The town is empty at step 0; one shop per 3 days, uniform over the SHOPS" | TOWNADAPT 09-17 | `_new_town`, `townShopUnlockInterval` 3 | engine-true | none |
| L14 | "BUY_PRODUCT exists only for WHEAT and FERTILIZER; a buy never touches a shop; stock may go negative" | TRADER, FERTDENY 09-17 | 719/719 turns bit-exact | engine-true (598-601) | none |
| L15 | "Seed and animal prices are constants" | DSMSEED1 09-24 | kaggriculture.py 602-605 | engine-true | none |
| L16 | "Hands vanish nightly; only the farmer is alive at turn 0; hire price is Fibonacci per farm per day" | DAWN0 09-18, ENDFIX1 09-23 | `_end_of_day` 876-881, `_do_hire` 700-708 | engine-true | none |
| L17 | "A sold unit adds +1 to the book for good; each shop removes a fixed c every 4 steps" | SLIP1 09-27 | `_commit_unit` 652-661, `_town_consume` 725-747 (single-product shops consume 2) | engine-true | none |
| L18 | "Dry plants die" — two versions: 2 consecutive dry days (IDLEWORK 09-18, `sim/eod.refresh_plants`) vs a planting left dry dies the same night (CREWAUDIT1b 09-27, L222/L783) | 09-18 / 09-27 | sim vs engine reading | engine: both hold. A planting starts at `consecutive_unwatered` = 1 (L222), so one dry night kills it; an established plant dies at 2 (L777-784) | none: engine code |
| L19 | "A planner may only admit work whose whole service chain is reachable (85.7 % of idle-tail plants die)" | IDLEWORK 09-18 | a projection over hypothetical untended plants | **falsified** by DRYDEATH1 09-23: executed PLANT_FILL_LATE plants survive (DRY +0.11/g). `tests/test_idlework.py` still pins the "law" | already falsified; the fill arms stay closed on coin (GAPFIX1, FILLWORK1), not on death |
| L20 | "The scarce thing is the unit-turn, not the tile" | VOLUMEHI 09-19 | pre-VRP crew censuses | VRP freed ~1,000 moves and 29-44 hires/game [routeopt1]; RESWEEP1 re-judged 19 crew-absorption arms on the deep router: −8..0 (V56 only) | a fill arm with Δours > 0 on the band under the deep router |
| L21 | "The rating is decided in the first ~40 games; a re-ship is 30× faster than climbing" | RATINGPATH 09-17 | dW(n) = 1270·n^−1.28, floor ±4.5 | **superseded**: Elo K floor 8.9 from game 70 [ratingpath2]; final = one Bradley-Terry fit over the Oct 1-15 episodes [rules1] | – |
| L22 | "Top-5 needs a 7 % loss rate against the 2,300-2,700 band" | RATINGPATH2 09-26 | Elo extrapolation from 99 games at mean 2,501 | no: it assumes our loss rate vs 2,900+ follows the Elo curve fitted on a V-dominated band. At 2,750+ PFS is MELON 1-6 [bandleg1 res] and 2,600+ opponents are 78 % MELON [livewatch20] | a measured win rate vs ≥ 2,850 opponents (no leg has one) |
| L23 | "The top 10 is one class, the fertilizer ENGINE" | TOPLEG 09-16 | 30 tapes, 0 V clones | drifted: TOPLOSS1 09-27, 59/60 top-10 winners and 60/60 losers play the 8m/12w plate | – |
| L24 | "No opponent buys Q4" | MMPQ 09-16 | tapes of 09-16 | **falsified** DSMLAND2 09-23 (DSM 126/126) | – |
| L25 | "Seat effect = board composition" | SEATFLIP1 09-26 | 200 same boards, gap +2 t 0.04 | V56 only | a band seat-flip run |
| L26 | "Yield per plant and per production night = the ENGINE seats" | YIELD1 09-26 | faithful-59 hooks, within 5 % | faithful-59 (ENGINE 09-22) | – |
| L27 | "Our sale turns already land on the day's highest quote" | CHURNPRICE1 09-26 | 32 live replays, 95-99.7 % | live, mixed families | – |
| L28 | "Judge base = the live package; training on master only" | ESJUDGE1 09-26, TRAINING-PROTOCOL 09-27 | STACKESW1 stale-base loss | yes | – |
| L29 | "The MELON cell is board-driven; nothing to probe" | MELONWIN1 09-27 | 51 fixed-tape seats; our side equal in W and L | one-sided (the rival cannot respond on a tape) | a reacting MELON agent whose output changes with our play |

**Count.** Of the 29, 10 are engine-true or verified on their measured sets (L1, L2, L11, L12-L18), 3 are falsified or superseded (L19, L21, L24), 2 have drifted with the field (L22, L23), 11 rest on V-family or open-loop evidence only (L3-L10, L20, L25, L29), and 3 were verified on non-band legs (L26-L28).

---

## 3. Judge holes: what the current gates cannot see

The current gates are the ship bar (`TRAINING-PROTOCOL §1.7`: dev100 ≥ +1, held100 ≥ +1, FRESH300 ≥ +3, tapes ≥ 0, faithful ≥ 0, Δtheirs t < 2) and the BAND leg (BANDLEG1, 142 open-loop seats, orig seat only).

| # | hole | evidence | risk to a top-5 candidate |
|---|---|---|---|
| J1 | **No seat at the rating that decides top 5.** | BAND max oppR0 2,849; 0 of 142 seats ≥ 2,850; MELON by bin under PFS: 7-14 (2,550-2,649), 6-17 (2,650-2,749), 1-6 (2,750-2,849). faithful-59 = 09-22 subs; 16 of today's top-20 uploaded 09-26/27 [nbintel6] | A candidate's rank-5 value is an extrapolation. The 1-6 cell at 2,750+ says the curve is falling. |
| J2 | **The ship bar has no MELON leg except faithful-59.** | 3 of 5 legs are reacting V56; tapes = V band (dev50); BAND leg not in the bar | Ships improve the V cell (already 81 % in band). vrp5 → vrp10: MELON 2,600+ 91 % → 90 % L [livewatch20]. Transfer: of the 4 arms that were net-positive on V legs and were re-read on the band on the same base, 3 read ≤ 0 there (SLIVER −2, CARE_RIDE −1, WHEAT_CYCLE WC −1; PFS +8) [bandstack1, shipsliver1, shipcare1, wheatcycle1]. |
| J3 | **Reacting legs that beat us are V only; MELON legs are open-loop only.** | pool 60/66 V openers [pool1]; the 6 reacting non-V bank openers lose 72-0 [nonv4]; NONV3 0/1,280 zero-melon fires; POOL3 no kernel for Cow Boy / WarRusher / flg / kuroko1t | Denial-type arms (PFS: Δtheirs −1,569) cannot be checked for a rival response. MELONGENES1 says the sign can flip (+10,448 tape → gift). |
| J4 | **Low power at the effect sizes that remain.** | Binomial on discordant pairs: a null arm passes dev ∧ held ∧ FRESH with p ≈ 0.03; a true +2 flips/100 (≈ +13 θ) passes with p ≈ 0.31-0.36, ≈ 0.2 with tapes and faithful. HEADOFF-BAND3: +230 θ ≈ 4 flips / 240 rows. PFS on band: 10-2, two-sided sign p 0.039; direct Δθ on vrp10's own 46 seats 0 (SE 11) | Between 2 and 4 in 5 true +13 θ arms are rejected, and closures at net −1..+2 do not show a zero effect. |
| J5 | **In-sample band for the two trainers.** | ESBAND1 trains on 71-seat halves of the 142 and accepts on the 142 [esband1 §1]; run3g1 trains on 110 of the 142 [trainfix4] | An ESBAND1/run3g1 candidate cannot be judged on the BAND leg. Precedents: flow148 +30/−11 in-sample → 0 transfer; af3_60 +398 → +149 out of sample. |
| J6 | **Sim-harness omissions found late.** | M20z latch absent from the jitted ES sim and from eswork/NEARMISS1 sims until 09-27 [esband1, melonlogic1]; overflow guards absent from the sim until SIMGAP1 09-24 (ESENG1 sim 58-42 vs engine 67-33); lazy-import crash scored LATE_ASK_FLOOR / END_WAVE arms at 3,000 [vloss1, endwave1]; 3 bank tape agents lacked actions.json → free wins [pool2] | Every sim-leg closure dated before its fix carries a harness caveat. ZERO-seat reads in ES before 09-27 15:18Z are wrong by construction. |
| J7 | **Base rows reused or mismatched.** | WINJUDGE (ENGINE28 base ran CLIP_CAP_ON: +269 → +178); RLJUDGE (base before WIDE_PICK_FREE: +398 → +281); VRPFALLBACK1 (`v2dev100.tsv` had RESIDUAL_RIVAL_PURSE_ON=True); STACKESW1 (g15 beat vrp7, lost to vrp8_jit) | 4 documented incidents, all biased upward. Reuse is now checked by reproduction (SHIPSLIVER1, STACKJIT1), which is the right control. |
| J8 | **The town draw is pinned on every tape leg.** | live draw depends on both farms' empty tiles (L1) | Unbiased per arm, but live variance of tile-changing arms is larger than any tape leg shows; a 46-game live read cannot confirm a +36 θ effect (vrp10 direct 0 ± 11). |
| J9 | **Latch seats.** | ZERO = 7 band seats; LATCH1: 7 firing seats, flips +1, Δmargin −5,258, live 2/99 | M20z stays on 8 open-loop tapes of evidence; ≤ 0.3 wins/100 either way. |
| J10 | **FRESH vs the live band mix.** | FRESH300 = fresh boards vs V56; live band = MELON 57 % / V 35 % / ZERO 9 % [bandleg1] | FRESH300 is the largest leg and carries the most weight in the bar; it is V-only. |
| J11 | **The Δours > 0 bar vs a wins-only final.** | PLACEFEED1 +6/−2, Δours −53 (t −0.28) → NO SHIP; after the pump fix it became PFS, the only band pass. CARE_FED_ON dev +3 (Δtheirs t −6.8), NONV_WOOL_CARE bed +3 / dev +2 (Δours −256 / −93) | The final is a BT fit on wins. A coin bar rejects denial arms that win games. |
| J12 | **Seat coverage of the band leg.** | BANDLEG1 ran the orig seat only (142 games, not 284) | Seat effect is 0 on V56 [seatflip1]; unmeasured on MELON seats. |
| J13 | **Opponent versions go stale within days.** | LIVELOSS13: 18/37 live losses were V versions not in the bank; LIVEWATCH19/20: 28 loss subs unbanked | The October field (final uploads 09-28..30) is not in any leg. |

---

## 4. Engine-rule audit: hits and misses

Full table: `S/buildreview1/B_engine_rules.tsv`, 69 rules (unit 7, op 4, crop 9, animal 9, shed 7, market 20, land 2, turn/time/end 5, rng 2, other 4), each with engine line, spec line, status, evidence doc and, where needed, a census design. Notes: `B_engine_notes.txt`.

**Spec vs engine.** Engine sha256 `bc8a54879ef0…` equals the spec.py header claim. No constant differs across the crop, animal, market, shop, land, hire and config tables. One wrong comment with a live consequence: spec.py:58-66 says a crop watered on every window day "already holds CROP_MAX_YIELD". Unfertilised, the engine caps wheat at 4/6 and carrot at 3/4 (py:440-443). The hire gate at `agent/runtime.py:295` prices a planting at `price × CROP_MAX_YIELD`, so it overvalues unfertilised wheat by 50 % and carrot by 33 %. Absent from spec (not wrong): actTimeout 1 s, decay every 2 steps, the weed/shop rng formula, the last processed step 718 (d29 h22; d29 h23 and the d29 night never run).

**Status counts.** AUDITED 50, EXPLOITED 12, FIXED 3, MODELLED_ONLY 4, UNAUDITED 0. 15 of the AUDITED rules rest on audits dated before 09-24, i.e. before the VRP router and PFS, and none of them on MELON band seats.

### 4.1 Rules a ship exploited or a bug fix restored
| rule | engine | ship / fix | doc |
|---|---|---|---|
| Last processed step 718; reward = money only, unsold stock = 0 | py:958-963 | ENDROUTE / ENDROUTE2 / SPLIT / ROW2 (ESR); pay_day cut-off | dropharv, endfamily, feedfire |
| Hour structure (day = step//24) | py:906-911 | LOT4 turn 17, hour-scheduled rows, LATE_EXEC | lot4sweep, endfix1 |
| DIG enables same-day dig + replant | py:484-491 | LATE_EXEC_ON | endfix1 |
| DROP destroys units beyond shed room; night drop capped at 100 | py:343-356, 843-857 | OVERFLOW_GUARD V1-V3 (FIXED) | overflow2-4 |
| Placement night: a new animal is unfed/uncared, banks no care | py:236-240, 813-830 | PLACEFEED_ON + PF_PUMPSAFE_ON (FIXED, vrp12_pfs) | crewaudit1, placefeed1-3 |
| FEED once/day; 2 unfed nights → escape; survival = a feed every other day | py:505-513, 813-820 | FEED_MANDATORY_ON, SURVIVAL_WATER_ON | feednight1, milktrace1 |
| Production pays base 1 unconditionally, care bonus only if fed that night | py:821-828 | CARE_FILL_ON, CARE_RIDE (vrp9_cs) | care-coverage, careaudit1 |
| Ongoing crops produce on survival, not same-day water | py:786-802 | alternating waters in the planner | wateraudit, yield1 |
| Moves 1 tile/turn, no collisions | py:88-93, 323-332 | ROUTE_VRP (+ JIT, deep RR) | routeopt1, routeraudit1 |
| SELL draws on the shed; DROP + SELL in one step works | py:596-597, 653-657 | ENDROUTE, BANK_BEFORE_LOT | dropharv, noopaudit |
| BUY_PRODUCT (wheat/fert) at price(inv−1), lands in the shed | py:598-601, 662-672 | OPEN_PUMP_ON | pumpoff3, placefeed3 |
| Fertiliser doubles in-window gains; timing matters | py:440-444, 798-799 | FERT_TIMING_ON (FT2, +2,845) | fertengine |
| Hire: Fibonacci per farm per day, hands vanish nightly, spawn argmin on access tiles | py:533-541, 700-708, 876-881 | HIRE_ROW, WIDE_PICK, EMPTY_ROUTE_UNHIRE | dawn0, widespawn, labour1 |

### 4.2 Rules never checked against our replays on the current code (top 10 by likely coins vs MELON rivals)
Each census runs over the 142 BAND seats (`S/bandleg1`, PFS master), ours vs the rival, split by family. No games beyond the replays.

| # | rule (engine line) | status | one-line census | lever threshold |
|---|---|---|---|---|
| 1 | A09 every live animal offers 1 fertiliser per night; an uncollected night is lost; fertiliser has no town drain (py:515-522, 831; 50, 114) | audited 09-11/09-23 (388/g), never on band | COLLECTs / available animal-nights d0-19, ours vs MELON rival | ≥ 10 fert/g missed (~500 coins/g) |
| 2 | T06 invalid unit actions are silent no-ops (py:313-319, 414) | NOOPAUDIT 09-23, pre-VRP | re-run the `S/noopaudit` hook: no-op unit-turns per class per game | any class ≥ 150 coins/g |
| 3 | U06 units resolve in order inside a step, so two units can harvest and replant a tile in one turn (py:935-939) | MODELLED_ONLY | same-step same-tile HARVEST/DIG → PLANT and DROP → PICKUP pairs per game | rival ≥ 5/g more |
| 4 | C02 unfertilised in-window watering caps wheat at 4/6, carrot at 3/4 (py:440-443) | WATERAUDIT 09-23, pre-VRP | in-window unwatered plant-days per crop (units lost) | ≥ 5 u/g |
| 5 | T07 + U03 ≤ 10 market rows per turn, shared with HIRE rows; a hired hand acts from the next step (py:551, 560, 571-578) | audited pre-VRP | d10-19 turns where HIRE+SELL+BUY hit 10 and hires spill; hand-turns lost × 30 coins | ≥ 150 coins/g |
| 6 | M16 shops drain every 4 steps after the market (2 u for YARN/PET_CAFE) (py:728-743) | TOWNADAPT 09-17 | drain units captured between our rows vs the rival's, per product, MELON losses | ≥ 200 coins/g |
| 7 | M03 carrot: PET_CAFE drains 12/day; fastest crop (py:43, 741) | CARROTFLAT 09-18, pre-VRP | carrot units and price d10-19 by PET_CAFE present/absent, MELON losses | ≥ 300 coins/g |
| 8 | S05 shed ops work from all 4 access tiles even while LOCKED (py:132-139, 339-342) | MODELLED_ONLY, no doc | share of shed trips not ending on the nearest access tile; walk turns saved | ≥ 20 turns/g |
| 9 | C04 a planting starts at 1 dry day, so one dry night kills it (py:222, 777-785) | DRYDEATH1 09-23, pre-VRP | DRY deaths and planting-day misses per game | ≥ 0.5 plantings/g |
| 10 | S03 PLACE-to-shed keeps what does not fit; DROP destroys it (py:393-410 vs 343-356) | MODELLED_ONLY | DROP events with inventory > room that a PLACE n would have kept | ≥ 5 u/g |

Lower priority (in the TSV): T02 step order vs the shop tick, U01 farmer h0-h2 turns, U04/U07 night carry, O02 atomic PLANT veto, S04 PICKUP batching, L02 HIRE/BUY_LAND row order, R01 shop draw vs band W/L.

**What the audit adds to the MELON question.** Nothing in the engine lets us buy back the melon book: no shop demands melon, the town centre drains 1 u/day (py:745-747), and the curve floors at +158 u, so the first seller wins it (MELONWIN1: rival first in 51/51). Against MELON rivals the coins have to come from crew turns and the other d10-19 books. That points the census effort at #1, #3 and #5.

---

## 5. Decision-space and opponent-space holes

### 5.1 The rating arithmetic by family (new measurement)
Elo MLE over the 142 BAND seats with each seat's oppR0 (`S/bandleg1/res/*.csv`, `boards_all.json`):

| arm | all seats | vs V (81 seats) | vs MELON (51 seats) |
|---|---|---|---|
| master (vrp10_esw) | θ 2,703 (83/142) | **2,904** (67/81) | **2,394** (9/51) |
| PFS (vrp12_pfs) | θ 2,745 (91/142) | **2,954** (70/81) | **2,495** (14/51) |

The overall θ is set by the share of MELON opponents at our rating. Under PFS, with the per-family win rates held fixed at mean oppR 2,642: MELON share 0.57 (vrp10's live band mix) → θ 2,656; 0.78 (vrp10's 2,600+ mix [livewatch20]) → 2,572; 0.95 (the top-10, where 59/60 winners play the plate [toploss1]) → 2,497.

**Reading.** Against V we already play at the top-5 level (2,954). Against MELON we play at 2,495. Top 5 at a MELON-dominated 2,950 needs MELON strength ≈ 2,950: a win rate vs the band's 2,668-mean MELON seats of ≈ 84 %, against 27 % today. That is +455 θ on one cell. No switch has moved that cell by more than ±1 of 51 seats [bandstack1].

### 5.2 Decisions never judged on the BAND leg
Of the 34 decisions in `S/gapreview1/A_decisions.tsv`, 7 have a BAND-leg read: D4 (SLIVER, in vrp9_cs and BANDSTACK1), D6 (P10 plate), D8/D9 (WHEAT_CYCLE WC), D15 (PFS), D17 (CARE_RIDE), D24 (FLOORHOLD1 sale floor), D29 (Tf counter, M20z latch). The other 27 were closed on V56, V-band tapes, ENGINE-59 or earlier legs. The ones the MELON loss evidence points at:

| decision | why it points at the MELON cell | where it was closed |
|---|---|---|
| D20 early crew d0-9 | MELON rivals run 7 hands d0-9 vs our 3 [lossmap17]; every floor we built was trimmed back (NONV1 3.72 → 3.78; BOEY2 3.0 vs 7; OPENPKG1 3.87 → 2.79) | EARLYRAMP (09-17, open-loop ENGINE, pre-VRP); never executed under VRP |
| D12 herd size/species d0-9 | MELON rivals: animals 7.3k vs 4.5k, 3 sheep d0, WOOL −8.4k of the margin [lossmap17, melonlogic1] | HERDVRP1, WOOLFIRST1, NONV4 (tapes +4, reacting 72-0 inert) — V56 or open-loop |
| D1 Q2/Q3 day | MELON rivals own Q2+Q3 by d9 [lossmap17] | WHEATMIX1 Q3_EARLY −9, BOEY Q2 d6 −36 — V56 only |
| D2 Q4 + wheat relay | 7 wheat-relay rivals are all losses; rival d10-19 wheat = +9.2k of the W/L gap [melonwin1]; Q4 denial ceiling +5.0k [dsmland2] | 13 arms, all V56 dev or ENGINE-59 |
| D3 tomato count | top-10 mirror edge TOMATO +6.8k/game [toploss1]; tomato 4.9 vs 18.8 plantings d0-19 [farmaudit1] | TOMATOFILL1 (V56, fill-only), TOMATO15 (09-16) |
| D23-D25 sale lots on MELON seats | walk 8.9k vs 4.9k/g, 70 vs 45 floor units [melonaudit1] | SLIP1 (engine demo, no paired run), DRIPSELL1 (V56). FLOORHOLD1 (09-27 17:44Z, band 142) closed the floor-hold version: f 0.1/0.2/0.3 net −4/−7/−7, f3 Δtheirs +295 t 3.37 (`S/floorhold1/pair.txt`) |

### 5.3 Opponent classes with fewer than 5 seats in the BAND leg
Counts from `S/bandleg1/sel.tsv` and `boards_all.json`, with MELONWIN1's strata:
- **Any family at oppR0 ≥ 2,850: 0 seats.** The top-5 bar is 2,948-2,954.
- V at ≥ 2,750: 1 seat. ZERO at ≥ 2,650: 3 seats. OTHER: 3 seats.
- MELON at ≥ 2,750: 7 seats (PFS 1-6).
- MELON rival with ≤ 8 plate tiles: 5 seats (5-0). The 36-tile mirror: 1 seat.
- The named top programs (DSM, Boey, Fourth Quadrant, mtmr, the 09-26/27 top-20 uploads): 0 seats. Their only legs are DSMFULL1's 131 seat-swap boards (09-23, old DSM sub) and faithful-59 (09-22).
- Distinct opponents: 106 in 142 seats.

### 5.4 The Oct 1-15 final: what no arm has modelled
From RULES1: one Bradley-Terry fit over the Oct 1-15 episodes of each team's latest 2 subs; the team shows its best bot; newer bots play more episodes; whether pre-deadline games count is unanswered.
1. **The pairing mix sets our BT θ.** Our strength is non-transitive (V 2,954 / MELON 2,495 under PFS, §5.1). Pairings follow live Elo, and the MELON share rises with rating (57 % of vrp10's band games, 78 % at 2,600+). No arm has modelled what mix our subs will draw in October, or whether a fresh 09-30 upload (which climbs from µ 600 through V-heavy bands and plays "much more frequent" episodes) changes our BT θ relative to a 09-27 sub.
2. **The two final slots are one bet.** vrp10_esw and vrp12_pfs differ by two switches; PFS dominates on the band (+36 family θ, direct 0). The team score is the better of the two, so the older slot carries near-zero option value. No arm has priced a decorrelated second slot.
3. **The October field is unseen.** 16 of the top-20 re-uploaded on 09-26/27 [nbintel6]; final uploads land 09-28..30. LIVELOSS13 found 18/37 live losses from V versions not in the bank. No leg will contain the final field before the deadline.
4. **Games between our own two subs** enter the BT fit. Their effect on the team's best-bot θ is unmodelled (expected small).
5. **Whether pre-deadline history counts** changes nothing for a sub uploaded after 09-27 but decides whether vrp10_esw's 84-game record (56-28) enters the fit.

---

## 6. Verdict: the top 8 holes by expected rating

**Scale first.** One net flip on the 142-seat BAND leg ≈ +4.5 θ at vrp10's family mix (PFS: +8 flips → +36 θ [bandleg1]). Top 5 needs +281..+321 θ. The measured gap sits in one cell: MELON strength 2,495 against a needed ≈ 2,950 (§5.1). E[Δθ] below = P(the probe yields a shippable arm by 09-30 23:59Z) × Δθ if it does, or, for instrument holes, the regression it prevents. The sum over all 8 is +11..+37 θ. **No hole in this list closes the top-5 gap; only #2 has a stake of that size, and its probability is low.**

| # | hole | evidence | probe | cost | E[Δθ] |
|---|---|---|---|---|---|
| 1 | **Trainers train on the only band judge (J5).** Any ESBAND1 / run3g1 candidate read on BANDLEG is in-sample. | ESBAND1 accepts on the same 142 seats it trains on [esband1 §1]; run3g1's 110 band rivals ⊂ the 142 [trainfix4]; precedents flow148 (+30/−11 → 0), af3_60 (+398 → +149), ESJUDGE10 | Build **BAND-HOLD**: ≥ 100 new ≥ 2,550 seats from vrp12_pfs + vrp10_esw live games after 09-27 13:00Z (`S/bandleg1/select.py` + `build_leg.py`, same fidelity checks). Freeze it. Any trainer candidate must pass BAND-HOLD net ≥ +2 and Δtheirs t < 2 before packaging. | 1.5 agent-h; ~100 tape builds + 100-200 base games | +6..+9 (regression prevented) |
| 2 | **The MELON program was never run at fidelity, and never against a reacting MELON agent that beats us.** | MELON strength 2,495 (§5.1); rivals with ≥ 12 plate tiles 1-23 [melonwin1]; rivals run 7 hands d0-9, Q2+Q3 by d9, animals 7.3k vs 4.5k, 102 vs 56 plantings d10-19 [lossmap17]; every port ran with our trims active (§0 item 4) | **Falsifier before any build:** on the 51 band MELON seats, run the existing OFF switches that make up the opening (MIRROR_OPEN_ON, NONV_EARLY_HANDS, BOEY_PKG_ON cells; they live on branch boeypkg1, worktree `kagg3_wt_boeypkg1` d0deb070, a pre-PFS base, so port them onto master 942b46cb first; WOOL_FIRST_ON and MELON_PLATE_TILES are already on master) with HIRE_ROW trim and EMPTY_ROUTE_UNHIRE disabled on d0-9, and measure executed fidelity (hands d0-9, animals d9, Q2/Q3 day, plantings d10-19) against the rival's. Stop if fidelity < 90 %. If ≥ 90 % and MELON net ≥ +3 with dev20 V56 ≥ 0, judge on BAND-HOLD. | 2.5 agent-h; ~300 games | +2..+6 (stake: MELON cell +455) |
| 3 | **No leg at ≥ 2,850 (J1).** | 0 of 142 BAND seats ≥ 2,850; 16 of the top-20 re-uploaded 09-26/27 | **TOPLEG-27:** seat-swap (DSMFULL1 method) our package into ≥ 100 recent games between top-30 teams, fetched with ListEpisodes of their current subs (S/toploss1 lists 341 top-10 losses, 60 censused); exact seed + pinned town; keep seats whose tape holds (ENGCONTRAST1 FAITHFUL filter). Report PFS vs vrp10_esw and #2's cell there. | 2 agent-h; ~300 games | +2..+5 (picks the final pair on the right population) |
| 4 | **The October BT pairing mix is unmodelled (§5.4 item 1).** | non-transitive strength V 2,954 / MELON 2,495; MELON share 57 % → 78 % → ~95 % with rating | Simulate the Oct 1-15 BT fit: per-family win rates from BANDLEG (PFS), family × rating mix from LIVEWATCH20, pairing = live Elo ± 52 [ratingpath2 §1], 1,300-2,000 games per sub; compare "keep the 09-27 subs" vs "fresh upload on 09-30". | 1 agent-h; 0 games | 0..+5 (decides upload timing) |
| 5 | **The second final slot carries no option value (§5.4 item 2).** | vrp10_esw vs vrp12_pfs: 2 switches apart; PFS +36 family θ, direct 0 | After #2-#4, put the best non-dominated candidate in the older slot (the one with the highest P(beats PFS on TOPLEG-27 / BAND-HOLD)); if none exists, re-upload PFS so both slots are PFS-class. The last 2 uploads before 09-30 23:59Z are the final pair [rules1]. | 0.5 agent-h; 0 games | 0..+5 |
| 6 | **The coin bar rejected flip-positive denial arms (J11).** | PLACEFEED1 +6/−2 rejected on Δours −53, then passed as PFS; CARE_FED_ON dev +3 (Δtheirs t −6.8); NONV_WOOL_CARE bed +3 / dev +2; MELONVETO_POST BAND2 +9/−6 but LIVE250 +4/−7 [BS 09-21] | Re-judge CARE_FED_ON, NONV_WOOL_CARE and MELONVETO_POST on PFS over BANDLEG + BAND-HOLD with a wins-first bar (net ≥ +2, Δtheirs t < 2, no Δours condition). | 1 agent-h; ~750 games | +1..+3 |
| 7 | **Q4 / wheat relay was never judged against wheat-relay MELON rivals.** | 7 wheat-relay rivals, all losses; rival d10-19 wheat +9.2k of the W/L gap [melonwin1]; 13 Q4 arms, all V56 or ENGINE-59 | Q4DIG1 cell (i) (own Q4 + `Q4_HERD_FIRST`, on branch boeypkg1, port to master) and the ESWORK Q4-band genes (within genes 6-9, whose code path is unshipped on master [srcsync1]) on the 51 MELON seats + dev20 V56 guard. | 1.5 agent-h; ~150 games | 0..+2 |
| 8 | **Engine rules never censused on MELON seats under the current code (§4.2).** | fertiliser COLLECT 1/animal-night with no drain (A09), two-unit same-step harvest+replant (U06), 10-row cap shared with HIRE (T07+U03); the last audits are 09-11..09-23, pre-VRP; spec.py:58-66 comment wrong and `agent/runtime.py:295` hire gate overvalues unfertilised wheat/carrot by 50 %/33 % | One replay census over the 142 BAND seats for §4.2 #1, #3 and #5 (engine hooks as in `S/crewaudit1`), ours vs the MELON rival; build an arm only where a threshold in §4.2 is crossed. Separately: price the runtime.py:295 gate with the fertilised/unfertilised cap. | 1 agent-h; 0 games (census) | 0..+2 |

**What the ranking says.** Holes 1, 3, 4 and 5 are instrument and decision holes: they do not raise strength, they stop the last three days from shipping a wrong or in-sample package. Hole 2 is the only one aimed at the cell that holds the gap. Its falsifier is cheap and tells us within one agent-session whether our executor can run the MELON program at all. If it cannot, top 5 is out of reach by 09-30, and the remaining effort belongs in #1, #3, #4 and #5.

**Not in the list, and why.** FLOORHOLD1 (sale floor for wool/milk/straw) ran on the band at 17:44Z: −4..−7 flips, NO SHIP. Structure siting was closed by SITING1 (ours 1.74 vs 1.99, near-shed switch = ROUTE_EFF −111). M20z keep/remove is ≤ 0.3 wins/100 [latch1]. Seat effects are 0 on V56 [seatflip1].
