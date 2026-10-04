# 2026-09-11 — `EARLY_SELL_MODE`: the two never-run values, measured against candidate B

`plan.py:2466` ships `EARLY_SELL_MODE = "A"`, and the enum admits seven values
(`"A", "A1", "A0", "A21", "B", "Z", "Z1"`, assert at plan.py:2477). The planner-wall audit
lists the mode as an open lever because only `"A"` has ever been run against the seat we
actually ship. This screens the two the brief named — **`"B"`** (lots 2/3 moved to the first
free turns, 4 and 5: "sell as it lands") and **`"A0"`** (lot 1 behind turn 0's hires instead
of behind the BUY row) — on candidate B's own promotion legs.

Nothing was promoted. `EARLY_SELL_MODE` stays `"A"`.

## Method (the pump sweep's pipeline, under `esm_` names)

Identical mechanism to `2026-09-11-open-pump-sweep.md`, reused rather than rebuilt:

* theta = candidate B, `artifacts/kagg2_games/thetas/flow193_g100_hr.npy`, switches
  `OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`;
* legs = the judge's own runners — `S/topb2/run.sh` (20 held-out top-tier pinned tapes × 2
  seats = 40 games, seed base 777001, `--seed-per-opponent`), `S/livec/run_holdout.sh`
  (LIVE-C ids 43-72, 60 games) and `S/livec/run_holdout2.sh` (ids 73-102, LIVEC-H30B);
