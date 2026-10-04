# The care that rides a feed: attribution, and the one gate that refuses it

Worktree `.claude/worktrees/care-cov` (base `9b5d3d7`). Three pinned boards x 2 seats = 6 games.
Engine census `scratchpad/feedsup/buckets.py`, planner probe `scratchpad/feedsup/probe2.py`
(a temporary hook in `_derive`, replaying all 180 hour-0 states with `flow135_g350_gpfwdfv`).

## Checkpoint 1 (t+20 min) - bucket attribution

Engine truth first, because the brief's "~40" comes from the older note's *banked* figure:

| per game | ours |
|---|---|
| animal-days fed | 254.2 |
| animal-days cared | 228.5 |
| cared **and** fed | 228.5 (every care of ours already rides a feed) |
| **fed and left uncared** | **25.7** |
| CARE ops in the action stream | 235.8 |
| -> emitted but not realised | **7.3** (a second CARE on an already-cared tile, or an animal gone) |

Planner side, at the cut `want_care = want_feed & care_ok`, per game:

| bucket | per game | verdict |
|---|---|---|
| fed and uncared **at admission** | 36.0 | (the tail hop recovers ~10 of these after the fact, hence 25.7 realised) |
| ...refused by `care_pays` (`care_price > price[WHEAT]`) | 28.0 | **the switch's target** |
| ...refused by the horizon (`h_next > VAL.pay_day()`) | 13.3 | leave alone: the bank reaches no sale |
| ...refused by `care_headroom` | **0.0** | not a constraint on our boards at all |
| ...refused by `survival_pays` / already cared | 0.0 / 0.0 | |
| **passes every gate except `care_pays`** | **22.7** | the free bucket |

Band split: d0-9 0.0 fed-uncared, d10-19 9.3 (all `care_pays`), d20-29 26.7 (18.7 `care_pays`,
13.3 horizon, overlapping).

Route cost of the third bucket ("would need an extra hop"): **zero, by construction.** The care is
added to the *feed's own tile chain*, so the unit is already standing on the tile and the op is the
adjacent turn - `tests/test_care_with_feed.py` asserts same unit, `|dt| == 1`. The action-stream
read confirms nothing better is available: pairing FEED actions to tiles is ambiguous on 210 of the
254 animal-days a game (several units FEED in the same turn), so the geometry question is answered
structurally rather than statistically.

Engine ordering: the bonus banks on the day flags alone -
`if tile["cared_today"] and tile["fed_today"]: pending_care_bonus += 1` at the nightly refresh
(`kaggriculture.py:829-830`), and CARE takes no item and no money (`:524-530`). So the CARE may sit
either side of the FEED and still bank tonight.

## The switch: `CARE_WITH_FEED_ON` (`plan.py:2834`, ships OFF)

Two hunks. `care_ride` is cut beside `care_ok` with `care_pays` dropped, and `want_care` reads it:

```python
care_ride = care_ok
if CARE_WITH_FEED_ON:
    care_ride = (has_animal & (view.t_cared == 0) & (h_next <= VAL.pay_day())
                 & care_headroom & survival_pays)
...
want_care = want_feed & care_ride
```

`feed_want`, `feed_value`, `care_val`, `mand_feed` and the tier all keep reading `care_ok`, so the
switch cannot buy a wheat and cannot promote a feed into the mandatory tier - it only ever *adds* to
`want_care` on a tile the day already feeds. The new care's admitted labour is `v_care`'s existing
floor of one coin (`:5712`), unreachable OFF, so it bids last for the day's turns.

## Checkpoint 2 (t+45 min) - planner A/B, 6 games, 180 hour-0 states

`scratchpad/feedsup/ab3.py`. Both arms on the identical states; unlike `FEED_RESERVE_ON`, this
switch acts entirely inside the day it plans, so a same-state A/B *is* the whole measurement.
"pairs" counts a CARE adjacent to a FEED in the same unit's row -- the tile chains that bank tonight.

| band | arm | unit-turns | PASS% | FEED | CARE | **pairs** | WATER | HARV | PLANT | FERT | hand-days |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d0-9   | OFF | 1088.0 | 19.62 | 48.2 | 48.2 | 48.2 | 166.7 | 35.3 | 62.0 | 0.0 | 45.3 |
| d0-9   | ON  | 1088.0 | 19.62 | 48.2 | 48.2 | 48.2 | 166.7 | 35.3 | 62.0 | 0.0 | 45.3 |
| d10-19 | OFF | 2712.0 | 16.70 | 114.2 | 109.2 | 104.8 | 369.8 | 146.7 | 53.7 | 106.3 | 113.0 |
| d10-19 | ON  | 2736.0 | 17.36 | 114.2 | **114.2** | **114.2** | 369.8 | 146.7 | 53.7 | 106.3 | 114.0 |
| d20-29 | OFF | 2716.0 | 16.82 | 91.8 | 78.5 | 65.2 | 320.5 | 221.8 | 55.5 | 89.5 | 113.2 |
| d20-29 | ON  | 2732.0 | 17.60 | 91.8 | **84.8** | **78.5** | 320.5 | 221.8 | 55.5 | 89.5 | 113.8 |

