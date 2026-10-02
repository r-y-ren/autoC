"""`plan.SELL_SLOT_RIVALRANK_ON`: the rival's MEASURED single-turn burst
re-ranks our SELL row.

`docs/strategy/2026-09-16-rivaltell-arm.md` sect.5 item 3 -- the tell is exact
and its per-turn MEAN died inside `sell_slot_scores`' batch clamp, so the thing
to read is a BURST and the thing to feed is the RANK, not the batch. The batch
term is untouched here; this adds one term to the key `sell_slot_perm` sorts.

The switch defaults OFF, so the shipped program is unchanged: the whole-plan
digest pin below is against a pristine `git archive master src` tree.
`docs/strategy/2026-09-16-rivalrank.md`.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, sys.argv[sys.argv.index("--digests") + 1]
                if "--digests" in sys.argv else "src")

import numpy as np

import kagg3
from kagg3 import spec
from kagg3.core import plan as P

# `kagg3` FIRST and only then the test helpers, which do their own
# `sys.path.insert(0, "src")` -- imported earlier they would load THIS tree's
# planner into the `--digests` subprocess and the pin would compare the tree
# with itself (`tests/test_lot4.py`, 2026-09-16).
import test_slotprio as SP                                     # noqa: E402

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

#: The tree the switch is OFF-identical to: master at the branch point, i.e.
#: the uploaded `lot4t17` + `SELL_SLOT_PRIORITY` pair with `SELL_SLOT_MIRROR`
#: beside it. A SHA and not `master`, so the pin keeps its meaning later.
MASTER = "b86b4c411d9255f75f6017609dc8c61525f43222"


def _digests():
    return SP._digests()


def _tree_digests(ref):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {ref} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


# =========================================================================
# OFF: the shipped program, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.SELL_SLOT_RIVALRANK_ON is False
    assert P.RIVAL_TELL_ON is False
    assert P.SELL_SLOT_MIRROR_ON is False
    assert P.SELL_SLOT_PRIORITY_ON is True          # what it modifies


def test_off_plan_is_byte_identical_to_master():
    """THE IDENTITY PIN: the whole plan tuple, hashed, on five boards x two
    reservations, against a pristine `git archive MASTER src` tree."""
    assert _digests() == _tree_digests(MASTER)


def test_the_master_pin_is_the_shipped_pair():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {MASTER}:src/kagg3/core/plan.py", shell=True,
                         cwd=root, capture_output=True, text=True, check=True).stdout
    assert "\nSELL_SLOT_PRIORITY_ON = True\n" in src
    assert "\nLOT4_ON = True\n" in src and "\nLOT4_TURN = 17\n" in src
    assert "SELL_SLOT_RIVALRANK_ON" not in src


def test_the_view_default_is_an_empty_measurement():
    assert np.array_equal(P._NO_BURST, np.zeros(spec.N_PRODUCTS, np.int32))
    assert np.array_equal(P.DayView(day=0, kind=0, occ=0, t_day=0, t_water=0,
                                    t_cons=0, t_yield=0, t_fert=0, t_cared=0,
                                    t_favail=0, shed=0, seeds=0, money=0,
                                    nquad=0, price=0, mkt_inv=0, shops=0
                                    ).opp_burst, P._NO_BURST)


# =========================================================================
# the term itself
# =========================================================================
PT = None


def _pt():
    global PT
    if PT is None:
        PT = np.asarray(P.default_price_table())
    return PT


def _row(q, inv):
    return (np.asarray(q, np.int32)[None, :], np.asarray(inv, np.int32)[None, :])


def test_a_zero_burst_is_the_identity():
    """No measurement anywhere -- the default view -- returns `score` itself,
    which is why an OFF view costs nothing even when the switch is on."""
    lots, inv = _row([5, 0, 3, 0, 0, 0, 0, 2, 0], [20] * 9)
    score = np.arange(spec.N_PRODUCTS, dtype=np.int32)[None, :] * 7
    out = P.sell_slot_rivalrank(np, _pt(), inv, lots,
                                np.zeros(spec.N_PRODUCTS, np.int32), score)
    assert np.array_equal(out, score)


def test_the_term_is_the_same_walk_as_the_proxy_with_the_measured_batch():
    """`sell_slot_rivalrank`'s correction at burst `b` equals
    `sell_slot_scores`' own read when the proxy batch is forced to `b` -- the
    two are the same SAME-ITEM price delta, one guessed and one measured."""
    lots, inv = _row([6, 0, 4, 0, 0, 0, 0, 0, 0], [13] * 9)
    burst = np.array([11, 0, 11, 0, 0, 0, 0, 0, 0], np.int32)
    zero = np.zeros((1, spec.N_PRODUCTS), np.int32)
    got = P.sell_slot_rivalrank(np, _pt(), inv, lots, burst, zero)
    lo, hi = P.SELL_SLOT_PRIORITY_BATCH_MIN, P.SELL_SLOT_PRIORITY_BATCH_MAX
    try:
        P.SELL_SLOT_PRIORITY_BATCH_MIN = P.SELL_SLOT_PRIORITY_BATCH_MAX = 11
        want = P.sell_slot_scores(np, _pt(), inv, lots,
                                  np.full(spec.N_PRODUCTS, 11, np.int32))
    finally:
        P.SELL_SLOT_PRIORITY_BATCH_MIN, P.SELL_SLOT_PRIORITY_BATCH_MAX = lo, hi
    assert np.array_equal(got, want)


def _sign(s, w=1):
    class _C:
        def __enter__(self):
            self.o = (P.SELL_SLOT_RIVALRANK_SIGN, P.SELL_SLOT_RIVALRANK_W)
            P.SELL_SLOT_RIVALRANK_SIGN, P.SELL_SLOT_RIVALRANK_W = s, w

        def __exit__(self, *a):
            P.SELL_SLOT_RIVALRANK_SIGN, P.SELL_SLOT_RIVALRANK_W = self.o
    return _C()


def test_the_sign_moves_a_fired_item_both_ways():
    """Two live products the proxy scores level; the rival is measurably
    dumping the second. `+1` puts it first, `-1` puts it last."""
    a, b = 0, 2
    q = np.zeros(spec.N_PRODUCTS, np.int32)
    q[a] = q[b] = 8
    lots, inv = _row(q, [15] * 9)
    score = np.zeros((1, spec.N_PRODUCTS), np.int32)
    burst = np.zeros(spec.N_PRODUCTS, np.int32)
    burst[b] = 12
    with _sign(+1):
        up = P.sell_slot_perm(np, lots[0],
                              P.sell_slot_rivalrank(np, _pt(), inv, lots,
                                                    burst, score)[0])
    with _sign(-1):
        dn = P.sell_slot_perm(np, lots[0],
                              P.sell_slot_rivalrank(np, _pt(), inv, lots,
                                                    burst, score)[0])
    assert int(up[0]) == b and int(up[1]) == a
    assert int(dn[0]) == a and int(dn[1]) == b


def test_every_live_slot_keeps_a_non_negative_key():
    """The `-1` sign subtracts, so the row is shifted: live slots stay at or
    above zero and therefore stay ahead of `sell_slot_perm`'s empty slots,
    whose keys are negative by construction."""
    q = np.array([9, 0, 7, 0, 4, 0, 0, 0, 0], np.int32)
    lots, inv = _row(q, [11] * 9)
    burst = np.array([20, 0, 3, 0, 0, 0, 0, 0, 0], np.int32)
    score = np.zeros((1, spec.N_PRODUCTS), np.int32)
    with _sign(-1, 4):
        out = P.sell_slot_rivalrank(np, _pt(), inv, lots, burst, score)[0]
        perm = P.sell_slot_perm(np, lots[0], out)
    assert (out[q > 0] >= 0).all()
    assert set(int(x) for x in perm[:3]) == {0, 2, 4}


def test_a_uniform_shift_does_not_re_order_the_row():
    """The non-negative shift is per row and uniform, so it is invisible to
    `sell_slot_perm` -- the only thing the switch may change is the order."""
    q = np.array([9, 0, 7, 0, 4, 0, 0, 0, 0], np.int32)
    lots, inv = _row(q, [11] * 9)
    burst = np.array([20, 0, 3, 0, 5, 0, 0, 0, 0], np.int32)
    score = np.array([[40, 0, 90, 0, 10, 0, 0, 0, 0]], np.int32)
    with _sign(-1, 4):
        key = P.sell_slot_rivalrank(np, _pt(), inv, lots, burst, score)[0]
    assert np.array_equal(P.sell_slot_perm(np, lots[0], key),
                          P.sell_slot_perm(np, lots[0],
                                           (key + 1000).astype(np.int32)))


def test_jit_equals_numpy():
    import jax
    import jax.numpy as jnp
    q = np.array([9, 0, 7, 0, 4, 0, 0, 3, 0], np.int32)
    lots, inv = _row(q, [11, 4, 30, 7, 19, 2, 8, 25, 1])
    burst = np.array([20, 0, 3, 0, 5, 0, 0, 24, 0], np.int32)
    score = np.array([[40, 0, 90, 0, 10, 0, 0, 55, 0]], np.int32)
    for s, w in ((1, 1), (-1, 1), (-1, 4), (1, 4)):
        with _sign(s, w):
            ref = P.sell_slot_rivalrank(np, _pt(), inv, lots, burst, score)
            f = jax.jit(lambda pt, i, l, b, sc:
                        P.sell_slot_rivalrank(jnp, pt, i, l, b, sc))
            got = np.asarray(f(jnp.asarray(_pt()), jnp.asarray(inv),
                               jnp.asarray(lots), jnp.asarray(burst),
                               jnp.asarray(score)))
        assert np.array_equal(ref, got), (s, w)


# =========================================================================
# the tell's burst read
# =========================================================================

def test_burst_is_the_window_maximum_not_the_mean():
    """The quantity `rivaltell-arm` sect.5 asked for: 30 units on one turn of
    six is a burst of 30, while `batch()` calls it a rate of 5 and the clamp
    swallows it."""
    from kagg3.agent import tell as T
    t = T.RivalTell()
    t.units[:] = 0
    t.sold[:] = False
    t.units[0, spec.I_MILK] = 30
    t.sold[0, spec.I_MILK] = True
    t.n = t.window
    b = t.burst()
    assert int(b[spec.I_MILK]) == 30
    assert int(t.batch()[spec.I_MILK]) == P.RIVAL_TELL_MIN_TURNS * 0 - 1  # NO_RATE


def test_burst_is_zero_before_a_full_window_and_on_the_skipped_items():
    from kagg3.agent import tell as T
    t = T.RivalTell()
    t.units[0, spec.I_MILK] = 9
    t.sold[0, spec.I_MILK] = True
    t.n = 1
    assert not t.burst().any()                      # short window
    t.n = t.window
    t.units[1, spec.I_WHEAT] = 40
    t.sold[1, spec.I_WHEAT] = True
    b = t.burst()
    assert int(b[spec.I_MILK]) == 9
    assert int(b[spec.I_WHEAT]) == 0                # RIVAL_TELL_SKIP


def test_the_switch_is_inert_without_slot_priority(monkeypatch):
    """The correction is a term of `SELL_SLOT_PRIORITY`'s key; it is not read
    at all when that switch is off."""
    v = SP._view(day=10, n_wh=8, shed_wh=50, shed_to=45)
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", False)
    base = SP._digest(SP._plan(v, SP._sell_macro()))
    monkeypatch.setattr(P, "SELL_SLOT_RIVALRANK_ON", True)
    assert SP._digest(SP._plan(v, SP._sell_macro())) == base


def test_an_armed_seat_with_no_measurement_is_the_slotprio_plan():
    """The sentinel view -- days 0-1, a gap, a rival that sold nothing -- plans
    exactly `SELL_SLOT_PRIORITY`'s row, so the arm only differs where the tell
    actually fires."""
    base = _digests()
    try:
        P.SELL_SLOT_RIVALRANK_ON = True
        assert _digests() == base
    finally:
        P.SELL_SLOT_RIVALRANK_ON = False


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _digests().items():
        print(_n, _d)
