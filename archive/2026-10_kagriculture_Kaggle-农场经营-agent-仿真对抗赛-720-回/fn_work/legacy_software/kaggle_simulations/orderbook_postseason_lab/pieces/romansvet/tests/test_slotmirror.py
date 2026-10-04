"""`plan.SELL_SLOT_MIRROR_ON` / `SELL_SLOT_MIRROR_GATE_ON`: the rival's row is
our own row.

`docs/strategy/2026-09-16-nbintel2.md` sect.4 / sect.6 items 1-2. The shipped
`SELL_SLOT_PRIORITY` ranks a SELL row by a proxy for contention whose batch
window measured flat (`2026-09-16-slotprio.md` sect.5); this replaces the
ranking with an EXACT lockstep replay (`sim/market.py`'s transcription of
`_process_market` / `_commit_unit`) against a mirror of our own row, and gates
the reorder on the rival board actually looking like the model.

Both switches default OFF, so the shipped program is unchanged: the whole-plan
digest pin below is against a pristine `git archive master src` tree.
`docs/strategy/2026-09-16-slotmirror.md`.
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
from kagg3.sim import market

# `kagg3` FIRST and only then the test helpers, which do their own
# `sys.path.insert(0, "src")` -- imported earlier they would load THIS tree's
# planner into the `--digests` subprocess and the pin would compare the tree
# with itself (`tests/test_lot4.py`, 2026-09-16).
import test_slotprio as SP                                     # noqa: E402

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

#: The tree both switches are OFF-identical to: master at the branch point,
#: i.e. the uploaded `lot4t17` + `SELL_SLOT_PRIORITY` pair. A SHA and not
#: `master`, so the pin keeps its meaning after this branch lands.
MASTER = "4054968b69360f40fc283de677b546f8bdb54459"


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
    assert P.SELL_SLOT_MIRROR_ON is False
    assert P.SELL_SLOT_MIRROR_GATE_ON is False
    assert P.SELL_SLOT_PRIORITY_ON is True          # what they modify


def test_off_plan_is_byte_identical_to_master():
    """THE IDENTITY PIN: the whole plan tuple, hashed, on five boards, against
    a pristine `git archive MASTER src` tree. Equal means this branch adds two
    switches and no behaviour."""
    assert _digests() == _tree_digests(MASTER)


def test_the_master_pin_is_the_shipped_pair():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {MASTER}:src/kagg3/core/plan.py", shell=True,
                         cwd=root, capture_output=True, text=True, check=True).stdout
    assert "\nSELL_SLOT_PRIORITY_ON = True\n" in src
    assert "\nLOT4_ON = True\n" in src and "\nLOT4_TURN = 17\n" in src
    assert "SELL_SLOT_MIRROR_ON" not in src


def _stocked(**kw):
    """A pin board with four products on the shelf -- the five pin boards hold
    two, and a two-product row's best permutation is often the identity."""
    v = SP._view(day=10, n_wh=8, shed_wh=50, shed_to=45, **kw)
    shed = np.asarray(v.shed).copy()
    shed[spec.I_STRAWBERRY], shed[spec.I_MELON] = 30, 12
    shed[spec.I_EGG], shed[spec.I_MILK] = 26, 18
    return v._replace(shed=shed)


def test_on_actually_moves_a_row(monkeypatch):
    """The other end of the pin: the arm is not a no-op."""
    v = _stocked()
    before = SP._digest(SP._plan(v, SP._sell_macro()))
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_ON", True)
    on = SP._plan(v, SP._sell_macro())
    assert SP._digest(on) != before
    # and not one unit of volume moved
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_ON", False)
    ro, rn = SP._rows(SP._plan(v, SP._sell_macro())), SP._rows(on)
    assert set(ro) == set(rn)
    for t in ro:
        assert sorted(ro[t]) == sorted(rn[t]), t
    assert any(ro[t] != rn[t] for t in ro)


# =========================================================================
# the replay is the engine's
# =========================================================================

def _rev(inv, q, item, mode):
    """`sim/market.sell_walk` on one order, the engine's own walk."""
    tables = type("T", (), {"price": P.default_price_table()})
    _k, rev, adv = market.sell_walk(np, tables, np.int32(item), np.int32(inv),
                                    np.int32(q), np.int32(mode))
    return int(rev), int(adv)


