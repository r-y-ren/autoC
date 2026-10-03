"""R6 顶层：check_dataset —— runs/ 下全部录制校验 + 数据集索引（按录制分组）。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DatasetIndex:
    recordings: int
    groups: list[str] = field(default_factory=list)   # 录制组（分组 CV 的划分单位）
    errors: list[str] = field(default_factory=list)
    index_path: str = ""


def check_dataset(runs_dir: str) -> DatasetIndex:
    """扫描 runs/ → 校验每条录制 → 产 dataset_index.json（group 字段非空是硬要求）。"""
    raise NotImplementedError("unimplemented:fn:check_dataset")
