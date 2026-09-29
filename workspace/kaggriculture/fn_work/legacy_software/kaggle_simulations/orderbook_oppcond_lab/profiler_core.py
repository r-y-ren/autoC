# -*- coding: utf-8 -*-
"""profiler_core：对手画像器单源分类器（内嵌件与离线重放同源字节）。

责任口径（任务 opp-conditional A1）：开局窗（step≤144）公开信号分类对手。
CORE_SRC=唯一分类器源：build_oppcond.py 将其**原文字节**织入各形态尾块
（内嵌件）；judge_oppcond.py 经 exec(CORE_SRC) 离线重放同一字节 → 在局分类
与离线判读逐字节同源（画像准确率口径无实现漂移）。

指纹件（公开信号）：money 轨迹/step1 现金差（EXP288 镜像口径）、step2
(rival money, market WHEAT) 指纹（CT_TABLE 形）、_r37_similarity 农场指纹、
rival_sold 卖流签名（v9 库存差分口径）、对手农场羊格数。

分类（顺序判决，保守未知兜底）——阈值冻结于 calib_fingerprints.json
（36 局 = 6 件 × 3 seeds × 双席；100% 席对称 + seed 不变）：
  1) step1 现金差<0.5 ∧ sim_max≥0.95        → h1_mirror（H1/tetsutani 型）
  2) 对手 step1 资金≥2999.5 ∧ sim_max≤0.5 ∧ step143 对手羊格≥3
                                            → wfr（WFR-攻击型）
  3) 4.0≤step1 现金差≤12.0 ∧ sim_max≥0.95   → r37_2965_family（r37/2965 系谱型）
  4) 其余                                   → unknown（未知；保守）

关键实证（calib + 静态磁带核对）：r37/2965a/2965b/r40 开局窗逐拍公开信号
全同——route0[:144] 动作哈希 b518f3763802 四件一致、逐拍 money 轨迹相等、
sim/农场指纹相同 → **窗口内系谱级不可分**，类合并为 r37_2965_family（C1 对
r37/2965 同动=动作等价；C2 视界按 r37 标定、逐面 Δ 判决）。
只写 orderbook_oppcond_lab/。
"""
from __future__ import annotations

import json

RECORD_VERSION = "oppcond-profiler-core/1.0"

