# GAPREVIEW1-A (2026-09-27, 11:44Z-12:05Z): every arm we ran, and the decisions no paired verdict covers

Read-only review, blind to the B review. Sources: `docs/strategy/BUILD-STORY.md` (all 3,296 lines), the 09-20..09-27 dated docs
that BUILD-STORY does not index (astra*, actionrl9-12, empty1, idle1, morework1, q4root1, q4teams1, liveloss14, crewaudit1),
`2026-09-26-ideas1.md`, `2026-09-11-lever-ranking.md` + `2026-09-10-consensus.md` (pre-FT2 switch census), the `plan.py`
switch list (32 ON / ~95 OFF), `S/livesweep/results.tsv`, `src/kagg3/spec.py`, `src/kagg3/core/ops.py` and the engine
(`kaggriculture.py`). No games were run.

Files:
- `S/gapreview1/A_ledger.tsv` — 335 arm rows (axis, arm, date, mechanism, verdict, key number, doc). Rows per axis: RL/ES 61,
  infra/judge 51, crop mix 38, routing 34, selling/price 32, opponent-conditioned 29, herd/feed/care 28, crew/hires 22,
  opening 18, land 12, endgame 10. Pre-09-16 screens are folded into group rows that cite the 09-10 consensus.
- `S/gapreview1/A_decisions.tsv` — the 34-row decision map below, with the covering arms per decision.

## 1. The decision space and what covers it

The engine gives each unit one op per turn (move, PLANT, WATER, HARVEST, FERTILIZE, DIG, BUILD_COOP/PASTURE, FEED, CARE,
COLLECT_FERTILIZER, PICKUP, DROP, PLACE) and each seat 10 market orders per turn (HIRE, BUY_LAND, BUY_SEED, BUY_ANIMAL,
BUY_PRODUCT for wheat/fertilizer only, SELL n units). There is one sale channel, the shared market; shops only drain it.
There is no animal sale. Hands reset every night.

