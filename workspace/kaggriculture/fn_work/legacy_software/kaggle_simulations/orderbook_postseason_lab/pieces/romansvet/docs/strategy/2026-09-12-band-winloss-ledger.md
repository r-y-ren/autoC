# §120 — What the −13.5k d15-29 win/loss gap is made of, and whether the knobs reach it

2026-09-12. Opens the question §118 (`2026-09-12-nexthigh-anatomy.md`) left standing: B's band
games are decided in d15-29 (NEXTHIGH wins recover +28,002 there against losses' +14,442, Δ +13,560
t 6.29, r 0.984 with the final margin) while d10-14 is a flat tax paid identically on both. That
told us *when*. It did not tell us *what* — units, price, product, or whether a theta can move it.

**Tool.** `S/bandledger/ledger.py` (`run` / `report` / `tables` / `shops`). It replays B on the 60
pinned-town boards of NEXT30 (2567-2750) + NEXTHIGH (2782-2946), both seats = **120 games**, on the
`S/simscreen/screen.py` recipe the anatomy scripts use, and scans **per day** out of the sim state
what the money curve could not show: per-product units sold and sale revenue **per seat**, shed per
item, tiles by crop, animals by type, fertilised tiles, weeds, quadrants, market inventory and
quoted price, the town's shop draw, and the macro B decodes that day (grow_mult, press, dev_weight,
hire_bias, crew_target, animal_want, forward_days). The per-product sale ledger is not in `State`,
so `run` installs two extra counters (`sold_np`, `sold_rp`, int32 [2, N_ITEMS]) on an **extended**
State plus a copy of `rollout._market_turn` that fills them — monkey-patched at run time, nothing
under `src/` touched. Verified: every board's d29 money reproduces `S/nextband/anatomy_band_B.csv`
and `S/nexthigh/anatomy_band_B.csv` **to the coin**.

Outputs: `S/bandledger/{ledger.md, per_board.csv, per_product.csv, raw_B.npz}`.

---

## 1. The gap reproduces, and it is entirely on THEIR side of the ledger

120 games, 73 wins / 47 losses (NEXTHIGH alone: 32/28, Δ d15-29 +12,699 t 8.67, which is §118's
+13,560 re-measured per seat rather than per board).

| slice | d0-9 | d10-14 | **d15-29** | margin d29 |
|---|---:|---:|---:|---:|
| B's 73 WINS | +3 | −16,411 | **+24,487** | +8,079 |
| B's 47 LOSSES | −66 | −17,420 | **+13,048** | −4,438 |
| win − loss | +69 (t 0.57) | +1,009 (t 2.57) | **+11,439 (t 11.35)** | +12,517 |

Split the d15-29 money change into the two seats:

| d15-29 money change | wins | losses | Δ | t |
|---|---:|---:|---:|---:|
| **ours** | +90,668 | +95,063 | **−4,395** | −1.10 |
| **theirs** | +66,181 | +82,015 | **−15,834** | −4.08 |

**B earns *more* coins in d15-29 on the boards it loses.** The whole discriminator is the
opponent's own d15-29 earnings: the clone books 82.0k on the boards B loses and 66.2k on the boards
B wins. This is not "we sold less" and it is not "we sold cheaper because they dumped first" — it
is **"they sold dearer"**.

## 2. Volume × price, by product (d15-29, 120 games)

Realised price = revenue / units. Volume effect = Δn·p̄, price effect = n̄·Δp.

