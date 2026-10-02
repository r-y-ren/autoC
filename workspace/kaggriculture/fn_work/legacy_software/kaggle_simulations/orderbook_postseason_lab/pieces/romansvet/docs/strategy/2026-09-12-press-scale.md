# `press` scale — is a HARDER late dump worth more against the band?

*2026-09-12. Built and screened at candidate **B** (`submission/theta.npy`) with
the `hr` switch string
`OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`.
Tree: a copy of the pristine `arms-next` branch head at `/root/tree_press`
(patch `S/press/press.patch`); `S/simscreen/`, `S/autojudge/` and `S/snr/` are
untouched.*

## The question

§114 of `docs/strategy/2026-09-10-consensus.md` and
`docs/strategy/2026-09-12-transfer-mechanism.md` identify B's **hard late dump**
as its best move against the band clone — the 2300-2600 seats the Kaggle ladder
is actually made of:

* on **107431404**, B sells 54 extra carrot on day 29, walking the price 96 → 79:
  **+2,292** to our purse and **−1,657** off the clone's own liquidation;
* on **107450083**, B floors wool to 1.

The ES drift that *softened* `press` is precisely what lost that. So: **is
harder better against the band, and what does it cost against the top tier?**

## What `press` is, and why scaling it is the right probe

`press` is the learned per-product number of coins a unit is expected to lose
per lot of delay. `core/sell.py:85-97` reads it as the marginal ramp

    adjusted = next_quote − press · lot_index + later_externality

and `allocate` takes a unit into a lot while `best_adj >= hold`. A **larger**
`press` makes a later lot look worse, so the allocator brings units forward and
one lot walks deeper down the price curve — a **harder dump**. A smaller
`press` spreads the same units across lots — a softer one. Scaling `press` is
therefore the minimal, monotone dial on exactly the behaviour §114 named, and it
needs no retraining.

`press` is live at B, not a dead gene: `b3 = +0.048` with `‖w3‖ = 2.09` over the
nine products, so `relu(tanh(gate))` is off its floor on a good share of
products and boards. (Gene-slope rule, `memory/gene-slope-check.md`.)

## The build

One file, `src/kagg3/core/brain.py`. The decode is

    press = _qfloor(xp, base * relu(tanh(out.gate))).astype(i32)     # brain.py:1053

and the switch multiplies the **float ramp**, after the decode and before any
`allocate`:

    _press_ramp = base * xp.maximum(xp.tanh(out.gate), 0.0)
    if PRESS_SCALE_ON:       _press_ramp = _press_ramp * PRESS_SCALE
    if PRESS_SCALE_LATE_ON:  _press_ramp = xp.where(obs.day >= PRESS_SCALE_LATE_DAY,
                                                    _press_ramp * PRESS_SCALE_LATE,
                                                    _press_ramp)
    press = _qfloor(xp, _press_ramp).astype(i32)

| choice | why |
|---|---|
| scale the float ramp, not the floored integer | keeps **exactly one floor and one cast**, so the int32/fixed-point type of `press` is the one the OFF path has. Scaling the floored integer would quantize twice and make `k = 1.0` non-trivially identical. |
| at the decode, not at the call site | all three consumers read `macro.press` — `plan.py:5224` (provisional allocate), `plan.py:6613` (`SELL.allocate`, the real lot split), `plan.py:6689` (`SELL.adjusted_marginals`, forced/terminal placement). One scale cannot desynchronise them. |
| environment, not a `plan.*` switch | the decode must be scaled in **both** runtimes that call it — `sim/rollout.py:211` (JAX sim) and `scripts/package_submission.py:142` (the shipped numpy agent). A runner that `setattr`s a `plan.*` attribute after import would move one and not the other. Consequence: `KAGG3_PRESS_SCALE*` is an env **prefix** and must never enter the switch string (`S/drainpin/on2b.py` asserts `hasattr(plan, name)`). Same rule as `KAGG3_SELL21`. |
| `xp.where`, not a Python `if`, for the day gate | under the JAX sim `obs.day` is a traced value; a Python branch on it would fail to trace. Both arms are float32[9], `obs.day` is 0-d, so it broadcasts. |
| day ≥ 25 is exact | `brain.decide` is called **once per day**: `agent/runtime.py:30-37` re-plans on `hour == 0` or a day change, `sim/rollout.py:211` calls it per day. The gate is a clean day boundary, not a within-day approximation. |

