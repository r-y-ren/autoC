# -*- coding: utf-8 -*-
# 【中文】build_v6.py —— R9-G2 assemble_v6_build（v6 确定性装配器）
# ===========================================================================
# v6 = 磁带手术基底 + P2 保险追加块（v4b 旗面形态：P2 on，P1/P3/P4 off）。
#   ① 基底 v48_derivative/main.py（sha256 dadee25a…2664a，107,008B，只读）
#      → 仅替换内嵌 _V48_ROUTES blob 为手术路由（tape_surgery.py 产物；
#      六路由键序/719 长度/事件点切换结构/反应层模块全部原样保留）；
#   ② 追加块复用 build.py 的 build_block（零修改 build.py，importlib 装载），
#      旗面 P2 on 其余 off（v4b 接线先例：blob 只含 P2 源、P1/P3/P4 零接线）。
# 核验（本脚本内自证）：
#   ① 手术基底与基底原文的差分只落在 _V48_ROUTES blob 区间（前缀/后缀
#      逐字节一致）；② 双跑 build_once 确定性；③ P1/P3/P4 token 零在场、
#      P2 token 在场（双旗零接线字节级）；④ blob 只含 P2 源且与 patches/
#      逐字节一致；⑤ tar 单成员 main.py 确定性双打包逐字节一致；⑥ 编译
#      通过；⑦ 路由解码回路（重编码 blob 解回 == routes_surgered.json）。
# 产物：v48_hybrid/v6/{main.py, submission.tar.gz, build_manifest.json,
#   README.md}
# ===========================================================================
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
HYBRID = os.path.dirname(HERE)
KSIM = os.path.dirname(HYBRID)

sys.dont_write_bytecode = True

SUBMIT_MESSAGE_V6 = ("giant-route tape surgery: production-line events "
                     "rescheduled to sheep-heavy giant plan (sell face "
                     "byte-frozen; economic-guard retained)")


