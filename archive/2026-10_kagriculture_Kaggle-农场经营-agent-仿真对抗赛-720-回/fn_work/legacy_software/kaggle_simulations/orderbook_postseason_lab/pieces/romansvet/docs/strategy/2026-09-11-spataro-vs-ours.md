# SpaTaro (LB #1, ~3107) vs our live agent — replay ledger, 2026-09-11

Measurement only (no levers proposed). Numbers are reconstructed from Kaggle replay
json with the profiler's lockstep market model (`scripts/replay_profile.py`
`_simulate_market`, recon error 0-500 coins per 720-step game) plus per-day tile /
hand / cash diffs (scratchpad `ledger.py`, listed at the end). Day = (t-1)//24,
hour = (t-1)%24. Hands are re-hired every morning in this engine, so "hands on
day d" = the max crew seen during day d.

Games: SpaTaro ×2 (seat 0 vs Otter Vibe, seat 1 vs ymg_aq; opponent ratings not
in the json). Ours ×4 = wins 107744147 (vs Fuat Çakıcı), 107743508 (Satoshi
Nguyen), 107723697 (Takamichi Toda) and loss 107738911 (Joyal), all 2026-09-11.
The other three of ours on disk (107737990 L, 107735016 W, 107729041 W) were
profiled too and agree with the four (their rows are in the scratchpad json).

## (a) How SpaTaro's strategy differs from ours

SpaTaro plays a front-loaded, all-in-labour farm: six hands from hour 1 of day 0
(4 at h0 for 7 coins, 2 more at h1 for 13) and six every day through day 5, with
the purse run to 0-100 coins every evening for the first ten days; it plants 10-11
melon tiles in hours 2-19 of day 0 and dumps 36 melons at ~253 on day 10, buys 2
cows + 2 sheep at hour 0 and adds one cow a day until it has 8 cows / 8-14 sheep by
day 10, and feeds the herd with 15-39 bought wheat units every morning (452-476
units, 16-18k coins over the game) so that fertilizer (217-231 units, 11-12k) and
milk/wool come on line by day 2-6. Its revenue is six products (wheat, strawberry,
melon, milk, wool, fertilizer) sold in 232-242 separate sell turns spread over all
24 hours (27-34 % of units in hour 0), and it harvests everything by day 29 (1
tile standing). We open with 4 hands (1 on d1, 3 on d2, 5 on d3-7), keep 165-2,076
coins idle overnight in days 0-9, plant our melons on days 9-12 and dump them on
days 22-25 at 112-209, buy 4 cows + 1 sheep + 1 goose at once on day 0 and then
add animals only on days 5-10, diversify into eggs/tomato/carrot after shops
appear, and sell in 49-56 turns, all at hours 1 and 18. The result: SpaTaro has
~3x our cash at day 10 (9.6k vs 3.0k) and 1.5x at day 20 (71k vs 48k), yet
finishes at 101-104k against our 94-114k — its edge is entirely in days 0-20 and
we out-earn it in days 21-29 (29-34k vs 42-70k).

## (b) Key numbers (median across games; SpaTaro n=2 shown as both values)

| metric | SpaTaro | ours (3W+1L) |
|---|---|---|
| hands day 0 / day 5 / day 10 | 6 / 6 / 10-11 | 4 / 5 / 9-10 |
| first day with >=6 / >=10 / >=12 hands | d0 / d10 / d18 | d7-8 / d10-11 / d12-13 |
| hand-days worked d0-d9 | 70 / 68 | 46 / 46 / 45 / 46 |
| cash at first hire of the day, d1-d9 | 8-98 coins (d8h02: 1,212) | 135-2,076 coins |
| end-of-day cash d0..d9 (min-max) | 0-98 (d4 sp2: 161) | 135-5,728 |
| tiles planted cumulative by d10 / standing at d10 | 79,56 / 62,50 | 73 / 46.5 |
| tiles planted cumulative by d20 / standing at d20 | 133 / 51 | 133.5 / 53 |
| tiles planted whole game / standing at d29 | 230,209 / 1,1 | 188 / 8.5 (0-19) |
| crop mix standing d10 | 39 straw / 22 wheat / 1 melon ; 27/20/3 | 16-28 straw / 17-21 wheat / 1-3 melon |
| melon tiles planted (day planted) | 10-11 (d0-d1, 1 on d5) | 14-17 (d9-d13) |
| melon dump day / units / avg price | d10 / 36 / 254 & 252 | d22 (d25) / 18-24 / 188-209 (112) |
| melon units sold total / revenue | 60,66 / 13.9k,15.9k | 84-102 / 13.9-15.0k |
| wheat tiles planted / units sold / wheat revenue | 166,155 / 727,714 / 30.6k,24.3k | 73-131 / 215-333 / 7.3-11.1k |
| wheat units BOUGHT (spend) | 452,476 (18.3k,16.0k) | 106-190 (3.5-7.2k; 53 of it = d0 pump) |
| cows / sheep / geese bought | 8,6 / 8,14 / 0 | 5-10 / 4-17 / 1-5 |
| fertilizer units sold | 217, 231 | 150-324 |
| eggs / tomato / carrot units sold | 0 / 0 / 30,55 | 46-158 / 0-142 / 63-306 |
| sell turns per game / units sold at hour 0 | 242,232 / 27 %,34 % | 55.5 (49-56) / 0 % (h1 60 %, h18 39 %) |
| land: quad 2 (day, cash before) / quad 3 | d6 1.3-1.4k / d8-9 2.1-2.6k | d5 1.8-1.9k / d10 2.7-6.6k |
| cash end of d10 | 10,344 / 8,811 | 3,041 (2,085-4,574) |
| cash end of d20 | 72,223 / 70,043 | 48,290 (37,902-57,298) |
| earned d21-d29 | 28.8k / 33.7k | 60.6k, 47.6k, 69.9k, 41.6k |
| final coins / margin | 100,988 +5.2k ; 103,697 +7.4k | 101,704 (94.3-113.8k) / +16.3k,+8.5k,+22.5k,-1.5k |

