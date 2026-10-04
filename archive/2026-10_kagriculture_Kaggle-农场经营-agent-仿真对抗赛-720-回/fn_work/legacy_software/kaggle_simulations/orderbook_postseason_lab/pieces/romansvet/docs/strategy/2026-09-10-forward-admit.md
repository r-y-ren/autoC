# FORWARD_ADMIT: hire against the work that is coming (2026-09-10)

## The gap

1.5 scores a hand against the work the board has **this morning**. Twelve melon
planted on day 0 have none (`CROP_WINDOW_START[MELON]` 6, `CROP_SATURATE_AGE`
10), so on days 1-5 `n_tasks0` is 0, every candidate's gain is `-HIRE_BILLS[h]`,
and the crew that must stand on day 10 is never hired — the 94 % -> 26 % of
`2026-09-09-forced-opening-ramp.md`.

## PRIOR ART — already implemented, already closed

Found while wiring the probe, and it dominates the rest. `arms-next` (45f8217)
**already carries `FORWARD_ADMIT_ON` / `FORWARD_ADMIT_DAYS`** (plan.py:3537) for
this exact reason, plus a trained horizon gene `g11`/`gb11`
(`macro.forward_days`), on by default. The hand override was measured on the
pinned judge and failed: HELD42 **-8,676** (t -12.11, +0/-10), LEG20 **-6,361**
(t -5.75), LOSS12 **-8,178** (t -8.98) — `2026-09-09-switch-sweep.md` rows
46/79/172; band6 hand probe 94.4 -> 65.3 %. Recorded verdict: *"the forward
horizon belongs to theta; do not override it."* Its diagnosis is
**double-counting**: it widens the water window and harvest age for *every*
tile, so a theta whose `hire_bias` and crew ramp are priced for today-only
admission pays twice.

## What this branch adds

A narrower shape aimed at that defect (`FORWARD_ADMIT_ON=False`,
`FORWARD_ADMIT_H=6`, both inert):

* **Quiet tiles only.** A tile with an op today keeps today's `n_ops` and
  `tile_value` untouched — the projection can only *add* a silent tile, so
  nothing already visible is re-priced.
* **Discounted, not flat.** A quiet tile first needing a hand on `day + k` is
  entered as one op worth `VAL.crop_remaining_value` (or `animal_value`)
  **divided by `1 + k`**, so the crew ramps into the maturity.
* Counts one-time crops' in-window waterings and `harvest_age` harvest,
  `crop_fires_on` for ongoing crops, `fires_on` for animals; clamped to
  `pay_day()`. Purchases, plantings and replants excluded — standing tiles only.

**Hook** (`_plan_and_stats`): the three inputs to the hire argmax, nothing else.
`_pickup_kinds`, `pre_early0`, `pack_orders0` and pass B read the unprojected
Prefix, so routes, admission and every purchase are unchanged.

## Unit test (`tests/test_forward_admit.py`, 6 pass)

`n` day-0 melon, all other tiles LOCKED, day 1, `tasks_today = 0`:

| board | OFF | ON |
|---|---|---|
| 12 melon (d1/3/5) | 0 | 1 |
| 60 melon (d1/3/5) | 0 | 7 |
| 60 melon, `H=3` (wait 5 > H) | 0 | 0 |
| 60 melon d10, all busy | 7 | 7 |

Twelve tiles are 24 estimated turns, so one hand covers them: the switch
restores a *reason* to hire, not a crew. Knob off: **76/76 pass** across
`test_plan*`, `test_hire_enumeration`, `test_hire_bill`, `test_crew_ramp`,
`test_genome_retype`, `test_admit_route`.

## Sim (CRN, 61 pinned-town tapes, both seats)

Theta `flow135_g350_gpfwdfv_gb028` (the probe default — it has a cached base;
`flow172_g60` had none and three fresh legs did not fit the box), patch ported
to a tree at 45f8217 as `FWD_PROJ_ON` because `fitness-shaping` predates the
pinned-town tape support the probe needs. Arm = knob on vs same theta, off:

| set | n | d-margin | SE | t | win (base) | flips |
|---|---|---|---|---|---|---|
| HELD42 | 84 | **-2,628** | 330 | **-7.97** | 19.0 % (21.4 %) | +0 / -2 |
| LEG20 | 20 | **-1,456** | 519 | **-2.81** | 70.0 % (70.0 %) | +0 / -0 |
| LOSS12 | 24 | **-6,403** | 1,155 | **-5.54** | 0.0 % (25.0 %) | +0 / -6 |
| ALL | 122 | -3,160 | | | | 0 % identical |

Arm (b) (`+ MELON_OPEN_ON`) was launched and killed at 17 min when the box ran
out; not reported.

Third signal: `g11` on this theta decodes to **`forward_days = 0` every day** —
given a free forward-admit gene the ES set it to zero, and put `crew_target` at
11 by day 10 instead. The ramp already buys the hands.

## Verdict

**DEAD.** Every set negative, |t| 2.8-8.0, zero boards flipped up, 6/12 LOSS12
flipped down, no board identical. Third independent read against the family
(existing switch -8,676; ES gene at zero; this shape -2,628). The
quiet-tiles-only + discount design cuts the damage ~2/3, supporting the
double-counting diagnosis, but does not change the sign. **Not ready for an
engine read on LOSS20 — do not promote.** Committed inert so the shape is on
the record; treat the family as closed absent a mechanism that is not "hire
earlier".
