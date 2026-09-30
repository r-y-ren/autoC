# -*- coding: utf-8 -*-
"""build_s8（s8 尖拍捕获+申报修复 lab）：s_append 形态上加尖拍层（新建 lab；不改既有代码）。

S8 = s_append 构建件（orderbook_s1form_lab/build/s_append/main.py，sha 4608e9e0…，
零改动字节前缀）+ 尾块注入"尖拍捕获+申报修复"层：
  ①尖拍判定：本步某品 quote ≥ 尖价线——分品绝对线沿 D8（WOOL≥144 / MILK≥124 =
    尖价带下缘）；果麦（WHEAT/MELON）d22 窗 step∈[528,552) ≥ 当日 0.75 分位
    （含当拍样本、样本≥6 起判）；且该品非"本轮已满申报"（本拍申报量已达投射
    可卖上限则跳过）；
  ②尖拍补卖：尖价拍该品本拍无原生卖单→追加小单（lot 2-4、单≤4、量守恒于可卖
    上限内、槽位 10 帽内）至可卖库存上限（投射可卖−本拍已申报）——把漏拍值
    收回来；
  ③同拍申报修复：该品本拍有原生卖单→申报量补至可卖上限（只补申报、不改时点）；
  ④anti-幻影：本拍申报+追加总量 ≤ 投射可卖（真实可卖），绝不超卖（D8 败局
    幻影申报 +34~43 件教训）；
  ⑤守恒：同品累计成交可超原计划（加卖非挪卖，A 件日新高先例合法）；非触发拍
    零足迹（同对象返回）；异常回退原动作；step≥712（E182 终局规划器窗）零触碰。
产物 orderbook_s8spike_lab/build/s8/。只写 orderbook_s8spike_lab/（判决件另产）。
不改既有代码；不提交；不发射。
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
BASE_MAIN = (KSIM_DIR / "orderbook_s1form_lab" / "build" / "s_append"
             / "main.py")
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_s8spike_manifest/1.0"
BASE_SHA = ("4608e9e01e5741151a034d88e7ba594e64013f384365b15f356be5f47"
            "d88f17d")
ENTRY_NAME = "_s8_agent"
SEPARATOR = "\n\n"

# ==== S8 尾块（尖拍捕获+申报修复层） ====================================
TAIL = r'''

"""s8 尖拍捕获+申报修复实验尾块（S8=s_append 形态+尖拍层）。构建底=
orderbook_s1form_lab/build/s_append/main.py 零改动字节前缀；宿主=块首捕获之
末 callable（_sf_agent 谱系）。纯同拍后处理，零跨拍挪量；异常回退原动作。
语义：
- ①尖拍判定：本步某品 quote ≥ 尖价线（分品绝对线沿 D8：WOOL≥144/MILK≥124；
  果麦 WHEAT/MELON d22 窗 step∈[528,552) ≥ 当日 0.75 分位，样本≥6 起判），
  且该品非"本轮已满申报"（本拍申报已达投射可卖上限则跳过）；
- ②尖拍补卖：尖价拍该品本拍无原生卖单→追加小单（lot 2-4、单≤4、槽位 10 帽内）
  至可卖库存上限（投射可卖−本拍已申报）；
- ③同拍申报修复：该品本拍有原生卖单→申报量补至可卖上限（只补申报不改时点）；
- ④anti-幻影：本拍申报+追加总量 ≤ 投射可卖（真实可卖），绝不超卖；
- ⑤守恒：同品累计成交可超原计划（加卖非挪卖，A 件日新高先例合法）；非触发拍
  零足迹（同对象返回）；异常回退原动作；step≥712（E182 终局规划器窗）零触碰。
