"""离线基准主流程（14 局×注入点×双口径裁决：主口径 DTSP≥反应式、参考口径 history 代差修正），rollout 全部经 seated 通道，引擎异常 fail-closed 记异常局。

上游: R2（详见 fn_docs/responsibility.md）

实现要点（[改造]件，源语义=software/scripts/planner_offline_bench.py 主流程
——main() 的"注入集配置→逐局逐注入点→双口径裁决→输出 JSON"编排）：
- rollout/评估全部走本包下层：计划选择经 evaluate_plan_portfolio（J 矩阵
  逐计划×逐 ω 全 seated rollout + 聚合委托 robust_selection），反应式/
  DTSP/孪生核验三口径直接经 rollout_with_replay_opponent（显式 me_seat
  注入——旧恒 seat0 错位通道不复存在）。不 import 旧树 scripts/ 与
  planner 包；只 import 本包下层。
- 双口径裁决语义照旧（m7 修订，2026-09-19）：主口径=逐局中位注入点
  DTSP≥反应式（同执行器单变量，容差 -GATE_EPS），official 门=≥
  primary_gate_wins(9)/min_episodes(12) 局不劣 且 全集合 mean
  Δ(DTSP−反应式)>0；参考口径=对 history 净执行器代差修正——修正项
  offset=同注入点反应式对 history（mean(reactive)−mean(truth)），修正后
  mean(DTSP−history)−offset ≥ −GATE_EPS（报告显式分解三字段：
  dtsp_vs_history / reactive_vs_history_offset / dtsp_vs_history_corrected）。
- 孪生核验（twin_noise）经 seated 通道等价重建：我席注入"回放 persona"
  callable（第 i 次调用回放官方动作流的 me 席动作），对席=回放动作——
  双席均按官方动作流重演，语义=旧 deps["run_to_end"] 核验。
- 败因归因照旧（attribute_failure 逐句迁移：twin_noise 优先→oracle
  重演判 opponent_model_gap→否则 plan_space_gap）；oracle 重演改经本包
  seated 通道逐候选 rollout（投影排序 top-K，含选中者）。
- 引擎异常 fail-closed 记异常局（本层新增，旧码异常即崩）：逐局 try/except
  → abnormal_episodes 记 {局号, 错误} 后继续整批（含回放缺失/指纹不符/
  注入步非法等一切单局失败）；全局性配置错误（空计划空间/缺反应式工厂/
  me_seat 非法/official 注入日不足）仍前置抛 ValueError。
- 旧 v13 装载面外置：旧 build_v13_namespace/v13_factory/旋钮覆盖由调用方
  装配为 plan_space 的 agent_factory 与 reactive_factory（逐 rollout 全新
  装载防串态语义由工厂形态承载）；旧 reactive_proxy 降级与
  overrides_skipped 清单不迁（显式工厂无降级路径）。
- 旧 find_episodes 发现与回放装载外置为调用方职责：episodes 直给回放
  映射（in-memory）。

输入配置结构登记（读旧码定真值：旧 main() argparse+evaluate_injection cfg
→ 新 injection_config 单 dict；me_seat 说明=台面默认席位，逐局可被条目
覆盖——旧 --team 的 TeamNames 席位推导属调用方发现逻辑）：
  injection_config 键：
    mode: "official"|"smoke"（旧 --mode，缺省 smoke；official 激活门禁）
    episodes: [局条目 Mapping]（每条：episode 局号 str / replay 回放映射
      （含非空 steps；rewards 缺省 [0,0]）/ me_seat 0|1 可选（缺省顶层）/
      round·opponent·mirror 元数据可选）
    injection_days: [int]（旧 --injection-days；缺省 official=(3,10,20)、
      smoke=(10,)；official 要求 ≥3，否则前置 ValueError——旧 exit 2）
    limit: int（旧 --limit；缺省 official=14、smoke=3；截 episodes）
    min_episodes: int（旧常量 12/3，可覆写）
    primary_gate_wins: int（旧常量 9）
    plan_space: [(plan_key, agent_factory)]（旧 enumerate_plans 外置：
      plan_key 可哈希进 J 矩阵；agent_factory=0 参工厂 fn()->agent）
    reactive_factory: 0 参工厂 fn()->agent（旧 v13_factory(None) 反应式臂）
    strategy/trim_fraction/weights/identity_key/plan_cap: 聚合参数透传
      evaluate_plan_portfolio（缺省 trimmed_mean/下层默认 0.25/None/
      None/120）
    oracle: bool（缺省=mode=="official"，旧 --no-oracle 反转）
    oracle_top_k: int（缺省 6）
    gate_eps/twin_noise_eps: float（旧常量 1.0/1.0）
    out_path: 可选——报告 JSON 落盘路径（旧 --out-dir/bench_report.json
      内联为单文件路径）
  opponent_models: Ω 成员序列（"名"=回放真实对手（公平性口径照旧）或
    ("名", opponent_factory)——旧 build_default_models 装配外置）
  me_seat: int 0|1（台面默认我方席位）

返回（=旧 bench_report.json 结构，去 team/reactive_proxy/overrides_skipped，
增 abnormal_episodes/me_seat/exit_code）：{mode, me_seat, generated_at_utc,
wall_seconds, configuration, criterion_note, opponent_models(Ω 名单——旧为
model.describe() 注记串，新架构 Ω 由调用方装配，登记名单), episodes(逐局
双口径裁决), abnormal_episodes, skipped_episodes, rows(逐注入点四口径行),
summary, exit_code(0=smoke 摇通或 official 过门；1=official 门未过/局数
不足——旧 exit 0/1 语义)}。
"""

