# -*- coding: utf-8 -*-
"""cond_route_build：件 C = H1 + 条件路由层（条件合装件；判决先行·不发射）。

责任口径（任务 cond-route-confirm）：在轨道 1 唯一正臂格（ICE_CREAM_SHOP+
YARN_STORE / r105 generic，netflip=+1 n=16）上做**条件合装**：
- 开局判世界=首两店有序对恰为 {ICE_CREAM_SHOP, YARN_STORE}（两序都算）→
  该局路由走 r105 线；否则行为与 H1 逐字节同。
- 换线机制沿 ab_t1a 既有尾块（step144 揭示帧锁存按世界强制路线；底 day27
  换线保留——与轨道 1 正臂逐字同机制，保证 Δ 复现口径一致）；末 callable
  不变（_hs_agent，官方 last-callable 语义）。
- 判世界时点=step144 揭示帧（world 第二店于 step143 才落定，最早可判时点；
  H1 基座同款 day6 锁存时点；pre-144 与 H1 逐字节同 → world 实现不受处理影响）。

产物 build_cond/：c_main.py + submission.tar.gz（成员恰 ['main.py']）+
build_manifest.json。构建校验 fail-closed：①语法 ②装载末 callable=_hs_agent
③基座字节前缀恒等（H1 零改动）④尾块 def 数=1（末 callable 语义保护）⑤router
探针（触发/非触发/两序/day27 语义逐点核对）。

基底=orderbook_strongest_lab/build/h1/main.py（sha 76b5f842…）。
复用（不改写）：ab_t1a 换线机制（尾块形态）、judge_r23._load_entry。
只写 orderbook_track1_lab/build_cond/。不改既有代码。不发射。
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

RECORD_VERSION = "cond-route-build/1.0"
BASE_MAIN = (KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")
BASE_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb67649"
                     "74b22f337")
OUT_DIR = MODULE_DIR / "build_cond"
EVID_DIR = OUT_DIR / "evidence"
ENTRY_NAME = "_hs_agent"
ROUTE_ARM = 105                     # 轨道 1 正臂 r105（generic）
TRIGGER_SHOPS = ("ICE_CREAM_SHOP", "YARN_STORE")
REVEAL_STEP = 144
DAY27_STEP = 648                    # H1 底 day27 换线（route=2）保留
SENTINEL = '"""cond-route C 条件路由层（judge-side only；H1 基座零改动）'

_TAIL = """
# ===== cond-route C 条件路由层（judge-side only；H1 基座零改动前缀恒等） =====
# 件 C = H1 + 条件路由：step144 揭示帧判世界（world 第二店 step143 才落定，
# 最早可判时点；H1 基座同款 day6 锁存）——首两店有序对恰为
# {ICE_CREAM_SHOP, YARN_STORE}（两序都算，排序键归一）→ 该局路由走 r105 线
# （step144..647 强制；底 day27 换线保留，与轨道 1 正臂 ab_t1a 逐字同机制）；
# 否则（非触发世界）router 原样返回基座值，行为与 H1 逐字节同。
_CR_BASE_ROUTER = _IMPL.chassis.router
_CR_ROUTE = %(route)d
_CR_TARGET_KEY = %(target_key)r
_CR_REVEAL = %(reveal)d


def _cr_router(observation, step, state):
    \"\"\"条件路由层：step144 锁存判世界→触发强制 r105；非触发零足迹。\"\"\"
    r = _CR_BASE_ROUTER(observation, step, state)
    try:
        if int(step) >= _CR_REVEAL and not state.get('cr_latched'):
            state['cr_latched'] = True
            town = observation.get('town') or {}
            shops = sorted(str(s) for s in
                           list(town.get('unlocked_shops') or [])[:2])
            if "+".join(shops) == _CR_TARGET_KEY:
                state['route'] = int(_CR_ROUTE)
                r = int(_CR_ROUTE)
    except Exception:
        pass
    return r


_IMPL.chassis.router = _cr_router

# ---- 入口归一（末 callable 保持=_hs_agent） ----
_CR_ENTRY_TMP = _hs_agent
del _hs_agent
_hs_agent = _CR_ENTRY_TMP
del _CR_ENTRY_TMP
"""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_tail() -> str:
    target_key = "+".join(sorted(TRIGGER_SHOPS))
    return _TAIL % {"route": ROUTE_ARM, "target_key": target_key,
                    "reveal": REVEAL_STEP}