"""
_S8_HOST = [v for v in list(globals().values()) if callable(v)][-1]
_S8_ITEMS_ABS = {'WOOL': 144.0, 'MILK': 124.0}
_S8_FG_ITEMS = ('WHEAT', 'MELON')
_S8_FG_WIN = (528, 552)
_S8_FG_Q = 0.75
_S8_FG_MIN_N = 6
_S8_LOT_MIN, _S8_LOT_MAX = 2, 4
_S8_MAX_SLOTS = 10
_S8_STEP_CAP = 712
_S8_BUY_OPS = ('BUY_PRODUCT', 'BUY_SEED', 'BUY_ANIMAL')
_S8_PARAMS = dict(form='s8_spike/1.0', abs_lines=dict(_S8_ITEMS_ABS),
                  fg_items=_S8_FG_ITEMS, fg_window=_S8_FG_WIN,
                  fg_quantile=_S8_FG_Q, fg_min_samples=_S8_FG_MIN_N,
                  lot=(_S8_LOT_MIN, _S8_LOT_MAX), max_slots=_S8_MAX_SLOTS,
                  step_cap=_S8_STEP_CAP,
                  invariant='申报+追加总量≤投射可卖（anti-幻影）；同拍内加卖/'
                            '补申报，零跨拍挪量；非触发拍零足迹；异常回退')
_S8_REPORT = dict(calls=0, changed_turns=0, errors=0, spike_item_ticks=0,
                  abs_triggers=0, fg_triggers=0,
                  topup_orders=0, topup_qty=0, append_orders=0, append_qty=0,
                  skip_full_decl=0, skip_slot=0, step_cap_out=0,
                  lot_hist={}, per_item={})
_S8_PX = {'day': -1, 'hist': {}}


def _s8_reset():
    _S8_REPORT.update(calls=0, changed_turns=0, errors=0,
                      spike_item_ticks=0, abs_triggers=0, fg_triggers=0,
                      topup_orders=0, topup_qty=0, append_orders=0,
                      append_qty=0, skip_full_decl=0, skip_slot=0,
                      step_cap_out=0)
    _S8_REPORT['lot_hist'] = {}
    _S8_REPORT['per_item'] = {}
    _S8_PX['day'] = -1
    _S8_PX['hist'] = {}


def _s8_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _s8_lots(q):
    """q>0 → 小单拆发（确定性均分；单≤4；q=1 保留 1）。"""
    q = int(q)
    if q <= 0:
        return ()
    if q <= _S8_LOT_MAX:
        return (q,)
    n = (q + _S8_LOT_MAX - 1) // _S8_LOT_MAX
    base, rem = divmod(q, n)
    return tuple([base + 1] * rem + [base] * (n - rem))


def _s8_item(item):
    return _S8_REPORT['per_item'].setdefault(
        item, dict(spike=0, topup_qty=0, append_qty=0, append_orders=0))


def _s8_spikes(observation, step):
    """尖拍判定：绝对线（WOOL/MILK）+ 果麦 d22 窗当日 0.75 分位。"""
    try:
        prices = ((observation or {}).get('market') or {}).get('prices') or {}
    except Exception:
        prices = {}
    out = {}
    for item, line in _S8_ITEMS_ABS.items():
        try:
            q = float(prices.get(item))
        except (TypeError, ValueError):
            continue
        if q >= line:
            out[item] = ('abs', q, line)
    day = step // 24
    if _S8_PX['day'] != day:
        _S8_PX['day'] = day
        _S8_PX['hist'] = {}
    for item in _S8_FG_ITEMS:
        try:
            q = float(prices.get(item))
        except (TypeError, ValueError):
            continue
        hist = _S8_PX['hist'].setdefault(item, [])
        hist.append(q)
        if _S8_FG_WIN[0] <= step < _S8_FG_WIN[1] \
                and len(hist) >= _S8_FG_MIN_N:
            srt = sorted(hist)
            idx = -(-75 * len(srt) // 100) - 1      # ceil(0.75n)-1 最近秩
            if idx < 0:
                idx = 0
            line = srt[min(idx, len(srt) - 1)]
            if q >= line:
                out[item] = ('fg_q', q, line)
    return out


def _s8_apply(observation, action):
    _S8_REPORT['calls'] += 1
    try:
        if not isinstance(action, dict):
            return action
        step = int((observation or {}).get('step', 0))
        if step >= _S8_STEP_CAP:
            _S8_REPORT['step_cap_out'] += 1
            return action
        spikes = _s8_spikes(observation, step)
        if not spikes:
            return action                        # 非触发拍零足迹
        market = action.get('market')
        if not isinstance(market, list):
            return action
        avail = dict(_xd7_projected(observation, action))
        declared, native, unparsed = {}, {}, set()
        for idx, entry in enumerate(market):
            if not isinstance(entry, (list, tuple)) or len(entry) < 2:
                continue
            op = entry[0]
            if op in _S8_BUY_OPS:                # 同拍买腿入仓（decl_m 同序）
                q = _s8_qty(entry[2]) if len(entry) >= 3 else None
                if q is not None and q > 0:
                    avail[entry[1]] = int(avail.get(entry[1], 0)) + q
                continue
            if op != 'SELL' or len(entry) < 3:
                continue
            item = entry[1]
            q = _s8_qty(entry[2])
            if q is None:
                unparsed.add(item)
                continue
            if q > 0:
                declared[item] = int(declared.get(item, 0)) + q
                if item not in native:
                    native[item] = idx
        out = list(market)
        changed = False
        for item in list(spikes):
            if item in unparsed:
                continue                         # 不确定挂量：保守不动
            have = int(avail.get(item, 0))
            room = have - int(declared.get(item, 0))
            if room <= 0:
                _S8_REPORT['skip_full_decl'] += 1
                continue                         # 本轮已满申报
            _S8_REPORT['spike_item_ticks'] += 1
            row = _s8_item(item)
            row['spike'] += 1
            if spikes[item][0] == 'abs':
                _S8_REPORT['abs_triggers'] += 1
            else:
                _S8_REPORT['fg_triggers'] += 1
            if item in native:
                # ③同拍申报修复：只补申报不改时点（补至可卖上限）
                idx = native[item]
                ent = list(out[idx])
                old = _s8_qty(ent[2]) or 0
                ent[2] = int(old + room)
                out[idx] = ent
                _S8_REPORT['topup_orders'] += 1
                _S8_REPORT['topup_qty'] += room
                row['topup_qty'] += room
                changed = True
                continue
            # ②尖拍补卖：追加小单（lot 2-4）至可卖上限（anti-幻影 ≤room）
            posted = 0
            for lot in _s8_lots(room):
                if len(out) >= _S8_MAX_SLOTS:
                    _S8_REPORT['skip_slot'] += 1
                    break
                out.append(['SELL', item, int(lot)])
                posted += lot
                _S8_REPORT['append_orders'] += 1
                row['append_orders'] += 1
                key = str(int(lot))
                _S8_REPORT['lot_hist'][key] = \
                    _S8_REPORT['lot_hist'].get(key, 0) + 1
            if posted:
                _S8_REPORT['append_qty'] += posted
                row['append_qty'] += posted
                changed = True
        if not changed:
            return action                        # 同对象零足迹
        _S8_REPORT['changed_turns'] += 1
        return dict(action, market=out)
    except Exception:
        _S8_REPORT['errors'] += 1
        return action                            # 异常回退（同对象零足迹）


def _s8_agent(observation, configuration=None):
    """s8 尖拍捕获入口（官方 last-callable）：宿主动作→尖拍层后处理。"""
    if int((observation or {}).get('step', 0)) == 0:
        _s8_reset()
    try:
        action = _S8_HOST(observation, configuration)
    except TypeError:
        action = _S8_HOST(observation)
    return _s8_apply(observation, action)


_s8_agent.telemetry = _S8_REPORT
kaggle_submission_agent = _s8_agent
'''


def build_s8():
    out_dir = MODULE_DIR / "build" / "s8"
    out_dir.mkdir(parents=True, exist_ok=True)
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA:
        raise RuntimeError("校验⓪红：基底 sha %s ≠ 预期 %s" % (base_sha, BASE_SHA))
    built = base_bytes.decode("utf-8") + SEPARATOR + TAIL
    checks = {}
    compile(built, "s8_main.py", "exec")                # ①compile
    checks["compile_ok"] = True
    ns = {}
    exec(compile(built, "s8_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == ENTRY_NAME)
    if not checks["last_callable_is_entry"]:
        raise RuntimeError("校验②红：末 callable 不是 %s" % ENTRY_NAME)
    out_bytes = built.encode("utf-8")
    checks["base_prefix_identity_ok"] = out_bytes[:len(base_bytes)] == base_bytes
    checks["roundtrip_strip_identity_ok"] = (
        out_bytes[len(base_bytes):] == (SEPARATOR + TAIL).encode("utf-8"))
    checks["host_capture_is_sf_agent"] = (
        ns.get("_S8_HOST") is ns.get("_sf_agent"))
    checks["params_ok"] = (ns.get("_S8_PARAMS", {}).get("abs_lines")
                           == {"WOOL": 144.0, "MILK": 124.0})
    if not all(checks.values()):
        raise RuntimeError("校验③红: %s" % checks)
    main_path = out_dir / "main.py"
    main_path.write_bytes(out_bytes)
    main_sha = hashlib.sha256(out_bytes).hexdigest()
    with tarfile.open(out_dir / "submission.tar.gz", "w:gz") as tf:
        data = out_bytes
        info = tarfile.TarInfo("main.py")
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
    manifest = {
        "schema": SCHEMA,
        "form": "s8",
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base": {"path": str(BASE_MAIN), "sha256": base_sha,
                 "bytes": len(base_bytes)},
        "main": {"path": str(main_path), "sha256": main_sha,
                 "bytes": len(out_bytes)},
        "entry": ENTRY_NAME,
        "host_entry": "_sf_agent",
        "semantics": {
            "spike_detect": "①尖拍判定：绝对线 WOOL≥144/MILK≥124（D8 尖价带"
                            "下缘）；果麦 WHEAT/MELON d22 窗 [528,552) ≥ 当日 "
                            "0.75 分位（ceil 秩、样本≥6 起判、含当拍）；且该品"
                            "非本轮已满申报",
            "spike_append": "②尖拍补卖：无原生卖单→追加小单 lot 2-4 至可卖库存"
                            "上限（投射可卖−本拍已申报），槽位 10 帽内",
            "decl_topup": "③同拍申报修复：有原生卖单→申报量补至可卖上限（只补"
                          "申报不改时点）",
            "anti_phantom": "④本拍申报+追加总量 ≤ 投射可卖（真实可卖），绝不"
                            "超卖（D8 幻影申报教训）",
            "conservation": "⑤同品累计成交可超原计划（加卖非挪卖，A 件日新高"
                            "先例合法）；非触发拍零足迹；异常回退；step≥712 零"
                            "触碰（E182 窗）",
        },
        "checks": checks,
        "commands": ["python3 orderbook_s8spike_lab/build_s8.py",
                     "python3 orderbook_s8spike_lab/judge_s8.py"],
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    m = build_s8()
    (EVID_DIR / "build_s8.json").write_text(
        json.dumps({"s8": {"sha256": m["main"]["sha256"],
                           "checks": m["checks"]}},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("BUILD s8", m["main"]["sha256"][:16], m["checks"], flush=True)
    print("BUILD OK %.1fs" % (time.perf_counter() - t0))
    return m


if __name__ == "__main__":
    main()