from __future__ import annotations

import json
import statistics
import time
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path

from run_official_bench.evaluate_plan_portfolio import (
    MAX_PLAN_CANDIDATES,
    evaluate_plan_portfolio,
)
from run_official_bench.rollout_with_replay_opponent import (
    make_twin_deps,
    rollout_with_replay_opponent,
)

__all__ = ["run_official_bench", "select_injection_steps", "attribute_failure",
           "GATE_EPS", "TWIN_NOISE_EPS", "OFFICIAL_INJECTION_DAYS",
           "SMOKE_INJECTION_DAYS", "OFFICIAL_MIN_EPISODES",
           "SMOKE_MIN_EPISODES", "OFFICIAL_LIMIT", "SMOKE_LIMIT",
           "OFFICIAL_PRIMARY_GATE_WINS", "ORACLE_TOP_K"]

# ---- 旧码常量照旧登记（planner_offline_bench.py:65-75）----
OFFICIAL_INJECTION_DAYS = (3, 10, 20)
SMOKE_INJECTION_DAYS = (10,)
OFFICIAL_MIN_EPISODES = 12
SMOKE_MIN_EPISODES = 3
OFFICIAL_LIMIT = 14
SMOKE_LIMIT = 3
OFFICIAL_PRIMARY_GATE_WINS = 9   # official 主口径 ≥9/14 局不劣门
ORACLE_TOP_K = 6                 # 败因归因 oracle 重演候选数（含选中者）
GATE_EPS = 1.0                   # 终局资金比较容差（float 噪声）
TWIN_NOISE_EPS = 1.0             # 孪生重演 vs 真值的逐位一致容差

CRITERION_NOTE = (
    "m7 修订双口径（2026-09-19；seated 通道迁移）：主口径=逐局中位注入点 "
    "DTSP≥反应式（同执行器单变量），official 需 ≥9/12 局不劣且全集合 "
    "mean Δ(DTSP−反应式)>0；参考口径=DTSP 对 history 减执行器代差 "
    "offset（=同注入点反应式对 history）后逐局不劣。两口径在注入点层面"
    "代数同构（DTSP−history−(反应式−history)≡DTSP−反应式），差别只在"
    "聚合统计（主=中位数、参考=均值）与归因框架。")


