"""The switch-gene block (`policy.SHAPES`' `sw`/`swb`, 2026-09-16).

`plan` carries 66 module constants `NAME_ON = True/False`. The lead flipped
them by hand and judged one arm at a time -- two reads a day against a ladder
that releases daily -- and `docs/strategy/2026-09-16-es-plateau.md` is the other
half of the argument: ES from B on the *existing* genes is flat (true effect
-124 +/- 47), so the search needs new expressible dimensions, and the switch
vector is 66 of them sitting in the source as constants.

Thirteen of them are read from the theta here. The three groups every appended block
in this layout has to pass, plus one this block adds:

* the layout -- an append at the tail, nothing before it moved, and the shipped
  6,789-long champion plans byte for byte what it planned at `4c6565b`;
* the decode -- exactly "the module default" at zero, one-sided, and a measured
  flip rate at the training sigma [GENE SLOPE RULE];
* backend agreement -- numpy against a trace, which take structurally different
  paths here (`plan._sw` returns a Python bool to one and a tracer to the
  other) and must still agree byte for byte;
* **equivalence** -- a gene forced ON must plan exactly what flipping the
  module constant plans, or the block is a new lever rather than the one the
  judge reads have been measuring.
"""
from __future__ import annotations

import contextlib
import hashlib
import os
import subprocess
import sys
import tempfile
import time

os.environ.setdefault("JAX_PLATFORMS", "cpu")
# The `--digests` subprocess below imports a pristine `git archive` tree
# instead of this one, so the path has to be chosen before the imports.
_SRC = (sys.argv[sys.argv.index("--digests") + 1] if "--digests" in sys.argv
        else "src")
sys.path.insert(0, _SRC)

import kagg3
import numpy as np

assert os.path.abspath(kagg3.__file__).startswith(os.path.abspath(_SRC)), \
    f"wrong tree: {kagg3.__file__}"

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import plan as P
from kagg3.core import policy as PO

#: The layout the block appends to -- `cd`'s, i.e. every theta written before
#: 2026-09-16, the shipped champion (6,789) included.
PRE_SW_N = 7065

#: The incumbent this branch must not move: the commit `geneswitch` forked off.
BASE_REV = "4c6565b"

CHAMPION = ("/mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/"
            "flow193_g100_hr.npy")
TRAJ = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", "trajectory_obs.npz")

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
TABLE = spec.build_price_table()


def _macro(**kw):
    """The shipped fixture macro (`tests/test_budget_order._macro`), inlined so
    this file runs against an archived `src` whose `Macro` has no `switches`
    field at all."""
    base = {
        "plant_target": np.zeros(spec.N_CROPS, np.int32),
        "animal_want": np.zeros(spec.N_ANIMALS, np.int32),
        "land_bias": np.int32(0),
        "hold": np.zeros(spec.N_PRODUCTS, np.int32),   # sell, so the market row is live
        "press": np.zeros(spec.N_PRODUCTS, np.int32),
        "grow_mult": np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32),
        "compact": np.int32(0),
        "dev_weight": np.int32(brain.GROW_ONE),
        "hire_bias": np.int32(0),
        "crew_target": np.int32(3),                    # so CREW_PUSH_COST has a push
        "animal_defer": np.int32(0),
        "forward_days": np.int32(0),
    }
    base.update(kw)
    return P.Macro(**base)


