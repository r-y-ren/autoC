# -*- coding: utf-8 -*-
"""build_unified_u2：U2 温和统一构建线（模型门控形态；判决先行·不发射不提交）。

背景：mpx 焦窗（+175.7）与 expx 模型核（+81）同面不可堆叠。U2=温和统一：
基底=mpx 胜者件（orderbook_modelpx_lab/build/mpx_w24_p2_3_h14/main.py，
sha f0101de9…）零改动读入，**只加门不动节奏**——MODELPX 预卖单放行条件加
一条模型门：当前报价 ≥ 未来 K=6 拍投影价（引擎公式 _r37_market_price +
城镇排水表 + 对手流；expx 件同源简化版）→ 只在模型判"当前=窗内局部峰"时
才放行预卖，不卖在下坡上。

手术面（字面量替换封印机同口径复用 orderbook_modelpx_lab）：
  ① `if p_next<p_cur-0.5:` ×4 → `if _u2_fire(...)`（计数 fail-closed；
    _u2_fire 内部=基线条件 ∧ 模型门；反替换回程逐字节=mpx 胜者件源）；
  ② 尾块追加：门层（_U2_K=6、648 后回基线守卫、异常回退基线、逐拍门台账
    _U2_REPORT/_U2_DEC）+ 入口捕获（宿主=mpx 件末 callable _mx_agent）+
    纯透传入口 _u2_agent（仅遥测镜像 _MX_REPORT['u2']，动作零改动）。
量帽 _mx_cap/窗 _S758_HOURS/_MX_WIN/planned/品项集与 mpx 胜者件逐字节同；
648 后门恒过=基线语义；非触发拍零足迹（fire_u2==fire_base 同码路；门纯收紧）。
四门体检（load/health/determinism/identity）复用 gates_oppcond 口径。
只写 orderbook_unified_u2_lab/。
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
FORM = "u2"
SCHEMA = "orderbook_unified_u2_manifest/1.0"
BASE_SHA_EXPECTED = ("f0101de9b558d1f56334739f9a49a0a0d4bc860a898792a9b69fc72c"
                     "3d84e44f")

# ---- 手术台账（1 组字面量 ×4；反替换回程=mpx 胜者件源） ----
SUB_OLD = "if p_next<p_cur-0.5:"
SUB_NEW = "if _u2_fire(p_next,p_cur,item,step,inv,rival_avg,p_now,observation):"
SUBS = ((SUB_OLD, SUB_NEW, 4),)

GATE_DESIGN = (
    "门=MODELPX 预卖放行条件加一：当前报价 p_now ≥ 未来 K=6 拍投影价最大值"
    "（当前=窗内局部峰才放行，不卖在下坡上）；投影=expx 件同源简化版"
    "（引擎公式 _r37_market_price+参数表、城镇排水 _u2_draw、对手流 rival_avg"
    "=站点 S758 侧 4 拍均值）；648 后回基线守卫沿用（step≥648 门恒过=mpx "
    "基线语义）；异常回退基线（门恒过+gate_err 计数）；门纯收紧"
    "（fire_u2=fire_base∧gate，只可能少卖不可能多卖）；量帽/窗/时段/品项/"
    "planned/阈 0.5 与 mpx 胜者件逐字节同（只加门不动节奏）")

# ---- 尾块：门层 + 入口捕获（纯透传+遥测镜像） ----
TAIL_TMPL = '''

# ---- 件 U2：模型门（温和统一；mpx 胜者件窗节奏零改动 + K=6 投影门） --------
# ---- 入口捕获（宿主=mpx 胜者件末 callable=_mx_agent；须先于本块 def） ----
_U2_HOST = [v for v in list(globals().values()) if callable(v)][-1]

_U2_K = 6
_U2_WIN_END = 648
_U2_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
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
                  gate_blocked=0, gate_err=0, post648_pass=0, fires=0)
_U2_DEC = []


def _u2_reset():
    _U2_REPORT.update(calls=0, gate_calls=0, base_fires=0, gate_pass=0,
                      gate_blocked=0, gate_err=0, post648_pass=0, fires=0)
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


def _u2_gate(item, step, inv, rival_avg, p_now, observation):
    """模型门：p_now >= max(未来 K=6 拍投影价) 才放行（当前=窗内局部峰）。
    648 后回基线守卫沿用（门恒过）；异常回退基线（门恒过）。"""
    try:
        if int(step) >= _U2_WIN_END:
            _U2_REPORT["post648_pass"] += 1
            return True
        params = _u2_params(observation)
        shops = (((observation or {}).get("town") or {})
                 .get("unlocked_shops") or [])
        cur = float(inv)
        proj_max = None
        for t in range(1, _U2_K + 1):
            cur = cur + float(rival_avg) - _u2_draw(item, int(step) + t - 1,
                                                    shops)
            if cur < 0.0:
                cur = 0.0
            px = _u2_price(item, cur, params)
            if proj_max is None or px > proj_max:
                proj_max = px
        return float(p_now) >= float(proj_max)
    except Exception:
        _U2_REPORT["gate_err"] += 1
        return True


def _u2_fire(p_next, p_cur, item, step, inv, rival_avg, p_now, observation):
    """MODELPX 预卖放行=基线条件(p_next<p_cur-0.5) ∧ 模型门；逐拍门台账。"""
    _U2_REPORT["gate_calls"] += 1
    try:
        base = bool(p_next < p_cur - 0.5)
    except Exception:
        base = False
    if not base:
        return False
    _U2_REPORT["base_fires"] += 1
    try:
        gate = bool(_u2_gate(item, step, inv, rival_avg, p_now, observation))
    except Exception:
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
    """u2 统一门控入口（官方 last-callable）：纯透传 + 门台账遥测镜像。"""
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


def substitute(base_src):
    src = base_src
    ledger = []
    for old, new, expect in SUBS:
        n = src.count(old)
        if n != expect:
            raise RuntimeError("校验①红: 字面量计数 %d 应为 %d: %r"
                               % (n, expect, old))
        src = src.replace(old, new)
        ledger.append({"old": old, "new": new, "count": n})
    back = src
    for old, new, cnt in reversed(SUBS):
        if back.count(new) != cnt:
            raise RuntimeError("校验②红: 反替换计数漂移: %r" % (new,))
        back = back.replace(new, old)
    if back != base_src:
        raise RuntimeError("校验②红: 反替换回程 != mpx 胜者件源")
    return src, ledger


def build_form(base_src):
    sub_src, ledger = substitute(base_src)
    injected = sub_src + TAIL_TMPL
    try:
        compile(injected, "<u2>", "exec")
    except Exception as exc:
        raise RuntimeError("校验③红: 注入后源语法不通过: %r" % (exc,))
    ns = {}
    try:
        exec(compile(injected, "<u2>", "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红: exec 失败: %r" % (exc,))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_u2_agent":
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红: 末 callable=%r 应为 '_u2_agent'" % (got,))
    if ns.get("_U2_HOST") is not ns.get("_mx_agent"):
        raise RuntimeError("校验④红: 块首捕获非 _mx_agent")
    # 基座语义抽查（量帽/窗/planned/品项集与 mpx 胜者件同参）
    got = {"win": int(ns.get("_MX_WIN")), "planned": int(ns.get("_MX_PLANNED")),
           "items": tuple(ns.get("_MX_ITEMS")), "h0": int(ns.get("_MX_H0")),
           "caps": tuple(ns.get("_MX_CAPS"))}
    want = {"win": 24, "planned": 2, "items": ("MILK", "STRAWBERRY", "WOOL"),
            "h0": 14, "caps": (3, 6, 10)}
    if got != want:
        raise RuntimeError("校验⑤红: mpx 参数漂移 got=%r want=%r" % (got, want))
    if tuple(ns.get("_S758_HOURS")) != tuple(range(14, 23)):
        raise RuntimeError("校验⑤红: _S758_HOURS 漂移 %r"
                           % (ns.get("_S758_HOURS"),))
    # 门语义探针（合成观测；引擎公式同源）
    _gate = ns["_u2_gate"]
    _fire = ns["_u2_fire"]
    obs = {"town": {"unlocked_shops": []},
           "market": {"prices": {}, "inventory": {}, "params": {}}}
    if _gate("MILK", 700, 10000, 0.0, 5, obs) is not True:
        raise RuntimeError("校验⑤红: 648 后守卫非恒过")
    # 库存高水位→投影价贴地板：p_now 高位必过；库存 0→投影价在峰顶：必拦
    peak = _gate("MILK", 200, 0, 0.0, 1, obs)
    trough = _gate("MILK", 200, 30000, 0.0, 10000, obs)
    if peak is not False or trough is not True:
        raise RuntimeError("校验⑤红: 门方向错 peak=%r trough=%r"
                           % (peak, trough))
    if _fire(51.0, 51.0, "MILK", 200, 30000, 0.0, 10000, obs) is not False:
        raise RuntimeError("校验⑤红: 非触发拍应零放行")
    if _fire(50.0, 52.0, "MILK", 200, 30000, 0.0, 10000, obs) is not True:
        raise RuntimeError("校验⑤红: 触发+门过应放行")
    if _fire(50.0, 52.0, "MILK", 200, 0, 0.0, 1, obs) is not False:
        raise RuntimeError("校验⑤红: 门拦（下坡）应扣留")
    if ns["_U2_REPORT"]["gate_blocked"] != 1 or \
            ns["_U2_REPORT"]["gate_pass"] != 1 or \
            ns["_U2_REPORT"]["base_fires"] != 2 or \
            ns["_U2_REPORT"]["gate_calls"] != 3:
        raise RuntimeError("校验⑤红: 门台账漂移 %r" % (ns["_U2_REPORT"],))
    return injected, ledger, got


def build_one(base_bytes):
    base_src = base_bytes.decode("utf-8")
    injected, ledger, got = build_form(base_src)
    data = injected.encode("utf-8")
    out = OUT_DIR / FORM / "main.py"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    tar_path = out.parent / "submission.tar.gz"
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(str(out), arcname="main.py")
    tar_bytes = buf.getvalue()
    tar_path.write_bytes(tar_bytes)
    man = {
        "schema": SCHEMA, "form": FORM,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "entry": "_u2_agent", "host": "_mx_agent",
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
        "subs": ledger,
        "tail_bytes": len(data) - len(base_bytes),
        "mpx_params_locked": got,
        "gate_design": GATE_DESIGN,
        "compile_ok": True, "entry_last_callable": "_u2_agent",
        "host_captured": "_mx_agent",
        "roundtrip_identity_ok": True,
        "reverse_extraction": "尾块剥离 + 字面量反替换 → 逐字节=mpx 胜者件源",
    }
    (out.parent / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return man


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（mpx 胜者件字节漂移）：%s" % base_sha)
    if not base_bytes.decode("utf-8").endswith("\n"):
        raise RuntimeError("构建底不以换行收尾（fail-closed）")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    man = build_one(base_bytes)
    out = {
        "version": "unified-u2-build/1.0",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN), "base_main_sha256": base_sha,
        "gate_design": GATE_DESIGN,
        "form": {k: man[k] for k in ("form", "main_sha256", "main_bytes",
                                     "tar_sha256", "subs", "tail_bytes",
                                     "mpx_params_locked",
                                     "roundtrip_identity_ok")},
    }
    (EVID_DIR / "build_unified_u2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("built", FORM, man["main_sha256"][:16], man["main_bytes"], "bytes",
          flush=True)


if __name__ == "__main__":
    main()
