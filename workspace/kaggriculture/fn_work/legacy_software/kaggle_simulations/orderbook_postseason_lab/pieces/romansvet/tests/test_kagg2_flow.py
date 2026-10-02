"""The exogenous kagg2 market flow: the table, the injection, and the promise
that a run without `--kagg2-flow` is the run that came before it.

The rung exists because `kagg2_proxy` reproduces kagg2's opening and not its
supply mix, and the supply mix is what sets the quotes -- see
`kagg3.es.kagg2_flow`'s module docstring for the measurement and the numbers.
What is asserted here is in four parts:

* the **table** is the measurement (shape, dtype, and every per-product season
  total against `~/scratch_price/price_sum.txt`'s 64-game means);
* **off is off** -- `rollout.episode(flow=None)` and `rollout.episode(flow=
  FLOW_OFF)` agree to the coin on real thetas, so the flag is inert in both the
  structural sense (no flow code in the program) and the arithmetic one;
* **on is on** -- the table's units reach the market inventory, the flow seat's
  own SELL / BUY_PRODUCT orders do not, and the quote path moves;
* the **randomisation** scales and shifts, and does so exactly (int32 all the
  way down, so there is one right answer rather than a tolerance).

`apply_flow` is written against the `xp` protocol and off `.at[]`, so the last
test runs it under plain numpy and under `jax.numpy` and demands the same
integers out of both.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.es import archetypes as AR
from kagg3.es import kagg2_flow as K2F
from kagg3.es.train import NO_BEST
from kagg3.sim import eod, market, rollout
from kagg3.sim.state import Tables, build_tables, initial_state

#: The 64-game means the table is rounded from (`price_sum.txt` section 1, and
#: `netprod.txt` for the BUY_PRODUCT split). Rounding 30 daily means to int32
#: can move a season total by at most half a unit a day, and in practice moves
#: none of these by more than 1.3.
MEASURED_SELL = {"WHEAT": 658.2, "CARROT": 12.4, "TOMATO": 0.0,
                 "STRAWBERRY": 245.2, "MELON": 119.8, "EGG": 0.0,
                 "MILK": 255.7, "WOOL": 154.9, "FERTILIZER": 253.6}
MEASURED_BUY = {"WHEAT": 595.1}


def _tables():
    return build_tables(jnp)


def _words(seed):
    return jnp.asarray(np.stack([eod.host_stream(int(seed), d)
                                 for d in range(spec.N_DAYS)]))


def _thresholds():
    hi, lo = eod.weed_threshold()
    return jnp.int32(hi), jnp.int32(lo)


def _theta(name):
    return jnp.asarray(AR.archetype_theta(**AR.named(name)))


# Episode-level tests go through `jax.jit`, not eager dispatch. Not for speed
# (though it is ~50x): an un-jitted `rollout.episode` dispatches every primitive
# inside a 30-day x 24-turn scan one at a time, each one its own XLA compile and
# its own write to the persistent compilation cache, and on this box that walk
# reliably segfaults the CPU backend inside `backend_compile_and_load` a few
# hundred thousand compiles in. One program per call is also what `es.train`
# actually runs, so the thing under test is the thing that ships.
@jax.jit
def _episode(tables, thetas, words, hi, lo):
    return rollout.episode(tables, thetas, words, hi, lo)


@jax.jit
def _episode_flow(tables, thetas, words, hi, lo, flow):
    return rollout.episode(tables, thetas, words, hi, lo, None, None, flow)


# ---------------------------------------------------------------- the table

def test_table_shape_and_dtype():
    for tab in (K2F.KAGG2_FLOW, K2F.KAGG2_BUY):
        assert tab.shape == (spec.N_DAYS, spec.N_PRODUCTS)
        assert tab.dtype == np.int32
        assert (tab >= 0).all()


def test_season_totals_are_the_measurement():
    """Each product's rounded season total is the 64-game mean it came from."""
    for i, name in enumerate(spec.PRODUCTS):
        got = int(K2F.KAGG2_FLOW[:, i].sum())
        want = MEASURED_SELL[name]
        assert abs(got - want) <= 1.5, f"{name}: table {got} vs measured {want}"
        got_b = int(K2F.KAGG2_BUY[:, i].sum())
        assert abs(got_b - MEASURED_BUY.get(name, 0.0)) <= 1.5, name
    assert K2F.SELL_TOTALS == tuple(int(x) for x in K2F.KAGG2_FLOW.sum(0))
    assert K2F.BUY_TOTALS == tuple(int(x) for x in K2F.KAGG2_BUY.sum(0))


