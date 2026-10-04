"""`plan.HORIZON_DROP_ON`: the terminal bounds, re-derived through DROP.

`O.LAST_SHED_DAY` = 28 was two facts at once -- the last day with an
end-of-day, and the last day whose work can still be sold. `plan.DROP_ON`
separated them: day 29's HARVEST/COLLECT -> walk home -> DROP ->
`SELL_TURNS[-1]` chain closes inside the day, so work done on day 29 monetizes
while the last end-of-day is still eod 28. Every horizon in the planner that
meant "the last day whose payoff can still be sold" is therefore one day short,
and this switch is that day. `valuation.pay_day()` is the only place it is
spelled.

Each test below pins one re-derived bound *at its flip day* -- the day on which
the decision changes -- with the switch off and on, so a future edit that moves
a horizon has to move a pinned day with it. `test_off_*` are the identity half:
off, `pay_day()` is `O.LAST_SHED_DAY` and the plan is the champion's, verified
end to end against `rep/drop_b28.csv` (12 rows re-run, every column identical).
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
from test_animal_acquisition_bound import _bought
from test_animal_acquisition_bound import _view as _animal_view
from test_budget_order import _macro
from test_no_late_planting import _obs, _theta_develop_all_crops

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import valuation as VAL

LAST = O.LAST_SHED_DAY                                   # 28, the last end-of-day
PAY = LAST + 1                                           # 29, the last payable day

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)

#: Five tiles a step or less from a shed-access tile (`plan.DIST_SHED`), in
#: serpentine index order. A day-29 fixture has to sit here: the DROP day's
#: budget ends at `SELL_TURNS[-1] + 1` and each block pays its walk home, so a
#: board in the far corner idles under *both* settings and pins nothing.
TILES = (34, 35, 43, 44, 45)


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "DROP_ON", True)
    monkeypatch.setattr(P, "HORIZON_DROP_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "DROP_ON", True)
    monkeypatch.setattr(P, "HORIZON_DROP_ON", True)


def _tile_view(day, kind, occ, **kw):
    """One quadrant of open board with whatever `kind`/`occ` say on it."""
    z = np.zeros(100, np.int32)
    base = dict(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(3000),
        nquad=np.int32(1), price=BASE_PRICE.copy())
    base.update(kw)
    return P.DayView(**base)


def _late_wheat_view(day, t_day=25):
    """Five wheat planted on `t_day`, standing at three units.

    The deadline clamp is the whole content of the fixture: `28 - 25 = 3` is
    under wheat's saturation age of 4, so this is one of the tiles whose
    harvest day the horizon actually moves.
    """
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[list(TILES)] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[list(TILES)] = spec.I_WHEAT
    td = np.zeros(100, np.int32)
    td[list(TILES)] = t_day
    ty = np.zeros(100, np.int32)
    ty[list(TILES)] = 3
    return _tile_view(day, kind, occ, t_day=td, t_yield=ty)


def _thirsty_tomato_view(day, t_day=20):
    """Five tomatoes one dry night from weeding, nothing ripe on them.

    Planted on day 20, and the planting day is load-bearing since
    `SURVIVAL_WATER_ON` (default since 2026-09-03): a survival watering is
    mandatory only where the crop's remaining value at its own sale day is
    positive, so the day-0 tomatoes this fixture used to build have no stream
    left by day 27 and are not watered on any day, under either horizon --
    which would make every assertion below pass for the wrong reason. Day 20
    is the same board with a payable tomorrow, and it reproduces the
    pre-switch answers exactly: watered on 27 under both horizons, on 28 only
    under `HORIZON_DROP_ON`, never on 29."""
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[list(TILES)] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[list(TILES)] = spec.I_TOMATO
    cons = np.zeros(100, np.int32)
    cons[list(TILES)] = 1
    td = np.zeros(100, np.int32)
    td[list(TILES)] = t_day
    return _tile_view(day, kind, occ, t_cons=cons, t_day=td)


def _cared_goose_view(day):
    """One hungry, uncared goose that has been laying since day 4, and the
    wheat to feed it. Its next payable fire is `day + 2` -- the CARE horizon's
    own question."""
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[TILES[0]] = spec.KIND_COOP
    occ = np.full(100, -1, np.int32)
    occ[TILES[0]] = 0                                     # a goose
    cons = np.zeros(100, np.int32)
    cons[TILES[0]] = 1                                    # unfed yesterday
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = 10
    return _tile_view(day, kind, occ, t_cons=cons, shed=shed)


def _ops(view, macro=None):
    """The set of unit ops the day emits."""
    unit_op = P.build_day(np, view, macro or _macro())[0]
    return set(int(v) for v in np.unique(np.asarray(unit_op)))


# ------------------------------------------------------- the horizon itself

def test_pay_day_is_the_shed_day_off_and_one_past_it_on(off):
    assert VAL.pay_day() == LAST == 28


def test_pay_day_moves_by_exactly_one_day(on):
    assert VAL.pay_day() == PAY == 29


def test_the_switch_never_moves_the_end_of_day_itself(on):
    """`LAST_SHED_DAY` is a fact about the engine (`episodeSteps` 720), not a
    policy: the switch reinterprets what reads it and never edits it."""
    assert O.LAST_SHED_DAY == 28


# ------------------------------------------------- the crop planting horizon

def test_plant_gate_flip_day_is_27_for_wheat_and_carrot(off, monkeypatch):
    """`day + CROP_FIRST_YIELD_DAY <= pay_day()`. Off, day 27 is one day past
    every crop's last planting; on, the two-day crops fit."""
    assert int(brain.decide(np, _theta_develop_all_crops(), _obs(27)).plant_target.sum()) == 0
    monkeypatch.setattr(P, "HORIZON_DROP_ON", True)
    tgt = brain.decide(np, _theta_develop_all_crops(), _obs(27)).plant_target
    early = spec.CROP_FIRST_YIELD_DAY <= PAY - 27         # wheat, carrot
    assert np.all(tgt[early] > 0) and np.all(tgt[~early] == 0)