### OURS
| product | n win | n loss | Δn | price win | price loss | Δp | rev win | rev loss | Δ rev | vol eff | price eff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| WHEAT | 168.8 | 176.4 | −7.5 | 39 | 39 | +1 | 6,649 | 6,821 | −172 | −295 | +123 |
| CARROT | 131.6 | 97.6 | +34.0 | 59 | 52 | +7 | 7,779 | 5,103 | +2,676 | +1,892 | +784 |
| TOMATO | 39.7 | 12.7 | +27.0 | 131 | 137 | −6 | 5,188 | 1,735 | +3,453 | +3,610 | −157 |
| **STRAWBERRY** | 197.1 | 253.9 | −56.8 | 112 | 145 | −33 | 22,089 | 36,944 | **−14,855** | −7,312 | −7,543 |
| MELON | 90.9 | 83.6 | +7.3 | 157 | 165 | −8 | 14,299 | 13,832 | +467 | +1,176 | −709 |
| EGG | 93.9 | 95.4 | −1.5 | 52 | 52 | +0 | 4,866 | 4,931 | −64 | −78 | +13 |
| MILK | 125.8 | 139.3 | −13.5 | 102 | 98 | +4 | 12,829 | 13,702 | −873 | −1,356 | +482 |
| WOOL | 123.6 | 106.8 | +16.8 | 146 | 123 | +23 | 18,086 | 13,172 | +4,914 | +2,261 | +2,653 |
| FERTILIZER | 119.8 | 107.9 | +11.9 | 30 | 29 | +0 | 3,562 | 3,166 | +396 | +351 | +44 |
| TOTAL | 1,091 | 1,074 | +17.5 | 87 | 93 | −5 | 95,348 | 99,407 | −4,060 | +1,577 | −5,637 |

### THEIRS
| product | n win | n loss | Δn | price win | price loss | Δp | rev win | rev loss | Δ rev | vol eff | price eff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| WHEAT | 231.2 | 226.0 | +5.2 | 39 | 39 | −0 | 9,024 | 8,925 | +100 | +204 | −105 |
| CARROT | 81.1 | 84.0 | −2.9 | 51 | 47 | +5 | 4,168 | 3,907 | +261 | −143 | +404 |
| TOMATO | 14.6 | 11.9 | +2.7 | 153 | 215 | −62 | 2,241 | 2,561 | −321 | +502 | −823 |
| **STRAWBERRY** | 249.9 | 248.3 | **+1.6** | 75 | 122 | **−47** | 18,737 | 30,262 | **−11,525** | +155 | **−11,681** |
| MELON | 2.2 | 0.0 | +2.2 | 187 | – | – | 414 | 0 | +414 | +207 | +207 |
| EGG | 53.9 | 63.3 | −9.5 | 50 | 52 | −1 | 2,720 | 3,287 | −567 | −484 | −83 |
| MILK | 170.4 | 177.6 | −7.2 | 70 | 86 | −16 | 11,933 | 15,356 | −3,423 | −561 | −2,863 |
| WOOL | 134.4 | 137.5 | −3.1 | 101 | 99 | +2 | 13,571 | 13,585 | −13 | −311 | +298 |
| FERTILIZER | 203.2 | 211.0 | −7.8 | 33 | 34 | −1 | 6,692 | 7,205 | −512 | −260 | −252 |
| TOTAL | 1,141 | 1,160 | −18.7 | 61 | 73 | −12 | 69,502 | 85,088 | −15,586 | −1,254 | **−14,333** |

**The clone's d15-29 volume is a constant and its price is the variable.** It sells 249.9 strawberry
units on the boards B wins and 248.3 on the boards B loses — Δ +1.6 units on 248 — while its
realised strawberry price moves 75 → 122. 92 % of the clone's Δ revenue is a *price* effect
(−14,333 of −15,586). It is an open-loop tape: it dumps the same basket either way and the market
decides what that basket is worth.

d0-14 is flat at the product level too (ours: wheat 136 vs 133 units, strawberry 6.1 vs 6.3, milk
51.8 vs 52.0; theirs: melon 69.7 vs 71.5 at an identical 242) — the §99/§118 "flat tax" survives
the finer cut.

