"""Losslessly compact the Rust independent masks; expand only on the accelerator."""

from __future__ import annotations

from typing import Any

import numpy as np

from kaggriculture.actions.catalog import MARKET_ACTIONS, UNIT_ACTIONS

MAX_UNITS = 20
MASKED_LOGIT = -1e9


def catalog_stems(actions: tuple) -> tuple[tuple, np.ndarray, np.ndarray]:
    stems = tuple(dict.fromkeys(action[:2] for action in actions))
    mapping = np.asarray([stems.index(action[:2]) for action in actions], dtype=np.int32)
    representatives = np.asarray([int(np.flatnonzero(mapping == index)[0]) for index in range(len(stems))])
    return stems, mapping, representatives


UNIT_STEMS, UNIT_STEM_INDEX, UNIT_REPRESENTATIVES = catalog_stems(UNIT_ACTIONS)
MARKET_STEMS, MARKET_STEM_INDEX, MARKET_REPRESENTATIVES = catalog_stems(MARKET_ACTIONS)
UNIT_STEM_SIZE = MAX_UNITS * len(UNIT_STEMS)
MASK_STEM_SIZE = UNIT_STEM_SIZE + len(MARKET_STEMS)
MASK_STATE_NAMES = ("legal_mask_stems",)
assert (len(UNIT_STEMS), len(MARKET_STEMS), MASK_STEM_SIZE) == (44, 22, 902)


class ActionMaskWorkspace:
    def __init__(self, rows: int, *, pin: bool = False, parallel: bool = False) -> None:
        self.unit_dense = np.empty((rows, MAX_UNITS, len(UNIT_ACTIONS)), dtype=np.bool_)
        self.market_dense = np.empty((rows, len(MARKET_ACTIONS)), dtype=np.bool_)
        self.stems = np.empty((rows, MASK_STEM_SIZE), dtype=np.bool_)
        self.units = self.stems[:, :UNIT_STEM_SIZE].reshape(rows, MAX_UNITS, len(UNIT_STEMS))
        self.market = self.stems[:, UNIT_STEM_SIZE:]
        self.parallel = parallel
        self.registration = None
        if pin:
            from kaggriculture.training.host_memory import register_host_array

            self.registration = register_host_array(self.stems)

    def write(self, environments: Any, players: np.ndarray | None = None) -> np.ndarray:
        if isinstance(environments, list):
            if players is not None or self.stems.shape[0] != 2 * len(environments):
                raise ValueError("list mask writer requires both seats of every environment")
            for game, environment in enumerate(environments):
                environment.write_action_masks_both(
                    self.unit_dense[2 * game : 2 * game + 2], self.market_dense[2 * game : 2 * game + 2]
                )
        elif players is None:
            environments.write_action_masks_both(self.unit_dense, self.market_dense, parallel=self.parallel)
        else:
            environments.write_action_masks_players(players, self.unit_dense, self.market_dense, parallel=self.parallel)
        np.take(self.unit_dense, UNIT_REPRESENTATIVES, axis=-1, out=self.units)
        np.take(self.market_dense, MARKET_REPRESENTATIVES, axis=-1, out=self.market)
        return self.stems


def apply_unit_masks(outputs: dict[str, Any], batch: dict[str, Any]) -> dict[str, Any]:
    import jax.numpy as jnp

    units = batch["legal_mask_stems"][:, :UNIT_STEM_SIZE].reshape(-1, MAX_UNITS, len(UNIT_STEMS))
    mask = jnp.take(units, jnp.asarray(UNIT_STEM_INDEX), axis=-1)
    masked = {
        **outputs,
        "unit_action": jnp.where(mask, outputs["unit_action"].astype(jnp.float32), MASKED_LOGIT),
        "unit_legal_count": mask.sum(axis=-1),
    }
    if "market_action" in outputs:
        # The market head is not masked here; the entropy normaliser still reads a per-slot count.
        market = outputs["market_action"]
        masked["market_legal_count"] = jnp.full(market.shape[:2], market.shape[-1], dtype=jnp.int32)
    return masked


def apply_action_masks(outputs: dict[str, Any], batch: dict[str, Any]) -> dict[str, Any]:
    import jax.numpy as jnp

    stems = batch["legal_mask_stems"].astype(jnp.bool_)
    units = stems[:, :UNIT_STEM_SIZE].reshape(-1, MAX_UNITS, len(UNIT_STEMS))
    market = stems[:, UNIT_STEM_SIZE:]
    unit_mask = jnp.take(units, jnp.asarray(UNIT_STEM_INDEX), axis=-1)
    market_mask = jnp.take(market, jnp.asarray(MARKET_STEM_INDEX), axis=-1)[:, None, :]
    return {
        **outputs,
        "unit_action": jnp.where(unit_mask, outputs["unit_action"].astype(jnp.float32), MASKED_LOGIT),
        "market_action": jnp.where(market_mask, outputs["market_action"].astype(jnp.float32), MASKED_LOGIT),
        "unit_legal_count": unit_mask.sum(axis=-1),
        "market_legal_count": market_mask.sum(axis=-1),
    }


