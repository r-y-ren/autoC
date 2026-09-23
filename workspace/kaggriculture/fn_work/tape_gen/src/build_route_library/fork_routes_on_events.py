"""fork_routes_on_events（L1，R2）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

商店事件分叉：从骨干 diverge 的轨迹按**首个走位分叉步**分组，与公开商店
事件对齐——事件步从轨迹 observability 实测（源回放 steps[e][seat].
observation.town.unlocked_shops 新店解锁，e=回放步索引）；对齐窗
0 ≤ f−e ≤ ALIGN_WINDOW（v48 实证锚：首店事件落日界 72k 步，路由 fork
88 ↔ 事件 72 gap=16、yarn_third fork 216 ↔ 事件 216 gap=0；本语料实测
主分叉族 fork 73 ↔ 事件 72 gap=1）。fork 早于事件（f<e）为因果不可能，
一律不对齐。

构造嵌缀树路由：route = 骨干全步 [0,f) + 分叉成员后缀 [f,719)——前缀共享
是设计不变量（v48 v23/policy_library.RouteLibrary.__post_init__：
shared_prefix_length(routes) ≥ 触发步）。每组出一条代表路由（稀疏纪律）：
组内按（终局边际 ↓ → 组内后缀中心性 ↓ → (eid,seat) ↑）选代表。
"""

from __future__ import annotations

import copy
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from build_route_library.elect_backbone import movement_stream, \
    shared_prefix_len

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]

#: 事件观测的源回放目录（与 T1 load_replay_corpus 默认语料一致，只读）。
DEFAULT_REPLAY_DIRS = [
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round27",
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round28",
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round26",
    _CAMPAIGN_ROOT / "fn_docs" / "references" / "data" / "online-replays"
    / "round27-ext",
]

#: 对齐窗：fork−event ∈ [0, 16]（v48 gap 0/16 双实证锚的包络）。
ALIGN_WINDOW = 16
#: 成组最小成员数（独立对局证据 ≥2，稀疏纪律）。
MIN_GROUP_SIZE = 2

_REPLAY_NAME = re.compile(r"^episode-(\d+)-replay\.json$")


def resolve_replay_path(episode_id, replay_dirs=None):
    """按 episode id 在语料目录集定位源回放（先见者留，与 T1 去重序一致）。"""
    dirs = [Path(d) for d in (DEFAULT_REPLAY_DIRS if replay_dirs is None
                              else replay_dirs)]
    for dir_path in dirs:
        candidate = dir_path / f"episode-{episode_id}-replay.json"
        if candidate.is_file():
            return candidate
    return None


