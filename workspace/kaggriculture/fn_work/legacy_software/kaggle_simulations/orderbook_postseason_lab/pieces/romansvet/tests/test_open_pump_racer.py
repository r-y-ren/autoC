"""The two switches for the seat that pumps back: `plan.OPEN_PUMP_SLOT0_ON`
and `plan.OPEN_PUMP_TELL_KEEP0_ON`.

`OPEN_PUMP_ON` denies a class-A opening its second sheep and is measured +20.5k
on panel24. Against the current top-10 tapes it is -4,640 (t -6.22), and
`scratchpad/pumpracer/` says why, order by order: those tapes open with
`BUY_PRODUCT WHEAT 53` at queue index 0 and nothing in front of it, while our
hour-0 leg sits at index `first`, behind the day's hires. `_process_market`
pairs the two seats by index over the compacted row, so their ladder walks the
virgin pot (1,584) and ours walks the drained one (1,796):

  * we pay 212 more and our own second SHEEP is refused at hour 1 by 27 coins;
  * their sell-back into the pot *we* drained earns +105 where a solo round
    trip loses 128, which is two extra day-1 hands and a permanent extra cow.

Two answers, each its own switch:

  SLOT0  put the hour-0 leg at index 0 and the hires behind it. Both ladders
         then interleave at 1,690 apiece. Against a seat that does not draw at
         hour 0 the index is free -- an untouched pot charges 1,584 whichever
         slot asks.
  TELL   at hour 1 the pot reads back the other seat's hour-0 draw, and when it
         says they pumped too, keep none of the 53 instead of five: those five
         sit at the top of a ladder into a pot both seats drained.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests -- the planner at `a838700` -- exactly as `test_open_pump.py` pins it.
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
from test_open_pump import _PINNED_OFF, D0, D0_MACRO, SELL_UNITS, _bare_market, _live
from test_route_early import PIN, PIN_SEEDS, _digest, _plan, _row, _seeded_case, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    """Both new switches off, on the tree the pin was taken from."""
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", False)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", False)
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)


@pytest.fixture
def slot0(monkeypatch):
    """SLOT0 on, over the pump, on the pinned stack."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", True)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)


@pytest.fixture
def pump_only(monkeypatch):
    """The shipped pump with SLOT0 off -- the arm SLOT0 has to leave alone."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)


def _shipped(monkeypatch, value):
    """SLOT0 against the *shipped* stack, not the pinned one: `EARLY_SELL`
    rewrites the BUY row the sell-back stands in, so the rows have to be
    checked there too."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", value)


# =========================================================================
# OFF: byte-identical to the planner these switches were cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switches' contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before them decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_the_two_switches_read_as_off(off):
    """And the arm above is the arm the OFF fixture runs: both switches read
    False inside it, so the digests are the pre-switch planner's."""
    assert P.OPEN_PUMP_SLOT0_ON is False
    assert P.OPEN_PUMP_TELL_KEEP0_ON is False


def test_slot0_and_the_pump_both_ship_on_again():
    """SLOT0 went on by default on 2026-09-04 and is still the shape the pump
    takes when it fires.  PUMPCLIP turned the PUMP ITSELF off on 2026-09-17 and
    ESR turned it back on on 2026-09-18 (`docs/strategy/2026-09-18-stack5.md`),
    so SLOT0 and the pump are live together again and TELL stays off.  Every
    test in this file that needs a particular arm still says so through a
    fixture; none of them read the default."""
    assert P.OPEN_PUMP_ON is True
    assert P.SWITCH_GENE_DEFAULTS["OPEN_PUMP_ON"] is True
    assert P.OPEN_PUMP_SLOT0_ON is True
    assert P.OPEN_PUMP_TELL_KEEP0_ON is False


def test_slot0_off_leaves_the_shipped_hour_zero_row_alone(pump_only):
    """With SLOT0 off the pump's row is slot for slot the one it always was:
    the hires first, the 53 units of wheat behind them."""
    row = _row(_plan(_view(**D0), _macro(**D0_MACRO)), O.TURN_HIRE)
    assert row[-1] == (O.MO_BUY_PRODUCT, spec.I_WHEAT, P.OPEN_PUMP_UNITS)
    assert {op for op, _, _ in row[:-1]} == {O.MO_HIRE}


