"""Unit-action rules applied at decode time: no fertilizer without gain, no same-tile duplicates.

The neural policy decodes each unit's action by an independent argmax over its 500 logits, with no
legal mask at inference (`legal_mask: False` in the shipped configs). Two kinds of waste follow,
and both are decided by the observation and the turn's other choices alone:

* **Fertilizer without gain.** FERTILIZE consumes a fertilizer whenever the unit holds one and
  stands on a plant, even when it changes nothing (`fast_env._apply_unit_action`: it only extends
  `fertilized_until_day`). It is masked when no covered day can raise a yield: already covered, no
  watering window (wheat, carrot, melon) or production night (tomato, strawberry) in the three days,
  or a bulk crop within one unit of its cap, where +2 and +1 land on the same cap.
* **Same-tile duplicates.** Two units on one tile issuing the same tile action in one turn: the
  engine lets the first act and the second does nothing (a second FERTILIZE still spends a
  fertilizer). Every unit reads the same observation, so an independent argmax cannot see the other.
  The unit whose probability for the action is highest keeps it; the others take their next-ranked
  action that is neither masked nor already claimed on that tile.

* **Seeds.** A turn whose PLANTs of a crop outnumber its seeds voids every one of them. Only that
  many PLANTs are kept, most probable first; a unit left without a seed PASSes on its tile and its
  seed is bought in the same turn's market (it arrives for the next turn), for crops that can still
  be harvested.
* **Care without a later production night.** CARE only banks a bonus for the animal's next
  production night after today (`fast_env._daily_refresh_animals` adds it after tonight's
  production), and the last night whose output can be collected is day 28's. CARE is masked when
  no such night is left, or when it does nothing at all (no animal, already cared for today).
* **Moves off the board.** The engine ignores them.

With no rule firing the result is the original argmax, ties included (stable ordering), so
`decide` reproduces `GreedyJaxPolicy.__call__` exactly on every other turn.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np

TURNS_PER_DAY = 24
LAST_DAY = 29
MARKET_SLOTS = 10
CROPS = {
    "WHEAT": {"first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT": {"first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO": {"first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON": {"first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
ANIMAL_CYCLE = {"GOOSE": (4, 1), "COW": (8, 2), "SHEEP": (6, 3)}  # (first_yield_day, interval)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
# The rules that can be switched off one by one (kagg_patch config.json); every function defaults to all.
RULES = frozenset({"fertilize_mask", "same_tile", "seed_stock", "care_mask", "offboard_mask"})
# Tile actions the engine lets act once per tile per turn; the value groups those that exclude each other.
EXCLUSIVE = {
    "WATER": "WATER",
    "FERTILIZE": "FERTILIZE",
    "HARVEST": "HARVEST",
    "DIG": "DIG",
    "BUILD_COOP": "BUILD",
    "BUILD_PASTURE": "BUILD",
    "PLANT": "PLANT",
    "CARE": "CARE",
    "FEED": "FEED",
    "COLLECT_FERTILIZER": "COLLECT_FERTILIZER",
}


def fertilize_gains(tile: Any, day: int) -> bool:
    """Whether a FERTILIZE on `tile` today can raise any yield the season can still collect."""
    if not (isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") in CROPS):
        return False
    crop = CROPS[tile["crop"]]
    covered = int(tile.get("fertilized_until_day", -1))
    planted = int(tile["planted_day"])
    for covered_day in range(day, day + 3):
        if covered_day <= covered or covered_day > LAST_DAY:
            continue
        age = covered_day - planted
        if not crop["ongoing"]:
            in_window = (crop["max_yield_day"] + 1) // 2 <= age <= crop["max_yield_day"]
            watered_already = covered_day == day and tile.get("watered_today")
            # Bulk crops only lose units at harvest, so today's yield bounds every later one from below.
            at_cap = int(tile.get("yield_units", 0)) >= crop["max_yield"] - 1
            if in_window and not watered_already and not at_cap:
                return True
            continue
        # A production night adds its units at the end of the covered day, collectable the next day.
        since_first = covered_day + 1 - planted - crop["first_yield_day"]
        productive = since_first >= 0 and since_first % crop["interval"] == 0
        if productive and since_first // crop["interval"] + 1 <= crop["max_yield"] and covered_day < LAST_DAY:
            return True
    return False


def care_gains(tile: Any, day: int) -> bool:
    """Whether a CARE today banks a bonus that a production night the season can collect will pay."""
    if isinstance(tile, dict) and tile.get("kind") in ("COOP", "PASTURE") and "animal" not in tile:
        # An earlier unit may place an animal here in this same turn; the engine applies units in order.
        return True
    if not (isinstance(tile, dict) and tile.get("animal") in ANIMAL_CYCLE) or tile.get("cared_today"):
        return False
    first, interval = ANIMAL_CYCLE[tile["animal"]]
    placed = int(tile["placed_day"])
    # The night of day n produces when n + 1 - placed - first is a non-negative multiple of the interval.
    return any(
        night + 1 - placed - first >= 0 and (night + 1 - placed - first) % interval == 0
        for night in range(day + 1, LAST_DAY)
    )


def exclusive_key(order: list[Any], position: tuple[int, int], tile: Any = None) -> tuple[Any, ...] | None:
    """The (tile, group) an action claims for the turn, or None when several units may share it."""
    operation = str(order[0])
    if operation in EXCLUSIVE:
        return (*position, EXCLUSIVE[operation])
    placing_animal = (
        operation == "PLACE"
        and len(order) >= 2
        and order[1] in ANIMAL_STRUCTURE
        and isinstance(tile, dict)
        and tile.get("kind") == ANIMAL_STRUCTURE[order[1]]
        and "animal" not in tile
    )
    return (*position, "PLACE_ANIMAL") if placing_animal else None


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=-1, keepdims=True)
    weights = np.exp(shifted)
    return weights / weights.sum(axis=-1, keepdims=True)


def choose_unit_actions(
    observation: dict[str, Any],
    logits: np.ndarray,
    vocabulary: tuple,
    shortfall: dict[str, int] | None = None,
    blocked_moves: list[set[str]] | None = None,
    enabled: frozenset[str] = RULES,
) -> list[list[Any]]:
    """Per-unit argmax with the fertilizer mask, then same-tile duplicates and seed stock by probability.

    `enabled` names the rules in force (`RULES`); with none of them the result is the plain argmax.

    `blocked_moves[unit]` names moves masked for that unit on top of the state rules (the
    oscillation experiment passes the reverse of a move the unit made last turn).

    Seeds: the engine voids every PLANT of a crop in a turn whose PLANTs outnumber that crop's seeds
    (`FastEnv._apply_player_actions`). Only as many PLANTs as there are seeds are kept, the most
    probable first; a unit left without a seed PASSes on its tile rather than taking another action,
    so it is still there when the seed arrives, and is counted into `shortfall`, which
    `finish_action` buys in the same turn's market (the market settles after the units act, so the
    seed is there for the next turn).
    """
    player = int(observation["player"])
    farm = observation["farms"][player]
    tiles = farm["tiles"]
    positions = [tuple(farm["farmer"]), *(tuple(hand) for hand in farm["hands"])][: len(logits)]
    inventories = observation.get("private", {}).get("inventories") or []
    seeds = {str(crop): int(n) for crop, n in (observation.get("private", {}).get("seeds") or {}).items()}
    planted: dict[str, int] = {}
    shortfall = shortfall if shortfall is not None else {}
    # Kaggle's second seat receives no "step" key; "day" is in both seats' observations.
    day = int(observation["day"]) if "day" in observation else int(observation["step"]) // TURNS_PER_DAY
    fertilize = vocabulary.index(("FERTILIZE",))
    care = vocabulary.index(("CARE",))
    moves = {index: MOVES[action[0]] for index, action in enumerate(vocabulary) if action[0] in MOVES}
    size = len(tiles)

    logits = np.asarray(logits, dtype=np.float64)
    probabilities = _softmax(logits)
    rankings = np.argsort(-logits, axis=-1, kind="stable")
    tile_of = [tiles[y][x] for x, y in positions]
    masked = []
    for unit, (x, y) in enumerate(positions):
        holds_fertilizer = int((inventories[unit] if unit < len(inventories) else {}).get("FERTILIZER", 0)) > 0
        unit_masked: set[int] = set()
        if "offboard_mask" in enabled:
            unit_masked |= {i for i, (dx, dy) in moves.items() if not (0 <= x + dx < size and 0 <= y + dy < size)}
        if "fertilize_mask" in enabled and not (holds_fertilizer and fertilize_gains(tile_of[unit], day)):
            unit_masked.add(fertilize)
        if "care_mask" in enabled and not care_gains(tile_of[unit], day):
            unit_masked.add(care)
        if blocked_moves is not None and unit < len(blocked_moves):
            unit_masked |= {index for index, action in enumerate(vocabulary) if action[0] in blocked_moves[unit]}
        masked.append(unit_masked)

    def allowed(unit: int, action_id: int) -> bool:
        return action_id not in masked[unit]

    first = [next(int(a) for a in rankings[unit] if allowed(unit, int(a))) for unit in range(len(positions))]
    # Highest confidence claims first, so a contested tile goes to the unit most sure of it.
    sequence = sorted(range(len(positions)), key=lambda unit: (-probabilities[unit, first[unit]], unit))
    claimed: set[tuple[Any, ...]] = set()
    chosen: list[list[Any]] = [["PASS"]] * len(positions)
    for unit in sequence:
        for action_id in rankings[unit]:
            action_id = int(action_id)
            if not allowed(unit, action_id):
                continue
            action = list(vocabulary[action_id])
            key = exclusive_key(action, positions[unit], tile_of[unit]) if "same_tile" in enabled else None
            if key is not None and key in claimed:
                continue
            if "seed_stock" in enabled and action[0] == "PLANT" and len(action) >= 2:
                crop = str(action[1])
                if planted.get(crop, 0) >= seeds.get(crop, 0):
                    # No seed left for this unit: it waits on its tile, and the seed is bought now.
                    shortfall[crop] = shortfall.get(crop, 0) + 1
                    chosen[unit] = ["PASS"]
                    break
                planted[crop] = planted.get(crop, 0) + 1
            if key is not None:
                claimed.add(key)
            chosen[unit] = action
            break
    return chosen


def add_seed_purchases(market: list[list[Any]], shortfall: dict[str, int], day: int) -> list[list[Any]]:
    """Make the turn's BUY_SEED orders cover the shortfall, for crops still harvestable this season."""
    market = [list(order) for order in market]
    for crop, needed in sorted(shortfall.items()):
        if crop not in CROPS or day + CROPS[crop]["first_yield_day"] > LAST_DAY or needed <= 0:
            continue
        orders = [order for order in market if order[0] == "BUY_SEED" and order[1] == crop]
        missing = needed - sum(int(order[2]) for order in orders)
        if missing <= 0:
            continue
        if orders:
            orders[0][2] = int(orders[0][2]) + missing
        elif len(market) < MARKET_SLOTS:
            market.append(["BUY_SEED", crop, missing])
    return market


