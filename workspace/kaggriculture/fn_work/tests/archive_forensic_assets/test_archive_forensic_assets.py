"""archive_forensic_assets 顶层镜像测试：tmp 假树全链编排/注册表 schema/探针失败/
import 面命中与散文豁免/v143 前置未满足/裁决缺件 fail-closed/默认注册表路径推导。"""

import json
from pathlib import Path

import pytest

from archive_forensic_assets.archive_forensic_assets import (
    SCRIPTS_POSTWAR_DIR,
    archive_forensic_assets,
)
from archive_forensic_assets.partition_script_tiers import (
    ADJUDICATED_TIERS,
    TIER_ARCHIVE,
    TIER_RETAIN,
    TIER_TOOLBOX,
)

_OUT_OF_SCOPE = ["run_eval.py", "market_ledger.py"]  # 其他需求管辖（R15/R1-R9）
_ABSORBED = {"absorbed": True, "evidence": "stub: seated 已吸收"}
_PROBE_OK = lambda _p: (True, "stub ok")  # noqa: E731


@pytest.fixture()
def fake_campaign(tmp_path):
    """tmp 假树：software/scripts 26 裁决件（空文件）+2 范围外件；bc models 证据件。"""
    scripts = tmp_path / "software" / "scripts"
    scripts.mkdir(parents=True)
    for name in ADJUDICATED_TIERS:
        (scripts / name).write_text("", encoding="utf-8")
    for name in _OUT_OF_SCOPE:
        (scripts / name).write_text("", encoding="utf-8")
    models = tmp_path / "software" / "bc_track" / "models"
    models.mkdir(parents=True)
    (models / "bc_model_v1.py").write_bytes(b"x" * 10)
    (models / "bc_model_v2.py").write_bytes(b"y" * 20)
    (models / "train_report.json").write_bytes(b"{}")
    return {"campaign": tmp_path, "scripts": scripts, "models": models}


def test_orchestration_pass_registry_schema_and_no_move(fake_campaign):
    verdict = archive_forensic_assets(
        fake_campaign["scripts"], fake_campaign["models"],
        bench_absorption_checker=lambda: _ABSORBED, probe_runner=_PROBE_OK)
    assert verdict["overall"] is True
    assert verdict["counts"] == {TIER_RETAIN: 5, TIER_TOOLBOX: 3, TIER_ARCHIVE: 18,
                                 "bc_models": 3, "out_of_r11_scope": 2}
    assert verdict["out_of_r11_scope"] == sorted(_OUT_OF_SCOPE)
    assert all(p["ok"] for p in verdict["retained_probes"]) \
        and len(verdict["retained_probes"]) == 5
    assert verdict["import_face_clean"] and verdict["import_face_hits"] == []
    assert verdict["bc_models_total_bytes"] == 32

    # 注册表落默认路径（战役根/fn_work/archive_registry.json）且 schema 完整
    registry_path = Path(verdict["registry_path"])
    assert registry_path == fake_campaign["campaign"] / "fn_work" \
        / "archive_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for key in ("contract", "generated_at", "frozen_tree", "postwar_execution",
                "counts", "tiers", "bc_models", "out_of_r11_scope", "verdict"):
        assert key in registry
    assert registry["frozen_tree"] is True
    assert registry["postwar_execution"]["registry_only"] is True
    assert registry["postwar_execution"]["blocked_files"] == []
    assert set(registry["tiers"]) == {TIER_RETAIN, TIER_TOOLBOX, TIER_ARCHIVE}
    for entry in registry["tiers"][TIER_ARCHIVE]:
        assert entry["postwar_dest"] == f"{SCRIPTS_POSTWAR_DIR}/{entry['file']}"
        assert set(entry) == {"file", "tier", "reason", "precondition",
                              "postwar_dest"}
    for tier in (TIER_RETAIN, TIER_TOOLBOX):
        assert all(e["postwar_dest"] is None
                   for e in registry["tiers"][tier])
    for entry in registry["bc_models"]["entries"]:
        assert entry["postwar_dest"].startswith("forensics_archive/bc_models/")

    # 零物理移动：裁决件全在原位、归档区目录未建
    assert all((fake_campaign["scripts"] / n).is_file()
               for n in ADJUDICATED_TIERS)
    assert not (fake_campaign["campaign"] / "forensics_archive").exists()


