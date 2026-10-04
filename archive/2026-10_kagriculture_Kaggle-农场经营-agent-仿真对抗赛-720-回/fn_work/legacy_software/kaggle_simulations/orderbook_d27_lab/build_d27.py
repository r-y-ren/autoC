# -*- coding: utf-8 -*-
"""build_d27：d27 实验室构建线（判决先行·不发射）。

责任口径（用户裁决 2026-09-29：d27 挂量墙卫生 + 日新高簇补全实验，只判决不
发射）：构建底=orderbook_r44_a/main.py（A 件字节）**零改动读入**，尾块注入
实验层（沿 orderbook_l1_derivative/append_layer_s_block 与 r45
append_advance_stack_block 形态）：块首捕获宿主末 callable（_D27_HOST=A 件
_dayhigh_agent），块尾末函数=_d27_agent（官方 last-callable 入口）。

四形态（消融矩阵）：
- placebo：纯注入恒等（捕获+透传，无任何后处理）——安慰剂臂；
- x1：仅 d27 挂量墙卫生（layer_x1）；
- x2：仅日新高簇补全（layer_x2）；
- x12：x2 内层追加、x1 外层卫生（tetsutani 928/948 追加在内、950-953 槽位
  卫生在外的嵌套序；X2 的 already 扣减在挂单表原样上计算=928 同口径）。

校验（fail-closed 不产出）：①注入后 compile ②exec 装载后末 callable=
_d27_agent（官方入口语义）③基座字节逐字前缀恒等 ④placebo 无后处理调用。
只写 orderbook_d27_lab/（构建产物 build/<form>/main.py + evidence/）。
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
BASE_MAIN = KSIM_DIR / "orderbook_r44_a" / "main.py"
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_d27_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("b387307fc12e26107c58ee604146fc621099ce88124fa0876fdd7"
                     "cef28300bd9")
SENTINEL = '"""d27 lab 实验尾块'
ENTRY_NAME = "_d27_agent"
CAPTURE_SRC = ("_D27_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"          # 基座尾与块首之间恰两个空行（layer S/r45 先例）

# 形态→层应用序（内层先应用；x12=tetsutani 嵌套序：追加在内、卫生在外）
FORMS = {
    "placebo": [],
    "x1": ["x1"],
    "x2": ["x2"],
    "x12": ["x2", "x1"],
}
LAYER_FILES = {"x1": "layer_x1.py", "x2": "layer_x2.py"}
LAYER_LABELS = {
    "x1": "件 X1=d27 挂量墙卫生（step>=624 同拍内死单清理/超库存 clamp/"
          "同品碎单并最早槽；零跨拍挪量）",
    "x2": "件 X2=日新高簇补全（tetsutani step928/948 语义差：父链在卖残量"
          "变现/投射仓基（当日 PICKUP 跳过）/追加单并首单 qty>0 口径）",
}

SHARED_SRC = '''
# ---- 共享段：宿主调用（元数自适应）+ 投射仓（同拍单位动作后） ----
def _xd7_call(observation, configuration):
    """宿主调用（A 件 _dayhigh_agent 双形态兼容；layer S 先例口径）。"""
    try:
        _sig = inspect.signature(_D27_HOST)
        try:
            _sig.bind(observation, configuration)
            return _D27_HOST(observation, configuration)
        except TypeError:
            return _D27_HOST(observation)
    except Exception:
        try:
            return _D27_HOST(observation, configuration)
        except TypeError:
            return _D27_HOST(observation)


def _xd7_projected(observation, action):
    """投射仓=本拍单位动作后、市场成交前的仓（基座 Chassis._projected_shed
    同源调用：PICKUP 减、DROP/PLACE 非动物结构加至仓容；失败回退裸 shed）。"""
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
        "    \"\"\"d27 实验入口（官方 last-callable）：宿主动作→实验层后处理。\"\"\"\n"
        "    action = _xd7_call(observation, configuration)\n"
        "%s%s"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_D27_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _D27_ENTRY_TMP\n"
        "del _D27_ENTRY_TMP\n" % (ENTRY_NAME, reset_block, posts,
                                  ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                  ENTRY_NAME))


def build_block(layers):
    """实验尾块组装（layers=应用序，内层在前）。"""
    parts = [SENTINEL + "（d27 挂量墙卫生 + 日新高簇补全实验层）\n"
             "构建底=orderbook_r44_a/main.py 零改动（逐字前缀恒等）；宿主=块首\n"
             "捕获之 A 件末 callable；纯同拍后处理，零跨拍挪量（R23/R26 红线）。\n"
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
        compile(injected, "<d27:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: 注入后源语法不通过: %r" % (form, exc))
    # ---- 校验②装载后末 callable=入口 ----
    ns = {}
    try:
        exec(compile(injected, "<d27:%s>" % form, "exec"), ns)
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


def main():
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（A 件字节漂移）：%s" % base_sha)
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
        "append_only_prefix_identical": True,
        "sentinel": SENTINEL,
        "entry": ENTRY_NAME,
        "layers": {k: LAYER_LABELS[k] for k in LAYER_FILES},
        "form_layer_order": {f: list(v) for f, v in FORMS.items()},
        "scope_notes": {
            "x1_window": "step>=624 全程（同拍内整理；终局 718 清算输出"
                         "结构性卫生不变：逐品单条正量实存挂单，无碎单/"
                         "无超库存/无死单——R29 终局清算器零触碰实测在案）",
            "x2_window": "全程（日新高簇语义补齐；同拍追加族）",
            "cross_tick": "零跨拍挪量（禁区红线 R23/R26）",
            "race_state_sync": "step928/948 的 _RACE_STATE prev_action 回写"
                               "守卫未补（防非触发拍级联足迹；残留语义差在"
                               "报告列明）",
        },
        "forms": {},
    }
    for form in FORMS:
        injected = build_form(form, base_src)
        data = injected.encode("utf-8")
        if not data.startswith(base_bytes):
            raise RuntimeError("校验④红 %s: 基座字节前缀不恒等" % form)
        out = OUT_DIR / form / "main.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        manifest["forms"][form] = {
            "main": str(out),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "injected_tail_bytes": len(data) - len(base_bytes),
            "layers": FORMS[form],
            "compile_ok": True,
            "entry_last_callable": ENTRY_NAME,
        }
        print(form, manifest["forms"][form]["sha256"][:16],
              manifest["forms"][form]["bytes"], flush=True)
    (EVID_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_manifest.json", flush=True)


if __name__ == "__main__":
    main()
