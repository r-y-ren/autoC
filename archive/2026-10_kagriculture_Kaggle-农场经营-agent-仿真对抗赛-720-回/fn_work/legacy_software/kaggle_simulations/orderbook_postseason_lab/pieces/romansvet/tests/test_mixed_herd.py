"""One day, more than one animal (PLANNER_V3_1 section 1.3).

`Macro.animal_kind` was `argmax(grow[EGG], grow[MILK], grow[WOOL])` -- one kind
for the whole day -- and `xp.argmax` returns the *first* maximum. At z = 0 the
three grow scores are equal, so an untrained policy bought geese and nothing
else, on every board, for the whole season. That is not a tie-break detail: it
is the initial policy's entire herd, and it is the wrong answer on the
planner's own arithmetic, where a cow's twelve milk fires plus the same
fertilizer beat a goose's eggs per coin on a blank day-0 board.

The fix is not a better argmax. It is three candidate lists: the k-th goose,
the k-th cow and the k-th sheep are priced separately, each against its own
product's sales-window curve, and `budget.grant` -- a threshold over value per
coin -- takes cows until the marginal cow falls below the marginal sheep and
then takes sheep. The mixed herd is derived, not declared. It matters because
the curves differ: `T` is 332 for egg but 122 for milk and 105 for wool, so
fourteen animals of one kind saturate one curve where 10 cows + 4 sheep spread
across two.

Three slots on the BUY row is the mechanical half (`BUY_ANIMAL` is one item per
slot in the engine), which is why land had to leave that row first (M2), and
five pickup kinds is the price: a unit whose block places all three kinds owes
three animal PICKUP turns and the engine charges every one.
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
from test_budget_order import _macro, one_kind

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import budget as BUD
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
GOOSE, COW, SHEEP = 0, 1, 2


def _view(money=10_000, coops=0, pastures=0, day=0, price=None, full=False):
    """A blank owned board with `coops` COOPs and `pastures` PASTUREs at the
    head of the sweep. Every quadrant unlocked, so land never enters.

    `full` plants every remaining tile with strawberries -- an ongoing crop, so
    they never read as free slots -- which is how a fixture says "these
    structures are the only places an animal can go"."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    if full:
        kind[coops + pastures:] = spec.KIND_PLANT
        occ = np.where(kind == spec.KIND_PLANT, spec.I_STRAWBERRY, -1).astype(np.int32)
    kind[:coops] = spec.KIND_COOP
    kind[coops:coops + pastures] = spec.KIND_PASTURE
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(4), price=BASE.copy() if price is None else price)


def _want(g=0, c=0, s=0):
    return np.array([g, c, s], np.int32)


def _row(view, macro):
    """`{animal index: quantity}` the BUY row commits."""
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    out = {}
    for slot in range(spec.MAX_MARKET_ORDERS):
        if int(op[O.TURN_BUY, slot]) == O.MO_BUY_ANIMAL and int(qty[O.TURN_BUY, slot]):
            out[int(arg[O.TURN_BUY, slot])] = int(qty[O.TURN_BUY, slot])
    return out


def _ops(plan, op):
    return int((plan[0] == op).sum())


def _placed(plan):
    """`{item index: placements}` the day's routes actually execute."""
    unit_op, unit_a = plan[0], plan[1]
    items, counts = np.unique(unit_a[unit_op == O.OP_PLACE], return_counts=True)
    return {int(i): int(c) for i, c in zip(items, counts)}


# ------------------------------------------------------------- the mix itself

def test_a_day_buys_two_kinds_when_both_clear_the_threshold():
    """Pastures free and a purse for several animals: the row carries cow *and*
    sheep quantities, not one kind's."""
    view = _view(money=10_000, pastures=6, day=0)
    row = _row(view, _macro(animal_want=_want(c=4, s=4)))
    assert row.get(COW, 0) > 0 and row.get(SHEEP, 0) > 0, row


