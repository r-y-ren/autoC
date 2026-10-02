"""`plan.SPREAD_ROWS_ON`: the day's voluntary sale, in per-tick bursts.

`docs/strategy/2026-09-16-pricevol.md` sect.4.3-4.4: the engine prices a SELL
order unit by unit and adds +1 to the shared inventory after every unit, so B's
9.73-unit burst forfeits 7,936 coins a game against the top five's 3.73-unit
burst and 2,554 -- and the town it pushes those bursts into eats 4.3 wheat /
3.5 strawberry / 2.5 milk / 1.8 wool units PER SHOP TICK.

This is the same day's volume cut over more rows: `spread_alloc` distributes the
VOLUNTARY allocation (the array `s_qty` is summed from, before a single bulk
add) over `spread_rows_turns()` at a per-product per-row cap, and `_market`
emits them. Volume, mix, the reservation gate and `s_qty` are untouched, so this
is not a re-schedule of whole lots (`docs/strategy/2026-09-10-consensus.md`
sect.85-90, the closed displacement-trade family) -- the pins below assert the
conservation directly.

OFF, `spread` is `None` and `_market` emits the rows it always emitted, so the
shipped program is unchanged: pinned below against a pristine
`git archive c5f68ac src` tree, whole-plan digests on five boards, exactly as
`tests/test_lot4.py` and `tests/test_crewpush.py` pin their own.
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


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0):
    """The `tests/test_lot4.py` / `tests/test_shed_deficit.py` fixture, so the
    three sell-row switches are measured on one board family."""
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


def _sell_macro():
    """`_macro()` holds everything (`hold` = 10,000), so its whole sale is the
    FORCED overflow and the voluntary allocation this switch reshapes is empty.
    A zero reservation is the board that actually exercises it."""
    return _macro(hold=np.zeros(spec.N_PRODUCTS, np.int32))


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


def _sell_grid(plan):
    """int[24, 9]: units of each product offered on each turn."""
    op, arg, qty = plan[3:6]
    g = np.zeros((op.shape[0], spec.N_PRODUCTS), np.int32)
    for t in range(op.shape[0]):
        for s in range(op.shape[1]):
            if op[t, s] == O.MO_SELL:
                g[t, arg[t, s]] += qty[t, s]
    return g


#: The `tests/test_lot4.py` set: one board that overflows (`hot`), one that does
#: not (`cool`), one already watered (`wet`), one with no plants (`bare`), one
#: with a town whose shops drain the shelf between the rows (`town`) -- which is
#: the only one whose per-tick cap is not 1, so it is the one that shows the
#: "tick" mode's cap actually binding.
PIN_BOARDS = (
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
    ("town", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
)
TOWN = dict(PIN_BOARDS)["town"]


#: `LOT4_ON` ships `True` at `LOT4_TURN = 17` (`docs/strategy/2026-09-16-lot4.md`,
#: POOLED180 +791 t 13.19, sub 56276165), and turn 17 is one of THIS switch's own
#: default rows -- so under the shipped four-lot day every ON case below trips
#: `plan._spread_check`'s collision guard ("spread row 17 collides with a row the
#: day already uses"). SPREAD6 was cut before that row existed and was REJECTED
#: without ever shipping (`docs/strategy/2026-09-16-pricevol.md`: -1,802 margin,
#: the sell-cadence family is closed), so its default row set is pinned to the
#: three-lot layout it was measured on rather than re-tuned; `tests/test_lot4.py`
#: owns the fourth row. The OFF-identity pin below re-states it, because that pin
#: hashes the SHIPPED tree on both sides.
@pytest.fixture(autouse=True)
def _lot4_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "LOT4_ON", False)     # turn 17 is a spread row here


def _own_digests():
    """Ten digests: the five boards under the held reservation (whose whole sale
    is the forced overflow) and under a zero one (whose whole sale is the
    voluntary allocation this switch reshapes) -- the pin has to cover both
    sides of the split `_plan_and_stats` makes."""
    out = {}
    for n, kw in PIN_BOARDS:
        out[n] = _digest(_plan(_view(**kw)))
        out[n + "_sell"] = _digest(_plan(_view(**kw), _sell_macro()))
    return out


def _head_digests():
    """The same five plans, built by a pristine `git archive c5f68ac src` tree in a
    subprocess -- the pin is the tree this switch was added to, not this file's
    own output."""
    return _pin.tree_digests(__file__, ref=_pin.SHIPPED)


# =========================================================================
# OFF: the shipped program, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.SPREAD_ROWS_ON is False
    assert P.SPREAD_ROWS_TURNS == (1, 5, 9, 13, 17, 21)
    assert P.SPREAD_ROWS_CAP_MODE == "tick"


def test_off_plan_is_byte_identical_to_head(monkeypatch):
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    monkeypatch.setattr(P, "LOT4_ON", True)      # both sides are the SHIPPED tree
    assert _own_digests() == _head_digests()


def test_off_leaves_the_sim_market_turns_alone():
    """`sim/rollout` reads the row set at import, after the runner has set the
    switches; OFF it must be the six turns it always resolved."""
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, 'src')\n"
         # the autouse fixture cannot reach a subprocess: state lot 4 off there too
         "from kagg3.core import plan as P; P.LOT4_ON = False\n"
         "from kagg3.sim import rollout as R; print(R.MARKET_TURNS)"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "(0, 1, 2, 3, 10, 18)"


# =========================================================================
# the row set and the cap
# =========================================================================

def test_the_rows_are_the_first_market_phase_after_each_shop_tick():
    """The whole point of the default layout: each row is quoted off a shelf
    exactly one shop tick thinner than the row before it."""
    ticks = [PJ.ticks_before(t)[0] for t in P.spread_rows_turns()]
    assert ticks == [1, 2, 3, 4, 5, 6]
    assert spec.SHOP_SELL_INTERVAL == 4


def test_turns_parse_from_a_dash_joined_string(monkeypatch):
    """A runner sweeps this on a COMMA-separated `--switches` line, so the
    tuple has to survive being written without commas."""
    monkeypatch.setattr(P, "SPREAD_ROWS_TURNS", "1-5-9-13")
    assert P.spread_rows_turns() == (1, 5, 9, 13)
    monkeypatch.setattr(P, "SPREAD_ROWS_TURNS", (5, 9))
    assert P.spread_rows_turns() == (5, 9)


def test_tick_cap_is_the_towns_own_per_tick_appetite():
    """"tick" mode's cap is `projector.town_tick_units` -- the pricevol sect.4.4
    column -- whenever the day's volume can actually FIT inside the rows at that
    width. Then it front-loads: each row takes what the town eats, and a small
    day finishes early."""
    shops = np.full(spec.N_SHOPS, 2, np.int32)
    n = len(P.spread_rows_turns())
    want = np.maximum(PJ.town_tick_units(np, shops), 1)
    qty = (want * n).astype(np.int32)                 # exactly fills the rows
    rows = P.spread_alloc(np, qty, shops)
    assert rows.shape == (n, spec.N_PRODUCTS)
    assert (rows == want[None, :]).all()
    # half the volume: the same cap, and the later rows stand empty
    rows = P.spread_alloc(np, (want * (n // 2)).astype(np.int32), shops)
    assert (rows[:n // 2] == want[None, :]).all()
    assert not rows[n // 2:].sum()


def test_tick_cap_never_dumps_a_tail_on_the_last_row():
    """A cap the volume cannot fit inside `n` rows does not spread the day, it
    dumps the residue on the LAST row of it -- which is `LOT4`'s turn-21 row,
    measured at band margin -831. Melon and fertilizer have no town bid at all
    (`spec.SHOP_CONSUME` columns 4 and 8 are zero on every shop), so they are
    the case that has to hold: the cap degrades to the equal share and the day
    is spread, not dumped."""
    shops = np.full(spec.N_SHOPS, 2, np.int32)
    n = len(P.spread_rows_turns())
    assert not PJ.town_tick_units(np, shops)[spec.I_MELON]
    assert not PJ.town_tick_units(np, shops)[spec.I_FERT]
    tick = np.maximum(PJ.town_tick_units(np, shops), 1)
    for total in (12, 60, 200):
        rows = P.spread_alloc(np, np.full(spec.N_PRODUCTS, total, np.int32), shops)
        eff = np.maximum(tick, -(-total // n))        # the cap the mode uses
        assert (rows.sum(axis=0) == total).all()
        # NO row exceeds the cap -- in particular the LAST one, which is where a
        # cap the volume cannot meet would pile the residue
        assert (rows <= eff[None, :]).all(), (total, rows)
        assert (rows[-1] <= eff).all(), (total, rows[-1])
        # the two no-bid products are spread, never stood on one row
        for p in (spec.I_MELON, spec.I_FERT):
            assert int(rows[:, p].max()) <= -(-total // n), (total, p, rows[:, p])


def test_every_unit_is_placed_and_the_last_row_takes_the_residue(monkeypatch):
    """Conservation is the whole safety argument: `LOT-DEPTH` measured a tight
    cap destroying units at the shed door, and the shed the residue would wait
    in is already at 99 % of its cap (`SHED-CLIP`)."""
    shops = np.full(spec.N_SHOPS, 1, np.int32)
    cap = np.maximum(PJ.town_tick_units(np, shops), 1)
    n = len(P.spread_rows_turns())
    for mode in ("tick", "equal"):
        monkeypatch.setattr(P, "SPREAD_ROWS_CAP_MODE", mode)
        for total in (0, 1, 7, 40, 250):
            qty = np.full(spec.N_PRODUCTS, total, np.int32)
            rows = P.spread_alloc(np, qty, shops)
            assert (rows.sum(axis=0) == qty).all(), (mode, total)
            assert (rows >= 0).all()
            if mode == "tick":
                eff = np.maximum(cap, -(-total // n))
                assert (rows <= eff[None, :]).all(), (mode, total)
            else:
                assert (rows <= -(-total // n)).all(), (mode, total)
                assert (rows >= total // n).all(), (mode, total)


def test_equal_mode_has_no_tail(monkeypatch):
    """The control arm: no row is more than one unit wider than another, on any
    volume -- so whatever "tick" buys or loses against it is the CAP and not the
    number of rows."""
    monkeypatch.setattr(P, "SPREAD_ROWS_CAP_MODE", "equal")
    shops = np.zeros(spec.N_SHOPS, np.int32)
    for total in (1, 5, 40, 97):
        rows = P.spread_alloc(np, np.full(spec.N_PRODUCTS, total, np.int32), shops)
        assert int(rows.max()) - int(rows.min()) <= 1, (total, rows[:, 0])
        assert int(rows.sum()) == total * spec.N_PRODUCTS


# =========================================================================
# ON: the rows exist, and the day is conserved
# =========================================================================

def test_on_emits_a_row_on_every_spread_turn(monkeypatch):
    """The rows land on the turns the switch names, and the merged row rides
    `EARLY_SELL`'s BUY-row turn rather than a row of its own."""
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    grid = _sell_grid(_plan(_view(**TOWN), _sell_macro()))
    live = {t for t in range(spec.TURNS_PER_DAY) if grid[t].sum()}
    assert live <= set(P.spread_rows_turns()) | set(P.early_lot_turns())
    # more than the shipped three-turn day, and every unit on a named row
    assert len(live) >= 4, live
    assert P.spread_merge_row() == 0
    assert O.EARLY_SELL_LOT1_TURN == 1


