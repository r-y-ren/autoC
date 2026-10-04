"""`plan.ENDGAME_TOMATO_ON`: plant the town's tomato lottery.

The finding, measured on the real engine (2026-09-04, flow58_g450,
`scratchpad/tomato/`). Endgame prices are set by which shops the town's
lottery drew, not by the board: PIZZA_SHOP and FARMERS_MARKET both buy TOMATO
and every shop drains the shared market every four steps. TOMATO's below-`I0`
curve is the only crop's that is a *hinge*, so a town with two tomato buyers
walks 60 -> 181 by day 28 while MELON collapses to 4-28. The theta reads the
price and not the shop list, so it plants its first tomato on day 16 and its
eighteenth on day 22 -- off the tail of the curve. The shop counts are in the
observation from the day they unlock, so the trigger is a fact the day already
holds.

The switch moves the *mix* and nothing else: the tiles the day plants do not
change, only what goes in them, exactly as `_wheat_mix` moves a share and
`_melon_open` moves the opening's.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests -- the planner at `a838700`, the same pin `test_same_day_fert.py`,
`test_midday_place.py` and `test_open_pump.py` use.
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
from test_route_early import (
    PIN,
    PIN_SEEDS,
    _digest,
    _plan,
    _row,
    _seeded_case,
)
from test_route_early import _view as _base_view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

#: The stack `test_route_early`'s digests were taken before -- the planner at
#: `a838700`. None of these five answers anything about the day's crop mix, and
#: pinning them off is what makes the identity claim this switch's own.
_PINNED_OFF = ("ROUTE_SPLIT_ON", "SURVIVAL_WATER_ON", "TAIL_CARE_ON",
               "FEED_MANDATORY_ON", "EARLY_SELL_ON")

_I_PIZZA = spec.SHOP_NAMES.index("PIZZA_SHOP")
_I_MARKET = spec.SHOP_NAMES.index("FARMERS_MARKET")
_I_BRUNCH = spec.SHOP_NAMES.index("BRUNCH_SPOT")
_I_SMOOTHIE = spec.SHOP_NAMES.index("SMOOTHIE_SHOP")

#: The measured tomato town: seed 473956351's three FARMERS_MARKETs.
TOMATO_TOWN = {_I_MARKET: 3}
#: The measured control town: seed 242285847's BRUNCH_SPOT x2 + SMOOTHIE_SHOP,
#: three shops and not one of them a tomato buyer.
NO_TOMATO_TOWN = {_I_BRUNCH: 2, _I_SMOOTHIE: 1}


def _shops(counts):
    s = np.zeros(spec.N_SHOPS, np.int32)
    for i, n in counts.items():
        s[i] = n
    return s


def _view(day=12, town=None, **kw):
    """`test_route_early`'s board with a town drawn on it."""
    return _base_view(day=day, **kw)._replace(
        shops=_shops(TOMATO_TOWN if town is None else town))


#: A mix the brain might choose in the back half: four crops, no tomato, and
#: more tiles than any one crop, so "the whole mix moves" has something to say.
MIX = np.array([4, 3, 0, 3, 2], np.int32)


def _day(view=None, mix=MIX, crew=6, **kw):
    return _plan(view if view is not None else _view(**kw),
                 _macro(plant_target=np.asarray(mix, np.int32),
                        crew_target=np.int32(crew)))


def _planted(plan):
    """{crop index: tiles the day plants}."""
    uop, ua = np.asarray(plan[0]), np.asarray(plan[1])
    crops, n = np.unique(ua[uop == O.OP_PLANT], return_counts=True)
    return {int(c): int(k) for c, k in zip(crops, n)}


def _seed_buys(plan):
    """{crop index: seeds the day's market rows buy}."""
    out = {}
    for turn in range(spec.TURNS_PER_DAY):
        for op, arg, qty in _row(plan, turn):
            if op == O.MO_BUY_SEED and qty:
                out[int(arg)] = out.get(int(arg), 0) + int(qty)
    return out


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", True)


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", False)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(monkeypatch):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte. Pinned on
    `test_route_early`'s digests, the same ones `test_same_day_fert.py` and
    `test_open_pump.py` hold their own switches to."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_plants_the_brains_mix_in_a_tomato_town(off):
    """OFF the town is not read at all: a day standing in front of three
    FARMERS_MARKETs plants the softmax's four crops and no tomato, which is the
    defect."""
    got = _planted(_day())
    assert got, "the fixture board planted nothing"
    assert spec.I_TOMATO not in got
    assert set(got) == {c for c in range(spec.N_CROPS) if MIX[c]}


