# -*- coding: utf-8 -*-
"""Track-C (BC) M1-1: 监督训练首跑（跑通优先于调优）.

两个解耦小 MLP（numpy 训练侧；推理侧导出纯 Python 权重）：
  unit-net:   x = G(167) + U(14) + is_farmer(1) -> 128 tanh -> 64 tanh
              -> heads: op(18) / arg(12) / qty(14)
  market-net: x = G(167) + slot_onehot(10)      -> 128 tanh -> 64 tanh
              -> heads: op(7) / item(12) / qty(14)

损失：逐头交叉熵 + 条件掩码（arg 头只在 PLANT/PICKUP/PLACE 计损；
qty 头只在 PICKUP/PLACE；市场 item/qty 只在数量型订单）+ 类别权重
（市场 NONE 槽降权，防退化解）。

数据切分：game 级确定性 held-out（md5(game_key) 十六进制首 8 位 % 100
< HOLDOUT_PCT），held-out 局两席都不进训练——bc_eval 用它们做反事实。

输出：
  bc_track/models/bc_model_v1.py        量化权重硬编码（int8 + per-layer scale）
  bc_track/data/split.json              训练/评估局切分（可复现）
  bc_track/models/train_report.json     逐头准确率（train / held-out）
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bc_schema as S                                     # noqa: E402

SOFTWARE = Path(__file__).resolve().parents[2]
DATA = SOFTWARE / "bc_track" / "data"
MODELS = SOFTWARE / "bc_track" / "models"
HOLDOUT_PCT = 8                     # game 级 held-out 百分比（约 13 局）
SEED = 20260920
UNIT_HIDDEN = (128, 64)
MARKET_HIDDEN = (128, 64)
ARG_OPS = {S.UNIT_OP_IDX["PLANT"], S.UNIT_OP_IDX["PICKUP"],
           S.UNIT_OP_IDX["PLACE"]}
QTY_OPS = {S.UNIT_OP_IDX["PICKUP"], S.UNIT_OP_IDX["PLACE"]}
MKT_QTY_OPS = {S.MARKET_OP_IDX["BUY_SEED"], S.MARKET_OP_IDX["BUY_PRODUCT"],
               S.MARKET_OP_IDX["BUY_ANIMAL"], S.MARKET_OP_IDX["SELL"]}
MKT_ITEM_OPS = MKT_QTY_OPS
NONE_W = 0.15                       # 市场 NONE 槽 CE 权重


def game_holdout(game_key: str) -> bool:
    h = hashlib.md5(game_key.encode()).hexdigest()[:8]
    return int(h, 16) % 100 < HOLDOUT_PCT


# --------------------------------------------------------------------------
# 数据装载
# --------------------------------------------------------------------------
def load_datasets():
    manifest = json.loads((DATA / "corpus_manifest.json")
                          .read_text(encoding="utf-8"))
    ux, uop, uarg, uqty = [], [], [], []
    mx, mop, mitem, mqty = [], [], [], []
    train_keys, held_keys = set(), set()
    n_seats_train = n_seats_held = 0
    for seat in manifest["seats"]:
        gkey = f"{seat['source']}:{seat['episode']}"
        held = game_holdout(gkey)
        (held_keys if held else train_keys).add(gkey)
        if held:
            n_seats_held += 1
            continue
        n_seats_train += 1
        path = DATA / "samples" / seat["file"]
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            payload = json.load(handle)
        for turn in payload["turns"]:
            g = turn["g"]
            for is_farmer, uf, act in turn["units"]:
                ux.append(g + uf + [1.0 if is_farmer else 0.0])
                uop.append(act[0]); uarg.append(act[1]); uqty.append(act[2])
            for slot_i, (op_i, item_i, qty_b) in enumerate(turn["market"]):
                oh = [0.0] * S.N_MARKET_SLOTS
                oh[slot_i] = 1.0
                mx.append(g + oh)
                mop.append(op_i); mitem.append(item_i); mqty.append(qty_b)
    to_np = lambda xs: np.asarray(xs, dtype=np.float32)    # noqa: E731
    i32 = lambda xs: np.asarray(xs, dtype=np.int64)        # noqa: E731
    unit = {"x": to_np(ux), "op": i32(uop), "arg": i32(uarg), "qty": i32(uqty)}
    mkt = {"x": to_np(mx), "op": i32(mop), "item": i32(mitem),
           "qty": i32(mqty)}
    return unit, mkt, sorted(train_keys), sorted(held_keys), \
        (n_seats_train, n_seats_held)


def load_heldout_reference():
    """held-out 局上专家（真值）样本——供 held-out 准确率对照。"""
    manifest = json.loads((DATA / "corpus_manifest.json")
                          .read_text(encoding="utf-8"))
    ux, uop = [], []
    mx, mop = [], []
    for seat in manifest["seats"]:
        gkey = f"{seat['source']}:{seat['episode']}"
        if not game_holdout(gkey):
            continue
        with gzip.open(DATA / "samples" / seat["file"], "rt",
                       encoding="utf-8") as handle:
            payload = json.load(handle)
        for turn in payload["turns"]:
            for is_farmer, uf, act in turn["units"]:
                ux.append(turn["g"] + uf + [1.0 if is_farmer else 0.0])
                uop.append(act[0])
            for slot_i, (op_i, *_rest) in enumerate(turn["market"]):
                oh = [0.0] * S.N_MARKET_SLOTS
                oh[slot_i] = 1.0
                mx.append(turn["g"] + oh)
                mop.append(op_i)
    to_np = lambda xs: np.asarray(xs, dtype=np.float32)    # noqa: E731
    return (to_np(ux), np.asarray(uop, dtype=np.int64),
            to_np(mx), np.asarray(mop, dtype=np.int64))


# --------------------------------------------------------------------------
# 模型（numpy，供训练；导出格式与 bc_policy 的纯 Python 前向一致）
# --------------------------------------------------------------------------
class MLP:
    """两隐层 tanh + 多 softmax 头。W/b 逐层；heads = {name: (W, b)}。"""

    def __init__(self, n_in: int, hidden, heads: dict[str, int], rng):
        sizes = [n_in, *hidden]
        self.W, self.b = [], []
        for a, c in zip(sizes, sizes[1:]):
            self.W.append(rng.normal(0, (2.0 / a) ** 0.5, (a, c))
                          .astype(np.float32))
            self.b.append(np.zeros(c, dtype=np.float32))
        last = hidden[-1]
        self.heads = {name: (rng.normal(0, (1.0 / last) ** 0.5,
                                     (last, n)).astype(np.float32),
                              np.zeros(n, dtype=np.float32))
                      for name, n in heads.items()}

    def forward(self, x):
        acts = [x]
        for w, b in zip(self.W, self.b):
            acts.append(np.tanh(acts[-1] @ w + b))
        h = acts[-1]
        outs = {name: h @ w + b for name, (w, b) in self.heads.items()}
        return outs, acts

    def loss_and_grads(self, x, targets: dict, masks: dict, weights: dict):
        """逐头 CE（带掩码/权重）。返回 (loss, grads dict)。acts[0]=x。"""
        outs, acts = self.forward(x)
        n = x.shape[0]
        idx = np.arange(n)
        loss = 0.0
        gw = [np.zeros_like(w) for w in self.W]
        gb = [np.zeros_like(b) for b in self.b]
        gheads = {k: (np.zeros_like(w), np.zeros_like(b))
                  for k, (w, b) in self.heads.items()}
        dh_total = np.zeros_like(acts[-1])
        for name, logits in outs.items():
            y = targets[name]
            m = masks.get(name)
            w_cls = weights.get(name)
            if m is not None and not m.any():
                continue
            z = logits - logits.max(axis=1, keepdims=True)
            ez = np.exp(z)
            probs = ez / ez.sum(axis=1, keepdims=True)
            p = probs[idx, y]
            per = -np.log(np.clip(p, 1e-9, None))
            if m is not None:
                per = per * m
            if w_cls is not None:
                per = per * w_cls[idx, y]
            loss += float(per.sum() / max(n, 1))
            dlog = probs.copy()
            dlog[idx, y] -= 1.0
            if m is not None:
                dlog *= m[:, None]
            if w_cls is not None:
                dlog *= w_cls
            dlog /= max(n, 1)
            hw, hb = gheads[name]
            hw += acts[-1].T @ dlog
            hb += dlog.sum(axis=0)
            dh_total += dlog @ self.heads[name][0].T
        # 逐层反传（acts[i] 是第 i 层输入；acts[i+1] 是第 i 层输出激活）
        dh = dh_total
        for i in reversed(range(len(self.W))):
            dh_pre = dh * (1.0 - acts[i + 1] ** 2)     # tanh'
            gw[i] += acts[i].T @ dh_pre
            gb[i] += dh_pre.sum(axis=0)
            dh = dh_pre @ self.W[i].T
        return loss, {"W": gw, "b": gb, "heads": gheads}

    def sgd_step(self, grads, lr):
        for i in range(len(self.W)):
            self.W[i] -= lr * grads["W"][i]
            self.b[i] -= lr * grads["b"][i]
        for name, (w, b) in self.heads.items():
            gw, gb = grads["heads"][name]
            self.heads[name] = (w - lr * gw, b - lr * gb)

    # ---- Adam（首跑 SGD 欠拟合 2.89->2.64 后引入，2026-09-20）----
    def _adam_slots(self):
        if not hasattr(self, "_m"):
            self._m = {"W": [np.zeros_like(w) for w in self.W],
                       "b": [np.zeros_like(b) for b in self.b],
                       "heads": {k: (np.zeros_like(w), np.zeros_like(b))
                                 for k, (w, b) in self.heads.items()}}
            self._v = {"W": [np.zeros_like(w) for w in self.W],
                       "b": [np.zeros_like(b) for b in self.b],
                       "heads": {k: (np.zeros_like(w), np.zeros_like(b))
                                 for k, (w, b) in self.heads.items()}}
            self._t = 0

    @staticmethod
    def _adam_delta(p, g, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
        m *= b1
        m += (1 - b1) * g
        v *= b2
        v += (1 - b2) * g * g
        return -lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)

    def adam_step(self, grads, lr):
        self._adam_slots()
        self._t += 1
        t = self._t
        for i in range(len(self.W)):
            self.W[i] += self._adam_delta(
                self.W[i], grads["W"][i], self._m["W"][i],
                self._v["W"][i], t, lr)
            self.b[i] += self._adam_delta(
                self.b[i], grads["b"][i], self._m["b"][i],
                self._v["b"][i], t, lr)
        for name, (w, b) in self.heads.items():
            gw, gb = grads["heads"][name]
            mw, mb = self._m["heads"][name]
            vw, vb = self._v["heads"][name]
            w += self._adam_delta(w, gw, mw, vw, t, lr)
            b += self._adam_delta(b, gb, mb, vb, t, lr)


def onehot_w(y, n_cls, w_map):
    out = np.ones((len(y), n_cls), dtype=np.float32)
    for cls, w in w_map.items():
        out[y == cls, cls] = w
    return out


def train_net(model, data, targets, masks, weights, epochs, batch, lr,
              log_prefix, optimizer="adam"):
    n = data.shape[0]
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    for epoch in range(epochs):
        order = rng.permutation(n)
        tot, nb = 0.0, 0
        for i in range(0, n, batch):
            idx = order[i:i + batch]
            loss, grads = model.loss_and_grads(
                data[idx], {k: v[idx] for k, v in targets.items()},
                {k: v[idx] for k, v in masks.items()} if masks else {},
                {k: v[idx] for k, v in weights.items()} if weights else {})
            if optimizer == "adam":
                model.adam_step(grads, lr)
            else:
                model.sgd_step(grads, lr)
            tot += loss
            nb += 1
        print(f"[{log_prefix}] epoch {epoch + 1}/{epochs} "
              f"loss={tot / max(nb, 1):.4f} "
              f"({time.time() - t0:.0f}s)", flush=True)
    return model


def head_acc(model, x, y, head):
    outs, _ = model.forward(x)
    pred = outs[head].argmax(axis=1)
    return float((pred == y).mean()), pred


# --------------------------------------------------------------------------
# 导出（int8 量化 + 纯 Python 前向源码）
# --------------------------------------------------------------------------
def quantize(mat, bits=8):
    scale = float(np.abs(mat).max()) / (2 ** (bits - 1) - 1)
    scale = max(scale, 1e-9)
    q = np.clip(np.round(mat / scale), -127, 127).astype(np.int8)
    return q, scale


def export_model(path: Path, unit_model: MLP, market_model: MLP, meta: dict):
    def ser(m: MLP):
        layers = []
        for w, b in zip(m.W, m.b):
            qw, sw = quantize(w)
            qb, sb = quantize(b)
            layers.append({"W": qw.flatten().tolist(), "Ws": sw,
                           "Wshape": list(qw.shape),
                           "b": qb.flatten().tolist(), "bs": sb})
        heads = {}
        for name, (w, b) in m.heads.items():
            qw, sw = quantize(w)
            qb, sb = quantize(b)
            heads[name] = {"W": qw.flatten().tolist(), "Ws": sw,
                           "Wshape": list(qw.shape),
                           "b": qb.flatten().tolist(), "bs": sb}
        return {"layers": layers, "heads": heads}
    payload = {
        "schema": S.SCHEMA_VERSION,
        "meta": meta,
        "unit_net": ser(unit_model),
        "market_net": ser(market_model),
    }
    body = json.dumps(payload, separators=(",", ":"))
    src = [
        '# -*- coding: utf-8 -*-',
        '"""Track-C BC 模型 v1 —— 量化权重硬编码（自动生成，勿手改）.',
        '',
        f'生成：train_bc.py @ {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}',
        f'schema：{S.SCHEMA_VERSION}；加载用 bc_policy.load_model()。',
        '"""',
        'MODEL_JSON = (',
    ]
    # 折行字符串（保持文件可 diff、行宽可控；单引号包裹 + 转义）
    chunk = 900
    for i in range(0, len(body), chunk):
        seg = body[i:i + chunk].replace("\\", "\\\\").replace("'", "\'")
        src.append(f"    '{seg}'")
    src.append(')')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(src) + "\n", encoding="utf-8")
    return path.stat().st_size


