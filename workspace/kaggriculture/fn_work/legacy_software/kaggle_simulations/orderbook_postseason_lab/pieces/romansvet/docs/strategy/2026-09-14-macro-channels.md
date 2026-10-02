# 2026-09-14 — MACRO-CHANNELS: the herd as a floor, and the sale clock

**CHECKPOINT 1 VERDICT: the ceiling was 91 % of the herd loss, and what is
left is still not a lever. ymg_aq's day-0 plate is neither free nor costly —
it is ALREADY OURS: B buys 1 GOOSE + 4 COW + 1 SHEEP on day 0 against the
top's 0/2/3, spends its whole 3,000-coin purse doing it (165 left at dawn d1),
and the floor's extra sheep is cash-refused. `"plate0"` is a -155 coin
(t -0.5) no-op on the band that still flips 3 boards; the rest of the herd
calendar as a floor (`"herd_floor"`) costs -1,784 (t -4.0) and 15 boards.**

**CHECKPOINT 2 VERDICT: the sale-timing channel is a loss, and it is entirely
the PULL-FORWARD half. Obeying ymg_aq's sale clock costs -2,824 coins/board
(t -13.4, 7 boards lost) on the band; imitating only their DELAYS
(`"sell_late"`) is free at -52 (t -0.4, 0 flips). Their clock is early
(median hour 0-1 for wheat, carrot, egg and fertilizer) and our late lots are
where the money is: the same 1,400 units fetch 89.9 coins each against B's
91.7. The opponent gains nothing from it (-205) — unlike every other macro
channel this one is a pure own-goal, not a transfer.**

Sim, descriptive, paired, CRN, action-replay opponent seat, theta B =
`flow193_g100_hr` with the shipped `hr` switches. **No engine game, no
training arm, no ladder claim.** OFF baselines are the existing
`raw_melOFF.npz` (68 band boards) and `raw_headOFF.npz` (12 ymg_aq boards) —
same tree, same board lists, the OFF path did not move. All coin figures are
per-board means over the two seats.

## 1. What was built

Five new `MACRO_MODE` values (`src/kagg3/core/plan.py:4734`), and sites 5/6
mode-gated for the first time so a herd-only or sell-only arm leaves the hire
enumeration alone:

| mode | sites | what the schedule owns |
|---|---|---|
| `"herd_floor"` | 1 (floor), 3, 4 | the herd, as a LOWER BOUND, all 30 days |
| `"plate0"` | 1 (floor), 3, 4, masked to day 0 | the day-0 plate and nothing else |
| `"hands_herd_floor"` | + 5, 6 | crew + herd floor |
| `"sell"` | 7 | the sale clock: each product's whole voluntary sale resolves on the lot carrying the schedule's hour |
| `"sell_late"` | 7 (hold half) | the sale clock as a DELAY only |

* **The floor.** `_macro_targets` (`:4853`) now writes
  `animal_want = maximum(decode, schedule[day])` under the three floor modes
  instead of the schedule's row whole. That is the MACRO-RAMP §5.2 defect
  fixed: the old site 1 wrote a zero row on the 24 days the extract says
  nothing about, which silenced B's own herd line and froze the herd at 5.9
  from d8 (B reaches 17.0 by d16). Under the floor the herd ends at 16.7
  against B's 17.0 — the ceiling is gone.
* **`"plate0"`** is the same floor with a traced `day == 0` mask on all three
  herd sites (`_macro_plate0()`, `:4771`; the mask at `:4857`, `:5579`,
  `:5000`). d1-29 are byte-identical to B, pinned by a test over the whole
  plan tuple on four days.
