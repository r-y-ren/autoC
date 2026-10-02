"""`plan.OPEN_PUMP_ON`: the opening splice's one market order, on our own day 0.

The K=1 opening splice's whole 17.6k edge is a wheat pump, measured order by
order in `scratchpad/curve/report.txt`: `BUY_PRODUCT WHEAT 53` at day 0 hour 0
takes the pot 10000 -> 9947 and the quote 25 -> 32, and the sell-back at the
head of the day-0 BUY row interleaves -- the engine pairs the two seats by
queue index -- with the class-A opening's own first order, `BUY_PRODUCT WHEAT
5`, so their five units cost 160 instead of 134 and the second 500-coin sheep
at the tail of that row is refused off a 24-coin cushion.

Two facts this file holds the switch to, because the mechanism is both:

  * the hour-0 leg is on `O.TURN_HIRE`, *behind* the day's hires, and
  * the sell-back is the FIRST live order of `O.TURN_BUY`. One slot later and
    our 53 units restore the pot before the opponent buys.

It costs no slot: `B_WHEAT` is the BUY row's head slot and day 0 buys no wheat,
so the sell-back changes one slot's op and nothing shifts. The switch refuses
to fire on any day that does buy wheat, which is what keeps that true.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests -- the plan at `a838700` -- and on the same fixture set, since those
digests are the planner with the same four switches out of the way.
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
import pytest
from test_budget_order import _macro
from test_route_early import PIN, PIN_SEEDS, _digest, _plan, _row, _seeded_case, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.sim import market

#: The day-0 board the switch is written for: the shipped opening mix on the
#: engine's own 3,000 coins.
D0 = dict(day=P.OPEN_PUMP_DAY, money=3_000)
D0_MACRO = dict(plant_target=np.asarray((10, 9, 0, 0, 0), np.int32))

SELL_UNITS = P.OPEN_PUMP_UNITS - P.OPEN_PUMP_KEEP


#: The stack `test_route_early`'s digests were taken before, pinned off here
#: for its reason: `PIN` is the planner at `a838700` and none of these five
#: answers anything about a market order. `EARLY_SELL_ON` is the one that does
#: touch this row, so it gets its own ON test against the shipped default.
_PINNED_OFF = ("ROUTE_SPLIT_ON", "SURVIVAL_WATER_ON", "TAIL_CARE_ON",
               "FEED_MANDATORY_ON", "EARLY_SELL_ON")


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)


def _shipped(monkeypatch, value):
    """The switch against the *shipped* stack, not the pinned one: `EARLY_SELL`
    rewrites the BUY row it stands in, so the rows have to be checked there."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", value)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_leaves_the_hire_row_to_the_hires(off):
    """Turn 0 is the crew's row and nothing else, on day 0 as on every day."""
    plan = _plan(_view(**D0), _macro(**D0_MACRO))
    assert {op for op, _, _ in _row(plan, O.TURN_HIRE)} <= {O.MO_HIRE}


def test_off_buy_row_never_sells(off):
    """And the BUY row is purchases only."""
    plan = _plan(_view(**D0), _macro(**D0_MACRO))
    assert O.MO_SELL not in {op for op, _, _ in _row(plan, O.TURN_BUY)}


def test_off_exempts_no_slot(off):
    """The guard is the guard it always was when the switch is off."""
    assert P.OPEN_PUMP_ON is False
    assert not P.open_pump_exempt(O.TURN_BUY).any()


def test_on_is_the_shipped_default_again_since_esr():
    """2026-09-17 PUMPCLIP turned the pump OFF; 2026-09-18 ESR turned it back
    ON (`docs/strategy/2026-09-18-stack5.md`: head to head on the 60 engine
    boards, pump-ON is +49,342 se 7,456 t +6.62, theirs -29,805, and pump-OFF's
    two -67k blow-ups come back positive).  It is a gene as well as a constant,
    and a zero gene decodes to this same ON -- so the `off` fixture above names
    the pre-switch program, not the shipped one."""
    assert P.OPEN_PUMP_ON is True
    assert P.SWITCH_GENE_DEFAULTS["OPEN_PUMP_ON"] is True
    assert "OPEN_PUMP_ON" in P.SWITCH_GENES


# =========================================================================
# ON: the pot at hour 0, the sell-back at index 0
# =========================================================================

def test_on_buys_the_pot_at_hour_zero_behind_the_hires(on):
    """`BUY_PRODUCT WHEAT OPEN_PUMP_UNITS` is the last order of turn 0, and the
    hires are all in front of it -- HIRE is atomic, so the crew is paid before
    this order commits a coin."""
    row = _row(_plan(_view(**D0), _macro(**D0_MACRO)), O.TURN_HIRE)
    assert row[-1] == (O.MO_BUY_PRODUCT, spec.I_WHEAT, P.OPEN_PUMP_UNITS)
    assert {op for op, _, _ in row[:-1]} <= {O.MO_HIRE}
    assert len(row) <= spec.MAX_MARKET_ORDERS


