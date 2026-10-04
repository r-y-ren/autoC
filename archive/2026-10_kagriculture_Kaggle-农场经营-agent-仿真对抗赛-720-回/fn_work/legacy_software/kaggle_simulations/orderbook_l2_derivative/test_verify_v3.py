"""test_verify_v3（R12 L0 验收）：两窗四门编排矩阵、最宽窗推荐、CLI 与
verify_summary_v3 结构。

不真跑全量（两窗×（16+8 局对局+24 局 lineage+26 局×两路重演+终态提取+发射
门）留给实现验证/正式跑批）：四门一律 monkeypatch 假件；矩阵覆盖：双窗全绿→
recommended=w600（600 更宽）；仅 w648 绿→w648；仅 w600 绿→w600；双红→None；
任一门抛异常→executed=False 门红该窗必红，但两窗四门共八次调用全跑不短路；
门② evidence 落点逐窗改指（复用不覆写 L1 包真台账）且跑后还原。"""

import hashlib
import json
import os
import platform
import re

import pytest

import verify_l2_gates as vlg  # noqa: E402  (自带 L1/L11/HERE sys.path 自举)

_CONTRACT_KEYS = {"overall", "windows", "recommended", "evidence_dir",
                  "started", "finished"}
_GATE_ORDER = ["h2h", "lineage", "equivalence", "launch"]
_WINDOWS = ["w648", "w600"]
_WINDOW_KEYS = {"window", "overall", "h2h", "lineage", "equivalence",
                "launch", "v3_main", "evidence_dir", "evidence_files"}

# 假件 payload：只携带编排要摘取的裁决面字段（per_game 等重台账本就不进 summary）。
_H2H_PAYLOAD = {"n": 16, "wins": 10, "rate": 0.625, "passed": True,
                "ref_face": {"n": 8, "wins": 5, "losses": 3, "ties": 0,
                             "rate": 0.625, "gating": False,
                             "evidence_path": "/fake/h2h_ref_evidence.json"},
                "evidence_path": "/fake/h2h_evidence.json"}
_LINEAGE_PAYLOAD = {
    "per_opponent": {
        "v48-pure": {"n": 8, "wins": 5, "losses": 0, "ties": 3,
                     "all_done": True, "per_game": []},
        "v4b": {"n": 8, "wins": 6, "losses": 0, "ties": 2,
                "all_done": True, "per_game": []},
        "hybrid-v2": {"n": 8, "wins": 4, "losses": 0, "ties": 4,
                      "all_done": True, "per_game": []},
    },
    "evidence_path": "/fake/lineage_evidence.json",
}
_EQUIV_PAYLOAD = {"form_face": {"ok": True, "appear_total": 1},
                  "result_face": {"ok": True, "dead_seeds_total_value": 120,
                                  "starve_free": True},
                  "subset": True, "cases": True, "n_errors": 0,
                  "evidence_path": "/fake/equivalence_evidence.json"}
_LAUNCH_PAYLOAD = {
    "gates": {"load": True, "full_episodes": True,
              "determinism": True, "package": True},
    "truncation_only_diff": {"ok": True, "divergent_steps": [648, 700]},
    "evidence_path": "/fake/launch_check_evidence.json",
}
_PAYLOADS = {"h2h": _H2H_PAYLOAD, "lineage": _LINEAGE_PAYLOAD,
             "equivalence": _EQUIV_PAYLOAD, "launch": _LAUNCH_PAYLOAD}
_GATE_MODULES = {"h2h": vlg.gate_h2h_vs_l1,
                 "lineage": vlg.gate_lineage_strength,
                 "equivalence": vlg.gate_equivalence_v3,
                 "launch": vlg.gate_launch_fourgate_l1}


@pytest.fixture
def pkg(tmp_path):
    """临时包根（gate 门均为假件，两窗 main.py 只需存在）。"""
    root = tmp_path / "orderbook_l2_candidate"
    for w in _WINDOWS:
        d = root / w
        d.mkdir(parents=True)
        (d / "main.py").write_text(
            "def _cxs_agent(obs):\n    return {}\n", encoding="utf-8")
    return root


