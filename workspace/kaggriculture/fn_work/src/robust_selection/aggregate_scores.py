# ===========================================================================
# 【中文·模块导览】robust_selection/aggregate_scores.py —— 逐计划跨对手聚合
# ---------------------------------------------------------------------------
# 迁自 software/kaggle_simulations/agent/planner/select.py 的 aggregate_scores
# （Track-B P2 语义），并落地 R3 修复：trimmed_mean 的裁切序由模型**名字典序**
# 改为**分数值序**。旧实现 `sorted(scores.items())` 按名字排序后裁端点，裁掉
# 的序统计量与值大小无关 → 悲观模型（pessimistic_fill 名字序恒居尾）恒被裁，
# 投影段悲观折扣零效力（反例与期望值见 snapshot_tests/test_counterexample_r3.py：
# 名字序 35.0/60.0 vs 值序 65.0/22.5）。聚合量与旗面/参数约定不变，三种策略：
#   trimmed_mean  值序截尾均值：每端裁 floor(n×trim_fraction) 个序统计量
#                 （n=1 时退化为该值）
#   worst_case    最坏情形 = min（悲观下界；与排序序无关）
#   weighted      加权均值 = Σw·x/Σw（需 weights 非负有限、覆盖全部键且和>0）
# 数学性质（与旧契约一致）：
#   单调性——抬高任一模型分数不降低聚合值（值序裁切下成立；名字序裁切下
#   不成立，正是 R3 所修）；
#   确定性——结果与输入 dict 顺序无关。
# 纪律：stdlib-only、确定性（值序排序）、非法输入抛带失败示例的显式异常。
# ===========================================================================

import math

AGGREGATION_STRATEGIES = ("trimmed_mean", "worst_case", "weighted")
DEFAULT_TRIM_FRACTION = 0.25


def aggregate_scores(scores, strategy="trimmed_mean", weights=None,
                     trim_fraction=DEFAULT_TRIM_FRACTION):
    """单计划跨对手模型的聚合分数（R3：trimmed_mean 按值序裁切）。

    scores: {model_name: float}（非空）；weights: {model_name: float}
    （weighted 策略必填且覆盖 scores 的全部键）。
    签名与旧码调用约定一致（robust_select 以 strategy=/weights=/
    trim_fraction= 关键字逐计划调用），返回 float 聚合值。
    """
    if not scores:
        raise ValueError(
            "aggregate_scores 收到空 scores（示例：{} 应至少含一个模型分数）")
    if strategy not in AGGREGATION_STRATEGIES:
        raise ValueError(
            f"strategy={strategy!r} 不在 {AGGREGATION_STRATEGIES} 内"
            f"（示例：'mean' 应改取 'trimmed_mean'）")
    # R3 修复点：裁切序=分数值序（旧码 `sorted(scores.items())` 按名字序，
    # pessimistic_fill / wheat_suppressor 恒被裁端点）。值序对 worst_case /
    # weighted 无行为影响，统一走值序保持单一路径。
    values = sorted(float(v) for v in scores.values())
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
        for name in sorted(scores):    # 确定性遍历（错误信息顺序稳定）
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
    # trimmed_mean：值序每端裁 floor(n×trim_fraction) 个；保证至少留 1 个
    frac = float(trim_fraction)
    if not 0.0 <= frac < 0.5:
        raise ValueError(
            f"trim_fraction={trim_fraction!r} 必须在 [0, 0.5) 内"
            f"（示例：0.5 会裁空两侧）")
    trim = int(math.floor(n * frac))
    trim = min(trim, (n - 1) // 2)      # 至少保留 1 个（n=1 → trim=0）
    kept = values[trim:n - trim] if trim else values
    return sum(kept) / len(kept)
