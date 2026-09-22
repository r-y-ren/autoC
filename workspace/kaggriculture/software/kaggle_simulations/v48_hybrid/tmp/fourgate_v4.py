# -*- coding: utf-8 -*-
# 【中文】fourgate_v4.py —— v4 发射四门（临时脚本，落 tmp/）
# ===========================================================================
# 复用 software/scripts/v48_derivative_launch_check.py 门实现（与 F2
# smoke_launch.py 同法：importlib 装载后仅重定向路径），对 v4/ 包执行：
#   门① 官方装载语义（干净 -I 子进程 get_last_callable 复刻 + stdlib 扫描
#        + named==last + 与主进程 fresh 装载动作流逐字节一致）；
#   门② vendored 引擎双席自打 2 局（seeds 101/102）完整 720 回合双 DONE、
#        每步 <1000ms、无可疑日志；
#   门③ 确定性：seed 101 重跑动作流哈希逐字节一致；
#   门④ 体积 ≤100MB。
# 附加交叉核验：v4 自打终局 vs 纯 v48 自打基线（h2h_gate.json 同种子）
# ——行为级≡的先声。产物：tmp/probes_v4/v4_smoke.json。
# ===========================================================================
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # v48_hybrid/
KSIM = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(KSIM)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

TMP = os.path.join(HERE, "tmp")
OUT_DIR = os.path.join(TMP, "probes_v4")
LC_TMP = os.path.join(TMP, "lc_tmp_v4")
LAUNCH_CHECK = os.path.join(SOFTWARE, "scripts",
                            "v48_derivative_launch_check.py")
V4_MAIN = os.path.join(HERE, "v4", "main.py")
V4_TAR = os.path.join(HERE, "v4", "submission.tar.gz")

sys.dont_write_bytecode = True


def load_check_module():
    spec = importlib.util.spec_from_file_location("v4_launch_check_base",
                                                  LAUNCH_CHECK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    t0 = time.perf_counter()
    os.makedirs(OUT_DIR, exist_ok=True)

    check = load_check_module()
    check.DERIV_DIR = os.path.join(HERE, "v4")
    check.DERIV_MAIN = V4_MAIN
    check.DERIV_TAR = V4_TAR
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

    tar_bytes = os.path.getsize(V4_TAR)
    main_bytes = os.path.getsize(V4_MAIN)
    gate4_size_ok = tar_bytes <= (100 << 20)

    # 交叉核验：v4 自打终局 vs 纯 v48 自打基线（同种子，h2h_gate 基线域）
    baseline = {}
    try:
        with open(os.path.join(HERE, "gates", "out", "h2h_gate.json"),
                  encoding="utf-8") as h:
            h2h = json.load(h)
        baseline = {str(g["seed"]): g["rewards"] for g in
                    h2h["zero_new_anomalies"]["baseline"]["games"]}
    except (OSError, KeyError):
        baseline = {}
    cross = {str(ep["seed"]):
             {"v4_rewards": ep["rewards"],
              "pure_v48_selfplay_rewards": baseline.get(str(ep["seed"])),
              "equal": baseline.get(str(ep["seed"])) == ep["rewards"]}
             for ep in g23["gate2_episodes"]}

    verdict = {
        "protocol": "v4-launch-fourgate/1.0",
        "package": {
            "main_sha256": check.sha256_bytes(open(V4_MAIN, "rb").read()),
            "main_bytes": main_bytes,
            "tar_sha256": check.sha256_bytes(open(V4_TAR, "rb").read()),
            "tar_bytes": tar_bytes,
            "gate4_size_ok": gate4_size_ok,
        },
        "gate1_official_load": g1,
        "gate2_full_episodes": g23,
        "crosscheck_v4_selfplay_vs_pure_v48_baseline": cross,
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    verdict["all_gates_pass"] = bool(
        g1["gate1_official_load_ok"]
        and g23["gate2_full_episodes_ok"]
        and g23["gate3_determinism_ok"]
        and gate4_size_ok)
    with open(os.path.join(OUT_DIR, "v4_smoke.json"), "w",
              encoding="utf-8") as h:
        json.dump(verdict, h, ensure_ascii=False, indent=1)

    shutil.rmtree(LC_TMP, ignore_errors=True)
    print(f"all_gates_pass = {verdict['all_gates_pass']}")
    print(f"crosscheck vs pure v48 selfplay baseline = "
          f"{json.dumps(cross, ensure_ascii=False)}")
    print(f"out -> {os.path.join(OUT_DIR, 'v4_smoke.json')}")
    return 0 if verdict["all_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
