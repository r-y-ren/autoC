# SELL5 — five sell lots instead of three, measured at candidate B

2026-09-11, review worktree `.claude/worktrees/arms-next`.
Patch `S/sell5/sell5.patch`, commands `S/sell5/README.md`.

## The claim under test

The 29-tape census (`docs/strategy/2026-09-11-expressibility.md` §3-5) found
78 % of the coin the top tier moves placed on market turns our planner never
occupies, and 42 % of their sell coin landing in the three shop-restock windows
we skip.

The windows, read off the engine rather than off the "every four turns" summary
(`S/sell21` derived this the same afternoon from the interpreter: the market
phase runs BEFORE `_town_consume`, which fires on `step % 4 == 0`, so the town
ticks at turns 0, 4, 8, 12, 16, 20 and `projector.ticks_before` gives turns
18/19/20 five ticks and 21/22/23 six):

| window | turns | our lots, shipped |
|---|---|---|
| A | 1-4 | lot 1 (turn 1 under `EARLY_SELL` mode A, turn 3 as fallback) |
| B | 5-8 | — |
| C | 9-12 | lot 2 (turn 10) |
| D | 13-16 | — |
| E | 17-20 | lot 3 (turn 18) |
| F | 21-23 | — |

SELL5 takes B and D. Window F is the one this switch deliberately does not
reach, and it is the largest single hole on the loss band
(`docs/strategy/2026-09-11-expressibility-band.md`: 25.3 % of LOSS10 sell coin,
turn 21 alone 12.1 %) -- that is `S/sell21`'s switch, not this one.

The cheap falsifier: give the day two more lots, in windows B and D, and
measure at B's own theta, paired, in the real engine. If the interface is the
binding constraint the extra rows should be worth coin at B's genes; if they
are not, the constraint is somewhere else.

## What was built

An **environment** switch `KAGG3_SELL5`, read at import in `core/ops.py`. It
has to be environment and not a `plan` attribute: `sell.N_LOTS`,
`plan.MIDDAY_PLACE_V2_TURN`, `plan.BANK_LOT` and `sim.rollout._SELL_ONLY_TURNS`
are all fixed at *import* off `O.SELL_TURNS`, and the judge's `setattr` switch
string is applied after the modules are in.

| value | lots | press ramp |
|---|---|---|
| unset / `0` | `(3, 10, 18)` | `press * lot_index`, the shipped program |
| `1` | `(3, 7, 10, 14, 18)` | `press * lot_index` as-is — the pressure RANGE grows `2*press` → `4*press` |
| `2` | `(3, 7, 10, 14, 18)` | rescaled `2/4`: `0, p/2, p, 3p/2, 2p` — same range the shipped three spanned, so B's `press` genes keep their meaning |
| `3` | **NOT BUILT** | see below |

`SELL_TURNS[0] = 3` and `SELL_TURNS[-1] = 18` are unchanged, so `TURN_PRESTOCK`,
the DROP-day turn budget, `MIDDAY_PLACE_V2_TURN`, the day-29 chain and the
BUY_LAND slot all read the turn they always read. Three anchors move with the
layout, each written so that OFF is the literal it always was:

* `plan.BANK_LOT = O.SELL_TURNS.index(O.SELL_TURNS_BASE[1])` — the lot standing
  on **turn 10** (index 1 OFF, 2 ON), so `BANK_BEFORE_LOT_ON` (live in B's
  switch string) banks into the same row at the same hour and its DROP deadline
  `drop_t <= O.SELL_TURNS[BANK_LOT]` is the same turn 10 it was;
* `plan.MELON_LOT_EARLY_TURNS` steps off turn 7 to `(6, 8, 9)` under the switch
  — its collision assert is unconditional (`ops` cannot read `plan`), and turn 7
  is a lot row now. Cosmetic: `MELON_OPEN_ON` is False and the melon hand family
  is closed;
* `plan.early_lot_turns()` returns `O.SELL_TURNS` under the switch whatever the
  `EARLY_SELL` mode. Modes "B"/"A21" relocate lots 2 and 3 *of three* and have
  no five-lot reading. **B ships mode "A"**, which returns `O.SELL_TURNS` on
  both paths anyway — its lot 1 rides `TURN_BUY` through `_rows`' `early_fits`,
  not through `early_lot_turns`.

