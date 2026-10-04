# Fertilizer: where the FERTILIZE decision is made, and what it buys

Working notes, checkpointed. Worktree `care-cov`, detached at 8ba5778.

## Checkpoint 1 (t+20 min) — Q1 answered from source; the archive already
## contains most of Q2 and the whole of Q4's lever.

### Q1 — where the planner decides to FERTILIZE

One gate, one line, `src/kagg3/core/plan.py:5269`:

    fert_cand = is_plant & (view.t_fert < day) & (fert_val > fert_bar)

Inputs, in order:

| input | where | what it is |
|---|---|---|
| `fert_val` | `plan.py:5256` -> `valuation.py:127 fert_marginal_value` | the exact clipped extra **crop units** one application buys on this tile, times `price[crop]`, today's hour-0 quote |
| `fert_bar` | `plan.py:5263-5269` | OFF = `view.price[I_FERT]`, the fertilizer's own hour-0 spot quote. ON [`FERT_VOLUME_ON`] = `NUM/DEN` x `_fert_reference` (`plan.py:3900`), mode `spot`/`base`/`marginal` |
| `view.t_fert < day` | `plan.py:5269` | never renew an active application (engine sets `fertilized_until_day = max(prev, day+2)`) |
| `is_plant` | tile kind | engine no-ops a FERTILIZE off a PLANT tile |

Downstream, all mechanical:
* `n_fert_want = sum(fert_cand)` (`5270`), `fert_rank = _rank_by(fert_cand, fert_val)` (`5271`)
* `fert_short = max(n_fert_want - shed[I_FERT], 0)` (`5272`) -> the BUY row's fertilizer quantity
* `n_fert_eff = min(n_fert_want, fert_avail)` (`5556`), `want_fert = fert_cand & (fert_rank < n_fert_eff)` (`5557`)
* `fert_reserved` holds that stock back from the day's sale.

**Budget:** fertilizer is candidate list 1 of `budget.grant`'s ten
(`plan.py:4849-4851`): `v_fert` is the k-th best admitted application's
**gross** `fert_val`, cost = the market buy quote `buy_q[I_FERT]`. So the
purchase and the burn are ranked on the same number.

**Unit-turn cost: none.** The gate charges no labour. A FERTILIZE costs a
unit-turn and drags a WATER behind it; neither appears in `fert_val` or in
`fert_bar`.

**Theta head: none on this gate.** `fert_val` reads the raw `view.price[crop]`
and `fert_bar` the raw `view.price[I_FERT]`. Theta reaches fertilizer only
indirectly, through `grow_mult[p]` and `macro.press`/`macro.hold` in the
budget/sell stages (`plan.py:4914`), never through `fert_cand`.

### Prior art found in the archive (user rule: check before re-measuring)

Three fertilizer levers are already built, measured and shelved, and one of
them is exactly the lever this task proposes:

1. `FERT_VOLUME_ON` (`plan.py:3739-3870`) — **"fertilize only when the
   application clears NUM/DEN x the fertilizer price"**, i.e. `FERT_PAYS_ON`.
   Built, three reference modes, 384 paired engine games each. Best mode
   (`marginal`) +636 coins at t 1.50, short of the +1,500 / t 2 bar. `base`
   *loses* 1,103. Verdict in-source: the applications our planner makes are
   buying crop yield at better than the unit's own sale price.
2. `FERT_MARGINAL_ON` (S/fert_marginal/report.md, commit 9ad4f8a) — price both
   sides on the sales-window curve. −1,745 at t −3.09 over 384 games. Shelved.
3. `FERT_BUY_ON` (S/fert_buy/report.md, commit 5a3f6fb) — buy more fertilizer.
   Provably dominated by `budget.grant`; 0 of 200 boards move. Shelved.
4. `FERT_CARRY_ON` (S/fert_carry/report.md, commit bea972d) — **not built**:
   0 no-op FERTILIZE ops in 11,386 classified ops.

