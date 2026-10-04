"""`grow`: the production half of a tape rung, and the clamp that needed it.

`--tape-flow-backed` says the flow seat may only sell what its shed holds. On
its own that was measured and unusable: the rung's board is a wheat clone and
the tapes sell strawberry, milk, wool and fertilizer, so the clamp deleted the
opponent instead of shrinking it (`sim.market.apply_flow`'s docstring has the
numbers). `grow` is the missing half -- what the recorded seat put into its
shed by every route other than the market -- credited to that shed before the
day's sells are clamped.

Four things are asserted here:

* the **identity** the measurement is defined by, on a replay's own shed
  observations::

      grow[d] = shed[d + 1] - shed[d] + sell[d] - buy[d]

  including the signed days (feeding wheat costs shed stock) and the fallback
  a replay with no shed observation takes;
* the **credit**: with `grow` the flow seat sells what it produced and is paid
  for it, where the same table with a zero `grow` row banks nothing;
* the **pin**: `backed=False` is byte-identical to the code before `grow`
  existed -- the digests below were taken on `61a3e04`, the commit this work
  started from, and `flow_rows` still returns a pair;
* the **refusal**: `--tape-flow-backed` against a table with no `grow` row
  names the file rather than training for a day against a rung that banks
  four figures.
"""
from __future__ import annotations

import json
import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import jax.numpy as jnp
import numpy as np
import pytest

import make_tape_rung as MTR
from kagg3 import spec
from kagg3.es import tape_flow as TPF
from kagg3.sim import eod, market, rollout
from kagg3.sim.state import build_tables, initial_state

SHIPPED = os.path.join(ROOT, "artifacts", "tape_games")
P = spec.N_PRODUCTS
D = spec.N_DAYS


@pytest.fixture(autouse=True)
def _pristine_flow_tables():
    """Registration mutates module state; hand it back exactly as found.

    `tests/test_kaggle_flow.py` asserts `FLOW_K` is *equal* to the size the two
    measured means alone imply, so a test that grew the stack and walked away
    would fail that one from a different file.
    """
    saved = (market._FLOW_SELL, market._FLOW_BUY, market._FLOW_GROW,
             market.FLOW_K, market.MAX_FLOW_DAY_UNITS)
    yield
    (market._FLOW_SELL, market._FLOW_BUY, market._FLOW_GROW,
     market.FLOW_K, market.MAX_FLOW_DAY_UNITS) = saved


# ------------------------------------------------------------------- identity

def _steps(sheds, seat=1, with_private=True):
    """A replay `steps` list carrying nothing but one seat's shed.

    `grow_table` reads the private shed at the day boundaries and nothing
    else, so this is the whole input to the identity -- no 30 MB of board.
    `sheds` is [n_turns] of per-product lists.
    """
    out = []
    for row in sheds:
        priv = {"shed": {p: int(v) for p, v in zip(spec.PRODUCTS, row)}}
        seats = []
        for s in (0, 1):
            obs = {"private": priv if (s == seat and with_private) else {}}
            seats.append({"observation": obs, "action": {}})
        out.append(seats)
    return out


def _walk(grow, sell, buy, start=None):
    """The shed trajectory the identity implies, sampled at day boundaries."""
    shed = np.zeros(P, np.int64) if start is None else np.asarray(start, np.int64)
    rows = [shed.copy()]
    for d in range(D):
        shed = shed + grow[d] - sell[d] + buy[d]
        rows.append(shed.copy())
    return np.stack(rows)


def _fixture(seed=3):
    """A season of (grow, sell, buy) that never asks the shed for what it has
    not got, with a signed `grow` day in it (wheat fed to the animals)."""
    rng = np.random.default_rng(seed)
    grow = np.zeros((D, P), np.int64)
    sell = np.zeros((D, P), np.int64)
    buy = np.zeros((D, P), np.int64)
    for d in range(D):
        grow[d, spec.I_WHEAT] = int(rng.integers(4, 20))
        grow[d, spec.I_MILK] = int(rng.integers(0, 6))
        if d > 3:
            sell[d, spec.I_WHEAT] = int(rng.integers(0, 4))
            sell[d, spec.I_MILK] = int(rng.integers(0, 3))
            buy[d, spec.I_WHEAT] = int(rng.integers(0, 3))
    # one day that consumed more than it grew: the sign the table has to keep
    grow[17, spec.I_WHEAT] = -6
    return grow, sell, buy