CORE_SRC = r'''
# ===== opp-profile core v1（单源分类器；内嵌件与离线重放同源字节） =====
_OC_CLASSES = ("r37_2965_family", "h1_mirror", "wfr", "unknown")
_OC_SIM_STEPS = (24, 48, 72, 96, 120, 143)
_OC_LOCK_STEP = 144
_OC_RACE_ITEMS = ("CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")
_OC_SHOP_ITEMS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def _oc_sim(obs):
    """_r37_similarity 同式：公开农格指纹匹配率（≥8 占用格才有效）。"""
    try:
        farms = obs.get("farms") or []
        player = int(obs.get("player", 0))
        if len(farms) < 2:
            return 0.0
        own, rival = farms[player], farms[1 - player]
        if (own.get("unlocked_quadrants") != rival.get("unlocked_quadrants")):
            return 0.0
        matches = total = 0
        for a, b in zip([t for row in (own.get("tiles") or []) for t in row],
                        [t for row in (rival.get("tiles") or []) for t in row]):
            sa = ((a.get("crop"), a.get("animal")) if isinstance(a, dict)
                  else (None, None))
            sb = ((b.get("crop"), b.get("animal")) if isinstance(b, dict)
                  else (None, None))
            if sa != (None, None) or sb != (None, None):
                total += 1
                matches += sa == sb
        return matches / total if total >= 8 else 0.0
    except Exception:
        return 0.0


def _oc_rival_animals(obs):
    """对手农场动物格计数（公开）。"""
    out = {}
    try:
        farms = obs.get("farms") or []
        player = int(obs.get("player", 0))
        if len(farms) < 2:
            return out
        farm = farms[1 - player]
        for row in (farm.get("tiles") or []):
            for tile in row:
                if isinstance(tile, dict) and tile.get("animal"):
                    a = str(tile.get("animal"))
                    out[a] = out.get(a, 0) + 1
    except Exception:
        pass
    return out


def _oc_town_draw(shops, step):
    """v9 同式：town/shop 每拍抽取量（卖流签名恢复用）。"""
    draw = dict.fromkeys(_OC_RACE_ITEMS, 0)
    try:
        if step % 4 == 0:
            for shop in shops:
                items = _OC_SHOP_ITEMS.get(shop, ())
                for item in items:
                    if item in draw:
                        draw[item] += 2 if len(items) == 1 else 1
        if step % 24 == 0:
            for item in draw:
                draw[item] += 1
    except Exception:
        pass
    return draw


def _oc_own_sells(act):
    out = {}
    try:
        for o in (act.get("market") or []):
            if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL":
                out[str(o[1])] = out.get(str(o[1]), 0) + int(o[2])
    except Exception:
        pass
    return out


def _oc_state_new():
    return {
        "last_step": -1, "cashdiff1": None, "rival_money1": None,
        "rival_money2": None, "rkey2": None, "sim_max": 0.0,
        "sim_seen": 0, "rival_animals_143": None, "rival_sold_cum": {},
        "own_sold_cum": {}, "prev_inv": None, "prev_step": None,
        "cls": None, "locked": False, "why": None,
    }


def _oc_update(st, obs, act):
    """逐拍吸收公开信号（窗口 step≤143；act=我席动作，仅用于卖流恢复）。"""
    try:
        step = int(obs.get("step", 0))
    except Exception:
        return st
    if step <= st.get("last_step", -1):
        return st
    st["last_step"] = step
    if step > 143:
        return st
    try:
        player = int(obs.get("player", 0))
        farms = obs.get("farms") or []
        if len(farms) < 2:
            return st
        own_m = float(farms[player].get("money", 0.0))
        riv_m = float(farms[1 - player].get("money", 0.0))
        if step == 1:
            st["cashdiff1"] = abs(riv_m - own_m)
            st["rival_money1"] = riv_m
        if step == 2:
            st["rival_money2"] = riv_m
            inv2 = ((obs.get("market") or {})
                    if isinstance(obs.get("market"), dict)
                    else {}).get("inventory") or {}
            try:
                st["rkey2"] = [round(riv_m, 3), int(inv2.get("WHEAT", 0))]
            except Exception:
                st["rkey2"] = None
        if step in _OC_SIM_STEPS:
            s = _oc_sim(obs)
            st["sim_seen"] = st.get("sim_seen", 0) + 1
            if s > st["sim_max"]:
                st["sim_max"] = s
        if step == 143:
            an = _oc_rival_animals(obs)
            st["rival_animals_143"] = an
        inv = ((obs.get("market") or {})
               if isinstance(obs.get("market"), dict)
               else {}).get("inventory") or {}
        if st.get("prev_inv") is not None and st.get("prev_step") == step - 1:
            shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
            draw = _oc_town_draw(shops, step - 1)
            osold = _oc_own_sells(act)
            for item in _OC_RACE_ITEMS:
                try:
                    sold = (int(inv.get(item, 0)) - int(st["prev_inv"].get(item, 0))
                            + draw.get(item, 0) - osold.get(item, 0))
                except Exception:
                    continue
                if sold > 0:
                    st["rival_sold_cum"][item] = \
                        st["rival_sold_cum"].get(item, 0) + int(sold)
            for item, n in osold.items():
                st["own_sold_cum"][item] = st["own_sold_cum"].get(item, 0) + n
        st["prev_inv"] = dict(inv)
        st["prev_step"] = step
    except Exception:
        pass
    return st


def _oc_decide(st):
    """纯判决：特征→类（顺序门；不确定→unknown 保守）。"""
    try:
        cd = st.get("cashdiff1")
        sm = float(st.get("sim_max") or 0.0)
        rm1 = st.get("rival_money1")
        an = st.get("rival_animals_143") or {}
        sheep = 0
        for k, v in an.items():
            if "SHEEP" in str(k):
                sheep += int(v)
        if cd is None or rm1 is None or st.get("sim_seen", 0) < 1:
            return "unknown", "window incomplete (cashdiff1/rival_money1/sim 未齐)"
        if cd < 0.5 and sm >= 0.95:
            return "h1_mirror", ("EXP288 镜像门: step1 现金差 %.3f<0.5 且 "
                                 "sim_max %.3f>=0.95" % (cd, sm))
        if rm1 >= 2999.5 and sm <= 0.5 and sheep >= 3:
            return "wfr", ("零开局交易+农场指纹: rival money@1 %.1f>=2999.5, "
                           "sim_max %.3f<=0.5, 对手羊格 %d>=3" % (rm1, sm, sheep))
        if 4.0 <= cd <= 12.0 and sm >= 0.95:
            return "r37_2965_family", ("系谱窗指纹: step1 现金差 %.3f∈[4,12] 且 "
                                       "sim_max %.3f>=0.95（r37/2965/r40 窗口内"
                                       "逐拍公开信号全同，系谱级）" % (cd, sm))
        return "unknown", ("保守未知: cashdiff1=%s sim_max=%.3f rival_money1=%s "
                           "sheep=%d" % (cd, sm, rm1, sheep))
    except Exception as exc:
        return "unknown", "decide error: %r" % (exc,)


def _oc_lock_if_due(st, step):
    """step≥144 且未锁 → 用窗内数据定类（锁后永不变）。"""
    try:
        if not st.get("locked") and int(step) >= _OC_LOCK_STEP:
            cls, why = _oc_decide(st)
            st["cls"] = cls
            st["why"] = why
            st["locked"] = True
    except Exception:
        st["cls"] = "unknown"
        st["why"] = "lock error"
        st["locked"] = True
    return st
'''