def test_the_mix_is_kagg2s_and_not_the_proxys():
    """The three facts about kagg2 the proxy rung gets wrong."""
    ix = spec.ITEM_IX
    # It keeps no geese and grows no tomatoes -- the proxy sells 92 eggs a game.
    assert K2F.KAGG2_FLOW[:, ix["EGG"]].sum() == 0
    assert K2F.KAGG2_FLOW[:, ix["TOMATO"]].sum() == 0
    # It is a net wheat *seller* that churns: the proxy is a net buyer of 290.
    net = int(K2F.KAGG2_FLOW[:, ix["WHEAT"]].sum() - K2F.KAGG2_BUY[:, ix["WHEAT"]].sum())
    assert net > 0
    assert K2F.KAGG2_BUY[:, ix["WHEAT"]].sum() > 500
    # Wheat is the only thing it buys off the market.
    for i, name in enumerate(spec.PRODUCTS):
        if name != "WHEAT":
            assert K2F.KAGG2_BUY[:, i].sum() == 0, name
    # The melon race is a two-day dump that opens on day 10.
    melon = K2F.KAGG2_FLOW[:, ix["MELON"]]
    assert melon[:10].sum() == 0
    assert melon[10] >= 55
    assert int(melon.sum()) == 120


def test_walk_is_long_enough_for_the_busiest_day():
    """`FLOW_K` has to cover the table times the trainer's scale cap."""
    assert K2F.MAX_DAY_UNITS == int(max(K2F.KAGG2_FLOW.max(), K2F.KAGG2_BUY.max()))
    assert market.FLOW_K > 2.0 * K2F.MAX_DAY_UNITS - 1


# ---------------------------------------------------------------- off is off

@pytest.mark.parametrize("name", ["mixed_ranch", None])
@pytest.mark.parametrize("seed", [11, 4242, 20260827, 777])
def test_zero_diff_when_off(name, seed):
    """`flow=FLOW_OFF` reproduces `flow=None` to the coin, ledger included.

    Two thetas and two seeds: a real archetype (`mixed_ranch`, which trades on
    every day of the season) and the zero theta, which is the pinned baseline
    every other ladder test is written against.
    """
    tables, (hi, lo) = _tables(), _thresholds()
    n = int(AR.archetype_theta(**AR.named("mixed_ranch")).shape[0])
    th = (jnp.stack([_theta(name)] * 2) if name
          else jnp.zeros((2, n), jnp.float32))
    words = _words(seed)

    base_money, base_daily, base_st = _episode(tables, th, words, hi, lo)
    off = jnp.asarray(market.FLOW_OFF, jnp.int32)
    money, daily, st = _episode_flow(tables, th, words, hi, lo, off)

    assert np.array_equal(np.asarray(base_money), np.asarray(money))
    assert np.array_equal(np.asarray(base_daily), np.asarray(daily))
    # The whole terminal state, not just the money: a flow that moved a single
    # unit of market inventory or a single coin of the opponent's would show up
    # in one of these leaves even when the two final scores happened to agree.
    for a, b in zip(base_st, st):
        assert np.array_equal(np.asarray(a), np.asarray(b))


def test_off_control_word_is_the_documented_one():
    seat, scale, shift = market.FLOW_OFF
    assert seat < 0 and scale == 1000 and shift == 0


# ---------------------------------------------------------------- on is on

def _blank_state(inv=None, money=20_000, shed=0):
    st = initial_state(jnp)
    st = st._replace(money=jnp.int32([money, money]))
    if inv is not None:
        st = st._replace(mkt_inv=jnp.asarray(inv, jnp.int32))
    if shed:
        st = st._replace(shed=jnp.full_like(st.shed, shed))
    return st


