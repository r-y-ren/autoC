"""End-of-day refresh, transcribed from `_end_of_day` and its helpers.

Randomness
----------
The engine keys a `random.Random((seed * 1_000_003) ^ day)` per day and consumes
it in a fixed order: one `random()` per **empty unlocked tile** for player 0 in
row-major order, then the same for player 1, then `choice(sorted(SHOPS))` on
shop-unlock days. The host draws that generator's raw 32-bit word stream and
hands it over as `words`; this module walks it with the same pointer arithmetic.

`random()` eats two words as `(w0 >> 5) * 2**26 + (w1 >> 6)` over `2**53`. Rather
than rebuild that double on device (float32 would lose the low bits right where
the 0.005 comparison lives), the weed test is done as an exact two-limb integer
compare against a threshold the host precomputes from `weedSpawnChance`.

`choice` over the 8 shops eats one word per attempt (`w >> 28`, rejecting >= 8),
so a short fixed-width scan over attempts reproduces it.
"""

from __future__ import annotations

import numpy as np

from .. import spec

NT = spec.N_TILES
MU = spec.MAX_UNITS
NI = spec.N_ITEMS

# Words consumed per day: 2 per empty tile for each of two players, plus a few
# rejection-sampling attempts for the shop draw.
STREAM_WORDS = 2 * 2 * NT + 16
SHOP_ATTEMPTS = 12
_BIG_SEQ = np.int32(1 << 20)

#: Where `--shop-crn` reads the shop draw from instead of `2 * used`.
#:
#: The engine's day generator is consumed weeds-first, so the word the shop
#: `choice` lands on is a function of how many EMPTY tiles the two seats left
#: that day. Two candidates that differ by one planted tile therefore draw
#: DIFFERENT shops for the rest of the season, and a YARN_STORE (the only wool
#: sink) is worth ~25k to whichever seat is holding wool -- a zero-mean +/-25k
#: lottery bolted onto every ES fitness difference (`scratchpad/coupling`).
#:
#: `2 * 2 * NT` is one past the last word any weed walk can reach (2 words per
#: tile, NT tiles, two seats), and `STREAM_WORDS` keeps 16 spare there, so the
#: draw is a *fresh* word of the same per-(seed, day) stream that no tile count
#: can move. `choice` is uniform over the eight shops whatever word it reads,
#: so the shop distribution -- and hence the expectation of fitness -- is
#: unchanged; only its coupling to our own play is cut.
SHOP_CRN_BASE = 2 * 2 * NT

#: `unlock_shop`'s "this day unlocked nothing" marker in a recorded town row.
#: Re-exported as `es.tape_actions.NO_UNLOCK`, which is what builds the rows.
NO_UNLOCK = -1


def weed_threshold(chance: float = spec.WEED_SPAWN_CHANCE):
    """Two-limb integer form of `random() < chance`, matching CPython exactly.

    `random()` is exactly `A * 2**-53` for the integer A built from two words, so
    `random() < chance` is `A < chance * 2**53`. That product is exact in float64
    (it is only an exponent shift), so the integer threshold is its floor, minus
    one more when it lands exactly on an integer.
    """
    x = chance * float(1 << 53)
    t = int(x) - (1 if x == int(x) else 0)
    return np.int32(t >> 26), np.int32(t & ((1 << 26) - 1))


def host_stream(seed: int, day: int, n: int = STREAM_WORDS) -> np.ndarray:
    """The engine's own generator, drained as raw words."""
    import random
    r = random.Random((seed * 1_000_003) ^ day)
    # uint32 all the way to the device: narrowing to signed int32 would turn the
    # logical shifts below into arithmetic ones for any word with the top bit set.
    return np.array([r.getrandbits(32) for _ in range(n)], dtype=np.uint32)


def refresh_plants(xp, st, day):
    nd = day + 1
    is_pl = st.kind == spec.KIND_PLANT
    c = xp.clip(st.occ, 0, spec.N_CROPS - 1)
    ong = xp.asarray(spec.CROP_ONGOING)[c]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[c]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[c], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[c]

    was_watered = st.t_water == 1
    cons = xp.where(was_watered, 0, st.t_cons + 1)
    died = is_pl & (cons >= 2)

    dsf = nd - st.t_day - first
    fires = is_pl & ~died & (ong == 1) & (dsf >= 0) & (dsf % interval == 0)
    pcount = dsf // interval + 1
    fires = fires & (pcount <= mxy)
    fertilized = was_watered & (st.t_fert >= day)
    new_yield = xp.where(fires, xp.minimum(mxy, st.t_yield + xp.where(fertilized, 2, 1)),
                         st.t_yield)
    new_life = xp.where(fires & (pcount == mxy), (nd + 1) * spec.TURNS_PER_DAY, st.t_life)

    kind = xp.where(died, spec.KIND_WEED, st.kind)
    occ = xp.where(died, -1, st.occ)
    return st._replace(
        kind=kind, occ=occ,
        t_cons=xp.where(is_pl, xp.where(died, 0, cons), st.t_cons),
        t_water=xp.where(is_pl, 0, st.t_water),
        t_yield=xp.where(is_pl, xp.where(died, 0, new_yield), st.t_yield),
        t_life=xp.where(is_pl & ~died, new_life, xp.where(died, -1, st.t_life)),
        t_fert=xp.where(died, -1, st.t_fert),
        t_day=xp.where(died, 0, st.t_day),
    )


