"""The two defects sections 2 and 3 of the 2026-09-08 plateau review name.

**Section 2** -- `opponent_slots` allocated the archetype block with plain
largest-remainder rounding, a pure function of `(k, weights)`. With an
unchanged configuration the same rungs took the leftover slots in *every*
generation, so a ladder wider than the block lost its tail outright: 127
equally-weighted tapes at 256 episodes (115 archetype pairs) never sampled the
last 12, in any generation of the run. `--slot-rotation carry` runs the same
allocation as a token bucket, so the leftovers rotate and the long-run share is
the requested one.

**Section 3** -- `paired_stats` pairs on `(seed, opponent, seat)` and then
computed the standard error as if the two mirrored seats of a board were
independent evidence. They are not: same board, same market draw, frequently
the same outcome. The review's probe took ten independent outcomes from
t = 3.00 to t = 4.36 by duplicating each into a second seat and nothing else.

Arithmetic only -- no engine, no rollouts.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import numpy as np
import pytest

from kagg3.es.train import (SlotCarry, arch_pairs, largest_remainder,
                            opponent_slots, paired_stats)


# ------------------------------------------------- section 2: the allocation

def test_the_fixed_rule_leaves_the_tail_of_a_wide_pool_unsampled():
    """The defect, reproduced: the review's 127-tape row of the probe table.

    256 episodes is 128 pairs; `arch_frac` 0.9 makes 115 of them archetype
    pairs; 115 slots over 127 equally-weighted rungs is 12 rungs at zero -- the
    same 12, in every generation, because the rule has no state to rotate.
    """
    n_arch, n_pairs = 127, 128
    idx = opponent_slots(n_pairs, n_pool=12, n_arch=n_arch, arch_frac=0.9)
    faced = np.bincount(idx[:115] - 12, minlength=n_arch)
    assert (faced == 0).sum() == 12
    # And a second generation is the identical row: nothing rotates.
    again = opponent_slots(n_pairs, n_pool=12, n_arch=n_arch, arch_frac=0.9)
    assert np.array_equal(idx, again)


def test_every_tape_in_a_127_rung_pool_is_sampled_over_100_generations():
    """The fix, on the configuration the review measured.

    100 generations at 115 slots is 11,500 slots over 127 rungs -- about 90
    each. Every rung has to get some, and the shares have to be even, because
    the weights are.
    """
    n_arch, n_pairs, gens = 127, 128, 100
    carry = SlotCarry()
    w = np.ones(n_arch)
    k = arch_pairs(n_pairs, n_arch, 0.9)
    assert k == 115
    total = np.zeros(n_arch, np.int64)
    for _ in range(gens):
        take = carry.take(k, w)
        assert take.sum() == k
        assert (take >= 0).all()
        total += take
    assert (total > 0).all(), f"{int((total == 0).sum())} rungs never sampled"
    share = total / total.sum()
    want = w / w.sum()
    # Within 2% of the requested share, relative.
    assert np.abs(share / want - 1.0).max() < 0.02


def test_the_long_run_share_follows_the_weights():
    """Uneven weights, same guarantee: the bucket is proportional, not merely
    non-starving. A rung on weight 3 gets three times a rung on weight 1, and a
    rung on weight 0 gets nothing at all."""
    w = np.array([3.0, 1.0, 1.0, 0.5, 2.0, 0.0, 1.5] * 6)   # 42 rungs
    carry = SlotCarry()
    total = np.zeros(len(w), np.int64)
    for _ in range(200):
        total += carry.take(37, w)
    assert total.sum() == 200 * 37
    assert total[5::7].sum() == 0          # every weight-0 rung, never faced
    share = total / total.sum()
    want = w / w.sum()
    live = want > 0
    assert np.abs(share[live] / want[live] - 1.0).max() < 0.02
    assert (total[live] > 0).all()


def test_the_credit_never_drifts_and_stays_bounded():
    """Why the share above is a guarantee rather than a measurement: the
    credit vector sums to zero after every generation and no entry can fall
    below -1, so a rung's cumulative slots track its weight to within one slot
    forever."""
    w = np.array([5.0, 1.0, 1.0, 1.0, 0.25])
    carry = SlotCarry()
    for _ in range(300):
        carry.take(3, w)
        assert abs(carry.credit.sum()) < 1e-9
        assert carry.credit.min() >= -1.0 - 1e-9


def test_generation_zero_of_a_uniform_ladder_matches_the_round_robin():
    """The rotation changes *which* generation a rung is faced in, not the
    counts a small ladder gets: at 8 rungs and 16 slots both rules give two
    each, and the first generation of a partial ladder gives the low-numbered
    rungs the spare slots exactly as the round-robin did."""
    for n_arch, k in ((8, 16), (9, 16), (4, 7)):
        take = SlotCarry().take(k, np.ones(n_arch))
        rr = np.bincount(np.arange(k) % n_arch, minlength=n_arch)
        assert np.array_equal(take, rr), (n_arch, k)


def test_a_rotated_allocation_is_still_a_valid_opponent_row():
    take = SlotCarry().take(arch_pairs(32, 5, 0.5), np.ones(5))
    idx = opponent_slots(32, n_pool=3, n_arch=5, arch_frac=0.5,
                         weights=np.ones(5), take=take)
    assert idx.shape == (32,)
    assert idx.min() >= 0 and idx.max() < 3 + 5 + 1
    assert np.array_equal(np.bincount(idx[:16] - 3, minlength=5), take)
    # The self-play half is the same round-robin it always was.
    assert np.array_equal(idx[16:],
                          opponent_slots(32, 3, 5, 0.5)[16:])


def test_a_take_that_does_not_spend_the_block_is_refused():
    with pytest.raises(ValueError, match="rung counts sum to"):
        opponent_slots(32, 3, 5, 0.5, np.ones(5), take=np.array([1, 1, 1, 1, 1]))
    with pytest.raises(ValueError, match="rung counts for"):
        opponent_slots(32, 3, 5, 0.5, np.ones(5), take=np.array([16, 0]))


def test_the_fixed_rule_is_untouched():
    """`--slot-rotation fixed` has to be the run that came before, byte for
    byte, or a resume cannot be compared with its own history."""
    a = opponent_slots(32, 12, 9, 0.5)
    b = opponent_slots(32, 12, 9, 0.5)
    assert np.array_equal(a, b)
    w = np.array([3.0, 2.0, 1.5] + [1.0] * 6)
    assert np.array_equal(
        np.bincount(opponent_slots(32, 12, 9, 0.5, w)[:16] - 12, minlength=9),
        largest_remainder(16, w))


# ------------------------------- section 2: common random numbers, in the sim

class _Stub:
    """Just enough of a Trainer for `opponent_index` -- no rollouts, no XLA."""

    def __init__(self, n_pool, n_arch, arch_frac, rotation="carry", weights=None):
        from kagg3.es.train import Config
        self.cfg = Config(arch_frac=arch_frac, slot_rotation=rotation)
        self.pool = [None] * n_pool
        self.archetypes = [None] * n_arch
        self._w = weights
        self.slot_carry = SlotCarry() if rotation == "carry" else None

    def weighted_slots(self):
        return self._w

    opponent_index = None       # bound below


def _index(stub, n_pairs):
    from kagg3.es.train import Trainer
    return Trainer.opponent_index(stub, n_pairs)


def test_one_opponent_row_serves_the_whole_population():
    """The rotation is *between* generations. Within one, every candidate
    plays one opponent list on one seed list -- which is what makes the
    antithetic pair's difference a gradient and not a board lottery.

    Two halves. `opponent_index` returns **one** row per generation, with no
    candidate axis: there is nothing per-candidate to differ. And
    `Trainer.generation` draws it once, before the population is stacked, so a
    refactor that moved the draw inside a per-candidate loop fails here.

    Twice in the source, once at run time: `--pinned-once` takes the second
    call (the residual budget, with the pinned rungs dropped) and every other
    run takes the first. They are the two arms of one `if`, so what the
    assertion below is about -- nothing between the draw and the rollout
    re-draws it -- is unchanged.
    """
    stub = _Stub(n_pool=4, n_arch=6, arch_frac=0.5)
    row = _index(stub, 32)
    assert row.shape == (32,)                   # per episode pair, full stop
    assert row.dtype == np.int64

    import inspect
    from kagg3.es.train import Trainer
    src = inspect.getsource(Trainer.generation)
    draw = "idx, keep = self.opponent_index(n_pairs), None"
    assert src.count(draw) == 1, "the unflagged row is drawn once"
    assert src.count("self.opponent_index(") == 2, "one draw per arm, no more"
    body = src[src.index("opp = jnp.stack"):src.index("money = ")]
    assert "opponent_index" not in body          # not re-drawn per candidate
    assert "opp = jnp.stack([candidates[i] for i in idx])" in src


def test_the_row_rotates_between_generations_but_keeps_its_shape():
    """The same stub, two generations: the counts move, the block size does
    not, and the fixed rule does not move at all."""
    stub = _Stub(n_pool=4, n_arch=9, arch_frac=0.5)
    rows = [_index(stub, 32) for _ in range(4)]
    counts = [np.bincount(r[:16] - 4, minlength=9) for r in rows]
    assert all(c.sum() == 16 for c in counts)
    assert not all(np.array_equal(counts[0], c) for c in counts[1:])
    total = sum(counts)
    assert (total > 0).all()

    fixed = _Stub(n_pool=4, n_arch=9, arch_frac=0.5, rotation="fixed")
    frows = [_index(fixed, 32) for _ in range(4)]
    assert all(np.array_equal(frows[0], r) for r in frows[1:])


def test_a_uniform_ladder_still_rotates_under_carry():
    """`weighted_slots()` says `None` for an all-ones ladder, which under the
    fixed rule means the interleaved round-robin -- and a uniform 127-rung
    ladder is exactly the case that truncates. The rotating rule has to fill
    the vector in rather than fall through to it."""
    stub = _Stub(n_pool=12, n_arch=127, arch_frac=0.9, weights=None)
    seen = np.zeros(127, np.int64)
    for _ in range(100):
        r = _index(stub, 128)
        seen += np.bincount(r[:115] - 12, minlength=127)
    assert (seen > 0).all()


def test_the_carry_survives_a_ladder_that_changed_width():
    """`--resume` plus a new `--tape-rung`. The credit is only meaningful as a
    zero-sum vector, so a re-sized one is re-centred rather than handing the
    survivors a head start they never earned against this rung set."""
    c = SlotCarry()
    c.take(7, np.ones(5))
    c.resize(8)
    assert len(c.credit) == 8
    assert abs(c.credit.sum()) < 1e-9
    take = c.take(8, np.ones(8))
    assert take.sum() == 8


# ---------------------------------------------- section 3: the mirrored seats

def _rows(outcomes, seats=(0,)):
    """`{(seed, opp, seat): (mine, theirs)}` for one leg."""
    return {(i, "o", s): v for i, v in enumerate(outcomes) for s in seats}


def test_duplicating_a_seat_no_longer_inflates_the_t():
    """The review's probe, exactly: ten independent board outcomes, then the
    same ten duplicated into a second seat. Row-independent standard errors
    took t from 3.00 to 4.36 on evidence that did not grow. Grouped, the two
    readings are the same number."""
    margins = [12_000.0, 9_000.0, 15_000.0, 3_000.0, 11_000.0,
               -2_000.0, 8_000.0, 14_000.0, 6_000.0, 10_000.0]
    inc = _rows([(100_000.0, 100_000.0)] * 10)
    cand = _rows([(100_000.0 + m, 100_000.0) for m in margins])
    one = paired_stats(cand, inc)
    assert one["n"] == 10 and one["boards"] == 10

    inc2 = _rows([(100_000.0, 100_000.0)] * 10, seats=(0, 1))
    cand2 = _rows([(100_000.0 + m, 100_000.0) for m in margins], seats=(0, 1))
    two = paired_stats(cand2, inc2)
    assert two["n"] == 20                       # twenty games...
    assert two["boards"] == 10                  # ...ten boards
    assert two["t_margin"] == pytest.approx(one["t_margin"], rel=1e-9)
    assert two["margin"] == pytest.approx(one["margin"], rel=1e-9)
    assert two["win"] == pytest.approx(one["win"], rel=1e-9)

    # And the old rule is the inflation the review measured: about sqrt(2) of
    # it (a shade more, because `ddof=1` over 2n rows divides by 2n-1).
    old = paired_stats(cand2, inc2, group_seats=False)
    assert old["t_margin"] / one["t_margin"] == pytest.approx(1.4530, rel=1e-3)


def test_the_probe_s_own_numbers():
    """The review's table, to two decimals: **3.00 -> 4.36** on ten
    independent board outcomes duplicated into a second seat, and back to 3.00
    once the seats are grouped."""
    d = np.array([1.0] * 9 + [-0.5])
    d = d - d.mean() + (3.0 * d.std(ddof=1) / np.sqrt(10))
    inc = _rows([(0.0, 0.0)] * 10)
    cand = _rows([(float(x), 0.0) for x in d])
    assert paired_stats(cand, inc)["t_margin"] == pytest.approx(3.0, rel=1e-9)
    inc2 = _rows([(0.0, 0.0)] * 10, seats=(0, 1))
    cand2 = _rows([(float(x), 0.0) for x in d], seats=(0, 1))
    assert paired_stats(cand2, inc2, group_seats=False)["t_margin"] == \
        pytest.approx(4.36, abs=5e-3)
    assert paired_stats(cand2, inc2)["t_margin"] == pytest.approx(3.0, rel=1e-9)


def test_the_two_seats_of_a_board_are_averaged_not_dropped():
    """A board whose seats disagree contributes their mean, not one of them:
    seat asymmetry is signal about the board, and dropping a seat would throw
    away half the games as well as half the standard error."""
    inc = {(0, "o", 0): (0.0, 0.0), (0, "o", 1): (0.0, 0.0),
           (1, "o", 0): (0.0, 0.0), (1, "o", 1): (0.0, 0.0)}
    cand = {(0, "o", 0): (10.0, 0.0), (0, "o", 1): (0.0, 0.0),
            (1, "o", 0): (10.0, 0.0), (1, "o", 1): (0.0, 0.0)}
    st = paired_stats(cand, inc)
    assert st["boards"] == 2
    assert st["margin"] == pytest.approx(5.0)     # the mean over four games
    # Both boards read +5, so the difference never varies: an infinite t, and
    # correctly so -- the candidate beat the incumbent on every board.
    assert st["t_margin"] == np.inf


def test_two_opponents_on_the_same_seed_are_two_boards():
    """The group is `(seed, opponent)`, not `seed`: one seed base plays every
    opponent in the gate's field, and those are different games."""
    inc = {(0, "a", 0): (0.0, 0.0), (0, "b", 0): (0.0, 0.0)}
    cand = {(0, "a", 0): (1.0, 0.0), (0, "b", 0): (2.0, 0.0)}
    assert paired_stats(cand, inc)["boards"] == 2


