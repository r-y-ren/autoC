"""Training on the states the policy never reaches on its own.

`land1` (gen 6,627) requests land on 0/30 days along its own trajectory, yet
asks for it on days 27-29 once *forced* into a 2-quadrant, 45k-coin state. ES
gets no gradient on multi-quadrant play because no training episode ever
visits it. A fraction of episodes therefore start warm -- extra quadrants
already unlocked and cash in hand -- for **both** seats alike, so the margin
stays fair and common random numbers still hold across the population.

Cold start must stay byte-identical: the submission, the engine-equivalence
gate and every ladder measurement run from the engine's own day-0 state.

The **asymmetric** opening is the other half of this file, and it is the one
with a trap in it. `kagg2_proxy` plays from extra quadrants and extra cash so
that a strong policy meets, in sim, something like the opponent it meets in the
real engine -- and `Trainer._play` used to index the start arrays by seed
*pair*, while `make_evaluator.one` seats the candidate at player 0 only on seat
0. A per-pair asymmetric row therefore lands on the rung in one game of the
pair and on **us** in the other, which is not a handicap, it is a coin flip
about who is rich. Starts are built at episode resolution for exactly that
reason, and the tests below assert the negative: our seat never receives it.
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

import jax.numpy as jnp
import numpy as np
import pytest

from kagg3 import spec
from kagg3.es import archetypes as A
from kagg3.es.train import Config, Trainer, opponent_slots, place_handicap
from kagg3.sim.state import initial_state


def _tree_equal(a, b):
    return all(np.array_equal(np.asarray(x), np.asarray(y))
               for x, y in zip(a, b))


def test_explicit_engine_defaults_match_the_implicit_cold_start():
    cold = initial_state(jnp)
    explicit = initial_state(jnp, nquad=jnp.ones((2,), jnp.int32),
                             money=jnp.full((2,), spec.STARTING_MONEY, jnp.int32))
    assert _tree_equal(cold, explicit)


def test_warm_start_unlocks_quadrants_in_land_order_per_seat():
    st = initial_state(jnp, nquad=jnp.asarray([3, 1], jnp.int32),
                       money=jnp.asarray([20_000, 3_000], jnp.int32))
    quad = spec.TILE_QUAD
    kind = np.asarray(st.kind)

    open0 = {0, int(spec.LAND_ORDER[0]), int(spec.LAND_ORDER[1])}
    for q in range(4):
        want = spec.KIND_EMPTY if q in open0 else spec.KIND_LOCKED
        assert (kind[0][quad == q] == want).all(), f"seat 0 quad {q}"
        want1 = spec.KIND_EMPTY if q == 0 else spec.KIND_LOCKED
        assert (kind[1][quad == q] == want1).all(), f"seat 1 quad {q}"
    assert np.asarray(st.nquad).tolist() == [3, 1]
    assert np.asarray(st.money).tolist() == [20_000, 3_000]


def _bare_trainer(**kw):
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**kw)
    tr.rng = np.random.default_rng(0)
    return tr


def test_warm_frac_zero_draws_only_the_engine_start():
    tr = _bare_trainer(warm_frac=0.0)
    nquad, money = tr.draw_starts(64)
    assert nquad.shape == (64, 2) and money.shape == (64, 2)
    assert (nquad == 1).all()
    assert (money == spec.STARTING_MONEY).all()


def test_warm_frac_one_draws_extra_land_and_cash_for_both_seats_alike():
    tr = _bare_trainer(warm_frac=1.0)
    nquad, money = tr.draw_starts(64)
    assert ((nquad >= 2) & (nquad <= 4)).all()
    assert ((money >= spec.STARTING_MONEY) & (money <= 40_000)).all()
    # Symmetric: the opponent plays the same off-distribution state.
    assert (nquad[:, 0] == nquad[:, 1]).all()
    assert (money[:, 0] == money[:, 1]).all()
    # Not degenerate: the draw actually covers the range.
    assert len(set(nquad[:, 0].tolist())) == 3


def test_warm_frac_quarter_warms_about_a_quarter_of_the_pairs():
    tr = _bare_trainer(warm_frac=0.25)
    nquad, _ = tr.draw_starts(400)
    warm = (nquad[:, 0] > 1).mean()
    assert 0.15 < warm < 0.35


# ------------------------------------------------------- the asymmetric opening

#: Deliberately **not** `A.PROXY_HANDICAP`. The fitted opening is money-only
#: (`1:87000`), so a quadrant assertion against it could not tell a handicapped
#: seat from an untouched one; this asks for extra land as well, which is what
#: makes "the opening lands on exactly one column of exactly one seat" testable
#: on both columns. The seat rule is what is under test, not the level.
PROXY = (3, 20_000)

#: The whole named ladder, so the proxy is in it.
FULL_LADDER = len(A.NAMES)

#: The longest ladder that does **not** reach the proxy, i.e. what
#: `--n-archetypes` has to be for the handicap to have nowhere to land.
#: Read off `NAMES` rather than written as `len(NAMES) - 1`: the proxy was
#: the last entry when this file was written, and 4ef23c4 (2026-08-28)
#: appended the Kaggle field rungs *behind* it, so "one short of the whole
#: ladder" has meant "the proxy is still in it" ever since.
COLD_LADDER = A.NAMES.index(A.PROXY_NAME)


def _proxy_trainer(n_arch=FULL_LADDER, **kw):
    """A `Trainer` with a ladder and a handicapped proxy, without a rollout.

    `_bind_rungs` is the whole subject here -- which rung gets the opening and
    which seat of which episode it lands on -- and none of that needs the
    archetype thetas to have been probed, so this skips the probe's rollouts.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(n_archetypes=n_arch, **dict({"proxy_handicap": PROXY}, **kw))
    tr.rng = np.random.default_rng(0)
    tr.archetype_names = list(A.NAMES[:n_arch])
    tr.pool = [None, None, None]
    tr.archetypes = [None] * n_arch
    tr._bind_rungs()
    return tr


