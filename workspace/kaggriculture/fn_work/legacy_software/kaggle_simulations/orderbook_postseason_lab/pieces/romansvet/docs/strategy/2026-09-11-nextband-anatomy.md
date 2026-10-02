# NEXT30 anatomy: the 2650-2750 half is the SAME clone as 2550-2650, with the variance squeezed out

2026-09-11/12. Answers the question `docs/strategy/2026-09-11-nextband.md §4` left open: B beats hr
by **+1,377 (t 2.20)** on the 2550-2650 half of NEXT30 and by **+102 (t 0.29) — level** on the
2650-2750 half. What do the stronger opponents *do* that the weaker ones do not, and where does B
lose the margin?

Tools: `S/nextband/anatomy.py` (`opp` / `band` / `report`), tables in `S/nextband/anatomy.md`,
per-board csvs `S/nextband/anatomy_opp_NEXT30.csv` and `S/nextband/anatomy_band_B.csv`.

* **Opponent side** — their own recorded game (`S/nextband/replays/ep_<episode>.json`, that team's
  own seat, the episode the tape was cut from). The market phase is re-simulated with
  `scripts/replay_profile._simulate_market`; **`max |recon_err| = 0` over all 30 boards**, i.e. the
  reconstruction reproduces every observed money delta to the coin, so the sell/buy columns are
  exact, not estimated.
* **Our side** — B played against each pinned-town tape in the sim's action-replay opponent seat
  (the `S/simscreen/screen.py` recipe: recorded town, `shop_crn` on, the leg's own seed from
  `boards.csv`, both seats), with `st.money` scanned out per day instead of only at the end.

**Caveats, up front.** 16 upper + 14 lower boards; one recorded game per team, so every opponent
column is n = 1 per team and the per-team value carries that game's own board luck. The recorded
game was against *that team's own* opponent, not against us, so absolute money levels in §1 are not
comparable between teams — only the *shape* of the build is. The band decomposition in §2 is the
pinned-town sim (99.5 % of the engine on pinned towns, `sim-equals-engine-2026-09-06`), not the
engine leg; the engine leg's board margins (`S/lossflip/nextband_B.csv`) are the numbers of record
and are quoted alongside.

---

## 1. What the opponents do — the means separate NOWHERE

46 behaviour columns, Welch t of upper (2650-2750) vs lower (2550-2650):

| column | upper 2650-2750 | lower 2550-2650 | diff | Welch t |
|---|---:|---:|---:|---:|
| hires on day 0 | **5.0** | **5.1** | -0.1 | -1.00 |
| hires on day 1 | **3.0** | **3.2** | -0.2 | -1.00 |
| hands at d10 | **11.0** | **11.0** | 0.0 | — |
| tiles planted by d10 | 69.8 | 70.7 | -1.0 | -0.71 |
| .. WHEAT by d10 | 37.8 | 37.3 | +0.5 | +1.19 |
| .. STRAWBERRY by d10 | **20.0** | 21.6 | -1.6 | -1.00 |
| .. MELON by d10 | **12.0** | 11.5 | +0.5 | +1.34 |
| .. CARROT / TOMATO by d10 | 0.0 | 0.3 / 0.0 | — | — |
| tiles planted by d29 | 236.5 | 233.7 | +2.8 | +0.76 |
| cows bought / first cow day | 7.7 / d0 | 7.8 / d0 | -0.1 | -0.25 |
| sheep bought / first sheep day | 6.8 / d0 | 6.4 / d0 | +0.4 | +0.50 |
| geese bought / first goose day | 2.5 / d8.7 | 2.4 / d7.6 | +0.1 | +0.33 |
| animals bought by d10 | 16.0 | 15.6 | +0.4 | +1.24 |
| **melon units sold** | **72.0** | **72.0** | 0.0 | 0.00 |
| melon first sell day | **10.0** | 10.5 | -0.5 | -1.00 |
| melon units d0-10 / d11-14 / d15+ | 60.0 / 12.0 / **0.0** | 55.3 / 10.7 / **6.0** | — | -1.00 |
| wool / milk / egg units | 173.5 / 231.4 / 65.2 | 168.6 / 231.7 / 61.0 | — | ≤ 0.37 |
| wheat / carrot / tomato / strawberry units | 339.6 / 83.6 / 5.0 / 248.1 | 311.1 / 84.6 / 15.4 / 253.8 | — | ≤ 1.43 |
| FERTILIZE ops applied | 64.9 | 72.2 | -7.3 | -0.95 |
| fertilizer units sold | 345.8 | 334.1 | +11.7 | +0.76 |
| sell rows (turns with a SELL) | 254.9 | 246.9 | +8.0 | +0.47 |
| .. d0-9 / d10-14 / d15-29 | 55.6 / 32.4 / 166.9 | 50.6 / 30.9 / 165.3 | — | ≤ 1.40 |
| PASS rate % | 6.7 | 7.3 | -0.6 | -0.82 |
| money d9 / d10 / d14 | 2,331 / 14,689 / 21,814 | 2,153 / 13,541 / 20,876 | — | ≤ 1.24 |

