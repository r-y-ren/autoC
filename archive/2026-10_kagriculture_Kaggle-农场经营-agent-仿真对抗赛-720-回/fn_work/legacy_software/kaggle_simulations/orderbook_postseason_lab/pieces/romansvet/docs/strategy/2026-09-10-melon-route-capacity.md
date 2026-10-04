# 2026-09-10 — is the d10 melon pot physically reachable for our route model?

**Review correction, September 13:** the historical numbers below are retained
as reported; the raw `S/melonroute` directory is absent from this checkout.
72 units / 17,440 implies **242.22**, not 233. Comparing that baseline receipt
with 12,537 gives **4,903**, not approximately 4,200. Neither subtraction is a
controlled estimate of deposit timing: the table reports the opponent earning
15,917 in the modified arm, versus 17,440 in the baseline. Thus “identical in
all three arms” cannot describe actual receipts. The old forced substitutions
remain negative evidence; the final claim that *any* melon arm must be additive
is broader than those experiments establish. See the
[current experiment review](2026-09-13-melon-sigma-reachability.md).

One pinned board, **107056463** (XJHya233 1827, seed 4674845, tape at seat 0), theta
`flow172_g170c`, patched-copy sim with per-product per-turn sale accounting
(`S/melonroute/`). **Sim, descriptive.** Turn `h` = sim turn (engine hour h+1).

## 1. What the archive already answered

* `MELON_OPEN_ON` alone: band6 54.2 → **15.1 %**, −17,554 t −12.8 (2026-09-04-verdicts:268).
* `MELON_OPEN`+`MIDDAY_PLACE_V2`: band −18,561 t −11.3, 4-opp −17,241 — *even with 60/72 units
  reaching the pot* (verdicts:4). MELON_D10/D10B: 17.2 % / **13.0 %**; the 12-tile plate
  displaces our **animal line** (COW 3→1, egg 2/day vs 5-12) → +31 k price gift by d27 (:376,:386).
* Pinned judge, 130 tapes: 12 tiles → **1.9 %**, −19,557; 8 tiles → 3.8 % (2026-09-09-verdicts:132).
* **"12/72 units reach the pot"** = the *default* build, 2026-09-05 05:47Z (:165). The forced
  builds were later measured at 54/72 (:172) and 60/72 at 185.8 vs their 60 at 246.4
  (`plan.py:846-856`, `S/mp2/verify3.sh`). Route capacity was never the open question.

## 2. d10-11 melon, hour by hour (this board)

Clone (identical in all three arms): harvests 12 tiles at h5-h9, then **PLACE+SELL pairs**
h9-h15 — 6 @270, 24 @252, 12 @244, 6 @239, 6 @234, 6 @230 = 60 u / 14,797, plus 12 @220 at
**d11 h0**. Total **72 u / 17,440, avg 233, 7 rows.**

| arm | our d10-11 melon | rows that filled | avg price | theirs |
|---|---|---|---|---|
| base | **0 u / 0** (1 melon tile at d10; our 84 u go from d18) | 0 | – | 72 u / 17,440 |
| `MELON_OPEN_ON` | 71 u / **11,638** | t15 12@222, t18 24@197, d11t1 35@121 | 164 | 72 u / 16,799 |
| +`MIDDAY_PLACE_ON,MIDDAY_PLACE_V2_ON` | 72 u / **12,537** | t11 6@244, t15 6@221, t18 **54@171**, d11 6 | 174 | 72 u / 15,917 |

## 3. The binding constraint

Not sell rows (`SELL_TURNS` 3/10/18 + `MELON_LOT_TURNS` 11/13/15 = 6 a day vs their 7), not the
shed (`SHED_CAPACITY` 100 > 72), not hands (both seats ~22 hires by d4), not harvest cadence
(all 12 tiles are cut by h13 in both forced arms). It is **deposit turn**: a harvest lands in the
*unit* (`sim/units.py`, `eod.py` drop at end of day), and only an excursion banks it.

* `MELON_OPEN` alone: first DROP at **t14**. The t11 and t13 melon lots ask 24 units each and
  **sell zero into an empty shed** (inv 47/53, shed 0) — 48 units of ask wasted, and 35 units
  ride to d11 h1 at **121**.
* `MIDDAY_PLACE_V2` fixes the chain and the route order (`plan.py:817-880`): 66 of 72 sell the
  same day. But only **12 units bank before t16**; the other **54 clear in one line at t18 @171**,
  behind the clone's whole ladder. Cost of the timing, this board: 72 u at 174 vs their 233 =
  **≈4,200 coins**, and it walks the quote so they lose 1,523 too.

## 4. Verdict

**Reachable — with `MIDDAY_PLACE_V2_ON` (`plan.py:922`, the melon route tier + the
`MIDDAY_PLACE_V2_TURN` deadline).** 66/72 units bank and sell on d10 here; at d11 eod the arm is
+7,993 own / −996 theirs against base. The route model is **not** the wall.

The pot is not the win. The second dumper is paid ~174 against 233, and five measured builds lose
15-20 k over d12-29 because the 12 tiles come out of our wheat/animal denial. Any melon arm must
be **additive** to the d0 board, not a swap — the FORWARD_ADMIT/tile-budget path, not this switch.
