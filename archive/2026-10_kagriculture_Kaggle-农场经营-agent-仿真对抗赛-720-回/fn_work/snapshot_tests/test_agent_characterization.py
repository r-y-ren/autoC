# test_agent_characterization.py —— 现役提交链 bot 端到端固化（R1 基线核心）
# ===========================================================================
# 【口径修正 2026-09-21】整局 characterization 从 planner-on 装载改为
#   旗关面装载；planner-on 降级为冒烟测试。
# 根因：planner-on 面的黎明规划器时间治理器读真实墙钟
#   （planner/runtime.py dawn_budget/_now()：0.85s 帽 + 速率 EWMA 选阶梯，
#   deadline 逐时间片），机器负载抖动跨过决策边界即换计划——实测连跑
#   两次终局资金漂移 [81108, 70273] vs [78199, 63920]（本机另见活跃度
#   674/680 vs 原冻结 671/679）；建套件时的三遍稳定只是恰好低于边界。
#   值级冻结只对无墙钟输入的决定性面成立（战役纪律先例：黄金哈希只对
#   旗关面做逐位冻结，software/scripts/planner_flagoff_golden.py）。
# 关旗机制（正规机制，与旗关黄金的"无 DTSP_RUNTIME_CONFIG 名字"先例
#   同一决定性面）：main.py 命名空间的 DTSP_RUNTIME_CONFIG 是 src/entry.py
#   黎明钩子的唯一唤醒开关（`_dtsp_cfg = globals().get(
#   "DTSP_RUNTIME_CONFIG")`，假值即死路）；runtime.dawn_hook 首行
#   `if not _cfg(config, "enabled"): return None`。装载后把
#   agent.__globals__["DTSP_RUNTIME_CONFIG"]["enabled"] 置 False 即配置级
#   关旗（runtime._DEFAULTS 同键）；PLANNER_ENABLED 由 src/constants.py
#   默认 False 且无人再置真。钩子短路于任何状态写入之前 → 零足迹，
#   动作流与 v13.8 旗关黄金同一决定性面。
# 旗关面新冻结值三遍记录（2026-09-21，Linux/Python 3.14.7，三遍独立
#   进程，PYTHONHASHSEED=默认/1/2，全部逐字节一致；单局墙钟
#   6.6s / 6.6s / 6.6s）：
#     rewards [59730.0, 59835.0]；winner 1；non_pass [682, 680]；
#     日动作哈希见 FROZEN_DAY_ACTION_SHA256（d0/d6 双席镜像一致——
#     确定性 bot 对称开局的自然结果）。
# 原冻结值留档（planner-on 口径，机器状态依赖，已废，勿再比对）：
#     rewards [75708.0, 66284.0]；winner 0；non_pass [671, 679]；
#     d0s0 d79fd288ece1c4c49dcdaace62d4e5610756ce894c0230b12479eba8763a73c3
#     d0s1 c889dcdadeacc746d5e6433c04a035a06bf1c19833d6c9e28972227bbb12625d
#     d6s0 27d250e0e100377ec1d9b12201f19121551492e4b69ba6b67099bc1b712b75e8
#     d6s1 ebff0c67bfb091b8f5ce1207630ded86c32825331ebb951e98c5838e8ae62a48
#     d10s0 a8dd616fe3673387e81f2fbfd6d2b410cb3a61c3600ac1abfed2dfdfea074187
#     d10s1 56ecfe093b93b228ecf20345de5f0dafd49f08fd970ad3049c6d04c8a291dfa1
#     d24s0 c7ec21fd5ad617c88abc61134dfeef723310df5c99f0481694aaecee34c5591f
#     d24s1 4139fdc98d14d1b50f75635c761906a6ae753dc31136c18d661b0b71b471da93
# 装载口径：双席各自独立装载 main.py（共享进程内 planner.runtime 的
#   per-player 状态键，与既有测试套件一致）。种子 20260921（写死）。
#   actTimeout=60（run_episode 显式传参冻结语义）。
# 时长：旗关面单局 ~7s；planner-on 冒烟整局 ~35-40s（时间治理器在帽内
#   规划，本机实测未超时）。
# ===========================================================================

import hashlib

import pytest

from kgenv.arena import SUBMISSION_MAIN, load_submission_agent
from kgenv.engine import FULL_EPISODE_STEPS, run_episode

SEED = 20260921
SAMPLE_DAYS = (0, 6, 10, 24)

# ---- 旗关面冻结值（2026-09-21 三遍逐字节一致后写入，记录见文件头）----
FROZEN_REWARDS = [59730.0, 59835.0]
FROZEN_WINNER = 1
FROZEN_NON_PASS = [682, 680]
FROZEN_DAY_ACTION_SHA256 = {
    # (day, seat) -> sha256(str(actions_of_that_day).encode()).hexdigest()
    (0, 0): "d41fe65e6e16657831d515804fbfa0b23109017460ede96c9e352928d54e9732",
    (0, 1): "d41fe65e6e16657831d515804fbfa0b23109017460ede96c9e352928d54e9732",
    (6, 0): "933198d78b4ccca1988f5ff669c188766cf1965779961ddc70f21bcbdc6af720",
    (6, 1): "933198d78b4ccca1988f5ff669c188766cf1965779961ddc70f21bcbdc6af720",
    (10, 0): "c96ee6f966d697a73eace6b337d7a2d96c85ba8bf88e186104effbdcf103ca4b",
    (10, 1): "7f225c01809e19d24a1591bcd3247a8dda24f46b3ee5376f91a5e35b8890f85e",
    (24, 0): "7ff6f63ebe30a6da5d03e99e9575729f6a7e83c81b493f5079640f9e3a06c673",
    (24, 1): "34bacd1072de375a78a397bceaa9c8a596f72299004572b66598772dec4b2187",
}


