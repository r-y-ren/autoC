"""边缘推理时延基准（dryrun 本机/deploy 清单，真机 manual）（bench_edge 块）。"""
from __future__ import annotations


class BenchError(Exception):
    """deploy 无目标配置。"""


def bench_edge(mode: str = "dryrun", config: dict | None = None):
    """dryrun：合成帧×predict_risk_tcn 计 P50/P95（口径 host-dryrun）；
    deploy：产 Jetson 部署指令清单（真机执行属 manual）。"""
    import statistics as stats
    import time

    if mode == "deploy":
        cfg = config or {}
        if not cfg.get("jetson_host"):
            raise BenchError("deploy 需要 config.jetson_host（设备到位后配置）")
        return {"mode": "deploy",
                "commands": [
                    f"rsync -a --exclude .venv fn_work/ {cfg['jetson_host']}:ahyd/",
                    "cd ahyd && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt",
                    ".venv/bin/python bench_edge.py --mode dryrun   # 真机口径实测",
                ],
                "note": "真机执行属 manual 项（R14），结果回读入 metrics 分片"}

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import numpy as np
    from run_progressive_risk.predict_risk_tcn import _build

    net = _build()
    net.eval()
    rng = np.random.default_rng(0)
    lat = []
    for _ in range(200):
        x = rng.normal(size=(200, 18))
        import torch
        t0 = time.perf_counter()
        with torch.no_grad():
            net(torch.as_tensor(x, dtype=torch.float32).unsqueeze(0))
        lat.append((time.perf_counter() - t0) * 1000)
    lat.sort()
    return {"mode": "dryrun", "caliber": "host-dryrun", "n": len(lat),
            "p50_ms": round(lat[len(lat) // 2], 2),
            "p95_ms": round(lat[int(len(lat) * 0.95)], 2),
            "note": "目标口径=Jetson 实测 P95≤100ms（设备到位后 deploy 真机复测）"}
