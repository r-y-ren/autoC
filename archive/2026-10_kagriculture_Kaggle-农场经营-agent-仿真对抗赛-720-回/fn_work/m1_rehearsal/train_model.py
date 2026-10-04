#!/usr/bin/env python3
"""train_model.py —— M1 预演：下一拍市场价格预测，LSTM 2 层序列模型（torch CUDA）

输入窗口 16 拍 × 43 维公开状态（价格/库存偏差/推断净成交量/城镇排水/时间/金钱），预测 t+1 拍 9 品价格增量。
损失：Huber(delta / base_p)（按品基准价归一，防大价品主导）。
预算：默认 24 分钟墙钟 + early stop（val nMAE, patience 6）。
产物：runs/ckpt_best.pt, runs/loss_history.json, runs/norm_stats.json, runs/train_config.json

用法（远程 WSL, kag_eval_venv）：
  python train_model.py --data <dir with {split}_*.npy> --out runs
"""
import argparse
import json
import math
import os
import time

import numpy as np
import torch
import torch.nn as nn

PRODS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], dtype=np.float32)
T_PARAM = np.array([400, 450, 200, 100, 300, 332, 122, 105, 200], dtype=np.float32)
N_STEPS = 720
WIN = 16
T0 = WIN - 1          # 首个可预测 t
T1 = N_STEPS - 2      # 最后可预测 t（目标 t+1 ≤ 719）
FEAT_DIM = 9 * 4 + 3 + 4


def load_split(data_dir, split):
    a = {}
    for name in ("prices", "inv_dev", "net_comm", "drain", "shops_n", "money"):
        a[name] = np.load(os.path.join(data_dir, f"{split}_{name}.npy"))
    return a


def build_feats(a, stats=None):
    """(n,720,F) float32 特征；stats 为 None 时返回待拟合的原始堆叠用于统计。"""
    n = a["prices"].shape[0]
    t_axis = np.arange(N_STEPS, dtype=np.float32)
    hour = t_axis % 24.0
    feats = np.zeros((n, N_STEPS, FEAT_DIM), dtype=np.float32)
    c = 0
    raws = {}
    for name in ("prices", "inv_dev", "net_comm", "drain"):
        x = a[name].astype(np.float32)
        if name == "net_comm":
            x = np.clip(x, -200, 200)
        raws[name] = x
        feats[:, :, c:c + 9] = x
        c += 9
    feats[:, :, c] = a["shops_n"].astype(np.float32); c += 1
    feats[:, :, c] = np.clip(a["money"][:, :, 0], 0, 200000) / 1000.0; c += 1
    feats[:, :, c] = np.clip(a["money"][:, :, 1], 0, 200000) / 1000.0; c += 1
    feats[:, :, c] = np.sin(2 * math.pi * hour / 24.0); c += 1
    feats[:, :, c] = np.cos(2 * math.pi * hour / 24.0); c += 1
    feats[:, :, c] = np.sin(2 * math.pi * t_axis / N_STEPS); c += 1
    feats[:, :, c] = np.cos(2 * math.pi * t_axis / N_STEPS); c += 1
    assert c == FEAT_DIM, c
    if stats is None:
        flat = feats.reshape(-1, FEAT_DIM)
        mu = flat.mean(axis=0).astype(np.float32)
        sd = flat.std(axis=0).astype(np.float32)
        sd[sd < 1e-6] = 1.0
        stats = {"mean": mu.tolist(), "std": sd.tolist()}
        return stats
    mu = np.array(stats["mean"], dtype=np.float32)
    sd = np.array(stats["std"], dtype=np.float32)
    feats = (feats - mu) / sd
    return feats.astype(np.float16), stats


def deltas(a):
    """(n,720,9) float32: delta[t] = price[t] - price[t-1]（delta[0]=0）。"""
    p = a["prices"].astype(np.float32)
    d = np.zeros_like(p)
    d[:, 1:, :] = p[:, 1:, :] - p[:, :-1, :]
    return d


