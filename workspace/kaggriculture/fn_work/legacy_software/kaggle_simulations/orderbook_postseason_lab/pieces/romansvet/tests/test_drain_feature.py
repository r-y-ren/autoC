"""The residual town-drain feature: what the network could not previously see.

`brain.features` has always carried own producing tiles, opponent producing
tiles and the market's inventory as three separate columns. What it could not
express is the quantity those three only *bound*: how much of the town's
remaining appetite for a product is still unclaimed. That residual is a product
of a tile count with the days left and a function of shop unlocks that have not
happened yet, so it is not linear in any column, and the 2026-08-26 diagnosis
measured what it costs -- the four markets that go over the drain are exactly
the four that lose money, while tomato, egg and carrot carry 679 units of drain
nobody supplies. The marginal unit of milk is worth **-55 coins** against
`kagg2` and the marginal unit of tomato **+93**.

The other half of this file is the checkpoint-compatibility contract. The two
weight blocks are appended, so every incumbent theta is a prefix of the layout
and reads them as an *addition* of an exactly-zero product -- they contribute
nothing to a decode that does not carry them.

That is a claim about the two weight blocks, and since 2026-08-26 it is no
longer the same claim as "an older theta decodes byte for byte". `brain.decide`
also gates the plant mix on the `share` column *directly*, with no weight
between the feature and the decision, so that the melon fix holds at zero
theta (`core/policy.py`, the `g7`/`gb7` note). That path is deliberately live
for every theta length, and the two tests at the bottom of this file pin both
halves: the weight blocks stay inert, and the hard gate does not.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import policy as PO

#: `spec.SHOP_CONSUME` averaged over the eight kinds, six ticks a day, over the
#: 132 shop-days a season contains, plus the town centre's 30 -- the season
#: drain table of `2026-08-26-drain-aware-reservation.md` section 1.1,
#: transcribed rather than recomputed so this is a real cross-check.
SEASON_DRAIN = {"WHEAT": 525, "CARROT": 327, "TOMATO": 228, "STRAWBERRY": 426,
                "MELON": 30, "EGG": 228, "MILK": 327, "WOOL": 228,
                "FERTILIZER": 0}


def _obs(day=0, nquad=4, shops=None, own=(), opp=(), inv=None, shed=None):
    """A board stated as (kind, occupant, count) triples per seat."""
    def board(layout):
        kind = np.where(spec.TILE_QUAD < nquad, spec.KIND_EMPTY,
                        spec.KIND_LOCKED).astype(np.int32)
        occ = np.full(spec.N_TILES, -1, np.int32)
        free = list(np.flatnonzero(kind == spec.KIND_EMPTY))
        for k, a, n in layout:
            for _ in range(n):
                t = free.pop(0)
                kind[t], occ[t] = k, a
        return kind, occ

    kind, occ = board(own)
    okind, oocc = board(opp)
    z = np.zeros(spec.N_TILES, np.int32)
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(20_000), opp_money=np.int32(20_000),
        kind=kind, occ=occ, opp_kind=okind, opp_occ=oocc,
        t_day=z.copy(), t_yield=z.copy(),
        shed=(np.zeros(spec.N_ITEMS, np.int32) if shed is None else shed),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=(np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
                 if inv is None else inv),
        price=np.asarray(brain._BASE, np.int32),
        shops=(np.zeros(spec.N_SHOPS, np.int32) if shops is None else shops))


def _crop(name, n):
    return (spec.KIND_PLANT, list(spec.CROPS).index(name), n)


def _animal(name, n):
    a = list(spec.ANIMALS).index(name)
    return (int(spec.ANIMAL_STRUCT[a]), a, n)


def _drain(obs):
    return np.asarray(brain.expected_drain(np, obs, brain.daily_town_demand(np, obs)))


# ------------------------------------------------------------------ the drain

def test_expected_drain_reproduces_the_measured_season_table():
    """Day 0, no shops open yet: the whole season's drain has to come out of
    the unlock calendar, because the *observed* shop set is empty and stays
    empty for three more days. A feature that priced only today's shops would
    read exactly zero drain on every day a planting decision is actually made.
    """
    got = _drain(_obs(day=0))
    want = np.array([SEASON_DRAIN[n] for n in spec.PRODUCTS], np.float32)
    np.testing.assert_array_equal(got, want)


def test_no_shop_ever_consumes_melon_or_fertilizer():
    """Melon's whole drain is the 30 town-centre ticks and fertilizer's is
    exactly zero -- the reason both realise under 0.6x base when they are sold
    at all, and the reason the `share` column has to be clipped."""
    got = _drain(_obs(day=0))
    assert got[spec.I_FERT] == 0.0
    assert got[spec.I_MELON] == float(spec.N_DAYS)


def test_the_drain_shrinks_monotonically_as_the_season_runs_out():
    prev = _drain(_obs(day=0))
    for day in range(1, spec.N_DAYS):
        cur = _drain(_obs(day=day))
        assert np.all(cur <= prev + 1e-6), day
        prev = cur
    assert np.all(prev >= 0.0)


def test_a_shop_the_town_has_drawn_is_priced_by_its_own_row_not_the_average():
    """`shops` counts *instances per kind* and the draw is with replacement, so
    a town that happened to draw the yarn store eight times drains wool at
    8x2x6 a day and everything else at the town centre's one. Averaging applies
    only to shops the calendar will unlock but the town has not drawn yet --
    here there are none, because day 27 is past the eighth unlock.
    """
    shops = np.zeros(spec.N_SHOPS, np.int32)
    shops[spec.SHOP_NAMES.index("YARN_STORE")] = spec.MAX_SHOP_INSTANCES
    got = _drain(_obs(day=27, shops=shops))
    horizon = spec.N_DAYS - 27
    ticks = spec.TURNS_PER_DAY // spec.SHOP_SELL_INTERVAL
    n = spec.MAX_SHOP_INSTANCES
    assert got[spec.I_WOOL] == horizon * (n * 2 * ticks + 1)   # + the centre's one
    assert got[spec.I_TOMATO] == horizon * 1                   # the centre alone
    assert got[spec.I_FERT] == 0.0


# ----------------------------------------------------------- the residual sign

def test_the_residual_is_positive_on_a_board_nobody_is_farming():
    """Every product the town actually consumes is unclaimed on an empty
    board, which is what "uncontested" means before either seat commits."""
    _, _, drain = brain.features(np, _obs(day=0))
    assert drain.shape == (spec.N_PRODUCTS, PO.N_DRAIN_FEAT)
    drained = [i for i in range(spec.N_PRODUCTS) if i != spec.I_FERT]
    assert np.all(drain[drained] > 0.0)
    # Fertilizer has no drain and no supply yet, so its residual is exactly 0 --
    # not positive. Nothing is being denied; there is nothing to deny.
    assert np.all(drain[spec.I_FERT] == 0.0)


@pytest.mark.parametrize("product,tiles", [
    ("TOMATO", _crop("TOMATO", 25)),
    ("STRAWBERRY", _crop("STRAWBERRY", 25)),
    ("MILK", _animal("COW", 25)),
    ("WOOL", _animal("SHEEP", 25)),
])
def test_both_seats_flooding_one_market_turns_its_residual_negative(product, tiles):
    """The whole point of the feature: the same product reads positive when it
    is nobody's and negative once the two boards between them are committed to
    more of it than the town will eat. Neither seat's tiles alone is the
    signal -- `features` already carries those two counts separately."""
    i = spec.PRODUCTS.index(product)
    _, _, bare = brain.features(np, _obs(day=0))
    _, _, mine = brain.features(np, _obs(day=0, own=[tiles]))
    _, _, both = brain.features(np, _obs(day=0, own=[tiles], opp=[tiles]))
    assert np.all(bare[i] > 0.0)
    assert np.all(both[i] < 0.0)
    assert np.all(both[i] < mine[i]) and np.all(mine[i] < bare[i])
    # ...and only that product moves. (Animals also make fertilizer, which is
    # exactly why the herd cases exclude it rather than pretending otherwise.)
    others = [j for j in range(spec.N_PRODUCTS)
              if j != i and not (j == spec.I_FERT and tiles[0] != spec.KIND_PLANT)]
    np.testing.assert_array_equal(bare[others], both[others])


def test_it_separates_the_contested_product_from_the_uncontested_one():
    """The measured case (section 4 of the diagnosis): both seats run cows, so
    the marginal unit of milk is worth -55 coins, while neither grows tomato
    and the marginal unit there is worth +93. Before this feature the grow
    score saw only "opponent has 20 producing tiles" with no idea whether the
    town could absorb them.
    """
    shops = np.zeros(spec.N_SHOPS, np.int32)
    for name in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP", "BAKERY"):
        shops[spec.SHOP_NAMES.index(name)] += 1     # the calendar's four by day 12
    # Both seats deep in cows, milk already dumped past the market's opening
    # level and more of it waiting in the shed; tomato drained 188 below
    # opening by a town nobody supplies. Both offsets are the measured
    # end-of-season `inv - I0` of section 3(b).
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_MILK] += 120
    inv[spec.I_TOMATO] -= 188
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_MILK] = 25
    herd = _animal("COW", 25)
    _, _, drain = brain.features(np, _obs(day=12, shops=shops, inv=inv, shed=shed,
                                          own=[herd], opp=[herd]))
    gap, share = drain[:, 0], drain[:, 1]
    assert gap[spec.I_MILK] < 0.0 < gap[spec.I_TOMATO]
    assert share[spec.I_MILK] < 0.0 < share[spec.I_TOMATO]


def test_supply_already_sitting_in_the_market_and_the_shed_counts():
    """Committed supply is not only future tiles: a market already above its
    opening inventory and a shed waiting for a lot are both units the town has
    yet to absorb."""
    base = _obs(day=10)
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_WOOL] += 400
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_MELON] = 90
    _, _, a = brain.features(np, base)
    _, _, b = brain.features(np, base._replace(mkt_inv=inv))
    _, _, c = brain.features(np, base._replace(shed=shed))
    assert b[spec.I_WOOL, 0] < 0.0 < a[spec.I_WOOL, 0]
    assert c[spec.I_MELON, 0] < 0.0 < a[spec.I_MELON, 0]


def test_both_columns_are_clipped_at_the_documented_bound():
    """Unclipped, `share` diverges on fertilizer (drain exactly zero) and one
    sigma step on a drain weight would be a double-digit logit swing."""
    flood = [_crop("MELON", 25)]
    _, _, drain = brain.features(np, _obs(day=0, own=flood, opp=flood))
    assert drain.min() == -brain.DRAIN_CLIP
    assert np.all(np.abs(drain) <= brain.DRAIN_CLIP)
    # Fertilizer: zero drain, a full herd of supply -- the saturating case.
    herd = [_animal("SHEEP", 25)]
    _, _, fert = brain.features(np, _obs(day=0, own=herd, opp=herd))
    assert fert[spec.I_FERT, 1] == -brain.DRAIN_CLIP


def test_the_horizon_is_the_days_a_harvest_can_still_reach_a_shed():
    """A tile placed after `ops.LAST_SHED_DAY` banks nothing, so it commits no
    supply -- the same terminal rule the rest of the planner derives from."""
    herd = [_animal("COW", 25)]
    _, _, a = brain.features(np, _obs(day=O.LAST_SHED_DAY + 1, own=herd, opp=herd))
    _, _, b = brain.features(np, _obs(day=O.LAST_SHED_DAY + 1))
    np.testing.assert_array_equal(a, b)


# ------------------------------------------------- checkpoint compatibility

#: The start index of every parameter block that existed before this feature.
#: Pinned as literals, not recomputed: the property under test is precisely
#: that no earlier block ever moves, and a table derived from `SHAPES` would
#: move with it and assert nothing.
FROZEN_OFFSETS = {
    "w1": 0, "b1": 2304, "w2": 2368, "b2": 2496, "g1": 2498, "gb1": 3266,
    "g2": 3298, "gb2": 3874, "g3": 3892, "gb3": 4180, "w3": 4189, "b3": 4253,
    "g4": 4254, "gb4": 4286, "g5": 4287, "gb5": 4383,
    "dh": 4386, "ds": 4514,
}


def test_no_pre_existing_block_moved():
    for name, off in FROZEN_OFFSETS.items():
        assert PO.offset(name) == off, name
    assert PO.N_PARAMS_LEGACY == 3892
    assert PO.offset("dh") == 4386          # the old N_PARAMS, i.e. a clean append
    # ... and the next block starts where this one ends, so `dh`/`ds` are a
    # prefix of every later layout exactly as `g5`/`gb5` are of this one.
    assert PO.offset("g6") == 4386 + PO.N_DRAIN_FEAT * (PO.N_ENC_HID + PO.N_ENC_OUT)


#: Every pre-`dh` layout length, i.e. every theta that carries no drain weights
#: at all: the legacy net, and the two blocks appended after it.
PRE_DRAIN_LENGTHS = (PO.N_PARAMS_LEGACY, 4287, 4386)


def _constant_drain(monkeypatch, value):
    """Force `residual_drain` to a constant, keeping its shape and dtype."""
    real = brain.residual_drain
    monkeypatch.setattr(brain, "residual_drain",
                        lambda xp, o, own, opp, demand:
                        real(xp, o, own, opp, demand) * 0.0 + value)


def test_the_drain_weights_cannot_move_a_theta_without_the_block(monkeypatch):
    """The compatibility claim, tested at the only place it can fail.

    Zero-padding is only inert because the drain enters `policy.forward` as
    `+ (f @ 0)`, which is exactly 0.0 and leaves the sum it joins bit-identical.
    Rather than trusting that, feed the decode two wildly different drain
    blocks and require every pre-2026-08-26 layout to decode to the identical
    `Macro` both times.

    Both constants sit **above** the plant mix's absorption gate, which reads
    the same feature with no weight in between (`brain.decide`). That is
    deliberate: this test is about the `dh`/`ds` weights, so the other channel
    is held at one verdict rather than being allowed to explain a difference
    the weights caused. The gate's own behaviour is the next test's job.
    """
    obs = _obs(day=9, own=[_crop("STRAWBERRY", 12), _animal("COW", 6)],
               opp=[_crop("MELON", 20)])

    def decoded(length):
        rng = np.random.default_rng(0)
        return {n: brain.decide(np, rng.normal(size=n).astype(np.float32) * 0.3, obs)
                for n in length}

    _constant_drain(monkeypatch, 3.7)
    ref = decoded(PRE_DRAIN_LENGTHS)
    _constant_drain(monkeypatch, -0.5)          # still clears the gate's -DRAIN_CLIP
    for n, got in decoded(PRE_DRAIN_LENGTHS).items():
        want = ref[n]
        for f, a, b in zip(want._fields, want, got):
            np.testing.assert_array_equal(np.asarray(a), np.asarray(b),
                                          err_msg=f"{n}-param theta, field {f}")


def test_the_absorption_gate_is_live_for_a_theta_without_the_block(monkeypatch):
    """The other side of the same coin, and the contract the melon fix needs.

    `brain.decide` gates the plant mix on the `share` column directly, so that
    a saturated market stops taking seed at **zero theta** -- the `g7`/`gb7`
    gene biases the threshold, it does not switch the gate on. So unlike the
    weights above, this path must move a pre-`dh` theta, and the shipped
    threshold is the clip floor: a market has to be saturated, not merely
    oversupplied, before the crop is dropped.
    """
    obs = _obs(day=9, own=[_crop("STRAWBERRY", 12), _animal("COW", 6)],
               opp=[_crop("MELON", 20)])
    melon = list(spec.CROPS).index("MELON")

    def targets(length):
        rng = np.random.default_rng(0)
        return {n: brain.decide(np, rng.normal(size=n).astype(np.float32) * 0.3,
                                obs).plant_target for n in length}

    # Merely negative is not enough -- only the clip floor is.
    _constant_drain(monkeypatch, -brain.DRAIN_CLIP + 0.5)
    open_gate = targets(PRE_DRAIN_LENGTHS)
    _constant_drain(monkeypatch, -brain.DRAIN_CLIP)
    shut_gate = targets(PRE_DRAIN_LENGTHS)
    for n in PRE_DRAIN_LENGTHS:
        assert open_gate[n].sum() > 0, n
        assert shut_gate[n].sum() == 0, n        # every crop saturated -> plant nothing

    # And on the real feature, the saturated market is melon's alone: the
    # opponent's twenty melon tiles commit more than the town eats all season,
    # while the five crops' other four stay plantable.
    monkeypatch.undo()
    for n in PRE_DRAIN_LENGTHS:
        rng = np.random.default_rng(0)
        got = brain.decide(np, rng.normal(size=n).astype(np.float32) * 0.3,
                           obs).plant_target
        assert got[melon] == 0, n
        assert got.sum() > 0, n


def test_a_theta_that_does_carry_the_block_reads_the_feature():
    """The other half: the genes must not be inert for a theta that has them,
    or the block is 132 parameters of decoration."""
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("b2") + 0] = 1.0                  # a live grow level
    # An empty board, so the absorption gate passes every crop and the only
    # thing that can move the mix is the weight under test. (Both seats deep in
    # melon -- what this case used to be -- now reads as saturated and the gate
    # empties the melon slot before `ds` gets a say, which would make the
    # assertions below pass for the wrong reason.)
    obs = _obs(day=0)
    flat = brain.decide(np, theta, obs)
    theta[PO.offset("ds") + 0 * PO.N_ENC_OUT + 0] = 2.0   # gap -> grow score
    lean = brain.decide(np, theta, obs)
    melon = list(spec.CROPS).index("MELON")
    straw = list(spec.CROPS).index("STRAWBERRY")
    assert flat.plant_target[melon] > 0
    # Melon's whole season drain is 30 units against strawberry's 426, so a
    # positive weight on the residual drains the melon slot and moves that mass
    # onto the crop with the most unclaimed drain.
    assert lean.plant_target[melon] < flat.plant_target[melon]
    assert lean.plant_target[straw] > flat.plant_target[straw]
    assert lean.plant_target.sum() == flat.plant_target.sum()
    # ...and the encoder path is live too.
    theta[PO.offset("ds") + 0 * PO.N_ENC_OUT + 0] = 0.0
    theta[PO.offset("dh") + 0 * PO.N_ENC_HID + 0] = 1.0
    theta[PO.offset("w2") + 0 * PO.N_ENC_OUT + 0] = 2.0
    assert not np.array_equal(brain.decide(np, theta, obs).plant_target,
                              flat.plant_target)


def test_numpy_and_jax_build_the_identical_drain_block():
    """Gate 2 for the new columns. Every decoded quantity is
    `floor(continuous * count)`, so a drain feature that differed in the last
    bit between the backends would flip decisions the shipped agent makes."""
    import jax.numpy as jnp

    from kagg3 import precision  # noqa: F401  pins matmul precision at import

    rng = np.random.default_rng(3)
    for _ in range(20):
        shops = rng.integers(0, 3, spec.N_SHOPS).astype(np.int32)
        shed = np.zeros(spec.N_ITEMS, np.int32)
        shed[:spec.N_PRODUCTS] = rng.integers(0, 40, spec.N_PRODUCTS)
        inv = (spec.MARKET_I0 + rng.integers(-800, 3000, spec.N_PRODUCTS)).astype(np.int32)
        obs = _obs(day=int(rng.integers(0, spec.N_DAYS)), shops=shops, shed=shed, inv=inv,
                   own=[_crop("WHEAT", 7), _animal("COW", 5)],
                   opp=[_crop("STRAWBERRY", 9), _animal("SHEEP", 4)])
        a = np.asarray(brain.features(np, obs)[2])
        b = np.asarray(brain.features(jnp, brain.PolicyObs(
            *[None if v is None else jnp.asarray(v) for v in obs]))[2])
        np.testing.assert_array_equal(a, b)