# =========================================================================
# ON: the mix, the town and the window
# =========================================================================

def test_on_moves_the_whole_mix_to_tomato(on):
    """Every tile the day plants gets a tomato -- not a share of them, the
    way `_wheat_mix` takes a share."""
    assert set(_planted(_day())) == {spec.I_TOMATO}


def test_on_plants_the_same_number_of_tiles(on, monkeypatch):
    """A mix change and not a development change: `sum(plant_target)` is
    preserved by construction, so the day's tile, seed and labour budget is
    sized against the same number and the same tiles get worked."""
    with_switch = sum(_planted(_day()).values())
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", False)
    without = sum(_planted(_day()).values())
    assert with_switch == without > 0


def test_on_buys_tomato_seed_and_nothing_else(on):
    """The purchase side follows the mix: the override runs before `_wants`,
    so the seeds the budget buys are the ones the tiles plant."""
    buys = _seed_buys(_day())
    assert buys, "the day bought no seed at all"
    assert set(buys) == {spec.I_TOMATO}


def test_on_leaves_a_town_with_no_tomato_buyer_alone(on, monkeypatch):
    """The control seed's town: three shops, none of them a tomato buyer, and
    the plan is the one the brain's mix makes."""
    view = _view(town=NO_TOMATO_TOWN)
    fired = _digest(_day(view))
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", False)
    assert fired == _digest(_day(view))


def test_on_leaves_a_town_one_shop_short_alone(on, monkeypatch):
    """`ENDGAME_TOMATO_SHOPS` is a floor, and a single buyer does not clear the
    hinge's 200-unit shoulder in a season."""
    view = _view(town={_I_PIZZA: 1})
    fired = _digest(_day(view))
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", False)
    assert fired == _digest(_day(view))


def test_on_counts_instances_and_not_kinds(on):
    """Duplicates count: two FARMERS_MARKETs drain the market twice as fast as
    one, and the engine's lottery draws instances."""
    for town in ({_I_MARKET: 2}, {_I_PIZZA: 2}, {_I_PIZZA: 1, _I_MARKET: 1}):
        assert set(_planted(_day(_view(town=town)))) == {spec.I_TOMATO}, town


def test_on_fires_only_inside_the_window(on, monkeypatch):
    """Days `ENDGAME_TOMATO_DAY .. ENDGAME_TOMATO_LAST_DAY`. Before the window
    the mix is the midgame's; after it a tomato cannot collect its four units
    before the bell."""
    for day in (P.ENDGAME_TOMATO_DAY, P.ENDGAME_TOMATO_LAST_DAY):
        assert set(_planted(_day(_view(day=day)))) == {spec.I_TOMATO}, day
    for day in (P.ENDGAME_TOMATO_DAY - 1, P.ENDGAME_TOMATO_LAST_DAY + 1):
        view = _view(day=day)
        fired = _digest(_day(view))
        with monkeypatch.context() as m:
            m.setattr(P, "ENDGAME_TOMATO_ON", False)
            assert fired == _digest(_day(view)), day


def test_on_leaves_a_day_that_plants_nothing_alone(on, monkeypatch):
    """The rewrite preserves the total, so a zero total stays zero: no seed is
    bought and no tile is planted on a day the brain wanted neither."""
    view = _view()
    fired = _digest(_day(view, mix=np.zeros(spec.N_CROPS, np.int32)))
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", False)
    assert fired == _digest(_day(view, mix=np.zeros(spec.N_CROPS, np.int32)))


def test_on_leaves_the_animals_alone(on):
    """Melon, animals and every sell rule are untouched: the only field
    `_endgame_tomato` replaces is `plant_target`."""
    view = _view()
    macro = _macro(plant_target=MIX.copy(), animal_want=np.array([2, 1, 1], np.int32),
                   crew_target=np.int32(6))
    out = P._endgame_tomato(np, view, macro)
    assert out._replace(plant_target=macro.plant_target) == macro
    assert int(np.sum(out.plant_target)) == int(np.sum(macro.plant_target))


def test_the_shop_mask_is_the_engines_tomato_demand():
    """Read off `spec.SHOP_CONSUME` and not named, so a demand-table change
    cannot silently un-fire the rule."""
    got = {spec.SHOP_NAMES[i] for i in np.flatnonzero(P._TOMATO_SHOPS)}
    assert got == {"PIZZA_SHOP", "FARMERS_MARKET"}


