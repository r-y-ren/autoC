# Candidate B vs the top tier — per-day paired coin ledger (2026-09-11, S/topledger/)

**Question.** B (`artifacts/kagg2_games/thetas/flow193_g100_hr.npy`, live sub 56161192) wins 32.5 %
of TOPB2. WHERE do the coins go against the top tier, and which part of the gap can a theta reach?

**Tool.** `S/topledger/ledger.py` — the `S/simscreen/screen.py` sim (pinned-town action tapes,
`shop_crn`, shipped `hr` switch string, frozen `boards_topb2.json`), with the day scan kept and a
per-seat row scanned out of every day: money, crop tiles, idle tiles, cumulative units sold / sale
coins / SELL rows (`State.sold_n/.sold_rev/.sold_rows`, written under `run_day(day_metrics=True)`;
the action-tape seat passes through `_market_turn` so **both** purses are measured), hands,
quadrants, shed units and shed per item, crop tiles per crop.
**Reproduction:** 40/40 TOPB2 boards give win 32.5 % / mean margin −1,472, digit-identical to
`S/simscreen/topb2_40.csv` and to the engine leg it reproduces (§50, ≤45 coins) — `day_metrics`
does not move the trajectory. Sets: TOPB2 (20 pinned tapes × 2 seats, 28 distinct games) and the
10 fresh top-tier pinned tapes 1067968xx-1068038xx × 2 seats (13 distinct games), win 70.0 %,
+529. Analysis `S/topledger/analyze.py`; raw `S/topledger/{topb2_B,fresh_B}.npz`.

## Already established (cited, not re-derived)

`2026-09-10-topb-loss-anatomy-g1000-B.md` (d10-14 melon dump is a flat tax, separation is d15-29
and it is the opponent's purse), `2026-09-11-top50-patterns.md` (T0a public band clone: 12 melon
d0, 60 dumped d10 @217, one hire/day, land d6+d11), `2026-09-10-livec-loss-anatomy.md` /
`-planner-ceiling-B.md` (top files 389 sell rows of 3.95 u to our 152 of 9.39 u),
`2026-09-09-forced-opening-ramp.md` (forcing the top opening loses 94→26 % because hire
enumeration prices hands on TODAY's tasks), `dominant-strategy-2026-09-03` (melon pot race; three
native harvest-day builds lost — 12/72 units reach the pot, the route model cannot PLACE mid-day).

## 1. Where the margin opens (cash margin us − them, end of day, mean/board)

TOPB2 (n=40):

| day | 0 | 4 | 8 | **10** | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | +106 | +712 | +103 | **−10,000** | −13,810 | −17,454 | −16,846 | −13,564 | −8,677 | −6,256 | −5,313 | −2,101 | −2,215 |
| wins | +108 | +833 | +175 | −11,490 | −15,105 | −16,845 | −15,931 | −13,023 | −7,245 | −2,952 | +787 | +6,493 | +8,614 |
| losses | +104 | +653 | +69 | −9,283 | −13,186 | −17,747 | −17,287 | −13,824 | −9,366 | −7,847 | −8,251 | −6,240 | −7,428 |

Fresh 10 (n=20) is the same shape: +101 at d8, −9,698 at d10, trough −18,392 at d14, −1,481 at d28.

**The hole opens on d10 and deepens to d14; every day from d17 on is ours.** It is consistent:
all 28 TOPB2 games and all 13 fresh games have a d10-14 cash hole between −14.5k and −29.1k
(mean −20.7k), and 24 of 28 / 12 of 13 have a positive d15-29 recovery. Margin ≈ (a nearly
constant d10-14 tax) + (a recovery that ranges −5.0k to +62.0k) — **the variance is all in the
recovery, not in the hole.**

## 2. Revenue / units / price per unit by band (mean per game)

TOPB2 | us rev | op rev | gap | us u | op u | us c/u | op c/u | us rows | op rows | us u/row | op u/row
---|---|---|---|---|---|---|---|---|---|---|---
d0-9 | 14,131 | 14,284 | −152 | 220.4 | 174.7 | 64.1 | 81.8 | 22.4 | 49.1 | 9.86 | 3.56
**d10-14** | 9,980 | 29,510 | **−19,530** | 104.6 | 230.1 | 95.4 | 128.3 | 18.1 | 38.7 | 5.79 | 5.95
d15-21 | 51,711 | 44,019 | +7,692 | 437.6 | 444.5 | **118.2** | 99.0 | 43.1 | 71.9 | 10.14 | 6.18
d22-29 | 50,160 | 44,344 | +5,816 | 634.9 | 726.2 | **79.0** | 61.1 | 59.8 | 116.5 | 10.63 | 6.23

