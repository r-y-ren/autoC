# -*- coding: utf-8 -*-
"""parse_episode_states（R19/R20 共享）：对局状态序列解析。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补·共享函数】）：
replay JSON → 逐步双席规范行 {step, seat, action, money, hands, animals_grid,
tiles}；解析口径经分析22 考古实测校准（磁带 step X ↔ replay si X+1；
steps[t][seat].observation 为该步执行后值；action 由前一拍观测算出）。
调用方：replay_guard_verdict, count_shearings。
"""
from __future__ import annotations

from typing import Any, Dict, List


def parse_episode_states(replay_path: str) -> List[Dict[str, Any]]:
    """replay JSON → 逐步双席规范行数组。

    签名意图：输入: replay JSON 路径 / 输出: 逐步状态行数组 /
    错误: 格式不符/缺字段即抛。
    """
    raise NotImplementedError("unimplemented:fn:parse_episode_states")
