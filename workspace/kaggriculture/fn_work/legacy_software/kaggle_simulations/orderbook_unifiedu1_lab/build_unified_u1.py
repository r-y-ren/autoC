# -*- coding: utf-8 -*-
"""build_unified_u1：U1 统一求解核构建线（全替换形态；判决先行·不发射不提交）。

构建底=orderbook_oppcond_lab/build/oc_c3/main.py（sha 3f8b57fd…）零改动读入，
内层手术=MODELPX **整个决策规则**替换为单一求解核（3 组字面量 8 站点，计数
台账+反替换回程逐字节=基座源封印）：
  ①p_next 计算 4 处同文 → _u1_pnext(...)（何时卖：窗内剩余可卖拍投影峰值/
    末拍清剩余；mpx 窗语义内化为约束集）；
  ②量帽长表达式 1 处 + take=min(avail,10) 3 处 → _u1_take(...)（卖多少：
    min(帽 3/6/10, MR≤0 截止量)；站点原量帽表达式作影子基线口径逐字传入）。
门字面量 if p_next<p_cur-0.5: 4 处不动（阈 0.5=封印旋钮）。尾块注入统一求解
核（u1_layer；knee/expx append 先例）：块首捕获宿主末 callable（_U1_HOST=
oc_c3 件 _hs_agent），块尾末函数=_u1_agent（官方 last-callable 入口）。

校验（fail-closed 不产出）：①替换计数 4/1/3 ②反替换回程逐字节=基座源
③注入后 compile ④exec 装载后末 callable=_u1_agent 且 _U1_HOST=_hs_agent、
守卫参数 K=12/WIN_END=648/TERM=718/H0=14 ⑤基座 sha 恒等 ⑥门字面量 4 处不动
⑦窗/帽探针（_u1_sellable/_u1_cap 边界断言）。另产 submission.tar.gz +
build_manifest。只写 orderbook_unifiedu1_lab/。
"""
from __future__ import annotations

import hashlib
import io
import json
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
BASE_MAIN = (KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
             / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_unifiedu1_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d3"
                     "9ba9bd23d")