def test_flow_moves_the_market_by_the_table():
    """A day of melon: 60 units in, inventory up 60, seat paid the walk."""
    tables = _tables()
    st = _blank_state()
    day = jnp.int32(10)
    out = market.apply_flow(jnp, tables, st, day,
                            jnp.asarray([1, 1000, 0], jnp.int32))
    d_inv = np.asarray(out.mkt_inv) - np.asarray(st.mkt_inv)
    want = np.asarray(K2F.KAGG2_FLOW[10], np.int64) - np.asarray(K2F.KAGG2_BUY[10], np.int64)
    # Every unit here prices well above the $1 floor, so a sell advances the
    # inventory one for one and the net move is sells minus buys.
    assert np.array_equal(d_inv, want)
    money = np.asarray(out.money) - np.asarray(st.money)
    assert money[0] == 0, "the flow must not touch the other seat"
    assert money[1] > 0
    # 60 melons off a fresh 10,000 inventory is worth six figures of the melon
    # curve; the exact number is the walk's, and the walk is `_solo`'s.
    assert money[1] > 10_000


def test_flow_picks_the_seat_it_is_given():
    tables = _tables()
    st = _blank_state()
    day = jnp.int32(10)
    a = market.apply_flow(jnp, tables, st, day, jnp.asarray([0, 1000, 0], jnp.int32))
    b = market.apply_flow(jnp, tables, st, day, jnp.asarray([1, 1000, 0], jnp.int32))
    assert np.asarray(a.money)[0] == np.asarray(b.money)[1]
    assert np.asarray(a.money)[1] == 20_000
    assert np.asarray(b.money)[0] == 20_000
    assert np.array_equal(np.asarray(a.mkt_inv), np.asarray(b.mkt_inv))


def test_flow_drains_the_seats_shed_but_never_past_empty():
    tables = _tables()
    day = jnp.int32(10)
    on = jnp.asarray([1, 1000, 0], jnp.int32)
    empty = market.apply_flow(jnp, tables, _blank_state(), day, on)
    assert (np.asarray(empty.shed)[1] >= 0).all()
    assert np.asarray(empty.shed)[1, spec.I_MELON] == 0

    stocked = _blank_state(shed=5)
    out = market.apply_flow(jnp, tables, stocked, day, on)
    shed = np.asarray(out.shed)
    # Day 10 sells 60 melon and 21 wheat and buys 33 wheat; the melon stock is
    # exhausted, the wheat one is exhausted and then partly refilled.
    assert shed[1, spec.I_MELON] == 0
    assert (shed[1] >= 0).all()
    assert shed[0, spec.I_MELON] == 5, "the other seat's shed is untouched"


def test_a_day_the_table_is_silent_on_moves_nothing():
    tables = _tables()
    st = _blank_state()
    day = jnp.int32(0)
    # Day 0: three wheat sold, eight bought, nothing else.
    out = market.apply_flow(jnp, tables, st, day,
                            jnp.asarray([1, 1000, 0], jnp.int32))
    d = np.asarray(out.mkt_inv) - np.asarray(st.mkt_inv)
    assert d[spec.I_MELON] == 0 and d[spec.I_MILK] == 0
    assert d[spec.I_WHEAT] == 3 - 8


def test_mask_blanks_only_the_inventory_orders_of_the_flow_seat():
    mop = np.full((2, spec.TURNS_PER_DAY, spec.MAX_MARKET_ORDERS), O.MO_NONE, np.int32)
    mop[:, 3, 0] = O.MO_SELL
    mop[:, 3, 1] = O.MO_BUY_PRODUCT
    mop[:, 0, 0] = O.MO_HIRE
    mop[:, 0, 1] = O.MO_BUY_SEED
    mop[:, 0, 2] = O.MO_BUY_ANIMAL
    mop[:, 10, 9] = O.MO_BUY_LAND
    out = np.asarray(market.mask_flow_seat(jnp, jnp.asarray(mop),
                                           jnp.asarray([1, 1000, 0], jnp.int32)))
    assert np.array_equal(out[0], mop[0]), "seat 0 is untouched"
    assert out[1, 3, 0] == O.MO_NONE and out[1, 3, 1] == O.MO_NONE
    for turn, slot in ((0, 0), (0, 1), (0, 2), (10, 9)):
        assert out[1, turn, slot] == mop[1, turn, slot], (turn, slot)


