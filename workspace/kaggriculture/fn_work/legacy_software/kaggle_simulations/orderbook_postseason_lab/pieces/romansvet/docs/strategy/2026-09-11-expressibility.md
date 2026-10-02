# How much of top-tier play is outside our decoder at all — 2026-09-11

**Question.** Two blind reviews ranked the *action interface* the first
bottleneck (`docs/strategy/2026-09-11-codex-blind-genes.md`). That is a
source-level claim. This measures it: byte-exact action tapes for the 29
top-tier opponents we train against (the 20 w10.2 rungs 107000107…107015773 of
`S/flow209/launch_flow209.sh` plus the nine w4 rungs 107776180…107786235), each
action classified against what our decoder can emit, weighted by the coin it
moves.

Census: `S/express/census.py` (runs in 2 s on CPU), tables in
`S/express/census.md`, per-tape rows in `S/express/census.csv`.

---

## 1. THE EXPRESSIBLE SET (written down before any tape was opened)

Our agent and the tapes live in the *same* representation: `plan.build_day`
(`core/plan.py:5745`) returns `(uop, ua, uq, mop, ma, mq)` shaped
`[30, 17, 24]` / `[30, 24, 10]`, and `es/tape_actions.py:232-265` packs a
recorded opponent's frames into exactly those arrays. So "expressible" is a
set membership question on `(day, turn, slot, op, arg)`, not an analogy.

The intra-day row layout is `src/kagg3/core/ops.py:97-200`, asserted at import
by `ops._check_schedule()` (`ops.py:259`), and emitted at the `plan.py` sites
below. Switch state in `.claude/worktrees/arms-next`: `MELON_OPEN_ON=False`
(`plan.py:643`), `PRESTOCK_ON=False` (`plan.py:2052`), `MARKET_PACK_ON=False`
(`plan.py:2327`), `EARLY_SELL_ON=True` (`plan.py:2463`), `EARLY_SELL_MODE="A"`
(`plan.py:2466`), `ROUTE_SPLIT_ON=True` (`plan.py:2226`).

