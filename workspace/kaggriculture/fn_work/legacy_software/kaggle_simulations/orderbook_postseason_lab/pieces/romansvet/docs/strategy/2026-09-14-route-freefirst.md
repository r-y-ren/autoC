# ROUTE-FREEFIRST — the morning turns are recoverable, and they are worth nothing

**VERDICT — NOT PROMOTABLE. The 68-band pooled Δcoins is +23 (t +0.18), Δmargin
−79 (t −0.51): NOT ≥ +450 at t ≥ 2.** Unlike PRESTOCK-REPAIR, this arm is not a
reachability failure — it fires on **66 of 68 boards** and it does exactly what
it was built to do: **h0-h1 PASS falls 266.3 → 237.0, −29.3 turns/game (11 % of
the block), 27.2 PICKUP unit-turns move out of hour 2 and into hour 1.** The
result that matters is what those turns bought: **nothing.** Worked turns/game
*fell* 9.4 (5,986.4 → 5,977.0), tiles worked rose 8.2, and the purse moved +23
coins on 68 boards. TURNS priced the morning block at 17.5 coins/turn, which
predicts **+513 coins** for 29.3 turns; the paired ledger delivers **+23**, a
20x overstatement and the two-purse rule again.

**The 266 morning PASS turns are slack, not a constraint.** That closes the
"give the crew its morning turn back" family: `ROUTE_SPLIT_ON` already took the
reachable half, this arm takes the rest, and the rest is free.

