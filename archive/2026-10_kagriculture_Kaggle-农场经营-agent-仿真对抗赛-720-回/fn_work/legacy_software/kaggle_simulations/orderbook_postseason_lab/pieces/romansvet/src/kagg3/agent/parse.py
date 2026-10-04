"""Turn a kaggle_environments observation into the arrays the planner expects.

Only used by the submission; the JAX simulator carries the same fields natively.
Tile arrays come out in serpentine sweep order (plan.SERP).
"""

from __future__ import annotations

import numpy as np

from .. import spec
from ..core import plan as P

_KIND = {
    "WEED": spec.KIND_WEED,
    "PLANT": spec.KIND_PLANT,
    "COOP": spec.KIND_COOP,
    "PASTURE": spec.KIND_PASTURE,
}
_CROP_IX = {name: i for i, name in enumerate(spec.CROPS)}
_ANIMAL_IX = {name: i for i, name in enumerate(spec.ANIMALS)}
_ONGOING = {name for i, name in enumerate(spec.CROPS) if spec.CROP_ONGOING[i]}


def _doa(t, obs):
    """[SWITCH, NOOP_FIX] An ongoing crop the engine's `_decay_plants` turns to
    WEED before hour `NOOP_DOA_H` of the current day (units decay one per two
    steps from `max_lifespan_step`, after that step's unit actions)."""
    mls = int(t.get("max_lifespan_step", -1))
    if mls < 0 or t["crop"] not in _ONGOING:
        return False
    step = int(obs.get("day", 0)) * spec.TURNS_PER_DAY + int(obs.get("hour", 0))
    s1 = max(mls, step)
    s1 += (s1 - mls) % 2
    return s1 + 2 * max(0, int(t["yield_units"]) - 1) - step < P.NOOP_DOA_H


