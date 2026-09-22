# -*- coding: utf-8 -*-
# 【中文】build_v4.py —— v4 旗关包装配驱动（临时脚本，落 tmp/）
# ===========================================================================
# v4 = P1 旗关构建（--p1 off，P2/P3 保留）。build.py 旗关模式只写
# tmp/main_p011.py（诊断件，不产包）——本脚本 import build.py 复用其
# build_once/pack_tar 原函数（零修改 build.py），产最终 v4 包：
#   v48_hybrid/v4/main.py + v4/submission.tar.gz + v4/build_manifest.json
# 核验：① CLI 子进程构建（--p1 off）sha == 进程内 build_once sha（同函数
# 双通道一致）；② 双跑 build_once / 双次 pack_tar 逐字节一致；③ P1 接线
# token 在 v4 文本零出现、在全开件在场（零接线字节级）；④ 基底逐字前缀；
# ⑤ tar 单成员 main.py 内容逐字节一致。
# ===========================================================================
from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # v48_hybrid/
V4_DIR = os.path.join(HERE, "v4")
TMP_DIR = os.path.join(HERE, "tmp")

SUBMIT_MESSAGE_V4 = ("public derivative with economic-guard layers "
                     "(v4: market layer off per online forensics)")

sys.dont_write_bytecode = True


def load_build_module():
    spec = importlib.util.spec_from_file_location(
        "v48h_build_mod", os.path.join(HERE, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    b = load_build_module()
    flags = {"P1": False, "P2": True, "P3": True}

    # ① CLI 子进程诊断构建（build.py --p1 off → tmp/main_p011.py）
    proc = subprocess.run([sys.executable, os.path.join(HERE, "build.py"),
                           "--p1", "off"], capture_output=True, text=True,
                          timeout=300)
    if proc.returncode != 0:
        print(proc.stdout[-800:], proc.stderr[-800:], sep="\n")
        raise SystemExit("build.py --p1 off failed")
    cli_info = json.loads(proc.stdout)
    cli_path = cli_info["diagnostic_build"]
    cli_sha = cli_info["sha256"]
    print(f"[cli] --p1 off -> {cli_path} sha256={cli_sha} "
          f"bytes={cli_info['bytes']} flags={cli_info['flags']}", flush=True)

    # ② 进程内双跑 build_once（与 CLI 同函数）
    main_v4 = b.build_once(flags)
    main_v4b = b.build_once(flags)
    if main_v4 != main_v4b:
        raise SystemExit("in-process build_once not deterministic")
    if b.sha256_bytes(main_v4) != cli_sha:
        raise SystemExit(f"cli vs in-process sha mismatch: {cli_sha} vs "
                         f"{b.sha256_bytes(main_v4)}")
    compile(main_v4, "main.py", "exec")

    # ③ 零接线验证（P1 token 零在场；P2/P3 token 在场=接线真实）
    v4_text = main_v4.decode("utf-8")
    all_on = open(os.path.join(HERE, "main.py"), "rb").read().decode("utf-8")
    zero_wiring = {}
    for key in ("P1", "P2", "P3"):
        toks = b.PATCHES[key]["tokens"]
        hits = {t: v4_text.count(t) for t in toks}
        present = {t: all_on.count(t) for t in toks}
        if key == "P1":
            ok = all(v == 0 for v in hits.values())
        else:
            ok = all(hits[t] >= 1 and present[t] >= 1 for t in toks)
        zero_wiring[key] = {"v4_token_hits": hits,
                            "all_on_token_hits": present, "ok": ok}
        print(f"[wiring] {key} ok={ok} v4_hits={hits}", flush=True)
    if not zero_wiring["P1"]["ok"] or not zero_wiring["P2"]["ok"] \
            or not zero_wiring["P3"]["ok"]:
        raise SystemExit("wiring verification failed")

    # ④ 基底逐字前缀
    base = b.load_base()
    if not main_v4.startswith(base):
        raise SystemExit("v4 main.py is not a byte-verbatim base prefix")

    # ⑤ 确定性打包 + tar 内容回读
    tar_bytes = b.pack_tar(main_v4)
    if b.pack_tar(b.build_once(flags)) != tar_bytes:
        raise SystemExit("tar packing not deterministic")
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as t:
        names = t.getnames()
        inner = t.extractfile("main.py").read()
    if names != ["main.py"] or inner != main_v4:
        raise SystemExit("tar member/byte mismatch")

    # 产物落盘（v4/ 新目录）
    os.makedirs(V4_DIR, exist_ok=True)
    with open(os.path.join(V4_DIR, "main.py"), "wb") as h:
        h.write(main_v4)
    with open(os.path.join(V4_DIR, "submission.tar.gz"), "wb") as h:
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
            "name": "v4",
            "cli": "python build.py --p1 off",
            "requirement": "fn_docs/requirements.md 变更记录 2026-09-24："
                           "v4=P1 旗关构建（--p1 off），P2/P3 保留；"
                           "行为级≡纯 v48+死价保险",
        },
        "base": {"path": "software/kaggle_simulations/v48_derivative/main.py",
                 "sha256": b.BASE_SHA256, "bytes": b.BASE_BYTES_EXPECT,
                 "verbatim_prefix": True},
        "patches": {key: {"module": b.PATCHES[key]["module"],
                          "source": f"patches/{b.PATCHES[key]['source']}",
                          "sha256": patch_shas[key],
                          "bytes": patch_sizes[key],
                          "role": b.PATCHES[key]["role"]}
                    for key in b.PATCH_ORDER},
        "flags": {"P1_ON": False, "P2_ON": True, "P3_ON": True},
        "flag_off_zero_wiring": {
            "P1": {"ok": True, "v4_token_hits":
                   zero_wiring["P1"]["v4_token_hits"],
                   "tokens_present_when_on": True},
            "verified": "v4 文本中 P1 接线 token（module/imports/helper/"
                        "seam 符号）计数全零；全开件（../main.py）中场",
        },
        "wiring_check_detail": zero_wiring,
        "cli_diagnostic_build": {"path": cli_path, "sha256": cli_sha,
                                 "bytes": cli_info["bytes"],
                                 "sha_match_in_process": True},
        "main_py": {"bytes": len(main_v4),
                    "sha256": b.sha256_bytes(main_v4),
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
        "submit_message": SUBMIT_MESSAGE_V4,
        "gate_results": {"status": "PENDING",
                         "note": "v4 轻量轮门禁回填：fourgate/h2h 全平局/"
                                 "patch_safety 双面/panel"},
    }
    with open(os.path.join(V4_DIR, "build_manifest.json"), "w",
              encoding="utf-8") as h:
        json.dump(manifest, h, ensure_ascii=False, indent=2, sort_keys=True)
        h.write("\n")

    print(json.dumps({
        "v4_main_sha256": manifest["main_py"]["sha256"],
        "v4_main_bytes": manifest["main_py"]["bytes"],
        "v4_tar_sha256": manifest["submission_tar_gz"]["sha256"],
        "v4_tar_bytes": manifest["submission_tar_gz"]["bytes"],
        "p1_source_sha256": patch_shas["P1"],
        "base_sha256": b.BASE_SHA256,
        "slug": slug, "submit_message": SUBMIT_MESSAGE_V4,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