def test_an_episode_with_the_flow_on_is_a_different_game():
    """End to end: the rung's own sells vanish and the table's arrive."""
    tables, (hi, lo) = _tables(), _thresholds()
    th = jnp.stack([_theta("mixed_ranch"), _theta(AR.PROXY_NAME)])
    words = _words(7)
    off_money, _, off_st = _episode(tables, th, words, hi, lo)
    on = jnp.asarray([1, 1000, 0], jnp.int32)
    on_money, _, on_st = _episode_flow(tables, th, words, hi, lo, on)

    off_inv, on_inv = np.asarray(off_st.mkt_inv), np.asarray(on_st.mkt_inv)
    off_cash, on_cash = np.asarray(off_money), np.asarray(on_money)
    # A different game: the shelves moved and so did both purses. Seat 1 is the
    # flow seat, so its own score is bound to move; seat 0 moving too is the
    # point of the rung -- the opponent is playing a different market.
    assert not np.array_equal(off_inv, on_inv)
    assert (off_cash != on_cash).all()
    # *Which* shelves end up fuller is not the table's decision alone. Seat 0
    # is a live opponent that re-plans against the quotes the flow moves, and
    # the archetype here is a rancher: cheapen milk and it answers by milking
    # more, so the ~178 units of milk the table injects come back out of the
    # season as a lower end-of-season milk inventory, not a higher one. Assert
    # instead on the two crops a ranch does not grow: strawberry, which the
    # table injects 245 u of and buys none of, and wheat, which it trades more
    # of than anything else. Both shelves end fuller with the flow on; milk
    # and wool are the ones whose sign the opponent gets to choose.
    for it in (spec.I_STRAWBERRY, spec.I_WHEAT):
        assert on_inv[it] > off_inv[it], spec.PRODUCTS[it]
    # The rung is still on the board -- masking its market orders must not
    # switch off its farm.
    assert (np.asarray(on_st.kind)[1] == spec.KIND_PLANT).sum() > 0


# ------------------------------------------------------------ randomisation

@pytest.mark.parametrize("scale,factor", [(500, 0.5), (1000, 1.0), (1500, 1.5)])
def test_scale_is_exact_thousandths(scale, factor):
    tables = _tables()
    st = _blank_state()
    day = jnp.int32(10)
    out = market.apply_flow(jnp, tables, st, day,
                            jnp.asarray([1, scale, 0], jnp.int32))
    d = np.asarray(out.mkt_inv) - np.asarray(st.mkt_inv)
    sell = (np.asarray(K2F.KAGG2_FLOW[10], np.int64) * scale + 500) // 1000
    buy = (np.asarray(K2F.KAGG2_BUY[10], np.int64) * scale + 500) // 1000
    assert np.array_equal(d, sell - buy)
    assert d[spec.I_MELON] == int(round(60 * factor))


def test_shift_slides_the_calendar():
    tables = _tables()
    st = _blank_state()
    on = lambda day, shift: np.asarray(market.apply_flow(
        jnp, tables, st, jnp.int32(day),
        jnp.asarray([1, 1000, shift], jnp.int32)).mkt_inv) - np.asarray(st.mkt_inv)
    assert np.array_equal(on(12, 2), on(10, 0))
    assert np.array_equal(on(8, -2), on(10, 0))


def test_days_shifted_off_the_season_are_silent():
    tables = _tables()
    st = _blank_state()
    for day, shift in ((0, 2), (spec.N_DAYS - 1, -2)):
        out = market.apply_flow(jnp, tables, st, jnp.int32(day),
                                jnp.asarray([1, 1000, shift], jnp.int32))
        assert np.array_equal(np.asarray(out.mkt_inv), np.asarray(st.mkt_inv))
        assert np.array_equal(np.asarray(out.money), np.asarray(st.money))