# --------------------------------------------------------------------------
# 纯函数（planner_offline_bench.py:82-89 / 152-181 逐句迁移）
# --------------------------------------------------------------------------
def select_injection_steps(n_steps, days):
    """注入步 = 各 dawn（day×24）；钳到可回放范围、去重升序。"""
    if n_steps < 2:
        raise ValueError(
            f"n_steps={n_steps!r} 太小，无法注入"
            f"（示例：720 步回放应传 len(steps)）")
    upper = n_steps - 2            # 留至少 1 步可 rollout
    return sorted({min(int(d) * 24, upper) for d in days if int(d) >= 0})


def attribute_failure(twin_noise, truth, reactive, dtsp, oracle_best,
                      oracle_key, dtsp_key, eps=GATE_EPS):
    """败因归因（判据失败时逐局输出；字段恒在、布尔值）。

    顺序：twin_noise 优先（孪生重演不逐位 => 其他 delta 不可信）；
    其次 oracle 重演若存在非选中候选显著胜过选中者且越过 reactive =>
    opponent_model_gap（对手模型误导排序）；否则 plan_space_gap
    （枚举面上没有计划能在真执行器上胜出/被选中者已是面内最优）。"""
    fail_d = (dtsp < truth - eps) or (dtsp < reactive - eps)
    result = {"judge_fail": fail_d, "twin_noise": False,
              "opponent_model_gap": False, "plan_space_gap": False,
              "reason": ""}
    if not fail_d:
        result["reason"] = "pass"
        return result
    if float(twin_noise) > TWIN_NOISE_EPS:
        result["twin_noise"] = True
        result["reason"] = (f"twin 重演偏差 {twin_noise:.1f} > "
                            f"{TWIN_NOISE_EPS}，孪生口径不可信")
        return result
    if oracle_best is not None and oracle_key != dtsp_key \
            and oracle_best > dtsp + eps and oracle_best > reactive + eps:
        result["opponent_model_gap"] = True
        result["reason"] = (f"oracle 候选 {oracle_key} 终局 {oracle_best:.0f}"
                            f" > 选中 {dtsp_key} {dtsp:.0f}：对手模型误导排序")
        return result
    result["plan_space_gap"] = True
    result["reason"] = ("枚举面内无候选在真执行器上显著越过选中者/反应式"
                        f"（oracle_best={oracle_best}）")
    return result


# --------------------------------------------------------------------------
# 内部件
# --------------------------------------------------------------------------
def _make_replay_persona(actions, me_seat, start):
    """回放 persona：第 i 次调用返回官方动作流第 start+i 步的 me 席动作。

    经 seated 通道注入我席后与"对席=回放动作"合流，即双席均按官方动作流
    重演——旧孪生核验（deps["run_to_end"](state, acts[start:])）的 seated
    等价重建。i 与通道推进计数逐一对齐（每步恰一次调用），循环守卫保证
    索引不越界。"""
    counter = [0]

    def persona(obs):                                  # noqa: ARG001
        index = start + counter[0]
        counter[0] += 1
        return actions[index][int(me_seat)]
    return persona


def _factory_by_key(plan_space, key):
    """按 plan_key 取 agent_factory（旧 _spec_by_key；不在集内即抛）。"""
    for plan_key, factory in plan_space:
        if plan_key == key:
            return factory
    sample = plan_space[0][0] if plan_space else None
    raise RuntimeError(f"排序键 {key!r} 不在候选集（示例：{sample!r} 在集内）")


