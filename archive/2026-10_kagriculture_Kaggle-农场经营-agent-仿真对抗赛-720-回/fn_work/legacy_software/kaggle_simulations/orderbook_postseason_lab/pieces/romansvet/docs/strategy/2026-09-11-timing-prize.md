# The sell-timing prize, priced engine-exact on 96 live games

**Date:** 2026-09-12 (data: 96 live Kaggle replays of subs 56161192 "B" and 56143250 "hr",
48 losses + 48 wins, `S/leftover/manifest.json`).
**Code:** `S/timing/price_timing.py` -> `S/timing/rows.csv` (41,646 lot rows), `S/timing/sweep.csv`
(14,085 of our lots x 24 target hours), tables in `S/timing/timing.md`.

## Why this measurement

Two censuses (`docs/strategy/2026-09-11-expressibility.md` §3-5, `-expressibility-band.md`) found that
78-85 % of the coin our opponents move is sold on market turns where we hold no lot. That is an
*exclusion* measure, not a prize: we sell the same goods, so the cost of selling at turn 18 instead of
turn 21 is the **price difference between the two market states**, not the whole sum. This note prices
that difference.

## Engine facts that set the problem up

From the hash-verified engine
(`/root/.cache/uv/.../kaggle_environments/envs/kaggriculture/kaggriculture.py`):

* `interpreter` runs unit actions -> `_process_market` -> `_town_consume(step)` -> decay -> end-of-day.
* `_town_consume` fires when `step % 4 == 0`, **after** that step's market phase. So the market phase at
  engine step `s` sees every town consumption at a multiple of 4 that is `<= s-1`. That partitions a day
  into six price windows:

  | window | A | B | C | D | E | F |
  |---|---|---|---|---|---|---|
  | hours | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 | 21-23 (+h0) |

* Town consumption *removes* inventory, and `market_price` rises as inventory falls, so **later in the
  day is structurally richer** (five extra shop ticks between h1 and h21), while every unit **we** sell
  adds +1 to inventory and pushes the next unit's price down (`_commit_unit`).
* **There is no spoilage and no storage cost.** `_decay_plants` decays un-harvested tiles only; shed
  stock never rots. The only cost of holding a lot one more window is shed room (cap 100) and the
  end-of-day overflow discard. Measured: **0 of 14,085** of our lots would have overflowed the shed if
  deferred four turns.

Our rows land only in windows A (h1, h3), C (h10) and E (h18):

| window | our turns | our executed units | our revenue | opp executed units | opp revenue |
|---|---|---|---|---|---|
| A | 1,3 | 82,286 | 5,661,799 | 32,242 | 1,950,411 |
| B | - | 0 | 0 | 14,543 | 1,367,733 |
| C | 10 | 2,805 | 255,279 | 17,620 | 2,097,533 |
| D | - | 0 | 0 | 17,141 | 1,641,781 |
| E | 18 | 51,018 | 6,455,833 | 27,613 | 2,337,692 |
| F | - | 0 | 0 | 42,460 | 3,110,451 |

## Method, and exactly how far it is "first order"

* Executed units and revenue per turn are the **engine's**: `scripts/replay_profile.py::_simulate_market`
  re-runs the per-unit lockstep market phase of one transition (shed stock, both seats interleaved,
  `_commit_unit` semantics). We call it once per transition with a fresh accumulator pair to get a
  per-turn, per-item breakdown. Whole-game totals reproduce the replay's own money.
* A counterfactual lot is priced with the engine's own `market_price` curve against the **recorded**
  market inventory at the alternative turn (the pre-market state of that engine step: the opponent's
  orders and every town tick up to that point exactly as they happened), committing one unit at a time
  and raising inventory by 1 per unit unless the price floored at 1.
* When a lot moves **later** we remove our own units from the later recorded state (they were not sold
  at the earlier turn in the counterfactual). Because the engine's orders are quantity orders against
  shed stock, the number of units the opponent commits is price-independent, so this adjustment is
  **exact**, not approximate.
* **What we do not model, and it matters:** (i) our units are not interleaved with the opponent's inside
  the alternative turn (the engine alternates seats unit-by-unit); (ii) the opponent is closed-loop and
  would see a different market and react; (iii) the *opponent's* revenue change is ignored entirely.
  For **our** revenue the error is only (i) and (ii).
* Baseline for every delta is the **same first-order pricing of the same units at the actual turn**, so
  the delta is purely the market-state difference; the engine-exact actual revenue is carried alongside.
* Moving a lot inside a day leaves the cumulative inventory at every turn outside `[src, dst)` unchanged,
  so a uniform policy (move *all* h1 lots, or *all* h18 lots) is internally consistent, and the h1 and
  h18 moves are independent of each other.

