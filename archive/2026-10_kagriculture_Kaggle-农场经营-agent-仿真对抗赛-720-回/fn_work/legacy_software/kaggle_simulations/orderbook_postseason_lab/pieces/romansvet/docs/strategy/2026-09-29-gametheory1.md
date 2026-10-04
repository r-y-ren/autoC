# GAMETHEORY1 (2026-09-29 06:56-09:26Z): a game-theory census of the engine, and the one untried cell it leaves

Stream dir `S/gametheory1/`. Worktree `/mnt/e/_work/kagg3_wt_gametheory1` (branch `gametheory1_0929` from master 8d670dad:
cherry-pick of HERD1's `HERD_PLAN` 269e8dee + new `HERD_MATCH` 07859bfe). No upload, no package, no GPU, no trainer.
Local: one process at nice 19 / ionice idle. Remote (8 cores) sat at load 13-17 from other streams until 08:10Z, so the 8-cell screen ran
locally; the M1 extension (60 more g0capsfix games, live27, 60 more flood games) ran on the remote with 2 workers once its load fell to 8.9.

USER ORDER: "review all game theory mechanisms and try to simulate applying it to our agent ... take different angle ... try thing no one tried".

## Verdict
- **CANDIDATE: NONE. PROMISING: NONE.** The census leaves exactly one untried cell family that does not belong to a running stream (a late,
  d10+ herd funded by idle cash, as a capacity best response in the supply-saturated milk book); it was built (`HERD_MATCH`, new) and run next to
  the absolute late floor (`HERD_PLAN` d10, HERD1's switch) as a named 8-cell screen, and its best cell does not hold at 80 games.
- **Bar check for M1:** own >= control - 1k on g0capsfix (-796) and on flood (-205): pass; margin t >= 2: FAIL (+0.23 on 80 g0capsfix games,
  -1.41 on live27); rival gain on the faithful tapes <= +3k: pass (-1.6k). -> NONE; not PROMISING (no read positive at t >= 2).
- **Best cell M1 = `HERD_MATCH=P|C:10:1`** (cow stock = the rival's visible cows + 1, d10-17):
  - vs g0capsfix, boards_m40 80 games: ours 114,372 / rival 89,327 / margin +25,046 vs control 115,169 / 90,217 / +24,952:
    **own -796 (t -2.08), rival -890 (t -2.48), margin +94 (t +0.23), flips +0/-0 (W 75 -> 75)**; windows ours d0-9 / d10-14 / d15-29
    +0 / -202 / -594, rival +0 / +201 / -1,091.
  - vs g0capsfix on the 27 live27 original seats: own -2,318 (t -3.09), rival -1,104 (t -1.65), margin -1,214 (t -1.41), flips 0/0.
  - vs flood (dours read): 80 games (boards_m40 0-39 x 2 seats): own -205 (t -0.80), rival +211 (t +1.08), margin -416 (t -1.01), flips +0/-0.
  - faithful live27 tapes (open loop: the real programme's recorded units re-priced, so it cannot react; 18 fired seats, all JC1-faithful both):
    own -1,682 (t -3.72), rival -1,558 (t -2.12), margin -124 (t -0.18), flips +0/-1 (W 4 -> 3).
  - Mechanism: the milk denial is real (rival milk coins -1.2k to -1.7k on every g0capsfix read, t -2.5 on its purse at 80 games), but after d10
    PFS is tile- and labour-bound, so the extra cows come out of strawberry (-0.5k), eggs (-0.3k) and wool (live27 -0.8k), and our own extra
    milk units cannibalize our own milk price (live27: +12 u, -786 coins). The crop books those tiles fed are denial books too (rival strawberry
    +0.3k). Net: a wash on margin, a loss on own coins.
- **The screen** (20 games per cell, every cell named 07:37Z): all 8 cells |dmargin| <= 1.6k with |t| <= 1.4, flips 0 except A7_gcf +2/-0.
  Absolute floors: A7 (+1 cow) barely binds (milk +6 u); A8 (+2) milk +11..+18 u; named extra A10 (+4 cows, g0capsfix only): milk +26 u and
  rival milk -2.1k, but our strawberry -1.5k and wool -12 u hand the rival +0.8k strawberry / +1.8k wool: own -309, margin -82 (t -0.05).
- **Census findings** (section 1): (1) one seat reaches the other only through the 9 books - no finite shared stock, seat order inert, the shop
  draw keyed to both seats' dusk empty tiles but blind (scrubbed 31-bit seed), every round trip exactly 0 on the rival's fills; (2) in the stock
  books (melon, fertilizer, wool without the yarn store) order is a pure zero-sum transfer: pre-empting the programme's d10 melon wave (its first
  melon SELL at d10 h8 median, h5 earliest, over 42 live games) is worth +0.4k (12 melons) .. +4.5k (78) each way, but only on a d0 plate;
  (3) our late volume is the only denial instrument (our milk -23..-50 u = rival milk +4.9..+10.0k across the banked cells), and its supply is
  fixed by d0-9 cash and by the post-d10 tile / labour limit - this stream shows the second limit is binding too.


## 1. Census (part 1): every channel through which one seat reaches the other's payoff

Full table with engine facts: `S/gametheory1/census.md` (copied below). Data: 42 live PFS-unfired games vs programme rivals >= 2,450
(`S/winanatomy1/games.json`, replays `S/livewatch23/gz`), scanned by `rpscan.py` / `rpscan2.py` -> `res/rptab.txt`, `res/rptab2.txt`;
the exact melon order value `melonorder.py` -> `res/melonorder.md`; the per-product two-purse deltas of banked cells via `gt_an.py --prod`.


### A. Engine facts (line refs = the vendored kaggriculture.py)
- **Payoff** = `farms[i]["money"]` at the step that sets DONE (engine step 718, `interpreter` end). Shed stock, seeds, animals, land, plants are worth 0. Live (42 PFS-unfired games vs programme rivals >= 2,450, `res/rptab.txt`): the programme ends with 152 coins of unsold stock per game, PFS with 0.
- **Step order** (`interpreter`): seat 0 unit actions, seat 1 unit actions (separate farms), then `_process_market` (both seats), then `_town_consume`, then plant decay, then at hour 23 `_end_of_day` (plants, animals, weeds, dusk drop, shop draw).
- **Market** (`_process_market`, `_commit_unit`): up to 10 orders per seat per step (`q[:max_orders]`), processed BY INDEX: index i of both seats completes before index i+1. Inside an index, HIRE / BUY_LAND resolve in player order (per-farm, no shared effect), then a per-unit lockstep: both seats' next units are quoted off the SAME pre-commit inventory, then committed seat 0 first. SELL = +1 inventory (not at price 1), BUY_PRODUCT (WHEAT, FERTILIZER only) = -1 inventory, quoted at inventory-1 so a round trip on an unchanged book nets exactly 0. Seeds and animals: fixed price, unlimited, no book.
- **Demand** (`_town_consume`, after the market every step): each shop instance removes 1 of each of its products every 4 steps (2 for the single-product YARN_STORE / PET_CAFE); the town centre removes 1 of every non-fertilizer product every 24 steps. **MELON has no shop (1 unit/day, town only); FERTILIZER has no demand at all; WOOL only via YARN_STORE.** Everything else has 2-5 shop types.
- **Curves** (`MARKET_PARAMS`): above I0 melon = 250 - 0.01 x^2, wool = 200 - 0.058 x^2 (quadratic), milk 160 - 2.10 x, strawberry 120 - 1.92 x, fertilizer 100 - 0.20 x (linear), tomato / carrot sqrt, egg / wheat log (flat). Below I0 tomato / carrot / egg are "hinge" (calm, then a quadratic shortage spike past T units).
- **Shop draw** (`_end_of_day`): `rng = Random((seed*1_000_003) ^ day)`; the rng first draws one `random()` per EMPTY unlocked tile of seat 0, then of seat 1 (weeds, p = 0.005), then `rng.choice(sorted(SHOPS))`, on days 2, 5, ..., 23 (8 instances, with replacement). Same town for both seats, visible at the dawn of the unlock day. Our dusk empty-tile count changes WHICH shop is drawn, but the 31-bit seed is scrubbed from the observation (`resolve_episode_seed`) -> steering is blind (0 EV).
- **Observation**: `farms` (both seats: money, every tile with crop / age / water / fert / yield, animals with fed / cared / pending bonus / yield, farmer + hand positions, quadrants, hires_today), `market` (inventory + prices), `town`. Private and NOT visible to the other seat: shed, seeds, carried inventories, orders.
- **Finite shared stock: none.** Seeds / animals / water unlimited; land and hires are per farm (hire n of the day costs fib(n)); the buyable wheat / fertilizer books start at I0 = 10,000 units.
- **Shed** 100 per seat; overflow at the dusk drop is discarded. Live: the programme's shed is full at dusk on 2.8 days / game, PFS's on 6.7.

### B. The round-trip identity (derived, `S/gametheory1` notes)
The rival's fill price depends only on the book level at its fill = I0 + cumulative net units sold by BOTH seats - cumulative town drain.
A buy-then-sell (or sell-then-buyback) of ours leaves our net position unchanged, so relative to not trading it moves the rival's fills by exactly 0
(worked on the linear book p = a - s x: buy K, sell K just before the rival's R units, buy K back after them, sell K at the end -> the rival's R units
fill at the same prices as with no trade, and our P&L is -s K^2); our own P&L of a round trip is <= 0 unless the town drain or the rival's own BUYS
fall inside the window. So **"denial dumping of bought units", the "sandwich" and "raising its costs" cannot deny**: the only instruments that move the
rival's prices are (a) our net PRODUCED volume and (b) its timing relative to the rival's fills; a round trip earns only from the town drain or
from the rival's own BUYS falling inside the window (ARB1's relay territory).

### C. Census table: mechanism | lever | tested? | untried cell (switch design) | coins bound (ledgers)

| # | mechanism (channel) | game-theory lever | tested? (doc: number) | untried cell / switch design | coins bound from ledgers |
|---|---|---|---|---|---|
| 1 | melon book: stock commons (1 u/day demand, quadratic above I0) | pre-emption at the d10 wave | V-era MELON_OPEN_ON + MELON_LOT_EARLY_ON (12-tile package, M12 -16.2k); programme era: plates (D10WAVE1 B4/B8, REALLOC1, MELONSHIFT1, COMBO1) sold AFTER the rival (205-235/u vs its 233-251) | **PREEMPT** (plate-conditional): d10-11 h0-7 harvest ripe melon -> DROP -> SELL MELON at index 0 before the programme's first melon sale (live d10 h8 median, h5 earliest; `res/rptab.txt`) | exact curve (`res/melonorder.md`): zero-sum transfer +/-0.36k (12 u) .. +/-4.5k (78 u vs a 52 wave), margin 2x; PFS itself has 0.2 melons in d10-14 -> inert without a plate; the plates cost -10..-17k margin elsewhere (herd) |
| 2 | melon book, late (d15-29) | Cournot quantity: we are the dominant late seller (92 u vs rival 13-27) | PRICEGAP1 mix cells; COMBO1 / MELONSHIFT1 "no melon replant" (running) | covered by COMBO1 | our late melons 176/u closed loop, 142/u live |
| 3 | fertilizer book: zero demand, linear 0.2/u | first mover in a pure stock; sell vs apply | FERT_RESERVE -32.7k, FERTSALE1 FERT_DUMP <= 0, FERTDENIAL, YIELD1 floor -1.6..-8.8k margin (every unit applied = one not sold, rival fert +0.7..+2.5k) | none (PFS already applies every unit worth more than its quote; sells the rest same day) | live: both seats dump ~550 u/game (100 -> 23); first-mover bound 0.2 x (same-day units) ~ 7 coins/day |
| 4 | wool book: stock unless YARN_STORE (12 u/day) | first mover / Cournot | WOOLFIRST1, SHEEPFIRST1, WOOLDENY1 (gift / own loss); STEER1 front | shop-draw bet = RISKWIN1 | c4p8: our wool -8 u = rival wool +4.1k |
| 5 | late flow books saturated (milk / strawberry / tomato / egg / carrot below base) | **Cournot in margin terms (volume = denial)** | early herd floors HERD1 d3-9 (c2 +0.4k ns, c4 -12.0k: displaces d0-9 cash); CONTEST1 (6 cells lose); OPP_SUPPLY (-3.0k); MELONDENY1; Q4 FQ tail (D10WAVE1 C -9.1k; vs big -8.1k) | **LATE HERD** (d10+, idle cash + Q3 tiles, never run): `HERD_PLAN=P\|C:10:n` (HERD1 switch, floors only ever run to d9) and **HERD_MATCH** (new): cow stock floored at the RIVAL's visible cows + delta from d10 | REALLOC1 c2p0: our milk -31 u -> rival milk +6.7k (216/u), our milk coins +0.6k (-21/u); a d10 cow ~ 21 milk d18-29 + 19 fert: rival -4.5k, own -1.0..+0.0k (hypothesis) |
| 6 | queue index within a step | first seller on a shared step | SELL_SLOT_PRIORITY SHIPPED; SLOTLOCK / SLOTMIRROR REJECT; SELLFIRST (0 rows permuted) | none | live: same-step same-product collisions 13.2 fert / 9.5 wheat / 6.5 milk / 5.5 strawberry per game, first index split evenly |
| 7 | hour within the day | sell before the rival's flood hour | LOT4 SHIP, EARLY_SELL ON, LOTDEPTH -1,981, OPP_FRONTRUN (level), SALESIDE1 (our dawn/dusk lots already +5.0k quote level) | none | SELLEARLY1 same-day cut <= +6.4k undepthed |
| 8 | sale day (hold vs sell) | wait for drain / first mover across days | SELLEARLY1 (+5 coins bound; SELL_BY -0.2..-0.6k), SALESIDE1 (every hold gifts, -1.4..-4.2k) | none | +5 |
| 9 | round trips on WHEAT / FERT (bought-unit dumping, sandwich) | denial dumping, front-running | derived identity (B): 0 on the rival's fills; STEER1 wheat0/5/hold/dump rival +2.9..+14.6k; RESALE1 -3..0; WHEATPUMP1 | none (closed by construction) | 0 |
| 10 | the rival's buys (live: 694 wheat + 93 fert / game, spread over d0-29, `res/rptab2.txt`) | sell into its buys (lockstep crossing), relay | OPEN_PUMP SHIPPED (+410, d0 only) | ARB1 (running) | programme relay loses 1.4/u on ~700 u = ~1k/game |
| 11 | raising the rival's input costs (feed wheat, fert) | raise rivals' costs | STEER1 (it is a net seller in both books: every buy lifts its sale prices) | none | rival +2.9..+14.6k |
| 12 | visible farm (money, tiles, herd, hands, quadrants) | commitment / bluff / Stackelberg signalling | never (the live programme's reaction function is unobservable: d0-2 opening fixed; no public programme kernel, STEER1) | untestable faithfully: the BC clone reads our money, m0-m1, hands, hires, quadrants and crop/animal counts (`S/bcbody1/feats.py`), so any bluff reads on the clone's learned correlations, not the programme's; live A/B is forbidden | unknown |
| 13 | our information on the rival (its committed tiles, ripe stock, reconstructed sales) | best response to its visible commitment | OPP_MIX (V-era), OPP_FRONTRUN, SLOTLOCK (opp_ripe), RIVAL_TELL | HERD_MATCH (row 5) reads it | - |
| 14 | shop draw keyed to both seats' dusk empty tiles | steer the town | M35 (seed inference dead), STEER1 (blind) | none (31-bit hidden seed) | 0 EV |
| 15 | weed rng (same stream) | - | - | none | 0 EV |
| 16 | seat order (P0 units first, P0 commits first, P0 weeds first, atomic HIRE/LAND in player order) | first-mover by seat | SEATFLIP1 (same-board P1 - P0 = 0) | none | 0 |
| 17 | finite shared stock (seeds, animals, hands, land, water) | pre-emption | engine: none exists | none | 0 |
| 18 | 10-order cap | cap gaming | per seat; SELLFIRST: 16.9 capped rows/game, no cross effect | none | 0 |
| 19 | end of game = cash only | liquidation race | ENDROUTE / ENDSELL / ENDGAME1 SHIPPED | none | rival end stock 152 coins/game |
| 20 | the rival's shed cap (full at dusk 2.8 d/game) | force its overflow | none (no instrument reaches its hold rule; round trips cannot, B) | none | its end stock 152 coins/game; dusk discards unmeasured |
| 21 | hinge books (tomato / carrot / egg shortage spikes below I0) | war of attrition / hold-out | TOMATO15, CARROTFLAT1-3, ENDGAME_TOMATO, PRICEGAP1 | none | - |
| 22 | risk / P(win) when behind; shop-draw bets | risk-seeking | - | RISKWIN1 (running) | - |
| 23 | d0-9 cash -> herd -> late volume (the constraint every row above hits) | budget allocation | HERD1, REALLOC1 (c3p0 -5.8k / c2p0 -11.5k margin per -1 / -2 h1 cows), LAND1, CREW1 | row 5 moves the herd lever to d10+ where cash is idle | idle cash 5.7k at dawn d10 (closed loop), 15.8k median d10-19 live (ECONCENSUS1) |

**Reading.** The only coupling is the 9 books (+ the blind rng + the unobservable reaction of the rival's policy to our farm). Inside the books every
timing and ordering lever is covered and every round trip is 0 by construction (B), so what is left is WHERE our produced volume lands:
(1) the d10 melon pre-emption (a pure zero-sum transfer, but it needs a d0 plate that the d0-9 cash cannot fund without cutting the herd), and
(2) late capacity in the supply-saturated books funded by the idle d10+ cash (never run: every herd floor so far bought in d0-9).
Part 2 runs (2) as a named grid; (1) is left to the plate streams with its exact bound.


### 1a. Three findings that carry the rest
1. **The only coupling is the 9 market books** (plus a blind shared rng and the rival's unobservable reaction to our visible farm). No finite
   shared stock exists (seeds, animals, water unlimited; land and hires per farm), seat order is inert (SEATFLIP1 0), the order cap is per seat,
   and the shop draw, though keyed to BOTH seats' dusk empty-tile count (`rng.random()` per empty tile of seat 0, then seat 1, then
   `rng.choice(SHOPS)`), is blind because the 31-bit seed is scrubbed. **Round trips cannot deny**: the rival's fill price is a function of the
   book level only (I0 + both seats' cumulative net units - town drain), so buy-then-dump, sandwiches and "raise its input costs" move its fills
   by exactly 0 relative to not trading (and STEER1 measured +2.9..+14.6k FOR the rival on the wheat moves). What moves the rival is our net
   PRODUCED volume and where it lands.
2. **Stock books make order a pure zero-sum transfer.** MELON has no shop (1 unit/day), FERTILIZER no demand, WOOL only the yarn store. On the
   melon curve the programme's d10 wave (live first melon SELL at d10 h8 median, h5 earliest, 42 games) could be pre-empted from d10 h1-h7:
   exact transfer +0.36k (12 of our melons) to +4.5k (78 vs a 52 wave) to us and the same off the rival (margin 2x, `res/melonorder.md`).
   It needs d0-planted melons; PFS has 0.2 in d10-14 and every d0 plate so far sold AFTER the rival (205-235/u vs its 233-251) and paid with
   the herd (rival +10-17k). Handed to the plate streams (COMBO1 / MELONSHIFT1) as a component with its bound.
3. **The late flow books are supply-saturated, so our volume there is the only denial instrument, and its price is set in d0-9 cash.**
   Every banked cell that cut our herd shows the same coefficient: our milk -23 / -31 / -35 / -50 units -> the rival's milk coins +4.9k / +6.7k /
   +7.5k / +10.0k (200-216 per unit) while our own milk coins move -0.9k..+1.0k (own marginal revenue ~0) [D10WAVE1 B4, REALLOC1 c2p0 / c4p8 /
   c2p8]. Every herd floor ever run bought in d0-9 (HERD1 d3-9: c2 +0.4k ns, c4 -12.0k), where it displaces other d0-9 spend. **Nobody has run a
   late (d10+) herd funded by the idle d10 cash** (5.7k at dawn d10 closed loop; 15.8k median d10-19 live, ECONCENSUS1) on the fresh Q3 tiles.

## 2. Part 2: the untried cells

### 2a. Switches (worktree `gametheory1_0929`)
- `HERD_PLAN="P|C:<day>:<n>"` (HERD1, cherry-picked unchanged): cow stock floored at n from `day` through `HERD_PLAN_LAST` (17), the floor passes
  the spot-value gate, "P" serves the lane first in `budget.grant`; purse, structures and placement still bind.
- `HERD_MATCH="P|C:<day>:<delta>"` (new, default ""): the same floor, but at the OTHER seat's standing cows (`view.opp_commit`, parsed from
  `obs.farms` every turn) + delta, capped at 12, through `HERD_MATCH_LAST` (17): a capacity best response in the milk book, where the rival
  holding the larger herd is exactly where our extra unit denies more than it cannibalizes. Both "" = every call site Python-false.
- OFF identity: worktree tree + vrp20 OFF string == `S/judgerival1/res/g0capsfix/pfs.csv` on boards_m40 0-2 x 2 seats, **6/6 exact** on every
  money column (`res/gt_off_local.csv`, `ident_cmp.py`).

### 2b. Grid (named 07:37Z before any run)
Cells A7 / A8 = `HERD_PLAN=P|C:10:7` / `P|C:10:8` (+1 / +2 cows over PFS's ~6.1 at d9), M0 / M1 = `HERD_MATCH=P|C:10:0` / `P|C:10:1`,
each vs g0capsfix (margin / flips; control `S/judgerival1/res/g0capsfix/pfs.csv`) and vs flood (dours; control
`S/judgerival2/res/jr2_pfs_fl.csv`), screen = boards_m40 0-9 x 2 seats (20 games), harness `S/judgerival1/rcr.py` (the judge's), extension
rule named with the grid: the best g0capsfix dmargin cell with own >= control - 1k goes to the 80-game g0capsfix and flood reads, live27 vs
g0capsfix and the faithful live27 tapes.

### 2c. Two-purse tables (`S/gametheory1/res/grid.md`, `final_tables.sh` -> `gt_an.py`)
Columns: W ctl->cell, flips +up/-down, means, paired deltas with t, cash windows d0-9 / d10-14 / d15-29 (sal checkpoints 240 / 360 / end;
where a control lacks the d15 checkpoint the row says so and the windows are d0-9 / d10-17 / d18-29), per-product unit / coin deltas for both seats.

### Screen vs g0capsfix, boards_m40 0-9 x 2 seats (20 games); control S/d10wave1/res/d10_ctl.csv (== S/judgerival1/res/g0capsfix/pfs.csv, with the d15 checkpoint)
control /mnt/e/_work/kaggriculture3/S/d10wave1/res/d10_ctl.csv: n 80
| cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | ours d0-9 / d10-14 / d15-29 (cell - ctl) | rival d0-9 / d10-14 / d15-29 (cell - ctl) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A7_gcf (windows d0-9/d10-17/d18-29) | 20 | 18->20 | +2/-0 | 109,604 | 84,465 | +25,140 | +41 (+0.05) | -68 (-0.09) | +109 (+0.10) | +0 / -128 / +170 | +0 / +368 / -436 |
|   ours per product (cell - ctl, whole game): WHEAT +8u +644, CARRO -5u -162, TOMAT -2u -774, STRAW -2u -395, MELON -0u -26, EGG -5u -258, MILK +6u +16, WOOL -3u +664, FERTI +4u +152 |
|   rival per product (cell - ctl, whole game): WHEAT -25u -752, CARRO -8u -331, TOMAT +4u +638, STRAW +3u +61, MELON +0u +59, EGG +1u +94, MILK +0u -565, WOOL -2u +668, FERTI +5u +43 |
| A8_gcf | 20 | 18->18 | +0/-0 | 109,453 | 84,201 | +25,252 | -110 (-0.20) | -332 (-0.50) | +222 (+0.31) | +0 / -64 / -46 | +0 / -313 / -19 |
|   ours per product (cell - ctl, whole game): WHEAT -8u +43, CARRO -5u -156, TOMAT -4u -548, STRAW -4u -1,170, MELON -0u +51, EGG +5u +235, MILK +11u +76, WOOL +1u +1,175, FERTI +19u +542 |
|   rival per product (cell - ctl, whole game): WHEAT -17u -445, CARRO -8u -345, TOMAT +1u +218, STRAW +6u +549, MELON +0u +91, EGG -0u -3, MILK +2u -1,228, WOOL -5u +790, FERTI -3u -348 |
| M0_gcf | 20 | 18->18 | +0/-0 | 108,693 | 84,778 | +23,915 | -870 (-1.82) | +245 (+0.46) | -1,115 (-1.33) | +0 / -78 / -792 | +0 / +71 / +174 |
|   ours per product (cell - ctl, whole game): WHEAT -8u -199, CARRO -0u +25, TOMAT -0u -644, STRAW -2u -736, MELON +0u -18, EGG +6u +274, MILK +7u +250, WOOL -4u -7, FERTI +10u +341 |
|   rival per product (cell - ctl, whole game): WHEAT -2u -35, CARRO -3u -123, TOMAT +4u +679, STRAW +7u +809, MELON +0u +96, EGG -4u -219, MILK +0u -1,133, WOOL -1u +139, FERTI -5u -298 |
| M1_gcf | 20 | 18->18 | +0/-0 | 110,156 | 83,747 | +26,409 | +593 (+0.68) | -785 (-0.89) | +1,378 (+1.22) | +0 / -207 / +800 | +0 / +719 / -1,504 |
|   ours per product (cell - ctl, whole game): WHEAT -5u +85, CARRO -5u -167, TOMAT -2u -306, STRAW -3u -658, MELON +0u +60, EGG -3u -117, MILK +14u +911, WOOL -3u +512, FERTI +15u +444 |
|   rival per product (cell - ctl, whole game): WHEAT -12u -408, CARRO -4u -187, TOMAT +2u +463, STRAW +4u +467, MELON +1u +177, EGG -1u -10, MILK -5u -1,596, WOOL -4u +242, FERTI -9u -384 |
| A10_gcf | 20 | 18->20 | +2/-0 | 109,254 | 84,306 | +24,948 | -309 (-0.31) | -227 (-0.22) | -82 (-0.05) | +0 / -286 / -23 | +0 / -290 / +63 |
|   ours per product (cell - ctl, whole game): WHEAT -6u +311, CARRO -5u -151, TOMAT -5u -259, STRAW -7u -1,504, MELON -2u +38, EGG -10u -410, MILK +26u +44, WOOL -12u +1,328, FERTI +26u +789 |
|   rival per product (cell - ctl, whole game): WHEAT -17u -283, CARRO -7u -295, TOMAT +2u +444, STRAW +8u +827, MELON -0u -80, EGG +6u +270, MILK -2u -2,109, WOOL -2u +1,754, FERTI +1u -481 |

### Screen vs flood (dours read), boards_m40 0-9 x 2 seats (20 games); control res/ctl/ms_ctl_fl.csv (MELONSHIFT1, == S/judgerival2/res/jr2_pfs_fl.csv 20/20)
control res/ctl/ms_ctl_fl.csv: n 20
| cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | ours d0-9 / d10-14 / d15-29 (cell - ctl) | rival d0-9 / d10-14 / d15-29 (cell - ctl) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A7_fl | 20 | 20->20 | +0/-0 | 119,396 | 74,549 | +44,847 | -33 (-0.04) | -544 (-0.64) | +511 (+0.43) | +0 / -73 / +39 | +0 / -275 / -269 |
|   ours per product (cell - ctl, whole game): WHEAT -3u -42, CARRO +0u +56, TOMAT -2u -203, STRAW -3u -631, MELON -2u -225, EGG -2u -117, MILK +13u +73, WOOL -3u +740, FERTI +8u +313 |
|   rival per product (cell - ctl, whole game): WHEAT +11u +548, CARRO -6u -333, TOMAT +3u +157, STRAW +3u -8, MELON -0u -82, EGG -1u -77, MILK +0u -471, WOOL +4u +116, FERTI +0u -41 |
| A8_fl | 20 | 20->20 | +0/-0 | 119,298 | 76,567 | +42,731 | -131 (-0.18) | +1,474 (+1.44) | -1,605 (-1.42) | +0 / -211 / +79 | +0 / +116 / +1,358 |
|   ours per product (cell - ctl, whole game): WHEAT -11u -281, CARRO +2u +138, TOMAT -3u -82, STRAW +1u -152, MELON +0u -74, EGG -7u -342, MILK +18u +206, WOOL -9u +716, FERTI +8u +231 |
|   rival per product (cell - ctl, whole game): WHEAT +4u +349, CARRO -5u -311, TOMAT +0u -8, STRAW +5u +767, MELON +1u +170, EGG +3u +156, MILK +4u -918, WOOL +6u +1,081, FERTI +7u +189 |
| M0_fl | 20 | 20->20 | +0/-0 | 118,529 | 75,104 | +43,424 | -901 (-1.32) | +11 (+0.03) | -912 (-1.34) | +0 / +13 / -914 | +0 / -132 / +143 |
|   ours per product (cell - ctl, whole game): WHEAT -2u +36, CARRO +3u +236, TOMAT -0u -33, STRAW +1u -424, MELON -0u -90, EGG -3u -142, MILK +4u +222, WOOL -4u -546, FERTI +1u +0 |
|   rival per product (cell - ctl, whole game): WHEAT +8u +415, CARRO -4u -212, TOMAT +2u +155, STRAW +3u -92, MELON -0u -20, EGG +1u +37, MILK +4u -288, WOOL +6u +260, FERTI +3u +75 |
| M1_fl | 20 | 20->20 | +0/-0 | 119,246 | 74,904 | +44,342 | -183 (-0.36) | -189 (-0.76) | +6 (+0.01) | +0 / -12 / -171 | +0 / +377 / -566 |
|   ours per product (cell - ctl, whole game): WHEAT -14u -489, CARRO +6u +387, TOMAT -1u -45, STRAW +1u -67, MELON -0u -35, EGG -5u -252, MILK +9u +271, WOOL -0u +261, FERTI +0u +5 |
|   rival per product (cell - ctl, whole game): WHEAT +12u +576, CARRO -7u -373, TOMAT -4u -284, STRAW +1u -137, MELON -0u -18, EGG -2u -81, MILK +6u -385, WOOL +1u -12, FERTI +5u +233 |

### M1 vs g0capsfix, all 80 boards_m40 games (screen 20 + remote extension 60); control d10_ctl.csv
control /mnt/e/_work/kaggriculture3/S/d10wave1/res/d10_ctl.csv: n 80
| cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | ours d0-9 / d10-14 / d15-29 (cell - ctl) | rival d0-9 / d10-14 / d15-29 (cell - ctl) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1_gcf80 | 80 | 75->75 | +0/-0 | 114,372 | 89,327 | +25,046 | -796 (-2.08) | -890 (-2.48) | +94 (+0.23) | +0 / -202 / -594 | +0 / +201 / -1,091 |
|   ours per product (cell - ctl, whole game): WHEAT -2u +76, CARRO -3u -78, TOMAT -2u -159, STRAW -2u -542, MELON +0u +77, EGG -6u -260, MILK +12u +41, WOOL -5u +72, FERTI +11u +245 |
|   rival per product (cell - ctl, whole game): WHEAT -6u -184, CARRO -1u -66, TOMAT -0u +61, STRAW +3u +305, MELON -0u +2, EGG +2u +113, MILK -2u -1,228, WOOL -4u +221, FERTI +1u -167 |

### M1 vs flood, boards_m40 (screen 20 + remote extension, n in the row); control S/judgerival2/res/jr2_pfs_fl.csv (windows d0-9/d10-17/d18-29: that control has no d15 checkpoint)
control /mnt/e/_work/kaggriculture3/S/judgerival2/res/jr2_pfs_fl.csv: n 80
| cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | ours d0-9 / d10-14 / d15-29 (cell - ctl) | rival d0-9 / d10-14 / d15-29 (cell - ctl) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1_fl80 (windows d0-9/d10-17/d18-29) | 80 | 80->80 | +0/-0 | 123,925 | 77,262 | +46,663 | -205 (-0.80) | +211 (+1.08) | -416 (-1.01) | +0 / -174 / -31 | +0 / +273 / -61 |
|   ours per product (cell - ctl, whole game): WHEAT -4u -141, CARRO +2u +96, TOMAT -0u -17, STRAW +0u +26, MELON -0u -68, EGG -3u -139, MILK +5u +208, WOOL -1u -13, FERTI +1u +50 |
|   rival per product (cell - ctl, whole game): WHEAT +7u +325, CARRO -1u -49, TOMAT -0u -28, STRAW +0u +101, MELON +0u +57, EGG +0u +7, MILK +1u -225, WOOL +0u +4, FERTI +1u +41 |

### M1 vs g0capsfix on the 27 live27 original seats; control S/judgerival2/res/g0cf_l27.csv
control /mnt/e/_work/kaggriculture3/S/judgerival2/res/g0cf_l27.csv: n 27
| cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | ours d0-9 / d10-14 / d15-29 (cell - ctl) | rival d0-9 / d10-14 / d15-29 (cell - ctl) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1_l27 (windows d0-9/d10-17/d18-29) | 27 | 27->27 | +0/-0 | 109,917 | 83,189 | +26,728 | -2,318 (-3.09) | -1,104 (-1.65) | -1,214 (-1.41) | +0 / -795 / -1,523 | +0 / +115 / -1,219 |
|   ours per product (cell - ctl, whole game): WHEAT -0u +105, CARRO -0u +28, TOMAT -0u -25, STRAW -2u -323, MELON -2u -194, EGG -3u -120, MILK +12u -786, WOOL -8u -844, FERTI +8u +247 |
|   rival per product (cell - ctl, whole game): WHEAT -7u -200, CARRO -3u -111, TOMAT +1u +93, STRAW +0u +86, MELON +0u +72, EGG +1u +27, MILK -0u -1,706, WOOL +2u +640, FERTI -0u -207 |

### M1 faithful live27 tapes (open loop, the real programme's recorded actions; MELONTRIAL1 tbl_l27.py rule)
games 18: fired (k2 sw) 18, unfired 0; status DONE 18, bad steps 0, 720 steps 18, turns > 1 s 5, max step ms 1517
unfired exact to live: 0/0 (h1 [])
fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; SELL MELON d10-14 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6]
| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 3 | +0/-1 | -1,682 (-3.72) | -1,558 (-2.12) | -124 (-0.18) |
| fired | 18 | 4 -> 3 | +0/-1 | -1,682 (-3.72) | -1,558 (-2.12) | -124 (-0.18) |
| fired, JC1-faithful both | 18 | 4 -> 3 | +0/-1 | -1,682 (-3.72) | -1,558 (-2.12) | -124 (-0.18) |

per fired seat (ours / theirs; * = JC1 faithful both):
  ai_114639739                 h1   564 live  84,030/100,627 -> pkg  84,070/101,860 *  mel_d1 0 sell_melon d10-14 0
  ai_114654661                 h1   564 live  88,317/108,959 -> pkg  88,920/108,654 *  mel_d1 0 sell_melon d10-14 0
  c0nrad_114645657             h1   190 live  97,866/115,301 -> pkg  96,115/111,872 *  mel_d1 0 sell_melon d10-14 0
  capitaalgain_114676374       h1     1 live 118,797/124,718 -> pkg 112,934/115,146 *  mel_d1 0 sell_melon d10-14 6
  chungkuangwen_114726910      h1   661 live  98,616/ 94,772 -> pkg  95,687/ 94,314 *  mel_d1 0 sell_melon d10-14 0
  dipamchakrabor_114633798     h1  2046 live 132,215/151,447 -> pkg 129,680/142,803 *  mel_d1 0 sell_melon d10-14 0
  gradientgrazin_114672177     h1   938 live 118,605/108,929 -> pkg 118,822/105,940 *  mel_d1 0 sell_melon d10-14 0
  istinetz_114667726           h1     1 live 105,925/121,076 -> pkg 105,925/121,076 *  mel_d1 0 sell_melon d10-14 0
  istinetz_114684168           h1     1 live  69,666/ 72,437 -> pkg  69,666/ 72,437 *  mel_d1 0 sell_melon d10-14 0
  istinetz_114686994           h1     1 live  78,856/ 94,812 -> pkg  77,169/ 92,098 *  mel_d1 0 sell_melon d10-14 0
  istinetz_114701777           h1     1 live  97,847/108,099 -> pkg  97,847/108,099 *  mel_d1 0 sell_melon d10-14 0
  madmax0404_114676576         h1   938 live 100,678/111,551 -> pkg 100,678/111,551 *  mel_d1 0 sell_melon d10-14 0
  monsaraida_114682642         h1   938 live  95,349/105,043 -> pkg  95,349/105,043 *  mel_d1 0 sell_melon d10-14 0
  shunkikyoya_114664852        h1    73 live 103,786/117,293 -> pkg 100,054/116,714 *  mel_d1 0 sell_melon d10-14 0
  sidazuo_114695876            h1    19 live  80,602/ 80,741 -> pkg  77,716/ 80,032 *  mel_d1 0 sell_melon d10-14 0
  thisray_114655920            h1   938 live  84,145/ 93,090 -> pkg  80,426/ 93,824 *  mel_d1 0 sell_melon d10-14 0
  thisray_114689938            h1   938 live  98,320/ 94,376 -> pkg  93,970/ 96,364 *  mel_d1 0 sell_melon d10-14 0
  vvs_114713033                h1   938 live 102,538/ 96,329 -> pkg 100,855/ 93,724 *  mel_d1 0 sell_melon d10-14 0


### 2d. Reading
- Every herd cell moves the rival's MILK coins down (-0.3k .. -1.7k): the late milk units deny, as the census coefficient says. None of them
  moves the margin, because each extra cow after d10 takes a crop tile and hands from strawberry / eggs / wool (the board is full from d14,
  WHEAT1: 0.2-1.9 empty tiles d14-24) and our own extra milk lowers our own milk price. The capacity best response exists only with capacity
  that is not already used: Q4 (-8.1..-9.1k, D10WAVE1 C / JUDGERIVAL3) or d0-9 cash (HERD1 / REALLOC1), both measured losses.
- How often the floors bind (games whose final purses differ from the control): A7 14/20, A8 14/20, M0 9/20, M1 16/20 and 48/80 vs g0capsfix;
  A7 12/20, A8 16/20, M0 8/20, M1 8/20 vs flood. HERD_MATCH binds only where the clone's visible herd exceeds ours AND a pasture tile is free.
- The tape read is open loop: the programme's recorded units are fixed and only re-priced, so a lever that changes the rival's prices is read
  there with the rival unable to react (it cannot sell more or less into our extra milk), which under-reads any rival response live.

### 2e. Not done / next
- A10 (`HERD_PLAN=P|C:10:10`, +4 cows) named 07:51Z: run vs g0capsfix only (after the tape freed the local slot); A10_fl not run.
- **Next cell: PREEMPT** on whichever d0-plate body COMBO1 / MELONSHIFT1 converge on: on d10-11 h0-7 harvest the ripe plate melons, DROP at the
  shed and SELL MELON at queue index 0 before the programme's first melon SELL (d10 h8 median); exact bound +0.7k (24 melons) .. +3.7k (78)
  to us and the same off the rival (`res/melonorder.md`), the only zero-sum transfer in the census no stream has measured in the programme era.

### 2f. Rule log
- 07:49Z one local `diff` used `<(...)` process substitution (reads /dev/fd) to compare rcrw2.py with rcr.py; read-only, nothing written;
  not repeated. No /dev redirect otherwise; local one worker at nice 19 / ionice idle; remote 2 workers launched only at load 8.9 (< 12).

