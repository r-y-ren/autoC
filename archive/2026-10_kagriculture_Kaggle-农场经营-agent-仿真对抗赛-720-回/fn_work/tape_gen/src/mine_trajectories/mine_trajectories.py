"""mine_trajectories（L0，R1）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

顶层编排：load_replay_corpus → extract_and_filter_seats → 轨迹库 JSONL
（fn_work/tape_gen/corpus/trajectory_store.jsonl）+ 摘要统计
（mining_summary.json：总席/保留席/剔除分解/语料哈希/库哈希）+ 过滤抽查
清单（filter_audit.md，≥10 局，局 id/席位/判定/依据前 51 步哈希）。

确定性：产物无墙钟字段、全排序输出——同语料双跑逐字节一致。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mine_trajectories.extract_and_filter_seats import extract_and_filter_seats
from mine_trajectories.load_replay_corpus import DEFAULT_CORPUS_DIRS, \
    load_replay_corpus

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_OUTPUT_DIR = _TAPE_GEN_ROOT / "corpus"

#: 抽查清单规模（层状确定性抽样：自博弈/克隆命中/其他 各取前 4 局）。
AUDIT_STRATA = ("self_play", "clone_hit", "other")
AUDIT_PER_STRATUM = 4


def mine_trajectories(payload=None):
    """意图级签名；真值在责任文档。

    payload 可覆盖：corpus_dirs / clone_reference / own_team / output_dir /
    audit_games。返回 {summary, manifest_counts, corpus_hash, store_sha256,
    paths}。
    """
    payload = dict(payload or {})
    output_dir = Path(payload.get("output_dir") or DEFAULT_OUTPUT_DIR)
    corpus = load_replay_corpus(payload.get("corpus_dirs"))
    result = extract_and_filter_seats(
        corpus,
        clone_reference=payload.get("clone_reference"),
        own_team=payload.get("own_team"))

    output_dir.mkdir(parents=True, exist_ok=True)
    store_path = output_dir / "trajectory_store.jsonl"
    lines = [json.dumps(seat, ensure_ascii=False, sort_keys=True,
                        separators=(",", ":"))
             for seat in result["seats"]]
    store_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    store_sha256 = hashlib.sha256(store_path.read_bytes()).hexdigest()

    summary = {
        "own_team": result["own_team"],
        "clone_reference": result["clone_reference"],
        "summary": result["summary"],
        "manifest_counts": corpus["counts"],
        "corpus_hash": corpus["corpus_hash"],
        "store_sha256": store_sha256,
        "store_lines": len(lines),
    }
    summary_path = output_dir / "mining_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n", encoding="utf-8")

    audit_path = output_dir / "filter_audit.md"
    audit_path.write_text(_audit_markdown(result,
                                          payload.get("audit_games")),
                          encoding="utf-8")

    return dict(summary, paths={
        "store": str(store_path),
        "summary": str(summary_path),
        "audit": str(audit_path),
    })


def _audit_markdown(result, audit_games=None) -> str:
    """过滤抽查清单：层状确定性抽样 ≥10 局，逐席判定+依据（前 51 步哈希）。"""
    seats = result["seats"]
    by_game = {}
    for seat in seats:
        by_game.setdefault(seat["episode_id"], []).append(seat)
    strata = {name: [] for name in AUDIT_STRATA}
    for episode_id in sorted(by_game):
        game_seats = by_game[episode_id]
        verdicts = {s["verdict"] for s in game_seats}
        if verdicts and verdicts <= {"own_team"}:
            stratum = "self_play"
        elif "clone_v48" in verdicts:
            stratum = "clone_hit"
        else:
            stratum = "other"
        strata[stratum].append(episode_id)

    limit = audit_games if isinstance(audit_games, int) and audit_games > 0 \
        else AUDIT_PER_STRATUM * len(AUDIT_STRATA)
    picked, tail = [], list(AUDIT_STRATA)
    while tail and len(picked) < limit:
        stratum = tail.pop(0)
        for episode_id in strata[stratum]:
            if len(picked) >= limit:
                break
            if episode_id not in picked:
                picked.append(episode_id)

    own = result["own_team"]
    ref = result["clone_reference"]
    lines = [
        "# 过滤抽查清单（clone 过滤人工核对用）",
        "",
        f"- 本队名（语料实测，频次最高）：`{own}`",
        f"- 克隆判定：开局 turns 1-{ref['turns']} 动作流（replay steps[1..{ref['turns']}]，"
        f"farmer+hands+market 规范 JSON）sha256（64 hex）== v48 家族路由前缀签名",
        f"（参照 routes.json {len(ref['routes'])} 条路由，实测合并为 "
        f"{ref['n_signatures']} 个有效签名——六路由前 88 步共享前缀）。",
        f"- 抽样：层状确定性（自博弈 {len(strata['self_play'])} 局 / 克隆命中 "
        f"{len(strata['clone_hit'])} 局 / 其他 {len(strata['other'])} 局，"
        "各取 episode id 升序前 4，不足顺延），本清单 "
        f"{len(picked)} 局。",
        "",
        "| 局 id | 席 | 队名 | 判定 | 依据 | 结果 | 终局边际 |",
        "|---|---|---|---|---|---|---|",
    ]
    for episode_id in picked:
        for seat in by_game[episode_id]:
            basis = _basis(seat, own)
            lines.append(
                f"| {episode_id} | {seat['seat']} | {seat['team']} "
                f"| {seat['verdict']} | {basis} | {seat.get('result', '?')} "
                f"| {seat.get('final_margin', '?')} |")
    lines.append("")
    lines.append(f"- 全库：{result['summary']}")
    lines.append("")
    return "\n".join(lines)


def _basis(seat, own_team) -> str:
    if seat["verdict"] == "own_team":
        return f"TeamNames=={own_team}（本队名）"
    if seat["verdict"] == "clone_v48":
        return (f"前51步哈希 {seat['opening_sig']} == "
                f"v48 前缀（路由 {'/'.join(seat['clone_routes'])}）")
    if seat["verdict"] == "other":
        return f"流异常：{seat.get('other_reason', '?')}"
    return f"前51步哈希 {seat['opening_sig']}（无 v48 匹配，非本队名）"
