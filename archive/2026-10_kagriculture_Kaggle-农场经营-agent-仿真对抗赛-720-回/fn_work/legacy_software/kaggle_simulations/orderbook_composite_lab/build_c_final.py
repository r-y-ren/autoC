# -*- coding: utf-8 -*-
"""build_c_final（composite lab）：三正交面合建完全体 c_final（新建 lab；不改既有代码）。

合建式（同面干扰定理：三面作用域正交，diff 审计证明零冲突）：
  C_final = oc_c3 冠军基（sha 3f8b57fd…，卖面零触碰）
          + fert60 层（orderbook_d1prod_lab：作物格 PASS→FERTILIZE，
            自用 0.428/肥处置配比 46/54 附近——D5 配比解）
          + M13 修复层（orderbook_m13fix_lab：D1 画像换局复位 +
            D2 C3 闩复位/换表可逆 + D3 s804 记账）。
三面作用域：fert=作物格动作（磁带 ops）；M13=状态复位/记账（代码面）；
oc_c3 卖面=零触碰（既有市场单零改写）。

M13 面沿 m13fix 先例（尾块/内层薄补丁+反替换回程封印），入口按本线
末 callable 语义归一为 _hs_agent（oc_c3 谱系入口）。
产物 orderbook_composite_lab/build/c_final/。只写 orderbook_composite_lab/。
不提交；不发射。
"""
from __future__ import annotations

import difflib
import hashlib
import io
import json
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
OC3_MAIN = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
FERT60_MAIN = KSIM_DIR / "orderbook_d1prod_lab" / "build" / "fert60" / "main.py"
OUT_DIR = MODULE_DIR / "build" / "c_final"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_composite_manifest/1.0"
OC3_SHA = "3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d39ba9bd23d"
FERT60_SHA = "1a5a233f39df64281b91657e1e07cb8926aefa33a85554f34ebbf51f5c3543f7"

# ---- 内层薄补丁①（D3，m13fix 先例逐字沿用）：_s804 自插 SELL 双写 _S758_HIST ----
D3_OLD = (
    "            h['prev']['own'][item]=h['prev']['own'].get(item,0)+take;"
    "_S804_REPORT['fires']+=1;_S804_REPORT['units']+=take;added=True")
D3_NEW = (
    "            h['prev']['own'][item]=h['prev']['own'].get(item,0)+take\n"
    "            _m13h=_S758_HIST.get(player) or {}\n"
    "            if (_m13h.get('prev') or {}).get('step')==step:"
    "_m13h['prev']['own'][item]=_m13h['prev']['own'].get(item,0)+take\n"
    "            _S804_REPORT['fires']+=1;_S804_REPORT['units']+=take;added=True")

# ---- 尾块（D1+D2，m13fix 先例逐字沿用；入口归一改本线 _hs_agent） ----
TAIL = '''

# ==== M13 状态闭合修复（c_final 尾块：D1 画像换局复位 + D2 C3 换局还原） ====
_M13_OC_AFTER = _oc_after
_M13_C3_SWAP = _oc_c3_swap
_M13_C3_BACKUP = [None]


def _m13_c3_restore():
    """换局复位：反向还原 C3 换表触点 + 一次性闩复位（step==0/换局重播）。"""
    try:
        bk = _M13_C3_BACKUP[0]
        if bk:
            routes = _IMPL.chassis.routes
            for (rid, idx), act in bk.items():
                seq = routes.get(rid)
                if seq is not None and 0 <= idx < len(seq):
                    seq[idx] = act
    except Exception:
        pass
    _M13_C3_BACKUP[0] = None
    _OC_C3_SWAPPED[0] = False


def _oc_after(observation, action):
    """M13 D1/D2：step==0 或 step<=last_step 换局重播（基座 _RACE_STATE 模板）。"""
    try:
        step = int((observation or {}).get('step', 0))
        player = int((observation or {}).get('player', 0))
        st = _OC_STATE.get(player)
        if st is None or step == 0 or step <= st.get('last_step', -1):
            _OC_STATE[player] = _oc_state_new()
            _m13_c3_restore()
    except Exception:
        pass
    return _M13_OC_AFTER(observation, action)


def _oc_c3_swap(observation, step):
    """M13 D2：换表前备份 delta 触点原值（换局可逆；非 wfr 零足迹）。"""
    if _OC_C3_SWAPPED[0] or int(step) < 144:
        return
    try:
        if _oc_cls(observation, step) not in _OC_C3_CLASSES:
            return
        bk = {}
        for rid, seq in _IMPL.chassis.routes.items():
            for sstep in (_OC_C3_DELTA.get(str(rid)) or {}):
                i = int(sstep)
                if 0 <= i < len(seq):
                    bk[(rid, i)] = seq[i]
        _M13_C3_BACKUP[0] = bk
    except Exception:
        _M13_C3_BACKUP[0] = None
    return _M13_C3_SWAP(observation, step)


# ---- 入口归一（末函数=_hs_agent；m13 尾块不改入口语义） ----
_M13_ENTRY_TMP = _hs_agent
del _hs_agent
_hs_agent = _M13_ENTRY_TMP
del _M13_ENTRY_TMP
'''


