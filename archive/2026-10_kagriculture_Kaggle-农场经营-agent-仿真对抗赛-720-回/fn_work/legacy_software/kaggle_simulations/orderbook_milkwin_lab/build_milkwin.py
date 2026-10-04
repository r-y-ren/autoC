# -*- coding: utf-8 -*-
"""build_milkwin：MODELPX 参数级实验变体构建线（牛奶窗变现；判决先行·不发射
不提交）。

构建底=orderbook_oppcond_lab/build/oc_c3/main.py（sha 3f8b57fd…）**零改动读入**，
参数级手术=基座 MODELPX 层 3 组精确字面量同参替换（阈 1 组×4、量帽档位 1 组
×1、hour-1 帽 1 组×3；计数 fail-closed）+ 尾块注入参数面（沿 build_knee append
先例）：块首捕获宿主末 callable（_MX_HOST=oc_c3 件 _hs_agent），块尾末函数=
_mx_agent（官方 last-callable 入口）。

变体（参数级一臂一旋钮；MILK 侧加权=量帽放大仅 MILK，STRAWBERRY/WOOL 保持
3/6/10）：
- mx_base   ：阈 0.5、帽 3/6/10 全品、无地毯（等价封印形态：应与 oc_c3 逐字节
              动作流同）；
- mx_cap2   ：阈 0.5、MILK 帽 6/12/20（×2 档位）；
- mx_cap33  ：阈 0.5、MILK 帽 10/20/30（×3.33 档位）;
- mx_thr_m02：阈 -0.2（更敏）、帽 3/6/10 全品；
- mx_thr_m10：阈 -1.0（更钝）、帽 3/6/10 全品；
- mx_carpet ：阈 0.5、帽 3/6/10 全品 + 窗内地毯（d14-20 step 336-480 MILK 日
              新高追加单，帽 20/步）——臂 3 条件加跑（判决侧触发）。

校验（fail-closed 不产出）：①替换计数恰 4/1/3 ②反替换回程逐字节=基座源
（参数级封印）③注入后 compile ④exec 装载后末 callable=_mx_agent 且
_MX_HOST=oc_c3 件 _hs_agent ⑤参数与形态一致 ⑥基座 sha 恒等。
另产 submission.tar.gz + build_manifest（含替换台账）。只写
orderbook_milkwin_lab/。
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
BASE_MAIN = (KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
             / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_milkwin_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d3"
                     "9ba9bd23d")
SENTINEL = '"""milkwin mx 实验尾块'
ENTRY_NAME = "_mx_agent"
HOST_NAME = "_hs_agent"
CAPTURE_SRC = ("_MX_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"
LAYER_FILE = "milkwin_layer.py"

# ---- 参数级替换台账（3 组字面量；反替换回程=基座源） ----
SUBS = (
    ("p_next<p_cur-0.5", "p_next<p_cur-_MX_THR", 4),
    ("take=min(avail,(10 if p_now>=100 else (10 if (step%24) in (10,11,12,13) "
     "and p_now>=30 else (planned if (step%24) in (10,11,12,13) and p_now>=10 "
     "else max(1,planned//2)))))",
     "take=min(avail,_mx_cap(item,p_now,step,planned))", 1),
    ("take=min(avail,10)", "take=min(avail,_mx_cap_h1(item))", 3),
)

# ---- 形态面（一臂一旋钮） ----
BASE_CAP = (3, 6, 10)
FORMS = {
    "mx_base": dict(thr=0.5, cap_milk=BASE_CAP, cap_other=BASE_CAP,
                    carpet=False),
    "mx_cap2": dict(thr=0.5, cap_milk=(6, 12, 20), cap_other=BASE_CAP,
                    carpet=False),
    "mx_cap33": dict(thr=0.5, cap_milk=(10, 20, 30), cap_other=BASE_CAP,
                     carpet=False),
    "mx_thr_m02": dict(thr=0.2, cap_milk=BASE_CAP, cap_other=BASE_CAP,
                       carpet=False),
    "mx_thr_m10": dict(thr=1.0, cap_milk=BASE_CAP, cap_other=BASE_CAP,
                       carpet=False),
    "mx_carpet": dict(thr=0.5, cap_milk=BASE_CAP, cap_other=BASE_CAP,
                      carpet=True),
}
LAYER_LABEL = ("件 MX=MODELPX 参数级实验（阈 p_next<p_cur-THR 全 4 处同参；"
               "量帽三档 MILK 侧加权 3/6/10→6/12/20 或 10/20/30，"
               "STRAWBERRY/WOOL 保基线；窗内地毯 d14-20 step336-480 MILK "
               "日新高追加单帽 20/步开关件）；零跨拍挪量、磁带 blob 零触碰、"
               "异常回退原动作")


def _entry_src():
    """入口生成：宿主动作→地毯后处理（关=同对象原样）；step==0 复位台账。"""
    return (
        "def %s(observation, configuration=None):\n"
        "    \"\"\"mx 参数实验入口（官方 last-callable）：宿主动作→窗内地毯"
        "后处理。\"\"\"\n"
        "    action = _MX_HOST(observation, configuration)\n"
        "    try:\n"
        "        if int(_mx_get(observation, 'step', 0) or 0) == 0:\n"
        "            _mx_reset()\n"
        "    except Exception:\n"
        "        pass\n"
        "    action = _mx_post(observation, action)\n"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_MX_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _MX_ENTRY_TMP\n"
        "del _MX_ENTRY_TMP\n" % (ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                 ENTRY_NAME, ENTRY_NAME))


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
    # 反替换回程=基座源（参数级封印）
    back = src
    for old, new, cnt in reversed(SUBS):
        if back.count(new) != cnt:
            raise RuntimeError("校验②红 %s: 反替换计数漂移: %r" % (form, new[:60]))
        back = back.replace(new, old)
    if back != base_src:
        raise RuntimeError("校验②红 %s: 反替换回程 != 基座源" % form)
    return src, ledger


def build_block(params):
    """实验尾块组装（参数面 + 地毯层 + 入口）。"""
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    for tok in ("__MX_THR__", "__MX_CAP_MILK__", "__MX_CAP_OTHER__",
                "__MX_CARPET__"):
        if tok not in layer_src:
            raise RuntimeError("milkwin_layer 缺占位 %s" % tok)
    layer_src = layer_src.replace("__MX_THR__", repr(float(params["thr"])))
    layer_src = layer_src.replace("__MX_CAP_MILK__",
                                  "(%d, %d, %d)" % tuple(params["cap_milk"]))
    layer_src = layer_src.replace("__MX_CAP_OTHER__",
                                  "(%d, %d, %d)" % tuple(params["cap_other"]))
    layer_src = layer_src.replace("__MX_CARPET__",
                                  "True" if params["carpet"] else "False")
    parts = [SENTINEL + "（MODELPX 参数级实验 milk-window）\n"
             "构建底=orderbook_oppcond_lab/build/oc_c3/main.py 零改动读入；"
             "参数级手术=3 组字面量同参替换（计数台账+反替换回程封印）；"
             "宿主=块首捕获之 oc_c3 件末 callable；窗内地毯只加同拍挂卖、"
             "零跨拍挪量（R23/R26 红线）、磁带 blob 零触碰。\n"
             '"""\n'
             + CAPTURE_SRC + "\n\n"]
    parts.append(layer_src.strip("\n") + "\n\n")
    parts.append(_entry_src())
    return "".join(parts)


def build_form(form, params, base_src):
    sub_src, ledger = substitute(base_src, form)
    block = build_block(params)
    injected = sub_src + SEPARATOR + block
    try:
        compile(injected, "<milkwin:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验③红 %s: 注入后源语法不通过: %r" % (form, exc))
    ns = {}
    try:
        exec(compile(injected, "<milkwin:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验④红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验④红 %s: 末 callable=%r 应为 %r"
                           % (form, got, ENTRY_NAME))
    if ns.get("_MX_HOST") is not ns.get(HOST_NAME):
        raise RuntimeError("校验④红 %s: 块首捕获非 %s" % (form, HOST_NAME))
    got = {"thr": float(ns.get("_MX_THR")),
           "cap_milk": tuple(ns.get("_MX_CAPS", {}).get("MILK")),
           "cap_other": tuple(ns.get("_MX_CAPS", {}).get("STRAWBERRY")),
           "carpet": bool(ns.get("_MX_CARPET_ON"))}
    want = {"thr": float(params["thr"]),
            "cap_milk": tuple(params["cap_milk"]),
            "cap_other": tuple(params["cap_other"]),
            "carpet": bool(params["carpet"])}
    if got != want:
        raise RuntimeError("校验⑤红 %s: 参数不符 got=%r want=%r"
                           % (form, got, want))
    # 档位函数单体探针（基线=3/6/10 原式逐档等价）
    _mx_cap = ns["_mx_cap"]
    _mx_cap_h1 = ns["_mx_cap_h1"]
    for it in ("MILK", "STRAWBERRY", "WOOL"):
        c1, c2, c3 = want["cap_milk"] if it == "MILK" else want["cap_other"]
        assert _mx_cap(it, 5, 24 * 4 + 2, 6) == c1
        assert _mx_cap(it, 10, 24 * 4 + 10, 6) == c2
        assert _mx_cap(it, 30, 24 * 4 + 10, 6) == c3
        assert _mx_cap(it, 100, 24 * 4 + 2, 6) == c3
        assert _mx_cap_h1(it) == c3
    return injected, ledger, got


def _make_tar(main_bytes):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    return buf.getvalue()


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（oc_c3 件字节漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("构建底不以换行收尾（fail-closed）")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": base_sha,
        "base_bytes": len(base_bytes),
        "subs": [{"old": o, "new": n, "count": c} for o, n, c in SUBS],
        "roundtrip_identity": "反替换回程逐字节=基座源（参数级封印）",
        "sentinel": SENTINEL,
        "entry": ENTRY_NAME,
        "host": HOST_NAME,
        "layer": LAYER_LABEL,
        "forms": {},
    }
    for form, params in FORMS.items():
        injected, ledger, got = build_form(form, params, base_src)
        data = injected.encode("utf-8")
        tail = len(data) - len(base_bytes)
        out = OUT_DIR / form / "main.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        tar_bytes = _make_tar(data)
        (OUT_DIR / form / "submission.tar.gz").write_bytes(tar_bytes)
        form_manifest = {
            "form": form,
            "entry": ENTRY_NAME,
            "main_sha256": hashlib.sha256(data).hexdigest(),
            "main_bytes": len(data),
            "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
            "tar_bytes": len(tar_bytes),
            "base_main_sha256": base_sha,
            "injected_tail_bytes": tail,
            "subs": ledger,
            "params": {"thr": got["thr"],
                       "cap_milk": list(got["cap_milk"]),
                       "cap_other": list(got["cap_other"]),
                       "carpet": got["carpet"]},
            "compile_ok": True,
            "entry_last_callable": ENTRY_NAME,
            "host_captured": HOST_NAME,
            "roundtrip_identity_ok": True,
            "byte_identical_to_base": data == base_bytes,
        }
        (OUT_DIR / form / "build_manifest.json").write_text(
            json.dumps(form_manifest, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        manifest["forms"][form] = form_manifest
        print(form, form_manifest["main_sha256"][:16],
              form_manifest["main_bytes"], "tail", tail,
              "params", form_manifest["params"], flush=True)
    (EVID_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_manifest.json", flush=True)


if __name__ == "__main__":
    main()