def test_grow_identity_recovers_the_production_from_the_shed():
    """`grow_table` inverts the identity exactly, sign and all."""
    grow, sell, buy = _fixture()
    bounds = _walk(grow, sell, buy)
    # one observation per turn; only indices 24*d are read
    turns = np.repeat(bounds[:-1], spec.TURNS_PER_DAY, axis=0)
    turns = np.concatenate([turns, bounds[-1][None]])
    steps = _steps(turns, seat=1)
    # `_shed_row` at the day boundaries is the whole input to the identity;
    # `grow_table` (next test) is the same arithmetic off a file.
    obs = np.stack([MTR._shed_row(steps[min(spec.TURNS_PER_DAY * d,
                                            len(steps) - 1)], 1)
                    for d in range(D + 1)])
    recovered = obs[1:] - obs[:-1] + sell - buy
    assert np.array_equal(recovered, grow)
    assert recovered[17, spec.I_WHEAT] == -6, "the signed day survives"


def test_grow_table_closes_the_identity_on_a_replay(tmp_path):
    """The real entry point, on a replay file: source, residual and roll."""
    grow, sell, buy = _fixture(seed=11)
    bounds = _walk(grow, sell, buy)
    turns = np.repeat(bounds[:-1], spec.TURNS_PER_DAY, axis=0)
    turns = np.concatenate([turns, bounds[-1][None]])
    path = tmp_path / "replay.json"
    path.write_text(json.dumps({"steps": _steps(turns, seat=0)}))

    got, source, residual = MTR.grow_table(str(path), 0, sell, buy)
    assert source == "shed_delta"
    assert np.array_equal(np.asarray(residual), np.zeros(P, np.int64))
    assert np.array_equal(got, grow.astype(np.int32))
    # and the forward roll lands on the observed boundaries, which is the
    # identity stated the other way round
    assert np.array_equal(_walk(got, sell, buy), bounds)


def test_a_replay_with_no_shed_observation_falls_back_to_the_actions(tmp_path):
    grow, sell, buy = _fixture(seed=5)
    bounds = _walk(grow, sell, buy)
    turns = np.repeat(bounds[:-1], spec.TURNS_PER_DAY, axis=0)
    turns = np.concatenate([turns, bounds[-1][None]])
    steps = _steps(turns, seat=0, with_private=False)
    # the fallback reads the board, which this fixture has none of; what is
    # under test is that the *route* changes rather than a zero shed being
    # read as an empty one.
    for s in steps:
        s[0]["observation"]["farms"] = [{"farmer": [0, 0], "hands": [],
                                         "tiles": [[{}]]}] * 2
    path = tmp_path / "replay.json"
    path.write_text(json.dumps({"steps": steps}))
    got, source, residual = MTR.grow_table(str(path), 0, sell, buy)
    assert source == "actions"
    assert residual is None, "the fallback does not claim the identity"
    assert got.shape == (D, P)


def test_every_shipped_tape_carries_a_grow_row():
    """The rungs an operator will actually name, as fixtures."""
    paths = sorted(p for p in os.listdir(SHIPPED) if p.endswith(".npz"))
    with_grow = [p for p in paths
                 if TPF.load(os.path.join(SHIPPED, p)).grow is not None]
    assert with_grow, "no tape rung has been re-cut"
    for name in with_grow:
        t = TPF.load(os.path.join(SHIPPED, name))
        assert t.grow.shape == (D, P) and t.grow.dtype == np.int32
        assert t.grow_source in ("shed_delta", "actions")
        # a seat cannot end the season owing the shed stock: whatever it sold
        # net of what it bought was produced at some point.
        net = t.grow.sum(0) - t.sell.sum(0) + t.buy.sum(0)
        assert (net >= 0).all(), f"{name}: {net.tolist()}"


# --------------------------------------------------------------- the credit

def _tape_table(sell_units=20, grow_units=20, product=spec.I_WOOL, day=10):
    sell = np.zeros((D, P), np.int32)
    grow = np.zeros((D, P), np.int32)
    sell[day, product] = sell_units
    grow[day, product] = grow_units
    return sell, np.zeros((D, P), np.int32), grow


def _blank(money=20_000):
    st = initial_state(jnp)
    return st._replace(money=jnp.int32([money, money]))