def substitute(base_src: str):
    """内层薄补丁 D3 + 尾块 D1/D2；反替换回程逐字节=基底（fert60）。"""
    if base_src.count(D3_OLD) != 1:
        raise RuntimeError("校验①红 D3 目标块计数 %d 应为 1"
                           % base_src.count(D3_OLD))
    if "_M13_" in base_src:
        raise RuntimeError("校验①红 基底已含 M13 痕迹")
    src = base_src.replace(D3_OLD, D3_NEW)
    src = src + TAIL
    return src


def reverse_extract(injected: str) -> str:
    """封印：剥离尾块 + 反替换 D3 -> 应逐字节=fert60 基底源。"""
    if not injected.endswith(TAIL):
        raise RuntimeError("校验②红 尾块不齐")
    stripped = injected[:-len(TAIL)]
    if stripped.count(D3_NEW) != 1:
        raise RuntimeError("校验②红 D3 反替换计数漂移")
    stripped = stripped.replace(D3_NEW, D3_OLD)
    return stripped


# ============================================================ 三面 diff 审计 ==
def _hunks(a: str, b: str):
    la, lb = a.splitlines(), b.splitlines()
    sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        def grab(ls, s0, s1):
            return " ".join(x[:160] for x in ls[s0:min(s1, s0 + 8)])
        out.append({"tag": tag, "a_lines": [i1 + 1, i2], "b_lines": [j1 + 1, j2],
                    "sample": grab(la, i1, i2) + " ||| " + grab(lb, j1, j2)})
    return out


def _classify(h):
    s = h.get("sample") or ""
    if "_R108_DATA" in s:
        return "fert:tape_blob"
    if "_GP_PLAN" in s or "_alt_install" in s:
        return "fert:assert_regen"
    if "_m13h" in s or ("_S758_HIST" in s and "prev" in s):
        return "m13:D3_ledger"
    if ("M13 状态闭合修复" in s or "_m13_c3_restore" in s or "_M13_" in s):
        return "m13:tail"
    return "unclassified"


