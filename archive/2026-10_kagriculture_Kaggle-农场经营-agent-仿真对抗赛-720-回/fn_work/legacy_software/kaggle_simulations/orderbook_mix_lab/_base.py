# -*- coding: utf-8 -*-
"""_base —— R15 共享常数与轻工具（orderbook_mix_lab 内部件）。

复用资产（只调用不重写）：
  - R14 orderbook_surge_lab：corpus（回放发现/标注/tag）、phase_a
    （daily_netflow_decompose）、phase_b（load_l3_callable/replay_dual_seat）；
  - L3 基座（orderbook_l3_derivative/main.py）磁带结构（_R108_DATA blob）。

引擎常数兜底表与 twin 装载的引擎模块一致（S 批实跑时 _engine_crops 会
对兜底表做一次校验，不一致即 fail）。
"""
from __future__ import annotations

import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_KSIM = os.path.dirname(_HERE)              # .../kaggle_simulations
_SOFTWARE = os.path.dirname(_KSIM)          # .../legacy_software
_CAMPAIGN = os.path.dirname(_SOFTWARE)      # .../fn_work 的上级 = 战役根

# 引擎/基座常数（与 L3 main.py SEED_PRICE 及引擎 CROPS 对齐；装载时校验）
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
              "STRAWBERRY": 100, "MELON": 80}
FIRST_YIELD_DAY = {"WHEAT": 2, "CARROT": 2, "TOMATO": 8,
                   "STRAWBERRY": 10, "MELON": 10}
PLANTABLE = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")

# 语料钉死件
TEAM_NAME = "renyxin"
EARLY_CRASH = (112844424, 112846785, 112847952)   # 29 败局排 3 早崩（-21k~-24k）
RNG_MATERIAL = "20260925r15"                       # rng=random.Random(20260925r15)
MIRROR_MARGIN_MAX = 400.0                          # |margin| < 400
MIRROR_FUND_GAP_MAX = 0.02                         # 资金差 < 2%
DEFAULT_REPLAY_DIR = "/tmp/r33audit"
DEFAULT_L3_MAIN = os.path.join(_KSIM, "orderbook_l3_derivative", "main.py")
DEFAULT_AUDIT_ROWS = os.path.join(_CAMPAIGN, "audit_rows.json")

R14_EVIDENCE = os.path.join(_KSIM, "orderbook_surge_lab", "evidence",
                            "judgment.json")

# 重演预算（需求：≤1100 局次）
MAX_REPLAYS = 1100


def rng_seed(material: str = RNG_MATERIAL) -> int:
    """材料串 → 可复现整数种子（R14 推导先例：sha256 前 16 hex 转 int）。"""
    import hashlib
    return int(hashlib.sha256(material.encode("utf-8")).hexdigest()[:16], 16)


# ---------------------------------------------------------------------------
# L3 磁带 blob 编解码（顺序沿 build_v6 的受控变更集方法：区间外逐字节不动）
# ---------------------------------------------------------------------------
_ROUTES_RE = re.compile(
    r"_R108_DATA=json\.loads\(zlib\.decompress\(base64\.b85decode\('([^']+)'\)\)\)")


def decode_l3_blob(main_text: str):
    """L3 main 文本 → (data, span)。span 为 blob 字面量（引号内）的字符区间。"""
    m = _ROUTES_RE.search(main_text)
    if not m:
        raise ValueError("L3 main 无 _R108_DATA blob")
    import base64
    import json
    import zlib
    data = json.loads(zlib.decompress(base64.b85decode(m.group(1))))
    return data, m.span(1)


def encode_l3_blob(data) -> str:
    """data → base85(zlib(json)) 字面量体（与 L3 原编码参数逐字节同构）。"""
    import base64
    import json
    import zlib
    raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return base64.b85encode(zlib.compress(raw.encode("utf-8"), 9)).decode("ascii")
