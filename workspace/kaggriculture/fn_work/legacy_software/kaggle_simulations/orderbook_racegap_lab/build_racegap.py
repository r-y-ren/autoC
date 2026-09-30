# -*- coding: utf-8 -*-
"""build_racegap：同拍竞速深化两臂构建线（T2 同族缺口利用；判决先行·不发射不提交）。

背景（同族主流=idle-seller 保守稳节奏）：卖窗窄而稳、按稳定周期出货、同拍 SELL
槽序重排抢成交；镜像同拍价差 8-10%。基底=u2v2 drop_half（sha 5d2d1246…）已含
X1 卫生层（并最早槽）。两臂只动挂单与追加（红线：零跨拍挪量）：
  ① gap 臂（缺口利用）：MODELPX/日新高追加单的放行时点加对手流感知——R28 删失
    口径对手出货流（invΔ+精确排水−own_sold，0 删失）近 3 拍 ≤2 单位（非出货
    缺口=其强拍之间）才放行追加，高→让位。收口：4 处 MODELPX（_u2_fire 全局
    重绑，纯收紧）+4 处日新高追加（S928/S932/S939/S948 字面量）。
  ② slot 臂（槽序匹配）：同拍我方 SELL 单优先级按对手同拍 SELL 单序对齐/抢先
    （对手列序不可见，按稳态节拍先验预测其强拍项；同拍内我单插其单前=X1 并
    最早槽的对手自适应版）：纯同拍重排——非洗仓可购品 SELL 前置最早列、
    预测同拍碰撞项先行（对齐其强品序）；洗仓腿/非 SELL/同品组相对序不动。
手术面：字面量替换封印（gap 4 组）+尾块；反替换回程逐字节=u2v2_drop_half 源。
只写 orderbook_racegap_lab/。
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
SCHEMA = "orderbook_racegap_manifest/1.0"
BASE_SHA_EXPECTED = ("5d2d12468a5d1ec53c3d3e4726de54e6a5d29eb038fc97ca45c72b2c"
                     "e7992df0")

# ---- gap 臂手术台账（4 处日新高追加放行点字面量；MODELPX 4 处经 _u2_fire 收口） ----
GAP_SUBS = (
    # S928 日新高动物品追加（逐拍）：eligible 扫描加缺口门
    ("            if price <= int(prior.get(item, price)):\n"
     "                continue",
     "            if price <= int(prior.get(item, price)) or not "
     "_rgp_gap_ok(item, step, p):\n"
     "                continue", 1),
    # S932 step709 携带 MILK 变现追加
    ("        if price <= prior:\n            return action",
     "        if price <= prior or not _rgp_gap_ok('MILK', step, p):\n"
     "            return action", 1),
    # S939 step693 无效 PLACE 携带 MILK 变现追加
    ("        if price<=prior:return action",
     "        if price<=prior or not _rgp_gap_ok('MILK',step,p):return action",
     1),
    # S948 日新高非消耗作物追加（逐拍；already 行锚定=与 S952/S953 同字面区分）
    ("            if price<=int(prior.get(item,price)):continue\n"
     "            already=",
     "            if price<=int(prior.get(item,price)) or not "
     "_rgp_gap_ok(item, step, p):continue\n"
     "            already=", 1),
)

# ---- 流跟踪公共块（gap/slot 两臂同式：R28 删失口径对手出货流窗） ----
FLOW_COMMON = '''
def _rgp_update(observation, action):
    """R28 删失口径对手出货流：d=inv'−inv+town_draw−own_sold，0 删失；24 拍滚动。"""
    try:
        step = int((observation or {}).get("step", 0))
        player = int((observation or {}).get("player", 0))
        inv = (((observation or {}).get("market") or {}).get("inventory") or {})
        shops = list((((observation or {}).get("town") or {})
                      .get("unlocked_shops") or []))
        own = {}
        for o in ((action or {}).get("market") or []):
            if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL":
                q = _x1_qty(o[2])
                if q is not None and q > 0:
                    own[str(o[1])] = own.get(str(o[1]), 0) + q
        flow = _RGP_FLOW.setdefault(player, {})
        prev = _RGP_PREV.get(player)
        if prev and prev.get("step") == step - 1:
            for item in _RGP_ITEMS:
                try:
                    d = (int(inv.get(item, 0)) - int(prev["inv"].get(item, 0))
                         + _u2_draw(item, step - 1, prev.get("shops") or ())
                         - int(prev["own"].get(item, 0)))
                except Exception:
                    continue
                if d < 0:
                    _RGP_REPORT["censored_lo"] += 1
                row = flow.setdefault(item, [])
                row.append(max(0, d))
                if len(row) > _RGP_HIST_LEN:
                    del row[:len(row) - _RGP_HIST_LEN]
            _RGP_REPORT["updates"] += 1
        _RGP_PREV[player] = {
            "step": step,
            "inv": {i: int(inv.get(i, 0)) for i in _RGP_ITEMS},
            "own": own, "shops": shops}
    except Exception:
        _RGP_REPORT["errors"] += 1


