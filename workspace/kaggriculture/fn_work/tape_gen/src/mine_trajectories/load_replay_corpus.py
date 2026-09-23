"""load_replay_corpus（L1，R1）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

装载回放语料目录集并产出清单（manifest）：逐件 sha256、类别标注
（full=完整回放 / projection=最小投影件，按件内 ``_min_projection``
标记检测）、跨目录按 episode id 去重（full 优先于 projection，同类别按
目录清单顺序）、语料级 corpus_hash。必选目录缺失即 fail-closed；
projection 类目录允许缺席（记入 skipped_dirs）。

克隆开局判定先例：fn_work/legacy_software/bc_track/scripts/extract_samples.py
（track-C，turns 1-51 byte-identical）。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_ONLINE_REPLAYS = _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"

#: 默认语料目录集：str/Path=必选；tuple=(path, {"required": False, ...})=可选。
#: round26 / round27-ext 为 /tmp 缓存持久化产物（2026-09-22 入库，gitignored）。
DEFAULT_CORPUS_DIRS = [
    _ONLINE_REPLAYS / "round27",
    _ONLINE_REPLAYS / "round28",
    _ONLINE_REPLAYS / "round26",
    _ONLINE_REPLAYS / "round27-ext",
    (_CAMPAIGN_ROOT / "fn_docs" / "hybrid" / "results" / "replays-lead-collapse",
     {"required": False}),  # projection 类，可选
]

_REPLAY_NAME = re.compile(r"^episode-(\d+)-replay\.json$")

#: 投影件内容标记（replays-lead-collapse 归档形态：steps[t>=1] 仅保留双席 action）。
_PROJECTION_MARKER = "_min_projection"


class CorpusError(RuntimeError):
    """语料装载 fail-closed（缺目录 / 件损坏）。"""


def _iter_dir_specs(corpus_dirs):
    for entry in corpus_dirs:
        if isinstance(entry, (tuple, list)) and len(entry) == 2 \
                and isinstance(entry[1], dict):
            yield Path(entry[0]), dict(entry[1])
        else:
            yield Path(entry), {}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_replay_corpus(corpus_dirs=None):
    """输入: 语料目录集 / 输出: {{games, corpus_hash}} / 错误: 缺目录 fail-closed。

    games 逐件字段：episode_id / path / sha256 / category(full|projection) /
    teams / rewards / seats / n_steps，按 episode_id 升序。
    corpus_hash = sha256 over 规范化 [(episode_id, sha256, category)]——
    同内容同哈希，与目录顺序无关。
    """
    specs = list(_iter_dir_specs(DEFAULT_CORPUS_DIRS if corpus_dirs is None
                                 else corpus_dirs))
    games = {}          # episode_id -> game record（去重后存活件）
    shadowed = []       # 被更高优先级件压掉的同 id 件
    skipped_dirs = []   # 缺席的可选目录

    for dir_path, opts in specs:
        required = bool(opts.get("required", True))
        if not dir_path.is_dir():
            if required:
                raise CorpusError(
                    f"corpus dir missing (fail-closed): {dir_path}")
            skipped_dirs.append({"path": str(dir_path),
                                 "category": "projection"})
            continue
        for name in sorted(os.listdir(dir_path)):
            m = _REPLAY_NAME.match(name)
            if not m:
                continue  # 元数据件（episodes.json/summary.json 等）不入语料
            path = dir_path / name
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise CorpusError(f"corrupt replay file (fail-closed): "
                                  f"{path}: {exc}") from exc
            info = doc.get("info") or {}
            teams = list(info.get("TeamNames") or [])
            steps = doc.get("steps")
            if not teams or not isinstance(steps, list) or len(steps) < 2:
                raise CorpusError(f"malformed replay (fail-closed): {path}")
            episode_id = info.get("EpisodeId")
            if not isinstance(episode_id, int):
                raise CorpusError(f"missing info.EpisodeId (fail-closed): {path}")
            category = "projection" if _PROJECTION_MARKER in doc else "full"
            record = {
                "episode_id": episode_id,
                "path": str(path),
                "sha256": _sha256_file(path),
                "category": category,
                "teams": teams,
                "rewards": list(doc.get("rewards") or []),
                "seats": len(teams),
                "n_steps": len(steps),
            }
            prior = games.get(episode_id)
            if prior is None:
                games[episode_id] = record
            elif prior["category"] == "projection" and category == "full":
                games[episode_id] = record  # full 压掉 projection
                shadowed.append(_shadow(prior, record))
            else:
                shadowed.append(_shadow(record, prior))  # 先见者留

    ordered = [games[eid] for eid in sorted(games)]
    fingerprint = [[g["episode_id"], g["sha256"], g["category"]]
                   for g in ordered]
    corpus_hash = hashlib.sha256(
        json.dumps(fingerprint, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")).hexdigest()
    return {
        "games": ordered,
        "shadowed": sorted(shadowed,
                           key=lambda s: (s["episode_id"], s["path"])),
        "skipped_dirs": sorted(skipped_dirs, key=lambda s: s["path"]),
        "counts": {
            "games": len(ordered),
            "full": sum(1 for g in ordered if g["category"] == "full"),
            "projection": sum(1 for g in ordered
                              if g["category"] == "projection"),
            "shadowed": len(shadowed),
        },
        "corpus_hash": corpus_hash,
    }


def _shadow(loser: dict, winner: dict) -> dict:
    return {"episode_id": loser["episode_id"], "path": loser["path"],
            "category": loser["category"],
            "shadowed_by": winner["path"]}
