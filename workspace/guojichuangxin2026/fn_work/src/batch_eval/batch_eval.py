"""跨场景批量总控：探测数据面→模型保障→run_eval×N→归档→快照（batch_eval 块）。"""
from __future__ import annotations


def batch_eval(scenarios: list, runs_per_scenario: int = 30,
               config: dict | None = None):
    """R11 验收本体。PX4 就绪→data_source=px4（spawn px4 会话）；否则 synthetic 兜底并记原因。

    模型保障：config.model 缺失时先合成重训（train_tcn，标 synthetic-trained）。
    每运行 archive_run 归档；快照 JSON 写 fn_docs/results/。
    """
    import json
    import time
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]           # fn_work
    campaign = Path(__file__).resolve().parents[3]       # 战役根（fn_docs/results 的家）
    import sys
    sys.path.insert(0, str(root / "src"))
    from batch_eval.probe_px4_env import probe_px4_env
    from shared.archive_run import archive_run

    cfg = dict(config or {})
    env = probe_px4_env({"px4_dir": cfg.get("px4_dir", "")})
    data_source = "px4" if env["ready"] else "synthetic"
    downgrade_note = "" if env["ready"] else "PX4 未就绪: " + "; ".join(env["missing"])

    model = cfg.get("model")
    quantiles = cfg.get("quantiles")
    model_note = "provided"
    if model is None and cfg.get("ensure_model", True):
        model, quantiles, model_note = _ensure_model(cfg)

    out = {"ts": time.strftime("%Y%m%d-%H%M%S"),
           "data_source": data_source, "downgrade_note": downgrade_note,
           "model": model_note, "scenarios": {}, "runs_total": 0}
    for sc in scenarios:
        from shared.run_eval import run_eval
        runs_root = cfg.get("runs_root", str(root / "runs"))
        summary = run_eval(sc, runs_per_scenario,
                           config={**cfg, "model": model, "quantiles": quantiles,
                                   "data_source": data_source,
                                   "note": f"{data_source}-mid"
                                   + ("+degraded-model" if model is None else "")})
        archived = []
        for rd in sorted(Path(runs_root).glob(f"{sc}_eval/*")):
            if (rd / "metrics.jsonl").exists():
                archived.append(archive_run(str(rd), str(campaign / "fn_docs" / "results")))
        out["scenarios"][sc] = {"summary": summary.get("summary"),
                                "archived_runs": len(archived)}
        out["runs_total"] += len(archived)
    snap = campaign / "fn_docs" / "results" / f"batch-{out['ts']}.json"
    snap.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    out["snapshot"] = str(snap)
    print(json.dumps({k: v for k, v in out.items() if k != "scenarios"},
                     ensure_ascii=False))
    return out


def _ensure_model(cfg):
    """模型工件保障：缺则合成重训（synthetic-trained 口径）。"""
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "src"))
    ckpt = root / "checkpoints" / "tcn.pt"
    if ckpt.exists() and not cfg.get("retrain"):
        from run_progressive_risk.build_feature_window import FEATURE_NAMES
        try:
            from shared.load_model_artifact import load_model_artifact
            blob = load_model_artifact(str(ckpt), FEATURE_NAMES)
            from run_progressive_risk.predict_risk_tcn import _build
            import torch
            net = _build()
            net.load_state_dict(blob["state_dict"])
            net.eval()
            return net, {"1": 0.05, "3": 0.10, "5": 0.15, "10": 0.20}, "ckpt-reused"
        except Exception:
            pass
    from launch_demo_session.spawn_sitl import SyntheticSITL
    from run_ingest.run_ingest import run_ingest
    from run_progressive_risk.train_tcn import train_tcn
    import tempfile
    dirs = []
    with tempfile.TemporaryDirectory() as td:
        for i in range(3):
            rd = Path(td) / f"r{i}"
            rd.mkdir()
            list(run_ingest({"run": {"hz": 20, "duration_s": 10.0,
                                     "home": [32.0, 118.8], "endpoint": "inproc"}},
                            rd, conn=SyntheticSITL("lowbat_headwind")))
            dirs.append(str(rd))
        res = train_tcn(dirs, {"epochs": 2, "out_dir": str(root / "checkpoints"),
                               "min_frames": 60})
    from run_progressive_risk.build_feature_window import FEATURE_NAMES
    from shared.load_model_artifact import load_model_artifact
    from run_progressive_risk.predict_risk_tcn import _build
    blob = load_model_artifact(res["checkpoint"], FEATURE_NAMES)
    net = _build()
    import torch
    net.load_state_dict(blob["state_dict"])
    net.eval()
    return net, {"1": 0.05, "3": 0.10, "5": 0.15, "10": 0.20}, "synthetic-trained"
