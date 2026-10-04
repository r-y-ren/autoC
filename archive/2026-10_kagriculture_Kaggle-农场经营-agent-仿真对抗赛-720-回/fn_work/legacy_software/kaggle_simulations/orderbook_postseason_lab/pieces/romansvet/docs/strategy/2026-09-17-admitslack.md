# ADMITSLACK — the admit stage's step budget against the day it really spends

2026-09-16 21:20–22:50Z, branch `admitslack` off master `0e66a6e` (FT2 +
ROUTEEFF + EVESTOCK). Follow-up to `2026-09-16-evestock.md` §5.2 ("any further
morning work must come from the labour credit being wrong about which tiles are
worth reaching — an admission arm"), `-routeeff.md` §3, `-lossmap2.md` §4-6,
`-idleops.md` §4. Leg: ENG22 (22 engine tapes, both seats, 44 games). No
training, no upload, remote untouched.

## 1. VERDICT

**The admission step estimate IS mis-calibrated, the switch that repairs it is
the first positive engine read this family has produced, and it is not a
promotion.** `ADMIT_SLACK_ON` (one turn a unit handed back to the admit stage)
on ENG22: **+326/board (sd 931, t +1.64)** on the seed the control was cut at,
**+388/board (sd 920, t +1.98)** on a second independent seed of the same 22
tapes, **pooled +357/board (se 138, t +2.59; per game +357, se 97, t +3.67)**,
board win **40.9 → 45.5 %** and **45.5 → 50.0 %**, flips **+2/−0** over the two
seeds. Kill gate (+100 at t ≥ 2): **PASS on the pooled read**, short of t = 2 on
either single seed. **Two purses: ours +162 (t +3.35), theirs −195 (t −3.34)** —
the first lever of this campaign that takes the coins off the other seat rather
than paying it. **V45LEG (30 clone boards): −44/board, t −0.18, win 70.0 →
66.7 %, flips +0/−1 — null.** POOLED180 not run; the lead decides.

The mechanism is measured on both ends. Admission's per-unit overhead is
charged at 6.08 steps a unit-day against a realised 3.20, and half the d20-29
days decline a ranked task on that budget while the crew ends the day idle. ON,
the day admits **+1.17** more tasks at the budget (`n_adm0` 58.14 → 59.31) — of
which the `ADMIT_ROUNDS` repair takes back **+0.80** (drop 1.80 → 2.60), so the
routed set rises **+0.38** a day, PROD ops **120.89 → 121.81** a day (**+9.2 a
game** in d20-29) and tail idle **16.02 → 15.82**. The repair loop is where 2/3
of the admitted slack goes, and that is the switch working as designed: what
the exact route cannot reach is dropped from the value tail.

## 2. The instrument — both halves of the same day

`S/admitslack/probe.py` = ROUTEEFF's engine-side step ledger (every unit step
is MOVE / PASS / PROD, so per unit-day `prod = present − move − pass`) **plus a
planner-side hook**: `_plan_and_stats` is wrapped, and the admission stage's own
numbers are read off the helpers it calls —

| captured | where | what it is |
|---|---|---|
| `n_tasks` | `task_order(d.task, d.tile_value, d.tier)` | the ranked task set |
| `cum_est` | the array `_count_le` reads at `plan.py:9287` | `cumsum(n_ops + EST_MOVES)` in value order |
| `labour` | the scalar it is compared against | `n_units * (turn_budget − max(_pickup_kinds, land_lead) − EST_LEAD)` |
| `n_adm0`, `n_adm` | `min(count, n_tasks)`, then each `_routes` round | admission before and after the `ADMIT_ROUNDS` repair |

so every day carries its **estimated** step bill and, from the same game, its
**realised** one. 22 boards, our seat, ~4 min at `WORKERS=3`.

## 3. The calibration (ENG22, our seat, d20-29, 220 unit-days of planning)

