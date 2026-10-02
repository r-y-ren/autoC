"""The production-forecast block: what it says, and what it must not change.

`brain.production_forecast` is the 2026-09-08 plateau diagnosis' section 4
input -- per-product, per-board, *when* supply arrives rather than how many
tiles make it. It reaches the network through `policy.SHAPES`' appended `fh`
and `fs`, so the whole block has to be inert on every theta trained before it,
and the numpy and JAX backends have to compute it identically or the packaged
agent plays moves the trained agent never would.

Three groups here:

* the semantics of the forecast itself, on hand-built boards where the answer
  is arithmetic off `spec` rather than a golden number;
* the identity: an upgraded theta decodes bit for bit as the 4,980-parameter
  original, over the recorded trajectory fixture;
* numpy vs JAX on the new columns, on boards whose clocks are spread over the
  season so the interval arithmetic is actually exercised.
"""
import os
import pathlib
import sys

import numpy as np
import pytest

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO

FIXTURE = ROOT / "tests" / "data" / "trajectory_obs.npz"
THETA = ROOT / "artifacts" / "theta.npy"
N_COLS = PO.N_FCAST_FEAT


def _obs(day=0, own=(), opp=(), money=5000, shed=None):
    """A board from a list of (kind, occ, planted_day, yield_units) tiles."""
    def board(tiles):
        kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
        occ = np.full(spec.N_TILES, -1, np.int32)
        t_day = np.zeros(spec.N_TILES, np.int32)
        t_yield = np.zeros(spec.N_TILES, np.int32)
        for i, (k, o, d, y) in enumerate(tiles):
            kind[i], occ[i], t_day[i], t_yield[i] = k, o, d, y
        return kind, occ, t_day, t_yield

    k, o, td, ty = board(own)
    ok, oo, otd, oty = board(opp)
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(money), opp_money=np.int32(money),
        kind=k, occ=o, opp_kind=ok, opp_occ=oo, t_day=td, t_yield=ty,
        opp_t_day=otd, opp_t_yield=oty,
        shed=np.zeros(spec.N_ITEMS, np.int32) if shed is None else shed,
        seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.array([spec.DEFAULT_MARKET_PARAMS[n]["base"]
                        for n in spec.PRODUCTS], np.int32),
        shops=np.zeros(8, np.int32))


def _plant(crop, planted_day, yield_units=0):
    return (spec.KIND_PLANT, crop, planted_day, yield_units)


def _animal(a, placed_day, yield_units=0):
    return (int(spec.ANIMAL_STRUCT[a]), a, placed_day, yield_units)


# ---------------------------------------------------------------- semantics

def test_shape_and_scale():
    f = np.asarray(brain.production_forecast(np, _obs()))
    assert f.shape == (spec.N_PRODUCTS, N_COLS)
    assert f.dtype == np.float32
    assert not f.any(), "an empty board forecasts nothing"


def test_equal_counts_different_clocks_now_differ():
    """The plateau diagnosis' complaint, as a test.

    Eight strawberry tiles are eight strawberry tiles to `features` whether the
    first yield is tomorrow or a week out -- `prod_feat` column 7 is a count.
    The forecast has to separate them, and the old columns still must not move.
    """
    tiles_a = [_plant(spec.I_STRAWBERRY, 0)] * 8      # planted day 0
    tiles_b = [_plant(spec.I_STRAWBERRY, 8)] * 8      # planted day 8
    a, b = _obs(day=12, own=tiles_a), _obs(day=12, own=tiles_b)

    pa, ga, da = (np.asarray(x) for x in brain.features(np, a))
    pb, gb, db = (np.asarray(x) for x in brain.features(np, b))
    assert np.array_equal(pa, pb) and np.array_equal(ga, gb) \
        and np.array_equal(da, db), "the old features cannot tell these apart"

    fa = np.asarray(brain.production_forecast(np, a))
    fb = np.asarray(brain.production_forecast(np, b))
    assert not np.array_equal(fa, fb), "the forecast must"
    # Age 12 against age 4, first yield at 10 every 2 days: the older board
    # banks one unit a tile within three days and two within seven, the younger
    # nothing within three and one within seven.
    scale = brain._FCAST_SCALE
    assert list(fa[spec.I_STRAWBERRY, :4] * scale[:4]) == [0.0, 0.0, 8.0, 16.0]
    assert list(fb[spec.I_STRAWBERRY, :4] * scale[:4]) == [0.0, 0.0, 0.0, 8.0]

    # And the standing column separates them too, once there is something to
    # harvest: the day-0 planting is past its first yield and the day-8 one is
    # not, so only the older board's units are reachable today.
    held = [_plant(spec.I_STRAWBERRY, 0, 2)] * 8, [_plant(spec.I_STRAWBERRY, 8, 2)] * 8
    ra = np.asarray(brain.production_forecast(np, _obs(day=12, own=held[0])))
    rb = np.asarray(brain.production_forecast(np, _obs(day=12, own=held[1])))
    assert float(ra[spec.I_STRAWBERRY, 0] * scale[0]) == 16.0
    assert rb[spec.I_STRAWBERRY, 0] == 0.0


