"""`plan.EVE_STOCK_ON`: buy tomorrow's pickups tonight, start tomorrow at turn 1.

`docs/strategy/2026-09-16-evestock.md`.  The measured cause of our dawn wait
(`S/evestock/probe.py`, ENG22, 22 real-engine boards, d20-29): of 111 lead-PASS
unit-turns a game -- the PASS steps before a unit's FIRST act, ROUTEEFF's
`dawn_pass` to the coin -- 51.6 % is a block owing a PICKUP of an item the shed
ALREADY holds and 33.8 % a PICKUP of an item the day's own turn-1 BUY row
delivers.  The engine class starts 28 % of its unit-days at turn 1 to our 13 %
and holds 4.87 seeds at dawn to our 0.66.

The switch is the composition of two arms that each reached one half:
`_prestock`'s row at `O.TURN_PRESTOCK` buys tomorrow's feed wheat and
fertilizer tonight (products only -- `PRESTOCK_SEEDS` is measured at -90,863),
which zeroes tomorrow's `wheat_buy` / `fert_bought`, and `ROUTE_FREEFIRST`'s
per-KIND block test then bases those blocks at `O.TURN_BUY`.  `route_base`,
`hire_wide_early`, the BANK/LOT ordering and `SELL_SLOT_PRIORITY`'s rows are
untouched.

OFF, the whole plan tuple is pinned against a pristine `git archive` of the
branch base, as `tests/test_route_freefirst.py` pins its own switch.
"""
from __future__ import annotations

import os
import subprocess
import sys

import _pin

_pin.bootstrap()

import numpy as np
from test_budget_order import _macro
from test_prestock_v2 import PIN_BOARDS, _case, _digest, _pass_turns, _row

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

#: The branch base: `master` bb695a2 (shipped FT2 + ROUTEEFF), which has no
#: `EVE_STOCK_ON` at all.  A SHA and not `HEAD`, so the pin keeps its meaning
#: once this branch is committed.
BASE = "bb695a2"


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _own_digests():
    return {cfg[0]: _digest(_plan(*_case(cfg))) for cfg in PIN_BOARDS}


def _base_digests():
    return _pin.tree_digests(__file__, ref=BASE)


def _bought_items(plan):
    """The item ids the day's own turn-1 BUY row delivers, `PICK_ITEM` space."""
    out = set()
    for turn in range(O.FULL_MARKET_TURNS):
        for op, arg, qty in _row(plan, turn):
            if qty <= 0:
                continue
            if op == O.MO_BUY_PRODUCT:
                out.add(int(arg))
            elif op == O.MO_BUY_ANIMAL:
                out.add(int(spec.I_GOOSE + arg))
    return out


# =========================================================================
# OFF: the shipped program, byte for byte
# =========================================================================

def test_the_switch_ships_off():
    assert P.EVE_STOCK_ON is False
    assert P.PRESTOCK_ON is False and P.PRESTOCK_V2_ON is False
    assert P.ROUTE_FREEFIRST_ON is False
    assert P.PRESTOCK_SEEDS is False          # the -90,863 half stays off


