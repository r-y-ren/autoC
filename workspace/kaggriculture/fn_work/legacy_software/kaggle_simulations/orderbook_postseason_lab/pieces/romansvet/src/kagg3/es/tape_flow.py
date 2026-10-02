"""One Kaggle opponent's measured market flow, as a training rung.

Why this exists
---------------
`kagg2_flow` and `kaggle_flow` are the right *kind* of opponent -- replay a
real market footprint instead of simulating a planner that makes one -- and
both are **means**: kagg2's is one bot averaged over 64 games, the Kaggle
field's is twelve different losers averaged into a centre. A mean is the right
target for "the field", and the wrong target for the two opponents that
actually hold the champion to a coin flip.

`scripts/tape_opponent.py` packages those two as verbatim tapes, and they beat
us 50/50 over 32 real-engine games. The tape is an *engine* opponent, though:
it emits action dicts, and the fast sim has no action-dict seat to feed them
to. What the sim can replay is the part of a tape that sets the prices the
policy is optimising against -- its per-day SELL / BUY_PRODUCT units -- which
is exactly what `sim.market.apply_flow` already walks, and exactly what
`scripts/replay_flow.py` already measures off a replay.

So a tape rung is one replay seat's *own* flow table, not a mean over games:

    python scripts/make_tape_rung.py replays/L_103254816.json \
        --ours "OurTeam" -o artifacts/tape_games/103254816.npz
    python scripts/train.py ... --tape-rung artifacts/tape_games/103254816.npz \
        --rung-weight tape_103254816=3

What it is not
--------------
It is not the tape. The tape's turn-by-turn plan -- when it hires, where it
walks, which tile it plants -- is not replayed; a planner archetype
(`es.train.TAPE_PLANNER`, the `wheat_clone` the class-A field is made of)
stands behind the rung to put a board in front of the policy's opponent
features, exactly as `kaggle_flow`'s does. What is verbatim is the *market
presence*, and the market presence is what moves the quotes.

Nor is it played verbatim: `es.train.Trainer.episode_flow` draws a scale and a
day shift per episode pair for this rung as it does for the other two
(`--tape-flow-scale` / `--tape-flow-shift`, defaulting to the kagg2 rung's
ranges). A single game's table is the most overfittable measurement in the
ladder -- it is n=1 -- so the randomisation matters more here, not less.

Format
------
An `.npz` written by `scripts/make_tape_rung.py`:

  ``sell``  int32 [N_DAYS, N_PRODUCTS] -- units this seat SOLD on each day
  ``buy``   int32 [N_DAYS, N_PRODUCTS] -- units it BOUGHT (BUY_PRODUCT)
  ``grow``  int32 [N_DAYS, N_PRODUCTS] -- units that entered the seat's shed
            that day by any route *other* than the market, net of the
            non-market ones that left it (feeding wheat to animals, a PICKUP
            carried off to fertilise). **Signed**, and optional: a table cut
            before 2026-09-05 has no `grow` and `load` returns `None` for it.
  ``meta``  a JSON string: the episode, both team names, which seat was
            measured, the seat's final money, the source replay, and --
            when `grow` is present -- `grow_source` ("shed_delta" or
            "actions").

Column order is `spec.PRODUCTS` and it is stored in `meta` as well, so a
mislabelled table is refused at load rather than trained on.

Why `grow` exists
-----------------
`sim.market.apply_flow`'s `--tape-flow-backed` clamp is only the engine's rule
if the flow seat's board grows what the table sells, and the rung's board is a
wheat clone that never holds strawberry / milk / wool / fertilizer. Clamping
against that shed does not shrink the opponent, it deletes it. `grow` is the
missing half of the measurement: credited to the flow seat's shed before the
day's sells are clamped, the seat sells what it actually produced, at the
sim's prices -- which include our seat's market pressure.

Sign convention
---------------
Per day `d`, with `shed[d]` the seat's shed at the *start* of day `d`::

    shed[d + 1] = shed[d] + grow[d] - sell[d] + buy[d]
    grow[d]     = shed[d + 1] - shed[d] + sell[d] - buy[d]

so `grow` is positive where the day's harvests / collections outweigh what the
seat picked back out of the shed, and negative where they do not.
"""

from __future__ import annotations

import json
import os
from typing import NamedTuple

import numpy as np

from .. import spec

#: Every tape rung's ladder label starts with this, so `--rung-weight` names
#: read as what they are and no measured-mean rung can collide with one.
RUNG_PREFIX = "tape_"


def rung_name(episode) -> str:
    """The ladder label for a tape cut from `episode`. -> str."""
    return f"{RUNG_PREFIX}{episode}"


