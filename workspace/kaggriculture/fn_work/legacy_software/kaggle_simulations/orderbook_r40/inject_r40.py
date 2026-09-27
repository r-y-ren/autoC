# -*- coding: utf-8 -*-
"""inject_r40_block（R23 L2）：运行时三件注入。

责任契约：_route40_select/apply_race_slots/apply_slot_hygiene+内嵌续段库
追加尾部；校验四条+库 sha 对账沿 B17/B23 先例；捕获行避底版撞名（_R40_*）。
"""
from __future__ import annotations

import ast
import hashlib
import json
from typing import Any, Dict

# 三件单一真源抽取序（_route40_agent 单参包装钉尾=装载后 last-callable）。
_BLOCK_FUNCS = ("_route40_select", "apply_race_slots", "apply_slot_hygiene")

# 块绑定名全集（撞名预检用；Any/Dict 为条件缺省填充不入集，不覆盖底版既有绑定）。
_BLOCK_BOUND = {"_route40_select", "apply_race_slots", "apply_slot_hygiene",
                "_route40_agent", "_R40_CALLABLES", "_R40_PARENT",
                "_R40_LIBRARY", "_R40_TYPING"}

# 块锚行核心短语（与 audit_diff_r40_vs_r37/pack_r40 识别口径一致；全文恰一次）。
_BLOCK_CORE = "r40 运行时尾块"

# 单参官方入口包装（运行时三件链转调；形态按 runtime_r40 现约定定形，docstring
# 留档——三件签名/语义见 runtime_r40.py：_route40_select(observation, library=None)
# 只读续段选择（latched/异常回退）、apply_race_slots(observation, action)→调整后
# action、apply_slot_hygiene(observation, action)→{"action","cleared","filled"}）。
_AGENT_SRC = '''def _route40_agent(observation):
    """单参数入口适配（官方 runner 语义：action = last_callable(observation)）。

    转调三件链（runtime_r40 现约定定形，docstring 留档）：
    - _route40_select(observation, 库)：step144 续段选择——只读、跨步 latched、
      异常回退 {route: None, family: None, confidence: 0.0}；结果存
      _route40_agent._last_select（测试可查），不改动作。
    - apply_race_slots(observation, action)：同回合卖单竞速——只动 SELL 槽序
      （空槽位次语义+V57 资金序不变量），异常→原动作。
    - apply_slot_hygiene(observation, action)：队列补洞——返回
      {"action", "cleared", "filled"}，取其 "action" 为最终动作。
    接线沿 _predict_agent 先例：父层=注入层捕获变量 _R40_PARENT、库=内嵌
    _R40_LIBRARY，均经 globals() 查找（测试可注入假父层/假库）。
    任何异常→父层动作原样（fail-safe）；父层缺失/父层抛/父层非 dict 动作→
    PASS 兜底 {"farmer": ["PASS"], "hands": [], "market": []}。
    本函数必须保持为模块 globals 最后一个 callable（注入校验③钉住）。
    """
    parent = globals().get("_R40_PARENT")
    if not callable(parent):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    try:
        action = parent(observation)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    if not isinstance(action, dict):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    try:
        _route40_agent._last_select = _route40_select(
            observation, globals().get("_R40_LIBRARY"))
    except Exception:
        pass
    try:
        action = apply_race_slots(observation, action)
    except Exception:
        pass
    try:
        out = apply_slot_hygiene(observation, action)
        if isinstance(out, dict) and isinstance(out.get("action"), dict):
            action = out["action"]
    except Exception:
        pass
    return action'''


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
    """canonical json sha256（route_library.build_audit.library_sha 同口径：
    sort_keys+ensure_ascii=False+紧凑分隔）。"""
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _library_literal(obj: Any) -> str:
    """库数据内嵌字面量（repr 单行）。

    口径留档：续段库含 best_route=None/covered=bool 等 Python 专属字面量，
    json 形（true/false/null）不可作 Python 字面量 exec——故内嵌取 repr 单行
    （ast.literal_eval 往返恒等）；canonical sha 对账另走 _canonical_lib_sha
    （json 口径，与 build_route_library 记录 sha 同源）。
    """
    return repr(obj)


