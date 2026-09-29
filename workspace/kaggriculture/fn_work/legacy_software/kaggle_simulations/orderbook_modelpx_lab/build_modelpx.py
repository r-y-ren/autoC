# -*- coding: utf-8 -*-
"""build_modelpx：MODELPX 预测器内部参数网格构建线（grid-search；判决先行·不
发射不提交）。

构建底=orderbook_oppcond_lab/build/oc_c3/main.py（sha 3f8b57fd…）零改动读入，
沿用 orderbook_milkwin_lab 手术面（参数替换+计数台账+反替换回程封印）扩展为
6 组字面量替换（fail-closed）：
  ①量帽档式 ×1 → _mx_cap(...)（帽钉死 (3,6,10)：帽=已判死门旋钮，防 planned
    联动污染轴2）
  ②planned=6 ×4 → planned=_MX_PLANNED（仅进 inv_next 预测式）
  ③滑窗 len(hist[i])>12:del hist[i][:6] ×3 → _MX_WIN/_MX_WIN//2
  ④S804 独立史 len(h[i])>12:del h[i][:6] ×1 → 同 ③
  ⑤_S758_ITEMS 三品 ×1 → _MX_ITEMS（轴3 品项集）
  ⑥_S758_HOURS = tuple(range(1,23)) ×1 → tuple(range(_MX_H0,23))（轴4 时段）
反替换回程逐字节=基座源（参数级封印）。阈 0.5/均值窗 4/hour-1 高价档不参改
（预登记口径：hour-1 档为独立继承层，不随时段轴）。

网格（预测器内部真绑定旋钮；正交抽样18 配置粗扫）：
  轴1 预测窗 win   ∈ {12, 6, 24}      （基线 12=预滑窗）
  轴2 planned     ∈ {6, 2, 12}        （基线 6）
  轴3 品项集 items ∈ {三品, +CARROT, +EGG}
  轴4 时段 h0      ∈ {2, 10, 14}      （h2-22/h10-22/h14-22 窗聚焦）
L9(3^4) 双阵列+贪心补齐 → 18 配置（含基线 mp_base=全基线，运行时 placebo）。
只写 orderbook_modelpx_lab/。
"""
from __future__ import annotations

import hashlib
import json
import time
from itertools import product
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
BASE_MAIN = (KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_modelpx_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d3"
                     "9ba9bd23d")