def test_slot0_changes_nothing_off_the_pumps_own_day(pump_only, monkeypatch):
    """The switch reorders one row of one day: over the pinned boards, every
    board that is not `OPEN_PUMP_DAY` hashes to the same plan either way."""
    was = {s: _digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS}
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", True)
    checked = 0
    for s in PIN_SEEDS:
        if int(_seeded_case(s)[0].day) == P.OPEN_PUMP_DAY:
            continue
        assert _digest(_plan(*_seeded_case(s))) == was[s], s
        checked += 1
    assert checked >= len(PIN_SEEDS) - 1


# =========================================================================
# SLOT0 ON: the pump at index 0, the hires behind it
# =========================================================================

def test_slot0_puts_the_pump_at_index_zero(slot0):
    """The whole mechanism: our first live order of hour 0 is the wheat draw,
    so its ladder is quoted off a pot the racer has not reached yet."""
    row = _row(_plan(_view(**D0), _macro(**D0_MACRO)), O.TURN_HIRE)
    assert row[0] == (O.MO_BUY_PRODUCT, spec.I_WHEAT, P.OPEN_PUMP_UNITS)
    assert {op for op, _, _ in row[1:]} == {O.MO_HIRE}
    assert len(row) <= spec.MAX_MARKET_ORDERS


def test_slot0_keeps_every_hire_the_day_asked_for(slot0, monkeypatch):
    """The hires move one slot along; not one of them is dropped off the end,
    which is the thing a scatter past the tenth slot would do in silence."""
    on = _row(_plan(_view(**D0), _macro(**D0_MACRO)), O.TURN_HIRE)
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", False)
    off_ = _row(_plan(_view(**D0), _macro(**D0_MACRO)), O.TURN_HIRE)
    assert on[1:] == off_[:-1]
    assert len(on) == len(off_)


def test_slot0_moves_nothing_but_the_hour_zero_row(slot0, monkeypatch):
    """The sell-back, the BUY row and the day's whole route are untouched: this
    switch reorders one turn's queue and does nothing else."""
    plan_on = _plan(_view(**D0), _macro(**D0_MACRO))
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", False)
    plan_off = _plan(_view(**D0), _macro(**D0_MACRO))
    assert _row(plan_on, O.TURN_BUY)[0] == (O.MO_SELL, spec.I_WHEAT, SELL_UNITS)
    assert _row(plan_on, O.TURN_BUY) == _row(plan_off, O.TURN_BUY)
    for k in (0, 1, 2):
        assert np.array_equal(plan_on[k], plan_off[k])


def test_slot0_ships_the_two_legs_against_the_shipped_stack(monkeypatch):
    """`EARLY_SELL_ON` rewrites the BUY row the sell-back stands in, so the two
    legs are checked again with the shipped switches standing."""
    _shipped(monkeypatch, True)
    plan = _plan(_view(**D0), _macro(**D0_MACRO))
    assert P.EARLY_SELL_ON and P.EARLY_SELL_MODE == "A"
    assert _row(plan, O.TURN_HIRE)[0] == (O.MO_BUY_PRODUCT, spec.I_WHEAT,
                                          P.OPEN_PUMP_UNITS)
    assert _row(plan, O.TURN_BUY)[0] == (O.MO_SELL, spec.I_WHEAT, SELL_UNITS)


def test_slot0_keeps_every_gate_the_pump_has(slot0):
    """Day, purse, `wheat_buy == 0` and the eleven-hand row: the switch moves
    an index, it does not relax a condition."""
    for day in (1, 2, 10, 29):
        plan = _plan(_view(day=day, money=3_000), _macro(**D0_MACRO))
        assert O.MO_BUY_PRODUCT not in {op for op, _, _ in _row(plan, O.TURN_HIRE)}, day
        assert O.MO_SELL not in {op for op, _, _ in _row(plan, O.TURN_BUY)}, day
    thin = _plan(_view(day=P.OPEN_PUMP_DAY, money=P.OPEN_PUMP_MIN_MONEY - 1),
                 _macro(**D0_MACRO))
    assert O.MO_BUY_PRODUCT not in {op for op, _, _ in _row(thin, O.TURN_HIRE)}
    assert O.MO_SELL not in {op for op, _, _ in _row(thin, O.TURN_BUY)}


def test_slot0_refuses_a_day_that_buys_wheat(monkeypatch):
    """`_market` directly: the sell-back still needs `B_WHEAT`'s slot."""
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", True)
    mkt = _bare_market(wheat_buy=4, pump=np.int32(P.OPEN_PUMP_UNITS))
    assert _live(mkt, O.TURN_BUY) == [(O.MO_BUY_PRODUCT, spec.I_WHEAT, 4)]
    assert {op for op, _, _ in _live(mkt, O.TURN_HIRE)} == {O.MO_HIRE}


