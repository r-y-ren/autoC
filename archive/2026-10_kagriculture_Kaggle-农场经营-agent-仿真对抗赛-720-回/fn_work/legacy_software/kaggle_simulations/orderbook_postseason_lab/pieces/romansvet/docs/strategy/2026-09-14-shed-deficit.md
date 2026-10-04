# 2026-09-14 — SHED-DEFICIT: the overflow projection's missing watering bonus

**VERDICT: the defect is REAL and the fix is EXACT, and it BUYS NOTHING —
REJECTED, and the "size the forced sale better" family is CLOSED.** The
projection `plan.py` uses to guard the shed door does under-count tonight's
inflow by two units per tile that waters and harvests on one chain (unit test
below: on a board with eight such tiles the ask grows by exactly 16). Paired
CRN on 80 game-seats, theta B `flow193_g100_hr` with the shipped `hr`
switches, the corrected term is **-30 coins on the 68 band boards (t -1.23),
margin -82 (t -2.60), and it hands the opponent +52 (t +2.51)** — the 68-band
pooled Δcoins is **far below the +450 / t ≥ 2 promotion bar and the margin is
significantly NEGATIVE**. It does not recover units either: destroyed units a
game-seat go **21.62 → 21.84 (+0.22, t +0.67)** on the band and 24.58 → 24.50
on ymg_aq. The whole effect is **+0.81 units a game-seat sold (t +2.08) at a
realised whole-book price of 91.45 → 91.39** — hour-0 stock dumped a little
cheaper, out of a shed the night refills anyway.

Sim, descriptive, paired-CRN board sets, action-replay opponent seat. No engine
game, no training arm, no ladder claim. `SHED_DEFICIT_ON` ships **default off**
and OFF is the shipped program byte for byte.

## 1. MECHANISM — the defect, and why correcting it cannot pay

| what | file:line |
|---|---|
| the guard | `plan.py:7547-7558` the forced sale: `proj_eod = shed - s_qty - picks_out + buys_in + inflow`, `deficit = max(proj_eod - SHED_CAPACITY, 0)` |
| **the defect** | `plan.py:7552-7553` `inflow` sums `view.t_yield` — the *pre-watering* yield, explicitly ("today's watering bonuses excluded", `:7534`) |
| the term the file already spells | `plan.py:7733` `bl_units = where(bank_mask & has_harv, view.t_yield + 2 * bl_w, 0)`, `bl_w = any(chain_op == OP_WATER)`; the same term again at `:7651` (`MELON_OPEN`) and `:7690` (`MIDDAY_PLACE_V2`) |
| why the chain earns it | `plan.py:6285-6291` the chain-order comment (`:6290`): FERTILIZE before WATER, **WATER before HARVEST ("watering still adds yield on the harvest day")** |
| the fix, ON | `plan.py:7548-7551` `sd_yield = view.t_yield + 2 * sd_w`, one boolean per tile, nothing else |
| **the constraint that eats it** | `plan.py:7580` `spare = max(avail - s_qty, 0)` — the forced sale may draw ONLY on hour-0 stock net of the day's reservations and net of the voluntary sale |
| what actually dies | `sim/eod.py:238-245` — tonight's **inflow**, which lands after the last lot (`early_lot_turns()` turn 18) has already resolved |

**The ask grows; the sale cannot.** `deficit` is an *ask*, and the greedy under
it spends that ask out of `spare`. Two measurements bound `spare` at ~zero on
exactly the days that clip:

1. SHED-CLIP §4(a) measured `shed - used - s_qty - forced` and found it **empty
   in practice** — "the first pass has already drained every product it was
   allowed to touch". Asking for more from an empty purse returns nothing.
2. The day already offers nearly the whole shed. Units sold that day against the
   dawn shed, our seat, 68 band boards, B OFF (`raw_melOFF.npz`):

