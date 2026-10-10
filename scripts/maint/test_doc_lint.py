#!/usr/bin/env python3
"""doc_lint（工作流文档一致性检查）回归测试：四类规则的正负向行为。

seam：脚本命令行层 + 临时 fixture（spec #9 / issue#10 对齐）。
规则：①脚本引用存在性 ②多战役调用参数（--campaign）③v1 平铺路径 ④旧插件名。
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = "scripts/maint/doc_lint.py"

GOOD_CMD = """# 示例命令
运行 `python scripts/guard/exist.py --campaign <cid> --phase deliver`。
路径写 `workspace/<cid>/blueprint.md` 与 `workspace/README.md`。
"""


def run_lint(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SRC_ROOT / SCRIPT), "--root", str(root), *args],
                          capture_output=True, text=True, timeout=60)


def make_fixture(bad: bool) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="autoc_doclint_test_"))
    (tmp / "scripts" / "guard").mkdir(parents=True)
    (tmp / "scripts" / "guard" / "exist.py").write_text(
        "# ok\nadd_argument('--campaign')\nadd_argument('--phase')\n", encoding="utf-8")
    cmds = tmp / ".zcode" / "commands"
    cmds.mkdir(parents=True)
    (cmds / "good.md").write_text(GOOD_CMD, encoding="utf-8")
    if bad:
        (cmds / "bad.md").write_text(
            "# 坏命令\n"
            "运行 `python scripts/guard/missing.py`。\n"
            "先 `init_state.py --phase verify --by accept`（缺战役参数）。\n"
            "跑 `python scripts/guard/exist.py --bogus-flag`（参数不存在）。\n"
            "看 `workspace/blueprint.md` 与 `workspace/acceptance/`。\n"
            "docx 交付走 document-skills。\n",
            encoding="utf-8")
        tpl = tmp / "config" / "templates"
        tpl.mkdir(parents=True)
        (tpl / "t.md").write_text("输出到 workspace/software/ 即可。\n", encoding="utf-8")
        briefs = tmp / "kb" / "briefs"
        briefs.mkdir(parents=True)
        (briefs / "bad.md").write_text("# 方案\n## acceptance 清单\n", encoding="utf-8")
    return tmp


def main() -> int:
    passed = 0

    # 正向：干净 fixture 零违规
    root = make_fixture(bad=False)
    try:
        p = run_lint(root)
        ok = p.returncode == 0 and "VIOLATION" not in p.stdout
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 干净文档零违规：rc={p.returncode} {p.stdout[-200:]}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    # 负向：四类规则逐一点名
    root = make_fixture(bad=True)
    try:
        p = run_lint(root)
        out = p.stdout
        checks = [
            ("脚本引用存在性", "missing.py" in out and "不存在" in out),
            ("多战役参数", "--campaign" in out or "战役参数" in out),
            ("参数存在性", "bogus-flag" in out and "无参数" in out),
            ("v1 平铺路径", "blueprint.md" in out and "平铺" in out),
            ("旧插件名", "document-skills" in out and "插件" in out),
            ("方案书禁用节", "禁用节" in out),
        ]
        ok_all = p.returncode == 1
        passed += ok_all
        print(f"{'PASS' if ok_all else 'FAIL'} 坏文档整体拦截：rc={p.returncode}")
        for name, hit in checks:
            passed += hit
            print(f"{'PASS' if hit else 'FAIL'} 规则点名：{name}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    # 只扫指定域：坏文档在 commands，--only templates 不应报它
    root = make_fixture(bad=True)
    try:
        p = run_lint(root, "--only", "templates")
        out = p.stdout
        ok = "bad.md" not in out and "t.md" in out
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} --only 域过滤：rc={p.returncode}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    # briefs 域：方案书禁用节（R5）点名
    root = make_fixture(bad=True)
    try:
        p = run_lint(root, "--only", "briefs")
        ok = p.returncode == 1 and "bad.md" in p.stdout and "禁用节" in p.stdout
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} R5 方案书禁用节拦截：rc={p.returncode}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    print(f"\n{passed}/10 PASS")
    return 0 if passed == 10 else 1


if __name__ == "__main__":
    sys.exit(main())
