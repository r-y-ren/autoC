"""R1 验收本体：帧率/字段覆盖率检查，退出码判定（run_ingest 块）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HZ_MIN = 20.0
_CORE = ("t", "roll", "pitch", "yaw", "voltage", "battery_remaining",
         "lat", "lon", "hdop", "rssi")
_COVER_MIN = 0.9


def replay_check(run_dir: str) -> int:
    """读 run_dir/frames/frames.jsonl → 报告帧率/覆盖率/掩码分布；PASS 返回 0。"""
    d = Path(run_dir)
    fp = d / "frames" / "frames.jsonl"
    if not fp.exists():
        print(f"ERR 目录结构不合法: {fp} 不存在", file=sys.stderr)
        return 2
    frames = [json.loads(x) for x in fp.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(frames) < 3:
        print("ERR 帧数不足（<3）", file=sys.stderr)
        return 2
    ts = [float(f["t"]) for f in frames if f.get("t") is not None]
    hz = (len(ts) - 1) / (ts[-1] - ts[0]) if len(ts) > 1 and ts[-1] > ts[0] else 0.0
    cover = {k: sum(1 for f in frames if f.get(k) is not None) / len(frames) for k in _CORE}
    masks = {}
    for f in frames:
        for k, v in (f.get("quality_mask") or {}).items():
            masks.setdefault(k, [0, 0])[1] += 1
            if v:
                masks[k][0] += 1
    bad_cover = [k for k, c in cover.items() if c < _COVER_MIN]
    ok = hz >= _HZ_MIN and not bad_cover
    report = {"run_dir": str(d), "frames": len(frames), "hz": round(hz, 1),
              "coverage": {k: round(c, 3) for k, c in cover.items()},
              "mask_ok_ratio": {k: round(a / b, 3) for k, (a, b) in masks.items()},
              "pass": ok}
    (d / "frames" / "replay_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[replay_check] frames={len(frames)} hz={hz:.1f} "
          f"({'PASS' if ok else 'FAIL'}；覆盖率不足字段={bad_cover or '无'})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(replay_check(sys.argv[1] if len(sys.argv) > 1 else "runs/latest"))