def _view(day=6, money=3_000, n_wh=6, age=4, n_an=2, shed_ca=30, shed_wh=8,
          shed_fert=4, yld=4, nquad=2, shops=1, water=0, cons=1,
          crop=spec.I_WHEAT, cared=0, an_cons=None, price=None):
    """A working farm: wheat tiles part way through their stream, two stocked
    coops, and a shed with something in it to sell, fertilize with and feed.

    The ten wired switches touch watering, feeding, care, fertilizer, the shed
    inflow, the crew push and the plant mix, so a fixture that reaches none of
    those would make every equivalence assertion below vacuous
    (`test_the_boards_actually_move` is the guard on that)."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield, t_cons = z.copy(), z.copy(), z.copy(), z.copy()
    t_cared, t_fert, t_favail = z.copy(), z - 1, z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = crop
    # Heterogeneous on purpose: identical tiles give every value switch the
    # same answer on all of them, and a bar that cuts nothing or everything
    # cannot change a plan. Ages and standing yields spread, so the admission
    # order, the fertilizer bar and the survival test each cut the board
    # somewhere in the middle.
    spread = np.arange(n_wh, dtype=np.int32)
    t_day[:n_wh] = day - age - (spread % 4)
    t_yield[:n_wh] = yld - (spread % 3)
    t_wat[:n_wh] = water
    t_cons[:n_wh] = cons
    t_favail[:n_wh] = 1
    kind[n_wh:n_wh + n_an] = spec.KIND_COOP
    occ[n_wh:n_wh + n_an] = 0                       # goose
    t_day[n_wh:n_wh + n_an] = day - age
    t_cons[n_wh:n_wh + n_an] = cons if an_cons is None else an_cons
    t_cared[n_wh:n_wh + n_an] = cared
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_CARROT] = shed_ca
    shed[spec.I_WHEAT] = shed_wh
    shed[spec.I_FERT] = shed_fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=t_cons, t_yield=t_yield, t_fert=t_fert, t_cared=t_cared,
        t_favail=t_favail, shed=shed,
        seeds=np.full(spec.N_CROPS, 4, np.int32), money=np.int32(money),
        nquad=np.int32(nquad),
        price=BASE_PRICE if price is None else np.asarray(price, np.int32),
        mkt_inv=np.full(spec.N_PRODUCTS, int(spec.MARKET_I0), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


#: A mix the brain does not choose on its own on a late board, so the three
#: plant-mix switches have something to rewrite. Applied to the *decoded*
#: macro, not instead of it, so the switch vector is still the theta's.
MIX = dict(plant_target=np.array([6, 4, 2, 3, 1], np.int32))

#: Nine boards across the season, chosen so that each wired switch actually
#: cuts one of them somewhere -- an equivalence assertion between two plans
#: neither switch can move is no assertion at all
#: (`test_the_boards_actually_move` is the guard, `S/geneswitch/probe.py` the
#: search that picked these).
PIN_BOARDS = (
    ("early", dict(day=3, money=1_200, n_wh=4, age=2, shed_ca=0, shed_wh=4), {}),
    ("mid", dict(day=6), {}),
    ("scarce", dict(day=12, money=200, n_wh=20, n_an=6, cons=2, yld=6), {}),
    ("feed", dict(day=9, money=200, n_wh=10, n_an=8, cons=2, an_cons=0,
                  shed_wh=40), {}),
    ("fert", dict(day=14, money=5_000, n_wh=12, n_an=3, shed_fert=20, cons=1,
                  crop=spec.I_STRAWBERRY, yld=6,
                  price=np.array([25, 35, 60, 120, 250, 5, 160, 200, 100],
                                 np.int32)), {}),
    ("mix16", dict(day=16, money=12_000, n_wh=8, n_an=2, shops=2, nquad=3), MIX),
    ("late26", dict(day=26, money=300, n_wh=16, n_an=4, cons=2, yld=4), {}),
    ("rich27", dict(day=27, money=60_000, n_wh=10, n_an=3, shops=3, nquad=4), {}),
    ("terminal", dict(day=29, money=60_000, n_wh=8, n_an=2), {}),
)


def _plan(view, macro):
    return tuple(np.asarray(a, np.int32) for a in P.build_day(np, view, macro, TABLE))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()[:16]


def _theta_macro(view, theta, macro_kw=None):
    """The macro the champion decodes for a board, so the pin covers the
    *decode* as well as the planner."""
    obs = brain.PolicyObs(
        day=view.day, money=view.money, opp_money=np.int32(3_000),
        kind=view.kind, occ=view.occ,
        opp_kind=np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32),
        opp_occ=np.zeros(spec.N_TILES, np.int32) - 1,
        t_day=view.t_day, t_yield=view.t_yield, shed=view.shed,
        seeds=view.seeds, nquad=view.nquad, opp_nquad=np.int32(2),
        mkt_inv=view.mkt_inv, price=view.price, shops=view.shops)
    macro = brain.decide(np, theta, obs)
    return macro._replace(**macro_kw) if macro_kw else macro


#: Module switches PROMOTED since `BASE_REV`, with the value they had there.
#: The pin below is a claim about the switch-gene BLOCK -- "a zero block is the
#: fork tree byte for byte" -- and a default promoted on its own evidence
#: (`FERT_TIMING_ON` 09-16, `ENDROUTE_ON` 09-17, each with its own identity pin
#: in `tests/test_fertengine.py` / `tests/test_endroute.py`) is not this block
#: moving.  Set back here, so the pin keeps measuring what it names; absent on
#: the fork tree itself, where the names do not exist at all.
PROMOTED_SINCE_BASE = {"FERT_TIMING_ON": False, "ENDROUTE_ON": False,
                       "OPEN_PUMP_ON": True, "CLIP_CAP_ON": False,
                       # 2026-09-18 WIDEPICK: shipped False -> True, and it
                       # re-cuts the `fert` board's wide morning, so the
                       # fork-commit identity has to ask it at its base value.
                       "WIDE_PICK_ON": False, "CARE_FILL_ON": False,
                       "OVERFLOW_GUARD_ON": False}


@contextlib.contextmanager
def _at_base_defaults():
    was = {n: getattr(P, n) for n in PROMOTED_SINCE_BASE if hasattr(P, n)}
    for n, v in PROMOTED_SINCE_BASE.items():
        if hasattr(P, n):
            setattr(P, n, v)
    try:
        yield
    finally:
        for n, v in was.items():
            setattr(P, n, v)


def _own_digests():
    theta = np.load(CHAMPION).astype(np.float32)
    out = {}
    with _at_base_defaults():
        for name, kw, mk in PIN_BOARDS:
            view = _view(**kw)
            out[name] = _digest(_plan(view, _theta_macro(view, theta, mk)))
            out[name + "_fx"] = _digest(_plan(view, _macro(**mk)))
    return out


def _base_digests():
    """The same plans built by a pristine `git archive 4c6565b src` tree in a
    subprocess -- the pin is the commit this branch forked off, not this file's
    own output."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {BASE_REV} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


