Stream: BRAINSTORM9 round 1 (Opus xhigh, fresh session, idea round only, no experiments run)
Date: 2026-09-30, 16:53Z-17:13Z
Verdict: FIVE untested rule-level ideas, ranked. The first run is TOMATO-SILENCE. None of the five can close 800 points on its own. Each one is sized to the only bar that exists today: +3 net flips vs vrp26 at t >= 2.

Read first: brainstorm8-summary, brainstorm7-summary, astra-brainstorm17, the coordinator log 09-30 12:03Z-16:53Z, MMPQRULES1R,
P48RULES1R, HARNESS1 (+ S/harness1/LAUNCH.md), LIVEWATCH24 and GAMEREAD2. For the prior-read notes I also used GAMEREAD1, TAILTRUTH1R,
CREWBC2, YIELD1, CROPMIX1, LATELOSS1, TOPAUDIT1, EARLYLAND1 (log entry 09-30 00:20Z), CREW24 (BUILD-STORY), SWITCHSWEEP1R,
STRAWDEMAND1R, and the memory files GEESE1 / HERD1 / LABOUR1 / NONV1 / SLIVER1 / IDLE2 / SCRIPTOPEN / DAWN0 / WHEATPUMP1 / ARB1. For the
engine facts I read src/kagg3/spec.py (crop and market rows), src/kagg3/sim/eod.py (plant and animal ticks) and src/kagg3/core/plan.py
(switch docs). S/brainstorm9/checkpoint.txt is the work log.

Coordinator narrowing (received mid-round): LATCHHERD1 already tests the latched herd+labour cell (cows/geese/sheep +2 x
hires +0/+2 on melon-coded programme seats). So no idea below spends a slot on herd size or crew size. The "end-of-game herd
shed" idea (MMPQ rule 4.8) was dropped on a code read: PFS feeding is already pay_day-aware (plan.py: a fire it banks for
must satisfy `h_next <= VAL.pay_day()`), so there is no d28-29 feed waste to recover. OPEN_PUMP is a price-denial round trip
(pump-off -565/game, t 9.34), not locked cash, so the opening's 53 wheat is not a capital lever.

## 1. What the 800 points mean, mechanically

**The ladder.** Ranks 1-10 run from 2,824 to 3,039: MMPQ 3,039, then DECEM, Victor, DSM, Mother-Goose, CDE, Vadim, TKNP and Majkel. All ten are
programmes. Our best live sub, vrp26, is rank ~288-296 at 2,281-2,293.

**Our record by class.**
- LIVEWATCH24 (100 games): 74-26. V 51-7 (88 %). P48 11-16; against comparable P48 (rival R0 >= 2000) 5/20 = 25 %. PQ4 1-2. Other 11-1.
- REFRESH7 (292 public games of the pair): V 172-17 (91 %), P48 18-54 (25 %), PQ4 1-10 (9 %), other 13-7.

**A ~3,000 agent's record by class, from the MMPQ reads.**
- vs P48c: 122-0, mean margin +7.6k. vs the public P48 variant +9.3k, vs the DSM variant +4.0k.
- vs its own 2464-clones (DECEM, Victor-new): 23-0, +3.6k.
- vs V: 61-0 at 118.3k vs 80.9k, +37.4k (TAILTRUTH1R).

**Our margins in coins.**
- vs V56 m40: +7.9k (106.5k vs 98.6k).
- vs P48 (P48TAPE165): MEL-coded seats -7.8k (15-55), NONE-coded seats -0.2k (30-56).
- vs PQ4: -23.4k in the d10-14 melon wave, recovering only +8.5k late.

**The 800 points are almost entirely the P48 and PQ4 columns.** We already beat V about as often as a 3,000 agent does, just by less.
- We win 25 % of P48 games where a 3,000 agent wins ~100 %. That is a swing of ~11-12k coins/game (from about -4k to +7.6k).
- We win 9 % of PQ4 games, a ~15-20k/game swing.
- In a field whose 2,400-3,000 band is programme seats (100 % of the top 39), 2,281 is simply where our V wins balance these losses.

**Where the P48 game is lost.**
- GAMEREAD2's P48 loss: -1.5k on d0-9, **-27.3k on d10-19**, +6.3k on d20-29. The d10-19 hole is melon -9.5k, wool -7.0k, milk -5.4k,
  wheat -4.7k and fert -3.0k. The rival had one more quadrant, 6 more hands and 4 more cows at d10, funded by its d0-1 melon plate.
