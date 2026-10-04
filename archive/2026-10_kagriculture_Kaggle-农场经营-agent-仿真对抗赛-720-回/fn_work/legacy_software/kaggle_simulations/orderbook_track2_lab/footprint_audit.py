# -*- coding: utf-8 -*-
"""footprint_audit：内生版差异拍足迹审计（非目标拍零足迹）。

数据：gates_track2 落盘的双席逐拍动作流（evidence/footprint/，同 seed 同件
自打=确定性配对）。审计口径：
- inner vs base / outer vs base / inner vs outer 逐拍动作对比（同席同拍）；
- 目标拍=step>=624（X1 触发窗）；**非目标拍（step<624）零足迹**：差异拍数必须为 0；
- 首差异拍步号 ≥624；差异拍步带分布；
- inner 卫生台账 ticks（_S1009_REPORT.hyg）全部 ≥624。
注意：同局双席自打下任一形态的动作差异会级联（对手=同形态镜像），
故级联差异允许出现在目标拍；非目标拍零足迹=机制窗口约束的硬断言。
只写 orderbook_track2_lab/。
"""
from __future__ import annotations

import json
import os
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
FOOT_DIR = os.path.join(ROOT, "evidence", "footprint")
WINDOW = 624
PAIR_DEFS = [("h1_inner", "h1_base"), ("h1_outer", "h1_base"),
             ("h1_inner", "h1_outer")]


def _load(form, tag):
    path = os.path.join(FOOT_DIR, "%s_%s.json" % (form, tag))
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _diff_stream(sa, sb):
    """两个 [(step, action_key)] 流逐拍对比 → 差异拍列表。"""
    diffs = []
    n = min(len(sa), len(sb))
    for i in range(n):
        (s1, a1), (s2, a2) = sa[i], sb[i]
        if s1 != s2 or a1 != a2:
            diffs.append({"idx": i, "step_a": s1, "step_b": s2,
                          "kind": "step_mismatch" if s1 != s2
                                  else "action_mismatch"})
    if len(sa) != len(sb):
        diffs.append({"idx": n, "kind": "length_mismatch",
                      "len_a": len(sa), "len_b": len(sb)})
    return diffs


def main():
    out = {"_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "window_target_step_ge": WINDOW,
           "caliber": ("同 seed 同件自打逐拍动作流对比；目标拍=step>=624（X1 触发"
                       "窗）；非目标拍=step<624 须零差异（零足迹硬断言）"),
           "pairs": {}, "hygiene_ticks": {}, "anomaly": []}
    ok_all = True
    for tag in ("s101", "s102", "s101_rerun"):
        for form_a, form_b in PAIR_DEFS:
            key = "%s_vs_%s@%s" % (form_a, form_b, tag)
            try:
                da = _load(form_a, tag)
                db = _load(form_b, tag)
            except Exception as exc:
                out["pairs"][key] = {"error": repr(exc)[:160]}
                continue
            rec = {"seed": da.get("seed"), "seats": []}
            for seat in (0, 1):
                sa = da["seats"][seat]
                sb = db["seats"][seat]
                diffs = _diff_stream(sa, sb)
                non_target = [d for d in diffs
                              if d.get("kind") != "length_mismatch"
                              and (d.get("step_a") or d.get("step_b") or 0)
                              < WINDOW]
                steps = sorted({d.get("step_a") for d in diffs
                                if d.get("kind") == "action_mismatch"})
                first = min((s for s in steps if s is not None), default=None)
                seat_rec = {
                    "seat": seat,
                    "n_ticks": min(len(sa), len(sb)),
                    "n_diff_ticks": len(diffs),
                    "first_diff_step": first,
                    "n_diff_step_lt_%d" % WINDOW: len(non_target),
                    "non_target_zero_footprint": len(non_target) == 0,
                    "diff_step_min": min(steps) if steps else None,
                    "diff_step_max": max(steps) if steps else None,
                }
                if not seat_rec["non_target_zero_footprint"]:
                    ok_all = False
                    seat_rec["non_target_examples"] = non_target[:5]
                rec["seats"].append(seat_rec)
            out["pairs"][key] = rec

    # ---- inner 卫生台账 ticks 全部 ≥624（自报口径交叉验证） ----
    for tag in ("s101", "s102", "s101_rerun"):
        try:
            gate = json.load(open(os.path.join(ROOT, "evidence", "gates.json"),
                                  encoding="utf-8"))
            reps = gate["forms"]["h1_inner"].get("hygiene_reports") or []
        except Exception as exc:
            out["hygiene_ticks"][tag] = {"error": repr(exc)[:160]}
            continue
        all_ticks = []
        idx = {"s101": 0, "s102": 1, "s101_rerun": 2}.get(tag, 0)
        if idx < len(reps):
            for rep in (reps[idx] or []):
                if isinstance(rep, dict):
                    all_ticks.extend(rep.get("ticks") or [])
        bad = [t for t in all_ticks if int(t) < WINDOW]
        out["hygiene_ticks"][tag] = {
            "n_ticks": len(all_ticks),
            "n_ticks_lt_%d" % WINDOW: len(bad),
            "all_in_window": not bad,
            "min_tick": min(all_ticks) if all_ticks else None,
        }
        if bad:
            ok_all = False

    out["overall_non_target_zero_footprint"] = ok_all
    with open(os.path.join(ROOT, "evidence", "footprint_audit.json"), "w",
              encoding="utf-8") as fh:
        fh.write(json.dumps(out, ensure_ascii=False, indent=1,
                            default=str) + "\n")
    print("footprint non-target zero:", ok_all)
    for k, v in out["pairs"].items():
        if isinstance(v, dict) and "seats" in v:
            print(" ", k, [(s["n_diff_ticks"], s["first_diff_step"],
                            s["non_target_zero_footprint"])
                           for s in v["seats"]])
    return out


if __name__ == "__main__":
    main()