| row type | can we emit it? | on which turns (SHIPPED) | turns under ANY switch setting | ordering constraint | site |
|---|---|---|---|---|---|
| `MO_HIRE` | yes | 0, 2 | 0, 1, 2 | first in its turn; ≤10/turn | `plan.py:7720`, `:7730`; `ops.py:110,119` |
| `MO_BUY_PRODUCT` | yes, WHEAT/FERT only (the **engine's** rule, `kaggriculture.py:598,606`) | 1 (+ turn 0 on d0 under `OPEN_PUMP_ON`) | 0, 1, 20 | slots 0-1 of the BUY row, WHEAT then FERT | `plan.py:7803,7805`; `ops.py:111` |
| `MO_BUY_SEED` | yes | 1 | 0, 1, 2, 20 | one slot per crop, crop-index order | `plan.py:7807` |
| `MO_BUY_ANIMAL` | yes | 1 | 0, 1, 2 | one slot per animal, after the seeds | `plan.py:7814` |
| `MO_BUY_LAND` | yes | 3 (slot 9) | 0-3 | last in the day's purchase order | `plan.py:8126`; `ops.py:126` |
| `MO_SELL` | yes | **1, 3, 10, 18** | 0,1,3,4,5,10,11,13,15,18 | one slot per product per turn, product-index order; ≤3 lots a day | `plan.py:7860, 8097, 8111`; `ops.py:135` `SELL_TURNS=(3,10,18)`, `:158` `EARLY_SELL_LOT1_TURN=1` |
| unit ops (all 18 of `ops.OP_*`) | yes, every verb | turns ≥ `ROUTE_BASE`=2 | ≥1 (`ROUTE_BASE_PACK`) | PICKUPs in one contiguous block at the route base, then the route | `ops.py:207-236`; plan.py emits all 18 verbs |

**So: four sell turns out of twenty-four, one buy turn, two hire turns, and
units idle until turn 2.** Everything after hour 0 is a replay of a plan built
at hour 0 (`agent/runtime.py:30`) — no intraday branch, no re-buy after a
refusal, no reaction to a price seen at turn 6.

---

## 2. POOLED CENSUS — 29 tapes, 23,806 market rows, 184,309 non-PASS unit actions

Coin is a **reference** figure: sales and product buys priced at spec's base
quote (`spec.DEFAULT_MARKET_PARAMS[p]["base"]`, the quote at inventory `I0`);
hires and land at their exact fixed ladders. The tapes carry no prices and
re-simulating 29 seasons did not fit the budget. 851 "dump the shed" rows
(qty ≥ 900, 745 of them on d27-29) are counted as rows and priced at zero,
which is conservative — they land where we cannot reach anyway.

### Market rows, SHIPPED switches

| class | rows | % rows | coin | % coin | d0-9 | d10-14 | d15-29 |
|---|---:|---:|---:|---:|---:|---:|---:|
| expressible | 7,207 | 30.3 % | 1,218,720 | **17.9 %** | 139,580 | 271,729 | 807,411 |
| inexpressible-time | 15,297 | 64.3 % | 5,330,512 | **78.3 %** | 737,182 | 1,142,778 | 3,450,552 |
| inexpressible-order | 1,119 | 4.7 % | 189,734 | 2.8 % | 11,156 | 17,732 | 160,846 |
| inexpressible-type | 183 | 0.8 % | 66,395 | 1.0 % | 6,675 | 1,405 | 58,315 |
| **total** | 23,806 | | 6,805,361 | | 894,593 | 1,433,644 | 4,477,124 |

Inexpressible share **by day band**: d0-9 84.4 %, d10-14 81.0 %, d15-29 82.0 %
— flat. The hole does not concentrate in a phase; it is the whole season.
By *mass* it is where the money is: 65.7 % of all inexpressible coin is d15-29,
which is the band the loss anatomy already named as the discriminator.

### Market rows, UNION over every switch setting the tree can be built with

| class | rows | % rows | coin | % coin |
|---|---:|---:|---:|---:|
| expressible | 11,684 | 49.1 % | 3,376,499 | **49.6 %** |
| inexpressible-time | 9,837 | 41.3 % | 2,909,199 | 42.7 % |
| inexpressible-order | 2,102 | 8.8 % | 453,268 | 6.7 % |
| inexpressible-type | 183 | 0.8 % | 66,395 | 1.0 % |

Even granting every switch at once — melon lots, prestock, market-pack,
early-sell mode B — **half the coin top-tier opponents move is still placed on a
turn our row builder cannot occupy.** No theta reaches it.

### Unit actions (the farm work)

| class | SHIPPED | UNION |
|---|---:|---:|
| expressible | 173,084 (93.9 %) | 178,169 (96.7 %) |
| inexpressible-time | 5,826 (3.2 %) | 681 (0.4 %) |
| inexpressible-order | 2,154 (1.2 %) | 2,214 (1.2 %) |
| inexpressible-type | 3,245 (1.8 %) | 3,245 (1.8 %) |

**The farm half is not the hole.** The engine's vocabulary is *exactly* ours —
18 unit verbs (`kaggriculture.py:312-543`) and 6 market verbs (`:631-649`),
every one of them emittable (`core/ops.py:6-24`, `:56-71`; `agent/render.py:8-49`).
There is no verb the engine accepts that our decoder cannot produce, so every
discriminator is about *turn, count and order*. The 1.8 % type residue is our
own planner's narrowing, not the engine's: `DROP` only on the terminal day
(`plan.py:5924, 5932`), `PICKUP` only of WHEAT/FERTILIZER/GOOSE/COW/SHEEP
(`plan.py:4041-4045`), `PLACE` only as animal placement (`plan.py:5588`; the
mid-block banking form at `:7614` is dead). 94-97 % of opponent unit actions sit
at turns we can act on. The expressibility gap is in the *market row cadence*.

---

## 3. THE TOP THREE HOLES, by share of inexpressible coin

| # | family | rows | coin | share | concrete example |
|---|---|---:|---:|---:|---|
| 1 | **Sale on a mid-day turn we have no lot on** (2, 4-9, 11-17) | 3,816 | 2,138,720 | **38.3 %** | `107782373` d8 turn 4 `SELL WOOL ×100` — 20,000 reference coin, six turns before our lot 2 at turn 10 |
| 2 | **Sale in the evening tail** (turns 19-23, after our last lot) | 2,424 | 1,321,855 | **23.7 %** | `107782373` d13 turn 21 `SELL WOOL ×100` — three restock ticks after our turn-18 lot closed |
| 3 | **Sale at turn 0**, in front of every market row of the day | 1,188 | 1,113,920 | **19.9 %** | `107015401` d25 turn 0 `SELL MELON ×30` — 7,500 coin quoted before our seat has presented anything |

Those three are one family: **sale timing outside our four lot turns = 81.9 %
of the inexpressible coin.** The remainder is small and scattered — `BUY_PRODUCT`
off the turn-1 row (4.0 %), within-turn slot order we cannot produce (3.4 %),
`BUY_SEED` off it (2.8 %), `BUY_ANIMAL` (2.6 %), `HIRE` at turn 1 (2.2 %, "sell
in the morning, hire with the proceeds"), `BUY_LAND` off turn 3 (1.9 %), and a
second row for the same `(op, arg)` in one turn (1.2 %).

### The mechanism, not just the count

Shops restock every four turns (`spec.SHOP_SELL_INTERVAL = 4`), so a day has
six price windows: turns 0-3, 4-7, 8-11, 12-15, 16-19, 20-23. Our four lot
turns (1, 3, 10, 18) fall in windows 0, 0, 2 and 4 — **we never present a sell
order in windows 1, 3 or 5 at all.** Opponent sell coin landing in those three
windows: 559,510 + 696,810 + 1,168,160 = **2,424,480 of 5,774,300 = 42.0 %**.
Half our own coverage is also wasted: lots 1 and 3 both sit in window 0, so our
three lots really only reach three of six windows.

---

## 4. LOTS (flow208) — does the first added block address this?

`S/lots/policy_lots.patch` adds 130 genes: two independently signed per-product
coin offsets on lots 1 and 2, changing the marginal `quote − press × lot_index`
ramp into an arbitrary three-point shape (`sell.py:97`).

**It adds no turn.** It re-weights the split across the three lots we already
present, all of which are already inside the expressible set. Therefore:

- **Coverage of the inexpressible coin: 0 %, by construction.**
- Its entire reach is the **20.2 %** of opponent sell coin (1,169,160 of
  5,774,300) that lands on turns 1/3/10/18 — and only the part of that which is
  a *mis-split*, not a mis-timing.

That does not make flow208 worthless — a better split inside three turns is a
real, cheap, 130-gene lever, and the block is proven inert-at-zero and
decodable at σ. But on this measurement it is a **minor hole, not the main
one**: the main one is that eight of every ten coins the top tier moves are
placed on a turn our row builder never occupies, and no reshaping of three
existing lots can follow them there. The interface change that would close the
measured hole is **more sell turns** (and a `HIRE` row after the morning lot),
not a richer function on the three we have.

---

## 5. Judgement: ~50 points or ~500?

**Closer to 500 than 50, but the measurement does not prove it, and the coin
figure is an upper bound on the prize, not the prize.** What the census
establishes is exclusion, not margin: we sell the *same goods*, and the cost of
selling them at turn 18 instead of turn 21 is only the price difference between
two market states, not the whole 1.3M coin the evening tail carries. The honest
read is the restock-window one — the top tier touches six price windows a day
and we touch three, half our lots doubled up in one of them. Against a ladder
where the top-10 cutoff is ~2,967 and our equilibria sit at 2,562-2,722, i.e. a
250-400 point climb, a lever that doubles the number of price windows our seat
can quote into is of the right order; every closed hand-lever family
(`counterfactuals-overstate`, the wool/mix/melon families) was a *re-ordering
within* the existing cadence, which is exactly the class this census says is
already ~19 % of the board. The cheap falsifier is direct and does not need a
gene at all: add a fourth and fifth `SELL_TURN` in windows 1 and 5
(`ops.SELL_TURNS`), pay the ~6 % simulator throughput each, and run one paired
250-board leg at B. If two more windows buys nothing in the engine, the
interface claim is refuted for ~4 hours of compute and flow208 keeps its slot.
If it buys, the interface is the path and the gene count never was.

**Caveats.** (i) Reference pricing, not live quotes — a sale's true coin depends
on the inventory it meets. (ii) The 851 dump-all rows are priced at zero, so the
d27-29 tail is understated. (iii) Unit-op "order" is only checked for the
PICKUP-block rule; route orderings we cannot walk are not counted, so the unit
expressible share of 95.7 % is an over-estimate. (iv) `BUY_PRODUCT` at turn 0 on day 0 (the `OPEN_PUMP_ON` row, `plan.py:7778`)
is scored inexpressible here, which slightly overstates the hole; it is inside
the 4.0 % `BUY_PRODUCT` family. (v) These 29 tapes are
top-tier; the 2200-band clone we lose to has a different cadence and is not
measured here.
