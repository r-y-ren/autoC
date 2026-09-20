# -*- coding: utf-8 -*-
"""Track-C (BC) M1 推理策略：权重硬编码模型的纯 Python 前向 agent.

stdlib-only、确定性（同 obs 同动作，无集合迭代序依赖）、独立于 v14.x
chassis（standalone，spec Implementation Decisions）。

前向性能设计（1s/回合 + 60s 池预算）：
  第一层输入 = G(167) + 局部段（U14+flag 或 slot10）。把第一层权重按行
  拆成 G 段与局部段——G·Wg 每回合只算一次，逐单位/逐槽只补局部段。

合法性掩码（引擎静默 no-op 的动作不浪费在 argmax 上；factsheet §3）：
  - DROP/PICKUP/PLACE 需站中心 2×2 棚访问格；
  - PLANT 需站 None 空地且该作物种子 >0（按 arg 头预测的作物）；
  - 地块类操作（WATER/HARVEST/...）需站已解锁地块（tile 非 "LOCKED"）。
  掩码 = 非法 op 的 logit 置 -inf，argmax 在合法集内取。

用法（bc_eval / 孪生内）：
    from bc_policy import BCPolicy
    policy = BCPolicy()          # 默认加载 models/bc_model_v1.py
    action = policy(obs)         # 官方语义 callable
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import bc_schema as S                                     # noqa: E402

MODELS_DIR = _HERE.parent / "models"
DEFAULT_MODEL = MODELS_DIR / "bc_model_v1.py"

SHED_ACCESS = {(4, 4), (5, 4), (4, 5), (5, 5)}
TILE_OPS = {"PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG",
            "BUILD_COOP", "BUILD_PASTURE", "FEED", "COLLECT_FERTILIZER",
            "CARE"}


# --------------------------------------------------------------------------
# obs 适配（twin.Observation 属性访问 / Struct / 纯 dict 三态归一）
# --------------------------------------------------------------------------
def to_plain_obs(obs) -> dict:
    if isinstance(obs, dict):
        return obs
    out = {}
    for key in ("day", "farms", "hour", "market", "player", "private",
                "remainingOverageTime", "step", "town"):
        val = getattr(obs, key, None)
        if val is not None:
            out[key] = val
    return out


# --------------------------------------------------------------------------
# 模型装载与纯 Python 前向
# --------------------------------------------------------------------------
def _deq(entry):
    """量化层条目 -> (flat_weight, scale, shape)。"""
    return (entry, )  # 占位：实际展开在 load_model


class Net:
    """纯 Python 两隐层 tanh + 多头。量化反演：W = Wq*ws（输出侧乘 ws）。

    正确的反量化语义（与 numpy 训练网一致）：
      y = W @ x + b ≈ ws*(Wq @ x) + bs*(bq)
    shared-G 路径：G 段点积每回合一次（precompute_g），局部段增量补。
    """

    __slots__ = ("W", "b", "heads", "g_split")

    def __init__(self, payload: dict, g_split: int):
        self.W = []
        self.b = []
        for layer in payload["layers"]:
            self.W.append((layer["W"], layer["Ws"],
                           tuple(layer["Wshape"])))
            self.b.append((layer["b"], layer["bs"], (layer["Wshape"][1],)))
        self.heads = {}
        for name, head in payload["heads"].items():
            self.heads[name] = (
                (head["W"], head["Ws"], tuple(head["Wshape"])),
                (head["b"], head["bs"], (head["Wshape"][1],)))
        self.g_split = g_split

    @staticmethod
    def _dot_raw(flat_w, xs, n_out):
        """未缩放点积：sum_i x[i]*Wq[i][j]（跳过零输入）。"""
        out = [0.0] * n_out
        k = 0
        for xv in xs:
            if xv == 0.0:
                k += n_out
                continue
            for j in range(n_out):
                out[j] += xv * flat_w[k + j]
            k += n_out
        return out

    @staticmethod
    def _finish(raw, b_flat, ws, bs):
        return [ws * o + bs * bv for o, bv in zip(raw, b_flat)]

    @staticmethod
    def _tanh_inplace(v):
        import math
        for i in range(len(v)):
            x = v[i]
            if x > 20.0:
                v[i] = 1.0
            elif x < -20.0:
                v[i] = -1.0
            else:
                v[i] = 2.0 / (1.0 + math.exp(-2.0 * x)) - 1.0

    def precompute_g(self, g_vec):
        """G 段过第一层（每回合一次）。返回未过 tanh 的预激活。"""
        w_flat, ws, wshape = self.W[0]
        b_flat, bs, _ = self.b[0]
        raw = self._dot_raw(w_flat, g_vec[: self.g_split], wshape[1])
        return self._finish(raw, b_flat, ws, bs)

    def finish_first_then_rest(self, g_pre, local_vec):
        """局部段补第一层 -> tanh -> 其余层 -> 头。"""
        w_flat, ws, wshape = self.W[0]
        n_out = wshape[1]
        acc = list(g_pre)
        k = self.g_split * n_out
        for li, xv in enumerate(local_vec):
            if xv == 0.0:
                continue
            base = k + li * n_out
            for j in range(n_out):
                acc[j] += ws * xv * w_flat[base + j]
        self._tanh_inplace(acc)
        h = acc
        for li in range(1, len(self.W)):
            w_flat, ws, wshape = self.W[li]
            b_flat, bs, _ = self.b[li]
            raw = self._dot_raw(w_flat, h, wshape[1])
            h = self._finish(raw, b_flat, ws, bs)
            self._tanh_inplace(h)
        heads = {}
        for name, (w_ent, b_ent) in self.heads.items():
            w_flat, ws, wshape = w_ent
            b_flat, bs, _ = b_ent
            raw = self._dot_raw(w_flat, h, wshape[1])
            heads[name] = self._finish(raw, b_flat, ws, bs)
        return heads

    def forward_full(self, x):
        """整向量前向（对齐自检用）。"""
        h = list(x)
        for li in range(len(self.W)):
            w_flat, ws, wshape = self.W[li]
            b_flat, bs, _ = self.b[li]
            raw = self._dot_raw(w_flat, h, wshape[1])
            h = self._finish(raw, b_flat, ws, bs)
            self._tanh_inplace(h)
        heads = {}
        for name, (w_ent, b_ent) in self.heads.items():
            w_flat, ws, wshape = w_ent
            b_flat, bs, _ = b_ent
            raw = self._dot_raw(w_flat, h, wshape[1])
            heads[name] = self._finish(raw, b_flat, ws, bs)
        return heads


def _load_payload(model_path: Path) -> dict:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        f"_bc_model_{abs(hash(str(model_path))) & 0xffffff:x}", model_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return json.loads(module.MODEL_JSON)


class BCPolicy:
    """官方语义 agent callable：obs -> {"farmer":…, "hands":…, "market":…}。"""

    def __init__(self, model_path=None, collect_stats=True):
        model_path = Path(model_path or DEFAULT_MODEL)
        payload = _load_payload(model_path)
        if payload.get("schema") != S.SCHEMA_VERSION:
            raise ValueError(
                f"模型 schema {payload.get('schema')} != 当前 "
                f"{S.SCHEMA_VERSION}（改版必须重训重导）")
        self.unit_net = Net(payload["unit_net"], S.N_GLOBAL_FEATURES)
        self.market_net = Net(payload["market_net"], S.N_GLOBAL_FEATURES)
        self.collect_stats = collect_stats
        self.reset_stats()
        self.meta = payload.get("meta") or {}

    def reset_stats(self):
        self.stats = {
            "unit_total": 0, "unit_move": 0, "unit_pass": 0,
            "unit_care": 0, "unit_water": 0, "unit_harvest": 0,
            "unit_shed": 0, "unit_illegal_masked": 0,
            "mkt_orders": 0, "mkt_sell": 0, "mkt_hire": 0,
            "mkt_buy_seed": 0, "mkt_buy_animal": 0,
            "mkt_buy_product": 0, "mkt_buy_land": 0, "turns": 0,
        }

    # ---- 掩码 -----------------------------------------------------------
    @staticmethod
    def _unit_mask(op_idx, obs_plain, seat, pos, seeds):
        """非法 op -> False（长度 18 布尔）。"""
        ok = [True] * len(S.UNIT_OPS)
        tiles = ((obs_plain.get("farms") or [{}] * 2)[seat]
                 .get("tiles")) or []
        x, y = int(pos[0]), int(pos[1])
        tile = (tiles[y][x] if 0 <= y < len(tiles) and 0 <= x < len(tiles[y])
                else "OOB")
        on_shed = (x, y) in SHED_ACCESS
        unlocked = tile is not None and tile != "LOCKED" and tile != "OOB"
        for i, op in enumerate(S.UNIT_OPS):
            if op in ("DROP", "PICKUP", "PLACE") and not on_shed:
                ok[i] = False
            elif op in TILE_OPS and not unlocked:
                ok[i] = False
            elif op == "PLANT":
                if tile is not None:
                    ok[i] = False
        return ok, tile

    # ---- 主入口 ---------------------------------------------------------
    def __call__(self, obs):
        obs_plain = to_plain_obs(obs)
        seat = int(obs_plain.get("player") or 0)
        g = S.extract_global_features(obs_plain, seat)
        g_u = self.unit_net.precompute_g(g)
        g_m = self.market_net.precompute_g(g)
        farms = obs_plain.get("farms") or []
        me = farms[seat] if seat < len(farms) else {}
        seeds = (obs_plain.get("private") or {}).get("seeds") or {}
        positions = [me.get("farmer")] + list(me.get("hands") or [])
        farmer_act = ["PASS"]
        hand_acts = []
        for i, pos in enumerate(positions):
            if not pos:
                if i > 0:
                    hand_acts.append(["PASS"])
                continue
            uf = S.extract_unit_features(obs_plain, seat, pos)
            heads = self.unit_net.finish_first_then_rest(
                g_u, uf + [1.0 if i == 0 else 0.0])
            op_logits, arg_logits, qty_logits = (heads["op"],
                                                 heads["arg"], heads["qty"])
            mask, _tile = self._unit_mask(0, obs_plain, seat, pos, seeds)
            # PLANT 合法性还依赖 arg 头预测的作物种子——两步近似：
            # arg 先取预测，若 PLANT 选中且该作物无种子则回退次优 op。
            arg_i = _argmax(arg_logits)
            order = _rank_order(op_logits, mask)
            op_i = order[0]
            crop = S.CROPS[arg_i % len(S.CROPS)]
            if S.UNIT_OPS[op_i] == "PLANT" and seeds.get(crop, 0) <= 0:
                op_i = order[1] if len(order) > 1 else S.UNIT_OP_IDX["PASS"]
                self.stats["unit_illegal_masked"] += 1
            qty_b = _argmax(qty_logits)
            act = S.decode_unit_action(op_i, arg_i, qty_b)
            if self.collect_stats:
                self._tally_unit(act)
            if i == 0:
                farmer_act = act
            else:
                hand_acts.append(act)
        market = []
        for slot in range(S.N_MARKET_SLOTS):
            oh = [0.0] * S.N_MARKET_SLOTS
            oh[slot] = 1.0
            heads = self.market_net.finish_first_then_rest(g_m, oh)
            op_i = _argmax(heads["op"])
            if op_i == 0:            # NONE
                continue
            item_i = _argmax(heads["item"])
            qty_b = _argmax(heads["qty"])
            market.append(S.decode_market_slots(
                [(op_i, item_i, qty_b)])[0])
        if self.collect_stats:
            self.stats["turns"] += 1
            for order in market:
                self.stats["mkt_orders"] += 1
                key = {"SELL": "mkt_sell", "HIRE": "mkt_hire",
                       "BUY_SEED": "mkt_buy_seed",
                       "BUY_ANIMAL": "mkt_buy_animal",
                       "BUY_PRODUCT": "mkt_buy_product",
                       "BUY_LAND": "mkt_buy_land"}.get(order[0])
                if key:
                    self.stats[key] += 1
        return {"farmer": farmer_act, "hands": hand_acts, "market": market}

    def _tally_unit(self, act):
        st = self.stats
        st["unit_total"] += 1
        op = act[0] if act else "PASS"
        if op in S.DIRS:
            st["unit_move"] += 1
        elif op == "PASS":
            st["unit_pass"] += 1
        elif op == "CARE":
            st["unit_care"] += 1
        elif op == "WATER":
            st["unit_water"] += 1
        elif op == "HARVEST":
            st["unit_harvest"] += 1
        elif op in ("DROP", "PICKUP", "PLACE"):
            st["unit_shed"] += 1

    def diagnostics(self) -> dict:
        st = self.stats
        n = max(st["unit_total"], 1)
        return {
            "turns": st["turns"],
            "unit_move_rate": round(st["unit_move"] / n, 4),
            "unit_pass_rate": round(st["unit_pass"] / n, 4),
            "care_total": st["unit_care"],
            "water_total": st["unit_water"],
            "harvest_total": st["unit_harvest"],
            "unit_illegal_masked": st["unit_illegal_masked"],
            "mkt_orders": st["mkt_orders"], "mkt_sell": st["mkt_sell"],
            "mkt_hire": st["mkt_hire"], "mkt_buy_seed": st["mkt_buy_seed"],
            "mkt_buy_animal": st["mkt_buy_animal"],
            "mkt_buy_product": st["mkt_buy_product"],
            "mkt_buy_land": st["mkt_buy_land"],
        }


def _argmax(xs):
    best = 0
    bv = xs[0]
    for i in range(1, len(xs)):
        if xs[i] > bv:
            bv = xs[i]
            best = i
    return best


def _rank_order(logits, mask):
    """合法集内按 logito 降序的 op 索引列表（确定性：平局取小索引）。"""
    order = sorted((i for i, ok in enumerate(mask) if ok),
                   key=lambda i: (-logits[i], i))
    return order


def forward_alignment_test(model_path=None) -> bool:
    """纯 Python 前向（shared-G 路径）vs 整向量路径一致性自检。"""
    pol = BCPolicy(model_path, collect_stats=False)
    import random
    rng = random.Random(7)
    for net, local_n in ((pol.unit_net, S.N_UNIT_FEATURES + 1),
                         (pol.market_net, S.N_MARKET_SLOTS)):
        g = [rng.uniform(-2, 2) for _ in range(S.N_GLOBAL_FEATURES)]
        loc = [rng.uniform(-2, 2) for _ in range(local_n)]
        g_pre = net.precompute_g(g)
        heads_a = net.finish_first_then_rest(g_pre, loc)
        heads_b = net.forward_full(g + loc)
        for name in heads_a:
            for a, b in zip(heads_a[name], heads_b[name]):
                if abs(a - b) > 1e-6 * max(1.0, abs(b)):
                    return False
    return True
