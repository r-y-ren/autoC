# -*- coding: utf-8 -*-
"""build_sx：合装件构建线（mpx 胜者件 + expx_v2 层；判决先行·不发射不提交）。

合装 sx = mpx 胜者件（mpx_w24_p2_3_h14，=oc_c3+MODELPX 窗聚焦 h14-22）叠
expx_v2 层（引擎模型化领卖 p_next 精确化 + 边际收益定单量 + 胜位守卫[窗收缩
step144-648 + 滞留保险]）。尾块注入沿 append 先例（expx 尾块追加于 mpx 尾块
之后）。

构建底=orderbook_oppcond_lab/build/oc_c3/main.py（sha 3f8b57fd…）零改动读入。
合装替换（fail-closed 计数 + 反替换回程逐字节=基座源封印）：
- expx 预测核（作用面 A）：p_next 计算 4 处同文 → _expx_pnext（与 mpx 窗字面
  量作用面正交）；
- expx 量帽 3 处（take=min(avail,10)）→ _expx_take(...,10,...)（mpx 不触碰）；
- **共享面 take_long 1 处**（expx 与 mpx 同指基座 take_long 字面量）：组合
  _expx_take(_mx_cap(...))——expx 边际定单量/滞留保险套 mpx 量帽 (3,6,10)，
  语义组合非冲突（expx 定单量以 mpx 帽为上限）；
- mpx 参数面（作用面 B）：planned=6×4 / 滑窗 hist×3 + h×1 / 品项集×1 / 时段×1。
尾块：mpx 参数头（_mx_cap/_MX_*）置 __future__ 后 + mpx 透传入口 _mx_agent +
expx 尾块（expx_layer_v2 + 入口 _expx_agent）。入口链 _expx_agent→_mx_agent→
_hs_agent（oc_c3）。

校验（fail-closed 不产出）：①替换计数 ②反替换回程=基座源 ③注入后 compile
④exec 末 callable=_expx_agent 且 _EXPX_HOST=_mx_agent（链式宿主）⑤基座 sha
恒等 ⑥门字面量 4 处不动 ⑦mpx/expx 参数与形态一致 ⑧diff 审计（作用面 A∩B=
共享 take_long 1 处已组合；命名零冲突 _MX_* vs _EXPX_*）。
只写 orderbook_sx_lab/。
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
for _p in (str(KSIM_DIR / "orderbook_modelpx_lab"),
           str(KSIM_DIR / "orderbook_expx_lab")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import build_modelpx as BMP  # noqa: E402  （mpx 参数头/入口/参数级字面量）
import build_expx as B1      # noqa: E402  （expx 预测核字面量/尾块机件）

BASE_MAIN = B1.BASE_MAIN
BASE_SHA_EXPECTED = B1.BASE_SHA_EXPECTED
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_sx_lab_manifest/1.0"

SENTINEL = '"""sx 合装件（mpx 胜者件+expx_v2 层）实验尾块'
ENTRY_NAME = "_expx_agent"
MPX_ENTRY = "_mx_agent"
HOST_NAME = "_mx_agent"          # expx 宿主=mpx 入口（链式）
LAYER_FILE_V2 = "expx_layer_v2.py"
EXPX_LAB = KSIM_DIR / "orderbook_expx_lab"
K_TOKEN, WIN_END_TOKEN, TERM_TOKEN = "__EXPX_K__", "__EXPX_WIN_END__", "__EXPX_TERM__"
HORIZON_K, WIN_END, TERM = 12, 648, 718

# ---- mpx 胜者件参数（mpx_w24_p2_3_h14；levels=(2,1,0,2)） ----
MX_WIN, MX_PLANNED, MX_ITEMS, MX_H0 = 24, 2, ("MILK", "STRAWBERRY", "WOOL"), 14

# ---- 共享面 take_long 组合文（expx 定单量套 mpx 量帽） ----
TAKE_LONG_SX_NEW = ("take=min(avail,_expx_take(item,step,inv,p_now,"
                    "_mx_cap(item,p_now,step,planned),avail,observation))")

