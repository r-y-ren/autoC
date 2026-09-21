"""从回放任意步以显式 me_seat 重建双席状态并推演（修复原恒 seat0 注入），幂等/指纹校验语义保留。

上游: R2（详见 fn_docs/responsibility.md）

实现要点（[改造]件，源语义综合）：
- 骨架 = software/scripts/v143_sellrace_gates.py:91-116 的 seated rollout：
  ``pair[me] = mine`` 显式按席位注入（我方 callable 动作进 me_seat 席、
  回放对手动作进对席），循环守卫/终止条件与 v143 逐句同构。
- 补足 bench 版（software/scripts/planner_offline_bench.py:306-321 原
  rollout_with_replay_opponent 及其调用生态）具备、而 v143 版留在调用方的
  回放装载/指纹校验/注入点语义：本函数自行完成"回放 -> 注入态"重建
  （twin.build_state_from_replay(replay, injection_point)）与官方动作流
  抽取（twin.replay_transition_actions），引擎装载走 twin.load_engine 的
  fail-closed 指纹链（wheel/场景两文件 sha256 逐一核对，不符即抛
  TwinFingerprintError，绝不静默降级）。
- 修复本体：旧 bench 版 ``deps["step"](state, [mine, theirs])`` 恒把"我方
  动作"注入 seat0——me_seat=1 的局我方 agent 的动作落进对手农场，终局
  数字为双席互换伪影（R2 快照反例：合成回放真值 [3000.0,1570.0] 旧通道
  输出 [1570.0,3000.0]）。本通道 me_seat∈{0,1} 均按实际席位注入。
- 幂等语义：每次调用自回放全新重建注入态（不共享可变状态、不改回放、
  不留跨调用残留）——同输入必同输出；调用方无需（旧版那样）在两次
  rollout 之间自行重建 state。
- 旧树只读消费：经 ``__file__`` 上溯发现战役根（blueprint.md+software+
  fn_docs 三特征齐备）后将 ``<战役根>/software`` 插入 sys.path，import
  旧树 ``kaggle_simulations.agent.planner.twin``（只读，不改它；与允许
  import 旧树 kgenv 同批示）。不 import 旧树 scripts/；不 import fn_work
  其他模块。
- 刻意不吸收项：v143 版的 pre_step 逐回合前置回调（gates b/c 门 DTSP
  runtime 黎明钩子专用）不进本通用通道——契约签名无此参，需要时由
  调用方经 deps["step"] 包装等价实现。
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from pathlib import Path

__all__ = ["rollout_with_replay_opponent", "make_twin_deps",
           "TwinFingerprintError"]

# 战役根目录特征（三件齐备才算；与仓库布局约定一致，不写字面战役路径）
_CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")

_twin = None


def __getattr__(name):
    """PEP 562 惰性再导出：TwinFingerprintError（旧树 twin 的指纹校验
    异常，调用方 except/断言用；首次访问才触发旧树装载）。"""
    if name == "TwinFingerprintError":
        return _load_twin().TwinFingerprintError
    raise AttributeError(name)


def _campaign_software_root() -> Path:
    """自本模块 __file__ 上溯发现战役根，返回其 software/ 子目录。

    fail-closed：上溯链上找不到特征齐备的战役根即抛 RuntimeError
    （不猜路径、不做 CWD 假设）。
    """
    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / name).exists() for name in _CAMPAIGN_FEATURES):
            return candidate / "software"
    raise RuntimeError(
        "未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES) + "），"
        f"上溯起点: {here}")


def _load_twin():
    """装载旧树 twin 模块（进程内缓存；只读消费）。"""
    global _twin
    if _twin is not None:
        return _twin
    software = str(_campaign_software_root())
    if software not in sys.path:
        sys.path.insert(0, software)
    from kaggle_simulations.agent.planner import twin  # noqa: E402 旧树只读
    _twin = twin
    return _twin


def make_twin_deps(wheel_path=None, force_reload=False):
    """默认依赖组（键契约沿两源共有约定，仅取 rollout 所需四键）：
    build(replay, step) -> state / transition_actions(replay) -> [a0,a1] 流 /
    step(state, [a0, a1]) -> state / final(state) -> [float, float]。
    build 内走 twin.load_engine(wheel_path, force_reload) 的 fail-closed
    指纹链——wheel/场景文件 sha256 与登记值不符即抛 TwinFingerprintError。
    """
    twin = _load_twin()

    def build(replay, step_index):
        bundle = twin.load_engine(wheel_path=wheel_path,
                                  force_reload=force_reload)
        return twin.build_state_from_replay(replay, step_index,
                                            bundle=bundle)

    return {
        "build": build,
        "transition_actions": twin.replay_transition_actions,
        "step": twin.step,
        "final": twin.final_money,
    }


def rollout_with_replay_opponent(replay, injection_point, agent_callable,
                                 me_seat, deps=None) -> list:
    """从回放 injection_point 步以显式 me_seat 重建双席态并推演至终局。

    Args:
        replay: 回放 dict（框架形态：configuration/info.seed/steps/rewards，
            twin.build_state_from_replay 可重建；缺失/无 steps 即抛）。
        injection_point: 注入步号（>=0；0=d0 全季）——先按官方动作流重演至
            该步得注入态，我方 callable 自该步起接管 me_seat 席。
        agent_callable: 我方决策函数 ``fn(obs) -> action``（None=恒不动作，
            等价框架对非 ACTIVE 席传 None）。动作注入 **me_seat 席**。
        me_seat: 我方席位（0 或 1；决定注入席与对手动作流取对席下标，
            不影响返回序）。回放对手动作注入 **对席**。
        deps: 可选依赖组（make_twin_deps 形状；None=默认 twin 依赖组，
            引擎装载含 fail-closed 指纹校验）。

    Returns:
        双席终局资金 ``[seat0_money, seat1_money]``——序=(seat0, seat1)，
        与我方席位解耦。

    Raises:
        ValueError: 回放缺失（None/非映射/无 steps）或 me_seat 不在 {0,1}。
        TwinFingerprintError: 引擎指纹校验失败（twin.load_engine 传播，
            fail-closed）。injection_point 超出可重演范围时 ValueError 由
            twin.build_state_from_replay 传播。
    """
    # ---- 输入校验（fail-closed，先于引擎装载）----
    if not isinstance(replay, Mapping) or not (replay.get("steps") or []):
        seen = "None" if replay is None else repr(replay)[:60]
        raise ValueError(
            f"回放缺失: 需要含非空 steps 的回放映射, got "
            f"{type(replay).__name__}: {seen}")
    me = int(me_seat)
    if me not in (0, 1):
        raise ValueError(f"me_seat 必须为 0 或 1, got {me_seat!r}")
    start = int(injection_point)
    if start < 0:
        raise ValueError(f"injection_point 必须 >= 0, got {start}")

    if deps is None:
        deps = make_twin_deps()

    # ---- 注入点语义：回放 -> 第 start 步双席注入态 + 官方动作流 ----
    # （指纹链在 build 内 fail-closed：wheel/场景文件不符即 TwinFingerprintError）
    state = deps["build"](replay, start)
    opp_actions = deps["transition_actions"](replay)

    # ---- seated rollout（骨架=v143:91-116）：mine→seats[me]、theirs→对席 ----
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    while not state.env.done and start + taken < len(opp_actions) \
            and taken < max_steps:
        obs = state.seats[me].observation
        mine = agent_callable(obs) if agent_callable is not None else None
        theirs = opp_actions[start + taken][1 - me]
        pair = [theirs, theirs]
        pair[me] = mine
        deps["step"](state, pair)
        taken += 1

    # ---- 双席终局资金：序=(seat0, seat1)，与我方席位解耦 ----
    return deps["final"](state)