def parse_view(obs, player: int, opp_rate=None, opp_burst=None) -> P.DayView:
    farm = obs["farms"][player]
    priv = obs["private"]
    tiles = farm["tiles"]

    n = spec.N_TILES
    kind = np.empty(n, np.int32)
    occ = np.full(n, -1, np.int32)
    t_day = np.zeros(n, np.int32)
    t_water = np.zeros(n, np.int32)
    t_cons = np.zeros(n, np.int32)
    t_yield = np.zeros(n, np.int32)
    t_fert = np.full(n, -1, np.int32)
    t_cared = np.zeros(n, np.int32)
    t_favail = np.zeros(n, np.int32)
    t_bank = np.zeros(n, np.int32)

    for k, tid in enumerate(P.SERP):
        y, x = divmod(int(tid), spec.BOARD)
        t = tiles[y][x]
        if t is None:
            kind[k] = spec.KIND_EMPTY
            continue
        if t == "LOCKED":
            kind[k] = spec.KIND_LOCKED
            continue
        kd = t.get("kind")
        kind[k] = _KIND[kd]
        if kd == "PLANT":
            occ[k] = _CROP_IX[t["crop"]]
            t_day[k] = t["planted_day"]
            t_water[k] = 1 if t["watered_today"] else 0
            t_cons[k] = t["consecutive_unwatered"]
            t_yield[k] = t["yield_units"]
            t_fert[k] = t.get("fertilized_until_day", -1)
            if P.NOOP_FIX_ON and P.NOOP_FIX_DOA and _doa(t, obs):
                # [SWITCH, NOOP_FIX] WEED before hour NOOP_DOA_H: nothing any
                # route can still water or harvest here today.
                t_water[k], t_cons[k], t_yield[k] = 1, 0, 0
        elif kd in ("COOP", "PASTURE"):
            a = t.get("animal")
            if a is not None:
                occ[k] = _ANIMAL_IX[a]
                t_day[k] = t["placed_day"]
                t_water[k] = 1 if t["fed_today"] else 0
                t_cons[k] = t["consecutive_unfed"]
                t_yield[k] = t["yield_units"]
                t_cared[k] = 1 if t["cared_today"] else 0
                t_favail[k] = 1 if t["fertilizer_available"] else 0
                t_bank[k] = t.get("pending_care_bonus", 0)

    shed = np.zeros(spec.N_ITEMS, np.int32)
    for name, v in (priv.get("shed") or {}).items():
        ix = spec.ITEM_IX.get(name)
        if ix is not None:
            shed[ix] = v
    seeds = np.zeros(spec.N_CROPS, np.int32)
    for name, v in (priv.get("seeds") or {}).items():
        ix = _CROP_IX.get(name)
        if ix is not None:
            seeds[ix] = v

    opp_tiles = parse_public_tiles(obs, 1 - player)
    return P.DayView(
        day=np.int32(obs.get("day", 0)),
        kind=kind, occ=occ, t_day=t_day, t_water=t_water, t_cons=t_cons,
        t_yield=t_yield, t_fert=t_fert, t_cared=t_cared, t_favail=t_favail,
        shed=shed, seeds=seeds,
        money=np.int32(farm["money"]),
        nquad=np.int32(len(farm["unlocked_quadrants"])),
        price=np.array([obs["market"]["prices"][n] for n in spec.PRODUCTS], np.int32),
        mkt_inv=parse_market(obs)[0],
        shops=parse_town(obs),
        t_bank=t_bank,
        opp_commit=parse_opp_commit(obs, player),
        # PROGRAM1's selector-only public channel.  This is populated
        # unconditionally because it must reflect the dawn observation even
        # while every production switch (including opp_money) remains off.
        program_opp_money=parse_opp_money(obs, player),
        opp_kind=opp_tiles[0], opp_occ=opp_tiles[1],
        opp_t_day=opp_tiles[2], opp_t_yield=opp_tiles[3],
        seat=np.int32(player),
        # [SWITCH, SELL_SLOT_PRIORITY] The other seat's standing ripe yield.
        # A second pass over the same tiles, so it is only walked when the
        # switch that reads it is on; off, the field keeps its empty default.
        **({"opp_ripe": parse_opp_ripe(obs, player)}
           if P.SELL_SLOT_PRIORITY_ON else {}),
        # [SWITCH, SELL_SLOT_MIRROR_GATE] The other seat's money, for the
        # gate's lead veto. `obs.farms` carries both purses; an absent second
        # farm reads as zero, the same empty-rival identity as `opp_commit`.
        **({"opp_money": parse_opp_money(obs, player)}
           if P.SELL_SLOT_MIRROR_GATE_ON else {}),
        # [SWITCH, RIVAL_TELL] The rival's measured sale rate, handed down by
        # the runtime that keeps the per-turn history (`agent/tell.py`). None
        # -- the switch off, day 0-1, or any direct caller -- leaves the field
        # at its all-`-1` sentinel, which is "keep the proxy".
        **({"opp_rate": opp_rate} if opp_rate is not None else {}),
        # [SWITCH, SELL_SLOT_RIVALRANK] The rival's measured single-turn sale
        # burst, from the same `agent/tell.py` history. None -- the switch off,
        # days 0-1, any direct caller -- leaves the all-zero default, which is
        # a correction term of exactly zero.
        **({"opp_burst": opp_burst} if opp_burst is not None else {}),
    )


def parse_public_tiles(obs, player: int):
    """Public `(kind, occ, placed_day, yield)` arrays for one whole farm.

    The arrays follow `plan.SERP`, but selector features only reduce them over
    the complete board.  No identifiers, private shed/seeds, town future, or
    outcome fields are read.
    """
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = np.full(spec.N_TILES, -1, np.int32)
    placed = np.zeros(spec.N_TILES, np.int32)
    yld = np.zeros(spec.N_TILES, np.int32)
    farms = obs.get("farms") or []
    if not (0 <= player < len(farms)):
        return kind, occ, placed, yld
    tiles = farms[player].get("tiles") or []
    for k, tid in enumerate(P.SERP):
        y, x = divmod(int(tid), spec.BOARD)
        if y >= len(tiles) or x >= len(tiles[y]):
            continue
        tile = tiles[y][x]
        if tile is None:
            continue
        if tile == "LOCKED":
            kind[k] = spec.KIND_LOCKED
            continue
        kd = tile.get("kind")
        kind[k] = _KIND[kd]
        yld[k] = int(tile.get("yield_units") or 0)
        if kd == "PLANT":
            occ[k] = _CROP_IX.get(tile.get("crop"), -1)
            placed[k] = int(tile.get("planted_day") or 0)
        elif kd in ("COOP", "PASTURE"):
            occ[k] = _ANIMAL_IX.get(tile.get("animal"), -1)
            placed[k] = int(tile.get("placed_day") or 0)
    return kind, occ, placed, yld


