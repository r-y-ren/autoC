"""Episode rollout: 30 days x 24 turns, mirroring `interpreter()` statement order.

Per turn the engine does: unit actions, market queue, town consumption, plant
decay, then end-of-day on the last turn of a day. This module does the same, with
two structural choices:

* The **policy** runs once per day (hour 0) and its whole-day plan is replayed
  across the following 24 turns -- GOAL.md's day-level policy.
* Market resolution is wrapped in a `lax.cond` on the hour. The planner only
  places orders on hours 0-2, the three SELL turns and -- under
  `plan.PRESTOCK_ON` -- `ops.TURN_PRESTOCK`, and the hour is the inner scan
  index, which carries no batch dimension, so this stays a real branch under
  `vmap` rather than degenerating into a select that evaluates both sides.
"""

from __future__ import annotations

import os as _os

import jax
import jax.numpy as jnp

from .. import spec
from ..core import brain
from ..core import loop as _loop
from ..core import ops as O
from ..core import plan as P
from ..core import policy as PO
from . import eod, market
from .state import State, initial_state, prices_of

#: Does this tree carry the forward-admit gene (`g11`/`gb11`, `brain.decide`'s
#: `macro.forward_days`)? A layout written before the block has neither the
#: parameter nor the `Macro` field, and every diagnostic below is then absent
#: from the traced program rather than merely zero -- which is what keeps
#: `day_row` the five-column array it has always been on such a tree, and the
#: `day_tiles` output byte-identical there. See `es.train.make_evaluator`.
FWD_GENE = ("forward_days" in P.Macro._fields
            and any(n == "g11" for n, _ in PO.SHAPES))

_loop.install(lambda n, body, carry: jax.lax.fori_loop(0, n, lambda i, c: body(c), carry))

TPD = spec.TURNS_PER_DAY
MU = spec.MAX_UNITS
MO = spec.MAX_MARKET_ORDERS
_SERP = jnp.asarray(P.SERP)
#: SELL turns the cheap sell-only market path handles -- every one of them, by
#: `ops._check_schedule`'s invariant that no SELL turn is inside the full-row
#: window. Built once so the scan body does not rebuild it per turn.
_MELON_LOT_TURNS = tuple(P.melon_lot_turns()) if P.MELON_OPEN_ON else ()
#: The turns the three lots stand on [SWITCH, EARLY_SELL]. Mode "B" moves lots
#: 2 and 3 up and "A21" moves lot 2 alone; `SELL_TURNS[0]` stays in the set
#: whatever the mode, because it carries the day's BUY_LAND and lot 1's
#: fallback on a day no earlier row could hold it. The lot-1 modes ("A", "A1",
#: "A0") leave the set exactly as it was -- their turn rides a full-row turn.
_LOT_TURNS = tuple(P.early_lot_turns())
#: The rows `plan.SPREAD_ROWS_ON` cuts the day's voluntary sale over
#: [SWITCH, SPREAD_ROWS]. Read at import like every other row set here, after
#: the runner has set the switch. The row on `O.EARLY_SELL_LOT1_TURN` needs no
#: entry: it rides the BUY row, which is inside the full-row window already.
_SPREAD_TURNS = tuple(P.spread_rows_turns()) if P.SPREAD_ROWS_ON else ()
#: The hour-23 overflow row [SWITCH, SHED_DUMP_ROW]. Read at import like every
#: other row set here, after the runner has set the switch; OFF the turn is not
#: resolved at all and the day is the six market turns it always was.
_DUMP_TURNS = (P.SHED_DUMP_ROW_TURN,) if P.SHED_DUMP_ROW_ON else ()
#: The terminal day's last executed row [SWITCH, ENDROUTE]. Same import-time
#: read; OFF the turn is not resolved at all.
_END_TURNS = (P.ENDROUTE_TURN,) if P.ENDROUTE_ON else ()
#: The terminal day's SECOND late row [SWITCH, ENDROUTE_ROW2]. Same import-time
#: read; OFF the turn is not resolved at all.
_END2_TURNS = ((P.ENDROUTE_ROW2_TURN,)
               if (P.ENDROUTE_ON and P.ENDROUTE_ROW2_ON) else ())
_SELL_ONLY_TURNS = jnp.asarray(
    sorted(set(t for t in _LOT_TURNS if t >= O.FULL_MARKET_TURNS)
           | set(t for t in _SPREAD_TURNS if t >= O.FULL_MARKET_TURNS)
           | set(_MELON_LOT_TURNS) | set(_DUMP_TURNS)
           | set(_END_TURNS) | set(_END2_TURNS)), jnp.int32)
