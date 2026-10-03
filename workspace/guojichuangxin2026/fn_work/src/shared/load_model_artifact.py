"""加载模型工件并校验版本戳与特征名匹配（shared 块）。"""
from __future__ import annotations

import pickle
from pathlib import Path


class ModelArtifactError(Exception):
    """文件缺失/特征不匹配/版本戳缺失；消息带指引。"""


def load_model_artifact(path: str, expected_features: list) -> object:
    """torch checkpoint（state_dict/feature_names/version）或 pickle 分类器；特征集合相等放行。"""
    p = Path(path)
    if not p.exists():
        raise ModelArtifactError(f"模型工件不存在: {path}（先跑 train_tcn 生成）")
    try:
        import torch
    except ImportError:
        torch = None  # noqa: N813

    if p.suffix in (".pt", ".pth"):
        if torch is None:
            raise ModelArtifactError("工件为 torch 格式但环境未装 torch")
        blob = torch.load(p, map_location="cpu", weights_only=False)
        if not isinstance(blob, dict) or "state_dict" not in blob:
            raise ModelArtifactError("torch 工件缺 state_dict")
    else:
        with open(p, "rb") as fh:
            blob = pickle.load(fh)
        blob = blob if isinstance(blob, dict) and "feature_names" in blob else {}
    if not blob.get("version"):
        raise ModelArtifactError(f"工件缺版本戳: {path}")
    if expected_features is not None:
        got, want = set(blob.get("feature_names") or []), set(expected_features)
        if got != want:
            raise ModelArtifactError(f"特征名不匹配: 期望-实际差集 {want - got or '（工件特征被拒）'}")
    return blob
