# 【中文】v48_derivative_launch_check.py —— v48 公开衍生版打包+四道发射验证
# ===========================================================================
# 背景：用户裁决（2026-09-21，brainstorming 硬门+AskUserQuestion）提交 v48/V50
#   系公开衍生版占终榜跟踪位。合规：host Addison Howard 2026-08-28 明文
#   "Anything freely and publicly available is fair use."
#   （references/digests/web-comp-intel-2026-09-19.md §3）；v48 notebook
#   2026-08-31 拉回（共享锁 09-23 之前），使用已公开代码不受锁约束。
# 本脚本四道门（全过才可发射）：
#   ①官方装载语义：干净 -I 子进程复刻 vendored kaggle_environments.agent
#     .get_last_callable（sys.path.append(exec_dir) → exec(src, env) →
#     sys.path.pop() → env 最后 callable），用真实引擎 obs 序列驱动装载出的
#     callable，全程无异常，且与主进程 fresh 装载动作流逐字节一致；
#   ②短局实测：官方引擎（vendored 1.32.7+nodeps）2 局完整 720 回合
#     （v48 双席位自打，seeds 101/102），statuses 双 DONE、rewards 有限、
#     每步 agent 耗时最大值 < 1000ms（官方 1s 预算）；
#   ③确定性：同 seed 同席位重跑，双席 720 步动作流哈希逐字节一致；
#   ④包体：submission.tar.gz ≤ 100MB（单 main.py，预期 ~82KB）。
# 包构建：从 references/data/intel-notebooks/v48build/main.py（解码真源码，
#   sha256 dadee25a…2664a）逐字复制，确定性 tar（mtime=0/uid=gid=0/mode 0644，
#   gzip mtime=0），双次构建字节一致（可复现审计）。
# 输出：exports/probes/v48_launch/v48_derivative_launch_check.json
# CLI：python scripts/v48_derivative_launch_check.py [--keep-tmp]
# ===========================================================================
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
ROOT = os.path.dirname(SOFTWARE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

SRC_MAIN = os.path.join(ROOT, "references", "data", "intel-notebooks",
                        "v48build", "main.py")
DERIV_DIR = os.path.join(SOFTWARE, "kaggle_simulations", "v48_derivative")
DERIV_MAIN = os.path.join(DERIV_DIR, "main.py")
DERIV_TAR = os.path.join(DERIV_DIR, "submission.tar.gz")
OUT_DIR = os.path.join(SOFTWARE, "exports", "probes", "v48_launch")
TMP_DIR = os.path.join(OUT_DIR, "tmp")

STEP_BUDGET_MS = 1000.0        # 官方每步 1s 预算
SIZE_CAP_BYTES = 100 * 1024 * 1024   # Kaggle 包上限 100MB
FULL_STEPS = 720               # 24 turns x 30 days
EPISODE_SEEDS = (101, 102)     # 与 h2h_v48 基线同种子域
OBS_JSON_CAP = 32 * 1024 * 1024     # obs 序列 JSON 上限，超出则均匀抽样
OBS_SAMPLE_N = 240

OFFICIAL_SEMANTICS_PINS = (
    ("sys.path.append(exec_dir)", "exec 前 append 解包目录"),
    ("sys.path.pop()", "exec 后 pop 移除解包目录"),
    ("[v for v in env.values() if callable(v)][-1]", "取最后 callable"),
)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm_action(a) -> str:
    """动作规范化串（与 p41/stepdiff 同口径，跨端可比）。"""
    if isinstance(a, (list, tuple)):
        return "[" + ",".join(norm_action(x) for x in a) + "]"
    if isinstance(a, dict):
        return "{" + ",".join(f"{k}:{norm_action(a[k])}"
                              for k in sorted(a)) + "}"
    if isinstance(a, float):
        return f"{a:.4f}"
    return json.dumps(a, ensure_ascii=False, sort_keys=True)


def action_stream_hash(seat_actions) -> str:
    parts = []
    for seat in (0, 1):
        for act in seat_actions[seat]:
            parts.append(norm_action(act))
    return sha256_bytes("\n".join(parts).encode("utf-8"))


# --------------------------------------------------------------------------
# 包构建（确定性 tar，双次构建字节一致）
# --------------------------------------------------------------------------
def build_tar_bytes(main_bytes: bytes) -> bytes:
    buf = io.BytesIO()
    gz = gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0)
    with tarfile.open(fileobj=gz, mode="w") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main_bytes)
        info.mode = 0o644
        info.mtime = 0
        info.uid = 0
        info.gid = 0
        tar.addfile(info, io.BytesIO(main_bytes))
    gz.close()   # 写 gzip trailer（tarfile 不代管传入的 fileobj）
    return buf.getvalue()


