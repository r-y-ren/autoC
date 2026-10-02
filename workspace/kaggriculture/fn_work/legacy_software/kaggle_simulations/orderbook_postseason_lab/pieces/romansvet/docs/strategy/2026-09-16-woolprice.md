# WOOL at price 1: why the herd keeps going, and what retargets when a price collapses

**Q1 — we do NOT keep buying sheep once wool is at 1.** Across 104 pinned-town games and the live episode the user named (109698269), sheep are bought
on days 0-14 and **never** on a day whose wool quote is at or below 50: **0 of 717 purchases**. What continues is *keeping* the herd, and the engine
gives no way out — SHEEP is not in `PRODUCTS`, so there is no SELL_ANIMAL, and a PASTURE tile cannot be replanted. The 500 coins are sunk; the only
alternative is starving the animal. Keeping it pays, because **a sheep is a fertilizer machine with a wool byproduct**: over the 13 floored days
d17-d29 of 109698269 our five sheep earned **2,138 coins of fertilizer and 87 of wool** against **1,018 of feed wheat** — net **+1,207**, wool **3.9
%** of the gross. Per sheep-day at the floor: +0.7 wool ≈ 1.4 coins, +1.0 fertilizer ≈ 35, −0.4 wheat ≈ −17; on its wool alone a sheep is **−16
coins/sheep-day**, on the whole animal **+19**. The labour already retargets on the floor day itself — FEED on sheep tiles 5/day → 2/day, CARE 5/day →
1.2/day on exactly d17 — because `care_pays = price[WOOL] > price[WHEAT]` (`plan.py:7184`) goes false. The wool that still arrives is harvested and
dumped because at price 1 a sale is **free disposal**: the engine does not add a $1 sale to market supply (`kaggriculture.py:659-661`), and the turn
would otherwise PASS. Holding for recovery is not available — 3.3 wool/day of production against a 1/day town drain, so `mkt_inv` sat at I0+59 for 13
straight days. **The defect is timing, not blindness:** the price response is reactive, it reads the spot quote, and through the whole buying window
(d0-d14) wool quotes 158-219 because the pot has not been filled yet.

**Q2 — PARTIAL** (§3): strong retarget at the head and at the labour gate, **none** at the acquisition bound, and the rival's supply is absent
everywhere.

## 1. Mechanics (`kaggle_environments/envs/kaggriculture/kaggriculture.py`)

WOOL is `{base 200, I0 10000, T 105, above_func "sq", above_target 3.20}` (:49): on the glut arm `price = 200 − 0.058050·(inv − I0)²`, floored at
`PRICE_FLOOR = 1` (:39, :206). The arm is **quadratic** — MILK's is linear, and that is what makes wool the most crash-prone product in the game. The
**pot is shared**: 59 net units across BOTH seats floors it, against ~236 units of two-herd season production (ep 109698269), and each of the last ten
units before the floor takes ~6 coins off the quote for both seats.

| net units above I0 | 0 | 20 | 30 | 40 | 50 | 55 | **59** |
|---|---:|---:|---:|---:|---:|---:|---:|
| WOOL quote (sq, T 105) | 200 | 177 | 148 | 107 | 55 | 24 | **1** |
| MILK quote (linear, T 122) | 160 | 118 | 97 | 76 | 55 | 45 | 36 |

Sales at 1 do not raise inventory (:659), so the floor absorbs. Recovery is town drain only (:733-749): the town centre takes **1 wool/day** and each
unlocked YARN_STORE instance **12/day** (6 ticks × mult 2); shops unlock every 3 days from a uniform draw over 8, so a YARN_STORE is a 1-in-8 lottery.
With none unlocked the quote sits at 1 and lifts to ~5 each dawn on the one drained unit — the realised 5.0 rows on d19/d25 below. SHEEP (:22): 500
coins, PASTURE, `first_yield_day 6`, `interval 3`, `max_held 6`; per fire `yield += 1 + care_bank`, the bank banked only on a cared **and** fed day
and cashed only on a fed fire day, but **the base 1 is added whether or not it was fed** (:820-829). It escapes at `consecutive_unfed >= 2`, so
survival is one wheat every other day, and `fertilizer_available` is set **every day regardless of feed** — 1 FERTILIZER per animal-day for one
COLLECT turn. That asymmetry is the whole of Q1's answer.

## 2. Behaviour

**Live episode 109698269** (sub 56277270 = seat 1, 96,301 vs `lcx666` 99,476; `S/woolprice/ep_wool.py` and `ep_cost.py`, market phase reconstructed
with the verified `replay_profile._simulate_market`):

| day | 10 | 13 | 14 | 15 | 16 | **17** | 18 | 20 | 25 | 29 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wool quote | 187 | 167 | 158 | 93 | 43 | **1** | 1 | 1 | 1 | 1 |
| our sheep / placed | 4 / **1** | 5/0 | 5/0 | 5/0 | 5/0 | 5 / **0** | 5/0 | 5/0 | 5/0 | 1/0 |
| our wool sold @ | 4 @186 | 4 @165 | 5 @154 | 10 @74 | 4 @40 | 9 @1.4 | 8 @1.5 | 6 @1.7 | 1 @5.0 | 2 @3.0 |
| THEIR wool sold @ | 0 | 0 | 12 @122 | 0 | **20 @3.7** | 0 | 12 @1.0 | 8 @1.0 | 8 @1.0 | 11 @1.0 |
| our FEED / CARE | 4/4 | 5/5 | 5/5 | 5/5 | 5/5 | **0/0** | 5/2 | 5/1 | 0/0 | 0/0 |

