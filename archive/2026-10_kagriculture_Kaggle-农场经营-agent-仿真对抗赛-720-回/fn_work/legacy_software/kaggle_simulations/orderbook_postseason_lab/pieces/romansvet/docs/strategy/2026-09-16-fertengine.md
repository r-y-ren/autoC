# FERTENGINE — the 2953+ class's fertilizer edge is TIMING, and it is worth +3,950

2026-09-16 15:05–17:00Z, branch `fertengine` off master `d214bc7`. Step 3 of
`2026-09-16-program-redirect.md`: extract the fertilizer / bought-wheat economy
of the fertilizer-ENGINE class (ENG22, where B is −3,228 / win 36 %) and express
the smallest option as a gene-driven behaviour.

## 1. VERDICT — §115b PASS, the largest in the file

**`FERT_TIMING_ON` / gene `g12` `macro.fert_defer`: POOLED180 +3,950, t +27.23,
47 board flips for and 0 against, on 169 boards.** Bar is +450 at t ≥ 3. Every
leg passes on its own, both kill gates first (ENG22 +1,702 t +4.34, V45LEG
+2,382 t +7.96) and the split is **majority OUR purse** (Δours +1,210 to +1,865
a board against Δtheirs −492 to −1,345), so it is a production lever and not the
denial family `2026-09-16-fertdenial.md` closed.

**What the class actually does differently is WHEN it spends the unit, not how
many it spends.** A FERTILIZE sets `fertilized_until_day = day + 2`
(`kaggriculture.py:481`), so it covers three end-of-days and what it buys
depends entirely on where in the tile's yield cycle it lands. Of our 185.1
applications a game **29 % land on the tile's best day; the engine class lands
91 %** — on the same collection stream, from *fewer* applications.

Two archive premises are corrected below (§2): the class does **not** apply less
fertilizer than us, and it does **not** spend less on bought wheat than us.

## 2. The instrument — 22 ENG22 boards + 5 V45 clones, both seats, real engine

`S/fertengine/probe.py` walks `env.steps`. The public `farms` array carries BOTH
seats' tile grids, so every count here is read off the engine's own state, not
modelled: each unit op with the tile it stood on, each market row with the
inventory it was quoted against, the day-boundary production split, the tile
census. `report.py` prints `ledger_eng22.txt` / `ledger_v45.txt`.

| per game, ENG22 (22 boards) | US | THEM | d |
|---|---:|---:|---:|
| FERT collected / applied | 376.9 / **185.1** | 351.6 / **170.7** | +25.2 / **+14.4** |
| FERT sold / bought (units) | 191.2 / 7.1 | 236.2 / 42.2 | −45.0 / −35.1 |
| WHEAT bought (units / coins) | **156.7 / 5,008** | **242.4 / 8,436** | −85.7 / −3,428 |
| WHEAT sold / planted / FEED ops | 303.6 / 93.5 / **313.0** | 474.0 / 122.7 / **314.2** | −170 / −29 / **−1.2** |
| PLANT / WATER / HARVEST ops | 179.8 / 954.9 / 438.0 | 215.6 / 1,038.8 / 470.0 | −35.8 / −84.0 / −31.9 |
| ongoing prod: FERTILIZED tile-days | **137.5** | **136.6** | +0.9 |
| ongoing prod: UNFERT tile-days | 12.5 | 26.8 | −14.3 |
| one-time in-window WATERs, fertilized | 151.2 (37 %) | 200.9 (48 %) | −49.7 |

* **The class does NOT apply less fertilizer.** `2026-09-11-fertilizer-engine.md`
  read 62 applied to our 190; on the cluster-1 tapes it is **170.7 to our
  185.1** — we apply *more*. Our ongoing fertilized production days already
  **equal** theirs (137.5 vs 136.6). Consistent with the ENG22 doc's own finding
  that the fertilizer coin line is worth ~600 to us, and with `FERT_DUMP`'s bar
  being a local optimum at both signs.
* **The bought-wheat lever is inverted.** `2026-09-11-majkel-vs-spataro.md` says
  the winner is the seat that buys *less* wheat — and against this class **we
  are already the Majkel**: 156.7 units / 5,008 coins to their 242.4 / 8,436,
  with FEED ops identical to 1.2 a game. There is no spend to cut. Ceiling 0.
