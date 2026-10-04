"""`--rung-theta NAME=PATH.npy`: a frozen trained theta pinned into the ladder.

The ladder is hand-set archetypes -- knob vectors, not trained policies -- so
the one comparison it cannot make is against a policy this project already
shipped. An **anchor** is that: a checkpoint's theta registered as a named rung,
scored on the same fixed seeds and logged beside every other rung.

It is a *holdout* rung by default, and that is the property worth pinning. A
weight of 0 is no episode slots in `opponent_slots` and no share of any
`absolute_report` headline, which is what `AR.HOLDOUT_RUNGS` means by "reported,
never trained or selected on" -- but unlike those, `--rung-weight NAME=W` can
pull it into the objective without a code change.

Absent the flag nothing moves: same rung list, same weights, same `None` from
`weighted_slots()`, so the opponent row is byte-identical to the run before.
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
import train as T

from kagg3.core import policy as PO
from kagg3.es.train import NO_BEST, Config, Trainer, opponent_slots
from kagg3.es import archetypes as A


def _tiny(**kw):
    return Config(pop=4, episodes=4, chunk=8, abs_pairs=2,
                  **dict({"holdout_rungs": False}, **kw))


@pytest.fixture(scope="module")
def anchor_path(tmp_path_factory):
    """A live theta on disk. Any archetype's own vector will do -- what the file
    has to be is a flat `N_PARAMS` policy that clears the liveness floor, which
    is exactly what a shipped checkpoint is."""
    p = tmp_path_factory.mktemp("anchor") / "best_abs.npy"
    np.save(p, np.asarray(A.archetype_theta(**A.named(A.NAMES[0])), np.float32))
    return str(p)


class _Stub:
    """Enough of a Trainer for the paths that never reach a rollout."""

    def __init__(self, names=(), thetas=()):
        self.cfg = Config()
        self.archetype_names = list(names)
        self.archetypes = list(thetas)
        # `add_anchor_rungs` ends in `reset_best_if_ladder_changed`, which reads
        # the whole `ladder_signature` before it works out that a stub with no
        # `ckpt_rungs` is not a resume at all. A real Trainer always has these
        # two -- `_bind_rungs` derives them from the names -- so a stand-in
        # without them fails on the signature rather than on the rule under test.
        self.rung_weights = np.ones(len(self.archetype_names))
        self.arch_handicap = np.zeros((len(self.archetype_names), 2), np.int32)
        self.reprobed = 0

    def reprobe_archetypes(self):
        self.reprobed += 1


# ----------------------------------------------------------------- parsing

def test_the_flag_is_repeatable_and_parsed_by_name(anchor_path):
    assert T.parse_rung_thetas([f"a={anchor_path}", f"b={anchor_path}"]) == \
        (("a", anchor_path), ("b", anchor_path))


def test_no_flag_parses_to_nothing_at_all():
    assert T.parse_rung_thetas(None) == ()
    assert T.parse_rung_thetas([]) == ()


def test_a_bad_rung_theta_is_refused_before_the_run_directory_exists(anchor_path):
    # Every one of these is a pure-function refusal, like `parse_rung_weights`:
    # it happens while the arguments are being read, before `os.makedirs`.
    with pytest.raises(SystemExit, match="expected NAME=PATH"):
        T.parse_rung_thetas([anchor_path])
    with pytest.raises(SystemExit, match="expected NAME=PATH"):
        T.parse_rung_thetas([f"={anchor_path}"])
    with pytest.raises(SystemExit, match="no such file"):
        T.parse_rung_thetas(["a=/nope/does_not_exist.npy"])
    with pytest.raises(SystemExit, match="more than once"):
        T.parse_rung_thetas([f"a={anchor_path}", f"a={anchor_path}"])


def test_an_anchor_may_not_shadow_a_ladder_pin(anchor_path):
    # The pins are what every measured number on record is stated against.
    for name in (A.NAMES[0], A.PROXY_NAME, "sampled0", "rung3"):
        with pytest.raises(SystemExit, match="ladder rung label"):
            T.parse_rung_thetas([f"{name}={anchor_path}"])


def test_a_weight_may_name_an_anchor_and_a_typo_is_still_refused():
    names = T.rung_names(2) + ["anchor"]
    assert T.parse_rung_weights(["anchor=3"], names) == (("anchor", 3.0),)
    with pytest.raises(SystemExit, match="no rung called"):
        T.parse_rung_weights(["anchor=3"], T.rung_names(2))


# ------------------------------------------------------- registration shape

def test_a_two_dimensional_file_is_not_a_theta(tmp_path):
    p = tmp_path / "pool.npy"
    np.save(p, np.zeros((4, PO.N_PARAMS), np.float32))
    with pytest.raises(SystemExit, match="flat theta vector"):
        T.add_anchor_rungs(_Stub(), (("a", str(p)),), (("a", 0.0),))


def test_an_older_layout_anchor_is_zero_extended(tmp_path):
    short = np.arange(PO.N_PARAMS - 3, dtype=np.float32) + 1.0
    p = tmp_path / "old.npy"
    np.save(p, short)
    stub = _Stub()
    T.add_anchor_rungs(stub, (("a", str(p)),), (("a", 0.0),))
    got = np.asarray(stub.archetypes[0])
    assert got.shape == (PO.N_PARAMS,)
    assert np.array_equal(got[:-3], short) and not got[-3:].any()


def test_re_registering_a_name_rebinds_it_rather_than_appending(tmp_path):
    """What makes `--resume` with the same flags idempotent: the anchor comes
    back inside `state.npz`'s archetypes, so the flag must not append a twin."""
    other = tmp_path / "other.npy"
    np.save(other, np.full(PO.N_PARAMS, 0.5, np.float32))
    stub = _Stub(["rusher", "anchor"], [np.zeros(PO.N_PARAMS, np.float32),
                                        np.zeros(PO.N_PARAMS, np.float32)])
    T.add_anchor_rungs(stub, (("anchor", str(other)),), (("anchor", 0.0),))
    assert stub.archetype_names == ["rusher", "anchor"]
    assert np.asarray(stub.archetypes[1]).tolist() == [0.5] * PO.N_PARAMS
    assert np.asarray(stub.archetypes[0]).tolist() == [0.0] * PO.N_PARAMS
    assert stub.reprobed == 1


