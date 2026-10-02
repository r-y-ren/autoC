# CARETIMING — the "is today the best day" question, asked of CARE and HARVEST

2026-09-16 17:50–18:30Z, branch `caretiming` off master `463ee05`. Follow-up to
`2026-09-16-fertengine.md`, whose §5 left the same question open for CARE and
HARVEST. Judged on top of the FT2 pair (`LOT4_ON,LOT4_TURN=17,
SELL_SLOT_PRIORITY_ON,FERT_TIMING_ON,FERT_TIMING_DAYS=2`).

## 1. VERDICT — **STOP at Q1. Nothing built, nothing judged. Family CLOSED.**

FERTILIZER was the one place our planner was worse than both opponent classes.
**CARE and HARVEST are the opposite: we are already better than both**, and our
residual loss is not day-choice, so no look-ahead gate can reach it.

| best-day hit rate, per game | ENG22 US | ENG22 THEM | V45 US | V45 THEM |
|---|---:|---:|---:|---:|
| CARE paid / CARE ops | **93.7 %** | 85.9 % | **94.8 %** | 75.7 % |
| one-time HARVEST at max yield | **51.1 %** | 32.8 % | **50.1 %** | 10.1 % |
| one-time HARVEST at saturation day | **82.9 %** | 56.6 % | **83.4 %** | 46.9 % |
| ongoing fires not clamped | 100.0 % | 99.9 % | 100.0 % | 100.0 % |
| (fertilizer, for contrast — FERTENGINE) | 29 % | **91 %** | 27 % | **79 %** |

**Gate-shaped ceiling, our purse: 6 coins/board on ENG22 and 0 on V45.** Bar is
+450 on both. Raw "value of lost units" is larger (CARE 2,040 / 1,791; HARVEST
1,325 / 1,013) but decomposes into buckets a deferral gate cannot touch — §2.

## 2. Q1 — the instrument and the ceiling, two-purse

`S/caretiming/probe.py` on the same 22 ENG22 + 5 V45 boards, both seats, real
engine, FT2 switches. It rebuilds each day's PRE-REFRESH state
(`steps[d*24+22].observation` patched with the turn-23 unit ops, since
`steps[t].action` applies to `steps[t-1].observation`) and replays the engine's
own refresh per tile, so every unit below is the engine's arithmetic. Rules that
define "best day" (`.venv/.../kaggriculture/kaggriculture.py`):

* **CARE** `:524-530` sets `cared_today`; `:829-830` the bank grows by 1 only
  when `cared_today AND fed_today`; `:826-828` a fire pops the WHOLE bank but
  only on a fed day, clamps to `min(max_held, yield+1+bonus)` `:827`, then
  **unconditionally zeroes the bank** `:828`.
* **HARVEST** `:446-470` takes all held units; a one-time tile is destroyed.
  `:431-443` an in-window watering adds 2 covered / 1 not, clamped to
  `max_yield`; `:800` the same per ongoing fire; `:752-766` a one-time tile past
  `max_lifespan_step` loses a unit every 2 steps; `:783` two unwatered days
  weed a tile, standing yield included.

| our purse, coins/board | ENG22 | V45 | reachable by a deferral gate? |
|---|---:|---:|---|
| CARE bank destroyed at an UNFED fire | 1,660 | 1,524 | **no** — §2.1 |
| CARE bank orphaned (animal/game ends) | 360 | 267 | no — `h_next <= pay_day()` already gates it; residual is escapes |
| CARE bank clipped at `max_held` | 11 | 0 | nil — `care_headroom` already gates it |
| CARE without a feed (never banks) | 8 | 0 | nil — `want_care = want_feed & care_ok` |
| one-time HARVEST early, **avoidable** | **6** | **0** | yes, and it is already zero |
| one-time HARVEST early, deadline-forced | 610 | 609 | **no** — deferring forfeits the crop |
| one-time tile DECAYED before harvest | 709 | 403 | no — labour, §2.2 |
| ongoing-fire clamp / animal clamp | 0 / 0 | 0 / 0 | nil |

Their purse: ENG22 CARE 5,331 / HARVEST 4,991; V45 CARE 8,322 / HARVEST 6,244 —
**the opponent classes leave 2.6–6.2× more here than we do**, the mirror of the
fertilizer read.

### 2.1 Why the 1,660 is not a CARE-day number

