# -*- coding: utf-8 -*-
"""build_v89：haodou V89 采纳/合成构建线（判决先行·不发射·不提交·不改既有代码）。

责任口径（任务 v89-upgrade）：
① V89 本体（B 组口径）：kernels pull haodou092/kaggriculture-harvest-ledger
   notebook 内嵌 FILES base85+zlib 三件 → EXPECTED sha 自校验解包 → main.py
   （entry=gated_fixed_sell_agent，V89 新增 G793 镜像谱门替代 V82 pet 尾包）。
② v89_pure：V89 字节原样重打包（对照恒等；tar=orderbook_2965_adopt 确定性配方）。
③ v89_full = V89 + X1 卫生层（orderbook_strongest_lab/layer_x1，build_block
   剥件复用）+ 画像器（profiler_core.CORE_SRC）+ C3 条件羊毛错峰（build_oppcond
   .build_c3_delta 在 V89 基底重算手术差量，写时复制零改动基底）。
   尾块注入沿 append 先例（build_strongest SEPARATOR+块；基座字节前缀恒等）。
④ G793 零冲突审计：命名足迹交集 + 静态互不引用 + 动态双武装探针
   （G793 bypass ∧ C3 swap ∧ X1 卫生 同时工作、各台账 errors=0）。
fail-closed：任一校验红即不产出该形态。只写 orderbook_v89_lab/。
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import re
import sys
import tarfile
import time
import zlib
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_oppcond_lab"),
          str(KSIM_DIR / "orderbook_strongest_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import build_oppcond as B            # noqa: E402  剥件复用（零改动引用）
import build_strongest as BS         # noqa: E402
from orderbook_2965_adopt import build_adopt as ba  # noqa: E402

RECORD_VERSION = "v89-build/1.0"
SCHEMA = "orderbook_v89_lab_manifest/1.0"
NOTEBOOK = Path("/tmp/v89test/pull/kaggriculture-harvest-ledger.ipynb")
NOTEBOOK_EXPECTED_SHA = ("5322f36d3fe8264c7cdcd31c29e26046e8e3fd45"
                         "191ead6f11ae47ceb1c76c8b")
BASE_SHA_EXPECTED = ("01ee3976f97a9ac71be40eff667b24c5a69cd86fce88bbbd"
                     "f25ea1e10aecd60d")
C3_EXPECT = {"changed_steps": 443, "routes_touched": 34}
V89_ENTRY = "gated_fixed_sell_agent"
FULL_ENTRY = "_hs_agent"
BUILD_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SIZE_CAP = 100 * 1024 * 1024
OC_CFG = {"c1": False, "c2": False, "c3": True, "h_short": 0}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------ B 组口径解包 --
def extract_v89():
    """notebook FILES base85+zlib 解包（EXPECTED sha 自校验）→ {name: bytes}。"""
    nb_raw = NOTEBOOK.read_bytes()
    nb_sha = sha(nb_raw)
    if nb_sha != NOTEBOOK_EXPECTED_SHA:
        raise RuntimeError("notebook sha 漂移：%s" % nb_sha)
    nb = json.loads(nb_raw)
    src = "".join(nb["cells"][1]["source"])
    marker = "for filename, encoded in FILES.items():"
    if marker not in src:
        raise RuntimeError("notebook 无 FILES 解包段（形态漂移）")
    ns: dict = {}
    exec(compile(src.split(marker)[0], "<v89cell1>", "exec"), ns)
    files, expected = ns["FILES"], ns["EXPECTED"]
    out = {}
    for name, enc in files.items():
        content = zlib.decompress(base64.b85decode(enc))
        if sha(content) != expected[name]:
            raise RuntimeError("内嵌件 %s sha 自校验红" % name)
        out[name] = content
    return {"notebook_sha256": nb_sha, "files": out,
            "expected": dict(expected),
            "extraction": "B 组口径：FILES base85+zlib 内嵌三件，EXPECTED sha "
                          "自校验解包（analysis32-public-arms-B 同法）"}


# ------------------------------------------------------------ G793 冲突审计 --
AUDIT_PROBE_SRC = r'''
def _v89audit_probe(ns):
    """G793 × 我方组件 双武装动态探针（返回台账；红=RuntimeError）。"""
    import copy as _copy
    rep = {}
    tile = {"kind": "CROP", "crop": "WHEAT", "animal": None}
    farm_a = {"tiles": [[tile, tile], [tile, tile]], "unlocked_quadrants": [0, 1],
              "money": 1000.0}
    farm_b = {"tiles": [[tile, tile], [tile, tile]], "unlocked_quadrants": [0, 1],
              "money": 1300.0}
    farm_c = {"tiles": [[tile, tile], [tile, tile]], "unlocked_quadrants": [0, 2],
              "money": 1000.0}
    # ① 纯函数指纹
    if ns["_g793_shape"](farm_a) != ns["_g793_shape"](farm_b):
        raise RuntimeError("audit①红：镜像指纹应相等")
    if ns["_g793_shape"](farm_a) == ns["_g793_shape"](farm_c):
        raise RuntimeError("audit①红：非镜像指纹应不等")
    rep["shape_ok"] = True
    # ② G793 bypass（镜像+现金差≥20 → 跳过置换、返回同对象）
    act = {"farmer": ["PASS"], "hands": [], "market": []}
    obs_mirror = {"step": 100, "player": 0, "farms": [farm_a, farm_b]}
    ns["_G793_STATE"].clear()
    ns["_G793_REPORT"].update(calls=0, classified=0, bypassed=0, errors=0)
    out = ns["_s793_reorder"](obs_mirror, act)
    if out is not act or ns["_G793_REPORT"]["classified"] < 1 \
            or ns["_G793_REPORT"]["bypassed"] < 1:
        raise RuntimeError("audit②红：G793 bypass 未触发 %s"
                           % ns["_G793_REPORT"])
    rep["g793_bypass_ok"] = True
    rep["g793_report_after_bypass"] = dict(ns["_G793_REPORT"])
    # ③ C3 换表（wfr → 换 443 拍稀疏差量；market 槽零触碰）
    base_routes = _copy.deepcopy(ns["_IMPL"].chassis.routes)
    ns["_OC_STATE"].clear()
    st = ns["_oc_state_for"]({"player": 0})
    st["cls"] = "wfr"
    st["locked"] = True
    ns["_OC_C3_SWAPPED"][0] = False
    ns["_oc_c3_swap"]({"step": 144, "player": 0}, 144)
    now = ns["_IMPL"].chassis.routes
    changed = sum(1 for rid in now for i, a in enumerate(now[rid])
                  if a != base_routes[rid][i])
    market_same = all(now[rid][i].get("market") == base_routes[rid][i].get("market")
                      for rid in now for i in range(len(now[rid])))
    if changed <= 0 or not market_same:
        raise RuntimeError("audit③红：C3 换表 changed=%d market_same=%s"
                           % (changed, market_same))
    rep["c3_swap_ok"] = True
    rep["c3_changed_steps"] = changed
    # ④ X1 卫生（step>=624 死单清理台账动、其余零足迹）
    a2 = {"farmer": ["PASS"], "hands": [],
          "market": [["SELL", "WOOL", 5, 1.0], ["SELL", "WOOL", 0, 1.0]]}
    ns["_X1_REPORT"].update(calls=0, changed_turns=0, dropped_dead=0,
                            clamped_orders=0, clamped_qty=0, merged_fragments=0,
                            merged_qty=0, unparsed_kept=0, window_out=0, errors=0)
    o2 = ns["_x1_post"]({"step": 700, "player": 0, "private": {"shed": {}}}, a2)
    if ns["_X1_REPORT"]["dropped_dead"] + ns["_X1_REPORT"]["merged_fragments"] < 1:
        raise RuntimeError("audit④红：X1 卫生未动 %s" % ns["_X1_REPORT"])
    rep["x1_hygiene_ok"] = True
    rep["x1_report"] = dict(ns["_X1_REPORT"])
    # ⑤ 双武装并发：G793 bypass ∧ C3 换表 ∧ X1 同时成立、errors=0
    ns["_G793_STATE"].clear()
    ns["_G793_REPORT"].update(calls=0, classified=0, bypassed=0, errors=0)
    ns["_OC_STATE"].clear()
    st = ns["_oc_state_for"]({"player": 0})
    st["cls"] = "wfr"
    st["locked"] = True
    ns["_OC_C3_SWAPPED"][0] = False
    ns["_IMPL"].chassis.routes = _copy.deepcopy(base_routes)
    r1 = ns["_s793_reorder"](obs_mirror, act)
    ns["_oc_c3_swap"]({"step": 144, "player": 0}, 144)
    r2 = ns["_x1_post"]({"step": 700, "player": 0, "private": {"shed": {}}},
                        {"farmer": ["PASS"], "hands": [],
                         "market": [["SELL", "WOOL", 0, 1.0]]})
    ok = (r1 is act and ns["_G793_REPORT"]["bypassed"] >= 1
          and ns["_OC_C3_SWAPPED"][0]
          and ns["_G793_REPORT"]["errors"] == 0
          and ns["_X1_REPORT"]["errors"] == 0)
    if not ok:
        raise RuntimeError("audit⑤红：双武装探针失败")
    ns["_IMPL"].chassis.routes = base_routes
    rep["dual_armed_ok"] = True
    rep["note"] = ("G793 改卖单置换序（order 轴）、C3 改羊毛落刀相位（timing 轴）、"
                   "X1 改同拍挂量卫生（qty 轴）；三轴正交、状态字典互不共享"
                   "（_G793_* vs _OC_*/_X1_* 零交集），双武装 errors=0")
    return rep
'''


def conflict_audit(base_names, injected_text):
    """静态命名审计（动态双武装探针另行）。"""
    inj_defs = set(re.findall(r"^def (\w+)\(", injected_text, re.M))
    inj_defs |= set(re.findall(r"^([A-Z_][A-Z0-9_]*)\s*=", injected_text))
    shared = sorted(inj_defs & base_names)
    if shared:
        raise RuntimeError("G793 冲突审计红：命名足迹交集 %s" % shared[:10])
    for tok in ("_G793", "_s793_reorder", "gated_fixed_sell_agent",
                "_g793_shape", "_S793_IT"):
        if tok in injected_text:
            raise RuntimeError("G793 冲突审计红：注入块引用宿主保留名 %s" % tok)
    return {"name_footprint_intersection": shared,
            "injected_names": sorted(inj_defs),
            "static_cross_reference_clean": True}


# ------------------------------------------------------------ 构建形态 --
def _pkg(out_dir: Path, data: bytes, manifest: dict):
    tar1 = ba.build_tar_bytes(data)
    if tar1 != ba.build_tar_bytes(data):
        raise RuntimeError("tar 双跑不一致（非可复现）")
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as t:
        names = t.getnames()
        inner = t.extractfile("main.py").read()
    if names != ["main.py"] or inner != data or len(tar1) > SIZE_CAP:
        raise RuntimeError("tar 身份红：%s" % (names,))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "main.py").write_bytes(data)
    (out_dir / "submission.tar.gz").write_bytes(tar1)
    manifest = dict(manifest, main_sha256=sha(data), main_bytes=len(data),
                    tar_sha256=sha(tar1), tar_bytes=len(tar1),
                    tar_members=names, tar_rebuild_reproducible=True,
                    tar_inner_main_matches_disk=True, tar_size_ok=True)
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    return manifest


def build_pure(base_bytes, ext):
    ns: dict = {}
    exec(compile(base_bytes.decode("utf-8"), "<v89pure>", "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    entry = loaded[-1].__name__ if loaded else None
    if entry != V89_ENTRY:
        raise RuntimeError("v89_pure 末 callable=%r 应为 %r" % (entry, V89_ENTRY))
    man = _pkg(BUILD_DIR / "v89_pure", base_bytes, {
        "schema": SCHEMA, "form": "v89_pure",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_notebook": str(NOTEBOOK),
        "source_notebook_sha256": ext["notebook_sha256"],
        "provenance": ("kernels pull haodou092/kaggriculture-harvest-ledger "
                       "2026-09-29（kernel HEAD=V89 Observable Mirror Gate）；"
                       + ext["extraction"] + "；EXPECTED main.py sha 自校验通过"),
        "base_main_sha256": sha(base_bytes),
        "embedded_expected_main_sha256": ext["expected"]["main.py"],
        "byte_identical_to_v89": True, "append_only_prefix_identical": True,
        "entry_last_callable": entry, "entry_expected": V89_ENTRY,
        "compile_ok": True, "layers": [],
        "note": "外部件（haodou 作者后续版 V89）无我方 sha 链锚，身份登记自闭合"
                "（manifest↔盘上↔tar 成员↔内嵌 EXPECTED）"})
    return man


def build_full(base_bytes, base_src):
    c3 = B.build_c3_delta(base_src)
    stats = c3["stats"]
    if (stats["changed_steps"] != C3_EXPECT["changed_steps"]
            or stats["routes_touched"] != C3_EXPECT["routes_touched"]
            or stats["market_slot_touched_steps"] != 0):
        raise RuntimeError("C3 差量漂移（V89 基底）：%s" % (
            {k: stats[k] for k in C3_EXPECT},))
    blob = base64.b85encode(zlib.compress(
        json.dumps(c3["delta"], sort_keys=True).encode(), 9)).decode()
    var_hash = hashlib.sha256(
        json.dumps(c3["delta"], sort_keys=True).encode()).hexdigest()[:16]
    x1_block = BS.build_block(["x1"])
    oc_tail = B.build_tail(OC_CFG, blob)
    text = base_src + BS.SEPARATOR + x1_block + oc_tail
    try:
        compile(text, "<v89full>", "exec")
    except Exception as exc:
        raise RuntimeError("v89_full 语法红: %r" % (exc,))
    ns: dict = {}
    exec(compile(text, "<v89full>", "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    entry = loaded[-1].__name__ if loaded else None
    if entry != FULL_ENTRY:
        raise RuntimeError("v89_full 末 callable=%r 应为 %r" % (entry, FULL_ENTRY))
    if not text.startswith(base_src):
        raise RuntimeError("v89_full 基座前缀漂移")
    probes = B.verify_form(text, base_src, OC_CFG, "v89_full", var_hash)
    base_names = set(re.findall(r"^def (\w+)\(", base_src, re.M)) | set(
        re.findall(r"^([A-Z_][A-Z0-9_]*)\s*=", base_src, re.M))
    audit_static = conflict_audit(base_names, x1_block + oc_tail)
    ns2: dict = {}
    exec(compile(text + "\n" + AUDIT_PROBE_SRC, "<v89full-audit>", "exec"), ns2)
    audit_dyn = ns2["_v89audit_probe"](ns2)
    man = _pkg(BUILD_DIR / "v89_full", text.encode("utf-8"), {
        "schema": SCHEMA, "form": "v89_full",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main_sha256": sha(base_bytes),
        "byte_identical_to_v89": False, "append_only_prefix_identical": True,
        "entry_last_callable": entry, "entry_expected": FULL_ENTRY,
        "compile_ok": True,
        "layers": ["x1_hygiene", "profiler", "c3_wool_phase"],
        "layer_order": "V89 基座 → X1 尾块（build_strongest.build_block 剥件）→ "
                       "oppcond 尾块（画像器+C3；C1/C2 惰性关闭）→ 入口 _hs_agent",
        "profiler_core_sha256": hashlib.sha256(
            B.CORE_SRC.encode()).hexdigest(),
        "c3_delta": {k: stats[k] for k in
                     ("changed_steps", "routes_touched",
                      "market_slot_touched_steps", "change_table_rows")},
        "c3_delta_expected": C3_EXPECT,
        "c3_variant_routes_hash": var_hash,
        "c3_recomputed_on_v89_base": True,
        "probes": {"verify_form": {
            "probe_core": len(probes["probe_core"]),
            "probe_c3": len(probes["probe_c3"]),
            "all_match": all(p["match"] for p in probes["probe_core"])
            and all(p["match"] for p in probes["probe_c3"])},
            "g793_conflict_static": audit_static,
            "g793_conflict_dynamic": audit_dyn},
    })
    return man


def main():
    t0 = time.perf_counter()
    ext = extract_v89()
    base_bytes = ext["files"]["main.py"]
    if sha(base_bytes) != BASE_SHA_EXPECTED:
        raise RuntimeError("V89 main sha 漂移：%s" % sha(base_bytes))
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("V89 本体不以换行收尾（fail-closed）")
    out = {"version": RECORD_VERSION,
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "artifact": {
               "kernel": "haodou092/kaggriculture-harvest-ledger",
               "kernel_version": "V89（notebook 自述：Observable Mirror Gate）",
               "notebook": str(NOTEBOOK),
               "notebook_sha256": ext["notebook_sha256"],
               "extraction": ext["extraction"],
               "embedded_files": {k: {"sha256": ext["expected"][k],
                                      "bytes": len(v)}
                                  for k, v in ext["files"].items()},
               "main_sha256": sha(base_bytes),
               "main_bytes": len(base_bytes),
               "entry_last_callable": V89_ENTRY,
               "diff_vs_v82": ("3 改块（tail wrapper 区 10136-10179）：删 "
                               "pet_any_demand_agent PET_CAFE 倾斜；增 "
                               "_g793_shape/_s793_reorder 覆写/gated_fixed_sell_"
                               "agent——step96-119 镜像谱判门（结构镜像∧现金差≥20"
                               "=cha22 谱特征→跳过投机置换）"),
           }}
    out["forms"] = {"v89_pure": build_pure(base_bytes, ext)}
    out["forms"]["v89_full"] = build_full(base_bytes, base_src)
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (EVID_DIR / "build_v89.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    for k, v in out["forms"].items():
        print(k, v["main_sha256"][:16], v["main_bytes"],
              v["entry_last_callable"], flush=True)
    print("manifest ->", EVID_DIR / "build_v89.json", flush=True)
    return out


if __name__ == "__main__":
    main()
