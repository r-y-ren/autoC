"""`plan.CLIP_CAP_ON`: the shed's 100 units of room, spent dearest-first.

`docs/strategy/2026-09-16-shedclip.md`. `_end_of_day` banks every unit's
inventory into a 100-unit shed and destroys the tail, 17.80 u / 1,415 coins a
board on the shipped pair; the same COUNT of units taken from the cheapest the
seat carried home would cost 277. This switch spends the room on the dear units
by capping the day's admitted HARVEST volume at `CLIP_CAP_ROOM`, dearest unit
price first, and leaving the cheap yield on the tile for tomorrow.

SHIPPED ON 2026-09-17 (PUMPCLIP, `docs/strategy/2026-09-17-stack1.md`).  Set
OFF nothing is traced: pinned below against a pristine `git archive <PRE_SWITCH>
src` tree, whole-plan digests on the five boards `tests/test_slotprio.py` and
`tests/test_lot4.py` pin their own.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np

import kagg3                                     # BEFORE test_budget_order
from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

_WT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if "--digests" not in sys.argv:
    assert kagg3.__file__.startswith(os.path.join(_WT, "src")), kagg3.__file__

from test_budget_order import _macro                              # noqa: E402

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0,
          n_mel=0, mel_yld=0, mel_age=0):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield = z.copy(), z.copy(), z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = spec.I_WHEAT
    t_day[:n_wh] = day - age
    t_yield[:n_wh] = yld
    t_wat[:n_wh] = t_water
    if n_mel:
        s = slice(n_wh, n_wh + n_mel)
        kind[s] = spec.KIND_PLANT
        occ[s] = spec.I_MELON
        t_day[s] = day - (mel_age or age)
        t_yield[s] = mel_yld
        t_wat[s] = t_water
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = shed_wh
    shed[spec.I_TOMATO] = shed_to
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, int(mkt_inv), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


PIN_BOARDS = (
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
    ("town", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("glut", dict(day=20, n_wh=24, yld=6, n_mel=8, mel_yld=6, mel_age=12)),
)


#: The tree this file's OFF pin is taken against: master before PUMPCLIP
#: promoted the cap.  `_pin.SHIPPED` now names a tree where `CLIP_CAP_ON` is
#: TRUE, so it can no longer stand for "the planner without the cap"; a SHA and
#: not a branch name, for the reason `_pin.SHIPPED` is one.
PRE_SWITCH = "c6da7f0"


def _own_digests(on=None):
    """The pin boards' whole-plan digests, with the cap pinned to `on`.

    `None` means "whatever this tree ships", which in the `--digests`
    subprocess is the ARCHIVED tree's own default.  That was OFF at
    `PRE_SWITCH` and ON here between PUMPCLIP and ESR; since ESR it is OFF at
    both, and the asymmetry the pin was written for is gone.  The pin below
    still asks for `False` explicitly, so it keeps its meaning either way."""
    if on is None:
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    was, P.CLIP_CAP_ON = P.CLIP_CAP_ON, on
    try:
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    finally:
        P.CLIP_CAP_ON = was


def _head_digests():
    return _pin.tree_digests(__file__, ref=PRE_SWITCH)


# =========================================================================
# OFF: the shipped program, byte for byte
# =========================================================================

def test_the_cap_does_not_ship_any_more():
    """2026-09-17 PUMPCLIP promoted it `False -> True`; 2026-09-18 ESR put it
    back (`docs/strategy/2026-09-18-stack5.md`: the cap is the single remaining
    negative board of the engine class -- topleg3 109888002, -18,144 -- and
    dropping it makes that class +738 se 118 t +6.26 with ZERO negatives for
    +88 t +1.82 on the pooled 241).  It KEEPS its gene column, per the
    catalogue rule, so the search can take it back without a layout change."""
    assert P.CLIP_CAP_ON is False
    assert P.SWITCH_GENE_DEFAULTS["CLIP_CAP_ON"] is False
    assert "CLIP_CAP_ON" in P.SWITCH_GENES
    assert P.CLIP_CAP_ROOM == spec.SHED_CAPACITY == 100


def test_off_plan_is_byte_identical_to_the_pre_switch_tree():
    """Set OFF, this planner is `PRE_SWITCH` byte for byte: the promotion moved
    the default and nothing else, so every judge read taken with the switch
    hand-flipped still describes this code."""
    assert _own_digests(on=False) == _head_digests()


def test_the_shipped_program_is_the_off_one_and_the_cap_still_moves_a_board():
    """And the guard on the pin above being vacuous: the cap has to bind
    somewhere in the fixture, or OFF-identity is a claim about two no-ops.
    Since ESR the shipped program is the OFF one, so the pin above and this
    line now describe the same planner -- and the ON arm is still a different
    one, which is what keeps the switch (and its gene column) meaningful."""
    assert _own_digests() == _own_digests(on=False)
    assert _own_digests(on=True) != _own_digests(on=False)


# =========================================================================
# ON
# =========================================================================

class _On:
    def __enter__(self):
        self.was = P.CLIP_CAP_ON
        P.CLIP_CAP_ON = True
        return self

    def __exit__(self, *a):
        P.CLIP_CAP_ON = self.was


class _Off:
    """The cap set OFF -- it ships ON since 2026-09-17, so every baseline in
    this section has to name the program it is a baseline FOR."""

    def __enter__(self):
        self.was = P.CLIP_CAP_ON
        P.CLIP_CAP_ON = False
        return self

    def __exit__(self, *a):
        P.CLIP_CAP_ON = self.was


def _harv_tiles(view):
    """The tiles whose chain still carries an OP_HARVEST."""
    pre = P._derive(np, view, _macro(), P.default_price_table(), np.int32(0),
                    np.bool_(False), np.int32(0))
    op = np.asarray(pre.chain_op)
    return np.where((op == O.OP_HARVEST).any(axis=1))[0]


def test_on_leaves_a_day_that_fits_alone():
    """Under the cap the switch is inert: same plan, same digest."""
    v = _view(day=10, n_wh=8, yld=6)                 # 48 units, far under 100
    with _Off():
        off = _digest(_plan(v))
    with _On():
        assert _digest(_plan(v)) == off


def test_on_drops_the_cheap_harvest_and_keeps_the_dear_one():
    """24 wheat x 6 + 8 melon x 6 = 192 units into 100 of room."""
    v = _view(day=20, n_wh=24, yld=6, n_mel=8, mel_yld=6, mel_age=12)
    with _Off():
        base = set(_harv_tiles(v).tolist())
    assert len(base) == 32, base
    with _On():
        kept = set(_harv_tiles(v).tolist())
    mel = set(range(24, 32))
    assert mel <= kept, "the dear crop is never the one suppressed"
    assert kept < base, "the cheap crop's harvests are"
    # Volume: the cap is a floor on the carry (the straddling tile is kept),
    # so the banked volume -- yield plus the unit an in-window watering adds,
    # which is what the cap counts -- is inside [room, room + one tile].
    vol = int((np.asarray(v.t_yield)[sorted(kept)] + 1).sum())
    assert P.CLIP_CAP_ROOM <= vol <= P.CLIP_CAP_ROOM + 7, vol


def test_on_suppresses_the_chain_op_not_only_its_value():
    """A suppressed tile must not be admitted for a harvest it will not take."""
    v = _view(day=20, n_wh=24, yld=6, n_mel=8, mel_yld=6, mel_age=12)
    with _On():
        pre = P._derive(np, v, _macro(), P.default_price_table(), np.int32(0),
                        np.bool_(False), np.int32(0))
        op = np.asarray(pre.chain_op)
        val = np.asarray(pre.tile_value)
        sup = [t for t in range(24) if not (op[t] == O.OP_HARVEST).any()]
        assert sup, "some wheat harvest is suppressed"
        for t in sup:
            # no HARVEST op, and the harvest's coins are out of the tile value
            assert not (op[t] == O.OP_HARVEST).any()
            assert val[t] < 6 * int(BASE_PRICE[spec.I_WHEAT])


def test_on_traces_under_jit():
    import jax
    import jax.numpy as jnp
    v = _view(day=20, n_wh=24, yld=6, n_mel=8, mel_yld=6, mel_age=12)
    jv = P.DayView(*[jnp.asarray(a) for a in v])
    jm = type(_macro())(*[jnp.asarray(a) for a in _macro()])
    with _On():
        f = jax.jit(lambda w: P.build_day(jnp, w, jm))
        got = tuple(np.asarray(a) for a in f(jv))
        assert _digest(got) == _digest(_plan(v))   # jit == numpy, ON


if __name__ == "__main__":                      # the master-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
