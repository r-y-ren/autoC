"""`plan.MIDDAY_PLACE_ON`: bank the melon at a rank that still makes the lot.

The diagnosis is `docs/spikes/2026-09-04-midday-place.md`. In one line: melon's
`CROP_FIRST_YIELD_DAY` is 10, so day 10 is the first day its harvest exists at
all, and the only way that harvest reaches day 10's market is a unit putting it
in the shed mid-day -- `_end_of_day` runs after turn 23. `MELON_OPEN_ON` has an
excursion for exactly that, but it fires after the block's **last** melon rank
and has no time rule, so on the near-shed board it actually builds the deposit
lands on turn 22, after every row of the day.

This switch is two expressions: the candidate ranks are the melon ranks whose
deposit lands by `O.MELON_LOT_TURNS[MIDDAY_PLACE_LOT]` (the rule
`BANK_BEFORE_LOT_ON` already carries), and the deposit op is `OP_PLACE`, whose
engine fallthrough banks one item and leaves the rest on the unit, instead of
`OP_DROP`, which dumps everything and destroys the overflow.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests -- the planner at `a838700`, the same pin `test_open_pump.py` uses.
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
from test_route_early import BASE_PRICE, PIN, PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

#: The board `MELON_OPEN_ON` actually builds: `_derive`'s `near_rank` puts the
#: melon on the tiles nearest a shed access, so this is the twelve smallest
#: `DIST_SHED` there are (0 on the four access tiles themselves, then 1).
NEAR = np.argsort(np.asarray(P.DIST_SHED), kind="stable")[:12]

#: The stack `test_route_early`'s digests were taken before -- the planner at
#: `a838700`. None of these five answers anything about a mid-day deposit, and
#: pinning them off is what makes the identity claim the switch's own.
_PINNED_OFF = ("ROUTE_SPLIT_ON", "SURVIVAL_WATER_ON", "TAIL_CARE_ON",
               "FEED_MANDATORY_ON", "EARLY_SELL_ON")

#: The row every deposit is judged against.
FIRST_ROW = O.MELON_LOT_TURNS[P.MIDDAY_PLACE_LOT]


def _view(tiles, day=P.MELON_OPEN_HARVEST_DAY, yld=6, wheat=()):
    """`n` ripe melon on `tiles`, on the day the opening's melon saturates --
    plus, on `wheat`, ripe wheat, which is the day's other harvest and the
    work the melon has to be swept in front of."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    kind[tiles] = spec.KIND_PLANT
    occ[tiles] = spec.I_MELON
    t_yield[tiles] = yld
    if len(wheat):
        kind[wheat] = spec.KIND_PLANT
        occ[wheat] = spec.I_WHEAT
        t_yield[wheat] = yld
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3_000), nquad=np.int32(4), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _route(tiles=NEAR, crew=6, day=P.MELON_OPEN_HARVEST_DAY, view=None):
    plan = _plan(_view(tiles, day=day) if view is None else view,
                 _macro(crew_target=np.int32(crew)))
    return tuple(np.asarray(x) for x in plan[:3])


def _deposits(route):
    """[(turn, op, arg, qty)] of every shed deposit the day's route emits."""
    uop, ua, uq = route
    out = []
    for u in range(spec.MAX_UNITS):
        for t in np.flatnonzero((uop[u] == O.OP_DROP) | (uop[u] == O.OP_PLACE)):
            out.append((int(t), int(uop[u, t]), int(ua[u, t]), int(uq[u, t])))
    return sorted(out)


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", False)
    monkeypatch.setattr(P, "MELON_OPEN_ON", True)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", True)
    monkeypatch.setattr(P, "MELON_OPEN_ON", True)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(monkeypatch):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte. Pinned on
    `test_route_early`'s digests, the same ones `test_open_pump.py` holds its
    own switch to."""
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", False)
    monkeypatch.setattr(P, "MELON_OPEN_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_keeps_the_melon_excursion_s_drop(off):
    """OFF the excursion is `MELON_OPEN_ON`'s: an OP_DROP with no argument, at
    the block's last melon rank -- which on this board is turn 22."""
    dep = _deposits(_route())
    assert dep, "the dump day banked nothing"
    assert {op for _, op, _, _ in dep} == {O.OP_DROP}
    assert all(a == 0 and q == 0 for _, _, a, q in dep), dep
    assert all(t > FIRST_ROW for t, *_ in dep), dep