if __name__ == "__main__":                    # the `--digests` subprocess
    for k, v in sorted(_own_digests().items()):
        print(k, v)
    raise SystemExit(0)

import pytest


def _forced(index, logit=8.0):
    """The champion, padded, with one switch gene driven hard ON.

    `sw` stays zero, so `z = gh @ sw + swb` is `logit` whatever the board puts
    in the head -- which makes the assertions below statements about the
    *decode* and not about one observation."""
    th = PO.pad(np.load(CHAMPION).astype(np.float32))
    th[PO.offset("swb") + index] = logit
    return th


def _padded():
    return PO.pad(np.load(CHAMPION).astype(np.float32))


needs_theta = pytest.mark.skipif(not os.path.isfile(CHAMPION),
                                 reason="needs the shipped champion")


@pytest.fixture(autouse=True)
def _restore():
    """Every test STARTS from the shipped switch vector and leaves the module
    constants where it found them.

    Resetting on the way IN as well as out is not belt and braces: several tests
    here compare two whole plans built minutes apart, so a constant another test
    (or another module's import) moved and did not put back turns one of them
    into a different program and the comparison silently measures that instead.
    The shipped vector is `SWITCH_GENE_DEFAULTS`, captured at import."""
    saved = {n: getattr(P, n) for n in P.SWITCH_GENES}
    for n, v in P.SWITCH_GENE_DEFAULTS.items():
        setattr(P, n, v)
    yield
    for n, v in saved.items():
        setattr(P, n, v)


# ------------------------------------------------------------------ layout

