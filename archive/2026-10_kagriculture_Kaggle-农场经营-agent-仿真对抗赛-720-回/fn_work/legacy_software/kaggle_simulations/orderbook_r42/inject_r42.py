# -*- coding: utf-8 -*-
"""inject_r42_block（R25 构建面）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：r40 字节尾部注入
三运行时件+常量；校验四条+sha 对账沿先例；捕获行 _R42_* 避撞名；末 callable=
官方入口；只加尾块。

【注入形制】（R23/R24 先例）：①捕获行先于一切 def（_R42_CALLABLES/
_R42_PARENT=原末 callable）；②三运行时件源 ast 抽取自本包模块，模块级
辅助名/常量整体改写 _R42P_ 前缀避撞名（公开函数名保留）；③末 def
_route42_agent=官方单参入口（链：父层→镜像门→终日清算→槽位编排，
逐件 fail-safe 原样）；④校验=捕获行位置/末 callable/件集恒等/块 sha
确定性，任一不过即抛。
"""
from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

MODULE_DIR = Path(__file__).resolve().parent

PUBLIC_FUNCS = {
    "slot_orchestration": ("apply_slot_orchestration", "merge_same_item_orders",
                           "clear_dead_slots", "select_best_layout"),
    "endgame": ("apply_endgame_liquidation",),
    "mirror": ("apply_mirror_gate",),
}

_PREAMBLE = """# ===== R25 运行时三件（slot orchestration / endgame liquidation /
# mirror gating）——judge-side 生成件，勿手改；末 callable=官方入口 =====
_R42_CALLABLES = [v for k, v in list(globals().items())
                  if callable(v) and not k.startswith("__")]
_R42_PARENT = _R42_CALLABLES[-1] if _R42_CALLABLES else None
"""

_AGENT = '''
def _route42_agent(observation):
    """r42 官方单参入口：父层动作→镜像门→终日清算→槽位编排（fail-safe）。"""
    parent = globals().get("_R42_PARENT")
    if not callable(parent):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    try:
        action = parent(observation)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    if not isinstance(action, dict):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    for fn in (apply_mirror_gate, apply_endgame_liquidation,
               apply_slot_orchestration):
        try:
            out = fn(observation, action)
            if isinstance(out, dict) and isinstance(out.get("action"), dict):
                action = out["action"]
        except Exception:
            pass
    return action
'''


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class _Renamer(ast.NodeTransformer):
    """顶层辅助名改写（仅标识符，不碰字符串字面量）。"""

    def __init__(self, renames):
        self.renames = renames

    def visit_FunctionDef(self, node):
        node.name = self.renames.get(node.name, node.name)
        return self.generic_visit(node)

    def visit_Name(self, node):
        node.id = self.renames.get(node.id, node.id)
        return node


def _extract_module(module_name: str) -> Tuple[str, List[str]]:
    """模块顶层件源抽取（函数+常量+import）；辅助名改写 _R42P_ 前缀。"""
    path = MODULE_DIR / ("%s.py" % module_name)
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    public = set(PUBLIC_FUNCS[module_name])
    renames: Dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name not in public:
            renames[node.name] = "_R42P_" + node.name.lstrip("_")
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id not in public and \
                        not t.id.startswith("__"):
                    renames[t.id] = "_R42P_" + t.id.lstrip("_")
    keep: List[str] = []
    names: List[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            seg = ast.get_source_segment(src, node)
            if seg and "__future__" not in seg:
                keep.append(seg)
        elif isinstance(node, ast.Assign):
            keep.append(ast.unparse(_Renamer(renames).visit(node)))
        elif isinstance(node, ast.FunctionDef):
            names.append(node.name)
            keep.append(ast.unparse(_Renamer(renames).visit(node)))
    return "\n".join(keep), names


def inject_r42_block(main_text: str, config: Any = None) -> Dict[str, Any]:
    """三运行时件注入。签名意图：输入: r40 main 文本+常量配置 / 输出:
    {main_text, block_sha, block_bytes} / 错误: 校验不过即抛。"""
    if not isinstance(main_text, str) or not main_text.strip():
        raise ValueError("main_text 非法")
    parts = [_PREAMBLE]
    seen: List[str] = []
    for mod in ("slot_orchestration", "endgame", "mirror"):
        body, names = _extract_module(mod)
        parts.append(body)
        seen.extend(PUBLIC_FUNCS[mod])
        if not all(n in names for n in PUBLIC_FUNCS[mod]):
            raise RuntimeError("模块缺公开件: %s" % mod)
    parts.append(_AGENT)
    block = "\n\n" + "\n\n".join(parts) + "\n"
    text = main_text + block
    compile(text, "<r42>", "exec")

    # 校验四条
    first_def = block.index("\ndef ") + 1 if "\ndef " in block else \
        len(block)
    if block.index("_R42_PARENT") > first_def:
        raise RuntimeError("捕获行不在一切 def 之前")
    for name in seen:
        if block.count("def %s(" % name) != 1:
            raise RuntimeError("件源重复或缺失: %s" % name)
    if block.count("def _route42_agent(") != 1:
        raise RuntimeError("官方入口缺失或重复")
    ns: Dict[str, Any] = {}
    exec(compile(text, "<r42-entry-check>", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    if not entries or entries[-1].__name__ != "_route42_agent":
        raise RuntimeError("末 callable 非官方入口")
    return {"main_text": text, "block_sha": _sha(block),
            "block_bytes": len(block.encode("utf-8"))}
