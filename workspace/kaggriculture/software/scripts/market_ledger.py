"""Precise market ledger: reimplements the engine's _process_market with
per-(player, op, item, price) logging so iteration decisions rest on exact
realized prices, not estimates. Dev-only tool (not part of the submission).
"""
import sys
sys.path.insert(0, ".")


def make_ledger_runner():
    import kaggle_environments.envs.kaggriculture.kaggriculture as K

    ledger = []

    def logged_process_market(state, env):
        obs0 = state[0].observation
        market = obs0.market
        farms = obs0.farms
        privates = [s.observation.private for s in state]
        board_size = int(K.get(env.configuration, "boardSize", 10))
        max_orders = max(1, int(K.get(env.configuration, "maxMarketOrdersPerTurn", 10)))
        hire_mult = int(K.get(env.configuration, "farmHandCostMult", K.FARM_HAND_COST_MULT))
        shed_capacity = int(K.get(env.configuration, "shedCapacity", 100))

        queues = []
        for s in state:
            action = s.action if isinstance(s.action, dict) else {}
            m = action.get("market", []) if isinstance(action, dict) else []
            q = list(m) if isinstance(m, list) else []
            queues.append(q[:max_orders])

        max_len = max((len(q) for q in queues), default=0)
        for i in range(max_len):
            order_states = []
            for player_id, q in enumerate(queues):
                ostate = None
                if i < len(q):
                    ostate = K._parse_order(q[i])
                order_states.append(ostate)

            for player_id, ostate in enumerate(order_states):
                if ostate is None:
                    continue
                op = ostate["type"]
                if op == "HIRE":
                    K._do_hire(farms[player_id], privates[player_id], board_size, hire_mult)
                    order_states[player_id] = None
                elif op == "BUY_LAND":
                    K._do_buy_land(farms[player_id], board_size)
                    order_states[player_id] = None

            idx_esc = 0
            while True:
                idx_esc += 1
                if idx_esc >= 100_000:
                    break
                quoted = [None, None]
                for player_id, ostate in enumerate(order_states):
                    if ostate is None or ostate["remaining"] <= 0:
                        continue
                    op = ostate["type"]
                    item = ostate["item"]
                    if op == "SELL" and item in K.PRODUCTS:
                        quoted[player_id] = ("SELL", item, K.market_price(item, market["inventory"][item], market.get("params")), ostate)
                    elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                        quoted[player_id] = ("BUY_PRODUCT", item, K.market_price(item, market["inventory"][item] - 1, market.get("params")), ostate)
                    elif op == "BUY_SEED" and item in K.CROPS:
                        quoted[player_id] = ("BUY_SEED", item, K.CROPS[item]["seed"], ostate)
                    elif op == "BUY_ANIMAL" and item in K.ANIMALS:
                        quoted[player_id] = ("BUY_ANIMAL", item, K.ANIMALS[item]["cost"], ostate)
                    else:
                        order_states[player_id] = None

                if all(q is None for q in quoted):
                    break
                committed_any = False
                for player_id, q in enumerate(quoted):
                    if q is None:
                        continue
                    op, item, price, ostate = q
                    ok = K._commit_unit(op, item, price, farms[player_id], privates[player_id], market, shed_capacity)
                    if ok:
                        ledger.append((K.get(obs0, "day", 0), player_id, op, item, price))
                        ostate["remaining"] -= 1
                        committed_any = True
                    else:
                        order_states[player_id] = None
                if not committed_any:
                    break
            K._refresh_prices(market)

    return logged_process_market, ledger


def summarize(ledger):
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0.0])
    for day, pid, op, item, price in ledger:
        k = (pid, op, item)
        agg[k][0] += 1
        agg[k][1] += price
    return agg
