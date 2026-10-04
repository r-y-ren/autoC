"""`plan.MACRO_EXEC_ON`: execute a per-day macro schedule instead of enumerating.

The switch exists to answer the question the FORWARD_ADMIT postmortem left open
(`docs/strategy/2026-09-05-build-story.md`, addenda 2026-09-09): our planner
prices hands, animals and tiles against the tasks the board emits *today*, so a
top-five ramp -- four hands, five animals and twelve tiles on day 0 -- is not
expressible however the genes are set. `MACRO_EXEC_ON` hands the planner the
ramp as data and measures whether the machinery can put it on the board.

Two halves:

* OFF is the shipped program.  The switch defaults False, the schedule is
  `None` until `macro_load` runs, and every site that reads either is inside
  `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:` -- so an unset environment
  and an unpatched `plan.py` are the same day plan.  Pinned here over the whole
  plan tuple, on the boards the switch is meant to change most.
* ON executes.  The crew, the herd and the mix are the schedule's, not the
  enumeration's, up to the purse -- and the herd is served ahead of the seeds
  inside the one `budget.grant` walk that holds both
  (`docs/strategy/2026-09-14-melon-animal-mechanism.md` §3).
"""
from __future__ import annotations

import json
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

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P

ND = spec.N_DAYS


def _view(money=3000, nquad=1, day=0):
    """A blank board: every tile free, nothing planted, nothing in the shed."""
    z = np.zeros(100, np.int32)
    return P.DayView(
        day=np.int32(day),
        kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(nquad),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _macro(**kw):
    base = {
        "plant_target": np.zeros(spec.N_CROPS, np.int32),
        "animal_want": np.zeros(spec.N_ANIMALS, np.int32),
        "land_bias": np.int32(0),
        "hold": np.full(spec.N_PRODUCTS, 10_000, np.int32),
        "press": np.zeros(spec.N_PRODUCTS, np.int32),
        "grow_mult": np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32),
        "compact": np.int32(0),
        "dev_weight": np.int32(brain.GROW_ONE),
        "hire_bias": np.int32(0),
        "crew_target": np.int32(0),
        "animal_defer": np.int32(0),
        "forward_days": np.int32(0),
    }
    # [g12] Appended after the pins in `tests/test_fertengine.py` were cut, and
    # those run this helper against a pristine PRE-`g12` `src` tree in a
    # subprocess -- so the field is named only when the planner has it.
    if "fert_defer" in P.Macro._fields:
        base["fert_defer"] = np.int32(0)
    base.update(kw)
    return P.Macro(**base)


def _sched(tmp_path, hands=None, anim=None, tiles=None, land=None, sell=None,
           tag="t"):
    d = dict(tag=tag,
             sell_hour=(sell if sell is not None
                        else [[-1] * spec.N_ITEMS] * ND),
             hands_target=(hands if hands is not None else [0] * ND),
             animals_target=(anim if anim is not None
                             else [[0] * spec.N_ANIMALS] * ND),
             tiles_target=(tiles if tiles is not None
                           else [[0] * spec.N_CROPS] * ND),
             land_target=(land if land is not None else [0] * ND))
    p = tmp_path / "sched.json"
    p.write_text(json.dumps(d))
    return str(p)


@pytest.fixture
def off():
    """Restore the module globals whatever a test did to them."""
    was = (P.MACRO_EXEC_ON, P.MACRO_SCHEDULE, P.MACRO_MODE)
    yield
    P.MACRO_EXEC_ON, P.MACRO_SCHEDULE, P.MACRO_MODE = was


def _plan(view, macro):
    return [np.asarray(x) for x in P.build_day(np, view, macro)]


def _hires(view, macro):
    op = _plan(view, macro)[3]
    return int((op == O.MO_HIRE).sum())


def _qty(view, macro, mo_op, arg=None):
    op, a, q = _plan(view, macro)[3:6]
    m = (op == mo_op) if arg is None else ((op == mo_op) & (a == arg))
    return int(q[m].sum())


# ------------------------------------------------------------------ OFF half

def test_off_is_the_shipped_default():
    assert P.MACRO_EXEC_ON is False
    assert P.MACRO_SCHEDULE is None
    assert P.MACRO_ENV == "KAGG3_MACRO_JSON"