def program_selector_features(obs, player: int) -> np.ndarray:
    """Compute PROGRAM1's 115-vector from this dawn observation only."""
    return np.asarray(P.program_selector_features(np, parse_view(obs, player)),
                      np.float32)


def parse_opp_money(obs, player: int) -> np.int32:
    """The OTHER seat's money. Read only by `plan.SELL_SLOT_MIRROR_GATE_ON`."""
    farms = obs.get("farms") or []
    q = 1 - player
    if not (0 <= q < len(farms)):
        return np.int32(0)
    return np.int32(farms[q].get("money", 0))


def parse_opp_commit(obs, player: int) -> np.ndarray:
    """int[9]: the OTHER seat's standing commitment per product.

    `kaggriculture.py` seats `obs.farms` whole -- both farms, tiles and all --
    so this is a fact the observation already carries. Same columns as
    `plan.opp_commitment`: crops in crop order, then one column per animal
    product, then FERTILIZER carrying the whole herd. A two-seat game is
    assumed and an absent second farm reads as an empty one, which is the
    identity for every rule that reads it.
    """
    commit = np.zeros(spec.N_PRODUCTS, np.int32)
    farms = obs.get("farms") or []
    q = 1 - player
    if not (0 <= q < len(farms)):
        return commit
    for row in farms[q]["tiles"]:
        for t in row:
            if not t or t == "LOCKED":
                continue
            kd = t.get("kind")
            if kd == "PLANT":
                c = _CROP_IX.get(t.get("crop"))
                if c is not None:
                    commit[c] += 1
            elif kd in ("COOP", "PASTURE"):
                a = _ANIMAL_IX.get(t.get("animal"))
                if a is not None:
                    commit[int(spec.ANIMAL_PRODUCT[a])] += 1
                    commit[spec.I_FERT] += 1
    return commit


def parse_opp_ripe(obs, player: int) -> np.ndarray:
    """int[9]: the OTHER seat's standing RIPE yield per product.

    The engine's own `yield_units`, which `obs.farms` carries for both seats;
    same columns as `plan.opp_ripe_yield`, which builds it in the simulator.
    FERTILIZER stays zero -- an animal's fertilizer is not a yield the tile is
    carrying. Read only by `plan.SELL_SLOT_PRIORITY_ON`.
    """
    ripe = np.zeros(spec.N_PRODUCTS, np.int32)
    farms = obs.get("farms") or []
    q = 1 - player
    if not (0 <= q < len(farms)):
        return ripe
    for row in farms[q]["tiles"]:
        for t in row:
            if not t or t == "LOCKED":
                continue
            kd = t.get("kind")
            y = int(t.get("yield_units") or 0)
            if not y:
                continue
            if kd == "PLANT":
                c = _CROP_IX.get(t.get("crop"))
                if c is not None:
                    ripe[c] += y
            elif kd in ("COOP", "PASTURE"):
                a = _ANIMAL_IX.get(t.get("animal"))
                if a is not None:
                    ripe[int(spec.ANIMAL_PRODUCT[a])] += y
    return ripe


def parse_market(obs):
    """(inventory[9], prices[9]) as int32."""
    inv = np.zeros(spec.N_PRODUCTS, np.int32)
    pr = np.zeros(spec.N_PRODUCTS, np.int32)
    m = obs["market"]
    for i, name in enumerate(spec.PRODUCTS):
        inv[i] = m["inventory"][name]
        pr[i] = m["prices"][name]
    return inv, pr


def parse_town(obs):
    """Count of each unlocked shop instance, in spec.SHOP_NAMES order."""
    counts = np.zeros(spec.N_SHOPS, np.int32)
    for name in obs["town"]["unlocked_shops"]:
        counts[spec.SHOP_NAMES.index(name)] += 1
    return counts
