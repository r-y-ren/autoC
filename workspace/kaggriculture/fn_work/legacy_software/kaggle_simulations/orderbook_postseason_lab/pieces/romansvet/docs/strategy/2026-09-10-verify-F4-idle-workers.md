# Verify — planner finding 4, "Forecast work can purchase idle temporary workers"

Independent verification, 2026-09-10. Read-only on every worktree `src/`; probes ran in
memory, engine runs from the shipped trees unmodified. Claim source:
`docs/2026-09-10-planner-findings.md` row 4 / `docs/reviews/planner-2026-09-10/REVIEW.md` §5.

Reviewed tree `.claude/worktrees/ship-pair` **verified**: `src/kagg3/core/plan.py`
sha256 `ac731e50…4df32` and `core/brain.py` `4f0ba872…bcfd7` equal
`docs/reviews/planner-2026-09-10/provenance.json` byte for byte. The CURRENT shipped tree
`.claude/worktrees/ship-pair-hr` (sub 56143250, `submission_flow172_g1000_pair_hr`) differs
from it in **exactly one line**: `plan.py:3523 HIRE_ROW_ON = False → True`. Nothing else.

## 1. Mechanism — CONFIRMED, and it is one term

The hire count is an enumerated argmax over `h` (`plan.py:5971-6152`). Two `_derive` passes:

* `plan.py:6000` `d0 = _derive(..., bill 0, reserve 0)` — today's real task set.
* `plan.py:6020-6027` `fwd_days = macro.forward_days` (the `g11` gene; the
  `FORWARD_ADMIT_ON` override is `False` in both trees), then
  `d_sc = _derive(..., rev1=d0.rev1, forward=fwd_days)` — the **projected** pass.
* `plan.py:5006-5027` is what `forward` does: `bonus_water = (age + f >= c_ws)` and
  `harvest_one = (age + f >= harvest_age)` — supersets of the unwidened masks, so the
  projected pass can only carry **more** tasks.
* `plan.py:6028-6031` `n_tasks0 / order0 / cum_est0 / cum_val0` are all built on `d_sc`.
* `plan.py:6108` `n_adm = min(_count_le(cum_est0, turns_h), n_tasks0)` and
  `plan.py:6124` `gain = _cum_take(cum_val0, n_adm) - bills[h] + hire_bias*h + crew_push`.
* `plan.py:6135` `h_star = argmax(scores)`; `plan.py:6142` **pass B re-derives with no
  `forward=` argument at all**, and the route, admission and market row read that `d`.

**The load-bearing term is `cum_val0` (`plan.py:6031`), taken from `d_sc`, scored against
`bills[h]` at `plan.py:6124`, while `_routes` is fed the unwidened `d` from
`plan.py:6142`.** A tile whose WATER/HARVEST lands `f` days out pays for a hand today at
today's fib wage and hands `_routes` nothing, so the hand's whole day is PASS. The gene
ceiling is `brain.py:721 FWD_DAYS_MAX = 6` = `max(spec.CROP_WINDOW_START)` (melon), decoded
at `brain.py:1140-1142` as `clip(_qfloor(16*z + 0.5), 0, 6)`.

## 2. Probe reproduced — exactly, and the trained policy does NOT hire

`docs/reviews/planner-2026-09-10/probe.py`'s `future_hiring` block, re-run on `ship-pair`
(100 melon tiles planted d0, seen d3, purse 10,000, `_macro()` defaults):

| macro | forward_days | HIRE orders | wages | non-PASS unit actions |
|---|---:|---:|---:|---:|
| probe zero-bias | 0 | 0 | 0 | 0 |
| probe zero-bias | 3 | **12** | **376** | **0** |
| probe zero-bias | 6 | 12 | 376 | 0 |
| **`flow172_g1000` decode** | **1** | **0** | **0** | 0 |
| `flow172_g1000`, forced 6 | 6 | 12 | 376 | 0 |
| `flow172_g1000`, `hire_bias=crew_target=0` | 1 | 0 | 0 | 0 |

376 = `sum(spec.HIRE_COST[:12])` (fibonacci 1,1,2,3,5,8,13,21,34,55,89,144). The 12/376/0
row is exact. The horizon threshold is arithmetic, not tuning:
`spec.CROP_WINDOW_START[I_MELON] = 6`, age 3, so `f >= 3` admits and `f <= 2` does not.

**The trained theta decodes `forward_days = 1` on that state and hires zero.** It also
carries `hire_bias = -358`, which is a *brake* on the enumeration, not an accelerator —
zeroing it changes nothing here, so the zero-hire result is the horizon, not the bias.

**On the CURRENT shipped tree (`ship-pair-hr`) every row above emits 0 HIRE orders**,
including the forced-horizon-6 one: `plan.py:6532 HIRE_ROW_ON` clamps the market HIRE row
to the smallest prefix of hands whose route is not all-PASS. The reviewed defect's coin
cost is already switched off in what we ship.

## 3. Incidence — the gap the review left open, now measured

Archive figures confirmed at source: `plan.py:3488-3523` (HIRE_ROW switch docstring) —
"idle hand-days 17.06 to 0.00 exactly, and +889 coins of hire bill … 768 paired games …
−378 a game (se 506, t −0.75, win 61.5 → 61.2 %)". `2026-09-10-forward-horizon-feasibility.md:134`
repeats it. `2026-09-09-plateau-review-verdicts.md` §5: "all-PASS hand-days (15.2/game) are
hands with no ranks left", 180 day-rows / 3 held-out boards.
`2026-09-09-loss6-anatomy.md:48`: PASS share of unit-turns ours 15.4-16.9 % vs top 6.4-9.8 %.
`2026-09-10-chain-optimisation-review.md:24` already ruled the same family TRUE-but-not-money.

