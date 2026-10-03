#!/usr/bin/env python3
"""plot_loss.py —— 训练 loss 曲线 PNG（本机运行，输入 loss_history.json）"""
import argparse
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("--hist", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
h = json.load(open(a.hist))
fig, ax1 = plt.subplots(figsize=(7, 4.2))
ep = list(range(len(h["train_loss"])))
ax1.plot(ep, h["train_loss"], color="#1f77b4", label="train Huber(delta/base)")
ax1.set_xlabel("epoch")
ax1.set_ylabel("train loss", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax2 = ax1.twinx()
ax2.plot(ep, h["val_nmae"], color="#d62728", label="val nMAE")
ax2.set_ylabel("val nMAE", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
best = h.get("best_epoch")
if best is not None and 0 <= best < len(ep):
    ax1.axvline(best, ls="--", c="gray", lw=1, label=f"best ep {best}")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)
ax1.set_title(f"LSTM training ({h.get('params', '?')} params, {h.get('total_minutes', '?')} min)")
fig.tight_layout()
fig.savefig(a.out, dpi=140)
print("saved", a.out)