LAYER_LABEL = ("件 SX=mpx 胜者件（mpx_w24_p2_3_h14）+expX_V2 层（MODELPX 预测"
               "核 p_next 精确化+边际收益定单量+胜位守卫[窗收缩 step144-648+滞留"
               "保险]）；take_long 共享面组合 _expx_take(_mx_cap)；零跨拍挪量、磁带"
               " blob 零触碰、异常回退基线语义）")

# ---- 合装替换台账（8 组；应用序，反替换回程=基座源） ----
SUBS = (
    # A. expx 预测核（作用面 A，与 mpx 窗字面量正交）
    (B1.PRED_OLD, B1.PRED_NEW, 4),
    # 共享面 take_long（expx∩mpx 同指基座字面量）→ 组合 _expx_take(_mx_cap)
    (B1.TAKE_LONG_OLD, TAKE_LONG_SX_NEW, 1),
    # A. expx 量帽 3 处（mpx 不触碰）
    (B1.TAKE10_OLD, B1._take_new(B1.TAKE10_OLD), 3),
    # B. mpx 参数面（作用面 B）
    BMP.SUBS[1],   # planned=6 → _MX_PLANNED  ×4
    BMP.SUBS[2],   # 滑窗 hist  ×3
    BMP.SUBS[3],   # 滑窗 h     ×1
    BMP.SUBS[4],   # 品项集     ×1
    BMP.SUBS[5],   # 时段       ×1
)
GATE_LIT = B1.GATE_LIT            # "if p_next<p_cur-0.5:" 门字面量不动


def _expx_tail_block():
    """expx_v2 尾块（沿 append 先例）：sentinel + 宿主捕获 + 模型核心 + 入口。"""
    layer_src = (EXPX_LAB / LAYER_FILE_V2).read_text(encoding="utf-8")
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


def substitute(base_src):
    """合装替换（计数 fail-closed）→ (替换后源, 台账)。"""
    src = base_src
    ledger = []
    if src.count(GATE_LIT) != 4:
        raise RuntimeError("校验⑥红: 门字面量计数 %d 应为 4" % src.count(GATE_LIT))
    for old, new, expect in SUBS:
        n = src.count(old)
        if n != expect:
            raise RuntimeError("校验①红: 字面量计数 %d 应为 %d: %r"
                               % (n, expect, old[:60]))
        src = src.replace(old, new)
        ledger.append({"old": old, "new": new, "count": n})
    # 反替换回程=基座源（内层手术封印）
    back = src
    for old, new, cnt in reversed(SUBS):
        if back.count(new) != cnt:
            raise RuntimeError("校验②红: 反替换计数漂移: %r" % new[:60])
        back = back.replace(new, old)
    if back != base_src:
        raise RuntimeError("校验②红: 反替换回程 != 基座源")
    if src.count(GATE_LIT) != 4:
        raise RuntimeError("校验⑥红: 替换后门字面量漂移")
    return src, ledger


