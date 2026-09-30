# -*- coding: utf-8 -*-
"""build_s9（s9 同族提胜精修 lab）：s8 形态上加尖拍拍面精修层（新建 lab；不改既有代码）。

S9 = s8 构建件（orderbook_s8spike_lab/build/s8/main.py，sha a59208fe…，零改动
字节前缀）+ 尾块注入"拍面精修"层（两形态）：
  s9a（③day-high 门）：法证①定位翻负类=③同拍申报修复在"平台拍"补量（挪卖无增益
    ：WOOL 199@当日峰 218 / 221@峰 227，先进 8 件净 −6），S9 撤销非当日新高拍的
    ③补量（还原宿主申报量）；真尖拍（当日新高）补量保留（674355 d23 WOOL@199→
    +787 属此类）。②追加单不动（分品毛增益 WHEAT +92~+338 为实）。
  s9b（s9a+追加量精修）：再加 ①实存量帽——追加/补量总量 ≤ 实存（观测 shed+单位
    仓+同拍买腿−本拍原生申报），消 no_stock 幻影单（法证实测 10/40 追加单空跑）；
    ②果麦单拍追加帽 ≤8 件（tetsutani 单拍 15 件大dump 类）。
语义边界：纯同拍后处理、零跨拍挪量（R23/R26 红线）；只做"撤销尖拍层自身加量/
裁量"，不改宿主动作；异常回退原动作；step≥712 零触碰。
产物 orderbook_s9fam_lab/build/{s9a,s9b}/。只写 orderbook_s9fam_lab/。
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
BASE_MAIN = (KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py")
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_s9fam_manifest/1.0"
BASE_SHA = ("a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae"
            "04e7c0a6")
ENTRY_NAME = "_s9_agent"
SEPARATOR = "\n\n"


def make_tail(cap_mode):
    """S9 尾块（cap_mode: 'off'=s9a / 'on'=s9b）。"""
    return r'''

"""s9 尖拍拍面精修实验尾块（S9=s8 形态+拍面精修层）。构建底=
orderbook_s8spike_lab/build/s8/main.py 零改动字节前缀；宿主=块首捕获之末
callable（_s8_agent 谱系）。纯同拍后处理，零跨拍挪量；只撤销/裁剪尖拍层自身
加量，不改宿主动作；异常回退原动作。
语义：
- ③day-high 门：同拍申报修复（topup）仅在当日新高拍保留（q>当日 running max）；
  平台拍补量=挪卖无增益（法证：WOOL 199@峰 218/221@峰 227 先进 8 件净 −6）→
  还原宿主申报量；真尖拍补量保留（d23 WOOL@199、d12 WOOL@231 类）；
- ②追加单量修（s9b）：实存量帽=追加/补量总量 ≤ 观测 shed+单位仓+同拍买腿−
  本拍原生申报（消 no_stock 幻影空跑）；果麦（WHEAT/MELON）单拍追加帽 ≤8 件；