def _rgp_gap_ok(item, step, player):
    """近 _RGP_WIN 拍对手出货量（删失口径）≤_RGP_GAP_MAX → 非出货缺口→True。
    窗未满/异常→True（基线放行）；高→False（让位）。纯收紧语义。"""
    try:
        _RGP_REPORT["gap_evals"] += 1
        row = (_RGP_FLOW.get(int(player)) or {}).get(str(item)) or []
        if len(row) < _RGP_WIN:
            _RGP_REPORT["gap_pass"] += 1
            return True
        ok = sum(row[-_RGP_WIN:]) <= _RGP_GAP_MAX
        if ok:
            _RGP_REPORT["gap_pass"] += 1
        else:
            _RGP_REPORT["gap_yield"] += 1
        return ok
    except Exception:
        _RGP_REPORT["errors"] += 1
        return True
'''

GAP_TAIL = '''

# ---- 件 RGP：同族缺口利用（gap 臂；追加放行时点对手流感知） --------------------
# ---- 入口捕获（宿主=u2v2 drop_half 末 callable=_u2_agent；须先于本块 def） ----
_RGP_HOST = [v for v in list(globals().values()) if callable(v)][-1]

_RGP_GAP_MAX = 2
_RGP_WIN = 3
_RGP_HIST_LEN = 24
_RGP_ITEMS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG",
              "MILK", "WOOL", "FERTILIZER")
_RGP_FLOW = {}
_RGP_PREV = {}
_RGP_REPORT = dict(calls=0, updates=0, gap_evals=0, gap_pass=0, gap_yield=0,
                   fire_pass=0, fire_yield=0, censored_lo=0, errors=0)
''' + FLOW_COMMON + '''

def _rgp_reset():
    _RGP_REPORT.update(calls=0, updates=0, gap_evals=0, gap_pass=0,
                       gap_yield=0, fire_pass=0, fire_yield=0, censored_lo=0,
                       errors=0)
    _RGP_FLOW.clear()
    _RGP_PREV.clear()


_RGP_ORIG_FIRE = _u2_fire


def _rgp_fire(p_next, p_cur, item, step, inv, rival_avg, p_now, observation):
    """MODELPX 4 处追加收口：基线 _u2_fire ∧ 对手缺口门（纯收紧）。"""
    base = _RGP_ORIG_FIRE(p_next, p_cur, item, step, inv, rival_avg, p_now,
                          observation)
    if not base:
        return False
    try:
        player = int((observation or {}).get("player", 0))
    except Exception:
        player = 0
    ok = _rgp_gap_ok(item, step, player)
    if ok:
        _RGP_REPORT["fire_pass"] += 1
    else:
        _RGP_REPORT["fire_yield"] += 1
    return ok


_u2_fire = _rgp_fire


def _rgp_agent(observation, configuration=None):
    """gap 臂入口（官方 last-callable）：透传 + 逐拍流窗更新 + 台账镜像。"""
    try:
        if int((observation or {}).get("step", 0)) == 0:
            _rgp_reset()
    except Exception:
        pass
    action = _RGP_HOST(observation, configuration)
    _rgp_update(observation, action)
    _RGP_REPORT["calls"] += 1
    try:
        _MX_REPORT["rgp"] = dict(_RGP_REPORT)
    except Exception:
        pass
    return action
'''

SLOT_TAIL = '''

# ---- 件 RGS：同族槽序匹配（slot 臂；同拍 SELL 槽序对齐/抢先） -----------------
# ---- 入口捕获（宿主=u2v2 drop_half 末 callable=_u2_agent；须先于本块 def） ----
_RGS_HOST = [v for v in list(globals().values()) if callable(v)][-1]

