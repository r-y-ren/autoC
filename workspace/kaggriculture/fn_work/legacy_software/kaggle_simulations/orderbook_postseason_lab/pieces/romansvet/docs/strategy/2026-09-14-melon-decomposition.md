# 2026-09-14 — why the forced day-0 melon opening loses: a per-product ledger

**Sim, descriptive, paired, CRN.** 68 pinned-town boards (40 TOPB2 + 28 LIVE-C
hold-out), theta B = `flow193_g100_hr`, seven switch arms, action-replay opponent
seat. No engine games, no training, no `src/` edits. Tools:
`S/melon_decomp/{ledger,report,summary,validate}.py` (a copy of the
`S/bandledger` per-product sale ledger wired onto the `S/simscreen` board lists;
`S/simscreen` itself untouched). Raw: `S/melon_decomp/raw_<arm>.npz`.

**Validation.** Arm B reproduces `S/simscreen/topb2_40.csv` (`flow193_g100_hr`)
on **40/40 boards, max |Δmargin| = 0 coins** (`validate.py`). Those simscreen
rows were themselves checked against the engine at sign 6/6, max d error 45
coins (`2026-09-11-simscreen-topb2.md`), so a row here is an engine row up to
that known error. Resolution: ±400 coins/board; every effect below is 9–70×
that.

## 1. Arms

`MELON_OPEN_ON` asserts against `BANK_BEFORE_LOT_ON` (plan.py:2483, one
excursion clock per block), so every melon arm runs on the shipped `hr`
composition **minus** `BANK_BEFORE_LOT_ON`. `Bnb` is that control: it is worth
−64 ± 943 coins (t −0.56), i.e. the confound is nil and the melon deltas below
are the melon's own.

