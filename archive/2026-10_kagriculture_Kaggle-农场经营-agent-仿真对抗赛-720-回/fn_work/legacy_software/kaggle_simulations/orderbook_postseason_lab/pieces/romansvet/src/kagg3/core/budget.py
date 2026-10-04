"""The buy side [HEURISTIC, PLANNER_V3_1 section 1.3]: marginal purchase
candidates granted greedily by value per coin down the purse.

Ten lists, each up to a shed's worth long, each already ordered so that
value per coin is non-increasing along it -- values fall (the k-th seed's
units sell further down the curve), costs rise (the k-th wheat is quoted
higher). "Best ratio first" across such lists is a threshold: every item
whose ratio is at least tau, for the smallest tau whose total cost fits the
purse. Bisection finds tau; top-ups then spend what the threshold left,
one item per round until nothing fits. Land is not a list -- it is lumpy, and
one quadrant is not a marginal unit of anything -- so the planner compares it
two ways ahead of this greedy. `marginal_gain` below is what prices it: the
same walk, over the ranks the quadrant's tiles would add, so land competes on
the very yardstick every other candidate is measured with.

Shed room is a second budget and is enforced here rather than clipped by the
caller [LAW, 0.10]: wheat, fertilizer and animals all land in the shed and
share one room, so a grant made against it and clipped afterwards would spend
coins on units the shed cannot hold and strand them -- five lists each
wanting the whole room can chase it with five times the units. Both the
threshold and the top-ups therefore carry the room, and `sum(n[SHED_LISTS])
<= room` holds on the way out.

The room needs a second threshold pass, though: one global tau cannot express
"few shed units, many seeds". A binding room drives tau above every shed
list's ratio, and that same tau then also shuts out every non-shed candidate
worth less per coin -- leaving the whole seed grant to the top-ups, which add
at most one item a round and so at most K items in total across all ten
lists. So the shed lists are frozen at the room-constrained threshold and the
non-shed lists are thresholded again on their own tau against the coins the
shed lists did not spend. Both passes are monotone, so both stay exact.

Documented approximation: purchases still compete for labour and tiles
outside this model.

int32 on both backends: `np.cumsum`/`np.sum` widen an int32 input to int64
while their jnp counterparts do not (the hazard projector.py documents), so
every reduction here pins `dtype`.
"""

from __future__ import annotations

from .. import spec
from . import loop
from . import projector as PJ

N_LISTS = 10                      # wheat (feeds), fertilizer, five seed crops, three animals
L_WHEAT, L_FERT, L_SEED0, L_ANIMAL0 = 0, 1, 2, 7
#: One list per animal kind, not one for "the day's animal" [1.3]. A single
#: list forced one kind on the whole day, and the greedy is a threshold over
#: value per coin, so three of them price the mix instead: cows until the
#: marginal cow falls below the marginal sheep, and then sheep. Which is the
#: mixed herd, derived rather than declared -- and it matters because the
#: product curves differ (`T` is 332 for egg but 122 for milk and 105 for
#: wool), so one kind saturates its own curve where two do not.
L_ANIMALS = tuple(range(L_ANIMAL0, L_ANIMAL0 + spec.N_ANIMALS))
#: Lists whose units go into the shed and so compete for one room. Seeds and
#: land are not shed items.
SHED_LISTS = (L_WHEAT, L_FERT) + L_ANIMALS
#: Lists a fresh quadrant's tiles admit more of, and so the ones `marginal_gain`
#: walks when it prices land. Feed wheat and fertilizer are per-task inputs
#: bought for tiles the farm already works, not per-tile purchases.
LAND_LISTS = tuple(range(L_SEED0, L_SEED0 + spec.N_CROPS)) + L_ANIMALS
RATIO_SHIFT = 10                  # value * 1024 // cost, int32-safe for values < COIN_CAP
#: Rounds `marginal_gain` walks. One quadrant is 25 tiles and no caller asks
#: for more, so the loop is fixed at that and `rounds_cap` gates it from there.
MARGIN_ROUNDS = spec.N_TILES // 4
#: The planner's one coin ceiling (`spec.COIN_CAP`), shared with `brain`'s
#: reservation decode, `plan`'s task-value clip and `sell.LIQUIDATE`.
VALUE_CAP = spec.COIN_CAP - 1
_NONE = -1


def _cum_at(xp, cum, k):
    """cum[:, k-1] per row (0 where k == 0)."""
    idx = xp.clip(k - 1, 0, cum.shape[1] - 1)
    return xp.where(k > 0, xp.take_along_axis(cum, idx[:, None], axis=1)[:, 0], 0)


