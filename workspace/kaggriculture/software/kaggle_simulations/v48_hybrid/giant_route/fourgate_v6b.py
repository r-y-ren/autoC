# -*- coding: utf-8 -*-
# 【中文】fourgate_v6b.py —— v6b 发射四门（R9-G2b，临时脚本，落 giant_route/）
# 复用 software/scripts/v48_derivative_launch_check.py 门实现（F2/v4/v4b/v5/
# v6 同法：importlib 装载后仅重定向路径），对 v6b/ 包执行四门冒烟；
# 通过后回填 v6b/build_manifest.json 与 v6b/README.md 门禁表。
# 产物：tmp/probes_v6b/v6b_smoke.json。
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HYBRID = os.path.dirname(HERE)
KSIM = os.path.dirname(HYBRID)
SOFTWARE = os.path.dirname(KSIM)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

TMP = os.path.join(HYBRID, "tmp")
OUT_DIR = os.path.join(TMP, "probes_v6b")
LC_TMP = os.path.join(TMP, "lc_tmp_v6b")
LAUNCH_CHECK = os.path.join(SOFTWARE, "scripts",
                            "v48_derivative_launch_check.py")
V6B_MAIN = os.path.join(HYBRID, "v6b", "main.py")
V6B_TAR = os.path.join(HYBRID, "v6b", "submission.tar.gz")

sys.dont_write_bytecode = True


