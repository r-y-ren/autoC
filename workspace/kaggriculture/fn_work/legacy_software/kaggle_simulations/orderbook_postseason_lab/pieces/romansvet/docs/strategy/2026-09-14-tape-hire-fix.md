# TOPB3 tape desync: the refused HIRE, and the `--hire-sticky` repair

Answers `docs/strategy/2026-09-14-topb3-leg.md` §3/§6. Built and measured 2026-09-14 08:00-09:00Z. **Headline: the defect is the
SHORT roster, not a shifted hand index. `--hire-sticky` lifts Majkel1337 retention 0.25 -> 0.52 and DSM 0.65 -> 0.74, grows the
fidelity-retained TOPB3 set 7 -> 10 boards (Majkel1337 0 -> 1), and is a bit-exact no-op on every board that already retained.**

## 1. Diagnosis

Instrumented on the worst board -- episode 108795516 (Majkel1337, retention 0.00), board index 1 of `S/topb3/ids.txt`, seed
1341060238, seat 0, B = `submission/theta.npy` -- with `S/topb3/hirefix/probe.py <leg replay> S/topb3/replays/ep_108795516.json`
(leg replay from `eval_vs_baselines.py --replay-dir`). Engine facts, `kaggle_environments` 1.32.7,
`envs/kaggriculture/kaggriculture.py` (sha256 `bc8a5487...` = `vendor/engine.lock.json`):

* `_do_hire` (:702-708) is `cost = mult * _fib(hires_today)`, then `if farm["money"] < cost: return` -- an unaffordable HIRE is
  dropped **in silence** and `hires_today` is **not** incremented.
* HIRE is an *atomic market order* (:571-580), one hire per market-queue index, queue truncated to `maxMarketOrdersPerTurn` (:560)
  first. `hands` is append-only inside a day and **wiped every night** (`_end_of_day`, :880-882), so a source hand index is exactly
  "the i-th hire that landed today".
* Hand identity is **positional**: `hands[idx - 1]`, an `[x, y]` tile, no name or id; a tape action's hand reference is the index
  into its own `hands` list, matched to the roster by `_align`.
* **An over-long `hands` list is NOT rejected.** `_apply_unit_action` (:907) runs per unit and returns at once when
  `_farmer_position` is None (:282): a silent per-unit no-op. The claim in `scripts/tape_opponent.py`'s docstring and in the leg doc
  -- "the engine rejects a whole action whose `hands` list is longer than the farm's" -- is **wrong for this engine**; corrected
  here.

Probe output on 108795516 (`step, day.hour, HIREs submitted, hands gained, cash here vs cash in the source at the same step`),
abridged:

```
step  d  h  HIREs got  cash_here  cash_src  roster
  24  1  0      8   3          4         7   0->3   <== FIRST REFUSED ACTION (type HIRE)
 168  7  0      8   0          0       414   0->0
 216  9  0      8   7         50      1827   0->7
 504 21  0      8   0          0     48301   0->0
```
* **First refusal: step 24 (day 1 hour 0)**, HIRE, 8 submitted / 3 landed, tape-seat cash **4** here vs **7** in the source at that
  step.
* **Subsequently illegal actions: 0.** Nothing becomes illegal; the damage is a cash spiral. A 3-hand crew instead of 4 does less
  work and earns less, and by day 7 the seat is on **0 coins** (source 414) and hires nothing on days 7, 8 and 21-23. Final coins 0
  vs 76,484. Per-day roster ours vs source: `4,3,5,6,6,6,8,0,0,7,8,11,...` vs `4,4,6,6,6,6,8,9,9,10,11,11,...`.
* The index shift is real but rare and second-order (day 15: 2 of 8 hires land at hour 0, 3 more at hour 1, so positionally-aligned
  live hand 2 is really the source's hand 8).

**Corollary that decides the design:** the source episode *also* had HIREs refused (8 submitted at step 24, 4 landed -- this file
over-submits and lets the fib cost ladder stop it), so a blind re-issue would buy hands the recorded player never had. The re-issue
must be **capped at the source's own roster**, which the tape already carries: `len(_TAPE[s]["hands"])` equals the source seat's
roster on **719/719 steps** of 108795516, checked against the ListEpisodes dump.

## 2. The flag

`scripts/tape_opponent.py --hire-sticky` bakes `_HIRE_STICKY_DEFAULT = True` into the emitted package; `TAPE_HIRE_STICKY=0/1` wins
at run time (no `KAGG3_` prefix on purpose -- `eval_vs_baselines._vendored_imports` clears that namespace for file agents). Default
**OFF**. Semantics, per step, under the flag:

1. `_SRC_HANDS[s] = len(_TAPE[s]["hands"])` is the source roster at step `s`.
2. `_MAP[j]` = source hand index for live hand `j`. When the roster grows by `g`, the `g` new slots are filled from `owed + [new
   source indices]`, lowest source index first; the rest becomes `owed`. A live hand with no source hand left to impersonate maps to
   `-1`.
3. Hand orders are read at `_MAP[j]`, **not** at `j`; an unresolvable reference emits `["PASS"]` for **that hand only** -- the
   farmer and market halves of the turn are untouched.
4. The tape's own market list stays **byte-identical** (queue order and the `maxMarketOrdersPerTurn` truncation are part of the
   recording). `["HIRE"]` is **appended behind it**, once per owed hand, capped at `_SRC_HANDS[s + 1] - live`: the roster can never
   overshoot the source's, and the re-issue sits behind this turn's SELLs, the cash that pays for it.