def test_loading_a_schedule_changes_nothing_while_the_switch_is_off(off, tmp_path):
    """A loaded schedule is inert: the gate is the switch, not the data.

    The whole plan tuple, on the four boards the switch is built to change --
    an opening purse, a rich day, a late day and a second quadrant."""
    macro = _macro(plant_target=np.array([8, 4, 0, 0, 0], np.int32),
                   animal_want=np.array([1, 2, 1], np.int32))
    views = [_view(), _view(money=12000), _view(day=20, money=6000),
             _view(nquad=2, money=9000)]
    before = [_plan(v, macro) for v in views]
    P.macro_load(_sched(tmp_path, hands=[9] * ND,
                        anim=[[3, 3, 3]] * ND,
                        tiles=[[20, 0, 0, 0, 5]] * ND,
                        land=[1] * ND))
    assert P.MACRO_SCHEDULE is not None and P.MACRO_EXEC_ON is False
    after = [_plan(v, macro) for v in views]
    for i, (b, a) in enumerate(zip(before, after)):
        for j, (x, y) in enumerate(zip(b, a)):
            assert np.array_equal(x, y), f"board {i} plan field {j} moved with the switch OFF"


def test_macro_load_of_nothing_is_none(off):
    P.MACRO_SCHEDULE = object()
    assert P.macro_load("") is None
    assert P.MACRO_SCHEDULE is None


# ------------------------------------------------------------------- ON half

def test_on_executes_the_schedule(off, tmp_path):
    """Crew, herd, mix and land are the schedule's, against a decode that asks
    for none of them -- the `FORWARD_ADMIT` case, where the day's own task set
    prices the ramp at zero."""
    macro = _macro()                       # the brain asks for nothing at all
    view = _view(money=6000)
    assert _hires(view, macro) == 0, "fixture no longer starts from a zero crew"
    P.macro_load(_sched(tmp_path, hands=[4] * ND, anim=[[0, 2, 3]] * ND,
                        tiles=[[12, 0, 0, 0, 2]] * ND))
    P.MACRO_EXEC_ON = True
    assert _hires(view, macro) == 4
    assert _qty(view, macro, O.MO_BUY_ANIMAL, 1) == 2      # COW
    assert _qty(view, macro, O.MO_BUY_ANIMAL, 2) == 3      # SHEEP
    assert _qty(view, macro, O.MO_BUY_SEED, spec.I_WHEAT) == 12
    assert _qty(view, macro, O.MO_BUY_SEED, spec.I_MELON) == 2


def test_the_crew_is_still_clipped_to_the_purse(off, tmp_path):
    """Affordability is the one thing the schedule cannot repeal: the ask is
    clipped to the largest crew the day can field and still re-field."""
    P.macro_load(_sched(tmp_path, hands=[spec.MAX_HANDS] * ND))
    P.MACRO_EXEC_ON = True
    macro = _macro()
    rich = _hires(_view(money=100000), macro)
    poor = _hires(_view(money=60), macro)
    assert rich > poor >= 0
    assert rich == spec.MAX_HANDS


def test_the_herd_is_served_before_the_seeds(off, tmp_path):
    """The displacement `2026-09-14-melon-animal-mechanism.md` §3 traced, run
    backwards: on a purse that cannot pay for both, the schedule's animals
    survive and the seeds are the ones clipped."""
    sched = _sched(tmp_path, anim=[[0, 1, 1]] * ND,
                   tiles=[[0, 0, 0, 0, 12]] * ND)          # 12 melon at 80 = 960
    P.macro_load(sched)
    P.MACRO_EXEC_ON = True
    macro = _macro()
    view = _view(money=1100)                # short of 960 + 400 + 500
    animals = _qty(view, macro, O.MO_BUY_ANIMAL)
    melon = _qty(view, macro, O.MO_BUY_SEED, spec.I_MELON)
    assert animals == 2, "the schedule's herd was displaced by the seed lists"
    assert melon < 12, "fixture is no longer purse-bound"