def shop_events(replay_path, seat: int):
    """源回放 -> [(事件步 e, 新解锁店名, 解锁后 shops 全序)]。

    事件步 = 回放步索引 t（obs at steps[t]；live 侧 obs.step==t 同一观测，
    v48 路由器即在该面读 town.unlocked_shops）。观测缺失/无镇数据 -> []。
    """
    try:
        doc = json.loads(Path(replay_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    events = []
    seen = []
    for t, step in enumerate(doc.get("steps") or []):
        entry = step[seat] if isinstance(step, list) and len(step) > seat \
            else {}
        obs = (entry or {}).get("observation") or {}
        shops = [str(s) for s in
                 ((obs.get("town") or {}).get("unlocked_shops") or [])]
        for shop in shops:
            if shop not in seen:
                seen.append(shop)
                events.append((t, shop, list(shops)))
    return events


def _member_events(episode_id, seat, replay_dirs, cache):
    key = (int(episode_id), int(seat))
    if key not in cache:
        path = resolve_replay_path(episode_id, replay_dirs)
        cache[key] = shop_events(path, seat) if path else None
    return cache[key]


def _fork_groups(backbone_stream, trajectories, backbone_key):
    """按首个走位分叉步分组成员（骨干自身与全同走位除外）。"""
    groups = defaultdict(list)
    identical = []
    for rec in trajectories:
        key = f"{rec['episode_id']}:{rec['seat']}"
        if key == backbone_key:
            continue
        fork = shared_prefix_len(backbone_stream, movement_stream(
            rec["actions"]))
        if fork >= len(backbone_stream):
            identical.append(rec)      # 全同走位：非分叉（骨干佐证）
        else:
            groups[fork].append(rec)
    return groups, identical


def _align_group(members, fork, replay_dirs, event_cache,
                 align_window=ALIGN_WINDOW):
    """组对齐裁决：组内多数成员在同一事件步 e 有窗内新店解锁。

    返回 (aligned, event_step, evidence)：evidence.per_member 为逐成员
    窗内事件步；对齐要求同一 e 的计票 ≥ 半数（向上取整）且 ≥1。
    """
    votes = Counter()
    per_member = {}
    for rec in members:
        events = _member_events(rec["episode_id"], rec["seat"],
                                replay_dirs, event_cache)
        ev_steps = set()
        if events:
            for e, _shop, _shops in events:
                if 0 <= fork - e <= align_window:
                    ev_steps.add(e)
        per_member[f"{rec['episode_id']}:{rec['seat']}"] = sorted(ev_steps)
        for e in ev_steps:
            votes[e] += 1
    if not votes:
        return False, None, {"per_member": per_member, "votes": {}}
    need = max(1, -(-len(members) // 2))
    best_e, best_n = None, -1
    for e in sorted(votes):
        if votes[e] > best_n:
            best_e, best_n = e, votes[e]
    aligned = best_n >= need
    return aligned, (best_e if aligned else None), {
        "per_member": per_member,
        "votes": {str(e): votes[e] for e in sorted(votes)},
        "quorum": need,
    }


def _representative(members, fork):
    """组代表：终局边际 ↓ → 组内后缀中心性 ↓ → (eid, seat) ↑。"""
    streams = {f"{r['episode_id']}:{r['seat']}":
               movement_stream(r["actions"]) for r in members}

    def suffix_centrality(rec):
        key = f"{rec['episode_id']}:{rec['seat']}"
        own = streams[key][fork:]
        return sum(shared_prefix_len(own, streams[k][fork:])
                   for k in streams if k != key)

    return sorted(members, key=lambda r: (
        -float(r.get("final_margin") or 0.0), -suffix_centrality(r),
        r["episode_id"], r["seat"]))[0]


def _route_steps(backbone_actions, member_actions, fork):
    """嵌缀路由：骨干全步 [0,f) + 成员后缀 [f,719)（深拷贝，防串改）。"""
    route = copy.deepcopy(backbone_actions[:fork])
    route.extend(copy.deepcopy(member_actions[fork:]))
    return route


def shared_full_prefix(routes):
    """v48 shared_prefix_length 同义实现（全动作 dict 逐步比较）。"""
    if not routes:
        return 0
    rows = list(routes.values())
    prefix = 0
    for actions in zip(*rows):
        if any(a != actions[0] for a in actions[1:]):
            break
        prefix += 1
    return prefix


def fork_routes_on_events(payload=None):
    """意图级签名；真值在责任文档。

    payload：{backbone: 骨干记录, trajectories: [保留席], replay_dirs,
    align_window=16, min_group_size=2}。
    返回 {routes, default_name, fork_table, trigger_step, shared_prefix,
    prefix_invariant_ok, walk_identical_count, ...}；routes 含骨干
    default 与每个对齐分叉组一条代表路由（名 fork_s{f}_e{e}）。
    错误：缺骨干/保留席 fail-closed。
    """
    payload = dict(payload or {})
    backbone = payload.get("backbone")
    trajectories = list(payload.get("trajectories") or [])
    if not backbone or not trajectories:
        raise ValueError("fork_routes_on_events needs backbone and "
                         "trajectories (fail-closed)")
    min_group = int(payload.get("min_group_size") or MIN_GROUP_SIZE)
    align_window = int(payload.get("align_window") or ALIGN_WINDOW)
    replay_dirs = payload.get("replay_dirs")

    backbone_key = f"{backbone['episode_id']}:{backbone['seat']}"
    backbone_stream = movement_stream(backbone["actions"])
    groups, identical = _fork_groups(backbone_stream, trajectories,
                                     backbone_key)

    routes = {"default": copy.deepcopy(backbone["actions"])}
    fork_table = []
    event_cache = {}
    trigger_step = None

    for fork in sorted(groups):
        members = groups[fork]
        aligned, event_step, evidence = _align_group(
            members, fork, replay_dirs, event_cache, align_window)
        best = _representative(members, fork)
        row = {
            "fork_step": fork,
            "n_members": len(members),
            "members": [f"{r['episode_id']}:{r['seat']}" for r in members],
            "event_aligned": aligned,
            "event_step": event_step,
            "gap": (fork - event_step) if aligned else None,
            "best_member": f"{best['episode_id']}:{best['seat']}",
            "best_margin": best.get("final_margin"),
            "alignment_evidence": evidence,
        }
        if not aligned:
            row["status"] = "excluded_unaligned"
            fork_table.append(row)
            continue
        if len(members) < min_group:
            row["status"] = "excluded_singleton"
            fork_table.append(row)
            continue
        name = f"fork_s{fork}_e{event_step}"
        routes[name] = _route_steps(backbone["actions"],
                                    best["actions"], fork)
        row["status"] = "route"
        row["route_name"] = name
        row["route_source"] = f"{best['episode_id']}:{best['seat']}"
        fork_table.append(row)
        if trigger_step is None or event_step < trigger_step:
            trigger_step = event_step

    shared_prefix = shared_full_prefix(routes)
    return {
        "routes": routes,
        "default_name": "default",
        "fork_table": fork_table,
        "trigger_step": trigger_step if trigger_step is not None
        else shared_prefix,
        "shared_prefix": shared_prefix,
        "prefix_invariant_ok": (trigger_step is None
                                or shared_prefix >= trigger_step),
        "walk_identical_count": len(identical),
        "walk_identical_members": [
            f"{r['episode_id']}:{r['seat']}" for r in identical],
        "align_window": align_window,
        "min_group_size": min_group,
    }
