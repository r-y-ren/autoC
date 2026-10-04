# -*- coding: utf-8 -*-
"""build_m13fix：M13 缺陷修复件 dh_fix 构建线（新建 lab；不改既有代码）。

基底=orderbook_unified_u2_lab/build/u2v2_drop_half/main.py
（sha256 5d2d12468a5d1ec53c3d3e4726de54e6a5d29eb038fc97ca45c72b2ce7992df0）。
手术面（尾块/内层薄补丁，足迹审计沿轨道 2——非触发拍零足迹）：
  D1 画像换局复位：_oc_after 开头 step==0 或 step<=last_step -> _oc_state_new()
     （基座 _RACE_STATE 单调闸换局重播模板）；
  D2 C3 闩复位+换表可逆：同一复位块 _oc_c3_restore（备份/还原 chassis.routes
     的 443 条 delta 触点，idx 412-618 与基座开局改写 0-6 不相交）+闩复位；
  D3 s804 自插单记台账：_s804_apply 自插 SELL 同步记 _S758_HIST own（low）。
封印：内层薄补丁逐字量计数 + 反替换回程逐字节=drop_half 基底源。
产出 build/u2v2_dh_fix/{main.py,build_manifest.json,submission.tar.gz}。
只写 orderbook_m13fix_lab/。不提交；不发射。
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
OUT_DIR = MODULE_DIR / "build" / "u2v2_dh_fix"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_m13fix_manifest/1.0"
BASE_SHA_EXPECTED = ("5d2d12468a5d1ec53c3d3e4726de54e6a5d29eb038fc97ca45c72b2"
                     "ce7992df0")

# ---- 内层薄补丁①（D3）：_s804 自插 SELL 双写 _S758_HIST own 台账 ----
D3_OLD = (
    "            h['prev']['own'][item]=h['prev']['own'].get(item,0)+take;"
    "_S804_REPORT['fires']+=1;_S804_REPORT['units']+=take;added=True")
D3_NEW = (
    "            h['prev']['own'][item]=h['prev']['own'].get(item,0)+take\n"
    "            _m13h=_S758_HIST.get(player) or {}\n"
    "            if (_m13h.get('prev') or {}).get('step')==step:"
    "_m13h['prev']['own'][item]=_m13h['prev']['own'].get(item,0)+take\n"
    "            _S804_REPORT['fires']+=1;_S804_REPORT['units']+=take;added=True")

# ---- 尾块（D1+D2）：画像换局复位 + C3 闩复位/换表可逆 ----
TAIL = '''

# ==== M13 状态闭合修复（dh_fix 尾块：D1 画像换局复位 + D2 C3 换局还原） ====
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


# ---- 入口归一（末函数=_u2_agent；m13 尾块不改入口语义） ----
_M13_ENTRY_TMP = _u2_agent
del _u2_agent
_u2_agent = _M13_ENTRY_TMP
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
    """封印：剥离尾块 + 反替换 D3 -> 应逐字节=drop_half 基底源。"""
    if not injected.endswith(TAIL):
        raise RuntimeError("校验②红 尾块不齐")
    stripped = injected[:-len(TAIL)]
    if stripped.count(D3_NEW) != 1:
        raise RuntimeError("校验②红 D3 反替换计数漂移")
    stripped = stripped.replace(D3_NEW, D3_OLD)
    return stripped


def build_one(base_bytes: bytes):
    base_src = base_bytes.decode("utf-8")
    injected = substitute(base_src)
    back = reverse_extract(injected)
    if back != base_src:
        raise RuntimeError("校验②红 反替换回程 != drop_half 基底源")
    try:
        compile(injected, "<m13fix:dh_fix>", "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 语法不通过: %r" % (exc,))
    ns = {}
    try:
        exec(compile(injected, "<m13fix:dh_fix>", "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 exec 失败: %r" % (exc,))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_u2_agent":
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 末 callable=%r" % (got,))
    if ns.get("_M13_OC_AFTER") is None or ns.get("_M13_C3_SWAP") is None:
        raise RuntimeError("校验④红 m13 尾块捕获缺失")
    if ns.get("_OC_C3_SWAPPED") != [False]:
        raise RuntimeError("校验④红 闩初值漂移")
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
        "schema": SCHEMA, "form": "u2v2_dh_fix",
        "desc": "M13 缺陷修复件（dh_fix）：D1 画像换局复位 + D2 C3 闩复位/换表"
                "可逆 + D3 s804 own 台账双写；单局内行为与 drop_half 逐拍恒等"
                "（修复仅在 step==0/换局边界生效）",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "entry": "_u2_agent",
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "patches": {
            "D1": "_oc_after 头部 step==0 或 step<=last_step -> _oc_state_new()"
                  "（_RACE_STATE 单调闸换局重播模板）",
            "D2": "_oc_c3_swap 换表前备份 443 条 delta 触点(idx 412-618)；"
                  "_m13_c3_restore 换局反向还原+闩复位（与 D1 同一复位块）",
            "D3": "_s804_apply 自插 SELL 同步记 _S758_HIST[player]['prev']"
                  "['own']（prev.step==step 守卫）"},
        "footprint": "非触发拍零足迹（轨道 2 口径）：单局内 D1/D2 仅 step==0/"
                     "换局触发；D3 仅自插拍双写台账（掩蔽零现症收口）；基座开局"
                     "改写层（steps0-6，19 条）属基座自改，非本补丁足迹",
        "subs": [{"old": D3_OLD, "new": D3_NEW, "count": 1}],
        "tail_bytes": len(TAIL.encode("utf-8")),
        "compile_ok": True, "exec_ok": True,
        "entry_last_callable": "_u2_agent",
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
    out = {"version": "m13fix-build/1.0", "base_main_sha256": sha,
           "form": {k: man[k] for k in ("main_sha256", "tar_sha256", "subs",
                                        "roundtrip_identity_ok")}}
    (EVID_DIR / "build_m13fix.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("built dh_fix", man["main_sha256"][:16], flush=True)


if __name__ == "__main__":
    main()