def test_an_unexecuted_animal_want_no_longer_eats_the_tiles(off, tmp_path):
    """`plant_total = n_dev - sum(animal_want)` (`brain.py:992`) is what made a
    refused herd cost crops (`2026-09-14-herd-growth-screen.md` §3). The
    schedule writes `plant_target` whole, after the decode, so the coupling
    cannot reach it: the tile line is the same with a large herd asked for and
    with none."""
    P.MACRO_EXEC_ON = True
    view = _view(money=20000)
    macro = _macro()
    P.macro_load(_sched(tmp_path, anim=[[0, 0, 0]] * ND, tiles=[[14, 0, 0, 0, 0]] * ND))
    lean = _qty(view, macro, O.MO_BUY_SEED, spec.I_WHEAT)
    P.macro_load(_sched(tmp_path, anim=[[2, 2, 2]] * ND, tiles=[[14, 0, 0, 0, 0]] * ND))
    fat = _qty(view, macro, O.MO_BUY_SEED, spec.I_WHEAT)
    assert lean == fat == 14


def test_the_schedule_is_per_day(off, tmp_path):
    hands = [0] * ND
    hands[3] = 5
    P.macro_load(_sched(tmp_path, hands=hands))
    P.MACRO_EXEC_ON = True
    macro = _macro()
    assert _hires(_view(money=9000, day=2), macro) == 0
    assert _hires(_view(money=9000, day=3), macro) == 5


def test_land_follows_the_schedule(off, tmp_path):
    land = [0] * ND
    land[5] = 1
    P.macro_load(_sched(tmp_path, land=land))
    P.MACRO_EXEC_ON = True
    macro = _macro()
    assert _qty(_view(money=9000, day=4), macro, O.MO_BUY_LAND) == 0
    assert _qty(_view(money=9000, day=5), macro, O.MO_BUY_LAND) == 1
    # and never a quadrant the purse cannot pay for
    assert _qty(_view(money=10, day=5), macro, O.MO_BUY_LAND) == 0


# ------------------------------------------------------------- MACRO_MODE

#: The ramp the EXEC-SCOPE gate executed, minus the calendar question: four
#: hands, a 0/2/3 plate, twelve wheat and two melon, and a quadrant -- against
#: a decode that asks for eight wheat, no herd and no land.
_RAMP = dict(hands=[4] * ND, anim=[[0, 2, 3]] * ND,
             tiles=[[12, 0, 0, 0, 2]] * ND, land=[1] * ND)


def _ramp_macro():
    return _macro(plant_target=np.array([8, 0, 0, 0, 0], np.int32))


def _arm(tmp_path, mode):
    P.macro_load(_sched(tmp_path, **_RAMP))
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = mode


def _row(view, macro):
    """`(hires, cows, sheep, wheat seeds, melon seeds, quadrants)`."""
    return (_hires(view, macro),
            _qty(view, macro, O.MO_BUY_ANIMAL, 1),
            _qty(view, macro, O.MO_BUY_ANIMAL, 2),
            _qty(view, macro, O.MO_BUY_SEED, spec.I_WHEAT),
            _qty(view, macro, O.MO_BUY_SEED, spec.I_MELON),
            _qty(view, macro, O.MO_BUY_LAND))


def test_the_default_mode_is_the_executor_the_gate_measured():
    assert P.MACRO_MODE == "full"
    assert P.MACRO_MODES[:4] == ("full", "hands", "hands_herd", "hands_herd_land")
    assert all(P._MACRO_SITES[n] == P._MACRO_CREW for n in (5, 6)), \
        "the crew sites are the ramp itself and fire under every crew mode"
    assert set(P._MACRO_CREW) | set(P._MACRO_HERD) | set(P._MACRO_SITES[7]) \
        | set(P._MACRO_SITES[8]) | set(P._MACRO_SITES[9]) == set(P.MACRO_MODES), \
        "a mode that fires no site at all"


def test_mode_full_is_the_whole_schedule(off, tmp_path):
    """Unchanged from the EXEC-SCOPE build: crew, herd, mix AND land."""
    _arm(tmp_path, "full")
    view = _view(money=9000, day=5)
    hires, cow, sheep, wheat, melon, land = _row(view, _ramp_macro())
    assert (hires, cow, sheep) == (4, 2, 3)
    assert (wheat, melon) == (12, 2), "the schedule's calendar is the mix"
    assert land == 1


