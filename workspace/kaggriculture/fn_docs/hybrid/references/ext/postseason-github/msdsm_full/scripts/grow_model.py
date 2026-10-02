"""Grow network depth while preserving the policy at initialization."""

import argparse
from dataclasses import replace
import json
from pathlib import Path
import _bootstrap  # noqa: F401


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--layers", type=int, required=True)
    parser.add_argument("--seed", type=int, default=48)
    parser.add_argument(
        "--preserve-optimizer", action="store_true", help="requires a full PPO checkpoint at an update boundary"
    )
    args = parser.parse_args()
    from kaggriculture.checkpoints import load_training_source
    from kaggriculture.model.policy import JaxModelConfig, parameter_count
    from kaggriculture.model.growth import block_indices, identity_block, grow_tree, grow_payload
    from kaggriculture.training.checkpointing import atomic_pickle, save_params_payload

    payload = load_training_source(args.checkpoint)
    previous = JaxModelConfig(**payload["model_config"])
    if previous.dropout:
        raise ValueError("function-preserving growth requires dropout=0")
    model = replace(previous, layers=args.layers)
    indices = block_indices(previous.layers, model.layers)
    if args.preserve_optimizer:
        grown, receipt = grow_payload(payload, model, seed=args.seed)
        atomic_pickle(args.output, grown)
    else:
        additions = tuple(identity_block(model, args.seed + i) for i in range(model.layers - previous.layers))
        params = grow_tree(payload["state"]["params"], additions, indices)
        save_params_payload(args.output, params, model.to_dict(), 0)
        receipt = {
            "layers": [previous.layers, model.layers],
            "parameters": parameter_count(params),
            "optimizer": "fresh on next PPO launch",
        }
    args.output.with_suffix(".growth.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
