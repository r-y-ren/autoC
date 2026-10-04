"""`plan.HIRE_ROW_ON`: hire the hands the day's route actually loads.

The crew size the enumeration picks (`n_hire`, `plan.py:1.5`) is an *intent*:
it sets `n_units`, `wide`, `route_base`, the bill and reserve `_derive` spends
against, `turn_budget`, `land_lead` and the admit stage's labour, and `_routes`
then cuts the day's ranks across that many units. The cut routinely runs out of
ranks before it runs out of units -- 17.06 hand-days a game under `flow58_g450`
are hands whose whole route came back PASS (`S/allday_idle/report.md`, 960
exactly re-planned day-rows).

ON, the HIRE market row alone is clamped to the hands that carry a route, and
nothing else moves. That decoupling is the whole switch: the retired
`HIRE_CLAMP_ON` clamped the *intent* against pass A's pre-purchase board, hired
fewer hands than `_routes` could load on 2.38 day-rows a game and cost -3,203.

+889 coins of hire bill a game is under the panel's paired noise floor, so this
file is the acceptance test rather than a t-test: OFF is pinned byte-identical,
and ON is pinned to change the HIRE row and only the HIRE row, by exactly the
hands `_routes` left idle.
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
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "HIRE_ROW_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "HIRE_ROW_ON", True)


#: Digests of the whole six-array plan on `test_route_early`'s 12 seeded
#: boards, taken off a clean tree at `a54f16f` -- the commit this switch was
#: cut into, with `ROUTE_SPLIT_ON`, `TAIL_CARE_ON`, `SURVIVAL_WATER_ON` and
#: `FEED_MANDATORY_ON` at their shipped defaults, which is why they are not
#: `test_route_early.PIN`. Regenerate only with a measured reason to move the
#: plan.
PIN = ("d4e7ca576cf7637f", "0b627c03c8178ccd", "5702eea5c8c6dee5", "ab85fff4377b3226",
       "46fecb48d2b8dd89", "9561fdea3e750fe6", "0b353de010dd650e", "b6ae535acf30126a",
       "2983c0382f4ce20a", "27dc7659bfa8076b", "7936ac26399f166e", "c01dd4d7169c0098")

#: A wider sweep than the pin for the ON invariants: same generator, so the
#: boards mix days that buy land with days that do not, wide crews and narrow.
CASE_SEEDS = tuple(range(24))


def _hires(plan):
    """Hands the plan's market rows ask for, over both HIRE turns."""
    op, _, qty = plan[3:6]
    return int(sum(int(qty[t, s]) for t in range(op.shape[0])
                   for s in range(op.shape[1]) if int(op[t, s]) == O.MO_HIRE))


def _acting(plan):
    """Indices of the hands that do anything at all today (unit 0 is the
    farmer, who is never hired)."""
    unit_op = np.asarray(plan[0])
    return [u for u in range(1, spec.MAX_UNITS) if (unit_op[u] != O.OP_PASS).any()]


def _both(seed):
    """The same board planned OFF and ON."""
    case = _seeded_case(seed)
    P.HIRE_ROW_ON = False
    off_plan = _plan(*case)
    P.HIRE_ROW_ON = True
    on_plan = _plan(*case)
    P.HIRE_ROW_ON = False
    return off_plan, on_plan


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF `n_hire_row` *is* `n_hire` and the `if`
    compiles nothing, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


# =========================================================================
# ON: the HIRE row moves, and only the HIRE row
# =========================================================================

def test_on_moves_the_hire_row_and_nothing_else():
    """Route ops, arguments, quantities and every non-HIRE market cell -- the
    BUY rows, the SELL lots, BUY_LAND -- are identical. Nothing upstream of
    `_market` reads `n_hire_row`, so this is the whole behavioural delta."""
    for seed in CASE_SEEDS:
        off_plan, on_plan = _both(seed)
        for i, name in enumerate(("unit_op", "unit_arg", "unit_qty")):
            assert np.array_equal(np.asarray(off_plan[i]), np.asarray(on_plan[i])), \
                f"seed {seed}: {name} moved"
        o1, a1, q1 = (np.asarray(x) for x in off_plan[3:6])
        o2, a2, q2 = (np.asarray(x) for x in on_plan[3:6])
        keep = (o1 != O.MO_HIRE) & (o2 != O.MO_HIRE)
        assert np.array_equal(o1[keep], o2[keep]), f"seed {seed}: a market op moved"
        assert np.array_equal(a1[keep], a2[keep]), f"seed {seed}: a market arg moved"
        assert np.array_equal(q1[keep], q2[keep]), f"seed {seed}: a market qty moved"
        assert _hires(on_plan) <= _hires(off_plan), f"seed {seed}: ON hired more"