def build_c_main(base_src: str) -> str:
    """条件合装构建（fail-closed 五校验）；返回注入后源文本。"""
    if not isinstance(base_src, str) or not base_src.strip():
        raise ValueError("base_src 非法")
    tail = build_tail()
    text = base_src + tail
    # 校验①语法
    try:
        compile(text, "<cond-route-C>", "exec")
    except Exception as exc:
        raise RuntimeError("校验①红：注入后源语法不通过: %r" % (exc,))
    # 校验④尾块 def 数=1（末 callable 语义保护）
    n_def = tail.count("\ndef ") + (1 if tail.startswith("def ") else 0)
    if n_def != 1:
        raise RuntimeError("校验④红：尾块 def 数=%d（应 1）" % n_def)
    # 校验②装载后末 callable=_hs_agent
    ns: dict = {}
    exec(compile(text, "<cond-route-C-entry>", "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验②红：末 callable=%r 应为 %r" % (got, ENTRY_NAME))
    # 校验③基座字节前缀恒等（append-only）
    if not text.startswith(base_src):
        raise RuntimeError("校验③红：基座字节前缀不恒等")
    # 校验⑤ router 探针（触发/非触发/两序/day27 语义逐点核对）
    probe = router_probe(ns, base_src)
    if not probe["passed"]:
        raise RuntimeError("校验⑤红：router 探针不通过: %s" % probe["failed"])
    return text


def _mk_obs(step: int, shops) -> dict:
    return {"step": step, "player": 0, "day": step // 24, "hour": step % 24,
            "town": {"unlocked_shops": list(shops)},
            "farms": [{"money": 1000.0}, {"money": 1000.0}],
            "market": {"inventory": {"WHEAT": 0}, "prices": {}}}


def router_probe(ns: dict, base_src: str) -> dict:
    """探针：件 C router vs H1 基座 router（同 obs 同 fresh state 逐点比对）。

    - 非触发世界：step0/72/144/200/648 全点与基座逐点一致（零足迹）；
    - 触发世界（两序都算）：step<144 与基座一致；144..647==r105；648==day27 底线。
    """
    base_ns: dict = {}
    exec(compile(base_src, "<cond-route-C-probe-base>", "exec"), base_ns)
    base_router = base_ns["_router"]
    cr_router = ns["_cr_router"]
    rows = []
    ok = True
    trigger_sets = [(TRIGGER_SHOPS[0], TRIGGER_SHOPS[1]),
                    (TRIGGER_SHOPS[1], TRIGGER_SHOPS[0])]
    non_trigger = [("ICE_CREAM_SHOP", "ICE_CREAM_SHOP"),
                   ("BAKERY", "YARN_STORE"), ("PET_CAFE", "PIZZA_SHOP"),
                   ("ICE_CREAM_SHOP", "PET_CAFE")]
    for shops in non_trigger + trigger_sets:
        is_trg = tuple(sorted(shops)) == tuple(sorted(TRIGGER_SHOPS))
        st_b, st_c = {}, {}
        for step in (0, 72, REVEAL_STEP, REVEAL_STEP + 40, DAY27_STEP):
            obs = _mk_obs(step, shops)
            rb = base_router(obs, step, st_b)
            rc = cr_router(obs, step, st_c)
            expect = rb
            if is_trg and REVEAL_STEP <= step < DAY27_STEP:
                expect = ROUTE_ARM
            match = (rc == expect)
            ok = ok and match
            rows.append({"shops": list(shops), "step": step,
                         "base": rb, "c": rc, "expect": expect,
                         "match": match})
    return {"passed": ok, "rows": rows,
            "failed": [r for r in rows if not r["match"]]}


def _make_tar(main_bytes: bytes) -> bytes:
    """submission.tar.gz（成员恰 ['main.py']，供身份门）。"""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    return buf.getvalue()


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = _sha256(base_bytes)
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("基底 sha 不符（H1 字节漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("基底不以换行收尾（fail-closed）")
    text = build_c_main(base_src)
    data = text.encode("utf-8")
    tar_bytes = _make_tar(data)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "c_main.py").write_bytes(data)
    (OUT_DIR / "submission.tar.gz").write_bytes(tar_bytes)
    target_key = "+".join(sorted(TRIGGER_SHOPS))
    manifest = {
        "schema": "orderbook_track1_lab_cond_manifest/1.0",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "candidate": "cond-route-C",
        "design": "H1 + 条件路由层（开局判世界=首两店有序对恰为 {%s}（两序都算）"
                  "→ 该局路由走 r105 线；否则行为与 H1 逐字节同）"
                  % ", ".join(TRIGGER_SHOPS),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": base_sha,
        "base_bytes": len(base_bytes),
        "main_name": "c_main.py",
        "main_sha256": _sha256(data),
        "main_bytes": len(data),
        "tar_name": "submission.tar.gz",
        "tar_sha256": _sha256(tar_bytes),
        "tar_bytes": len(tar_bytes),
        "tar_members": ["main.py"],
        "append_only_prefix_identical": True,
        "entry": ENTRY_NAME,
        "entry_last_callable": True,
        "route_arm": ROUTE_ARM,
        "trigger_key": target_key,
        "reveal_step": REVEAL_STEP,
        "day27_switch_preserved": True,
        "mechanism": "ab_t1a 尾块换线机制复用（step144 揭示帧锁存按世界强制路线；"
                     "底 day27 换线保留；末 callable 不变）",
        "compile_ok": True,
        "tail_def_count": 1,
    }
    (OUT_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("built", manifest["main_sha256"][:16], manifest["main_bytes"],
          "bytes; tar", manifest["tar_bytes"], flush=True)
    return manifest


if __name__ == "__main__":
    main()
