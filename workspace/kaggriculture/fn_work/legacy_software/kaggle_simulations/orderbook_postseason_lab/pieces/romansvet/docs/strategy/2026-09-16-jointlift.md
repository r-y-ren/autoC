# JOINTLIFT: tiles AND hands together — the one shape the archive never ran

**Verdict (sim, paired CRN, 68 band + 44 ENG22 seats + 20 TOP5NOW seats).**
The joint arm is **falsified, hard, on all three board sets.** Tiles + hands
together is **−4,835 coins of margin (t −13.1) on the 68 band**, −3,421
(t −8.5) on the 44 ENG22 seats and −3,241 (t −5.8) on the 20 TOP5NOW seats,
with **24 outcome flips, every one of them to the opponent** and win % 42.6 →
17.6 on the band. It is not the sum of its parts and it is not a near miss: it
is the tiles leg's own loss (−5,009, t −14.1) with +174 of the crew leg's
credit on top. No arm came within 3.1k of the +300/t 2 sim bar, so **no engine
POOLED180 leg was run** and no §115b read exists. `CREW_PUSH_COST_ON` sum
alone reproduced its stored +53 t 0.57 to the coin and is still level.

**The mechanism, in one line:** the hands do get tasks and the tiles do get
labour — and it is the *wrong* labour. The joint arm plants **+19 more tiles a
game (193.4 → 212.4), every one of them wheat (99.8 → 121.2), and makes
exactly zero extra wheat** (322.01 → 321.87 units, t −0.04). Total crew-turns
worked move **+41 a game** against the 695 `2026-09-14-turns.md` says we are
short. The extra PLANT turns come out of the CARE/FEED/COLLECT chain:
**FERTILIZER −23.3 units (t −16.8), CARROT −20.5 (t −8.1)**, all nine products
**−64.1 (t −13.0)**. The route's own `value_dropped` goes **514 → 5,810 coins a
game**, 5,418 of it in d20-29. We buy the seed, spend the turn putting it in
the ground, and the crop is never watered to maturity.

Both prior verdicts were right, and they compose the wrong way round: the fill
is not labour-starved because the crew will not grow (it grows by itself,
+8.25 hires a season, the moment the tiles arrive), it is labour-starved
because **the board is already at full labour utilisation** — PASS share
14.2 %, unchanged by every arm except the one that lifts the HIRE_ROW clamp.

Sim only. Nothing here reached the engine.

---

## 1. What was run

