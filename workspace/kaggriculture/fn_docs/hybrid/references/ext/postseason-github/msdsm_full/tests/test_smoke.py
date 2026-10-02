"""Small CPU checks; no games, replay download or training run."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))


class SmokeChecks(unittest.TestCase):
    def test_cached_replay_integrity(self):
        import hashlib
        from types import SimpleNamespace
        from unittest.mock import patch
        from kaggriculture.data.prepare_replays import prepare

        engine = SimpleNamespace(action_legality=None, require_expected_engine=lambda: None)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            replay = root / "replay.json.gz"
            replay.write_bytes(b"original replay")
            digest = hashlib.sha256(replay.read_bytes()).hexdigest()
            row = {
                "episode_id": 1,
                "target_seat": 0,
                "target_submission_id": 2,
                "replay_path": replay.name,
                "replay_sha256": digest,
            }
            receipt = {"key": "2-1-0", "replay_sha256": digest}
            (root / "2-1-0.json").write_text(json.dumps(receipt))
            (root / "2-1-0.npz").touch()
            with patch.dict(sys.modules, {"kaggriculture.actions.legality": engine}):
                self.assertEqual(prepare((row, directory, directory)), receipt)
                replay.write_bytes(b"changed replay")
                with self.assertRaisesRegex(ValueError, "replay checksum mismatch"):
                    prepare((row, directory, directory))
                row["replay_sha256"] = hashlib.sha256(replay.read_bytes()).hexdigest()
                with self.assertRaisesRegex(ValueError, "cached replay differs"):
                    prepare((row, directory, directory))

    def test_public_ppo_config(self):
        from unittest.mock import patch
        from kaggriculture.training.ppo import parse_args, validate_run

        with patch.object(
            sys,
            "argv",
            [
                "train_ppo",
                "--config",
                str(ROOT / "configs/ppo.json"),
                "--bc-checkpoint",
                "unused.pkl",
                "--output-dir",
                "unused-run",
            ],
        ):
            args = parse_args()
        validate_run(args)
        self.assertEqual(args.games * args.horizon * 2, 92032)
        self.assertEqual(args.gae_lambda, 0.97)

    def test_tiny_policy_and_depth_growth(self):
        import jax
        import jax.numpy as jnp
        import numpy as np
        from dataclasses import replace
        from kaggriculture.agents.neural import prepare_fixed_batch
        from kaggriculture.model.policy import JaxModelConfig, initialize_params, add_zero_value_head, policy_forward
        from kaggriculture.model.growth import block_indices, identity_block, grow_tree
        from kaggriculture.observations.features import encode_observation
        from kaggriculture.search.reference_engine import Game

        model = JaxModelConfig(**json.loads((ROOT / "configs/model/smoke.json").read_text()))
        params = add_zero_value_head(initialize_params(jax.random.PRNGKey(0), model), model)
        observation = Game(seed=0).observation(0)
        batch = prepare_fixed_batch(encode_observation(observation), observation).arrays
        batch = jax.tree.map(jnp.asarray, batch)
        output = policy_forward(params, batch, model)
        self.assertEqual(output["unit_action"].shape, (1, 20, 500))
        self.assertEqual(output["market_action"].shape, (1, 10, 1903))
        grown_model = replace(model, layers=2)
        grown = grow_tree(params, (identity_block(grown_model, 1),), block_indices(1, 2))
        after = policy_forward(grown, batch, grown_model)
        for name in ("unit_action", "market_action", "value"):
            np.testing.assert_allclose(output[name], after[name], rtol=1e-5, atol=1e-5)
        from kaggriculture.training.checkpointing import save_params_payload
        from kaggriculture.agents.final import FinalAgent

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tiny.pkl"
            for variant in ("A", "B"):
                config = replace(model, sequential_patch=(variant == "B"))
                save_params_payload(path, params, config.to_dict(), 0)
                agent = FinalAgent(path, variant, heuristic_settings={"search_from_day": None}, warm=False)
                action = agent(observation)
                self.assertEqual(set(action), {"farmer", "hands", "market"})
                self.assertLessEqual(len(action["market"]), 10)
                if variant == "A":
                    self.assertFalse(agent.controller.failed)


if __name__ == "__main__":
    unittest.main()
