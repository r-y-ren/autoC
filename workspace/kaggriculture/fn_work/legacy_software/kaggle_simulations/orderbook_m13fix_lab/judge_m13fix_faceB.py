# -*- coding: utf-8 -*-
"""judge_m13fix_faceB：双局专组第二镜像面（ep2 具名镜像类对手 h1）。

背景：faceA（ep2=本件自拷贝镜像）的钱面结构性平局（干净件对镜像恒 0），
净翻胜(=margin>0 翻)不可判；faceB 用 h1_mirror 类 namesake（h1 件）作 ep2
对手，margin 为实数，污染恢复可翻胜。8 组×双席×2 局×2 臂=64 局次；
并入 faceA 后总预算 188+64=252 ≤ 300。复用 judge_m13fix 的 run_chain。
只写 orderbook_m13fix_lab/ + 证据文件；不提交；不发射。
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
sys.path.insert(0, str(MODULE_DIR))

_spec = importlib.util.spec_from_file_location("judge_m13fix", MODULE_DIR / "judge_m13fix.py")
J = importlib.util.module_from_spec(_spec)
sys.modules["judge_m13fix"] = J
_spec.loader.exec_module(J)

H1_OPP = str(KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")


def flip_stats(rows):
    return J.flip_stats(rows)


def main():
    t0 = time.perf_counter()
    from orderbook_r40 import sim_bridge as sb
    ev_path = J.EVID_PATH
    ev = json.loads(ev_path.read_text(encoding="utf-8"))
    # 认证沿用主跑（faceB 同引擎同语料；不重认证省局次）
    auth_lite = ((ev.get("source") or {}).get("sim_auth") or {})
    if not auth_lite.get("consistency_ok"):
        print("faceB aborted: 主跑 sim_auth 未过", flush=True)
        return
    run_cfg = {"engine": "auto", "bridge": None, "workers": J.WORKERS}
    run_cfg["engine"] = "sim"     # 主跑已 30/30 认证；faceB 强制 sim 线

    chains = []
    for seed in J.NEUTRAL_FOLDS:
        for seat in (0, 1):
            for arm_path in (J.DROPHALF_MAIN, J.DHFIX_MAIN):
                try:
                    chains.append(J.run_chain(arm_path, seed, seat, run_cfg,
                                              ep2_opp_path=H1_OPP))
                except Exception as exc:
                    J.ANOMALIES.append("faceB chain %s seed=%s seat=%s: %r"
                                       % (Path(arm_path).parent.name, seed,
                                          seat, exc))
    by_arm = {"drop_half": [], "dh_fix": []}
    for c in chains:
        key = "dh_fix" if "dh_fix" in str(c.get("arm")) else "drop_half"
        by_arm.setdefault(key, []).append(c)
    keymap = {(c["seed"], c["seat"]): c for c in by_arm["dh_fix"]}
    flip_rows, ep1_rows = [], []
    for c in by_arm["drop_half"]:
        v = keymap.get((c["seed"], c["seat"]))
        if not v:
            continue
        if c.get("ep2_margin") is not None and v.get("ep2_margin") is not None:
            flip_rows.append({"seed": c["seed"], "seat": c["seat"],
                              "margin_control": round(float(c["ep2_margin"]), 1),
                              "margin_variant": round(float(v["ep2_margin"]), 1)})
        if c.get("ep1_margin") is not None and v.get("ep1_margin") is not None:
            ep1_rows.append({"seed": c["seed"], "seat": c["seat"],
                             "margin_control": round(float(c["ep1_margin"]), 1),
                             "margin_variant": round(float(v["ep1_margin"]), 1)})
    fb_ps = flip_stats(flip_rows)
    fb_e1 = flip_stats(ep1_rows)
    pol = {a: {
        "n": len(by_arm[a]),
        "ep1_trigger_ok": sum(1 for c in by_arm[a] if c.get("ep1_trigger_ok")),
        "ep2_zero_pollution": sum(1 for c in by_arm[a]
                                  if c.get("ep2_zero_pollution")),
        "ep2_zero_pollution_given_ep1_trigger": sum(
            1 for c in by_arm[a]
            if c.get("ep1_trigger_ok") and c.get("ep2_zero_pollution")),
        "ep2_latch_true": sum(1 for c in by_arm[a] if c.get("ep2_latch") == [True]),
        "ep2_dirty_cells_max": max([c.get("ep2_dirty_cells") or 0
                                    for c in by_arm[a]] or [0]),
        "ep2_cls_hist": {cls: sum(1 for c in by_arm[a] if c.get("ep2_cls") == cls)
                         for cls in sorted({str(c.get("ep2_cls"))
                                            for c in by_arm[a]})},
    } for a in ("drop_half", "dh_fix")}
    ev["multi_game_group"]["faceB_h1"] = {
        "design": "faceB：同进程双局串跑 ep1 WFR 对手 → ep2 镜像类具名对手 h1"
                  "（h1_mirror 类 namesake；全矩阵画像 100%% h1_mirror 语义）；"
                  "8 组×双席×2 臂=32 链 64 局",
        "chains": chains, "pollution": pol,
        "ep2_flip_table": fb_ps, "ep1_flip_table": fb_e1,
    }

    # ---- 判据合并重算（净翻胜以 faceB 实数钱面为主判，faceA 记结构性平局） ----
    dh_poll = pol["dh_fix"]
    zero_poll_b = (dh_poll["ep2_zero_pollution_given_ep1_trigger"]
                   == dh_poll["ep1_trigger_ok"] and dh_poll["ep1_trigger_ok"] > 0
                   and dh_poll["ep2_latch_true"] == 0)
    fa = ev["multi_game_group"]
    fa_poll = fa["pollution"]["dh_fix"]
    zero_poll_a = (fa_poll["ep2_zero_pollution_given_ep1_trigger"]
                   == fa_poll["ep1_trigger_ok"] and fa_poll["ep1_trigger_ok"] > 0
                   and fa_poll["ep2_latch_true"] == 0)
    pooled_rows = list(fb_ps.get("rows_lite") or []) + \
        list((fa.get("ep2_flip_table") or {}).get("rows_lite") or [])
    pooled = flip_stats(pooled_rows)
    pairs_ft = ev["pairs"]["flip_table"]
    all_flips_neg = all(x == 0 for x in (pairs_ft.get("flips_neg"),
                                         (fa.get("ep2_flip_table") or {}).get("flips_neg"),
                                         (fa.get("ep1_flip_table") or {}).get("flips_neg"),
                                         fb_ps.get("flips_neg"),
                                         fb_e1.get("flips_neg")))
    rp = ev["pairs"]["realized"]
    ev["criteria"] = {
        "净翻胜>0": {
            "scope": "faceB（ep2 vs h1 实数钱面）主判 + faceA/配对组（结构性平局"
                     "/逐拍恒等）附记",
            "faceB_ep2_net_flip_wins": fb_ps.get("net_flip_wins"),
            "faceB_ep2_flips_pos": fb_ps.get("flips_pos"),
            "faceB_ep2_flips_neg": fb_ps.get("flips_neg"),
            "faceB_ep2_W_L_T": "%s/%s/%s" % (fb_ps.get("W"), fb_ps.get("L"),
                                             fb_ps.get("T")),
            "faceB_ep2_mean_delta": fb_ps.get("mean_delta"),
            "faceA_ep2_net_flip_wins": (fa.get("ep2_flip_table") or {}).get(
                "net_flip_wins"),
            "faceA_ep2_W_L_T": "%s/%s/%s" % (
                (fa.get("ep2_flip_table") or {}).get("W"),
                (fa.get("ep2_flip_table") or {}).get("L"),
                (fa.get("ep2_flip_table") or {}).get("T")),
            "faceA_note": "自拷贝镜像恒平局（margin 0 非 >0），净翻胜结构性不可判；"
                          "Δ 口径 W14/L2 mean+1638.75=污染恢复",
            "pooled_net_flip_wins": pooled.get("net_flip_wins"),
            "pairs_net_flip_wins": pairs_ft.get("net_flip_wins"),
            "passed": bool((fb_ps.get("net_flip_wins") or 0) > 0
                           or (pooled.get("net_flip_wins") or 0) > 0),
        },
        "flips_neg==0": {
            "pairs": pairs_ft.get("flips_neg"),
            "faceA_ep2": (fa.get("ep2_flip_table") or {}).get("flips_neg"),
            "faceA_ep1": (fa.get("ep1_flip_table") or {}).get("flips_neg"),
            "faceB_ep2": fb_ps.get("flips_neg"),
            "faceB_ep1": fb_e1.get("flips_neg"),
            "passed": bool(all_flips_neg),
        },
        "双局专组零污染": {
            "faceA_dh_fix_ep2_zero_given_trigger":
                "%d/%d" % (fa_poll["ep2_zero_pollution_given_ep1_trigger"],
                           fa_poll["ep1_trigger_ok"]),
            "faceB_dh_fix_ep2_zero_given_trigger":
                "%d/%d" % (dh_poll["ep2_zero_pollution_given_ep1_trigger"],
                           dh_poll["ep1_trigger_ok"]),
            "faceB_dh_fix_ep2_latch_true": dh_poll["ep2_latch_true"],
            "faceB_drop_half_ep2_polluted":
                "%d/%d" % (pol["drop_half"]["ep2_latch_true"],
                           pol["drop_half"]["n"]),
            "faceB_drop_half_ep2_dirty_cells_max":
                pol["drop_half"]["ep2_dirty_cells_max"],
            "passed": bool(zero_poll_a and zero_poll_b),
        },
        "实现价非负": dict(rp, passed=bool(rp.get("nonneg_both"))),
    }
    passed = all(v["passed"] for v in ev["criteria"].values())
    ev["verdict"] = {
        "criteria_passed": passed,
        "positive_arm": passed,
        "pairs_identity_ok": (pairs_ft.get("W") == 0 and pairs_ft.get("L") == 0
                              and ev["pairs"].get("stream_sha_identical")
                              == "32/32"),
        "multi_game_zero_pollution_ok": bool(zero_poll_a and zero_poll_b),
        "summary": ("dh_fix 三缺陷已修（探针 12/12 全绿；drop_half 对照 P8/P10 "
                    "DEFECT+P13 FAIL）；单局配对32/32 逐拍恒等=零回归；双局专组 "
                    "faceA %d/%d + faceB %d/%d 链零污染（drop_half %d/%d+%d/%d "
                    "污染形态）；faceB ep2 净翻胜 %s（W/L/T %s，mean Δ %s）"
                    % (fa_poll["ep2_zero_pollution"], fa_poll["n"],
                       dh_poll["ep2_zero_pollution"], dh_poll["n"],
                       fa["pollution"]["drop_half"]["ep2_latch_true"],
                       fa["pollution"]["drop_half"]["n"],
                       pol["drop_half"]["ep2_latch_true"], pol["drop_half"]["n"],
                       fb_ps.get("net_flip_wins"),
                       "%s/%s/%s" % (fb_ps.get("W"), fb_ps.get("L"),
                                     fb_ps.get("T")),
                       fb_ps.get("mean_delta"))),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    b = ev.setdefault("budget", {})
    b["multi_game_局次"] = int(b.get("multi_game_局次") or 0) + len(chains) * 2
    b["total_局次"] = (int(b.get("auth_局次") or 0) + int(b.get("pairs_局次") or 0)
                       + int(b.get("multi_game_局次") or 0))
    b["within_cap"] = b["total_局次"] <= J.BUDGET_CAP
    b["faceB_局次"] = len(chains) * 2
    ev["anomaly"] = list(J.ANOMALIES) + list(ev.get("anomaly") or [])
    ev["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ev["elapsed_s_faceB"] = round(time.perf_counter() - t0, 1)
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=1,
                                  default=str) + "\n", encoding="utf-8")
    J.LEDGER_PATH.write_text(json.dumps(
        {"budget": b, "criteria": ev["criteria"],
         "faceB_ep2_flip_table": fb_ps, "faceB_ep1_flip_table": fb_e1,
         "faceB_pollution": pol},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("FACEB VERDICT:", json.dumps(ev["verdict"], ensure_ascii=False,
                                       default=str)[:400], flush=True)
    print("DONE budget:", b, flush=True)
    return ev


if __name__ == "__main__":
    main()
