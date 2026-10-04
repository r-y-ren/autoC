# MELONAUDIT1 (2026-09-27 15:54Z-16:40Z): rule-miss bug hunt on the band MELON cell under PFS

**Verdict: NONE. No bug-class rule miss is worth ≥ 300 coins/game where we are worse than the rival.**
- The only flagged category is (e), the sale walk and floor dumps. It traces to two design choices, and neither is a rule that fails to do what its docstring says:
  - the 3-lot sale schedule;
  - a learned reservation `hold` of about 0.
- The loss is VOLUME. In the 37 losses the rival sells **2,231 units/game vs our 1,594** (+637; d10-19 866 vs 462). Its revenue is **164.9k vs 123.1k**.
  - In the 14 wins the volumes are equal: 1,553 vs 1,593 units.

## Bed (`S/melonaudit1/play.py`)
- **Seats:** the 51 BAND-leg MELON seats (`S/bandleg1/boards_all.json`, fam MELON), replayed with src = master (PFS on).
- **Harness:** the bandleg1 harness (SAFETY_S 1e9, REPAIR_MS 1e7, actTimeout 600, head_940, theta7659, orig seat). The engine replay is kept this time. The leg itself deletes its replays, so this is why the seats were replayed.
- **Fidelity:** **51/51 byte-exact** to `S/bandleg1/res/pfv1.csv`. The split is 37 losses / 14 wins.
- **Loss margins:** ≤ 3k: **5**, ≤ 5k: **7**, ≤ 10k: **15**, ≤ 20k: 32, > 20k: 5. Median 11.3k.
  - Only 7 of the 37 losses are within 5k; this is not a near-miss cell.
- **The rival** is a fixed tape. Its misses are its live ones, and its market rejects include open-loop divergence.

## Census (`bash S/melonaudit1/run.sh`, ~1 min on the cached replays)
- Values are means per game, in coins, at each game's own quotes.
- **These are ONE-SIDED counterfactuals** (no price impact, no rival response). Under the TWO-PURSE rule, none of them is a paired result.
- **Care reconciliation:** the care attribution (a) sums exactly to CREWAUDIT1 care_lost + escape (ours 2,348, rival 5,718 on losses).

| | category | losses: ours | losses: rival | losses: present (ours) | wins: ours | wins: rival |
|---|---|---|---|---|---|---|
| a | unfed on placement night (exact; cow misses are cap-absorbed) | 194 (8.35 nights, 7.43 of them COW) | 438 | 100 % | 139 | 330 |
| a | unfed, no wheat on farm / shed full (room) | 69 / 0 | 642 / 0 | 100 % / 0 | 193 / 0 | 39 / 0 |
| a | unfed with wheat on farm (choice) / fed but uncared | 1,432 / 309 | 3,785 / 503 | 100 % | 1,740 / 186 | 3,938 / 392 |
| b | dried plantings / over-ripe decay | 22 / 121 | 787 / 326 | 19 % / 51 % | 51 / 183 | 1,748 / 519 |
| c | fert with no bonus in its window / outside the growth window | 64 / 0 | 71 / 7 | 76 % / 0 | 21 / 0 | 77 / 6 |
| d | OPEN_PUMP fired on d0 | 37/37 games | 3/37 | – | 14/14 | 2/14 |
| e | sale gap vs the day's max quote | **12,044** | 11,631 | 100 % | 10,626 | 9,427 |
| e | of which own-step walk (pre-step quote − price) | **8,872** | 4,925 | 100 % | 7,560 | 4,026 |
| e | floor sales (price ≤ 5): units / at the next day's max quote | **70 u / 1,014** | 45 u / 741 | 100 % | 68 u / 821 | 59 u / 697 |
| f | product unsold at d29 (shed / hands) | 0 / 15 | 40 / 3 | 0 / 3 % | 0 / 0 | 249 / 1 |
| g | shop buys never used | 35 | 114 | 16 % | 4 | 487 |
| h | hands with < 6 productive ops × their hire cost | 287 (8.4 hands) | 471 (22.4) | 100 % | 273 | 573 |
| i | land bought, share of its quadrant never planted/built | 4 | 35 | 5 % | 0 | 60 |
| j | rejected unit ops / market units / atomic-PLANT blocks (count) | 4.7 / 23.1 / 0 | 58 / 125 / 6 | – | 4.5 / 22.9 / 0 | 147 / 59 / 20 |

