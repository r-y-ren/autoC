# FERTRESERVE — holding fertilizer back hands the rival 17,556 coins

2026-09-16 12:55–13:45Z, branch `fertreserve`. Mechanism #3 of
`2026-09-16-nbintel2.md` §6 (`_r85_fertilizer`, `2026-09-16-v45-notebook.md`
§2.7). The public notebook was read for MECHANICS only; every line here is ours.

## 1. VERDICT

1. **Step 0, the `_r148_atomic` audit: ZERO.** Over 5 real-engine boards /
   3,600 turns our seat never requested more PLANTs of a crop than it held seeds
   for (`probe.py` applies the engine's test, `kaggriculture.py:920-931`, to our
   emitted action dict and the private seed bag). Seeds are bought in the turn-1
   BUY row against the same plan that emits the PLANTs, so the two cannot
   disagree. **Row CLOSED.**
2. **`FERT_RESERVE_ON` built, measured, REJECTED at the ENG22 kill gate, both
   ends.** Increment over the shipped pair: **−32,709 (t −7.45)** with the herd's
   supply netted off, **−48,134 (t −12.28)** in the literal V45 form
   (`FERT_RESERVE_SUPPLY_NUM = 0`). Bar +100, t ≥ 2. **0 of 44 games won, 10
   board flips against, 0 for.** No POOLED180 run, none warranted.
3. **The instrument says why, and it is not the fertilizer revenue.** Our purse
   barely moves (−3,968); the **RIVAL's purse rises +17,556**. Our 218-unit
   fertilizer dump is not a revenue stream, it is a **price-denial instrument
   against the fertilizer-ENGINE class** — the class ENG22 is drawn from. §3.
4. **The fertilizer-hold family is closed at both ends** — price floor
   (`FERT_FLOOR_ON`, −4,890 t −13.01) and now the quantity reserve. §4.

## 2. What was built

`FERT_RESERVE_ON` (default **OFF**), `FERT_RESERVE_DAYS = 3` (fertilizer's own
coverage window), `FERT_RESERVE_SUPPLY_NUM/DEN = 1/1`. `_fert_future_reserve`
walks `day+1 .. day+DAYS` **backwards**,
`R(last+1) = 0`, `R(k) = max(demand(k) - supply(k) + R(k+1), 0)`.
`demand(k)` = standing plant tiles whose coverage has lapsed by `k`, on the
three-day cycle `fertilized_until_day = day + 2` sets, still standing on `k`
(one-time crops to `t_day + harvest_age`, ongoing to `pay_day`); tiles the day
fertilizes carry `day + 2`. `supply(k)` = the herd's free unit a day — the engine
re-arms **every** animal's `fertilizer_available` at **every** end of day
(`kaggriculture.py:831`). `R(day+1)` joins `n_fert_eff` at the one site that
decides what the lots may draw on; the provisional lot-1 pass takes the same
reserve with an all-false mask, keeping its revenue a lower bound (BUY_LAND safe).

`tests/test_fertreserve.py` (14, pass): whole-plan sha256 OFF-identity on 5 boards
against a pristine `git archive 4054968 src` subprocess; the helper never entered
OFF; seven recurrence properties; ON moves fertilizer units and **no other
product's**; the terminal day voids it; `jit == numpy` on the whole plan.

## 3. The instrument — 5 ENG22 boards, our seat, ON against OFF, real engine,
paired board for board (`S/fertreserve/instrument.csv`)

| per game | OFF | ON | d |
|---|---:|---:|---:|
| fertilizer units SOLD | 218.4 | 111.4 | **−107.0** |
| coins per unit sold | 59.5 | 68.7 | +9.2 |
| units BOUGHT back | 8.4 | 2.0 | −6.4 |
| FERTILIZE ops that found a unit | 182.6 | **165.4** | **−17.2** |
| FERTILIZE ops starved of one | 0.8 | 0.0 | −0.8 |
| COLLECT_FERTILIZER units taken | 401.4 | 282.0 | −119.4 |
| fertilizer quote, day 13 / day 25 | 69.8 / 36.8 | 74.6 / **53.0** | +4.8 / **+16.2** |
| OUR coins | 112,643 | 108,675 | −3,968 |
| **THEIR coins** | 106,536 | **124,091** | **+17,556** |
| margin | +6,108 | −15,416 | −21,524 |

Only the first line was the hypothesis.* **The surface it was built for is worth nothing.** It saves **0.8 applications
  a game** (913 of 917 already find their unit), and the 8.4 bought units cost
  63.6 against a mean sale of 59.5 — on a quote with **no town drain**, which
  only walks *down* (100 at d2 → 70 at d13 → 37 at d25). Holding to avoid a
  later buy is selling high to save low, backwards.
* **Self-defeating on its own objective**: applications that fire fall 183 → 165.
  A reserved shed is a shed the crew stops collecting into (401 → 282) — the
  100-unit cap that killed `TOMATO_HOLD` and `FERT_FLOOR`.
* **The real channel is DENIAL.** Theirs +17,556 against our −3,968: ENG22 sells
  fertilizer, and our dump collapsed the quote they sell into. A lever costing us
  4k and paying them 18k reads as "+9.2 coins a unit" in any own-row ledger.

## 4. Standing

* `FERT_RESERVE_ON` ships **OFF** and stays: the measured answer to a question the
  V45 layer list will provoke again. Master `src` is byte-identical OFF.
* **CLOSED**: fertilizer-hold, both ends. Do not reopen on a ledger read.* **OPEN, the only direction this leg leaves — the opposite sign.** Our dump is
  worth ~17.5k of the engine class's purse and dumping *harder* (selling into
  today's reservation, or buying to dump) has never been priced. A new family,
  market denial not sale timing; it needs its own instrument first.
* `S/fertreserve/`: `run_all.sh`, `probe.py`, `report.py`, `instrument.csv`,
  `fr_on_eng22.csv`, `fr_nosup_eng22.csv`. CTL = banked
  `S/lossflip/c2_combo_eng22.csv`, legitimate because OFF is master.
