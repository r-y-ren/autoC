# -*- coding: utf-8 -*-
"""divergence —— leoprovorov 分歧度量体系（冰火终章 cell 11/17 数学区）。

口径（cell 11）：
  f_g(t) = (op(farmer), n_hands, sorted{op(h)}, {op(m)})，op=(class,good)；
  MOVE 方向并类、数量丢弃、hands 排序列表、market 集合。
  D(t) = 1 − max_c n_c(t)/N(t)；K(t)=不同 bundle 数。
  p_q = min{t : D(t) > q}，q ∈ {0.10, 0.25, 0.50}（cell 17）。
用途：磁带长度刻度（p25 即"两半 agent 的边界"）+ 与 data/opponents_baseline.json
11 队自报表对读（判决分层）。只用胜局是 leoprovorov 口径，本模块对任意局集可用，
调用方负责选样并在报告声明。
"""
from __future__ import annotations

import collections
from typing import Any, Dict, List, Optional, Sequence

from orderbook_p4up_lab.records import bundle_key_jsonable

P_QUANTILES = (0.10, 0.25, 0.50)
SHOP_UNLOCKS = [72, 144, 216]  # leoprovorov cell 16 SHOP_UNLOCKS 前三店


def divergence_curve(streams: Sequence[Sequence[Optional[dict]]]) -> List[Dict[str, Any]]:
    """逐拍 D(t)/K(t)。N(t)=有该拍的局数。"""
    n_max = max((len(s) for s in streams), default=0)
    out = []
    for t in range(n_max):
        keys = [bundle_key_jsonable(s[t]) for s in streams if t < len(s)]
        n = len(keys)
        if n == 0:
            continue
        cnt = collections.Counter(keys)
        d = 1 - max(cnt.values()) / n
        out.append({"t": t, "n": n, "D": round(d, 4), "K": len(cnt)})
    return out


def p_steps(curve: List[Dict[str, Any]],
            quantiles: Sequence[float] = P_QUANTILES) -> Dict[str, Optional[int]]:
    """p_q = min{t : D(t) > q}（严格大于，cell 17 公式）。"""
    out: Dict[str, Optional[int]] = {}
    for q in quantiles:
        hit = next((c["t"] for c in curve if c["D"] > q), None)
        out[f"p{int(q * 100)}"] = hit
    return out


def window_mean_D(curve: List[Dict[str, Any]], t0: int, t1: int) -> Optional[float]:
    vals = [c["D"] for c in curve if t0 <= c["t"] < t1]
    return round(sum(vals) / len(vals), 4) if vals else None


def tape_profile(streams: Sequence[Sequence[Optional[dict]]],
                 label: Optional[str] = None) -> Dict[str, Any]:
    """一组局的磁带长度画像：p10/p25/p50 + 两窗均值（对照 leoprovorov 发表窗）。"""
    curve = divergence_curve(streams)
    return {
        "label": label,
        "n_games": len(streams),
        "turns": len(curve),
        **p_steps(curve),
        "mean_D_d0_71": window_mean_D(curve, 0, 72),
        "mean_D_d72_143": window_mean_D(curve, 72, 144),
        "bundle_caliber": ("leoprovorov f_g(t)：MOVE 并类、数量丢弃、market 集合比、"
                           "hands 排序列表、附 n_hands（cell 11 数学区）"),
    }