def test_probe_failure_fails_overall(fake_campaign, tmp_path):
    def failing_probe(path):
        return (False, "exit 2") if path.name == "twin_fidelity.py" \
            else (True, "stub ok")
    verdict = archive_forensic_assets(
        fake_campaign["scripts"], fake_campaign["models"],
        registry_path=tmp_path / "reg.json",
        bench_absorption_checker=lambda: _ABSORBED, probe_runner=failing_probe)
    assert verdict["overall"] is False
    failed = [p for p in verdict["retained_probes"] if not p["ok"]]
    assert [p["file"] for p in failed] == ["twin_fidelity.py"]


def test_import_face_hit_fails_overall(fake_campaign, tmp_path):
    host = fake_campaign["scripts"] / "twin_fidelity.py"
    host.write_text("import v15_h2h_v48\n", encoding="utf-8")
    verdict = archive_forensic_assets(
        fake_campaign["scripts"], fake_campaign["models"],
        registry_path=tmp_path / "reg.json",
        bench_absorption_checker=lambda: _ABSORBED, probe_runner=_PROBE_OK)
    assert verdict["overall"] is False
    assert verdict["import_face_clean"] is False
    assert verdict["import_face_hits"] == [
        {"file": "v15_h2h_v48.py", "referer": "twin_fidelity.py", "line": 1}]
    # 带引号文件名引用（动态装载形态）同样命中
    host.write_text('run("v48plus_metrics.py")\n', encoding="utf-8")
    verdict2 = archive_forensic_assets(
        fake_campaign["scripts"], fake_campaign["models"],
        registry_path=tmp_path / "reg2.json",
        bench_absorption_checker=lambda: _ABSORBED, probe_runner=_PROBE_OK)
    assert verdict2["import_face_hits"][0]["file"] == "v48plus_metrics.py"


def test_docstring_prose_mention_is_not_a_hit(fake_campaign, tmp_path):
    """散文口径提及（docstring 注释）不算依赖——实树 p41 对 stepdiff_probe 仅注释提及。"""
    host = fake_campaign["scripts"] / "p41_official_load_probe.py"
    host.write_text(
        'def f():\n    """动作规范化串（与 round23_dtsp_stepdiff_probe 同口径）。"""\n',
        encoding="utf-8")
    verdict = archive_forensic_assets(
        fake_campaign["scripts"], fake_campaign["models"],
        registry_path=tmp_path / "reg.json",
        bench_absorption_checker=lambda: _ABSORBED, probe_runner=_PROBE_OK)
    assert verdict["import_face_clean"] is True
    assert verdict["overall"] is True


def test_v143_precondition_unmet_refuses_archive(fake_campaign, tmp_path):
    unmet = {"absorbed": False, "evidence": "stub: 未吸收"}
    verdict = archive_forensic_assets(
        fake_campaign["scripts"], fake_campaign["models"],
        registry_path=tmp_path / "reg.json",
        bench_absorption_checker=lambda: unmet, probe_runner=_PROBE_OK)
    assert verdict["overall"] is False
    assert verdict["v143_precondition"]["absorbed"] is False
    assert "拒绝" in verdict["summary"]
    registry = json.loads(
        Path(verdict["registry_path"]).read_text(encoding="utf-8"))
    assert registry["postwar_execution"]["blocked_files"] == \
        ["v143_sellrace_gates.py"]
    # 拒绝归档 v143 ≠ 改动裁决档位：归档档仍 18 件（含 v143），封锁在执行面
    assert verdict["counts"][TIER_ARCHIVE] == 18


def test_missing_adjudicated_file_fail_closed(fake_campaign):
    (fake_campaign["scripts"] / "profile_v48_gap.py").unlink()
    with pytest.raises(ValueError, match="profile_v48_gap.py"):
        archive_forensic_assets(
            fake_campaign["scripts"], fake_campaign["models"],
            bench_absorption_checker=lambda: _ABSORBED, probe_runner=_PROBE_OK)


def test_default_probe_runner_executes_help(fake_campaign, tmp_path):
    """默认探针=子进程 `python <script> --help`；空脚本 exit 0 即可跑。"""
    verdict = archive_forensic_assets(
        fake_campaign["scripts"], fake_campaign["models"],
        registry_path=tmp_path / "reg.json",
        bench_absorption_checker=lambda: _ABSORBED)
    assert verdict["overall"] is True
    for probe_result in verdict["retained_probes"]:
        assert probe_result["ok"] is True
        assert "(--help)" in probe_result["detail"]
