# -*- coding: utf-8 -*-
"""inject_cash_guard_block（R19/R20 L2）：现金保底守卫源码块注入。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
生成 cash_guard_block 三函数链源码文本追加到副本尾部；注入校验四条——
py_compile 通过、AST 可解析、装载后 globals 最后 callable=_r37_agent、
对底版 diff 仅尾部追加（无既有行改动）。
"""
from __future__ import annotations

from typing import Any, Dict


def inject_cash_guard_block(main_text: str) -> Dict[str, Any]:
    """生成守卫块源码并追加到 main_text 尾部，跑注入校验四条。

    签名意图：输入: r34a main 文本 / 输出: {main_text, block_sha}（注入后
    main+块 sha） / 错误: 校验任一不过即抛。

    命名方案（docstring 留档；生成块首注释同步说明）：
    - 单一真源=cash_guard_block.py：三函数（_r37_defer_low_priority /
      _r37_cash_guard / _r37_agent）源码经 ast 整段抽取生成块文本，不许手抄；
      仅一处受控改名——纯核 _r37_agent（observation, base_action 双参数）在块内
      改名 _r37_guard_core（\\b 词边界全量改名，含其 _defer_ledger 函数属性账
      自引用，账随函数走；cash_guard_block.py 源文件本身不改名）。
    - 捕获行机制：_R37_GUARD_CALLABLES/_R37_GUARD_PARENT 位于块首、先于块内
      一切 def 与 import 执行（exec 时序保证捕获到注入时刻 globals 既有最后
      callable=底版基座 agent，而非块内自身函数）；双下划线名排除（Python 3.14
      模块样板 __annotate__ 等非宿主面；层 D _CXD_HOST / layer S _CXS_HOST
      last-callable 捕获同款先例）。刻意不用 _R37_PARENT 之名——r34a 主干
      L1883 已绑 _R37_PARENT 并 L1914 逐步调用，覆写会致链上递归。
    - 块尾单参数入口占名 _r37_agent（官方 runner 语义：action=last_callable(
      observation)）：base_action = _R37_GUARD_PARENT(observation) 后转调纯核
      _r37_guard_core(observation, base_action)；纯核 fail-safe 行为不变。
    - 自包含：stdlib only——typing 导入仅供三函数签名注解求值，Any/Dict 缺省
      填充（不覆盖底版既有绑定），且置捕获行之后（Dict/Any 皆 callable，不得
      抢 globals 末位）。
    - 块文本=追加载荷整体（含前置两空行分隔，层 D/counter T-B 尾块同款形态），
      block_sha = sha256(块文本 utf-8 字节)；确定性：同输入同输出（块文本只
      依赖 cash_guard_block.py 源，与 main_text 无关）。

    注入校验四条（任一不过即抛 RuntimeError，不许静默）：①compile() 内存编译
    注入全文；②ast.parse 注入全文；③exec 注入全文于全新命名空间（预置假基座
    callable 供无 callable 底版捕获）→ globals 最后 callable 名恰为 _r37_agent
    且可单参调用（合成 obs 冒烟走一遍，返回 dict 动作）；④diff：注入全文以原
    main_text 为逐字节前缀且恰=原文+块文本（零既有行改动）。

    输入预检（先于四条）：main_text 非 str→TypeError；空/纯空白→ValueError；
    块绑定名与底版模块级绑定撞名→ValueError（防 dict 重绑序陷阱与静默覆写；
    语法坏文本不在预检拦，交校验①红定罪）。
    """
    import ast
    import hashlib
    import re
    from pathlib import Path

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

    # ---- 0. 输入预检 ----
    if not isinstance(main_text, str):
        raise TypeError("main_text must be str, got %s" % type(main_text).__name__)
    if not main_text.strip():
        raise ValueError("main_text must not be empty/whitespace-only")

    # ---- 1. 块文本生成（cash_guard_block.py 源 ast 整段抽取，禁手抄第二份） ----
    src_path = Path(__file__).resolve().with_name("cash_guard_block.py")
    src = src_path.read_text(encoding="utf-8")
    src_tree = ast.parse(src, filename=str(src_path))
    wanted = ("_r37_agent", "_r37_cash_guard", "_r37_defer_low_priority")
    segs: Dict[str, str] = {}
    for node in src_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in wanted:
            seg = ast.get_source_segment(src, node)
            if not seg:
                raise RuntimeError("block source extraction failed: %s" % node.name)
            segs[node.name] = seg
    missing = [name for name in wanted if name not in segs]
    if missing:
        raise RuntimeError("cash_guard_block.py 缺函数定义: %s" % missing)
    # 受控改名：纯核 _r37_agent → _r37_guard_core（块尾单参数入口占 _r37_agent）
    core_seg = re.sub(r"\b_r37_agent\b", "_r37_guard_core", segs["_r37_agent"])

    header = (
        "# ============ r37 现金保底守卫尾块（自动生成，勿手改） ============\n"
        "# 生成元：orderbook_r37/inject_guard.py::inject_cash_guard_block\n"
        "# 源真值：orderbook_r37/cash_guard_block.py（三函数源码 ast 整段抽取）\n"
        "# 命名方案：纯核 _r37_agent（双参数）→ 块内改名 _r37_guard_core（源文件\n"
        "#   不改名，词边界全量改名含 _defer_ledger 函数属性账自引用，账随函数走）；\n"
        "#   块尾单参数入口占名 _r37_agent——官方 runner 按模块 globals 最后一个\n"
        "#   callable 当 agent（action = fn(observation)）。\n"
        "# 捕获行：先于本块一切 def/import 执行，取注入时刻 globals 既有最后\n"
        "#   callable=底版基座 agent（层 D _CXD_HOST / layer S _CXS_HOST 同款\n"
        "#   last-callable 先例；双下划线名排除 Python 3.14 模块样板 __annotate__）。\n"
        "#   刻意不用 _R37_PARENT：r34a 主干已绑该名并逐步调用，覆写会致链上递归。\n"
        "# 自包含：stdlib only；typing 缺省填充置捕获行之后（Dict/Any 皆 callable，\n"
        "#   不得抢 globals 末位）且不覆盖底版既有绑定。\n"
        "# =================================================================\n"
        "\n"
        "_R37_GUARD_CALLABLES = [v for k, v in list(globals().items())\n"
        "                        if callable(v) and not (k.startswith(\"__\") and k.endswith(\"__\"))]\n"
        "_R37_GUARD_PARENT = _R37_GUARD_CALLABLES[-1] if _R37_GUARD_CALLABLES else None\n"
        "\n"
        "import typing as _r37_guard_typing\n"
        "if \"Any\" not in globals():\n"
        "    Any = _r37_guard_typing.Any\n"
        "if \"Dict\" not in globals():\n"
        "    Dict = _r37_guard_typing.Dict\n"
    )
    adapter = (
        "def _r37_agent(observation):\n"
        "    '''单参数入口适配（官方 runner 语义：action = last_callable(observation)）。\n"
        "\n"
        "    base_action = _R37_GUARD_PARENT(observation)（块首捕获的底版基座\n"
        "    agent）取基座动作，再转调纯核 _r37_guard_core(observation, base_action)\n"
        "    （cash_guard_block.py _r37_agent 的块内改名；fail-safe：纯核任何异常\n"
        "    →基座动作原样返回）。命名方案见块首注释；本函数必须保持为模块\n"
        "    globals 最后一个 callable（注入校验③钉住）。\n"
        "    '''\n"
        "    base_action = _R37_GUARD_PARENT(observation)\n"
        "    return _r37_guard_core(observation, base_action)\n"
    )
    block_text = ("\n\n"
                  + header + "\n\n"
                  + core_seg + "\n\n\n"
                  + segs["_r37_cash_guard"] + "\n\n\n"
                  + segs["_r37_defer_low_priority"] + "\n\n\n"
                  + adapter + "\n")

    # ---- 1b. 撞名预检：块绑定名不得与底版模块级绑定重名（防静默覆写） ----
    block_bound = {"_R37_GUARD_CALLABLES", "_R37_GUARD_PARENT", "_r37_guard_typing",
                   "_r37_guard_core", "_r37_cash_guard", "_r37_defer_low_priority",
                   "_r37_agent"}
    try:
        base_tree = ast.parse(main_text, filename="<main_text>")
    except SyntaxError:
        base_tree = None     # 语法坏文本交校验①红定罪，预检不越权
    if base_tree is not None:
        overlap = block_bound & _module_bound_names(base_tree)
        if overlap:
            raise ValueError("块绑定名与底版模块级绑定撞名: %s" % sorted(overlap))

    # ---- 2. 尾部追加装配（原 main_text 逐字节前缀，零既有行改动） ----
    injected_text = main_text + block_text

    # ---- 校验①：compile() 内存编译注入全文 ----
    try:
        compiled = compile(injected_text, "<inject_cash_guard_block>", "exec")
    except Exception as exc:
        raise RuntimeError("校验①红：compile() 内存编译注入全文未通过: %r" % exc) from exc

    # ---- 校验②：ast.parse 注入全文 ----
    try:
        ast.parse(injected_text, filename="<inject_cash_guard_block>")
    except Exception as exc:
        raise RuntimeError("校验②红：ast.parse 注入全文未通过: %r" % exc) from exc

    # ---- 校验③：exec 装载 + globals 最后 callable=_r37_agent + 单参冒烟 ----
    ns: Dict[str, Any] = {}

    def _check3_stub(observation):
        return {"farmer": ["PASS"], "hands": [], "market": []}

    ns["_r37_check3_stub_base"] = _check3_stub   # 预置假基座（无 callable 底版供捕获）
    try:
        exec(compiled, ns)
    except Exception as exc:
        raise RuntimeError("校验③红：注入全文 exec 装载失败: %r" % exc) from exc
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not (k.startswith("__") and k.endswith("__"))]
    if not loaded:
        raise RuntimeError("校验③红：exec 后命名空间无任何 callable")
    last_name, last_fn = loaded[-1]
    if last_name != "_r37_agent" or getattr(last_fn, "__name__", None) != "_r37_agent":
        raise RuntimeError(
            "校验③红：globals 最后 callable=%r（__name__=%r），应为 '_r37_agent'"
            % (last_name, getattr(last_fn, "__name__", None)))
    smoke_obs = {
        "step": 5,
        "player": 0,
        "farms": {
            0: {"money": 100.0, "tiles": [[0] * 5 for _ in range(5)],
                "farmer": [0, 0], "hands": [], "consecutive_unfed": 0,
                "animals_grid": [[None] * 5 for _ in range(5)], "animals": []},
            1: {"money": 100.0, "tiles": [[0] * 5 for _ in range(5)],
                "farmer": [0, 0], "hands": [], "consecutive_unfed": 0,
                "animals_grid": [[None] * 5 for _ in range(5)], "animals": []},
        },
        "private": {"shed": {}, "seeds": {}, "inventories": [{}, {}]},
        "market": {"inventory": {"WHEAT": 0}, "prices": {"WHEAT": [0, 0, 0, 0]}},
        "town": {"unlocked_shops": []},
        "weather": [0.0] * 720,
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

    block_sha = hashlib.sha256(block_text.encode("utf-8")).hexdigest()
    return {"main_text": injected_text, "block_sha": block_sha}
