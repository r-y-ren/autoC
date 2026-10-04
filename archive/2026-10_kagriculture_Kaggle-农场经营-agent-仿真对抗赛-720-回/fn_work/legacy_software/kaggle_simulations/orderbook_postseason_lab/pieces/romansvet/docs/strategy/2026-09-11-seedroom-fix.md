# SEED_ROOM_PURSE_ON: the day-0 seed room, re-solved against the herd the purse bought

2026-09-11, agent `seedroom`. Fixes the switch named in
`docs/strategy/2026-09-11-switch-named.md` (consensus §66).

## The defect

`brain.py`'s `animal_count = _qfloor(xp, animal_share * n_dev)` sits at **6.9913**
for candidate B against the 6.9999 `_qfloor` boundary. A perturbation that carries
the product over the boundary asks for a **7th animal the day-0 greedy never buys**
— the herd is byte-identical on every day of the game — and yet the board is not:

* `plan._seed_room` sizes `ft_ub` on `max(a_want, a_have)`, i.e. on what the brain
  ASKED for, before `budget.grant` prices a single coin;
* one more fresh pasture is charged against the planting capacity, so `seed_cap`
  falls by one;
* `plan._wants` clips the prefix, dropping the last seed of the day;
* day 0 plants 18 instead of 19 and stands one tile **idle for the rest of the
  season**.

Measured here on the 6-board TOPB2 ledger (`S/seedroom/day0.py`), our seat, day 0:

| theta | planted | tile_WHEAT | idle | money |
|---|---|---|---|---|
| B (OFF and ON) | 19.00 | 11.00 | 0.00 | 150.7 |
| crossing `s0p01_p512_minus_a0p03` OFF | 18.00 | 10.00 | **1.00** | 160.7 |
| crossing `s0p01_p512_minus_a0p03` ON | **19.00** | 10.00 | **0.00** | 140.7 |

The whole of the -2,077 coins a board the crossing theta loses on TOPB2 is bought
with those ten coins of unspent seed money.

## The fix that did NOT work (recorded so it is not retried)

The obvious purse-aware reservation — inside `_seed_room`, clip the acquisition to
`a_have + purse // spec.ANIMAL_COST` in list order against the day's own
post-bill, post-reserve `money` — is **INERT**: 0/160 boards moved, on B and on
the crossing theta alike. On the tie board the day ends holding 151 coins, so the
7th animal is affordable *in isolation*; it is unaffordable only against the wheat,
fertilizer and seed the greedy ranks above it. **Affordability is not a property of
the purse, it is the greedy's own answer** — so the switch has to ask the greedy.

## The fix

`SEED_ROOM_PURSE_ON` (plan.py, default False, patch `S/seedroom/plan.patch`, +79/-6
lines in four hunks):

1. the switch constant and its rationale;
2. `_seed_want(xp, view, macro, seed_cap)` lifted verbatim out of `_wants` — the
   seed-purchase want clipped prefix-wise to a seed room — so the second walk asks
   the identical question of a re-sized room;
3. ON, immediately after `n_buy = BUD.grant(...)`: the seed room is re-derived from
   `a_have + a_got` (the animals the grant actually **bought**), and the seed lists
   are re-solved over it with the coins the first walk left outside them. This is
   `PLANT_FILL_ON`'s own second-walk machinery and carries its guarantees: the two
   walks together never pass `purse`, and a threshold on a list whose value per coin
   does not rise can only extend the first answer.

`a_got <= max(a_want - a_have, 0)` (a grant never passes its want), so the new cap
is never smaller than the old one — **the switch can only ever hand a tile back**.

## Measurements (S/seedroom/screen.py = S/simscreen/screen.py on the private tree)

