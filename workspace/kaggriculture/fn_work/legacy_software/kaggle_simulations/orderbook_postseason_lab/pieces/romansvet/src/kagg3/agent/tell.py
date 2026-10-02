"""RIVAL_TELL: the rival's own sales, read off the public pot one turn behind.

`docs/strategy/2026-09-16-rivaltell.md` sect.7 is the spec and sect.2 the
derivation; this module is that estimator re-derived against the engine in
production code (nothing is imported from `S/`).  The three engine lines it
stands on (`kaggle_environments/envs/kaggriculture/kaggriculture.py`):

  `_commit_unit`  SELL -> `market.inventory[item] += 1`, **only above the price
                  floor**; `BUY_PRODUCT` -> `-= 1`                 (:652-674)
  `_town_consume` every unlocked shop INSTANCE eats `spec.SHOP_CONSUME` on
                  `step % 4 == 0`, the centre eats `TOWN_CENTER_CONSUME` on
                  `step % 24 == 0`                                 (:728-751)
  interpreter     unit ops -> market -> town -> decay -> end of day (:894-946)

so the pot a seat reads at the top of step `t+1` satisfies, exactly,

    inv[t+1] - inv[t] = (our_sell + riv_sell) - (our_buy + riv_buy) - town(t)

and with our own row known,

    riv_net(t) = inv[t+1] - inv[t] + town(t) - our_sell(t) + our_buy(t)

which is `riv_sell(t) - riv_buy(t)`: a NET, and therefore blind to a rival that
buys and sells the same item on the same turn.  Measured on 50 real engine
games (sect.3 of that doc): precision 1.000, recall 0.976 with the miss rate
carried entirely by WHEAT and FERTILIZER -- the two items
`plan.RIVAL_TELL_SKIP` refuses to gate on.

Our own side is the row we ORDERED, not the units that cleared: the observation
carries no fill report, and the doc prices that choice at 0.2 % of cells.
"""

from __future__ import annotations

import numpy as np

from .. import spec
from ..core import plan as P

#: `batch()` sentinel: no measurement for this item, keep the `opp_ripe` proxy.
NO_RATE = -1


def town_tick(step: int, shops) -> np.ndarray:
    """int[9]: units the town removes from the pot on engine step `step`."""
    out = np.zeros(spec.N_PRODUCTS, np.int32)
    if step % spec.SHOP_SELL_INTERVAL == 0:
        out += np.asarray(shops, np.int32) @ spec.SHOP_CONSUME
    if step % spec.TOWN_CENTER_SELL_INTERVAL == 0:
        out += spec.TOWN_CENTER_CONSUME
    return out.astype(np.int32)


def rival_net(inv, prev_inv, step, shops, our_sell, our_buy) -> np.ndarray:
    """int[9]: the rival's NET sales on step `step`.

    `inv` is the pot at the top of step `step + 1`, `prev_inv` / `shops` the pot
    and the unlocked-shop counts at the top of `step`, `our_sell` / `our_buy`
    our own market row for that step.
    """
    return (np.asarray(inv, np.int32) - np.asarray(prev_inv, np.int32)
            + town_tick(step, shops)
            - np.asarray(our_sell, np.int32)
            + np.asarray(our_buy, np.int32)).astype(np.int32)


def order_units(market_row):
    """(sell[9], buy[9]) from one rendered `render.market_actions` row."""
    sell = np.zeros(spec.N_PRODUCTS, np.int32)
    buy = np.zeros(spec.N_PRODUCTS, np.int32)
    for order in market_row or ():
        if order[0] == "SELL":
            sell[spec.ITEM_IX[order[1]]] += int(order[2])
        elif order[0] == "BUY_PRODUCT":
            buy[spec.ITEM_IX[order[1]]] += int(order[2])
    return sell, buy