## (c) Concrete differences, with the numbers

1. **Day-0 crew and daily re-hire.** SpaTaro: `[HIRE]x4` at d0h0 (cash 3000→ pays 7),
   `[HIRE]x2` at d0h1 (pays 13), then 6/6/6/6/6/6 hands on d0-d5, 9 on d6, 9-10 on
   d8-d10; it hires 4 at h0 and 2 more at h1 every day (two rows). Ours: 4 at d0h0,
   then 1 (d1), 3 (d2), 5 (d3-d7), 7 (d8), 6 (d9), 10 (d10), one HIRE row at h0
   only. Hand-days d0-d9: 68-70 vs 45-46. Favours SpaTaro.
2. **Zero idle cash for ten days.** SpaTaro's end-of-day purse d0-d9 is 48, 28, 18,
   10, 71, 11, 98, 93, 8, 22 (game 1) and 78, 6, 78, 6, 161, 74, 1, 8, 19, 167
   (game 2); every coin is spent on seeds, animals, hands and bought wheat the same
   day. Ours d0-d9: 165, 135, 633, 691, 1,484, 826, 711, 2,076, 1,433, 5,728
   (game 147; the other three are alike). Favours SpaTaro (working capital), though
   it also means SpaTaro cannot react to anything until the d10 melon cash arrives.
3. **Melon pot race, day 0 -> day 10.** SpaTaro buys 7 melon seeds at d0h0 and 7 more
   at d0h11 with the last 161 coins, plants 9-10 melon tiles on d0 (hours 2-19), 1-2
   on d1, and sells 36 units at 254/252 on d10 (h0-h23, 12 sell turns that day) — d10
   cash jumps from 22 to 10,344. We plant 2-3 melon tiles on d9-d10 and 11-14 more on
   d11-d13, and sell 18-24 units per day on d22-d25 at 188-209 (112 in game 697 after
   the opponent dumped first). Same melon revenue (14-16k) but 12 days later.
   Favours SpaTaro (d10 cash 3x, more hands affordable d10-d13).
4. **Herd on bought wheat.** SpaTaro buys wheat every day: 22, 13, 23, 7, 5, 12, 5,
   7, 19, 21 units on d0-d9 and 8-39/day after, at hours 1-3 (order hours: h1 16-17,
   h2 20-23, h3 16-18 orders per game) — 452-476 units, 16-18k coins, the single
   largest spend line. It adds one COW per day d3-d9 (2 on d0) and sheep in blocks
   (d6: 3, d12: 4). Fertilizer sales start d2 (4 units @98-99) and run 4-17 units
   every day to d29 (217-231 units, 11-12k). We buy 4 cows + 1 sheep + 1 goose at
   d0h1 (cash 1,353 -> 165) then nothing until d5 (1 cow) and d8-d10 (sheep, geese);
   our wheat purchases are the d0 53-unit pump plus 5-10/day for feed (106-190).
   Both sides sell 150-324 fertilizer; SpaTaro's milk+wool 44-60k vs ours 9-91k
   (wool 85k in game 697 with 17 sheep). Mixed; SpaTaro's herd is earlier and steadier.
5. **Wheat volume.** SpaTaro plants 155-166 wheat tiles (44 in the 4 days after
   BAKERY appears on d20 in game 1; 35 after PET_CAFE d11 and 38 after
   FARMERS_MARKET d23 in game 2) and sells 714-727 units at 40-48 late (69-87
   units/day on d27-d29). We plant 73-131 wheat tiles and sell 215-333. Wheat is
   24-31k of SpaTaro's revenue vs 7-11k of ours (18k in the 474-unit loss 990).
   Favours SpaTaro in gross; net of the 16-18k wheat it buys back the wheat line
   is ~+8-14k, comparable to ours.
