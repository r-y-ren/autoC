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


class OnlineCalibrator:
    """R18 在线自适应共形（ACI 口径）：滑窗漂移检验触发分位数刷新；静态/自适应双态可配。

    用法：在线模式下把每次实现的非一致性分数喂 update()；drift 检出（滑窗均值偏移>阈）
    则对分位数做加权刷新（上浮抗漂移）；quantiles() 取当前表喂 calibrate_conformal。
    """

    def __init__(self, base_quantiles: dict, drift_window: int = 30,
                 drift_ratio: float = 0.35, alpha: float = 0.1):
        self.q = dict(base_quantiles)
        self.win, self.ratio, self.alpha = [], drift_ratio, alpha
        self.window_n = drift_window
        self.drift_events = 0

    def update(self, scores):
        """scores: 本批非一致性分数（|y−pred| 口径）；返回是否发生漂移刷新。"""
        import numpy as np
        self.win = (self.win + list(scores))[-self.window_n:]
        if len(self.win) < self.window_n // 2:
            return False
        arr = np.asarray(self.win)
        half = len(arr) // 2
        old_m, new_m = float(arr[:half].mean()), float(arr[half:].mean())
        base = max(old_m, 1e-6)
        if (new_m - old_m) / base > self.ratio:      # 漂移检出
            # 重校准语义：分位数抬到近期经验分位（只升不降，追得上噪声跳变）
            emp = float(np.quantile(arr, 1.0 - self.alpha))
            self.q = {k: min(0.5, max(v, emp)) for k, v in self.q.items()}
            self.drift_events += 1
            self.win = self.win[half:]               # 重置基线窗
            return True
        return False

    def quantiles(self):
        return dict(self.q)
