"""The crew-target ramp and the early-spend deferral (`g10`/`gb10`, 2026-08-30).

Every Kaggle loss we have a replay for is the same game: by day 10 the opponent
has ~12 hired hands and ~9k coins and we have ~6 and ~3.3k, with the difference
already sunk into animals and coops (8.1k of animal spend against their 5.8k,
three coops against none). `hire_bias` cannot state the fix. It is a constant
number of coins per hand inside a day bucket, so it tilts the enumeration's
gain and nothing else: it cannot say "the crew has to be twelve by day 10", and
it cannot say "the pasture waits until it is".

`g10` says both, as two biases on decisions the planner already makes:

* a crew **target** shaped as a logistic in the day -- height, midpoint and
  steepness -- with `plan.CREW_TARGET_PUSH` coins added to 1.5's enumerated
  gain for every candidate hand up to it. The push is above the dearest
  marginal fib bill in reach, so the argmax walks up to the target and stops.
* an **animal deferral**: while the day's crew is under that target, the animal
  candidate values and the structure builds are both scaled by
  `keep / DEFER_ONE`, so the coins and the free tiles the crew's work needs are
  not spent on a coop first.

The first test in the file is the inertness assertion, for the same reason it
is in `test_crew_and_herd_mix.py`: this block is appended, every checkpoint on
disk is a prefix of the layout, and `scripts/train.py --init-theta` zero-pads
one into it. If a zero `g10` moved a single decision, every incumbent theta
would have silently changed strategy.
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
from test_crew_and_herd_mix import _crew, _obs
from test_mixed_herd import _ops, _view, _want

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.es import archetypes as A

#: The layout `g10` appends to -- `g9`/`gb9`'s, and the length of every theta
#: written before 2026-08-30 (`artifacts/theta.npy` included).
PRE_RAMP_N = 4848


# --------------------------------------------------------------- the layout

def test_the_ramp_block_is_a_clean_append():
    """`g10` starts exactly where the previous layout ended, so an older theta
    is still a prefix rather than a re-layout."""
    assert PO.offset("g10") == PRE_RAMP_N
    # The layout this block ended, not the current `N_PARAMS`: blocks are only
    # ever appended, so pinning the tail here would make every later block's
    # own append test fail this one. `fh`/`fs` (2026-09-08), `gp` (2026-09-08)
    # and `g11`/`gb11` (2026-09-09) have since been appended past it.
    assert PO.offset("gb10") + PO.N_CREW_RAMP_OUT == 4980
    assert (PO.offset("gb10") + PO.N_CREW_RAMP_OUT
            == PRE_RAMP_N + PO.N_HEAD_HID * PO.N_CREW_RAMP_OUT + PO.N_CREW_RAMP_OUT)
    # Anchored on the block's own name, not on `SHAPES[-2:]`: every later
    # append would fail a tail pin by construction.
    names = [n for n, _ in PO.SHAPES]
    assert names[names.index("g10"):names.index("g10") + 2] == ["g10", "gb10"]
    # Live coordinates: the ES has to be able to find them without a flag.
    mask = PO.live_mask()
    assert mask[PO.offset("g10"):].all()


# ------------------------------------------------------------- inertness

def _ramp(theta, day):
    m = brain.decide(np, np.asarray(theta, np.float32), _obs(day=day, money=200_000))
    return int(m.crew_target), int(m.animal_defer)


def test_a_zero_block_asks_for_no_crew_and_defers_nothing_on_any_day():
    """`relu(tanh(0)) == 0` on the height, so the logistic's whole output is
    0.0 whatever the midpoint and the steepness decode to."""
    zero = np.zeros(PO.N_PARAMS, np.float32)
    for day in range(spec.N_DAYS):
        assert _ramp(zero, day) == (0, 0), day


@pytest.mark.parametrize("name", A.NAMES)
def test_a_pre_ramp_theta_decodes_byte_for_byte(name):
    """Every named rung, truncated to the pre-`g10` layout and zero-padded back
    -- which is exactly the `--init-theta` path (`policy.unpack`, `policy.pad`).

    Byte for byte on the whole `Macro`, not just the two new fields: the
    deferral is an integer scale on candidate values, and `x * DEFER_ONE //
    DEFER_ONE == x` has to hold on the real numbers a rung produces.
    """
    full = A.archetype_theta(**A.named(name))
    short = full[:PRE_RAMP_N].copy()
    np.testing.assert_array_equal(PO.pad(short), full)
    for obs in (_obs(day=0), _obs(day=8, money=40_000), _obs(day=22, money=120_000)):
        a = brain.decide(np, short, obs)
        b = brain.decide(np, full, obs)
        for f, x, y in zip(a._fields, a, b):
            np.testing.assert_array_equal(np.asarray(x), np.asarray(y), err_msg=f)


def test_a_zero_ramp_leaves_the_planner_where_it_was():
    """The planner half of the same claim: the enumeration's push is `0 * h`
    and the deferral scale is exactly `DEFER_ONE`, so the day's crew, its BUY
    row and its build ops are the ones it always chose."""
    view = _view(money=200_000, day=6)
    m = _macro(plant_target=np.array([20, 0, 0, 0, 0], np.int32),
               animal_want=_want(g=3, c=3))
    plan = P.build_day(np, view, m)
    for field, value in (("crew_target", np.int32(0)), ("animal_defer", np.int32(0)),
                         ("animal_defer", np.int32(P.DEFER_ONE))):
        # `animal_defer` saturated with a zero target is still inert: nothing
        # is under a target of zero, so the deferral never engages.
        got = P.build_day(np, view, m._replace(**{field: value}))
        for a, b in zip(plan, got):
            np.testing.assert_array_equal(np.asarray(a), np.asarray(b), err_msg=field)


# ------------------------------------------------------------- the decode

def test_the_target_is_a_ramp_in_the_day():
    """Height, midpoint and steepness, read off the decode: monotone in the
    day, zero well before the midpoint and at the height well after it."""
    th = A.archetype_theta(crew_target=2.0, crew_mid=-0.5, crew_steep=2.0)
    got = [_ramp(th, d)[0] for d in range(spec.N_DAYS)]
    assert got == sorted(got), got
    assert got[0] == 0, got
    assert got[-1] == max(got) <= spec.MAX_HANDS, got
    assert got[-1] >= 12, got            # the field's own day-10 crew is 12-14


def test_the_midpoint_moves_the_ramp_and_the_steepness_sharpens_it():
    early = A.archetype_theta(crew_target=2.0, crew_mid=-1.0, crew_steep=2.0)
    late = A.archetype_theta(crew_target=2.0, crew_mid=1.0, crew_steep=2.0)
    assert _ramp(early, 10)[0] > _ramp(late, 10)[0]
    soft = A.archetype_theta(crew_target=2.0, crew_mid=0.0, crew_steep=-3.0)
    hard = A.archetype_theta(crew_target=2.0, crew_mid=0.0, crew_steep=3.0)
    # Same height and midpoint; the sharp one is further from its height early
    # and closer to it late.
    assert _ramp(hard, 4)[0] < _ramp(soft, 4)[0]
    assert _ramp(hard, 26)[0] > _ramp(soft, 26)[0]


def test_the_deferral_decodes_one_sided_and_bounded():
    """`relu(tanh)` in `DEFER_ONE` fixed point: exactly 0 at or below zero --
    which is what makes the block inert -- monotone above it, and capped at
    `DEFER_ONE` (x1, the whole value) rather than running past it."""
    for knob, want in ((-5.0, 0), (-2.0, 0), (0.0, 0), (10.0, P.DEFER_ONE)):
        assert _ramp(A.archetype_theta(animal_defer=knob), 5)[1] == want, knob
    got = [_ramp(A.archetype_theta(animal_defer=k), 5)[1]
           for k in (0.0, 0.3, 0.7, 1.5, 10.0)]
    assert got == sorted(got) and got[1] > 0, got


def test_numpy_and_jax_agree_on_the_ramp():
    import jax
    import jax.numpy as jnp
    th = A.archetype_theta(crew_target=1.3, crew_mid=-0.4, crew_steep=0.9,
                           animal_defer=0.7)
    for day in range(spec.N_DAYS):
        o = _obs(day=day, money=50_000)
        a = brain.decide(np, th, o)
        b = brain.decide(jnp, jnp.asarray(th), jax.tree_util.tree_map(jnp.asarray, o))
        assert (int(a.crew_target), int(a.animal_defer)) == \
               (int(b.crew_target), int(b.animal_defer)), day


# ------------------------------------------------------------- the planner

def test_the_target_raises_the_crew_the_planner_hires():
    """The lever the Kaggle losses ask for, measured through `build_day`: the
    same board, the same work and the same purse, with only the target moving.

    Twelve queued plantings is deliberately *not* labour-saturated -- the
    enumeration settles well short of `MAX_HANDS` on it, which is the state we
    lose from -- so the target has somewhere to move the day to.
    """
    view = _view(money=200_000, day=6)
    base = _macro(plant_target=np.array([12, 0, 0, 0, 0], np.int32))
    crews = [_crew(view, base._replace(crew_target=np.int32(t)))
             for t in (0, 4, 8, 12)]
    assert crews == sorted(crews), crews
    assert crews[0] < 12 <= crews[-1], crews
    # Exactly the target, not merely more: the push is flat past it, so the
    # argmax stops there rather than running to `MAX_HANDS`.
    assert crews[-1] == 12, crews


def test_the_target_cannot_hire_past_what_the_purse_can_pay():
    """`afford` is still the enumeration's, and it still holds back
    `cash_reserve` -- a target is a bias on the gain, not an override."""
    poor = _view(money=300, day=6)
    base = _macro(plant_target=np.array([12, 0, 0, 0, 0], np.int32))
    assert _crew(poor, base._replace(crew_target=np.int32(14))) < 14


def test_the_deferral_holds_the_animal_row_back_while_the_crew_is_short():
    """The second half: with a target the day cannot meet yet, a saturated
    deferral takes the animal purchases off the BUY row entirely."""
    view = _view(money=200_000, day=2)
    base = _macro(animal_want=_want(g=4, c=4, s=4),
                  plant_target=np.array([12, 0, 0, 0, 0], np.int32))
    def bought(m):
        op, _, qty = P.build_day(np, view, m)[3:6]
        return int(qty[op == O.MO_BUY_ANIMAL].sum())

    assert bought(base) > 0
    # A target above what a day-2 purse can field, so the crew stays short and
    # the deferral is live for the whole day.
    short = base._replace(crew_target=np.int32(spec.MAX_HANDS),
                          animal_defer=np.int32(P.DEFER_ONE))
    assert bought(short) == 0
    # Half the deferral is half the value, not none of it: the greedy still
    # ranks animals, it just ranks them lower.
    half = base._replace(crew_target=np.int32(spec.MAX_HANDS),
                         animal_defer=np.int32(P.DEFER_ONE // 2))
    assert bought(half) <= bought(base)


def test_the_deferral_stops_the_coop_going_up():
    """Builds, not just purchases: a build takes a free tile ahead of every
    planting, so a day with stock already in the shed could still put a coop
    where the crew's wheat belongs."""
    view = _view(money=200_000, day=2)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_GOOSE] = 4                       # already bought, nothing to defer
    view = view._replace(shed=shed)
    base = _macro(animal_want=_want(g=4))
    assert _ops(P.build_day(np, view, base), O.OP_BUILD_COOP) > 0
    held = base._replace(crew_target=np.int32(spec.MAX_HANDS),
                         animal_defer=np.int32(P.DEFER_ONE))
    assert _ops(P.build_day(np, view, held), O.OP_BUILD_COOP) == 0