* **What is left is per-application yield.** Ours 288.7 covered events (137.5
  ongoing fires + 151.2 in-window waters) from 185.1 applications = **1.56**;
  theirs 337.5 from 170.7 = **1.98**.

### 2.1 Where each application lands — the finding

`kaggriculture.py:440` (one-time crop) grants **+2 instead of +1** on each
in-window watering inside the coverage; `:799` does the same per fire for an
ongoing crop. So the best day is exact: for WHEAT (window ages 2–4) it is age 2,
where one unit buys 3; for STRAWBERRY (fires every 2 days) it is the EVE of a
fire, where one unit catches two fires instead of one.

| applications / game (ENG22) | US | THEM |
|---|---:|---:|
| WHEAT before its window (`ONE_EARLY`) | **44.9** | 3.5 |
| WHEAT inside it (`ONE_IN`) | 13.1 | **62.0** |
| CARROT before / inside | **18.3** / 3.5 | 1.0 / **23.7** |
| STRAWBERRY no fire tomorrow (`ONG_MISS`) | **62.4** | 9.1 |
| STRAWBERRY fire-eve (`ONG_HIT`) | 30.2 | **50.5** |
| TOMATO miss / hit | 6.6 / 6.0 | 0.3 / **18.2** |
| **on the best day** | **52.9 (29 %)** | **155.0 (91 %)** |

The V45 clone reads the same way (27 % against 79 %), so this is not an ENG22
artefact — it is the one place our planner is worse than *both* opponent classes.

**Ceiling, our purse, before the two-purse discount:** closing the
per-application gap at our own application count buys ~+78 covered events a game
(1.56 → 1.98 × 185.1). Weighted by what those events actually are — wheat at
~38, carrot ~35, strawberry ~180 before its price impact — **+2,000 … +3,000 a
board on ENG22 and the same on a V45 read.** Over +450 on both, so the box
proceeded to build.

**Why the bar never caught it.** `fert_marginal_value` already prices all of
this exactly and `fert_rank` already orders by it. `fert_cand` is a *bar* test
(`fert_val > price[I_FERT]`), and at a 20–70 coin quote the mediocre day clears
the bar just as the best day does. The site never asks whether the SAME unit on
the SAME tile buys more TOMORROW.

## 3. What was built

`plan.FERT_TIMING_ON` (default **OFF**), `FERT_TIMING_DAYS = 2`,
`FERT_TIMING_MAX = 3`, and the gene **`g12`/`gb12`** → `brain.fert_defer` →
`macro.fert_defer`, decoded `clip(round(FERT_DEFER_GAIN·z), 0, FERT_DEFER_MAX)`
with `FERT_DEFER_GAIN = 16.0`, the `g11` line. 33 params, 7,065 → 7,098.

One addition at the fertilizer site (`plan.py`, after `fert_cand`): a running
maximum of the same `fert_marginal_value` over `day+1 .. day+ft_days`, and

```python
fert_cand = fert_cand & (fert_val >= best)
```