def test_mode_hands_takes_the_crew_and_nothing_else(off, tmp_path):
    """Sites 5 + 6 only. `plant_target` and `animal_want` are the decode's, so
    the schedule's herd and its two melon tiles never reach the board, and the
    land gate is the valuation it always was (0 here, measured with the switch
    off on this very view)."""
    _arm(tmp_path, "hands")
    view = _view(money=9000, day=5)
    hires, cow, sheep, wheat, melon, land = _row(view, _ramp_macro())
    assert hires == 4, "the crew is the one thing this mode claims"
    assert (cow, sheep) == (0, 0), "the herd was written despite mode 'hands'"
    assert melon == 0, "the schedule's calendar reached plant_target"
    assert wheat > 0, "fixture no longer plants the decode's own mix"
    assert land == 0, "the land calendar fired under mode 'hands'"


def test_mode_hands_herd_writes_the_herd_but_not_the_tiles(off, tmp_path):
    """Site 1 restricted to `animal_want` -- the arm the EXEC-SCOPE report's
    §6.1 asked for: the ramp without the calendar."""
    _arm(tmp_path, "hands_herd")
    view = _view(money=9000, day=5)
    hires, cow, sheep, wheat, melon, land = _row(view, _ramp_macro())
    assert (hires, cow, sheep) == (4, 2, 3), "the ramp did not land"
    assert melon == 0, "`plant_target` is `brain.decide`'s under this mode"
    assert wheat > 0
    assert land == 0, "site 2 belongs to 'hands_herd_land'"


def test_mode_hands_herd_land_adds_the_quadrant(off, tmp_path):
    _arm(tmp_path, "hands_herd_land")
    view = _view(money=9000, day=5)
    hires, cow, sheep, wheat, melon, land = _row(view, _ramp_macro())
    assert (hires, cow, sheep) == (4, 2, 3)
    assert melon == 0, "the calendar is still the decode's"
    assert land == 1, "site 2 did not fire"


def test_an_unknown_mode_is_an_error_not_a_silent_full(off, tmp_path):
    _arm(tmp_path, "herd_only")
    with pytest.raises(ValueError, match="unknown MACRO_MODE"):
        _plan(_view(money=9000), _ramp_macro())


def test_every_mode_is_inert_while_the_switch_is_off(off, tmp_path):
    """The OFF path does not read the mode: the outer
    `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:` short-circuits first,
    so even a nonsense mode is the shipped program."""
    macro = _ramp_macro()
    views = [_view(), _view(money=12000), _view(day=20, money=6000),
             _view(nquad=2, money=9000)]
    before = [_plan(v, macro) for v in views]
    P.macro_load(_sched(tmp_path, **_RAMP))
    for mode in P.MACRO_MODES + ("herd_only",):
        P.MACRO_MODE = mode
        assert P.MACRO_EXEC_ON is False
        for i, (b, v) in enumerate(zip(before, views)):
            for j, (x, y) in enumerate(zip(b, _plan(v, macro))):
                assert np.array_equal(x, y), f"mode {mode} board {i} field {j}"


# -------------------------------------------- MACRO-CHANNELS: floors and sales

def _herd(view, macro):
    """`(goose, cow, sheep)` actually bought."""
    return tuple(_qty(view, macro, O.MO_BUY_ANIMAL, k)
                 for k in range(spec.N_ANIMALS))


def _floor_macro():
    """A decode that asks for one GOOSE and eight wheat -- so a floor has
    something of its own to keep, and a ceiling something to silence."""
    return _macro(plant_target=np.array([8, 0, 0, 0, 0], np.int32),
                  animal_want=np.array([1, 0, 0], np.int32))


def test_mode_herd_floor_takes_the_maximum_not_the_schedule(off, tmp_path):
    """The MACRO-RAMP §5.2 defect, fixed: under `"hands_herd"` the schedule is
    the whole word on `animal_want` and a zero row silences the decode's own
    herd; under `"herd_floor"` the want is `max(decode, schedule)`, so the
    plate lands on the day it is named and the decode keeps its goose on every
    day the schedule says nothing about."""
    sched = dict(_RAMP)
    sched["anim"] = [[0, 0, 0]] * ND
    sched["anim"][0] = [0, 2, 3]
    P.macro_load(_sched(tmp_path, **sched))
    P.MACRO_EXEC_ON = True
    view0, view5 = _view(money=9000), _view(money=9000, day=5)
    macro = _floor_macro()

    P.MACRO_MODE = "hands_herd"
    assert _herd(view5, macro) == (0, 0, 0), "fixture: the ceiling silences it"

    P.MACRO_MODE = "herd_floor"
    assert _herd(view0, macro) == (1, 2, 3), "the plate is a floor over the decode"
    assert _herd(view5, macro) == (1, 0, 0), "the decode's own want was silenced"


