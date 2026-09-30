# -*- coding: utf-8 -*-
"""build_expx_v2：MODELPX 预测核精确化 + 胜位守卫构建线（判决先行·不发射
不提交）。

与 build_expx 同一内层手术（MODELPX 的 p_next 计算 4 处同文替换，反替换
回程逐字节=基座 3f8b57fd… 封印），尾块换 expx_layer_v2（胜位守卫）：
- ① 窗收缩：expx 仅 step 144-648 生效，648 后全基线语义（终局库存形态回归）；
- ② 滞留保险：MR 持有时若自家模型窗内峰值出货容量清不掉该件投射仓存量
  →立即按基线语义出货（防末局滞留）。
校验同 build_expx（①替换计数 4/1/3 ②反替换回程=基座源 ③compile ④exec
末 callable=_expx_agent 且 _EXPX_HOST=_hs_agent ⑤基座 sha 恒等 ⑥门字面量
4 处不动）+ ⑦守卫参数与形态一致（WIN_END=648/TERM=718/K=12）。
只写 orderbook_expx_lab/。
"""
from __future__ import annotations

import hashlib
import io
import json
import tarfile
import time
from pathlib import Path

import build_expx as B1

MODULE_DIR = Path(__file__).resolve().parent
BASE_MAIN = B1.BASE_MAIN
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_expx_lab_manifest_v2/1.0"

SENTINEL = '"""expx-v2 MODELPX 预测核精确化+胜位守卫实验尾块'
ENTRY_NAME = "_expx_agent"
HOST_NAME = "_hs_agent"
LAYER_FILE = "expx_layer_v2.py"
K_TOKEN = "__EXPX_K__"
WIN_END_TOKEN = "__EXPX_WIN_END__"
TERM_TOKEN = "__EXPX_TERM__"
HORIZON_K = 12
WIN_END = 648
TERM = 718

LAYER_LABEL = ("件 EXPX-V2=MODELPX 预测核精确化+胜位守卫（v1 同式 K=12 拍"
               "精确投影/峰值拍出货/边际收益定单量；加 ①窗收缩 step144-648"
               "生效 648 后全基线语义 ②滞留保险 MR 持有时模型窗内峰值容量"
               "清不掉该件即按基线出货；异常回退基线语义；零跨拍挪量、磁带 "
               "blob 零触碰）")


def build_block_v2():
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    for tok, val in ((K_TOKEN, HORIZON_K), (WIN_END_TOKEN, WIN_END),
                     (TERM_TOKEN, TERM)):
        if tok not in layer_src:
            raise RuntimeError("expx_layer_v2 缺占位 %s" % tok)
        layer_src = layer_src.replace(tok, str(int(val)))
    parts = [
        SENTINEL + "（不发射不提交；" + LAYER_LABEL + "） \"\"\"",
        B1.CAPTURE_SRC,
        "if not callable(_EXPX_HOST):\n    raise RuntimeError('宿主捕获失败')",
        layer_src.strip(),
        B1._entry_src().rstrip(),
        "",
    ]
    return B1.SEPARATOR.join(parts)


def main():
    t0 = time.time()
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != B1.BASE_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")

    src2, ledger = B1.substitute(base_src)
    full = src2 + B1.SEPARATOR + build_block_v2() + "\n"
    compile(full, "expx_v2_main.py", "exec")

    ns: dict = {}
    exec(compile(full, "expx_v2_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    entry = entries[-1]
    if getattr(entry, "__name__", "") != ENTRY_NAME:
        raise RuntimeError("校验④红: 末 callable=%r"
                           % getattr(entry, "__name__", None))
    host = ns.get("_EXPX_HOST")
    if getattr(host, "__name__", "") != HOST_NAME:
        raise RuntimeError("校验④红: _EXPX_HOST=%r"
                           % getattr(host, "__name__", None))
    if (int(ns.get("_EXPX_K", 0)) != HORIZON_K
            or int(ns.get("_EXPX_WIN_END", 0)) != WIN_END
            or int(ns.get("_EXPX_TERM", 0)) != TERM):
        raise RuntimeError("校验⑦红: 守卫参数漂移")
    for fn in ("_expx_pnext", "_expx_take", "_expx_update", "_expx_note_own",
               "_expx_reset"):
        if not callable(ns.get(fn)):
            raise RuntimeError("校验④红: 缺 %s" % fn)

    OUT = OUT_DIR / "expx_v2"
    OUT.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    main_path = OUT / "main.py"
    main_path.write_text(full, encoding="utf-8")
    main_sha = hashlib.sha256(main_path.read_bytes()).hexdigest()

    tar_buf = io.BytesIO()
    with tarfile.open(fileobj=tar_buf, mode="w:gz") as tar:
        tar.add(str(main_path), arcname="main.py")
    tar_bytes = tar_buf.getvalue()
    (OUT / "submission.tar.gz").write_bytes(tar_bytes)

    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "form": "expx_v2",
        "base_main": str(BASE_MAIN), "base_sha256": base_sha,
        "main_sha256": main_sha,
        "main_bytes": main_path.stat().st_size,
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
        "subs": ledger, "subs_roundtrip_identity_ok": True,
        "gate_literal_untouched": True,
        "horizon_k": HORIZON_K, "win_end": WIN_END, "term": TERM,
        "guard": ["①窗收缩 step144-648 生效（648 后全基线语义）",
                  "②滞留保险 MR 持有时模型窗内峰值容量清不掉该件→基线出货"],
        "items": ["MILK", "STRAWBERRY", "WOOL"],
        "layer_label": LAYER_LABEL,
        "entry": ENTRY_NAME, "entry_last_callable": True,
        "host_entry": HOST_NAME, "compile_ok": True,
        "replacements": {
            "p_pred_sites": 4, "take_long_sites": 1, "take_cap10_sites": 3,
            "replacement_point": "MODELPX 的 p_next 计算（内层改造）"},
    }
    (OUT / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("BUILD V2 OK", main_sha[:16], "bytes", manifest["main_bytes"],
          round(time.time() - t0, 1), "s")
    return manifest


if __name__ == "__main__":
    main()