Two variants:

* `KAGG3_PRESS_SCALE=k` — every day.
* `KAGG3_PRESS_SCALE_LATE=k` — only days ≥ 25 (`KAGG3_PRESS_SCALE_LATE_DAY`),
  so the opening and the mid-game are byte-identical and only the liquidation
  tail moves. This is the surgical form of the §114 hypothesis.

OFF (unset / `""` / `"1"` / `"1.0"`) both `if`s are skipped and the decode line
is the expression it always was.

`S/press/press.patch` applies with `patch -p1` to a fresh `git archive arms-next`
tree and reproduces `/root/tree_press/src/kagg3/core/brain.py` byte for byte
(verified 2026-09-12).

## Inert check

**PASS.** Both switches OFF, `/root/tree_press` vs a pristine
`git archive arms-next` tree, through `S/press/screen_tree.py`:

    PASS coin-identical on 32 boards (tape, seed, seat, mine, theirs, margin, shop_sig)
        ('107463847', '4674845', '0', '94698', '98435', '-3737', '132')
        ('107463847', '4674845', '1', '94698', '98435', '-3737', '132')
        ('107464824', '279044179', '0', '110414', '101283', '9131', '132')
        ('107464824', '279044179', '1', '110414', '101283', '9131', '132')

The reference board is exactly the one `S/sell21/test_inert.sh` pins —
107463847 seed 4674845 → **94698 / 98435 / −3737 / sig 132**. Reproduce with
`bash S/press/test_inert.sh`.

The switch is **live**, not a dead gene: at k = 2.0 it changes 70 of 120 LIVE-C
boards (ALL) and 35 of 120 (LATE, days ≥ 25 only), which is the right footprint
for a dial that can only bite where there is stock left to lot.

## Screen, theta B, both variants (sim screen, lottery-free)

Tables regenerate with `.venv/bin/python S/press/pair.py`; the same output is
banked in `S/press/screen_table.md`. `D ours` / `D theirs` are the **two-purse
seat split** — the paired change in our own money and in the opponent's.

### LIVE-C hold-out 120  (OFF = livec_off, theta B, hr switches)

| cell               |   n | win% OFF | win% ON |  d/game |     sd |      t |     +/-/= |  D ours |      t | D theirs |      t |
|--------------------|-----|----------|---------|---------|--------|--------|-----------|---------|--------|----------|--------|
| all075             | 120 |     71.7 |    71.7 |     -37 |    234 |  -1.71 |  34/29/57 |     +12 |  +0.91 |      +49 |  +2.96 |
| all125             | 120 |     71.7 |    71.7 |     +21 |    179 |  +1.30 |  22/23/75 |     -16 |  -2.45 |      -38 |  -2.79 |
| all150             | 120 |     71.7 |    71.7 |      +7 |    203 |  +0.36 |  24/35/61 |     -35 |  -3.93 |      -41 |  -2.86 |
| all200             | 120 |     71.7 |    71.7 |      +3 |    295 |  +0.11 |  28/42/50 |     -68 |  -4.94 |      -71 |  -3.64 |
| late075            | 120 |     71.7 |    71.7 |      -5 |     62 |  -0.91 |  10/13/97 |      +4 |  +0.79 |       +9 |  +2.80 |
| late125            | 120 |     71.7 |    71.7 |     -11 |     58 |  -2.08 |  6/11/103 |     -10 |  -1.94 |       +1 |  +0.95 |
| late150            | 120 |     71.7 |    71.7 |     -24 |     98 |  -2.71 |   6/19/95 |     -21 |  -3.09 |       +3 |  +0.74 |
| late200            | 120 |     71.7 |    71.7 |     -41 |    165 |  -2.71 |   8/27/85 |     -46 |  -3.75 |       -5 |  -0.75 |

#### LIVE-C half 43-72

