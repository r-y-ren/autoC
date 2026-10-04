"""relocate_library_modules 顶层镜像测试：tmp 假战役树全链编排（扫描检出+建库位
roundtrip+改线注册落盘）/零物理移动/G17 缺件 fail-closed/副本断链（语法坏）
fail-closed。"""

import importlib.util
import json
from pathlib import Path

import pytest

from relocate_library_modules.relocate_library_modules import (
    LIB_MODULE,
    LIB_PUBLIC_NAMES,
    NEW_IMPORT_MODULE,
    REGISTRY_NAME,
    relocate_library_modules,
)

_FAKE_LEDGER = '''"""Fake vendored ledger library (G17 stand-in, no entry)."""
from __future__ import annotations


class OfficialMarketLedger:
    def rows(self):
        return []


def make_ledger_runner(seed=None):
    return OfficialMarketLedger()


def summarize(ledger):
    return {}
'''


@pytest.fixture()
def fake_campaign(tmp_path):
    """tmp 假战役树：blueprint.md+fn_docs 特征、software/scripts（G17 件+消费方
    +入口件）、software/tests path 装载消费方、fn_work 库位与注册表落点。"""
    campaign = tmp_path / "kaggriculture"
    scripts = campaign / "software" / "scripts"
    tests = campaign / "software" / "tests"
    for d in (scripts, tests, campaign / "fn_docs"):
        d.mkdir(parents=True)
    (campaign / "blueprint.md").write_text("# fake\n", encoding="utf-8")
    (scripts / LIB_MODULE).write_text(_FAKE_LEDGER, encoding="utf-8")
    (scripts / "sell_plan_reconciliation.py").write_text(
        "import argparse\n"
        "from scripts.market_ledger import OfficialMarketLedger\n",
        encoding="utf-8")
    (scripts / "run_eval.py").write_text(
        "import argparse\nif __name__ == '__main__':\n    pass\n",
        encoding="utf-8")
    (tests / "test_market_reconciliation_ledger.py").write_text(
        'LEDGER = _load("market_ledger", SOFTWARE / "scripts" / '
        f'"{LIB_MODULE}")\n', encoding="utf-8")
    library_dir = campaign / "fn_work" / "src" / "relocate_library_modules"
    return {"campaign": campaign, "scripts": scripts, "tests": tests,
            "library_dir": library_dir,
            "registry_path": campaign / "fn_work" / REGISTRY_NAME}


def test_orchestration_library_roundtrip_and_registry(fake_campaign):
    fc = fake_campaign
    verdict = relocate_library_modules(
        fc["scripts"], library_dir=fc["library_dir"],
        registry_path=fc["registry_path"])

    assert verdict["overall"] is True
    assert verdict["market_ledger_detected"] is True
    # 扫描裁决：G17 件在列，入口件不误报
    misplaced_files = [e["file"] for e in verdict["scan"]["misplaced"]]
    assert LIB_MODULE in misplaced_files
    assert "run_eval.py" not in misplaced_files \
        and "sell_plan_reconciliation.py" not in misplaced_files
    assert verdict["additional_misplaced"] == []

    # 建库位 roundtrip：逐字节副本+按 path 装载公开名全在场
    copy_path = fc["library_dir"] / LIB_MODULE
    source = fc["scripts"] / LIB_MODULE
    assert copy_path.is_file()
    assert copy_path.read_bytes() == source.read_bytes()
    assert verdict["library"]["byte_equal"] is True
    assert verdict["library"]["sha256_source"] == verdict["library"]["sha256_copy"]
    assert verdict["library"]["new_import_module"] == NEW_IMPORT_MODULE
    spec = importlib.util.spec_from_file_location("mirror_copy", copy_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert all(hasattr(module, n) for n in LIB_PUBLIC_NAMES)

    # 零物理移动：源件原位在树，未被删改
    assert source.is_file() and source.read_text(encoding="utf-8") == _FAKE_LEDGER

    # 改线注册：两消费方（import 语句+path 装载引用）逐条带行号
    consumers = {(c["file"], c["kind"]): c for c in verdict["consumers"]}
    recon = consumers[("software/scripts/sell_plan_reconciliation.py",
                       "import语句")]
    assert recon["line"] == 2
    ledger_test = consumers[(
        "software/tests/test_market_reconciliation_ledger.py", "文件名引用")]
    assert ledger_test["line"] == 1

    # 注册表落盘与 schema
    assert Path(verdict["registry_path"]) == fc["registry_path"]
    registry = json.loads(fc["registry_path"].read_text(encoding="utf-8"))
    for key in ("contract", "generated_at", "frozen_tree", "library",
                "rewiring", "consumers", "scan", "additional_misplaced",
                "postwar_execution", "verdict"):
        assert key in registry
    assert registry["frozen_tree"] is True
    assert registry["rewiring"]["new_import_module"] == NEW_IMPORT_MODULE
    assert registry["library"]["dest"] == (
        "fn_work/src/relocate_library_modules/market_ledger.py")
    steps = registry["postwar_execution"]["steps"]
    assert any("git mv" in s for s in steps)
    assert any("R15 验收" in s for s in steps)


def test_g17_source_fact_violation_fail_closed(fake_campaign):
    fc = fake_campaign
    (fc["scripts"] / LIB_MODULE).unlink()  # G17 件缺位=源事实漂移
    with pytest.raises(ValueError, match="G17 源事实核验失败"):
        relocate_library_modules(fc["scripts"], library_dir=fc["library_dir"],
                                 registry_path=fc["registry_path"])
    # fail-closed 先行：库位副本与注册表均未落盘
    assert not (fc["library_dir"] / LIB_MODULE).exists()
    assert not fc["registry_path"].exists()


def test_broken_copy_chain_fail_closed(fake_campaign):
    fc = fake_campaign
    (fc["scripts"] / LIB_MODULE).write_text(
        "def broken(:\n", encoding="utf-8")  # 语法坏件：复制后 import 回探断链
    with pytest.raises(ValueError, match="断链即失败"):
        relocate_library_modules(fc["scripts"], library_dir=fc["library_dir"],
                                 registry_path=fc["registry_path"])
