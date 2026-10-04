# BRAINSTORM1 (2026-09-29, round 1): the arms review, the invariants, and the ranked ways to beat the programme

Round 1 of a continuing brainstorm, 07:02-10:02Z, analysis plus 3 closed-loop runs. Files are in S/brainstorm1/.

## Verdict: NOT YET
No way found in round 1 meets all four "solid" conditions:
- a mechanism the engine explains;
- a ledger bound at least the size of the gap (+10.4k margin, or W >= 14/27 on live27) that does not shrink our late volume;
- a supporting first read;
- buildable and judgeable by 09-30 12:00Z.

The one family whose arithmetic bound reaches the gap is **PLATE-FIRST**: a melon plate on the starting tiles, sold on d10 before the programme's h9 first melon sale.
- Melon-market margin: +7.5k at 48 melons and +12.6k at 72 (pie2).
- Every funded plate so far paid for itself out of the d0-9 herd.
- PLATENOLAND1's partial read (per the orchestrator) is the same story. The plate on the starting tiles keeps COW 4 + goose, but the planner drops the sheep: own +2.1k, rival +7.3k. STOP=29 loses -8..-19k.
- A d0-9 herd coin is worth ~7-14 coins of margin; a d10+ coin is worth <= 1 (dialogue H8).
- Round 2's cell locks the programme's own d0 herd (2C + 3S, which is T3's lock: own +1.2k, W +4/-0) under a 5-6 tile shed-adjacent plate sold first on d10.

The two cheap adders tested here: T1 late tomato NONE (own -715, t -2.34) and T2 fertilizer race NONE (margin -46). T3 (the programme's d0 herd, WOOL_FIRST) reads own +1.2k, W +4/-0 but margin -0.9k: the early-wool race pays for the lost milk race.

## 1. Arms review (S/brainstorm1/arms.md + arms_A..D)
Every stream of 09-27..09-29 is one row, verbatim, in four files, about 115 arms in all. arms.md groups them into nine families.

| family | best cell | why it lost | constraint it proved |
|---|---|---|---|
| whole-programme imitation (BCBODY1-10, PACKCLONE1, PROGRAMME1, OPENPKG1, BOEY2) | clone r5a3 -34.7k closed loop; PROGRAMME1 -34k | 22 % fewer units executed; the scripted package cannot be funded or hired (3,060 > 3,000) | copying the schedule is not being the programme; BC data line CLOSED |
| d0 melon plate (D10WAVE1, MELONTRIAL1, REALLOC1, COMBO1, MELONSHIFT1, MELONDENY1, MELONDUMP1) | P8d3 m40 own +3.2k, margin -1.4k, W +5/-0 | the plate overflows the 25 starting tiles; the planner buys Q2 (1,000) at d0 and cuts cows/sheep/goose; the rival's late milk/wool/strawberry rise +10-17k | the plate must not be paid by the herd |
| herd / crew / land / yield / wheat scale (HERD1, CREW1, LAND1, YIELD1, WHEAT1, MILKSHOP1, EGGS2, Q4DIG1) | HERD1 c2 +0.4k ns | the d0-9 purse is fully cycled into the herd; Fibonacci hires; board full from d12 | capacity axes CLOSED |
| sale mechanics (SALESIDE1, SELLEARLY1, FLOORHOLD1, SLIP1, PRICEGAP1) | ask 0.96 -1.4k | no order book, lockstep quotes; held units are sold by the rival | CLOSED; our big lots are denial |
| KERNEL2 fire lists (V3..PACKWIDE1, FIRELIVE1) | band +43 on tapes | tape rivals cannot re-plan; live transfer -0.91 | tapes are not evidence |
| steering / arbitrage (STEER1, WHEATPUMP1, ARB1) | +0.1k/game | only the product book is shared; buys lift the rival's sale price | dead |
| gene / RL training (ESBAND1-2, ESFLAT1, PPO, BCSIM1) | flat | local peak on tapes; sparse win reward | a closed-loop fitness was never searched |
| judges (REACTCLONE1, JUDGERIVAL1-3, PRICEFAITH1, JC1) | - | clone rival 0.875x live, no late flood | g0capsfix for margin, flood for dours, big for Q4/wheat, live27 last |
| census (WINANATOMY1, BEATPROG1, TOPMECH1, TOPOPEN1, LOSSBODY1) | - | PFS's live wins = board draw or weaker rival; FQ wins with Q4 on the programme skeleton | the gap is the d0-14 body |

## 2. The invariants (S/brainstorm1/invariants.md)
1. **The invariant this review changed: TWO KINDS OF CURVES.**
   - *Non-recovering pies:* MELON (only the town centre drains it, 1/day), FERTILIZER (never drains), WOOL without a YARN_STORE (1/day). Their totals are fixed: melon ~32k at today's 171 units, fertilizer ~25k, wool ~8k. Order of sale splits them.
   - *Recovering curves:* wheat, strawberry, milk, tomato, carrot, egg drain through 2-5 shop types. On these, our volume is denial.
   - On the live main-42 ledger (7 W / 35 L vs programme rivals >= 2,450), the -8.1k final gap is fertilizer -5.2k + melon -4.3k + wool -4.2k + egg -1.0k. Milk, strawberry, carrot and tomato are within +-0.9k, and PFS wins d18-29 net by +5.9k.
   - **So the target is not "earn the d10-14 wave" (the whole-game melon split is 13.8k vs 18.1k). It is "sell first on the three pies without cutting the recovering-curve herd".**
2. d0 cash is exact (3,000; PFS has 201 left at dawn d1). Every d0 addition is a cut, and the cut compounds through the d5-9 herd purse: 640 coins diverted gave the rival +9.6k (COMBO1).
3. Capacity is capped: hands 11-14 cost 89-377 coins/day; the board is full from d12; the d15-29 cash has no use for either player.
4. Sale mechanics are closed. Tape reads are not evidence. The closed-loop rival earns 0.875x live and does not flood late.
5. **BT requirement.** At the top-10 line (theta 2,875) a body must score:

   | vs rival rated | 2,400 | 2,500 | 2,600 | 2,700 | 2,800 | 2,900 | 3,000 |
   |---|---|---|---|---|---|---|---|
   | expected score | 0.94 | 0.90 | 0.83 | 0.73 | 0.61 | 0.46 | 0.33 |

   That is ~0.80 against the MELON family at today's mix: 41-44 of the 51 band MELON seats. PFS has 14 there (0.27), and wins 0.17 live against programme rivals >= 2,450. Wins against stronger rivals move theta more, because the residual is 1 - sigma.
6. **Portfolio.** Two different bodies do not add (team = max of independently fitted thetas). A body fired on programme seats only (KERNEL2_FIRE_SWITCHES) dominates PFS iff it wins more programme games without touching V/ZERO. That is the free slot's bar.

## 3. Candidates, ranked (S/brainstorm1/candidates.md: 35 in families a-f)
| # | candidate | mechanism | evidence for | evidence against | bound | cost | first read |
|---|---|---|---|---|---|---|---|
| 1 | **PLATE-FIRST.** Melon plate on the STARTING tiles, funded by the carrot row + the goose (no d0 land; COW 4 + SHEEP 1 kept); SELL MELON at queue index 0 by d10 h8, before the programme's h9 first sale; later, the d10 melon cash rebuys herd | Melon is a non-recovering pie. The first 48-72 units at d10 take the top and push the programme's 52-unit wave and its 25.7 late melons down the sq curve | Gross melon-market margin (pie2, live d10 schedule): +7.5k at 48 melons (+4.2k if sold after the programme), +12.6k at 72 (+6.7k). ARB1 V2: +5.7k at 40 units, +13.6k at 78. At sd 8.5k, +12.6k alone would move P(win) vs the programme from 0.17 to ~0.70. B8 decomposition without its herd cut: own +2.7k, rival +2.0k. Realistic net +1..+5k, because the carrot row feeds the d2-4 strawberry slots (early strawberry volume is denial capital) | 2-3 h on PLATENOLAND1's switches + a d10 sale step | PLATENOLAND1 (running) reads the cascade; round 2 adds the first-mover step |
| 2 | **Early-wool race** (WOOL_FIRST: the programme's d0 herd 2C + 3S + 0G, wool sold as produced) | The early wool pie drains 1/day until a YARN_STORE is drawn; the programme's 3 d0 sheep sell 27.5 u at 202 in d5-9 and fund its reinvestment | pie: +20 early wool units = +3.6k own, -2.1k rival in d5-9; H2 ledger | Each h1 cow cut hands the rival +5..10k of milk (early milk is denial capital in the late glut); WOOLFIRST1 (tapes, 09-23) -3..-6 | -5..+2k | 0 h (switch in master) | **T3**: 80 g vs g0capsfix, own +1,170 (t 1.36), rival +2,081, margin -911 (t -0.65), W +4/-0; the wool race pays for the lost milk race |
| 3 | **Fertilizer race** (FERT_DUMP from d5, bonus 20) | Fertilizer never drains; each unit sold lowers every later unit 0.2 for both seats; the programme sells 140 by d14 vs our 91 | pie: +1.8k per 20 units sold earlier | FERTSALE1 (vs V56) <= 0; PFS's kept applications already beat the quote | +0.4..1.5k | 0 h | **T2 NONE**: 80 g vs g0capsfix, margin -46 (t -0.09), own -588 |
| 4 | **Underdog variance** (shop-draw bets on programme seats) | BT counts wins; mu -8.1k, sd 8.5k gives P 0.17; +4.8k sd = +10 points | RISKWIN1: wins by visible YARN count | option value, not variance, where the tilt is reactive | +5..10 pts P(win) | RISKWIN1 | running |
| 5 | **Closed-loop gene search** over plate tiles/day, h1 cows/sheep/geese, land day, fertilizer bar | The switches interact; no joint search was ever run on a reacting-rival fitness | ESFLAT1 optimised tapes, not the closed loop | seed noise sd 2-5k per 80 games | <= +3k | GPU1 lane or 2 CPU workers, 3 h | round 2 |
| 6 | P8d3 as the slot-2 fallback (plate on d3-4 after the herd) | the plate after the d0 herd | m40 own +3.2k, W +5/-0; big +7.0k | margin -1.4k; live27 -5.3k | ~0 | package 2 h | NONE (MELONSHIFT1) |
| 7 | Late tomato into the "under-supplied" curve (ENDGAME_TOMATO, 12 tiles) | live tomato drain 11.3/day > both seats' 8.1/day | ar2: 111 coins/tile-day | the flood rival's 49.5 tomatoes leave no headroom | measured -0.7k | 0 h | **T1 NONE**: 42 g vs flood, own -715 (t -2.34), our +20.8 tomatoes sell at 55 |
| 8 | Queue-index-first selling | lockstep: an earlier index books first | engine; NBINTEL6 | the programme sells lots of 3 hourly | <= 0.9k | 1 h | open (GAMETHEORY1 census) |

## 4. Round-1 reads (S/brainstorm1/res/)
- `ledger_an.txt`: the window x product ledger behind invariant 1. It also shows:
  - the programme's d5-9 reinvestment (11.5k spent vs 6.0k) is funded by early wool (+4.4k: 27.5 units at 202 from 3 d0 sheep) plus the 4.0k PFS leaves idle at dawn d10;
  - the wheat relay is a d5-9 cost.
- `pie.txt` / `pie2.txt`: melon, wool and fertilizer pies, from the exact engine price and drains.
  - Plate 48 sold before the programme's first sale: +7.5k melon margin with our late melons kept, +0.4k without them. The same plate sold on d11, after the programme: +4.2k. Plate 72: +12.6k / +6.7k.
  - Fertilizer: +20 / 40 / 60 units sold earlier give +1.8 / 3.5 / 5.1k (market only).
- `d10melon.txt`: 42 live replays, scanned per step.
  - The programme's first SELL MELON is at d10 h9 (median; min h6), queue index 0.
  - Units requested: 2.7 by h8, 18.6 by h12, 27.4 on d10, 41.1 by d11. That leaves a first-mover window of d10 h0-h8.
  - MELONDENY1 capped our reach at <= 20 units by h8, because hands spawn at the 4 shed-access tiles.
- `ar2.txt`: PFS's late crop value per tile-day is tomato 111, melon 92, carrot 55, strawberry 35, wheat 34. On fertilizer, PFS applies ~134 and sells 217; the programme applies ~99 and sells 328.
- `bt_req.txt`: the table in section 2.
- **T1** `bs1_tom12_fl` (ENDGAME_TOMATO, 12 tiles, vs flood, m40 80): NONE, stopped at 42/80: own -715 (t -2.34), margin -700 (t -1.89), 0 flips. Our +20.8 tomatoes in d18-29 bring only +1,149 (55/unit: the flood rival's 49.5 tomatoes leave no headroom). Displaced wheat, strawberry and melon cost -1.3k; the rival loses only -250 of tomato (res/salcmp_t1.txt)
- **T2** `bs1_fdump5_gcf` (FERT_DUMP from d5, bonus 20, vs g0capsfix, m40 80): NONE: 80 games, dmargin -46 (t -0.09), own -588 (t -1.95), rival -542 (t -1.49), flips +2/-1 (W 75->76). We sell +12.4 fertilizer units in d10-17 (+687) but lose -19.7 units of fertilized wheat (-713); the rival loses -470 of fertilizer (res/salcmp_t2.txt)
- **T3** `bs1_wool_gcf` (WOOL_FIRST: the programme's d0 herd 2C + 3S + 0G, wool sold as produced, vs g0capsfix, m40 80): 80 games: own +1,170 (t 1.36), rival +2,081 (t 1.89), margin -911 (t -0.65), W 75->79 (+4/-0). Our wool is +12.4 u / +2.4k in d0-9 and the rival loses -4.1k of wool over the game, but it gains +6.1k of milk and we lose -1.4k of eggs (res/salcmp_t3.txt). The wool race and the milk race offset, as invariant 1 predicts pie for pie. NONE on margin, but it is the only d0 reallocation so far that does not cost own coins, and it keeps the sheep that every plate cell drops.

## 5. Dialogue with the orchestrator (S/brainstorm1/dialogue.md)
- **H1** two kinds of curves: ACCEPT. Plate must remove late melons: REFUTE; the pie says keep them, and move only the surplus tile-days.
- **H2** funding: WOOL + zero idle cash; the relay is a cost.
- **H3** dairy: REFUTE by arithmetic (margin -1..+1k, own -4..-6k), matching MILKSHOP1 and HERD1 c4.
- **H4** seat order: REFUTE (lockstep, same quote for both seats); the queue index is worth +-0.9k. The only real first-mover window is the d10 melon wave (h0-h8).
- **H5** requirement stated as above.
- **H6** a/b/c/e REFUTE (PROGRAMME1; H3; H4; round trip nets 0). (d) the late curve with headroom is tomato (T1).
- **H7**: ACCEPT, with the price corrected: the d0 quadrant costs 1,000, not 2,000. It is ranked #1 as PLATE-FIRST.
- **H8** (COMBO1 NONE; PLATENOLAND1 drops the sheep): ACCEPT both invariants. H2 dominates H3: 640 d0-9 herd coins hand the rival +4.6k / +7.3k / +8.7k (P8d3 / PLATENOLAND1 / COMBO1), about 7-14x, while a d10+ cow nets <= 1x. T3 tested H2's funding source (the early wool) directly.

## 6. Round 2 design
**Goal.** Close the funding cascade that eats the melon first-mover gain. That gain is the only mechanism whose gross bound (+12.6k at 72 melons) reaches the top-20/top-10 requirement: +15.9k of mean shift for a 0.82 win rate at sd 8.5k.

**R2.0 (the cell the round-1 reads point to): PROG-D0 + MELON_RUSH** = WOOL_FIRST's d0 lock (2 cows + 3 sheep served first, no goose) + a 5-6 tile melon plate on the shed-adjacent carrot row (carrot seeds dropped) + no land before d5 + the d10 MELON_RUSH sale below.
- This is the programme's own d0 (at d1: 6.6 melon tiles, 2.1 cows, 2.9 sheep). It fits PFS's ~2,600 h1 budget: 2,300 herd + 400-480 seed.
- T3 shows the lock alone is own +1.2k / W +4/-0 / margin -0.9k: the wool race pays for the milk race.
- PLATENOLAND1 shows that without a lock the planner drops the sheep under a plate (rival +7.3k).

**R2.1 PLATE-FIRST v2.** 3 h build + 1.5 h judge, built in a worktree on PLATENOLAND1's switches.
- (a) The plate sits on the NW tiles within 3 steps of the shed-access tile (4,4): 10 tiles with x+y >= 5.
- (b) It is funded by the carrot row + the goose only. COW 4 + SHEEP 1 stay locked, as do the h0 pump and 9-11 feed wheat, with no land before d5.
- (c) A default-off MELON_RUSH step on the first ripe day: hire at h0, harvest the ripe plate tiles h1-h5, DROP, then SELL MELON at queue index 0 by h8. The programme's first melon SELL is at d10 h9 (median; min h6), and it has requested 2.7 units by h8.
- (d) The d10-11 melon cash rebuys cows/sheep, restoring d18-29 denial volume.
- Fire it on programme seats only (KERNEL2_FIRE_SWITCHES).
- Judge:
  - g0capsfix m40 80, margin;
  - big + flood, own coins;
  - live27 closed loop;
  - the fired live27 tapes, which give the exact melon denial on the programme's recorded wave (ARB1 V2 method).
- Stop rule: dmargin <= 0 on g0capsfix OR on live27 -> the plate family closes.
- If it passes, it becomes the slot-2 package (MELONTRIAL1 route, 2 h) by 09-30 12:00Z.

**R2.2 data before the build (30 min, 1 local worker).** A d10 trace of one control game gives:
- the hour each PFS unit can reach each plate tile;
- the number of melons that can be in the shed by h8 (MELONDENY1 measured <= 20 against V at h8; the programme leaves until h9-h12).

This sizes the plate: 36 / 48 / 72 melons.

**R2.3 closed-loop gene search** (in parallel, only if the GPU1 closed-loop lane is offered). CMA over about 8 scalars:
- plate tiles and plate day;
- H1 cows / sheep / geese;
- LAND day;
- FERT bar;
- tomato tiles.

Fitness = g0capsfix m40 margin + 0.5 x flood own coins, 80 games per evaluation, 3 h.

**Engine timing for MELON_RUSH (kaggriculture.py `interpreter`).**
- Unit actions (move / HARVEST / DROP) resolve BEFORE `_process_market` in the same step, so melons DROPped at step t can be SOLD at step t.
- The farmer starts every day on the NW access tile (4,4) and acts from h0. Hands hired at h0 spawn on the access tiles when the market resolves and act from h1.
- 9 NW tiles lie within 3 moves of (4,4): (3,4) and (4,3) at 1 move; (2,4), (3,3), (4,2) at 2; (1,4), (2,3), (3,2), (4,1) at 3.
- The farmer + 4 hands can each harvest 2 plate tiles and DROP by about h7-h8: 8 tiles x 5-6 = 40-48 melons in the shed, sold at queue index 0 by h8. The programme's median first sale is h9, and it requests 2.7 units by h8.
- MELONDENY1's <= 20-unit reach came from the default plate placement, not from a shed-adjacent plate.
- Fertilize the plate: melon yield accrues only on waterings at ages 6-12, +1 each or +2 when fertilized, capped at 6. An unfertilized tile harvested at d10 holds 4-5 units. Two applications (d6, d9) reach 6 per tile: about +1.5 melons x ~250 against ~170 of fertilizer per tile. (MELONLOGIC1: the programme uses no fertilizer in d0-9.)
- R2.2 also records when the g0capsfix clone rival first sells melon on d10, from one per-step closed-loop trace. The judge can only see a first-mover gain if the clone keeps the programme's h9 timing; if it sells earlier, the fired live27 tapes are the melon-denial judge.

## Round 2 (08:22-08:50Z): PLATE-FIRST, predicted by component, stopped at the state log

**Verdict: NOT YET.** PLATE-FIRST is closed at its base. The stop rule fired before any new code was written.

### Component prediction vs measurement (S/brainstorm1/prediction_r2.md, written before any code)
All margins are vs PFS, on g0capsfix closed loop unless marked.

| step | body | predicted | measured |
|---|---|---|---|
| 0 | c2p8 (REALLOC1): 2 cows + plate 8 | -14.5k | -14.5k (80 g) |
| 1 | 6 tiles instead of 8 | -11.9k | -11.9k (c2p6, 80 g) |
| 2 | + 3-sheep lock, goose dropped, no land before d6 (= PLATENOLAND1's x_wf8 set) | **-3.9..-1.3k** | **-14.8k** (6 g, t -3.77; own +1.0k, rival +15.7k). Faithful live27 tapes: -14.6k, W 3->1 (13 seats, PLATENOLAND1) |
| 3 | + plate fertilizer d6 | +0.6k | not built |
| 4 | + MELON_RUSH (sell first by d10 h4-h7) | +0..+2.8k (GAMETHEORY1 melonorder: 36 vs a 52 wave = +1.4k each way) | not built |

**The component that failed is step 2, the funding.**
- The sheep swap was worth +10.6k in T3 vs c2p0 (idle cash). Under a plate it is worth about -2.9k: the lock and the plate empty the d2-9 purse (dawn d2 33 vs 127; d5 684 vs 1,389).
- At d9 the herd is 2-3 cows / 2 sheep (one of the 3 sheep lost) / 0-1 geese, vs 6.4 / 3.3 / 1.6 in the control. Our wheat is -70 units and d10-17 strawberry -10.
- The rival gains in every book it takes back: wheat +3.3k, strawberry +4.3k, milk +4.7k, carrot +1.6k, eggs +1.4k, wool +1.2k.
- The plate itself works: +28 melons in d10-17 (+6.8k), late melon -4.8k. Steps 3-4 can add at most +3.4k, so they cannot close -14.8k.

### State log (condition 2), x_wf8 base, 3 boards x 2 seats
- OFF identity of the bs1 tree: 6/6 exact vs JUDGERIVAL1's pfs.csv. The tree is worktree kagg3_wt_brainstorm1, branch brainstorm1_0929 = 8d670dad + MELON_SHIFT + LAND_DAY + PLATE_NO_LAND_BEFORE, cherry-picked from 14d155ef / a5489c73 / bf4191f2.
- d0 h1: WHEAT 11 + CARROT 3 + MELON 6 + COW 2 + SHEEP 3, then COW 1 on d1. Dawn cash d1 433, d2 33.
- 6 plate tiles from d1. BUY_LAND on d6 and d11-12.
- **NO-GO** on "a sheep dropped" (3 -> 2 by d9) and on the d5-9 herd collapse.

### WOOL_FIRST (T3) reads for the free slot (Q3)
| read | n | W | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|
| m40 closed loop vs g0capsfix | 80 | 75 -> 79 (+4/-0) | +1,170 (1.36) | +2,081 (1.89) | -911 (-0.65) |
| live27 closed loop vs g0capsfix | 27 | 27 -> 27 | +308 (0.24) | +3,559 (2.26) | -3,250 (-1.63) |
| live27 fired tapes, JC1-faithful both | 12 | 3 -> 2 (+0/-1) | +3,005 (1.78) | +2,326 (1.25) | +679 (0.49) |
| live27 fired tapes, all | 18 | 4 -> 6 (+4/-2) | +13,008 | -12,903 | +25,911 (6 broken istinetz/thisray tapes) |

- Herd at d9: 5.7 / 4.7 / 0.8 vs 6.4 / 3.3 / 1.6. At d14: 7.0 / 8.3 / 3.1 vs 7.5 / 8.3 / 3.4.
- The h1 fire on the 18 tapes is the designed state (COW 2 + SHEEP 3).
- **The free-slot bar is not met.** Flips are positive only on m40; the faithful tapes are -1, and live27 closed loop is -3.3k.

### W4C2S (round-3 seed, named before running): the wool race without losing the milk race
WOOL_FIRST with COWS=4, SHEEP=2, GEESE=0: the 4 h1 cows kept, the goose swapped for a 2nd sheep. It costs 2,600 at h1, which fits PFS's ~2,870 h1 purse.
- **Result: NONE (named and run, stopped early).**
  - m40, 20 g vs g0capsfix: own -5,026 (t -2.99), rival +16,761 (t 8.76), margin -21,787 (t -9.77), flips 0/-6.
  - live27 seat-0 half, 13 g: margin -18,190 (t -5.43), flips 0/-5. The l27b half was killed by pid.
- **State:** h1 = COW 4 + SHEEP 2 + WHEAT 11 + CARROT 8 leaves 13 coins at dawn d1 and d2. By d9 the herd is 4 cows / 0 sheep / 0.1 geese (unfed escapes; no d5-9 buys; control 6.4 / 3.3 / 1.6).
- Our wool is -41 units and eggs -66 units; the rival's late wool is +7.0k, milk +5.7k, fertilizer +3.0k.
- **This is the new invariant: PFS's d0 purse has ZERO slack.** Its 201-coin dawn-d1 remainder is the feed/placement reserve that keeps the h1 herd alive, and its d2-9 income is what grows the herd to 6/3/2 by d9.
- Every cell that takes d0-4 coins has now lost 10-22k on both judges: plate, sheep swap, cow cut, goose-for-sheep (B4, B8, c2p0..c4p8, COMBO1, P8d3, N8_9_d5, x_wf8, W4C2S). Only T3's exact swap (2C+3S, 100 coins freed) is own-positive.

### Dialogue answers
- **Q1 (dairy from idle cash).** It is pasture and labour, plus our own milk price; feed is not the cost.
  - GAMETHEORY1 measured it: HERD_MATCH M1 from d10 = own -0.8k / margin +0.1k (80 g); live27 own -2.3k / margin -1.2k.
  - The rival's milk denial is real (-1.2..-1.7k, ~160 per unit), but the cows take crop tiles and hands (our strawberry -0.5..-1.2k, tomato -0.3..-0.6k) and cannibalize our milk (-0.8k on +12 units).
  - My -4..-6k (4 cows) was the same arithmetic at double the dose.
- **Q2 (fertilizer -5.2k).** It is volume, not order; net of the programme's buy-back it is -2.3k (res/fert_net.txt).
  - PFS nets 11.2k vs the programme's 13.5k; the programme buys 72.5 units back for ~3.0k.
  - Both sell at the same per-window prices (96/86/68/51/26 vs 96/84/67/51/24).
  - The gap is +42 units collected (~10 % more animal-days).
  - No order lever is left. T2 (FERT_DUMP from d5) sold +12.4 units earlier, but they came out of fertilized wheat: margin -46 on 80 g.
- **Q3 (WOOL_FIRST).** See the table above: live27 W 27 -> 27 closed loop and 3 -> 2 on faithful tapes; dours +0.3k / +3.0k. It does not meet the free-slot bar.

### Round 3 design
1. **Close the d0 family.** Nine bodies on two judges show the zero-slack invariant. Nothing that spends a d0-4 coin differently can be judged positive by 09-30, and the melon first-mover (<= +2.8k) cannot pay its funding (>= 10k).
2. **Round 3 = the one lever that touches neither the d0 purse nor our late volume: CLOSE-GAME DENIAL from d24** (RISKWIN1's named next cell).
   - Trigger: when |cash margin| < 5k at dawn d24, all shops are known and the game is near-deterministic.
   - Action: on the first lot of each day, put our late stock of the rival's two largest late products (strawberry, milk) at queue index 0.
   - Bound: 8 of the main 42 games are within 5k at d24 (5 of them wins), so <= 3 flips / 42 = +7 points of P(win) vs the programme at ~0 own cost elsewhere.
   - Build 1.5 h as a default-off switch in kagg3_wt_brainstorm1. Judge on the faithful live27 tapes (their d24 states are the real programme's) and the closed-loop games with |margin| < 5k at d24.
   - Stop if flips <= 0 on faithful tapes.
3. Free-slot rule until then: nothing built beats PFS on the programme seats in both reads (WOOL_FIRST 0 on live27 closed loop / -1 on faithful tapes). FINALPLAN1's second-PFS option stands.

## Round 3 (08:55-09:10Z): close-game denial not built (nothing to move); max-of-two priced; the programme's d0 sequence decoded; H2 closed

**Verdict: NOT YET.**
- None of the three lines produces a body that beats PFS on programme seats.
- The free-slot question reduces to max-of-two: any second body at least as strong as PFS adds ~+0.56 sigma, i.e. +10..+14 rating points at ~500 October games.

### Line 1: close-game denial, stopped at the state check (S/brainstorm1/res/hourscan.txt)
Main-42 live replays, d18-28, per hour:
- PFS already sells its late strawberry / milk / wool in one lot at **h17**: 7.2 / 6.4 / 6.1 units a day.
  - h17 is the post-tick peak: quote 77 / 76 / 102, vs 65-70 before the tick.
  - The dawn (h1) lot carries 5.9 / 0.5 / 1.1 units.
- `EARLY_SELL_ON` and `SELL_SLOT_PRIORITY_ON` (+ `SELLS_FIRST`) are already shipped ON. Lot 1 rides the h1 BUY row with sells first, in coin-at-risk order.
- The programme sells small lots at every tick hour (h1 / h9 / h13 / h21). At h17 it sells only 1.1 / 1.2 / 0.7 units.
- So "queue index 0 on the first lot" has at most ~20 coins a day to move (7 of our units ahead of 1 of its units, at the 1.92 / 2.1 coins-per-unit slope).
- Tomato is the one book where HOLDING pays us (ARB1: +1.0k us / +0.2k rival, t 1.1).
- **NOT BUILT, NONE by mechanism.** State log = 0 units to move.

### Line 2: two copies of PFS (S/brainstorm1/res/btnoise.txt)
- **Per-submission BT theta MLE** (opponents fixed at their pre-game rating; LIVEWATCH23 game lists):

  | sub | games | theta | se |
  |---|---|---|---|
  | vrp20_pfsoff | 82 | 2,468 | 45 |
  | vrp19w_k2wide | 78 | 2,601 | 61 |
  | vrp18 | 48 | 2,557 | 71 |
  | vrp17 | 88 | 2,537 | 49 |
  | vrp15 | 84 | 2,571 | 44 |
  | vrp12 (FINALSLOT1) | 93 | 2,605 | 41 |

  - Scaled by sqrt(n), se = 17-24 at ~500 October games (FINALSLOT1's rate law), 31-44 at 150 games, 45-60 at ~75.
  - The three PFS-bodied subs (vrp20 / vrp18 / vrp12) spread 2,468-2,605. That is within their se, plus field drift.
- **Max-of-two gain.** Team = max of two independently fitted thetas.
  - Two copies of one body with per-fit noise sigma give E[max] - mu = sigma / sqrt(pi) = **0.564 sigma = +10..+14 rating points** at ~500 games (+26..+34 if only ~75 October games).
  - This is BOLDSLOT1's 3.4-rank option at 510 games, now in rating points.
- **Rules.** The Kaggle rules page is behind JS (not readable).
  - FORUM_RESEARCH [OFFICIAL] #732931: only the latest 2 submissions are active; the final BT uses episodes where both agents are active; 5 uploads/day.
  - Byte-identical resubmissions are reported by competitors (#734000, #736127) with no sanction.
  - Nothing found forbids a duplicate.
- **What the bold slot must beat.** For equal sigma, E[max(PFS, X)] > E[max(PFS, PFS')] iff mu_X > mu_PFS.
  - So a programme-seat specialist must add live programme-seat wins without losing V/ZERO wins. Nothing built does so on both reads.
  - Live now: vrp19w (the wide fire list) sits at +133 +- 76 theta over vrp20 on its own games (1.75 se, different opponent mixes). FIRELIVE1's counterfactual says its fire lost 3 wins on the 18 fired games. The θ gap is not evidence of a better body until a paired read on common opponents agrees.

### Line 3: where the programme's cash path leaves ours (S/brainstorm1/res/diverge.txt)
Exact per-day ledgers, 6 live27 seats.
- The x_wf8 emulation (2 cows + 3 sheep + 6 melons, our planner) was played through the real engine against the recorded programme tape, replay kept. It was compared with the programme on the tape (= the live programme to within ~1 % through d9) and with PFS live on the same boards.

| d0-9 | x_wf8 | programme | PFS live |
|---|---|---|---|
| revenue | 9.8k | 18.5k | 14.4k |
| fertilizer | 2.7k | 6.3k | 4.0k |
| wool | 1.6k | 5.7k | 1.2k |
| wheat | 2.7k | 3.9k | 2.8k |
| milk | 2.4k | 2.5k | 4.5k |
| spend: animals / feed+relay / land / hires | 3.4 / 2.1 / 1.0 / 0.04k | 7.5 / 5.7 / 3.0 / 0.44k | 4.6 / 2.5 / 1.0 / 0.07k |
| animals standing d1 -> d9 | 4.2 -> 5.7 | 5.0 -> 16.0 | 6.0 -> 10.8 |

- **Divergence day 0, hour 1: our purse.**
  - Our h1 row is SELL WHEAT 48, seeds 650 (MELON 6 = 480), COW 2, SHEEP 3.
  - The row executes in queue order, so after the seeds and the 2 cows we hold 426 coins and **the 3rd sheep bounces** (animal spend 1,800 vs the programme's 2,283).
- **Days 1-3: feed.**
  - The programme buys 21 / 25 / 49 feed wheat on d0-2 and feeds 3.0-6.3 units a day, i.e. every animal. It pays for this with its d2 wheat sales (1.5k).
  - We feed 3.3 / 1.3 / 3.3 units for 4.2-4.7 animals. 0.7 cow and 0.7 sheep escape by d3.
- From there the programme's fertilizer (1 unit per animal per day, sold from d0) and wool (16.8 units at d6 from 3 fed-and-cared sheep) compound.
  - It reinvests daily: animals 5 -> 16, land 3.0k by d9, hires to 10.
- **Micro, and scriptable:** yes for the order (x_wf5 = 5-tile shift: all 3 sheep land; own +2.1k vs x_wf8), and yes for the feed floor.
- **But it does not close the margin.**
  - x_wf5, 6 g vs g0capsfix: own +3,069 (t 1.51), rival +13,936, dmargin -10,867 (t -6.03).
  - The rival's gain is our 2-cow d0: our milk -44 units, rival milk +7.5k. Plus carrot +3.2k, strawberry +3.0k.
- **H2 CLOSED.**
  - The programme's d0-9 lead is income we can generate only with its herd sequence (2 cows + 3 sheep, fed).
  - On the shared book, that sequence hands a rival holding the milk race +10-14k.
  - PFS's 4 h1 cows are exactly the denial the sequence gives up.

### Round 4 design
1. **Stop the body search for this deadline.** Every closed family is listed in invariants.md A-E: d0 (zero slack; H2 closed on the exact ledger), d10+ capacity, sale mechanics, the close game, the fire lists.
2. **The one remaining lever is the slot decision.**
   - Refresh LIVEWATCH23 for vrp19w and vrp20 (read-only ListEpisodes) and fit theta on their COMMON opponents (paired by opponent sub).
   - Apply the max-of-two rule: keep vrp19w if its paired theta >= vrp20's; otherwise re-upload the vrp20 package as the second slot by 09-30 21:00Z (the upload is the user's call).
   - Expected value of the PFS copy is +0.564 sigma, about +10..+14 points. That is a requirement, not a rank forecast.

## Session summary (written by the orchestrator, 2026-09-29 09:22Z; session closed after round 3 + a stopped round 4 under the user's 3-round rule)

**Requirement (not a forecast).** A top-10 body needs ~0.82 vs rivals rated 2,400-2,800 (~+15.9k mean margin at sd 8.5k). PFS: 0.60 at 2,400-2,600, 0.17 vs the programme (>= 2,450), 10-11 vs V rivals at 2,340-2,520 (parity games, 7 of 11 losses within 3.3k).

**Invariants established.**
1. Melon, fertilizer and wool (without a YARN_STORE) never recover inside a game: their coins go to whoever sells first. Live gap -8.1k = fertilizer -5.2k (volume: their ~10 % more animal-days), melon -4.3k, wool -4.2k, egg -1.0k; milk/strawberry/carrot/tomato within +-0.9k.
2. PFS's d0 purse has ZERO slack: the 201 coins at dawn d1 are the feed reserve; nine bodies that spend a d0-4 coin differently lose 10-22k. The d0 family (plates, herd mixes, land timing) is closed for the deadline.
3. Our late herd/crop volume is our only denial tool; every lever that shrinks it hands the programme +5-19k in late prices.
4. The seats couple only through the 9 market books; a buy/sell round trip moves the rival's fill prices by exactly 0; seat order gives no edge; the shop draw is hidden-seeded (blind).
5. PFS already sells late strawberry/milk/wool at h17 right after the shop drain at the day's best price (EARLY_SELL on): sale timing has nothing left to move.
6. The programme's d0-9 lead is fertilizer +3.6k and wool +4.1k, both from ANIMAL COUNT: it buys 21/25/49 feed wheat on d0-2, feeds everything, and reinvests daily from 5 to 16 animals by d9; PFS grows 6 -> 11 and buys ~4.8 sheep in one lump on d10 from cash left idle. With the programme's 2-cow start our body loses the milk race (-7.5k), so H2 is closed for that start only.

**Tested this session.** WOOL_FIRST: m40 own +1.2k, W +4/-0, margin -0.9k; live27 tapes W 3->2 (free-slot bar not met). FERT_DUMP d5 NONE. Late tomato hold NONE. PLATE-FIRST base -14.8k (stopped by rule). W4C2S -21.8k. Close-game denial not built (nothing to move). Dairy from idle cash flat (GAMETHEORY1 80 g +0.1k).

**Round-4 partial reads (stopped 09:20Z).** Feed audit on the main-42 live replays: PFS never lets an animal go 2 consecutive unfed days; unfed-that-day counts d0 4.0 (placement), d2 3.6 (dawn cash 110, shed wheat 0), d6 2.2, else <= 1; escapes 3 in 42 games (d7) vs the programme's 1. Slot fit: vrp19w 149 g 96-53 theta 2,485 +- 33, vrp20 156 g 91-65 theta 2,463 +- 30 on all games; on 49 COMMON opponents vrp19w 2,424 +- 45 vs vrp20 2,487 +- 45 = -63 +- 64 (by opponent sub, 47: -40 +- 69): vrp19w is not better than PFS where they meet the same rivals.

**Slot arithmetic.** Two copies of PFS = +10..+14 expected rating points from max-of-two noise (SE 17-24 at ~500 October games); nothing in the rules forbids a duplicate; a bold body earns its slot only if its own mean rating >= PFS's. The upload decision is the user's.

**Open line handed to BRAINSTORM2.** PFS's own d0 mix (untouched) + the programme's d1-9 policy: feed everything first (d2 and d6 are the unfed days), and buy the animals PFS purchases on d10 anyway as early as daily cash allows (sheep first), so late volume is never smaller than the control's. Files: S/brainstorm1/{arms.md, invariants.md, candidates.md, dialogue.md, round2.md, res/}.