SENTINEL = '# ---- modelpx mp 实验尾块'
ENTRY_NAME = "_mx_agent"
HOST_NAME = "_hs_agent"
CAPTURE_SRC = ("_MX_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"

# ---- 参数级替换台账（6 组字面量；反替换回程=基座源） ----
SUBS = (
    ("take=min(avail,(10 if p_now>=100 else (10 if (step%24) in (10,11,12,13) "
     "and p_now>=30 else (planned if (step%24) in (10,11,12,13) and p_now>=10 "
     "else max(1,planned//2)))))",
     "take=min(avail,_mx_cap(item,p_now,step,planned))", 1),
    ("planned=6", "planned=_MX_PLANNED", 4),
    ("len(hist[i])>12:del hist[i][:6]",
     "len(hist[i])>_MX_WIN:del hist[i][:_MX_WIN//2]", 3),
    ("len(h[i])>12:del h[i][:6]",
     "len(h[i])>_MX_WIN:del h[i][:_MX_WIN//2]", 1),
    ("_S758_ITEMS=('MILK','STRAWBERRY','WOOL')", "_S758_ITEMS=_MX_ITEMS", 1),
    ("_S758_HOURS = tuple(range(1,23))",
     "_S758_HOURS = tuple(range(_MX_H0,23))", 1),
)

# ---- 轴（level 0=基线） ----
AXES = {
    "win": (12, 6, 24),            # 轴1 预测窗（预滑窗）
    "planned": (6, 2, 12),         # 轴2 planned 常数
    "items": ("base3", "carrot", "egg"),   # 轴3 品项集
    "h0": (2, 10, 14),             # 轴4 时段聚焦（h2-22/h10-22/h14-22）
}
ITEMS_MAP = {
    "base3": ("MILK", "STRAWBERRY", "WOOL"),
    "carrot": ("MILK", "STRAWBERRY", "WOOL", "CARROT"),
    "egg": ("MILK", "STRAWBERRY", "WOOL", "EGG"),
}
LEVEL_NAMES = {"win": ("12", "6", "24"), "planned": ("6", "2", "12"),
               "items": ("3", "carrot", "egg"), "h0": ("2", "10", "14")}
BASELINE = (0, 0, 0, 0)

LAYER_LABEL = ("件 MPX=MODELPX 预测器内部参数网格（滑窗 _MX_WIN、planned 常数、"
               "品项集 _MX_ITEMS、时段 _MX_H0 起点）；量帽钉死 (3,6,10)、阈 0.5、"
               "均值窗 4 不参改；hour-1 高价档独立继承不随时段轴；零跨拍挪量、"
               "磁带 blob 零触碰、异常回退原动作")


def _entry_src():
    """入口生成：宿主动作纯透传（参数手术在宿主体内）；计数仅报告。"""
    return (
        "# ---- 入口捕获（宿主=oc_c3 件末 callable） ----\n"
        + CAPTURE_SRC + "\n\n"
        "def %s(observation, configuration=None):\n"
        "    \"\"\"mpx 网格入口（官方 last-callable）：纯透传。\"\"\"\n"
        "    action = _MX_HOST(observation, configuration)\n"
        "    try:\n"
        "        _MX_REPORT['calls'] += 1\n"
        "    except Exception:\n"
        "        pass\n"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_MX_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _MX_ENTRY_TMP\n"
        "del _MX_ENTRY_TMP\n" % (ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                 ENTRY_NAME, ENTRY_NAME))


# 参数头置于基座源之前（模块级赋站点 _S758_ITEMS/_S758_HOURS 先读后定义）；
# _mx_cap 随头（被替换行在函数体内迟绑定）。
LAYER_TMPL = '''# ---- 件 MPX：MODELPX 预测器内部参数网格层（grid-search 参数头） --------
_MX_WIN = __MX_WIN__
_MX_PLANNED = __MX_PLANNED__
_MX_ITEMS = __MX_ITEMS__
_MX_H0 = __MX_H0__
_MX_CAPS = (3, 6, 10)
_MX_REPORT = dict(win=_MX_WIN, planned=_MX_PLANNED, items=list(_MX_ITEMS),
                  h0=_MX_H0, calls=0)


def _mx_cap(item, p_now, step, planned):
    """量帽钉死基线 (3,6,10)：帽位=已判死门旋钮，不随 planned 联动。"""
    c1, c2, c3 = _MX_CAPS
    if p_now >= 100:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 30:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 10:
        return c2
    return c1
'''


def cfg_id(levels):
    win, planned, items, h0 = levels
    return "mpx_w%s_p%s_%s_h%s" % (LEVEL_NAMES["win"][win],
                                   LEVEL_NAMES["planned"][planned],
                                   LEVEL_NAMES["items"][items],
                                   LEVEL_NAMES["h0"][h0])


def grid18():
    """L9 双阵列+贪心补齐 → 18 个正交抽样配置（level 序，含基线）。"""
    l9 = ((0, 0, 0, 0), (0, 1, 1, 1), (0, 2, 2, 2), (1, 0, 1, 2),
          (1, 1, 2, 0), (1, 2, 0, 1), (2, 0, 2, 1), (2, 1, 0, 2),
          (2, 2, 1, 0))
    rows = list(l9)
    seen = set(rows)
    for a, b, c, d in l9:                       # 第二阵列：水平置换去混淆
        row = (a, (b + 1) % 3, (c + 2) % 3, (d + 1) % 3)
        if row not in seen:
            seen.add(row)
            rows.append(row)
    # 贪心补齐：最大化新水平对覆盖
    def pair_score(row, covered):
        s = 0
        for i in range(4):
            for j in range(i + 1, 4):
                if (i, row[i], j, row[j]) not in covered:
                    s += 1
        return s
    covered = set()
    for row in rows:
        for i in range(4):
            for j in range(i + 1, 4):
                covered.add((i, row[i], j, row[j]))
    for cand in product(range(3), repeat=4):
        if len(rows) >= 18:
            break
        if cand in seen:
            continue
        sc = pair_score(cand, covered)
        if sc >= 3:
            rows.append(cand)
            seen.add(cand)
            for i in range(4):
                for j in range(i + 1, 4):
                    covered.add((i, cand[i], j, cand[j]))
    for cand in product(range(3), repeat=4):     # 兜底补足
        if len(rows) >= 18:
            break
        if cand not in seen:
            rows.append(cand)
            seen.add(cand)
    assert BASELINE in rows, "基线配置必须在粗扫网格内（placebo）"
    return rows[:18]


def substitute(base_src, form):
    """参数级替换（计数 fail-closed）→ (替换后源, 台账)。"""
    src = base_src
    ledger = []
    for old, new, expect in SUBS:
        n = src.count(old)
        if n != expect:
            raise RuntimeError("校验①红 %s: 字面量计数 %d 应为 %d: %r"
                               % (form, n, expect, old[:60]))
        src = src.replace(old, new)
        ledger.append({"old": old, "new": new, "count": n})
    back = src
    for old, new, cnt in reversed(SUBS):
        if back.count(new) != cnt:
            raise RuntimeError("校验②红 %s: 反替换计数漂移: %r" % (form, new[:60]))
        back = back.replace(new, old)
    if back != base_src:
        raise RuntimeError("校验②红 %s: 反替换回程 != 基座源" % form)
    return src, ledger


def build_form(form, levels, base_src):
    win = AXES["win"][levels[0]]
    planned = AXES["planned"][levels[1]]
    items = ITEMS_MAP[AXES["items"][levels[2]]]
    h0 = AXES["h0"][levels[3]]
    sub_src, ledger = substitute(base_src, form)
    layer = (LAYER_TMPL
             .replace("__MX_WIN__", repr(int(win)))
             .replace("__MX_PLANNED__", repr(int(planned)))
             .replace("__MX_ITEMS__", repr(items))
             .replace("__MX_H0__", repr(int(h0))))
    header = (SENTINEL + "（MODELPX 预测器内部参数网格 grid-search）\n"
              "# 构建底=orderbook_oppcond_lab/build/oc_c3/main.py 零改动读入；\n"
              "# 参数级手术=6 组字面量同参替换（计数台账+反替换回程逐字节封印）；\n"
              "# 参数头随 __future__ 之后置入（模块级赋站点先读后定义）、\n"
              "# 尾部捕获宿主+纯透传入口、零行为后处理。\n")
    anchor = "from __future__ import annotations\n"
    idx = sub_src.find(anchor)
    if idx < 0 or sub_src.count(anchor) != 1:
        raise RuntimeError("校验③红 %s: __future__ 锚点非恰 1" % form)
    cut = idx + len(anchor)
    injected = (header + sub_src[:cut] + "\n" + layer.strip("\n") + "\n"
                + SEPARATOR + sub_src[cut:] + SEPARATOR + _entry_src())
    try:
        compile(injected, "<modelpx:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 %s: 注入后源语法不通过: %r" % (form, exc))
    ns = {}
    try:
        exec(compile(injected, "<modelpx:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 %s: 末 callable=%r 应为 %r"
                           % (form, got, ENTRY_NAME))
    if ns.get("_MX_HOST") is not ns.get(HOST_NAME):
        raise RuntimeError("校验④红 %s: 块首捕获非 %s" % (form, HOST_NAME))
    got = {"win": int(ns.get("_MX_WIN")), "planned": int(ns.get("_MX_PLANNED")),
           "items": tuple(ns.get("_MX_ITEMS")), "h0": int(ns.get("_MX_H0"))}
    want = {"win": int(win), "planned": int(planned), "items": tuple(items),
            "h0": int(h0)}
    if got != want:
        raise RuntimeError("校验⑤红 %s: 参数不符 got=%r want=%r" % (form, got, want))
    _mx_cap = ns["_mx_cap"]
    for it in ("MILK", "STRAWBERRY", "WOOL", "CARROT", "EGG"):
        assert _mx_cap(it, 5, 24 * 4 + 2, 6) == 3
        assert _mx_cap(it, 10, 24 * 4 + 10, 6) == 6
        assert _mx_cap(it, 30, 24 * 4 + 10, 6) == 10
        assert _mx_cap(it, 100, 24 * 4 + 2, 6) == 10
    return injected, ledger, got


def build_one(levels, base_src=None):
    """单配置构建→写 build/<id>/main.py + manifest（fail-closed 不产出）。"""
    form = cfg_id(levels)
    if base_src is None:
        base_bytes = BASE_MAIN.read_bytes()
        if hashlib.sha256(base_bytes).hexdigest() != BASE_SHA_EXPECTED:
            raise RuntimeError("构建底 sha 不符（oc_c3 件字节漂移）")
        base_src = base_bytes.decode("utf-8")
    injected, ledger, got = build_form(form, levels, base_src)
    data = injected.encode("utf-8")
    out = OUT_DIR / form / "main.py"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    man = {
        "form": form, "levels": list(levels), "entry": ENTRY_NAME,
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data),
        "base_main_sha256": BASE_SHA_EXPECTED,
        "injected_tail_bytes": len(data) - len(base_src.encode("utf-8")),
        "subs": ledger, "params": got,
        "compile_ok": True, "entry_last_callable": ENTRY_NAME,
        "host_captured": HOST_NAME, "roundtrip_identity_ok": True,
    }
    (OUT_DIR / form / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return man


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("构建底不以换行收尾（fail-closed）")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    rows = grid18()
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN), "base_main_sha256": base_sha,
        "subs": [{"old": o, "new": n, "count": c} for o, n, c in SUBS],
        "roundtrip_identity": "反替换回程逐字节=基座源（参数级封印）",
        "layer": LAYER_LABEL,
        "axes": {k: list(v) for k, v in AXES.items()},
        "grid": [{"levels": list(r), "form": cfg_id(r)} for r in rows],
        "forms": {},
    }
    for r in rows:
        man = build_one(r, base_src)
        manifest["forms"][man["form"]] = man
        print(man["form"], man["main_sha256"][:16], man["params"], flush=True)
    (EVID_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_manifest.json", flush=True)


if __name__ == "__main__":
    main()