# =========================================================================
# ON: the time rule and the op
# =========================================================================

def test_on_deposits_are_a_place_of_melon(on):
    """The op is the engine's selective shed deposit, named and quantified: it
    banks melon and leaves whatever else the block still carries alone."""
    dep = _deposits(_route())
    assert dep, "the dump day banked nothing"
    for _, op, arg, qty in dep:
        assert op == O.OP_PLACE
        assert arg == spec.I_MELON
        assert qty == P.MIDDAY_PLACE_QTY


@pytest.mark.parametrize("crew", [4, 6, 8, 11])
def test_on_every_deposit_makes_the_row_that_sells_it(on, crew):
    """The time rule is the point: a rank whose deposit cannot reach the first
    melon row is not a candidate, so no excursion is ever spent on one."""
    dep = _deposits(_route(crew=crew))
    assert dep, f"crew {crew} banked nothing"
    assert all(t <= FIRST_ROW for t, *_ in dep), dep


def test_on_moves_the_near_shed_board_in_front_of_the_row(on, monkeypatch):
    """The measurement the switch exists for. On the board `MELON_OPEN_ON`
    builds, OFF deposits land on turn 22 -- after every row of the day -- and
    ON they land on turns 9 and 11, both in front of the first melon row."""
    on_dep = [t for t, *_ in _deposits(_route())]
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", False)
    off_dep = [t for t, *_ in _deposits(_route())]
    assert sum(t <= FIRST_ROW for t in off_dep) == 0, off_dep
    assert sum(t <= FIRST_ROW for t in on_dep) == len(on_dep) > 0, on_dep
    assert max(on_dep) < min(off_dep), (on_dep, off_dep)


def test_on_leaves_a_day_without_melon_alone(on):
    """Only the dump day has an excursion at all; the rule cannot invent one."""
    for day in (P.MELON_OPEN_HARVEST_DAY - 1, P.MELON_OPEN_HARVEST_DAY + 1):
        plan = _plan(_view(NEAR, day=day), _macro(crew_target=np.int32(6)))
        uop = np.asarray(plan[0])
        assert not (uop == O.OP_PLACE).any(), day


# =========================================================================
# In the simulator: the melon actually reaches the shed, on the day
# =========================================================================