- Pooled P48 losses: -26.6k late L-W margin, of which **-19.3k is our own price loss** (bs7). We sell the same late products the
  P48 rival floods.
- MMPQ beats P48 the other way round (P48RULES1R §7). P48 is ahead 5.5k at d11 and 4.9k at d17, then MMPQ takes +14k on d17-29
  with three rules: Q4 at d10 (+125 wheat u), an early tomato block (+75 tomato u) and 12 hands from d10. Animals are equal.

**Scale.** The biggest single gain shipped today moved P48 seats by **+1.3k/game** in H mode (vrp26 vs vrp24, +7-2 flips on 149). One net flip is
worth about 1.2 ranks (FINALSLOT1). The 800 points are therefore about 8-10 times the day's best mechanism, and no single rule
closes them. The realistic target for any idea below is **+3 net flips, about +4 ranks**. The ideas are ranked by how plausibly
each one reaches that.

## 2. Five ideas nobody tested today (ranked by my plausibility)

Common test frame, the same for all five. It is the frozen-candidate gate of bs8 applied to one switch.
- **Tree:** the shipped vrp26 tree (master fe602a07 = dist/vrp26_hyb_eve_vrp.tar.gz md5 2dcd6d44) plus one default-OFF switch.
- **OFF identity:** 3/3 per set before any read.
- **Sets:**
  - 172 P48 tapes (P48TAPE172) + 26 PQ4 tapes (PQ4TAPE26), HARNESS1 **H mode**, `HARNESS_MODE=H python S/harness1/hrun.py TREE SW OUT EPS`
    (`RSTUNE_WOOLGATE=G25` on P48, empty on PQ4), paired vs vrp26 rows on the same tapes;
  - OTH56 (the STACK1/CONFIRM1 lrun list);
  - V56 m40 + v21 reacting (`S/vband1/vr.py`, controls `S/vband1/res/v56_ctl_{m40,v21}`).
