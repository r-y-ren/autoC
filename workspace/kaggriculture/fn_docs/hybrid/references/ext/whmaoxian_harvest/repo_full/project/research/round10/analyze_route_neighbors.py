"""Read V9's encoded route DATA without importing or executing the agent.

Usage: python research/round10/analyze_route_neighbors.py [--json path]
The default source is experiments/round9_market_slack.py relative to repo root.
Only stdlib is required. This program performs no Kaggriculture games.
"""

from __future__ import annotations

import argparse
import ast
import base64
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import zlib


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "experiments" / "round9_market_slack.py"
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}


def load_payload(source: Path) -> tuple[dict, str]:
    """Extract only the literal b85 argument of json/zlib/base64 calls."""
    line = next(
        line for line in source.read_text(encoding="utf-8").splitlines()
        if line.startswith("_R108_DATA=")
    )
    expression = ast.parse(line).body[0].value
    expected = ("json.loads", "zlib.decompress", "base64.b85decode")
    for name in expected:
        if not isinstance(expression, ast.Call) or len(expression.args) != 1:
            raise ValueError(f"unexpected payload expression: expected {name}")
        if ast.unparse(expression.func) != name:
            raise ValueError(f"unexpected payload call: expected {name}")
        expression = expression.args[0]
    if not isinstance(expression, ast.Constant) or not isinstance(expression.value, str):
        raise ValueError("payload must be a literal string")
    encoded = expression.value.encode("ascii")
    raw = zlib.decompress(base64.b85decode(encoded))
    payload = json.loads(raw)
    if not all(k in payload for k in ("actions", "routes", "shops")):
        raise ValueError("unknown route payload schema")
    return payload, hashlib.sha256(raw).hexdigest()


def first_animal(tape: list[dict]) -> list[tuple[int, str, int]]:
    return [
        (step, order[1], int(order[2]))
        for step in range(144, min(168, len(tape)))
        for order in tape[step].get("market", [])
        if order and len(order) >= 3 and order[0] == "BUY_ANIMAL"
    ]


def _actions(tape: list[dict], step: int) -> tuple:
    action = tape[step]
    return action.get("farmer"), action.get("hands")


def _animal_support_only(a: list[dict], b: list[dict], steps: list[int]) -> bool:
    species = {"COW", "GOOSE"}
    structures = {"BUILD_PASTURE", "BUILD_COOP"}
    for step in steps:
        left = [a[step].get("farmer") or ["PASS"], *(a[step].get("hands") or [])]
        right = [b[step].get("farmer") or ["PASS"], *(b[step].get("hands") or [])]
        if len(left) != len(right):
            return False
        for before, after in zip(left, right):
            if before == after:
                continue
            if (
                len(before) == len(after)
                and before[0] == after[0]
                and before[0] in ("PICKUP", "PLACE")
                and before[1] in species
                and after[1] in species
                and before[2:] == after[2:]
            ):
                continue
            if len(before) == len(after) == 1 and {before[0], after[0]} == structures:
                continue
            return False
    return True


def _orders(tape: list[dict], op: str) -> list[tuple]:
    return [
        (step, tuple(order))
        for step in range(144, min(648, len(tape)))
        for order in tape[step].get("market", [])
        if order and order[0] == op
    ]


def _daily_hires(tape: list[dict]) -> dict[int, int]:
    count = Counter(
        step // 24
        for step, order in _orders(tape, "HIRE")
        if len(order) >= 1
    )
    return dict(sorted(count.items()))


def _shop_mapping(payload: dict) -> dict[int, list[list[str]]]:
    by_route: dict[int, list[list[str]]] = defaultdict(list)
    for entry in payload["shops"]:
        shops = list(entry["shops"])
        if "YARN_STORE" not in shops:
            by_route[int(entry["route"])].append(shops)
    return dict(by_route)


def _sells(tape: list[dict], item: str) -> list[tuple[int, int]]:
    return [
        (step, int(order[2]))
        for step in range(144, min(648, len(tape)))
        for order in tape[step].get("market", [])
        if order and len(order) >= 3 and order[:2] == ["SELL", item]
    ]


def _buy_product_totals(tape: list[dict]) -> dict[str, int]:
    quantities = Counter()
    for _, order in _orders(tape, "BUY_PRODUCT"):
        if len(order) >= 3:
            quantities[str(order[1])] += int(order[2])
    return dict(sorted(quantities.items()))


