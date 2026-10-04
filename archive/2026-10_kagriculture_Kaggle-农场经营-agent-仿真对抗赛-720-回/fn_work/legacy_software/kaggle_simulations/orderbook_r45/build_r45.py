# -*- coding: utf-8 -*-
"""build_r45 及 advance 栈注入件（R28 构建线）。

责任契约（fn_docs/hybrid/responsibility.md【R28 增补】）：r40 字节 +
append_advance_stack_block（**账本+谷底闸门+提前层三件齐注，缺任一即构建
失败**）→ diff 审计（白名单=advance 栈注入块；磁带五区零改动）→ 确定性
打包 + manifest（k/视界/窗口参数定桩登记）+ sha 链（…→r40→r45）；描述
"public derivative with debt-ledgered advance selling"。三件不齐/审计白名单外
即抛（不产出）。

注入形态沿 orderbook_l1_derivative/append_layer_s_block 先例：块首捕获宿主
末 callable（_ADV_HOST_AGENT）、块尾末函数=_advance_agent（官方 last-callable
入口）；基座全文逐字节前缀恒等（五区零改动的前缀逐字证明，audit_base 同口径）。

【契约登记（批间）】append_advance_stack_block(main_src, modules) 的 modules
为三件套逻辑键源文本映射：{"debt_ledger", "valley_gate", "advance_layer"}，
缺任一/空文本即抛（三件缺一不注入，宁可构建失败）。物理归属（B47 实况）：
账本与提前层可在 advance_layer.py 同源提供、谷底闸门取 quote_context/
gate_added_sells 语义件——由调用方拼接映射到逻辑三键。build_r45 的
params={"modules": 同上（值可为 .py 路径或源文本）, "k","horizon","window"
（定桩）, 其余键原样登记 manifest}。
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
import time
from pathlib import Path
from typing import Any, Dict

MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = MODULE_DIR / "build"
SCHEMA = "orderbook_r45_manifest/1.0"
VARIANT = "r45"
DESCRIPTION = "public derivative with debt-ledgered advance selling"
# 血统锚（沿 orderbook_r43/build_r43 同口径登记：…→r34a→r37→r40；r45=本件自证）
BASE_CHAIN = {
    "a16e0e9b": "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab",
    "r34a": "51fc19dba2d0bcbf2d0a3720c26ff318541a0e6ce5800873bc863f612451aa5b",
    "r37": "23a513f903317e4d6133aea87e5205bd75cab057090e92c162e5c3be8e32707f",
    "r40": "4ce951f088740e0b3d4366dbf95f8bb225817b0417bbb2fcea6292a559ee9ea8",
}
CHAIN_ANCHORS = ("a16e0e9b", "r34a", "r37", "r40", "r45")
# 三件套逻辑键（缺任一即构建失败）
THREE_PIECES = ("debt_ledger", "valley_gate", "advance_layer")
PIECE_LABELS = {
    "debt_ledger": "①债务账本（r36_debts 口径：提前量记债、原 due_step 抵扣）",
    "valley_gate": "②谷底闸门（quote>=base 才提前，gate_added_sells 语义）",
    "advance_layer": "③有界视界提前层（末函数=_advance_agent）",
}
ADVANCE_SENTINEL = '"""advance 栈尾块'   # 块首 sentinel（注入判重/白名单锚）
ENTRY_NAME = "_advance_agent"            # 注入后末 callable（官方入口）
# 块首捕获宿主末 callable（官方 get_last_callable 同语义：插入序最后 callable）
CAPTURE_SRC = ("_ADV_HOST_AGENT = "
               "[v for v in list(globals().values()) if callable(v)][-1]")
SEPARATOR = "\n\n"                       # 基座尾与块首之间恰两个空行（layer S 先例）
# k/视界/窗口参数定桩缺省（判决标定后经 params 覆写入 manifest）
PARAM_DEFAULTS = {"k": 4, "horizon": 48, "window": [192, 695]}
# 磁带五区（零改动区登记；前缀逐字证明覆盖全域）
TAPE_ZONES = (("tape", "磁带"), ("routing", "路由"),
              ("anti_clone", "反克隆抢卖"), ("slot_reorder", "卖单槽位重排"),
              ("terminal", "终局清仓"))
SIZE_CAP_BYTES = 100 * 1024 * 1024       # 包体上限（五门④同值）


