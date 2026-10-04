"""An **action** tape: one recorded seat's per-step action dicts, as sim ops.

`es.tape_flow` replays a recorded opponent's per-day market *aggregates*
through `market.apply_flow`, with a generic archetype board standing behind
them. That surrogate is not the opponent: measured on 288 bit-exact boards its
margin correlates with the engine's at spearman 0.25 and it plays 8-12k coins
stronger than the tape does, so a theta ranking taken from it is worthless
(`scratchpad/simspike/NOTES.md`).

This module replays the *actions* instead -- the same dicts
`scripts/tape_opponent.py` packages into `artifacts/panel_opp/
opponent_tape_<ep>/main.py` and that our paired engine evaluations already run
against. Seat 1's `(uop, ua, uq)` and `(mop, ma, mq)` for a turn are a gather
from a precomputed table, and from there the turn goes through exactly the code
paths our own seat's plan goes through (`sim.units.apply_units`,
`sim.rollout._market_turn`), so the opponent's farm, shed, money, hires, land
and market pressure are all simulated rather than approximated.

Why this needs no unit-id mapping
---------------------------------
A recorded frame is `{"farmer": [...], "hands": [[...], ...], "market": [...]}`
and every unit order acts on the tile the unit is *standing on*: there are no
ids and no coordinates in it. The engine walks `[farmer, *hands]` by list
position (`interpreter`), which is the sim's unit-slot order exactly -- slot 0
is the farmer, slot h+1 is `hands[h]` -- and `_spawn_hand`'s placement rule is
already transcribed in `market._hire`. So the mapping is the identity, and the
only alignment the engine-side tape agent performs (truncate / pad `hands` to
the live roster) is what `units.apply_units`'s `real` mask already does.

Layout
------
The engine's 719 recorded steps are `step = day * 24 + hour`, so the table is
stored day-major, which is the shape `rollout.run_day` consumes:

    uop, ua, uq   int32 [N_DAYS, MAX_UNITS, TURNS_PER_DAY]
    mop, ma, mq   int32 [N_DAYS, TURNS_PER_DAY, MAX_MARKET_ORDERS]

`hours` is the set of hours on which the tape ever presents a market row. It is
static (it comes off the file, not off the trace), and `rollout` unions it with
its own `MARKET_TURNS` to decide which turns resolve a market row at all.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

from .. import spec
from ..core import ops as O

MU = spec.MAX_UNITS
TPD = spec.TURNS_PER_DAY
MO = spec.MAX_MARKET_ORDERS
ND = spec.N_DAYS

#: engine op name -> (sim op code, how to read `action[1]`)
#:   None    no argument
#:   "crop"  crop index (PLANT)
#:   "item"  item index (PICKUP / PLACE), with `action[2]` as the quantity
_UNIT_OPS = {
    "PASS": (O.OP_PASS, None),
    "NORTH": (O.OP_NORTH, None),
    "SOUTH": (O.OP_SOUTH, None),
    "EAST": (O.OP_EAST, None),
    "WEST": (O.OP_WEST, None),
    "PLANT": (O.OP_PLANT, "crop"),
    "WATER": (O.OP_WATER, None),
    "HARVEST": (O.OP_HARVEST, None),
    "FERTILIZE": (O.OP_FERTILIZE, None),
    "DIG": (O.OP_DIG, None),
    "BUILD_COOP": (O.OP_BUILD_COOP, None),
    "BUILD_PASTURE": (O.OP_BUILD_PASTURE, None),
    "FEED": (O.OP_FEED, None),
    "COLLECT_FERTILIZER": (O.OP_COLLECT_FERT, None),
    "CARE": (O.OP_CARE, None),
    "PICKUP": (O.OP_PICKUP, "item"),
    "DROP": (O.OP_DROP, None),
    "PLACE": (O.OP_PLACE, "item"),
}

#: engine market op -> (sim order code, index space of `order[1]`)
_MARKET_OPS = {
    "HIRE": (O.MO_HIRE, None),
    "BUY_LAND": (O.MO_BUY_LAND, None),
    "BUY_SEED": (O.MO_BUY_SEED, "crop"),
    "BUY_ANIMAL": (O.MO_BUY_ANIMAL, "animal"),
    "BUY_PRODUCT": (O.MO_BUY_PRODUCT, "product"),
    "SELL": (O.MO_SELL, "product"),
}

#: Ladder label of an action rung, `tape_act_<episode>`. Distinct from
#: `tape_flow.RUNG_PREFIX` on purpose: the two rungs replay the same recording
#: through different machinery, and a `--rung-weight` naming one must never
#: silently weight the other.
RUNG_PREFIX = "tape_act_"


def rung_name(episode) -> str:
    return f"{RUNG_PREFIX}{episode}"


_CROP_IX = {n: i for i, n in enumerate(spec.CROPS)}
_ANIMAL_IX = {n: i for i, n in enumerate(spec.ANIMALS)}
_PRODUCT_IX = {n: i for i, n in enumerate(spec.PRODUCTS)}
_ITEM_IX = spec.ITEM_IX


class TapeActions(NamedTuple):
    """Device-resident action tape. `hours` is host-side and static.

    `town` is the recorded **town schedule** (`--with-town`), or `None` when the
    tape does not carry one -- which is every tape cut before the flag existed,
    and what keeps the sim's device program byte-identical for them. See
    `town_array` for the layout and `sim.eod.unlock_shop` for what reads it.
    """
    uop: object      # int32 [ND, MU, TPD]
    ua: object
    uq: object
    mop: object      # int32 [ND, TPD, MO]
    ma: object
    mq: object
    hours: tuple = ()
    episode: int = 0
    dropped: tuple = ()
    town: object = None      # int32 [ND] or None
    #: [HIRE-STICKY] `src_hands[d, h]` = the roster the RECORDED seat had when
    #: it computed the action at step `d * TPD + h` (`len(frame["hands"])`), and
    #: `mlen[d, h]` = the length of its recorded market row (clipped to `MO`,
    #: which is where `_process_market` truncates it). Both are `None` on a tape
    #: built before the fields existed -- every `.npz` on disk -- which is the
    #: static "this rung cannot run the hire-sticky reflex" case
    #: (`sim.rollout.HIRE_STICKY`), so the device program is unchanged for them.
    src_hands: object = None  # int32 [ND, TPD] or None
    mlen: object = None       # int32 [ND, TPD] or None


_SHOP_IX = {n: i for i, n in enumerate(spec.SHOP_NAMES)}

#: A day the recorded town unlocked nothing. `sim.eod.unlock_shop` reads the
#: whole row and forces the draw only where it is non-negative; the constant
#: lives there because that is the only code that interprets it.
from ..sim.eod import NO_UNLOCK        # noqa: E402,F401  (re-export)


def town_array(schedule) -> np.ndarray:
    """`[(day, "SHOP_NAME"), ...]` -> int32 [ND], `town[d]` = the shop instance
    the town gained *on* day `d` (`NO_UNLOCK` on every other day).

    `day` is the day the shop is first VISIBLE, which is the engine's
    `next_day`: `_end_of_day(day)` appends to `town["unlocked_shops"]` and the
    observation at `day + 1, hour 0` is the first one that carries it. Indexing
    by the visible day is what lets `unlock_shop` -- which runs at the end of
    day `d` -- read `town[d + 1]` and get the shop the recording gained there.
    """
    out = np.full(ND, NO_UNLOCK, np.int32)
    for day, name in schedule:
        d = int(day)
        ix = _SHOP_IX.get(name)
        if ix is None:
            raise ValueError(f"unknown shop {name!r}; expected one of {spec.SHOP_NAMES}")
        if not 0 <= d < ND:
            raise ValueError(f"town unlock on day {d}, outside 0..{ND - 1}")
        if out[d] != NO_UNLOCK:
            raise ValueError(f"two town unlocks recorded on day {d}")
        out[d] = ix
    return out


def town_schedule(town) -> list:
    """`town_array`'s inverse: int32 [ND] -> `[[day, "SHOP_NAME"], ...]`."""
    return [[int(d), spec.SHOP_NAMES[int(v)]]
            for d, v in enumerate(np.asarray(town)) if int(v) != NO_UNLOCK]