def test_on_sells_exactly_what_off_sells(monkeypatch):
    """Volume, product by product, ON == OFF: this is the claim that separates
    the switch from the closed re-schedule family. The reservation gate, the
    reserved feed wheat and fertilizer, the forced overflow and every bulk add
    are all upstream of the spread and see the numbers they always saw."""
    for _n, kw in PIN_BOARDS + (("d29", dict(day=29, n_wh=0, shed_wh=60,
                                             shed_to=38, shops=2)),):
        view = _view(**kw)
        for macro in (_macro(), _sell_macro()):
            monkeypatch.setattr(P, "SPREAD_ROWS_ON", False)
            off = _sell_grid(_plan(view, macro))
            monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
            on = _sell_grid(_plan(view, macro))
            assert (on.sum(axis=0) == off.sum(axis=0)).all(), \
                (kw, off.sum(0), on.sum(0))


def test_on_cuts_the_burst_down(monkeypatch):
    """The mechanism, on a board whose town drains the shelf between the rows:
    the deepest single (turn, product) burst of the day is strictly smaller."""
    view, macro = _view(**TOWN), _sell_macro()
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", False)
    off = _sell_grid(_plan(view, macro))
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    on = _sell_grid(_plan(view, macro))
    assert int(on.max()) < int(off.max()), (off.max(), on.max())
    assert int(on.sum()) == int(off.sum())
    assert int((on > 0).sum()) > int((off > 0).sum())      # more, smaller rows


