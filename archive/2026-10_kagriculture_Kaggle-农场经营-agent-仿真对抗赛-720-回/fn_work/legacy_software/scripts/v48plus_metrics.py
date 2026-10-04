# 【中文】v48plus_metrics.py —— 把 v48plus 三份探针 JSON 合入 software/metrics.json 分片
# ===========================================================================
# 数据纪律：只写实测值（探针产物），方法字段写明测量口径与产物路径。
# 顶层 <战役根>/metrics.json 是 merge_metrics.py 的汇总生成物，本脚本不碰。
# CLI：python scripts/v48plus_metrics.py
# ===========================================================================
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
PROBE = os.path.join(SOFTWARE, "exports", "probes", "v48plus")
METRICS = os.path.join(SOFTWARE, "metrics.json")


def load(name):
    with open(os.path.join(PROBE, name), "r", encoding="utf-8") as handle:
        return json.load(handle)


def main():
    gate = load("v48plus_ab_gate.json")
    launch = load("v48plus_launch_check.json")
    ablation = load("v48plus_layer_ablation.json")

    panel = {k: v for k, v in gate["panel"].items()
             if not k.startswith("_")}
    entries = {
        "v48plus_build": {
            "method": "v48plus 确定性构建（software/kaggle_simulations/v48plus/build_v48plus.py，2026-09-21）：base=references/data/intel-notebooks/v48build/main.py（sha256 dadee25a…，与在跑 v48_derivative/main.py 逐字节一致）逐字前缀 + v48plus_layers.py（V49/V50 经济层手工移植 COURIER+SHEDROOM，纯追加零改动 base）逐字后缀；双次构建/双次确定性 tar（mtime=0/uid=gid=0/mode0644/gzip mtime=0）字节一致自证；stdlib-only",
            "value": launch["package"],
        },
        "v48plus_layer_selection": {
            "method": "层选择证据（scripts/v48plus_layer_ablation.py，seeds 101/102 × 双席 × starter/v14.2 = 8 局/变体）：COURIER(C)/CAPHARV(CH)/SHEDROOM(SR) 八组合消融；结论=CAPHARV 在本底座六路线全部跟踪局 0 次触发（磁带已在 cap 前收割，死代码）移出 shipping build；CH 孤立切片存在跨段符号依赖（_V48P_COURIER_MOVES）属消融 harness 伪影已注明；starter 面板（无状态对手，干净口径）base 0 / C +1228 / SR +3752 / C_SR +3340；v14.2 列受其跨局模块态漂移混淆（消融面板内 base 两次等价装载差 >1k）仅作参考；全量判定以 ab_gate 面板（v14.2 每局 fresh 装载）为准",
            "value": {
                "variants_starter_delta": {
                    name: rec["starter_mean_vs_base"]
                    for name, rec in ablation["variants"].items()},
                "capharv_swaps_all_tracked_games": 0,
                "shipping_layers": ["COURIER", "SHEDROOM"],
                "probe": "exports/probes/v48plus/v48plus_layer_ablation.json",
            },
        },
        "v48plus_ab_gate": {
            "method": "孪生 A/B 门（scripts/v48plus_ab_gate.py，官方 vendored 1.32.7 引擎，2026-09-21）：判据①=同种子 v48(dadee25a) vs v48+ 直接 h2h 16 局（seeds 101-104/201-204 × 双席位）v48+ 得分（胜+0.5平）≥45%；判据②=多样对手面板同种子同席对照（starter 基线 8 seeds×双席、我方 v14.2 每局 fresh 装载、2 巨人回放对手流原种子逐动作回放）总体 mean(v48+)/mean(v48) ≥0.97；判据③=全部 statuses 双 DONE + contract ok + 每步 agent 耗时 <1000ms；附 9 巨人局 d0 反事实（round24 TARGET9，twin 引擎，对手=回放真实动作）方向核对",
            "value": {
                "plus_main_sha256": gate["plus"]["sha256"],
                "h2h": {"games": len(gate["h2h"]["games"]),
                        "plus_wins": gate["h2h"]["plus_wins"],
                        "v48_wins": gate["h2h"]["v48_wins"],
                        "ties": gate["h2h"]["ties"],
                        "plus_score": gate["h2h"]["plus_score"],
                        "pass_45pct": gate["h2h"]["pass"]},
                "panel_overall": gate["panel"]["_overall"],
                "panel_by_opponent": {
                    k: {"v48_mean": v["v48_mean"],
                        "plus_mean": v["plus_mean"],
                        "ratio": v["ratio"]}
                    for k, v in panel.items()},
                "anomalies": gate["anomalies"],
                "layer_telemetry": gate["layer_telemetry"],
                "giants_d0_counterfactual": {
                    "summary": gate["giants"]["_summary"],
                    "direction_ok": gate["giants"]["_direction_ok"],
                    "episodes": {k: v for k, v in gate["giants"].items()
                                 if not k.startswith("_")}},
                "verdict": gate["verdict"],
                "probe": "exports/probes/v48plus/v48plus_ab_gate.json",
            },
        },
        "v48plus_launch_check": {
            "method": "发射四件套预检（scripts/v48plus_launch_check.py 复用 v48_derivative_launch_check 四门实现，包路径重定向 v48plus，2026-09-21）：门1=干净 -I 子进程复刻官方 get_last_callable（append→exec→pop→最后 callable），seed101 局 719 真实 obs 驱动并与主进程 fresh 装载逐字节比对；门2=双席自打完整局 seeds 101/102 各 720 turns，statuses/每步耗时；门3=同 seed 重跑双席动作流规范化哈希一致；门4=tar.gz ≤100MB；另断言 base 逐字前缀 + layers 逐字后缀",
            "value": {
                "all_gates_pass": launch["all_gates_pass"],
                "gate1_official_load_ok": launch["gate1_official_load"]["gate1_official_load_ok"],
                "last_callable": launch["gate1_official_load"]["evidence"]["last_callable_name"],
                "gate2_full_episodes_ok": launch["gate2_full_episodes"]["gate2_full_episodes_ok"],
                "gate3_determinism_ok": launch["gate3_determinism_ok"],
                "gate4_size_ok": launch["gate4_size_ok"],
                "max_step_ms": max(ep["max_step_ms"] for ep in
                                   launch["gate2_full_episodes"]["gate2_episodes"]),
                "tar_bytes": launch["package"]["tar_bytes"],
                "probe": "exports/probes/v48plus/v48plus_launch_check.json",
            },
        },
    }

    with open(METRICS, "r", encoding="utf-8") as handle:
        metrics = json.load(handle)
    for key, entry in entries.items():
        entry["value"] = json.loads(json.dumps(
            entry["value"], ensure_ascii=False))
        metrics["metrics"][key] = entry
    metrics["measured_at"] = "2026-09-21"
    with open(METRICS, "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, ensure_ascii=False, indent=1)
        handle.write("\n")
    print("merged keys:", list(entries))
    print("verdict:", json.dumps(gate["verdict"], ensure_ascii=False))


if __name__ == "__main__":
    main()
