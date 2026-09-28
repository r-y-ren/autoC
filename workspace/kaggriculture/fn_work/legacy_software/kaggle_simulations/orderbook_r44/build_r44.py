# -*- coding: utf-8 -*-
"""r44 构建线（R27）：三形态 A/B/AB 注入构建——r40 字节零改动读入→按 form 注入
尾块链→diff 审计→确定性打包+manifest+sha 链。

契约（fn_docs/hybrid/responsibility.md【R27 增补】）：
- build_r44_variant(base_main_path, form, out_dir)：form∈{A,B,AB}；AB=dayhigh
  内层+glutgate 外层（门作用于含追加单的最终列表）；审计白名单外/双跑不一致
  即抛（不产出）。
- append_dayhigh_block(main_src)：quote_context 源+dayhigh 层源按序拼接进候选
  尾块（块首捕获宿主末 callable=_DH_HOST；块尾封口 _dayhigh_agent 成新末
  callable）；三道写入前防线沿 append_layer_s_block 先例（拒原件/判重/纯净副本）。
- append_glutgate_block(main_src)：同形态，块嵌 _glutgate_agent（捕获 _GG_HOST）；
  AB 形态 gate 在 dayhigh 之外层。

约束：stdlib-only；构建失败即抛（fail-closed）；确定性双跑；层文件只按文本
拼接（不 import 层实现）；r40 基座/在飞件零改动。
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent

SCHEMA = "orderbook_r44_manifest/1.0"

# 描述文案（R27 跨批契约原文，逐形态）
DESCRIPTIONS = {
    "A": "public derivative with day-high realization",
    "B": "public derivative with glut gate",
    "AB": "public derivative with day-high realization and glut gate",
}

# 形态→产物目录名（调用方按此给 out_dir；本函数只落 out_dir 本身）
FORM_DIRS = {
    "A": "orderbook_r44_a",
    "B": "orderbook_r44_b",
    "AB": "orderbook_r44_ab",
}

# sha 链：…→r34a→r40→r44_*。上游谱系常量沿 build_r43.BASE_CHAIN 同源登记；
# r40 节点=构建底实测 sha（真 r40 即下值；合成基座如实记其实测值，不冒充）。
UPSTREAM_CHAIN = {
    "a16e0e9b": "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab",
    "r34a": "51fc19dba2d0bcbf2d0a3720c26ff318541a0e6ce5800873bc863f612451aa5b",
    "r37": "23a513f903317e4d6133aea87e5205bd75cab057090e92c162e5c3be8e32707f",
}
FLYING_R40_SHA256 = ("4ce951f088740e0b3d4366dbf95f8bb225817b0417bbb2fcea"
                     "6292a559ee9ea8")

_SEP = "\n\n"  # 追加分隔（append_layer_s_block 先例：源各以恰一换行收尾→两空行）

# 块 sentinel（判重/链序判别；只出现在生成块首行）
_DH_MARKER = "# r44-tail-block:dayhigh"
_GG_MARKER = "# r44-tail-block:glutgate"

# 块首宿主捕获（约束：先于块内一切 def 执行才捕获到宿主末 callable；双下划线
# 模块样板名排除，layer S _CXS_HOST 先例同款公式）
_DH_HEAD = (
    _DH_MARKER + "\n"
    "# 块首宿主捕获（约束：先于块内一切 def 执行）\n"
    "_DH_LAST = [v for k, v in list(globals().items())"
    " if callable(v) and not (k.startswith('__') and k.endswith('__'))]\n"
    "_DH_HOST = _DH_LAST[-1] if _DH_LAST else None\n"
)
_GG_HEAD = (
    _GG_MARKER + "\n"
    "# 块首宿主捕获（约束：先于块内一切 def 执行）\n"
    "_GG_LAST = [v for k, v in list(globals().items())"
    " if callable(v) and not (k.startswith('__') and k.endswith('__'))]\n"
    "_GG_HOST = _GG_LAST[-1] if _GG_LAST else None\n"
)

# 块尾封口（约束：官方 get_last_callable 取 globals 末 callable=本层入口——del+
# 回绑使入口名重插 dict 末位，与层源内部 def 顺序无关）
_DH_SEAL = (
    "# 尾部封口（约束：globals 末 callable=_dayhigh_agent）\n"
    "_DH_ENTRY = _dayhigh_agent\ndel _dayhigh_agent\n"
    "_dayhigh_agent = _DH_ENTRY\n"
)
_GG_SEAL = (
    "# 尾部封口（约束：globals 末 callable=_glutgate_agent）\n"
    "_GG_ENTRY = _glutgate_agent\ndel _glutgate_agent\n"
    "_glutgate_agent = _GG_ENTRY\n"
)

# 磁带 blob 行锚（retape_sheep._BLOB_RE 同口径：_R108_DATA 字面量单行）
_TAPE_BLOB_RE = re.compile(r"^_R108_DATA=.*$", re.M)


def build_r44_variant(base_main_path, form, out_dir):
    """构建编排：r40 字节按 form∈{A,B,AB} 注入尾块链（AB=dayhigh 内层+glutgate
    外层）→diff 审计（改动仅限注入块、磁带五区零改动）→确定性打包
    submission.tar.gz+build_manifest.json+sha 链（…→r34a→r40→r44_*）。

    签名意图：输入: r40 main 路径+form+out_dir（调用方按 FORM_DIRS 给目录）/
    输出: r44_{form} main+tar+manifest+diff 审计 / 错误: 审计白名单外或双跑
    不一致即抛（不产出）。
    """
    # ---- 0. form 归一校验（A/B/AB）----
    if not isinstance(form, str):
        raise ValueError("form 非法: %r（仅 A/B/AB）" % (form,))
    norm = form.strip().upper()
    if norm not in DESCRIPTIONS:
        raise ValueError("form 非法: %r（仅 A/B/AB）" % (form,))

    # ---- 1. 基座零改动读入（r40 字节；构建前后在飞件 sha 恒等在审计复核）----
    base_path = Path(base_main_path)
    if not base_path.is_file():
        raise FileNotFoundError("构建底 main 不存在: %s" % base_path)
    base_bytes = base_path.read_bytes()
    base_text = base_bytes.decode("utf-8")
    base_sha = hashlib.sha256(base_bytes).hexdigest()

    # ---- 2. 注入尾块链（AB=dayhigh 内层、glutgate 外层——门作用于最终列表）----
    if norm == "A":
        injected = append_dayhigh_block(base_text)
        block_plan = ("dayhigh",)
    elif norm == "B":
        injected = append_glutgate_block(base_text)
        block_plan = ("glutgate",)
    else:  # AB
        injected = append_glutgate_block(append_dayhigh_block(base_text))
        block_plan = ("dayhigh", "glutgate")

    # ---- 3. diff 审计（独立复算期望注入字节，白名单=注入尾块）----
    # 约束：改动仅限注入块=产物恰=基座+（sep+块）链；块文本由层源独立复推
    # （不走 append_*，防注入器被污染）；磁带五区（磁带/路由/反克隆抢卖/卖单槽位
    # 重排/终局清仓）全在基座区，前缀逐字节恒等即逐区零改动，磁带 blob 另显式复核。
    q_src = (MODULE_DIR / "quote_context.py").read_text(encoding="utf-8")
    if not q_src.endswith("\n"):
        raise ValueError("quote_context.py 源不以换行收尾（fail-closed）")
    exp_parts = []
    block_meta = {}
    if "dayhigh" in block_plan:
        day_src = (MODULE_DIR / "dayhigh_layer.py").read_text(encoding="utf-8")
        if not day_src.endswith("\n"):
            raise ValueError("dayhigh_layer.py 源不以换行收尾（fail-closed）")
        exp_dh = _DH_HEAD + _SEP + q_src + _SEP + day_src + _SEP + _DH_SEAL
        exp_parts.append(exp_dh)
        block_meta["dayhigh"] = {
            "sha256": hashlib.sha256(exp_dh.encode("utf-8")).hexdigest(),
            "bytes": len(exp_dh.encode("utf-8")),
        }
    if "glutgate" in block_plan:
        gg_src = (MODULE_DIR / "glutgate_layer.py").read_text(encoding="utf-8")
        if not gg_src.endswith("\n"):
            raise ValueError("glutgate_layer.py 源不以换行收尾（fail-closed）")
        exp_gg = _GG_HEAD + _SEP + q_src + _SEP + gg_src + _SEP + _GG_SEAL
        exp_parts.append(exp_gg)
        block_meta["glutgate"] = {
            "sha256": hashlib.sha256(exp_gg.encode("utf-8")).hexdigest(),
            "bytes": len(exp_gg.encode("utf-8")),
        }
    expected = base_text + "".join(_SEP + part for part in exp_parts)
    if injected != expected:
        raise RuntimeError("审计白名单外：产物≠基座+注入尾块链（改动越出注入块）")
    if not injected.startswith(base_text):
        raise RuntimeError("审计白名单外：基座前缀被改动（非 append-only）")
    tail_bytes = len(injected.encode("utf-8")) - len(base_bytes)

    # 磁带五区零改动：磁带 blob（_R108_DATA 单行字面量）显式复核（无 blob 的
    # 合成基座记 null，不造假；前缀恒等已覆盖全域）
    m_base = _TAPE_BLOB_RE.search(base_text)
    m_out = _TAPE_BLOB_RE.search(injected)
    if m_base is None:
        tape_blob_sha = None
    else:
        if m_out is None or m_out.group(0) != m_base.group(0):
            raise RuntimeError("审计白名单外：磁带 blob 区被改动（磁带五区零改动破）")
        tape_blob_sha = hashlib.sha256(
            m_base.group(0).encode("utf-8")).hexdigest()

    # r40 在飞件零改动：构建前后基座文件 sha 恒等
    if hashlib.sha256(base_path.read_bytes()).hexdigest() != base_sha:
        raise RuntimeError("r40 在飞件被改动（基座文件构建前后 sha 不恒等）")

    audit = {
        "whitelist": ["tail_block_injection"],
        "blocks": list(block_plan),
        "append_only": True,
        "injected_tail_bytes": tail_bytes,
        "tape_five_zones_unchanged": True,
        "tape_blob_sha256": tape_blob_sha,
        "base_file_unchanged": True,
    }

    # ---- 4. 确定性打包（build_adopt.build_tar_bytes 真源复用；双跑逐字节）----
    try:
        from orderbook_2965_adopt import build_adopt as _ba  # noqa: WPS433
    except ImportError:  # 脚本态兜底（pack_r40 同款）
        _adopt = str(MODULE_DIR.parent / "orderbook_2965_adopt")
        if _adopt not in sys.path:
            sys.path.insert(0, _adopt)
        import build_adopt as _ba  # type: ignore
    main_bytes = injected.encode("utf-8")
    tar1 = _ba.build_tar_bytes(main_bytes)
    tar2 = _ba.build_tar_bytes(main_bytes)
    if tar1 != tar2 or hashlib.sha256(tar1).hexdigest() != \
            hashlib.sha256(tar2).hexdigest():
        raise RuntimeError("双跑不一致（确定性破坏），不产出（fail-closed）")
    import io
    import tarfile
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as tf:
        names = tf.getnames()
        inner = tf.extractfile("main.py").read() if "main.py" in names else None
    if names != ["main.py"] or inner != main_bytes:
        raise RuntimeError("tar 成员/内层 main 校验失败: %s" % (names,))

    # ---- 5. manifest（sha 链 …→r34a→r40→r44_*；描述文案按形态）----
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    tar_sha = hashlib.sha256(tar1).hexdigest()
    variant = "r44_" + norm.lower()
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%d"),
        "form": norm,
        "variant": variant,
        "description": DESCRIPTIONS[norm],
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": tar_sha,
        "tar_bytes": len(tar1),
        "tar_members": ["main.py"],
        "double_run_sha256": {"run1": tar_sha, "run2":
                              hashlib.sha256(tar2).hexdigest()},
        "base_main_sha256": base_sha,
        "base_matches_flying_r40": base_sha == FLYING_R40_SHA256,
        "base_sha_chain": dict(UPSTREAM_CHAIN, r40=base_sha, **{variant: main_sha}),
        "blocks": block_meta,
        "audit": audit,
        "complete": True,
    }

    # ---- 6. 落盘（全部校验过后才写；失败路径不产出）----
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    main_path = out / "main.py"
    tar_path = out / "submission.tar.gz"
    man_path = out / "build_manifest.json"
    main_path.write_bytes(main_bytes)
    tar_path.write_bytes(tar1)
    man_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")
    if hashlib.sha256(main_path.read_bytes()).hexdigest() != main_sha:
        raise RuntimeError("main sha 自证不符（落盘回读漂移）")

    return {
        "form": norm,
        "main_path": str(main_path),
        "tar_path": str(tar_path),
        "man_path": str(man_path),
        "main_sha256": main_sha,
        "tar_sha256": tar_sha,
        "audit": audit,
        "manifest": manifest,
    }


def append_dayhigh_block(main_src):
    """把 quote_context 源码+dayhigh_layer.py 源码按序拼接追加进候选尾块（同一
    命名空间；块首捕获宿主末 callable 常量 _DH_HOST；块尾封口 _dayhigh_agent 成
    新末 callable——语义照抄 append_layer_s_block 先例）。

    三道写入前防线沿先例（拒原件/判重/纯净副本）。签名意图：输入: 候选 main 源 /
    输出: 注入后 main 源 / 错误: 拒原件/重复注入即抛。
    """
    q_src = (MODULE_DIR / "quote_context.py").read_text(encoding="utf-8")
    day_src = (MODULE_DIR / "dayhigh_layer.py").read_text(encoding="utf-8")
    if not q_src.endswith("\n") or not day_src.endswith("\n"):
        raise ValueError("层源不以换行收尾，两空行分隔约定不成立（fail-closed）")
    block = _DH_HEAD + _SEP + q_src + _SEP + day_src + _SEP + _DH_SEAL

    # 防线一（拒原件）：原件/文件指代只读——输入须为候选 main 源文本（str）；
    # 本函数纯文本变换零写盘，基座原件永不被写（先例 main_path 指向原件即拒）。
    if not isinstance(main_src, str):
        raise ValueError(
            "refusing to inject: 输入非候选 main 源文本（原件/文件指代只读）: %s"
            % type(main_src).__name__)

    # 防线二（判重）：已含 dayhigh 尾块（sentinel/块字节）拒绝二次追加
    if _DH_MARKER in main_src or block in main_src:
        raise ValueError(
            "already injected: 目标候选已含 dayhigh 尾块（sentinel/块字节判重），"
            "拒绝二次追加")

    # 防线三（纯净副本）：前置态=零注入的完整候选副本（残块/外来块/坏源/收尾
    # 漂移一律拒）
    if _GG_MARKER in main_src:
        raise ValueError(
            "前置态漂移（非纯净副本）：候选已含 glutgate 尾块（链序错/外来块）")
    if not main_src.endswith("\n") or main_src.endswith("\n\n"):
        raise ValueError(
            "前置态漂移（非纯净副本）：候选须以恰一换行收尾（两空行分隔约定）")
    try:
        tree = ast.parse(main_src)
    except SyntaxError as exc:
        raise ValueError(
            "前置态漂移（非纯净副本）：候选源不可解析: %r" % (exc,)) from exc
    if not any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               for n in tree.body):
        raise ValueError(
            "前置态漂移（非纯净副本）：候选无可捕获末 callable（缺顶层函数）")
    if main_src[:-1].split("\n")[-1].strip().startswith("#"):
        raise ValueError(
            "前置态漂移（非纯净副本）：候选以注释尾行收尾（先例 base+'# drift' 形态）")

    injected = main_src + _SEP + block

    # 注入校验（fail-closed）：①可编译可解析 ②exec 装载后末 callable=_dayhigh_agent
    # 且宿主捕获成功 ③append-only（产物=原文+分隔+块，逐字节）
    try:
        compile(injected, "<r44-dayhigh>", "exec")
    except Exception as exc:
        raise RuntimeError("校验①红：注入后源码不可编译: %r" % (exc,)) from exc
    try:
        ast.parse(injected)
    except SyntaxError as exc:
        raise RuntimeError("校验①红：注入后源码 ast.parse 未过: %r" % (exc,)) from exc
    ns = {}
    try:
        exec(compile(injected, "<r44-dayhigh>", "exec"), ns)  # noqa: S102
    except Exception as exc:
        raise RuntimeError("校验②红：注入后源码 exec 失败: %r" % (exc,)) from exc
    loaded = [v for k, v in ns.items()
              if callable(v) and not (k.startswith("__") and k.endswith("__"))]
    if not loaded or loaded[-1].__name__ != "_dayhigh_agent":
        raise RuntimeError(
            "校验②红：装载后末 callable 非 _dayhigh_agent（实际 %r）"
            % (loaded[-1].__name__ if loaded else None,))
    if not callable(ns.get("_DH_HOST")):
        raise RuntimeError("校验②红：宿主末 callable 捕获失败（_DH_HOST 不可调）")
    if injected != main_src + _SEP + block:
        raise RuntimeError("校验③红：产物≠原文+分隔+块（非 append-only）")
    return injected


def append_glutgate_block(main_src):
    """把 quote_context 源码+glutgate_layer.py 源码按序拼接追加进候选尾块（B=
    单独层；AB=接在 dayhigh 层外层，门作用于含追加单的最终列表）；块嵌
    _glutgate_agent（捕获 _GG_HOST）。防线同 append_dayhigh_block。
    """
    q_src = (MODULE_DIR / "quote_context.py").read_text(encoding="utf-8")
    gg_src = (MODULE_DIR / "glutgate_layer.py").read_text(encoding="utf-8")
    if not q_src.endswith("\n") or not gg_src.endswith("\n"):
        raise ValueError("层源不以换行收尾，两空行分隔约定不成立（fail-closed）")
    block = _GG_HEAD + _SEP + q_src + _SEP + gg_src + _SEP + _GG_SEAL

    # 防线一（拒原件）：同 append_dayhigh_block
    if not isinstance(main_src, str):
        raise ValueError(
            "refusing to inject: 输入非候选 main 源文本（原件/文件指代只读）: %s"
            % type(main_src).__name__)

    # 防线二（判重）：已含 glutgate 尾块拒绝二次追加
    if _GG_MARKER in main_src or block in main_src:
        raise ValueError(
            "already injected: 目标候选已含 glutgate 尾块（sentinel/块字节判重），"
            "拒绝二次追加")

    # 防线三（纯净副本）：前置态=纯净基座（B）或基座+完整 dayhigh 尾块（AB）；
    # 残块/坏源/收尾漂移一律拒
    if not main_src.endswith("\n") or main_src.endswith("\n\n"):
        raise ValueError(
            "前置态漂移（非纯净副本）：候选须以恰一换行收尾（两空行分隔约定）")
    try:
        tree = ast.parse(main_src)
    except SyntaxError as exc:
        raise ValueError(
            "前置态漂移（非纯净副本）：候选源不可解析: %r" % (exc,)) from exc
    if not any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               for n in tree.body):
        raise ValueError(
            "前置态漂移（非纯净副本）：候选无可捕获末 callable（缺顶层函数）")
    if main_src[:-1].split("\n")[-1].strip().startswith("#"):
        raise ValueError(
            "前置态漂移（非纯净副本）：候选以注释尾行收尾（先例 base+'# drift' 形态）")
    if _DH_MARKER in main_src:
        # AB 前置态：dayhigh 块须完整（恰一 sentinel 且以 dayhigh 封口收尾）
        if main_src.count(_DH_MARKER) != 1 or \
                not main_src.endswith(_DH_SEAL):
            raise ValueError(
                "前置态漂移（非纯净副本）：dayhigh 尾块残缺（残块/半注入）")

    injected = main_src + _SEP + block

    # 注入校验（fail-closed）：①可编译可解析 ②exec 装载后末 callable=_glutgate_agent
    # 且宿主捕获成功 ③append-only
    try:
        compile(injected, "<r44-glutgate>", "exec")
    except Exception as exc:
        raise RuntimeError("校验①红：注入后源码不可编译: %r" % (exc,)) from exc
    try:
        ast.parse(injected)
    except SyntaxError as exc:
        raise RuntimeError("校验①红：注入后源码 ast.parse 未过: %r" % (exc,)) from exc
    ns = {}
    try:
        exec(compile(injected, "<r44-glutgate>", "exec"), ns)  # noqa: S102
    except Exception as exc:
        raise RuntimeError("校验②红：注入后源码 exec 失败: %r" % (exc,)) from exc
    loaded = [v for k, v in ns.items()
              if callable(v) and not (k.startswith("__") and k.endswith("__"))]
    if not loaded or loaded[-1].__name__ != "_glutgate_agent":
        raise RuntimeError(
            "校验②红：装载后末 callable 非 _glutgate_agent（实际 %r）"
            % (loaded[-1].__name__ if loaded else None,))
    if not callable(ns.get("_GG_HOST")):
        raise RuntimeError("校验②红：宿主末 callable 捕获失败（_GG_HOST 不可调）")
    if injected != main_src + _SEP + block:
        raise RuntimeError("校验③红：产物≠原文+分隔+块（非 append-only）")
    return injected
