"""聚合值差 <τ(0.5%) 时优先选 identity 近平计划，按现状迁移（行为不变）。

上游: R3（详见 fn_docs/responsibility.md）

实现要点（源语义=software/kaggle_simulations/agent/planner/select.py 的
robust_select K1 近平守成 tie-break 片段，行为不变迁移，无修复项）：
- argmax 规则沿用旧码 ranking：按 (-聚合值, plan_key) 字典序取首位——平票时
  key 字典序最小者胜，输入 dict 顺序不影响结果。
- K1 守成闸（round-24 法证终稿 §5 K1）：最优计划非 identity 且聚合边际
  margin = best - identity < tau×max(1.0, |identity|) 时改选 identity 守成点；
  比较为严格小于——边界 margin == gate 处**不**切换（旧码 `if margin < gate`）。
  gate 的 max(1.0, ·) 地板：|identity|<1 时退化为绝对阈值 tau。
- identity_key=None（关闭守成，P2.6 行为）、identity_key 不在 aggregates
  （缺席）、或最优即 identity 时均原样返回 argmax，不抛错（错误: 无）。
- 冻结语义锚点：snapshot_tests/test_planner_select_characterization.py
  的 K1 边际 1.5 < tau×1000=5.0 → 恒选守成点。
"""

__all__ = ["IDENTITY_TIEBREAK_TAU", "break_ties_by_identity"]

# K1 近平守成 tie-break 阈值（round-24 法证终稿 §5 K1，2026-09-20）：最优
# 计划相对 identity 守成点的聚合边际 < tau×|identity 值| 时恒选守成点——
# 消除"计划微差但方差大"的误选（d0 反事实：5/9 局 base 即最优，DTSP v2
# 反而 -3.1k~-32.1k；anchor 晚季误选 -21.7k）。0.005 = 0.5% 终局资金。
IDENTITY_TIEBREAK_TAU = 0.005


def break_ties_by_identity(aggregates, identity_key=None,
                           tau=IDENTITY_TIEBREAK_TAU):
    """对聚合结果 {plan_key: agg} 施 K1 近平守成 tie-break，返回决胜计划。

    aggregates: {plan_key: 聚合值}（非空；空集防御属上层 robust_selection）。
    identity_key: K1 守成点键（None=关闭守成 tie-break，行为与 P2.6 一致）；
    最优计划非 identity 且其聚合边际 < tau×max(1,|identity 值|) 时改选
    identity。
    返回决胜 plan_key；守成裁决不改 ranking 本身（上层持原序自注记）。
    """
    ranking = sorted(aggregates.items(), key=lambda kv: (-kv[1], kv[0]))
    best_key, best_value = ranking[0]
    if identity_key is not None and identity_key in aggregates \
            and best_key != identity_key:
        identity_value = aggregates[identity_key]
        margin = best_value - identity_value
        gate = tau * max(1.0, abs(identity_value))
        if margin < gate:
            best_key = identity_key
    return best_key
