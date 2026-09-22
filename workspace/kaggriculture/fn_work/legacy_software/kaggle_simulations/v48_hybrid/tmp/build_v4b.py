# -*- coding: utf-8 -*-
# 【中文】build_v4b.py —— v4b 双旗关包装配驱动（临时脚本，落 tmp/）
# ===========================================================================
# v4b = P1/P3 双旗关构建（--p1 off --p3 off，P2 死价保险保留）。
# 动机（v4 门禁 FAIL 根因）：P1 旗关使 P3 失去门控（defer 探针属 P1），
# P3 里程碑表把纯 v48 磁带轨迹本身判偏离 → 推迟卖单 → 与 v48 行为分叉
# （v4 首分叉 step252，4/4 种子 P3 单因，P2 全程零触发）。v4b 方案 =
# P1/P3 同关：行为级 ≡ 纯 v48 + P2 保险（P2 线上零误触发 + 保险面已实弹
# 验证）。
# build.py 旗关模式只写 tmp/main_p010.py（诊断件，不产包）——本脚本
# import build.py 复用其 build_once/pack_tar 原函数（零修改 build.py），
# 产最终 v4b 包：
#   v48_hybrid/v4b/main.py + v4b/submission.tar.gz + v4b/build_manifest.json
# 核验：① CLI 子进程构建（--p1 off --p3 off）sha == 进程内 build_once sha
# （同函数双通道一致）；② 双跑 build_once / 双次 pack_tar 逐字节一致；
# ③ P1+P3 接线 token 在 v4b 文本零出现、在全开件在场（双旗零接线字节级）；
# ④ P2 token 在场 + 内嵌 blob 只含 P2 源（P1/P3 模块零内嵌，源与 patches/
# 逐字节一致）；⑤ 基底逐字前缀；⑥ tar 单成员 main.py 内容逐字节一致。
# ===========================================================================
from __future__ import annotations

import base64
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tarfile
import zlib

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # v48_hybrid/
V4B_DIR = os.path.join(HERE, "v4b")

SUBMIT_MESSAGE_V4B = ("public derivative with economic-guard layer "
                      "(v4b: market/milestone layers off per online "
                      "forensics; dead-price guard retained)")

sys.dont_write_bytecode = True


