# -*- coding: utf-8 -*-
"""build_s809look：S5 速赢实验——C_final 基座 `_S809_LOOK` 前瞻常数调参构建线
（判决先行·不发射不提交）。

构建底=orderbook_composite_lab/build/c_final/main.py（sha a37c0d34…）**零改动读入**，
参数级手术=step809 就绪提前层前瞻常数 `_S809_LOOK` 字面量同参替换（3→6 / 3→12，
计数 fail-closed）。该常数为**基座原生层参数**（step809 就绪提前层自带），非外挂
挪量；口径对照 doanthuan/kaggriculture（Apache-2.0）公开复刻记录 `_S809_LOOK`
3→12（对平版 step1009 自报 85%）——只调参数不拷码。

变体（一臂一旋钮）：
- look6 ：`_S809_LOOK` 3→6（中间档）
- look12：`_S809_LOOK` 3→12（doanthuan 口径）
- 对照基 = C_final 原件（`_S809_LOOK`=3，不产出拷贝，判决侧直接引用）

校验（fail-closed 不产出）：①基座 sha 恒等 a37c0d34… ②字面量计数恰 1
③反替换回程逐字节=基座源（参数级封印）④注入后 compile ⑤exec 装载后
`_S809_LOOK`=目标值且末 callable 与基座同名（入口语义零变化）⑥逐行 diff 恰 1 行
（零结构变化）。产出 build/look6/main.py、build/look12/main.py +
evidence/build_s809look.json（含替换台账）。只写 orderbook_s5s809_lab/。
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
BASE_MAIN = (KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final"
             / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_s5s809look_manifest/1.0"

BASE_SHA_EXPECTED = ("a37c0d3487fe1d2152ec6c0b767b36afc21ad18207accb2d3cf1f1b"
                     "077016a92")
OLD = "_S809_LOOK=3"
ENTRY_NAME = "_hs_agent"
FORMS = {"look6": 6, "look12": 12}


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _load_probe(src: str, path: str):
    """exec 装载一次：返回 (末 callable 名, `_S809_LOOK` 值)。"""
    ns: dict = {}
    exec(compile(src, path, "exec"), ns)
    entries = [k for k, v in ns.items() if callable(v)]
    return (entries[-1] if entries else "", ns.get("_S809_LOOK"))


def build_form(base_src: str, base_sha: str, form: str, value: int):
    """单参数替换（计数 fail-closed）→ 台账 dict。"""
    new_lit = "_S809_LOOK=%d" % value
    n = base_src.count(OLD)
    if n != 1:
        raise RuntimeError("校验②红 %s: 字面量计数 %d 应为 1: %r" % (form, n, OLD))
    src = base_src.replace(OLD, new_lit)
    if src.count(new_lit) != 1:
        raise RuntimeError("校验②红 %s: 替换后计数漂移: %r" % (form, new_lit))
    # 反替换回程=基座源（参数级封印）
    back = src.replace(new_lit, OLD)
    if back != base_src:
        raise RuntimeError("校验③红 %s: 反替换回程 != 基座源" % form)
    # compile
    compile(src, "build/%s/main.py" % form, "exec")
    # exec 装载：参数值 + 末 callable 与基座同名
    name, loaded_val = _load_probe(src, "build/%s/main.py" % form)
    if loaded_val != value:
        raise RuntimeError("校验⑤红 %s: _S809_LOOK=%r 应为 %d"
                           % (form, loaded_val, value))
    if name != ENTRY_NAME:
        raise RuntimeError("校验⑤红 %s: 末 callable=%r 应为 %s"
                           % (form, name, ENTRY_NAME))
    # 逐行 diff 恰 1 行
    a = base_src.splitlines()
    b = src.splitlines()
    if len(a) != len(b):
        raise RuntimeError("校验⑥红 %s: 行数漂移 %d vs %d" % (form, len(a), len(b)))
    diff_lines = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    if len(diff_lines) != 1:
        raise RuntimeError("校验⑥红 %s: diff 行数 %d 应为 1"
                           % (form, len(diff_lines)))
    i, old_line, new_line = diff_lines[0]
    if old_line.strip() != OLD or new_line.strip() != new_lit:
        raise RuntimeError("校验⑥红 %s: diff 行非参数行: %r -> %r"
                           % (form, old_line.strip(), new_line.strip()))
    return src, {
        "form": form,
        "value": value,
        "substitution": {"old": OLD, "new": new_lit, "count": 1,
                         "line_no": i},
        "roundtrip_identity_ok": True,
        "compile_ok": True,
        "load_ok": True,
        "entry": name,
        "diff_lines": 1,
        "main_sha256": _sha(src.encode("utf-8")),
        "main_bytes": len(src.encode("utf-8")),
    }


def main():
    t0 = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    base_b = BASE_MAIN.read_bytes()
    base_sha = _sha(base_b)
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("校验①红: 基座 sha 漂移 %s != %s"
                           % (base_sha, BASE_SHA_EXPECTED))
    base_src = base_b.decode("utf-8")
    ledgers = {}
    for form, value in FORMS.items():
        src, ledger = build_form(base_src, base_sha, form, value)
        out = OUT_DIR / form / "main.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(src, encoding="utf-8")
        ledgers[form] = ledger
        print("built", form, ledger["main_sha256"][:12], flush=True)
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "task": "S5 速赢：C_final `_S809_LOOK` 3→6/3→12 原生层前瞻常数调参"
                "（纯参数改、零结构变化、不提交不发射）",
        "base": {
            "main": str(BASE_MAIN),
            "sha256": base_sha,
            "bytes": len(base_b),
            "entry": ENTRY_NAME,
            "param": {"name": "_S809_LOOK", "value": 3,
                      "layer": "step809 就绪提前层前瞻常数（基座原生层参数）"},
        },
        "param_caliber": ("doanthuan/kaggriculture（Apache-2.0）公开复刻记录："
                          "step1009 基座 `_S809_LOOK` 3→12（ready-stock 销售前瞻"
                          "加深）对平版 step1009 自报 85%；look6=中间档；"
                          "只调参数不拷码"),
        "forms": ledgers,
        "conservation": {
            "structural_change": 0,
            "footprint": "仅 step809 触发面（市场 SELL 面单量；farmer/hands 零触碰）",
            "seal": "参数级封印：字面量计数台账 + 反替换回程逐字节=基座源"
                    "（roundtrip_identity_ok）",
        },
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    (EVID_DIR / "build_s809look.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("MANIFEST ok", flush=True)
    return manifest


if __name__ == "__main__":
    main()