Last sheep placed **d10** at a 187 quote; floor reached **d17**, never left; **zero** placed after it. It is **their** dump that tips it — 60 units to
our 32 by d17, and their 20-unit sale on d16 takes the quote 43 → 1. Season: ours 75 u / 4,160 coins, theirs 161 u / 7,098. **104 pinned-town boards**
(`S/topledger3` 36 + `S/melon_decomp` 68, engine-validated to the coin; `S/woolprice/instrument.py`, `days.csv`): 50/104 reach a wool dawn quote ≤ 2,
mean first floor day **18.7**, 8.6 floor days a board, **0 of 717 sheep bought** on a day quoting ≤ 50; pooled purchases peak at d8 (1.45) and d10
(2.19) and are **0.00 from d17 on**; units sold before the first floor day ours 42.0, **theirs 56.0** — the rival is the larger half on the mean board
too.

## 3. The planner: what retargets, and what cannot

| stage | reads a price? | code | verdict |
|---|---|---|---|
| `animal_want` (how many, which) | **YES, strongly** | `brain.py:552-553` (`(inv−I0)/T`, `price/base`), `:603` (`mean(price/base)`), `:1010-1011`, `:1031-1033` | live |
| labour: CARE / FEED | **YES** | `plan.py:7184` `care_pays`; `:7186` `feed_want` → `must_feed` | fires on the floor day |
| budget: k-th animal's value | **YES**, forward + own pipeline | `plan.py:6909` `inv_h`, `:6948` `_stream_rev` | own supply only |
| **gate `acquire_ok`** | **NO in practice** | `plan.py:7426-7428` `ub_coins`, spot `price[a_prod]` | **fertilizer-dominated** |
| the rival's supply, anywhere | **NO** | `OPP_SUPPLY_ON :1832`, `OPP_MIX_ON :1897`, both OFF | both **refused** |

**The head really does retarget** (`S/woolprice/decode_price.py`, 2,400 real dawn observations, theta B, only WOOL's quote and inventory changed): at
`price[WOOL]=1, mkt_inv=I0+59` the sheep want goes to **exactly 0 on every row** (mean 0.0708 → 0.0000) and the total animal ask falls **730 → 320**;
at `price[WOOL]=400, mkt_inv=I0−300` the sheep want goes **0.0708 → 0.8167** (×11.5), ask 730 → 2,482. Live and strong — it just never sees a low wool
price while the herd is being bought. **`acquire_ok` cannot turn on the product's price at all**: `ub_coins = ub_units·price[product] +
ub_fert·price[FERT] − ub_feeds·price[WHEAT]`, and the fertilizer term is 1.7-3.5× the product term.

| board | SHEEP fires × quote | + fert | − feed | `ub_coins` vs cost 500 |
|---|---:|---:|---:|---:|
| d8, clean market | 6 × 200 = 1,200 | 2,100 | −500 | 2,800 ✓ |
| d12, +50 units | 4 × 55 = 220 | 1,700 | −400 | 1,520 ✓ |
| **d17, quote 1** | **3 × 1 = 3** | **1,200** | **−275** | **928 ✓ still buys** |

`OPP_SUPPLY_ON` / `OPP_MIX_ON` are the two attempts to put the rival's stream into this pricing; both refused at −430 … −3,986 with the two-purse
signature — our purse falls, **theirs rises** (`docs/strategy/2026-09-11-oppsupply-screen.md`).

## 4. `ANIMAL_BUY_FWD_ON` — built, default OFF, **measured inert, REJECT**

Price the acquisition bound's product term on the sales-window curve the units are actually sold on (`PJ.inv_at_day + _pipeline_units`, the `inv_h`
`_candidates` and `CARE_HOLD_ON` already use), as a `min` against spot — a CARE wants a price floor, a PURCHASE wants a ceiling. `plan.py`
`ANIMAL_BUY_FWD_ON` beside `CARE_HOLD_ON` + 12 lines in `_derive`; `tests/test_animal_fwd.py` 4 passed, incl. the whole-plan sha256 of six pinned
boards against a pristine `git archive aed911c src` subprocess. **Screen** (`S/woolprice/run_screen.sh`, `pair.py`; 40 TOPB2 pinned boards, theta B,
paired vs the shipped pair): **Δ = +0 coins, 0 win / 0 loss / 40 ties**, both purses unchanged to the coin. Structurally inert — it cannot refuse an
animal (table above), and the only other channel, `v_place = ub_coins[place_kind]` (`plan.py:7948`), never binds a turn contest. **The finding is
worth more than the arm: no correction to a product's own price can change B's herd, because the herd is not bought on its product.**

**Would a wool retarget differ from the losers?** No, and now mechanically rather than by prior. Every refused lever (FERT_RESERVE −32.7k, OPP_SUPPLY
−430…−3,986, CARE_HOLD −238, carrot hold) withheld supply from a shared pot and handed the rival the price. A wool retarget is worse off: wool is **4
%** of what the herd earns after the floor, so even a perfect one only redirects the 500-coin purchase — and `2026-09-14-herd-growth-screen.md` §1
already measured every version of one fewer sheep / one more cow in d3-d11 at −24 … −2,697 (`cow68p1`, displacing −0.56 sheep, −1,009 t −3.22). **The
wool-price family closes on the acquisition side.** What stays open is what the mechanism doc left open: **wool per sheep-day 0.930 against a 1.333
ceiling**, a care-cadence question no price touches.

Files: `S/woolprice/{instrument.py,days.csv,ep_wool.py,ep109698269.csv,ep_cost.py,decode_price.py,run_screen.sh,screen_tree.py,
pair.py,woolfwd_{off,on}.csv,screen*.log}`.
