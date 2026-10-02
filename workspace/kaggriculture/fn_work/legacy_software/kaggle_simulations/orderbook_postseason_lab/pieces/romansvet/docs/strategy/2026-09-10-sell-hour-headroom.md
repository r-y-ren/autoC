# Sell-hour headroom beyond flow172_g60 — CRN sim probe

2026-09-09. Base = **flow172_g60**, 61 pinned-town action tapes x 2 seats (122 board-seats),
worktree `arms-next`, harness `S/sellhour/run.sh` — `S/simprobe/run.sh` forked so the probe can
also force `kagg3.core.ops` knobs (`SELL_TURNS` is snapshotted at import by `sell.N_LOTS` and
three `plan` asserts, so it is set before either module exists; `ops._check_schedule()` re-runs
on the forced layout). Base: win 45.1 %, margin −376. **A screen, not a promotion.**

## Which knobs are live

- `ops.SELL_TURNS` — **live**. `plan.early_lot_turns()` returns it verbatim under
  `EARLY_SELL_MODE="A"`, `rollout.MARKET_TURNS` is built from it at import, and the lot count is
  generic (`sell.N_LOTS = len(SELL_TURNS)`), so 2 and 4 lots both trace.
- `plan.EARLY_SELL_ON` — **live** (`plan._market`).
- per-product sell-hour map — **does not exist**: the product→lot split is `sell.allocate`'s
  greedy on learned `hold`/`press`, not a turn table. Arm 5 skipped — a code change, not a knob.

`SELL_TURNS[-1] < TURN_PRESTOCK < 23` caps the last lot at turn 21, so the requested
`(3,10,18,22)` is **illegal**; `(3,10,18,21)` ran instead (`TURN_PRESTOCK` moved with it, inert
under `PRESTOCK_ON=False`).

## Arms — paired Δmargin vs g60, same boards and seeds

| # | arm | HELD42 (n=84) | LEG20 (n=20) | LOSS12 |
|---|---|---|---|---|
| 1 | `SELL_TURNS=(3,10,21)` | −165 sd 1618 SE 177 **t −0.94** | −299 sd 1082 SE 242 **t −1.24** | −463 t −1.64 |
| 2 | `SELL_TURNS=(3,10,18,21)` | −77 sd 1312 SE 143 **t −0.54** | −116 sd 1148 SE 257 **t −0.45** | −109 t −0.44 |
| 3 | `EARLY_SELL_ON=False` | −77 sd 870 SE 95 **t −0.81** | −54 sd 870 SE 195 **t −0.28** | +32 t +0.27 |
| 4 | `SELL_TURNS=(10,18)` | −10,123 sd 6460 **t −14.4** | −10,739 **t −5.47** | −12,578 t −9.25 |

The probe prints margins only — no price/unit column.

## Verdict: **no headroom** in the lot-turn layout

No legal move of the evening row clears noise. Turn 18 is already at or past the profitable end —
turn 21 buys one restock tick and pays for it with a shorter DROP-day route budget
(`turn_budget` is cut to `SELL_TURNS[-1] + 1`), dropping two held-out tapes. A fourth lot buys
nothing: the allocator can already put the whole day in lot 3.

Arm 4 is **confounded, not a lever read**: `SELL_TURNS[0]` carries the day's BUY_LAND in its
tenth slot, so deleting turn 3 pushes every land purchase to turn 10 and costs 24 held-out
board-seats. It measures land timing, not sell hours.

Arm 3 is the informative one. The turn-1 sale was worth +2.2k when it shipped; under g60 it is
**−77 ± 95** (HELD42) and **−54 ± 195** (LEG20) — zero. ES never found a *layout* lever: it moved
units out of lot 1 into lot 3 through the learned `hold`/`press` reservations (h1 105.8→99.4
rows, h18 32.2→38.0), and the early row now has nothing left to carry.

**Worth an engine read: none.** The next question is a reservation, not a turn — whether
`sell.press` has decodable range to push past 38 h18 rows. That is a gene-slope check.
