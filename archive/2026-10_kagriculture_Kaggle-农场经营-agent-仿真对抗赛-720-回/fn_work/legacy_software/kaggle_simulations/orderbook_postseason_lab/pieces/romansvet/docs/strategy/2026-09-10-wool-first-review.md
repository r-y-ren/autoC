# Review: WOOL_FIRST_LOT (worktree wool-first, 646f55c on 45f8217)

Independent read, 2026-09-10. Diff is +293 lines, two files, no deletions.

## 1. OFF byte-identity — CLEAN
All additions are module-level constants, two asserts, `plan.wool_first`, and one
`if WOOL_FIRST_LOT_ON:` block at `plan.py:6790`; the flag is False, so nothing
traces. Worktree tests (`test_wool_first`, `test_sell_allocator`,
`test_bank_before_lot`): **26 passed, 0 failed**. The OFF test pins
`test_route_early`'s twelve-seed six-array digest taken off 45f8217, and a second
test makes `wool_first` raise on a 12-wool / two-YARN_STORE board, so OFF is not
merely the gates refusing. Restack arithmetic checked by hand at CAP 4 and 1:
column sum preserved, surplus drains latest-lot-first.

## 2. Price walk — per-product, but ONE real cross-product coupling
`sell._price_at` is `price_table[p, clip(pos[l,p])]` — each quote reads only its
own product's inventory, and `adjusted_marginals` columns never touch. Moving
wool into lot 1 changes **wool's quote only**; the `WOOL_FIRST_MIN_UNITS`
docstring ("walks our own lot-1 quote down for the products beside them") is
wrong. "Fullest shelf": `PJ.projected_inv` walks the town tick forward and price
is monotone non-increasing in inventory, so turn 3 is the least-drained shelf and
the lowest quote — cost/unit ≈ `price[inv(t3)+j] − price[inv(t18)+j]`.

**The coupling the diff misses**: `_market` counts lot 1's *live products*,
`n_s = sum(lot1 > 0)`, and gates the early row on `row_fits = (n_b + n_s) <= 10`
(`plan.py:8064`) and `hire_fits = (first + n_s) <= 10` (`plan.py:8039`). Adding
wool to lot 1 increments `n_s`, so on a busy day the restack pushes the **whole**
lot 1 — all nine products — off turn 1 back to `SELL_TURNS[0]`. That is a
plausible second component of the −1,066/seat and is worth splitting out before
any judge.

## 3. Sink gate — reads the pinned town correctly
`town_inject.install` wraps `_end_of_day` and overwrites
`state[0].observation.town["unlocked_shops"]` with the day-`day+1` prefix; the
engine then assigns that same dict to every other seat (kaggriculture.py:945-951),
and `parse_town` counts it into `view.shops`. Hour 0 of day D sees the **pinned**
unlock. Day 0 is empty by construction, so the gate cannot fire there.

## 4. The one-line DAY variant
`hold` alone decides whether a unit leaves *today*; wool carries no queued
`avail` reservation (`plan.py:6677-6690` reserves wheat and fertilizer only).
Insert after `plan.py:6693-6696`:

    hold = xp.where(e_wool & (view.shops.astype(i32)[I_YARN_STORE] > 0),
                    xp.minimum(hold, WOOL_SINK_HOLD_MAX), hold)

mirroring `_sell_hold`'s `FERT_FLOOR` clause (`plan.py:3910-3917`); `view` is
already in scope, nothing else changes. That moves the median sell-DAY, which is
what the anatomy measured.

## 5. Verdict
**Fit to judge paired as-is** — OFF-default, reversible, arithmetic sound. But it
is the *turn* lever while the anatomy's gap is the *day*, and self-play already
reads it negative. Judge the §4 hold override in the same worktree first; if only
one gate slot is free, spend it on the day.
