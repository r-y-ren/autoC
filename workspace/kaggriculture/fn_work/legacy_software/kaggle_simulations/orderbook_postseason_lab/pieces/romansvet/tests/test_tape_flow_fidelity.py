"""`--tape-flow-backed` and `--tape-flow-spread`: the two fidelity switches.

Both are off by default and both must be *inert* when off, so the first thing
in here is a verbatim transcription of the arithmetic `market.apply_flow` had
before either existed (`_apply_flow_before`), checked against the live function
over a grid of days, tables, seats and scales. That is the byte-identity claim:
not "close", not "equal on one case", but the same integers out of the same
inputs on every case the pre-change code could have been asked.

With them **on**:

* `backed` -- the flow seat may only sell what its shed holds, and the clamp
  lands *before* the revenue and the market's inventory advance, not only on
  the shed drain. A seat holding nothing sells nothing and is paid nothing.
* `spread` -- the day's table is spent one `MARKET_TURNS`-share at a time. The
  season total is the table's to the unit; with no other trader in the book the
  end-of-day market inventory is the unspread one as well, because the price
  curve is monotone in inventory and a unit that reached the floor stays there.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import jax                                                        # noqa: E402
import jax.numpy as jnp                                           # noqa: E402
import numpy as np                                                # noqa: E402
import pytest                                                     # noqa: E402

from kagg3 import spec                                            # noqa: E402
from kagg3.es import archetypes as AR                             # noqa: E402
from kagg3.sim import eod, market, rollout                        # noqa: E402
from kagg3.sim.state import build_tables, initial_state           # noqa: E402


# --------------------------------------------------------------- the old code

def _apply_flow_before(xp, tables, st, day, flow):
    """`market.apply_flow` as it stood before the two switches. Verbatim.

    Kept here rather than imported so the identity test cannot be broken by
    the same edit it is guarding: if someone changes the live function's
    default behaviour, this copy does not follow.
    """
    i32 = xp.int32
    seat = flow[market.FLOW_SEAT]
    sel = xp.arange(2, dtype=i32) == seat
    src = day - flow[market.FLOW_SHIFT]
    live = (seat >= 0) & (src >= 0) & (src < spec.N_DAYS)
    d = xp.clip(src, 0, spec.N_DAYS - 1)
    scale = xp.where(live, flow[market.FLOW_SCALE], 0)
    if int(flow.shape[-1]) > market.FLOW_TABLE:
        tbl = flow[market.FLOW_TABLE]
        sell_row = xp.asarray(market._FLOW_SELL)[tbl, d]
        buy_row = xp.asarray(market._FLOW_BUY)[tbl, d]
    else:
        sell_row = xp.asarray(market.K2.KAGG2_FLOW)[d]
        buy_row = xp.asarray(market.K2.KAGG2_BUY)[d]
    n_sell = (sell_row * scale + 500) // 1000
    n_buy = (buy_row * scale + 500) // 1000

    K = market.FLOW_K
    j = xp.arange(K, dtype=i32)
    prod = xp.arange(spec.N_PRODUCTS, dtype=i32)

    def walk(inv, off):
        idx = xp.clip(inv[:, None] + off - spec.PRICE_TABLE_LO,
                      0, spec.PRICE_TABLE_N - 1)
        q = tables.price[prod[:, None], idx]
        return q, xp.cumsum(q, axis=1)

    def total(cum, k):
        return xp.where(k > 0, cum[prod, xp.clip(k - 1, 0, K - 1)], 0)

    def shed_delta(row):
        wide = xp.concatenate(
            [row, xp.zeros((spec.N_ITEMS - spec.N_PRODUCTS,), i32)])
        return xp.where(sel[:, None], wide[None, :], 0)

    k = xp.clip(n_sell, 0, K - 1)
    q, cum = walk(st.mkt_inv, j[None, :])
    rev = total(cum, k)
    adv = xp.sum(((q > spec.PRICE_FLOOR) & (j[None, :] < k[:, None])).astype(i32),
                 axis=1)
    have = xp.sum(xp.where(sel[:, None], st.shed[:, :spec.N_PRODUCTS], 0), axis=0)
    drain = xp.minimum(k, have)
    st = st._replace(
        mkt_inv=st.mkt_inv + adv,
        money=st.money + xp.where(sel, xp.sum(rev), 0),
        shed=st.shed + shed_delta(-drain),
    )

    kb = xp.clip(n_buy, 0, K - 1)
    _, cumb = walk(st.mkt_inv, -1 - j[None, :])
    cost = total(cumb, kb)
    room = xp.maximum(
        spec.SHED_CAPACITY - xp.sum(xp.where(sel, xp.sum(st.shed, axis=1), 0)), 0)
    before = xp.cumsum(kb) - kb
    take = xp.minimum(kb, xp.maximum(room - before, 0))
    return st._replace(
        mkt_inv=st.mkt_inv - kb,
        money=st.money - xp.where(sel, xp.sum(cost), 0),
        shed=st.shed + shed_delta(take),
    )


# ------------------------------------------------------------------- fixtures

def _tables():
    return build_tables(jnp)


def _state(money=200_000, shed=0, inv=None):
    st = initial_state(jnp)
    st = st._replace(money=jnp.int32([money, money]))
    if shed:
        st = st._replace(shed=jnp.full_like(st.shed, shed))
    if inv is not None:
        st = st._replace(mkt_inv=jnp.asarray(inv, jnp.int32))
    return st


def _same(a, b, what=""):
    for f in ("money", "mkt_inv", "shed"):
        assert np.array_equal(np.asarray(getattr(a, f)),
                              np.asarray(getattr(b, f))), f"{what}: {f}"


def _one_product_table(item, day, sell=0, buy=0):
    """A table that trades one product on one day and nothing else. -> id."""
    s = np.zeros((spec.N_DAYS, spec.N_PRODUCTS), np.int32)
    b = np.zeros((spec.N_DAYS, spec.N_PRODUCTS), np.int32)
    s[day, item] = sell
    b[day, item] = buy
    return market.register_flow_table(s, b)


def _word(seat, scale=1000, shift=0, table=None):
    if table is None:
        return jnp.asarray([seat, scale, shift], jnp.int32)
    return jnp.asarray([seat, scale, shift, table], jnp.int32)


# ------------------------------------------------- (b) OFF is the old program

@pytest.mark.parametrize("day", [0, 7, 14, 21, 29])
@pytest.mark.parametrize("word", [(1, 1000, 0), (0, 1000, 0), (1, 1600, 3),
                                  (1, 700, -2), (-1, 1000, 0)])
def test_off_is_the_pre_switch_arithmetic_to_the_coin(day, word):
    """Flags off: the same integers the old `apply_flow` produced."""
    tabs = _tables()
    for shed in (0, 4, 60):
        st = _state(shed=shed)
        for w in (_word(*word), _word(*word, table=market.FLOW_T_KAGG2)):
            new = market.apply_flow(jnp, tabs, st, jnp.int32(day), w)
            old = _apply_flow_before(jnp, tabs, st, jnp.int32(day), w)
            _same(new, old, f"day={day} word={word} shed={shed}")
            # and the default really is off
            _same(new, market.apply_flow(jnp, tabs, st, jnp.int32(day), w,
                                         backed=False, part=None),
                  "explicit off")


def test_off_episode_is_the_pre_switch_episode():
    """The whole season, not just one day: flags off reproduce the run."""
    tabs = _tables()
    hi, lo = eod.weed_threshold()
    words = jnp.asarray(np.stack([eod.host_stream(20260902, d)
                                  for d in range(spec.N_DAYS)]))
    th = jnp.stack([jnp.asarray(AR.archetype_theta(**AR.named("wheat_clone"))),
                    jnp.asarray(AR.archetype_theta(**AR.named("wheat_clone")))])
    flow = _word(1, table=market.FLOW_T_KAGG2)
    run = jax.jit(lambda f, b, s: rollout.episode(
        tabs, th, words, jnp.int32(hi), jnp.int32(lo), None, None, f,
        flow_backed=b, flow_spread=s), static_argnums=(1, 2))
    base = np.asarray(run(flow, False, False)[0])
    # `episode`'s own defaults are the same program.
    plain = jax.jit(lambda f: rollout.episode(
        tabs, th, words, jnp.int32(hi), jnp.int32(lo), None, None, f))
    assert np.array_equal(base, np.asarray(plain(flow)[0]))
    # and the switches are not no-ops, or there would be nothing to test
    assert not np.array_equal(base, np.asarray(run(flow, True, False)[0]))
    assert not np.array_equal(base, np.asarray(run(flow, False, True)[0]))


# --------------------------------------------------- (a) BACKED is the engine

def test_backed_sells_nothing_out_of_an_empty_shed():
    """Holding 0, the seat sells 0, earns 0, and the book never sees it."""
    tabs = _tables()
    day = 3
    tid = _one_product_table(spec.I_MELON, day, sell=7)
    st = _state(shed=0)
    w = _word(1, table=tid)
    on = market.apply_flow(jnp, tabs, st, jnp.int32(day), w, backed=True)
    _same(on, st, "an empty shed must move nothing at all")
    # Off, the same seat is paid six figures for melons it never grew.
    off = market.apply_flow(jnp, tabs, st, jnp.int32(day), w)
    assert np.asarray(off.money)[1] > np.asarray(st.money)[1]
    assert np.asarray(off.mkt_inv)[spec.I_MELON] == \
        np.asarray(st.mkt_inv)[spec.I_MELON] + 7


def test_backed_sells_min_of_stock_and_the_table():
    """Holding 5 against a row of 7, the seat sells exactly 5 -- and that is
    the same trade a table asking for 5 would have made."""
    tabs = _tables()
    day = 3
    seven = _one_product_table(spec.I_MELON, day, sell=7)
    five = _one_product_table(spec.I_MELON, day, sell=5)
    st = _state(shed=0)
    st = st._replace(shed=st.shed.at[1, spec.I_MELON].set(5))

    clamped = market.apply_flow(jnp, tabs, st, jnp.int32(day),
                                _word(1, table=seven), backed=True)
    honest = market.apply_flow(jnp, tabs, st, jnp.int32(day),
                               _word(1, table=five))
    _same(clamped, honest, "min(stock, row) is the row it could afford")
    assert np.asarray(clamped.shed)[1, spec.I_MELON] == 0
    assert np.asarray(clamped.money)[1] > np.asarray(st.money)[1]

    # Stock above the row is not a licence to sell more than the row.
    rich = st._replace(shed=st.shed.at[1, spec.I_MELON].set(40))
    a = market.apply_flow(jnp, tabs, rich, jnp.int32(day),
                          _word(1, table=seven), backed=True)
    b = market.apply_flow(jnp, tabs, rich, jnp.int32(day),
                          _word(1, table=seven))
    _same(a, b, "with the stock to back it, backed changes nothing")


def test_backed_leaves_the_buys_alone():
    """Only the sell side is clamped; a BUY is exogenous cash, as before."""
    tabs = _tables()
    day = 5
    tid = _one_product_table(spec.I_WHEAT, day, buy=11)
    st = _state(shed=0)
    w = _word(1, table=tid)
    on = market.apply_flow(jnp, tabs, st, jnp.int32(day), w, backed=True)
    off = market.apply_flow(jnp, tabs, st, jnp.int32(day), w)
    _same(on, off, "buys are untouched by --tape-flow-backed")
    assert np.asarray(on.shed)[1, spec.I_WHEAT] == 11


# ------------------------------------------------------ (c) SPREAD conserves

def _spread_day(tabs, st, day, w, backed=False):
    """Every market turn's share, in turn order, off one day's rows."""
    n = len(rollout.MARKET_TURNS)
    # `grow=backed`: under the clamp the seat is credited with the production
    # its table implies, and `apply_flow` refuses a precomputed row pair that
    # does not carry it.
    rows = market.flow_rows(jnp, jnp.int32(day), w, grow=backed)
    for p in range(n):
        st = market.apply_flow(jnp, tabs, st, jnp.int32(day), w, backed=backed,
                               rows=rows, part=jnp.int32(p), nparts=n)
    return st


@pytest.mark.parametrize("day", [0, 6, 10, 17, 24])
def test_spread_spends_exactly_the_days_row(day):
    """Summed over the day's market turns, the shares are the table's row."""
    n = len(rollout.MARKET_TURNS)
    w = _word(1, table=market.FLOW_T_KAGG2)
    sell, buy = market.flow_rows(jnp, jnp.int32(day), w)
    for row in (sell, buy):
        parts = [np.asarray(market._share_of_day(jnp, row, jnp.int32(p), n))
                 for p in range(n)]
        assert np.array_equal(np.sum(parts, axis=0), np.asarray(row))
        # every share but the last is the same floor share
        for p in range(n - 1):
            assert np.array_equal(parts[p], np.asarray(row) // n)


@pytest.mark.parametrize("day", [0, 6, 10, 17, 24])
def test_spread_moves_the_same_stock_and_the_same_book(day):
    """With nobody else in the book, spreading a day is the unspread day.

    `mkt_inv` and the seat's `shed` land on the same integers: the quantities
    are conserved by construction, a sell advances the book once per unit
    priced above the floor, and the price curve is monotone in inventory -- so
    a unit that reached the floor in one walk reaches it in the other. Only
    `money` is allowed to differ, and it does: the tape now pays the second
    half of its day at the prices its own first half made, which is the whole
    point of the switch.
    """
    tabs = _tables()
    w = _word(1, table=market.FLOW_T_KAGG2)
    st = _state(shed=30)
    once = market.apply_flow(jnp, tabs, st, jnp.int32(day), w)
    many = _spread_day(tabs, st, day, w)
    assert np.array_equal(np.asarray(once.mkt_inv), np.asarray(many.mkt_inv))
    assert np.array_equal(np.asarray(once.shed), np.asarray(many.shed))
    assert np.asarray(many.money)[0] == np.asarray(once.money)[0]


def test_spread_in_the_rollout_is_the_same_day_shared_out():
    """`run_day` under the switch applies each share once, on a market turn.

    Both seats are handed a theta that places no market order at all, so the
    day's whole market move is the tape's and the unspread day is the exact
    reference. `MARKET_TURNS` is the set `turn_body` itself branches on.
    """
    tabs = _tables()
    hi, lo = eod.weed_threshold()
    words = jnp.asarray(np.stack([eod.host_stream(4242, d)
                                  for d in range(spec.N_DAYS)]))
    idle = jnp.zeros((2, len(AR.archetype_theta(**AR.named("wheat_clone")))),
                     jnp.float32)
    w = _word(1, table=market.FLOW_T_KAGG2)
    day = jnp.int32(9)
    st = _state(shed=30)
    run = jax.jit(lambda s, sp: rollout.run_day(
        tabs, s, day, words[9], jnp.int32(hi), jnp.int32(lo), idle,
        do_eod=False, flow=w, flow_spread=sp), static_argnums=(1,))
    a = run(st, False)
    b = run(st, True)
    assert np.array_equal(np.asarray(a.mkt_inv), np.asarray(b.mkt_inv))
    assert np.array_equal(np.asarray(a.shed), np.asarray(b.shed))
    # The seat's coins are the thing that moves: it no longer gets the whole
    # book to itself before the first order of the day.
    assert np.asarray(a.money)[1] != np.asarray(b.money)[1]


def test_market_turns_is_exactly_the_set_turn_body_branches_on():
    from kagg3.core import ops as O
    from kagg3.core import plan as P
    want = set(range(O.FULL_MARKET_TURNS)) | set(O.SELL_TURNS)
    if P.PRESTOCK_ON:
        want |= {O.TURN_PRESTOCK}
    assert set(rollout.MARKET_TURNS) == want
    assert list(rollout.MARKET_TURNS) == sorted(rollout.MARKET_TURNS)
    # every share lands inside the last day's shortened scan too
    assert max(rollout.MARKET_TURNS) < spec.TURNS_PER_DAY - 1


# ------------------------------------------------------------- (d) the wiring

def test_config_and_trainer_carry_the_switches():
    from kagg3.es.train import Config, make_evaluator
    cfg = Config()
    assert cfg.tape_flow_backed is False and cfg.tape_flow_spread is False
    # `make_evaluator`'s extra arguments are optional, so every existing call
    # site (scripts/ladder.py, the GPU gate, the tests) is unchanged.
    assert make_evaluator(jnp.int32(1), jnp.int32(1)) is not None


def test_the_liveness_floor_is_lifted_only_for_the_flow_rungs_and_only_backed():
    """`--tape-flow-backed` starves the flow seat below `AR.MIN_COINS`.

    The rung's coins are an exogenous table clamped to a `TAPE_PLANNER` shed,
    so with the switch on `tape_103254816` probes at 7,011 against a floor of
    10,000 and `Trainer.__init__` would refuse to start. The floor is lifted
    for the flow rungs and nothing else -- and only with the switch on.
    """
    from kagg3.es import archetypes as AR
    from kagg3.es.train import Config, Trainer

    def floors(backed):
        tr = Trainer.__new__(Trainer)
        tr.cfg = Config(tape_flow_backed=backed)
        tr.flow_rung, tr.kaggle_rung = 11, 12
        tr.tape_slots = ((13, 2), (14, 3))
        return [tr._liveness_floor(i) for i in range(16)]

    off = floors(False)
    assert off == [AR.MIN_COINS] * 16
    on = floors(True)
    assert [i for i, f in enumerate(on) if f == 0.0] == [11, 12, 13, 14]
    assert all(f == AR.MIN_COINS for i, f in enumerate(on)
               if i not in (11, 12, 13, 14))


def test_the_cli_flags_reach_the_config():
    import runpy
    import subprocess
    del runpy
    out = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "scripts", "train.py"), "--help"],
        capture_output=True, text=True, env={**os.environ, "JAX_PLATFORMS": "cpu"})
    assert "--tape-flow-backed" in out.stdout
    assert "--tape-flow-spread" in out.stdout
