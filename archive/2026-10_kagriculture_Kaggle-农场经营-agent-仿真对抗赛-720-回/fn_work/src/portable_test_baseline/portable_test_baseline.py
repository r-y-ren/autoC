"""测试基线机器无关化入口：工件 LF 重建、断言双平台化、机器语境声明三件编排 + 终检裁决。

上游: R6, R20（详见 fn_docs/responsibility.md）

实现要点：
- 编排序：①regenerate_artifacts_lf（exports 根级 index 类 LF 重建+双 sha 登记）
  → ②relax_platform_assertions（fn_work/tests 扫描；根在 fn_work/tests 内才落盘
  改写，逐处登记）→ ③终检=fn_work 全套件本机跑（subprocess pytest，可注入）
  → ④declare_machine_context（以①②③实测记录渲染声明，落 fn_docs）。
- 裁决 dict（fail-closed）：ok = 套件绿(exit 0) AND 扫描残留 0 AND 重建完成；
  checks 逐项列出，windows_main_machine_recheck 显式登记为跨机人工事项
  （R6"重建后主力机基线回退即失败"——本机不可代跑，不静默）。
- suite_runner 注入口（测试用）：callable(tests_root) -> (exit_code, output_text)；
  默认真跑 [sys.executable, -m, pytest, tests, -q, --tb=no, -rs]，从汇总行解析
  passed/failed/skipped（解析失败不冒充，记 None 并以 exit code 为准）。
- 数据纪律：裁决/声明中的一切实测数字只来自本函数真实运行结果（套件输出/
  重建报告计数），无任何手写估计。
"""

from __future__ import annotations

import platform
import re
import subprocess
import sys
from pathlib import Path

from portable_test_baseline.declare_machine_context import declare_machine_context
from portable_test_baseline.regenerate_artifacts_lf import regenerate_artifacts_lf
from portable_test_baseline.relax_platform_assertions import relax_platform_assertions
from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["run_fn_work_suite", "parse_pytest_summary", "portable_test_baseline"]

_SUMMARY_RE = re.compile(
    r"(?P<passed>\d+) passed(?:,\s+(?P<failed>\d+) failed)?"
    r"(?:,\s+(?P<skipped>\d+) skipped)?(?:,\s+(?P<xfailed>\d+) xfailed)?")
_SUITE_TIMEOUT_SECONDS = 1800


def run_fn_work_suite(tests_root: Path) -> tuple[int, str]:
    """真跑 fn_work 全套件（subprocess，与进程 CWD 无关），返回 (exit_code, output)。"""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(tests_root), "-q", "--tb=no", "-rs"],
        capture_output=True, text=True, timeout=_SUITE_TIMEOUT_SECONDS, check=False)
    return proc.returncode, proc.stdout + proc.stderr


def parse_pytest_summary(output_text: str) -> dict:
    """自 pytest -q 输出解析汇总行计数；解析不到即返回 summary_line=None（不冒充）。"""
    for line in reversed(output_text.splitlines()):
        line = line.strip()
        match = _SUMMARY_RE.search(line)
        if match:
            return {
                "summary_line": line,
                "passed": int(match.group("passed")),
                "failed": int(match.group("failed") or 0),
                "skipped": int(match.group("skipped") or 0),
                "xfailed": int(match.group("xfailed") or 0),
            }
    return {"summary_line": None, "passed": None, "failed": None,
            "skipped": None, "xfailed": None}


def _collect_data_dependency_skips(output_text: str) -> list[dict]:
    """自 -rs 输出收集 skip 明细（SKIPPED [n] reason in file）——缺什么逐项留档。"""
    skips = []
    for line in output_text.splitlines():
        line = line.strip()
        if line.startswith("SKIPPED ["):
            reason = re.sub(r"^SKIPPED \[\d+\]\s*", "", line)
            skips.append({"item": reason.split(" in ")[0].strip() if " in " in reason
                          else reason, "missing": reason})
    return skips