6. **No geese, eggs or tomato; late carrot only.** SpaTaro sells 0 eggs, 0 tomato,
   30-55 carrots (14-16 carrot tiles, of which 7-14 after PET_CAFE/FARMERS_MARKET
   unlocks on d17/d23). Its post-unlock plantings are wheat+strawberry for every
   shop type until d23. We plant tomato after BRUNCH_SPOT/ICE_CREAM_SHOP (9 and 8
   tiles, game 147; 142 tomato units, 30k) and carrots after FARMERS_MARKET/
   YARN_STORE d20-d23 (28-30 tiles; 197-306 units in games 147/911), plus 1-5
   geese (46-188 eggs, 2-10k). Favours us in days 21-29 (we earn 42-70k there vs
   SpaTaro's 29-34k).
7. **Selling cadence.** SpaTaro issues 232-242 sell turns per game (8/day; 12-15/day
   from d10), 27-34 % of units in hour 0 and the rest across all 23 other hours;
   its late strawberry goes at 170-226 on d15-d20 then collapses to 8-36 on d21-d25
   (72 units sold below 40). We sell in 49-56 turns, 60 % of units at hour 1 and 39
   % at hour 18, never at hour 0. Strawberry: ours 200-241 units at avg 115-137
   over the game vs SpaTaro 203-268 at avg 119-135 — no price edge either way.
8. **Land timing is the same.** Quad 2 on d5 (ours, cash 1.8-1.9k) vs d6 (SpaTaro,
   1.3-1.4k); quad 3 d10 (ours) vs d8-d9 (SpaTaro). Not a differentiator.
9. **Finish.** SpaTaro leaves 1 planted tile and 1-23 shed units at step 719; we leave
   0-19 planted tiles (16 in game 147, 19 in game 508 — 12-14 of them melon) and
   0-7 fertilizer. Favours SpaTaro by a few thousand at most.

## (d) What the replays cannot tell us

- Opponent strength in SpaTaro's two games (Otter Vibe, ymg_aq): ratings are not in
  the json, so SpaTaro's +5-7k margins are not comparable to our +8-22k vs 2500-2700.
- Whether SpaTaro's daily wheat purchases are feed or a price attack: the engine only
  fills BUY_PRODUCT for WHEAT/FERTILIZER, and SpaTaro also queues BUY_PRODUCT for
  CARROT/MILK/STRAWBERRY/TOMATO/WOOL/MELON every morning (never filled) — noise or
  a probe, indistinguishable here.
- Why 155-166 wheat tiles yield 714-727 wheat units (4.4/tile): fertilized regrowth,
  replanting inside the same day, or harvest counting — not derivable from tile diffs.
- Shop-adaptivity: only 2 SpaTaro games, 7 distinct shop sequences; the d23
  FARMERS_MARKET -> 14 carrots and d17 PET_CAFE -> carrots d24-27 are suggestive
  of reaction but could be fixed late-game carrot slots.
- Melon price SpaTaro would have got against a seat that also dumps on d10 (both its
  opponents here dumped later or not at all).
- n=2 for SpaTaro; day-to-day figures (e.g. 8 vs 6 cows) vary between its two games.

## (e) Files and scripts used

- Replays: `S/flow198/eps/ep_107738945.json`, `S/flow198/eps/ep_107738965.json`
  (SpaTaro); `S/ep_107744147.json`, `S/ep_107743508.json`, `S/ep_107723697.json`,
  `S/ep_107738911.json` (ours; also profiled `S/ep_107737990.json`,
  `S/ep_107735016.json`, `S/ep_107729041.json`). `S/ep_107460204.json` does not exist.
- Reused: `scripts/replay_profile.py` (`SeatAcc`, `_simulate_market`, `_fib`).
- Written (scratchpad, `/tmp/claude-0/-mnt-e--work-kaggriculture3/ceff837c-0f2b-47d5-9f53-fe5fc99063a1/scratchpad/spataro/`):
  `ledger.py <replay> <team name> <out.json>` (per-day ledger + opening log, prints
  the text table; outputs `sp1.txt/sp2.txt`, `us_<id>.txt`, matching json),
  `summ.py *.json` (one summary row per game used for table (b)),
  `hours.py` (sell-hour histogram, wheat-buy hours, shop-unlock -> next-4-day plantings).
  Run with `JAX_PLATFORMS=cpu python3 ...` from the repo root.
- Prior context glanced: `docs/strategy/2026-09-10-livec-loss-anatomy.md`,
  `docs/strategy/2026-09-09-loss6-anatomy.md`.

Durable copies of the ledger scripts: S/spataro/tools/{ledger,summ,hours}.py (scratchpad originals are lost on reboot).