def _load_flagoff_agent():
    """装载现役 main.py 后配置级关旗（机制见文件头）。"""
    agent = load_submission_agent(SUBMISSION_MAIN)
    agent.__globals__["DTSP_RUNTIME_CONFIG"]["enabled"] = False
    return agent


def _day_action_sha256(recorded, day):
    actions = [act for d, act in recorded if d == day]
    return hashlib.sha256(str(actions).encode()).hexdigest()


@pytest.fixture(scope="module")
def flagoff_episode():
    """旗关面自博弈一局（双席独立装载 main.py 后各自关旗），wrapper 逐回
    合记录 (day, action)。只跑一次，module 级共享给全部旗关断言（~7s）。
    """
    agent0 = _load_flagoff_agent()
    agent1 = _load_flagoff_agent()
    rec0, rec1 = [], []

    def wrapped0(obs):
        action = agent0(obs)
        rec0.append((int(getattr(obs, "day", 0)), action))
        return action

    def wrapped1(obs):
        action = agent1(obs)
        rec1.append((int(getattr(obs, "day", 0)), action))
        return action

    result = run_episode(wrapped0, wrapped1, SEED, act_timeout=60.0)
    return result, rec0, rec1, agent0, agent1


@pytest.fixture(scope="module")
def planner_on_episode():
    """planner-on 冒烟面自博弈一局（默认装载，DTSP 黎明钩子活跃），
    module 级共享（~35-40s）。不冻结任何值——见冒烟测试旁注。
    """
    agent0 = load_submission_agent(SUBMISSION_MAIN)
    agent1 = load_submission_agent(SUBMISSION_MAIN)
    result = run_episode(agent0, agent1, SEED, act_timeout=60.0)
    return result, agent0, agent1


def test_flagoff_episode_and_activity_frozen(flagoff_episode):
    result, _, _, agent0, agent1 = flagoff_episode
    # 对局完成契约
    assert result["statuses"] == ["DONE", "DONE"]
    assert result["turns_played"] == FULL_EPISODE_STEPS == 720
    assert result["seed"] == SEED
    assert result["winner"] == FROZEN_WINNER
    assert result["note"] == ""
    # 旗关面自检：整局打完旗必须仍关、无任何 planner 注入痕迹
    assert agent0.__globals__["PLANNER_ENABLED"] is False
    assert agent1.__globals__["PLANNER_ENABLED"] is False
    assert "_DTSP_PRISTINE_SNAPSHOT" not in agent0.__globals__
    assert "_DTSP_PRISTINE_SNAPSHOT" not in agent1.__globals__
    # 活性门摘要（冻结值）
    activity = result["activity"]
    assert activity["ok"] is True
    assert activity["completion_ok"] is True
    assert [seat["non_pass_decisions"] for seat in activity["seats"]] == \
        FROZEN_NON_PASS
    # 719 个决策（720 状态 − 初态），双席各一。
    assert activity["decisions"] == 719
    assert activity["states"] == 720


def test_flagoff_final_rewards_frozen(flagoff_episode):
    result, _, _, _, _ = flagoff_episode
    assert result["rewards"] == FROZEN_REWARDS


def test_flagoff_daily_action_hashes_frozen(flagoff_episode):
    _, rec0, rec1, _, _ = flagoff_episode
    for day in SAMPLE_DAYS:
        assert _day_action_sha256(rec0, day) == \
            FROZEN_DAY_ACTION_SHA256[(day, 0)], f"seat0 day{day} drifted"
        assert _day_action_sha256(rec1, day) == \
            FROZEN_DAY_ACTION_SHA256[(day, 1)], f"seat1 day{day} drifted"


def test_flagoff_decision_stream_shape(flagoff_episode):
    _, rec0, rec1, _, _ = flagoff_episode
    assert len(rec0) == len(rec1) == 719
    # 719 = 24×29 + 23：d0..d28 每天 24 个决策，d29 少最后一个
    # （720 状态 − 初态 = 719 决策，引擎不给我方最后一步发言权）。
    days0 = sorted({d for d, _ in rec0})
    assert days0 == list(range(30))
    for day in days0:
        expected = 24 if day < 29 else 23
        assert sum(1 for d, _ in rec0 if d == day) == expected


def test_planner_on_smoke_full_episode(planner_on_episode):
    # planner-on 冒烟面：默认装载（DTSP_RUNTIME_CONFIG.enabled=True）整局，
    # 只断言完成契约——DONE、零异常、720 步。不冻结任何值：
    # 时间治理器墙钟敏感，值级冻结不适用（根因与口径修正见文件头）。
    result, agent0, agent1 = planner_on_episode
    assert result["statuses"] == ["DONE", "DONE"]
    assert result["turns_played"] == FULL_EPISODE_STEPS == 720
    assert result["note"] == ""                       # 无终局异常注记
    # 零异常：黎明钩子异常记账为空（有异常时钩子落 _DTSP_HOOK_ERRORS）
    assert agent0.__globals__.get("_DTSP_HOOK_ERRORS", []) == []
    assert agent1.__globals__.get("_DTSP_HOOK_ERRORS", []) == []
    # 装载面自检（非值冻结）：planner 本局确实接合（否则冒烟面退化为
    # 又一局旗关，断言面空心化）。
    runtime = agent0.__globals__.get("DTSP_RUNTIME_MODULE")
    assert runtime is not None and runtime.trace()["engaged"] is True
