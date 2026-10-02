"""Which seeds a real-engine eval leg is played on.

`scripts/eval_vs_baselines.py` drew ONE seed list and played every opponent on
it, so a leg's noise was the noise of `--games` seeds however many opponents it
named. Measured 2026-09-01: the per-seed paired win difference between two
thetas has an sd of 0.165 across seeds and correlates only weakly across
opponents (r 0.1-0.4), so nine opponents x twelve seeds x two seats -- 216
games -- carried +/-4.8 points of seed noise while sampling twelve seeds. The
same 216 games drawn from a list per opponent sample 108 seeds, at +/-1.6 and
the same wall clock.

`--seed-per-opponent` is that draw, and it is opt-in: the default path has to
stay the one every CSV on disk was written with, because two CSVs are only
paired on `(seed, seat)` when they were drawn the same way.
"""
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.append(os.path.join(ROOT, "scripts"))

import eval_vs_baselines as E


def _legacy(seed_base, games):
    """The draw the script made before the flag existed, spelled out here
    rather than imported: a change to it must fail in this file, not be
    absorbed by it."""
    return list(np.random.default_rng(seed_base).integers(0, 2 ** 31 - 1, games))


def test_the_default_is_the_one_list_it_always_drew():
    """Every opponent on the same seeds, and those seeds the legacy draw --
    which is what makes a CSV written today comparable with one written in
    August."""
    lists = E.seed_lists(20260821, 12, 4, False)
    assert len(lists) == 4
    want = _legacy(20260821, 12)
    assert [list(x) for x in lists] == [want] * 4


def test_the_flag_gives_every_opponent_its_own_seeds():
    """Distinct per opponent -- including the first, which must NOT be handed
    the legacy list: opponent 0 sharing it would leave the leg sampling
    `games` seeds for that opponent and make the flag a half-measure whose
    first column is still the old draw."""
    lists = E.seed_lists(20260825, 12, 9, True)
    assert len(lists) == 9
    seen = [tuple(int(s) for s in x) for x in lists]
    assert len(set(seen)) == 9
    assert list(lists[0]) != _legacy(20260825, 12)
    # And no seed is shared between any two opponents, which is the whole
    # claim: 9 x 12 distinct seeds, not 12 seeds nine times.
    pooled = {int(s) for x in lists for s in x}
    assert len(pooled) == 9 * 12


def test_the_derivation_is_a_stride_off_the_base():
    """Deterministic in `(seed_base, i)` and nothing else, so the same call
    from a resumed segment, a tracker row and a paired analysis draws the same
    games. Opponent `i` is `seed_base + SEED_STRIDE * (i + 1)`."""
    assert E.SEED_STRIDE == 1000003
    lists = E.seed_lists(20260825, 6, 3, True)
    for i, got in enumerate(lists):
        want = np.random.default_rng(20260825 + E.SEED_STRIDE * (i + 1)) \
            .integers(0, 2 ** 31 - 1, 6)
        assert list(got) == list(want)
    # Called twice, the same lists.
    assert [list(x) for x in E.seed_lists(20260825, 6, 3, True)] == \
        [list(x) for x in lists]


def test_the_replicate_pair_of_bases_stays_disjoint():
    """`RealGate` measures the replicate on `--seed-base + 1`. With a stride
    of one that second base's opponent `i - 1` would replay opponent `i`'s
    games, and the replicate would confirm the acceptance on the seeds that
    produced it. A prime stride keeps the two legs' seeds apart."""
    a = {int(s) for x in E.seed_lists(20260825, 12, 9, True) for s in x}
    b = {int(s) for x in E.seed_lists(20260826, 12, 9, True) for s in x}
    assert not (a & b)


@pytest.mark.parametrize("per_opponent", (False, True))
def test_the_jobs_are_the_same_shape_either_way(per_opponent):
    """The flag changes the seeds, not the games: `--games` seeds x 2 seats
    per opponent, in `--opponents` order, is the CSV's shape and the arithmetic
    `read_eval_csv` and `scripts/kagg2_track_row.py` do on it."""
    opponents = ["starter", "random", "pass"]
    lists = E.seed_lists(20260821, 5, len(opponents), per_opponent)
    jobs = [(int(s), o, seat)
            for o, seeds in zip(opponents, lists)
            for s in seeds for seat in (0, 1)]
    assert len(jobs) == 3 * 5 * 2
    assert [o for _, o, _ in jobs[:10]] == ["starter"] * 10
    assert [seat for _, _, seat in jobs[:4]] == [0, 1, 0, 1]