def diff_audit(oc3_src, fert_src, cfin_src):
    """三面零冲突证明：①fert 面=oc_c3→fert60（仅磁带 blob+断言重生成块）
    ②M13 面=fert60→c_final（仅 D3 一行+尾块）③卖面零触碰（市场单逐拍恒等
    +改写区无卖面决策码）④两面改写区不相交（同面干扰定理前提）。"""
    # ---- 面① fert：文本 hunk 分类 ----
    hunks_f = _hunks(oc3_src, fert_src)
    cls_f = {}
    for h in hunks_f:
        c = _classify(h)
        cls_f[c] = cls_f.get(c, 0) + 1
        h["face"] = c
    # ---- 面② M13：文本 hunk 分类 ----
    hunks_m = _hunks(fert_src, cfin_src)
    cls_m = {}
    for h in hunks_m:
        c = _classify(h)
        cls_m[c] = cls_m.get(c, 0) + 1
        h["face"] = c
    unclassified = [h for h in hunks_f + hunks_m if h["face"] == "unclassified"]

    # ---- 面①③ 磁带级：oc_c3 vs fert60 解码逐格对比 ----
    import sys
    if str(KSIM_DIR) not in sys.path:
        sys.path.insert(0, str(KSIM_DIR))
    from orderbook_r37 import retape_sheep as rs  # noqa: WPS433
    pk_b = rs._decode_routes(oc3_src)
    pk_v = rs._decode_routes(fert_src)
    pk_c = rs._decode_routes(cfin_src)
    sell_same = True
    unit_diffs = {"PASS->FERTILIZE": 0, "other": 0}
    other_samples = []
    n_cells = 0
    for rid in pk_b["routes"]:
        ib, iv = pk_b["routes"][rid], pk_v["routes"][rid]
        for s in range(len(ib)):
            ab = pk_b["actions"][ib[s]]
            av = pk_v["actions"][iv[s]]
            mb, mv = ab.get("market") or [], av.get("market") or []
            if mb != mv:
                sell_same = False
            ub = [("F", ab.get("farmer") or ["PASS"])] + \
                 [("h%d" % k, h) for k, h in enumerate(ab.get("hands") or [])
                  if isinstance(h, list)]
            uv = [("F", av.get("farmer") or ["PASS"])] + \
                 [("h%d" % k, h) for k, h in enumerate(av.get("hands") or [])
                  if isinstance(h, list)]
            if ub == uv:
                continue
            n_cells += 1
            ok = len(ub) == len(uv)
            if ok:
                for (ua, oa), (u2, ob) in zip(ub, uv):
                    if ua != u2:
                        ok = False
                        break
                    if oa == ob:
                        continue
                    if oa == ["PASS"] and ob == ["FERTILIZE"]:
                        unit_diffs["PASS->FERTILIZE"] += 1
                    else:
                        unit_diffs["other"] += 1
                        ok = False
                        if len(other_samples) < 5:
                            other_samples.append(
                                {"route": rid, "step": s, "unit": ua,
                                 "from": oa, "to": ob})
            else:
                unit_diffs["other"] += 1
                if len(other_samples) < 5:
                    other_samples.append({"route": rid, "step": s,
                                          "note": "unit 签名不齐"})
    # c_final 磁带= fert60 磁带（M13 面零磁带触碰）
    blob_fert_ok = True
    try:
        for rid in pk_v["routes"]:
            iv, ic = pk_v["routes"][rid], pk_c["routes"][rid]
            for s in range(len(iv)):
                if pk_v["actions"][iv[s]] != pk_c["actions"][ic[s]]:
                    blob_fert_ok = False
                    break
    except Exception:
        blob_fert_ok = False
    # ---- 改写区不相交（面① hunk 行区 vs 面② hunk 行区，b 侧）----
    def spans(hunks, key):
        return [(h[key][0], h[key][1]) for h in hunks]
    sp_f = spans(hunks_f, "b_lines")
    sp_m = spans(hunks_m, "a_lines")
    overlap = [x for x in sp_f for y in sp_m
               if not (x[1] < y[0] or y[1] < x[0])]
    return {
        "faces": {
            "fert": {"src": "orderbook_d1prod_lab/build/fert60（oc_c3+fert 层）",
                     "n_hunks": len(hunks_f), "hunk_classes": cls_f},
            "m13": {"src": "orderbook_m13fix_lab 三修复件（D1/D2/D3）",
                    "n_hunks": len(hunks_m), "hunk_classes": cls_m},
            "oc_c3_sell_face": {"touch": 0,
                                "caliber": "既有市场单零改写（磁带级）+改写区无卖面决策码"},
        },
        "tape_cells_changed_oc3_to_fert": n_cells,
        "unit_op_diffs": unit_diffs,
        "unit_op_diff_other_samples": other_samples,
        "sell_orders_identical_oc3_vs_fert": bool(sell_same),
        "tape_identical_fert_vs_cfin": bool(blob_fert_ok),
        "hunk_spans_disjoint": bool(not overlap),
        "unclassified_hunks": len(unclassified),
        "unclassified_samples": unclassified[:3],
        "zero_conflict": bool(not unclassified and not overlap and sell_same
                             and blob_fert_ok and unit_diffs["other"] == 0),
    }


