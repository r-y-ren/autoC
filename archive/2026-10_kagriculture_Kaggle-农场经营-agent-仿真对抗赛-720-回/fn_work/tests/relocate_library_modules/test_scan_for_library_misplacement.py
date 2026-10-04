"""scan_for_library_misplacement 镜像测试：tmp 假树扫描检出（无入口+被 import）/
入口标记三形态豁免/孤立无入口件不检出/点前缀 import 与动态装载引用计数/
缺目录 fail-closed。"""

import pytest

from relocate_library_modules.scan_for_library_misplacement import (
    scan_for_library_misplacement,
)


@pytest.fixture()
def fake_scripts(tmp_path):
    """tmp 假树：三入口形态件+无入口库件（被引/孤立）+消费方。"""
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "entry_main.py").write_text(
        "def main():\n    pass\n\n\nif __name__ == '__main__':\n"
        "    main()\n", encoding="utf-8")
    (scripts / "entry_argparse.py").write_text(
        "import argparse\n\nparser = argparse.ArgumentParser()\n",
        encoding="utf-8")
    (scripts / "library_like.py").write_text(
        "def helper():\n    return 1\n", encoding="utf-8")
    (scripts / "orphan_lib.py").write_text(
        "def unused():\n    return 2\n", encoding="utf-8")
    (scripts / "consumer.py").write_text(
        "import library_like\nfrom library_like import helper\n",
        encoding="utf-8")
    return scripts


def test_detects_entryless_imported_module_only(fake_scripts):
    hits = scan_for_library_misplacement(fake_scripts)
    assert [h["file"] for h in hits] == ["library_like.py"]
    hit = hits[0]
    assert hit["importers"] == ["consumer.py"]
    # 三入口标记全缺位即"无入口"实证
    assert hit["entry_markers"] == {"def main": False, "argparse": False,
                                    "__main__ guard": False}


def test_entry_marker_forms_exempt_and_orphan_not_flagged(fake_scripts):
    names = {h["file"] for h in scan_for_library_misplacement(fake_scripts)}
    # 三种入口形态（def main/argparse/__main__）任一在场即不判库件
    assert "entry_main.py" not in names
    assert "entry_argparse.py" not in names
    # 孤立无入口件（无人 import）不进清单——判据=无入口且被 import
    assert "orphan_lib.py" not in names
    assert "consumer.py" not in names  # 消费方有 import 面，非被引方


def test_dotted_import_and_dynamic_load_count(fake_scripts):
    (fake_scripts / "dotted_consumer.py").write_text(
        "from scripts.library_like import helper\n", encoding="utf-8")
    (fake_scripts / "dyn_loader.py").write_text(
        "spec = load('library_like', root / 'library_like.py')\n",
        encoding="utf-8")
    hits = scan_for_library_misplacement(fake_scripts)
    hit = next(h for h in hits if h["file"] == "library_like.py")
    assert hit["importers"] == ["consumer.py", "dotted_consumer.py",
                                "dyn_loader.py"]


def test_missing_directory_fail_closed(tmp_path):
    with pytest.raises(ValueError, match="不存在或非目录"):
        scan_for_library_misplacement(tmp_path / "nope")