— hold the unit while a later day inside the look-ahead buys strictly more.
`ft_days` is `FERT_TIMING_DAYS` under the switch and `macro.fert_defer`
otherwise, gated by `_static_horizon`, the `FORWARD_ADMIT` idiom: a zero horizon
never builds the projected valuation on the numpy path and is a `where` no-op
under a trace. Nothing downstream needs plumbing (`FERT_DUMP`'s reason):
`n_fert_want` falls, `fert_reserved` falls, `avail[I_FERT]` rises and
`SELL.allocate` sells the deferred unit — it is spent later or sold, never lost.

`tests/test_fertengine.py` (16, pass): whole-plan sha256 OFF-identity on six
boards against a pristine `git archive d214bc7 src` subprocess; `DAYS = 0` and
`fert_defer = 0` each re-evaluate to OFF on every board; the strawberry fire-eve
is kept and the day-early one deferred; wheat waits for age 2; TOMATO (a daily
fire) is never deferred; the deferred units are SOLD and no other product moves;
the gene alone drives the gate with the switch OFF; monotone in days; the
shipped theta decodes 0 on 200 recorded boards; the ES slope at sigma 0.02 sits
in the `g11` band (median 15–35 % of 512 members move, mode still 0); a short
theta pads; `jit == numpy`, one traced program for horizons 0, 1 and 2.
`policy.init_theta` zeroes `g12` (a 2-D block would otherwise be He-scaled),
`test_crop_day.py::test_layout_offsets` re-pinned to the new tail, and four
`_macro` helpers name `fert_defer` only when the planner has the field, because
the digest pin runs them against a pre-`g12` tree.

## 4. The legs — paired against the banked shipped pair

CTL = `S/lossflip/c2_combo_*` (LOT4_ON, LOT4_TURN 17, SELL_SLOT_PRIORITY_ON),
legitimate because OFF is master to the byte — and **verified, not assumed**: a
fresh OFF run of this worktree on ENG22 (`S/lossflip/fe_ctl_eng22.csv`,
17:15–17:17Z) is identical to the banked control on every seed / opponent / seat
/ purse column, so every increment below is a pure switch difference on one
tree. Kill gates first: +100 and t ≥ 2.

| arm | ENG22 (44 games / 22 boards) | V45LEG (60 / 30) | flips |
|---|---:|---:|---|
| `ft1` DAYS=1 | +34 (t +0.19) | not run | +0/−1 |
| **`ft2` DAYS=2** | **+1,702 (t +4.34)** | **+2,382 (t +7.96)** | +0/−1, +1/−0 |
| `ft3` DAYS=3 | +1,702 (t +4.34) | not run | +0/−1 |

`ft3` is `ft2` to the coin: nothing on a real board peaks more than two days out,
which is what `FERT_TIMING_MAX = 3` bounds. `ft1` is level because the gate is a strict
comparison and STRAWBERRY — the expensive crop, and 62.4 of our 92.6 misplaced
ongoing applications — hits a TIE at one day out: two days before a fire, today
and tomorrow both catch exactly one fire (`day+1..day+3` and `day+2..day+4` each
hold the single fire at `day+3`), and only the day AFTER that catches two. So a
one-day look-ahead spends the unit and a two-day one holds it. WHEAT rises
strictly (1 → 2 → 3 units at ages 0/1/2) and is caught by either. **Only `ft2` was pooled.**

| §115b leg (`ft2`) | boards | Δmargin | t | W/L |
|---|---:|---:|---:|---|
| LIVEC-H30 | 30 | +3,980 | +12.51 | 14/0 |
| LIVEC-H30B | 30 | +3,924 | +12.13 | 4/0 |
| NEXT30 | 30 | +3,539 | +10.77 | 11/0 |
| POOLED BAND (90) | 90 | +3,814 | +20.53 | 29/0 |
| BAND180 | 79 | +4,104 | +18.08 | 18/0 |
| **POOLED180** | **169** | **+3,950** | **+27.23** | **47/0** |

**§115b: PASS.** Two-purse split, per board: ENG22 Δours **+1,210** / Δtheirs
−492; V45LEG +1,264 / −1,119; BAND180 +1,500 / −1,345; LIVEC-H30 +1,668 / −901;
LIVEC-H30B +1,865 / −911. **55–71 % of every leg is our own purse** — the
opposite signature to `FERT_VOLUME` (58–85 % denial, never promoted) and to the
whole market-denial family. The ENG22 board win rate falls 45.5 → 40.9 % on one
flipped board while the margin rises 1,702: this class is won by coins, not by
board count, and 47 boards flip our way across the pool against 0 the other way.

## 5. Standing

* **`FERT_TIMING_ON` is the first lever to clear §115b by an order of
  magnitude** (previous best: LOT4@17, +791 t 13.19). It should be shipped as
  `FERT_TIMING_ON=True,FERT_TIMING_DAYS=2` on top of the pair, and the gene
  `g12` left for the ES restart to tune per board rather than per season.
* **CORRECTED, do not re-derive:** the 2953+ class does not apply less
  fertilizer (170.7 to our 185.1) and does not buy less wheat (242.4 to our
  156.7). Both premises in the 2026-09-11 fertilizer/Majkel documents point the
  wrong way on this population. Its edge is 91 % best-day placement.
* **OPEN, and now cheap:** the same "is today the best day" question applies to
  CARE (the care bonus is consumed only on a fed production day,
  `kaggriculture.py:827`) and to HARVEST timing. `S/fertengine/probe.py`
  measures both without a new run.
* `S/fertengine/`: `run_all.sh` (`instrument` | `eng22` | `v45` | `pool <arm>`),
  `probe.py`, `report.py`, `ledger_eng22.txt`, `ledger_v45.txt`, `raw/` (27
  board json), leg csvs `ft1_* ft2_* ft3_*`.