def test_ongoing_crop_counts_its_interval():
    """Strawberry: first yield at age 10, one unit every 2 days, 4 in a life."""
    first = int(spec.CROP_FIRST_YIELD_DAY[spec.I_STRAWBERRY])
    iv = int(spec.CROP_INTERVAL[spec.I_STRAWBERRY])
    mxy = int(spec.CROP_MAX_YIELD[spec.I_STRAWBERRY])
    assert (first, iv, mxy) == (10, 2, 4)
    scale = brain._FCAST_SCALE

    # Planted on day 0, read on day 9: the first fire is at the end of day 9
    # (age 10 tomorrow), then day 11, 13, 15 -- so 1 within a day, 2 within 3
    # and 4 (its whole life) within 7.
    f = np.asarray(brain.production_forecast(
        np, _obs(day=9, own=[_plant(spec.I_STRAWBERRY, 0)])))
    got = f[spec.I_STRAWBERRY, :4] * scale
    assert list(got) == [0.0, 1.0, 2.0, 4.0]

    # Ten of them, and the lifetime cap still holds at 7 days out.
    f = np.asarray(brain.production_forecast(
        np, _obs(day=9, own=[_plant(spec.I_STRAWBERRY, 0)] * 10)))
    assert float(f[spec.I_STRAWBERRY, 3] * scale[3]) == 40.0


def test_one_time_crop_counts_its_water_window():
    """Wheat: one unit per watered day in [window start, max yield day], cap 6."""
    ws = int(spec.CROP_WINDOW_START[spec.I_WHEAT])
    mxd = int(spec.CROP_MAX_YIELD_DAY[spec.I_WHEAT])
    mxy = int(spec.CROP_MAX_YIELD[spec.I_WHEAT])
    assert (ws, mxd, mxy) == (2, 4, 6)
    scale = brain._FCAST_SCALE

    # Age 0 on day 0, holding its seeded unit. Watering tomorrow finds it at
    # age 1, still short of the window, so nothing within a day; ages 2 and 3
    # land within three days and age 4 closes it out within seven -- and never
    # more than 3, because the window closes.
    f = np.asarray(brain.production_forecast(
        np, _obs(day=0, own=[_plant(spec.I_WHEAT, 0, 1)])))
    assert list(f[spec.I_WHEAT, :4] * scale[:4]) == [0.0, 0.0, 2.0, 3.0]

    # Already at the cap: no water can add to it.
    f = np.asarray(brain.production_forecast(
        np, _obs(day=0, own=[_plant(spec.I_WHEAT, 0, mxy)])))
    assert not f[spec.I_WHEAT, 1:4].any()

    # Past its first yield with units standing: harvestable now.
    f = np.asarray(brain.production_forecast(
        np, _obs(day=5, own=[_plant(spec.I_WHEAT, 0, 4)])))
    assert float(f[spec.I_WHEAT, 0] * scale[0]) == 4.0