def test_grow_credits_the_shed_and_the_sells_are_paid():
    """The same table, with and without its production row."""
    tables = build_tables(jnp)
    sell, buy, grow = _tape_table()
    dead = market.register_flow_table(sell, buy)                 # no grow
    live = market.register_flow_table(sell, buy, grow)
    assert dead != live, "production is part of a table's identity"

    day = jnp.int32(10)
    st = _blank()
    off = market.apply_flow(jnp, tables, st, day,
                            jnp.asarray([1, 1000, 0, dead], jnp.int32),
                            backed=True)
    on = market.apply_flow(jnp, tables, st, day,
                           jnp.asarray([1, 1000, 0, live], jnp.int32),
                           backed=True)
    # Without `grow` the wheat-clone shed holds no wool: nothing sold, nothing
    # earned, the book never moved. That is the defect the flag had.
    assert np.asarray(off.money)[1] == 20_000
    assert np.asarray(off.mkt_inv)[spec.I_WOOL] == np.asarray(st.mkt_inv)[spec.I_WOOL]
    # With it the seat sells the 20 wool it grew, is paid the sim's walk for
    # them, and the book carries all 20.
    assert np.asarray(on.money)[1] > 20_000
    assert (np.asarray(on.mkt_inv)[spec.I_WOOL]
            == np.asarray(st.mkt_inv)[spec.I_WOOL] + 20)
    # and the credit is consumed by the sale, not banked
    assert np.asarray(on.shed)[1, spec.I_WOOL] == 0
    assert np.asarray(on.money)[0] == 20_000, "the other seat is untouched"


def test_a_short_grow_day_sells_only_what_it_grew():
    tables = build_tables(jnp)
    sell, buy, grow = _tape_table(sell_units=20, grow_units=7)
    tid = market.register_flow_table(sell, buy, grow)
    st = _blank()
    out = market.apply_flow(jnp, tables, st, jnp.int32(10),
                            jnp.asarray([1, 1000, 0, tid], jnp.int32), backed=True)
    assert (np.asarray(out.mkt_inv)[spec.I_WOOL]
            == np.asarray(st.mkt_inv)[spec.I_WOOL] + 7)
    assert np.asarray(out.shed)[1, spec.I_WOOL] == 0


def test_the_credit_takes_the_shed_cap():
    """`SHED_CAPACITY` is the engine's only cap, and the credit takes it."""
    tables = build_tables(jnp)
    sell = np.zeros((D, P), np.int32)
    grow = np.zeros((D, P), np.int32)
    grow[10, spec.I_WOOL] = 250                        # more than a shed holds
    tid = market.register_flow_table(sell, np.zeros((D, P), np.int32), grow)
    out = market.apply_flow(jnp, tables, _blank(), jnp.int32(10),
                            jnp.asarray([1, 1000, 0, tid], jnp.int32), backed=True)
    assert np.asarray(out.shed)[1].sum() == spec.SHED_CAPACITY


def test_a_negative_grow_day_drains_but_never_past_empty():
    tables = build_tables(jnp)
    sell = np.zeros((D, P), np.int32)
    grow = np.zeros((D, P), np.int32)
    grow[10, spec.I_WHEAT] = -40
    tid = market.register_flow_table(sell, np.zeros((D, P), np.int32), grow)
    st = _blank()._replace(shed=jnp.zeros_like(initial_state(jnp).shed)
                           .at[1, spec.I_WHEAT].set(12))
    out = market.apply_flow(jnp, tables, st, jnp.int32(10),
                            jnp.asarray([1, 1000, 0, tid], jnp.int32), backed=True)
    assert np.asarray(out.shed)[1, spec.I_WHEAT] == 0
    assert (np.asarray(out.shed) >= 0).all()


def test_spread_credits_the_days_grow_once_over_its_slices():
    """Proportional per market turn, and the day's total to the unit."""
    tables = build_tables(jnp)
    sell = np.zeros((D, P), np.int32)
    grow = np.zeros((D, P), np.int32)
    grow[10, spec.I_WOOL] = 17                     # deliberately not divisible
    tid = market.register_flow_table(sell, np.zeros((D, P), np.int32), grow)
    flow = jnp.asarray([1, 1000, 0, tid], jnp.int32)
    rows = market.flow_rows(jnp, jnp.int32(10), flow, grow=True)
    assert len(rows) == 3
    n = len(rollout.MARKET_TURNS)
    st = _blank()
    for part in range(n):
        st = market.apply_flow(jnp, tables, st, jnp.int32(10), flow, backed=True,
                               rows=rows, part=jnp.int32(part), nparts=n)
    assert np.asarray(st.shed)[1, spec.I_WOOL] == 17