- **Qualifies (each idea's number):**
  - pooled net flips >= +3 vs vrp26 at paired t >= 2;
  - own >= 0 on every set;
  - V56 no regression (m40 >= 38/40, v21 >= 15/21; latched cells must be V56 action-identical);
  - d15-17 strawberry units and d18-29 animal units >= control.
- **Budget:** <= 4 cells, 2 h wall on <= 4 local workers (nice 19 + ionice idle).

### #1 TOMATO-SILENCE: plant the one late product the P48-public rival leaves empty (plausibility ~12 %)

**Mechanism (one sentence).** On P48-latched seats where at least one tomato-consuming shop is open at d9 and the rival shows 0 tomato tiles at d10 h0, rebalance N of our d10-13 plantings (the new Q3 tiles plus freed tiles) from late strawberry and wheat to tomato. The tomatoes ripen d18-21, 4 fires of +1/+2 each. They sell into a tomato market that the P48-public rival does not supply until ~d20 and that the tomato shops drain.

**Why the invariants allow it.**
- The d15-17 strawberry wall is made by d4-7 plantings (CREWBC2: "d15-17 supply = tiles planted d4-d7 x units per tick"). A d10-13 rebalance cannot touch it.
- The herd and the animal chain are unchanged.
- V seats stay action-identical under the melon latch (REFRESH9 census: 165/165 P48 + 26/26 PQ4, 0/113 V false positives; LATCHFIX1 149/149).
- The gate "rival tomato tiles at d10 h0 == 0" excludes DSM and MMPQ (first tomato d8.9 and d8, 9-11 tiles by d12) without a cash code.

**The evidence behind it.**
- The -19.3k P48 price loss is product overlap: every late line we sell (strawberry, milk, wool, eggs, wheat, carrot) is one the P48 rival floods.
- The P48 rulebook's public variant plants tomato only from d20.0±7.4 (d8-12: 1.0±2.7 tiles; 58±57 u d15-29). The family supply
  curves give tomato d10-29 at P48 47 u, V56 25 u and PQ4 109 u.
- PFS's own tomato is structurally near zero before d15:
  - GAMEREAD1: the softmax gives tomato 0.2-4 % on d0-14, although tomato is the most under-supplied product (share +1..+4).
  - From d15 there is no room: the field is full d12-21 with perennial strawberry.
  - From d22 `can_mature` blocks tomato.
- Of MMPQ's three rules that beat P48, early tomato (+75 u) is the only one that needs neither Q4 land nor melon cash.
- Engine rows (spec.py): tomato seed 50, first yield at 8 days, then daily for 4 fires, ongoing; market base 60, hinge 0.40 below target.
  So a tomato tile gives 4-8 units in 12 days. A late-strawberry tile planted d10 gives 4-8 units into the d20-26 glut (vs V
  216u@108 / 208u@89). Wheat gives ~2.5 cycles x ~4.7 u x ~51 ≈ 600 coins in the same footprint.

**Prior reads that touched tomato, and what they found.**
- TOMATO15 (09-16, old planner): the ENG22 tomato/carrot aim was falsified.
- BRAINSTORM1 T1 ENDGAME_TOMATO: 12 late tiles on all seats vs the flood clone: own -715 (t -2.34), the 20.8 extra tomatoes sold at 55 into the clone's flood.
- CROPMIX1 (09-30): the MMPQ tomato+carrot targets on the executor body (not PFS) gave +0.0084 coin ratio (t 1.20). Tiles came out of wheat (315 -> 221 u).
- LATELOSS1 (09-29): selling our late tomatoes earlier is worth at most +134/game.
- TOPAUDIT1: the PQ4 seat sells 119-159 tomatoes on d18-29, P48 23-82.

None of these was P48-latched, demand-keyed, gated on rival tomato silence, drawn from late strawberry rather than wheat, or read in a reacting harness.

**The 2-hour test.** `TOMATO_SILENCE_ON` (default OFF) is a ~30-line clone of `_melon_plate` (plan.py:8527): "rebalance the day's crop mix onto crop X on days DAY..LAST, tiles come off the other crops, wheat last". It uses X = TOMATO, DAY = 10, the melon latch, the shop gate (PIZZA_SHOP or FARMERS_MARKET open) and the rival-silence gate. Four cells:

| cell | N | LAST | seats |
|---|---|---|---|
| a | 6 | 12 | latched |
| b | 12 | 13 | latched |
| c | 12 | 13 | latched, shop gate off (the dose check) |
| d | 12 | 13 | all seats, silence gate on (the V question, since V56 supplies only 25 tomatoes) |

Also log tomato units, our tomato price, and strawberry units d18-29.

**Qualifies:** net flips >= +3 vs vrp26 at t >= 2 on 172 + 26 + OTH56. Cells a-c are V56 action-identical. Cell d needs m40 >= 38 and v21 >= 15.

**Kill:** own < 0 on P48, or a tomato price below ~100 (the value falls under wheat's ~600-coin footprint).

**Why only ~12 %.**
- CROPMIX1's executor gain stayed under t 2.
- GAMEREAD2's P48 rival sold 97 tomatoes on d20-29 at about 49/u (-4,765 over 97 u), so on some P48 boards the late tomato market is already cheap. The shop gate has to carry the idea.
- The rival's tomato sales on the P48 tapes are taped: the harness makes lots follow stock. That is acceptable here because P48 tomato is stock-driven anyway (r(lot, shed) 0.86).

**Step 0 (10 min, read-only, before any cell).** Take a census on the 172 P48 tapes:
- how many boards the gate fires on (tomato shop open at d9 AND rival tomato tiles = 0 at d10 h0);
- the town tomato quote on d18-24 on those boards.

Kill the idea if the gate fires on fewer than 20 boards, or if the d18-24 quote is below 100.

### #2 EVE-SEED: finish the evening-input rule that shipped today (plausibility ~8 %)

**Mechanism (one sentence).** With EVE_STOCK already moving feed and fertilizer to the h20 row, add `EVENING_SEED_ON` (tomorrow's planted seeds bought at `TURN_PRESTOCK` 20, seed prices fixed so no book moves) and `H1_WORK_ON` (a block whose opener is already on hand starts at hour 1), so that planting blocks lose the turn-1 BUY wait too.

**Why the invariants allow it.**
- It changes when inputs arrive, not what is planted or bought: no herd change, no crop mix change, no sale change.
- The days window (10,14) + (18,26) skips the d15-17 wall days. That avoids EVESTOCK1's side effect, where a shed at 95-97/100 on d15-17 moved 74 strawberry units from d17 to d18.
- `EVENING_SEED_FLOOR` 1500 and days >= 10 exclude the PRESTOCK_SEEDS d0-purse collapse (-90,863).

**Why now.**
- EVE_STOCK is today's only mechanism that became a win: +5 flips on 172 at t 2.47, V56 m40 38/40 +405, then part of hA's +9/219.
- Its gain is next-day pickup savings. The same saving is still available on every planting block.
- IDLE2: winners plant 102 vs 61 at h17-22, and our idle is 421 vs 30.

**Prior reads.**
- CREW24 (09-23, vrp3-era tree, V56 dev100, no EVE): EVENING_SEED net -5. H1 cut idle only 439 -> 425, tiles flat: "the idle crew has nothing to plant".
- SWITCHSWEEP1R 24-game screen: H1_WORK +475 (t 1.24) and H23_WATER +230 (t 0.95). Neither was promoted, and EVENING_SEED was not a survivor.
- None of these reads was taken on top of EVE (shipped 12:03Z today) or in H mode.
- NONV1 / IDLE2: the planner ask, not the start turn, limits planting. This is the main reason for the low plausibility.

**The 2-hour test.**
- Cells on vrp26:
  - (a) EVENING_SEED, days (10,26);
  - (b) (a) + H1_WORK;
  - (c) (b) with days (10,14) + (18,26);
  - (d) (c) with `EVENING_SEED_MAX` 6.
- First check whether seeds count against the 100-unit shed (`view.seeds` vs shed). If they do, cell (c) is the only admissible one.
- Log plantings by hour, PASS h0-2, and strawberry d15-17.

**Qualifies:** net flips >= +3 vs vrp26 at t >= 2, with V56 no regression (this idea is unlatched, so V56 is a real read: m40 >= 38/40, v21 >= 15/21).

### #3 EARLY-Q3 on programme seats: the EARLYLAND1 arm that never got a win read (plausibility ~6 %)

**Mechanism (one sentence).** On melon-latched seats (the latch fires at d2 h0, before the purchase), buy Q3 on d8 the way both programmes do. They sell fixed lots first (MMPQ/P48 SELL MILK 6 at d8 h1 and h6), then BUY_LAND, retried within the day. Otherwise PFS's one-a-day dawn land gate lands SW on d10 h3.

**Why the invariants allow it.**
- Only latched seats change, so V56 is action-identical.
- The known risk is EARLYLAND1's "land displaces the day's herd", which would cut late animal units. The cell therefore carries a herd-protect guard: the land buy uses only cash above today's herd want.

**Prior reads.**
- EARLYLAND1 (09-30 00:20Z, LAND_FUND_ON on the anchor tree): Q3 by d8 h6 on 13/16 programme boards against a stage-1 dose bar of 14. The arm was killed at the dose bar. There was never a win or margin read, and never a reacting harness.
- GAMEREAD2: the P48 rival had SW at d9 h3 and we had it at d10 h3. At d10 it was one quadrant, 6 hands and 4 cows ahead.
- Q4DIG1 / Q4WHEAT1R / D10WAVE1 closed **Q4** on PFS. This idea is Q3 timing, not Q4.

**The 2-hour test.** Port LAND_FUND_ON from the EARLYLAND1 branch onto vrp26, with the latch and the guard. Cells:
- (a) Q3-only, no guard;
- (b) Q3 + herd-protect guard;
- (c) (b) with retries until d9 h12.

Read on 172 P48 + 26 PQ4 in H mode plus the V56 identity check.

**Harness caveat.** A rival land slip is not modelled, because the rival's units are taped. This idea changes only our timing, so the harness is valid for it.

**Qualifies:** net flips >= +3 at t >= 2, own >= 0, animal units d18-29 >= control on the latched seats.

**Why low.** The day gained is one or two days of 25 tiles, against a ~11k/game P48 gap.

### #4 CARROT-FLOOD DODGE: stop selling into P48's largest late flood (plausibility ~4 %)

**Mechanism (one sentence).** On P48-latched seats, cap our d18-27 carrot plantings (K = 0 or half) and give those tiles to wheat. The P48 rulebook shows their carrot back-loaded d19-27, scaled by carrot demand at d15 (0/1/2/3 shops -> 24/47/68/94 tiles), sold "all stock" at h22-h1 and dumped with d29 sentinels (78 of 119 carrot sentinel orders fall on d29).

**Why the invariants allow it.** It changes d18+ plantings only (the wall is safe), the herd is untouched, and V56 stays identical under the latch.

**Prior reads.**
- CARROTFLAT 1-3 (09-18): keeping carrot when the town bid is low was REJECTED; the class gate gave +177..+284 at t 1.4-1.6.
- CARROT_EARLY_HOLD (09-16): rejected for shed eviction.
- STRAWDEMAND1R (09-30): the strawberry version of "remove our glut" was **a two-purse wash**. This is the main reason for the low plausibility: removing our carrot raises the rival's carrot price as much as ours.
- Carrot base price is 35 (spec.py), so the stake is a few hundred coins.
- Never read latched on P48 with the rulebook's demand key, and never in H mode.

**The 2-hour test.** Cells: K = 0 and K = half, each keyed and unkeyed on carrot demand at d15 (4 cells). Read on 172 P48 in H mode, with 26 PQ4 as a guard.

**Qualifies:** net flips >= +3 at t >= 2 with own >= 0. A two-purse wash (own up, rival up by the same) is a NONE.

### #5 D29-DUMP DODGE: sell our last lots ahead of P48's sentinel dump (plausibility ~2 %)

**Mechanism (one sentence).** On P48-latched seats, sell d28's harvest on d28 (an extra dusk lot at turn 22) instead of carrying it into d29. P48 rule 5.9 dumps every product with sentinel SELL 9999/1000 on d29. Our shipped ENDROUTE sells the whole d29 shed on the last turn, into their dump.

**Why the invariants allow it.** It touches only d28-29 sales on latched seats.

**Prior reads.**
- ENDSELL (09-17): a d28-29 early dump lost -68 (t -0.74) against the pre-programme field.
- ENDFAMILY (09-18): the end-value axis is closed. The last lot carries 1,250-1,565 coins of produce and is "the deepest lot of the game".
- DROPHARV / ENDROUTE: the terminal-turn sale shipped (+116).
- None of these was P48-latched against a rival known to dump on d29.

**The 2-hour test.** One cell, on P48 172 in H mode. The harness reproduces sentinel lots from stock.

**Qualifies:** net flips >= +3 at t >= 2. Realistically this is worth <= 0.5k/game, so it is listed for completeness rather than for flips.

### Considered and not proposed (each already read)

**Herd and labour size.**
- LATCHHERD1 is running that cell.
- GEESE1 (09-19): GEESE_TARGET=4 gave -17.6k, a gift.
- HERD1: every extra animal replaces another, because d0-9 cash is fully spent.
- LATE_GOOSE: closed.
- TAILTRUTH1R: every sheep step gives V56 +4..10k.
- LABOUR1 / NONV1: hires follow work.
- HIRE_BIAS_ZERO: -547 in STACK2.

**Opening.**
- SCRIPTOPEN: -16.2k.
- WOOL_FIRST: "non-transferable".
- MIRROR_OPEN: a tape artefact.
- DAWN0: hands are bought daily.
- OPEN_PUMP-off: -565 (t 9.34).

**Fertilizer.**
- Collection is already ~98 % on sight (actscan 09-16), 19/day vs MMPQ 22 (CREWBC2).
- Tick-eve strawberry fertilizer: PFS already fertilizes 7.2/7.2 production nights (YIELD1) and sells 48-51 strawberries d15-17, the same as MMPQ.
- FERT_VOLUME (bar multiple): -302 on the screen. FERT_DUMP: <= 0 on all 9 V56 cells.

**Melon, wool and timing** (MELONPQ1, WOOLGATE1, PRECADENCE1): closed today.

**Shed-clear for the wall.** STACK2's EVE reserve 10 gave +10 flips but incremental margin -162. EVESTOCK1 measured the shed cost at only ~0.4 strawberry u/game.

## 3. The one to run first: #1 TOMATO-SILENCE

It is the only candidate that meets all of these:
- It attacks the documented P48 loss channel: the -19.3k price loss is product overlap, and tomato is the one late product the P48-public rulebook leaves unsupplied until ~d20.
- It is invariant-safe by construction: d10+ plantings only, no herd change, and V56 action-identical under a latch that is 165/165 P48 + 26/26 PQ4 with 0/113 V false positives.
- It copies one of MMPQ's three P48-beating rules, the one that needs neither Q4 land nor melon cash.
- It is a small, low-risk patch that clones an existing rebalance hook (`_melon_plate`), with two observable gates: a tomato shop open, and rival tomato tiles = 0 at d10.

Cell (d) doubles as the first test of whether the same substitution (late-glut strawberry -> tomato) also pays against V, which supplies only 25 tomatoes.

## 4. The question for round 2

"On the P48 seats we lose (NONE-coded -0.2k, MEL-coded -7.8k), which late product does the rival leave unsupplied that PFS can grow from d10+ tiles without touching the d4-7 strawberry tiles or the herd? And does TOMATO-SILENCE turn that into >= +3 net flips in H mode? If it does not, is the P48 gap then provably out of reach for any rule that respects the two invariants?"

## Slips
- One `find` over the whole tree timed out and was moved to the background (read-only, no output used).
- No experiments run and no remote. The only writes are this doc and S/brainstorm9/checkpoint.txt.
