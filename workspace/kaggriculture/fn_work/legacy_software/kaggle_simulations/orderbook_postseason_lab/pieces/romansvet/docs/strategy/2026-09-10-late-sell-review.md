# 2026-09-10 — review: `LATE_SELL_FILL_ON` (worktree `late-sell`, b7e2ae4)

Review of b7e2ae4 on `late-sell`, base `arms-next` 45f8217. Line numbers are the
worktree's `plan.py`.

## 1. OFF path — byte-identical

The diff is: two constants; an `if LATE_SELL_FILL_ON:` block at 6641-6657; and a
**move** of the `avail` lines (6658-6662) below `fert_reserved`. Nothing reads `avail`
between the two positions and `fert_reserved` does not read it, so the move is pure
reordering; no other site reads either reservation (6634, 6639, 6652-6662).
**OFF is byte-identical**; the pinned-digest test is the right guard.

Targeted set, `pytest -q` in the worktree: **173 passed, 0 failed, exit 0** —
late_sell_fill 5, sell_allocator 12, sell_side 9, fert_reserved 3, shed_overflow 12,
overflow_forced_sale 18, day29_endgame 9, drop_op 9, early_sell 61, bank_before_lot 8,
tail_fill 10, feed_rationing 6, route_early 11.

## 2. ON mechanism — sound; `blk` really is known at hour 0

The route **is** the plan: `_routes` returns `blk` (7710/7745) and the emitted PICKUP
rows are literally `unit_q = blk[i]` (6621), so "actually picked up" is not a forecast
but the planner's own op quantity. `blk` is final at 6653 (the admit/route loop exits
at 6547); later mutations — `idle` PASS (6623), a pickup turn past the budget — only
make the day pick up *less*. `proj_eod` (6705) and `SHED_OVERFLOW_ON` (6903) already
charge exactly `blk`, so the switch removes a real OFF inconsistency.

Starvation: no. `minimum` never releases below the pickup, and every divergence
(refused HIRE, idle unit, dropped pickup turn) reduces real pickups below `blk`.
`TAIL_CARE_ON` (True) is the one path that FEEDs outside `want_feed`, but it spends
the block's own harvested wheat carry (7504-7511), not a shed pickup, so `blk[0]` is
the whole shed draw. Fertiliser agrees: `want_fert = fert_cand & (fert_rank <
n_fert_eff)` (5524), so `sum(blk[1]) <= n_fert_eff`. Purchases are untouched — `avail`
is the hour-0 shed, and the turn-1 BUY tops up before the route base. **No bug.**

## 3. The builder's doubt is correct

`terminal = day > O.LAST_SHED_DAY` (5976, = 28) and both reservations are
`xp.where(terminal, 0, ...)` (6634, 6639) — day 29 holds nothing back. `DROP_ON` adds
`gain` = projected banked harvest, `t_yield + 2*water`, to lot 3 (6782-6786); 6771-6775
states the over-ask is deliberate ("asking for more than arrives costs nothing").
`MIDDAY_DROP_ON` is False, so
`drop_day == terminal ==` day 29 only. On d21-28 a SELL row cannot exceed the shed
(`lots` bounded by `avail`, `forced` by `spare = max(avail - s_qty, 0)`, 6729). The
≈19-unit signature is day-29 lot 3 asking for units that do not exist. **The switch
does not fix §2's defect.**

## 4. Verdict

Worth the ~5-minute paired leg as a cheap long shot, not as the §2 fix. It frees
d21-28 `want_feed` that admission dropped (`want_feed` is clipped by wheat
availability, not labour, 5512), but §5 measured the route completing 99.8 % of queued
value and `_worth` (5836) already strikes late feeds with no tomorrow — expect small.

CONFIRM: paired Δmargin > 0, t ≥ 2, driven by d21-28 wheat/fert volume.
REFUTE: level, or negative by displacement (freed wheat is wheat not fed; unfed animals
escape). Log `wheat_reserved - min(...)` per game: under ~2 units/game the mechanism is
inert and the leg is uninformative whatever its margin — close the arm.

Higher-value follow-up: price the day-29 lot-3 over-ask. Rows are clipped
unit-by-unit, so it is likely a non-defect — closing §2's last open signature.