`ops._check_layout` (`_check_schedule`) passes with the switch on, plus three
new invariants: the first and last lot turns are the shipped ones, the shipped
three are a subset, and the tuple is strictly increasing.

### Why `KAGG3_SELL5=3` (a sixth lot, window 5) was not built

A lot at turn 21 needs `TURN_PRESTOCK` moved to 22 — that part is an
ops-assertion change only, and it passes. But it also moves `SELL_TURNS[-1]`
from 18 to 21, and **plan.py anchors read that value directly**:

* `turn_budget` (plan.py ~3171 and ~6165) is `O.SELL_TURNS[-1] + 1 - route_base`
  on a DROP day, and `DROP_ON = True` is live in B's build — a DROP day's crew
  would get three more turns;
* `MIDDAY_PLACE_V2_TURN = int(O.SELL_TURNS[-1])` (plan.py ~932) and the
  `_midday_place_turn()` deadline chain;
* the day-29 terminal chain reasoning in §4 of the module docstring, which is
  keyed on the last lot standing at turn 18.

That is a planner change, not an interface one, so it is documented and not
built. To build it: pin `MIDDAY_PLACE_V2_TURN` and the two `turn_budget` sites
to `O.SELL_TURNS_BASE[-1]` (18) rather than `O.SELL_TURNS[-1]`, re-derive the
DROP-day budget proof for a 21-turn last row, and add `TURN_PRESTOCK = 22` under
the switch. Roughly a day's work with its own falsifier, and on the evidence
below it is not worth it.

## Inert check (switch OFF)

| check | result |
|---|---|
| sim screen, board `107463847` seed `4674845` | `mine 94698  theirs 98435  margin -3737  shop_sig 132` — the coin-exact numbers `S/lots/test_judge_pad.sh` records for B on the unmodified tree |
| **engine**, TOPB2 40 games (`sell5off_B_topb2.csv` vs `flow193_g100_hr_topb2.csv`) | **byte-identical** |
| **engine**, LIVEC-H30 60 games | **byte-identical** |
| **engine**, LIVEC-H30B 60 games | **byte-identical** |

160 engine games, every coin identical with the switch off.

`pytest tests/test_sell_allocator.py tests/test_melon_open.py` — 21 passed with
the switch off. With `KAGG3_SELL5=2` nine of them fail, all on three-lot
literals (`assert [20, 0, 0, 0, 0] == [20, 0, 0]`; the melon test asserts
byte-identity to the pre-switch planner). The allocator's answer is unchanged —
all 20 units still go to lot 1 — so these are expectations written against
`N_LOTS == 3`, not defects. A build that ever shipped five lots would have to
re-express them against `SELL.N_LOTS`.

## Sim screen (S/simscreen/screen.py, hr switches, paired on identical boards)

Paired with `S/sell5/pair_screen.py` (two seats of a board averaged into one
observation before the spread, as `S/bank/paired.py` does).

| board set | variant | n rows | win % OFF → ON | mean Δmargin | SE | t | games identical |
|---|---|---|---|---|---|---|---|
| TOPB2 40 | `1` | 40 | 32.5 → 32.5 | −1 | 42 | −0.02 | 0/40 |
| TOPB2 40 | `2` | 40 | 32.5 → 32.5 | **+26** | 25 | +1.05 | 2/40 |
| LIVE-C hold-out 120 | `1` | 120 | 71.7 → 71.7 | +21 | 40 | +0.53 | 6/120 |
| LIVE-C hold-out 120 | `2` | 120 | 71.7 → 71.7 | **+43** | 15 | +2.91 | 12/120 |

The switch is live — 0/40 games identical under variant 1 — and worth almost
nothing: both variants are inside the screen's own ±400/board resolution.

## Engine legs (real engine, paired, `--seed-per-opponent`, hr switches, theta B)

Theta B is `artifacts/kagg2_games/thetas/flow193_g100_hr.npy`, **md5
`7fcf39485bae65ee84171957c5843814`** — identical to `submission/theta.npy` in
the main checkout. The dispatch quoted `41b87adc`; that md5 matches nothing on
disk, and `S/sell21` hit the same discrepancy the same evening.

B's own csvs for the same boards and seeds are the OFF side
(`S/lossflip/flow193_g100_hr_{topb2,livech,livech2}.csv`), and the byte-identical
control legs above prove they are what this tree plays with the switch off.