def test_animals_and_their_fertilizer():
    """A goose lays at age 4 then every day; every animal makes fertilizer."""
    first = int(spec.ANIMAL_FIRST_YIELD_DAY[0])
    iv = int(spec.ANIMAL_INTERVAL[0])
    assert (first, iv) == (4, 1)
    scale = brain._FCAST_SCALE
    f = np.asarray(brain.production_forecast(
        np, _obs(day=3, own=[_animal(0, 0)])))
    # First fire at the end of day 3 (age 4 tomorrow), then daily.
    assert list(f[spec.I_EGG, :4] * scale[:4]) == [0.0, 1.0, 3.0, 7.0]
    # Fertilizer is one a day per living animal from the day it is placed, and
    # its standing quantity is not observable, so column 0 stays empty.
    assert list(f[spec.I_FERT, :4] * scale[:4]) == [0.0, 1.0, 3.0, 7.0]


def test_opponent_half_reads_the_opponent_board():
    tiles = [_animal(2, 0)] * 3                      # three sheep
    ours = np.asarray(brain.production_forecast(np, _obs(day=10, own=tiles)))
    theirs = np.asarray(brain.production_forecast(np, _obs(day=10, opp=tiles)))
    half = N_COLS // 2
    assert np.array_equal(ours[:, :half], theirs[:, half:])
    assert not ours[:, half:].any() and not theirs[:, :half].any()


def test_no_private_state_reaches_the_forecast():
    """Shed, seeds and cash are private; the forecast must not read them."""
    base = _obs(day=6, own=[_plant(spec.I_TOMATO, 0)], opp=[_animal(1, 1)])
    shed = np.arange(spec.N_ITEMS, dtype=np.int32) * 7
    seeds = np.arange(spec.N_CROPS, dtype=np.int32) + 3
    other = base._replace(shed=shed, seeds=seeds, money=np.int32(99999),
                          opp_money=np.int32(1), mkt_inv=base.mkt_inv + 40)
    assert np.array_equal(np.asarray(brain.production_forecast(np, base)),
                          np.asarray(brain.production_forecast(np, other)))


# ------------------------------------------------------- the identity check

@pytest.mark.skipif(not FIXTURE.is_file(), reason="needs the trajectory fixture")
def test_upgraded_theta_decodes_identically():
    """Check 1: `scripts/upgrade_theta.py`'s pad changes no decision.

    Every recorded observation in the fixture, decoded by a pre-forecast theta
    and by the same theta padded to this layout. `policy.unpack` pads a short
    theta on the way in, so this is really the assertion that the pad and the
    decode agree -- and, run against a golden dump taken before the block
    existed, that neither moved. `artifacts/theta.npy` is 4,980 parameters or
    shorter; either way it predates `fh`/`fs`.
    """
    if not THETA.is_file():
        pytest.skip("needs a trained theta")
    old = np.load(THETA).astype(np.float32)
    assert old.shape[0] < PO.N_PARAMS, "this theta already carries the block"
    new = PO.pad(old)
    assert new.shape == (PO.N_PARAMS,)
    assert np.array_equal(new[:old.shape[0]], old)
    assert not new[PO.offset("fh"):].any(), "the appended block must be zeros"

    d = np.load(FIXTURE)
    present = [f for f in brain.PolicyObs._fields if f in d.files]
    n = len(d["day"])
    assert n >= 1000, f"fixture too small to be meaningful: {n}"
    bad = []
    for i in range(n):
        o = brain.PolicyObs(**{f: d[f][i] for f in present})
        a, b = brain.decide(np, old, o), brain.decide(np, new, o)
        for f, x, y in zip(a._fields, a, b):
            if not np.array_equal(np.asarray(x), np.asarray(y)):
                bad.append(f"decision {i}: {f}")
    assert not bad, f"{len(bad)} of {n} decisions moved:\n" + "\n".join(bad[:10])


