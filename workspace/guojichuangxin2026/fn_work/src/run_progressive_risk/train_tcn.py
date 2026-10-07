"""离线训练管线：样本生成（按架次分组防泄漏）→轻量 TCN checkpoint（run_progressive_risk 块）。"""
from __future__ import annotations


class TrainError(Exception):
    """数据不足/标注缺失。"""


def _load_run(data_dir: str):  # 支持 runs/ 与 fn_docs/results/ 两种布局（同为 manifest+frames）
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


class _LinearProbe:
    """稀疏事件线性探针（arxiv-2609.39386 实证路线）：窗口统计特征→危险概率+分位数平均。"""

    def __init__(self, w, b, feats_summary, quantiles, feature_names):
        self.w, self.b, self.fs = w, b, feats_summary
        self.quantiles, self.feature_names = quantiles, feature_names

    def __call__(self, x):
        """x: [T,F] 或 [1,T,F]（与 predict_risk_tcn 同接口）→ 同构输出 dict。"""
        import math

        import numpy as np
        import torch
        xa = np.asarray(x, dtype=float)
        if xa.ndim == 3:
            xa = xa[0]
        s, _ = _window_summary(xa)                       # [3F] 末值/均值/斜率
        logit = float((np.asarray(self.w).reshape(1, -1) @ np.nan_to_num(s) + self.b)[0])
        p5 = 1.0 / (1.0 + math.exp(-logit))
        probs = {h: max(0.0, min(1.0, p5 * self.quantiles.get(h, 1.0)))
                 for h in ("1", "3", "5", "10")}
        return {"probs": probs,
                "time_to_unsafe_s": max(0.0, min(60.0, (0.5 - p5) * 30.0)),
                "raw": {"probs": torch.full((1, 4), float(p5))}}

    def state_dict(self):
        import numpy as np
        return {"w": self.w.tolist() if hasattr(self.w, "tolist") else list(self.w),
                "b": float(self.b) if not hasattr(self.b, "tolist") else self.b.tolist(),
                "fs": self.fs, "quantiles": self.quantiles,
                "feature_names": self.feature_names, "kind": "probe"}


def _probe_fit(X, y):
    """最小二乘+岭正则拟合探针；X: [N, 3F] 统计摘要；y: 0/1。"""
    import numpy as np
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    Xd = np.nan_to_num(X, nan=0.0)
    Xb = np.hstack([Xd, np.ones((len(Xd), 1))])
    lam = 1.0
    A = Xb.T @ Xb + lam * np.eye(Xb.shape[1])
    w_full = np.linalg.solve(A, Xb.T @ y)
    return w_full[:-1], w_full[-1]


def _window_summary(win):
    """[T,F]→[3F] 末值/均值/斜率（NaN 置列中位）。"""
    import numpy as np
    w = np.asarray(win, dtype=float)
    out = []
    for i in range(w.shape[1]):
        v = w[:, i]
        fill = float(np.nanmedian(v)) if np.isfinite(v).any() else 0.0
        v = np.nan_to_num(v, nan=fill)
        out += [v[-1], v.mean(), v[-1] - v[0]]
    return np.asarray(out), [float(np.nanmedian(w[:, i])) if np.isfinite(w[:, i]).any() else 0.0
                             for i in range(w.shape[1])]


def _sparse_recall(preds, ys):
    """稀疏事件召回口径：p>0.5 报警的正样本占比（误报并报，选优用）。"""
    hit = sum(1 for p, y in zip(preds, ys) if y > 0.5 and p > 0.5)
    n_pos = sum(1 for y in ys if y > 0.5) or 1
    return hit / n_pos


def train_tcn(data_dirs: list, train_config: dict) -> dict:
    """小数据快速训练（默认 3 epoch CPU 可跑）；产 checkpoint+元数据+验证报告。"""
    import json
    import math
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
    # R17：线性探针基线并跑（arxiv-2609.39386 实证路线）——按稀疏事件召回选优
    import numpy as np
    probe_ckpt = out_dir / "probe.pkl"
    probe_note = "skipped"
    best_kind, best_art = "tcn", {"path": str(ckpt), "kind": "tcn"}
    try:
        from run_progressive_risk.build_feature_window import FEATURE_NAMES
        Xtr, ytr, Xva, yva = [], [], [], []
        raw_va = []
        for x, y, g in samples:
            s, fills = _window_summary(x)
            (Xva if g in val_g else Xtr).append(s)
            (yva if g in val_g else ytr).append(y)
            if g in val_g:
                raw_va.append(x)
        if len(Xtr) >= 4:
            w, b = _probe_fit(Xtr, ytr)
            probe = _LinearProbe(np.asarray(w), float(b), {"fill": fills},
                                 {"1": 1.15, "3": 1.05, "5": 1.0, "10": 0.85},
                                 FEATURE_NAMES)
            import pickle
            with open(probe_ckpt, "wb") as fh:
                pickle.dump({"probe": probe.state_dict(), "version": f"probe-{int(time.time())}",
                             "feature_names": FEATURE_NAMES, "kind": "probe"}, fh)
            pv = [float(probe(xw)["probs"]["5"]) for xw in raw_va]   # 原始窗评估（摘要已在内部）
            probe_recall = _sparse_recall(pv, yva)
            tc_logits = hist[-1].get("val_acc_5s") or 0.0
            probe_note = f"probe_recall={probe_recall:.3f} tcn_val_acc={tc_logits:.3f}"
            if probe_recall >= tc_logits:
                best_kind, best_art = "probe", {"path": str(probe_ckpt), "kind": "probe"}
            comparison = {"probe_recall": round(probe_recall, 3),
                          "tcn_val_acc": round(tc_logits, 3), "winner": best_kind}
        else:
            comparison = {"winner": "tcn", "note": "val 不足探针跳过"}
    except Exception as exc:
        comparison = {"winner": "tcn", "probe_error": str(exc)}

    report = out_dir / "train_report.json"
    report.write_text(json.dumps({"samples": len(samples), "params": params,
                                  "seconds": round(time.time() - t0, 1), "history": hist,
                                  "selection": comparison},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
    return {"checkpoint": str(ckpt), "report": str(report), "params": params,
            "samples": len(samples), "history": hist, "selection": comparison,
            "best": best_art}
