"""AST 解析布局根构建 import 图（import/from/from-import 名/动态装载字面量），断言主线不依赖指定实验区/测试资产区成员，违例清单输出（strict 模式违例抛）；对旧树提供只读消费面扫描（四件 direct/transitive 消费者，designation 依据）。

上游: R13, R14（详见 fn_docs/responsibility.md）

实现要点：
- import 边语义：ast.Import 每别名一条边；ast.ImportFrom 一条边（target=P）
  附 from 名单 names（`from kgenv.bots import llm_provider` 的成员命中按
  P.llm_provider 组合判定——from-import 名单不预展开为伪模块边，保持图
  语义干净：函数名导入不算模块边）、相对导入按文件包位解析为绝对形态
  （kgenv/redlines.py 的 `from .economy import …` → kgenv.economy）、
  `importlib.import_module("…")`/`__import__("…")` 字面量亦计为声明边。
  成员命中 = 边 target（或 target+from 名单组合）等于成员名或以成员名
  +"." 开头（子模块）。
- 主线断言只看**声明面**（直接 import）：`import kgenv` 不因 kgenv/__init__ 的
  eager import 判为主线直接依赖 economy（那是传递面，由
  transitive_member_exposure 单独披露，战后随 __init__ 剔除消解）。
- 旧树只读分析模式 scan_legacy_consumers：全树 AST 扫描产出每件
  {direct: [{consumer, line, stmt}], transitive: [{consumer, via}]}——direct=
  声明边命中；transitive=经包 __init__（eager import）或经另一成员文件一跳
  触达（如 redlines→economy 成员内边）。旧树零写入。
- fail-closed：布局根缺失/无 .py 文件/源码解析失败均 ValueError 拒绝空跑；
  strict=True 违例抛 MainlineImportViolationError（附 violations 属性）。
- 模块内零字面战役路径（R20）：默认根经 shared.discover_campaign_roots 发现。
"""

from __future__ import annotations

import ast
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["MainlineImportViolationError", "ZONE_DORMANT_LAB", "ZONE_TEST_ASSET",
           "DESIGNATED_ZONE_MEMBERS", "build_import_graph",
           "scan_legacy_consumers", "transitive_member_exposure",
           "prune_mainline_import_graph"]

ZONE_DORMANT_LAB = "dormant_lab"
ZONE_TEST_ASSET = "test_asset"

# R13/R14 指定成员（module id → 分区）：gym_env/llm_provider→dormant 实验区，
# economy/redlines→测试资产区（fn_docs/requirements.md R13/G15、R14/G16）
DESIGNATED_ZONE_MEMBERS: dict[str, str] = {
    "kgenv.gym_env": ZONE_DORMANT_LAB,
    "kgenv.bots.llm_provider": ZONE_DORMANT_LAB,
    "kgenv.economy": ZONE_TEST_ASSET,
    "kgenv.redlines": ZONE_TEST_ASSET,
}


class MainlineImportViolationError(RuntimeError):
    """strict 模式下主线 import 图含分区成员（违例即抛，附 violations 清单）。"""

    def __init__(self, message: str, violations: list[dict]):
        super().__init__(message)
        self.violations = violations


def _rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _file_module(rel: str) -> str | None:
    """文件相对路径 → 点分模块名（kgenv/bots/llm_provider.py → kgenv.bots.llm_provider）。"""
    parts = Path(rel).with_suffix("").parts
    if not parts or (len(parts) == 1 and parts[0] == "__init__"):
        return None
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else None


def _file_package(rel: str) -> str:
    """文件所属包（父目录链点分；顶层文件为空串）。"""
    return _file_module(str(Path(rel).parent / "__init__.py")) or ""


def _relative_base(package: str, level: int) -> str:
    """相对导入基准包：level=1 → 当前包；每多一级上溯一层；越界返回空串。"""
    parts = package.split(".") if package else []
    up = level - 1
    if up > len(parts):
        return ""
    return ".".join(parts[: len(parts) - up]) if up else package