| day | 15 | 17 | 19 | 21 | 23 | 25 | 27 | 28 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dawn shed | 88.6 | 84.8 | 87.6 | 85.8 | 86.8 | 85.9 | 95.0 | 92.2 |
| sold that day | 58.0 | 61.7 | 65.1 | 69.9 | 63.0 | 65.3 | 74.8 | 79.9 |
| fraction | 0.65 | 0.73 | 0.74 | 0.81 | 0.73 | 0.76 | 0.79 | **0.87** |

   The ~20-unit residue is feed wheat and fertilizer the day's own tasks have
   reserved — `avail` is already net of it, so `spare` cannot reach it either.

So the corrected ask converts into **+0.81 units a game-seat over a whole
30-day season** (t +2.08) — two orders below the 2-units-per-watered-harvest
the term adds to the ask on a day that reaches 15-25 harvest tiles. And those
0.81 units come out of *hour-0 stock at the day's cheapest marginal quote*,
while the units that die are *tonight's inflow*, which no row of today can
reach. Hence: coins down, opponent up, clip unchanged.

## 2. PAIRED — every set, both subsets

Baselines are the stored OFF raws (`raw_headOFF.npz`, `raw_melOFF.npz`); the
identity leg proves the edited tree reproduces them exactly.

| set | our coins Δ (t) | margin Δ (t) | THEIR coins Δ (t) | win % B → arm | flips | units sold Δ (t) |
|---|---:|---:|---:|---:|---:|---:|
| IDENTITY (edited src OFF, 12 ymg_aq) | **+0** (—) | +0 | +0 | 0.0 → 0.0 | 0 | +0.00 |
| 12 ymg_aq | **-4** (-0.41) | -13 (-0.96) | +9 (+1.79) | 0.0 → 0.0 | 0 | +0.17 (+1.48) |
| **68 band** | **-30 (-1.23)** | **-82 (-2.60)** | **+52 (+2.51)** | 42.6 → 39.7 | **2 (both to them)** | +0.81 (+2.08) |
| 40 TOPB2 | -8 (-0.33) | -67 (-1.86) | +58 (+1.74) | 32.5 → 27.5 | 2 (both to them) | +1.02 (+1.96) |
| 28 LIVE-C | -61 (-1.29) | -104 (-1.81) | +43 (+2.59) | 57.1 → 57.1 | 0 | +0.50 (+0.86) |

**The 68-band pooled Δcoins is -30 with t -1.23 — it does NOT clear +450 / t ≥ 2.**
The only significant readings in the table are against us: margin -82 (t -2.60)
and their coins +52 (t +2.51) on the band. Selling a handful of extra units at
the cheapest marginal quote leaves that much more on the shared shelf, which the
action-replay seat then buys and sells at a better price (`KAGGLE-POPULATION`'s
shared pot).

## 3. UNITS RECOVERED — none (`S/shed_clip/instrument.py`, ON vs OFF)

Per game-seat, dawn-quote pricing, both seats, same CRN boards:

| set | seat | leg | DROP u | nightfall u | total u | coins @dawn |
|---|---|---|---:|---:|---:|---:|
| 68 band | us | B (off) | 6.25 | 15.37 | **21.62** | 1,718 |
| 68 band | us | SHED_DEFICIT | 6.26 | 15.57 | **21.84** | 1,691 |
| 12 ymg_aq | us | B (off) | 2.67 | 21.92 | **24.58** | 1,816 |
| 12 ymg_aq | us | SHED_DEFICIT | 2.75 | 21.75 | **24.50** | 1,810 |
| 68 band | them | either | 0.07 | 4.34 | 4.41 | 169 |

Paired, our seat: band **+0.22 u (sd 2.72, t +0.67)**, TOPB2 +0.07 (t +0.15),
LIVE-C +0.43 (t +1.21), ymg_aq -0.08 (t -0.56). The opponent's clip is
identical to the unit on every board — the arm never touches their seat's plan,
which is the paired harness working as designed. The day profile moves a few
tenths between d21-d27 and back; it is noise of the same size as the effect.

**Read plainly: of the 15.4 units the night destroys on the band, the corrected
projection recovers zero.** The nightfall clip is not a projection error at all
— it is the day's own harvest arriving after the last market row, into a shed
whose sellable stock the planner has already put on a row.

