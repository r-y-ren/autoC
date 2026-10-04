"""The Kaggle field's measured market flow: what the opponents that beat us do.

Why this exists
---------------
`kagg2_flow` is one opponent's supply mix, measured off one bot. It is the
right *kind* of rung -- replay a real market footprint instead of simulating an
opponent that makes one -- and the wrong opponent. The 2026-08-30 Kaggle
autopsy of the games our champion lost puts the winners nowhere near kagg2:
12-14 hands by day 10, ~196 tiles planted (137 wheat, 37 strawberry), ~9 cows
and 4 sheep, ~98k final money. They are tuned wheat clones, and the market they
make is a market our training has never seen.

This is that market, measured the same way.

                       kagg2          Kaggle field
      WHEAT           658 / -595      473 / -292
      CARROT           12               20
      TOMATO            0                0
      STRAWBERRY      245              287
      MELON           120               87
      EGG               0                0
      MILK            257              229
      WOOL            155              144
      FERTILIZER      255              240

Read against kagg2 the field is a *lighter* seller of everything except berries
and carrots, and it churns far less wheat -- but it liquidates: the busiest
single day in the table is 110 units of wheat on day 29, against kagg2's 107 on
day 23. The strawberry line opens on day 16 and stays open, where kagg2's is a
late trickle, and the melon race is two smaller dumps (day 10 and day 20)
rather than one big one.

Provenance
----------
* Source games: 12 Kaggle replays of our `flow30d_g2520` submission's **losses**
  (`replays/flow30d_g2520_L_*.json`), one per opposing team -- Ayaz Ahmed Kazi,
  ChandramouliNagasundaram, Grim Reaper, Lujia Liang, T Soo, Vib, Yuyannnn,
  meatori-nu, naphthalene, small fry in the underworld, stsa asts,
  ほのぼの牧場. Twelve different opponents, not twelve games of one, which is
  the point: the rung is the *field*, not a bot.
* Measured by `scripts/replay_flow.py`, which reconstructs the engine's
  lockstep market phase with `scripts/replay_profile.py`'s `_simulate_market`
  and counts the **executed** units per product per day (a queued order that
  found an empty shed moves no quote). The per-game season totals reproduce the
  profiler's own `sellu_<PRODUCT>` / `buyprod_<PRODUCT>` columns exactly --
  `tests/test_kaggle_flow.py::test_totals_match_the_profiler` re-runs both on
  one replay and compares.
* Table = mean units per day over the 12 games, rounded half-up to int32.
* Measured 2026-08-30. The generated table lives in `kaggle_flow_table.json`
  next to this file so a re-measurement is a re-run of the script and a diff,
  not a hand edit of a literal.

Not a tape
----------
Same caveat as `kagg2_flow`, and more so, because these are twelve *different*
opponents averaged: the table is a centre, and `es.train.Trainer` draws a scale
and a day shift per episode pair around it (`--kaggle-flow-scale` /
`--kaggle-flow-shift`, defaulting to whatever the kagg2 rung is using). What
the rung asserts is the shape of the field's supply, not any one game's tape.

The yardstick's flow ensemble (`--abs-flow-draws`) stays on `kagg2_flow`: it is
a *comparability* device, fixed forever so two checkpoints' numbers mean the
same thing, and every number on record was read there. This rung is measured at
the centre in the liveness probe and trained on, and is not a selection metric
today.
"""

from __future__ import annotations

import json
import os

import numpy as np

from .. import spec

#: Name of the ladder rung that plays this table; `--rung-weight` accepts it.
RUNG_NAME = "kaggle_flow"

#: The generated measurement, shipped in the repo next to this module.
TABLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "kaggle_flow_table.json")


def _load(path=TABLE_PATH):
    with open(path) as fh:
        doc = json.load(fh)
    if list(doc["products"]) != list(spec.PRODUCTS):
        raise ValueError(
            f"{path}: product order {doc['products']} is not spec.PRODUCTS "
            f"{list(spec.PRODUCTS)}; the table's columns would be mislabelled.")
    if int(doc["days"]) != int(spec.N_DAYS):
        raise ValueError(f"{path}: {doc['days']} days, spec says {spec.N_DAYS}.")
    sell = np.asarray(doc["sell"], dtype=np.int32)
    buy = np.asarray(doc["buy"], dtype=np.int32)
    want = (int(spec.N_DAYS), int(spec.N_PRODUCTS))
    if sell.shape != want or buy.shape != want:
        raise ValueError(f"{path}: tables are {sell.shape} / {buy.shape}, "
                         f"expected {want}.")
    if (sell < 0).any() or (buy < 0).any():
        raise ValueError(f"{path}: a negative unit count.")
    return doc, sell, buy


TABLE, KAGGLE_FLOW, KAGGLE_BUY = _load()

#: int32 [N_DAYS, N_PRODUCTS], day-major exactly like `kagg2_flow.KAGG2_FLOW`
#: so `sim.market.apply_flow` can stack the two and gather on a table index.
KAGGLE_FLOW.flags.writeable = False
KAGGLE_BUY.flags.writeable = False

assert KAGGLE_FLOW.shape == (spec.N_DAYS, spec.N_PRODUCTS)
assert KAGGLE_BUY.shape == (spec.N_DAYS, spec.N_PRODUCTS)

#: Season totals of the rounded tables, for the provenance check in
#: `tests/test_kaggle_flow.py`.
SELL_TOTALS = tuple(int(x) for x in KAGGLE_FLOW.sum(0))
BUY_TOTALS = tuple(int(x) for x in KAGGLE_BUY.sum(0))

#: Longest single-day order in either table (wheat, day 29 -- the endgame
#: liquidation). `sim.market.FLOW_K` is sized off the max of this and
#: `kagg2_flow.MAX_DAY_UNITS`.
MAX_DAY_UNITS = int(max(KAGGLE_FLOW.max(), KAGGLE_BUY.max()))

#: How many games the table is a mean over, and which.
N_GAMES = int(TABLE["n_games"])
SOURCES = tuple(TABLE["sources"])
OPPONENTS = tuple(TABLE.get("opponents", ()))
MEASURED = str(TABLE["measured"])
