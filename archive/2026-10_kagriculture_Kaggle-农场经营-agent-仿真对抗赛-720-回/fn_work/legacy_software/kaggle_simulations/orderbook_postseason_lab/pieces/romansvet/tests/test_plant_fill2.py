"""`PLANT_FILL_ON` v2: work the idle tiles the herd is not holding.

`brain.decide` makes the day's development a learned fraction of the free
tiles -- `n_dev = dev_frac * n_free` (brain.py:622) -- and that fraction is the
*hard* cap on plantings: `_wants` clips the seed want to it and `plant_eff`
clips the PLANT ops to it. Measured over the 32 McGrain replays our board
carries 196.6 idle tile-days a game and 101.6 of them are still EMPTY three
days later, worth ~2,400-2,700 coins a game at our own realised wheat.

v1 of this switch (b0185b2) filled all of them in the gene's proportions and
lost 20,315 a game: the idle tiles are the reserve the herd is built out of,
and a strawberry or melon tile never gives one back. v2 prices that reserve
two ways -- it holds `PLANT_FILL_RESERVE_DAYS` days of `macro.animal_want`
free on top of today's builds (`_fill_cap`), and it fills in WHEAT alone
whenever the gene wants wheat today, because a wheat tile is `free_slot` again
inside the reserve window (`_fill_wheat`).

The reserve works and the switch still ships OFF: it loses 9,085 a game paired
over 48 seeds x 2 seats against four opponents (t -10.13) and 8,694 against
McGrain (t -3.98). The herd now survives -- wool 152 units to 136, fertilizer
191 to 144 where v1 took them to 97 and 84 -- but the fill's PLANT +22.3 and
WATER +80.8 a game come out of COLLECT_FERTILIZER -47.3, FEED -33.2 and
CARE -31.1: the scarce thing is the unit-turn, not the tile. `plan.py`'s own
switch block carries the full measurement. These tests exist so the mechanics
are pinned at both settings -- the hypothesis will be asked a third time.

The OFF half is the identity half, pinned on digests taken off a clean 38b1820
tree with every switch at its shipped default.
"""
from __future__ import annotations

import hashlib
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
from test_admit_route import TABLE, _farm
from test_budget_order import _macro, geese
from test_route_early import PIN_SEEDS, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def fill_on(monkeypatch):
    monkeypatch.setattr(P, "PLANT_FILL_ON", True)


def _wheat(n):
    return np.array([n, 0, 0, 0, 0], np.int32)


def _board(money=50_000, seeds=100, nplant=0, day=13):
    """`nplant` tiles carrying an ongoing crop that is neither ripe nor
    thirsty, the rest EMPTY -- so the free-tile count is `100 - nplant` and
    nothing else on the board competes for a turn."""
    tiles = {p: {"kind": spec.KIND_PLANT, "occ": spec.I_TOMATO, "t_day": day}
             for p in range(nplant)}
    return _farm(tiles, day=day)._replace(
        money=np.int32(money), seeds=np.full(spec.N_CROPS, seeds, np.int32))


def _wanted(view, macro):
    """Tiles whose chain starts with PLANT, off `_derive` -- the day's want
    before the route's turn budget cuts it."""
    d = P._derive(np, view, macro, TABLE, np.int32(0), False, np.int32(0))
    return int((np.asarray(d.chain_op[:, 0]) == O.OP_PLANT).sum())


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Digests of the whole six-array plan on `test_route_early`'s seeded boards,
#: taken off a clean `38b1820` tree (`git archive 38b1820`) with every switch
#: at its file default -- the shipped stack, ROUTE_SPLIT/SURVIVAL_WATER/
#: TAIL_CARE/FEED_MANDATORY on. They pin the pre-switch planner and not this
#: file's own output, and they cover the `_wants` -> `_seed_room` split as well
#: as the `plant_eff` clip, both of which OFF must re-evaluate unchanged.
PIN_38B1820 = (
    "d4e7ca576cf7637f", "0b627c03c8178ccd", "5702eea5c8c6dee5", "ab85fff4377b3226",
    "46fecb48d2b8dd89", "9561fdea3e750fe6", "0b353de010dd650e", "b6ae535acf30126a",
    "2983c0382f4ce20a", "27dc7659bfa8076b", "7936ac26399f166e", "c01dd4d7169c0098")


def test_off_plan_is_byte_identical_to_the_clean_tree():
    """OFF `_fill_wheat` is never called, no second grant is run and
    `fill_target` *is* `macro.plant_target`, so a theta trained before the
    switch decodes byte for byte."""
    assert P.PLANT_FILL_ON is False
    got = tuple(_digest(tuple(np.asarray(a) for a in P.build_day(np, *_seeded_case(s))))
                for s in PIN_SEEDS)
    assert got == PIN_38B1820


# =========================================================================
# the arithmetic: which crop the fill goes into, and how much of it
# =========================================================================

