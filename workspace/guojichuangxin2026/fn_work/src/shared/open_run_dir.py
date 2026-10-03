"""创建时间戳运行目录+运行清单（配置/种子/机器/设备在场清单）（shared 块）。"""
from __future__ import annotations

import json
import platform
import socket
from datetime import datetime
from pathlib import Path


def open_run_dir(root: str, scenario: str, seed: int | None = None,
                 config_snapshot: dict | None = None) -> Path:
    """返回运行目录；同秒冲突加 +n 序号；根不可写抛 IOError。

    签名微调：新增可选 config_snapshot（登记于 batches.md 变更记录）。
    """
    base = Path(root) / scenario
    base.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    probe = base / (f"{stamp}-{seed}" if seed is not None else stamp)
    run_dir, n = probe, 2
    while run_dir.exists():
        run_dir = base / f"{probe.name}+{n}"
        n += 1
    try:
        run_dir.mkdir()
        (run_dir / "raw").mkdir()
        (run_dir / "frames").mkdir()
    except OSError as exc:
        raise IOError(f"运行目录不可写: {run_dir}") from exc
    manifest = {
        "scenario": scenario, "seed": seed,
        "created": datetime.now().isoformat(timespec="seconds"),
        "host": {"name": socket.gethostname(), "machine": platform.machine(),
                 "python": platform.python_version()},
        "config_snapshot": config_snapshot or {},
        "modules_present": [],
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    return run_dir
