"""Release gates 2 and 3 from GOAL.md.

Shared-tile actions are legal and execute in unit order. Their engine
equivalence regressions live in test_drop_op.py; no disjoint-tile invariant
is imposed on the planner.

Gate 1 (simulator vs kaggle_environments) lives in test_sim_equivalence.py.
"""
import os
import sys
import tarfile
import tempfile

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain, ops as O, plan as P, policy as PO


def _random_obs(rng) -> brain.PolicyObs:
    """A plausible mid-season position, not a uniformly random one."""
    n = spec.N_TILES
    kind = np.where(spec.TILE_QUAD < rng.integers(1, 5), spec.KIND_EMPTY,
                    spec.KIND_LOCKED).astype(np.int32)
    roll = rng.random(n)
    unlocked = kind == spec.KIND_EMPTY
    kind = np.where(unlocked & (roll < 0.45), spec.KIND_PLANT, kind)
    kind = np.where(unlocked & (roll >= 0.45) & (roll < 0.6), spec.KIND_COOP, kind)
    kind = np.where(unlocked & (roll >= 0.6) & (roll < 0.7), spec.KIND_PASTURE, kind)
    kind = np.where(unlocked & (roll >= 0.7) & (roll < 0.78), spec.KIND_WEED, kind)
    occ = np.where(kind == spec.KIND_PLANT, rng.integers(0, spec.N_CROPS, n),
                   np.where((kind == spec.KIND_COOP) | (kind == spec.KIND_PASTURE),
                            rng.integers(-1, spec.N_ANIMALS, n), -1)).astype(np.int32)
    opp_kind = kind[rng.permutation(n)]
    day = np.int32(rng.integers(0, spec.N_DAYS))
    return brain.PolicyObs(
        day=day,
        money=np.int32(rng.integers(0, 60000)),
        opp_money=np.int32(rng.integers(0, 60000)),
        kind=kind, occ=occ, opp_kind=opp_kind, opp_occ=occ[rng.permutation(n)],
        t_day=np.maximum(day - rng.integers(0, 14, n), 0).astype(np.int32),
        t_yield=rng.integers(0, 7, n).astype(np.int32),
        shed=rng.integers(0, 30, spec.N_ITEMS).astype(np.int32),
        seeds=rng.integers(0, 20, spec.N_CROPS).astype(np.int32),
        nquad=np.int32(rng.integers(1, 5)), opp_nquad=np.int32(rng.integers(1, 5)),
        mkt_inv=(spec.MARKET_I0 + rng.integers(-2000, 20000, spec.N_PRODUCTS)).astype(np.int32),
        price=rng.integers(1, 300, spec.N_PRODUCTS).astype(np.int32),
        shops=rng.integers(0, 3, spec.N_SHOPS).astype(np.int32),
    )


def test_numpy_matches_jax_policy():
    """Gate 2: training is JAX float32 on GPU, the submission is numpy on CPU.

    A divergence here would be silent and would invalidate every offline result,
    so this compares the whole decoded Macro -- the actual decision -- rather
    than just the raw network output.

    Breadth only: random weights and a synthetic board. That combination is too
    insensitive to catch a wrong matmul precision -- an untrained theta's
    sigmoids sit near 0.5, so `sigmoid * count` rarely lands on a floor
    boundary. This gate once passed while running at TF32, which is exactly the
    condition it should have failed on. The precision assertion below closes
    that, and tests/test_backend_agreement.py covers the trained-policy case on
    real trajectory observations.
    """
    import jax
    import jax.numpy as jnp

    # Not incidental to the comparison: at TF32 the forward pass is ~3.5e-3 from
    # numpy's, which flips floor() decisions. Asserted here so running this file
    # alone still catches an unpinned process, rather than passing because some
    # other test happened to be collected first and imported the pin.
    assert jax.config.jax_default_matmul_precision == "highest", (
        "JAX matmul precision is not pinned -- see kagg3.precision")
    rng = np.random.default_rng(0)
    for trial in range(40):
        theta = PO.init_theta(np.random.default_rng(100 + trial))
        obs = _random_obs(rng)
        m_np = brain.decide(np, theta, obs)
        jobs = brain.PolicyObs(*[None if v is None else jnp.asarray(v) for v in obs])
        m_jx = brain.decide(jnp, jnp.asarray(theta), jobs)
        for field, a, b in zip(m_np._fields, m_np, m_jx):
            assert np.array_equal(np.asarray(a), np.asarray(b)), \
                f"trial {trial}: macro field {field} differs: numpy={a} jax={b}"


def test_submission_has_no_training_deps():
    """The archive must never carry jax or torch into the 1.6 vCPU runtime."""
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import package_submission as pkg
    theta = os.path.join(ROOT, "artifacts", "theta.npy")
    if not os.path.exists(theta):
        pytest.skip("no theta yet")
    with tempfile.TemporaryDirectory() as d:
        out = pkg.build(__import__("pathlib").Path(theta),
                        __import__("pathlib").Path(d) / "s.tar.gz")
        assert not pkg.forbidden_imports()
        assert out.stat().st_size < 100 * 1024 * 1024
        with tarfile.open(out) as tf:
            names = tf.getnames()
        assert "main.py" in names and "theta.npy" in names


