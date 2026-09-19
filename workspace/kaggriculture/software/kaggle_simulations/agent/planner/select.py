# ===========================================================================
# 【中文·模块导览】planner/select.py —— DTSP 鲁棒选择器（Track-B P2）
# ---------------------------------------------------------------------------
# 职责：对 J(plan,ω) 效用矩阵做鲁棒聚合与 argmax。三种聚合策略（可配置，
#   track-B §4 组件 4"对手模型集上取 trimmed-mean / worst-case"）：
#     trimmed_mean  截尾均值：每端裁掉 floor(n×trim_fraction) 个序统计量
#                   （对单对手模型异常值稳健；n=1 时退化为该值）
#     worst_case    最坏情形 = min（悲观下界）
#     weighted      加权均值 = Σw·x/Σw（需 weights 全非负且和 >0）
# 数学性质（tests/test_planner_contract.py 逐条钉住）：
#   单调性——抬高任一模型分数不降低该计划的聚合值（序统计量逐坐标弱增）；
#   平票确定性——聚合值相等的计划按 key() 字典序取最小，输入顺序无关。
# 纪律：stdlib-only、确定性（全部排序显式键）、非法输入抛带失败示例的
#   显式异常。
# ===========================================================================

import math

AGGREGATION_STRATEGIES = ("trimmed_mean", "worst_case", "weighted")
DEFAULT_TRIM_FRACTION = 0.25
# K1 近平守成 tie-break 阈值（round-24 法证终稿 §5 K1，2026-09-20）：最优
# 计划相对 identity 守成点的聚合边际 < tau×|identity 值| 时恒选守成点——
# 消除"计划微差但方差大"的误选（d0 反事实：5/9 局 base 即最优，DTSP v2
# 反而 -3.1k~-32.1k；anchor 晚季误选 -21.7k）。0.005 = 0.5% 终局资金。
IDENTITY_TIEBREAK_TAU = 0.005


def aggregate_scores(scores, strategy="trimmed_mean", weights=None,
                     trim_fraction=DEFAULT_TRIM_FRACTION):
    """单计划跨对手模型的聚合分数。

    scores: {model_name: float}（非空）；weights: {model_name: float}
    （weighted 策略必填且覆盖 scores 的全部键）。
    """
    if not scores:
        raise ValueError(
            "aggregate_scores 收到空 scores（示例：{} 应至少含一个模型分数）")
    if strategy not in AGGREGATION_STRATEGIES:
        raise ValueError(
            f"strategy={strategy!r} 不在 {AGGREGATION_STRATEGIES} 内"
            f"（示例：'mean' 应改取 'trimmed_mean'）")
    values = [float(v) for _, v in sorted(scores.items())]
    n = len(values)
    if strategy == "worst_case":
        return min(values)
    if strategy == "weighted":
        if weights is None:
            raise ValueError(
                "weighted 策略需要 weights（示例：weights={'pessimistic_fill'"
                ": 0.5, ...}）")
        wsum = 0.0
        acc = 0.0
        for name in sorted(scores):
            if name not in weights:
                raise ValueError(
                    f"weights 缺模型键 {name!r}（示例：scores 含 "
                    f"'pessimistic_fill' 而 weights 无此键）")
            w = float(weights[name])
            if w < 0.0 or math.isnan(w):
                raise ValueError(
                    f"weights[{name!r}]={w!r} 必须为非负有限数"
                    f"（示例：-0.1 非法）")
            acc += w * float(scores[name])
            wsum += w
        if wsum <= 0.0:
            raise ValueError(
                f"weights 之和 {wsum} 必须 >0（示例：全 0 非法）")
        return acc / wsum
    # trimmed_mean：按【值序】裁掉每端 floor(n×trim_fraction) 个序统计量；
    # 保证至少留 1 个（n=1 → trim=0）。
    # v3.1 缺陷修复（2026-09-20，标定实测证据）：此前按 name-sorted 顺序
    #   切片——键序 ≠ 值序时裁掉的是"名字居中"而非"值居中"的模型，
    #   实测 Ω=4 下 kept=(值最小+值最大)、悲观/中性两个中位模型反被裁掉
    #   （110683437 d5 实测：kept=(9496.0, 13374.2)=min+max，悲观 10015.5
    #   与 wheat_sup 10960.1 被裁）——投影器对悲观折扣全局失敏（自适应
    #   折扣成为死代码），与本文档"序统计量"契约直接矛盾。
    #   已有契约测试用 {'a':1,'b':2,'c':3,'d':4} 键序=值序的巧合样本，未
    #   能暴露该缺陷；回归测试见 test_planner_contract
    #   ::test_trimmed_mean_value_order_statistics。
    frac = float(trim_fraction)
    if not 0.0 <= frac < 0.5:
        raise ValueError(
            f"trim_fraction={trim_fraction!r} 必须在 [0, 0.5) 内"
            f"（示例：0.5 会裁空两侧）")
    trim = int(math.floor(n * frac))
    trim = min(trim, (n - 1) // 2)      # 至少保留 1 个（n=1 → trim=0）
    ordered = sorted(values)            # 值序（序统计量口径）
    kept = ordered[trim:n - trim] if trim else ordered
    return sum(kept) / len(kept)


def robust_select(j_matrix, strategy="trimmed_mean", weights=None,
                  trim_fraction=DEFAULT_TRIM_FRACTION, identity_key=None,
                  tau=IDENTITY_TIEBREAK_TAU):
    """J(plan,ω) 矩阵的鲁棒 argmax（确定性；K1 近平守成 tie-break）。

    j_matrix: {plan_key: {model_name: score}}（两层的值均可哈希键控）。
    identity_key: K1 守成点键（None=关闭守成 tie-break，行为与 P2.6 一致）；
    最优计划非 identity 且其聚合边际 < tau×max(1,|identity 值|) 时改选
    identity（ranking 保持原序，tie_break 注记守成裁决）。
    返回 {"best": plan_key, "ranking": [(plan_key, agg)...], "strategy":...,
          "tie_break": None|str, "aggregates": {plan_key: agg}}。
    ranking 按 (-agg, plan_key) 字典序——平票时 key 字典序最小者胜，
    输入 dict 顺序不影响结果。
    """
    if not j_matrix:
        raise ValueError(
            "robust_select 收到空 J 矩阵（示例：{} 应至少含一个计划）")
    aggregates = {}
    for plan_key in sorted(j_matrix):
        aggregates[plan_key] = aggregate_scores(
            j_matrix[plan_key], strategy=strategy, weights=weights,
            trim_fraction=trim_fraction)
    ranking = sorted(aggregates.items(), key=lambda kv: (-kv[1], kv[0]))
    best_key, best_value = ranking[0]
    tied = [k for k, v in ranking if v == best_value]
    tie_break = None
    if len(tied) > 1:
        tie_break = (f"{len(tied)} 个计划聚合值并列 {best_value!r}，"
                     f"按 key 字典序取 {best_key!r}")
    if identity_key is not None and identity_key in aggregates \
            and best_key != identity_key:
        identity_value = aggregates[identity_key]
        margin = best_value - identity_value
        gate = tau * max(1.0, abs(identity_value))
        if margin < gate:
            best_key, best_value = identity_key, identity_value
            tie_break = (
                f"K1 近平守成：最优 {ranking[0][0]!r} 对 identity 边际 "
                f"{margin:+.1f} < tau×|identity|={gate:.1f}（τ="
                f"{tau}）→ 恒选守成点 {identity_key!r}")
    return {"best": best_key, "ranking": ranking, "strategy": strategy,
            "tie_break": tie_break, "aggregates": dict(aggregates)}