def _evaluate_injection(deps, replay, me, inj, episode_id, plan_space, omega,
                        omega_names, reactive_factory, agg_kwargs, plan_cap,
                        oracle_enabled, oracle_top_k):
    """单注入点评估：真值/孪生核验/反应式/DTSP 四口径 + 败因归因。

    （=旧 evaluate_injection 的 seated 迁移：计划选择段内联展开为
    evaluate_plan_portfolio 调用，C/D 两臂 rollout 换 seated 通道。）

    返回行 dict（报告 rows 成员；异常原样上抛→调用方记异常局）。"""
    day = inj // 24
    truth = [float(x) for x in replay.get("rewards") or [0.0, 0.0]]

    # B) 孪生按官方动作流重演核验（seated 等价重建）→ twin_noise
    acts = deps["transition_actions"](replay)
    twin_final = rollout_with_replay_opponent(
        replay, inj, _make_replay_persona(acts, me, inj), me, deps=deps)
    twin_noise = abs(float(twin_final[me]) - truth[me])

    # D-选择) 计划组合评估：J(plan,ω) 逐格 seated rollout → robust_selection
    portfolio = evaluate_plan_portfolio(
        plan_space, omega, inj, replay, me, deps=deps, plan_cap=plan_cap,
        **agg_kwargs)
    best_key = portfolio["best"]

    # C) 反应式基线（调用方反应式臂工厂；对手=回放真实动作）
    reactive_final = rollout_with_replay_opponent(
        replay, inj, reactive_factory(), me, deps=deps)

    # D) DTSP：选中计划同孪生同对手（公平性单变量口径照旧）
    best_factory = _factory_by_key(plan_space, best_key)
    dtsp_final = rollout_with_replay_opponent(
        replay, inj, best_factory() if best_factory is not None else None,
        me, deps=deps)

    # 败因归因（判据失败且孪生可信才花 oracle 预算）
    oracle_best, oracle_key = None, None
    attribution = attribute_failure(
        twin_noise, truth[me], reactive_final[me], dtsp_final[me],
        oracle_best, oracle_key, best_key)
    if attribution["judge_fail"] and not attribution["twin_noise"] \
            and oracle_enabled:
        oracle_best, oracle_key = _oracle_rerun(
            deps, replay, me, inj, plan_space, portfolio["ranking"],
            best_key, top_k=oracle_top_k)
        attribution = attribute_failure(
            twin_noise, truth[me], reactive_final[me], dtsp_final[me],
            oracle_best, oracle_key, best_key)

    return {
        "episode": episode_id, "step": inj, "day": day, "me_seat": me,
        "truth_me": truth[me],
        "twin_resim_me": float(twin_final[me]),
        "twin_noise": twin_noise,
        "reactive_me": float(reactive_final[me]),
        "dtsp_me": float(dtsp_final[me]),
        "dtsp_vs_history": float(dtsp_final[me]) - truth[me],
        "dtsp_vs_reactive": float(dtsp_final[me])
        - float(reactive_final[me]),
        "best_plan": best_key, "n_plans": portfolio["n_plans"],
        "n_omega": portfolio["n_omega"],
        "plan_ranking_top3": [k for k, _ in portfolio["ranking"][:3]],
        "tie_break": portfolio["tie_break"],
        "opponent_models": omega_names,
        "oracle_best": oracle_best, "oracle_key": oracle_key,
        "judge_fail": attribution["judge_fail"],
        "twin_noise_flag": attribution["twin_noise"],
        "opponent_model_gap": attribution["opponent_model_gap"],
        "plan_space_gap": attribution["plan_space_gap"],
        "attribution_reason": attribution["reason"],
    }


def _oracle_rerun(deps, replay, me, inj, plan_space, ranking, best_key,
                  top_k):
    """败因归因 oracle：投影排序 top-K 候选各按真实对手 seated rollout 一次。"""
    top = [k for k, _ in ranking[:max(1, int(top_k))]]
    if best_key not in top:
        top = [best_key] + top[:max(0, int(top_k) - 1)]
    best_final, best_name = None, None
    for key in top:
        factory = _factory_by_key(plan_space, key)
        final = rollout_with_replay_opponent(
            replay, inj, factory() if factory is not None else None,
            me, deps=deps)
        me_value = float(final[me])
        if best_final is None or me_value > best_final:
            best_final, best_name = me_value, key
    return best_final, best_name


