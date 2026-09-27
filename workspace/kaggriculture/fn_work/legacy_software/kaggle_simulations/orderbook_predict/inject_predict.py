# -*- coding: utf-8 -*-
"""inject_predict_block（R21 L2；R22 改造→v2 块）：预测块注入。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】+【R22 增补】）：
生成预测块源码（六件 v2：detect_clone+五函数链+_predict_agent，含 credit 账）
+内嵌卖流库数据（v2 库）追加到副本尾部；注入校验四条沿 B17（py_compile/AST/
装载后 globals 末 callable=_predict_agent 单参可调/逐字节尾部追加零改行）
+库数据完整性校验（库 sha 对账，canonical ensure_ascii=False 口径）；捕获行
命名避底版撞名（先例 _R37_GUARD_PARENT）。
"""
from __future__ import annotations

import ast
import hashlib
import json
from typing import Any, Dict

# 六件单一真源抽取序（_predict_agent 钉尾=装载后 last-callable；v2 含 detect_clone）。
_BLOCK_FUNCS = ("detect_clone", "infer_rival_sells", "match_sellflow", "extrapolate_sells",
                "apply_dodge", "_predict_agent")

# 块绑定名全集（撞名预检用；Any/Dict 为条件缺省填充不入集，不覆盖底版既有绑定）。
_BLOCK_BOUND = {"detect_clone", "_PREDICT_CALLABLES", "_PREDICT_PARENT", "_PREDICT_LIBRARY",
                "_PREDICT_TYPING", "infer_rival_sells", "match_sellflow",
                "extrapolate_sells", "apply_dodge", "_predict_agent"}


def _module_bound_names(tree):
    """收集模块级绑定名（函数/类体是独立作用域，不入模块 globals）。"""
    names = set()

    def _scan_targets(target):
        for x in ast.walk(target):
            if isinstance(x, ast.Name):
                names.add(x.id)

    def _scan(stmts):
        for st in stmts:
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(st.name)
                continue
            if isinstance(st, (ast.Import, ast.ImportFrom)):
                for a in st.names:
                    names.add(a.asname or a.name.split(".")[0])
                continue
            if isinstance(st, ast.Assign):
                for t in st.targets:
                    _scan_targets(t)
                continue
            if isinstance(st, ast.AnnAssign):
                if isinstance(st.target, ast.Name):
                    names.add(st.target.id)
                continue
            if isinstance(st, ast.AugAssign):
                _scan_targets(st.target)
                continue
            if isinstance(st, (ast.For, ast.AsyncFor)):
                _scan_targets(st.target)
            elif isinstance(st, (ast.With, ast.AsyncWith)):
                for item in st.items:
                    if item.optional_vars is not None:
                        _scan_targets(item.optional_vars)
            elif isinstance(st, ast.Global):
                names.update(st.names)
            for attr in ("body", "orelse", "finalbody"):
                sub = getattr(st, attr, None)
                if isinstance(sub, list):
                    _scan(sub)
            for handler in getattr(st, "handlers", []):
                _scan(handler.body)

    _scan(tree.body)
    return names


def _canonical_lib_sha(obj: Any) -> str:
    """canonical json sha256（与 sellflow 建库件同口径：sort_keys+紧凑分隔）。"""
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)  # 与 pack AST 重算口径统一（评审 P3）
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _library_literal(obj: Any) -> str:
    """库数据内嵌字面量（json.dumps ensure_ascii=False 紧凑分隔，单行）。"""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def _split_library(library: Any):
    """库参数两形兼容，返回 (库数据, 记录 sha 或 None)。

    - 裸库 dict（库数据本体）→ 内嵌其 JSON dump，对账=块内 vs 参数两侧重算。
    - 建库件返回形 {"library":库数据, "build_audit":{"sha256_of_library":…}}
      → 内嵌 library 键的库数据本体，另按建库记录 sha 做完整性对账（改库
      一字节而记录 sha 不动→抛）。
    """
    if isinstance(library, dict) and isinstance(library.get("library"), dict) \
            and isinstance(library.get("build_audit"), dict):
        rec = library["build_audit"].get("sha256_of_library")
        return library["library"], (rec if isinstance(rec, str) else None)
    return library, None