def test_the_block_is_a_clean_append():
    # 2026-09-17: 10 -> 11, `ENDROUTE_ON` appended at the END of the tuple when
    # it shipped (the block must be the full catalogue of shipped switches),
    # then 11 -> 13 when PUMPCLIP shipped `OPEN_PUMP_ON = False` and
    # `CLIP_CAP_ON = True` as one arm -- both are a shipped value now, so both
    # are columns, appended in that order and never renumbered.
    # 2026-09-18: 13 -> 15 when PES shipped `ENDROUTE2_ON = True` and
    # `ENDROUTE2_SPLIT_ON = True` as one cell with PUMPCLIP -- same rule, same
    # append-at-the-end, `g12` shifts 7,494 -> 7,560 and the layout 7,527 ->
    # 7,593.
    # 2026-09-18: 15 -> 16 when ESR shipped `ENDROUTE_ROW2_ON = True` -- same
    # rule, same append-at-the-end, `g12` shifts 7,560 -> 7,593 and the layout
    # 7,593 -> 7,626.  The SAME ship moved `OPEN_PUMP_ON` back to True and
    # `CLIP_CAP_ON` back to False; neither is renumbered and neither leaves the
    # tuple, because a zero gene decodes to the module default WHATEVER that
    # default currently is, so the block still carries both either way.
    # 2026-09-18: 16 -> 17 when WIDEPICK shipped `WIDE_PICK_ON = True` -- same
    # rule, same append-at-the-end, `g12` shifts 7,593 -> 7,626 and the layout
    # 7,626 -> 7,659.
    # 2026-09-18: 17 -> 18 when WIDEPICK2 WROTE `WIDE_PICK_FREE_ON` -- the
    # catalogue rule is about the SWITCH, not about its shipped value, so a
    # written-and-OFF arm is a column too and a zero gene decodes to its False.
    # `g12` shifts 7,659 -> 7,692 and the layout 7,692 -> 7,725.
    # Widening SHIFTS `g12`, so a theta written under the 7,428, 7,461, 7,527,
    # 7,593, 7,626 or 7,659 layout is not a prefix of this one; everything at
    # or below 7,065 still is.
    assert PO.N_SWITCH_GENES == len(P.SWITCH_GENES) == 21
    assert P.SWITCH_GENES[-9:] == ("CLIP_CAP_ON",
                                   "ENDROUTE2_ON", "ENDROUTE2_SPLIT_ON",
                                   "ENDROUTE_ROW2_ON", "WIDE_PICK_ON",
                                   "WIDE_PICK_FREE_ON", "MELONVETO_POST_ON",
                                   "CARE_FILL_ON", "OVERFLOW_GUARD_ON")
    assert PO.offset("sw") == PRE_SW_N
    # FERTENGINE appended g12/gb12 (33 params) AFTER this block on the merge,
    # so the block ends at 7,758 and the layout at 7,791.
    assert PO.offset("g12") == PRE_SW_N + PO.N_HEAD_HID * 21 + 21 == 7_758
    assert PO.N_PARAMS == 7_791
    names = [n for n, _ in PO.SHAPES]
    assert names[-4:-2] == ["sw", "swb"]
    # Every new coordinate is live, so the ES can find it without a flag ...
    assert PO.live_mask()[PO.offset("sw"):].all()
    # ... and `--train-only` can name the block on its own, which is what makes
    # it the cheapest arm in the layout (693 coordinates against 7,791).
    from kagg3.es.train import train_mask
    m = train_mask("sw,swb")
    assert m[PO.offset("sw"):PO.offset("g12")].all() and not m[:PO.offset("sw")].any()
    assert not m[PO.offset("g12"):].any()
    assert int(m.sum()) == 693


def test_pad_zero_extends_and_keeps_the_prefix():
    rng = np.random.default_rng(1)
    old = rng.normal(0.0, 0.3, PRE_SW_N).astype(np.float32)
    new = PO.pad(old)
    assert new.shape == (PO.N_PARAMS,)
    assert np.array_equal(new[:PRE_SW_N], old)
    assert not new[PO.offset("sw"):].any()


