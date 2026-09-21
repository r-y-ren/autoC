# test_agent_characterization.py —— 现役提交链 bot 端到端固化（R1 基线核心）
# ===========================================================================
# 钉什么：software/kaggle_simulations/agent/main.py 装载的现役提交 agent
#   （DTSP 开启态、_SELLRACE_SHIP=False）经 kgenv.engine 通道打完整一局
#   自博弈（双席各自独立装载 main.py，共享进程内 planner.runtime 的
#   per-player 状态键，与既有测试套件的装载口径一致）的：
#     * 对局完成契约：statuses DONE/DONE、720 步、胜者；
#     * 双方终局资金（冻结值）；
#     * d0/d6/d10/d24 四天的双席动作序列 sha256（冻结值，
#       sha256(str(actions).encode())，与任务规约同式）；
#     * 活性门摘要（activity ok / 双席 non-PASS 决策数）。
# 种子：20260921（写死）。actTimeout=60（run_episode 显式传参冻结语义）。
# 时长：本机（Linux/Python 3.14.7）单局约 35-40s，未超 120s 阈值，
#   无需短局/降频采样。
# 确定性验证：2026-09-21 以 PYTHONHASHSEED=1/2 双进程复跑，全部冻结值
#   逐字节一致（bot 无集合迭代序依赖的纪律在端到端层面成立）。
# 已知边界：DTSP 黎明规划有 0.85s 预算帽（墙钟治理）。本机实测各黎明
#   规划远低于帽，梯子不因机器速度截断；极慢机器理论上可能触发预算
#   截断使冻结值漂移——复跑三遍验证见 README（本机三遍全绿）。
# ===========================================================================

import hashlib

import pytest

from kgenv.arena import SUBMISSION_MAIN, load_submission_agent
from kgenv.engine import FULL_EPISODE_STEPS, run_episode

SEED = 20260921
SAMPLE_DAYS = (0, 6, 10, 24)

# ---- 冻结值（2026-09-21，Linux/Python 3.14.7 本机实测固化）----
FROZEN_REWARDS = [75708.0, 66284.0]
FROZEN_WINNER = 0
FROZEN_NON_PASS = [671, 679]
FROZEN_DAY_ACTION_SHA256 = {
    # (day, seat) -> sha256(str(actions_of_that_day).encode()).hexdigest()
    (0, 0): "d79fd288ece1c4c49dcdaace62d4e5610756ce894c0230b12479eba8763a73c3",
    (0, 1): "c889dcdadeacc746d5e6433c04a035a06bf1c19833d6c9e28972227bbb12625d",
    (6, 0): "27d250e0e100377ec1d9b12201f19121551492e4b69ba6b67099bc1b712b75e8",
    (6, 1): "ebff0c67bfb091b8f5ce1207630ded86c32825331ebb951e98c5838e8ae62a48",
    (10, 0): "a8dd616fe3673387e81f2fbfd6d2b410cb3a61c3600ac1abfed2dfdfea074187",
    (10, 1): "56ecfe093b93b228ecf20345de5f0dafd49f08fd970ad3049c6d04c8a291dfa1",
    (24, 0): "c7ec21fd5ad617c88abc61134dfeef723310df5c99f0481694aaecee34c5591f",
    (24, 1): "4139fdc98d14d1b50f75635c761906a6ae753dc31136c18d661b0b71b471da93",
}


def _day_action_sha256(recorded, day):
    actions = [act for d, act in recorded if d == day]
    return hashlib.sha256(str(actions).encode()).hexdigest()


@pytest.fixture(scope="module")
def episode():
    """自博弈一局（双席独立装载 main.py），wrapper 逐回合记录 (day, action)。

    只跑一次，module 级共享给本文件全部断言（单局 ~35s）。
    """
    agent0 = load_submission_agent(SUBMISSION_MAIN)
    agent1 = load_submission_agent(SUBMISSION_MAIN)
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
    return result, rec0, rec1


def test_episode_completion_contract(episode):
    result, rec0, rec1 = episode
    assert result["statuses"] == ["DONE", "DONE"]
    assert result["turns_played"] == FULL_EPISODE_STEPS == 720
    assert result["seed"] == SEED
    assert result["winner"] == FROZEN_WINNER
    assert result["note"] == ""


def test_final_rewards_frozen(episode):
    result, _, _ = episode
    assert result["rewards"] == FROZEN_REWARDS


def test_daily_action_hashes_frozen(episode):
    _, rec0, rec1 = episode
    for day in SAMPLE_DAYS:
        assert _day_action_sha256(rec0, day) == \
            FROZEN_DAY_ACTION_SHA256[(day, 0)], f"seat0 day{day} drifted"
        assert _day_action_sha256(rec1, day) == \
            FROZEN_DAY_ACTION_SHA256[(day, 1)], f"seat1 day{day} drifted"


def test_activity_summary_frozen(episode):
    result, _, _ = episode
    activity = result["activity"]
    assert activity["ok"] is True
    assert activity["completion_ok"] is True
    assert [seat["non_pass_decisions"] for seat in activity["seats"]] == \
        FROZEN_NON_PASS
    # 719 个决策（720 状态 − 初态），双席各一。
    assert activity["decisions"] == 719
    assert activity["states"] == 720


def test_decision_stream_shape(episode):
    _, rec0, rec1 = episode
    assert len(rec0) == len(rec1) == 719
    # 719 = 24×29 + 23：d0..d28 每天 24 个决策，d29 少最后一个
    # （720 状态 − 初态 = 719 决策，引擎不给我方最后一步发言权）。
    days0 = sorted({d for d, _ in rec0})
    assert days0 == list(range(30))
    for day in days0:
        expected = 24 if day < 29 else 23
        assert sum(1 for d, _ in rec0 if d == day) == expected
