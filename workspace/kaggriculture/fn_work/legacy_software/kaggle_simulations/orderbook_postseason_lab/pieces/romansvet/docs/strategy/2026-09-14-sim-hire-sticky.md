# The hire-sticky reflex in the TRAINING-SIM tape seat

Closes the open item at the end of `docs/strategy/2026-09-14-tape-hire-fix.md` §6 ("the sim seat (`es.tape_actions`) does
NOT carry this reflex, so a sim screen and an engine leg now disagree on a hire-heavy tape under the flag"). Built and
measured 2026-09-14 09:00-09:45Z.

**VERDICT: ported, default-OFF, and OFF is bit-identical (36 TOPB3 rows x 14 ledger arrays x 31 day snapshots, 0 coins).
With the flag ON the sim reproduces the ENGINE's `--hire-sticky` leg to the coin on 15 of 18 boards; measurable boards
(sim retention >= 0.95) go 7 -> 8 (DSM 1 -> 2, Majkel1337 0 -> 0, ymg_aq 6 -> 6), and B's paired margin on the 7 boards
measurable both ways moves -48/board (t -1.00). The three boards where sim and engine disagree are the three where the
sim's re-issue never fires at all, which isolates them to the half of the engine flag deliberately not ported -- `_MAP`
-- and refutes the fix doc's §2 "`_MAP` provably reduces to the identity" (§6).**

The lever the sim now carries is the one the fix doc called the measurable half: a refused HIRE is re-issued later the
same day, behind the tape's own market row, capped at the source's own roster.

## 1. Code paths

Both edits are behind one trace-time Python bool, the `plan.PRESTOCK_ON` pattern: with it off, not one instruction of
the new path is emitted, so an unflagged run is the program it always was rather than a masked copy of a new one.

* `src/kagg3/sim/rollout.py:96` -- `HIRE_STICKY`, default OFF, `KAGG3_TAPE_HIRE_STICKY=1` at import or
  `setattr(rollout, "HIRE_STICKY", True)` before the first trace (:74-97 documents the defect and the semantics).
* `src/kagg3/sim/rollout.py:313-321` -- inside `run_day`'s tape block: gathers this day's two host-side rows
  (`tape.src_hands[t, day]`, `tape.mlen[t, day]`) and the seat mask into `sticky`. Absent when the flag is off OR the
  tape carries no roster.
* `src/kagg3/sim/rollout.py:352-357` -- `turn_body(st, h, rows=None)`: the turn's market row for both seats becomes a
  parameter. `rows is None` -- every call on the default path -- traces the same three gathers it always did.
* `src/kagg3/sim/rollout.py:422-460` -- the day's scan, in two versions. Default: unchanged. Sticky: the carry gains two
  int32 scalars, `owed` (hires still to make good today) and `prev` (the roster when the previous turn was planned),
  which is the engine agent's `_STATE["owed"]` / `_STATE["live"]`. Per turn: `live = nhands[tape seat]` read *before*
  the units and the market (the engine agent's `_hand_count(observation)`); `owed = max(0, owed + added - (live -
  prev))`, `added = src_hands[h] - src_hands[h-1]`, both zeroed at `h == 0` (the nightly wipe, `eod.py:271`); `extra =
  clip(min(owed, src_hands[h+1] - live), 0, MO)` and 0 on the day's last turn; `extra` slots of `MO_HIRE` written at
  `mlen[h] .. mlen[h]+extra`, i.e. APPENDED behind the recorded row and its refused slots, inside the `MAX_MARKET_ORDERS`
  truncation. Same five rules as `scripts/tape_opponent.py`'s HIRE-STICKY MODE, which was read-only here.
* `src/kagg3/es/tape_actions.py:127-135, 255-259, 276-279` -- two new optional table fields, `src_hands` and `mlen`,
  int32 `[ND, TPD]`: the roster the RECORDING had at the start of each step (`len(frame["hands"])`, pre-truncation) and
  the length of its recorded market row (clipped to `MO`). `save` / `load` / `device` / `stack` (:302, :318, :340, :363)
  carry them the way `town` is carried -- written only when present, `None` on every `.npz` cut before them, an all-zero
  row for a stacked member that lacks them (`owed` then never leaves 0, so that tape plays its frozen row flag-on).
* NOT ported, on purpose: the engine flag's `_MAP` (live hand -> source hand). The sim addresses unit slot `u` with
  `uop[d, u, h]` and masks slots past the live roster in `units.apply_units`; a slot past the source's roster reads a
  zero row, which is `OP_PASS`. That IS the map -- see §6 for the one case where it is not.

Tools (new): `S/sim_hire/{build_tapes.py,ledger.py,ledger_band.py,retain.py,tapes/,retain.txt,*.log,raw_*.npz}`. Test:
`tests/test_sim_hire_sticky.py` (2 tests, `..` in 258 s): flag-off equivalence of a tape carrying the new rows against
the same tape with them stripped (money, roster, shed, 4 days), and flag-on day-1 roster on 108795516 == the source's
day-1 roster (4), where the frozen tape ends on 3.

## 2. Identity, flag OFF

`S/sim_hire/ledger.py` is `S/topledger3/ledger.py` with three knobs bolted on (`--src`, `--tapes-dir`, `--hire-sticky`)
and nothing else changed: same 36 rows (18 episodes x 2 tape seats, `S/topledger3/boards.json`), same theta
(`flow193_g100_hr`), same switches (`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON`), same `shop_crn`, same
pinned towns, same monkey-patched per-product `_market_turn`.

* `raw_off_base.npz` = a frozen pre-edit copy of `src/` + the **original** `artifacts/tape_actions_town/` tapes;
  `raw_off.npz` = the edited tree, flag OFF, + the **re-cut** `S/sim_hire/tapes/` tapes.
* **All 14 arrays (`money, nhands, shed, mkt_inv, price, tiles, anim, fert, idle, nquad, sold_np, sold_rp, buy_np,
  buy_cp`) x 36 rows x 31 day snapshots are equal element-for-element.** 0 coins, and not only on coins.
* The re-cut is pinned: `S/sim_hire/build_tapes.py` rebuilds each table from the package the `.npz` was cut from and
  refuses to write unless the six action arrays, `hours` and the town row come back bit-identical -- 18/18.
* The **68-board band set** (`S/melon_decomp/boards.json`, TOPB2 40 + LIVEC 28, 34 episodes) repeats it through
  `S/sim_hire/ledger_band.py`: `raw_band_off.npz` (edited tree, flag OFF) and `raw_band_on_rowless.npz` (edited tree,
  flag **ON**, against the original row-less tapes) are both equal to `raw_band_base.npz` (frozen pre-edit tree) on all
  14 arrays x 68 rows x 31 days. The second is the `src_hands is None` no-op proved end to end, not only by reading.
  The TOPB3 36 rows include all 6 ymg_aq boards in both seats.
* `S/topledger3/raw_B.npz` is NOT the reference and cannot be: that ledger imports
  `.claude/worktrees/arms-next/src`, whose `sim/units.py` is the older parallel-scatter version and whose `rollout.py`
  has no `prev_mkt_inv`. Same boards, same tapes, same theta, same switches, only the tree differs -> max |money diff|
  **103,249**. Which tree is right is settled in §3: master's sim matches the engine leg 18/18, `raw_B` 3/18.

## 3. Measurement: TOPB3, 18 tapes, sim OFF vs sim ON vs the engine

`S/sim_hire/retain.py raw_off.npz raw_on.npz raw_off_base.npz` -> `S/sim_hire/retain.txt`. RETENTION = mean final coins
of the TAPE seat over the board's two seat rows / `_SOURCE_MONEY` -- `S/topb3/hirefix/retain.py`'s definition, read out
of the sim ledger. `eng` = the engine legs measured in `2026-09-14-tape-hire-fix.md` §4.

| episode | team | src coins | sim OFF | sim ON | eng OFF | eng ON | B margin OFF | B margin ON |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 108790149 | Majkel1337 | 86,556 | 0.23 | 0.83 | 0.23 | 0.83 | +99,820 | +21,964 |
| 108795516 | Majkel1337 | 76,484 | 0.00 | 0.29 | 0.00 | 0.29 | +116,157 | +87,898 |
| 108801472 | Majkel1337 | 101,403 | 0.18 | 0.86 | 0.18 | 0.86 | +105,147 | +23,359 |
| 108807571 | Majkel1337 | 153,246 | 0.20 | 0.28 | 0.20 | 0.28 | +106,040 | +89,834 |
| 108819121 | Majkel1337 | 134,432 | 0.49 | 0.45 | 0.49 | 0.45 | +87,647 | +104,928 |
| 108825010 | Majkel1337 | 98,981 | 0.42 | 0.44 | 0.42 | 0.44 | +82,801 | +77,142 |
| 108790159 | ymg_aq | 81,428 | 1.05 | 1.05 | 1.05 | 1.05 | −14,064 | −14,064 |
| 108806291 | ymg_aq | 118,956 | 1.01 | 1.01 | 1.01 | 1.01 | −9,977 | −9,977 |
| 108807563 | ymg_aq | 129,194 | 1.04 | 1.04 | 1.04 | 1.04 | −15,126 | −15,126 |
| 108814574 | ymg_aq | 111,342 | 0.95 | 0.95 | 0.95 | 0.95 | −7,400 | −7,400 |
| 108820106 | ymg_aq | 70,780 | 1.06 | 1.06 | 1.06 | 1.06 | −12,081 | −12,081 |
| 108826138 | ymg_aq | 116,345 | 1.02 | 1.02 | 1.02 | 1.02 | −23,861 | −23,861 |
| 108741964 | DSM | 114,583 | 0.75 | **0.75** | 0.75 | **0.40** | +30,801 | +30,801 |
| 108751325 | DSM | 109,955 | 0.41 | 0.39 | 0.41 | 0.39 | +84,267 | +87,802 |
| 108784054 | DSM | 104,369 | 0.78 | **0.78** | 0.78 | **0.87** | +30,711 | +30,711 |
| 108790144 | DSM | 108,081 | 0.27 | 1.00 | 0.27 | 1.00 | +97,559 | +916 |
| 108795512 | DSM | 153,242 | 1.00 | 1.00 | 1.00 | 1.00 | −5,682 | −6,018 |
| 108813021 | DSM | 67,008 | 0.68 | **0.75** | 0.68 | **0.80** | +22,263 | +16,087 |

* **Sim vs engine, flag OFF: every one of the 18 B margins is the engine leg's to the coin** (17 exactly, one off by 0.5
  from averaging two seats). Flag ON: 15 of 18. `raw_B.npz` (arms-next tree) matches 3 of 18, max |diff| 124,815 -- the
  sequential `units.py` in master is what makes the tape seat engine-faithful, and a tape ledger cut against that
  worktree is not a reading of the engine.
* **MEASURABLE (sim retention >= 0.95) 7 -> 8 of 18: DSM 1 -> 2, Majkel1337 0 -> 0, ymg_aq 6 -> 6 (unchanged).** The
  gain is 108790144 (0.27 -> 1.00). At the engine's own 0.85 bar it would be 7 -> 10, as §4 of the fix doc reports;
  0.95 is a stricter bar and Majkel1337's best board (0.86) does not clear it.
* Mean retention 0.64 -> 0.78 (Majkel1337 0.25 -> 0.52, DSM 0.65 -> 0.78, ymg_aq 1.02 -> 1.02, every ymg_aq board
  identical to the coin). B margin over all 18: +43,057 (sd 52,725, t +3.46) -> +26,829 (sd 43,401, t +2.62).
* **On the 7 boards measurable both ways: B −12,599 (sd 6,019) OFF -> −12,647 (sd 5,956) ON; paired ON−OFF −48/board
  (sd 127, t −1.00).** The flag does not move the reading on the boards that were already readable -- it adds one.
* 20 of 36 rows change at all; 8 boards are bit-identical ON vs OFF (the 6 ymg_aq, plus 108741964 and 108784054).

## 4. Turning it on in training

Nothing in `es/train.py` changed and no `Config` flag was added: `load_many` -> `stack` -> `device` carry the two new
fields already, and `run_day` reads the module bool. A training run needs both halves -- `KAGG3_TAPE_HIRE_STICKY=1` in
the environment, **and** `--tape-actions` tapes re-cut with `S/sim_hire/build_tapes.py` (an old `.npz` silently stays a
frozen tape). A batch may mix the two: a member without the rows gets an all-zero row and never owes a hire.

## 5. What still desyncs

* Ten boards stay under 0.95, five under 0.5 (108795516 0.29, 108807571 0.28, 108819121 0.45, 108825010 0.44,
  108751325 0.39). The residual is the cash spiral, as in the engine: the re-issue can only buy a hand the seat can
  afford, and on 108795516 it is on 0 coins from day 7. A purse-side repair is UNVERIFIED (the 2026-09-11 `--sticky`
  arm that carried refused BUYs made tapes weaker).
* Majkel1337 still contributes **zero** measurable boards at 0.95, so a sim screen against the rank-1 file is still
  n=0. TOPB3 is not a sim gate yet either.
* A re-issue owed on a turn whose recorded row already fills all 10 market slots is dropped, in the sim and in the
  engine alike (`mlen` maxes at `MO` on every one of the 18 tapes) -- the same truncation the recording lived under.

## 6. The `_MAP` finding (and the engine's unexplained regression)

The three boards where sim ON and engine ON disagree -- 108741964, 108784054, 108813021 -- are all DSM, and on the first
two **the sim's re-issue never fires: every array is bit-identical ON vs OFF**, so on those boards the sim tape seat is
never short of the roster the recording had. Since sim and engine agree to the coin with the flag OFF, the engine's
movement there cannot be the re-issue. It has to be the other half of the engine flag, the half the sim does not carry:
`_MAP` is a *persistent* day-level assignment, so when the live seat lands MORE hires in a turn than the source did, the
surplus live hand is assigned `-1` and PASSes **for the rest of that day** even after the source's own roster grows past
it and its orders exist again. That is a real behaviour change, and it is the natural reading of the fix doc's
"108741964 DSM 0.75 -> 0.40, unexplained -- a real cost of the flag".

So `2026-09-14-tape-hire-fix.md` §2's "`_MAP` provably reduces to the identity on every path the engine can produce" is
**wrong in the one case where the live seat out-hires its source**, which is the case that board is in. Two consequences:

1. The sim and the engine will keep disagreeing on hire-heavy tapes under the flag until one of them changes -- 3 of 18
   boards here. **Recommendation: fix the ENGINE side** (let an unassigned source hand be claimed later in the day
   instead of pinning `-1`), not the sim side; that is also the cheapest explanation of the regression.
2. UNVERIFIED by direct instrumentation of the engine's `_MAP`: deduced from the OFF-identity plus the sim's
   never-firing re-issue. A short probe on 108741964 would settle it.