# ------------------------------------------------------------------- the pin

def _five_day_state(backed, spread, tid, seed=20260905):
    """Five days of `run_day` with the rung on. -> (money, mkt_inv, shed).

    Jitted, for `test_kagg2_flow`'s reason: an un-jitted `run_day` dispatches
    every primitive one at a time and a five-day walk takes minutes.
    """
    import jax
    from kagg3.core import policy
    from kagg3.es.train import host_words

    tables = build_tables(jnp)
    hi_t, lo_t = eod.weed_threshold()
    words = jnp.asarray(np.asarray(host_words(np.asarray([seed])))[0])
    th = jnp.zeros((2, policy.N_PARAMS), jnp.float32)
    flow = jnp.asarray([1, 1000, 0, tid], jnp.int32)

    @jax.jit
    def walk(st, words, flow):
        for d in range(5):
            st = rollout.run_day(tables, st, jnp.int32(d), words[d], hi_t, lo_t,
                                 th, flow=flow, flow_backed=backed,
                                 flow_spread=spread)
        return st

    st = walk(initial_state(jnp), words, flow)
    return (np.asarray(st.money), np.asarray(st.mkt_inv), np.asarray(st.shed))


@pytest.mark.parametrize("spread", [False, True])
def test_backed_off_is_the_program_it_always_was(spread):
    """The pin: `grow` on the table changes nothing with the switch off.

    Two tables identical but for their production row have to produce the same
    trajectory under `backed=False`, because nothing on that path reads
    production. That is the invariance the flag's default rests on, and it is
    checked as integers rather than a digest so a failure says which array.
    """
    sell, buy, grow = _tape_table(sell_units=20, grow_units=20)
    a = market.register_flow_table(sell, buy)
    b = market.register_flow_table(sell, buy, grow)
    ma, ia, sa = _five_day_state(False, spread, a)
    mb, ib, sb = _five_day_state(False, spread, b)
    assert np.array_equal(ma, mb)
    assert np.array_equal(ia, ib)
    assert np.array_equal(sa, sb)


def test_flow_rows_still_returns_a_pair_with_the_switch_off():
    """The structural half of the pin: no third gather when nothing reads it."""
    sell, buy, grow = _tape_table()
    tid = market.register_flow_table(sell, buy, grow)
    flow = jnp.asarray([1, 1000, 0, tid], jnp.int32)
    assert len(market.flow_rows(jnp, jnp.int32(10), flow)) == 2
    assert len(market.flow_rows(jnp, jnp.int32(10), flow, grow=True)) == 3


def test_a_three_wide_word_reads_a_zero_grow_row():
    """kagg2's mean was measured before `grow`; it has none, and says so."""
    _s, _b, g = market.flow_rows(jnp, jnp.int32(10),
                                 jnp.asarray([1, 1000, 0], jnp.int32), grow=True)
    assert np.array_equal(np.asarray(g), np.zeros(P, np.int32))


# --------------------------------------------------------------- the refusal

def test_tape_flow_backed_names_a_table_that_has_no_grow(tmp_path):
    from kagg3.es.train import Config, Trainer

    path = tmp_path / "tape_999.npz"
    sell, buy, grow = _tape_table()
    TPF.save(str(path), sell, buy, {"episode": 999, "rung": "tape_999"})
    with pytest.raises(ValueError) as exc:
        Trainer(Config(tape_rungs=(str(path),), tape_flow_backed=True,
                       n_archetypes=0))
    assert "tape_999.npz" in str(exc.value)
    assert "grow" in str(exc.value)


def test_a_table_with_grow_is_accepted_by_the_same_check(tmp_path):
    """The other half: the refusal is about the row, not about the flag."""
    path = tmp_path / "tape_998.npz"
    sell, buy, grow = _tape_table()
    TPF.save(str(path), sell, buy, {"episode": 998, "rung": "tape_998"},
             grow=grow)
    t = TPF.load(str(path))
    assert t.grow is not None and t.grow_source == "shed_delta"
    assert market.register_flow_table(t.sell, t.buy, t.grow) >= 0
