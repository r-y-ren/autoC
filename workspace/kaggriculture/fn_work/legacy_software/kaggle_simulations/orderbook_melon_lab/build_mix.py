# -*- coding: utf-8 -*-
"""build_mix（melon lab）：组合臂混装形 C_final+果品件（薄补丁形态；新建 lab）。

混装式（组合臂，同面干扰/重复基座口径双记）：
  mix = c_final 完全体（sha a37c0d34…，内含共享底盘 sell_lead/_v44y_reorder/
        step720-725 尾部重排再应用/V219 番茄层——果品件与其内生面存在重叠）
      + 果品件①前跑卖引：FRONT_RUN_ITEMS（MILK/WOOL/STRAWBERRY/MELON）四品
        next-step 预卖 + 次步扣减（prvsiyan _sell_lead/_front_run/_apply_suppression
        概念移植，Apache-2.0，prvsiyan/doanthuan 谱系署名随包；mooman 件未用）
      + 果品件②终局块重排：step712-718 窗口 SELL 连续块重排末尾再应用
        （prvsiyan FRO 尾部再应用模式；复用基座内生 _v44y_reorder，零再实现）。
果品产线权重（MELON/TOMATO 倾斜）系 S_melon 自有 tape 计划面，不入混装
（跨计划宇宙移植需重写磁带计划，超出薄补丁口径）——见 manifest。

入口归一沿 m13fix/c_final 先例（末函数=_hs_agent 重绑）。产物
orderbook_melon_lab/build/mix/。只写本 lab；不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
CFINAL_MAIN = (KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py")
OUT_DIR = MODULE_DIR / "build" / "mix"
EVID_DIR = MODULE_DIR / "evidence"
CFINAL_SHA = "a37c0d3487fe1d2152ec6c0b767b36afc21ad18207accb2d3cf1f1b077016a92"

TAIL = r'''

# ==== S4 果品件混装层（orderbook_melon_lab：C_final + 果品件） ====
# 果品件①前跑卖引：FRONT_RUN_ITEMS 四品 next-step 预卖 + 次步扣减。
#   概念移植自 prvsiyan_melons（Apache-2.0）Chassis._sell_lead/_front_run/
#   _apply_suppression（prvsiyan/doanthuan 谱系；上游通知见该件头部）。
#   范围收窄到四品（FRONT_RUN_ITEMS），窗沿 prvsiyan sell_lead 条件
#   （step%4!=0、次步<=718、次步%72!=0）。
# 果品件②终局块重排：step712-718 窗口 SELL 连续块内重排末尾再应用。
#   概念移植自 prvsiyan FRO 尾部模式（"Reapply the inherited _v44y_reorder
#   AFTER later wrappers"）；重排核复用基座内生 _v44y_reorder（零再实现，
#   教训定理：基座内生机制不外层重写）。
# 只置换既有连续 SELL 块内槽位；数量/物理动作/固定价单/BUY 单不动。
_MELON_PARENT = _hs_agent
_MELON_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
_MELON_MIN_PRICE = 2
_MELON_LAST = 718
_MELON_STATE = {}
_MELON_REPORT = dict(calls=0, ps_turns=0, ps_units=0, sup_turns=0, sup_units=0,
                     ro_turns=0, ro_gain=0.0, errors=0)


def _melon_planned(obs, step):
    """自家 tape 次步计划 SELL（四品口径；prvsiyan sell_lead 前瞻语义）。"""
    try:
        player = int(_get(obs, "player", 0))
        chassis = _IMPL.chassis
        st = (chassis.players or {}).get(player) or {}
        route = st.get("route")
        if route not in chassis.routes:
            return {}
        tape = chassis.routes[route]
        nxt = step + 1
        if not (0 <= nxt < len(tape)) or not isinstance(tape[nxt], dict):
            return {}
        planned = {}
        for o in (tape[nxt].get("market") or []):
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in _MELON_ITEMS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        return planned
    except Exception:
        return {}


def _melon_suppress(action, state, step):
    """次步扣减：把一步前预卖的量从本步 SELL 里扣掉（prvsiyan _apply_suppression）。"""
    if state.get("due") != step:
        return action, 0
    remaining = dict(state.get("debt", {}))
    kept = []
    trimmed = 0
    for order in action.get("market") or []:
        order = list(order)
        if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
            removed = min(max(0, _int(order[2])), remaining[order[1]])
            order[2] = _int(order[2]) - removed
            remaining[order[1]] -= removed
            trimmed += removed
        kept.append(order)
    state["debt"] = {k: v for k, v in remaining.items() if v > 0}
    if trimmed:
        action = dict(action)
        action["market"] = kept
    return action, trimmed


def _melon_presell(obs, action, step, state):
    """FRONT_RUN_ITEMS 四品 next-step 预卖（prvsiyan sell_lead 条件逐条沿用）。"""
    nxt = step + 1
    if nxt > _MELON_LAST or nxt % 72 == 0 or step % 4 == 0:
        return action
    planned = _melon_planned(obs, step)
    if not planned:
        return action
    market = [list(o) for o in (action.get("market") or [])]
    already = {o[1] for o in market if o and o[0] == "SELL" and len(o) > 1}
    try:
        view = FarmView(obs)
        projected = dict(projected_shed(action, view))
        prices = (_get(obs, "market", {}) or {}).get("prices") or {}
        added = 0
        for item in _MELON_ITEMS:
            if planned.get(item, 0) <= 0 or item in already:
                continue
            if _int(prices.get(item, 0)) < _MELON_MIN_PRICE:
                continue
            qty = min(_int(projected.get(item, 0)), _int(planned[item]))
            if qty <= 0:
                continue
            if len(market) >= 10:
                break
            market.append(["SELL", item, qty])
            projected[item] = projected.get(item, 0) - qty
            already.add(item)
            state["debt"][item] = state["debt"].get(item, 0) + qty
            state["due"] = nxt
            added += 1
            _MELON_REPORT["ps_units"] += qty
        if added:
            _MELON_REPORT["ps_turns"] += 1
            action = dict(action)
            action["market"] = market
    except Exception:
        _MELON_REPORT["errors"] += 1
    return action


def _melon_mix_agent(observation, configuration=None):
    action = _MELON_PARENT(observation, configuration)
    try:
        step = int(_get(observation, "step", 0))
        player = int(_get(observation, "player", 0))
        if step == 0:
            _MELON_STATE.clear()
            for k in _MELON_REPORT:
                _MELON_REPORT[k] = 0
        _MELON_REPORT["calls"] += 1
        state = _MELON_STATE.setdefault(player, {"debt": {}, "due": -1})
        action, trimmed = _melon_suppress(action, state, step)
        if trimmed:
            _MELON_REPORT["sup_turns"] += 1
            _MELON_REPORT["sup_units"] += trimmed
        action = _melon_presell(observation, action, step, state)
        if 712 <= step <= 718:
            revised = _v44y_reorder(observation, action)
            if revised is not None and revised != action:
                _MELON_REPORT["ro_turns"] += 1
                action = revised
                st = _RACE_STATE.get(player)
                if st is not None and st.get("prev_action") is not None and st.get("step") == step:
                    st["prev_action"] = action
    except Exception:
        _MELON_REPORT["errors"] += 1
    return action
_melon_mix_agent.telemetry = _MELON_REPORT

# ---- 入口归一（末函数=_hs_agent；m13fix/c_final 尾块先例逐字沿用） ----
_MELON_ENTRY_TMP = _melon_mix_agent
del _melon_mix_agent
del _hs_agent
_hs_agent = _MELON_ENTRY_TMP
del _MELON_ENTRY_TMP
'''


def main() -> None:
    raw = CFINAL_MAIN.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != CFINAL_SHA:
        raise SystemExit("c_final sha mismatch: %s" % sha)
    out = raw.decode("utf-8") + TAIL
    out_bytes = out.encode("utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "main.py").write_bytes(out_bytes)
    manifest = {
        "schema": "orderbook_melon_manifest/1.0",
        "arm": "mix",
        "form": "混装形 C_final+果品件（薄补丁尾块）",
        "base": str(CFINAL_MAIN),
        "base_sha256": sha,
        "out": str(OUT_DIR / "main.py"),
        "out_sha256": hashlib.sha256(out_bytes).hexdigest(),
        "out_bytes": len(out_bytes),
        "entry": "_hs_agent（尾块重绑末函数，m13fix 先例）",
        "fruit_pieces": {
            "A_前跑卖引": "FRONT_RUN_ITEMS 四品 next-step 预卖+次步扣减（prvsiyan sell_lead/front_run 概念移植，Apache-2.0）",
            "B_终局块重排": "step712-718 窗口 _v44y_reorder 末尾再应用（prvsiyan FRO 模式；核复用基座内生件零再实现）",
        },
        "not_grafted": "果品产线权重（MELON/TOMATO 倾斜）=S_melon 自有 tape 计划面，跨计划宇宙移植需重写磁带计划，超出薄补丁口径",
        "overlap_audit": {
            "inner_sell_lead": "c_final 内生 Chassis._sell_lead（_SETTINGS sell_lead=True；_r36 门控在 0-287/696-718 窗生效）——果品件①同面不同窗不同品域，重复基座风险",
            "inner_reorder": "c_final 内生 _v44y_reorder + step720/722/724/725 尾部再应用（step>=216）——果品件②与其窗重叠，纯增量=712-718 一次追加半步",
            "inner_v219": "c_final 内生 V219 番茄层（果品件与之同源上游）",
            "theorem": "外挂层重复基座内生机制=同型失败（分析35 教训定理）+同面优化不可堆叠只能统一（分析43/44）——混装形为定理检验臂",
        },
        "mooman_cleanroom": "mooman 件无许可，未移植未引用",
    }
    (EVID_DIR / "mix_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("mix built:", manifest["out_sha256"][:16], manifest["out_bytes"], "bytes")


if __name__ == "__main__":
    main()
