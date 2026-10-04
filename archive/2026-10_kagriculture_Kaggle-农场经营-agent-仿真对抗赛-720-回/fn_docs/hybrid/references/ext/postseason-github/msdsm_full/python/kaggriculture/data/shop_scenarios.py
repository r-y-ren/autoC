"""Training-only shop sequences; normal evaluation never uses these overrides."""

import importlib.util
import random
from pathlib import Path


def load_reference(path: Path):
    spec = importlib.util.spec_from_file_location("training_search_reference", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def shop_sequence(group: str, seed: int, names: list[str]) -> list[str] | None:
    if group == "normal":
        return None
    rng = random.Random(seed ^ 0x51A51)
    sequence = [rng.choice(sorted(names)) for _ in range(8)]
    if group == "tomato":
        forced = [rng.choice(["PIZZA_SHOP", "FARMERS_MARKET"]) for _ in range(2)]
    elif group == "extreme":
        forced = [rng.choice(sorted(names))] * rng.randint(3, 8)
    else:
        raise ValueError(f"unknown scenario: {group}")
    for position, shop in zip(rng.sample(range(8), len(forced)), forced, strict=True):
        sequence[position] = shop
    return sequence


def override_shops(town: dict, sequence: list[str] | None) -> None:
    if sequence is not None:
        count = len(town["unlocked_shops"])
        town["unlocked_shops"][:] = sequence[:count]
