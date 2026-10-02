# 2026-09-09 — `ANIMAL_FIRST_ON`: fund the day's animals before its seeds

Follows `docs/strategy/2026-09-09-pasture-cadence.md`, Q2 bucket **(c)**: on 4
of the 15 our-seat day-states of days 1-10 where our herd trails the clone's on
the three pinned held-out boards, the planner **wanted** animals, the purse
**held** the cheapest wanted one, and `budget.grant` spent the coins on seed.
14 animals across those four mornings.

Judge: the same 180 pinned hour-0 states, replayed through `plan.build_day` by
`scratch/pastprobe.py`. **No engine run.**

## The switch

`src/kagg3/core/plan.py:4406-4462` (doc + the two constants),
`:4465-4489` (`_animal_first`, 13 code lines), `:5571-5574` (the branch at the
`n_buy = BUD.grant(...)` call site). 19 lines of code in all; `core/budget.py`
is untouched.

Two `grant`s over **disjoint** list sets, so neither budget is double-spent:

```python
payable = is_anim & (wants > 0) & (values[:, 0] > 0) & (costs[:, 0] <= purse)
gate    = (sum(payable) > 0) & (room > 0)
n_anim  = BUD.grant(..., where(gate & payable, wants, 0), purse,
                    min(room, ANIMAL_FIRST_MAX))
n_rest  = BUD.grant(..., where(gate & is_anim, 0, wants),
                    purse - spend(n_anim), room - sum(n_anim))
return  where(gate & is_anim, n_anim, n_rest)
```

No value is re-priced and no ratio is touched — the animals are simply granted
first, in the planner's own preference order (`grant` over the animal lists
alone is the same threshold), and every other list is re-solved on what is
left. `spend(n_anim) + spend(n_rest) <= purse` and the shed units `<= room`
hold by construction.

Off the gate — **want zero, or a purse under the cheapest wanted animal** —
`w_first` is all zeros, `rest` is `wants` untouched, and the second walk *is*
the OFF `grant`: same purse, same room, same wants, same call.

`ANIMAL_FIRST_MAX` is the shed units the first walk may take in a day. The
default `PJ.K` (101) is past any want and past the shed, so **the bound is
inert and the walk stops at the want**; lower it and the animals it refuses are
refused outright rather than handed back to the seed pass — they stay visible
in `purchase_shortfall`, because `wants` is never touched.

## Tests — `tests/test_animal_first.py`, 32 passing

| test | what it pins |
|---|---|
| `test_ships_off` | `ANIMAL_FIRST_ON is False`, `MAX == PJ.K` |
| `test_off_plan_is_byte_identical_to_the_pre_switch_planner` | `test_route_early`'s 12 `PIN` digests |
| `test_on_is_the_off_plan_when_no_animal_is_wanted` | want 0 → digest for digest |
| `test_on_is_the_off_plan_when_the_purse_cannot_pay` (×2) | purse 120 / 250 < 300 |
| `test_off_the_gate_the_helper_is_the_grant_itself` | unit: `_animal_first == BUD.grant` off the gate |
| `test_on_funds_the_animal_the_seeds_outranked` (×3) | the (c) signature: OFF 0 animals + all seed, ON 1/2/3 animals and fewer seeds |
| `test_on_never_buys_fewer_animals_than_off` | monotone in the herd over the 12 pinned boards |
| `test_the_animals_come_in_the_planners_own_preference_order` | goose→cow→sheep at equal value |
| `test_max_bounds_the_days_animals` (×3) | cap 1/2/3 against a want of 27 and a 90k purse |
| `test_max_does_not_bind_at_its_default` | want 4 of each, all 12 granted |
| `test_neither_budget_is_double_spent` (×16) | `spend <= purse`, shed units `<= room` |
| `test_the_unbought_want_is_still_a_shortfall` | capped want still priced into `purchase_shortfall` |

## A/B over the 180 pinned states

**OFF is the pre-switch planner: 0 of 180 states differ** on
`a_buy / n_build / seed_buy / plant_eff / spend / purse_left / w_anim /
n_buy / buy_land / shortfall / wants`, measured against a probe run of
`472b93b`'s own `plan.py`.

ON, **26 of 180** states move — all on days 3-9, all three boards.

| | OFF | ON | delta |
|---|---|---|---|
| animals wanted (`w_anim`) | 166 | 166 | **0** |
| **animals bought (`a_buy`)** | 88 | **126** | **+38** |
| **structures built (`n_build`)** | 86 | **124** | **+38** |
| seeds bought | 1,029 | 876 | **−153** |
| tiles planted (`plant_eff`) | 1,039 | 886 | **−153** |
| coins spent | 106,719 | 108,059 | +1,340 |
| purse left | 4,045,620 | 4,044,374 | −1,246 |
| `purchase_shortfall` | 261,913 | 330,099 | +68,186 |