def _sim_shed_by_turn(route, tiles=NEAR, until=None):
    """Play `route` through `sim.units.apply_units` on a board of ripe melon and
    return our shed's melon count after each turn.

    The unit phase alone -- no market, no end-of-day -- because the question is
    exactly "is it in the shed *during* the day", which the end-of-day would
    answer for free and so would answer nothing.
    """
    import jax.numpy as jnp

    from kagg3.sim.state import initial_state
    from kagg3.sim.units import apply_units

    uop, ua, uq = route
    st = initial_state(jnp)
    z = np.zeros((2, spec.N_TILES), np.int32)
    kind = np.asarray(st.kind).copy()
    occ = np.asarray(st.occ).copy()
    t_day, t_yield, t_cons = z.copy(), z.copy(), z.copy()
    t_life = (z - 1).copy()
    kind[0] = spec.KIND_EMPTY
    for tile in tiles:
        kind[0, tile] = spec.KIND_PLANT
        occ[0, tile] = spec.I_MELON
        t_day[0, tile] = -int(P.MELON_OPEN_HARVEST_DAY)
        t_yield[0, tile] = 6
        t_cons[0, tile] = 1
        t_life[0, tile] = 100_000
    upos = np.asarray(st.upos).copy()
    for u in range(spec.MAX_UNITS):
        upos[0, u] = int(P.SPAWN_Y[u]) * spec.BOARD + int(P.SPAWN_X[u])
    nhands = np.asarray(st.nhands).copy()
    nhands[0] = spec.MAX_UNITS - 1
    nquad = np.asarray(st.nquad).copy()
    nquad[0] = 4
    st = st._replace(
        kind=jnp.asarray(kind), occ=jnp.asarray(occ), t_day=jnp.asarray(t_day),
        t_yield=jnp.asarray(t_yield), t_cons=jnp.asarray(t_cons),
        t_life=jnp.asarray(t_life), upos=jnp.asarray(upos),
        nhands=jnp.asarray(nhands), nquad=jnp.asarray(nquad))

    zero = jnp.zeros((spec.MAX_UNITS, spec.TURNS_PER_DAY), jnp.int32)
    b_op = jnp.stack([jnp.asarray(uop), zero])
    b_a = jnp.stack([jnp.asarray(ua), zero])
    b_q = jnp.stack([jnp.asarray(uq), zero])
    out = []
    for h in range(spec.TURNS_PER_DAY if until is None else until + 1):
        st = apply_units(jnp, st, jnp.int32(0), b_op[:, :, h], b_a[:, :, h],
                         b_q[:, :, h])
        out.append(int(np.asarray(st.shed)[0, spec.I_MELON]))
    return out


def test_on_puts_melon_in_the_shed_before_the_first_row(on, monkeypatch):
    """The whole claim, in the simulator: with the switch on, our shed holds
    melon by the turn the first melon row resolves; with it off it holds none
    at any turn of the day, because the only deposit is at turn 22 and the
    day's rows are gone by then."""
    on_shed = _sim_shed_by_turn(_route())
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", False)
    off_shed = _sim_shed_by_turn(_route())
    assert off_shed[FIRST_ROW] == 0, off_shed
    assert on_shed[FIRST_ROW] > 0, on_shed
    # Every melon a deposit banks is six units a tile, so the count is a
    # multiple of six and it is what the excursions carried.
    assert on_shed[FIRST_ROW] % 6 == 0, on_shed


# =========================================================================
# The simulator's own PLACE-to-shed branch
# =========================================================================

def _one_turn(op, arg, qty, inv, pos=44, kind=None):
    """One unit standing on `pos` with `inv` in hand, taking one op."""
    import jax.numpy as jnp

    from kagg3.sim.state import initial_state
    from kagg3.sim.units import apply_units

    st = initial_state(jnp)
    k = np.asarray(st.kind).copy()
    k[0] = spec.KIND_EMPTY
    if kind is not None:
        k[0, pos] = kind
    upos = np.asarray(st.upos).copy()
    upos[0, 0] = pos
    iv = np.asarray(st.inv).copy()
    seq = np.asarray(st.inv_seq).copy()
    for n, (item, count) in enumerate(inv.items()):
        iv[0, 0, item] = count
        seq[0, 0, item] = n + 1
    st = st._replace(kind=jnp.asarray(k), upos=jnp.asarray(upos),
                     inv=jnp.asarray(iv), inv_seq=jnp.asarray(seq))
    uop = np.zeros((2, spec.MAX_UNITS), np.int32)
    ua = np.zeros((2, spec.MAX_UNITS), np.int32)
    uq = np.zeros((2, spec.MAX_UNITS), np.int32)
    uop[0, 0], ua[0, 0], uq[0, 0] = op, arg, qty
    st = apply_units(jnp, st, jnp.int32(0), jnp.asarray(uop), jnp.asarray(ua),
                     jnp.asarray(uq))
    return np.asarray(st.shed)[0], np.asarray(st.inv)[0, 0]