def test_the_three_columns_are_the_engines_own_walks():
    pt = P.default_price_table()
    inv0 = int(spec.MARKET_I0)
    for item, q, off in ((spec.I_WHEAT, 40, 0), (spec.I_MELON, 3, -200),
                         (spec.I_STRAWBERRY, 12, 900)):
        lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
        lots[0, item] = q
        inv = np.full((1, spec.N_PRODUCTS), inv0 + off, np.int32)
        rev = P.sell_slot_mirror_revenues(np, pt, inv, lots)[0, item]
        solo, adv = _rev(inv0 + off, q, item, market.M_SELL_SOLO)
        pair, _ = _rev(inv0 + off, q, item, market.M_SELL_PAIR)
        late, _ = _rev(inv0 + off + adv, q, item, market.M_SELL_SOLO)
        assert (int(rev[0]), int(rev[1]), int(rev[2])) == (solo, pair, late)
        # and the order is the physical one: early >= coupled >= late
        assert rev[0] >= rev[1] >= rev[2]


def test_a_product_with_no_units_scores_nothing():
    pt = P.default_price_table()
    inv = np.full((1, spec.N_PRODUCTS), int(spec.MARKET_I0), np.int32)
    lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
    lots[0, spec.I_WHEAT] = 5
    rev = P.sell_slot_mirror_revenues(np, pt, inv, lots)[0]
    assert not rev[spec.I_MELON].any()


# =========================================================================
# the search
# =========================================================================

def _pos(lots_row):
    live = lots_row > 0
    lv = live.astype(np.int32)
    out = np.where(live, np.cumsum(lv) - lv,
                   lv.sum() + np.cumsum(1 - lv) - (1 - lv)).astype(np.int32)
    return out


def _rows(seed, n=120):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
        k = int(rng.integers(2, 7))
        lots[0, rng.choice(spec.N_PRODUCTS, k, replace=False)] = rng.integers(1, 40, k)
        inv = (np.full((1, spec.N_PRODUCTS), int(spec.MARKET_I0), np.int32)
               + rng.integers(-300, 300, spec.N_PRODUCTS)).astype(np.int32)
        yield inv, lots


def test_the_climb_never_scores_below_the_row_we_ship():
    """Strict improvement only, so the identity permutation -- every product
    coupled with its own clone -- is a floor, not a starting guess."""
    pt = P.default_price_table()
    for inv, lots in _rows(11):
        rev = P.sell_slot_mirror_revenues(np, pt, inv, lots)[0]
        th = _pos(lots[0])
        ours = 8 - np.asarray(P.sell_slot_mirror_scores(np, pt, inv, lots)[0])
        assert int(P._mirror_total(np, rev, th, ours)) \
            >= int(P._mirror_total(np, rev, th, th))


def test_the_climb_is_within_a_coin_or_two_of_the_exact_optimum():
    """Brute force over every permutation of the live block: the bounded
    2-swap climb is not merely an improvement, it is essentially the answer."""
    import itertools
    pt = P.default_price_table()
    gap = 0
    for inv, lots in _rows(5, 40):
        rev = P.sell_slot_mirror_revenues(np, pt, inv, lots)[0]
        th = _pos(lots[0])
        live = np.flatnonzero(lots[0] > 0)
        best = max(int(P._mirror_total(np, rev, th, _o(th, live, pm)))
                   for pm in itertools.permutations(range(len(live))))
        ours = 8 - np.asarray(P.sell_slot_mirror_scores(np, pt, inv, lots)[0])
        gap = max(gap, best - int(P._mirror_total(np, rev, th, ours)))
    assert gap <= 25, gap


def _o(th, live, pm):
    o = th.copy()
    o[live] = np.asarray(pm, np.int32)
    return o


def test_the_perm_keeps_the_live_block_and_every_unit():
    pt = P.default_price_table()
    for inv, lots in _rows(2, 40):
        sc = P.sell_slot_mirror_scores(np, pt, inv, lots)
        perm = np.asarray(P.sell_slot_perm(np, lots[0], sc[0]))
        assert sorted(perm.tolist()) == list(range(spec.N_PRODUCTS))
        n_live = int((lots[0] > 0).sum())
        assert (lots[0][perm][:n_live] > 0).all()
        assert sorted(lots[0][perm].tolist()) == sorted(lots[0].tolist())


def test_jit_is_numpy():
    import jax
    import jax.numpy as jnp
    pt = P.default_price_table()
    inv, lots = next(_rows(9, 1))
    lots = np.repeat(lots, 3, axis=0)
    inv = np.repeat(inv, 3, axis=0)
    f = jax.jit(lambda i, l: P.sell_slot_mirror_scores(jnp, jnp.asarray(pt), i, l))
    assert (np.asarray(f(jnp.asarray(inv), jnp.asarray(lots)))
            == P.sell_slot_mirror_scores(np, pt, inv, lots)).all()
    g = jax.jit(lambda lo, r, m, om: P.sell_slot_gate(jnp, lo, r, m, om))
    args = (jnp.asarray(lots), jnp.zeros(spec.N_PRODUCTS, jnp.int32),
            jnp.int32(0), jnp.int32(0))
    assert bool(g(*args)) is bool(P.sell_slot_gate(
        np, lots, np.zeros(spec.N_PRODUCTS, np.int32), np.int32(0), np.int32(0)))