def test_slot0_refuses_an_eleven_hand_opening(monkeypatch):
    """Ten hires plus the buy is eleven orders and the engine takes ten, so a
    full hire row still takes the turn whole."""
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", True)
    mkt = _bare_market(n_hire=spec.MAX_MARKET_ORDERS,
                       pump=np.int32(P.OPEN_PUMP_UNITS))
    assert {op for op, _, _ in _live(mkt, O.TURN_HIRE)} == {O.MO_HIRE}
    assert _live(mkt, O.TURN_BUY) == []


@pytest.mark.parametrize("n_hire", [0, 1, 5, 9])
def test_slot0_fits_the_engines_ten_at_every_crew_size(monkeypatch, n_hire):
    """The widest row the switch admits is the buy plus nine hands."""
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", True)
    row = _live(_bare_market(n_hire=n_hire, pump=np.int32(P.OPEN_PUMP_UNITS)),
                O.TURN_HIRE)
    assert row[0] == (O.MO_BUY_PRODUCT, spec.I_WHEAT, P.OPEN_PUMP_UNITS)
    assert row[1:] == [(O.MO_HIRE, 0, 1)] * n_hire
    assert len(row) <= spec.MAX_MARKET_ORDERS


# =========================================================================
# The order of payment: the sim's rounds are the engine's rounds
# =========================================================================
#
# `_process_market` resolves the atomic orders (HIRE, BUY_LAND) of slot round
# *i* before that round's lockstep -- but the rounds themselves run in slot
# order, so a buy at index 0 commits before a hire at index 1. That is the one
# real thing SLOT0 gives up, and it is only harmless because the day-0 hire
# ladder is Fibonacci and tiny. `sim/market.process_slot` has the same shape,
# so the sim's day-0 cash is the engine's for either row order.

def test_the_day_zero_hire_bill_fits_behind_the_ladder():
    """88 coins of hires against 3,000 less the ~1,690-coin ladder: the buy
    spending first cannot refuse a hand of the opening."""
    widest = int(spec.HIRE_COST[:spec.MAX_MARKET_ORDERS - 1].sum())
    assert widest == 88
    assert spec.STARTING_MONEY - 1_796 > widest


def _sim_row(op_row, arg_row, qty_row):
    """Run one seat's ten-slot market row through the simulator's own slot
    loop, the other seat idle, from the engine's day-0 state."""
    import jax.numpy as jnp

    from kagg3.sim import market
    from kagg3.sim.state import build_tables, initial_state

    tables = build_tables(jnp)
    st = initial_state(jnp)
    for s in range(spec.MAX_MARKET_ORDERS):
        op = jnp.asarray([op_row[s], O.MO_NONE], jnp.int32)
        it = jnp.asarray([arg_row[s], 0], jnp.int32)
        n = jnp.asarray([qty_row[s], 0], jnp.int32)
        st = market.process_slot(tables, st, op, it, n)
    return (int(st.money[0]), int(st.nhands[0]), int(st.mkt_inv[spec.I_WHEAT]),
            int(st.shed[0, spec.I_WHEAT]))


def _hand_row(pump_first, n_hire):
    n = spec.MAX_MARKET_ORDERS
    op = np.full(n, O.MO_NONE, np.int32)
    arg = np.zeros(n, np.int32)
    qty = np.zeros(n, np.int32)
    buy, hires = (0, range(1, n_hire + 1)) if pump_first else (n_hire, range(n_hire))
    for s in hires:
        op[s], qty[s] = O.MO_HIRE, 1
    op[buy], arg[buy], qty[buy] = O.MO_BUY_PRODUCT, spec.I_WHEAT, P.OPEN_PUMP_UNITS
    return op, arg, qty


def test_the_sim_pays_the_same_day_zero_cash_for_either_row_order():
    """Both orders leave the same money, the same crew and the same pot: the
    hires are affordable behind the ladder, so the reorder is free in cash and
    only moves who is quoted first against the *other* seat."""
    n_hire = 5
    before = _sim_row(*_hand_row(False, n_hire))
    after = _sim_row(*_hand_row(True, n_hire))
    assert before == after
    money, hands, pot, shed = after
    assert hands == n_hire and shed == P.OPEN_PUMP_UNITS
    assert pot == spec.MARKET_I0 - P.OPEN_PUMP_UNITS
    assert money == spec.STARTING_MONEY - 1_584 - int(spec.HIRE_COST[:n_hire].sum())


