"""Frozen-policy, cached-feature critic warmup before self-play PPO."""

from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
from types import SimpleNamespace
import jax
import jax.numpy as jnp
import numpy as np
import optax
from kaggriculture.config import parse_config_args
from kaggriculture.model.policy import cast_dense_params, dense, policy_forward
from kaggriculture.training.sharding import flatten_pmap_batch, put_replicated, shard_batch
from kaggriculture.training.objectives import PPOConfig, make_optimizer, paired_zero_sum_values
from kaggriculture.training.rollout import collect_self_play, generalized_advantage_estimate, make_sampler
from kaggriculture.training.ppo import critic_validation_metrics, load_bc_checkpoint, update_early_stopping
from kaggriculture.training.checkpointing import actor_hash, atomic_pickle, policy_hash, save_params_payload

INPUT_NAMES = ("value_features", "value_cost_difference", "value_time")


def cached_values(value: dict, inputs: dict) -> jax.Array:
    hidden = dense(inputs["value_features"], value["hidden"], jnp.float32)
    hidden = jax.nn.gelu(hidden, approximate=False)
    logits = dense(hidden, value["output"], jnp.float32)[..., 0]
    w0, w1 = value["linear_cost"]
    logits += (w0 + w1 * inputs["value_time"]) * inputs["value_cost_difference"]
    return paired_zero_sum_values(logits)


def head_loss(value: dict, inputs: dict, targets: jax.Array) -> jax.Array:
    return 0.5 * jnp.mean(optax.huber_loss(cached_values(value, inputs), targets, delta=1.0))


def make_scan(optimizer: optax.GradientTransformation):
    @jax.jit
    def update(value: dict, adam: tuple, inputs: dict, targets: jax.Array):
        def step(carry, batch):
            params, state = carry
            features, returns = batch
            loss, gradients = jax.value_and_grad(head_loss)(params, features, returns)
            updates, state = optimizer.update(gradients, state, params)
            return (optax.apply_updates(params, updates), state), (loss, optax.global_norm(gradients))

        return jax.lax.scan(step, (value, adam), (inputs, targets), reverse=True)

    return update


def make_encoder(params: dict, model, devices: tuple):
    cast = cast_dense_params(params, jnp.float32)

    def encode(weights, batch):
        out = policy_forward(weights, batch, model, dtype=jnp.float32, return_value_inputs=True)
        return {name: out[name] for name in INPUT_NAMES}

    if len(devices) == 1:
        compiled = jax.jit(encode)
        return lambda batch: compiled(cast, batch)
    weights = put_replicated(cast, devices)
    compiled = jax.pmap(encode, devices=devices)

    def parallel(batch):
        result = compiled(weights, shard_batch(batch, devices))
        return jax.tree.map(flatten_pmap_batch, result)

    return parallel


def collect_features(params: dict, model, config: dict, index: int, devices: tuple) -> tuple[dict, dict]:
    games = config["validation_games"] if index < 0 else config["games"]
    seed = config["validation_seed"] if index < 0 else config["training_seed"] + index * games
    rng = jax.random.PRNGKey(config["seed"])
    rng = jax.random.fold_in(rng, 0x56414C if index < 0 else index)
    started = time.monotonic()
    sampler = make_sampler(model, jnp.float32, devices)
    rollout, _ = collect_self_play(
        params,
        model,
        games=games,
        horizon=config["horizon"],
        seed_counter=seed,
        rng=rng,
        compute_dtype=jnp.float32,
        gamma=1.0,
        gae_lambda=0.97,
        sampler=sampler,
        inference_batch_size=config["games"] * 2,
    )
    collected = time.monotonic()
    encoder = make_encoder(params, model, devices)
    arrays = {
        "value_features": np.empty((rollout.transitions, model.d_model), np.float32),
        "value_cost_difference": np.empty(rollout.transitions, np.float32),
        "value_time": np.empty(rollout.transitions, np.float32),
    }
    batch_size = config["games"] * 2
    for start in range(0, rollout.transitions, batch_size):
        selected = np.arange(start, min(start + batch_size, rollout.transitions))
        valid = len(selected)
        if valid < batch_size:
            selected = np.pad(selected, (0, batch_size - valid), mode="wrap")
        batch = {name: values[selected] for name, values in rollout.states.items()}
        result = jax.device_get(encoder(batch))
        for name in INPUT_NAMES:
            arrays[name][start : start + valid] = result[name][:valid]
    arrays["money"] = rollout.money
    timings = {"rollout_seconds": collected - started, "encode_seconds": time.monotonic() - collected}
    # A real batch verifies the frozen-trunk decomposition before any cache is published.
    batch = {name: values[:batch_size] for name, values in rollout.states.items()}
    direct = jax.jit(lambda p, b: paired_zero_sum_values(policy_forward(p, b, model)["value"]))(params, batch)
    cached = cached_values(params["value"], {name: jnp.asarray(arrays[name][: len(direct)]) for name in INPUT_NAMES})
    timings["value_max_abs_error"] = float(jnp.max(jnp.abs(direct - cached)))
    if timings["value_max_abs_error"] > 2e-4:
        raise RuntimeError(f"cached critic differs from direct forward: {timings}")
    return arrays, timings