- **(j):** our 23 market rejects are SELL orders larger than shed stock. That is over-ordering the engine truncates, and it is benign. Our 4.7 unit no-ops are water/harvest on tiles already done.
- **Flag rule:** ours ≥ 300, worse than the rival, and present in ≥ 50 % of losses. **Only (e) passes**: walk +3,947, floor +757, next-day hold value +272.

## Traces of (e) (`trace_sell.py`, `trace_hold.py` → `trace_hold.log`; both runs reproduce the leg's scores exactly)
**mhw 113460543**, a −11.3k loss.
- d19 h17: SELL MILK 38, quote 139 → 59.
- d21 h17: SELL MILK 30, quote **63 → 1**.
- Planner at d21:
  - `hold` = [0,0,7,2,0,3,**0**,0,0]. MILK hold is 0.
  - `sell.allocate` puts all 30 milk in lot 3 (turn 18) voluntarily. No forced-overflow units are involved.
- The milk market recovered only 59 → 63 over two days. The 30 units exceed what the town drains.

**hamedvakili 114125877**, a −0.7k loss.
- d26 h17: WOOL 23, 151 → 37.
- d28 h17: WOOL 16, **82 → 1**.
- `hold` WOOL = 4 and 3. This is again a voluntary lot-3 allocation.

**What decides it:**
- `src/kagg3/core/brain.py:1309`: `hold = 0.8·base·softplus(z)/softplus(0)`. The logit z is learned (theta7659/head_940), and it decodes to 0-7 coins against bases of ~100.
- `src/kagg3/core/sell.py:104` (`allocate`): sells every unit whose adjusted marginal ≥ hold.
- `src/kagg3/core/ops.py:126`: `SELL_TURNS = (3, 10, 18)`, 3 lots per day. Ours use 78 sell-steps/game; the rival uses 256.

**Classification: CHOICE, not a bug.** The decode and the allocator do what their docstrings say. The reservation is a learned value that trained to "release same day". Both alternatives were already measured:
- more lots per day: 4 lots −77 (t −0.5), 5-lot falsifier, sell21c (`2026-09-10-sell-hour-headroom.md`, `2026-09-11-sell5-falsifier.md`);
- cross-day holding: SELLAUDIT1 paired replay gift, SELL AXIS CLOSED.

The floor dumps are the tail of thin markets that we over-supply: WOOL 28, STRAWBERRY 17, MILK 12, MELON 7, FERT 6 units/game. The one-sided 962 coins/game of "hold to tomorrow" assumes a recovery the curves do not show.

## Streams (≤ 2)
1. **FLOORHOLD1 (cheap, falsifier).** A price floor for WOOL/MILK/STRAWBERRY in `plan._sell_hold` (plan.py:6776, same machinery as FERT_FLOOR/CARROT_EARLY_HOLD). Grid the floor at 0.1/0.2/0.3 × base.
   - Judge on the 142 band seats plus dev 0-9 V56.
   - Prior: SELLAUDIT1 predicts a gift. Upper bound: the one-sided 962 coins/game, which is optimistic.
2. **None on the rule side.** The MELON loss is d10-19 sale VOLUME (+404 units/game to the rival), which the census attributes to no rule miss.
   - The rival misses more in 12 of the 17 valued categories (we are worse only in the 4 (e) rows and in unsold-in-hands, +13), and it still sells more.
   - Any build here is a production-capacity question (already CLOSED axes: HERD, FILL, Q4, RELAY), not a bug fix.

## Files
- `S/melonaudit1/`:
  - `run.sh`: one command. It replays when a replay is missing, then runs the census.
  - `play.py`, `census.py`, `sellshape.py`, `trace_sell.py`, `trace_hold.py`, `trace_hold.log`.
  - `bed.tsv`, `play.csv`, `out/census.{tsv,md}` + the CREWAUDIT1 tables, `checkpoint.txt`.
  - `gz/` (69 MB) is not committed; `run.sh` regenerates it in ~7 min.
- **Clean-shell verify:** `env -i … bash S/melonaudit1/run.sh S/melonaudit1/out_verify`. compare.py reports IDENTICAL; census.tsv and games.tsv are byte-identical.