Board sets: `boards_topb2.json` (40) and `boards.json` (LIVE-C hold-out, 120), the
frozen pinned-town lottery-free sets. Switch string
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON` (+`SEED_ROOM_PURSE_ON`).

* **OFF is byte-identical**: B's 40 TOPB2 and 120 LIVE-C rows reproduce
  `S/simscreen/{topb2_40,full120}.csv` to the coin, 0/160 rows differ. The
  `_seed_want` extraction is a pure lift.
* **B ON == B OFF, byte for byte**: 0/40 TOPB2 and 0/120 LIVE-C rows differ, and the
  6-board per-day ledger diff (`S/seedroom/cmpled.py`) is **exactly zero on every
  day and every column** (money, planted, idle, tile_WHEAT, shed, the three animal
  counts, hands). The two-purse displacement question does not arise: `dours` and
  `dtheirs` are both 0. B's own herd want is granted in full, so the reservation
  never binds on the live candidate — **the switch carries zero risk to B**.
* **The crossing theta recovers**:

| family | n | crossing OFF | crossing ON | d | sd | t | gap to B OFF | gap to B ON |
|---|---|---|---|---|---|---|---|---|
| TOPB2 | 40 | -3,548 | -1,779 | **+1,769** | 2,686 | +4.17 | -2,077 | -308 |
| LIVE-C | 120 | +5,179 | +5,238 | +59 | 2,351 | +0.27 | -100 | -41 |

  85 % of the TOPB2 switch and 59 % of the (much smaller) LIVE-C switch are removed.
  `dours +876 / dtheirs -892` on TOPB2: the tile we plant is a unit the tape seat
  does not sell into the same market.

## Decision

Both gates of the escalation are met: crossing ON recovers +1,769/board on TOPB2
(>= +1,200), and B ON vs B OFF is 0 on LIVE-C with `dours == dtheirs == 0`. GO for
engine legs, and they are RUN (`bash S/seedroom/engine.sh all`, 2026-09-11 17:47-18:05Z,
one flock on `/root/kagg3_judge.lock` per runner call):

| leg | n | B | sr_on | dmargin | flips |
|---|---|---|---|---|---|
| TOPB2 | 40 | 32.5 % | 32.5 % | **0** | 0W 0L, 40 ties |
| LIVEC-H30 | 60 | 63.3 % | 63.3 % | **0** | 0W 0L, 60 ties |
| LIVEC-H30B | 60 | 83.3 % | 83.3 % | **0** | 0W 0L, 60 ties |
| LIVE62 | 124 | 85.5 % | 85.5 % | **0** | 0W 0L, 124 ties |

**284 engine games, every one a tie to the coin.** The real engine agrees with the
sim: with `SEED_ROOM_PURSE_ON` the live candidate plays exactly the game it played
without it. This is a **regression check, not a promotion test** — the switch buys
nothing for B and costs nothing; what it buys is the fitness landscape around B.

## Why it matters to the ES

The switch is not an edge in B's play — it is a **cliff in the fitness landscape
around B**. OFF, a perturbation that moves `animal_share * n_dev` across the
`_qfloor` boundary is scored on a board that lost a tile for the whole season, so the
ES reads a -2,077 coin wall on TOPB2 that has nothing to do with the herd it was
asked about. ON, the wall is 85 % gone and the same perturbation is scored on the
play it actually describes.

## Files

* `S/seedroom/plan.patch` — the patch (apply to a private copy of the arms-next
  worktree; `/root/wt_seedroom` carries it).
* `S/seedroom/{screen.py,ledger.py}` — `S/simscreen` / `S/topledger` with a
  `KAGG3_TREE` env override; board files and baselines shared, csv/npz local.
* `S/seedroom/{run.sh,ledger.sh,cross.sh,engine.sh}` — the runs.
* `S/seedroom/{cmp.py,cmpled.py,day0.py,crosscmp.py}` — the pairings above.

## Does the E3b crossing set collapse? No — 13/14 survive

`S/seedroom/cross.sh` + `crosscmp.py`: the 14 thetas the E3b census calls *crossing*
(they move 100 % of boards on BOTH families), screened ON against B on the first 10
TOPB2 boards, with the OFF halves read from `S/onestep_b/csv`.

**13 of 14 still move 100 % of the 10 boards** (only `s0p04_p2048_minus_a0p1` falls
to 8/10). What does shrink is the penalty: the mean paired gain over the 14 goes
from **-1,111 OFF to -783 ON** (-30 %), and the worst offenders improve most
(`s0p04_p512_plus_a0p03` -1,387 → -779, `s0p01_p512_minus_a0p03` -1,417 → -885).

So the `animal_count` tie is **one leg of the cliff, not all of it**: these are
mostly alpha-0.1 steps that move much more than the herd boundary. The fix removes
the largest single day-0 discontinuity; it does not make the one-step landscape
smooth, and the E3 one-step verdicts are not overturned by it.