def decide(
    policy: Any, observation: dict[str, Any], runtime: Any = None, enabled: frozenset[str] = RULES
) -> dict[str, Any]:
    """`GreedyJaxPolicy.__call__` with the unit decode replaced by `choose_unit_actions`.

    `runtime` (`kagg_patch.Runtime`, or `pipeline/runtime_adapter.Runtime` in evaluation) plays the
    bundle's own format, including its own last-step action, which that format's policy plays before
    any forward pass. `enabled` names the rules in force.
    """
    import jax
    import jax.numpy as jnp

    if runtime is not None:
        final = runtime.final_turn_action(observation)
        if final is not None:
            policy.previous_observation = deepcopy(observation)
            policy.previous_action = deepcopy(final)
            return final
        if policy.config.legal_mask:
            raise NotImplementedError("legal masks are only wired for the neural format")
        encode_observation, prepare_fixed_batch = runtime.encode_observation, runtime.prepare_fixed_batch
        vocabulary = runtime.UNIT_ACTIONS
    else:
        from kaggriculture.actions.masks import observation_mask_stems
        from kaggriculture.actions.catalog import UNIT_ACTIONS as vocabulary
        from kaggriculture.observations.features import encode_observation
        from kaggriculture.agents.neural import prepare_fixed_batch

    estimate = policy._inventory_estimate(observation)
    fixed = prepare_fixed_batch(encode_observation(observation, estimate), observation)
    if policy.config.legal_mask:
        fixed.arrays["legal_mask_stems"] = observation_mask_stems(observation)
    outputs = jax.device_get(
        policy.forward(policy.params, {name: jnp.asarray(value) for name, value in fixed.arrays.items()})
    )
    return finish_action(
        policy,
        observation,
        outputs,
        fixed.encoded_own_units,
        fixed.actual_own_units,
        vocabulary,
        runtime=runtime,
        enabled=enabled,
    )


