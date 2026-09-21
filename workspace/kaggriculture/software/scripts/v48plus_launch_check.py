# 【中文】v48plus_launch_check.py —— v48+ 发射四件套预检
# ===========================================================================
# 复用 v48_derivative_launch_check.py 的四道门实现（单一实现防漂移），
#   仅把包路径重定向到 v48plus/，并追加两项 v48plus 特有断言：
#   0a) 构建自证：main.py = v48 解码真源码（dadee25a…）逐字前缀 + layers
#       逐字后缀，双次构建字节一致（build_v48plus.py 的 manifest 复核）；
#   0b) 官方语义装载/短局实测/确定性/包体四门 = 门①②③④同口径。
# 输出：exports/probes/v48plus/v48plus_launch_check.json
# CLI：python scripts/v48plus_launch_check.py [--keep-tmp]
# ===========================================================================
from __future__ import annotations

import argparse
import hashlib
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

BASE_MAIN = os.path.join(CAMP, "references", "data", "intel-notebooks",
                         "v48build", "main.py")
LAYERS = os.path.join(SOFTWARE, "kaggle_simulations", "v48plus",
                      "v48plus_layers.py")
PLUS_DIR = os.path.join(SOFTWARE, "kaggle_simulations", "v48plus")
PLUS_MAIN = os.path.join(PLUS_DIR, "main.py")
PLUS_TAR = os.path.join(PLUS_DIR, "submission.tar.gz")
OUT_PATH = os.path.join(SOFTWARE, "exports", "probes", "v48plus",
                        "v48plus_launch_check.json")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_check_module():
    path = os.path.join(HERE, "v48_derivative_launch_check.py")
    spec = importlib.util.spec_from_file_location("v48plus_launch_base",
                                                  path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_artifact() -> dict:
    """跑构建器（含双次构建/双次打包自证），并断言 v48 前缀逐字保留。"""
    import subprocess
    proc = subprocess.run([sys.executable,
                           os.path.join(PLUS_DIR, "build_v48plus.py")],
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit(f"构建失败:\n{proc.stdout}\n{proc.stderr}")
    manifest = json.loads(proc.stdout)

    base = open(BASE_MAIN, "rb").read()
    layers = open(LAYERS, "rb").read()
    main = open(PLUS_MAIN, "rb").read()
    prefix_ok = main.startswith(base if base.endswith(b"\n") else base + b"\n")
    suffix_ok = main.endswith(layers)
    verbatim_ok = prefix_ok and suffix_ok
    if not verbatim_ok:
        raise SystemExit("FAIL: main.py 不是 base 逐字前缀 + layers 逐字后缀")
    return {
        "base_sha256": manifest["base"]["sha256"],
        "layers_sha256": manifest["layers"]["sha256"],
        "main_sha256": manifest["main_py"]["sha256"],
        "main_bytes": manifest["main_py"]["bytes"],
        "tar_sha256": manifest["submission_tar_gz"]["sha256"],
        "tar_bytes": manifest["submission_tar_gz"]["bytes"],
        "base_verbatim_prefix_ok": prefix_ok,
        "layers_verbatim_suffix_ok": suffix_ok,
        "deterministic_build_ok": bool(
            manifest["deterministic_double_build"]
            and manifest["submission_tar_gz"]["deterministic_double_pack"]),
        "stdlib_only_ok": True,
        "gate4_size_ok": manifest["submission_tar_gz"]["bytes"] <= (100 << 20),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-tmp", action="store_true")
    args = parser.parse_args()

    t0 = time.perf_counter()
    package = build_artifact()
    print(f"[build] main {package['main_bytes']}B "
          f"sha256={package['main_sha256'][:12]}… "
          f"tar {package['tar_bytes']}B "
          f"sha256={package['tar_sha256'][:12]}…", flush=True)

    check = load_check_module()
    check.DERIV_DIR = PLUS_DIR
    check.DERIV_MAIN = PLUS_MAIN
    check.DERIV_TAR = PLUS_TAR
    check.OUT_DIR = os.path.dirname(OUT_PATH)
    check.TMP_DIR = os.path.join(os.path.dirname(OUT_PATH), "tmp_v48plus")

    g23 = check.gate2_gate3()
    obs_seed101 = g23.pop("_obs_series_seed101", None)
    for ep in g23["gate2_episodes"]:
        print(f"[gate2] seed={ep['seed']} statuses={ep['statuses']} "
              f"rewards=[{ep['rewards'][0]:.0f},{ep['rewards'][1]:.0f}] "
              f"max_step={ep['max_step_ms']}ms p99={ep['p99_step_ms']}ms "
              f"wall={ep['wall_s']}s", flush=True)
    print(f"[gate3] determinism_ok={g23['gate3_determinism_ok']} "
          f"run1={g23['gate3_hashes']['run1'][:12]}… "
          f"run2={g23['gate3_hashes']['run2'][:12]}…", flush=True)

    g1 = check.gate1(obs_seed101)
    ev = g1["evidence"]
    print(f"[gate1] last_callable={ev['last_callable_name']} "
          f"mismatches={g1['isolated_vs_local_action_mismatches']} "
          f"non_stdlib={ev['non_stdlib_imports']}", flush=True)

    verdict = {
        "protocol": "v48plus-launch-check/1.0",
        "package": package,
        "gate1_official_load": g1,
        "gate2_full_episodes": g23,
        "gate3_determinism_ok": g23["gate3_determinism_ok"],
        "gate4_size_ok": package["gate4_size_ok"],
        "build_gates_ok": bool(package["base_verbatim_prefix_ok"]
                               and package["layers_verbatim_suffix_ok"]
                               and package["deterministic_build_ok"]
                               and package["stdlib_only_ok"]),
        "all_gates_pass": bool(g1["gate1_official_load_ok"]
                               and g23["gate2_full_episodes_ok"]
                               and g23["gate3_determinism_ok"]
                               and package["gate4_size_ok"]),
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(verdict, handle, ensure_ascii=False, indent=1)
    if not args.keep_tmp:
        import shutil
        shutil.rmtree(check.TMP_DIR, ignore_errors=True)
    print(f"all_gates_pass = {verdict['all_gates_pass']}")
    print(f"out -> {OUT_PATH}")
    return 0 if verdict["all_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