| # | decision | status | covering arms (paired verdicts) |
|---|---|---|---|
| D1 | day of Q2/Q3 purchase | **PARTIAL** | only EARLIER was judged under the current body (Q3_EARLY −9, BOEY_Q2_DAY=6 −36, NONV1 Q9 0); later/never only by the 09-10 land-veto arms (pre-FT2, tapes) |
| D2 | Q4 | COVERED | MMPQ, PLANTASK1, Q4PROG1, Q4VRP1 (12 cells), Q4RELAY1, RELAY12, Q4LIMIT1, Q4FIX1, Q4DIG1 |
| D3 | crop per tile/day | COVERED, **tomato swap PARTIAL** | CROP_SCARCE, TURNCOST, CONTEST1, WHEATMIX1, ENGMIX1, CARROTFLAT/BID, PLANAUDIT1; tomato only as a fill (TOMATOFILL1) or a 20-board ES slope (ESNEW1) |
| D4 | planting volume (the ask) | COVERED | PLANT_FILL_LATE, PLANTASK1, WHEATLATE1, RELAYFILL1, CREWRELAY1, GAPFIX1, ENDWAVE1, FILLWORK1, ROUTEFILL1; SLIVER and ESWORK relay shipped |
| D5 | planting day / horizon | COVERED | PLANTTIMING (ceiling 0), LATEPLANT1 |
| D6 | d0 opening | COVERED | MELON_OPEN, MELONGENES1, MELONVRP1, MELONDENY1, MIRROROPEN, BOEY2, OPENPKG1; M20z shipped |
| D7-D9 | water, fertilize, harvest timing | COVERED | DRYDEATH1, WATERAUDIT; FERT_TIMING shipped, WHEATCYCLE1; CARETIMING/HARVEST ceiling 0 |
| D10 | dig / replant spent tiles, weeds | COVERED | LATE_EXEC shipped, EXPIRY1, NOOPAUDIT, IDLETILE1 |
| D11 | seed buys | COVERED | DSMSEED1 (seed price is a constant), PRESTOCK seeds |
| D12 | herd size, species, buy day | COVERED | HERDRAMP, HERDVRP1, SHEEPFIRST1, WOOLFIRST1, NONV4, GEESE1, EGGDOSE1, EGGS2, ENGHERD1, HERD_CAP_SHEEP |
| D13 | pen / crop spatial layout | **PARTIAL** | COMPACT_SOFT and ROUTE_EFF (pre-FT2), TILEALLOC; never an arm in the VRP era |
| D14 | placement day/hour | COVERED | MIDDAY_PLACE/V2 (LIVESWEEP −5), ANIMAL_SAME_DAY 0 |
| D15 | **feed + care on the placement night** | **UNCOVERED** | none; CREWAUDIT1 found it 09-27 |
| D16-D17 | feed and care on later nights | COVERED | FEEDKEEP1, FEEDNIGHT1, FEEDROOM1/2, CLIPCENSUS1; CARE_FILL and CARE_RIDE shipped, CARE_FED, NONV_WOOL_CARE |
| D18 | collection cadence (animal products, fertilizer) | **UNCOVERED** (small) | YIELD1 observation only |
| D19 | hires per day | COVERED | JOINTLIFT, CREW-PUSH, FWDHIRE, KNOBVRP1, HIRELEVEL1, LABOUR1; EMPTY_ROUTE_UNHIRE shipped |
| D20 | early crew d0-9 | **PARTIAL** | EARLYRAMP −10.3k (pre-VRP, tapes); under VRP the NONV1/OPENPKG1 floors were trimmed, so the dose never ran |
| D21-D22 | routing, dawn/dusk, shed logistics | COVERED | ROUTE_* family, PLANNER3, ROUTENN1-3, ROUTEOPT1 + ROUTERJIT1 shipped, RRDEEP2, RLROUTER1; DAWN0, WIDE_PICK(+FREE) shipped, CREW24, OVERFLOW_GUARD V1-3 shipped. MARKET_PACK / ROUTE_EARLY / PRESTOCK_ON are VOID (crash, −109 on LIVESWEEP) |
| D23 | sell turn inside the day | COVERED, **turn-0 lot PARTIAL** | LOT4 shipped, LOT5, SELLRACE, V15_DODGE, CHURNPRICE1, LOTDEPTH, DRIPSELL1; A0 (lot 1 behind turn-0 hires) read level on 09-11, pre-FT2, tapes only |
| D24-D25 | sell day, lot size / split / order | COVERED | SELLDAY, SELLPROJ, SELL_SPREAD, SELLAUDIT1; SPREAD6, SLIP1, SELL_SLOT_PRIORITY shipped, SLOTLOCK |
| D26-D27 | wheat/fert buys, fert apply vs sell | COVERED | OPEN_PUMP shipped, RESALE1, FERTSALE1, TRADER, FERTDENY, FERT_RESERVE, FERTDENIAL |
| D28 | end-of-game liquidation | COVERED | ENDROUTE family shipped, ENDSELL, ENDGAME1, ENDWAVE1 |
| D29-D30 | opponent- and town-conditioned play | COVERED | RIVAL_TELL, PLANSELECT, MELONREACT, ENGGATE1, NONV1-4, M20z, MELONCOUNTER2, NVTSHIP1, V15LOSS1, BOEY1; TOWNADAPT (6 arms) |
| D31 | steering the shop draw with our own empty tiles | CLOSED BY LAW | the seed is a hidden 31-bit int, cleared from the configuration (`resolve_episode_seed`); MPCFEAS |
| D32-D34 | clock, seat, learned layer | COVERED | VRPDEADLINE1, ROUTERJIT1; SEATFLIP1; 60+ ES/PPO runs |

## 2. The gap list (strict: no paired verdict exists)

**G1. Placement-night FEED+CARE (D15) — UNCOVERED.**
- (a) Never proposed until CREWAUDIT1 (09-27). The planner models a new animal as "placed today and hungry on day+1"
  (`plan.py:10441`); the feed/care plan is built from dawn's tiles, so today's placements never enter it. FEEDNIGHT1 traced only
  production nights; CARE_FILL/CARE_RIDE act on dawn animals.
