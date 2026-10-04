"""Create a random policy compatible with BC, PPO and inference."""

import argparse
import json
from pathlib import Path
import _bootstrap  # noqa: F401


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    import jax
    import jax.numpy as jnp
    from kaggriculture.model.policy import JaxModelConfig, initialize_params, add_zero_value_head, parameter_count
    from kaggriculture.training.checkpointing import save_params_payload

    model = JaxModelConfig(**json.loads(args.config.read_text()))
    params = add_zero_value_head(initialize_params(jax.random.PRNGKey(args.seed), model), model)
    params["value"]["linear_cost"] = jnp.zeros(2, jnp.float32)
    save_params_payload(args.output, params, model.to_dict(), 0)
    print(json.dumps({"parameters": parameter_count(params), "output": str(args.output)}))


if __name__ == "__main__":
    main()