def load_build_module():
    spec = importlib.util.spec_from_file_location(
        "v48h_build_mod_v6", os.path.join(HYBRID, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def splice_routes(base_text: str, routes_body: str) -> str:
    """把手术路由 blob 体替换进基底（blob 区间外逐字节不动）。"""
    import re
    import tape_surgery as ts
    m = ts._ROUTES_RE.search(base_text)
    if not m:
        raise SystemExit("base _V48_ROUTES blob not found")
    lo, hi = m.span(1)
    return base_text[:lo] + routes_body + base_text[hi:]


def blob_identity(b, main_bytes: bytes) -> dict:
    """v6 追加块内嵌 blob 只含 P2 源（P1/P3 模块零内嵌），与 patches/ 一致。"""
    import base64
    import zlib
    text = main_bytes.decode("utf-8")
    lines = text.split("\n")
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith("_V48H_MODULES = "))
    chunk = []
    for ln in lines[start + 1:]:
        if ln.startswith("    '") and ln.rstrip().endswith("'"):
            chunk.append(ln.strip()[1:-1])
        elif ln == ")" and chunk:
            break
    if not chunk:
        return {"ok": False, "error": "blob block not found"}
    modules = json.loads(zlib.decompress(
        base64.b85decode("".join(chunk))).decode("utf-8"))
    detail = {}
    for name, src in modules.items():
        fname = "economic_guard.py"
        disk = open(os.path.join(HYBRID, "patches", fname), "rb").read()
        detail[name] = {
            "embedded_sha256": sha256_bytes(src.encode()),
            "disk_sha256": sha256_bytes(disk),
            "identical": src == disk.decode("utf-8"),
        }
    return {"ok": (all(v["identical"] for v in detail.values())
                   and sorted(modules) == ["v48h.p2_economic_guard"]),
            "embedded_modules": sorted(modules),
            "detail": detail}


def build_readme(main_sha, main_bytes, tar_sha, tar_bytes, surg, flags,
                 wiring) -> str:
    lines = []
    a = lines.append
    a("# v6 — 磁带手术候选（R9-G2 perform_tape_surgery + assemble_v6_build）")
    a("")
    a("> 基底 `../../v48_derivative/main.py`（dadee25a…，只读）经"
      "`giant_route/tape_surgery.py` 产线事件手术：六路由内"
      "BUY/BUILD/HIRE/种植事件按 `giant_route/target_schedule.json` 改写；"
      "卖单面/移动骨架/事件点切换结构/反应层（反克隆/槽位重排/终局清仓/"
      "杂草修复）逐字节保留。追加块沿 v4b 旗面（P2 死价保险 on，"
      "P1/P3/P4 off）。本目录产物由 `giant_route/build_v6.py` 确定性生成。")
    a("")
    a("## 身份链")
    a("")
    a("| 件 | sha256 | 字节 |")
    a("|---|---|---|")
    a(f"| 基底（未手术原样） | `{surg['base_sha256']}` | 107008 |")
    a(f"| 手术基底（blob 替换后） | `{surg['surgered_base_sha256']}` | "
      f"{surg['surgered_base_bytes']} |")
    a(f"| v6 `main.py`（手术基底 + P2 追加块） | `{main_sha}` | "
      f"{main_bytes} |")
    a(f"| `submission.tar.gz` | `{tar_sha}` | {tar_bytes} |")
    a("")
    a(f"开关：P1/P3/P4 off、P2 on（v4b 接线形态）；手术差分 "
      f"{surg['diff_entries']} 条（hires/buys/plants/land），编辑 "
      f"{surg['edits']} 处——明细 `../giant_route/surgery_diff.json`。")
    a("")
    a("## 门禁（四门冒烟结果回填）")
    a("")
    a("| 门 | 判据 | 结果 |")
    a("|---|---|---|")
    a("| gate1 官方装载语义 | 干净 -I 子进程 get_last_callable 复刻一致 | "
      "PENDING |")
    a("| gate2 双席自打 | seeds 101/102 双局 720 回合 DONE、每步 <1000ms | "
      "PENDING |")
    a("| gate3 确定性 | seed101 重跑动作流哈希逐字节一致 | PENDING |")
    a("| gate4 体积 | tar ≤ 100MB | PENDING |")
    a("")
    a("结构性门禁（h2h/seated/胜局回归/经济面）属 R9-G4 "
      "verify_structure_gates，不在本装配器内。")
    a("")
    return "\n".join(lines) + "\n"


def main() -> int:
    import tape_surgery as ts
    b = load_build_module()

    # ① 手术基底
    routes, base_text, span = ts.decode_routes()
    base_bytes = base_text.encode("utf-8")
    new_routes = json.load(open(os.path.join(HERE, "routes_surgered.json"),
                                encoding="utf-8"))
    body, payload = ts.encode_routes(new_routes)
    surg_base_text = splice_routes(base_text, body)
    surg_base = surg_base_text.encode("utf-8")
    compile(surg_base, "main.py", "exec")
    # 解码回路
    import base64
    import re
    import zlib
    m = ts._ROUTES_RE.search(surg_base_text)
    blob = "".join(re.findall(r"'([^']*)'", m.group(1)))
    back = json.loads(zlib.decompress(
        base64.b85decode(blob)).decode("utf-8"))
    if back != new_routes:
        raise SystemExit("route re-encode roundtrip mismatch")
    # blob 区间外逐字节一致（前缀截止点与后缀起点的原文 span 为准）
    lo = span[0]
    hi_new = m.span(1)[1]
    if surg_base_text[:lo] != base_text[:lo] or \
            surg_base_text[hi_new:] != base_text[span[1]:]:
        raise SystemExit("surgery leaked outside the routes blob span")

    # ② P2-only 追加块（build.py 旗面机制，基底 text = 手术基底）
    flags = {"P1": False, "P2": True, "P3": False, "P4": False}
    patch_sources, patch_shas = {}, {}
    for key in b.PATCH_ORDER:
        raw = open(os.path.join(b.PATCH_DIR, b.PATCHES[key]["source"]),
                   "rb").read()
        patch_sources[key] = raw.decode("utf-8")
        patch_shas[key] = b.sha256_bytes(raw)
    first = surg_base + b.build_block(flags, surg_base_text,
                                      patch_sources, patch_shas
                                      ).encode("utf-8")
    second = surg_base + b.build_block(flags, surg_base_text,
                                       patch_sources, patch_shas
                                       ).encode("utf-8")
    if first != second:
        raise SystemExit("build is not deterministic")
    compile(first, "main.py", "exec")

    # ③ 零接线验证（P1/P3/P4 token 零在场；P2 在场）
    v6_text = first.decode("utf-8")
    wiring = {}
    for key in ("P1", "P2", "P3", "P4"):
        toks = b.PATCHES[key]["tokens"]
        hits = {t: v6_text.count(t) for t in toks}
        if key == "P2":
            ok = all(v >= 1 for v in hits.values())
        else:
            ok = all(v == 0 for v in hits.values())
        wiring[key] = {"v6_token_hits": hits, "ok": ok}
        if not ok:
            raise SystemExit(f"wiring verification failed for {key}")

    # ④ blob 身份（只含 P2）
    ident = blob_identity(b, first)
    if not ident["ok"]:
        raise SystemExit("patch blob identity verification failed")

    # ⑤ 前缀检查（v6 = 手术基底逐字前缀 + 追加块）
    if not first.startswith(surg_base):
        raise SystemExit("v6 main.py is not a byte-verbatim surgered-base "
                         "prefix")

    # ⑥ 确定性打包
    tar_bytes = b.pack_tar(first)
    if b.pack_tar(first) != tar_bytes:
        raise SystemExit("tar packing is not deterministic")
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as t:
        names = t.getnames()
        inner = t.extractfile("main.py").read()
    if names != ["main.py"] or inner != first:
        raise SystemExit("tar member/byte mismatch")

    # 产物落盘 v6/
    out_dir = os.path.join(HYBRID, "v6")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "main.py"), "wb") as h:
        h.write(first)
    with open(os.path.join(out_dir, "submission.tar.gz"), "wb") as h:
        h.write(tar_bytes)

    surg_report = json.load(open(os.path.join(HERE, "surgery_report.json"),
                                 encoding="utf-8"))
    surg = {
        "base_sha256": surg_report["base_sha256"],
        "surgered_base_sha256": sha256_bytes(surg_base),
        "surgered_base_bytes": len(surg_base),
        "diff_entries": surg_report["diff_entries"],
        "edits": surg_report["edits"],
    }
    manifest = {
        "variant": {
            "name": "v6",
            "assembler": "giant_route/build_v6.py",
            "rationale": "R9 giant-route 结构梯：磁带产线事件手术"
                         "（sheep-heavy 排程）+ P2 死价保险（v4b 旗面形态）；"
                         "卖单面/反应层/事件点切换结构逐字节保留",
        },
        "base": {"path": "software/kaggle_simulations/v48_derivative/main.py",
                 "sha256": b.BASE_SHA256, "bytes": b.BASE_BYTES_EXPECT,
                 "verbatim_prefix": False,
                 "note": "前缀非逐字：_V48_ROUTES blob 区间被手术路由替换，"
                         "区间外逐字节一致（build_v6.py 自证）"},
        "tape_surgery": {
            "tool": "giant_route/tape_surgery.py",
            "schedule": "giant_route/target_schedule.json",
            "routes_blob_span": [lo, hi_new],
            "surgered_base_sha256": surg["surgered_base_sha256"],
            "routes_json_sha256": sha256_bytes(json.dumps(
                new_routes, sort_keys=True).encode()),
            "diff_entries": surg["diff_entries"],
            "edits": surg["edits"],
            "report": "giant_route/surgery_report.json",
            "preserved": ["SELL orders (byte-identical per route)",
                          "movement verbs (farmer+hands, byte-identical)",
                          "route switch points 88/120/153/216 + router "
                          "modules (byte-identical)",
                          "reaction layers: anti-clone preemptive sell / "
                          "sell-slot reorder / terminal liquidation / weed "
                          "repair (byte-identical)"],
        },
        "patches": {key: {"module": b.PATCHES[key]["module"],
                          "source": f"patches/{b.PATCHES[key]['source']}",
                          "sha256": patch_shas[key],
                          "role": b.PATCHES[key]["role"],
                          "embedded": key == "P2"}
                    for key in b.PATCH_ORDER},
        "flags": {"P1_ON": False, "P2_ON": True, "P3_ON": False,
                  "P4_ON": False},
        "flag_off_zero_wiring": {k: wiring[k]["ok"]
                                 for k in ("P1", "P3", "P4")},
        "wiring_check_detail": wiring,
        "blob_identity": ident,
        "main_py": {"bytes": len(first), "sha256": sha256_bytes(first),
                    "surgered_base_prefix_bytes": len(surg_base)},
        "submission_tar_gz": {"bytes": len(tar_bytes),
                              "sha256": sha256_bytes(tar_bytes),
                              "members": names,
                              "deterministic_double_pack": True},
        "deterministic_double_build": True,
        "stdlib_only": True,
        "submit_message": SUBMIT_MESSAGE_V6,
        "gate_results": {"status": "PENDING",
                         "note": "四门冒烟由 giant_route/fourgate_v6.py 回填；"
                                 "结构五线属 R9-G4"},
    }
    with open(os.path.join(out_dir, "build_manifest.json"), "w",
              encoding="utf-8") as h:
        json.dump(manifest, h, ensure_ascii=False, indent=2, sort_keys=True)
        h.write("\n")

    readme = build_readme(sha256_bytes(first), len(first),
                          sha256_bytes(tar_bytes), len(tar_bytes), surg,
                          flags, wiring)
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8") as h:
        h.write(readme)

    print(json.dumps({
        "v6_main_sha256": manifest["main_py"]["sha256"],
        "v6_main_bytes": manifest["main_py"]["bytes"],
        "v6_tar_sha256": manifest["submission_tar_gz"]["sha256"],
        "v6_tar_bytes": manifest["submission_tar_gz"]["bytes"],
        "surgered_base_sha256": surg["surgered_base_sha256"],
        "wiring_ok": {k: v["ok"] for k, v in wiring.items()},
        "blob_ok": ident["ok"],
        "out": out_dir,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
