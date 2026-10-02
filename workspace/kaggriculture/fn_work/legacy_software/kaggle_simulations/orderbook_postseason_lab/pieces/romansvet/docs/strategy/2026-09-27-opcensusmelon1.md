# OPCENSUS-MELON1 (2026-09-27, ~21:05Z): op-by-op census, top MELON teams vs PFS on the same boards

BUILDREVIEW1 hole 5, second half. This is a replay/ledger study only. It builds no arm and runs no new game. Tools are in `S/opcensusmelon1/`, the base is `S/melonswap1/` (read-only), and the repo is at master 942b46cb.

## Verdict
- On the same boards, PFS's own purse does not trail the top MELON teams by any robust amount. There are 49 boards where the rival tape survives the swap (rival final purse within 10 % of its live purse). On those, T − P = +3,313/game (T ahead on 71 % of boards). At 20 % tolerance (91 boards) the sign flips to −1,071.
- The margin gap on the 49 intact boards is +6.4k/game: our own purse is +3.3k and the rival's purse is +3.1k (the rival earns more against PFS). On those boards T goes 27-22 and PFS goes 14-35.
- Three books carry the own-purse gap: **wheat d10-19 (+3.35k, 100 % of boards)**, **carrot d20-29 (+1.5k, 84 %)** and strawberry (+1.9k, intact boards only; −3.8k on all 160). PFS's cheaper roster and land offset them: land + hire −2.65k, and T spends more on 94 % of boards.
- All three rule candidates below belong to families that are already CLOSED. No new family comes out of this census.

## Method
- **Boards.** All 160 boards of `S/melonswap1/boards_swap.json`: 8 top MELON teams × 20 live games, with the rival's MELON d0-9 ≥ 9 tiles, covering 121 unique episodes. All 160 swap games were finished in `S/melonswap1/res/pfs.csv` by the end of the run.
- **Seats.**
  - T: the top team's live seat.
  - R: its live rival.
  - P: PFS in T's seat against the rival tape (the gz_pfs replay).
  - R': the rival tape in the swap game.
