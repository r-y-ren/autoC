# Majkel1337 (LB #2, ~3090) vs SpaTaro (LB #1, ~3108) — how the losses happen, 2026-09-11

Measurement only; no levers proposed. Six SpaTaro losses to Majkel1337 on 2026-09-11
(episodes 107751894 −18,402 / 107722216 −8,203 / 107727330 −6,938 / 107683794 −6,038 /
107744872 −2,522 / 107722209 −1,802; SpaTaro ratings 3101-3135, Majkel 3027-3089 at
the time). `S/spataro/rows.json` has NO SpaTaro win over Majkel1337 (0-6), so there is
no contrast game. Method = the SpaTaro-vs-ours ledger (`scripts/replay_profile.py`
`_simulate_market`, recon error 30-532 coins per seat per game) run on BOTH seats,
plus a per-hour two-seat market-flow pass. Day = (t-1)//24, hour = (t-1)%24; "hands
on day d" = max crew seen that day. M = Majkel1337, S = SpaTaro.

## (a) How Majkel1337 beats SpaTaro

Majkel1337 is the same farm as SpaTaro — six-product wheat/strawberry/melon/milk/wool/
fertilizer, purse run to 0-100 coins every evening for nine days, 12-melon d0-d2
pot race dumped on d10, quad 2 on d6 and quad 3 on d8-d9, 11 hands from d10, 213-268
sell turns spread over the day — and it does NOT out-earn SpaTaro: its gross revenue
is lower in 4 of 6 games (median −3.9k, range −16.5k…+9.9k). It wins on the cost
side: it buys 117-190 wheat units (4.1-7.2k) where SpaTaro buys 375-535 (14.0-21.7k),
so its total spend is 7.7-18.6k lower in every game (median −8.8k) while SpaTaro's
extra bought wheat comes back only partly as extra wheat sales (SpaTaro's net wheat
line is +8.5…+18.1k vs Majkel's +5.0…+12.5k in the 4 games where it is ahead, and
negative in 107722209). On the revenue side Majkel re-mixes rather than adds: it
gives up 5-17k of wheat revenue and 0.3-5.5k of carrot in every game and takes back
strawberry (+2.9…+7.4k in 5/6, by holding 39-66 units off the d20-d24 price collapse
and selling them on d27-d29 at 146-232), melon (+0.5…+2.7k in 4/6 from 12 tiles / 72
units vs 9-11 / 54-66), tomato (+0.6…+6.0k, 6/6, SpaTaro grows none), eggs (+3.5-4.6k
in the 3 games it buys 2 geese) and wool (+2.1…+5.6k in 4/6, 3 sheep on d0 vs 2).
The timeline is the mirror of SpaTaro-vs-ours: SpaTaro is ahead at d10 in all six
games (8.7k vs 5.9k median; its 6-7 day-0 hands and 48-unit melon dump start earlier),
Majkel out-earns it in d11-d20 in all six (59.0k vs 53.0k) and in d21-d29 in all six
(48.0k vs 44.6k), and the +1.8…+18.4k margin equals the spend gap plus the mix
re-shuffle. Neither seat attacks the other's market: Majkel's only BUY_PRODUCT item
is WHEAT (feed), its d0 five-unit buy-and-sell-back is a ~20-coin event, and the two
seats' shared d10 melon dump costs each of them ~10 coins/unit versus SpaTaro's
solo dumps.

## (b) Key numbers (median across the six games; per-game range in brackets)

