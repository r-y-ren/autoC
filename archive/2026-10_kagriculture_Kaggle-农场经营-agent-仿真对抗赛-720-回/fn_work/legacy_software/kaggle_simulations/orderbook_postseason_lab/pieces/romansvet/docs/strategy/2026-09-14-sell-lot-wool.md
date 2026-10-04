# 2026-09-14 — SELL-LOT / WOOL: our lot allocator, priced from both ends

**CHECKPOINT 1 VERDICT: no fixed lot beats the allocator's spread, but two
products have a measured, replicated slope inside it. Pinning EVERY product to
one lot costs -4,748 (lot 1, t -16.8), -4,928 (lot 2, t -7.8) and -6,497
(lot 3, t -11.4) coins/board on 68 band boards, so the allocator's `when` is
right in aggregate — third time this family has said so. Per product it is
not: EGG gains +1,613 (lot 2) / +1,435 (lot 3) on the band and +1,594/+1,782
on the twelve ymg_aq boards, FERTILIZER +223/+299 and +1,183/+1,209, STRAW
+1,523/+1,849 and +358/+446 — every one of them far outside the ±52 noise
floor, and all three agree in sign across the two board sets. MILK is the
mirror image (-1,760 pinned to lot 1) and wheat/carrot/tomato/melon want the
spread. Single-product arms then split the three: STRAW alone on lot 3 is
**+524 coins (t +4.4)**, replicated and outside noise but a margin wash
(-231, the opponent takes +755); EGG alone on lot 2 is **-9 (t -0.4), a
pure no-op** — its +1,613 in the sweep was the cash collapse of §2.1, not
placement. Read the sweep's per-product column as a POINTER, not a price.**

**CHECKPOINT 2 VERDICT: the wool gap is PRODUCTION, not selling; the herd test of it is cash-refused and the sale-row test of it is clipped (§4, §4b). We sell
100 % of the wool we shear — 116.4 collected, 116.4 sold, 0.00 unsold at
the end on the band; 121.7/121.7/0.00 against ymg_aq — so "unsold stock 5.3"
in the top-5 ledger is other products, and no lot, hold or clock change can
recover a unit of it. The -13.2 units (ymg) / -30.7 units (band) are two
thirds SHEARING RATE (0.929 wool per sheep-day against their 0.996 / 1.081)
and one third SHEEP-DAYS, and the sheep-days are all in d0-9: we stand
**1.0 sheep from d1 to d8** while they stand 1.9-3.3, so their first shear
banks 11.2-18.0 units against our 5.0. Against ymg_aq the price half of the
gap (-25 coins/unit, -3,370) is larger than the volume half (-2,327); on the
band our realised wool price is BETTER (+8.9) and the whole -2,987 is volume.**

**THE PAIRED TEST: `"sheep13"`, a 3-head sheep floor on days 1-3 — see §4.**

Sim, descriptive, paired, CRN, action-replay opponent seat, theta B =
`flow193_g100_hr` with the shipped `hr` switches. **No engine game, no
training arm, no ladder claim.** OFF baselines are the existing
`S/macro_exec/raw_melOFF.npz` (68 band boards) and `raw_headOFF.npz` (12
ymg_aq boards) — same tree, same board lists, the OFF path did not move.

## 0. A labelling defect in the report script, carried into MACRO-CHANNELS

