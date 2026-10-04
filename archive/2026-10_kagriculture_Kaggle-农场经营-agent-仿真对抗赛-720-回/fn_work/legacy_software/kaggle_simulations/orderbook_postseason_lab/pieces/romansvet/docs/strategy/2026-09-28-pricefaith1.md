# PRICEFAITH1: is GUARD=0's rival-money cut on the MELON band real, or the open-loop tape? (2026-09-28, 20:06Z-20:45Z)

Stream dir `S/pricefaith1/`. Evidence only: no src, dist, package or clone-cfg change. CPU only (remote 3 workers, local 1 worker at nice 19 / idle io).

## Verdict
- **GUARD=0's +10 band flips are a tape artefact.** All 18 flips (14 up, 4 down) sit on seats where at least one arm breaks the rival tape (rival units off the recorded game by more than 5 %). On the 33 seats where both games keep the rival within 5 %, the flips are **+0/-0**, and both arms win **0** of them.
- **Every flip follows the rival's units, not its prices.** On all 18 flip seats, the flip goes to the arm under which the rival sells fewer units. On the 14 up-flips, the rival sells a median 33 % fewer units than recorded under G0, against 6 % under the control. On the 4 down-flips, the control collapsed the tape harder (mhw_113460543: rival units -75 %, control margin +109k).
- **The clone's whole band win count is breakage.** In every cell (ctrl 30 W, G0 40, uSS 33, no-land 29), **0 wins are on JC1-faithful seats (0 of 62 / 34 / 63 / 65)**. Every win is on a seat where the rival sold at least 5 % fewer units than recorded (median -40 % on the wins).
- **Where the rival's -9,956 comes from (G0 - ctrl, 116 seats).**
  - It is almost all lost income in d10-29: -9,746 of the -9,956 (d18-29 -7,040, d10-17 -2,706; d0-9 adds -465). Spend moves only -255.
  - Of the d10-29 loss, **62 % is units** (-6,086: the rival sells 68 fewer units a seat; strawberry -2,149, milk -1,076, egg -601, wool -502, melon -457) and **38 % is price** (-3,660).
  - The price part is our extra animal products depressing the rival's prices: milk -2,109, wool -2,068, fertilizer -874. Under G0 we sell +61 eggs, +23 milk and +49 fertilizer a seat and 50 fewer wheat, so the rival's wheat price rises (+1,364).
- **The cascade on the up-flip seats is open-loop breakage.**
  - The rival's d0-9 income falls: REC 14.1k, ctrl 13.2k, G0 12.4k (G0 sells +7 wool in d0-9, so the rival's wool price falls).
  - Its d0-9 buys then fail: spend REC 15.8k, ctrl 15.4k, G0 14.2k.
  - Its production follows: d10-29 units 1,882 -> 1,728 -> 1,321, and d10-29 income 145k -> 144k -> 111k.
  - A 0.8k early cash dent becoming a 33k collapse is the tape replaying commands for hands and plants that no longer exist. A reacting rival would re-plan.
  - When we sit in seat 0, our empty tiles consume the daily weed RNG before the rival farm, so the rival's weeds are re-dealt as well. G0 breaks the tape more on seat 0 (rival units -6.4 pp vs ctrl) than on seat 1 (-1.7 pp), and it takes +7 of the +10 flips on seat 0 (53 seats) against +3 on seat 1 (63 seats).
- **What may be real is the price channel on faithful seats, and it moves no flips.** On the 33 JC1 seats the rival loses -8,827 (t -4.62) at almost constant units. That is 80 % price effect: wool -4.4k, milk -2.2k, fertilizer -1.2k, wheat +1.9k. Our own purse moves +707 (t 0.44).
  - The margin gains +9.5k/seat (t 3.48), but the control's median margin on those seats is -32.7k (best -8.7k), so no seat flips.
  - CAPAUDIT1's live27 run saw no denial at all: G0's faithful dtheirs was +122. One hypothesis, not tested here: live27 runs the SALE hand-back, and about 70 % of the band denial falls in d18-29.