5. `owed`/`_MAP` clear at the day boundary (`step % turnsPerDay == 0`) -- a hire deferred past midnight is a different hire -- and
   the whole state resets whenever the step does not follow the last one (one module image per worker replays many games).

Because source hires only ever append and an owed hand is filled from the lowest unassigned source index, **`_MAP` provably reduces
to the identity on every path the engine can produce**: the existing `_align` truncation was already the right hand-identity
assignment. It is kept explicit because it makes "source index" the addressing scheme, and turns an unresolvable reference into one
PASS instead of a wrong order. **The measurable lever is the deferred hire, not the remap.** -- said here so nobody credits the
wrong half.

`--from-main` re-cuts an existing package in the new mode with no replay, carrying `_TAPE`, `_TOWN` and provenance over; it refuses
to write unless `verify_frozen_match` proves the new file, flag off, equals the old one at **every step x every roster size 0..14**
(10,815 pairs/tape). `verify()` forces the flag off.

## 3. Test output

`.venv/bin/python -m pytest tests/test_tape_hire_sticky.py -q` -> `........... [100%]` (11 tests). Covered: flag-off equivalence
both directions; `TAPE_HIRE_STICKY=0` beating a baked `True`; source roster recovery; owed hire re-issued and appended (not
prepended) behind the SELLs; stops when the roster matches; never overshoots; dropped at the day boundary; hands addressed by source
index; **unresolvable hand reference PASSes and the rest of the turn survives**; new-episode reset; past-the-end PASS. Each of the
48 packages below was written only after its own `verify_frozen_match` returned 0 (`S/topb3/hirefix/recut.log`, 48/48
`frozen-identical`).

## 4. Measurement: TOPB3, 18 tapes, flag OFF vs ON

