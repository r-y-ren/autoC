# CROPFORMULA — how the shipped FT2 agent picks which crops to plant

2026-09-17. Source-cited, end to end, plus 20 instrumented engine-class boards.
Data: `S/cropformula/graphs.json` (collector `S/cropformula/collect.py`, softmax
probe `S/cropformula/probe_softmax.py`). No source was changed; every hook is a
runtime monkeypatch inside the measurement process.

## 0. The one-paragraph answer

FT2 has **no crop-selection rule written in code**. It has a *learned score per
crop* (`grow`), a softmax over it whose sharpness is also learned, and then two
**hard engine masks** — "can it ripen in time" and "is the market already
oversupplied" — after which the day's development budget is split by largest
remainder. Everything downstream (`plan.py`) is *clipping and placement*, not
choice: tiles, then seed coins, then labour. The shipped theta is **6,789
params**, which is **shorter than `PO.offset("cm") = 6,855`**, so the entire
`crop_mix` / `CROP_DAY` / `MELON` gene branch (`brain.py:1105-1123`) is **not
taken** — the two `brain.*` switches in the shipped judge string
(`brain.MELON_GENE_ON`, `brain.CROP_DAY_ON`) are inert on this checkpoint.

## 1. The exact chain

### 1.1 Observation → features → head (`src/kagg3/core/brain.py`)

`decide` (brain.py:995) runs `features(xp, obs)` (brain.py:533) → one
`prod[9,12]` block per product, a `glob[24]` vector and `residual_drain`
(brain.py:239).

Per-product columns (brain.py:551-564), in order:

| # | column | meaning |
|---|--------|---------|
|0|`(inv - MARKET_I0)/T`|market inventory vs opening|
|1|`price/base`|today's quote over the crop's base|
|2|`log1p(base)/6`|price scale|
|3|`T/450`|curve width|
|4,5|`_BT`,`_AT`|below/above target shape params|
|6|`demand/20`|town units/day at today's shops|
|7|`own/25`|**our** producing tiles of that product|
|8|`opp/25`|**the rival's** producing tiles of that product|
|9|`shed/100`|our shed stock|
|10|`_FIRST/12`|`spec.CROP_FIRST_YIELD_DAY` — **days to first harvest**|
|11|`_RATE`|steady-state units/day of a producing tile|

`glob` (brain.py:583-607) carries `day/30`, `(30-day)/30`, our money, **the
rival's money**, the money gap, free/unlocked/planted/animal tiles for **both**
boards, shed totals, seed totals, shop count and the mean `price/base`.

`residual_drain` (brain.py:239-284) is the only non-linear market term:

```
drain    = expected_drain(day..N_DAYS, today's shops + scheduled unlocks)   # brain.py:218
supply   = (mkt_inv - MARKET_I0) + our shed + (own + opp) * _RATE * days_left
gap      = clip((drain - supply)/T,          ±DRAIN_CLIP)    # DRAIN_CLIP = 4.0, brain.py:237
share    = clip((drain - supply)/(drain + 1), ±DRAIN_CLIP)
```

`PO.forward` turns these into `scores[12,2]`; column 0 is **`grow`**
(brain.py:1006) — one learned scalar per product. That is the crop preference.

### 1.2 How many tiles get planted at all

```
dev_frac     = sigmoid(head[5] + aux[2]*n_free/25)                 # brain.py:1061
n_dev        = floor(dev_frac * n_free)                            # brain.py:1062
animal_count = floor(sigmoid(head[6]) * n_dev)                     # brain.py:1064
animal_want  = largest_remainder(softmax(grow[animals]*sharp + a_mix), animal_count)  # 1093
plant_total  = n_dev - sum(animal_want)                            # brain.py:1094
```

### 1.3 The crop split — the formula

Shipped FT2 (`theta.shape[0] = 6789 <= PO.offset("cm") = 6855`) takes the
`else` branch at **brain.py:1129**:

```
sharp = 1 + 4*sigmoid(head[7])                                   # learned, measured 2.3 - 3.9
w     = softmax( grow[0:5] * sharp )                             # brain.py:1129
w     = w * can_mature                                           # brain.py:1140-1142
w     = w * absorb                                               # brain.py:1182-1184
w     = w / sum(w)               (sum(w)==0 -> plant_total := 0) # brain.py:1192-1193
plant_target = largest_remainder(w, plant_total, 5)              # brain.py:1194
```

