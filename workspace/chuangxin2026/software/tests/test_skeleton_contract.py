"""骨架契约元测试：编译全过 + 桩标记统一 + scripts 验收入口存在。"""

from __future__ import annotations

import compileall
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # software/


def test_all_py_compile():
    assert compileall.compile_dir(str(ROOT / "linkbench"), quiet=1) is True


def test_stub_markers_present_and_greppable():
    hits = [p for p in (ROOT / "linkbench").rglob("*.py")
            if "unimplemented:fn:" in p.read_text(encoding="utf-8")]
    assert len(hits) >= 25, "桩标记锚点应覆盖全部业务文件"


def test_js_stub_markers():
    for js in ("app.js", "anim.js"):
        text = (ROOT / "linkbench" / "ui" / "static" / js).read_text(encoding="utf-8")
        assert "unimplemented:fn:" in text


def test_acceptance_entrypoints_exist():
    for rel in ("smoke_boot.py", "ui_selftest.py",
                "scripts/run_scenario.py", "scripts/check_dataset.py",
                "scripts/eval_jamming_cls.py", "scripts/demo.py"):
        assert (ROOT / rel).exists(), rel


def test_scenario_fixtures_exist():
    names = {"smoke.yaml", "smoke_loop.yaml", "gb42590_noise.yaml", "nojam_control.yaml"}
    found = {p.name for p in (ROOT / "scenarios").glob("*.yaml")}
    assert names <= found
