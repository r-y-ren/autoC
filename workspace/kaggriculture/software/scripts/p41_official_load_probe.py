# 【中文】p41_official_load_probe.py —— 生产装载路径接合探针（P4.1 根因定位）
# ===========================================================================
# 背景：DTSP v1（submission 56342843）线上 19 局动作流与纯 v13.8 逐字节
#   一致（零接合），而全部本地测试接合正常。本探针在本机按"官方打包→
#   官方装载→真实 replay obs 驱动"完整复现生产路径，逐关卡可证伪：
#     A) 打包：submission.tar.gz 解包到临时目录（模拟官方后端解包）；
#     B) 装载：严格复刻 vendored kaggle_environments.agent.get_last_callable
#        语义 —— sys.path.append(exec_dir) → exec(main.py 源码, 空 env) →
#        sys.path.pop() → 取 env 中最后一个 callable（vendored agent.py
#        L50-64；装载后 exec_dir 从 sys.path 移除是生产语义的关键一环）；
#     C) 驱动：灾难局（episode-110634204）obs 序列喂给装载出的 agent，
#        收集动作流 + 命名空间证据（PLANNER_ENABLED / _DTSP_LAST_PLAN_KEY /
#        planner 是否进过 sys.modules / 装载后 sys.path 是否仍含解包目录）。
#   子进程以 -I（隔离模式）运行且驱动脚本放在解包目录之外——杜绝本机
#   开发环 sys.path 污染掩盖生产缺陷（P3 测试矩阵的盲区正是这个污染）。
# 判定：打包 agent 动作流 vs 纯 v13.8 基线（同一 obs 流）逐步比对；
#   一致 = 零接合；分歧首步 + 命名空间证据 = 接合定位。
# ===========================================================================
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
AGENT_DIR = os.path.join(SOFTWARE, "kaggle_simulations", "agent")
PKG = os.path.join(AGENT_DIR, "submission.tar.gz")
WHEEL = os.path.join(SOFTWARE, "vendor",
                     "kaggle_environments-1.32.7+nodeps-py3-none-any.whl")
DEFAULT_REPLAY = os.path.join(
    SOFTWARE, "..", "references", "data", "online-replays", "round23",
    "episode-110634204-replay.json")
OUT_DIR = os.path.join(SOFTWARE, "exports", "probes", "p41_engagement")

# 生产装载语义的复刻锚点：vendored agent.py 必须仍含 append/pop 对
# （若上游语义变化，本探针的复刻假设需人工重审）。
OFFICIAL_SEMANTICS_PINS = (
    ("sys.path.append(exec_dir)", "exec 前 append 解包目录"),
    ("sys.path.pop()", "exec 后 pop 移除解包目录"),
    ("[v for v in env.values() if callable(v)][-1]", "取最后 callable"),
)


def norm_action(a):
    """动作规范化串（与 round23_dtsp_stepdiff_probe 同口径）。"""
    if isinstance(a, (list, tuple)):
        return "[" + ",".join(norm_action(x) for x in a) + "]"
    if isinstance(a, dict):
        return "{" + ",".join(f"{k}:{norm_action(a[k])}"
                              for k in sorted(a)) + "}"
    if isinstance(a, float):
        return f"{a:.4f}"
    return json.dumps(a, ensure_ascii=False, sort_keys=True)


