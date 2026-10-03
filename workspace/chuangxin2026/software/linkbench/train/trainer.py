"""R7 顶层：train_model —— 谱图分类（七类：六样式+无干扰），分组 CV 评测。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TrainResult:
    model_path: str
    backend: str            # "toolbox" | "local"
    macro_f1: float         # 分组 CV（仅实测回填）
    confusion_png: str
    report_md: str


def train_model(data_dir: str, out_dir: str = "models", *, backend: str = "auto") -> TrainResult:
    """数据集 → 训练 → 分组 CV 评测（混淆矩阵+Macro-F1）→ 模型与报告落盘。"""
    raise NotImplementedError("unimplemented:fn:train_model")


def evaluate(model_path: str, data_dir: str) -> dict:
    """独立评测入口（验收 scripts/eval_jamming_cls.py 调用）：返回分组 CV 指标 dict。"""
    raise NotImplementedError("unimplemented:fn:evaluate")