with the two masks

```
can_mature = (day + spec.CROP_FIRST_YIELD_DAY[c] <= VAL.pay_day())        # brain.py:1140
absorb     = (drain[c, share] + DRAIN_CLIP*tanh(out.sat[c]) > -DRAIN_CLIP) # brain.py:1182
```

`VAL.pay_day()` is **29** with `plan.HORIZON_DROP_ON = True` (plan.py:558,
valuation.py:43). `out.sat` is a learned per-crop threshold bias; at zero theta
the test is exactly "is this market saturated at the clip floor".

**Gene values that matter in shipped FT2** — `cm` (32×5), `cb[5]` and `cd[5,9]`
are all **beyond the checkpoint's length and therefore exactly zero/unused**;
`sw`/`swb` (switch genes, offset 7,065) likewise. The only live crop genes are
the `grow` readout weights and `head[7]`, plus `out.sat`. Measured means over 6
ENG22 boards (`softmax_detail` in graphs.json): `sharp` 3.88 on day 0 falling to
~2.3-2.8; `grow` day 0 = wheat 0.72, carrot 0.73, tomato −0.74, strawberry
−0.34, melon −0.55.

### 1.4 The `plant_target` rewrites in `plan.py`

**Every one of them is OFF in shipped FT2** (module default `False`, and the
shipped switch string `OPEN_PUMP_ON, TAIL_FILL_ON, BANK_BEFORE_LOT_ON,
HIRE_ROW_ON, brain.MELON_GENE_ON, brain.CROP_DAY_ON` does not name any of them).
`macro.plant_target` therefore reaches the clip byte for byte as `brain.decide`
wrote it:

- `_melon_open` (plan.py:6874, `MELON_OPEN_ON=False` @1009) — day-0 melon plate.
- `_wheat_mix` (plan.py:6759, `WHEAT_VOLUME_ON=False` @6727) — share onto wheat.
- `_crop_scarce` (plan.py:6848, `CROP_SCARCE_ON=False` @6838) — forward/spot re-share.
- `_macro_targets` (plan.py:7297, `MACRO_EXEC_ON=False` @6973) — scripted calendar.
- `_endgame_tomato` (plan.py:7348, `ENDGAME_TOMATO_ON=False` @1811).
- `_late_straw_cap` (plan.py:7401, `LATE_STRAW_CAP_ON=False` @1887).
- `_opp_mix` (plan.py:2136, `OPP_MIX_ON=False` @2021) — rival-supply re-weight.
- `_fill_wheat` via `fill_target` (plan.py:8367-8389, `PLANT_FILL_ON=False` @6483,
  `PLANT_FILL_LATE_ON=False` @6507) — so `fill_target == macro.plant_target`.
- `open_board()` (plan.py:1536) is `False` (all three of `MELON_OPEN_ON`,
  `OPEN_DENY_ON`, `MIRROR_OPEN_ON` off), so neither the melon-first seed prefix
  (plan.py:7455-7463) nor the near-shed melon placement (plan.py:8560-8578) runs.

### 1.5 The clips, in the order they bind

```
1 TILES   a_want, seed_cap = _seed_room(macro, n_free, sfree, a_have)   # plan.py:6620-6643
          seed_cap = max(n_free - tiles the herd's builds take, 0)      # plan.py:6642
          want_raw = max(plant_target - view.seeds, 0)                  # plan.py:7448
          before   = cumsum(want_raw) - want_raw            (crop order) # plan.py:7465
          w_seed   = clip(want_raw, 0, max(seed_cap - before, 0))        # plan.py:7466
2 MONEY   n_buy   = budget.grant(values, costs, wants, purse, room)      # plan.py:8366
          seed_buy = n_buy[L_SEED0 : L_SEED0+5]                          # plan.py:8436
          seed value  v_c = grow_mult[c]*clip(_stream_rev(price_table[c],
                            inv_h[c], u_new[c]), 0, VALUE_CAP)//GROW_ONE # plan.py:7543-7544
          seed cost   = spec.CROP_SEED_COST[c]                           # plan.py:7546
3 PLANT   plant_eff = min(fill_target, view.seeds + seed_buy)            # plan.py:8463
          p_cum     = cumsum(plant_eff)                                  # plan.py:8551
          plant_here = free_slot & 0 <= plant_rank < p_cum[-1]           # plan.py:8552
          plant_crop = count_le(p_cum, plant_rank)   (crop-order prefix) # plan.py:8581
4 CREW    the PLANT op is emitted per tile (plan.py:8672) and then has to be
          admitted by the day's labour route/budget like every other op.
```

