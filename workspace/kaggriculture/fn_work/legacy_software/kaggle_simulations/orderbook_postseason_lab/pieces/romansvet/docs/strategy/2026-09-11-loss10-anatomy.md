# Loss-10 anatomy (2026-09-11, ladder losses of candidate B, sub 56161192)

Measurement only. Ledgers rebuilt from the replays with scripts/replay_profile.py market
re-simulation (recon_err 0-350 coins per seat). Scratch: scratchpad/bloss/{ledger,runall,cmp,rev}.py,
per-seat ledgers led_<id>_{us,opp}.{json,txt}, cmp.txt.

## Answer

There is no counter-class. All ten opponents (rated 2175-2381, ten different team names) are the
same open-loop public clone, and it is the SAME file we beat three times this morning against
"2500-2600" names (107744147, 107743508, 107735016): identical hire schedule (5 hands at d0h1, 3/4/5/4/3-4/7/6-7/8/8 by
d9, 11 at d10), 12 melon tiles planted d0h7-h12 with the purse run to 530, pastures h3-h9 with 2 cows + 2 sheep,
land d6 and d11, 160 wheat / 33 strawberry / 31 carrot tiles for the game, and a 60-melon dump at d10h0 for 247 each
(14.8k). Six of the ten action streams are 97-100 % byte-identical to the first loss; the other four differ only in
late-game details (the ledgers through d11 are identical to the coin). Their d0 market play (BUY 13 / SELL 13 /
BUY 13 wheat at h0, SELL 13 + BUY 5 at h1) is their own micro-pump and does not touch us. Our seat's day-by-day
margin is the same curve in every one of the 13 games, win or loss: ≈ 0 through d9, one −16.4k step on d10
(their melon dump; our melon is planted d9-16 and sold d20-27 at 190-200), −4k more on d11, trough of −16.5…−28.3k
on d14-16, then recovery. The ONLY thing that separates the 10 losses from the 3 wins is the size of the d15-29
recovery: +12.1…+21.3k (mean +16.6k) in the losses vs +18.9/+30.2/+33.7k in the wins, and the recovery is decided
by the town's shop sequence, which the clone ignores and our planner follows: both large wins had PIZZA_SHOP on d8
(tomato revenue +30.0k and +4.1k for us; the clone plants no tomato), while in the ten losses PIZZA_SHOP arrives
d14/d20/d23 or never and our tomato revenue is 0-3.6k. Two structural gaps vs this clone are present in all 13
games and make every game a near coin-flip (loss margins −0.7…−8.5k, mean −3.6k): FERTILIZER (they sell 340-356
units for 17-19k, we sell 131-245 for 8-12k: −7.3k mean in losses AND −7.3k in wins) and the melon pot (−3.3k mean,
they sell 60 at 247 on d10, we sell 12-30 at 132-213 from d20). Our OPEN_PUMP costs 177 coins and does nothing to
them: they sell 13 wheat into our pumped quote at 32.8, buy 5 back at 28, and still complete 5 hires + 2 cows + 2
sheep at h1 with 1,100 cash left (no refusal). The "two losing-record files that beat us every time" are this clone
too; their overall records are losing because the clone loses to the top band, not because they are weak vs us.

## Per-game table

Hands = d0/d5/d10 (max). Melon = tiles planted / main dump day @ price. Wheat = units bought over the game.
"Neg" = first day the cash margin is meaningfully negative (all games: d10, the melon dump; earlier days are ±1k).
Trough = worst end-of-day margin. Rec = margin change d15→d29 (us − opp). Item deltas are our revenue − theirs (k).