| metric | Majkel1337 | SpaTaro |
|---|---|---|
| hands d0 / d5 / d10 | 4 / 6 / 11 (identical all 6) | 6-7 / 6-7 / 10-11 |
| hand-days d0-9 / d10-19 / d20-29 | 68 [67-68] / 110 / 108 | 70 [68-73] / 105.5 [104-113] / 102.5 [97-108] |
| hire spend (coins) | 4,929 | 4,239 [3,769-5,353] |
| tiles planted by d10 / by d20 / whole game | 63.5 [60-65] / 154.5 [140-158] / 256.5 [229-265] | 70.5 [49-83] / 149 [129-178] / 243.5 [163-284] |
| standing tiles d10 / d20 / d29 | 55.5 / 54 / 6.5 [3-13] | 54.5 / 57 / 3.5 [0-8] |
| melon tiles (planted) / dump day / dump units / dump avg price | 12 (6 d0, 4 d1, 2 d2) / d10 / 30 / 244.5 [240-249] | 10.5 [9-11] (8-9 d0, 2 d2) / d10 / 36 [30-48] / 243.5 [240-247] |
| melon units sold / melon revenue | 72 (all 6) / 14.5k [14.1-14.9k] | 63 [54-66] / 13.5k [12.1-14.2k] |
| wheat tiles / units sold / wheat revenue | 185.5 [140-208] / 397.5 [273-499] / 15.3k [11.2-19.7k] | 148.5 [114-214] / 672.5 [511-890] / 25.8k [20.4-34.1k] |
| wheat units BOUGHT (spend) | 151 [117-190] (5.5k [4.1-7.2k]) | 397 [375-535] (15.6k [14.0-21.7k]) |
| net wheat line (revenue − bought) | +10.1k [+5.0…+12.5k] | +10.3k [−1.3…+18.1k] |
| cows / sheep / geese bought | 8.5 [5-12] / 5.5 [3-10] / 1 [0-2] | 8.5 [4-14] / 8 [4-11] / 0 |
| animal spend | 6.65k [5.7-7.9k] | 7.35k [5.8-10.6k] |
| fertilizer units sold / revenue | 187.5 [156-220] / 11.6k | 222 [166-323] / 12.6k |
| strawberry units / avg price / revenue | 254 / 180.5 [162-211] / 47.0k [30.8-54.0k] | 256 / 160 [135-205] / 42.0k [23.8-54.0k] |
| strawberry units sold d20-d24 / d27-d29 | 77 [35-78] / 53 [39-66] | 114 [55-147] / 17 [2-38] |
| tomato / egg / carrot revenue | 4.5k [0.6-6.0k] / 1.7k [0-4.6k] / 0.8k [0-8.5k] | 0 / 0 / 3.0k [0.3-14.0k] |
| sell turns / share of units sold at hour 0 | 244 [213-268] / 16.5 % | 228 [220-241] / 34 % |
| land: quad 2 (day, cash before) / quad 3 | d6 1.9-2.1k / d9 1.2-3.1k | d6 1.2-1.5k / d8-d10 2.0-2.3k |
| cash end of d10 | 5.9k [4.7-7.3k] (behind in 6/6) | 8.7k [5.6-12.3k] |
| cash end of d20 | 65.6k [55.0-82.3k] (ahead in 5/6) | 63.4k [58.3-81.6k] |
| earned d11-d20 / d21-d29 | 59.0k [50.2-77.6k] / 48.0k [31.6-78.1k] (ahead 6/6 both) | 53.0k [49.7-76.0k] / 44.6k [22.3-77.0k] |
| gross revenue / total spend | 139.2k [110.9-184.8k] / 27.6k [25.0-28.1k] | 137.8k [112.5-201.3k] / 36.2k [35.2-46.3k] |
| final / margin | 114.4k [86.6-160.4k] / +6.5k [+1.8…+18.4k] | 105.3k [80.6-158.6k] |

## (c) The differences, with numbers

1. **Bought wheat is the whole cost gap (consistent 6/6).** Spend difference M−S per
   game: −8.7k, −7.8k, −12.9k, −7.7k, −8.8k, −18.6k; of which the WHEAT purchase line
   is −8.8k, −8.8k, −12.3k, −8.5k, −9.6k, −16.2k. Seeds (+0.0…+0.8k), animals
   (−2.7k…0), hires (+0.4…+1.2k in 5/6) and land (0) are noise beside it. SpaTaro buys
   wheat every day of the game (11-20 on d0, 15-38/day d6-d12, 2-43/day to d29), and
   runs a buy-then-sell-back loop on d0-d9 (11-22 events per game where wheat bought
   at 29-31 is sold within 6 hours). Majkel buys 5-8/day d0-d2, nothing d3-d5, 3-30/day
   d6-d9, one large 35-77-unit feed purchase on d10 after the melon cash, and 13-15
   units on 0-4 late days; 20-28 BUY_PRODUCT orders per game, all WHEAT.
2. **Revenue is level, not higher (varies).** Gross revenue M−S: +9.9k, +0.4k, −6.1k,
   −1.6k, −6.5k, −16.5k. Majkel wins the three games where its revenue is lower by
   spending less; in 107722209 (margin +1.8k) SpaTaro out-grossed it by 16.5k (76k
   milk from 14 cows) and lost anyway on 21.7k of bought wheat.
