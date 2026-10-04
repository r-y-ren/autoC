# ===========================================================================
# 【中文·模块导览】robust_selection/robust_selection.py —— 鲁棒选择主流程（L0）
# ---------------------------------------------------------------------------
# 迁自 software/kaggle_simulations/agent/planner/select.py 的 robust_select
# 主流程（行为不变迁移；R3 值序裁切修复由本包叶子 aggregate_scores 承载）：
#   逐计划对 {model_name: score} 调 aggregate_scores 聚合 → 决胜全权委托
#   break_ties_by_identity（(-agg, plan_key) 字典序 argmax + K1 近平守成闸，
#   两次调用分别取"无守成 argmax"与"叠加守成闸后的终裁"）→ 本层只组装
#   返回结构与注记串（平票注记 / K1 守成注记），不重复实现裁切或平票逻辑。
# 返回结构（沿旧码）：{"best", "ranking", "strategy", "tie_break",
#   "aggregates"}；ranking 按 (-agg, plan_key) 字典序——平票时 key 字典序
#   最小者胜，输入 dict 顺序不影响结果；K1 守成裁决不改 ranking（保持原序）。
# 签名登记（ fn_docs 意图 → 旧码真值）：函数名 robust_select→robust_selection
#   （对齐包名），参数名/默认值/返回 dict 结构与旧码一致。
# 纪律：stdlib-only、确定性（全部排序显式键）、空矩阵抛带失败示例的显式异常。
# ===========================================================================

from robust_selection.aggregate_scores import (
    DEFAULT_TRIM_FRACTION,
    aggregate_scores,
)
from robust_selection.break_ties_by_identity import (
    IDENTITY_TIEBREAK_TAU,
    break_ties_by_identity,
)

__all__ = ["robust_selection"]


def robust_selection(j_matrix, strategy="trimmed_mean", weights=None,
                     trim_fraction=DEFAULT_TRIM_FRACTION, identity_key=None,
                     tau=IDENTITY_TIEBREAK_TAU):
    """J(plan,ω) 矩阵的鲁棒 argmax（确定性；K1 近平守成 tie-break）。

    j_matrix: {plan_key: {model_name: score}}（两层的值均可哈希键控）。
    identity_key: K1 守成点键（None=关闭守成 tie-break，行为与 P2.6 一致）；
      最优计划非 identity 且其聚合边际 < tau×max(1,|identity 值|) 时改选
      identity（ranking 保持原序，tie_break 注记守成裁决）。
    聚合与决胜分别委托本包叶子 aggregate_scores / break_ties_by_identity；
    单计划分数集为空、非法 strategy/weights 等由叶子显式抛错。
    返回 {"best": plan_key, "ranking": [(plan_key, agg)...], "strategy":...,
          "tie_break": None|str, "aggregates": {plan_key: agg}}。
    """
    if not j_matrix:
        raise ValueError(
            "robust_selection 收到空 J 矩阵（示例：{} 应至少含一个计划）")
    aggregates = {}
    for plan_key in sorted(j_matrix):
        aggregates[plan_key] = aggregate_scores(
            j_matrix[plan_key], strategy=strategy, weights=weights,
            trim_fraction=trim_fraction)
    ranking = sorted(aggregates.items(), key=lambda kv: (-kv[1], kv[0]))
    # 决胜委托叶子：top=无守成 argmax（平票按 key 字典序）；best=叠加 K1
    # 守成闸后的终裁。二者不同 ⇔ 守成闸触发（本层只据此组装注记）。
    top_key = break_ties_by_identity(aggregates, identity_key=None)
    best_key = break_ties_by_identity(aggregates, identity_key=identity_key,
                                      tau=tau)
    top_value = aggregates[top_key]
    best_value = aggregates[best_key]
    tie_break = None
    tied = [k for k, v in ranking if v == top_value]
    if len(tied) > 1:
        tie_break = (f"{len(tied)} 个计划聚合值并列 {top_value!r}，"
                     f"按 key 字典序取 {top_key!r}")
    if best_key != top_key:
        identity_value = aggregates[identity_key]
        margin = top_value - identity_value
        gate = tau * max(1.0, abs(identity_value))
        tie_break = (
            f"K1 近平守成：最优 {top_key!r} 对 identity 边际 "
            f"{margin:+.1f} < tau×|identity|={gate:.1f}（τ="
            f"{tau}）→ 恒选守成点 {identity_key!r}")
    return {"best": best_key, "ranking": ranking, "strategy": strategy,
            "tie_break": tie_break, "aggregates": dict(aggregates)}
