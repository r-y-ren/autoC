# TOWNADAPT — there is no step-0 town, and we already out-adapt the engine class on every product

2026-09-17 02:53–03:12Z. Research box, no src change. Worktree `kaggriculture3-townadapt` (branch
`townadapt`, off master `b9d9a7e`). `S/townadapt/{bucket,probe,report,slopes}.py`, `run_all.sh`:
two-purse product ledger on **52 boards** (ENG22 22 + V45LEG 30, seat 0, FT2 package, CRN; closes
to the coin 52/52) + bucket table over 164 control rows (ENG22 44, V45 60, TOPLEG2 60).

## 0. VERDICT — NOTHING. Town-conditional family CLOSED.

## 1. The town is EMPTY at step 0, has no multipliers, and our own tiles re-roll it
`kaggriculture.py:188` `_new_town()` returns `{"unlocked_shops": []}` — that is the entire town
object, and `:259-273` is all of it that reaches the observation. There are **no price multipliers
and no per-board base prices**: `MARKET_PARAMS` is a module constant, so every board quotes off one
curve and a town moves a price only by *consuming inventory* (`_town_consume :728-748`: each shop
instance removes `SHOP_CONSUME` every `townShopSellInterval`=4 steps — **2** units for a
single-product shop (`YARN_STORE`, `:107`), 1 otherwise; centre 1 of all but FERTILIZER per 24). Shops arrive **one per 3 days, days 3…24**, `rng.choice(sorted(SHOPS))` = uniform over 8
kinds **with replacement**, capped at `MAX_SHOP_INSTANCES=8` (`:118`, `_end_of_day :885-891`). So
P(k YARN) ~ Binom(8, 1/8): **P(≥2)=26.4 %**, P(≥3)=6.7 % (judge population 23/82 = 28 %, uniform as
claimed). That draw shares the day's RNG with weed spawning (`:871-891`), so our own tile changes
re-roll later shops — the town is not even exogenous (2026-09-06 shop-lottery).

## 2. We consume it everywhere; herd and mix already move with it
`agent/parse.py:201-205` counts the list into `view.shops` int[8] every turn; it feeds the price
forecast (`core/projector.py:187,192,255,261`), the head's inputs (`core/brain.py:195,205,240,602`),
the burst cap (`core/plan.py:3539`) and `_OPP_MIX_SHOP_W` (`plan.py:2047`). Herd/mix are not
rule-gated on shops but respond through the forecast: animal spend −6,983→**−9,350** (ENG22) and
−7,135→**−9,446** (V45) from yarn≤1 to yarn≥2 towns; r(yarn, our wool units) **+0.72**, r(yarn, our
wool price) **+0.86** over 52 boards.

## 3. Bucket table — the yarn town is where we WIN
| feature | bkt | n | win % | margin | ours | theirs |
|---|---|---:|---:|---:|---:|---:|
| YARN≥2 pooled | hi | 46 | **78.3** | +13,828 | 113,037 | 99,209 |
| YARN≥2 pooled | lo | 118 | 50.0 | +14,379 | 108,264 | 93,885 |

Per leg, hi/lo mean margin: ENG22 **+2,721**/−1,537 (n 8/36), V45 **+5,544**/+4,022 (26/34),
TOPLEG2 **+39,182**/+33,652 (12/48) — yarn is the *best* bucket on all three legs. The worst is
CARROT appetite (pooled hi 50.0 %/+6,243 vs lo 63.8 %/+20,169), a board-wealth confound (§4).

## 4. The kill — our demand-response slope BEATS theirs on all seven products
Units sold regressed on that product's per-tick town appetite, both purses, 52 boards:
| product | tick rng | OUR slope u/tick | THEIR slope | ours−theirs | our purse gap |
|---|---|---|---|---:|---:|
| CARROT | 0-9 | **+38.0 ± 3.2** | +10.5 ± 3.2 | **+27.5** | +1,512 |
| STRAWBERRY | 1-6 | +37.5 ± 5.7 | +17.8 ± 5.1 | **+19.7** | +5,772 |
| TOMATO / EGG / MILK | 0-5 / 0-5 / 1-7 | +25.4 / +19.2 / +37.7 | +15.1 / +9.8 / +28.5 | +10.2 / +9.4 / +9.1 | +577 / +1,877 / −229 |
| WHEAT | 2-8 | +27.2 ± 7.3 | +19.0 ± 51.2 | +8.2 | −6,329 |
| WOOL | 0-6 | +42.8 ± 5.9 | +41.3 ± 5.5 | +1.5 | −1,566 |

**No product has a positive ceiling for imitating the engine class** — matching their slope makes us
*less* town-adaptive on all seven. Wool, the EARLYLOSS channel, is exactly level (+1.5 ± 8), and its
"5 sheep / 109 units on a 3× yarn town" is a live board draw, not our behaviour: over 23 judge
yarn≥2 boards we sell a median ~300 wool units at 165-232/u.

## 5. Ceiling for the strongest feature (wool on yarn≥2 towns), two purses
**ENG22** (4 boards): our wool 256.2 u @ 190.1 vs their 230.8 @ 185.9 → we are **+5,811 AHEAD**, so
matching them is worth **−5,811**, negative at any dilution. **V45** (13 boards): our 257.0 @ 185.9
vs their 261.9 @ 183.6 → gap **−322**; matching at spot = 4.9 u × 185.9 = +911 gross, and with own
impact ON those 4.9 units re-price our own 257 by ≈ −0.7/u ([[melongift]] wool curve ~0.14/u per
unit) = −180 → **+731 raw**, × 26.4 % town frequency = **+193/board** (+314 at the V45 leg's own
43 %). **TOPLEG2** (6 boards): 83.3 % win, +39,182 — no deficit to buy back. Signs disagree across
legs; best diluted number **+193**, under half the +450 bar.

## 6. The last un-judged town-conditional arm, measured
`brain.PLANT_MIX_DRAIN_ON` (brain.py:880, H1 "plant into town appetite nobody has claimed") is the
only planted town switch unrun since its 2026-08-30 kill at GAIN 1.0 (t −15.4); its own note asks
for "a gain an order of magnitude smaller". At **GAIN 0.1** on ENG22, FT2 package, paired vs
`ft2_eng22.csv`: **−332/board, sd 2,745, t −0.57, flips +1/−0** (`S/lossflip/tadrain01_eng22.csv`).
REJECT. With `ENDGAME_TOMATO_ON` (plan.py:1728, dose-responsive loss) and `OPP_MIX_ON`
(plan.py:1938, off), **every town-conditional arm in the tree is now measured and rejected**. The
surviving per-product gaps are not town-conditional (WHEAT −6,329 WHEATGAP, MELON −4,089 first-mover
rent, FERTILIZER −875); the tilt that is ours to keep is already a live theta block
(`brain.residual_drain`), not a switch.
