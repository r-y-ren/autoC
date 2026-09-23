"""build_route_library（L0，R2）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

顶层编排：trajectory_store（T1 产物）→ elect_backbone →
fork_routes_on_events → verify_replay_fidelity → 产物落盘
fn_work/tape_gen/library/：

* ``routes.json``——v48 可载入形态（{路由名: [719 步 {farmer,hands,
  market}]}，与参照 routes.json 同基格式，载入路径兼容：dict 名→719 步，
  shared_prefix_length ≥ 触发步，可直接喂 build_fast_route_router 的
  routes 参量）；
* ``library_manifest.json``——超集字段（骨干选举/分叉事件表/逐路由溯源/
  fidelity 结果/前缀不变量/哈希链），供 R4/R5 与审计消费。

确定性：全排序输出、规范 JSON、无墙钟字段——同库双跑逐字节一致。
错误：保留席不足（<2）fail-closed；fidelity 任一失配 fail-closed（拒绝
出库）；前缀不变量破坏 fail-closed。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build_route_library.elect_backbone import elect_backbone
from build_route_library.fork_routes_on_events import fork_routes_on_events
from build_route_library.verify_replay_fidelity import verify_replay_fidelity

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_STORE_PATH = _TAPE_GEN_ROOT / "corpus" / "trajectory_store.jsonl"
DEFAULT_OUTPUT_DIR = _TAPE_GEN_ROOT / "library"

MIN_TRAJECTORIES = 2


class LibraryError(RuntimeError):
    """路由库构建 fail-closed（轨迹不足 / fidelity 失配 / 不变量破坏）。"""


def _load_store(store_path: Path):
    seats = []
    with open(store_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("verdict") == "kept" and rec.get("actions"):
                seats.append(rec)
    seats.sort(key=lambda r: (r["episode_id"], r["seat"]))
    return seats


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _dump_routes(routes) -> str:
    return json.dumps(routes, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def build_route_library(payload=None):
    """意图级签名；真值在责任文档。

    payload 可覆盖：store_path / output_dir / replay_dirs / align_window /
    min_group_size / min_shared_prefix。返回 manifest（含 paths 与哈希）。
    """
    payload = dict(payload or {})
    store_path = Path(payload.get("store_path") or DEFAULT_STORE_PATH)
    output_dir = Path(payload.get("output_dir") or DEFAULT_OUTPUT_DIR)
    if not store_path.is_file():
        raise LibraryError(f"trajectory store missing (fail-closed): "
                           f"{store_path}")

    trajectories = _load_store(store_path)
    if len(trajectories) < MIN_TRAJECTORIES:
        raise LibraryError(f"kept trajectories {len(trajectories)} < "
                           f"{MIN_TRAJECTORIES} (fail-closed)")

    election = elect_backbone({
        "trajectories": trajectories,
        "min_shared_prefix": payload.get("min_shared_prefix"),
    })
    backbone = election["backbone"]

    forked = fork_routes_on_events({
        "backbone": backbone,
        "trajectories": trajectories,
        "replay_dirs": payload.get("replay_dirs"),
        "align_window": payload.get("align_window"),
        "min_group_size": payload.get("min_group_size"),
    })
    routes = forked["routes"]
    if not forked["prefix_invariant_ok"]:
        raise LibraryError(
            f"prefix invariant broken: shared_prefix "
            f"{forked['shared_prefix']} < trigger "
            f"{forked['trigger_step']} (fail-closed)")

    sources = {"default": {"actions": backbone["actions"],
                           "aligned_from": 0}}
    for row in forked["fork_table"]:
        if row["status"] != "route":
            continue
        member = next(
            r for r in trajectories
            if f"{r['episode_id']}:{r['seat']}" == row["route_source"])
        sources[row["route_name"]] = {
            "actions": member["actions"],
            "aligned_from": row["fork_step"],
            "prefix_actions": backbone["actions"],
        }
    fidelity = verify_replay_fidelity({"routes": routes,
                                       "sources": sources})
    if not fidelity["all_ok"]:
        raise LibraryError(f"replay fidelity broken (fail-closed): "
                           f"{fidelity['fidelity']}")

    routes_text = _dump_routes(routes)
    routes_sha = _sha256_text(routes_text)
    manifest = {
        "format": {
            "base": "v48 routes.json（dict 路由名 -> [719 步 "
                    "{farmer,hands,market}]）",
            "load_path": "兼容 v48 fast_route_router.routes 参量与 "
                         "v23 policy_library.RouteLibrary（dict 名->719 "
                         "步；shared_prefix ≥ 触发步）",
            "superset_fields": "仅 library_manifest.json（routes.json "
                               "本身保持纯基格式）",
        },
        "store": {
            "path": str(store_path),
            "sha256": _sha256_text(store_path.read_text(encoding="utf-8")),
            "kept_trajectories": len(trajectories),
        },
        "backbone_election": {
            "backbone": election["backbone_key"],
            "episode_id": backbone["episode_id"],
            "seat": backbone["seat"],
            "team": backbone.get("team"),
            "opponent": backbone.get("opponent"),
            "result": backbone.get("result"),
            "final_margin": backbone.get("final_margin"),
            "supporters": election["supporters"],
            "centrality": election["centrality"],
            "rule": election["rule"],
            "n_trajectories": election["n_trajectories"],
        },
        "fork_events": {
            "align_window": forked["align_window"],
            "min_group_size": forked["min_group_size"],
            "trigger_step": forked["trigger_step"],
            "shared_prefix": forked["shared_prefix"],
            "prefix_invariant_ok": forked["prefix_invariant_ok"],
            "walk_identical_count": forked["walk_identical_count"],
            "fork_table": forked["fork_table"],
        },
        "routes": {
            name: {
                "n_steps": len(steps),
                "sha256": _sha256_text(_dump_routes(steps)),
                "source_kind": "backbone" if name == "default"
                else "fork_member",
                "fork_step": sources[name]["aligned_from"],
            } for name, steps in sorted(routes.items())
        },
        "route_provenance": {
            name: {
                "source_seat": (f"{backbone['episode_id']}:"
                                f"{backbone['seat']}"
                                if name == "default"
                                else next(
                                    r2 for r2 in forked["fork_table"]
                                    if r2.get("route_name") == name
                                )["route_source"]),
                "aligned_from": sources[name]["aligned_from"],
            } for name in sorted(routes)
        },
        "fidelity": fidelity,
        "routes_sha256": routes_sha,
        "n_routes": len(routes),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    routes_path = output_dir / "routes.json"
    routes_path.write_text(routes_text + "\n", encoding="utf-8")
    manifest_path = output_dir / "library_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n", encoding="utf-8")

    manifest["paths"] = {"routes": str(routes_path),
                         "manifest": str(manifest_path)}
    return manifest
