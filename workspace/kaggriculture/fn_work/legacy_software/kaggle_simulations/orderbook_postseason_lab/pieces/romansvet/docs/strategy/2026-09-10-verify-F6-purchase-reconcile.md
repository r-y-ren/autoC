# Verify F6 — "purchases finalized against queued work, not final execution"

Independent verification of finding 6 of `docs/2026-09-10-planner-findings.md` (= finding 7 of
`docs/reviews/planner-2026-09-10/REVIEW.md`). 2026-09-10; read-only on every worktree.

**VERDICT: PARTLY CONFIRMED — mechanism and counts exact, cost refuted.**
The interface mismatch is real, reproduces to the coin, and is present unchanged in the shipped
tree. Its measured cost is a one-day float, not a loss: **≈20 coins/game of seed is still
unplanted at day 29** (0.02 % of score, ~1/70 of the LIVE62 per-game SE). Not a promotable
lever — code hygiene only. Do not spend judge time on it.

## 1. Source — purchase is sized before the route, and nothing reconciles it

`.claude/worktrees/ship-pair/src/kagg3/core/plan.py` (reviewed tree):

| line | what |
|---|---|
| 5354 / 5399 | `wants_pre = _wants(...)` / `wants` — seed want from the gene target and **free tiles**, never from the route |
| 5443 | `n_buy = BUD.grant(xp, values, costs, wants, purse, room)` — the purchase greedy |
| 5447-5448 | `fert_bought = min(n_buy[L_FERT], room - wheat_buy)`; `seed_buy = n_buy[L_SEED0:...]` |
| 5475 | `plant_eff = xp.minimum(fill_target, view.seeds + seed_buy)` — **the day's PLANT task set is sized _from_ the purchase**, the reverse of the claimed direction |
| 6142 | final `_derive(...)` — the purchase is final here |
| 6514 | `(route_op, ..., blk, covered, ...)` — **first moment the executed set exists** |
| 6606 | `wheat_reserved = sum(d.want_feed)` — queued feeds, not `blk[0]` |
| 6614 | `fert_reserved = d.n_fert_eff` — queued applications, not `blk[1]` |
| 6894 | `mkt = _market(xp, d.wheat_buy, d.fert_bought, d.seed_buy, ...)` — pre-route quantities emitted verbatim |

Between 6514 and 6894 nothing reduces `d.seed_buy` or `d.fert_bought`. The only consumers of
`covered`/`blk` are the shed-overflow projection (`picks_out`, 6659) and the dead `_prestock`
(5847; `PRESTOCK_ON = False`, 2065; `PRESTOCK_SEEDS = False`, 2092).
**Claim 1 confirmed: sized before the route, no reconciliation step exists.**

**Shipped-tree difference:** `diff ship-pair/src/kagg3/core/plan.py ship-pair-hr/...` is exactly
one line — `3523 HIRE_ROW_ON False -> True`. `budget.py` and `sell.py` are byte-identical.
The finding applies to the shipped composition unchanged.

## 2. Reproduction, and the fate of the excess

`docs/reviews/planner-2026-09-10/games.json` reproduces **exactly**: 27/120 day-plans,
37 wheat + 22 carrot + 1 tomato + 4 melon, **1,180 coins**; 5 plans / 7 fertilizer;
0 excess wheat reservations. Arithmetic checks against `spec.CROP_SEED_COST` (10/20/50/100/80).

**Scope correction:** the "four baseline games" are **three distinct trajectories** —
`107244033` seat 0 and seat 1 are byte-identical. 24 of the 27 excess plans and 1,080 of the
1,180 coins are one game counted twice. Distinct totals: **15/90 day-plans, 640 coins.**

