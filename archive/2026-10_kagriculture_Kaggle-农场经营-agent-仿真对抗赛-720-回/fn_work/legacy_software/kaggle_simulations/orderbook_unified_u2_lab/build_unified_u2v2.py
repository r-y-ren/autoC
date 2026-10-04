# -*- coding: utf-8 -*-
"""build_unified_u2v2：U2v2 软门构建线（择优或全试；判决先行·不发射不提交）。

背景：U2 硬门（p_now ≥ max(投影K=6)）胜率口径正信号（h2h 0.656、flips_neg 0）
但钱面被过锋利的门拖负（拦 68% 预卖）。U2v2=软门形态，基底同 U2=mpx 胜者件
（orderbook_modelpx_lab/build/mpx_w24_p2_3_h14/main.py，sha f0101de9…）：
  ①容差门 tol：放行 = p_now ≥ max(投影 K=6)×(1−tol)，tol=1%/3% 两档
    （局部峰带容差，容忍投影噪声）；
  ②跌幅门 drop：跌幅 p_now−p_next 触发时改半量放行而非全拦（Wangyh666 公开
    件形态：跌>$0.5 半量前置；drop_half）；及字面形态"仅当跌>$1 才拦"
    （drop1_block）。两形态全试后择优作第三臂。
手术面（字面量替换封印机同口径）：3 组字面量 fail-closed 计数 + 反替换回程
逐字节=mpx 胜者件源；尾块=门层（_U2_MODE/_U2_TOL 参数化）+ 纯透传入口。
648 后回基线守卫沿用（step≥648 门恒过、量整形关断）；非触发拍零足迹；
量帽/窗/时段/品项/planned/阈与 mpx 胜者件逐字节同。只写 orderbook_unified_u2_lab/。
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
BASE_MAIN = (KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
             / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_unified_u2v2_manifest/1.0"
BASE_SHA_EXPECTED = ("f0101de9b558d1f56334739f9a49a0a0d4bc860a898792a9b69fc72c"
                     "3d84e44f")

# ---- 手术台账（3 组字面量；反替换回程=mpx 胜者件源） ----
SUBS = (
    ("if p_next<p_cur-0.5:",
     "if _u2_fire(p_next,p_cur,item,step,inv,rival_avg,p_now,observation):", 4),
    ("take=min(avail,_mx_cap(item,p_now,step,planned))",
     "take=_u2_qty(min(avail,_mx_cap(item,p_now,step,planned)),p_now,p_next,"
     "step)", 1),
    ("take=min(avail,10)",
     "take=_u2_qty(min(avail,10),p_now,p_next,step)", 3),
)

# ---- 形态表（择优或全试：容差两档 + 跌幅族两形态） ----
FORMS = {
    "u2v2_tol1": {"mode": "tol", "tol": 0.01,
                  "desc": "容差门 1%：p_now ≥ max(投影K=6)×0.99"},
    "u2v2_tol3": {"mode": "tol", "tol": 0.03,
                  "desc": "容差门 3%：p_now ≥ max(投影K=6)×0.97"},
    "u2v2_drop1_block": {"mode": "drop_block", "tol": 1.0,
                         "desc": "跌幅门字面：p_now−p_next>$1 才拦，否则全量"},
    "u2v2_drop_half": {"mode": "drop_half", "tol": 0.5,
                       "desc": "跌幅门 Wangyh666 形态：跌>$0.5 半量前置"
                               "（跌幅触发时改半量放行而非全拦）"},
}

GATE_DESIGN = (
    "U2v2 软门（mpx 胜者件窗节奏零改动）：①容差门=放行 iff p_now ≥ "
    "max(投影K=6)×(1−tol)（引擎公式+城镇排水+对手流同 U2；tol 1%/3% 两档）；"
    "②跌幅门 drop_half=Wangyh666 形态（跌>$0.5 触发时 take 取半量≥1 放行，"
    "非全拦）/ drop1_block=字面形态（仅跌>$1 才拦）。648 后回基线守卫沿用"
    "（门恒过+量整形关断）；异常回退基线；非触发拍零足迹；量帽/窗/时段/"
    "品项/planned/阈 0.5 与 mpx 胜者件逐字节同")

TAIL_TMPL = '''

# ---- 件 U2V2：软门（温和统一 v2；mpx 胜者件窗节奏零改动） ------------------
# ---- 入口捕获（宿主=mpx 胜者件末 callable=_mx_agent；须先于本块 def） ----
_U2_HOST = [v for v in list(globals().values()) if callable(v)][-1]

_U2_MODE = "__U2_MODE__"
_U2_TOL = __U2_TOL__
_U2_K = 6
_U2_WIN_END = 648
_U2_SHOPS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_U2_REPORT = dict(calls=0, gate_calls=0, base_fires=0, gate_pass=0,
                  gate_blocked=0, gate_err=0, post648_pass=0, fires=0,
                  half_fires=0)
_U2_DEC = []


def _u2_reset():
    _U2_REPORT.update(calls=0, gate_calls=0, base_fires=0, gate_pass=0,
                      gate_blocked=0, gate_err=0, post648_pass=0, fires=0,
                      half_fires=0)
    del _U2_DEC[:]


def _u2_price(item, inv, params):
    return float(_r37_market_price(item, int(inv), params))


def _u2_params(observation):
    try:
        params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
        for k, patch in (((observation or {}).get("market") or {})
                         .get("params") or {}).items():
            if k in params and isinstance(patch, dict):
                params[k].update(patch)
        return params
    except Exception:
        return None


def _u2_draw(item, step, shops):
    d = 0
    if step % 4 == 0:
        for s in shops or ():
            prods = _U2_SHOPS.get(s) or ()
            if item in prods:
                d += 2 if len(prods) == 1 else 1
    if step % 24 == 0 and item != "FERTILIZER":
        d += 1
    return d


def _u2_proj(item, step, inv, rival_avg, observation):
    """未来 K=6 拍投影价最大值（引擎公式+排水+对手流；expx 同源简化）。"""
    params = _u2_params(observation)
    shops = (((observation or {}).get("town") or {})
             .get("unlocked_shops") or [])
    cur = float(inv)
    proj_max = None
    for t in range(1, _U2_K + 1):
        cur = cur + float(rival_avg) - _u2_draw(item, int(step) + t - 1, shops)
        if cur < 0.0:
            cur = 0.0
        px = _u2_price(item, cur, params)
        if proj_max is None or px > proj_max:
            proj_max = px
    return float(proj_max)


def _u2_pass(item, step, inv, rival_avg, p_now, p_next, observation):
    """软门放行判定（tol/drop_block）；drop_half 恒过（量整形另计）。"""
    if int(step) >= _U2_WIN_END:
        _U2_REPORT["post648_pass"] += 1
        return True
    if _U2_MODE == "drop_half":
        return True
    if _U2_MODE == "drop_block":
        return not (float(p_now) - float(p_next) > _U2_TOL)
    proj_max = _u2_proj(item, step, inv, rival_avg, observation)
    return float(p_now) >= float(proj_max) * (1.0 - _U2_TOL)


def _u2_qty(q, p_now, p_next, step):
    """量整形（仅 drop_half：跌幅触发 take 取半量≥1；648 后关断）。"""
    try:
        q = int(q)
        if _U2_MODE != "drop_half" or q <= 0 or int(step) >= _U2_WIN_END:
            return q
        if float(p_now) - float(p_next) > _U2_TOL:
            half = q // 2
            if half < 1:
                half = 1
            _U2_REPORT["half_fires"] += 1
            return half
        return q
    except Exception:
        _U2_REPORT["gate_err"] += 1
        return q


def _u2_fire(p_next, p_cur, item, step, inv, rival_avg, p_now, observation):
    """MODELPX 预卖放行=基线条件(p_next<p_cur-0.5) ∧ 软门；逐拍门台账。"""
    _U2_REPORT["gate_calls"] += 1
    try:
        base = bool(p_next < p_cur - 0.5)
    except Exception:
        base = False
    if not base:
        return False
    _U2_REPORT["base_fires"] += 1
    try:
        gate = bool(_u2_pass(item, step, inv, rival_avg, p_now, p_next,
                             observation))
    except Exception:
        _U2_REPORT["gate_err"] += 1
        gate = True
    if gate:
        _U2_REPORT["gate_pass"] += 1
        _U2_REPORT["fires"] += 1
    else:
        _U2_REPORT["gate_blocked"] += 1
    try:
        if len(_U2_DEC) < 400:
            _U2_DEC.append([int(step), str(item), True, gate])
    except Exception:
        pass
    return gate


def _u2_agent(observation, configuration=None):
    """u2v2 软门入口（官方 last-callable）：纯透传 + 门台账遥测镜像。"""
    try:
        if int((observation or {}).get("step", 0)) == 0:
            _u2_reset()
    except Exception:
        pass
    action = _U2_HOST(observation, configuration)
    try:
        _MX_REPORT["u2"] = dict(_U2_REPORT)
        _U2_REPORT["calls"] += 1
    except Exception:
        pass
    return action


# ---- 入口归一（末函数=_u2_agent） ----
_U2_ENTRY_TMP = _u2_agent
del _u2_agent
_u2_agent = _U2_ENTRY_TMP
del _U2_ENTRY_TMP
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
        raise RuntimeError("校验②红 %s: 反替换回程 != mpx 胜者件源" % form)
    return src, ledger


def build_form(form, cfg, base_src):
    sub_src, ledger = substitute(base_src, form)
    tail = TAIL_TMPL.replace("__U2_MODE__", str(cfg["mode"])) \
        .replace("__U2_TOL__", repr(float(cfg["tol"])))
    injected = sub_src + tail
    try:
        compile(injected, "<u2v2:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 %s: 语法不通过: %r" % (form, exc))
    ns = {}
    try:
        exec(compile(injected, "<u2v2:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_u2_agent":
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 %s: 末 callable=%r" % (form, got))
    if ns.get("_U2_HOST") is not ns.get("_mx_agent"):
        raise RuntimeError("校验④红 %s: 块首捕获非 _mx_agent" % form)
    got = {"win": int(ns.get("_MX_WIN")), "planned": int(ns.get("_MX_PLANNED")),
           "items": tuple(ns.get("_MX_ITEMS")), "h0": int(ns.get("_MX_H0")),
           "caps": tuple(ns.get("_MX_CAPS")), "mode": ns.get("_U2_MODE"),
           "tol": float(ns.get("_U2_TOL"))}
    want = {"win": 24, "planned": 2, "items": ("MILK", "STRAWBERRY", "WOOL"),
            "h0": 14, "caps": (3, 6, 10), "mode": cfg["mode"],
            "tol": float(cfg["tol"])}
    if got != want:
        raise RuntimeError("校验⑤红 %s: 参数漂移 %r != %r" % (form, got, want))
    if tuple(ns.get("_S758_HOURS")) != tuple(range(14, 23)):
        raise RuntimeError("校验⑤红 %s: _S758_HOURS 漂移" % form)
    _probe_gate(form, ns)
    return injected, ledger, got


def _probe_gate(form, ns):
    """门语义探针（合成观测；引擎公式同源）。"""
    _fire, _pass, _qty = ns["_u2_fire"], ns["_u2_pass"], ns["_u2_qty"]
    _proj = ns["_u2_proj"]
    obs = {"town": {"unlocked_shops": []},
           "market": {"prices": {}, "inventory": {}, "params": {}}}
    if _pass("MILK", 700, 10000, 0.0, 5, 4.0, obs) is not True:
        raise RuntimeError("校验⑤红 %s: 648 后守卫非恒过" % form)
    mode = form
    if "tol" in mode:
        proj = _proj("MILK", 200, 30000, 0.0, obs)
        tol = float(ns["_U2_TOL"])
        if _pass("MILK", 200, 30000, 0.0, proj, proj - 1.0, obs) is not True:
            raise RuntimeError("校验⑤红 %s: p_now=proj 顶应过" % form)
        soft = proj * (1.0 - tol * 0.5)
        if _pass("MILK", 200, 30000, 0.0, soft, soft - 1.0, obs) is not True:
            raise RuntimeError("校验⑤红 %s: 容差带内应过（软化失效）" % form)
        hard = proj * (1.0 - tol * 2.0)
        if _pass("MILK", 200, 30000, 0.0, hard, hard - 1.0, obs) is not False:
            raise RuntimeError("校验⑤红 %s: 容差带外应拦" % form)
    elif mode == "u2v2_drop1_block":
        if _pass("MILK", 200, 10000, 0.0, 10, 8.5, obs) is not False:
            raise RuntimeError("校验⑤红 %s: 跌>$1 应拦" % form)
        if _pass("MILK", 200, 10000, 0.0, 10, 9.5, obs) is not True:
            raise RuntimeError("校验⑤红 %s: 跌≤$1 应过" % form)
    elif mode == "u2v2_drop_half":
        if _pass("MILK", 200, 10000, 0.0, 10, 8.5, obs) is not True:
            raise RuntimeError("校验⑤红 %s: drop_half 门恒过" % form)
        if _qty(10, 10.0, 8.5, 200) != 5:
            raise RuntimeError("校验⑤红 %s: 跌触发应半量" % form)
        if _qty(10, 10.0, 9.8, 200) != 10:
            raise RuntimeError("校验⑤红 %s: 未触发应全量" % form)
        if _qty(10, 10.0, 8.5, 700) != 10:
            raise RuntimeError("校验⑤红 %s: 648 后量整形应关断" % form)
        if _qty(1, 10.0, 8.5, 200) != 1:
            raise RuntimeError("校验⑤红 %s: 半量下限应为 1" % form)
    if _fire(51.0, 51.0, "MILK", 200, 30000, 0.0, 10000, obs) is not False:
        raise RuntimeError("校验⑤红 %s: 非触发拍应零放行" % form)


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
        "entry": "_u2_agent", "host": "_mx_agent",
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
        "subs": ledger, "tail_bytes": len(data) - len(base_bytes),
        "params_locked": got, "compile_ok": True,
        "entry_last_callable": "_u2_agent", "host_captured": "_mx_agent",
        "roundtrip_identity_ok": True,
    }
    (out.parent / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return man


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（mpx 胜者件字节漂移）：%s" % base_sha)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {"version": "unified-u2v2-build/1.0",
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "base_main": str(BASE_MAIN), "base_main_sha256": base_sha,
           "gate_design": GATE_DESIGN, "forms": {}}
    for form, cfg in FORMS.items():
        man = build_one(form, cfg, base_bytes)
        out["forms"][form] = {k: man[k] for k in
                              ("desc", "main_sha256", "tar_sha256", "subs",
                               "params_locked", "roundtrip_identity_ok")}
        print("built", form, man["main_sha256"][:16], flush=True)
    (EVID_DIR / "build_unified_u2v2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_unified_u2v2.json", flush=True)


if __name__ == "__main__":
    main()