All sim-descriptive: CRN sim, tape-action opponent seat, pinned towns,
`shop_crn`, theta `flow193_g100_hr` (= B), switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON`, 12 ymg_aq boards +
68 band boards (TOPB2 40 + LIVE-C 28), both seats of every town. **No engine
game, no ES arm, no promotion gate, no remote host.** Baselines are the on-disk
OFF raws (`raw_headOFF.npz`, `raw_melOFF.npz`).

## 1. Which blocks are held back today, and by what

Two different laws hold the morning, and only one of them is a law.

| law | file:line | what it forbids |
|---|---|---|
| **the hire law** | `ops.ROUTE_BASE`, read at `plan.py:6841` | a hand hired in turn t first acts in t + 1. A narrow crew is hired at `TURN_HIRE` = 0, so `O.TURN_BUY` = 1 is already its first legal turn. Not the binding thing. |
| **the spawn law** | `ops.ROUTE_BASE_WIDE`, `plan.py:6962` | a unit that has *walked* off its shed-access tile re-scatters every hand `_spawn_hand` places afterwards, so on a **wide** day (`n_hire > MO`, `plan.py:6840` -- a second HIRE row at turn 2) nobody may step before turn 3. Untouched here. |
| **the BUY-row dependency** | `_buy_row_units`, `plan.py:3351` | the real jailer. `route_base` = `O.ROUTE_BASE` = `TURN_BUY + 1` so that "the shed already holds what the BUY row bought" (`plan.py:7314`). |

`route_split` (`plan.py:6943-6965` day gate, `plan.py:8093-8094` per block) is
the existing relief, and its per-block test is the strongest one there is:

```python
free_first = (base_move > 0) | (cop[s, 0] != O.OP_PLANT)      # plan.py:8093
narrow_ok  = (~wide) & (d_pick[e1] == 0) & free_first          # plan.py:8094
```

`d_pick[e1] == 0` is **"this block owes no PICKUP at all"** — the per-*day*
question `_buy_row_units` asks ("does *anything* ride the row"), pushed down to
a block. `free_first` is already the per-op half and it is already correct:
PLANT is the one op the row feeds directly, every other carried input arriving
through a PICKUP. So today a block that walks first and picks up nothing gets
turn 1 — and **any block that owes a single PICKUP waits**, even for wheat the
day does not buy. `2026-09-14-turns.md` measures the consequence: 236.3 of
269.5 hour-1 unit-turns are PASS and 210.4 units PICKUP at hour 2. **The held
block is the pickup-owing one.**

**First-op classes that need nothing from the BUY row.** A unit collecting at
`O.TURN_BUY` draws *last night's* shed close (`_end_of_day` →
`_drop_inventories_to_shed`), because turn 1's market phase runs **after** turn
1's unit phase — the ordering `_buy_row_units`' own docstring states for the
seed. So:

* **a move** (`base_move > 0`) — already free under `free_first`;
* **WATER, HARVEST, DIG, BUILD, CARE, COLLECT_FERT** — consume nothing carried;
* **a PICKUP of a kind the day does not buy** — fed by last night's shed; **new here**;
* **FEED / FERTILIZE behind such a PICKUP** — same;
* **PLANT** — the **one** exception. The seed is credited after turn 1's unit
  phase, so PLANT stays behind the row on every seed-buying day, which is
  nearly every day (`2026-09-14-prestock-repair.md` §5).

## 2. What was built (default-off, `src/kagg3/core/plan.py`)

| site | line | what |
|---|---|---|
| `ROUTE_FREEFIRST_ON = False` | `plan.py:2377` | master switch (doc block `2334-2376`) |
| `freefirst` | `plan.py:6967-6976` | `[N_PICK]` bool: which pickup kinds today's BUY row delivers (`wheat_buy > 0`, `fert_bought > 0`, `a_buy[a] > 0`). **Seeds absent on purpose** — nothing PICKUPs a seed and `free_first` holds the PLANT. Gated on `route_split is not None`, so it is a widening of an existing gate and never a new one. |
| per-block test | `plan.py:8095-8112` | `owed1 = cpick[:, e1] - prev` is the trial block's own demand per kind; `free_pick` = every owed kind has a **zero purchase today**; `narrow_ok = (~wide) & free_pick & ((d_pick[e1] > 0) \| free_first)`. A block owing nothing has `owed1` all zero and reduces to the old expression, so the set only grows. |
| pickup rows | `plan.py:7334-7342` | `pk_base = route_base - early` — a narrow early block may now owe pickups, so its rows move with its start exactly as the wide branch's already do. Identical to the shipped line wherever `early` is zero or `wide`. |

**Both laws hold.** The hire law: `TURN_BUY` is the narrow crew's first legal
turn, so this reaches it and never goes below it (asserted on real plans by
`test_on_moves_no_unit_in_front_of_a_row_it_depends_on`). The spawn law: the
switch is `~wide`-only, and the op it pulls to turn 1 is a **stationary**
PICKUP. PLANT: a block that owes a pickup starts its route at
`TURN_BUY + d_pick ≥ O.ROUTE_BASE`, so the seed has resolved before it plants
either way.

**Tests.** `JAX_PLATFORMS=cpu python -m pytest tests/test_macro_exec.py
tests/test_rebuy.py tests/test_prestock_v2.py tests/test_lot_split.py -q` →
**50 passed**; `tests/test_route_freefirst.py -q` → **6 passed**. The six:
OFF whole-plan tuple hashed against a **pristine `git archive HEAD src` tree
built in a subprocess** (the OFF-identity receipt, as `test_prestock_v2.py`
does); OFF keeps every PICKUP behind `O.ROUTE_BASE`; ON drops h0-h1 PASS on the
`stocked` fixture; ON puts no unit in front of a row it depends on (every
sub-`ROUTE_BASE` PICKUP is of an item the day's own market rows do **not**
deliver, and nothing acts below `O.TURN_BUY`); a PLANT-first block on a
seed-buying day is byte-identical; a day that buys what its blocks collect
(`feed`, 4 shed wheat vs 12 hungry geese) is byte-identical.

## 3. The paired ledger (ON − OFF, same CRN boards, both seats)

| set | n | our coins Δ (t) | margin Δ (t) | their coins Δ (t) | wins | flips |
|---|---:|---:|---:|---:|---:|---:|
| ymg_aq | 12 | −46 (−0.13) | **−759 (−1.80)** | +714 (+1.48) | 0→0 | +0/−0 |
| **band pooled** | **68** | **+23 (+0.18)** | **−79 (−0.51)** | +102 (+1.88) | 29→28 | +0/−1 |
| band TOPB2 | 40 | +23 (+0.11) | −167 (−0.66) | +190 (+2.16) | 13→12 | +0/−1 |
| band LIVE-C | 28 | +24 (+0.30) | +48 (+0.49) | −23 (−0.83) | 16→16 | +0/−0 |

**The 68-band pooled Δcoins is +23 with t +0.18. It is NOT ≥ +450 at t ≥ 2.**

Our own purse is a dead heat; the margin is negative because **their** coins
rise (+102, t +1.88 on band; +714, t +1.48 on ymg). Collecting a turn earlier
shifts our buys and sells by one turn against a shared pot, and the tape
opponent is the one that banks the difference — the 2026-08-28 "we both got
richer" externality with only one of us richer.

The switch is **live**, not dead: 66/68 band boards and 12/12 ymg boards end on
a different purse, spread −4,106 … +2,637, median +75. The first divergent day
is **day 9** on almost every board — before that, every block either owes no
pickup (already `route_split`'s) or owes a kind the day buys.

## 4. Turns recovered: 29.3 of 266.3 (`S/turns` instrument, 12 ymg_aq boards)

| arm | worked turns/game | active turns/game | h0-h1 PASS | h0 PASS | h1 PASS | h2 PASS |
|---|---:|---:|---:|---:|---:|---:|
| OFF (B) | 5,986.4 | 6,673.4 | **266.3** | 30.0 | 236.3 | 24.1 |
| ON | 5,977.0 | 6,627.2 | **237.0** | 30.0 | 207.0 | 22.5 |

The movement is exactly the intended one, and nothing else moves:

| hour | op | OFF | ON | Δ |
|---|---|---:|---:|---:|
| 1 | PASS | 236.3 | 207.0 | **−29.3** |
| 1 | PICKUP | 0.0 | 27.2 | **+27.2** |
| 2 | PICKUP | 210.4 | 187.8 | −22.7 |
| 2 | WEST/EAST/NORTH | 32.7 | 55.5 | +22.8 |
| — | **PICKUP, whole game** | **291.6** | **291.7** | **+0.1** |
| — | tiles worked | 1,230.8 | 1,239.0 | +8.2 |
| — | WATER | 972.2 | 978.2 | +5.9 |
| — | hires (unit-days) | 3,380.7 | 3,354.8 | −25.9 |

**Nothing new is picked up** (+0.1 PICKUP turns a game) — the same collection
happens one turn earlier and the walk it used to wait for starts one turn
earlier. Worked turns **fall** 9.4.

**Why the turn does not become work.** The admission estimate already spent it.
`plan.py:7201` credits every unit on a `route_split` day with the extra turn —
`labour = labour + xp.where(route_split, n_units, 0)` — and its own comment
says why it is optimistic: *which* units come out early is a property of the
block cut, which does not exist at that point. So OFF, `n_admit` is **already
sized as if every block got the morning turn**; delivering it for real adds no
admitted tile, it only lets an already-over-admitted list finish earlier. The
realised gain is the 8.2 tiles/game the shorter day happens to reach —
+23 coins. (Per day the turn *is* live: on the `stocked` fixture the block's
worked ops go 41 → 44.)

## 5. What this closes

1. **The 266-turn morning block is answered.** `route_split` took the
   no-pickup half; this takes the "owes only what the shed already holds" half;
   what is left behind the row is the PLANT, which is a real data dependency,
   and the wide day, which is the spawn law. There is no third slice.
2. **And the answer is that the block is slack.** Two independent arms now
   agree: PRESTOCK-REPAIR bought 6.3 worked turns for −326 coins, ROUTE-FREEFIRST
   buys 29.3 morning turns for +23. **17.5 coins/turn is a counterfactual price,
   not a lever price** — TWO-PURSE RULE, eighth family.
3. **The binding constraint is admission, not turns** (`plan.py:7201`,
   `ADMIT_ROUNDS`). Any further morning work has to come from the *estimate*
   being wrong about which tiles are worth reaching, not from the crew having
   more turns to reach them with.

## 6. Next

1. **Do not spend an engine leg on ROUTE_FREEFIRST.** Leave it default-off in
   the tree as the read the family never had, exactly as `PRESTOCK_V2_ON` sits.
2. **If anyone re-opens the morning, open it at `plan.py:7201`.** The honest
   experiment is the opposite of this one: make the labour credit *exact* (drop
   the day-level `+ n_units`, credit only the blocks `_routes` actually cuts
   early) and see whether a truthful, smaller `n_admit` picks better tiles. That
   is an admission arm, not a route arm, and it is the only one of the two this
   ledger has not falsified.
3. **The smaller crew (350.6 turns) is still the larger half of the 695**
   (`2026-09-14-turns.md` §5) and is untouched by every arm in this family: the
   binding thing there is the hire enumeration's value model, not the wage and
   not the route.
4. Their-coins rising on both board sets (+102 / +714) is worth one cheap probe
   on its own: a one-turn shift in *our* market timing moves the tape
   opponent's purse by more than it moves ours.

## 7. Files

Scripts/logs `S/route_freefirst/{launch.sh,turns.sh,diag.py,ff_ymg.log,
ff_band.log,turns_off.log,turns_on.log,ledger.md,turns.md,diag.md}`; raws
`S/macro_exec/raw_freefirst_{ymg,band}.npz` and
`S/turns/raw_ff_{off,on}_ymg.npz`; code `src/kagg3/core/plan.py` (default-off),
`tests/test_route_freefirst.py`. Ledger reproduced with
`S/prestock/report.py`, turns with `S/prestock/turns_cmp.py`.