### The margin gap by product — Δ(ours) − Δ(theirs)
| product | ours Δrev | theirs Δrev | **margin Δ** |
|---|---:|---:|---:|
| WOOL | +4,914 | −13 | **+4,927** |
| TOMATO | +3,453 | −321 | **+3,773** |
| MILK | −873 | −3,423 | **+2,550** |
| CARROT | +2,676 | +261 | **+2,415** |
| FERTILIZER | +396 | −512 | +908 |
| EGG | −64 | −567 | +502 |
| MELON | +467 | +414 | +53 |
| WHEAT | −172 | +100 | −272 |
| **STRAWBERRY** | −14,855 | −11,525 | **−3,330** |
| **sum** | | | **+11,527** (measured +11,439; residual = d15-29 spend) |

Strawberry is the biggest single line on both sides and it nets **against** the wins: B's own
strawberry book is *larger* on the boards it loses (36.9k vs 22.1k) and larger than the clone's
there too. What wins boards is the **rest of the basket** — wool, tomato, milk, carrot — not
strawberry.

## 3. Board covariates: the win is mostly a town-shop lottery

Every town holds exactly 5 of the 8 shops. Presence of one shop, over the 120 games (55 distinct
towns):

| shop (its sinks) | absent: margin / win % | present: margin / win % | Δ margin |
|---|---:|---:|---:|
| **SMOOTHIE_SHOP (strawberry, milk)** | **+7,346 / 80.0 %** | **−993 / 41.7 %** | **−8,339** |
| YARN_STORE (wool) | +2,152 / 65.4 % | +5,078 / 52.4 % | +2,925 |
| PET_CAFE (carrot) | +1,433 / 54.5 % | +4,186 / 64.5 % | +2,753 |
| PIZZA_SHOP (wheat, tomato, milk) | +1,870 / 51.7 % | +4,398 / 69.4 % | +2,528 |
| BRUNCH / BAKERY / ICE_CREAM / FARMERS | +3,966…+4,391 | +1,812…+2,080 | −1,992…−2,351 |

SMOOTHIE_SHOP is the covariate, and it holds **inside each family**, so it is not a NEXT30 /
NEXTHIGH artefact:

| family | stratum | n | margin | t | d15-29 | win % |
|---|---|---:|---:|---:|---:|---:|
| NEXT30 | no smoothie | 36 | +7,555 | +6.40 | +23,232 | 88.9 |
| NEXT30 | smoothie | 24 | −1,057 | −1.07 | +15,765 | 37.5 |
| NEXTHIGH | no smoothie | 24 | +7,032 | +3.58 | +24,179 | 66.7 |
| NEXTHIGH | smoothie | 36 | −951 | −0.86 | +16,828 | 44.4 |

Point-biserial ρ with the win over all 120: `shop6` (SMOOTHIE) **−0.304** (ρ with margin **−0.475**),
`shop4` (PET_CAFE) +0.262 / +0.331, strawberry price at d15 −0.364 / −0.529, at d22 −0.386 / −0.487,
market strawberry inventory at d15 +0.361 / +0.529. Weeds, the seed word and the opponent's rating
are all **below** 0.3 with the margin (weeds and seed do not reach the top 18 at all).

Only the **shop draw** is exogenous on that list — the strawberry price and inventory columns are
themselves consequences of the game. So: **yes, there is a lottery at |ρ| > 0.3, and it is the town's
5-of-8 shop draw, one shop in particular.**

**The mechanism.** SMOOTHIE_SHOP is the strawberry+milk sink. With it in town, the strawberry
market is drained every tick, the price never collapses, and the clone's fixed ~249-unit late
strawberry dump cashes at 105 instead of 81 — the clone's whole edge, handed to it by the board.
Without it, strawberry inventory piles up (both seats dump into one pot), the quote falls to 37 by
d22, and the *open-loop* seat eats the collapse while B, which reads the price, does not.

## 4. Does B already react? Yes — and it reacts into the wrong product

Same theta on every board, so all knob differences are the observation talking. Means over d15-29,
our seat, win boards vs loss boards (120 games):