#: Every turn on which a market row is resolved, in turn order -- hours
#: 0..FULL_MARKET_TURNS-1, the SELL turns, and `TURN_PRESTOCK` under
#: `plan.PRESTOCK_ON`. This is `turn_body`'s `full_row | later_sell` set written
#: out, and it is what `--tape-flow-spread` divides a tape's day between: the
#: turns the tape is allowed to trade on are exactly the ones we trade on.
MARKET_TURNS = tuple(sorted(
    set(range(O.FULL_MARKET_TURNS)) | set(_LOT_TURNS) | set(_MELON_LOT_TURNS)
    | set(_SPREAD_TURNS)
    | set(_DUMP_TURNS) | set(_END_TURNS) | set(_END2_TURNS)
    | ({O.TURN_PRESTOCK}
       if (P.PRESTOCK_ON or (P.PRESTOCK_V2_ON and P.PRESTOCK_V2_BUY_ON))
       else set())))
_MARKET_TURNS = jnp.asarray(MARKET_TURNS, jnp.int32)
#: The default `run_day(tape_ctl=)`: the tape in physical seat 1, table 0.
TAPE_ON = (1, 0)
#: `tape_ctl` for an episode of a tape-enabled batch that plays no tape.
TAPE_OFF = (-1, 0)

#: [HIRE-STICKY] The sim-seat port of `scripts/tape_opponent.py --hire-sticky`
#: (`docs/strategy/2026-09-14-tape-hire-fix.md`). A HIRE the tape's purse cannot
#: pay for is dropped in silence by `_do_hire` and never retried, so the tape
#: plays the rest of the day -- and, through the cash spiral, the rest of the
#: game -- a hand short of the roster it was recorded with; on the worst TOPB3
#: board that is 0 coins against a source 76,484. With the flag on, a tape seat
#: re-issues the hires it owes on the later turns of the SAME day, appended
#: BEHIND its own recorded market row (so behind the SELLs that pay for them)
#: and capped at the roster the recording itself reached, `tape.src_hands`.
#:
#: Default OFF, and OFF is read at trace time (a Python bool, like
#: `plan.PRESTOCK_ON`), so an unflagged run emits the device program it always
#: emitted -- not a masked-out copy of the new one. A tape with no `src_hands`
#: (every `.npz` cut before the field existed) is the same static no-op.
#:
#: `KAGG3_TAPE_HIRE_STICKY=1` at import, or `setattr(rollout, "HIRE_STICKY",
#: True)` before the first trace, which is how the `S/` harnesses set switches.
#: The unit-order half of the engine-side flag (`_MAP`, live hand -> source
#: hand) is NOT ported and does not need to be: the sim addresses unit slot `u`
#: with `uop[d, u, h]` and masks slots past the live roster in
#: `units.apply_units`, which is that map already, and the map provably reduces
#: to the identity anyway (ibid. §2).
HIRE_STICKY = _os.environ.get("KAGG3_TAPE_HIRE_STICKY", "").strip().lower() \
    not in ("", "0", "no", "off", "false")


def day_view(st: State, p: int, day, price) -> P.DayView:
    g = _SERP
    q = 1 - p
    return P.DayView(
        day=day,
        kind=st.kind[p][g], occ=st.occ[p][g], t_day=st.t_day[p][g],
        t_water=st.t_water[p][g], t_cons=st.t_cons[p][g], t_yield=st.t_yield[p][g],
        t_fert=st.t_fert[p][g], t_cared=st.t_cared[p][g], t_favail=st.t_favail[p][g],
        shed=st.shed[p], seeds=st.seeds[p], money=st.money[p], nquad=st.nquad[p],
        price=price, mkt_inv=st.mkt_inv, shops=st.shops, t_bank=st.t_bank[p][g],
        # The other seat's standing book, the same whole-array reduction
        # `policy_obs` already hands the network as `opp_kind`/`opp_occ`. Raw
        # board order: `opp_commitment` counts and never indexes a tile table.
        opp_commit=P.opp_commitment(jnp, st.kind[q], st.occ[q]),
        # PROGRAM1 selector-only public fields.  The frozen 64-vector ignores
        # them; `program_selector_features` reduces the raw board arrays.
        program_opp_money=st.money[q], opp_kind=st.kind[q], opp_occ=st.occ[q],
        opp_t_day=st.t_day[q], opp_t_yield=st.t_yield[q], seat=jnp.int32(p),
        # [SWITCH, SELL_SLOT_PRIORITY] The same reduction over the other
        # seat's standing yield. Built only when the switch that reads it is
        # on, so an OFF rollout traces the graph it always traced.
        **({"opp_ripe": P.opp_ripe_yield(jnp, st.kind[q], st.occ[q],
                                         st.t_yield[q])}
           if P.SELL_SLOT_PRIORITY_ON else {}),
        # [SWITCH, SELL_SLOT_MIRROR_GATE] The rival purse, for the gate's
        # money-lead veto only -- `policy_obs` already reads `st.money[q]`.
        **({"opp_money": st.money[q]} if P.SELL_SLOT_MIRROR_GATE_ON else {}),
    )


