# -*- coding: utf-8 -*-
"""judge_r25 及判决面子件（R25）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：分项+总判
（判据=R25 ①②③+总判原文）：P1 单价+d21-28 / P2 尾段翻正+stranding /
P3 镜像臂+净加卖 0；总判=h2h vs r40 ≥0.55 ∧ 联赛 ≥80%；聚合 evidence。
"""
from __future__ import annotations

from typing import Any, Dict


def judge_r25(package: Any, corpus: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """判决 v25（分项+总判）。签名意图：输入: r42 包+语料+副证配置 / 输出:
    evidence JSON / 错误: 单局红计入不短路。"""
    raise NotImplementedError("unimplemented:fn:judge_r25")


def endgame_stats(states: Any, baselines: Any = None) -> Dict[str, Any]:
    """尾段读数（d29 段差/终拍滞留/翻车翻正）。签名意图：输入: 对局状态序列
    +基线局集 / 输出: {d29_margin, stranding_value, flips, verdict} /
    错误: 缺字段→UNKNOWN。"""
    raise NotImplementedError("unimplemented:fn:endgame_stats")


def mirror_arm_stats(games: Any, credit_ledger: Any = None) -> Dict[str, Any]:
    """镜像臂读数（胜率+credit 净加卖核对）。签名意图：输入: 镜像臂对局集+
    credit 账本 / 输出: {win_rate, net_add_sell, verdict} / 错误: 缺账本
    →UNKNOWN。"""
    raise NotImplementedError("unimplemented:fn:mirror_arm_stats")