| knob | win | loss | Δ | t |
|---|---:|---:|---:|---:|
| **press3 (STRAWBERRY sell pressure)** | 31.35 | 14.77 | **+16.58** | **+5.13** |
| **grow_mult3 (STRAWBERRY)** | 186.7 | 253.1 | **−66.5** | **−4.22** |
| press2 (TOMATO) | 5.69 | 9.47 | −3.77 | −3.75 |
| grow_mult2 (TOMATO) | 475.7 | 402.0 | +73.8 | +2.60 |
| grow_mult1 (CARROT) | 438.1 | 375.4 | +62.7 | +2.87 |
| grow_mult0 (WHEAT) | 528.1 | 496.9 | +31.3 | +2.87 |
| animal_want2 (SHEEP) | 0.06 | 0.01 | +0.05 | +2.57 |
| hire_bias | −82.5 | −88.0 | +5.5 | +2.05 |
| crew_target | 11.30 | 11.39 | −0.08 | −1.82 |
| dev_weight | 18.70 | 19.07 | −0.37 | −1.37 |

B moves these a long way board to board (grow_mult3 spans 118→477 with sd 84 across boards;
press3 spans 0.6→85.6): the trained genes are **live and board-reactive inside the window**, which
is what §114 said they should be. The direction is the problem. Put the same knobs next to the
shop draw:

| ours, mean over d15-29 | non-smoothie town | smoothie town |
|---|---:|---:|
| grow_mult3 (strawberry) | 190.0 | **235.4** |
| press3 (strawberry) | 31.1 | **18.6** |
| strawberry tiles | 16.9 | **19.3** |
| tomato tiles | 4.78 | **2.27** |
| sheep | 7.26 | **6.35** |
| carrot tiles | 6.59 | 5.64 |

On the town that keeps the strawberry price up, B **tilts the late board further into strawberry
and holds it longer** (grow_mult3 +45, press3 −12.5, +2.5 tiles) — and pays for it elsewhere. The
d15-29 margin, product by product, smoothie town minus non-smoothie town:

| product | no-smoothie margin | smoothie margin | Δ | note |
|---|---:|---:|---:|---|
| TOMATO | +3,096 | −157 | **−3,252** | our units 40 → 18 at the same price 132; confounded (PIZZA 0.60→0.43, FARMERS 0.53→0.37) |
| WOOL | +3,957 | +1,212 | **−2,745** | our units 126→109, price 151→123, sheep 7.3→6.4; **YARN_STORE rate is flat (0.37 → 0.33)** |
| CARROT | +3,449 | +1,881 | −1,567 | our units 128→109; PET_CAFE 0.67→0.60, partly confounded |
| EGG | +2,516 | +1,383 | −1,133 | BAKERY 0.43→0.60, BRUNCH 0.63→0.40 |
| STRAWBERRY | +4,319 | +4,994 | **+675** | the tilt buys back 675 of the 8,697 it costs |
| MELON / WHEAT / MILK / FERT | | | +645 / +511 / −247 / +40 | |
| **sum** | | | **−7,075** | (measured d15-29 Δ −7,208, full margin Δ −8,339) |

