"""Rollout-only land decisions; never used by the policy or its objective."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np

from kaggriculture.actions.catalog import MARKET_ACTIONS
from kaggriculture.observations.features import FEATURE_INDEX
from kaggriculture.training.phase_entropy import PHASES
from kaggriculture.actions.sell_quantity import NON_SELL_IDS
from kaggriculture.observations.tracker_constants import LAND_PRICES

LAND_ENGINE_ID = MARKET_ACTIONS.index(("BUY_LAND",))
PHASE_WINDOWS = (("all", 0, 719), *PHASES)
DAY_BINS = 31  # Thirty purchase days plus never purchased within this rollout.
HAND_SCALE = 32  # `self_hand_count` is stored as hands / 32.
DAYS = 30
NOON_HOUR = 12


def land_order_probability(log_probs: jax.Array, *, absolute: bool) -> jax.Array:
    index = NON_SELL_IDS.index(LAND_ENGINE_ID) if absolute else LAND_ENGINE_ID
    slot_probability = jnp.exp(log_probs[..., index])
    # Heads are independent conditional on the observation. This is an order event,
    # not the probability that the sequential market resolver accepts a purchase.
    return -jnp.expm1(jnp.sum(jnp.log1p(-slot_probability), axis=-1))


def land_counts(features: np.ndarray) -> np.ndarray:
    return np.rint(features[:, 0, FEATURE_INDEX["self_unlocked_count"]] * 4).astype(np.int8)


def hand_counts(features: np.ndarray) -> np.ndarray:
    return np.rint(features[:, 0, FEATURE_INDEX["self_hand_count"]] * HAND_SCALE).astype(np.int8)


@dataclass
class LandTrace:
    counts: np.ndarray
    affordable: np.ndarray
    probability: np.ndarray
    hands: np.ndarray

    @classmethod
    def create(cls, horizon: int, agents: int) -> LandTrace:
        return cls(
            np.empty((horizon + 1, agents), dtype=np.int8),
            np.empty((horizon, agents), dtype=np.bool_),
            np.empty((horizon, agents), dtype=np.float32),
            np.empty((horizon + 1, agents), dtype=np.int8),
        )

    def observe(self, step: int, features: np.ndarray, money: np.ndarray) -> None:
        count = land_counts(features)
        self.counts[step] = count
        self.hands[step] = hand_counts(features)
        price = np.asarray((*LAND_PRICES, np.inf))[count - 1]
        self.affordable[step] = np.asarray(money).reshape(-1) >= price

    def totals(self, valid_games: int) -> dict[str, float]:
        agents = valid_games * 2
        if not 0 < agents <= self.probability.shape[1]:
            raise ValueError("invalid non-padding game count")
        counts = self.counts[:, :agents]
        if np.any((counts < 1) | (counts > 4)) or np.any(np.diff(counts, axis=0) < 0):
            raise ValueError("land ownership must increase monotonically from one to four")
        probability = self.probability[:, :agents].astype(np.float64)
        if not np.isfinite(probability).all() or np.any((probability < 0) | (probability > 1)):
            raise ValueError("invalid land order probability")
        terms = np.stack((probability, 1 - probability), axis=-1)
        logs = np.log(terms, out=np.zeros_like(terms), where=terms > 0)
        entropy = -(terms * logs).sum(axis=-1) / np.log(2)
        success = counts[1:] > counts[:-1]
        totals = {"agents": float(agents)}
        for phase, start, end in PHASE_WINDOWS:
            for owned in range(1, 4):
                mask = (counts[:-1][start:end] == owned) & self.affordable[start:end, :agents]
                prefix = f"{phase}/{owned}"
                totals[f"{prefix}/count"] = float(mask.sum())
                totals[f"{prefix}/probability"] = float(probability[start:end][mask].sum())
                totals[f"{prefix}/entropy"] = float(entropy[start:end][mask].sum())
                totals[f"{prefix}/success"] = float(success[start:end][mask].sum())
        for target in range(2, 5):
            reached = counts[1:] >= target
            any_reached = reached.any(axis=0)
            first_step = reached.argmax(axis=0)
            bins = np.where(any_reached, first_step // 24, DAY_BINS - 1)
            histogram = np.bincount(bins, minlength=DAY_BINS)
            for index, count in enumerate(histogram):
                totals[f"acquisition/{target}/{index}"] = float(count)
            totals[f"acquisition/{target}/step_sum"] = float(first_step[any_reached].sum())
        for owned in range(1, 5):
            totals[f"final/{owned}"] = float(np.sum(counts[-1] == owned))
        hands = self.hands[:, :agents]
        if np.any((hands < 0) | (hands > HAND_SCALE)):
            raise ValueError("hand counts must lie between zero and the feature scale")
        final_histogram = np.bincount(hands[-1].astype(np.int64), minlength=HAND_SCALE + 1)
        for count, games in enumerate(final_histogram):
            totals[f"hands/final/{count}"] = float(games)
        # Hands are hired per day and expire overnight, so sample at noon rather than at hour 0.
        for day in range(DAYS):
            totals[f"hands/day/{day}"] = float(hands[min(day * 24 + NOON_HOUR, hands.shape[0] - 1)].sum())
        return totals


def land_report(totals: dict[str, float]) -> dict[str, Any]:
    report: dict[str, Any] = {
        "agent_games": round(totals["agents"]),
        "eligibility": "pre-turn raw money >= next land price; excludes SELL-financed opportunities",
        "probability_event": "at least one BUY_LAND order among ten independent slots, not resolver success",
        "phases": {},
        "acquisition": {},
        "final_owned_counts": {str(n): round(totals[f"final/{n}"]) for n in range(1, 5)},
    }
    for phase, _, _ in PHASE_WINDOWS:
        report["phases"][phase] = {}
        for owned in range(1, 4):
            prefix = f"{phase}/{owned}"
            count = totals[f"{prefix}/count"]
            report["phases"][phase][str(owned)] = {
                "eligible_states": round(count),
                "buy_order_probability": totals[f"{prefix}/probability"] / count if count else None,
                "binary_normalized_entropy": totals[f"{prefix}/entropy"] / count if count else None,
                "actual_purchase_rate": totals[f"{prefix}/success"] / count if count else None,
            }
    for target in range(2, 5):
        histogram = np.asarray([totals[f"acquisition/{target}/{i}"] for i in range(DAY_BINS)])
        purchased = histogram[:-1].sum()
        distribution = histogram / totals["agents"]
        nonzero = distribution[distribution > 0]
        report["acquisition"][str(target)] = {
            "day_counts_1_to_30": histogram[:-1].astype(int).tolist(),
            "never_purchased": int(histogram[-1]),
            "purchase_fraction": float(purchased / totals["agents"]),
            "mean_purchase_step_zero_based": totals[f"acquisition/{target}/step_sum"] / purchased
            if purchased
            else None,
            "day_distribution_normalized_entropy": float(-np.sum(nonzero * np.log(nonzero)) / np.log(DAY_BINS)),
        }
    final_hands = {
        str(n): round(totals[f"hands/final/{n}"]) for n in range(HAND_SCALE + 1) if totals[f"hands/final/{n}"]
    }
    report["hands"] = {
        "final_count_histogram": final_hands,
        "mean_final_count": sum(int(n) * c for n, c in final_hands.items()) / totals["agents"],
        "mean_at_noon_by_day_0_to_29": [totals[f"hands/day/{day}"] / totals["agents"] for day in range(DAYS)],
    }
    return report
