"""test_verify_v2（R11 L0 验收）：四门编排矩阵、CLI 解析与 verify_summary 结构。

不真跑全量（16+8+24 局对局、26 局×两路重演与发射门留给实现验证/正式跑批）：
四门一律 monkeypatch 假件（除门② fail-closed 用例走真装载、假对手路径——
装载即抛不开局）；verify_summary.json 落临时包目录 evidence/，不碰真
evidence/ 盘面。矩阵覆盖：全过→overall True；任一门红→overall False（其余
门照跑，全跑不短路）；任一门抛异常→executed=False 门红但四门都被调用；
门② evidence 落点改指本包（复用不覆写 L1 包真台账）且跑后还原。"""

import hashlib
import json
import os
import platform
import re

import pytest

import verify_l11_gates as vlg  # noqa: E402  (自带 L1_DIR/HERE sys.path 自举)

_HERE = os.path.dirname(os.path.abspath(__file__))

_CONTRACT_KEYS = {"overall", "h2h", "lineage", "equivalence", "launch",
                  "evidence_dir", "started", "finished"}
_GATE_ORDER = ["h2h", "lineage", "equivalence", "launch"]

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
                  "result_face": {"ok": True, "dead_seeds_total_value": 120},
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
                 "equivalence": vlg.gate_equivalence_v2,
                 "launch": vlg.gate_launch_fourgate_l1}


@pytest.fixture
def pkg(tmp_path):
    """临时包目录（gate 门均为假件，main.py 只需存在且可 last-callable 装载）。"""
    p = tmp_path / "orderbook_l11_candidate"
    p.mkdir()
    (p / "main.py").write_text(
        "def _cxs_agent(obs):\n    return {}\n", encoding="utf-8")
    return p


def _install_fakes(monkeypatch, outcomes=None, calls=None):
    """四门全装假件。outcomes：门名→True/False/异常实例（异常即抛）；
    calls：列表，按完成序记录 (门名, args, kwargs)。"""
    outcomes = dict({"h2h": True, "lineage": True, "equivalence": True,
                     "launch": True}, **(outcomes or {}))

    def _make(label):
        outcome = outcomes[label]

        def run(*args, **kwargs):
            if calls is not None:
                calls.append((label, args, kwargs))
            if isinstance(outcome, BaseException):
                raise outcome
            payload = dict(_PAYLOADS[label])
            if outcome is False:                          # 红门时裁决面同红
                if label == "h2h":
                    payload["passed"] = outcome
                if label == "lineage":
                    payload["passed"] = outcome
                    payload["per_opponent"] = {
                        name: dict(summ, losses=1 if not outcome else 0)
                        for name, summ in payload["per_opponent"].items()}
                if label == "equivalence":
                    payload["form_face"] = {"ok": outcome,
                                            "appear_total": 3}
                    payload["result_face"] = {"ok": outcome,
                                              "dead_seeds_total_value": 910}
                    payload["subset"] = outcome
                    payload["cases"] = outcome
                if label == "launch":
                    payload["truncation_only_diff"] = {
                        "ok": outcome,
                        "divergent_steps": [648, 700] if outcome else [600, 700]}
            return dict(payload, passed=bool(outcome))

        return run

    for label, module in _GATE_MODULES.items():
        monkeypatch.setattr(module, "run", _make(label))


# ---- ① 编排矩阵 ----


def test_all_pass_overall_true(pkg, monkeypatch):
    _install_fakes(monkeypatch)
    result = vlg.verify(str(pkg))
    assert set(result) == _CONTRACT_KEYS
    assert result["overall"] is True
    for name in _GATE_ORDER:
        entry = result[name]
        assert entry["passed"] is True
        assert entry["executed"] is True
        assert entry["error"] is None
        assert entry["wall_s"] >= 0
    assert result["h2h"]["n"] == 16 and result["h2h"]["rate"] == 0.625
    assert result["h2h"]["ref_face"]["gating"] is False
    assert set(result["lineage"]["per_opponent"]) == {
        "v48-pure", "v4b", "hybrid-v2"}
    assert result["equivalence"]["form_face"] is True
    assert result["equivalence"]["appear_total"] == 1
    assert result["equivalence"]["dead_seeds_total_value"] == 120
    assert result["launch"]["gates"]["load"] is True
    assert result["launch"]["truncation_only_diff"]["n_divergent"] == 2
    assert result["evidence_dir"] == str(pkg / "evidence")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
                        result["started"])
    assert result["finished"] >= result["started"]