def test_mode_herd_floor_leaves_the_crew_to_the_enumeration(off, tmp_path):
    """Sites 5 and 6 are mode-gated now: a herd-only arm may not take the
    schedule's nine hands, or it is not measuring one channel."""
    sched = dict(_RAMP)
    sched["hands"] = [9] * ND
    sched["anim"] = [[0, 0, 0]] * ND   # nothing for the herd sites to add
    P.macro_load(_sched(tmp_path, **sched))
    macro = _macro(plant_target=np.array([8, 0, 0, 0, 0], np.int32))
    view = _view(money=9000, day=5)
    off_hires = _hires(view, macro)
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "herd_floor"
    assert _hires(view, macro) == off_hires
    P.MACRO_MODE = "hands_herd_floor"
    assert _hires(view, macro) == 9, "the hands mode no longer takes the crew"


def test_mode_plate0_is_day_zero_only(off, tmp_path):
    """The day-0 plate, and nothing after it: on d1-29 the herd sites are
    masked away and the plan is the decode's own."""
    P.macro_load(_sched(tmp_path, **_RAMP))     # 0/2/3 on EVERY day
    macro = _floor_macro()
    views = [_view(money=9000, day=d) for d in (1, 3, 6, 20)]
    off_rows = [_plan(v, macro) for v in views]
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "plate0"
    assert _herd(_view(money=9000, day=0), macro) == (1, 2, 3), "no plate on day 0"
    for i, (v, b) in enumerate(zip(views, off_rows)):
        for j, (x, y) in enumerate(zip(b, _plan(v, macro))):
            assert np.array_equal(x, y), f"plate0 moved day {v.day} field {j}"


def _sell_view(day=8, money=9000):
    """A board with straw in the shed and nothing else to do with it."""
    v = _view(money=money, day=day)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_STRAWBERRY] = 30
    return v._replace(shed=shed)


def _sell_macro():
    return _macro(plant_target=np.array([8, 0, 0, 0, 0], np.int32),
                  hold=np.zeros(spec.N_PRODUCTS, np.int32))


def _sell_turns(view, macro, product):
    """`{turn: units}` for every SELL row of `product` in the day plan."""
    op, a, q = _plan(view, macro)[3:6]
    out = {}
    for t in range(op.shape[0]):
        n = int(q[t][(op[t] == O.MO_SELL) & (a[t] == product)].sum())
        if n:
            out[t] = n
    return out


def test_mode_sell_moves_the_sale_onto_the_schedules_lot(off, tmp_path):
    """Site 7: the day's whole voluntary sale of a product resolves on the lot
    that carries the schedule's hour -- forward out of the late lots when the
    tape sold early, back into them when it sold late."""
    view, macro = _sell_view(), _sell_macro()
    base = _sell_turns(view, macro, spec.I_STRAWBERRY)
    assert sum(base.values()) > 0, "fixture no longer sells the strawberries"
    lots = list(P.early_lot_turns())
    assert lots == [3, 10, 18], "the lot turns moved; the mapping below is stale"

    seen = []
    for hour in (0, 3, 4, 10, 11, 18):
        sell = [[-1] * spec.N_ITEMS for _ in range(ND)]
        sell[int(view.day)][spec.I_STRAWBERRY] = hour
        P.macro_load(_sched(tmp_path, sell=sell, **_RAMP))
        P.MACRO_EXEC_ON = True
        P.MACRO_MODE = "sell"
        rows = _sell_turns(view, macro, spec.I_STRAWBERRY)
        assert len(rows) == 1, f"hour {hour} left the sale split: {rows}"
        assert sum(rows.values()) == sum(base.values()), "the volume moved"
        seen.append(next(iter(rows)))
    # The lot the hour lands in, not the turn it is emitted on: lot 1's ROW is
    # turn 1 here, because `BANK_BEFORE_LOT_ON`'s excursion carries it.
    assert seen[0] == seen[1] <= lots[0], f"hours 0 and 3 are lot 1: {seen}"
    assert seen[2] == seen[3] == lots[1], f"hours 4 and 10 are lot 2: {seen}"
    assert seen[4] == seen[5] == lots[2], f"hours 11 and 18 are lot 3: {seen}"