# 同拍竞速标的=非洗仓可购品（对手无 BUY 侧对冲：WHEAT/FERTILIZER 有 BUY_PRODUCT
# 洗仓腿不动）；纯同拍重排：零改量/零加减单/同品组相对序不动/非 SELL 相对序不动。
_RGS_RACE_ITEMS = ("CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK",
                   "WOOL")
_RGP_GAP_MAX = 2
_RGP_WIN = 3
_RGP_HIST_LEN = 24
_RGP_ITEMS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG",
              "MILK", "WOOL", "FERTILIZER")
_RGP_FLOW = {}
_RGP_PREV = {}
_RGP_REPORT = dict(calls=0, updates=0, gap_evals=0, gap_pass=0, gap_yield=0,
                   fire_pass=0, fire_yield=0, censored_lo=0, errors=0)
_RGS_REPORT = dict(calls=0, turns=0, moved_sells=0, collision_pins=0,
                   front_pins=0, invariant_violations=0, errors=0)
''' + FLOW_COMMON + '''

def _rgs_reset():
    _RGP_REPORT.update(calls=0, updates=0, gap_evals=0, gap_pass=0,
                       gap_yield=0, fire_pass=0, fire_yield=0, censored_lo=0,
                       errors=0)
    _RGP_FLOW.clear()
    _RGP_PREV.clear()
    _RGS_REPORT.update(calls=0, turns=0, moved_sells=0, collision_pins=0,
                       front_pins=0, invariant_violations=0, errors=0)