New engine measurement (13 games, ~5 engine-minutes; `flow172_g1000`, pinned town
`S/band2100p/town_schedules.json`, LIVE-C tapes 107429978 / 107430502, seed 777001, both
seats — the seats are byte-identical here because the tape is open-loop and the town pinned,
so this is **2 distinct boards**, not 4):

| tree | hires/game | acting/game | **idle hand-days/game** | PASS share | margin/game |
|---|---:|---:|---:|---:|---:|
| `ship-pair` (HIRE_ROW_ON=False) | 278.0 | 267.0 | **11.0** | 17.7 % | +2,334 |
| `ship-pair-hr` (shipped) | 270.0 | 270.0 | **0.00** | 14.7 % | +803 |
| `ship-pair`, `forward_days` forced 0 | 250.5 | 248.0 | **2.5** | 14.4 % | **−7,720** |

Trained gene in play: `forward_days` mean **2.1 days**, positive on **11 of 30** day-rows,
hits the ceiling 6. **8.5 of the 11 idle hand-days a game (~77 %) are caused by the forward
horizon** — that is the incidence the review said it had not measured.

And the price of removing it: forcing `forward_days = 0` costs **−13,037 / −13,676 coins of
our own cash** on the two boards (74,112 → 61,075 and 73,411 → 59,735), flipping both wins
to losses. The idle hands are a rounding error inside a lever worth ~13k a game.

## 4. Verdict

* **Mechanism: CONFIRMED.** Exact, one term, reproduced to the coin (12 hires / 376 / all PASS).
* **Incidence under the trained policy: REAL BUT SMALL** — 11.0 idle hand-days a game on
  278 hires (4.0 %), 8.5 of them from the gene. The review was right to flag that it had not
  measured this and right that the stress state overstates it (the trained decode hires 0 there).
* **The implication is WRONG, and it was already measured twice before today.**
  "Price today's executable work against today's wages" *is* `forward_days = 0`, and it is
  −13.4k a game here. `HIRE_ROW_ON` — the strictly cheaper version, which deletes the idle
  hands and keeps the horizon — is 17.06 → 0.00 idle hand-days for −378 ± 506 over 768 paired
  games. Idle hands are nearly free; the horizon that buys them is not.
* **The campaign's diagnosis is the one the paired evidence supports.** Hands priced on
  TODAY's tasks is exactly why the planner cannot ramp (`plan.py:3530-3536`: forcing the
  top-tier melon opening reads band6 win **94 % → 26 %**, 0 hands d1-5, because melon emits
  no task for 6 days). The review asks to *shorten* the horizon; the archive's forced-opening
  work asks to *lengthen* it. Both endpoints lose — `FORWARD_ADMIT_ON` fixed at 3 reads
  94.4 → 65.3 %, −9,224, t −6.7 (`2026-09-09-verdicts.txt:919`), and 0 reads −13.4k here —
  which is the signature of a **trained interior optimum**, not a defect. The correct reading
  is that `g11` is already doing the job and neither hand-set endpoint beats it.
* **`HIRE_ROW_ON` note:** shipped ON since 56143250 on its own h2h evidence (+453 t 3.6 LIVE62,
  LIVE-C22 +990 t 5.0), not on the idle-hand argument. My 2-board paired read of it is
  **−1,532/game**, same sign as the archive's −378 ± 506 and well inside a 2-board lottery;
  it is not evidence against the shipped switch, and 2 boards cannot settle it either way.

## 5. Residual lever and its exact test

Nothing here is worth a build. If anyone insists on one, the only untried shape is *not*
"price against today's wages" but **a horizon that is charged for the hands it buys** —
e.g. discount `cum_val0`'s projected rungs by `f` days before `plan.py:6124` compares them
to `bills[h]`, leaving `d0`'s rungs undiscounted. It is a one-expression change at
`plan.py:6031`, byte-identical at `fwd_days == 0`.

Exact paired test, in order, from a fresh worktree, base = `g940pair` rows already banked:

```
S/livec/run.sh  <name> <worktree> artifacts/kagg2_games/thetas/flow172_g1000.npy \
    "OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True"
S/topb2/run.sh  <name> <worktree> <same theta> "<same switches>"     # veto
S/live62/run.sh <name> <worktree> <same theta> "<same switches>"     # veto, LIVE55 rule
```

Promotion bar (unchanged): LIVE-C +5 win points with paired `d margin > 0`; TOPB2 and LIVE55
each no worse than −2 win points and no worse than +2/−4 W/L. An identity leg at zero
horizon must be 100 % `=` rows first.

## 6. Dead ends recorded

* `forward_days = 0` (the review's implication, executed exactly): −13.0k / −13.7k own cash,
  both boards flip from win to loss. **CLOSED.**
* `FORWARD_ADMIT_ON = True` fixed at 3 days (the opposite endpoint): 94.4 → 65.3 %, −9,224,
  t −6.7, d-ours −13,157. Already closed 2026-09-09; re-confirmed as the mirror image.
* Deleting idle hand-days without touching the horizon (`HIRE_ROW_ON`): −378 ± 506 over 768
  paired games, i.e. free. Not a lever in either direction.
* Seat-swapping a pinned-town open-loop tape at a fixed seed: **degenerate** — seat 0 and
  seat 1 produced byte-identical own-play and margins on both boards. Any future 2-seat
  count on pinned tapes must vary the seed (`--seed-per-opponent`) or it doubles nothing.