def load_check_module():
    spec = importlib.util.spec_from_file_location("v6b_launch_check_base",
                                                  LAUNCH_CHECK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def backfill(verdict: dict) -> None:
    g1, g2 = verdict["gate1_official_load"], verdict["gate2_full_episodes"]
    ep_lines = "; ".join(
        f"seed{ep['seed']} statuses={ep['statuses']} "
        f"rewards=[{ep['rewards'][0]:.0f},{ep['rewards'][1]:.0f}] "
        f"{ep['turns_played']}回合 max {ep['max_step_ms']}ms "
        f"p99 {ep['p99_step_ms']}ms"
        for ep in g2["gate2_episodes"])
    summary = {
        "gate1_official_load": (
            f"干净 -I 子进程 get_last_callable 复刻，named==last"
            f"（{g1['evidence']['last_callable_name']}），isolated vs local "
            f"动作流 mismatch="
            f"{g1['isolated_vs_local_action_mismatches']}，stdlib 扫描空"),
        "gate2_full_episodes": (
            f"seeds 101/102 双席自打双 DONE 720 回合，{ep_lines}"),
        "gate3_determinism": (
            f"seed101 重跑动作流哈希逐字节一致"
            f"（{g2['gate3_hashes']['run1'][:12]}…）"),
        "gate4_size": (f"{verdict['package']['tar_bytes']:,}B ≤ 100MB"),
        "passed": verdict["all_gates_pass"],
        "artifact": "tmp/probes_v6b/v6b_smoke.json",
    }
    mpath = os.path.join(HYBRID, "v6b", "build_manifest.json")
    with open(mpath, encoding="utf-8") as h:
        manifest = json.load(h)
    manifest["gate_results"]["launch_fourgate"] = summary
    manifest["gate_results"]["status"] = "SMOKE_ONLY_PASS"
    with open(mpath, "w", encoding="utf-8") as h:
        json.dump(manifest, h, ensure_ascii=False, indent=2, sort_keys=True)
        h.write("\n")

    rpath = os.path.join(HYBRID, "v6b", "README.md")
    with open(rpath, encoding="utf-8") as h:
        readme = h.read()
    rows = {
        "| gate1 官方装载语义 | 干净 -I 子进程 get_last_callable 复刻一致 | "
        "PENDING |":
            "| gate1 官方装载语义 | 干净 -I 子进程 get_last_callable 复刻一致 | "
            f"PASS（{summary['gate1_official_load']}） |",
        "| gate2 双席自打 | seeds 101/102 双局 720 回合 DONE、每步 <1000ms | "
        "PENDING |":
            "| gate2 双席自打 | seeds 101/102 双局 720 回合 DONE、每步 <1000ms | "
            f"PASS（{summary['gate2_full_episodes']}） |",
        "| gate3 确定性 | seed101 重跑动作流哈希逐字节一致 | PENDING |":
            "| gate3 确定性 | seed101 重跑动作流哈希逐字节一致 | "
            f"PASS（{summary['gate3_determinism']}） |",
        "| gate4 体积 | tar ≤ 100MB | PENDING |":
            "| gate4 体积 | tar ≤ 100MB | "
            f"PASS（{summary['gate4_size']}） |",
    }
    for old, new in rows.items():
        if old not in readme:
            raise SystemExit(f"README gate row not found: {old[:40]}…")
        readme = readme.replace(old, new)
    with open(rpath, "w", encoding="utf-8") as h:
        h.write(readme)


def main() -> int:
    t0 = time.perf_counter()
    os.makedirs(OUT_DIR, exist_ok=True)

    check = load_check_module()
    check.DERIV_DIR = os.path.join(HYBRID, "v6b")
    check.DERIV_MAIN = V6B_MAIN
    check.DERIV_TAR = V6B_TAR
    check.OUT_DIR = OUT_DIR
    check.TMP_DIR = LC_TMP

    g23 = check.gate2_gate3()
    obs_seed101 = g23.pop("_obs_series_seed101", None)
    for ep in g23["gate2_episodes"]:
        print(f"[gate2] seed={ep['seed']} statuses={ep['statuses']} "
              f"rewards=[{ep['rewards'][0]:.0f},{ep['rewards'][1]:.0f}] "
              f"turns={ep['turns_played']} max_step={ep['max_step_ms']}ms "
              f"p99={ep['p99_step_ms']}ms wall={ep['wall_s']}s", flush=True)
    print(f"[gate3] determinism_ok={g23['gate3_determinism_ok']} "
          f"run1={g23['gate3_hashes']['run1'][:12]}… "
          f"run2={g23['gate3_hashes']['run2'][:12]}…", flush=True)

    g1 = check.gate1(obs_seed101)
    ev = g1["evidence"]
    print(f"[gate1] last_callable={ev['last_callable_name']} "
          f"n_obs={g1['n_obs_replayed']} "
          f"mismatches={g1['isolated_vs_local_action_mismatches']} "
          f"non_stdlib={ev['non_stdlib_imports']} "
          f"named==last:{ev['named_agent_same_output_as_last']} "
          f"loader_pop={ev['loader_pop_applied']} "
          f"wall={g1['driver_wall_s']}s", flush=True)

    tar_bytes = os.path.getsize(V6B_TAR)
    main_bytes = os.path.getsize(V6B_MAIN)
    gate4_size_ok = tar_bytes <= (100 << 20)
    print(f"[gate4] tar={tar_bytes}B main={main_bytes}B "
          f"size_ok={gate4_size_ok}", flush=True)

    verdict = {
        "protocol": "v6b-launch-fourgate/1.0",
        "package": {
            "main_sha256": check.sha256_bytes(open(V6B_MAIN, "rb").read()),
            "main_bytes": main_bytes,
            "tar_sha256": check.sha256_bytes(open(V6B_TAR, "rb").read()),
            "tar_bytes": tar_bytes,
            "gate4_size_ok": gate4_size_ok,
        },
        "gate1_official_load": g1,
        "gate2_full_episodes": g23,
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    verdict["all_gates_pass"] = bool(
        g1["gate1_official_load_ok"]
        and g23["gate2_full_episodes_ok"]
        and g23["gate3_determinism_ok"]
        and gate4_size_ok)
    with open(os.path.join(OUT_DIR, "v6b_smoke.json"), "w",
              encoding="utf-8") as h:
        json.dump(verdict, h, ensure_ascii=False, indent=1)

    if verdict["all_gates_pass"]:
        backfill(verdict)
    shutil.rmtree(LC_TMP, ignore_errors=True)
    print(f"all_gates_pass = {verdict['all_gates_pass']}")
    print(f"out -> {os.path.join(OUT_DIR, 'v6b_smoke.json')}")
    return 0 if verdict["all_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
