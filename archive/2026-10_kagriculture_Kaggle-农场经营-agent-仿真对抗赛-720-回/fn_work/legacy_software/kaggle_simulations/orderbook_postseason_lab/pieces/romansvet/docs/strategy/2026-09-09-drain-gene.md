# The drain-mix gene: let the search state the tilt, per product

*2026-09-09, worktree `.claude/worktrees/drain-gene` (detached at `8b535ec`).*

## 1. What this replaces

Two hand-set constants, both of them additions of `residual_drain`'s `share`
column to a mix softmax:

| knob | where | what it adds | verdict |
|---|---|---|---|
| `brain.PLANT_MIX_DRAIN_ON` | the five crop logits | `PLANT_MIX_DRAIN_GAIN * share` | **lost**: 192 real-engine games at gain 1.0, paired diff -11,906, t = -15.4; lost again dose-responsively on the pinned judge (§13 of `2026-09-09-plateau-review-verdicts.md`) |
| `brain.ANIMAL_MIX_DRAIN_ON` (care-cov tree) | the three animal logits | `ANIMAL_MIX_DRAIN_GAIN * share` | the **first fixed knob to pass the pinned judge**; +2.0 to +2.2k a game over the six byte-exact live losses, but carried by 2 boards of 6 with 2 negative, and a full tilt overshoots by -5.5k on 107056463 where the season milk sink (426) already exceeds the *joint* supply (375) |

`share` is the right scalar -- `2026-09-09-herd-composition.md` measured
`corr(season wool sink, coins per sheep-day) = +0.98` and
`corr(season milk sink, coins per cow-day) = +0.89`, and the only sink-shaped
raw column the mix softmax reads (`daily_town_demand`) is structurally biased
towards wool by `_town_consume`'s `multiplier = 2`. What is wrong is the
**one constant for eight products**. Nothing in `brain.py` knows whether this
board's melon `share` -- saturated at the clip floor, `-4.0` -- deserves the
same coefficient as its wool `share`, which the recorded boards put anywhere
between `+0.08` and `+0.87`. No human number can be right on both.

So the constant becomes a per-product head output and ES states it.

## 2. The block

```
("gd",  (N_HEAD_HID, N_MIX_DRAIN)),   # 32 x 8 = 256
("gbd", (N_MIX_DRAIN,)),              #           8
```

* `N_MIX_DRAIN = spec.N_CROPS + spec.N_ANIMALS = 8` -- exactly the products
  that *have* a mix logit. `spec.PRODUCTS` orders the market
  `WHEAT CARROT TOMATO STRAWBERRY MELON EGG MILK WOOL FERTILIZER`, so column
  `p` of the block is `residual_drain` row `p` with no index table in between,
  and FERTILIZER -- the one product no mix softmax covers -- is exactly the row
  left out.
* offsets: `gd` at **6,789**, `gbd` at **7,045**; `N_PARAMS` **6,789 -> 7,053**.
  Every earlier offset is unmoved (`fh@4980 fs@5492 gp@5508 g11@6372 gb11@6404
  fv@6405`), pinned by `test_the_block_is_a_clean_append`.
* new output `Outputs.mixd`, `gh @ gd + gbd`, off the same global hidden layer
  the animal share, the plant sharpness, the crew ramp and the land bias come
  off -- so the tilt can differ by *board* as well as by product.

## 3. The decode

```python
mix_drain = xp.clip(MIX_DRAIN_GAIN * (out.mixd * drain[:PO.N_MIX_DRAIN, 1]),
                    -MIX_DRAIN_CLIP, MIX_DRAIN_CLIP)
...
wa = _softmax(..., grow[EGG,MILK,WOOL] * sharpness + a_mix + mix_drain[N_CROPS:])
w  = _softmax(..., grow[:N_CROPS]      * sharpness      + mix_drain[:N_CROPS])
```

**Linear in the parameter, deliberately.** The memory rule for genes
(`gene-slope-check`) exists because the forward-admit gene shipped as
`round(6 * sigmoid(z - 4))` and **not one of 512 members at sigma 0.02 decoded
a single day**: a saturating decode is flat at the origin and a zero-init gene
lives at the origin. `MIX_DRAIN_GAIN * z` has the same slope everywhere and is
still exactly 0 at 0.

`MIX_DRAIN_CLIP` bounds the decoded **term**, not the gene -- `share` is already
clipped to `+-DRAIN_CLIP = 4`, so the clip only stops a saturated gene from
turning the softmax into an argmax.

**No switch.** The term is added unconditionally, because at zero it is exactly
`0.0` and `x + 0.0 == x` -- the inertness `fh`/`fs`, `gp` and `fv` are all
appended under. What a `+ 0.0` needs is a pin of the *pre-gene program*, and
that is section 5.