def diff_audit():
    """作用面正交性审计：A(expx 预测核/量帽/守卫) vs B(mpx 窗字面量/参数)。"""
    A_subs = [B1.PRED_OLD, B1.TAKE_LONG_OLD, B1.TAKE10_OLD]
    B_subs = [s[0] for s in BMP.SUBS]           # mpx 6 组基座字面量
    shared = [x for x in A_subs if x in B_subs]
    # 命名空间审计：_MX_* vs _EXPX_* 零冲突
    mpx_names = {"_MX_WIN", "_MX_PLANNED", "_MX_ITEMS", "_MX_H0", "_MX_CAPS",
                 "_MX_REPORT", "_mx_cap", "_MX_HOST", "_mx_agent"}
    expx_names = {"_EXPX_ITEMS", "_EXPX_K", "_EXPX_WIN_END", "_EXPX_TERM",
                  "_EXPX_MAX_BATCH", "_EXPX_SHOPS", "_EXPX_STATE", "_EXPX_DEC",
                  "_EXPX_REPORT", "_expx_reset", "_expx_diff", "_expx_price",
                  "_expx_params", "_expx_draw", "_expx_rival", "_expx_update",
                  "_expx_note_own", "_expx_traj", "_expx_pnext", "_expx_take",
                  "_EXPX_HOST", "_expx_agent"}
    name_overlap = sorted(mpx_names & expx_names)
    return {
        "surface_A_expx": {
            "prediction_core": "p_next 计算 4 处（B1.PRED_OLD→_expx_pnext）",
            "sizing": "take=min(avail,10) 3 处→_expx_take(...,10,...)",
            "guard": "胜位守卫：窗收缩 step144-648（648 后 fire_x=fire_base）"
                     "+ 滞留保险（MR 持有时模型窗内峰值容量清不掉→基线出货）",
        },
        "surface_B_mpx": {
            "window_literal": "滑窗 len(hist[i])>12:del[:6] ×3 + len(h[i])>12 "
                              "×1 → _MX_WIN/_MX_WIN//2",
            "params": "planned=6×4 / 品项集×1 / 时段×1（_MX_PLANNED/_MX_ITEMS/"
                      "_MX_H0）",
            "cap": "take_long 量帽 → _mx_cap(item,p_now,step,planned) 钉死 "
                   "(3,6,10)",
        },
        "shared_sites": {
            "count": len(shared),
            "literals": [s[:70] for s in shared],
            "reconciliation": "take_long 1 处（expx 与 mpx 同指基座字面量 "
                              "B1.TAKE_LONG_OLD==BMP.SUBS[0][0]）→ 组合 "
                              "take=min(avail,_expx_take(...,_mx_cap(...),...))"
                              "：expx 边际定单量/滞留保险以 mpx 量帽 (3,6,10) 为"
                              "上限（语义组合非冲突，expx 不推翻 mpx 帽）",
        },
        "orthogonal_prediction_vs_window": True,   # A 预测核 ∩ B 窗字面量 = ∅
        "name_overlap": name_overlap,
        "zero_name_conflict": not name_overlap,
        "conflict_verdict": "ZERO_CONFLICT（预测核/窗字面量严格正交；唯一共享面 "
                            "take_long 组合 _expx_take(_mx_cap) 语义无矛盾；"
                            "_MX_* 与 _EXPX_* 命名零碰撞）",
    }