@pytest.mark.parametrize("red_gate", _GATE_ORDER)
def test_one_gate_red_fails_overall_others_still_run(pkg, monkeypatch,
                                                     red_gate):
    calls = []
    _install_fakes(monkeypatch, {red_gate: False}, calls)
    result = vlg.verify(str(pkg))
    assert result["overall"] is False
    assert result[red_gate]["passed"] is False
    assert [c[0] for c in calls] == _GATE_ORDER          # 全跑不短路
    for name in _GATE_ORDER:
        if name != red_gate:
            assert result[name]["passed"] is True


@pytest.mark.parametrize("broken_gate", _GATE_ORDER)
def test_gate_exception_fail_closed_all_gates_called(pkg, monkeypatch,
                                                     broken_gate):
    calls = []
    _install_fakes(
        monkeypatch, {broken_gate: RuntimeError(f"boom-{broken_gate}")}, calls)
    result = vlg.verify(str(pkg))
    assert result["overall"] is False                     # 不可执行=整体 fail
    entry = result[broken_gate]
    assert entry["executed"] is False
    assert entry["passed"] is False
    assert f"RuntimeError: boom-{broken_gate}" in entry["error"]
    assert [c[0] for c in calls] == _GATE_ORDER           # 其余门照跑
    for name in _GATE_ORDER:
        if name != broken_gate:
            assert result[name]["executed"] is True


def test_lineage_missing_opponent_fail_closed(pkg, monkeypatch):
    # 门②提示语义：对手 main 路径断裂 → L1 门②真装载即抛 GateLineageError（不
    # 开局）→ 编排记该门不可执行（门红），其余三门照跑。
    calls = []
    real_lineage_run = vlg.gate_lineage_strength.run      # 先留真件
    _install_fakes(monkeypatch, None, calls)              # 四门装假
    monkeypatch.setattr(vlg.gate_lineage_strength, "run",
                        real_lineage_run)                 # 门②还原真实现
    monkeypatch.setattr(
        vlg, "OPPONENTS",
        {"v48-pure": os.path.join(str(pkg), "nope", "main.py"),
         "v4b": os.path.join(str(pkg), "nope2", "main.py"),
         "hybrid-v2": os.path.join(str(pkg), "nope3", "main.py")})
    result = vlg.verify(str(pkg))
    assert result["overall"] is False
    lineage = result["lineage"]
    assert lineage["executed"] is False
    assert "GateLineageError" in lineage["error"]
    assert "per_opponent" not in lineage                  # 无裁决面可摘
    assert [c[0] for c in calls] == ["h2h", "equivalence", "launch"]


def test_lineage_evidence_redirected_to_pkg_not_l1_ledger(pkg, monkeypatch):
    # 门②复用证据纪律：L1 门② evidence 落点是 L1 包内模块常量——编排须改指本包
    # evidence/lineage_evidence.json（跑后还原模块常量），防覆写 L1 真台账。
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
    probe = pkg / "evidence" / "lineage_evidence.json"
    assert probe.is_file()                                # 落本包 evidence/
    assert json.loads(probe.read_text(encoding="utf-8"))["note"] == "redirect probe"
    assert result["lineage"]["evidence_path"] == str(probe)
    assert (gs.EVIDENCE_DIR, gs.EVIDENCE_PATH) == (original_dir, original_path)


def test_pkg_and_episodes_defaults(monkeypatch, tmp_path):
    # pkg 缺省=HERE（本编排所在包）；episodes 缺省=相对推导的语料目录。
    p = tmp_path / "self_pkg"
    p.mkdir()
    (p / "main.py").write_text("def _cxs_agent(obs):\n    return {}\n",
                               encoding="utf-8")
    calls = []
    _install_fakes(monkeypatch, None, calls)
    monkeypatch.setattr(vlg, "HERE", str(p))
    result = vlg.verify()
    assert result["evidence_dir"] == str(p / "evidence")
    eq_args = next(c for c in calls if c[0] == "equivalence")[1]
    assert eq_args[0] == vlg.EPISODES_DIR_DEFAULT
    assert os.path.isdir(vlg.EPISODES_DIR_DEFAULT)         # 语料真实在场
    assert (p / "evidence" / "verify_summary.json").is_file()


# ---- ② CLI 参数解析 ----


def test_cli_usage_errors(capsys):
    assert vlg.main([]) == 2                              # 缺 pkg_dir
    assert vlg.main(["a", "b", "c"]) == 2                 # 参数过多
    err = capsys.readouterr().err
    assert vlg.USAGE in err


def test_cli_exit_code_follows_overall(pkg, monkeypatch):
    _install_fakes(monkeypatch)
    assert vlg.main([str(pkg)]) == 0
    _install_fakes(monkeypatch, {"equivalence": False})
    assert vlg.main([str(pkg)]) == 1