def _rgs_beat(item, step, player):
    """对手稳态节拍预测（同拍 SELL 单序先验）：正流出拍间隔中位数 p̂；
    (step−last_beat) 整除 p̂ → 该品为对手同拍强拍（碰撞项）。
    返回 (due, strength)；强度=其最近拍出货量（强品先行=其单序稳态先验）。"""
    try:
        row = (_RGP_FLOW.get(int(player)) or {}).get(str(item)) or []
        beats = [i for i, v in enumerate(row) if v >= 1]
        if len(beats) < 2:
            return False, 0
        gaps = sorted(beats[i + 1] - beats[i] for i in range(len(beats) - 1))
        phat = max(1, gaps[len(gaps) // 2])
        last = beats[-1]
        last_step = step - 1 - (len(row) - 1 - last)
        if step <= last_step:
            return False, 0
        due = ((step - last_step) % phat) == 0
        return bool(due), int(row[last])
    except Exception:
        return False, 0


def _rgs_slot(observation, action):
    """同拍我方 SELL 单对齐/抢先（v2 保序形态；纯重排）：
    ①对齐=SELL 相对序不动（基底计划序=对手稳态单序先验，扫查实测同拍同序
    38/51；v1 碰撞项重排经诊断破序致负已删）；
    ②抢先=自由 SELL（无同列表同品 BUY_*）越非卖单冒泡前置（我单插其单前）；
    ③洗仓腿/同品组/SELL 相对序/非 SELL 相对序不动；无可改→原对象零足迹。"""
    _RGS_REPORT["calls"] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list) or len(market) < 2:
            return action
        orders = [list(o) if isinstance(o, (list, tuple)) else o for o in market]
        bought = set()
        for o in orders:
            if (isinstance(o, list) and len(o) >= 3
                    and str(o[0]) in ("BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL")):
                bought.add(str(o[1]))

        def is_sell(o):
            return (isinstance(o, list) and len(o) >= 3 and o[0] == "SELL"
                    and (_x1_qty(o[2]) or 0) > 0)

        def is_free_sell(o):
            return is_sell(o) and str(o[1]) not in bought

        out = list(orders)
        moved = 0
        changed = True
        while changed:
            changed = False
            for i in range(1, len(out)):
                if is_free_sell(out[i]) and not is_sell(out[i - 1]):
                    out[i - 1], out[i] = out[i], out[i - 1]
                    moved += 1
                    changed = True
        if not moved or all(a is b for a, b in zip(out, orders)):
            return action

        def key(o):
            if not isinstance(o, (list, tuple)):
                return ("raw", str(o))
            return (str(o[0]) if len(o) > 0 else "",
                    str(o[1]) if len(o) > 1 else "",
                    _x1_qty(o[2]) if len(o) > 2 else None)

        if sorted(map(key, orders)) != sorted(map(key, out)):
            _RGS_REPORT["invariant_violations"] += 1
            return action
        _RGS_REPORT["turns"] += 1
        _RGS_REPORT["moved_sells"] += sum(1 for o in out if is_free_sell(o))
        _RGS_REPORT["front_pins"] += moved
        return dict(action, market=out)
    except Exception:
        _RGS_REPORT["errors"] += 1
        return action


def _rgs_agent(observation, configuration=None):
    """slot 臂入口（官方 last-callable）：宿主动作→同拍槽序重排+流窗更新。"""
    try:
        if int((observation or {}).get("step", 0)) == 0:
            _rgs_reset()
    except Exception:
        pass
    action = _RGS_HOST(observation, configuration)
    action = _rgs_slot(observation, action)
    _rgp_update(observation, action)
    _RGS_REPORT["calls"] += 1
    try:
        _MX_REPORT["rgs"] = dict(_RGS_REPORT)
        _MX_REPORT["rgs_flow"] = dict(_RGP_REPORT)
    except Exception:
        pass
    return action
'''

ARMS = {
    "gap": {
        "desc": "缺口利用：MODELPX/日新高追加放行加对手流门（近3拍出货≤2 才放行）",
        "subs": GAP_SUBS, "tail": GAP_TAIL, "entry": "_rgp_agent",
        "host": "_u2_agent",
        "mechanism": (
            "R28 删失口径对手出货流窗（invΔ+_u2_draw 精确排水−own_sold，0 删失，"
            "24 拍滚动）；放行=近 3 拍流和 ≤_RGP_GAP_MAX(2)=非出货缺口（其强拍"
            "之间）→放行追加，>2→让位。收口：4 处 MODELPX 追加（_u2_fire 全局"
            "重绑纯收紧）+4 处日新高追加（S928/S932/S939/S948 字面量）；窗未满/"
            "异常→基线放行；零跨拍挪量、只动追加放行时点"),
    },
    "slot": {
        "desc": "槽序匹配 v2（保序形态）：同拍我方 SELL 单对齐（保序）+抢先（越非卖单前置）",
        "subs": (), "tail": SLOT_TAIL, "entry": "_rgs_agent",
        "host": "_u2_agent",
        "mechanism": (
            "纯同拍重排（零改量/零加减单）：①对齐=SELL 相对序不动（基底计划序=对手"
            "稳态单序先验；扫查实测同拍同序 38/51，v1 碰撞项重排破序致负已删）；"
            "②抢先=自由 SELL（无同列表同品 BUY_*）越非卖单冒泡前置=我单插其单前"
            "（X1 并最早槽的对手自适应版；弱支配：早列竞速只赢不输+买单资金/仓容"
            "只更好）；③洗仓腿/同品组/SELL 相对序/非 SELL 相对序不动；无可改→原对象"),
    },
}


def substitute(base_src, subs, arm):
    src = base_src
    ledger = []
    for old, new, expect in subs:
        n = src.count(old)
        if n != expect:
            raise RuntimeError("校验①红 %s: 字面量计数 %d 应为 %d: %r"
                               % (arm, n, expect, old))
        src = src.replace(old, new)
        ledger.append({"old": old[:80], "new": new[:80], "count": n})
    back = src
    for old, new, cnt in reversed(subs):
        if back.count(new) != cnt:
            raise RuntimeError("校验②红 %s: 反替换计数漂移: %r" % (arm, new[:60]))
        back = back.replace(new, old)
    if back != base_src:
        raise RuntimeError("校验②红 %s: 反替换回程 != drop_half 源" % arm)
    return src, ledger


def _probe(arm, ns):
    """臂语义探针（合成观测/动作；引擎公式同源）。"""
    if arm == "gap":
        gap_ok, fire = ns["_rgp_gap_ok"], ns["_u2_fire"]
        obs = {"step": 200, "player": 0,
               "town": {"unlocked_shops": []},
               "market": {"prices": {}, "inventory": {}, "params": {}}}
        if gap_ok("MILK", 200, 0) is not True:
            raise RuntimeError("校验⑤红 gap: 窗未满应基线放行")
        ns["_RGP_FLOW"][0] = {"MILK": [5, 0, 0]}
        if gap_ok("MILK", 200, 0) is not False:
            raise RuntimeError("校验⑤红 gap: 近3拍高流应让位")
        ns["_RGP_FLOW"][0] = {"MILK": [0, 0, 1]}
        if gap_ok("MILK", 200, 0) is not True:
            raise RuntimeError("校验⑤红 gap: 缺口应放行")
        if fire(51.0, 51.0, "MILK", 200, 30000, 0.0, 10000, obs) is not False:
            raise RuntimeError("校验⑤红 gap: 非触发拍应零放行")
        ns["_RGP_FLOW"][0] = {"MILK": [5, 0, 0]}
        if fire(50.0, 51.0, "MILK", 200, 30000, 0.0, 10000, obs) is not False:
            raise RuntimeError("校验⑤红 gap: 强拍应让位")
        ns["_RGP_FLOW"][0] = {"MILK": [0, 0, 0]}
        if fire(50.0, 51.0, "MILK", 200, 30000, 0.0, 10000, obs) is not True:
            raise RuntimeError("校验⑤红 gap: 缺口触发拍应放行")
    else:
        slot = ns["_rgs_slot"]
        obs = {"step": 200, "player": 0, "town": {"unlocked_shops": []},
               "market": {"prices": {}, "inventory": {}}}
        act = {"market": [["HIRE"], ["SELL", "MILK", 2], ["SELL", "WHEAT", 3]]}
        out = slot(obs, act)["market"]
        if out[0] != ["SELL", "MILK", 2] or out[1] != ["SELL", "WHEAT", 3]:
            raise RuntimeError("校验⑤红 slot: 自由 SELL 应越非卖单前置且保序")
        if out[2] != ["HIRE"]:
            raise RuntimeError("校验⑤红 slot: 非卖单应后移")
        act2 = {"market": [["BUY_PRODUCT", "WHEAT", 5], ["SELL", "WHEAT", 5]]}
        if slot(obs, act2) is not act2:
            raise RuntimeError("校验⑤红 slot: 洗仓腿应原对象零改动")
        act3 = {"market": [["SELL", "MILK", 2], ["HIRE"], ["SELL", "WOOL", 1]]}
        out3 = slot(obs, act3)["market"]
        if [o[1] for o in out3 if o and o[0] == "SELL"] != ["MILK", "WOOL"]:
            raise RuntimeError("校验⑤红 slot: SELL 相对序（对齐保序）应保持")


def build_one(arm, cfg, base_bytes):
    base_src = base_bytes.decode("utf-8")
    sub_src, ledger = substitute(base_src, cfg["subs"], arm)
    injected = sub_src + cfg["tail"]
    try:
        compile(injected, "<racegap:%s>" % arm, "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 %s: 语法不通过: %r" % (arm, exc))
    ns = {}
    try:
        exec(compile(injected, "<racegap:%s>" % arm, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 %s: exec 失败: %r" % (arm, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != cfg["entry"]:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 %s: 末 callable=%r（应 %r）"
                           % (arm, got, cfg["entry"]))
    host = "_RGP_HOST" if arm == "gap" else "_RGS_HOST"
    if ns.get(host) is not ns.get("_u2_agent"):
        raise RuntimeError("校验④红 %s: 块首捕获非 _u2_agent" % arm)
    _probe(arm, ns)
    data = injected.encode("utf-8")
    out = OUT_DIR / arm / "main.py"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(str(out), arcname="main.py")
    tar_bytes = buf.getvalue()
    (out.parent / "submission.tar.gz").write_bytes(tar_bytes)
    man = {
        "schema": SCHEMA, "arm": arm, "desc": cfg["desc"],
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "entry": cfg["entry"], "host": cfg["host"],
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
        "subs": ledger, "tail_bytes": len(data) - len(base_bytes),
        "mechanism": cfg["mechanism"], "compile_ok": True,
        "entry_last_callable": cfg["entry"], "host_captured": cfg["host"],
        "roundtrip_identity_ok": True,
    }
    (out.parent / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return man


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（drop_half 字节漂移）：%s" % base_sha)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {"version": "racegap-build/1.0",
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "base_main": str(BASE_MAIN), "base_main_sha256": base_sha,
           "redline": "零跨拍挪量；只动挂单与追加", "arms": {}}
    for arm, cfg in ARMS.items():
        man = build_one(arm, cfg, base_bytes)
        out["arms"][arm] = {k: man[k] for k in
                            ("desc", "main_sha256", "tar_sha256", "subs",
                             "mechanism", "roundtrip_identity_ok")}
        print("built", arm, man["main_sha256"][:16], flush=True)
    (EVID_DIR / "build_racegap.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_racegap.json", flush=True)


if __name__ == "__main__":
    main()
