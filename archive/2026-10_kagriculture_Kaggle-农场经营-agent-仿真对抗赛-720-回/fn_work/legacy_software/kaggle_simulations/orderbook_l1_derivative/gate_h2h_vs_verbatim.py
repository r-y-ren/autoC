"""gate_h2h_vs_verbatim（R10 门①）：seated 双席位 ≥16 局对 orderbook verbatim 互胜 ≥0.55。

装载语义（2026-09-24 评审 P0 修复，重要）：官方 last-callable 桌面复刻——直接
import 复用门② gate_lineage_strength._load_entry（同款实现，不制第四份复制），
装载后加身份断言（门④ L1_LAST_CALLABLE/BASELINE_LAST_CALLABLE 同款先例）：
L1 侧 callable.__name__ 必须 = _cxs_agent、verbatim 侧必须 = _cxd_agent，断言
失败抛 GateH2HError"装载身份不符"（fail-closed）。此前误用
kgenv.arena.load_submission_agent：其具名 `agent` 优先分支对两 main 均取到
层链中途的内层 agent（L1 漏掉层 S），两席实为同一基座互打 → 16 局全 tie 的
证据无效（原"截断在该种子域不触发"定性系装载缺陷误定性，评审 P0 纠正）。

裁决口径（汇总字段沿用 round-30 先例 ../orderbook_derivative/h2h_evidence.json）：
- 局序 = seeds 顺序 × 席位 (0, 1)：每 seed 我方（L1 候选）坐 seat0/seat1 各一
  局；seeds 缺省 (101,102,103,104,201,202,203,204) → 16 局。
- per_game 条目照先例格式 {seed, cand_seat, rewards[2], statuses[2], winner,
  margin, elapsed_s}；margin = 我方 reward − 对方 reward（cand 视角，席位翻转
  不改符号）；winner 取 "cand"/"opp"/"tie"。
- 互胜率 rate = cand_wins / (cand_wins + opp_wins)，tie 不计分母：round-30
  先例汇总字段为 n_games/cand_wins/opp_wins/ties 且 ties=0，与本口径在先例
  数据上等值（cand_wins/n_games == cand_wins/(cand_wins+opp_wins)）；按验收
  锚例 9W6L1T→0.6（=9/15）定形。无决胜局（全 tie）时 rate=0.0，fail-closed。
- fail-closed：任一局 statuses ≠ ["DONE","DONE"]（Error/Timeout）→
  all_done=False → passed=False，无论互胜率；单局 Python 级异常同样按非
  DONE 局入账（statuses 记 ["ERROR","ERROR"]、note 留痕），不让门抛异常逃逸。
- PASS 判据：n>0 且 all_done 且 rate ≥ 0.55（WIN_RATE_THRESHOLD）。
- 台账：本文件同目录 evidence/h2h_evidence.json（mkdir -p，evidence_path 可
  覆写——门③ run 同款口径，供测试 tmp 隔离防覆写真台账）；汇总字段沿
  round-30（n_games/cand_wins/opp_wins/ties/cand_wins_seatA(ofN)/
  cand_wins_seatB(ofN)/mean_margin/all_done/games），seatA/seatB 的 ofN 按
  实际每席位局数写（缺省 8），另加 rate/win_rate_threshold/passed 三键作门
  裁决留痕，并记 loader 双席装载身份（l1_callable/verbatim_callable）。
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any, Dict, FrozenSet, List, Optional, Sequence

from gate_lineage_strength import GateLineageError, _load_entry
from gate_launch_fourgate_l1 import BASELINE_LAST_CALLABLE, L1_LAST_CALLABLE

DEFAULT_SEEDS = (101, 102, 103, 104, 201, 202, 203, 204)
WIN_RATE_THRESHOLD = 0.55
EVIDENCE_NAME = "h2h_evidence.json"
L1_EXPECTED_CALLABLES = frozenset({L1_LAST_CALLABLE})        # {"_cxs_agent"}
VERBATIM_EXPECTED_CALLABLES = frozenset({BASELINE_LAST_CALLABLE})  # {"_cxd_agent"}


class GateH2HError(RuntimeError):
    """门① fail-closed：装载失败/装载身份不符（不可执行=门红，由编排承载）。"""


def _load_verified(main_path: Any, expected_names: FrozenSet[str], role: str):
    """官方 last-callable 装载（复用门② _load_entry）+ 身份断言（门④同款先例）。

    callable.__name__ 必须在 expected_names 白名单内；装载异常（转译
    GateLineageError）或身份不符抛 GateH2HError——没验证装的是谁就开打=门①
    证据无效（评审 P0 教训），绝不静默开跑。
    """
    try:
        fn = _load_entry(main_path, role)
    except GateLineageError as exc:
        raise GateH2HError(str(exc)) from exc
    name = getattr(fn, "__name__", None)
    if name not in expected_names:
        raise GateH2HError(
            f"{role} 装载身份不符：last-callable={name!r} 不在期望集 "
            f"{sorted(expected_names)}（{main_path}）")
    return fn


def _software_root() -> str:
    """kgenv 所在的 legacy_software 根（由本文件位置推导，不手拼路径）。"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _summarize(per_game: List[Dict[str, Any]]) -> Dict[str, Any]:
    """纯函数：从 per_game 台账算互胜率与门裁决（单测直接喂合成局）。

    互胜口径见模块 docstring：tie 不计分母；非 DONE 局不计 W/L/T、只拉红
    all_done；margin 仅对有限数值局计入 mean_margin。
    """
    n = len(per_game)
    wins = losses = ties = 0
    seat_games = {0: 0, 1: 0}
    seat_wins = {0: 0, 1: 0}
    all_done = True
    margins: List[float] = []
    for game in per_game:
        seat = int(game["cand_seat"])
        seat_games[seat] += 1
        if list(game["statuses"]) != ["DONE", "DONE"]:
            all_done = False
            continue
        winner = game["winner"]
        if winner == "cand":
            wins += 1
            seat_wins[seat] += 1
        elif winner == "opp":
            losses += 1
        else:
            ties += 1
        margin = game.get("margin")
        if (isinstance(margin, (int, float)) and not isinstance(margin, bool)
                and math.isfinite(float(margin))):
            margins.append(float(margin))
    decided = wins + losses
    rate = round(wins / decided, 4) if decided else 0.0
    passed = bool(n) and all_done and rate >= WIN_RATE_THRESHOLD
    return {
        "n": n, "wins": wins, "losses": losses, "ties": ties,
        "rate": rate, "passed": passed, "all_done": all_done,
        "seat_games": seat_games, "seat_wins": seat_wins,
        "mean_margin": round(sum(margins) / len(margins), 1) if margins else None,
    }