def _resolve_config(injection_config, opponent_models, me_seat):
    """配置解析与前置校验（fail-closed：结构性错误整批抛，不留到局级）。"""
    if not isinstance(injection_config, Mapping):
        raise ValueError(
            f"injection_config 必须为映射, got {type(injection_config).__name__}")
    mode = injection_config.get("mode", "smoke")
    if mode not in ("official", "smoke"):
        raise ValueError(f"mode 必须 official|smoke, got {mode!r}")
    official = mode == "official"

    days = list(injection_config.get("injection_days")
                or (OFFICIAL_INJECTION_DAYS if official
                    else SMOKE_INJECTION_DAYS))
    days = [int(d) for d in days]
    if official and len(days) < 3:
        raise ValueError(f"official 模式要求 >=3 个注入日（当前 {days}）")

    episodes = list(injection_config.get("episodes") or [])
    limit = int(injection_config.get("limit")
                or (OFFICIAL_LIMIT if official else SMOKE_LIMIT))
    episodes = episodes[:limit]

    plan_space = list(injection_config.get("plan_space") or [])
    if not plan_space:
        raise ValueError("计划空间为空：plan_space 需非空 (plan_key, "
                         "agent_factory) 序列（旧 enumerate_plans 空集即 "
                         "RuntimeError）")
    omega = list(opponent_models or [])
    if not omega:
        raise ValueError("对手模型集 Ω 为空：opponent_models 需非空"
                         "（成员=裸名或 (名, 工厂)）")
    omega_names = [m if isinstance(m, str) else m[0] for m in omega]

    me = int(me_seat)
    if me not in (0, 1):
        raise ValueError(f"me_seat 必须为 0 或 1, got {me_seat!r}")
    reactive_factory = injection_config.get("reactive_factory")
    if not callable(reactive_factory):
        raise ValueError("缺反应式基线工厂：reactive_factory 需为 0 参工厂"
                         " fn() -> agent（旧 v13_factory(None) 反应式臂）")

    strategy = injection_config.get("strategy", "trimmed_mean")
    trim_fraction = injection_config.get("trim_fraction")
    agg_kwargs = {"strategy": strategy,
                  "weights": injection_config.get("weights"),
                  "identity_key": injection_config.get("identity_key")}
    if trim_fraction is not None:
        agg_kwargs["trim_fraction"] = float(trim_fraction)

    return {
        "mode": mode, "official": official, "injection_days": days,
        "limit": limit, "episodes": episodes, "plan_space": plan_space,
        "omega": omega, "omega_names": omega_names, "me_seat": me,
        "reactive_factory": reactive_factory, "agg_kwargs": agg_kwargs,
        "plan_cap": injection_config.get("plan_cap", MAX_PLAN_CANDIDATES),
        "min_episodes": int(injection_config.get("min_episodes")
                            or (OFFICIAL_MIN_EPISODES if official
                                else SMOKE_MIN_EPISODES)),
        "primary_gate_wins": int(injection_config.get(
            "primary_gate_wins", OFFICIAL_PRIMARY_GATE_WINS)),
        "oracle": bool(injection_config.get("oracle", official)),
        "oracle_top_k": int(injection_config.get("oracle_top_k",
                                                 ORACLE_TOP_K)),
        "gate_eps": float(injection_config.get("gate_eps", GATE_EPS)),
        "twin_noise_eps": float(injection_config.get("twin_noise_eps",
                                                     TWIN_NOISE_EPS)),
        "out_path": injection_config.get("out_path"),
    }


def _episode_summary(episode_id, meta, ep_rows):
    """逐局双口径裁决（旧 main 汇总段数学照旧：主=中位、参考=均值修正）。"""
    def mean(key):
        return sum(r[key] for r in ep_rows) / len(ep_rows)

    d_hist = mean("dtsp_vs_history")
    d_react = mean("dtsp_vs_reactive")
    med_react = statistics.median(r["dtsp_vs_reactive"] for r in ep_rows)
    primary_pass = med_react >= -GATE_EPS
    mean_offset = mean("reactive_me") - mean("truth_me")
    corrected = d_hist - mean_offset
    reference_pass = corrected >= -GATE_EPS
    fails = [r for r in ep_rows if r["judge_fail"]]
    return {
        "episode": episode_id, "round": meta.get("round"),
        "me_seat": meta["me_seat"], "opponent": meta.get("opponent"),
        "mirror": bool(meta.get("mirror")), "n_injections": len(ep_rows),
        "mean_truth_me": mean("truth_me"),
        "mean_reactive_me": mean("reactive_me"),
        "mean_dtsp_me": mean("dtsp_me"),
        "dtsp_vs_history": d_hist, "dtsp_vs_reactive": d_react,
        "median_dtsp_vs_reactive": med_react,
        "primary_pass": primary_pass,
        "reactive_vs_history_offset": mean_offset,
        "dtsp_vs_history_corrected": corrected,
        "reference_pass": reference_pass,
        "gate_pass": primary_pass,      # 兼容键=主口径
        "fail_attribution": {
            "twin_noise": sum(1 for r in fails if r["twin_noise_flag"]),
            "opponent_model_gap": sum(1 for r in fails
                                      if r["opponent_model_gap"]),
            "plan_space_gap": sum(1 for r in fails if r["plan_space_gap"]),
        },
    }