- **Calibration on truth (FIRELIVE1's 18 live seats) does not validate a price flag.**
  - The per-product price leg (2X %) trips on **every** seat, 18/18 live and 116/116 band. Any change in our sales mix moves some rival product's realised price by 24-172 % of its recorded income.
  - The total-income leg keeps the same 3 artefact rows that JC1 keeps: Crop Dustas, high frequency farming 114820595 and Nevska 114787667. Their rival units (±1.3 %) and income (-2.9..+4.2 %) look as faithful as the consistent rows.
  - The deviation bonus FIRELIVE1 inferred does not show in the rival's ledger. On the 14 JC1 seats OFF's gain is our own purse (+5.6k, t 3.48). The rival even earns +4.2k more.
- **Judge rule (§D):** count clone flips only on seats where both arms are JC1-faithful on the exact ledger. Report pf10t as the sensitivity set. Treat the per-product price leg as a diagnostic, not a gate. On the band, where the clone wins no faithful seat, score coins and margin (t) on the JC1 set, not flips.

## 0. Method and exactness
- **Instrumented engine.** `fastenv/` is a copy of the BCSIM1 bit-exact C++ port with one addition: a per-farm ledger `sold_rev[item]`, updated in `commit_unit` SELL, plus `kag_sales()`. It exports cumulative sold units and coins for the 9 products, plus total spend and sell revenue. Decisions and RNG are untouched.
  - The identity `money = 3000 + sell_revenue - total_spend` holds on every game checked.
- **Band runs (`pf_grid.py`, the CAPAUDIT1 harness copy `fastenv/kh.py`, remote CPU, 3 workers, N=29, JAX CPU, 20:14-20:33Z).** 116 MELON band seats x 5 cells = 580 games:
  - **REC** = the recorded live game: our live tape `S/bandleg1/ourtape/<ep>` vs the rival tape.
  - **ctrl** = CAPAUDIT1 control: r5a3, GUARD=1, caps90, CARE=1, land fix L7t70.
  - **G0** = ctrl with GUARD=0.
  - **uSS** = ctrl with strawberry seeds uncapped.
  - **NOLAND** = LAND3Q1 r5a3 CARE=1 control, without the land fix.
- **Money-exact 580/580.** REC 116/116 = the live purses. ctrl, G0 and uSS 116/116 each = CAPAUDIT1 `res/grid_all.csv`. NOLAND 116/116 = LAND3Q1 `res/grid_r5a3.csv` ctrl. The 3-seat smoke (x3 boards, REC/ctrl/G0) was 9/9 before the launch.
- **FIRELIVE1 seats.**
  - LIVE = the live replay's joint actions (`S/livewatch2{2,3}/gz`) replayed through the instrumented engine: 18/18 = live purses.
  - OFF = FIRELIVE1's OFF arm re-run in the python engine with the joint actions kept (`off_leg.py`, local, 1 worker, 20:10-20:19Z): 18/18 = `S/firelive1/res/off.csv`. It was then replayed through the instrumented engine: 18/18 exact.
- **Phases** are d0-9 (steps 0-239), d10-17 (240-431) and d18-29 (432-719). Realised unit price = coins / units per phase.

## A. The flag (`S/pricefaith1/price_faith.py`)
Per game, against the recorded game of the same tape (REC on band seats, LIVE on live seats):
- **jc1**: |rival units sold d0-29 - recorded| <= 5 % and rival purse >= 0.5 x recorded. This is the JC1 units rule on the exact ledger instead of the pre-step-shed estimate. It agrees with FIRELIVE1's JC1 column on 17/18 seats; kenmatsu4 is -1.9 % exact against +14.5 % in the estimate.
- **pfX** (the spec, X = 5, 10): jc1, AND the rival's income d10-29 within X % of recorded, AND for every product |d income_p d10-29| <= 2X % x max(recorded income_p, 5 % of the recorded d10-29 total).
- **pfXt** (added, because pfX keeps no seats): jc1 AND the rival's income d10-29 within X %.
- **Pairing:** a paired seat is in set S only if both games are S-faithful, as in `S/judgeclean1/pair_faith.py`.

## B. Calibration on FIRELIVE1's 18 fired live seats (LIVE = truth, OFF = the deviating PFS counterfactual)
An artefact row is a seat where OFF won and LIVE lost: FIRELIVE1's 7 flips. Per-seat detail is in `res/calib.md` and `res/calib_seats.tsv`.

| flag | kept | artefact rows kept | artefact rows flagged out | consistent rows kept | consistent rows flagged out | kept: W OFF -> W LIVE |
|---|---|---|---|---|---|---|
| FIRELIVE1 JC1 (shed estimate) | 13 | 3 | 4 | 10 | 1 | 9 -> 6 |
| jc1 (exact ledger) | 14 | 3 | 4 | 11 | 0 | 9 -> 6 |
| pf10t | 13 | 3 | 4 | 10 | 1 | 8 -> 5 |
| pf5t | 12 | 3 | 4 | 9 | 2 | 7 -> 4 |
| **pf10 (spec)** | **0** | 0 | 7 | 0 | **11** | - |
| **pf5 (spec)** | **0** | 0 | 7 | 0 | **11** | - |

- **No tolerance separates the artefact rows.**
  - The per-product leg flags all 18. The worst product moves 24-172 % on consistent rows and 27-65 % on artefact rows.
  - JC1 / pf10t / pf5t catch the same 4 unit-broken artefact rows (Black Mamba x2, Matt Motoki, Nevska 114811497) and keep the same 3 faithful ones.
  - pf5t only adds false alarms (cjen07 +16.8 %, team +9.6 %).
- **What moves on the 14 JC1 seats (OFF - LIVE, `res/calib_prodphase.md`).**
  - The rival's units -8.6/seat (≈ 0), but its d10-29 income is +3.6k (t 2.21), all from price: melon +4.5k (PFS does not flood melon the way the fired V56 did), strawberry -4.4k, wool +3.4k.
  - Our purse +5.6k (t 3.48).
  - So the price channel is always live and runs in both directions per product. The deviation bonus is in our own purse, not in the rival's ledger.

## C. Re-score on the 116 MELON band seats (`res/rescore.md`, `res/rescore_pairs.csv`, per seat `res/rescore_seats.csv`)
### GUARD=0 (G0) vs control
| set | n | W ctrl -> G0 | flips | dours (t) | dtheirs (t) |
|---|---|---|---|---|---|
| all | 116 | 30 -> 40 | +14/-4 = **+10** | +3,918 (+3.58) | -9,956 (-5.28) |
| JC1-faithful | 33 | 0 -> 0 | +0/-0 = **+0** | +707 (+0.44) | -8,827 (-4.62) |
| price-faithful pf10t | 21 | 0 -> 0 | +0/-0 = **+0** | -1,453 (-0.86) | -6,029 (-4.22) |
| price-faithful pf5t | 9 | 0 -> 0 | +0/-0 = **+0** | -987 (-0.36) | -7,508 (-3.23) |
| pf10 / pf5 (spec) | 0 / 0 | - | - | - | - |

- **Per-seat counts.**
  - Across the 116 seats, the JC1 pattern (ctrl, G0) is: 33 both faithful, 29 ctrl faithful with G0 broken ("10"), 1 the reverse ("01"), 53 both broken.
  - Flips by pattern: up "10" 7, up "00" 7, down "00" 4, **on "11": 0**.
  - The full flip list, with rival units per arm and margins, is in `res/g0_flipstats.md`.
- **By seat.**
  - Seat 0 (the rival's weeds re-dealt by our empty tiles): all 53, +8/-1 = +7, dtheirs -11.6k; JC1 10 seats, +0.
  - Seat 1: all 63, +6/-3 = +3, dtheirs -8.6k; JC1 23 seats, +0.
- **Margin on the faithful sets.**
  - JC1: +9,534/seat (t 3.48); ctrl median -32.7k (best -8.7k), G0 median -23.3k (best -1.1k).
  - pf10t: +4,576 (t 2.01).

### Other cells, same flag
| comparison | set | n | W | flips | dours (t) | dtheirs (t) |
|---|---|---|---|---|---|---|
| uSS vs ctrl | all | 116 | 30 -> 33 | +6/-3 = +3 | +634 (+0.87) | -240 (-0.20) |
| uSS vs ctrl | JC1 | 57 | 0 -> 0 | +0 | +904 (+1.30) | +828 (+0.96) |
| uSS vs ctrl | pf10t | 38 | 0 -> 0 | +0 | +591 (+0.67) | +435 (+0.59) |
| uSS vs ctrl | pf5t | 23 | 0 -> 0 | +0 | +1,507 (+1.41) | +304 (+0.29) |
| L7t70 (ctrl) vs no-land | all | 116 | 29 -> 30 | +2/-1 = +1 | +806 (+1.76) | -220 (-0.89) |
| L7t70 (ctrl) vs no-land | JC1 | 62 | 0 -> 0 | +0 | +425 (+0.72) | -13 (-0.04) |
| L7t70 (ctrl) vs no-land | pf10t | 42 | 0 -> 0 | +0 | +1,384 (+2.29) | -178 (-0.55) |
| L7t70 (ctrl) vs no-land | pf5t | 27 | 0 -> 0 | +0 | +709 (+0.94) | -131 (-0.30) |

- **The coin cells stay coin cells on faithful seats.** uSS (+0.9k, t 1.3) and the land fix (+1.4k on pf10t, t 2.3) keep their own-purse gain with no rival-money effect (|dtheirs| < 0.9k).
- **G0 is the only cell whose rival cut is tape-shaped**, and the only one that breaks the tape more than the control does: faithful G0 games number 34/116, against 62-65 for the other cells.

### Where the rival's -10k comes from (G0 - ctrl; mean per seat; units effect = d units x ctrl price, price effect = G0 units x d price)
| phase | product | set all (116): d units | d income (t) | units effect | price effect | set JC1 (33): d units | d income (t) | units effect | price effect |
|---|---|---|---|---|---|---|---|---|---|
| d0-9 | ALL | -0.9 | -465 (-7.32) | | | +0.1 | -391 (-5.55) | | |
| d0-9 | WOOL | +0.1 | -285 (-10.84) | +8 | -293 | -0.1 | -291 (-6.48) | -27 | -263 |
| d10-17 | ALL | -14.9 | -2,706 (-4.49) | | | -5.1 | -1,853 (-3.35) | | |
| d18-29 | ALL | -52.9 | -7,040 (-4.92) | | | -8.6 | -5,933 (-3.77) | | |
| d10-29 | WHEAT | -8.0 | +1,121 (+3.64) | -243 | +1,364 | +0.8 | +1,925 (+2.32) | +32 | +1,893 |
| d10-29 | CARROT | -6.4 | -130 (-1.22) | -332 | +202 | -0.5 | +122 (+1.27) | -10 | +132 |
| d10-29 | TOMATO | -4.5 | -242 (-1.66) | -385 | +143 | -0.7 | +26 (+0.54) | -103 | +129 |
| d10-29 | STRAWBERRY | -11.0 | -2,360 (-3.52) | -2,149 | -212 | -2.8 | -849 (-2.12) | -447 | -402 |
| d10-29 | MELON | -2.6 | -435 (-2.06) | -457 | +22 | -0.7 | -178 (-0.93) | -114 | -65 |
| d10-29 | EGG | -12.5 | -729 (-4.38) | -601 | -129 | -2.9 | -285 (-2.50) | -133 | -153 |
| d10-29 | MILK | -8.9 | -3,184 (-4.15) | -1,076 | -2,109 | -2.7 | -2,626 (-2.08) | -406 | -2,220 |
| d10-29 | WOOL | -6.5 | -2,570 (-4.43) | -502 | -2,068 | -0.6 | -4,567 (-3.27) | -179 | -4,389 |
| d10-29 | FERTILIZER | -7.5 | -1,215 (-6.73) | -341 | -874 | -3.5 | -1,352 (-3.46) | -164 | -1,188 |
| **d10-29** | **ALL** | **-67.8** | **-9,746 (-5.02)** | **-6,086** | **-3,660** | -13.7 | -7,787 (-4.01) | -1,524 | -6,263 |

- **Our side, G0 - ctrl, all seats.** d0-9 +2,040 (wool +1,320). d10-29 +5,065: eggs +2,891, milk +2,373, fertilizer +1,478, wheat -928, carrot -731. So GUARD=0 turns the clone toward animal products, and those are the rival's price losses.
- **Against the recorded game** (`res/rescore.md`): the control already costs the rival -6,971 of d10-29 income, 249 fewer units. G0 costs it -16,718 and 317 fewer units. Both arms are far from the live game, and the band scores how much each one breaks the tape.

## D. Verdict for the ship gate, and the judge rule
**Verdict: artefact.**
- GUARD=0's +10 flips, and the 62 % units share of the rival's -10k, come from open-loop tape breakage: the rival loses hands, plants and weeds-free tiles and cannot re-plan. The flips are 0 on faithful seats, and they follow the rival's units on 18/18 flip seats.
- What remains on faithful seats is the price channel: the rival's money falls at constant units, and the margin gains +9.5k with t 3.5. It moves no flip, because the clone is 30k behind on those seats.
- It did not appear on live27 (CAPAUDIT1: faithful dtheirs +122).
- **Keep GUARD=0 only as a coin option** (JC1 dours +707, t 0.44, which is noise). **Do not count its band flips.**

**Judge rule for clone candidates, from now on:**
1. **Run base and candidate with the ledger, plus REC.** REC is the tape's recorded game: our live tape vs the rival tape.
2. **Flip claims count only on the JC1 set.** Seats enter only when both games are JC1-faithful on the exact ledger: rival units within 5 % of REC, rival purse >= 0.5 x REC.
3. **Report pf10t as the sensitivity set** (JC1 plus rival income d10-29 within 10 % of REC).
4. **The per-product price leg is a diagnostic, not a gate.** It removes every seat, and on live truth it separated nothing.
5. **On the band, the clone wins 0 JC1 seats in every cell, so flips there are always 0.** Score candidates by dours and dmargin with t on the JC1 set. A candidate's win count on non-faithful seats is a measure of tape breakage.
6. **Flag a candidate as breakage when its flips sit on "10" / "01" seats** (one arm faithful, the other broken), or when its faithful-seat count drops well below the control's (G0: 34 vs 62).
7. **Ship evidence stays with the live-seat legs** (live27 / FIRELIVE1-style replays), with the JC1 filter.
- **The deviation bonus FIRELIVE1 found is not visible in any rival-side flag.** It sits in our own purse, so a band "own-purse" gain on faithful seats is still only an upper bound.

**Commands (from /mnt/e/_work/kaggriculture3):**
```
# 1. ledger runs: jobs json = [{"cell": "REC", "cfg": {}, "label": L}, ...] + the judge's own base/candidate job rows (same cfg keys as S/capaudit1/jobs_*.json)
JAX_PLATFORMS=cpu python3 S/pricefaith1/pf_grid.py --jobs J.json --boards S/capaudit1/boards_m116.json --params P.npz --out S/<stream>/res/x.csv [--w W --nw NW --N 29]
# 2. flag a judge csv (label column) for cell C  -> judge_pf.csv with jc1 / pf10t / pf5t / pf10 / pf5 + metrics
python3 S/pricefaith1/price_faith.py flag --sal S/<stream>/res/x_sal.jsonl --ref REC --cell C --csv <judge.csv> --out <judge_pf.csv>
# 3. paired re-score (all / jc1 / pf10t / pf5t / pf10 / pf5) + the rival product/phase table
python3 S/pricefaith1/price_faith.py pair --sal S/<stream>/res/x_sal.jsonl --ref REC --base ctrl --arm C
```
Example: `python3 S/pricefaith1/price_faith.py flag --sal S/pricefaith1/res/sal_all.jsonl --ref REC --cell G0 --csv S/capaudit1/res/grid_g0.csv --out S/pricefaith1/res/grid_g0_pf.csv` gives 116/116 rows: jc1 34, pf10t 28, pf5t 16, pf10 0, pf5 0.

## Files
- `S/pricefaith1/fastenv/`: `sim.hpp`, `kagapi.cpp`, `kag.py` (+ `kag_sales`); `kh.py` (the CAPAUDIT1 harness copy, which records the ledger at steps 240 and 432 and at the end).
- `pf_grid.py` (ledger runs, REC + clone cells), `jobs_all.json` / `jobs_main.json` / `jobs_uss.json` / `jobs_smoke.json`, `pf_acts.py` (FIRELIVE1 LIVE/OFF replays), `off_leg.py` + `run_off.sh` (the OFF re-run with actions kept, `rp_off/`), `price_faith.py`, `calib.py`, `rescore.py`, `dump_tables.py`.
- `res/`:
  - `sal_all.jsonl` (580 band games), `all_rows.csv`, `fl_sal.jsonl` (36 live-seat games), `off_rerun.csv`;
  - `calib.md`, `calib_seats.tsv`, `calib_prodphase.md`;
  - `rescore.md`, `rescore_pairs.csv`, `rescore_seats.csv`, `g0_flipstats.md`, `wins_by_faith.md`, `grid_g0_pf.csv`;
  - per-seat product x phase tables `seat_products_band.tsv` and `seat_products_firelive1.tsv`.
- Remote `~/stage_pricefaith1` holds a copy of `~/stage_capaudit1` without `live/` and `res/`, plus this stream's files. It is kept.

## Rule incident
- At about 20:13Z, one local read command carried a stderr redirect to the null device (`cat logs/smoke.log 2>/dev/null`). It was a redirect only, with no other read or write under /dev, and it was not repeated. Logged in `S/pricefaith1/checkpoint.txt`.
