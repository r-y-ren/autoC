# -*- coding: utf-8 -*-
"""judge_cash_guard_replay（R19 L1）+ replay_guard_verdict（L2）：判决重演线。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
本地官方引擎重放 6 局灾难局（112938600/112968467/112976582/113002280/
113094793/113099386）+10 胜局对照（同窗抽样），r37 件对原局实况逐局双席位
各演一遍（排除座位效应）；逐局三指标（d2 前牲畜逃走/BUY_ANIMAL 失败/
d1 h0 现金）+对照终局资金差。判据（R19 ②）：死牛 0、买牲畜失败 0、
d1 h0 现金≥4、对照资金 l1 非负。
"""
from __future__ import annotations

from typing import Any, Dict, Sequence


def judge_cash_guard_replay(pkg_path: str, corpus: Sequence[str]) -> Dict[str, Any]:
    """6 灾难局+10 对照局重放并聚合三指标出 evidence JSON。

    签名意图：输入: r37 包+语料局单 / 输出: evidence JSON（逐局三指标+对照
    终局资金差） / 错误: 单局重放失败标红计入，不短路全跑。
    """
    raise NotImplementedError("unimplemented:fn:judge_cash_guard_replay")


def replay_guard_verdict(states: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """单局三指标核算：d2 前牲畜逃走计数（格上牲畜消失+consecutive_unfed
    轨迹吻合）、BUY_ANIMAL 失败计数（提交后未成交）、d1 h0 现金值；对照局加
    终局资金差（r37−实况）。

    签名意图：输入: parse_episode_states 输出 /
    输出: {died_before_d2, buy_failed, cash_d1h0, final_delta, verdict} /
    错误: 缺字段→verdict=UNKNOWN。
    """
    raise NotImplementedError("unimplemented:fn:replay_guard_verdict")
