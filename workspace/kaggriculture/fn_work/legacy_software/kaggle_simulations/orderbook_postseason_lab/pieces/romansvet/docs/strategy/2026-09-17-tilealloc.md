# TILEALLOC — the work assignment at TILE level (`_routes`), built and REJECTED

2026-09-16 22:32–23:10Z, branch `tilealloc` off master `79a3aee`. Follow-up to
`2026-09-16-routecut.md` §6, which closed the block BOUNDARY by a theorem and
named what was left: a tile-level allocator, a unit working a tile out of the
MIDDLE of its neighbour's block. Leg: ENG22 (44 games) vs the FT2 control.

## 1. VERDICT

**The transfer is buildable, it fires, and the engine does not pay for it:
ENG22 −335/board, sd 2,763, t −0.57, board win 40.9 → 40.9 %, flips +0/−0, 20
of 44 games changed.** Both purses fall (ours −427 t −1.43, theirs −92 t
−0.55): not a gift to the other seat, just work the day does slightly worse.
The constrained ceiling it was built against is real (+1,932/board, §2), but
the re-instrument says the walk goes UP: `mid_move` 8.929 → 8.963 a unit-day,
moves 10.175 → 10.192, prod ops 10.340 → **10.327**.

**The cause is that the turns the transfer frees are already spent.** The
stealer pays out of the turns the greedy cut could not use — but with
`TAIL_FILL_ON` those are not idle: the filler already walks them to the
NEAREST carry-free op (`tail_move` 0.000 both ways), so a steal trades a cheap
tail hop for a dearer task hop, and the loser's freed turns are recut into
ranks that cost their own walk. Same shape as EVESTOCK and ROUTEEFF.

`TILE_ALLOC_ON` ships **OFF**, pinned byte-identical to `79a3aee`. With
ROUTEORDER (order, +433/−175) and ROUTECUT (boundary, ≤ 0 by theorem), the
**route-walk family is closed on all three handles**: the order inside a block,
the boundary between blocks, and the assignment of tiles across blocks.

## 2. The constrained ceiling (`S/tilealloc/ceiling.py`, 22 ENG22 boards, d20-29)

`S/routecut/cut_ceiling.py` plus two arms constrained **exactly like the rule**:
adjacent units only, no intra-block re-ordering, every shed interaction pinned
to its own turn (each slot's steps ≤ its window), a tile consuming a carried
input may not leave its unit-day.

| arm (d20-29) | moves saved /unit-day | 1:1 | at 2.211 steps/op |
|---|---:|---:|---:|
| ORDER (free intra-slot order, no migration) | 1.318 | +7,061 (t 15.8) | +3,389 |
| ADJ (+ adjacent migration, free order) | 1.702 | +8,790 (t 15.5) | +4,310 |
| **XFER** (migration only, cheapest insertion) | **0.514** | **+2,915** (t 12.7) | **+1,341** |
| **XFER_RANK** (migration only, RANK insertion) | **0.334** | **+1,932** (t 10.7) | **+893** |

The transfer alone is **+1,932/board 1:1, +893 at 2.211 steps/op** — over the
+450 build bar. Walk identity 10.17/10.17 moves a unit-day.

## 3. The switch — `TILE_ALLOC_ON` (OFF), plan.py:2534 (constants), :10489 + :10553 (day geometry), :10834 (the transfer pass), :10944 (decode hand-off), :11326 (`covered`)

* **Steal.** A pickup-free rank `j` ahead of the block (`idx > e + 1`, within
  `TILE_ALLOC_LOOK` 12, not beside an existing hole) is appended to the block's
  walk for `dist(last tile, j) + n_ops[j]` turns, refused unless the unit that
  would have walked it gives back strictly more (`seg[j] + move[j+1] −
  dist(j−1, j+1)`): the day always spends strictly fewer turns on the same
  work. One steal a unit (`TILE_ALLOC_PASSES`), dearest first.
* **Hole.** Every later unit skips a stolen rank; its block is a prefix with
  holes, decoded by `_ro_block`'s mask with a RANK key, so the route's shape is
  unchanged. A block that inherited a hole is recut against `bud + sav`
  (`ROUTE_ORDER_ON`'s "spend the saving"), taken only if the REAL swept clock,
  return leg included, fits the window.
* **Gates.** Only pickup-free ranks move, so `d_pick`, `d_lead`, `blk` and
  pickup-before-use are untouched; never on a DROP day; never from a unit with
  no successor; never from an excursion block (`ins == 0` — it may still
  inherit a hole, which can only make its deposit turn sooner, read off the
  real clock); the shed gate in `ROUTE_ORDER_SHED_GATE`'s form. `covered`
  carries the stolen ranks.

`tests/test_tilealloc.py` (12 pass): whole-plan sha256 OFF-identity vs
`git archive 79a3aee src`; the transfer fires on a spiky geometry; no tile
worked twice; turn-budget invariant at three budgets, drop day and not; the
shed-visit-never-later invariant; pickup before use; `covered` carries the
steal; three-way mutual exclusion; jit.

## 4. Legs (control `S/lossflip/ft2_eng22.csv`, `S/nexthigh/pair.py`)

| leg | Δ/board | sd | t | ours | theirs | board win | flips |
|---|---:|---:|---:|---:|---:|---|---|
| **ENG22 (22 boards, 44 games)** | **−335** | 2,763 | **−0.57** | −427 (t −1.43) | −92 (t −0.55) | 40.9 → 40.9 % | +0/−0 |

Per game Δ −335 se 412 t −0.81; 20 of 44 games changed, so this is a live
null-to-negative read, not an inert one. Re-instrument (2,572 unit-days,
d20-29, ON vs OFF): `mid_move` 8.929 → 8.963, `dawn_move` 1.246 → 1.229,
`tail_move` 0.000 → 0.000, moves 10.175 → 10.192, prod ops 10.340 → 10.327,
distinct tiles 5.047 → 5.053. No V45LEG, no POOLED180: the kill gate (+100,
t 2) is not met.

## 5. Standing

* **The assignment is reachable and worthless at this margin.** `_cut`'s
  contiguity is no longer the binding law (the mask decode expresses any
  per-tile assignment, proven on the engine); what binds is that the crew has
  no free turns to re-allocate — the tail filler holds them.
* **Every walk-priced ceiling here is over-stated by the value of a tail hop**
  (ROUTEEFF / ROUTEORDER / ROUTECUT / TILEALLOC all price a saved MOVE as
  1/2.211 of a prod op, right only when the turn would be idle). The next such
  ceiling must be measured against `TAIL_FILL_ON`, not against idleness.
* What is left on the route is a different objective: a different SET of tiles
  (admission) — ADMITSLACK's ledger.

## 6. Repro

```bash
WORKERS=3 bash S/tilealloc/run_all.sh instrument eng22    # 22 boards, ~3 min
.venv/bin/python S/tilealloc/ceiling.py                   # the constrained ceiling
.venv/bin/python -m pytest -q tests/test_tilealloc.py     # 12 tests, OFF identity
FT2="OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,\
brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True,LOT4_ON=True,LOT4_TURN=17,\
SELL_SLOT_PRIORITY_ON=True,FERT_TIMING_ON=True,FERT_TIMING_DAYS=2"
WORKERS=3 bash S/judge7065/run_eng22.sh tilealloc artifacts/kagg2_games/thetas/\
flow193_g100_hr.npy /mnt/e/_work/kaggriculture3-tilealloc "$FT2,TILE_ALLOC_ON=True"
.venv/bin/python S/nexthigh/pair.py S/lossflip/ft2_eng22.csv S/lossflip/tilealloc_eng22.csv
```