# --------------------------------------------------------------------------
# 子进程驱动器（写入解包目录之外，-I 隔离运行）
# --------------------------------------------------------------------------
DRIVER_SRC = '''
"""官方语义装载驱动器：append -> exec -> pop -> 最后 callable。"""
import json, sys

pkg_dir, obs_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
main_py = pkg_dir + "/main.py"
with open(main_py, "r", encoding="utf-8") as h:
    src = h.read()

# --- 复刻 kaggle_environments.agent.get_last_callable（vendored 1.32.7）---
env = {}
exec_dir = pkg_dir                      # dirname(main.py)

# loader pop 保真（最小复刻，独立于 main.py 的腰带插入——main.py 会无条件
# 自插包根，路径长度检查会被它污染）：
sys.path.append(exec_dir)
_n1 = len(sys.path)
try:
    exec(compile("pass", "<popcheck>", "exec"), {})
finally:
    sys.path.pop()
loader_pop_applied = (len(sys.path) == _n1 - 1
                      and exec_dir not in sys.path)

sys.path.append(exec_dir)
try:
    exec(compile(src, main_py, "exec"), env)
finally:
    sys.path.pop()
# 修复后 main.py 会无条件自插包根（腰带层），故 exec_dir 仍可能留在
# sys.path——那是我们的条目，不是 loader 的（loader 的那份已被 pop 移除）。

# 取 env 中最后一个 callable（env 是 dict：插入序 = 定义序）
agent = [v for v in env.values() if callable(v)][-1]

ns = agent.__globals__
with open(obs_path, "r", encoding="utf-8") as h:
    obs_list = json.load(h)

actions = []
for obs in obs_list:
    actions.append(agent(obs))

evidence = {
    "loader_pop_applied": loader_pop_applied,
    "exec_dir_on_sys_path_after_load": exec_dir in sys.path,
    "planner_in_sys_modules": "planner.runtime" in sys.modules,
    "has_DTSP_RUNTIME_CONFIG": "DTSP_RUNTIME_CONFIG" in ns,
    "has_DTSP_RUNTIME_MODULE": "DTSP_RUNTIME_MODULE" in ns,
    "PLANNER_ENABLED": ns.get("PLANNER_ENABLED"),
    "has_pristine_snapshot": "_DTSP_PRISTINE_SNAPSHOT" in ns,
    "has_last_plan_key": "_DTSP_LAST_PLAN_KEY" in ns,
    "last_plan_key": ns.get("_DTSP_LAST_PLAN_KEY"),
    "hook_errors": list(ns.get("_DTSP_HOOK_ERRORS") or []),
    "sys_path_tail": sys.path[-3:],
}
rt = ns.get("DTSP_RUNTIME_MODULE")
if rt is not None:
    t = rt.trace()
    evidence["dawn_records"] = t["dawns"]
    evidence["failopens"] = t["failopens"]
    evidence["game_resets"] = t["game_resets"]
    evidence["engaged"] = any(d.get("selected") for d in t["dawns"])

with open(out_path, "w", encoding="utf-8") as h:
    json.dump({"actions": actions, "evidence": evidence}, h,
              ensure_ascii=False)
'''


def _check_official_semantics_pins():
    """从 vendored wheel 抽 agent.py 源码，锚定装载语义三要素。"""
    import zipfile
    with zipfile.ZipFile(WHEEL) as zf:
        src = zf.read("kaggle_environments/agent.py").decode("utf-8")
    missing = [name for pin, name in OFFICIAL_SEMANTICS_PINS if pin not in src]
    if missing:
        raise SystemExit(f"FAIL vendored agent.py 装载语义锚点缺失: {missing}"
                         "（上游语义可能已变，人工重审本探针复刻）")
    return True


def _load_obs_series(replay_path, seat, max_steps):
    with open(replay_path, "r", encoding="utf-8") as h:
        replay = json.load(h)
    steps = replay["steps"]
    obs_list = []
    for t in range(min(max_steps, len(steps))):
        entry = steps[t][seat] if isinstance(steps[t], list) \
            else steps[t].get(str(seat))
        obs = (entry or {}).get("observation")
        if obs is None:
            break
        obs_list.append(obs)
    return obs_list


def _v138_baseline_actions(obs_list):
    """纯 v13.8 基线（主进程计算：bench.exec 装载不依赖 sys.path 污染）。"""
    if SOFTWARE not in sys.path:
        sys.path.insert(0, SOFTWARE)
    sys.path.insert(0, HERE)
    import planner_offline_bench as bench  # noqa: E402
    ns, _a, _s = bench.build_v13_namespace(None)
    agent_fn = ns["agent"]
    return [agent_fn(obs) for obs in obs_list]


