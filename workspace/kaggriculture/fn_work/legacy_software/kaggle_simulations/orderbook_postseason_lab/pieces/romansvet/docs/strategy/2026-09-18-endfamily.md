# ENDFAMILY — the end-of-game ledger under the SPLIT cell, and the row it asks for, 2026-09-18

**Verdict: the VALUE ledger is EMPTY and the remaining leak is DEPTH.**
`ENDROUTE2_SPLIT_ON` banks the whole 431-coin DROPHARV ceiling — the residue
under it is **0.0 coins a board on TOPLEG2 and 6.0 on TOPLEG3** — but it sells
the day's entire late harvest through ONE row. `plan.ENDROUTE_ROW2_ON` (built,
tested, **OFF**) offers the same flat ask on turn 21 as well, and on the 28-board
retention-gated engine class it reads **+347 a board over the SPLIT cell, se 133,
t +2.60, with the rival's purse DOWN 48** — and **+738, t +6.26 over FT2**,
nearly double SPLIT's own +391.

Tools: `S/endfamily/run_ledger.sh` (the ledger, real engine, SPLIT switches on),
`S/endfamily/sweep.sh` (one knob point on the 28-board line). Switch
`plan.ENDROUTE_ROW2_ON` / `ENDROUTE_ROW2_TURN`, pins in
`tests/test_endroute_row2.py`. Branch `endfamily` off `e2split` (903bf79).

## 1. The ledger, under the SPLIT cell

`S/endroute2/measure2.py` re-run with `ENDROUTE_ON + ENDROUTE2_ON +
ENDROUTE2_SPLIT_ON`, 24 TOPLEG2 + 24 TOPLEG3 engine-class boards, shipped FT2
theta + the 6 shipped switches, everything priced at the final quote.

| rank | item | TOPLEG2 | TOPLEG3 | what it is |
|---|---|---:|---:|---|
| 1 | **produce in HANDS at d29 h22** | **1,249.8** | **1,564.8** | wheat 12.0/14.7, carrot 7.3/4.4, fertilizer 2.6/5.0, wool, milk, egg, straw, tomato — banked and **sold, through one row** |
| 2 | idle PASS unit-turns d29 | 17.2 | 14.4 | was 53.4 before ENDROUTE2 |
| 3 | idle PASS unit-turns d27 / d28 | 20.0 / 15.0 | 19.5 / 15.4 | off the terminal day, `IDLEOPS` |
| 4 | ripe PLANT tiles @ end | **0.0** | **6.0** | wheat 0.25 units, TOPLEG3 only |
| 5 | shed @ end / hands @ end / ripe ANIMAL @ end | 0.0 | 0.0 | — |

* **DROPHARV bucket B (290 a board of unsold FERTILIZER) is ZERO.** The question
  "is fertilizer not admitted as a sell product on the terminal row?" is
  answered: it is. `ENDROUTE_ASK` is a flat ask over all nine products, day 29
  DROPs 9.5-9.7 units, and the shed is empty when the game stops. No arm there.
* **DROPHARV bucket C (141 a board of ripe tiles) is 0.0 / 6.0.** The two-trip
  route harvests them. Nothing dies in hands, nothing is banked too late
  (d29 DROP/PLACE on turn ≥ 22: 2.3-2.5 ops, and they still make the row).
* d28 carries no separate leak: its dawn picture (2,872-2,936 plant +
  3,418-4,135 animal) is the day's own work-in-progress and d29 harvests it.
  d28 DROP is 0.4-0.5 unit-turns — d28 is not a drop day, and its harvest rides
  into d29's rows, which is what makes those rows deep.

**So the end-of-game VALUE axis is CLOSED: there is no unsold stock, no
unharvested tile and no uncollected animal product left to reach.** What is left
is item 1 read the other way round: 1,250-1,565 coins of produce all arriving at
the same turn, nine slots, one walk down the quote. The last lot of the game is
the deepest lot of the game.

## 2. The switch — `plan.ENDROUTE_ROW2_ON`

