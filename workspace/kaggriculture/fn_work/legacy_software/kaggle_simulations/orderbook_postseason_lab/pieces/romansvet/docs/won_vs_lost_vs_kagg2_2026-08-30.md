# Champion vs kagg2: what separates the wins from the losses

Data: `artifacts/theta.npy` vs `/mnt/e/_work/kaggriculture2/main.py`, 96 seeds x 2 seats
= 192 real-engine games, `--seed-base 20260828`.
**win 78.1 % | mean margin +9,013 | sd 10,866 | worst -13,117.**

Replays: `scratchpad/diag/replays_b28/<seed>_<seat>.json` (dumped by the new
`eval_vs_baselines.py --replay-dir`), profiled with `scripts/replay_profile.py`
(`--ours ours`) into `scratchpad/diag/profile_b28.csv` (384 rows x 228 cols).
The profiler's market reconstruction closes exactly: `recon_err_pct_of_rev = 0.0`
on every row, and every row's `final_money` equals the eval CSV's `mine`.

## 0. The premise is wrong: the losses are not random across seeds

| fact | value |
|---|---|
| seeds won in **both** seats | 71 / 96 |
| seeds lost in **both** seats | **17 / 96** |
| seeds split between seats | 8 / 96 |
| seat-0 vs seat-1 margin correlation over seeds | **r = 0.850** |
| between-seed margin variance / (between + within) | **92 %** |
| seat 0 | win 79.2 %, margin +9,234, sd 10,773 |
| seat 1 | win 77.1 %, margin +8,791, sd 10,953 |

92 % of our margin variance is a property of the *seed*, not of the seat or of
noise. There is a reproducible class of ~18 % of worlds we lose on. Every
"won vs lost" split below is therefore also a "which world" split, which is
what makes it actionable and also what makes it confoundable (see (d)).

## (a) Top 15 discriminating features -- OUR seat

Welch t on 150 won vs 42 lost games; `d` is Cohen's d. `[shared]` marks a
column that describes the *shared market or town* and is identical for both
seats of a game.

| # | column | won | lost | t | d |
|---|---|---|---|---|---|
| 1 | `revenue_premium_share` (% of revenue above base price) | 22.7 | 16.6 | **+7.79** | 0.98 |
| 2 | `move_rate` (% of unit actions that walk) | 38.7 | 37.8 | +5.78 | 0.77 |
| 3 | `price_d29_TOMATO` [shared] | 124.4 | 84.8 | +5.19 | 0.52 |
| 4 | `invend_FERTILIZER` (end inventory above I0) [shared] | 435.3 | 467.9 | -5.10 | -0.79 |
| 5 | `price_min_FERTILIZER` [shared] | 12.9 | 6.2 | +5.06 | 0.79 |
| 6 | `price_d29_FERTILIZER` [shared] | 12.9 | 6.2 | +5.06 | 0.79 |
| 7 | `price_mean_TOMATO` [shared] | 75.8 | 67.5 | +5.04 | 0.51 |
| 8 | `invend_WHEAT` [shared] | -437.9 | -331.3 | -4.88 | -0.73 |
| 9 | **`rev_days24_30`** | **34,139** | **25,720** | +4.61 | 0.66 |
| 10 | `pass_rate` | 18.0 | 18.5 | -4.59 | -0.77 |
| 11 | `sell_units_total` | 1,196 | 1,228 | -4.58 | -0.66 |
| 12 | `price_d29_WHEAT` [shared] | 45.5 | 42.9 | +4.37 | 0.69 |
| 13 | `sellu_early_WHEAT` (wheat units sold, days 0-15) | 46.9 | 49.5 | -4.28 | -0.86 |
| 14 | `sellrev_TOMATO` | 4,522 | 1,345 | +4.21 | 0.44 |
| 15 | `buyprod_FERTILIZER` (units bought from market) | 4.5 | 2.2 | +4.16 | 0.51 |

Requested panel that did *not* make the top 15, because it does not discriminate:

| column | won | lost | t |
|---|---|---|---|
| `hands_d5` / `hands_d10` / `hands_d20` | 7.0 / 6.3 / 11.8 | 7.0 / 6.2 / 12.0 | +0.10 / +0.46 / -0.86 |
| `hires_total`, `spend_hire` | 241, 4,842 | 242, 5,114 | -0.61, -1.11 |
| `unsold` at end (eval CSV) | 0.0 | 0.0 | 0 (never any) |
| `money_d20` | 47,100 | 46,725 | +0.26 |
| `first_day_10k` / `first_day_50k` | 13.9 / 21.3 | 13.8 / 21.7 | +1.60 / -1.16 |
| `rev_days0_7` / `rev_days8_15` | 7,320 / 28,079 | 7,353 / 28,852 | -1.95 / -1.81 |

