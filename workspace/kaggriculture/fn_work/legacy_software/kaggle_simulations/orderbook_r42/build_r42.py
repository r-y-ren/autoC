# -*- coding: utf-8 -*-
"""build_r42 及构建面三子件（R25）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：r40 字节为底 →
inject_r42_block → audit_diff_r42_vs_r40 → pack_r42；r40 已发射件零改动。
manifest 沿 r40 形制（orderbook_r42_manifest/1.0，sha 链 a16e0e9b→r34a→
r37→r40→r42；双跑恒等自证）。
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import tarfile
import time
from pathlib import Path
from typing import Any, Dict

MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = MODULE_DIR / "build"
SCHEMA = "orderbook_r42_manifest/1.0"
VARIANT = "r42"
DESCRIPTION = ("public derivative with slot orchestration, endgame "
               "liquidation and mirror gating")
BASE_CHAIN = {
    "a16e0e9b": "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab",
    "r34a": "51fc19dba2d0bcbf2d0a3720c26ff318541a0e6ce5800873bc863f612451aa5b",
    "r37": "23a513f903317e4d6133aea87e5205bd75cab057090e92c162e5c3be8e32707f",
    "r40": "4ce951f088740e0b3d4366dbf95f8bb225817b0417bbb2fcea6292a559ee9ea8",
}


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def audit_diff_r42_vs_r40(r42_main: str, r40_main: str,
                          change_table: Any = None) -> Dict[str, Any]:
    """变更归因审计（白名单一类=尾部运行时块）。签名意图：输入: r42 main+
    r40 main+变更表 / 输出: 归因表 / 错误: 白名单外即抛。"""
    if not isinstance(r42_main, str) or not isinstance(r40_main, str):
        raise TypeError("main 文本须为 str")
    if not r42_main.startswith(r40_main):
        raise RuntimeError("变更越界：r42 非 r40 纯尾部追加（白名单外）")
    tail = r42_main[len(r40_main):]
    tail_sha = _sha_bytes(tail.encode("utf-8"))
    if isinstance(change_table, dict) and change_table.get("block_sha"):
        if change_table["block_sha"] != tail_sha:
            raise RuntimeError("尾块 sha 不符: %s vs %s"
                               % (change_table["block_sha"], tail_sha))
    return {
        "whitelist": ["tail_runtime_block"],
        "tail_block": {"bytes": len(tail.encode("utf-8")),
                       "sha256": tail_sha},
        "base_bytes": len(r40_main.encode("utf-8")),
        "unattributed": [],
    }


def _tar_bytes(main_text: str) -> bytes:
    """确定性 tar.gz（固定 mtime/uid/gid/名序，双跑恒等）。"""
    raw = main_text.encode("utf-8")
    buf = io.BytesIO()
    gz = gzip.GzipFile(fileobj=buf, mode="wb", mtime=0)
    with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tf:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(raw)
        info.mtime = 0
        info.uid = info.gid = 0
        info.uname = info.gname = ""
        info.mode = 0o644
        tf.addfile(info, io.BytesIO(raw))
    gz.close()
    return buf.getvalue()


def pack_r42(r42_main: str, out_dir: Any = None,
             runtime_block: Any = None) -> Dict[str, Any]:
    """确定性打包+manifest（sha 链 …→r37→r40→r42）。签名意图：输入: r42
    main+运行时块元数据 / 输出: submission.tar.gz+manifest / 错误: 双跑不
    一致即抛。"""
    out = Path(out_dir) if out_dir is not None else DEFAULT_OUT
    out.mkdir(parents=True, exist_ok=True)
    main_path = out / "main.py"
    tar_path = out / "submission.tar.gz"
    man_path = out / "build_manifest.json"
    main_path.write_text(r42_main, encoding="utf-8")
    tar1 = _tar_bytes(r42_main)
    tar2 = _tar_bytes(r42_main)
    if _sha_bytes(tar1) != _sha_bytes(tar2):
        raise RuntimeError("双跑不一致")
    tar_path.write_bytes(tar1)
    main_bytes = main_path.read_bytes()
    tar_bytes = tar_path.read_bytes()
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%d"),
        "variant": VARIANT,
        "description": DESCRIPTION,
        "main_sha256": _sha_bytes(main_bytes),
        "main_bytes": len(main_bytes),
        "tar_sha256": _sha_bytes(tar_bytes),
        "tar_bytes": len(tar_bytes),
        "tar_members": ["main.py"],
        "double_run_sha256": {"run1": _sha_bytes(tar1),
                              "run2": _sha_bytes(tar2)},
        "base_sha_chain": dict(BASE_CHAIN,
                               **{VARIANT: _sha_bytes(main_bytes)}),
        "runtime_block": {"present": True,
                          "bytes": int((runtime_block or {})
                                       .get("block_bytes", 0)),
                          "sha256": (runtime_block or {}).get("block_sha")},
        "complete": True,
    }
    return {"manifest": manifest, "main_path": str(main_path),
            "tar_path": str(tar_path), "man_path": str(man_path),
            "main_sha256": manifest["main_sha256"],
            "tar_sha256": manifest["tar_sha256"]}


def build_r42(r40_main: Any, out_dir: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """构建编排。签名意图：输入: r40 main 路径+常量配置 / 输出: r42 main+
    manifest+变更集审计 / 错误: 超白名单即抛。"""
    from orderbook_r42 import inject_r42 as ij  # noqa: WPS433
    r40_path = Path(str(r40_main))
    if not r40_path.is_file():
        raise FileNotFoundError("r40 main 不存在: %s" % r40_path)
    out = Path(out_dir) if out_dir is not None else DEFAULT_OUT
    base_text = r40_path.read_text(encoding="utf-8")
    inj = ij.inject_r42_block(base_text, config)
    text = inj["main_text"]
    audit = audit_diff_r42_vs_r40(text, base_text, inj)
    packed = pack_r42(text, out_dir=out, runtime_block=inj)
    manifest = packed["manifest"]
    # 写盘后自证
    if manifest["main_sha256"] != _sha_bytes(
            Path(packed["main_path"]).read_bytes()):
        raise RuntimeError("main sha 自证不符")
    if not manifest["complete"]:
        raise RuntimeError("manifest 自证不完整")
    Path(packed["man_path"]).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True)
        + "\n", encoding="utf-8")
    return {
        "main_path": packed["main_path"],
        "tar_path": packed["tar_path"],
        "man_path": packed["man_path"],
        "main_sha256": manifest["main_sha256"],
        "tar_sha256": manifest["tar_sha256"],
        "block_sha": inj["block_sha"],
        "audit": audit,
        "manifest": manifest,
    }
