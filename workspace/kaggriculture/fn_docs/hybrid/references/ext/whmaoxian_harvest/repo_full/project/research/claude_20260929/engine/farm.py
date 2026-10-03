"""Kaggriculture reactive farm engine (stdlib only).

Economic plan (rule based, shop aware) + per-step task executor for the farmer and
hired hands + market layer. Written 2026-09-29.
"""
import math

# ----------------------------------------------------------------------------- rules
CROPS = {
    "WHEAT": dict(seed=10, first=2, maxd=4, ongoing=False, cap=6),
    "CARROT": dict(seed=20, first=2, maxd=3, ongoing=False, cap=4),
    "TOMATO": dict(seed=50, first=8, maxd=8, ongoing=True, cap=4, interval=1),
    "STRAWBERRY": dict(seed=100, first=10, maxd=10, ongoing=True, cap=4, interval=2),
    "MELON": dict(seed=80, first=10, maxd=12, ongoing=False, cap=6),
}
ANIMALS = {
    "GOOSE": dict(cost=300, struct="COOP", first=4, interval=1, held=4, product="EGG"),
    "COW": dict(cost=400, struct="PASTURE", first=8, interval=2, held=6, product="MILK"),
    "SHEEP": dict(cost=500, struct="PASTURE", first=6, interval=3, held=6, product="WOOL"),
}
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SHOPS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
MP = {
    "WHEAT": (25, 400, "sqrt", 0.80, "log", 0.20), "CARROT": (35, 450, "hinge", 1.00, "sqrt", 0.70),
    "TOMATO": (60, 200, "hinge", 0.40, "sqrt", 0.60), "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON": (250, 300, "log", 0.20, "sq", 3.60), "EGG": (50, 332, "hinge", 0.40, "log", 0.20),
    "MILK": (160, 122, "sqrt", 0.60, "linear", 1.60), "WOOL": (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
LAND_PRICE = (1000, 2000, 4000)
SHED_ADJ = ((4, 4), (5, 4), (4, 5), (5, 5))
TPD = 24
LAST = 718  # last acting step


def fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _shape(f, x, T):
    x = max(0.0, x)
    if f == "linear": return x
    if f == "sq": return x * x
    if f == "sqrt": return math.sqrt(x)
    if f == "log": return math.log(1.0 + x)
    if f == "hinge":
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def price_at(item, inv):
    base, T, bf, bt, af, at = MP[item]
    if inv < 10000:
        p = base + bt * base / _shape(bf, T, T) * _shape(bf, 10000 - inv, T)
    else:
        p = base - at * base / _shape(af, T, T) * _shape(af, inv - 10000, T)
    return max(1, int(round(p)))


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def step_toward(pos, target):
    x, y = pos
    tx, ty = target
    if x < tx: return "EAST"
    if x > tx: return "WEST"
    if y < ty: return "SOUTH"
    if y > ty: return "NORTH"
    return "PASS"


def nearest_shed(pos):
    return min(SHED_ADJ, key=lambda p: (dist(pos, p), SHED_ADJ.index(p)))
