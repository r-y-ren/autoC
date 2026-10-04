"""`plan.LOT4_ON`: a fourth afternoon sell row.

`SHED-CLIP` (2026-09-14) counted 21.6 units a game-seat destroyed at the shed
door under B's shipped switches, **15.4 of them at the nightly dump on days
14-28**; `SHED-DEFICIT` (same day) closed the two repairs that make the forced
sale *ask* for more (both draw on `spare = max(avail - s_qty, 0)`, which the
first pass has already drained) and ranked "a row AFTER the harvest lands"
first of what is left, bounded at the whole 1,272-coin band nightfall clip.

This is that row: `early_lot_turns()` gains `LOT4_TURN`, `n_lots()` follows it,
and `sell.allocate` reads its lot count off the projection it was handed.  Every
unit the day sells is a unit of room at the dump.

2026-09-16 -- THE SWITCH SHIPS ON, at `LOT4_TURN` = 17
(`docs/strategy/2026-09-16-brv45.md` sect.5: POOLED180 +791 on 169 boards,
se 60, t +13.19, sect.115b PASS).  Turn 17 stands immediately IN FRONT of lot 3,
not behind it, so the day's rows are `(3, 10, 17, 18)` and `n_lots() - 1` --
which every "day's LAST lot" bulk add names -- is still turn 18.

The pins therefore moved with the default, and both halves are kept:

* the SHIPPED (ON, 17) plan is the pinned identity, against a pristine
  `git archive <PRE_SWITCH> src` tree whose module defaults are still
  `(False, 21)` but whose two knobs are set to `(True, 17)` after import -- i.e.
  the ship commit changed the two constants and nothing else, and the shipped
  program is byte for byte the one the brv45 leg measured through the runner's
  post-import switch string;
* the OFF plan still equals that pre-switch tree's OWN defaults, so the
  three-lot program the champion theta was trained on is one `LOT4_ON = False`
  away, unchanged.

Whole-plan digests on five boards, exactly as `tests/test_shed_deficit.py` and
`tests/test_prestock_v2.py` pin their own.
"""
from __future__ import annotations

import contextlib
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

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import sell as SELL

# `kagg3` FIRST, and only then `test_budget_order` -- which does its own
# `sys.path.insert(0, "src")` (`tests/test_budget_order.py:24`) and imports
# `kagg3` on the way in. Imported before the block above it would load THIS
# tree's planner into the `--digests` subprocess and the pins below would
# compare the tree with itself. They silently did until 2026-09-16.
from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0):
    """`n_wh` wheat tiles of `age` days on a shed holding `shed_wh` wheat and
    `shed_to` tomato -- the `tests/test_shed_deficit.py` fixture, so the two
    switches are measured on one board family."""
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
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, int(mkt_inv), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def _sell_rows(plan):
    """{turn: units offered} over every SELL slot the day emits."""
    op, _arg, qty = plan[3:6]
    out = {}
    for t in range(op.shape[0]):
        n = int(qty[t][op[t] == O.MO_SELL].sum())
        if n:
            out[t] = n
    return out


def _sold(plan):
    return sum(_sell_rows(plan).values())