def _unit_row(action) -> tuple[int, int, int]:
    """One `["OP", ...]` order as `(op, arg, qty)`. Unknown ops become PASS."""
    if not isinstance(action, (list, tuple)) or not action:
        return O.OP_PASS, 0, 0
    name = action[0]
    hit = _UNIT_OPS.get(name)
    if hit is None:
        return O.OP_PASS, 0, 0
    op, kind = hit
    if kind is None:
        return op, 0, 0
    if len(action) < 2:
        # `_apply_unit_action` returns without acting on a PLANT / PICKUP /
        # PLACE that names no item.
        return O.OP_PASS, 0, 0
    if kind == "crop":
        ix = _CROP_IX.get(action[1])
        return (op, ix, 0) if ix is not None else (O.OP_PASS, 0, 0)
    ix = _ITEM_IX.get(action[1])
    if ix is None:
        return O.OP_PASS, 0, 0
    n = int(action[2]) if len(action) >= 3 else 1
    if n <= 0:
        return O.OP_PASS, 0, 0
    return op, ix, n


def _market_row(order) -> tuple[int, int, int]:
    """One market order as `(op, arg, qty)`; `_parse_order`'s rejections
    become MO_NONE, which is what a `None` order state does in the engine --
    the slot is *kept* (the engine pairs the seats by raw queue position, not
    by a compacted one), it just never commits."""
    if not isinstance(order, (list, tuple)) or not order:
        return O.MO_NONE, 0, 0
    hit = _MARKET_OPS.get(order[0])
    if hit is None:
        return O.MO_NONE, 0, 0
    op, space = hit
    if space is None:
        return op, 0, 1
    if len(order) < 3:
        return O.MO_NONE, 0, 0
    try:
        n = int(order[2])
    except (TypeError, ValueError):
        return O.MO_NONE, 0, 0
    if n <= 0:
        return O.MO_NONE, 0, 0
    table = {"crop": _CROP_IX, "animal": _ANIMAL_IX, "product": _PRODUCT_IX}[space]
    ix = table.get(order[1])
    if ix is None:
        # `_process_market` aborts the whole order on a malformed sub-op
        # (BUY_PRODUCT of something that is not WHEAT / FERTILIZER, SELL of an
        # animal); the slot stays but commits nothing.
        return O.MO_NONE, 0, 0
    if op == O.MO_BUY_PRODUCT and ix not in (spec.I_WHEAT, spec.I_FERT):
        return O.MO_NONE, 0, 0
    return op, ix, n


