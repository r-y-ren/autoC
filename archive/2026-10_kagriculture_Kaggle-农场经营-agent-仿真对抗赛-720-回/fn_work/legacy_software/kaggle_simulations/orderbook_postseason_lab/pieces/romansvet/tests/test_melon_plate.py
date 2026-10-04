"""`plan.MELON_PLATE_TILES` / `MELON_PLATE_DAY`: the opening melon plate as two
programmable floats [MELONGENES].

`MELON_OPEN_ON` is the same plate as a fixed PACKAGE -- twelve tiles on day 0
plus a dump-day excursion, a `MIDDAY_PLACE` wall and the assert that forbids
`BANK_BEFORE_LOT_ON`, which the shipped ESR string carries.  These two floats
are the plate's SIZE and DATE alone: one `plant_target` rewrite on one day, the
crop harvested and sold by the ordinary lot allocator, nothing else attached --
so the pair composes with the whole shipped package and a trainer can move them
as continuous genes.

The `test_off_*` half is the identity half.  `MELON_PLATE_TILES == 0` is read
at TRACE time by `melon_plate_on`, so `_melon_plate` is never called and the
expression the planner builds is the one it built before the floats existed.
`PIN` below is taken off the **pre-switch master tree** (`d35fcfb9`), not off
this file's own output.

Coin-exactness at 0 is pinned one level up, on whole engine games rather than
on the plan: `test_off_two_boards_are_coin_exact` replays two HIBAND boards
under the shipped ESR string with and without the floats named in the switch
string and asserts both purses to the coin.  It shells out to the leg harness
and is opt-in (`KAGG3_MELONPLATE_COINS=1`), because a pytest process must never
be the thing that runs two engine games by accident [pytest suite OOM].
"""
from __future__ import annotations

import os
import subprocess
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case, _view

from kagg3 import spec
from kagg3.core import plan as P

R = "/mnt/e/_work/kaggriculture3"


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "MELON_PLATE_TILES", 0.0)
    monkeypatch.setattr(P, "MELON_PLATE_DAY", 0.0)


def _on(monkeypatch, tiles, day=0.0):
    monkeypatch.setattr(P, "MELON_PLATE_TILES", float(tiles))
    monkeypatch.setattr(P, "MELON_PLATE_DAY", float(day))


def _mix(target, day=0):
    """`_melon_plate`'s rewritten plant target on `day`."""
    macro = _macro(plant_target=np.asarray(target, np.int32))
    return [int(x) for x in P._melon_plate(np, _view(day=day), macro).plant_target]


# =========================================================================
# OFF: byte-identical to the planner the floats were cut into
# =========================================================================

#: Digests of the whole six-array plan on the first two `PIN_SEEDS` boards,
#: taken off the pre-switch master tree `d35fcfb9` at the SHIPPED switch
#: defaults (no fixture pins anything off -- the plate has to be invisible on
#: the package we actually fly, not on a stripped one).
#: Regenerate only with a measured reason to move the plan.
PIN = ("8feb802135bbe2e2", "a570427be251bf1e")


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The contract: at `MELON_PLATE_TILES == 0` every expression is the one it
    replaced, so a theta trained before the floats decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS[:2])
    assert got == PIN


def test_zero_is_the_shipped_default():
    """OFF is the default, so an unmodified import is the pinned planner."""
    assert float(P.MELON_PLATE_TILES) == 0.0
    assert not P.melon_plate_on()


def test_off_never_calls_the_rewrite(off, monkeypatch):
    """`melon_plate_on` is the only gate, and it is read at trace time."""
    called = []
    monkeypatch.setattr(P, "_melon_plate",
                        lambda *a, **k: called.append(1) or a[2])
    _plan(*_seeded_case(0))
    assert called == []


# =========================================================================
# ON: the plate is the size and the date it is asked for
# =========================================================================

def test_on_raises_melon_to_the_tile_count(monkeypatch):
    """MELON is raised to the knob and `sum(plant_target)` is preserved."""
    _on(monkeypatch, 8)
    tgt = np.zeros(spec.N_CROPS, np.int32)
    tgt[spec.I_WHEAT] = 6
    tgt[spec.I_CARROT] = 6
    got = _mix(tgt)
    assert got[spec.I_MELON] == 8
    assert sum(got) == 12


def test_on_pays_with_wheat_last(monkeypatch):
    """`_MELON_PAY_RANK`: the carrot covers the debt before the wheat does, so
    the plate cannot buy itself out of the feed and the rotation."""
    _on(monkeypatch, 4)
    tgt = np.zeros(spec.N_CROPS, np.int32)
    tgt[spec.I_WHEAT] = 6
    tgt[spec.I_CARROT] = 6
    got = _mix(tgt)
    assert got[spec.I_CARROT] == 2 and got[spec.I_WHEAT] == 6


def test_on_never_lowers_a_day_that_already_wants_more(monkeypatch):
    """The floats can only ever RAISE melon."""
    _on(monkeypatch, 4)
    tgt = np.zeros(spec.N_CROPS, np.int32)
    tgt[spec.I_MELON] = 9
    tgt[spec.I_WHEAT] = 3
    assert _mix(tgt)[spec.I_MELON] == 9


def test_on_cannot_claim_more_tiles_than_the_day_plants(monkeypatch):
    """`min(TILES, plant_total)` -- the day's budget is sized against the sum."""
    _on(monkeypatch, 12)
    tgt = np.zeros(spec.N_CROPS, np.int32)
    tgt[spec.I_CARROT] = 5
    got = _mix(tgt)
    assert got[spec.I_MELON] == 5 and sum(got) == 5


@pytest.mark.parametrize("day", [0, 2, 4])
def test_on_touches_that_day_and_no_other(monkeypatch, day):
    """`MELON_PLATE_DAY` is the only day rewritten."""
    _on(monkeypatch, 8, day)
    tgt = np.zeros(spec.N_CROPS, np.int32)
    tgt[spec.I_CARROT] = 10
    assert _mix(tgt, day=day)[spec.I_MELON] == 8
    for other in (d for d in (0, 2, 4, 7) if d != day):
        assert _mix(tgt, day=other)[spec.I_MELON] == 0


# =========================================================================
# OFF: coin-exact on whole engine games
# =========================================================================

#: The two HIBAND boards the coin pin is taken on, and the margins the shipped
#: ESR package scores on them with the floats ABSENT from the switch string.
#: Measured 2026-09-19 (MELONGENES1) with `S/melongenes/run_grid.sh base`.
COIN_BOARDS = ("110504774", "110516257")


@pytest.mark.skipif(os.environ.get("KAGG3_MELONPLATE_COINS") != "1",
                    reason="opt-in: runs two engine games [pytest suite OOM]")
def test_off_two_boards_are_coin_exact():
    """Naming the floats at 0 in the switch string moves not one coin."""
    out = subprocess.run(
        ["bash", f"{R}/S/melongenes/coin_pin.sh"],
        capture_output=True, text=True, timeout=1800)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "COIN-EXACT" in out.stdout, out.stdout
