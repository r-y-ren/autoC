"""SIMGAP1: the fast sim reproduces our ENGINE seat.

1. `sim.market` resolves a SELL/BUY_PRODUCT cross at the $1 floor exactly as the
   engine's per-unit lockstep (`kaggriculture._process_market` + `_commit_unit`).
2. (slow, `KAGG3_SIMGAP_SLOW=1`) LIVE250 dev board 0 vs the reacting V56 notebook,
   head_940 + RESIDUAL_RIVAL_PURSE_ON, our seat with the runtime layer
   (`S/simgap1/ourseat.py` "guard" mode): both purses == the engine's 75,828 / 74,681.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, "src")
os.environ.setdefault("JAX_PLATFORMS", "cpu")

from kagg3 import spec  # noqa: E402
from kagg3.core import ops as O  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def _engine_lockstep(item, inv, seller_units, buyer_units, buyer_money, seller_seat):
    from kaggle_environments.envs.kaggriculture import kaggriculture as K
    money = [0, 0]
    money[1 - seller_seat] = buyer_money
    left = {seller_seat: seller_units, 1 - seller_seat: buyer_units}
    alive = {0: True, 1: True}
    while any(alive[p] and left[p] > 0 for p in (0, 1)):
        q = {}
        for p in (0, 1):
            if alive[p] and left[p] > 0:
                q[p] = K.market_price(item, inv) if p == seller_seat else K.market_price(item, inv - 1)
        for p in (0, 1):
            if p not in q:
                continue
            if p == seller_seat:
                money[p] += q[p]
                inv += 1 if q[p] > 1 else 0
            else:
                if money[p] < q[p]:
                    alive[p] = False
                    continue
                money[p] -= q[p]
                inv -= 1
            left[p] -= 1
    return money, inv


@pytest.mark.parametrize("seller_seat", [0, 1])
@pytest.mark.parametrize("inv_off,sell,buy,cash", [(0, 17, 2, 500), (3, 5, 9, 500), (0, 4, 30, 7), (-2, 20, 3, 500)])
def test_floor_cross_matches_engine_lockstep(seller_seat, inv_off, sell, buy, cash):
    import jax.numpy as jnp
    from kaggle_environments.envs.kaggriculture import kaggriculture as K
    from kagg3.sim import market
    from kagg3.sim.state import build_tables, initial_state
    tables = build_tables(jnp)
    item = spec.PRODUCTS.index("FERTILIZER")
    inv = 10000
    while K.market_price("FERTILIZER", inv) > 1:     # first floor inventory
        inv += 1
    inv += inv_off
    st = initial_state(jnp, None, None)
    b = 1 - seller_seat
    st = st._replace(money=st.money.at[seller_seat].set(0).at[b].set(cash),
                     shed=st.shed.at[:].set(0).at[seller_seat, item].set(sell),
                     mkt_inv=st.mkt_inv.at[item].set(inv))
    op = np.zeros(2, np.int32)
    op[seller_seat], op[b] = O.MO_SELL, O.MO_BUY_PRODUCT
    n = np.zeros(2, np.int32)
    n[seller_seat], n[b] = sell, buy
    out = market.process_slot(tables, st, jnp.asarray(op), jnp.asarray([item, item], jnp.int32), jnp.asarray(n))
    money, inv_e = _engine_lockstep("FERTILIZER", inv, sell, buy, cash, seller_seat)
    assert [int(x) for x in out.money] == money
    assert int(out.mkt_inv[item]) == inv_e


@pytest.mark.skipif(not os.environ.get("KAGG3_SIMGAP_SLOW"), reason="slow: ~3 min (compile + one V56 game)")
def test_board0_guard_mode_equals_engine():
    env = dict(os.environ, KAGG3_PPO_SW_EXTRA="RESIDUAL_RIVAL_PURSE_ON=True", JAX_PLATFORMS="cpu")
    out = subprocess.run([sys.executable, str(ROOT / "S/simgap1/fid.py"), "guard", "0", "1"],
                         capture_output=True, text=True, env=env, timeout=1200).stdout
    line = next(l for l in out.splitlines() if l.startswith("board 0 "))
    assert "sim 75828/74681 eng 75828/74681" in line, line