OPPOSITE_MOVE = {"NORTH": "SOUTH", "SOUTH": "NORTH", "EAST": "WEST", "WEST": "EAST"}


def reversal_blocks(policy: Any, observation: dict[str, Any]) -> list[set[str]]:
    """For each unit, the move that would undo the move it made last turn (same day, move carried out)."""
    previous, action = getattr(policy, "previous_observation", None), getattr(policy, "previous_action", None)
    player = int(observation["player"])
    farm = observation["farms"][player]
    positions = [tuple(farm["farmer"]), *(tuple(hand) for hand in farm["hands"])]
    blocks: list[set[str]] = [set() for _ in positions]
    if previous is None or action is None or int(previous.get("day", -1)) != int(observation.get("day", -2)):
        return blocks
    before = previous["farms"][player]
    earlier = [tuple(before["farmer"]), *(tuple(hand) for hand in before["hands"])]
    orders = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
    for unit, (start, order) in enumerate(zip(earlier, orders)):
        if unit >= len(positions) or not order or order[0] not in MOVES:
            continue
        dx, dy = MOVES[order[0]]
        if positions[unit] == (start[0] + dx, start[1] + dy):
            blocks[unit].add(OPPOSITE_MOVE[order[0]])
    return blocks


def finish_action(
    policy: Any,
    observation: dict[str, Any],
    outputs: dict[str, Any],
    encoded_units: int,
    actual_units: int,
    vocabulary: tuple,
    row: int = 0,
    rules: bool = True,
    oscillation: bool = False,
    runtime: Any = None,
    enabled: frozenset[str] = RULES,
) -> dict[str, Any]:
    """Decode one row of forward outputs into an action and record it as the policy's previous one.

    `rules=False` is the shipped decode (independent argmax per unit), for batched evaluation.
    `oscillation=True` also masks a move straight back where the unit came from last turn (experiment).
    `runtime` (evaluation only) supplies another submission format's market decode; the shipped
    neural bundles use their own neural runtime.
    """
    if runtime is not None:
        shed_after_unit_actions, decode_market_order = runtime.shed_after_unit_actions, runtime.decode_market_order
    else:
        from kaggriculture.actions.quantities import shed_after_unit_actions
        from kaggriculture.agents.neural import decode_market_order

    unit_logits = np.asarray(outputs["unit_action"][row, :encoded_units])
    shortfall: dict[str, int] = {}
    if rules:
        blocked = reversal_blocks(policy, observation) if oscillation else None
        unit_actions = choose_unit_actions(observation, unit_logits, vocabulary, shortfall, blocked, enabled)
    else:
        unit_actions = [list(vocabulary[int(np.argmax(logits))]) for logits in unit_logits]
    unit_actions.extend([["PASS"] for _ in range(actual_units - encoded_units)])
    sellable_shed = shed_after_unit_actions(observation, unit_actions)
    market = []
    for logits in outputs["market_action"][row]:
        order = decode_market_order(logits, sellable_shed)
        if order is None:
            continue
        market.append(order)
        if order[0] == "SELL":
            item = str(order[1])
            sellable_shed[item] = max(0, sellable_shed.get(item, 0) - int(order[2]))
    if shortfall:
        day = int(observation["day"]) if "day" in observation else int(observation["step"]) // TURNS_PER_DAY
        market = add_seed_purchases(market, shortfall, day)
    action = {"farmer": unit_actions[0], "hands": unit_actions[1:], "market": market}
    policy.previous_observation = deepcopy(observation)
    policy.previous_action = deepcopy(action)
    return action
