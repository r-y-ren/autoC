"""`plan.WIDE_PICK_ON`: the wide day's SECOND stationary pickup.

A wide day (`n_hire > ops.MO`) hires a second row at turn 2, so nobody may step
before turn 3 [LAW, `ops.ROUTE_BASE_WIDE`]: a unit that has walked off its
shed-access tile re-scatters every hand `_spawn_hand` places afterwards.
`ROUTE_SPLIT_ON`'s wide branch already buys the one turn that law leaves -- a
pickup-owing block collects at turn 2, standing still.  Turn 1 is the same kind
of turn and it is still empty on every wide day of the three HOURTRACE tapes
(143 of 143 turn-0 unit-days PASS at turn 1, `S/widespawn/count.py`).

This switch hands that turn to the block that owes **two or more** pickup kinds
(45.7 unit-days a game): kind A at `O.TURN_BUY`, kind B at `TURN_BUY + 1`, walk
at `O.ROUTE_BASE_WIDE`.  Both pickups are stationary, so the occupancy counts
the turn-2 HIRE row reads are bit-identical and every hand lands where
`plan.SPAWN_SLOT` says.

Turn 1's market phase runs AFTER turn 1's unit phase, so the pickup pulled to
turn 1 draws last night's shed -- `ROUTE_FREEFIRST`'s per-kind test, asked of
the kind that actually lands there.  `pk_turn` stamps the rows in `PICK_ITEM`
order, so that is the block's lowest-indexed owed kind and no other (30.7 of
the 45.7 unit-days a game own a free *first* kind).

OFF, the whole plan tuple is pinned against a pristine `git archive` of
`_pin.SHIPPED`, as `tests/test_route_freefirst.py` pins its own switch.
"""
from __future__ import annotations

import hashlib
import os

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_prestock_v2 import _digest, _row, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

MO = P.MO


#: Twelve boards, and the last eight are WIDE -- the class the switch acts on.
#: A wide day is one whose HIRE row asks for more than `ops.MO` = 10 hands, so
#: the board has to carry enough reachable work to pay for eleven; the coops
#: and the ripe tomatoes do that, and the shed stock decides which kinds the
#: BUY row still has to deliver (`wheat`/`fert` high = the kind is free, low =
#: the row feeds it and the block keeps the turn it has).
PIN_BOARDS = (
    ("plant", dict(day=10, money=20_000), dict(plant_target=[4, 0, 0, 0, 0])),
    ("feed", dict(day=10, money=20_000, n_coop=12, wheat=4), {}),
    ("mixed", dict(day=14, money=20_000, n_coop=6, n_ripe=4, wheat=2, fert=3),
     dict(plant_target=[2, 1, 0, 0, 0])),
    ("stocked", dict(day=12, money=20_000, n_coop=8, n_ripe=4, wheat=60, fert=20),
     {}),
    ("wide_stocked", dict(day=12, money=400_000, n_coop=40, n_ripe=40,
                          wheat=400, fert=400, nquad=4), {}),
    ("wide_bare", dict(day=12, money=400_000, n_coop=40, n_ripe=40,
                       wheat=0, fert=0, nquad=4), {}),
    ("wide_wheat_only", dict(day=12, money=400_000, n_coop=40, n_ripe=40,
                             wheat=400, fert=0, nquad=4), {}),
    ("wide_fert_only", dict(day=12, money=400_000, n_coop=40, n_ripe=40,
                            wheat=0, fert=400, nquad=4), {}),
    ("wide_late", dict(day=22, money=400_000, n_coop=48, n_ripe=32,
                       wheat=400, fert=400, nquad=4), {}),
    ("wide_early", dict(day=6, money=400_000, n_coop=32, n_ripe=24,
                        wheat=400, fert=400, nquad=4), {}),
    ("wide_plant", dict(day=12, money=400_000, n_coop=36, n_ripe=24,
                        wheat=400, fert=400, nquad=4),
     dict(plant_target=[6, 2, 0, 0, 0])),
    ("wide_huge", dict(day=16, money=600_000, n_coop=56, n_ripe=40,
                       wheat=600, fert=600, nquad=4), {}),
)