def build():
    t0 = time.time()
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")

    sub_src, ledger = substitute(base_src)

    # mpx 参数头（_mx_cap/_MX_*）+ 入口（_mx_agent 透传）
    layer = (BMP.LAYER_TMPL
             .replace("__MX_WIN__", repr(int(MX_WIN)))
             .replace("__MX_PLANNED__", repr(int(MX_PLANNED)))
             .replace("__MX_ITEMS__", repr(MX_ITEMS))
             .replace("__MX_H0__", repr(int(MX_H0))))
    header = (BMP.SENTINEL + "（MODELPX 预测器内部参数网格 grid-search；合装 sx）\n"
              "# 构建底=orderbook_oppcond_lab/build/oc_c3/main.py 零改动读入；\n"
              "# 合装=mpx 胜者件参数面 + expx_v2 层（预测核/定单量/胜位守卫）。\n")
    anchor = "from __future__ import annotations\n"
    idx = sub_src.find(anchor)
    if idx < 0 or sub_src.count(anchor) != 1:
        raise RuntimeError("校验③红: __future__ 锚点非恰 1")
    cut = idx + len(anchor)
    mpx_entry = BMP._entry_src()
    expx_tail = _expx_tail_block()
    full = (header + sub_src[:cut] + "\n" + layer.strip("\n") + "\n"
            + B1.SEPARATOR + sub_src[cut:] + B1.SEPARATOR + mpx_entry
            + B1.SEPARATOR + expx_tail + "\n")

    # 校验③ compile
    compile(full, "sx_main.py", "exec")

    # 校验④ exec 装载：末 callable=_expx_agent，_EXPX_HOST=_mx_agent（链式）
    ns = {}
    exec(compile(full, "sx_main.py", "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        raise RuntimeError("校验④红: 末 callable=%r 应为 %s"
                           % (loaded[-1].__name__ if loaded else None, ENTRY_NAME))
    host = ns.get("_EXPX_HOST")
    if getattr(host, "__name__", "") != HOST_NAME:
        raise RuntimeError("校验④红: _EXPX_HOST=%r 应为 %s"
                           % (getattr(host, "__name__", None), HOST_NAME))
    # 链式宿主：_mx_agent 的 _MX_HOST=oc_c3 _hs_agent
    if getattr(ns.get("_MX_HOST"), "__name__", "") != "_hs_agent":
        raise RuntimeError("校验④红: _MX_HOST 链断（应=_hs_agent）")
    # 校验⑦ 参数一致
    if (int(ns.get("_MX_WIN")) != MX_WIN or int(ns.get("_MX_PLANNED")) != MX_PLANNED
            or tuple(ns.get("_MX_ITEMS")) != MX_ITEMS or int(ns.get("_MX_H0")) != MX_H0):
        raise RuntimeError("校验⑦红: mpx 参数漂移")
    if (int(ns.get("_EXPX_K")) != HORIZON_K or int(ns.get("_EXPX_WIN_END")) != WIN_END
            or int(ns.get("_EXPX_TERM")) != TERM):
        raise RuntimeError("校验⑦红: expx 守卫参数漂移")
    for fn in ("_expx_pnext", "_expx_take", "_expx_update", "_expx_note_own",
               "_expx_reset", "_mx_cap"):
        if not callable(ns.get(fn)):
            raise RuntimeError("校验④红: 缺 %s" % fn)
    # _mx_cap 量帽 (3,6,10) 形态
    _mx_cap = ns["_mx_cap"]
    assert _mx_cap("MILK", 5, 24 * 4 + 2, 2) == 3
    assert _mx_cap("MILK", 10, 24 * 4 + 10, 2) == 6
    assert _mx_cap("MILK", 30, 24 * 4 + 10, 2) == 10

    da = diff_audit()
    if not da["zero_name_conflict"]:
        raise RuntimeError("校验⑧红: 命名冲突 %r" % da["name_overlap"])
    if da["shared_sites"]["count"] != 1:
        raise RuntimeError("校验⑧红: 共享面数漂移 %d 应为 1"
                           % da["shared_sites"]["count"])

    OUT = OUT_DIR / "sx"
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
        "schema": SCHEMA, "form": "sx",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "composite": "mpx_w24_p2_3_h14 + expx_v2 层",
        "base_main": str(BASE_MAIN), "base_sha256": base_sha,
        "main_sha256": main_sha, "main_bytes": main_path.stat().st_size,
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
        "mpx_winner": {"form": "mpx_w24_p2_3_h14", "levels": [2, 1, 0, 2],
                       "main_sha256": "f0101de9b558d1f56334739f9a49a0a0d4bc860"
                                      "a898792a9b69fc72c3d84e44f"},
        "expx_layer": {"k": HORIZON_K, "win_end": WIN_END, "term": TERM,
                       "label": LAYER_LABEL},
        "params": {"win": MX_WIN, "planned": MX_PLANNED,
                   "items": list(MX_ITEMS), "h0": MX_H0},
        "subs": ledger, "subs_roundtrip_identity_ok": True,
        "gate_literal_untouched": True, "entry_last_callable": ENTRY_NAME,
        "host_entry": HOST_NAME, "chain": "expx_agent→mx_agent→hs_agent",
        "compile_ok": True,
        "diff_audit": da,
    }
    (OUT / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    (EVID_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("BUILD SX OK", main_sha[:16], "bytes", manifest["main_bytes"],
          "shared_sites", da["shared_sites"]["count"],
          round(time.time() - t0, 1), "s", flush=True)
    return manifest


if __name__ == "__main__":
    build()
