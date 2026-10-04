"""双平台断言工具（路径等价 normcase 语义封装 / is_absolute 跨平台判断）+ fn_work/tests 全树 Windows-only 模式扫描与修正。

上游: R6, R20（详见 fn_docs/responsibility.md）

实现要点：
- 源事实：旧树 2 处 Windows-only 断言语义——os.path.normcase 仅 Windows 折叠
  大小写与斜杠（POSIX 恒等），据此断言"大小写不敏感等价"在 POSIX 必挂；
  Path("C:/…").is_absolute() 在 Windows 真、POSIX 假（无盘符概念）。旧树只读
  不可改，本模块给出 fn_work 测试可用的双平台等价语义，并扫描 fn_work/tests
  全树检出残留 Windows-only 模式（检出器三类：normcase 折叠断言、盘符字面量
  is_absolute、sys.platform/os.name 分支），命中者改用工具（fn_work 内可改）。
- fold_path = 分隔符规范（\\→/）+ casefold：在两平台给出同一语义（Windows
  口径），使大小写不敏感等价断言双平台行为一致——这是对 normcase 的可移植
  封装，而非平台各自为政。
- is_absolute_cross_platform：盘符（^[A-Za-z]:[\\/]）或 UNC（\\\\…）路径一律
  判绝对（补齐 POSIX 上缺失的 Windows 语义）；其余走平台原生 Path.is_absolute
  （POSIX 绝对路径语义双平台本就不必强求一致，本工具只钉 Windows-only 断言面）。
- 修正器（apply_fixes=True）仅对两处典则形态做锚定改写：
  os.path.normcase(str(X)) == os.path.normcase(str(Y)) → paths_equivalent(X, Y)；
  Path("C:/…").is_absolute() → is_absolute_cross_platform("C:/…")。改写后
  compile() 语法门，失败即整文件回滚并登记；sys.platform 分支不自动改写
  （需人工双分支设计），留在 residual_hits。逐处登记（file/line/old/new）。
- 写入安全：默认仅当扫描根位于 <战役根>/fn_work/tests 内才允许落盘改写；
  其余根（含测试注入的 tmp 树）只扫描报告不写。
"""

from __future__ import annotations

import re
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = [
    "fold_path",
    "paths_equivalent",
    "assert_paths_equal",
    "is_windows_drive_path",
    "is_absolute_cross_platform",
    "WINDOWS_ONLY_DETECTORS",
    "scan_windows_only_patterns",
    "relax_platform_assertions",
]

_WIN_DRIVE_RE = re.compile(r"^[A-Za-z]:[/\\]")
_DRIVE_LITERAL_RE = re.compile(r"""["'][A-Za-z]:[/\\][^"']*["']""")
_PATH_DRIVE_CALL_RE = re.compile(r"""Path\(\s*(["'][A-Za-z]:[/\\][^"']*["'])\s*\)\s*\.\s*is_absolute\s*\(\s*\)""")
_NORMCASE_EQ_RE = re.compile(
    r"os\.path\.normcase\(\s*str\(\s*(?P<a>.+?)\s*\)\s*\)\s*==\s*"
    r"os\.path\.normcase\(\s*str\(\s*(?P<b>.+?)\s*\)\s*\)")

# 检出器三类：normcase 折叠断言 / 盘符字面量 is_absolute / 平台分支
WINDOWS_ONLY_DETECTORS = {
    "normcase_fold": {
        "pattern": re.compile(r"\bos\.path\.normcase\b|\bfrom\s+ntpath\s+import\b|\bntpath\.normcase\b"),
        "remediation": "os.path.normcase 在 POSIX 为恒等——等价断言改用 paths_equivalent/assert_paths_equal（双平台同语义）",
    },
    "windows_drive_is_absolute": {
        "pattern": None,  # 组合判定：同行 .is_absolute( 与 盘符字面量
        "literal": _DRIVE_LITERAL_RE,
        "call": re.compile(r"\.is_absolute\s*\("),
        "remediation": "Path(\"C:/…\").is_absolute() 仅 Windows 为真——改用 is_absolute_cross_platform（补盘符/UNC 语义）",
    },
    "sys_platform_branch": {
        "pattern": re.compile(r"\bsys\.platform\s*==|\bos\.name\s*==|\bsys\.platform\s*!="),
        "remediation": "平台分支需双平台各自可达的设计（或 skipif 标注），不能仅单平台断言；不自动改写，留人工",
    },
}