def build_package() -> dict:
    src_bytes = open(SRC_MAIN, "rb").read()
    src_sha = sha256_bytes(src_bytes)

    os.makedirs(DERIV_DIR, exist_ok=True)
    shutil.rmtree(os.path.join(DERIV_DIR, "__pycache__"),
                  ignore_errors=True)
    with open(DERIV_MAIN, "wb") as h:
        h.write(src_bytes)
    written = open(DERIV_MAIN, "rb").read()
    assert written == src_bytes, "DERIV main.py 与源字节不一致"

    tar1 = build_tar_bytes(src_bytes)
    tar2 = build_tar_bytes(src_bytes)
    assert tar1 == tar2, "tar.gz 双次构建不一致（非可复现）"
    with open(DERIV_TAR, "wb") as h:
        h.write(tar1)

    # 解包校验：单成员 main.py，内容逐字节一致
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as t:
        names = t.getnames()
        inner = t.extractfile("main.py").read()
    assert names == ["main.py"], f"tar 成员异常: {names}"
    assert inner == src_bytes, "tar 内 main.py 与源字节不一致"

    return {
        "src_main_sha256": src_sha,
        "src_main_bytes": len(src_bytes),
        "tar_sha256": sha256_bytes(tar1),
        "tar_bytes": len(tar1),
        "tar_members": names,
        "tar_rebuild_reproducible": True,
        "gate4_size_ok": len(tar1) <= SIZE_CAP_BYTES,
        "gate4_size_mb": round(len(tar1) / (1024 * 1024), 3),
    }


# --------------------------------------------------------------------------
# 门②/③：官方引擎完整局 + 每步计时 + 确定性
# --------------------------------------------------------------------------
class TimedAgent:
    """包装 agent：记录每次调用耗时（ms），不改行为。"""

    def __init__(self, fn, timings):
        self._fn = fn
        self._timings = timings

    def __call__(self, obs, configuration=None):
        t0 = time.perf_counter()
        try:
            return self._fn(obs, configuration)
        finally:
            self._timings.append((time.perf_counter() - t0) * 1000.0)


import contextlib


@contextlib.contextmanager
def _no_bytecode():
    """spec 装载不落 __pycache__（保持交付目录只有 main.py + tar.gz）。"""
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        yield
    finally:
        sys.dont_write_bytecode = old


def load_deriv_agent():
    from kgenv.arena import load_submission_agent   # get_last_callable 同语义
    with _no_bytecode():
        return load_submission_agent(DERIV_MAIN)


