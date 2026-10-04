# -*- coding: utf-8 -*-
"""build_k1（iterk K1）：H1 底 + 毛期错峰手术构建线（判决先行·不发射）。

责任口径（任务 K1）：构建底=orderbook_strongest_lab/build/h1/main.py（H1 件
字节，sha 76b5f842…）零改动读入；两形态：
- h1_base：H1 原样复制（字节恒等对照底）；
- k1：H1 磁带区经 layer_k1.retape_phase_offset 错峰手术（剪毛刀 d17/20/23/26
  → d+1/d+2，d29 保留；量守恒零跨拍）+ 变更表注释内嵌（单行 blob 外追加）。

校验（fail-closed 不产出）：①构建底 sha 恒等 ②手术后 blob 外字节零漂移
（_encode_routes 自检链）③compile ④exec 装载末 callable=_hs_agent（入口
语义保持）⑤逐格刀次守恒+市场单槽恒等（layer_k1 手术内置核算）。
只写 orderbook_iterk_lab/。
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
from orderbook_iterk_lab import layer_k1 as k1  # noqa: E402
from orderbook_r37 import retape_sheep as rs  # noqa: E402

H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
H1_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb676497"
                  "4b22f337")
BUILD_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
ENTRY_NAME = "_hs_agent"
SCHEMA = "orderbook_iterk_lab_build/1.0"


def _manifest_for(path: Path, base_sha: str, extra: dict) -> dict:
    data = path.read_bytes()
    return {
        "form": path.parent.name,
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "base_main_sha256": base_sha,
        "entry": ENTRY_NAME,
        **extra,
    }


def _check_entry(text: str, form: str) -> None:
    ns: dict = {}
    try:
        exec(compile(text, "<iterk:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验③红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 %s: 末 callable=%r 应为 %r"
                           % (form, got, ENTRY_NAME))


def main() -> dict:
    base_bytes = H1_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != H1_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（H1 件字节漂移）：%s" % base_sha)
    base_text = base_bytes.decode("utf-8")
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    # ---- h1_base：字节恒等复制 ----
    h1_dir = BUILD_DIR / "h1_base"
    h1_dir.mkdir(parents=True, exist_ok=True)
    (h1_dir / "main.py").write_bytes(base_bytes)
    _check_entry(base_text, "h1_base")

    # ---- k1：错峰手术（写时复制；blob 外零漂移由 _encode_routes 自检链）----
    pkg = rs._decode_routes(base_text)
    before_counts = k1.static_shear_day_counts(pkg)
    result = k1.retape_phase_offset(pkg)
    after_counts = k1.static_shear_day_counts(result["routes"])
    new_text = rs._encode_routes(base_text, result["routes"])
    try:
        compile(new_text, "<iterk:k1>", "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 k1: compile 失败: %r" % exc)
    _check_entry(new_text, "k1")

    k1_dir = BUILD_DIR / "k1"
    k1_dir.mkdir(parents=True, exist_ok=True)
    (k1_dir / "main.py").write_text(new_text, encoding="utf-8")
    change_table = result["change_table"]

    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(H1_MAIN),
        "base_main_sha256": base_sha,
        "layer": "layer_k1.retape_phase_offset（最小磁带手术：剪毛刀错峰）",
        "semantics": {
            "public_phase": list(k1.PUBLIC_PHASE),
            "move_days": list(k1.MOVE_DAYS),
            "keep_days": list(k1.KEEP_DAYS),
            "targets": list(k1.DEFAULT_TARGETS),
            "量守恒": "逐格刀次守恒（每产毛单位仍收一次；d29 保留刀）",
            "零跨拍": "市场单槽零触碰（订单槽不删/不移/不填）",
            "fallback": "逐刀独立手术失败保原刀（per-cut fallback）",
        },
        "stats": result["stats"],
        "static_shear_day_counts": {
            "caliber": "磁带口径逐日刀次（41 路由合计，_shear_cells 格位口径）",
            "before": before_counts,
            "after": after_counts,
        },
        "change_table_rows": len(change_table),
        "forms": {},
    }
    manifest["forms"]["h1_base"] = _manifest_for(
        h1_dir / "main.py", base_sha,
        {"byte_identical_to_H1": True, "layers": []})
    manifest["forms"]["k1"] = _manifest_for(
        k1_dir / "main.py", base_sha,
        {"byte_identical_to_H1": False, "layers": ["k1_shear_phase"],
         "blob_surgery": True})
    (EVID_DIR / "build_k1_realrun.json").write_text(
        json.dumps({"manifest": manifest, "change_table": change_table},
                   ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    (h1_dir / "build_manifest.json").write_text(
        json.dumps(manifest["forms"]["h1_base"], ensure_ascii=False,
                   indent=1) + "\n", encoding="utf-8")
    (k1_dir / "build_manifest.json").write_text(
        json.dumps(manifest["forms"]["k1"], ensure_ascii=False,
                   indent=1) + "\n", encoding="utf-8")
    print("h1_base", manifest["forms"]["h1_base"]["main_sha256"][:16])
    print("k1     ", manifest["forms"]["k1"]["main_sha256"][:16],
          "moved", result["stats"]["moved"], "/", result["stats"]["phase_cuts"])
    print("evidence ->", EVID_DIR / "build_k1_realrun.json")
    return manifest


if __name__ == "__main__":
    main()
