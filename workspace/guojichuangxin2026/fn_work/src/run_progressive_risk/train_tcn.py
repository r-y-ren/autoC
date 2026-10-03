"""离线训练管线：样本生成（按架次分组防泄漏）→轻量 TCN checkpoint（run_progressive_risk 块）。"""
from __future__ import annotations


class TrainError(Exception):
    """数据不足/标注缺失。"""


def _load_run(data_dir: str):
    import json
    from pathlib import Path
    d = Path(data_dir)
    fp = d / "frames" / "frames.jsonl"
    if not fp.exists():
        raise TrainError(f"运行目录缺 frames: {d}")
    frames = [json.loads(x) for x in fp.read_text(encoding="utf-8").splitlines() if x.strip()]
    man = d / "manifest.json"
    manifest = json.loads(man.read_text(encoding="utf-8")) if man.exists() else {}
    return frames, manifest


def _labels_for(frames, manifest, danger_battery=25.0):
    """危险标签：battery_remaining 首次跌破 danger_battery 的时刻起=1（失控判据：返航能源线）。"""
    t_danger = None
    for f in frames:
        b = f.get("battery_remaining")
        if b is not None and b < danger_battery and t_danger is None:
            t_danger = float(f.get("t", 0))
    return t_danger


def make_dataset(data_dirs: list, cfg: dict | None = None):
    """(X 窗, y 未来 5s 危险, 架次 id) 三元组列表；按目录=架次分组防泄漏。"""
    from run_progressive_risk.build_feature_window import build_feature_window
    samples = []
    for gid, dd in enumerate(data_dirs):
        frames, manifest = _load_run(dd)
        t_danger = _labels_for(frames, manifest)
        if t_danger is None:
            continue  # 无危险标注的架次只供背景（跳过监督样本）
        for i in range(len(frames)):
            win = build_feature_window(frames[: i + 1], {"hz": 20, "min_frames": 160})
            if win is None:
                continue
            t = float(frames[i].get("t", 0))
            y = 1.0 if t + 5.0 >= t_danger else 0.0
            samples.append((win, y, gid))
    if not samples:
        raise TrainError("无监督样本（缺危险标注架次或窗不足）")
    return samples


def train_tcn(data_dirs: list, train_config: dict) -> dict:
    """小数据快速训练（默认 3 epoch CPU 可跑）；产 checkpoint+元数据+验证报告。"""
    import json
    import time
    from pathlib import Path

    import numpy as np
    import torch
    import torch.nn as nn

    from run_progressive_risk.build_feature_window import FEATURE_NAMES
    from run_progressive_risk.predict_risk_tcn import _build

    cfg = {"epochs": int(train_config.get("epochs", 3)), "lr": 1e-3,
           "batch": 8, "seed": int(train_config.get("seed", 42))}
    torch.manual_seed(cfg["seed"])
    samples = make_dataset(data_dirs, train_config)
    # 分组切分：架次为界（同一架次只进一个集合）
    gids = sorted({g for _, _, g in samples})
    val_g = {gids[-1]} if len(gids) > 1 else set()
    tr = [(x, y) for x, y, g in samples if g not in val_g]
    va = [(x, y) for x, y, g in samples if g in val_g] or tr[-2:]
    if len(tr) < 4:
        raise TrainError(f"训练样本不足: {len(tr)}")
    net = _build()
    params = sum(p.numel() for p in net.parameters())
    if params > 2_000_000:
        raise TrainError(f"参数量超限: {params}")
    opt = torch.optim.Adam(net.parameters(), lr=cfg["lr"])
    lossf = nn.BCEWithLogitsLoss()
    hist = []
    t0 = time.time()
    for ep in range(cfg["epochs"]):
        net.train()
        idx = np.random.permutation(len(tr))
        tot = 0.0
        for s in range(0, len(tr), cfg["batch"]):
            rows = [tr[i] for i in idx[s : s + cfg["batch"]]]
            t_min = min(r[0].shape[0] for r in rows)          # 因果窗：按最短裁尾
            xb = torch.as_tensor(np.stack([r[0][-t_min:] for r in rows]), dtype=torch.float32)
            # 末帧特征→危险头（简化监督：池化整体判未来 5s）
            yb = torch.as_tensor([r[1] for r in rows], dtype=torch.float32).view(-1, 1)
            out = net(xb)
            logits = out["raw"]["probs"][:, 2:3].logit()
            loss = lossf(logits, yb)
            opt.zero_grad(); loss.backward(); opt.step()
            tot += float(loss)
        net.eval()
        with torch.no_grad():
            vv = va[:16]
            tv = min(r[0].shape[0] for r in vv)
            vx = torch.as_tensor(np.stack([r[0][-tv:] for r in vv]), dtype=torch.float32)
            vy = np.array([r[1] for r in va[:16]])
            vp = net(vx)["raw"]["probs"][:, 2].numpy()
            val_acc = float(((vp > 0.5).astype(float) == vy).mean()) if len(vp) else float("nan")
        hist.append({"epoch": ep + 1, "train_loss": round(tot / max(1, len(tr) // cfg["batch"]), 4),
                     "val_acc_5s": round(val_acc, 3)})
    out_dir = Path(train_config.get("out_dir", "checkpoints"))
    out_dir.mkdir(parents=True, exist_ok=True)
    ckpt = out_dir / "tcn.pt"
    torch.save({"state_dict": net.state_dict(), "feature_names": FEATURE_NAMES,
                "version": f"tcn-{int(time.time())}", "kind": "tcn",
                "params": params, "history": hist}, ckpt)
    report = out_dir / "train_report.json"
    report.write_text(json.dumps({"samples": len(samples), "params": params,
                                  "seconds": round(time.time() - t0, 1), "history": hist},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
    return {"checkpoint": str(ckpt), "report": str(report), "params": params,
            "samples": len(samples), "history": hist}
