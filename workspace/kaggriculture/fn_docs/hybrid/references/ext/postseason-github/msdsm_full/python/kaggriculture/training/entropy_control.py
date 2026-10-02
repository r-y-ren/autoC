"""Per-head normalized-entropy feedback, independent of the PPO accelerator loop."""

from __future__ import annotations

import math
import struct
from dataclasses import asdict, dataclass
from typing import Any

HEAD_ENTROPY_DEFAULTS = {
    "unit_entropy_target": None,
    "market_entropy_target": None,
    "head_entropy_ema_decay": 0.9,
    "head_entropy_interval": 5,
    "head_entropy_relative_band": 0.1,
    "head_entropy_change_factor": 1.25,
    "head_entropy_coefficient_min": 1e-9,
    "uncapped_entropy": False,
}


@dataclass(frozen=True)
class HeadEntropyConfig:
    unit_target: float
    market_target: float
    ema_decay: float = 0.9
    interval: int = 5
    relative_band: float = 0.1
    change_factor: float = 1.25
    minimum: float = 1e-9
    maximum: float | None = 1e-4

    def validate(self) -> None:
        values = (
            self.unit_target,
            self.market_target,
            self.ema_decay,
            self.relative_band,
            self.change_factor,
            self.minimum,
        )
        if self.maximum is not None:
            values += (self.maximum,)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("entropy-controller settings must be finite")
        if not 0 < self.unit_target < 1 or not 0 < self.market_target < 1:
            raise ValueError("head entropy targets must be in (0, 1)")
        if not 0 <= self.ema_decay < 1 or self.interval <= 0 or not 0 <= self.relative_band < 1:
            raise ValueError("invalid entropy EMA, interval, or relative band")
        if self.change_factor <= 1 or self.minimum <= 0:
            raise ValueError("invalid entropy coefficient bounds or change factor")
        if self.maximum is not None and self.minimum > self.maximum:
            raise ValueError("entropy coefficient maximum is below its minimum")


@dataclass(frozen=True)
class EntropyChannel:
    coefficient: float
    ema: float | None = None


@dataclass(frozen=True)
class HeadEntropyState:
    unit: EntropyChannel
    market: EntropyChannel
    observations: int = 0

    @classmethod
    def initialize(cls, coefficient: float, config: HeadEntropyConfig) -> HeadEntropyState:
        coefficient = max(config.minimum, coefficient)
        if config.maximum is not None:
            coefficient = min(config.maximum, coefficient)
        validate_coefficient(coefficient)
        return cls(EntropyChannel(coefficient), EntropyChannel(coefficient))

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> HeadEntropyState:
        return cls(EntropyChannel(**raw["unit"]), EntropyChannel(**raw["market"]), int(raw["observations"]))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def config_from_args(args: Any) -> HeadEntropyConfig | None:
    unit = getattr(args, "unit_entropy_target", None)
    market = getattr(args, "market_entropy_target", None)
    if unit is None and market is None:
        return None
    if unit is None or market is None:
        raise ValueError("specify both Unit and Market entropy targets")
    config = HeadEntropyConfig(
        unit_target=unit,
        market_target=market,
        ema_decay=args.head_entropy_ema_decay,
        interval=args.head_entropy_interval,
        relative_band=args.head_entropy_relative_band,
        change_factor=args.head_entropy_change_factor,
        minimum=args.head_entropy_coefficient_min,
        maximum=None if getattr(args, "uncapped_entropy", False) else args.entropy_coefficient_max,
    )
    config.validate()
    return config


def validate_coefficient(coefficient: float) -> None:
    if not math.isfinite(coefficient):
        raise FloatingPointError("entropy coefficient is nonfinite")
    try:
        encoded = struct.pack("f", coefficient)
    except OverflowError as error:
        raise FloatingPointError("entropy coefficient cannot be represented in float32") from error
    if not math.isfinite(struct.unpack("f", encoded)[0]):
        raise FloatingPointError("entropy coefficient cannot be represented in float32")


def update_head_entropy(
    state: HeadEntropyState, config: HeadEntropyConfig, unit_entropy: float, market_entropy: float
) -> tuple[HeadEntropyState, dict[str, Any]]:
    observed = (unit_entropy, market_entropy)
    valid = all(math.isfinite(value) and 0 <= value <= 1.000001 for value in observed)
    if not valid:
        return state, {
            "mode": "per_head_target",
            "adjusted": False,
            "reason": "invalid_entropy_measurement",
            "observations": state.observations,
        }
    count = state.observations + 1
    due = count % config.interval == 0
    channels = {}
    report: dict[str, Any] = {
        "mode": "per_head_target",
        "observations": count,
        "adjustment_due": due,
        "interval": config.interval,
        "ema_decay": config.ema_decay,
        "coefficient_max": config.maximum,
    }
    for name, previous, value, target in (
        ("unit", state.unit, unit_entropy, config.unit_target),
        ("market", state.market, market_entropy, config.market_target),
    ):
        ema = value if previous.ema is None else config.ema_decay * previous.ema + (1 - config.ema_decay) * value
        lower, upper = target * (1 - config.relative_band), target * (1 + config.relative_band)
        coefficient = previous.coefficient
        reason = "interval" if not due else "target_band"
        if due and ema < lower:
            coefficient *= config.change_factor
            if config.maximum is not None:
                coefficient = min(config.maximum, coefficient)
            reason = "below_band" if coefficient != previous.coefficient else "maximum_reached"
        elif due and ema > upper:
            coefficient = max(config.minimum, coefficient / config.change_factor)
            reason = "above_band" if coefficient != previous.coefficient else "minimum_reached"
        validate_coefficient(coefficient)
        channels[name] = EntropyChannel(coefficient, ema)
        report[name] = {
            "normalized_entropy": value,
            "ema": ema,
            "target": target,
            "lower": lower,
            "upper": upper,
            "coefficient_used": previous.coefficient,
            "coefficient_next": coefficient,
            "adjusted": coefficient != previous.coefficient,
            "reason": reason,
        }
    report["adjusted"] = report["unit"]["adjusted"] or report["market"]["adjusted"]
    return HeadEntropyState(channels["unit"], channels["market"], count), report