def test_zero_block_is_inert_in_the_forward_pass():
    """The other half of the identity: a caller that has no forecast at all and
    one that has a real one must agree while `fh`/`fs` are zero."""
    rng = np.random.default_rng(7)
    theta = rng.normal(0.0, 0.3, PO.N_PARAMS).astype(np.float32)
    theta[PO.offset("fh"):] = 0.0
    p = PO.unpack(np, theta)
    obs = _obs(day=11, own=[_plant(spec.I_MELON, 3), _animal(1, 2)],
               opp=[_plant(spec.I_TOMATO, 1)] * 4)
    prod, glob, drain = brain.features(np, obs)
    fcast = brain.production_forecast(np, obs)
    a = PO.forward(np, p, prod, glob, drain)
    b = PO.forward(np, p, prod, glob, drain, fcast)
    for f, x, y in zip(a._fields, a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y)), f
    # ... and not inert once the block is trained away from zero.
    theta[PO.offset("fs"):] = 0.25
    c = PO.forward(np, PO.unpack(np, theta), prod, glob, drain, fcast)
    assert not np.array_equal(np.asarray(a.scores), np.asarray(c.scores))


# --------------------------------------------------------- backend agreement

def _spread_boards(n=48, seed=11):
    """Boards whose clocks are spread over the season, both seats occupied."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        day = int(rng.integers(0, spec.N_DAYS))
        def tiles():
            ts = []
            for _ in range(int(rng.integers(0, 30))):
                if rng.random() < 0.65:
                    c = int(rng.integers(0, spec.N_CROPS))
                    ts.append(_plant(c, int(rng.integers(0, day + 1)),
                                     int(rng.integers(0, int(spec.CROP_MAX_YIELD[c]) + 1))))
                else:
                    a = int(rng.integers(0, spec.N_ANIMALS))
                    ts.append(_animal(a, int(rng.integers(0, day + 1)),
                                      int(rng.integers(0, int(spec.ANIMAL_MAX_HELD[a]) + 1))))
            return ts
        out.append(_obs(day=day, own=tiles(), opp=tiles()))
    return out


def test_numpy_matches_jax_on_the_forecast():
    """Check 2. The trainer runs the JAX path and the submission the numpy one;
    a forecast that differs between them is a train/serve divergence, and every
    quantity `decide` derives from it is a `floor` away from a different move."""
    import jax
    import jax.numpy as jnp
    from kagg3 import precision  # noqa: F401  pins matmul precision at import

    jf = jax.jit(lambda *fs: brain.production_forecast(jnp, brain.PolicyObs(*fs)))
    worst = 0.0
    nonzero = 0
    for obs in _spread_boards():
        a = np.asarray(brain.production_forecast(np, obs))
        b = np.asarray(jf(*[None if v is None else jnp.asarray(v) for v in obs]))
        assert a.shape == b.shape == (spec.N_PRODUCTS, N_COLS)
        worst = max(worst, float(np.abs(a - b).max()))
        nonzero += int((a != 0).sum())
        assert np.array_equal(a, b), f"forecast differs\nnumpy={a}\njax={b}"
    assert nonzero > 500, f"the boards barely produced anything: {nonzero}"
    assert worst == 0.0


def test_numpy_matches_jax_on_the_decision_with_a_trained_block():
    """The forecast reaching a decision, with `fh`/`fs` off zero so the block
    actually moves the scores -- the integer cliffs are what this is for."""
    import jax
    import jax.numpy as jnp
    from kagg3 import precision  # noqa: F401

    if not THETA.is_file():
        pytest.skip("needs a trained theta")
    rng = np.random.default_rng(3)
    theta = PO.pad(np.load(THETA).astype(np.float32))
    off = PO.offset("fh")
    theta[off:] = rng.normal(0.0, 0.2, PO.N_PARAMS - off).astype(np.float32)

    jd = jax.jit(lambda th, *fs: brain.decide(jnp, th, brain.PolicyObs(*fs)))
    jt = jnp.asarray(theta)
    bad = []
    for i, obs in enumerate(_spread_boards(n=24, seed=5)):
        a = brain.decide(np, theta, obs)
        b = jd(jt, *[None if v is None else jnp.asarray(v) for v in obs])
        for f, x, y in zip(a._fields, a, b):
            if not np.array_equal(np.asarray(x), np.asarray(y)):
                bad.append(f"board {i}: {f} numpy={np.asarray(x)} jax={np.asarray(y)}")
    assert not bad, "\n".join(bad[:10])
