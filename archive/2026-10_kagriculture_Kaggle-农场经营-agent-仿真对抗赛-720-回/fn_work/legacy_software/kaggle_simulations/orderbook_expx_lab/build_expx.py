# -*- coding: utf-8 -*-
"""build_expx：MODELPX 预测核精确化变体构建线（引擎公式最优执行；判决先行·
不发射不提交）。

构建底=orderbook_oppcond_lab/build/oc_c3/main.py（sha 3f8b57fd…）**零改动读入**，
内层改造=MODELPX 的 p_next 计算 4 处同文精确替换（启发式一步预报→K=12 拍
引擎公式轨迹峰值投影；量帽表达式→边际收益定单量，帽沿基线）+ 尾块注入模型
核心（沿 build_knee append 先例）：块首捕获宿主末 callable（_EXPX_HOST=oc_c3
件 _hs_agent），块尾末函数=_expx_agent（官方 last-callable 入口）。

变体（单形态）：
- expx：MILK/STRAWBERRY/WOOL 精确价格投影（price(inv) 形状函数全表+城镇排水
  表+R28 删失口径对手流估计）→ 轨迹局部峰值拍出货 + 边际收益=0 定单量
  （吸收曲线算自家出货边际冲击；预卖帽沿基线 3/6/10/10 档）。

校验（fail-closed 不产出）：①替换计数恰 4/1/3 ②反替换回程逐字节=基座源
（内层手术封印）③注入后 compile ④exec 装载后末 callable=_expx_agent 且
_EXPX_HOST=oc_c3 件 _hs_agent ⑤基座 sha 恒等 ⑥替换只落在 MODELPX 内核
（gate 字面量 4 处不动=门语义沿用）。
另产 submission.tar.gz + build_manifest（含替换台账）。只写
orderbook_expx_lab/。
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
SCHEMA = "orderbook_expx_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d3"
                     "9ba9bd23d")
SENTINEL = '"""expx MODELPX 预测核精确化实验尾块'
ENTRY_NAME = "_expx_agent"
HOST_NAME = "_hs_agent"
CAPTURE_SRC = ("_EXPX_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"
LAYER_FILE = "expx_layer.py"
K_TOKEN = "__EXPX_K__"
HORIZON_K = 12

# ---- 内层替换台账（3 组字面量；反替换回程=基座源） ----
PRED_OLD = ("inv_next=inv+rival_avg+planned-_s758_draw_units(item,step);"
            "p_next=float(_r37_market_price(item,max(0,int(inv_next))))")
PRED_NEW = ("p_next=_expx_pnext(item,step,inv,rival_avg,avail,p_now,planned,"
            "observation)")
GATE_LIT = "if p_next<p_cur-0.5:"          # 门字面量不动（语义沿用）
TAKE_LONG_OLD = ("take=min(avail,(10 if p_now>=100 else (10 if (step%24) in "
                 "(10,11,12,13) and p_now>=30 else (planned if (step%24) in "
                 "(10,11,12,13) and p_now>=10 else max(1,planned//2)))))")
TAKE10_OLD = "take=min(avail,10)"


def _take_new(old):
    """量帽替换文由基座字面量程序化导出（保表达式逐字节同）。"""
    prefix = "take=min(avail,"
    assert old.startswith(prefix) and old.endswith(")")
    cap_expr = old[len(prefix):-1]
    return ("take=min(avail,_expx_take(item,step,inv,p_now,%s,avail,"
            "observation))" % cap_expr)


SUBS = (
    (PRED_OLD, PRED_NEW, 4),
    (TAKE_LONG_OLD, _take_new(TAKE_LONG_OLD), 1),
    (TAKE10_OLD, _take_new(TAKE10_OLD), 3),
)

LAYER_LABEL = ("件 EXPX=MODELPX 预测核精确化（p_next 计算 4 处同文替换：K=12 "
               "拍引擎公式轨迹峰值投影（price(inv) 形状函数+城镇排水表+R28 "
               "删失口径对手流估计）；峰值拍出货门沿基座 p_next<p_cur-0.5；"
               "边际收益=0 定单量（吸收曲线算自家出货边际冲击）预卖帽沿基线 "
               "3/6/10/10；异常回退基线语义；零跨拍挪量、磁带 blob 零触碰）")


def _entry_src():
    """入口生成：宿主动作→逐拍估计滚动/自家可见量入账（不改动作）；
    step==0 复位台账。"""
    return (
        "def %s(observation, configuration=None):\n"
        "    \"\"\"expx 精确模型入口（官方 last-callable）：估计滚动→宿主→"
        "自家 SELL 可见量入账；动作零改动。\"\"\"\n"
        "    try:\n"
        "        _step_x = int((observation or {}).get('step', 0))\n"
        "        if _step_x == 0:\n"
        "            _expx_reset()\n"
        "        _expx_update(observation, _step_x)\n"
        "    except Exception:\n"
        "        _EXPX_REPORT['errors'] += 1\n"
        "    action = _EXPX_HOST(observation, configuration)\n"
        "    try:\n"
        "        _expx_note_own(observation, action)\n"
        "    except Exception:\n"
        "        _EXPX_REPORT['errors'] += 1\n"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_EXPX_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _EXPX_ENTRY_TMP\n"
        "del _EXPX_ENTRY_TMP\n" % (ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
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


def build_block():
    """实验尾块组装（模型核心 + 入口）。"""
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    if K_TOKEN not in layer_src:
        raise RuntimeError("expx_layer 缺占位 %s" % K_TOKEN)
    layer_src = layer_src.replace(K_TOKEN, str(int(HORIZON_K)))
    parts = [
        SENTINEL + "（不发射不提交；" + LAYER_LABEL + "） \"\"\"",
        CAPTURE_SRC,
        "if not callable(_EXPX_HOST):\n    raise RuntimeError('宿主捕获失败')",
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
    block = build_block()
    full = src2 + SEPARATOR + block + "\n"

    # 校验③ compile
    compile(full, "expx_main.py", "exec")

    # 校验④ exec 装载：末 callable=_expx_agent，_EXPX_HOST=oc_c3 件 _hs_agent
    ns: dict = {}
    exec(compile(full, "expx_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    if not entries:
        raise RuntimeError("校验④红: 装载后无 callable")
    entry = entries[-1]
    if getattr(entry, "__name__", "") != ENTRY_NAME:
        raise RuntimeError("校验④红: 末 callable=%r 应为 %s"
                           % (getattr(entry, "__name__", None), ENTRY_NAME))
    host = ns.get("_EXPX_HOST")
    if getattr(host, "__name__", "") != HOST_NAME:
        raise RuntimeError("校验④红: _EXPX_HOST=%r 应为 %s"
                           % (getattr(host, "__name__", None), HOST_NAME))
    if int(ns.get("_EXPX_K", 0)) != HORIZON_K:
        raise RuntimeError("校验④红: _EXPX_K 漂移")
    for fn in ("_expx_pnext", "_expx_take", "_expx_update", "_expx_note_own",
               "_expx_reset"):
        if not callable(ns.get(fn)):
            raise RuntimeError("校验④红: 缺 %s" % fn)

    OUT = OUT_DIR / "expx"
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
        "form": "expx",
        "base_main": str(BASE_MAIN),
        "base_sha256": base_sha,
        "main_sha256": main_sha,
        "main_bytes": main_path.stat().st_size,
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes),
        "tar_members": ["main.py"],
        "subs": ledger,
        "subs_roundtrip_identity_ok": True,
        "gate_literal_untouched": True,
        "horizon_k": HORIZON_K,
        "items": ["MILK", "STRAWBERRY", "WOOL"],
        "layer_label": LAYER_LABEL,
        "entry": ENTRY_NAME,
        "entry_last_callable": True,
        "host_entry": HOST_NAME,
        "compile_ok": True,
        "replacements": {
            "p_pred_sites": 4, "take_long_sites": 1, "take_cap10_sites": 3,
            "replacement_point": "MODELPX 的 p_next 计算（内层改造）",
        },
    }
    (OUT / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("BUILD OK", main_sha[:16], "bytes", manifest["main_bytes"],
          round(time.time() - t0, 1), "s")
    return manifest


if __name__ == "__main__":
    main()