_UTILITY_IMPORT = (
    "from portable_test_baseline.relax_platform_assertions import ("
    "is_absolute_cross_platform, paths_equivalent)")


def fold_path(path) -> str:
    """可移植 normcase 等价折叠：分隔符规范（\\→/）+ casefold（双平台同语义）。"""
    return str(path).replace("\\", "/").casefold()


def paths_equivalent(left, right) -> bool:
    """路径等价判断（normcase 语义封装）：大小写不敏感+分隔符规范，双平台一致。"""
    return fold_path(left) == fold_path(right)


def assert_paths_equal(left, right, msg: str | None = None) -> None:
    """断言路径等价（normcase 口径）——替代 POSIX 上失效的 normcase 相等断言。"""
    if not paths_equivalent(left, right):
        raise AssertionError(
            msg or f"路径不等价（normcase 口径）: {left!r} != {right!r}")


def is_windows_drive_path(path) -> bool:
    """盘符（C:/ C:\\）或 UNC（\\\\server\\share）路径形态判定（平台无关）。"""
    text = str(path)
    return bool(_WIN_DRIVE_RE.match(text)) or text.startswith("\\\\")


def is_absolute_cross_platform(path) -> bool:
    """绝对路径判断的双平台口径：盘符/UNC 一律绝对，其余走平台原生语义。"""
    if is_windows_drive_path(path):
        return True
    return Path(str(path)).is_absolute()


def _detect_line(line: str) -> str | None:
    detector = WINDOWS_ONLY_DETECTORS["normcase_fold"]
    if detector["pattern"].search(line):
        return "normcase_fold"
    drive = WINDOWS_ONLY_DETECTORS["windows_drive_is_absolute"]
    if drive["literal"].search(line) and drive["call"].search(line):
        return "windows_drive_is_absolute"
    platform_det = WINDOWS_ONLY_DETECTORS["sys_platform_branch"]
    if platform_det["pattern"].search(line):
        return "sys_platform_branch"
    return None


