# SWITCH-NAMED — the day-0 decision behind B's 0.003 switch, and the recentre test

Agent, 2026-09-11, 60-minute box, CPU only. Continues `docs/strategy/2026-09-11-day0-switch.md`
(consensus §63). New files: `S/switch0/{tie.py,grad.py,day0.py}`, `S/recentre/`. No change under
`src/` (`git diff --stat src/` empty), no judge lock, no engine legs, no ssh.

## 1. The decision: a SEVENTH ANIMAL that is never bought, paid for with the ELEVENTH WHEAT TILE

`S/topledger/ledger.py` on the 6 TOPB2 boards, B against the crossing theta
`s0p01_p512_minus_a0p03` (`S/switch0/day0.py switch0_B switch0_X`). Our seat, day 0, every column
that differs — and on all six boards it is the same four, with the same sign and the same size:

| column | B | X (crossed) | Δ |
|---|---|---|---|
| `money` (end of day 0) | 146,146,160,160,146,146 | 156,156,170,170,156,156 | **+10** (one wheat seed) |
| `planted` | 19 on all six | 18 on all six | **−1** |
| `idle` | 0 on all six | 1 on all six | **+1** |
| `tile_WHEAT` | 11 on all six | 10 on all six | **−1** |

*Board-independent*, as §1 of the switch doc predicted: identical on 6 boards and 2 seats, and the
**opponent seat's day-0 row is byte-identical** (0 columns differ), so this is not a pump, a denial
or anything the other seat did — it is our own opening, decided before the first turn.

It persists: `planted` is still 19 vs 18 on days 1, 2 and 3, and the idle tile is still idle.

**And the animal is never acquired.** `animal_GOOSE/COW/SHEEP` are identical on every day of both
runs — `[1,4,1]` at the end of day 0 and `[1,5,1]` by day 5 for *both* thetas. The crossing theta
asks for a 7th animal, the purse never buys it, and the only thing the want does is take a tile out
of the seed cap. It pays one wheat tile for nothing, on every board, for the whole season
(final money: B ahead on 5 of the 6, mean −1,124).

### 1.1 Where the tile is taken — the exact lines

The decision is one integer, and the chain from it to the refused seed is three lines:

1. **`src/kagg3/core/brain.py:624`** — the decision itself:
   `animal_count = _qfloor(xp, animal_share * n_dev.astype(xp.float32))`
   with `animal_share = sig(head[6])` (`brain.py:623`) and `n_dev = _qfloor(dev_frac * n_free)`
   (`brain.py:622`). `animal_count` then becomes `macro.animal_want` through
   `_largest_remainder` (`brain.py:646`), and `plant_total = n_dev - sum(animal_want)`
   (`brain.py:647`) is one *smaller* for it.
2. **`src/kagg3/core/plan.py:4373`** (`_seed_room`, line 4351) — the planner reserves the fresh
   tile for a want it has not priced yet:
   `seed_cap = xp.maximum(n_free - xp.sum(ft_ub, dtype=i32), 0)`, where `ft_ub` is
   `_place_split(xp, xp.maximum(a_want, a_have), n_free, sfree)`'s fresh-tile claim.
3. **`src/kagg3/core/plan.py:4667`** (`_wants`, line 4628) — the seed want is clipped to what is
   left: `w_seed = xp.clip(want_raw, 0, xp.maximum(seed_cap - before, 0))`. With `seed_cap` one
   smaller the 11th wheat seed is **not a candidate at all**, so `budget.grant` never gets to
   price it, the BUY row is 10 coins cheaper, and one tile stays empty.

(Line numbers are the repo tree on `fitness-shaping`. The sim the judge and these drivers run is
`.claude/worktrees/arms-next/src`, where the same three lines are `brain.py:924`, `plan.py:4373`
and `plan.py:4667` — the bodies are identical.)

The often-suspected day-0 knobs are **not** it: the hire enumeration's argmax (`plan.py:5991`,
`h_star = xp.argmax(xp.stack(scores))`) picks the same crew on both sides — `hands` and `nquad`
never appear in the day-0 diff — and the `OPEN_PUMP` wheat quantity is unchanged (the opponent's
day-0 row is identical to the coin).

## 2. The near-tie, measured — why the radius is 0.003

`S/switch0/tie.py` + `S/switch0/grad.py`. No instrumentation in `src/`: `brain.decide(xp, theta,
obs)` takes its array module as an argument, so the driver passes a shim that delegates every
attribute to `jax.numpy` and **records the argument of each `floor` call** — i.e. every
`_qfloor`-quantised decode, in order, eagerly, with concrete values (and, in `raw` mode, as
tracers, so `jax.grad` differentiates straight through to theta).

The competing candidates at this decision are the two integers `_qfloor` can return, 6 and 7, and
their "scores" are the one continuous quantity `animal_share * n_dev` and the boundary:

| quantity | value |
|---|---|
| `animal_share * n_dev` at B (day 0, the `floor` argument at `brain.py:624`) | **6.991294** |
| the boundary `floor(x + max(QUANT_EPS, QUANT_REL·x)) = 7` | **6.999900** |
| **score gap** to the losing candidate | **0.008606** |
| `‖∇_θ (animal_share · n_dev)‖` at B, over all 6,789 coordinates | **31.859** |
| **switch radius** = gap / ‖∇‖ (perpendicular distance to the hyperplane) | **0.000270** |
| directional derivative along the E3b crossing ray `s0p01_p512_minus` | 3.572 (cos 0.112) |
| **radius along that ray** = gap / (∇·n̂_ray) | **0.002409** |
| trainer generation step `R = lr·√n_live` | 0.2323 = **860 ×** the perpendicular radius |

The ray number is the prediction the α ladder already measured blind: §3 of the switch doc
brackets the crossing between ‖θ−B‖ = 0.00232 (no flip) and 0.00348 (all 40 boards flip), and
gap/(∇·n̂) = **0.002409** falls inside that bracket. The 0.003 in consensus §63 is therefore not a
fitted number: it is `0.008606 / 3.572`, a score gap divided by a directional derivative.

The perpendicular radius is **0.00027** — B is 860 times closer to this switch than one generation
step, and a *single coordinate* moving by one `lr` (0.003) is 11 times the radius.

Dividing by the *whole* gradient norm is also what explains §2 of the switch doc (no gene carries
it): `∇` is dense, 6,789 coordinates, and the crossing ray's cosine with it is 0.112 — a generic
direction. Any displacement with ‖Δθ‖ ≳ 0.00027/cos crosses, which is why 5 of 8 signed random
controls and 3 of 34 single-block moves (`w1`, `g1`, `g2` — the three blocks on the `head[6]`
path, each flipping all 6 boards by exactly −1,269 coins; `S/simscreen/switch0_only_topb2.csv`)
cross it on their own.

## 3. Test 1 — recentring B along −∇ (the §63 fix)

n̂ = −∇/‖∇‖ (the normal of the near-tie, pointing back into B's own cell — the "better" of the two
definitions the fix proposes). `B_c = B + c·n̂`, `S/recentre/thetas/Bc_*.npy`.

**The decode says the premise fails before any board is played.** `S/switch0/tie.py` along n̂:

| c | `animal_share·n_dev` | `n_dev` pre-floor | `macro.plant_target` | `macro.animal_want` | day-0 plan |
|---|---|---|---|---|---|
| 0 (B) | 6.9913 | 28.6858 | [11,11,0,0,0] | [1,4,1] | — |
| 0.0005 … 0.012 | 6.975 … 6.618 | 28.694 … 28.884 | [11,11,0,0,0] | [1,4,1] | **identical to B** |
| **0.020** | 6.6069 | **29.0113** | [12,11,0,0,0] | [1,4,1] | **changed** (`n_dev` 28 → 29) |
| 0.050 | 5.7511 | 29.4561 | [13,11,0,0,0] | [1,3,1] | changed (also `animal_count` 6 → 5) |
| 0.100 | 4.7181 | 30.0799 | [14,11,0,1,0] | [1,3,0] | changed |

Moving away from the animal-count tie walks straight into the **development** tie at
`brain.py:622` (`n_dev = _qfloor(dev_frac · n_free)`, 28.686 at B, boundary 29): the cell around B
along n̂ is only ~0.012-0.020 wide, and the three prescribed c values are all outside it. c = 0.05
then crosses the animal tie's *other* wall (`animal_count` 6 → 5). Test 1's "Δ 0 on 100 % of
boards" is therefore impossible at c ≥ 0.02 by construction, and the screens below measure how
much damage that does rather than whether n̂ is clean.

`S/simscreen/screen.py`, `shopdiff 0.0 %` on every row (the shop draw is pinned, so every
coin below is play, not lottery). `B_c` against B on both frozen files:

| theta | ‖Δθ‖ | TOPB2 40 boards: moved | Δmargin (t) | LIVE-C 120 boards: moved | Δmargin (t) |
|---|---|---|---|---|---|
| `Bc_0p02` | 0.02 | **40/40 = 100 %** | −84 (−0.23) | **120/120 = 100 %** | −66 (−0.37) |
| `Bc_0p05` | 0.05 | 40/40 = 100 % | −3,065 (−3.99) | 120/120 = 100 % | −3,239 (−10.82) |
| `Bc_0p1` | 0.10 | 40/40 = 100 % | **−16,517 (−11.88)** | 120/120 = 100 % | **−18,254 (−28.52)** |

Win rate falls with it: TOPB2 32.5 % → 35.0 / 22.5 / **5.0 %**, LIVE-C 71.7 % → 76.7 / 60.8 /
**4.2 %**.

**Test 1 fails at every c, including the one whose day-0 plan is byte-identical to B's.**
`Bc_0p02` decodes the same `plant_target`, the same `animal_want` and the same day-0 board as B
(§3 table) and still moves **every board in both families** — so a *different* switch, on a later
day, flips inside 0.02 of B as well. n̂ is not a free direction: it is only free of the *one*
tie it was built from. At 0.05 and 0.1 the theta is simply destroyed.

## 4. Test 2 — is B_0.1 a smooth centre?

