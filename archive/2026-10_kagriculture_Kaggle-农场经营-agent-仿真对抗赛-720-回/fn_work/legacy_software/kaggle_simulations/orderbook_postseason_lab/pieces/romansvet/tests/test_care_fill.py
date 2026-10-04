"""`plan.CARE_FILL_ON`: spend every otherwise-PASS turn on a CARE.

The engine's rule (`_daily_refresh_animals`, `kaggriculture.py:804-833`,
ported at `sim/eod.py:94-127`): `pending_care_bonus` increments only
`if cared_today and fed_today` (`:829-830`), and a production night pays
`min(max_held, yield_units + 1 + bonus)` with `bonus` read only on a fed
animal and the bank wiped either way (`:826-828`). So a CARE is one product
unit at the next fire, on an animal that is fed both today and on the fire
night -- a cow cared and fed daily runs 3 milk per 2 days against the bare 1.
`OP_CARE` is idempotent inside a day (`:527`), which is the cap the filler
holds itself to: one CARE per animal per day.

The gap is coverage, not mechanism. In Kaggle loss 105393487 the opponent
issued 967 CARE ops on the same 8 COW + 4 SHEEP herd to our 230, and 604 of
our 1,309 PASS unit-turns sit in hours 18-23 -- the tail `_routes` leaves
after cutting each block at the last tile its budget reaches. `TAIL_CARE_ON`
already walks one hop of that tail; this switch walks up to `CARE_FILL_HOPS`
more, because the tails that hold the 604 are the long ones.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests -- the planner at `a838700`, the same pin `test_open_pump.py` and
`test_midday_place.py` use.
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
from test_route_early import PIN, PIN_SEEDS, _digest, _plan, _seeded_case, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)
#: What a filled turn may ever hold: the walk there, and the CARE.
FILL_OPS = MOVES + (O.OP_CARE,)

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)

#: The stack `test_route_early`'s digests were taken before -- the planner at
#: `a838700`. None of these five answers anything about the tail's care, and
#: pinning them off is what makes the identity claim this switch's own.
_PINNED_OFF = (
    "LOT4_ON", "EARLY_SELL_ON", "TAIL_FILL_ON", "TAIL_CARE_ON",
    "BANK_BEFORE_LOT_ON", "SURVIVAL_WATER_ON", "FEED_MANDATORY_ON",
    "FERT_TIMING_ON", "HIRE_ROW_ON", "SELL_SLOT_PRIORITY_ON",
    "SELL_SLOT_PRIORITY_SELLS_FIRST_ON", "PRESTOCK_V2_BUY_ON",
    "OPEN_PUMP_ON", "OPEN_PUMP_SLOT0_ON", "ENDROUTE_ON", "ENDROUTE_ROW2_ON",
    "ENDROUTE2_ON", "ENDROUTE2_SPLIT_ON", "WIDE_PICK_ON", "WIDE_PICK_FREE_ON",
    "ROUTE_SPLIT_ON",
)


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "CARE_FILL_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "CARE_FILL_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


#: `n_animal` head-of-serpentine animals behind `n_crop` ripe plants, and a
#: wheat quote *above* the product quote so `care_pays` fails and the day's own
#: route plans no CARE at all -- the census case, in miniature. `fed` is the
#: morning `fed_today` flag: 1 is the animal the tail may care for one turn and
#: no wheat, 0 is the animal a lone CARE banks nothing on (`:829`).
def _herd(n_animal=6, n_crop=2, animal=1, day=10, fed=1, cared=0, bank=0,
          yld=0, t_day=1, wheat=0, money=0):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield, t_dayv, t_water, t_cared, t_bank = (z.copy() for _ in range(5))
    a0 = n_crop
    kind[a0:a0 + n_animal] = spec.ANIMAL_STRUCT[animal]
    occ[a0:a0 + n_animal] = animal
    t_dayv[a0:a0 + n_animal] = t_day
    t_water[a0:a0 + n_animal] = fed
    t_cared[a0:a0 + n_animal] = cared
    t_bank[a0:a0 + n_animal] = bank
    t_yield[a0:a0 + n_animal] = yld
    kind[:n_crop] = spec.KIND_PLANT
    occ[:n_crop] = spec.I_TOMATO
    t_yield[:n_crop] = 6
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    price = BASE_PRICE.copy()
    price[spec.I_WHEAT] = 400                    # > MILK and WOOL: `care_pays` fails
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_dayv, t_water=t_water,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=t_cared,
        t_favail=z.copy(), shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(4), price=price,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32), t_bank=t_bank)


def _pair(view, macro, monkeypatch):
    """(plan with the switch off, plan with it on) on one board."""
    monkeypatch.setattr(P, "CARE_FILL_ON", False)
    base = _plan(view, macro)
    monkeypatch.setattr(P, "CARE_FILL_ON", True)
    return base, _plan(view, macro)


def _written(base, got):
    """[(unit, turn, op)] the switch wrote into a turn that used to PASS."""
    b, g = np.asarray(base[0]), np.asarray(got[0])
    return [(int(u), int(t), int(g[u, t]))
            for u, t in np.argwhere((b == O.OP_PASS) & (g != O.OP_PASS))]


def _cares(plan):
    """Number of CARE ops the whole day's routes emit."""
    return int((np.asarray(plan[0]) == O.OP_CARE).sum())


