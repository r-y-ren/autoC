# -*- coding: utf-8 -*-
"""build_day2526：d25/26 窗内整形特调构建线（参数替换封印+尾块；判决先行·
不发射不提交）。

背景（forensics_day2526 根因）：drop_half 的半量整形在 d25/26 产线窗（step
576-648；MILK interval2/SHEEP interval3 周期落点 + 小时 1 阶触发密集）扰动
成交节奏/实现价，钱差跨日边界搬运（8 局 traced：d25/26 单日差 +4.75/−22.0，
稀疏 3/8 局；同区域同号于 mpx 网格 d25 −33.6 与 U2 硬门 d26 −33.6）。
修复形态（≤2 臂，按根因）：
  ①d2526_milkpass：d25/26 窗内 MILK 特定品放行（触发时全量前置；余品半量
    照旧）——触发面最大源（step 577/601 小时 1 MILK）直接消形；
  ②d2526_h70：d25/26 窗内半量比例 50%→70%（全品；触发售 70%≥1）——温和
    收敛扰动同时保对冲。
封印机（milkwin 参数替换 + uni_u2 尾块先例）：
  - 字面量替换 2 组（_u2_qty 调用点补 item 形参；fail-closed 计数 1+3）+
    反替换回程逐字节=drop_half 基底（sha 5d2d1246…）；
  - 尾块重绑 _u2_qty（窗 576-648 参数化；窗外/未触发/648 后原样回退
    _U2_QTY_ORIG=drop_half 原装）；非触发拍零足迹；守恒零跨拍红线不碰；
  - 入口 _d2526_agent 末 callable 归一 + 纯透传台账。
  - 中性形 d2526_neutral（mode=off）供等价封印：同 (seed,seat) 动作流 digest
    全等 + 终局钱相等 vs drop_half。
只写 orderbook_day2526_lab/。不改既有代码；不提交；不发射。
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
BASE_MAIN = (KSIM_DIR / "orderbook_unified_u2_lab" / "build" / "u2v2_drop_half"
             / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_day2526_manifest/1.0"
BASE_SHA_EXPECTED = ("5d2d12468a5d1ec53c3d3e4726de54e6a5d29eb038fc97ca45c72b2c"
                     "e7992df0")

# ---- 手术台账（2 组字面量：_u2_qty 调用点补 item；反替换回程=drop_half 源） ----
SUBS = (
    ("take=_u2_qty(min(avail,_mx_cap(item,p_now,step,planned)),p_now,p_next,"
     "step)",
     "take=_u2_qty(min(avail,_mx_cap(item,p_now,step,planned)),p_now,p_next,"
     "step,item)", 1),
    ("take=_u2_qty(min(avail,10),p_now,p_next,step)",
     "take=_u2_qty(min(avail,10),p_now,p_next,step,item)", 3),
)

FORMS = {
    "d2526_milkpass": {
        "mode": "milk_pass", "ratio": 0.5,
        "desc": "d25/26 窗（step 576-648）内 MILK 特定品放行：触发时全量前置"
                "（不整形），余品半量照旧；窗外原样"},
    "d2526_h70": {
        "mode": "h70", "ratio": 0.7,
        "desc": "d25/26 窗（step 576-648）内半量比例 50%→70%：触发时售 70%≥1"
                "（全品）；窗外原样"},
    "d2526_neutral": {
        "mode": "off", "ratio": 0.5,
        "desc": "中性封印形（mode=off 恒回退 drop_half 原装 _u2_qty）：等价"
                "封印专用，不参判"},
}

TAIL_TMPL = '''

# ---- 件 D2526：d25/26 窗内整形特调（drop_half 基底零改；尾块重绑 _u2_qty） ----
# ---- 入口捕获（宿主=drop_half 末 callable=_u2_agent；须先于本块 def） ----
_D2526_HOST = [v for v in list(globals().values()) if callable(v)][-1]

_D2526_MODE = "__D2526_MODE__"
_D2526_RATIO = __D2526_RATIO__
_D2526_WIN = (576, 648)
_D2526_DROP = 0.5
_D2526_REPORT = dict(calls=0, shaped=0, milk_pass=0, h70_fires=0, fallback=0)
_D2526_QTY_ORIG = _u2_qty


def _d2526_qty(q, p_now, p_next, step, item=None):
    """窗内整形特调（step 576-648）；窗外/未触发/异常原样回退 drop_half。"""
    _D2526_REPORT["fallback"] += 1
    try:
        s = int(step)
        qi = int(q)
    except Exception:
        return _D2526_QTY_ORIG(q, p_now, p_next, step)
    if not (_D2526_WIN[0] <= s < _D2526_WIN[1]) or qi <= 0:
        return _D2526_QTY_ORIG(q, p_now, p_next, step)
    try:
        triggered = float(p_now) - float(p_next) > _D2526_DROP
    except Exception:
        triggered = False
    if not triggered:
        return _D2526_QTY_ORIG(q, p_now, p_next, step)
    if _D2526_MODE == "milk_pass":
        _D2526_REPORT["shaped"] += 1
        if str(item) == "MILK":
            _D2526_REPORT["milk_pass"] += 1
            return qi
        half = qi // 2
        if half < 1:
            half = 1
        return half
    if _D2526_MODE == "h70":
        _D2526_REPORT["shaped"] += 1
        _D2526_REPORT["h70_fires"] += 1
        frac = (qi * int(round(_D2526_RATIO * 100.0))) // 100
        if frac < 1:
            frac = 1
        return frac
    return _D2526_QTY_ORIG(q, p_now, p_next, step)


# ---- 重绑：调用点（字面量替换后）仍按名 _u2_qty 解析 → 特调接管 ----
_u2_qty = _d2526_qty


def _d2526_agent(observation, configuration=None):
    """d2526 入口（官方 last-callable）：纯透传 + 特调台账镜像。"""
    try:
        if int((observation or {}).get("step", 0)) == 0:
            _D2526_REPORT.update(calls=0, shaped=0, milk_pass=0, h70_fires=0,
                                 fallback=0)
    except Exception:
        pass
    action = _D2526_HOST(observation, configuration)
    try:
        _MX_REPORT["d2526"] = dict(_D2526_REPORT)
        _D2526_REPORT["calls"] += 1
    except Exception:
        pass
    return action


# ---- 入口归一（末函数=_d2526_agent） ----
_D2526_ENTRY_TMP = _d2526_agent
del _d2526_agent
_d2526_agent = _D2526_ENTRY_TMP
del _D2526_ENTRY_TMP
'''


def substitute(base_src, form):
    src = base_src
    ledger = []
    for old, new, expect in SUBS:
        n = src.count(old)
        if n != expect:
            raise RuntimeError("校验①红 %s: 字面量计数 %d 应为 %d: %r"
                               % (form, n, expect, old))
        src = src.replace(old, new)
        ledger.append({"old": old, "new": new, "count": n})
    back = src
    for old, new, cnt in reversed(SUBS):
        if back.count(new) != cnt:
            raise RuntimeError("校验②红 %s: 反替换计数漂移: %r" % (form, new))
        back = back.replace(new, old)
    if back != base_src:
        raise RuntimeError("校验②红 %s: 反替换回程 != drop_half 基底源" % form)
    return src, ledger


def build_form(form, cfg, base_src):
    sub_src, ledger = substitute(base_src, form)
    tail = TAIL_TMPL.replace("__D2526_MODE__", str(cfg["mode"])) \
        .replace("__D2526_RATIO__", repr(float(cfg["ratio"])))
    injected = sub_src + tail
    try:
        compile(injected, "<d2526:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 %s: 语法不通过: %r" % (form, exc))
    ns = {}
    try:
        exec(compile(injected, "<d2526:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_d2526_agent":
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 %s: 末 callable=%r" % (form, got))
    if ns.get("_D2526_HOST") is not ns.get("_u2_agent"):
        raise RuntimeError("校验④红 %s: 块首捕获非 _u2_agent" % form)
    if ns.get("_u2_qty") is not ns.get("_d2526_qty"):
        raise RuntimeError("校验④红 %s: _u2_qty 重绑失效" % form)
    if ns.get("_D2526_QTY_ORIG") is ns.get("_u2_qty") or \
            getattr(ns.get("_D2526_QTY_ORIG"), "__name__", "") != "_u2_qty":
        raise RuntimeError("校验④红 %s: 原装 _u2_qty 捕获漂移" % form)
    got = {"mode": ns.get("_D2526_MODE"), "ratio": float(ns.get("_D2526_RATIO")),
           "win": tuple(ns.get("_D2526_WIN")), "drop": float(ns.get("_D2526_DROP")),
           "u2_mode": ns.get("_U2_MODE"), "u2_tol": float(ns.get("_U2_TOL"))}
    want = {"mode": cfg["mode"], "ratio": float(cfg["ratio"]),
            "win": (576, 648), "drop": 0.5, "u2_mode": "drop_half",
            "u2_tol": 0.5}
    if got != want:
        raise RuntimeError("校验⑤红 %s: 参数漂移 %r != %r" % (form, got, want))
    _probe(form, ns)
    return injected, ledger, got


def _probe(form, ns):
    """特调语义探针（经重绑名 _u2_qty 走线；drop_half 原装=回退基准）。"""
    qty = ns["_u2_qty"]
    # 回退基准（drop_half 原装）：触发半量≥1；未触发全量；648 后关断
    if qty(10, 10.0, 8.5, 300, "MILK") != 5:
        raise RuntimeError("校验⑤红 %s: 窗外触发应原样半量" % form)
    if qty(10, 10.0, 9.8, 600, "MILK") != 10:
        raise RuntimeError("校验⑤红 %s: 未触发应原样全量" % form)
    if qty(10, 10.0, 8.5, 700, "MILK") != 10:
        raise RuntimeError("校验⑤红 %s: 648 后应原样关断" % form)
    if form == "d2526_milkpass":
        if qty(10, 10.0, 8.5, 600, "MILK") != 10:
            raise RuntimeError("校验⑤红 %s: 窗内 MILK 应全量放行" % form)
        if qty(10, 10.0, 8.5, 600, "WOOL") != 5:
            raise RuntimeError("校验⑤红 %s: 窗内余品应照旧半量" % form)
        if qty(1, 10.0, 8.5, 576, "STRAWBERRY") != 1:
            raise RuntimeError("校验⑤红 %s: 半量下限应为 1" % form)
    elif form == "d2526_h70":
        if qty(10, 10.0, 8.5, 600, "MILK") != 7:
            raise RuntimeError("校验⑤红 %s: 窗内触发应 70%%" % form)
        if qty(3, 10.0, 8.5, 576, "WOOL") != 2:
            raise RuntimeError("校验⑤红 %s: 70%% 取整应向下且≥1" % form)
        if qty(1, 10.0, 8.5, 600, "MILK") != 1:
            raise RuntimeError("校验⑤红 %s: 70%% 下限应为 1" % form)
    elif form == "d2526_neutral":
        if qty(10, 10.0, 8.5, 600, "MILK") != 5:
            raise RuntimeError("校验⑤红 %s: 中性形窗内应原样半量" % form)
    fire = ns["_u2_fire"]
    obs = {"town": {"unlocked_shops": []},
           "market": {"prices": {}, "inventory": {}, "params": {}}}
    if fire(51.0, 51.0, "MILK", 200, 30000, 0.0, 10000, obs) is not False:
        raise RuntimeError("校验⑤红 %s: 非触发拍应零放行（门零改）" % form)


def build_one(form, cfg, base_bytes):
    base_src = base_bytes.decode("utf-8")
    injected, ledger, got = build_form(form, cfg, base_src)
    data = injected.encode("utf-8")
    out = OUT_DIR / form / "main.py"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(str(out), arcname="main.py")
    tar_bytes = buf.getvalue()
    (out.parent / "submission.tar.gz").write_bytes(tar_bytes)
    man = {
        "schema": SCHEMA, "form": form, "desc": cfg["desc"],
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "entry": "_d2526_agent", "host": "_u2_agent",
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "subs": ledger, "tail_bytes": len(data) - len(base_bytes),
        "params_locked": got, "compile_ok": True,
        "entry_last_callable": "_d2526_agent",
        "roundtrip_identity_ok": True,
    }
    (out.parent / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return man


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("基底 sha 不符（drop_half 字节漂移）：%s" % base_sha)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {"version": "day2526-build/1.0",
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "base_main": str(BASE_MAIN), "base_main_sha256": base_sha,
           "forms": {}}
    for form, cfg in FORMS.items():
        man = build_one(form, cfg, base_bytes)
        out["forms"][form] = {k: man[k] for k in
                              ("desc", "main_sha256", "tar_sha256", "subs",
                               "params_locked", "roundtrip_identity_ok")}
        print("built", form, man["main_sha256"][:16], flush=True)
    (EVID_DIR / "build_day2526.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_day2526.json", flush=True)


if __name__ == "__main__":
    main()
