# -*- coding: utf-8 -*-
"""build_strongest：最强版本构建线（base=H haodou V82 采纳件，判决先行·不发射）。

责任口径（任务）：把战场上学到的最强组件合成为候选。构建底=orderbook_haodou_adopt/
submission.tar.gz 内 main.py（H 件字节，sha bdb82117…）**零改动读入**，尾块注入
实验层（沿 build_d27 append_layer_s_block 形态）：块首捕获宿主末 callable
（_H_HOST=H 件 pet_any_demand_agent），块尾末函数=_hs_agent（官方 last-callable 入口）。

三形态（消融矩阵）：
- h0：H 原样重打包（纯注入恒等：捕获+透传，无任何后处理）——对照恒等；
- h1：H + X1（d27 挂量墙卫生；主推形态）；
- h12：H + X1 + X2（X2 日新高补全内层追加、X1 卫生外层；消融）。

校验（fail-closed 不产出）：①注入后 compile ②exec 装载后末 callable=_hs_agent
③基座字节逐字前缀恒等 ④h0 无后处理调用。另产 submission.tar.gz + build_manifest
（供四门 gate_launch_fourgate_l1 重定向复用）。只写 orderbook_strongest_lab/。
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
ADOPT_DIR = KSIM_DIR / "orderbook_haodou_adopt"
BASE_TAR = ADOPT_DIR / "submission.tar.gz"
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_strongest_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("bdb821178ca73c0e8480f06c1887e20921caea0438398a5edb68bd9"
                     "ad20b1de8")
SENTINEL = '"""strongest lab 实验尾块'
ENTRY_NAME = "_hs_agent"
CAPTURE_SRC = ("_H_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"          # 基座尾与块首之间恰两个空行（layer S/r45 先例）

# 形态→层应用序（内层先应用；h12=tetsutani 嵌套序：追加在内、卫生在外）
# h0=H 原样重打包（字节恒等，无注入；对照恒等基座）；placebo=纯注入恒等
# （捕获+透传，证尾块注入零足迹）；h1/h12=注入实验层。
FORMS = {
    "placebo": [],
    "h1": ["x1"],
    "h12": ["x2", "x1"],
}
IDENTITY_FORM = "h0"        # 字节恒等形态（无注入尾块）
LAYER_FILES = {"x1": "layer_x1.py", "x2": "layer_x2.py"}
LAYER_LABELS = {
    "x1": "件 X1=d27 挂量墙卫生（step>=624 同拍内死单清理/超库存 clamp/"
          "同品碎单并最早槽；零跨拍挪量）",
    "x2": "件 X2=日新高簇补全（tetsutani step928/948 语义差：父链在卖残量"
          "变现/投射仓基（当日 PICKUP 跳过）/追加单并首单 qty>0 口径）",
}

# 共享段：宿主调用（不依赖 inspect；元数自适应）+ 投射仓（同拍单位动作后）。
# 函数名 _xd7_call/_xd7_projected 与复制层 layer_x1/x2 引用保持一致。
SHARED_SRC = '''
# ---- 共享段：宿主调用（元数自适应）+ 投射仓（同拍单位动作后） ----
def _xd7_call(observation, configuration):
    """宿主调用（H 件 pet_any_demand_agent 双形态兼容；不依赖 inspect）。"""
    try:
        return _H_HOST(observation, configuration)
    except TypeError:
        return _H_HOST(observation)


def _xd7_projected(observation, action):
    """投射仓=本拍单位动作后、市场成交前的仓（基座 Chassis._projected_shed
    同源调用；失败回退裸 shed）。"""
    try:
        player = int((observation or {}).get("player", 0))
    except Exception:
        player = 0
    try:
        view = _View(observation, player, _IMPL.chassis.cfg)
        proj = _IMPL.chassis._projected_shed(action, view)
        return {k: int(v) for k, v in dict(proj).items()}
    except Exception:
        try:
            shed = ((observation or {}).get("private") or {}).get("shed") or {}
            return {k: int(v) for k, v in dict(shed).items()}
        except Exception:
            return {}
'''


def _entry_src(layers):
    """入口生成：宿主动作→逐层后处理（内层先）；step==0 复位各层台账。"""
    resets = "".join("            _%s_reset()\n" % ln for ln in layers)
    posts = "".join("    action = _%s_post(observation, action)\n" % ln
                    for ln in layers)
    reset_block = ""
    if layers:
        reset_block = (
            "    try:\n"
            "        if int((observation or {}).get('step', 0)) == 0:\n"
            "%s"
            "    except Exception:\n"
            "        pass\n" % resets)
    return (
        "def %s(observation, configuration=None):\n"
        "    \"\"\"strongest 实验入口（官方 last-callable）：宿主动作→实验层后处理。\"\"\"\n"
        "    action = _xd7_call(observation, configuration)\n"
        "%s%s"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_HS_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _HS_ENTRY_TMP\n"
        "del _HS_ENTRY_TMP\n" % (ENTRY_NAME, reset_block, posts,
                                 ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                 ENTRY_NAME))


def build_block(layers):
    """实验尾块组装（layers=应用序，内层在前）。"""
    parts = [SENTINEL + "（d27 挂量墙卫生 + 日新高簇补全实验层）\n"
             "构建底=orderbook_haodou_adopt/submission.tar.gz 内 main.py 零改动"
             "（逐字前缀恒等）；宿主=块首捕获之 H 件末 callable；纯同拍后处理，"
             "零跨拍挪量（R23/R26 红线）。\n"
             '"""\n'
             + CAPTURE_SRC + "\n\n"]
    parts.append(SHARED_SRC.strip("\n") + "\n\n")
    for name in layers:
        src = (MODULE_DIR / LAYER_FILES[name]).read_text(encoding="utf-8")
        parts.append(src.strip("\n") + "\n\n")
    parts.append(_entry_src(layers))
    return "".join(parts)


def build_form(form, base_src):
    layers = FORMS[form]
    block = build_block(layers)
    injected = base_src + SEPARATOR + block
    # ---- 校验①语法 ----
    try:
        compile(injected, "<strongest:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: 注入后源语法不通过: %r" % (form, exc))
    # ---- 校验②装载后末 callable=入口 ----
    ns = {}
    try:
        exec(compile(injected, "<strongest:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验②红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验②红 %s: 末 callable=%r 应为 %r"
                           % (form, got, ENTRY_NAME))
    # ---- 校验③ placebo 无后处理 ----
    if form == "placebo" and ("_x1_post(" in injected.split(SENTINEL, 1)[1]
                              or "_x2_post(" in injected.split(SENTINEL, 1)[1]):
        raise RuntimeError("校验③红 placebo: 恒等件不得含后处理调用")
    return injected


def _make_tar(main_bytes):
    """submission.tar.gz（成员恰 ['main.py']，供四门身份门）。"""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    return buf.getvalue()


def _read_base_from_tar():
    with tarfile.open(fileobj=io.BytesIO(BASE_TAR.read_bytes()),
                      mode="r:gz") as tar:
        member = tar.extractfile("main.py")
        if member is None:
            raise RuntimeError("submission.tar.gz 内无 main.py")
        return member.read()


def main():
    base_bytes = _read_base_from_tar()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（H 件字节漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("构建底不以换行收尾（fail-closed）")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_tar": str(BASE_TAR),
        "base_main": "submission.tar.gz::main.py",
        "base_main_sha256": base_sha,
        "base_bytes": len(base_bytes),
        "append_only_prefix_identical": True,
        "sentinel": SENTINEL,
        "entry": ENTRY_NAME,
        "layers": {k: LAYER_LABELS[k] for k in LAYER_FILES},
        "form_layer_order": {f: list(v) for f, v in FORMS.items()},
        "scope_notes": {
            "x1_window": "step>=624 全程（同拍内整理；超库存幻影死单清理）",
            "x2_window": "全程（日新高簇语义补齐；同拍追加族）",
            "cross_tick": "零跨拍挪量（禁区红线 R23/R26）",
        },
        "forms": {},
    }
    for form in [IDENTITY_FORM] + list(FORMS):
        if form == IDENTITY_FORM:
            data = base_bytes                 # H 原样重打包（字节恒等）
            tail = 0
            layers = []
            entry = "H_native_last_callable"
        else:
            injected = build_form(form, base_src)
            data = injected.encode("utf-8")
            tail = len(data) - len(base_bytes)
            layers = FORMS[form]
            entry = ENTRY_NAME
        if not data.startswith(base_bytes):
            raise RuntimeError("校验④红 %s: 基座字节前缀不恒等" % form)
        out = OUT_DIR / form / "main.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        tar_bytes = _make_tar(data)
        (OUT_DIR / form / "submission.tar.gz").write_bytes(tar_bytes)
        form_manifest = {
            "form": form,
            "entry": entry,
            "main_sha256": hashlib.sha256(data).hexdigest(),
            "main_bytes": len(data),
            "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
            "tar_bytes": len(tar_bytes),
            "base_main_sha256": base_sha,
            "injected_tail_bytes": tail,
            "layers": layers,
            "compile_ok": True,
            "entry_last_callable": entry,
            "append_only_prefix_identical": True,
            "byte_identical_to_H": data == base_bytes,
        }
        (OUT_DIR / form / "build_manifest.json").write_text(
            json.dumps(form_manifest, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        manifest["forms"][form] = form_manifest
        print(form, form_manifest["main_sha256"][:16], form_manifest["main_bytes"],
              "tail", tail, flush=True)
    (EVID_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_manifest.json", flush=True)


if __name__ == "__main__":
    main()