def policy_obs(st: State, p: int, day, price, prev_mkt_inv=None) -> brain.PolicyObs:
    q = 1 - p
    # Direct legacy callers have no history, so their feature is exactly zero.
    # `episode` always supplies the prior dawn explicitly after its first day.
    prev_mkt_inv = st.mkt_inv if prev_mkt_inv is None else prev_mkt_inv
    return brain.PolicyObs(
        day=day, money=st.money[p], opp_money=st.money[q],
        kind=st.kind[p], occ=st.occ[p], opp_kind=st.kind[q], opp_occ=st.occ[q],
        t_day=st.t_day[p], t_yield=st.t_yield[p],
        shed=st.shed[p], seeds=st.seeds[p],
        nquad=st.nquad[p], opp_nquad=st.nquad[q],
        mkt_inv=st.mkt_inv, price=price, shops=st.shops,
        # Public board state, same as `opp_kind`/`opp_occ`: `brain.
        # production_forecast` needs the opponent's clock to say *when* their
        # supply lands. Raw board order, and the forecast only reduces.
        opp_t_day=st.t_day[q], opp_t_yield=st.t_yield[q],
        prev_mkt_inv=prev_mkt_inv,
    )


def town_consume(st: State) -> State:
    step = st.step
    shop = (st.shops @ jnp.asarray(spec.SHOP_CONSUME)) * \
        (step % spec.SHOP_SELL_INTERVAL == 0)
    center = jnp.asarray(spec.TOWN_CENTER_CONSUME) * \
        (step % spec.TOWN_CENTER_SELL_INTERVAL == 0)
    return st._replace(mkt_inv=st.mkt_inv - shop - center)


def decay_plants(st: State) -> State:
    step = st.step
    is_pl = st.kind == spec.KIND_PLANT
    mls = st.t_life
    tick = is_pl & (mls >= 0) & (step >= mls) & (((step - mls) % 2) == 0)
    ny = jnp.where(tick, st.t_yield - 1, st.t_yield)
    dead = tick & (ny <= 0)
    # A weed in the engine is a bare {"kind": "WEED"} with no plant fields, so
    # clear the lot. Nothing reads them (every planner rule that touches
    # t_cons / t_fert is gated on the tile being a PLANT), but leaving stale
    # values behind would make the state non-canonical and every future
    # sim-vs-engine diff noisier than it needs to be.
    return st._replace(
        kind=jnp.where(dead, spec.KIND_WEED, st.kind),
        occ=jnp.where(dead, -1, st.occ),
        t_yield=jnp.where(dead, 0, ny),
        t_life=jnp.where(dead, -1, st.t_life),
        t_day=jnp.where(dead, 0, st.t_day),
        t_water=jnp.where(dead, 0, st.t_water),
        t_cons=jnp.where(dead, 0, st.t_cons),
        t_fert=jnp.where(dead, -1, st.t_fert),
    )


def compact_orders(mop, ma, mq):
    """Market rows as the engine receives them: `render.py` drops MO_NONE
    slots, so live orders shift left and the engine pairs the two seats by the
    index in that compacted list, not by the planner's fixed product slot.

    Works on any leading shape `[..., MO]`; called once per day on the whole
    `[2, TPD, MO]` block so the turn scan body stays unchanged.
    """
    i32 = jnp.int32
    live = (mop != O.MO_NONE).astype(i32)                        # [..., MO]
    dest = jnp.cumsum(live, axis=-1) - live
    n = mop.shape[-1]
    slot = jnp.arange(n, dtype=i32)
    sel = ((dest[..., None, :] == slot[:, None]) & (live[..., None, :] > 0)).astype(i32)
    gather = lambda a: jnp.sum(sel * a[..., None, :], axis=-1)
    mop_c = jnp.where(jnp.sum(sel, axis=-1) > 0, gather(mop), O.MO_NONE)
    return mop_c, gather(ma), gather(mq)