def test_the_registry_is_a_layout_and_says_so():
    """Column `i` is `SWITCH_GENES[i]` for the life of every theta trained
    under it: the names are unique, and each default is the module's."""
    assert len(set(P.SWITCH_GENES)) == len(P.SWITCH_GENES)
    for i, n in enumerate(P.SWITCH_GENES):
        assert P.SWITCH_GENE_INDEX[n] == i
        assert P.SWITCH_GENE_DEFAULTS[n] is bool(getattr(P, n))


# ------------------------------------------------------------------ decode

@needs_theta
def test_a_theta_below_the_block_decodes_the_module_defaults():
    """The inertness a shorter theta gets: `unpack` zero-pads it, `z` is 0.0
    and the vector is `SWITCH_DEFAULT`, so on the numpy path every guarded site
    takes its original Python branch and no `where` is built."""
    theta = np.load(CHAMPION).astype(np.float32)
    assert theta.shape == (6_789,)
    for _n, kw, _mk in PIN_BOARDS:
        m = _theta_macro(_view(**kw), theta)
        assert not np.asarray(m.switches).any()
        for name in P.SWITCH_GENES:
            assert P._sw(m, name) is P.SWITCH_GENE_DEFAULTS[name]


@needs_theta
def test_a_zero_block_decodes_every_switch_to_its_module_default():
    theta = _padded()
    assert not theta[PO.offset("sw"):].any()
    for _n, kw, _mk in PIN_BOARDS:
        macro = _theta_macro(_view(**kw), theta)
        assert macro.switches is not None
        assert np.asarray(macro.switches).dtype == np.int32
        assert not np.asarray(macro.switches).any()
        for name in P.SWITCH_GENES:
            assert P._sw(macro, name) is P.SWITCH_GENE_DEFAULTS[name]


def test_the_decode_is_one_sided_and_inert_at_zero():
    """`round(SWITCH_GAIN * z) > 0`: 0 at z = 0 -- `_qfloor(0.5)` must break
    *down* or an untrained block would ship ten flipped switches -- and a
    negative logit is the default too, not a second flip."""
    assert int(brain._qfloor(np, np.float32(brain.SWITCH_GAIN * 0.0 + 0.5))) == 0
    th = PO.pad(np.zeros(PRE_SW_N, np.float32))
    for z in (0.0, -0.01, -1.0, -40.0):
        th[PO.offset("swb"):] = z
        m = _theta_macro(_view(), th)
        assert not np.asarray(m.switches).any(), z
    for z in (0.5 / brain.SWITCH_GAIN + 1e-3, 1.0, 40.0):
        th[PO.offset("swb"):] = z
        assert np.asarray(_theta_macro(_view(), th).switches).all(), z


# -------------------------------------------------------------- equivalence

@needs_theta
@pytest.mark.parametrize("index,name", list(enumerate(P.SWITCH_GENES)))
def test_a_forced_gene_plans_exactly_what_the_module_switch_plans(index, name):
    """The equivalence claim: ON by gene and ON by constant are the same plan,
    byte for byte, on every pin board -- so every judge read taken on the
    hand-flipped switch still describes the gene."""
    gene = _forced(index)
    flipped = not P.SWITCH_GENE_DEFAULTS[name]
    for bname, kw, mk in PIN_BOARDS:
        view = _view(**kw)
        by_gene = _plan(view, _theta_macro(view, gene, mk))
        setattr(P, name, flipped)               # the lead's override wins ...
        by_module = _plan(view, _theta_macro(view, gene, mk))
        setattr(P, name, P.SWITCH_GENE_DEFAULTS[name])
        for i, (a, b) in enumerate(zip(by_gene, by_module)):
            assert np.array_equal(a, b), f"{name} on {bname}: plan[{i}]"


