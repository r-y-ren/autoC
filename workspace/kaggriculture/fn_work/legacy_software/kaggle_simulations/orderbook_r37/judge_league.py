# -*- coding: utf-8 -*-
"""judge_sheep_league（R20 L1）+ count_shearings（L2）：判决联赛线。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
离线真交易联赛 300-500 局（配置局数）：r37 vs r34a 主对双席位+强对手样本
（分析22 败局对手谱系）+mirror 对；逐局 WL+剪毛刀次+照顾覆盖率；聚合判据
出 evidence JSON。判据（R20 ②）：剪毛 5 刀达成、h2h vs r34a ≥0.55、
胜局对照不翻负；care_rate/feed_rate 为观测指标不进门槛。
"""
from __future__ import annotations

from typing import Any, Dict, Sequence


def judge_sheep_league(r37_pkg: str, r34a_pkg: str, opponents: Sequence[str],
                       n_games: int) -> Dict[str, Any]:
    """300-500 局联赛跑批+逐局 WL/刀次/分组胜率聚合。

    签名意图：输入: r37 包+r34a 包+对手清单+局数配置 / 输出: evidence JSON
    （逐局 WL/刀次/分组胜率） / 错误: fail-closed。
    """
    raise NotImplementedError("unimplemented:fn:judge_sheep_league")


def count_shearings(states: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """剪毛刀次统计：数对羊格的动物格 HARVEST（product=WOOL）事件数，按局/
    按只聚合；同出 CARE/FEED 覆盖率（照顾全程观测指标，不进门槛）。

    签名意图：输入: parse_episode_states 输出 /
    输出: {shearings, care_rate, feed_rate} / 错误: 缺字段→UNKNOWN。
    """
    raise NotImplementedError("unimplemented:fn:count_shearings")