def test_mode_sell_past_the_last_lot_holds_the_product(off, tmp_path):
    sell = [[-1] * spec.N_ITEMS for _ in range(ND)]
    view, macro = _sell_view(), _sell_macro()
    sell[int(view.day)][spec.I_STRAWBERRY] = 23
    P.macro_load(_sched(tmp_path, sell=sell, **_RAMP))
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "sell"
    assert _sell_turns(view, macro, spec.I_STRAWBERRY) == {}, \
        "an hour past the last lot has no row left to carry it"


def test_mode_sell_touches_nothing_but_the_sale(off, tmp_path):
    """No hands site, no herd site, no tile site: the crew, the herd and the
    seed row are the decode's own, on a schedule that names all three."""
    sell = [[-1] * spec.N_ITEMS for _ in range(ND)]
    view, macro = _sell_view(), _sell_macro()
    sell[int(view.day)][spec.I_STRAWBERRY] = 12
    P.macro_load(_sched(tmp_path, sell=sell, **_RAMP))
    before = _plan(view, macro)
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "sell"
    after = _plan(view, macro)
    for j, (x, y) in enumerate(zip(before, after)):
        if j < 3:
            assert np.array_equal(x, y), f"the unit routes moved, field {j}"
    op_b, a_b, q_b = before[3:6]
    op_a, a_a, q_a = after[3:6]
    for mo in (O.MO_HIRE, O.MO_BUY_SEED, O.MO_BUY_ANIMAL, O.MO_BUY_LAND):
        assert int(q_b[op_b == mo].sum()) == int(q_a[op_a == mo].sum()), \
            f"mode 'sell' moved {mo}"


def test_mode_sell_late_is_the_delay_half_only(off, tmp_path):
    """`"sell_late"` carries the hold and not the pull-forward: an hour every
    lot already stands at or after is no change at all, where `"sell"` pulls
    the whole sale onto lot 1."""
    view, macro = _sell_view(), _sell_macro()
    base = _sell_turns(view, macro, spec.I_STRAWBERRY)
    sell = [[-1] * spec.N_ITEMS for _ in range(ND)]
    sell[int(view.day)][spec.I_STRAWBERRY] = 0
    P.macro_load(_sched(tmp_path, sell=sell, **_RAMP))
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "sell_late"
    assert _sell_turns(view, macro, spec.I_STRAWBERRY) == base, \
        "hour 0 delays nothing, so the allocation must stand"
    # ... and the hold half is shared with `"sell"`.
    sell[int(view.day)][spec.I_STRAWBERRY] = 23
    P.macro_load(_sched(tmp_path, sell=sell, **_RAMP))
    P.MACRO_MODE = "sell_late"
    assert _sell_turns(view, macro, spec.I_STRAWBERRY) == {}
    sell[int(view.day)][spec.I_STRAWBERRY] = 12
    P.macro_load(_sched(tmp_path, sell=sell, **_RAMP))
    P.MACRO_MODE = "sell_late"
    rows = _sell_turns(view, macro, spec.I_STRAWBERRY)
    assert list(rows) == [P.early_lot_turns()[2]] and \
        sum(rows.values()) == sum(base.values()), \
        f"an hour past lots 1 and 2 carries their units to lot 3: {rows}"


# ------------------------------------------------- SELL-LOT: our own clock

def _sell_view2(day=8, money=9000):
    """`_sell_view` with wheat in the shed as well, so one product can be
    pinned while the other stays with the allocator."""
    v = _sell_view(day=day, money=money)
    shed = np.array(v.shed)
    shed[spec.I_WHEAT] = 30
    return v._replace(shed=shed)


