#!/usr/bin/env python3
"""evaluate.py —— M1 预演评测：test 集三对照（persistence / 查表 / LSTM）+ 引擎先验 + 完美库存 oracle

方法：
  persistence : delta_hat = 0（下一拍价格 = 当前拍）
  lookup      : 条件均值表 E[delta | 品×库存桶×排水态×时段]，训练集拟合（含确定性排水结构的分桶知识）
  engine_prior: inv_pred[t+1] = inv[t] - drain[t]（引擎结构先验，零成交假设），价格用训练集标定的 inv→price 映射
                （回放 1.32.2 与本地 1.32.7 引擎在 hinge 品有版本差，故标定而非硬编码公式）
  lstm        : 训练好的序列模型
  oracle_inv  : 标定映射作用于真实 inv[t+1]（诊断行：库存已知时价格可精确恢复的程度）

主指标：MAE（价格单位，等价于 |delta_hat - delta_true| 均值）、nMAE=MAE/base、精确命中率（取整后相等）、
       ±1 命中率、方向命中率（|delta_true|≥1 的格子）。

用法（远程 WSL）：
  python evaluate.py --data <dir> --runs runs --out results_raw.json
"""
import argparse
import json
import os

import numpy as np
import torch

from train_model import (BASE, PRODS, T_PARAM, FEAT_DIM, N_STEPS, T0, T1, WIN,
                         PriceLSTM, build_feats, deltas, load_split)

INV_CUTS = np.array([-1e9, -1.0, -0.5, -0.1, 0.0, 0.1, 0.5, 1.0, 1e9])


def method_metrics(delta_hat, delta_true, base):
    err = delta_hat - delta_true
    ae = np.abs(err)
    mae = float(ae.mean())
    nmae = float((ae / base).mean())
    exact = float((np.rint(delta_hat).astype(np.int32) == np.rint(delta_true).astype(np.int32)).mean())
    within1 = float((ae <= 1.0).mean())
    m = np.abs(delta_true) >= 1.0
    diracc = float((np.sign(delta_hat[m]) == np.sign(delta_true[m])).mean()) if m.any() else None
    return {"mae": round(mae, 4), "nmae": round(nmae, 5), "exact": round(exact, 4),
            "within1": round(within1, 4), "dir_acc": round(diracc, 4) if diracc is not None else None}


def per_product(delta_hat, delta_true, base):
    out = {}
    ae = np.abs(delta_hat - delta_true)
    for j, p in enumerate(PRODS):
        out[p] = {"mae": round(float(ae[..., j].mean()), 4),
                  "nmae": round(float(ae[..., j].mean() / base[j]), 5),
                  "exact": round(float((np.rint(delta_hat[..., j]) == np.rint(delta_true[..., j])).mean()), 4)}
    return out