Season, per game: **CARE 235.8 -> 247.2 (+11.4), CARE+FEED pairs 218.2 -> 240.8 (+22.6)** -- the
22.7 the probe said were refused by `care_pays` alone, recovered exactly. And nothing else moves:
FEED 254.2 both arms, WATER 857.0, HARVEST 403.8, PLANT 171.2, FERTILIZE 195.8, wheat sold 231.3,
wheat bought 147.8, all identical. There is no displacement to price.

The one cost: live unit-turns 6,516 -> 6,556 and hand-days 271.5 -> 273.2 (**+1.7 hands a game**) --
the extra care work raises 1.5's hire enumeration -- and PASS 1,123.2 -> 1,169.2, i.e. the switch
buys 1.7 hands, spends 22.6 of their turns on care and leaves the other 46 idle. d0-9 is untouched
(no herd yet); the whole effect is d10-29.

Sizing: 22.6 banked units a game at the d10-29 quotes the census measured (milk 143.7, wool 100.8)
is +2.3k to +3.2k coins, against 1.7 hand-days of wages.

Tests: `tests/test_care_with_feed.py`, 10 tests -- OFF pinned byte-identical on `test_route_early`'s
`PIN_SEEDS` digest, ON pinned on same-unit/adjacent-turn placement, herd scaling, and the three
gates it must keep (no feed -> no care, headroom, horizon, and "cannot buy a wheat the care alone
would want"). 74 tests green across `care_with_feed`, `route_early`, `care_fill`, `care_hold`,
`feed_mandatory`, `feed_rationing`, `feed_care_cadence`, `feed_value`.

## Engine paired read - LEVEL, and n is really 1

`scratchpad/feedsup/engine.py`: the same three pinned boards, both seats, pinned town schedule,
theta `flow135_g350_gpfwdfv`, `eval_vs_baselines._play` verbatim.

| episode | seat | OFF ours | OFF theirs | ON ours | ON theirs | d ours | d theirs | win |
|---|---|---|---|---|---|---|---|---|
| 106401414 | 0 | 86,959 | 67,578 | 86,812 | 67,595 | -147 | +17 | W -> W |
| 106401414 | 1 | 86,959 | 67,578 | 86,812 | 67,595 | -147 | +17 | W -> W |
| 106773901 | 0 | 101,483 | 132,057 | 101,484 | 132,057 | +1 | 0 | L -> L |
| 106773901 | 1 | 101,483 | 132,057 | 101,484 | 132,057 | +1 | 0 | L -> L |
| 106793159 | 0 | 146,711 | 153,513 | 146,711 | 153,513 | 0 | 0 | L -> L |
| 106793159 | 1 | 147,943 | 153,135 | 147,943 | 153,135 | 0 | 0 | L -> L |

**mean -49 coins a game for us, +6 for them; wins 2/6 both arms.** Both purses barely move.

Two boards came back identical to the coin, which had to be checked rather than assumed.
`scratchpad/feedsup/verify.py` replays 106793159 seat 0 with the switch set in-process and dumps the
engine replay: ON and OFF are the same game -- 326 fed, 313 cared, 313 both, 317 CARE ops, in both.
The switch did not misfire; **that board has no surface**. The per-game census says why:

| game | animal-days | fed | cared | **fed-uncared** |
|---|---|---|---|---|
| 106401414 seat 0 / 1 | 359 | 241 | 191 | **50 / 50** |
| 106773901 seat 0 / 1 | 254 | 194 | 179/180 | 15 / 14 |
| 106793159 seat 0 / 1 | 381/382 | 326/329 | 313/317 | 13 / 12 |

The 22.6 pairs a game the A/B measured are **not spread over the three boards** -- 106401414 carries
50 of them and the other two 12-15 each, and those two are exactly the boards the engine read shows
inert. So the read is one board with surface, and on it the switch banked ~50 extra care units and
came out 147 coins behind (with the opponent 17 ahead). That is two orders of magnitude inside the
shop-lottery band (any tile change re-rolls every later shop, +/-25k zero-mean), so it is **not a
verdict, it is an absence of one**.

`CARE_WITH_FEED_ON` stays **OFF**. It is the cleanest planner delta in this family -- +22.6
CARE+FEED pairs with FEED, WATER, HARVEST, PLANT, FERTILIZE and both wheat rows byte-identical -- and
it has no engine evidence behind it.

## What could not be verified

1. **Whether the extra 50 banked units on 106401414 ever reached a sale.** The read says the coins
   did not appear; the two candidate sinks -- `max_held` at the fire, and our own glut walking the
   milk/wool curve down -- were not separated. The census tool for this exists
   (`docs/strategy/2026-09-09-care-coverage.md` measured the opponent losing 22.3 units a game at the
   cap); it was not run on an ON replay.
2. **Any read wider than one board.** Three pinned boards, one with surface, is not a measurement.
   The next step is the 42-board pinned held-out set, not another 3-board pair.
3. `v_care`'s pricing for the new cares. They ride the existing floor of one coin, which makes them
   bid last -- deliberately, to keep displacement at zero, and the A/B confirms zero. Pricing them at
   the product instead (the wheat is sunk) would admit them earlier and *would* displace; untested.
