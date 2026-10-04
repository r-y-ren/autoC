# -*- coding: utf-8 -*-
"""extract_world_fingerprint（R24 v2 共享）：市场面画像提取。

责任契约（fn_docs/hybrid/responsibility.md【R24 增补 v2·共享函数】）：
从对局状态序列或运行时 observation 的 step144 时点提取**市场面三桶离散
签名**（v1 具名三维[地块布局/作物适性/城镇需求节律]经 71 局方差扫描证伪
为常量退役——evidence/r24_world_variance_forensic.json）：
  ①价格偏移桶 a：主力变现品 WOOL/MILK 价格相对基准偏移均值档
  ②库存水位桶 b：市场 WHEAT 库存分档
  ③需求节奏桶 c：主力作物 STRAWBERRY/WHEAT 价格相对基准偏移均值档
签名=三桶标 "a|b|c"（各取 L/M/H）。**禁入守卫（硬）**：签名与中间量不得
含店名/店对/店表导出量/route_id/自家走法量——检出即抛。建库/运行时/实验
三口径同函数同输出（同世界→同签名）。
"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional, Sequence, Tuple

REVEAL_STEP = 144

#: 基准价（step0 常量，71/71 局逐位同——方差扫描口径）。
BASE_PRICES: Dict[str, float] = {
    "CARROT": 35.0, "EGG": 50.0, "FERTILIZER": 100.0, "MELON": 250.0,
    "MILK": 160.0, "STRAWBERRY": 120.0, "TOMATO": 60.0, "WHEAT": 25.0,
    "WOOL": 200.0,
}

BAND_LO = 1.15          # 偏移分档界（1.15/1.25 覆盖实测 1.1-1.3 档面）
BAND_HI = 1.25
INV_LO = 9200.0         # 市场 WHEAT 库存分档界（初值 10000，消费下拉）
INV_HI = 9700.0

#: 禁入令牌（大小写不敏感子串）：店名全集+店表/route/自家走法量词。
_BANNED_TOKENS: Tuple[str, ...] = (
    "BAKERY", "BRUNCH_SPOT", "FARMERS_MARKET", "ICE_CREAM_SHOP", "PET_CAFE",
    "PIZZA_SHOP", "SMOOTHIE_SHOP", "YARN_STORE",
    "SHOP", "ROUTE", "HIRES", "LAND_BUYS", "TILES", "CROPS",
)


def _guard_signature(signature: str) -> str:
    """禁入守卫：签名含禁入令牌或纯数字段（route_id 形）即抛。"""
    up = str(signature).upper()
    for tok in _BANNED_TOKENS:
        if tok in up:
            raise ValueError("禁入令牌混入签名: %r" % tok)
    for seg in str(signature).split("|"):
        if seg.strip().isdigit():
            raise ValueError("route_id 形段混入签名: %r" % seg)
    return signature


def _step_label(obs: Dict[str, Any]) -> int:
    """观察步标：step 字段或 day*24+hour（与 r37 _step_of 同式）。"""
    raw = obs.get("step")
    if raw is not None:
        return int(raw)
    return int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))


def _band(ratio: float) -> str:
    """偏移档：<1.15 L / <1.25 M / 其余 H。"""
    if ratio < BAND_LO:
        return "L"
    if ratio < BAND_HI:
        return "M"
    return "H"


def _inv_band(inv: float) -> str:
    """库存档：<9200 L / <9700 M / 其余 H。"""
    if inv < INV_LO:
        return "L"
    if inv < INV_HI:
        return "M"
    return "H"


def _face_from_obs(obs: Dict[str, Any]) -> Optional[str]:
    """单帧观察→三桶签名；字段缺失→None。"""
    market = obs.get("market")
    if not isinstance(market, dict):
        return None
    prices = market.get("prices")
    invs = market.get("inventory")
    if not isinstance(prices, dict) or not isinstance(invs, dict):
        return None

    def _dev(item: str) -> Optional[float]:
        px = prices.get(item)
        base = BASE_PRICES.get(item)
        if not isinstance(px, (int, float)) or not base:
            return None
        return float(px) / float(base)

    dev_wool, dev_milk = _dev("WOOL"), _dev("MILK")
    dev_straw, dev_wheat = _dev("STRAWBERRY"), _dev("WHEAT")
    wh = invs.get("WHEAT")
    if dev_wool is None or dev_milk is None or dev_straw is None or \
            dev_wheat is None or not isinstance(wh, (int, float)):
        return None
    a = _band((dev_wool + dev_milk) / 2.0)
    b = _inv_band(float(wh))
    c = _band((dev_straw + dev_wheat) / 2.0)
    return _guard_signature("%s|%s|%s" % (a, b, c))


def _iter_obs_candidates(source: Any) -> Sequence[Dict[str, Any]]:
    """输入形态归一→候选观察序列（观察 dict/（步,观察,动作）/录像步对）。"""
    out = []
    if isinstance(source, dict):
        out.append(source)
        return out
    if isinstance(source, (list, tuple)):
        for entry in source:
            if isinstance(entry, dict) and "market" in entry:
                out.append(entry)
            elif isinstance(entry, (list, tuple)):
                for item in entry:
                    if isinstance(item, dict) and "market" in item:
                        out.append(item)
                    elif isinstance(item, (list, tuple)) and len(item) >= 2 \
                            and isinstance(item[1], dict):
                        out.append(item[1])
    return out


def extract_world_fingerprint(source: Any) -> Optional[str]:
    """市场面三桶签名（建库/运行时/实验三口径同输出）。

    签名意图：输入: 状态序列或 observation（step144 市场面） / 输出:
    签名字符串 "a|b|c" 或 None / 错误: 禁入量检出→抛；字段缺失→None
    （caller 转兜底）。
    """
    try:
        cands = _iter_obs_candidates(source)
        obs: Optional[Dict[str, Any]] = None
        for cand in cands:
            try:
                if _step_label(cand) == REVEAL_STEP:
                    obs = cand
                    break
            except Exception:
                continue
        if obs is None and isinstance(source, dict):
            obs = source
        if obs is None:
            return None
        return _face_from_obs(obs)
    except ValueError:
        raise
    except Exception:
        return None