`u_new = VAL.new_plant_units(crop, day)` (plan.py:8237, valuation.py:196) is the
units a seed planted **today** still delivers by `pay_day` — it is where the
crop's growth schedule enters the *money* clip.

## 2. Dependency questions, answered

**Does any term depend on days-to-harvest / growth time / days remaining?
YES — four places.**

1. **Hard mask.** `can_mature = day + spec.CROP_FIRST_YIELD_DAY[c] <= pay_day()`
   — **brain.py:1140-1142**. With `pay_day() = 29` the last plantable day is
   wheat/carrot 27, tomato 21, strawberry/melon 19. Measured: mean
   `plant_target[MELON]` is 0.05 on day 19 and **exactly 0.0 on days 20-29** on
   all 20 boards, and `can_mature[MELON]` flips 1→0 at day 20 in the probe.
2. **Feature.** `spec.CROP_FIRST_YIELD_DAY/12` is product column 10 of the
   encoder (**brain.py:563**), and `_RATE` (units/day of a producing tile) is
   column 11 — so the learned `grow` score sees the growth schedule directly.
3. **Seed value.** `u_new[c] = VAL.new_plant_units(c, day)` (plan.py:8237 →
   valuation.py:196-221) computes yield-by-`pay_day` from
   `CROP_FIRST_YIELD_DAY`, `CROP_INTERVAL`, `CROP_MAX_YIELD`,
   `CROP_SATURATE_AGE` and `CROP_WINDOW_START`, and returns **0** if the crop
   cannot mature. It scales the seed's value in `budget.grant` (plan.py:7543)
   and the planting's labour value `rev_plant` (plan.py:8762).
4. **Horizon feature.** `glob[0] = day/30`, `glob[1] = (30-day)/30`
   (brain.py:584-585) — the head can (and does) shape the mix by calendar day.

What is **not** there: no per-crop "last plantable day" constant, no explicit
tile-turnover term (wheat's 4-day cycle is only visible to the net through
columns 10/11), and on this checkpoint **no day-indexed crop bias** (`cd` is
past the end of theta).

**Does any term depend on the rival's plantings? YES, but only through
aggregates.**

- `prod[:,8] = opp/25` — the rival's producing tiles per product (brain.py:559).
- `glob[9] = opp_plant/100`, `glob[20] = opp_animal/100`, `glob[3] = opp_money`,
  `glob[4] = money - opp_money`, `glob[8] = opp_unlocked`, `glob[21] = opp_nquad`.
- `residual_drain` charges `(own + opp) * _RATE * days_left` against the town's
  remaining appetite (brain.py:277-279), and that feeds the **`absorb` mask**
  (brain.py:1182). This is the only place a rival planting can *veto* a crop.
- The explicit rival-reactive rewrites `_opp_mix` (`OPP_MIX_ON`) and
  `_opp_supply` (`OPP_SUPPLY_ON`) are **OFF**.

**Does any term depend on expected price AT RIPENING? NO.**
Every valuation is at **today's hour-0 quote**: `price/base` in the feature
block, `price_table[c]`/`inv_h[c]` in `_stream_rev` (plan.py:7543),
`view.price[plant_crop]` in `rev_plant` (plan.py:8762), and the docstrings say
so explicitly ("Prices are today's hour-0 quotes -- the Phase-1 projection",
valuation.py:20, 109, 155). The only forward-priced object in the repo is
`_crop_scarce`'s forward/spot ratio (plan.py:6848) and it is **OFF**. The
consequence is stated in the code itself (brain.py:1152-1158): melon is priced
at 271 on day 10 against a realised 84.

## 3. Crop facts (engine, `src/kagg3/spec.py:41-76`)