Variants per lot (day d, hour h, item, u units): **(a)** h -> h+4 (next window); **(b)** h -> 7 if h==10,
14 if h==18, else h-4 (the SELL5 turns); **(c)** `u//2` at h, the rest at h+4. Plus a full sweep of every
target hour 0-23.

## Result 1 -- the three requested variants

| variant | set | n | mean delta/game | median | p90 | worst | games > 0 | % of our sell revenue | paired t |
|---|---|---|---|---|---|---|---|---|---|
| (a) +4 / next window | LOSSES | 48 | **+759** | +724 | +2,660 | -1,719 | 60 % | 0.60 % | 3.4 |
| (a) +4 / next window | WINS | 48 | **+1,049** | +1,006 | +2,740 | -1,051 | 77 % | 0.80 % | 5.6 |
| (b) -4 / SELL5 (7,14) | LOSSES | 48 | **-346** | -358 | +420 | -1,623 | 27 % | -0.27 % | -4.0 |
| (b) -4 / SELL5 (7,14) | WINS | 48 | **-508** | -462 | +80 | -2,714 | 17 % | -0.39 % | -6.1 |
| (c) half now / half next | LOSSES | 48 | **+247** | +168 | +1,097 | -896 | 58 % | 0.20 % | 2.4 |
| (c) half now / half next | WINS | 48 | **+332** | +336 | +1,002 | -647 | 67 % | 0.25 % | 4.3 |

Losses where the delta alone covers the loss margin: **(a) 5/48**, **(b) 0/48**, **(c) 1/48**
(narrow losses under 2,000 coins: 4/14, 0/14, 1/14).

A hindsight oracle that picks the best of {stay, a, b, c} **per lot** gets +2,988/game on losses and
covers 21/48 — but it gets +2,806/game on **wins** too, so 94 % of that oracle is selection over
per-lot deltas of a few hundred coins, not a defect. Treat it as a ceiling, not a plan.

## Result 2 -- the full turn sweep (which single turn is worth the most)

Mean delta per game if every lot at the source hour moved to the target hour (96 games):

**from h1** (90.8 lots/game, 856 units/game)

| target | h2 | h3 | h5 | h6 | h9 | h10 | h13 | h14 | h17 | h18 | h21 | h22 | h0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| delta/game | +191 | +76 | +635 | +529 | +834 | +668 | **+881** | +502 | +663 | +518 | +123 | -401 | -1,107 |

**from h18** (45.9 lots/game, 531 units/game)

| target | h9 | h13 | h14 | h17 | h19 | h20 | h21 | h22 | h23 | h0 |
|---|---|---|---|---|---|---|---|---|---|---|
| delta/game | -1,174 | -68 | -405 | +531 | +34 | -525 | **+911** | +250 | +190 | -4,777 |

**from h10** (9.8 lots/game, 29 units/game): best target h17, **+36/game** — negligible, the h10 row is
tiny (2,805 units over 96 games, 2 % of our volume).

Per move, split by result:

| move | LOSS mean (t) | WIN mean (t) | losses covered alone |
|---|---|---|---|
| h18 -> h21 | **+1,096** (6.8) | +726 (5.1) | 7/48 |
| h1 -> h13 | +739 (6.0) | +1,023 (7.4) | 5/48 |
| h1 -> h5 | +490 (5.8) | +781 (7.3) | 3/48 |
| h18 -> h22 | +249 (1.3) | +252 (1.8) | 3/48 |

Best fixed re-schedule the sweep supports (h1->h13, h18->h21, h10->h17; the moves are independent):

| set | n | mean delta/game | median | paired t | d0-9 | d10-14 | d15-29 | losses covered |
|---|---|---|---|---|---|---|---|---|
| LOSSES | 48 | **+1,876** | +1,752 | 8.0 | +9 | -186 | **+2,052** | 13/48 (8/14 narrow) |
| WINS | 48 | **+1,783** | +1,687 | 7.9 | -3 | -209 | **+1,995** | — |

## Result 3 -- day bands and products

Bands (mean delta per game, our seat):

| band | set | our units/game | our revenue/game | (a) +4 | (b) -4 | (c) split |
|---|---|---|---|---|---|---|
| d0-9 | LOSS | 225 | 14,725 | +9 | -41 | +4 |
| d0-9 | WIN | 226 | 14,692 | -0 | -37 | -2 |
| d10-14 | LOSS | 108 | 10,945 | -82 | -13 | -40 |
| d10-14 | WIN | 114 | 10,894 | -75 | -13 | -38 |
| d15-29 | LOSS | 1,081 | 100,778 | **+831** | -291 | +283 |
| d15-29 | WIN | 1,083 | 105,735 | **+1,125** | -458 | +372 |