def test_mode_lot_pins_the_whole_sale_on_one_lot(off, tmp_path):
    """Site 8: `"lot1"`/`"lot2"`/`"lot3"` move the day's whole voluntary sale
    onto that lot with the allocator's own quantities, and read no schedule
    hour at all -- the rows below are all -1."""
    view, macro = _sell_view(), _sell_macro()
    base = _sell_turns(view, macro, spec.I_STRAWBERRY)
    assert sum(base.values()) > 0, "the fixture no longer sells the strawberries"
    lots = list(P.early_lot_turns())
    assert lots == [3, 10, 18], "the lot turns moved; the assertions are stale"
    P.macro_load(_sched(tmp_path, **_RAMP))       # every `sell_hour` is -1
    P.MACRO_EXEC_ON = True
    seen = []
    for k, mode in enumerate(("lot1", "lot2", "lot3")):
        P.MACRO_MODE = mode
        rows = _sell_turns(view, macro, spec.I_STRAWBERRY)
        assert len(rows) == 1, f"{mode} left the sale split: {rows}"
        assert sum(rows.values()) == sum(base.values()), \
            f"{mode} moved volume: {rows} against {base}"
        seen.append(next(iter(rows)))
    # Lot 1's ROW can stand earlier than turn 3 -- `BANK_BEFORE_LOT_ON`'s
    # excursion carries it -- so lot 1 is "at or before turn 3", not "turn 3".
    assert seen[0] <= lots[0], f"lot1 is the first lot: {seen}"
    assert seen[1] == lots[1] and seen[2] == lots[2], f"lots 2 and 3: {seen}"


def test_mode_lot_ignores_the_schedule_hour(off, tmp_path):
    """The lot modes are OUR clock: an hour that `"sell"` would obey (23 sells
    nothing at all) changes nothing under `"lot3"`."""
    view, macro = _sell_view(), _sell_macro()
    base = sum(_sell_turns(view, macro, spec.I_STRAWBERRY).values())
    sell = [[-1] * spec.N_ITEMS for _ in range(ND)]
    sell[int(view.day)][spec.I_STRAWBERRY] = 23
    P.macro_load(_sched(tmp_path, sell=sell, **_RAMP))
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "sell"
    assert _sell_turns(view, macro, spec.I_STRAWBERRY) == {}, \
        "the fixture's hour no longer holds the product under 'sell'"
    P.MACRO_MODE = "lot3"
    rows = _sell_turns(view, macro, spec.I_STRAWBERRY)
    assert list(rows) == [P.early_lot_turns()[2]] and sum(rows.values()) == base


def test_mode_lot_touches_nothing_but_the_sale(off, tmp_path):
    """No hands site, no herd site, no tile site, and no BUY row moved."""
    view, macro = _sell_view(), _sell_macro()
    P.macro_load(_sched(tmp_path, **_RAMP))
    before = _plan(view, macro)
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "lot2"
    after = _plan(view, macro)
    for j in range(3):
        assert np.array_equal(before[j], after[j]), f"the unit routes moved, {j}"
    op_b, _, q_b = before[3:6]
    op_a, _, q_a = after[3:6]
    for mo in (O.MO_HIRE, O.MO_BUY_SEED, O.MO_BUY_ANIMAL, O.MO_BUY_LAND):
        assert int(q_b[op_b == mo].sum()) == int(q_a[op_a == mo].sum()), \
            f"mode 'lot2' moved {mo}"
    assert int(q_b[op_b == O.MO_SELL].sum()) == int(q_a[op_a == O.MO_SELL].sum()), \
        "mode 'lot2' changed the volume sold"


def test_sell_lot_products_restricts_the_move(off, tmp_path):
    """`SELL_LOT_PRODUCTS` prices one product at a time: the named product is
    pinned, every other one keeps the allocator's placement."""
    view, macro = _sell_view2(), _sell_macro()
    base_s = _sell_turns(view, macro, spec.I_STRAWBERRY)
    base_w = _sell_turns(view, macro, spec.I_WHEAT)
    assert sum(base_s.values()) > 0 and sum(base_w.values()) > 0, "fixture"
    P.macro_load(_sched(tmp_path, **_RAMP))
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "lot3"
    was = P.SELL_LOT_PRODUCTS
    try:
        P.SELL_LOT_PRODUCTS = (spec.I_STRAWBERRY,)
        rows_s = _sell_turns(view, macro, spec.I_STRAWBERRY)
        rows_w = _sell_turns(view, macro, spec.I_WHEAT)
    finally:
        P.SELL_LOT_PRODUCTS = was
    assert list(rows_s) == [P.early_lot_turns()[2]] and \
        sum(rows_s.values()) == sum(base_s.values()), f"straw not pinned: {rows_s}"
    assert rows_w == base_w, f"wheat moved with straw: {rows_w} against {base_w}"
    assert P.SELL_LOT_PRODUCTS is None, "the default is OFF"