def test_on_sells_back_at_index_zero_of_the_buy_row(on):
    """The whole mechanism: our first live order of turn 1 is the sell-back, so
    it interleaves with the opponent's own first order at the drained quote."""
    row = _row(_plan(_view(**D0), _macro(**D0_MACRO)), O.TURN_BUY)
    assert row[0] == (O.MO_SELL, spec.I_WHEAT, SELL_UNITS)
    assert len(row) <= spec.MAX_MARKET_ORDERS


def test_on_leaves_the_rest_of_the_day_zero_row_intact(on, monkeypatch):
    """One slot changes op and nothing shifts: behind the sell-back the row is
    the purchases the day always made, in the order it always made them."""
    plan_on = _plan(_view(**D0), _macro(**D0_MACRO))
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
    plan_off = _plan(_view(**D0), _macro(**D0_MACRO))
    assert _row(plan_on, O.TURN_BUY)[1:] == _row(plan_off, O.TURN_BUY)
    # and the day's work is untouched -- this is a market order, not a tile.
    for k in (0, 1, 2):
        assert np.array_equal(plan_on[k], plan_off[k])


def test_on_ships_the_same_two_legs_against_the_shipped_stack(monkeypatch):
    """`EARLY_SELL_ON` rewrites the BUY row -- it compacts the live orders and
    packs the day's first lot in behind them -- so the two legs are checked
    again with the shipped switches standing, not only the pinned ones."""
    _shipped(monkeypatch, True)
    plan = _plan(_view(**D0), _macro(**D0_MACRO))
    assert P.EARLY_SELL_ON and P.EARLY_SELL_MODE == "A"
    assert _row(plan, O.TURN_HIRE)[-1] == (O.MO_BUY_PRODUCT, spec.I_WHEAT,
                                           P.OPEN_PUMP_UNITS)
    assert _row(plan, O.TURN_BUY)[0] == (O.MO_SELL, spec.I_WHEAT, SELL_UNITS)


def test_on_fires_on_day_zero_only(on):
    """Every other day has a traded pot, an opponent who is not opening, and a
    purse that is not priced to the coin."""
    for day in (1, 2, 5, 10, 20, 29):
        plan = _plan(_view(day=day, money=3_000), _macro(**D0_MACRO))
        assert O.MO_BUY_PRODUCT not in {op for op, _, _ in _row(plan, O.TURN_HIRE)}, day
        assert O.MO_SELL not in {op for op, _, _ in _row(plan, O.TURN_BUY)}, day


def test_on_needs_the_purse_for_the_whole_leg(on):
    """A day that cannot pay the ladder skips both legs rather than half the
    trade -- a partial buy is a partial denial and a real cost."""
    plan = _plan(_view(day=P.OPEN_PUMP_DAY, money=P.OPEN_PUMP_MIN_MONEY - 1),
                 _macro(**D0_MACRO))
    assert O.MO_BUY_PRODUCT not in {op for op, _, _ in _row(plan, O.TURN_HIRE)}
    assert O.MO_SELL not in {op for op, _, _ in _row(plan, O.TURN_BUY)}


# =========================================================================
# The layout the switch stands on
# =========================================================================

def _bare_market(**kw):
    """`_market` on an empty day: no purchases, no lots, `n_hire` hands."""
    args = dict(wheat_buy=0, fert_buy=0,
                seed_buy=np.zeros(spec.N_CROPS, np.int32),
                a_buy=np.zeros(spec.N_ANIMALS, np.int32), buy_land=0,
                lots=np.zeros((3, spec.N_PRODUCTS), np.int32), n_hire=3)
    args.update(kw)
    return P._market(np, **args)


def _live(mkt, turn):
    op, arg, qty = mkt
    return [(int(op[turn, s]), int(arg[turn, s]), int(qty[turn, s]))
            for s in range(spec.MAX_MARKET_ORDERS) if int(op[turn, s]) != O.MO_NONE]


def test_the_pump_refuses_a_day_that_buys_wheat():
    """The sell-back takes `B_WHEAT`'s slot, so a day with a live wheat buy in
    it cannot pump -- checked, not assumed, because it is the reason the fixed
    layout does not have to move."""
    mkt = _bare_market(wheat_buy=4, pump=np.int32(P.OPEN_PUMP_UNITS))
    assert _live(mkt, O.TURN_BUY) == [(O.MO_BUY_PRODUCT, spec.I_WHEAT, 4)]
    assert {op for op, _, _ in _live(mkt, O.TURN_HIRE)} <= {O.MO_HIRE}