SENTINEL = '"""u1 统一求解核（何时卖+卖多少 单一决策核）实验尾块'
ENTRY_NAME = "_u1_agent"
HOST_NAME = "_hs_agent"
CAPTURE_SRC = ("_U1_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"
LAYER_FILE = "u1_layer.py"
K_TOKEN = "__U1_K__"
WIN_END_TOKEN = "__U1_WIN_END__"
TERM_TOKEN = "__U1_TERM__"
H0_TOKEN = "__U1_H0__"
HORIZON_K = 12
WIN_END = 648
TERM = 718
H0 = 14

# ---- 内层替换台账（3 组字面量 8 站点；反替换回程=基座源） ----
PRED_OLD = ("inv_next=inv+rival_avg+planned-_s758_draw_units(item,step);"
            "p_next=float(_r37_market_price(item,max(0,int(inv_next))))")
PRED_NEW = ("p_next=_u1_pnext(item,step,inv,rival_avg,avail,p_now,planned,"
            "observation)")
GATE_LIT = "if p_next<p_cur-0.5:"          # 门字面量不动（阈 0.5 封印）
TAKE_LONG_OLD = ("take=min(avail,(10 if p_now>=100 else (10 if (step%24) in "
                 "(10,11,12,13) and p_now>=30 else (planned if (step%24) in "
                 "(10,11,12,13) and p_now>=10 else max(1,planned//2)))))")
TAKE10_OLD = "take=min(avail,10)"


def _take_new(old):
    """量帽替换文由基座字面量程序化导出（站点原量帽=影子基线口径逐字传入）。"""
    prefix = "take=min(avail,"
    assert old.startswith(prefix) and old.endswith(")")
    cap_expr = old[len(prefix):-1]
    return ("take=min(avail,_u1_take(item,step,inv,p_now,%s,avail,"
            "observation))" % cap_expr)


SUBS = (
    (PRED_OLD, PRED_NEW, 4),
    (TAKE_LONG_OLD, _take_new(TAKE_LONG_OLD), 1),
    (TAKE10_OLD, _take_new(TAKE10_OLD), 3),
)

LAYER_LABEL = ("件 U1=统一求解核（全替换形态）：MODELPX 整个决策规则（p_next "
               "4 站点+量帽 4 站点）替换为单一决策核同时做何时卖+卖多少——K=12 "
               "拍引擎公式投影（price(inv) 全表+城镇排水表+R28 删失口径对手流）"
               "；窗约束=mpx 语义内化（可卖拍 step∈[144,648)∧hour∈14..22，胜者"
               "件字面量语义）；现在卖 iff 当前报价≥窗内剩余可卖拍投影峰值价或"
               "窗将关闭（末拍清剩余）；量=min(帽 3/6/10, MR≤0 截止量)；胜位守卫"
               "沿 expx_v2（648 后回基线+滞留保险）；非触发拍零足迹、异常回退基线"
               "语义、零跨拍挪量、磁带 blob 零触碰）")


def _entry_src():
    """入口生成：估计滚动→宿主→自家 SELL 可见量入账（动作零改动）。"""
    return (
        "def %s(observation, configuration=None):\n"
        "    \"\"\"u1 统一求解核入口（官方 last-callable）：估计滚动→宿主→"
        "自家 SELL 可见量入账；动作零改动。\"\"\"\n"
        "    try:\n"
        "        _step_u = int((observation or {}).get('step', 0))\n"
        "        if _step_u == 0:\n"
        "            _u1_reset()\n"
        "        _u1_update(observation, _step_u)\n"
        "    except Exception:\n"
        "        _U1_REPORT['errors'] += 1\n"
        "    action = _U1_HOST(observation, configuration)\n"
        "    try:\n"
        "        _u1_note_own(observation, action)\n"
        "    except Exception:\n"
        "        _U1_REPORT['errors'] += 1\n"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_U1_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _U1_ENTRY_TMP\n"
        "del _U1_ENTRY_TMP\n" % (ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                 ENTRY_NAME, ENTRY_NAME))


def substitute(base_src):
    """内层替换（计数 fail-closed）→ (替换后源, 台账)。"""
    src = base_src
    ledger = []
    if src.count(GATE_LIT) != 4:
        raise RuntimeError("校验⑥红: 门字面量计数 %d 应为 4"
                           % src.count(GATE_LIT))
    for old, new, expect in SUBS:
        n = src.count(old)
        if n != expect:
            raise RuntimeError("校验①红: 字面量计数 %d 应为 %d: %r"
                               % (n, expect, old[:60]))
        src = src.replace(old, new)
        ledger.append({"old": old, "new": new, "count": n})
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


def build_block():
    """实验尾块组装（统一求解核 + 入口）。"""
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    for tok, val in ((K_TOKEN, HORIZON_K), (WIN_END_TOKEN, WIN_END),
                     (TERM_TOKEN, TERM), (H0_TOKEN, H0)):
        if tok not in layer_src:
            raise RuntimeError("u1_layer 缺占位 %s" % tok)
        layer_src = layer_src.replace(tok, str(int(val)))
    parts = [
        SENTINEL + "（不发射不提交；" + LAYER_LABEL + "） \"\"\"",
        CAPTURE_SRC,
        "if not callable(_U1_HOST):\n    raise RuntimeError('宿主捕获失败')",
        layer_src.strip(),
        _entry_src().rstrip(),
        "",
    ]
    return SEPARATOR.join(parts)


def main():
    t0 = time.time()
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")

    src2, ledger = substitute(base_src)
    full = src2 + SEPARATOR + build_block() + "\n"
    compile(full, "u1_main.py", "exec")

    ns: dict = {}
    exec(compile(full, "u1_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    entry = entries[-1]
    if getattr(entry, "__name__", "") != ENTRY_NAME:
        raise RuntimeError("校验④红: 末 callable=%r"
                           % getattr(entry, "__name__", None))
    host = ns.get("_U1_HOST")
    if getattr(host, "__name__", "") != HOST_NAME:
        raise RuntimeError("校验④红: _U1_HOST=%r"
                           % getattr(host, "__name__", None))
    if (int(ns.get("_U1_K", 0)) != HORIZON_K
            or int(ns.get("_U1_WIN_END", 0)) != WIN_END
            or int(ns.get("_U1_TERM", 0)) != TERM
            or int(ns.get("_U1_H0", 0)) != H0):
        raise RuntimeError("校验④红: 守卫参数漂移")
    for fn in ("_u1_pnext", "_u1_take", "_u1_update", "_u1_note_own",
               "_u1_reset", "_u1_sellable", "_u1_cap"):
        if not callable(ns.get(fn)):
            raise RuntimeError("校验④红: 缺 %s" % fn)

    # 校验⑦ 窗/帽探针（mpx 胜者件字面量语义边界）
    sellable = ns["_u1_sellable"]
    assert sellable(158) is True          # step 158 = hour 14（窗内）
    assert sellable(157) is False         # hour 13（窗外）
    assert sellable(143) is False         # <144
    assert sellable(646) is True          # hour 22，648 前末日窗
    assert sellable(647) is False         # hour 23
    assert sellable(648) is False         # ≥648 胜位守卫①
    cap = ns["_u1_cap"]
    assert cap(5, 24 * 4 + 2) == 3
    assert cap(10, 24 * 4 + 10) == 6
    assert cap(30, 24 * 4 + 10) == 10
    assert cap(100, 24 * 4 + 2) == 10

    OUT = OUT_DIR / "u1"
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
        "form": "u1",
        "base_main": str(BASE_MAIN), "base_sha256": base_sha,
        "main_sha256": main_sha,
        "main_bytes": main_path.stat().st_size,
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
        "subs": ledger, "subs_roundtrip_identity_ok": True,
        "gate_literal_untouched": True,
        "horizon_k": HORIZON_K, "win_end": WIN_END, "term": TERM, "h0": H0,
        "kernel": "统一求解核（何时卖+卖多少 单一决策核；非 mpx/expx 双层叠加）",
        "window": "可卖拍=step∈[144,648) ∧ (step%24)∈{14..22}（mpx 胜者件字面"
                  "量语义内化为约束集）",
        "sizing": "min(帽 3/6/10, MR≤0 截止量)；末拍清剩余（MR 放行至帽位）",
        "guard": ["①窗收缩 648 后回基线（fire_x=fire_base+基线量帽）",
                  "②滞留保险 MR 持有时窗内峰值容量清不掉投射仓存量→基线出货"],
        "items": ["MILK", "STRAWBERRY", "WOOL"],
        "layer_label": LAYER_LABEL,
        "entry": ENTRY_NAME, "entry_last_callable": True,
        "host_entry": HOST_NAME, "compile_ok": True,
        "probes": {"window_edges_ok": True, "cap_tiers_ok": True},
        "replacements": {
            "p_pred_sites": 4, "take_sites": 4,
            "replacement_point": "MODELPX 整个决策规则（内层全替换）"},
    }
    (OUT / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("BUILD U1 OK", main_sha[:16], "bytes", manifest["main_bytes"],
          round(time.time() - t0, 1), "s")
    return manifest


if __name__ == "__main__":
    main()