def test_at_theta_zero_the_planner_no_longer_wants_only_geese():
    """The z = 0 argmax bug, pinned at the decode: three equal grow scores now
    split three ways instead of collapsing onto the first maximum."""
    theta = np.zeros(PO.N_PARAMS, np.float32)
    obs = brain.PolicyObs(
        day=np.int32(0), money=np.int32(3000), opp_money=np.int32(3000),
        kind=np.full(100, spec.KIND_EMPTY, np.int32),
        occ=np.zeros(100, np.int32) - 1,
        opp_kind=np.full(100, spec.KIND_EMPTY, np.int32),
        opp_occ=np.zeros(100, np.int32) - 1,
        t_day=np.zeros(100, np.int32), t_yield=np.zeros(100, np.int32),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(4), opp_nquad=np.int32(4),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32), price=BASE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))
    want = brain.decide(np, theta, obs).animal_want
    assert int(want.sum()) > 0, "the fixture asks for no animals at all"
    assert int((want > 0).sum()) > 1, f"still one kind only: {want}"


def test_the_kind_split_follows_value_per_coin_not_a_score():
    """Floor the milk market and a purse that can only stock two animals buys
    sheep instead of cows.

    Not "buys no cows": an animal's value is its product stream *plus* the
    fertilizer every animal makes, and the fertilizer alone pays for a 400-coin
    cow. What moves is the ranking -- a cow with no milk is worth less per coin
    than a sheep with wool -- and a threshold over value per coin is exactly
    what `budget.grant` is."""
    view = _view(money=700, pastures=6, day=0)
    macro = _macro(animal_want=_want(c=4, s=4))
    inv = view.mkt_inv.copy()
    inv[spec.I_MILK] = spec.MARKET_I0 + 40_000
    # a purse for one animal: a cow is 400 and a sheep 500, and 900 is out
    assert _row(view, macro) == {COW: 1}, _row(view, macro)
    assert _row(view._replace(mkt_inv=inv), macro) == {SHEEP: 1}


def test_cow_and_sheep_compete_for_the_same_pastures():
    """Two free pastures, two cows and two sheep wanted: exactly two animals
    are placed on them and the lower list index is served first."""
    view = _view(money=10_000, pastures=2, day=0, full=True)
    plan = P.build_day(np, view, _macro(animal_want=_want(c=2, s=2)))
    placed = _placed(plan)
    assert placed.get(spec.I_COW, 0) == 2, placed
    assert placed.get(spec.I_SHEEP, 0) == 0, placed
    assert _ops(plan, O.OP_BUILD_PASTURE) == 0, "there was nowhere to build"


def test_standing_structures_are_stocked_before_new_ones_are_built_per_kind():
    """0.8's rule survives the split, and it is per structure kind: the goose
    fills the free coop, the cow the free pasture, and only the surplus builds."""
    view = _view(money=10_000, coops=1, pastures=1, day=0)
    plan = P.build_day(np, view, _macro(animal_want=_want(g=2, c=2)))
    assert _ops(plan, O.OP_BUILD_COOP) == 1
    assert _ops(plan, O.OP_BUILD_PASTURE) == 1
    assert _ops(plan, O.OP_PLACE) == 4


def test_five_pickup_kinds_are_charged_when_a_day_places_all_three():
    view = _view(money=20_000, day=0)
    macro = _macro(animal_want=_want(g=2, c=2, s=2))
    plan = P.build_day(np, view, macro)
    placed = _placed(plan)
    assert set(placed) >= {spec.I_GOOSE, spec.I_COW, spec.I_SHEEP}, placed
    picks = np.unique(plan[1][plan[0] == O.OP_PICKUP])
    assert set(int(i) for i in picks) >= {spec.I_GOOSE, spec.I_COW, spec.I_SHEEP}
    assert O.MAX_PICKUPS == 2 + spec.N_ANIMALS


def test_the_buy_row_holds_exactly_ten_slots_and_never_eleven():
    """Every purchase the day can make at once: two products, five seeds and
    three animals is exactly the engine's ten, and land is elsewhere (M2)."""
    view = _view(money=100_000, day=0)
    macro = _macro(animal_want=_want(g=1, c=1, s=1),
                   plant_target=np.array([2, 2, 2, 2, 2], np.int32))
    op = P.build_day(np, view, macro)[3]
    assert int((op[O.TURN_BUY] != O.MO_NONE).sum()) <= spec.MAX_MARKET_ORDERS
    for turn in range(spec.TURNS_PER_DAY):
        assert int((op[turn] != O.MO_NONE).sum()) <= spec.MAX_MARKET_ORDERS