def build(tape: list[dict], episode: int = 0, town=None) -> TapeActions:
    """Recorded frames (`tape[s]` = the action taken at engine step s) -> arrays.

    `town` is `--with-town`'s `[(day, "SHOP_NAME"), ...]`, or `None`.
    """
    uop = np.zeros((ND, MU, TPD), np.int32)
    ua = np.zeros((ND, MU, TPD), np.int32)
    uq = np.zeros((ND, MU, TPD), np.int32)
    mop = np.zeros((ND, TPD, MO), np.int32)
    ma = np.zeros((ND, TPD, MO), np.int32)
    mq = np.zeros((ND, TPD, MO), np.int32)
    src_hands = np.zeros((ND, TPD), np.int32)
    mlen = np.zeros((ND, TPD), np.int32)
    hours, dropped = set(), []

    for step, frame in enumerate(tape):
        if step >= ND * TPD:
            break
        d, h = divmod(step, TPD)
        # [HIRE-STICKY] The source roster, recorded before anything is dropped:
        # `_align`'s truncation is what the LIVE seat does, this is what the
        # recording had. Clipped to the state's crew bound for the same reason
        # `units` is.
        src_hands[d, h] = min(len(frame.get("hands") or []), MU - 1)
        units = [frame.get("farmer") or ["PASS"], *(frame.get("hands") or [])]
        if len(units) > MU:
            # `MAX_UNITS` is the state's bound, not the engine's; no recorded
            # seat has ever come near it, so this is a loud-enough note rather
            # than a silent truncation.
            dropped.append(("hands", step, len(units)))
            units = units[:MU]
        for u, action in enumerate(units):
            uop[d, u, h], ua[d, u, h], uq[d, u, h] = _unit_row(action)

        row = list(frame.get("market") or [])
        if len(row) > MO:
            # `_process_market` truncates each seat's queue to
            # `maxMarketOrdersPerTurn` before it parses anything.
            dropped.append(("market", step, len(row)))
            row = row[:MO]
        # [HIRE-STICKY] where a re-issued HIRE is APPENDED: behind the recorded
        # row, including any slot `_market_row` rejected (the engine keeps a
        # refused order's slot -- the seats are paired by raw queue position).
        mlen[d, h] = len(row)
        for i, order in enumerate(row):
            mop[d, h, i], ma[d, h, i], mq[d, h, i] = _market_row(order)
        if np.any(mop[d, h] != O.MO_NONE):
            hours.add(h)

    return TapeActions(uop, ua, uq, mop, ma, mq,
                       hours=tuple(sorted(hours)), episode=int(episode),
                       dropped=tuple(dropped),
                       town=None if town is None else town_array(town),
                       src_hands=src_hands, mlen=mlen)


