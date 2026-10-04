# -*- coding: utf-8 -*-
# 反制对手（R22 make_counter_opponent 生成）：Wool Front-Runner 型
# ①嗅探对手羊 BUY_ANIMAL/剪毛 HARVEST 信号（动作流或农格差分）
# ②命中后提前 sniff_window(1-2) 回合集中倒毛 WOOL
# ③Anti-Shock：step-1 不跟大单、吸收麦冲击
_CFG = {'sniff_window': 2, 'dump_qty': 48, 'anti_shock': True}


def _make_agent():
    st = {"dump_at": None, "opp_animals": None, "opp_yield": None}

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
            action = {"farmer": ["PASS"], "hands": [], "market": []}
            if _sniff(obs) and st["dump_at"] is None:
                lead = 1 if _CFG["sniff_window"] <= 1 else 2
                st["dump_at"] = step + lead
            # Anti-Shock：step-1 不跟大单、吸收麦冲击（该拍不出市场单）
            if _CFG["anti_shock"] and step <= 1:
                return action
            if st["dump_at"] is not None and step >= st["dump_at"]:
                action["market"] = [["SELL", "WOOL", _CFG["dump_qty"]]]
                st["dump_at"] = None
            return action
        except Exception:
            return {"farmer": ["PASS"], "hands": [], "market": []}
    return agent


agent = _make_agent()