def test_planner_never_emits_cross_orders():
    """The simulator's market model assumes a SELL and a BUY_PRODUCT never land
    on the same item in the same slot (see docs/DESIGN.md). That holds because
    the planner emits one fixed slot layout for both seats -- this checks it
    rather than trusting it, across independently drawn positions for the two
    seats and every turn of the day."""
    from kagg3.sim import market

    rng = np.random.default_rng(7)
    for trial in range(50):
        plans = []
        for seat in range(2):
            theta = PO.init_theta(np.random.default_rng(900 + trial * 2 + seat))
            obs = _random_obs(rng)
            macro = brain.decide(np, theta, obs)
            view = P.DayView(
                day=obs.day, kind=obs.kind[P.SERP], occ=obs.occ[P.SERP],
                t_day=obs.t_day[P.SERP], t_water=np.zeros(spec.N_TILES, np.int32),
                t_cons=rng.integers(0, 2, spec.N_TILES).astype(np.int32),
                t_yield=obs.t_yield[P.SERP],
                t_fert=np.full(spec.N_TILES, -1, np.int32),
                t_cared=np.zeros(spec.N_TILES, np.int32),
                t_favail=rng.integers(0, 2, spec.N_TILES).astype(np.int32),
                shed=obs.shed, seeds=obs.seeds, money=obs.money, nquad=obs.nquad,
                price=obs.price)
            plans.append(P.build_day(np, view, macro))

        for h in range(spec.TURNS_PER_DAY):
            mkt_op = np.stack([plans[0][3][h], plans[1][3][h]])
            mkt_a = np.stack([plans[0][4][h], plans[1][4][h]])
            market.assert_no_cross(mkt_op, mkt_a, exempt=P.open_pump_exempt(h))


def _row_cost(view, plan):
    """Coins the day's turn-1 row commits, priced the way the engine walks it."""
    from kagg3.core import projector as PJ
    op, arg, qty = plan[3:6]
    quotes = PJ.buy_quotes(np, P.default_price_table(),
                           PJ.projected_inv(np, view.mkt_inv, view.shops, O.TURN_BUY))
    total = 0
    for s in range(spec.MAX_MARKET_ORDERS):
        o, a, q = int(op[O.TURN_BUY, s]), int(arg[O.TURN_BUY, s]), int(qty[O.TURN_BUY, s])
        if q == 0:
            continue
        if o == O.MO_BUY_PRODUCT:
            total += int(quotes[a, :q].sum())
        elif o == O.MO_BUY_SEED:
            total += q * int(spec.CROP_SEED_COST[a])
        elif o == O.MO_BUY_ANIMAL:
            total += q * int(spec.ANIMAL_COST[a])
    return total


def test_the_day_never_commits_more_than_the_purse_it_has():
    """PLANNER_V3_1 1.5's coin order, fuzzed: hire bill, then the cash reserve,
    then land, then the greedy -- and the whole of it inside `view.money`.

    Two assertions, because only one of the four may draw on money that has not
    landed yet. Everything that resolves at turn 1 has to fit the hour-0 purse
    net of the bill and the reserve; the land price alone may lean on the
    morning's projected lot-1 revenue (M2), and even then only on a 3/4
    discount of it -- so the bound here uses the *whole* shed's lot-1 revenue,
    which is strictly larger than anything `_derive` can have counted.

    The reserve is the part that has no give: a day that spent it would leave
    the farm unable to field a crew tomorrow, and a farm with no crew earns
    nothing, which is a spiral rather than a bad day.
    """
    from kagg3.core import projector as PJ
    from kagg3.core import sell as SELL

    rng = np.random.default_rng(11)
    table = P.default_price_table()
    checked = 0
    for trial in range(200):
        theta = PO.init_theta(np.random.default_rng(500 + trial))
        obs = _random_obs(rng)
        macro = brain.decide(np, theta, obs)
        view = P.DayView(
            day=obs.day, kind=obs.kind[P.SERP], occ=obs.occ[P.SERP],
            t_day=obs.t_day[P.SERP], t_water=np.zeros(spec.N_TILES, np.int32),
            t_cons=rng.integers(0, 2, spec.N_TILES).astype(np.int32),
            t_yield=obs.t_yield[P.SERP], t_fert=np.full(spec.N_TILES, -1, np.int32),
            t_cared=np.zeros(spec.N_TILES, np.int32),
            t_favail=rng.integers(0, 2, spec.N_TILES).astype(np.int32),
            shed=obs.shed, seeds=obs.seeds, money=obs.money, nquad=obs.nquad,
            price=obs.price, mkt_inv=obs.mkt_inv, shops=obs.shops)
        plan = P.build_day(np, view, macro)
        op, qty = plan[3], plan[5]

        n_hire = int((op == O.MO_HIRE).sum())
        bill = int(spec.HIRE_COST[:n_hire].sum())
        reserve = int(P.cash_reserve(np, np.int32(n_hire), view.day))
        row = _row_cost(view, plan)
        land = (int(qty[op == O.MO_BUY_LAND].sum())
                * int(spec.LAND_PRICES[min(int(view.nquad) - 1, 2)]))
        money = int(view.money)

        assert bill + reserve + row <= money, (
            f"trial {trial}: turn-1 commitments {bill} + {reserve} + {row} "
            f"exceed the hour-0 purse {money}")

        q1 = PJ.sell_quotes(np, table,
                            PJ.projected_inv(np, view.mkt_inv, view.shops, O.SELL_TURNS[0]))
        rev1_cap = int(PJ.sell_revenue(np, q1, view.shed[:spec.N_PRODUCTS]).sum())
        assert bill + reserve + row + land <= money + rev1_cap, (
            f"trial {trial}: the day committed {bill + reserve + row + land} against "
            f"{money} in hand and at most {rev1_cap} the morning could fetch")
        checked += land > 0
    assert checked > 0, "no trial bought land; the land half of the invariant is vacuous"
    assert SELL.N_LOTS == len(O.SELL_TURNS)