# =========================================================================
# the gate
# =========================================================================

def _gate(ours, theirs, money=0, opp=0):
    lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
    lots[0] = ours
    return bool(P.sell_slot_gate(np, lots, np.asarray(theirs, np.int32),
                                 np.int32(money), np.int32(opp)))


def test_gate_is_the_histogram_intersection_and_the_lead():
    same = np.zeros(spec.N_PRODUCTS, np.int32)
    same[spec.I_WHEAT], same[spec.I_TOMATO] = 20, 20
    assert _gate(same, same)                       # a perfect clone fires
    assert _gate(same, same * 3)                   # scale-free
    other = np.zeros(spec.N_PRODUCTS, np.int32)
    other[spec.I_MELON] = 40
    assert not _gate(same, other)                  # disjoint mix does not
    assert not _gate(same, np.zeros(spec.N_PRODUCTS, np.int32))   # empty farm
    assert not _gate(np.zeros(spec.N_PRODUCTS, np.int32), same)   # empty row
    half = np.zeros(spec.N_PRODUCTS, np.int32)
    half[spec.I_WHEAT], half[spec.I_MELON] = 20, 20
    assert _gate(same, half) == (P.SELL_SLOT_MIRROR_GATE_SIM_PCT <= 50)
    # the lead veto
    assert _gate(same, same, money=P.SELL_SLOT_MIRROR_GATE_LEAD - 1, opp=0)
    assert not _gate(same, same, money=P.SELL_SLOT_MIRROR_GATE_LEAD, opp=0)
    assert _gate(same, same, money=10 ** 6, opp=10 ** 6)


def test_a_vetoed_day_is_the_off_plan(monkeypatch):
    """The gate's veto is `prio = 0`, which is `sell_slot_perm`'s identity --
    the row is the one the pre-`SELL_SLOT_PRIORITY` planner emitted, live
    products in product order (identical after the `MO_NONE` compaction the
    engine's own reader does)."""
    ripe = np.zeros(spec.N_PRODUCTS, np.int32)
    ripe[spec.I_MELON] = 40                       # nothing like our row
    v = _stocked(opp_ripe=ripe)
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", False)
    off = SP._rows(SP._plan(v, SP._sell_macro()))
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", True)
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_ON", True)
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_GATE_ON", True)
    gated = SP._rows(SP._plan(v, SP._sell_macro()))
    for t in off:
        if all(o == 0 for o, _a, _q in off[t]):   # a pure SELL row
            assert [(a, q) for _o, a, q in off[t]] == \
                   [(a, q) for _o, a, q in gated[t]], t


def test_gate_off_never_reads_the_rival_purse(monkeypatch):
    """`opp_money` is supplied by the view builders only when the gate is on,
    so an ungated rollout traces the graph it always traced."""
    assert int(np.asarray(SP._view().opp_money)) == 0
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_ON", True)
    SP._plan(SP._view(), SP._sell_macro())        # no opp_money on the view


def test_both_view_builders_carry_the_purse_when_the_gate_is_on(monkeypatch):
    from kagg3.agent import parse
    obs = {"day": 3, "farms": [{"money": 111}, {"money": 222}]}
    assert int(parse.parse_opp_money(obs, 0)) == 222
    assert int(parse.parse_opp_money(obs, 1)) == 111
    assert int(parse.parse_opp_money({"farms": []}, 0)) == 0
    import inspect

    from kagg3.sim import rollout
    src = inspect.getsource(rollout.day_view)
    assert "opp_money" in src and "SELL_SLOT_MIRROR_GATE_ON" in src


def test_the_switch_is_inert_without_slot_priority(monkeypatch):
    """Both new switches modify `SELL_SLOT_PRIORITY`'s ordering; neither is
    read when that switch is off."""
    v = SP._view(day=10, n_wh=8, shed_wh=50, shed_to=45)
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", False)
    base = SP._digest(SP._plan(v, SP._sell_macro()))
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_ON", True)
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_GATE_ON", True)
    assert SP._digest(SP._plan(v, SP._sell_macro())) == base


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _digests().items():
        print(_n, _d)