def test_mode_sheep13_is_a_windowed_sheep_floor(off, tmp_path):
    """`"sheep13"` asks for `SHEEP_FLOOR_N` sheep on `SHEEP_FLOOR_DAYS` and
    for nothing at all on any other day -- no schedule row is read, and the
    goose and cow columns stay the decode's own."""
    macro = _ramp_macro()
    lo, hi = P.SHEEP_FLOOR_DAYS
    inside = [_view(money=9000, day=d) for d in range(lo, hi + 1)]
    outside = [_view(money=9000, day=0), _view(money=9000, day=hi + 1),
               _view(money=9000, day=20)]
    before = [_plan(v, macro) for v in outside]
    base_in = [_herd(v, macro) for v in inside]
    P.macro_load(_sched(tmp_path, **_RAMP))       # anim rows are 0/2/3
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "sheep13"
    for v, was in zip(inside, base_in):
        got = _herd(v, macro)
        assert got[2] == P.SHEEP_FLOOR_N, f"day {v.day} sheep {got}"
        assert got[:2] == was[:2], \
            f"day {v.day} moved the goose/cow columns: {got} against {was}"
    for v, b in zip(outside, before):
        for j, (x, y) in enumerate(zip(b, _plan(v, macro))):
            assert np.array_equal(x, y), f"sheep13 moved day {v.day} field {j}"


# --------------------------------------- SELL-LOT: the day's shear, same day

def _pasture_view(day=8, money=9000, yield_=5, n=3):
    """A board whose only tiles are `n` sheep with a fleece ready today."""
    v = _view(money=money, day=day)
    kind, occ = np.array(v.kind), np.array(v.occ)
    t_yield, t_day = np.array(v.t_yield), np.array(v.t_day)
    for i in range(n):
        kind[i], occ[i], t_yield[i], t_day[i] = spec.KIND_PASTURE, 2, yield_, 0
    return v._replace(kind=kind, occ=occ, t_yield=t_yield, t_day=t_day)


def test_animal_same_day_is_off_by_default_and_offers_the_shear_when_on():
    """`ANIMAL_SAME_DAY_ON` adds the day's reached animal harvest to the day's
    LAST lot. OFF -- the shipped default -- no row of the day offers it at
    all, which is the defect: the fleece sits until `_end_of_day` and sells on
    tomorrow's opening row."""
    assert P.ANIMAL_SAME_DAY_ON is False, "the switch ships OFF"
    view = _pasture_view()
    macro = _macro(plant_target=np.zeros(spec.N_CROPS, np.int32),
                   hold=np.zeros(spec.N_PRODUCTS, np.int32))
    before = _plan(view, macro)
    assert _sell_turns(view, macro, spec.I_WOOL) == {}, \
        "the day already offers the shear; the switch has nothing to fix"
    was = P.ANIMAL_SAME_DAY_ON
    try:
        P.ANIMAL_SAME_DAY_ON = True
        rows = _sell_turns(view, macro, spec.I_WOOL)
        after = _plan(view, macro)
    finally:
        P.ANIMAL_SAME_DAY_ON = was
    assert list(rows) == [P.early_lot_turns()[-1]], f"not the last lot: {rows}"
    assert sum(rows.values()) == 3 * 5, f"three fleeces of five: {rows}"
    for j in range(3):
        assert np.array_equal(before[j], after[j]), \
            f"the unit routes moved, field {j}"
    op_b, _, q_b = before[3:6]
    op_a, _, q_a = after[3:6]
    for mo in (O.MO_HIRE, O.MO_BUY_SEED, O.MO_BUY_ANIMAL, O.MO_BUY_LAND):
        assert int(q_b[op_b == mo].sum()) == int(q_a[op_a == mo].sum()), \
            f"ANIMAL_SAME_DAY moved {mo}"
