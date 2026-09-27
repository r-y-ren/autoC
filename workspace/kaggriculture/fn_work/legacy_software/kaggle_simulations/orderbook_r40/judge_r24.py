# -*- coding: utf-8 -*-
"""judge_r24 及判决面子件（R24 L1/L2）。

责任契约（fn_docs/hybrid/responsibility.md【R24 增补】）：
判决 v24——联赛 h2h vs r40（核心判据 ≥0.55）+库信息自检
（library_info_check，交叉口径防循环）+观测记录（联赛总胜率/族命中率/
族内 n 分布）；聚合 evidence。判据=R24 验收 ②③④ 原文。
"""
from __future__ import annotations

from typing import Any, Dict


def judge_r24(package: Any, corpus: Any = None, config: Any = None) -> Dict[str, Any]:
    """判决 v24（h2h vs r40+库信息自检+观测，聚合 evidence）。

    签名意图：输入: r41 包+语料+副证配置 / 输出: evidence JSON /
    错误: 单局红计入不短路。
    """
    raise NotImplementedError("unimplemented:fn:judge_r24")


def library_info_check(games: Any, library: Any) -> Dict[str, Any]:
    """库信息自检（命中胜率−未命中胜率 > 0 方向性检验，交叉口径防循环）。

    签名意图：输入: 判决对局集+库 / 输出: {hit_wr, miss_wr, delta, verdict,
    hit_rate, n_dist} / 错误: 样本不足→UNKNOWN 不短路。
    """
    raise NotImplementedError("unimplemented:fn:library_info_check")
