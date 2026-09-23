"""split_train_holdout（L1，R5）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

对手级不相交分离（种子化；留出 ≥30% 对手；对手名单从轨迹库元数据取）。

* 对手身份 = 保留席（kept 席）的 ``team`` 字段（T1 轨迹库元数据）——
  保留席即对手席，其 ``opponent`` 字段恒为我方（renyxin），不可用作对手
  名单。我席 = 对手席对席（me_seat = 1 − opp_seat；seated 重演注入位）。
* **挖掘源圈禁**：库件来源对手（backbone=Anton Tikhonov、fork 后缀=
  Yuzu——library_manifest.json route_provenance 真值）强制入训练侧；
  留出对手与挖掘源不相交（R9 镜像假阳教训内建）。
* 分离算法（确定性）：对手全序（team 字典序）→ random.Random(seed)
  shuffle → 从可分池（=全对手 − 挖掘源）取前 ceil(30%×总对手数) 为留出
  → 其余 + 挖掘源为训练。局随对手走（一局=一保留席=一对手）。
* 证明字段：train/holdout 对手交集 = []、留出对手占比 ≥0.30、挖掘源
  ∉ 留出、me_seat/opp_seat 互补——写入 split 产物供验收。
* fail-closed：留出局不足（< min_holdout_games，缺省 30）或留出对手占比
  < 请求占比 → ValueError。

回放定位：按 T1 语料目录序（round27→round28→round26→round27-ext→
lead-collapse）扫 episode-*-replay.json 文件名建索引；保留席缺回放
（fail-closed）。产物（output_dir）：split_train_holdout.json。
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_STORE_PATH = _TAPE_GEN_ROOT / "corpus" / "trajectory_store.jsonl"

#: T1 语料目录序（load_replay_corpus.DEFAULT_CORPUS_DIRS 同序，缺者跳过）。
DEFAULT_REPLAY_DIRS = (
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round27",
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round28",
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round26",
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round27-ext",
    _CAMPAIGN_ROOT / "fn_docs" / "hybrid" / "results"
    / "replays-lead-collapse",
)

#: 库件来源对手（挖掘源；library_manifest.json route_provenance 真值：
#: default←111298489:1 Anton Tikhonov，fork_s73_e72←112028163:1 Yuzu；
#: 市场变体派生自 default 骨干，同源）。
MINING_SOURCE_OPPONENTS = ("Anton Tikhonov", "Yuzu")

DEFAULT_SEED = 20260923
DEFAULT_HOLDOUT_FRACTION = 0.30
DEFAULT_MIN_HOLDOUT_GAMES = 30


def _canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _path_free(split) -> dict:
    """split 的去路径投影（replay_path → 文件名）：split_sha256 只沉淀
    跨机可复现的分离事实（对手归属/局单/种子），不掺本机绝对路径。"""
    projection = json.loads(_canonical(split))

    def strip(games):
        return [{k: v for k, v in g.items() if k != "replay_path"}
                for g in games]
    projection["train"]["games"] = strip(projection["train"]["games"])
    projection["holdout"]["games"] = strip(projection["holdout"]["games"])
    return projection


def build_replay_index(replay_dirs=None):
    """episode_id → 回放路径（目录序扫描；文件名序确定）。"""
    dirs = replay_dirs or DEFAULT_REPLAY_DIRS
    index = {}
    for directory in dirs:
        directory = Path(directory)
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("episode-*-replay.json")):
            try:
                episode_id = int(path.name.split("-")[1])
            except (IndexError, ValueError):
                continue
            index.setdefault(episode_id, str(path))
    return index


def load_kept_games(store_path=None, replay_dirs=None):
    """轨迹库保留席 → 局清单（对手=team、我席=对席、回放路径）。"""
    store_path = Path(store_path) if store_path else DEFAULT_STORE_PATH
    if not store_path.is_file():
        raise ValueError(f"trajectory store missing (fail-closed): "
                         f"{store_path}")
    index = build_replay_index(replay_dirs)
    games = []
    with store_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if "actions" not in record:
                continue  # 元数据行（我方/克隆席）——非对手局
            episode_id = int(record["episode_id"])
            opp_seat = int(record["seat"])
            replay_path = index.get(episode_id)
            if replay_path is None:
                raise ValueError(f"replay file missing for kept seat "
                                 f"(fail-closed): {episode_id}:{opp_seat}")
            games.append({
                "episode_id": episode_id,
                "opp_seat": opp_seat,
                "me_seat": 1 - opp_seat,
                "opponent": str(record["team"]),
                "result": record.get("result"),
                "final_margin": record.get("final_margin"),
                "replay_path": replay_path,
            })
    games.sort(key=lambda g: (g["episode_id"], g["opp_seat"]))
    return games


def split_train_holdout(payload=None):
    """意图级签名；真值在责任文档。

    payload：{store_path, replay_dirs, seed=20260923,
    holdout_fraction=0.30, min_holdout_games=30, forced_train_opponents
    （缺省 MINING_SOURCE_OPPONENTS）, output_dir}。
    返回 {seed, train, holdout, proof, split_sha256}；train/holdout 各含
    opponents 与 games（局随对手走）；proof={intersection（必空）,
    holdout_opponent_fraction, mining_sources_in_store,
    mining_sources_in_holdout（必空）, seat_complement_ok}。
    output_dir 给定时写 split_train_holdout.json。
    """
    payload = dict(payload or {})
    seed = int(payload.get("seed") or DEFAULT_SEED)
    fraction = float(payload.get("holdout_fraction")
                     or DEFAULT_HOLDOUT_FRACTION)
    min_games = int(payload.get("min_holdout_games")
                    or DEFAULT_MIN_HOLDOUT_GAMES)
    forced = list(payload.get("forced_train_opponents")
                  or MINING_SOURCE_OPPONENTS)

    games = load_kept_games(payload.get("store_path"),
                            payload.get("replay_dirs"))
    if not games:
        raise ValueError("no kept games found (fail-closed)")

    opponents = sorted({g["opponent"] for g in games})
    forced_set = set(forced)
    eligible = [o for o in opponents if o not in forced_set]
    n_holdout = min(len(eligible),
                    max(1, math.ceil(fraction * len(opponents))))
    shuffled = list(eligible)
    random.Random(seed).shuffle(shuffled)
    holdout_opponents = set(shuffled[:n_holdout])
    train_opponents = set(opponents) - holdout_opponents

    train_games = [g for g in games if g["opponent"] in train_opponents]
    holdout_games = [g for g in games
                     if g["opponent"] in holdout_opponents]

    intersection = sorted(train_opponents & holdout_opponents)
    holdout_fraction_actual = len(holdout_opponents) / len(opponents)
    mining_in_holdout = sorted(forced_set & holdout_opponents)
    if intersection:
        raise ValueError(f"split leak: {intersection} (fail-closed)")
    if mining_in_holdout:
        raise ValueError(f"mining source leaked into holdout: "
                         f"{mining_in_holdout} (fail-closed)")
    if holdout_fraction_actual < fraction - 1e-9:
        raise ValueError(
            f"holdout opponents {holdout_fraction_actual:.4f} < "
            f"{fraction:.4f} (fail-closed)")
    if len(holdout_games) < min_games:
        raise ValueError(f"holdout games {len(holdout_games)} < "
                         f"{min_games} (fail-closed)")

    result = {
        "seed": seed,
        "holdout_fraction_requested": fraction,
        "train": {
            "opponents": sorted(train_opponents),
            "games": train_games,
        },
        "holdout": {
            "opponents": sorted(holdout_opponents),
            "games": holdout_games,
        },
        "proof": {
            "intersection": intersection,
            "n_opponents_total": len(opponents),
            "n_train_opponents": len(train_opponents),
            "n_holdout_opponents": len(holdout_opponents),
            "holdout_opponent_fraction": holdout_fraction_actual,
            "n_train_games": len(train_games),
            "n_holdout_games": len(holdout_games),
            "mining_source_opponents": sorted(forced_set),
            "mining_sources_in_store": sorted(forced_set
                                              & set(opponents)),
            "mining_sources_in_holdout": mining_in_holdout,
            "seat_complement_ok": all(
                g["me_seat"] == 1 - g["opp_seat"]
                for g in train_games + holdout_games),
        },
    }
    result["split_sha256"] = hashlib.sha256(
        _canonical(_path_free(result)).encode("utf-8")).hexdigest()

    output_dir = payload.get("output_dir")
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "split_train_holdout.json"
        path.write_text(_canonical(result) + "\n", encoding="utf-8")
        result["paths"] = {"split": str(path)}
    return result