A **second** flat ask on `ENDROUTE_ROW2_TURN`, day 29 only, built and emitted
exactly like `endrow` (`endrow2 = endrow`, the same nine product slots in the
same order, the same `ENDROUTE_ASK`, seat-symmetric, emitted from the shared
planner). It sells what the second trip has already DROPped by turn 21, so the
turn-22 row meets a shallower shed and both rows trade nearer the top of the
book. It is an **amount**, not a price, and it stands after the day's last lot,
so it can take nothing off any earlier row.

`ENDROUTE_ROW2_TURN` = **21**. The window between the day's last lot (18) and
`ENDROUTE_TURN` (22) has exactly two free turns — 20 is `O.TURN_PRESTOCK` and 23
is the dump row — so the knob has one alternative, 19, and the sweep below is
complete.

Requires `ENDROUTE_ON`: without the turn-22 row there is no second trip to
split, and a lone row between the last lot and the end of the day is a `LOT4`,
already measured.

OFF, `endrow2` is `None`, `_market` emits the rows it always emitted and
`rollout.MARKET_TURNS` is the set it always resolved, so the champion theta
decodes byte for byte: `tests/test_endroute_row2.py` pins whole-plan sha256
digests on five boards against a pristine `git archive 903bf79 src` subprocess,
and ON it pins that days 10/27/28 are untouched and day 29 grows exactly one row.

## 3. The cells — 28-board retention-gated engine class, paired two-purse

Every cell is the SPLIT stack (FT2 + the 6 shipped switches + `ENDROUTE_ON` +
`ENDROUTE2_ON` + `ENDROUTE2_SPLIT_ON`) with one thing changed, judged against
the `e2split` rows on the same boards, same seeds, same tapes
(`S/dropharv/pooled28.py`).

| cell | change | boards | d/board vs SPLIT | se | t | ours | theirs |
|---|---|---:|---:|---:|---:|---:|---:|
| **ef_row2** | **`ENDROUTE_ROW2_ON`, turn 21** | 28 | **+347** | 133 | **+2.60** | +299 | **−48** |
| ef_row2_19 | `ENDROUTE_ROW2_ON`, turn 19 | 28 | +185 | 63 | +2.92 | +156 | −29 |
| ef_et21 | `ENDROUTE_TURN` = 21 | 28 | +234 | 153 | +1.53 | +147 | −87 |
| ef_mt7 | `ENDROUTE2_SPLIT_MAX_TURNS` 9 → 7 | 28 | +24 | 35 | +0.68 | +18 | −6 |
| ef_mv800 | `ENDROUTE2_SPLIT_MIN_VALUE` 400 → 800 | 28 | −153 | 51 | −2.98 | −135 | +17 |
| ef_t10 | `ENDROUTE2_SPLIT_TURN` 18 → 10 (lot 2) | 28 | −165 | 51 | −3.21 | −148 | +16 |

The §8.4 sweep is now closed on all three SPLIT knobs: relaxing the gates was
already worse (§8.1), **tightening `MIN_VALUE` is worse too** (−153, t −2.98),
tightening `MAX_TURNS` is flat (+24, t +0.68), and **moving the first dump to
lot 2 is worse** (−165, t −3.21). The shipped `BANK_*` values and
`SPLIT_TURN` = the day's last lot are a genuine local optimum.

`ENDROUTE_TURN` 21 is positive (+234) but noisy (sd 809) and it also shortens
`ENDROUTE2`'s turn budget by one, which is a route change, not a row. The second
row gets the same coins without giving the budget back, and gets more of them.

Against FT2 on the same 28 boards, `ef_row2` is **+738, se 118, t +6.26** (ours
+826, theirs +89), against SPLIT's own **+391, t +2.40**.

## 4. POOLED169

`S/e2split/run_pool.sh efr2 ",ENDROUTE_ROW2_ON=True"` — LIVEC-H30 / LIVEC-H30B /
NEXT30 / BAND180, this worktree's src, shipped FT2 theta, read by
`S/endroute2/pooled169.py`.