def _cared_tiles(plan):
    """Serpentine ranks the plan's routes issue a CARE on, with repeats."""
    uop = np.asarray(plan[0])
    sx, sy = np.asarray(P.SERP_X), np.asarray(P.SERP_Y)
    out = []
    for u in range(spec.MAX_UNITS):
        x, y = P.SPAWN_X[u], P.SPAWN_Y[u]
        for t in range(P.TPD):
            op = int(uop[u, t])
            if op in MOVES:
                dx, dy = O.MOVE_DELTA[op]
                x, y = x + dx, y + dy
            elif op == O.OP_CARE:
                out.append(int(np.flatnonzero((sx == x) & (sy == y))[0]))
    return out


# =========================================================================
# OFF: byte-identical to the planner the switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(monkeypatch):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    monkeypatch.setattr(P, "CARE_FILL_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_passes_the_tail_beside_a_fed_uncared_herd(off, monkeypatch):
    """The behaviour the switch exists to change: six fed, uncared cows a step
    away, `care_pays` refusing every one of them, and the unit spending the
    rest of the day on PASS."""
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    unit_op = np.asarray(_plan(_herd(), _macro())[0])
    assert not (unit_op == O.OP_CARE).any(), "the board planned a care"
    last = int(np.nonzero(unit_op[0] != O.OP_PASS)[0].max())
    assert P.TPD - 1 - last >= 8, last


# =========================================================================
# ON: the tail cares, again and again, and nothing else moves
# =========================================================================

def test_on_cares_every_animal_the_tail_can_reach(on, monkeypatch):
    """`CARE_FILL_HOPS` hops on a herd the day feeds and never cares: each one
    is a walk plus a CARE, and the count is the hop budget."""
    base, got = _pair(_herd(), _macro(), monkeypatch)
    wrote = _written(base, got)
    assert [op for _, _, op in wrote if op == O.OP_CARE], wrote
    for _, _, op in wrote:
        assert op in FILL_OPS, wrote
    assert _cares(got) - _cares(base) == P.CARE_FILL_HOPS, (_cares(base),
                                                            _cares(got))


def test_on_never_cares_one_animal_twice(on, monkeypatch):
    """The engine's cap: `OP_CARE` sets `cared_today` and a second is a no-op
    (`:527`), so `cf_free` strikes the tile for this unit's later hops and for
    every unit after it. Every CARE the day emits lands on its own tile."""
    _, got = _pair(_herd(n_animal=12), _macro(crew_target=np.int32(6)),
                   monkeypatch)
    tiles = _cared_tiles(got)
    assert tiles, "no care was emitted"
    assert len(tiles) == len(set(tiles)), tiles


