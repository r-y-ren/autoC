"""gate_lineage_strength（R10 门②）：对 v48 纯件/v4b/hybrid-v2 各 ≥8 局无翻负。

契约（责任文档）：
- 签名 run(l1_main, opponents: dict, per_opponent_n: int = 8) -> dict；对手键名沿
  "v48-pure"/"v4b"/"hybrid-v2"（run 本身不硬编码名单，由 opponents dict 定阵容）；
- 对每对手跑 per_opponent_n 局：seeds 101-104 双席位=8 局（缺省，块 0=dev 种子，
  与 h2h 台账 dev 口径一致）；n 参数可调——n>8 依 (101+100k..104+100k)×(seat0,seat1)
  阶梯扩位（n=16 即 dev+regression 201-204 双席位，h2h 台账 16 局同构）；
- 裁决：任一负局（losses>0）→门红；平局允许不计负；非 DONE 局/对局异常=不可裁
  →不进 w/l/t 也不记平，经 all_done=False 强制门红（异常局绝不静默当平）；
- evidence 落本目录 evidence/lineage_evidence.json，格式 {对手: {n, wins, losses,
  ties, all_done, per_game}}；per_game 沿 h2h 台账（orderbook_derivative/
  h2h_evidence.json）同款字段：seed/cand_seat/rewards/statuses/winner/margin/
  elapsed_s——rewards 按席位序（seat0 在前），margin=cand-opp（正=L1 赢）；
- 返回 {per_opponent: <同 evidence 内容>, passed: bool, evidence_path: str}；
- fail-closed：装载失败/入参不可裁（opponents 空、n 非正、路径不存在、文件无
  callable）→ 抛 GateLineageError；对局异常记 per_game error 且门红，不中断其余局。

装载语义（与 round-30 台账对齐，重要）：官方 last-callable 入口——
kaggle_environments.agent.get_last_callable 的桌面版复刻（exec 后取 globals 最后
callable，双下划线名排除），同 test_build.test_last_callable_is_cxs_agent 先例。
对 L1 main.py 取到 _cxs_agent（层 S 运行时入口）。注意不得改用
kgenv.arena.load_submission_agent：它优先具名 agent()，对 L1 会取到 v55 核心
（无层 D/S——round-30 build_manifest gate_note 记录该装载面 203/719 步分歧）；
对三对手虽行为等价（其 _kaggle_submission_entrypoint/_v48hybrid_entrypoint 仅转调
具名 agent），为与基线台账同口径仍统一走 last-callable。
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Callable, Dict, List, Tuple, Union

_HERE = os.path.dirname(os.path.abspath(__file__))
_SOFTWARE_ROOT = os.path.dirname(os.path.dirname(_HERE))  # legacy_software（kgenv 所在）
if _SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, _SOFTWARE_ROOT)

from kgenv.engine import run_episode  # noqa: E402  (对局同 kgenv: engine.run_episode)

EVIDENCE_DIR = os.path.join(_HERE, "evidence")
EVIDENCE_PATH = os.path.join(EVIDENCE_DIR, "lineage_evidence.json")

AgentRef = Union[str, os.PathLike, Callable[[dict], dict]]

# seed 阶梯：块 k 的种子 = (101+100k, 102+100k, 103+100k, 104+100k)，每种子双席位。
# 块 0=dev 种子（缺省 8 局口径）；块 1=201-204（regression，n=16 时启用）。
_SEEDS_PER_BLOCK = (101, 102, 103, 104)
_BLOCK_STRIDE = 100
_WINNERS = ("cand", "opp", "tie")


class GateLineageError(RuntimeError):
    """门② fail-closed：入参不可裁或装载失败（整体不可执行=门红语义由编排承载）。"""


def _seed_seat_pairs(n: int) -> List[Tuple[int, int]]:
    """前 n 个 (seed, cand_seat) 对：seed 主序、席位次序（101/0,101/1,102/0,…）。"""
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise GateLineageError(f"per_opponent_n 必须为正整数，got {n!r}")
    pairs: List[Tuple[int, int]] = []
    block = 0
    while len(pairs) < n:
        for seed in _SEEDS_PER_BLOCK:
            for seat in (0, 1):
                pairs.append((seed + block * _BLOCK_STRIDE, seat))
                if len(pairs) == n:
                    return pairs
        block += 1
    return pairs  # pragma: no cover（循环内必 return）


def _load_entry(agent: AgentRef, role: str) -> Callable[[dict], dict]:
    """官方 last-callable 装载（get_last_callable 桌面版；语义注见模块 docstring）。

    已装载 callable 直接透传；路径则 exec 后取最后非双下划线 callable。exec 环境
    预置 __name__（非 "__main__"，防文件内主守卫构建器落盘）与 __file__。
    任何装载异常=GateLineageError（fail-closed，不静默降级）。
    """
    if callable(agent):
        return agent
    if isinstance(agent, (str, os.PathLike)) and not isinstance(agent, bool):
        path = os.path.abspath(os.fspath(agent))
        if not os.path.isfile(path):
            raise GateLineageError(f"{role} 装载失败：文件不存在 {path}")
        try:
            with open(path, "rb") as fh:
                src = fh.read()
            ns: Dict[str, Any] = {"__name__": "gate_lineage_agent", "__file__": path}
            exec(compile(src, path, "exec"), ns)  # noqa: S102 - 官方 last-callable 装载桌面版
        except Exception as exc:
            raise GateLineageError(
                f"{role} 装载失败（fail-closed）: {path}: {type(exc).__name__}: {exc}"
            ) from exc
        entries = [(k, v) for k, v in ns.items()
                   if callable(v) and not (k.startswith("__") and k.endswith("__"))]
        if not entries:
            raise GateLineageError(f"{role} 装载失败：{path} 无 callable 入口")
        return entries[-1][1]
    raise GateLineageError(
        f"{role} 需为 main.py 路径或已装载 callable，got {type(agent).__name__}")


def _adjudicate(per_game: List[Dict[str, Any]]) -> Dict[str, Any]:
    """纯裁决（合成可测，不碰引擎）：{n, wins, losses, ties, all_done}。

    只有 statuses==["DONE","DONE"] 且 rewards 为二元数值列表的局才进 w/l/t；
    winner 取 "cand"/"opp"/"tie"（rewards 已按席位序，winner 由 margin 符号定）。
    非 DONE/带 error/winner 缺失的局不进 w/l/t（n 照计）且置 all_done=False——
    门级 passed 要求 losses==0 且 all_done，异常局强制翻红、绝不记平。
    """
    wins = losses = ties = 0
    all_done = True
    for game in per_game:
        rewards = game.get("rewards")
        normal = (game.get("statuses") == ["DONE", "DONE"]
                  and isinstance(rewards, list) and len(rewards) == 2
                  and all(isinstance(r, (int, float)) and not isinstance(r, bool)
                          for r in rewards))
        winner = game.get("winner")
        if not normal or winner not in _WINNERS:
            all_done = False
            continue
        if winner == "cand":
            wins += 1
        elif winner == "opp":
            losses += 1
        else:
            ties += 1
    return {"n": len(per_game), "wins": wins, "losses": losses, "ties": ties,
            "all_done": all_done}


def _play_one(cand_fn: Callable[[dict], dict], opp_fn: Callable[[dict], dict],
              seed: int, cand_seat: int) -> Dict[str, Any]:
    """单局：L1 居 cand_seat 席，对局同 kgenv.engine.run_episode（缺省 720 步）。

    返回 h2h 台账同款 per_game 条目（键集固定七元；异常局 rewards/statuses 为
    None 并附 error 字段，经 all_done=False 承载门红，不向上传播）。
    """
    try:
        if cand_seat == 0:
            res = run_episode(cand_fn, opp_fn, seed, collect_daily=False)
        else:
            res = run_episode(opp_fn, cand_fn, seed, collect_daily=False)
    except Exception as exc:  # 对局异常=不可裁局（fail-closed 由 all_done=False 承载）
        return {"seed": int(seed), "cand_seat": int(cand_seat),
                "rewards": None, "statuses": None, "winner": None,
                "margin": None, "elapsed_s": None,
                "error": f"{type(exc).__name__}: {exc}"}
    rewards_raw = res.get("rewards")
    statuses = [str(s) for s in (res.get("statuses") or [])]
    rewards = ([float(r) if isinstance(r, (int, float)) and not isinstance(r, bool)
                else None for r in rewards_raw]
               if isinstance(rewards_raw, list) and len(rewards_raw) == 2 else None)
    done = (rewards is not None and None not in rewards
            and statuses == ["DONE", "DONE"])
    if done:
        margin = rewards[cand_seat] - rewards[1 - cand_seat]
        winner = "cand" if margin > 0 else "opp" if margin < 0 else "tie"
    else:
        margin, winner = None, None
    return {"seed": int(seed), "cand_seat": int(cand_seat), "rewards": rewards,
            "statuses": statuses, "winner": winner,
            "margin": round(margin, 1) if margin is not None else None,
            "elapsed_s": res.get("elapsed_seconds")}


def run(l1_main, opponents: dict, per_opponent_n: int = 8) -> dict:
    """门②主体：每对手 per_opponent_n 局，任一负局即门红（允许平）。

    l1_main/opponents 值均可为 main.py 路径或已装载 callable（装载走官方
    last-callable 语义，见模块 docstring）。返回 {per_opponent, passed,
    evidence_path}；evidence 无论红绿均落盘（红局台账即败因记录）。
    """
    if not isinstance(opponents, dict) or not opponents:
        raise GateLineageError(
            f"opponents 必须为非空 dict（对手名→main.py 路径/callable），got {opponents!r}")
    pairs = _seed_seat_pairs(per_opponent_n)
    cand_fn = _load_entry(l1_main, "l1_main")
    opp_fns = {str(name): _load_entry(ref, f"opponents[{name!r}]")
               for name, ref in opponents.items()}

    per_opponent: Dict[str, Dict[str, Any]] = {}
    for name, opp_fn in opp_fns.items():
        per_game = [_play_one(cand_fn, opp_fn, seed, seat) for seed, seat in pairs]
        per_opponent[name] = dict(_adjudicate(per_game), per_game=per_game)
        for game in per_game:  # 编排可观测的逐局一行台账（stdout，证据以 JSON 为准）
            tag = game.get("error") or (
                f'margin={game["margin"]:+.1f} '
                f'{"WIN" if game["winner"] == "cand" else "TIE" if game["winner"] else "?"}')
            print(f"[gate-lineage] {name} seed={game['seed']} "
                  f"seat={game['cand_seat']} {tag}", flush=True)

    passed = all(summary["losses"] == 0 and summary["all_done"]
                 for summary in per_opponent.values())
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    with open(EVIDENCE_PATH, "w", encoding="utf-8") as fh:
        json.dump(per_opponent, fh, ensure_ascii=False, indent=1)
    return {"per_opponent": per_opponent, "passed": passed,
            "evidence_path": EVIDENCE_PATH}