- (b) 17.5 of 17.5 placements a game skip the night (rival 34 %), in all 16 games. The first production pays 1 + pending bonus, so
  each sheep/goose loses 1 unit (john: 14 sheep placed d6-11 at wool 229-239). One-sided +1.6k gross / +1.3k net a game
  [2026-09-27-crewaudit1.md]. Discount for the two-purse rule: our extra wool lowers our own later quote, so expect +0.4..0.8k.
  The rival's purse should fall (added volume on a shared book), so the gift risk is low.
- (c) `PLACEFEED_ON`: same-day FEED+CARE for a sheep or goose placed today when the first-production quote beats wheat (the
  placing unit carries 1 wheat). Paired vs the master (vrp10_esw) config on dev100, held100, VLOSSBED100, FRESH300, tapes dev50,
  faithful-59 and the 16 NEARMISS1 seats. Expected Δours +300..+800, Δtheirs ≤ 0, +1..+3 flips per 300.
- (d) Rank 1. It is the only open item with a measured premise in both wins and losses, and it waits on user approval.

**G2. Q2/Q3 later or never (D1) — PARTIAL.**
- (a) Under the current body only earlier dates were judged. The later/never direction was last judged by the 09-10 land-veto
  arms (3 arms DEAD), pre-FT2 against open-loop tapes, and the ES land gene never resolved anything.
- (b) Q3_EARLY moved Q3 from d10.0 to d7.9: own purse +912 (t 2.32) but the rival +4,315 (t 6.52), because the 2,000 came out of
  the herd purse [2026-09-26-wheatmix1.md]. The mirror (later Q3 leaves d9-11 herd money) is untested. We out-earn the ENGINE
  on Q3 by 4.8k [2026-09-23-dsmland1.md], so a later Q3 also has a crop cost.
- (c) Grid Q3 day {ship, +1, +2, +3, never} × Q2 day {ship, +1} on dev 0-49 both seats vs V56 in the exact sim (10 cells, 1,000
  games), then held100/FRESH300 for survivors. Expected ±1-2 flips.
- (d) Rank 2.