def test_cli_passes_args_through(pkg, tmp_path, monkeypatch):
    epdir = tmp_path / "replays"
    epdir.mkdir()
    calls = []
    _install_fakes(monkeypatch, None, calls)
    assert vlg.main([str(pkg), str(epdir)]) == 0
    by_gate = {c[0]: c for c in calls}
    v2_main = str(pkg / "main.py")
    h2h_args, h2h_kwargs = by_gate["h2h"][1], by_gate["h2h"][2]
    assert h2h_args == (v2_main, vlg.L1_MAIN, vlg.VERBATIM_MAIN)
    assert h2h_kwargs == {
        "evidence_path": str(pkg / "evidence" / "h2h_evidence.json")}
    lin_args, lin_kwargs = by_gate["lineage"][1], by_gate["lineage"][2]
    assert lin_args == (v2_main, vlg.OPPONENTS)
    assert lin_kwargs == {"per_opponent_n": 8}
    assert by_gate["equivalence"][1] == (
        str(epdir), v2_main, vlg.L1_MAIN, vlg.VERBATIM_MAIN)
    assert by_gate["equivalence"][2] == {
        "evidence_path": str(pkg / "evidence" / "equivalence_evidence.json")}
    assert by_gate["launch"][1] == (str(pkg),)


# ---- ③ verify_summary.json 结构（假件跑） ----


def test_verify_summary_structure(pkg, monkeypatch):
    _install_fakes(monkeypatch, {"equivalence": False})   # 红门也完整落台账
    result = vlg.verify(str(pkg))
    path = pkg / "evidence" / "verify_summary.json"
    assert path.is_file()
    summary = json.loads(path.read_text(encoding="utf-8"))

    # 契约八键 + 编排戳面
    assert _CONTRACT_KEYS <= set(summary)
    assert set(summary) == _CONTRACT_KEYS | {
        "protocol", "pkg_path", "episodes_dir", "gates_passed",
        "evidence_files", "environment", "mains"}
    assert summary["protocol"] == "verify-l11-gates/1.0"
    assert summary["pkg_path"] == str(pkg)
    assert summary["episodes_dir"] == vlg.EPISODES_DIR_DEFAULT
    assert summary["overall"] is False
    assert summary["gates_passed"] == {"h2h": True, "lineage": True,
                                       "equivalence": False, "launch": True}
    assert summary["overall"] == result["overall"]        # 与返回值一致

    # evidence 五件清单（均落 <pkg>/evidence/）
    assert summary["evidence_files"] == {
        "h2h": str(pkg / "evidence" / "h2h_evidence.json"),
        "h2h_ref": str(pkg / "evidence" / "h2h_ref_evidence.json"),
        "lineage": str(pkg / "evidence" / "lineage_evidence.json"),
        "equivalence": str(pkg / "evidence" / "equivalence_evidence.json"),
        "launch": str(pkg / "evidence" / "launch_check_evidence.json"),
    }

    # 环境戳：python 版本 + 起止时间 + v2/L1/verbatim 三 main 的 sha256
    env = summary["environment"]
    assert env["python_version"] == platform.python_version()
    assert env["python_full"] and env["platform"]
    assert summary["started"] == result["started"]
    assert summary["finished"] == result["finished"]
    mains = summary["mains"]
    assert mains["v2_main"] == str(pkg / "main.py")
    assert mains["l1_main"] == vlg.L1_MAIN
    assert mains["verbatim_main"] == vlg.VERBATIM_MAIN
    assert mains["sha256"]["v2_main"] == hashlib.sha256(
        (pkg / "main.py").read_bytes()).hexdigest()
    assert mains["sha256"]["l1_main"] == hashlib.sha256(
        open(vlg.L1_MAIN, "rb").read()).hexdigest()
    assert mains["sha256"]["verbatim_main"] == hashlib.sha256(
        open(vlg.VERBATIM_MAIN, "rb").read()).hexdigest()

    # 各门 entry：passed/executed/error 齐备，红门留痕
    for name, passed in summary["gates_passed"].items():
        entry = summary[name]
        assert entry["passed"] is passed
        assert entry["executed"] is True
        assert entry["error"] is None
        assert entry["evidence_path"] == _PAYLOADS[name]["evidence_path"]
    assert summary["equivalence"]["form_face"] is False
    assert summary["equivalence"]["appear_total"] == 3    # 红面指标留痕
    assert summary["equivalence"]["dead_seeds_total_value"] == 910
    assert summary["h2h"]["ref_face"]["n"] == 8
    assert summary["lineage"]["per_opponent"]["v4b"]["wins"] == 6
    assert summary["launch"]["truncation_only_diff"]["min_divergent_step"] == 648
