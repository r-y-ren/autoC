# RIVAL_TELL — the measured rival sale rate inside SLOTPRIO's batch term: built, parity-clean, worth 0

2026-09-16, 09:49–10:35Z. Worktree `/mnt/e/_work/kaggriculture3-rivaltell`, branch
`rivaltell` off `ee8dedd`. Tools `S/rivaltell2/`, leg csvs `S/lossflip/rivaltell_*`.
Builds `docs/strategy/2026-09-16-rivaltell.md` sect.7 (the spec) on top of
`2026-09-16-slotprio.md` sect.6 item 1 (the thing that "could move +394").

## 0. VERDICT

**DEAD — the increment is zero and its sign is negative.** Judge leg 1 (0-coin parity)
passes exactly; leg 2's kill rule (≥ +100 and t ≥ 2) fails by the whole distance on two
engine populations, so BAND180 was run once for the record and POOLED180 was not run at all.

| leg | games | ON − CTL (the increment) | t | flips | rows identical |
|---|---:|---:|---:|---:|---:|
| ENG22 | 44 | **−0.0** | −0.10 | +3 / −2 | 39 / 44 |
| V45LEG | 60 | **−2.1** | −3.47 | +0 / −12 | 48 / 60 |
| BAND180 | 158 | **−18.5** | −4.26 | +10 / −48 | 100 / 158 |

The arm is not noisy, it is **absent**: 63-89 % of games are the same coin row, and where
it does bite it bites the wrong way — on BAND180, the leg that carries the promotion
statistic, it is **significantly negative** (−18.5, t −4.26, 48 boards down against 10 up). §115b is not applicable to an increment this size; the
total (SLOTPRIO + RIVAL_TELL vs B) is SLOTPRIO's own read minus a couple of coins.

## 1. Why it cannot move, measured before the first leg

The spec's batch is `clip(mean rival units sold per TURN over the last 6 turns, 8, 24)`,
gated to items sold on ≥ 2 of those 6 turns. On the 50 banked real-engine streams
(`S/rivaltell/data`, the same V45LEG/BAND180 boards the legs play), replayed through the
**production** estimator:

| quantity | value |
|---|---|
| items gated per dawn (of 7 eligible) | **0.212**, max 3 |
| dawns that gate nothing at all | **81.4 %** |
| gated batch values at the floor (≤ 8) | **100.0 %** (raw rate mean **1.83**, max 6) |

A rival sells an item on ~5 % of turns and in bursts: 30 wool on one turn of six is 5
units a *turn*, and `BATCH_MIN = 8` swallows it. So the tell can only ever **lower** a
product's batch to the floor — i.e. move the item the rival demonstrably sells **to the
back** of our SELL row — and it can only do that to one item every five days.
`slotprio` sect.5 had already shown the batch clamp is flat (±2x on both ends moves ENG22
/ V45LEG by at most −33 coins and never up); this is the same flatness seen from the other
side, and the V45LEG sign (−2.1, 12 of 12 touched games negative) is exactly the demotion.

## 2. What was built (default OFF, requires `SELL_SLOT_PRIORITY_ON`)

| piece | file:line |
|---|---|
| estimator, re-derived from the engine (nothing imported from `S/`) | `src/kagg3/agent/tell.py` |
| doc block + the five switches | `src/kagg3/core/plan.py:4060-4097` |
| `sell_slot_scores(..., opp_rate=None)` — `where(rate >= 0, rate, opp_ripe)` | `plan.py:4100-4125` |
| `DayView.opp_rate`, default all-`-1` sentinel | `plan.py:4909` |
| caller: `view.opp_rate if RIVAL_TELL_ON else None` | `plan.py:8744` |
| `parse_view(obs, player, opp_rate=None)` | `agent/parse.py:80,97` |
| per-turn state + rotation beside the `OPEN_PUMP_TELL_KEEP0` hook | `agent/runtime.py:36,58-70,88` |
| tests (9) | `tests/test_rivaltell.py` |
| leg runner | `S/rivaltell2/run_legs.sh`, scorer `S/rivaltell2/score.py` |

`RivalTell` keeps one `int32[6,9]` ring per seat. Each turn `observe(step, inv, shops)`
closes the **previous** step with the pot this one opens on —
`riv_net(t) = inv[t+1] − inv[t] + town(t) − our_sell(t) + our_buy(t)` — and
`record_orders` files the row we are about to present, because the observation carries no
fill report. A gap in the stream drops the history rather than pricing a delta across it.
The rate is read at hour 0 and handed to `build_day` through the view, so the window a
plan sees is the previous day's last six turns; the three SELL rows of the day are then
planned against it. Below a full window (days 0-1), after a gap, or on any item the gate
does not fire on, the field stays `-1` and `sell_slot_scores` keeps the `opp_ripe` proxy.