@needs_theta
def test_the_boards_actually_move():
    """The guard on the test above being vacuous: a majority of the thirteen genes
    must change the plan on at least one pin board, or the equivalence is a
    claim about two identical no-ops."""
    def digests(theta):
        out = {}
        for n, kw, mk in PIN_BOARDS:
            view = _view(**kw)
            macro = _theta_macro(view, theta, mk)
            out[n] = _digest(_plan(view, macro))
            # `_derive`'s chains too: a tier switch can reorder the admission
            # on a board whose turns then execute the same ops anyway, and that
            # is still the switch doing its job.
            out[n + "_d"] = _digest(P._derive(np, view, macro, TABLE, np.int32(0),
                                              np.False_, np.int32(0)))
        return out

    base = digests(_padded())
    moved = [name for i, name in enumerate(P.SWITCH_GENES)
             if digests(_forced(i)) != base]
    assert len(moved) >= 9, moved


@needs_theta
def test_the_module_override_beats_the_gene_and_only_then():
    """`plan`'s constants stay a manual A/B lever: moved off the value they
    ship with they pin the switch whatever the theta says, left alone the gene
    rules. One comparison, the same rule as `FORWARD_ADMIT_ON`."""
    view = _view(day=11, money=9_000)
    for i, name in enumerate(P.SWITCH_GENES):
        dflt = P.SWITCH_GENE_DEFAULTS[name]
        gene_on = _theta_macro(view, _forced(i))
        assert P._sw(gene_on, name) is (not dflt)
        setattr(P, name, not dflt)
        assert P._sw(gene_on, name) is (not dflt)     # agrees, and by override
        setattr(P, name, dflt)
        # ... and the override pins it in the *other* direction too: a gene
        # that asks for the flip is ignored while the constant is elsewhere.
        assert P._sw(_theta_macro(view, _padded()), name) is dflt


# ---------------------------------------------------------------- identity

@needs_theta
def test_the_shipped_champion_plans_byte_for_byte_what_4c6565b_planned():
    """The OFF-identity pin: the 6,789-long champion and the hand fixture, on
    every pin board, hashed, against a pristine tree at the fork commit -- with
    the switches promoted since (`PROMOTED_SINCE_BASE`) set back to the values
    they had there, so what is measured is this block and not them."""
    assert _own_digests() == _base_digests()


# ------------------------------------------------------- backend agreement

_JF = []


def _jit_build_day():
    """One compiled program for the whole file: every test below traces the
    same `build_day` and only the values differ, so eleven `jax.jit` wrappers
    would be thirteen compiles of one program."""
    if not _JF:
        import jax
        import jax.numpy as jnp
        _JF.append(jax.jit(lambda v, m: P.build_day(jnp, v, m, jnp.asarray(TABLE))))
    return _JF[0]


def _jax_args(view, macro):
    import jax.numpy as jnp
    jview = view._replace(**{f: jnp.asarray(getattr(view, f)) for f in view._fields})
    jmacro = macro._replace(**{f: jnp.asarray(getattr(macro, f))
                               for f in macro._fields})
    return jview, jmacro


@needs_theta
@pytest.mark.parametrize("index", [None] + list(range(len(P.SWITCH_GENES))))
def test_numpy_and_a_trace_agree(index):
    """numpy takes the Python branch and a trace takes the `where`; they must
    still produce the same plan byte for byte. `index=None` is the zero block,
    where numpy skips every `where` the trace has to build."""
    theta = _padded() if index is None else _forced(index)
    jf = _jit_build_day()
    for bname, kw, mk in PIN_BOARDS[:4]:
        view = _view(**kw)
        macro = _theta_macro(view, theta, mk)
        jview, jmacro = _jax_args(view, macro)
        for i, (a, b) in enumerate(zip(_plan(view, macro), jf(jview, jmacro))):
            assert np.array_equal(a, np.asarray(b)), f"{bname}: plan[{i}]"


@needs_theta
def test_the_jit_still_compiles_and_reports_what_it_cost():
    """A traced switch means both branches are in the program; this is the bar
    that the ten of them did not blow the compile up. The number is reported
    against `4c6565b`'s in docs/strategy/2026-09-16-geneswitch.md."""
    import jax
    import jax.numpy as jnp

    view = _view(day=11, money=9_000)
    macro = _theta_macro(view, _padded())
    jview, jmacro = _jax_args(view, macro)
    # Its own wrapper, not the shared one: a cached compile would measure
    # nothing at all when this test happens to run second.
    jf = jax.jit(lambda v, m: P.build_day(jnp, v, m, jnp.asarray(TABLE)))
    t0 = time.time()
    jax.block_until_ready(jf(jview, jmacro))
    print(f"\ngeneswitch first compile: {time.time() - t0:.1f} s")
    assert time.time() - t0 < 600.0