class PriceLSTM(nn.Module):
    def __init__(self, in_dim=FEAT_DIM, hidden=192, layers=2, p_drop=0.1):
        super().__init__()
        self.lstm = nn.LSTM(in_dim, hidden, num_layers=layers, batch_first=True,
                            dropout=p_drop if layers > 1 else 0.0)
        self.norm = nn.LayerNorm(hidden)
        self.head = nn.Sequential(nn.Linear(hidden, 96), nn.ReLU(), nn.Linear(96, 9))

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(self.norm(out[:, -1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=int, default=80)
    ap.add_argument("--max-minutes", type=float, default=24.0)
    ap.add_argument("--samples-per-epoch", type=int, default=500_000)
    ap.add_argument("--batch", type=int, default=1024)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--patience", type=int, default=6)
    ap.add_argument("--seed", type=int, default=17)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.backends.cudnn.benchmark = True
    print("device:", dev, flush=True)

    tr = load_split(args.data, "train")
    va = load_split(args.data, "val")
    stats = build_feats(tr)          # 先拟合并保存
    with open(os.path.join(args.out, "norm_stats.json"), "w") as f:
        json.dump(stats, f)
    trX, _ = build_feats(tr, stats)
    vaX, _ = build_feats(va, stats)
    trD = deltas(tr)
    vaD = deltas(va)
    base = torch.tensor(BASE, device=dev)

    trX_t = torch.from_numpy(trX).to(dev)
    vaX_t = torch.from_numpy(vaX).to(dev)
    # 目标 = delta[t+1] = price[t+1]-price[t]；切片取索引 T0+1..T1+1，窗口末拍 t 与目标按 t-T0 对齐
    trD_t = torch.from_numpy(trD[:, T0 + 1:T1 + 2].astype(np.float32)).to(dev)
    vaD_t = torch.from_numpy(vaD[:, T0 + 1:T1 + 2].astype(np.float32)).to(dev)
    n_tr, n_va = trX_t.shape[0], vaX_t.shape[0]
    nw = T1 - T0 + 1
    print(f"train eps={n_tr} val eps={n_va} windows/ep={nw}", flush=True)

    # 全窗口索引（train 用随机子采样；val 用固定子采样 20 万）
    rng = np.random.default_rng(args.seed)
    val_sel = rng.choice(n_va * nw, size=min(200_000, n_va * nw), replace=False)
    val_ep = torch.from_numpy((val_sel // nw).astype(np.int64)).to(dev)
    val_t = torch.from_numpy((val_sel % nw + T0).astype(np.int64)).to(dev)

    model = PriceLSTM().to(dev)
    n_par = sum(p.numel() for p in model.parameters())
    print(f"model params: {n_par}", flush=True)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
    lossf = nn.SmoothL1Loss()

    off = torch.arange(-WIN + 1, 1, device=dev)

    def gather(X, ep, t):
        idx = t.unsqueeze(1) + off.unsqueeze(0)          # (B,16)
        return X[ep.unsqueeze(1), idx].float()

    hist = {"train_loss": [], "val_nmae": [], "val_mae": [], "epoch_sec": [], "params": n_par}
    best = float("inf")
    best_ep = -1
    t_start = time.time()
    stop = False
    for ep in range(args.epochs):
        model.train()
        sel = rng.choice(n_tr * nw, size=min(args.samples_per_epoch, n_tr * nw), replace=False)
        ep_idx = torch.from_numpy((sel // nw).astype(np.int64)).to(dev)
        t_idx = torch.from_numpy((sel % nw + T0).astype(np.int64)).to(dev)
        perm = torch.randperm(len(sel), device=dev)
        tot = 0.0
        nb = 0
        t_ep = time.time()
        for i in range(0, len(sel), args.batch):
            b = perm[i:i + args.batch]
            e, t = ep_idx[b], t_idx[b]
            x = gather(trX_t, e, t)
            y = trD_t[e, t - T0] / base
            with torch.autocast("cuda", dtype=torch.bfloat16):
                pred = model(x)
                loss = lossf(pred.float(), y)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            tot += loss.item()
            nb += 1
        sched.step()

        model.eval()
        errs = []
        with torch.no_grad():
            for i in range(0, len(val_ep), 8192):
                e, t = val_ep[i:i + 8192], val_t[i:i + 8192]
                x = gather(vaX_t, e, t)
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    pred = model(x).float()
                dn = (pred - vaD_t[e, t - T0] / base).abs()   # normalized abs err
                errs.append(dn.view(-1, 9))
        dn_all = torch.cat(errs)
        val_nmae = dn_all.mean().item()
        val_mae = (dn_all * base).mean().item()
        sec = time.time() - t_ep
        hist["train_loss"].append(tot / max(nb, 1))
        hist["val_nmae"].append(val_nmae)
        hist["val_mae"].append(val_mae)
        hist["epoch_sec"].append(round(sec, 2))
        marker = ""
        if val_nmae < best - 1e-6:
            best = val_nmae
            best_ep = ep
            torch.save({"state_dict": model.state_dict(), "config": vars(args), "epoch": ep,
                        "val_nmae": val_nmae, "params": n_par},
                       os.path.join(args.out, "ckpt_best.pt"))
            marker = " *"
        print(f"epoch {ep:02d} train_loss={tot/max(nb,1):.5f} val_nMAE={val_nmae:.5f} "
              f"val_MAE={val_mae:.3f} ({sec:.0f}s){marker}", flush=True)
        with open(os.path.join(args.out, "loss_history.json"), "w") as f:
            json.dump(hist, f)
        elapsed = (time.time() - t_start) / 60.0
        if elapsed > args.max_minutes:
            print(f"time budget reached ({elapsed:.1f} min), stop", flush=True)
            stop = True
        if ep - best_ep >= args.patience:
            print(f"early stop (no val improvement for {args.patience} epochs)", flush=True)
            stop = True
        if stop:
            break
    hist["best_epoch"] = best_ep
    hist["best_val_nmae"] = best
    hist["total_minutes"] = round((time.time() - t_start) / 60.0, 2)
    with open(os.path.join(args.out, "loss_history.json"), "w") as f:
        json.dump(hist, f)
    print("TRAIN DONE best_ep", best_ep, "val_nMAE", round(best, 5),
          "minutes", hist["total_minutes"], flush=True)


if __name__ == "__main__":
    main()
