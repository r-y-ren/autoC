"""`plan.ANIMAL_DEFER_ON`: the crew ramp's animal deferral, forced by a constant.

`scratchpad/shortfall/report.txt` traced `_derive`'s pass-B locals over 24 real
games and found `purchase_shortfall` is not spread over the season: days 6-7
carry 75 % of it, and 62 % of the starved coins are cow and sheep. The knob
that was supposed to answer that -- `macro.animal_defer` [g10] -- is inert
twice: it is 0 in all 960 rows of the champion theta, and it is gated on
`crew_now < macro.crew_target` where `crew_now` is read back off the hire bill
the deferral protects, so it cancels itself (`defer 256` and `defer 66` are
byte-identical plans, the `HIRE_CLAMP` post-mortem near `plan.py:829`).

ON, days at or before `ANIMAL_DEFER_LAST_DAY` price the animal lists at
`ANIMAL_DEFER_KEEP / DEFER_ONE` unconditionally -- no `crew_now`, no gene --
and later days keep the gene's expression untouched.

The `test_off_*` half is the identity half: off, the `if` is a Python-level
module-constant branch that never runs, `a_keep` is the `xp.where` it always
was, and every plan decodes byte for byte. The digest is
`test_bank_before_lot.py`'s own OFF pin -- the current shipped default (DROP,
HORIZON_DROP, ROUTE_SPLIT, SURVIVAL_WATER, TAIL_CARE, FEED_MANDATORY and
EARLY_SELL at their defaults) -- since this switch changes nothing about it
either.
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
from test_bank_before_lot import PIN
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "ANIMAL_DEFER_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "ANIMAL_DEFER_ON", True)
    monkeypatch.setattr(P, "ANIMAL_DEFER_LAST_DAY", 7)
    monkeypatch.setattr(P, "ANIMAL_DEFER_KEEP", 128)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_shipped_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_is_the_shipped_default():
    """The switch ships off."""
    assert P.ANIMAL_DEFER_ON is False


# =========================================================================
# ON: the deferral, and its inert settings
# =========================================================================

def test_on_at_full_keep_is_the_off_plan(on, monkeypatch):
    """`ANIMAL_DEFER_KEEP == DEFER_ONE` is x1.0: the forced branch runs but
    every scaled quantity is `x * 256 // 256 == x`, so ON at the inert value
    is the OFF plan exactly. This is what proves the *branch* is inert and
    the *number* is the whole switch."""
    monkeypatch.setattr(P, "ANIMAL_DEFER_KEEP", P.DEFER_ONE)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_on_before_day_zero_is_the_off_plan(on, monkeypatch):
    """`ANIMAL_DEFER_LAST_DAY < 0` covers no day: the `xp.where` never selects
    the forced value and the plan is the OFF plan."""
    monkeypatch.setattr(P, "ANIMAL_DEFER_LAST_DAY", -1)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_on_never_crashes_and_keeps_the_shape(on):
    """Safe to run across the whole pin set: no crash, ops stay in range and
    the day keeps its turn budget."""
    from kagg3 import spec
    for s in PIN_SEEDS:
        plan = _plan(*_seeded_case(s))
        op = np.asarray(plan[0])
        assert op.min() >= 0, s
        assert op.shape[1] == spec.TURNS_PER_DAY, s


def test_on_prices_animals_at_half_inside_the_window_and_full_outside(on):
    """The mechanism, direct: `_derive` hands `_candidates` the deferral scale
    as its last positional argument, so wrap it and read the number off the
    call. Inside the window it is `ANIMAL_DEFER_KEEP`, past it the gene's own
    `DEFER_ONE` (the champion theta's `animal_defer` is 0 and `crew_target`
    is 0, so the gene's branch is the inert one).

    The synthetic `PIN_SEEDS` boards never actually buy an animal -- their
    `plant_target`-only macro leaves `animal_want` at 0 -- which is why the
    plan digests do not move on them and why the wiring is checked here
    rather than through a digest."""
    seen = []
    real = P._candidates

    def spy(*args, **kw):
        seen.append(int(np.asarray(args[-1])))
        return real(*args, **kw)

    P._candidates = spy
    try:
        for s in PIN_SEEDS:
            view, macro = _seeded_case(s)
            seen.clear()
            _plan(view, macro)
            want = (P.ANIMAL_DEFER_KEEP if int(view.day) <= P.ANIMAL_DEFER_LAST_DAY
                    else P.DEFER_ONE)
            assert seen and set(seen) == {want}, (s, int(view.day), seen)
    finally:
        P._candidates = real


def test_off_prices_animals_at_full_on_every_day(off):
    """The same probe with the switch off: the gene's expression is inert
    under a zero-theta macro, so every day is `DEFER_ONE` -- which is the
    self-cancelling status quo this switch exists to bypass."""
    seen = []
    real = P._candidates

    def spy(*args, **kw):
        seen.append(int(np.asarray(args[-1])))
        return real(*args, **kw)

    P._candidates = spy
    try:
        for s in PIN_SEEDS:
            _plan(*_seeded_case(s))
        assert set(seen) == {P.DEFER_ONE}
    finally:
        P._candidates = real


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