def test_the_pump_refuses_an_eleven_hand_opening():
    """Turn 0's ten slots are the engine's truncation; an eleventh order there
    is eaten in silence, so a full hire row takes the turn."""
    mkt = _bare_market(n_hire=spec.MAX_MARKET_ORDERS,
                       pump=np.int32(P.OPEN_PUMP_UNITS))
    assert {op for op, _, _ in _live(mkt, O.TURN_HIRE)} == {O.MO_HIRE}
    assert _live(mkt, O.TURN_BUY) == []


def test_zero_units_is_off():
    """`pump=0` is how every non-pump day reaches `_market`."""
    mkt = _bare_market(pump=np.int32(0))
    assert {op for op, _, _ in _live(mkt, O.TURN_HIRE)} == {O.MO_HIRE}
    assert _live(mkt, O.TURN_BUY) == []


def test_the_pump_takes_the_head_slot_and_shifts_nothing():
    """A pumping day with a full row behind it still fits the engine's ten."""
    mkt = _bare_market(seed_buy=np.full(spec.N_CROPS, 2, np.int32),
                       a_buy=np.full(spec.N_ANIMALS, 1, np.int32),
                       pump=np.int32(P.OPEN_PUMP_UNITS))
    row = _live(mkt, O.TURN_BUY)
    assert row[0] == (O.MO_SELL, spec.I_WHEAT, SELL_UNITS)
    assert len(row) == 1 + spec.N_CROPS + spec.N_ANIMALS <= spec.MAX_MARKET_ORDERS


# =========================================================================
# The one cross the planner makes on purpose
# =========================================================================

def test_the_guard_still_fires_off_the_exempt_slot(monkeypatch):
    """`assert_no_cross` is narrowed by one slot, not weakened."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    n = spec.MAX_MARKET_ORDERS
    op = np.full((2, n), O.MO_NONE, np.int32)
    arg = np.zeros((2, n), np.int32)
    # a cross in the animal half of the row: still unmodelled, still loud.
    op[0, P.buy_row_slot(P.B_ANIMAL)] = O.MO_SELL
    op[1, P.buy_row_slot(P.B_ANIMAL)] = O.MO_BUY_PRODUCT
    with pytest.raises(AssertionError):
        market.assert_no_cross(op, arg, exempt=P.open_pump_exempt(O.TURN_BUY))


def test_the_exempt_slot_is_the_sell_back(monkeypatch):
    """And the pump's own cross -- our SELL against a foreign seat's opening
    BUY_PRODUCT WHEAT -- is the trade, so the guard lets that one slot past."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    n = spec.MAX_MARKET_ORDERS
    op = np.full((2, n), O.MO_NONE, np.int32)
    arg = np.zeros((2, n), np.int32)
    op[0, P.buy_row_slot(P.B_WHEAT)] = O.MO_SELL
    op[1, P.buy_row_slot(P.B_WHEAT)] = O.MO_BUY_PRODUCT
    market.assert_no_cross(op, arg, exempt=P.open_pump_exempt(O.TURN_BUY))
    with pytest.raises(AssertionError):
        market.assert_no_cross(op, arg)