def _market_turn(tables, st, mop, ma, mq, sell_only=False, land=False,
                 sales=False):
    """Walk the ten order slots in engine order.

    A scan rather than a Python loop: the slot body is large (two atomic-order
    branches plus the quote walks), and unrolling it ten times inside a 24-turn
    scan inside a 29-day scan makes XLA compilation the dominant cost. Semantics
    are identical -- slots still resolve strictly in order.

    Rows must already be compacted (`compact_orders`); `run_day` does that once
    per day.

    `sales` is a trace-time Python bool, off by default, and is the only writer
    of `State.sold_n` / `.sold_rev` / `.sold_rows`. It is measured here rather
    than inside `market.process_slot` because a sale resolves down three
    different paths there (the coupled walk, the cross, and the solo remainder)
    and the *slot* is where the three are already summed. Within one slot a
    seat carries exactly one op, so when that op is `MO_SELL` the slot's whole
    money gain is sale revenue and its whole shed drop is units sold: no other
    branch of `process_slot` fires for that seat. A row is counted only if it
    actually moved a unit -- a SELL against an empty shed is not a slice.

    A flow rung's exogenous seat (`market.apply_flow`) never passes through
    here, so its sales are *not* in the ledger; that seat is credited for goods
    it never grew, and its realised price is fiction. An action-tape opponent
    does pass through here, and is measured like any other seat.
    """
    def body(carry, x):
        op, arg, qty = x
        if not sales:
            return market.process_slot(tables, carry, op, arg, qty, sell_only=sell_only), None
        was_money, was_shed = carry.money, carry.shed.sum(axis=1)
        out = market.process_slot(tables, carry, op, arg, qty, sell_only=sell_only)
        sold = jnp.where(op == O.MO_SELL, was_shed - out.shed.sum(axis=1), 0)
        rev = jnp.where(op == O.MO_SELL, out.money - was_money, 0)
        # [WHEATMIX1] per item: one SELL per seat per slot, so the item whose shed fell carries the slot's revenue
        sold_i = jnp.where((op == O.MO_SELL)[:, None], carry.shed - out.shed, 0)
        return out._replace(
            sold_n=out.sold_n + sold,
            sold_rev=out.sold_rev + rev,
            sold_rows=out.sold_rows + (sold > 0).astype(jnp.int32),
            sold_ni=out.sold_ni + jnp.maximum(sold_i, 0),
            sold_ri=out.sold_ri + jnp.where(sold_i > 0, rev[:, None], 0)), None

    st, _ = jax.lax.scan(body, st, (mop.T, ma.T, mq.T))
    if land:
        # The day's BUY_LAND rides the last slot of a SELL turn [M2]; it is
        # atomic and seat-local, so resolving it after the turn's sells is
        # exactly the engine's order (`market.apply_land_row`).
        st = market.apply_land_row(jnp, st, mop)
    return st