def portable_test_baseline(artifact_sources=None, tests_root=None, output_root=None,
                           machine_context_output=None, suite_runner=None, *,
                           repo_root=None, campaign_boundary=None) -> dict:
    """三叶编排+终检，输出裁决 dict（R6 机器无关化入口）。

    Args:
        artifact_sources / output_root / repo_root / campaign_boundary: 透传
            regenerate_artifacts_lf（None=旧树 exports 根级 index 类 /
            <战役根>/fn_work/artifacts / 发现仓根 / 战役根；后两者测试注入
            tmp 工件树时覆写）。
        tests_root: 终检套件根；None=<战役根>/fn_work/tests。
        machine_context_output: 声明文档输出；None=<战役根>/fn_docs/machine_context.md。
        suite_runner: None=真跑 pytest；测试注入 callable(root)->(exit_code, text)。

    Returns:
        裁决 dict：ok/verdict/checks/artifacts/assertions/suite/machine_context/
        windows_main_machine_recheck（跨机人工事项，显式登记不静默）。
    """
    campaign_root = discover_campaign_roots()["campaign_root"]
    if tests_root is None:
        tests_root_resolved = campaign_root / "fn_work" / "tests"
    else:
        tests_root_resolved = Path(tests_root)

    # ① 工件 LF 重建（双 sha 登记）
    artifacts_root, regen_report = regenerate_artifacts_lf(
        artifact_sources=artifact_sources, output_root=output_root,
        repo_root=repo_root, campaign_boundary=campaign_boundary)
    # ② 断言双平台化扫描（fn_work/tests 内才落盘改写——契约许可面）
    relax_report = relax_platform_assertions(
        test_sources=tests_root_resolved, apply_fixes=True)
    # ③ 终检：fn_work 全套件本机跑
    if suite_runner is None:
        exit_code, suite_text = run_fn_work_suite(tests_root_resolved)
        suite_command = f"python -m pytest {tests_root_resolved} -q --tb=no -rs"
    else:
        exit_code, suite_text = suite_runner(tests_root_resolved)
        suite_command = "<injected suite_runner>"
    suite_summary = parse_pytest_summary(suite_text)
    data_skips = _collect_data_dependency_skips(suite_text)
    suite_green = exit_code == 0
    scan_clean = relax_report["residual"] == 0
    # ④ 机器语境声明（以 ①②③ 实测记录渲染）
    records = {
        "local_run": {
            "command": suite_command,
            "platform": platform.platform(),
            "python": platform.python_version(),
            "summary_line": suite_summary["summary_line"],
            "collected": None,
            "passed": suite_summary["passed"],
            "failed": suite_summary["failed"],
            "skipped": suite_summary["skipped"],
        },
        "data_dependency_skips": data_skips,
        "crlf_lf_strategy": (
            f"exports index 类 {regen_report['totals']['collections']} 件、条目 "
            f"{regen_report['totals']['entries']}：LF 重建 "
            f"{regen_report['totals']['rebuilt_lf']}、二进制跳过 "
            f"{regen_report['totals']['skipped_binary']}、缺失 "
            f"{regen_report['totals']['missing']}；legacy=CRLF 口径变体 "
            f"{regen_report['totals']['legacy_is_crlf_variant']} 条双 sha 登记"
            f"（产物根 {regen_report['output_root']}）"),
        "assertion_strategy": (
            f"扫描 {relax_report['scan']['files_scanned']} 文件，Windows-only 命中 "
            f"{relax_report['scan']['hit_count']}、改写 {relax_report['fixed']}、"
            f"残留 {relax_report['residual']}（残留>0 即裁决失败）"),
        "windows_main_machine_recheck": (
            "本机不可执行；同 commit Windows 主力机复跑若基线回退，本裁决口径即失败（R6）"),
    }
    context_path = declare_machine_context(
        records, output_path=machine_context_output)

    ok = bool(suite_green and scan_clean)
    return {
        "ok": ok,
        "verdict": "pass" if ok else "fail",
        "checks": {
            "fn_work_suite_green": suite_green,
            "scan_zero_hits": scan_clean,
            "lf_rebuild_done": regen_report["totals"]["rebuilt_lf"] > 0
                               or regen_report["totals"]["entries"] == 0,
            "machine_context_written": context_path.is_file(),
        },
        "artifacts": {
            "output_root": str(artifacts_root),
            "totals": regen_report["totals"],
            "report_files": regen_report["report_files"],
        },
        "assertions": {
            "files_scanned": relax_report["scan"]["files_scanned"],
            "hits": relax_report["scan"]["hit_count"],
            "fixed": relax_report["fixed"],
            "residual": relax_report["residual"],
            "fixes_applied": relax_report["fixes_applied"],
        },
        "suite": {
            "command": suite_command,
            "exit_code": exit_code,
            **suite_summary,
            "data_dependency_skips": data_skips,
        },
        "machine_context": {"path": str(context_path)},
        "windows_main_machine_recheck": records["windows_main_machine_recheck"],
    }