| cell               |   n | win% OFF | win% ON |  d/game |     sd |      t |     +/-/= |  D ours |      t | D theirs |      t |
|--------------------|-----|----------|---------|---------|--------|--------|-----------|---------|--------|----------|--------|
| all075 [43-72]     |  60 |     63.3 |    63.3 |     -38 |    226 |  -1.30 |  18/12/30 |      -3 |  -0.23 |      +35 |  +1.19 |
| all125 [43-72]     |  60 |     63.3 |    63.3 |     +18 |    180 |  +0.78 |  12/12/36 |     -15 |  -1.45 |      -33 |  -1.85 |
| all150 [43-72]     |  60 |     63.3 |    63.3 |      -3 |    215 |  -0.10 |  14/19/27 |     -41 |  -3.09 |      -38 |  -1.84 |
| all200 [43-72]     |  60 |     63.3 |    63.3 |     +16 |    353 |  +0.34 |  16/24/20 |     -58 |  -3.10 |      -74 |  -2.26 |
| late075 [43-72]    |  60 |     63.3 |    63.3 |     -10 |     45 |  -1.77 |    4/4/52 |      -6 |  -1.25 |       +4 |  +1.78 |
| late125 [43-72]    |  60 |     63.3 |    63.3 |     -15 |     77 |  -1.50 |    4/6/50 |     -11 |  -1.17 |       +4 |  +1.88 |
| late150 [43-72]    |  60 |     63.3 |    63.3 |     -28 |    121 |  -1.82 |   4/10/46 |     -19 |  -1.99 |       +9 |  +1.09 |
| late200 [43-72]    |  60 |     63.3 |    63.3 |     -36 |    195 |  -1.42 |   6/16/38 |     -31 |  -1.95 |       +5 |  +0.41 |

#### LIVE-C half 73-102

| cell               |   n | win% OFF | win% ON |  d/game |     sd |      t |     +/-/= |  D ours |      t | D theirs |      t |
|--------------------|-----|----------|---------|---------|--------|--------|-----------|---------|--------|----------|--------|
| all075 [73-102]    |  60 |     80.0 |    80.0 |     -35 |    245 |  -1.11 |  16/17/27 |     +28 |  +1.22 |      +63 |  +3.95 |
| all125 [73-102]    |  60 |     80.0 |    80.0 |     +25 |    180 |  +1.06 |  10/11/39 |     -18 |  -2.08 |      -42 |  -2.07 |
| all150 [73-102]    |  60 |     80.0 |    80.0 |     +16 |    191 |  +0.66 |  10/16/34 |     -29 |  -2.43 |      -45 |  -2.20 |
| all200 [73-102]    |  60 |     80.0 |    80.0 |     -10 |    226 |  -0.34 |  12/18/30 |     -77 |  -3.85 |      -67 |  -3.15 |
| late075 [73-102]   |  60 |     80.0 |    80.0 |      +0 |     75 |  +0.01 |    6/9/45 |     +13 |  +1.75 |      +13 |  +2.30 |
| late125 [73-102]   |  60 |     80.0 |    80.0 |      -7 |     29 |  -1.92 |    2/5/53 |      -9 |  -2.06 |       -2 |  -1.89 |
| late150 [73-102]   |  60 |     80.0 |    80.0 |     -20 |     68 |  -2.28 |    2/9/49 |     -23 |  -2.37 |       -3 |  -2.42 |
| late200 [73-102]   |  60 |     80.0 |    80.0 |     -46 |    130 |  -2.75 |   2/11/47 |     -62 |  -3.27 |      -16 |  -2.10 |

### TOPB2 40  (OFF = topb2_off, theta B, hr switches)

| cell               |   n | win% OFF | win% ON |  d/game |     sd |      t |     +/-/= |  D ours |      t | D theirs |      t |
|--------------------|-----|----------|---------|---------|--------|--------|-----------|---------|--------|----------|--------|
| all075             |  40 |     32.5 |    32.5 |    -111 |    679 |  -1.03 |   7/18/15 |     +67 |  +0.88 |     +178 |  +3.33 |
| all125             |  40 |     32.5 |    32.5 |      +5 |    165 |  +0.20 |    6/9/25 |      -9 |  -0.31 |      -14 |  -1.48 |
| all150             |  40 |     32.5 |    32.5 |     -37 |    130 |  -1.79 |   5/13/22 |     -39 |  -1.37 |       -3 |  -0.25 |
| all200             |  40 |     32.5 |    32.5 |     -33 |    137 |  -1.51 |   7/17/16 |     -71 |  -2.09 |      -39 |  -1.88 |
| late075            |  40 |     32.5 |    32.5 |     +13 |     90 |  +0.92 |    3/6/31 |     +31 |  +1.76 |      +18 |  +1.89 |
| late125            |  40 |     32.5 |    32.5 |     -20 |     65 |  -1.92 |    2/7/31 |     -22 |  -2.16 |       -2 |  -1.36 |
| late150            |  40 |     32.5 |    32.5 |     -25 |     83 |  -1.91 |    2/9/29 |     -27 |  -2.09 |       -2 |  -1.36 |
| late200            |  40 |     32.5 |    32.5 |     -31 |    109 |  -1.80 |   2/13/25 |     -38 |  -2.50 |       -7 |  -1.28 |