* **Site 7, the sale clock** (`:6990`, a new `if MACRO_EXEC_ON and
  MACRO_SCHEDULE is not None:` block immediately after `SELL.allocate`, before
  `s_qty`). **Precisely what was built, because it is not what the checkpoint
  asked for:** `extract.py` records `sell_hour[day][product]` — the first turn
  a SELL row for that product resolved on the tape — **and nothing about the
  quantity**, so "sell up to q at hour h" is *not expressible from the
  schedule as it exists*; the executable version is "sell at h". Our three
  lots stand on turns 3/10/18 (`early_lot_turns()`), so each product's hour
  maps to the first lot at or after it (h ≤ 3 → lot 1, 4-10 → lot 2, 11-18 →
  lot 3, h > 18 → the day sells none of it voluntarily) and the day's whole
  voluntary sale of that product moves there. `-1` (the tape sold none that
  day) is no constraint rather than a ban: the channel under test is *when*,
  and a day the top holds a product is a day our own reservation still decides.
  The shed law is downstream and untouched — whatever a hold overflows is
  still force-sold. `macro_load` decodes the row at `:4821` (shifted ±1 so the
  zero-pad reads as -1).
* **`"sell_late"`** keeps whatever the allocator already placed at or after
  the hour and carries only the units that would have resolved too early, so
  it is the delay half of the channel alone. It exists because ymg_aq's hours
  are *early*, which makes `"sell"` mostly a pull-forward, and the two halves
  had to be priced apart.
* **Sites 5 and 6 are mode-gated.** Site 5 (`:6444`) is now inside
  `if _macro_site(5):`; site 6 is by exclusion, so its guard (`:6846`) gained
  `and _macro_site(6)`. **That guard line is the one edit outside a
  `MACRO_EXEC` block**, and `MACRO_EXEC_ON` short-circuits in front of it, so
  the OFF path evaluates exactly as before — pinned, as always, by
  `test_every_mode_is_inert_while_the_switch_is_off` over the whole plan tuple
  on four boards for all ten modes plus a nonsense one.

## 2. Checkpoint 1 — the herd as a floor

**68 band boards** (B wins 43 %, so flips are informative):