def _install_fakes(monkeypatch, outcomes=None, calls=None):
    """四门全装假件。outcomes：{(窗名, 门名): True/False/异常实例}（异常即抛），
    缺省全绿；calls：列表，按完成序记录 (窗名, 门名, args, kwargs)。"""
    outcomes = dict(outcomes or {})

    def _window_of(label, args, kwargs):
        if label == "equivalence":
            return f"w{kwargs['window']}"
        if label == "launch":
            return os.path.basename(os.path.abspath(args[0]))
        return os.path.basename(os.path.dirname(os.path.abspath(args[0])))

    def _make(label):
        def run(*args, **kwargs):
            window = _window_of(label, args, kwargs)
            if calls is not None:
                calls.append((window, label, args, kwargs))
            outcome = outcomes.get((window, label), True)
            if isinstance(outcome, BaseException):
                raise outcome
            payload = dict(_PAYLOADS[label])
            if outcome is False:                          # 红门时裁决面同红
                if label == "lineage":
                    payload["per_opponent"] = {
                        name: dict(summ, losses=1)
                        for name, summ in payload["per_opponent"].items()}
                if label == "equivalence":
                    payload["form_face"] = {"ok": False, "appear_total": 3}
                    payload["result_face"] = {
                        "ok": False, "dead_seeds_total_value": 600,
                        "starve_free": False}
            return dict(payload, passed=bool(outcome))

        return run

    for label, module in _GATE_MODULES.items():
        monkeypatch.setattr(module, "run", _make(label))


# ---- ① 两窗编排矩阵与最宽窗推荐 ----

def test_both_windows_green_recommends_widest_w600(pkg, monkeypatch):
    calls = []
    _install_fakes(monkeypatch, None, calls)
    result = vlg.verify(str(pkg))
    assert set(result) == _CONTRACT_KEYS
    assert result["overall"] is True
    assert result["recommended"] == "w600"            # 600>648 宽度：双绿取宽
    assert set(result["windows"]) == {"w648", "w600"}
    # 全跑不短路：两窗 × 四门共八次调用，跑序=窗序(w648→w600)×门序。
    assert [(c[0], c[1]) for c in calls] == [
        (w, gate) for w in _WINDOWS for gate in _GATE_ORDER]
    for wname, window in zip(_WINDOWS, (648, 600)):
        entry = result["windows"][wname]
        assert set(entry) == _WINDOW_KEYS
        assert entry["window"] == window
        assert entry["overall"] is True
        assert entry["v3_main"] == str(pkg / wname / "main.py")
        assert entry["evidence_dir"] == str(pkg / wname / "evidence")
        for gate in _GATE_ORDER:
            assert entry[gate]["passed"] is True
            assert entry[gate]["executed"] is True
            assert entry[gate]["error"] is None
            assert entry[gate]["wall_s"] >= 0
        assert entry["equivalence"]["form_face"] is True
        assert entry["equivalence"]["starve_free"] is True
        assert entry["equivalence"]["dead_seeds_total_value"] == 120
        assert entry["h2h"]["ref_face"]["gating"] is False
        assert set(entry["lineage"]["per_opponent"]) == {
            "v48-pure", "v4b", "hybrid-v2"}
        assert entry["launch"]["truncation_only_diff"]["n_divergent"] == 2
    assert result["evidence_dir"] == str(pkg / "evidence")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
                        result["started"])
    assert result["finished"] >= result["started"]


def test_only_w648_green_recommends_w648(pkg, monkeypatch):
    # w600 一门红即整窗红：recommended 回退到全绿的 w648。
    calls = []
    _install_fakes(monkeypatch, {("w600", "h2h"): False}, calls)
    result = vlg.verify(str(pkg))
    assert result["recommended"] == "w648"
    assert result["overall"] is True
    assert result["windows"]["w648"]["overall"] is True
    assert result["windows"]["w600"]["overall"] is False
    assert result["windows"]["w600"]["h2h"]["passed"] is False
    assert len(calls) == 8                            # 红窗其余门照跑


def test_only_w600_green_recommends_w600(pkg, monkeypatch):
    _install_fakes(monkeypatch, {("w648", "equivalence"): False})
    result = vlg.verify(str(pkg))
    assert result["windows"]["w648"]["overall"] is False
    assert result["recommended"] == "w600"            # 宽窗全绿仍取宽
    assert result["overall"] is True


def test_both_windows_red_recommends_none(pkg, monkeypatch):
    calls = []
    _install_fakes(monkeypatch, {("w648", "equivalence"): False,
                                 ("w600", "launch"): False}, calls)
    result = vlg.verify(str(pkg))
    assert result["recommended"] is None
    assert result["overall"] is False
    assert result["windows"]["w648"]["overall"] is False
    assert result["windows"]["w600"]["overall"] is False
    assert [(c[0], c[1]) for c in calls] == [          # 全跑不短路
        (w, gate) for w in _WINDOWS for gate in _GATE_ORDER]