def test_the_deferral_lifts_once_the_crew_has_arrived():
    """It is a *deferral*, not a ban: a day whose crew has already reached the
    target buys and builds exactly what it would have without the gene."""
    view = _view(money=200_000, day=2)
    base = _macro(animal_want=_want(g=4, c=4),
                  plant_target=np.array([12, 0, 0, 0, 0], np.int32))
    met = base._replace(crew_target=np.int32(0), animal_defer=np.int32(P.DEFER_ONE))
    for a, b in zip(P.build_day(np, view, base), P.build_day(np, view, met)):
        np.testing.assert_array_equal(np.asarray(a), np.asarray(b))


def test_the_ramp_reaches_the_planner_from_a_theta():
    """End to end: knobs on `gb10`, through `brain.decide`, into 1.5's argmax
    and the buy side -- the path a trained theta actually takes."""
    view = _view(money=200_000, day=10)
    plants = np.zeros(spec.N_CROPS, np.int32)
    plants[spec.I_WHEAT] = 12

    def day10(theta):
        m = brain.decide(np, theta, _obs(day=10, money=200_000))
        m = m._replace(plant_target=plants, animal_want=_want(g=4, c=4))
        op, _, qty = P.build_day(np, view, m)[3:6]
        return int(qty[op == O.MO_HIRE].sum()), int(qty[op == O.MO_BUY_ANIMAL].sum())

    flat = day10(A.archetype_theta())
    # A midpoint around day 6 and a sharp rise: the field's own opening.
    ramped = day10(A.archetype_theta(crew_target=2.0, crew_mid=-1.4, crew_steep=2.0,
                                     animal_defer=10.0))
    assert ramped[0] > flat[0], (flat, ramped)      # more hands by day 10
    assert ramped[1] <= flat[1], (flat, ramped)     # not at the animals' expense


