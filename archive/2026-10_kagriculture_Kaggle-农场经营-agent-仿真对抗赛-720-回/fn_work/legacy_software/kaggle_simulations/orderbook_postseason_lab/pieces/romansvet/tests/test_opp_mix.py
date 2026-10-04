"""`plan.OPP_MIX_ON`: price the other seat's standing book into the plant mix.

The finding, measured on the real engine (2026-09-05, flow102_g280 against the
six 1950-2110 band tapes, `scratchpad/lossanat/report.md`): nothing separates a
win board from a loss board before day 8 and 73 % of the separation lands on
days 26-29, always through the same event -- our liquidation running into the
opponent's own book. Their book is fixed across wins and losses (264 STRAWBERRY,
263 MILK, 176 WOOL, **0 TOMATO**); what moves is ours. Win boards: 79 u TOMATO
and 196 u MILK at 164/u. Loss boards: 255 u STRAWBERRY head-on into their 264,
at 98/u.

`ENDGAME_TOMATO_ON` answers that from the town's side with a fixed product.
This switch answers it from the *opponent's* side with no fixed product: the
engine seats `obs.farms` whole, so the tiles the other seat has committed to
each product are a fact the day already holds (`DayView.opp_commit`).

Two claims are tested and nothing else:

* OFF the opponent's farm is invisible -- the plan is bit-identical whatever
  the other seat holds, and identical to the pre-switch planner's on
  `test_route_early`'s pinned digests.
* ON a heavy opponent commitment moves the planting choice: it comes off the
  contested crop's value in `_candidates` and off its share of the day's mix in
  `_opp_mix`, and the day's tile total does not move.
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
from test_route_early import PIN, PIN_SEEDS, _digest, _plan, _seeded_case
from test_route_early import _view as _base_view

from kagg3 import spec
from kagg3.core import plan as P

#: The stack `test_route_early`'s digests were taken before -- the planner at
#: `a838700`, the same pin `test_endgame_tomato.py` holds its own switch to.
_PINNED_OFF = ("ROUTE_SPLIT_ON", "SURVIVAL_WATER_ON", "TAIL_CARE_ON",
               "FEED_MANDATORY_ON", "EARLY_SELL_ON")

#: A mix the brain might choose in the back half: four crops, no tomato, and
#: STRAWBERRY the biggest single claim -- the contested product.
MIX = np.array([3, 2, 0, 6, 2], np.int32)


def _commit(**by_product):
    c = np.zeros(spec.N_PRODUCTS, np.int32)
    for name, n in by_product.items():
        c[getattr(spec, "I_" + name)] = n
    return c


#: The band tape's own book, as the probe read it off a real game at day 12:
#: 33 STRAWBERRY tiles against 20 WHEAT and a small herd.
BAND_BOOK = _commit(STRAWBERRY=33, WHEAT=20, MILK=9, WOOL=8, FERT=17)


def _view(day=14, commit=None, **kw):
    return _base_view(day=day, **kw)._replace(
        opp_commit=BAND_BOOK if commit is None else commit)


def _day(view=None, mix=MIX, crew=6, **kw):
    return _plan(view if view is not None else _view(**kw),
                 _macro(plant_target=np.asarray(mix, np.int32),
                        crew_target=np.int32(crew)))


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "OPP_MIX_ON", True)


# =========================================================================
# OFF: byte-identical, and the other seat is not read at all
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(monkeypatch):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    monkeypatch.setattr(P, "OPP_MIX_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)
    assert tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS) == PIN


def test_off_cannot_see_the_other_seat(monkeypatch):
    """`opp_commit` is a new *field*, so the identity above is not enough on its
    own: OFF the plan has to be the same plan on an empty opponent farm and on
    a farm holding 33 strawberry tiles."""
    monkeypatch.setattr(P, "OPP_MIX_ON", False)
    empty = _digest(_day(_view(commit=np.zeros(spec.N_PRODUCTS, np.int32))))
    assert empty == _digest(_day(_view(commit=BAND_BOOK)))


def test_off_default_view_is_an_empty_opponent():
    """A hand-built view that never heard of the field reads as an empty farm,
    which is the identity for the weight."""
    assert not np.any(np.asarray(_base_view(day=14).opp_commit))
    w = P._opp_mix_weight(np, _base_view(day=14))
    assert np.array_equal(np.asarray(w), np.full(spec.N_PRODUCTS, P.OPP_MIX_ONE))


# =========================================================================
# ON: the penalty moves the planting choice
# =========================================================================

def test_on_penalises_the_crop_the_other_seat_is_committed_to(on):
    """The weight is the tilt itself: 33 of the other seat's ~70 producing
    tiles are strawberry, so strawberry is the cheapest product on the board
    and a crop they hold nothing of stays at 1x."""
    w = np.asarray(P._opp_mix_weight(np, _view()))
    assert w[spec.I_STRAWBERRY] < P.OPP_MIX_ONE
    assert w[spec.I_STRAWBERRY] == w.min()
    assert w[spec.I_TOMATO] == P.OPP_MIX_ONE      # they hold none
    assert w.max() <= P.OPP_MIX_ONE               # a penalty, never a bonus
    assert w.min() >= P.OPP_MIX_FLOOR             # and never a ban


def test_on_moves_the_mix_off_the_contested_crop(on):
    """`_opp_mix` takes each crop's own share of the penalty and gives it to the
    least contested crop that can still mature -- the day plants the same number
    of tiles, and fewer of them are the contested one."""
    macro = _macro(plant_target=MIX.copy(), crew_target=np.int32(6))
    out = np.asarray(P._opp_mix(np, _view(), macro).plant_target)
    assert out[spec.I_STRAWBERRY] < MIX[spec.I_STRAWBERRY]
    assert int(out.sum()) == int(MIX.sum())


def test_on_moves_the_seed_the_day_actually_plants(on, monkeypatch):
    """End to end through `build_day`: the tiles planted with strawberry drop
    and the day's planted total does not."""
    from kagg3.core import ops as O

    def planted(plan):
        uop, ua = np.asarray(plan[0]), np.asarray(plan[1])
        crops, n = np.unique(ua[uop == O.OP_PLANT], return_counts=True)
        return {int(c): int(k) for c, k in zip(crops, n)}

    view = _view()
    with_switch = planted(_day(view))
    monkeypatch.setattr(P, "OPP_MIX_ON", False)
    without = planted(_day(view))
    assert with_switch != without, "the switch changed nothing at all"
    assert (with_switch.get(spec.I_STRAWBERRY, 0)
            < without.get(spec.I_STRAWBERRY, 0))
    assert sum(with_switch.values()) == sum(without.values())


