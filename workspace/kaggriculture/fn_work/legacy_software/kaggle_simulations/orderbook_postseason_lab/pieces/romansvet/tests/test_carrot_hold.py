"""`plan.CARROT_EARLY_HOLD_ON`: a reservation floor under the d0-14 carrot lot.

`TOMATO15` (`docs/strategy/2026-09-16-tomato15.md` sect.2): B sells its CARROT
in two blocks priced 18-24 coins a unit apart on every opponent class -- 25-26
units at 33.0-33.5 in d0-9 against a 35 base, and 67-96 units at 51.5-56.9 in
d15-29 -- and the archive line that closed the two carrot *tile* arms left the
sell side explicitly open (`docs/strategy/2026-09-09-verdicts.txt:499`, "Tile
count closed; carrot sell-timing still open").  ON, the carrot entry of the
day's reservation is floored at `NUM/DEN` of this game's own carrot base until
`CARROT_EARLY_HOLD_DAY`; nothing else moves -- not a tile, not a seed, not the
crew, not the mix.

OFF, `_sell_hold` returns its argument untouched and builds no array, so the
champion theta decodes byte for byte: pinned below against a pristine
`git archive c5f68ac src` tree, whole-plan digests on five boards, exactly as
`tests/test_crewpush.py` and `tests/test_lot4.py` pin their own.
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
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=6, money=3_000, n_wh=6, age=4, shed_ca=30, shed_wh=0, yld=4,
          nquad=1, shops=0, mkt_inv=spec.MARKET_I0):
    """The `tests/test_crewpush.py` board with CARROT in the shed: the sale
    side is what this switch touches, so the fixture has to hand the day a
    carrot lot to refuse."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield = z.copy(), z.copy(), z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = spec.I_WHEAT
    t_day[:n_wh] = day - age
    t_yield[:n_wh] = yld
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_CARROT] = shed_ca
    shed[spec.I_WHEAT] = shed_wh
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


def _sold(plan, item):
    """Units of `item` the day's whole plan commits to the market."""
    op, arg, qty = plan[3], plan[4], plan[5]
    return int(qty[(op == O.MO_SELL) & (arg == item)].sum())


#: A selling macro: the shipped fixture holds everything at 10,000, which would
#: make every board inert for a reservation switch. Zero reservation on every
#: product is the hardest case for a floor -- it has nothing to hide behind.
def _sell_macro(**kw):
    kw.setdefault("hold", np.zeros(spec.N_PRODUCTS, np.int32))
    return _macro(**kw)


#: Five boards that reach the sale from both sides: an early day with a carrot
#: lot (`early`), the same board on the release day (`release`), the terminal
#: day whose law must survive the floor (`terminal`), a board with no carrot at
#: all (`nocarrot`, where the switch must be inert by construction), and a rich
#: late day that also sells wheat (`late`).
PIN_BOARDS = (
    ("early", dict(day=6, shed_ca=30), {}),
    ("release", dict(day=15, shed_ca=30), {}),
    ("terminal", dict(day=29, shed_ca=30, money=60_000), {}),
    ("nocarrot", dict(day=6, shed_ca=0, shed_wh=40), {}),
    ("late", dict(day=20, shed_ca=24, shed_wh=30, money=25_000, shops=2), {}),
)


def _own_digests():
    return {n: _digest(_plan(_view(**kw), _sell_macro(**mk)))
            for n, kw, mk in PIN_BOARDS}


def _head_digests():
    """The same five plans, built by a pristine `git archive c5f68ac src` tree in a
    subprocess -- the pin is the tree this switch was added to, not this file's
    own output."""
    return _pin.tree_digests(__file__, ref=_pin.SHIPPED)


# =========================================================================
# OFF: the shipped program, character for character
# =========================================================================

def test_off_is_the_default():
    assert P.CARROT_EARLY_HOLD_ON is False
    assert P.CARROT_EARLY_HOLD_DAY == 15
    assert P.CARROT_EARLY_HOLD_NUM > P.CARROT_EARLY_HOLD_DEN > 0


def test_off_sell_hold_returns_the_same_object():
    """Not merely equal: the OFF path must not build an array at all, which is
    what makes the digest pin below a statement about the program and not about
    numpy's arithmetic."""
    pt = np.asarray(P.default_price_table())
    hold = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    for day in (0, 6, 14, 15, 29):
        out = P._sell_hold(np, pt, hold, np.bool_(False), day=day)
        assert out is hold


