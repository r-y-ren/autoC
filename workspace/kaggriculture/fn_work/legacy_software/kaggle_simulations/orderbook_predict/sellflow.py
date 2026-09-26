# -*- coding: utf-8 -*-
"""build_sellflow_library（R21 L2）：对手卖流库构建。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
从 86 局逐动作 replay（/tmp/r33audit）提取对手 SELL 事件（步/品类/量），
聚合为按（首二店组合，step-2 身份指纹）键的分布库（步窗-品类-量直方）；
analysis20/22 分层标签作注记；输出可内嵌紧凑数据结构+构建审计（来源 sha/
覆盖局数）。
"""
from __future__ import annotations

from typing import Any, Dict


def build_sellflow_library(replay_dir: str, labels: Any = None) -> Dict[str, Any]:
    """86 局逐动作 replay → 对手卖流分布库+构建审计。

    签名意图：输入: replay 目录+分层标签 / 输出: {library, build_audit} /
    错误: 语料缺失/解析失败即抛（fail-closed）。
    """
    raise NotImplementedError("unimplemented:fn:build_sellflow_library")