# ============================================================ 包写盘 ==
def build_one(oc3_src: str, fert_bytes: bytes):
    base_src = fert_bytes.decode("utf-8")
    t0 = time.perf_counter()
    injected = substitute(base_src)
    back = reverse_extract(injected)
    if back != base_src:
        raise RuntimeError("校验②红 反替换回程 != fert60 基底源")
    try:
        compile(injected, "<c_final>", "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 语法不通过: %r" % (exc,))
    ns = {}
    try:
        exec(compile(injected, "<c_final>", "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 exec 失败: %r" % (exc,))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_hs_agent":
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 末 callable=%r" % (got,))
    if ns.get("_M13_OC_AFTER") is None or ns.get("_M13_C3_SWAP") is None:
        raise RuntimeError("校验④红 m13 尾块捕获缺失")
    if ns.get("_OC_C3_SWAPPED") != [False]:
        raise RuntimeError("校验④红 闩初值漂移")
    audit = diff_audit(oc3_src, base_src, injected)
    if not audit["zero_conflict"]:
        raise RuntimeError("校验⑤红 三面 diff 审计未过: %r"
                           % (audit.get("unclassified_samples"),))
    data = injected.encode("utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "main.py"
    out.write_bytes(data)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(str(out), arcname="main.py")
    tar_bytes = buf.getvalue()
    (OUT_DIR / "submission.tar.gz").write_bytes(tar_bytes)
    man = {
        "schema": SCHEMA, "form": "c_final",
        "desc": "三正交面合建完全体：oc_c3 冠军基 + fert60 层（作物格 "
                "PASS→FERTILIZE，自用 0.428/肥处置配比）+ M13 修复层"
                "（画像复位+C3 闩复位/换表可逆+s804 记账）",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "faces": {
            "oc_c3": {"main": str(OC3_MAIN), "sha256": OC3_SHA,
                      "role": "冠军基（卖面零触碰）"},
            "fert60": {"main": str(FERT60_MAIN), "sha256": FERT60_SHA,
                       "role": "作物格动作面（PASS→FERTILIZE 自用 0.428）"},
            "m13": {"main": str(KSIM_DIR / "orderbook_m13fix_lab" / "build"
                                / "u2v2_dh_fix" / "main.py"),
                    "role": "状态复位面（D1/D2/D3）",
                    "note": "补丁形态沿 m13fix 先例；落座基底改 fert60"},
        },
        "base_main": str(FERT60_MAIN),
        "base_main_sha256": hashlib.sha256(fert_bytes).hexdigest(),
        "champion_base_sha256": OC3_SHA,
        "entry": "_hs_agent",
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "patches": {
            "D1": "_oc_after 头部 step==0 或 step<=last_step -> _oc_state_new()",
            "D2": "_oc_c3_swap 换表前备份 delta 触点；_m13_c3_restore 换局"
                  "反向还原+闩复位",
            "D3": "_s804_apply 自插 SELL 同步记 _S758_HIST prev own"},
        "subs": [{"old": D3_OLD, "new": D3_NEW, "count": 1}],
        "tail_bytes": len(TAIL.encode("utf-8")),
        "compile_ok": True, "exec_ok": True,
        "entry_last_callable": "_hs_agent",
        "roundtrip_identity_ok": True,
        "roundtrip_target": "fert60 基底源逐字节",
        "diff_audit": audit,
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    (OUT_DIR / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    return man


def main():
    oc3_bytes = OC3_MAIN.read_bytes()
    fert_bytes = FERT60_MAIN.read_bytes()
    sha3 = hashlib.sha256(oc3_bytes).hexdigest()
    shaf = hashlib.sha256(fert_bytes).hexdigest()
    if sha3 != OC3_SHA:
        raise RuntimeError("oc_c3 冠军基 sha 漂移: %s" % sha3)
    if shaf != FERT60_SHA:
        raise RuntimeError("fert60 基底 sha 漂移: %s" % shaf)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    man = build_one(oc3_bytes.decode("utf-8"), fert_bytes)
    out = {"version": "c-final-build/1.0",
           "champion_sha": sha3, "fert60_sha": shaf,
           "form": {k: man[k] for k in ("main_sha256", "tar_sha256", "subs",
                                        "roundtrip_identity_ok",
                                        "diff_audit")}}
    (EVID_DIR / "build_c_final.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("built c_final", man["main_sha256"][:16], flush=True)
    return man


if __name__ == "__main__":
    main()