WHEAT and FERTILIZER are never gated (`RIVAL_TELL_SKIP`): the estimator is a **net** and
those two are the only items a rival trades both ways in one turn.

The production estimator reproduces the instrument, unit for unit — 50 real games, the 7
gated items, our own side taken from the **orders** we presented:
**exact net cells 0.9980, precision 1.0000, recall 0.9853** (tp 7,098 / fp 0 / fn 106).

**The simulator keeps the proxy.** `sim/rollout.day_view` has no per-turn pot history to
rotate (the day scan carries only the dawn inventory, and the rival there is a twin
planned at the same dawn), so a sim seat's `opp_rate` is the sentinel and an ON sim run
IS the SLOTPRIO run. That is why the kill gate here is the cheapest **engine** leg
(ENG22, 44 games, 2.5 min) and not `S/simscreen` — the screen is structurally blind to
this switch, which is a property of the switch, not a shortcut.

## 3. Parity — judge leg 1, exactly 0 coins

* `tests/test_rivaltell.py` — 9 tests, all pass, plus `tests/test_slotprio.py`'s 10:
  * `test_off_plan_is_byte_identical_to_head` — ten whole-plan sha256 digests (five boards
    × held/zero reservation) against a pristine `git archive HEAD src` tree in a
    subprocess. **Equal.**
  * `test_the_sentinel_is_the_slotprio_plan` — armed, measurement at the sentinel, the
    five ON boards digest-equal to `SELL_SLOT_PRIORITY_ON` alone.
  * `test_the_measured_rate_replaces_the_proxy_per_item`,
    `test_a_fired_item_reorders_the_row_against_the_proxy` — the rank does move when a
    rate fires (MILK ahead of the rival's standing STRAWBERRY).
  * three estimator tests on a synthetic observation stream built from the engine
    identity: recovery beside our own trades with every shop unlocked, the 2-of-6 gate and
    the short window, and a gap dropping the history.
* On the engine, `RIVAL_TELL_ON=True,RIVAL_TELL_FORCE_PROXY=True` (`arm par`) is
  **coin-for-coin identical to `arm ctl` on 44 / 44 ENG22 games**, and `arm ctl` is
  identical to the banked `slotprio_on_eng22.csv` on 44 / 44 — so this tree's SLOTPRIO
  program is the one that posted +394, and the armed seat only differs where the
  measurement fires.

Pre-existing failure, unrelated and present on pristine HEAD:
`tests/test_open_pump.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner`.

## 4. The numbers

`S/rivaltell2/run_legs.sh <ctl|par|on> <eng22|v45|band180|pool>`, both arms from this
worktree, theta `flow193_g100_hr`, shipped switch string + `SELL_SLOT_PRIORITY_ON`.
Paired per **game** (board × seat), Δmargin = (mine − theirs).

| leg | games | CTL − B | t | ON − B | t | **ON − CTL** | t |
|---|---:|---:|---:|---:|---:|---:|---:|
| ENG22 | 44 | +445.8 | +4.46 | +445.7 | +4.45 | **−0.0** | −0.10 |
| V45LEG | 60 | +457.1 | +5.55 | +455.0 | +5.52 | **−2.1** | −3.47 |
| BAND180 | 158 | +428.1 | +5.03 | +409.5 | +4.78 | **−18.5** | −4.26 |

POOLED180 (the §115b statistic) was **not run**: the promotion bar is +450 on the total and
the increment over an already-shipped-OFF SLOTPRIO is −2 coins, so there is nothing to
promote and nothing to fit.

## 5. What this closes

1. **`slotprio` sect.6 item 1 is answered and negative.** "A better rival read than
   standing ripe yield" was the named candidate for the missing 56 coins. The read is
   perfect (precision 1.000) and worth **nothing**, because the quantity the score needs is
   *how much the rival can put in the pot in one slot round* — a burst — and a per-turn
   average of a bursty seller is always below the floor the clamp already applies.
2. The batch term of `sell_slot_scores` is now **closed from both ends**: re-sizing the
   clamp is flat (slotprio sect.5.2) and re-sourcing it from the measurement is flat
   (here). Any further coins in the sell-row family have to come from a different term —
   the rows we do not have (`spread6`, closed), a fourth block to rank, or the two thirds
   that half (a) already carries.
3. `agent/tell.py` survives the arm as a **free, exact, per-turn rival instrument** the
   tree did not have (sect.2 numbers). The next user of it should read a *burst* —
   e.g. units per SELLING turn, or the rival's largest single-turn row in the window —
   not a rate, and should feed something that is not already clamped at 8.
