"""Tomato-action exploration when town demand contains at least two tomato shops."""

from __future__ import annotations

import jax
import jax.numpy as jnp

from kaggriculture.actions.catalog import MARKET_ACTIONS, PRODUCTS, UNIT_ACTIONS
from kaggriculture.observations.features import FEATURE_INDEX
from kaggriculture.actions.sell_quantity import ABSOLUTE_START, QUANTITY_COUNT

TOMATO_SHOP_BONUS_DEFAULT = 0.0
TOMATO_SHOP_COUNT_THRESHOLD = 2
SHOP_COUNT_SCALE = 8

BUY_TOMATO_IDS = tuple(index for index, action in enumerate(MARKET_ACTIONS) if action[:2] == ("BUY_SEED", "TOMATO"))
LEGACY_SELL_TOMATO_IDS = tuple(index for index, action in enumerate(MARKET_ACTIONS) if action[:2] == ("SELL", "TOMATO"))
ABSOLUTE_SELL_TOMATO_START = ABSOLUTE_START + PRODUCTS.index("TOMATO") * QUANTITY_COUNT
ABSOLUTE_SELL_TOMATO_IDS = tuple(range(ABSOLUTE_SELL_TOMATO_START, ABSOLUTE_SELL_TOMATO_START + QUANTITY_COUNT))
PLANT_TOMATO_ID = UNIT_ACTIONS.index(("PLANT", "TOMATO"))


def at_least_one(probability: jax.Array, mask: jax.Array | None = None) -> jax.Array:
    probability = jnp.clip(probability.astype(jnp.float32), 0.0, 1.0)
    if mask is not None:
        probability = jnp.where(mask, probability, 0.0)
    return -jnp.expm1(jnp.sum(jnp.log1p(-probability), axis=-1))


def tomato_shop_eligibility(features: jax.Array) -> jax.Array:
    global_features = features[:, 0].astype(jnp.float32)
    count = SHOP_COUNT_SCALE * (
        global_features[:, FEATURE_INDEX["shop_count:PIZZA_SHOP"]]
        + global_features[:, FEATURE_INDEX["shop_count:FARMERS_MARKET"]]
    )
    return count >= TOMATO_SHOP_COUNT_THRESHOLD


def tomato_in_shed(features: jax.Array) -> jax.Array:
    tomato_product = features[..., FEATURE_INDEX["token:PRODUCT"]] * features[..., FEATURE_INDEX["item:TOMATO"]]
    encoded_count = features[..., FEATURE_INDEX["product_shed_count"]]
    return jnp.any((tomato_product > 0.5) & (encoded_count > 0), axis=-1)


def tomato_shop_bonus_terms(
    unit_logits: jax.Array,
    market_logits: jax.Array,
    features: jax.Array,
    unit_mask: jax.Array,
    coefficient: float | jax.Array,
    *,
    absolute_sell: bool,
) -> tuple[jax.Array, dict[str, jax.Array]]:
    unit_probability = jax.nn.softmax(unit_logits.astype(jnp.float32), axis=-1)
    market_probability = jax.nn.softmax(market_logits.astype(jnp.float32), axis=-1)
    buy_slot_probability = jnp.sum(market_probability[..., jnp.asarray(BUY_TOMATO_IDS)], axis=-1)
    sell_ids = ABSOLUTE_SELL_TOMATO_IDS if absolute_sell else LEGACY_SELL_TOMATO_IDS
    sell_slot_probability = jnp.sum(market_probability[..., jnp.asarray(sell_ids)], axis=-1)

    buy_probability = at_least_one(buy_slot_probability)
    sell_inventory_eligible = tomato_in_shed(features).astype(jnp.float32)
    sell_probability = sell_inventory_eligible * at_least_one(sell_slot_probability)
    plant_probability = at_least_one(unit_probability[..., PLANT_TOMATO_ID], unit_mask)
    eligible = tomato_shop_eligibility(features).astype(jnp.float32)
    reward = eligible * (buy_probability + sell_probability + plant_probability)
    loss = -jnp.asarray(coefficient, dtype=jnp.float32) * reward
    return loss, {
        "tomato_shop_bonus_loss": loss,
        "tomato_shop_eligible": eligible,
        "tomato_shop_sell_inventory_eligible": eligible * sell_inventory_eligible,
        "tomato_shop_buy_probability": eligible * buy_probability,
        "tomato_shop_sell_probability": eligible * sell_probability,
        "tomato_shop_plant_probability": eligible * plant_probability,
        "tomato_shop_bonus_coefficient": jnp.full_like(loss, coefficient),
    }