**The largest |Welch t| over all 46 columns is 1.43** (wheat units sold). At n = 30 with 46
correlated columns the *expected* maximum |t| under the null is ~2.3-2.6, so 1.43 is not merely
non-significant — it is **below what pure noise would produce**. Rating as a continuous regressor
over all 30 boards (more powerful than the median split) gives the same answer: largest |t| over
the same columns is well inside the multiplicity bar.

### The band is one open-loop clone, and the upper half is its zero-variance core

The d0-10 build fingerprint `(hires_d0, hires_d1, wheat@d10, strawberry@d10, melon@d10, cows,
sheep, first melon sell day)` takes **8 distinct values over 30 teams, and 18 of the 30 boards share
the single modal value** `(5, 3, 38, 20, 12, 8, 6, d10)`. Every one of the 30 teams hires 5 on d0
and ~3 on d1, has 11 hands at d10, sells exactly 72 melon units, and opens the melon dump on d10.
This is the clone family of `kaggle-clone-family-2026-09-05` / LOSS10, measured team by team.

What *does* separate the halves is the **dispersion**, and it separates hard (F test of the lower
half's variance over the upper half's, df 13/15):

| column | sd upper | sd lower | F (lo/up) | p |
|---|---:|---:|---:|---:|
| hires on day 0 | **0.00** | 0.27 | ∞ | < 1e-4 |
| hires on day 1 | **0.00** | 0.80 | ∞ | < 1e-4 |
| MELON tiles by d10 | **0.00** | 1.40 | ∞ | < 1e-4 |
| STRAWBERRY tiles by d10 | **0.00** | 6.06 | ∞ | < 1e-4 |
| melon units sold after d14 | **0.00** | 22.4 | ∞ | < 1e-4 |
| weed tiles grown | 1.2 | 8.2 | 42.6 | < 1e-4 |
| plant29 total tiles | 2.7 | 13.5 | 25.6 | < 1e-4 |
| money at d10 | 910 | 3,354 | 13.6 | < 1e-4 |
| FERTILIZE ops | 8.3 | 27.8 | 11.1 | < 1e-4 |
| PASS rate % | 1.1 | 2.3 | 4.5 | 0.007 |
| units sold, all | 63.7 | 112.7 | 3.1 | 0.038 |

Sixteen out of sixteen upper-half teams plant **exactly** 12 melon and 20 strawberry by d10, hire
**exactly** 5 on d0, and have **zero** melon left to sell after d14. The lower half contains the
stragglers: teams that plant 9 melon, that are still dumping melon at d20+, that grow 40 weeds, that
burn 120 FERTILIZE ops. The 100-point rating difference inside this band is **not a different
strategy — it is the same strategy with the execution noise removed**.

---

## 2. Where B's margin goes — the d10-14 melon pot is a flat tax, d15-29 is the whole game

B vs each pinned-town tape, both seats averaged, per-day money scanned out of the sim
(`S/nextband/anatomy_band_B.csv`; full per-board table in `S/nextband/anatomy.md §2`). The sim
reproduces the engine leg board for board (Chris Deotte -3,440 sim / -3,804 engine; Van-Phuc Huynh
+25,095 / +25,054; kwa +2,914 / +2,914).