### `KAGG3_SELL5=2` (rescaled ramp — B's press genes keep their meaning)

| leg | n games | boards | wins OFF | wins ON | mean Δmargin | SE | t (boards) | W / L flipped |
|---|---|---|---|---|---|---|---|---|
| TOPB2 | 40 | 20 | 32.5 % | 32.5 % | **+35** | 28 | +1.24 | 0 / 0 |
| LIVEC-H30 (43-72) | 60 | 30 | 63.3 % | 63.3 % | **+44** | 20 | +2.24 | 0 / 0 |
| LIVEC-H30B (73-102) | 60 | 30 | 83.3 % | 83.3 % | **+52** | 38 | +1.38 | 0 / 0 |

### `KAGG3_SELL5=1` (raw ramp — the pressure range doubles)

| leg | n games | boards | wins OFF | wins ON | mean Δmargin | SE | t (boards) | W / L flipped |
|---|---|---|---|---|---|---|---|---|
| TOPB2 | 40 | 20 | 32.5 % | 32.5 % | +50 | 68 | +0.73 | 0 / 0 |
| LIVEC-H30 (43-72) | 60 | 30 | 63.3 % | 63.3 % | +9 | 75 | +0.12 | 0 / 0 |
| LIVEC-H30B (73-102) | 60 | 30 | 83.3 % | 83.3 % | −15 | 75 | −0.20 | 0 / 0 |

Variant 2 is positive on all three legs; variant 1 is noise with one leg
negative — which is the expected sign of the ramp argument: at variant 1 every
one of B's `press` values is charged over a lot index that runs 0..4 instead of
0..2, so a gene trained for three lots means something else.

**Not one game changed hands in 320 paired engine games.** The whole effect is
a +35..+52 coin drift on games decided by thousands.

## Why the effect is that small: where the coin actually goes

`S/sell5/lotprobe.py` wraps `plan.build_day` over one real engine game
(tape 107448662, seed 777001, theta B, hr switches) and tallies the units the
planner offers per market turn over the whole season:

| turn | OFF units (days with a live row) | `SELL5=2` units |
|---|---|---|
| 1 (lot 1, `EARLY_SELL` mode A rides the BUY row) | 913 (28 days) | 913 (28 days) |
| 7 (new, window 1) | — | 25 (12 days) |
| 10 | 51 (14 days) | 26 (12 days) |
| 14 (new, window 3) | — | 27 (14 days) |
| 18 (last lot) | 477 (20 days) | 450 (20 days) |
| **total** | **1441** | **1441** |

The two new rows carry **52 of 1441 units, 3.6 %**, and every one of them is
taken out of turns 10 and 18 — the season's total volume is identical to the
unit. 63 % of the day's sell volume already leaves on the *first* row and 31 %
on the *last*: `sell.allocate`'s pressure term and its later-lot externality
make the greedy either sell at once or wait for the deepest shop recovery, and
the windows in between are worth nearly nothing to it. The planner is not short
of rows. It is short of a reason to use them.

That is the direct answer to the census: the 42 % of opponent sell coin in
windows B/D (the census's 1 and 3) is **not** reachable by adding rows at B's
genes. B declines the
rows when it has them.

### Against the two parallel readings of the same afternoon

* **TIMING-PRIZE** (`docs/strategy/2026-09-11-timing-prize.md`, 21:40Z) repriced
  96 live replays and read variant (b), "every lot four turns earlier = SELL5's
  turns 7 and 14", at **−346 / −508 coins a game**: FALSIFIED as a revenue play.
  The engine at B says **+35 / +44 / +52**. Both are right, and the lot probe is
  why: SELL5 does not *move* a lot four turns earlier, it *adds* a row and lets
  the allocator decide -- and the allocator moves 3.6 % of the volume, not 100 %.
  The ledger priced a counterfactual the planner never chooses.
* **SELL21-BUILD** (22:04Z) took the other end of the day, `SELL_TURNS[-1]`
  18 → 21, and the sim screen at B read **−1,134/game (t −8.87)** on the LIVE-C
  hold-out: the ledger's "later pays" sign refuted by the opponent term -- our
  531 units at turn 18 are depressing the price the *other* seat sells into, so
  lot 3 at turn 18 is denial and worth more than its own price window. SELL5
  never touches turn 18's row size by more than 27 units of 477, which is
  exactly why it does not pay that cost -- and also why it cannot collect the
  prize.

Read together: the day's sell schedule at B is close to a local optimum of the
*allocator's own objective*, and both directions off it -- earlier rows (this
doc) and a later last row (`S/sell21`) -- are level or worse in the engine. The
sell-timing family reads closed at B's genes, for the fourth time
(`counterfactuals-overstate`).

