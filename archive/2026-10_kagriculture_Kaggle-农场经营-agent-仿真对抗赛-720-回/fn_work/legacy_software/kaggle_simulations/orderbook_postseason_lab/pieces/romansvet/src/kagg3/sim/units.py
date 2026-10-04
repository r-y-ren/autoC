"""Sequential per-turn unit actions matching the reference engine's unit order.

Real planner and tape vectors can contain multiple units acting on one tile.
All mutable farm, shed, seed, and inventory state is therefore carried through
unit indices. Atomic PLANT blocking is computed once from the initial vector.
"""
from __future__ import annotations

from jax import lax
from .. import spec
from ..core import ops as O

MU = spec.MAX_UNITS
NT = spec.N_TILES
NI = spec.N_ITEMS
_BIG_SEQ = 1 << 20


def _onehot(xp, idx, n, dtype):
    return (xp.arange(n, dtype=xp.int32) == idx).astype(dtype)


def _prepare_ops(xp, st, uop, ua):
    """Mask inactive units and apply the engine's turn-atomic PLANT rejection."""
    out = uop
    for p in range(2):
        real = xp.arange(MU, dtype=xp.int32) < (1 + st.nhands[p])
        op = xp.where(real, out[p], O.OP_PASS)
        valid_arg = (((op != O.OP_PLANT) | ((ua[p] >= 0) & (ua[p] < spec.N_CROPS)))
                     & (((op != O.OP_PICKUP) & (op != O.OP_PLACE))
                        | ((ua[p] >= 0) & (ua[p] < NI))))
        op = xp.where((op >= O.OP_PASS) & (op < O.N_OPS) & valid_arg, op, O.OP_PASS)
        plant = op == O.OP_PLANT
        crop = xp.clip(ua[p], 0, spec.N_CROPS - 1)
        demand = xp.sum((xp.arange(spec.N_CROPS)[None, :] == ua[p, :, None]).astype(xp.int32)
                        * plant[:, None], axis=0)
        blocked = demand > st.seeds[p]
        op = xp.where(plant & blocked[crop], O.OP_PASS, op)
        out = out.at[p].set(op)
    return out


