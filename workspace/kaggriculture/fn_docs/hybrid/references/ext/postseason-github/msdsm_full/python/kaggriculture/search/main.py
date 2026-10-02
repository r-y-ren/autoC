"""Kaggriculture: day 0--29 production and routing search, no learned model.

Only observations passed to agent() are used. The opponent estimator is a
rule-based state estimator supplied in the original agent, not a neural model.
The bundled x86_64 library runs without runtime compilation.
"""

from __future__ import annotations
import hashlib
import importlib
import importlib.machinery
import os
from pathlib import Path
import sys
import traceback
import types

_search = None
_last_step = -1
_last_player = None
_disabled_day = None
_DEFAULTS = {
    "episodeSteps": 720,
    "turnsPerDay": 24,
    "boardSize": 10,
    "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10,
    "farmHandCostMult": 1,
    "townShopSellInterval": 4,
    "townCenterSellInterval": 24,
    "townShopUnlockInterval": 3,
}
_PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")


def _load_search_policy(configuration):
    # Kaggle's exec-based loader omits __file__, but supplies the entry path
    # in configuration when it calls agent(). Resolve siblings from that path.
    entry_path = globals().get("__file__")
    if entry_path is None and configuration is not None:
        entry_path = (
            configuration.get("__raw_path__")
            if hasattr(configuration, "get")
            else getattr(configuration, "__raw_path__", None)
        )
    root = Path(entry_path).resolve().parent if entry_path else Path("/kaggle_simulations/agent")
    if not (root / "search_policy.py").is_file():
        raise FileNotFoundError(f"Agent bundle is missing search_policy.py: {root}")
    # Give each bundle its own namespace, including copies of the same version.
    # Keep sibling imports relative; never publish them as top-level modules.
    root = root.resolve()
    package_name = "_kaggriculture_astra_" + hashlib.sha256(str(root).encode("utf-8")).hexdigest()
    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__package__ = package_name
        package.__path__ = [str(root)]
        package.__spec__ = importlib.machinery.ModuleSpec(package_name, loader=None, is_package=True)
        package.__spec__.submodule_search_locations = package.__path__
        sys.modules[package_name] = package
    return importlib.import_module(".search_policy", package_name).SearchPolicy


def _supported(obs, configuration):
    farm = obs["farms"][int(obs["player"])]
    if len(farm["tiles"]) != 10 or any(len(row) != 10 for row in farm["tiles"]):
        return False
    if obs.get("market", {}).get("params"):
        return False
    if configuration is not None:
        for key, value in _DEFAULTS.items():
            actual = (
                configuration.get(key, value) if hasattr(configuration, "get") else getattr(configuration, key, value)
            )
            if actual != value:
                return False
    return True


def _safe_action(obs):
    """Return carried goods and sell. Used only on unsupported input or error.

    This is not a learned-policy fallback and does not create new production.
    """
    player = int(obs.get("player", 0))
    farm = obs["farms"][player]
    half = len(farm["tiles"]) // 2
    centers = ((half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half))
    actions = []
    positions = [farm["farmer"], *farm.get("hands", [])]
    for x, y in positions:
        if (x, y) in centers:
            actions.append(["DROP"])
        else:
            tx, ty = min(centers, key=lambda p: abs(x - p[0]) + abs(y - p[1]))
            if x != tx:
                actions.append(["EAST" if x < tx else "WEST"])
            else:
                actions.append(["SOUTH" if y < ty else "NORTH"])
    market = [["SELL", item, 1000000] for item in _PRODUCTS]
    return {"farmer": actions[0], "hands": actions[1:], "market": market}


def agent(observation, configuration=None):
    global _search, _last_step, _last_player, _disabled_day
    day = int(observation.get("day", 0))
    hour = int(observation.get("hour", 0))
    step = int(observation.get("step", 24 * day + hour))
    player = int(observation.get("player", 0))
    if step < _last_step or (step == 0 and _last_step >= 0) or (_last_player is not None and player != _last_player):
        _search = None
        _disabled_day = None
    _last_step, _last_player = step, player
    if not _supported(observation, configuration) or not 0 <= day < 30:
        return _safe_action(observation)
    if _disabled_day == day:
        return _safe_action(observation)
    if _disabled_day is not None:
        _search = None
        _disabled_day = None
    try:
        if _search is None:
            # A fresh process cannot reconstruct a route already partly executed.
            if hour != 0:
                _disabled_day = day
                return _safe_action(observation)
            SearchPolicy = _load_search_policy(configuration)
            _search = SearchPolicy(seconds=2.8)
        overage = max(0.0, float(observation.get("remainingOverageTime", 60.0)))
        # Kaggle clock: 1s/turn + 60s overage. Spend the overage across the
        # remaining dawns, capped at 2.8s per dawn, keeping a 5s reserve.
        _search.seconds = min(2.8, 0.90 + max(0.0, overage - 5.0) / max(1, 30 - day))
        if day == 29:
            # The remaining calls only replay this terminal plan. Use part of
            # the otherwise unused allowance, retaining three seconds plus
            # the 0.10-second Python/dispatch reserve.
            _search.seconds = min(6.0, 0.90 + max(0.0, overage - 3.0))
        return _search(observation)
    except Exception:
        if os.environ.get("KAGGRICULTURE_RAISE_AGENT_ERRORS") == "1":
            raise
        traceback.print_exc(file=sys.stderr)
        _disabled_day = day
        return _safe_action(observation)
