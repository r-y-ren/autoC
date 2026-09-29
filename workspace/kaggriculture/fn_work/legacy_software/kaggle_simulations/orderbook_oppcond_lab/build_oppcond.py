# -*- coding: utf-8 -*-
"""build_oppcond：对手画像器 + 条件策略构建线（判决先行·不发射·不提交）。

责任口径（任务 opp-conditional A1）：基底=orderbook_strongest_lab/build/h1/
main.py（H1 件字节，sha 76b5f842…）零改动读入；形态（内生优先：画像器与条件
门全部织入同一尾块，profiler_core.CORE_SRC 原文字节=离线重放同源）：
- h1_base：H1 原样复制（字节恒等对照底）；
- oc_c1：画像器 + C1 条件路由（ICE+YARN 世界 ∧ 系谱型→r105 线；H1/未知→
  默认表；底 day27 换线保留——cond-route 已证机制逐字同源）；
- oc_c2：画像器 + C2 条件视界（系谱型→RACE 预留视界缩短 _V9_ITEM_HZ 注入；
  H1/未知→40 档默认零改动；H_SHORT 由小网格标定）；
- oc_c1c2c3：画像器 + C1 + C2 + C3 条件卖压（WFR-攻击型→羊毛相位错峰：
  layer_k1.retape_phase_offset 手术件按 (route,step) 稀疏差量内嵌，144 锁存
  后换 route 表；非 WFR 零足迹）。

构建校验（fail-closed 不产出）：①语法 ②装载末 callable=_hs_agent ③基座
字节前缀恒等（H1 零改动）④画像器探针（阈值冻结核对表）⑤C1 router 探针
（触发/非触发/两序/day27 + 类门逐点）⑥C2 视界注入探针（spy 口径）⑦C3 换表
探针（变体哈希 + 市场单槽恒等=零跨拍）。
用法：python3 build_oppcond.py grid   # C2 小网格变体（build/grid_h*/）
      python3 build_oppcond.py final --h-short N
只写 orderbook_oppcond_lab/。不改既有代码。不发射。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
import io
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

from profiler_core import CORE_SRC, probe_expected  # noqa: E402
from orderbook_iterk_lab import layer_k1 as k1  # noqa: E402
from orderbook_r37 import retape_sheep as rs  # noqa: E402

RECORD_VERSION = "oppcond-build/1.0"
BASE_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
BASE_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb67649"
                     "74b22f337")
BUILD_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
ENTRY_NAME = "_hs_agent"
ROUTE_ARM = 105
TRIGGER_KEY = "ICE_CREAM_SHOP+YARN_STORE"
REVEAL_STEP = 144
GRID_H = (8, 12, 16, 24)
DELTA_CAP = 600          # C3 稀疏差量上限（超出=fail-closed；实测 443=147 落刀走位链）


# ------------------------------------------------------------ C3 变体差量 --
def build_c3_delta(base_text: str) -> dict:
    """K1 毛期错峰手术 → (route, step) 稀疏差量（写时复制；输入零改动）。

    返回 {"delta": {rid(str): {step(str): action}}, "stats": {...}}。
    """
    pkg = rs._decode_routes(base_text)
    before = k1.static_shear_day_counts(pkg)
    result = k1.retape_phase_offset(pkg)
    after = k1.static_shear_day_counts(result["routes"])
    base_keys = sorted(pkg["routes"].keys(), key=lambda x: int(x))
    var_keys = sorted(result["routes"]["routes"].keys(), key=lambda x: int(x))
    if [int(x) for x in base_keys] != [int(x) for x in var_keys]:
        raise RuntimeError("C3 红：术后路由键集漂移")
    delta = {}
    n_changed = 0
    n_market_diff = 0
    for rid in base_keys:
        ia = pkg["routes"][rid]
        ib = result["routes"]["routes"][rid]
        if len(ia) != len(ib):
            raise RuntimeError("C3 红：路由 %s 长度漂移" % rid)
        for step, (x, y) in enumerate(zip(ia, ib)):
            a = pkg["actions"][x]
            b = result["routes"]["actions"][y]
            if a != b:
                delta.setdefault(str(rid), {})[str(step)] = b
                n_changed += 1
                if a.get("market") != b.get("market"):
                    n_market_diff += 1
    if n_market_diff:
        raise RuntimeError("C3 红：差量触碰市场单槽 %d 拍（零跨拍破）" % n_market_diff)
    if n_changed > DELTA_CAP:
        raise RuntimeError("C3 红：差量 %d 超上限 %d" % (n_changed, DELTA_CAP))
    return {"delta": delta, "change_table": result["change_table"], "stats": {
        "changed_steps": n_changed, "routes_touched": len(delta),
        "market_slot_touched_steps": n_market_diff,
        "surgery_stats": result["stats"], "shear_day_before": before,
        "shear_day_after": after, "change_table_rows": len(result["change_table"]),
    }}


# ------------------------------------------------------------ 尾块组装 --
def build_tail(cfg: dict, c3_blob: str) -> str:
    parts = []
    parts.append("\n# ===== opp-conditional layer（judge-side only；"
                 "H1 基座零改动前缀恒等） =====\n")
    parts.append("# 画像器（profiler_core.CORE_SRC 同源字节）+ 条件门 "
                 "C1/C2/C3；分类不确定→未知=零足迹。\n")
    parts.append(CORE_SRC)
    parts.append("\n\n_OC_STATE = {}\n\n\n")
    parts.append(
        "def _oc_state_for(observation):\n"
        "    try:\n"
        "        player = int((observation or {}).get('player', 0))\n"
        "    except Exception:\n"
        "        player = 0\n"
        "    st = _OC_STATE.get(player)\n"
        "    if st is None:\n"
        "        st = _OC_STATE[player] = _oc_state_new()\n"
        "    return st\n\n\n"
        "def _oc_after(observation, action):\n"
        "    _oc_update(_oc_state_for(observation), observation, action)\n\n\n"
        "def _oc_cls(observation, step):\n"
        "    st = _oc_state_for(observation)\n"
        "    _oc_lock_if_due(st, step)\n"
        "    return st.get('cls') or 'unknown'\n\n")
    # ---- C1 条件路由 ----
    parts.append("# ---- C1 条件路由：ICE+YARN 世界 ∧ 系谱型→r105 线；"
                 "其余默认表（cond-route 已证机制同源） ----\n")
    parts.append(
        "_OC_ROUTE_ARM = %d\n"
        "_OC_TRIGGER_KEY = %r\n"
        "_OC_C1_CLASSES = %r\n"
        "_OC_BASE_ROUTER = _IMPL.chassis.router\n\n\n"
        "def _oc_router(observation, step, state):\n"
        "    r = _OC_BASE_ROUTER(observation, step, state)\n"
        "    try:\n"
        "        if int(step) >= %d and not state.get('oc_latched'):\n"
        "            state['oc_latched'] = True\n"
        "            town = observation.get('town') or {}\n"
        "            shops = sorted(str(s) for s in\n"
        "                           list(town.get('unlocked_shops') or [])[:2])\n"
        "            if '+'.join(shops) == _OC_TRIGGER_KEY:\n"
        "                if _oc_cls(observation, step) in _OC_C1_CLASSES:\n"
        "                    state['route'] = _OC_ROUTE_ARM\n"
        "                    r = _OC_ROUTE_ARM\n"
        "    except Exception:\n"
        "        pass\n"
        "    return r\n\n\n"
        "_IMPL.chassis.router = _oc_router\n\n"
        % (ROUTE_ARM, TRIGGER_KEY,
           ("r37_2965_family",) if cfg.get("c1") else (),
           REVEAL_STEP))
    # ---- C2 条件视界 ----
    parts.append("# ---- C2 条件视界：系谱型→RACE 预留视界 %d（_V9_ITEM_HZ "
                 "注入）；H1/未知→40 档默认零改动 ----\n" % cfg.get("h_short", 0))
    parts.append(
        "_OC_H_SHORT = %d\n"
        "_OC_C2_CLASSES = %r\n"
        "_OC_BASE_RESERVE = _r36_reserve\n\n\n"
        "def _oc_r36_reserve(obs, action):\n"
        "    try:\n"
        "        player = int(obs.get('player', 0))\n"
        "        cls = _oc_cls(obs, int(obs.get('step', 0)))\n"
        "    except Exception:\n"
        "        player, cls = 0, 'unknown'\n"
        "    if cls in _OC_C2_CLASSES:\n"
        "        saved = _V9_ITEM_HZ.get(player)\n"
        "        _V9_ITEM_HZ[player] = dict.fromkeys(V9_RACE_ITEMS, _OC_H_SHORT)\n"
        "        try:\n"
        "            return _OC_BASE_RESERVE(obs, action)\n"
        "        finally:\n"
        "            if saved is None:\n"
        "                _V9_ITEM_HZ.pop(player, None)\n"
        "            else:\n"
        "                _V9_ITEM_HZ[player] = saved\n"
        "    return _OC_BASE_RESERVE(obs, action)\n\n\n"
        "_r36_reserve = _oc_r36_reserve\n\n"
        % (int(cfg.get("h_short") or 0),
           ("r37_2965_family",) if cfg.get("c2") else ()))
    # ---- C3 条件卖压 ----
    parts.append("# ---- C3 条件卖压：WFR-攻击型→羊毛相位错峰（K1 手术件 "
                 "稀疏差量内嵌；非 WFR 零足迹） ----\n")
    if cfg.get("c3"):
        delta_expr = "json.loads(zlib.decompress(base64.b85decode(%r)))" % c3_blob
    else:
        delta_expr = "{}"
    parts.append(
        "_OC_C3_CLASSES = %r\n"
        "_OC_C3_DELTA = %s\n"
        "_OC_C3_SWAPPED = [False]\n\n\n"
        "def _oc_c3_swap(observation, step):\n"
        "    if _OC_C3_SWAPPED[0] or int(step) < %d:\n"
        "        return\n"
        "    try:\n"
        "        if _oc_cls(observation, step) not in _OC_C3_CLASSES:\n"
        "            return\n"
        "        routes = {}\n"
        "        for rid, seq in _IMPL.chassis.routes.items():\n"
        "            s = list(seq)\n"
        "            for sstep, act in (_OC_C3_DELTA.get(str(rid)) or {}).items():\n"
        "                s[int(sstep)] = act\n"
        "            routes[rid] = s\n"
        "        _IMPL.chassis.routes = routes\n"
        "        _OC_C3_SWAPPED[0] = True\n"
        "    except Exception:\n"
        "        pass\n\n"
        % (("wfr",) if cfg.get("c3") else (), delta_expr, REVEAL_STEP))
    # ---- 入口包 ----
    parts.append("# ---- 入口包（画像观测零动作改动；末 callable 保持 "
                 "_hs_agent） ----\n")
    parts.append(
        "_OC_PARENT = _hs_agent\n"
        "del _hs_agent\n"
        "def _hs_agent(observation, configuration=None):\n"
        "    action = _OC_PARENT(observation, configuration)\n"
        "    try:\n"
        "        step = int((observation or {}).get('step', 0))\n"
        "        _oc_after(observation, action)\n"
        "        if step >= %d:\n"
        "            _oc_c3_swap(observation, step)\n"
        "    except Exception:\n"
        "        pass\n"
        "    return action\n" % REVEAL_STEP)
    return "".join(parts)


# ------------------------------------------------------------ 校验探针 --
def _mk_obs(step: int, shops, money=(1000.0, 1000.0)) -> dict:
    return {"step": step, "player": 0, "day": step // 24, "hour": step % 24,
            "town": {"unlocked_shops": list(shops)},
            "farms": [{"money": money[0]}, {"money": money[1]}],
            "market": {"inventory": {"WHEAT": 0}, "prices": {}}}


def verify_form(text: str, base_src: str, cfg: dict, form: str,
                variant_routes_hash: str) -> dict:
    """fail-closed 七校验；返回探针台账。"""
    # ① 语法
    try:
        compile(text, "<oppcond:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: %r" % (form, exc))
    # ③ 基座字节前缀恒等
    if not text.startswith(base_src):
        raise RuntimeError("校验③红 %s: 基座前缀漂移" % form)
    # ② 装载末 callable=_hs_agent
    ns: dict = {}
    exec(compile(text, "<oppcond:%s>" % form, "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验②红 %s: 末 callable=%r" % (form, got))
    # ④ 画像器探针（阈值冻结核对表）
    probe = []
    for row in probe_expected():
        got, why = ns["_oc_decide"]({
            "cashdiff1": row["features"][0],
            "rival_money1": row["features"][1],
            "sim_max": row["features"][2],
            "sim_seen": 1,
            "rival_animals_143": {"SHEEP": row["features"][3]},
        })
        probe.append({"expect": row["expect"], "got": got,
                      "match": got == row["expect"], "why": why})
    if not all(p["match"] for p in probe):
        raise RuntimeError("校验④红 %s: 画像探针 %s" % (form, probe))
    # ⑤ C1 router 探针
    c1_rows = []
    if cfg.get("c1"):
        trig = [("ICE_CREAM_SHOP", "YARN_STORE"),
                ("YARN_STORE", "ICE_CREAM_SHOP")]
        nontrig = [("ICE_CREAM_SHOP", "ICE_CREAM_SHOP"),
                   ("BAKERY", "YARN_STORE"), ("PET_CAFE", "PIZZA_SHOP")]
        cases = ([(s, "r37_2965_family") for s in trig]
                 + [(s, "h1_mirror") for s in trig]
                 + [(s, "unknown") for s in trig]
                 + [(s, "r37_2965_family") for s in nontrig])
        for shops, cls in cases:
            st_b, st_c = {}, {}
            ns["_OC_STATE"].clear()
            st = ns["_oc_state_for"]({"player": 0})
            st["cls"] = cls
            st["locked"] = True
            vals = {}
            for step in (0, 72, REVEAL_STEP, REVEAL_STEP + 40, 648):
                obs = _mk_obs(step, shops)
                rb = ns["_OC_BASE_ROUTER"](obs, step, st_b)
                rc = ns["_oc_router"](obs, step, st_c)
                expect = rb
                is_trg = tuple(sorted(shops)) == tuple(
                    sorted(("ICE_CREAM_SHOP", "YARN_STORE")))
                if is_trg and cls == "r37_2965_family" \
                        and REVEAL_STEP <= step < 648:
                    expect = ROUTE_ARM
                vals[step] = (rb, rc, expect, rc == expect)
            ok = all(v[3] for v in vals.values())
            c1_rows.append({"shops": list(shops), "cls": cls,
                            "steps": {str(k): {"base": v[0], "oc": v[1],
                                               "expect": v[2], "match": v[3]}
                                      for k, v in vals.items()},
                            "match": ok})
        if not all(r["match"] for r in c1_rows):
            raise RuntimeError("校验⑤红 %s: C1 router 探针失败" % form)
    # ⑥ C2 视界注入探针（spy）
    c2_rows = []
    if cfg.get("c2"):
        for cls, expect_override in (("r37_2965_family", True),
                                     ("h1_mirror", False),
                                     ("unknown", False)):
            seen = {}
            def spy(obs, action, _seen=seen):  # noqa: B023
                _seen["hz"] = ns["_V9_ITEM_HZ"].get(int(obs.get("player", 0)))
                return action
            ns["_OC_BASE_RESERVE"] = spy
            ns["_OC_STATE"].clear()
            st = ns["_oc_state_for"]({"player": 0})
            st["cls"] = cls
            st["locked"] = True
            ns["_V9_ITEM_HZ"].pop(0, None)
            ns["_oc_r36_reserve"]({"player": 0, "step": 300}, {"market": []})
            hz = seen.get("hz")
            got = (isinstance(hz, dict) and hz
                   and set(hz.values()) == {int(cfg["h_short"])})
            restored = 0 not in ns["_V9_ITEM_HZ"]
            c2_rows.append({"cls": cls, "expect_override": expect_override,
                            "got_override": bool(got),
                            "restored": restored,
                            "match": bool(got) == expect_override and restored})
        if not all(r["match"] for r in c2_rows):
            raise RuntimeError("校验⑥红 %s: C2 视界探针失败 %s" % (form, c2_rows))
    # ⑦ C3 换表探针
    c3_rows = []
    if cfg.get("c3"):
        import copy as _copy
        base_routes = _copy.deepcopy(ns["_IMPL"].chassis.routes)
        for cls, expect_swap in (("wfr", True), ("h1_mirror", False),
                                 ("unknown", False),
                                 ("r37_2965_family", False)):
            ns["_OC_STATE"].clear()
            ns["_OC_C3_SWAPPED"][0] = False
            ns["_IMPL"].chassis.routes = _copy.deepcopy(base_routes)
            st = ns["_oc_state_for"]({"player": 0})
            st["cls"] = cls
            st["locked"] = True
            ns["_oc_c3_swap"](_mk_obs(REVEAL_STEP, ("PET_CAFE",)),
                              REVEAL_STEP)
            now = ns["_IMPL"].chassis.routes
            changed = 0
            for rid, seq in now.items():
                for i, a in enumerate(seq):
                    if a != base_routes[rid][i]:
                        changed += 1
            market_same = all(
                now[rid][i].get("market") == base_routes[rid][i].get("market")
                for rid in now for i in range(len(now[rid])))
            got = changed > 0
            c3_rows.append({"cls": cls, "expect_swap": expect_swap,
                            "got_swap": got, "changed_steps": changed,
                            "market_slots_identical": market_same,
                            "match": got == expect_swap and market_same})
        if not all(r["match"] for r in c3_rows):
            raise RuntimeError("校验⑦红 %s: C3 换表探针失败 %s" % (form, c3_rows))
        ns["_IMPL"].chassis.routes = base_routes
    return {"probe_core": probe, "probe_c1": c1_rows, "probe_c2": c2_rows,
            "probe_c3": c3_rows, "variant_routes_hash": variant_routes_hash}


def _make_tar(main_bytes: bytes) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    return buf.getvalue()


def _build_base_copy(base_bytes: bytes, base_src: str, name: str) -> dict:
    """h1_base：H1 字节恒等复制（对照底；无尾块）。"""
    ns: dict = {}
    exec(compile(base_src, "<oppcond:%s>" % name, "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        raise RuntimeError("校验②红 %s: 末 callable 非 %s" % (name, ENTRY_NAME))
    out_dir = BUILD_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)
    tar_bytes = _make_tar(base_bytes)
    (out_dir / "main.py").write_bytes(base_bytes)
    (out_dir / "submission.tar.gz").write_bytes(tar_bytes)
    manifest = {
        "schema": "orderbook_oppcond_manifest/1.0",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "form": name, "cfg": {"c1": False, "c2": False, "c3": False,
                              "h_short": 0},
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "main_bytes": len(base_bytes),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
        "byte_identical_to_H1": True,
        "append_only_prefix_identical": True, "entry": ENTRY_NAME,
        "entry_last_callable": True, "layers": [],
        "compile_ok": True,
        "probes": {"entry_ok": True},
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("built", name, manifest["main_sha256"][:16], "(byte-identical)",
          flush=True)
    return manifest


def build_form(name: str, base_bytes: bytes, base_src: str, cfg: dict,
               c3_blob: str, variant_routes_hash: str) -> dict:
    if name == "h1_base":
        return _build_base_copy(base_bytes, base_src, name)
    text = base_src + build_tail(cfg, c3_blob)
    data = text.encode("utf-8")
    probes = verify_form(text, base_src, cfg, name, variant_routes_hash)
    out_dir = BUILD_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)
    tar_bytes = _make_tar(data)
    (out_dir / "main.py").write_bytes(data)
    (out_dir / "submission.tar.gz").write_bytes(tar_bytes)
    manifest = {
        "schema": "orderbook_oppcond_manifest/1.0",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "form": name, "cfg": dict(cfg),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data), "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
        "append_only_prefix_identical": True, "entry": ENTRY_NAME,
        "entry_last_callable": True,
        "profiler_core_sha256": hashlib.sha256(CORE_SRC.encode()).hexdigest(),
        "layers": [k for k, on in (("profiler", True), ("c1_route", cfg.get("c1")),
                                   ("c2_horizon", cfg.get("c2")),
                                   ("c3_wool_phase", cfg.get("c3"))) if on],
        "route_arm": ROUTE_ARM if cfg.get("c1") else None,
        "trigger_key": TRIGGER_KEY if cfg.get("c1") else None,
        "h_short": cfg.get("h_short") if cfg.get("c2") else None,
        "c3_variant_routes_hash": variant_routes_hash if cfg.get("c3") else None,
        "compile_ok": True, "probes": probes,
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("built", name, manifest["main_sha256"][:16], manifest["main_bytes"],
          "bytes", flush=True)
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("grid", "final"))
    ap.add_argument("--h-short", type=int, default=None)
    args = ap.parse_args()
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（H1 字节漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("基底不以换行收尾（fail-closed）")
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    c3 = build_c3_delta(base_src)
    import base64 as _b64, zlib as _zlib
    blob = _b64.b85encode(_zlib.compress(
        json.dumps(c3["delta"], sort_keys=True).encode(), 9)).decode()
    var_hash = hashlib.sha256(
        json.dumps(c3["delta"], sort_keys=True).encode()).hexdigest()[:16]

    forms = {}
    if args.mode == "grid":
        forms["h1_base"] = build_form(
            "h1_base", base_bytes, base_src,
            {"c1": False, "c2": False, "c3": False, "h_short": 0}, "", "none")
        for h in GRID_H:
            forms["grid_h%d" % h] = build_form(
                "grid_h%d" % h, base_bytes, base_src,
                {"c1": False, "c2": True, "c3": False, "h_short": h}, "", "none")
    else:
        if args.h_short is None:
            raise SystemExit("final 需 --h-short")
        h = int(args.h_short)
        forms["h1_base"] = build_form(
            "h1_base", base_bytes, base_src,
            {"c1": False, "c2": False, "c3": False, "h_short": 0}, "", "none")
        forms["oc_c1"] = build_form(
            "oc_c1", base_bytes, base_src,
            {"c1": True, "c2": False, "c3": False, "h_short": 0}, "", "none")
        forms["oc_c2"] = build_form(
            "oc_c2", base_bytes, base_src,
            {"c1": False, "c2": True, "c3": False, "h_short": h}, "", "none")
        forms["oc_c1c2c3"] = build_form(
            "oc_c1c2c3", base_bytes, base_src,
            {"c1": True, "c2": True, "c3": True, "h_short": h}, blob, var_hash)

    out = {"version": RECORD_VERSION, "mode": args.mode,
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "c3_delta": c3["stats"], "c3_blob_bytes": len(blob),
           "c3_mechanism": "layer_k1.retape_phase_offset（剪毛刀 d17/20/23/26 → "
                           "d+1/d+2，d29 保留；量守恒零跨拍）按 (route,step) 稀疏"
                           "差量内嵌；WFR-攻击型 144 锁存后换表",
           "forms": {k: {kk: v[kk] for kk in
                         ("form", "cfg", "main_sha256", "main_bytes",
                          "tar_sha256", "layers")}
                     for k, v in forms.items()}}
    (EVID_DIR / ("build_%s.json" % args.mode)).write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    (EVID_DIR / "c3_change_table.json").write_text(
        json.dumps({"version": RECORD_VERSION,
                    "change_table": c3["change_table"]},
                   ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("c3 delta:", c3["stats"]["changed_steps"], "steps /",
          c3["stats"]["routes_touched"], "routes; blob", len(blob), "bytes")
    return out


if __name__ == "__main__":
    main()