| leg | boards | d/board | sd | se | t | ours | theirs | win base→cand |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **vs the SPLIT cell** (`e2sp`) — **the increment** | | | | | | | | |
| LIVEC-H30 | 30 | +133 | 286 | 52 | +2.55 | +110 | −23 | 86.7 → 86.7 % |
| LIVEC-H30B | 30 | +117 | 244 | 45 | +2.62 | +81 | −36 | 90.0 → 90.0 % |
| NEXT30 | 30 | +210 | 456 | 83 | +2.52 | +146 | −64 | 86.7 → 86.7 % |
| BAND180 | 79 | +110 | 209 | 23 | +4.70 | +72 | −38 | 83.5 → 83.5 % |
| **POOLED169** | **169** | **+133** | 286 | **22** | **+6.05** | +93 | **−40** | 85.8 → 85.8 % |
| **vs FT2** | | | | | | | | |
| LIVEC-H30 | 30 | +542 | 607 | 111 | +4.89 | +611 | +69 | 86.7 → 86.7 % |
| LIVEC-H30B | 30 | +711 | 674 | 123 | +5.78 | +790 | +78 | 90.0 → 90.0 % |
| NEXT30 | 30 | +395 | 552 | 101 | +3.92 | +491 | +95 | 86.7 → 86.7 % |
| BAND180 | 79 | +475 | 530 | 60 | +7.95 | +553 | +79 | 82.3 → 83.5 % |
| **POOLED169** | **169** | **+514** | 579 | **45** | **+11.54** | +594 | +80 | **85.2 → 85.8 %** |
| vs E + E2 (`er2_on`) | 169 | +378 | 548 | 42 | +8.97 | +297 | −82 | 85.8 → 85.8 % |
| vs ENDROUTE alone (`er_on`) | 169 | +489 | 585 | 45 | +10.86 | +569 | +80 | 85.2 → 85.8 % |

One board flips and it flips **to us** — 107248812, the same board §8's SPLIT
flipped, now won from the FT2 baseline. **Every leg is positive on both
comparisons and nothing is anywhere near negative**; the weakest increment leg
is BAND180 +110 at t +4.70 and the weakest by t is NEXT30 +210 at t +2.52.

The whole family on one pool, for the record:

| arm | boards | d vs FT2 | se | t | ours | theirs |
|---|---:|---:|---:|---:|---:|---:|
| ENDROUTE alone | 169 | +25 | 3 | +8.58 | +25 | +0 |
| E + E2 | 169 | +136 | 47 | +2.92 | +297 | +161 |
| E + E2 + SPLIT | 169 | +381 | 44 | +8.74 | +501 | +120 |
| **E + E2 + SPLIT + ROW2** | 169 | **+514** | 45 | **+11.54** | +594 | +80 |

## 5. Verdict

**`ENDROUTE_ROW2_ON` PASSES the stated ship criterion on every clause.** The
increment over the SPLIT cell is **+133 a board at t +6.05** on POOLED169, no leg
is at t ≤ −2 (the worst leg is +110 at t +4.70), and it takes the increment
**off the rival**: `theirs` −40 against SPLIT, and the family's gift on the whole
pool falls from +120 to **+80** while our own purse rises from +501 to +594.

And the stack it completes clears **§115b** for the first time in the
end-of-game family: `E + E2 + SPLIT + ROW2` is **+514 a board on POOLED169 at
t +11.54** against FT2, over the +450 bar with t ≫ 3, win rate 85.2 → 85.8 %,
one flipped board and it flips to us.

It is still a two-purse trade rather than ENDROUTE alone's free coin — the
rival's purse is +80 against FT2, not 0 — but it is the *least* gifting member of
the family that is also the largest, and the only direction in which the gift has
ever gone DOWN while our purse went up.

**Defaults are unchanged and nothing shipped here**: `ENDROUTE_ROW2_ON`,
`ENDROUTE2_SPLIT_ON`, `ENDROUTE2_ON` and `ENDROUTE_ON` are all `False` on the
`endfamily` branch, no tarball was built and nothing was merged. The ship
decision is the same one §8.4 raised, now on a bigger and cleaner arm.

**What is closed by this box**: the end-of-game VALUE ledger (no stock, no ripe
tile, no animal product, no cash-convertible residue left — §1), the three SPLIT
knobs (§3, all four sweep points at or below the shipped values), and
`ENDROUTE_ROW2_TURN` (19 and 21 are the only free seats and 21 wins). **What is
open**: the d29 idle PASS (14-17 unit-turns) and whether a third late row is
worth the fourth free turn the day does not have.