def _split_library(library: Any):
    """库参数两形兼容，返回 (库核心数据, 记录 sha 或 None)。

    - 建库件返回形 {"library": 库数据, "build_audit": {...}}（build_route_library
      产物）→ 取 library 键数据本体，另按 build_audit.library_sha（或
      sha256_of_library）做完整性对账（改库一字节而记录 sha 不动→抛）。
    - 裸库 dict → 本体；自带 "build_audit" 构建账时同口径识别。
    - 内嵌口径=剔除 "build_audit" 构建账后的库核心（version/families/default/
      defeat_worlds），其 canonical sha == build_audit.library_sha（route_library
      lib_core 同源，真库=0236c30e…）。
    """
    if isinstance(library, dict) and isinstance(library.get("library"), dict) \
            and isinstance(library.get("build_audit"), dict):
        data, audit = library["library"], library["build_audit"]
    else:
        data = library
        audit = data.get("build_audit") if isinstance(data, dict) and \
            isinstance(data.get("build_audit"), dict) else None
    if not isinstance(data, dict):
        raise TypeError("坏库：library must be a dict, got %s"
                        % type(data).__name__)
    core = ({k: v for k, v in data.items() if k != "build_audit"}
            if isinstance(data.get("build_audit"), dict) else data)
    recorded = None
    if audit is not None:
        rec = audit.get("library_sha", audit.get("sha256_of_library"))
        recorded = rec if isinstance(rec, str) else None
    return core, recorded


