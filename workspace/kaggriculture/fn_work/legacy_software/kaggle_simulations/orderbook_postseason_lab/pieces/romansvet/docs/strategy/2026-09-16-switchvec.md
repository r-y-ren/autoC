# SWITCHVEC — the plan's switch VECTOR is additive; there is no "three on, two off"

2026-09-16, branch `switchvec`. Every one of the plan's ~66 module switches had been judged
ONE AT A TIME. `SELL_SLOT_PRIORITY_ON` was the standing proof that this is not enough:
REJECTED alone (+394), PASSED stacked on `LOT4@17` (+459). The user asked the next question —
*what if the win needs three switches on and two off?* This is the first search of the vector.

**VERDICT — §115b NOT MET, no POOLED180 cut, and the family is CLOSED by measurement.** Two
complete `2^5` cubes (all 5 main effects and **all 10 two-factor interactions estimated with
zero aliasing**, on two independent tape families) say the switches are **additive to within
~15 %**: the largest interaction is 1/7 of the largest main effect and **not one of 40 simple
effects changes sign**. One candidate is handed to the lead: `OPEN_PUMP_ON=False` +
`CLIP_CAP_ON=True`, sim **+387 (t +2.05)** pooled over 128 boards.

## 1. Tool, reference, boards
`S/switchvec/screen.py` = `S/simscreen/screen.py` with `WORKTREE` pointed at this tree. That
matters: the shipped tool imports the stale `.claude/worktrees/arms-next` checkout, which
predates `LOT4_ON`, `SELL_SLOT_PRIORITY_ON`, `CLIP_CAP_ON`, `SHED_DUMP_ROW_ON` and
`CREW_PUSH_COST_ON` — **it cannot screen the pair at all**, and its `HR_SWITCHES` default is
not the pair either. Reference here is the pair: the six-switch `BASE` of `S/combo2/run_all.sh`
(`2026-09-16-judge-baseline-rule.md`). Boards: new `S/switchvec/boards_v45leg2.json` — the 44
post-09-15 `S/v45leg2/ids.txt` tapes, pinned town, both seats, 1 seed = **88**; hold-out
`S/simscreen/boards_topb2.json` = **40**.

One switch vector per process, paired OFFLINE against the reference process. Licensed by
byte-reproducibility: `REF`/`T11`/`T22` (chunk 44/11/22) and `OPT1`
(`--xla_backend_optimization_level=1`) agree on **88/88 margins**, `shopdiff` 0.0 % everywhere.
Cost ≈ 400 s single-threaded TRACE + 40 s of episodes, so boards are nearly free and width is
everything: `PAR=4 x OMP_NUM_THREADS=2` (the 8-thread budget of 2 x OMP 4) ran 74 screens.

## 2. Factors — K = 12, N = 42 runs
Defaults, best single reads and every exclusion with its reason: **`S/switchvec/factors.md`**.
* **CORE (5, full `2^5` = 32 runs, resolution ∞)**: `LOT4_ON`, `SELL_SLOT_PRIORITY_ON`,
  `OPEN_PUMP_ON`, `CLIP_CAP_ON`, `TAIL_FILL_ON` — the shipped pair, the thrice-measured
  pump-off gradient, the largest surviving positive rejected alone (POOLED180 +131), and the
  only sweep arm that ever read over +1,000. One per mechanism family.
* **SECONDARY (7, Plackett-Burman 8, res III, core held at the pair)**: `BANK_BEFORE_LOT_ON`,
  `HIRE_ROW_ON`, `OPP_SUPPLY_ON`, `CARE_FILL_ON`, `CREW_PUSH_COST_ON`, `SHED_DUMP_ROW_ON`,
  `CARE_HOLD_ON`.
* **OUT**: 17 hard rejects (|Δ| > 2,000, `FERT_RESERVE_ON` −32.7k … `ROUTE_EARLY_ON` −158.9k),
  7 measured-inert, 5 assert-blocked or inert without a companion (`PRESTOCK_ON` /
  `MARKET_PACK_ON` need `EARLY_SELL_ON=False`, a +2,184 t 5.1 lever = a different bundle), and
  every companion integer fixed at its documented value (`LOT4_TURN=17`, `SHED_DUMP_ROW_TURN=23`).

## 3. Main effects — Δmargin OFF→ON, paired, 16 runs vs 16
| factor | 88-board | 40-board hold-out | prior single read | agrees |
|---|---|---|---|---|
| `LOT4_ON` | **+720 (t +11.18)** | **+621 (t +5.64)** | POOLED180 +791 t +13.19 | yes |
| `TAIL_FILL_ON` | +701 (t +4.77) | +414 (t +1.48) | sim LEG20 +1,366 t +2.61 | yes |
| `SELL_SLOT_PRIORITY_ON` | **+445 (t +7.32)** | **+413 (t +6.30)** | +394 alone / +459 on LOT4 | yes |
| `OPEN_PUMP_ON` | −270 (t −2.35) | −247 (t −0.63) | pump-OFF +335…+410 t≈2.2 | yes |
| `CLIP_CAP_ON` | +49 (t +0.73) | +275 (t +2.07) | POOLED180 +131 t +2.00 | yes |