def run_full_episode(seed: int) -> dict:
    """单局：v48 双席位自打（计时包装），官方引擎 720 回合。"""
    from kaggle_environments import make

    timings = ([], [])
    agents = [TimedAgent(load_deriv_agent(), timings[0]),
              TimedAgent(load_deriv_agent(), timings[1])]
    t0 = time.perf_counter()
    env = make("kaggriculture",
               configuration={"episodeSteps": FULL_STEPS, "seed": int(seed),
                              "actTimeout": 60.0},
               debug=True)
    env.run([agents[0], agents[1]])
    elapsed = time.perf_counter() - t0

    final = env.steps[-1]
    rewards = [float(s["reward"]) for s in final]
    statuses = [s["status"] for s in final]
    turns_played = len(env.steps)          # kgenv 口径：含初始态，== episodeSteps

    seat_actions = [[], []]
    obs_series = []
    for index in range(1, len(env.steps)):
        for seat in (0, 1):
            seat_actions[seat].append(env.steps[index][seat].get("action")
                                      or {})
        obs_series.append(env.steps[index][0].get("observation") or {})

    # debug=True 时 env.logs 是逐步执行元数据（duration/stdout/stderr，stderr
    # 空即无错）；真正的错误信号 = status != DONE 或日志含 ERROR/Timed out/
    # 非空 stderr。只保留可疑行，不灌全量日志。
    raw_logs = [str(line) for line in getattr(env, "logs", []) if line]
    suspicious = [s[:300] for s in raw_logs
                  if "ERROR" in s or "Timed out" in s
                  or "Traceback" in s]

    all_t = sorted(timings[0] + timings[1])
    n_calls = len(all_t)

    def pct(p):
        return all_t[min(n_calls - 1, int(n_calls * p))] if n_calls else 0.0

    return {
        "seed": seed,
        "statuses": statuses,
        "rewards": rewards,
        "turns_played": turns_played,
        "agent_action_steps": turns_played - 1,
        "n_engine_log_lines": len(raw_logs),
        "suspicious_log_lines": suspicious,
        "wall_s": round(elapsed, 1),
        "agent_calls": n_calls,
        "max_step_ms": round(all_t[-1], 2) if all_t else None,
        "p99_step_ms": round(pct(0.99), 2),
        "mean_step_ms": round(sum(all_t) / n_calls, 2) if n_calls else None,
        "action_stream_sha256": action_stream_hash(seat_actions),
        "obs_series": obs_series,
    }


def gate2_gate3() -> dict:
    ep1 = run_full_episode(EPISODE_SEEDS[0])     # seed 101（obs 供门①）
    ep2 = run_full_episode(EPISODE_SEEDS[1])     # seed 102
    ep1b = run_full_episode(EPISODE_SEEDS[0])    # seed 101 重跑（确定性）

    obs_seed101 = ep1.pop("obs_series")
    ep1["obs_count"] = len(obs_seed101)
    ep2["obs_count"] = len(ep2.pop("obs_series") or [])
    ep1b["obs_count"] = len(ep1b.pop("obs_series") or [])
    episodes = [ep1, ep2, ep1b]

    gate2_ok = all(
        ep["statuses"] == ["DONE", "DONE"]
        and ep["turns_played"] == FULL_STEPS
        and ep["max_step_ms"] is not None and ep["max_step_ms"] < STEP_BUDGET_MS
        and not ep["suspicious_log_lines"]
        for ep in episodes[:2]
    ) and all(abs(r) < 1e12 for ep in episodes[:2] for r in ep["rewards"])

    gate3_ok = (episodes[0]["action_stream_sha256"]
                == episodes[2]["action_stream_sha256"])

    return {
        "gate2_full_episodes_ok": gate2_ok,
        "gate2_step_budget_ms": STEP_BUDGET_MS,
        "gate2_episodes": episodes[:2],
        "gate3_determinism_ok": gate3_ok,
        "gate3_rerun_seed": EPISODE_SEEDS[0],
        "gate3_hashes": {"run1": episodes[0]["action_stream_sha256"],
                         "run2": episodes[2]["action_stream_sha256"]},
        "_obs_series_seed101": obs_seed101,
    }


