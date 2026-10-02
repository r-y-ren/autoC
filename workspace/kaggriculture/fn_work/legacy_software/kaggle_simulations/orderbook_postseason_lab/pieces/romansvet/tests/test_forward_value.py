"""The forward-value block (`policy.SHAPES`' `fv`, 2026-09-09).

The global head reads `glob_feat` and, since `gp`, a summary of the encoder --
and neither of them says **when the standing board pays**. `glob_feat` counts
planted tiles, free slots, cash and quadrants; `spec.CROP_WINDOW_START` is not
in it. So the head that sizes the crew, the land bias, dev_frac and the animal
share reads an identical vector on a twelve-melon day-0 opening that emits no
task for six days and on a wheat board that pays tomorrow, which is precisely
what the forced-opening diagnostic measured: the melon board prices hands
against an empty task set and hires nobody.

`brain.forward_value` is the missing number -- per seat, over horizons 1, 3 and
7 days, the units the board will produce and what they are worth at today's
quote -- and `fv` is the zero-init path from it into the head's
pre-activation.

Three groups, the same three every appended block here has to pass:

* the layout: an append at the tail, nothing before it moved, and a padded
  champion plans byte for byte on six fixed boards;
* the semantics of the feature itself, on hand-built boards where the answer is
  arithmetic off `spec` rather than a golden number;
* numpy vs JAX with the block trained off zero -- the trainer runs one backend
  and the submission the other, and every decoded quantity is a `floor` away
  from a different move.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")

import numpy as np
import pytest
from test_forward_admit import BASE, TABLE, _melon_open, _ripe

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import plan as P
from kagg3.core import policy as PO

#: The layout `fv` appends to -- the forward-admit gene's, i.e. the length of
#: every theta written before 2026-09-09 21:00Z (`flow135_g350_gpfwd` included).
PRE_FV_N = 6405

CHAMPION = ("/mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/"
            "flow135_g350_gpfwd.npy")

#: The same six boards `tests/test_forward_gene.py` pins its own append on:
#: three under the forced melon opening (the case the block exists for, before
#: / at / past its window) and three with real work on them, so
#: "byte-identical" is a claim about the decode and not about one lucky day.
BOARDS = [_melon_open(day=1),
          _melon_open(day=3, money=9_000),
          _melon_open(day=6, money=20_000),
          _ripe(),
          _ripe(day=4, money=500),
          _ripe(day=27, money=120_000)]


def _obs_of(view, opp_tiles=()):
    """The `PolicyObs` of a `DayView` -- the same board, seen by the network.

    Built from the view rather than blank so the forward-value vector on these
    boards is genuinely non-zero: "a zero block is inert" is only a claim about
    the *weights* if the feature it multiplies is not zero itself.
    """
    z = np.zeros(spec.N_TILES, np.int32)
    ok = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    oo = z - 1
    otd, oty = z.copy(), z.copy()
    for i, (k, o, d, y) in enumerate(opp_tiles):
        ok[i], oo[i], otd[i], oty[i] = k, o, d, y
    return brain.PolicyObs(
        day=np.asarray(view.day), money=np.asarray(view.money),
        opp_money=np.int32(3000),
        kind=np.asarray(view.kind), occ=np.asarray(view.occ),
        opp_kind=ok, opp_occ=oo,
        t_day=np.asarray(view.t_day), t_yield=np.asarray(view.t_yield),
        opp_t_day=otd, opp_t_yield=oty,
        shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.asarray(view.nquad), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=BASE.copy(), shops=np.zeros(spec.N_SHOPS, np.int32))


def _tiles_obs(day=0, own=(), opp=(), money=5000):
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
        shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=BASE.copy(), shops=np.zeros(spec.N_SHOPS, np.int32))


def _plant(crop, planted_day, yield_units=0):
    return (spec.KIND_PLANT, crop, planted_day, yield_units)


def _fv(obs):
    return np.asarray(brain.forward_value(np, obs))


#: Slices of the twelve-vector, in `brain.forward_value`'s documented order.
OWN_U, OWN_C, OPP_U, OPP_C = (slice(0, 3), slice(3, 6), slice(6, 9), slice(9, 12))


# ------------------------------------------------------------------ layout

def test_the_block_is_a_clean_append():
    """`fv` starts exactly where the previous layout ended, so `flow135_g350`
    and every theta before it is still a prefix rather than a re-layout."""
    assert PO.N_FWDVAL_FEAT == 12 == PO.N_FWDVAL_SEATS * PO.N_FWDVAL_CH * 3
    assert len(brain.FWDVAL_HORIZONS) == 3
    assert PO.offset("fv") == PRE_FV_N
    # The block's own end, not `N_PARAMS`: the next append lands past it, and
    # pinning the tail here would fail it by construction.
    assert PRE_FV_N + PO.N_FWDVAL_FEAT * PO.N_HEAD_HID == 6789
    names = [n for n, _ in PO.SHAPES]
    assert names[names.index("gb11") + 1] == "fv"
    # No bias block: `gb1` is already the bias on this pre-activation, exactly
    # as for `gp`.
    assert "gbv" not in dict(PO.SHAPES) and "fvb" not in dict(PO.SHAPES)
    # Every new coordinate is live -- `fv` feeds `gh`, and `gh` feeds outputs
    # `brain.decide` reads -- and `--train-only` can name the block on its own,
    # which is how the arm is meant to be run.
    end = PO.offset("fv") + PO.N_FWDVAL_FEAT * PO.N_HEAD_HID
    assert PO.live_mask()[PO.offset("fv"):end].all()
    from kagg3.es.train import train_mask
    m = train_mask("fv")
    assert m[PO.offset("fv"):end].all() and not m[:PO.offset("fv")].any()


def test_market_momentum_is_a_clean_inert_append():
    """The 66 new coordinates follow `fv`; zero padding preserves its policy."""
    assert PO.N_MOMENTUM_FEAT == 1
    assert PO.offset("mh") == 6789
    assert PO.offset("ms") == 6853
    assert PO.offset("ms") + PO.N_MOMENTUM_FEAT * PO.N_ENC_OUT == 6855
    assert PO.Params._fields[PO.Params._fields.index("mh") + 1] == "ms"

    rng = np.random.default_rng(91)
    old = rng.normal(0.0, 0.3, 6789).astype(np.float32)
    padded = PO.pad(old)
    assert padded[:6789].tobytes() == old.tobytes()
    assert not padded[6789:].any()
    prod, glob, drain, fcast, fwdval = _inputs(6)
    momentum = rng.normal(size=(spec.N_PRODUCTS, 1)).astype(np.float32)
    params = PO.unpack(np, padded)
    before = PO.forward(np, params, prod, glob, drain, fcast, fwdval)
    after = PO.forward(np, params, prod, glob, drain, fcast, fwdval, momentum)
    for name, a, b in zip(before._fields, before, after):
        assert np.asarray(a).tobytes() == np.asarray(b).tobytes(), name


def test_market_momentum_direct_score_is_product_local():
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("ms")] = np.float32(0.5)
    prod, glob, drain, fcast, fwdval = _inputs(7)
    momentum = np.zeros((spec.N_PRODUCTS, 1), np.float32)
    momentum[spec.I_TOMATO, 0] = 1
    base = PO.forward(np, PO.unpack(np, theta), prod, glob, drain, fcast, fwdval)
    got = PO.forward(np, PO.unpack(np, theta), prod, glob, drain, fcast,
                     fwdval, momentum)
    delta = np.asarray(got.scores) - np.asarray(base.scores)
    assert delta[spec.I_TOMATO].tolist() == [0.5, 0.0]
    assert not np.delete(delta, spec.I_TOMATO, axis=0).any()


def test_nonzero_market_momentum_matches_complete_plans_across_backends():
    """A live mh/ms sentinel must agree through integer decode and routing."""
    import jax
    import jax.numpy as jnp

    view = BOARDS[3]
    obs = _obs_of(view)
    base = PO.pad(np.load("artifacts/kagg2_games/thetas/flow193_g100_hr.npy"))
    previous = np.asarray(obs.mkt_inv).copy()
    previous[spec.I_MILK] += int(brain._T[spec.I_MILK])
    shifted = obs._replace(prev_mkt_inv=previous)
    steady = obs._replace(prev_mkt_inv=np.asarray(obs.mkt_inv).copy())
    assert brain.market_momentum(np, shifted)[spec.I_MILK, 0] == 1
    assert not brain.market_momentum(np, steady).any()

    def evaluate(xp, theta, observation, day_view, table):
        macro = brain.decide(xp, theta, observation)
        return tuple(macro) + tuple(P.build_day(xp, day_view, macro, table)[:6])

    compiled = jax.jit(lambda theta, observation, day_view, table:
                       evaluate(jnp, theta, observation, day_view, table))
    fields = list(P.Macro._fields) + [f"plan_{i}" for i in range(6)]
    for gene, value in (("mh", 0.25), ("ms", 0.5)):
        theta = base.copy()
        theta[PO.offset(gene)] = np.float32(value)
        for observation in (steady, shifted):
            expected = evaluate(np, theta, observation, view, TABLE)
            actual = compiled(jnp.asarray(theta),
                              jax.tree_util.tree_map(jnp.asarray, observation),
                              jax.tree_util.tree_map(jnp.asarray, view), jnp.asarray(TABLE))
            for name, a, b in zip(fields, expected, actual):
                a, b = np.asarray(a), np.asarray(b)
                assert a.dtype == b.dtype and a.shape == b.shape, (gene, name)
                assert a.tobytes() == b.tobytes(), (gene, name)


def test_pad_zero_extends_and_keeps_the_prefix():
    rng = np.random.default_rng(1)
    old = rng.normal(0.0, 0.3, PRE_FV_N).astype(np.float32)
    new = PO.pad(old)
    assert new.shape == (PO.N_PARAMS,)
    assert np.array_equal(new[:PRE_FV_N], old)
    assert not new[PO.offset("fv"):].any()


# --------------------------------------------------------------- semantics

def test_the_melon_opening_is_visible_only_at_the_far_horizon():
    """The forced-opening diagnostic, as a feature.

    Melon's water window is `[CROP_WINDOW_START, CROP_MAX_YIELD_DAY]` = [6, 12]
    and a one-time crop takes one unit per watered day in it, so twelve tiles
    planted on day 0 produce nothing within a day or three of day 0 and 2 units
    a tile within seven (days 6 and 7). By day 4 the +3d horizon has reached
    the window too, and the +7d one sees the whole of it.
    """
    n = 12
    ws = int(spec.CROP_WINDOW_START[spec.I_MELON])
    mxd = int(spec.CROP_MAX_YIELD_DAY[spec.I_MELON])
    assert (ws, mxd) == (6, 12)
    tiles = [_plant(spec.I_MELON, 0)] * n

    def units(day):
        return _fv(_tiles_obs(day=day, own=tiles))[OWN_U] * brain._FWDVAL_UNIT_SCALE

    # day 0: the near horizons cannot see the window at all.
    d0 = units(0)
    assert list(d0) == [0.0, 0.0, float(n * (min(mxd, 7) - (ws - 1)))] == [0, 0, 24]
    # day 4: +3d reaches days 6 and 7 of the window, +7d the whole of it.
    d4 = units(4)
    assert list(d4) == [0.0, float(n * 2), float(n * (mxd - 5 - 1))] == [0, 24, 72]
    assert d4[2] > d0[2] > 0.0, "the far horizon must grow as the window nears"

    # And wheat pays at once, which is the contrast the head could not draw:
    # window [2, 4], so a day-1 board already banks a unit a tile within a day.
    wheat = _fv(_tiles_obs(day=1, own=[_plant(spec.I_WHEAT, 0)] * n))[OWN_U]
    assert float(wheat[0] * brain._FWDVAL_UNIT_SCALE[0]) == float(n)
    assert float(units(1)[0]) == 0.0, "melon says nothing tomorrow"


def test_the_coin_channel_prices_the_units():
    """Units alone cannot tell a wheat board from a melon board; coins can.

    Same tile count, same in-window days, quotes a factor of ten apart --
    `obs.price` is what the channel multiplies by, so the two boards agree on
    the units row and differ by exactly that ratio on the coins row.
    """
    n = 8
    wheat = _fv(_tiles_obs(day=1, own=[_plant(spec.I_WHEAT, 0)] * n))
    melon = _fv(_tiles_obs(day=7, own=[_plant(spec.I_MELON, 0)] * n))
    u_w = wheat[OWN_U] * brain._FWDVAL_UNIT_SCALE
    u_m = melon[OWN_U] * brain._FWDVAL_UNIT_SCALE
    assert float(u_w[0]) == float(u_m[0]) == float(n)      # one unit a tile, tomorrow
    c_w = float(wheat[OWN_C][0] * brain._FWDVAL_COIN_SCALE[0])
    c_m = float(melon[OWN_C][0] * brain._FWDVAL_COIN_SCALE[0])
    assert c_w == float(n * BASE[spec.I_WHEAT])
    assert c_m == float(n * BASE[spec.I_MELON])
    assert c_m == 10.0 * c_w                               # 250 against 25

    # An empty board says nothing at all, on either channel or either seat.
    assert not _fv(_tiles_obs()).any()


def test_the_two_seats_are_read_by_the_identical_expression():
    """The opponent's clock is public, and the melon race is a race: the same
    board on the other seat has to land in the opposite half of the vector,
    number for number."""
    tiles = [_plant(spec.I_MELON, 0)] * 12 + [_plant(spec.I_TOMATO, 2, 1)] * 5
    mine = _fv(_tiles_obs(day=9, own=tiles))
    theirs = _fv(_tiles_obs(day=9, opp=tiles))
    assert np.array_equal(mine[OWN_U], theirs[OPP_U])
    assert np.array_equal(mine[OWN_C], theirs[OPP_C])
    assert not mine[OPP_U].any() and not theirs[OWN_U].any()
    assert mine[OWN_U].any(), "the fixture must actually forecast something"

    # And a board carrying both seats is the two halves side by side.
    both = _fv(_tiles_obs(day=9, own=tiles, opp=tiles))
    assert np.array_equal(both[OWN_U], mine[OWN_U])
    assert np.array_equal(both[OPP_C], theirs[OPP_C])


def test_the_scales_are_dyadic_so_both_backends_agree():
    """[LAW] every divisor here is a power of two -- the quantities above are
    exact integers in float32 and a dyadic divisor is an exponent adjustment,
    which is what keeps numpy and `jax.jit` on the same `floor`."""
    for s in (brain._FWDVAL_UNIT_SCALE, brain._FWDVAL_COIN_SCALE):
        assert s.dtype == np.float32
        for v in s:
            assert float(v) > 0 and np.log2(float(v)) % 1.0 == 0.0, v
    assert _fv(_tiles_obs()).dtype == np.float32
    assert _fv(_tiles_obs()).shape == (PO.N_FWDVAL_FEAT,)


# ---------------------------------------------------------------- identity

def _inputs(seed):
    rng = np.random.default_rng(seed)
    return (rng.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_PROD_FEAT)).astype(np.float32),
            rng.normal(0.0, 1.0, PO.N_GLOBAL_FEAT).astype(np.float32),
            rng.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_DRAIN_FEAT)).astype(np.float32),
            rng.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_FCAST_FEAT)).astype(np.float32),
            rng.normal(0.0, 1.0, PO.N_FWDVAL_FEAT).astype(np.float32))


def _forward_pre_fv(p, prod, glob, drain, fcast):
    """`policy.forward` as it stood at 6,405 parameters, written out longhand.

    Comparing the new `forward` against itself with a zero block would prove
    nothing about the *expression*; this is the expression the champion was
    trained under.
    """
    x = np.concatenate([prod, np.broadcast_to(glob, (spec.N_PRODUCTS,
                                                     PO.N_GLOBAL_FEAT))], axis=1)
    pre = (x @ p.w1 + p.b1) + drain @ p.dh
    h = np.tanh(pre + fcast @ p.fh)
    scores = (h @ p.w2 + p.b2) + drain @ p.ds + fcast @ p.fs
    press = h @ p.w3 + p.b3
    summary = np.concatenate([scores, press], axis=1) / PO.PROD_SUMMARY_SCALE
    gh = np.tanh((glob @ p.g1 + p.gb1) + summary.reshape(PO.N_PROD_SUMMARY) @ p.gp)
    crew = gh @ p.g8 + p.gb8
    return PO.Outputs(scores=scores, head=gh @ p.g2 + p.gb2, prio=gh @ p.g3 + p.gb3,
                      gate=press[:, 0], lots=(gh @ p.g4 + p.gb4)[0],
                      aux=gh @ p.g5 + p.gb5, dev=gh @ p.g6 + p.gb6,
                      sat=(gh @ p.g7 + p.gb7)[0], crew=crew,
                      hire=np.concatenate([crew[:1], gh @ p.g9 + p.gb9]),
                      ramp=gh @ p.g10 + p.gb10, fwd=(gh @ p.g11 + p.gb11)[0],
                      crop_mix=np.zeros(spec.N_CROPS, np.float32))


@pytest.mark.parametrize("seed", range(8))
def test_padded_theta_reproduces_the_old_forward_exactly(seed):
    """A 6,405 theta padded to `N_PARAMS` computes, bit for bit, what the
    pre-`fv` forward computed from the same inputs -- with a *non-zero*
    forward-value vector, so the claim is about the weights."""
    rng = np.random.default_rng(100 + seed)
    old = rng.normal(0.0, 0.3, PRE_FV_N).astype(np.float32)
    prod, glob, drain, fcast, fwdval = _inputs(seed)
    p = PO.unpack(np, PO.pad(old))
    got = PO.forward(np, p, prod, glob, drain, fcast, fwdval)
    want = _forward_pre_fv(p, prod, glob, drain, fcast)
    for f, a, b in zip(got._fields, got, want):
        assert np.array_equal(np.asarray(a), np.asarray(b)), f


def test_a_nonzero_block_moves_the_global_outputs_only():
    """Off zero the block changes every head output -- and *only* those: `fv`
    joins the head's pre-activation, downstream of the encoder, so the
    per-product scores and the timing pressure must not move."""
    rng = np.random.default_rng(4)
    old = rng.normal(0.0, 0.3, PRE_FV_N).astype(np.float32)
    prod, glob, drain, fcast, fwdval = _inputs(3)
    base = PO.forward(np, PO.unpack(np, PO.pad(old)), prod, glob, drain, fcast, fwdval)

    theta = PO.pad(old)
    fv = PO.offset("fv")
    theta[fv:fv + PO.N_FWDVAL_FEAT * PO.N_HEAD_HID] = rng.normal(
        0.0, 0.1, PO.N_FWDVAL_FEAT * PO.N_HEAD_HID)
    got = PO.forward(np, PO.unpack(np, theta), prod, glob, drain, fcast, fwdval)

    for f in ("scores", "gate"):
        assert np.array_equal(np.asarray(getattr(got, f)),
                              np.asarray(getattr(base, f))), f
    for f in ("head", "prio", "lots", "aux", "dev", "sat", "crew", "hire",
              "ramp", "fwd"):
        assert not np.array_equal(np.asarray(getattr(got, f)),
                                  np.asarray(getattr(base, f))), f

    # The point of the block: two boards whose `glob_feat` is identical and
    # whose forward value differs now decode different global outputs.
    other = PO.forward(np, PO.unpack(np, theta), prod, glob, drain, fcast,
                       fwdval[::-1].copy())
    assert not np.array_equal(np.asarray(got.head), np.asarray(other.head))


@pytest.mark.skipif(not os.path.isfile(CHAMPION), reason="needs flow135_g350_gpfwd")
def test_the_padded_champion_plans_byte_for_byte():
    """`flow135_g350_gpfwd` zero-padded to 6,789 makes the identical decision
    and the identical plan on six boards -- the claim
    `artifacts/.../flow135_g350_gpfwdfv.npy` rests on."""
    old = np.load(CHAMPION).astype(np.float32)
    assert old.shape == (PRE_FV_N,), old.shape
    new = PO.pad(old)
    assert not new[PO.offset("fv"):].any()
    seen = 0
    for view in BOARDS:
        obs = _obs_of(view)
        # Not every board forecasts something -- `_ripe(day=13)`'s tomatoes are
        # past their lifetime cap -- but the claim is only worth making if some
        # of them do, so the vector the zero weights multiply is counted.
        seen += int(bool(_fv(obs).any()))
        a, b = brain.decide(np, old, obs), brain.decide(np, new, obs)
        for f, x, y in zip(a._fields, a, b):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"{view.day}: {f}"
        pa = [np.asarray(x) for x in P.build_day(np, view, a, TABLE)]
        pb = [np.asarray(x) for x in P.build_day(np, view, b, TABLE)]
        for i, (x, y) in enumerate(zip(pa, pb)):
            assert np.array_equal(x, y), f"day {view.day}: plan[{i}]"
    assert seen >= 3, f"only {seen} of the six boards forecast anything"


# ------------------------------------------------------- backend agreement

def test_numpy_matches_jax_with_a_trained_block():
    import jax
    import jax.numpy as jnp
    from kagg3 import precision  # noqa: F401  pins matmul precision at import

    rng = np.random.default_rng(21)
    theta = PO.pad(rng.normal(0.0, 0.3, PRE_FV_N).astype(np.float32))
    fv = PO.offset("fv")
    theta[fv:fv + PO.N_FWDVAL_FEAT * PO.N_HEAD_HID] = rng.normal(
        0.0, 0.1, PO.N_FWDVAL_FEAT * PO.N_HEAD_HID)
    theta = theta.astype(np.float32)

    jf = jax.jit(lambda th, *fs: PO.forward(jnp, PO.unpack(jnp, th), *fs))
    jt = jnp.asarray(theta)
    p = PO.unpack(np, theta)
    worst = 0.0
    for seed in range(12):
        fs = _inputs(seed)
        a = PO.forward(np, p, *fs)
        b = jf(jt, *[jnp.asarray(f) for f in fs])
        for f, x, y in zip(a._fields, a, b):
            worst = max(worst, float(np.abs(np.asarray(x) - np.asarray(y)).max()))
    assert worst < 1e-5, f"numpy and JAX disagree by {worst}"

    # The feature itself, not just the matmul: exact equality, because every
    # divisor is dyadic and every numerator an exact integer count.
    jv = jax.jit(lambda *o: brain.forward_value(jnp, brain.PolicyObs(*o)))
    for view in BOARDS:
        o = _obs_of(view, opp_tiles=[_plant(spec.I_STRAWBERRY, 0, 2)] * 9)
        a = _fv(o)
        b = np.asarray(jv(*[None if v is None else jnp.asarray(v) for v in o]))
        assert np.array_equal(a, b), f"day {view.day}: {a} vs {b}"


def test_the_decision_agrees_across_backends_with_a_trained_block():
    """The block reaching a decision -- the integer cliffs are what this is
    for, and every head output it moves is floored to one."""
    import jax
    import jax.numpy as jnp
    from kagg3 import precision  # noqa: F401

    rng = np.random.default_rng(31)
    theta = PO.pad(np.load("artifacts/theta.npy").astype(np.float32))
    fv = PO.offset("fv")
    theta[fv:fv + PO.N_FWDVAL_FEAT * PO.N_HEAD_HID] = rng.normal(
        0.0, 0.05, PO.N_FWDVAL_FEAT * PO.N_HEAD_HID).astype(np.float32)
    theta = theta.astype(np.float32)

    jd = jax.jit(lambda th, *o: brain.decide(jnp, th, brain.PolicyObs(*o)))
    jt = jnp.asarray(theta)
    bad = []
    for view in BOARDS:
        o = _obs_of(view, opp_tiles=[_plant(spec.I_MELON, 0)] * 12)
        a = brain.decide(np, theta, o)
        b = jd(jt, *[None if v is None else jnp.asarray(v) for v in o])
        for f, x, y in zip(a._fields, a, b):
            if not np.array_equal(np.asarray(x), np.asarray(y)):
                bad.append(f"day {view.day}: {f} numpy={np.asarray(x)} jax={np.asarray(y)}")
    assert not bad, "\n".join(bad[:10])


def test_the_macro_is_unmoved_by_a_zero_block_on_every_board():
    """The `Macro`'s own fields are what the planner reads; a zero `fv` must
    leave every one of them where the 6,405 layout put it, on all six boards --
    and this one is a *random* theta rather than the champion, so the claim
    does not rest on one point of the parameter space."""
    rng = np.random.default_rng(7)
    old = rng.normal(0.0, 0.05, PRE_FV_N).astype(np.float32)
    new = PO.pad(old)
    for view in BOARDS:
        obs = _obs_of(view)
        a, b = brain.decide(np, old, obs), brain.decide(np, new, obs)
        for f, x, y in zip(a._fields, a, b):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"{view.day}: {f}"
