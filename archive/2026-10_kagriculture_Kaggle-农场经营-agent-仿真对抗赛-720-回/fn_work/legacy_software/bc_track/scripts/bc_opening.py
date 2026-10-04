# -*- coding: utf-8 -*-
"""票 03 第 1 轮·方案 A：开局市场剧本先验注入（修"冻死吸引子"）.

M1 归因：市场头 non-NONE 准确率 30.8% < 多数类 39.7%，闭环后 8/8 局
从未发出任何买单（buy_seed/animal/product/land 全 0），资金冻死在
~2,975。修复思路（island-ga "base schedule is where the cheap points
are"）：d0-d3 市场订单强制走顶部剧本先验，把开局态拉回专家分布，
d4 起交还 BC 两头。

剧本来源（逐字解码，非转写表格）：
  references/data/intel-notebooks/v48build/main.py 内 _V48_ROUTES
  （zlib+b85 payload）解压出的 6 条 719 步路由之 'default'，取前 96 步
  （d0-d3；其中前 88 步为全路由共享前缀，digest 实证）的市场订单列。
  来源登记：references/digests/public-bot-reverse-eng-20260920.md §1/§2
  （抓取 2026-08-31，精读 2026-09-20）。

单变量纪律：只覆写市场订单（steps 0..N-1），单位动作全季归 BC；
N 默认 96。剧本中买不起/无货可卖的订单按引擎语义静默 no-op、零成本
（island-ga "Financing by optimism"）。

用法：
    from bc_opening import OpeningScriptPolicy
    policy = OpeningScriptPolicy(BCPolicy(), until_step=96)
"""
from __future__ import annotations

import json
from pathlib import Path

from bc_policy import to_plain_obs

# v48 'default' 路由 steps 0-95 市场订单（step -> orders；缺省步 = 空单）。
# d0: 4 羊(2000)+瓜种7(560)+麦种5(50)+麦产品4+HIRE×2 → 日终 ~$190
_SCRIPT: dict[int, list] = {
    0: [["BUY_PRODUCT", "WHEAT", 4], ["HIRE"], ["HIRE"],
        ["BUY_SEED", "MELON", 7], ["BUY_SEED", "WHEAT", 5],
        ["BUY_ANIMAL", "SHEEP", 4]],
    2: [["BUY_PRODUCT", "WHEAT", 4]],
    24: [["BUY_PRODUCT", "WHEAT", 5], ["BUY_SEED", "WHEAT", 1]],
    25: [["HIRE"], ["HIRE"], ["HIRE"], ["BUY_SEED", "WHEAT", 1]],
    41: [["SELL", "FERTILIZER", 1], ["BUY_SEED", "WHEAT", 3]],
    42: [["BUY_PRODUCT", "WHEAT", 2]],
    44: [["SELL", "FERTILIZER", 3], ["BUY_SEED", "STRAWBERRY", 1]],
    45: [["BUY_SEED", "STRAWBERRY", 1]],
    48: [["HIRE"], ["HIRE"], ["HIRE"]],
    52: [["BUY_PRODUCT", "WHEAT", 2]],
    68: [["BUY_PRODUCT", "WHEAT", 1]],
    70: [["SELL", "FERTILIZER", 4], ["BUY_PRODUCT", "WHEAT", 3]],
    72: [["HIRE"], ["HIRE"], ["HIRE"], ["BUY_SEED", "STRAWBERRY", 1]],
    88: [["BUY_PRODUCT", "WHEAT", 3], ["BUY_PRODUCT", "WHEAT", 1]],
    92: [["SELL", "FERTILIZER", 1]],
    93: [["SELL", "FERTILIZER", 3]],
}

DEFAULT_UNTIL_STEP = 96          # d0-d3（step = day*24 + hour）

# 全剧本模式（A2）单位动作表：v48 'default' 路由 steps 0-95 的
# farmer/hands/market 完整动作（data/v48_default_d0d3_actions.json，
# 由 references/data/intel-notebooks/v48build/main.py 的 _V48_ROUTES
# 解码生成；farmer 每日 EOD 归位出生点、hands EOD 清零——引擎语义保证
# 逐日位置独立，剧本单位动作可跨局复放；非法动作静默 no-op）。
_FULL_TABLE_PATH = (Path(__file__).resolve().parent.parent / "data"
                    / "v48_default_d0d3_actions.json")


def _load_full_table() -> dict[int, dict]:
    raw = json.loads(_FULL_TABLE_PATH.read_text(encoding="utf-8"))
    return {int(k): v for k, v in raw.items()}


def _obs_step(obs_plain: dict) -> int:
    """席位无关步号：obs.step 只写在 seat0（框架语义），seat1 用
    day*24+hour 推导——与 bc_schema.extract_global_features 同一解读。"""
    step = obs_plain.get("step")
    if step is None:
        step = (int(obs_plain.get("day") or 0) * 24
                + int(obs_plain.get("hour") or 0))
    return int(step)


class OpeningScriptPolicy:
    """官方语义 callable 包装。

    - units=False（A1）：步号 < until_step 时只覆写市场订单；
    - units=True（A2）：步号 < until_step 时 farmer/hands/market 全走
      v48 剧本（市场表同 A1 逐字一致）。
    其余一切透传被包装策略。"""

    def __init__(self, base, until_step: int = DEFAULT_UNTIL_STEP,
                 collect_stats=True, units: bool = False):
        self.base = base
        self.until_step = int(until_step)
        self.collect_stats = collect_stats
        self.units = units
        self._full = _load_full_table() if units else None
        self.trace: list[tuple[int, list]] = []   # (step, market_orders)

    def __call__(self, obs):
        plain = to_plain_obs(obs)
        step = _obs_step(plain)
        if step >= self.until_step:
            return self.base(obs)
        if not self.units:
            action = self.base(obs)
            action = dict(action)
            action["market"] = [list(o) for o in _SCRIPT.get(step, [])]
            if self.collect_stats and action["market"]:
                self.trace.append((step, action["market"]))
            return action
        entry = self._full.get(step) or {}
        action = {
            "farmer": list(entry.get("f") or ["PASS"]),
            "hands": [list(h) for h in entry.get("h") or []],
            "market": [list(o) for o in entry.get("m") or []],
        }
        if self.collect_stats and action["market"]:
            self.trace.append((step, action["market"]))
        return action

    def __getattr__(self, name):
        return getattr(self.base, name)