@pytest.mark.parametrize("broken_gate", _GATE_ORDER)
def test_gate_exception_fail_closed_all_gates_called(pkg, monkeypatch,
                                                     broken_gate):
    # 不可执行=该门红该窗必红，但两窗四门全跑（fail-closed 不短路）；另一窗
    # 全绿时 recommended 回退该窗、overall 仍真（推荐只认全绿窗）。
    calls = []
    _install_fakes(
        monkeypatch, {("w600", broken_gate): RuntimeError(f"boom-{broken_gate}")},
        calls)
    result = vlg.verify(str(pkg))
    assert result["windows"]["w600"]["overall"] is False
    entry = result["windows"]["w600"][broken_gate]
    assert entry["executed"] is False
    assert entry["passed"] is False
    assert f"RuntimeError: boom-{broken_gate}" in entry["error"]
    assert result["recommended"] == "w648"            # w648 全绿仍可推荐
    assert result["overall"] is True
    assert [(c[0], c[1]) for c in calls] == [
        (w, gate) for w in _WINDOWS for gate in _GATE_ORDER]
    for wname in _WINDOWS:
        for gate in _GATE_ORDER:
            if (wname, gate) != ("w600", broken_gate):
                assert result["windows"][wname][gate]["executed"] is True


def test_lineage_evidence_redirected_per_window(pkg, monkeypatch):
    # 门②复用证据纪律：L1 门② evidence 落点是 L1 包内模块常量——编排须逐窗
    # 改指该窗 evidence/lineage_evidence.json（跑后还原模块常量），防覆写 L1
    # 真台账。
    gs = vlg.gate_lineage_strength
    original_dir, original_path = gs.EVIDENCE_DIR, gs.EVIDENCE_PATH

    def probe_run(*args, **kwargs):
        os.makedirs(gs.EVIDENCE_DIR, exist_ok=True)
        with open(gs.EVIDENCE_PATH, "w", encoding="utf-8") as fh:
            json.dump({"note": "redirect probe"}, fh)
        return dict(_LINEAGE_PAYLOAD, passed=True,
                    evidence_path=gs.EVIDENCE_PATH)

    _install_fakes(monkeypatch)
    monkeypatch.setattr(gs, "run", probe_run)
    result = vlg.verify(str(pkg))
    assert result["overall"] is True
    for wname in _WINDOWS:
        probe = pkg / wname / "evidence" / "lineage_evidence.json"
        assert probe.is_file()                        # 落该窗 evidence/
        assert json.loads(probe.read_text(encoding="utf-8"))["note"] == \
            "redirect probe"
        assert result["windows"][wname]["lineage"]["evidence_path"] == str(probe)
    assert (gs.EVIDENCE_DIR, gs.EVIDENCE_PATH) == (original_dir, original_path)


def test_pkg_and_episodes_defaults(monkeypatch, tmp_path):
    # pkg_root 缺省=HERE（本编排所在包根）；episodes 缺省=相对推导的语料目录。
    p = tmp_path / "self_pkg"
    for w in _WINDOWS:
        d = p / w
        d.mkdir(parents=True)
        (d / "main.py").write_text("def _cxs_agent(obs):\n    return {}\n",
                                   encoding="utf-8")
    calls = []
    _install_fakes(monkeypatch, None, calls)
    monkeypatch.setattr(vlg, "HERE", str(p))
    result = vlg.verify()
    assert result["evidence_dir"] == str(p / "evidence")
    eq_args = [c for c in calls if c[1] == "equivalence"]
    assert all(c[2][0] == vlg.EPISODES_DIR_DEFAULT for c in eq_args)
    assert os.path.isdir(vlg.EPISODES_DIR_DEFAULT)     # 语料真实在场
    assert (p / "evidence" / "verify_summary_v3.json").is_file()


# ---- ② CLI 参数解析 ----

def test_cli_usage_errors(capsys):
    assert vlg.main([]) == 2                          # 缺 pkg_root
    assert vlg.main(["a", "b", "c"]) == 2             # 参数过多
    err = capsys.readouterr().err
    assert vlg.USAGE in err


def test_cli_exit_code_follows_recommended(pkg, monkeypatch):
    _install_fakes(monkeypatch)
    assert vlg.main([str(pkg)]) == 0                  # 双绿→recommended w600
    _install_fakes(monkeypatch, {("w648", "equivalence"): False,
                                 ("w600", "launch"): False})
    assert vlg.main([str(pkg)]) == 1                  # 双红→无推荐


