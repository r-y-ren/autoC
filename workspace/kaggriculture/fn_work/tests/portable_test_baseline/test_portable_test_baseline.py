"""portable_test_baseline 真实测试：三叶编排（注入桩跑全套管线）、裁决键与 fail-closed 分支、汇总行解析。"""

import json

import pytest

from portable_test_baseline.portable_test_baseline import (
    parse_pytest_summary,
    portable_test_baseline,
)


@pytest.fixture()
def pipeline_env(tmp_path):
    """tmp 全链环境：tmp 工件仓（1 CRLF 条目）+ 干净测试树 + tmp 声明输出。"""
    repo = tmp_path / "repo"
    coll = repo / "collA"
    coll.mkdir(parents=True)
    artifact = b'{\r\n  "v": 1\r\n}\r\n'
    (coll / "a.json").write_bytes(artifact)
    import hashlib
    (coll / "index.json").write_text(json.dumps({
        "schema_version": "artifact-index/1.0", "collection": "collA",
        "entries": [{"path": "collA/a.json",
                     "sha256": hashlib.sha256(artifact).hexdigest(),
                     "artifact_id": "a"}]}), encoding="utf-8")
    tests = tmp_path / "suite"
    tests.mkdir()
    (tests / "test_ok.py").write_text("def test_ok():\n    assert True\n",
                                      encoding="utf-8")
    return {"repo": repo, "tests": tests,
            "context_out": tmp_path / "docs" / "machine_context.md",
            "out_root": tmp_path / "artifacts"}


def _run_pipeline(env, exit_code, output, extra_tests=None):
    tests = env["tests"]
    if extra_tests:
        extra_tests(tests)
    calls = []

    def runner(root):
        calls.append(root)
        return exit_code, output

    verdict = portable_test_baseline(
        artifact_sources=env["repo"], output_root=env["out_root"],
        tests_root=tests, machine_context_output=env["context_out"],
        suite_runner=runner, repo_root=env["repo"], campaign_boundary=env["repo"])
    return verdict, calls


def test_orchestrated_pass_verdict_keys(pipeline_env):
    verdict, calls = _run_pipeline(pipeline_env, 0, "10 passed in 1.0s\n")
    # ① 工件重建在终检前完成（LF 落盘、双 sha 登记）
    rebuilt = pipeline_env["out_root"] / "collA" / "a.json"
    assert rebuilt.is_file() and b"\r" not in rebuilt.read_bytes()
    # ② 扫描干净树零命中
    # ③ 注入 runner 收到的正是终检套件根
    assert calls == [pipeline_env["tests"]]
    # ④ 声明文档已写
    assert pipeline_env["context_out"].is_file()
    # 裁决键
    assert verdict["ok"] is True
    assert verdict["verdict"] == "pass"
    assert verdict["checks"] == {
        "fn_work_suite_green": True, "scan_zero_hits": True,
        "lf_rebuild_done": True, "machine_context_written": True}
    assert verdict["artifacts"]["totals"]["rebuilt_lf"] == 1
    assert verdict["assertions"]["hits"] == 0
    assert verdict["assertions"]["residual"] == 0
    assert verdict["suite"]["exit_code"] == 0
    assert verdict["suite"]["passed"] == 10
    assert verdict["suite"]["failed"] == 0
    assert verdict["machine_context"]["path"] == str(pipeline_env["context_out"])
    # Windows 主力机复检边界显式登记（不静默）
    assert "Windows" in verdict["windows_main_machine_recheck"]
    # 声明内容吃到了编排实测记录
    text = pipeline_env["context_out"].read_text(encoding="utf-8")
    assert "10 passed in 1.0s" in text
    assert "LF 重建 1" in text


def test_fail_verdict_when_suite_red(pipeline_env):
    verdict, _ = _run_pipeline(pipeline_env, 1, "7 passed, 3 failed in 2.0s\n")
    assert verdict["ok"] is False
    assert verdict["verdict"] == "fail"
    assert verdict["checks"]["fn_work_suite_green"] is False
    assert verdict["checks"]["scan_zero_hits"] is True
    assert verdict["suite"]["failed"] == 3


def test_fail_verdict_when_scan_residual(pipeline_env):
    def inject_platform_branch(tests):
        # 拼接构造：本测试文件自身不得命中扫描器 token（自指防御）
        (tests / "test_branch.py").write_text(
            "import sys\n\ndef test_b():\n    if sys." +
            "platform == 'win32':\n        assert True\n", encoding="utf-8")

    verdict, _ = _run_pipeline(pipeline_env, 0, "5 passed in 1.0s\n",
                               extra_tests=inject_platform_branch)
    assert verdict["ok"] is False  # 扫描残留>0：终检不放过（tmp 树不在改写许可面）
    assert verdict["verdict"] == "fail"
    assert verdict["checks"]["scan_zero_hits"] is False
    assert verdict["assertions"]["hits"] == 1
    assert verdict["assertions"]["residual"] == 1


def test_suite_summary_parsed_to_records(tmp_path):
    def runner_with_skips(root):
        return 0, (".....s..\nSKIPPED [1] test_x.py:3: 缺 corpus/raw 语料\n"
                   "8 passed, 1 skipped in 3.0s\n")

    repo = _mini_repo(tmp_path)
    verdict = portable_test_baseline(
        artifact_sources=repo, output_root=tmp_path / "o",
        tests_root=_clean_tests(tmp_path), machine_context_output=tmp_path / "mc.md",
        suite_runner=runner_with_skips, repo_root=repo, campaign_boundary=repo)
    assert verdict["suite"]["skipped"] == 1
    assert verdict["suite"]["passed"] == 8
    assert verdict["suite"]["data_dependency_skips"], "skip 明细应入记录"
    assert "corpus/raw" in verdict["suite"]["data_dependency_skips"][0]["missing"]
    text = (tmp_path / "mc.md").read_text(encoding="utf-8")
    assert "corpus/raw" in text  # 声明文档逐项标注缺什么


def _mini_repo(tmp_path):
    repo = tmp_path / "mrepo"
    coll = repo / "c"
    coll.mkdir(parents=True)
    (coll / "x.json").write_bytes(b"{}\n")
    (coll / "index.json").write_text(json.dumps({
        "entries": [{"path": "c/x.json", "sha256": "0" * 64}]}), encoding="utf-8")
    return repo


def _clean_tests(tmp_path):
    tests = tmp_path / "mtests"
    tests.mkdir()
    (tests / "t.py").write_text("def test_t():\n    assert True\n", encoding="utf-8")
    return tests


# --------------------------------------------------------------------------- #
# 汇总行解析（解析不到不冒充）
# --------------------------------------------------------------------------- #

def test_parse_pytest_summary_variants():
    parsed = parse_pytest_summary("202 passed in 151.53s")
    assert parsed == {"summary_line": "202 passed in 151.53s", "passed": 202,
                      "failed": 0, "skipped": 0, "xfailed": 0}
    parsed = parse_pytest_summary("976 passed, 8 failed, 8 skipped in 64s")
    assert (parsed["passed"], parsed["failed"], parsed["skipped"]) == (976, 8, 8)
    parsed = parse_pytest_summary("7 passed, 1 skipped, 2 xfailed in 3s")
    assert (parsed["passed"], parsed["xfailed"]) == (7, 2)


def test_parse_pytest_summary_no_line():
    parsed = parse_pytest_summary("no summary here")
    assert parsed["summary_line"] is None
    assert parsed["passed"] is None
