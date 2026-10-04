# Post-sale H30 mechanism review

This review uses only the preserved first four H30 boards: eight paired OFF /
`h30_water` games. It is a replay explanation, not a new evaluation, and it
does not pool this evidence with H30B or any other family. The reproducible
checks are in `S/postlot/explain_mechanism.py`.

## What the paired replays establish

The post-sale hook did not fire on seed 1166044943 and both seats were identical
to OFF. It fired once in each of the other six games. Each firing bought one
melon seed for 80 coins, planted and watered it on the firing day, and later
harvested that exact tile at yield six. Thus crop execution is not the failure
mode in this subset.

| seed | seat | hook | own action / market rows changed | own cash | opponent cash | opponent physical rows |
|---:|---:|---|---:|---:|---:|---:|
| 1166044943 | 0 | none | 0 / 0 | 0 | 0 | 0 |
| 1166044943 | 1 | none | 0 / 0 | 0 | 0 | 0 |
| 1196709180 | 0 | melon, day 6 hour 11 | 517 / 58 | -1575 | +122 | 24 |
| 1196709180 | 1 | melon, day 6 hour 11 | 517 / 58 | -1575 | +122 | 0 |
| 2079139712 | 0 | melon, day 4 hour 11 | 575 / 52 | +417 | +54 | 48 |
| 2079139712 | 1 | melon, day 4 hour 11 | 576 / 53 | +383 | +54 | 0 |
| 2097576449 | 0 | melon, day 6 hour 11 | 530 / 59 | +466 | +70 | 0 |
| 2097576449 | 1 | melon, day 6 hour 11 | 535 / 60 | -322 | +79 | 0 |

The first controlled action difference is the injected purchase itself. The
next daily plan sees different money, seed inventory, and then the extra plant.
The resulting plans diverge broadly: 517 to 576 of 719 controlled action rows
change in every firing game. This is the central distinction. The hook adds a
crop to the state of a policy that replans every day; it does not add an
otherwise isolated purchase, harvest, and sale to a fixed trajectory.

## Why a harvested crop can finish down 1575 coins

For seed 1196709180, identically in both seats, the injected melon was harvested
on day 16 hour 17 and its first following six-melon sale was in the day 17 hour
1 order. The paired cash path closes exactly as follows:

| component | ON minus OFF cash |
|---|---:|
| injected seed purchase | -80 |
| all other changes through the row before the crop sale | +802 |
| bundled crop-sale transition | +1440 |
| all changes after that transition | -3737 |
| final | **-1575** |

The +1440 is the difference in the whole bundled transition, which also buys a
wheat seed and sells wheat, eggs, wool, and fertilizer. It cannot be assigned
entirely to the six melons from these observations. Even granting the full
+1440 to that row, later replanning loses 3737 relative coins.

The final market program is materially different. Across the season, ON
submits six more melon units for sale, exactly the injected yield, but also 13
fewer wheat, nine fewer carrot, four fewer strawberry, and 20 fewer wool units;
it submits 37 more egg and two more milk units and changes purchases, animals,
and hiring. These are submitted quantities, not a claim that every requested
unit executed. Two large later transitions show the practical displacement:
on day 22 hour 1 ON requests 12 rather than 18 melons and the whole transition
is -1248 relative to OFF; on day 23 hour 1 it requests six rather than 12,
adds a four-wheat purchase, and the transition is -1389. The two changed final
liquidation rows contribute another -1369. Summed by whether the controlled
market list matches, -1561 of the final -1575 occurs on rows whose controlled
orders differ; rows with the same controlled market list sum to -14.

The smaller seed 2097576449 seat-1 loss has a different chronology. Its seed
purchase is -80, other changes before the first following crop sale are -1543,
the bundled sale transition is +1117, and later changes recover +184, closing
at -322. This reinforces that a successful harvest does not identify the sign
of the full replanned trajectory. The other three firing games finish up by
+383 to +466, so the preserved boards do not show one universal loss mechanism.

## The 72 opponent physical-state rows are weed relocations

All 72 rows consist solely of two opponent tile positions exchanging `WEED`
and empty. Opponent farmer positions, hands, unlocked land, hire count, private
shed, seeds, and carried inventories remain equal. Each two-tile signature is
created once at a day boundary and then persists unchanged to step 719:

| seed / controlled seat | creation | OFF weed | ON weed | rows |
|---|---|---|---|---:|
| 1196709180 / 0 | end of day 28 | (1, 6) | (0, 7) | 696–719: 24 |
| 2079139712 / 0 | end of day 27 | (9, 0) | (8, 1) | 672–719: 48 |

The engine's end-of-day weed walk uses one deterministic random draw per empty
unlocked tile, traversing player 0 before player 1. Reconstructing the eligible
tiles and `random.Random((seed * 1_000_003) ^ day)` reproduces both relocations
exactly:

| seed / day | player-0 eligible tiles OFF / ON | shared hit draw | opponent rank OFF / ON |
|---|---:|---:|---:|
| 1196709180 / 28 | 25 / 23 | index 50 = 0.00483190721447091 | 25 at (1,6) / 27 at (0,7) |
| 2079139712 / 27 | 19 / 18 | index 21 = 0.0004271789816491234 | 2 at (9,0) / 3 at (8,1) |

The changed controlled farm therefore shifts the same below-0.005 RNG draw to
a later empty tile on player 1's farm. This also explains the seat asymmetry.
When the hook controls seat 1, the opponent is player 0, whose weed draws occur
before player 1's changed empty-tile count, and no opponent physical difference
appears.

These weed rows do not explain the initial opponent cash advantage. Before the
weed difference exists, opponent cash is already +251 on seed 1196709180 seat
0 and +140 on seed 2079139712 seat 0; the final differences are +122 and +54.
Across all eight games the opponent submits exactly the same action sequence,
including the same market orders. The earlier cash decomposition found 560
changed opponent cash transitions, 536 with a different displayed pre-action
price. The unchanged shared market re-quotes and commits units against inventory
changed by our sales, so identical opponent orders receive different proceeds.
The late weed signatures never expand and do not change the submitted opponent
actions. The preserved replays do not provide a counterfactual that separately
removes those weeds, so they establish the RNG mechanism and temporal order,
not an independently measured zero effect on final cash.

## Limits and decision consequence

This is exact evidence for four H30 boards only. It does not explain the full
30-board H30 opponent gain, and the full OFF capture was still in progress
during this review. Cash transitions containing several market orders cannot
be attributed order by order from replay money alone. Most importantly, the
paired games do not hold later controlled plans fixed, so they measure the
whole feedback path rather than a standalone crop return.

The evidence supports no policy promotion or new variant. It identifies two
separate observed effects to examine on the eventual 30-board decomposition:
controlled replanning changes production and liquidation enough to reverse a
successful crop's local gain, while shared inventory changes the proceeds of
unchanged opponent orders. The 72 physical rows have a narrower, fully
reproduced cause in end-of-day weed RNG indexing.
