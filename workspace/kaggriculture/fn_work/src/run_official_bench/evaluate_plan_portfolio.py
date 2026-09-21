"""计划枚举×对手模型集的评估编排（枚举≤帽/逐计划逐对手 seated rollout/聚合委托 robust_selection）。

上游: R2（详见 fn_docs/responsibility.md）

实现要点（[改造]件，源语义=software/scripts/planner_offline_bench.py 的
DTSP 计划评估段——evaluate_injection 内 enumerate→J 矩阵→robust_select
编排，签名真值自旧码登记）：
- 枚举≤帽：旧码经旧树 plans.enumerate_plans(obs_summary) 产 ≤120 候选
  （plans.py:57 MAX_PLAN_CANDIDATES=120，"任务包"硬帽；超帽截断且
  identity 守成点豁免恒在——enumerate_plans_audited 尾段语义）。本层只
  import 两下层，消费调用方枚举好的 plan_space 并重施同一硬帽：保持
  调用方枚举序截断 + identity 豁免（被截掉时换入末位）。差异注记：旧码
  截断前按"贴近基线序"（quota_scale/land_due_shift 等 PlanSpec 内部键）
  排 grid 计划——该序由旧树枚举器产出，plan_space 已携带，本层不重排。
- 逐计划逐对手评估：旧 J(plan,ω) 矩阵 = plans.project_season 解析投影；
  按 R2 改造指令，投影面全部换 seated rollout 实测——J[plan][ω] =
  rollout_with_replay_opponent(replay, injection_point, plan 执行器,
  me_seat) 终局资金的 **me_seat 位**（旧恒 seat0 注入的错位口径不复
  存在；ω 的解析供给压价面由调用方构建 Ω 对手 callable 时自行消费）。
- 对手席位口径照旧（公平性单变量对比）：Ω 成员为裸名 → 对手席=回放
  真实动作（与旧 bench "Ω 只作用于计划选择、不改变轨迹对手"一致）；
  成员为 (名, callable) → 模型驱动对手席（旧树 opponents.OpponentModel
  的 propose_actions 本就是"孪生 rollout 中对手席动作"接口），经
  deps["step"] 包装就位——seated 通道形状与 me_seat 语义不动。
- 聚合委托：旧 select.robust_select(j_matrix, strategy/weights/
  trim_fraction/identity_key) → 本层 fn_work robust_selection（R3 值序
  语义），参数原位透传；本层不重复实现任何裁切/决胜。
- 注入点语义照旧：injection_point 原样透传 seated 通道（0=d0 全季；
  中间步先按官方动作流重演至该步再接管）。
- 旧树只读消费：不 import 旧树 scripts/ 与 planner 包（枚举器/Ω 模型的
  适配是调用方 run_official_bench 的职责）；只 import 两下层——本包
  rollout_with_replay_opponent 与 robust_selection 包。
- 纪律：stdlib-only、确定性（计划/Ω 按调用方序迭代，键序由下层排序）。

签名登记（fn_docs 意图 → 旧码真值）：旧 evaluate_injection(deps,
replay, me_seat, inj_step, cfg) 内联编排 → 新 evaluate_plan_portfolio(
plan_space, omega, injection_point, replay, me_seat, deps=None, *,
strategy, weights, trim_fraction, identity_key, plan_cap)——cfg 聚合
四参显式化，obs_summary/枚举器外置为 plan_space（调用方枚举+配对执行
器），返回在 robust_selection 结果上叠加评估面（j_matrix/n_plans/
n_omega/plan_cap/capped）。
"""

from __future__ import annotations

from run_official_bench.rollout_with_replay_opponent import (
    make_twin_deps,
    rollout_with_replay_opponent,
)
from robust_selection.robust_selection import (
    DEFAULT_TRIM_FRACTION,
    robust_selection,
)

__all__ = ["evaluate_plan_portfolio", "MAX_PLAN_CANDIDATES"]

# 枚举硬上限（源语义=旧树 planner/plans.py:57 MAX_PLAN_CANDIDATES=120，
# "任务包"硬帽；本模块不 import 旧树 planner 包，按值重登记——升帽须与
# 旧树两处同步）。
MAX_PLAN_CANDIDATES = 120


def _apply_plan_cap(plans, plan_cap, identity_key):
    """枚举≤帽：超帽截断到帽内 + identity 守成点豁免（恒在，被截掉则
    换入末位）；帽内原样。保持调用方枚举序（贴近基线序属旧树枚举器，
    plan_space 已携带——见模块头差异注记）。plan_cap=None 不施帽。"""
    if plan_cap is None or len(plans) <= int(plan_cap):
        return list(plans)
    kept = list(plans[:int(plan_cap)])
    if identity_key is not None and kept \
            and identity_key not in {key for key, _ in kept}:
        identity_entry = next(
            (entry for entry in plans if entry[0] == identity_key), None)
        if identity_entry is not None:
            kept[-1] = identity_entry
    return kept