| arm | ours | theirs | Δcoins vs B (t) | Δmargin vs B (t) | hires/season | herd d3/d6/d10/d16 | idle d10 | tiles d10 | win % | flips +/- |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 104,092 | 104,284 | — | — | 261.9 | 6.0/6.6/11.1/17.0 | 2.7 | 37.7 | 43 % | — |
| **plate0** | 103,937 | 105,049 | **-155 (-0.5)** | -920 (-3.4) | 261.3 | 6.0/6.6/10.9/17.1 | 1.6 | 37.5 | 38 % | +0/-3 |
| **herd_floor** | 102,308 | 110,330 | **-1,784 (-4.0)** | -7,830 (-10.1) | 257.4 | 6.0/7.8/11.5/16.7 | 4.9 | 33.6 | 21 % | +0/-15 |
| hands_herd_floor | 94,896 | 118,119 | -9,196 (-9.4) | -23,031 (-14.2) | 277.0 | 6.0/7.8/10.0/15.5 | 7.4 | 32.0 | 4 % | +0/-26 |
| *hands* (RAMP) | 99,232 | 107,682 | -4,860 (-9.1) | -8,258 (-15.0) | 277.0 | 6.0/6.0/10.1/17.0 | 1.9 | 38.0 | 19 % | +0/-16 |
| *hands_herd* (ceiling) | 85,447 | 121,275 | -18,645 (-12.7) | -35,636 (-21.1) | 277.0 | 5.0/6.0/5.9/**5.9** | 5.8 | 40.4 | 3 % | +0/-27 |

**12 ymg_aq boards** (B wins 0 % of these — they are top-five tapes):

| arm | ours | theirs | Δcoins vs B (t) | Δmargin vs B (t) | hires/season | herd d3/d6/d10/d16 | idle d10 | tiles d10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 93,127 | 106,879 | — | — | 261.2 | 6.0/6.5/10.7/17.2 | 1.1 | 38.1 |
| **plate0** | 94,546 | 108,804 | **+1,418 (+1.9)** | -508 (-1.2) | 262.8 | 6.0/6.5/10.7/17.0 | 4.3 | 39.2 |
| **herd_floor** | 85,140 | 110,046 | **-7,987 (-2.3)** | -11,154 (-3.2) | 255.5 | 6.0/7.2/11.1/16.8 | 7.2 | 31.5 |
| hands_herd_floor | 81,228 | 119,120 | -11,899 (-3.9) | -24,140 (-7.1) | 277.0 | 6.0/7.0/9.7/13.9 | 7.9 | 32.1 |
| *hands* (RAMP) | 90,391 | 113,943 | -2,736 (-5.3) | -9,800 (-6.4) | 277.0 | 6.0/5.5/9.2/16.1 | 2.0 | 38.8 |

### 2.1 The ceiling was the defect, and fixing it recovers 16,861 of 18,645

`"hands_herd"` -18,645 → `"hands_herd_floor"` -9,196 is the crew-inclusive
pair; the crew-free pair is the honest one: the herd calendar as a *ceiling*
cost -18,645 with the crew, as a *floor* without the crew it costs -1,784.
The herd at d16 is 16.7 under the floor against 5.9 under the ceiling and
17.0 for B. MACRO-RAMP §5.2 was right that the -18,645 confounded two things,
and the split is roughly 91/9 in favour of "stop growing the herd".

### 2.2 The day-0 plate is already ours, not free

This is the sharpest result of the checkpoint and it is a *negative* answer to
the question as posed. B's opening is **1 GOOSE + 4 COW + 1 SHEEP = 6 head on
day 0** — one head MORE than ymg_aq's 0/2/3 plate — bought with 53 wheat seeds
out of a 3,000-coin purse that is empty by dawn d1 (164.7 coins left; total
day-0 spend 4,025, the difference being the day's own sales). The floor asks
for `max(1,0)/max(4,2)/max(1,3) = 1/4/3` = 8 head and delivers 6: **the two
extra sheep are cash-refused**, exactly as `2026-09-14-herd-growth-screen.md`
§2 measured for the d6 cows. Day-1 purchases are identical unit for unit
(53 wheat, 1/4/1 animals, 4,025 coins) with the plate imposed and without.

So the arm is a no-op that still costs: -155 coins (t -0.5, inside noise) but
-920 margin (t -3.4) and **3 boards flipped to losses**, because the 40-coin
difference in dawn-d1 cash reshuffles the shop lottery downstream. There is no
free day-0 herd lever here. The herd screen's finding stands with a better
reason: the day-0 herd is not lost on coins to seed spend *in our planner* —
our planner already buys it, and the purse, not the valuation, is what stops
the seventh head.

### 2.3 What `"herd_floor"`'s -1,784 is made of

The floor's own asks are d3 (1 COW) and d6 (4 COW), and they land: herd 7.8 at
d6 against B's 6.6, 19.0 head bought over the season against 17.0. The cost is
**tile displacement, paid late**: crop tiles at dawn d10 are 33.6 against B's
37.7 and idle tiles 4.9 against 2.7, because the coop/pasture the extra head
needs is built on a tile the day would have planted and the seed spend rises
(buy spend 13,840 against 12,701). The coin trace is level to d15
(+55 at d6, -734 at d15), craters in the back half (-3,994 at d18, **-6,825 at
d21**) and half-recovers by d30 (-1,784) as the late herd pays back. Wage bill
actually *falls* (5,075 against 5,306, hires 257.4 against 261.9): a farm with
more animals and fewer crops has less work.

### 2.4 The channels are worse than additive

`hands` -4,860 plus `herd_floor` -1,784 is -6,644; `hands_herd_floor` measures
**-9,196**, an interaction of -2,552. The crew the schedule fields early and
the herd the floor buys early compete for the same dawn purse — dawn cash d6
is 769 against B's 866 — and both end up under-delivered (herd d16 15.5,
against 16.7 for the floor alone).

## 3. Checkpoint 2 — the sale clock

**68 band boards:**

| arm | ours | theirs | Δcoins vs B (t) | Δmargin vs B (t) | units sold | coins/unit | win % | flips +/- |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 104,092 | 104,284 | — | — | 1,404 | 91.7 | 43 % | — |
| **sell** | 101,268 | 104,079 | **-2,824 (-13.4)** | -2,619 (-13.2) | 1,400 | 89.9 | 32 % | +0/-7 |
| **sell_late** | 104,040 | 105,035 | **-52 (-0.4)** | -803 (-5.0) | 1,404 | 91.7 | 43 % | +0/-0 |

**12 ymg_aq boards:** `sell` **-3,364 (t -6.3)**, margin -3,199 (t -4.9);
`sell_late` **-711 (t -1.8)**, margin -1,183 (t -2.9).

### 3.1 The loss is the pull-forward, and only the pull-forward

ymg_aq's sale clock is early — the modal hour over the days they sell is
**1 wheat, 0 carrot, 1 tomato, 5 straw, 0 melon, 0 egg, 1 wool, 0 fert**, and
of 270 (day, product) cells only 21 name an hour after our first lot (turn 3)
and 7 an hour after our last (turn 18). So `"sell"` is overwhelmingly a
*forward* move: the day's whole sale of a product is dumped into lot 1 instead
of spread over the three lot curves the allocator chose. That is the entire
loss. `"sell_late"`, which carries the delays and never pulls anything
forward, is **-52 coins on 68 boards with zero flips** — free, and pointedly
so: imitating the top's *patience* costs nothing, imitating their *haste*
costs 2,772.

| arm | ΔWHEAT | ΔCARROT | ΔTOMATO | ΔSTRAW | ΔMELON | ΔMILK | ΔEGG | ΔWOOL | ΔFERT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sell | -52 | -98 | -154 | -591 | +51 | -24 | **-1,595** | -350 | -91 |
| sell_late | -147 | -40 | +11 | +245 | +56 | -19 | -75 | -138 | -87 |

**EGG is 56 % of the damage.** The top sells eggs on 20 of the 30 days, at a
median hour of 0;
our allocator spreads the coop's daily output over lots 2 and 3, where the
town has restocked the shelf and the quote has recovered. Straw (-591, their
hour 5) is the same story one lot later. The two products whose Δ is positive
under `sell_late` (straw +245, melon +56) are the ones whose *delay* helps.

### 3.2 It is an own-goal, not a transfer

Every other macro channel measured this week has `Δmargin ≈ 2 × Δcoins`,
because the shared pot hands what we stop buying and selling to the opponent:
`"hands"` gives them +3,398, `"hands_herd"` +16,991, `"herd_floor"` +6,046.
The sale clock gives them **-205** — Δmargin -2,619 against Δcoins -2,824.
Nothing changes hands; we simply sell the same 1,400 units into a worse part
of the day's price curve. **Our lot allocator is strictly better at the
*when* than the top's tape is**, which is the first channel in this family
where our machinery beats theirs outright rather than merely surviving.

### 3.3 So `"sell" + "hands"` was not run

The checkpoint's condition was "if `sell` is positive on either set". It is
negative on both (-2,824 band, -3,364 ymg), so the combined arm was skipped and
the budget went into the `sell_late` decomposition instead, which is what
turned "the timing channel loses" into "which half of it loses".

## 4. Tests

```
$ JAX_PLATFORMS=cpu python -m pytest tests/test_macro_exec.py -q
.......................                                                  [100%]
```

23 tests, all pass (`--collect-only -q` reports 23; `pyproject.toml` already
carries `addopts = "-q"`, which is why the count line is suppressed). Seven
are new:

* `test_mode_herd_floor_takes_the_maximum_not_the_schedule` — the same view
  under `"hands_herd"` (herd silenced to 0/0/0 on a day the schedule zeroes)
  and under `"herd_floor"` (the decode's goose survives, the plate lands).
* `test_mode_herd_floor_leaves_the_crew_to_the_enumeration` — sites 5/6 are
  gated: a nine-hand schedule hires the enumeration's count under
  `"herd_floor"` and nine under `"hands_herd_floor"`.
* `test_mode_plate0_is_day_zero_only` — the plate on day 0, and the whole plan
  tuple unchanged on d1/d3/d6/d20.
* `test_mode_sell_moves_the_sale_onto_the_schedules_lot` — hours 0/3 → lot 1,
  4/10 → lot 2, 11/18 → lot 3, volume conserved, never split.
* `test_mode_sell_past_the_last_lot_holds_the_product` — hour 23 sells none.
* `test_mode_sell_touches_nothing_but_the_sale` — unit routes byte-identical,
  HIRE/BUY_SEED/BUY_ANIMAL/BUY_LAND quantities unchanged.
* `test_mode_sell_late_is_the_delay_half_only` — hour 0 is a no-op, hour 23
  holds, hour 12 carries lots 1-2 to lot 3.

`test_every_mode_is_inert_while_the_switch_is_off` now covers all ten modes
plus a nonsense one, over the whole plan tuple on four boards.

## 5. What this says

1. **The herd channel is closed.** Ceiling -18,645, floor -1,784, day-0 plate
   -155 — the curve flattens toward zero as the schedule says less, and never
   crosses it. There is no herd instruction from ymg_aq's tape that pays.
2. **The day-0 opening is not where the 300 rating points are.** B already
   fields more head on day 0 than the top does, on an empty purse. The
   FORWARD_ADMIT family (crew, herd, tiles, land, and now the opening plate)
   is measured out.
3. **Our sale allocator beats theirs.** The one channel where copying the top
   makes us *strictly* worse with no benefit to them. Any future "imitate the
   top" arm should leave the sale rows alone; the patience half is free if it
   is ever wanted for another reason.
4. **`sell_hour` is now priced.** All four macro channels of EXEC-SCOPE §6.2
   (crew, herd, calendar, sale clock) have been measured and all four lose.
   The executor family has nothing left to extract from ymg_aq's tape.

## 6. Next experiment

**EGG-LOT**: the one number in this report that points *forward* rather than
closing a door is `"sell"`'s -1,595 on eggs — proof that lot placement of a
daily-output product is worth over a thousand coins a board in the wrong
direction, which means the allocator's current placement is a live gradient in
the right one. Re-run the `sell` machinery with our own clock instead of
ymg_aq's: force every product's sale into lot 1, lot 2 and lot 3 in turn
(three arms, same 68 boards, ~5 min each) and read off the per-product profile
of what the day's price curve pays. If any product's best fixed lot beats the
allocator's spread by more than the -52 noise floor `sell_late` establishes,
that is a `SELL` heuristic change with a measured slope — the first one this
family has produced.

## 7. Files

* `src/kagg3/core/plan.py` — modes `:4705-4760`, `_macro_plate0` `:4771`,
  `sell` row `:4821`, floor `:4853`, site 3 `:5577`, site 4 `:4999`, site 5
  `:6444`, site 6 `:6846`, site 7 `:6990`.
* `tests/test_macro_exec.py` — seven new tests, 23 total.
* `S/macro_exec/report_channels.py` — the cross-arm ledger (adds herd d16, the
  sale ledger by product, units and coins/unit, the opponent's Δ).
* `S/macro_exec/report_channels.md` — both board sets, every arm.
* `S/macro_exec/raw_{herd_floor,plate0,hands_herd_floor,sell,sell_late}.npz`
  (12 ymg_aq boards) and `raw_*_band.npz` (68 band boards), plus the matching
  `.log` files.
