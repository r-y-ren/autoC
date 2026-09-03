#!/usr/bin/env python
"""Deterministic submission packager (multi-module tar.gz era, v13.1+).

Usage (from anywhere):
    python build.py           # package submission.tar.gz next to main.py
    python build.py --check   # rebuild in memory, byte-compare with disk

Contract change (user ruling 2026-09-03): the submission is a MULTI-MODULE
tar.gz archive (officially supported -- kaggle_environments.get_last_callable
appends the extraction dir to sys.path "so that way python agents can import
other files").  The static single-file merge is RETIRED; main.py is a thin
entry that loads agent/src/*.py in a fixed topological order into one flat
namespace at import time (identical semantics, merge point moved from build
time to import time; tracebacks now point at the real module files).

Determinism: fixed member order (main.py, then src modules in load order),
zeroed mtimes/uid/gid, fixed modes, gzip mtime 0 -- byte-reproducible archives.
Prints the archive sha256 for identity-chain registration.
"""
import argparse
import ast
import gzip
import hashlib
import io
import os
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = HERE / "submission.tar.gz"

# Bump when the PACKAGE LAYOUT changes (member set / order / entry shape).
VERSION = "pkg.1"

# Flat-namespace load order -- MUST match main.py's _MODULE_ORDER.  The
# src-split era's _archive_header.py is retired from the package (the
# archive comments live in git history; the 64-byte marker moved to
# main.py's first line).
MODULE_ORDER = ["constants", "telemetry", "observer", "strategy", "mission",
                "solver", "executor", "market", "entry"]


def fragment_names(path):
    """Top-level bound names of a fragment (cross-module shadowing guard)."""
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
    seen = {}
    duplicates = []
    for mod in MODULE_ORDER:
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
        sys.exit("FAIL cross-module duplicate names would shadow in the "
                 "flat namespace")
    # entry contract lives in main.py itself now
    main_src = (HERE / "main.py").read_text(encoding="utf-8")
    tree = ast.parse(main_src)
    defs = [st.name for st in tree.body
            if isinstance(st, ast.FunctionDef)]
    if not defs or defs[-1] != "agent":
        sys.exit("FAIL main.py's last top-level def must be `agent` "
                 "(get_last_callable contract)")
    if "Kaggriculture submission agent" not in main_src[:64]:
        sys.exit("FAIL main.py must keep the 64-byte submission marker")


def build_bytes():
    """Byte-reproducible tar.gz: main.py + src modules in load order."""
    members = [(HERE / "main.py", "main.py")]
    for mod in MODULE_ORDER:
        members.append((SRC / f"{mod}.py", f"src/{mod}.py"))
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for path, arcname in members:
            data = path.read_bytes()
            info = tarfile.TarInfo(arcname)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    raw = buf.getvalue()
    gz = io.BytesIO()
    with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0) as z:
        z.write(raw)
    return gz.getvalue()


def postcheck():
    for mod in MODULE_ORDER:
        source = (SRC / f"{mod}.py").read_text(encoding="utf-8")
        compile(source, str(SRC / f"{mod}.py"), "exec")
    compile((HERE / "main.py").read_text(encoding="utf-8"),
            str(HERE / "main.py"), "exec")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="compare a rebuild against the on-disk archive")
    args = ap.parse_args()

    precheck()
    postcheck()
    data = build_bytes()

    if args.check:
        on_disk = OUT.read_bytes() if OUT.is_file() else b""
        if data != on_disk:
            sys.exit("FAIL on-disk submission.tar.gz differs from the "
                     "deterministic rebuild (hand edit? run: python build.py)")
        print(f"OK submission.tar.gz matches deterministic rebuild "
              f"({len(data)} bytes, layout {VERSION})")
        return

    OUT.write_bytes(data)
    print(f"packaged {OUT} ({len(data)} bytes, layout {VERSION})")
    print(f"sha256 = {hashlib.sha256(data).hexdigest()}")
    print("members: main.py + " + ", ".join(MODULE_ORDER))


if __name__ == "__main__":
    main()