def test_the_last_day_collects_the_full_yield():
    """The knob's arithmetic, against the crop table. TOMATO is
    `first_yield_day 8, interval 1, max_yield 4, ongoing`, so a tile planted on
    day `d` collects `min(4, 30 - (d + 8))` units and `ENDGAME_TOMATO_LAST_DAY`
    is the last `d` that collects all four."""
    c = spec.I_TOMATO
    assert (int(spec.CROP_FIRST_YIELD_DAY[c]), int(spec.CROP_INTERVAL[c]),
            int(spec.CROP_MAX_YIELD[c]), int(spec.CROP_ONGOING[c])) == (8, 1, 4, 1)

    def units(d):
        return max(0, min(int(spec.CROP_MAX_YIELD[c]),
                          spec.N_DAYS - (d + int(spec.CROP_FIRST_YIELD_DAY[c]))))

    d = P.ENDGAME_TOMATO_LAST_DAY
    assert units(d) == int(spec.CROP_MAX_YIELD[c])
    assert units(d + 1) < units(d)


# =========================================================================
# ENDGAME_TOMATO_TILES: the budget
# =========================================================================

def _mix_out(view, mix=MIX):
    """`plant_target` after the rule, as a list."""
    macro = _macro(plant_target=np.asarray(mix, np.int32), crew_target=np.int32(6))
    return [int(x) for x in np.asarray(
        P._endgame_tomato(np, view, macro).plant_target)]


def test_budget_zero_is_the_unbudgeted_rule(on, monkeypatch):
    """The 0 default is "no budget": the whole mix moves, value for value with
    the rule as it was measured, so nothing that reads the switch at its
    default sees a different plan."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_TILES", 0)
    view = _view()
    assert _mix_out(view) == [0, 0, int(np.sum(MIX)), 0, 0]
    assert set(_planted(_day(view))) == {spec.I_TOMATO}


def test_budget_caps_the_tiles_and_keeps_the_total(on, monkeypatch):
    """A budget under the day's total takes exactly the budget and hands the
    rest back to the brain's crops in the brain's proportions -- a mix change
    still, so `sum(plant_target)` does not move."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_TILES", 5)
    got = _mix_out(_view())
    assert got[spec.I_TOMATO] == 5
    assert sum(got) == int(np.sum(MIX))
    assert got[spec.I_STRAWBERRY] and got[spec.I_WHEAT], got


def test_budget_counts_the_tomato_already_on_the_board(on, monkeypatch):
    """Tiles HELD, not tiles planted: three live tomato plants spend the same
    crew and sell into the same pot, so a budget of five leaves room for two."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_TILES", 5)
    got = _mix_out(_view(n_ripe=3))
    assert got[spec.I_TOMATO] == 2
    assert sum(got) == int(np.sum(MIX))


def test_budget_already_full_plants_no_tomato(on, monkeypatch):
    """A board already at the budget claims nothing, and the day keeps the
    brain's own mix tile for tile."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_TILES", 3)
    view = _view(n_ripe=4)
    assert _mix_out(view) == [int(x) for x in MIX]
    fired = _digest(_day(view))
    monkeypatch.setattr(P, "ENDGAME_TOMATO_ON", False)
    assert fired == _digest(_day(view))


def test_budget_over_the_days_total_is_the_whole_mix(on, monkeypatch):
    """A budget the day cannot spend does not invent tiles: the claim is
    clipped to the day's own total."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_TILES", 40)
    assert _mix_out(_view()) == [0, 0, int(np.sum(MIX)), 0, 0]


def test_budget_does_not_fire_outside_the_window(on, monkeypatch):
    """The budget is a size, not a second trigger: a day outside the window is
    still the brain's."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_TILES", 5)
    assert _mix_out(_view(day=P.ENDGAME_TOMATO_LAST_DAY + 1)) == [int(x) for x in MIX]
    assert _mix_out(_view(town=NO_TOMATO_TOWN)) == [int(x) for x in MIX]


def test_budget_never_cuts_the_brains_own_tomato(on, monkeypatch):
    """The floor, and the reason for it: the give-back can only hand a tile to
    a crop the brain asked for, so a mix that is tomato and nothing else keeps
    its total rather than inventing crops the gene ruled out."""
    monkeypatch.setattr(P, "ENDGAME_TOMATO_TILES", 2)
    only = np.zeros(spec.N_CROPS, np.int32)
    only[spec.I_TOMATO] = 7
    assert _mix_out(_view(), mix=only) == list(only)
    mixed = np.array([2, 0, 6, 0, 0], np.int32)
    got = _mix_out(_view(), mix=mixed)
    assert got[spec.I_TOMATO] == 6 and sum(got) == 8, got


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