Fresh 10: d0-9 −808, **d10-14 −20,096**, d15-21 +7,692, d22-29 +7,875; us c/u 109.1 / 74.3 vs
their 93.0 / 58.9. **B already realises a higher price per unit than the top tier in every late
band on both families** — the g1000-era "we match volume and lose price" read does not hold for B.

Win/loss decomposition of the band gap:

| band | TOPB2 WIN gap | TOPB2 LOSS gap | swing | fresh WIN | fresh LOSS | swing |
|---|---|---|---|---|---|---|
| d0-9 | +594 | −512 | +1,106 | −547 | −1,415 | +868 |
| **d10-14** | −19,483 | −19,553 | **+70** | −20,092 | −20,103 | **+11** |
| d15-21 | +9,449 | +6,846 | +2,603 | +12,049 | −2,475 | +14,524 |
| d22-29 | +15,981 | +922 | +15,060 | +7,947 | +7,707 | +240 |

The d10-14 hole is **the same coin for coin on the boards we win** (swing +70 / +11): a tax, not a
discriminator — the g1000 finding reproduces exactly at B. All of the separation is d15-29
(swing +17,663 TOPB2, +14,764 fresh), and two thirds of it is **their** purse: their d15-29
revenue is 75.1k on wins vs 94.8k on losses (+19.7k) while ours moves 100.5k → 102.5k (+2.1k);
fresh, theirs +9.3k, ours −5.2k.

## 3. Board and labour state (us | them)

| metric | d5 | d10 | d15 | d20 | d29 |
|---|---|---|---|---|---|
| crop tiles | 32.0\|18.4 | 47.8\|40.5 | 56.9\|56.4 | 53.7\|57.2 | 7.4\|4.0 |
| idle tiles | 11.4\|7.5 | 11.8\|1.9 | 1.4\|1.7 | 4.6\|2.3 | 50.9\|55.8 |
| quadrants | 2.0\|1.3 | 3.0\|2.4 | 3.0\|3.0 | 3.0\|3.0 | 3.0\|3.0 |
| shed units | 8.0\|14.4 | 27.1\|63.9 | **85.0\|61.7** | 82.2\|72.2 | 7.5\|1.0 |
| hands (d29, pre-eod) | | | | | 9.1\|11.1 |

Melon tiles d10 4.3\|3.1, d20 **10.4\|0.7** — B plants melon late and sells it into the market
their d10 dump has vacated (our d15-21 118 c/u). Shed at d14: ours 36.8 wheat + 16.4 fertilizer +
8.0 wool; theirs 30.8 + 13.4 + 1.6. Hands read 0 at every day boundary because the crew is paid
off in `end_of_day` — only d29 (no eod) is a real reading. (Animal columns read 0: the driver
counted `occ == N_CROPS + a`, but `State.occ` holds the bare animal index — a one-line fix in
`S/topledger/ledger.py:day_row`, re-run costs 5 min; herd facts here come from the archive.)

## 4. The three mechanisms

### M1 — the d10-14 melon pot: −19.5k/game (TOPB2), −20.1k (fresh). STRUCTURAL.

Their 230 units at 128 c/u in five days against our 105 at 95. Flat across wins and losses
(swing +70 / +11), so it buys no board on its own — but it is the whole gross-revenue deficit
(season: us 125,982, them 132,157). To contest it we must hold 12 melon tiles from d0 and deposit
~60 units before the d10 h0 lot. Two independently measured walls: hire enumeration prices hands
on **today's** tasks and melon emits none for six days (`plan.py:3499-3531`; forced opening
94→26 %), and the deposit chain, not the sell rows, is the cap — 12 of 72 units reach the pot,
`MIDDAY_PLACE_V2` −18,561 t −11.3 (`2026-09-10-chain-optimisation-review-B.md`). Not reachable by
any theta setting: the ES can move the crew ramp (the `g11` `macro.forward_days` gene,
`plan.py:3408`, which rules while `FORWARD_ADMIT_ON=False`) but it cannot move a unit from a tile
to the shed inside a day. **B already prices this correctly** by harvesting melon into the
post-dump market instead.

### M2 — the d15-29 recovery, and it is the opponent's late realised price: ±17.7k/game. NOT THETA-REACHABLE.

The discriminator. Their d15-29 coins/unit is 80.5 on the boards we lose and 65.3 on the boards we
win (r(their c/u, margin) **−0.49**) at flat volume (their units r +0.23; ours r +0.16). Our own
late revenue barely moves (r(our c/u) +0.13). The per-board split makes it plain: recovery +62.0k
where their basket clears at 54 c/u (107466019), −2.3k where it clears at 93 (107460187).
The planner cannot see this by construction — `plan.py:1457-1479`, **"THE HOLE"**: *"the genes get
two scalars per product, `hold` and `press`, and `press` is a straight line in the lot index — it
cannot say 'wheat is fine all game but on day 21 the other seat dumps a hundred units into lot
3'"*. No theta weight expresses opponent supply; the only expression in the tree is the OFF switch
`OPP_SUPPLY_ON` (`plan.py:1507`) + `OPP_SUPPLY_SCALE`/`_PATH`.