def test_sim_place_banks_one_item_and_keeps_the_rest():
    """The engine's PLACE fallthrough (`kaggriculture.py:377-408`) banks
    `min(qty, inv[item])` of the named item and leaves everything else on the
    unit. That is what makes a mid-block deposit safe."""
    shed, inv = _one_turn(O.OP_PLACE, spec.I_MELON, 100,
                          {spec.I_MELON: 12, spec.I_WHEAT: 5})
    assert shed[spec.I_MELON] == 12
    assert shed[spec.I_WHEAT] == 0
    assert inv[spec.I_MELON] == 0
    assert inv[spec.I_WHEAT] == 5


def test_sim_drop_still_takes_everything():
    """And DROP is unchanged: the whole load, feed wheat included."""
    shed, inv = _one_turn(O.OP_DROP, 0, 0, {spec.I_MELON: 12, spec.I_WHEAT: 5})
    assert shed[spec.I_MELON] == 12 and shed[spec.I_WHEAT] == 5
    assert inv.sum() == 0


def test_sim_place_obeys_the_shed_cap_without_destroying_the_remainder():
    """DROP destroys what does not fit; PLACE leaves it on the unit."""
    shed, inv = _one_turn(O.OP_PLACE, spec.I_MELON, spec.SHED_CAPACITY + 40,
                          {spec.I_MELON: spec.SHED_CAPACITY + 40})
    assert shed[spec.I_MELON] == spec.SHED_CAPACITY
    assert inv[spec.I_MELON] == 40


def test_sim_place_away_from_the_shed_banks_nothing():
    """It is a shed op: the unit has to be orthogonally adjacent to the shed."""
    shed, inv = _one_turn(O.OP_PLACE, spec.I_MELON, 100, {spec.I_MELON: 12},
                          pos=0)
    assert shed[spec.I_MELON] == 0 and inv[spec.I_MELON] == 12


def test_sim_animal_place_still_wins_over_the_shed():
    """An animal onto a matching free structure is the engine's first branch and
    it returns there, so it never reaches the shed path -- even standing on a
    shed-access tile."""
    shed, inv = _one_turn(O.OP_PLACE, spec.I_COW, 1, {spec.I_COW: 1},
                          pos=44, kind=spec.KIND_PASTURE)
    assert shed[spec.I_COW] == 0 and inv[spec.I_COW] == 0


# =========================================================================
# V2: the harvest day's chain, and the row the deposit is judged against
# =========================================================================

#: The shape the real board has: `_derive`'s nearest free tiles inside one
#: unlocked quadrant run `DIST_SHED` 2..5, not the 0-and-1 of `NEAR`.
FAR = np.arange(12)


@pytest.fixture
def v2(monkeypatch):
    monkeypatch.setattr(P, "MELON_OPEN_ON", True)
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", True)
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", True)


def test_v2_judges_the_deposit_against_the_day_s_last_row(v2, monkeypatch):
    """One reader, two answers: V2's deadline is the last row of the day that
    sells out of the shed, V1's is the first melon lot."""
    assert P._midday_place_turn() == P.MIDDAY_PLACE_V2_TURN == O.SELL_TURNS[-1]
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", False)
    assert P._midday_place_turn() == O.MELON_LOT_TURNS[P.MIDDAY_PLACE_LOT]


def test_v2_admits_a_deposit_the_first_row_refuses(v2, monkeypatch):
    """The rule the switch moves. V1 will only take a deposit that makes the
    *first* melon row, and on the real board no melon deposit ever does -- the
    measured turns are 13 to 27 (`S/mp2/`), so the excursion is never taken
    and the whole harvest rides to day 11 hour 0. V2 judges it against the
    day's last selling row instead, and here that is exactly the deposit V1
    refuses: turn 15 rather than turn 11."""
    v2_dep = _deposits(_route(tiles=FAR, crew=9))
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", False)
    v1_dep = _deposits(_route(tiles=FAR, crew=9))
    assert v2_dep, "the dump day banked nothing"
    assert all(t <= P.MIDDAY_PLACE_V2_TURN for t, *_ in v2_dep), v2_dep
    assert max(t for t, *_ in v2_dep) > FIRST_ROW, v2_dep
    assert all(t <= FIRST_ROW for t, *_ in v1_dep), v1_dep
    for _, op, arg, qty in v2_dep:
        assert (op, arg, qty) == (O.OP_PLACE, spec.I_MELON, P.MIDDAY_PLACE_QTY)