Same leg, seeds, town registry, theta (`submission/theta.npy` = flow193_g100_hr, md5 7fcf3948) and switches. OFF =
`S/lossflip/topb3_B.csv` (the leg doc's §4 baseline, shipped `artifacts/panel_opp_town/` packages); ON =
`S/lossflip/topb3_Bhire.csv`, the same 18 tapes re-cut with `--hire-sticky` into `S/topb3/hirefix/tapes/`, run by
`S/topb3/hirefix/run_topb3_on.sh`, `WORKERS=4`, 36 rows, 96 s. Table: `S/topb3/hirefix/retain.py S/topb3/ids.txt <off> <on>`.

| episode | team | src coins | ret OFF | ret ON | B margin OFF | B margin ON |
|---|---|---:|---:|---:|---:|---:|
| 108790149 | Majkel1337 | 86,556 | 0.23 | **0.83** | +99,820 | +21,964 |
| 108795516 | Majkel1337 | 76,484 | 0.00 | 0.29 | +116,157 | +87,898 |
| 108801472 | Majkel1337 | 101,403 | 0.18 | **0.86** | +105,147 | +23,359 |
| 108807571 | Majkel1337 | 153,246 | 0.20 | 0.28 | +106,040 | +89,834 |
| 108819121 | Majkel1337 | 134,432 | 0.49 | 0.45 | +87,647 | +104,928 |
| 108825010 | Majkel1337 | 98,981 | 0.42 | 0.44 | +82,801 | +77,142 |
| ymg_aq x6 | 108790159 / 108806291 / 108807563 / 108814574 / 108820106 / 108826138 | — | 1.05 / 1.01 / 1.04 / 0.95 / 1.06 / 1.02 | **same** | −14,064 / −9,977 / −15,126 / −7,400 / −12,081 / −23,861 | **same** |
| 108741964 | DSM | 114,583 | 0.75 | **0.40** | +30,801 | +106,932 |
| 108751325 | DSM | 109,955 | 0.41 | 0.39 | +84,267 | +87,802 |
| 108784054 | DSM | 104,369 | 0.78 | **0.87** | +30,711 | +10,412 |
| 108790144 | DSM | 108,081 | 0.27 | **1.00** | +97,559 | +916 |
| 108795512 | DSM | 153,242 | 1.00 | 1.00 | −5,682 | −6,018 |
| 108813021 | DSM | 67,008 | 0.68 | 0.80 | +22,263 | +12,129 |

Per file: Majkel1337 0.25 -> **0.52** (B +99,602 -> +67,521); DSM 0.65 -> **0.74** (+43,320 -> +35,362); ymg_aq 1.02 -> 1.02,
**every board identical to the coin** (−13,751 both ways).

* All 18: retention 0.64 -> 0.76; B margin +43,057 (t +3.46) -> **+29,711 (sd 47,668, t +2.64)**.
* Paired ON−OFF, 18 boards: B margin **−13,346/board** (sd 39,556, t −1.43), B coins −2,040/board (t −0.69) -- the tape gets
  stronger, B's own coins barely move.
* **Fidelity-retained set (>= 0.85) grows 7 -> 10 boards** (`S/topb3/retention.py`): ON adds 108801472 (the first retained
  Majkel1337 board), 108784054 and 108790144 (DSM). B there: OFF 7 boards, 0.0 % win, −12,599 (t −5.54); **ON 10 boards, 30.0 % win,
  −5,384 (sd 13,733, t −1.24)**. Paired on the 7 retained under both flags: −48/board, t −1.00. 12 of 36 games coin-identical OFF vs
  ON.

**Not fixed.** Five boards stay under 0.5 (108795516 0.29, 108807571 0.28, 108819121 0.45, 108825010 0.44, 108751325 0.39) and one
regresses (108741964 DSM 0.75 -> 0.40, unexplained -- a real cost of the flag, UNVERIFIED). The re-issue can only buy a hand the
seat can *afford*: on 108795516 the seat has 0 coins from day 7, so the owed hire never clears. The residual is the cash spiral,
which a hire reflex cannot undo -- UNVERIFIED whether a purse-side repair would (the 2026-09-11 `--sticky` arm that carried refused
BUYs made tapes *weaker*).

## 5. Non-regression: NEXTHIGH, 30 tapes, flag ON

Same protocol, `S/topb3/hirefix/run_nexthigh_on.sh`, 60 rows, `S/lossflip/nexthigh_Bhire.csv` vs the `nexthigh_B.csv` baseline.

* Retention **0.99 -> 0.99**; every board unchanged to 2 d.p. B mean margin **+2,045 -> +2,045** (sd 8,860 -> 8,858, t +1.26 both
  ways), leg win 53.3 % both ways.
* Paired ON−OFF: B coins **−7/board** (sd 37, t −1.00), B margin +1/board -- **well inside the < 200/board bar**. 54 of 60 games
  coin-identical; only 3 of 30 boards move at all, and the largest single-board move in B's coins is **−204** (108043365).
* **Flag-off control, end to end:** the 18 `--hire-sticky` packages re-run with `TAPE_HIRE_STICKY=0`
  (`S/lossflip/topb3_Boffctl.csv`) are **36 of 36 games coin-identical to `topb3_B.csv`**, leg mean margin +43,057 -- the
  number the leg doc quotes. The flag-off path is identical in the engine, not only in the 10,815-pair sweep.

## 6. Status and what is left

* Nothing in `artifacts/panel_opp_town/` was touched; the ON packages live in `S/topb3/hirefix/tapes/` and no judge leg points at
  them. `S/autojudge/watch.sh`, `S/unitorder/judge_family_inventory_20260913.json` and `S/topb3/inventory_entry.json` untouched.
  New: `S/topb3/hirefix/{probe.py,recut.sh,recut.log,retain.py, run_topb3_on.sh,run_nexthigh_on.sh,legs.log}`.
* The 48 packages were cut before two docstring paragraphs in the template were corrected (§1) -- comment text only, but a re-cut
  produces different bytes, so **re-cut before promoting**.
* TOPB3 is still not a promotion gate: 8 of 18 boards stay below 0.85 and Majkel1337 contributes one retained board, so B vs the
  rank-1 file is n=1 -- UNVERIFIED.
* Open: the 108741964 regression; whether a purse-side repair lifts the five boards under 0.5; the sim seat (`es.tape_actions`, a
  static day table in the jitted rollout) does NOT carry this reflex, so a sim screen and an engine leg now disagree on a hire-heavy
  tape under the flag.