| crop | seed | first yield (days) | max-yield day | interval | max yield | ongoing | base price | T | last plantable day (pay_day 29) |
|---|---|---|---|---|---|---|---|---|---|
|WHEAT|10|2|4|0|6|no|25|400|27|
|CARROT|20|2|3|0|4|no|35|450|27|
|TOMATO|50|8|8|1|4|**yes**|60|200|21|
|STRAWBERRY|100|10|10|2|4|**yes**|120|100|19|
|MELON|80|10|12|0|6|no|250|300|19|

`CROP_WINDOW_START = (max_yield_day+1)//2`; `CROP_SATURATE_AGE` = melon 10 (not
12), every other crop = its max-yield day (spec.py:73-76). Market curves
(spec.py:111-120): melon `above = sq @ 3.6x` — the steepest collapse of the
five; strawberry `linear @ 1.6x`; carrot `sqrt @ 0.7x`; wheat `log @ 0.2x`.

## 4. Measured, 20 ENG22 fertilizer-engine boards (seat 0, pinned towns)

Win rate 0.35 (7/20). `S/cropformula/graphs.json`.

**Target vs actual (ours, season tiles):** wheat 93.4, carrot 33.7, strawberry
30.6, melon 15.1, tomato 6.9. `planted_actual_per_day` tracks
`plant_target_per_day` almost exactly from day ~8 on — the gene, not the
planner, is what chooses.

**Rival (same boards):** wheat 123.4, carrot 37.8, strawberry 30.0, melon 13.3,
tomato 11.2 — a *similar mix, more of it*, and **9.9 melon tiles on day 0-1
against our 0.0** (our first melon lands day 4+, mean day 10.9 vs their 3.5).

**Binding clip per day** (`clip_binding_share`): day 0 = **tiles** on 20/20
boards; days 3-7 = **money** on 65/55/85/70/40 % of boards; day 8 onward the
target is met outright on 80-100 % of boards, with **crew** the only residual
(peaks 0.50 on day 23, 0.35 on day 25). Days 1-2 and 28-29 are `no_want`
(`sum(plant_target) == 0`). So: the early game is cash-bound, the late game is
labour-bound, and the middle game plants exactly what the gene asks.

**`plant_target` vs that day's quote** (pooled OLS, 600 points):
carrot slope **+0.115 tiles/coin, r = 0.371** (the BACKHALF finding reproduced);
melon +0.0037, r = 0.277; strawberry +0.0078, r = 0.143; tomato +0.0038,
r = 0.107; wheat +0.030, r = 0.069. Carrot is the crop whose target is most
visibly driven by the town's bid.

**Lifecycle, ours vs theirs** (per game; market phase re-simulated exactly):

| crop | ours: tiles / day planted / day sold / coins-per-unit | theirs |
|---|---|---|
|WHEAT|93.4 / 13.8 / 17.2 / 36.6|123.4 / 15.8 / 20.4 / 38.1|
|CARROT|33.7 / 17.1 / 21.4 / 47.4|37.8 / 23.0 / 26.4 / 49.2|
|TOMATO|6.9 / 16.2 / 26.0 / 107.4|11.2 / 13.2 / 23.5 / 79.4|
|STRAWBERRY|30.6 / 6.7 / 20.3 / **129.4**|30.0 / 8.1 / 21.5 / 113.8|
|MELON|15.1 / **10.9** / 21.8 / **155.4**|13.3 / **3.5** / 13.8 / **224.1**|

Melon is the whole story again: same tile count, **7.4 days later in the
ground**, 8 days later to market, **−69 coins/unit** (MELONENG / MELONGIFT).
And the mechanism is now named precisely: melon's `residual_drain` share is
pinned at **−4.0 = −DRAIN_CLIP from day 1** (probe `share`), so melon only ever
survives `absorb` on the learned `out.sat` bias, and it cannot be planted at all
after day 19 (`can_mature`).

## 5. What this closes and what it leaves open

Closed by inspection: there is no hand-written crop rule to tune, and no
price-at-ripening term exists anywhere in the live path. The day-indexed crop
gene (`cd`) and the crop-mix readout (`cm`/`cb`) — the two levers an ES arm
would name — are **not present in the shipped checkpoint at all**, which is
consistent with GENEJUDGE/CROPMIX having closed those families on *longer*
thetas. The untested statement this box adds: **`out.sat` (the `absorb`
threshold) and `head[7]` (the softmax sharpness) are the only two live scalars
between `grow` and `plant_target` on the shipped theta**, and neither has ever
been judged on its own.