3. **Wheat revenue down, strawberry up (both consistent).** Wheat revenue M−S: −14.4k,
   −12.3k, −11.4k, −17.3k, −8.3k, −5.2k (6/6). Strawberry revenue M−S: +7.4k, +4.4k,
   +2.9k, +7.0k, +5.6k, −0.04k (5/6), on the SAME unit count (254 vs 256): Majkel's
   average strawberry price is 162-211 vs SpaTaro's 135-205 (+6…+27/unit, 6/6). The
   mechanism is timing: in the four games with a d20-d24 strawberry collapse (107751894
   142→19-34, 107722216 189→82-115, 107744872 180→94-144, 107683794 111-143 depressed
   d18-d22) SpaTaro sells 55-147 units into it and Majkel 35-78; Majkel then sells 43-46
   units on d28/d29 at 146-193 where SpaTaro has 0-12 left. Same 36 strawberry tiles.
4. **Melon: one more row of tiles, same dump day (consistent).** Majkel plants exactly
   12 melon tiles (6 on d0 hours 10-14, 4 on d1, 2 on d2) in all six games and sells
   exactly 72 units; SpaTaro plants 8-9 on d0 plus 2 on d2 (9-11) and sells 54-66.
   Both dump on d10: SpaTaro sells first (6 units at h4-h5 for 270, 6 at h9 for 260),
   Majkel sells 30 units in h10-h13 at 250→230-244, SpaTaro the rest at h10-h21 down
   to 205-222. Majkel then sells 6 on d11 (198-221) and 24-30 on d11/d12 (154-192),
   SpaTaro 6-18 on d11 and 6-10 on d12-d13 (114-150). Melon revenue M−S: −0.1k, +2.4k,
   +1.5k, +0.5k, −0.05k, +2.7k.
5. **Products SpaTaro never grows (consistent for tomato, varies for eggs).** Majkel
   plants 1-10 tomato tiles between d10 and d19 in all six games (1 on d10 in three games, the rest d15-d19) (8-72 units, 0.6-6.0k) and
   buys 2 geese on d6 in three games (71-77 eggs, 3.5-4.6k); SpaTaro has 0 tomato, 0
   eggs in all six. SpaTaro instead plants 4-85 carrot tiles after PET_CAFE/
   FARMERS_MARKET (0.3-14.0k, higher than Majkel in 6/6, Majkel 0-69 tiles).
6. **Herd: wool over milk (varies).** Majkel buys 2 cows + 3 sheep at d0h1 (all 6)
   and adds on d6 either 4 cows + 2 geese (3 games), 6 cows (2) or 2 cows + 4 sheep
   (1); SpaTaro buys 2 cows + 2 sheep at d0h0 and adds one cow a day d3-d9 and sheep
   in blocks. Wool M−S: +4.4k, +4.0k, +5.6k, +2.1k, −1.5k, −2.1k; milk M−S: +1.8k,
   −1.5k, −2.3k, −1.5k, −1.1k, −10.3k. Fertilizer units S 166-323 vs M 156-220 (S
   higher 4/6; revenue level, −0.8k median).
7. **Labour: fewer day-0 hands, flat 11 afterwards (consistent).** Majkel hires 4 at
   d0h1 (cost 7, after buying 1 cow + 5 wheat at h0 with 3,000), 4 on d1, 6 on d2-d5,
   8/9/9/9-10 on d6-d9, then 8 at h0 + 3 at h1 = 11 every day d10-d27 and 10 on
   d28-d29 — the hand vector is identical in five games and differs by one hand (9 on d9) in the sixth. SpaTaro hires 6-7 on d0,
   6 on d1-d5, 7-9 d6-d8, 9-10 d9, then 10-12 varying by day and tapering to 7-9 on
   d28-d29. Hand-days d0-9 68 vs 68-73 (SpaTaro ahead), d10-29 218 vs 194-221.
8. **Cash curve (consistent shape).** End-of-day cash d0/d2/d4/d6/d8: Majkel 7-9 /
   16-80 / 289-422 / 12-209 / 1,030-2,127; SpaTaro 0-122 / 13-164 / 12-79 / 2-36 /
   0-986. Majkel carries a few hundred idle coins on d4-d5 and ~1-2k on d8 that
   SpaTaro spends; SpaTaro's d10 cash is higher in all six games (5.6-12.3k vs
   4.7-7.3k), Majkel's d20 cash in five (55.0-82.3k vs 58.3-81.6k).

## (d) Market interaction — does Majkel1337 attack SpaTaro's market?

- **Buy-then-sell pumps: one token event.** Majkel's only buy→sell-back-within-6h
  wheat events on d0-d9 are 1-4 per game: 5 units bought at d0h0 (quote 25→28-29)
  and 3-4 sold back one per hour at h1-h5 (27-29 each), plus 1-2 two-unit events on
  d1-d2. SpaTaro buys 6-19 wheat units in the same d0h0 order set, so its d0 wheat
  costs +3-4/unit ≈ 20-70 coins more; the pump costs Majkel ~15-25 coins. Immaterial.
  SpaTaro's own d0-d9 buy→sell-back loop is 11-22 events per game.