def run_probe(replay_path, seat=0, max_steps=720, keep_tmp=False,
              pkg_path=PKG):
    _check_official_semantics_pins()
    obs_list = _load_obs_series(replay_path, seat, max_steps)
    if not obs_list:
        raise SystemExit(f"FAIL replay 无 obs: {replay_path}")

    with tempfile.TemporaryDirectory(prefix="p41_probe_") as td:
        extract_dir = os.path.join(td, "pkg")
        os.makedirs(extract_dir)
        with tarfile.open(pkg_path, "r:gz") as tar:
            tar.extractall(extract_dir)          # 模拟官方后端解包
        # 驱动脚本放解包目录之外（防 sys.path[0] 救援 import planner）
        driver_path = os.path.join(td, "driver", "driver.py")
        os.makedirs(os.path.dirname(driver_path))
        with open(driver_path, "w", encoding="utf-8") as h:
            h.write(DRIVER_SRC)
        obs_path = os.path.join(td, "obs.json")
        out_path = os.path.join(td, "out.json")
        with open(obs_path, "w", encoding="utf-8") as h:
            json.dump(obs_list, h, ensure_ascii=False)

        # -I 隔离：无 site / 无 PYTHONPATH / 无用户目录 —— 只有 stdlib。
        proc = subprocess.run(
            [sys.executable, "-I", driver_path, extract_dir, obs_path,
             out_path], capture_output=True, text=True, timeout=600)
        if proc.returncode != 0:
            raise SystemExit(f"FAIL driver 子进程退出 {proc.returncode}\n"
                             f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        with open(out_path, "r", encoding="utf-8") as h:
            loaded = json.load(h)

    baseline = _v138_baseline_actions(obs_list)
    actions = loaded["actions"]
    first_mm = None
    mm_steps = []
    for i, (mine, base) in enumerate(zip(actions, baseline)):
        if norm_action(mine) != norm_action(base):
            mm_steps.append(i)
            if first_mm is None:
                first_mm = {"step": i, "day": obs_list[i].get("day"),
                            "hour": obs_list[i].get("hour")}
    day_of = {i: obs_list[i].get("day") for i in mm_steps}
    mm_after_d10 = [i for i in mm_steps if day_of.get(i, 0) >= 10]

    verdict = {
        "replay": os.path.basename(replay_path),
        "seat": seat,
        "n_obs": len(obs_list),
        "n_actions": len(actions),
        "n_mismatch": len(mm_steps),
        "first_mismatch": first_mm,
        "mismatch_after_d10": len(mm_after_d10),
        "match_rate": round(1.0 - len(mm_steps) / max(1, len(actions)), 4),
        "engaged": bool(loaded["evidence"].get("engaged")),
        "evidence": loaded["evidence"],
        "official_semantics_pins": [p for p, _ in OFFICIAL_SEMANTICS_PINS],
        "pkg_path": os.path.abspath(pkg_path),
        "pkg_sha256": hashlib.sha256(
            open(pkg_path, "rb").read()).hexdigest(),
    }
    return verdict


def main():
    ap = argparse.ArgumentParser(
        description="official get_last_callable production-load engagement "
                    "probe (P4.1)")
    ap.add_argument("--replay", default=DEFAULT_REPLAY)
    ap.add_argument("--seat", type=int, default=0)
    ap.add_argument("--max-steps", type=int, default=720)
    ap.add_argument("--out", default=os.path.join(OUT_DIR,
                                                  "official_load_probe.json"))
    args = ap.parse_args()
    verdict = run_probe(args.replay, seat=args.seat,
                        max_steps=args.max_steps)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as h:
        json.dump(verdict, h, ensure_ascii=False, indent=1)
    print(f"replay={verdict['replay']} seat={verdict['seat']} "
          f"n={verdict['n_actions']} match_rate={verdict['match_rate']:.1%} "
          f"n_mismatch={verdict['n_mismatch']} "
          f"first_mm={verdict['first_mismatch']} "
          f"mm_after_d10={verdict['mismatch_after_d10']}")
    ev = verdict["evidence"]
    for key in ("exec_dir_on_sys_path_after_load", "planner_in_sys_modules",
                "has_DTSP_RUNTIME_CONFIG", "has_DTSP_RUNTIME_MODULE",
                "PLANNER_ENABLED", "has_pristine_snapshot",
                "has_last_plan_key", "engaged"):
        print(f"  {key} = {ev.get(key)}")
    for err in (ev.get("hook_errors") or [])[:3]:
        print(f"  hook_error: {err}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