And the ones that do, further down the list:

| column | won | lost | t | corr with margin |
|---|---|---|---|---|
| `money_d5` / `money_d10` | 724 / 3,631 | 787 / 4,665 | -3.83 / -3.70 | -0.08 |
| `plant_WHEAT` | 67.0 | 74.9 | -3.76 | **-0.275** (partial vs town wheat demand: -0.280) |
| `plant_STRAWBERRY` | 33.3 | 28.5 | +2.81 | -0.09 |
| `plant_TOMATO` | 4.7 | 3.1 | +1.86 | **+0.188** |
| `plant_total` | 141.2 | 146.6 | -3.07 | -0.281 |
| `sellu_FERTILIZER` / `sellrev_FERTILIZER` | 200 / 11,096 | 226 / 11,726 | -3.88 / -3.71 | +0.06 / -0.00 |
| `place_total` / `build_PASTURE` / `spend_animal` | 17.7 / 15.7 / 7,763 | 19.2 / 17.3 / 8,486 | -3.85 / -2.96 / -3.25 | +0.01 / -0.03 / +0.05 |
| `quad3_day` (day the 2,000-coin quadrant is bought) | 9.8 | 11.3 | -3.08 | **-0.294** |
| `quads_end` / `spend_land` | 2.9 / 2,880 | 3.0 / 3,000 | -3.08 | **-0.393** |
| `spend_product` (market buys) | 6,035 | 5,643 | +2.31 | **+0.300** |
| `sellrev_STRAWBERRY` | 41,528 | 29,816 | +3.73 | -0.01 |
| `sellday50_MILK` / `sellday50_FERTILIZER` | 13.9 / 10.3 | 15.9 / 10.9 | -3.04 / -4.04 | -0.34 / -0.01 |