def test_the_single_seat_case_is_unchanged():
    """Every existing gate CSV in the campaign writes one row per game with a
    distinct seed, so the grouping is a no-op on them and no historical verdict
    moves."""
    cand = {(i, "o", i % 2): (100.0, 0.0) if i < 13 else (0.0, 100.0)
            for i in range(24)}
    inc = {(i, "o", i % 2): (100.0, 0.0) if i < 12 else (0.0, 100.0)
           for i in range(24)}
    st = paired_stats(cand, inc)
    assert st["n"] == 24 and st["boards"] == 24
    assert st["t_win"] == pytest.approx(1.0)
    assert st["t_win"] == pytest.approx(
        paired_stats(cand, inc, group_seats=False)["t_win"])


# ---------------------------------------- the arch_frac 0 trap, made loud

def test_arch_pairs_is_the_block_size_both_rules_use():
    assert arch_pairs(128, 127, 0.9) == 115
    assert arch_pairs(128, 127, 0.0) == 0        # the trap
    assert arch_pairs(128, 0, 0.9) == 0          # no ladder at all
    assert arch_pairs(32, 4, 1.0) == 32


# --------------------------------------- the arch_frac 0 trap, said out loud

class _TapeStub:
    """Enough of a Trainer for `tape_slot_complaint`."""

    def __init__(self, arch_frac, names, weights=None, tape=("t1", "t2")):
        from kagg3.es.train import Config
        self.cfg = Config(arch_frac=arch_frac)
        self.archetype_names = list(names)
        self.archetypes = [None] * len(names)
        self.tape_slots = tuple((names.index(t), i)
                                for i, t in enumerate(tape))
        self.tape_act_slots = ()
        self._w = weights

    def weighted_slots(self):
        return self._w