| game | opponent (rating) | their d0 opening | hands us / opp | melon us / opp | wheat us / opp | neg | trough | final | decisive items |
|---|---|---|---|---|---|---|---|---|---|
| 107764944 | Sinh Nguyễn Đức (2203) | 5 hires h1, 12 melon, 2 cow 2 sheep, purse 530 | 4/5/9 (14) / 5/4/11 | 17 / d22 @193 ; 12 / d10 @247 | 144 / 155 | d10 −13.9k | d16 −24.0k | −0.7k | rec +21.3k: carrot +10.6 (PET_CAFE d2), wool +7.5; fert −5.2, milk −3.9, wheat −3.9, melon −3.1 |
| 107766829 | daulettoibazar (2381) | same | 4/5/9 (13) / 5/4/11 | 17 / d22 @193 ; 12 / d10 @247 | 128 / 129 | d10 −15.0k | d15 −22.2k | −1.5k | rec +20.7k: wheat +3.9, egg +2.7; wool −3.6, fert −3.3, melon −3.0 |
| 107769126 | dont share my work (2220) | same | 4/5/10 (12) / 5/4/11 | 17 / d22 @183 ; 12 / d10 @247 | 112 / 155 | d10 −12.4k | d15 −16.5k | −3.5k | rec +12.9k: carrot +7.3, egg +5.3, tomato +3.6 (FARMERS d11); fert −6.8, straw −6.0, melon −2.7 |
| 107769991 | JiangWenfeng1 (2188) | same | 4/5/8 (12) / 5/4/11 | 15 / d22 @201 ; 12 / d10 @247 | 160 / 155 | d10 −12.5k | d15 −20.3k | −4.7k | rec +15.7k: straw +8.8, egg +3.4; wool −9.9 (YARN d17), fert −7.5, melon −3.2 |
| 107771992 | Variiiiiii (2175) | same | 4/5/8 (13) / 5/4/11 | 12 / d22 @213 ; 12 / d10 @247 | 198 / 155 | d10 −13.8k | d16 −28.3k | −8.5k | rec +15.6k: straw +17.5, milk +11.5; wool −19.1 (they 34.7k, YARN d11), fert −8.1, melon −4.7 |
| 107777972 | cha7ura (2334) | same | 4/5/8 (13) / 5/4/11 | 15 / d22 @201 ; 12 / d10 @247 | 138 / 155 | d10 −12.8k | d16 −21.5k | −3.5k | rec +16.8k: straw +9.3, carrot +3.6; fert −7.8, wool −3.6, milk −3.6 |
| 107779009 | Maksim Borisov (2300) | same | 4/5/8 (12) / 5/4/11 | 13 / d22 @193 ; 12 / d10 @247 | 148 / 155 | d10 −12.5k | d15 −19.2k | −0.9k | rec +18.3k: straw +9.3, egg +5.6; fert −7.9, wool −5.8, melon −4.1 |
| 107779976 | TOSS (2279) | same | 4/5/9 (13) / 5/4/11 | 17 / d25 @132 ; 12 / d10 @247 | 124 / 155 | d10 −13.8k | d14 −21.3k | −5.4k | rec +14.7k: wool +4.9, wheat +2.8; fert −5.5, milk −3.3, melon −2.9 (our dump landed on a 132 quote) |
| 107780983 | My second life (2284) | same | 4/5/9 (12) / 5/4/11 | 15 / d22 @188 ; 12 / d10 @247 | 105 / 155 | d10 −12.7k | d14 −17.8k | −4.7k | rec +12.1k: straw +8.1, carrot +3.0; fert −10.8, milk −6.3, wool −3.3 |
| 107781955 | Kucing Garong (2269) | same | 4/5/9 (12) / 5/4/11 | 14 / d22 @201 ; 12 / d10 @247 | 153 / 155 | d10 −12.8k | d15 −20.7k | −3.2k | rec +17.5k: straw +11.4, carrot +7.6, tomato +3.2; wool −10.3, fert −9.8, melon −3.5 |
| WIN 107744147 | Fuat Çakıcı | same clone (d0 wheat 13 only) | 4/5/10 (12) / 5/4/11 | 14 / d22 @193 ; 12 / d10 @247 | 148 / 137 | d10 −12.6k | d14 −17.9k | +16.3k | rec +33.7k: TOMATO +30.0 (PIZZA d8, FARMERS d5), carrot +7.6; fert −8.2, wool −5.6 |
| WIN 107743508 | Satoshi Nguyen | clone variant: 14 hands, 3rd land d18, 312 wheat | 4/5/9 (12) / 5/4/11 (14) | 15 / d22 @188 ; 12 / d10 @247 | 190 / 312 | d10 −16.6k | d15 −21.6k | +8.5k | rec +30.2k: tomato +4.1 (PIZZA d8), wool +2.4; opp overspent hires (9.6k vs our 5.3k) and land 7k |
| WIN 107735016 | test_money | same clone | 4/5/10 (12) / 5/4/11 | 16 / d22 @201 ; 12 / d10 @247 | 107 / 155 | d10 −12.4k | d14 −18.4k | +2.0k | rec +18.9k: straw +7.4, carrot +7.2, egg +4.0; fert −10.4, wool −3.2 |