def _declared_edges(tree: ast.Module, package: str, source_lines: list[str]) \
        -> list[dict]:
    """AST → 声明 import 边 [{target, line, stmt, names}]（去重排序）。

    ImportFrom 为一条边（target=模块 P，names=from 名单）；import/dynamic 为
    target 边（names 空）。names 供成员命中组合判定（P.N），不预展开为边。
    """
    edges: dict[tuple[str, int], dict] = {}

    def add(target: str, lineno: int, names: tuple[str, ...] = ()) -> None:
        if not target or target.startswith("."):
            return
        stmt = source_lines[lineno - 1].strip() if 0 < lineno <= len(
            source_lines) else ""
        key = (target, lineno)
        if key in edges:
            edges[key]["names"] = sorted(
                {*edges[key]["names"], *names})
        else:
            edges[key] = {"target": target, "line": lineno, "stmt": stmt,
                          "names": sorted(names)}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                add(alias.name, node.lineno)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = _relative_base(package, node.level)
                if not base:
                    continue  # 越界相对导入（顶层文件），无法解析为绝对形态
                module = f"{base}.{node.module}" if node.module else base
            else:
                module = node.module or ""
            if module:
                add(module, node.lineno,
                    tuple(alias.name for alias in node.names))
        elif isinstance(node, ast.Call):
            func = node.func
            is_dynamic = (
                (isinstance(func, ast.Name) and func.id == "__import__")
                or (isinstance(func, ast.Attribute)
                    and func.attr == "import_module"))
            if is_dynamic and node.args and isinstance(node.args[0], ast.Constant) \
                    and isinstance(node.args[0].value, str):
                add(node.args[0].value, node.lineno)
    return [edges[key] for key in sorted(edges)]


def build_import_graph(scan_root) -> dict:
    """AST 解析 scan_root 下全部 .py 构建 import 图（只读）。

    Returns:
        {"root": 绝对路径 str,
         "files": {rel_posix: {"module": 点名|None, "imports": [边…]}},
         "counts": {"files": n, "declared_imports": n}}

    Raises:
        ValueError: 根缺失 / 无 .py 文件 / 任一源码解析失败（fail-closed 拒空跑）。
    """
    root = Path(scan_root)
    if not root.is_dir():
        raise ValueError(f"扫描根不存在或非目录: {root}")
    py_files = sorted(p for p in root.rglob("*.py")
                      if "__pycache__" not in p.parts)
    if not py_files:
        raise ValueError(f"扫描根下无 .py 文件，拒绝空跑: {root}")

    files: dict[str, dict] = {}
    total_edges = 0
    for path in py_files:
        rel = _rel_posix(path, root)
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            raise ValueError(
                f"源码解析失败（fail-closed，import 图不可部分构建）: "
                f"{rel}: {exc}") from exc
        edges = _declared_edges(tree, _file_package(rel), text.splitlines())
        files[rel] = {"module": _file_module(rel), "imports": edges}
        total_edges += len(edges)
    return {"root": str(root.resolve()), "files": files,
            "counts": {"files": len(files), "declared_imports": total_edges}}


def _match_member(target: str, zone_members: dict[str, str]) -> list[dict]:
    """声明名命中分区成员（等于成员名或成员名子模块）。"""
    hits = []
    for member, zone in sorted(zone_members.items()):
        if target == member or target.startswith(member + "."):
            hits.append({"imported": target, "member": member, "zone": zone})
    return hits


def _edge_member_hits(edge: dict, zone_members: dict[str, str]) -> list[dict]:
    """一条声明边的成员命中：target 直配 + from 名单组合（P.N）匹配。

    一条边对同一成员至多计一次命中（违例按语句计，不按名单展开次数）。
    """
    hits: list[dict] = []
    seen: set[str] = set()

    def _collect(hit: dict) -> None:
        if hit["member"] not in seen:
            seen.add(hit["member"])
            hits.append(hit)

    for hit in _match_member(edge["target"], zone_members):
        _collect(hit)
    for name in edge.get("names") or ():
        for hit in _match_member(f"{edge['target']}.{name}", zone_members):
            _collect(hit)
    return hits


def _pkg_init_map(graph: dict) -> dict[str, str]:
    """包名 → __init__.py 相对路径（kgenv → kgenv/__init__.py）。"""
    return {info["module"]: rel for rel, info in graph["files"].items()
            if rel.endswith("__init__.py") and info["module"]}


def transitive_member_exposure(target: str, graph: dict,
                               zone_members: dict[str, str]) -> list[dict]:
    """声明边 target 经包 __init__（eager import）/另一成员文件一跳触达的成员。

    一跳披露（非全闭包）：`import kgenv.arena` 经 kgenv/__init__.py 的 eager
    import 触达 economy/redlines/gym_env；`import kgenv.redlines` 经 redlines
    文件触达 economy。target 自身命中成员不算（那是 direct，非 transitive）。
    """
    exposures: set[tuple[str, str]] = set()
    inits = _pkg_init_map(graph)
    # ① target 的各级祖先包（含自身若为包）的 __init__ 声明面（target 自身剔除：
    #    那是 direct 面，不重复计入 transitive）
    parts = target.split(".")
    for i in range(len(parts), 0, -1):
        pkg = ".".join(parts[:i])
        rel_init = inits.get(pkg)
        if rel_init is None:
            continue
        for edge in graph["files"][rel_init]["imports"]:
            for hit in _edge_member_hits(edge, zone_members):
                if hit["member"] != target:
                    exposures.add((hit["member"], rel_init))
    # ② target 即成员 → 其文件声明面触达的其他成员（成员内边，如 redlines→economy）
    if target in zone_members:
        target_file = next(
            (rel for rel, info in graph["files"].items()
             if info["module"] == target), None)
        if target_file is not None:
            for edge in graph["files"][target_file]["imports"]:
                for hit in _edge_member_hits(edge, zone_members):
                    if hit["member"] != target:
                        exposures.add((hit["member"], target_file))
    return [{"member": m, "via": via} for m, via in sorted(exposures)]


