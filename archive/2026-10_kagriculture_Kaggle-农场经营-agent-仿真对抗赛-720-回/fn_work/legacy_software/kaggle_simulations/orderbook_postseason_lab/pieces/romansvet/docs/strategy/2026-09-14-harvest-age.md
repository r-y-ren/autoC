# HARVEST-AGE: does taking wheat at `c_first` (ymg_aq's schedule) buy cycles?

**VERDICT CHECKPOINT 1 (harvest age) — LOSS, on both sets, on every arm.**
Lowering the one-time-crop harvest age by k days costs **-2,473 (t -1.8) /
-3,143 (t -6.5) coins at k=1** and **-6,555 (t -4.5) / -7,474 (t -15.5) at
k=2** (ymg / band), with paired margins **-4,910 (t -5.1) / -4,165 (t -6.7)**
and **-7,886 (t -9.5) / -8,761 (t -15.5)**.  Wheat-only-at-`c_first` (ymg_aq's
own schedule) is -5,884 (t -7.7) / -6,394 (t -15.1) coins; on the band set it
flips 18 boards from win to loss and takes the win rate 43 % -> 16 %.  The +1
control loses -30,538 / -29,179, so the measurement is live in both
directions.  **The delta is volume, not price: crop units 794 -> 616 (band,
k=2) while coins per unit go UP (wheat 37.3 -> 38.3, carrot 64.2 -> 74.2).**

**VERDICT CHECKPOINT 2 (the late-season stop) — LOSS.**  Developing *every*
free tile on d20-d27 instead of `dev_frac x n_free` does raise late planting
(band 58.0 -> 76.0 tiles, d20-27 idle 2,345 -> 1,665 tile-hours) and still
loses **-4,980 coins (t -20.0)**, margin -5,183 (t -18.6), 15 boards flipped.
Forcing that window to wheat loses -6,562 (t -5.5).  The extra plantings are
paid for in harvests: +18 tiles planted costs -7.1 one-time harvests and -44
crop units on the same 68 boards.

**No arm is positive at t >= 2 on either set, so the TOPB3R9 leg was not run.**