Shop sequences (unlock day): losses — L1 PET2 SMOOTHIE5 YARN8 ICE11 FARMERS17 PIZZA23; L2 SMOOTHIE2 YARN5 BAKERY8
ICE14 PET17 BRUNCH20 FARMERS23; L3 BAKERY2 PET5 ICE8 FARMERS11 BRUNCH17 SMOOTHIE20; L4 ICE2 BAKERY5 SMOOTHIE8
FARMERS11 PIZZA14 YARN17 BRUNCH20; L5 SMOOTHIE2 YARN11 BRUNCH14 BAKERY17 PET20 FARMERS23; L6 BRUNCH2 SMOOTHIE5
PET8 YARN11 PIZZA14; L7 ICE2 BAKERY5 BRUNCH8 PIZZA20 YARN23; L8 BAKERY2 FARMERS5 YARN8 ICE14 SMOOTHIE17; L9 PET2
BRUNCH5 ICE11 PIZZA14; L10 FARMERS2 ICE5 PET8 YARN14 BRUNCH17. Wins — W1 PET2 FARMERS5 PIZZA8 BRUNCH14 ICE20
YARN23; W2 YARN2 FARMERS5 PIZZA8 SMOOTHIE11 BAKERY17; W3 FARMERS2 PET5 BRUNCH8 YARN11 BAKERY17 PIZZA20.

## Common mechanism, with numbers

1. Same opponent in all 13 games. Opponent hire events, plant totals, animal buys, land days, wheat buys by day
   (31/8/6/10/21/18/40/21 on d0/1/4/6/8/9/10/11), melon dump (60 @ 247 on d10h0) and fertilizer sales are identical
   across the 10 losses and 2 of the 3 wins; the third win is a hand-modified variant of the same clone.
   Action-stream identity vs loss 1: 100/39/97/99/99/32/99/71/98/100 % (the 32-39 % ones differ in serialisation or
   late detail only; ledgers equal through d11). Our own actions diverge from game to game at d3h0 (shop reaction)
   but our per-day cash curve is identical to ±0.5k through d9 in all 13 games.
2. The d10 step = their melon pot. Daily earn delta (us − opp) on d10 is −15.1…−18.4k in every game (their 60
   melons 14.8k + strawberry at h0 vs our d10 sales). Cash at end of d10: they 16.2-18.4k, we 3.2-4.8k. We plant
   melon only from d9 (1-3 tiles/day to d16, 12-17 tiles) and sell it d20-27 at 183-213 (once 132) — total melon
   revenue 12.7-14.8k vs their 17.4k, i.e. −3.3k mean, but the CASH TIMING (their +14k on d10 → land d11 and 11
   hands) is the step. This is identical in wins and losses, so it is not what decides these ten games.
3. Fertilizer: they sell 340-356 units (16.4-19.3k) in every game; we sell 131-245 (8.4-11.9k) and end with 1-14
   unsold. Delta −3.3…−10.8k, mean −7.3k in losses and −7.3k in wins. Structural, not decisive.
4. Wool: negative in 8/10 losses (−2.9…−19.1k, mean −4.6k); their 6 sheep are placed on d0-d1 and YARN_STORE sells
   for them as well. In the −8.5k loss (L5) wool alone was −19.1k (they 34.7k).