**d15-29 carries essentially 100 % of the prize.** d0-9 is exactly zero (the market is still near I0 =
10,000 and the curve is flat there); d10-14 is slightly *negative*.

Products (all 96 games, our seat, delta per game):

| product | units/game | revenue/game | (a) +4 | (b) -4 | (c) split | carrier of the best move |
|---|---|---|---|---|---|---|
| STRAWBERRY | 236.1 | 33,889 | +284 | -24 | +62 | **+879 on h1->h13** |
| WOOL | 128.0 | 19,513 | **+677** | -65 | +277 | **+523 on h18->h21** |
| MILK | 199.1 | 25,369 | +72 | -279 | +29 | **+373 on h18->h21** |
| TOMATO | 27.9 | 3,180 | +55 | -41 | +27 | +48 on h18->h21 |
| MELON | 85.9 | 13,787 | +14 | 0 | +4 | +12 |
| EGG | 114.6 | 5,952 | +4 | -10 | 0 | +7 |
| WHEAT | 315.6 | 11,518 | -22 | -6 | -14 | +28 |
| CARROT | 108.1 | 5,378 | -66 | -2 | -32 | -14 |
| FERTILIZER | 202.6 | 10,297 | -113 | 0 | -64 | -161 |

The prize is **thin-market, high-base goods**: WOOL (base 200, T 105), MILK (160, T 122), STRAWBERRY
(120, T 100). WHEAT / CARROT / FERTILIZER (T 400/450/200, flat curves) are *negative* — deferring them
just lets the town tick be spent on someone else's units.

## Result 4 -- the opponent control: is any of THEIR edge timing?

Force each of their lots onto the nearest of our turns {1,3,10,18} in the same day:

| set | their revenue/game | lots/game | units/game | mean delta/game | median | lots that lose |
|---|---|---|---|---|---|---|
| games we LOST | 134,989 | 292 | 1,593 | **+3,288** | +3,020 | 9 % |
| games we WON | 125,545 | 282 | 1,566 | **+3,309** | +3,198 | 9 % |

The sign is **positive**: on our schedule they would have earned *more*, not less. This estimate is
biased upward (each of their lots is priced against a market that does not carry their other lots, and
they hold ~292 lots per game), so read it as "their window choice is worth **at most** zero to them".
Identical on wins and losses. **None of the opponent's edge is window selection.** Their coin comes from
volume and mix (1,593 units/game vs our 1,414 and a richer basket), not from which turn they quote on.

## Judgement

The sell-timing prize is **real, highly significant, and an order of magnitude below the loss-margin
scale — and it is not loss-specific**. The best fixed re-schedule our own rows admit (h1->h13,
h18->h21) is worth **+1,876 coins/game on the 48 losses (t 8.0, 1.5 % of our 126k sell revenue)**
against a mean loss margin of 5,186; it covers **13/48 losses** and 8 of the 14 narrow ones, but it is
worth **+1,783 on the 48 wins** — a 93-coin loss/win difference, i.e. a level uplift, not the thing that
decides games. Every coin of it is in **d15-29** (d0-9 is exactly zero, d10-14 slightly negative) and in
the **thin-market goods — WOOL, MILK, STRAWBERRY**; WHEAT, CARROT and FERTILIZER are negative and should
stay on the early row. The single most valuable turn is **h18 -> h21** (+911/game overall, +1,096 on
losses, t 6.8, carried by WOOL +523 and MILK +373): it is the only genuinely *free* move, because our
entire buy row sits at h0-h3 (4,160 of our 4,160 non-SELL orders in a 12-game sample) and h21 cash still
lands before the next day's buys — whereas the nominally-larger h1 -> h13 (+881/game, STRAWBERRY +879)
would starve that same morning buy row of the cash it is funded by, a cost this measurement does not
price. Direction matters more than schedule density: **later pays, earlier does not** — the SELL5 turns
7/14 are strictly worse (-346/game on losses, t -4.0), so variant (b) is falsified as a revenue play.
And the symmetric measurement kills the exclusion framing outright: forcing the opponent's 292 lots/game
onto *our* four turns would have paid them **more** (+3,288/game, identical on wins and losses), so the
78-85 % coin share they move in windows we skip is not an edge they are extracting — it is an accounting
artefact. Recommendation: take h18 -> h21 for WOOL/MILK/TOMATO in d15-29 as a small, free, testable
switch (~+1.1k/game on losses, worth ~0.2 pt of win rate at the 298 pts/logit calibration), and close
the sell-timing family for anything larger.

## Reproduce

```
export JAX_PLATFORMS=cpu
python S/timing/price_timing.py S/leftover/manifest.json -j 8 --sweep   # ~30 s, writes rows.csv, sweep.csv, timing.md
python S/timing/price_timing.py --tables                                # tables only
```
