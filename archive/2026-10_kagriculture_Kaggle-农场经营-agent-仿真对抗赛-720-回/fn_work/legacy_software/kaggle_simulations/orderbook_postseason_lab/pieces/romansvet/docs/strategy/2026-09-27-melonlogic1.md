# MELONLOGIC1 (2026-09-27 10:06Z-10:45Z): the decision logic of the non-V MELON openers that beat vrp10/vrp9

**Verdict: NONE.** Two rules explain 73 % of the mean margin: the d0-6 melon plate and the sheep herd. Both are d0 opening
decisions, made before any rival tell exists.
- Porting the plate as a d2-gated parameter change (P10) is a gift on the held tapes: −2 flips, Δtheirs +10.5k (t 5.08).
- The sheep port on master (WOOL_FIRST on a d1 latch) does nothing. The only working sheep lever is NONV4's HERD_ADD, which is not in master, and it was NO SHIP.

No build stream is recommended.

**Side finding: the shipped M20z latch.** It fires on 2 of 99 vrp10/9 live games. It cost the tine.sh game: live −23,475, and the real engine with the latch OFF gives +8,780 byte-exact. The latch swings each fire by ±20-32k, and on the 5 latch seats it is still net +1 flip, so KEEP it.
- The sim harness (eswork/NEARMISS1) does not run the runtime ENGINE_GATE latch. Its tine "FLAG" is exactly the no-latch game.

Harness: `S/melonlogic1/` (read-only on src). Rules come from `extract.py` + `rules.py` → `rules.txt`, `net.txt` and `latch.tsv`.
- Probes ran in the real engine with `ml1leg.py`: master as shipped = src vrp10_esw defaults + head_940 + theta7659, SAFETY_S 1e9, REPAIR_MS 1e7, actTimeout 600, orig seat.
- The 6 tapes were made by NEARMISS1 and read from `S/nearmiss1/tapes`. The 14 NONV1/NONV2 tapes are in `S/pool1/bank`.
- Paired results are in `summary.txt`. 52 real-engine games, local, 2 processes.

## 1. Seats: the 6 largest non-V MELON losses of vrp10/vrp9
seek inspiration −41,368 · AI是我的豆包 −23,652 · tine.sh −23,475 · ready or not −21,425 · boominginging −15,486 · Rogues −10,884.
- Median −22,450, mean −22,715. The ledger closes exactly: the sum of the net cells equals the mean margin.
- The LIVEWATCH16 seats (vrp3, at most −16k) are older code. They serve as the held bed in §4 instead.

## 2. Program spec: rules with numbers (rival R vs ours O on the same board; medians over the 6, per-rival values in `rules.txt`)
| # | rule | R (6 rivals) | O |
|---|---|---|---|
| 1 | d0 plate | 5-10 MELON + 2-13 WHEAT, no carrot (5/6); tine opens 5C/1W and adds melon d1-3; plate at d2 dawn 1-10 melon (med 7.5) | 11W/8C + 5 pastures, 0 melon |
| 2 | 2nd melon batch | melon plantings d0-9 = 10-15 (med 14); d10-19 only 0-5 (med 1.5) | d0-9 4, d10-19 11 |
| 3 | strawberry after the first harvest (d3+) | 10-39 planted d0-9 | 9-32 (same) |
| 4 | crew | 4-6 hands d0-5, jump to 8-10 at Q2 (d6), 10-12 d10-29; hands d0-9 6.5, hire$ d0-9 388-633 | 3.4, 47-76 |
| 5 | land | Q2 d6 (6/6), Q3 d8-9 (5/6), no Q4 | Q2 d5, Q3 d10 |
| 6 | herd | d0 2C+3S (4/6), 3C+2S, 4C+2S; d6-9 after Q2 +1-4 cows (6/6), then either geese +2-10 (4/6) or sheep +4-9 (seek, boom); d10 C/S/G 7/3.5/3 | d0 4C+1S+1G, adds d8-11; d10 5.5/2/1.5 |
| 7 | water | 171-239 WATER d0-9 | 216 (same) |
| 8 | fertilizer | none d0-9; 49-92 FERTILIZE d10-19 | 80 (same) |
| 9 | sales | melon sold on ripening d10-13, 24-38 units the first day, 60-78 units d10-19; sale orders spread over the day, 2-3× our order count (lots 33-68 / 71-226 / 99-290 per phase) | melon 12-24 units d10-19, sold d17-27; orders only at dawn/dusk (lots 19-24 / 39-61 / 93-123) |
| 10 | d10-19 replant | wheat 15-83, tomato 0-19, carrot 0-15, melon 0-5 | wheat 24-51, melon 1-15 |
| 11 | wheat pump | 1/6 (ready or not buys 4,076 shop wheat and resells it; about break-even) | none |