def test_a_negative_seat_is_off_whatever_the_rest_of_the_word_says():
    tables = _tables()
    st = _blank_state()
    out = market.apply_flow(jnp, tables, st, jnp.int32(10),
                            jnp.asarray([-1, 1500, 2], jnp.int32))
    assert np.array_equal(np.asarray(out.mkt_inv), np.asarray(st.mkt_inv))
    assert np.array_equal(np.asarray(out.money), np.asarray(st.money))
    assert np.array_equal(np.asarray(out.shed), np.asarray(st.shed))


# ---------------------------------------------------------------- backends

@pytest.mark.parametrize("day,word", [(10, (1, 1000, 0)), (23, (0, 1500, -2)),
                                      (5, (1, 500, 1))])
def test_numpy_and_jax_agree(day, word):
    """`apply_flow` is integer arithmetic, so the two backends are equal, not
    close. Nothing on this path is a float, and that is the point: the flow
    moves market inventory, and market inventory decides a quote by table
    lookup, so a one-unit disagreement is a different price all season."""
    jst = _blank_state(shed=4)
    jout = market.apply_flow(jnp, _tables(), jst, jnp.int32(day),
                             jnp.asarray(word, jnp.int32))

    nst = jst.__class__(*[np.asarray(x) for x in jst])
    ntab = Tables(price=np.asarray(build_tables(jnp).price))
    nout = market.apply_flow(np, ntab, nst, np.int32(day),
                             np.asarray(word, np.int32))

    for name, a, b in zip(jst._fields, jout, nout):
        assert np.array_equal(np.asarray(a), np.asarray(b)), name


# ------------------------------------------------------------ the wiring

def test_flow_control_words():
    from kagg3.es.train import flow_control
    w = flow_control([-1, 0, 1], [1000, 1200, 800], [0, 2, -1])
    assert w.dtype == np.int32 and w.shape == (3, 3)
    # An off episode is forced back to FLOW_OFF, so two off batches are equal
    # whatever randomisation was drawn for them.
    assert tuple(w[0]) == market.FLOW_OFF
    assert tuple(w[1]) == (0, 1200, 2)
    assert tuple(w[2]) == (1, 800, -1)
    assert tuple(flow_control([1])[0]) == (1, 1000, 0), "centre by default"


def test_the_flag_adds_a_rung_and_the_rung_carries_the_flow():
    """`--kagg2-flow` is one extra slot, past --n-archetypes, named for
    `--rung-weight`, at no handicap -- and the trainer points the flow at the
    opponent's physical seat, not ours."""
    from kagg3.es.train import Config, Trainer

    cfg = Config(pop=2, episodes=4, chunk=4, abs_pairs=2, n_archetypes=2,
                 holdout_rungs=False, kagg2_flow=True, kagg2_flow_jitter=0,
                 kagg2_flow_scale=(1.0, 1.0))
    tr = Trainer(cfg, seed=0)
    assert tr.archetype_names[-1] == K2F.RUNG_NAME
    assert len(tr.archetypes) == cfg.n_archetypes + 1
    assert tr.flow_rung == len(tr.archetypes) - 1
    assert tuple(tr.arch_handicap[tr.flow_rung]) == AR.NO_HANDICAP
    assert tr.archetype_coins[tr.flow_rung] >= AR.MIN_COINS

    n_pairs = 2
    idx = np.full(n_pairs, len(tr.pool) + tr.flow_rung)
    flow = np.asarray(tr.episode_flow(n_pairs, idx))
    assert flow.shape == (2 * n_pairs, 3)
    # Episode e faces the rung at physical player `1 - (e % 2)`.
    assert list(flow[:, 0]) == [1, 0, 1, 0]
    # A pair's two seats share one draw; at this config that draw is the centre.
    assert (flow[:, 1] == 1000).all() and (flow[:, 2] == 0).all()

    # A pair facing the self-play pool carries no flow at all.
    off = np.asarray(tr.episode_flow(n_pairs, np.zeros(n_pairs, int)))
    assert (off == np.asarray(market.FLOW_OFF, np.int32)).all()