## 4. WHAT WAS BUILT

| file | what |
|---|---|
| `src/kagg3/core/plan.py:567-603` | `SHED_DEFICIT_ON = False` + the rationale, beside `SHED_OVERFLOW_ON` |
| `src/kagg3/core/plan.py:7548-7552` | the body: `sd_yield = view.t_yield + 2 * sd_w` inside `inflow`, Python-level `if`, so OFF the expression is `view.t_yield` unchanged |
| `tests/test_shed_deficit.py` | 8 tests: OFF is the default; OFF whole-plan digests on four boards against a pristine `git archive HEAD src` subprocess; the pin board really waters before it harvests; ON adds exactly 2 units of forced sale per watered-harvest tile (16 on 8 tiles); ON is inert where the bonus cannot apply (no overflow / already watered / no plants); `deficit` never negative and the sale never exceeds the dawn shed over a 18-board sweep |
| `S/shed_deficit/launch.sh` | the five legs (ON ymg, ON band, OFF identity, and the SHED-CLIP census re-run ON on both sets) |
| `S/shed_deficit/clip_cmp.py` | destroyed units ON vs OFF from two `S/shed_clip` raws, paired, with `--subset` |
| `S/shed_deficit/report.sh`, `report.md` | every table above |
| `S/macro_exec/raw_sheddef_ymg.npz`, `raw_sheddef_band.npz`, `raw_sheddef_ident.npz` | the paired raws |
| `S/shed_clip/raw_sd_ymg.npz`, `raw_sd_band.npz` | the clip census ON |
| `S/shed_deficit/*.log` | the run logs (456-517 s, five legs in parallel on CPU) |

OFF identity: `tests/test_macro_exec.py test_rebuy.py test_prestock_v2.py
test_lot_split.py test_route_freefirst.py` = **56 passed**, plus
`tests/test_shed_deficit.py` = 8 passed. The identity leg in §2 is the same
claim at sim level: max |delta| 0 on every recorded array, 12 boards.

## 5. NEXT

**Not built: `SHED_D29_ROW_ON`** (a day-29 sell row at turn ~15). It was the
optional second half of this box and it is not worth the build. SHED-CLIP §4(b)
bounded it at **446 coins (band) / 130 (ymg)** — below the promotion bar on its
own before the ~6 % training-throughput cost of an extra resolved turn on every
day of the season, and §3 above has now shown that the family's other candidate
recovers nothing, so the bound is the optimistic end of a family with a zero in
it. Anyone who runs it should run it as a **day-29-only** row and price the
throughput separately.

**What this closes.** Both planner-side repairs to the shed door are now
measured and both are zeros: `SHED_OVERFLOW_ON` recovers 0.10 units a board
(SHED-CLIP §4a) and `SHED_DEFICIT_ON` recovers -0.22. The forced sale cannot be
the lever, because it draws on hour-0 stock that is already fully offered while
the units that die are tonight's inflow. **Close "size the forced sale better".**

**What is still open, in order.**

1. **A row AFTER the harvest lands.** The engine resolves a market every turn;
   we resolve three (`early_lot_turns()` 3/10/18) and the harvest of d15-28
   lands across the afternoon. This is the only lever that can reach the units
   that die — and unlike the day-29 row it applies to 14 days, not one, so its
   bound is the whole 1,272-coin band nightfall clip rather than 446. Price a
   fourth lot turn against its throughput before building it.
2. **Carry less into the night.** The residue the day does not sell is feed
   wheat and fertilizer reserved for tasks (§1's 20-unit gap). A reservation
   that the route will not reach is stock that can only die; `SHED_OVERFLOW_ON`
   tried to give it back to the SALE and found it empty, but nobody has tried
   not to *reserve* it — that is a `want_feed` / `n_fert_eff` question, not a
   sale question.
3. Leave the day-29 DROP alone. SHED-CLIP already showed the binding constraint
   there is total capacity (103.6 units offered into 100), not order.
