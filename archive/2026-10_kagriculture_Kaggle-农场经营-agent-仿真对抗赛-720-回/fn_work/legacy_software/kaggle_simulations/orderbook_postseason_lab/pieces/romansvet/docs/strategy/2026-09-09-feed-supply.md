# Feed supply: what actually caps the fundable CARE+FEED pair

Worktree `.claude/worktrees/care-cov` (base dc24975). Data: the 3 pinned replays under
`scratchpad/alloc_review/rep` (6 games = 3 boards x 2 seats), plus a temporary probe inside
`plan._derive` replaying all 180 (game, day) hour-0 states through `build_day` with the live theta
(`flow135_g350_gpfwdfv.npy`). Scripts: `scratchpad/feedsup/census.py` (engine census) and
`scratchpad/feedsup/probe.py` (planner probe).

## Checkpoint 1 (t+20 min) - the previous note's mechanism is wrong

`docs/strategy/2026-09-09-care-coverage.md` concluded that ~21 planned CAREs a game land on an animal
whose FEED *failed* for lack of wheat in the acting unit's inventory. That is not what happens.

Engine census, per game, our seat (6 games):

| quantity | ours | opp |
|---|---|---|
| animal-days | 331.5 | 378.0 |
| FEED ops in the action stream | 254.2 | 327.7 |
| animal-days the engine records `fed_today` | **254.2** | 321.0 |
| PICKUP WHEAT units | 252.3 | 377.7 |
| cared / cared-and-fed | 228.5 / 228.5 | 351.3 / 312.7 |
| WHEAT sold / bought | 231.3 / 147.8 | 426.3 / 207.0 |
| wheat crop tile-days | 258.3 | 532.0 |

**FEED ops emitted == animal-days fed, exactly.** No FEED of ours is ever dropped by the engine for
an empty unit inventory, and every wheat we pick up becomes a feed (252.3 picked / 254.2 fed; the
balance is carry from a wheat HARVEST). So design (a) - a bigger wheat PICKUP - has **zero surface**.

Planner probe, per game (means over 6 games), taken at the point `want_feed` / `want_care` are cut:

| stage | per game | what removes the animal-days |
|---|---|---|
| animal-days | 318.8 | |
| `feed_want` | 275.5 | -43.3: no reason to feed (`care_ok` false: `max_held` headroom, or past `VAL.pay_day()` on d27-29) |
| `feed_pass` | 266.0 | -9.5: feed value below the wheat quote |
| `want_feed` | **252.7** | **-13.3: rationed by `wheat_avail = shed_wheat + wheat_buy`** |
| `care_ok` | 229.7 | |
| `want_care` | **216.7** | -13.0, i.e. exactly the rationed feeds |

**The binding constraint on the fundable CARE+FEED pair is 13.3 animal-days a game where the day's
wheat (shed + what the budget granted) will not stretch to a feed that passed the value test.**

And the sale is what empties the shed: `plan.py:6580` reserves `sum(want_feed)` wheat - *today's*
feeds only - and sell lot 1 takes literally all the rest, every day. Day 16 (mean): 27.7 wheat in
the shed at hour 0, 9.0 reserved, **18.7 sold**; day 15: 39.0 in, 13.7 reserved, 25.3 sold; day 5:
38.7 in, 5.3 reserved, 33.3 sold. Two days later the day buys the wheat straight back - 147.8 units
a game against 231.3 sold, round-tripped across the price curve. On the short days the budget then
refuses the buy (d13: 7.0 wanted, 3.2 granted, 3.9 feeds rationed away).

=> the lever is (b): reserve the herd's next-N-day feed from the SELL lot, not just today's.

## The switch: `FEED_RESERVE_ON` (`plan.py`, ships OFF)

One expression, at the sale's wheat reservation in `_plan_and_stats`:

```python
wheat_need = xp.sum(d.want_feed.astype(i32), dtype=i32).astype(i32)
if FEED_RESERVE_ON:                                          # [SWITCH]
    fr_struct = (view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE)
    fr_herd = xp.sum((fr_struct & (view.occ >= 0)).astype(i32), dtype=i32).astype(i32)
    wheat_need = xp.maximum(wheat_need, fr_herd * FEED_RESERVE_DAYS).astype(i32)
wheat_reserved = xp.where(terminal, 0, wheat_need).astype(i32)
```

Design (b) of the three, because (a) has no surface at all (FEED ops emitted == animal-days fed,
exactly, so no FEED ever fails for an empty unit inventory) and (c) is a rotation change worth
hundreds of lines. It adds no PASS turn and displaces no crop task *by construction*: the sale
resolves at turn 1, after `_derive` has already fixed the day's purchases, task list and block cut.
The forced-overflow continuation is untouched, so a shed that would overflow still liquidates the
reserve rather than destroying it. `tests/test_feed_reserve.py`, 8 tests: the OFF half is
`test_route_early`'s `PIN_SEEDS` digest (byte-identical, and `FEED_RESERVE_DAYS = 0` reproduces it
with the switch ON), the ON half pins the floor, its scaling, the short-shed no-op and the terminal
day.

## Planner A/B, 3 pinned boards x 2 seats = 6 games, 180 (game, day) hour-0 states