- **Ledger (`ledger.py`).** It runs ECONCENSUS `measure()`, the native-engine transition replay of the recorded actions (the same instrument as MELONSWAP1's `ledger.py`). It keeps every per-day key for both seats of both replays: effective ops, planted/harvested by crop, feed units by animal, sold/revenue by product, spend by category, hires, pass/no-op turns, and tile-days by kind, crop and animal.
  - The swap replays store `info` after `steps`, so the header is re-ordered first.
  - `ledger_valid` holds on 640/640 rows (cash and stock closure).
  - **Reconcile:** P and R' finals equal `pfs.csv` ours/theirs on 160/160 boards.
- **Analysis (`analyse.py`, `books.py`).** Windows are d0-2, d3-9, d10-19 and d20-29.
  - **Flag rule:** the direction holds on ≥ 60 % of boards, and |coins| ≥ 300/game where a coin value exists. Count-only rows are flagged on the fraction alone and marked "(count)".
  - **Coin values:** revenue and spend are exact. Harvest units are valued at the pooled sale price.
  - **Gap decomposition:** per product, the midpoint volume (Δu × p̄) plus price (Δp × ū), plus five cost categories. It sums exactly to Δcash.
  - **Books:** herd = milk + wool + egg + fertilizer revenue − animals − fertilizer bought − feed wheat at the board's wheat price. Wheat = revenue − all wheat buys + feed credit. Each crop = revenue − seed. The books sum exactly to cash.
  - All coins are one-sided, own-purse figures (the TWO-PURSE rule applies: none of this is a paired result).
- **Why the intact subset.** On all 160 boards the rival tape often breaks when PFS sits in T's seat. P's margin is then +34.8k against T's +1.1k and Δtheirs is +16.9k, so the money columns are only usable on the rival-intact subset. P's op counts come from P's own plan, so the op census uses all 160 boards, and a flag must hold on both sets.

## 1. Flagged categories (T − P per game, board fraction on all 160 / intact 49; `res/census*.tsv`)
| category | window | T | P | coins T−P | T>P (T<P) |
|---|---|---|---|---|---|
| PLANT_WHEAT | d10-19 | 63.9 | 37.8 | (wheat book +3.35k) | 96 % / 98 % |
| TILES_crop_MELON (P's d10-15 melon plate) | d10-19 | 2.6 | 10.2 | (melon book −0.2k..−1.0k) | T<P 100 % |
| SELL_WHEAT | d10-19 | 312 u | 58 u | +9.9k / +11.9k | 99 % / 100 % |
| BUY_PRODUCT (wheat) | d3-19 | 356 u | 65 u | −12.5k / −14.9k | 70-100 % |
| SELL_MELON | d10-19 / d20-29 | 72 / 0 | 20 / 70 | +9.8k / −11.1k (net ≈ 0) | 100 % each way |
| HARVEST/SELL_EGG | d10-29 | 225 u | 101 u | +5.0k | 94-97 % |
| SELL_WOOL | d3-9 / d10-29 | 28 / 102 | 6 / 131 | +3.9k / −8.8k | 100 % / T<P 74-76 % |
| SELL_FERTILIZER | d0-19 | 214 u | 130 u | +4.2k | 67-100 % |
| OP_FERTILIZE | d10-29 | 222 | 179 | (fert used, P covers more tile-days) | 84-96 % |
| PLANT_CARROT | d20-29 | 39.6 | 25.1 | carrot book +1.5k | 78-84 % |
| HIRE_n | d3-9 / d10-19 | 52 / 111 | 29 / 94 | −0.4k / −1.3k | 100 % |
| land (Q3 day) | d8-9 vs d10 | T 99 % by d9 | P 96 % on d10 | −1.9k d3-9, +0.9k d10-19 | 100 % |
| IDLE_hand_turns | d10-29 | 91 | 475 | ~−0.3k hire cost | T<P 100 % |

Where PFS leads:
- d0 carrot plate: +0.9k.
- d3-9 wheat harvest: +1.6k.
- d3-9 milk (4 cows on d0): +1.9k.
- d10-29 wool (P buys sheep and pastures on d10-19 on 88-90 % of boards): +8.8k.
- Higher realised prices on almost every product (T sells more volume and walks the price down).

PFS's idle hand turns (about 23 per day, d10-29) fall at dawn and dusk (FILLWORK1). At about 15 coins per hire that is under 300/game.

## 2. Money gap decomposition (intact 49; `res/gap_intact10.tsv`, `res/books_intact10.tsv`)
| window | Δcash T−P | sale volume | sale price | costs |
|---|---|---|---|---|
| d0-2 | −595 | −233 | −75 | seed −741, product +736 |
| d3-9 | −4,702 | +4,907 (wool +4.2k, wheat +2.2k, fert +1.8k, milk −2.0k, carrot −0.9k) | −390 | product −4.9k, animal −2.3k, land −1.9k |
| d10-19 | +16,213 | +27,223 (wheat +11.6k, melon +11.6k, fert +2.6k, egg +2.3k) | −2,570 | product −10.1k, hire −1.2k |
| d20-29 | −7,602 | +2,376 (melon −11.1k, wheat +5.4k, egg +2.9k, carrot +2.2k, tomato +1.8k) | −5,182 | product −4.7k |
| **ALL** | **+3,313** | **+25,660** | **+465** | **−22,811** (product −19.0k, hire −1.5k, land −1.1k, seed −0.9k, animal −0.3k) |

Books, T − P, over d0-29:

| book | intact 49 | T>P (intact) | all 160 | T>P (all) |
|---|---|---|---|---|
| wheat | +2,543 | 86 % | +2,628 | 81 % |
| carrot | +1,389 | 82 % | +1,269 | 79 % |
| strawberry | +1,897 | 59 % | −3,776 | — |
| tomato | +250 | — | +225 | — |
| herd | +55 | — | −13,350 | — |
| melon | −168 | — | −963 | — |
| land + hire | −2,652 | T<P 94 % | −2,796 | — |
| **cash** | **+3,313** | | **−16,763** (rival breaks) | |

- **Reconcile:** Δcash equals the reward difference per board, and P and R' match `pfs.csv` on 160/160 boards.
- **Wheat buys:** T's ~570 bought wheat units are resold at about break-even. The whole wheat book gap is the +98 harvested units in d10-19.

## 3. Rule candidates (all in CLOSED families)
1. **Melon-land double crop.** T sows its melon plate on d0-2 (9 seeds, 100 %) and sells it d10-19. It then relays wheat on the freed and new Q3 land from d8 (10.3 and 7.2 wheat plantings on d8-9, against PFS's 3.4 and 2.4). PFS sows 12 melons on d10-15 on that land (7.5 melon tiles d10-19) and sells them d20-29.
   - The melon books are equal, but T also earns the **d10-19 wheat book: +3.35k/game (100 % of boards)**. The gain holds for all 8 teams (+2.5k..+4.4k) and without Q4 (+3.5k, 98 %).
   - Recoverable if PFS matched T: about +3.4k/game one-sided.
   - Family: melon-plate timing (MELON_PLATE_TILES, MELONVRP1, MELONGENES1, P10 gated plate, MELONCOUNTER2) and Q3 d8 (TOPLOSS1 list, LAND_BIAS_ZERO −16.6k). CLOSED as a gift: MELONLOGIC1 Δtheirs +10.5k, t 5.08.
   - Note: PFS's late melon deliberately avoids the MELON rival's d10-19 melon book.
   - Reopen evidence: a paired d0/d2 plate against these 51 BAND MELON seats with Δtheirs ≤ 0. MELONHYBRID1, in flight, is the nearest shape.
2. **Late carrot fill, d17-27.** T raises carrot sowing from 2/day on d17 to 8/day on d26: 45 against 31 plantings on d20-29 (intact; 39.6 against 25.1 on all boards) (78-80 % of boards), and 14.7 against 1.8 on d10-19. Over d22-27 PFS's empty tiles climb from 3.3 to 11.1 while about 24 hand turns a day are passed.
   - Rule: "when a tile frees on d17-24 and ≥ 5 days remain, sow carrot".
   - Recoverable: **+1.3-1.5k/game** one-sided (carrot book d20-29, 82-84 %).
   - Family: RELAYFILL1 / CREW_RELAY / TAIL_FILL / FILLWORK1. REJECTED: RELAYFILL FRAC 1.0 on these seats gave −2 flips, Δours −580 (MELONVOL1, today).
   - Reopen evidence: a carrot-only fill (the rejected relay mixed in wheat, which displaces feed) with paired Δours > 0 and Δtheirs ≤ 0.
3. **Early herd.** T buys 3 sheep on d0 (100 %), then +2.3 cows and 5.7 geese with 5.6 coops on d3-9 (94-100 %). PFS instead buys sheep and pastures on d10-19.
   - Eggs +5.0k and wool d3-9 +3.9k, but **the herd book nets +55 (intact) / −13.4k (all): 0 coins recoverable**.
   - Family: WOOLFIRST1 / GEESE1 / EGGDOSE1 / EGGS2 / HERDTILT, CLOSED.
   - Reopen evidence: none from this census, because the book is flat.

## Files and re-run
- **Files:**
  - `S/opcensusmelon1/`: `ledger.py`, `analyse.py`, `books.py`, `run.sh`.
  - `res/`: census, gap, books, boards and day tables, for all boards and for the `_intact10` / `_intact20` subsets.
  - `res/ledger.jsonl` (56 MB) is not committed. It regenerates in about 12 min.
- **Re-run:** `bash S/opcensusmelon1/run.sh`. It needs replay only and runs 2 processes. The ledger is resumable and picks up new `pfs.csv` rows.
