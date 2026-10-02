# 2026-09-11 — can the d10 melon pot be taken ADDITIVELY?

**Review correction, September 13:** this is an unexecuted build proposal, not
a failed additive experiment. The copied 72 / 17,440 average is 242.22, not
233; its difference from 12,537 is 4,903. That cross-arm difference is not an
isolated timing cost. The historical source data are unavailable in this
checkout, so the figures below remain attributed historical reports. See the
[route correction](2026-09-10-melon-route-capacity.md) and
[current experiment decision](2026-09-13-melon-sigma-reachability.md).

Question: buy extra land early, plant it all melon on d0-1, leave the existing basket
alone. Does it pay after the land price and the second-dumper quote (~174)?

## 1. What the archive already settled (not re-measured)

* `2026-09-10-melon-route-capacity.md` / plateau §56: the pot **is** reachable — with
  `MIDDAY_PLACE_V2_ON`, 66/72 units sell on d10 (72 u / 12,537, avg **174**, vs the clone's
  72 / 17,440 at 233); the deposit turn costs ~4.2k of timing. It still loses as a **swap**:
  five builds lose 15-20k over d12-29 because the 12 tiles displace the animal/wheat denial
  (`MELON_OPEN_ON` band6 54.2→15.1 %, −17,554; pinned judge 1.9 % at 12 tiles, 3.8 % at 8).
* `2026-09-10-residual-loss20.md` §3 / plateau §51: at d10 we hold 46.6 tiles with
  **13.3 idle**, they hold 32 with **0**; melon ≈ −15k of the −22.7k d10-14 band.
* `2026-09-09-board-fill.md`: 99.4 % of idle tile-days are the plan cap, not seed, cash or
  labour; lifting it (`PLANT_FILL_LATE_ON`, plateau §17) costs 5.6-6.9k of our own purse and
  loses +0/−10 — family closed. Same doc corrects the premise: we out-plant them (44.5 vs
  33.1) and hold more quadrants (2.9 vs 2.0); "47 vs 59" was never the record.

## 2. Land cadence: the clone's vs ours (new, descriptive)

Tape census, 5 LOSS20 boards (`S/melonadd/tape_land.py`): every clone buys land at
**d6 t6** and **d11 t1** — 2 quads at d10, 3 from d11 — plants 19 tiles on d0
(7 WHEAT + 12 MELON, `CROP_SEED_COST` 70 + **960**), 33 cumulative plantings by d5,
70 by d10, and ends d0 with ~50 coins.

Sim trace of our seat, flow172_g170c on 107056463 (`S/melonadd/land_probe.py`):
BUY_LAND rows fire on **d5** and **d10** — quad 2 from d6, quad 3 from **d11**, one day
*ahead* of the clone. d0: 19 tiles planted, **0 empty tiles left**, money 3000 → **145**.

So: our land cadence is not behind, and **day 0 has no spare tile and no spare coin**.

## 3. Is it expressible in knobs? No.

* `_melon_open` (plan.py:4581) *preserves* `sum(plant_target)` by construction — the
  melon debt is paid by other crops in `_MELON_PAY_RANK` order. Melon is a swap by
  design; `MELON_OPEN_TILES/_DAY/_LOT` cannot make it additive.
* `buy_land` (plan.py:5358) has no switch: `nquad<4 & ~terminal & money>=land_gap &
  money>=land_cost//LAND_OWN_DEN & (land_value + macro.land_bias > 0)`. `land_bias` is a
  **gene** (brain.py:893), not a knob; `LAND_OWN_DEN`/`LAND_REV_*` do not bind on d0
  (3000 ≥ 1000); `DEV_DAYS`/`LAND_PICKUPS` reprice every day's quadrant, not d0's.

No sim arm was run: nothing expresses "one extra quad on d0, all melon, rest unchanged".

## 4. Build spec (if it is ever wanted)

`MELON_ADD_ON` (plan.py switch, default False), `MELON_ADD_DAY = 0`, `MELON_ADD_TILES = 12`:
(a) OR into `buy_land` at plan.py:5358 the term `MELON_ADD_ON & (view.day == MELON_ADD_DAY)
& (view.nquad < 4) & (money >= land_cost)`, keeping the M2 own-purse and terminal gates —
inputs `view.day`, `view.nquad`, `money`, `land_cost`;
(b) a new `_melon_add(xp, view, macro, n_pros)` called inside `_derive` **after** line 5372
(where `n_free`/`wants` already carry the prospective tiles), which *raises*
`plant_target[I_MELON]` by `min(MELON_ADD_TILES, n_pros)` and touches no other crop, so the
total grows by exactly the claim — the opposite of `_melon_open`'s invariant. Reuse
`_MELON_SEED_RANK` and `_rank_near`; run with `MIDDAY_PLACE_ON,MIDDAY_PLACE_V2_ON`;
(c) tests: OFF decodes byte-for-byte, ON gives d0 nquad 2 and `sum(plant_target)` +12.

## 5. Verdict — **needs build X, and the arithmetic argues against it**

Additive costs **1,000 (quad 2) + 960 (12 melon seed) = 1,960 of a 3,000-coin d0 purse**
that §2 shows is already spent to 145. There is no idle d0 tile to use instead, so the
land is unavoidable. The gross prize is the §56 number, ~12.5k at the second dumper's 174,
against a d0-4 band we already lead by 1,158 and a herd line the swap arms lost 15-20k on.
Note the clone's own melon is **not** additive: it plants the same 19 tiles we do and pays
740 more seed coins. If built, judge on LEG20/HELD42 paired margin and expect the
displacement (two-purse rule) to land in the herd.
