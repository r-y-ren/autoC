"""单件与总量体积预算断言（预算定桩 B7：单件 ≤2 MiB、总量 ≤10 MiB），
超标抛 SizeBudgetExceeded 并给逐件超标清单，不许静默截断。

上游: R19（详见 fn_docs/responsibility.md）

实现要点：
- 预算定桩（本批 B7 落死，R19"体积预算在定桩时明确"）：PER_FILE_MAX_BYTES=2 MiB、
  TOTAL_MAX_BYTES=10 MiB，写为本模块常量——单件上限护住 ~GB 语料混入（回放/语料
  冻结核永不入最小集），总量上限护住 fresh clone 克隆体积。
- fail-closed：任一单件或总量超标即抛，violations 逐件列出（路径+实测字节+上限），
  绝不裁剪/丢件凑预算（R19"超预算即失败，不许静默截断"）。
- budget 可注入（测试/临时收紧用），None=定桩常量；键名固定
  per_file_max_bytes / total_max_bytes，缺键即按定桩常量取值（不猜）。
"""

from __future__ import annotations

__all__ = [
    "PER_FILE_MAX_BYTES",
    "TOTAL_MAX_BYTES",
    "DEFAULT_BUDGET",
    "SizeBudgetExceeded",
    "enforce_size_budget",
]

# ---- 预算定桩（B7，R19）--------------------------------------------------- #
PER_FILE_MAX_BYTES = 2 * 1024 * 1024   # 单件 ≤ 2 MiB
TOTAL_MAX_BYTES = 10 * 1024 * 1024     # 收集总量 ≤ 10 MiB
# --------------------------------------------------------------------------- #

DEFAULT_BUDGET: dict = {
    "per_file_max_bytes": PER_FILE_MAX_BYTES,
    "total_max_bytes": TOTAL_MAX_BYTES,
    "pinned_in": "fn_work/src/package_minimal_repro_set/enforce_size_budget.py (B7)",
}


class SizeBudgetExceeded(RuntimeError):
    """体积预算超标（fail-closed）：violations 逐件列出，不静默截断。"""

    def __init__(self, violations: list):
        self.violations = violations
        lines = ["最小可复算集体积预算超标（不允许静默截断，收拢超标件后重跑）:"]
        for item in violations:
            if item["kind"] == "per_file":
                lines.append(
                    f"  [单件] {item['source_path']}: {item['size']} bytes "
                    f"> 上限 {item['limit']} bytes")
            else:
                lines.append(
                    f"  [总量] 合计 {item['size']} bytes > 上限 {item['limit']} bytes")
        super().__init__("\n".join(lines))


def enforce_size_budget(file_set: list, budget: dict | None = None) -> list:
    """对 collected 文件集做单件+总量预算断言，通过返回逐件标注清单。

    Args:
        file_set: collect_gate_golden_files 返回的 collected 件登记列表
            （须含 source_path 与 size）。
        budget: 预算 dict；None=定桩常量（单件 2 MiB/总量 10 MiB）。

    Returns:
        逐件标注后的清单（原登记字段 + per_file_ok 布尔 + 预算口径），
        全部通过时才返回。

    Raises:
        SizeBudgetExceeded: 任一单件或总量超标（violations 逐件，不静默截断）。
        KeyError/TypeError: file_set 条目缺 source_path/size（登记不完整，
            fail-closed 不猜）。
    """
    resolved = dict(DEFAULT_BUDGET)
    if budget:
        for key in ("per_file_max_bytes", "total_max_bytes"):
            if key in budget:
                resolved[key] = budget[key]

    violations: list[dict] = []
    annotated: list[dict] = []
    total = 0
    for entry in file_set:
        size = int(entry["size"])
        per_ok = size <= resolved["per_file_max_bytes"]
        if not per_ok:
            violations.append({
                "kind": "per_file",
                "source_path": entry["source_path"],
                "size": size,
                "limit": resolved["per_file_max_bytes"],
            })
        annotated.append({**entry, "per_file_ok": per_ok})
        total += size
    if total > resolved["total_max_bytes"]:
        violations.append({
            "kind": "total",
            "source_path": "<total>",
            "size": total,
            "limit": resolved["total_max_bytes"],
        })

    if violations:
        raise SizeBudgetExceeded(violations)

    return annotated