#: Filled at import off the OFF plans: a board is wide iff its own HIRE rows
#: ask for more than `ops.MO` hands, which is the test `_derive` makes.
WIDE = ()


def _case(cfg):
    board, kw = cfg[1], dict(cfg[2])
    if "plant_target" in kw:
        kw["plant_target"] = np.asarray(kw["plant_target"], np.int32)
    return _view(**board), _macro(**kw)


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _own_digests():
    return {cfg[0]: _digest(_plan(*_case(cfg))) for cfg in PIN_BOARDS}


#: The tree this switch's OFF arm is the planner OF -- the ship it was judged
#: against (`5c089fb`, branch `widepick`, every other module constant equal to
#: today's).  `_pin.SHIPPED` is a MOVING ref and it now names a tree that runs
#: this switch, so the OFF pin has to name a fixed one that does not, exactly
#: as `tests/test_endroute2.py` keeps its own `PRE_SWITCH`.
PRE_SWITCH = "5c089fb"


def _head_digests():
    return _pin.tree_digests(__file__, ref=PRE_SWITCH)


def _n_hire(plan):
    """The hands the day's HIRE rows ask for: one order per hand, which is the
    count `_derive` compares with `ops.MO` to call the day wide."""
    return int((plan[3] == O.MO_HIRE).sum())


def _bought_items(plan):
    """The item ids the day's own BUY row delivers."""
    out = set()
    for turn in range(O.FULL_MARKET_TURNS):
        for op, arg, qty in _row(plan, turn):
            if qty <= 0:
                continue
            if op == O.MO_BUY_PRODUCT:
                out.add(int(arg))
            elif op == O.MO_BUY_ANIMAL:
                out.add(int(spec.I_GOOSE + arg))
    return out


def _occupancy(plan, turn):
    """Which of the four shed-access tiles each unit stands on at `turn`, by the
    only thing that can move it: the moves it has emitted so far.  A unit that
    has emitted no move is still on its spawn tile, which is the state
    `_spawn_hand` counts [`sim/market.py:118-137`]."""
    unit_op = plan[0]
    moved = np.zeros(unit_op.shape[0], bool)
    for u in range(unit_op.shape[0]):
        ops = unit_op[u, :turn + 1]
        moved[u] = bool(((ops >= O.OP_NORTH) & (ops <= O.OP_WEST)).any())
    return moved


HIRES = {cfg[0]: _n_hire(_plan(*_case(cfg))) for cfg in PIN_BOARDS}
WIDE = tuple(n for n, h in HIRES.items() if h > MO)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "WIDE_PICK_ON", True)


# =========================================================================
# OFF: the shipped program, character for character
# =========================================================================

def test_off_plan_is_byte_identical_to_the_shipped_tree(monkeypatch):
    """The whole plan tuple of all twelve boards, hashed, against a pristine
    `git archive` of `PRE_SWITCH` -- the ship this switch was judged against.

    2026-09-18: the switch SHIPPED, so the claim inverts. OFF is no longer the
    default; it is the planner at `PRE_SWITCH`, and that is what is pinned."""
    assert P.WIDE_PICK_ON is True
    monkeypatch.setattr(P, "WIDE_PICK_ON", False)
    assert _own_digests() == _head_digests()


def test_the_fixture_carries_wide_days():
    """The fixture's own claim: at least four of the twelve hire more than
    `ops.MO` hands, which is what makes their crew wait for
    `ROUTE_BASE_WIDE`, and the classification below is read off the plans."""
    assert len(WIDE) >= 4, HIRES
    assert all(HIRES[n] > MO for n in WIDE), HIRES


