"""`plan.SELL_SLOT_PRIORITY_ON`: the index of a SELL is a contested resource.

`docs/strategy/2026-09-16-v45-notebook.md` sect.2.4-2.5 and sect.4 item 1: the
engine quotes each unit of BOTH seats' same-index orders at the same inventory
and commits both, +1 inventory per unit sold, so within one turn's order list
the index of a SELL decides the quote it meets. The nine product slots of a
SELL row are a free permutation -- no new order, no new turn, no unit of volume
-- and this switch ranks them by the coins the row's own units lose if the
rival's batch lands in the pot first.

2026-09-16 -- THE SWITCH SHIPS ON, on top of the shipped `LOT4_ON` at turn 17
(`docs/strategy/2026-09-16-combo2.md`: the INCREMENT over `lot4t17` is POOLED180
+459 on 169 boards, se 63, t +7.31, 8 row flips for and 0 against -- sect.115b
PASS, where the standalone arm missed the +450 bar by 56 coins).

The pins therefore moved with the default, and both halves are kept:

* the SHIPPED (ON) plan is the pinned identity, against a pristine
  `git archive <PRE_SWITCH> src` tree -- the uploaded `lot4t17` commit, whose
  module default is still `False` -- with the switch set to `True` after import,
  i.e. the ship commit changed one constant and nothing else, and the shipped
  program is byte for byte the one `S/combo2` measured through the runner's
  post-import switch string;
* the OFF plan still equals that tree's OWN default, so the shipped `lot4t17`
  program is one `SELL_SLOT_PRIORITY_ON = False` away, unchanged.

Whole-plan digests on the five boards `tests/test_spread6.py` and
`tests/test_lot4.py` pin their own.
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

import contextlib

import numpy as np

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.sim import market

# `kagg3` FIRST, and only then `test_budget_order` -- which does its own
# `sys.path.insert(0, "src")` (`tests/test_budget_order.py:24`) and imports
# `kagg3` on the way in. Imported before the block above it would load THIS
# tree's planner into the `--digests` subprocess and the pins below would
# compare the tree with itself (`tests/test_lot4.py`, 2026-09-16).
from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0,
          opp_ripe=None):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield = z.copy(), z.copy(), z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = spec.I_WHEAT
    t_day[:n_wh] = day - age
    t_yield[:n_wh] = yld
    t_wat[:n_wh] = t_water
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = shed_wh
    shed[spec.I_TOMATO] = shed_to
    kw = {} if opp_ripe is None else {"opp_ripe": np.asarray(opp_ripe, np.int32)}
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, int(mkt_inv), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32), **kw)


def _sell_macro():
    return _macro(hold=np.zeros(spec.N_PRODUCTS, np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


PIN_BOARDS = (
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
    ("town", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
)


#: The commit the ship commit sits on: the uploaded `lot4t17` tree
#: (`LOT4_ON = True`, `LOT4_TURN = 17`) with `SELL_SLOT_PRIORITY_ON = False`.
#: A SHA and not `HEAD~1`, so the pin keeps its meaning after this branch is
#: fast-forwarded into `master` and master moves on.
PRE_SWITCH = "15e8e233a837eecd8c0fa71f5c62f6d1f29ee56c"


@contextlib.contextmanager
def _knob(on):
    """`plan.SELL_SLOT_PRIORITY_ON` set after import, which is exactly how every
    runner (`S/macro_exec/run.py`'s switch string, `S/combo2/run_all.sh`) set it
    for the measured legs."""
    was = P.SELL_SLOT_PRIORITY_ON
    P.SELL_SLOT_PRIORITY_ON = on
    try:
        yield
    finally:
        P.SELL_SLOT_PRIORITY_ON = was


def _digests():
    out = {}
    for n, kw in PIN_BOARDS:
        out[n] = _digest(_plan(_view(**kw)))
        out[n + "_sell"] = _digest(_plan(_view(**kw), _sell_macro()))
    return out


def _own_digests(on=None):
    """This tree's ten plans -- under the shipped default, or under the switch
    set after import."""
    if on is None:
        return _digests()
    with _knob(on):
        return _digests()


def _tree_digests(ref=PRE_SWITCH, on=None):
    """The same ten plans, built by a pristine `git archive <ref> src` tree in a
    subprocess -- the pin is a committed tree, not this file's own output.  The
    knob travels as an environment variable and is applied after that tree's
    import, so `ref`'s own module default is what is pinned when `on` is
    `None`."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = dict(os.environ)
    if on is not None:
        env["KAGG3_TEST_SLOTPRIO_ON"] = "1" if on else "0"
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {ref} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True, env=env)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


# =========================================================================
# THE SHIPPED PROGRAM: ON, byte for byte
# =========================================================================

