# -*- coding: utf-8 -*-
"""extract_world_fingerprint（R24 共享）：世界开局画像提取。

责任契约（fn_docs/hybrid/responsibility.md【R24 增补·共享函数】）：
从对局状态序列（建库口径）或运行时 observation（选路口径）提取外生世界面
三维离散签名：①起始地块布局桶 ②作物适性桶 ③城镇需求节律桶；签名=三桶标
"a|b|c"。**禁入守卫（硬）**：签名与中间量不得含店名/店对/店表导出量/
route_id/自家走法量（hires/land_buys/tiles_by_crop 等）——检出即抛。
两口径同函数同输出（同世界→同签名）。
"""
from __future__ import annotations

from typing import Any, Optional


def extract_world_fingerprint(source: Any) -> Optional[str]:
    """世界开局画像三维签名（建库/运行时两口径同输出）。

    签名意图：输入: 状态序列或 observation（step≤144 可观测外生面） /
    输出: 签名字符串 "a|b|c" 或 None / 错误: 禁入量检出→抛；
    字段缺失→None（caller 转兜底）。
    """
    raise NotImplementedError("unimplemented:fn:extract_world_fingerprint")