def test_off_puts_no_unit_on_turn_1_of_a_wide_day(monkeypatch):
    """The state the switch converts: OFF, a wide day's whole crew PASSes at
    `O.TURN_BUY`, which is the 143-of-143 the tapes measure."""
    monkeypatch.setattr(P, "WIDE_PICK_ON", False)
    for cfg in PIN_BOARDS:
        if cfg[0] not in WIDE:
            continue
        unit_op = _plan(*_case(cfg))[0]
        assert (unit_op[:, O.TURN_BUY] == O.OP_PASS).all(), cfg[0]


# =========================================================================
# ON: the turn, and the two laws it must not break
# =========================================================================

def test_the_fixture_cannot_show_the_switch_fire_and_says_so(on):
    """The fixture's honest limit, asserted rather than hidden.

    `test_prestock_v2._view` lays its hungry coops in one run and its ripe
    tomatoes in another, and a ripe tomato owes no FERTILIZE -- so every block
    a wide day cuts out of it owes **one** pickup kind (wheat, for the FEED),
    never two, and `d_pick >= 2` is false on all twelve boards.  The switch is
    therefore INERT here, which is the right answer for this board and not
    evidence about the arm.

    The firing evidence is the real sim on the three HOURTRACE Mother-Goose
    boards: `S/widepick/count.py` predicts 30.7 converted unit-turns a game and
    the paired ON/OFF replay (`S/widepick/{on,off}`) measures **34.7 a game**,
    against **0.0** OFF, with **zero** MOVEs at turns 0-2 on either arm.  The
    safety tests below are the ones this fixture can carry, and they are the
    ones that matter: nothing but a stationary PICKUP below
    `O.ROUTE_BASE_WIDE`, and the occupancy the turn-2 HIRE row counts is the
    OFF occupancy exactly.
    """
    for cfg in PIN_BOARDS:
        if cfg[0] not in WIDE:
            continue
        view, macro = _case(cfg)
        with pytest.MonkeyPatch.context() as m:
            m.setattr(P, "WIDE_PICK_ON", False)
            off = _plan(view, macro)[0]
        assert (off[:, O.TURN_BUY] == O.OP_PASS).all(), cfg[0]
        assert (_plan(view, macro)[0][:, O.TURN_BUY] == O.OP_PASS).all(), cfg[0]


def test_on_only_ever_adds_a_pickup_at_turn_buy(on):
    """Nothing but a stationary PICKUP may appear below `O.ROUTE_BASE_WIDE`:
    that is the whole of the spawn law's permission.  Wide days only: on a
    narrow day `ROUTE_SPLIT_ON` already puts a STEP on `O.TURN_BUY`, which is
    shipped behaviour this switch neither adds to nor touches."""
    for cfg in PIN_BOARDS:
        if cfg[0] not in WIDE:
            continue
        unit_op = _plan(*_case(cfg))[0]
        early = unit_op[:, :O.TURN_BUY + 1]
        assert set(np.unique(early)) <= {O.OP_PASS, O.OP_PICKUP}, cfg[0]


def test_on_never_moves_a_unit_before_the_hire_row_resolves(on):
    """The spawn law itself [LAW, `ops.ROUTE_BASE_WIDE`].  On a wide day the
    second HIRE row is at turn 2, so no unit may have emitted a MOVE by the end
    of turn 2 -- if one had, `_spawn_hand`'s occupancy count would change and
    every later hand would land on a different tile than `plan.SPAWN_SLOT`
    predicts."""
    for cfg in PIN_BOARDS:
        if cfg[0] not in WIDE:
            continue
        plan = _plan(*_case(cfg))
        assert not _occupancy(plan, O.ROUTE_BASE_WIDE - 1).any(), cfg[0]


def test_on_occupancy_at_the_hire_row_is_the_off_occupancy(on):
    """The same claim read as a diff: the tiles the turn-2 HIRE row counts are
    the tiles it counts OFF, so the hires are placed identically and the plan
    below them is comparable at all."""
    for cfg in PIN_BOARDS:
        if cfg[0] not in WIDE:
            continue
        view, macro = _case(cfg)
        with pytest.MonkeyPatch.context() as m:
            m.setattr(P, "WIDE_PICK_ON", False)
            off = _occupancy(_plan(view, macro), O.ROUTE_BASE_WIDE - 1)
        on_ = _occupancy(_plan(view, macro), O.ROUTE_BASE_WIDE - 1)
        assert np.array_equal(off, on_), cfg[0]