# --------------------------------------------------------------------------
# 顶层：离线基准主流程
# --------------------------------------------------------------------------
def run_official_bench(injection_config, opponent_models, me_seat,
                       deps=None):
    """离线基准主流程：逐局逐注入点四口径评估 → 双口径裁决 → 报告 dict。

    Args:
        injection_config: 注入集配置（结构登记见模块头"输入配置结构登记"节；
            键=mode/episodes/injection_days/limit/plan_space/reactive_factory/
            strategy/trim_fraction/weights/identity_key/plan_cap/
            min_episodes/primary_gate_wins/oracle/oracle_top_k/gate_eps/
            twin_noise_eps/out_path）。
        opponent_models: 对手模型集 Ω（成员="名"（回放真实对手）或
            ("名", opponent_factory)）；只作用于 DTSP 计划选择，不改变
            C/D 轨迹对手——公平性单变量口径照旧。
        me_seat: 台面默认我方席位 0|1（逐局可被 episodes 条目 me_seat 覆盖）。
        deps: rollout 依赖组（make_twin_deps 形状；None=默认 twin 组，引擎
            装载含 fail-closed 指纹校验）。

    Returns:
        报告 dict（=旧 bench_report.json 结构，结构登记见模块头"返回"节；
        summary.exit_code：smoke 恒 0；official 门过 0、未过/局数不足 1）。

    Raises:
        ValueError: 结构性配置错误（空计划空间/空 Ω/缺 reactive_factory/
            me_seat 非法/official 注入日不足/mode 非法）。单局引擎异常
            （含回放缺失、指纹不符）**不抛**——记 abnormal_episodes 留因
            后继续整批（fail-closed 记异常局，契约"错误"面）。
    """
    t_start = time.time()
    cfg = _resolve_config(injection_config, opponent_models, me_seat)
    deps_eff = deps if deps is not None else make_twin_deps()

    rows, episode_rows, abnormal, skipped = [], [], [], []
    for position, entry in enumerate(cfg["episodes"]):
        episode_id = (str(entry.get("episode"))
                      if isinstance(entry, Mapping)
                      and entry.get("episode") is not None
                      else f"episode_{position}")
        try:
            if not isinstance(entry, Mapping):
                raise ValueError(f"局条目非映射: {type(entry).__name__}")
            ep_me = entry.get("me_seat")
            ep_me = cfg["me_seat"] if ep_me is None else int(ep_me)
            if ep_me not in (0, 1):
                raise ValueError(f"me_seat 必须为 0 或 1, "
                                 f"got {entry.get('me_seat')!r}")
            replay = entry.get("replay")
            if not isinstance(replay, Mapping) \
                    or not (replay.get("steps") or []):
                raise ValueError("回放缺失: 局条目需含非空 steps 的 replay 映射")
            n_steps = len(replay["steps"])
            inj_steps = select_injection_steps(n_steps, cfg["injection_days"])
            if len(inj_steps) < (3 if cfg["official"] else 1):
                skipped.append({"episode": episode_id,
                                "reason": f"注入步不足: steps={n_steps}"})
                continue
            ep_rows = []
            for inj in inj_steps:
                row = _evaluate_injection(
                    deps_eff, replay, ep_me, inj, episode_id,
                    cfg["plan_space"], cfg["omega"], cfg["omega_names"],
                    cfg["reactive_factory"], cfg["agg_kwargs"],
                    cfg["plan_cap"], cfg["oracle"], cfg["oracle_top_k"])
                row["round"] = entry.get("round")
                row["mirror"] = bool(entry.get("mirror"))
                row["opponent"] = entry.get("opponent")
                ep_rows.append(row)
            rows.extend(ep_rows)       # 全注入点成功才提交（异常局不留半程行）
            episode_rows.append((episode_id, entry, ep_me, ep_rows))
        except Exception as exc:       # noqa: BLE001 单局 fail-closed 记异常局
            abnormal.append({"episode": episode_id,
                             "error": f"{type(exc).__name__}: {exc}"})

    episode_summaries = [
        _episode_summary(episode_id, dict(entry, me_seat=ep_me), ep_rows)
        for episode_id, entry, ep_me, ep_rows in episode_rows]

    enough = len(episode_summaries) >= cfg["min_episodes"]
    n_primary = sum(1 for e in episode_summaries if e["primary_pass"])
    n_reference = sum(1 for e in episode_summaries if e["reference_pass"])
    pooled_mean_d_react = (sum(r["dtsp_vs_reactive"] for r in rows)
                           / len(rows)) if rows else 0.0
    # official 门禁（m7 修订主口径）：≥primary_gate_wins/min_episodes 局中位
    # 不劣 且 全集合 mean Δ>0；smoke 只摇通 harness，门禁值恒 False。
    all_pass = bool(cfg["official"] and enough
                    and n_primary >= cfg["primary_gate_wins"]
                    and pooled_mean_d_react > 0.0)
    exit_code = 0 if (not cfg["official"] or all_pass) else 1

    report = {
        "mode": cfg["mode"], "me_seat": cfg["me_seat"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "wall_seconds": round(time.time() - t_start, 1),
        "configuration": {
            "injection_days": cfg["injection_days"], "limit": cfg["limit"],
            "min_episodes": cfg["min_episodes"],
            "primary_gate_wins": cfg["primary_gate_wins"],
            "strategy": cfg["agg_kwargs"]["strategy"],
            "trim_fraction": cfg["agg_kwargs"].get("trim_fraction"),
            "weights": cfg["agg_kwargs"]["weights"],
            "plan_cap": cfg["plan_cap"],
            "identity_key": cfg["agg_kwargs"]["identity_key"],
            "n_plan_space": len(cfg["plan_space"]),
            "n_omega": len(cfg["omega"]),
            "gate_eps": cfg["gate_eps"],
            "twin_noise_eps": cfg["twin_noise_eps"],
            "oracle": cfg["oracle"], "oracle_top_k": cfg["oracle_top_k"],
        },
        "criterion_note": CRITERION_NOTE,
        "opponent_models": cfg["omega_names"],
        "episodes": episode_summaries,
        "abnormal_episodes": abnormal,
        "skipped_episodes": skipped,
        "rows": rows,
        "summary": {
            "episodes_evaluated": len(episode_summaries),
            "episodes_passed": n_primary,
            "episodes_passed_reference": n_reference,
            "episodes_abnormal": len(abnormal),
            "injections_evaluated": len(rows),
            "gates_all_pass": bool(all_pass),
            "enough_episodes": bool(enough),
            "pooled_mean_dtsp_vs_reactive": pooled_mean_d_react,
            "mean_dtsp_vs_history": (sum(e["dtsp_vs_history"]
                                         for e in episode_summaries)
                                     / len(episode_summaries))
            if episode_summaries else 0.0,
            "mean_dtsp_vs_reactive": (sum(e["dtsp_vs_reactive"]
                                          for e in episode_summaries)
                                      / len(episode_summaries))
            if episode_summaries else 0.0,
            "attribution_totals": {
                key: sum(1 for r in rows
                         if r.get("judge_fail") and r[key])
                for key in ("twin_noise_flag", "opponent_model_gap",
                            "plan_space_gap")
            },
            "exit_code": exit_code,
        },
    }

    if cfg["out_path"] is not None:
        out = Path(cfg["out_path"])
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2,
                      sort_keys=True)

    return report