- **Buying what SpaTaro sells: coincidence-level.** Majkel's executed wheat buys in the
  same hour SpaTaro executes a wheat sale: 27, 30, 3, 21, 13, 25 units per game =
  2-16 % of Majkel's buys, concentrated at h0-h3 where both seats trade. Majkel issues
  no BUY_PRODUCT for any item but WHEAT (SpaTaro issues 300-450 unfilled orders per
  game for CARROT/TOMATO/MELON/STRAWBERRY/MILK/WOOL/EGG).
- **Melon price effect: shared dump.** Both seats dump on d10; the quote falls 272
  (h0-h3) → 266 (h4-h9) → 250-244 (h10-h12) → 232-221 (h13-h16) → 205-226 (evening).
  Each seat realises 240-249 on d10 vs SpaTaro's 252-254 in its games against
  non-dumping seats (2026-09-11-spataro-vs-ours.md): ≈ −10/unit ≈ −300…−500 coins
  each; symmetric, SpaTaro's earlier h4/h9 blocks earn it 270/260 on 12 units.
- **Strawberry price effect: shared, SpaTaro pushes harder.** Combined d20 volume
  60-101 units; the d20-d24 collapse occurs in 4/6 games and both seats sell into it,
  SpaTaro 1.5-2x the units. Attribution of the price fall to one seat is not
  possible from the replay (single shared quote); what is measurable is that
  Majkel withholds 39-66 units to d27-d29.
- No other cross-seat pattern: no fertilizer buys by Majkel (SpaTaro buys 1-9 in
  3 games), no seed-price or land interaction (both quad 2 on d6).

## (e) What could not be told

- No SpaTaro win vs Majkel exists (0-6 in rows.json), so "what SpaTaro does when it
  wins the pairing" is unmeasured; ratings of both were 3027-3135, so the games are
  peer-level.
- Whether SpaTaro's 375-535 bought wheat is feed for its larger herd (fertilizer 166-323
  units) or an unprofitable churn: milk+fertilizer revenue is only 0.8-1.5k higher than
  Majkel's on median while the wheat line costs 8.5-16.2k more; the split between feed
  and sell-back cannot be read from tile/shed diffs.
- Whether Majkel's late strawberry hold is a price rule or a fixed schedule: 5/6 games
  sell 43-46 units on d28/d29, the sixth (no collapse) sells evenly — consistent with
  either.
- Shop adaptivity: tomato is planted d10-d19 in all six games regardless of which shops
  unlocked (BRUNCH_SPOT d5/d8/d14, PIZZA d5/d11/d17, or neither in 107722209), and the
  d1-d2 melon rows (4+2) and d0 herd (2 cows + 3 sheep) are identical in all six, so
  the opening looks scheduled, not reactive; carrot (0-69 tiles) does vary with FARMERS_MARKET/
  PET_CAFE but n is small.
- Recon error 218-264 coins on Majkel's seat in 5/6 games (30 in one) vs 33-532 for
  SpaTaro; sub-1k line items (fertilizer, eggs) carry that uncertainty.

## (f) Files and scripts used

- Replays (downloaded this session): `S/spataro/ep_107751894.json`, `ep_107722216.json`,
  `ep_107727330.json`, `ep_107683794.json`, `ep_107744872.json`, `ep_107722209.json`.
- Ladder record: `S/spataro/rows.json` (6 Majkel1337 rows, all won=false).
- Reused: `scripts/replay_profile.py` (`SeatAcc`, `_simulate_market`, `_fib`);
  scratchpad `spataro/ledger.py` (unchanged, run per seat).
- Written (scratchpad `/tmp/claude-0/-mnt-e--work-kaggriculture3/ceff837c-0f2b-47d5-9f53-fe5fc99063a1/scratchpad/spataro/mj/`):
  `<seat>_<episode>.txt|json` (12 per-day ledgers), `summ2.py` → `summary.txt` (the
  table in (b), per game), `market.py` → `market.txt` (two-seat per-hour flows: melon
  d10 hour sequence and quote, wheat buy/sell overlaps, pump events, BUY_PRODUCT order
  mix, strawberry by day, first-sale days, cash curves), and an inline decomposition of
  each margin into revenue-line and spend-category differences (reproduced in (c) 1-2).
  Run with `JAX_PLATFORMS=cpu python3 ...` from the repo root.
- Prior context: `docs/strategy/2026-09-11-spataro-vs-ours.md`.
