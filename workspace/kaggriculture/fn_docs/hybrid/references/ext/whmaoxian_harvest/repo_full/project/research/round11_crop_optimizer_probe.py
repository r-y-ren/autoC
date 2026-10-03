"""Read-only probe of V9's day-11 crop tranche and later route actions."""

from collections import Counter, defaultdict
from pathlib import Path
import contextlib
import io

ROOT = Path(__file__).resolve().parents[1]

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments.agent import get_last_callable

source = ROOT / "submissions/release_v9/main.py"
policy = get_last_callable(source.read_text(encoding="utf-8"), path=str(source))
routes = policy.__globals__["_IMPL"].chassis.routes

for route, tape in sorted(routes.items()):
    day11 = Counter()
    later = defaultdict(Counter)
    orders = defaultdict(Counter)
    for step, action in enumerate(tape):
        day = step // 24
        for command in [action.get("farmer"), *(action.get("hands") or [])]:
            if command and command[0] in ("PLANT", "HARVEST", "WATER", "FERTILIZE", "DIG"):
                if day == 11:
                    day11[tuple(command)] += 1
                if 18 <= day <= 29:
                    later[day][tuple(command)] += 1
        for order in action.get("market", []):
            if order and order[0] in ("BUY_SEED", "SELL") and len(order) >= 3 and order[1] in ("STRAWBERRY", "TOMATO", "CARROT", "WHEAT"):
                if 10 <= day <= 29:
                    orders[day][tuple(order)] += 1
    print("ROUTE", route, "day11", dict(day11))
    for day in range(18, 30):
        action = {str(k):v for k,v in later[day].items() if k[0] in ("HARVEST", "PLANT", "DIG")}
        sell = {str(k):v for k,v in orders[day].items()}
        if action or sell:
            print("  day", day, "actions", action, "orders", sell)
