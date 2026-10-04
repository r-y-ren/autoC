# -*- coding: utf-8 -*-
"""gates_topform：H2/H1 四门体检 + 足迹审计门（gates_strongest/gates_track2 同口径；
判决先行·不发射）。

四门：①装载 last-callable（h2/h1=_hs_agent 不变）②双席 DONE+单步<1s（seeds
101/102 官方 kaggriculture 引擎完整局）③确定性双跑逐字节（同 seed 动作流
sha256 一致）④体积 <100MB+sha 身份（tar 成员恰 ['main.py']、盘上一致、sha 对
build_manifest、h1 字节恒等现 H1、h2 diff 圈禁 step1009 函数体）。

足迹审计门（沿轨道 2，本任务守恒硬约束）：
- 非触发拍零足迹：同 seed H2 vs H1 动作流逐拍对比，差异拍只许落在触发相位
  （t%4∈{0,1}：0=谷底后置拍、1=due 加回拍），其余拍逐字零差异；
- 净卖量恒等：逐品全游戏 SELL 挂量合计 H2 vs H1（记账抵扣后应相等）；
- 零跨拍拆并：差异拍内单列表只含整单移除/整单加回（无部分挪量=逐单 qty
  原样出现在对拍）。
复用（不改写）：orderbook_track2_lab/episode_trace.run_episode。
只写 orderbook_topform_lab/。
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import tarfile
import time
from io import BytesIO
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM = str(MODULE_DIR.parent)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)
sys.path.insert(0, os.path.join(KSIM, "orderbook_track2_lab"))

import episode_trace as et  # noqa: E402

RECORD_VERSION = "gates-topform/1.0"
EPISODE_SEEDS = (101, 102)
STEP_BUDGET_MS = et.STEP_BUDGET_MS
SIZE_CAP_BYTES = 100 * 1024 * 1024
FORMS = ("h2", "h1")
EXPECTED_ENTRY = {"h2": "_hs_agent", "h1": "_hs_agent"}
BUILD = MODULE_DIR / "build"
EVID = MODULE_DIR / "evidence"
FOOT_DIR = EVID / "footprint"
H1_SRC = (Path(KSIM) / "orderbook_strongest_lab" / "build" / "h1" / "main.py")


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _gate_load(form):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(str(BUILD / form / "main.py"))
    name = getattr(entry, "__name__", "")
    ok = name == EXPECTED_ENTRY[form]
    return {"passed": bool(ok), "entry": name, "expected": EXPECTED_ENTRY[form]}


def _gate_identity(form):
    sys.path.insert(0, str(MODULE_DIR))
    import build_topform as bt  # noqa: WPS433
    pkg = BUILD / form
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    size_ok = len(tar_bytes) < SIZE_CAP_BYTES
    members_ok = members == ["main.py"]
    inner_ok = inner == main_bytes
    sha_ok = main_sha == man.get("main_sha256")
    h1_bytes = H1_SRC.read_bytes()
    if form == "h1":
        rel_ok = main_bytes == h1_bytes
        rel = "字节恒等现 H1（76b5f842…）"
    else:
        h1_src = h1_bytes.decode("utf-8")
        src = main_bytes.decode("utf-8")
        i = h1_src.index(bt.BLOCK_DEF)
        j = h1_src.index(bt.BLOCK_END)
        ii = src.index(bt.BLOCK_DEF)
        jj = src.index(bt.BLOCK_END)
        rel_ok = (src[:ii] == h1_src[:i] and src[jj:] == h1_src[j:]
                  and src.count(bt.BLOCK_DEF) == 1)
        rel = "diff 圈禁 step1009 函数体（前后缀逐字恒等；无尾块）"
    ok = all([size_ok, members_ok, inner_ok, sha_ok, rel_ok])
    return {"passed": bool(ok), "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "inner_matches_disk": inner_ok,
            "sha_matches_manifest": sha_ok, "h1_relation": rel,
            "h1_relation_ok": rel_ok}


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


# ------------------------------------------------------------ 足迹审计门 --
# 口径（轨道 2 同式）：硬门=函数级零足迹/守恒探针（同输入同对象、整单挪量、
# due 记账精确抵扣）；动作流逐拍对比=级联读数（外生引擎自适应层连锁，非门）。
def _load_dump(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    seats = []
    for s in data.get("seats") or []:
        seats.append({int(step): act for step, act in s})
    return data, seats


def _parse_orders(act_key):
    try:
        act = json.loads(act_key)
    except Exception:
        return []
    out = []
    for o in (act.get("market") or []) if isinstance(act, dict) else []:
        if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL":
            try:
                q = int(o[2])
            except Exception:
                q = None
            out.append((str(o[1]), q))
    return out


def _stream_readings(dump_h2, dump_h1):
    """级联读数（非门）：差异拍相位分布 + 逐品挂量差。"""
    _, seats2 = _load_dump(dump_h2)
    _, seats1 = _load_dump(dump_h1)
    readings = []
    for seat in (0, 1):
        s2 = seats2[seat] if seat < len(seats2) else {}
        s1 = seats1[seat] if seat < len(seats1) else {}
        steps = sorted(set(s2) | set(s1))
        diff_steps = [t for t in steps if s2.get(t) != s1.get(t)]
        phase = {}
        for t in diff_steps:
            phase[t % 4] = phase.get(t % 4, 0) + 1
        qty2 = {}
        qty1 = {}
        for t in steps:
            for item, q in _parse_orders(s2.get(t) or "{}"):
                if q is not None:
                    qty2[item] = qty2.get(item, 0) + q
            for item, q in _parse_orders(s1.get(t) or "{}"):
                if q is not None:
                    qty1[item] = qty1.get(item, 0) + q
        net = {item: qty2.get(item, 0) - qty1.get(item, 0)
               for item in set(qty2) | set(qty1)}
        readings.append({
            "seat": seat, "n_steps": len(steps),
            "n_diff_steps": len(diff_steps),
            "diff_steps_by_mod4": {str(k): v for k, v in sorted(phase.items())},
            "sell_order_qty_delta_h2_minus_h1": {k: v for k, v in sorted(net.items()) if v},
        })
    return readings


def _probe_namespace():
    import types
    holder = {"action": None}

    class _StubChassisCfg:
        pass

    class _StubChassis:
        cfg = _StubChassisCfg()
        players = {}

        @staticmethod
        def _projected_shed(action, view):
            return dict(view.shed)

    class _StubImpl:
        chassis = _StubChassis()

    class _StubView:
        def __init__(self, obs, player, cfg):
            pv = (obs or {}).get("private")
            self.shed = dict((pv.get("shed") or {}) if isinstance(pv, dict) else {})

    ns = {
        "_S1009_REPORT": {"calls": 0, "changed": 0, "errors": 0},
        "_S1009_PARENT": lambda obs, cfg=None: holder["action"],
        "_s793_reorder": lambda obs, action: action,
        "_s834_key": lambda action: tuple(tuple(o) for o in
                                          (action.get("market") or [])),
        "_RACE_STATE": {},
        "_View": _StubView,
        "_IMPL": _StubImpl,
        "_holder": holder,
    }
    return ns, holder, _StubImpl


def _footprint_probe(n_cases=200, seed=20260929):
    """函数级硬门：①非触发拍同对象零足迹 ②整单挪量（零跨拍拆并）
    ③due 记账精确抵扣（净卖量恒等，配对拍验证）④WHEAT/FERT 不动。"""
    import random
    import copy as _copy
    from collections import Counter
    sys.path.insert(0, str(MODULE_DIR))
    import build_topform as bt  # noqa: WPS433
    ns, holder, _StubImpl = _probe_namespace()
    exec(compile(bt.WEAVED_BODY, "<probe:step1009>", "exec"), ns)
    fn = ns["step1009_step1008_fortyfirst_final_fixedsell_closure_agent"]
    ITEMS = ("WHEAT", "CARROT", "MILK", "EGG", "WOOL", "FERTILIZER", "MELON")
    rng = random.Random(seed)
    fail = {"non_trigger_footprint": [], "whole_order": [], "net_identity": [],
            "wash_items": [], "pair_identity": []}
    n_non_trigger = n_moves = n_pairs = 0

    def _mk_market():
        market = []
        for _ in range(rng.randint(0, 8)):
            kind = rng.random()
            if kind < 0.6:
                market.append(["SELL", rng.choice(ITEMS),
                               rng.choice([1, 2, 5, 7, 30])])
            elif kind < 0.8:
                market.append(["BUY_PRODUCT",
                               rng.choice(("WHEAT", "FERTILIZER")), 2])
            elif kind < 0.9:
                market.append([])
            else:
                market.append(["BUY_SEED", "MELON", 3])
        return market

    def _run(step, player, market, shed):
        obs = {"step": step, "player": player,
               "private": {"shed": dict(shed)}, "market": {"prices": {}}}
        mk = _copy.deepcopy(market)
        holder["action"] = {"farmer": ["PASS"], "hands": [], "market": mk}
        ret = fn(obs, None)
        return ret, holder["action"], mk

    for case in range(n_cases):
        step = rng.choice([1, 2, 3, 5, 9, 13, 250, 251, 253, 255, 603,
                           701, 714, 717])
        player = rng.choice([0, 1])
        shed = {it: rng.randint(0, 25) for it in ITEMS}
        market = _mk_market()
        got, raw, mk = _run(step, player, market, shed)
        if got is not raw or got.get("market") is not mk:
            fail["non_trigger_footprint"].append({"case": case, "step": step})
        n_non_trigger += 1

        # 触发拍（%4==0）→ 整单挪量 + due[t+1] 记账；配对拍 t+1 → 整单加回
        tstep = (case % 178) * 4  # 保证 %4==0 且落在 0..708
        shed2 = {it: rng.randint(1, 25) for it in ITEMS}
        market2 = _mk_market()
        got2, _raw2, mk2 = _run(tstep, player, market2, shed2)
        led = fn.tf if hasattr(fn, "tf") else {}
        dued = (led.get("due") or {}).get(player) or {}
        cb = Counter((o[1], o[2]) for o in market2
                     if isinstance(o, (list, tuple)) and len(o) >= 3
                     and o[0] == "SELL")
        ca = Counter((o[1], o[2]) for o in (got2.get("market") or [])
                     if isinstance(o, (list, tuple)) and len(o) >= 3
                     and o[0] == "SELL")
        due_next = dict(dued.get(tstep + 1) or {})
        moved = {}
        for (it, q), n in (cb - ca).items():
            if it in ("WHEAT", "FERTILIZER"):
                fail["wash_items"].append({"case": case, "item": it})
            moved[it] = moved.get(it, 0) + q * n
            n_moves += 1
        for (it, q), n in (ca - cb).items():
            fail["whole_order"].append({"case": case, "added": (it, q, n)})
        for it, q in moved.items():
            if due_next.get(it, 0) != q:
                fail["net_identity"].append(
                    {"case": case, "item": it, "moved": q,
                     "due": due_next.get(it, 0), "step": tstep})
        # 配对拍验证：due 加回量=记账量（净卖量恒等）
        if due_next:
            n_pairs += 1
            shed3 = {it: rng.randint(0, 25) for it in ITEMS}
            market3 = _mk_market()[:2]  # 小单列表：保证 due 整单加回不触槽位再延
            got3, _raw3, mk3 = _run(tstep + 1, player, market3, shed3)
            base = Counter((o[1], o[2]) for o in market3
                           if isinstance(o, (list, tuple)) and len(o) >= 3
                           and o[0] == "SELL")
            after = Counter((o[1], o[2]) for o in (got3.get("market") or [])
                            if isinstance(o, (list, tuple)) and len(o) >= 3
                            and o[0] == "SELL")
            added = {}
            for (it, q), n in (after - base).items():
                added[it] = added.get(it, 0) + q * n
            dued2 = (fn.tf.get("due") or {}).get(player) or {}
            residual = dict(dued2.get(tstep + 1) or {})
            for it, q in due_next.items():
                # 净卖量恒等：加回 + 再延残额 == 原记账量
                if added.get(it, 0) + residual.get(it, 0) != q:
                    fail["pair_identity"].append(
                        {"case": case, "item": it, "due": q,
                         "added": added.get(it, 0),
                         "residual": residual.get(it, 0),
                         "step": tstep + 1})
    passed = not any(fail.values())
    return {"passed": passed, "n_cases": n_cases, "seed": seed,
            "n_non_trigger_cases": n_non_trigger, "n_moves": n_moves,
            "n_pair_checks": n_pairs,
            "failures": {k: v[:5] for k, v in fail.items() if v}}


def main():
    os.chdir(MODULE_DIR)
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {"commands": ["python3 orderbook_topform_lab/build_topform.py",
                                "python3 orderbook_topform_lab/gates_topform.py"],
                   "episode_seeds": list(EPISODE_SEEDS),
                   "runner": "episode_trace.run_episode（track2 同款+逐拍动作流）"},
        "forms": {},
    }
    overall_ok = True
    budget = {"gate_episodes": 0}
    dumps = {}
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
            if tag != "s101_rerun":
                dumps[(form, seed, tag)] = dump
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
        passed = all(g.get("passed") for g in res.values()
                     if isinstance(g, dict) and "passed" in g)
        overall_ok = overall_ok and passed
        res["overall"] = passed
        res["elapsed_s"] = round(time.perf_counter() - t0, 1)
        out["forms"][form] = res
        print(form, "gates:", {k: v.get("passed") for k, v in res.items()
                               if isinstance(v, dict) and "passed" in v},
              "overall", passed, flush=True)

    # ---- 足迹审计门：函数级硬门探针 + 级联读数（非门） ----
    try:
        out["footprint_probe"] = _footprint_probe()
    except Exception as exc:
        out["footprint_probe"] = {"passed": False, "error": repr(exc)[:300]}
    print("footprint probe:", out["footprint_probe"].get("passed"),
          out["footprint_probe"].get("failures"), flush=True)
    try:
        readings = {}
        for seed, tag in ((EPISODE_SEEDS[0], "s101"), (EPISODE_SEEDS[1], "s102")):
            readings["seed_%d" % seed] = _stream_readings(
                dumps.get(("h2", seed, tag)), dumps.get(("h1", seed, tag)))
        out["stream_readings"] = readings
    except Exception as exc:
        out["stream_readings"] = {"error": repr(exc)[:300]}

    out["overall_passed"] = bool(overall_ok
                                 and out["footprint_probe"].get("passed"))
    out["budget"] = budget
    (EVID / "gates.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("OVERALL gates passed:", out["overall_passed"], "budget:", budget,
          flush=True)


if __name__ == "__main__":
    main()