Harness `S/macro_exec/run.py` (paired, CRN, both seats, byte-exact
action-replay opponent seat), theta B `flow193_g100_hr`, shipped `hr` switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON`.

```bash
bash S/jointlift/launch.sh        # 7 arms x 68 band      (369 s)
bash S/jointlift/launch_eng.sh    # 8 arms x ENG22/TOP5NOW (712 s)
export JAX_PLATFORMS=cpu
.venv/bin/python S/jointlift/instrument.py both 10 'PLANT_FILL_LATE_ON,CREW_PUSH_COST_ON,CREW_PUSH_COST_MODE=sum'
.venv/bin/python S/jointlift/probe_report.py off fill push both bothnr
```

**Identity legs, both clean.** `raw_jl_band_ident.npz` (this edited tree, every
new switch OFF) is **byte-identical to the stored `S/macro_exec/raw_melOFF.npz`
on every array** — +0 coins, +0 margin. `raw_jl_e22_off.npz` is likewise
byte-identical to the stored `S/macro_exec/raw_t15_e22_off.npz`. The port below
is invisible OFF.

**One source change**, the smallest the measurement allowed:
`PLANT_FILL_LATE_ON` / `PLANT_FILL_FROM_DAY = 12` did not exist on master. They
were built on the `board-fill` worktree (`cd8a040`) and **never merged**, so
`2026-09-09-board-fill.md` sect.4's lever had no code to run. Ported verbatim
into `src/kagg3/core/plan.py:5071-5095` (switch + day constant) and `:6636-6661`
(6 lines: the `or`, the day gate on `fill_target`, the day gate on `w_fill`),
default OFF, with `tests/test_plant_fill_late.py` — 9 tests, the
`tests/test_crewpush.py` pattern, OFF pinned on whole-plan digests against a
pristine `git archive HEAD src` tree. All 9 pass.
(`tests/test_route_early.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner`
and `tests/test_budget_order.py::test_grow_multiplier_tilts_the_seed_mix` fail
— **verified pre-existing on HEAD** with the port stashed.)

### Why day 8 is the "earlier day"

`2026-09-09-board-fill.md`'s herd argument is that the fill must not start
before the herd is bought, because the channel is `n_free` → `n_dev` →
`animal_count`. On the 68 band the OFF baseline's herd curve (dawn animal
count, `raw_melOFF.npz`) is **flat at 6.00 through day 7**, then 7.00 (d8),
9.79 (d9), 11.12 (d10), 15.44 (d11), 16.29 (d12), plateau ~16.9 from d13.
The herd wave is **d8-d11**. Day 8 is therefore the first day on which any
herd beyond the opening six has been bought, and the last candidate that does
not put the fill strictly in front of the herd; **day 6 does**, and is carried
below as the control the argument predicts should be worse. It is: −5,760 vs
−4,875.

## 2. The band table (68 boards, paired CRN, sim)

| arm | our coins Δ | their coins Δ | **MARGIN Δ** | t | win % | flips (to us / to them) |
|---|---:|---:|---:|---:|---:|---:|
| (1) `PLANT_FILL_LATE_ON` alone (d12) | −4,723 | +286 | **−5,009** | −14.13 | 42.6 → 14.7 | 0 / 19 |
| (2) `CREW_PUSH_COST_ON` sum alone | +68 | +15 | **+53** | +0.57 | 42.6 → 42.6 | 0 / 0 |
| (3) **both** | −4,591 | +244 | **−4,835** | −13.12 | 42.6 → 17.6 | 0 / 17 |
| (4) both, `PLANT_FILL_FROM_DAY=8` | −4,358 | +517 | **−4,875** | −14.49 | 42.6 → 22.1 | 0 / 14 |
| (4c) both, `PLANT_FILL_FROM_DAY=6` (control) | −4,980 | +780 | **−5,760** | −16.40 | 42.6 → 16.2 | 0 / 18 |
| (5) both, `HIRE_ROW_ON=False` | −7,172 | +232 | **−7,404** | −16.04 | 42.6 → 11.8 | 0 / 21 |

Arm (2) is the stored `2026-09-16-crewpush.md` read reproduced to the coin
(+53, t 0.57) — the CRN is intact and the port did not move it.

**Both is not additive.** (3) − (1) = **+174** of margin: the whole of the crew
leg's contribution on top of the tiles leg is a rounding error against the
tiles leg's −5,009. The two levers do not compound; the tiles leg simply
dominates.

## 3. Does the extra crew get tasks? Does the extra land get labour?

`S/jointlift/instrument.py` replays each arm's **own trajectory** day by day on
the first 10 TOPB2 boards and reads the plan the rollout actually runs, plus its
`DayStats` — the quantities the sim raws cannot carry.

| per game, 10 TOPB2 boards | off (B) | fill | push | both | both, no HIRE_ROW |
|---|---:|---:|---:|---:|---:|
| **PLANTINGS, season** | 193.4 | 215.2 | 194.0 | **212.4** | 216.0 |
| .. wheat | 99.8 | 122.6 | 100.4 | **121.2** | 122.2 |
| .. carrot / tomato / straw / melon | 43.4 / 1.6 / 32.6 / 16.0 | 43.4 / 1.0 / 32.4 / 15.8 | 43.4 / 1.6 / 32.6 / 16.0 | 41.8 / 1.2 / 32.6 / 15.6 | 44.4 / 1.4 / 32.6 / 15.4 |
| seeds BOUGHT, season | 193.8 | 222.4 | 194.4 | 221.0 | 223.0 |
| HIRE-row hands, season | 261.7 | 265.0 | 262.1 | 263.6 | **293.2** |
| hand INTENT `n_hire`, season | 283.6 | 290.2 | 288.6 | 293.2 | 293.2 |
| **intent the clamp refused** | 21.9 | 25.2 | 26.5 | **29.6** | **0.0** |
| **crew-turns WORKED (non-PASS)** | 6,003.8 | 6,068.0 | 6,000.7 | **6,045.2** | 6,049.6 |
| crew-turns offered (cells) | 7,000.8 | 7,080.0 | 7,010.4 | 7,046.4 | **7,756.8** |
| **PASS share of crew-turns** | **14.2 %** | 14.3 % | 14.4 % | **14.2 %** | **22.0 %** |
| idle tiles at dawn, tile-days | 215.0 | 149.6 | 211.2 | 154.4 | 144.8 |
| **route `value_dropped`, coins** | **514** | 5,718 | 408 | **5,810** | 5,220 |
| purchase shortfall, coins | 12,439 | 12,425 | 12,439 | 12,542 | 12,710 |
| units CLIPPED at EOD (overflow) | 0.0 | 5.2 | 0.0 | 5.2 | 2.4 |

crew-turns worked / PLANTINGS / `value_dropped`, by window:

| days | off (B) | fill | push | both | both, no HIRE_ROW |
|---|---:|---:|---:|---:|---:|
| d0-5 | 554 / 52.0 / 38 | 554 / 52.0 / 38 | 554 / 52.0 / 38 | 554 / 52.0 / 38 | 563 / 52.4 / 13 |
| d6-11 | 960 / 41.8 / 0 | 960 / 41.8 / 0 | 960 / 41.8 / 0 | 960 / 41.8 / 0 | 961 / 41.8 / 21 |
| d12-19 | 2,061 / 36.2 / 2 | 2,100 / 40.4 / 316 | 2,060 / 36.2 / 0 | 2,097 / 40.4 / 354 | 2,073 / 40.2 / 67 |
| d20-29 | 2,429 / 63.4 / 474 | 2,454 / 81.0 / 5,364 | 2,427 / 64.0 / 370 | 2,434 / 78.2 / **5,418** | 2,453 / 81.6 / 5,119 |

**Read.**

1. **The tiles buy the hands by themselves.** The fill leg *alone* moves the
   season's hires +8.25 (t +20.5, band raws); the push leg alone moves them
   **+0.16 (t +1.5)**. Causation runs tiles → hands, never hands → tiles. The
   premise that "more hands supply the labour the extra tiles need" is
   therefore vacuous: once the tiles are there the enumeration hires the hands
   without any help from `CREW_PUSH_COST`, which is exactly why (3) − (1) is
   +174 and not a lift.
2. **The extra hands are already fully loaded.** PASS share is 14.2 % OFF and
   14.2 % in the joint arm. The crew is not sitting idle waiting for work: the
   whole crew-turn budget moves **+41 a game** (6,003.8 → 6,045.2) for +19
   plantings. `2026-09-14-turns.md`'s 695-turn gap closes by 6 %.
3. **The work the tiles create is dropped, not done.** `value_dropped` — coins
   of queued task value the day's route does not reach — goes 514 → 5,810, and
   93 % of it lands in d20-29, exactly where the fill's wheat would have needed
   its WATER and HARVEST. The board-fill dry run saw the same thing on the
   engine (route drops 9 → 50, 4 → 87, 35 → 79 over d10-29).
4. **So the extra wheat is never made.** +21.4 wheat plantings, +27 seeds
   bought, and wheat units produced **322.01 → 321.87 (t −0.04)**. The seed
   coin and the PLANT turn are both spent; the unit never arrives.
5. **What the PLANT turns displace is the herd chain**, as `PLANT_FILL_ON`'s
   own autopsy said: FERTILIZER 192.7 → 169.4 (−23.3, t −16.8), CARROT
   107.8 → 87.3 (−20.5, t −8.1), STRAWBERRY −5.8, EGG −3.8, MELON −3.9 — all
   nine products **1,411.3 → 1,347.2, −64.1 units (t −13.0)**. At
   `2026-09-16-spread6.md` sect.5.1's 159 coins of margin per unit that is
   −10.2k gross; we lose −4,835 net because the smaller book realises a better
   price (91.45 → 92.82) and buys 7.4 fewer wheat.

### The HIRE_ROW clamp (arm 5)

`HIRE_ROW_ON` guards **one thing and only one thing**: `n_hire_row =
min(n_hire, n_act)` at `plan.py:7863-7878`, the count the HIRE *market row*
asks for. It does not touch `n_units`, `wide`, `route_base`, the bill,
`turn_budget`, `land_lead`, the admit stage's labour or `crew_now` — the
switch's own docstring makes the decoupling the point, and the retired
`HIRE_CLAMP_ON` (which clamped the *intent* and cost −3,203 a game) is the
thing it was built not to be. It is excluded under a `MACRO_EXEC` schedule
(the fifth MACRO_EXEC site, by exclusion) because a schedule's premise is that
the ramp is bought before the work exists. Turning it off is therefore safe in
the narrow sense — nothing else changes — and it is the exact lever the
crewpush report named as eating 40/42 moved intents.

Off, it does exactly what it says: **intent refused 29.6 → 0.0** hands a
season, HIRE-row hands 263.6 → 293.2, crew-turn cells 7,046 → 7,757
(**+710 hand-turns bought**). Crew-turns *worked*: 6,045.2 → 6,049.6.
**+710 hand-turns bought buys +4 turns of work.** PASS share 14.2 % → 22.0 %,
production flat (1,347.2 → 1,348.2 units), and the fib bill takes another
**−2,569 of margin** (−7,404 vs −4,835). This is the cleanest measurement the
campaign has of "the crew is task-limited, not push-limited", and it closes the
HIRE_ROW question as well: the clamp is not what stands between us and the
top's crew.

## 4. Hands × tiles on the band (68 boards, joint arm vs B)

| quantity | B (off) | both | paired Δ | t |
|---|---:|---:|---:|---:|
| hands FIELDED d5 / d10 | 4.94 / 8.82 | 4.94 / 8.82 | +0.00 / +0.00 | — |
| hands FIELDED d15 / d20 | 11.94 / 11.49 | 12.15 / 11.68 | +0.21 / +0.19 | +3.02 / +2.72 |
| hires, season | 252.8 | 260.9 | +8.09 | +18.28 |
| planted tiles dawn d15 / d20 | 56.16 / 56.78 | 57.81 / 58.09 | +1.65 / +1.31 | +11.9 / +13.6 |
| planted TILE-DAYS d0-29 | 1,223.4 | 1,286.1 | +62.72 | +26.70 |
| idle TILE-DAYS d12-29 | 148.7 | 88.6 | −60.18 | −23.66 |
| animals dawn d15 | 16.94 | 16.82 | −0.12 | −2.64 |
| units made, all nine | 1,411.3 | 1,347.2 | **−64.07** | **−13.02** |

The fill **works** as a fill: idle tile-days d12-29 fall 40 %, planted tile-days
rise +63. The d5 and d10 crew and tile counts are untouched, so the ramp is
intact and this is a purely late-board change — the herd argument's own
requirement, satisfied. It still loses.

`2026-09-16-pop-shift.md` sect.3's gap is 282 plantings and 11.1 hands at d10
against our 192 / 9.1. This arm reaches **212 plantings and moves d10 hands by
0.00**. The plantings half of the gap is 22 % closed and costs 4.8k; the hands
half does not move at all, because d10 hiring is set by the ramp and the fill
is refused before d12 by construction.

## 5. The engine classes (sim, paired CRN)

| arm | 44 ENG22 seats: margin Δ (t) | flips | 20 TOP5NOW seats: margin Δ (t) | flips |
|---|---:|---:|---:|---:|
| `PLANT_FILL_LATE_ON` alone | **−3,811** (−11.23) | 0 / 7 | **−3,065** (−5.08) | 0 / 2 |
| `CREW_PUSH_COST_ON` sum alone | **−15** (−0.13) | 0 / 0 | **−72** (−2.15) | 0 / 0 |
| **both** | **−3,421** (−8.46) | 0 / 5 | **−3,241** (−5.78) | 0 / 2 |

Same shape, same size, same sign against the 2953+ engine class and against
the ten TOP5NOW boards that pass both fidelity gates. On ENG22 the joint arm
is again the tiles leg plus +390, all nine products −38.8 units (t −5.6) with
FERTILIZER −16.6 and CARROT −19.7 — the identical displacement. The push leg's
+53 on the band is **−15 on ENG22 and −72 on TOP5NOW**: it is noise of one sign
on the band and noise of the other sign on the engine class, which is what
t 0.57 always meant.

## 6. What this closes

- **The joint shape is dead.** The archive's two verdicts ("tiles lose because
  labour binds", "hands are inert because the crew is task-limited") do not
  leave a joint lift open, because the second one is not a *supply* statement
  about hands — it is a statement that **the crew is already working 85.8 % of
  its turns**. Adding tiles adds queued value the route drops; adding hands
  adds PASS. Neither direction has slack to trade.
- **`PLANT_FILL_LATE_ON` now has its paired run** and it is a loss on all three
  board sets. The `2026-09-09-board-fill.md` "NOT VERIFIED" line is discharged:
  the late half of v2 is *not* where v2's loss is absent, it is where it is
  concentrated. Ships OFF, tested OFF.
- **`HIRE_ROW_ON` is confirmed as shipped.** Lifting it buys 710 hand-turns a
  game and 4 turns of work, for −2,569.
- The next tile on this board has to come with **labour that is not taken from
  the herd chain** — i.e. a route/admit change, not a purchase change. That is
  `_admit`'s question (`plan.py:6446`), which this family never touched.

## 7. Not done

- **No engine leg.** The §115b bar needs a sim arm at ≥ +300 t ≥ 2 before
  `S/judge7065/run_band180.sh` is worth 180 boards; the best arm here is +53
  (t 0.57) and the rest are −3.4k to −7.4k. Nothing was submitted to the
  engine and no POOLED180 number exists for any of these switches.
- `PLANT_FILL_FROM_DAY` was swept at 6, 8 and 12 only, and `both8`'s
  −4,875 leaves no reason to sweep finer.
- `PLANT_FILL_RESERVE_DAYS` (the fill's herd reserve, 3) was not swept; the
  herd damage here is a *route* displacement (FERT/CARROT, not animals bought
  — animals at d29 are +0.65), so a bigger reserve is unlikely to be the fix.
- The probe is 10 TOPB2 boards, not 68: the plan-level quantities (PLANTINGS,
  PASS share, `value_dropped`) are the head of the band, the coin/margin/unit
  numbers are all 68/44/20.