def test_on_leaves_an_animal_the_day_never_feeds_alone(on, monkeypatch):
    """A CARE on an unfed animal banks nothing (`:829`). The herd is unfed and
    the shed is empty, so the day plans no feed either -- and the tail must
    leave every one of those turns as PASS."""
    base, got = _pair(_herd(fed=0, wheat=0), _macro(), monkeypatch)
    assert _written(base, got) == []
    for k in range(3):
        assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), k


def test_on_refuses_an_animal_with_no_bank_headroom(on, monkeypatch):
    """`min(max_held, yield + 1 + bonus)` (`:827`): a bank with nowhere to go
    pays nothing. A cow holds 6, so a bank of 5 leaves no room for tonight's
    care plus the base unit the fire pays anyway, and 4 leaves exactly enough.
    Day 11 on purpose -- a cow placed on day 1 does not fire that night, so
    the bank really does carry (`eod.refresh_animals` wipes it at every fire)."""
    for bank, want in ((5, False), (4, True)):
        base, got = _pair(_herd(day=11, bank=bank), _macro(), monkeypatch)
        assert bool(_written(base, got)) is want, (bank, _written(base, got))


def test_on_refuses_a_care_that_fires_past_the_horizon(on, monkeypatch):
    """The unit a care banks has to still be sellable. Two cows on day 27,
    one day of `placed_day` apart: the one placed on day 1 fires on day 29,
    the last day `VAL.pay_day()` still monetizes; the one placed on day 0
    fires on day 30 and never sells what tonight's care banks."""
    for t_day, want in ((0, False), (1, True)):
        base, got = _pair(_herd(day=27, t_day=t_day), _macro(), monkeypatch)
        assert bool(_written(base, got)) is want, (t_day, _written(base, got))


def test_on_respects_the_turns_the_tail_has_left(on, monkeypatch):
    """One hop is a walk plus a CARE, taken out of what the block leaves.
    Padding the block with ripe crop stops eats the tail, and the cares the
    filler adds fall away with it."""
    added = [_cares(g) - _cares(b) for b, g in
             (_pair(_herd(n_animal=4, n_crop=n), _macro(), monkeypatch)
              for n in (2, 10, 18))]
    assert added == sorted(added, reverse=True), added
    assert added[0] > 0 and added[-1] == 0, added


def test_on_leaves_every_turn_the_route_owns_alone(monkeypatch):
    """Against the shipped defaults, on fourteen seeded boards: the filler
    writes into PASS turns and nowhere else, so it changes no admission, no
    block cut and no market row -- every op the day already had is on the same
    turn, for the same unit, with the same argument."""
    cases = [_seeded_case(s) for s in PIN_SEEDS + (100, 101)]
    cases += [(_herd(**kw), _macro()) for kw in _FIRING]
    for s, (view, macro) in enumerate(cases):
        base, got = _pair(view, macro, monkeypatch)
        keep = np.asarray(base[0]) != O.OP_PASS
        for k in range(3):                       # unit_op, unit_a, unit_q
            assert np.array_equal(np.asarray(base[k])[keep],
                                  np.asarray(got[k])[keep]), (s, k)
        for k in (3, 4, 5):                      # mkt_op, mkt_a, mkt_q
            assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), (s, k)


#: Boards the filler actually fires on -- a herd the day feeds and does not
#: care, in the four shapes the hop has to handle: cows and sheep, a herd
#: wider than `CARE_FILL_HOPS` and one narrower, and a crew of one against a
#: crew of six.
_FIRING = (dict(), dict(n_animal=12), dict(animal=2),
           dict(n_animal=12, n_crop=6))


