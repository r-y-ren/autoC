"""elect_backbone（L1，R2）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

骨干选举：保留席轨迹中，farmer+hands 走位流被最多其他轨迹以 ≥ 阈值前缀
共享者为骨干。市场单**不构成共享约束**（对齐 v48 机制实证：六磁带实为
一条被验证的走位编排，farm_fast/bakery_capital 的 farmer 动作与 default
逐字相同、仅市场被改——共享前缀以 farmer+hands 流为准）。

选举规则（确定性，序即优先级，逐级消解并列）：
1. supporters@MIN_SHARED_PREFIX（默认 51，track-C/T1 开局窗口先例）最多；
2. medoid 中心性（与其余全部轨迹的走位共享前缀长度总和）最大；
3. 终局边际最大（并列走位中偏向胜局磁带，v48 "fast-climber" 先例）；
4. (episode_id, seat) 升序。

确定性：全排序输出，同输入同结果（无墙钟、无哈希随机化）。
"""

from __future__ import annotations

import json

from mine_trajectories.extract_and_filter_seats import seat_action_blob

#: 开局共享窗口（步）：track-C 克隆判定先例 turns=51。
DEFAULT_MIN_SHARED_PREFIX = 51


def movement_key(step: dict) -> str:
    """单步走位键：farmer+hands 规范 JSON（市场单不计入共享约束）。"""
    return json.dumps({"farmer": step.get("farmer"),
                       "hands": step.get("hands") or []},
                      sort_keys=True, separators=(",", ":"))


def movement_stream(actions) -> list:
    """719 步动作流 -> 走位键序列。"""
    return [movement_key(step) for step in actions]


def shared_prefix_len(stream_a, stream_b) -> int:
    """两条走位流的首个分叉步（共享前缀长度；全同则 = 流长）。"""
    upper = min(len(stream_a), len(stream_b))
    i = 0
    while i < upper and stream_a[i] == stream_b[i]:
        i += 1
    return i


def pairwise_shared_prefixes(trajectories):
    """逐对走位共享前缀长度表。

    返回 {(id_key_a, id_key_b): 共享长度}（id_key="episode_id:seat"），
    仅含 a<b（字典序）方向的一半。
    """
    streams = {}
    for rec in trajectories:
        key = f"{rec['episode_id']}:{rec['seat']}"
        streams[key] = movement_stream(rec["actions"])
    pairs = {}
    keys = sorted(streams)
    for i, ka in enumerate(keys):
        for kb in keys[i + 1:]:
            pairs[(ka, kb)] = shared_prefix_len(streams[ka], streams[kb])
    return pairs


def elect_backbone(payload=None):
    """意图级签名；真值在责任文档。

    payload：{trajectories: [保留席记录（含 actions 与元数据）],
    min_shared_prefix: int=51}。
    返回 {backbone, backbone_key, supporters, centrality, rule,
    shared_prefix_lens, streams_sha256}——shared_prefix_lens 供
    fork_routes_on_events 复用（逐对走位共享前缀）。
    错误：无有效轨迹（缺 actions）fail-closed。
    """
    payload = dict(payload or {})
    trajectories = list(payload.get("trajectories") or [])
    min_shared = int(payload.get("min_shared_prefix")
                     or DEFAULT_MIN_SHARED_PREFIX)

    usable = [rec for rec in trajectories
              if isinstance(rec.get("actions"), list) and rec["actions"]]
    if not usable:
        raise ValueError(
            "no usable trajectories for backbone election (fail-closed)")

    streams = {f"{r['episode_id']}:{r['seat']}": movement_stream(r["actions"])
               for r in usable}
    keys = sorted(streams)

    scored = []
    for key in keys:
        others = [k for k in keys if k != key]
        supporters = sum(1 for k in others
                         if shared_prefix_len(streams[key], streams[k])
                         >= min_shared)
        centrality = sum(shared_prefix_len(streams[key], streams[k])
                         for k in others)
        rec = next(r for r in usable if f"{r['episode_id']}:{r['seat']}"
                   == key)
        margin = float(rec.get("final_margin") or 0.0)
        episode_id, seat = rec["episode_id"], rec["seat"]
        # 序即优先级：supporters ↓、centrality ↓、margin ↓、(eid, seat) ↑
        scored.append((-supporters, -centrality, -margin, episode_id, seat,
                       key))
    scored.sort()
    winner = scored[0]
    backbone = next(r for r in usable
                    if f"{r['episode_id']}:{r['seat']}" == winner[5])

    pairs = {}
    for i, ka in enumerate(keys):
        for kb in keys[i + 1:]:
            pairs[(ka, kb)] = shared_prefix_len(streams[ka], streams[kb])

    return {
        "backbone": backbone,
        "backbone_key": winner[5],
        "supporters": -winner[0],
        "centrality": -winner[1],
        "rule": {
            "min_shared_prefix": min_shared,
            "priority": ["supporters@min_shared_prefix",
                         "medoid_centrality", "final_margin",
                         "(episode_id, seat) asc"],
            "note": "共享前缀以 farmer+hands 走位流为准，市场单不计入"
                    "（v48 机制：farm_fast/bakery_capital 与 default 的"
                    "farmer 流逐字相同，仅市场被改）",
        },
        "shared_prefix_lens": {f"{a}|{b}": v for (a, b), v in pairs.items()},
        "n_trajectories": len(usable),
    }