### M3 — carry and slice: our shed holds 85 units at d15 to their 62, and we file 6.9 SELL rows/day to their 12.6. PARTLY THETA-REACHABLE.

d15-29: 103 rows of 10.1-10.6 u against 188 of 6.2 (the 152-vs-389 season figure, reproduced at B).
Our realised price falls 118 → 79 c/u from d15-21 to d22-29 while 635 units leave in the last
band, and that last band is exactly where the loss boards' deficit sits (WIN gap +15,981 vs LOSS
+922). Lot **sizing** is `sell.allocate`'s greedy over the learned `hold`/`press` scalars
(`plan.py:1457`, `:6597`) — inside theta, and already under ES pressure. Lot **turns** are planner
constants (`ops.SELL_TURNS = (3,10,18)`, `MELON_LOT_TURNS = (11,13,15)`) and the widest setting is
already refuted: `EARLY_SELL_MODE "B"` (all six market turns) −7,976 TOPB2 t −9.8 (§47), and the
per-product sell-hour map "does not exist" (`2026-09-10-sell-hour-headroom.md`). So the row-count
half is closed; only a late-band-only split is untested.

## 5. Ranked tests

**T1 (recommended) — confirm `OPP_SUPPLY_ON` on pinned top-tier boards.** The −2,972 / −3,616 that
closed it (2026-09-05) was measured on **drawn** band6 boards, which `tape-fidelity-2026-09-11`
voids (drawn towns cripple open-loop opponents); the only pinned read is
`2026-09-09-switch-sweep.md:119` — HELD42 **+617 t +2.54, +6 flips / −0 drops**, LEG20 +47,
LOSS12 −733, with the author's own note "worth one confirmation leg if a slot is free". It is the
only expression of M2 in the tree. *Change:* `OPP_SUPPLY_ON=True, OPP_SUPPLY_SCALE=1.0,
OPP_SUPPLY_PATH=artifacts/opp_supply/S_pop.npy` appended to the shipped `hr` switch string, theta
B unchanged. *Legs:* TOPB2 40 + LIVEC-H30 + LIVEC-H30B, paired against B's own csvs (screen first
on `boards_topb2.json` + `boards.json`, ~250 s, refuse at 20-board |t| ≳ 2.5 per §50).
*Falsifies:* TOPB2 Δ ≤ 0, or any LIVE-C leg down, or the opponent's d15-29 c/u on the loss boards
unchanged (re-run `S/topledger/ledger.py` and read it — the mechanism claim, not just the margin).
*Predicted signature if real:* their d15-29 coins/unit on our loss boards falls from 80 toward 65
and our last-band c/u rises from 79; our own units and rows barely move.

**T2 — late-band-only lot split (d22-29).** M3's untested half: our price collapses 118 → 79 in a
band where we move 635 units in 60 rows. *Change:* one constant — a fourth sell lot for days ≥ 22
only (`ops.SELL_TURNS` is global today; the day-conditional form does not exist and would be a
build). *Legs:* TOPB2 + LIVEC-H30 paired vs B. *Falsifies:* d22-29 c/u does not rise, or total
units fall (the EARLY_SELL "B" failure mode: 90 units unsold at the horn). Rank 2 because it costs
a code change and the family's wide version already lost.

**T3 — does B's `g11` horizon fire at all?** The melon/idle-tile root cause (hire enumeration on
today's tasks) has a live theta gene, `macro.forward_days`, and nobody has read what B decodes for
it. *Change:* none — return `fwd` from `S/topledger/ledger.py`'s `run_day` call (it is already the
second element) and print the per-day horizon. *Falsifies nothing by itself*; if B decodes 0 on
every day, the gene is dead weight like flow151's and the ES has never had the melon/land ramp
available, which re-opens M1 as a *training* target rather than a planner one. 20 minutes.

## 6. Open

- Animal columns in `S/topledger/*.npz` are zero (indexing bug named in §3); the wool/herd half of
  the late band is therefore quoted from the archive, not measured here.
- Per-product late revenue is not separable from this ledger (the sale ledger is per seat, not per
  product). If T1's mechanism check needs it, the shed-per-item columns at d14/d20 are the proxy
  already dumped: ours d20 24.6 straw + 10.7 wheat + 6.1 melon, theirs 25.2 wheat + 12.8 straw.
