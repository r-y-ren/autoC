# -*- coding: utf-8 -*-
"""build_c_base：完全体底座 C_base 构建线（新建 lab；不改既有代码）。

基底=orderbook_oppcond_lab/build/oc_c3/main.py（冠军件，sha256 3f8b57fd…）。
修复层=orderbook_m13fix_lab 的 M13 修复面（u2v2_dh_fix：D1 画像换局复位 +
D2 C3 闩复位/换表可逆 + D3 s804 自插记账），剥离 drop_half 依赖后移植：
  - D3 内层薄补丁逐字移植（目标块两基座逐字节同源，count=1）；
  - D1/D2 独立尾块逐字移植，仅入口归一改 _hs_agent（oc_c3 末 callable）；
  - 尾块所引符号（_OC_STATE/_oc_state_new/_oc_after/_oc_c3_swap/_oc_cls/
    _OC_C3_CLASSES/_OC_C3_DELTA/_OC_C3_SWAPPED/_IMPL.chassis.routes）在 oc_c3
    同名同语义（_oc_c3_swap 两基座逐字节同源），无 drop_half 专有耦合。
四门+足迹审计：
  G1 内层薄补丁逐字量计数（D3_OLD count==1）；
  G2 反替换回程逐字节=oc_c3 基底源（封印）；
  G3 compile；
  G4 exec + 末 callable=_hs_agent + 尾块捕获齐 + 闩/备份初值；
  足迹审计：补丁足迹=1 行内层子串 + 尾块；触发面收敛（D1 仅换局边界、D2 备份
  仅 wfr 换表拍、还原仅换局边界、D3 仅自插拍）；delta 触点表两基座同源
  （443 格 idx 412-618，与基座开局改写带 0-6 不相交）；非触发拍零足迹由
  P13 逐拍迹 + 32 局逐拍恒等实证（见 judge_c_base）。
产出 build/c_base/{main.py,build_manifest.json,submission.tar.gz}。
只写 orderbook_composite_lab/。不提交；不发射。
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
BASE_MAIN = (KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py")
OUT_DIR = MODULE_DIR / "build" / "c_base"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_composite_manifest/1.0"
BASE_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d3"
                     "9ba9bd23d")
PORT_FROM = ("orderbook_m13fix_lab/build/u2v2_dh_fix "
             "(main_sha f4b947e1…, base u2v2_drop_half 5d2d1246…)")

# ---- 内层薄补丁（D3）：_s804 自插 SELL 双写 _S758_HIST own 台账（逐字移植） ----
D3_OLD = (
    "            h['prev']['own'][item]=h['prev']['own'].get(item,0)+take;"
    "_S804_REPORT['fires']+=1;_S804_REPORT['units']+=take;added=True")
D3_NEW = (
    "            h['prev']['own'][item]=h['prev']['own'].get(item,0)+take\n"
    "            _m13h=_S758_HIST.get(player) or {}\n"
    "            if (_m13h.get('prev') or {}).get('step')==step:"
    "_m13h['prev']['own'][item]=_m13h['prev']['own'].get(item,0)+take\n"
    "            _S804_REPORT['fires']+=1;_S804_REPORT['units']+=take;added=True")

# ---- 尾块（D1+D2）：画像换局复位 + C3 闩复位/换表可逆（逐字移植；入口 _hs_agent） ----
TAIL = '''

# ==== M13 状态闭合修复移植（c_base 尾块：D1 画像换局复位 + D2 C3 换局还原） ====
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
    """内层薄补丁 D3 + 尾块 D1/D2；反替换回程逐字节=基底。"""
    if base_src.count(D3_OLD) != 1:
        raise RuntimeError("校验①红 D3 目标块计数 %d 应为 1"
                           % base_src.count(D3_OLD))
    src = base_src.replace(D3_OLD, D3_NEW)
    src = src + TAIL
    return src


def reverse_extract(injected: str) -> str:
    """封印：剥离尾块 + 反替换 D3 -> 应逐字节=oc_c3 基底源。"""
    if not injected.endswith(TAIL):
        raise RuntimeError("校验②红 尾块不齐")
    stripped = injected[:-len(TAIL)]
    if stripped.count(D3_NEW) != 1:
        raise RuntimeError("校验②红 D3 反替换计数漂移")
    stripped = stripped.replace(D3_NEW, D3_OLD)
    return stripped


def footprint_audit(base_src: str, injected: str):
    """足迹审计：补丁足迹=1 行内层子串 + 尾块；触发面收敛；delta 表零改写。"""
    import difflib
    added_tail = len(TAIL.encode("utf-8"))
    added_d3 = len(D3_NEW.encode("utf-8")) - len(D3_OLD.encode("utf-8"))
    hunks = [h for h in difflib.unified_diff(
        base_src.splitlines(), injected.splitlines(), lineterm="", n=0)
        if h.startswith(("+@", "-@", "@@")) or h.startswith(("+++", "---"))]
    n_hunk_headers = sum(1 for h in hunks if h.startswith("@@"))
    audit = {
        "patch_footprint": {
            "inner_sub_count": 1,
            "inner_sub_added_bytes": added_d3,
            "tail_added_bytes": added_tail,
            "diff_hunks": n_hunk_headers,
            "note": "补丁足迹=1 行内层子串（D3）+ 尾块（D1/D2）；基底其余逐字节不变"
                    "（G2 反替换回程为证）",
        },
        "trigger_surface": {
            "D1": "仅 step==0 或 step<=last_step（换局边界）改 _OC_STATE[player]",
            "D2_backup": "仅 wfr 类 ∧ step>=144 首次换表拍写 _M13_C3_BACKUP（读操作）",
            "D2_restore": "仅换局边界还原 443 条 delta 触点 + 闩复位",
            "D3": "仅 _s804_apply 自插 SELL 拍双写 _S758_HIST own（prev.step==step 守卫）",
            "non_trigger_ticks": "零写入（零足迹，轨道 2 口径）",
        },
        "delta_map": {
            "cells": None, "idx_min": None, "idx_max": None,
            "unchanged_from_base": True,
            "disjoint_from_base_opening_rewrite": "idx 412-618 ∩ 基座开局改写 0-6 = ∅",
        },
        "runtime_zero_footprint_evidence":
            "probe_c_base P13 逐拍迹（ep2 dirty==0 每拍）+ judge_c_base 32 局"
            " stream_sha 逐拍恒等（identity_pairs.stream_identical）",
    }
    return audit


def build_one(base_bytes: bytes):
    base_src = base_bytes.decode("utf-8")
    injected = substitute(base_src)                       # G1
    back = reverse_extract(injected)                      # G2
    if back != base_src:
        raise RuntimeError("校验②红 反替换回程 != oc_c3 基底源")
    try:
        compile(injected, "<c_base>", "exec")             # G3
    except Exception as exc:
        raise RuntimeError("校验③红 语法不通过: %r" % (exc,))
    ns = {}
    try:
        exec(compile(injected, "<c_base>", "exec"), ns)   # G4
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
    if ns.get("_M13_C3_BACKUP") != [None]:
        raise RuntimeError("校验④红 备份初值漂移")
    audit = footprint_audit(base_src, injected)
    mp = ns.get("_OC_C3_DELTA") or {}
    cells = [int(k) for v in mp.values() for k in v]
    audit["delta_map"]["cells"] = len(cells)
    audit["delta_map"]["idx_min"] = min(cells) if cells else None
    audit["delta_map"]["idx_max"] = max(cells) if cells else None
    if len(cells) != 443 or min(cells) != 412 or max(cells) != 618:
        raise RuntimeError("足迹审计红 delta 触点漂移: n=%d rng=%s-%s"
                           % (len(cells), min(cells or [0]), max(cells or [0])))
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
        "schema": SCHEMA, "form": "c_base",
        "desc": "完全体底座 C_base = oc_c3（冠军件 3f8b57fd）+ M13 修复层移植"
                "（D1 画像换局复位 + D2 C3 闩复位/换表可逆 + D3 s804 自插记账）；"
                "单局内行为与 oc_c3 逐拍恒等（修复仅在 step==0/换局边界与自插拍生效）",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "port_from": PORT_FROM,
        "port_notes": "D3/D1/D2 逐字移植；唯一适配=入口归一 _u2_agent→_hs_agent"
                      "（oc_c3 末 callable）；尾块引用符号两基座同名同语义，"
                      "_oc_c3_swap 两基座逐字节同源，无 drop_half 专有耦合",
        "entry": "_hs_agent",
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "patches": {
            "D1": "_oc_after 头部 step==0 或 step<=last_step -> _oc_state_new()"
                  "（_RACE_STATE 单调闸换局重播模板）",
            "D2": "_oc_c3_swap 换表前备份 443 条 delta 触点(idx 412-618)；"
                  "_m13_c3_restore 换局反向还原+闩复位（与基座开局改写 0-6 不相交）",
            "D3": "_s804_apply 自插 SELL 同步记 _S758_HIST[player]['prev']"
                  "['own']（prev.step==step 守卫）"},
        "footprint": audit,
        "subs": [{"old": D3_OLD, "new": D3_NEW, "count": 1}],
        "tail_bytes": len(TAIL.encode("utf-8")),
        "gates": {
            "G1_sub_count": "PASS (count==1)", "G2_roundtrip_identity": "PASS",
            "G3_compile": "PASS", "G4_exec_entry": "PASS (末 callable=_hs_agent)",
        },
        "compile_ok": True, "exec_ok": True,
        "entry_last_callable": "_hs_agent",
        "roundtrip_identity_ok": True,
    }
    (OUT_DIR / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return man


def main():
    base_bytes = BASE_MAIN.read_bytes()
    sha = hashlib.sha256(base_bytes).hexdigest()
    if sha != BASE_SHA_EXPECTED:
        raise RuntimeError("基底 sha 漂移: %s" % sha)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    man = build_one(base_bytes)
    out = {"version": "c-base-build/1.0", "base_main_sha256": sha,
           "port_from": PORT_FROM,
           "form": {k: man[k] for k in ("main_sha256", "tar_sha256", "subs",
                                        "roundtrip_identity_ok", "gates")},
           "footprint": man["footprint"]}
    (EVID_DIR / "build_c_base.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("built c_base", man["main_sha256"][:16], flush=True)


if __name__ == "__main__":
    main()