def test_cli_passes_args_through(pkg, tmp_path, monkeypatch):
    epdir = tmp_path / "replays"
    epdir.mkdir()
    calls = []
    _install_fakes(monkeypatch, None, calls)
    assert vlg.main([str(pkg), str(epdir)]) == 0
    by_call = {(c[0], c[1]): c for c in calls}
    for wname, window in zip(_WINDOWS, (648, 600)):
        w_main = str(pkg / wname / "main.py")
        w_ev = pkg / wname / "evidence"
        h2h_args, h2h_kwargs = by_call[(wname, "h2h")][2:4]
        assert h2h_args == (w_main, vlg.L1_MAIN, vlg.VERBATIM_MAIN)
        assert h2h_kwargs == {"evidence_path": str(w_ev / "h2h_evidence.json")}
        lin_args, lin_kwargs = by_call[(wname, "lineage")][2:4]
        assert lin_args == (w_main, vlg.OPPONENTS)    # seeds 缺省（不传）
        assert lin_kwargs == {"per_opponent_n": 8}
        eq_args, eq_kwargs = by_call[(wname, "equivalence")][2:4]
        assert eq_args == (str(epdir), w_main, vlg.L1_MAIN, vlg.VERBATIM_MAIN)
        assert eq_kwargs == {
            "window": window,
            "evidence_path": str(
                w_ev / f"equivalence_evidence_w{window}.json")}
        launch_args, launch_kwargs = by_call[(wname, "launch")][2:4]
        assert launch_args == (str(pkg / wname),)
        assert launch_kwargs == {
            "evidence_path": str(w_ev / "launch_check_evidence.json")}


# ---- ③ verify_summary_v3.json 结构（假件跑） ----

def test_verify_summary_v3_structure(pkg, monkeypatch):
    _install_fakes(monkeypatch, {("w600", "equivalence"): False})  # 红窗留痕
    result = vlg.verify(str(pkg))
    path = pkg / "evidence" / "verify_summary_v3.json"
    assert path.is_file()
    summary = json.loads(path.read_text(encoding="utf-8"))

    # 契约六键 + 编排戳面
    assert _CONTRACT_KEYS <= set(summary)
    assert set(summary) == _CONTRACT_KEYS | {
        "protocol", "pkg_root", "episodes_dir", "width_order",
        "windows_passed", "environment", "mains"}
    assert summary["protocol"] == "verify-l2-gates/1.0"
    assert summary["pkg_root"] == str(pkg)
    assert summary["episodes_dir"] == vlg.EPISODES_DIR_DEFAULT
    assert summary["width_order"] == ["w600", "w648"]  # 宽→窄
    assert summary["recommended"] == "w648"            # w600 红回退窄窗
    assert summary["overall"] is True
    assert summary["windows_passed"] == {"w648": True, "w600": False}
    assert summary["overall"] == result["overall"]     # 与返回值一致

    # 两窗对比：w648 entry 完整在场
    entry = summary["windows"]["w648"]
    assert set(entry) == _WINDOW_KEYS
    assert entry["equivalence"]["form_face"] is True
    assert entry["equivalence"]["dead_seeds_total_value"] == 120
    assert entry["evidence_files"]["equivalence"] == str(
        pkg / "w648" / "evidence" / "equivalence_evidence_w648.json")
    assert summary["windows"]["w600"]["equivalence"]["passed"] is False

    # 环境戳：python 版本 + 起止时间 + 三 main（两窗 v3/L1/verbatim）sha256
    env = summary["environment"]
    assert env["python_version"] == platform.python_version()
    assert env["python_full"] and env["platform"]
    assert summary["started"] == result["started"]
    assert summary["finished"] == result["finished"]
    mains = summary["mains"]
    assert mains["l1_main"] == vlg.L1_MAIN
    assert mains["verbatim_main"] == vlg.VERBATIM_MAIN
    assert mains["windows"] == {
        wname: {"main": str(pkg / wname / "main.py")} for wname in _WINDOWS}
    assert mains["sha256"]["l1_main"] == hashlib.sha256(
        open(vlg.L1_MAIN, "rb").read()).hexdigest()
    assert mains["sha256"]["verbatim_main"] == hashlib.sha256(
        open(vlg.VERBATIM_MAIN, "rb").read()).hexdigest()
    for wname in _WINDOWS:
        assert mains["sha256"][f"{wname}_main"] == hashlib.sha256(
            (pkg / wname / "main.py").read_bytes()).hexdigest()

    # 各门 entry：passed/executed/error 齐备
    for wname in _WINDOWS:
        for gate in _GATE_ORDER:
            assert summary["windows"][wname][gate]["executed"] is True
            assert summary["windows"][wname][gate]["error"] is None
