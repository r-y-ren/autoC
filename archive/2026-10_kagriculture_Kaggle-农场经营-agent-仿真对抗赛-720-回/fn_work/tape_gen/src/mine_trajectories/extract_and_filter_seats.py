"""extract_and_filter_seats（L1，R1）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

逐席提取 719 步动作流（replay steps[t>=1] 的 action，即 game step 0..718；
单位动作 farmer+hands 与市场单 market 分列保留），并做两类过滤：

* 我方席：TeamNames 含本队名——本队名从语料实测（席位名频次最高者），
  不硬编码；
* 克隆席：开局 turns 1-51 与 v48 家族路由（routes.json 六路由）逐字节
  一致（sha256 over 规范化 JSON blob），先例 track-C
  （bc_track/scripts/extract_samples.py opening_signature，turns=51）。

元数据：对手名 / 我席结果 / 终局边际 / 克隆旗 / 类别（full|projection）。
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]

#: v48 家族六路由磁带库（6×719，2026-09-23 深读解码产物）。
DEFAULT_ROUTES_PATH = (_CAMPAIGN_ROOT / "fn_docs" / "hybrid" / "results"
                       / "2026-09-23-v48-coordination-deepread" / "routes.json")

CLONE_TURNS = 51          # 先例 track-C：turns 1-51 byte-identical
_EXPECTED_STEPS = 720     # 完整回放 = 初始步 + 719 动作步


class CloneReferenceError(RuntimeError):
    """克隆参照流缺失（fail-closed）。"""


def seat_action_blob(action: dict) -> str:
    """动作 dict -> 规范序列化（与 track-C extract_samples.seat_action_blob 同式）。"""
    return json.dumps({"farmer": action.get("farmer"),
                       "hands": action.get("hands") or [],
                       "market": action.get("market") or []},
                      sort_keys=True, separators=(",", ":"))


def _normalize(action: dict) -> dict:
    return {"farmer": action.get("farmer"),
            "hands": action.get("hands") or [],
            "market": action.get("market") or []}


def load_clone_signatures(clone_reference=None, turns: int = CLONE_TURNS) -> dict:
    """v48 家族参照签名：{opening 签名 -> [路由名，升序]}。

    clone_reference：routes.json 路径或 {路由名: [719 动作]} dict。
    路由 step i 对应 replay steps[i+1]（route[t]==steps[t+1].action，实测）。
    """
    if clone_reference is None:
        clone_reference = DEFAULT_ROUTES_PATH
    if isinstance(clone_reference, (str, Path)):
        try:
            routes = json.loads(Path(clone_reference).read_text(
                encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise CloneReferenceError(
                f"clone reference routes missing/corrupt (fail-closed): "
                f"{clone_reference}: {exc}") from exc
    else:
        routes = clone_reference
    sigs = {}
    for name in sorted(routes):
        tape = routes[name]
        if not isinstance(tape, list) or len(tape) < turns:
            raise CloneReferenceError(
                f"clone route shorter than {turns} turns: {name}")
        h = hashlib.sha256()
        for i in range(turns):
            h.update(seat_action_blob(tape[i]).encode("utf-8"))
        sigs.setdefault(h.hexdigest(), []).append(name)
    return sigs


def detect_own_team(games) -> str:
    """从语料实测本队名：席位名频次最高（并列取字典序最小）。"""
    counts = Counter()
    for game in games:
        for name in game.get("teams") or []:
            if name:
                counts[name] += 1
    if not counts:
        return ""
    top = max(counts.values())
    return min(name for name, n in counts.items() if n == top)


def extract_and_filter_seats(corpus, clone_reference=None, own_team=None,
                             clone_turns: int = CLONE_TURNS):
    """逐席 719 步动作流提取+克隆/我方席过滤+元数据。

    corpus：load_replay_corpus 的清单。返回 {own_team, clone_reference,
    seats, summary}；seats 按 (episode_id, seat) 升序，保留席含完整
    actions 流（719 × {farmer,hands,market}），剔除席仅元数据（无 actions）。
    """
    if not corpus or not corpus.get("games"):
        raise ValueError("empty corpus manifest")
    signatures = load_clone_signatures(clone_reference, clone_turns)
    if own_team is None:
        own_team = detect_own_team(corpus["games"])

    seats = []
    excluded = Counter()
    kept_by_category = Counter()
    for game in corpus["games"]:
        doc = json.loads(Path(game["path"]).read_text(encoding="utf-8"))
        steps = doc["steps"]
        teams = game["teams"]
        rewards = game["rewards"]
        stream_ok = len(steps) == _EXPECTED_STEPS
        per_seat = []
        for seat in range(game["seats"]):
            entry = {
                "episode_id": game["episode_id"],
                "seat": seat,
                "team": teams[seat],
                "category": game["category"],
                "n_steps": len(steps),
            }
            opponent = teams[1 - seat] if game["seats"] == 2 else None
            entry["opponent"] = opponent
            if game["seats"] == 2 and len(rewards) == 2 \
                    and rewards[seat] is not None and rewards[1 - seat] is not None:
                margin = rewards[seat] - rewards[1 - seat]
                entry["reward"] = rewards[seat]
                entry["final_margin"] = margin
                entry["result"] = "W" if margin > 0 else (
                    "L" if margin < 0 else "D")
            stream, opening_sig = _extract_stream(steps, seat, clone_turns)
            entry["opening_sig"] = opening_sig
            matched = signatures.get(opening_sig, [])
            entry["clone"] = bool(matched)
            entry["clone_routes"] = list(matched)
            if own_team and entry["team"] == own_team:
                entry["verdict"] = "own_team"
                excluded["own_team"] += 1
            elif matched:
                entry["verdict"] = "clone_v48"
                excluded["clone_v48"] += 1
            elif not stream_ok or stream is None:
                entry["verdict"] = "other"
                entry["other_reason"] = (
                    f"n_steps={len(steps)} != {_EXPECTED_STEPS}")
                excluded["other"] += 1
            else:
                entry["verdict"] = "kept"
                entry["actions"] = stream
                kept_by_category[game["category"]] += 1
            per_seat.append(entry)
        seats.extend(per_seat)

    total = len(seats)
    kept = sum(1 for s in seats if s["verdict"] == "kept")
    return {
        "own_team": own_team,
        "clone_reference": {
            "turns": clone_turns,
            "n_signatures": len(signatures),
            "routes": sorted(r for names in signatures.values() for r in names),
        },
        "seats": seats,
        "summary": {
            "games": len(corpus["games"]),
            "total_seats": total,
            "kept": kept,
            "excluded": {
                "own_team": excluded["own_team"],
                "clone_v48": excluded["clone_v48"],
                "other": excluded["other"],
            },
            "kept_by_category": dict(sorted(kept_by_category.items())),
        },
    }


def _extract_stream(steps, seat: int, clone_turns: int):
    """replay -> (719 步动作流, 开局签名)；步数异常时流为 None。"""
    h = hashlib.sha256()
    upper = min(clone_turns + 1, len(steps))
    stream = []
    for t in range(1, len(steps)):
        action = (steps[t][seat] or {}).get("action") or {}
        norm = _normalize(action)
        if t < upper:
            h.update(seat_action_blob(norm).encode("utf-8"))
        stream.append(norm)
    if len(stream) != _EXPECTED_STEPS - 1:
        return None, h.hexdigest()
    return stream, h.hexdigest()