`S/macro_exec/report_channels.py:16` lists `PROD = [... "MELON", "MILK",
"EGG", ...]`, but `spec.py:29` is `I_EGG, I_MILK, I_WOOL, I_FERT = 5, 6, 7,
8`. **Columns 5 and 6 are swapped in every table that script printed.** So
`2026-09-14-macro-channels.md` §3.1's headline — "EGG is 56 % of the damage,
-1,595" — is **MILK**, and its "-24 MILK" is EGG. The correction is confirmed
independently here: pinning every product to lot 1 (this report's `lot1`,
which is what ymg_aq's early clock amounts to) costs MILK -1,760 on the band
and -1,795 on ymg_aq, and EGG **+19 / -31**. Every other column of that report
(and every wool number, column 7) is unaffected. `S/sell_lot/report_lot.py` is
the corrected copy; the top-5 ledger (`S/oppsell/extract.py`, `PROD =
list(spec.PRODUCTS)`) was always right.

## 1. What was built

Two new `MACRO_MODE` families, both wholly inside `if MACRO_EXEC_ON and
MACRO_SCHEDULE is not None:` blocks, and two new default-off module constants.
The OFF path is character-identical and pinned as always by
`test_every_mode_is_inert_while_the_switch_is_off` over the whole plan tuple.

| mode | site | what it does |
|---|---|---|
| `"lot1"`/`"lot2"`/`"lot3"` | 8 (new) | every voluntary unit of every product in `SELL_LOT_PRODUCTS` resolves on that one lot, OUR clock, the allocator's own quantities |
| `"sheep13"` | 1, 3, 4, windowed | `animal_want[SHEEP] = max(decode, SHEEP_FLOOR_N)` on `SHEEP_FLOOR_DAYS` and nothing else |
| `ANIMAL_SAME_DAY_ON` | the sale rows | every animal harvest the route reaches is offered on the day's LAST lot (a plain default-off switch, not a mode) |

* **Site 8** (`src/kagg3/core/plan.py:7101`) sits beside site 7 and reads no
  schedule row at all — the mode names the lot. `move = sum(lots, axis=0)` is
  exactly what the value-gated greedy already decided to sell today, so
  nothing the reservation refused is sold and nothing it accepted is held:
  only the row changes. `s_qty` is unchanged in total, so the shed-overflow
  deficit downstream is the same number it was.
* **`SELL_LOT_PRODUCTS`** (`:4799`, default `None` = every product) restricts
  the move to one product, which is what turns the confounded three-arm
  profile into a single-product paired measurement (§2.3). A bare int is
  accepted so a runner can name it on a `--switches` line.
* **`"sheep13"`** (`_macro_targets`, `:4926`) is a STOCK want like every other
  `animal_want` — site 4 differences the standing head off it — on the sheep
  column alone. `_macro_window()` (`:4837`) generalises `"plate0"`'s `day == 0`
  mask to an inclusive window and now carries both modes; the three plate0
  mask sites (`:4949`, `:5091`, `:5671`) read the window instead, value for
  value, and the plate0 tests still pass unchanged.
* **`SHEEP_FLOOR_N = 3`, `SHEEP_FLOOR_DAYS = (1, 3)`** (`:4787`). Day 0 is
  excluded on purpose: MACRO-CHANNELS §2.2 measured the day-0 version of this
  ask (the top's 0/2/3 plate) **cash-refused** — B spends its whole 3,000-coin
  purse on 1 GOOSE + 4 COW + 1 SHEEP and has 165 coins at dawn d1.

## 2. Checkpoint 1 — own-clock lot placement

**68 band boards** (B wins 43 %):

| arm | ours | theirs | Δcoins vs B (t) | Δmargin vs B (t) | units | coins/unit | idle d10 | tiles d10 | win % | flips +/- |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 104,092 | 104,284 | — | — | 1,404 | 91.7 | 2.7 | 37.7 | 43 % | — |
| **lot1** | 99,344 | 103,064 | **-4,748 (-16.8)** | -3,529 (-13.2) | 1,410 | 88.0 | 2.7 | 37.6 | 29 % | +0/-9 |
| **lot2** | 99,164 | 115,032 | **-4,928 (-7.8)** | -15,676 (-25.5) | 1,327 | 94.4 | 9.7 | 25.9 | 6 % | +0/-25 |
| **lot3** | 97,595 | 117,093 | **-6,497 (-11.4)** | -19,306 (-30.0) | 1,268 | 97.4 | 9.5 | 26.1 | 3 % | +0/-27 |

**12 ymg_aq boards:** `lot1` **-3,520 (t -6.5)**, `lot2` **-7,807 (t -3.1)**,
`lot3` **-8,596 (t -5.3)**; margins -2,548 / -16,542 / -18,728.

### 2.1 The two arms are two different failures

`lot1` is the clean one: the farm is untouched (idle 2.7, tiles 37.6, herd
identical, hires 262.9 against 261.9), the same 1,410 units are sold, and they
fetch **88.0 instead of 91.7** — a pure price loss of 3.7 coins/unit, and the
opponent gains nothing (-1,220). That is the same own-goal MACRO-CHANNELS
§3.2 found, isolated from the tape: dumping the day's whole book on turn 3
walks every product down its own curve.

`lot2`/`lot3` are a **cash-clock** failure, not a price one: coins/unit RISES
to 94.4/97.4, but the farm collapses — crop tiles at dawn d10 are 25.9 against
37.7, idle tiles 9.7 against 2.7, and 77-136 fewer units are sold all season.
Holding the book to turns 10/18 means the morning's purse is yesterday's
revenue only; dawn cash d6 reads *higher* (1,862 against 866) because the day
could not spend it in time. The opponent takes +10,748 / +12,809 of what we
stop developing. So the aggregate verdict "lot 2 and lot 3 are bad" is mostly
a statement about the BUY row, which is why the per-product arms below matter.

### 2.2 The per-product profile (Δ sale revenue vs B, mean coins/board)

| product | band lot1 | band lot2 | band lot3 | ymg lot1 | ymg lot2 | ymg lot3 | best lot |
|---|---:|---:|---:|---:|---:|---:|---|
| WHEAT | -153 | -1,766 | -3,258 | -240 | -1,254 | -2,038 | the spread |
| CARROT | -142 | -1,279 | -1,888 | -189 | -905 | -1,264 | the spread |
| TOMATO | -209 | -891 | -1,066 | -489 | -2,068 | -2,622 | the spread |
| STRAW | -1,507 | **+1,523** | **+1,849** | -470 | **+358** | **+446** | **lot 3** |
| MELON | -21 | -778 | -929 | -2 | -1,656 | -1,718 | the spread |
| **EGG** | +19 | **+1,613** | **+1,435** | -31 | **+1,594** | **+1,782** | **lot 2-3** |
| MILK | **-1,760** | -1,107 | -683 | **-1,795** | -476 | -45 | the spread (never lot 1) |
| WOOL | -764 | -947 | -735 | -234 | -1,905 | -1,354 | the spread |
| FERT | -35 | +223 | +299 | -13 | **+1,183** | **+1,209** | **lot 2-3** |

Read against the ±52 noise floor `sell_late` established. EGG, FERT and STRAW
are positive on both board sets at both late lots; WHEAT, CARROT, TOMATO and
MELON are negative everywhere; MILK's worst lot is lot 1 by a factor of two.
The three winners are exactly the **daily-output** products (a coop's egg, a
COLLECT's fertilizer) plus the one crop that harvests in a big late batch —
i.e. stock that ARRIVES DURING THE DAY, after the dawn allocator sized
`avail` from the hour-0 shed. The losers are the dawn-stock products, whose
curve the allocator already prices correctly.

### 2.3 Single-product arms (the confound removed)

`SELL_LOT_PRODUCTS` pins ONE product and leaves the other eight with the
allocator, so the farm-wide cash collapse of §2.1 cannot leak in:

| arm (68 band boards) | ours | Δcoins vs B (t) | Δmargin vs B (t) | Δ that product | units | coins/unit | Δopponent | flips +/- |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** | 104,092 | — | — | — | 1,404 | 91.7 | — | — |
| **straw → lot 3** | 104,616 | **+524 (+4.4)** | -231 (-1.1) | STRAW **+537** | 1,402 | 92.2 | +755 | +0/-4 |
| **egg → lot 2** | 104,084 | **-9 (-0.4)** | +20 (+0.8) | EGG **-7** | 1,404 | 91.7 | -29 | +0/-0 |

**Straw replicates and egg does not.** Straw alone on lot 3 is **+524 coins
(t +4.4)** with the farm untouched (idle 2.7, tiles 37.7, hires 261.6) and
+537 of it on the straw line itself — the three-arm sweep's +1,849 was about a
third real. It is a coin gain and a **margin wash**: the opponent takes +755
of the same shelf, so Δmargin is -231 (t -1.1) and 4 boards flip. Egg alone on
lot 2 is **-9 coins, zero flips, every product inside ±25** — the sweep's
+1,613 was entirely the §2.1 cash collapse redistributing, not a placement
gain. Which is the point of §3's mechanism rather than a refutation of it: the
egg the allocator can move is YESTERDAY's egg, already in the dawn shed; the
egg that is actually mispriced is today's, which no lot of today offers at all.

## 3. Checkpoint 2 — the wool anatomy

`S/sell_lot/wool.py` reads the dawn snapshots the CRN runner already writes
(`sold_np`, `sold_rp`, `shed`, `anim`, `price`, `mkt_inv`), both seats, so the
tape's own wool book is differenced against ours board for board. Nothing is
re-simulated.

| band | sheep-days us/th | collected us/th | sold us/th | coins us/th | coins/unit us/th |
|---|---|---|---|---|---|
| *12 ymg_aq boards* | | | | | |
| d0-9 | 10/29 | 9.0/30.0 | 5.0/23.3 | 993/4,808 | 198/206 |
| d10-14 | 25/21 | 10.7/16.7 | 8.8/23.3 | 1,405/4,305 | 159/185 |
| d15-29 | 95/85 | 102.0/88.2 | 107.8/88.2 | 19,104/18,086 | 177/205 |
| **season** | **131/135** | **121.7/134.8** | **121.7/134.8** | **21,501/27,199** | **177/202** |
| *68 band boards* | | | | | |
| d0-9 | 11/20 | 9.0/18.7 | 5.0/18.4 | 1,007/3,773 | 201/205 |
| d10-14 | 26/28 | 13.3/20.8 | 8.9/20.1 | 1,673/3,656 | 188/182 |
| d15-29 | 88/88 | 94.2/107.9 | 102.6/108.6 | 13,607/11,845 | 133/109 |
| **season** | **125/136** | **116.4/147.4** | **116.4/147.1** | **16,287/19,274** | **140/131** |

**Where the 13 units are (ymg_aq).** Not in the shed: collected 121.7, sold
121.7, wool held at the end **0.00** (all products 5.42 — the ledger's "unsold
5.3" is fertilizer and melon, not wool), and **zero** days on which we hold
wool at dawn and sell none. Not in the sheep count at d20 either — 6.5 to
their 5.8, as the ledger said. It is:

1. **Shearing rate, ~2/3 of it.** Wool per sheep-day 0.929 (ours) against
   0.996 (ymg_aq) and **1.081** (the band clones). At our 125-131 sheep-days
   that is 8-19 units. Hands, not animals.
2. **Sheep-days in d0-9, ~1/3.** 10 against 29 (ymg) and 11 against 20
   (band). Season totals are nearly level (131/135, 125/136) — the herd
   catches up by d12 and passes them by d16. The gap is entirely the opening.

**The day-by-day mechanism** (both board sets, identical shape):

| d | sheep us/th | wool collected us/th | wool sold us/th | dawn quote |
|---|---|---|---|---:|
| 1-5 | **1.0**/1.9-3.2 | 0/0 | 0/0 | 206 → 217 |
| 6 | 1.0/2.2-3.2 | **5.0/11.2-18.0** | **0.0**/9.8-18.0 | 218-220 |
| 7 | 1.1/2.2-3.3 | 0/0 | **5.0**/0.0-1.4 | 199-202 |
| 9 | 2.3-2.9/3.7-4.0 | 4.0/7.5-12.0 | **0.0**/5.3-7.3 | 197-200 |
| 10 | 2.8-3.3/3.8-4.7 | 0/0 | **4.0**/0.2-7.7 | 190-194 |
| 12 | 5.3-5.5/4.0-5.8 | 4.0-4.4/7.5-13.0 | **0.0**/3.0-6.9 | 171-193 |
| 13 | 5.9/5.8 | 0.4/1.1 | **4.4**/2.0 | 186 |

Two readings, and the second is the one worth having:

* **We hold exactly ONE sheep from d1 to d8.** The first shear therefore banks
  5 units where theirs banks 11-18. Sheep 2 and 3 arrive around d9-d12.
* **Every batch we shear is sold the NEXT MORNING; theirs is sold the same
  day.** d6 shear → d7 sale, d9 → d10, d12 → d13, on every board. The
  allocator sizes `avail` from the **hour-0 shed** (`plan.py:7022`), and wool
  that a hand collects at hour 9 is not in it, so no lot of that day offers
  it. Fertilizer has a fix for exactly this (`SAME_DAY_FERT_ON`, `:7294`),
  melon has two (`MELON_OPEN`, `MIDDAY_PLACE_V2`), and the DROP return leg
  adds the route's banked harvest to lot 3 — **animal products have none**.
  The quote falls 218 → 202 across that one night (d6 → d7), so the latency
  is worth roughly 8-16 coins on each early unit, and it is the same defect
  §2.2 sees from the other side: EGG and FERT, the two daily-output products,
  are the two that GAIN from a later lot.

Against ymg_aq the price half (-25 coins/unit, -3,370) is larger than the
volume half (-2,327); on the band our price is *better* (+8.9) and the whole
-2,987 is volume. Their 202 coins/unit is bought with 23.3 units sold in d0-9
at 206, while the quote is still at its opening 200-217 — a pure calendar
effect, not a better sale.

## 4. The paired test — `"sheep13"`, a 3-head sheep floor on d1-3

| arm | ours | theirs | Δcoins vs B (t) | Δmargin vs B (t) | sheep d1-8 | herd d6/d10/d16 | wool units | hires | flips +/- |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| **B** (68 band) | 104,092 | 104,284 | — | — | 1.0…1.2 | 6.6/11.1/17.0 | 116.4 | 261.9 | — |
| **sheep13** (68 band) | 103,880 | 104,395 | **-212 (-1.1)** | -323 (-1.4) | **1.0…1.2** | 6.6/11.2/17.1 | 117.0 | 263.1 | +2/-1 |
| **B** (12 ymg_aq) | 93,127 | 106,879 | — | — | 1.0…1.2 | 6.5/10.7/17.2 | 121.7 | 261.2 | — |
| **sheep13** (12 ymg_aq) | 87,941 | 124,730 | **-5,186 (-2.0)** | -23,037 (-8.7) | 1,1,1,**2,2,2,2,2** | 4.2/6.0/12.7 | **113.7** | 236.4 | +0/-0 |

**The floor is cash-refused on the band, exactly as the day-0 plate was.**
Sheep at dawn d1-d8 under `"sheep13"` is 1.0/1.0/1.0/1.0/1.0/1.0/1.1/1.2 —
**character-identical to B**. The ask never lands, so the -212 (t -1.1, inside
noise, +2/-1 flips) is the shop lottery reshuffled by a few coins of dawn
cash and nothing else. On the twelve ymg_aq boards it lands *partially* (2.0
sheep from d4, never 3) and is a disaster: the herd it displaces never
recovers (d10 6.0 against 10.7, d16 12.7 against 17.2), the crew falls to
236.4 hires, the opponent takes +17,851, and **wool itself goes DOWN**,
113.7 units against 121.7 — the second sheep costs more cows than it earns
fleeces.

So the opening-herd family is closed for sheep too, on the same mechanism
MACRO-CHANNELS §2.2 named for the day-0 plate: the purse, not the valuation,
is what refuses the head. §3's two-thirds share of the wool gap — the shearing
RATE, 0.929 wool per sheep-day against 1.081 — is untouched by this test and
is the half that never had a herd explanation in the first place.

## 4b. A second paired test — `ANIMAL_SAME_DAY_ON`, and why it is a no-op

The mechanism §3 names is one line deep, so it was built and measured inside
the box rather than left as a recommendation. `ANIMAL_SAME_DAY_ON`
(`plan.py:1747`, default OFF, `:7337`) adds every animal harvest the route
REACHES to the day's last lot, exactly as `SAME_DAY_FERT_ON` does for
fertilizer — the same offer `BANK_BEFORE_LOT_ON` already makes for whatever
the excursion banks (`bl_gain`, animal tiles included), widened from
`bank_mask` to `covered`.

| arm | ours | Δcoins vs B (t) | Δmargin vs B (t) | ΔWOOL | ΔEGG | ΔMILK | wool units | flips +/- |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **B** (68 band) | 104,092 | — | — | — | — | — | 116.4 | — |
| **animal_sd** (68 band) | 104,098 | **+6 (+0.3)** | -44 (-2.2) | +28 | +22 | +4 | **117.4** | +0/-2 |
| **B** (12 ymg_aq) | 93,127 | — | — | — | — | — | 121.7 | — |
| **animal_sd** (12 ymg_aq) | 93,130 | **+3 (+1.0)** | -3 (-2.3) | +0 | +8 | -5 | **121.7** | +0/-0 |

**The row was never the constraint.** The offer lands on **one extra wool unit
per board** on the band and **zero** on the ymg set; every product is inside
±40. The unit test proves the row is emitted (15 wool on turn 18 from three
ready fleeces, where OFF emits nothing), so the ask is being CLIPPED: a SELL
is clipped to the shed unit by unit, and at turn 18 the fleece is still with
the hand that took it. Animal yield reaches the shed at `_end_of_day` unless
the route walks a DROP or the excursion banks it — and `BANK_BEFORE_LOT_ON`'s
`bl_gain` already sells the fleeces that ARE banked.

So the wool sale latency is a **route** property, not a sale-row property, and
the SELL side of this family is now closed from both ends: §2 says the
allocator's placement of dawn stock is right, §4b says the rows for mid-day
stock are already there and empty.

## 5. Tests

```
$ JAX_PLATFORMS=cpu python -m pytest tests/test_macro_exec.py -q
............................                                             [100%]
```

Six new (`tests/test_macro_exec.py`):

* `test_mode_lot_pins_the_whole_sale_on_one_lot` — one row, volume conserved,
  lot 1 / 2 / 3 in order, on a schedule whose every `sell_hour` is -1.
* `test_mode_lot_ignores_the_schedule_hour` — hour 23 holds the product under
  `"sell"` and changes nothing under `"lot3"`.
* `test_mode_lot_touches_nothing_but_the_sale` — unit routes byte-identical,
  HIRE/BUY_SEED/BUY_ANIMAL/BUY_LAND and total SELL volume unchanged.
* `test_sell_lot_products_restricts_the_move` — straw pinned, wheat left with
  the allocator, and the constant defaults to `None`.
* `test_mode_sheep13_is_a_windowed_sheep_floor` — `SHEEP_FLOOR_N` sheep on
  d1-3, goose/cow columns untouched, whole plan tuple unchanged on d0, d4, d20.
* `test_animal_same_day_is_off_by_default_and_offers_the_shear_when_on` — the
  switch ships OFF and the day offers the shear on NO row while it is; ON,
  three ready fleeces put 15 wool on the last lot and move no BUY row.

`test_the_default_mode_is_the_executor_the_gate_measured` gained site 8 in its
"a mode that fires no site at all" assertion.

**The wider sale path.** `test_sell_allocator.py`, `test_drop_op.py`,
`test_day29_endgame.py`, `test_animal_count_semantics.py` and
`test_macro_exec.py` all pass. `test_early_sell.py` (3) and
`test_bank_before_lot.py` (1) fail — **and fail identically on a pristine HEAD
(01b502d) copy of `plan.py` in a scratch tree**, so they are pre-existing and
not this work: both are hard-coded plan digests pinned to commit `73c5b8a`
that the planner has moved past.

**An identity leg, beyond the unit tests.** `raw_identOFF_ymg.npz` is this
tree with no switch touched at all, 12 ymg_aq boards, against the pre-existing
`S/macro_exec/raw_headOFF.npz`: **all 15 arrays byte-equal** (money, sold_np,
sold_rp, buy_np, buy_cp, shed, tiles, anim, fert, idle, nhands, hire_n, nquad,
mkt_inv, price — 31 days x 2 seats x 12 boards). The OFF path did not move.

## 6. What this says

1. **The allocator's aggregate `when` is right and its per-product `when` is
   not.** Three fixed lots all lose by thousands, and inside that loss EGG,
   FERT and STRAW each gain over a thousand coins by moving late on both board
   sets. This is the first measured, replicated slope this family has produced.
2. **The slope has a mechanism, and it is one line of code deep.** The three
   winners are the products whose stock ARRIVES mid-day, after `avail` was
   read from the hour-0 shed. Fertilizer, melon and the DROP return leg each
   have a bespoke "add it to the last lot" patch; egg, milk and wool have
   none, so every unit an animal yields today is sold tomorrow morning.
3. **The mid-day-stock rows are already there and already empty.** The one
   patch the mechanism implies (`ANIMAL_SAME_DAY_ON`) is a measured +6 (t
   +0.3): the sale row is emitted and clipped, so the constraint is the route
   that carries the fleece, not the plan that offers it.
4. **Wool is not a selling problem.** 100 % of what we shear is sold, 0.00 is
   left at the end. Any future wool lever is a HAND lever (shear rate) or an
   opening-herd lever, never a sale lever — which also means the old two-purse
   caution applies to the ledger's "-5,659 wool" in a new way: the coins are
   real but the channel named in §7 of the ledger (under-selling) is not.

## 7. Next experiment

**ANIMAL_DROP — put the fleece in the shed, not the row in the plan.** §4b
retires the obvious candidate: the last lot already offers the day's shear and
the offer is clipped, because the yield is still with the hand at turn 18.
What has never been priced is the other half — letting the ROUTE bank an
animal harvest the way `BANK_BEFORE_LOT_ON`'s excursion banks a crop one.
`bl_gain` (`plan.py:7330`) shows the wiring is already there and already
covers animal tiles; what it lacks is a reason for `_routes` to walk the
shed-adjacent DROP for a pasture rather than a wheat block. The measurement is
cheap and the upside is bounded above by §3's price trace: 8-16 coins on each
of ~30 early units per board, i.e. a few hundred coins — worth one arm, not a
campaign.

**The larger pointer is STRAW → lot 3 (+524, t +4.4).** It is the only
positive paired coin result in this report, it is a one-line change to the
allocator's press/reservation for a single product, and its problem is the
+755 the opponent takes from the same shelf. The next question is whether
straw's late lot can be taken WITHOUT handing them the early one — e.g.
lot 2 + lot 3 only, or the last-lot half of the book — which is a
`SELL_LOT_PRODUCTS`-shaped arm that costs 6 minutes.

## 8. Files

* `src/kagg3/core/plan.py` — `ANIMAL_SAME_DAY_ON` `:1747` and its block
  `:7337`, site 8 `:7101`, `SELL_LOT_PRODUCTS` `:4799`,
  `_MACRO_SHEEP`/`SHEEP_FLOOR_N`/`SHEEP_FLOOR_DAYS` `:4780-4788`,
  `_macro_window()` `:4837`, the sheep branch of `_macro_targets` `:4926`,
  windowed masks `:4949` / `:5091` / `:5671`, mode tables `:4740-4800`.
* `tests/test_macro_exec.py` — six new tests, 29 total.
* `S/sell_lot/run.py` — `S/macro_exec/run.py` with `HERE` moved (unchanged
  otherwise).
* `S/sell_lot/report_lot.py` — `report_channels.py` with the EGG/MILK
  labelling fixed (§0).
* `S/sell_lot/wool.py` — the wool anatomy over the dawn snapshots.
* `S/sell_lot/raw_{lot1,lot2,lot3}_{band,ymg}.npz`,
  `raw_{straw_lot3,egg_lot2,sheep13,animal_sd}_band.npz`,
  `raw_{sheep13,animal_sd}_ymg.npz`, `raw_identOFF_ymg.npz` (the
  byte-equality leg), and the matching `.log` / `.md` files
  (`report_lot_{band,ymg}.md`, `report_single_band.md`,
  `report_sheep13_ymg.md`, `report_animal_sd_{band,ymg}.md`,
  `wool_{band,ymg}.md`).