## 3. Which rules carry the margin (net = revenue − buy cost, ours − theirs, per game; `net.txt`)
| rule → cell | mean | median | share of mean |
|---|---|---|---|
| R1+R2 melon plate → MELON (d10-19 −11.5k, d20-29 +2.9k) | −8,139 | −8,240 | 36 % |
| R6 sheep → WOOL (d0-9 −3.8k on 6/6) | −8,391 | −5,376 | 37 % |
| R6 geese → EGG | −3,876 | −4,940 | 17 % |
| fert resale → FERTILIZER | −3,675 | −2,760 | 16 % |
| R6 cows → MILK | −2,286 | −1,406 | 10 % |
| offsets: hires +1.7k, animals +1.05k, wheat +1.2k, carrot +0.8k | | | |

**Melon + wool = 73 % of the mean** (61 % on medians, 83 % with eggs). Eggs are closed three times over and fert resale is closed (FERTSALE1), so the top 2 are the plate and the sheep.

## 4. Ports of the top 2 (real engine, paired vs master, orig seat)
| arm | switch (existing, parameter-only) | bed | flips | Δours (t) | Δtheirs (t) |
|---|---|---|---|---|---|
| P10 plate | `ENGINE_GATE_DAY=2, MELON 1..10, SET MELON_PLATE_TILES=10;MELON_PLATE_DAY=1;NONV_PLATE_LAST=6` | 5 new seats (tine excluded, see below) | +1/−0 (boom) | +11,272 (2.91) | +1,621 (1.23) |
| P10 plate | same | held: 10 NONV1 melon tapes | **+0/−2** (by, lamdang) | +5,459 (2.19) | **+10,541 (5.08)** |
| WF sheep | `ENGINE_GATE_DAY=1, MELON 1..10, SET WOOL_FIRST_ON=True` | 5 new seats | 0 | −171 | +26 (identical on 3/5; sheep at d10 unchanged) |

- P10 on tine is measured against OFF, because its d1 Tz latch is replaced: −877 ours, +8,844 theirs, 1 flip down.
- P10 fires only on d2 melon 1-10, so it is byte-identical on V56 (12 melon at d2, 0/100 dev and held, NONV2). The dev V56 legs were skipped by construction.
- P10 is the known plate gift (NONV2 M20: +17k theirs), now shown at dose 10 on the held tapes. The new seats' gain does not hold, and pooled over 15 seats it is −1 flip.
- WOOL_FIRST acts only on d0-2 asks, and on a d1 latch the purse does not reach it. The sheep port needs HERD_ADD_SHEEP, which is on the nonv4 branch, not in master: NONV4 a2 was NO SHIP (reacting gift +639, t 2.54). WOOLFIRST1 ungated was NO SHIP too (milk gift).

## 5. Side finding: the shipped M20z latch (Tz, d1, rival 0 melon and ≥1 plant)
- Live it fired 2/99 times: tine.sh L −23,475 and Joseph Adamski W +8,484.
- Real engine OFF vs base on the 5 latch seats: tine +32.3k (L→W), tomatos −29.5k (W→L), lucas −8.5k (W→L), atif +16.2k, fufu −3.6k. For OFF that is net −1 flip, so **keep the latch**.
- G2 (latch at d2) swaps tine for tomatos: net 0. Both rivals plant melon only from d1-2 (tine 10 melon d1-4, tomatos 36 melon d1-9), so no rival-side tell separates them. NO SHIP.
- Harness note: the eswork/NEARMISS1 sim does not execute the runtime ENGINE_GATE latch. On any seat where the latch fires, its numbers are the OFF policy (tine sim +8,780 = real-engine OFF 88,549/79,769 exactly).