def refresh_animals(xp, st, day):
    nd = day + 1
    is_st = (st.kind == spec.KIND_COOP) | (st.kind == spec.KIND_PASTURE)
    has = is_st & (st.occ >= 0)
    a = xp.clip(st.occ, 0, spec.N_ANIMALS - 1)
    first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a]
    interval = xp.maximum(xp.asarray(spec.ANIMAL_INTERVAL)[a], 1)
    held = xp.asarray(spec.ANIMAL_MAX_HELD)[a]

    fed = st.t_water == 1
    cons = xp.where(fed, 0, st.t_cons + 1)
    escaped = has & (cons >= 2)
    alive = has & ~escaped

    dsf = nd - st.t_day - first
    fires = alive & (dsf >= 0) & (dsf % interval == 0)
    # The banked CARE bonus is only paid out on a day the animal was fed, and it
    # is cleared either way once a production fires.
    bonus = xp.where(fed, st.t_bank, 0)
    new_yield = xp.where(fires, xp.minimum(held, st.t_yield + 1 + bonus), st.t_yield)
    bank = xp.where(fires, 0, st.t_bank)
    bank = xp.where(alive & (st.t_cared == 1) & fed, bank + 1, bank)

    return st._replace(
        occ=xp.where(escaped, -1, st.occ),
        t_cons=xp.where(has, xp.where(escaped, 0, cons), st.t_cons),
        t_yield=xp.where(has, xp.where(escaped, 0, new_yield), st.t_yield),
        t_bank=xp.where(has, xp.where(escaped, 0, bank), st.t_bank),
        t_favail=xp.where(alive, 1, xp.where(escaped, 0, st.t_favail)),
        t_water=xp.where(has, 0, st.t_water),
        t_cared=xp.where(has, 0, st.t_cared),
        t_day=xp.where(escaped, 0, st.t_day),
    )


def spawn_weeds(xp, st, words, hi_t, lo_t):
    """One draw per empty unlocked tile, player 0's tiles before player 1's."""
    i32 = xp.int32
    empty = (st.kind == spec.KIND_EMPTY).astype(i32)              # [2, NT]
    rank = xp.cumsum(empty, axis=1) - empty                        # draw index within player
    n0 = xp.sum(empty[0])
    offset = xp.stack([xp.zeros((), i32), n0])[:, None]
    di = rank + offset                                             # [2, NT]
    hi = (words[2 * di] >> 5).astype(i32)          # words are uint32: logical shift
    lo = (words[2 * di + 1] >> 6).astype(i32)
    hit = (hi < hi_t) | ((hi == hi_t) & (lo <= lo_t))
    grew = (empty == 1) & hit
    st = st._replace(kind=xp.where(grew, spec.KIND_WEED, st.kind),
                     t_day=xp.where(grew, 0, st.t_day),
                     t_water=xp.where(grew, 0, st.t_water),
                     t_cons=xp.where(grew, 0, st.t_cons),
                     t_yield=xp.where(grew, 0, st.t_yield),
                     t_life=xp.where(grew, -1, st.t_life),
                     t_fert=xp.where(grew, -1, st.t_fert))
    return st, n0 + xp.sum(empty[1])


