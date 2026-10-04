"""Extract the generic licensed chassis without v6 route-specific overlays.

This creates reusable library source, not an agent submission. A builder must
append routes, a router, and the last callable entry point before using it.
"""
import ast
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / "external/one_more_wheat.py").read_text(encoding="utf-8")
tree = ast.parse(source)
factory = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "make_agent")
core = "".join(source.splitlines(keepends=True)[:factory.end_lineno])
core += "\n# Extracted from the frozen One More Wheat source on 2026-09-22.\n"
core += "# Upstream Apache-2.0 notices are retained above. Generic library only.\n"
path = root / "experiments/round7_local_chassis_core.py"
path.write_text(core, encoding="utf-8", newline="\n")
compile(core, str(path), "exec")
print(f"{path}: {len(core.encode('utf-8'))} bytes")