def test_plant_gate_still_closes_one_day_later(on):
    """The gate moves; it does not disappear. Day 28 + 2 = 30 is past 29."""
    assert int(brain.decide(np, _theta_develop_all_crops(), _obs(28)).plant_target.sum()) == 0


def test_every_crop_last_planting_day_moves_by_one(off, monkeypatch):
    """`new_plant_units` is the value side of the same gate, and the two must
    agree crop by crop or a seed is bought for a tile that will not be planted.
    """
    for hi, flag in ((LAST, False), (PAY, True)):
        monkeypatch.setattr(P, "HORIZON_DROP_ON", flag)
        for c in range(spec.N_CROPS):
            last = hi - int(spec.CROP_FIRST_YIELD_DAY[c])
            crop = np.int32(c)
            assert int(VAL.new_plant_units(np, crop, np.int32(last))) > 0
            assert int(VAL.new_plant_units(np, crop, np.int32(last + 1))) == 0


# ------------------------------------------------------- the deadline harvest

def test_day_28_harvests_the_late_wheat_off(off):
    """`harvest_age = clip(28 - 25, first, sat) = 3` and the crop is 3 days
    old, so day 28 is its deadline: three units to the shed, sold on 29."""
    assert O.OP_HARVEST in _ops(_late_wheat_view(LAST))


def test_day_28_grows_the_late_wheat_one_more_day_on(on):
    """`clip(29 - 25, 2, 4) = 4`: the tile is worth one more in-window
    watering, and the DROP chain sells the day-29 harvest that follows."""
    ops = _ops(_late_wheat_view(LAST))
    assert O.OP_HARVEST not in ops
    assert O.OP_WATER in ops


def test_day_29_harvests_the_late_wheat_under_both(off, monkeypatch):
    """The deferral has a floor: on day 29 the clamp is satisfied either way,
    so the switch never leaves a crop standing past the season."""
    for flag in (False, True):
        monkeypatch.setattr(P, "HORIZON_DROP_ON", flag)
        ops = _ops(_late_wheat_view(PAY))
        assert O.OP_HARVEST in ops and O.OP_DROP in ops


def test_saturated_tiles_do_not_move(off, monkeypatch):
    """Only the clamped tiles move. A wheat planted on day 20 saturates at age
    4 under either horizon, so its harvest day is day 24 either way."""
    for flag in (False, True):
        monkeypatch.setattr(P, "HORIZON_DROP_ON", flag)
        assert O.OP_HARVEST in _ops(_late_wheat_view(24, t_day=20))
        assert O.OP_HARVEST not in _ops(_late_wheat_view(23, t_day=20))


