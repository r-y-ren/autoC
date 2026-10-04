"""`plan.WHEAT_VOLUME_ON`: the wheat line, bought with tile turnover.

The 2026-09-03 live study prices WHEAT at +4,806 a loss in the opponents'
favour -- 372 units a season against our 246, at the identical realised 42
coins. The flow ledger over four real-engine games against the class-A tape
`opponent_tape_104502967`, both seats, reproduces it (+4,429 revenue, +4,507
net of each side's wheat purchases) and closes to an identity: of their +103.4
extra units sold, +73.9 are extra *harvest*, +8.6 extra purchases, +5.4 a
smaller feed bill and +15.5 wheat we destroy dropping into a full shed. We feed
the same herd, buy the same wheat, realise the same price and fill at hour 3
against their mean hour 12. We simply grow less: 13.0 wheat tiles on day 10 to
our 3.8, 187.0 plantings a season to our 92.9.

`PLANT_FILL_ON` already tested "plant more tiles" and lost 9,085 a game at
t -10.13 on the unit-turns it took off the animal cadence. This switch does not
touch the number of tiles the day plants: it moves `WHEAT_VOLUME_NUM /
WHEAT_VOLUME_DEN` of the day's *non-wheat* target onto WHEAT, at a preserved
`sum(plant_target)`. Wheat is the one crop whose tile is freed on the harvest
(`ongoing` False, `max_yield_day` 4), so the same standing tile count turns
over three or four times where a strawberry tile turns over once.

The `test_off_*` half is the identity half: off, `_wheat_mix` is never called
and `macro.plant_target` reaches `_derive` exactly as `brain.decide` wrote it.
The digests are the whole six-array plan on `test_route_early`'s seeded boards,
taken off a clean `git archive 41c38ac` export -- the commit this switch was
cut into, with the promoted stack at its shipped default.
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
from test_route_early import (PIN_SEEDS, _digest, _plan, _seeded_case, _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "WHEAT_VOLUME_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "WHEAT_VOLUME_ON", True)


#: Plant targets the mix rewrite is exercised on, as `brain.decide` would hand
#: them over: the shipped day-0 opening (10 WHEAT + 9 CARROT), a mid-season
#: spread, a target with no wheat at all (the gene's own "wheat is dead today"),
#: an all-wheat one and an empty one.
_TARGETS = ((10, 9, 0, 0, 0), (3, 3, 2, 2, 0), (6, 4, 3, 2, 1),
            (0, 5, 5, 5, 5), (0, 0, 0, 0, 0), (7, 0, 0, 0, 0), (1, 2, 3, 4, 5))


def _mix_cases():
    """Boards with free tiles and a purse, over a spread of days and targets."""
    for day in (0, 6, 12, 18):
        for tgt in _TARGETS:
            yield (_view(day=day, money=20_000, n_coop=2, n_ripe=6, yld=3),
                   _macro(crew_target=np.int32(6),
                          plant_target=np.asarray(tgt, np.int32),
                          hold=np.zeros(spec.N_PRODUCTS, np.int32)))


def _n_planted(plan, crop):
    """How many PLANT ops of `crop` the compiled day walks."""
    unit_op, unit_a = plan[0], plan[1]
    return int(np.sum((np.asarray(unit_op) == O.OP_PLANT)
                      & (np.asarray(unit_a) == crop)))


def _n_op(plan, op):
    return int(np.sum(np.asarray(plan[0]) == op))


# =========================================================================
# the mix rewrite itself
# =========================================================================

def test_mix_preserves_the_total():
    """The switch is a mix change, not a development change: `n_dev`,
    `animal_want`, `_seed_room` and the labour budget all read
    `sum(plant_target)` and none of them may move."""
    for tgt in _TARGETS:
        t = np.asarray(tgt, np.int32)
        out = P._wheat_mix(np, _macro(plant_target=t)).plant_target
        assert int(np.sum(out)) == int(np.sum(t)), (tgt, out)
        assert np.all(np.asarray(out) >= 0), (tgt, out)


def test_mix_never_takes_wheat_off_a_crop_the_gene_ruled_out():
    """`plant_target[I_WHEAT] > 0` is the gene's own statement that wheat is
    live today -- it carries `can_mature` and the drain mask through from
    `brain.decide` -- so a target with no wheat is returned untouched and the
    rewrite can never plant a crop that cannot reach `pay_day`."""
    for tgt in ((0, 5, 5, 5, 5), (0, 0, 0, 0, 1), (0, 0, 0, 0, 0)):
        t = np.asarray(tgt, np.int32)
        out = P._wheat_mix(np, _macro(plant_target=t)).plant_target
        assert tuple(int(x) for x in out) == tgt, (tgt, out)


def test_mix_only_ever_moves_tiles_onto_wheat():
    """Every other crop is weakly cut and WHEAT weakly gains, so the rewrite
    has one direction and the knobs cannot be read backwards."""
    for tgt in _TARGETS:
        t = np.asarray(tgt, np.int32)
        out = np.asarray(P._wheat_mix(np, _macro(plant_target=t)).plant_target)
        assert out[spec.I_WHEAT] >= t[spec.I_WHEAT], (tgt, out)
        for c in range(spec.N_CROPS):
            if c != spec.I_WHEAT:
                assert out[c] <= t[c], (tgt, out)


def test_mix_moves_more_as_the_fraction_rises(monkeypatch):
    """`NUM/DEN` is a fraction and not a count, which is what lets the ES learn
    it: monotone in the fraction, and at `NUM == DEN` the whole non-wheat
    target moves."""
    t = np.asarray((4, 6, 6, 6, 6), np.int32)
    got = []
    for num, den in ((0, 3), (1, 4), (1, 3), (1, 2), (1, 1)):
        monkeypatch.setattr(P, "WHEAT_VOLUME_NUM", num)
        monkeypatch.setattr(P, "WHEAT_VOLUME_DEN", den)
        got.append(int(P._wheat_mix(np, _macro(plant_target=t)).plant_target[spec.I_WHEAT]))
    assert got == sorted(got), got
    assert got[0] == 4 and got[-1] == int(np.sum(t)), got


def test_take_lr_hits_its_cap_exactly():
    """`_take_lr` is the largest remainder the rewrite's identity rests on."""
    for v in ((9, 5, 3, 1, 0), (2, 2, 2, 2, 2), (0, 0, 0, 0, 0), (7, 0, 0, 0, 0)):
        a = np.asarray(v, np.int32)
        for cap in range(0, int(np.sum(a)) + 1):
            got = np.asarray(P._take_lr(np, a, np.int32(cap)))
            assert int(np.sum(got)) == cap, (v, cap, got)
            assert np.all(got <= a) and np.all(got >= 0), (v, cap, got)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Digests of the whole six-array plan on `PIN_SEEDS`, taken off the tree at