def test_no_flag_is_no_rung_and_no_flow_program():
    from kagg3.es.train import Config, Trainer
    tr = Trainer(Config(pop=2, episodes=4, chunk=4, abs_pairs=2, n_archetypes=2,
                        holdout_rungs=False), seed=0)
    assert K2F.RUNG_NAME not in tr.archetype_names
    assert tr.flow_rung == -1
    assert len(tr.archetypes) == 2
    # `None` is what selects `make_evaluator`'s flow-free program.
    assert tr.flow_words(np.zeros(4, bool), np.zeros(4, np.int32)) is None
    assert tr.episode_flow(2, np.zeros(2, int)) is None


def test_rung_names_matches_the_ladder_the_run_will_build():
    import train as T
    from kagg3.es.train import Config, Trainer
    for flag in (False, True):
        cfg = Config(pop=2, episodes=4, chunk=4, abs_pairs=2, n_archetypes=2,
                     holdout_rungs=False, kagg2_flow=flag,
                     kagg2_flow_jitter=0, kagg2_flow_scale=(1.0, 1.0))
        assert T.rung_names(2, flag) == Trainer(cfg, seed=0).archetype_names


def test_vmap_over_a_per_episode_control_word():
    """The flag is per episode and must not be a Python branch."""
    tables, (hi, lo) = _tables(), _thresholds()
    th = jnp.stack([_theta("mixed_ranch"), _theta(AR.PROXY_NAME)])
    words = jnp.stack([_words(3), _words(3), _words(3)])
    flow = jnp.asarray([[-1, 1000, 0], [1, 1000, 0], [1, 500, 2]], jnp.int32)

    run = jax.jit(jax.vmap(
        lambda w, f: rollout.episode(tables, th, w, hi, lo, None, None, f)[0],
        in_axes=(0, 0)))
    money = np.asarray(run(words, flow))
    solo = np.asarray(_episode(tables, th, words[0], hi, lo)[0])
    # Row 0 is off, so it is the plain episode; the other two are not, and are
    # not each other either.
    assert np.array_equal(money[0], solo)
    assert not np.array_equal(money[0], money[1])
    assert not np.array_equal(money[1], money[2])


# ------------------------------------------------------------------ resuming

