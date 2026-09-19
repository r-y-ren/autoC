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

P3 extension (DTSP in-bot runtime, 2026-09-19): the archive also carries the
planner/ package (fixed member order) and the fingerprint-verified scene
pair under planner/scene/ extracted from the vendored wheel at build time --
the runtime loads it zero-write via twin.load_engine_from_scene at dawn.

Determinism: fixed member order (main.py, src modules in load order,
planner modules, scene pair), zeroed mtimes/uid/gid, fixed modes, gzip
mtime 0 -- byte-reproducible archives.  Prints the archive sha256 for
identity-chain registration.
"""
import argparse
import ast
import gzip
import hashlib
import io
import os
import sys
import tarfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
PLANNER = HERE / "planner"
OUT = HERE / "submission.tar.gz"

# Bump when the PACKAGE LAYOUT changes (member set / order / entry shape).
VERSION = "pkg.2-dtsp"

# Flat-namespace load order -- MUST match main.py's _MODULE_ORDER.  The
# src-split era's _archive_header.py is retired from the package (the
# archive comments live in git history; the 64-byte marker moved to
# main.py's first line).
MODULE_ORDER = ["constants", "telemetry", "observer", "strategy", "mission",
                "solver", "executor", "market", "entry"]

# planner/ package members in fixed (dependency) order: twin <- plans /
# opponents / select <- runtime.  Imported as a real package by the thin
# entry at dawn; the flat src namespace never imports it at load time.
PLANNER_ORDER = ["__init__.py", "twin.py", "plans.py", "opponents.py",
                 "select.py", "runtime.py"]

# Bundled scene pair (extracted from the vendored wheel, sha256-verified
# against planner.twin's registered P1 fingerprints before packing).
SCENE_MEMBERS = {"planner/scene/kaggriculture.py": "kaggriculture.py",
                 "planner/scene/kaggriculture.json": "kaggriculture.json"}

# Vendored wheel with the scene files (repo-relative to software/).
VENDOR_RELATIVE = os.path.join("..", "..", "vendor",
                               "kaggle_environments-1.32.7+nodeps-py3-"
                               "none-any.whl")
SCENE_ZIP_MEMBERS = {
    "planner/scene/kaggriculture.py":
        "kaggle_environments/envs/kaggriculture/kaggriculture.py",
    "planner/scene/kaggriculture.json":
        "kaggle_environments/envs/kaggriculture/kaggriculture.json",
}


def scene_bytes_and_sha():
    """Extract + verify the scene pair from the vendored wheel.

    Fail-closed: any sha256 drift against planner.twin's registered P1
    values aborts the build (never pack an unverified engine)."""
    sys.path.insert(0, str(HERE))
    from planner import twin as planner_twin
    wheel_path = os.path.abspath(os.path.join(HERE, VENDOR_RELATIVE))
    if not os.path.isfile(wheel_path):
        sys.exit(f"FAIL vendored wheel missing: {wheel_path}")
    with zipfile.ZipFile(wheel_path) as zf:
        data = {}
        for arc, member in SCENE_ZIP_MEMBERS.items():
            data[arc] = zf.read(member)
    checks = (
        ("planner/scene/kaggriculture.py", data, planner_twin.SCENE_PY_SHA256),
        ("planner/scene/kaggriculture.json", data,
         planner_twin.SCENE_JSON_SHA256))
    for arc, blob, expected in checks:
        got = hashlib.sha256(blob[arc]).hexdigest()
        if got != expected:
            sys.exit(f"FAIL scene fingerprint drift for {arc}: "
                     f"{got} != {expected}")
    if planner_twin.WHEEL_SHA256 != \
            hashlib.sha256(Path(wheel_path).read_bytes()).hexdigest():
        sys.exit("FAIL vendored wheel sha256 drifted from planner.twin "
                 "registration")
    return data


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
    # P3 packaging contract: the DTSP master gate must exist in main.py so
    # the packaged bot actually plans; flag-off equivalence is orthogonal
    # (golden suite execs src without this name).
    if "DTSP_RUNTIME_CONFIG" not in main_src:
        sys.exit("FAIL main.py must define DTSP_RUNTIME_CONFIG (P3 dawn "
                 "hook gate)")
    # P4.1 (2026-09-19): the official loader (get_last_callable) pops the
    # extraction dir off sys.path right after exec -- a turn-time
    # `import planner.runtime` is dead in production (v1 zero-engagement
    # root cause).  main.py must eagerly import the runtime during exec
    # (while the append window is open) and stash it for the entry hook.
    if "DTSP_RUNTIME_MODULE" not in main_src:
        sys.exit("FAIL main.py must define DTSP_RUNTIME_MODULE (P4.1 eager "
                 "planner import; turn-time sys.path import is dead in the "
                 "official loader)")
    for rel in PLANNER_ORDER:
        if not (PLANNER / rel).is_file():
            sys.exit(f"FAIL missing planner member: {PLANNER / rel}")


def build_bytes():
    """Byte-reproducible tar.gz: main.py + src modules (load order)
    + planner package (fixed order) + verified scene pair."""
    members = [(HERE / "main.py", "main.py")]
    for mod in MODULE_ORDER:
        members.append((SRC / f"{mod}.py", f"src/{mod}.py"))
    for rel in PLANNER_ORDER:
        members.append((PLANNER / rel, f"planner/{rel}"))
    scene = scene_bytes_and_sha()
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
        for arcname in sorted(scene):
            data = scene[arcname]
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
    for rel in PLANNER_ORDER:
        source = (PLANNER / rel).read_text(encoding="utf-8")
        compile(source, str(PLANNER / rel), "exec")


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
    print("members: main.py + " + ", ".join(MODULE_ORDER)
          + " + planner(" + ", ".join(PLANNER_ORDER) + ") + scene pair")


if __name__ == "__main__":
    main()
