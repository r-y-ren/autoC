"""Strategy archetypes are thetas for our own planner whose decode is set by
hand: bias blocks carry the global decisions and the value outputs, encoder
units tilt crop choice by product value. They exist so self-play has opponents
that expand, dump and *hold* -- behaviours a single lineage never shows itself.

They are also the yardstick `Trainer.absolute_eval` measures against and
champion selection now runs on, so "does this archetype earn anything" is a
correctness property, not a nicety. Measured 2026-08-25 the old `wheat_farmer`
finished every game on **0 coins**: `value_tilt=-3` pushed every grow score to
about -15, the softplus in `_unit_ratio` mapped that to a grow multiplier of 0,
and it spent its purse on land it never planted. `grow_bias` is what makes that
unreachable -- it sets the *level* of the grow vector while the tilts only set
its shape.
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

# The land-value fixtures, reused rather than rebuilt: `land_cap` is only a cap
# if the *planner* refuses, and `test_land_value` already owns the board and
# the `build_day` probe that asks it. (Same cross-import as
# `test_land_value` -> `test_budget_order`.)
import test_budget_order as BO
import test_land_value as LV

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO
from kagg3.es import archetypes as A


def _obs(money=20_000, nquad=2, day=12):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD < nquad] = spec.KIND_EMPTY
    kind[:10] = spec.KIND_PLANT
    occ = np.where(kind == spec.KIND_PLANT, 3, -1).astype(np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32); shed[:spec.N_PRODUCTS] = 20
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(money), opp_money=np.int32(money),
        kind=kind, occ=occ, opp_kind=kind.copy(), opp_occ=occ.copy(),
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.full(spec.N_CROPS, 50, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.asarray(brain._BASE, np.int32),
        shops=np.zeros(8, np.int32))


def test_theta_has_the_full_layout():
    th = A.archetype_theta()
    assert th.shape == (PO.N_PARAMS,) and th.dtype == np.float32


def test_unknown_knobs_are_refused():
    with pytest.raises(KeyError, match="value_tilt_"):
        A.archetype_theta(value_tilt_=1.0)


def test_expander_buys_land_and_develops():
    m = brain.decide(np, A.archetype_theta(**A.named("expander")), _obs())
    assert int(m.land_bias) > 0
    assert int(m.plant_target.sum() + m.animal_want.sum()) >= 35   # 40 free tiles, dev ~0.9+


def test_value_tilt_prefers_high_value_crops():
    hi = brain.decide(np, A.archetype_theta(value_tilt=+3.0, dev=10.0, animal_share=-10.0), _obs())
    lo = brain.decide(np, A.archetype_theta(value_tilt=-3.0, dev=10.0, animal_share=-10.0), _obs())
    wheat = list(spec.CROPS).index("WHEAT")
    melon = list(spec.CROPS).index("MELON")
    assert hi.plant_target[melon] > hi.plant_target[wheat]
    assert lo.plant_target[wheat] > lo.plant_target[melon]


def test_mid_tilt_prefers_strawberry_over_melon():
    """`value_tilt` is monotone in log1p(base), so it can only ever crown melon.

    Melon is also the product whose price collapses fastest when it is dumped
    (`above_target` 3.6, against strawberry's and milk's 1.6), so "tilt toward
    value" and "tilt toward what survives being sold" are different directions
    and the knob set needs both. `mid_tilt` is a band on the same feature.
    """
    m = brain.decide(np, A.archetype_theta(mid_tilt=3.0, dev=10.0, animal_share=-10.0), _obs())
    straw = list(spec.CROPS).index("STRAWBERRY")
    melon = list(spec.CROPS).index("MELON")
    wheat = list(spec.CROPS).index("WHEAT")
    assert m.plant_target[straw] > m.plant_target[melon]
    assert m.plant_target[straw] > m.plant_target[wheat]
    # ...and the cow, whose milk is in the same band, over the goose and the
    # sheep. Read off a macro that actually wants animals: `animal_share` is
    # -10 above, so that herd is empty and its argmax would say nothing. The
    # herd is a proportional split now rather than an argmax over the same
    # three scores, so what the band buys is a *majority* of cows.
    herd = brain.decide(np, A.archetype_theta(mid_tilt=3.0, dev=10.0, animal_share=2.0),
                        _obs()).animal_want
    assert int(herd.sum()) > 0, "the fixture wants no animals"
    assert int(np.argmax(herd)) == 1, herd


def test_mid_tilt_band_covers_exactly_strawberry_milk_and_wool():
    band = (np.tanh(A._BAND_K * (A._VALUE - A._BAND_LO))
            - np.tanh(A._BAND_K * (A._VALUE - A._BAND_HI)))
    inside = [spec.I_STRAWBERRY, spec.I_MILK, spec.I_WOOL]
    assert np.all(band[inside] > 1.5)
    outside = [i for i in range(spec.N_PRODUCTS) if i not in inside]
    assert np.all(band[outside] < 0.2)


def test_grow_bias_sets_the_level_and_the_tilts_only_the_shape():
    """The `wheat_farmer` regression: a negative tilt must not switch growing off.

    `_unit_ratio` is a softplus, so it reads the *level* of the grow vector.
    Centring the tilts means only `grow_bias` moves that level -- and because a
    softmax is shift-invariant, centring changes no crop mix.
    """
    base = dict(dev=10.0, animal_share=-10.0)
    cheap = brain.decide(np, A.archetype_theta(value_tilt=-3.0, grow_bias=8.0, **base), _obs())
    assert int(cheap.plant_target.sum()) > 0
    assert int(cheap.grow_mult.max()) > 0
    # The level is the knob, in both directions and for either tilt sign.
    for tilt in (-3.0, 0.0, 3.0):
        lo = brain.decide(np, A.archetype_theta(value_tilt=tilt, grow_bias=0.0, **base), _obs())
        hi = brain.decide(np, A.archetype_theta(value_tilt=tilt, grow_bias=8.0, **base), _obs())
        assert int(hi.grow_mult.sum()) > int(lo.grow_mult.sum())
        assert np.array_equal(lo.plant_target, hi.plant_target)   # shift-invariant mix


def test_hold_knob_scales_the_reservation_value():
    dump = brain.decide(np, A.archetype_theta(hold=-10.0), _obs())
    keep = brain.decide(np, A.archetype_theta(hold=10.0), _obs())
    base = brain.decide(np, A.archetype_theta(), _obs())
    assert np.all(dump.hold < base.hold) and np.all(base.hold < keep.hold)
    assert np.all(dump.hold >= 0)


def test_press_knob_is_zero_or_positive():
    assert np.all(brain.decide(np, A.archetype_theta(press=-3.0), _obs()).press == 0)
    assert np.all(brain.decide(np, A.archetype_theta(press=3.0), _obs()).press > 0)


def test_the_market_timing_archetypes_actually_hold_and_press():
    """Measured 2026-08-25, every named archetype had hold <= 0 and press == 0.

    That is one behaviour, not four: they all sold at any price the market
    offered, so nothing in the ladder ever competed with the policy for a
    *good* price -- only for a sale.

    `staple_bulk` used to be counted here and no longer is: a reservation above
    base on the *cheapest* product in the game is not market timing, it is a
    shed that never empties (retuned 2026-08-25, see `archetypes._NAMED`). It
    still prices delay; what it will not do is refuse a normal price.
    """
    for name in ("patient_grower", "squeeze_seller"):
        knobs = A.named(name)
        assert 0.5 <= knobs["hold"] <= 3.0
        assert 0.5 <= knobs["press"] <= 2.0
        m = brain.decide(np, A.archetype_theta(**knobs), _obs())
        # A reservation above base price: it will not sell into a normal market.
        assert np.all(m.hold > np.asarray(brain._BASE, np.int32))
        assert np.all(m.press > 0)

    bulk = A.named("staple_bulk")
    m = brain.decide(np, A.archetype_theta(**bulk), _obs())
    assert bulk["hold"] < 0 and bulk["press"] > 0
    assert np.all(m.hold < np.asarray(brain._BASE, np.int32))
    assert np.all(m.press > 0)


def test_squeeze_seller_is_not_patient_grower():
    """The two market-timing rungs have to be two strategies.

    Until 2026-08-25 they were one: at `hold=1` (1.52x base) neither ever sold
    on timing grounds, and their other differences all decode to the same day,
    so the pair played byte-identical seasons and the probe measured both at
    exactly 21,200 coins. `squeeze_seller`'s reservation now sits where a
    drained market clears it, which is what lets its `press` matter at all.
    """
    pg, sq = A.named("patient_grower"), A.named("squeeze_seller")
    a = brain.decide(np, A.archetype_theta(**pg), _obs())
    b = brain.decide(np, A.archetype_theta(**sq), _obs())
    assert not np.array_equal(a.hold, b.hold)
    # Both still refuse a normal market -- they differ in how far above it.
    base = np.asarray(brain._BASE, np.int32)
    assert np.all(a.hold > base) and np.all(b.hold > base)
    assert np.all(b.hold < a.hold)


def test_sampled_archetypes_are_diverse_and_valid():
    # At _obs() the affordability ratio is clip(20000/2000 - 1, -1, 4) = 4, so
    # the land bias' sign is sign(land + 4 * land_afford). With land ~ U(-6, 6) and
    # land_afford ~ U(0, 1) each draw lands on the "no" side with p ~ 0.33;
    # over 40 draws the chance of never seeing it is ~1e-7.
    rng = np.random.default_rng(0)
    lands, presses, holds = set(), set(), set()
    for _ in range(40):
        k = A.sample_archetype(rng)
        assert set(k) == set(A.KNOBS)
        m = brain.decide(np, A.archetype_theta(**k), _obs())
        lands.add(int(m.land_bias) > 0)
        presses.add(bool(np.any(m.press > 0)))
        # The widened range has to actually produce opponents that refuse a
        # normal price, not just ones that dump a little less eagerly.
        holds.add(bool(np.all(m.hold > np.asarray(brain._BASE, np.int32))))
    assert lands == {0, 1}
    assert presses == {False, True}
    assert holds == {False, True}


def test_every_named_archetype_decodes():
    assert len(A.NAMES) == len(A._NAMED)
    for name in A.NAMES:
        knobs = A.named(name)
        assert set(knobs) == set(A.KNOBS)
        brain.decide(np, A.archetype_theta(**knobs), _obs())


# ------------------------------------------- crowd and land_cap: kagg2's shape

def _farm_obs(cows=0, sheep=0, geese=0, melons=0, **kw):
    """`_obs` with its ten filler strawberry tiles replaced by a named herd
    and crop block.

    `crowd` is the only knob in this file that reads *state*, and the state it
    reads is `brain.features` column 7 -- this farm's own producing tiles of
    each product. A fixture for it has to name that count exactly rather than
    inherit `_obs`'s filler.
    """
    o = _obs(**kw)
    kind, occ = o.kind.copy(), o.occ.copy()
    kind[kind == spec.KIND_PLANT] = spec.KIND_EMPTY
    occ[:] = -1
    free = list(np.flatnonzero(kind == spec.KIND_EMPTY))
    melon = list(spec.CROPS).index("MELON")
    for k, a, n in ((spec.KIND_PASTURE, 1, cows), (spec.KIND_PASTURE, 2, sheep),
                    (spec.KIND_COOP, 0, geese), (spec.KIND_PLANT, melon, melons)):
        for _ in range(n):
            t = free.pop(0)
            kind[t], occ[t] = k, a
    return o._replace(kind=kind, occ=occ)


def test_the_new_knobs_write_nothing_at_their_no_op_values():
    """The seven pre-2026-08-26 rungs must still decode byte for byte.

    They carry `crowd=0` and `land_cap=_N_QUAD` explicitly (every named entry
    lists every knob), so "no-op" has to mean *no weights written*, not merely
    "weights that cancel".
    """
    plain = A.archetype_theta(land=3.0)
    assert np.array_equal(plain, A.archetype_theta(land=3.0, crowd=0.0))
    assert np.array_equal(plain, A.archetype_theta(land=3.0, land_cap=float(A._N_QUAD)))


def test_crowd_moves_the_herd_mix_off_the_kind_the_board_is_already_full_of():
    """`Macro.animal_want` is a proportional split of the three animal grow
    scores, so a constant theta already asks for a mix. What it cannot do on
    its own is *re-rank* that mix as the herd fills: the three scores are
    constants, so the same kind leads on every board of the season.

    `crowd` is the only knob that moves them -- it subtracts
    `crowd * tanh(own / 25)` per product, so each kind crowds itself out and
    the next one takes the head of the split. That re-ranking is what reaches
    the board: `budget.grant` is a threshold on value per coin, so the leading
    kind is the one that gets bought (measured in-sim: `crowd` 0 ends
    `mixed_ranch` on 0 geese / 1.9 cows / 0 sheep, `crowd` 5 on 2.0/1.4/2.2).
    """
    knobs = A.named("mixed_ranch")
    th, flat = A.archetype_theta(**knobs), A.archetype_theta(**dict(knobs, crowd=0.0))
    boards = (_farm_obs(), _farm_obs(sheep=8), _farm_obs(sheep=16, cows=8))
    lead = [int(np.argmax(brain.decide(np, th, o).animal_want)) for o in boards]
    assert lead == [2, 1, 0], lead           # sheep -> cow -> goose
    # Not merely a leader flip: the crowded kind is driven out of the split.
    crowded = brain.decide(np, th, _farm_obs(sheep=16, cows=8)).animal_want
    assert int(crowded[2]) == 0 and int(crowded[0]) > 0, crowded
    # `crowd` off, the same theta asks for the same mix on every board.
    flat_wants = [np.asarray(brain.decide(np, flat, o).animal_want) for o in boards]
    assert [int(np.argmax(w)) for w in flat_wants] == [2, 2, 2]
    assert all(w[2] >= w[1] >= w[0] for w in flat_wants)


def test_crowd_moves_the_crop_book_off_what_the_board_is_already_full_of():
    knobs = A.named("mixed_ranch")
    melon = list(spec.CROPS).index("MELON")
    straw = list(spec.CROPS).index("STRAWBERRY")
    bare = brain.decide(np, A.archetype_theta(**knobs), _farm_obs())
    full = brain.decide(np, A.archetype_theta(**knobs), _farm_obs(melons=20))
    assert bare.plant_target[melon] > bare.plant_target[straw]
    assert full.plant_target[straw] > full.plant_target[melon] == 0

    # `crowd` off, same two boards. This used to assert the books were equal
    # to the unit -- "the mix is blind to what is already planted" -- and since
    # 2026-08-26 that is one knob too strong. `brain.decide`'s market-
    # saturation gate (`absorb`) reads the board too, and it is not a `crowd`
    # knob: 20 melon tiles pin melon's residual-drain share at `-DRAIN_CLIP`,
    # so the gate drops melon whatever `crowd` says and the surviving weights
    # renormalise over the smaller book. Both paths drive melon out, which is
    # why the half above still passes; they are told apart here.
    #
    # What `crowd` off still buys is that nothing *re-ranks*. `crowd` subtracts
    # a per-product term and reorders the book; the gate only deletes entries,
    # so the crops it left alone come back in the same order on both boards.
    flat = A.archetype_theta(**dict(knobs, crowd=0.0))
    a = np.asarray(brain.decide(np, flat, _farm_obs()).plant_target)
    b = np.asarray(brain.decide(np, flat, _farm_obs(melons=20)).plant_target)
    assert a[melon] > 0 and b[melon] == 0, (a, b)     # the gate, not `crowd`
    keep = [i for i in range(len(spec.CROPS)) if i != melon]
    assert (list(np.argsort(a[keep], kind="stable"))
            == list(np.argsort(b[keep], kind="stable"))), (a, b)


def test_crowd_is_inert_on_a_board_that_produces_nothing():
    """It is centred where `grow_bias` is measured, so it changes no level."""
    a = brain.decide(np, A.archetype_theta(dev=10.0, grow_bias=8.0), _farm_obs())
    b = brain.decide(np, A.archetype_theta(dev=10.0, grow_bias=8.0, crowd=6.0), _farm_obs())
    assert np.array_equal(a.grow_mult, b.grow_mult)
    assert np.array_equal(a.plant_target, b.plant_target)


@pytest.mark.parametrize("cap", [2, 3])
def test_land_cap_is_the_board_the_archetype_stops_on(cap):
    """`land` is a bias on `head[1]` and `head[1]` reads no quadrant count, so
    an eager `land` leans toward every quadrant it can afford. `kagg2` stops
    at three.

    Since the land bias became coins the step cannot veto outright -- the
    decode is `land_price * tanh(...)`, bounded at one price either way. So
    the cap is asserted where it is expressible: past it the bias saturates to
    exactly *minus one quadrant price*, which is `brain`'s own "this gene has
    vetoed land" value (`land_ok`), and below it the bias is positive.
    """
    th = A.archetype_theta(land=6.0, land_afford=1.0, land_cap=float(cap))
    price = [int(spec.LAND_PRICES[min(q - 1, 2)]) for q in (1, 2, 3, 4)]
    got = [int(brain.decide(np, th, _obs(nquad=q)).land_bias) for q in (1, 2, 3, 4)]
    assert got == [p if q < cap else -p for q, p in zip((1, 2, 3, 4), price)]


def test_land_cap_at_the_full_board_leaves_the_decision_to_land():
    """`_N_QUAD` is the no-cap value and writes no weights (see above), so the
    eager `land` still leans yes on every board -- including the full one,
    where it is the engine and not the gene that has nothing left to sell.
    """
    th = A.archetype_theta(land=6.0, land_afford=1.0, land_cap=float(A._N_QUAD))
    assert [int(brain.decide(np, th, _obs(nquad=q)).land_bias) > 0
            for q in (1, 2, 3, 4)] == [True] * 4


@pytest.mark.parametrize("nquad", [2, 3])
def test_land_cap_holds_through_the_planner_and_not_only_the_decode(nquad):
    """The decode's saturated -1 is a *demand for one more full price*, not a
    veto, so what makes the cap a cap is whether a season's valuation ever
    clears it. At the quadrants `land_cap` guards it does not: `land_reach`
    prices only the tiles one day's crew can walk to, and that many tiles are
    never worth a second 2,000 or 4,000 coins.

    The most favourable board the cap will ever face -- day 6, a fat purse and
    a whole quadrant of unmet seed demand behind the wall, the fixture that
    *does* buy at zero bias. Measured in-sim, the same holds over a season: on
    five rungs and 8 games each, `land_cap` 2 ends every game on exactly 2
    quadrants and `land_cap` 3 on exactly 3.

    Only quadrants 2..4 are asserted, and that is the whole domain: `land_cap`
    is drawn from `[2, _N_QUAD]` and no named rung goes below 2. The engine's
    opening quadrant costs 1,000, and *that* one a 25-tile seed want does buy
    through a saturated-negative gene -- the bias is scaled to the price it is
    refusing, so the cheapest quadrant is the one it refuses least.
    """
    price = np.int32(spec.LAND_PRICES[nquad - 1])
    view = LV._board(day=6, money=50_000, nquad=nquad)
    want = BO._macro(plant_target=np.array([50, 0, 0, 0, 0], np.int32))
    assert LV._land(view, want._replace(land_bias=np.int32(0))) == 1
    assert LV._land(view, want._replace(land_bias=-price)) == 0


def test_mixed_ranch_is_the_eighth_rung_and_carries_kagg2s_shape():
    assert A.NAMES[7] == "mixed_ranch"
    k = A.named("mixed_ranch")
    assert k["land_cap"] == 3.0        # kagg2's 75-tile board, bought day 6 and 11
    assert k["crowd"] > 0.0            # a book and a mixed herd, not one of each
    # kagg2 drips under the town's drain and sells above base; a reservation on
    # a farm with a herd starves here, so this rung dumps instead.
    assert k["hold"] < 0.0
    m = brain.decide(np, A.archetype_theta(**k), _farm_obs(nquad=3))
    assert np.all(m.hold < np.asarray(brain._BASE, np.int32))
    # On its cap the gene demands a whole extra quadrant price, which is
    # `brain`'s own veto value: the land bias is exactly minus the price.
    assert int(m.land_bias) == -int(spec.LAND_PRICES[2])
    # And it asks for a herd of more than one kind -- the shape `crowd` is here
    # for. `mixed_ranch` used `animal_share` 0.5 until 2026-08-26, and under
    # the land valuation that share bought no animals at all (measured: an
    # empty pasture on all 8 probe games, 29,485 coins against 71,215 at 1.0).
    assert k["animal_share"] > 0.0
    want = brain.decide(np, A.archetype_theta(**k), _farm_obs(nquad=3, sheep=8)).animal_want
    assert int(np.sum(want > 0)) >= 2, want