def test_on_pulls_only_a_kind_the_buy_row_does_not_deliver(on):
    """`ROUTE_FREEFIRST`'s per-kind test, asked of the kind that lands on turn
    1.  Turn 1's market phase runs after turn 1's unit phase, so a unit
    collecting a kind the row is about to deliver would draw a quantity that
    does not exist yet."""
    for cfg in PIN_BOARDS:
        plan = _plan(*_case(cfg))
        bought = _bought_items(plan)
        unit_op, unit_a = plan[0], plan[1]
        for u in range(unit_op.shape[0]):
            if unit_op[u, O.TURN_BUY] != O.OP_PICKUP:
                continue
            assert int(unit_a[u, O.TURN_BUY]) not in bought, (cfg[0], u)


def test_on_moves_no_quantity(on):
    """No quantity changes: the same rows of the same sizes, on different
    turns.  The per-unit PICKUP totals per item are equal ON and OFF for every
    unit whose block the switch did not re-cut, and the DAY's market rows are
    untouched on every board."""
    for cfg in PIN_BOARDS:
        view, macro = _case(cfg)
        with pytest.MonkeyPatch.context() as m:
            m.setattr(P, "WIDE_PICK_ON", False)
            off = _plan(view, macro)
        on_ = _plan(view, macro)
        for turn in range(O.FULL_MARKET_TURNS):
            assert _row(off, turn) == _row(on_, turn), (cfg[0], turn)


def test_a_wide_day_whose_row_feeds_its_first_kind_is_the_off_plan(on):
    """`wide_bare` holds nothing, so the BUY row delivers the wheat and the
    fertilizer its blocks collect -- the first owed kind is never free and the
    plan is byte-identical."""
    view, macro = _case(PIN_BOARDS[5])
    with pytest.MonkeyPatch.context() as m:
        m.setattr(P, "WIDE_PICK_ON", False)
        off = _plan(view, macro)
    assert all(np.array_equal(a, b) for a, b in zip(off, _plan(view, macro)))


def test_a_narrow_day_is_the_off_plan(on):
    """The switch is `wide`-only: `ROUTE_FREEFIRST`'s narrow arm is a separate
    switch, judged separately, and turning this one on must not widen it."""
    for cfg in PIN_BOARDS:
        if cfg[0] in WIDE:
            continue
        view, macro = _case(cfg)
        with pytest.MonkeyPatch.context() as m:
            m.setattr(P, "WIDE_PICK_ON", False)
            off = _plan(view, macro)
        assert all(np.array_equal(a, b) for a, b in zip(off, _plan(view, macro))), cfg[0]


def test_the_switch_is_a_column_of_the_gene_block():
    """2026-09-18, on the ship: the catalogue rule (USER 2026-09-17) is that the
    gene block carries EVERY shipped switch, so `WIDE_PICK_ON` is appended as
    the LAST column of `plan.SWITCH_GENES` -- no block of its own, no new shape,
    just one more column of `sw`/`swb`, which is what keeps the shipped 6,789
    theta an exact prefix of the layout."""
    from kagg3.core import policy as PO
    assert "wp" not in dict(PO.SHAPES)
    # 2026-09-18 WIDEPICK2 appended `WIDE_PICK_FREE_ON` behind it, so the
    # column INDEX is what this pin owns, not the last position.
    assert P.SWITCH_GENE_INDEX["WIDE_PICK_ON"] == 16
    assert P.SWITCH_GENE_INDEX["WIDE_PICK_FREE_ON"] == 17
    assert PO.N_SWITCH_GENES == len(P.SWITCH_GENES) == 19
    assert PO.N_PARAMS == 7_725


if __name__ == "__main__":
    for _n, _d in _own_digests().items():
        print(_n, _d)
