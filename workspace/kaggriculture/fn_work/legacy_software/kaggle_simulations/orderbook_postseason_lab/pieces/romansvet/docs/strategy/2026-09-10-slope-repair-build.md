# Slope repair: the `plant_floor` gene and the `compact` soft decode (2026-09-10)

Built on branch `slope-repair` (worktree off `arms-next`). Both changes are inert by
default; nothing in the judged lineage moves until an arm turns them on.

## Layout

`g12` (32x5) + `gb12` (5) appended after `fv`: **N_PARAMS 6,789 -> 6,954**, `offset("g12")
== 6789`. Every earlier theta is still a prefix; `PO.pad` zero-extends into the new block
and `--init-theta` pads automatically. All 165 coordinates are live in `live_mask`, and
`--train-only g12,gb12` addresses them.

## Decodes

**plant_floor** (`brain.PLANT_FLOOR_ON`, default OFF). Per crop,
`floor = clip(round(FLOOR_GAIN*z), 0, FLOOR_ONE) / FLOOR_ONE` with `FLOOR_GAIN = 8`,
`FLOOR_ONE = 16` — a share of the day's plantable tiles in sixteenths. Masked by the mix's
own `can_mature * absorb`, scaled by `max(sum, 1)`, then mixed *before* the largest
remainder as `w = floor + (1 - sum(floor)) * w`. A convex combination, so the day still
hands out exactly `plant_total` tiles; at a zero gene it is `0.0 + 1.0*w`, i.e. `w` bit for
bit. The switch is the [LAW] graph guard, not the gene: OFF is the shipped expression
character for character.

**compact** (`plan.COMPACT_SOFT_ON`, default OFF, `COMPACT_SOFT_GAIN = 2.5`). ON the
decode is `clip(round(GAIN*z), 0, DIST_MAX)`, `FWD_DAYS_GAIN`'s straight line. The shipped
`floor(DIST_MAX*relu(tanh z))` cannot reach `DIST_MAX` at all (`tanh < 1`), so the last
band — `_dev_key == DIST_SHED`, the only setting that orders the spawn tile ahead of its
neighbours — is unreachable by construction. Above `DIST_MAX` there is nothing to reach:
`_dev_key` is a monotone scale of `DIST_SHED`, so wider ranges are the identical ordering
(and overrun `_rank_near`'s bucket unroll). The gene has `DIST_MAX + 1` behaviours; the
shipped decode expresses `DIST_MAX` of them.

## Slope check (MEMORY's gene rule), flow172_g1000 padded, 96 antithetic draws, sigma 0.02

Over the 2,400 recorded decisions of `tests/data/trajectory_obs.npz`:

| | moves | mean abs delta |
|---|---|---|
| `plant_floor`, melon | **19.1 %** of (member, board) | 0.0116 share (0.19 steps) |
| `plant_floor`, any crop | 62.6 % | largest floor in the population 0.125 |
| `compact` OFF (shipped) | **0.00 %** | 0.0000 bands — the gene is dead, as audited |
| `compact` ON, gain 2.5 | **10.29 %** | 0.1029 bands; band 8 on 46.9 % of days |

Identity: `flow172_g1000` (6,789) vs its zero-pad (6,954) decodes **0 field mismatches over
2,400 boards** with the floor switch OFF *and* ON, and plans equal array for array on four
boards. `plant_target[MELON]` is 0 on all 2,400 for the incumbent; with `gb12[MELON] = 2.0`
melon takes the whole allocation on 864 of the 1,584 boards that plant >= 8 tiles, up to 22
tiles on a day-0 board — the twelve-melon corner is expressible.

Tests: `tests/test_plant_floor.py` 22 passed (layout, pad, decode, OFF/ON identity, corner,
slope, backend agreement); with the layout-sensitive suites
(`test_forward_value`, `test_forward_gene`, `test_global_product`, `test_forecast_feature`,
`test_es_masking`, `test_genome_retype`) **103 passed**. Three of those pinned the layout's
tail rather than their own block's end and are re-pinned in the second commit.
The 42 test files that mention `largest_remainder`, `plant_target` or `compact` (578 tests,
engine-heavy `archetype`/`abs`/`eval` suites excluded for time) give **574 passed, 4 failed**
-- and all four (`test_dev_locality::test_a_shorter_theta_is_inert`,
`test_dev_weight::test_a_saturated_weight_never_outranks_a_mandatory_tile`,
`test_open_pump::test_on_traces_under_jit_and_keeps_both_legs[3]`,
`test_open_pump_racer::test_slot0_traces_under_jit_and_keeps_both_legs`) fail identically on
the base commit checked out clean. Pre-existing, not this branch.

## Launching an arm

Turn `brain.PLANT_FLOOR_ON = True` in the staged tree (and `plan.COMPACT_SOFT_ON = True`
only for a separate arm — one switch per arm, or the A/B reads two changes).

    --init-theta artifacts/kagg2_games/thetas/flow172_g300.npy   # auto-pads 6,789 -> 6,954
    --train-only g12,gb12 --sigma 0.02 --optimizer sgd --weight-decay 0

The switch travels with the tree, so the packaged submission must be built from a tree with
the same switch state the arm trained under — a 6,954 theta run with `PLANT_FLOOR_ON =
False` silently loses the gene and plants the incumbent's mix.

`g12,gb12` first: 165 coordinates against 5,997 live, so the champion is held byte for byte
and the same population buys ~36x the samples per coordinate. Widen to
`g1,gb1,g12,gb12` only after the narrow arm shows a gain. Gate: paired LIVE55 + TOPB,
drawn legs veto only (per the held-out judge rule) — melon's ledgered loss is -14.1k a
game, decisive in 69 of 88 live losses, so the arm is worth a full gate and not a legs read.