- 非触发拍零足迹（同对象返回）；异常回退；step≥712（E182 窗）零触碰。
"""
_S9_HOST = [v for v in list(globals().values()) if callable(v)][-1]
_S8_APPLY_REAL = _s8_apply
_S9_CAP_MODE = __CAP_MODE__
_S9_FG_ITEMS = ('WHEAT', 'MELON')
_S9_FG_TICK_CAP = 8
_S9_MARK = {'h': None, 'o': None}
_S9_PX = {'day': -1, 'hi': {}}
_S9_PARAMS = dict(form='s9_family_refine/1.0', cap_mode=_S9_CAP_MODE,
                  topup_gate='day-high（q>当日 running max，含当拍）',
                  stock_cap=('实存量帽：shed+Σ单位仓+同拍买腿−原生申报'
                             if _S9_CAP_MODE == 'on' else 'off'),
                  fg_tick_cap=(_S9_FG_TICK_CAP
                               if _S9_CAP_MODE == 'on' else 'off'),
                  invariant='纯同拍后处理；零跨拍挪量；只撤销/裁剪尖拍层加量；'
                            '异常回退；step≥712 零触碰')
_S9_REPORT = dict(calls=0, changed_turns=0, errors=0, step_cap_out=0,
                  noop=0, topup_veto=0, topup_keep=0, append_keep_orders=0,
                  append_drop_orders=0, append_drop_qty=0, fg_cap_trim=0,
                  stock_cap_trim=0)


def _s9_reset():
    _S9_REPORT.update(calls=0, changed_turns=0, errors=0, step_cap_out=0,
                      noop=0, topup_veto=0, topup_keep=0,
                      append_keep_orders=0, append_drop_orders=0,
                      append_drop_qty=0, fg_cap_trim=0, stock_cap_trim=0)
    _S9_PX['day'] = -1
    _S9_PX['hi'] = {}
    _S9_MARK['h'] = None
    _S9_MARK['o'] = None


def _s9_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _s9_spy(observation, action):
    """包 _s8_apply：捕获宿主动作与尖拍层输出（diff 依据）。"""
    hm = None
    try:
        if isinstance(action, dict):
            hm = [list(e) if isinstance(e, (list, tuple)) else e
                  for e in (action.get('market') or [])]
    except Exception:
        hm = None
    out = _S8_APPLY_REAL(observation, action)
    try:
        _S9_MARK['h'] = hm
        _S9_MARK['o'] = [list(e) if isinstance(e, (list, tuple)) else e
                         for e in (out.get('market') or [])] \
            if isinstance(out, dict) else None
    except Exception:
        _S9_MARK['h'] = None
        _S9_MARK['o'] = None
    return out


_s8_apply = _s9_spy        # 宿主谱系内 _s8_agent 的同名查找→间谍


def _s9_apply(observation, action):
    _S9_REPORT['calls'] += 1
    try:
        step = int((observation or {}).get('step', 0))
        mkt = (observation or {}).get('market')
        prices = (mkt or {}).get('prices') or {} if isinstance(mkt, dict) \
            else {}
        day = step // 24
        if _S9_PX['day'] != day:
            _S9_PX['day'] = day
            _S9_PX['hi'] = {}
        is_high = {}
        for item, raw in prices.items():
            try:
                q = float(raw)
            except (TypeError, ValueError):
                continue
            hi = _S9_PX['hi'].get(item)
            is_high[item] = hi is None or q > hi
            if hi is None or q > hi:
                _S9_PX['hi'][item] = q
        if step >= _S8_STEP_CAP:
            _S9_REPORT['step_cap_out'] += 1
            return action
        hm, om = _S9_MARK.get('h'), _S9_MARK.get('o')
        if hm is None or om is None or hm == om:
            _S9_REPORT['noop'] += 1
            return action
        market = action.get('market')
        if not isinstance(market, list):
            _S9_REPORT['noop'] += 1
            return action
        n = len(hm)
        out = [list(e) if isinstance(e, (list, tuple)) else e for e in om]
        changed = False
        # ---- ③day-high 门：非当日新高拍 topup 还原宿主申报量 ----
        for i in range(min(n, len(om))):
            if om[i] == hm[i]:
                continue
            b, a = hm[i], om[i]
            if not (isinstance(b, (list, tuple)) and isinstance(a, (list, tuple))
                    and len(b) >= 3 and len(a) >= 3 and b[0] == 'SELL'
                    and a[0] == 'SELL' and b[1] == a[1]):
                continue
            item = str(a[1])
            if is_high.get(item):
                _S9_REPORT['topup_keep'] += 1
                continue
            out[i] = list(b)          # ③撤销：还原宿主申报量
            _S9_REPORT['topup_veto'] += 1
            changed = True
        # ---- ②追加单（尾部多出的 SELL 条目）----
        appends = []
        for j in range(n, len(om)):
            e = om[j]
            if isinstance(e, (list, tuple)) and len(e) >= 3 and e[0] == 'SELL':
                q = _s9_qty(e[2])
                if q is not None and q > 0:
                    appends.append((j, str(e[1]), int(q)))
        drop = set()
        if _S9_CAP_MODE == 'on':
            # 果麦单拍追加帽（从尾部裁）
            fg_used = {}
            for j, item, q in appends:
                if item in _S9_FG_ITEMS:
                    used = fg_used.get(item, 0)
                    if used + q > _S9_FG_TICK_CAP:
                        keep = max(0, _S9_FG_TICK_CAP - used)
                        if keep <= 0:
                            drop.add(j)
                            _S9_REPORT['fg_cap_trim'] += 1
                            _S9_REPORT['append_drop_qty'] += q
                        else:
                            out[j] = ['SELL', item, keep]
                            _S9_REPORT['fg_cap_trim'] += 1
                            _S9_REPORT['append_drop_qty'] += (q - keep)
                            fg_used[item] = used + keep
                            continue
                    fg_used[item] = used + q
            # 实存量帽：尖拍层加量总量 ≤ 实存（shed+单位仓+买腿−原生申报）
            added, native_decl, buys = {}, {}, {}
            for e in hm:
                if not isinstance(e, (list, tuple)) or len(e) < 3:
                    continue
                if e[0] == 'SELL':
                    q = _s9_qty(e[2])
                    if q is not None and q > 0:
                        native_decl[str(e[1])] = native_decl.get(
                            str(e[1]), 0) + int(q)
                elif e[0] in ('BUY_PRODUCT', 'BUY_ANIMAL'):
                    q = _s9_qty(e[2])
                    if q is not None and q > 0:
                        buys[str(e[1])] = buys.get(str(e[1]), 0) + int(q)
            for i in range(min(n, len(om))):
                if om[i] == hm[i]:
                    continue
                b, a = hm[i], om[i]
                if isinstance(b, (list, tuple)) and isinstance(a, (list, tuple)) \
                        and len(b) >= 3 and len(a) >= 3 and b[0] == 'SELL' \
                        and a[0] == 'SELL' and b[1] == a[1]:
                    bq, aq = _s9_qty(b[2]), _s9_qty(a[2])
                    if bq is not None and aq is not None and aq > bq:
                        it = str(a[1])
                        added[it] = added.get(it, 0) + int(aq - bq)
            for j, item, q in appends:
                if j not in drop:
                    added[item] = added.get(item, 0) + q
            try:
                priv = (observation or {}).get('private') or {}
                shed = priv.get('shed') or {}
                invs = priv.get('inventories') or []
            except Exception:
                shed, invs = {}, []
            for item, add in list(added.items()):
                if add <= 0:
                    continue
                try:
                    real = int(shed.get(item, 0))
                except Exception:
                    real = 0
                unit = 0
                try:
                    for u in invs:
                        if isinstance(u, dict):
                            unit += int(u.get(item, 0) or 0)
                except Exception:
                    unit = 0
                room_real = max(0, real + unit + buys.get(item, 0)
                                - native_decl.get(item, 0))
                over = add - room_real
                if over <= 0:
                    continue
                for j, it2, q in reversed(appends):
                    if it2 != item or j in drop or over <= 0:
                        continue
                    e = out[j]
                    cur = _s9_qty(e[2]) if isinstance(e, (list, tuple)) \
                        and len(e) >= 3 else None
                    if not cur or cur <= 0:
                        continue
                    if cur <= over:
                        drop.add(j)
                        over -= cur
                        _S9_REPORT['stock_cap_trim'] += 1
                        _S9_REPORT['append_drop_qty'] += cur
                    else:
                        out[j] = ['SELL', item, cur - over]
                        _S9_REPORT['stock_cap_trim'] += 1
                        _S9_REPORT['append_drop_qty'] += over
                        over = 0
        final = []
        for j in range(len(out)):
            if j >= n and j in drop:
                _S9_REPORT['append_drop_orders'] += 1
                continue
            final.append(out[j])
        kept = sum(1 for j, _it, _q in appends if j not in drop)
        _S9_REPORT['append_keep_orders'] += kept
        if not changed and kept == len(appends):
            _S9_REPORT['noop'] += 1
            return action                 # 同对象零足迹
        _S9_REPORT['changed_turns'] += 1
        return dict(action, market=final)
    except Exception:
        _S9_REPORT['errors'] += 1
        return action                     # 异常回退（同对象零足迹）


def _s9_agent(observation, configuration=None):
    """s9 拍面精修入口（官方 last-callable）：宿主→尖拍层→精修后处理。"""
    if int((observation or {}).get('step', 0)) == 0:
        _s9_reset()
    try:
        action = _S9_HOST(observation, configuration)
    except TypeError:
        action = _S9_HOST(observation)
    return _s9_apply(observation, action)


_s9_agent.telemetry = _S9_REPORT
kaggle_submission_agent = _s9_agent
'''.replace('__CAP_MODE__', repr(cap_mode))


def build_s9(form, cap_mode):
    out_dir = MODULE_DIR / "build" / form
    out_dir.mkdir(parents=True, exist_ok=True)
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA:
        raise RuntimeError("校验⓪红：基底 sha %s ≠ 预期 %s" % (base_sha, BASE_SHA))
    tail = make_tail(cap_mode)
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
        raise RuntimeError("校验②红：末 callable 不是 %s" % ENTRY_NAME)
    out_bytes = built.encode("utf-8")
    checks["base_prefix_identity_ok"] = out_bytes[:len(base_bytes)] == base_bytes
    checks["roundtrip_strip_identity_ok"] = (
        out_bytes[len(base_bytes):] == (SEPARATOR + tail).encode("utf-8"))
    checks["host_capture_is_s8_agent"] = (
        ns.get("_S9_HOST") is ns.get("_s8_agent"))
    checks["spy_rebind_ok"] = (
        ns.get("_s8_apply") is not ns.get("_S8_APPLY_REAL")
        and getattr(ns.get("_s8_apply"), "__name__", "") == "_s9_spy")
    checks["params_ok"] = (
        ns.get("_S9_PARAMS", {}).get("cap_mode") == cap_mode
        and ns.get("_S9_CAP_MODE") == cap_mode)
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
        "form": form,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base": {"path": str(BASE_MAIN), "sha256": base_sha,
                 "bytes": len(base_bytes)},
        "main": {"path": str(main_path), "sha256": main_sha,
                 "bytes": len(out_bytes)},
        "entry": ENTRY_NAME,
        "host_entry": "_s8_agent",
        "cap_mode": cap_mode,
        "semantics": {
            "topup_dayhigh_gate": "③同拍申报修复仅当日新高拍保留（q>当日 "
                                  "running max）；平台拍补量=挪卖→还原宿主申报",
            "append_unchanged": "②追加单沿 s8 语义（分品毛增益 WHEAT "
                                "+92~+338 为实）" if cap_mode == 'off'
                                else "②追加单量修：实存量帽+果麦单拍帽 8",
            "stock_cap": "实存量帽：shed+Σ单位仓+同拍买腿−原生申报（消 no_stock"
                         " 幻影空跑 10/40）" if cap_mode == 'on' else "off",
            "conservation": "纯同拍后处理；零跨拍挪量（R23/R26 红线）；只撤销/"
                            "裁剪尖拍层加量；非触发拍零足迹；异常回退；step≥712 "
                            "零触碰",
        },
        "checks": checks,
        "commands": ["python3 orderbook_s9fam_lab/build_s9.py",
                     "python3 orderbook_s9fam_lab/judge_s9.py"],
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    ms = {"s9a": build_s9("s9a", "off"), "s9b": build_s9("s9b", "on")}
    (EVID_DIR / "build_s9.json").write_text(
        json.dumps({f: {"sha256": m["main"]["sha256"],
                        "checks": m["checks"]}
                    for f, m in ms.items()},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f, m in ms.items():
        print("BUILD", f, m["main"]["sha256"][:16], m["checks"], flush=True)
    print("BUILD OK %.1fs" % (time.perf_counter() - t0))
    return ms


if __name__ == "__main__":
    main()