def run_day(tables, st: State, day, words, hi_t, lo_t, thetas, n_turns=TPD, do_eod=True,
            flow=None, flow_backed=False, flow_spread=False, shop_crn=False,
            tape=None, tape_ctl=None, tape_turns=None, day_metrics=False,
            prev_mkt_inv=None):
    price = prices_of(jnp, tables, st.mkt_inv)
    # Freeze one public pair before either seat plans.  Neither seat order nor a
    # later tape override may mutate the history seen at this dawn.
    previous = st.mkt_inv if prev_mkt_inv is None else prev_mkt_inv
    plans = [brain.decide(jnp, thetas[p],
                          policy_obs(st, p, day, price, previous))
             for p in range(2)]
    # [`day_metrics`] The day's decoded forward-admit horizon, both seats, read
    # off the macro the day is about to be planned from -- no second decode and
    # no second rollout. `day_metrics` and `FWD_GENE` are both Python bools
    # read at trace time, so a run that did not ask for the metrics (or a tree
    # with no `g11`) emits not one instruction of this and returns the bare
    # state it always returned.
    fwd = (jnp.stack([p.forward_days for p in plans]).astype(jnp.int32)
           if day_metrics and FWD_GENE else None)
    built = [P.build_day(jnp, day_view(st, p, day, price), plans[p], tables.price)
             for p in range(2)]

    uop = jnp.stack([b[0] for b in built])          # [2, MU, TPD]
    ua = jnp.stack([b[1] for b in built])
    uq = jnp.stack([b[2] for b in built])
    mop, ma, mq = compact_orders(jnp.stack([b[3] for b in built]),     # [2, TPD, MO]
                                 jnp.stack([b[4] for b in built]),
                                 jnp.stack([b[5] for b in built]))

    # --- the action-replay seat (`--tape-actions`, `es.tape_actions`) --------
    # Seat 1's whole day, unit ops and market rows alike, is a gather from the
    # recorded tape rather than anything the planner produced. `tape is None`
    # is the static "no such seat in this program" case and emits nothing, so an
    # unflagged run's device program is the one it always was.
    #
    # The seat-1 plan above is still *built* (both seats' `build_day` share one
    # traced call) and then discarded: it costs a little compile time and no
    # accuracy, and it keeps this override a two-line splice into the existing
    # day rather than a second, divergent day body.
    #
    # `tape_ctl` is the int32 `[seat, table]` control word, the same shape of
    # thing `market.apply_flow`'s is and for the same reason: the trainer plays
    # every pair in both seats, so the tape has to be able to sit in either one,
    # and one traced program has to serve a batch drawn from several tapes. A
    # negative seat is an episode of a tape-enabled batch that is not playing a
    # tape rung, which is `flow_control`'s convention exactly.
    #
    # The market rows are NOT compacted. Compaction models `render.py` dropping
    # the planner's empty slots before the engine sees them; a tape's row is
    # already the list the engine received, and `_process_market` pairs the two
    # seats by raw queue position, so a refused order there holds its slot.
    town_row = None
    sticky = None
    if tape is not None:
        ctl = jnp.asarray(TAPE_ON if tape_ctl is None else tape_ctl, jnp.int32)
        seat, t = ctl[0], ctl[1]
        on = jnp.arange(2, dtype=jnp.int32) == seat                   # [2]
        pick = lambda a: a[jnp.clip(t, 0, a.shape[0] - 1), day][None]
        uop = jnp.where(on[:, None, None], pick(tape.uop), uop)
        ua = jnp.where(on[:, None, None], pick(tape.ua), ua)
        uq = jnp.where(on[:, None, None], pick(tape.uq), uq)
        mop = jnp.where(on[:, None, None], pick(tape.mop), mop)
        ma = jnp.where(on[:, None, None], pick(tape.ma), ma)
        mq = jnp.where(on[:, None, None], pick(tape.mq), mq)
        if tape.town is not None:
            # [`--with-town`] The recorded TOWN of the same episode, int32 [ND]
            # indexed by the day a shop becomes visible. It is a property of the
            # board, not of the seat -- the engine's town is shared -- so it is
            # not masked by `on`; it is only switched off for an episode whose
            # `tape_ctl` seats no tape at all (a negative seat, `flow_control`'s
            # convention), which then draws its shops exactly as before.
            # `tape.town is None` is the static "no tape here carries a town"
            # case and leaves `eod.unlock_shop`'s program untouched.
            row = tape.town[jnp.clip(t, 0, tape.town.shape[0] - 1)]   # [ND]
            town_row = jnp.where(seat >= 0, row, eod.NO_UNLOCK)
        if HIRE_STICKY and tape.src_hands is not None:
            # [HIRE-STICKY] This day's two host-side rows, gathered exactly as
            # the action tables are: the roster the RECORDING had at the start
            # of each of the day's 24 turns, and the length of its recorded
            # market row there (where a re-issue is appended). Both are `None`
            # -> this whole block is absent, at trace time.
            g = lambda a: a[jnp.clip(t, 0, a.shape[0] - 1), day]      # [TPD]
            sticky = (g(tape.src_hands), g(tape.mlen), on)
    tape_turns = MARKET_TURNS if tape_turns is None else tuple(tape_turns)
    _TAPE_MARKET = jnp.asarray(tape_turns, jnp.int32)

    # The exogenous kagg2 flow (`market.apply_flow`). `flow is None` is the
    # static "no such rung in this program" case and emits nothing at all, so an
    # unflagged run's device program is the one it always was; a `flow` array
    # whose seat is negative is the same thing decided at trace time, for the
    # episodes of a flow-enabled run that are not playing the rung.
    #
    # Order matters twice over: the day-boundary `price` above is read *before*
    # the flow moves anything, because that is the quote both agents plan
    # against in the engine; and the seat's own orders are blanked after
    # compaction, because compaction is what fixes the slot pairing.
    #
    # `--tape-flow-spread` (`flow_spread`) keeps the masking and the
    # day-boundary quote exactly as above and only moves *when* the table is
    # spent: the day's rows are read once here and `turn_body` applies one
    # `len(MARKET_TURNS)`-th of them on each market turn instead. Both flags are
    # Python bools, read at trace time, so a run with them off emits the code it
    # always did.
    f_rows = None
    if flow is not None:
        mop = market.mask_flow_seat(jnp, mop, flow)
        if flow_spread:
            # `grow=flow_backed`: the production row is `--tape-flow-backed`'s
            # input and nothing else reads it, so with the switch off this
            # gathers the two tables it always gathered.
            f_rows = market.flow_rows(jnp, day, flow, grow=flow_backed)
        else:
            st = market.apply_flow(jnp, tables, st, day, flow, backed=flow_backed)

    def turn_body(st, h, rows=None):
        # `rows` is [HIRE-STICKY]'s hook: the turn's market row for both seats,
        # already carrying this turn's re-issued HIREs. `None` -- every call on
        # the default path -- traces the same three gathers it always did.
        from .units import apply_units
        mop_h, ma_h, mq_h = (mop[:, h], ma[:, h], mq[:, h]) if rows is None else rows
        st = apply_units(jnp, st, day, uop[:, :, h], ua[:, :, h], uq[:, :, h])
        if f_rows is not None:
            # [`--tape-flow-spread`] This turn's share of the tape's day, in
            # front of our own row for the same turn -- the engine commits in
            # player order off one pre-commit inventory, and putting the tape
            # first is the same conservative reading the unspread path takes.
            # After `apply_units`, so the day's harvest is in the shed before
            # `--tape-flow-backed` asks what the seat can actually sell.
            # `h` is the inner scan index and carries no batch dimension, so
            # this stays a real branch under `vmap`.
            part = jnp.sum((_MARKET_TURNS < h).astype(jnp.int32))
            st = jax.lax.cond(
                jnp.any(h == _MARKET_TURNS),
                lambda s: market.apply_flow(jnp, tables, s, day, flow,
                                            backed=flow_backed, rows=f_rows,
                                            part=part,
                                            nparts=len(MARKET_TURNS)),
                lambda s: s, st)
        # Turns 0 .. FULL_MARKET_TURNS-1 carry the full market row (both HIRE
        # rows and the BUY row); every SELL turn carries SELL orders and, in
        # its last slot, the day's BUY_LAND, and takes the cheaper sell-only
        # path plus one atomic land conditional. `ops._check_
        # schedule` keeps the two sets disjoint, so no turn is resolved twice
        # and none is skipped.
        later_sell = jnp.any(h == _SELL_ONLY_TURNS)
        # `plan.PRESTOCK_ON`'s row: BUY_PRODUCT and BUY_SEED at
        # `O.TURN_PRESTOCK`, a turn no other row uses. It needs the *full*
        # market path (the sell-only one skips buys), so it is a third branch
        # rather than a wider `_SELL_ONLY_TURNS`. Read at trace time, so with
        # the switch off the device program is the one it always was.
        full_row = h < O.FULL_MARKET_TURNS
        if P.PRESTOCK_ON or (P.PRESTOCK_V2_ON and P.PRESTOCK_V2_BUY_ON):
            # `PRESTOCK_V2_ON` emits the same row on the same turn [SWITCH].
            full_row = full_row | (h == O.TURN_PRESTOCK)
        if tape is not None:
            # A recorded seat trades on hours the planner never uses -- the six
            # band tapes present a market row on all 24 of them -- so the
            # schedule is the union of ours and the tape's, read at trace time
            # off the file. Every turn in it takes the FULL path: the tape buys
            # and hires at arbitrary hours, and the cheap sell-only path skips
            # both. `land=False` with it, because the full path already resolves
            # BUY_LAND atomically in its own slot, which is where the engine
            # resolves it -- `apply_land_row` is the sell-only path's stand-in
            # for exactly that and would double-buy here.
            body = lambda s: _market_turn(tables, s, mop_h, ma_h, mq_h,
                                          sales=day_metrics)
            st = (body(st) if len(tape_turns) == TPD
                  else jax.lax.cond(jnp.any(h == _TAPE_MARKET), body,
                                    lambda s: s, st))
        else:
            st = jax.lax.cond(
                full_row,
                lambda s: _market_turn(tables, s, mop_h, ma_h, mq_h,
                                       sales=day_metrics),
                lambda s: jax.lax.cond(
                    later_sell,
                    lambda s2: _market_turn(tables, s2, mop_h, ma_h, mq_h,
                                            sell_only=True, land=True,
                                            sales=day_metrics),
                    lambda s2: s2, s),
                st)
        st = town_consume(st)
        st = decay_plants(st)
        return st._replace(step=st.step + 1), None

    if sticky is None:
        st, _ = jax.lax.scan(turn_body, st, jnp.arange(n_turns, dtype=jnp.int32))
    else:
        # [HIRE-STICKY] The same day, with two int32 scalars added to the carry:
        # `owed`, how many hires the tape seat still has to make good today, and
        # `prev`, its roster when the previous turn was planned (the engine-side
        # agent's `_STATE["owed"]` / `_STATE["live"]`, whose `_MAP` half is the
        # identity here -- see the flag's note above).
        src_h, mlen, on_seat = sticky
        slot_ix = jnp.arange(MO, dtype=jnp.int32)

        def sticky_body(carry, h):
            st, owed, prev = carry
            # The roster the seat would observe now: unit actions and the market
            # row are both still ahead of it this turn, and `market._hire` is
            # the only thing that moves it, so this is the engine agent's
            # `_hand_count(observation)`.
            live = jnp.sum(jnp.where(on_seat, st.nhands, 0))
            at0 = h == 0                       # the nightly wipe: no owed hires
            prev = jnp.where(at0, live, prev)
            added = jnp.where(at0, 0, src_h[h] - src_h[jnp.maximum(h - 1, 0)])
            owed = jnp.where(at0, 0, jnp.maximum(0, owed + added - (live - prev)))
            # Cap: the roster the source itself reached by the start of the next
            # turn. Nothing is owed across midnight, so the day's last turn
            # re-issues nothing.
            room = jnp.where(h + 1 < TPD, src_h[jnp.minimum(h + 1, TPD - 1)] - live, 0)
            extra = jnp.clip(jnp.minimum(owed, room), 0, MO)
            hit = (slot_ix >= mlen[h]) & (slot_ix < mlen[h] + extra)   # [MO]
            sel = on_seat[:, None] & hit[None, :]                     # [2, MO]
            rows = (jnp.where(sel, O.MO_HIRE, mop[:, h]),
                    jnp.where(sel, 0, ma[:, h]),
                    jnp.where(sel, 1, mq[:, h]))
            st, _ = turn_body(st, h, rows)
            return (st, owed, live), None

        (st, _, _), _ = jax.lax.scan(
            sticky_body, (st, jnp.int32(0), jnp.int32(0)),
            jnp.arange(n_turns, dtype=jnp.int32))
    if do_eod:
        st = eod.end_of_day(jnp, st, day, words, hi_t, lo_t, shop_crn=shop_crn,
                            town=town_row)
    # `day_metrics` is the caller's trace-time bool, so the return *type* is a
    # static fact about the program: every call that did not ask for the day's
    # metrics gets the state alone, exactly as before.
    return (st, fwd) if day_metrics else st