def _complain(stub):
    from kagg3.es.train import Trainer
    return Trainer.tape_slot_complaint(stub)


def test_arch_frac_zero_with_tapes_loaded_is_named_out_loud():
    """flow123-127 ran for hours with their tape rungs loaded, registered and
    listed at startup -- and `--arch-frac 0.0`, so every episode went to the
    self-play pool and the tape verdicts were void. Nothing said so."""
    msg = _complain(_TapeStub(0.0, ["a", "t1", "t2"]))
    assert msg and "--arch-frac 0" in msg and "t1" in msg
    assert "never played" in msg


def test_every_tape_on_weight_zero_is_named_too():
    msg = _complain(_TapeStub(0.5, ["a", "t1", "t2"],
                              weights=np.array([1.0, 0.0, 0.0])))
    assert msg and "--rung-weight" in msg and "t1" in msg


def test_a_configuration_that_does_train_on_tapes_says_nothing():
    assert _complain(_TapeStub(0.5, ["a", "t1", "t2"])) is None
    assert _complain(_TapeStub(0.5, ["a", "t1", "t2"],
                               weights=np.array([1.0, 0.0, 3.0]))) is None
    # No tapes at all is not this warning's business.
    assert _complain(_TapeStub(0.0, ["a", "t1", "t2"], tape=())) is None