def test_free_slot_count_reads_the_same_clamp(off, monkeypatch):
    """`brain.n_free_slots` counts the tiles a harvest frees today off the very
    same clamp; if the two ever disagree the day plants tiles it does not
    clear."""
    z = np.zeros(100, np.int32)
    td = z.copy(); td[list(TILES)] = 25
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[list(TILES)] = spec.KIND_PLANT
    occ = z - 1; occ[list(TILES)] = spec.I_WHEAT
    obs = _obs(LAST)._replace(kind=kind, occ=occ, t_day=td)
    n_off = int(brain.n_free_slots(np, obs))
    monkeypatch.setattr(P, "HORIZON_DROP_ON", True)
    assert int(brain.n_free_slots(np, obs)) == n_off - 5


# ------------------------------------------------------------ survival on 28

def test_day_28_lets_the_crop_weed_off(off):
    """Off, nothing that lives into day 29 is worth a turn, so the last
    survival watering is day 27's."""
    assert O.OP_WATER not in _ops(_thirsty_tomato_view(LAST))


def test_day_28_waters_for_survival_on(on):
    """On, day 29 harvests what day 28 keeps alive -- and a plant that weeds at
    eod 28 (`refresh_plants`: `cons >= 2`) has nothing to harvest."""
    assert O.OP_WATER in _ops(_thirsty_tomato_view(LAST))


def test_day_27_waters_under_both(off, monkeypatch):
    """The flip day is 28 and only 28: day 27 always had a payable tomorrow."""
    for flag in (False, True):
        monkeypatch.setattr(P, "HORIZON_DROP_ON", flag)
        assert O.OP_WATER in _ops(_thirsty_tomato_view(27))


def test_day_29_never_waters_for_survival(off, monkeypatch):
    """And the new horizon has its own last day: nothing survives day 29."""
    for flag in (False, True):
        monkeypatch.setattr(P, "HORIZON_DROP_ON", flag)
        assert O.OP_WATER not in _ops(_thirsty_tomato_view(PAY))


# ---------------------------------------------------------- the animal bound

def test_day_25_goose_is_rejected_off(off):
    """0.2's own worked example: three sellable fertilizers (d26-28), no egg,
    three wheat -- 3 x 100 - 3 x 25 = 225 against a 300-coin goose."""
    assert _bought(_animal_view(25), 0) == 0


def test_day_25_goose_is_bought_on(on):
    """The d29 collection and the first egg fire (eod 28 -> harvest day 29)
    both monetize now: 50 + 4 x 100 - 3 x 25 = 375 against 300."""
    assert _bought(_animal_view(25), 0) == 1


def test_the_animal_bound_flip_day_moves_to_26(on):
    """It moves by one day; it does not vanish. Day 26: still no fire by 29,
    three fertilizers, two feeds -- 300 - 50 = 250 against 300."""
    assert _bought(_animal_view(26), 0) == 0


def test_a_standing_animal_keeps_its_last_fire_and_fertilizer(off, monkeypatch):
    """`animal_value` on the day the horizon bites: a goose laying daily since
    day 0, valued on day 28."""
    args = (np, BASE_PRICE, np.int32(0), np.int32(0), np.int32(0), np.int32(0),
            np.int32(LAST))
    off_val = int(VAL.animal_value(*args))
    monkeypatch.setattr(P, "HORIZON_DROP_ON", True)
    on_val = int(VAL.animal_value(*args))
    # one more egg (the eod-28 fire, harvested on 29) and one more fertilizer
    assert on_val - off_val == int(BASE_PRICE[spec.I_EGG]) + int(BASE_PRICE[spec.I_FERT])


def test_care_pays_only_when_its_fire_is_payable(off, monkeypatch):
    """A CARE banked on day 27 cashes at `next_fire_after` = day 29. Off that
    fire is past the horizon and the care is not worth the turn.

    `TAIL_CARE_ON` off: it is on by default since 2026-09-03 and it spends a
    unit's *idle tail* on the nearest animal the day left uncared, which is a
    free turn and never asks `care_pays` at all. With it on this board is
    cared under both horizons, and the horizon gate -- which is what this test
    is about -- has no visible effect."""
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    assert O.OP_CARE not in _ops(_cared_goose_view(27))
    monkeypatch.setattr(P, "HORIZON_DROP_ON", True)
    assert O.OP_CARE in _ops(_cared_goose_view(27))


# ------------------------------------------------------------- the hire purse

def test_cash_reserve_covers_day_29s_crew_only_on(off, monkeypatch):
    """Off, day 28 keeps nothing back -- "day 29 hires nobody by law". On, day
    29 hires through the DROP enumeration and every `HIRE_TURNS` row resolves
    before `SELL_TURNS[0]`, so its crew is paid out of coins day 28 carried."""
    assert int(P.cash_reserve(np, np.int32(0), np.int32(LAST))) == 0
    monkeypatch.setattr(P, "HORIZON_DROP_ON", True)
    assert int(P.cash_reserve(np, np.int32(0), np.int32(LAST))) > 0


