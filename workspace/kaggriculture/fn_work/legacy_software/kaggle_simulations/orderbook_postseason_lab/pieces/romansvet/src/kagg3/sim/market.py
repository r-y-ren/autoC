"""Market resolution, transcribed from `_process_market` / `_commit_unit`.

The engine walks orders one unit at a time, quoting both players against the
same pre-commit inventory and then committing in player order. That loop is
unbounded in the source but bounded in fact: SELL is capped by `shed[item]`,
BUY_PRODUCT and BUY_ANIMAL by shed room, and the shed holds at most
`SHED_CAPACITY`. So no market-inventory order ever moves more than 100 units,
and the whole walk can be evaluated as a fixed-length vector of quotes plus a
cumulative sum instead of a data-dependent loop. BUY_SEED is the one unbounded
order, and it has a fixed price, so it needs no walk at all.

Coupling
--------
Two orders interact only when both touch market inventory (SELL / BUY_PRODUCT)
on the same item. Then the pair advances in lockstep and the shared inventory
moves two units per round instead of one. The resolution splits into three
segments:

  1. rounds `[0, m)` where `m = min(k0, k1)` -- both players commit,
  2. round `m` -- the player that can still afford it commits alone, at the
     quote both players saw (the engine commits in player order, so a failure by
     one does not roll back the other),
  3. rounds `> m` -- the survivor continues solo against a fresh quote walk.

`k_p` is each player's affordable round count under coupled pricing, which is
exactly right through round `m` because the inventory path up to there is
determined by both players being active.

The one unsupported pair is SELL against BUY_PRODUCT on the same item in the
same slot. The planner emits an identical slot layout for both seats, so it
cannot arise in self-play; `assert_no_cross` flags it rather than silently
computing the wrong answer.
"""

from __future__ import annotations

import numpy as np

from .. import spec
from ..core import ops as O
from ..es import kagg2_flow as K2
from ..es import kaggle_flow as KG
from .state import MAX_UNITS_PER_ORDER

K = MAX_UNITS_PER_ORDER + 1

#: The busiest single day over every table `apply_flow` can be asked to replay.
#: The two measured means are here at import; `register_flow_table` raises it
#: when a tape rung's table is busier (`es.tape_flow`).
MAX_FLOW_DAY_UNITS = max(K2.MAX_DAY_UNITS, KG.MAX_DAY_UNITS)

#: Length of `apply_flow`'s quote walk. The exogenous flow is a whole *day* of
#: one seat's orders folded into a single walk, so it is not bounded by
#: `MAX_UNITS_PER_ORDER` the way one order slot is: kagg2's busiest day is 107
#: wheat and the Kaggle field's is 110. Sized off the max over **every**
#: registered table, since one program serves whichever the control word
#: selects. Twice that leaves room for the trainer's flow scale (capped at 2.0
#: in `scripts/train.py` for exactly this reason) and the walk is clamped to it,
#: so a scale past the cap truncates rather than reading out of bounds.
FLOW_K = 2 * MAX_FLOW_DAY_UNITS + 1

# quote-walk modes
M_SELL_SOLO = 0
M_SELL_PAIR = 1
M_BUY_SOLO = 2
M_BUY_PAIR = 3