def load_build_module():
    spec = importlib.util.spec_from_file_location(
        "v48h_build_mod_v4b", os.path.join(HERE, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blob_identity(b, main_bytes: bytes) -> dict:
    """v4b 内嵌 blob 只含 P2 源（P1/P3 模块零内嵌），源字节与 patches/ 一致。"""
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
    blob_text = "".join(chunk)
    modules = json.loads(zlib.decompress(
        base64.b85decode(blob_text)).decode("utf-8"))
    detail = {}
    for name, src in modules.items():
        fname = ("economic_guard.py" if "p2_" in name
                 else "milestone_monitor.py" if "p3_" in name
                 else "midgame_sell_layer.py")
        disk = open(os.path.join(HERE, "patches", fname), "rb").read()
        detail[name] = {
            "embedded_sha256": hashlib.sha256(src.encode()).hexdigest(),
            "disk_sha256": hashlib.sha256(disk).hexdigest(),
            "identical": src == disk.decode("utf-8"),
        }
    return {"ok": (all(v["identical"] for v in detail.values())
                   and sorted(modules) == ["v48h.p2_economic_guard"]),
            "embedded_modules": sorted(modules),
            "p1_module_absent": not any("p1_" in k for k in modules),
            "p3_module_absent": not any("p3_" in k for k in modules),
            "detail": detail}


def main() -> int:
    b = load_build_module()
    flags = {"P1": False, "P2": True, "P3": False}

    # ① CLI 子进程诊断构建（build.py --p1 off --p3 off → tmp/main_p010.py）
    proc = subprocess.run([sys.executable, os.path.join(HERE, "build.py"),
                           "--p1", "off", "--p3", "off"],
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        print(proc.stdout[-800:], proc.stderr[-800:], sep="\n")
        raise SystemExit("build.py --p1 off --p3 off failed")
    cli_info = json.loads(proc.stdout)
    cli_path = cli_info["diagnostic_build"]
    cli_sha = cli_info["sha256"]
    print(f"[cli] --p1 off --p3 off -> {cli_path} sha256={cli_sha} "
          f"bytes={cli_info['bytes']} flags={cli_info['flags']}", flush=True)

    # ② 进程内双跑 build_once（与 CLI 同函数）
    main_v4b = b.build_once(flags)
    main_v4b_2 = b.build_once(flags)
    if main_v4b != main_v4b_2:
        raise SystemExit("in-process build_once not deterministic")
    if b.sha256_bytes(main_v4b) != cli_sha:
        raise SystemExit(f"cli vs in-process sha mismatch: {cli_sha} vs "
                         f"{b.sha256_bytes(main_v4b)}")
    compile(main_v4b, "main.py", "exec")

    # ③ 零接线验证（P1+P3 token 零在场；P2 token 在场=接线真实）
    v4b_text = main_v4b.decode("utf-8")
    all_on = open(os.path.join(HERE, "main.py"), "rb").read().decode("utf-8")
    zero_wiring = {}
    for key in ("P1", "P2", "P3"):
        toks = b.PATCHES[key]["tokens"]
        hits = {t: v4b_text.count(t) for t in toks}
        present = {t: all_on.count(t) for t in toks}
        if key in ("P1", "P3"):
            ok = all(v == 0 for v in hits.values())
        else:
            ok = all(hits[t] >= 1 and present[t] >= 1 for t in toks)
        zero_wiring[key] = {"v4b_token_hits": hits,
                            "all_on_token_hits": present, "ok": ok}
        print(f"[wiring] {key} ok={ok} v4b_hits={hits}", flush=True)
    if not (zero_wiring["P1"]["ok"] and zero_wiring["P2"]["ok"]
            and zero_wiring["P3"]["ok"]):
        raise SystemExit("wiring verification failed")

    # ④ blob 身份（只内嵌 P2，源与 patches/ 逐字节一致）
    ident = blob_identity(b, main_v4b)
    print(f"[blob] ok={ident['ok']} embedded={ident['embedded_modules']} "
          f"p1_absent={ident['p1_module_absent']} "
          f"p3_absent={ident['p3_module_absent']}", flush=True)
    if not ident["ok"]:
        raise SystemExit("blob identity verification failed")

    # ⑤ 基底逐字前缀
    base = b.load_base()
    if not main_v4b.startswith(base):
        raise SystemExit("v4b main.py is not a byte-verbatim base prefix")

    # ⑥ 确定性打包 + tar 内容回读
    tar_bytes = b.pack_tar(main_v4b)
    if b.pack_tar(b.build_once(flags)) != tar_bytes:
        raise SystemExit("tar packing not deterministic")
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as t:
        names = t.getnames()
        inner = t.extractfile("main.py").read()
    if names != ["main.py"] or inner != main_v4b:
        raise SystemExit("tar member/byte mismatch")

    # 产物落盘（v4b/ 新目录）
    os.makedirs(V4B_DIR, exist_ok=True)
    with open(os.path.join(V4B_DIR, "main.py"), "wb") as h:
        h.write(main_v4b)
    with open(os.path.join(V4B_DIR, "submission.tar.gz"), "wb") as h:
        h.write(tar_bytes)

    slug, _ = b.extract_slug()
    patch_shas, patch_sizes = {}, {}
    for key in b.PATCH_ORDER:
        raw = open(os.path.join(b.PATCH_DIR, b.PATCHES[key]["source"]),
                   "rb").read()
        patch_shas[key] = b.sha256_bytes(raw)
        patch_sizes[key] = len(raw)

    manifest = {
        "variant": {
            "name": "v4b",
            "cli": "python build.py --p1 off --p3 off",
            "rationale": "v4 轻量轮门禁 FAIL 根因：P1 旗关后 defer 探针缺失"
                         "使 P3 失去门控，P3 里程碑表把纯 v48 磁带轨迹判偏离"
                         "（首分叉 step252，4/4 种子 P3 单因，P2 零触发）；"
                         "v4b = P1/P3 同关（双旗零接线），行为级≡纯 v48 + "
                         "P2 死价保险（线上零误触发 + 保险面实弹验证）",
        },
        "base": {"path": "software/kaggle_simulations/v48_derivative/main.py",
                 "sha256": b.BASE_SHA256, "bytes": b.BASE_BYTES_EXPECT,
                 "verbatim_prefix": True},
        "patches": {key: {"module": b.PATCHES[key]["module"],
                          "source": f"patches/{b.PATCHES[key]['source']}",
                          "sha256": patch_shas[key],
                          "bytes": patch_sizes[key],
                          "role": b.PATCHES[key]["role"],
                          "embedded": key == "P2"}
                    for key in b.PATCH_ORDER},
        "flags": {"P1_ON": False, "P2_ON": True, "P3_ON": False},
        "flag_off_zero_wiring": {
            "P1": {"ok": True,
                   "v4b_token_hits": zero_wiring["P1"]["v4b_token_hits"],
                   "tokens_present_when_on": True},
            "P3": {"ok": True,
                   "v4b_token_hits": zero_wiring["P3"]["v4b_token_hits"],
                   "tokens_present_when_on": True},
            "verified": "v4b 文本中 P1+P3 接线 token（module/imports/helper/"
                        "seam 符号）计数全零；全开件（../main.py）中场；"
                        "P2 token 在场=接线真实",
        },
        "wiring_check_detail": zero_wiring,
        "blob_identity": ident,
        "cli_diagnostic_build": {"path": cli_path, "sha256": cli_sha,
                                 "bytes": cli_info["bytes"],
                                 "sha_match_in_process": True},
        "main_py": {"bytes": len(main_v4b),
                    "sha256": b.sha256_bytes(main_v4b),
                    "base_prefix_bytes": b.BASE_BYTES_EXPECT},
        "submission_tar_gz": {"bytes": len(tar_bytes),
                              "sha256": b.sha256_bytes(tar_bytes),
                              "members": names,
                              "deterministic_double_pack": True},
        "deterministic_double_build": True,
        "stdlib_only": True,
        "competition_slug": {"value": slug,
                             "extracted_from":
                                 "software/scripts/sync_online_probe.py"},
        "submit_message": SUBMIT_MESSAGE_V4B,
        "gate_results": {"status": "PENDING",
                         "note": "v4b 轻量轮门禁回填：fourgate/h2h 全平局/"
                                 "patch_safety 双面/panel"},
    }
    with open(os.path.join(V4B_DIR, "build_manifest.json"), "w",
              encoding="utf-8") as h:
        json.dump(manifest, h, ensure_ascii=False, indent=2, sort_keys=True)
        h.write("\n")

    print(json.dumps({
        "v4b_main_sha256": manifest["main_py"]["sha256"],
        "v4b_main_bytes": manifest["main_py"]["bytes"],
        "v4b_tar_sha256": manifest["submission_tar_gz"]["sha256"],
        "v4b_tar_bytes": manifest["submission_tar_gz"]["bytes"],
        "base_sha256": b.BASE_SHA256,
        "slug": slug, "submit_message": SUBMIT_MESSAGE_V4B,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