def day_row(st, fwd=None):
    """Per-seat board and sale ledger at this instant. -> int32 [2, 5] or [2, 6]

    Columns: `(planted, idle, units sold, sale coins, SELL rows)`. The first
    two are counts of the board *now*; the last three are the season-to-date
    cumulative totals `_market_turn(sales=True)` keeps, so a window's figures
    are the difference of two days' rows and nothing has to be stored per turn.

    `fwd` is the day's decoded forward-admit horizon per seat (int32 [2],
    `brain.decide`'s `macro.forward_days`, the `g11` gene) or `None`. Given, it
    is appended as a **sixth** column and is the one entry that is *not*
    cumulative: it is today's reading, because a horizon is a decision and not
    a ledger, and `es.train`'s diagnostic sums it over the season itself.
    `None` -- every caller before the gene existed, and every tree whose layout
    has no `g11` (`FWD_GENE`) -- appends nothing and the array is the
    five-column one it always was.

    `planted` is `KIND_PLANT` -- a crop tile, which is what the day-10 board
    ledger counted ("56 planted tiles to our 47"). A coop or a pasture is
    neither planted nor idle: it is a *placed* tile, and the two counts are
    deliberately not a partition of the board.

    `idle` is an unlocked tile holding no crop and no animal: `KIND_EMPTY` plus
    `KIND_WEED`. A weed is an empty tile the end-of-day draw landed on, and it
    has to be dug before anything can be planted there, so for the purpose of
    "how much of the board is working" it is the same state as empty. The
    snapshot is taken *after* `end_of_day`, which is where `spawn_weeds` runs,
    so counting `KIND_EMPTY` alone would silently drop the tiles that had just
    been turned over.

    Locked tiles are in neither count, which is what makes the difference
    `planted - idle` a statement about the board a seat has actually bought.
    """
    planted = (st.kind == spec.KIND_PLANT).sum(axis=1)
    idle = ((st.kind == spec.KIND_EMPTY)
            | (st.kind == spec.KIND_WEED)).sum(axis=1)
    cols = [planted, idle, st.sold_n, st.sold_rev, st.sold_rows]
    if fwd is not None:
        cols.append(fwd)
    return jnp.stack(cols, axis=1).astype(jnp.int32)


