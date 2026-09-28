# -*- coding: utf-8 -*-
"""build_iter1：组 I 增量移植构建线（基底=最强版 H1，判决先行·不发射·不线上提交）。

责任口径（任务）：把横测发现的两个不同家族机制移植到最强版 H1 上做判决实验。
构建底=orderbook_strongest_lab/build/h1/main.py（H1 件字节，sha 76b5f842…）
**零改动读入**，尾块注入形态沿 append_layer_s_block/build_strongest 先例：
块首捕获宿主末 callable（_IX_HOST=H1 件 _hs_agent），块尾末函数=_ix_agent
（官方 last-callable 入口）。

四形态（判决矩阵）：
- h1_base：H1 原样重打包（字节恒等，无注入；原样对照）；
- i1：H1 + I1（mooman e087 CXTB 番茄晚市放量门语义移植）；
- i2：H1 + I2（statma ca25 HERD 报价门控卖序 + COURIER 当日可送品优先出
  精简移植；产线换畜种=磁带手术级，不可移植，不硬做）；
- i12：H1 + I1 + I2（组合消融）。

校验（fail-closed 不产出）：①注入后 compile ②exec 装载后末 callable=_ix_agent
③基座字节逐字前缀恒等 ④h1_base 字节恒等。另产 submission.tar.gz + build_manifest
（供四门 gate_launch_fourgate_l1 重定向复用）。只写 orderbook_iter1_lab/。
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
BASE_MAIN = (KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_iter1_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb676"
                     "4974b22f337")
SENTINEL = '"""iter1 实验尾块'
ENTRY_NAME = "_ix_agent"
CAPTURE_SRC = ("_IX_HOST = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"          # 基座尾与块首之间恰两个空行（layer S/r45/strongest 先例）

# 形态→层应用序（内层先应用；i12=i1 内层、i2 外层）
FORMS = {
    "i1": ["i1"],
    "i2": ["i2"],
    "i12": ["i1", "i2"],
}
IDENTITY_FORM = "h1_base"   # 字节恒等形态（无注入尾块）
LAYER_FILES = {"i1": "layer_i1.py", "i2": "layer_i2.py"}
LAYER_LABELS = {
    "i1": "件 I1=番茄晚市放量门（e087 CXTB 语义移植：公开面对手在田番茄 yield"
          "之和+市场库存+排水节奏→对手下批供给压力投影；d26-29 按门放量/挂起，"
          "节奏 ≤20 单元/日；阈值取紧档 9000/80=112.5 每单元；step>=712 终局清仓）",
    "i2": "件 I2=HERD 报价门控卖序（羊毛/奶 ≥150+店铺结构门开→计划外卖量按源件"
          "卖序放头）+ COURIER 当日可送品优先出（hour>=12 当日入仓 COURIER 品目"
          "首槽/加量挪头）；产线换畜种=磁带手术级不可移植（如实报，不硬做）",
}

# 共享段：宿主调用（元数自适应）+ 投射仓（同拍单位动作后）。
# 函数名 _ix_call/_ix_projected 与复制层 layer_i1/i2 引用保持一致。
SHARED_SRC = '''
# ---- 共享段：宿主调用（元数自适应）+ 投射仓（同拍单位动作后） ----
def _ix_call(observation, configuration):
    """宿主调用（H1 件 _hs_agent 双形态兼容；不依赖 inspect）。"""
    try:
        return _IX_HOST(observation, configuration)
    except TypeError:
        return _IX_HOST(observation)


def _ix_projected(observation, action):
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
        "    \"\"\"iter1 实验入口（官方 last-callable）：宿主动作→实验层后处理。\"\"\"\n"
        "    action = _ix_call(observation, configuration)\n"
        "%s%s"
        "    return action\n"
        "\n"
        "# ---- 入口归一（末函数=%s） ----\n"
        "_IX_ENTRY_TMP = %s\n"
        "del %s\n"
        "%s = _IX_ENTRY_TMP\n"
        "del _IX_ENTRY_TMP\n" % (ENTRY_NAME, reset_block, posts,
                                 ENTRY_NAME, ENTRY_NAME, ENTRY_NAME,
                                 ENTRY_NAME))


def build_block(layers):
    """实验尾块组装（layers=应用序，内层在前）。"""
    parts = [SENTINEL + "（番茄晚市放量门 + HERD/COURIER 订单层精简移植实验层）\n"
             "构建底=orderbook_strongest_lab/build/h1/main.py 零改动"
             "（逐字前缀恒等）；宿主=块首捕获之 H1 件末 callable；纯同拍后处理，"
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
        compile(injected, "<iter1:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: 注入后源语法不通过: %r" % (form, exc))
    # ---- 校验②装载后末 callable=入口 ----
    ns = {}
    try:
        exec(compile(injected, "<iter1:%s>" % form, "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验②红 %s: exec 失败: %r" % (form, exc))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        got = loaded[-1].__name__ if loaded else None
        raise RuntimeError("校验②红 %s: 末 callable=%r 应为 %r"
                           % (form, got, ENTRY_NAME))
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
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（H1 件字节漂移）：%s" % base_sha)
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
        "not_ported": {
            "herd_species_swap":
                "HERD 产线换畜种（BUILD_COOP→BUILD_PASTURE、BUY_ANIMAL/PICKUP/"
                "PLACE GOOSE→SHEEP/COW 指令改写）=磁带手术级，订单/守卫层不可表达"
                "→不可移植，不硬做（H1 内层已含同源 V9_HERD 全层）",
            "courier_walk_drop":
                "COURIER 走位送货（worker 路径规划+DROP 时机）=物理层→不可移植；"
                "仅移植其市场面（当日入仓品首槽/加量挪头）",
        },
        "scope_notes": {
            "i1_window": "day 26..29（step 624..719）；step>=712 终局清仓",
            "i1_trigger": "今日投影释放均价 >= 112.5（源件紧档 9000/80）→放量，"
                          "否则挂起；对手压力不可读→零足迹",
            "i2_window": "全程；HERD 门=羊毛/奶 ≥150+店铺结构；COURIER 面="
                         "hour>=12 且 step<718 当日入仓 COURIER 品目",
            "cross_tick": "零跨拍挪量（禁区红线 R23/R26）",
        },
        "forms": {},
    }
    for form in [IDENTITY_FORM] + list(FORMS):
        if form == IDENTITY_FORM:
            data = base_bytes                 # H1 原样重打包（字节恒等）
            tail = 0
            layers = []
            entry = "H1_native_last_callable"
        else:
            injected = build_form(form, base_src)
            data = injected.encode("utf-8")
            tail = len(data) - len(base_bytes)
            layers = FORMS[form]
            entry = ENTRY_NAME
        if not data.startswith(base_bytes):
            raise RuntimeError("校验③红 %s: 基座字节前缀不恒等" % form)
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
            "byte_identical_to_h1_base": data == base_bytes,
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
