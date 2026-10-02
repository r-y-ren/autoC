# 2026-09-14 — MACRO_EXEC: can our planner execute a top-five macro plan?

**VERDICT: the ramp is EXECUTABLE, the calendar is NOT, and the executed plan
loses.** Under `plan.MACRO_EXEC_ON` (default False) our seat reproduces
ymg_aq's day-0 board **exactly** — 4 hands, herd 0/2/3, tiles 12 wheat / 2
melon — and delivers **277 of 277** season hires (100 %, against B's 261),
which is the first time any build of ours has stood up a top-five opening.
Tiles are only **43 %** delivered and animals **60 %**, and the coin gate
**fails**: pooled we end on **55,306 against ymg_aq's 138,009 = 0.40 of their
coins**, where B on the same 12 boards ends on **93,127 = 0.87**. Target was
within 20 %. The binding failure is not the ramp but the *calendar*: a fixed
per-day planting schedule desynchronises from our own harvest cadence and the
farm idles — **44.0 idle tiles at dawn d10 against B's 1.1**. `sell_hour` is
**NOT BUILT** (extracted into the JSON, not consumed).

Sim, descriptive, paired, CRN, action-replay opponent seat, theta B =
`flow193_g100_hr`, shipped `hr` switches. No engine game, no training arm.

## 1. What was built

`MACRO_EXEC_ON` (`src/kagg3/core/plan.py:4678`) is a module-level boolean
applied with `setattr` exactly like `OPEN_PUMP_ON` / `TAIL_FILL_ON` /
`BANK_BEFORE_LOT_ON` / `HIRE_ROW_ON` (there is no env-var switch mechanism in
this codebase; the harnesses set the globals before importing `sim`). The
schedule itself is a JSON file named by `KAGG3_MACRO_JSON` and decoded once,
host-side, by `plan.macro_load` (`:4692`) into module constants
`hands[30] anim[30,3] tiles[30,5] land[30]`; `MACRO_SCHEDULE` is `None` until
it is called. **Both** must be set for any new code to run.

Six sites, each `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:`:

| # | site | line | what it does |
|---|---|---:|---|
| 1 | `_plan_and_stats` mix rewrites | 5521 | `_macro_targets` writes `plant_target` and `animal_want` from the schedule, **after** every other mix rewrite, so the schedule is the last word and `plant_total = n_dev - sum(animal_want)` (`brain.py:992`, the herd-screen §3 coupling) cannot reach the schedule's tiles |
| 2 | `_derive` land gate | 5440 | `buy_land` follows `land_target[day]`; the two hard laws (a quadrant exists, the purse covers the gap) still bind |
| 3 | `_derive` candidate values | 6094 (in `_derive`, after `_candidates`) | the three animal lists are floored to `BUD.VALUE_CAP` so the ONE `budget.grant` walk serves the herd ahead of the seed lists — the displacement `2026-09-14-melon-animal-mechanism.md` §3 traced (12 melon seeds at 80 outranking a 500-coin SHEEP). A floor, not a multiplier: on a board whose tasks have not appeared the animal's own price is often 0 |
| 4 | `_wants` animal want | 4870 | `acquire_ok` (`ub_coins > ANIMAL_COST`) is skipped — the last *value* gate on the herd, and it prices the animal off today's board |
| 5 | hire argmax | 6289 | `h_star` = `min(hands_target[day], largest affordable h)`; `afford` is the enumeration's own test and `HIRE_BILLS` is non-decreasing, so counting affordable h under the ask IS the clip |
| 6 | `HIRE_ROW_ON` trim | 6702 | excluded under a schedule. This trim (`n_hire_row = min(n_hire, n_act)`) is the last task-set gate on the crew; with it on, the day-0 ask of 4 hands was delivered as **2** |

Sites 3-6 were not in the original design and are the build's main finding:
*four separate today-only value gates* stand between a macro ask and the
board, and the ramp does not execute until all four are lifted.

Tools: `S/macro_exec/extract.py` (tape -> JSON), `run.py` (CRN ledger, a copy
of `S/topledger3/ledger.py` re-pointed at the repo `src`, with `--src`,
`--macro`, and a HIRE counter — `st.nhands` is 0 at every dawn), `report.py`.
Schedules `S/macro_exec/macro_ymg_aq.json` (+6 per-episode); raw
`raw_{headOFF,repoOFF,macroON,melOFF,melON}.npz`. Tests
`tests/test_macro_exec.py` (9, all pass).

## 2. Identity with the switch OFF

`S/macro_exec/run.py` run twice over the 12 ymg_aq boards — once against a
pristine `git archive HEAD src` tree, once against the working tree with the
switch OFF — and compared over every recorded array:

| array | max abs delta |
|---|---:|
| money, tiles, anim, nhands, hire_n, nquad, idle, fert | **0** |
| shed, sold_np, sold_rp, buy_np, buy_cp, mkt_inv, price | **0** |

**max |delta| = 0 over all 15 arrays x 31 snapshots x 2 seats x 12 boards;
paired margin delta 0 coins.** `tests/test_macro_exec.py` adds the stronger
unit form: with a schedule **loaded** and the switch OFF, the whole plan tuple
is unchanged on four boards (opening purse, rich day, late day, second
quadrant). `tests/test_melon_gene.py` passes.
`tests/test_backend_agreement.py` fails on `legacy` with 2 of 2400 decisions
disagreeing on `hire_bias` — **pre-existing**: the identical failure
reproduces on the HEAD tree (`brain.py` is not touched by this build).

## 3. The macro, from ymg_aq's own tapes

`extract.py` counts the market rows and unit ops of
`artifacts/tape_actions_town/<ep>.npz` for the 6 retention>=0.95 ymg_aq
episodes. Days 0-5 are **identical across all six** (the open-loop clone of
`kaggle-clone-family`); the spread starts at d6. The pooled (per-day median)
schedule:

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hands | 4 | 1 | 4 | 4 | 4 | 4 | 9 | 5 | 8 | 9 | 11 | 9 |
| animals G/C/S | 0/2/3 | . | . | 0/1/0 | . | . | 0/4/0 | . | . | . | . | . |
| tiles WH/ST/ME | 12/0/2 | . | 11/0/0 | 0/6/0 | 7/3/0 | 0/2/0 | 7/10/3 | 1/0/1 | 2/0/3 | 4/2/0 | 8/1/0 | 3/0/0 |
| land | . | . | . | . | . | 1 | . | . | 1 | . | . | . |

Season: 277 hires, 7 COW + 3 SHEEP, 142 wheat / 24 strawberry / 11 carrot /
10 melon / 5 tomato tiles, quadrants on d5 and d8.

## 4. Executability (12 ymg_aq boards, our seat, mean per board)

| d | hands tgt | ON | B | anim tgt | ON | B | tiles tgt (WH/ST/ME) | ON | B |
|---|---:|---:|---:|---|---|---|---|---|---|
| 0 | 4 | **4.0** | 4.0 | 0/2/3 | **0/2/3** | 1/4/1 | 12/0/2 | **12/0/2** | 11/0/0 |
| 2 | 4 | **4.0** | 3.0 | . | . | . | 11/0/0 | 3/0/0 | 0/0/0 |
| 3 | 4 | **4.0** | 5.0 | 0/1/0 | **0/1/0** | 0 | 0/6/0 | 0/0/0 | 5/2/0 |
| 6 | 9 | **9.0** | 4.0 | 0/4/0 | **0/0/0** | 0/0.2/0 | 7/10/3 | -1/2/2 | 0/3/2 |
| 8 | 8 | **8.0** | 5.9 | . | . | . | 2/0/3 | -5/0/3 | -2/1/1 |
| 10 | 11 | **11.0** | 8.4 | . | . | . | 8/1/0 | 6/1/-2 | 6/2/2 |

* **Hands: 100 %.** 277/277 over the season, every day exactly on target,
  including the 4 on day 0 that `FORWARD_ADMIT` could only lift to 2.
* **Day 0 is ymg_aq's board to the tile**: standing at dawn d1, ours
  `[12,0,0,0,2]` tiles and `[0,2,3]` herd, theirs `[12,0,0,0,2]` and `[0,2,3]`.
  B stands `[11,8,0,0,0]` and `[1,4,1]`.
* **Animals 60 %.** The day-0 plate and the d3 cow land; the **d6 request for
  4 cows is refused entirely** — dawn cash d6/d7 is 673/765 against ~400 a
  head after the day's other bills, the same budget-bound refusal
  `2026-09-14-herd-growth-screen.md` §2 measured. Herd at d10: ours 5.0,
  B 10.7, theirs 10.
* **Tiles 43 %, and this is the failure.** d2 asks 11 wheat and plants 3.
  Standing tiles at d10: ours 25.0, B 38.1, theirs 53. **Idle tiles at d10:
  ours 44.0, B 1.1.** A fixed per-day planting calendar assumes ymg_aq's own
  harvest cadence; ours differs from day 2 onward, so the schedule's plantings
  arrive on days with no free tiles and the days that do free tiles carry a
  target of zero. Site 1 makes the schedule the *whole* development plan, so
  where it says nothing, nothing is planted — the farm empties.

## 5. Coins (the gate)

| board set | ours (macro) | ours (B) | theirs | macro/theirs | B/theirs |
|---|---:|---:|---:|---:|---:|
| 12 ymg_aq boards | **55,306** | 93,127 | 138,009 | **0.401** | 0.871 |
| 68 band boards (diagnostic) | 67,062 | 104,092 | 142,466 | 0.471 | 0.998 |

ymg_aq boards: margin vs the tape **-82,703** (sd 21,350, t -13.4, win 0 %)
against B's -13,751 (t -8.5, win 0 %); paired our-coins macro - B **-37,821**
(t -8.8). Band boards: paired Δmargin **-75,212** (sd 22,575, **t -27.5**),
our coins -37,030 (t -19.9), against B's own -192 (t -0.1) on that set.
**The gate fails on both.**

## 6. What this says, and what remains

The FORWARD_ADMIT postmortem's sentence — "the top's ramp is hands, animals
and tiles bought together; the animal budget and the plant cap do not see the
projection" — is now **measured rather than inferred**, and it is only half
right. With all six gates lifted the ramp goes onto the board intact: the
crew, the herd and the plate of day 0 are ymg_aq's exactly. What does not
transfer is the *rest of the season*: an open-loop calendar cannot survive
contact with our own harvest clock, and the 44 idle tiles at d10 cost more
than the opening buys.

Remaining, in the order that matters:

1. **The tile line must stay closed-loop.** The obvious next arm: apply the
   schedule to hands + animals + land only, and let `brain.decide` keep
   `plant_target` (site 1 restricted to `animal_want`). That isolates the
   ramp's value from the calendar's cost and is one flag-day of work.
2. **`sell_hour` NOT BUILT.** `extract.py` writes it; nothing consumes it.
   The sale-timing family has no gene (`2026-09-14-herd-growth-screen.md`),
   so this is the one macro channel still unmeasured.
3. **The d6 cow refusal is a cash fact, not a planner fact** — same finding as
   the herd screen. A schedule cannot buy what the purse does not hold; only a
   different d0-d5 revenue line can.
4. **Per-board schedules.** The gate used one pooled schedule because the
   module constants are baked into the `jit` trace; d0-d5 is identical across
   the six episodes, so the opening is exact, but d6+ is a median. A
   theta-decoded schedule (the lead decision's next step) has no such problem.
