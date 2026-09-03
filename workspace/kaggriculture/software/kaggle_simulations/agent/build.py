#!/usr/bin/env python
"""Deterministic builder: merges the src/* fragments into main.py.

Usage (from anywhere):
    python build.py           # rebuild agent/main.py in place
    python build.py --check   # rebuild in memory, byte-compare with disk

Contract (see docs/worker_route_scheduler_design.md and JOURNAL 2026-09-02):
  * Flat-namespace merge in a FIXED topological order; src modules never
    import each other -- the merged file is one namespace, exactly like the
    pre-refactor single file. entry.py is merged last so `agent(obs)` is the
    final callable (official kaggle_environments get_last_callable semantics).
  * Byte-deterministic: no timestamps, fixed order, LF endings, utf-8. The
    only import-time side effects (all verified self-contained) are the
    telemetry/state dict inits, the _FIB_CUM fill loop and
    _WHEAT_FARM_PLAN = _wheat_farm_plan() (constants-first order covers it).
  * stdlib-only output: import whitelist {copy, math, json, hashlib}.
  * Prints sha256 + canonical LF sha256 of the artifact for identity-chain
    registration (software/active_candidate.json).
"""
import argparse
import ast
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = HERE / "main.py"

# Bump when the merge LAYOUT changes (module set / order / header format).
VERSION = "src-split.1"

# Topological order. _archive_header first (keeps the v10.9 archive comments
# and the module docstring in place), entry.py ALWAYS last.
MERGE_ORDER = [
    "_archive_header", "constants", "telemetry", "observer", "strategy",
    "mission", "solver", "executor", "market", "entry",
]

ALLOWED_IMPORTS = {"copy", "math", "json", "hashlib"}

META_LINES = [
    "# " + "=" * 74,
    "# Kaggriculture submission agent -- BUILT ARTIFACT, DO NOT EDIT DIRECTLY.",
    "# Edit src/*.py, then rebuild:  python build.py   (deterministic merge)",
    "# layout " + VERSION + " -- merge order: " + " -> ".join(MERGE_ORDER),
    "# " + "=" * 74,
    "",
]

IMPORT_BLOCK = "import copy\nimport math\n"


def fragment_names(path):
    """Top-level bound names of a fragment: (module, name) pairs.

    Within one module rebinding is allowed (e.g. _WHEAT_FARM_PLAN = None
    then the real plan); the SAME name bound in two different modules would
    silently shadow in the flat namespace and is a hard error.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    pairs = []
    for st in tree.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            pairs.append(st.name)
        elif isinstance(st, ast.Assign):
            for tgt in st.targets:
                for node in ast.walk(tgt):
                    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                        pairs.append(node.id)
        elif isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name):
            pairs.append(st.target.id)
    return pairs


def precheck():
    """Cross-module duplicate-name detection (silent-shadowing guard)."""
    seen = {}
    duplicates = []
    for mod in MERGE_ORDER:
        path = SRC / f"{mod}.py"
        if not path.is_file():
            sys.exit(f"FAIL missing fragment: {path}")
        for name in fragment_names(path):
            if name in seen and seen[name] != mod:
                duplicates.append((name, seen[name], mod))
            seen.setdefault(name, mod)
    if duplicates:
        for name, first, second in duplicates:
            print(f"DUPLICATE top-level name {name!r}: {first}.py vs {second}.py")
        sys.exit("FAIL cross-module duplicate names would shadow in the merge")
    # executor authority: _execute_routes may only be referenced by the
    # dispatcher (solver's _solve_and_execute) and the entry wiring --
    # no other module may grow a private execution path
    for mod in MERGE_ORDER:
        if mod in ("executor", "solver", "entry"):
            continue
        text = (SRC / f"{mod}.py").read_text(encoding="utf-8")
        if "_execute_routes" in text:
            sys.exit(f"FAIL {mod}.py references _execute_routes "
                     "(only solver's dispatcher and entry may)")


def build_bytes():
    parts = ["\n".join(META_LINES)]
    for mod in MERGE_ORDER:
        text = (SRC / f"{mod}.py").read_text(encoding="utf-8")
        if not text.endswith("\n"):
            text += "\n"
        parts.append(f"# ===== src/{mod}.py " + "=" * 49 + "\n")
        parts.append(text)
        if mod == "_archive_header":
            # hoisted stdlib imports, AFTER the archive docstring so it stays
            # the module docstring (first statement of the file)
            parts.append(IMPORT_BLOCK)
    body = "\n".join(parts)
    # single trailing newline; all fragments already end with one
    return body.encode("utf-8")


def postcheck(data):
    try:
        tree = ast.parse(data.decode("utf-8"))
    except SyntaxError as exc:
        sys.exit(f"FAIL merged file does not parse: {exc}")
    compile(data.decode("utf-8"), str(OUT), "exec")

    imports = set()
    for st in tree.body:
        if isinstance(st, ast.Import):
            imports |= {a.name for a in st.names}
        elif isinstance(st, ast.ImportFrom):
            sys.exit(f"FAIL non-absolute import in merged file: {ast.dump(st)}")
    if imports != ALLOWED_IMPORTS:
        sys.exit(f"FAIL imports must be exactly {sorted(ALLOWED_IMPORTS)}, "
                 f"got {sorted(imports)}")

    last = tree.body[-1]
    if not (isinstance(last, ast.FunctionDef) and last.name == "agent"):
        sys.exit("FAIL last top-level statement is not `def agent` "
                 "(get_last_callable contract)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="compare a rebuild against the on-disk main.py")
    args = ap.parse_args()

    precheck()
    data = build_bytes()
    postcheck(data)

    if args.check:
        on_disk = OUT.read_bytes() if OUT.is_file() else b""
        if data != on_disk:
            sys.exit("FAIL on-disk main.py differs from the deterministic "
                     "rebuild (hand edit? run: python build.py)")
        print(f"OK main.py matches deterministic rebuild "
              f"({len(data)} bytes, layout {VERSION})")
        return

    OUT.write_bytes(data)  # explicit bytes, LF, utf-8 (Windows-safe)
    sha = hashlib.sha256(data).hexdigest()
    lf = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
    print(f"built {OUT} ({len(data)} bytes, layout {VERSION})")
    print(f"sha256           = {sha}")
    print(f"canonical_lf_sha = {lf}")


if __name__ == "__main__":
    main()
