"""Simulator state and the derived tables it gathers from.

Layout notes
------------
* Tile arrays are in **row-major tile id** order (`y * BOARD + x`), matching the
  engine. The planner works in serpentine order, so building a DayView gathers
  through `plan.SERP` and scattering results back gathers through `SERP_INV`.
* `money` is int32. The engine stores a float, but starting money and every
  price, cost and land fee are integers, so money is exactly integral all season
  and int32 removes any float-comparison ambiguity from `money < cost`.
* Everything is a flat array, so `vmap` over a batch of episodes just adds a
  leading axis.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

from .. import spec

MU = spec.MAX_UNITS
NT = spec.N_TILES
NP = spec.N_PRODUCTS
NI = spec.N_ITEMS

# Largest number of units one market order can move in a single slot. SELL is
# bounded by shed[item] and BUY_PRODUCT / BUY_ANIMAL by shed room, and the shed
# holds at most SHED_CAPACITY, so 100 units is a hard cap. BUY_SEED is unbounded
# but has a fixed price and needs no per-unit walk.
MAX_UNITS_PER_ORDER = spec.SHED_CAPACITY


class Tables(NamedTuple):
    """Host-built, device-resident lookup tables. Never recomputed on device."""
    price: object       # int32 [9, PRICE_TABLE_N]  price at each absolute inventory


class State(NamedTuple):
    step: object            # int32   scalar turn counter
    money: object           # int32   [2]
    kind: object            # int32   [2, 100]
    occ: object             # int32   [2, 100]  crop idx / animal idx / -1
    t_day: object           # int32   [2, 100]  planted_day / placed_day
    t_water: object         # int32   [2, 100]  watered_today / fed_today
    t_cons: object          # int32   [2, 100]  consecutive_unwatered / unfed
    t_yield: object         # int32   [2, 100]
    t_life: object          # int32   [2, 100]  max_lifespan_step, -1 for ongoing
    t_fert: object          # int32   [2, 100]  fertilized_until_day, -1
    t_cared: object         # int32   [2, 100]
    t_favail: object        # int32   [2, 100]
    t_bank: object          # int32   [2, 100]  pending_care_bonus
    shed: object            # int32   [2, 12]
    seeds: object           # int32   [2, 5]
    inv: object             # int32   [2, MU, 12]  per-unit inventories
    inv_seq: object         # int32   [2, MU, 12]  turn each item first appeared
                            #         (the engine drops inventories in dict
                            #          insertion order, which decides who
                            #          survives a shed overflow)
    upos: object            # int32   [2, MU]      tile id of each unit
    nhands: object          # int32   [2]
    hires_today: object     # int32   [2]
    nquad: object           # int32   [2]
    mkt_inv: object         # int32   [9]
    shops: object           # int32   [8]  instance count per shop type
    nshops: object          # int32   scalar
    # --- sale ledger, per seat. Written only under `rollout.run_day(
    # day_metrics=True)`; on every other rollout they stay at their zero init
    # and not one instruction updates them, so the season is the season it
    # always was. They exist so the ES can price *how* a seat sells, not only
    # what it ends with -- 30 recorded top-10 games realise +19k over days
    # 15-29 at flat volume, through 2.1x our SELL rows in half-size slices.
    sold_n: object          # int32 [2]  cumulative units sold to the market
    sold_rev: object        # int32 [2]  cumulative coins those sales paid
    sold_rows: object       # int32 [2]  cumulative SELL slots that moved a unit
    sold_ni: object         # int32 [2, NI] [WHEATMIX1] units sold per item (same writer as sold_n)
    sold_ri: object         # int32 [2, NI] [WHEATMIX1] coins per item


def build_tables(xp, params=None) -> Tables:
    return Tables(price=xp.asarray(spec.build_price_table(params)))


def floor_inventory(params=None) -> np.ndarray:
    """Lowest market inventory at which each product's price hits the $1 floor.

    Diagnostic, not used by the rollout -- the market walk tests `price > 1`
    directly. It is worth computing because these numbers are the single most
    important strategic fact in the game: several premium products floor only
    tens of units above the starting inventory, which makes market saturation,
    not production capacity, the binding constraint.
    """
    price = spec.build_price_table(params)
    at_floor = price <= spec.PRICE_FLOOR
    first = np.argmax(at_floor, axis=1)
    zidx = np.where(at_floor.any(axis=1), first, spec.PRICE_TABLE_N)
    return (zidx + spec.PRICE_TABLE_LO).astype(np.int32)


def initial_state(xp, nquad=None, money=None) -> State:
    """Mirror of _initialize / _new_farm for a two-player default episode.

    `nquad` / `money` (int32 [2], per seat) describe a **warm start**: the first
    `nquad - 1` extra quadrants are already unlocked in the engine's own
    purchase order (`LAND_ORDER`: NE, SW, SE) and the seat holds `money`
    coins. Omitted, both default to the engine's day 0, which is the only
    start the submission and the equivalence gate ever use. Training uses warm
    starts for a fraction of episodes so that multi-quadrant play receives a
    gradient at all -- see `es.train.Trainer.draw_starts`.
    """
    i32 = xp.int32
    if nquad is None:
        nquad = xp.ones((2,), i32)
    if money is None:
        money = xp.full((2,), spec.STARTING_MONEY, i32)
    quad = xp.asarray(spec.TILE_QUAD)
    # Rank of each quadrant in the purchase order: NW is 0, then LAND_ORDER.
    order = xp.asarray(np.concatenate([[0], spec.LAND_ORDER]).astype(np.int32))
    quad_rank = xp.sum((order[None, :] == quad[:, None]).astype(i32)
                       * xp.arange(4, dtype=i32)[None, :], axis=1)
    unlocked = quad_rank[None, :] < xp.asarray(nquad, i32)[:, None]
    kind = xp.where(unlocked, spec.KIND_EMPTY, spec.KIND_LOCKED).astype(i32)
    z2 = xp.zeros((2, NT), i32)
    spawn = xp.full((2, MU), spec.DEFAULT_SPAWN_TILE, i32)
    return State(
        step=xp.asarray(0, i32),
        money=xp.asarray(money, i32),
        kind=kind,
        occ=z2 - 1,
        t_day=z2, t_water=z2, t_cons=z2, t_yield=z2,
        t_life=z2 - 1, t_fert=z2 - 1, t_cared=z2, t_favail=z2, t_bank=z2,
        shed=xp.zeros((2, NI), i32),
        seeds=xp.zeros((2, spec.N_CROPS), i32),
        inv=xp.zeros((2, MU, NI), i32),
        inv_seq=xp.full((2, MU, NI), 1 << 20, i32),
        upos=spawn,
        nhands=xp.zeros((2,), i32),
        hires_today=xp.zeros((2,), i32),
        nquad=xp.asarray(nquad, i32),
        mkt_inv=xp.full((NP,), spec.MARKET_I0, i32),
        shops=xp.zeros((spec.N_SHOPS,), i32),
        nshops=xp.asarray(0, i32),
        sold_n=xp.zeros((2,), i32),
        sold_rev=xp.zeros((2,), i32),
        sold_rows=xp.zeros((2,), i32),
        sold_ni=xp.zeros((2, NI), i32),
        sold_ri=xp.zeros((2, NI), i32),
    )


def prices_of(xp, tables: Tables, mkt_inv):
    """Current quoted price of every product."""
    return tables.price[xp.arange(NP), mkt_inv - spec.PRICE_TABLE_LO]