# ------------------------------------------------------------- in a Trainer

@pytest.fixture(scope="module")
def base():
    return Trainer(_tiny(n_archetypes=2), seed=0)


@pytest.fixture(scope="module")
def anchored(anchor_path):
    tr = Trainer(_tiny(n_archetypes=2), seed=0)
    T.add_anchor_rungs(tr, (("anchor", anchor_path),), (("anchor", 0.0),))
    return tr


def test_the_anchor_is_a_named_rung_holding_the_file_s_theta(anchored,
                                                             anchor_path):
    assert anchored.archetype_names[-1] == "anchor"
    assert np.array_equal(np.asarray(anchored.archetypes[-1]), np.load(anchor_path))
    assert len(anchored.archetypes) == len(anchored.archetype_names) == 3
    # Aligned with the probe, or every `keep` ratio in `absolute_report` reads 0.
    assert len(anchored.archetype_coins) == 3
    assert anchored.archetype_coins[-1] >= A.MIN_COINS


def test_the_anchor_is_appended_and_the_ladder_pins_do_not_move(anchored, base):
    assert anchored.archetype_names[:2] == base.archetype_names
    for a, b in zip(anchored.archetypes, base.archetypes):
        assert np.array_equal(np.asarray(a), np.asarray(b))


def test_the_anchor_is_a_holdout_rung_by_default(anchored):
    assert anchored.rung_weights.tolist() == [1.0, 1.0, 0.0]
    idx = opponent_slots(32, len(anchored.pool), 3, anchored.cfg.arch_frac,
                         anchored.weighted_slots())
    # Rung 2 is the anchor; `candidates()` is pool + archetypes + [theta].
    assert (idx == len(anchored.pool) + 2).sum() == 0


def test_a_weight_pulls_the_anchor_into_the_objective(anchor_path):
    tr = Trainer(_tiny(n_archetypes=2), seed=0)
    T.add_anchor_rungs(tr, (("anchor", anchor_path),), (("anchor", 3.0),))
    assert tr.rung_weights.tolist() == [1.0, 1.0, 3.0]
    idx = opponent_slots(32, len(tr.pool), 3, tr.cfg.arch_frac,
                         tr.weighted_slots())
    assert (idx == len(tr.pool) + 2).sum() > 0


def test_the_anchor_is_scored_and_logged_but_carries_no_weight(anchored):
    rep = anchored.absolute_report(anchored.theta)
    assert len(rep.mine) == len(rep.theirs) == len(rep.wins) == 3
    assert rep.weights[-1] == 0.0            # out of every headline mean
    assert rep.theirs[-1] > 0                # and still measured
    assert 0.0 <= rep.keep[-1]


def test_without_the_flag_the_rung_list_is_identical(base):
    assert base.archetype_names == list(A.NAMES[:2])
    assert base.rung_weights.tolist() == [1.0, 1.0]
    assert base.weighted_slots() is None     # the byte-identical opponent row
    assert base.cfg.rung_weight == ()


# ------------------------------------------------- alongside the flow rung