## Throughput cost

Steady-state simulator throughput, `S/simscreen/screen.py` with `--chunk`
sized so a whole chunk after the first is compile-free (the chunk-2 minus
chunk-1 delta is pure episode time), single process, 4 threads, CPU:

The box was carrying other agents' screens all evening, and a run measured on
its own reads 10-15 % apart from the next one (a lone OFF run timed 21.0, 11.9,
12.0 and 13.7 s for four compile-free 40-episode chunks). So OFF and ON were
run **simultaneously**, which makes the contention symmetric, twice:

| run | OFF chunk deltas (40 eps) | ON (`SELL5=2`) chunk deltas |
|---|---|---|
| paired run 1 | 9.9 s, 9.7 s | 10.1 s, 9.9 s |
| paired run 2 | 9.6 s, 9.8 s | 10.0 s, 10.0 s |
| **mean** | **9.75 s / 40 eps = 4.10 eps/s** | **10.00 s / 40 eps = 4.00 eps/s** |

**−2.5 % episode throughput** for the two extra lots (+2.6 % episode time),
and +1 % on the trace compile (209.0/189.6 s OFF vs 210.9/191.4 s ON, chunk 1).
The `ops.SELL_TURNS` docstring's "~6 % of episode throughput each" is an
overstatement for this path: two extra sell-only market resolutions out of a
24-turn day cost about 1.3 % each here, because `sim/rollout.turn_body` takes
the cheap `sell_only=True` branch on them and the unit phase, `town_consume`
and `decay_plants` dominate a turn.

Measured with `S/simscreen/screen.py --boards 120 --chunk 40`: chunk 1 carries
the compile, chunks 2 and 3 are the same batch shape and so compile-free, and
their deltas are pure episode time.

A training arm would therefore pay ~2.5 % per generation. That is affordable in
itself -- it is the prize, not the price, that fails below.

## Verdict

**SELL5 LEVEL.** Variant 2 beats B by +35 / +44 / +52 coins a game on TOPB2 /
LIVEC-H30 / LIVEC-H30B — positive on all three paired legs, but with zero games
flipped, t below 2 on two of the three, and a size two orders of magnitude under
the margins that decide these boards. Variant 1 is noise. This is not a lever at
B's genes and it must not be promoted on these numbers.

It is also **not a refutation of the interface claim** in the only sense that
matters for training: the switch is live (0/40 games identical), it is inert
when off to the coin over 160 engine games, its direction is consistent, and the
lot probe shows the constraint is the ALLOCATOR's preference and not the row
count. B's `press` and `hold` genes were fitted against three lots; under five
they have never been asked what an intermediate window is worth.

### Is a training arm on SELL5 warranted?

**No, not as the next arm — and not as a sell/press-only arm at all.**
The throughput price (−2.5 %/generation) is affordable; the prize is not there.

* The ceiling is small and it is measured, not assumed: the new rows move 3.6 %
  of the season's volume and the total volume is unchanged. Even if training
  placed every one of those 52 units perfectly the prize is a few hundred coins
  a game, well inside the ±2,000/board engine noise these legs carry.
* An arm that trains only `sell`/`press` genes is training the genes that
  *decline* the rows. The probe says they decline them because selling later is
  weakly worse under the pressure+externality model at B's quotes, not because
  the values are mis-set. That is a model change, not a fitting problem.
* The throughput cost is real and is paid on every episode of the arm (see
  above), against a prize inside the noise.

What the evidence *does* argue for, if the intermediate windows are ever to be
worth taking: change what the allocator believes about them. The two candidates
the probe points at are (a) the later-lot externality, which currently charges
lot `l` for the whole telescoped drop on every later lot and so over-penalises
an early-window sale once there are five of them, and (b) the fact that lot 1 at
turn 1 takes 63 % of the volume before any window comparison happens at all. The
switch built here is the vehicle for testing either; it is ready and inert.
