# `test_no_tile_write_collisions`: the 7 baseline hits are a gate-definition problem

Follow-up to `2026-09-10-ship-pair.md` §7. Worktree `ship-pair` (`b9b732b`);
scripts `S/simgate/{enumerate_hits,wide,fid}.py`.

## 1. The collisions

Reproduced exactly: 7 pair-OFF, 8 with `BANK_BEFORE_LOT_ON`. Tile state read in
view (serpentine) space, `view.kind[SERP_INV[tile]]`.

| trial | turn | tile | units | ops | tile |
|---|---|---|---|---|---|
| 12 | 22 | 34 | 0, 3 | CARE + FEED | COOP, animal 1 |
| 23 | 22 | 31 | 3, 6 | CARE + HARVEST | COOP, animal 1 |
| 46 | 14 | 0 | 0, 5 | COLLECT_FERT + CARE | PASTURE, animal 2 |
| 51 | 21 | 18 | 2, 6 | HARVEST + CARE | COOP, animal 0 |
| 52 | 22 | 21 | 2, 13 | COLLECT_FERT + CARE | PASTURE, animal 0 |
| 56 | 23 | 17 | 1, 2 | CARE + HARVEST | PASTURE, animal 0 |
| 57 | 23 | 5 | 0, 13 | HARVEST + CARE | COOP, animal 2 |
| **5** | **11** | **33** | **3, 4** | **FEED + CARE** | **COOP, animal 1** (bank arm) |

## 2. Code path

`TAIL_CARE_ON = False` takes all 8 to **zero** (`ROUTE_SPLIT`, `TAIL_FILL`,
`SURVIVAL_WATER`, `FEED_MANDATORY` do not). Source: the tail care hop in `plan.py:~7480`
(`_routes`, the `c_ok`/`care_free` block), which `plan.py:2649` documents —
*"the 'tiles no block holds' rule is dropped outright: the tile a block already
ran its ops on is the case that pays."* `care_free` still keeps two **tails**
off one tile, so the only possible collision is one tail hop against one route
block: the route sweep's disjointness is intact, the tail steps outside it.
`n_units` is not over-counted — it equals the sim's own
`real = arange(MU) < 1 + nhands` mask, and every hit is at turn >= 11.

## 3. Engine rule (`kaggriculture.py:312, 480-530, 935-939`)

Strictly sequential, farmer then hands in index order. The second action on a
tile is **applied, not refused** — each op carries its own day flag:
`fed_today` (checked *before* the wheat is taken), `cared_today`,
`fertilizer_available`, `yield_units`. Animal HARVEST does not clear the tile
(only a non-ongoing PLANT harvest does), so for distinct animal ops the engine
is order-independent.

## 4. Fidelity

The four animal ops write disjoint arrays in `sim/units.py`: CARE -> `t_cared`,
FEED -> `t_water`, COLLECT_FERT -> `t_favail`, animal HARVEST -> `t_yield`
(`h_animal` is deliberately not in `reset_meta`). `S/simgate/fid.py` replays
each of the 8 through `apply_units` both ways: **parallel scatter == sequential,
8/8, every field.** At 400 trials: 30 collisions, all on animal tiles, all
*distinct* animal-op pairs, **0 same-op pairs, 0 non-animal tiles**. Pinned
tapes agree (`2026-09-10-flow172-g60-live-anatomy.md` §1): 110 board-seats, mean
abs sim-engine diff 154 coins, W/L agreement 100 %, corr 1.000.

## 5. Verdict

**Gate over-counts — real collisions, no coin impact.** Two units on one
*animal* tile is legal, order-independent and deliberately taken.

**Recommendation: fix the gate.** Assert disjointness per *written array*, not
per tile — exempt distinct animal ops on an animal tile; keep failing on a
same-op pair or any `reset_meta` writer (PLANT/PLACE/BUILD/DIG/one-shot
HARVEST), which would still duplicate inventory or race a tile write.