def test_the_merged_row_falls_back_with_lot_1(monkeypatch):
    """Turn 1 is the BUY row: the spread row that stands there takes lot 1's
    seat in the `EARLY_SELL` merge, and a day whose purchases and sale cannot
    both fit the engine's ten slots sells it on `O.SELL_TURNS[0]` instead --
    which is why turn 3 keeps its fallback role and its BUY_LAND slot."""
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    op, _arg, qty = _plan(_view(**TOWN), _sell_macro())[3:6]
    on_one = int(qty[O.EARLY_SELL_LOT1_TURN][op[O.EARLY_SELL_LOT1_TURN]
                                             == O.MO_SELL].sum())
    on_three = int(qty[O.SELL_TURNS[0]][op[O.SELL_TURNS[0]] == O.MO_SELL].sum())
    assert on_one > 0 or on_three > 0
    # turn 3's tenth slot is still the day's BUY_LAND slot, never a SELL
    assert op[O.SELL_TURNS[0]][spec.MAX_MARKET_ORDERS - 1] != O.MO_SELL


def test_an_empty_shed_offers_nothing_on_any_spread_row(monkeypatch):
    """A row with nothing behind it keeps its slots `MO_NONE`, which is what
    both seats presenting an identical layout depends on."""
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    op, _arg, qty = _plan(_view(day=10, n_wh=0, shed_wh=0, shed_to=0),
                          _sell_macro())[3:6]
    for t in P.spread_rows_turns():
        if t == O.EARLY_SELL_LOT1_TURN:
            continue                      # the BUY row carries the purchases
        assert not (op[t] == O.MO_SELL).any(), t
        assert int(qty[t].sum()) == 0, t