All 24 turns rendered at each state's real crew size (36,960 hand-days):

| verb | OFF | ON | delta |
|---|---|---|---|
| **PASS** | 8,923 | **9,342** | **+419** |
| PLACE | 88 | 126 | +38 |
| BUILD_PASTURE | 70 | 104 | +34 |
| BUILD_COOP | 16 | 20 | +4 |
| **PLANT** | 1,027 | 880 | **−147** |
| WATER | 5,142 | 5,003 | −139 |
| FEED | 1,525 | 1,468 | −57 |
| CARE | 1,415 | 1,358 | −57 |
| WEST/EAST/NORTH/SOUTH | 15,686 | 15,585 | −101 |
| HARVEST / FERTILIZE / DROP | 3,660 | 3,660 | 0 |

**This is the opposite sign from `ANIMAL_RESTOCK_ON`.** That switch only filled
structures that already stood; here `sfree` is 0 through the d3-9 window, so
**every one of the 38 animals takes a tile and a BUILD**, the planting loses
147 tiles and the crew gains 419 PASS turns. The lever is displacement by
construction and the +68k shortfall is the seed it refused.

The four cited (c) states all move, exactly as traced:

| board | d | purse | want | OFF `a_buy` | ON `a_buy` | seeds |
|---|---|---|---|---|---|---|
| 106401414 | 7 | 568 | 1 goose, 1 cow, 1 sheep | 0 | 1 sheep | 4 → 1 |
| 106773901 | 8 | 1,780 | 4 cow, 1 sheep | 0 | **4 cow** | 12 → 0 |
| 106773901 | 9 | 415 | 2 cow, 1 sheep | 0 | 1 cow | 8 → 1 |
| 106793159 | 7 | 580 | 1 cow, 2 sheep | 0 | 1 sheep | 5 → 1 |

### Per-day herd, 106773901 (our seat)

`cum` is the planner's own cumulative `a_buy`; `recorded` is what the engine
replay actually owned (placed + shed), for scale.

| day | purse | want | OFF buy | ON buy | OFF cum | ON cum | recorded ours | clone |
|---|---|---|---|---|---|---|---|---|
| 0 | 2,981 | 6 | 6 | 6 | 6 | 6 | 0 | 0 |
| 3 | 583 | 2 | 0 | **1** | 6 | 7 | 5 | 5 |
| 4 | 14 | 2 | 0 | 0 | 6 | 7 | 4 | 6 |
| 5 | 884 | 1 | 1 | 1 | 7 | 8 | 4 | 6 |
| 6 | 1,385 | 1 | 1 | 1 | 8 | 9 | 5 | 6 |
| 7 | 899 | 0 | 0 | 0 | 8 | 9 | 6 | 8 |
| 8 | 1,780 | 5 | 0 | **4** | 8 | **13** | 6 | 10 |
| 9 | 415 | 3 | 0 | **1** | 8 | **14** | 6 | 13 |
| 10 | 3,033 | 2 | 2 | 2 | 10 | 16 | 6 | 14 |
| 11 | 2,037 | 2 | 2 | 2 | 12 | 18 | 8 | 16 |
| 12 | 1,393 | 1 | 1 | 1 | 13 | **19** | 10 | 17 |
| 13-29 | 127 → 84,088 | 0 | 0 | 0 | 13 | 19 | 10-11 | 14-17 |

The window the pasture doc named (d6→d10, they add 8 and we add 3) is exactly
where the switch fires, and by d12 the planner's cumulative herd is 19 against
the clone's recorded 17 — where OFF planned 13.

## NOT VERIFIED

- **No paired engine run.** The A/B is static: each of the 180 states is the
  *recorded* hour-0 observation, so the extra animals are never on the board on
  the following day. The compounding both ways is unmodelled — their product
  and their feed bill on the plus side, the tile they permanently take and the
  crop that never grows on it on the minus side. The **−153 tiles planted is
  the honest headline**, and it is bigger than any per-state number here.
- +419 PASS is the crew-lever failure signature and this switch has it. Whether
  the extra herd absorbs those turns on later days cannot be read off frozen
  states.
- The town-price side is unpriced: 38 more animals is 38 more streams into the
  same WOOL/MILK/EGG pots the season already decays (208.8 → 72.8 for wool).
- `ANIMAL_FIRST_MAX` is only tested for the bound, never swept for value; the
  default is deliberately inert.
- Only the three pinned boards; the d3-9 window is where every moved state sits,
  so nothing is known about a board that reaches d10 with a different `sfree`.
