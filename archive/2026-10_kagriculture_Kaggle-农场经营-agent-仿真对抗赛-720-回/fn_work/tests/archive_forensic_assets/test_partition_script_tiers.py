"""partition_script_tiers 镜像测试：三档划分计数/条目 schema/未分类拒/重复拒/路径归一。"""

import pytest

from archive_forensic_assets.partition_script_tiers import (
    ADJUDICATED_TIERS,
    TIER_ARCHIVE,
    TIER_RETAIN,
    TIER_TOOLBOX,
    partition_script_tiers,
)


def test_full_adjudicated_partition_counts_and_schema():
    result = partition_script_tiers(ADJUDICATED_TIERS.keys())
    assert result["counts"] == {TIER_RETAIN: 5, TIER_TOOLBOX: 3, TIER_ARCHIVE: 18}
    assert len(result["entries"]) == 26
    for entry in result["entries"]:
        assert set(entry) == {"file", "tier", "reason", "precondition"}
        assert entry["tier"] in (TIER_RETAIN, TIER_TOOLBOX, TIER_ARCHIVE)
        assert entry["reason"]
        ruling = ADJUDICATED_TIERS[entry["file"]]
        assert entry["tier"] == ruling["tier"]
        assert entry["precondition"] == ruling["precondition"]
    # 唯一带前置件 = v143（W3 依赖 W1 的波间契约）
    with_precond = [e for e in result["entries"] if e["precondition"]]
    assert [e["file"] for e in with_precond] == ["v143_sellrace_gates.py"]
    assert with_precond[0]["precondition"] == "run_official_bench 已吸收 seated（B3 完成）"


def test_unclassified_script_rejected_fail_closed():
    with pytest.raises(ValueError) as excinfo:
        partition_script_tiers(["twin_fidelity.py", "not_in_manifest.py",
                                "another_stranger.py"])
    message = str(excinfo.value)
    assert "未分类件 2 件" in message
    assert "another_stranger.py" in message and "not_in_manifest.py" in message


def test_duplicate_script_rejected():
    with pytest.raises(ValueError, match="重复件"):
        partition_script_tiers(["twin_fidelity.py", "twin_fidelity.py"])


def test_path_forms_normalized_to_basename():
    result = partition_script_tiers(
        ["/some/where/software/scripts/twin_fidelity.py",
         "relative/path/v143_sellrace_gates.py"])
    assert result["counts"][TIER_RETAIN] == 1
    assert result["counts"][TIER_ARCHIVE] == 1
    assert {e["file"] for e in result["entries"]} == {
        "twin_fidelity.py", "v143_sellrace_gates.py"}