def test_resume_into_the_flow_rung_extends_the_ladder(tmp_path):
    """`--kagg2-flow --resume` on a pre-flow checkpoint grows the ladder by one.

    This is how the flow run actually starts: every long run on this machine
    predates the rung, and throwing away a 12-rung pool and a few thousand
    generations of theta to pick up one opponent would be an absurd price. So
    the flag extends the restored ladder instead of being refused by it.

    Three halves to the assertion, and they are the whole contract. The **ES
    state** -- theta, the Adam moments, the step counter, sigma and its restart
    count, the generation, the cumulative elapsed and the host RNG -- must come
    back bit for bit, because none of it is indexed by rung. The **per-rung
    bookkeeping** -- weights, openings, liveness coins -- must be rebuilt for
    all ten in the cold-start way, because a rung appended here has to be
    indistinguishable from the same rung on a fresh ladder. And `best_abs`,
    which is neither: it is a coin count *against* the nine-rung ladder, so the
    tenth rung retires it. Kept, it is a bar the ten-rung run can never clear
    and `best_abs.npy` is never written again.
    """
    import train as T
    from kagg3.es.train import Config, Trainer

    base = dict(pop=2, episodes=4, chunk=4, abs_pairs=2, n_archetypes=9,
                holdout_rungs=False, sigma=0.037)
    old = Trainer(Config(**base), seed=3)
    assert len(old.archetypes) == 9
    assert K2F.RUNG_NAME not in old.archetype_names
    assert old.flow_rung == -1

    # Move every piece of ES state off its default, so "preserved" has content.
    old.theta = old.theta + 0.25
    old.m = old.m + 0.5
    old.t = 41
    # One *stepping* restart: both counters, since a resume rebuilds sigma from
    # the step count and the two only part at `--stall-sigma-mult 1.0`.
    old.sigma_restarts = old.sigma_steps = 1
    old.sigma = base["sigma"] * 2.0
    old.best_abs = 123_456.0
    old.rng.integers(0, 2 ** 31 - 1, 17)
    run_dir = str(tmp_path)
    T.save_state(run_dir, old, 1234, elapsed=987.5)

    new = Trainer(Config(kagg2_flow=True, kagg2_flow_jitter=0,
                         kagg2_flow_scale=(1.0, 1.0), **base), seed=0)
    gen, how, elapsed = T.load_resume(new, run_dir)

    # --- the ladder grew, at the end, and nothing else about it moved
    assert new.archetype_names == list(old.archetype_names) + [K2F.RUNG_NAME]
    assert len(new.archetypes) == 10
    assert new.flow_rung == 9
    for a, b in zip(old.archetypes, new.archetypes):
        assert np.array_equal(np.asarray(a), np.asarray(b))

    # --- per-rung bookkeeping rebuilt for all ten, cold-start style
    assert len(new.rung_weights) == 10 and new.rung_weights[-1] == 1.0
    assert new.arch_handicap.shape == (10, 2)
    assert tuple(new.arch_handicap[-1]) == AR.NO_HANDICAP
    assert len(new.archetype_coins) == 10
    assert new.archetype_coins[-1] >= AR.MIN_COINS

    # --- ES state is exactly what was checkpointed
    assert (gen, elapsed) == (1234, 987.5)
    assert np.array_equal(np.asarray(new.theta), np.asarray(old.theta))
    assert np.array_equal(np.asarray(new.m), np.asarray(old.m))
    assert np.array_equal(np.asarray(new.v), np.asarray(old.v))
    assert new.t == 41
    assert new.sigma_restarts == 1
    assert new.sigma == pytest.approx(base["sigma"] * 2.0)
    assert len(new.pool) == len(old.pool)

    # --- but the yardstick moved, so the number measured on the old one goes
    assert new.best_abs == NO_BEST
    assert np.array_equal(np.asarray(new.best_abs_theta), np.asarray(new.theta))
    assert "kagg2_flow" in new.best_reset_note and "123,456" in new.best_reset_note

    # --- the host RNG resumed mid-stream, so the two draw the same next seeds.
    # Before `episode_flow` below, which draws the rung's scale and shift from
    # this very generator -- the resumed run continues one stream, and anything
    # that reads it moves it.
    assert list(new.rng.integers(0, 2 ** 31 - 1, 5)) == \
        list(old.rng.integers(0, 2 ** 31 - 1, 5))

    # --- and the ladder it grew really does carry the flow
    idx = np.full(2, len(new.pool) + new.flow_rung)
    assert list(np.asarray(new.episode_flow(2, idx))[:, 0]) == [1, 0, 1, 0]


def test_resume_without_the_flag_leaves_the_ladder_alone(tmp_path):
    """The extension is the flag's doing, not the resume's."""
    import train as T
    from kagg3.es.train import Config, Trainer

    base = dict(pop=2, episodes=4, chunk=4, abs_pairs=2, n_archetypes=2,
                holdout_rungs=False)
    old = Trainer(Config(**base), seed=1)
    T.save_state(str(tmp_path), old, 7)
    new = Trainer(Config(**base), seed=2)
    T.load_resume(new, str(tmp_path))
    assert new.archetype_names == list(old.archetype_names)
    assert new.flow_rung == -1


# ------------------------------------------- where the gradient's family sits

def _flow_trainer(seed=7, **cfg):
    """A `Trainer` carrying only what `episode_flow` reads.

    `__new__` rather than a real construction: what is under test is which
    numbers come off `self.rng` and where they land in the control word, and
    building the ladder would spend a minute of archetype probing to find out.
    """
    from kagg3.es.train import Config, Trainer

    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**dict({"kagg2_flow": True}, **cfg))
    tr.pool = []
    tr.flow_rung = 0
    tr.rng = np.random.default_rng(seed)
    return tr


