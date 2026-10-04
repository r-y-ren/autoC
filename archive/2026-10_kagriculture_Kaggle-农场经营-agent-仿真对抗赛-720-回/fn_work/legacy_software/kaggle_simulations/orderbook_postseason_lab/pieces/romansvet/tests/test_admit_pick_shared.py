"""H5: charge the pickup allowance to the crew once, not to every unit
(`plan.ADMIT_PICK_SHARED`).

Admission charges `_pickup_kinds(d)` turns to each of `n_units`; `_routes`
then charges each unit only the kinds its own block consumes. On a day whose
pickup demand is concentrated the difference is admitted work the crew has the
turns for and never gets, and the units that run their stripe out PASS.

The switch is OFF by default and these tests toggle it explicitly.
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
from test_budget_order import _macro, geese

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


def _busy_view(n_animals=25, n_plants=75, day=10):
    """A wide board with two live pickup kinds: hungry animals want feed wheat
    and thirsty plants want fertilizer, so `_pickup_kinds` is 2 while the
    demand sits in only a couple of the crew's blocks."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    kind[:n_animals] = spec.KIND_COOP
    occ[:n_animals] = 0                                  # geese
    lo = 100 - n_plants
    kind[lo:] = spec.KIND_PLANT
    occ[lo:] = spec.I_TOMATO
    t_cons = z.copy()
    t_cons[:n_animals] = 1                               # unfed yesterday
    t_cons[lo:] = 1                                      # unwatered yesterday
    t_day = z.copy()
    t_day[lo:] = day - 8                                 # in a fertilizer window
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = 60
    shed[spec.I_FERT] = 90
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy() + 1, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(60_000), nquad=np.int32(4),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _quiet_view(day=10):
    """Harvest-only work: nothing wants a pickup, so the switch has nothing to
    hand back."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    kind[:40] = spec.KIND_PLANT
    occ[:40] = spec.I_WHEAT
    t_day = z.copy() + (day - 4)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy() + 6, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(60_000),
        nquad=np.int32(4), price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _ops(view, macro):
    unit_op = P.build_day(np, view, macro)[0]
    return np.asarray(unit_op)


def _working_turns(view, macro):
    """Unit-turns that are not a PASS."""
    return int((_ops(view, macro) != O.OP_PASS).sum())


MACRO = _macro(animal_want=geese(0))


def test_switch_off_is_unchanged(monkeypatch):
    monkeypatch.setattr(P, "ADMIT_PICK_SHARED", False)
    off = _ops(_busy_view(), MACRO)
    # Re-running with the switch still off has to give the very same plan.
    assert np.array_equal(off, _ops(_busy_view(), MACRO))


def test_a_day_with_no_pickup_demand_is_identical(monkeypatch):
    """`_pickup_kinds == 0` makes the two expressions the same number, so the
    switch cannot move a day that carries nothing."""
    view = _quiet_view()
    monkeypatch.setattr(P, "ADMIT_PICK_SHARED", False)
    off = _ops(view, MACRO)
    monkeypatch.setattr(P, "ADMIT_PICK_SHARED", True)
    assert np.array_equal(off, _ops(view, MACRO))


def test_switch_on_admits_more_work_when_pickups_are_charged_per_unit(monkeypatch):
    view = _busy_view()
    monkeypatch.setattr(P, "ADMIT_PICK_SHARED", False)
    off = _working_turns(view, MACRO)
    monkeypatch.setattr(P, "ADMIT_PICK_SHARED", True)
    on = _working_turns(view, MACRO)
    assert on > off, f"expected the switch to fill idle turns, got {off} -> {on}"


def test_the_mandatory_tier_still_leads(monkeypatch):
    """The extra admission comes off the value tail, so it must not cost the
    day a feed it was already doing [LAW, 0.5]."""
    view = _busy_view()
    monkeypatch.setattr(P, "ADMIT_PICK_SHARED", False)
    off = int((_ops(view, MACRO) == O.OP_FEED).sum())
    monkeypatch.setattr(P, "ADMIT_PICK_SHARED", True)
    assert int((_ops(view, MACRO) == O.OP_FEED).sum()) >= off