def test_on_prices_the_contested_seed_below_the_plain_valuation(on):
    """The other half of the switch, and the one that keeps the purchase side
    agreeing with the mix: the k-th strawberry seed is worth less in
    `_candidates` than it is OFF, and an uncontested crop's is unchanged."""
    view = _view()
    macro = _macro(plant_target=MIX.copy(), crew_target=np.int32(6))
    P.OPP_MIX_ON = False
    try:
        off = _values(view, macro)
    finally:
        P.OPP_MIX_ON = True
    on_ = _values(view, macro)
    straw = 2 + spec.I_STRAWBERRY
    tom = 2 + spec.I_TOMATO
    assert (on_[straw] <= off[straw]).all() and (on_[straw] < off[straw]).any()
    assert np.array_equal(on_[tom], off[tom])


def _values(view, macro):
    """`_candidates`' value table for one view, through `_derive`'s own call."""
    seen = {}
    orig = P._candidates

    def spy(*a, **k):
        out = orig(*a, **k)
        seen.setdefault("v", out[0])
        return out

    P._candidates = spy
    try:
        P.build_day(np, view, macro)
    finally:
        P._candidates = orig
    return np.asarray(seen["v"])


def test_on_is_inert_before_its_day(on, monkeypatch):
    """`OPP_MIX_DAY` is the gate: the day before it the plan is the OFF plan."""
    view = _view(day=P.OPP_MIX_DAY - 1)
    fired = _digest(_day(view))
    monkeypatch.setattr(P, "OPP_MIX_ON", False)
    assert fired == _digest(_day(view))