def _deps_with_model_opponent(base_deps, opponent_factory, me_seat):
    """ω 驱动对手席的依赖组包装：仅替换 deps["step"]——推进前把对手席
    槽位改写为 ω callable 就地生成的动作（通道读到的"回放对手动作"被
    覆写；seated 通道形状、me_seat 语义、其余依赖键不动）。

    本函数逐 rollout 调用一次，opponent_factory 在此实例化——对手执行器
    与计划侧 agent_factory 同语义"逐 rollout 全新装载"防串态。
    opponent_factory=None 原样返回（含 None → 通道内默认 twin 依赖组，
    对手=回放真实动作——公平性口径照旧）；base_deps 需包装而非 None 时
    物化 make_twin_deps() 默认组（与通道内默认同源）。"""
    if opponent_factory is None:
        return base_deps
    base = base_deps if base_deps is not None else make_twin_deps()
    base_step = base["step"]
    opp = 1 - int(me_seat)
    opponent_callable = opponent_factory()

    def step(state, pair):
        pair = list(pair)
        pair[opp] = opponent_callable(state.seats[opp].observation)
        return base_step(state, pair)

    wrapped = dict(base)
    wrapped["step"] = step
    return wrapped


def evaluate_plan_portfolio(plan_space, omega, injection_point, replay, me_seat,
                            deps=None, *, strategy="trimmed_mean",
                            weights=None, trim_fraction=DEFAULT_TRIM_FRACTION,
                            identity_key=None,
                            plan_cap=MAX_PLAN_CANDIDATES):
    """计划枚举×对手模型集 Ω 的评估编排：逐计划×逐 ω seated rollout 打分
    → J(plan,ω) 矩阵 → 聚合委托 robust_selection → 逐计划聚合分。

    Args:
        plan_space: 计划空间，(plan_key, agent_factory) 对的序列——
            plan_key 可哈希（进 J 矩阵与聚合）；agent_factory 为 0 参工厂
            ``fn() -> agent``（agent=``fn(obs)->action``），**逐 rollout
            全新装载**防跨 ω/跨 rollout 串态（源语义=旧码 v13_factory 每
            rollout 新建 agent、"逐 rollout 全新装载防跨局串态"）；无状态
            执行器传 ``lambda: agent`` 即可；None=该计划恒不动作（等价
            非 ACTIVE 席）。旧树 PlanSpec 的配对适配（spec.key()/
            plan_to_knob_overrides/v13_factory）由调用方完成，本层不认
            PlanSpec 内部结构。
        omega: 对手模型集 Ω，成员为 ``"name"``（裸名：对手席=回放真实
            动作，公平性口径照旧）或 ``("name", opponent_factory)``（模型
            驱动对手席——opponent_factory 为 0 参工厂 ``fn() -> agent``，
            与计划侧 agent_factory 同语义逐 rollout 全新装载；经
            deps["step"] 包装就位，见 _deps_with_model_opponent）。旧树
            OpponentModel 的适配（.name/propose_actions）由调用方完成。
        injection_point: 注入步号（>=0；原样透传 seated 通道——0=d0
            全季，中间步先按官方动作流重演至该步再接管）。
        replay: 回放映射（seated 通道契约：含非空 steps）。
        me_seat: 我方席位 0|1（透传 seated 通道；分值取 final[me_seat]，
            与返回序 (seat0, seat1) 解耦——R2 修复口径）。
        deps: 依赖组（make_twin_deps 形状；None=通道默认 twin 组，引擎
            装载含 fail-closed 指纹校验）。
        strategy/weights/trim_fraction/identity_key: robust_selection
            聚合参数，默认沿下层（trimmed_mean / 0.25 / 关守成）；旧码
            恒传 plans.identity_spec().key() 的守成点由调用方传入。
        plan_cap: 枚举硬帽（默认 MAX_PLAN_CANDIDATES=120；None=不施帽）。

    Returns:
        dict：robust_selection 结果原样（best/ranking/strategy/tie_break/
        aggregates——ranking 按 (-聚合值, plan_key) 值序）+ 评估面
        j_matrix（{plan_key: {ω名: 我席终局分}}）、n_plans、n_omega、
        plan_cap、capped。

    错误: 无自设错误面——空计划空间的空 J 矩阵由 robust_selection 显式
        抛，回放缺失/me_seat 非法/注入点越界/引擎指纹不符由 seated 通道
        抛，异常原样传播（fail-closed）。
    """
    plans = list(plan_space)
    models = list(omega)
    kept = _apply_plan_cap(plans, plan_cap, identity_key)
    me = int(me_seat)
    j_matrix = {}
    for plan_key, agent_factory in kept:
        scores = {}
        for model in models:
            if isinstance(model, str):
                name, opponent_factory = model, None
            else:
                name, opponent_factory = model
            agent_callable = agent_factory() if agent_factory is not None \
                else None
            final = rollout_with_replay_opponent(
                replay, injection_point, agent_callable, me,
                deps=_deps_with_model_opponent(deps, opponent_factory, me))
            scores[name] = float(final[me])
        j_matrix[plan_key] = scores
    selection = robust_selection(
        j_matrix, strategy=strategy, weights=weights,
        trim_fraction=trim_fraction, identity_key=identity_key)
    result = dict(selection)
    result.update({
        "j_matrix": j_matrix,
        "n_plans": len(kept),
        "n_omega": len(models),
        "plan_cap": plan_cap,
        "capped": len(plans) > len(kept),
    })
    return result