def test_on_only_ever_writes_a_walk_or_a_care(monkeypatch):
    """Nothing that needs a purchase, a PICKUP or a carry, and no HARVEST: the
    one op the filler takes banks into tile state at end of day and carries
    nothing out. `_FIRING` fires it, so this is not vacuous."""
    fired = 0
    for i, kw in enumerate(_FIRING):
        for crew in (1, 6):
            macro = _macro(crew_target=np.int32(crew))
            base, got = _pair(_herd(**kw), macro, monkeypatch)
            wrote = _written(base, got)
            fired += len(wrote)
            for u, t, op in wrote:
                assert op in FILL_OPS, (i, crew, u, t, op)
    assert fired > 0, "the filler never fired"


def test_on_never_fills_a_drop_day(on, monkeypatch):
    """A DROP day's tail is the walk home plus the DROP, measured from the
    block's last tile -- a fill hop would walk the unit off it."""
    if not P.DROP_ON:
        pytest.skip("DROP_ON is off")
    for day in (O.LAST_SHED_DAY, O.LAST_SHED_DAY + 1):
        view, macro = _view(day=day, n_coop=8, n_ripe=24, yld=6, wheat=20,
                            money=8_000), _macro()
        base, got = _pair(view, macro, monkeypatch)
        for k in range(3):
            assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), (day, k)


def test_on_composes_with_both_tail_switches(monkeypatch):
    """The three share the tail cursor and nothing else, and this one runs
    last. With the care hop and the filler also on the invariant still holds,
    and no tile is cared twice."""
    monkeypatch.setattr(P, "TAIL_FILL_ON", True)
    monkeypatch.setattr(P, "TAIL_CARE_ON", True)
    cases = [_seeded_case(s) for s in PIN_SEEDS]
    cases += [(_herd(**kw), _macro()) for kw in _FIRING]
    for s, (view, macro) in enumerate(cases):
        base, got = _pair(view, macro, monkeypatch)
        keep = np.asarray(base[0]) != O.OP_PASS
        for k in range(3):
            assert np.array_equal(np.asarray(base[k])[keep],
                                  np.asarray(got[k])[keep]), (s, k)
        tiles = _cared_tiles(got)
        assert len(tiles) == len(set(tiles)), (s, tiles)


def test_on_traces_under_jit(monkeypatch):
    """The trainer's regime: the planner runs on `jax` tracers inside
    `sim/rollout.py`'s season-long `lax.scan`, so nothing in the hop may
    branch on a traced scalar in Python or pull one through `int()`. The hop
    count is the only Python loop in it, and `CARE_FILL_ON` is a Python bool.
    """
    import jax
    import jax.numpy as jnp

    from kagg3.core import brain
    from kagg3.core import policy as PO
    from kagg3.sim import rollout
    from kagg3.sim.state import build_tables, initial_state, prices_of

    monkeypatch.setattr(P, "CARE_FILL_ON", True)
    tables = build_tables(jnp)
    theta = jnp.asarray(PO.init_theta(np.random.default_rng(0)))

    def build(day, theta):
        st = initial_state(jnp)
        price = prices_of(jnp, tables, st.mkt_inv)
        return P.build_day(jnp, rollout.day_view(st, 0, day, price),
                           brain.decide(jnp, theta,
                                        rollout.policy_obs(st, 0, day, price)),
                           tables.price)[0]

    out = np.asarray(jax.jit(build)(jnp.int32(10), theta))     # must not raise
    assert out.shape == (spec.MAX_UNITS, P.TPD)


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03. It is pinned off for
#: this file the way `a838700`'s stack is pinned off for the digest fixture:
#: the worked boards below are the plan *before* it, and what this file is
#: about (the tail's care) is a question the switch does not answer either way.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.TAIL_FILL_ON` and `plan.BANK_BEFORE_LOT_ON` both went on by default on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: OFF digests above were taken before the pair existed, so they are pinned off
#: here the way `EARLY_SELL_ON` is; `tests/test_tail_fill.py` and
#: `tests/test_bank_before_lot.py` own the two switches.
@pytest.fixture(autouse=True)
def _tail_pair_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)
