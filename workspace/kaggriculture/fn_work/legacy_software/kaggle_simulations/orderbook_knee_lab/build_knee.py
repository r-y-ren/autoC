# -*- coding: utf-8 -*-
"""build_knee：价格膝点量门变体构建线（基底=h1 件，判决先行·不发射不提交）。

构建底=orderbook_strongest_lab/build/h1/main.py（sha 76b5f842…）**零改动读入**，
尾块注入实验层（沿 build_strongest append 先例）：块首捕获宿主末 callable
（_KG_HOST=h1 件 _hs_agent），块尾末函数=_kg_agent（官方 last-callable 入口）。

两变体（X=判决标定初值/次档）：
- knee_x10：膝点量门步帽 X=10 件；
- knee_x20：膝点量门步帽 X=20 件。
两变体仅 `_KG_PARAMS["step_cap"]` 一处差异（文本占位 __KG_STEP_CAP__ 注入）。

校验（fail-closed 不产出）：①注入后 compile ②exec 装载后末 callable=_kg_agent
③基座（h1）字节逐字前缀恒等 ④块首捕获=_hs_agent ⑤step_cap 与形态一致。
另产 submission.tar.gz + build_manifest（供四门门禁重定向复用）。
只写 orderbook_knee_lab/。
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
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_knee_lab_manifest/1.0"

H1_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764"
                   "974b22f337")
SENTINEL = '"""strongest knee 实验尾块'
ENTRY_NAME = "_kg_agent"
HOST_NAME = "_hs_agent"
CAPTURE_SRC = ("_KG_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"          # 基座尾与块首之间恰两个空行（build_strongest 先例）
LAYER_FILE = "knee_layer.py"
STEP_CAP_TOKEN = "__KG_STEP_CAP__"

FORMS = {"knee_x10": 10, "knee_x20": 20}
LAYER_LABEL = ("件 KG=价格膝点量门（谷底三品 FERTILIZER/MILK/WOOL 本步 SELL "
               "单量按 quote<0.7×base 截留至 min(沈存30%,步帽X)；只减不挪、"
               "零跨拍、磁带 blob 零触碰、终局清算窗 712-718 不截留、异常回退"
               "原动作）")


def _entry_src():
    """入口生成：宿主动作→膝点量门后处理；step==0 复位台账。"""
    return (
        "def %s(observation, configuration=None):\n"
        "    \"\"\"knee 量门实验入口（官方 last-callable）：宿主动作→膝点量门"
        "后处理。\"\"\"\n"
        "    action = _KG_HOST(observation, configuration)\n"
        "    try:\n"
        "        if int(_kg_get(observation, 'step', 0) or 0) == 0:\n"
        "            _kg_reset()\n"
        "    except Exception:\n"
        "        pass\n"
        "    action = _kg_post(observation, action)\n"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_KG_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _KG_ENTRY_TMP\n"
        "del _KG_ENTRY_TMP\n" % (ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                 ENTRY_NAME, ENTRY_NAME))


def build_block(step_cap):
    """实验尾块组装（膝点量门层 + 入口）。"""
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    if STEP_CAP_TOKEN not in layer_src:
        raise RuntimeError("knee_layer 缺占位 %s" % STEP_CAP_TOKEN)
    layer_src = layer_src.replace(STEP_CAP_TOKEN, str(int(step_cap)))
    parts = [SENTINEL + "（价格膝点量门 knee 层）\n"
             "构建底=orderbook_strongest_lab/build/h1/main.py 零改动（逐字前缀"
             "恒等）；宿主=块首捕获之 h1 件末 callable；纯同拍后处理，只减不挪、"
             "零跨拍挪量（R23/R26 红线）、磁带 blob 零触碰。\n"
             '"""\n'
             + CAPTURE_SRC + "\n\n"]
    parts.append(layer_src.strip("\n") + "\n\n")
    parts.append(_entry_src())
    return "".join(parts)


def build_form(form, step_cap, base_src):
    block = build_block(step_cap)
    injected = base_src + SEPARATOR + block
    # ---- 校验①语法 ----
    try:
        compile(injected, "<knee:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: 注入后源语法不通过: %r" % (form, exc))
    # ---- 校验②装载后末 callable=入口；④捕获=宿主；⑤参数一致 ----
    ns = {}
    try:
        exec(compile(injected, "<knee:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验②红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验②红 %s: 末 callable=%r 应为 %r"
                           % (form, got, ENTRY_NAME))
    if ns.get("_KG_HOST") is not ns.get(HOST_NAME):
        raise RuntimeError("校验④红 %s: 块首捕获非 %s" % (form, HOST_NAME))
    if int(ns.get("_KG_PARAMS", {}).get("step_cap", -1)) != int(step_cap):
        raise RuntimeError("校验⑤红 %s: step_cap 不符" % form)
    return injected


def _make_tar(main_bytes):
    """submission.tar.gz（成员恰 ['main.py']，供四门身份门）。"""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    return buf.getvalue()


def main():
    base_bytes = H1_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != H1_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（h1 件字节漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("构建底不以换行收尾（fail-closed）")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(H1_MAIN),
        "base_main_sha256": base_sha,
        "base_bytes": len(base_bytes),
        "append_only_prefix_identical": True,
        "sentinel": SENTINEL,
        "entry": ENTRY_NAME,
        "host": HOST_NAME,
        "layer": LAYER_LABEL,
        "forms": {},
    }
    for form, step_cap in FORMS.items():
        injected = build_form(form, step_cap, base_src)
        data = injected.encode("utf-8")
        tail = len(data) - len(base_bytes)
        if not data.startswith(base_bytes):
            raise RuntimeError("校验③红 %s: 基座字节前缀不恒等" % form)
        out = OUT_DIR / form / "main.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        tar_bytes = _make_tar(data)
        (OUT_DIR / form / "submission.tar.gz").write_bytes(tar_bytes)
        ns_probe = {}
        exec(compile(injected, "<probe:%s>" % form, "exec"), ns_probe)
        form_manifest = {
            "form": form,
            "entry": ENTRY_NAME,
            "main_sha256": hashlib.sha256(data).hexdigest(),
            "main_bytes": len(data),
            "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
            "tar_bytes": len(tar_bytes),
            "base_main_sha256": base_sha,
            "injected_tail_bytes": tail,
            "params": {k: (list(v) if isinstance(v, tuple) else v)
                       for k, v in ns_probe.get("_KG_PARAMS", {}).items()},
            "compile_ok": True,
            "entry_last_callable": ENTRY_NAME,
            "append_only_prefix_identical": True,
            "byte_identical_to_h1": data == base_bytes,
        }
        (OUT_DIR / form / "build_manifest.json").write_text(
            json.dumps(form_manifest, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        manifest["forms"][form] = form_manifest
        print(form, form_manifest["main_sha256"][:16],
              form_manifest["main_bytes"], "tail", tail, flush=True)
    (EVID_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_manifest.json", flush=True)


if __name__ == "__main__":
    main()