def append_advance_stack_block(main_src, modules):
    """advance 栈注入（沿 append_layer_s_block 形态；谷底闸门语义复用
    gate_added_sells；三件缺一不注入）。签名意图：输入: 候选 main 源+三件
    模块源 / 输出: 注入后 main 源 / 错误: 缺件即抛。"""
    # ---- 三件齐检（缺件即抛，宁可构建失败） -------------------------------
    if not isinstance(main_src, str) or not main_src:
        raise ValueError("main_src 须为非空 str")
    if not isinstance(modules, dict):
        raise ValueError("modules 须为三件套源映射 dict（缺件即抛）")
    if ADVANCE_SENTINEL in main_src:
        raise ValueError("already injected: main_src 已含 advance 栈块（sentinel 判重）")
    pieces: Dict[str, str] = {}
    for key in THREE_PIECES:
        src = modules.get(key)
        if not isinstance(src, str) or not src.strip():
            raise ValueError(f"三件不齐：缺 {key!r} 源（{PIECE_LABELS[key]}）")
        pieces[key] = src
    # ---- 块组装：块首捕获宿主末 callable，末函数=_advance_agent ------------
    block = (ADVANCE_SENTINEL + "（R28 债务账本式卖提前·三件套注入块）\n"
             "严格三件整搬（缺一即构建失败）；宿主行为零改动（仅尾部追加）。\n"
             '"""\n'
             + CAPTURE_SRC + "\n\n")
    for key in THREE_PIECES:
        block += "# ---- " + PIECE_LABELS[key] + " ----\n"
        block += pieces[key].rstrip("\n") + "\n\n"
    # 入口归一：官方 get_last_callable=插入序最后 callable；提前层源内定义序
    # 不作要求，块尾重绑保末函数=_advance_agent（缺 _advance_agent 即 exec 红）。
    block += ("# ---- 入口归一（末函数=_advance_agent） ----\n"
              "_ADV_ENTRY_TMP = _advance_agent\n"
              "del _advance_agent\n"
              "_advance_agent = _ADV_ENTRY_TMP\n"
              "del _ADV_ENTRY_TMP\n")
    if not main_src.endswith("\n"):
        raise ValueError("main_src 不以换行收尾，两空行分隔约定不成立（fail-closed）")
    injected = main_src + SEPARATOR + block
    # ---- 校验①语法（compile 同 py_compile 语义，不落盘） --------------------
    try:
        compile(injected, "<advance_stack_block>", "exec")
    except Exception as exc:
        raise RuntimeError(f"校验①红：注入后源语法不通过: {exc!r}") from exc
    # ---- 校验②装载后末 callable=_advance_agent（官方入口语义） -------------
    ns: Dict[str, Any] = {}
    try:
        exec(compile(injected, "<advance_stack_block>", "exec"), ns)
    except Exception as exc:
        raise RuntimeError(f"校验②红：注入后源 exec 失败: {exc!r}") from exc
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded:
        raise RuntimeError("校验②红：exec 后命名空间无任何 callable")
    if loaded[-1].__name__ != ENTRY_NAME:
        raise RuntimeError(
            f"校验②红：装载后最后 callable={loaded[-1].__name__!r}，应为 {ENTRY_NAME!r}")
    if not callable(ns.get("_ADV_HOST_AGENT")):
        raise RuntimeError("校验②红：块首未捕获宿主末 callable（_ADV_HOST_AGENT）")
    # ---- 校验③append-only：基座全文逐字节前缀恒等（五区零改动） ------------
    if not injected.startswith(main_src) or \
            injected != main_src + SEPARATOR + block:
        raise RuntimeError("校验③红：注入非纯尾部追加（基座区域被改动）")
    # ---- 校验④白名单内容：sentinel+三件源恰在块内 -------------------------
    tail = injected[len(main_src):]
    if ADVANCE_SENTINEL not in tail:
        raise RuntimeError("校验④红：注入块缺 sentinel")
    for key in THREE_PIECES:
        if pieces[key].rstrip("\n") not in tail:
            raise RuntimeError(f"校验④红：注入块缺 {key!r} 源")
    return injected