def test_a_colliding_row_is_refused(monkeypatch):
    """Every row the day already owns is refused at trace time, not silently
    overwritten: a second write to a turn would eat the row already there."""
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    for bad in ((3, 9), (0, 9), (2, 9), (9, 18), (9, 9), (9, 5)):
        monkeypatch.setattr(P, "SPREAD_ROWS_TURNS", bad)
        with pytest.raises(AssertionError):
            _plan(_view(**TOWN), _sell_macro())


def test_the_early_variant_is_all_in_front_of_the_clone_dump(monkeypatch):
    """`(1, 5, 9, 13)` is the arm `LOT4` sect.2b's sign flip asks for: every row
    in front of the hour-17 dump the band tapes play."""
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    monkeypatch.setattr(P, "SPREAD_ROWS_TURNS", (1, 5, 9, 13))
    assert max(P.spread_rows_turns()) < 17
    view, macro = _view(**TOWN), _sell_macro()
    grid = _sell_grid(_plan(view, macro))
    assert not grid[17:].sum(), grid[17:]
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", False)
    off = _sell_grid(_plan(view, macro))
    assert (grid.sum(axis=0) == off.sum(axis=0)).all()


def test_on_adds_the_rows_to_the_sims_market_turns():
    """`sim/rollout` has to resolve the market on every turn the plan writes a
    row to, or the units are offered into a phase that never runs."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, 'src')\n"
         "from kagg3.core import plan as P; P.SPREAD_ROWS_ON = True\n"
         "from kagg3.sim import rollout as R; print(R.MARKET_TURNS)"],
        cwd=root, capture_output=True, text=True, check=True)
    got = eval(out.stdout.strip())
    assert set((1, 5, 9, 13, 17, 21)) <= set(got), got
    assert set((0, 1, 2, 3, 10, 18)) <= set(got), got


def test_a_land_day_can_keep_the_shipped_layout(monkeypatch):
    """`SPREAD_ROWS_SKIP_LAND_DAYS`: the day's BUY_LAND rides the spare tenth
    slot of `O.SELL_TURNS[0]` and is funded by lot 1's own turn-1 proceeds, so a
    turn-1 row cut to the town's per-tick appetite can leave the purse short at
    turn 3. With the knob on, a day that buys land sells exactly what OFF sells,
    on exactly the rows OFF sells it on; a day that does not is untouched by the
    knob."""
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    monkeypatch.setattr(P, "SPREAD_ROWS_SKIP_LAND_DAYS", True)
    # a day with money enough to buy land off a shed worth selling
    view = _view(day=6, money=60_000, n_wh=8, shed_wh=50, shed_to=45, shops=2,
                 nquad=1)
    plan = _plan(view, _sell_macro())
    op, _arg, qty = plan[3:6]
    land = (op == O.MO_BUY_LAND).any()
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", False)
    off = _sell_grid(_plan(view, _sell_macro()))
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    on = _sell_grid(plan)
    if land:
        assert (on == off).all(), (off.sum(0), on.sum(0))
    else:
        assert (on.sum(axis=0) == off.sum(axis=0)).all()
    # and the knob never changes the day's volume either way
    monkeypatch.setattr(P, "SPREAD_ROWS_SKIP_LAND_DAYS", False)
    plain = _sell_grid(_plan(view, _sell_macro()))
    assert (plain.sum(axis=0) == off.sum(axis=0)).all()


def test_the_kaggle_agent_renders_the_rows(monkeypatch):
    """The engine seat is not the sim: the packaged agent replays the hour-0
    plan through `kagg3.agent.render.turn_action`, which reads the same
    [24, 10] market arrays. The rows have to come out of THAT path at the hours
    the switch names, or the sim measures a schedule the ladder never plays."""
    from kagg3.agent import render as AR
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", True)
    plan = _plan(_view(**TOWN), _sell_macro())
    hours = {}
    for t in range(spec.TURNS_PER_DAY):
        sells = [o for o in AR.turn_action(plan, t, 0)["market"] if o[0] == "SELL"]
        if sells:
            hours[t] = sum(o[2] for o in sells)
    assert set(hours) <= set(P.spread_rows_turns()) | set(P.early_lot_turns()), hours
    assert len(hours) >= 4, hours
    monkeypatch.setattr(P, "SPREAD_ROWS_ON", False)
    off = _plan(_view(**TOWN), _sell_macro())
    off_h = {}
    for t in range(spec.TURNS_PER_DAY):
        sells = [o for o in AR.turn_action(off, t, 0)["market"] if o[0] == "SELL"]
        if sells:
            off_h[t] = sum(o[2] for o in sells)
    assert sum(hours.values()) == sum(off_h.values()), (off_h, hours)
    assert len(hours) > len(off_h), (off_h, hours)


if __name__ == "__main__":                      # the HEAD-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