And the exact Q2 census was already run once, on 32 McGrain replays
(`S/fert_marginal/quant.md`, bonus model exact on 2934/2934 post-states):
181.2 ops/game buying **269.4 extra crop units** worth 29,602 realised coins
against 7,708 of forgone fertilizer sales = **+21,894 coins/game, positive in
32/32 games**. Per crop: STRAWBERRY 90.2 ops -> 117.5 units, WHEAT 62.0 -> 115.0,
CARROT 16.2 -> 15.1, TOMATO 12.4 -> 20.8, MELON 0.4 -> 0.9.

That measurement is on the *old* champion (flow58_g450) against one tape. The
open question this task can still answer is whether it holds for **g350 on the
six live losses**, and what the **clone's** 61-98 applications are spent on —
never censused. That is the work in progress below.

## Checkpoint 2 (t+65 min) — the census, both seats, on the nine live boards

Method: the Kaggle replay JSONs (`S/ep_<ep>.json`) carry both seats' private
inventories, so no engine run was needed and nothing here is seed noise — these
are the live games to the coin. The fertilizer-bonus model is lifted verbatim
from `S/fert_marginal/fert.py` and re-validated here: **2,254/2,254 predicted
`yield_units` exact on the ongoing-refresh path, 0 mismatches, 2 dead ops in
18 seat-games.** Script `S/fertcens/cens.py`, aggregation `S/fertcens/agg.py`.

Op counts reproduce `2026-09-09-loss6-anatomy.md:49` exactly (ours 171–189,
theirs 61–98), which is the census's own cross-check.

Crop units are priced at the end-of-day quote of the day they were produced;
each application's fertilizer is charged at that same day's fertilizer quote
(the marginal price one more unit would have fetched).

### Q2 — what each seat's applications buy, per crop

**OURS, six live losses (n=6, per game)**

| crop | ops | extra units | u/op | crop coins | fert coins | net | net/op |
|---|---|---|---|---|---|---|---|
| WHEAT | 86.2 | 161.2 | 1.87 | 6,316 | 3,212 | **+3,104** | +36.0 |
| CARROT | 6.3 | 6.3 | 1.00 | 287 | 80 | +207 | +32.6 |
| TOMATO | 7.7 | 12.3 | 1.61 | 1,763 | 123 | +1,640 | +214.0 |
| STRAWBERRY | 79.2 | 102.0 | 1.29 | 15,875 | 4,012 | **+11,863** | +149.9 |
| MELON | 0.0 | — | — | — | — | — | — |
| **TOTAL** | **179.3** | **281.8** | 1.57 | 24,240 | 7,426 | **+16,815** | +93.8 |

**THE CLONE, same six games (n=6, per game)**

| crop | ops | extra units | u/op | crop coins | fert coins | net | net/op |
|---|---|---|---|---|---|---|---|
| WHEAT | 3.8 | 4.5 | 1.17 | 50 | 28 | +22 | +5.7 |
| CARROT | 4.2 | 4.2 | 1.00 | 20 | 3 | +17 | +4.1 |
| STRAWBERRY | 70.8 | 127.3 | 1.80 | 15,279 | 2,874 | **+12,405** | +175.1 |
| **TOTAL** | **78.8** | **136.0** | 1.73 | 15,349 | 2,905 | **+12,444** | +157.8 |

Three pinned boards (106401414 / 106773901 / 106793159): ours 187.0 ops →
+21,622 (WHEAT 50.0 @ +29.4, CARROT 27.3 @ +29.3, TOMATO 9.7 @ +251.5,
STRAWBERRY 100.0 @ +169.2); opponent 85.3 ops → +15,823 (STRAWBERRY 68.3 @
+231.2, CARROT 15.3 ops producing **zero** extra units, WHEAT 1.7 @ +14.8).

**Pays / does not pay.** Every crop either seat fertilizes is positive against
the fertilizer's own spot quote. Nothing is negative. The clone is not running
a better allow-list; it is running a *narrower* one — 90 % of its applications
are STRAWBERRY, and its 15.3 pinned-board CARROT applications buy literally
nothing. Our extra 100 applications a game are WHEAT (86) plus TOMATO (8) plus
STRAWBERRY (8), and the marginal one earns +36 coins gross of labour.

