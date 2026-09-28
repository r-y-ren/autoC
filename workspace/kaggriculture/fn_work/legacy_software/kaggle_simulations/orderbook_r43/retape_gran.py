# -*- coding: utf-8 -*-
"""retape_granularity（R26 L2 ③跨拍细颗粒）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：大额同拍 SELL
（超过阈值）按该品排水节奏拆分至相邻拍（目标单均量向 4.6-5.9 量级靠拢）；
逐品守恒；同拍内同品仍并单（在①之后运行，只拆跨拍）。
"""
from __future__ import annotations

from typing import Any, Dict


def retape_granularity(routes: Any, drain_table: Any = None,
                       config: Any = None) -> Dict[str, Any]:
    """③跨拍细颗粒。签名意图：输入: 解码路由表+排水表+阈值配置 / 输出:
    {routes, 变更表 kind=granularity, 守恒账} / 错误: 守恒破即抛。"""
    raise NotImplementedError("unimplemented:fn:retape_granularity")
