"""The two things a constant theta could not say (2026-08-28): how many hands
to lease, and what mix of animals to want.

Both were found by a replay autopsy of 64 Kaggle games (`es/archetypes.py`,
"the Kaggle field"). The modal opponent reaches **14 hands by day 10** where we
reach 7-8, and the highest-scoring class runs a **12 SHEEP / 6 COW** pasture --
and neither is reachable from the genome as it stood:

* the crew size is not a gene at all. `plan` section 1.5 enumerates every
  affordable `h` and takes the argmax of admitted task value less
  `HIRE_BILLS[h]`; `dev`, `free_urgency` and `dev_weight` move it only by
  making the day's *work* worth more.
* the herd want and the planner's own valuation of an animal read the **same**
  per-product grow score. `_unit_ratio` is clipped at `GROW_MAX`, so any
  separation big enough to move the want leaves both animals worth 4x, and
  `budget.grant` -- value per coin -- then takes the cheaper cow every time.

`g8`/`gb8` adds one bias to each decision and changes nothing else. The first
test in each half is therefore the inertness assertion: a theta whose `g8`
block is zero must decode **byte for byte** as the same theta truncated to the
pre-gene layout, or every incumbent checkpoint has silently changed strategy.
The nine-rung table in `tests/test_archetype_ladder.py` is the same claim
measured in coins.
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
from test_mixed_herd import BASE, _view

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.es import archetypes as A

#: Length of the layout `g8`/`gb8` appends to -- the one every checkpoint
#: written before 2026-08-28 is stored under. Truncating a theta to it is
#: exactly "the genome before the crew and herd-mix genes existed"; the shipped
#: `artifacts/theta.npy` has been written under the *current*, longer layout
#: since 3a124bf, so the tests below slice it rather than assume its length.
PRE_GENE_N = 4617

#: Length of the layout the hire-bias day buckets (`g9`/`gb9`) append to -- the
#: one a theta trained between 2026-08-28's two commits is written under, and
#: the only pad in the file that is not a pad to zeros: `policy.unpack` copies
#: the season-constant bias into every bucket, so truncating here has to leave
#: the decode alone on *every* day and not only on the first six.
PRE_BUCKET_N = 4749

GOOSE, COW, SHEEP = 0, 1, 2


def _obs(day=0, money=3000, nquad=4, kind=None, occ=None):
    """A blank owned board. Big enough that `n_dev` is not the binding
    constraint on the herd, which is what the mix tests need."""
    z = np.zeros(100, np.int32)
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(money), opp_money=np.int32(3000),
        kind=np.full(100, spec.KIND_EMPTY, np.int32) if kind is None else kind,
        occ=z - 1 if occ is None else occ,
        opp_kind=np.full(100, spec.KIND_EMPTY, np.int32), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32), price=BASE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))


#: A spread of boards, so "byte-identical" is a claim about the decode and not
#: about one lucky day.
OBS = [_obs(), _obs(day=12, money=40_000), _obs(day=27, money=120_000, nquad=2),
       _obs(day=5, money=800, nquad=1)]


def _decisions(theta):
    return [brain.decide(np, np.asarray(theta, np.float32), o) for o in OBS]


def _crew(view, macro):
    """Hands the day's market rows actually hire -- the number 1.5 chose."""
    op, _, qty = P.build_day(np, view, macro)[3:6]
    return int(qty[op == O.MO_HIRE].sum())


# --------------------------------------------------------------- inertness

@pytest.mark.parametrize("name", A.NAMES)
def test_a_zero_g8_block_decodes_as_the_pre_gene_genome(name):
    """Every rung that does *not* name the new knobs is unmoved.

    `archetype_theta` writes `gb8` unconditionally, so this is the assertion
    that writing zeros there is the same as not having the block: truncate to
    `PRE_GENE_N` and `policy.unpack`'s zero padding must rebuild a genome that
    decodes to the identical `Macro`, field by field.
    """
    theta = A.archetype_theta(**A.named(name))
    if theta[PO.offset("g8"):].any():
        pytest.skip(f"{name} names the crew or herd-mix knobs")
    for a, b in zip(_decisions(theta[:PRE_GENE_N]), _decisions(theta)):
        for f, x, y in zip(a._fields, a, b):
            np.testing.assert_array_equal(np.asarray(x), np.asarray(y), err_msg=f)


