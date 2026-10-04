# -*- coding: utf-8 -*-
"""build_s_form（s1 卖面结构重写 lab）：C_final 卖面 → 顶强卖面形态（新建 lab；不改既有代码）。

S_form = C_final（sha a37c0d34…，零改动字节前缀）+ 尾块注入卖面重写层，两形态：
  s_split（主形态·同拍拆发）：
    ①小单清仓流：SELL 单量形态 3/6/10 帽位 → 逐单 2-4 拆发（同拍内拆分[同拍
      拆并语义·X1 量守恒同族]，跨拍不拆=R23/R26 红线；槽位 10 帽内拆发、超帽
      合并尾部保总量，绝不挪拍）；
    ②申报背书：申报量=min(申报,投射可卖)（decl_m 同序口径；钱面中立实证；
      全清率 0.72-0.94 顶强形=副产品）；
    ③d12-24 平台投放：MSW×12..22 时（C_final 焦窗窗权沿用）每拍小量放行
      （非脉冲、不等价峰），追加单量 ≤4/单、可多单（≤2 单/品/拍）；
    ④d29 终局分抛（D6 节奏点）：step 696-711 每拍小单分抛（追加 ≤4/单、可多
      单、全品）——现行攒量（S758 族 696 后止火+718 整仓清算）改逐拍小单；
    ⑤d0 开局粒度（D6 节奏点）：开局买单拆小单（量守恒、HIRE/BUY_LAND 原子
      单不动）——"BUY5 d0 4-10 单"粒度口径；
  s_append（R26 线回退形态·多拍小单追加）：②③④⑤ 同，①改"追加承载"——
    SELL 原单不拆（追加单量 ≤4/单、可多单 承载 lot 2-4 形态）。
保守不变量：净卖总量恒等（同品累计卖出量与基线一致——同拍拆发量守恒+追加只挂
投射可卖余量+终局清算兜底；只改单量形态与频次，零跨拍挪量）；磁带 blob 零触碰；
异常回退原动作（同对象零足迹）。

产物 orderbook_s1form_lab/build/{s_split,s_append}/。只写 orderbook_s1form_lab/
与 fn_docs/hybrid/results/2026-09-30-s1-sellform.json（判决件另产）。不提交；不发射。
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
BASE_MAIN = (KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final"
             / "main.py")
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_s1form_manifest/1.0"
BASE_SHA = ("a37c0d3487fe1d2152ec6c0b767b36afc21ad18207accb2d3cf1f1b0"
            "77016a92")
ENTRY_NAME = "_sf_agent"
SEPARATOR = "\n\n"
MODE_TOKEN = "__SF_MODE__"
FORMS = {"s_split": 0, "s_append": 1}

# ==== S_form 尾块（卖面结构重写层；两形态共用，__SF_MODE__ 注入） ==========
TAIL = r'''

"""s1 卖面结构重写实验尾块（S_form：顶强卖面形态=lot 2-4 小单粒度 + 申报背书
+ d12-24 平台投放 + d29 终局分抛 + d0 开局粒度）。构建底=c_final 零改动字节
前缀；宿主=块首捕获之末 callable（_hs_agent 谱系）。
语义（__SF_MODE__：0=s_split 同拍拆发主形态 / 1=s_append 多拍小单追加回退形态）：
- ①小单粒度：mode0=本步 SELL 单 qty→逐单 2-4 lot 同拍拆发（量守恒；槽位 10
  帽内拆发、超帽合并尾部保总量；跨拍不拆=R23/R26 红线）；mode1=原单不拆，
  lot 2-4 形态由追加单承载（追加单量 ≤4/单、可多单）；
- ②申报背书：qty=min(申报,投射可卖)（decl_m 同序口径：_xd7_projected 起底
  +同拍更早 BUY_PRODUCT/BUY_ANIMAL 入仓腿，逐单顺序扣减；裁 0 留占槽）；
- ③d12-24 平台：step∈[288,600) ∧ (step%24)∈12..22 ∧ MSW 品组，每拍小量放行
  （非脉冲、不等价峰），追加 ≤4/单、≤2 单/品/拍，只挂投射可卖余量；
- ④d29 终局分抛：step∈[696,712) 全品每拍小单分抛（追加 ≤4/单、≤2 单/品/拍）
  ——现行攒量（S758 族 696 止火、718 整仓清算）改逐拍小单（D6 38-45 张口径）；
