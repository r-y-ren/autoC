# -*- coding: utf-8 -*-
# 反制对手（iterk K1 取材重建）：Wool Front-Runner 型
# 取材=orderbook_r45/evidence/counter_wool_front_runner.py（R22 make_counter_opponent
# 生成件）；重建差分（判决口径留档 evidence/judge_k1_realrun.json counter_rebuild）：
#   ①真毛供给：原件 SELL WOOL 48 无库存=幻影单引擎零效果（R22「反制件偏弱」根因）；
#     重建加自足羊毛农场（5 羊自建牧场、隔日 FEED+CARE、剪毛囤毛）使倒毛有真弹药；
#   ②倒毛量=min(dump_qty, 棚存 WOOL)（原件恒 48=无货空单）；
#   ③集毛阈值 dump_min（集中倒毛口径：囤到阈值才倒，不足则顺延候弹药）；
#   ④季末清仓 step>=714 全部 WOOL 变现（终局钱口径）。
# 核心语义（原件保持）：①嗅探对手羊 BUY_ANIMAL/剪毛 HARVEST 信号（动作流或
# 农格差分）②命中后提前 sniff_window(2) 回合集中倒毛 WOOL ③Anti-Shock：
# step<=1 不跟大单、吸收麦冲击（该拍不出市场单）。
_CFG = {'sniff_window': 2, 'dump_qty': 48, 'anti_shock': True,
        'n_sheep': 4, 'dump_min': 12, 'liquidate_step': 714}

# 牧场布局（board 10：NW 解锁；shed 通道格 (4,4) 出生位）：四牧场
# A(3,4) B(2,4) C(1,4) D(3,3)；日链 (4,4)→W A→W B→W C→E→E (3,4)→N D；
# 单元指令=裸方向（引擎 FARMER_MOVES 键）。
_CELLS = [(3, 4), (2, 4), (1, 4), (3, 3)]


