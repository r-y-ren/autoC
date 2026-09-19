# ===========================================================================
# P4.1 接合证明门（常驻，2026-09-19）—— v2 候选登记的前置门
# ---------------------------------------------------------------------------
# 背景：DTSP v1（submission 56342843）线上 19 局动作流与纯 v13.8 逐字节
#   一致（零接合），而 P3 全部本地测试接合正常。根因（本门钉死复现）：
#   官方 get_last_callable 在 exec 后 sys.path.pop() 掉解包目录（vendored
#   agent.py L50-64），v1 的黎明钩子在回合期 `import planner.runtime` 每
#   黎明 ModuleNotFoundError → entry 静默旗关 → 动作流与 v13.8 一致。
#   修复：main.py 装载期（append 窗口内）急切导入 planner 存入
#   DTSP_RUNTIME_MODULE；entry 钩子优先消费该名字。
# 本门在干净子进程（python -I，驱动脚本在解包目录之外——杜绝开发环
#   sys.path 污染）按官方语义装载"当前打包产物"并用灾难局
#   episode-110634204 的真实 obs 序列驱动，断言：
#     1) 官方装载语义锚点在 vendored agent.py 中在场（复刻保真）；
#     2) 装载后解包目录确不在 sys.path（门的保真自证：确实复现了 pop）；
#     3) planner.runtime 进过 sys.modules、DTSP_RUNTIME_MODULE 在命名空间、
#        PLANNER_ENABLED=True、无 hook_errors、trace.engaged=True；
#     4) 打包 agent 动作流与纯 v13.8 基线（同一 obs 流）分歧，且 d10 之后
#        分歧 ≥1 步（灾难局接合基准：d10 投影器选 C1@1.25×(-1)×0.90，
#        覆盖生效后动作流必变）。
# 此门不过 = 不许登记 v2（P4.1 任务包裁决）。
# ===========================================================================
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
AGENT_DIR = SOFTWARE / "kaggle_simulations" / "agent"
PROBE = SOFTWARE / "scripts" / "p41_official_load_probe.py"
REPLAY = SOFTWARE.parent / "references" / "data" / "online-replays" / \
    "round23" / "episode-110634204-replay.json"


def _load_probe_module():
    spec = importlib.util.spec_from_file_location("p41_official_load_probe",
                                                  str(PROBE))
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("p41_official_load_probe", module)
    spec.loader.exec_module(module)
    return module


def _ensure_fresh_archive():
    """门跑在当前源码的确定性重建上（先原位重建 submission.tar.gz）。"""
    result = subprocess.run([sys.executable, str(AGENT_DIR / "build.py")],
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, \
        f"build.py failed:\n{result.stdout}\n{result.stderr}"
    return result.stdout.strip().splitlines()[-2]  # sha256 行


def test_official_loader_semantics_pins_present():
    """装载语义复刻保真：vendored agent.py 必须仍含 append/pop/最后callable
    三锚点（上游语义变化 → 本门复刻假设需人工重审）。"""
    probe = _load_probe_module()
    assert probe._check_official_semantics_pins() is True


def test_packaged_bot_engages_on_disaster_replay_under_official_semantics():
    """接合证明门主断言（灾难局、双条件：trace.engaged + d10 后分歧）。"""
    assert REPLAY.is_file(), f"灾难局回放缺失: {REPLAY}"
    sha_line = _ensure_fresh_archive()
    probe = _load_probe_module()
    verdict = probe.run_probe(str(REPLAY), seat=0, max_steps=720)

    ev = verdict["evidence"]
    # —— 门的保真自证：loader 的 pop 确实发生（官方语义复刻有效）——
    assert ev["loader_pop_applied"] is True, \
        "门失效：装载复刻未执行 sys.path.pop（未复现官方语义）"
    # —— P4.1 修复生效证据 ——
    assert ev["has_DTSP_RUNTIME_CONFIG"] is True
    assert ev["has_DTSP_RUNTIME_MODULE"] is True, \
        "main.py 装载期急切导入缺失（DTSP_RUNTIME_MODULE 不在命名空间）"
    assert ev["planner_in_sys_modules"] is True
    assert ev["PLANNER_ENABLED"] is True
    assert ev["hook_errors"] == [], f"钩子报错: {ev['hook_errors']}"
    # —— 接合遥测 ——
    assert verdict["engaged"] is True, "trace.engaged=False：零接合"
    dawns = ev.get("dawn_records") or []
    selected = [d for d in dawns if d.get("selected")]
    assert selected, "无任何黎明完成计划注入"
    assert any(d.get("day") == 10 for d in dawns), "d10 黎明记录缺失"
    assert any(d.get("policy") == "rollout" for d in dawns), \
        "无 rollout 档黎明（孪生精化段未启动）"
    assert all("rung" in d or d.get("policy") != "rollout" for d in dawns)
    # —— 动作流分歧（接合基准：d10 后与纯 v13.8 可分辨）——
    assert verdict["n_mismatch"] >= 1, \
        f"打包动作流与纯 v13.8 完全一致（零接合）: {verdict['match_rate']}"
    assert verdict["mismatch_after_d10"] >= 1, \
        "d10 后无动作分歧（覆盖未生效）"
    print(f"[p41 gate] pkg {sha_line}\n"
          f"  mismatch={verdict['n_mismatch']}/{verdict['n_actions']} "
          f"first_mm={verdict['first_mismatch']} "
          f"after_d10={verdict['mismatch_after_d10']}\n"
          f"  dawns={len(dawns)} failopens={ev.get('failopens')} "
          f"selected={selected[0].get('selected')}")


def test_pristine_v1_failure_mode_is_documented():
    """归档证据：v1 包（ee19d2c7，线上 submission 56342843）在本门的
    干净子进程里零接合（match_rate=1.0、planner 从未导入）。登记表
    v2 时该证据链必须可追溯（exports/probes/p41_engagement/）。"""
    evidence_path = SOFTWARE / "exports" / "probes" / "p41_engagement" / \
        "official_load_probe.json"
    if not evidence_path.is_file():
        return  # 探针未跑过（v1 证据归档为可选；主门不依赖）
    saved = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert saved["pkg_sha256"].startswith("ee19d2c7"), \
        ("归档探针产物对应的不是 v1 提交包（重跑探针会覆盖本证据，"
         "v1 证据请另行归档）")
    assert saved["match_rate"] == 1.0 and saved["n_mismatch"] == 0
    assert saved["evidence"]["planner_in_sys_modules"] is False