def test_the_sim_resolves_hire_at_the_head_of_its_own_slot_round():
    """And the engine's rule, stated as a measurement rather than a comment: a
    hire in a *later* slot than the buy is paid later, so a purse that cannot
    hold both loses the hire and not the buy."""
    op, arg, qty = _hand_row(True, 1)
    import jax.numpy as jnp

    from kagg3.sim import market
    from kagg3.sim.state import build_tables, initial_state
    tables = build_tables(jnp)
    st = initial_state(jnp)._replace(money=jnp.asarray([1_584, 0], jnp.int32))
    for s in range(spec.MAX_MARKET_ORDERS):
        st = market.process_slot(
            tables, st,
            jnp.asarray([op[s], O.MO_NONE], jnp.int32),
            jnp.asarray([arg[s], 0], jnp.int32),
            jnp.asarray([qty[s], 0], jnp.int32))
    assert int(st.shed[0, spec.I_WHEAT]) == P.OPEN_PUMP_UNITS
    assert int(st.money[0]) == 0 and int(st.nhands[0]) == 0


# =========================================================================
# SLOT0 under the trainer: `build_day` compiled, not walked
# =========================================================================

def test_slot0_traces_under_jit_and_keeps_both_legs(monkeypatch):
    """Every gate the switch reads is a traced scalar in `rollout`, so the
    reordered row has to compile as a select and not a Python branch."""
    from test_open_pump import _traced_day_zero, _traced_live

    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    monkeypatch.setattr(P, "OPEN_PUMP_SLOT0_ON", True)
    run = _traced_day_zero(0)
    hire = _traced_live(run(0), O.TURN_HIRE)
    assert hire[0] == (O.MO_BUY_PRODUCT, spec.I_WHEAT, P.OPEN_PUMP_UNITS)
    assert {op for op, _, _ in hire[1:]} == {O.MO_HIRE}
    assert _traced_live(run(0), O.TURN_BUY)[0] == (O.MO_SELL, spec.I_WHEAT,
                                                   SELL_UNITS)
    for day in (1, 7, 20):
        rows = run(day)
        assert O.MO_BUY_PRODUCT not in {o for o, _, _
                                        in _traced_live(rows, O.TURN_HIRE)}, day


# =========================================================================
# TELL: the hour-1 pot, and the one place it can be read
# =========================================================================
#
# The day's plan is built once, at hour 0, so `view.mkt_inv` is the *virgin*
# pot and no expression inside `build_day` can see the tell. The recovery is a
# patch on the cached plan at the turn the BUY row is emitted --
# `agent/runtime.Runtime.act`. The trainer's rollout builds the whole day at
# dawn under one `lax.scan` and cannot see the tell at all, so this switch is
# a submission-path switch and self-play is unchanged by it.

def _pumped_plan(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    return _plan(_view(**D0), _macro(**D0_MACRO))


def _inv(theirs):
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_WHEAT] = spec.MARKET_I0 - P.OPEN_PUMP_UNITS - theirs
    return inv


def test_the_tell_is_off_by_default():
    assert P.OPEN_PUMP_TELL_KEEP0_ON is False
    assert P.open_pump_tell_armed(P.OPEN_PUMP_DAY, O.TURN_BUY) is False