def scan_windows_only_patterns(tests_root) -> dict:
    """扫描测试树检出 Windows-only 断言模式（三类检出器，逐行命中留档）。"""
    root = Path(tests_root)
    if not root.is_dir():
        raise NotADirectoryError(f"扫描根不是目录: {root}")
    hits = []
    files_scanned = 0
    for py in sorted(root.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        files_scanned += 1
        text = py.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            kind = _detect_line(line)
            if kind is not None:
                hits.append({
                    "file": py.resolve().relative_to(root.resolve()).as_posix(),
                    "line": lineno,
                    "kind": kind,
                    "text": stripped,
                    "remediation": WINDOWS_ONLY_DETECTORS[kind]["remediation"],
                })
    return {
        "tests_root": str(root),
        "files_scanned": files_scanned,
        "hit_count": len(hits),
        "hits": hits,
    }


def _rewrite_source(source: str) -> tuple[str, list[dict]]:
    """两处典则形态的锚定改写（逐处登记），不动其他字节。"""
    fixes = []

    def _normcase_sub(match: re.Match) -> str:
        fixes.append({"kind": "normcase_fold",
                      "old": match.group(0),
                      "new": f"paths_equivalent({match.group('a')}, {match.group('b')})"})
        return f"paths_equivalent({match.group('a')}, {match.group('b')})"

    def _drive_sub(match: re.Match) -> str:
        fixes.append({"kind": "windows_drive_is_absolute",
                      "old": match.group(0),
                      "new": f"is_absolute_cross_platform({match.group(1)})"})
        return f"is_absolute_cross_platform({match.group(1)})"

    source = _NORMCASE_EQ_RE.sub(_normcase_sub, source)
    source = _PATH_DRIVE_CALL_RE.sub(_drive_sub, source)
    return source, fixes


def _insert_utility_import(source: str) -> str:
    """在文件头部 import 区末尾插入工具 import（无 import 时插在 docstring 后）。"""
    if _UTILITY_IMPORT in source:
        return source
    lines = source.splitlines(keepends=True)
    last_import = None
    for idx, line in enumerate(lines[:120]):
        if line.startswith(("import ", "from ")):
            last_import = idx
    if last_import is None:
        # 无 import：插在模块 docstring 之后（或文件首）
        insert_at = 0
        if lines and lines[0].lstrip().startswith(('"""', "'''")):
            quote = lines[0].lstrip()[:3]
            if len(lines[0].strip()) > 6 and lines[0].strip().endswith(quote):
                insert_at = 1
            else:
                for idx, line in enumerate(lines[1:], start=1):
                    if line.strip().endswith(quote):
                        insert_at = idx + 1
                        break
        lines.insert(insert_at, _UTILITY_IMPORT + "\n\n")
        return "".join(lines)
    lines.insert(last_import + 1, _UTILITY_IMPORT + "\n")
    return "".join(lines)


def _fixes_allowed(tests_root: Path) -> bool:
    """落盘改写许可：仅 fn_work/tests 树内（契约：fn_work 内文件可改）。"""
    campaign_root = discover_campaign_roots()["campaign_root"]
    allowed_root = (campaign_root / "fn_work" / "tests").resolve()
    try:
        Path(tests_root).resolve().relative_to(allowed_root)
        return True
    except ValueError:
        return False


def relax_platform_assertions(test_sources=None, apply_fixes: bool = False) -> dict:
    """扫描（并按许可改写）测试树 Windows-only 断言模式，出具报告。

    Args:
        test_sources: None=<战役根>/fn_work/tests（程序化发现）；或扫描根路径。
        apply_fixes: True=对命中处两处典则形态做锚定改写并逐处登记——仅当扫描根
            位于 <战役根>/fn_work/tests 内才真正落盘；其余根只报告不写。

    Returns:
        dict：scan（扫描报告）+ fixes_applied（逐处 file/line/old/new/kind）+
        residual_hits（改写后仍残留的命中，含 sys.platform 分支等需人工项）+
        fixed/residual 计数与 writes_allowed 标志。
    """
    if test_sources is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
        tests_root = campaign_root / "fn_work" / "tests"
    else:
        tests_root = Path(test_sources)
    scan = scan_windows_only_patterns(tests_root)
    report = {"scan": scan, "fixes_applied": [], "writes_allowed": False}
    if not scan["hits"] or not apply_fixes:
        report.update({"residual_hits": scan["hits"],
                       "fixed": 0, "residual": scan["hit_count"]})
        return report
    if not _fixes_allowed(tests_root):
        report.update({"residual_hits": scan["hits"],
                       "fixed": 0, "residual": scan["hit_count"],
                       "note": "扫描根不在 fn_work/tests 内，只报告不改写"})
        return report
    report["writes_allowed"] = True

    by_file: dict[str, list[dict]] = {}
    for hit in scan["hits"]:
        by_file.setdefault(hit["file"], []).append(hit)
    fixed_records = []
    residual = []
    for rel, hits in sorted(by_file.items()):
        target = (tests_root / rel).resolve()
        original = target.read_text(encoding="utf-8")
        rewritten, fixes = _rewrite_source(original)
        fixed_old_texts = [f["old"] for f in fixes]
        file_fixed, file_residual = [], []
        for hit in hits:
            auto_fixable = hit["kind"] in ("normcase_fold", "windows_drive_is_absolute")
            covered = any(old in hit["text"] or hit["text"] in old
                          for old in fixed_old_texts)
            (file_fixed if auto_fixable and covered else file_residual).append(hit)
        if fixes and not file_fixed:
            # 改写发生却无命中对应（形态漂移）：保守不改该文件
            residual.extend(hits)
            fixed_records.append({"file": rel, "kind": "rollback",
                                  "note": "改写与命中不对应（形态漂移），整文件不改"})
            continue
        if file_fixed:
            candidate = _insert_utility_import(rewritten)
            try:
                compile(candidate, str(target), "exec")
            except SyntaxError:
                residual.extend(hits)
                fixed_records.append({"file": rel, "kind": "rollback",
                                      "note": "改写后语法门失败，整文件回滚不改"})
                continue
            target.write_text(candidate, encoding="utf-8", newline="\n")
            for fix in fixes:
                fixed_records.append({
                    "file": rel,
                    "kind": fix["kind"],
                    "old": fix["old"],
                    "new": fix["new"],
                    "note": "改用双平台断言工具（登记处）",
                })
        residual.extend(file_residual)
    report["fixes_applied"] = fixed_records
    report["residual_hits"] = residual
    report["fixed"] = len([r for r in fixed_records
                           if r.get("kind") != "rollback"])
    report["residual"] = len(residual)
    return report