def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, on five boards, against a pristine HEAD
    tree -- the `day=` keyword added to `_sell_hold` must not move a coin."""
    assert _own_digests() == _head_digests()


# =========================================================================
# ON: what the floor does
# =========================================================================

def test_on_floors_only_carrot_and_only_before_the_day(monkeypatch):
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    pt = np.asarray(P.default_price_table())
    base = int(pt[spec.I_CARROT, P._I0_COL])
    floor = (base * P.CARROT_EARLY_HOLD_NUM) // P.CARROT_EARLY_HOLD_DEN
    hold = np.zeros(spec.N_PRODUCTS, np.int32)
    for day in range(0, P.CARROT_EARLY_HOLD_DAY):
        out = np.asarray(P._sell_hold(np, pt, hold, np.bool_(False), day=day))
        assert int(out[spec.I_CARROT]) == floor, day
        assert (np.delete(out, spec.I_CARROT) == 0).all(), day
    for day in (P.CARROT_EARLY_HOLD_DAY, 20, 29):
        out = np.asarray(P._sell_hold(np, pt, hold, np.bool_(False), day=day))
        assert (out == hold).all(), day


def test_on_never_raises_a_reservation_the_decode_set_higher(monkeypatch):
    """A floor, not a setting: a theta that already reserves carrot above it
    keeps its own number."""
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    pt = np.asarray(P.default_price_table())
    hold = np.full(spec.N_PRODUCTS, 9_999, np.int32)
    out = np.asarray(P._sell_hold(np, pt, hold, np.bool_(False), day=3))
    assert (out == hold).all()


def test_on_is_void_on_the_terminal_day(monkeypatch):
    """[LAW, 0.4] day 29 sells whatever the reservation says; the floor may not
    strand a unit there. The terminal flag, not the day number, is the gate --
    `CARROT_EARLY_HOLD_DAY` could be set past 29 by a sweep."""
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_DAY", 30)
    pt = np.asarray(P.default_price_table())
    hold = np.zeros(spec.N_PRODUCTS, np.int32)
    out = np.asarray(P._sell_hold(np, pt, hold, np.bool_(True), day=29))
    assert (out == hold).all()


def test_on_refuses_the_early_carrot_lot_and_releases_it_after(monkeypatch):
    """The whole plan, not the helper: an early day that sells carrot OFF sells
    none ON, and the release day sells exactly what it sold OFF."""
    early, release = _view(day=6, shed_ca=30), _view(day=15, shed_ca=30)
    off_early = _sold(_plan(early, _sell_macro()), spec.I_CARROT)
    off_release = _sold(_plan(release, _sell_macro()), spec.I_CARROT)
    assert off_early > 0 and off_release > 0          # the fixture has to bind
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    assert _sold(_plan(early, _sell_macro()), spec.I_CARROT) == 0
    assert _sold(_plan(release, _sell_macro()), spec.I_CARROT) == off_release


def test_on_leaves_every_other_product_alone(monkeypatch):
    """The floor is one entry of `hold`: the same early board's wheat lot is
    the lot it was OFF."""
    v = _view(day=6, shed_ca=30, shed_wh=40)
    off = _sold(_plan(v, _sell_macro()), spec.I_WHEAT)
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    assert _sold(_plan(v, _sell_macro()), spec.I_WHEAT) == off


def test_on_is_inert_with_no_carrot_to_hold(monkeypatch):
    """No carrot in the shed: the plan is the OFF plan to the byte, so a board
    the switch cannot reach cannot be charged for it."""
    v = _view(day=6, shed_ca=0, shed_wh=40)
    off = _digest(_plan(v, _sell_macro()))
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    assert _digest(_plan(v, _sell_macro())) == off


def test_the_floor_is_this_game_s_own_base_not_the_default(monkeypatch):
    """Read off the price table for the reason `FERT_FLOOR` reads it there:
    under the training randomisation (`spec.sample_market_params`) the base
    moves, and a floor pinned to `spec.DEFAULT_MARKET_PARAMS` would bind at the
    wrong quote."""
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    pt = np.array(P.default_price_table(), np.int32)
    pt[spec.I_CARROT, :] = pt[spec.I_CARROT, :] * 2
    hold = np.zeros(spec.N_PRODUCTS, np.int32)
    out = np.asarray(P._sell_hold(np, pt, hold, np.bool_(False), day=3))
    base2 = int(pt[spec.I_CARROT, P._I0_COL])
    assert int(out[spec.I_CARROT]) == (base2 * P.CARROT_EARLY_HOLD_NUM
                                       ) // P.CARROT_EARLY_HOLD_DEN


def test_fert_floor_still_works_beside_it(monkeypatch):
    """The two floors share one helper; turning either on must not disturb the
    other's entry."""
    pt = np.asarray(P.default_price_table())
    hold = np.zeros(spec.N_PRODUCTS, np.int32)
    monkeypatch.setattr(P, "FERT_FLOOR_ON", True)
    only_fert = np.asarray(P._sell_hold(np, pt, hold, np.bool_(False), day=3))
    assert int(only_fert[spec.I_FERT]) > 0
    assert int(only_fert[spec.I_CARROT]) == 0
    monkeypatch.setattr(P, "CARROT_EARLY_HOLD_ON", True)
    both = np.asarray(P._sell_hold(np, pt, hold, np.bool_(False), day=3))
    assert int(both[spec.I_FERT]) == int(only_fert[spec.I_FERT])
    assert int(both[spec.I_CARROT]) > 0


if __name__ == "__main__":                      # the HEAD-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
