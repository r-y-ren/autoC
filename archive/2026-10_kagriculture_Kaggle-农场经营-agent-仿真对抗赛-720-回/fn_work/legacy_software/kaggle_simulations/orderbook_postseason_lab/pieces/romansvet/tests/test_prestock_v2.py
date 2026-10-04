"""`plan.PRESTOCK_V2_ON`: the prestock row, reconciled with turn 1's writers.

`PRESTOCK_ON` has never had a valid read on the shipped tree.  Two asserts
refuse it -- `assert not (EARLY_SELL_ON and (MARKET_PACK_ON or PRESTOCK_ON))`
at module scope and `assert hire_wide_early is None, "OPEN_PUMP owns turn 1"`
inside `_market` -- and every screen since 2026-09-10 crashed the seat at
import and recorded the 3,000-coin idle line as a -155k "read"
(`docs/strategy/2026-09-11-route-early-bug.md`).

Neither assert is about the purchase.  Both subjects are `hire_wide_early`,
the overflow HIRE row PRESTOCK moves into turn 1 -- and that row only ever
carries anything on a WIDE day (`rest = max(n_hire - MO, 0)`).  So V2 fires on
narrow days only and passes `hire_wide_early=None`: the purchase keeps
`O.TURN_PRESTOCK` = 20, a turn no other row uses, turn 1 keeps exactly the
writers it has today, and neither assert has a subject.  Nothing is deleted.

`PRESTOCK_V2_FARMER0_ON` is the second half: unit 0 is not hired, so the only
law holding it at turn 0 is spawn occupancy -- and a PICKUP does not step off
the shed-access tile.  A farmer whose block opens with a PICKUP takes it at
turn 0, which is the op `ymg_aq`'s hour-0 farmer issues against B's 100 % PASS
(`docs/strategy/2026-09-14-turns.md`).

OFF, both are the shipped program: pinned below against a pristine `git
archive HEAD src` tree, whole-plan digests on three boards.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

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

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_coop=0, n_ripe=0, wheat=0, fert=0, seeds=None,
          yld=4, nquad=1):
    """`tests/test_prestock.py`'s board, unchanged: `n_coop` hungry geese, then
    `n_ripe` ripe tomatoes, then empty tiles for whatever the macro wants."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    t_yield = z.copy()
    kind[:n_coop] = spec.KIND_COOP
    occ[:n_coop] = 0
    t_cons[:n_coop] = 1
    hi = n_coop + n_ripe
    kind[n_coop:hi] = spec.KIND_PLANT
    occ[n_coop:hi] = spec.I_TOMATO
    t_yield[n_coop:hi] = yld
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    shed[spec.I_FERT] = fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32) if seeds is None
        else np.asarray(seeds, np.int32),
        money=np.int32(money), nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _row(plan, turn):
    op, arg, qty = plan[3:6]
    return [(int(op[turn, s]), int(arg[turn, s]), int(qty[turn, s]))
            for s in range(spec.MAX_MARKET_ORDERS) if int(op[turn, s]) != O.MO_NONE]


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def _pass_turns(plan, lo, hi):
    """Unit-turns spent on PASS in turns [lo, hi], over the units that act."""
    unit_op = plan[0]
    acts = (unit_op != O.OP_PASS).any(axis=1)
    return int((unit_op[acts, lo:hi + 1] == O.OP_PASS).sum())


#: Three boards, `tests/test_prestock.py`'s own: a planting day, a feeding day,
#: and a day that does both against a shed with room to spare.  Plus one narrow
#: day whose residual BUY row a full shed empties -- V2's own subject.
PIN_BOARDS = (
    ("plant", dict(day=10, money=20_000), dict(plant_target=[4, 0, 0, 0, 0])),
    ("feed", dict(day=10, money=20_000, n_coop=12, wheat=4), {}),
    ("mixed", dict(day=14, money=20_000, n_coop=6, n_ripe=4, wheat=2, fert=3),
     dict(plant_target=[2, 1, 0, 0, 0])),
    ("stocked", dict(day=12, money=20_000, n_coop=8, n_ripe=4, wheat=60, fert=20),
     {}),
)


def _case(cfg):
    board, kw = cfg[1], dict(cfg[2])
    if "plant_target" in kw:
        kw["plant_target"] = np.asarray(kw["plant_target"], np.int32)
    return _view(**board), _macro(**kw)


def _head_digests():
    """The same four plans, built by a pristine `git archive c5f68ac src` tree in
    a subprocess.  The pin is the tree this switch was added to and not this
    file's own output, which is the only form of "OFF is character-identical"
    worth asserting."""
    return _pin.tree_digests(__file__, ref=_pin.SHIPPED)