# --------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--batch", type=int, default=8192)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--model-name", default="bc_model_v1.py",
                    help="导出模型文件名（models/ 下；schema 改版必须换名）")
    args = ap.parse_args(argv)

    t0 = time.time()
    unit, mkt, train_keys, held_keys, seat_counts = load_datasets()
    print(f"[data] unit samples={unit['x'].shape[0]} "
          f"market slots={mkt['x'].shape[0]} "
          f"train_games={len(train_keys)} held_games={len(held_keys)} "
          f"seats(train/held)={seat_counts}")
    (DATA / "split.json").parent.mkdir(parents=True, exist_ok=True)
    (DATA / "split.json").write_text(json.dumps(
        {"holdout_pct": HOLDOUT_PCT, "seed": SEED,
         "train_games": train_keys, "heldout_games": held_keys},
        indent=1), encoding="utf-8")

    rng = np.random.default_rng(SEED)
    n_uin = S.N_GLOBAL_FEATURES + S.N_UNIT_FEATURES + 1
    unit_model = MLP(n_uin, UNIT_HIDDEN,
                     {"op": len(S.UNIT_OPS), "arg": len(S.ITEMS),
                      "qty": len(S.QTY_BUCKETS)}, rng)
    # 条件掩码
    arg_m = np.isin(unit["op"], sorted(ARG_OPS))
    qty_m = np.isin(unit["op"], sorted(QTY_OPS))
    train_net(unit_model, unit["x"],
              {"op": unit["op"], "arg": unit["arg"], "qty": unit["qty"]},
              {"arg": arg_m, "qty": qty_m}, {},
              args.epochs, args.batch, args.lr, "unit")

    rng2 = np.random.default_rng(SEED + 1)
    n_min = S.N_GLOBAL_FEATURES + S.N_MARKET_SLOTS
    market_model = MLP(n_min, MARKET_HIDDEN,
                       {"op": len(S.MARKET_ORDER_OPS), "item": len(S.ITEMS),
                        "qty": len(S.QTY_BUCKETS)}, rng2)
    item_m = np.isin(mkt["op"], sorted(MKT_ITEM_OPS))
    qty_m2 = np.isin(mkt["op"], sorted(MKT_QTY_OPS))
    none_w = onehot_w(mkt["op"], len(S.MARKET_ORDER_OPS),
                      {S.MARKET_OP_IDX["NONE"]: NONE_W})
    train_net(market_model, mkt["x"],
              {"op": mkt["op"], "item": mkt["item"], "qty": mkt["qty"]},
              {"item": item_m, "qty": qty_m2}, {"op": none_w},
              args.epochs, args.batch, args.lr, "market")

    # ---- 评估：train 子集 + held-out 专家样本 ----
    report = {"schema": S.SCHEMA_VERSION, "seed": SEED,
              "epochs": args.epochs, "batch": args.batch, "lr": args.lr,
              "hidden": {"unit": UNIT_HIDDEN, "market": MARKET_HIDDEN},
              "none_weight": NONE_W, "counts": {
                  "unit_samples": int(unit["x"].shape[0]),
                  "market_slots": int(mkt["x"].shape[0]),
                  "train_games": len(train_keys),
                  "heldout_games": len(held_keys)}}

    sub = np.random.default_rng(SEED + 2).choice(
        unit["x"].shape[0], size=min(200_000, unit["x"].shape[0]),
        replace=False)
    acc_op, _ = head_acc(unit_model, unit["x"][sub], unit["op"][sub], "op")
    am = arg_m[sub]
    acc_arg, _ = head_acc(unit_model, unit["x"][sub][am], unit["arg"][sub][am],
                          "arg")
    qm = qty_m[sub]
    acc_qty, _ = head_acc(unit_model, unit["x"][sub][qm],
                          unit["qty"][sub][qm], "qty")
    msub = np.random.default_rng(SEED + 3).choice(
        mkt["x"].shape[0], size=min(200_000, mkt["x"].shape[0]),
        replace=False)
    acc_mop, _ = head_acc(market_model, mkt["x"][msub], mkt["op"][msub], "op")
    nm = item_m[msub]
    acc_mitem, _ = head_acc(market_model, mkt["x"][msub][nm],
                            mkt["item"][msub][nm], "item")
    # 多数类基线（参照系：不学任何东西的常数预测）
    vals, cnts = np.unique(unit["op"], return_counts=True)
    maj_unit = float(cnts.max() / cnts.sum())
    nn = mkt["op"][mkt["op"] != S.MARKET_OP_IDX["NONE"]]
    vals2, cnts2 = np.unique(nn, return_counts=True)
    maj_mkt_nn = float(cnts2.max() / cnts2.sum())
    report["majority_baseline"] = {"unit_op": maj_unit,
                                   "market_op_nonnone": maj_mkt_nn}
    report["train_acc"] = {"unit_op": acc_op, "unit_arg": acc_arg,
                           "unit_qty": acc_qty, "market_op": acc_mop,
                           "market_item": acc_mitem}
    print(f"[acc/train] unit op={acc_op:.3f} arg={acc_arg:.3f} "
          f"qty={acc_qty:.3f} | market op={acc_mop:.3f} "
          f"item={acc_mitem:.3f}")

    hx_u, hy_u, hx_m, hy_m = load_heldout_reference()
    if len(hy_u):
        h_op, _ = head_acc(unit_model, hx_u, hy_u, "op")
        h_mop, pred_m = head_acc(market_model, hx_m, hy_m, "op")
        nonnone = hy_m != S.MARKET_OP_IDX["NONE"]
        h_mop_nn = (float((pred_m[nonnone] == hy_m[nonnone]).mean())
                    if nonnone.any() else None)
        report["heldout_acc"] = {"unit_op": h_op, "market_op_all": h_mop,
                                 "market_op_nonnone": h_mop_nn}
        print(f"[acc/held] unit op={h_op:.3f} | market op(all)={h_mop:.3f} "
              f"op(non-NONE)={h_mop_nn}")

    meta = {"seed": SEED, "epochs": args.epochs,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                          time.gmtime())}
    out_path = MODELS / args.model_name
    size = export_model(out_path, unit_model, market_model, meta)
    report["model_file"] = str(out_path.relative_to(SOFTWARE))
    report["model_bytes"] = size
    report["wall_seconds"] = round(time.time() - t0, 1)
    MODELS.mkdir(parents=True, exist_ok=True)
    (MODELS / "train_report.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"[train] model -> {out_path} ({size} B) "
          f"report -> {MODELS / 'train_report.json'} "
          f"wall={report['wall_seconds']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