def test_a_trained_theta_is_unmoved_by_the_appended_block():
    """The incumbent, not a hand-set rung: trained coordinates rather than a
    rung's hand-set ones, taken through the padding path every pre-g8
    checkpoint on disk takes. `artifacts/theta.npy` is itself written under the
    current layout, so its first `PRE_GENE_N` coordinates stand in for the
    checkpoint that was written before the block existed."""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "artifacts", "theta.npy")
    if not os.path.isfile(path):
        pytest.skip("no trained theta on this machine")
    full = np.load(path).astype(np.float32)
    assert full.shape[0] >= PRE_GENE_N
    short = full[:PRE_GENE_N].copy()
    padded = np.concatenate([short, np.zeros(PO.N_PARAMS - PRE_GENE_N, np.float32)])
    for a, b in zip(_decisions(short), _decisions(padded)):
        for f, x, y in zip(a._fields, a, b):
            np.testing.assert_array_equal(np.asarray(x), np.asarray(y), err_msg=f)
    assert all(int(m.hire_bias) == 0 for m in _decisions(padded))


def test_head_zero_is_not_a_free_slot_for_this_gene():
    """Why `g8` exists at all rather than a decode hung on `head[0]`.

    `head[0]` is the old `n_hire` and is in `policy.DEAD_HEAD`, so ES stopped
    updating `g2[:, 0]` -- it did not zero it. A gene placed there would decode
    to something different for every checkpoint trained before the masking.
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "artifacts", "theta.npy")
    if not os.path.isfile(path):
        pytest.skip("no trained theta on this machine")
    g2 = PO.unpack(np, np.load(path).astype(np.float32)).g2
    assert np.abs(g2[:, 0]).max() > 0.1


def test_the_inert_values_write_no_weights_at_all():
    plain = A.archetype_theta(land=3.0)
    assert np.array_equal(plain, A.archetype_theta(land=3.0, hire_bias=0.0))
    assert np.array_equal(plain, A.archetype_theta(land=3.0, animal_mix={}))
    assert np.array_equal(plain, A.archetype_theta(land=3.0, animal_mix=[0, 0, 0]))


# ------------------------------------------------------------- the crew gene

def test_the_hire_bias_decode_is_bounded_and_signed():
    for knob in (-3.0, -0.5, 0.0, 0.3, 3.0):
        got = int(brain.decide(np, A.archetype_theta(hire_bias=knob), OBS[0]).hire_bias)
        want = int(brain._qfloor(np, brain.HIRE_BIAS_MAX * np.tanh(np.float32(knob))))
        assert got == want, knob
        assert abs(got) <= brain.HIRE_BIAS_MAX


def test_a_positive_hire_bias_raises_the_crew_the_planner_chooses():
    """The point of the gene, measured through `build_day` rather than the
    decode: same board, same work, same purse -- only the bias moves.

    A day with 40 plantings queued and a full purse is deliberately *not*
    labour-saturated at the enumeration's own optimum, which is the state the
    Kaggle field beats us in (their 14 hands on day 10 against our 7-8).
    """
    view = _view(money=200_000, day=3)
    crews = [_crew(view, _macro(plant_target=np.array([40, 0, 0, 0, 0], np.int32),
                                hire_bias=np.int32(b)))
             for b in (0, 100, 250, 400, 1000)]
    assert crews == sorted(crews), crews
    assert crews[-1] > crews[0], crews
    assert crews[-1] == spec.MAX_HANDS, crews


def test_a_negative_hire_bias_lowers_it():
    view = _view(money=200_000, day=3)
    target = np.array([40, 0, 0, 0, 0], np.int32)
    base = _crew(view, _macro(plant_target=target, hire_bias=np.int32(0)))
    assert base > 0
    assert _crew(view, _macro(plant_target=target,
                              hire_bias=np.int32(-1000))) < base


def test_the_crew_gene_reaches_the_planner_from_a_theta():
    """End to end: a knob on `gb8`, through `brain.decide`, into 1.5's argmax.

    Both directions, because the decode is signed and because the positive one
    saturates on its own -- a day with a full purse and plenty of queued work
    already hires `MAX_HANDS` at bias 0, and that is the enumeration doing its
    job rather than the gene failing to reach it.
    """
    view = _view(money=200_000, day=3)

    def crew(knob):
        m = brain.decide(np, A.archetype_theta(hire_bias=knob), _obs(day=3, money=200_000))
        return _crew(view, m._replace(plant_target=np.array([40, 0, 0, 0, 0], np.int32)))

    crews = [crew(k) for k in (-2.0, -0.5, 0.0, 2.0)]
    assert crews == sorted(crews), crews
    assert crews[-1] > crews[0], crews


# ---------------------------------------------------------- the herd-mix gene

def _want(theta, obs=None):
    return np.asarray(brain.decide(np, theta, obs if obs is not None else OBS[0]).animal_want)


#: A herd rung with both pasture animals at the same, saturated grow score --
#: the configuration in which the want is 50/50 and nothing but `animal_mix`
#: can move it (`_CLONE_BOOK`'s MILK and WOOL are both 8.0).
_HERD = dict(A.named("wheat_clone"), hire_bias=0.0, animal_mix={})


def test_animal_mix_shifts_the_want_without_touching_the_grow_score():
    """The whole reason the gene is not another entry in the book.

    `grow_mult` *is* `_unit_ratio(grow)` clipped -- what `budget.grant` prices
    an animal at. A bias written into the book moves both; this one moves only
    the want, so a rung can ask for 2:1 sheep while a cow stays exactly as
    valuable and as affordable as it was.
    """
    base = A.archetype_theta(**_HERD)
    tilted = A.archetype_theta(**dict(_HERD, animal_mix={"SHEEP": float(np.log(2.0))}))

    m0, m1 = brain.decide(np, base, OBS[0]), brain.decide(np, tilted, OBS[0])
    np.testing.assert_array_equal(np.asarray(m0.grow_mult), np.asarray(m1.grow_mult))
    np.testing.assert_array_equal(np.asarray(m0.plant_target), np.asarray(m1.plant_target))
    assert int(np.sum(m0.animal_want)) == int(np.sum(m1.animal_want))

    w0, w1 = np.asarray(m0.animal_want), np.asarray(m1.animal_want)
    assert abs(int(w0[COW]) - int(w0[SHEEP])) <= 1, w0   # equal scores, equal want
    assert w1[SHEEP] > w1[COW], w1
    assert w1[SHEEP] > w0[SHEEP] and w1[COW] < w0[COW], (w0, w1)


def test_animal_mix_is_a_log_share_and_reads_off_the_entry():
    """`ln 2` of separation is a 2:1 want, to the unit. That readability is the
    reason the decode is a clipped identity rather than a `tanh` ramp."""
    tilted = A.archetype_theta(**dict(_HERD, animal_mix={"SHEEP": float(np.log(2.0))}))
    w = _want(tilted)
    total = int(w[COW] + w[SHEEP])
    assert total >= 6, w                     # enough animals for the ratio to show
    assert w[SHEEP] == pytest.approx(2 * w[COW], abs=1), w


def test_animal_mix_is_shift_invariant():
    a = A.archetype_theta(**dict(_HERD, animal_mix={"SHEEP": 0.7}))
    b = A.archetype_theta(**dict(_HERD, animal_mix={"COW": -0.7}))
    np.testing.assert_array_equal(_want(a), _want(b))


def test_animal_mix_is_clipped_and_stays_finite():
    hard = A.archetype_theta(**dict(_HERD, animal_mix={"SHEEP": 50.0}))
    w = _want(hard)
    assert np.isfinite(w).all() and w[COW] == 0 and w[SHEEP] > 0, w


def test_animal_mix_refuses_a_wrong_shaped_vector():
    with pytest.raises(ValueError):
        A.archetype_theta(animal_mix=[1.0, 2.0])
    with pytest.raises(ValueError):
        A.archetype_theta(animal_mix={"COW": 1.0, "PIG": 2.0})


# ------------------------------------------------------- the hire-bias buckets
#
# `hire_bias` was one number for the whole season. The Kaggle field's labour
# ramp is a shape -- 3-4 hands on day 5, 14 by day 10 -- and one number cannot
# say it: a bias big enough for the late crew buys the cheap early hands first
# and leaves the purse with nothing to plant with (`es/archetypes.py`, the
# `wheat_clone` v2 note). Four biases indexed by the day say it in the one
# place that was missing, and nowhere else: `plan` section 1.5 still receives a
# single integer.


def test_the_bucket_block_is_a_clean_append():
    """`g9` starts exactly where the previous layout ended, which is the whole
    reason an older theta is still a prefix rather than a re-layout."""
    assert PO.offset("g9") == PRE_BUCKET_N
    # The layout the *next* block appends to, so this stays a statement about
    # `g9` rather than about whatever was appended after it.
    assert PO.offset("g10") == (PRE_BUCKET_N + PO.N_HEAD_HID * PO.N_HIRE_EXTRA
                                + PO.N_HIRE_EXTRA) == 4848
    assert len(brain.HIRE_BIAS_BUCKETS) + 1 == PO.N_HIRE_BUCKETS == 4


def test_the_day_picks_the_bucket():
    """Days 0-5, 6-10, 11-20, 21+, tested on both sides of every edge."""
    ramp = (2.0, 1.0, -0.5, -2.0)
    want = [int(brain._qfloor(np, brain.HIRE_BIAS_MAX * np.tanh(np.float32(z))))
            for z in ramp]
    assert len(set(want)) == 4, want          # four distinct numbers to tell apart
    th = A.archetype_theta(hire_bias=ramp)
    got = {d: int(brain.decide(np, th, _obs(day=d)).hire_bias) for d in range(30)}
    for d, v in got.items():
        b = 0 if d < 6 else 1 if d < 11 else 2 if d < 21 else 3
        assert v == want[b], (d, v, b)


def test_a_scalar_hire_bias_is_still_one_number_for_the_season():
    """The knob did not change meaning: an entry that writes one number gets
    that number on every day, which is what every v1 and v2 rung wrote."""
    th = A.archetype_theta(hire_bias=0.3)
    assert len({int(brain.decide(np, th, _obs(day=d)).hire_bias)
                for d in range(30)}) == 1


def test_the_hire_bias_knob_refuses_a_wrong_shaped_ramp():
    with pytest.raises(ValueError):
        A.archetype_theta(hire_bias=(1.0, 2.0))


def test_a_pre_bucket_theta_keeps_its_bias_on_every_day():
    """The compatibility claim, and the one the pad has to *work* for.

    Zero in `g9` would mean "no bias from day 6 on", which is not what a theta
    written before the block said -- it said one number for the season. So
    `unpack` copies `g8` column 0 into the buckets when it pads, and truncating
    a four-bucket theta whose buckets are all equal must decode to the same
    `Macro`, field by field, on both sides of every edge.
    """
    full = A.archetype_theta(**dict(A.named("wheat_clone"), hire_bias=0.3))
    short = full[:PRE_BUCKET_N].copy()
    assert full[PO.offset("gb9"):].any()             # the buckets are really written
    for day in (0, 5, 6, 10, 11, 20, 21, 28):
        a = brain.decide(np, short, _obs(day=day))
        b = brain.decide(np, full, _obs(day=day))
        for f, x, y in zip(a._fields, a, b):
            np.testing.assert_array_equal(np.asarray(x), np.asarray(y),
                                          err_msg=f"{f} on day {day}")
        assert int(a.hire_bias) != 0                 # and it is not the trivial 0 == 0


def test_the_pad_carries_the_weight_column_and_not_only_the_bias():
    """A trained theta's crew gene is a 32-wide column of weights, not a bias.

    Hand-set rungs only ever write `gb8`, so a test that padded one of those
    would pass with the column copy missing entirely.
    """
    rng = np.random.default_rng(0)
    short = rng.normal(0.0, 0.3, PRE_BUCKET_N).astype(np.float32)
    p = PO.unpack(np, short)
    assert np.abs(np.asarray(p.g8)[:, 0]).max() > 0.0
    np.testing.assert_array_equal(
        np.asarray(p.g9), np.repeat(np.asarray(p.g8)[:, :1], PO.N_HIRE_EXTRA, axis=1))
    np.testing.assert_array_equal(
        np.asarray(p.gb9), np.repeat(np.asarray(p.gb8)[:1], PO.N_HIRE_EXTRA))
    # The decode's own statement of the same thing: on one board the four
    # buckets are one number. (Not "the same coins on every day": a trained
    # crew gene is a column of weights on the head's hidden layer, so its
    # *value* moves with the board -- the buckets moving together is the
    # invariant.) Exact after the quantisation, which is what `plan` reads;
    # the pre-activations agree to a float32 ulp rather than bit for bit,
    # because buckets 1..3 are their own matmul and a copied column is not a
    # copied *reduction*. A bias-only theta -- every rung here, and every
    # checkpoint on disk, whose `g8` block is zero -- is exact even there.
    prod, glob, drain = brain.features(np, _obs(day=0))
    out = PO.forward(np, p, prod, glob, drain)
    np.testing.assert_allclose(np.asarray(out.hire), float(out.crew[0]), rtol=1e-6)
    q = brain._qfloor(np, brain.HIRE_BIAS_MAX * np.tanh(out.hire)).astype(np.int32)
    assert len(set(np.asarray(q).tolist())) == 1, q


def test_the_flat_pad_is_the_same_pad_unpack_does():
    """`policy.pad` is what `scripts/train.py --resume` and `--init-theta` hand
    on, and a padded theta never reaches `unpack`'s legacy branch again -- so
    the copy has to happen there too or a resumed run silently loses its bias
    from day 6 on. Batched, because the trainer pads a pool and two Adam
    moments the same way."""
    rng = np.random.default_rng(1)
    short = rng.normal(0.0, 0.3, PRE_BUCKET_N).astype(np.float32)
    padded = PO.pad(short)
    assert padded.shape == (PO.N_PARAMS,) and padded.dtype == np.float32
    for day in (0, 6, 11, 21):
        a = brain.decide(np, short, _obs(day=day))
        b = brain.decide(np, padded, _obs(day=day))
        for f, x, y in zip(a._fields, a, b):
            np.testing.assert_array_equal(np.asarray(x), np.asarray(y), err_msg=f)

    pool = np.stack([short, np.zeros(PRE_BUCKET_N, np.float32)])
    got = PO.pad(pool)
    assert got.shape == (2, PO.N_PARAMS)
    np.testing.assert_array_equal(got[0], padded)
    np.testing.assert_array_equal(got[1], np.zeros(PO.N_PARAMS, np.float32))
    # A theta already at this layout is returned as it came.
    assert PO.pad(padded) is padded


def _crew_on(theta, day, view, plants=0):
    """Hands `plan` 1.5 hires on `day`, decoding `theta` against the same day.

    Both halves of the path in one call: the decode picks the bucket off
    `obs.day` and the planner enumerates against `view.day`, which is what
    makes this a test of the gene rather than of `_macro`.
    """
    m = brain.decide(np, theta, _obs(day=day, money=200_000))
    target = np.zeros(spec.N_CROPS, np.int32)
    target[spec.I_WHEAT] = plants
    return _crew(view, m._replace(plant_target=target))


def test_an_early_bucket_raises_the_day_10_crew():
    """What the buckets are *for*, in the planner rather than in the decode.

    Twelve queued plantings and a full purse: a day the enumeration settles
    well short of `MAX_HANDS` on, so the bias has somewhere to move it -- and
    it is bucket **1** that moves day 10, which a season-constant gene could
    not have said without also moving day 0.
    """
    flat = A.archetype_theta(hire_bias=0.0)
    ramp = A.archetype_theta(hire_bias=(0.0, 2.0, 0.0, 0.0))
    view = _view(money=200_000, day=10)
    assert _crew_on(ramp, 10, view, plants=12) > _crew_on(flat, 10, view, plants=12)
    # Day 3 is bucket 0, which this ramp leaves at zero: the gene reaches the
    # days it names and no others.
    v3 = _view(money=200_000, day=3)
    assert _crew_on(ramp, 3, v3, plants=12) == _crew_on(flat, 3, v3, plants=12)


def _late_board(day):
    """A late-season board with real work on it: every tile carries an ongoing
    crop with a harvest ready. `_view`'s plain board has none by then -- a
    planting made on day 22 cannot mature, so the day queues nothing and hires
    nobody, which is the enumeration's own answer and not the gene's."""
    return _view(money=200_000, day=day, full=True)._replace(
        t_yield=np.full(100, 3, np.int32))


@pytest.mark.parametrize("day", [21, 27])
def test_the_late_bucket_moves_the_late_crew(day):
    """Bucket 3 (days 21+), on a board whose work is a harvest rather than a
    planting. Signed, and read as the *difference* the bucket makes: the two
    thetas are identical everywhere else, so nothing but the day's bucket can
    separate them."""
    pos = A.archetype_theta(hire_bias=(0.0, 0.0, 0.0, 2.0))
    neg = A.archetype_theta(hire_bias=(0.0, 0.0, 0.0, -2.0))
    view = _late_board(day)
    assert _crew_on(pos, day, view) > _crew_on(neg, day, view)


def test_no_bucket_hires_on_the_terminal_day(monkeypatch):
    """The terminal day's crew is the enumeration's, not bucket 3's [LAW, 0.4].

    With `plan.DROP_ON` off -- the law this test was written against, before
    51e7b50 -- day 29 is past `ops.LAST_SHED_DAY`, nothing a hand does
    monetizes, and 1.5 hires nobody whatever the bucket says. On, which is the
    shipped default, the day-29 chain closes inside the day and its harvest is
    sold by the last lot (`valuation.pay_day()` = 29), so a board of ripe tiles
    on a 200,000 purse is work for the whole crew.

    Either way the bucket does not move it: the gene shifts the *score* of a
    count, and here both signs land on the same end of the enumeration -- zero
    with the horizon shut, `spec.MAX_HANDS` with it open.
    """
    pos = A.archetype_theta(hire_bias=(0.0, 0.0, 0.0, 2.0))
    neg = A.archetype_theta(hire_bias=(0.0, 0.0, 0.0, -2.0))
    board = _late_board(29)
    crew = spec.MAX_HANDS if P.DROP_ON else 0
    assert _crew_on(pos, 29, board) == crew
    assert _crew_on(neg, 29, board) == crew
    monkeypatch.setattr(P, "DROP_ON", False)
    assert _crew_on(pos, 29, board) == 0
    assert _crew_on(neg, 29, board) == 0


# Crop proportions have the same independent readout as animal proportions.
def test_crop_mix_is_zero_initialized_and_isolated_from_existing_parameters():
    from kagg3.es.train import train_mask

    assert PO.offset("cm") == 6855
    assert PO.offset("cb") == 7015
    # `cd` (CROP-DAY, 2026-09-14) is appended after `cb`, so the crop-mix
    # readout still ends where it did and the layout grows past it.
    assert PO.offset("cd") == 7020
    assert PO.N_PARAMS == 7395
    mask = train_mask("cm,cb") * PO.live_mask()
    assert not mask[:6855].any() and mask[6855:7020].all()
    assert not mask[7020:].any()
    assert int(mask.sum()) == 165
    initialized = PO.init_theta(np.random.default_rng(71))
    assert not initialized[6855:].any()
    old = np.load("artifacts/kagg2_games/thetas/flow193_g100_hr.npy")
    padded = PO.pad(old)
    assert padded[:len(old)].tobytes() == old.tobytes()
    for obs in OBS:
        short = brain.decide(np, old, obs)
        full = brain.decide(np, padded, obs)
        for field, a, b in zip(short._fields, short, full):
            np.testing.assert_array_equal(a, b, err_msg=field)


def test_crop_mix_matrix_reads_context_without_a_bias():
    # Isolate one matrix edge; a cb-only implementation must fail this check.
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("gb1")] = np.float32(0.5)
    theta[PO.offset("cm") + spec.I_MELON] = np.float32(2.0)
    params = PO.unpack(np, theta)
    prod = np.zeros((spec.N_PRODUCTS, PO.N_PROD_FEAT), np.float32)
    glob = np.zeros(PO.N_GLOBAL_FEAT, np.float32)
    drain = np.zeros((spec.N_PRODUCTS, PO.N_DRAIN_FEAT), np.float32)
    out = PO.forward(np, params, prod, glob, drain)
    expected = np.zeros(spec.N_CROPS, np.float32)
    expected[spec.I_MELON] = 2 * np.tanh(np.float32(0.5))
    np.testing.assert_array_equal(out.crop_mix, expected)


@pytest.mark.parametrize("crop", range(spec.N_CROPS))
def test_crop_mix_changes_proportions_without_changing_valuation_or_herd(crop):
    theta = PO.pad(np.load("artifacts/kagg2_games/thetas/flow193_g100_hr.npy"))
    before = brain.decide(np, theta, OBS[0])
    theta[PO.offset("cb") + crop] = 10.0
    after = brain.decide(np, theta, OBS[0])
    assert after.plant_target[crop] > before.plant_target[crop]
    assert after.plant_target.sum() == before.plant_target.sum()
    assert (after.plant_target >= 0).all()
    for field in before._fields:
        if field != "plant_target":
            np.testing.assert_array_equal(getattr(before, field), getattr(after, field),
                                          err_msg=field)
    # An allocation preference cannot make a late crop mature before payday.
    late = _obs(day=20)
    theta[PO.offset("cb"):PO.offset("cb") + spec.N_CROPS] = 0
    theta[PO.offset("cb") + spec.I_MELON] = 100
    assert brain.decide(np, theta, late).plant_target[spec.I_MELON] == 0


def test_crop_mix_matches_complete_plans_across_backends():
    import jax
    import jax.numpy as jnp
    from test_forward_value import BOARDS, TABLE, _obs_of

    old = np.load("artifacts/kagg2_games/thetas/flow193_g100_hr.npy")
    padded = PO.pad(old)
    live = padded.copy()
    live[PO.offset("cm"):PO.offset("cb")] = np.random.default_rng(82).normal(
        0.0, 0.5, PO.N_HEAD_HID * spec.N_CROPS)
    live[PO.offset("cb") + spec.I_MELON] = 6.0

    def evaluate(xp, theta, obs, view, table):
        m = brain.decide(xp, theta, obs)
        return tuple(m) + tuple(P.build_day(xp, view, m, table)[:6])

    compiled = jax.jit(lambda theta, obs, view, table:
                       evaluate(jnp, theta, obs, view, table))
    names = list(P.Macro._fields) + [f"plan_{i}" for i in range(6)]
    for view in (BOARDS[0], BOARDS[-1]):
        obs = _obs_of(view)
        baseline = evaluate(np, old, obs, view, TABLE)
        jax_baseline = None
        for theta in (old, padded, live):
            expected = evaluate(np, theta, obs, view, TABLE)
            actual = compiled(jnp.asarray(theta),
                              jax.tree_util.tree_map(jnp.asarray, obs),
                              jax.tree_util.tree_map(jnp.asarray, view), jnp.asarray(TABLE))
            for field, a, b in zip(names, expected, actual):
                a, b = np.asarray(a), np.asarray(b)
                assert a.dtype == b.dtype and a.shape == b.shape, field
                assert a.tobytes() == b.tobytes(), field
            if theta is old:
                jax_baseline = actual
            if theta is padded:
                for field, a, b, ja, jb in zip(names, baseline, expected,
                                              jax_baseline, actual):
                    np.testing.assert_array_equal(a, b, err_msg=field)
                    assert np.asarray(ja).tobytes() == np.asarray(jb).tobytes(), field
