"""Reproduce a V9 market-order target-drift counterexample on frozen code."""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
from io import StringIO
from itertools import permutations
import json
from pathlib import Path

from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parents[2]
path = ROOT / 'submissions/release_v9/main.py'
assert hashlib.sha256(path.read_bytes()).hexdigest() == (
    '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
)
with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
    entry = get_last_callable(path.read_text(encoding='utf-8'), path=str(path))
globals_ = entry.__globals__
params = globals_['_R37_MARKET_PARAMS']
factor_margin = globals_['_v44y_factor_margin']

orders_0 = [
    ['SELL', 'EGG', 108],
    ['SELL', 'MILK', 98],
    ['SELL', 'MELON', 80],
]
inventory = {item: int(spec['I0']) for item, spec in params.items()}
inventory.update({'EGG': 10134, 'MILK': 9992, 'MELON': 9978})
stock = {item: 200 for item in params}


def one_pass(orders):
    """The one-block branch of the frozen V9 reorder routine."""
    margin = factor_margin(orders, inventory, stock, params)
    best_score = margin(orders)
    best_orders = orders
    for perm in permutations(orders):
        score = margin(perm)
        if score > best_score + 0.5:
            best_score, best_orders = score, list(perm)
    return best_orders, best_score


orders_1, first_model_score = one_pass(orders_0)
orders_2, second_model_score = one_pass(orders_1)
original_model = factor_margin(orders_0, inventory, stock, params)
assert orders_0 != orders_1 != orders_2
assert original_model(orders_1) > original_model(orders_2)
print(json.dumps({
    'initial': orders_0,
    'after_one_call': orders_1,
    'after_two_calls': orders_2,
    'original_model_values': [original_model(o) for o in
                              (orders_0, orders_1, orders_2)],
    'first_model_best': first_model_score,
    'second_model_best': second_model_score,
}, indent=2))
