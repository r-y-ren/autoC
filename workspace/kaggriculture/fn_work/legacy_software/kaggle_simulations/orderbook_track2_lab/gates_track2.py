# -*- coding: utf-8 -*-
"""gates_track2：track2 三形态四门体检（gates_strongest 同口径；判决先行·不发射）。

四门：①装载 last-callable（outer=_hs_agent；inner/base=pet_any_demand_agent
不变）②双席 DONE+单步<1s（seeds 101/102 官方 kaggriculture 引擎完整局，
每步 <1000ms）③确定性双跑逐字节（同 seed 重跑动作流 sha256 一致）④体积
<100MB+sha 身份（tar 成员恰 ['main.py']、内层 main 与盘上一致、sha 对
build_manifest、三形态对基座/现 H1 字节关系）。

外加两读数（不占门）：语义平价探针（内生 _hy_post 与外挂 _X1._x1_post 在
随机合成动作上输出逐字一致=语义=X1 同）+ 卫生台账（每局 _X1_REPORT /
_S1009_REPORT.hyg 汇总）。动作流逐拍落盘（evidence/footprint/）供内生版
差异拍足迹审计（非目标拍零足迹）。

复用（不改写）：episode_trace.run_episode（v48 run_full_episode 同款+追踪）。
门内全跑不短路；任一门异常→该门 {passed:False, error}，overall 必红。
只写 orderbook_track2_lab/。
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import random
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM = str(MODULE_DIR.parent)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)
sys.path.insert(0, str(MODULE_DIR))

import episode_trace as et  # noqa: E402

RECORD_VERSION = "gates-track2/1.0"
EPISODE_SEEDS = (101, 102)
STEP_BUDGET_MS = et.STEP_BUDGET_MS
SIZE_CAP_BYTES = 100 * 1024 * 1024
FORMS = ("h1_outer", "h1_inner", "h1_base")
EXPECTED_ENTRY = {"h1_outer": "_hs_agent", "h1_inner": "pet_any_demand_agent",
                  "h1_base": "pet_any_demand_agent"}
BUILD = MODULE_DIR / "build"
EVID = MODULE_DIR / "evidence"
FOOT_DIR = EVID / "footprint"
H1_OUTER_SRC = (Path(KSIM) / "orderbook_strongest_lab" / "build" / "h1"
                / "main.py")
ADOPT_BASE = Path(KSIM) / "orderbook_haodou_adopt" / "submission.tar.gz"


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _base_bytes():
    with tarfile.open(fileobj=io.BytesIO(ADOPT_BASE.read_bytes()),
                      mode="r:gz") as tar:
        return tar.extractfile("main.py").read()


def _gate_load(form):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(str(BUILD / form / "main.py"))
    name = getattr(entry, "__name__", "")
    ok = name == EXPECTED_ENTRY[form]
    return {"passed": bool(ok), "entry": name,
            "expected": EXPECTED_ENTRY[form]}


def _gate_identity(form):
    pkg = BUILD / form
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    size_ok = len(tar_bytes) < SIZE_CAP_BYTES
    members_ok = members == ["main.py"]
    inner_ok = inner == main_bytes
    sha_ok = main_sha == man.get("main_sha256")
    base = _base_bytes()
    outer = H1_OUTER_SRC.read_bytes()
    if form == "h1_outer":
        rel_ok = main_bytes == outer
        rel = "字节恒等现 H1（外挂 X1 尾块）"
    elif form == "h1_base":
        rel_ok = main_bytes == base
        rel = "字节恒等采纳件基座（无卫生）"
    else:
        # 内生版：diff 圈禁=step1009 函数体块（前缀/后缀逐字恒等）
        sys.path.insert(0, str(MODULE_DIR))
        import build_track2 as bt  # noqa: WPS433
        i = base.decode("utf-8").index(bt.BLOCK_DEF)
        j = base.decode("utf-8").index(bt.BLOCK_END)
        src = main_bytes.decode("utf-8")
        ii = src.index(bt.BLOCK_DEF)
        jj = src.index(bt.BLOCK_END)
        rel_ok = (src[:ii] == base.decode("utf-8")[:i]
                  and src[jj:] == base.decode("utf-8")[j:]
                  and src.count(bt.BLOCK_DEF) == 1)
        rel = "diff 圈禁 step1009 函数体（前后缀逐字恒等；无尾块）"
    ok = all([size_ok, members_ok, inner_ok, sha_ok, rel_ok])
    return {"passed": bool(ok), "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "inner_matches_disk": inner_ok,
            "sha_matches_manifest": sha_ok, "base_relation": rel,
            "base_relation_ok": rel_ok}


def _gate_health(form, episodes):
    details = []
    ok = True
    for ep in episodes:
        statuses = list(ep.get("statuses") or [])
        rewards = list(ep.get("rewards") or [])
        good = (statuses == ["DONE", "DONE"] and len(rewards) == 2
                and all(_is_num(r) and abs(float(r)) < 1e12 for r in rewards)
                and _is_num(ep.get("max_step_ms"))
                and float(ep["max_step_ms"]) < STEP_BUDGET_MS
                and ep.get("turns_played") == et.FULL_STEPS)
        ok = ok and good
        details.append({"seed": ep.get("seed"), "statuses": statuses,
                        "turns_played": ep.get("turns_played"),
                        "max_step_ms": ep.get("max_step_ms"),
                        "p99_step_ms": ep.get("p99_step_ms"),
                        "mean_step_ms": ep.get("mean_step_ms"),
                        "wall_s": ep.get("wall_s"), "passed": good})
    return {"passed": bool(ok), "step_budget_ms": STEP_BUDGET_MS,
            "episodes": details}


def _gate_determinism(ep1, ep1b):
    h1 = ep1.get("action_stream_sha256")
    h2 = ep1b.get("action_stream_sha256")
    ok = bool(h1) and h1 == h2
    return {"passed": bool(ok), "rerun_seed": ep1.get("seed"),
            "hashes": {"run1": h1, "run2": h2}}


# ------------------------------------------------- 语义平价探针（非门） --
def _semantics_parity(n_cases=400, seed=20260929):
    """内生 _hy_post 与外挂 X1._x1_post 同输入同输出（语义=X1 同）。"""
    import importlib.util as _ilu
    x1_path = str(Path(KSIM) / "orderbook_strongest_lab" / "layer_x1.py")
    spec = _ilu.spec_from_file_location("track2_layer_x1", x1_path)
    x1 = _ilu.module_from_spec(spec)
    spec.loader.exec_module(x1)

    import build_track2 as bt  # noqa: WPS433

    holder = {"action": None}

    # 合成世界：投射仓=私仓（两边同 stub，隔离算法本身）
    class _StubChassisCfg:
        pass

    class _StubChassis:
        cfg = _StubChassisCfg()

        @staticmethod
        def _projected_shed(action, view):
            return dict(view.shed)

    class _StubImpl:
        chassis = _StubChassis()

    class _StubView:
        def __init__(self, obs, player, cfg):
            self.shed = dict(((obs or {}).get("private") or {})
                             .get("shed") or {})

    def stub_projected(obs, act):
        return dict(_StubView(obs, 0, None).shed)

    x1._xd7_projected = stub_projected

    ns = {
        "_S1009_REPORT": {"calls": 0, "changed": 0, "errors": 0},
        "_S1009_PARENT": lambda obs, cfg=None: holder["action"],
        "_s793_reorder": lambda obs, action: action,
        "_s834_key": lambda action: tuple(tuple(o) for o in
                                          (action.get("market") or [])),
        "_RACE_STATE": {},
        "_View": _StubView,
        "_IMPL": _StubImpl,
    }
    exec(compile(bt.WEAVED_BODY, "<parity:step1009>", "exec"), ns)
    inner_fn = ns["step1009_step1008_fortyfirst_final_fixedsell_closure_agent"]

    rng = random.Random(seed)
    ITEMS = ("WHEAT", "CARROT", "MILK", "EGG", "WOOL", "FERTILIZER")
    mismatch = []
    n_bad = 0
    for case in range(n_cases):
        step = rng.choice([0, 100, 623, 624, 625, 660, 700, 718, 719])
        shed = {it: rng.randint(0, 20) for it in ITEMS}
        market = []
        for _ in range(rng.randint(0, 10)):
            kind = rng.random()
            if kind < 0.55:
                market.append(["SELL", rng.choice(ITEMS),
                               rng.choice([0, -3, 1, 2, 5, 8, 30, 90,
                                           10.0, 7])])
            elif kind < 0.75:
                market.append(["BUY_PRODUCT", rng.choice(ITEMS),
                               rng.randint(1, 6)])
            elif kind < 0.85:
                market.append(["BUY_ANIMAL", rng.choice(("COW", "SHEEP")),
                               rng.randint(1, 2)])
            elif kind < 0.92:
                market.append([])
            else:
                market.append(["BUY_SEED", rng.choice(ITEMS), 3])
        obs = {"step": step, "player": 0,
               "private": {"shed": dict(shed)}, "market": {"prices": {}}}
        import copy as _copy
        mk1 = _copy.deepcopy(market)
        mk2 = _copy.deepcopy(market)
        got_outer = x1._x1_post(obs, {"farmer": ["PASS"], "hands": [],
                                      "market": mk1})
        holder["action"] = {"farmer": ["PASS"], "hands": [], "market": mk2}
        got_inner = inner_fn(obs, None)
        if (got_outer.get("market") or []) != (got_inner.get("market") or []):
            n_bad += 1
            if len(mismatch) < 5:
                mismatch.append({"case": case, "step": step,
                                 "in": market,
                                 "outer": got_outer.get("market"),
                                 "inner": got_inner.get("market")})
    return {"n_cases": n_cases, "seed": seed,
            "n_mismatch": n_bad, "mismatch_examples": mismatch,
            "passed": n_bad == 0}


def main():
    os.chdir(MODULE_DIR)
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {"commands": ["python3 orderbook_track2_lab/build_track2.py",
                                "python3 orderbook_track2_lab/gates_track2.py"],
                   "episode_seeds": list(EPISODE_SEEDS),
                   "runner": "episode_trace.run_episode（v48 run_full_episode"
                             " 同款+逐拍动作流）"},
        "forms": {},
    }
    overall_ok = True
    budget = {"gate_episodes": 0}
    for form in FORMS:
        pkg = str(BUILD / form)
        main_py = os.path.join(pkg, "main.py")
        res = {}
        t0 = time.perf_counter()
        try:
            res["load"] = _gate_load(form)
        except Exception as exc:
            res["load"] = {"passed": False, "error": repr(exc)[:200]}
        eps = []
        for tag, seed in (("s101", EPISODE_SEEDS[0]), ("s102", EPISODE_SEEDS[1]),
                          ("s101_rerun", EPISODE_SEEDS[0])):
            dump = str(FOOT_DIR / ("%s_%s.json" % (form, tag)))
            try:
                ep = et.run_episode(main_py, seed, dump_path=dump)
            except Exception as exc:
                ep = {"seed": seed, "error": repr(exc)[:200]}
            ep["tag"] = tag
            eps.append(ep)
            budget["gate_episodes"] += 1
            print(" ", form, tag, ep.get("statuses"), ep.get("turns_played"),
                  "max_ms", ep.get("max_step_ms"), ep.get("wall_s"), "s",
                  flush=True)
        ok_eps = [e for e in eps if "error" not in e]
        by_tag = {e.get("tag"): e for e in ok_eps}
        try:
            res["health"] = _gate_health(
                form, [by_tag[t] for t in ("s101", "s102") if t in by_tag])
        except Exception as exc:
            res["health"] = {"passed": False, "error": repr(exc)[:200]}
        try:
            if "s101" in by_tag and "s101_rerun" in by_tag:
                res["determinism"] = _gate_determinism(by_tag["s101"],
                                                       by_tag["s101_rerun"])
            else:
                res["determinism"] = {"passed": False, "error": "rerun 局缺失"}
        except Exception as exc:
            res["determinism"] = {"passed": False, "error": repr(exc)[:200]}
        try:
            res["identity"] = _gate_identity(form)
        except Exception as exc:
            res["identity"] = {"passed": False, "error": repr(exc)[:200]}
        for e in eps:
            e.pop("seats", None)
        res["hygiene_reports"] = [e.get("hygiene_reports") for e in ok_eps]
        passed = all(g.get("passed") for g in res.values()
                     if isinstance(g, dict) and "passed" in g)
        overall_ok = overall_ok and passed
        res["overall"] = passed
        res["elapsed_s"] = round(time.perf_counter() - t0, 1)
        out["forms"][form] = res
        print(form, "gates:", {k: v.get("passed") for k, v in res.items()
                               if isinstance(v, dict) and "passed" in v},
              "overall", passed, flush=True)

    # ---- 语义平价探针（内生=外挂同语义；非门，读数） ----
    try:
        out["semantics_parity"] = _semantics_parity()
    except Exception as exc:
        out["semantics_parity"] = {"passed": False, "error": repr(exc)[:300]}
    print("semantics parity:", out["semantics_parity"].get("passed"),
          out["semantics_parity"].get("n_mismatch"), flush=True)

    out["overall_passed"] = overall_ok
    out["budget"] = budget
    (EVID / "gates.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("OVERALL gates passed:", overall_ok, "budget:", budget, flush=True)


if __name__ == "__main__":
    main()