def test_on_is_the_default():
    """2026-09-16: the switch ships, both halves, at the measured batch window."""
    assert P.SELL_SLOT_PRIORITY_ON is True
    assert P.SELL_SLOT_PRIORITY_SELLS_FIRST_ON is True
    assert (P.SELL_SLOT_PRIORITY_BATCH_MIN, P.SELL_SLOT_PRIORITY_BATCH_MAX) == (8, 24)
    assert P.sell_slot_exempt(O.EARLY_SELL_LOT1_TURN).all()


def test_the_pre_switch_tree_is_the_uploaded_lot4t17_tree():
    """The pin's other end, named: `PRE_SWITCH` really is the shipped `lot4t17`
    tree with this switch off, so the two digest pins below mean what they say."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {PRE_SWITCH}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "\nSELL_SLOT_PRIORITY_ON = False\n" in src
    assert "\nLOT4_ON = True\n" in src and "\nLOT4_TURN = 17\n" in src


def test_shipped_plan_is_the_pre_switch_tree_with_the_knob_set():
    """THE IDENTITY PIN. The whole plan tuple, hashed, against a pristine
    `git archive PRE_SWITCH src` tree whose `SELL_SLOT_PRIORITY_ON` is set to
    `True` after import -- which is how `S/combo2/run_all.sh` set it for the
    measured legs. Equal means the ship commit moved one constant and no
    behaviour, and that the +459 increment is a read of exactly this program."""
    assert _own_digests() == _tree_digests(on=True)


def test_off_plan_is_byte_identical_to_the_pre_switch_planner():
    """OFF is still the uploaded `lot4t17` program: this tree with the switch
    off against the pre-switch tree's OWN default."""
    assert _own_digests(on=False) == _tree_digests()


def test_off_view_default_is_an_empty_rival_farm():
    assert not np.asarray(_view().opp_ripe).any()


# =========================================================================
# the ranking
# =========================================================================

def test_score_is_the_revenue_a_rival_batch_takes_away():
    """`sum_j price(inv+j) - price(inv+batch+j)` over our own units, and the
    batch is the rival's ripe yield clamped to [MIN, MAX]."""
    pt = P.default_price_table()
    inv = np.full((1, spec.N_PRODUCTS), int(spec.MARKET_I0), np.int32)
    lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
    lots[0, spec.I_STRAWBERRY] = 5
    for ripe, want_batch in ((0, 8), (3, 8), (30, 24), (12, 12)):
        r = np.zeros(spec.N_PRODUCTS, np.int32)
        r[spec.I_STRAWBERRY] = ripe
        got = int(P.sell_slot_scores(np, pt, inv, lots, r)[0, spec.I_STRAWBERRY])
        i0 = int(spec.MARKET_I0) - spec.PRICE_TABLE_LO
        row = pt[spec.I_STRAWBERRY]
        want = int(sum(row[i0 + j] - row[i0 + want_batch + j] for j in range(5)))
        assert got == want, (ripe, got, want)
    # a product with no units in the row scores nothing
    assert not P.sell_slot_scores(np, pt, inv, lots, np.zeros(9, np.int32))[0].sum() \
        - int(P.sell_slot_scores(np, pt, inv, lots, np.zeros(9, np.int32))[0, spec.I_STRAWBERRY])


def test_perm_is_live_first_score_desc_then_product_index():
    lot = np.array([3, 0, 4, 2, 0, 0, 0, 0, 0], np.int32)
    sc = np.array([10, 99, 50, 10, 99, 0, 0, 0, 0], np.int32)
    perm = np.asarray(P.sell_slot_perm(np, lot, sc))
    # live: TOMATO(50) then WHEAT(10) then STRAWBERRY(10, higher index)
    assert list(perm[:3]) == [spec.I_TOMATO, spec.I_WHEAT, spec.I_STRAWBERRY]
    # the dead slots keep product order behind them, and it IS a permutation
    assert sorted(perm.tolist()) == list(range(spec.N_PRODUCTS))
    assert list(perm[3:]) == [1, 4, 5, 6, 7, 8]


def test_headline_value_is_not_the_rank():
    """The point of the mechanism: MELON at 250/u sits behind STRAWBERRY at
    120/u when only three melons are offered and the rival grows strawberry."""
    pt = P.default_price_table()
    inv = np.full((1, spec.N_PRODUCTS), int(spec.MARKET_I0), np.int32)
    lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
    lots[0, spec.I_MELON], lots[0, spec.I_STRAWBERRY] = 3, 5
    ripe = np.zeros(spec.N_PRODUCTS, np.int32)
    ripe[spec.I_STRAWBERRY] = 30
    sc = P.sell_slot_scores(np, pt, inv, lots, ripe)
    perm = np.asarray(P.sell_slot_perm(np, lots[0], sc[0]))
    assert perm[0] == spec.I_STRAWBERRY and perm[1] == spec.I_MELON
    assert BASE_PRICE[spec.I_MELON] > BASE_PRICE[spec.I_STRAWBERRY]


# =========================================================================
# ON: what actually moves
# =========================================================================

def _on(monkeypatch, **kw):
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", True)
    for k, v in kw.items():
        monkeypatch.setattr(P, k, v)


