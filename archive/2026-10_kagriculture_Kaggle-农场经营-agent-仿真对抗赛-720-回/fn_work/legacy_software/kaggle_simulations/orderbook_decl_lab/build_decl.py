# -*- coding: utf-8 -*-
"""build_decl：申报量-持货匹配变体构建线（基底=oc_c3 件，判决先行·不发射不提交）。

构建底=orderbook_oppcond_lab/build/oc_c3/main.py（sha 3f8b57fd…）**零改动读入**，
尾块注入实验层（沿 build_knee append 先例）：块首捕获宿主末 callable
（_DL_HOST=oc_c3 件 _hs_agent），块尾末函数=_dl_agent（官方 last-callable 入口）。

两变体：
- decl_m：decl 层（申报量=min(申报,投射可卖沈存)，无条件裁）；
- decl_restock：decl+补链（该品未来有补货→不动，无补货才裁）。
两变体仅 `_DL_PARAMS["mode"]` 一处差异（文本占位 __DL_MODE__ 注入）。

校验（fail-closed 不产出）：①注入后 compile ②exec 装载后末 callable=_dl_agent
③基座（oc_c3）字节逐字前缀恒等 ④块首捕获=_hs_agent ⑤mode 与形态一致。
另产 submission.tar.gz + build_manifest（供四门门禁复用）。
只写 orderbook_decl_lab/。
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
OC_MAIN = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_decl_lab_manifest/1.0"

OC_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d39"
                   "ba9bd23d")
SENTINEL = '"""decl match 实验尾块'
ENTRY_NAME = "_dl_agent"
HOST_NAME = "_hs_agent"
CAPTURE_SRC = ("_DL_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"          # 基座尾与块首之间恰两个空行（build_knee 先例）
LAYER_FILE = "decl_layer.py"
MODE_TOKEN = "__DL_MODE__"

FORMS = {"decl_m": 0, "decl_restock": 1}
LAYER_LABEL = ("件 DL=申报量-持货匹配（本步 SELL 单 qty=min(申报,投射可卖沈存)，"
               "基座 _clamp_sells 同序口径：_xd7_projected+同拍更早入仓买腿；"
               "decl_m 无条件裁 / decl_restock 补链保守——未来有补货不动、无补货"
               "才裁；零跨拍、只裁申报不动时点、不改单集合与槽位、磁带 blob "
               "零触碰、异常回退原动作）")


def _entry_src():
    """入口生成：宿主动作→申报量裁剪后处理；step==0 复位台账。"""
    return (
        "def %s(observation, configuration=None):\n"
        "    \"\"\"decl 匹配实验入口（官方 last-callable）：宿主动作→申报量"
        "裁到可交付量。\"\"\"\n"
        "    action = _DL_HOST(observation, configuration)\n"
        "    try:\n"
        "        if int(_dl_get(observation, 'step', 0) or 0) == 0:\n"
        "            _dl_reset()\n"
        "    except Exception:\n"
        "        pass\n"
        "    action = _dl_post(observation, action)\n"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_DL_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _DL_ENTRY_TMP\n"
        "del _DL_ENTRY_TMP\n" % (ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                 ENTRY_NAME, ENTRY_NAME))


def build_block(mode):
    """实验尾块组装（decl 层 + 入口）。"""
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    if MODE_TOKEN not in layer_src:
        raise RuntimeError("decl_layer 缺占位 %s" % MODE_TOKEN)
    layer_src = layer_src.replace(MODE_TOKEN, str(int(mode)))
    parts = [SENTINEL + "（申报量-持货匹配 decl 层）\n"
             "构建底=orderbook_oppcond_lab/build/oc_c3/main.py 零改动（逐字前缀"
             "恒等）；宿主=块首捕获之 oc_c3 件末 callable；纯同拍后处理，只裁申报、"
             "零跨拍（R23/R26 红线）、磁带 blob 零触碰。\n"
             '"""\n'
             + CAPTURE_SRC + "\n\n"]
    parts.append(layer_src.strip("\n") + "\n\n")
    parts.append(_entry_src())
    return "".join(parts)


def build_form(form, mode, base_src):
    block = build_block(mode)
    injected = base_src + SEPARATOR + block
    # ---- 校验①语法 ----
    try:
        compile(injected, "<decl:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: 注入后源语法不通过: %r" % (form, exc))
    # ---- 校验②装载后末 callable=入口；④捕获=宿主；⑤mode 一致 ----
    ns = {}
    try:
        exec(compile(injected, "<decl:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验②红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验②红 %s: 末 callable=%r 应为 %r"
                           % (form, got, ENTRY_NAME))
    if ns.get("_DL_HOST") is not ns.get(HOST_NAME):
        raise RuntimeError("校验④红 %s: 块首捕获非 %s" % (form, HOST_NAME))
    if int(ns.get("_DL_PARAMS", {}).get("mode", -1)) != int(mode):
        raise RuntimeError("校验⑤红 %s: mode 不符" % form)
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
    base_bytes = OC_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != OC_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（oc_c3 件字节漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("构建底不以换行收尾（fail-closed）")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(OC_MAIN),
        "base_main_sha256": base_sha,
        "base_bytes": len(base_bytes),
        "append_only_prefix_identical": True,
        "sentinel": SENTINEL,
        "entry": ENTRY_NAME,
        "host": HOST_NAME,
        "layer": LAYER_LABEL,
        "forms": {},
    }
    for form, mode in FORMS.items():
        injected = build_form(form, mode, base_src)
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
                       for k, v in ns_probe.get("_DL_PARAMS", {}).items()},
            "compile_ok": True,
            "entry_last_callable": ENTRY_NAME,
            "append_only_prefix_identical": True,
            "byte_identical_to_oc_c3": data == base_bytes,
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
