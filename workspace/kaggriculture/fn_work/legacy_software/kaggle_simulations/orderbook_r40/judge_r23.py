# -*- coding: utf-8 -*-
"""judge_r23 + segment_stats（R23 L1/L2）：判决线。

责任契约：败局 12 局定向重演（分析24 败局谱系）+联赛 300-500 局（含榜前
550 段强手样本）+分段统计（d21-28 资金差/实现单价/有效挂单率）+仿真器对照
（≥30 局抽样与官方引擎逐局一致）；聚合分项四判据+总判出 evidence。
"""
from __future__ import annotations

from typing import Any, Dict


def judge_r23(pkg_path: str, corpus: Any, bench: Any = None) -> Dict[str, Any]:
    """判决 v23：败局定向重演+联赛+分段统计+仿真器对照，聚合分项+总判。

    签名意图：输入: r40 包+语料+副证配置 / 输出: evidence JSON /
    错误: 单局红计入不短路。
    """
    raise NotImplementedError("unimplemented:fn:judge_r23")


def segment_stats(states: Any, baseline: Any = None) -> Dict[str, Any]:
    """分段统计：d21-28 段资金差、实现单价、有效挂单占比、批量化率。

    签名意图：输入: 对局状态序列+原局基线 / 输出: {seg_delta, realized_px,
    fill_rate, lot_size, verdict} / 错误: 缺字段→UNKNOWN。
    """
    raise NotImplementedError("unimplemented:fn:segment_stats")
