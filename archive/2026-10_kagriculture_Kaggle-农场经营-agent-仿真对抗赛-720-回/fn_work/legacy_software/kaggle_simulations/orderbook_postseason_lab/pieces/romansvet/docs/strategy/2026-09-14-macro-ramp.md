# 2026-09-14 — MACRO-RAMP: what is the ramp worth without the calendar?

**VERDICT: no mode beats B. The calendar was 87 % of EXEC-SCOPE's loss, and
the ramp is the other 13 % — still a loss.** Stripping the planting calendar
off the executor (`MACRO_MODE="hands"`: the crew is ymg_aq's, everything else
is B's) lifts the arm from **-37,030** coins/board to **-4,860** on the 68 band
boards (**t -9.1**, paired, 0 boards flipped to a win, 16 flipped to a loss)
and from -37,821 to **-2,736** (t -5.3) on the 12 ymg_aq boards. Adding the
herd calendar (`"hands_herd"`) costs a further **-13,785** on the band because
the schedule is a *ceiling* as well as a floor: it names 10 head, our purse
delivers 6, and it silences B's own herd line, which reaches **17.0 head** by
d16. The land calendar (`"hands_herd_land"`) is a **wash** (+481 coins, inside
noise) — it buys the third quadrant five days early, idles 28.8 of its tiles at
dawn d10, and has reconverged by d16.

So the answer to EXEC-SCOPE §6.1 is: **the top's crew is not the top's edge.**
Our planner can now field 277 hires a season on ymg_aq's exact day-by-day
profile, and doing so is worth **-4,860 coins/board** against the crew our own
enumeration picks.

Sim, descriptive, paired, CRN, action-replay opponent seat, theta B =
`flow193_g100_hr`, shipped `hr` switches. **No engine game, no training arm, no
ladder claim.** All coin figures are per-board means over the two seats.

## 1. What was built

`plan.MACRO_MODE` (`src/kagg3/core/plan.py:4708`), a module-level string
applied with `setattr` exactly like `MACRO_EXEC_ON`, selecting which of the six
`MACRO_EXEC` sites fire:

| mode | sites | what the schedule owns |
|---|---|---|
| `"full"` (default) | 1-6 | crew, herd, **mix**, land — EXEC-SCOPE's executor, unchanged |
| `"hands"` | 5, 6 | the crew, and only the crew |
| `"hands_herd"` | 1 (`animal_want` only), 3, 4, 5, 6 | crew + herd |
| `"hands_herd_land"` | + 2 | crew + herd + quadrant days |

Sites 5 (the hire argmax clip) and 6 (the `HIRE_ROW_ON` trim, excluded by
exclusion) are the ramp itself and fire under every mode, so neither carries a
mode test. Site 1's split lives in `_macro_targets` (`:4781`): under `"full"`
it writes `plant_target` and `animal_want`; under the three ramp modes it
writes `animal_want` and leaves `plant_target` to `brain.decide`, so the tile
line stays closed-loop. `_macro_site(n)` (`:4723`) is host-side and read at
trace time, like every other switch here, and raises on an unknown mode rather
than silently meaning `"full"`.

**The OFF path is character-identical.** Every line the diff removes is inside
one of the four `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:` blocks that
gained a nested mode test; the block headers, and every line outside them, are
untouched. `tests/test_macro_exec.py` pins it over the whole plan tuple on four
boards **for every mode including a nonsense one**
(`test_every_mode_is_inert_while_the_switch_is_off`).

`S/macro_exec/run.py` gains `--mode`; `S/macro_exec/report_ramp.py` is the
cross-mode ledger. Raws: `raw_{hands,hands_herd,hands_herd_land}.npz` (12
ymg_aq boards) and `raw_*_band.npz` (68 TOPB2/LIVEC boards), paired against the
existing `raw_headOFF.npz` and `raw_melOFF.npz` — the OFF baselines were not
re-run, since the board lists and the tree are the same and the OFF path did
not move. Full table in `S/macro_exec/report_ramp.md`.

## 2. The numbers

**12 ymg_aq boards** (B wins 0 % of these — they are top-five tapes):

| arm | our coins | theirs | Δcoins vs B (t) | Δmargin vs B (t) | hires/season | herd d3/d6/d10 | idle d10 | crop tiles d10 | flips +/- |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 93,127 | 106,879 | — | — | 261.2 | 6.0/6.5/10.7 | 1.1 | 38.1 | — |
| full | 55,306 | 138,009 | **-37,821 (-8.8)** | -68,952 (-11.2) | 277.0 | 5.0/5.0/5.0 | 44.0 | 25.0 | +0/-0 |
| **hands** | 90,391 | 113,943 | **-2,736 (-5.3)** | -9,800 (-6.4) | 277.0 | 6.0/5.5/9.2 | 2.0 | 38.8 | +0/-0 |
| hands_herd | 72,009 | 118,914 | -21,119 (-3.8) | -33,154 (-5.0) | 277.0 | 5.0/6.0/6.0 | 12.4 | 44.1 | +0/-0 |
| hands_herd_land | 72,162 | 119,028 | -20,966 (-3.8) | -33,115 (-5.1) | 277.0 | 5.0/6.0/6.0 | 25.4 | 43.6 | +0/-0 |

**68 band boards** (B wins 43 %, so flips are informative here):

| arm | our coins | theirs | Δcoins vs B (t) | Δmargin vs B (t) | hires/season | herd d3/d6/d10 | idle d10 | crop tiles d10 | win % | flips +/- |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 104,092 | 104,284 | — | — | 261.9 | 6.0/6.6/11.1 | 2.7 | 37.7 | 43 % | — |
| full | 67,062 | 142,466 | **-37,030 (-19.9)** | -75,212 (-27.5) | 277.0 | 5.0/5.0/5.0 | 40.8 | 29.2 | 0 % | +0/-29 |
| **hands** | 99,232 | 107,682 | **-4,860 (-9.1)** | -8,258 (-15.0) | 277.0 | 6.0/6.0/10.1 | 1.9 | 38.0 | 19 % | +0/-16 |
| hands_herd | 85,447 | 121,275 | -18,645 (-12.7) | -35,636 (-21.1) | 277.0 | 5.0/6.0/5.9 | 5.8 | 40.4 | 3 % | +0/-27 |
| hands_herd_land | 85,928 | 121,132 | -18,164 (-12.6) | -35,012 (-20.9) | 277.0 | 5.0/6.0/5.9 | 28.8 | 40.2 | 3 % | +0/-27 |

Every mode delivers **277/277** hires, on the exact per-day profile, on every
board — the executability result of EXEC-SCOPE holds under all four modes and
is not what is being measured any more.

`Δmargin` is roughly twice `Δcoins` in every row because the opponent seat is a
*shared-pot* replay: what we stop buying and stop selling reappears in their
prices. Their coins rise 104,284 -> 107,682 under `"hands"` and -> 121,275
under `"hands_herd"`. The coin column is the honest one for "is this worth
doing"; the margin column is what a promotion gate would score.

## 3. What the residual is made of

### 3.1 `"hands"`: -4,860 on the band is a reallocation, not an addition

Season hires 277.0 against B's 261.9 — but the schedule is *below* B on d3-d5
(-0.7/-0.4/-0.9) and far above on d6 (**+4.6**), d8 (+1.5), d9 (+2.8), d10
(+2.2). The herd (17.0 head by d16 against B's 17.0) and the tile line (56.3 vs
56.8 at d20) end up B's, so almost nothing else moves:

| arm | wage bill | sell revenue | buy spend | net | end coins |
|---|---:|---:|---:|---:|---:|
| B | 5,306 | 128,413 | 12,701 | 115,712 | 104,092 |
| hands | 5,837 | 124,367 | 13,039 | 111,328 | 99,232 |

The extra fifteen hands cost **+531** in fib bills and lose **-4,046** in sale
revenue. The wage is 11 % of the loss; the rest is the crew arriving on the
wrong days: **idle tiles at dawn d8 are 8.1 against B's 3.3** and crop tiles
35.0 against 39.7, i.e. the d6 surge of nine hands is spent on a farm that has
not been developed to feed it, and the four hands the schedule *withholds* on
d3-d5 are the ones that would have developed it. The gap accrues steadily
(-69 at d6, -480 at d9, -1,725 at d12, -3,207 at d18, -4,859 at d30) — it is
not an opening effect and it never recovers.

### 3.2 `"hands_herd"`: -13,785 more, and it is the ceiling, not the refusals

Two separate things happen, and only one is the refusal EXEC-SCOPE named:

* **Cash-refused asks: 4 of 10 head.** The d6 request for four cows is refused
  entirely — dawn cash d6 is 840 against ~400 a head after the day's other
  bills — exactly as `2026-09-14-herd-growth-screen.md` §2 measured. Delivered
  6.0 head (5 on d0, 1 on d3), 60 %, identical under `"full"`.
* **The ceiling: 11 head B buys and the schedule forbids.** B buys **17.0** head
  over the season and stands at 17.0 by d16; under the schedule the herd
  **freezes at 5.9 from d8 to the end of the season**, because site 1 makes
  `animal_want` the schedule's whole word and the schedule says 0/0/0 on every
  day after d6. This is the larger half by far, and the coin trace proves it:
  the arm is **ahead of B by +2,588 coins at dawn d12** (a small herd is cheap)
  and behind by -7,209 at d18, -14,934 at d27, -18,644 at the end. The animal
  line is a compounding revenue stream and capping it is a back-half tax.

ymg_aq's own tape carries 7 COW + 3 SHEEP and earns 142k; the schedule is not
wrong *for them*. It is wrong for us because the rest of B's play — its
selling, its shed, its tile mix — is tuned to a 17-head farm.

### 3.3 `"hands_herd_land"`: a wash

+481 coins over `"hands_herd"` on the band (+153 on ymg), both far inside the
board-to-board sd. The forced d5/d8 quadrants put `nquad` at 3.00 by dawn d10
against B's 2.00 and leave **28.8 idle tiles** there against B's 2.7 — tile
displacement with no coin consequence, because the farm catches up by d16 (idle
1.8 vs B's 1.2 at d20) and B buys the same third quadrant a few days later
anyway. **The land calendar is neither the loss nor a lever.**

### 3.4 Where `"full"`'s remaining -32,170 lived

`full` - `hands` on the band is -32,170 coins, and §3.2/§3.3 account for
-13,785 of it via the herd. The balance, **~-18,400, is the planting calendar
alone** — 40.8 idle tiles at dawn d10 against 1.9 under `"hands"`, sell revenue
84,958 against 124,367. EXEC-SCOPE's verdict stands and is now quantified: the
calendar is the single most expensive of the three channels.

## 4. Tests

```
$ JAX_PLATFORMS=cpu python -m pytest tests/test_macro_exec.py -q
................                                                         [100%]
```

16 tests, all pass (`pyproject.toml` already carries `addopts = "-q"`, so the
second `-q` suppresses the count line; `--collect-only` reports "16 tests
collected"). Seven are new:

* `test_the_default_mode_is_the_executor_the_gate_measured` — `"full"` is the
  default and sites 5/6 fire under every mode.
* `test_mode_full_is_the_whole_schedule` — crew, herd, mix AND land, unchanged.
* `test_mode_hands_takes_the_crew_and_nothing_else` — 4 hands; herd 0, the
  schedule's melon tiles 0, land 0 (the decode's own answer on that view,
  measured with the switch off).
* `test_mode_hands_herd_writes_the_herd_but_not_the_tiles` — 4 hands, 2 COW +
  3 SHEEP, melon 0, land 0.
* `test_mode_hands_herd_land_adds_the_quadrant` — the same plus land 1.
* `test_an_unknown_mode_is_an_error_not_a_silent_full`.
* `test_every_mode_is_inert_while_the_switch_is_off` — the whole plan tuple on
  four boards, for all four modes and a nonsense one.

## 5. What this says

1. **The crew channel is closed.** 277/277 delivered, on the top's exact
   profile, is worth -4,860 coins/board (t -9.1) and 16 lost boards. Hand count
   is not what separates 2715 from 3004; the FORWARD_ADMIT hypothesis is now
   measured on both ends and both ends lose.
2. **The macro-as-ceiling defect is a build bug, not a finding.** Site 1
   overwrites `animal_want` on *every* day, including the 24 days the extracted
   schedule says nothing about, which silences B's own herd growth. A schedule
   that named only floors (`animal_want = max(decode, schedule)`) would separate
   "the top's opening plate" from "stop growing the herd" — the -18,645 above
   confounds the two. That is the one cheap experiment left in this family.
3. **The land calendar is measured and empty.** Neither loss nor lever; drop it
   from any future macro arm.
4. **`sell_hour` is still NOT BUILT** — unchanged from EXEC-SCOPE §6.2, and now
   the only macro channel of the four that has never been priced.

## 6. Next experiment

**FLOOR-NOT-CEILING**: one flag-day change to `_macro_targets` making the
schedule's herd a floor (`animal_want = maximum(decode, schedule)`) under a
fifth mode, re-run on the same 68 band boards. If the arm lands between
`"hands"` (-4,860) and `"hands_herd"` (-18,645) at around -5k it confirms the
ceiling was the whole herd cost and the opening plate is free; if it lands
*above* `"hands"` it is the first positive signal this family has produced and
the day-0 0/2/3 plate is a real lever. Either way it is the last unconfounded
question the schedule channel holds, and it costs one 5-minute run.