def fit_lookup(tr, rng, max_cells=6_000_000):
    """查表基线：key=(品, 库存桶, 排水态, 时段桶) → 训练集条件均值 delta。"""
    iv = tr["inv_dev"][:, T0:T1 + 1].astype(np.float32) / T_PARAM   # (n,704,9)
    bucket = np.digitize(iv, INV_CUTS[1:-1])                         # (n,704,9) 0..7
    t_ax = np.arange(T0, T1 + 1)
    phase = np.broadcast_to((t_ax // 120)[None, :, None], bucket.shape)
    dr = tr["drain"][:, T0:T1 + 1].sum(axis=2)                       # (n,704)
    dfl = np.where(dr >= 2, 2, np.where(dr >= 1, 1, 0))[:, :, None]
    delta = (tr["prices"][:, T0 + 1:T1 + 2].astype(np.float32)
             - tr["prices"][:, T0:T1 + 1].astype(np.float32))        # (n,704,9)
    n = delta.shape[0]
    sel = np.arange(n)
    if n * 704 > 6_000_000:
        sel = rng.choice(n, size=6_000_000 // 704, replace=False)
    b = bucket[sel].astype(np.int32)
    ph = phase[sel][:, :, :1].astype(np.int32)
    df = dfl[sel].astype(np.int32)
    pidx = np.arange(9, dtype=np.int32)[None, None, :]
    key = (pidx * (8 * 6 * 3) + b * (6 * 3) + ph * 3 + df).reshape(-1).astype(np.int64)
    val = delta[sel].reshape(-1)
    K = 9 * 8 * 6 * 3
    s = np.bincount(key, weights=val, minlength=K)
    c = np.bincount(key, minlength=K)
    tbl = np.zeros(K, dtype=np.float32)
    nz = c > 0
    tbl[nz] = s[nz] / c[nz]
    return tbl


def apply_lookup(tbl, te):
    iv = te["inv_dev"][:, T0:T1 + 1].astype(np.float32) / T_PARAM
    bucket = np.digitize(iv, INV_CUTS[1:-1])
    t_ax = np.arange(T0, T1 + 1)
    phase = np.broadcast_to(t_ax // 120, bucket.shape[:1] + (704,))[:, :, None]
    dr = te["drain"][:, T0:T1 + 1].sum(axis=2)
    dfl = np.where(dr >= 2, 2, np.where(dr >= 1, 1, 0))[:, :, None]
    pidx = np.arange(9)[None, None, :]
    key = ((pidx * 8 * 6 * 3) + bucket * 6 * 3 + phase * 3 + dfl).astype(np.int64)
    return tbl[key]


def fit_inv_price_map(tr):
    """训练集标定 inv→price 精确映射（引擎确定性定价的版本鲁棒恢复）。"""
    maps = {}
    inv = (tr["inv_dev"].astype(np.int32) + 10000).reshape(-1, 9)
    pr = tr["prices"].astype(np.int32).reshape(-1, 9)
    for j in range(9):
        order = np.argsort(inv[:, j], kind="stable")
        vi, pi = inv[:, j][order], pr[:, j][order]
        # 同 inv 多 price（版本差/取整边界）→ 取众数
        uniq, start = np.unique(vi, return_index=True)
        mp = np.full(22001, -1, dtype=np.int32)
        for k in range(len(uniq)):
            seg = pi[start[k]:start[k + 1] if k + 1 < len(uniq) else None]
            vals, cnts = np.unique(seg, return_counts=True)
            mp[uniq[k]] = vals[np.argmax(cnts)]
        # 前向/后向填充未见 inv
        idx = np.arange(22001)
        known = mp >= 0
        mp = np.where(known, mp, np.interp(idx, idx[known], mp[known])).astype(np.int32)
        maps[j] = np.clip(mp, 1, None)
    return maps


def apply_map(maps, inv_abs):
    out = np.empty_like(inv_abs, dtype=np.float32)
    for j in range(9):
        v = np.clip(inv_abs[..., j], 0, 22000)
        out[..., j] = maps[j][v]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(7)
    dev = "cuda" if torch.cuda.is_available() else "cpu"

    te = load_split(args.data, "test")
    tr = load_split(args.data, "train")
    n_te = te["prices"].shape[0]
    print("test episodes:", n_te, "train episodes:", tr["prices"].shape[0], flush=True)

    delta_true = (te["prices"][:, T0 + 1:T1 + 2].astype(np.float32)
                  - te["prices"][:, T0:T1 + 1].astype(np.float32))  # (n,704,9)

    # ---- LSTM preds
    stats = json.load(open(os.path.join(args.runs, "norm_stats.json")))
    ck = torch.load(os.path.join(args.runs, "ckpt_best.pt"), map_location=dev, weights_only=False)
    model = PriceLSTM().to(dev)
    model.load_state_dict(ck["state_dict"])
    model.eval()
    teX, _ = build_feats(te, stats)
    teX_t = torch.from_numpy(teX).to(dev)
    off = torch.arange(-WIN + 1, 1, device=dev)
    nw = T1 - T0 + 1
    preds = np.empty((n_te, nw, 9), dtype=np.float32)
    with torch.no_grad():
        for e in range(n_te):
            t_idx = torch.arange(T0, T1 + 1, device=dev)
            ep = torch.full((nw,), e, device=dev, dtype=torch.int64)
            for i in range(0, nw, 8192):
                t = t_idx[i:i + 8192]
                idx = t.unsqueeze(1) + off.unsqueeze(0)
                x = teX_t[ep[i:i + 8192].unsqueeze(1), idx].float()
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    pr = model(x).float()
                preds[e, i:i + 8192] = pr.cpu().numpy()
            if (e + 1) % 500 == 0:
                print(f"  lstm eval {e + 1}/{n_te}", flush=True)

    # ---- baselines
    pers = np.zeros_like(delta_true)
    tbl = fit_lookup(tr, rng)
    look = apply_lookup(tbl, te)
    maps = fit_inv_price_map(tr)
    inv_t = te["inv_dev"][:, T0:T1 + 1].astype(np.int32) + 10000
    drain_t = te["drain"][:, T0:T1 + 1].astype(np.int32)
    price_t = te["prices"][:, T0:T1 + 1].astype(np.float32)
    inv_next_true = te["inv_dev"][:, T0 + 1:T1 + 2].astype(np.int32) + 10000
    eng = apply_map(maps, inv_t - drain_t) - price_t
    oracle = apply_map(maps, inv_next_true) - price_t

    methods = {"persistence": pers, "lookup": look, "engine_prior": eng, "lstm": preds, "oracle_inv": oracle}
    base = BASE
    res = {"test_episodes": n_te, "windows": int(delta_true.size / 9),
           "overall": {}, "per_product": {}, "configs": {"ckpt_epoch": ck.get("epoch"), "params": ck.get("params")}}
    for name, dh in methods.items():
        res["overall"][name] = method_metrics(dh, delta_true, base)
        res["per_product"][name] = per_product(dh, delta_true, base)
        print(name, res["overall"][name], flush=True)

    # ---- regime 拆解（库存体制，nMAE 口径）
    x_reg = te["inv_dev"][:, T0:T1 + 1].astype(np.float32) / T_PARAM
    base_b = base[None, None, :]
    regimes = {"deep_short(<-1T)": x_reg < -1, "short[-1T,0)": (x_reg >= -1) & (x_reg < 0),
               "normal[0,T)": (x_reg >= 0) & (x_reg < 1), "glut[1T,2T)": (x_reg >= 1) & (x_reg < 2),
               "heavy_glut(>=2T)": x_reg >= 2}
    res["regime_nmae"] = {}
    for rname, mask3 in regimes.items():
        row = {}
        for name, dh in methods.items():
            ae = np.abs(dh - delta_true) / base_b
            row[name] = round(float(ae[mask3].mean()), 5) if mask3.any() else None
        res["regime_nmae"][rname] = {"cells": int(mask3.sum()), **row}

    # ---- 大变动格（|delta_true|>=5）
    big = np.abs(delta_true) >= 5
    res["big_move_cells"] = {"cells": int(big.sum())}
    for name, dh in methods.items():
        ae = np.abs(dh - delta_true)
        res["big_move_cells"][name] = {"mae": round(float(ae[big].mean()), 3)}

    # ---- 失败案例：LSTM 误差 top3 + 每品 top1
    err = np.abs(preds - delta_true)
    flat = err.reshape(-1)
    top = np.argpartition(flat, -3)[-3:]
    top = top[np.argsort(-flat[top])]
    cases = []
    n_ep = n_te
    for fidx in top:
        e = int(fidx // (704 * 9)); rem = fidx % (704 * 9); t = int(rem // 9) + T0; j = int(rem % 9)
        w0 = max(0, t - WIN + 1)
        cases.append({
            "episode_test_idx": e, "t": t, "product": PRODS[j],
            "err_ltm": round(float(err[e, t - T0, j]), 2),
            "window_prices": te["prices"][e, w0:t + 1, j].tolist(),
            "true_next_price": int(te["prices"][e, t + 1, j]), "price_t": int(te["prices"][e, t, j]),
            "inv_dev_t": int(te["inv_dev"][e, t, j]), "net_comm_recent": te["net_comm"][e, max(0, t - 5):t + 1, j].tolist(),
            "drain_t": int(te["drain"][e, t, j]),
            "delta_true": float(delta_true[e, t - T0, j]),
            "delta_pred": {"persistence": 0.0, "lookup": float(look[e, t - T0, j]),
                           "engine_prior": float(eng[e, t - T0, j]), "lstm": float(preds[e, t - T0, j])},
        })
    res["failure_cases"] = cases

    # WHEAT 专项（备选任务=对手麦流强度的代理读数）
    jw = PRODS.index("WHEAT")
    res["wheat_focus"] = {"overall": {n: method_metrics(dh[..., jw:jw + 1], delta_true[..., jw:jw + 1], base[jw:jw + 1]) for n, dh in methods.items()},
                          "big_move_mae": {n: round(float(np.abs(dh[..., jw] - delta_true[..., jw])[np.abs(delta_true[..., jw]) >= 5].mean()), 3)
                                           if (np.abs(delta_true[..., jw]) >= 5).any() else None for n, dh in methods.items()}}

    # ---- 配对显著性：LSTM/查表/引擎先验 vs persistence，MAE 差的逐局块 bootstrap 95% CI
    def ep_mean_ae(dh):
        return np.abs(dh - delta_true).mean(axis=(1, 2))   # (n_ep,)
    pers_e = ep_mean_ae(pers)
    sig = {}
    for name in ("lookup", "engine_prior", "lstm"):
        d = ep_mean_ae(methods[name]) - pers_e              # 负 = 优于 persistence
        boots = []
        for _ in range(2000):
            idx = rng.integers(0, len(d), len(d))
            boots.append(d[idx].mean())
        lo, hi = np.percentile(boots, [2.5, 97.5])
        sig[name + "_vs_persistence"] = {"mean_diff": round(float(d.mean()), 5),
                                         "ci95": [round(float(lo), 5), round(float(hi), 5)],
                                         "better": bool(hi < 0)}
    d = ep_mean_ae(preds) - ep_mean_ae(look)
    boots = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    sig["lstm_vs_lookup"] = {"mean_diff": round(float(d.mean()), 5),
                             "ci95": [round(float(lo), 5), round(float(hi), 5)],
                             "better": bool(hi < 0)}
    res["significance_block_bootstrap_2000"] = sig

    with open(args.out, "w") as f:
        json.dump(res, f, indent=1)
    print("EVAL DONE ->", args.out, flush=True)


if __name__ == "__main__":
    main()