def test_flow_and_anchor_rungs_coexist(tmp_path, anchor_path):
    """`--kagg2-flow --rung-theta anchor=... --resume` on a 9-rung checkpoint.

    The two flags grow the same ladder from opposite ends of `main`: the flow
    rung is appended by `Trainer` (inside `reprobe_archetypes`, which is also
    where a restored ladder is extended by it), the anchor by
    `add_anchor_rungs` afterwards. What has to hold is that they compose --
    `[9 ladder] + [kagg2_flow] + [anchor]`, `flow_rung` pointing at the flow
    rung and not at the anchor, and every per-rung array the same length as the
    ladder, because `absolute_report` reads `archetype_coins` positionally and
    a short one silently reads every `keep` ratio as 0.

    Episode-level calls go through `jax.jit` for the reason
    `test_kagg2_flow.py` gives: an un-jitted `rollout.episode` compiles every
    primitive of the scan separately and segfaults this box's CPU backend.
    `Trainer`'s own evaluator is already one compiled program, so the probe and
    the report below are that.
    """
    from kagg3.es import kagg2_flow as K2F

    base = dict(pop=2, episodes=4, chunk=4, abs_pairs=2, n_archetypes=9,
                holdout_rungs=False)

    # --- the flags parse against the ladder the run will actually hold
    names = T.rung_names(9, kagg2_flow=True)
    assert names[-1] == K2F.RUNG_NAME
    weights = T.parse_rung_weights([f"{K2F.RUNG_NAME}=3", "anchor=1"],
                                   names + ["anchor"])
    assert weights == ((K2F.RUNG_NAME, 3.0), ("anchor", 1.0))
    anchor_weight = tuple((n, dict(weights).get(n, 0.0)) for n in ["anchor"])
    rung_weight = tuple((n, w) for n, w in weights if n != "anchor")
    assert rung_weight == ((K2F.RUNG_NAME, 3.0),)

    # --- a checkpoint from before either flag: nine hand-set rungs
    old = Trainer(Config(**base), seed=3)
    assert len(old.archetypes) == 9 and old.flow_rung == -1
    old.theta = old.theta + 0.25
    old.t = 41
    old.best_abs = 123_456.0
    T.save_state(str(tmp_path), old, 1234, elapsed=987.5)

    # --- resumed with both flags, in `main`'s order: Trainer, resume, anchor
    cfg = Config(kagg2_flow=True, kagg2_flow_jitter=0,
                 kagg2_flow_scale=(1.0, 1.0), rung_weight=rung_weight, **base)
    new = Trainer(cfg, seed=0)
    gen, _how, elapsed = T.load_resume(new, str(tmp_path))
    T.add_anchor_rungs(new, (("anchor", anchor_path),), anchor_weight)

    # --- eleven rungs, in order, and the flow rung is the flow rung
    assert new.archetype_names == list(A.NAMES[:9]) + [K2F.RUNG_NAME, "anchor"]
    assert new.flow_rung == 9
    assert new.archetype_names[new.flow_rung] == K2F.RUNG_NAME

    # --- every per-rung array is the ladder's length, or the report lies
    assert len(new.archetypes) == 11
    assert len(new.archetype_coins) == 11
    assert len(new.rung_weights) == 11
    assert new.arch_handicap.shape == (11, 2)
    assert new.rung_weights.tolist() == [1.0] * 9 + [3.0, 1.0]
    assert min(new.archetype_coins) >= A.MIN_COINS

    # --- the ES state is still the checkpoint's; the anchor is the file's
    assert (gen, elapsed) == (1234, 987.5)
    assert np.array_equal(np.asarray(new.theta), np.asarray(old.theta))
    assert new.t == 41
    # Two new rungs and a re-divided set of weights: `best_abs` was a coin
    # count against neither, so it is retired rather than inherited.
    assert new.best_abs == NO_BEST
    assert np.array_equal(np.asarray(new.archetypes[-1]), np.load(anchor_path))

    # --- the flow reaches rung 9 and only rung 9, anchor included
    flow = np.asarray(new.episode_flow(
        3, np.array([len(new.pool) + 9, len(new.pool) + 10, 0])))
    assert list(flow[:, 0]) == [1, 0, -1, -1, -1, -1]

    # --- and the report scores all eleven, the anchor weighted as asked
    rep = new.absolute_report(new.theta)
    assert len(rep.mine) == len(rep.theirs) == len(rep.wins) == 11
    assert len(rep.keep) == len(rep.live) == len(rep.weights) == 11
    assert rep.weights[9] == (3.0 if rep.live[9] else 0.0)
    assert rep.weights[-1] == (1.0 if rep.live[-1] else 0.0)