def prune_mainline_import_graph(layout_root=None, *, zone_members=None,
                                strict=False) -> tuple[dict, list[dict]]:
    """解析主线布局根 import 图，断言不依赖指定分区成员，返回 (图, 违例清单)。

    Args:
        layout_root: 主线布局根（目录）；None=discover_campaign_roots 定位
            战役根下 fn_work/src（R20：不写字面路径、不依赖 CWD）。
        zone_members: {module id: zone}；None=R13/R14 指定四件
            （DESIGNATED_ZONE_MEMBERS）。
        strict: True 时违例抛 MainlineImportViolationError（violations 附加）；
            False 返回违例清单由调用方裁决。

    Returns:
        (import_graph, violations)：violations 逐条
        {importer, line, stmt, imported, member, zone}。

    Raises:
        ValueError: 布局根缺失/无 .py 文件/源码解析失败（fail-closed）。
        MainlineImportViolationError: strict 且违例非空。
    """
    if layout_root is None:
        layout_root = discover_campaign_roots()["campaign_root"] / "fn_work" \
            / "src"
    members = dict(DESIGNATED_ZONE_MEMBERS if zone_members is None
                   else zone_members)
    if not members:
        raise ValueError("zone_members 为空：断言无对象即空跑，fail-closed 拒绝")
    graph = build_import_graph(layout_root)

    violations: list[dict] = []
    for rel in sorted(graph["files"]):
        for edge in graph["files"][rel]["imports"]:
            for hit in _edge_member_hits(edge, members):
                violations.append({"importer": rel, "line": edge["line"],
                                   "stmt": edge["stmt"], **hit})
    if strict and violations:
        detail = "\n".join(
            f"  {v['importer']}:{v['line']} {v['stmt']!r} → "
            f"{v['member']} ({v['zone']})" for v in violations)
        raise MainlineImportViolationError(
            f"主线 import 图含分区成员 {len(violations)} 处:\n{detail}",
            violations)
    return graph, violations


def scan_legacy_consumers(scan_root, zone_members=None, *, graph=None) -> dict:
    """旧树只读分析：分区成员的当前消费面（designation 依据，零写入）。

    Args:
        scan_root: 旧树根（如 <战役根>/software；只读）。
        zone_members: {module id: zone}；None=DESIGNATED_ZONE_MEMBERS。
        graph: 已建好的该树 import 图（复用调用方构建结果）；None=现建。

    Returns:
        {member_id: {"zone", "direct": [{consumer, line, stmt}],
                     "transitive": [{consumer, via, member}]}}
        consumer/via 为 scan_root 相对 posix 路径；direct 含成员内边
        （如 redlines.py 对 economy 的消费，如实计入 economy 的 direct 面）。
    """
    members = dict(DESIGNATED_ZONE_MEMBERS if zone_members is None
                   else zone_members)
    if graph is None:
        graph = build_import_graph(scan_root)
    module_to_rel = {info["module"]: rel
                     for rel, info in graph["files"].items()}

    # 先收集各文件直接命中的成员（传递面剔重：直接消费者不重复入传递面）
    direct_members: dict[str, set[str]] = {}
    for rel in sorted(graph["files"]):
        hits = {hit["member"]
                for edge in graph["files"][rel]["imports"]
                for hit in _edge_member_hits(edge, members)}
        if hits:
            direct_members[rel] = hits

    result: dict[str, dict] = {}
    for member in sorted(members):
        result[member] = {"zone": members[member], "direct": [], "transitive": []}
    for rel in sorted(graph["files"]):
        for edge in graph["files"][rel]["imports"]:
            for hit in _edge_member_hits(edge, members):
                result[hit["member"]]["direct"].append(
                    {"consumer": rel, "line": edge["line"],
                     "stmt": edge["stmt"]})
            for expo in transitive_member_exposure(edge["target"], graph,
                                                   members):
                if module_to_rel.get(expo["member"]) == rel or expo["via"] == rel:
                    continue  # 成员自身文件/披露源文件不算自己的传递消费者
                if expo["member"] in direct_members.get(rel, set()):
                    continue  # 该文件已直接声明此成员，传递面不重复披露
                result[expo["member"]]["transitive"].append(
                    {"consumer": rel, "via": expo["via"],
                     "member": expo["member"]})
    return result