def test_an_unset_shift_range_is_the_jitter_draw_it_replaces():
    """Zero-diff, down to the generator state.

    `--kagg2-flow-shift` reaches into the one draw the whole run's
    common-random-numbers scheme is threaded through, so "unset behaves the
    same" has to mean the same *stream*, not merely the same distribution: one
    extra or differently-bounded draw here re-seeds every episode after it.
    """
    from kagg3.es.train import Config

    n, j = 5, 3
    tr = _flow_trainer(kagg2_flow_jitter=j)
    got = np.asarray(tr.episode_flow(n, np.zeros(n, int)))

    # The arithmetic the jitter path did, replayed off an untouched generator.
    ref = np.random.default_rng(7)
    lo, hi = Config().kagg2_flow_scale
    scale = np.rint(ref.uniform(lo, hi, n) * 1000).astype(np.int32)
    shift = ref.integers(-j, j + 1, n).astype(np.int32)
    assert list(got[:, 1]) == list(np.repeat(scale, 2))
    assert list(got[:, 2]) == list(np.repeat(shift, 2))
    # Same number of draws, same bounds: the stream is where it always was.
    assert tr.rng.bit_generator.state == ref.bit_generator.state

    # And the jitter written out as a range is the jitter: the flag is a
    # recentring, not a second randomisation.
    same = _flow_trainer(kagg2_flow_shift=(-j, j))
    assert np.array_equal(np.asarray(same.episode_flow(n, np.zeros(n, int))),
                          got)


def test_a_shift_range_recentres_the_gradients_flow_family():
    """The calibration sweep puts the real matchup near +2 days, which the
    symmetric jitter cannot reach the middle of: `+-2` draws 0 on average and
    never draws 3 or 4 at all."""
    n = 64
    up = np.asarray(_flow_trainer(kagg2_flow_shift=(0, 4))
                    .episode_flow(n, np.zeros(n, int)))[:, 2]
    assert up.min() >= 0 and up.max() <= 4
    # Inclusive on both ends, and every level in between is reachable.
    assert set(int(x) for x in np.unique(up)) == {0, 1, 2, 3, 4}
    # A pair's two seats still share one draw -- the pairing is what cancels
    # the variance the margin is read through.
    assert (up[0::2] == up[1::2]).all()

    # The default jitter cannot produce the top of that range at all, which is
    # the whole reason the flag exists.
    plain = np.asarray(_flow_trainer().episode_flow(n, np.zeros(n, int)))[:, 2]
    assert plain.max() <= 2 and plain.min() >= -2

    # A degenerate range pins the level, which is the ablation "train at +2".
    pinned = np.asarray(_flow_trainer(kagg2_flow_shift=(2, 2))
                        .episode_flow(n, np.zeros(n, int)))[:, 2]
    assert (pinned == 2).all()


def test_the_shift_range_and_the_jitter_are_mutually_exclusive():
    """Two ways of stating the same draw: an operator who passed both stated a
    centre and a width that disagree about where the centre is. Refused rather
    than resolved by precedence, and refused without the rung as every other
    flow shaping flag is."""
    import subprocess

    def run(*flags):
        return subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "train.py"),
             "--run", "_shift_flag_check", *flags],
            capture_output=True, text=True,
            env=dict(os.environ, JAX_PLATFORMS="cpu"))

    both = run("--kagg2-flow", "--kagg2-flow-shift", "0:4",
               "--kagg2-flow-jitter", "3")
    assert both.returncode != 0
    assert "--kagg2-flow-shift 0:4 with --kagg2-flow-jitter 3" in both.stderr

    no_rung = run("--kagg2-flow-shift", "0:4")
    assert no_rung.returncode != 0
    assert "--kagg2-flow-shift without --kagg2-flow" in no_rung.stderr

    bad = run("--kagg2-flow", "--kagg2-flow-shift", "4:0")
    assert bad.returncode != 0 and "need LO <= HI" in bad.stderr

    # The refusals happen before anything is written, so a rejected invocation
    # leaves no run directory behind.
    assert not os.path.exists(os.path.join(ROOT, "artifacts", "_shift_flag_check"))