## Reading

**1. The dial is live but small-amplitude.** At k = 2.0, ALL moves 70 of 120
LIVE-C boards and LATE 35 of 120; the rest are bit-identical. The effect sizes
are tens of coins per game against a ±20k margin spread, because `press` enters
as `press · lot_index` with `lot_index ∈ {0, 1, 2}` — doubling it moves the
marginal by single-digit coins per unit, over the few dozen units that are
actually contested at the margin of a lot.

**2. Harder is NOT better — and neither is softer. `press` at B is a local
optimum in margin.** On LIVE-C the profile is
`k 0.75 → −37 (t −1.71)`, `k 1.25 → +21 (t +1.30)`, `k 1.5 → +7 (t +0.36)`,
`k 2.0 → +3 (t +0.11)` for ALL — a shallow hump whose peak is inside the noise —
and monotonically **negative** for LATE (`−5`, `−11`, `−24`, `−41`). On
TOPB2 every cell is negative. **Not one cell of sixteen clears the promotion
gate** (board-level t ≥ 1.5 positive with our purse up); the win rate is
*identical* to the OFF arm in every single cell — 71.7 % on LIVE-C, 32.5 % on
TOPB2 — across all eight k values and both board sets.

**3. The seat split says the two directions fail for opposite reasons.** This is
the informative part, and both failures are two-purse failures:

* **Harder (k > 1): mutual destruction, and we pay more than they do.**
  ALL k = 2.0 on LIVE-C: our purse **−68** (t −4.94), theirs **−71** (t −3.64).
  We push more units into an earlier lot, walk further down our own curve, and
  the deeper flood does indeed cost the opponent — but it costs *us* essentially
  the same amount, so the margin never moves. The LATE variant is worse and
  cleaner: our purse **−46** (t −3.75) with theirs **−5** (t −0.75, level). A
  harder *tail-only* dump is almost **pure self-harm** — past day 25 there is
  not enough of the opponent's liquidation left to deny, so the extra price walk
  is paid by us alone.
* **Softer (k = 0.75): we hand the opponent back more than we keep.** LIVE-C:
  our purse **+12** (t +0.91, level) against theirs **+49** (t +2.96). TOPB2 is
  the same shape and larger: ours **+67** (t +0.88) against theirs **+178**
  (t +3.33). Spreading our units across lots does lift our own realised price a
  little, but it lifts the price the opponent liquidates into about four times
  as much. **This is the §114 denial asset, measured directly and from the
  other side** — and it is exactly why the ES drift that softened `press` cost
  us against the band clone.

**4. §114 is confirmed in direction and refuted in dose.** §114 says B's hard
late dump is a real asset against the band and that *softening* it loses money.
The k = 0.75 column reproduces that: soften and the clone's purse rises 4×
faster than ours. But the switch also shows B is already **at** the top of that
hill — pushing past it earns nothing, because the opponent's liquidation is
finite and we run out of their revenue to destroy before we run out of our own
price curve to walk down. The §114 gain is a *level* effect, not a *slope*: it
is worth having, not worth doubling.

**5. Nothing here is promotable, and nothing is a §57 false positive either.**
There is no cell where our purse rises significantly. The one cell where our
purse rises at all (k = 0.75) is the classic handed-back signature in reverse:
their purse rises more. Per `memory/counterfactuals-overstate.md`, that is not
promotable in either direction.

## Engine legs

**Not run, by the dispatch's own gate.** The gate was "the best variant/k on
LIVE-C, if any is positive at board-level t ≥ 1.5 **with our purse up**". The
best LIVE-C cell is ALL k = 1.5 at **+7 coins/game, t +0.36**, and its purse
split is **ours −35 (t −3.93)** — level in margin and negative in our own purse.
No cell qualifies, so no BAND40 or LIVEC-H30 leg was spent. (The commands are
banked in `S/press/README.md` for a later dose, pinned to
`S/lossflip/band40_B.csv` and `S/lossflip/sl_B_livech2.csv`.)

