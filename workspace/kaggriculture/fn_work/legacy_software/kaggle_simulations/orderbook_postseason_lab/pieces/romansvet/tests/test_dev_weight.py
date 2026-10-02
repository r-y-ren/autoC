"""`dev_weight`: *how much* of the day's labour development is worth (R4).

`v_plant` and `v_place` price a fresh tile at its stream value under
`grow_mult` -- which is per *product* and also sizes the purchase budget, so
nothing before this could say "spend more of today's turns on development"
without also buying more seed. `dev_weight` scales the two task values and
nothing else, so the day's seed order is unchanged and only the labour
boundary moves.

It scales the **value**, never the tier. Promoting development into the
mandatory tier was measured at -23,312 +- 9,198 coins against `starter` and
-6,041 +- 10,635 against `kagg2`: the route order carries no value information
inside a group, so anything admitted ahead of a harvest spends the turns the
harvest needed. Development has to win the labour on coins.

Measured at x3 on top of the one-crossing route, 16 paired games per matchup:
+6,117 +- 7,179 coins against `starter`, +4,896 +- 12,143 against `kagg2`, and
+9,341 +- 4,768 on the `kagg2` margin.
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
from test_admit_route import TABLE, _farm, _ripe
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import budget as BUD
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO

ONE = brain.GROW_ONE


def _derive(view, macro):
    return P._derive(np, view, macro, TABLE, np.int32(0), False, np.int32(0))


def _one_wheat(weight):
    return _macro(plant_target=np.array([1, 0, 0, 0, 0], np.int32),
                  dev_weight=np.int32(weight))


def test_dev_weight_is_one_at_zero_theta():
    from test_genome_retype import _obs_sell
    m = brain.decide(np, np.zeros(PO.N_PARAMS, np.float32), _obs_sell())
    assert int(m.dev_weight) == ONE


def test_a_weight_of_one_leaves_every_task_value_where_it_was():
    """x1 has to be exact, not approximately exact: `v * ONE // ONE == v` for
    every non-negative int, which is what makes every incumbent checkpoint's
    admission order identical."""
    view = _farm({60: _ripe(spec.I_TOMATO, 3)})._replace(money=np.int32(50_000))
    d = _derive(view, _one_wheat(ONE))
    plant = np.flatnonzero(np.asarray(d.chain_op[:, 0]) == O.OP_PLANT).tolist()
    assert plant == [0]
    # 4 wheat units at the fixture's 25 coins, unscaled
    assert int(d.tile_value[0]) == 100


def test_a_saturated_weight_lifts_a_planting_above_an_optional_harvest():
    """The admission order is (tier, value), so this is where the gene bites:
    a wheat planting worth 100 sits behind a three-unit tomato harvest worth
    180 at x1, and ahead of it at x2 and x4. Nothing about the route changed --
    the planting simply bought its way past the harvest in coins."""
    view = _farm({60: _ripe(spec.I_TOMATO, 3)})._replace(money=np.int32(50_000))
    heads = {}
    for w in (ONE, 2 * ONE, 4 * ONE):
        d = _derive(view, _one_wheat(w))
        assert int(d.tile_value[60]) == 180 and int(d.tier[60]) == 0
        assert int(d.tile_value[0]) == 100 * (w // ONE)
        heads[w] = int(P.task_order(np, d.task, d.tile_value, d.tier)[0])
    assert heads == {ONE: 60, 2 * ONE: 0, 4 * ONE: 0}


def test_a_saturated_weight_never_outranks_a_mandatory_tile():
    """Work that is lost for good if skipped today outranks every optional
    tile whatever the values say [LAW, 0.5], and `dev_weight` touches the
    value alone. A day-26 wheat harvest is worth 25 coins against a planting
    the gene has taken to 200, and it still heads the admission order."""
    tile = {"kind": spec.KIND_PLANT, "occ": spec.I_WHEAT, "t_yield": 1, "t_day": 20}
    view = _farm({60: tile}, day=26)._replace(money=np.int32(50_000))
    for w in (ONE, 4 * ONE):
        d = _derive(view, _one_wheat(w))
        assert int(d.tier[60]) == 1 and int(d.tile_value[60]) == 25
        assert int(d.tile_value[0]) == 50 * (w // ONE)
        assert int(P.task_order(np, d.task, d.tile_value, d.tier)[0]) == 60


def test_the_scaled_value_stays_inside_int32_at_the_coin_ceiling():
    """`v_plant` is clipped to `VALUE_CAP` on the way in as well as out, so the
    product is at most `VALUE_CAP * 4 * GROW_ONE` < 2**30 whatever the price
    table says. Asserted on the arithmetic, because the board that would reach
    it is not constructible in a season."""
    assert BUD.VALUE_CAP * 4 * ONE < 2 ** 31 - 1
    cap = np.int32(BUD.VALUE_CAP)
    for w in (ONE, 4 * ONE):
        scaled = np.clip(np.int32(cap) * np.int32(w) // np.int32(ONE), 0, cap)
        assert scaled.dtype == np.int32 and int(scaled) == BUD.VALUE_CAP


def test_dev_weight_does_not_move_the_day_purchases():
    """It is a labour weight, not a budget one: `grow_mult` sizes the seed
    order and `dev_weight` is deliberately absent from it, so the same day
    buys the same seed however the gene is set."""
    from test_budget_order import _buy_qty
    view = _farm({})._replace(money=np.int32(4_000))
    macro = _macro(plant_target=np.array([12, 0, 0, 0, 0], np.int32))
    base = _buy_qty(view, macro, O.MO_BUY_SEED)
    assert base > 0
    assert _buy_qty(view, macro._replace(dev_weight=np.int32(4 * ONE)), O.MO_BUY_SEED) == base


def test_dev_weight_is_int32_on_both_backends():
    import jax
    import jax.numpy as jnp
    from test_genome_retype import _obs_sell, _theta_with
    th = _theta_with(sell=1.5, gate=0.7, grow=-0.4)
    obs = _obs_sell()
    for xp, t, o in ((np, th, obs),
                     (jnp, jnp.asarray(th), jax.tree_util.tree_map(jnp.asarray, obs))):
        m = brain.decide(xp, t, o)
        for name in ("compact", "dev_weight"):
            v = np.asarray(getattr(m, name))
            assert v.dtype == np.int32 and v.shape == (), (xp.__name__, name)


def test_the_weight_is_capped_at_the_same_four_times_as_grow_mult():
    """The cap is what keeps the product inside int32, so it is pinned rather
    than left to the transform. `_unit_ratio` is unbounded above."""
    theta = np.zeros(PO.N_PARAMS, np.float32)
    from test_genome_retype import _obs_sell
    theta[PO.offset("gb6") + 1] = 40.0
    m = brain.decide(np, theta, _obs_sell())
    assert int(m.dev_weight) == int(brain.GROW_MAX * ONE) == 4 * ONE
    theta[PO.offset("gb6") + 1] = -40.0
    assert int(brain.decide(np, theta, _obs_sell()).dev_weight) == 0
