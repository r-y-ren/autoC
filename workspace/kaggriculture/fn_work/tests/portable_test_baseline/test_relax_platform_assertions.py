"""relax_platform_assertions 真实测试：双平台断言语义（normcase 封装/is_absolute）、扫描器检出注入用例、修正器锚定改写与写入许可策略。"""

import pytest

from portable_test_baseline.relax_platform_assertions import (
    assert_paths_equal,
    fold_path,
    is_absolute_cross_platform,
    is_windows_drive_path,
    paths_equivalent,
    relax_platform_assertions,
    scan_windows_only_patterns,
)

# --------------------------------------------------------------------------- #
# 双平台断言语义
# --------------------------------------------------------------------------- #

def test_fold_path_and_equivalence():
    # normcase 双平台封装：大小写不敏感 + 分隔符规范，两平台同一语义
    assert paths_equivalent("C:/tmp/EVAL_RESULTS.JSON", "c:\\tmp\\eval_results.json")
    assert paths_equivalent("Data/Foo.JSON", "data/foo.json")
    assert not paths_equivalent("C:/tmp/a.json", "C:/tmp/b.json")
    assert fold_path("A\\B\\C") == "a/b/c"
    assert fold_path("MiXeD/Case") == "mixed/case"


def test_assert_paths_equal_raises_with_detail():
    assert_paths_equal("X/Y", "x/y")  # 等价不抛
    with pytest.raises(AssertionError, match="C:/a"):
        assert_paths_equal("C:/a.json", "C:/b.json", "prefix C:/a mismatch")


def test_is_absolute_cross_platform():
    # Windows-only 断言面：盘符/UNC 一律绝对（补 POSIX 缺失语义），双平台一致
    assert is_absolute_cross_platform("C:/tmp/out.json") is True
    assert is_absolute_cross_platform("C:\\tmp\\out.json") is True
    assert is_absolute_cross_platform(r"\\server\share\f.json") is True
    assert is_windows_drive_path("D:/x") is True
    assert is_windows_drive_path("/x") is False
    # 相对路径双平台一致为假
    assert is_absolute_cross_platform("rel/path.json") is False
    assert is_absolute_cross_platform("out.json") is False


# --------------------------------------------------------------------------- #
# 扫描器：注入用例检出 + 干净树零命中
# --------------------------------------------------------------------------- #

@pytest.fixture()
def injected_tests_tree(tmp_path):
    # 注入内容经字符串拼接构造：本测试文件自身不得命中扫描器 token（自指防御）
    root = tmp_path / "tests"
    root.mkdir()
    (root / "test_normcase_style.py").write_text(
        "import os\n"
        "\n"
        "def test_paths():\n"
        "    p1, p2 = 'C:/tmp/A.JSON', 'c:/tmp/a.json'\n"
        "    assert os.path." + "normcase(str(p1)) == os.path." +
        "normcase(str(p2))\n",
        encoding="utf-8")
    (root / "test_drive_abs_style.py").write_text(
        "from pathlib import Path\n"
        "\n"
        "def test_out_path():\n"
        "    assert Path('C:/windows" + "/temp/evil.json').is_abs" +
        "olute()\n",
        encoding="utf-8")
    (root / "test_platform_branch.py").write_text(
        "import sys\n"
        "\n"
        "def test_branch():\n"
        "    if sys." + "platform == 'win32':\n"
        "        assert True\n",
        encoding="utf-8")
    (root / "test_clean.py").write_text(
        "from portable_test_baseline.relax_platform_assertions import paths_equivalent\n"
        "\n"
        "def test_ok():\n"
        "    assert paths_equivalent('A/b', 'a/B')\n",
        encoding="utf-8")
    (root / "commented_only.py").write_text(
        "# os.path." + "normcase mentioned in comment only\n"
        "# if sys." + "platform == 'win32': pass\n",
        encoding="utf-8")
    return root


