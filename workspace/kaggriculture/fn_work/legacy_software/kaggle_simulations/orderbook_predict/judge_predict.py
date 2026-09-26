# -*- coding: utf-8 -*-
"""judge_predict_replay（R21 L1）+ flip_stats（L2）：判决线。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
重放 26 败局（starve strip 语料；晚段崩 15 局为重点）+10 胜局对照，r38 件
对原局实况逐局双席位各演一遍；聚合判据出 evidence；另跑闭环副证（h2h vs
r37 主对+r34a 辅对，独立 seed n、席位翻转不双计）。
判据（R21 ②）：胜局对照不翻负 ∧ 晚崩局翻正 ≥1/3（15 局中 ≥5 翻正）∧
闭环 h2h ≥0.55；realized 价提升为观测指标。
"""
from __future__ import annotations

from typing import Any, Dict, Sequence


def judge_predict_replay(pkg_path: str, corpus: Sequence[str],
                         bench: Any = None) -> Dict[str, Any]:
    """26 败局+10 对照重演+闭环副证，聚合判据出 evidence JSON。

    签名意图：输入: r38 包+语料局单+副证配置 / 输出: evidence JSON（逐局翻转/
    realized 价/避让次数/副证 h2h） / 错误: 单局失败标红计入不短路。
    """
    raise NotImplementedError("unimplemented:fn:judge_predict_replay")


def flip_stats(states: Any, baseline: Any) -> Dict[str, Any]:
    """逐局统计：晚崩翻转判定（原局后半程被翻 vs r38 重演结局）、撞车品项
    realized 价差、避让/抢跑次数；胜局对照终局资金差（不翻负判据）。

    签名意图：输入: 对局状态序列+原局基线 / 输出: {flip, realized, dodges,
    front_runs, final_delta, verdict} / 错误: 缺字段→UNKNOWN。
    """
    raise NotImplementedError("unimplemented:fn:flip_stats")
