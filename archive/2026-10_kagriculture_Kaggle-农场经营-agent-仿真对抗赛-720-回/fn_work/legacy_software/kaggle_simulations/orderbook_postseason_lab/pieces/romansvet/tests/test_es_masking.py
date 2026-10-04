"""Dead parameter columns (PLANNER_V3_1 section 2) are masked out of the ES
perturbation and update: they neither move nor move anything. The fresh
lineage may copy an older theta's encoder trunk and nothing else.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

import numpy as np

from kagg3.core import policy as PO
from kagg3.es.train import Config, Trainer, perturbations, train_mask


def _block(mask, name):
    off = PO.offset(name)
    shape = dict(PO.SHAPES)[name]
    return mask[off:off + int(np.prod(shape))].reshape(shape)


def test_mask_counts_match_the_spec():
    m = PO.live_mask()
    assert m.shape == (PO.N_PARAMS,) and m.dtype == np.float32
    dead = int((m == 0).sum())
    # 792, not 825: `head[2]` is decoded again (the animal-mix sharpness),
    # so its column of `g2` (32) and its `gb2` bias (1) are live.
    assert dead == PO.N_DEAD == 792
    assert int((_block(m, "g3") == 0).sum()) + int((_block(m, "gb3") == 0).sum()) == 297
    assert int((_block(m, "g4") == 0).sum()) + int((_block(m, "gb4") == 0).sum()) == 33
    assert int((_block(m, "g5") == 0).sum()) + int((_block(m, "gb5") == 0).sum()) == 33
    g2 = _block(m, "g2")
    assert int((g2[:, 13:18] == 0).sum()) + int((_block(m, "gb2")[13:18] == 0).sum()) == 165


def test_live_heads_and_the_encoder_are_unmasked():
    m = PO.live_mask()
    g2 = _block(m, "g2")
    for h in (1, 5, 6, 7):
        assert np.all(g2[:, h] == 1)
    for name in ("w1", "b1", "w2", "b2", "w3", "b3", "g1", "gb1"):
        assert np.all(_block(m, name) == 1)
    g5 = _block(m, "g5")
    assert np.all(g5[:, 1:] == 1) and np.all(g5[:, 0] == 0)


def test_the_masked_perturbation_is_itself_zero_on_dead_coordinates():
    # The update leaving `theta` alone is only half of it: the *perturbation*
    # must be zero there too, or every candidate in the population would still
    # be evaluated with a jittered dead block and the fitness would carry its
    # noise back into the live gradient through the advantage.
    import jax
    tr = Trainer(Config(pop=8, episodes=2, chunk=8, n_archetypes=0, warm_frac=0.0), seed=0)
    eps = np.asarray(perturbations(jax.random.PRNGKey(0), 4, tr.n) * tr.mask)
    dead = PO.live_mask() == 0
    assert eps.shape == (4, tr.n)
    assert np.all(eps[:, dead] == 0.0)
    assert np.any(eps[:, ~dead] != 0.0)
    assert np.asarray(tr.mask).tolist() == PO.live_mask().tolist()


def _diagnostic_trainer(seed=7):
    import jax.numpy as jnp
    tr = Trainer(Config(pop=64, episodes=2, chunk=64, n_archetypes=0,
                        warm_frac=0.0, sigma=0.01), seed=seed)
    def play(thetas, field):
        episodes = field.episodes or tr.cfg.episodes
        return jnp.stack(
            (jnp.arange(thetas.shape[0] * episodes, dtype=jnp.float32)
                 .reshape(thetas.shape[0], episodes) + 1000,
             jnp.full((thetas.shape[0], episodes), 900, jnp.float32)), axis=-1)
    tr.play_generation_field = play
    return tr


def _diagnostic_state(tr):
    import jax
    return (np.asarray(tr.theta).tobytes(), np.asarray(tr.m).tobytes(),
            np.asarray(tr.v).tobytes(), np.asarray(jax.random.key_data(tr.key)).tobytes(),
            repr(tr.rng.bit_generator.state), tr.t, tr.adam_t,
            None if tr.slot_carry is None else tr.slot_carry.credit.tobytes(),
            repr(tr.last_rung_episodes))


def test_scope_diagnostic_uses_fixed_disjoint_masks_and_does_not_update():
    tr = _diagnostic_trainer()
    before = _diagnostic_state(tr)
    tr.apply_gradient = lambda _g: (_ for _ in ()).throw(
        AssertionError("diagnostic must not update"))
    got = tr.antithetic_scope_diagnostic()
    assert _diagnostic_state(tr) == before
    masks = np.asarray(got.masks)
    assert got.scopes == ("M", "H", "J") and got.pairs == 32
    assert [int(x.sum()) for x in masks] == [66, 130, 196]
    assert np.array_equal(masks[2], np.maximum(masks[0], masks[1]))
    assert not np.any((masks[0] != 0) & (masks[1] != 0))
    raw = np.asarray(got.field.noise)
    masked = np.asarray(got.masked_noise)
    assert raw.shape == (32, tr.n) and masked.shape == (3, 32, tr.n)
    assert np.array_equal(masked, raw[None] * masks[:, None])
    assert got.money.shape[:2] == (3, 64)
    assert got.gradients.shape == (3, 3, tr.n)
    from kagg3.es.train import rank_normalise
    for scope in range(3):
        own_rank = rank_normalise(got.own[scope])
        relative_rank = rank_normalise(got.relative[scope])
        assert np.array_equal(np.asarray(got.own_rank[scope]), np.asarray(own_rank))
        assert np.array_equal(np.asarray(got.relative_rank[scope]),
                              np.asarray(relative_rank))
        advantages = (own_rank, relative_rank,
                      tr.cfg.abs_weight * own_rank
                      + (1 - tr.cfg.abs_weight) * relative_rank)
        for component, advantage in enumerate(advantages):
            expected = ((advantage[:32] - advantage[32:])
                        @ got.masked_noise[scope] / (64 * tr.sigma))
            np.testing.assert_allclose(np.asarray(got.gradients[scope, component]),
                                       np.asarray(expected), rtol=1e-6, atol=1e-6)


def test_scope_diagnostic_restores_generation_field_state_on_failure():
    tr = _diagnostic_trainer(8)
    before = _diagnostic_state(tr)
    tr.play_generation_field = lambda *_args: (_ for _ in ()).throw(
        RuntimeError("synthetic evaluator failure"))
    import pytest
    with pytest.raises(RuntimeError, match="synthetic evaluator failure"):
        tr.antithetic_scope_diagnostic()
    assert _diagnostic_state(tr) == before


def test_scope_masks_are_live_policy_blocks_not_the_active_trainer_mask():
    tr = _diagnostic_trainer(9)
    tr.mask = np.zeros(tr.n, np.float32)
    got = tr.antithetic_scope_diagnostic()
    live = PO.live_mask()
    assert np.array_equal(np.asarray(got.masks[0]), live * train_mask("mh,ms"))
    assert np.array_equal(np.asarray(got.masks[1]), live * train_mask("w2,b2"))


def test_scope_diagnostic_reuses_the_ordinary_generation_zero_field():
    diagnostic_tr = _diagnostic_trainer(10)
    ordinary_tr = _diagnostic_trainer(10)
    diagnostic = diagnostic_tr.antithetic_scope_diagnostic()
    seen = {}
    play = ordinary_tr.play_generation_field

    def capture(thetas, field):
        seen["field"] = field
        return play(thetas, field)

    ordinary_tr.play_generation_field = capture
    ordinary_tr.apply_gradient = lambda _grad: None
    ordinary_tr.generation()
    field = seen["field"]
    for name in ("noise", "key", "next_key", "seeds", "opponent_index",
                 "words", "opponents", "episodes"):
        a, b = np.asarray(getattr(diagnostic.field, name)), np.asarray(getattr(field, name))
        assert a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes(), name
    assert diagnostic.field.rung_episodes == field.rung_episodes


def test_scope_runtime_metadata_reads_the_real_jax_config_api():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import train as T
    got = T.scope_runtime_metadata()
    assert got["backend"] == "cpu"
    assert isinstance(got["jax_enable_x64"], bool)
    assert isinstance(got["jax_enable_compilation_cache"], bool)
    assert got["devices"] and all(d["platform"] == "cpu" for d in got["devices"])


def test_scope_serializer_saves_raw_keys_noise_and_no_object_arrays(tmp_path):
    import json
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import train as T
    tr = _diagnostic_trainer(11)
    got = tr.antithetic_scope_diagnostic()
    got = got._replace(field=got.field._replace(episodes=tr.cfg.episodes))
    state = T.scope_training_snapshot(tr)
    T.save_scope_diagnostic(str(tmp_path), tr, got, state, state)
    with np.load(tmp_path / "scope_diagnostic.npz", allow_pickle=False) as data:
        assert data["field__noise"].shape == (32, tr.n)
        assert data["field__key"].dtype != object
        assert data["field__next_key"].dtype != object
        assert data["raw_interaction__own"].shape == (32,)
        assert data["paired_difference__own"].shape == (3, 32)
        np.testing.assert_array_equal(data["paired_difference__own"],
                                      np.asarray(got.own[:, :32] - got.own[:, 32:]))
        assert all(data[name].dtype != object for name in data.files)
    metadata = json.loads((tmp_path / "scope_diagnostic.json").read_text())
    assert metadata["fitness_weights"] == {"own": 0.6, "relative": 0.4}
    assert set(metadata["scope_summaries"]) == {"M", "H", "J"}
    for scope in metadata["scope_summaries"].values():
        assert scope["own"]["pairs"] == 32
        assert scope["own"]["ties"] + scope["own"]["nonzero"] == 32


def test_scope_cli_preserves_existing_output_and_refuses_promotion(tmp_path):
    import subprocess
    theta = tmp_path / "initial.npy"
    np.save(theta, np.zeros(PO.N_PARAMS, np.float32))
    existing = tmp_path / "existing"
    existing.mkdir()
    marker = existing / "config.json"
    marker.write_text("preserve this existing run\n")
    fresh = tmp_path / "must_not_be_created"
    command = [sys.executable, os.path.join(ROOT, "scripts/train.py"),
               "--antithetic-scope-diagnostic", "--init-theta", str(theta),
               "--pop", "4096", "--episodes", "124", "--sigma", "0.01"]
    for out, flags, message in (
            (existing, [], "diagnostic output already exists"),
            (fresh, ["--promote"], "incompatible with --promote")):
        result = subprocess.run(command + ["--run", str(out)] + flags,
                                cwd=ROOT, capture_output=True, text=True,
                                timeout=30)
        assert result.returncode != 0
        assert message in result.stderr
    assert marker.read_text() == "preserve this existing run\n"
    assert sorted(p.name for p in existing.iterdir()) == ["config.json"]
    assert not fresh.exists()


def test_a_generation_leaves_dead_coordinates_untouched():
    # one tiny real generation on CPU (compiles the episode once)
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0, warm_frac=0.0), seed=0)
    before = np.asarray(tr.theta).copy()
    tr.generation()
    after = np.asarray(tr.theta)
    dead = PO.live_mask() == 0
    assert np.array_equal(before[dead], after[dead])
    assert not np.array_equal(before[~dead], after[~dead])


def test_trunk_warm_start_copies_only_the_encoder_trunk(tmp_path):
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import train as T
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0), seed=1)
    fresh = np.asarray(tr.theta).copy()
    old = np.full(PO.N_PARAMS, 7.0, np.float32)
    path = str(tmp_path / "old_theta.npy")
    np.save(path, old)
    T.warm_trunk(tr, path)
    got = np.asarray(tr.theta)
    assert T.TRUNK_BLOCKS == ("w1", "b1", "g1", "gb1", "dh")
    for name in T.TRUNK_BLOCKS:
        assert np.all(_block(got, name) == 7.0)
    # `ds` writes straight onto the grow and sell scores, so it is a head and
    # must not be inherited across a lineage break, `dh` being an input block.
    for name in ("w2", "b2", "g2", "gb2", "g3", "gb3", "w3", "b3", "g4", "gb4",
                 "g5", "gb5", "ds"):
        assert np.array_equal(_block(got, name), _block(fresh, name))
    # Ladder rung 0 is `Trainer.__init__`'s `[self.theta]`, so it has to follow
    # the warm start or the pool keeps an opponent this lineage never chose.
    assert np.array_equal(np.asarray(tr.pool[0]), got)


def test_trunk_warm_start_from_an_older_layout_leaves_the_new_block_fresh(tmp_path):
    """`--trunk-from` is how a fresh lineage inherits an encoder, and the theta
    it is pointed at is by definition older than the current layout -- every
    one on this machine is 3,892, 4,287 or 4,386 params long. A trunk block
    appended after that theta was written simply is not in the file; the fresh
    init has to stand rather than the load failing.
    """
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import train as T
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0), seed=1)
    fresh = np.asarray(tr.theta).copy()
    path = str(tmp_path / "legacy_theta.npy")
    np.save(path, np.full(PO.N_PARAMS_LEGACY, 7.0, np.float32))
    T.warm_trunk(tr, path)
    got = np.asarray(tr.theta)
    for name in ("w1", "b1", "g1", "gb1"):
        assert np.all(_block(got, name) == 7.0), name
    assert np.array_equal(_block(got, "dh"), _block(fresh, "dh"))


def test_trunk_warm_start_refuses_a_file_that_ends_inside_a_block(tmp_path):
    """A shorter *layout* ends between blocks; ending inside one is a truncated
    file, and copying the prefix would put half a matrix in the trunk."""
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import pytest
    import train as T
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0), seed=1)
    path = str(tmp_path / "truncated.npy")
    np.save(path, np.full(PO.offset("gb1") + 3, 7.0, np.float32))
    with pytest.raises(SystemExit, match="ends inside block gb1"):
        T.warm_trunk(tr, path)


def test_trunk_warm_start_refuses_something_that_is_not_a_theta(tmp_path):
    # A run directory's `pool.npy` is a *stack* of thetas and `state.npz` is an
    # archive; either one silently indexed as a flat vector would copy garbage
    # into the encoder trunk. Refuse on rank instead.
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import pytest
    import train as T
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0), seed=1)
    path = str(tmp_path / "pool.npy")
    np.save(path, np.zeros((12, PO.N_PARAMS), np.float32))
    with pytest.raises(SystemExit, match="flat theta vector"):
        T.warm_trunk(tr, path)


def test_init_theta_seats_the_init_theta_on_ladder_rung_0():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import train as T
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0), seed=1)
    fresh = np.asarray(tr.theta).copy()
    init = np.full(PO.N_PARAMS, 3.0, np.float32)
    T.install_init_theta(tr, init)
    assert np.array_equal(np.asarray(tr.theta), init)
    assert np.array_equal(np.asarray(tr.best_abs_theta), init)
    # Ladder rung 0 is `Trainer.__init__`'s `[self.theta]`: it has to be the
    # init theta, not the He-init nobody chose.
    assert np.array_equal(np.asarray(tr.pool[0]), init)
    assert not np.array_equal(np.asarray(tr.pool[0]), fresh)