def test_the_fill_helpers_hold_their_identities():
    """Three contracts. (1) At or under the target the fill *is* the target,
    down both branches, so the helper is safe to call on any day. (2) With
    wheat live the whole surplus is wheat and no other crop moves -- the tile
    comes back inside the reserve window. (3) With wheat ruled out by the gene
    the fill falls back to v1's proportions, and a crop the softmax refused
    stays refused. Both branches agree across backends."""
    jnp = pytest.importorskip("jax.numpy")
    live = np.array([2, 1, 0, 0, 3], np.int32)
    dead = np.array([0, 3, 0, 0, 3], np.int32)
    for cap in (0, 3, 6):                       # (1) at or under sum(target) = 6
        assert list(P._fill_wheat(np, live, np.int32(cap))) == [2, 1, 0, 0, 3]
        assert list(P._fill_wheat(np, dead, np.int32(cap))) == [0, 3, 0, 0, 3]
    assert list(P._fill_wheat(np, live, np.int32(20))) == [16, 1, 0, 0, 3]   # (2)
    assert list(P._fill_wheat(np, dead, np.int32(20))) == [0, 10, 0, 0, 10]  # (3)
    z = np.zeros(spec.N_CROPS, np.int32)
    assert list(P._fill_wheat(np, z, np.int32(40))) == [0] * spec.N_CROPS
    for t in (live, dead, z):
        for cap in (0, 5, 20, 37):
            a = P._fill_wheat(np, t, np.int32(cap))
            b = P._fill_wheat(jnp, jnp.asarray(t), jnp.int32(cap))
            assert list(a) == [int(x) for x in b], (list(t), cap)


# =========================================================================
# ON: the reserve rule
# =========================================================================

def test_on_fills_only_the_tiles_beyond_the_reserve(fill_on):
    """Ten free tiles, a gene target of one wheat, and a herd that wants two
    geese a day. Today's builds take two tiles (`_seed_room`, no free coop),
    which leaves eight; `PLANT_FILL_RESERVE_DAYS = 3` days of the same
    acquisition holds six of those, so the fill takes two -- and with no herd
    at all it takes all ten."""
    assert P.PLANT_FILL_RESERVE_DAYS == 3
    view = _board(nplant=90)
    assert _wanted(view, _macro(plant_target=_wheat(1))) == 10
    assert _wanted(view, _macro(plant_target=_wheat(1), animal_want=geese(2))) == 2


def test_on_leaves_the_reserve_free_when_placements_are_due(fill_on):
    """Four geese a day against ten free tiles: today's builds take four and
    three days of them want twelve more, so there is nothing to fill with and
    the day plants exactly the gene's target -- the fill can only ever add."""
    view = _board(nplant=90)
    for want, target in ((4, 1), (4, 3), (9, 1)):
        macro = _macro(plant_target=_wheat(target), animal_want=geese(want))
        assert _wanted(view, macro) == target


def test_on_is_byte_identical_when_no_tile_is_idle(fill_on):
    """A hundred worked tiles: `seed_cap` is zero, the cap is zero, the fill is
    the identity and the second grant asks for nothing the first did not."""
    view = _board(nplant=100)
    for target, want in ((0, 0), (6, 0), (6, 2), (40, 1)):
        macro = _macro(plant_target=_wheat(target), animal_want=geese(want))
        on = _digest(tuple(np.asarray(a) for a in P.build_day(np, view, macro)))
        P.PLANT_FILL_ON = False                 # the fixture restores it
        try:
            off = _digest(tuple(np.asarray(a) for a in P.build_day(np, view, macro)))
        finally:
            P.PLANT_FILL_ON = True
        assert on == off, (target, want)


def test_on_funds_the_fill_out_of_the_leftover(fill_on):
    """The funding rule v1 learned the hard way: a first cut raised the seed
    want inside `_wants`, the extra seeds entered the day's one greedy beside
    the animals and won it (~16x value per coin against a goose's ~8x), and the
    herd stopped being bought. Funded out of the grant's leftover the goose is
    bought first and the fill takes what is left, so the animal row is the OFF
    row byte for byte and only the seed row moves."""
    view = _board(nplant=90, seeds=0, money=390)
    macro = _macro(plant_target=_wheat(1), animal_want=geese(1))

    def bought():
        op, _, qty = P.build_day(np, view, macro)[3:6]
        return (int(qty[op == O.MO_BUY_SEED].sum()),
                int(qty[op == O.MO_BUY_ANIMAL].sum()))

    on = bought()
    P.PLANT_FILL_ON = False
    try:
        off = bought()
    finally:
        P.PLANT_FILL_ON = True
    assert on[1] == off[1] == 1                 # the herd is untouched
    assert off[0] == 1                          # OFF buys the gene's one seed
    assert 1 < on[0] <= 6                        # the leftover, inside the reserve


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the plant fill) is a question the switch does
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