**G3. Turn-0 dawn lot vs the reacting V seat (D23) — PARTIAL.**
- (a) Mode A0 (lot 1 behind turn 0's hires, in free slots) read level on 09-11: +432 / −9 / −119, |t| ≤ 2.1, pre-FT2 and on
  tapes only. It is refused while OPEN_PUMP_ON is live, and the pump ships ON. SELLRACE then called hours 0-1 "unreachable" by
  layout, not by engine law.
- (b) Rivals place 23.7 % of their units in hours 0-1 [2026-09-17-sellrace.md]. A 3-turn leapfrog cost us −301/board when
  v15stack did it to us [2026-09-23-v15loss1.md]. Against that, our sale turns already land on 95-99.7 % of the day's max quote
  [2026-09-26-churnprice1.md], and SELLRACE's reachable-hour ceiling was −308.
- (c) Allow A0 on d1-29 only (the pump uses d0), then paired dev100 + held100 vs V56 (400 games). Expected ±300/board, 0..+1 flips.
- (d) Rank 3.

**G4. Tomato share swap on d2-12 (D3) — PARTIAL.**
- (a) Tomato was judged only as a fill on the router's slack (TOMATOFILL1: displaced plantings, gift), as TOMATO15 (09-16, pre-FT2)
  and as a ±1σ slope on 20 boards (ESNEW1). A swap that keeps the ask and moves wheat/carrot tiles to tomato was never judged paired.
- (b) For: FARMAUDIT1 4.9 vs 18.8 tomato plantings on d0-19 (~5.7k); TOPLOSS1 +6.8k tomato edge; YIELD1 709 vs 315 plantings.
  Against: ESNEW1 d0-4 and d5-9 `pl_TOMATO` +1σ read own −554 / −510 with the rival +1,819 / +1,587; PLANAUDIT1's causal 3-day
  rebuild −8.5k; the standing gift law.
- (c) TOMATO crop-logit bonus k ∈ {0.5, 1, 2} on d2-12 with the ask fixed; dev 0-49 both seats vs V56 (300 games); kill if
  Δtheirs t ≥ 2. Expected ≤ 0.
- (d) Rank 4.

**G5. Collection cadence (D18) — UNCOVERED, small.**
- (a) Never proposed. YIELD1 saw that REAL lets product sit to `max_held` and collects less often, then closed yield.
- (b) The engine pays by production, not by op. Our idle hands cost only +34/g of hire bill [2026-09-27-crewaudit1.md], and
  bill savings convert at 0..−2 flips (RRDEEP2), so saved ops are worth little.
- (c) Census only (0 games): HARVEST-on-pen and COLLECT_FERTILIZER ops a game from the CREWAUDIT1 replays, plus the cap-loss risk.
  Build only if ≥ 100 ops/game can be saved. Expected ≤ +100/g, 0 flips.
- (d) Rank 5.

**G6. Pen / crop layout (D13) — PARTIAL.** (a) Last judged pre-FT2 (COMPACT_SOFT −327, ROUTE_EFF −111). (b) Routes sit within
4.4 % of their own shortest tour (ROUTERAUDIT1) and the rival walks 41 % more (CREWAUDIT1). (c) Census of pen distance against
visit frequency (0 games). Expected < +100/g. (d) Rank 6.

**G7. Early crew d0-9 under VRP (D20) — PARTIAL.** (a) EARLYRAMP ran the dose pre-VRP on tapes; under VRP no arm executed it.
(b) EARLYRAMP −10,278 with the rival +7,664; the d0-9 purse is spent to the coin (ENGPLATE1). Top teams fund 6.6-6.8 hands from
a d0 program that OPENPKG1/BOEY2 closed. (c) No probe recommended; the prior is about 0. (d) Rank 7.

**G8. MARKET_PACK / ROUTE_EARLY / PRESTOCK_ON (D22) — VOID.** (a) All three crash the seat (−109 wins on LIVESWEEP; the
lever-ranking P3 "3,000-coin signature"), so none was ever judged working. (b) DAWN0/H1WAIT: the h1 wait is structural, with
+165 reachable, and WIDE_PICK(+FREE) already took the wide-day turn. (c) Fix the crash, then dev 0-24 (50 games). (d) Rank 8.

Not gaps, because a paired verdict or an engine law exists: shop-draw steering (the seed is hidden), selling animals (no engine
op), buying non-wheat/fert products (TRADER), seed lot size (constant price), weeds (cleared the same day), seat (SEATFLIP1),
the live clock (ROUTERJIT1 p99 0.17 s), and S1 non-V herd engines (their decisive moves are d0, before any tell; NONV1-4,
MELONCOUNTER2, NVTSHIP1 and MELONLOGIC1 judged the gated counters).

## 3. Verdict: top 5 gaps by expected value

| # | gap | probe | cost |
|---|---|---|---|
| 1 | G1 placement-night feed+care | `PLACEFEED_ON` for sheep/goose, full paired legs vs vrp10_esw | 3-4 agent-h, ~1,400 games |
| 2 | G2 later/never Q2/Q3 | 10-cell day grid vs V56, exact sim, then held/FRESH | 2 agent-h, ~1,600 games |
| 3 | G3 turn-0 dawn lot (A0) on d1-29 | re-judge A0 with the pump kept on d0, dev100 + held100 vs V56 | 1.5 agent-h, ~400 games |
| 4 | G4 tomato swap d2-12 | tomato logit bonus with the ask fixed, 3 cells, kill on gift | 1.5 agent-h, ~300 games |
| 5 | G5 collection cadence | census from the CREWAUDIT1 replays, build only above 100 ops/game | 1 agent-h, 0 games |

Everything else in the decision space carries a paired verdict. The ledger's closures are real. G1 is the only gap with a
premise over +1k/game; G2-G4 are plausible ±1-2 flip arms with negative priors from the standing gift law. G5-G8 are worth under
+200/g each.