def test_self_play_never_crosses(monkeypatch):
    """It cannot arise in self-play at all: both seats open on 3,000 coins, so
    both pump on day 0 and both present SELL in that slot."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    plan = _plan(_view(**D0), _macro(**D0_MACRO))
    for h in range(spec.TURNS_PER_DAY):
        mkt_op = np.stack([np.asarray(plan[3])[h]] * 2)
        mkt_a = np.stack([np.asarray(plan[4])[h]] * 2)
        market.assert_no_cross(mkt_op, mkt_a)


# =========================================================================
# The switch under the trainer: `build_day` compiled, not walked
# =========================================================================
#
# The planner runs in two regimes -- concrete numpy in `agent/runtime.py`, and
# `jax` tracers inside `sim/rollout.py`'s `lax.scan` over the season -- and the
# pump's gates (`day == 0`, the purse, `wheat_buy == 0`, an eleven-hand row)
# are all traced scalars there. Nothing in the switch may branch on one in
# Python, and nothing may pull one through `int()`: the first cut of it did,
# on the layout assert, and the trainer would not compile.

def _traced_day_zero(theta_seed):
    """`build_day` on the sim's own day-0 state, under `jax.jit`, exactly as
    `rollout.run_day` calls it. Returns the compiled function and the day-0
    market rows, so a caller can ask the same program for another day."""
    import jax
    import jax.numpy as jnp

    from kagg3.core import brain, policy as PO
    from kagg3.sim import rollout
    from kagg3.sim.state import build_tables, initial_state, prices_of

    tables = build_tables(jnp)

    def market_rows(day, theta):
        st = initial_state(jnp)
        price = prices_of(jnp, tables, st.mkt_inv)
        obs = rollout.policy_obs(st, 0, day, price)
        built = P.build_day(jnp, rollout.day_view(st, 0, day, price),
                            brain.decide(jnp, theta, obs), tables.price)
        return built[3], built[4], built[5]

    theta = jnp.asarray(PO.init_theta(np.random.default_rng(theta_seed)))
    f = jax.jit(market_rows)
    return (lambda day: [np.asarray(x) for x in f(jnp.int32(day), theta)])


def _traced_live(rows, turn):
    op, arg, qty = rows
    return [(int(op[turn, s]), int(arg[turn, s]), int(qty[turn, s]))
            for s in range(spec.MAX_MARKET_ORDERS)
            if int(op[turn, s]) != O.MO_NONE]


#: Two openings that pump: a light crew, and the nine-hand row that fills turn
#: 0 to the engine's tenth slot with the hour-0 leg in it.
@pytest.mark.parametrize("theta_seed", [0, 3])
def test_on_traces_under_jit_and_keeps_both_legs(monkeypatch, theta_seed):
    """The trainer's regime: `build_day` compiles with the switch on, and the
    day-0 rows it emits carry the same two legs the numpy planner emits."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    rows = _traced_day_zero(theta_seed)(0)          # must not raise
    hire = _traced_live(rows, O.TURN_HIRE)
    assert hire[-1] == (O.MO_BUY_PRODUCT, spec.I_WHEAT, P.OPEN_PUMP_UNITS)
    assert {op for op, _, _ in hire[:-1]} <= {O.MO_HIRE}
    assert len(hire) <= spec.MAX_MARKET_ORDERS
    op, arg, qty = rows
    w = P.buy_row_slot(P.B_WHEAT)
    assert (int(op[O.TURN_BUY, w]), int(arg[O.TURN_BUY, w]),
            int(qty[O.TURN_BUY, w])) == (O.MO_SELL, spec.I_WHEAT, SELL_UNITS)
    assert _traced_live(rows, O.TURN_BUY)[0] == (O.MO_SELL, spec.I_WHEAT,
                                                 SELL_UNITS)


def test_on_the_day_gate_is_traced_and_not_compiled_away(monkeypatch):
    """One compiled program, two days: the season runs under a single
    `lax.scan`, so `day == OPEN_PUMP_DAY` has to be a select over a tracer and
    not a Python `if` that bakes day 0's answer into every day."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    run = _traced_day_zero(0)
    assert _traced_live(run(0), O.TURN_HIRE)[-1][0] == O.MO_BUY_PRODUCT
    for day in (1, 7, 20):
        rows = run(day)
        assert O.MO_BUY_PRODUCT not in {o for o, _, _ in
                                        _traced_live(rows, O.TURN_HIRE)}, day
        assert O.MO_SELL not in {o for o, _, _ in
                                 _traced_live(rows, O.TURN_BUY)}, day


def test_off_traces_under_jit_too(monkeypatch):
    """And with the switch off the compiled day-0 rows are the ones the
    planner always emitted -- turn 0 hires, turn 1 buys."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
    rows = _traced_day_zero(0)(0)
    assert {op for op, _, _ in _traced_live(rows, O.TURN_HIRE)} <= {O.MO_HIRE}
    assert O.MO_SELL not in {op for op, _, _ in _traced_live(rows, O.TURN_BUY)}


#: `plan.OPEN_PUMP_SLOT0_ON` went on by default on 2026-09-04: the pump's
#: hour-0 leg moved from slot `first` -- behind the day's hires -- to queue
#: index 0, so that against a seat that draws at hour 0 too the two ladders
#: interleave instead of ours walking the pot they drained. It is pinned off
#: for this file the way `ff3fe12` pinned `OPEN_PUMP_ON` off for the modules it
#: moved under: every row assertion here reads the hour-0 row at the slot the
#: pump was emitted on before that switch, and the question this file asks --
#: that the pump fires on day 0 only, behind a paid crew, and sells back at
#: index 0 of the BUY row -- is the same at either index.
#: `tests/test_open_pump_racer.py` owns both halves of SLOT0.
@pytest.fixture(autouse=True)
def _open_pump_slot0_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", False)


#: `plan.TAIL_FILL_ON` and `plan.BANK_BEFORE_LOT_ON` went on by default on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: OFF digests in this file were taken before the pair existed and still mean
#: what they meant -- "OFF, this file's switch leaves the planner it was cut
#: into alone" -- so the pair is pinned off here the way `EARLY_SELL_ON` and
#: `OPEN_PUMP_ON` were pinned off before it (`854b86b`).
#: `tests/test_tail_fill.py` and `tests/test_bank_before_lot.py` own the two.
@pytest.fixture(autouse=True)
def _tail_pair_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)