def _apply_one(xp, st, day, op, arg, qty, p, j):
    """Apply one already-masked unit action to the current carried State."""
    i32 = xp.int32
    pos = st.upos[p, j]
    inv_before = st.inv[p, j]
    seq_before = st.inv_seq[p, j]

    # Movement returns immediately in the engine; op predicates below make all
    # other changes no-ops while the position update observes board bounds.
    x, y = pos % spec.BOARD, pos // spec.BOARD
    dx = (op == O.OP_EAST).astype(i32) - (op == O.OP_WEST).astype(i32)
    dy = (op == O.OP_SOUTH).astype(i32) - (op == O.OP_NORTH).astype(i32)
    nx, ny = x + dx, y + dy
    moving = (dx != 0) | (dy != 0)
    in_board = (nx >= 0) & (nx < spec.BOARD) & (ny >= 0) & (ny < spec.BOARD)
    newpos = xp.where(moving & in_board, ny * spec.BOARD + nx, pos)

    # Read the current tile before deciding PLACE precedence. A previous unit
    # may have changed it during this same turn.
    k = st.kind[p, pos]
    o = st.occ[p, pos]
    shed_adj = xp.asarray(spec.IS_SHED_ADJACENT)[pos]
    pa = xp.clip(arg - spec.I_GOOSE, 0, spec.N_ANIMALS - 1)
    animal_branch = ((op == O.OP_PLACE) & (arg >= spec.I_GOOSE) & (arg < NI)
                    & ((k == spec.KIND_COOP) | (k == spec.KIND_PASTURE))
                    & (o < 0) & (k == xp.asarray(spec.ANIMAL_STRUCT)[pa]))
    animal_place = animal_branch & (inv_before[xp.clip(arg, 0, NI - 1)] > 0)

    # Shed branches execute before the LOCKED guard and carry immediately to
    # the next unit. DROP destroys the entire load even when capacity is short;
    # PLACE deposits only what fits and retains its remainder.
    want_pick = (op == O.OP_PICKUP) & shed_adj & (qty > 0)
    item = xp.clip(arg, 0, NI - 1)
    pick = _onehot(xp, item, NI, i32) * xp.where(
        want_pick, xp.minimum(qty, st.shed[p, item]), 0)
    shed = st.shed[p] - pick
    drop = (op == O.OP_DROP) & shed_adj
    place_shed = (op == O.OP_PLACE) & shed_adj & ~animal_branch & (qty > 0)
    place_n = xp.where(place_shed, xp.minimum(qty, inv_before[item]), 0)
    deposit_want = xp.where(drop, inv_before,
                            _onehot(xp, item, NI, i32) * place_n)
    order = xp.argsort(seq_before * NI + xp.arange(NI, dtype=i32))
    ordered = deposit_want[order]
    room = xp.maximum(spec.SHED_CAPACITY - xp.sum(shed), 0)
    cumulative = xp.cumsum(ordered)
    dep_ordered = xp.minimum(room, cumulative) - xp.minimum(room, cumulative - ordered)
    deposited = xp.zeros(NI, i32).at[order].set(dep_ordered)
    shed = shed + deposited
    inv = inv_before + pick - xp.where(drop, inv_before, deposited)

    locked = k == spec.KIND_LOCKED
    is_plant = (k == spec.KIND_PLANT) & ~locked
    is_structure = ((k == spec.KIND_COOP) | (k == spec.KIND_PASTURE)) & ~locked
    has_animal = is_structure & (o >= 0)
    empty = k == spec.KIND_EMPTY
    yld = st.t_yield[p, pos]
    crop = xp.clip(o, 0, spec.N_CROPS - 1)
    animal = xp.clip(o, 0, spec.N_ANIMALS - 1)
    age = day - st.t_day[p, pos]
    crop_ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    crop_first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    crop_max_day = xp.asarray(spec.CROP_MAX_YIELD_DAY)[crop]
    crop_window = xp.asarray(spec.CROP_WINDOW_START)[crop]
    crop_max = xp.asarray(spec.CROP_MAX_YIELD)[crop]

    plant_crop = xp.clip(arg, 0, spec.N_CROPS - 1)
    plant_ongoing = xp.asarray(spec.CROP_ONGOING)[plant_crop]
    plant_max_day = xp.asarray(spec.CROP_MAX_YIELD_DAY)[plant_crop]
    do_plant = (op == O.OP_PLANT) & empty & (st.seeds[p, plant_crop] > 0)
    do_water = (op == O.OP_WATER) & is_plant & (st.t_water[p, pos] == 0)
    in_window = (crop_ongoing == 0) & (age >= crop_window) & (age <= crop_max_day)
    water_bonus = xp.where(st.t_fert[p, pos] >= day, 2, 1)
    water_yield = xp.where(in_window, xp.minimum(crop_max, yld + water_bonus), yld)
    harvest_plant = (op == O.OP_HARVEST) & is_plant & (yld > 0) & (age >= crop_first)
    harvest_animal = (op == O.OP_HARVEST) & has_animal & (yld > 0)
    harvest_once = harvest_plant & (crop_ongoing == 0)
    do_fert = (op == O.OP_FERTILIZE) & is_plant & (inv[spec.I_FERT] > 0)
    do_feed = ((op == O.OP_FEED) & has_animal & (st.t_water[p, pos] == 0)
               & (inv[spec.I_WHEAT] > 0))
    do_collect = (op == O.OP_COLLECT_FERT) & has_animal & (st.t_favail[p, pos] == 1)
    do_care = (op == O.OP_CARE) & has_animal & (st.t_cared[p, pos] == 0)
    do_dig = (op == O.OP_DIG) & ~locked & (k != spec.KIND_EMPTY) & ~has_animal
    do_coop = (op == O.OP_BUILD_COOP) & empty
    do_pasture = (op == O.OP_BUILD_PASTURE) & empty
    do_place = animal_place
    reset = do_plant | do_place | do_coop | do_pasture | do_dig | harvest_once

    new_kind = xp.where(do_plant, spec.KIND_PLANT,
               xp.where(harvest_once | do_dig, spec.KIND_EMPTY,
               xp.where(do_coop, spec.KIND_COOP,
               xp.where(do_pasture, spec.KIND_PASTURE, k))))
    new_occ = xp.where(do_plant, plant_crop,
              xp.where(harvest_once | do_dig | do_coop | do_pasture, -1,
              xp.where(do_place, pa, o)))
    write_tile = do_plant | harvest_once | do_dig | do_coop | do_pasture | do_place
    kind = st.kind.at[p, pos].set(xp.where(write_tile, new_kind, k))
    occ = st.occ.at[p, pos].set(xp.where(write_tile, new_occ, o))

    def tile_set(arr, value, active):
        old = arr[p, pos]
        return arr.at[p, pos].set(xp.where(active, value, old))

    t_day = tile_set(st.t_day, xp.where(do_plant | do_place, day, 0),
                     do_plant | do_place | reset)
    t_water = tile_set(st.t_water, xp.where(do_water | do_feed, 1, 0),
                       do_water | do_feed | reset)
    t_cons = tile_set(st.t_cons, xp.where(do_plant, 1, 0), do_plant | reset)
    new_yield = xp.where(do_water, water_yield, yld)
    new_yield = xp.where(harvest_plant | harvest_animal, 0, new_yield)
    new_yield = xp.where(do_plant, xp.where(plant_ongoing == 1, 0, 1), new_yield)
    new_yield = xp.where(do_place | do_coop | do_pasture | do_dig, 0, new_yield)
    t_yield = tile_set(st.t_yield, new_yield,
                       do_water | harvest_plant | harvest_animal | reset)
    t_life = tile_set(st.t_life,
        xp.where(do_plant, xp.where(plant_ongoing == 1, -1,
                 (day + plant_max_day + 1) * spec.TURNS_PER_DAY), -1), do_plant | reset)
    t_fert = tile_set(st.t_fert,
        xp.where(do_fert, xp.maximum(st.t_fert[p, pos], day + 2), -1), do_fert | reset)
    t_cared = tile_set(st.t_cared, xp.where(do_care, 1, 0), do_care | reset)
    t_favail = tile_set(st.t_favail, xp.asarray(0, dtype=st.t_favail.dtype), do_collect | reset)
    t_bank = tile_set(st.t_bank, xp.asarray(0, dtype=st.t_bank.dtype), reset)

    product = xp.asarray(spec.ANIMAL_PRODUCT)[animal]
    gain = (_onehot(xp, crop, NI, i32) * xp.where(harvest_plant, yld, 0)
            + _onehot(xp, product, NI, i32) * xp.where(harvest_animal, yld, 0)
            + _onehot(xp, spec.I_FERT, NI, i32) * do_collect
            - _onehot(xp, spec.I_FERT, NI, i32) * do_fert
            - _onehot(xp, spec.I_WHEAT, NI, i32) * do_feed
            - _onehot(xp, item, NI, i32) * do_place)
    inv = inv + gain
    appeared = (inv_before == 0) & (inv > 0)
    gone = inv == 0
    inv_seq = xp.where(appeared, st.step, xp.where(gone, _BIG_SEQ, seq_before))
    seeds = st.seeds.at[p, plant_crop].add(xp.where(do_plant, -1, 0))

    return st._replace(kind=kind, occ=occ, t_day=t_day, t_water=t_water,
        t_cons=t_cons, t_yield=t_yield, t_life=t_life, t_fert=t_fert,
        t_cared=t_cared, t_favail=t_favail, t_bank=t_bank,
        shed=st.shed.at[p].set(shed), seeds=seeds,
        inv=st.inv.at[p, j].set(inv), inv_seq=st.inv_seq.at[p, j].set(inv_seq),
        upos=st.upos.at[p, j].set(newpos))


def apply_units_unrolled(xp, st, day, uop, ua, uq):
    """Static Python-unrolled scalar unit fold."""
    op = _prepare_ops(xp, st, uop, ua)
    for p in range(2):
        for j in range(MU):
            st = _apply_one(xp, st, day, op[p, j], ua[p, j], uq[p, j], p, j)
    return st


def apply_units_loop(xp, st, day, uop, ua, uq):
    """`lax.fori_loop` scalar unit fold; provisional default implementation."""
    op = _prepare_ops(xp, st, uop, ua)
    for p in range(2):
        st = lax.fori_loop(0, MU,
            lambda j, carry: _apply_one(xp, carry, day, op[p, j], ua[p, j], uq[p, j], p, j), st)
    return st


apply_units = apply_units_loop