class TapeFlow(NamedTuple):
    """One replay seat's measured per-day market footprint."""
    name: str                   #: ladder label, `tape_<episode>`
    sell: np.ndarray            #: int32 [N_DAYS, N_PRODUCTS]
    buy: np.ndarray             #: int32 [N_DAYS, N_PRODUCTS]
    meta: dict                  #: provenance, see the module docstring
    path: str = ""              #: where it was loaded from
    #: int32 [N_DAYS, N_PRODUCTS], **signed**, or `None` on a table cut before
    #: `grow` existed. Last so that the one positional construction below and
    #: any caller unpacking a `TapeFlow` keep reading the same fields.
    grow: np.ndarray = None

    @property
    def grow_source(self) -> str:
        """How `grow` was derived. -> "shed_delta" / "actions" / ""."""
        return str(self.meta.get("grow_source", "")) if self.grow is not None else ""

    @property
    def max_day_units(self) -> int:
        """The busiest single day in either table -- `sim.market.FLOW_K`'s input."""
        return int(max(self.sell.max(initial=0), self.buy.max(initial=0)))

    @property
    def sell_totals(self) -> tuple:
        return tuple(int(x) for x in self.sell.sum(0))

    @property
    def buy_totals(self) -> tuple:
        return tuple(int(x) for x in self.buy.sum(0))


def _check(path, name, arr, signed=False):
    """Shape and (unless `signed`) sign check on one table. -> arr.

    `grow` is the one signed table: a day that fed more wheat to the animals
    than it harvested is a real day, and refusing it would be refusing the
    measurement rather than a mistake in it.
    """
    want = (int(spec.N_DAYS), int(spec.N_PRODUCTS))
    if arr.shape != want:
        raise ValueError(f"{path}: `{name}` is {arr.shape}, expected {want}.")
    if not signed and (arr < 0).any():
        raise ValueError(f"{path}: `{name}` holds a negative unit count.")
    return arr


def save(path, sell, buy, meta, grow=None):
    """Write a tape rung. -> path.

    The product order and the day count go into `meta` as well as being
    asserted here: a table whose columns are not `spec.PRODUCTS` is not a
    weaker measurement, it is a different one, and `load` refuses it.

    `grow` is optional and additive: omitted, the file written is byte for byte
    the file this function wrote before `grow` existed.
    """
    sell = _check(path, "sell", np.asarray(sell, np.int32))
    buy = _check(path, "buy", np.asarray(buy, np.int32))
    meta = dict(meta)
    meta.setdefault("products", list(spec.PRODUCTS))
    meta.setdefault("days", int(spec.N_DAYS))
    d = os.path.dirname(os.path.abspath(path))
    if d:
        os.makedirs(d, exist_ok=True)
    extra = {}
    if grow is not None:
        extra["grow"] = _check(path, "grow", np.asarray(grow, np.int32),
                               signed=True)
        meta.setdefault("grow_source", "shed_delta")
    np.savez(path, sell=sell, buy=buy, meta=np.str_(json.dumps(meta,
                                                              sort_keys=True)),
             **extra)
    return path


def load(path) -> TapeFlow:
    """Read a tape rung written by `save`. -> TapeFlow.

    Everything that could silently mean the wrong thing is checked: the column
    order against `spec.PRODUCTS`, the day count, the shapes and the sign. The
    rung is an opponent the gradient sees for the whole run; a table whose
    columns are one product out would train against a market nobody makes.
    """
    with np.load(path, allow_pickle=False) as z:
        if "sell" not in z or "buy" not in z:
            raise ValueError(f"{path}: not a tape rung -- no `sell`/`buy` "
                             f"arrays (has {sorted(z.files)}).")
        sell = _check(path, "sell", np.asarray(z["sell"], np.int32))
        buy = _check(path, "buy", np.asarray(z["buy"], np.int32))
        grow = (_check(path, "grow", np.asarray(z["grow"], np.int32), signed=True)
                if "grow" in z else None)
        meta = json.loads(str(z["meta"])) if "meta" in z else {}
    products = list(meta.get("products", spec.PRODUCTS))
    if products != list(spec.PRODUCTS):
        raise ValueError(
            f"{path}: product order {products} is not spec.PRODUCTS "
            f"{list(spec.PRODUCTS)}; the table's columns would be mislabelled.")
    if int(meta.get("days", spec.N_DAYS)) != int(spec.N_DAYS):
        raise ValueError(f"{path}: {meta['days']} days, spec says {spec.N_DAYS}.")
    episode = meta.get("episode")
    name = meta.get("rung") or rung_name(
        episode if episode is not None else
        os.path.splitext(os.path.basename(path))[0])
    if not str(name).startswith(RUNG_PREFIX):
        raise ValueError(f"{path}: rung label {name!r} does not start with "
                         f"{RUNG_PREFIX!r}; a tape rung has to be tellable "
                         f"from a measured-mean one by name alone.")
    sell.flags.writeable = False
    buy.flags.writeable = False
    if grow is not None:
        grow.flags.writeable = False
    return TapeFlow(str(name), sell, buy, meta, str(path), grow)


def load_many(paths):
    """`load` each path, refusing a repeated rung name. -> (TapeFlow, ...)

    Two tapes with one label would take one ladder slot between them and the
    second would silently never be played -- and `--rung-weight` could not name
    either.
    """
    out = []
    seen = {}
    for p in paths:
        t = load(p)
        if t.name in seen:
            raise ValueError(f"two tape rungs called {t.name!r}: {seen[t.name]} "
                             f"and {p}. One label is one ladder slot.")
        seen[t.name] = p
        out.append(t)
    return tuple(out)