def spend(xp, costs, n):
    """int: coins a grant of `n[l]` units off each list costs.

    The same `cumsum`/`_cum_at` read `grant`'s own `total` does, exposed so a
    caller can ask what the walk left in the purse rather than re-deriving it
    from a second walk. Pinned to int32 on both backends, like every other
    reduction here.
    """
    i32 = xp.int32
    cum = xp.cumsum(xp.maximum(costs.astype(i32), 1), axis=1, dtype=i32)
    return xp.sum(_cum_at(xp, cum, xp.clip(xp.asarray(n).astype(i32), 0, PJ.K)),
                  dtype=i32).astype(i32)


def marginal_gain(xp, values, costs, wants, extra, rounds_cap, purse, lists):
    """int: net coins (value less cost) of the best `rounds_cap` candidates
    taken from ranks `[wants[l], wants[l] + extra[l])` of the lists named in
    `lists`, best ratio first against `purse`.

    Structurally `grant`'s top-up walk with a shifted start and a bounded round
    count, and it shares its tie rules verbatim: `argmax` takes the first
    maximum, so equal ratios fall to the lower list index. It is deliberately
    *not* a second `grant` -- three grants per day is over the throughput gate
    -- so it carries no shed room and no threshold, only the purse.

    `lists` is a static tuple of list indices; `extra` is an int[N_LISTS] cap
    on how far past each want the walk may go; `rounds_cap` bounds the whole
    walk. The result is clipped to +-VALUE_CAP.
    """
    i32 = xp.int32
    values = xp.clip(values.astype(i32), 0, VALUE_CAP)
    costs = xp.maximum(costs.astype(i32), 1)
    wants = xp.clip(wants.astype(i32), 0, PJ.K)
    extra = xp.maximum(xp.asarray(extra).astype(i32), 0)
    rounds_cap = xp.asarray(rounds_cap).astype(i32)
    ratio = xp.where(values > 0, (values << RATIO_SHIFT) // costs, _NONE)

    lid = xp.arange(N_LISTS, dtype=i32)
    live = xp.zeros(N_LISTS, i32)
    for _list in lists:
        live = live + (lid == _list).astype(i32)

    def body(carry):
        n, left, gain, rnd = carry
        nxt = xp.clip(wants + n, 0, PJ.K - 1)
        c_next = xp.take_along_axis(costs, nxt[:, None], axis=1)[:, 0]
        v_next = xp.take_along_axis(values, nxt[:, None], axis=1)[:, 0]
        r_next = xp.take_along_axis(ratio, nxt[:, None], axis=1)[:, 0]
        ok = ((n < extra) & (wants + n < PJ.K) & (r_next >= 0) & (c_next <= left)
              & (live > 0) & (rnd < rounds_cap))
        key = xp.where(ok, r_next, _NONE)
        best = xp.argmax(key)
        can = key[best] >= 0
        hit = (lid == best).astype(i32) * can.astype(i32)
        return (n + hit,
                left - xp.where(can, c_next[best], 0),
                gain + xp.where(can, v_next[best] - c_next[best], 0),
                rnd + 1)

    zeros = xp.zeros(N_LISTS, i32)
    _, _, gain, _ = loop.repeat(xp, MARGIN_ROUNDS, body,
                                (zeros, xp.asarray(purse).astype(i32),
                                 xp.asarray(0, i32), xp.asarray(0, i32)))
    return xp.clip(gain, -VALUE_CAP, VALUE_CAP).astype(i32)


def grant(xp, values, costs, wants, purse, room=None):
    """int[N_LISTS]: how many of each list to buy.

    values, costs: int[N_LISTS, K]; wants: int[N_LISTS]; purse: int scalar.
    `room` is the shed units `SHED_LISTS` may take between them; None means
    unconstrained.

    Precondition, enforced rather than trusted: `wants <= K`. Each list is
    only K items long, so a larger want has nothing behind it -- and the
    top-up loop's `clip(n, 0, K - 1)` would re-read the last item and grant it
    twice. `plan.py` never asks for more than the board's 100 tiles, so the
    clip below never binds there; it is the guard for the next caller.
    """
    i32 = xp.int32
    values = xp.clip(values.astype(i32), 0, VALUE_CAP)
    costs = xp.maximum(costs.astype(i32), 1)
    wants = xp.minimum(wants.astype(i32), PJ.K)
    j = xp.arange(PJ.K, dtype=i32)[None, :]
    live = (j < wants[:, None]) & (values > 0)
    ratio = xp.where(live, (values << RATIO_SHIFT) // costs, _NONE)
    # The walk is at most K = 101 units at the table's dearest quote, so no
    # partial sum passes 1.07e8; ten of them total 1.07e9, which is still
    # inside int32 but no longer with the margin eight lists had -- a twentieth
    # list would not fit.
    cum = xp.cumsum(costs, axis=1, dtype=i32)

    lid = xp.arange(N_LISTS, dtype=i32)
    shed = xp.zeros(N_LISTS, i32)
    for _list in SHED_LISTS:
        shed = shed + (lid == _list).astype(i32)
    # No grant can exceed N_LISTS * K units, so that ceiling is "unconstrained"
    # and the room arithmetic stays one code path on both backends.
    room = xp.asarray(N_LISTS * PJ.K if room is None else room).astype(i32)

    def counts(tau):
        return xp.sum((ratio >= tau).astype(i32), axis=1, dtype=i32)

    def total(n):
        return xp.sum(_cum_at(xp, cum, n), dtype=i32)

    def shed_units(n):
        return xp.sum(n * shed, dtype=i32)          # <= len(SHED_LISTS) * K

    # Smallest tau whose grant fits *both* budgets; 31 halvings cover 2**31.
    # Counts fall as tau rises, so cost and shed units both fall with it and
    # the conjunction is still monotone -- the bisection stays exact.
    def bisect(carry):
        lo, hi = carry
        mid = (lo + hi) // 2
        n = counts(mid)
        fits = (total(n) <= purse) & (shed_units(n) <= room)
        return (xp.where(fits, lo, mid + 1), xp.where(fits, mid, hi))
    _, hi = loop.repeat(xp, 31, bisect, (xp.asarray(0, i32), xp.asarray((1 << 30), i32)))
    n1 = counts(hi)

    # Second threshold, non-shed lists only (see the module docstring). The
    # shed lists are frozen at `n1`; the rest are re-thresholded on their own
    # tau against `purse` less what the shed lists spent. `tau = hi` already
    # fits that budget -- the first pass's whole grant fit the purse, and this
    # one drops its shed half -- so the second tau is no higher and the
    # non-shed counts can only grow. Cost stays inside the purse
    # (`shed_spend + total(n_free) <= purse`) and the room is untouched.
    free = xp.where(shed[:, None] > 0, _NONE, ratio)
    shed_spend = xp.sum(_cum_at(xp, cum, n1 * shed), dtype=i32)

    def counts_free(tau):
        return xp.sum((free >= tau).astype(i32), axis=1, dtype=i32)

    def bisect_free(carry):
        lo, hi_ = carry
        mid = (lo + hi_) // 2
        fits = total(counts_free(mid)) <= purse - shed_spend
        return (xp.where(fits, lo, mid + 1), xp.where(fits, mid, hi_))
    _, hi_free = loop.repeat(xp, 31, bisect_free,
                             (xp.asarray(0, i32), xp.asarray((1 << 30), i32)))
    n = xp.where(shed > 0, n1, counts_free(hi_free))
    left = purse - total(n)

    # Lumpy top-ups: the threshold is all-or-nothing per ratio level, so equal
    # ratios at the boundary can leave coins unspent. Keep granting the
    # best-ratio next item that still fits -- both budgets -- until nothing
    # does. At most one item per round, so K rounds add at most K items *in
    # total* across the ten lists, not K per list: this mops up the ratio
    # boundary the two thresholds left, it is not a substitute for them.
    def topup(carry):
        n, left, room_left = carry
        nxt = xp.clip(n, 0, PJ.K - 1)
        c_next = xp.take_along_axis(costs, nxt[:, None], axis=1)[:, 0]
        r_next = xp.take_along_axis(ratio, nxt[:, None], axis=1)[:, 0]
        ok = ((n < wants) & (r_next >= 0) & (c_next <= left)
              & ((shed == 0) | (room_left > 0)))
        # argmax takes the first maximum, so ties already fall to the lower
        # list; packing the list into the key would overflow int32 (ratio
        # reaches 2**30).
        key = xp.where(ok, r_next, _NONE)
        best = xp.argmax(key)
        can = key[best] >= 0
        hit = (lid == best).astype(i32) * can.astype(i32)
        n = n + hit
        left = left - xp.where(can, c_next[best], 0)
        return n, left, room_left - shed_units(hit)
    n, _, _ = loop.repeat(xp, PJ.K, topup, (n, left, (room - shed_units(n)).astype(i32)))
    return n.astype(i32)
