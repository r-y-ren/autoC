"""gate_launch_fourgate_l1（R10 门④）：发射四门——重定向 v48_derivative_launch_check
单实现换包复用 + L1 专属附加断言（末 callable=_cxs_agent；与 _cxd_agent 基线的
完整序列差异仅来自截断层）。

四门（scripts/v48_derivative_launch_check.py 单实现，照 v48plus_launch_check.py
重定向先例改 check.DERIV_DIR/DERIV_MAIN/DERIV_TAR/OUT_DIR 四属性换包复用）：
  ①官方装载语义：干净 -I 子进程复刻 vendored kaggle_environments.agent
    .get_last_callable，真实引擎 obs 驱动零分歧；本门另断言末 callable=_cxs_agent；
  ②双席自打：seeds 101/102 全 720 回合 DONE 且每步 <1000ms；
  ③确定性：同 seed 重跑动作流 sha256 逐字节一致；
  ④包体+身份链：tar ≤100MB、成员恰 ["main.py"]、内层 main 与盘上一致、
    main/tar（及在场 layer 块）sha+bytes 对 build_manifest.json 核对全匹配。

附加断言（R10 验收④）：装载观测驱动对比 L1(_cxs_agent) vs verbatim(_cxd_agent)
动作序列——差异步全部 step≥648 且差异形态=BUY_SEED 整单消失（保序子序列、
非 market 槽位逐项相等）；非此形态即门红（阈值与 layer_s_block._CXS_FROM 同源）。

与先例的一处必要补充（round-30 台账 note_named_vs_last 同结论）：kgenv.arena
.load_submission_agent 有 named `agent` 优先分支，而 orderbook 系 main.py 的
named agent 是作者内层（层 D/S 之前）——发射门按官方语义一律走 last callable，
故四属性之外还重定向 check.load_deriv_agent 为本模块的官方语义装载器
（append → exec → pop → 最后 callable，与 -I 驱动器/装载锚点逐句同款）。

evidence：orderbook_l1_derivative/evidence/launch_check_evidence.json（格式沿
round-30 launch_check_evidence.json：gate1_official_load / gate2_full_episodes /
package 身份链）。任一门红或身份链不匹配 → passed=False（fail-closed；身份链
不匹配时早退，不对身份不明的包驱动长局）。"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tarfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                                   # kaggle_simulations/
SOFTWARE = os.path.dirname(KSIM)                               # legacy_software/
CHECK_PATH = os.path.join(SOFTWARE, "scripts",
                          "v48_derivative_launch_check.py")    # 四门单实现
VERBATIM_MAIN = os.path.join(KSIM, "orderbook_derivative",
                             "main.py")                        # _cxd_agent 基线包

SIZE_CAP_BYTES = 100 * 1024 * 1024        # 与单实现 SIZE_CAP_BYTES 同值
L1_LAST_CALLABLE = "_cxs_agent"
BASELINE_LAST_CALLABLE = "_cxd_agent"
DROPPED_DETAIL_CAP = 48                   # 附加断言逐差步明细上限（防台账膨胀）


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_last_callable(main_path: str):
    """官方 get_last_callable 语义装载：append → exec → pop → 最后 callable。

    不用 kgenv.arena.load_submission_agent：其 named `agent` 优先分支会取到
    orderbook 系作者内层（层 D/S 之前），非官方提交入口。装载不落 __pycache__
    （单实现 _no_bytecode 同款），exec 目录装载后即从 sys.path 弹出（锚点
    sys.path.pop() 同款）。
    """
    with open(main_path, "r", encoding="utf-8") as h:
        src = h.read()
    env = {}
    exec_dir = os.path.dirname(os.path.abspath(main_path))
    sys.path.append(exec_dir)
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        exec(compile(src, main_path, "exec"), env)
    finally:
        sys.path.pop()
        sys.dont_write_bytecode = old
    return [v for v in env.values() if callable(v)][-1]


class _Struct(dict):
    """kaggle_environments.utils.Struct 最小复刻（单实现 gate1 基线同款）。"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e