def unlock_shop(xp, st, words, base, day, town=None):
    """`rng.choice(sorted(SHOPS))` -- one word per attempt, rejecting >= 8.

    `town` is a **recorded** schedule (`es.tape_actions.town_array`, int32 [ND]
    indexed by the day the shop becomes visible, `NO_UNLOCK` = -1 elsewhere), or
    `None`. `None` is the static "this program has no recorded town" case and
    emits exactly the code it always did.

    With one, this board's draw is replaced by the recording: `town[day + 1]`
    both names the shop and says whether the day unlocks at all. That is the
    point of the whole flag -- a recorded seat plants for the town that unlocked
    in ITS game, and replaying it under a freshly drawn town farms for the wrong
    shops. The replacement is per BOARD, not per seat: the engine's town is
    shared, and so is `st.shops`.

    A row that is all -1 (a member of a `stack`ed batch that carries no town of
    its own) falls straight back to the drawn shop, which is what makes a mixed
    batch legal.
    """
    i32 = xp.int32
    nd = day + 1
    due = (nd % spec.SHOP_UNLOCK_INTERVAL == 0) & (st.nshops < spec.MAX_SHOP_INSTANCES)
    k = xp.arange(SHOP_ATTEMPTS, dtype=i32)
    v = (words[base + k] >> 28).astype(i32)
    ok = v < spec.N_SHOPS
    pick = v[xp.argmax(ok)]
    if town is not None:
        rec = town[xp.clip(nd, 0, town.shape[0] - 1)].astype(i32)
        on = rec >= 0                       # this day unlocks in the recording
        has = xp.any(town >= 0)             # this board carries a town at all
        pick = xp.where(on, xp.clip(rec, 0, spec.N_SHOPS - 1), pick)
        # Where the board has a town, the recording is authoritative in BOTH
        # directions: a day it did not unlock on must not unlock here either.
        due = xp.where(has, on, due)
    add = (xp.arange(spec.N_SHOPS, dtype=i32) == pick).astype(i32) * due.astype(i32)
    return st._replace(shops=st.shops + add, nshops=st.nshops + due.astype(i32))


def drop_inventories(xp, st):
    """Dump every unit inventory into the shed, honouring shedCapacity.

    The engine walks `inventories` in unit order and, inside each unit, walks the
    inventory dict in **insertion order** -- so which items survive an overflow
    depends on the order that unit first acquired them. `inv_seq` records that
    first-acquisition turn (a unit performs at most one acquiring op per turn, so
    the turn number is a sufficient key), and sorting on (unit, seq) reproduces
    the engine's walk exactly.
    """
    i32 = xp.int32
    shed = st.shed
    inv = st.inv
    seq = st.inv_seq
    unit_ix = xp.arange(MU, dtype=i32)[:, None] * xp.ones((1, NI), i32)

    out_shed = []
    for p in range(2):
        # Per seat. Adding `seq[2, MU, NI]` to the [MU, NI] unit index used to
        # broadcast both seats' keys into one 264-entry array, whose argsort
        # then indexed this seat's 132 counts -- JAX clamps the excess indices
        # silently, so seat 1 was walked in seat 0's order.
        key = unit_ix * (_BIG_SEQ * 2) + seq[p]                     # [MU, NI]
        flat_n = inv[p].reshape(-1)
        flat_k = key.reshape(-1)
        order = xp.argsort(flat_k)
        n_sorted = flat_n[order]
        item_of = (xp.arange(MU * NI, dtype=i32) % NI)[order]
        room0 = xp.maximum(spec.SHED_CAPACITY - xp.sum(shed[p]), 0)
        cum = xp.cumsum(n_sorted)
        take = xp.minimum(room0, cum) - xp.minimum(room0, cum - n_sorted)
        add = xp.zeros(NI, i32)
        oh = (xp.arange(NI, dtype=i32)[None, :] == item_of[:, None]).astype(i32)
        add = xp.sum(oh * take[:, None], axis=0)
        out_shed.append(shed[p] + add)

    return st._replace(shed=xp.stack(out_shed),
                       inv=xp.zeros_like(st.inv),
                       inv_seq=xp.full_like(st.inv_seq, _BIG_SEQ))


def end_of_day(xp, st, day, words, hi_t, lo_t, shop_crn=False, town=None):
    """`shop_crn` is `es.train.Config.shop_crn` / `--shop-crn`: a Python bool
    read at trace time, off by default, so an unflagged run emits the program
    it always did and reproduces the engine word for word. On, the shop draw
    moves to `SHOP_CRN_BASE` -- a common random number across candidates that
    plant differently. Weeds keep their per-tile draws either way.

    `town` is the tape's recorded schedule (`--with-town`), or `None`; see
    `unlock_shop`. It overrides the draw entirely, so `shop_crn` becomes moot
    for a board that carries one -- the coupling `--shop-crn` exists to cut is
    gone by construction once the shops no longer depend on any draw.
    """
    st = refresh_plants(xp, st, day)
    st = refresh_animals(xp, st, day)
    st, used = spawn_weeds(xp, st, words, hi_t, lo_t)
    st = drop_inventories(xp, st)
    base = SHOP_CRN_BASE if shop_crn else 2 * used
    st = unlock_shop(xp, st, words, base, day, town=town)
    return st._replace(
        upos=xp.full_like(st.upos, spec.DEFAULT_SPAWN_TILE),
        nhands=xp.zeros_like(st.nhands),
        hires_today=xp.zeros_like(st.hires_today),
    )
