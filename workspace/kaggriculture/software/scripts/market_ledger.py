"""Tracing helpers for the vendored official Kaggriculture market engine.

The tracer deliberately delegates market resolution to the installed official
engine.  It wraps only ``_commit_unit`` (and the parser for order identity), so
prices, lockstep ordering, inventory mutations, and success/failure decisions
remain those of the engine itself.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator


def _value(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _requested(raw_order: Any, parsed: Any) -> int:
    try:
        if isinstance(parsed, dict) and "remaining" in parsed:
            return int(parsed["remaining"])
        return int(raw_order[2])
    except (IndexError, TypeError, ValueError, KeyError):
        return 1


class OfficialMarketLedger:
    """Capture every official ``_commit_unit`` attempt in one episode."""

    def __init__(self, seed: int | None = None):
        self.seed = seed
        self.rows: list[dict[str, Any]] = []
        self._engine = None
        self._originals: dict[str, Any] = {}
        self._context: dict[str, Any] | None = None

    def _prepare_context(self, state: Any, env: Any) -> dict[str, Any]:
        import kaggle_environments.envs.kaggriculture.kaggriculture as engine

        obs0 = state[0].observation
        day = int(_value(obs0, "day", 0))
        hour = int(_value(obs0, "hour", 0))
        max_orders = max(1, int(_value(env.configuration,
                                        "maxMarketOrdersPerTurn", 10)))
        expected: list[dict[str, Any]] = []
        for player, seat in enumerate(state):
            action = seat.action if isinstance(seat.action, dict) else {}
            market = action.get("market", []) if isinstance(action, dict) else []
            queue = list(market) if isinstance(market, list) else []
            # _process_market parses by column, then by player.  Build the same
            # sequence so a parsed order can retain its official column/seat.
            expected.append({"player": player, "queue": queue[:max_orders]})
        parse_sequence: list[dict[str, Any]] = []
        max_len = max((len(row["queue"]) for row in expected), default=0)
        for column in range(max_len):
            for player, row in enumerate(expected):
                if column < len(row["queue"]):
                    parse_sequence.append({
                        "player": player,
                        "order_column": column,
                        "raw": row["queue"][column],
                    })
        return {
            "day": day,
            "hour": hour,
            "parse_sequence": parse_sequence,
            "orders": [],
            "farm_players": {id(seat.observation.farms[player]): player
                             for player, seat in enumerate(state)
                             for _ in [0]},
            "farms": {id(farm): player for player, farm in
                      enumerate(_value(obs0, "farms", []) or [])},
            "engine": engine,
        }

    def _parse_order(self, raw_order: Any) -> Any:
        parsed = self._originals["_parse_order"](raw_order)
        ctx = self._context
        if ctx is None:
            return parsed
        meta = ctx["parse_sequence"].pop(0) if ctx["parse_sequence"] else {}
        if not isinstance(parsed, dict) or "item" not in parsed:
            return parsed
        ctx["orders"].append({
            "player": meta.get("player"),
            "order_column": meta.get("order_column"),
            "op": parsed.get("type"),
            "item": parsed.get("item"),
            "requested_qty": _requested(raw_order, parsed),
            "filled_qty": 0,
            "failed": False,
        })
        return parsed

    def _commit_unit(self, op: Any, item: Any, price: Any, farm: Any,
                     private: Any, market: Any, shed_capacity: Any = 100) -> bool:
        ok = self._originals["_commit_unit"](
            op, item, price, farm, private, market, shed_capacity)
        ctx = self._context
        if ctx is None or op not in ("SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL"):
            return ok
        player = ctx["farms"].get(id(farm))
        candidates = [row for row in ctx["orders"]
                      if not row["failed"] and row["filled_qty"] < row["requested_qty"]
                      and row["op"] == op and row["item"] == item
                      and (player is None or row["player"] == player)]
        row = candidates[0] if candidates else None
        # A row should always be found for an official commit.  Keep the event
        # visible with a null column if an upstream engine changes its parser.
        self.rows.append({
            "seed": self.seed,
            "day": ctx["day"],
            "hour": ctx["hour"],
            "player": player,
            "order_column": row["order_column"] if row else None,
            "op": op,
            "item": item,
            "unit_price": float(price),
            "success": bool(ok),
        })
        if row is not None:
            if ok:
                row["filled_qty"] += 1
            else:
                row["failed"] = True
        return ok

    @contextmanager
    def installed(self) -> Iterator["OfficialMarketLedger"]:
        """Install hooks for the duration of an official engine run."""
        import kaggle_environments.envs.kaggriculture.kaggriculture as engine

        self._engine = engine
        self._originals = {
            "_process_market": engine._process_market,
            "_parse_order": engine._parse_order,
            "_commit_unit": engine._commit_unit,
        }

        def process_market(state: Any, env: Any) -> Any:
            previous = self._context
            self._context = self._prepare_context(state, env)
            try:
                return self._originals["_process_market"](state, env)
            finally:
                self._context = previous

        def parse_order(raw_order: Any) -> Any:
            return self._parse_order(raw_order)

        def commit_unit(op: Any, item: Any, price: Any, farm: Any,
                        private: Any, market: Any,
                        shed_capacity: Any = 100) -> bool:
            return self._commit_unit(op, item, price, farm, private, market,
                                     shed_capacity)

        engine._process_market = process_market
        engine._parse_order = parse_order
        engine._commit_unit = commit_unit
        try:
            yield self
        finally:
            engine._process_market = self._originals["_process_market"]
            engine._parse_order = self._originals["_parse_order"]
            engine._commit_unit = self._originals["_commit_unit"]
            self._context = None


def make_ledger_runner(seed: int | None = None) -> OfficialMarketLedger:
    """Return a ledger context; kept as a small compatibility factory."""
    return OfficialMarketLedger(seed=seed)


# Legacy helper retained for callers that only need a simple aggregation.
def summarize(ledger):
    from collections import defaultdict

    agg = defaultdict(lambda: [0, 0.0])
    for row in ledger:
        if isinstance(row, dict):
            if not row.get("success"):
                continue
            key = (row.get("player"), row.get("op"), row.get("item"))
            agg[key][0] += 1
            agg[key][1] += float(row.get("unit_price", 0.0))
        else:
            day, pid, op, item, price = row
            key = (pid, op, item)
            agg[key][0] += 1
            agg[key][1] += price
    return agg