def test_only_the_proxy_rung_carries_an_opening_handicap():
    tr = _proxy_trainer()
    hcap = {n: tuple(int(x) for x in h)
            for n, h in zip(tr.archetype_names, tr.arch_handicap)}
    assert hcap[A.PROXY_NAME] == PROXY
    others = {n: h for n, h in hcap.items() if n != A.PROXY_NAME}
    assert set(others.values()) == {A.NO_HANDICAP}, others
    # `kagg2_proxy` is `mixed_ranch`'s knobs; the *opening* is the whole
    # difference between the two rungs, so the cold twin must stay cold.
    assert A.named(A.PROXY_NAME) == A.named("mixed_ranch")
    assert hcap["mixed_ranch"] == A.NO_HANDICAP


def test_a_handicap_with_no_rung_to_land_on_is_refused():
    """The silent failure `--resume` hides, and the only one worth raising for.

    On resume the archetype set comes from the *checkpoint*, not from
    `--n-archetypes`, so an 8-rung run resumed with `--n-archetypes 9
    --proxy-handicap` keeps its eight cold rungs and trains against no proxy at
    all -- while `config.json` records the flag and the operator reads a log
    that says the run is on the new objective. `scripts/train.py` catches the
    cold-start half of this before the run directory exists; this catches the
    half it cannot see.

    The ladder that refuses is `COLD_LADDER` rungs -- the eight in front of
    the proxy -- and not `len(NAMES) - 1`, which stopped being short of the
    proxy at 4ef23c4: rungs appended behind it leave it on every ladder
    long enough to reach them, so the old expression built a ladder that
    *has* the rung and asserted a refusal that was correct not to come.
    """
    with pytest.raises(ValueError, match=f"no `{A.PROXY_NAME}` rung"):
        _proxy_trainer(n_arch=COLD_LADDER)

    # And the default handicap is nobody's business: a ladder without the rung
    # is exactly as legal as it was before the rung existed.
    tr = _proxy_trainer(n_arch=4, proxy_handicap=A.NO_HANDICAP)
    assert [tuple(int(x) for x in h) for h in tr.arch_handicap] \
        == [A.NO_HANDICAP] * 4


