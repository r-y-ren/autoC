"""Track-B P3 集成测试：DTSP bot 内运行时（planner/runtime.py + entry 接线）。

覆盖任务包 P3 的六类验收面：
  1. 黎明调度正确性——非 h0 回合零规划开销（引擎不装载、不记轨迹）；
  2. 时间治理器——干池跳过规划沿用上日计划；假时钟注入下 deadline
     降级路径（rollout 提前收手/整段跳过）；
  3. fail-open 三道——注入异常后动作流与旗关 golden **逐字节一致**；
     已注入后再失败恢复 v13.8 原值；引擎指纹不符粘性关断；
  4. 对手模型运行时账本——obs 公开量守恒记账；
  5. 打包清单——planner+scene 成员、确定性、大小上限、scene 指纹；
  6. 端到端——4 种子全季旗开 DTSP 本地局：无超时、无异常、不崩溃。

机内预算：fail-open 黄金对比 1 个整季孪生自博弈（~3s）；端到端 4 局
官方引擎整季（DTSP 规划在环，~4min）——本文件是套件的主要新增耗时。
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import pytest

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))
# 装载语义说明（P4.1 修订，2026-09-19）：生产路径上 main.py 在装载期
# （loader append 窗口内）急切导入 planner 存入 DTSP_RUNTIME_MODULE——
# 官方 get_last_callable exec 后 pop 掉解包目录，回合期 sys.path 导入在
# 线上必败（v1 零接合根因，见 tests/test_p41_engagement_gate.py）。本
# 测试进程把 AGENT_DIR 插进 sys.path，为的是让 bench 裸命名空间的钩子
# 走"回合期回退导入"路径拿到与本文件相同的 planner.runtime 实例，
# monkeypatch/断言才真正咬合。
AGENT_DIR = SOFTWARE / "kaggle_simulations" / "agent"
if str(AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_DIR))

import planner.runtime as _rt_mod          # noqa: E402（与钩子同实例）

GOLDEN_PATH = SOFTWARE / "exports" / "probes" / "planner_flagoff" \
    / "golden_v138.json"
SEEDS = (11, 22, 33, 47, 58, 69)
E2E_SEEDS = (11, 22, 33, 47)

DEFAULT_CONFIG = {
    "enabled": True, "seed": 1, "budget_cap_s": 0.85,
    "rollout_models": ("pessimistic_fill",),
    "ladder": ((6, 1), (4, 2), (3, 3), (2, 4), (1, 6)),
}


def _load_golden_module():
    spec = importlib.util.spec_from_file_location(
        "planner_flagoff_golden_p3",
        str(SOFTWARE / "scripts" / "planner_flagoff_golden.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("planner_flagoff_golden_p3", module)
    spec.loader.exec_module(module)
    return module


def _fresh_ns(module):
    """按 main.py 同语义的裸 src 命名空间（含旗关默认），清运行态。"""
    _rt_mod.reset_state()
    ns = module.build_v138_namespace()
    return ns


def _synthetic_obs(module, player=1):
    head = module.synthetic_season_head(11)
    return head["steps"][0][player]["observation"]


@pytest.fixture()
def runtime():
    _rt_mod.reset_state()
    yield _rt_mod
    _rt_mod.reset_state()


# ===========================================================================
# 1. 黎明调度：非 h0 零开销；h0 才规划
# ===========================================================================
class TestDawnScheduling:

    def test_non_dawn_turn_is_zero_overhead(self, runtime):
        """hour!=0：不装载引擎、不记轨迹、不动命名空间。"""
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = _synthetic_obs(mod)
        obs = dict(obs)
        obs["hour"] = 7
        t0 = time.perf_counter()
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=3, hour=7)
        assert time.perf_counter() - t0 < 0.01
        assert runtime._STATE["engine"] is None      # 引擎都没装载
        assert runtime.trace()["dawns"] == []
        assert ns["PLANNER_ENABLED"] is False

    def test_dawn_hour_plans_and_applies(self, runtime):
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = _synthetic_obs(mod)
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=0, hour=0)
        assert ns["PLANNER_ENABLED"] is True
        assert ns.get("_DTSP_LAST_PLAN_KEY")
        assert ns["PLANNER_OVERRIDES"], "register must carry plan knobs"
        records = runtime.trace()["dawns"]
        assert len(records) == 1 and records[0]["policy"] in \
            ("rollout", "projector_only")

    def test_identical_obs_reuses_decision(self, runtime):
        """同 obs 重复调用：幂等重放注入，不重花预算（cache_hit 记录）。"""
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = _synthetic_obs(mod)
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=0, hour=0)
        plan = ns["_DTSP_LAST_PLAN_KEY"]
        ns["PLANNER_OVERRIDES"].clear()              # 人为破坏后重放
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=0, hour=0)
        assert ns["_DTSP_LAST_PLAN_KEY"] == plan     # 决策被重放
        assert ns["PLANNER_OVERRIDES"]               # 覆盖被重建
        records = runtime.trace()["dawns"]
        assert len(records) == 2
        assert records[-1]["policy"] == "cache_hit"  # 未重新规划
        assert records[-1]["elapsed_s"] < 0.05


# ===========================================================================
# 2. 时间治理器：干池跳过；假时钟 deadline 降级
# ===========================================================================
class TestTimeGovernor:

    def test_budget_formula_and_dry_pool(self, runtime):
        mod = _load_golden_module()
        cfg = dict(DEFAULT_CONFIG)
        obs = dict(_synthetic_obs(mod))
        obs["remainingOverageTime"] = 60
        budget, pool = runtime.dawn_budget(obs, 0, cfg)
        assert (budget, pool) == (0.85, 60.0)        # min(cap, 0.5+60/30*0.5)
        obs["remainingOverageTime"] = 0.1
        budget, pool = runtime.dawn_budget(obs, 10, cfg)
        assert budget == 0.0 and pool == 0.1         # 池枯 → 0

    def test_dry_pool_skips_planning_keeps_yesterday(self, runtime):
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = dict(_synthetic_obs(mod))
        obs["remainingOverageTime"] = 0.1            # ≤ base/2 → 跳过
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=5, hour=0)
        assert ns["PLANNER_ENABLED"] is False        # 未注入任何计划
        assert runtime.trace()["dawns"][-1]["policy"] == "keep_yesterday"

    def test_tiny_budget_skips_rollout_stage(self, runtime):
        """预算只够投影段：策略=projector_only（P2.6 配置仍可注入）。"""
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = dict(_synthetic_obs(mod))
        obs["remainingOverageTime"] = 60
        cfg = dict(DEFAULT_CONFIG, budget_cap_s=0.2,
                   rollout_gate_budget_s=0.35)
        runtime.dawn_hook(obs, ns, cfg, player=1, day=0, hour=0)
        record = runtime.trace()["dawns"][-1]
        assert record["policy"] == "projector_only"
        assert record["rollouts"] == 0
        assert ns["PLANNER_ENABLED"] is True
        assert record["elapsed_s"] < 0.3

    def test_fake_clock_deadline_degrades_to_projector(self, runtime,
                                                       monkeypatch):
        """假时钟：refinement 起点已过 deadline → 整段跳过、用当前最优。"""
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = _synthetic_obs(mod)
        fake = {"t": 100.0}
        monkeypatch.setattr(runtime, "_now", lambda: fake["t"])
        real_perf = time.perf_counter

        def advancing():
            fake["t"] += 0.02                        # 时间照走但恒超预算
            return real_perf()

        # t_start=100；deadline=100+0.85-0.06；refinement 门槛前 _now 恒
        # 返回 100+0.02*k —— 让 rung 挑选时可用预算足够、进入后立刻超限
        cfg = dict(DEFAULT_CONFIG)
        runtime.dawn_hook(obs, ns, cfg, player=1, day=0, hour=0)
        record = runtime.trace()["dawns"][-1]
        assert record["policy"] in ("projector_only", "rollout")
        if record["policy"] == "rollout":
            assert record["budget_s"] >= record["elapsed_s"] * 0.5

    def test_rollout_refinement_aborts_on_deadline(self, runtime):
        """逐时间片：refinement 内 deadline 到 → 用已完成的 rollout。"""
        mod = _load_golden_module()
        from kaggle_simulations.agent.planner import plans as plans_mod
        obs = _synthetic_obs(mod)
        from kaggle_simulations.agent.planner import twin as twin_mod
        bundle = twin_mod.load_engine()
        dawn_state = twin_mod.new_state_from_obs(obs, player=1, seed=1,
                                                 bundle=bundle)
        module = bundle.module
        summary = runtime.build_obs_summary(module, obs, 1, 0)
        candidates = plans_mod.enumerate_plans(summary)
        models = [__import__(
            "kaggle_simulations.agent.planner.opponents",
            fromlist=["opponents"]).PessimisticFill()]
        deadline = runtime._now() + 0.15              # 只够 1-2 条 rollout
        done, steps = runtime._rollout_refinement(
            bundle, dict(DEFAULT_CONFIG), deadline, dawn_state, 1,
            candidates, models, {}, [])
        assert steps >= 0
        assert len(done) <= len(candidates)
        for per_model in done.values():
            for score in per_model.values():
                assert isinstance(score, float)


# ===========================================================================
# 3. fail-open 三道
# ===========================================================================
class TestFailOpen:

    def test_injected_exception_action_stream_matches_flagoff_golden(
            self, runtime, monkeypatch):
        """三道之一（任意异常）：fail-open 后整季动作流与旗关 golden
        **逐字节一致**（种子 11 全季双席自博弈 sha256）。

        经 entry 接线全链驱动（agent(obs) 内的钩子），故模拟生产装载：
        main.py 会把包根插入 sys.path——这里同样插入后用顶层
        planner.runtime 实例（钩子 import 到的就是它）。"""
        assert GOLDEN_PATH.is_file()
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        expected = {row["seed"]: row["sha256"] for row in golden["seeds"]}

        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        ns["DTSP_RUNTIME_CONFIG"] = dict(DEFAULT_CONFIG)

        def _boom(*args, **kwargs):
            raise RuntimeError("injected planner explosion (test)")

        monkeypatch.setattr(_rt_mod._plans, "enumerate_plans", _boom)
        flag_on = mod.season_action_hash(ns["agent"], 11)
        assert flag_on["sha256"] == expected[11], (
            "fail-open 后动作流必须与旗关 golden 逐字节一致")
        assert _rt_mod._STATE["sticky_off"] is True
        assert ns["PLANNER_ENABLED"] is False
        assert _rt_mod.trace()["failopens"]

    def test_failopen_after_apply_restores_pristine_values(
            self, runtime, monkeypatch):
        """三道之二：已注入后次黎明失败 → 全部 governed 键回 v13.8 原值。

        v3 K1 注：d0 注入的计划可能就是 identity 守成点（直写键=原生值，
        无可观测偏离）——偏离前提改为人为破坏直写键（快照机制与选择的
        计划解耦）。"""
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = _synthetic_obs(mod)
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=0, hour=0)
        assert ns["PLANNER_ENABLED"] is True
        pristine = ns["_DTSP_PRISTINE_SNAPSHOT"]
        assert pristine                              # 快照在位
        # 人为偏离直写键（等同计划注入的偏离形态）
        ns["SE_DUE_DAY"] = 3
        ns["LAND_PLAN"] = {1: (2, 1700), 2: (5, 2700)}
        ns["STRAW_TOTAL_CAP_REGIME"] = 99

        def _boom(*args, **kwargs):
            raise ValueError("second-dawn failure (test)")

        monkeypatch.setattr(runtime._plans, "enumerate_plans", _boom)
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=1, hour=0)
        assert ns["PLANNER_ENABLED"] is False
        assert ns["PLANNER_OVERRIDES"] == {}
        for name, value in pristine.items():
            assert ns[name] == value, f"governed key {name} not restored"
        assert runtime.trace()["failopens"], "failopen telemetry missing"

    def test_fingerprint_mismatch_sticky_fail_open(self, runtime,
                                                   monkeypatch):
        """三道之三：引擎指纹不符 → 粘性关断 + 遥测记因。"""
        from kaggle_simulations.agent.planner import twin as twin_mod
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = _synthetic_obs(mod)

        def _drift():
            raise twin_mod.TwinFingerprintError("wheel sha256 漂移（测试）")

        monkeypatch.setattr(runtime, "resolve_engine", _drift)
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=0, hour=0)
        assert ns["PLANNER_ENABLED"] is False
        assert runtime._STATE["sticky_off"] is True
        fails = runtime.trace()["failopens"]
        assert fails and "TwinFingerprintError" in fails[0]
        # 粘性：后续黎明零开销直接返回
        runtime.dawn_hook(obs, ns, DEFAULT_CONFIG, player=1, day=1, hour=0)
        assert len(runtime.trace()["dawns"]) == 1

    def test_disabled_config_is_inert(self, runtime):
        mod = _load_golden_module()
        ns = _fresh_ns(mod)
        obs = _synthetic_obs(mod)
        runtime.dawn_hook(obs, ns, dict(DEFAULT_CONFIG, enabled=False),
                          player=1, day=0, hour=0)
        assert ns["PLANNER_ENABLED"] is False
        assert runtime.trace()["dawns"] == []


# ===========================================================================
# 4. 对手模型运行时账本（obs 公开量守恒）
# ===========================================================================
class TestOpponentLedger:

    def test_inflow_and_herd_recorded(self, runtime):
        mod = _load_golden_module()
        from kaggle_simulations.agent.planner import twin as twin_mod
        module = twin_mod.load_engine().module
        base = _synthetic_obs(mod, player=0)
        market = dict(base["market"])
        inventory = dict(market["inventory"])
        inventory["WHEAT"] = inventory.get("WHEAT", 0) + 30
        market["inventory"] = inventory
        obs_day3 = dict(base)
        obs_day3["day"] = 3
        obs_day3["market"] = market
        summary = runtime.build_obs_summary(module, obs_day3, 0, 3)
        history, inflow = runtime.update_opponent_ledger(
            obs_day3, 0, 3, summary)
        assert history == [] and inflow == {}        # 首黎明：只有基线
        market2 = dict(market)
        inventory2 = dict(inventory)
        inventory2["WHEAT"] = inventory["WHEAT"] + 12   # 又入市 12（含消费修正前）
        market2["inventory"] = inventory2
        obs_day4 = dict(base)
        obs_day4["day"] = 4
        obs_day4["market"] = market2
        summary4 = runtime.build_obs_summary(module, obs_day4, 0, 4)
        history, inflow = runtime.update_opponent_ledger(
            obs_day4, 0, 4, summary4)
        assert history and history[-1]["day"] == 3
        assert inflow["WHEAT"] >= 12                 # Δ库存+城镇消费 ≥ Δ
        assert isinstance(history[-1]["animal_buys"], int)


# ===========================================================================
# 5. 打包清单（build.py P3 扩展）
# ===========================================================================
class TestPackaging:

    def test_archive_members_scene_fingerprint_and_size(self):
        sys.path.insert(0, str(AGENT_DIR))
        spec = importlib.util.spec_from_file_location(
            "build_p3_test", str(AGENT_DIR / "build.py"))
        build = importlib.util.module_from_spec(spec)
        sys.modules.setdefault("build_p3_test", build)
        spec.loader.exec_module(build)
        data = build.build_bytes()
        assert len(data) < 300 * 1024, f"package too large: {len(data)}"
        assert data == build.build_bytes()           # 确定性（内存复建）
        import tarfile
        import io as _io
        with tarfile.open(fileobj=_io.BytesIO(data)) as tar:
            names = set(tar.getnames())
            blob = {m.name: tar.extractfile(m).read()
                    for m in tar.getmembers() if m.isfile()}
        for expected in ("main.py", "src/entry.py", "planner/__init__.py",
                         "planner/twin.py", "planner/plans.py",
                         "planner/opponents.py", "planner/select.py",
                         "planner/runtime.py",
                         "planner/scene/kaggriculture.py",
                         "planner/scene/kaggriculture.json"):
            assert expected in names, f"missing package member {expected}"
        import hashlib
        from kaggle_simulations.agent.planner import twin as twin_mod
        assert hashlib.sha256(
            blob["planner/scene/kaggriculture.py"]).hexdigest() == \
            twin_mod.SCENE_PY_SHA256
        assert hashlib.sha256(
            blob["planner/scene/kaggriculture.json"]).hexdigest() == \
            twin_mod.SCENE_JSON_SHA256
        assert build.precheck() is None              # 装载契约全过

    def test_on_disk_archive_matches_rebuild(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, str(AGENT_DIR / "build.py"), "--check"],
            capture_output=True, text=True)
        assert result.returncode == 0, \
            f"build.py --check failed:\n{result.stdout}\n{result.stderr}"


# ===========================================================================
# 6. 端到端：4 种子全季旗开 DTSP 本地局（官方引擎在环）
# ===========================================================================
class TestEndToEnd:

    def test_full_season_dtsp_selfplay_four_seeds(self, runtime):
        """4 种子全季：无超时（逐回合 <1s）、无异常、无 fail-open、
        完成 720 回合；终局资金对 golden 自博弈基线不崩塌（≥0.5×）。"""
        from kgenv.engine import run_episode
        mod = _load_golden_module()
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        golden_money = {row["seed"]: row["final_money"]
                        for row in golden["seeds"]}
        rt = _rt_mod                                  # 与钩子同实例
        results = {}
        for seed in E2E_SEEDS:
            rt.reset_state()
            inner = self._load_submission()
            times = []

            def timed_agent(obs):
                # co_argcount==1：框架按参数个数截断实参（obs, config），
                # 多一个默认参数都会被喂进 config。
                t0 = time.perf_counter()
                action = inner(obs)
                times.append(time.perf_counter() - t0)
                return action

            result = run_episode(timed_agent, timed_agent, seed=seed,
                                 episode_steps=720)
            assert result["statuses"] == ["DONE", "DONE"], \
                f"seed {seed}: {result['statuses']} {result.get('note')}"
            assert result["turns_played"] == 720
            assert times and max(times) < 1.0, \
                f"seed {seed}: agent call exceeded actTimeout " \
                f"({max(times):.3f}s)"
            assert not rt.trace()["failopens"], \
                f"seed {seed}: unexpected fail-open: {rt.trace()['failopens']}"
            policies = [d["policy"] for d in rt.trace()["dawns"]]
            assert policies, f"seed {seed}: no dawn planning happened"
            assert "failopen" not in policies
            pair_sum = sum(result["rewards"])
            golden_pair = sum(golden_money[seed])
            assert pair_sum >= 0.5 * golden_pair, (
                f"seed {seed}: DTSP selfplay pair {pair_sum:.0f} collapsed "
                f"vs golden {golden_pair:.0f}")
            results[seed] = {
                "rewards": result["rewards"],
                "max_turn_s": round(max(times), 4),
                "dawns": len(policies),
                "rollout_dawns": sum(1 for p in policies if p == "rollout"),
                "vs_golden_pair": round(pair_sum - golden_pair, 1),
                "switched": sum(1 for d in rt.trace()["dawns"]
                                if d.get("switched")),
            }
        (SOFTWARE / "exports" / "probes" / "p3_integration"
         / "e2e_selfplay.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=1),
            encoding="utf-8")

    @staticmethod
    def _load_submission():
        """main.py 装载（DTSP 总闸在位）；进程内复用避免重复 exec。"""
        cache = getattr(TestEndToEnd, "_agent", None)
        if cache is None:
            spec = importlib.util.spec_from_file_location(
                "submission_main_p3", str(AGENT_DIR / "main.py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules.setdefault("submission_main_p3", module)
            spec.loader.exec_module(module)
            cache = module.agent
            TestEndToEnd._agent = cache
        return cache