def test_on_leaves_the_crew_the_plan_intends_alone():
    """`cash_reserve` and `_derive`'s `hire_bill` -- the two channels the hire
    count has into the day's purchases, and the second is where `crew_now`
    (:2177) and the g10 animal deferral read the crew -- see the *unclamped*
    `n_hire` ON, argument for argument. That is what keeps the deferral
    byte-identical for a future theta whose `animal_defer` is not 0."""
    seen = {}

    def _spy(flag):
        calls = []
        real_reserve, real_derive = P.cash_reserve, P._derive
        P.cash_reserve = lambda xp, n, day: (
            calls.append(("reserve", int(np.asarray(n)), int(np.asarray(day)))),
            real_reserve(xp, n, day))[1]
        P._derive = lambda xp, v, m, pt, bill, term, res, **kw: (
            calls.append(("derive", int(np.asarray(bill)), int(np.asarray(res)))),
            real_derive(xp, v, m, pt, bill, term, res, **kw))[1]
        P.HIRE_ROW_ON = flag
        try:
            for seed in CASE_SEEDS:
                _plan(*_seeded_case(seed))
        finally:
            P.cash_reserve, P._derive, P.HIRE_ROW_ON = real_reserve, real_derive, False
        seen[flag] = calls

    _spy(False)
    _spy(True)
    assert seen[True] == seen[False]


def test_on_hires_exactly_the_hands_that_act():
    """The count is the smallest prefix of hands holding every acting one. On
    every board here the idle hands are the trailing indices -- as they were on
    all 960 replayed day-rows -- so it is also the plain population count."""
    for seed in CASE_SEEDS:
        off_plan, on_plan = _both(seed)
        acting = _acting(on_plan)
        assert acting == list(range(1, len(acting) + 1)), \
            f"seed {seed}: the acting hands are not a prefix -- {acting}"
        assert _hires(on_plan) == len(acting), \
            f"seed {seed}: hired {_hires(on_plan)} for {len(acting)} acting hands"
        assert _acting(off_plan) == acting, f"seed {seed}: the acting set moved"


def test_on_never_hires_fewer_hands_than_act():
    """The invariant `HIRE_CLAMP_ON` broke on 2.38 day-rows a game, for -3,203:
    a hand `_routes` loaded must be in the row, because the engine slices the
    rendered plan by its real hand count and hand `u` runs unit `u`'s route."""
    for seed in CASE_SEEDS:
        _, on_plan = _both(seed)
        acting = _acting(on_plan)
        assert _hires(on_plan) >= len(acting), f"seed {seed}: an acting hand was not hired"
        assert not acting or _hires(on_plan) >= acting[-1], \
            f"seed {seed}: hand {acting[-1]} acts outside the HIRE row"


def test_on_hires_the_whole_crew_when_every_hand_acts():
    """No clamp where there is nothing to clamp. Seed 1's enumeration buys 7
    hands and `_routes` loads all 7, so ON and OFF emit the same row -- and
    across the sweep ON differs from OFF on exactly the boards with an idle
    hand."""
    off_plan, on_plan = _both(1)
    assert len(_acting(on_plan)) == _hires(off_plan) == 7
    assert _hires(on_plan) == _hires(off_plan)
    for seed in CASE_SEEDS:
        off_plan, on_plan = _both(seed)
        idle = _hires(off_plan) - len(_acting(on_plan))
        assert _hires(off_plan) - _hires(on_plan) == idle, f"seed {seed}"


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the hire row) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


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