The same eight signed random 0.2323/10 = **0.0232** steps that were drawn at B (one per `rand` ray
of `S/onestep_b`, at the sign that crossed at B where a sign crossed: `rand0−`, `rand2−`, `rand3−`,
`rand5−`, `rand7+`, plus `rand1−`, `rand4−`, `rand6−`), re-applied at `B_0.1` and screened on the
40 TOPB2 boards against `B_0.1` itself as the reference. Baseline at B: **5 of 8 cross** (flip
100 % of boards). (Note: the E3b random controls are 0.0232 long — α 0.1 *of* the 0.2323
generation step — not 0.2323; the brief's figure is the full step.)

| theta at `B_0.1` | boards moved (of 40) | Δmargin vs `B_0.1` | t | crosses (100 %)? |
|---|---|---|---|---|
| `rand0−` | 20 = 50.0 % | +31 | +0.15 | no |
| `rand1−` | 22 = 55.0 % | +332 | +2.26 | no |
| `rand2−` | 24 = 60.0 % | +292 | +1.66 | no |
| `rand3−` | 18 = 45.0 % | +155 | +0.74 | no |
| `rand4−` | 24 = 60.0 % | +557 | +2.43 | no |
| `rand5−` | 23 = 57.5 % | +493 | +2.10 | no |
| `rand6−` | 18 = 45.0 % | +40 | +0.36 | no |
| `rand7+` | 20 = 50.0 % | +467 | +2.24 | no |

**0 of 8 cross at `B_0.1`, against 5 of 8 at B.** By the letter of the test, `B_0.1` is a smooth
centre: no random step of the trainer's own α 0.1 length flips the whole board set, each moves
45-60 % of boards, and the eight readings are a spread of ordinary ±1,000-coin board noise rather
than one shared cliff. Five of the eight even read positive at t ≥ 2.

And it is worthless, because §3 measured what `B_0.1` *is*: a 5 %-win theta, 16.5 k coins a board
below B on the top tier and 18.3 k below it on the hold-out. Every one of those eight steps
gaining a few hundred coins is the neighbourhood telling us the same thing — there is a lot of
room to improve, uphill, back towards where B was.

## 5. Verdict

**The decision is named, the radius is derived, and the recentre fix is REFUTED.**

1. **The switch is the day-0 herd/crop tile split**: `animal_share · n_dev` = **6.9913** at B
   against a `_qfloor` boundary at **6.9999** (`brain.py:624`). On B's side the day asks for 6
   animals and 11 wheat tiles; 0.0086 further and it asks for 7 animals — **buys none of them**
   (the herd row is identical on every day of both ledgers) — and pays for the want with the 11th
   wheat tile, which `plan.py:4373` reserves out of `seed_cap` and `plan.py:4667` then clips the
   seed want to. 10 coins unspent, one tile idle for the season, −1,774/board on TOPB2.
2. **The 0.003 is arithmetic, not a fit**: gap 0.008606 / ‖∇‖ 31.859 = **0.00027** perpendicular;
   along E3b's own crossing ray, 0.008606 / 3.572 = **0.00241**, inside the blind bracket
   [0.00232, 0.00348] the α ladder measured. One generation step is 860 × the radius.
3. **Recentring does not work, and the reason is general.** Pushing B off this hyperplane along
   its own normal walks into the next one (`n_dev` 28 → 29) within 0.012-0.020, and *every* c
   moved 100 % of boards in both families — even c = 0.02, whose day-0 plan is byte-identical to
   B's. B is not near one switch; it is in a small cell bounded by many, and there is no
   "widen the margin" direction. **Do not stage an ES arm from `B_0.1`** (or from any `B_c`): it
   is smooth exactly because it is far from every tie B's good play sits on, and it plays at 4-5 %
   win rate.
4. **What the measurement does hand us is a planner lever, not an ES one.** `_seed_room` reserves
   a fresh tile for `max(a_want, a_have)` — "the most builds this day can want" — *before* the
   purse has priced anything, so on day 0 a 7th animal the farm cannot afford still evicts a wheat
   tile that it can. A purse-aware reservation (reserve only for animals the day can actually buy)
   would make both sides of this tie plant 11 wheat and would **remove the switch**, which is
   worth more than either side of it: it is 2,080 coins of board-independent variance out of the
   objective at B. That is a `plan.py` change and a falsifiable one — paired screen on LIVE-C +
   TOPB2, and the two-purse displacement rule applies (`counterfactuals-overstate`): the tile has
   to be shown to earn more than the animal want it is taken from, not merely to exist.
   **Not implemented in this box** (`git diff --stat src/` empty).

## Files
`S/switch0/tie.py` (the `xp`-shim decode driver — no `src/` instrumentation), `S/switch0/grad.py`
(the gradient, the radius, and the `B_c` builder), `S/switch0/day0.py` (ledger diff),
`S/recentre/thetas/` (`B`, `Bc_0p02/0p05/0p1`, the 8 `r*_at_Bc0p1`), `S/recentre/build_test2.py`,
`S/recentre/tie_grad.npy`, screens `S/simscreen/rc_test1_topb2.csv`, `rc_test1_livec.csv`,
`rc_test2_topb2.csv`.