# ------------------------------------------------------- seasons, end to end

def test_seeded_seasons_are_identical_at_zero_ramp():
    """The parity claim in the simulator rather than in the decode.

    Four seeded seasons, played twice by the same rung -- once as the
    pre-`g10` theta every checkpoint on disk is, once zero-padded into this
    layout. Coins, the day-by-day money curve and the board the season leaves
    behind all have to match exactly, or the appended block is not inert and
    `--init-theta`'s zero pad is a strategy change.
    """
    import jax
    import jax.numpy as jnp
    from kagg3.es.train import host_words
    from kagg3.sim import eod, rollout
    from kagg3.sim.state import build_tables

    seeds = [11, 23, 37, 101]
    tables = build_tables(jnp)
    words = jnp.asarray(host_words(seeds))
    hi_t, lo_t = eod.weed_threshold()

    @jax.jit
    def run(thetas, w):
        def one(wd):
            money, daily, st = rollout.episode(tables, thetas, wd,
                                               jnp.int32(hi_t), jnp.int32(lo_t))
            return money, daily, st.kind, st.occ, st.shed, st.money, st.nquad
        return jax.vmap(one)(w)

    full = A.archetype_theta(**A.named("wheat_clone"))
    zero = np.zeros(PO.N_PARAMS, np.float32)
    old = [np.asarray(t[:PRE_RAMP_N]) for t in (full, zero)]
    new = [PO.pad(t.copy()) for t in old]
    a = run(jnp.stack([jnp.asarray(t) for t in old]), words)
    b = run(jnp.stack([jnp.asarray(t) for t in new]), words)
    for x, y in zip(a, b):
        np.testing.assert_array_equal(np.asarray(x), np.asarray(y))
    # The seasons are real ones and not a degenerate zero-coin trace, or the
    # equality above would be vacuous.
    assert (np.asarray(a[0])[:, 0] > 0).all(), np.asarray(a[0])