Same-state arms (`scratchpad/feedsup/ab.py`) are **identical** on every op -- FEED 254.2, CARE 235.8,
PASS 1,123.2, WATER 857.0 -- and differ only in the lot: wheat sold 231.3 -> 213.7 a game. That is
the switch's whole same-day footprint, and it is the honest answer to "does it displace anything
today": no.

The reserve's only channel is the *next* morning's shed, which a same-state replay cannot see. A
sequential carry model (`scratchpad/feedsup/ab2.py` -- replay each board's 30 days in order, carrying
`max(carry + sold_OFF - sold_ON, 0)` wheat forward into the shed the ON arm plans on):

| arm | unit-turns/g | PASS% | FEED/g | CARE/g | WATER/g | PLANT/g | wheat sold/g | wheat bought/g |
|---|---|---|---|---|---|---|---|---|
| OFF      | 6516.0 | 17.24 | 254.2 | 235.8 | 857.0 | 171.2 | 231.3 | 147.8 |
| ON d=1   | 6504.0 | 17.13 | 254.2 | 234.8 | 855.7 | 170.8 | 228.3 | 128.5 |
| ON d=2   | 6448.0 | 16.77 | **258.5** | **239.3** | 849.5 | 165.7 | 228.3 | 69.7 |
| ON d=3   | 6444.0 | 16.90 | 259.5 | 240.3 | 849.5 | 166.0 | 228.3 | 63.0 |

At the shipped `FEED_RESERVE_DAYS = 1` the floor (the herd, 13.7 head on d15-29) barely clears the
reservation the day already makes (`want_feed` 9-14), so it keeps 3 wheat a game off the lots and
buys 19.3 fewer -- and funds **zero** extra feeds. Two herd-days is where the reserve starts to
carry: +4.3 FEED and +3.5 CARE a game, 78.1 fewer wheat bought back, against -5.5 PLANT, -7.5 WATER
and 68 fewer live unit-turns (2.8 hand-days) -- the shed room the held wheat occupies, displacing
seed and animal buys.

**Caveat on the carry model, stated because it decides the read:** the carried wheat is added to the
shed but never consumed by the day's pickups in the model, so it can only leave through a sale. That
overstates the carry, and with it the d=2/d=3 rows. The +4.3 FEED is an upper bound, not a
measurement.

## Engine paired read -- the switch LOSES, do not promote

`scratchpad/feedsup/engine.py`: the same three pinned boards, both seats, pinned town schedule,
theta `flow135_g350_gpfwdfv`, `eval_vs_baselines._play` verbatim. `FEED_RESERVE_DAYS = 2` -- the only
arm the carry model gave a positive FEED delta, so the read was spent on the arm most likely to show
the mechanism.

| episode | seat | OFF ours | OFF theirs | ON ours | ON theirs | d ours | d theirs | win |
|---|---|---|---|---|---|---|---|---|
| 106401414 | 0 | 86,959 | 67,578 | 85,887 | 69,185 | **-1,072** | +1,607 | W -> W |
| 106401414 | 1 | 86,959 | 67,578 | 85,887 | 69,185 | -1,072 | +1,607 | W -> W |
| 106773901 | 0 | 101,483 | 132,057 | 101,634 | 132,098 | +151 | +41 | L -> L |
| 106773901 | 1 | 101,483 | 132,057 | 101,634 | 132,098 | +151 | +41 | L -> L |
| 106793159 | 0 | 146,711 | 153,513 | 139,578 | 154,304 | **-7,133** | +791 | L -> L |
| 106793159 | 1 | 147,943 | 153,135 | 140,923 | 153,917 | -7,020 | +782 | L -> L |

**mean -2,666 coins a game for us, +812 for the opponent; wins 2/6 both arms** (the pinned boards are
seat-symmetric, so this is 3 distinct games, and the loss is carried by one of them).

The sign is consistent with the carry model's *costs* rather than its benefit: on 106793159 the
reserve costs 7.1k, and the opponent gains on every board -- the wheat we keep off the lots is wheat
they sell into a shelf we left them. The displacement the model flagged (-5.5 PLANT, -7.5 WATER, 2.8
hand-days a game, all of it shed room) is the mechanism, and it is worth more than 4.3 feeds.

`FEED_RESERVE_ON` stays **OFF**, and on this evidence should not be promoted at any `DAYS >= 2`. The
`DAYS = 1` arm was not read in the engine: the planner A/B shows it funds exactly zero extra feeds
(FEED 254.2 both arms), so the read would have priced a 3-wheat-a-game sale deferral against nothing.

## What is left standing

The measurement, not the switch. Two facts that outlive it:

1. **Design (a) is dead.** FEED ops emitted == animal-days fed, 254.2 == 254.2. No FEED of ours ever
   fails for an empty unit inventory, and the previous note's mechanism ("the FEED failed") is wrong.
2. **The 13.3 rationed feeds a game are a budget-grant refusal, not a sale.** `want_feed` is cut by
   `feed_rank < wheat_avail` on 13.3 animal-days, and on those days `wants[L_WHEAT]` exceeds
   `wheat_buy` -- the greedy wanted the wheat and did not grant it (d13: 7.0 wanted, 3.2 granted,
   money 1,026). Feeding those animals is a *purse* question at the BUY row, not a reservation
   question at the SELL row, and the next lever in this family belongs in `budget.grant`'s ranking of
   the wheat list -- where it costs no shed room, which is what killed this one.