def diagnostics(arrays: dict, values: np.ndarray, config: dict, games: int) -> dict:
    rollout = SimpleNamespace(
        games=games, horizon=config["horizon"], money=arrays["money"], transitions=games * config["horizon"] * 2
    )
    return critic_validation_metrics(rollout, values.reshape(-1), np.arange(rollout.transitions), huber_delta=1.0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--games", type=int, default=64)
    parser.add_argument("--validation-games", type=int, default=16)
    parser.add_argument("--horizon", type=int, default=719)
    parser.add_argument("--max-updates", type=int, default=100)
    parser.add_argument("--patience", type=int, default=8)
    parser.add_argument("--training-seed", type=int, default=20_000_000)
    parser.add_argument("--validation-seed", type=int, default=30_000_000)
    parser.add_argument("--seed", type=int, default=51)
    args = parse_config_args(parser)
    if min(args.games, args.validation_games, args.max_updates, args.patience) < 1 or args.horizon != 719:
        parser.error("critic warmup requires positive counts and the full 719-step horizon")
    train_stop = args.training_seed + args.games * args.max_updates
    val_stop = args.validation_seed + args.validation_games
    if args.training_seed < val_stop and args.validation_seed < train_stop:
        parser.error("training and validation seeds must be disjoint")
    if (args.output / "critic_best_jax.pkl").exists():
        parser.error("use a new critic output directory")
    args.output.mkdir(parents=True, exist_ok=True)
    config = {
        k: getattr(args, k)
        for k in (
            "games",
            "validation_games",
            "horizon",
            "max_updates",
            "patience",
            "training_seed",
            "validation_seed",
            "seed",
        )
    }
    params, model = load_bc_checkpoint(args.policy)
    if "linear_cost" not in params["value"]:
        parser.error("critic needs the money-prior parameters; initialize with scripts/init_model.py")
    source_hash = policy_hash(params)
    actor = actor_hash(params)
    devices = tuple(jax.local_devices())
    optimizer = make_optimizer(PPOConfig(learning_rate=1e-4, adam_epsilon=1e-5, gradient_norm=5, value_coefficient=0.5))
    value, adam = params["value"], optimizer.init(params["value"])
    validation, _ = collect_features(params, model, config, -1, devices)
    validation_inputs = {name: jnp.asarray(validation[name]) for name in INPUT_NAMES}
    predict, update = jax.jit(cached_values), make_scan(optimizer)
    baseline = diagnostics(validation, np.asarray(predict(value, validation_inputs)), config, args.validation_games)
    best_loss, stale, best_update = baseline["huber_loss"], 0, 0

    def save_best(completed: int):
        fitted = {**params, "value": value}
        if actor_hash(fitted) != actor:
            raise RuntimeError("critic warmup changed the frozen actor")
        atomic_pickle(
            args.output / "critic_best_jax.pkl",
            {
                "critic_params": jax.device_get(fitted),
                "model_config": model.to_dict(),
                "policy_sha256": source_hash,
                "completed_updates": completed,
                "validation_loss": best_loss,
            },
        )
        save_params_payload(args.output / "policy_with_critic.pkl", fitted, model.to_dict(), 0)

    save_best(0)
    for index in range(args.max_updates):
        arrays, timings = collect_features(params, model, config, index, devices)
        features = {name: jnp.asarray(arrays[name]) for name in INPUT_NAMES}
        predictions = np.asarray(predict(value, features))
        outcomes = np.sign(arrays["money"][:, 0] - arrays["money"][:, 1]).astype(np.float32)
        terminal = np.stack((outcomes, -outcomes), axis=-1)
        targets, _ = generalized_advantage_estimate(
            predictions,
            terminal,
            horizon=args.horizon,
            games=args.games,
            gamma=1.0,
            gae_lambda=0.97,
        )
        inputs = {
            name: data.reshape((args.horizon, args.games * 2, *data.shape[1:])) for name, data in features.items()
        }
        (value, adam), (losses, _) = update(value, adam, inputs, jnp.asarray(targets).reshape(args.horizon, -1))
        if not all(np.isfinite(np.asarray(x)).all() for x in jax.tree.leaves((value, adam))):
            raise RuntimeError("nonfinite critic update")
        report = diagnostics(validation, np.asarray(predict(value, validation_inputs)), config, args.validation_games)
        best_loss, stale, improved = update_early_stopping(best_loss, stale, report["huber_loss"], 1e-5)
        if improved:
            best_update = index + 1
            save_best(best_update)
        row = {
            "update": index + 1,
            "best_update": best_update,
            "validation": report,
            "mean_loss": float(jnp.mean(losses)),
            **timings,
        }
        with (args.output / "metrics.jsonl").open("a") as stream:
            stream.write(json.dumps(row) + "\n")
        print(json.dumps(row), flush=True)
        if stale >= args.patience:
            break


if __name__ == "__main__":
    main()