def build_r45(base_main_path, params, out_dir):
    """构建编排：r40 字节+append_advance_stack_block（账本+门+提前层三件齐注）→
    diff 审计（白名单=advance 栈注入块）→确定性打包+manifest（k/视界/窗口定桩）
    +sha 链。签名意图：输入: r40 main+参数配置 / 输出: r45 main+submission.tar.gz
    +manifest+diff 审计 / 错误: 三件不齐/白名单外即抛（不产出）。"""
    base_path = Path(str(base_main_path))
    if not base_path.is_file():
        raise FileNotFoundError(f"r40 main 不存在: {base_path}")
    cfg = params if isinstance(params, dict) else {}
    out = Path(str(out_dir)) if out_dir is not None else DEFAULT_OUT
    base_text = base_path.read_text(encoding="utf-8")
    base_bytes = base_path.read_bytes()
    # ---- 三件源归一（.py 路径→文本；缺件即抛） ----------------------------
    mods_in = cfg.get("modules")
    if not isinstance(mods_in, dict):
        raise ValueError("三件不齐：params 缺 modules 映射")
    resolved: Dict[str, str] = {}
    for key in THREE_PIECES:
        val = mods_in.get(key)
        if isinstance(val, Path):
            if not val.is_file():
                raise ValueError(f"三件不齐：{key!r} 路径不存在: {val}")
            val = val.read_text(encoding="utf-8")
        elif isinstance(val, str) and val.endswith(".py"):
            cand = Path(val)
            if cand.is_file():
                val = cand.read_text(encoding="utf-8")
        if not isinstance(val, str) or not val.strip():
            raise ValueError(f"三件不齐：缺 {key!r} 源（{PIECE_LABELS[key]}）")
        resolved[key] = val
    # ---- 注入（三件齐注；缺任一已在上抛） --------------------------------
    injected = append_advance_stack_block(base_text, resolved)
    # ---- diff 审计：白名单=advance 栈注入块；磁带五区零改动 ---------------
    if injected == base_text:
        raise RuntimeError("diff 审计红：无 advance 栈注入块（空注入）")
    if not injected.startswith(base_text):
        raise RuntimeError("diff 审计红：白名单外改动（基地区域/磁带五区被改）")
    tail = injected[len(base_text):]
    if ADVANCE_SENTINEL not in tail:
        raise RuntimeError("diff 审计红：白名单外改动（尾块缺 sentinel）")
    for key in THREE_PIECES:
        if resolved[key].rstrip("\n") not in tail:
            raise RuntimeError(f"diff 审计红：白名单外改动（缺 {key!r} 源）")
    audit = {
        "whitelist": ["advance_stack_block"],
        "prefix_identical": True,
        "zones_zero_change": {zone: "unchanged（前缀逐字节恒等）"
                              for zone, _label in TAPE_ZONES},
        "tail_bytes": len(tail.encode("utf-8")),
        "tail_sha256": hashlib.sha256(tail.encode("utf-8")).hexdigest(),
    }
    # ---- 确定性打包（双跑逐字节；mtime=0/USTAR/固定属主） -----------------
    raw = injected.encode("utf-8")
    runs = []
    for _ in range(2):
        buf = io.BytesIO()
        gz = gzip.GzipFile(fileobj=buf, mode="wb", mtime=0)
        with tarfile.open(fileobj=gz, mode="w",
                          format=tarfile.USTAR_FORMAT) as tf:
            info = tarfile.TarInfo(name="main.py")
            info.size = len(raw)
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mode = 0o644
            tf.addfile(info, io.BytesIO(raw))
        gz.close()
        runs.append(buf.getvalue())
    if hashlib.sha256(runs[0]).hexdigest() != \
            hashlib.sha256(runs[1]).hexdigest():
        raise RuntimeError("确定性打包双跑不一致")
    if len(runs[0]) > SIZE_CAP_BYTES:
        raise RuntimeError("包体超 100MB 上限")
    tar_bytes = runs[0]
    main_sha = hashlib.sha256(raw).hexdigest()
    tar_sha = hashlib.sha256(tar_bytes).hexdigest()
    # ---- manifest（k/视界/窗口定桩登记+sha 链 …→r40→r45） ----------------
    pinned: Dict[str, Any] = dict(PARAM_DEFAULTS)
    if isinstance(cfg, dict):
        for key, val in cfg.items():
            if key != "modules":
                pinned[key] = val
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%d"),
        "variant": VARIANT,
        "description": DESCRIPTION,
        "main_sha256": main_sha,
        "main_bytes": len(raw),
        "tar_sha256": tar_sha,
        "tar_bytes": len(tar_bytes),
        "tar_members": ["main.py"],
        "double_run_sha256": {"run1": hashlib.sha256(runs[0]).hexdigest(),
                              "run2": hashlib.sha256(runs[1]).hexdigest()},
        "base_sha_chain": dict(BASE_CHAIN, **{VARIANT: main_sha}),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "base_main_bytes": len(base_bytes),
        "params_pinned": pinned,
        "three_pieces": {key: {"sha256": hashlib.sha256(
            resolved[key].encode("utf-8")).hexdigest(),
            "bytes": len(resolved[key].encode("utf-8"))}
            for key in THREE_PIECES},
        "audit": audit,
        "complete": True,
    }
    # ---- 落盘（审计不过/双跑不一致以上已抛，不产出） ----------------------
    out.mkdir(parents=True, exist_ok=True)
    main_path = out / "main.py"
    tar_path = out / "submission.tar.gz"
    man_path = out / "build_manifest.json"
    main_path.write_bytes(raw)
    tar_path.write_bytes(tar_bytes)
    man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1,
                                   sort_keys=True) + "\n", encoding="utf-8")
    if main_path.read_bytes() != raw or tar_path.read_bytes() != tar_bytes:
        raise RuntimeError("落盘自证不符（盘上字节≠构建字节）")
    return {
        "main_path": str(main_path),
        "tar_path": str(tar_path),
        "man_path": str(man_path),
        "main_sha256": main_sha,
        "tar_sha256": tar_sha,
        "audit": audit,
        "manifest": manifest,
        "params_pinned": pinned,
        "out_dir": str(out),
    }
