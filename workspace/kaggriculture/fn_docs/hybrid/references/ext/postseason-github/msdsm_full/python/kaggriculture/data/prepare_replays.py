"""Build episode-grouped, resolver-filtered replay tensors for training."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np

from kaggriculture.actions.catalog import MARKET_ACTION_TO_ID, UNIT_ACTION_TO_ID, UNIT_QUANTITY_OPS
from kaggriculture.observations.features import FEATURE_DIM, encode_observation
from kaggriculture.observations.inventory_tracker import OpponentInventoryTracker
from kaggriculture.actions.sell_quantity import ABSOLUTE_START, NON_SELL_IDS, PRODUCTS, QUANTITY_COUNT

TOKENS, UNITS, SLOTS, IGNORE = 264, 20, 10, -100
NON_SELL_MAP = {old: new for new, old in enumerate(NON_SELL_IDS)}


def validation_episode(episode_id: int, seed: int = 50) -> bool:
    digest = hashlib.sha256(f"{seed}:{episode_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % 10 == 0


def label_actions(observation: dict, action: dict, legal: Any) -> np.ndarray:
    count = 1 + len(observation["farms"][observation["player"]].get("hands", []))
    hands = action.get("hands", [])
    units = [action.get("farmer", ["PASS"])] + [
        hands[index] if index < len(hands) else ["PASS"] for index in range(count - 1)
    ]
    labels = np.full(UNITS + SLOTS, IGNORE, np.int32)
    for index, order in enumerate(units[:UNITS]):
        if not legal.unit_mask[index]:
            continue
        order = order or ["PASS"]
        operation = order[0]
        try:
            key = (
                (operation, order[1], int(order[2]) if len(order) > 2 else 1)
                if operation in UNIT_QUANTITY_OPS
                else (operation, order[1])
                if operation == "PLANT"
                else (operation,)
            )
            labels[index] = UNIT_ACTION_TO_ID.get(key, IGNORE)
        except (IndexError, TypeError, ValueError):
            pass
    market = action.get("market", [])
    for index in range(SLOTS):
        order = market[index] if index < len(market) else ["NOOP"]
        order = order or ["NOOP"]
        if not legal.market_mask[index]:
            continue
        operation = order[0]
        try:
            if operation == "SELL":
                executed = int(legal.market_executed[index])
                if 1 <= executed <= QUANTITY_COUNT:
                    labels[UNITS + index] = ABSOLUTE_START + PRODUCTS.index(order[1]) * QUANTITY_COUNT + executed - 1
            elif operation in {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL"}:
                key = (operation, order[1], int(order[2]) if len(order) > 2 else 1)
                labels[UNITS + index] = NON_SELL_MAP.get(MARKET_ACTION_TO_ID.get(key, IGNORE), IGNORE)
            else:
                labels[UNITS + index] = NON_SELL_MAP.get(MARKET_ACTION_TO_ID.get((operation,), IGNORE), IGNORE)
        except (IndexError, TypeError, ValueError):
            pass
    return labels


def prepare(task: tuple[dict, str, str]) -> dict:
    from kaggriculture.actions.legality import action_legality, require_expected_engine

    row, manifest_directory, cache_directory = task
    require_expected_engine()
    episode = int(row["episode_id"])
    seat = int(row["target_seat"])
    submission = int(row["target_submission_id"])
    key = f"{submission}-{episode}-{seat}"
    cache = Path(cache_directory)
    receipt = cache / f"{key}.json"
    replay_path = Path(manifest_directory) / row["replay_path"]
    if hashlib.sha256(replay_path.read_bytes()).hexdigest() != row["replay_sha256"]:
        raise ValueError(f"replay checksum mismatch: {episode}")
    if receipt.is_file():
        cached = json.loads(receipt.read_text())
        if cached.get("replay_sha256") != row["replay_sha256"]:
            raise ValueError(f"cached replay differs from manifest; use a new cache directory: {episode}")
        if (cache / f"{key}.npz").is_file():
            return cached
    with gzip.open(replay_path, "rt") as stream:
        replay = json.load(stream)
    if replay.get("module_version") != "1.32.7" or len(replay["steps"]) != 720:
        raise ValueError(f"wrong engine or incomplete replay: {episode}")
    steps = replay["steps"]
    features = np.zeros((719, TOKENS, FEATURE_DIM), np.float16)
    labels = np.full((719, UNITS + SLOTS), IGNORE, np.int16)
    tracker = OpponentInventoryTracker(observer_player=seat)
    for turn in range(719):
        observation = steps[turn][seat]["observation"]
        if turn:
            tracker.update(steps[turn - 1][seat]["observation"], observation, steps[turn][seat].get("action", {}))
        actions = [state.get("action", {}) for state in steps[turn + 1]]
        encoded = encode_observation(observation, tracker.estimate())
        features[turn, : len(encoded.features)] = encoded.features
        labels[turn] = label_actions(
            observation,
            actions[seat] or {},
            action_legality([state["observation"] for state in steps[turn]], actions, seat),
        )
    destination = cache / f"{key}.npz"
    temporary = destination.with_suffix(".tmp")
    with temporary.open("wb") as stream:
        np.savez_compressed(stream, features=features, labels=labels)
    os.replace(temporary, destination)
    result = {
        "key": key,
        "episode_id": episode,
        "submission_id": submission,
        "seat": seat,
        "split": "validation" if validation_episode(episode) else "train",
        "samples": 719,
        "valid_labels": int(np.sum(labels != IGNORE)),
        "ignored_labels": int(np.sum(labels == IGNORE)),
        "replay_sha256": row["replay_sha256"],
    }
    temporary = receipt.with_suffix(".tmp")
    temporary.write_text(json.dumps(result, sort_keys=True) + "\n")
    os.replace(temporary, receipt)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--submission", type=int, action="append", help="Explicit allowed submission IDs")
    args = parser.parse_args()
    expected_submissions = set(args.submission) if args.submission else None
    args.cache.mkdir(parents=True, exist_ok=True)
    tasks = []
    manifest_hashes = {}
    seen = set()
    for path in args.manifest:
        manifest = json.loads(path.read_text())
        submission = int(manifest["source"]["submission_id"])
        if expected_submissions is not None and submission not in expected_submissions:
            raise ValueError(f"unexpected replay source: {submission}")
        manifest_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        for row in manifest["episodes"]:
            identity = int(row["episode_id"]), int(row["target_seat"])
            if identity not in seen:
                seen.add(identity)
                tasks.append((row, str(path.parent), str(args.cache)))
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        rows = list(executor.map(prepare, tasks))
    splits = {row["split"] for row in rows}
    if splits != {"train", "validation"}:
        raise ValueError(f"replay split is incomplete: {splits}")
    index = {"schema_version": 1, "seed": 50, "manifests": manifest_hashes, "episodes": rows}
    temporary = args.cache / "index.tmp"
    temporary.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.cache / "index.json")
    print(
        json.dumps(
            {"episodes": len(rows), "splits": {split: sum(r["split"] == split for r in rows) for split in splits}}
        )
    )


if __name__ == "__main__":
    main()