**So the loss ledger's `FERTILIZER −4.1k` is an income-line artifact.** They
book 15.1k of fertilizer *sales* to our 10.0k because they burn 79 units to our
179; we book the difference back as crop revenue, and we book **+4.4k more of
it than they do** (+16,815 against +12,444). We are ahead on this trade.

### Q3 — two-purse, if we dropped the 86 WHEAT applications

The two markets move in opposite directions and the engine's own curves decide
which wins (`kaggriculture.py:192 market_price`; params at `:37-58`).

*Fertilizer* — `above_func "linear"`, `above_target 0.40`, `T 200`, `base 100`
→ exactly **0.2 coins per unit above I0**, and fertilizer is the one product
with **zero town drain** (no shop lists it; the town centre consumes one of
every *other* product), so its inventory is a pure cumulative pool. Measured
end-of-game inventory in the six losses: 10,468–10,493, quote **1–6 coins** —
already on the floor (`PRICE_FLOOR = 1`, `:39`). Walking the real per-day sale
schedules of both seats through `market_price` with 86 extra units of ours
added from day 12:

    ours   fertilizer revenue   9,997 -> 11,591   +1,594
    theirs fertilizer revenue  15,116 -> 13,612   -1,504
    margin from the fertilizer market alone                 +3,098

The 86 units fetch 18.5 coins each, not the 41 the naive census credits,
because they walk their own curve down — and they take 1,504 coins off the
clone, which sells 356 units to our 206. That half is a genuine denial win.

*Wheat* — `below_func "sqrt"`, `below_target 0.80`, `T 400`. The observed wheat
quote **rises** 28 → 43 over the season, i.e. the town drain holds inventory
*below* I0 on the steep branch, where a withdrawn unit is expensive. Same
walk, day-start inventory taken from the observed quote so the drain is
implicit, our sales cut by the 161 lost units pro-rata from day 12:

    ours   wheat revenue  12,955 ->  6,474   -6,481
    theirs wheat revenue  13,814 -> 14,517     +704
    margin from the wheat market alone                      -7,184

**Net: −4,086 coins of margin per game.** Dropping the wheat fertilizations
loses more on the scarce-side wheat curve than it wins on the saturated
fertilizer curve, and it hands the clone +704 of wheat price on the 386 units
it sells. Two-purse verdict: the lever is a displacement, not a saving.

### Q4 — the smallest lever, and why it is not built

The lever the task names — *fertilize only when the projected doubled yield
beats the fertilizer price plus a margin* — **already exists**, shipped OFF, as
`plan.FERT_VOLUME_ON` (`plan.py:3739-3870`, `FERT_VOLUME_NUM/DEN`,
`FERT_VOLUME_MODE` in `spot`/`base`/`marginal`). Its measured table is in the
source block: best mode +636 coins at t 1.50 over 384 paired engine games,
short of the +1,500 / t 2 bar; the `base` mode loses 1,103. Building it again
would be a duplicate.

The per-crop allow-list variant (match the clone: STRAWBERRY only) is refuted
by the two rows above before any code is written: **it is exactly the −4,086
counterfactual**, because 86 of the 100 applications it would remove are wheat.
Consistent with the `FERT_CARRY_ON` precedent (`S/fert_carry/report.md`), no
dead constant was added to `plan.py` for a lever whose measurement is already
the wrong sign.

**Not verified:** the −4,086 is a market-curve counterfactual on the observed
sale schedules, not a paired engine run — it holds every other decision fixed,
so it does not price what the 86 freed unit-turns (and the 86 WATERs they drag,
`plan.py:5561`) would earn elsewhere. At the PRESTOCK calibration (~9 coins a
turn) that is ~1.5k, which narrows the gap but does not close it. No engine
paired run was made (machine loaded; the parent chains those).
