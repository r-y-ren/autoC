# Review: `CASH_RESERVE_SCALE` (worktree cash-reserve, c04f36b on 45f8217)

Read-only review, 2026-09-10. Verdict: **fit to judge paired as-is.**

## 1. Default identity

The src diff is a `[KNOB]` docstring block plus one guarded branch in
`plan.cash_reserve` (`plan.py:3627`). At 1.0 the `if` is False, so `bill` is the
same `HIRE_BILLS[idx]` gather and no arithmetic is emitted. Verified by
recomputing the pre-knob formula over every `(n_hire 0..17, day 0..30)` pair:
identical in all 558 cells. `pay_day() == 29`, reserve void from there as before.

`pytest test_cash_reserve test_hire_bill test_budget_order -q` from the worktree
(`PYTHONPATH=src JAX_PLATFORMS=cpu`): **28 passed in 191s**, 0 failed
(26 pre-existing + 2 added).

## 2. One derivation site

Defined once (`plan.py:3591`), called from exactly two places, both in the hire
scan: `plan.py:6132` (`afford`: `bills[h] + cash_reserve(...) <= view.money`) and
`plan.py:6142` (pass-B `_derive` reserve arg). Every other `HIRE_BILLS[` hit is
something else — `plan.py:4915` recovers `crew_now`, `5371` `n_units`, `5998` is
the enumeration's bill table; `policy.py:67`,
`brain.py:654/669/1075` and six `es/archetypes.py` hits are prose. `projector.py`
and `budget.py` hold no reserve or hire-bill arithmetic at all — `budget.grant`
receives a purse. Nothing re-derives the floor.

## 3. Judge wrapper reaches it

`S/drainpin/on2b.py` imports `plan`, `setattr`s, then `runpy`s
`eval_vs_baselines.py`. Neither traces at import (no `jax.jit` outside
`es/train.py` and a few scripts) and the engine seat is pure NumPy
(`agent/runtime.py`), so `cash_reserve` reads the module global per call —
trace time never arises in this harness. `conv()` maps `0.5`→float, `0`→int 0
(branch taken), `1`→int 1 (identity). Workers are `ProcessPoolExecutor` under
Python 3.11 `fork`, so the override is inherited. It does take effect.

## 4. Feed / care interaction

Lowering the reserve only *raises* the buy purse (`plan.py:5163`,
`money = view.money - hire_bill - reserve`), so the scale never squeezes feed
directly. The risk is the `afford` gate: at 0.0 a farm may hire the crew its whole
purse pays for and wake on nothing (the 7-coins-on-day-2 replay the docstring
cites); `want_feed` is rationed to `wheat_avail`, so animals can go unfed.
**0.0 is hazardous; 0.5 keeps half the re-fielding floor and is safe to play.**
Second-order: the reserve is what zeroes `land_value` most days, so 0.5 buys more
land too — intended, but the arm is not a pure hire-row test.

## 5. Notes

Nothing snapshots switch values into a package, so a promoted value must be
edited into `plan.py`, as with every other `[SWITCH]`. `xp.round` on float32 is
exact for these bills (max 2583 at `MAX_HANDS = 16`) — 0 mismatches at 0.5.