def observation_mask_stems(observation: dict[str, Any], config: dict[str, Any] | None = None) -> np.ndarray:
    """Official-observation path for debug/submission; never used by Rust PPO rollouts."""
    from kaggle_environments.envs.kaggriculture import kaggriculture as rules

    config = {} if config is None else config
    result = np.zeros((1, MASK_STEM_SIZE), dtype=np.bool_)
    units = result[0, :UNIT_STEM_SIZE].reshape(MAX_UNITS, len(UNIT_STEMS))
    market = result[0, UNIT_STEM_SIZE:]
    unit_index = {stem: index for index, stem in enumerate(UNIT_STEMS)}
    units[:, unit_index[("PASS",)]] = True
    market[0] = True
    step = int(observation.get("step", 0))
    if step >= config.get("episodeSteps", 720) - 1:
        return result
    farm = observation["farms"][int(observation["player"])]
    private = observation["private"]
    shed, seeds = private["shed"], private["seeds"]
    board_size = config.get("boardSize", 10)
    room = sum(shed.values()) < config.get("shedCapacity", 100)
    day = step // config.get("turnsPerDay", 24)
    positions = [farm["farmer"], *farm["hands"]]
    for unit, (x, y) in enumerate(positions[:MAX_UNITS]):
        tile = farm["tiles"][y][x]
        inventory = private["inventories"][unit]
        adjacent = rules._is_shed_adjacent((x, y), board_size)
        for operation, (dx, dy) in rules.FARMER_MOVES.items():
            units[unit, unit_index[(operation,)]] = 0 <= x + dx < board_size and 0 <= y + dy < board_size
        units[unit, unit_index[("DROP",)]] = adjacent and bool(inventory)
        for stem, index in unit_index.items():
            operation = stem[0]
            if operation == "PICKUP":
                units[unit, index] = adjacent and shed.get(stem[1], 0) > 0
            elif operation == "PLACE":
                item = stem[1]
                matching = (
                    item in rules.ANIMALS
                    and isinstance(tile, dict)
                    and "animal" not in tile
                    and tile.get("kind") == rules.ANIMALS[item]["structure"]
                )
                units[unit, index] = inventory.get(item, 0) > 0 and (matching or (adjacent and room))
            elif operation == "PLANT":
                units[unit, index] = tile is None and seeds.get(stem[1], 0) > 0
        if tile is None:
            units[unit, unit_index[("BUILD_COOP",)]] = True
            units[unit, unit_index[("BUILD_PASTURE",)]] = True
        elif isinstance(tile, dict):
            animal = "animal" in tile
            plant = tile.get("kind") == "PLANT"
            units[unit, unit_index[("DIG",)]] = not animal
            if plant:
                units[unit, unit_index[("WATER",)]] = not tile["watered_today"]
                units[unit, unit_index[("HARVEST",)]] = (
                    tile["yield_units"] > 0
                    and day - tile["planted_day"] >= rules.CROPS[tile["crop"]]["first_yield_day"]
                )
                units[unit, unit_index[("FERTILIZE",)]] = inventory.get("FERTILIZER", 0) > 0
            elif animal:
                units[unit, unit_index[("HARVEST",)]] = tile["yield_units"] > 0
                units[unit, unit_index[("FEED",)]] = not tile["fed_today"] and inventory.get("WHEAT", 0) > 0
                units[unit, unit_index[("CARE",)]] = not tile["cared_today"]
                units[unit, unit_index[("COLLECT_FERTILIZER",)]] = tile["fertilizer_available"]
    money = farm["money"]
    public_market = observation["market"]
    for index, stem in enumerate(MARKET_STEMS):
        op = stem[0]
        if op == "BUY_SEED":
            market[index] = money >= rules.CROPS[stem[1]]["seed"]
        elif op == "BUY_PRODUCT":
            market[index] = room and money >= rules.market_price(
                stem[1], public_market["inventory"][stem[1]] - 1, public_market.get("params")
            )
        elif op == "BUY_ANIMAL":
            market[index] = room and money >= rules.ANIMALS[stem[1]]["cost"]
        elif op == "SELL":
            market[index] = shed.get(stem[1], 0) > 0
        elif op == "HIRE":
            market[index] = money >= config.get("farmHandCostMult", 1) * rules._fib(farm["hires_today"])
        elif op == "BUY_LAND":
            extra = len(farm["unlocked_quadrants"]) - 1
            market[index] = extra < len(rules.LAND_PRICES) and money >= rules.LAND_PRICES[extra]
    return result