def test_the_shed_room_clamp_walks_the_three_animal_slots_in_order():
    """Room for two units and three kinds wanted: the clamp hands the room down
    the engine's own slot order and never over-commits the shed."""
    view = _view(money=100_000, day=0)
    shed = view.shed.copy()
    shed[spec.I_MELON] = spec.SHED_CAPACITY - 2
    view = view._replace(shed=shed)
    row = _row(view, _macro(animal_want=_want(g=2, c=2, s=2)))
    assert sum(row.values()) <= 2, row


def test_the_animal_lists_are_the_greedys_own():
    assert BUD.N_LISTS == 2 + spec.N_CROPS + spec.N_ANIMALS
    assert BUD.L_ANIMALS == tuple(range(BUD.L_ANIMAL0, BUD.L_ANIMAL0 + spec.N_ANIMALS))
    assert set(BUD.SHED_LISTS) == {BUD.L_WHEAT, BUD.L_FERT} | set(BUD.L_ANIMALS)
    assert 2 not in PO.DEAD_HEAD, "the animal-mix sharpness is decoded again"


def test_mixed_herd_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view = _view(money=20_000, coops=2, pastures=2, day=0)
    macro = _macro(animal_want=_want(g=3, c=3, s=3),
                   plant_target=np.array([4, 0, 0, 0, 0], np.int32))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))


def test_one_kind_still_works():
    """The single-kind day is a special case of the split, not a lost one."""
    view = _view(money=10_000, coops=3, day=0)
    row = _row(view, _macro(animal_want=one_kind(GOOSE, 3)))
    assert row == {GOOSE: 3}, row


def _walk(want, room, same_struct):
    """The unrolled walk `_share` replaced: clip, subtract, clip the next."""
    left = {}
    out = []
    for a in range(spec.N_ANIMALS):
        k = int(spec.ANIMAL_STRUCT[a]) if same_struct else 0
        r = left.get(k, np.int32(room[a] if same_struct else room))
        got = min(int(want[a]), max(int(r), 0))
        left[k] = int(r) - got
        out.append(got)
    return np.array(out, np.int32)


def test_share_is_the_unrolled_walk_lane_by_lane():
    """`_share` is a rewrite for the GPU tile emitter (see `plan._prefix`), not
    a new rule: it must be the running-scalar walk on every input the planner
    can hand it, or the mixed herd changes shape under it."""
    rng = np.random.default_rng(20260826)
    for _ in range(400):
        want = rng.integers(0, 9, spec.N_ANIMALS).astype(np.int32)
        room = np.int32(rng.integers(0, 12))
        got = P._share(np, want, room, P.BEFORE_ALL)
        assert np.array_equal(got, _walk(want, room, False)), (want, room, got)
        # Per-kind rooms: cow and sheep share theirs, the goose's is its own.
        coop, past = rng.integers(0, 12, 2).astype(np.int32)
        sfree = np.where(P.NEEDS_COOP, coop, past).astype(np.int32)
        got = P._share(np, want, sfree, P.BEFORE_STRUCT)
        assert np.array_equal(got, _walk(want, sfree, True)), (want, sfree, got)


def test_place_split_still_shares_the_pastures():
    """The rewrite kept `_place_split`'s whole point: cow and sheep may not
    both claim the same free pasture."""
    sfree = np.where(P.NEEDS_COOP, 0, 3).astype(np.int32)
    fs, ft = P._place_split(np, _want(g=0, c=5, s=5), np.int32(0), sfree)
    assert list(fs) == [0, 3, 0] and list(ft) == [0, 0, 0], (fs, ft)
    # What the pastures could not take spills onto the free tiles, in list order.
    fs, ft = P._place_split(np, _want(g=0, c=5, s=5), np.int32(4), sfree)
    assert list(fs) == [0, 3, 0] and list(ft) == [0, 2, 2], (fs, ft)