def _make_agent():
    st = {"dump_at": None, "opp_animals": None, "opp_yield": None,
          "queue": None, "day": -1, "feed_day": False, "d0": None}

    def _get(obs, key, default=None):
        if isinstance(obs, dict):
            return obs.get(key, default)
        return getattr(obs, key, default)

    def _int(v, default=0):
        try:
            if isinstance(v, bool):
                return default
            return int(v)
        except Exception:
            return default

    def _sniff(obs):
        player = _int(_get(obs, "player", 0), 0)
        opp = 1 - player
        farms = _get(obs, "farms") or []
        farm = {}
        if isinstance(farms, (list, tuple)) and 0 <= opp < len(farms) \
                and isinstance(farms[opp], dict):
            farm = farms[opp]
        animals, yld = 0, 0
        for row in (farm.get("tiles") or []):
            if not isinstance(row, (list, tuple)):
                continue
            for tile in row:
                if isinstance(tile, dict) and tile.get("animal"):
                    animals += 1
                    yld += _int(tile.get("yield_units"), 0)
        act = _get(obs, "opponent_action")
        if not isinstance(act, dict):
            la = _get(obs, "last_actions")
            if isinstance(la, (list, tuple)) and 0 <= opp < len(la):
                act = la[opp]
        hit = False
        if isinstance(act, dict):
            for o in (act.get("market") or []):
                if isinstance(o, (list, tuple)) and len(o) >= 2 \
                        and o[0] == "BUY_ANIMAL":
                    hit = True
            for u in [act.get("farmer")] + list(act.get("hands") or []):
                if isinstance(u, (list, tuple)) and len(u) >= 1 \
                        and u[0] == "HARVEST":
                    hit = True
        if st["opp_animals"] is not None and animals > st["opp_animals"]:
            hit = True
        if st["opp_yield"] is not None and yld < st["opp_yield"]:
            hit = True
        st["opp_animals"], st["opp_yield"] = animals, yld
        return hit

    def _own(obs, player):
        farms = _get(obs, "farms") or []
        if isinstance(farms, (list, tuple)) and 0 <= player < len(farms) \
                and isinstance(farms[player], dict):
            return farms[player]
        return {}

    def _tile(farm, cell):
        tiles = farm.get("tiles") or []
        x, y = cell
        try:
            return tiles[y][x]
        except Exception:
            return None

    def _shed(obs):
        priv = _get(obs, "private") or {}
        shed = priv.get("shed") or {}
        return shed if isinstance(shed, dict) else {}

    def _tile_ops(farm, cell, feed_day):
        tile = _tile(farm, cell)
        ops = []
        if tile is None:
            ops.append(["BUILD_PASTURE"])
        elif isinstance(tile, str):
            ops.append(["DIG"])
            ops.append(["BUILD_PASTURE"])
        elif isinstance(tile, dict) and tile.get("animal") is None:
            if tile.get("kind") in ("PASTURE", "COOP"):
                ops.append(["PLACE", "SHEEP"])
            else:
                ops.append(["DIG"])
                ops.append(["BUILD_PASTURE"])
        if isinstance(tile, dict) and tile.get("animal"):
            if _int(tile.get("yield_units"), 0) > 0:
                ops.append(["HARVEST"])
            if feed_day:
                if not tile.get("fed_today"):
                    ops.append(["FEED"])
                if not tile.get("cared_today"):
                    ops.append(["CARE"])
        return ops

    def _day_plan(obs, player, day, feed_day):
        """当日单元指令队列（步 0 起逐拍执行；≥24 截断）。"""
        farm = _own(obs, player)
        ops = []
        if feed_day:
            ops.append(["PICKUP", "WHEAT", _CFG["n_sheep"]])
        # 走位链：(4,4) →W→ A(3,4) →W→ B(2,4) →W→ C(1,4) →E→ (2,4) →E→ (3,4)
        # →N→ D(3,3) →W→ E(2,3)
        chain = [("WEST", 0), ("WEST", 1), ("WEST", 2), ("EAST", None),
                 ("EAST", None), ("NORTH", 3)]
        for mv, idx in chain:
            ops.append([mv])
            if idx is not None:
                ops.extend(_tile_ops(farm, _CELLS[idx], feed_day))
        while len(ops) < 24:
            ops.append(["PASS"])
        return ops[:24]

    def agent(obs):
        try:
            raw_step = _get(obs, "step")
            if raw_step is None:
                step = _int(_get(obs, "day"), 0) * 24 \
                    + _int(_get(obs, "hour"), 0)
            else:
                step = _int(raw_step, None)
                if step is None:
                    return {"farmer": ["PASS"], "hands": [], "market": []}
            day = step // 24
            player = _int(_get(obs, "player", 0), 0)
            action = {"farmer": ["PASS"], "hands": [], "market": []}

            # ---- 嗅探（原件语义）----
            if _sniff(obs) and st["dump_at"] is None:
                lead = 1 if _CFG["sniff_window"] <= 1 else 2
                st["dump_at"] = step + lead

            # ---- 农场日编排（隔日 FEED+CARE；剪毛囤毛）----
            if day != st["day"]:
                st["day"] = day
                st["feed_day"] = (day % 2 == 1)
                st["queue"] = _day_plan(obs, player, day, st["feed_day"]) \
                    if day >= 1 else None
            if day == 0:
                queue = st["d0"]
                if queue is None:
                    queue = [
                        ["WEST"], ["BUILD_PASTURE"],
                        ["WEST"], ["BUILD_PASTURE"],
                        ["WEST"], ["BUILD_PASTURE"],
                        ["EAST"], ["EAST"], ["EAST"],
                        ["PICKUP", "SHEEP", _CFG["n_sheep"]],
                        ["WEST"], ["PLACE", "SHEEP"],
                        ["WEST"], ["PLACE", "SHEEP"],
                        ["WEST"], ["PLACE", "SHEEP"],
                        ["EAST"], ["EAST"], ["NORTH"],
                        ["BUILD_PASTURE"], ["PLACE", "SHEEP"],
                        ["PASS"], ["PASS"], ["PASS"], ["PASS"],
                    ]
                    st["d0"] = queue
            else:
                queue = st.get("queue")
            idx = step - day * 24
            if isinstance(queue, list) and 0 <= idx < len(queue):
                action["farmer"] = list(queue[idx])

            # ---- Anti-Shock（原件语义）：step<=1 不出市场单 ----
            if _CFG["anti_shock"] and step <= 1:
                action["market"] = []
                return action

            market = []
            shed = _shed(obs)
            wool = _int(shed.get("WOOL"), 0)

            # ---- 开局买羊（step2 起；Anti-Shock 之后）----
            if day == 0 and step == 2:
                market.append(["BUY_ANIMAL", "SHEEP", _CFG["n_sheep"]])
            # ---- 隔日饲料采购（偶数日末为次日 FEED 备料）----
            if day >= 0 and step % 24 == 23 and day % 2 == 0 and step < 714:
                market.append(["BUY_PRODUCT", "WHEAT", _CFG["n_sheep"]])
            # ---- 季末清仓 ----
            if step >= _CFG["liquidate_step"] and wool > 0:
                market.append(["SELL", "WOOL", wool])
            # ---- 集中倒毛（原件语义 + 集毛阈值）----
            elif st["dump_at"] is not None and step >= st["dump_at"]:
                if wool >= _CFG["dump_min"]:
                    market.append(["SELL", "WOOL", min(_CFG["dump_qty"], wool)])
                    st["dump_at"] = None
                else:
                    st["dump_at"] = step + 2    # 顺延候弹药（集中倒毛口径）
            action["market"] = market
            return action
        except Exception:
            return {"farmer": ["PASS"], "hands": [], "market": []}
    return agent


agent = _make_agent()
