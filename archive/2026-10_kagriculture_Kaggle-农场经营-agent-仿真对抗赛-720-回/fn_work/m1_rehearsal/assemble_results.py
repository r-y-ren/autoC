#!/usr/bin/env python3
"""assemble_results.py —— 汇总远程评测原始结果 + 训练历史 + 语料 manifest → 最终结果 JSON（本机运行）

输入：
  --raw    远程回传的 results_raw.json（evaluate.py 产出）
  --hist   loss_history.json
  --prep   data/summary.json（prepare_data.py 产出）
  --ckmeta 训练配置（train_config 由 loss_history/ckpt 摘要代替）
  --out    输出 JSON 路径
"""
import argparse
import datetime
import json

ap = argparse.ArgumentParser()
ap.add_argument("--raw", required=True)
ap.add_argument("--hist", required=True)
ap.add_argument("--prep", required=True)
ap.add_argument("--wall-minutes", type=float, required=True, help="训练墙钟（远程日志读数）")
ap.add_argument("--out", required=True)
a = ap.parse_args()

raw = json.load(open(a.raw))
hist = json.load(open(a.hist))
prep = json.load(open(a.prep))

res = {
    "version": "m1-rehearsal/1.0",
    "_generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "task": "混合系 M1 预测器 BC 蒸馏可行性预演（dff20b-5 激进项 P5）：下一拍市场价格预测，纯研究，不碰产线/提交",
    "corpus": {
        "source": "fn_docs/hybrid/references/ext/fingerprint-scan/raw/ashok205-shards/（ashok205 top10 归档 parquet，58 件）",
        "episodes_total": prep.get("n_jobs"),
        "skipped_invalid": prep.get("skipped"),
        "split_by_episode": "md5(episode_id)%100 → 80/10/10，同局不跨集",
        "train_episodes": (prep.get("train") or {}).get("episodes"),
        "val_episodes": (prep.get("val") or {}).get("episodes"),
        "test_episodes": (prep.get("test") or {}).get("episodes"),
        "windows_per_episode": 704,
        "req_vs_inferred_committed_cell_match": prep.get("req_vs_committed"),
        "team_unique": prep.get("team_unique"),
        "team_top10_share_note": "对手分布=top10 语料非全体（限界，见报告）",
    },
    "task_definition": {
        "input": "16 拍公开状态窗口：9 品价格/库存偏差(−10000)/推断净成交量/城镇排水向量 + 商店数/双方金钱/时间相位（43 维）",
        "output": "t+1 拍 9 品价格（=预测 delta）",
        "target_metric": "MAE（价格单位）、nMAE=MAE/base、精确命中率、±1 命中率、方向命中率",
    },
    "methods": {
        "persistence": "delta_hat=0（下一拍价格=当前拍）",
        "lookup": "条件均值表 E[delta|品×库存桶8×排水态3×时段桶6]=1296 格，训练集拟合",
        "engine_prior": "inv_pred[t+1]=inv[t]−drain[t]（引擎结构先验，零成交假设），价格=训练集标定 inv→price 映射",
        "lstm": "2 层 LSTM(hidden 192)+MLP 头，%.0fK 参数，窗口 16，Huber(delta/base)，bf16" % (hist.get("params", 0) / 1000),
        "oracle_inv": "标定映射作用于真实 inv[t+1]（诊断行：完美库存下的价格恢复上界）",
    },
    "training": {
        "params": hist.get("params"),
        "epochs_run": len(hist.get("train_loss", [])),
        "best_epoch": hist.get("best_epoch"),
        "best_val_nmae": hist.get("best_val_nmae"),
        "wall_minutes_gpu_node": a.wall_minutes,
        "budget_minutes": 24,
        "loss_history": {"train_loss": hist.get("train_loss"), "val_nmae": hist.get("val_nmae"),
                          "val_mae": hist.get("val_mae"), "epoch_sec": hist.get("epoch_sec")},
    },
    "test_results": {
        "episodes": raw.get("test_episodes"),
        "windows": raw.get("windows"),
        "overall": raw.get("overall"),
        "per_product": raw.get("per_product"),
        "regime_nmae": raw.get("regime_nmae"),
        "big_move_cells": raw.get("big_move_cells"),
        "wheat_focus": raw.get("wheat_focus"),
        "significance_block_bootstrap_2000": raw.get("significance_block_bootstrap_2000"),
        "failure_cases": raw.get("failure_cases"),
    },
    "verdict_inputs": {
        "lstm_beats_persistence": raw["significance_block_bootstrap_2000"]["lstm_vs_persistence"]["better"],
        "lstm_beats_lookup": raw["significance_block_bootstrap_2000"]["lstm_vs_lookup"]["better"],
        "lstm_beats_engine_prior_mae": raw["overall"]["lstm"]["mae"] < raw["overall"]["engine_prior"]["mae"],
    },
}
with open(a.out, "w") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
print("assembled ->", a.out)
print(json.dumps(res["verdict_inputs"], indent=1))
