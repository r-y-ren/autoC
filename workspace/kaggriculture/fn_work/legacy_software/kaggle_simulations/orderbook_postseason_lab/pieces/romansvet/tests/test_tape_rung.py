"""Tape rungs: one Kaggle replay seat's market flow as an ES training rung.

`kagg2_flow` and `kaggle_flow` are *means* -- one bot over 64 games, twelve
losers averaged into a centre. The two class-A tapes that hold our champion to
50% are neither, and the sim has no action-dict seat to replay a tape into. So
the rung is that seat's own measured per-day SELL / BUY_PRODUCT table, played
through the `sim.market.apply_flow` path the other two rungs already use.

What is asserted here is in four parts:

* the **file** round-trips, and every way a table could silently mean something
  else (a permuted product order, a wrong day count, a negative count, two
  rungs with one name) is refused at load;
* the **registration** is idempotent by content, hands out distinct ids for
  distinct tables, and raises `FLOW_K` when a busier table needs it -- without
  moving the two measured means' ids;
* the **rung plays**: `apply_flow` on the tape's table id injects the tape's
  own recorded row, day for day, and a full episode runs through
  `rollout.episode` with the 4-wide control word;
* the **trainer** points a tape rung's episodes at that rung's table and leaves
  a run without one on the exact 3-column word it had before.

The two shipped tables in `artifacts/tape_games/` are checked as fixtures: they
are the rungs an operator will actually name.
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

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg3 import spec
from kagg3.es import kagg2_flow as K2F
from kagg3.es import tape_flow as TPF
from kagg3.sim import eod, market, rollout
from kagg3.sim.state import build_tables, initial_state

#: The tables `scripts/make_tape_rung.py` cut from the two replays that hold
#: the champion to 50% (`Captainuknow`, `Andrew Reed`).
SHIPPED = os.path.join(ROOT, "artifacts", "tape_games")


@pytest.fixture(autouse=True)
def _pristine_flow_tables():
    """Registration mutates module state; hand it back exactly as found.

    `sim.market`'s table stack and `FLOW_K` are process-wide, and
    `tests/test_kaggle_flow.py` asserts `FLOW_K` is *equal* to the size the two
    measured means alone imply. A test that grew it and walked away would fail
    that one from a different file, which is the worst kind of failure to read.
    """
    saved = (market._FLOW_SELL, market._FLOW_BUY, market._FLOW_GROW,
             market.FLOW_K, market.MAX_FLOW_DAY_UNITS)
    yield
    (market._FLOW_SELL, market._FLOW_BUY, market._FLOW_GROW,
     market.FLOW_K, market.MAX_FLOW_DAY_UNITS) = saved


def _table(seed=0, scale=1):
    """A plausible flow table: a few products, a few days, non-negative."""
    rng = np.random.default_rng(seed)
    sell = np.zeros((spec.N_DAYS, spec.N_PRODUCTS), np.int32)
    buy = np.zeros_like(sell)
    for d in range(5, spec.N_DAYS):
        sell[d, spec.ITEM_IX["WHEAT"]] = int(rng.integers(0, 40)) * scale
        sell[d, spec.ITEM_IX["MILK"]] = int(rng.integers(0, 12)) * scale
        buy[d, spec.ITEM_IX["WHEAT"]] = int(rng.integers(0, 20)) * scale
    return sell, buy


def _meta(episode=999):
    return {"episode": episode, "rung": TPF.rung_name(episode), "seat": 0,
            "team": "Someone", "opponent": "OurTeam",
            "final_money": 123456, "source": "L_999.json", "n_games": 1}


def _write(tmp_path, seed=0, episode=999, scale=1):
    sell, buy = _table(seed, scale)
    path = str(tmp_path / f"{episode}.npz")
    TPF.save(path, sell, buy, _meta(episode))
    return path, sell, buy


# ------------------------------------------------------------------- the file

def test_save_load_round_trip(tmp_path):
    path, sell, buy = _write(tmp_path)
    tape = TPF.load(path)
    assert tape.name == "tape_999"
    assert np.array_equal(np.asarray(tape.sell), sell)
    assert np.array_equal(np.asarray(tape.buy), buy)
    assert tape.sell.dtype == np.int32 and tape.buy.dtype == np.int32
    assert tape.meta["team"] == "Someone"
    assert tape.meta["final_money"] == 123456
    # `save` stamps the two things `load` refuses a table for.
    assert tape.meta["products"] == list(spec.PRODUCTS)
    assert tape.meta["days"] == spec.N_DAYS
    assert tape.sell_totals == tuple(int(x) for x in sell.sum(0))
    assert tape.buy_totals == tuple(int(x) for x in buy.sum(0))
    assert tape.max_day_units == int(max(sell.max(), buy.max()))


def test_load_refuses_a_permuted_product_order(tmp_path):
    """A table one column out is not a weaker measurement, it is another one."""
    sell, buy = _table()
    meta = dict(_meta(), products=list(spec.PRODUCTS)[::-1])
    path = str(tmp_path / "bad.npz")
    np.savez(path, sell=sell, buy=buy, meta=np.str_(json.dumps(meta)))
    with pytest.raises(ValueError, match="product order"):
        TPF.load(path)


def test_load_refuses_a_wrong_day_count(tmp_path):
    sell, buy = _table()
    meta = dict(_meta(), days=spec.N_DAYS + 1)
    path = str(tmp_path / "bad.npz")
    np.savez(path, sell=sell, buy=buy, meta=np.str_(json.dumps(meta)))
    with pytest.raises(ValueError, match="days"):
        TPF.load(path)


def test_load_refuses_a_wrong_shape_and_a_negative_count(tmp_path):
    sell, buy = _table()
    short = str(tmp_path / "short.npz")
    np.savez(short, sell=sell[:5], buy=buy[:5],
             meta=np.str_(json.dumps(_meta())))
    with pytest.raises(ValueError, match="expected"):
        TPF.load(short)

    neg = sell.copy()
    neg[7, 0] = -1
    with pytest.raises(ValueError, match="negative"):
        TPF.save(str(tmp_path / "neg.npz"), neg, buy, _meta())


def test_load_refuses_a_file_that_is_not_a_rung(tmp_path):
    path = str(tmp_path / "other.npz")
    np.savez(path, theta=np.zeros(3))
    with pytest.raises(ValueError, match="not a tape rung"):
        TPF.load(path)


def test_load_many_refuses_two_rungs_with_one_name(tmp_path):
    """One label is one ladder slot: the second would never be played."""
    a, _, _ = _write(tmp_path / "a", seed=1)
    b, _, _ = _write(tmp_path / "b", seed=2)
    with pytest.raises(ValueError, match="two tape rungs"):
        TPF.load_many([a, b])
    assert len(TPF.load_many([a])) == 1


def test_the_shipped_tapes_are_the_two_that_hold_the_champion():
    """`artifacts/tape_games/` carries the rungs an operator names."""
    paths = sorted(os.path.join(SHIPPED, f) for f in os.listdir(SHIPPED)
                   if f.endswith(".npz"))
    tapes = {t.name: t for t in TPF.load_many(paths)}
    assert {"tape_103254816", "tape_103210032"} <= set(tapes)
    for name, team in (("tape_103254816", "Captainuknow"),
                       ("tape_103210032", "Andrew Reed")):
        t = tapes[name]
        assert t.meta["team"] == team
        assert t.meta["opponent"] == "OurTeam"
        assert t.meta["n_games"] == 1, "a tape rung is one game, not a mean"
        # A class-A wheat clone: it is a heavy net wheat seller and it keeps no
        # geese, which is what makes it a different market from `kagg2_flow`.
        wheat = spec.ITEM_IX["WHEAT"]
        assert t.sell_totals[wheat] - t.buy_totals[wheat] > 200
        assert t.sell_totals[spec.ITEM_IX["EGG"]] == 0
        assert t.sell_totals != K2F.SELL_TOTALS, "this is not kagg2's market"


# --------------------------------------------------------------- registration

def test_registration_is_idempotent_by_content(tmp_path):
    path, sell, buy = _write(tmp_path)
    tape = TPF.load(path)
    before = market.registered_flow_tables()
    first = market.register_flow_table(tape.sell, tape.buy)
    again = market.register_flow_table(tape.sell, tape.buy)
    assert first == again == before
    assert market.registered_flow_tables() == before + 1
    # A *different* table is a different id, and the two measured means keep
    # theirs -- every rung index and control word already on record depends on
    # it.
    other_sell, other_buy = _table(seed=5)
    assert market.register_flow_table(other_sell, other_buy) == before + 1
    assert market.FLOW_T_KAGG2 == 0 and market.FLOW_T_KAGGLE == 1
    assert first >= market.N_MEASURED_TABLES


def test_registration_refuses_a_table_that_is_not_one():
    with pytest.raises(ValueError, match="expected"):
        market.register_flow_table(np.zeros((3, 3), np.int32),
                                   np.zeros((3, 3), np.int32))
    sell, buy = _table()
    bad = sell.copy()
    bad[0, 0] = -2
    with pytest.raises(ValueError, match="negative"):
        market.register_flow_table(bad, buy)


def test_a_busier_table_lengthens_the_quote_walk():
    """`FLOW_K` is what stops a big day truncating instead of scaling."""
    k0, m0 = market.FLOW_K, market.MAX_FLOW_DAY_UNITS
    sell, buy = _table(seed=3)
    sell[12, spec.ITEM_IX["WHEAT"]] = m0 + 50
    market.register_flow_table(sell, buy)
    assert market.MAX_FLOW_DAY_UNITS == m0 + 50
    assert market.FLOW_K == 2 * (m0 + 50) + 1 > k0
    # A table that already fitted leaves it alone.
    market.register_flow_table(*_table(seed=4))
    assert market.FLOW_K == 2 * (m0 + 50) + 1


# ------------------------------------------------------------ the rung plays

def _tables():
    return build_tables(jnp)


def _blank_state(money=20_000, shed=0):
    st = initial_state(jnp)
    st = st._replace(money=jnp.int32([money, money]))
    if shed:
        st = st._replace(shed=jnp.full_like(st.shed, shed))
    return st


@pytest.mark.parametrize("day", [6, 13, 22, 29])
def test_the_rung_injects_the_recorded_row_for_that_day(day):
    """What the sim plays on day `d` is what the tape recorded on day `d`.

    The tape's *market presence* is the part of it the sim replays, so this is
    the tape-fidelity check the rung can be held to: the injected units are the
    measured ones, day for day, and not the mean of some other opponent's.
    """
    tape = TPF.load(os.path.join(SHIPPED, "103254816.npz"))
    tid = market.register_flow_table(tape.sell, tape.buy)
    tabs, st = _tables(), _blank_state()
    out = market.apply_flow(jnp, tabs, st, jnp.int32(day),
                            jnp.asarray([1, 1000, 0, tid], jnp.int32))
    d_inv = np.asarray(out.mkt_inv) - np.asarray(st.mkt_inv)
    want = (np.asarray(tape.sell[day], np.int64)
            - np.asarray(tape.buy[day], np.int64))
    # Every unit here prices well above the $1 floor, so a sell advances the
    # inventory one for one and the net move is sells minus buys -- the same
    # reading `test_kagg2_flow.test_flow_moves_the_market_by_the_table` takes.
    assert np.array_equal(d_inv, want)
    # Seat 1 is the flow seat: the other seat's purse must not move.
    assert (np.asarray(out.money) - np.asarray(st.money))[0] == 0


def test_the_tape_table_is_not_the_kagg2_table():
    """The rung exists because it is a *different* market; prove it is one."""
    tape = TPF.load(os.path.join(SHIPPED, "103254816.npz"))
    tid = market.register_flow_table(tape.sell, tape.buy)
    tabs, st = _tables(), _blank_state()
    day = jnp.int32(10)
    mine = market.apply_flow(jnp, tabs, st, day,
                             jnp.asarray([1, 1000, 0, tid], jnp.int32))
    k2 = market.apply_flow(jnp, tabs, st, day,
                           jnp.asarray([1, 1000, 0, market.FLOW_T_KAGG2],
                                       jnp.int32))
    assert not np.array_equal(np.asarray(mine.mkt_inv), np.asarray(k2.mkt_inv))


def test_the_rung_plays_a_whole_episode():
    """End to end through `rollout.episode` -- the thing training runs."""
    tape = TPF.load(os.path.join(SHIPPED, "103210032.npz"))
    tid = market.register_flow_table(tape.sell, tape.buy)
    tabs = _tables()
    hi, lo = eod.weed_threshold()
    words = jnp.asarray(np.stack([eod.host_stream(20260830, d)
                                  for d in range(spec.N_DAYS)]))
    from kagg3.core import policy as PO
    thetas = jnp.zeros((2, PO.N_PARAMS), jnp.float32)

    @jax.jit
    def play(flow):
        return rollout.episode(tabs, thetas, words, jnp.int32(hi),
                               jnp.int32(lo), None, None, flow)

    money, _daily, _st = play(jnp.asarray([1, 1000, 0, tid], jnp.int32))
    off = jnp.asarray(tuple(market.FLOW_OFF) + (market.FLOW_T_KAGG2,),
                      jnp.int32)
    base, _bd, _bs = play(off)
    money, base = np.asarray(money), np.asarray(base)
    assert np.isfinite(money).all()
    # The flow seat is 1: it earned the tape's market coins, and the quotes it
    # moved changed what seat 0 could realise. Both halves have to move, or the
    # rung is not an opponent.
    assert money[1] != base[1]
    assert money[0] != base[0]


# ----------------------------------------------------------------- the trainer

def _stub(seed=7, tape_slots=(), **cfg):
    """A `Trainer` carrying only what `episode_flow`/`flow_words` read.

    `__new__` rather than a real construction, for `test_kagg2_flow`'s reason:
    what is under test is which table each episode is pointed at, and building
    a ladder would spend a minute of archetype probing to find out.
    """
    from kagg3.es.train import Config, Trainer

    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**cfg)
    tr.pool = []
    tr.flow_rung = 0 if cfg.get("kagg2_flow") else -1
    tr.kaggle_rung = -1
    tr.tapes = tuple((f"tape_{i}", tid) for i, (_r, tid) in enumerate(tape_slots))
    tr.tape_slots = tuple(tape_slots)
    tr.rng = np.random.default_rng(seed)
    return tr


def test_a_tape_rung_episode_is_pointed_at_its_own_table():
    tr = _stub(kagg2_flow=True, tape_slots=((1, 4), (2, 7)))
    rungs = np.array([-1, 0, 1, 2])
    is_flow, table = tr.flow_rung_tables(rungs)
    assert list(is_flow) == [False, True, True, True]
    assert list(table) == [market.FLOW_T_KAGG2, market.FLOW_T_KAGG2, 4, 7]


def test_episode_flow_carries_the_table_column_for_a_tape_run():
    n = 4
    tr = _stub(kagg2_flow=True, tape_slots=((1, 5),))
    # Pair 0 plays the kagg2 rung, pairs 1..3 the tape rung.
    idx = np.array([0, 1, 1, 1])
    w = np.asarray(tr.episode_flow(n, idx))
    assert w.shape == (2 * n, 4), "a tape run needs the table column"
    assert list(w[:2, market.FLOW_TABLE]) == [market.FLOW_T_KAGG2] * 2
    assert list(w[2:, market.FLOW_TABLE]) == [5] * 6
    # Both seats of a pair share one draw, and the flow drives `1 - seat`.
    assert list(w[:, market.FLOW_SEAT]) == [1, 0] * n
    assert w[2, market.FLOW_SCALE] == w[3, market.FLOW_SCALE]


def test_the_tape_draw_is_last_so_a_run_without_one_is_unchanged():
    """Adding the rung must not move the RNG stream of the runs before it."""
    n = 5
    idx = np.zeros(n, int)
    plain = _stub(kagg2_flow=True)
    with_tape = _stub(kagg2_flow=True, tape_slots=((1, 5),))
    a = np.asarray(plain.episode_flow(n, idx))
    b = np.asarray(with_tape.episode_flow(n, idx))
    # Same scales and shifts on the kagg2 pairs: the tape's own draw happens
    # after them, so it cannot re-seed the episodes that came first.
    assert list(a[:, market.FLOW_SCALE]) == list(b[:, market.FLOW_SCALE])
    assert list(a[:, market.FLOW_SHIFT]) == list(b[:, market.FLOW_SHIFT])
    assert a.shape[1] == 3 and b.shape[1] == 4


def test_a_run_with_no_flow_rung_at_all_still_has_no_flow():
    tr = _stub()
    assert tr.episode_flow(3, np.zeros(3, int)) is None
    assert tr.flow_words(np.zeros(3, bool), np.zeros(3, np.int32)) is None


def test_tape_flow_ranges_default_to_the_kagg2_rungs():
    """`None` is 'share the kagg2 draw', not 'no randomisation'."""
    from kagg3.es.train import Config

    n = 6
    tr = _stub(kagg2_flow=True, tape_slots=((0, 5),))
    w = np.asarray(tr.episode_flow(n, np.zeros(n, int)))
    lo, hi = Config().kagg2_flow_scale
    j = Config().kagg2_flow_jitter
    assert (w[:, market.FLOW_SCALE] >= lo * 1000).all()
    assert (w[:, market.FLOW_SCALE] <= hi * 1000).all()
    assert (np.abs(w[:, market.FLOW_SHIFT]) <= j).all()
    # And a stated range is used instead.
    tr2 = _stub(kagg2_flow=True, tape_slots=((0, 5),),
                tape_flow_scale=(1.0, 1.0), tape_flow_shift=(3, 3))
    w2 = np.asarray(tr2.episode_flow(n, np.zeros(n, int)))
    assert set(w2[:, market.FLOW_SCALE]) == {1000}
    assert set(w2[:, market.FLOW_SHIFT]) == {3}


# ---------------------------------------------------------------- the script

def test_resolve_seat_measures_the_other_seat():
    import make_tape_rung as MTR

    teams = ["Captainuknow", "OurTeam"]
    assert MTR.resolve_seat(teams, "OurTeam", None, None) == 0
    assert MTR.resolve_seat(teams, "OurTeam", None, 1) == 1
    assert MTR.resolve_seat(teams, "OurTeam", "Captain", None) == 0
    with pytest.raises(SystemExit):
        MTR.resolve_seat(teams, "Nobody Here", None, None)


def test_rung_names_lists_the_tapes_the_ladder_will_hold():
    import train as TRAIN

    names = TRAIN.rung_names(2, kagg2_flow=True, kaggle_flow=True,
                             tapes=("tape_1", "tape_2"))
    assert names[-4:] == [K2F.RUNG_NAME, "kaggle_flow", "tape_1", "tape_2"]