def test_scanner_detects_injected_cases(injected_tests_tree):
    report = scan_windows_only_patterns(injected_tests_tree)
    kinds = {(hit["file"], hit["kind"]) for hit in report["hits"]}
    assert ("test_normcase_style.py", "normcase_fold") in kinds
    assert ("test_drive_abs_style.py", "windows_drive_is_absolute") in kinds
    assert ("test_platform_branch.py", "sys_platform_branch") in kinds
    assert report["hit_count"] == 3
    assert report["files_scanned"] == 5  # 注入 4 件 + 注释件（注释行不计命中）
    # 命中带行号与整改提示
    norm_hit = next(h for h in report["hits"] if h["kind"] == "normcase_fold")
    assert norm_hit["line"] == 5
    assert "paths_equivalent" in norm_hit["remediation"]


def test_scanner_clean_tree_zero_hits(tmp_path):
    (tmp_path / "test_fine.py").write_text(
        "def test_ok():\n    assert 1 + 1 == 2\n", encoding="utf-8")
    report = scan_windows_only_patterns(tmp_path)
    assert report["hit_count"] == 0
    assert report["hits"] == []


def test_scanner_rejects_missing_root(tmp_path):
    with pytest.raises(NotADirectoryError):
        scan_windows_only_patterns(tmp_path / "nope")


# --------------------------------------------------------------------------- #
# 修正器：锚定改写（monkeypatch 许可面）+ 默认策略只报告不改写
# --------------------------------------------------------------------------- #

def test_fixer_rewrites_canonical_shapes(injected_tests_tree, monkeypatch):
    import portable_test_baseline.relax_platform_assertions as mod
    monkeypatch.setattr(mod, "_fixes_allowed", lambda root: True)

    report = relax_platform_assertions(injected_tests_tree, apply_fixes=True)
    assert report["writes_allowed"] is True
    assert report["fixed"] == 2
    # sys.platform 分支不自动改写 → 残留
    assert report["residual"] == 1
    assert report["residual_hits"][0]["kind"] == "sys_platform_branch"
    # 逐处登记
    fixed_kinds = sorted(r["kind"] for r in report["fixes_applied"])
    assert fixed_kinds == ["normcase_fold", "windows_drive_is_absolute"]

    norm_src = (injected_tests_tree / "test_normcase_style.py").read_text(encoding="utf-8")
    assert "paths_equivalent(p1, p2)" in norm_src
    assert "import os\n" in norm_src  # 原 import 保留，仅断言形态改写
    assert mod._UTILITY_IMPORT in norm_src
    drive_src = (injected_tests_tree / "test_drive_abs_style.py").read_text(encoding="utf-8")
    assert "is_absolute_cross_platform('C:/windows/temp/evil.json')" in drive_src
    # 改写后仍可编译（修正器内语法门），行为双平台等价
    compile(drive_src, "drive", "exec")
    # 改写后再扫描：normcase/is_absolute 命中归零，仅剩 sys.platform 分支
    rescan = scan_windows_only_patterns(injected_tests_tree)
    assert [h["kind"] for h in rescan["hits"]] == ["sys_platform_branch"]


def test_fixer_write_policy_blocks_tmp_roots(injected_tests_tree):
    # 默认策略：扫描根不在 fn_work/tests 内 → 只报告不改写
    before = (injected_tests_tree / "test_normcase_style.py").read_text(encoding="utf-8")
    report = relax_platform_assertions(injected_tests_tree, apply_fixes=True)
    assert report["writes_allowed"] is False
    assert report["fixed"] == 0
    assert report["residual"] == 3
    assert (injected_tests_tree / "test_normcase_style.py").read_text(encoding="utf-8") == before


def test_default_reports_only_when_no_hits(tmp_path):
    (tmp_path / "t.py").write_text("def test_x():\n    assert True\n", encoding="utf-8")
    report = relax_platform_assertions(tmp_path, apply_fixes=False)
    assert report["scan"]["hit_count"] == 0
    assert report["residual"] == 0
