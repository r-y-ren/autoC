"""Zero-extend token-adapter kernels when feature names are appended to an adapter."""

from __future__ import annotations

from typing import Any

import jax
import numpy as np

from kaggriculture.observations.features import TOKEN_ADAPTER_FEATURES

ADAPTER_ROWS = {token_type: len(names) for token_type, names in TOKEN_ADAPTER_FEATURES.items()}


def _adapter_kernel_type(path: tuple) -> str | None:
    keys = [getattr(entry, "key", None) for entry in path]
    for index, key in enumerate(keys):
        if key == "adapters" and index + 2 < len(keys) and keys[index + 2] == "kernel":
            return str(keys[index + 1])
    return None


def adapter_rows(tree: Any) -> dict[str, int]:
    """Current input-row counts of every adapter kernel in a parameter-shaped tree."""
    rows: dict[str, int] = {}
    for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
        token_type = _adapter_kernel_type(path)
        if token_type is not None and getattr(leaf, "ndim", 0) == 2:
            rows[token_type] = int(leaf.shape[0])
    return rows


def expand_adapter_kernels(tree: Any, target_rows: dict[str, int] | None = None) -> Any:
    """Pad adapter kernels (and any Adam moment or accumulator shaped like them) with zero rows.

    New feature columns are appended to the end of each adapter's feature list, so appended zero
    rows leave every existing output unchanged until training moves them.
    """
    target_rows = ADAPTER_ROWS if target_rows is None else target_rows

    def pad(path: tuple, leaf: Any) -> Any:
        token_type = _adapter_kernel_type(path)
        if token_type is None or getattr(leaf, "ndim", 0) != 2:
            return leaf
        target = target_rows[token_type]
        current = int(leaf.shape[0])
        if current == target:
            return leaf
        if current > target:
            raise ValueError(f"{token_type} adapter has {current} rows, more than the {target} features")
        array = np.asarray(leaf)
        padded = np.zeros((target, array.shape[1]), dtype=array.dtype)
        padded[:current] = array
        return padded

    return jax.tree_util.tree_map_with_path(pad, tree)