# --------------------------------------------------------- a slope ES feels
#
# A gene the search cannot select on is a dead gene [GENE SLOPE RULE
# 2026-09-09]: the `g170` block shipped in a zone where *no* perturbation at
# the training sigma moved its decode. `S/geneswitch/slope.py` is the full
# measurement (4,096 antithetic members, eight recorded boards); this is its
# bar, so a later edit to `SWITCH_GAIN` cannot walk the block back into a flat
# zone unnoticed.

ES_POP, ES_SIGMA = 512, 0.02
#: Fraction of the population that must decode a flip, per gene. A *minority*:
#: the centre has to stay the plan most members make, and 17 % is what
#: `SWITCH_GAIN = 8` measures off B at sigma 0.02.
BAND = (0.08, 0.35)


@pytest.mark.skipif(not os.path.isfile(CHAMPION) or not os.path.isfile(TRAJ),
                    reason="needs the champion and the trajectory fixture")
def test_one_es_step_flips_a_minority_of_the_population():
    theta = _padded()
    d = np.load(TRAJ)
    idx = np.random.default_rng(3).choice(len(d["day"]), 4, replace=False)
    inputs = []
    for i in idx:
        o = brain.PolicyObs(**{f: d[f][i] for f in brain.PolicyObs._fields
                               if f in d.files})
        prod, glob, drain = brain.features(np, o)
        b = brain.board_forecasts(np, o)
        inputs.append((prod, glob, drain, brain.production_forecast(np, o, b),
                       brain.forward_value(np, o, b), brain.market_momentum(np, o)))
    rng = np.random.default_rng(1234)
    eps = rng.normal(0.0, 1.0, (ES_POP // 2, PO.N_PARAMS)).astype(np.float32)
    eps = np.concatenate([eps, -eps])
    flips = np.empty((ES_POP, len(inputs), PO.N_SWITCH_GENES), bool)
    for m in range(ES_POP):
        p = PO.unpack(np, (theta + ES_SIGMA * eps[m]).astype(np.float32))
        for b, args in enumerate(inputs):
            z = PO.forward(np, p, *args).switch
            flips[m, b] = np.asarray(
                brain._qfloor(np, brain.SWITCH_GAIN * z + 0.5) > 0)
    per_gene = flips.mean(axis=(0, 1))
    lo, hi = BAND
    assert lo <= per_gene.min() and per_gene.max() <= hi, per_gene
    # ... and the centre itself is unmoved: the modal member flips nothing.
    #
    # The bound has to be WIDTH-AWARE, and a bare 0.10 was not: the share that
    # flips nothing is ~prod(1 - p_i) over the block, so the SAME decode looks
    # quieter every time the catalogue grows -- 0.128 at eleven genes on p 0.17,
    # 0.089 at thirteen, and the measured 0.062 at thirteen is p ~ 0.20.  So pin
    # the claim rather than the number: all-quiet is still the single most
    # common draw (no flipped pattern beats it), and it is within a factor of
    # two of what independent genes at the measured per-gene rates would give.
    quiet = (~flips.any(axis=2)).mean()
    indep = float(np.prod(1.0 - per_gene))
    assert quiet > 0.5 * indep, (quiet, indep)
    counts = {}
    for row in flips.reshape(-1, PO.N_SWITCH_GENES):
        k = row.tobytes()
        counts[k] = counts.get(k, 0) + 1
    zero = np.zeros(PO.N_SWITCH_GENES, bool).tobytes()
    assert counts.get(zero, 0) == max(counts.values()), \
        f"all-quiet {counts.get(zero, 0)} is not the modal draw of {len(counts)}"