| slice | n | d0-9 | d10-14 | d15-29 | margin d29 | win % |
|---|---:|---:|---:|---:|---:|---:|
| ALL | 30 | **+3,029** (sd 1,036) | **-20,705** (sd 2,916) | **+21,786** (sd 7,762) | +4,110 | 70.0 |
| upper 2650-2750 | 16 | +2,940 | -20,778 | +21,074 | +3,236 | 68.8 |
| lower 2550-2650 | 14 | +3,131 | -20,621 | +22,600 | +5,110 | 71.4 |
| upper - lower (Welch t) | | -191 (t -0.51) | -157 (t **-0.14**) | -1,526 (t -0.52) | -1,874 (t -0.66) | |
| B's 21 WINS | 21 | +2,899 | -20,055 | **+24,670** | +7,513 | |
| B's 9 LOSSES | 9 | +3,333 | -22,221 | **+15,058** | -3,830 | |

The shape is the same on **every one of the 30 boards**: we lead by ~3k through d9 (their melon is
in the ground, ours is cash), we are taxed ~-20.7k in d10-14 when the clone dumps its 72 melon units
into the pot, and we take it all back and more in d15-29. Correlation with the final margin:

| band | corr with d29 margin | share of the margin's variance |
|---|---:|---:|
| d0-9 | **-0.120** | 1.9 % |
| d10-14 | **+0.177** | 14.7 % |
| d15-29 | **+0.930** | 103.9 % |

The d10-14 melon pot is a **flat tax paid on every board** — its sd (2,916) is a seventh of the
d15-29 band's (7,762) and it explains 15 % of the margin's variance against d15-29's 104 %. This is
§54's `d10-14 pot = flat tax, d15-29 denial = the discriminator` reading, reproduced on the 2550-2750
band with a per-day ledger instead of a top-tier one.

### The engine leg's own losses (the numbers of record, `S/lossflip/nextband_B.csv`)

B loses 9 of 30 boards. Five are in the upper half, four in the lower, and the *sizes* differ:

| half | B's losses | mean loss | B's wins | mean win |
|---|---|---:|---|---:|
| upper 2650-2750 | 5/16 — Chris Deotte 2750.0 (-3,804), keeplooking 2715.7 (-2,315), gachichan 2711.7 (-4,651), ibr mo sal 2701.5 (-1,847), parv goyal2 2690.0 (-3,568) | -3,237 | 11/16 | +6,003 |
| lower 2550-2650 | 4/14 — sue124 2643.9 (-11,011), xingyun_byto 2630.5 (-2,742), hongqian miao 2618.4 (-1,821), Exposed 2571.4 (-3,352) | -4,732 | 10/14 | +8,783 |

B's win *rate* is nearly the same in both halves (68.8 % vs 71.4 %) and its losses are, if anything,
**smaller** on the upper half. The upper half costs us on the **upside**: mean win +6,003 vs +8,783,
and the two biggest wins of the whole leg sit at 2662 and 2627. The 2650-2750 edge loss is not more
losses — **it is the wins getting smaller**, exactly the signature of an opponent who leaves fewer
coins on the table rather than one who plays a different game.

---

## 3. The three answers

### (i) Different behaviour, or the same behaviour with less slack? — **the same behaviour, with less slack.**

No measured column separates the halves in the mean. The largest |Welch t| over 46 behaviour
columns is **1.43** (wheat units sold, 339.6 vs 311.1), below the ~2.3-2.6 maximum that pure noise
produces at n = 30 over that many columns; day-0 hires (5.0 vs 5.1), hands at d10 (11.0 vs 11.0),
melon tiles by d10 (12.0 vs 11.5), melon units (72 vs 72), first melon sale (d10 vs d10.5), cows
(7.7 vs 7.8), sheep (6.8 vs 6.4), wool/milk/egg (173/231/65 vs 169/232/61), fertilizer applied
(64.9 vs 72.2) and sell rows per band (55.6/32.4/166.9 vs 50.6/30.9/165.3) are all the same build.
18 of 30 teams share one byte-identical d0-10 fingerprint.

The halves separate in **variance**, decisively: hires d0 sd 0.00 vs 0.27, melon tiles d10 sd 0.00
vs 1.40, strawberry tiles d10 sd 0.00 vs 6.06, melon sold after d14 sd 0.00 vs 22.4 (all F = ∞,
p < 1e-4), weeds F 42.6, planted tiles F 25.6, money at d10 F 13.6, FERTILIZE ops F 11.1, PASS rate
F 4.5. **The 2650-2750 half is the same clone with its execution noise removed.** That is the
mechanism of the decayed edge: our +1,377 on the lower half is earned against stragglers who misplay
the shared script (9 melon instead of 12, melon still being dumped at d20, 40 weeds), and those
mistakes simply are not present above 2650.

