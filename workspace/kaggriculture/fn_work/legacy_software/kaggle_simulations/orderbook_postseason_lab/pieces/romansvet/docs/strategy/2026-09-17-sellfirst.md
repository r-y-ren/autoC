# SELLFIRST — V46's market-list partition is the order we already emit: ceiling 0, STOP

2026-09-16 22:45–23:10Z, branch `sellfirst` off `e55d66f`. Successor to
`2026-09-16-slotprio.md`; raised by `2026-09-17-nbintel3.md` sect.2 row `_adv_frontload`,
the one V46 layer that doc marked UNMEASURED. Tool `S/sellfirst/census.py`, output
`S/sellfirst/census_eng22.txt`. No public code read or copied (mechanics only).

## 0. VERDICT — **STOP at step 1. Zero rows affected, ceiling 0 coins, nothing built.**

Over **22 ENG22 boards / 2,248 emitted market rows** with the shipped FT2 switch set,
the V46 partition "SELLs, then BUY_PRODUCTs, then the rest" permutes **0 rows**:

    rows                       2248     (102.18 / game)
    rows_v46_permutes             0     <-- the whole result
    mixed_rows                  590     ( 26.82 / game)   turn 1: 589, turn 3: 1
    rows_at_cap (10 orders)     371     ( 16.86 / game)
    buyproduct_before_sell        0     other_before_sell   0
    same_item_rows                0

It is the **identity permutation**, so both purses move 0 and no kill gate was run.

## 1. THE ENGINE RULE
`.venv/.../kaggle_environments/envs/kaggriculture/kaggriculture.py:544` `_process_market`:

* **:557** `queues.append(q[:max_orders])` — the list is truncated at 10 **per seat per
  turn**; rows past index 9 are dropped in silence.
* **:561** `for i in range(max_len)` — strictly **per-index sequential**. Within index `i`:
  **:571-579** the atomic HIRE / BUY_LAND resolve first in player order, then **:583-620**
  a per-unit lockstep quotes BOTH seats off the *same* running `market["inventory"]` and
  commits both; **:628** `_refresh_prices` runs after every index.
* So index order is load-bearing on exactly three channels: (i) truncation, (ii) the
  inventory (hence the quote) a later row meets, (iii) money — `_commit_unit` (:652) caps
  a BUY at cash on hand, so a SELL ahead of a BUY funds it.

## 2. WHAT WE EMIT TODAY (and why it is already sorted)
`agent/render.market_actions` (`src/kagg3/agent/render.py:31`) walks slots 0..9 of
`plan._market`'s row and drops `MO_NONE`, so **slot order == list order**.

| row | content | order |
|---|---|---|
| turn 1, merged BUY row | lot 1's sells + the day's purchases | half (a) of `SELL_SLOT_PRIORITY`, `plan.py:11429-11452`, puts the sell block at offset 0 and the buys behind it (shipped ON, `plan.py:4440-4442`) |
| the buy block itself | `DEFAULT_ORDER = (B_WHEAT, B_FERT, B_SEEDS, B_ANIMAL)`, `plan.py:4362` | the only two `BUY_PRODUCT` slots (wheat, fertilizer) are already slots 0-1, ahead of every `BUY_SEED`/`BUY_ANIMAL` |
| `SELL_TURNS[0]` | nine sells + `BUY_LAND` in the **last** slot (`plan.py:4357`, `sim/market.py:156`) | sells first, "the rest" last |
| hire rows | HIRE only under shipped `EARLY_SELL_MODE = "A"` (`plan.py:3168`) | nothing to sort |

So `SELL ≺ BUY_PRODUCT ≺ rest` holds on every row **by construction**, not by luck — and
the census confirms it on every one of 2,248 real rows. **A `SELL_FIRST_ON` switch would
be a no-op.** Truncation is unreachable too: the 371 full rows are exactly 10 wide
(`MO = 10`, `plan.py:139`) because `_market`'s `fits` predicates refuse an eleventh order.

## 3. THE ONE CELL V46 WOULD PERMUTE — and why we refuse it
Half (a) declines to move the sells when the day **buys** wheat/fertilizer and lot 1
**sells that same item** (`same_item`, `plan.py:11441-11445`), or on `OPEN_PUMP`'s day.
That row is the SELL-vs-BUY_PRODUCT **cross** (`sim/market.py:672`). It fired **0 times in
2,248 rows**. Lifting the guard is anyway `OPEN_PUMP`'s round trip run backwards
(sell into a high shelf, then buy it back cheaper) — family CLOSED at §115b
(`2026-09-16-v45leg.md`, +410/+367/+335, t 2.2-2.4).

## 4. STANDING
The market-row family is now closed on all four of its halves: extra row (`lot5`),
overflow row (`sheddump`), within-sells rank (`slotprio`, SHIPPED), and **sells-vs-buys
index order (here — already optimal)**. `nbintel3` sect.2's last unmeasured V46 layer is
answered: we shipped it on 2026-09-16, one release ahead of them.

## 5. REPRO
    cd /mnt/e/_work/kaggriculture3-sellfirst
    JAX_PLATFORMS=cpu .venv/bin/python S/sellfirst/census.py --tapes 22