def inject_r40_block(main_text: str, library: Any) -> Dict[str, Any]:
    """生成 r40 运行时块（三件+库）追加尾部，跑校验四条+库 sha 对账。

    签名意图：输入: r37 main 文本+库数据 / 输出: {main_text, block_sha} /
    错误: 校验不过即抛。

    命名方案（docstring 留档；捕获行 _R40_* 避底版 _PREDICT_*/_R37_GUARD_* 系
    撞名，注入前撞名预检、撞名即抛，先例 inject_predict.py）：
    - 单一真源=runtime_r40.py：三件（_route40_select/apply_race_slots/
      apply_slot_hygiene）源码经 ast 整段抽取生成块文本，零手抄零改名
      （抽取序=_BLOCK_FUNCS，_route40_agent 单参包装钉尾）。
    - 单参包装 _route40_agent(observation)（官方入口，形态按 runtime_r40 现
      约定定形，详见 _AGENT_SRC docstring）：父层取动作 → _route40_select
      续段选择（只读，结果存 _last_select）→ apply_race_slots 竞速 →
      apply_slot_hygiene 补洞取 action → 返回；异常 fail-safe。
    - 捕获行机制：_R40_CALLABLES/_R40_PARENT 位于块首、先于块内一切 def 与
      import 执行（exec 时序保证捕获到注入时刻 globals 既有最后 callable=底版
      基座 agent[真 r37=_r37_agent 链]，而非块内自身函数）；过滤
      not k.startswith("__")（与 audit/pack 件共同约定的块结构同款）。
    - 库数据内嵌：_R40_LIBRARY = repr(库核心)（单行字面量，口径见
      _library_literal）；_route40_agent 经 globals()["_R40_PARENT"] 调父层、
      globals()["_R40_LIBRARY"] 取库。
    - 自包含：stdlib only——typing 缺省填充（仅供三件签名注解求值）置捕获行
      之后（Dict/Any 皆 callable，不得抢 globals 末位）且不覆盖底版既有绑定。
    - 块文本=追加载荷整体（含前置两空行分隔，B17 尾块同款形态），block_sha =
      sha256(块文本 utf-8 字节)；确定性：同输入同输出（块文本只依赖
      runtime_r40.py 源与库数据，与 main_text 无关）。

    注入校验四条（任一不过即抛 RuntimeError，不许静默）：①compile() 内存编译
    注入全文；②ast.parse 注入全文；③exec 注入全文于全新命名空间（预置假父层
    callable 供无 callable 底版捕获）→ globals 最后 callable 名恰为
    _route40_agent 且可单参调用（合成 obs 冒烟走一遍，返回 dict 动作）；
    ④diff：注入全文以原 main_text 为逐字节前缀且恰=原文+块文本（零既有行改动）。

    库 sha 对账（库数据完整性校验，不过即抛 RuntimeError「库sha对账红」）：
    块内 _R40_LIBRARY 解析回对象的 canonical json sha == 参数库核心的
    canonical json sha（route_library.build_audit.library_sha 口径）；参数带
    建库记录 sha 时再对账 == 记录 sha。

    输入预检（先于四条）：main_text 非 str→TypeError；空/纯空白→ValueError；
    库非 dict→TypeError，库不可作 Python 字面量内嵌/不可 canonical sha→
    ValueError（「坏库」）；块绑定名与底版模块级绑定撞名→ValueError（防 dict
    重绑序陷阱与静默覆写；语法坏文本不在预检拦，交校验①红定罪）。
    """
    from pathlib import Path

    # ---- 0. 输入预检 ----
    if not isinstance(main_text, str):
        raise TypeError("main_text must be str, got %s" % type(main_text).__name__)
    if not main_text.strip():
        raise ValueError("main_text must not be empty/whitespace-only")
    lib_data, recorded_sha = _split_library(library)
    try:
        lib_repr = _library_literal(lib_data)
        ast.literal_eval(lib_repr)   # 内嵌字面量必须可作 Python 字面量回读
        param_sha = _canonical_lib_sha(lib_data)
    except Exception as exc:
        raise ValueError("坏库：库数据不可作 Python 字面量内嵌/不可 canonical sha: %r"
                         % exc) from exc

    # ---- 1. 块文本生成（runtime_r40.py 三件源 ast 整段抽取，禁手抄第二份） ----
    src_path = Path(__file__).resolve().with_name("runtime_r40.py")
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
        raise RuntimeError("runtime_r40.py 缺函数定义: %s" % missing)

    header = (
        "# ============ " + _BLOCK_CORE + "（自动生成，勿手改） ============\n"
        "# r40 块内容：续段选择器+同回合卖单竞速+队列补洞三件链+内嵌续段库"
        "（锚行=本块首行标记，audit/pack 按核心短语识别）\n"
        "_R40_CALLABLES = [v for k, v in list(globals().items())"
        " if callable(v) and not k.startswith(\"__\")]\n"
        "_R40_PARENT = _R40_CALLABLES[-1] if _R40_CALLABLES else None\n"
        "_R40_LIBRARY = " + lib_repr + "\n"
        "\n"
        "import typing as _R40_TYPING\n"
        "if \"Any\" not in globals():\n"
        "    Any = _R40_TYPING.Any\n"
        "if \"Dict\" not in globals():\n"
        "    Dict = _R40_TYPING.Dict\n"
    )
    body = "\n\n\n".join(segs[name] for name in _BLOCK_FUNCS) + "\n\n\n" \
        + _AGENT_SRC + "\n"
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
        compiled = compile(injected_text, "<inject_r40_block>", "exec")
    except Exception as exc:
        raise RuntimeError("校验①红：compile() 内存编译注入全文未通过: %r" % exc) from exc

    # ---- 校验②：ast.parse 注入全文 ----
    try:
        ast.parse(injected_text, filename="<inject_r40_block>")
    except Exception as exc:
        raise RuntimeError("校验②红：ast.parse 注入全文未通过: %r" % exc) from exc

    # ---- 校验③：exec 装载 + globals 最后 callable=_route40_agent + 单参冒烟 ----
    ns: Dict[str, Any] = {}

    def _check3_stub(observation):
        return {"farmer": ["PASS"], "hands": [], "market": [["SELL", "MILK", 2]]}

    ns["_r40_check3_stub_base"] = _check3_stub   # 预置假父层（无 callable 底版供捕获）
    try:
        exec(compiled, ns)
    except Exception as exc:
        raise RuntimeError("校验③红：注入全文 exec 装载失败: %r" % exc) from exc
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not k.startswith("__")]
    if not loaded:
        raise RuntimeError("校验③红：exec 后命名空间无任何 callable")
    last_name, last_fn = loaded[-1]
    if last_name != "_route40_agent" or getattr(last_fn, "__name__", None) \
            != "_route40_agent":
        raise RuntimeError(
            "校验③红：globals 最后 callable=%r（__name__=%r），应为 '_route40_agent'"
            % (last_name, getattr(last_fn, "__name__", None)))
    smoke_obs = {
        "step": 5, "day": 0, "hour": 5, "player": 0,
        "farms": [{"money": 210.0, "hands": [], "unlocked_quadrants": [],
                   "tiles": []},
                  {"money": 229.0, "hands": [], "unlocked_quadrants": [],
                   "tiles": []}],
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

    # ---- 库 sha 对账：块内 _R40_LIBRARY vs 参数库核心（完整性） ----
    try:
        emb = None
        for node in ast.parse(block_text, filename="<r40_runtime_block>").body:
            if isinstance(node, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "_R40_LIBRARY"
                    for t in node.targets):
                seg = ast.get_source_segment(block_text, node.value)
                if seg:
                    emb = ast.literal_eval(seg)
                break
        if emb is None:
            raise RuntimeError("库sha对账红：块内未找到 _R40_LIBRARY 赋值")
        emb_sha = _canonical_lib_sha(emb)
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError("库sha对账红：块内 _R40_LIBRARY 解析失败: %r" % exc) from exc
    if emb_sha != param_sha:
        raise RuntimeError(
            "库sha对账红：块内 _R40_LIBRARY canonical sha %s != 参数库核心 sha %s"
            % (emb_sha, param_sha))
    if recorded_sha is not None and recorded_sha != emb_sha:
        raise RuntimeError(
            "库sha对账红：块内 canonical sha %s != 建库记录 sha %s（库数据完整性不符）"
            % (emb_sha, recorded_sha))

    block_sha = hashlib.sha256(block_text.encode("utf-8")).hexdigest()
    return {"main_text": injected_text, "block_sha": block_sha}