A care taken on day `D` always pays at the **same** fire — the first one
strictly after `D` (`valuation.next_fire_after`, plan.py:7443, which is
byte-exact against `:826-830`). Every day between two fires therefore buys
**identically**; the "is today better than tomorrow" comparison is a TIE on
every day, so a FERT_TIMING-shaped gate can never fire. What destroys the 15.4
(ENG22) / 14.2 (V45) cares a game is that the *fire* arrives **unfed** — 22.2
of 164 fires a game — which is a FEED-coverage decision, already priced exactly
by `bank_feed` (plan.py:7424) and `bank_val` (:7488) and bounded by the wheat
budget; the day histogram agrees, days 17–29 with day 29 the largest bucket.
And there is no room to move a care to anyway: **397.8 animal-days a game, 312.2
fed, 283.9 cared — only 28.3 fed-but-uncared days exist**, and moving a care
inside its own inter-fire interval changes nothing.

### 2.2 Why the HARVEST buckets are not day-choice either

Of our 23.5 (ENG22) / 23.0 (V45) early one-time harvests a game, **8.7 / 8.2 are
deadline-forced** (`planted_day + max_yield_day > pay_day() = 29`) and **the
avoidable loss is 0.1 / 0.0 units a game** — the mask is already exactly right.
Every early harvest a gate could legally defer is on day 29, where deferring
forfeits the units outright, so `HARVEST_TIMING_ON` would be strictly
**negative**. DECAY (7.1 / 4.4 units, days 21–28) is a unit-turn shortfall on
tiles the mask *already* wants harvested, and a deferral gate only removes ops.

## 3. Q2 — the mechanism (worktree `463ee05`), for the record

* `harvest_age = clip(VAL.pay_day() - t_day, c_first, c_sat)` plan.py:**7356** —
  already the saturation day unless the deadline binds. `harvest_one` :**7381**.
* `harvest_ong = is_plant & (c_ongoing==1) & (t_yield>0) & (age>=c_first)`
  :**7382**; `want_harv_animal = has_animal & (t_yield>0)` :**7521** — both
  "take it the moment there is anything"; measured clamp loss 0.
* `h_next = VAL.next_fire_after(...)` :**7443**; `bank_carry` :**7444**;
  `care_headroom = bank_carry + 2 <= an_held` :**7445**; `care_ok` :**7465**
  (`t_cared==0`, `h_next <= pay_day()`, headroom, `care_pays`, `survival_pays`);
  `care_val` :**7511** → `feed_value` :**7512** → `feed_pass` :**7518**;
  `want_care = want_feed & care_ok` :**8028**; `v_care` :**8282**.
* The quantity a one-line gate would compare — `price[an_prod]` at `h_next` for
  CARE, `crop_remaining_value(..., day+k, harvest_age)` for HARVEST — is
  **constant in `k`** in both cases by construction, which is precisely why
  FERT_TIMING had a gap here and these two do not: `fert_marginal_value` varies
  with the day, these do not.

## 4. Q3 — not built

Stop bar met at Q1 (6 and 0 against +450): no `CARE_TIMING_ON` /
`HARVEST_TIMING_ON`, no `tests/test_caretiming.py`, no legs, and the FT2 control
re-run was not spent. **plan.py is untouched on this branch** — the 7,428-int
layout is undisturbed while `flow220_sw` trains.

## 5. Dead ends / standing

* **CARE day-choice and HARVEST day-choice are CLOSED**, on the mechanism and
  not just on a leg: the payoff of both is day-invariant inside the window a
  gate could move them in.
* **CORRECTED premise:** FERTENGINE §5 read the CARE bonus as day-sensitive
  because it is consumed on a fed production day. It is — but it is *banked*
  the same from any day in the interval, so the sensitivity is to the FEED at
  the fire, not to the CARE.
* **The one live descendant is a FEED lever**: 22.2 of 164 fires a game go
  unfed and burn 0.69 banked cares each. That is the wheat budget's call
  (`feed_pass`, `feed_price` off `buy_q[I_WHEAT]`); it belongs in a FEED box
  with its own bar, not here.
* `S/caretiming/`: `run_all.sh` (`instrument` | `ctl` | `eng22` | `v45` |
  `pool`), `probe.py`, `report.py`, `ledger_eng22.txt`, `ledger_v45.txt`,
  `raw/` (27 board json). Reproduce with
  `WORKERS=3 bash S/caretiming/run_all.sh instrument`.