5. What decides the ten: the d15-29 recovery. Losses +12.1…+21.3k (mean +16.6k) vs trough −16.5…−28.3k
   (mean −21.2k). Wins +18.9/+30.2/+33.7k vs trough −17.9/−21.6/−18.4k. The recovery comes from our shop-driven
   crops: tomato via PIZZA_SHOP d8 (+30.0k in W1; 25 tiles; the clone never plants tomato so the price is ours),
   carrot via PET_CAFE/FARMERS (+7…+11k), strawberry (+8…+17k where the clone's 33 tiles do not flood it). Where
   PIZZA is late/absent (all 10 losses) our tomato revenue is 0-3.6k and the recovery falls 1-8k short.
6. Hands: they reach 11 by d10 for 3.6k of hire spend (one cheap h0/h1 hire per day); we reach 8-10 for 4.5-7.5k
   (bunched hires at h0: +3/+4 on d10). Hire spend delta against us +0.9…+3.9k in 9/10 losses; in the variant we beat
   (W2) the clone over-hired (+4.4k against it). Structural, present in wins too.
7. Pump interaction (Q4): our BUY 53 at h0 costs 1,640 (quote 25→33); our SELL 48 at h1 returns 1,463; net −177
   coins and 5 wheat kept. The clone's h0 BUY 26 / SELL 13 executes in the same lockstep (buys at 30.6 avg, sells at
   32.8), then BUY 5 at 28 — it profits ≈ +30 from our pump and its d0 purchases (5 hires, 2 cows, 2 sheep, 12
   melon seed) all fill; the pump neither hurts nor helps here. Nothing in their play targets us: they place no
   BUY_PRODUCT other than wheat (their own planting stock), sell melon before we hold any, and their d10 40-wheat
   buy is planting stock.

## Per-game cost of the mechanism (coins, day)

d10 melon step (us − opp daily delta on d10): L1 −17.4k, L2 −18.4k, L3 −15.1k, L4 −16.4k, L5 −17.4k, L6 −16.1k,
L7 −16.3k, L8 −16.0k, L9 −15.1k, L10 −16.2k (wins: −16.0/−16.7/−15.6k). d11 second step −3.1…−4.7k in all 13.
Fertilizer gap over the game: L1 −5.2k, L2 −3.3k, L3 −6.8k, L4 −7.5k, L5 −8.1k, L6 −7.8k, L7 −7.9k, L8 −5.5k,
L9 −10.8k, L10 −9.8k. Shortfall of recovery vs the wins' mean (+27.6k): L1 −6.3k, L2 −6.9k, L3 −14.7k, L4 −11.9k,
L5 −12.0k, L6 −10.8k, L7 −9.3k, L8 −12.9k, L9 −15.5k, L10 −10.1k — this is the quantity that maps to the final
margins (−0.7…−8.5k) once the d10-16 trough (which is the same size in wins) is netted out.

## Class description (Q2)

Not the SpaTaro/Majkel template (6 hands d0, herd h0, 30+ melon). This is the public "band" clone: 5 hires at h1,
12 melon d0h7-h12, 2 cows + 2 sheep d0, purse to 530, one hire per day, land d6/d11, ≈ 160 wheat as feed/fert
engine (350 fertilizer sold), 33 strawberry, 31 carrot, melon dumped once at d10h0, everything sold at h0
(219 h0 units) with 220+ sell turns; open-loop — it never reads the shop sequence. Its 2175-2381 ratings and the
two losing records (82-259, 72-155) are the same file rated by whom it met; against us it is a 3-10 coin-flip on
the shop draw, not a counter.

## Our seat vs our wins (Q3)

Identical through d9 in all 13 games (4 hires h0, pump, 1 goose 4 cows 1 sheep, 11 wheat + 8 carrot seed, land d5
and d10, min cash 112). Divergence is crop mix from d3 on: wins planted 25/18 tomato (PIZZA d8) and 55 carrot;
losses planted 0-7 tomato. Our melon is always late (d9-16) and sold at 190-200 instead of 247. Our sells are 100 %
late-hour (0 h0 units in every game) vs their h0 dump; that did not change between wins and losses.

## What could not be told

Whether the shop sequence is the WHOLE recovery difference (n = 3 wins; tomato explains W1 alone; W3 was +2.0k
with no PIZZA until d20). Why our fertilizer output is 100-200 units lower with more cows (not traced to feed
hours here). The parent's 1/20 pinned-town replay is consistent with the town (shop sequence) being the board
variable that decides these games; no seed-dependent mechanism was found.

## Files

S/ep_<id>.json for the 13 ids; S/bloss/{loss_ids.txt,rows.json}; scripts/replay_profile.py; S/spataro/tools/ledger.py
(copied to scratchpad/bloss/ledger.py, unchanged); scratchpad/bloss/{runall.py,cmp.py,rev.py,cmp.txt,led_*.json}.