def _to_struct(obj):
    if isinstance(obj, dict):
        return _Struct({k: _to_struct(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_to_struct(v) for v in obj]
    return obj


def _redirect_check(pkg_path: str):
    """照 v48plus_launch_check 先例装载单实现并重定向（四属性+装载器）。"""
    spec = importlib.util.spec_from_file_location("l1_launch_check_base",
                                                  CHECK_PATH)
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    check.DERIV_DIR = pkg_path
    check.DERIV_MAIN = os.path.join(pkg_path, "main.py")
    check.DERIV_TAR = os.path.join(pkg_path, "submission.tar.gz")
    check.OUT_DIR = os.path.join(pkg_path, "evidence")
    check.TMP_DIR = os.path.join(pkg_path, "evidence", "tmp_launch")
    check.load_deriv_agent = lambda: _load_last_callable(check.DERIV_MAIN)
    return check


def _identity_chain(pkg_path: str) -> dict:
    """身份链：盘上 main/tar（及在场 layer 块）对 build_manifest.json 核对。"""
    manifest_path = os.path.join(pkg_path, "build_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as h:
        manifest = json.load(h)
    main_path = os.path.join(pkg_path, "main.py")
    tar_path = os.path.join(pkg_path, "submission.tar.gz")
    main_bytes = open(main_path, "rb").read()
    tar_bytes = open(tar_path, "rb").read()
    main_sha, tar_sha = _sha256(main_bytes), _sha256(tar_bytes)

    members, inner_ok = [], False
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        if members == ["main.py"]:
            inner_ok = tar.extractfile("main.py").read() == main_bytes

    def field(disk, key):
        want = manifest.get(key)
        return {"disk": disk, "manifest": want, "match": disk == want}

    chain = {
        "manifest_path": manifest_path,
        "main_sha256": field(main_sha, "main_sha256"),
        "main_bytes": field(len(main_bytes), "main_bytes"),
        "tar_sha256": field(tar_sha, "tar_sha256"),
        "tar_bytes": field(len(tar_bytes), "tar_bytes"),
        "tar_members": members,
        "tar_members_ok": members == ["main.py"],
        "tar_inner_main_matches_disk": inner_ok,
        "tar_size_ok": len(tar_bytes) <= SIZE_CAP_BYTES,
        "tar_size_mb": round(len(tar_bytes) / (1024 * 1024), 3),
    }
    block_path = os.path.join(pkg_path, "layer_s_block.py")
    if os.path.isfile(block_path):   # 可选面：层文件在场才交叉核对
        chain["block_sha256"] = field(_sha256(open(block_path, "rb").read()),
                                      "block_sha256")
    matches = [chain[k]["match"] for k in
               ("main_sha256", "main_bytes", "tar_sha256", "tar_bytes")]
    chain["candidate"] = manifest.get("candidate")
    chain["match"] = bool(all(matches) and chain["tar_members_ok"] and inner_ok
                          and chain.get("block_sha256", {"match": True})["match"])
    return chain


def _seed_drop_form(base_action, l1_action, norm_action):
    """差异形态判据：l1 == base 删去若干 BUY_SEED 整单（保序子序列、其余相等）。"""
    if not (isinstance(base_action, dict) and isinstance(l1_action, dict)):
        return False, "action 非 dict"
    if set(base_action) != set(l1_action):
        return False, "action 键集不同"
    for key in base_action:
        if key != "market" and norm_action(base_action[key]) != norm_action(l1_action[key]):
            return False, f"非 market 槽位 {key} 漂移"
    base_market, l1_market = base_action.get("market"), l1_action.get("market")
    if not (isinstance(base_market, list) and isinstance(l1_market, list)):
        return False, "market 非 list"
    j, dropped = 0, []
    for order in base_market:
        if j < len(l1_market) and norm_action(order) == norm_action(l1_market[j]):
            j += 1
        else:
            dropped.append(order)
    if j != len(l1_market):
        return False, "market 非保序子序列（含新增/改单）"
    for order in dropped:
        if not (isinstance(order, (list, tuple)) and len(order) >= 3
                and order[0] == "BUY_SEED"):
            return False, "删除订单含非 BUY_SEED 形态"
    return True, f"BUY_SEED 整单消失 x{len(dropped)}"


def _truncation_only_diff(check, obs_series) -> dict:
    """真实 obs 驱动 L1 vs verbatim（两包官方语义装载），差异仅截断层。

    与门①装载通道同输入（seed 101 局 seat0 obs 全序列）：两包各自 fresh 装载
    （官方每席独立装载语义），同一 obs 序列逐位驱动，逐步对比动作流；差异步
    应全部 step≥_CXS_FROM 且形态=BUY_SEED 整单消失。
    """
    import layer_s_block   # 阈值与上发代码同源（test_consts_crosscheck 看护）
    threshold = int(layer_s_block._CXS_FROM)

    l1_fn = _load_last_callable(check.DERIV_MAIN)
    base_fn = _load_last_callable(VERBATIM_MAIN)
    l1_name = getattr(l1_fn, "__name__", None)
    base_name = getattr(base_fn, "__name__", None)

    steps, violations, dropped_detail = [], [], []
    for raw in obs_series:
        step = int(raw.get("step", -1))
        try:
            a1 = l1_fn(_to_struct(raw))
            a0 = base_fn(_to_struct(raw))
        except Exception as exc:
            steps.append(step)
            violations.append({"step": step,
                               "detail": f"驱动异常 {type(exc).__name__}: {exc}"})
            continue
        if check.norm_action(a1) == check.norm_action(a0):
            continue
        steps.append(step)
        ok, detail = _seed_drop_form(a0, a1, check.norm_action)
        if ok:
            if len(dropped_detail) < DROPPED_DETAIL_CAP:
                dropped_detail.append({"step": step, "form": detail})
        else:
            violations.append({"step": step, "detail": detail})

    all_ge = all(s >= threshold for s in steps)
    ok = bool(l1_name == L1_LAST_CALLABLE
              and base_name == BASELINE_LAST_CALLABLE
              and all_ge and not violations)
    return {
        "ok": ok,
        "threshold": threshold,
        "n_obs": len(obs_series),
        "l1_main": check.DERIV_MAIN,
        "l1_callable": l1_name,
        "baseline_main": VERBATIM_MAIN,
        "baseline_callable": base_name,
        "divergent_steps": steps,
        "n_divergent": len(steps),
        "min_divergent_step": min(steps) if steps else None,
        "all_divergent_steps_ge_threshold": all_ge,
        "form_violations": violations,
        "dropped_detail": dropped_detail,
    }


def run(pkg_path=None) -> dict:
    """门④主入口：四门+附加断言；返回四门结果+证据路径。

    pkg_path=包目录（默认本目录）；从其 build_manifest.json 读期望 sha 做身份
    链核对。任一门红或身份链不匹配 → passed=False（fail-closed；身份链不匹配
    时早退，四门标记未驱动）。
    """
    t0 = time.perf_counter()
    pkg_path = os.path.abspath(pkg_path) if pkg_path is not None else HERE
    evidence_dir = os.path.join(pkg_path, "evidence")
    evidence_path = os.path.join(evidence_dir, "launch_check_evidence.json")
    gates = {"load": False, "full_episodes": False, "determinism": False,
             "package": False}
    truncation = {"ok": False, "divergent_steps": []}
    identity, g1, g23, errors = None, None, None, []
    early_exit = False

    os.makedirs(evidence_dir, exist_ok=True)

    # 身份链先行：不匹配即 fail-closed，不对身份不明的包驱动长局。
    try:
        identity = _identity_chain(pkg_path)
        gates["package"] = bool(identity["match"] and identity["tar_size_ok"])
    except (Exception, SystemExit) as exc:
        errors.append(f"identity_chain: {type(exc).__name__}: {exc}")
        identity = {"match": False, "candidate": None,
                    "note": "identity evaluation raised"}
        gates["package"] = False

    if not gates["package"]:
        early_exit = True
    else:
        check = _redirect_check(pkg_path)
        obs_series = None
        try:
            g23 = check.gate2_gate3()
            obs_series = g23.pop("_obs_series_seed101", None)
            gates["full_episodes"] = bool(g23["gate2_full_episodes_ok"])
            gates["determinism"] = bool(g23["gate3_determinism_ok"])
        except (Exception, SystemExit) as exc:
            errors.append(f"gate2_gate3: {type(exc).__name__}: {exc}")
            g23 = None
        if obs_series is not None:
            try:
                g1 = check.gate1(obs_series)
                ev1 = g1.get("evidence") or {}
                gates["load"] = bool(
                    g1.get("gate1_official_load_ok")
                    and ev1.get("last_callable_name") == L1_LAST_CALLABLE)
            except (Exception, SystemExit) as exc:
                errors.append(f"gate1: {type(exc).__name__}: {exc}")
                g1 = None
            finally:
                shutil.rmtree(check.TMP_DIR, ignore_errors=True)
            try:
                truncation = _truncation_only_diff(check, obs_series)
            except (Exception, SystemExit) as exc:
                errors.append(f"truncation_only_diff: {type(exc).__name__}: {exc}")
                truncation = {"ok": False, "divergent_steps": [],
                              "note": f"evaluation raised: {exc}"}

    passed = bool(all(gates.values()) and truncation.get("ok"))

    verdict = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol": "orderbook-l1-launch-fourgate/1.0",
        "candidate": identity.get("candidate"),
        "package": identity,
        "gate1_official_load": g1,
        "gate2_full_episodes": g23,
        "gates": gates,
        "last_callable_expected": L1_LAST_CALLABLE,
        "truncation_only_diff": truncation,
        "fail_closed_early_exit": early_exit,
        "errors": errors,
        "passed": passed,
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    with open(evidence_path, "w", encoding="utf-8") as h:
        json.dump(verdict, h, ensure_ascii=False, indent=1)

    return {
        "gates": gates,
        "truncation_only_diff": {"ok": truncation.get("ok", False),
                                 "divergent_steps": truncation.get(
                                     "divergent_steps", [])},
        "passed": passed,
        "evidence_path": evidence_path,
    }


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    result = run(argv[0] if argv else None)
    for name, ok in result["gates"].items():
        print(f"[gate] {name}: {'PASS' if ok else 'FAIL'}")
    trunc = result["truncation_only_diff"]
    steps = trunc["divergent_steps"]
    print(f"[extra] truncation_only_diff ok={trunc['ok']} "
          f"n_divergent={len(steps)} "
          f"min_step={min(steps) if steps else None}")
    print(f"passed = {result['passed']}")
    print(f"evidence -> {result['evidence_path']}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
