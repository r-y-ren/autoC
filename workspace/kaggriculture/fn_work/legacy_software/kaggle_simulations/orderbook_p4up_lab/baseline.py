# -*- coding: utf-8 -*-
"""baseline —— leoprovorov p25 磁带长度基线（对手画像/判决分层）。

data/opponents_baseline.json = 11 队 p10/p25/p50 自报硬数据（cell 16 ROWS）+
口径注 + 来源；分层边界（tape_tier_scheme）为我方派生口径（对齐店开拍 72/144）。
用法：divergence.tape_profile() 实测候选/对手磁带长度 → profile_lookup() 给
tier + 最近邻基线队，入判决分层。
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data",
                     "opponents_baseline.json")


def load_baseline(path: Optional[str] = None) -> Dict[str, Any]:
    with open(path or _DATA, encoding="utf-8") as fh:
        return json.load(fh)


def tape_tier(p25: Optional[int], tiers: Optional[List[Dict[str, str]]] = None
              ) -> Optional[str]:
    """按 p25 落档（边界=我方派生口径，见 baseline JSON tape_tier_scheme）。"""
    if p25 is None:
        return None
    tiers = tiers or load_baseline()["tape_tier_scheme"]["tiers"]
    for t in tiers:
        rule = t["rule"]
        if "p25 <= 4" == rule and p25 <= 4:
            return t["tier"]
        if rule == "4 < p25 < 72" and 4 < p25 < 72:
            return t["tier"]
        if rule == "72 <= p25 < 144" and 72 <= p25 < 144:
            return t["tier"]
        if rule == "p25 >= 144" and p25 >= 144:
            return t["tier"]
    return None


def profile_lookup(p10: Optional[int], p25: Optional[int], p50: Optional[int],
                   baseline: Optional[Dict[str, Any]] = None
                   ) -> Dict[str, Any]:
    """实测 p10/p25/p50 → 分层 + 最近邻基线队（|Δp25| 最小，p10/p50 作并列裁决）。"""
    base = baseline or load_baseline()
    tier = tape_tier(p25, base["tape_tier_scheme"]["tiers"])
    nearest = None
    if p25 is not None:
        cand = []
        for row in base["teams"]:
            d25 = abs(row["p25"] - p25)
            d10 = abs(row["p10"] - (p10 if p10 is not None else row["p10"]))
            d50 = abs(row["p50"] - (p50 if p50 is not None else row["p50"]))
            cand.append((d25, d10, d50, row))
        cand.sort(key=lambda c: (c[0], c[1], c[2]))
        nearest = {"team": cand[0][3]["team"], "delta_p25": cand[0][0],
                   "wins": cand[0][3]["wins"], "note": cand[0][3].get("note", "")}
    return {
        "measured": {"p10": p10, "p25": p25, "p50": p50},
        "tape_tier": tier,
        "tier_reading": next(
            (t["reading"] for t in base["tape_tier_scheme"]["tiers"]
             if t["tier"] == tier), None),
        "nearest_baseline_team": nearest,
        "baseline_self_reported": True,
        "caliber_note": base["caliber"]["bundle_definition"],
        "self_check_rule": ("'冰在火位=过刚、火在冰位=白花'（leoprovorov cell 6 应用 5，"
                            "自检法）：候选 p25 明显长于其世界的同行=白花灵活性；明显短=过刚"),
    }