def _own_digests():
    return {cfg[0]: _digest(_plan(*_case(cfg))) for cfg in PIN_BOARDS}


# =========================================================================
# OFF: the shipped program, character for character
# =========================================================================

def test_off_emits_nothing_at_the_prestock_turn():
    assert (P.PRESTOCK_V2_ON, P.PRESTOCK_V2_FARMER0_ON) == (False, False)
    for cfg in PIN_BOARDS:
        assert _row(_plan(*_case(cfg)), O.TURN_PRESTOCK) == [], cfg[0]


def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    assert _own_digests() == _head_digests()


def test_off_keeps_the_morning_schedule():
    """Hires at turns 0 and 2, the BUY row at turn 1, no unit before
    `O.TURN_BUY` (`ROUTE_SPLIT_ON`, on by default, owns that one turn)."""
    for cfg in PIN_BOARDS:
        plan = _plan(*_case(cfg))
        assert all(o == O.MO_HIRE for o, _, _ in _row(plan, O.TURN_HIRE)), cfg[0]
        assert all(o != O.MO_HIRE for o, _, _ in _row(plan, O.TURN_BUY)), cfg[0]
        acting = np.argwhere(plan[0] != O.OP_PASS)
        if len(acting):
            assert int(acting[:, 1].min()) >= O.TURN_BUY, cfg[0]


# =========================================================================
# ON: the row tonight, the turn tomorrow
# =========================================================================

def test_on_runs_beside_early_sell_and_open_pump(monkeypatch):
    """The point of the switch.  `EARLY_SELL_ON` and `OPEN_PUMP_ON` are the
    shipped defaults; `PRESTOCK_ON` raises at import beside the first and at
    trace time beside the second.  V2 does neither, and leaves turn 1 to its
    existing writers: no HIRE lands there."""
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    monkeypatch.setattr(P, "PRESTOCK_V2_ON", True)
    monkeypatch.setattr(P, "PRESTOCK_V2_FARMER0_ON", True)
    for cfg in PIN_BOARDS:
        plan = _plan(*_case(cfg))
        assert all(o != O.MO_HIRE for o, _, _ in _row(plan, O.TURN_BUY)), cfg[0]
    view, macro = _case(PIN_BOARDS[1])
    row = _row(_plan(view, macro), O.TURN_PRESTOCK)
    bought = {arg: qty for op, arg, qty in row if op == O.MO_BUY_PRODUCT}
    assert bought.get(spec.I_WHEAT, 0) > 0, row
    assert all(op != O.MO_BUY_SEED for op, _, _ in row), row


def test_on_drops_the_hour_0_1_pass_turns(monkeypatch):
    """The measurement the switch exists for: on a day whose residual BUY row
    is empty the crew starts at `ops.ROUTE_BASE_PRE`, so the morning wait
    shrinks.  Counted over turns 0-1 on the `stocked` board, whose shed already
    holds the feed and fertilizer the day wants."""
    view, macro = _case(PIN_BOARDS[3])
    off = _pass_turns(_plan(view, macro), 0, 1)
    monkeypatch.setattr(P, "PRESTOCK_V2_ON", True)
    on = _pass_turns(_plan(view, macro), 0, 1)
    monkeypatch.setattr(P, "PRESTOCK_V2_FARMER0_ON", True)
    on_f = _pass_turns(_plan(view, macro), 0, 1)
    assert on < off, (off, on)
    assert on_f <= on, (on, on_f)


def test_on_never_spends_past_the_purse(monkeypatch):
    """The prestock row is funded from `Prefix.purse_left`, a purse already net
    of the hire bill and `cash_reserve`, so its cost can never exceed the day's
    own money -- the reserve cannot be breached and a short purse buys a prefix
    of the want rather than nothing."""
    monkeypatch.setattr(P, "PRESTOCK_V2_ON", True)
    table = np.asarray(P.default_price_table())
    for money in (0, 120, 600, 3_000, 20_000):
        view = _view(day=12, money=money, n_coop=10, n_ripe=4, wheat=1, fert=0)
        plan = _plan(view, _macro())
        quotes = PJ.buy_quotes(
            np, table,
            PJ.projected_inv(np, view.mkt_inv, view.shops, O.TURN_PRESTOCK,
                             view.day))
        cost = 0
        for op, arg, qty in _row(plan, O.TURN_PRESTOCK):
            assert op == O.MO_BUY_PRODUCT, (op, arg, qty)
            cost += int(np.cumsum(quotes[arg])[min(qty, PJ.K) - 1])
        assert cost <= int(money), (money, cost)


if __name__ == "__main__":                      # the HEAD-tree subprocess
    pass  # the path was chosen at the top of the file
    for _n, _d in _own_digests().items():
        print(_n, _d)
