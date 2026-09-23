"""gate_h2h_vs_verbatim（R10 门①）：seated 双席位 ≥16 局对 orderbook verbatim 互胜 ≥0.55。

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
- 台账：本文件同目录 evidence/h2h_evidence.json（mkdir -p）；汇总字段沿
  round-30（n_games/cand_wins/opp_wins/ties/cand_wins_seatA(ofN)/
  cand_wins_seatB(ofN)/mean_margin/all_done/games），seatA/seatB 的 ofN 按
  实际每席位局数写（缺省 8），另加 rate/win_rate_threshold/passed 三键作门
  裁决留痕。
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Sequence

DEFAULT_SEEDS = (101, 102, 103, 104, 201, 202, 203, 204)
WIN_RATE_THRESHOLD = 0.55
EVIDENCE_NAME = "h2h_evidence.json"


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
        seeds: Optional[Sequence[int]] = None) -> Dict[str, Any]:
    """{n, wins, losses, ties, rate, passed, per_game, evidence_path}。

    任一局非 DONE 即门红（fail-closed）；对局走官方引擎 kgenv.engine.run_episode
    （episode_steps=720），装载走 kgenv.arena.load_submission_agent（last-callable）。
    """
    if seeds is None:
        seeds = DEFAULT_SEEDS
    root = _software_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    from kgenv.arena import load_submission_agent
    from kgenv.engine import FULL_EPISODE_STEPS, run_episode

    cand_agent = load_submission_agent(l1_main)
    opp_agent = load_submission_agent(verbatim_main)

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
        "games": per_game,
    }
    evidence_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    evidence_path = os.path.join(evidence_dir, EVIDENCE_NAME)
    with open(evidence_path, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    return {
        "n": summary["n"], "wins": summary["wins"],
        "losses": summary["losses"], "ties": summary["ties"],
        "rate": summary["rate"], "passed": summary["passed"],
        "per_game": per_game, "evidence_path": evidence_path,
    }
