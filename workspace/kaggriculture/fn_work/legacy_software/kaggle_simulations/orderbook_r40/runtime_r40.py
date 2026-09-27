# -*- coding: utf-8 -*-
"""R23 运行时三件（注入包内）。

责任契约：_route40_select（step144 续段选择）/apply_race_slots（同回合
卖单竞速）/apply_slot_hygiene（队列补洞）。本文件源文本由 inject_r40_block
追加进包内（含内嵌续段库）。
"""
from __future__ import annotations

from typing import Any, Dict


def _route40_select(observation: Dict[str, Any], library: Any = None) -> Dict[str, Any]:
    """step144 续段选择：按当局开局长相族（前 144 步宏观指纹）查库选路线
    续段；无族命中→回退现行 _router 店对逻辑；只读选择不改磁带主体。

    签名意图：输入: observation+库 / 输出: {route, family, confidence} /
    错误: 库缺→回退默认路由。

    口径留档（与 route_library.build_route_library 两件共同约定）：
    - 族键="<hires>|<land_buys>|<tiles_by_crop>|<首二店>"：hires/land_buys=
      前 144 步（步标 0..143）farms[player].hands/unlocked_quadrants 计数正增量
      累计；tiles_by_crop=step144 当拍 crop 非空地块数（count 降序、作物名升序）
      渲染 "CROP:n,..."（空="NONE"）；首二店=step144 当拍 town.unlocked_shops[:2]
      以 "+" 连接（空="NONE"）。步标=observation["step"] 或 day*24+hour。
    - 触发：首拍 step>=144（正常即 step==144）按族键查库，命中且族有胜局
      best_route→{route: route_id, family: 族键, confidence: 族 win_rate}；
      结果跨步锁定（latched），step==0 或步标回退=新局复位。
    - 回退信号：route=None 表示回退现行 `_router` 店对逻辑（无族命中/族无胜局
      best_route/库缺/异常一律 {route: None, family: None 或族键, confidence: 0.0}；
      异常不锁定，后续好拍可重触发）。confidence=置信度（命中=族 win_rate）。
    """
    import json

    def _jl(x):
        return json.loads(x) if isinstance(x, str) else x

    def _label(obs):
        raw = obs.get("step")
        if raw is not None:
            return int(raw)
        return int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))

    fallback = {"route": None, "family": None, "confidence": 0.0}
    try:
        step = _label(observation)
        st = getattr(_route40_select, "_fp_state", None)
        if st is None or step == 0 or step < st.get("last_step", -1):
            st = {"hires": 0, "land": 0, "hands_prev": None, "uq_prev": None,
                  "latched": None, "last_step": -1}
            _route40_select._fp_state = st
        st["last_step"] = step
        if st["latched"] is not None:
            return dict(st["latched"])
        farms = _jl(observation.get("farms"))
        if not isinstance(farms, list) or len(farms) != 2:
            raise ValueError("farms 形态非法")
        farm = farms[int(observation.get("player", 0))]
        hands = len(_jl(farm.get("hands")) or [])
        uq = len(_jl(farm.get("unlocked_quadrants")) or [])
        if step < 144:
            if st["hands_prev"] is not None:
                if hands > st["hands_prev"]:
                    st["hires"] += hands - st["hands_prev"]
                if uq > st["uq_prev"]:
                    st["land"] += uq - st["uq_prev"]
            st["hands_prev"], st["uq_prev"] = hands, uq
            return dict(fallback)
        crops = {}
        for row in (_jl(farm.get("tiles")) or []):
            if not isinstance(row, list):
                continue
            for cell in row:
                if isinstance(cell, dict) and cell.get("crop"):
                    c = str(cell["crop"])
                    crops[c] = crops.get(c, 0) + 1
        tiles_str = ",".join(
            "%s:%d" % (c, n) for c, n in
            sorted(crops.items(), key=lambda kv: (-kv[1], kv[0]))) or "NONE"
        shops = list(_jl((observation.get("town") or {}))
                     .get("unlocked_shops") or [])[:2]
        shops_str = "+".join(str(s) for s in shops) or "NONE"
        key = "%d|%d|%s|%s" % (st["hires"], st["land"], tiles_str, shops_str)
        lib = library
        if isinstance(lib, str):
            lib = json.loads(lib)
        if isinstance(lib, dict) and "families" not in lib and \
                isinstance(lib.get("library"), dict):
            lib = lib["library"]
        fam = (lib.get("families") or {}).get(key) if isinstance(lib, dict) else None
        if isinstance(fam, dict) and fam.get("best_route") is not None:
            out = {"route": fam["best_route"], "family": key,
                   "confidence": float(fam.get("win_rate", 0.0))}
        elif isinstance(fam, dict):
            out = {"route": None, "family": key, "confidence": 0.0}
        else:
            out = dict(fallback)
        st["latched"] = out
        return dict(out)
    except Exception:
        return dict(fallback)


def apply_race_slots(observation: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """同回合卖单竞速：我方 SELL 单前移至市场表前部槽（对手挂单前成交；
    沿空槽位次语义+V57 资金序不变量）；只动 SELL 槽序。

    签名意图：输入: observation, action / 输出: 调整后 action /
    错误: 异常→原动作。
    """
    raise NotImplementedError("unimplemented:fn:apply_race_slots")


def apply_slot_hygiene(observation: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """队列补洞：识别零执行占坑单（上一拍挂出未成交）→清坑+后位有效单前移
    补洞（空槽位次语义不破坏）；只动自家市场单。

    签名意图：输入: observation, action / 输出: 调整后 action+补洞账 /
    错误: 异常→原动作。
    """
    raise NotImplementedError("unimplemented:fn:apply_slot_hygiene")