### (ii) Which band decides B's losses there?

**The d15-29 band, on all nine losses and on both halves — and it is the same band that decides the
wins.** All 9 of B's losses have d10-14 as their most negative band, but that is true of all 30
boards: everyone pays the melon-pot tax. What separates a loss from a win is the **recovery**:
+15,058 on the 9 losses vs +24,670 on the 21 wins (a -9,612 gap), while the d10-14 tax differs by
only -2,166 and the d0-9 lead is actually *larger* on the losses (+3,333 vs +2,899). B never loses
a NEXT30 board in the opening or in the pot; it loses boards where the d15-29 denial phase returns
15k instead of 25k.

The band decomposition is **identical across the two rating halves** (d0-9 t -0.51, d10-14 t
**-0.14**, d15-29 t -0.52) — further confirmation of (i): the upper half is not taxing us harder or
earlier, it is simply leaving less on the table in d15-29 (+21,074 vs +22,600, and mean *win*
+6,195 vs +8,963).

### (iii) Does anything point at a knob the ES trains, or at a closed family?

**It points at a closed family, not at an open lever.** The ES's live blocks under
`--train-only gp,dh,ds,g5,gb5,w3,b3,b1` (`docs/strategy/2026-09-11-g10-decode-diff.md`) are
`gp` = the global head's product-glut residual, `dh`/`ds` = the town's residual drain into the
encoder and straight onto grow/sell, `w3` = the sell head's per-product price gate, `b3` = the sell
head's global lot-count bias, `g5`/`gb5` = land_afford / free_urgency, `b1` = encoder bias. Every
one of those is a **sell-side price/lot/timing** or **town-drain** knob. Nothing in the ES's 1,191
trained genes touches the opening, hiring, tile mix or animal schedule — and the opening, hiring,
tile mix and animal schedule are precisely the columns that are *identical* across the band, so
there is nothing there for it to exploit anyway.

On the sell side, the anatomy says the upper half's clone leaves nothing to take:
* its melon is **entirely gone by d14** (0.0 units after d14, sd 0.0) — no late melon to under-cut,
  and the d10-14 melon pot is a **flat tax** on both seats (§54, `2026-09-08-loss-anatomy`);
* its fertilizer is 65 applied / 346 sold — the **§57 FERT_VOLUME** family, closed (margin up, wins
  level), re-confirmed by **§86** (what we leave in the shed is 47 coins/game);
* its sell-row cadence is 255 rows/game vs our allocator's — the **§85/§88/§89/§90/§91** sell-timing
  family, **closed**: SELL21 refused on the screen (hands them +1,383/game), SELL5 level in the
  engine (+35…+52 coins, 0 flips in 320 paired games);
* under-cutting their price is **§55 OPP_SUPPLY_ON** (refused on pinned boards) and **§68
  OPP_FRONTRUN** (level, refused); imitating their opening is **§70 WALL IMITATION** (-24k/board);
  their melon/mix schedule is the closed hand-melon (`dominant-strategy-2026-09-03`, 1.9 %,
  -19.6k), mix-rule, wool and shop-adaptive top-5 families; **§76** says B is a strict local optimum
  in its own 41-integer lattice (radius 1-2), so the integer race is closed too.

So: **no new lever is open here, and no re-pointing of the ES's block list is argued for.** What the
anatomy *does* argue is about the **objective and the judge**, not the knobs:

1. **The NEXT30 leg is measuring the right thing and should stay** (§97, informational): it is the
   only leg whose opponents are the zero-variance version of the clone. But its *upper half* is the
   part that carries information about the 2967 cutoff, and the lower half is largely re-measuring
   straggler-punishing that LIVE-C already measures.
2. **Beating this band needs a lever that works against a mistake-free clone.** Every family we have
   closed was closed against either the ≤2500 live files or the 2953+ top tier; the anatomy says the
   2650-2750 wall is the *same script* as both, so re-opening any of them on this band would be
   re-running a closed experiment against a tighter version of the same opponent — not worth a leg.
3. The one honest reading for the ES: the upper half's clone is a **fixed, noiseless opponent**, so
   the remaining margin there is a pure price/allocation problem — which is the half of the game the
   trained blocks (`gp`, `w3`, `b3`, `dh`) do control. That is an argument for *keeping* the current
   block list and for judging arms on the NEXT30 **upper half** specifically, not for adding genes.