# --------------------------------------------------------------------------
# 门①：干净 -I 子进程官方装载语义（p41 方法）
# --------------------------------------------------------------------------
DRIVER_SRC = '''
"""官方语义装载驱动器：append -> exec -> pop -> 最后 callable（-I 隔离）。"""
import json, sys


class _Struct(dict):
    """kaggle_environments.utils.Struct 最小复刻：dict + 属性访问。"""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e


def to_struct(obj):
    """递归包装：dict -> _Struct（引擎喂给 agent 的 obs 即属性可访问形态）。"""
    if isinstance(obj, dict):
        return _Struct({k: to_struct(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [to_struct(v) for v in obj]
    return obj


pkg_dir, obs_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(pkg_dir + "/main.py", "r", encoding="utf-8") as h:
    src = h.read()

stdlib_before = set(sys.modules)
env = {}
exec_dir = pkg_dir

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
    exec(compile(src, pkg_dir + "/main.py", "exec"), env)
finally:
    sys.path.pop()

callables = [v for v in env.values() if callable(v)]
last = callables[-1]
agent_named = env.get("agent")

with open(obs_path, "r", encoding="utf-8") as h:
    obs_list = json.load(h)

actions, errors = [], []
for raw in obs_list:
    obs = to_struct(raw)
    try:
        actions.append(last(obs))
    except Exception as e:
        errors.append({"i": len(actions), "error": repr(e)})
        actions.append(None)

named_probe_ok = None
if callable(agent_named) and obs_list:
    try:
        a1 = last(to_struct(obs_list[0]))
        a2 = agent_named(to_struct(obs_list[0]))
        named_probe_ok = json.dumps(a1, sort_keys=True) == json.dumps(
            a2, sort_keys=True)
    except Exception as e:
        named_probe_ok = f"error: {repr(e)}"

new_modules = [k for k in sys.modules if k not in stdlib_before]
non_stdlib_suspects = [
    k for k, m in sys.modules.items()
    if k not in stdlib_before
    and getattr(m, "__file__", None) is not None
    and not str(m.__file__).startswith("<bundled")
    and k.split(".")[0] not in sys.stdlib_module_names
]

evidence = {
    "n_callables": len(callables),
    "last_callable_name": getattr(last, "__name__", None),
    "has_named_agent": callable(agent_named),
    "named_agent_same_output_as_last": named_probe_ok,
    "loader_pop_applied": loader_pop_applied,
    "exec_dir_on_sys_path_after_load": exec_dir in sys.path,
    "n_new_sys_modules": len(new_modules),
    "non_stdlib_imports": non_stdlib_suspects,
    "action_errors": errors,
    "n_obs": len(obs_list),
    "n_actions": len(actions),
}

with open(out_path, "w", encoding="utf-8") as h:
    json.dump({"actions": actions, "evidence": evidence}, h,
              ensure_ascii=False)
'''


def check_official_semantics_pins() -> str:
    import kaggle_environments.agent as k_agent
    with open(k_agent.__file__, "r", encoding="utf-8") as h:
        src = h.read()
    missing = [name for pin, name in OFFICIAL_SEMANTICS_PINS if pin not in src]
    if missing:
        raise SystemExit(f"FAIL 本机 kaggle_environments.agent 装载语义锚点"
                         f"缺失: {missing}")
    return k_agent.__file__


