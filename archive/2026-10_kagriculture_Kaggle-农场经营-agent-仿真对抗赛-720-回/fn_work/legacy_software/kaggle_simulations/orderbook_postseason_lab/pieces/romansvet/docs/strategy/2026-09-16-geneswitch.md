# The switch genes: `plan`'s constants become theta coordinates

2026-09-16, branch `geneswitch` off `4c6565b`. Answers the program redirect
(`2026-09-16-program-redirect.md`): stop hand-flipping `plan`'s `NAME_ON`
constants one judged arm at a time; let training decide the vector. ES from B
on the *existing* genes reads -124 +/- 47, so the search needs new expressible
dimensions -- and 66 of them sit in the source as constants.

## 1. What is gene-able (all 66 in `S/geneswitch/switches.md`)

| class | n | what it is |
|---|---|---|
| A | 5 | already one select/ternary on a value the day computes anyway |
| B | 15 | an `if` around value computation; rewrites to `where`, both branches built |
| C | 46 | **structural** -- rows, turns or route blocks, read at trace-construction time (`early_lot_turns`, `route_turns`, `_routes`, `MACRO_SCHEDULE`) |

That 46 is the finding. A traced bit cannot move a shape, so this gene layer
reaches 30 % of the hand-flip surface; the rest -- LOT4, the sell slots, the
pump, prestock, the routes, every market row -- needs a shape-static superset
program with masked rows first, i.e. the action interface.

## 2. The block

`policy.SHAPES` gains `("sw", (32, 10))`, `("swb", (10,))` at the tail: 330
params, 7,065 -> 7,395, an append, so every earlier theta is an exact prefix.
**Decode** (`brain.SWITCH_GAIN = 8`, `brain.decide`):

    z = gh @ sw + swb                       # [10], off the global head
    flip_i = round(SWITCH_GAIN * z_i) > 0   # _qfloor(8*z + 0.5) > 0
    switch_i = module_default_i XOR flip_i

A deadband, not a sign test, one-sided like `press`/`compact`: at `z = 0` it is
`floor(0.5 + eps) == 0`, so the untrained block is every switch exactly where
the module ships it -- the pair ships identically and a shorter theta decodes
byte for byte. A sign test would put half the population on the far side of all
ten at once and leave the centre a point selection never returns to. Read off
`gh`, so a gene-switch may depend on the board -- strictly wider than a
constant that could only be set for the season.

**Precedence, one comparison** (`plan._sw`, the `FORWARD_ADMIT_ON` rule): a
module constant the lead has moved off its shipped value is a manual override
and wins outright, so `S/drainpin/on2b.py` and every paired A/B runner still pin
a switch against any theta. Otherwise the theta rules.

**Both backends** (`_sw_pick` / `_sw_macro`, the `_static_horizon` pattern):
`_sw` hands numpy a Python `bool` -- the shipped program takes its original
branch and builds no `where` -- and a trace a 0/1 tracer with both branches.

## 3. Wired (K = 10: every A, plus the bounded-cost B)

`FEED_MANDATORY_ON`, `SURVIVAL_WATER_ON`, `ANIMAL_DEFER_ON`, `CARE_HOLD_ON`,
`FERT_VOLUME_ON`, `SHED_DEFICIT_ON`, `CREW_PUSH_COST_ON`, `WHEAT_VOLUME_ON`,
`LATE_STRAW_CAP_ON`, `ENDGAME_TOMATO_ON`. Excluded by judge read:
`FERT_RESERVE_ON` (-32.7k, t -7.5), `MACRO_EXEC_ON`, `SPREAD_ROWS_ON` (-1,802);
everything else is C. One repair the wiring forced: `crew_push_cum()` re-read `CREW_PUSH_COST_ON`
inside itself, so a gene asking for the push got the flat table. It takes an
`on=` override now; the no-arg call is unchanged.

## 4. Evidence
* **Slope** (`S/geneswitch/slope.py`, 4,096 antithetic members off B, 8
  recorded boards): **17.0-17.7 %** of the population decodes a flip per gene
  at sigma 0.02, **34.9-36.4 %** at 0.05; 1.7 flips a member, 17 % flip
  nothing -- a minority, so the centre is still the plan most members make
  [GENE SLOPE RULE]. Gain 8 *is* that measurement: 16 reads 31.6 % / 3.2.
* **Identity**: whole-plan sha256 on 9 boards x (champion decode, hand fixture)
  against a pristine `git archive 4c6565b src` tree -- equal; three further
  `..._byte_identical_to_head` pins pass against the same commit.
* **Equivalence**: each of the ten, forced ON by gene, plans byte for byte what
  the flipped module constant plans, on all 9 boards; 9 of 10 provably move a
  plan or a `_derive` chain there (`SHED_DEFICIT_ON` needs a day the fixtures
  do not reach).
* **Tests**: `tests/test_geneswitch.py`, 32 tests, green. Against the fork
  commit the 19-file regression set goes 29 red -> 26 red: **no new failure**,
  and the three that flip green are identity pins.
* **Compile**: first `jax.jit(build_day)` is **204.1 s** vs **169.2 s** at
  `4c6565b` on the identical board, +21 % -- the price of ten `where`-selected
  sites (`S/geneswitch/compile_time.py`, same fixture both trees).
* **Sim** (`S/simscreen/screen_gs.py`, 40 frozen TOPB2 pinned-town boards):
  `ENDGAME_TOMATO_ON` by gene (`swb[9] = 8`) and by constant give the identical
  margin on **40 of 40 boards** (win 22.5 %, -5,105 both ways). Its own read is
  -4,406, t -2.49 against B -- it loses, the 2026-09-16 tomato verdict, and now
  something the ES can find on its own.

## 5. Launch
`S/geneswitch/launch_remote.sh` prints the command; it does not ssh or run.
`STAGE=block` is `--train-only sw,swb`: 330 coordinates, B held byte for byte,
~22x the samples per live coordinate, and the only arm whose result *is* a
switch vector -- ten bits the lead can read off. Widen to `STAGE=all` only if it
moves. Seat: the 44 fresh 09-16 clone tapes (`S/v45leg2/ids.txt`), pinned towns.
Rsync the tree first: against `master/src` the arm trains nothing.

## 6. Risks
1. **Compile** +21 %; widening much past ten wants a measurement, not a guess.
2. **Ten at once**: 1.7 flips a member, so credit assignment is noisier than a
   hand-judged arm -- the redirect's own trade; `--train-only` limits the cost.
3. **Board-dependence cuts both ways**: `_sw` can say ON on day 3 and OFF on day
   20, so a gene arm does not transfer back to a fixed-switch claim.
4. **30 % coverage**: the switches the ladder reads most are all class C.
5. The suite was already 29 red at `4c6565b` (test-triage in flight): this is a
   delta, not a green board.