# ---------------------------------------------------- 单源装载（离线侧） --
_NS: dict = {}
exec(compile(CORE_SRC, "<opp-profile-core>", "exec"), _NS)
_oc_sim = _NS["_oc_sim"]
_oc_state_new = _NS["_oc_state_new"]
_oc_update = _NS["_oc_update"]
_oc_decide = _NS["_oc_decide"]
_oc_lock_if_due = _NS["_oc_lock_if_due"]
OC_CLASSES = _NS["_OC_CLASSES"]


def replay_class(sink, lock_step: int = 144):
    """离线重放：追踪槽 [(step, obs, act)]（我席）→ (cls, why, state)。

    与内嵌件同源字节（CORE_SRC）；入局分类=同函数逐拍同序喂入。
    """
    st = _oc_state_new()
    for entry in (sink or []):
        try:
            step = int(entry[0])
            obs = entry[1]
            act = entry[2]
        except Exception:
            continue
        if not isinstance(obs, dict):
            continue
        if step > 143:
            break
        _oc_update(st, obs, act)
    _oc_lock_if_due(st, lock_step)
    return st.get("cls"), st.get("why"), st


def classify_features(cashdiff1, rival_money1, sim_max, sheep143, sim_seen=1):
    """合成特征直判（构建探针/网格核对用）。"""
    st = _oc_state_new()
    st["cashdiff1"] = cashdiff1
    st["rival_money1"] = rival_money1
    st["sim_max"] = sim_max
    st["sim_seen"] = sim_seen
    st["rival_animals_143"] = {"SHEEP": sheep143}
    return _oc_decide(st)


def probe_expected():
    """阈值冻结核对表（calib 实测特征 → 期望类）。"""
    rows = [
        # (cashdiff1, rival_money1, sim_max, sheep143, expect)
        (0.0, 2854.0, 1.0, 2, "h1_mirror"),
        (8.0, 2850.0, 1.0, 2, "r37_2965_family"),
        (143.0, 3000.0, 0.0833, 4, "wfr"),
        (0.0, 3000.0, 0.0833, 0, "unknown"),
        (8.0, 2850.0, 0.5, 2, "unknown"),
        (143.0, 3000.0, 0.0833, 0, "unknown"),
        (None, 2850.0, 1.0, 2, "unknown"),
    ]
    out = []
    for cd, rm1, sm, sp, expect in rows:
        got, why = classify_features(cd, rm1, sm, sp)
        out.append({"features": [cd, rm1, sm, sp], "expect": expect,
                    "got": got, "match": got == expect, "why": why})
    return out


if __name__ == "__main__":
    print(json.dumps({
        "version": RECORD_VERSION,
        "classes": list(OC_CLASSES),
        "probe": probe_expected(),
    }, ensure_ascii=False, indent=1))