- ⑤d0 开局粒度：step<24 非原子买单（BUY_PRODUCT/BUY_SEED/BUY_ANIMAL）拆
  ≤4 单位小单（量守恒；HIRE/BUY_LAND 原子单不动）；
- 保守不变量：净卖总量恒等（拆发量守恒+追加只挂投射可卖余量+终局清算兜底）；
  磁带 blob 零触碰；异常回退原动作（同对象零足迹）。
"""
_SF_HOST = [v for v in list(globals().values()) if callable(v)][-1]
_SF_MODE = __SF_MODE__
_SF_ITEMS = ('MILK', 'STRAWBERRY', 'WOOL')
_SF_WIN = (288, 600)
_SF_HOURS = tuple(range(12, 23))
_SF_LOT_MIN, _SF_LOT_MAX = 2, 4
_SF_MAX_SLOTS = 10
_SF_PLAT_MAX_ORDERS = 2
_SF_BUY_OPS = ('BUY_PRODUCT', 'BUY_SEED', 'BUY_ANIMAL')
_SF_PARAMS = dict(form='s1_sellform/1.0', mode=_SF_MODE, lot=(2, 4),
                  win=_SF_WIN, hours=_SF_HOURS, items=_SF_ITEMS,
                  d29=(696, 712), d0=24,
                  plat_max_orders_per_item=_SF_PLAT_MAX_ORDERS)
_SF_REPORT = dict(calls=0, changed_turns=0, errors=0,
                  decl_orders=0, decl_qty=0, zero_kept=0, unparsed_kept=0,
                  split_orders=0, split_lots=0, split_qty=0,
                  slot_merge_orders=0, slot_merge_qty=0,
                  plat_orders=0, plat_qty=0, plat_skipped_slot=0,
                  d29_orders=0, d29_qty=0, d0_buy_orders=0, d0_buy_qty=0,
                  lot_hist={}, per_item={})


def _sf_reset():
    _SF_REPORT.update(calls=0, changed_turns=0, errors=0,
                      decl_orders=0, decl_qty=0, zero_kept=0, unparsed_kept=0,
                      split_orders=0, split_lots=0, split_qty=0,
                      slot_merge_orders=0, slot_merge_qty=0,
                      plat_orders=0, plat_qty=0, plat_skipped_slot=0,
                      d29_orders=0, d29_qty=0, d0_buy_orders=0, d0_buy_qty=0)
    _SF_REPORT['lot_hist'] = {}
    _SF_REPORT['per_item'] = {}


def _sf_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（不确定，保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _sf_lots(q, lo=None, hi=None):
    """q>0 → 小单拆发（确定性均分；q=1 保留 1）。"""
    q = int(q)
    lo = _SF_LOT_MIN if lo is None else lo
    hi = _SF_LOT_MAX if hi is None else hi
    if q <= 0:
        return ()
    if q <= hi:
        return (q,)
    n = (q + hi - 1) // hi
    base, rem = divmod(q, n)
    return tuple([base + 1] * rem + [base] * (n - rem))


def _sf_item_row(item):
    return _SF_REPORT['per_item'].setdefault(item, dict(
        decl_qty=0, split_qty=0, split_lots=0, plat_qty=0, d29_qty=0,
        posted=0))


def _sf_lot_hist(q):
    h = _SF_REPORT['lot_hist']
    key = str(int(q)) if float(q).is_integer() else str(q)
    h[key] = h.get(key, 0) + 1


def _sf_append(out, item, qty, kind):
    """追加小单（≤4/单、可多单）；kind∈{plat,d29} 记台账。"""
    posted = 0
    spare = int(qty)
    for _ in range(_SF_PLAT_MAX_ORDERS):
        if len(out) >= _SF_MAX_SLOTS:
            if spare >= _SF_LOT_MIN:
                _SF_REPORT['plat_skipped_slot'] += 1
            break
        lot = spare if spare <= _SF_LOT_MAX else _SF_LOT_MAX
        if lot <= 0 or (lot < _SF_LOT_MIN and spare != 1):
            break
        out.append(['SELL', item, int(lot)])
        spare -= lot
        posted += lot
    if posted:
        if kind == 'd29':
            _SF_REPORT['d29_orders'] += 1
            _SF_REPORT['d29_qty'] += posted
            _sf_item_row(item)['d29_qty'] += posted
        else:
            _SF_REPORT['plat_orders'] += 1
            _SF_REPORT['plat_qty'] += posted
            _sf_item_row(item)['plat_qty'] += posted
    return posted


def _sf_apply(observation, action):
    _SF_REPORT['calls'] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get('market')
        if not isinstance(market, list) or not market:
            return action
        step = int((observation or {}).get('step', 0))
        avail = dict(_xd7_projected(observation, action))
        do_split = (_SF_MODE == 0)
        d0_grain = step < 24
        groups = []
        for entry in market:
            is_sell = (isinstance(entry, (list, tuple)) and len(entry) >= 3
                       and entry[0] == 'SELL')
            if not is_sell:
                op = entry[0] if isinstance(entry, (list, tuple)) and \
                    len(entry) >= 2 else None
                if op in _SF_BUY_OPS:
                    q = _sf_qty(entry[2]) if len(entry) >= 3 else None
                    if q is not None and q > 0:
                        avail[entry[1]] = avail.get(entry[1], 0) + q
                        # ⑤d0 开局粒度：非原子买单拆 ≤4 小单（量守恒）
                        if d0_grain and q > _SF_LOT_MAX:
                            lots = _sf_lots(q)
                            groups.append([[op, entry[1], int(l)]
                                           for l in lots])
                            _SF_REPORT['d0_buy_orders'] += 1
                            _SF_REPORT['d0_buy_qty'] += q
                            continue
                groups.append([entry])
                continue
            item = entry[1]
            qty = _sf_qty(entry[2])
            if qty is None:
                _SF_REPORT['unparsed_kept'] += 1
                groups.append([entry])
                continue
            q0 = qty if qty > 0 else 0
            have = int(avail.get(item, 0))
            q = q0 if q0 <= have else have          # ②申报背书（decl_m 同序）
            if q < q0:
                _SF_REPORT['decl_orders'] += 1
                _SF_REPORT['decl_qty'] += q0 - q
                _sf_item_row(item)['decl_qty'] += q0 - q
            avail[item] = have - q
            if q <= 0:
                _SF_REPORT['zero_kept'] += 1
                groups.append([['SELL', item, 0]])  # 裁 0 留占槽（decl 口径）
                continue
            if do_split:
                lots = _sf_lots(q)
                groups.append([['SELL', item, int(l)] for l in lots])
            else:
                groups.append([['SELL', item, int(q)]])
        # 槽位预算（10）：每条目先保 1 槽，组内尽量拆发；超帽合并尾部（量守恒）
        out = []
        remaining = len(groups)
        budget = _SF_MAX_SLOTS
        for group in groups:
            remaining -= 1
            allowed = budget - remaining
            if allowed < 1:
                allowed = 1
            k = len(group)
            if k == 1:
                out.extend(group)
                budget -= 1
                continue
            if allowed >= k:
                out.extend(group)
                budget -= k
                if group and group[0][0] == 'SELL':
                    _SF_REPORT['split_orders'] += 1
                    _SF_REPORT['split_lots'] += k - 1
                    _SF_REPORT['split_qty'] += sum(l[2] for l in group)
                    row = _sf_item_row(group[0][1])
                    row['split_qty'] += sum(l[2] for l in group)
                    row['split_lots'] += k
            else:
                if allowed <= 1:
                    merged = [[group[0][0], group[0][1],
                               int(sum(l[2] for l in group))]]
                else:
                    head = group[:allowed - 1]
                    tail_qty = sum(l[2] for l in group[allowed - 1:])
                    merged = head + [[group[0][0], group[0][1],
                                      int(tail_qty)]]
                out.extend(merged)
                budget -= len(merged)
                _SF_REPORT['slot_merge_orders'] += 1
                _SF_REPORT['slot_merge_qty'] += sum(l[2] for l in merged)
        # ③d12-24 平台 + ④d29 终局分抛（每拍小量 vs 现行攒量；追加 ≤4/单）
        if _SF_WIN[0] <= step < _SF_WIN[1] and (step % 24) in _SF_HOURS:
            for item in _SF_ITEMS:
                _sf_append(out, item, int(avail.get(item, 0)), 'plat')
        elif 696 <= step < 712:
            for item in list(PRODUCTS):
                _sf_append(out, item, int(avail.get(item, 0)), 'd29')
        for o in out:
            if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == 'SELL':
                q = _sf_qty(o[2])
                if q is not None and q > 0:
                    _sf_item_row(o[1])['posted'] += q
                    _sf_lot_hist(q)
        changed = len(out) != len(market) or any(
            a != b for a, b in zip(market, out))
        if not changed:
            return action                       # 同对象零足迹
        _SF_REPORT['changed_turns'] += 1
        return dict(action, market=out)
    except Exception:
        _SF_REPORT['errors'] += 1
        return action                           # 异常回退（同对象零足迹）


def _sf_agent(observation, configuration=None):
    """s1 卖面重写入口（官方 last-callable）：宿主动作→卖面形态后处理。"""
    if int((observation or {}).get('step', 0)) == 0:
        _sf_reset()
    try:
        action = _SF_HOST(observation, configuration)
    except TypeError:
        action = _SF_HOST(observation)
    return _sf_apply(observation, action)


_sf_agent.telemetry = _SF_REPORT
kaggle_submission_agent = _sf_agent
'''


def build_form(form: str, mode: int):
    out_dir = MODULE_DIR / "build" / form
    out_dir.mkdir(parents=True, exist_ok=True)
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA:
        raise RuntimeError("校验⓪红：基底 sha %s ≠ 预期 %s" % (base_sha, BASE_SHA))
    tail = TAIL.replace(MODE_TOKEN, str(int(mode)))
    built = base_bytes.decode("utf-8") + SEPARATOR + tail
    checks = {}
    compile(built, form + "_main.py", "exec")            # ①compile
    checks["compile_ok"] = True
    ns = {}
    exec(compile(built, form + "_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == ENTRY_NAME)
    if not checks["last_callable_is_entry"]:
        raise RuntimeError("校验②红 %s：末 callable 不是 %s" % (form, ENTRY_NAME))
    out_bytes = built.encode("utf-8")
    checks["base_prefix_identity_ok"] = out_bytes[:len(base_bytes)] == base_bytes
    checks["roundtrip_strip_identity_ok"] = (
        out_bytes[len(base_bytes):] == (SEPARATOR + tail).encode("utf-8"))
    checks["host_capture_is_hs_agent"] = (
        ns.get("_SF_HOST") is ns.get("_hs_agent"))
    checks["mode_ok"] = int(ns.get("_SF_MODE", -1)) == int(mode)
    if not all(checks.values()):
        raise RuntimeError("校验③红 %s: %s" % (form, checks))
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
        "form": form,
        "mode": int(mode),
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base": {"path": str(BASE_MAIN), "sha256": base_sha,
                 "bytes": len(base_bytes)},
        "main": {"path": str(main_path), "sha256": main_sha,
                 "bytes": len(out_bytes)},
        "entry": ENTRY_NAME,
        "host_entry": "_hs_agent",
        "semantics": {
            "small_lot": ("①SELL 单量 2-4 档：mode0=同拍拆发（量守恒、槽位 10 帽内、"
                          "跨拍不拆）；mode1=原单不拆、lot 形态由追加单承载"
                          "（追加 ≤4/单、可多单）"),
            "decl": "②申报量=min(申报,投射可卖)（decl_m 同序；裁 0 留占槽）",
            "platform": "③d12-24（288-599）× 12..22 时 MSW 每拍小量（≤4/单、"
                        "≤2 单/品/拍、不等价峰、非脉冲）",
            "d29_clearance": "④step 696-711 全品每拍小单分抛（≤4/单、≤2 单/品/"
                             "拍）——现行攒量（696 止火/718 整仓）改逐拍小单",
            "d0_grain": "⑤step<24 非原子买单拆 ≤4 小单（量守恒；HIRE/BUY_LAND "
                        "原子单不动）",
            "invariant": "净卖总量恒等（拆发量守恒+追加只挂投射可卖余量+终局清算"
                         "兜底；同拍内形态变化，零跨拍挪量）；异常回退原动作",
        },
        "checks": checks,
        "commands": ["python3 orderbook_s1form_lab/build_s_form.py",
                     "python3 orderbook_s1form_lab/judge_s_form.py"],
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for form, mode in FORMS.items():
        m = build_form(form, mode)
        out[form] = {"sha256": m["main"]["sha256"], "mode": mode,
                     "checks": m["checks"]}
        print("BUILD", form, m["main"]["sha256"][:16], m["checks"], flush=True)
    (EVID_DIR / "build_all.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("BUILD OK %.1fs" % (time.perf_counter() - t0))
    return out


if __name__ == "__main__":
    main()