def analyze(source: Path, max_different_steps: int = 30) -> dict:
    payload, digest = load_payload(source)
    routes = {
        int(route_id): [payload["actions"][index] for index in action_ids]
        for route_id, action_ids in payload["routes"].items()
    }
    shops_by_route = _shop_mapping(payload)
    edges = []
    route_ids = sorted(routes)
    for offset, left in enumerate(route_ids):
        a = routes[left]
        for right in route_ids[offset + 1 :]:
            b = routes[right]
            if len(a) < 648 or len(b) < 648:
                continue
            if any(a[t] != b[t] for t in range(144)):
                continue
            aa, bb = first_animal(a), first_animal(b)
            if aa == bb or not aa or not bb:
                continue
            different = [t for t in range(144, 648) if a[t] != b[t]]
            if len(different) > max_different_steps:
                continue
            physical = [t for t in different if _actions(a, t) != _actions(b, t)]
            market = [t for t in different if a[t].get("market") != b[t].get("market")]
            animal_cost_a = sum(ANIMAL_COST.get(kind, 0) * qty for _, kind, qty in aa)
            animal_cost_b = sum(ANIMAL_COST.get(kind, 0) * qty for _, kind, qty in bb)
            hires_equal = _daily_hires(a) == _daily_hires(b)
            land_equal = _orders(a, "BUY_LAND") == _orders(b, "BUY_LAND")
            seed_equal = _orders(a, "BUY_SEED") == _orders(b, "BUY_SEED")
            input_equal = _orders(a, "BUY_PRODUCT") == _orders(b, "BUY_PRODUCT")
            input_totals_a = _buy_product_totals(a)
            input_totals_b = _buy_product_totals(b)
            input_delta = {
                item: input_totals_b.get(item, 0) - input_totals_a.get(item, 0)
                for item in sorted(input_totals_a.keys() | input_totals_b.keys())
                if input_totals_b.get(item, 0) != input_totals_a.get(item, 0)
            }
            sales_a = {item: _sells(a, item) for item in ("EGG", "MILK")}
            sales_b = {item: _sells(b, item) for item in ("EGG", "MILK")}
            early_market_prefix_equal = all(
                a[t].get("market", []) == b[t].get("market", [])
                for t in range(144, min(aa[0][0], bb[0][0]))
                if any(order for order in a[t].get("market", []))
                or any(order for order in b[t].get("market", []))
            )
            edges.append(
                {
                    "routes": [left, right],
                    "first_buy": [aa, bb],
                    "first_buy_cost_delta": animal_cost_b - animal_cost_a,
                    "different_steps": len(different),
                    "physical_different_steps": len(physical),
                    "market_different_steps": len(market),
                    "first_different_step": different[0],
                    "first_physical_difference": physical[0] if physical else None,
                    "animal_support_only_physical_diff": _animal_support_only(a, b, physical),
                    "same_daily_hires": hires_equal,
                    "same_land_orders": land_equal,
                    "same_seed_orders": seed_equal,
                    "same_input_orders": input_equal,
                    "buy_product_quantity_delta_right": input_delta,
                    "same_nonempty_market_before_buy": early_market_prefix_equal,
                    "same_egg_and_milk_sale_schedule": sales_a == sales_b,
                    "first_egg_sale_steps": [
                        sales_a["EGG"][0][0] if sales_a["EGG"] else None,
                        sales_b["EGG"][0][0] if sales_b["EGG"] else None,
                    ],
                    "non_yarn_shop_pairs": [
                        len(shops_by_route.get(left, [])),
                        len(shops_by_route.get(right, [])),
                    ],
                }
            )
    edges.sort(key=lambda edge: (edge["different_steps"], edge["routes"]))
    return {
        "source": str(source),
        "payload_sha256": digest,
        "route_count": len(routes),
        "non_yarn_shop_pair_count": sum(len(v) for v in shops_by_route.values()),
        "edge_count": len(edges),
        "edges": edges,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--max-different-steps", type=int, default=30)
    parser.add_argument("--json", type=Path, help="write complete result to JSON")
    args = parser.parse_args()
    result = analyze(args.source, args.max_different_steps)
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"routes={result['route_count']} non_yarn_shop_pairs={result['non_yarn_shop_pair_count']} "
        f"candidate_edges={result['edge_count']} payload_sha256={result['payload_sha256']}"
    )
    print("route_pair  buy_left -> buy_right  changed physical market  cash_delta_right  hires land seeds inputs prebuy same_sale animal_only  shop_pair_counts")
    for edge in result["edges"]:
        left, right = edge["routes"]
        buy_a, buy_b = edge["first_buy"]
        flags = "".join(
            "Y" if edge[key] else "N"
            for key in (
                "same_daily_hires",
                "same_land_orders",
                "same_seed_orders",
                "same_input_orders",
                "same_nonempty_market_before_buy",
                "same_egg_and_milk_sale_schedule",
                "animal_support_only_physical_diff",
            )
        )
        print(
            f"{left:3d}-{right:<3d}  {buy_a} -> {buy_b}  "
            f"{edge['different_steps']:3d} {edge['physical_different_steps']:3d} "
            f"{edge['market_different_steps']:3d}  "
            f"{edge['first_buy_cost_delta']:+5d}  {flags}  {edge['non_yarn_shop_pairs']}"
        )


if __name__ == "__main__":
    main()