def save(path, ta: TapeActions) -> None:
    """`town` is written only when the tape carries one, so a tape cut without
    `--with-town` is the same six-array file it always was and an older reader
    keeps loading it."""
    extra = {} if ta.town is None else {"town": np.asarray(ta.town, np.int32)}
    # Same rule for the hire-sticky pair: written only when the tape carries
    # them, so a reader that predates them loads the file it always loaded.
    for f in ("src_hands", "mlen"):
        if getattr(ta, f) is not None:
            extra[f] = np.asarray(getattr(ta, f), np.int32)
    np.savez_compressed(
        path, uop=ta.uop, ua=ta.ua, uq=ta.uq, mop=ta.mop, ma=ta.ma, mq=ta.mq,
        hours=np.asarray(ta.hours, np.int32), episode=np.int32(ta.episode), **extra)


def load_many(paths) -> list:
    """`--tape-actions` paths -> loaded tables, refusing a duplicate episode.

    Two rungs with one name would collide in `Trainer._bind_rungs`'s
    name -> slot map and silently drop one of them, so it is refused here,
    seconds into the run, rather than after a gate.
    """
    out = [load(p) for p in paths]
    seen = {}
    for path, ta in zip(paths, out):
        if ta.episode in seen:
            raise ValueError(f"--tape-actions names episode {ta.episode} twice: "
                             f"{seen[ta.episode]} and {path}")
        seen[ta.episode] = path
    return out


def load(path) -> TapeActions:
    """`town` is optional: a file without the key loads as `town=None`, which is
    the static "this rung draws its own shops" case the sim has always run."""
    z = np.load(path)
    opt = {f: (z[f].astype(np.int32) if f in z.files else None)
           for f in ("town", "src_hands", "mlen")}
    return TapeActions(
        z["uop"].astype(np.int32), z["ua"].astype(np.int32), z["uq"].astype(np.int32),
        z["mop"].astype(np.int32), z["ma"].astype(np.int32), z["mq"].astype(np.int32),
        hours=tuple(int(h) for h in z["hours"]), episode=int(z["episode"]), **opt)


def device(xp, ta: TapeActions) -> TapeActions:
    """The action arrays (and `town`, when there is one) as device arrays;
    `hours` / `episode` stay host-side."""
    out = {f: xp.asarray(getattr(ta, f)) for f in TapeActions._fields[:6]}
    for f in ("town", "src_hands", "mlen"):
        if getattr(ta, f) is not None:
            out[f] = xp.asarray(getattr(ta, f))
    return ta._replace(**out)


def stack(tapes: list[TapeActions]) -> TapeActions:
    """One leading axis over several tapes, for `vmap` over a batch of boards.

    `hours` is the *union*: the market-turn schedule is read at trace time and
    one program serves the whole batch, so every turn any member trades on has
    to resolve for all of them.

    `town` is stacked to [T, ND] as soon as ANY member carries one; a member
    that does not gets an all-`NO_UNLOCK` row, which `sim.eod.unlock_shop` reads
    as "draw this board's shops as usual". A batch where nobody carries one
    stays `None`, so its device program is unchanged.
    """
    hours = tuple(sorted(set().union(*[set(t.hours) for t in tapes])))
    town = None
    if any(t.town is not None for t in tapes):
        town = np.stack([np.full(ND, NO_UNLOCK, np.int32) if t.town is None
                         else np.asarray(t.town, np.int32) for t in tapes])
    # [HIRE-STICKY] Same rule as `town`, and an all-zero row is the right
    # stand-in for a member that carries no roster: `owed` never leaves 0, so
    # that tape runs the frozen row it always ran even with the flag on.
    sticky = {}
    for f, shape in (("src_hands", (ND, TPD)), ("mlen", (ND, TPD))):
        if any(getattr(t, f) is not None for t in tapes):
            sticky[f] = np.stack([np.zeros(shape, np.int32) if getattr(t, f) is None
                                  else np.asarray(getattr(t, f), np.int32)
                                  for t in tapes])
    return TapeActions(*[np.stack([t[i] for t in tapes]) for i in range(6)],
                       hours=hours, episode=0, town=town, **sticky)


def _package_ns(main_py) -> dict:
    src = open(main_py).read()
    ns: dict = {}
    exec(compile(src, str(main_py), "exec"), ns)     # noqa: S102 - our own file
    return ns


def tape_from_package(main_py) -> list[dict]:
    """The `_TAPE` list out of a `scripts/tape_opponent.py` package."""
    return list(_package_ns(main_py)["_TAPE"])


def town_from_package(main_py) -> list:
    """The `_TOWN` schedule out of a `scripts/tape_opponent.py --with-town`
    package: `[[day, "SHOP_NAME"], ...]`, empty for a package cut without it."""
    return [list(row) for row in (_package_ns(main_py).get("_TOWN") or [])]