Per-product economics over all 192 of our games (units, revenue, coins/unit,
correlation of that product's revenue with our margin):

| product | units | revenue | coins/unit | base | corr(rev, margin) |
|---|---|---|---|---|---|
| TOMATO | 23.3 | 3,827 | **164.5** | 60 | **+0.325** |
| WOOL | 150.8 | 22,939 | 152.2 | 200 | **+0.334** |
| STRAWBERRY | 243.0 | 38,966 | 160.3 | 120 | -0.01 |
| MELON | 74.3 | 11,582 | 155.8 | 250 | -0.11 |
| MILK | 164.8 | 20,109 | 122.0 | 160 | -0.17 |
| EGG | 72.9 | 4,001 | 54.9 | 50 | +0.04 |
| CARROT | 78.3 | 3,705 | 47.3 | 35 | +0.08 |
| FERTILIZER | 205 | 11,234 | **54.7** | 100 | **-0.003** |
| WHEAT | 190.3 | 7,973 | **41.9** | 25 | **-0.227** |

## (b) Top 15 discriminating features -- KAGG2's seat

Split by *kagg2's* result (42 kagg2 wins vs 150 kagg2 losses).

| # | column | k2 won | k2 lost | t | d |
|---|---|---|---|---|---|
| 1 | `revenue_premium_share` | 18.8 | 21.8 | -5.85 | -0.74 |
| 2 | `price_d29_TOMATO` [shared] | 84.8 | 124.4 | -5.19 | -0.52 |
| 3 | `invend_FERTILIZER` [shared] | 467.9 | 435.3 | +5.10 | 0.79 |
| 4 | `price_min_FERTILIZER` [shared] | 6.2 | 12.9 | -5.06 | -0.79 |
| 5 | `price_mean_TOMATO` [shared] | 67.5 | 75.8 | -5.04 | -0.51 |
| 6 | `invend_WHEAT` [shared] | -331.3 | -437.9 | +4.88 | 0.73 |
| 7 | `price_d29_WHEAT` [shared] | 42.9 | 45.5 | -4.37 | -0.69 |
| 8 | **`sellday50_MILK`** (median revenue day for milk) | 17.9 | 15.6 | +4.15 | 0.70 |
| 9 | `price_mean_FERTILIZER` [shared] | 58.3 | 60.9 | -4.01 | -0.65 |
| 10 | `sellrev_MELON` | 18,953 | 19,165 | -3.79 | -0.62 |
| 11 | `price_mean_WHEAT` [shared] | 38.2 | 39.2 | -3.74 | -0.62 |
| 12 | **`towncons_WHEAT`** (town wheat demand) [shared] | 433.3 | 532.6 | -3.59 | -0.58 |
| 13 | `plant_total` | 187.6 | 187.0 | +3.41 | 0.53 |
| 14 | `price_d10_STRAWBERRY` [shared] | 173.6 | 184.7 | -3.59 | -0.64 |
| 15 | `plant_WHEAT` | 129.5 | 128.0 | +2.94 | 0.56 |

Also notable on kagg2's side: `spend_land` 4,810 vs 3,933 and `quads_end`
3.5 vs 3.2 (t = +2.57) -- it buys the 4,000-coin third extra quadrant more often
in the games it wins; `place_SHEEP` 7.6 vs 5.8 and `spend_animal` 7,086 vs 6,547
(t = +2.6); `sellrev_MILK` 24,865 vs 20,405 and `sellrev_WOOL` 24,982 vs 19,554.

kagg2's baseline behaviour, for scale (means over all 192 games):

| | ours | kagg2 |
|---|---|---|
| `unit_actions` | 6,231 | **6,915** |
| `op_PASS` / `pass_rate` | 1,127 / 18.1 % | 654 / **9.4 %** |
| `plant_WHEAT` | 68.7 | **128.3** |
| `sellu_WHEAT` | 190.3 | **669.7** |
| `plant_TOMATO` / `sellu_TOMATO` | 4.7 / 23.3 | **0.0 / 0.0** |
| `sellu_FERTILIZER` | 205 | 256 |
| `op_FERTILIZE` | 165 | 61 |
| `quads_end` / `spend_land` | 2.95 / 2,880 | **3.28 / 4,125** |
| `hands_max` / `hands_d29` | 12.7 / **0** | 12.0 / **8** |

The shared-market rows on both sides tell the same story from two ends:
**the games we lose are the games in which the shared price level is low** --
fertilizer floors at 6 instead of 13, wheat is drained 100 units less below I0,
tomato ends at 85 instead of 124 -- and the games kagg2 wins are exactly those.
`towncons_WHEAT` (a pure function of the town's shop draw, which is seed data,
not agent behaviour) is 433 in kagg2's wins versus 533 in its losses: **the
losing worlds are towns whose shops do not eat wheat.** The shop mix confirms
it -- the 17 always-lost seeds average 0.74 FARMERS_MARKET and 0.62
ICE_CREAM_SHOP per town versus 1.20 and 1.04 for the rest, and 1.41
SMOOTHIE_SHOP versus 0.89.

## (c) Ranked hypotheses for a planner change

### H1 (strongest). Land allocated to wheat is a treadmill; move it to tomato.
Wheat is our worst channel by a wide margin -- 190 units at **41.9 coins/unit**
and `corr(sellrev_WHEAT, margin) = -0.227` -- while kagg2 pours 128 tiles and
670 units of wheat into the same market. Tomato is the mirror image: **kagg2
plants zero tomato and sells zero**, the market keeps `invend_TOMATO = -208`
(scarce) and `price_mean_TOMATO = 75.8` against a base of 60, and it is our
single best coins/unit product at **164.5** -- and we sell only 23 units.
Evidence lines: `plant_WHEAT` 67.0 won / 74.9 lost, t = -3.76, and the
correlation survives controlling for the seed's town wheat demand
(partial r = -0.280 given `towncons_WHEAT`); `sellrev_TOMATO` 4,522 won / 1,345
lost, t = +4.21; games with `plant_TOMATO >= 9` win 85 % at +13,400 mean margin
(n = 41) versus 78 % at +8,595 for the 83 games that plant no tomato at all.
Change: raise the crop-mix bias towards TOMATO (and away from WHEAT) as a
function of the tomato price / market inventory, i.e. let the planner see that
nobody else is selling it. Note that we already **buy** 155 wheat units from the
market per game for feed and `corr(buyprod_WHEAT, margin) = +0.227` -- buying
gluted wheat instead of growing it is already the profitable direction.

### H2. Stop selling fertilizer into a floor we create ourselves; spend it.
We sell 205 fertilizer units for 11,234 coins -- **54.7 coins/unit against a base
of 100** -- and `corr(sellrev_FERTILIZER, margin) = -0.003`: the channel is a
pure wash. It is a wash because we glut it: `corr(our fertilizer units sold,
price_min_FERTILIZER) = -0.849`, and with kagg2's 256 units on top the market
ends **+468** above I0 with the price floored at 6.2 in the games we lose versus
12.9 in the games we win (t = +5.06, d = 0.79). Meanwhile the games we win are
the ones where we sell *fewer* units (200 vs 226, t = -3.88), sell them *later*
(`sellday50_FERTILIZER` 10.3 vs 10.9) and **buy** more back (`buyprod_FERTILIZER`
4.5 vs 2.2, t = +4.16), and `op_FERTILIZE` is higher in wins (169 vs 158,
t = +3.19). Change: price fertilizer's marginal sale against its *use* value on
our own tiles and cut the sale entirely once the market inventory is above I0;
the ~370 `COLLECT_FERTILIZER` unit-turns a game (6 % of all our unit actions)
should feed our own yield rather than a 6-coin sale.

### H3. The loss is an endgame collapse: the last week is the whole margin.
`rev_days24_30` is the single largest correlate of our margin (**r = +0.404**,
34,139 won versus 25,720 lost, t = +4.61) -- and that one window's 8,419-coin
gap is **half** of the 16,690-coin distance between our mean win (+12,664) and
our mean loss (-4,027), from a window that is a quarter of the game.
Days 0-7 and 8-15 do not discriminate at all (t = -1.95, -1.81),
and `money_d20` is flat (t = +0.26): we enter the last third level and then
diverge. Two structural suspects, both cheap to test: we field **zero hands on
day 29** (`hands_d29` = 0.0 in every one of the 192 games) while kagg2 fields 8,
which forfeits ~190 unit-turns of the last selling day; and our late sales run
into prices we have already flattened (H2, and `revenue_premium_share` 22.7 vs
16.6, the top discriminator overall at t = +7.79). Change: extend the
end-of-horizon logic so the last day is still staffed and still selling, and
make the late-game sell schedule price-aware rather than inventory-clearing.

### H4. Reconsider the second land purchase (the 2,000-coin quadrant).
`quads_end` has the strongest single margin correlation of any of our own
decisions (**r = -0.393**, partial -0.423). In the 9 games where the planner
stopped at 2 quadrants the mean margin was **+28,246** and the win rate 9/9;
in the 183 where it bought the second extra quadrant it was **+8,067**. Among
the games that do buy it, buying it *late* is worse (`quad3_day` 9.8 in wins
versus 11.3 in losses, t = -3.08, r = -0.294). Read together: the purchase
competes with the early economy for cash and for hands, and a late one is a
purchase the farm could not afford. Note the opposite sign on kagg2's side -- it
spends 4,125 on land and buys the 4,000 quadrant *more* in the games it wins --
so this is a claim about our development curve, not about land in general.
Change: gate the 2nd/3rd quadrant on a payback test (spare unit-turns and spare
seed capital at the current day) rather than on a day/cash threshold.
**Weakest evidence of the four**: n = 9 is about 5 independent seeds, and the
direction is confounded with seed richness -- treat as a probe, not a landing.

### H5 (cheap, orthogonal). Reclaim the 18 % pass rate.
Our units PASS on **18.1 %** of actions (1,127 PASS ops a game) against kagg2's
9.4 %, and kagg2 gets 6,915 unit actions to our 6,231. The gap is not the hire
count -- `hires_total` 241 vs 277 and `hands_d5/d10/d20` are statistically
identical between wins and losses -- so the idle turns are a routing/queueing
loss, not a staffing one. Within our own games, `pass_rate` is lower and
`move_rate` higher in the games we win (18.0 vs 18.5, t = -4.59; 38.7 vs 37.8,
t = +5.78). The effect per game is small but it is free and it compounds with
H1-H3, which all need unit-turns.

## (d) Caveats

- **Seed richness is the dominant confound.** 92 % of our margin variance is
  between seeds and the two seats of a seed agree at r = 0.85, so almost every
  "won vs lost" contrast is partly "rich world vs poor world". The town shop
  draw is exogenous and measurably different in the losing seeds
  (`towncons_WHEAT` 433 vs 533), so any behavioural column correlated with the
  world's wheat demand inherits that signal. I controlled the crop-mix claims
  in H1 with a partial correlation against `towncons_WHEAT` (`plant_WHEAT`
  survives: -0.275 raw, -0.280 partial), but the land claim in H4 is not
  controlled and should be treated as a hypothesis only.
- **Half the top-15 columns are shared-market columns**, identical for both
  seats of a game by construction. They are diagnostics of the price level, not
  independent evidence; they appear on both tables with opposite signs for
  exactly that reason.
- **Direction of causation is not established anywhere.** The planner chooses
  `plant_TOMATO` partly *because* the tomato price is good, so the tomato result
  is at least partly "we plant tomato in worlds where tomato pays". The proper
  test is an intervention: change the bias, re-run the same 96 seeds, and read
  the paired margin.
- **Seat asymmetry is not a problem here** (79.2 % vs 77.1 %, margins +9,234 vs
  +8,791), so pooling the two seats is safe; but the two seats of a seed are
  *not* independent samples, and the t-statistics above are computed as if they
  were. Effective n is roughly halved -- read `|t| >= 3` as the threshold, not
  `|t| >= 2`.
- **One opponent, one theta, one seed base.** Everything here is against
  kagg2 specifically, and kagg2 is one randomised rung, not the objective. H1's
  tomato headroom in particular exists *because kagg2 never plants tomato*; a
  Kaggle-population opponent that does would shrink it.
- `unsold` is 0 in all 192 games and `recon_err` is 0 on all 384 profile rows,
  so neither terminal inventory nor profiler error is in play.
