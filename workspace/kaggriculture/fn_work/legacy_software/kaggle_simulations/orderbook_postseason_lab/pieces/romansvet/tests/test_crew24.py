"""CREW24: EVENING_SEED_ON / H1_WORK_ON / H23_WATER_ON -- OFF 3-board parity vs master + one behaviour test each."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from test_prestock_v2 import PIN_BOARDS, _case, _pass_turns, _row
from kagg3 import spec
from kagg3.core import ops as O, plan as P

BASE = 'bc52a1f7'   # master at branch time (LATE_EXEC_ON=True shipped)
TGT = np.array([2, 1, 0, 0, 0], np.int32)


def _boards():
    return [('opening', _view(day=0, money=3_000)),
            ('mid', _view(day=15, money=20_000, nquad=3, n_wh=20)),
            ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]


def _plan(v, m=None):
    return tuple(np.asarray(a) for a in P.build_day(np, v, m or _macro(plant_target=TGT)))


def _own_digests():
    return {n: _pin.digest(_plan(v)) for n, v in _boards()}


def _pass_count(plan, lo, hi):
    uop = plan[0]
    return int(np.sum(uop[lo:hi] == O.OP_PASS)) if uop.ndim >= 2 else 0


def test_off_three_board_parity():
    assert P.EVENING_SEED_ON is False and P.H1_WORK_ON is False and P.H23_WATER_ON is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=BASE)


def test_evening_seed_row(monkeypatch):
    v = _view(day=15, money=20_000, nquad=3, n_wh=4)
    assert _row(_plan(v), O.TURN_PRESTOCK) == []
    monkeypatch.setattr(P, 'EVENING_SEED_ON', True)
    row = _row(_plan(v), O.TURN_PRESTOCK)
    assert row and all(op == O.MO_BUY_SEED for op, a, q in row), row
    assert sum(q for _, _, q in row) <= P.EVENING_SEED_MAX
    # outside the day window (d0 purse) nothing is bought
    assert _row(_plan(_view(day=0, money=3_000)), O.TURN_PRESTOCK) == []


def test_h1_work_held_stock_starts_at_hour1(monkeypatch):
    """`stocked` board: the shed already holds the day's feed and fertilizer, so
    blocks that collect them take hour 1 instead of PASSing it."""
    view, macro = _case(PIN_BOARDS[3])
    off = _pass_turns(_plan(view, macro), 0, 2)
    monkeypatch.setattr(P, 'H1_WORK_ON', True)
    on = _pass_turns(_plan(view, macro), 0, 2)
    assert on < off, (on, off)


def test_h23_water_admits_more_when_labour_bound(monkeypatch):
    """On a labour-bound admit stage (EST_LEAD raised so the credit binds) the
    +2 turns/unit admit more ranks and the crew works more turns; before
    `H23_WATER_DAY0` the plan is unchanged."""
    monkeypatch.setattr(P, 'EST_LEAD', 17)
    v = _view(day=15, money=20_000, nquad=4, n_wh=60)
    off = _plan(v)
    monkeypatch.setattr(P, 'H23_WATER_ON', True)
    on = _plan(v)
    work = lambda p: int(np.sum(p[0] != O.OP_PASS))
    assert work(on) > work(off), (work(on), work(off))
    monkeypatch.setattr(P, 'H23_WATER_DAY0', 16)
    assert _pin.digest(_plan(v)) == _pin.digest(off)


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