def test_v2_never_costs_the_day_a_harvest(v2, monkeypatch):
    """What leaves the harvest day is the *replant*, never the harvest or the
    watering that pays the sixth unit for it: melon is a one-time crop, so
    `_daily_refresh_plants` skips it and day 10's own watering is the last
    unit of the six."""
    v2_ops = np.asarray(_route(tiles=FAR, crew=9)[0])
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", False)
    v1_ops = np.asarray(_route(tiles=FAR, crew=9)[0])
    assert (v2_ops == O.OP_HARVEST).sum() == (v1_ops == O.OP_HARVEST).sum()
    assert (v2_ops == O.OP_WATER).sum() == (v1_ops == O.OP_WATER).sum()


def test_v2_leaves_a_day_without_ripe_melon_alone(v2):
    """The trigger is the crop, so a day whose melon is not ripe yet has no
    excursion and no shortened chain -- `_view` dates every plant to day 0, so
    below `CROP_SATURATE_AGE` nothing harvests and nothing banks."""
    for day in (P.MELON_OPEN_HARVEST_DAY - 1, P.MELON_OPEN_HARVEST_DAY - 4):
        plan = _plan(_view(FAR, day=day), _macro(crew_target=np.int32(9)))
        uop = np.asarray(plan[0])
        assert not (uop == O.OP_PLACE).any(), day


def test_v2_banks_a_melon_day_that_is_not_the_opening_s(v2):
    """The switch's second measurement (`S/mp2/`, the coordinator's ledger):
    the default build plants melon on days 4-6 and harvests it on 13-16, and
    V1's excursion is nailed to `MELON_OPEN_HARVEST_DAY`, so those harvests
    ride to the next morning and sell at ~150 instead of ~200. V2 reads the
    crop, not the calendar."""
    for day in (P.MELON_OPEN_HARVEST_DAY + 3, P.MELON_OPEN_HARVEST_DAY + 6):
        dep = _deposits(_route(tiles=FAR, crew=9, day=day))
        assert dep, f"day {day} banked nothing"
        assert all(t <= P.MIDDAY_PLACE_V2_TURN for t, *_ in dep), (day, dep)
        for _, op, arg, qty in dep:
            assert (op, arg, qty) == (O.OP_PLACE, spec.I_MELON,
                                      P.MIDDAY_PLACE_QTY)


def test_v2_needs_no_melon_opening_to_have_an_excursion(monkeypatch):
    """And it stands alone: `MELON_OPEN_ON` is the opening's twelve day-0
    tiles, not the mid-day deposit, so V2 supplies the excursion itself on
    every ripe day. Without it -- `MIDDAY_PLACE_ON` alone off the shipped
    default -- there is no excursion to move and the day banks nothing."""
    monkeypatch.setattr(P, "MELON_OPEN_ON", False)
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", True)
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", True)
    assert _deposits(_route(tiles=FAR, crew=9))
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", False)
    assert not _deposits(_route(tiles=FAR, crew=9))