| per day | estimate | realised |
|---|---:|---:|
| admitted-task steps | **161.2** (`cum_est` at `n_adm`) | **225.3** (prod 120.9 + mid_move 104.4) |
| per-unit overhead | **73.2** (6.08 a unit) | **38.5** (dawn_move 15.0 + dawn_pass 11.4 + PICKUP 12.0) |
| **day total** | **234.4** | **263.8** worked, of **250.9** unit-turns |
| per admitted task | **2.86** | **4.00** |

**Ratio est/realised per admitted task = 0.716** — the task half of the model
**under**-charges (`EST_MOVES = 1` against 1.85 realised inter-tile moves a
task) while the per-unit half **over**-charges by nearly 2× (6.08 charged
against a realised 3.20 a unit-day: walk-out 1.25, dawn wait 0.95, pickup
1.00). The two errors do not cancel, and the residue is visible in the day:

* `n_tasks` **59.1**, `n_adm0` **58.1**, `n_adm` after the repair **56.3** —
  the loop drops **1.8** tiles a day it admitted and the route could not reach;
* **50.9 %** of d20-29 days are **budget-bound** (`n_adm < n_tasks`), and on
  **every one of them** the crew still ends the day with tail idle: mean slack
  **19.0 steps a day** (1.37 a unit-day), 16.0 averaged over all days.

**Budget-bound AND slack on the same day is the mis-calibration** — 50.9 % of
d20-29 days decline a ranked task for want of a step budget the route then does
not spend.

## 4. Ceiling — spot on the landing day, our impact ON, nothing past d29

`S/admitslack/report.py`. The declined ranks (`n_adm..n_tasks`) are packed into
each unit's own realised tail slack at their own estimate **corrected by the
measured ratio**, their chain ops become extra PROD ops of our own d20-29 mix,
and the units are sold by walking the engine's `price(inv)` curve down from the
quote we realised (SPREAD6), seed charged on the PLANT share (FEEDFIRE: nothing
past d29). Our purse only.

| correction applied to the declined task's own estimate | ceiling / board | ops / game |
|---|---:|---:|
| none (est as written) | +1,036 ± 143 (t 7.23) | +21.2 |
| **× 1.40 — the measured est→realised ratio** | **+669 ± 105 (t 6.35)** | **+13.2** |
| × 1.86 (task steps priced at the full realised move rate) | +395 ± 64 (t 6.15) | +8.3 |

At the measured calibration the ceiling clears the +450 bar, which is why the
switch was built. It is an average-product ceiling and generous by
construction.

## 5. The switch — `ADMIT_SLACK_ON` (default OFF)

`src/kagg3/core/plan.py:213-251` (constants) and `:9327-9334` (the one
expression):

```python
if ADMIT_SLACK_ON:
    labour = labour + n_units * ADMIT_SLACK_TURNS      # ADMIT_SLACK_TURNS = 1
```

One turn a unit handed back to the admit stage — the measured tail idle
(1.37 steps a unit-day), not the 2.9-step over-charge, so the day is never
admitted against work it has no room for. It is the **safe** direction by the
module's own doctrine (`plan.py:231`): over-admission is exactly what
`ADMIT_ROUNDS` exists to repair — each round drops the tiles the exact route
could not reach, from the **value** tail — while an under-admission has no
repair at all. The repair loop is untouched, the expression is shape-static and
traces under `jit`, and the hire enumeration's `turns_h` is deliberately **not**
given the turn (`ADMIT_PICK_SHARED`'s reason: the crew size stays where the
champion put it, so this is a test of the idle turns alone).

`tests/test_admitslack.py` — **8 pass**: whole-plan sha256 OFF-identity against
a pristine `git archive 0e66a6e src` subprocess (`tests/_pin.py`), the base tree
named and asserted to have no such switch, `ADMIT_SLACK_TURNS = 0` identical to
the shipped plan, `n_admit` rises on a fixed budget-bound state and is still
capped at `n_tasks`, a task-bound day cannot move, the first `_routes` round of
a loaded board is handed a larger admitted set end to end, and the branch traces
under `jit`.