* run on the **copy** of `.claude/worktrees/arms-next` at `scratchpad/pumptree` (plan.py md5
  `3098247432e4a18ebdd7f0008f4d0dc0` = the judge's), with the mode moved by
  `S/drainpin/on2b.py` `setattr` before the first trace — never by editing a tree. That is
  legitimate here because every reader of the mode is a trace-time call
  (`early_lot_turns()`, plan.py:2527, read at plan.py:6612 and 8091), not an import-time
  constant;
* paired against B's own base csvs with `S/bank/paired.py` on `(seed, opponent, seat)`,
  `t` on per-board seat means; runner `S/esm/sweep.sh`, log `S/esm/sweep.out`.

**Identity gate:** `EARLY_SELL_MODE="A"` set explicitly reproduces the base csv exactly —
40/40 TOPB2 rows identical, Δ = 0. The mechanism moves the constant and nothing else.

### `"A0"` cannot be run with the pump on — and fails silently

`plan.py:7752` refuses the hire-row / lot-first / zero-row modes while `OPEN_PUMP` is live
("OPEN_PUMP needs the sell-back at index 0 of the BUY row"), and `"A0"` is in
`EARLY_SELL_MODES_HIRE_ROW`. The probe (`S/esm/a0_pumpon_probe.log`) shows what that costs:
the assert fires inside the traced plan, the harness catches it, and **our seat plays the
whole season with 0 moves and ends on `STARTING_MONEY` = 3,000 coins** (margin −154,609).
No traceback, exit status 0. Any future sweep that pairs a switch combination the planner
refuses will read as a 154k loss rather than as an error — worth knowing before the next
constant sweep.

So `"A0"` is measured with `OPEN_PUMP_ON=False`, paired against the **pump-off** seat on the
same boards (`S/lossflip/pump_off_*.csv`, from the pump sweep), and also reported end-to-end
against shipped B so the pump's own delta is not hidden.

## Results

Base = candidate B as shipped, except the `A0` rows, whose base is B with the pump off.
"flips" = games won that the base lost / lost that it won (40, 60, 60 games respectively).

| variant | set | boards | win% base→variant | flips +/− | Δmargin/game | t | verdict |
|---|---|---|---|---|---|---|---|
| identity (`MODE="A"` set explicitly) | TOPB2 | 20 | 32.5 → 32.5 | 0/0 | **0** | — | **gate passed**, 40/40 rows identical |
| `MODE="B"` | TOPB2 | 20 | 32.5 → **15.0** | 0/−7 | **−7,976** | **−9.78** | **DEAD — kill rule, 20/20 boards worse** |
| `MODE="B"` | LIVEC-H30 | 30 | 63.3 → **33.3** | 0/−18 | **−7,284** | **−20.49** | **DEAD — 30/30 boards worse** |
| `MODE="A0"` (pump off) | TOPB2 | 20 | 32.5 → 35.0 | +2/−1 | +432 | 1.18 | not significant |
| `MODE="A0"` (pump off) | LIVEC-H30 | 30 | 63.3 → 61.7 | 0/−1 | −9 | −0.06 | level |
| `MODE="A0"` (pump off) | LIVEC-H30B | 30 | 80.0 → 80.0 | 0/0 | −119 | −2.14 | tiny and negative (sd 302) |
| `MODE="A0"` end-to-end vs shipped B | TOPB2 | 20 | 32.5 → 35.0 | +2/−1 | +204 | 0.40 | level |
| `MODE="A0"` end-to-end vs shipped B | LIVEC-H30 | 30 | 63.3 → 61.7 | 0/−1 | +11 | 0.04 | level |
| (control) `OPEN_PUMP_ON=False` | LIVEC-H30B | 30 | 83.3 → 80.0 | 0/−2 | +338 | 1.10 | the A0 rows' base, level |

### Why mode `"B"` loses ~8k a game, everywhere

Not the shop-draw lottery this file's predecessor warned about: 50 of 50 boards move the same
way, and the per-game telemetry says what happens. Mean `unsold` units at the end of a game
(the csv's own column):

| set | base (`"A"`) | `"B"` |
|---|---|---|
| TOPB2 | 7.7 | **90.4** |
| LIVEC-H30 | 7.4 | **91.5** |

Mode `"B"` puts lots 2 and 3 on turns 4 and 5 (`O.EARLY_SELL_LATE_TURNS`) instead of 10 and
18. With `DROP_ON` live the crew drops its pickups into the shed *during* the day, so the
stock the afternoon produces arrives after the last sell row has already gone out: the day's
own harvest has no row left to stand on and rides to the next day, and ~83 units never get
sold at all. Our own coins fall 8,302/game on the hold-out while the opponents' fall 1,018 —
this is not a denial trade that backfired, it is our own produce left in the shed. The
`ops.py:160-167` rationale for the mode ("every recorded 2800-tier opponent's flow lands at
hours 10-17, so a day finished selling by hour 6 is in front of all of them") is correct
about the race and wrong about the inventory: being first is worth far less than selling the
afternoon at all. **The row-count direction in the loss ledger — the top tier's 389 sell rows
of 3.95 units against our 152 of 9.39 — cannot be bought by moving our three lots earlier.**
It needs *more* rows spread across the day, not the same three compressed into hours 3-5.

## Conclusion

1. **`"B"` is dead, decisively and mechanistically** — −7,976 (t −9.78) on TOPB2 and −7,284
   (t −20.49) on the hold-out, 50/50 boards worse, because lots on turns 4-5 leave the
   afternoon's ~83 dropped units unsold. This is the first read on these legs that is a
   mechanism rather than a seed-set lottery, and it closes the mode as a place to look for
   the top tier's row-count edge.
2. **`"A0"` is level and unmeasurable against the shipped build** — +432 (t 1.18) TOPB2,
   −9 (t −0.06) LIVEC-H30, −119 (t −2.14, sd 302) LIVEC-H30B; end-to-end against shipped B
   it is +204 / +11 (|t| < 0.5). It also cannot ship while `OPEN_PUMP_ON` is live at all
   (plan.py:7752), so there is nothing here to promote.
3. **A pipeline warning worth more than either result:** a planner assert inside the traced
   plan does not crash the eval — the seat simply plays nothing and scores 3,000 coins. Any
   switch sweep must check `moves > 0` before believing a large negative.

## Artefacts

* csvs: `S/lossflip/esm_{ident,modeB,A0off,pumpoff}_{topb2,livech,livech2}.csv`
  (paired against `S/lossflip/flow193_g100_hr_{topb2,livech,livech2}.csv` and
  `S/lossflip/pump_off_{topb2,livech}.csv`).
* paired lines `S/esm/sweep.out`; runner `S/esm/sweep.sh`; A0-with-pump probe
  `S/esm/a0_pumpon_probe.log`.
* Nothing in the judge's tree, csv namespace, lock or state was touched; no theta promoted.
