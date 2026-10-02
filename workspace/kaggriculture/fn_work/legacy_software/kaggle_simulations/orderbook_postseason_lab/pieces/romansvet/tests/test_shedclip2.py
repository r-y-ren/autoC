"""SHEDCLIP2: the three refinements `CLIP_CAP_ON` left open.

`docs/strategy/2026-09-16-shedclip2.md`, and §6 of the SHEDCLIP doc:

  (a) `CLIP_CAP_TERMINAL_OFF` -- the whole cap stands down on day 29, where
      there is no `_end_of_day` and a suppressed harvest is a harvest the
      liquidation never sells.
  (b) `CLIP_FERT_SKIP_ON`     -- on a night the haul overflows, the 26-coin
      COLLECT_FERT ops are dropped (op and value) instead of charged to the
      room, so the harvest competes for all 100 units.
  (c) `CLIP_CAP_STRICT_ON`    -- the straddling tile is suppressed too: a
      ceiling on the carry instead of a floor.

All three are inert without `CLIP_CAP_ON` (which itself ships ON since
2026-09-17) and all three are OFF by default, so
the shipped plan is byte-identical -- pinned below against a pristine
`git archive master src` tree.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, sys.argv[sys.argv.index("--digests") + 1]
                if "--digests" in sys.argv else "src")

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
SWITCHES = ("CLIP_CAP_TERMINAL_OFF", "CLIP_FERT_SKIP_ON", "CLIP_CAP_STRICT_ON")


def _view(day=20, money=20_000, n_wh=24, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0,
          n_mel=8, mel_yld=6, mel_age=12, n_anim=0, favail=0, a_yield=0):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield, t_fav = z.copy(), z.copy(), z.copy(), z.copy()
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
    if n_anim:                       # geese: KIND_COOP, animal index 0
        s = slice(n_wh + n_mel, n_wh + n_mel + n_anim)
        kind[s] = spec.KIND_COOP
        occ[s] = 0
        t_day[s] = day - 6
        t_yield[s] = a_yield
        t_fav[s] = favail
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = shed_wh
    shed[spec.I_TOMATO] = shed_to
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=t_fav, shed=shed,
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
    ("hot", dict(day=10, n_wh=8, n_mel=0, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, n_mel=0)),
    ("wet", dict(day=10, n_wh=8, n_mel=0, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, n_mel=0, shed_wh=60, shed_to=38)),
    ("glut", dict(day=20, n_wh=24, yld=6, n_mel=8, mel_yld=6, mel_age=12)),
    ("barn", dict(day=20, n_wh=24, yld=6, n_mel=8, mel_yld=6, mel_age=12,
                  n_anim=20, favail=1, a_yield=3)),
    ("last", dict(day=29, n_wh=24, yld=6, n_mel=8, mel_yld=6, mel_age=12)),
)


#: The tree this file's pin is taken against: master before PUMPCLIP promoted
#: `CLIP_CAP_ON`.  A SHA and not `master`, which is self-referential the moment
#: this branch merges, and which since 2026-09-17 would name a tree whose cap is
#: ON -- the three refinements below are only meaningful against a tree without
#: it.
PRE_SWITCH = "c6da7f0"


#: Every switch that shipped ON after `PRE_SWITCH` and that this file's boards
#: can feel, set to what the reference tree has. The cap itself is the subject;
#: `ENDROUTE2_ON` / `ENDROUTE2_SPLIT_ON` shipped with PES on 2026-09-18 and do
#: not exist at `c6da7f0` at all, so without them the pin would be reading
#: three switches and calling the answer the cap's.
#: `ENDROUTE_ROW2_ON` joined them with ESR on 2026-09-18 for the same reason.
_PRE_SWITCH_VALUES = dict(CLIP_CAP_ON=False, ENDROUTE2_ON=False,
                          ENDROUTE2_SPLIT_ON=False, ENDROUTE_ROW2_ON=False)


def _own_digests():
    """The pin boards with the CAP ITSELF set off -- the reference tree has no
    cap, and this one ships with one, so the pin names the refinements."""
    was = {k: getattr(P, k, None) for k in _PRE_SWITCH_VALUES}
    for k, v in _PRE_SWITCH_VALUES.items():
        setattr(P, k, v)
    try:
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    finally:
        for k, v in was.items():
            setattr(P, k, v)


def _head_digests():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {PRE_SWITCH} src | tar -x -C {td}", shell=True,
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
    """The three refinements are still OFF, and since ESR (2026-09-18) so is
    the CAP they ride on: PUMPCLIP shipped it on 09-17 and STACK5 took it back
    on the engine-class read, so this whole family is inert in the shipped
    program again and `test_inert_without_the_cap` below is now a statement
    about what ships."""
    for n in SWITCHES:
        assert getattr(P, n) is False, n
    assert P.CLIP_CAP_ON is False


def test_off_plan_is_byte_identical_to_the_pre_switch_tree():
    assert _own_digests() == _head_digests()


def test_inert_without_the_cap():
    """All three ride on `CLIP_CAP_ON`; alone none of them traces.

    The cap ships ON since 2026-09-17, so "without the cap" is now a thing the
    test has to say out loud rather than a default it can lean on."""
    v = _view(n_anim=20, favail=1, a_yield=3)
    with _On(CLIP_CAP_ON=False):
        off = _digest(_plan(v))
        for n in SWITCHES:
            with _On(**{n: True}):
                assert P.CLIP_CAP_ON is False
                assert _digest(_plan(v)) == off, n


# =========================================================================
# ON
# =========================================================================

class _On:
    """Set plan switches for the block, restore whatever was there."""

    def __init__(self, **kw):
        self.kw = kw

    def __enter__(self):
        self.old = {k: getattr(P, k) for k in self.kw}
        for k, v in self.kw.items():
            setattr(P, k, v)
        return self

    def __exit__(self, *a):
        for k, v in self.old.items():
            setattr(P, k, v)


def _pre(view, terminal=False):
    return P._derive(np, view, _macro(), P.default_price_table(), np.int32(0),
                     np.bool_(terminal), np.int32(0))


def _ops(view, op, terminal=False):
    """Tiles whose packed chain carries `op`."""
    o = np.asarray(_pre(view, terminal).chain_op)
    return set(np.where((o == op).any(axis=1))[0].tolist())


def _harv(view, terminal=False):
    return _ops(view, O.OP_HARVEST, terminal)


# ---- (a) the terminal day ------------------------------------------------

def test_cap_binds_on_the_terminal_day():
    """The premise: as shipped the cap suppresses harvests on day 29 too."""
    v = _view(day=29)
    with _On(CLIP_CAP_ON=True):
        assert len(_harv(v, terminal=True)) < 32


def test_terminal_off_restores_the_whole_day_29_harvest():
    v = _view(day=29)
    with _On(CLIP_CAP_ON=True):
        base = _harv(v, terminal=True)
        with _On(CLIP_CAP_TERMINAL_OFF=True):
            free = _harv(v, terminal=True)
    assert base < free, (len(base), len(free))
    assert len(free) == 32, "day 29 harvests every ripe tile again"


def test_terminal_off_leaves_the_ordinary_day_alone():
    v = _view(day=20)
    with _On(CLIP_CAP_ON=True):
        base = _digest(_plan(v))
        with _On(CLIP_CAP_TERMINAL_OFF=True):
            assert _digest(_plan(v)) == base


# ---- (b) drop the collections -------------------------------------------

def test_fert_skip_drops_the_collections_on_a_clipping_night():
    """20 geese hold a fertilizer each; 192 units of harvest overflow the room."""
    v = _view(n_anim=20, favail=1, a_yield=0)
    with _On(CLIP_CAP_ON=True):
        col = _ops(v, O.OP_COLLECT_FERT)
        assert len(col) == 20, col
        base_h = _harv(v)
        with _On(CLIP_FERT_SKIP_ON=True):
            assert _ops(v, O.OP_COLLECT_FERT) == set()
            arm_h = _harv(v)
    # The 20 units of room the collections were charged go to the harvest.
    assert len(arm_h) > len(base_h), (len(base_h), len(arm_h))


def test_fert_skip_takes_the_value_with_the_op():
    """A tile must not be admitted for a collection it will not make."""
    v = _view(n_anim=20, favail=1, a_yield=0)
    with _On(CLIP_CAP_ON=True):
        base = np.asarray(_pre(v).tile_value)
        with _On(CLIP_FERT_SKIP_ON=True):
            arm = np.asarray(_pre(v).tile_value)
    # The collection's coins leave the tile with its op; the feed/care value
    # the same tile also carries stays put.
    d = (base - arm)[32:52]
    assert (d == BASE_PRICE[spec.I_FERT]).all(), d


def test_fert_skip_leaves_a_night_that_fits_alone():
    """Under the room the collections are kept and charged as before."""
    v = _view(n_wh=8, n_mel=0, yld=6, n_anim=10, favail=1)   # 48 u + 10
    with _On(CLIP_CAP_ON=True):
        base = _digest(_plan(v))
        assert len(_ops(v, O.OP_COLLECT_FERT)) == 10
        with _On(CLIP_FERT_SKIP_ON=True):
            assert _digest(_plan(v)) == base


# ---- (c) the straddling tile --------------------------------------------

def _volume(view, kept):
    return int((np.asarray(view.t_yield)[sorted(kept)] + 1).sum())


def test_strict_cuts_the_straddling_tile():
    v = _view()
    with _On(CLIP_CAP_ON=True):
        floor = _harv(v)
        with _On(CLIP_CAP_STRICT_ON=True):
            ceil = _harv(v)
    assert ceil < floor, (len(floor), len(ceil))
    assert _volume(v, floor) >= P.CLIP_CAP_ROOM      # a floor on the carry
    assert _volume(v, ceil) <= P.CLIP_CAP_ROOM       # a ceiling on it


def test_strict_never_suppresses_the_dear_crop():
    v = _view()
    with _On(CLIP_CAP_ON=True, CLIP_CAP_STRICT_ON=True):
        kept = _harv(v)
    assert set(range(24, 32)) <= kept


# ---- jit parity ----------------------------------------------------------

def _jit_eq(view, **kw):
    import jax
    import jax.numpy as jnp
    jv = P.DayView(*[jnp.asarray(a) for a in view])
    jm = type(_macro())(*[jnp.asarray(a) for a in _macro()])
    with _On(CLIP_CAP_ON=True, **kw):
        f = jax.jit(lambda w: P.build_day(jnp, w, jm))
        got = tuple(np.asarray(a) for a in f(jv))
        assert _digest(got) == _digest(_plan(view)), kw


def test_jit_equals_numpy_on_every_arm():
    v = _view(n_anim=20, favail=1, a_yield=3)
    _jit_eq(v)
    for n in SWITCHES:
        _jit_eq(v, **{n: True})
    _jit_eq(v, **{n: True for n in SWITCHES})


if __name__ == "__main__":                      # the master-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
