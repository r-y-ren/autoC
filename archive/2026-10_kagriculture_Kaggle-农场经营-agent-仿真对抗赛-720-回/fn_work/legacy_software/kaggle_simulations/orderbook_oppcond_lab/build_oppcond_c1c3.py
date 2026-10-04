# -*- coding: utf-8 -*-
"""build_oppcond_c1c3：剥离劣化件 C2 后的 C1+C3 纯增形态构建+四门（不发射·不提交）。

责任口径（任务 opp-conditional-v2 A1）：沿既有构建线（build_oppcond 组件复用，
不改既有代码）组合——
- 基底 = orderbook_strongest_lab/build/h1/main.py（H1 件字节 sha 76b5f842…）
  零改动读入（build_oppcond.BASE_SHA_EXPECTED 硬校验）；
- oc_c1c3 = 画像器（profiler_core.CORE_SRC sha 0ed5e7c2…）+ C1 条件路由
  （ICE+YARN 世界 ∧ 系谱型→r105 线）+ C3 条件羊毛错峰（WFR-攻击型→K1 手术
  稀疏差量 443 拍/34 路由件，与全套形态同源差量）；**不含 C2**（cfg.c2=False
  → _OC_C2_CLASSES=() 惰性零足迹；layers 记账不含 c2_horizon）。

校验：build_oppcond.verify_form 七探针（①语法 ②末 callable=_hs_agent ③基座
字节前缀恒等 ④画像探针 ⑤C1 router 探针 ⑦C3 换表探针）+ C3 差量守恒断言
（443 拍/34 路由，与 oc_c1c2c3 全套件同一手术差量）。
四门门禁：gates_oppcond 同口径复用（load / health(DONE+单步<1s+720 turns) /
determinism(双跑 sha) / identity(体积+sha+前缀恒等)），形态=oc_c1c3 单件。
只写 orderbook_oppcond_lab/build/oc_c1c3/ 与 evidence/build_c1c3.json、
evidence/gates_c1c3.json。不改既有代码。不发射。
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
import time
import zlib
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import build_oppcond as B  # noqa: E402
import gates_oppcond as G  # noqa: E402

RECORD_VERSION = "oppcond-build-c1c3/1.0"
FORM = "oc_c1c3"
CFG = {"c1": True, "c2": False, "c3": True, "h_short": 0}
C3_EXPECT = {"changed_steps": 443, "routes_touched": 34}


def main():
    t0 = time.perf_counter()
    base_bytes = B.BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != B.BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（H1 字节漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("基底不以换行收尾（fail-closed）")

    # ---- C3 手术差量（与全套形态同源：layer_k1.retape_phase_offset 写时复制） ----
    c3 = B.build_c3_delta(base_src)
    stats = c3["stats"]
    if (stats["changed_steps"] != C3_EXPECT["changed_steps"]
            or stats["routes_touched"] != C3_EXPECT["routes_touched"]):
        raise RuntimeError("C3 差量漂移：%s ≠ %s" % (
            {k: stats[k] for k in C3_EXPECT}, C3_EXPECT))
    blob = base64.b85encode(zlib.compress(
        json.dumps(c3["delta"], sort_keys=True).encode(), 9)).decode()
    var_hash = hashlib.sha256(
        json.dumps(c3["delta"], sort_keys=True).encode()).hexdigest()[:16]

    # ---- 构建 oc_c1c3（build_form 复用；fail-closed 七探针内建） ----
    manifest = B.build_form(FORM, base_bytes, base_src, CFG, blob, var_hash)
    if manifest["layers"] != ["profiler", "c1_route", "c3_wool_phase"]:
        raise RuntimeError("layers 记账漂移：%s" % manifest["layers"])

    build_out = {
        "version": RECORD_VERSION, "mode": "c1c3",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "design": "画像器 + C1 条件路由 + C3 条件羊毛错峰；剥掉 C2（c2=False "
                  "→ _OC_C2_CLASSES=() 惰性；layers 无 c2_horizon）",
        "base_main": str(B.BASE_MAIN), "base_main_sha256": base_sha,
        "byte_zero_change_on_base": True,
        "profiler_core_sha256": hashlib.sha256(
            B.CORE_SRC.encode()).hexdigest(),
        "c3_delta": {k: stats[k] for k in
                     ("changed_steps", "routes_touched",
                      "market_slot_touched_steps", "change_table_rows",
                      "surgery_stats")},
        "c3_delta_expected": C3_EXPECT,
        "c3_blob_bytes": len(blob), "c3_variant_routes_hash": var_hash,
        "c3_same_source_as_full_set": "build_oppcond.build_c3_delta（"
                                      "layer_k1.retape_phase_offset；全套形态 "
                                      "oc_c1c2c3 同一手术差量件）",
        "form": {k: manifest[k] for k in
                 ("form", "cfg", "main_sha256", "main_bytes", "tar_sha256",
                  "layers", "route_arm", "trigger_key",
                  "c3_variant_routes_hash")},
        "probes_ok": True,
        "probe_rows": {"core": len(manifest["probes"]["probe_core"]),
                       "c1": len(manifest["probes"]["probe_c1"]),
                       "c2": len(manifest["probes"]["probe_c2"]),
                       "c3": len(manifest["probes"]["probe_c3"])},
    }
    (B.EVID_DIR / "build_c1c3.json").write_text(
        json.dumps(build_out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("built", FORM, manifest["main_sha256"][:16], manifest["main_bytes"],
          "bytes layers", manifest["layers"], flush=True)

    # ---- 四门（gates_oppcond 同口径单件复用） ----
    pkg = B.BUILD_DIR / FORM
    gates = {}
    for name, fn in (("load", G._gate_load), ("health", G._gate_health),
                     ("determinism", G._gate_determinism)):
        try:
            gates[name] = fn(pkg)
        except Exception as exc:
            gates[name] = {"passed": False,
                           "error": "%s: %s" % (type(exc).__name__, exc)}
    try:
        gates["identity"] = G._gate_identity(pkg, FORM)
    except Exception as exc:
        gates["identity"] = {"passed": False,
                             "error": "%s: %s" % (type(exc).__name__, exc)}
    gates["overall"] = all(g.get("passed") for g in gates.values())
    gates_out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "oppcond-gates-c1c3/1.0",
        "source": {"commands": ["python3 orderbook_oppcond_lab/"
                               "build_oppcond_c1c3.py"],
                   "forms": [FORM], "episode_seeds": list(G.EPISODE_SEEDS),
                   "gates_caliber": "gates_oppcond 四门同口径"
                                    "（load/health/determinism/identity）"},
        "forms": {FORM: gates},
        "overall_passed": bool(gates["overall"]),
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    (B.EVID_DIR / "gates_c1c3.json").write_text(
        json.dumps(gates_out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("gates", {k: gates[k].get("passed") for k in
                    ("load", "health", "determinism", "identity")},
          "overall", gates["overall"], flush=True)
    if not gates["overall"]:
        raise SystemExit("四门未全过（gates_c1c3.json）")
    return {"build": build_out, "gates": gates_out}


if __name__ == "__main__":
    main()
