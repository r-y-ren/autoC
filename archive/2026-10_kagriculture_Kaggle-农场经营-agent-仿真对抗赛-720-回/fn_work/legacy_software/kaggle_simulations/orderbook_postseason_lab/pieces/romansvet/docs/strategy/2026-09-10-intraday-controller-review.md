# Review: "add a small intraday market controller" (2026-09-10)

Read-only review of a proposal to let the agent revise market decisions during
the day. Branch `fitness-shaping`. Nothing was run, nothing was changed.

## 1. Claim by claim

| # | claim | verdict | evidence |
|---|---|---|---|
| 1 | the runtime builds the whole day's plan at hour 0 and replays it | **TRUE** | `src/kagg3/agent/runtime.py:30-34` rebuilds only when `hour == 0` / the day changes; `src/kagg3/agent/render.py:52-60` renders from the cached arrays plus `n_hands` and reads no obs |
| 2 | apart from a narrow opening exception it cannot revise market decisions | **TRUE, and narrower than stated** | the sole intraday patch is `runtime.py:42-44` (`open_pump_tell_keep0`, hour-1 wheat pot). Its switch `OPEN_PUMP_TELL_KEEP0_ON` is **False** (`core/plan.py:1276`), so the *shipped* build makes zero intraday market revisions |
| 3 | it cannot react to a failed purchase | **TRUE but empty** | no refusal path exists; and instrumented on 24/42 held-out boards our orders are refused 3.96x/game = 0.07 % of 5,666 acting turns, 0 of 1,971 BUY rows, 0 HIRE/LAND/PLACE/DROP/PICKUP refusals (`2026-09-09-plateau-review-verdicts.md` §2). A re-plan-on-refusal hook has nothing to react to |
| 4 | a controller could use "actual inventory" mid-day | **FALSE** | a sale draws on the *shed*, and the day's harvest reaches the shed only at end of day (`plan.py:6457-6460`; `sim/eod.py:181 drop_inventories`). Mid-day inventory sits on the unit and cannot be sold without a purpose-built excursion |
| 5 | feed reservations / expected deposits are new information | **FALSE** | both are already priced at hour 0: feed wheat and the day's fertilizer are subtracted from `avail` (`plan.py:6461-6472`), the forced-overflow pass projects tonight's shed (`plan.py:6499-6510`) |
| 6 | production-timing features exist in the latest package | **TRUE for the shipped 6789 layout, FALSE on this branch** | `arms-next:src/kagg3/core/policy.py:379 (fh/fs), :416 (gp), :424 (g11), :439 (fv)`, jointly retrained flow146-157 (§3 of the plateau review). Every candidate theta is 6789 (`flow172_g300.npy`); this branch is `N_PARAMS = 4980` and its `brain.py` has no forecast block. They are hour-0 inputs, not intraday observation |
| 7 | "the next experiment should test whether the agent can act on new information during the day" | **ALREADY TESTED — CLOSED** | `2026-09-09-plateau-review-verdicts.md` §2 is verbatim this proposal: "Let it revise market decisions during the day — NOT binding (CLOSED)" |

## 2. Where a controller would have to hook

Sale rows are decided once, in `build_day`: `SELL.allocate` (`core/sell.py:100`)
called at `plan.py:6494-6496` with `hold`/`press` decoded from theta
(`brain.decide`), `avail` = hour-0 shed net of reservations, and lot curves
projected on `early_lot_turns()` (`plan.py:2523`). Rows are emitted by
`_market` (`plan.py:7559`). So "adjust sale timing and quantity" = re-entering
`allocate` per turn, or patching `mkt_q` the way `open_pump_tell_keep0`
(`plan.py:1703-1736`) does.

Determinism is not the obstacle: the packager vendors `core/*.py` + `theta.npy`
verbatim (`scripts/package_submission.py:40-49, 219`) and the numpy path is
already the reference. The costs are (a) per-turn planner cost, which the
hour-0 cache exists to avoid (`runtime.py:3-7`), and (b) the ES harness, which
scans a day at a time.

## 3. Prior evidence

Won, and both are **schedules, not reactions**: `EARLY_SELL` mode A, the turn-1
lot, +2,184 (t 5.1), shipped (`plan.py:2463`); the tail pair `TAIL_FILL_ON` +
`BANK_BEFORE_LOT_ON`, engine H_dm +801, LEG20 +1,403 (§32) — still `False` here
(`plan.py:1858`, `:2589`), promoted on the `drain-pair` tree.

Lost, paired, real engine: `SAME_DAY_FERT` -29,560 (t -25.12, +0/-16);
`MIDDAY_DROP` -4,311 (t -10.29); `MIDDAY_PLACE_V2` -101; `MELON_OPEN` +
`MIDDAY_PLACE_V2` band -18,561 (t -11.3); `OPP_SUPPLY` -2,972/-3,616;
COLLECT_DAY_SELL +100 no flip; COLLECT_DROP +16/-5 pinned but -1,441 drawn —
route displacement (`2026-09-05-build-story.md:959`); sell-hour cadence 6 rows
-324 / 4 rows -348, and §52 (`2026-09-10-sell-hour-headroom.md`) finds **zero**
headroom under g60 — the turn-1 sale itself is now worth -77. Losses carry the
two-purse signature (`2026-09-08-how-we-built-the-agent.md:70-72`): displacement
of our own better work, or denial handed back.

Standing: the ES lineage is the only thing that has moved the live read —
flow172_g300+pair LIVE55 34.5 -> 70.9 %, +6,753 (t 9.95), 47/53
(`2026-09-10-upload-dossier.md:118`; 79.1 % on the clean 43-board line). (The
"83-89 %" figure in the proposal does not appear in the archive.) All hand
planner lever families are recorded closed.

## 4. Recommendation

**Do not run it as stated.** Its premise is either implemented (hour-0 pricing
of inventory, reservations, deposits, production timing) or refuted (§2 of the
plateau review, plus eleven paired engine losses on same-day/mid-day market
levers). The one fact it names that is real — the once-per-day restriction — is
not binding, because the information it would unlock does not exist mid-day.

**Smallest honest version, if the premise must be tested at all** (~1 sim screen
+ 1 leg, no new code): flip `OPEN_PUMP_TELL_KEEP0_ON` to `True`
(`plan.py:1276`). It is the only intraday read already built, still unmeasured
in the engine, one constant, and it is literally "act on new information during
the day" — the hour-1 pot says whether the other seat pumped.

**Second candidate, and not intraday:** the only defect the instrumented run
found is d21-29 SELL rows short ~19 units/game (liquidation sizing, §2). Fix it
inside `build_day`; it needs no runtime change.

**Judge either must pass:** LIVE55 on the 53 byte-exact held-out pinned live
boards — d-margin > 0, seat-grouped |t| >= 2, >= 28/53 positive
(`2026-09-09-judge-live55.md`); drawn legs are a veto only.