## 6. The gate

| read | FT2 (control) | `ADMIT_SLACK_ON` | Δ |
|---|---:|---:|---:|
| ENG22 seed A margin/board | −763 | −437 | **+326 (sd 931, t +1.64)** |
| ENG22 seed B margin/board | −847 | −458 | **+388 (sd 920, t +1.98)** |
| **ENG22 pooled (44 board-reads)** | — | — | **+357 (se 138, t +2.59)** |
| ENG22 pooled per game (88) | — | — | +357 (se 97, **t +3.67**) |
| our purse / their purse (per game) | — | — | **+162 (t +3.35) / −195 (t −3.34)** |
| board win | 40.9 / 45.5 % | 45.5 / 50.0 % | flips +2/−0, 23/44 boards up |
| **V45LEG margin/board (30)** | 4,682 | 4,637 | **−44 (sd 1,387, t −0.18)**, win 70.0 → 66.7 %, flips +0/−1 |

Instrumented ON vs OFF on the same 22 boards, our seat, d20-29 (`raw` vs
`raw_on`):

| per planning day | OFF | ON | Δ |
|---|---:|---:|---:|
| `n_tasks` | 59.11 | 59.58 | +0.47 |
| `n_adm0` (admitted at the budget) | 58.14 | **59.31** | **+1.17** |
| `ADMIT_ROUNDS` repair drop | 1.80 | **2.60** | +0.80 |
| `n_adm` routed | 56.34 | 56.72 | +0.38 |
| PROD ops | 120.89 | **121.81** | **+0.92 (+9.2/game)** |
| tail idle steps | 16.02 | 15.82 | −0.20 |
| prod ops / unit-day | 10.05 | 10.09 | +0.04 |
| tail idle / unit-day | 1.332 | 1.311 | −0.021 |

So the switch converts a **fifth** of its extra admission into ops, and the
+357 a board it is worth is bought by **9 ops a game** — a coin-per-op far above
the 52 the ceiling priced, which says the ops it adds are the ones at the top of
the declined tail (the value order's own next ranks), not average ones. The
other seat losing 195 a game says the same thing from the other side: the extra
work is sold into the shared pot.

## 7. Files

`S/admitslack/{probe.py,report.py,run_all.sh,report_off.txt,report_on.txt,gate.txt}`
(raws `S/admitslack/raw*/`, not committed), code `src/kagg3/core/plan.py`
(default OFF), `tests/test_admitslack.py`, legs `S/lossflip/{admitslack,ft2s2,admitslacks2}_eng22.csv` and
`S/lossflip/admitslack_v45.csv`.

```bash   # $FT2 = the shipped switch string, spelled out in S/lossmap2/run_all.sh
WORKERS=3 bash S/admitslack/run_all.sh instrument            # 22 boards, ~4 min
.venv/bin/python S/admitslack/report.py                      # calibration + ceiling
RATIO=1.4 .venv/bin/python S/admitslack/report.py            # the corrected ceiling
.venv/bin/python -m pytest -q tests/test_admitslack.py       # 8 tests, OFF identity
WORKERS=3 bash S/judge7065/run_eng22.sh admitslack artifacts/kagg2_games/thetas/\
flow193_g100_hr.npy /mnt/e/_work/kaggriculture3-admitslack "$FT2,ADMIT_SLACK_ON=True"
.venv/bin/python S/nexthigh/pair.py S/lossflip/ft2_eng22.csv S/lossflip/admitslack_eng22.csv
OUT=S/admitslack/raw_on WORKERS=3 bash S/admitslack/run_all.sh instrument \
  "$FT2,ADMIT_SLACK_ON=True" on                              # the ON re-instrument
```
