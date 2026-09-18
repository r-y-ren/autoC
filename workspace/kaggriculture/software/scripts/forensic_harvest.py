"""Bounded forensic replay sampler —— 冲刺 ① 线上证据收口（final_sprint_plan 2026-09-19）.

用法：
    python scripts/forensic_harvest.py --targets round:15:8 round:20:12 ref:55902180:cmp-v92:12

- round:N:K  —— 取第 N 轮台账的 submission ref，抓最新 K 个 PUBLIC 局回放，
  落入正规 round 回放目录（与 sync_online_probe.fetch 同布局，可被 ingest 消费）；
- ref:R:L:K —— 无台账锚定的原始 ref（如 v9.2=55902180），落入
  references/data/online-replays/cmp-<L>/（对照目录，登记 references/INDEX.md）。

每个目标重查 episodes 清单（不依赖本地旧缓存）、按 createTime 倒序取最新 K 局、
已存在的回放文件跳过；写 forensic_manifest.json（含来源命令与抓取时间，引用纪律）。
只读 Kaggle（list/replay 下载），绝不提交。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_online_probe import (  # noqa: E402
    SOFTWARE,
    _launch,
    _parse_json_payload,
    _run_kaggle,
    campaign_root_from_software,
)

from kgenv.online_probe import replay_dir, submission_ref_of  # noqa: E402


def _episodes_for_ref(ref: int) -> list[dict]:
    raw = _run_kaggle(["competitions", "episodes", str(ref), "--format", "json"])
    eps = _parse_json_payload(raw)
    if not isinstance(eps, list):
        raise SystemExit(f"unexpected episodes payload for ref {ref}: {type(eps)}")
    return eps


def _latest_public(eps: list[dict], n: int) -> list[dict]:
    public = [e for e in eps if "PUBLIC" in str(e.get("type", ""))]
    public.sort(key=lambda e: str(e.get("createTime", "")), reverse=True)
    return public[:n]


def _fetch(dest: Path, eid) -> str:
    target = dest / f"episode-{eid}-replay.json"
    if target.exists():
        return "skip"
    _run_kaggle(["competitions", "replay", str(eid), "-p", str(dest), "-q"])
    return "fetched"


def harvest(target: str, campaign: Path) -> dict:
    parts = target.split(":")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if parts[0] == "round":
        round_no, n = int(parts[1]), int(parts[2])
        _, ledger = _launch(SOFTWARE, round_no)
        ref = submission_ref_of(ledger)
        if ref is None:
            raise SystemExit(f"round {round_no} ledger has no submission ref")
        dest = replay_dir(campaign, round_no)
        label = f"round{round_no}"
    elif parts[0] == "ref":
        ref, label, n = int(parts[1]), parts[2], int(parts[3])
        # label 原样作目录名（约定自带 cmp- 前缀，脚本不再叠加）
        dest = campaign / "references" / "data" / "online-replays" / label
    else:
        raise SystemExit(f"bad target {target!r}")
    dest.mkdir(parents=True, exist_ok=True)
    eps = _episodes_for_ref(ref)
    picked = _latest_public(eps, n)
    results = {}
    for rec in picked:
        eid = rec["id"]
        try:
            results[str(eid)] = _fetch(dest, eid)
        except Exception as exc:  # noqa: BLE001 —— 单局失败不熔断整批，如实入 manifest
            results[str(eid)] = f"failed: {str(exc)[:160]}"
    manifest = {
        "target": target,
        "label": label,
        "submission_ref": ref,
        "captured_at_utc": now,
        "source": {
            "channel": "kaggle-cli",
            "competition": "kaggriculture",
            "commands": [
                f"kaggle competitions episodes {ref} --format json",
                "kaggle competitions replay <episode_id>",
            ],
        },
        "episodes_total": len(eps),
        "selected": [
            {"id": r["id"], "createTime": r.get("createTime"), "endTime": r.get("endTime")}
            for r in picked
        ],
        "fetch_results": results,
    }
    (dest / "forensic_manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    fetched = sum(1 for v in results.values() if v == "fetched")
    skipped = sum(1 for v in results.values() if v == "skip")
    failed = sum(1 for v in results.values() if v.startswith("failed"))
    return {
        "label": label, "ref": ref, "total": len(eps), "selected": len(picked),
        "fetched": fetched, "skipped": skipped, "failed": failed,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--targets", nargs="+", required=True,
                    help="round:N:K 或 ref:R:LABEL:K，可多个")
    args = ap.parse_args()
    campaign = campaign_root_from_software(SOFTWARE)
    summary = []
    for t in args.targets:
        summary.append(harvest(t, campaign))
        print(json.dumps(summary[-1], ensure_ascii=False))
    print(json.dumps({"campaign": str(campaign), "summary": summary}, indent=1))
    return 0 if all(s["failed"] == 0 for s in summary) else 1


if __name__ == "__main__":
    raise SystemExit(main())
