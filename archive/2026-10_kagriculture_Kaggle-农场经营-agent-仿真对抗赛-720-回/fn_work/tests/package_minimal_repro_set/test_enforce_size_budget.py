"""enforce_size_budget 真实测试：定桩常量口径（2 MiB/10 MiB）、通过返回逐件标注、
单件/总量超标 fail-closed 抛（violations 逐件、消息含路径）、预算注入收紧、
空集通过。"""

import pytest

from package_minimal_repro_set.enforce_size_budget import (
    DEFAULT_BUDGET,
    PER_FILE_MAX_BYTES,
    TOTAL_MAX_BYTES,
    SizeBudgetExceeded,
    enforce_size_budget,
)


def _entry(path: str, size: int) -> dict:
    return {"category": "twin_fidelity_manifest", "source_path": path,
            "dest_path": f"fn_work/minimal_repro_set/x/{path}",
            "sha256": "0" * 64, "size": size, "status": "collected"}


def test_budget_pinned_constants():
    assert PER_FILE_MAX_BYTES == 2 * 1024 * 1024        # 单件 ≤ 2 MiB（B7 定桩）
    assert TOTAL_MAX_BYTES == 10 * 1024 * 1024          # 总量 ≤ 10 MiB（B7 定桩）
    assert DEFAULT_BUDGET["per_file_max_bytes"] == PER_FILE_MAX_BYTES
    assert DEFAULT_BUDGET["total_max_bytes"] == TOTAL_MAX_BYTES
    assert "B7" in DEFAULT_BUDGET["pinned_in"]


def test_within_budget_returns_annotated_list():
    file_set = [_entry("a.json", 100), _entry("b.md", 4096)]
    result = enforce_size_budget(file_set)
    assert [r["per_file_ok"] for r in result] == [True, True]
    assert result[0]["source_path"] == "a.json"
    assert len(result) == len(file_set)                 # 无增删（不截断）


def test_single_file_over_limit_fails_closed_with_listing():
    big = 2 * 1024 * 1024 + 1
    file_set = [_entry("small.json", 10), _entry("golden_v138.json", big)]
    with pytest.raises(SizeBudgetExceeded) as excinfo:
        enforce_size_budget(file_set)
    violations = excinfo.value.violations
    assert len(violations) == 1 and violations[0]["kind"] == "per_file"
    assert violations[0]["source_path"] == "golden_v138.json"
    assert violations[0]["size"] == big
    assert violations[0]["limit"] == PER_FILE_MAX_BYTES
    assert "golden_v138.json" in str(excinfo.value)     # 消息逐件列出
    assert "单件" in str(excinfo.value)


def test_total_over_limit_with_small_files():
    per_file = 1024 * 1024                              # 每件 1 MiB：单件全合规
    file_set = [_entry(f"part{i}.json", per_file) for i in range(11)]  # 合计 11 MiB
    with pytest.raises(SizeBudgetExceeded) as excinfo:
        enforce_size_budget(file_set)
    kinds = {v["kind"] for v in excinfo.value.violations}
    assert kinds == {"total"}
    assert excinfo.value.violations[0]["size"] == 11 * 1024 * 1024
    assert "总量" in str(excinfo.value)


def test_injected_tighter_budget_enforced():
    file_set = [_entry("a.json", 200)]
    with pytest.raises(SizeBudgetExceeded) as excinfo:
        enforce_size_budget(file_set, {"per_file_max_bytes": 100})
    assert excinfo.value.violations[0]["limit"] == 100
    # 部分注入：只收单件上限，总量沿用定桩
    result = enforce_size_budget(file_set, {"per_file_max_bytes": 1000})
    assert result[0]["per_file_ok"] is True


def test_empty_set_passes():
    assert enforce_size_budget([]) == []