## 4. The measured slope

Method: `N` isotropic members at the arm's own sigma 0.02 off the arm's own
init (`flow135_g350_gpfwdfv_gb028`, trained everywhere except this block),
decided twice on each recorded hour-0 board -- once with `MIX_DRAIN_GAIN` and
once with it at 0.0 -- and scored as **"this member's gene moved its own herd
or plant mix"**. That is the ES-visibility question: not the population's
spread, but whether the gene each member drew changes what that member does.

Boards: `tests/data/trajectory_obs.npz` (recorded hour-0 observations off real
games), `rng(3).choice(2400, 12)`.

At sigma 0.02 the gene's pre-activation reads `sd 0.048`, `|z| mean 0.038`;
mean `share` over the 12 boards is
`[1.86 1.37 1.50 1.51 -4.00 1.16 0.11 0.08]` (melon saturated at the clip
floor, wool and milk near zero on this sample).

Sweep (256 members x 12 boards, fraction of (member, board) pairs whose herd
or plant mix the member's own gene moved):

| `MIX_DRAIN_GAIN` | any mix | herd only | plant only | per-board median |
|---|---|---|---|---|
| 2.0 | 10.4 % | 2.9 % | 7.8 % | 10.2 % |
| 2.5 | 12.4 % | 3.4 % | 9.5 % | 11.7 % |
| 3.0 | 14.9 % | 3.9 % | 11.6 % | 13.9 % |
| **5.0** | **24.4 %** | **6.3 %** | **19.8 %** | **23.8 %** |
| 6.0 | 28.7 % | 7.8 % | 23.1 % | 26.8 % |
| 8.0 | 35.4 % | 10.0 % | 28.8 % | 35.9 % |

(A first pass on a different 8-board draw read roughly twice these fractions at
the same gain -- the change-fraction is strongly board-dependent, which is why
the band is checked on a *median over boards* as well as on the pooled mean.)

**`MIX_DRAIN_GAIN = 5.0`, `MIX_DRAIN_CLIP = 3.0`.** 24.4 % pooled, 23.8 %
per-board median -- the middle of the 15-35 % band. The number looks large only
because the two things it multiplies are small: the block's pre-activation is
`sd 0.048` at this sigma and `share` averages about 1.3 in magnitude, so one
sigma of gene moves the *decoded logit* by roughly 0.3 -- well inside
`MIX_DRAIN_CLIP` and a fraction of what the plant softmax's own sharpness
(`1 + 4*sigmoid(head[7])`, in [1, 5] over grow scores of order 1) spans.

One of the twelve boards never moves at any gain (no free tile: the day plants
nothing and buys nothing whatever the mix says), so the test asserts
"at least three boards in four are live" rather than "every board is live".

The herd half is the weaker one (6.3 % at gain 5.0) for a structural reason
worth recording: the fixture's boards buy **0.99 animals a day on average** and
68 % buy any at all, against 7.45 plantings -- a three-way softmax rounded to
one unit has far fewer chances to flip than a five-way one rounded to seven.
That is a property of the decision, not of the gene, and raising the gain to
fix it would push the plant half past the band.

## 5. Identity: the pre-gene program, pinned

The `+ 0.0` claim is only worth what pins it. Two digests, both taken on
`8b535ec` **before** the block existed, both with the live init theta:

* `PIN` -- `brain.decide` plus the whole six-array `plan.build_day` on the
  twelve `test_route_early.PIN_SEEDS` boards (seeded day/purse/herd/ripe/weeds/
  quadrant boards, with a seeded *opponent* half so `residual_drain` --
  opponent-inclusive -- is not reading half its input);
* `TRAJ_PIN` -- one digest over the `Macro` of 200 recorded trajectory states.

Both come back byte for byte with the block in. That is the assertion a
"padded theta equals short theta" test cannot make -- both sides of *that* go
through the new graph, so it can only prove the block is zero, never that the
graph is unchanged. These digests are numpy; the JAX half of the same question
is the two backend-agreement tests, which compare `decide` under `jax.jit`
against numpy with the block trained **off** zero.

## 6. Tests -- `tests/test_drain_mix_gene.py`

| group | test |
|---|---|
| layout | `test_the_block_is_a_clean_append`, `test_every_new_coordinate_is_live_and_nameable`, `test_pad_zero_extends_and_keeps_the_prefix` |
| identity | `test_padded_theta_reproduces_the_old_forward_exactly` (x8 seeds), `test_the_pin_seed_plans_are_the_pre_gene_planners`, `test_two_hundred_recorded_states_decode_the_pre_gene_macro`, `test_the_padded_champion_is_the_short_one_on_every_pin_seed`, `test_a_zero_gain_is_a_zero_gene` |
| decode | `test_the_decoded_term_is_linear_in_the_gene_and_clipped`, `test_a_positive_gene_tilts_the_mix_towards_unclaimed_appetite`, `test_the_gene_is_per_product_and_not_one_constant` |
| slope | `test_the_arms_init_decodes_a_zero_tilt_on_every_real_board`, `test_one_es_step_moves_the_mix_for_a_minority_of_the_population` (the 15-35 % band, as an assertion) |
| backends | `test_numpy_matches_jax_with_a_trained_block`, `test_the_decision_agrees_across_backends_with_a_trained_block` |

`tests/test_forward_value.py` and `tests/test_global_product.py` each construct
a longhand `PO.Outputs`; both gained a `mixd=np.zeros(N_MIX_DRAIN)` field, which
is what those helpers' thetas always emitted.

## 7. The padded init

```
python scripts/upgrade_theta.py \
  artifacts/kagg2_games/thetas/flow135_g350_gpfwdfv_gb028.npy \
  artifacts/kagg2_games/thetas/flow135_g350_gpfwdfv_gb028_gd.npy
# 6789 -> 7053 params, blocks appended: gd, gbd, |theta| 15.4539 -> 15.4539
```

`scripts/upgrade_theta.py` already *is* the padding helper the task asked for
(it is `policy.pad` and a file); no new script was needed. md5 of the padded
theta: `d1b23026d7788f4f3a5d17caba5e3741`.

## 8. Launch -- flow168

Full script: `docs/strategy/2026-09-09-launch_flow168.sh` (flow166's recipe,
seven lines changed). Two of the seven are the gene; five are the coordinator's
recipe correction of 2026-09-09: flow166 reads **nearly level on the 86 gate
tapes it trains on (-0.4k/game) while the 10 held-out leg-family tapes still
fall (-1.9k/game)**, i.e. training moves the boards it trains on and the gate
was reading a set that training had already touched.

```
# flow168 (2026-09-09, DRAIN-MIX GENE arm): flow166's gate-aligned recipe with
# a new theta layout and a held-out gate. NEW BLOCK gd/gbd (6,789 -> 7,053;
# 264 coordinates): one per-product gain on residual_drain's `share`, decoded
# LINEARLY as MIX_DRAIN_GAIN * (gh @ gd + gbd) * share, clipped to
# +-MIX_DRAIN_CLIP, added to the herd softmax (EGG/MILK/WOOL) and the plant
# softmax (five crops) exactly where the fixed knobs add their constant.
# Zero-init it is exactly 0.0, so this init is byte-for-byte the flow166 init.
# MEASURED SLOPE at sigma 0.02: 24.4 % of (member, board) pairs move at
# MIX_DRAIN_GAIN = 5.0 (256 members x 12 recorded boards, median 23.8 %).
# GATE = 12 FRESH KAGGLE-LOSS TAPES (NEVER TRAINED); FAMILY IN TRAINING.

cd ~/stage_draingene                     # NOT stage_leg20: the block is code
CUDA_VISIBLE_DEVICES=__GPU__ python scripts/train.py \
  --run flow168 --seed 268 \
  --init-theta artifacts/kagg2_games/thetas/flow135_g350_gpfwdfv_gb028_gd.npy \
  --best-margin 0.04 \
  ... --rung-weight tape_act_<10 family ids>=2 ...        # family INTO training
  --real-gate-leg-family 107056463,107067869,107068399,107070717,107072760,\
107079367,107081922,107088554,107090008,107089992,107092814,107095149 \
  --real-gate-opponent ...,artifacts/panel_opp_town/opponent_tape_<each of the 12>/main.py \
  --real-gate-pinned-seats 2 --real-gate-recentre 3 --real-gate-every 100 ...
```

The seven changes, in the script's own words:

1. `--init-theta ..._gb028_gd.npy` (the padded champion, md5
   `d1b23026d7788f4f3a5d17caba5e3741`);
2. `--run flow168`; 3. `--seed 268`;
4. the **10 leg-family tapes move from `--rung-weight tape_act_<id>=0` to `=2`**
   -- into training; they were already listed in `--tape-actions`;
5. `--real-gate-leg-family` becomes the **12 fresh Kaggle-loss tapes**
   `107056463 107067869 107068399 107070717 107072760 107079367 107081922
   107088554 107090008 107089992 107092814 107095149`. **None of the twelve
   appears in `--tape-actions` or in any `--rung-weight`** (asserted while the
   script was written), so the held-out set is genuinely untrained;
6. their 12 opponent packages join `--real-gate-opponent`: 48 -> **60
   opponents, 120 gate games**, of which **24 are the held-out twelve** at
   `--real-gate-pinned-seats 2`. All 12 verified present on the remote
   2026-09-09 (`ls ~/stage_leg20/artifacts/panel_opp_town/`, 175 packages,
   **none missing**);
7. `--best-margin 0.005 -> 0.04`. Shaping stays off (`--abs-weight 0.0
   --d10-cash-weight 0 --tile-fill-weight 0`), gate every 100, re-centre 3.

**Staging.** The remote is not a git repo *and this arm is a code change*: copy
`~/stage_leg20` to `~/stage_draingene` (for `artifacts/tape_actions_town`,
`panel_opp_town`, `town_schedules.json`, `kagg2_games/thetas`), rsync this
worktree's `src/ scripts/ tests/` over it, then build the init in place with
`scripts/upgrade_theta.py` -- it must print `6789 -> 7053` and md5
`d1b23026d7788f4f3a5d17caba5e3741`. A stale tree refuses the 7,053 theta
outright, which is the failure mode we want rather than a silent truncation.

For the cheap variant, `--train-only gd,gbd` searches 264 coordinates against
7,053 with the champion held byte for byte.

## 9. What is NOT verified here

* **No engine or gate result.** This is a layout + decode change with a
  measured slope; whether the tilt pays is flow168's question, and the
  machine was loaded (~29 on 12 cores) so no paired engine legs were run.
* The slope is measured on `trajectory_obs.npz` boards, not on the three
  pinned live-loss boards' recorded observations -- the pinned replays live in
  a session scratchpad, not in the tree, so a test cannot depend on them.
* The gene is trained *with* the rest of the theta in the flow168 recipe
  (`--train-only all`), so a flat gate result will not separate "the gene is
  useless" from "the arm drifted".
* The flow168 script has **not been run**, here or on the remote. What was
  checked is only that its 12 held-out opponent packages exist on the remote
  and that none of the 12 appears in `--tape-actions` or in any
  `--rung-weight`, that all 60 gate opponents are unique, that the 10 family
  ids carry `=2` and are in `--tape-actions`, and that all **41** long flags
  the script uses exist in `scripts/train.py`'s parser. What has *not*
  happened is `argparse` actually parsing the line or a single generation
  running: the flag set is flow166's, edited textually.

## 10. Run log

* **14:15Z** -- pre-gene digests captured on `8b535ec` (12 `PIN_SEEDS` boards +
  200 recorded states, `flow135_g350_gpfwdfv_gb028`). This had to happen
  *before* the edit or the identity claim has no golden.
* **14:25Z** -- `gd`/`gbd` appended (`policy.py`), term added to both mix
  softmaxes (`brain.py`), init padded to 7,053 with
  `scripts/upgrade_theta.py`; both digests re-read identical.
* **14:35Z** -- gain swept at 256 members x 12 recorded boards: 2.0 -> 10.4 %,
  3.0 -> 14.9 %, 5.0 -> 24.4 %, 8.0 -> 35.4 %. `MIX_DRAIN_GAIN = 5.0`.
* **14:45Z** -- `tests/test_drain_mix_gene.py` green, 22 tests. Coordinator's
  recipe correction folded into the flow168 script (family into training, gate
  = the 12 fresh Kaggle-loss tapes, 60 opponents, `--best-margin 0.04`); all 12
  opponent packages verified present on the remote; all 41 flags checked
  against `scripts/train.py`'s parser.
* **14:50Z** -- `tests/test_forward_value.py:137` found pinning `== PO.N_PARAMS`
  (which its own comment warns against) and relaxed to the block's own end.
* **15:05Z** -- test status at hand-off. GREEN: `tests/test_drain_mix_gene.py`
  (22 tests, whole file), `tests/test_global_product.py` +
  `tests/test_forward_value.py` (33 tests, `-k "not champion"`). NOT RUN: an
  11-file sweep (`test_forward_gene`, `test_plant_mix_drain`,
  `test_mixed_herd`, `test_crew_and_herd_mix`, `test_es_masking`,
  `test_route_early`, `test_warm_start`, `test_resume_roundtrip`,
  `test_genome_retype`, and the two `champion` tests that want
  `flow135_g350_gp*.npy`) hit a 25-minute wall clock on a box already at load
  ~29 and was killed before reporting -- **run it before the arm is trusted**;
  it is the sweep that would catch a layout consumer this change missed.
* Also verified by hand: the padded init decides identically under `jax.jit`
  and under numpy on a recorded board (all `Macro` fields equal), its first
  6,789 coordinates are the champion's byte for byte, and its tail is zero.