**The strawberry tilt is a displacement, and a bad one.** It returns +675 of margin and costs
−3,252 tomato, −2,745 wool, −1,567 carrot, −1,133 egg. Within either stratum the residual
correlation points the same way: ρ(margin) with our late strawberry tiles is **−0.52** on
non-smoothie towns and **−0.69** on smoothie towns; with grow_mult3 −0.64 / −0.42; with press3
(sell it, don't hold it) **+0.54 / +0.48**.

## 5. The five answers

1. **Which products and days carry the gap.** d15-29 only (d0-14 is flat unit-for-unit on both
   seats). The single largest line is **strawberry**, and it is a *price* line, not a volume line:
   the clone sells the same 249 units either way at 75 (B wins) or 122 (B loses). In margin terms
   the winning basket is **wool +4,927, tomato +3,773, milk +2,550, carrot +2,415**, against
   strawberry **−3,330**.
2. **Is it board luck or a play difference.** **Mostly board luck, with a play response riding on
   it.** One exogenous covariate clears |ρ| 0.3 — the town's 5-of-8 shop draw, specifically
   SMOOTHIE_SHOP: −8,339 coins and 80.0 % → 41.7 % win rate, holding inside both families
   (t +6.4 / +3.6 on the non-smoothie strata, ≈0 on the smoothie strata). Weeds, the seed word and
   the opponent's rating predict nothing. That part is a lottery no theta removes. What *is* play is
   B's response to the draw: it answers the high strawberry price by tilting the late board into
   strawberry and away from tomato / wool / carrot.
3. **Do the trained knobs reach it.** Yes, mechanically: `press` and `grow_mult` per product,
   `animal_want`, `hire_bias` and `crew_target` are exactly the quantities that differ, they differ
   at t 5.1 / 4.2 / 2.6, and B already swings them 2-4× across boards. The fault is direction, not
   reach.
4. **Coins at stake.** The reachable part of the 13.5k is **not** the 8.3k shop term — it is the
   mis-allocation inside it. The cleanest unconfounded line is **wool: −2,745 per smoothie board**
   (YARN_STORE presence is flat across the two strata, so the wool collapse is B's own displacement,
   not a missing sink). Adding the part of carrot and egg not explained by sink displacement puts
   the reachable pool at roughly **−1,900 to −3,900 coins per smoothie board**, i.e. **−950 to
   −1,950 pooled** over the 50 % of boards that draw one.
5. **What half of it is worth.** Capturing half: **+475 to +975 pooled band coins**, centred near
   **+700**. The §119 promotion bar is ≈ **+600 pooled band coins**. So this is, on the arithmetic,
   a promotion-sized prize — and the only one this decomposition finds that is not the shop lottery.

### What it says about the next arm
* Aim at the **late strawberry weight conditioned on the strawberry sink**: `g5/gb5` (grow_mult)
  and `press` on items 3 (strawberry), 2 (tomato) and 7 (wool), with `gb5`/`b1` carrying the sheep.
* **`press` is pinned in flow213.** `press3` has the largest win/loss separation of any decoded knob
  in the window (Δ +16.6, t +5.13) and the strongest within-stratum margin correlation (+0.54 /
  +0.48). Pinning `press` freezes the one family this study points at. Worth re-checking before
  flow213 is promoted over an arm that leaves it free.
* The town's shop vector is **observable to the policy** (`st.shops` is in `PolicyObs`), so a
  "strawberry sink present → hold the tomato/wool board" response is expressible in the existing
  gene set; it does not need a new interface.

## Caveats
* **Sim, not engine.** The `S/simscreen` action-seat sim is 99.5 % of the engine (`sim-equals-engine`
  note) and every board's d29 money here reproduces the two anatomy csvs to the coin, but the
  per-product ledger has never been checked against an engine replay.
* **One game per board-seat.** 60 boards × 2 seats = 120 games, one seed each. The seats are not
  independent (on many NEXT30 boards the two seats return the identical game), so the effective n
  for the shop covariate is nearer 60 than 120 and the t-statistics above are optimistic. The
  SMOOTHIE split survives at n=24-36 inside each family, which is the check that matters.
* **This is a cross-section, so it is selection, not a lever.** Every number here compares boards B
  already won against boards B already lost, or towns against towns. Per the standing
  `counterfactuals-overstate` rule, a replay regression never justifies a lever: the +700 figure is
  a *ceiling on where to look*, not a predicted gain. It has to be paid for by a paired arm.
* The tomato, carrot and egg terms are **confounded** by sink displacement (a town with SMOOTHIE has
  5−1 slots for the rest). Wool is the one term with a flat sink rate across strata.
* `nhands` reads 0 in the window because the snapshot is taken after end-of-day, when hands are
  released; `crew_target` is the hiring quantity to read instead.