| arm | switches on top of `OPEN_PUMP_ON,TAIL_FILL_ON,HIRE_ROW_ON` |
|---|---|
| B | `+BANK_BEFORE_LOT_ON` (the shipped `hr` string, reference) |
| Bnb | — (bank switch off; the melon arms' true control) |
| M12 | `MELON_OPEN_ON` (tiles 12, the default) |
| M8 / M4 | `MELON_OPEN_ON, MELON_OPEN_TILES=8 / 4` |
| M12E | M12 `+ MELON_LOT_EARLY_ON` (melon rows to turns 6/7/8) |
| M12P | M12 `+ MIDDAY_PLACE_ON, MIDDAY_PLACE_V2_ON` |

`MELON_LOT_EARLY_ON` + `MIDDAY_PLACE_V2_ON` are **not** compatible in substance:
`MIDDAY_PLACE_V2_TURN = O.SELL_TURNS[-1]` (plan.py:932) is *behind* the early
lots, so the V2 deposit would bank melon after the rows that sell it. Arm 5 is
run without `MELON_LOT_EARLY_ON`.

## 2. Arm table (paired vs B)

| arm | boards | win % | margin | d margin | sd | t |
|---|---|---|---|---|---|---|
| B | 68 | 42.6 | +101 | — | — | — |
| Bnb | 68 | 39.7 | +37 | −64 | 943 | −0.56 |
| **M12** | 68 | **2.9** | −23,416 | **−23,517** | 9,786 | −19.8 |
| M8 | 68 | 2.9 | −16,725 | −16,826 | 6,722 | −20.6 |
| M4 | 68 | 20.6 | −8,999 | −9,100 | 6,074 | −12.4 |
| M12E | 68 | 2.9 | −23,509 | −23,610 | 9,810 | −19.9 |
| M12P | 68 | 2.9 | −28,062 | −28,163 | 11,051 | −21.0 |

Per board set (same ordering, same sign): TOPB2 (40) B win 32.5 %, M12 −20,512
t −12.1, M8 −15,143, M4 −8,384, M12P −25,849. LIVE-C (28) B win 57.1 %, M12
−27,811 t −23.4, M8 −19,231, M4 −10,123, M12P −31,467. The loss is ≈ −2,000
coins per melon tile and roughly linear: −2,275/tile at 4, −2,103 at 8,
−1,960 at 12.

## 3. The coin decomposition

Δmargin = [our melon + our other − our spend + our residual] − [same for them].
The opponent is a byte-exact action replay, so **every delta on their side is a
price effect of our supply**, never a behaviour change. Coins per board, ALL 68:

| arm | d margin | (b) melon race | (a) displacement | (c) cash/purse |
|---|---|---|---|---|
| M4 | −9,100 | **+1,179** | **−10,214** | −66 |
| M8 | −16,826 | **+2,163** | **−17,899** | −1,091 |
| M12 | −23,517 | **+3,016** | **−26,647** | +114 |
| M12E | −23,610 | +2,921 | −26,646 | +116 |
| M12P | −28,163 | **+4,897** | **−33,495** | +436 |

(b) = our melon revenue delta + the melon revenue we take off them;
(a) = our non-melon revenue delta + the non-melon revenue they gain;
(c) = market spend and residual (wages/upkeep/land) on both sides. The three
columns sum to the margin to within 1 coin on every arm.

**The melon race is won, and it is small.** M12 sells 72 melon units on d10–11
that B never sells, worth +12,771 in d10–14; it gives back −11,366 of B's own
later melon, nets **+1,405**; the denial it buys off the clone is **+1,611**
(their d10 price 246 vs 249, their d11 price 173 vs 223). Total prize
**+3,016**, i.e. **13 %** of the loss and of the opposite sign.

**The bill is displacement, and it is two-sided.** M12 costs us −5,491 of our
own non-melon revenue and hands the clone **+21,156** — 90 % of the whole loss
is the opponent's receipts rising because our other lines stop gluting the
shared pot.

**Cash starvation on d0–5 is not the mechanism.** Our money at dawn d1…d5 moves
+140, +198, −13, +203, −596 under M12 (M4: +260, +290, +147, +229, −222). The
day-0 tile total is preserved exactly (19 tiles in every arm), season market
spend moves +579, and the (c) column is ≤ 1.1k on every arm. **UNVERIFIED:**
`nhands` reads 0.00 at dawn for both seats in every arm (the field is empty at
dawn in this state), so "hands at d10" could not be measured here.

## 4. M12 per-product ledger vs B (coins/board, [units])

| seat | product | d0-9 | d10-14 | d15-29 | season |
|---|---|---|---|---|---|
| ours | WHEAT | −650 [−21.6] | −534 [−15.3] | −1,728 [−43.2] | **−2,911 [−80.2]** |
| ours | CARROT | −825 [−24.9] | +41 [+1.1] | −675 [−20.7] | **−1,459 [−44.5]** |
| ours | TOMATO | 0 | 0 | +485 [+6.9] | +485 [+6.9] |
| ours | STRAWBERRY | 0 | −1,290 [−6.2] | +3,642 [+6.0] | +2,351 [−0.1] |
| ours | MELON | 0 | **+12,771 [+72.0]** | **−11,366 [−25.7]** | +1,405 [+46.3] |
| ours | EGG | +1 | −274 [−5.3] | −368 [−9.1] | −642 [−14.4] |
| ours | MILK | −1,000 [−6.0] | −1,455 [−11.4] | +1,959 [−23.0] | −496 [−40.4] |
| ours | WOOL | −1,007 [−5.0] | −1,673 [−8.9] | +1,819 [−1.5] | −861 [−15.4] |
| ours | FERTILIZER | −1,543 [−17.8] | −783 [−12.4] | +368 [−9.1] | −1,958 [−39.2] |
| **ours** | **ALL SALES** | **−5,024** | **+6,803** | **−5,865** | **−4,086** |
| theirs | WHEAT | +2 | +35 | +219 | +256 [−0.6] |
| theirs | CARROT | 0 | +2 | +508 | +511 [−0.1] |
| theirs | TOMATO | 0 | 0 | −118 | −118 |
| theirs | STRAWBERRY | 0 | +2 | **+7,678 [+0.2]** | **+7,680** |
| theirs | MELON | 0 | −813 | −799 | **−1,611 [+0.0]** |
| theirs | EGG | 0 | +1 | +71 | +71 |
| theirs | MILK | +4 | +792 | **+6,738 [+0.1]** | **+7,533** |
| theirs | WOOL | +33 | +398 | +2,631 [−0.4] | **+3,062** |
| theirs | FERTILIZER | +128 | +340 | +1,692 [+0.3] | **+2,160** |
| **theirs** | **ALL SALES** | **+167** | **+758** | **+18,620** | **+19,545** |

Their unit counts are unchanged to ±0.6 (fixed tape) — **+19.5k of receipts on
the same units**, 95 % of it in d15-29, all of it price. Our own lost units are
80 WHEAT, 44 CARROT, 40 MILK, 39 FERTILIZER, 15 WOOL, 14 EGG.

## 5. What the plate actually displaces

| covariate (mean over 68 boards) | M12 | M8 | M4 | B |
|---|---|---|---|---|
| day-0 plant WHEAT / CARROT / MELON | 7 / 0 / 12 | 11 / 0 / 8 | 11 / 4 / 4 | 11 / 8 / 0 |
| tiles planted d0 (total) | 19 | 19 | 19 | 19 |
| COW at d10 | 3.32 | 4.62 | 5.38 | 6.15 |
| SHEEP at d10 | 0.06 | 0.21 | 0.68 | 3.26 |
| GOOSE at d10 | 0.84 | 0.88 | 1.07 | 1.71 |
| STRAWBERRY tiles at d10 | 19.85 | — | — | 26.29 |
| idle tiles at d10 | 5.51 | 2.79 | 4.07 | 2.68 |
| our MELON units d10 @ price | 35.9 @ 216 | 26.1 @ 222 | 12.0 @ 227 | 0 |
| our MELON units d11 @ price | 35.6 @ 140 | 21.9 @ 171 | 12.0 @ 203 | 0 |
| their MELON units d10 @ price | 50.9 @ 246 | 50.9 @ 247 | 50.9 @ 249 | 50.9 @ 249 |
| their MELON units d11 @ price | 10.1 @ 173 | 10.1 @ 186 | 10.1 @ 208 | 10.1 @ 223 |
| MELON quote at dawn d11 | 189 | 202 | 219 | 233 |

Our realised melon price is **178** over the 72 units (216 on d10, 140 on d11)
against their **234**; the archive's "we sell at ~174 vs their ~233" is
reproduced across 68 boards. The gap is worth ~4.0k of gross melon revenue —
but taking it back would not change the verdict, because the whole melon leg is
only +3.0k of a −23.5k hole.

The animal line is the thing that dies, exactly as `2026-09-06 06:20Z` reported
(COW 3→1 there): **COW 6.15→3.32, SHEEP 3.26→0.06, GOOSE 1.71→0.84**. Note
SHEEP collapses even at **4** tiles (3.26→0.68) and even when the day-0 wheat is
untouched (M8/M4 take all their tiles from carrot), so the mechanism is the tile
and route budget the melon plate occupies from d0 to d10, not the day-0 wheat
split and not the purse.

## 6. Better melon extraction makes it worse

M12E (`MELON_LOT_EARLY_ON`, rows at turns 6/7/8) is **inert**: −93 coins vs M12,
melon revenue +12,721 vs +12,771. M12P (`MIDDAY_PLACE`+V2) does what it claims —
our melon revenue +904 better, the clone's melon −977 further down, prize
+4,897 vs +3,016 — and loses **4,646 more**, because the excursion takes another
−3,538 out of our own non-melon lines (WHEAT −96 units, CARROT −62, EGG −36) and
hands the clone another +3,310. **Every coin of melon extraction bought so far
has cost more than a coin of displacement.**

## 7. Conclusion, in coins

For the default 12-tile forced opening (−23,517/board, 2.9 % win rate):

* **(a) displacement: −26,647** (113 % of the loss) — −5,491 our own lines,
  −21,156 handed to the clone as price on unchanged units.
* **(b) melon price/timing: +3,016** (−13 %) — the opening *wins* the melon race
  in coins even at 178 vs 236 a unit. Melon price is not the defect.
* **(c) cash starvation d0-5: ≈ 0** (+114; dawn cash within ±600 coins, tile
  total identical). Refuted as a mechanism on these boards.

**A non-displacing melon build must be additive in tiles AND in route time, and
must preserve, per board:** ~2.8 COW, ~3.2 SHEEP, ~0.9 GOOSE standing at d10
(they carry 40 MILK, 15 WOOL, 14 EGG, 39 FERTILIZER units of season supply),
~80 WHEAT and ~44 CARROT units of season supply, and ~6.4 strawberry tiles at
d10. Those lines are worth **26.6k a board** — 5.5k of our own receipts and
**21.2k of price denial**, of which strawberry +7.7k, milk +7.5k, wool +3.1k and
fertilizer +2.2k are the clone's four biggest gains. Against that the melon pot
is worth **+3.0k gross at 12 tiles** (+1.2k at 4 tiles), so a build that
preserves every displaced line and adds 12 melon tiles on new land has a
ceiling near +3.0k/board before paying for the land, the seed (960 coins) and
the crew turns — and the archive prices that land+seed at 1,960 of a 3,000-coin
day-0 purse (`2026-09-11-additive-melon.md`). **Nothing here recommends a
forced-plate arm.** The measurement that would matter is whether ~12 tiles of
melon can be added with **zero** change to the animal count at d10; this ledger
gives the exact per-line budget such an arm has to hold.

## 8. Limits

* Sim, not the engine. Validated to the coin against the simscreen TOPB2 rows
  (40/40), which track the engine at |Δd| ≤ 45 coins on 6 thetas; that check
  covers thetas, **not switches** — no engine leg of a melon arm was run here.
* One theta (B). The opponent seats are pinned action tapes: a population the
  20 TOPB2 + 14 LIVE-C tapes do not cover is outside this measurement.
* `buy_cp` attributes market spend to the item whose shed count rose; land,
  wages and upkeep fall into the residual column (≤ 853 coins on every arm).
* Melon prices are per-board means over boards where that seat sold melon that
  day (n given in `S/melon_decomp/report.py` output), not unit-weighted.
