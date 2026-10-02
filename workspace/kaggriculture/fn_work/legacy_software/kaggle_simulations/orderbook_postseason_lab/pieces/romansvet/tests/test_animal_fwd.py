"""`plan.ANIMAL_BUY_FWD_ON`: the animal-acquisition bound `ub_coins` prices the
animal's product on the sales-window curve its units are actually sold on,
instead of the spot quote of the day it is bought.

WOOL is the product the switch is an argument about: `above_func "sq"`,
`above_target 3.20`, `T 105`, so the town's wool pot floors at PRICE_FLOOR after
~59 net units across BOTH seats, and a herd committed on a 190-coin quote sells
into a 1-coin one.  See `docs/strategy/2026-09-16-woolprice.md`.

THE SWITCH SHIPS OFF unless that document's legs say otherwise.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, sys.argv[sys.argv.index("--digests") + 1]
                if "--digests" in sys.argv else "src")

import contextlib

import numpy as np

from kagg3 import spec
from kagg3.core import plan as P

# `kagg3` FIRST, and only then `test_budget_order` -- which does its own
# `sys.path.insert(0, "src")`, so imported above it the `--digests` subprocess
# would load THIS tree's planner and the pins would compare the tree with
# itself (`tests/test_lot4.py`, 2026-09-16).
from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=8, money=20_000, n_wh=6, n_past=2, n_sheep=0, nquad=2, shops=0,
          wool_inv=0, wool_price=None, shed_sheep=0):
    """A board with wheat (the feed), free pasture to place on, and a wool
    market whose inventory the caller sets.  `wool_inv` is units ABOVE
    `MARKET_I0`; `wool_price` defaults to the engine quote at that inventory."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_yield = z.copy(), z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = spec.I_WHEAT
    t_day[:n_wh] = day - 4
    t_yield[:n_wh] = 2
    kind[n_wh:n_wh + n_past] = spec.KIND_PASTURE
    kind[n_wh + n_past:n_wh + n_past + n_sheep] = spec.KIND_PASTURE
    occ[n_wh + n_past:n_wh + n_past + n_sheep] = 2   # bare animal index (SHEEP)
    t_day[n_wh + n_past:n_wh + n_past + n_sheep] = day - 3
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = 40
    shed[spec.I_SHEEP] = shed_sheep
    inv = np.full(spec.N_PRODUCTS, int(spec.MARKET_I0), np.int32)
    inv[spec.I_WOOL] = spec.MARKET_I0 + int(wool_inv)
    price = BASE_PRICE.copy()
    price[spec.I_WOOL] = int(_quote(int(wool_inv)) if wool_price is None else wool_price)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=price, mkt_inv=inv,
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


def _quote(units_over):
    """The engine's WOOL quote at `MARKET_I0 + units_over` -- `market_price`
    with `above_func "sq"`, `above_target 3.20`, `T 105`, floored at 1."""
    amp = 3.20 * 200 / (105.0 ** 2)
    return max(1, int(round(200 - amp * max(0.0, units_over) ** 2)))


def _buy_macro():
    """A macro that ASKS for sheep, so `acquire_ok` and the marginal-unit
    budget are the things deciding, not a zero want."""
    return _macro(animal_want=np.array([0, 0, 2], np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _buy_macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


PIN_BOARDS = (
    ("clean", dict(day=8, wool_inv=0)),
    ("half", dict(day=10, wool_inv=30)),
    ("deep", dict(day=12, wool_inv=50)),
    ("floored", dict(day=17, wool_inv=59)),
    ("herd", dict(day=12, wool_inv=40, n_sheep=5)),
    ("terminal", dict(day=29, wool_inv=59, n_sheep=5)),
)

#: The commit this branch sits on -- master's shipped pair, whose planner has no
#: `ANIMAL_BUY_FWD_ON` at all.  A SHA and not `HEAD~1`, so the pin keeps its
#: meaning after the branch is merged and master moves on.
PRE_SWITCH = "aed911c"


@contextlib.contextmanager
def _knob(on=True):
    was = P.ANIMAL_BUY_FWD_ON
    P.ANIMAL_BUY_FWD_ON = on
    try:
        yield
    finally:
        P.ANIMAL_BUY_FWD_ON = was


def _digests():
    return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _tree_digests(ref=PRE_SWITCH):
    """The same plans built by a pristine `git archive <ref> src` tree in a
    subprocess -- the pin is a committed tree, not this file's own output."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {ref} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


def _bought(plan, item):
    """Units of one item the day's market rows BUY."""
    from kagg3.core import ops as O
    op, arg, qty = plan[3], plan[4], plan[5]
    m = ((np.asarray(op) == O.MO_BUY_ANIMAL) & (np.asarray(arg) == item))
    return int(np.asarray(qty)[m].sum())


# =========================================================================
# OFF is master, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.ANIMAL_BUY_FWD_ON is False


def test_off_plan_is_byte_identical_to_master():
    """The whole-plan digest of six boards against a pristine master tree."""
    assert _digests() == _tree_digests()


def test_an_undrained_market_is_the_off_plan():
    """The switch is a `min` against the spot quote, so on a board whose
    sales-window curve is at or above spot the ON plan must re-evaluate to the
    OFF one -- the property that makes it a ceiling and not a second
    mechanism.  A day-0 board with an empty farm has no pipeline and a market
    at `I0`, where the forward quote is the scarcity side of the curve."""
    v = _view(day=0, n_wh=0, n_past=2, wool_inv=-40)
    off = _digest(_plan(v))
    with _knob():
        assert _digest(_plan(v)) == off


def test_on_never_raises_the_bound():
    """`ub_coins` is a `min` on the product term, so ON can only ever refuse an
    animal OFF would have bought, never the reverse."""
    for n, kw in PIN_BOARDS:
        v = _view(**kw)
        off = _bought(_plan(v), 2)
        with _knob():
            on = _bought(_plan(v), 2)
        assert on <= off, (n, off, on)


if "--digests" in sys.argv:
    for _n, _d in _digests().items():
        print(_n, _d)