#: Four boards, the `test_shed_deficit.py` set: one that overflows (`hot`), one
#: that does not (`cool`), one already watered (`wet`), one with no plants
#: (`bare`).  `deficit`, the lot curves and the liquidation all read the shed,
#: so the pin needs every corner of it.
PIN_BOARDS = (
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
    ("town", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
)

#: A town with shops drains the shelf between the lots, so a later lot quotes
#: strictly above an earlier one and the allocator's choice of ROW is live.  On
#: a shopless board every lot quotes alike and `argmax` takes the earliest
#: (`sell.allocate`'s documented tie rule), which is why `hot` cannot show the
#: fourth row carrying anything and `TOWN` can.
TOWN = dict(PIN_BOARDS)["town"]


#: The commit the ship commit sits on: `LOT4_ON = False`, `LOT4_TURN = 21`,
#: i.e. the three-lot planner the champion theta `flow193_g100_hr` was trained
#: and uploaded on.  A SHA and not `HEAD~1`, so the pin keeps its meaning after
#: this branch is fast-forwarded into `master` and master moves on.
PRE_SWITCH = "39740890db98e66c2cbc9b890cbab92fb920427e"


@contextlib.contextmanager
def _knobs(lot4_on, lot4_turn):
    """`plan.LOT4_ON` / `LOT4_TURN` set after import, which is exactly how every
    runner (`S/macro_exec/run.py`'s switch string) set them for the measured
    legs."""
    was = (P.LOT4_ON, P.LOT4_TURN)
    P.LOT4_ON, P.LOT4_TURN = lot4_on, lot4_turn
    try:
        yield
    finally:
        P.LOT4_ON, P.LOT4_TURN = was


def _own_digests(lot4_on=None, lot4_turn=None):
    """This tree's five plans -- under the shipped defaults, or under knobs set
    after import."""
    if lot4_on is None and lot4_turn is None:
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    on = P.LOT4_ON if lot4_on is None else lot4_on
    turn = P.LOT4_TURN if lot4_turn is None else lot4_turn
    with _knobs(on, turn):
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _tree_digests(ref=PRE_SWITCH, lot4_on=None, lot4_turn=None):
    """The same five plans, built by a pristine `git archive <ref> src` tree in a
    subprocess -- the pin is a committed tree, not this file's own output.  The
    two knobs travel as environment variables and are applied after that tree's
    import, so `ref`'s own module defaults are what is pinned when both are
    `None`."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = dict(os.environ)
    if lot4_on is not None:
        env["KAGG3_TEST_LOT4_ON"] = "1" if lot4_on else "0"
    if lot4_turn is not None:
        env["KAGG3_TEST_LOT4_TURN"] = str(lot4_turn)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {ref} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True, env=env)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


# =========================================================================
# THE SHIPPED PROGRAM: ON at turn 17, character for character
# =========================================================================

def test_on_at_turn_17_is_the_default():
    """2026-09-16: the row ships. The merged tuple -- not an appended one -- is
    the whole point of 17, and `n_lots() - 1` still names turn 18."""
    assert P.LOT4_ON is True
    assert P.LOT4_TURN == 17
    assert P.early_lot_turns() == (3, 10, 17, 18) == tuple(
        sorted(tuple(O.SELL_TURNS) + (P.LOT4_TURN,)))
    assert P.n_lots() == 4 == SELL.N_LOTS + 1
    assert P.early_lot_turns()[P.n_lots() - 1] == O.SELL_TURNS[-1]


def test_the_pre_switch_tree_is_the_three_lot_planner():
    """The pin's other end, named: `PRE_SWITCH` really is the commit whose
    defaults are `(False, 21)`, so the two digest pins below mean what they
    say."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {PRE_SWITCH}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "\nLOT4_ON = False\n" in src
    assert "\nLOT4_TURN = 21\n" in src


def test_shipped_plan_is_the_pre_switch_tree_with_the_two_knobs_set():
    """THE IDENTITY PIN. The whole plan tuple, hashed, against a pristine
    `git archive PRE_SWITCH src` tree whose `LOT4_ON` / `LOT4_TURN` are set to
    the shipped values after import -- which is how `S/macro_exec/run.py` set
    them for every measured leg. Equal means the ship commit moved two
    constants and no behaviour, and that the +791 POOLED180 read is a read of
    exactly this program."""
    assert _own_digests() == _tree_digests(lot4_on=True, lot4_turn=17)


def test_off_plan_is_byte_identical_to_the_pre_switch_planner():
    """OFF is still the three-lot program the champion theta was trained on:
    this tree with `LOT4_ON = False` against the pre-switch tree's OWN
    defaults."""
    assert _own_digests(lot4_on=False) == _tree_digests()


def test_off_is_one_constant_away():
    assert P.early_lot_turns.__module__ == "kagg3.core.plan"
    with _knobs(False, P.LOT4_TURN):
        assert P.early_lot_turns() == tuple(O.SELL_TURNS)
        assert P.n_lots() == SELL.N_LOTS == len(O.SELL_TURNS)


# =========================================================================
# ON: one more row, in the afternoon, and legal
# =========================================================================

def test_the_fourth_turn_is_a_legal_afternoon_row(monkeypatch):
    """The layout invariants the module asserts at import, re-read through the
    switch: strictly increasing (the lot index IS the pressure rank), after the
    last shipped lot, inside the day, and colliding with no row the day already
    uses."""
    monkeypatch.setattr(P, "LOT4_ON", True)
    turns = P.early_lot_turns()
    assert turns == tuple(sorted(tuple(O.SELL_TURNS) + (P.LOT4_TURN,)))
    assert list(turns) == sorted(turns) and len(set(turns)) == len(turns)
    assert O.FULL_MARKET_TURNS <= P.LOT4_TURN < spec.TURNS_PER_DAY
    assert O.SELL_TURNS[0] < P.LOT4_TURN
    assert P.LOT4_TURN not in (set(O.SELL_TURNS) | set(O.MELON_LOT_TURNS)
                               | set(O.EARLY_SELL_LATE_TURNS)
                               | {O.TURN_PRESTOCK})
    assert P.n_lots() == 4


def test_a_swept_turn_is_merged_in_time_order(monkeypatch):
    """`LOT4_TURN` is a knob a runner sweeps off the command line, and the lot
    index IS the timing-pressure rank, so the tuple must stay sorted whatever
    the sweep sets -- and `n_lots() - 1`, which every "day's LAST lot" bulk add
    names, must still be the day's last row."""
    monkeypatch.setattr(P, "LOT4_ON", True)
    for turn in (13, 14, 17, 19, 21, 22, 23):
        monkeypatch.setattr(P, "LOT4_TURN", turn)
        turns = P.early_lot_turns()
        assert list(turns) == sorted(turns), turns
        assert set(turns) == set(O.SELL_TURNS) | {turn}
        assert turns[P.n_lots() - 1] == max(turns)


def test_on_emits_a_sell_row_on_the_fourth_turn(monkeypatch):
    """The row exists and it carries units.  On a town board the shelf drains
    between the lots, so a lot with MORE town ticks behind it quotes strictly
    above an earlier one and `allocate`'s `argmax` takes it; on a TIE the
    documented rule takes the EARLIEST row.  That is exactly why 17 is the
    shipped turn (`brv45` sect.5.1): `ticks_before(17) == ticks_before(18) == 5`,
    so the new row quotes level with lot 3 and wins the tie -- the same units,
    one turn earlier, in front of the day's deepest lot.  Swept to 21 (three
    more ticks) the same code quotes it strictly above and sells there instead.
    Either way the day's sale lands on `LOT4_TURN`."""
    view = _view(**TOWN)
    monkeypatch.setattr(P, "LOT4_ON", False)
    off = _sell_rows(_plan(view))
    assert max(off) == O.SELL_TURNS[-1], off
    monkeypatch.setattr(P, "LOT4_ON", True)
    on = _sell_rows(_plan(view))
    assert on.get(P.LOT4_TURN, 0) > 0, on
    assert max(on) == P.LOT4_TURN == 17, on
    assert sum(on.values()) == sum(off.values()), (off, on)
    assert set(on) <= set(O.SELL_TURNS) | {O.EARLY_SELL_LOT1_TURN, P.LOT4_TURN}
    monkeypatch.setattr(P, "LOT4_TURN", 21)
    late = _sell_rows(_plan(view))
    assert max(late) == 21 and late[21] > 0, late


def test_on_never_offers_more_than_the_dawn_shed(monkeypatch):
    """The fourth lot is another ROW, not another purse: `allocate` still stops
    at `avail`, so no non-terminal board offers more than the shed holds, and
    the extra row never *reduces* the day's sale below the three-lot one (a
    later, less-drained quote can only add units that clear `hold`)."""
    for shed_wh in (0, 10, 30, 50, 70, 94):
        for shed_to in (0, 5, 45):
            view = _view(day=10, n_wh=8, shed_wh=shed_wh, shed_to=shed_to)
            monkeypatch.setattr(P, "LOT4_ON", False)
            off = _sold(_plan(view))
            monkeypatch.setattr(P, "LOT4_ON", True)
            on = _sold(_plan(view))
            stock = shed_wh + shed_to
            assert on <= stock, (shed_wh, shed_to, on, stock)
            assert on >= off, (shed_wh, shed_to, off, on)


def test_terminal_liquidation_is_conserved_not_grown(monkeypatch):
    """Day 29's reservation is `SELL.LIQUIDATE`, so the whole shed goes out
    whatever the row count.  The fourth lot must therefore move volume, not
    create it: the same total, and no row deeper than the deepest OFF row."""
    for kw in (dict(day=29, n_wh=0, shed_wh=60, shed_to=38),
               dict(day=29, n_wh=0, shed_wh=60, shed_to=38, shops=2)):
        view = _view(**kw)
        monkeypatch.setattr(P, "LOT4_ON", False)
        off = _sell_rows(_plan(view))
        monkeypatch.setattr(P, "LOT4_ON", True)
        on = _sell_rows(_plan(view))
        assert sum(on.values()) == sum(off.values()) == 98, (kw, off, on)
        assert max(on.values()) <= max(off.values()), (kw, off, on)


def test_empty_shed_offers_nothing_on_the_new_row(monkeypatch):
    """A row with nothing behind it keeps its slots `MO_NONE`, which is what
    both seats presenting an identical layout depends on."""
    view = _view(day=10, n_wh=0, shed_wh=0, shed_to=0)
    monkeypatch.setattr(P, "LOT4_ON", True)
    plan = _plan(view)
    op, _arg, qty = plan[3:6]
    assert not (op[P.LOT4_TURN] == O.MO_SELL).any()
    assert int(qty[P.LOT4_TURN].sum()) == 0


def test_allocator_reads_its_lot_count_off_the_projection():
    """`sell.allocate`'s shape is the projection's, not `N_LOTS`': the switch is
    flipped after import, so a frozen constant would silently drop the row."""
    price = np.stack([np.arange(spec.PRICE_TABLE_N, 0, -1, np.int32)] * spec.N_PRODUCTS)
    mkt = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    shops = np.zeros(spec.N_SHOPS, np.int32)
    avail = np.full(spec.N_PRODUCTS, 5, np.int32)
    hold = np.zeros(spec.N_PRODUCTS, np.int32)
    press = np.zeros(spec.N_PRODUCTS, np.int32)
    for turns in (O.SELL_TURNS, tuple(O.SELL_TURNS) + (21,)):
        lots = SELL.allocate(np, price, mkt, shops, avail, hold, press,
                             turns=turns, rounds=8)
        assert lots.shape == (len(turns), spec.N_PRODUCTS)
        assert int(lots.sum()) == int(avail.sum())


if __name__ == "__main__":                # the pristine-tree subprocess
    # The knobs arrive as environment variables because this process imports a
    # DIFFERENT tree's `plan`, whose defaults are the ones under test.
    if "KAGG3_TEST_LOT4_ON" in os.environ:
        P.LOT4_ON = os.environ["KAGG3_TEST_LOT4_ON"] == "1"
    if "KAGG3_TEST_LOT4_TURN" in os.environ:
        P.LOT4_TURN = int(os.environ["KAGG3_TEST_LOT4_TURN"])
    for _n, _d in _own_digests().items():
        print(_n, _d)