def test_cash_reserve_is_still_void_on_the_last_day(off, monkeypatch):
    """The last payable day has no tomorrow to hire for under either setting."""
    for flag, day in ((False, LAST), (True, PAY)):
        monkeypatch.setattr(P, "HORIZON_DROP_ON", flag)
        assert int(P.cash_reserve(np, np.int32(0), np.int32(day))) == 0


def test_cash_reserve_is_unchanged_before_the_flip(off, monkeypatch):
    for day in range(0, LAST):
        for n in (0, 5, spec.MAX_HANDS):
            r = int(P.cash_reserve(np, np.int32(n), np.int32(day)))
            monkeypatch.setattr(P, "HORIZON_DROP_ON", True)
            assert int(P.cash_reserve(np, np.int32(n), np.int32(day))) == r
            monkeypatch.setattr(P, "HORIZON_DROP_ON", False)


# ----------------------------------------------------------- the OFF identity

def test_the_tile_horizons_do_not_move_before_the_endgame(off, monkeypatch):
    """The *tile* horizons -- the deadline clamp, the plant gate, the survival
    rule, the CARE fire -- are all clamped well short of day 28 in midseason,
    so these boards plan identically under both settings.

    This is deliberately not the claim that the switch is endgame-confined,
    because it is not: `ub_fert` and `_pipeline_units` count "one fertilizer
    per remaining day" and that count moves by one on **every** day of a season
    with animals, which reprices the animal candidates from day 0. The measured
    paired sd is 7,633 against DROP's 581 for exactly that reason. What this
    test pins is that nothing on a *tile* moves early -- a horizon that leaked
    into the crop or animal calendars would show up here as a changed plan and
    not only as a changed score."""
    views = [_late_wheat_view(d, t_day=max(d - 3, 0)) for d in range(0, 25)]
    views += [_thirsty_tomato_view(d) for d in range(0, 25)]
    views += [_cared_goose_view(d) for d in range(0, 25)]
    for v in views:
        monkeypatch.setattr(P, "HORIZON_DROP_ON", False)
        a = [np.asarray(x).copy() for x in P.build_day(np, v, _macro())]
        monkeypatch.setattr(P, "HORIZON_DROP_ON", True)
        b = [np.asarray(x) for x in P.build_day(np, v, _macro())]
        for x, y in zip(a, b):
            assert np.array_equal(x, y), f"day {int(v.day)} plan moved before the horizon"


def test_off_reads_no_horizon_but_the_shed_day(off):
    """The identity that makes the champion decode byte for byte: with the
    switch off `pay_day()` *is* `O.LAST_SHED_DAY`, so every expression that
    reads it is the integer expression it replaced."""
    assert VAL.pay_day() is not None and VAL.pay_day() == O.LAST_SHED_DAY
    for day in range(spec.N_DAYS):
        for hi in (VAL.pay_day(),):
            assert hi == 28


def test_valuation_binds_the_plan_module_without_importing_it(off):
    """`valuation` must never import `plan` lazily: `eval_vs_baselines`'s
    `_vendored_imports` hides this repo's `kagg3` from `sys.modules` and `src`
    from `sys.path` for the length of every game seated against a packaged
    agent, so a runtime import there resolves to the packaged planner or
    raises. Measured when it was written that way: 12 games at 3,000 coins.
    """
    assert VAL._PLAN is sys.modules[P.__name__]
    src = open(os.path.join("src", "kagg3", "core", "valuation.py"), encoding="utf-8").read()
    assert "import plan" not in src.split("_PLAN = None")[-1]


def test_the_horizon_plan_agrees_across_backends(on):
    """The switch is a Python constant, so it folds into the trace as a
    literal -- but the days it re-opens (day-28 survival work, the day-29 DROP
    on a deferred harvest) are days the numpy path had no reason to route
    before, and the equivalence surface is the plan, not the constant."""
    import jax
    import jax.numpy as jnp
    for view in (_late_wheat_view(LAST), _late_wheat_view(PAY),
                 _thirsty_tomato_view(LAST), _cared_goose_view(27)):
        macro = _macro()
        a = P.build_day(np, view, macro)
        b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                        jax.tree_util.tree_map(jnp.asarray, macro),
                        jnp.asarray(spec.build_price_table()))
        for x, y in zip(a, b):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"day {int(view.day)}"