def episode(tables, thetas, words, hi_t, lo_t, start_nquad=None, start_money=None,
            flow=None, flow_backed=False, flow_spread=False,
            tape=None, tape_ctl=None, tape_turns=None, shop_crn=False,
            day_tiles=False):
    """thetas [2, N_PARAMS], words [N_DAYS, STREAM_WORDS] -> final money [2].

    `start_nquad` / `start_money` (int32 [2]) select a warm start, see
    `state.initial_state`; omitted, the season opens on the engine's day 0.

    `flow` is `market.apply_flow`'s int32 [3] control word, or `None`. `None` is
    static and emits no flow code whatsoever, which is what makes an unflagged
    run bit-identical rather than merely equal; `market.FLOW_OFF` is the same
    behaviour with the code present, for the episodes of a flow-enabled batch
    that are not playing the rung.

    `tape` is an `es.tape_actions.TapeActions` whose six arrays are device
    arrays with a leading table axis (`tape_actions.stack` then `.device`), or
    `None`, and `tape_ctl` is its int32 `[seat, table]` control word per
    episode (`TAPE_ON` = seat 1, table 0, is the default and what the parity
    gate uses; a negative seat plays no tape). With one, seat 1 plays no policy
    at all: every unit order and every market row it presents is the recorded
    frame for that turn, applied through `units.apply_units` and
    `_market_turn` exactly as ours is. `tape_turns` is the static set of hours
    on which a market row resolves -- `MARKET_TURNS | tape.hours` -- and it
    must cover every hour any member of a `vmap` batch trades on
    (`tape_actions.stack` takes that union).

    `flow_backed` / `flow_spread` are `--tape-flow-backed` / `--tape-flow-spread`
    (`es.train.Config.tape_flow_backed` / `.tape_flow_spread`): Python bools,
    read at trace time, both off by default. See `market.apply_flow`.

    `shop_crn` is `--shop-crn` (`es.train.Config.shop_crn`), the same kind of
    trace-time bool, also off by default: it moves the end-of-day shop draw off
    the weed walk's moving cursor, so two candidates that plant differently
    still unlock the same shops. See `eod.SHOP_CRN_BASE`.

    `day_tiles` is a trace-time Python bool, off by default: on, the return
    grows a **fourth** element, `day_row(st)` stacked per day (int32 [N_DAYS,
    2, 5] -- day, seat, (planted, idle, units sold, sale coins, SELL rows),
    plus a sixth column, that day's decoded `macro.forward_days`, on a tree
    that carries the `g11` gene, see `FWD_GENE`),
    alongside the per-day money `daily` already carries, and `run_day` keeps
    the sale ledger those last three columns read. Off -- every call before
    `es.train`'s day-10 fitness terms existed -- not one instruction of either
    is emitted and the return is the 3-tuple it always was, which is why every
    other caller in the tree is untouched. The board counts are read off the
    state the day scan already carries and the ledger off the market slot that
    was resolving anyway, so this is a wider output, never a second pass.

    The engine stops at step `episodeSteps - 2` = 718, so the season is 29 full
    days plus 23 turns, with no end-of-day refresh after the last one. That final
    refresh cannot move money (only the market and hiring do, and those happen on
    hours 0-2), but reproducing the cut keeps the whole trajectory comparable and
    not just the reward.
    """
    st = initial_state(jnp, start_nquad, start_money)

    def day_body(carry, d):
        st, previous = carry
        current = st.mkt_inv
        out = run_day(tables, st, d, words[d], hi_t, lo_t, thetas, flow=flow,
                      flow_backed=flow_backed, flow_spread=flow_spread,
                      shop_crn=shop_crn,
                      tape=tape, tape_ctl=tape_ctl, tape_turns=tape_turns,
                      day_metrics=day_tiles, prev_mkt_inv=previous)
        # `day_tiles` is a Python bool read at trace time, so the default run
        # scans out `st.money` and nothing else, exactly as it always did.
        if not day_tiles:
            return (out, current), out.money
        st, fwd = out
        return (st, current), (st.money, day_row(st, fwd))

    # The first previous value equals the first current dawn, hence zero.  Each
    # completed day carries the inventory that was current before that day's
    # actions, so day d+1 observes dawn[d] - dawn[d+1].
    (st, previous), scanned = jax.lax.scan(
        day_body, (st, st.mkt_inv),
        jnp.arange(spec.N_DAYS - 1, dtype=jnp.int32))
    daily, rows = scanned if day_tiles else (scanned, None)
    last = spec.N_DAYS - 1
    out = run_day(tables, st, jnp.int32(last), words[last], hi_t, lo_t, thetas,
                  n_turns=TPD - 1, do_eod=False, flow=flow,
                  flow_backed=flow_backed, flow_spread=flow_spread,
                  shop_crn=shop_crn,
                  tape=tape, tape_ctl=tape_ctl, tape_turns=tape_turns,
                  day_metrics=day_tiles, prev_mkt_inv=previous)
    st, fwd = out if day_tiles else (out, None)
    daily = jnp.concatenate([daily, st.money[None, :]])
    if day_tiles:
        return st.money, daily, st, jnp.concatenate(
            [rows, day_row(st, fwd)[None, :, :]])
    return st.money, daily, st