#: `41c38ac` -- the commit before this switch. Regenerate only with a measured
#: reason to move the plan.
PIN = ("d4e7ca576cf7637f", "0b627c03c8178ccd", "5702eea5c8c6dee5", "ab85fff4377b3226",
       "46fecb48d2b8dd89", "9561fdea3e750fe6", "0b353de010dd650e", "b6ae535acf30126a",
       "2983c0382f4ce20a", "27dc7659bfa8076b", "7936ac26399f166e", "c01dd4d7169c0098")


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF nothing is called and the mix reaches
    `_derive` as the gene wrote it, so a theta trained before it decodes byte
    for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_ignores_the_knobs(off, monkeypatch):
    """OFF `_wheat_mix` is never called, so neither knob is read: the compiled
    day is the same at any `NUM/DEN`."""
    cases = list(_mix_cases())
    base = [_digest(_plan(v, m)) for v, m in cases]
    for num, den in ((0, 1), (1, 1), (3, 7)):
        monkeypatch.setattr(P, "WHEAT_VOLUME_NUM", num)
        monkeypatch.setattr(P, "WHEAT_VOLUME_DEN", den)
        assert [_digest(_plan(v, m)) for v, m in cases] == base, (num, den)


def test_shipped_default_is_off_and_the_knobs_are_a_proper_fraction():
    assert P.WHEAT_VOLUME_ON is False
    assert 0 < P.WHEAT_VOLUME_NUM <= P.WHEAT_VOLUME_DEN


# =========================================================================
# ON: the same tiles, more of them wheat
# =========================================================================

def test_on_plants_at_least_as_much_wheat(monkeypatch):
    """The point of the switch. Weakly more WHEAT on every board, strictly more
    somewhere -- a day whose target already had no room for another wheat tile
    (an all-wheat target, an empty one) is allowed to stand still."""
    cases = list(_mix_cases())
    monkeypatch.setattr(P, "WHEAT_VOLUME_ON", False)
    before = [_n_planted(_plan(v, m), spec.I_WHEAT) for v, m in cases]
    monkeypatch.setattr(P, "WHEAT_VOLUME_ON", True)
    after = [_n_planted(_plan(v, m), spec.I_WHEAT) for v, m in cases]
    assert all(a >= b for a, b in zip(after, before)), list(zip(before, after))
    assert sum(after) > sum(before), (sum(before), sum(after))


def test_on_does_not_plant_more_tiles(monkeypatch):
    """`PLANT_FILL_ON`'s failure, priced out by construction: the day's PLANT
    count is bounded by the same `plant_total` it was, so no unit-turn is taken
    off the animal cadence to pay for a wheat tile."""
    cases = list(_mix_cases())
    monkeypatch.setattr(P, "WHEAT_VOLUME_ON", False)
    before = [_n_op(_plan(v, m), O.OP_PLANT) for v, m in cases]
    monkeypatch.setattr(P, "WHEAT_VOLUME_ON", True)
    after = [_n_op(_plan(v, m), O.OP_PLANT) for v, m in cases]
    assert all(a <= b for a, b in zip(after, before)), list(zip(before, after))


def test_on_leaves_a_wheatless_day_alone(on):
    """A day the gene ruled wheat out compiles exactly as it does OFF."""
    cases = [(v, m) for v, m in _mix_cases()
             if int(np.asarray(m.plant_target)[spec.I_WHEAT]) == 0]
    assert cases
    got = [_digest(_plan(v, m)) for v, m in cases]
    P.WHEAT_VOLUME_ON = False
    try:
        base = [_digest(_plan(v, m)) for v, m in cases]
    finally:
        P.WHEAT_VOLUME_ON = True
    assert got == base


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03 (commit 0772ed3): the
#: day's first lot rides turn 1 behind the BUY row instead of standing on
#: `O.SELL_TURNS[0]`. This file's PIN digests were taken before that, so the
#: switch is pinned off here the way `a838700`'s stack was pinned off for the
#: digest fixtures; `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.OPEN_PUMP_ON` went on by default on 2026-09-04 (commit ff3fe12): on
#: day 0 the plan buys `OPEN_PUMP_UNITS` wheat behind the hire row and sells it
#: back from the BUY row's head slot. The PIN digests above predate it, so it
#: is pinned off here like `EARLY_SELL_ON`; `tests/test_open_pump.py` owns
#: both halves of the switch.
@pytest.fixture(autouse=True)
def _open_pump_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)


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
