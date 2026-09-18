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
    # trimmed_mean：每端裁 floor(n×trim_fraction) 个；保证至少留 1 个
    frac = float(trim_fraction)
    if not 0.0 <= frac < 0.5:
        raise ValueError(
            f"trim_fraction={trim_fraction!r} 必须在 [0, 0.5) 内"
            f"（示例：0.5 会裁空两侧）")
    trim = int(math.floor(n * frac))
    trim = min(trim, (n - 1) // 2)      # 至少保留 1 个（n=1 → trim=0）
    kept = values[trim:n - trim] if trim else values
    return sum(kept) / len(kept)


def robust_select(j_matrix, strategy="trimmed_mean", weights=None,
                  trim_fraction=DEFAULT_TRIM_FRACTION):
    """J(plan,ω) 矩阵的鲁棒 argmax（确定性）。

    j_matrix: {plan_key: {model_name: score}}（两层的值均可哈希键控）。
    返回 {"best": plan_key, "ranking": [(plan_key, agg)...], "strategy":...,
          "tie_break": None|str, "aggregates": {plan_key: agg}}。
    ranking 按 (-agg, plan_key) 字典序——平票时 key 字典序最小者胜，
    输入 dict 顺序不影响结果；tie_break 注记平票情形。
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
    return {"best": best_key, "ranking": ranking, "strategy": strategy,
            "tie_break": tie_break, "aggregates": dict(aggregates)}
