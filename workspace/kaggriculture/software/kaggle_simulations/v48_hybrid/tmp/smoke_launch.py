# -*- coding: utf-8 -*-
# 【中文】smoke_launch.py —— v48_hybrid 冒烟（F2 批次，临时脚本，落 tmp/）
# ===========================================================================
# 三道冒烟（v48plus_launch_check 先例，门实现复用 scripts/
# v48_derivative_launch_check.py，仅重定向路径到 v48_hybrid/，产物全落
# v48_hybrid/tmp/，不触碰 v48_hybrid/ 外任何文件）：
#   ① 官方装载语义：干净 -I 子进程复刻 get_last_callable（append→exec→
#      pop→最后 callable），真实引擎 obs 序列驱动，零异常，且与主进程
#      fresh 装载动作流逐字节一致；named agent == last callable；
#   ② vendored 引擎（1.32.7+nodeps）双席自打 2 局完整 720 回合
#      （seeds 101/102）statuses 双 DONE、每步 <1000ms；
#   ③ 确定性：seed 101 重跑，双席 720 步动作流哈希逐字节一致。
# 前置：重跑 build.py（包双跑逐字节自证）+ audit_base.py（分区审计 PASS）。
# CLI：python tmp/smoke_launch.py [--keep-tmp]
# ===========================================================================
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # v48_hybrid/
KSIM = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(KSIM)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

TMP = os.path.join(HERE, "tmp")
OUT_DIR = os.path.join(TMP, "probes")
LC_TMP = os.path.join(TMP, "lc_tmp")

HYB_MAIN = os.path.join(HERE, "main.py")
HYB_TAR = os.path.join(HERE, "submission.tar.gz")
LAUNCH_CHECK = os.path.join(SOFTWARE, "scripts",
                            "v48_derivative_launch_check.py")


def run(cmd, cwd=None):
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                          cwd=cwd)
    return proc


def load_check_module():
    spec = importlib.util.spec_from_file_location("hybrid_launch_base",
                                                  LAUNCH_CHECK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap_is_keep = "--keep-tmp" in sys.argv
    sys.dont_write_bytecode = True   # 不在交付目录落 __pycache__
    t0 = time.perf_counter()
    os.makedirs(TMP, exist_ok=True)

    # 0) 重建 + 审计
    proc = run([sys.executable, os.path.join(HERE, "build.py")])
    if proc.returncode != 0:
        print(proc.stdout[-2000:], proc.stderr[-2000:], sep="\n")
        raise SystemExit("build.py failed")
    manifest = json.loads(proc.stdout)
    print(f"[build] main {manifest['main_py']['bytes']}B "
          f"sha256={manifest['main_py']['sha256'][:12]}…  "
          f"tar {manifest['submission_tar_gz']['bytes']}B "
          f"sha256={manifest['submission_tar_gz']['sha256'][:12]}…  "
          f"deterministic_double_build="
          f"{manifest['deterministic_double_build']} "
          f"double_pack="
          f"{manifest['submission_tar_gz']['deterministic_double_pack']} "
          f"flag_off_zero_wiring={manifest['flag_off_zero_wiring']}",
          flush=True)

    proc = run([sys.executable, os.path.join(HERE, "audit_base.py")])
    if proc.returncode != 0:
        print(proc.stdout[-2000:], proc.stderr[-2000:], sep="\n")
        raise SystemExit("audit_base.py failed")
    audit_tail = [ln for ln in proc.stdout.splitlines()
                  if ln.startswith("audit_pass")]
    print(f"[audit] {audit_tail[-1] if audit_tail else 'audit_pass = ?'} "
          f"(partitioned diff: prefix verbatim, zero modified base lines, "
          f"five zero-change zones, three injection points only)",
          flush=True)

    # 1-3) 四门口径冒烟（gate2/3 → gate1，obs 复用）
    check = load_check_module()
    check.DERIV_DIR = HERE
    check.DERIV_MAIN = HYB_MAIN
    check.DERIV_TAR = HYB_TAR
    check.OUT_DIR = OUT_DIR
    check.TMP_DIR = LC_TMP

    g23 = check.gate2_gate3()
    obs_seed101 = g23.pop("_obs_series_seed101", None)
    for ep in g23["gate2_episodes"]:
        print(f"[gate2] seed={ep['seed']} statuses={ep['statuses']} "
              f"rewards=[{ep['rewards'][0]:.0f},{ep['rewards'][1]:.0f}] "
              f"turns={ep['turns_played']} "
              f"max_step={ep['max_step_ms']}ms p99={ep['p99_step_ms']}ms "
              f"wall={ep['wall_s']}s", flush=True)
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

    verdict = {
        "protocol": "v48-hybrid-smoke/1.0",
        "package": {
            "main_sha256": manifest["main_py"]["sha256"],
            "main_bytes": manifest["main_py"]["bytes"],
            "tar_sha256": manifest["submission_tar_gz"]["sha256"],
            "tar_bytes": manifest["submission_tar_gz"]["bytes"],
            "deterministic_double_build":
                manifest["deterministic_double_build"],
            "deterministic_double_pack":
                manifest["submission_tar_gz"]["deterministic_double_pack"],
            "flag_off_zero_wiring": manifest["flag_off_zero_wiring"],
            "gate4_size_ok":
                manifest["submission_tar_gz"]["bytes"] <= (100 << 20),
        },
        "gate1_official_load": g1,
        "gate2_full_episodes": g23,
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    verdict["all_gates_pass"] = bool(
        g1["gate1_official_load_ok"]
        and g23["gate2_full_episodes_ok"]
        and g23["gate3_determinism_ok"]
        and verdict["package"]["gate4_size_ok"])
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "v48_hybrid_smoke.json"), "w",
              encoding="utf-8") as h:
        json.dump(verdict, h, ensure_ascii=False, indent=1)

    if not ap_is_keep:
        shutil.rmtree(LC_TMP, ignore_errors=True)
    print(f"all_gates_pass = {verdict['all_gates_pass']}")
    print(f"out -> {os.path.join(OUT_DIR, 'v48_hybrid_smoke.json')}")
    return 0 if verdict["all_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