def _off(monkeypatch):
    """The shipped default is ON since 2026-09-16, so the OFF side of a
    comparison is the one that has to be asked for."""
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", False)


def _rows(plan):
    """{turn: [(product, qty), ...] in SLOT order} over every live market row."""
    op, arg, qty = plan[3:6]
    out = {}
    for t in range(op.shape[0]):
        r = [(int(op[t, s]), int(arg[t, s]), int(qty[t, s]))
             for s in range(op.shape[1]) if op[t, s] != O.MO_NONE]
        if r:
            out[t] = r
    return out


def test_on_moves_the_slots_but_not_one_unit_of_volume(monkeypatch):
    ripe = np.zeros(spec.N_PRODUCTS, np.int32)
    ripe[spec.I_TOMATO] = 30
    v = _view(day=10, n_wh=8, shed_wh=50, shed_to=45, opp_ripe=ripe)
    _off(monkeypatch)
    off = _plan(v, _sell_macro())
    _on(monkeypatch)
    on = _plan(v, _sell_macro())
    # every turn's multiset of (op, product, qty) is untouched
    ro, rn = _rows(off), _rows(on)
    assert set(ro) == set(rn)
    for t in ro:
        assert sorted(ro[t]) == sorted(rn[t]), t
    # and at least one SELL row is actually re-ordered
    assert any(ro[t] != rn[t] for t in ro)


def test_on_never_crosses_a_buy_of_the_same_item(monkeypatch):
    """Half (a) stops at a BUY of the same item: a day that buys wheat and
    sells wheat on the merged row keeps the shipped order."""
    _on(monkeypatch)
    for kw in (dict(day=10, n_wh=8, shed_wh=50, shed_to=45),
               dict(day=12, n_wh=0, shed_wh=60, shed_to=38),
               dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)):
        rows = _rows(_plan(_view(**kw), _sell_macro())).get(O.EARLY_SELL_LOT1_TURN, [])
        buys = {a for o, a, _ in rows if o == O.MO_BUY_PRODUCT}
        for i, (o, a, _q) in enumerate(rows):
            if o == O.MO_SELL and a in buys:
                j = [k for k, (o2, a2, _) in enumerate(rows)
                     if o2 == O.MO_BUY_PRODUCT and a2 == a][0]
                assert j < i, (kw, rows)


def test_on_takes_the_cross_exemption_and_nothing_wider(monkeypatch):
    _on(monkeypatch)
    assert P.sell_slot_exempt(O.EARLY_SELL_LOT1_TURN).all()
    for t in range(spec.TURNS_PER_DAY):
        if t != O.EARLY_SELL_LOT1_TURN:
            assert not P.sell_slot_exempt(t).any(), t
    _off(monkeypatch)
    assert not P.sell_slot_exempt(O.EARLY_SELL_LOT1_TURN).any()
    # a pure SELL row cannot cross at all, whatever the permutation
    op = np.array([[O.MO_SELL] * 4, [O.MO_SELL] * 4])
    arg = np.array([[3, 0, 2, 1], [0, 1, 2, 3]])
    market.assert_no_cross(op, arg)


def test_the_whole_switch_traces_under_jit():
    """`opp_ripe_yield` reads `spec.ANIMAL_PRODUCT` at PYTHON time: an
    `xp.asarray` of it makes `int(prod[a])` a tracer and the sim dies on the
    first day (`ConcretizationTypeError`, caught here rather than 10 minutes
    into a screen)."""
    import jax
    import jax.numpy as jnp
    kind = jnp.full(spec.N_TILES, spec.KIND_PLANT, jnp.int32)
    occ = jnp.zeros(spec.N_TILES, jnp.int32)
    y = jnp.full(spec.N_TILES, 3, jnp.int32)
    f = jax.jit(lambda k, o, t: P.opp_ripe_yield(jnp, k, o, t))
    assert int(np.asarray(f(kind, occ, y))[spec.I_WHEAT]) == 3 * spec.N_TILES
    pt = jnp.asarray(P.default_price_table())
    inv = jnp.full((3, spec.N_PRODUCTS), int(spec.MARKET_I0), jnp.int32)
    lots = jnp.zeros((3, spec.N_PRODUCTS), jnp.int32).at[0, 0].set(4)
    g = jax.jit(lambda i, l, r: P.sell_slot_perm(
        jnp, l[0], P.sell_slot_scores(jnp, pt, i, l, r)[0]))
    assert int(np.asarray(g(inv, lots, jnp.zeros(spec.N_PRODUCTS, jnp.int32)))[0]) == 0


if __name__ == "__main__":                # the pristine-tree subprocess
    # The knob arrives as an environment variable because this process imports
    # a DIFFERENT tree's `plan`, whose default is the one under test.
    if "KAGG3_TEST_SLOTPRIO_ON" in os.environ:
        P.SELL_SLOT_PRIORITY_ON = os.environ["KAGG3_TEST_SLOTPRIO_ON"] == "1"
    for _n, _d in _own_digests().items():
        print(_n, _d)