All sim-descriptive: CRN sim, tape-action opponent seat, pinned towns,
`shop_crn`, theta `flow193_g100_hr` (= B), switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON`, 12 ymg_aq boards
(`S/macro_exec/boards_ymg.json`) + 68 band boards
(`S/seed_screen/boards_BAND.json`), both seats of every town.  No engine game,
no ES arm, no promotion gate.

Tools: `S/harvest_age/{patches.py,ledger.py,report.py}`; raws
`raw_<arm>_{ymg,band}.npz`; logs `<arm>_{ymg,band}.log`; tables
`S/harvest_age/report.md` (+ `report_ymg.md`, `report_band.md`).

## 0. Method, and why the patch is trustworthy

`src/kagg3/core/plan.py` is being edited by another agent, so **no arm reads
the working tree**.  `S/harvest_age/patches.py` unpacks `git archive HEAD src`
(HEAD `21d330a`) into the scratchpad and makes one copy per arm, each a
**single-line substitution** at each site and nothing else.  `S/harvest_age/
ledger.py` is `S/dev_slope/ledger.py` (per-item sell/buy accounting
`_market_turn` + per-day dawn `snap`) plus `S/replant/instrument.py`'s
`units.apply_units` wrapper, trimmed to six counters.  `--src` selects the tree.

Two independent checks that the harness is non-perturbing:

* **B reproduces `S/dev_slope/raw_{ymg,band}_B.npz` bit-for-bit** on `money`,
  `sold_np`, `sold_rp`, `tiles`, `anim`, `idle`, `nhands` -- from the frozen
  tree, with the `apply_units` wrapper installed.
* The wrapper's counters reproduce REPLANT-SCOPE's independently-measured
  numbers exactly: B plants **184.2** tiles/season on the ymg set (REPLANT-
  SCOPE 184.2), frees **141.2** (141.2), idles **316** tile-hours over d0-d19
  (316), plants **53.6** tiles on d20-d27 (53.6) and idles **2,306**
  tile-hours there (2,306).

`c_sat` / `sat` is read at exactly one place in each module, so the
substitution moves the harvest mask, `brain.n_free_slots` and (through the
`harvest_age` argument of `VAL.crop_remaining_value`) the water/tier pricing
together, and touches nothing else.

### The exact patches (verbatim)

Site 1, `kagg3/core/plan.py` (frozen tree line 5223; `plan.py:5313` in the
working tree, which carries another agent's +166 lines):

```
-    harvest_age = xp.clip(VAL.pay_day() - view.t_day, c_first, c_sat)
k1:  harvest_age = xp.clip(VAL.pay_day() - view.t_day, c_first, xp.maximum(c_first, c_sat - 1))
k2:  harvest_age = xp.clip(VAL.pay_day() - view.t_day, c_first, xp.maximum(c_first, c_sat - 2))
wf:  harvest_age = xp.clip(VAL.pay_day() - view.t_day, c_first, xp.where(crop == spec.I_WHEAT, c_first, c_sat))
p1:  harvest_age = xp.clip(VAL.pay_day() - view.t_day, c_first, c_sat + 1)
```

Site 2, `kagg3/core/brain.py:185` (`n_free_slots`, the dawn free-tile census --
its own comment says it has to stay the same clamp):

```
-    harvest_age = xp.clip(VAL.pay_day() - obs.t_day, first, sat)
k1:  harvest_age = xp.clip(VAL.pay_day() - obs.t_day, first, xp.maximum(first, sat - 1))
k2:  harvest_age = xp.clip(VAL.pay_day() - obs.t_day, first, xp.maximum(first, sat - 2))
wf:  harvest_age = xp.clip(VAL.pay_day() - obs.t_day, first, xp.where(c == spec.I_WHEAT, first, sat))
p1:  harvest_age = xp.clip(VAL.pay_day() - obs.t_day, first, sat + 1)
```

**There is a third copy of the clamp**, `valuation.remaining_plant_units`
(`valuation.py:204`, `harvest_age = xp.clip(hi - t_day, first, sat)`), which
prices a *new* planting -- the brief named two sites, so k1/k2/wf/p1 leave it
at B's and the arm's planner still values a wheat seed at 4 units.  Arm `k2v`
moves that line too (`xp.maximum(first, sat - 2)`) and bounds the effect: it
lands within noise of `k2` (-5,788 vs -6,555 ymg; -8,695 vs -7,474 band), so
the mis-pricing is **not** what sinks the arm.

CHECKPOINT 2, `kagg3/core/brain.py` (`decide`).  `can_mature`
(`obs.day + CROP_FIRST_YIELD_DAY <= VAL.pay_day()`, `HORIZON_DROP_ON` => 29)
**already** lets wheat and carrot be planted through d27, so the horizon mask
is not the stop -- the stop is `n_dev = dev_frac x n_free`.  The smallest
patch that makes B "plant on d20-27 what fits before d29" is therefore to
develop every free tile in that window and let `can_mature`, `free_slot`, the
purse and the turn budget do the rest:

```
-    plant_total = n_dev - xp.sum(animal_want)
late:  plant_total = xp.where((obs.day >= 20) & (obs.day <= 27), n_free - xp.sum(animal_want), n_dev - xp.sum(animal_want))
```

and `latew` adds the wheat-only mix in the same window:

```
-    w = w * can_mature
latew: w = xp.where((obs.day >= 20) & (obs.day <= 27), (xp.arange(spec.N_CROPS) == spec.I_WHEAT).astype(xp.float32), w * can_mature)
```

## 1. The crop table says the lever is dead before a single game is run

`units(a) = min(max_yield, 1 + max(min(a, max_yield_day) - window_start + 1, 0))`
(one unit at `_new_plant`, +1 per in-window WATER, +2 if fertilized).

| crop | seed | c_first | c_sat (B) | max_yield_day | window start | u @c_first | u @c_sat-1 | u @c_sat | u @c_sat+1 | **u/tile-day @c_first** | @c_sat-1 | **@c_sat** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| WHEAT | 10 | 2 | 4 | 4 | 2 | 2 (age 2) | 3 (age 3) | 4 | 4 (age 5) | **1.00** | 1.00 | **1.00** |
| CARROT | 20 | 2 | 3 | 3 | 2 | 2 (age 2) | 2 (age 2) | 3 | 3 (age 4) | **1.00** | 1.00 | **1.00** |
| TOMATO | 50 | 8 | 8 | 8 | 4 | ongoing -- `harvest_ong` fires at age >= c_first; `harvest_age` is never read | | | | | | |
| STRAWBERRY | 100 | 10 | 10 | 10 | 5 | ongoing -- same | | | | | | |
| MELON | 80 | 10 | 10 | 12 | 6 | 6 (age 10) | 6 (age 10) | 6 | 6 (age 11) | **0.60** | 0.60 | **0.60** |

Three facts fall out:

1. **Wheat's and carrot's window start is 2, equal to `c_first`, so
   `units(a) = a` and the yield rate is flat at 1.00 units per tile-day at
   every legal harvest age.** Harvesting wheat at 2 instead of 4 halves the
   units per harvest and doubles the cycles: exactly zero units gained, one
   extra 10-coin seed and one extra PLANT+HARVEST pair of unit-turns per
   tile per 4 days.  Fertilizer scales both sides (`units(a) = 1 + 2(a-1)`
   capped at 6) and does not change the ratio.
2. **Melon cannot move.**  `c_first = c_sat = 10`, so `max(c_first, c_sat-k)`
   is 10 for k = 1 and 2; the k arms touch wheat and carrot only.
3. **Tomato and strawberry are ongoing crops** -- `harvest_ong = is_plant &
   (c_ongoing == 1) & (t_yield > 0) & (age >= c_first)` is a different mask and
   never reads `harvest_age`.  So "wheat-only at `c_first`" (arm `wf`) and
   "k = 2" (arm `k2`) differ only in carrot.

So the crop table predicts the sign before the sim runs: **B is already at the
rate optimum, at the lowest op cost.**  What the ledger adds is the size of the
loss and its anatomy.

## 2. CHECKPOINT 1 -- the paired ledger

### 12 ymg_aq boards

| arm | our coins | d coins vs B (t) | margin | d margin vs B (t) | win % | flips +/- | planted/season | one-time harvests | idle t-h d0-19 | PASS % | units/harvest | herd d10 | cash d10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 93,127 | - | -13,751 | - | 0 % | - | 184.2 | 141.2 | 316 | 10.3 | 3.53 | 10.7 | 6,032 |
| k1 | 90,654 | **-2,473 (-1.8)** | -18,661 | **-4,910 (-5.1)** | 0 % | +0/-0 | 204.8 | 163.0 | 1,222 | 10.0 | 2.81 | 10.1 | 5,321 |
| k2 | 86,572 | **-6,555 (-4.5)** | -21,638 | **-7,886 (-9.5)** | 0 % | +0/-0 | 221.9 | 181.5 | 1,873 | 10.0 | 1.82 | 9.6 | 5,030 |
| wf (wheat @c_first) | 87,244 | **-5,884 (-7.7)** | -20,217 | **-6,466 (-10.3)** | 0 % | +0/-0 | 225.3 | 183.9 | 1,519 | 10.2 | 1.91 | 10.1 | 5,305 |
| p1 (+1 control) | 62,590 | **-30,538 (-11.7)** | -67,093 | **-53,341 (-26.2)** | 0 % | +0/-0 | 157.5 | 25.9 | 2,507 | 10.9 | 6.42 | 6.2 | 4,953 |
| k2v (k2 + valuation) | 87,339 | **-5,788 (-4.1)** | -21,185 | **-7,433 (-10.7)** | 0 % | +0/-0 | 217.2 | 177.2 | 1,876 | 9.9 | 1.78 | 9.9 | 5,173 |

(B loses every ymg_aq board on margin already -- ymg_aq is a 3,000-band
opponent; the win column is 0 % for every arm and only the paired delta
carries information there.)

### 68 band boards (TOPB2 / LIVE-C)

| arm | our coins | d coins vs B (t) | margin | d margin vs B (t) | win % | flips +/- | planted/season | one-time harvests | idle t-h d0-19 | PASS % | units/harvest | herd d10 | cash d10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 104,092 | - | -192 | - | **43 %** | - | 182.9 | 142.3 | 343 | 10.2 | 3.63 | 11.1 | 5,803 |
| k1 | 100,950 | **-3,143 (-6.5)** | -4,357 | **-4,165 (-6.7)** | 34 % | +2/-8 | 193.8 | 154.6 | 1,186 | 10.2 | 2.83 | 10.9 | 5,895 |
| k2 | 96,618 | **-7,474 (-15.5)** | -8,952 | **-8,761 (-15.5)** | 9 % | +0/-23 | 214.7 | 176.7 | 1,388 | 10.1 | 1.89 | 10.1 | 5,309 |
| wf | 97,698 | **-6,394 (-15.1)** | -6,302 | **-6,110 (-11.8)** | 16 % | +0/-18 | 215.6 | 176.4 | 1,145 | 10.0 | 1.97 | 10.9 | 5,302 |
| p1 | 74,913 | **-29,179 (-21.6)** | -54,778 | **-54,587 (-18.0)** | 0 % | +0/-29 | 159.5 | 30.4 | 2,716 | 10.6 | 5.43 | 6.0 | 4,712 |
| k2v | 95,397 | **-8,695 (-22.6)** | -11,782 | **-11,590 (-21.9)** | 6 % | +0/-25 | 210.9 | 173.3 | 1,778 | 10.1 | 1.95 | 9.5 | 5,114 |

### units and coins per unit, band set, our seat, board mean

| arm | WHEAT | CARROT | TOMATO | STRAWBERRY | MELON | EGG | MILK | WOOL | crop units | crop revenue | animal revenue |
|---|---|---|---|---|---|---|---|---|---:|---:|---:|
| B | 322 / 37.3 | 108 / 64.2 | 28 / 141.8 | 252 / 137.1 | 85 / 161.4 | 116 / 51.6 | 191 / 129.1 | 116 / 139.9 | **794** | 71,109 | 46,997 |
| k1 | 269 / 37.2 | 83 / 70.8 | 27 / 142.4 | 255 / 137.5 | 85 / 160.5 | 112 / 52.0 | 189 / 130.7 | 116 / 139.8 | 720 | 68,528 | 46,752 |
| k2 | 176 / 38.3 | 72 / 74.2 | 25 / 143.5 | 258 / 137.1 | 86 / 159.8 | 108 / 52.0 | 182 / 132.5 | 118 / 137.9 | **616** | 64,754 | 45,955 |
| wf | 173 / 38.4 | 89 / 69.5 | 26 / 141.6 | 256 / 138.1 | 86 / 160.1 | 110 / 52.0 | 188 / 127.9 | 119 / 136.8 | 630 | 65,578 | 46,095 |
| p1 | 78 / 37.9 | 4 / 188.6 | 11 / 166.0 | 233 / 149.3 | 75 / 169.6 | 58 / 52.7 | 143 / 154.5 | 84 / 168.4 | 402 | 53,108 | 39,319 |

(cells are `units sold / coins per unit`.)

## 3. Anatomy: yield-bound first, hand-bound second, **not** price-bound

**Yield-bound.**  The trade the arms actually make, band set:

| arm | one-time harvests | x | units per one-time harvest | = | crop units |
|---|---:|---|---:|---|---:|
| B | 142.3 | | **3.63** | | 794 |
| k1 | 154.6 (+8.6 %) | | 2.83 (-22 %) | | 720 (-9.3 %) |
| k2 | 176.7 (+24 %) | | 1.89 (-48 %) | | 616 (-22 %) |

Section 1 says the *tile* trade is exactly neutral (1.00 u/tile-day either
way); the sim says the *farm* trade is 24 % more cycles for 48 % less yield,
because the extra cycles never materialise on the freed tiles.  Idle
tile-hours, band set, by decade:

| arm | d0-9 | d10-19 | d20-29 |
|---|---:|---:|---:|
| B | 255 | 88 | 3,974 |
| k1 | 1,047 | 139 | 4,758 |
| k2 | 1,157 | 231 | 5,289 |

**The freed tiles sit.**  `free_slot` does contain `harvest_one`, and the dawn
plan does pair harvest and replant one hour apart (REPLANT-SCOPE), but the
*number* of tiles the day develops is `n_dev = _qfloor(dev_frac x n_free)`
(`brain.py:1008-1009`) -- a fraction.  Doubling `n_free` puts back only
`dev_frac` of it, so the harvest-age arms manufacture free tiles about twice as
fast as the development rule will re-fill them, and B's tightest stretch of the
season (255 idle tile-hours over d0-d9) becomes its loosest (1,157).  DEV-SLOPE
already showed `dev_frac` cannot be raised to absorb them (dp1 -9,644, dmax
-13,420).

**Hand-bound.**  The crew is not idler, it is smaller and busier with churn
(band, board mean):

| arm | active unit-turns | PASS % | PLANT + one-time-HARVEST turns | cash d10 | herd d10 |
|---|---:|---:|---:|---:|---:|
| B | 6,689 | 10.2 | 325 | 5,803 | 11.1 |
| k1 | 6,595 | 10.2 | 348 | 5,895 | 10.9 |
| k2 | 6,408 | 10.1 | 391 | 5,309 | 10.1 |

k2 spends **+66 unit-turns** on plant/harvest churn out of **-281 fewer
unit-turns in total** -- the roster shrinks because the coins that hire it
arrive later (cash at d10 5,803 -> 5,309, herd 11.1 -> 10.1).  PASS share is
flat at ~10 %, so none of this is slack being taken up; it is the same booked
day re-allocated from WATER/HARVEST/SELL chains to PLANT chains.

**Not price-bound.**  Coins per unit move the *wrong* way for a
"more units into the same pot" story: wheat 37.3 -> 38.3 and carrot 64.2 ->
74.2 under k2.  Fewer units meet a slightly better quote; total crop revenue
still falls 71,109 -> 64,754, and animal revenue is flat (46,997 -> 45,955).
The entire delta is volume.

**The +1 control** confirms the instrument: at `c_sat + 1` the harvest mask
fires a day after the water window closes, one-time harvests collapse 142.3 ->
30.4 (crops weed out before the route reaches them), crop units fall to 402 and
the arm loses -29,179 coins.  A dead knob would move neither direction; this
one moves both.

## 4. CHECKPOINT 2 -- the late-season stop

`can_mature` was not the gate.  With `HORIZON_DROP_ON` (`VAL.pay_day() = 29`)
wheat and carrot are already plantable through d27 and B plants 58.0 tiles
there; the binding constraint is `n_dev = dev_frac x n_free`, the same rule
that strands the harvest-age arms' freed tiles.  Arms `late` (develop every
free tile on d20-d27) and `latew` (same, forced to wheat):

| set | arm | d coins vs B (t) | d margin vs B (t) | win % | flips | planted d20-27 | planted/season | one-time harvests | idle t-h d20-27 | units d25-29 | revenue d25-29 | unsold stock |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ymg | B | - | - | 0 % | - | 53.6 | 184.2 | 141.2 | 2,306 | 273 | 17,002 | 0 |
| ymg | late | **-3,442 (-6.3)** | -3,544 (-6.5) | 0 % | +0/-0 | 67.8 | 198.4 | 137.2 | 1,734 | 247 | 15,882 | 0 |
| ymg | latew | **-3,500 (-7.7)** | -3,619 (-6.3) | 0 % | +0/-0 | 66.4 | 197.0 | 136.2 | 1,730 | 252 | 15,057 | 0 |
| band | B | - | - | 43 % | - | 58.0 | 182.9 | 142.3 | 2,345 | 303 | 21,490 | 0 |
| band | late | **-4,980 (-20.0)** | -5,183 (-18.6) | 21 % | +0/-15 | 76.0 | 200.9 | 135.2 | 1,665 | 258 | 18,955 | 0 |
| band | latew | **-6,562 (-5.5)** | -8,627 (-3.7) | 15 % | +0/-19 | 70.9 | 195.8 | 129.2 | 1,733 | 264 | 16,535 | 0 |

The patch does what it says -- band d20-27 planting 58.0 -> 76.0 (+18.0),
d20-27 idle 2,345 -> 1,665 (-680, 29 % of the window's idle closed) -- and the
farm gets *worse*:

* **+18 tiles planted costs -7.1 one-time harvests** (142.3 -> 135.2) and -44
  crop units (794 -> 750).  The PLANT+WATER chains for the late tiles come out
  of the same booked afternoon that was harvesting and walking to the shed;
  d25-d29 units fall 303 -> 258 and d25-29 revenue 21,490 -> 18,955.
* **Unsold stock at the end is 0 on every arm**, B included, so nothing is
  being stranded in the shed -- the late tiles are not "extra output that
  arrives too late", they are output that never happens.
* **Forcing wheat makes it worse, and the reason is the crop it displaces.**
  `latew` books +44 wheat units (322 -> 366) at 36.6 coins and loses 76 carrot
  units (108 -> 32) at 64.2: about +1,600 against -4,900 in crop revenue.
  Carrot is the better late crop at the band's quotes, not wheat.

So REPLANT-SCOPE's second site is also closed: the d20-27 tile gap against
ymg_aq (58.0 vs 90.7) is **not** reachable by planting more of B's own tiles
in that window.  Whatever ymg_aq does there, it is paid for by a crew and a
harvest chain B does not have, not by a relaxed horizon.

## 5. What this closes, and the one next experiment

The REPLANT-SCOPE build recommendation listed two one-scalar switches as the
places the opponent's 56-tile lead lives.  **Both are now measured and both
lose**, at t >= 4 on the band set, on top of DEV-SLOPE (development fraction,
both directions), LAND (earlier land) and WHEAT-SLOPE (more wheat tiles).  The
common cause is one line: `n_dev = _qfloor(dev_frac x n_free)` sizes the day's
development **once, at dawn, as a fraction**, so every lever that manufactures
free tiles (earlier harvest, more land, a relaxed horizon) hands them to a rule
that refuses to plant them, and every lever that raises the fraction plants
tiles the crew cannot then work.  Tile supply is not the constraint; **the
crew-turns that convert a tile into a sold unit are**, and B already runs its
crew at 10 % PASS with hours 4-12 fully booked.

**Next experiment: price the day in unit-turns, not in tiles.**  Instrument
`_derive`'s route for one B season and count, per day, the turns spent on
WATER / HARVEST / PLANT / walk / SELL against the units each produced, then
test the one arm none of the tile levers tried: **hold the tile count fixed and
cut the WATER bill** -- `SURVIVAL_WATER_ON`'s own comment says a tile whose
stream is spent is "30.3 tile-days a game of mandatory work that buys nothing",
and wheat at `c_sat` spends 3 of its 4 tile-days being watered.  If the crew is
the binding purse, the lever is turns per unit, and that is the only term of it
nothing has moved yet.

## UNVERIFIED

* Sim only.  No engine game, no ES arm, no promotion gate, no coin claim that
  survives the TWO-PURSE rule: these are paired CRN sim deltas against a
  tape-action opponent seat, which is how DEV-SLOPE, LAND and REPLANT-SCOPE
  were run and is the same descriptive ledger, not an engine result.
* The band set is all 68 TOPB2/LIVE-C boards and the ymg set all 12; no arm was
  positive at t >= 2 on either, so the TOPB3R9 sim ledger was **not** run.
* `valuation.remaining_plant_units` keeps B's clamp in k1/wf/p1 (the brief
  named two sites); only `k2v` moves it, and it lands within noise of `k2`.
* Arm `p1` harvests at `c_sat + 1` unconditionally.  For wheat (5) and carrot
  (4) that is past `CROP_MAX_YIELD_DAY`, so the extra day buys no units and the
  crop is exposed to one more weed night -- it is a control, not a proposal.
* Idle tile-hours count a tile from the first turn it holds a crop; tiles
  converted to COOP/PASTURE and never-planted tiles are excluded (same
  definition as REPLANT-SCOPE).
* `buy_cp` ("seed+buy spend" in `S/harvest_age/report.md`) tracks shed-visible
  purchases only; seeds land in `st.seeds`, not `st.shed`, so the extra seed
  bill of the short-cycle arms is **not** in that column.  It is small either
  way (10 coins a wheat cycle).
* d29 runs 23 turns (`n_turns = TPD - 1`, no eod), so its hour-23 counters are
  empty by construction.
* Switch state as measured: the runner's four plus the shipped defaults
  (`MIDDAY_PLACE_V2_ON = False`, `HORIZON_DROP_ON = True`).