def gate1(obs_series) -> dict:
    agent_py = check_official_semantics_pins()

    if os.path.isdir(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR)
    extract_dir = os.path.join(TMP_DIR, "pkg")
    os.makedirs(extract_dir)
    with tarfile.open(DERIV_TAR, "r:gz") as tar:
        tar.extractall(extract_dir)          # 模拟官方后端解包

    # obs 序列：全量或（超限时）均匀抽样，保证驱动/基线同输入
    payload = json.dumps(obs_series, ensure_ascii=False)
    if len(payload.encode("utf-8")) > OBS_JSON_CAP:
        step = max(1, len(obs_series) // OBS_SAMPLE_N)
        obs_series = obs_series[::step][:OBS_SAMPLE_N]
        payload = json.dumps(obs_series, ensure_ascii=False)
    obs_path = os.path.join(TMP_DIR, "obs.json")
    with open(obs_path, "w", encoding="utf-8") as h:
        h.write(payload)

    driver_path = os.path.join(TMP_DIR, "driver", "driver.py")
    os.makedirs(os.path.dirname(driver_path))
    with open(driver_path, "w", encoding="utf-8") as h:
        h.write(DRIVER_SRC)
    out_path = os.path.join(TMP_DIR, "out.json")

    t0 = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, "-I", driver_path, extract_dir, obs_path, out_path],
        capture_output=True, text=True, timeout=900)
    wall_s = round(time.perf_counter() - t0, 1)
    if proc.returncode != 0:
        raise SystemExit(f"FAIL 门① 驱动子进程退出 {proc.returncode}\n"
                         f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
    with open(out_path, "r", encoding="utf-8") as h:
        loaded = json.load(h)

    # 主进程 fresh 装载基线（同一 obs 序列）——包内驱动 vs 本地基线逐字节比对
    baseline_fn = load_deriv_agent()

    class _Struct(dict):
        def __getattr__(self, name):
            try:
                return self[name]
            except KeyError as e:
                raise AttributeError(name) from e

    def to_struct(obj):
        if isinstance(obj, dict):
            return _Struct({k: to_struct(v) for k, v in obj.items()})
        if isinstance(obj, list):
            return [to_struct(v) for v in obj]
        return obj

    baseline_actions = [baseline_fn(to_struct(raw)) for raw in obs_series]

    mismatches = [
        i for i, (mine, base) in enumerate(
            zip(loaded["actions"], baseline_actions))
        if norm_action(mine) != norm_action(base)
    ]

    ev = loaded["evidence"]
    gate1_ok = (
        ev["n_actions"] == len(obs_series)
        and not ev["action_errors"]
        and ev["last_callable_name"] is not None
        and ev["named_agent_same_output_as_last"] is True
        and not ev["non_stdlib_imports"]
        and not mismatches
    )
    return {
        "gate1_official_load_ok": gate1_ok,
        "agent_py_checked": agent_py,
        "driver_wall_s": wall_s,
        "n_obs_replayed": len(obs_series),
        "obs_subsampled": len(obs_series) < 720,
        "isolated_vs_local_action_mismatches": len(mismatches),
        "evidence": ev,
    }


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="v48 public-derivative package build + 4-gate launch "
                    "check")
    ap.add_argument("--keep-tmp", action="store_true")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    t0 = time.perf_counter()
    pkg = build_package()
    print(f"[build] main.py {pkg['src_main_bytes']}B sha256="
          f"{pkg['src_main_sha256'][:12]}…  tar.gz {pkg['tar_bytes']}B "
          f"sha256={pkg['tar_sha256'][:12]}…  "
          f"size_ok={pkg['gate4_size_ok']}", flush=True)

    g23 = gate2_gate3()
    obs_seed101 = g23.pop("_obs_series_seed101", None)
    for ep in g23["gate2_episodes"]:
        print(f"[gate2] seed={ep['seed']} statuses={ep['statuses']} "
              f"turns={ep['turns_played']} rewards="
              f"[{ep['rewards'][0]:.0f},{ep['rewards'][1]:.0f}] "
              f"max_step={ep['max_step_ms']}ms p99={ep['p99_step_ms']}ms "
              f"mean={ep['mean_step_ms']}ms wall={ep['wall_s']}s",
              flush=True)
    print(f"[gate3] seed101 run1={g23['gate3_hashes']['run1'][:12]}… "
          f"run2={g23['gate3_hashes']['run2'][:12]}… "
          f"determinism_ok={g23['gate3_determinism_ok']}", flush=True)

    g1 = gate1(obs_seed101)
    ev = g1["evidence"]
    print(f"[gate1] last_callable={ev['last_callable_name']} "
          f"n_obs={g1['n_obs_replayed']} mismatches="
          f"{g1['isolated_vs_local_action_mismatches']} "
          f"non_stdlib={ev['non_stdlib_imports']} "
          f"loader_pop={ev['loader_pop_applied']} "
          f"wall={g1['driver_wall_s']}s", flush=True)

    verdict = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "package": pkg,
        "gate1_official_load": g1,
        "gate2_full_episodes": g23,
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    verdict["all_gates_pass"] = bool(
        g1["gate1_official_load_ok"]
        and g23["gate2_full_episodes_ok"]
        and g23["gate3_determinism_ok"]
        and pkg["gate4_size_ok"])

    out = os.path.join(OUT_DIR, "v48_derivative_launch_check.json")
    with open(out, "w", encoding="utf-8") as h:
        json.dump(verdict, h, ensure_ascii=False, indent=1)

    if not args.keep_tmp:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

    print(f"all_gates_pass = {verdict['all_gates_pass']}")
    print(f"out -> {out}")
    return 0 if verdict["all_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