def inject_predict_block(main_text: str, library: Any) -> Dict[str, Any]:
    """生成预测块（六件 v2 链+库数据）追加尾部，跑注入校验四条+库 sha 对账。

    签名意图：输入: r37 main 文本+库数据 / 输出: {main_text, block_sha} /
    错误: 校验任一不过即抛。

    命名方案（docstring 留档；捕获行命名 _PREDICT_* 避底版 _R37_GUARD_*/
    _r37_agent 系撞名，注入前撞名预检、撞名即抛，先例 inject_guard.py）：
    - 单一真源=predict_block.py：六件 v2（detect_clone / infer_rival_sells /
      match_sellflow / extrapolate_sells / apply_dodge / _predict_agent）源码
      经 ast 整段抽取生成块文本，零手抄零改名（_predict_agent 钉尾）。
    - 捕获行机制：_PREDICT_CALLABLES/_PREDICT_PARENT 位于块首、先于块内一切
      def 与 import 执行（exec 时序保证捕获到注入时刻 globals 既有最后
      callable=底版基座 agent[真 r37=_r37_agent 链]，而非块内自身函数）；
      过滤 not k.startswith(\"__\")（Python 3.14 模块样板 __annotate__ 等非宿主面；
      与并行 audit/pack 件共同约定的块结构同款）。
    - 库数据内嵌：_PREDICT_LIBRARY = json.dumps(库数据, ensure_ascii=False,
      separators 紧凑)（单行字面量）；_predict_agent 经 globals()
      ["_PREDICT_PARENT"] 调父层、globals()["_PREDICT_LIBRARY"] 取库
      （predict_block.py 现约定）。
    - 自包含：stdlib only——typing 缺省填充（仅供五函数签名注解求值）置捕获行
      之后（Dict/Any 皆 callable，不得抢 globals 末位；仅供六函数签名注解
      求值）且不覆盖底版既有绑定。
    - 块文本=追加载荷整体（含前置两空行分隔，B17 尾块同款形态），
      block_sha = sha256(块文本 utf-8 字节)；确定性：同输入同输出（块文本只
      依赖 predict_block.py 源与库数据，与 main_text 无关）。

    注入校验四条（任一不过即抛 RuntimeError，不许静默）：①compile() 内存编译
    注入全文；②ast.parse 注入全文；③exec 注入全文于全新命名空间（预置假父层
    callable 供无 callable 底版捕获）→ globals 最后 callable 名恰为
    _predict_agent 且可单参调用（合成 obs 冒烟走一遍，返回 dict 动作）；
    ④diff：注入全文以原 main_text 为逐字节前缀且恰=原文+块文本（零既有行改动）。

    库 sha 对账（库数据完整性校验，不过即抛 RuntimeError「库sha对账红」）：
    块内 _PREDICT_LIBRARY 解析回对象的 canonical json sha == 参数 library
    的 canonical json sha（sellflow 建库件口径 json.dumps(sort_keys=True,
    separators=(",",":")) 的 utf-8 字节 sha256）；参数带建库记录 sha 时再对账
    == 记录 sha。

    输入预检（先于四条）：main_text 非 str→TypeError；空/纯空白→ValueError；
    库非 dict→TypeError，库不可紧凑 JSON 内嵌/不可作 Python 字面量内嵌（true/
    false/null 形）/不可 canonical sha→ValueError（「坏库」）；块绑定名与底版
    模块级绑定撞名→ValueError（防 dict 重绑序陷阱与静默覆写；语法坏文本不在
    预检拦，交校验①红定罪）。
    """
    from pathlib import Path

    # ---- 0. 输入预检 ----
    if not isinstance(main_text, str):
        raise TypeError("main_text must be str, got %s" % type(main_text).__name__)
    if not main_text.strip():
        raise ValueError("main_text must not be empty/whitespace-only")
    lib_data, recorded_sha = _split_library(library)
    if not isinstance(lib_data, dict):
        raise TypeError("坏库：library must be a dict, got %s" % type(lib_data).__name__)
    try:
        lib_json = _library_literal(lib_data)
        ast.literal_eval(lib_json)   # 内嵌字面量必须可作 Python 字面量回读
        param_sha = _canonical_lib_sha(lib_data)
    except Exception as exc:
        raise ValueError("坏库：库数据不可紧凑 JSON 内嵌/不可 canonical sha: %r" % exc) from exc

    # ---- 1. 块文本生成（predict_block.py 六件源 ast 整段抽取，禁手抄第二份） ----
    src_path = Path(__file__).resolve().with_name("predict_block.py")
    src = src_path.read_text(encoding="utf-8")
    src_tree = ast.parse(src, filename=str(src_path))
    segs: Dict[str, str] = {}
    for node in src_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in _BLOCK_FUNCS:
            seg = ast.get_source_segment(src, node)
            if not seg:
                raise RuntimeError("block source extraction failed: %s" % node.name)
            segs[node.name] = seg
    missing = [name for name in _BLOCK_FUNCS if name not in segs]
    if missing:
        raise RuntimeError("predict_block.py 缺函数定义: %s" % missing)

    header = (
        "# ============ r38 对手预测尾块（自动生成，勿手改） ============\n"
        "# r39 v2 块内容：detect_clone+五函数链+内嵌卖流库 v2（锚行短语沿 v1，"
        "audit/pack 识别不动）\n"
        "_PREDICT_CALLABLES = [v for k, v in list(globals().items())"
        " if callable(v) and not k.startswith(\"__\")]\n"
        "_PREDICT_PARENT = _PREDICT_CALLABLES[-1] if _PREDICT_CALLABLES else None\n"
        "_PREDICT_LIBRARY = " + lib_json + "\n"
        "\n"
        "import typing as _PREDICT_TYPING\n"
        "if \"Any\" not in globals():\n"
        "    Any = _PREDICT_TYPING.Any\n"
        "if \"Dict\" not in globals():\n"
        "    Dict = _PREDICT_TYPING.Dict\n"
    )
    body = "\n\n\n".join(segs[name] for name in _BLOCK_FUNCS) + "\n"
    block_text = "\n\n" + header + "\n\n" + body

    # ---- 1b. 撞名预检：块绑定名不得与底版模块级绑定重名（防静默覆写） ----
    try:
        base_tree = ast.parse(main_text, filename="<main_text>")
    except SyntaxError:
        base_tree = None     # 语法坏文本交校验①红定罪，预检不越权
    if base_tree is not None:
        overlap = _BLOCK_BOUND & _module_bound_names(base_tree)
        if overlap:
            raise ValueError("块绑定名与底版模块级绑定撞名: %s" % sorted(overlap))

    # ---- 2. 尾部追加装配（原 main_text 逐字节前缀，零既有行改动） ----
    injected_text = main_text + block_text

    # ---- 校验①：compile() 内存编译注入全文 ----
    try:
        compiled = compile(injected_text, "<inject_predict_block>", "exec")
    except Exception as exc:
        raise RuntimeError("校验①红：compile() 内存编译注入全文未通过: %r" % exc) from exc

    # ---- 校验②：ast.parse 注入全文 ----
    try:
        ast.parse(injected_text, filename="<inject_predict_block>")
    except Exception as exc:
        raise RuntimeError("校验②红：ast.parse 注入全文未通过: %r" % exc) from exc

    # ---- 校验③：exec 装载 + globals 最后 callable=_predict_agent + 单参冒烟 ----
    ns: Dict[str, Any] = {}

    def _check3_stub(observation):
        return {"farmer": ["PASS"], "hands": [], "market": [["SELL", "MILK", 2]]}

    ns["_predict_check3_stub_base"] = _check3_stub   # 预置假父层（无 callable 底版供捕获）
    try:
        exec(compiled, ns)
    except Exception as exc:
        raise RuntimeError("校验③红：注入全文 exec 装载失败: %r" % exc) from exc
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not k.startswith("__")]
    if not loaded:
        raise RuntimeError("校验③红：exec 后命名空间无任何 callable")
    last_name, last_fn = loaded[-1]
    if last_name != "_predict_agent" or getattr(last_fn, "__name__", None) != "_predict_agent":
        raise RuntimeError(
            "校验③红：globals 最后 callable=%r（__name__=%r），应为 '_predict_agent'"
            % (last_name, getattr(last_fn, "__name__", None)))
    smoke_obs = {
        "step": 5, "day": 0, "hour": 5, "player": 0,
        "farms": [{"money": 210.0}, {"money": 229.0}],
        "market": {"inventory": {"WHEAT": 9989, "MILK": 500},
                   "prices": {"WHEAT": 25, "MILK": 160}},
        "town": {"unlocked_shops": ["BAKERY", "YARN_STORE"]},
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
    }
    try:
        smoke_out = last_fn(smoke_obs)      # 单参调用形态：action = fn(observation)
    except Exception as exc:
        raise RuntimeError("校验③红：单参冒烟调用失败: %r" % exc) from exc
    if not isinstance(smoke_out, dict):
        raise RuntimeError(
            "校验③红：单参冒烟返回 %s，应为 dict 动作" % type(smoke_out).__name__)

    # ---- 校验④：diff 仅尾部追加（注入全文以原 main_text 为逐字节前缀） ----
    if not injected_text.startswith(main_text):
        raise RuntimeError("校验④红：注入全文不以原 main_text 为逐字节前缀（既有行被改动）")
    if injected_text != main_text + block_text:
        raise RuntimeError("校验④红：注入全文 != 原 main_text + 块文本（尾部追加不成立）")
    main_bytes = main_text.encode("utf-8")
    injected_bytes = injected_text.encode("utf-8")
    if injected_bytes[:len(main_bytes)] != main_bytes:
        raise RuntimeError("校验④红：注入全文 utf-8 字节前缀与原文不逐字节相等")

    # ---- 库 sha 对账：块内 _PREDICT_LIBRARY vs 参数 library（完整性） ----
    try:
        emb = None
        for node in ast.parse(block_text, filename="<r38_predict_block>").body:
            if isinstance(node, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "_PREDICT_LIBRARY"
                    for t in node.targets):
                seg = ast.get_source_segment(block_text, node.value)
                if seg:
                    emb = ast.literal_eval(seg)
                break
        if emb is None:
            raise RuntimeError("库sha对账红：块内未找到 _PREDICT_LIBRARY 赋值")
        emb_sha = _canonical_lib_sha(emb)
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError("库sha对账红：块内 _PREDICT_LIBRARY 解析失败: %r" % exc) from exc
    if emb_sha != param_sha:
        raise RuntimeError(
            "库sha对账红：块内 _PREDICT_LIBRARY canonical sha %s != 参数 library sha %s"
            % (emb_sha, param_sha))
    if recorded_sha is not None and recorded_sha != emb_sha:
        raise RuntimeError(
            "库sha对账红：块内 canonical sha %s != 建库记录 sha %s（库数据完整性不符）"
            % (emb_sha, recorded_sha))

    block_sha = hashlib.sha256(block_text.encode("utf-8")).hexdigest()
    return {"main_text": injected_text, "block_sha": block_sha}