def test_the_tell_arms_on_day_zeros_buy_turn_only(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    assert P.open_pump_tell_armed(P.OPEN_PUMP_DAY, O.TURN_BUY)
    for hour in (0, 2, 3, 12, 23):
        assert not P.open_pump_tell_armed(P.OPEN_PUMP_DAY, hour), hour
    for day in (1, 5, 29):
        assert not P.open_pump_tell_armed(day, O.TURN_BUY), day


def test_the_tell_keeps_nothing_when_the_pot_says_they_pumped(monkeypatch):
    """A top-10 opening draws 30-43 units at hour 0; over the threshold the
    sell-back goes from 48 to all 53."""
    plan = _pumped_plan(monkeypatch)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    out = P.open_pump_tell_keep0(plan, P.OPEN_PUMP_DAY, O.TURN_BUY,
                                 _inv(P.OPEN_PUMP_TELL_MIN))
    assert _row(out, O.TURN_BUY)[0] == (O.MO_SELL, spec.I_WHEAT,
                                        P.OPEN_PUMP_UNITS)
    # one slot's quantity and nothing else.
    assert _row(out, O.TURN_BUY)[1:] == _row(plan, O.TURN_BUY)[1:]
    for k in (0, 1, 2, 3, 4):
        assert np.array_equal(np.asarray(out[k]), np.asarray(plan[k]))


def test_the_tell_holds_its_five_units_against_a_quiet_pot(monkeypatch):
    """A class-A tape is idle at hour 0, so the pot reads back a draw of zero
    and the five feed units are the cheap wheat they always were."""
    plan = _pumped_plan(monkeypatch)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    for theirs in (0, 5, P.OPEN_PUMP_TELL_MIN - 1):
        out = P.open_pump_tell_keep0(plan, P.OPEN_PUMP_DAY, O.TURN_BUY,
                                     _inv(theirs))
        assert out is plan, theirs


def test_the_tell_does_not_mutate_the_cached_plan(monkeypatch):
    """The runtime replays the same arrays for the rest of the day."""
    plan = _pumped_plan(monkeypatch)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    before = np.array(plan[5], np.int32)
    P.open_pump_tell_keep0(plan, P.OPEN_PUMP_DAY, O.TURN_BUY,
                           _inv(P.OPEN_PUMP_TELL_MIN))
    assert np.array_equal(np.asarray(plan[5]), before)


def test_the_tell_leaves_a_plan_without_a_sell_back_alone(monkeypatch):
    """A day the pump declined has a buy or a hole in `B_WHEAT`'s slot, and the
    patch must not turn either into a sale of wheat we do not hold."""
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    plan = _plan(_view(**D0), _macro(**D0_MACRO))
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    out = P.open_pump_tell_keep0(plan, P.OPEN_PUMP_DAY, O.TURN_BUY,
                                 _inv(P.OPEN_PUMP_TELL_MIN))
    assert out is plan


def test_the_tell_is_off_when_the_pump_is(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    assert not P.open_pump_tell_armed(P.OPEN_PUMP_DAY, O.TURN_BUY)


# --- the runtime hook itself ---------------------------------------------

def _obs(hour, theirs):
    """The slice of a kaggle observation `Runtime.act` reads at a non-zero
    hour: the seat's hands, and the market the tell is read from."""
    inv = _inv(theirs)
    return {
        "player": 0, "day": P.OPEN_PUMP_DAY, "hour": hour,
        "farms": [{"hands": []}, {"hands": []}],
        "market": {"inventory": {n: int(inv[i]) for i, n in enumerate(spec.PRODUCTS)},
                   "prices": {n: 0 for n in spec.PRODUCTS}},
    }


def _runtime(monkeypatch, plan):
    from kagg3.agent import runtime
    rt = runtime.Runtime(macro_fn=None)
    rt.plan, rt.day = plan, P.OPEN_PUMP_DAY
    return rt


def test_the_runtime_emits_the_recovered_row_at_hour_one(monkeypatch):
    """Where the switch actually lives: the plan is fixed at hour 0, so the
    recovery happens at the turn the BUY row is handed to the engine."""
    plan = _pumped_plan(monkeypatch)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    rt = _runtime(monkeypatch, plan)
    action = rt.act(_obs(O.TURN_BUY, P.OPEN_PUMP_TELL_MIN))
    assert action["market"][0] == ["SELL", "WHEAT", P.OPEN_PUMP_UNITS]


def test_the_runtime_emits_the_shipped_row_against_a_quiet_pot(monkeypatch):
    plan = _pumped_plan(monkeypatch)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", True)
    rt = _runtime(monkeypatch, plan)
    action = rt.act(_obs(O.TURN_BUY, 0))
    assert action["market"][0] == ["SELL", "WHEAT", SELL_UNITS]


def test_the_runtime_is_untouched_with_the_tell_off(monkeypatch):
    """Off, the hook is one `and` and the market is not even parsed."""
    plan = _pumped_plan(monkeypatch)
    monkeypatch.setattr(P, "OPEN_PUMP_TELL_KEEP0_ON", False)
    rt = _runtime(monkeypatch, plan)
    obs = _obs(O.TURN_BUY, P.OPEN_PUMP_TELL_MIN)
    del obs["market"]                       # unread when the switch is off
    assert rt.act(obs)["market"][0] == ["SELL", "WHEAT", SELL_UNITS]
    assert rt.plan is plan


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