def test_v2_banks_the_melon_with_the_day_s_other_harvests_on_the_board(v2):
    """The day's half of the reorder, on a board that has other work to be
    swept in front of. A block is a contiguous run of the route order, so a
    melon rank the order leaves late is a melon rank *no* block can bank in
    time however the block sweeps itself -- the tier moves the melon to the
    head of the route order instead, where the blocks that can reach the shed
    own it. Twelve ripe melon behind twenty-four ripe wheat still bank inside
    the day here; the size of the effect is the engine's to measure, and it is
    30 -> 60 of 72 units on the dump day (`S/mp2/`)."""
    dep = _deposits(_route(view=_view(FAR, wheat=np.arange(40, 64)), crew=9))
    assert dep, "the melon behind the wheat never reached the shed"
    assert all(t <= P.MIDDAY_PLACE_V2_TURN for t, *_ in dep), dep
    for _, op, arg, qty in dep:
        assert (op, arg, qty) == (O.OP_PLACE, spec.I_MELON, P.MIDDAY_PLACE_QTY)


# =========================================================================
# V2: the row that sells what the deposit banked
# =========================================================================

def _melon_offer(plan, turn):
    """Units of MELON the day's market schedule offers on `turn`."""
    mop, ma, mq = (np.asarray(x) for x in plan[3:6])
    return int(sum(int(mq[turn, s])
                   for s in range(spec.MAX_MARKET_ORDERS)
                   if int(mop[turn, s]) == O.MO_SELL
                   and int(ma[turn, s]) == spec.I_MELON))


def test_v2_offers_the_banked_melon_on_the_day_s_last_row(v2, monkeypatch):
    """The half the deposit is worthless without. `SELL.allocate` runs once at
    dawn against the hour-0 shed, and on a harvest day the melon is still on
    the vine, so melon's slot in all three lots is empty and the PLACE lands
    in a shed no row of the day offers -- measured on the real engine, every
    banked unit rode to the next morning's opening row. V2 adds what the
    excursion banked to the day's last lot, the only row a deposit judged
    against `MIDDAY_PLACE_V2_TURN` can reach."""
    day = P.MELON_OPEN_HARVEST_DAY + 3      # a ripe day that is not the dump day
    view = _view(FAR, day=day)
    plan = _plan(view, _macro(crew_target=np.int32(9)))
    assert _deposits(tuple(np.asarray(x) for x in plan[:3])), "nothing banked"
    row = _melon_offer(plan, P.MIDDAY_PLACE_V2_TURN)
    assert row > 0 and row % 6 == 0, row
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", False)
    off = _plan(view, _macro(crew_target=np.int32(9)))
    assert _melon_offer(off, P.MIDDAY_PLACE_V2_TURN) == 0


def test_v2_row_covers_the_melon_the_shed_is_holding_by_then(monkeypatch):
    """And it covers it: the row asks for at least every unit the simulator
    has in the shed by the turn it fires, so nothing the excursion banked is
    left standing for `_end_of_day`. Over-asking is free -- every SELL is
    clipped to the shed unit by unit in both engine and simulator."""
    monkeypatch.setattr(P, "MELON_OPEN_ON", False)
    monkeypatch.setattr(P, "MIDDAY_PLACE_ON", True)
    monkeypatch.setattr(P, "MIDDAY_PLACE_V2_ON", True)
    plan = _plan(_view(NEAR), _macro(crew_target=np.int32(6)))
    route = tuple(np.asarray(x) for x in plan[:3])
    shed = _sim_shed_by_turn(route, until=P.MIDDAY_PLACE_V2_TURN)
    assert shed[P.MIDDAY_PLACE_V2_TURN] > 0, shed
    assert _melon_offer(plan, P.MIDDAY_PLACE_V2_TURN) >= shed[P.MIDDAY_PLACE_V2_TURN]


def test_v2_leaves_the_row_alone_on_a_day_that_banks_nothing(v2):
    """The row rides on the deposit, so a day whose melon is not ripe has
    neither -- the switch cannot invent a sale out of an empty shed."""
    view = _view(FAR, day=P.MELON_OPEN_HARVEST_DAY - 4)
    plan = _plan(view, _macro(crew_target=np.int32(9)))
    assert not _deposits(tuple(np.asarray(x) for x in plan[:3]))
    assert _melon_offer(plan, P.MIDDAY_PLACE_V2_TURN) == 0


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