def test_the_handicap_reaches_the_opponent_seat_of_the_proxys_episodes_only():
    """The trap, asserted from both sides.

    Every episode of a proxy pair hands the opening to the *opponent's*
    physical player, and no episode anywhere hands it to ours. Checked over
    both seats of every pair, because the whole failure mode is that the two
    seats of one pair disagree.
    """
    tr = _proxy_trainer(warm_frac=0.0)
    # Enough pairs for the round-robin to reach the ninth rung twice: at
    # `arch_frac` 0.5 the archetype block is half of them.
    n_pairs = 4 * len(A.NAMES)
    idx = opponent_slots(n_pairs, len(tr.pool), len(tr.archetypes), 0.5)
    nquad, money = tr.episode_starts(n_pairs, idx)

    assert nquad.shape == money.shape == (2 * n_pairs, 2)
    proxy_slot = len(tr.pool) + tr.archetype_names.index(A.PROXY_NAME)
    e = np.arange(2 * n_pairs)
    seat = e % 2                     # our seat; the opponent sits at 1 - seat
    is_proxy = np.asarray(idx)[e // 2] == proxy_slot
    assert is_proxy.any() and not is_proxy.all(), "the split must be non-trivial"

    ours_q, ours_m = nquad[e, seat], money[e, seat]
    theirs_q, theirs_m = nquad[e, 1 - seat], money[e, 1 - seat]

    # Ours is the engine's day 0 in every single episode, proxy pairs included.
    assert (ours_q == 1).all()
    assert (ours_m == spec.STARTING_MONEY).all()
    # Theirs is the handicap on exactly the proxy's episodes and nowhere else.
    assert (theirs_q[is_proxy] == PROXY[0]).all()
    assert (theirs_m[is_proxy] == PROXY[1]).all()
    assert (theirs_q[~is_proxy] == 1).all()
    assert (theirs_m[~is_proxy] == spec.STARTING_MONEY).all()


def test_both_seats_of_a_proxy_pair_are_handicapped_the_same_way():
    """Seat 0 and seat 1 of one pair must be mirror images, not opposites.

    Indexed by pair, an asymmetric row would put the opening on column 1 in
    both games of the pair -- which is the rung on seat 0 and *us* on seat 1.
    The margin over the pair would then average a handicapped opponent with a
    handicapped self and measure nothing.
    """
    tr = _proxy_trainer(warm_frac=0.0)
    n_pairs = 2 * len(A.NAMES)
    idx = opponent_slots(n_pairs, len(tr.pool), len(tr.archetypes), 1.0)
    nquad, _ = tr.episode_starts(n_pairs, idx)
    proxy_slot = len(tr.pool) + tr.archetype_names.index(A.PROXY_NAME)
    assert (idx == proxy_slot).sum() == 2
    for p in range(n_pairs):
        if idx[p] != proxy_slot:
            continue
        # seat 0: opponent is player 1. seat 1: opponent is player 0.
        assert nquad[2 * p].tolist() == [1, PROXY[0]]
        assert nquad[2 * p + 1].tolist() == [PROXY[0], 1]


def test_no_handicap_leaves_episode_starts_as_the_pair_draw_repeated():
    """The default is the run that was there before: both seats share a start."""
    tr = _proxy_trainer(warm_frac=1.0)
    tr.cfg = tr.cfg._replace(proxy_handicap=A.NO_HANDICAP)
    tr._bind_rungs()
    n_pairs = 16
    idx = opponent_slots(n_pairs, len(tr.pool), len(tr.archetypes), 0.5)
    tr.rng = np.random.default_rng(0)
    nquad, money = tr.episode_starts(n_pairs, idx)
    tr.rng = np.random.default_rng(0)
    pair_q, pair_m = tr.draw_starts(n_pairs)

    assert np.array_equal(nquad, np.repeat(pair_q, 2, axis=0))
    assert np.array_equal(money, np.repeat(pair_m, 2, axis=0))
    assert (nquad[:, 0] == nquad[:, 1]).all()


def test_a_handicap_can_only_add_never_walk_a_warm_start_back():
    """`warm_frac` opens some pairs on up to 4 quadrants and 40,000 coins.

    The rung's opening is a floor on top of that, not a replacement: walking a
    warm opponent *back* to 3 quadrants would make the handicap a penalty on
    exactly the pairs it was least needed on.
    """
    nquad = np.array([[4, 4], [1, 1], [2, 2]], np.int32)
    money = np.array([[40_000, 40_000], [3_000, 3_000], [9_000, 9_000]], np.int32)
    got_q, got_m = place_handicap(nquad, money, np.array([1, 1, 0]),
                                  np.array([PROXY, PROXY, PROXY], np.int32))

    assert got_q.tolist() == [[4, 4], [1, 3], [3, 2]]
    assert got_m.tolist() == [[40_000, 40_000], [3_000, 20_000], [20_000, 9_000]]
    # And the input is not mutated: `draw_starts` hands out one array a
    # generation and `_play` reads it after this.
    assert nquad.tolist() == [[4, 4], [1, 1], [2, 2]]


def test_the_probe_puts_the_handicap_on_the_rungs_own_seat():
    """`_probe_archetypes` reverses the seats: there the rung is the candidate.

    The archetype is passed as `theta_c`, so it sits at physical player `seat`,
    not `1 - seat`. Getting that backwards would hand the opening to the zero
    theta and measure a rung that never played its own game.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(abs_pairs=2)
    tr.n = 3
    tr.tables = None
    tr.abs_words = jnp.zeros((2, 3, 4), jnp.uint32)
    seen = {}

    def spy(tables, cand, opp, words, seat, nq, mo):
        seen.update(seat=np.asarray(seat), nq=np.asarray(nq), mo=np.asarray(mo))
        return jnp.zeros((cand.shape[0], 2))

    tr.evaluate = spy
    tr._probe_archetypes([jnp.zeros(3), jnp.zeros(3)],
                         np.array([A.NO_HANDICAP, PROXY], np.int32))

    seat, nq, mo = seen["seat"], seen["nq"], seen["mo"]
    e = np.arange(len(seat))
    per = len(seat) // 2
    rung1 = e >= per                              # the handicapped one
    assert (nq[e, seat][rung1] == PROXY[0]).all()
    assert (mo[e, seat][rung1] == PROXY[1]).all()
    assert (nq[e, 1 - seat] == 1).all()           # the zero theta stays cold
    assert (nq[e, seat][~rung1] == 1).all()


def test_warm_episode_runs_and_keeps_its_extra_land():
    from kagg3.core import policy as PO
    from kagg3.es.train import host_words
    from kagg3.sim import eod, rollout
    from kagg3.sim.state import build_tables

    rng = np.random.default_rng(0)
    thetas = jnp.stack([jnp.asarray(PO.init_theta(rng)) for _ in range(2)])
    words = jnp.asarray(host_words([7])[0])
    hi_t, lo_t = eod.weed_threshold()
    tables = build_tables(jnp)
    nquad = jnp.asarray([3, 3], jnp.int32)
    money = jnp.asarray([15_000, 15_000], jnp.int32)

    final, _, st = rollout.episode(tables, thetas, words, jnp.int32(hi_t), jnp.int32(lo_t),
                                   start_nquad=nquad, start_money=money)

    assert np.isfinite(np.asarray(final)).all()
    assert (np.asarray(st.nquad) >= 3).all()
    locked = (np.asarray(st.kind) == spec.KIND_LOCKED).sum(axis=1)
    assert (locked <= 25).all()