def _play_one(run_episode: Any, episode_steps: int, cand_agent: Any,
              opp_agent: Any, seed: int, cand_seat: int) -> Dict[str, Any]:
    """跑一局并落成先例格式的 per_game 条目（异常=非 DONE 局，fail-closed）。"""
    agents = [cand_agent, opp_agent] if cand_seat == 0 else [opp_agent, cand_agent]
    try:
        res = run_episode(agents[0], agents[1], seed,
                          episode_steps=episode_steps, collect_daily=False)
        rewards = [float(r) for r in res["rewards"]]
        statuses = [str(s) for s in res["statuses"]]
    except Exception as exc:  # 单局崩=门红入账，不向上抛（fail-closed 留痕）
        return {"seed": seed, "cand_seat": cand_seat, "rewards": None,
                "statuses": ["ERROR", "ERROR"], "winner": None, "margin": None,
                "elapsed_s": None,
                "note": f"episode raised {type(exc).__name__}: {exc}"}
    game: Dict[str, Any] = {
        "seed": seed, "cand_seat": cand_seat, "rewards": rewards,
        "statuses": statuses, "winner": None,
        "margin": rewards[cand_seat] - rewards[1 - cand_seat],
        "elapsed_s": res.get("elapsed_seconds"),
    }
    if statuses != ["DONE", "DONE"]:
        game["note"] = res.get("note") or f"non-terminal statuses: {statuses}"
    else:
        winner = res.get("winner")
        game["winner"] = ("cand" if winner == cand_seat
                          else "opp" if winner == 1 - cand_seat else "tie")
    return game


def run(l1_main: str, verbatim_main: str,
        seeds: Optional[Sequence[int]] = None,
        evidence_path: Optional[str] = None,
        l1_expected_names: FrozenSet[str] = L1_EXPECTED_CALLABLES,
        verbatim_expected_names: FrozenSet[str] = VERBATIM_EXPECTED_CALLABLES,
        ) -> Dict[str, Any]:
    """{n, wins, losses, ties, rate, passed, per_game, evidence_path}。

    任一局非 DONE 即门红（fail-closed）；对局走官方引擎 kgenv.engine.run_episode
    （episode_steps=720）。装载走官方 last-callable 桌面复刻（复用门②
    _load_entry）+ 身份断言：l1_main 末 callable 必须 = _cxs_agent（层 S 运行时
    入口）、verbatim_main 必须 = _cxd_agent——不符即抛 GateH2HError"装载身份
    不符"（fail-closed，不开打；评审 P0 修复，此前 kgenv.arena
    load_submission_agent 的具名 agent 优先分支对两 main 均装到内层基座，
    16 局实为基座互打全 tie，证据无效）。evidence_path 缺省本目录
    evidence/h2h_evidence.json，可覆写（测试 tmp 隔离）。
    """
    if seeds is None:
        seeds = DEFAULT_SEEDS
    root = _software_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    from kgenv.engine import FULL_EPISODE_STEPS, run_episode

    cand_agent = _load_verified(l1_main, l1_expected_names, "l1_main")
    opp_agent = _load_verified(verbatim_main, verbatim_expected_names,
                               "verbatim_main")

    per_game: List[Dict[str, Any]] = []
    for seed in seeds:
        for cand_seat in (0, 1):
            per_game.append(_play_one(run_episode, FULL_EPISODE_STEPS,
                                      cand_agent, opp_agent, int(seed),
                                      cand_seat))

    summary = _summarize(per_game)
    seat_a_key = "cand_wins_seatA(of%d)" % summary["seat_games"][0]
    seat_b_key = "cand_wins_seatB(of%d)" % summary["seat_games"][1]
    evidence = {
        "n_games": summary["n"],
        "cand_wins": summary["wins"],
        "opp_wins": summary["losses"],
        "ties": summary["ties"],
        seat_a_key: summary["seat_wins"][0],
        seat_b_key: summary["seat_wins"][1],
        "mean_margin": summary["mean_margin"],
        "all_done": summary["all_done"],
        "rate": summary["rate"],
        "win_rate_threshold": WIN_RATE_THRESHOLD,
        "passed": summary["passed"],
        "loader": {
            "semantics": "official-last-callable",
            "l1_callable": getattr(cand_agent, "__name__", None),
            "verbatim_callable": getattr(opp_agent, "__name__", None),
        },
        "games": per_game,
    }
    target = os.path.abspath(evidence_path) if evidence_path else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "evidence", EVIDENCE_NAME)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    return {
        "n": summary["n"], "wins": summary["wins"],
        "losses": summary["losses"], "ties": summary["ties"],
        "rate": summary["rate"], "passed": summary["passed"],
        "per_game": per_game, "evidence_path": target,
    }
