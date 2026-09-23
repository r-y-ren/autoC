"""test_gate_launch（继承 R10 验收④）：门④发射四门接线与 fail-closed。

三组：
①真跑组（module 级 fixture 恰一次，~1 分钟）：全四门（整包装载+双席自打
  2 局+确定性重跑）+ 附加断言全绿；evidence 经 evidence_path 落 tmp（不写
  真 evidence/，评审 P1 测试隔离）且四门结果/附加断言/身份链（对
  build_manifest 核对）三段齐、与返回值一致；
②身份链破坏组：临时目录拷贝包件+篡改 manifest 期望 main sha → passed=False
  （fail-closed 早退不驱动长局；不碰真 manifest）；
③差异步组：附加断言的 divergent_steps（719 真实 obs 驱动 L1 vs verbatim 的
  diff 步集合）全部 ≥648。"""

import json
import shutil
from pathlib import Path

import pytest

import gate_launch_fourgate_l1 as gate

_HERE = Path(__file__).resolve().parent
_PKG = _HERE
_MANIFEST = _PKG / "build_manifest.json"


@pytest.fixture(scope="module")
def launch_result(tmp_path_factory):
    """真跑全四门一次（module 级共享：三组断言同一次产物，防重复 1 分钟级跑批）。

    evidence_path 指 tmp（评审 P1：测试不覆写真 evidence/launch_check_
    evidence.json——真台账只归 verify_layer_s_gates 全量编排落）。
    """
    ev_file = (tmp_path_factory.mktemp("launch_ev")
               / "launch_check_evidence.json")
    return gate.run(str(_PKG), evidence_path=str(ev_file))


def test_four_gates_all_pass(launch_result):
    # ①四门全绿 + 附加断言 ok → passed=True
    assert launch_result["passed"] is True
    assert launch_result["gates"] == {
        "load": True, "full_episodes": True,
        "determinism": True, "package": True,
    }
    assert launch_result["truncation_only_diff"]["ok"] is True


def test_evidence_file_fields(launch_result):
    ev_path = Path(launch_result["evidence_path"])
    # 评审 P1：台账落 tmp（evidence_path 覆写），绝不在真 evidence/ 落盘
    assert ev_path.name == "launch_check_evidence.json"
    assert not ev_path.is_relative_to(_PKG)
    assert ev_path.is_file()
    verdict = json.loads(ev_path.read_text(encoding="utf-8"))
    assert verdict["passed"] is True
    assert verdict["gates"] == launch_result["gates"]
    assert verdict["truncation_only_diff"]["ok"] is True
    assert not verdict["errors"]

    # 门①段：官方装载 ok 且末 callable=_cxs_agent（-I 驱动器零分歧）
    g1 = verdict["gate1_official_load"]
    assert g1["gate1_official_load_ok"] is True
    assert g1["evidence"]["last_callable_name"] == "_cxs_agent"
    assert g1["isolated_vs_local_action_mismatches"] == 0
    assert g1["evidence"]["action_errors"] == []

    # 门②③段：seeds 101/102 全 720 回合 DONE、每步 <1000ms；重跑哈希一致
    g2 = verdict["gate2_full_episodes"]
    assert g2["gate2_full_episodes_ok"] is True
    assert g2["gate3_determinism_ok"] is True
    assert [ep["seed"] for ep in g2["gate2_episodes"]] == [101, 102]
    for ep in g2["gate2_episodes"]:
        assert ep["statuses"] == ["DONE", "DONE"]
        assert ep["turns_played"] == 720
        assert ep["max_step_ms"] is not None and ep["max_step_ms"] < 1000.0
    assert g2["gate3_hashes"]["run1"] == g2["gate3_hashes"]["run2"]

    # 身份链段：盘上 main/tar sha 对 build_manifest.json 核对全匹配
    pkg = verdict["package"]
    assert pkg["match"] is True
    assert pkg["main_sha256"]["match"] is True
    assert pkg["tar_sha256"]["match"] is True
    manifest = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert pkg["main_sha256"]["manifest"] == manifest["main_sha256"]
    assert pkg["tar_sha256"]["manifest"] == manifest["tar_sha256"]
    assert pkg["tar_members"] == ["main.py"]
    assert pkg["tar_inner_main_matches_disk"] is True
    assert pkg["tar_size_ok"] is True


def test_divergent_steps_all_ge_648(launch_result):
    # ③附加断言差异步：与 _cxd_agent 基线的序列差异全部落在截断层区（step≥648）
    steps = launch_result["truncation_only_diff"]["divergent_steps"]
    assert isinstance(steps, list)
    assert all(isinstance(s, int) and s >= 648 for s in steps)
    trunc = json.loads(Path(launch_result["evidence_path"]).read_text(
        encoding="utf-8"))["truncation_only_diff"]
    assert trunc["l1_callable"] == "_cxs_agent"
    assert trunc["baseline_callable"] == "_cxd_agent"
    assert trunc["n_obs"] == 719
    assert trunc["all_divergent_steps_ge_threshold"] is True
    assert trunc["form_violations"] == []


def test_identity_chain_break_fails_closed(tmp_path):
    # ②身份链破坏：临时目录拷贝包件（不碰真 manifest），篡改期望 main sha
    pkg_copy = tmp_path / "orderbook_l1_derivative"
    pkg_copy.mkdir()
    for name in ("main.py", "submission.tar.gz", "build_manifest.json",
                 "layer_s_block.py"):
        shutil.copy2(_PKG / name, pkg_copy / name)
    manifest = json.loads(
        (pkg_copy / "build_manifest.json").read_text(encoding="utf-8"))
    manifest["main_sha256"] = "0" * 64          # 期望 sha 破坏（其余不动）
    (pkg_copy / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    result = gate.run(str(pkg_copy))
    assert result["passed"] is False
    assert result["gates"]["package"] is False
    verdict = json.loads(Path(result["evidence_path"]).read_text(encoding="utf-8"))
    assert verdict["package"]["main_sha256"]["match"] is False
    assert verdict["package"]["tar_sha256"]["match"] is True   # 未篡改面仍核对通过
    # fail-closed 早退：身份不明不驱动长局（四门未执行）
    assert verdict["fail_closed_early_exit"] is True
    assert verdict["gate2_full_episodes"] is None
    assert verdict["gate1_official_load"] is None
    # 真包 manifest 未被触碰
    assert json.loads(_MANIFEST.read_text(encoding="utf-8"))["main_sha256"] \
        != "0" * 64