Every sign holds on both families and the two shipped levers reproduce their engine reads
almost exactly. The cube is not fitting noise.

## 4. Interactions — all ten, clear (a full `2^5` has no alias structure)
88-board, with the first factor's simple effect at the second OFF / ON:

| pair | Δ | t | eff(2nd OFF) | eff(2nd ON) | sign flip |
|---|---|---|---|---|---|
| PUMP × TAILFILL | −108 | −0.77 | −162 | −378 | no |
| **LOT4 × SLOTPRIO** | **+68** | **+4.93** | +652 | +789 | no |
| PUMP × CLIP | −58 | −2.13 | −212 | −328 | no |
| CLIP × TAILFILL | −45 | −1.40 | +94 | +4 | no |
| SLOTPRIO × TAILFILL | +37 | +2.64 | +407 | +482 | no |
| the other five | ≤ \|14\| | — | — | — | no |

Hold-out: largest `PUMP × TAILFILL` **+244** (t +2.36), then `PUMP × CLIP` −143,
`CLIP × TAILFILL` +114; the other seven ≤ |45|; again **no sign flip**. The two files disagree
about which interaction is biggest — that is the noise floor on this quantity, ≈ ±200 coins.

**This is the answer.** Interactions are real (`LOT4 × SLOTPRIO` at t +4.93 is exactly the
synergy that turned SLOT-PRIO from a 56-coin REJECT into a §115b PASS) but the largest of the
ten is +108 against main effects of 445–720, and a switch that loses alone loses in every
context. **One-at-a-time judging was not leaving a combination on the table.**

## 5. The one real vector finding — pump-OFF **+** clip-cap
Cell `C27` is the only vector in either cube positive on **both** files, and its parts are not:

| vs the pair | 88-board | 40-board hold-out | pooled 128 |
|---|---|---|---|
| `C25` pump-OFF alone | +381 (t +2.10) | **−153 (t −0.38)** | +214 (t +1.20) |
| `C31` clip-cap alone | +28 (t +0.37) | +219 (t +1.16) | +88 (t +1.11) |
| **`C27` both** | +359 (t +1.85) | **+449 (t +1.04)** | **+387 (t +2.05)** |

Adding `CLIP_CAP_ON` on top of pump-off is **+173 (t +2.69)** pooled (+603 t +4.60 hold-out,
−23 on the 88). Mechanically it is the sign `PUMP × CLIP` has: the clip cap holds night-haul
stock the opening pump would otherwise price against. Both parts are already banked on the
engine alone (`PUMPOFF3` POOLED180 +335 t +2.2; `SHEDCLIP` +131 t +2.00), whose additive sum
is +466. It is a **two**-switch effect, not a hidden multi-switch regime.

## 6. Secondary seven, and a method warning
PB-8 OFF→ON (res III — alias strings, not verdicts): `HIRE_ROW_ON` **+1,873 / +2,778**,
`CARE_FILL_ON` −495/−540, `OPP_SUPPLY_ON` −677/−525, `CREW_PUSH_COST_ON` −413/−361,
`CARE_HOLD_ON` −179/+424, `BANK_BEFORE_LOT_ON` +218/−108, `SHED_DUMP_ROW_ON` +111/+59. Both
shipped-ON switches want to stay on — `HIRE_ROW_ON` far more strongly than its old −378/game
estimate. `OPP_SUPPLY_ON`'s +617 t +2.54 from the 09-09 pinned sweep does not survive on fresh
tapes.

**`SHED_DUMP_ROW_ON`'s +111 / +980 is an alias artefact.** Direct runs `X1`/`X2` (pump-off ±
clip, with the switch on) are **byte-identical to `C25`/`C27` on 88/88 and 40/40 boards** — it
moves exactly zero coins, confirming `2026-09-16-sheddump.md` from the other side. A res-III
main effect is an alias string, not a read: cubes, or a direct flip, or nothing.

## 7. Next
* **For the lead to cut (§115b):** `BASE,OPEN_PUMP_ON=False,CLIP_CAP_ON=True` vs the pair,
  both arms on **one** tree — `plan.py` moved 621 lines between `ee8dedd` (where `c2_combo`
  was banked) and master `4c6565b`, so the banked control is not comparable. Not cut here: the
  confirmation gate (+450 on both files) is missed, and the engine runners write into the main
  checkout's shared `S/lossflip/`, which this box must not touch.
* **Closed:** no further fractional-factorial or vector run is worth a slot.
* Files: `S/switchvec/{factors.md,design.csv,run_screen.sh,screen.py,fit.py,results.md,
  boards_v45leg2.json,csv/,csv_topb2/,logs/}`. 74 screens, ~340 s each, 4-wide, box 14:26–17:15Z.