def _quotes(xp, tables, item, inv, mode):
    """Price quoted at each successive round of a walk, length K."""
    j = xp.arange(K, dtype=xp.int32)
    off = xp.where(mode == M_SELL_SOLO, j,
          xp.where(mode == M_SELL_PAIR, 2 * j,
          xp.where(mode == M_BUY_SOLO, -1 - j, -1 - 2 * j)))
    idx = xp.clip(inv + off - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    return tables.price[item, idx]


def _take(xp, cum, k):
    """cum[k-1], i.e. the total over the first k rounds (0 when k == 0)."""
    return xp.where(k > 0, cum[xp.clip(k - 1, 0, K - 1)], 0)


def sell_walk(xp, tables, item, inv, ncap, mode):
    """Returns (k, revenue, inventory_advance_rounds)."""
    q = _quotes(xp, tables, item, inv, mode)
    cum = xp.cumsum(q)
    k = xp.clip(ncap, 0, K - 1)
    revenue = _take(xp, cum, k)
    # A unit sold at the $1 floor is still paid for but is not added to supply,
    # so the inventory only advances on rounds priced above the floor.
    j = xp.arange(K, dtype=xp.int32)
    adv = xp.sum(((q > spec.PRICE_FLOOR) & (j < k)).astype(xp.int32))
    return k, revenue, adv


def buy_walk(xp, tables, item, inv, ncap, money, mode):
    """Returns (k, cost). Stops at the first unit the player cannot afford."""
    q = _quotes(xp, tables, item, inv, mode)
    cum = xp.cumsum(q)
    afford = xp.sum((cum <= money).astype(xp.int32))
    k = xp.clip(xp.minimum(ncap, afford), 0, K - 1)
    return k, _take(xp, cum, k)


def _hire(xp, st, p):
    """`_do_hire`: fib pricing, spawn on the least-occupied shed-access tile.

    `nhands < MAX_HANDS` is *not* an engine rule -- `_do_hire` caps nothing and
    appends hands until the money runs out. It is this state's array bound:
    `upos`, `inv` and `inv_seq` are `MAX_UNITS` wide, so a hand past the
    ceiling has nowhere to live. The planner never asks for more (`spec`
    documents where 16 comes from and `ops._check_schedule` keeps the crew
    inside the two hire rows' market slots), so the clamp never fires on a
    plan this repo emits; it is here so a hand-built order row is dropped
    rather than silently scattered out of bounds.
    """
    i32 = xp.int32
    n_done = xp.clip(st.hires_today[p], 0, spec.MAX_HANDS)
    cost = xp.asarray(spec.HIRE_COST)[n_done]
    ok = (st.money[p] >= cost) & (st.nhands[p] < spec.MAX_HANDS)

    access = xp.asarray(spec.SHED_ACCESS_TILE)                       # NWSE order
    live = xp.arange(spec.MAX_UNITS, dtype=i32) <= st.nhands[p]
    counts = xp.sum(((st.upos[p][None, :] == access[:, None]) & live[None, :]).astype(i32),
                    axis=1)
    # argmin returns the first minimum, and the array is already in NWSE order,
    # which is exactly the engine's tie-break.
    slot = xp.argmin(counts)
    idx = st.nhands[p] + 1

    return st._replace(
        money=st.money.at[p].add(xp.where(ok, -cost, 0)),
        hires_today=st.hires_today.at[p].add(ok.astype(i32)),
        nhands=st.nhands.at[p].add(ok.astype(i32)),
        upos=st.upos.at[p, xp.clip(idx, 0, spec.MAX_UNITS - 1)].set(
            xp.where(ok, access[slot], st.upos[p, xp.clip(idx, 0, spec.MAX_UNITS - 1)])),
    )


def _buy_land(xp, st, p):
    """`_do_buy_land`: NE, SW, SE at 1000 / 2000 / 4000."""
    i32 = xp.int32
    n_extra = xp.clip(st.nquad[p] - 1, 0, 2)
    cost = xp.asarray(spec.LAND_PRICES)[n_extra]
    ok = (st.nquad[p] < 4) & (st.money[p] >= cost)
    quad = xp.asarray(spec.LAND_ORDER)[n_extra]
    unlock = ok & (xp.asarray(spec.TILE_QUAD) == quad) & (st.kind[p] == spec.KIND_LOCKED)
    return st._replace(
        money=st.money.at[p].add(xp.where(ok, -cost, 0)),
        nquad=st.nquad.at[p].add(ok.astype(i32)),
        kind=st.kind.at[p].set(xp.where(unlock, spec.KIND_EMPTY, st.kind[p])),
    )


def apply_land_row(xp, st, mop):
    """Resolve a BUY_LAND riding a SELL turn's spare slot.

    The planner puts it in the row's *last* slot, so after compaction it is
    still the last live order of that seat's row and every one of that seat's
    sells has already resolved when it commits. Applying it once after the
    whole slot scan is therefore exactly in-order, not an approximation:
    BUY_LAND is atomic -- `_do_buy_land` runs at the head of its slot round,
    in player order, outside the SELL/BUY lockstep -- and it reads and writes
    only its own seat's money, quadrant count and tiles, none of which the
    other seat's sells in this turn can move.

    That is what lets the cheap sell-only path carry a land order for the cost
    of one conditional a turn instead of the whole `process_slot` body ten
    times.
    """
    want = xp.any(mop == O.MO_BUY_LAND, axis=-1)                # [2]
    for p in range(2):
        st = _cond(xp, want[p], lambda s, p=p: _buy_land(xp, s, p), st)
    return st


#: A `flow` control word: `(seat, scale_milli, shift[, table])`, int32 [3] or
#: [4], one per episode. `seat < 0` switches the whole path off, which is how
#: every episode that is not playing a flow rung passes through it. Packed into
#: one array rather than separate arguments so it rides `make_evaluator`'s vmap
#: and `shard_batch` as a single batched leaf.
#:
#: The optional fourth column selects **which** measured table is replayed --
#: `FLOW_T_KAGG2` for `es.kagg2_flow`, `FLOW_T_KAGGLE` for `es.kaggle_flow`.
#: It is optional, and its absence is not a default but a different program:
#: a 3-wide word takes the exact expression the 3-wide word always took, so a
#: run with only `--kagg2-flow` is byte-identical to the run that came before
#: the second table existed. `es.train.flow_control` emits 3 columns unless a
#: table is asked for.
FLOW_SEAT, FLOW_SCALE, FLOW_SHIFT, FLOW_TABLE = 0, 1, 2, 3
FLOW_OFF = (-1, 1000, 0)

#: Table ids for `FLOW_TABLE`, in the order `_FLOW_SELL` / `_FLOW_BUY` stack
#: them. `FLOW_T_KAGG2` is 0 so that a 4-wide word with the column left at zero
#: replays the same table a 3-wide word does.
FLOW_T_KAGG2, FLOW_T_KAGGLE = 0, 1

#: The measured tables, stacked on a leading table axis for the gather a 4-wide
#: control word does. The two campaign-wide means are here at import;
#: `register_flow_table` appends a run's tape rungs before the evaluator is
#: traced, and they are constants folded into the traced program from then on.
_FLOW_SELL = np.stack([K2.KAGG2_FLOW, KG.KAGGLE_FLOW]).astype(np.int32)
_FLOW_BUY = np.stack([K2.KAGG2_BUY, KG.KAGGLE_BUY]).astype(np.int32)

#: The `grow` half of each table -- what the measured seat put into its shed
#: that day by any route other than the market, net of what it took back out
#: (`es.tape_flow`'s sign convention). Read **only** under
#: `--tape-flow-backed`, which is the only path that asks what the flow seat
#: can actually sell. The two campaign-wide means were measured before `grow`
#: existed and carry a zero row, which under the clamp is the old behaviour
#: (a seat that grows nothing sells nothing) -- so `--tape-flow-backed` is for
#: tape rungs, and `es.train` refuses the flag without a table that has one.
_FLOW_GROW = np.zeros_like(_FLOW_SELL)

#: How many tables were in the stack at import, i.e. before any registration:
#: the two campaign-wide means. A table id at or past this is a run's own tape.
N_MEASURED_TABLES = int(_FLOW_SELL.shape[0])


def register_flow_table(sell, buy, grow=None):
    """Append a measured day table to the stack. -> its `FLOW_TABLE` id.

    `es.kagg2_flow` and `es.kaggle_flow` are campaign constants and live in the
    stack from import. A tape rung's table is a *run's* input -- one replay
    seat, named on the command line (`--tape-rung`) -- so it is registered
    here, by `es.train.Trainer.__init__`, before anything is traced. From the
    program's point of view the two are the same thing: a constant on the
    leading axis of the gather a 4-wide control word does.

    Registration is idempotent by **content**: registering a table equal to one
    already in the stack returns that one's id rather than growing it. Two
    trainers in one process (the tests, and `--resume` inside a sweep) would
    otherwise stack a fresh copy per construction and re-trace the evaluator
    against a bigger constant every time, for no change in behaviour.

    `FLOW_K` -- the length of the quote walk -- is raised if the new table's
    busiest day needs more than the current one covers. Raising it changes the
    walk's *length*, never its result: the walk is clamped at `k` and cumsums a
    longer prefix, so a table that already fitted replays identically. A run
    with no tape rung registers nothing and therefore compiles exactly the
    program it compiled before this function existed.

    `grow` (`es.tape_flow`'s signed production row, or `None` for a table cut
    before it existed) rides the same stack and is read only under
    `backed=True`. It counts towards the content match: two tapes with the same
    market footprint and different production are different opponents under the
    clamp, so they may not share a slot.
    """
    global _FLOW_SELL, _FLOW_BUY, _FLOW_GROW, FLOW_K, MAX_FLOW_DAY_UNITS
    want = (int(spec.N_DAYS), int(spec.N_PRODUCTS))
    sell = np.asarray(sell, np.int32)
    buy = np.asarray(buy, np.int32)
    grow = (np.zeros(want, np.int32) if grow is None
            else np.asarray(grow, np.int32))
    if sell.shape != want or buy.shape != want or grow.shape != want:
        raise ValueError(f"register_flow_table: tables are {sell.shape} / "
                         f"{buy.shape} / {grow.shape}, expected {want}.")
    if (sell < 0).any() or (buy < 0).any():
        raise ValueError("register_flow_table: a negative unit count.")
    for i in range(int(_FLOW_SELL.shape[0])):
        if ((_FLOW_SELL[i] == sell).all() and (_FLOW_BUY[i] == buy).all()
                and (_FLOW_GROW[i] == grow).all()):
            return i
    _FLOW_SELL = np.concatenate([_FLOW_SELL, sell[None]]).astype(np.int32)
    _FLOW_BUY = np.concatenate([_FLOW_BUY, buy[None]]).astype(np.int32)
    _FLOW_GROW = np.concatenate([_FLOW_GROW, grow[None]]).astype(np.int32)
    busiest = int(max(sell.max(initial=0), buy.max(initial=0)))
    if busiest > MAX_FLOW_DAY_UNITS:
        MAX_FLOW_DAY_UNITS = busiest
        FLOW_K = 2 * MAX_FLOW_DAY_UNITS + 1
    return int(_FLOW_SELL.shape[0]) - 1


def registered_flow_tables():
    """How many tables `FLOW_TABLE` can select right now. -> int."""
    return int(_FLOW_SELL.shape[0])


def flow_rows(xp, day, flow, grow=False):
    """The day's scaled (sell, buy) unit rows for a control word. -> two [9].

    Split out of `apply_flow` so `rollout.run_day` can read the day's table
    once and hand the same two rows to every market turn under
    `--tape-flow-spread`, instead of gathering out of the constant table inside
    the turn scan. `apply_flow` with `rows=None` calls it and is the expression
    it always was.

    `grow` (a Python bool, so the choice is made at trace time) appends the
    day's **production** row and returns three. It is `--tape-flow-backed`'s
    input and nothing else reads it, so with the switch off this returns the
    pair it always returned and gathers exactly the two tables it always did.
    """
    src = day - flow[FLOW_SHIFT]
    live = (flow[FLOW_SEAT] >= 0) & (src >= 0) & (src < spec.N_DAYS)
    d = xp.clip(src, 0, spec.N_DAYS - 1)
    scale = xp.where(live, flow[FLOW_SCALE], 0)
    # Which measured table. A 3-wide control word has no table column and reads
    # kagg2's directly -- the same expression, and so the same program, as
    # before `kaggle_flow` existed. The width is static under `vmap`/`jit`, so
    # this branch is taken at trace time and costs nothing at runtime.
    if int(flow.shape[-1]) > FLOW_TABLE:
        tbl = flow[FLOW_TABLE]
        sell_row = xp.asarray(_FLOW_SELL)[tbl, d]
        buy_row = xp.asarray(_FLOW_BUY)[tbl, d]
        grow_row = xp.asarray(_FLOW_GROW)[tbl, d] if grow else None
    else:
        sell_row = xp.asarray(K2.KAGG2_FLOW)[d]
        buy_row = xp.asarray(K2.KAGG2_BUY)[d]
        # A 3-wide word is kagg2's table, and kagg2's `grow` row is the zero
        # row: the mean was measured before `grow` existed.
        grow_row = xp.zeros(spec.N_PRODUCTS, xp.int32) if grow else None
    # Round half up in int32: no float anywhere on this path.
    out = ((sell_row * scale + 500) // 1000, (buy_row * scale + 500) // 1000)
    if not grow:
        return out
    # `grow` is signed, so `// 1000` floors rather than truncates; the +500 is
    # still the half-up bias the other two rows take and the whole family
    # scales together -- production has to move with the sales it backs, or the
    # clamp binds on a scale the measurement never had.
    return out + ((grow_row * scale + 500) // 1000,)


def _share_of_day(xp, row, part, nparts):
    """`row` split over `nparts` market turns, remainder on the last. -> [9].

    `row // nparts` on every turn and everything left over on the last one, so
    the day's total is the table's row to the unit whatever `nparts` is. `part`
    is traced (the turn scan index reduced to a market-turn ordinal), `nparts`
    static; the whole thing is elementwise on a [9] vector, so no lane is built
    out of its own chain.
    """
    base = row // nparts
    return base + xp.where(part == nparts - 1, row - base * nparts, 0)


def apply_flow(xp, tables, st, day, flow, backed=False, rows=None,
               part=None, nparts=1):
    """Replay a measured market day for one seat. -> State.

    `flow` is the control word above: which seat, how hard, how far shifted,
    and -- on a 4-wide word -- which measured table (`es.kagg2_flow`'s or
    `es.kaggle_flow`'s). `scale_milli` scales every product's units by
    thousandths and `shift` slides the whole calendar, so the rung is a
    *family* of opponents shaped like the measurement rather than one replayed
    tape; days that slide off either end of the season contribute nothing.

    Ordering
    --------
    Called once a day from `rollout.run_day`, after the day-boundary quote has
    been handed to both planners and before the turn scan opens. That is the
    same point the engine's first market round sees: unit actions on hour 0 run
    before the market but never touch `market["inventory"]`, so the inventory
    this walks is exactly the pre-commit inventory `_process_market` would quote
    the day's first slot against. The flow therefore lands in front of both
    seats' own orders -- the conservative reading of a day-resolution table, and
    the one that reproduces what the real quote series shows: the day-boundary
    price is the undepressed reference and kagg2's bulk is already in the book
    by the time the late sell turns come round.

    Within the day, sells resolve before buys. Only wheat has both, and it is
    the seat's own harvest reaching the market before it restocks feed.

    Fidelity flags (both off by default; off, every expression below is the one
    it always was and the device program is unchanged)
    ------------------------------------------------------------------------
    * `backed` -- `--tape-flow-backed`. Clamp the sell count to the seat's shed
      *before* the revenue and the inventory advance are taken, not only on the
      drain. Off, an exogenous table is paid for -- and floods the market with
      -- goods the seat never grew; the engine has no such seat (a SELL there is
      capped by `shed[item]`), which is worth ~14k of phantom coins a season on
      a clone tape that sells high-base products a wheat board cannot hold.

      The clamp alone was **measured and not usable** (2026-09-02): it is only
      the engine's rule if the seat's board grows what the table sells, and a
      flow rung's board does not -- it is `es.train.TAPE_PLANNER`, a wheat
      clone, whose shed never holds the strawberry / milk / wool / fertilizer
      the tapes trade. Clamping against that shed did not shrink the opponent,
      it deleted it: on flow57's ladder with `backed` (and `spread`) on, the
      tape seat banked ~8k against the real 101.8k and our seat 166k against
      103.5k. `scratchpad/tapefix/results.md` has those numbers.

      **The missing half is `grow`** (2026-09-05). A tape rung's table now
      carries the production its market footprint implies -- what entered the
      recorded seat's shed by any route other than the market, net of what left
      it the same way (`es.tape_flow`'s sign convention, measured by
      `scripts/make_tape_rung.py` off the replay's own shed observations).
      Under `backed` that row is credited to the flow seat's shed *before* the
      day's sells are clamped, so the seat sells what it actually produced and
      is paid at the **sim's** prices -- which carry our seat's pressure on the
      book, which is the whole reason to replay a tape in the sim rather than
      read its recorded revenue. The credit takes the same shed cap the buy
      path takes (`spec.SHED_CAPACITY` over the seat's whole shed, claimed in
      `spec.PRODUCTS` order), and a negative day drains, clamped at what the
      seat holds.

      The credit itself is uncapped and `spec.SHED_CAPACITY` is applied at
      the *end* of the walk, after the day's sells: capping the credit pinned
      the seat's shed at 100 from day 5 (the rung's masked wheat-clone board
      squats in the same shared shed) and threw away 42% of the production and
      33% of the table's sell units, which is where our seat's 20-30% price
      inflation over the engine came from.

      Under `--tape-flow-spread` the day's `grow` is split over the day's
      market turns by the same `_share_of_day` the sell and buy rows take --
      **proportionally, not all at the first slice** -- so the day's total is
      the table's row to the unit whatever `len(MARKET_TURNS)` is, and the
      identity `shed[d+1] = shed[d] + grow[d] - sell[d] + buy[d]` the
      measurement is defined by survives the split.

      A table with no `grow` row (a tape cut before 2026-09-05, or either
      campaign-wide mean) carries the zero row, which under the clamp is the
      old, useless behaviour; `es.train.Trainer` refuses `--tape-flow-backed`
      unless every tape rung on the ladder has one.
    * `rows` / `part` / `nparts` -- `--tape-flow-spread`. `rows` is a
      precomputed `flow_rows` pair, so the day's table is gathered once;
      `part`/`nparts` apply only that market turn's `_share_of_day` slice.
      `rollout.run_day` then calls this once per market turn instead of once a
      day, and the tape trades at the same hours we do rather than emptying its
      whole day into the book before our first order.

    What it moves
    -------------
    * `mkt_inv` -- the whole point. Sells advance it once per unit priced above
      the floor (the engine pays for a floor unit but does not add it to
      supply); buys retire one unit per unit, floor or not, exactly as `_solo`.
    * the flow seat's `money`, by what the walk realises. No affordability
      check: the table is exogenous, and the seat's coins are bookkeeping for
      the win bit, not a budget the flow has to fit inside.
    * the flow seat's `shed`, drained by what the table sold (clamped at what
      it actually holds) and filled by what the table bought (clamped by shed
      room). `rollout.run_day` masks this seat's own SELL / BUY_PRODUCT orders,
      so without the drain its shed would clog inside a week and its harvests
      would stall -- the flow is its market presence, and this is the stock that
      presence consumes. Under `backed` it is also *credited*, first, with the
      table's `grow` row: the stock that presence is made of.

    Everything is a `where` on a traced control word, so this is `vmap`-safe
    with a per-episode flag and adds no Python-level branch -- and, unlike most
    of this module, it stays off `.at[]` so it runs under plain numpy as well as
    `jax.numpy`, which is what lets the two be compared unit for unit.
    """
    i32 = xp.int32
    seat = flow[FLOW_SEAT]
    sel = xp.arange(2, dtype=i32) == seat                      # [2] bool
    if rows is None:
        rows = flow_rows(xp, day, flow, grow=backed)
    n_sell, n_buy = rows[0], rows[1]
    # `backed` is a Python bool, so the production row is either there at trace
    # time or the whole credit below is not emitted at all. A caller that
    # precomputed `rows` has to have asked `flow_rows` for it; silently reading
    # a missing row as zero production is the old, opponent-deleting clamp.
    if backed and len(rows) < 3:
        raise ValueError("apply_flow(backed=True) needs the production row: "
                         "call flow_rows(..., grow=True).")
    n_grow = rows[2] if backed else None
    if part is not None:
        n_sell = _share_of_day(xp, n_sell, part, nparts)
        n_buy = _share_of_day(xp, n_buy, part, nparts)
        if backed:
            n_grow = _share_of_day(xp, n_grow, part, nparts)

    j = xp.arange(FLOW_K, dtype=i32)
    prod = xp.arange(spec.N_PRODUCTS, dtype=i32)

    def walk(inv, off):
        idx = xp.clip(inv[:, None] + off - spec.PRICE_TABLE_LO,
                      0, spec.PRICE_TABLE_N - 1)
        q = tables.price[prod[:, None], idx]                   # [9, FLOW_K]
        return q, xp.cumsum(q, axis=1)

    def total(cum, k):
        return xp.where(k > 0, cum[prod, xp.clip(k - 1, 0, FLOW_K - 1)], 0)

    def shed_delta(row):
        """A per-product row -> a [2, N_ITEMS] shed delta on the flow seat."""
        wide = xp.concatenate(
            [row, xp.zeros((spec.N_ITEMS - spec.N_PRODUCTS,), i32)])
        return xp.where(sel[:, None], wide[None, :], 0)

    def seat_shed():
        """The flow seat's product stock. -> [N_PRODUCTS]."""
        return xp.sum(xp.where(sel[:, None], st.shed[:, :spec.N_PRODUCTS], 0),
                      axis=0)

    # ------------------------------------------------------------------- grow
    if backed:
        # [`--tape-flow-backed`] What the recorded seat produced this day (or
        # this slice of it), into the shed the sells below are clamped against.
        # Drain first -- a negative day fed more wheat to the animals than it
        # harvested -- then credit.
        #
        # The credit is **not** capped by shed room, and the cap is taken at
        # the end of the walk instead (`spill`, below). Measured 2026-09-05 on
        # tape_105441481 with the cap on the credit: the flow seat's shed is
        # pinned at `SHED_CAPACITY` from day 5 of the season, because the
        # rung's own board is a wheat clone whose SELL orders `mask_flow_seat`
        # blanks -- its harvest can only leave through the tape's wheat row and
        # otherwise squats in the shared 100-unit shed. 42% of the day's
        # production was refused and 33% of the table's sell units never
        # reached the book, so the sim's supply was short and our seat's prices
        # inflated 20-30% over the engine's. The engine has no such throttle:
        # there a day's harvest sits in the units' hands and is DROPped as the
        # day goes, and what the seat sells that day never has to fit in the
        # shed beside yesterday's carry.
        back = xp.minimum(xp.maximum(-n_grow, 0), seat_shed())
        st = st._replace(shed=st.shed + shed_delta(-back))
        st = st._replace(shed=st.shed + shed_delta(xp.maximum(n_grow, 0)))

    # ------------------------------------------------------------------ sells
    k = xp.clip(n_sell, 0, FLOW_K - 1)
    if backed:
        # [`--tape-flow-backed`] The seat may only sell what its shed holds, so
        # the clamp has to happen *before* the revenue and the inventory
        # advance, not just on the drain. Off (the default) `k` is the table's
        # own count and every expression below is the one it always was.
        k = xp.minimum(
            k, xp.sum(xp.where(sel[:, None], st.shed[:, :spec.N_PRODUCTS], 0),
                      axis=0))
    q, cum = walk(st.mkt_inv, j[None, :])
    rev = total(cum, k)
    adv = xp.sum(((q > spec.PRICE_FLOOR) & (j[None, :] < k[:, None])).astype(i32),
                 axis=1)
    have = xp.sum(xp.where(sel[:, None], st.shed[:, :spec.N_PRODUCTS], 0), axis=0)
    drain = xp.minimum(k, have)
    st = st._replace(
        mkt_inv=st.mkt_inv + adv,
        money=st.money + xp.where(sel, xp.sum(rev), 0),
        shed=st.shed + shed_delta(-drain),
    )

    # ------------------------------------------------------------------- buys
    kb = xp.clip(n_buy, 0, FLOW_K - 1)
    # The buy walk needs the cumulative cost only: a BUY retires one unit of
    # inventory per unit bought whatever it cost, floor or not (`_solo`).
    _, cumb = walk(st.mkt_inv, -1 - j[None, :])
    cost = total(cumb, kb)
    # Shed room is shared, so the products claim it in PRODUCTS order the way a
    # slot walk would; only wheat ever asks for any.
    room = xp.maximum(
        spec.SHED_CAPACITY - xp.sum(xp.where(sel, xp.sum(st.shed, axis=1), 0)), 0)
    before = xp.cumsum(kb) - kb
    take = xp.minimum(kb, xp.maximum(room - before, 0))
    st = st._replace(
        mkt_inv=st.mkt_inv - kb,
        money=st.money - xp.where(sel, xp.sum(cost), 0),
        shed=st.shed + shed_delta(take),
    )
    if not backed:
        return st

    # ------------------------------------------------------------------ spill
    # [`--tape-flow-backed`] The shed cap, taken *after* the day's sells rather
    # than on the credit, so the production the table implies reaches the book
    # and only the carry into the next slice is trimmed. What does not fit is
    # drawn off in `spec.PRODUCTS` order -- wheat first -- which is exactly the
    # stock that should go: wheat is the one product both the tape and the
    # rung's masked wheat-clone board hold, and the clone's share of the pile
    # is an artifact of masking its SELL orders, not something the recorded
    # seat was carrying. Whatever the seat still needs to sell is credited
    # again, uncapped, on the next slice.
    stock = seat_shed()
    excess = xp.maximum(
        xp.sum(xp.where(sel, xp.sum(st.shed, axis=1), 0)) - spec.SHED_CAPACITY, 0)
    spill = xp.clip(excess - (xp.cumsum(stock) - stock), 0, stock)
    return st._replace(shed=st.shed + shed_delta(-spill))


def mask_flow_seat(xp, mop, flow):
    """Blank the flow seat's own market-inventory orders. -> mop.

    SELL and BUY_PRODUCT only: those are the two ops that move `mkt_inv`, and
    the table is standing in for them. HIRE, BUY_LAND, BUY_SEED and BUY_ANIMAL
    stay live, so the seat still builds a kagg2-shaped board for the policy's
    opponent features to read -- they are fixed-price or seat-local and cannot
    move a quote.

    Applied *after* `compact_orders`, so no other slot shifts index and the
    pairing the engine does by position is untouched.
    """
    who = (xp.arange(2, dtype=xp.int32) == flow[FLOW_SEAT])[:, None, None]
    return xp.where(who & ((mop == O.MO_SELL) | (mop == O.MO_BUY_PRODUCT)),
                    O.MO_NONE, mop)


def _solo(xp, tables, st, p, op, item, ncap):
    """One player walking the market alone."""
    i32 = xp.int32
    is_sell = op == O.MO_SELL
    inv = st.mkt_inv[item]
    mode = xp.where(is_sell, M_SELL_SOLO, M_BUY_SOLO)
    q = _quotes(xp, tables, item, inv, mode)
    cum = xp.cumsum(q)
    j = xp.arange(K, dtype=i32)

    afford = xp.sum((cum <= st.money[p]).astype(i32))
    k = xp.clip(xp.where(is_sell, ncap, xp.minimum(ncap, afford)), 0, K - 1)
    total = _take(xp, cum, k)
    adv = xp.sum(((q > spec.PRICE_FLOOR) & (j < k)).astype(i32))

    d_money = xp.where(is_sell, total, -total)
    d_inv = xp.where(is_sell, adv, -k)
    d_shed = xp.where(is_sell, -k, k)
    return st._replace(
        money=st.money.at[p].add(d_money),
        mkt_inv=st.mkt_inv.at[item].add(d_inv),
        shed=st.shed.at[p, item].add(d_shed),
    )


def process_slot(tables, st, op, item, n, sell_only=False):
    """Resolve market order slot `i` for both players. op/item/n are [2].

    `sell_only` (static) compiles just the SELL path: a SELL turn carries
    nothing but sells and, in its last slot, the day's BUY_LAND -- which
    `rollout` resolves once per turn through `apply_land_row` rather than
    per slot. The hire / seed / animal / buy branches are most of this
    function's cost.
    """
    import jax.numpy as xp
    i32 = xp.int32

    if sell_only:
        act = (op == O.MO_SELL) & (n > 0)
        return _inventory_orders(xp, tables, st, op, item, n, act)

    # Atomic orders resolve once, in player order, and leave the lockstep.
    for p in range(2):
        # Bind `p` per iteration: these lambdas are applied immediately, but a
        # late-binding closure over a loop variable is the kind of thing that
        # only breaks once someone defers the call.
        st = _cond(xp, op[p] == O.MO_HIRE, lambda s, p=p: _hire(xp, s, p), st)
        st = _cond(xp, op[p] == O.MO_BUY_LAND, lambda s, p=p: _buy_land(xp, s, p), st)

    act = (op != O.MO_NONE) & (n > 0)
    sum_shed = xp.sum(st.shed, axis=1)
    room = xp.maximum(spec.SHED_CAPACITY - sum_shed, 0)

    # Fixed-price orders never touch market inventory, so they never couple.
    for p in range(2):
        it = xp.clip(item[p], 0, spec.N_CROPS - 1)
        cost = xp.asarray(spec.CROP_SEED_COST)[it]
        k = xp.where(act[p] & (op[p] == O.MO_BUY_SEED),
                     xp.minimum(n[p], st.money[p] // cost), 0)
        st = st._replace(money=st.money.at[p].add(-k * cost),
                         seeds=st.seeds.at[p, it].add(k))
    sum_shed = xp.sum(st.shed, axis=1)
    room = xp.maximum(spec.SHED_CAPACITY - sum_shed, 0)
    for p in range(2):
        it = xp.clip(item[p], 0, spec.N_ANIMALS - 1)
        cost = xp.asarray(spec.ANIMAL_COST)[it]
        k = xp.where(act[p] & (op[p] == O.MO_BUY_ANIMAL),
                     xp.minimum(xp.minimum(n[p], st.money[p] // cost), room[p]), 0)
        st = st._replace(money=st.money.at[p].add(-k * cost),
                         shed=st.shed.at[p, spec.I_GOOSE + it].add(k))

    return _inventory_orders(xp, tables, st, op, item, n, act)


def _inventory_orders(xp, tables, st, op, item, n, act):
    """SELL / BUY_PRODUCT: the orders that move market inventory."""
    i32 = xp.int32
    is_mkt = act & ((op == O.MO_SELL) | (op == O.MO_BUY_PRODUCT))
    it = xp.clip(item, 0, spec.N_PRODUCTS - 1)
    sum_shed = xp.sum(st.shed, axis=1)
    room = xp.maximum(spec.SHED_CAPACITY - sum_shed, 0)
    shed_have = xp.stack([st.shed[0, it[0]], st.shed[1, it[1]]])
    ncap = xp.where(op == O.MO_SELL, xp.minimum(n, shed_have), xp.minimum(n, room))
    ncap = xp.where(is_mkt, ncap, 0)

    same = is_mkt[0] & is_mkt[1] & (it[0] == it[1]) & (ncap[0] > 0) & (ncap[1] > 0)
    # A SELL meeting a BUY_PRODUCT on one item in one slot is the *cross*, and
    # it is a third regime, not a variant of the coupled one: the two commits
    # move market inventory in opposite directions, so above the floor the
    # inventory is back where it started at the end of every round and both
    # quotes stand still. That is exactly the trade `plan.OPEN_PUMP_ON` makes
    # on purpose against a foreign seat, and an action-tape opponent
    # (`es.tape_actions`) presents BUY_PRODUCT WHEAT opposite our SELL WHEAT
    # all season, so it has to be resolved rather than flagged.
    coupled = same & (op[0] == op[1])
    is_sell = op[0] == O.MO_SELL

    # Coupled segment: shared quote walk, inventory moving two units per round.
    inv = st.mkt_inv[it[0]]
    mode = xp.where(is_sell, M_SELL_PAIR, M_BUY_PAIR)
    q = _quotes(xp, tables, it[0], inv, mode)
    cum = xp.cumsum(q)
    j = xp.arange(K, dtype=i32)
    kc = xp.stack([
        xp.clip(xp.where(is_sell, ncap[p],
                         xp.minimum(ncap[p], xp.sum((cum <= st.money[p]).astype(i32)))),
                0, K - 1)
        for p in range(2)])
    m = xp.where(coupled, xp.minimum(kc[0], kc[1]), 0)

    seg1 = _take(xp, cum, m)
    adv1 = xp.sum(((q > spec.PRICE_FLOOR) & (j < m)).astype(i32))
    # Round m: the engine commits in player order, so a failure by one seat does
    # not undo the other's commit at the same quote.
    extra = coupled & (kc > m)
    qm = q[xp.clip(m, 0, K - 1)]
    n_extra = xp.sum(extra.astype(i32))
    adv2 = xp.where(is_sell, xp.sum((extra & (qm > spec.PRICE_FLOOR)).astype(i32)), 0)

    d_money_pair = xp.where(is_sell, seg1, -seg1) + \
        xp.where(extra, xp.where(is_sell, qm, -qm), 0)
    d_shed_pair = xp.where(is_sell, -(m + extra.astype(i32)), m + extra.astype(i32))
    d_inv_pair = xp.where(is_sell, 2 * adv1 + adv2, -(2 * m + n_extra))

    st = st._replace(
        money=st.money + xp.where(coupled, d_money_pair, 0),
        shed=st.shed.at[0, it[0]].add(xp.where(coupled, d_shed_pair[0], 0))
                    .at[1, it[1]].add(xp.where(coupled, d_shed_pair[1], 0)),
        mkt_inv=st.mkt_inv.at[it[0]].add(xp.where(coupled, d_inv_pair, 0)),
    )

    # --- the cross: one seat sells the item the other buys -----------------
    # `_commit_unit` pays the seller `P(inv)` and charges the buyer `P(inv-1)`,
    # both quoted off the same pre-commit inventory, and then moves the
    # inventory +1 and -1. So as long as the sale is above the floor (a $1 sale
    # adds no supply, `_commit_unit`) the inventory returns to `inv` after every
    # round and both prices are constant for the whole overlap. The seller never
    # fails -- `ncap` is already capped by its shed -- so the overlap is
    # `min(seller rounds, buyer's affordable rounds)`, after which whichever
    # order still has units left walks on alone from the *unchanged* `inv`,
    # which is what the `remaining` below hands to `_solo`.
    #
    # Below the floor the two directions no longer cancel (the sale stops
    # adding supply while the purchase keeps taking it away) and the walk has no
    # closed form; that case falls through to the two solo walks, which is what
    # this function did with every cross before.
    inv_s = xp.clip(inv - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    inv_b = xp.clip(inv - 1 - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    p_sell = tables.price[it[0], inv_s]
    p_buy = tables.price[it[0], inv_b]
    cross = same & (op[0] != op[1]) & (p_sell > spec.PRICE_FLOOR)
    seat_sells = op == O.MO_SELL
    rounds = xp.where(seat_sells, ncap,
                      xp.minimum(ncap, st.money // xp.maximum(p_buy, 1)))
    mx = xp.where(cross, xp.minimum(rounds[0], rounds[1]), 0)
    d_money_x = xp.where(seat_sells, mx * p_sell, -mx * p_buy)
    d_shed_x = xp.where(seat_sells, -mx, mx)
    st = st._replace(
        money=st.money + xp.where(cross, d_money_x, 0),
        shed=st.shed.at[0, it[0]].add(xp.where(cross, d_shed_x[0], 0))
                    .at[1, it[1]].add(xp.where(cross, d_shed_x[1], 0)),
    )

    # --- the cross AT the $1 floor [SIMGAP1] --------------------------------
    # With the sale at the floor it adds no supply while the purchase still
    # takes one away, so the inventory drifts down and the quotes move every
    # round: no closed form. The engine's per-unit lockstep, round by round
    # (`_process_market`: both quote off one pre-commit inventory, seller
    # `P(inv)`, buyer `P(inv-1)`, commits in player order; a buyer that cannot
    # pay is dropped). Used to fall through to two solo walks (seller first),
    # which paid the seller the floor for every unit and priced the buyer and
    # any later slot off the wrong inventory (6/100 dev boards, 2 coins).
    fx = same & (op[0] != op[1]) & ~(p_sell > spec.PRICE_FLOOR)
    s_idx = xp.where(seat_sells[0], 0, 1)
    b_idx = 1 - s_idx
    ncap_s, ncap_b = ncap[s_idx], ncap[b_idx]
    mon_b0 = st.money[b_idx]
    it0 = it[0]

    def _price_at(v):
        return tables.price[it0, xp.clip(v - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)]

    def _fx_cond(c):
        ks, kb, alive, v, gain, cost = c
        return fx & alive & (ks < ncap_s) & (kb < ncap_b)

    def _fx_body(c):
        ks, kb, alive, v, gain, cost = c
        ps, pb = _price_at(v), _price_at(v - 1)
        ok = (mon_b0 - cost) >= pb
        v = v + (ps > spec.PRICE_FLOOR).astype(i32) - ok.astype(i32)
        return (ks + 1, kb + ok.astype(i32), ok, v, gain + ps,
                cost + xp.where(ok, pb, 0))

    import jax
    z = xp.asarray(0, i32)
    ks, kb, alive, v_fx, gain, cost = jax.lax.while_loop(
        _fx_cond, _fx_body, (z, z, xp.asarray(True), inv, z, z))
    d_money_fx = xp.zeros(2, i32).at[s_idx].add(gain).at[b_idx].add(-cost)
    st = st._replace(
        money=st.money + xp.where(fx, d_money_fx, 0),
        shed=st.shed.at[s_idx, it0].add(xp.where(fx, -ks, 0))
                    .at[b_idx, it0].add(xp.where(fx, kb, 0)),
        mkt_inv=st.mkt_inv.at[it0].set(xp.where(fx, v_fx, st.mkt_inv[it0])),
    )
    rem_fx = xp.zeros(2, i32).at[s_idx].add(ncap_s - ks).at[b_idx].add(
        xp.where(alive, ncap_b - kb, 0))

    # Whoever ran out at round m is dropped; the survivor finishes alone.
    remaining = xp.where(coupled, xp.where(extra, ncap - (m + 1), 0),
                         xp.where(cross, ncap - mx, xp.where(fx, rem_fx, ncap)))
    for p in range(2):
        st = _solo(xp, tables, st, p, op[p], it[p], xp.maximum(remaining[p], 0))
    return st


def _cond(xp, pred, fn, st):
    """Apply fn(st) where pred, elementwise on every leaf."""
    out = fn(st)
    return st.__class__(*[xp.where(pred, b, a) for a, b in zip(st, out)])


def assert_no_cross(mkt_op, mkt_a, exempt=None):
    """SELL against BUY_PRODUCT on one item in one slot is not modelled.

    The planner emits an identical slot layout for both seats, so this never
    fires in self-play; it exists so the gap is loud rather than silent.

    `exempt` is a bool mask over the slots, for the one cross the planner makes
    on purpose: `plan.OPEN_PUMP_ON` sells wheat back at the head of the day-0
    BUY row precisely so it interleaves with a *foreign* seat's opening
    `BUY_PRODUCT WHEAT` at the drained quote. It cannot arise in self-play --
    both seats pump on day 0 and both present SELL there -- so exempting the
    slot narrows the guard by one slot on one day rather than weakening it.
    Pass `plan.open_pump_exempt(turn)`; `None` exempts nothing.
    """
    import numpy as _np
    o, a = _np.asarray(mkt_op), _np.asarray(mkt_a)
    sell, buy = o == O.MO_SELL, o == O.MO_BUY_PRODUCT
    cross = ((sell[0] & buy[1]) | (buy[0] & sell[1])) & (a[0] == a[1])
    if exempt is not None:
        cross = cross & ~_np.asarray(exempt, bool)
    if cross.any():
        raise AssertionError("SELL/BUY_PRODUCT cross-order on the same item is unmodelled")