**Fate of every purchased seed unit (FIFO by purchase day, over the traces' own ledger):**

| | wheat | carrot | tomato | melon | coins |
|---|--:|--:|--:|--:|--:|
| planted same day | 360 | 153 | 46 | 63 | 21,500 |
| planted 1-2 days later | 37 | 18 | 1 | 4 | **1,100** |
| planted >2 days later | 0 | 2 | 0 | 0 | 40 |
| never planted by d29 | 0 | 2 | 0 | 0 | **40** |

**1,140 of the 1,180 coins (96.6 %) are planted, 1,100 of them within two days.**
The residual 40 coins is 2 carrot seeds — one distinct event counted twice. The claim's own
caveat ("not measured lost profit") is correct; the float is ≈1 day long.

Carryover identity `stock[d+1] = stock[d] + buy[d] - ops[d]` holds on 118/120 rows; the two
misses (d26 of the duplicated game, +1 carrot) are an emitted carrot PLANT the engine refused,
so `seed_ops` slightly *overstates* use and the metric slightly *understates* over-purchase.

**Fertilizer is a different quantity.** `fert_reserved` withholds units from the morning sale
lot; it is not a purchase. The 7 units cost one day of price timing plus shed room, **not
7 units of coins**. `games.py` never recorded `fert_bought`, so the traces cannot price
fertilizer over-*purchase* at all — that part of the finding is unmeasured, not measured small.

## 3. Independent incidence, current shipped composition

`S/drainpin/on2b.py` from `ship-pair-hr`, theta `flow172_g1000.npy`, switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON = True`, LIVE-C tapes
`107429978` / `107430502`, both seats, `--seed-per-opponent --seed-base 777001`,
`--replay-dir`. 4 games in 70 s. Seat 0 ≡ seat 1 on both boards again → 2 distinct trajectories.

Ledgered from engine truth (`private["seeds"]` deltas), not from the action stream:

| board | seeds bought | planted | unplanted at d29 | coins dead | excess-buy day-plans |
|---|--:|--:|--|--:|--|
| 279044179 (107429978) | 229 | 227 | 2 CARROT | **40** | 2/30 (5 u, 80 c; 40 c planted next day) |
| 4674845 (107430502) | 197 | 195 | 2 WHEAT | **20** | 2/30 (4 u, 40 c; 20 c planted next day) |

Every emitted BUY_SEED was accepted. **99.1 % of all seed ever bought is planted.**
Across all five distinct trajectories now measured (3 review + 2 mine) the terminal dead seed
is 0, 0, 40, 40, 20 coins — **mean ≈20 coins/game against ~85,000 coins scored.**
Fertilizer: 14 / 4 units bought, 211 / 196 applications (nearly all fertilizer comes from
COLLECT_FERTILIZER), 8 / 11 units left unsold in the shed at the end.

## 4. Archive — what has already been priced

- **`PRESTOCK_SEEDS` (2026-08-30, `docs/PLANNER_V3_1.md:776-885`) — measured and rejected:
  0/24 games, mean margin −90,863 vs +10,702.** That is buying *further ahead*; the opposite
  direction of a reconciliation fix, and the only seed-purchase timing read on record.
- `PRESTOCK_ON` (feed+fert): paired diff −334, sd 7,707, **t = −0.21, n=24**; never re-confirmed,
  and VOID/broken on this lineage since `EARLY_SELL_ON` (assert `plan.py:2478`;
  `S/glut/verdicts.log:31,35` — idle-agent 3,000-coin signature).
- `FERT_FLOOR` dead four ways: HELD42 −3,551 **t −16.77** (+0/−8), LEG20 −3,172, TOPB −4.3k,
  LIVE-C22 −3.9k. Shipped OFF; there is currently no price floor on any reservation.
- `FERT_VOLUME`: LIVE62 standalone +746 t 4.0, but **CLOSED as a package candidate 2026-09-10**
  — on top of hire-row it drops wins 88.7 → 86.3 % (pure denial margin).
- `SHED_OVERFLOW_ON = False` (plan.py:565): the residue of unreached reservations is destroyed,
  measured at 473 units / ≤675 coins per game — but the built repair is **byte-inert on the
  pinned judge** (band6 190/192 identical, +1 coin) and closed 2026-09-06.
- **No paired read exists for "buy exactly what you plant" (buying *less*) or for a
  route → purchase resource ledger.** This finding is genuinely new; it is also the smallest.

**The shed-room coupling does not apply to seeds.** Engine `_do_buy_seed`
(`kaggriculture.py:367`): *"Seeds live in private['seeds'] ... they never pass through farmer
inventory or the shed"*; the price is the constant `CROPS[item]["seed"]`, with no market curve
and no `SHED_CAPACITY` clip. `plan.py:5865` says the same. Unplanted seed costs neither shed
room nor any opponent-facing price. It applies only to the fertilizer half.

## 5. Verdict, the exact paired test, dead ends

**PARTLY CONFIRMED.** Mechanism: confirmed, exact lines above, shipped tree included.
Counts: confirmed to the coin. Cost: **float, not loss — ≈20 coins/game terminal dead seed**,
about 1/70 of the LIVE62 per-game SE (~1,486). Two orders of magnitude below what any judge
here can resolve. The finding is a correct description of an interface, not a lever.

**If anyone still wants the paired read** — add `RECONCILE_BUY_ON` (default False) and, after
`covered/blk` at 6514, recompute
`planted[c] = sum((chain_op==OP_PLANT) & (chain_a==c) & covered)`,
`seed_buy' = min(seed_buy, max(planted - view.seeds, 0))`, `wheat_reserved' = sum(blk[0])`,
`fert_reserved' = sum(blk[1])`, and pass `seed_buy'` into `_market` at 6894. **Do not trim
`fert_bought` the same way without re-deriving `proj_eod`** — it is the room the overflow
projection at 6659 is sized against. Then, with
`SW="OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,RECONCILE_BUY_ON=True"`:
`S/topb2/run.sh recon <wt> artifacts/kagg2_games/thetas/flow172_g1000.npy "$SW"`, then
`S/livec/run.sh`, then `S/live62/run.sh` (same args), paired against the g1000pair baseline.

**Expected two-purse signature:** ours **+≤20/game**, theirs **exactly 0** — seed price is a
constant, so not buying a seed cannot move any quote the opponent trades against; the
reconciliation has *no denial channel at all*. Any movement on their purse, or more than ±20 on
ours, is displacement (freed coins changing the grant's later choices, or a fert trim moving the
forced-overflow sale), not the fix, and the arm must be rejected. At 1/70 of the SE the test
cannot resolve it either way.

**Dead ends recorded.**
1. *Counting seeds from the dumped action stream.* The replay JSON renders 32 of ~195 PLANT
   actions per game as a bare `"PLANT"` string with no crop, spread across all days. That
   inflated a first pass to 72/120 day-plans and 5,340 coins. The `private["seeds"]` ledger
   shows all 195 plantings consumed a seed (163 tagged + 32 bare = 195 = 197 bought − 2 left),
   so the bare strings are a **replay-dump serialization artifact**, not engine no-ops and not
   a planner defect. Ledger seeds from `private["seeds"]`, never from the action stream.
2. *Shed-room hypothesis for seeds* — refuted at the engine and in plan.py (section 4).
3. *`seed_ops`-based excess* counts an engine-refused PLANT as use (1 unit in 120 day-plans),
   so it is a slight under-count; immaterial at this size.
4. *"Four games" in this review family is at most two or three trajectories* — pinned tapes make
   seat 0 and seat 1 produce identical play on some boards. Both the review's set and mine hit
   it. Any future incidence count on pinned tapes must de-duplicate before reporting an n.
