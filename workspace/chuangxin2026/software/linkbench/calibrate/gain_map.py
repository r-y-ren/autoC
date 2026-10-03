"""软件增益 → 注入功率映射（发射端标定的核心换算）。"""

from __future__ import annotations


def software_gain_to_db(gain_index: float) -> float:
    """B210 UHD 增益档位 → 标称注入功率 dB（标定表查表/内插）。"""
    raise NotImplementedError("unimplemented:fn:software_gain_to_db")