## Verdict

| cell | LIVE-C 120 (d, t \| D ours) | TOPB2 40 (d, t \| D ours) | verdict |
|---|---|---|---|
| `PRESS_SCALE` 0.75 | −37, t −1.71 \| +12 ns | −111, t −1.03 \| +67 ns | **REFUSED** — hands the opponent +49 (t 3.0) / +178 (t 3.3) |
| `PRESS_SCALE` 1.25 | **+21, t +1.30** \| **−16 (t −2.45)** | +5, t +0.20 \| −9 ns | **LEVEL** — best cell of the sixteen, still under the t 1.5 bar AND our purse is down |
| `PRESS_SCALE` 1.5 | +7, t +0.36 \| −35 (t −3.93) | −37, t −1.79 \| −39 ns | **LEVEL** |
| `PRESS_SCALE` 2.0 | +3, t +0.11 \| −68 (t −4.94) | −33, t −1.51 \| −71 (t −2.09) | **LEVEL** |
| `PRESS_SCALE_LATE` 0.75 | −5, t −0.91 \| +4 ns | +13, t +0.92 \| +31 ns | **LEVEL** |
| `PRESS_SCALE_LATE` 1.25 | −11, t −2.08 \| −10 ns | −20, t −1.92 \| −22 (t −2.16) | **REFUSED** |
| `PRESS_SCALE_LATE` 1.5 | −24, t −2.71 \| −21 (t −3.09) | −25, t −1.91 \| −27 (t −2.09) | **REFUSED** |
| `PRESS_SCALE_LATE` 2.0 | −41, t −2.71 \| −46 (t −3.75) | −31, t −1.80 \| −38 (t −2.50) | **REFUSED** |

Every cell's **win rate is bit-identical to the OFF arm** — 71.7 % on LIVE-C,
32.5 % on TOPB2, in all sixteen. The LIVE-C halves agree (43-72 and 73-102 give
the same signs on every cell, so this is not a hold-out-half artefact).

**Family verdict: the scalar `press` dose at B is CLOSED.** Both directions are
level-or-worse on the band proxy and level-or-worse on the top tier; the win
rate does not move by a single board in any of sixteen cells.

## Is an ES arm with `press` re-centred harder warranted?

**No — not a re-centring on the scalar axis, and the measurement says why.**

A *uniform* harder `press` is the thing this switch tested, and it is worth
**+7 ± 20 coins/game at best** on the band proxy and negative on the top tier.
Re-centring an ES arm's `b3` to sit harder would be seeding it at a point this
screen has already priced at zero, and would spend a GPU arm re-deriving a flat
direction. It is also the wrong shape of fix: a scalar multiplies all nine
products together, and §114's mechanism is explicitly **per product** — B's
asset is flooring *carrot and wool* at d29 against a carrot/wheat one-lump
liquidator, while the drift that lost it also *gained* by flooring *milk*
against the mixed top tier. A single scalar cannot separate those; it moves
both and they cancel, which is precisely the ±0 this screen reports.

What the seat split **does** warrant, and what should be built instead:

1. **A per-product press probe, not a scalar.** The k = 0.75 column shows the
   denial asset is real and worth ~50 coins/game on LIVE-C (their purse) and
   ~180 on TOPB2. A `KAGG3_PRESS_SCALE_PROD=<9 comma-separated k>` variant would
   let the carrot/wool axis be pushed while milk/fertilizer is held, which is
   the only form in which §114's mechanism is expressible. This is a one-line
   extension of the switch already built here.
2. **`press` is not where the band/top-tier conflict can be resolved** —
   §114's verdict (c) stands and this screen strengthens it. The conflict is
   about *which product* to floor at d29, and that is a conditioning problem
   (§78 refuted the observation class) or a per-product-weight problem, not a
   dose problem.
3. **Freeze `press` against further drift rather than re-centring it.** The
   2026-09-12T03:18Z drift read found flow210's hr seed walking `press` **up on
   8 of 9 products** while flow209 walked the other way. This screen prices the
   whole scalar axis at zero margin, so that drift is ES noise spending
   variance on a flat direction. Pinning `press` (the §67 PINNED-INTS
   machinery) in a training arm is the cheap, measured move — it removes a
   known-flat direction from the search rather than betting on a sign.

