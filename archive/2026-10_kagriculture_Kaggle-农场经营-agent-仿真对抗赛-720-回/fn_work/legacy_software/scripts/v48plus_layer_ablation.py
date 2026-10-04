# 【中文】v48plus_layer_ablation.py —— v48+ 三层逐层消融（诊断 vs v14.2 回退）
# ===========================================================================
# 背景：quick A/B 面板显示 v48+ 对 starter +2.1%、对回放对手 ~1.00、
#   对我方 v14.2 -8.9%。本探针按层组合切片构建变体（base/C/CH/SR/C+CH/
#   C+SR/CH+SR/ALL），对 v14.2 与 starter 各跑同种子同席对照，定位回退层。
# 变体构建：v48plus_layers.py 按 section 注释行切片拼接（构建器同序），
#   变体文件只落 probes 目录（D14 圈禁内）。
# 输出：exports/probes/v48plus/v48plus_layer_ablation.json
# CLI：python scripts/v48plus_layer_ablation.py [--seeds 101,102]
# ===========================================================================
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
CAMP = os.path.dirname(SOFTWARE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

from kgenv.arena import load_submission_agent, run_episode  # noqa: E402

V48_MAIN = os.path.join(CAMP, "references", "data", "intel-notebooks",
                        "v48build", "main.py")
LAYERS = os.path.join(SOFTWARE, "kaggle_simulations", "v48plus",
                      "v48plus_layers.py")
OUR_MAIN = os.path.join(SOFTWARE, "kaggle_simulations", "agent", "main.py")
VARIANT_DIR = os.path.join(SOFTWARE, "exports", "probes", "v48plus",
                           "variants")
OUT_PATH = os.path.join(SOFTWARE, "exports", "probes", "v48plus",
                        "v48plus_layer_ablation.json")

DASH = "# ---------------------------------------------------------------------------"


def slice_sections():
    lines = open(LAYERS, "r", encoding="utf-8").read().splitlines(keepends=True)
    marks = {}
    for i, line in enumerate(lines):
        if line.startswith("# COURIER (from"):
            marks["C"] = i - 1          # include the dash line above
        elif line.startswith("# CAPHARV (V49"):
            marks["CH"] = i - 1
        elif line.startswith("# SHEDROOM (V49"):
            marks["SR"] = i - 1
        elif line.startswith("def _v48plus_entrypoint"):
            marks["TAIL"] = i
    head = "".join(lines[:marks["C"]])
    courier = "".join(lines[marks["C"]:marks["CH"]])
    capharv = "".join(lines[marks["CH"]:marks["SR"]])
    shedroom = "".join(lines[marks["SR"]:marks["TAIL"]])
    tail = "".join(lines[marks["TAIL"]:])
    return head, {"C": courier, "CH": capharv, "SR": shedroom}, tail


def load_variant(path, tag):
    spec = importlib.util.spec_from_file_location(f"v48plus_variant_{tag}",
                                                  os.path.abspath(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="101,102")
    args = parser.parse_args()
    seeds = [int(s) for s in args.seeds.split(",") if s]
    os.makedirs(VARIANT_DIR, exist_ok=True)

    head, sections, tail = slice_sections()
    base_src = open(V48_MAIN, "r", encoding="utf-8").read()
    if not base_src.endswith("\n"):
        base_src += "\n"
    variants = {
        "base": [],
        "C": ["C"],
        "CH": ["CH"],
        "SR": ["SR"],
        "C_CH": ["C", "CH"],
        "C_SR": ["C", "SR"],
        "CH_SR": ["CH", "SR"],
        "ALL": ["C", "CH", "SR"],
    }
    our = load_submission_agent(OUR_MAIN)
    import kgenv.bots.baseline as baseline_bots
    opponents = [("our_v14_2", our),
                 ("starter", baseline_bots.baseline_wheat_agent)]

    out = {"protocol": "v48plus-layer-ablation/1.0", "variants": {}}
    for name, order in variants.items():
        if name == "base":
            module = None
            agent_fn = load_submission_agent(V48_MAIN)
        else:
            path = os.path.join(VARIANT_DIR, f"main_{name}.py")
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(base_src + head
                             + "".join(sections[k] for k in order) + tail)
            module = load_variant(path, name)
            agent_fn = module.agent
        rec = {"rows": [], "telemetry": None}
        for opp_name, opp_fn in opponents:
            for seed in seeds:
                for seat in (0, 1):
                    if seat == 0:
                        res = run_episode(agent_fn, opp_fn, seed)
                    else:
                        res = run_episode(opp_fn, agent_fn, seed)
                    mine = float(res["rewards"][seat])
                    rec["rows"].append({"opp": opp_name, "seed": seed,
                                        "seat": seat, "money": mine,
                                        "statuses": res["statuses"]})
                    print(f"  {name:6s} {opp_name} seed={seed} seat={seat} "
                          f"money={mine:.0f}", flush=True)
        if module is not None:
            rec["telemetry"] = dict(module._V48P_REPORT)
        for opp_name, _ in opponents:
            rows = [r["money"] for r in rec["rows"] if r["opp"] == opp_name]
            rec[f"{opp_name}_mean"] = round(sum(rows) / len(rows), 1)
        out["variants"][name] = rec
        print(f"== {name}: v14_2_mean={rec['our_v14_2_mean']} "
              f"starter_mean={rec['starter_mean']}", flush=True)

    base_rec = out["variants"]["base"]
    for opp_name, _ in opponents:
        key = f"{opp_name}_mean"
        for name, rec in out["variants"].items():
            rec[f"{key}_vs_base"] = round(rec[key] - base_rec[key], 1)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("wrote", OUT_PATH, flush=True)


if __name__ == "__main__":
    main()