def test_on_is_inert_at_zero_strength(on, monkeypatch):
    """Strength 0 is the identity, and it is read through `float` so the
    switch harness can pass it as the string `"0.5"`."""
    monkeypatch.setattr(P, "OPP_MIX_STRENGTH", "0.0")
    view = _view()
    fired = _digest(_day(view))
    monkeypatch.setattr(P, "OPP_MIX_ON", False)
    assert fired == _digest(_day(view))
    monkeypatch.setattr(P, "OPP_MIX_STRENGTH", "0.5")
    assert P._opp_mix_strength() == P.OPP_MIX_ONE // 2


def test_on_preserves_the_total_on_a_day_that_plants_nothing(on, monkeypatch):
    """A proportional tilt of zero tiles is zero tiles."""
    view = _view()
    zero = np.zeros(spec.N_CROPS, np.int32)
    fired = _digest(_day(view, mix=zero))
    monkeypatch.setattr(P, "OPP_MIX_ON", False)
    assert fired == _digest(_day(view, mix=zero))


def test_on_leaves_everything_but_the_mix_alone(on):
    """`_opp_mix` replaces one field, exactly like the three mix rewrites above
    it in `_plan_and_stats`."""
    macro = _macro(plant_target=MIX.copy(),
                   animal_want=np.array([2, 1, 1], np.int32),
                   crew_target=np.int32(6))
    out = P._opp_mix(np, _view(), macro)
    assert out._replace(plant_target=macro.plant_target) == macro


# =========================================================================
# The observation side
# =========================================================================

def test_commitment_counts_crops_and_maps_animals_to_products():
    """`opp_commitment` is the integer twin of `brain._producing`: crops in crop
    order, animals through their product, and FERTILIZER carrying the herd."""
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = np.full(spec.N_TILES, -1, np.int32)
    kind[:4] = spec.KIND_PLANT
    occ[:4] = [spec.I_STRAWBERRY, spec.I_STRAWBERRY, spec.I_WHEAT, spec.I_TOMATO]
    kind[4:6] = spec.KIND_PASTURE
    occ[4:6] = [spec.I_SHEEP - spec.I_GOOSE, spec.I_COW - spec.I_GOOSE]
    got = np.asarray(P.opp_commitment(np, kind, occ))
    assert got[spec.I_STRAWBERRY] == 2 and got[spec.I_WHEAT] == 1
    assert got[spec.I_TOMATO] == 1
    assert got[spec.I_WOOL] == 1 and got[spec.I_MILK] == 1
    assert got[spec.I_FERT] == 2                     # every animal makes it


def test_parse_reads_the_other_seats_farm():
    """The submission path: `agent/parse.py` fills the same nine columns off
    `obs["farms"][1 - player]`, which the engine seats whole."""
    from kagg3.agent import parse

    def tile(**kw):
        return kw

    tiles = [[None] * spec.BOARD for _ in range(spec.BOARD)]
    tiles[0][0] = tile(kind="PLANT", crop="STRAWBERRY")
    tiles[0][1] = tile(kind="PLANT", crop="STRAWBERRY")
    tiles[0][2] = tile(kind="PASTURE", animal="SHEEP")
    tiles[0][3] = "LOCKED"
    obs = {"farms": [{"tiles": [[None] * spec.BOARD for _ in range(spec.BOARD)]},
                     {"tiles": tiles}]}
    got = parse.parse_opp_commit(obs, 0)
    assert got[spec.I_STRAWBERRY] == 2
    assert got[spec.I_WOOL] == 1 and got[spec.I_FERT] == 1
    assert parse.parse_opp_commit({}, 0).sum() == 0


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