class RivalTell:
    """The rolling `plan.RIVAL_TELL_WINDOW`-turn read of the rival's sales.

    One instance per seat, held by `agent.runtime.Runtime`.  Each turn the seat
    calls `observe(step, inv, shops)` with the pot it is looking at -- which
    closes the PREVIOUS step, since the identity needs the next dawn's pot to
    price a turn -- and `record_orders(action["market"])` with the row it is
    about to present.  `batch()` is what the day plan reads.

    A gap in the stream (a seat that skips turns, a fresh game) drops the
    history rather than pricing a delta across it: the identity is only exact
    on consecutive steps.
    """

    def __init__(self, window=None):
        self.window = int(P.RIVAL_TELL_WINDOW if window is None else window)
        self.units = np.zeros((self.window, spec.N_PRODUCTS), np.int32)
        self.sold = np.zeros((self.window, spec.N_PRODUCTS), bool)
        self.n = 0
        self._prev = None      # (step, inv[9], shops[8], sell[9], buy[9])

    # ---- the stream -----------------------------------------------------
    def observe(self, step, inv, shops):
        inv = np.asarray(inv, np.int32).copy()
        shops = np.asarray(shops, np.int32).copy()
        if self._prev is not None:
            p_step, p_inv, p_shops, p_sell, p_buy = self._prev
            if p_step == step - 1:
                self._push(rival_net(inv, p_inv, p_step, p_shops, p_sell, p_buy))
            else:
                self.units[:] = 0
                self.sold[:] = False
                self.n = 0
        self._prev = (int(step), inv, shops,
                      np.zeros(spec.N_PRODUCTS, np.int32),
                      np.zeros(spec.N_PRODUCTS, np.int32))

    def record_orders(self, market_row):
        if self._prev is None:
            return
        sell, buy = order_units(market_row)
        self._prev = self._prev[:3] + (sell, buy)

    def _push(self, net):
        i = self.n % self.window
        self.units[i] = np.clip(net, 0, None)
        self.sold[i] = net >= 1
        self.n += 1

    # ---- what the plan reads --------------------------------------------
    def batch(self):
        """int[9]: measured units/turn per item, `NO_RATE` where it does not fire.

        The gate is `plan.RIVAL_TELL_MIN_TURNS` of the window's turns with a
        credited sale; WHEAT and FERTILIZER are never gated (`RIVAL_TELL_SKIP`)
        because they are the only two items the net loses units on.  Below a
        full window -- days 0-1, or after a gap -- every item keeps the proxy.
        The rate is the integer mean over the WHOLE window, floor-divided: a
        rival that sells 30 wool on one turn of six is offering 5 units a turn,
        not 30, and `sell_slot_scores` clamps it to `[BATCH_MIN, BATCH_MAX]`.
        """
        out = np.full(spec.N_PRODUCTS, NO_RATE, np.int32)
        if P.RIVAL_TELL_FORCE_PROXY or self.n < self.window:
            return out
        fires = self.sold.sum(axis=0) >= P.RIVAL_TELL_MIN_TURNS
        fires[list(P.RIVAL_TELL_SKIP)] = False
        rate = self.units.sum(axis=0) // self.window
        return np.where(fires, rate, NO_RATE).astype(np.int32)

    def burst(self):
        """int[9]: the rival's LARGEST single-turn sale of the window, 0 where none.

        The burst and not the rate [SWITCH, SELL_SLOT_RIVALRANK]: our slot
        index only decides who reaches the shared inventory first inside ONE
        turn's slot round, and a rival puts at most one turn's orders into that
        round, so the units that can get ahead of ours are the units of its
        biggest turn.  `docs/strategy/2026-09-16-rivaltell-arm.md` sect.5 is
        where this quantity is named, after the window MEAN died under the
        batch clamp's floor.

        The gate is `plan.SELL_SLOT_RIVALRANK_MIN_TURNS` turns of the window
        with a credited sale -- 1 by default, because a maximum needs no second
        sample to mean something -- and `RIVAL_TELL_SKIP` still holds: WHEAT
        and FERTILIZER are the two items the NET loses units on.  Below a full
        window, and after a gap, every item reads zero, which is the identity
        for `plan.sell_slot_rivalrank`.
        """
        out = np.zeros(spec.N_PRODUCTS, np.int32)
        if self.n < self.window:
            return out
        fires = self.sold.sum(axis=0) >= P.SELL_SLOT_RIVALRANK_MIN_TURNS
        fires[list(P.RIVAL_TELL_SKIP)] = False
        return np.where(fires, self.units.max(axis=0), 0).astype(np.int32)
