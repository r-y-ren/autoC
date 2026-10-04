# -*- coding: utf-8 -*-
"""build_r43 及构建面三子件（R26）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：r40 字节解码 →
（组件开关）三手术 → 重编码 → audit_diff_r43_vs_r40 → pack_r43；组件全关=
纯重编码（安慰剂件，须与 r40 字节恒等）；r40 已发射件零改动；零运行时注入。
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
import time
from pathlib import Path
from typing import Any, Dict

MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = MODULE_DIR / "build"
SCHEMA = "orderbook_r43_manifest/1.0"
VARIANT = "r43"
DESCRIPTION = ("public derivative with drain-aligned selling and sheep "
               "lifecycle surgery")
BASE_CHAIN = {
    "a16e0e9b": "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab",
    "r34a": "51fc19dba2d0bcbf2d0a3720c26ff318541a0e6ce5800873bc863f612451aa5b",
    "r37": "23a513f903317e4d6133aea87e5205bd75cab057090e92c162e5c3be8e32707f",
    "r40": "4ce951f088740e0b3d4366dbf95f8bb225817b0417bbb2fcea6292a559ee9ea8",
}
COMPONENTS = ("drain", "gran", "sheep")


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _surgery(text: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """解码→组件开关手术→重编码；返回 {text, change_tables, placebo}。"""
    from orderbook_r37 import retape_sheep as rs  # noqa: WPS433
    from orderbook_r43 import drain_table as dt  # noqa: WPS433
    from orderbook_r43 import retape_drain as rd  # noqa: WPS433
    from orderbook_r43 import retape_gran as rg  # noqa: WPS433
    from orderbook_r43 import retape_sheep as rsl  # noqa: WPS433
    on = {k: bool(config.get(k, True)) for k in COMPONENTS}
    pkg = rs._decode_routes(text)
    tables: Dict[str, Any] = {}
    if on["drain"]:
        drain_tbl = dt.build_drain_table()
        out = rd.retape_drain_aligned(pkg, drain_tbl,
                                      config.get("drain_cfg"))
        pkg, tables["drain_align"] = out["routes"], out["change_table"]
    if on["gran"]:
        out = rg.retape_granularity(pkg, None, config.get("gran_cfg"))
        pkg, tables["granularity"] = out["routes"], out["change_table"]
    if on["sheep"]:
        out = rsl.retape_sheep_lifecycle(pkg, config.get("sheep_cfg"))
        pkg, tables["sheep_lifecycle"] = out["routes"], out["change_table"]
    new_text = rs._encode_routes(text, pkg)
    placebo = not any(on.values())
    if placebo and new_text != text:
        raise RuntimeError("安慰剂件非恒等：纯重编码产生了字节差异")
    return {"text": new_text, "change_tables": tables, "placebo": placebo}


def audit_diff_r43_vs_r40(r43_main: str, r40_main: str,
                          change_tables: Any = None) -> Dict[str, Any]:
    """变更归因审计（白名单=blob 区间差异=三类手术；区间外逐字节同）。
    签名意图：输入: r43 main+r40 main+变更表 / 输出: 归因表 / 错误: 白名单
    外即抛。"""
    from orderbook_r37 import retape_sheep as rs  # noqa: WPS433
    if not isinstance(r43_main, str) or not isinstance(r40_main, str):
        raise TypeError("main 文本须为 str")
    m40 = rs._BLOB_RE.search(r40_main)
    m43 = rs._BLOB_RE.search(r43_main)
    if not m40 or not m43:
        raise RuntimeError("blob 缺失")
    if r40_main[:m40.span(1)[0]] != r43_main[:m43.span(1)[0]] or \
            r40_main[m40.span(1)[1]:] != r43_main[m43.span(1)[1]:]:
        raise RuntimeError("变更越界：blob 区间外存在差异（白名单外）")
    rows = 0
    for name, table in (change_tables or {}).items():
        rows += len(table or [])
    return {
        "whitelist": ["tape_blob_surgery"],
        "kinds": sorted((change_tables or {}).keys()),
        "change_rows": rows,
        "blob_bytes_delta": len(m43.group(1)) - len(m40.group(1)),
        "runtime_block_diff": False,
    }


def _tar_bytes(main_text: str) -> bytes:
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


def pack_r43(r43_main: str, out_dir: Any = None,
             meta: Any = None) -> Dict[str, Any]:
    """确定性打包+manifest（sha 链 …→r37→r40→r43）。签名意图：输入: r43
    main+手术元数据 / 输出: submission.tar.gz+manifest / 错误: 双跑不一致
    即抛。"""
    out = Path(out_dir) if out_dir is not None else DEFAULT_OUT
    out.mkdir(parents=True, exist_ok=True)
    main_path = out / "main.py"
    tar_path = out / "submission.tar.gz"
    man_path = out / "build_manifest.json"
    main_path.write_text(r43_main, encoding="utf-8")
    tar1 = _tar_bytes(r43_main)
    tar2 = _tar_bytes(r43_main)
    if _sha_bytes(tar1) != _sha_bytes(tar2):
        raise RuntimeError("双跑不一致")
    tar_path.write_bytes(tar1)
    mb = main_path.read_bytes()
    tb = tar_path.read_bytes()
    meta = meta if isinstance(meta, dict) else {}
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%d"),
        "variant": VARIANT,
        "description": DESCRIPTION,
        "main_sha256": _sha_bytes(mb),
        "main_bytes": len(mb),
        "tar_sha256": _sha_bytes(tb),
        "tar_bytes": len(tb),
        "tar_members": ["main.py"],
        "double_run_sha256": {"run1": _sha_bytes(tar1),
                              "run2": _sha_bytes(tar2)},
        "base_sha_chain": dict(BASE_CHAIN,
                               **{VARIANT: _sha_bytes(mb)}),
        "surgery": {"kinds": meta.get("kinds", []),
                    "change_rows": meta.get("change_rows", 0),
                    "placebo": bool(meta.get("placebo", False))},
        "complete": True,
    }
    return {"manifest": manifest, "main_path": str(main_path),
            "tar_path": str(tar_path), "man_path": str(man_path),
            "main_sha256": manifest["main_sha256"],
            "tar_sha256": manifest["tar_sha256"]}


def build_r43(r40_main: Any, out_dir: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """构建编排。签名意图：输入: r40 main 路径+组件开关配置 / 输出: r43
    main+manifest+三手术账+变更审计 / 错误: 任一手术守恒破即抛（不产出）。"""
    r40_path = Path(str(r40_main))
    if not r40_path.is_file():
        raise FileNotFoundError("r40 main 不存在: %s" % r40_path)
    cfg = config if isinstance(config, dict) else {}
    base_text = r40_path.read_text(encoding="utf-8")
    out_dir = Path(out_dir) if out_dir is not None else DEFAULT_OUT
    sur = _surgery(base_text, cfg)
    audit = audit_diff_r43_vs_r40(sur["text"], base_text,
                                  sur["change_tables"])
    rows = sum(len(t or []) for t in sur["change_tables"].values())
    packed = pack_r43(sur["text"], out_dir=out_dir, meta={
        "kinds": sorted(sur["change_tables"].keys()), "change_rows": rows,
        "placebo": sur["placebo"]})
    manifest = packed["manifest"]
    if manifest["main_sha256"] != _sha_bytes(
            Path(packed["main_path"]).read_bytes()):
        raise RuntimeError("main sha 自证不符")
    Path(packed["man_path"]).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True)
        + "\n", encoding="utf-8")
    return {
        "main_path": packed["main_path"],
        "tar_path": packed["tar_path"],
        "man_path": packed["man_path"],
        "main_sha256": manifest["main_sha256"],
        "tar_sha256": manifest["tar_sha256"],
        "audit": audit,
        "change_tables": sur["change_tables"],
        "placebo": sur["placebo"],
        "manifest": manifest,
    }