def test_the_base_tree_has_no_such_switch():
    """The pin's other end, named."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {BASE}:src/kagg3/core/plan.py", shell=True,
                         cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "EVE_STOCK_ON" not in src
    assert "\nROUTE_FREEFIRST_ON = False\n" in src


def test_off_plan_is_byte_identical_to_the_base_tree():
    """THE IDENTITY PIN: whole-plan sha256 against `git archive BASE src`."""
    assert _own_digests() == _base_digests()


def test_off_emits_no_row_at_the_prestock_turn():
    for cfg in PIN_BOARDS:
        assert _row(_plan(*_case(cfg)), O.TURN_PRESTOCK) == [], cfg[0]


# =========================================================================
# ON: tonight's row, and tomorrow's turn 1
# =========================================================================

def test_on_buys_tomorrows_pickups_tonight(monkeypatch):
    """The evening half: a BUY_PRODUCT row at `O.TURN_PRESTOCK`, of the kinds
    tomorrow's blocks will PICKUP (feed wheat, fertilizer) and nothing else --
    no seed, no animal, no land."""
    monkeypatch.setattr(P, "EVE_STOCK_ON", True)
    fired = 0
    for cfg in PIN_BOARDS:
        row = _row(_plan(*_case(cfg)), O.TURN_PRESTOCK)
        for op, arg, qty in row:
            assert op == O.MO_BUY_PRODUCT, (cfg[0], op)
            assert int(arg) in (spec.I_WHEAT, spec.I_FERT), (cfg[0], arg)
            assert qty > 0
        fired += bool(row)
    assert fired, "the evening row never fires on any pin board"


def test_on_bases_the_next_days_blocks_at_turn_1_with_the_items_held(monkeypatch):
    """The morning half, on the state an evening pre-buy leaves behind: the
    `stocked` board's shed holds 60 wheat and 20 fertilizer, so the day buys
    neither, its blocks owe only held kinds -- and they collect at `O.TURN_BUY`
    instead of `O.ROUTE_BASE`, which is the dawn PASS this switch is for."""
    view, macro = _case(PIN_BOARDS[3])
    off = _plan(view, macro)
    assert not (off[0][:, :O.ROUTE_BASE] == O.OP_PICKUP).any()
    monkeypatch.setattr(P, "EVE_STOCK_ON", True)
    on = _plan(view, macro)
    assert spec.I_WHEAT not in _bought_items(on) and spec.I_FERT not in _bought_items(on)
    assert (on[0][:, O.TURN_BUY] == O.OP_PICKUP).any(), "no block took turn 1"
    assert _pass_turns(on, 0, O.ROUTE_BASE - 1) < _pass_turns(off, 0, O.ROUTE_BASE - 1)


def test_on_moves_no_unit_in_front_of_a_row_it_depends_on(monkeypatch):
    """The safety property, on every pin board: a PICKUP below `O.ROUTE_BASE`
    must be of an item today's own market rows do not deliver, and nothing acts
    below the hire law's floor `O.TURN_BUY`."""
    monkeypatch.setattr(P, "EVE_STOCK_ON", True)
    for cfg in PIN_BOARDS:
        plan = _plan(*_case(cfg))
        bought = _bought_items(plan)
        unit_op, unit_a = plan[0], plan[1]
        for u in range(unit_op.shape[0]):
            for t in range(O.ROUTE_BASE):
                if int(unit_op[u, t]) == O.OP_PICKUP:
                    assert int(unit_a[u, t]) not in bought, (cfg[0], u, t)
        acting = np.argwhere(unit_op != O.OP_PASS)
        if len(acting):
            assert int(acting[:, 1].min()) >= O.TURN_BUY, cfg[0]


def test_on_leaves_the_sell_and_hire_rows_where_they_were(monkeypatch):
    """`route_base` and the market layout are untouched: every turn except
    `O.TURN_PRESTOCK` carries the same rows ON as OFF (BANK/LOT ordering and
    `SELL_SLOT_PRIORITY` intact), on a board whose blocks the switch moves."""
    view, macro = _case(PIN_BOARDS[3])
    off = _plan(view, macro)
    monkeypatch.setattr(P, "EVE_STOCK_ON", True)
    on = _plan(view, macro)
    for turn in range(spec.TURNS_PER_DAY):
        if turn == O.TURN_PRESTOCK:
            continue
        assert _row(off, turn) == _row(on, turn), turn


def test_the_switch_traces_under_jit(monkeypatch):
    """Both halves compile: caught here rather than ten minutes into a leg."""
    import jax
    import jax.numpy as jnp
    monkeypatch.setattr(P, "EVE_STOCK_ON", True)
    view, macro = _case(PIN_BOARDS[3])
    f = jax.jit(lambda v, m: P.build_day(jnp, v, m))
    out = f(jax.tree_util.tree_map(jnp.asarray, view),
            jax.tree_util.tree_map(jnp.asarray, macro))
    assert np.asarray(out[0]).shape == np.asarray(_plan(view, macro)[0]).shape


if __name__ == "__main__":                      # the BASE-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
