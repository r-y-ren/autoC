"""共形校准：点概率→90% 覆盖率区间（纯查表）（run_progressive_risk 块）。"""
from __future__ import annotations


class ConformalError(Exception):
    """校准表缺失/口径不符。"""


def calibrate_conformal(prediction: dict, quantiles: dict) -> dict:
    """quantiles: {"1": q1, "3": q3, ...}（留出集非一致性分数分位数）。

    输出逐 horizon 区间 [max(0,p−q), min(1,p+q)] 与宽度；覆盖目标由分位数口径蕴含。
    """
    if not quantiles:
        raise ConformalError("校准分位数表缺失（先在留出集上计算）")
    out = {}
    for hz_s, p in prediction["probs"].items():
        if hz_s not in quantiles:
            raise ConformalError(f"horizon {hz_s}s 无校准分位数")
        q = float(quantiles[hz_s])
        p = float(p)
        out[hz_s] = {"prob": p, "lo": max(0.0, p - q), "hi": min(1.0, p + q),
                     "width": min(1.0, p + q) - max(0.0, p - q)}
    return {"intervals": out,
            "time_to_unsafe_s": prediction.get("time_to_unsafe_s")}
