# -*- coding: utf-8 -*-
"""build_unified_v3：D4 统一求解完全体构建线（判决先行·不发射不提交）。

构建底=orderbook_oppcond_lab/build/oc_c3/main.py（sha 3f8b57fd…）零改动读入，
内层手术=MODELPX **整个决策规则**替换为单一求解核（3 组字面量 8 站点，计数
台账+反替换回程逐字节=基座源封印；与 u1 同一手术面）：
  ①p_next 计算 4 处同文 → _u3_pnext(...)（卖时+卖量联合决策；哨兵过基座门）；
  ②量帽长表达式 1 处 + take=min(avail,10) 3 处 → _u3_take(...)。
门字面量 if p_next<p_cur-0.5: 4 处不动（哨兵语义：卖=−1e18/持有=+1e18）。
尾块注入统一求解核（u3_layer；knee/expx/u1 append 先例）：块首捕获宿主末
callable（_U3_HOST=oc_c3 件 _hs_agent），块尾末函数=_u3_agent。

两形态同手术面对照（D5 推翻性发现并入）：
  v3k = peak（原设计）：柔窗 h14-22=1.0/h10-13,23=0.5/其余 0；预测连续跌
        >$0.5→半量、现价≥连续投影峰→全量（帽内）、MR≤0 截止、末拍清剩余；
  v3p = platform（D5 平台语义主形态）：小单持续放行不等峰（lot 沿帽 3/6/10
        小批）、跌幅>$0.5 半量保留、柔窗 d12-24 平台 [288,576)=1.0/其余 0.5、
        连续空间比较仅用于跌幅判定。
校验（fail-closed 不产出）：①替换计数 4/1/3 ②反替换回程逐字节=基座源
③注入后 compile ④exec 装载后末 callable=_u3_agent 且 _U3_HOST=_hs_agent、
守卫参数 K=12/WIN_END=648/TERM=718 ⑤基座 sha 恒等 ⑥门字面量 4 处不动
⑦窗/帽/半量门/守卫探针。另产 submission.tar.gz + build_manifest。
只写 orderbook_unifiedv3_lab/。
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
SCHEMA = "orderbook_unifiedv3_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d3"
                     "9ba9bd23d")
SENTINEL = '"""u3 unified_v3 单核（卖时+卖量+窗 联合优化）实验尾块'
ENTRY_NAME = "_u3_agent"
HOST_NAME = "_hs_agent"
CAPTURE_SRC = ("_U3_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"
LAYER_FILE = "u3_layer.py"
K_TOKEN = "__U3_K__"
WIN_END_TOKEN = "__U3_WIN_END__"
TERM_TOKEN = "__U3_TERM__"
FORM_TOKEN = "__U3_FORM__"
HORIZON_K = 12
WIN_END = 648
TERM = 718

FORMS = {
    "v3k": {
        "form": "peak",
        "desc": "peak 形态（原设计对照）：柔窗 h14-22=1.0/h10-13,23=0.5/其余 0；"
                "预测连续跌>$0.5→半量、现价≥连续投影峰→全量（帽内）、MR≤0 截止"
                "（平局破向卖出）、窗将关闭末拍清剩余、滞留保险",
    },
    "v3p": {
        "form": "platform",
        "desc": "platform 形态（D5 平台语义主形态）：小单持续放行不等峰（lot 沿帽"
                " 3/6/10 小批）、跌幅>$0.5 半量保留、柔窗 d12-24 平台 [288,576)"
                "=1.0/其余 0.5（产线节奏对齐）、连续空间比较仅用于跌幅判定",
    },
}

# ---- 内层替换台账（3 组字面量 8 站点；反替换回程=基座源） ----
PRED_OLD = ("inv_next=inv+rival_avg+planned-_s758_draw_units(item,step);"
            "p_next=float(_r37_market_price(item,max(0,int(inv_next))))")
PRED_NEW = ("p_next=_u3_pnext(item,step,inv,rival_avg,avail,p_now,planned,"
            "observation)")
GATE_LIT = "if p_next<p_cur-0.5:"          # 门字面量不动（哨兵语义）
TAKE_LONG_OLD = ("take=min(avail,(10 if p_now>=100 else (10 if (step%24) in "
                 "(10,11,12,13) and p_now>=30 else (planned if (step%24) in "
                 "(10,11,12,13) and p_now>=10 else max(1,planned//2)))))")
TAKE10_OLD = "take=min(avail,10)"


def _take_new(old):
    """量帽替换文由基座字面量程序化导出（站点原量帽=影子基线口径逐字传入）。"""
    prefix = "take=min(avail,"
    assert old.startswith(prefix) and old.endswith(")")
    cap_expr = old[len(prefix):-1]
    return ("take=min(avail,_u3_take(item,step,inv,p_now,%s,avail,"
            "observation))" % cap_expr)


SUBS = (
    (PRED_OLD, PRED_NEW, 4),
    (TAKE_LONG_OLD, _take_new(TAKE_LONG_OLD), 1),
    (TAKE10_OLD, _take_new(TAKE10_OLD), 3),
)

LAYER_LABEL = (
    "件 U3=unified_v3 单核：MODELPX 整个决策规则（p_next 4 站点+量帽 4 站点）"
    "替换为单一决策核同时做何时卖+卖多少+窗——K=12 拍引擎公式连续投影"
    "（price(inv) 全表+城镇排水表+R28 删失口径对手流）；柔窗（peak=小时权重"
    " h14-22 1.0/h10-13,23 0.5；platform=d12-24 平台 1.0/其余 0.5）；半量门"
    "（预测连续跌>$0.5→半量）+峰值全量/平台持续放行；MR≤0 截止；胜位守卫"
    "（648 后回基线+滞留保险）；非触发拍零足迹、异常回退基线语义、零跨拍挪量、"
    "磁带 blob 零触碰）")


def _entry_src():
    """入口生成：估计滚动→宿主→自家 SELL 可见量入账（动作零改动）。"""
    return (
        "def %s(observation, configuration=None):\n"
        "    \"\"\"u3 unified_v3 入口（官方 last-callable）：估计滚动→宿主→"
        "自家 SELL 可见量入账；动作零改动。\"\"\"\n"
        "    try:\n"
        "        _step_u = int((observation or {}).get('step', 0))\n"
        "        if _step_u == 0:\n"
        "            _u3_reset()\n"
        "        _u3_update(observation, _step_u)\n"
        "    except Exception:\n"
        "        _U3_REPORT['errors'] += 1\n"
        "    action = _U3_HOST(observation, configuration)\n"
        "    try:\n"
        "        _u3_note_own(observation, action)\n"
        "    except Exception:\n"
        "        _U3_REPORT['errors'] += 1\n"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_U3_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _U3_ENTRY_TMP\n"
        "del _U3_ENTRY_TMP\n" % (ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
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


def build_block(form):
    """实验尾块组装（统一求解核 + 入口）。"""
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    for tok, val in ((K_TOKEN, HORIZON_K), (WIN_END_TOKEN, WIN_END),
                     (TERM_TOKEN, TERM)):
        if tok not in layer_src:
            raise RuntimeError("u3_layer 缺占位 %s" % tok)
        layer_src = layer_src.replace(tok, str(int(val)))
    if FORM_TOKEN not in layer_src:
        raise RuntimeError("u3_layer 缺占位 %s" % FORM_TOKEN)
    layer_src = layer_src.replace(FORM_TOKEN, '"%s"' % form)
    parts = [
        SENTINEL + "（不发射不提交；" + LAYER_LABEL + "） \"\"\"",
        CAPTURE_SRC,
        "if not callable(_U3_HOST):\n    raise RuntimeError('宿主捕获失败')",
        layer_src.strip(),
        _entry_src().rstrip(),
        "",
    ]
    return SEPARATOR.join(parts)


def probe_ns(ns, form):
    """⑦窗/帽/半量门/守卫探针（合成观测；引擎公式同源）。"""
    w = ns["_u3_w"]
    cap = ns["_u3_cap"]
    shape = ns["_u3_shape"]
    pnext = ns["_u3_pnext"]
    take = ns["_u3_take"]
    assert cap(5, 24 * 4 + 2) == 3
    assert cap(10, 24 * 4 + 10) == 6
    assert cap(30, 24 * 4 + 10) == 10
    assert cap(100, 24 * 4 + 2) == 10
    if form == "peak":
        assert w(158) == 1.0            # step 158 = hour 14（主权重）
        assert w(157) == 0.5            # hour 13（邻近衰减）
        assert w(168) == 0.0            # hour 0（窗外抑制）
        assert w(647) == 0.5            # hour 23（邻近衰减）
    else:
        assert w(300) == 1.0            # d12.5 平台内
        assert w(200) == 0.5            # 平台外
        assert w(100) == 0.5            # 平台外（早盘仍 0.5=不等峰）
        assert w(647) == 0.5
    assert shape(10, 0.6) == (5, True)      # 跌>$0.5 → 半量
    assert shape(10, 0.4) == (10, False)    # 未触发 → 全量
    assert shape(1, 2.0) == (1, True)       # 半量下限 1
    obs = {"town": {"unlocked_shops": []},
           "market": {"prices": {}, "inventory": {}, "params": {}}}
    ns["_u3_reset"]()
    q = pnext("MILK", 700, 30000, 0.0, 10, 5, 6, obs)
    assert abs(q) < 1e17, "648 后应基线语义（p_next_base 回值，非哨兵）"
    assert ns["_U3_DEC"][(700, "MILK")]["mode"] == "post_win_base"
    assert take("MILK", 700, 30000, 5, 6, 10, obs) == 6, "648 后量帽=基线"
    if form == "peak":
        ns["_u3_reset"]()
        q = pnext("MILK", 168, 30000, 0.0, 10, 5, 6, obs)
        assert q > 1e17 and ns["_U3_DEC"][(168, "MILK")]["mode"] == \
            "window_suppressed", "peak 窗外（hour 0）应抑制"
    else:
        ns["_u3_reset"]()
        q = pnext("MILK", 168, 30000, 0.0, 10, 5, 6, obs)
        dec = ns["_U3_DEC"][(168, "MILK")]
        assert dec["fire_x"] is True and dec["mode"] == "platform", \
            "platform 应持续放行不等峰"
        assert 1 <= int(dec["q"]) <= 5, "platform 小单帽内（w=0.5→帽减半）"


def build_one(name, cfg, base_bytes):
    base_src = base_bytes.decode("utf-8")
    form = cfg["form"]
    sub_src, ledger = substitute(base_src)
    tail = build_block(form)
    injected = sub_src + SEPARATOR + tail + "\n"
    try:
        compile(injected, "<u3:%s>" % name, "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 %s: 语法不通过: %r" % (name, exc))
    ns = {}
    try:
        exec(compile(injected, "<u3:%s>" % name, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 %s: exec 失败: %r" % (name, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or getattr(loaded[-1], "__name__", "") != ENTRY_NAME:
        got = getattr(loaded[-1], "__name__", None) if loaded else None
        raise RuntimeError("校验④红 %s: 末 callable=%r" % (name, got))
    if ns.get("_U3_HOST") is not ns.get(HOST_NAME):
        raise RuntimeError("校验④红 %s: 块首捕获非 %s" % (name, HOST_NAME))
    if (int(ns.get("_U3_K", 0)) != HORIZON_K
            or int(ns.get("_U3_WIN_END", 0)) != WIN_END
            or int(ns.get("_U3_TERM", 0)) != TERM):
        raise RuntimeError("校验④红 %s: 守卫参数漂移" % name)
    if ns.get("_U3_FORM") != form:
        raise RuntimeError("校验④红 %s: 形态参数漂移 %r" % (name,
                                                        ns.get("_U3_FORM")))
    for fn in ("_u3_pnext", "_u3_take", "_u3_update", "_u3_note_own",
               "_u3_reset", "_u3_w", "_u3_cap", "_u3_shape", "_u3_mr_qty"):
        if not callable(ns.get(fn)):
            raise RuntimeError("校验④红 %s: 缺 %s" % (name, fn))
    probe_ns(ns, form)

    out = OUT_DIR / name
    out.mkdir(parents=True, exist_ok=True)
    main_path = out / "main.py"
    main_path.write_bytes(injected.encode("utf-8"))
    main_sha = hashlib.sha256(main_path.read_bytes()).hexdigest()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(str(main_path), arcname="main.py")
    tar_bytes = buf.getvalue()
    (out / "submission.tar.gz").write_bytes(tar_bytes)
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "form": form, "name": name, "desc": cfg["desc"],
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "main_sha256": main_sha,
        "main_bytes": main_path.stat().st_size,
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
        "subs": ledger, "subs_roundtrip_identity_ok": True,
        "gate_literal_untouched": True,
        "horizon_k": HORIZON_K, "win_end": WIN_END, "term": TERM,
        "window": ("peak=小时权重 h14-22 1.0/h10-13,23 0.5/其余 0"
                   if form == "peak" else
                   "platform=d12-24 平台 [288,576) 1.0/其余 0.5"),
        "sizing": ("半量门（预测连续跌>$0.5→半量≥1）+峰值全量（帽内）+MR≤0 截止"
                   if form == "peak" else
                   "半量门（预测连续跌>$0.5→半量≥1）+平台小单持续放行"
                   "（lot=max(1,帽×窗权)，不等峰）"),
        "guard": ["①648 后回基线（fire_x=fire_base+基线量帽，零足迹）",
                  "②滞留保险（peak 形态：MR 持有时窗内峰值容量清不掉投射仓"
                  "存量→基线出货）", "异常回退基线语义", "非触发拍零足迹"],
        "items": ["MILK", "STRAWBERRY", "WOOL"],
        "carrot": "可选未启用（站点面 _S758_ITEMS 零改动，CARROT 走基线）",
        "layer_label": LAYER_LABEL,
        "entry": ENTRY_NAME, "entry_last_callable": True,
        "host_entry": HOST_NAME, "compile_ok": True,
        "probes": {"window_edges_ok": True, "cap_tiers_ok": True,
                   "half_gate_ok": True, "win_guard_ok": True},
        "replacements": {
            "p_pred_sites": 4, "take_sites": 4,
            "replacement_point": "MODELPX 整个决策规则（内层全替换）"},
    }
    (out / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest, tail


def main():
    t0 = time.time()
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {"version": "unified-v3-build/1.0",
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "base_main": str(BASE_MAIN), "base_main_sha256": base_sha,
           "kernel_design": {
               "core": "单一连续空间求解器（卖时+卖量+窗联合优化）",
               "projection": "K=12 拍引擎公式价格轨迹，比较全用未取整连续价"
                             "（u1v2 取整修复件）",
               "half_gate": "预测连续跌>$0.5→半量（drop_half 语义并入单核）",
               "peak_clause": "peak=现价≥连续投影峰→全量（帽内）+MR≤0 截止；"
                              "platform=小单持续放行不等峰（D5 平台语义）",
               "window": "peak=小时柔窗；platform=d12-24 平台柔窗（D5）",
               "guards": "648 后回基线+滞留保险；异常回退基线；非触发拍零足迹"},
           "forms": {}}
    tails = {}
    for name, cfg in FORMS.items():
        man, tail = build_one(name, cfg, base_bytes)
        tails[name] = tail
        out["forms"][name] = {k: man[k] for k in
                              ("desc", "main_sha256", "tar_sha256", "subs",
                               "probes", "window", "sizing")}
        print("built", name, man["main_sha256"][:16], flush=True)
    (EVID_DIR / "build_unified_v3.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("BUILD U3 OK", round(time.time() - t0, 1), "s")
    return out


if __name__ == "__main__":
    main()
