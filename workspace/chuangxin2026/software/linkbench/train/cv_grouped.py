"""分组交叉验证：按录制组划分（防段级泄漏，arXiv:2607.01025 实证教训）。"""

from __future__ import annotations


def grouped_split(index_path: str, n_splits: int = 5) -> list[tuple[list[str], list[str]]]:
    """dataset_index.json → [(train_groups, test_groups)] × n_splits；
    同一录制的相邻窗口只允许落在同一侧。"""
    raise NotImplementedError("unimplemented:fn:grouped_split")
