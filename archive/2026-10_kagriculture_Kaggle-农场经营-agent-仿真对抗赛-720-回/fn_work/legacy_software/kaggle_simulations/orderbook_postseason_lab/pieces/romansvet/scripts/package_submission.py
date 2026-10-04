"""Build dist/submission.tar.gz.

Contract (GOAL.md hard constraints):
  * `main.py` at the archive root, imports resolving under
    /kaggle_simulations/agent/
  * pure numpy at inference -- torch and jax are never imported
  * deterministic: no RNG, no wall-clock branching, fixed tie-breaks
  * the policy runs once per in-game day (30x), not once per turn (720x)

kaggle_environments execs the file and takes the **last callable defined in the
module namespace**, so `agent` must be the final definition in main.py.
"""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import shutil
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "kagg3"
BUILD = ROOT / "build" / "submission"
DIST = ROOT / "dist"

# Inference needs the spec, the shared core, and the numpy agent shell. `sim/`
# and `es/` are training-only and pull in jax, so they are never packaged.
INCLUDE = [
    ("__init__.py", "kagg3/__init__.py"),
    # `__init__` imports this to pin JAX matmul precision; it never imports jax
    # itself, and leaving it out silently breaks the archive -- the agent throws
    # ImportError, kaggle_environments swallows it, and the farm finishes on its
    # starting money. See tests/test_submission_runs.py.
    ("precision.py", "kagg3/precision.py"),
    ("spec.py", "kagg3/spec.py"),
    ("core/__init__.py", "kagg3/core/__init__.py"),
    ("core/ops.py", "kagg3/core/ops.py"),
    ("core/loop.py", "kagg3/core/loop.py"),
    ("core/valuation.py", "kagg3/core/valuation.py"),
    ("core/plan.py", "kagg3/core/plan.py"),
    ("core/projector.py", "kagg3/core/projector.py"),
    ("core/sell.py", "kagg3/core/sell.py"),
    ("core/budget.py", "kagg3/core/budget.py"),
    ("core/policy.py", "kagg3/core/policy.py"),
    ("core/brain.py", "kagg3/core/brain.py"),
    ("agent/__init__.py", "kagg3/agent/__init__.py"),
    ("agent/parse.py", "kagg3/agent/parse.py"),
    ("agent/render.py", "kagg3/agent/render.py"),
    ("agent/runtime.py", "kagg3/agent/runtime.py"),
    ("agent/overflow.py", "kagg3/agent/overflow.py"),
    ("agent/tell.py", "kagg3/agent/tell.py"),
    # runtime.py imports these eagerly (no lazy import inside a game: the engine harness
    # drops repo modules while a file-agent opponent plays). [ROUTEOPT1]
    ("agent/route_nn.py", "kagg3/agent/route_nn.py"),
    ("agent/route_nn3.py", "kagg3/agent/route_nn3.py"),
    ("agent/route_vrp.py", "kagg3/agent/route_vrp.py"),
    # route_vrp loads its C solver from these two (both in the vrp10_esw upload). [PKGFIX1]
    ("agent/route_vrp_c.c", "kagg3/agent/route_vrp_c.c"),
    ("agent/route_vrp_c.so", "kagg3/agent/route_vrp_c.so"),
    # plan.py np.loads the shipped ESWORK_THETA from here at import. [PKGFIX1]
    ("core/eswork_theta.npy", "kagg3/core/eswork_theta.npy"),
]

# Only an --opening build needs these. `main.py` builds its planner inline
# rather than through `runtime.make_agent`, so the plain package never imports
# `opening` and must not carry it -- an OFF build has to stay byte-identical to
# every build made before the splice existed.
OPENING_INCLUDE = [
    ("agent/opening.py", "kagg3/agent/opening.py"),
]

# [V56PACK1] Only a --kernel2 build carries the embedded V56 kernel (runtime KERNEL2, Apache-2.0 source,
# exec'd per game, never imported) and passes the engine configuration through to `Runtime.act` (the kernel
# reads it). A build without the flag is byte-identical to every build before KERNEL2 existed.
KERNEL2_INCLUDE = [
    ("agent/v56kernel.py", "kagg3/agent/v56kernel.py"),
]
_ANCHOR_ACT = "    return rt.act(observation)\n"
_ON_ACT = "    return rt.act(observation, configuration)\n"


# [PACK25] Only a tree whose plan.py ships OPP_SUPPLY_FAMILY_ON = True carries the family supply curves
# (projector.OPP_FAMILY_DIR = kagg3/core/opp_supply/S_<family>.npy, S_OTH for off-list rivals). A tree with the
# switch OFF never reads them, and its build is byte-identical to every build before the curves existed.
OPP_FAMILY_FILES = ("S_MEL.npy", "S_OTH.npy", "S_P48.npy", "S_PQ4.npy", "S_V56.npy", "S_pop.npy")


def opp_family_include() -> list:
    """The opp_supply curve files the tree's OPP_SUPPLY_FAMILY_ON default needs (parsed, never imported)."""
    on = False
    for node in ast.parse((SRC / "core" / "plan.py").read_text()).body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and getattr(node.targets[0], "id", "") == "OPP_SUPPLY_FAMILY_ON"):
            on = bool(ast.literal_eval(node.value))
    if not on:
        return []
    return [("core/opp_supply/" + f, "kagg3/core/opp_supply/" + f) for f in OPP_FAMILY_FILES
            if (SRC / "core" / "opp_supply" / f).exists()]


def kernel2_default() -> bool:
    """The KERNEL2_ON default of the tree being packaged (parsed, never imported)."""
    for node in ast.parse((SRC / "core" / "plan.py").read_text()).body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and getattr(node.targets[0], "id", "") == "KERNEL2_ON"):
            return bool(ast.literal_eval(node.value))
    return False


#: The tape's name inside the archive. Copied byte-identical: it is a leaf
#: module with no relative imports, exec'd exactly as the engine would exec it.
TAPE_NAME = "opening_tape.py"

# --- residual action head [ACTIONRL] ----------------------------------------
# `--residual <head_k.npz>` ships the trained head. Two files and three lines
# in main.py; with no flag NOTHING below runs and the archive is byte-identical
# to one built before the flag existed (the md5 is the test).
#
# `head.py` lands as `kagg3/core/residual_head.py` because that is the name
# `plan._residual_head_module` tries FIRST -- a relative import, so the package
# never has to find the repo. `head.numpy_fn` imports numpy alone, which is
# what keeps `forbidden_imports` green; the weights are a `.npz`, invisible to
# an AST scan and to the no-jax rule alike.
# [PKGFIX1] the shipped module is src/kagg3/core/residual_head.py (md5 5e833774 in vrp10_esw);
# S/actionrl/head.py carries the unshipped RLACT "act" layout and is NOT what ships.
RESIDUAL_HEAD_PY = SRC / "core" / "residual_head.py"

# [PKGFIX1] Defaults = the shipped parameter files (sub 56600971 res940_vrp10_esw), so a bare
# `python scripts/package_submission.py` packages the live policy: theta7659 (md5 94a8ffd2),
# head_940 (md5 769ff15e), and ESWORK_THETA via src/kagg3/core/eswork_theta.npy (md5 6928257a).
# artifacts/theta.npy (md5 328af843) is NOT the shipped theta and is never a default.
DEFAULT_THETA = ROOT / "submission" / "theta.npy"
DEFAULT_RESIDUAL = ROOT / "submission" / "residual_head.npz"
RESIDUAL_MODULE = "kagg3/core/residual_head.py"
RESIDUAL_NPZ = "residual_head.npz"

MAIN = '''"""Kaggriculture submission entrypoint.

Weights in theta.npy are the output of OpenAI-ES over a bit-exact JAX
reimplementation of this environment; nothing here is hand-tuned strategy. The
forward pass is pure numpy and runs once per in-game day.

The turn loop itself is NOT written out here: `agent` only builds the macro
observation and hands the turn to `kagg3.agent.runtime.Runtime`, the same class
the repo's own evaluations drive. This file used to carry a hand-copy of
`Runtime.act`, and the copy fell a patch behind the original -- silently, because
the switch that patch serves was off. Delegation makes that class of drift
impossible: there is one act path, and the archive vendors it.
"""

import inspect
import os
import sys

import numpy as np


def _locate():
    """Directory this agent was loaded from.

    kaggle_environments execs the file through `compile(raw, path, "exec")` with a
    bare globals dict, so `__file__` is absent -- but the compiled code object
    keeps the real path, and the loader only puts the agent's directory on
    sys.path for the duration of that exec. Recover it here and keep it.
    """
    cands = []
    try:
        cands.append(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        pass
    fn = inspect.currentframe().f_code.co_filename
    if fn and not fn.startswith("<"):
        cands.append(os.path.dirname(os.path.abspath(fn)))
    cands.append("/kaggle_simulations/agent")
    cands.append(os.getcwd())
    for c in cands:
        if os.path.isfile(os.path.join(c, "theta.npy")):
            return c
    return cands[0]


_HERE = _locate()
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from kagg3 import spec
from kagg3.agent import parse, runtime as _runtime
from kagg3.core import brain

_THETA = np.load(os.path.join(_HERE, "theta.npy")).astype(np.float32)
_RUNTIMES = {}


def _macro(obs, player, view, prev_mkt_inv):
    opp = obs["farms"][1 - player]
    vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
    po = brain.PolicyObs(
        day=np.int32(view.day), money=view.money,
        opp_money=np.int32(opp["money"]),
        kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
        t_day=view.t_day, t_yield=view.t_yield,
        shed=view.shed, seeds=view.seeds,
        nquad=view.nquad, opp_nquad=np.int32(len(opp["unlocked_quadrants"])),
        mkt_inv=parse.parse_market(obs)[0], price=view.price,
        shops=parse.parse_town(obs),
        # Public: every farm's tiles carry planted_day / placed_day and
        # yield_units; only observation["private"] is withheld. Feeds
        # brain.production_forecast's opponent half.
        opp_t_day=vo.t_day, opp_t_yield=vo.t_yield,
        prev_mkt_inv=prev_mkt_inv,
    )
    return brain.decide(np, _THETA, po)


# NOTE: this must remain the LAST callable defined in the module -- the loader
# picks the final callable in the exec namespace as the agent.
def agent(observation, configuration=None):
    # One `Runtime` per seat, exactly as `runtime.make_agent` keeps them; the
    # splice wrapper `make_agent` adds on top is applied by the build instead,
    # so an OFF package never imports `opening`.
    player = observation.get("player", 0)
    rt = _RUNTIMES.get(player)
    if rt is None:
        rt = _RUNTIMES[player] = _runtime.Runtime(_macro, pass_prev_mkt_inv=True)
    return rt.act(observation)
'''

# --- opening splice ---------------------------------------------------------
# Kaggle runs the archive with no environment of ours, so a package that wants
# the splice has to switch it on itself. The three edits below turn the OFF
# main.py above into an ON one; with no tape they are simply not applied and
# the emitted file is the string above, byte for byte.

_ANCHOR_IMPORTS = '''
from kagg3 import spec
from kagg3.agent import parse, runtime as _runtime
'''

_ON_IMPORTS = '''
# Replay the bundled tape for days [0, K), then hand the board to the planner.
# The spec has to reach os.environ before the agent below is built, and the
# path has to be absolute: kaggle_environments execs this file with a bare
# globals dict from an arbitrary cwd, so a bare name would not resolve.
os.environ.setdefault(
    "KAGG3_OPENING", os.path.join(_HERE, "%s") + ":%d")

from kagg3 import spec
from kagg3.agent import opening as _opening, parse, runtime as _runtime
'''

_ANCHOR_AGENT = '''
# NOTE: this must remain the LAST callable defined in the module -- the loader
# picks the final callable in the exec namespace as the agent.
def agent(observation, configuration=None):
'''

_ON_AGENT = '''
def _planner(observation, configuration=None):
'''

# --- residual splice --------------------------------------------------------
# One anchor, one replacement, applied to whichever main.py the opening splice
# produced: the residual is orthogonal to the opening and the two compose.

_ANCHOR_THETA = '''
_THETA = np.load(os.path.join(_HERE, "theta.npy")).astype(np.float32)
_RUNTIMES = {}
'''

_ON_RESIDUAL = '''
_THETA = np.load(os.path.join(_HERE, "theta.npy")).astype(np.float32)

# The residual action head [ACTIONRL]: a 2x64 numpy MLP that may move the
# planner's plant / animal / hire / hold counts inside a fixed clamp, and is
# re-clamped by `plan._residual_override` on the other side. `residual_on()`
# loads the weights lazily on the first planned day, so the import graph here
# is unchanged and this file still imports nothing but numpy.
from kagg3.core import plan as _plan

_plan.RESIDUAL_ON = True
_plan.RESIDUAL_HEAD = os.path.join(_HERE, "%s")

_RUNTIMES = {}
'''

_ON_TAIL = '''

_SPLICED = _opening.from_env(_planner)


# NOTE: this must remain the LAST callable defined in the module -- the loader
# picks the final callable in the exec namespace as the agent. A plain `def`,
# not the splice object itself: the loader trims its argument list by
# `agent.__code__.co_argcount`, which a callable instance does not have.
def agent(observation, configuration=None):
    return _SPLICED(observation, configuration)
'''


def main_source(opening_days: int = 0, residual: bool = False, kernel2: bool = False) -> str:
    """The package `main.py`.

    Both splices OFF returns the template text unchanged, which is the whole
    contract: an OFF build has to stay byte-identical to every build made
    before either splice existed.
    """
    src = MAIN
    if opening_days > 0:
        if _ANCHOR_IMPORTS not in src or _ANCHOR_AGENT not in src:
            raise AssertionError("main.py template drifted from the opening anchors")
        src = src.replace(_ANCHOR_IMPORTS, _ON_IMPORTS % (TAPE_NAME, opening_days), 1)
        src = src.replace(_ANCHOR_AGENT, _ON_AGENT, 1) + _ON_TAIL
    if residual:
        if _ANCHOR_THETA not in src:
            raise AssertionError("main.py template drifted from the residual anchor")
        src = src.replace(_ANCHOR_THETA, _ON_RESIDUAL % RESIDUAL_NPZ, 1)
    if kernel2:
        if src.count(_ANCHOR_ACT) != 1:
            raise AssertionError("main.py template drifted from the kernel2 anchor")
        src = src.replace(_ANCHOR_ACT, _ON_ACT, 1)
    return src


def build(theta_path: Path, out: Path, opening: Path | None = None,
          opening_days: int = 0, residual: Path | None = None, kernel2: bool | None = None) -> Path:
    if kernel2 is None:   # [V56PACK1] a library build follows the tree's KERNEL2_ON default
        kernel2 = kernel2_default()
    if BUILD.exists():
        shutil.rmtree(BUILD)
    include = (list(INCLUDE) + (list(OPENING_INCLUDE) if opening else [])
               + (list(KERNEL2_INCLUDE) if kernel2 else []) + opp_family_include())
    for rel, dest in include:
        d = BUILD / dest
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / rel, d)
    (BUILD / "main.py").write_text(
        main_source(opening_days if opening else 0, residual is not None, kernel2))
    if opening:
        shutil.copy2(opening, BUILD / TAPE_NAME)
    if residual is not None:
        shutil.copy2(RESIDUAL_HEAD_PY, BUILD / RESIDUAL_MODULE)
        shutil.copy2(residual, BUILD / RESIDUAL_NPZ)
    shutil.copy2(theta_path, BUILD / "theta.npy")
    shutil.copy2(ROOT / "vendor" / "engine.lock.json", BUILD / "engine.lock.json")

    DIST.mkdir(exist_ok=True)
    # Deterministic archive: sorted entries, zeroed mtime/uid/gid -- and a gzip
    # header written with mtime=0. "w:gz" stamps the *current* time in that
    # header, which alone made two builds of identical inputs differ, so the
    # sha256 printed below could not identify what was uploaded.
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as raw, gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as gz, \
            tarfile.open(fileobj=gz, mode="w") as tf:
        for path in sorted(BUILD.rglob("*")):
            info = tf.gettarinfo(str(path), arcname=str(path.relative_to(BUILD)))
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            if path.is_file():
                with open(path, "rb") as fh:
                    tf.addfile(info, fh)
            else:
                tf.addfile(info)
    return out


def forbidden_imports() -> list[str]:
    """Real import statements only.

    A substring scan for "import jax" also fires on prose -- `precision.py`
    explains that the archive "must not import jax at all" -- so the gate is
    parsed, not grepped. ast also catches forms a substring misses, like
    `import jax.numpy as jnp` nested inside a function.
    """
    bad = []
    for path in sorted(BUILD.rglob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                root = name.split(".")[0]
                if root in ("jax", "torch", "tensorflow"):
                    bad.append(f"{path.relative_to(BUILD)}:{node.lineno}: imports {root}")
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", default=str(DEFAULT_THETA))
    ap.add_argument("--out", default=str(DIST / "submission.tar.gz"))
    ap.add_argument("--opening", default=None,
                    help="tape main.py to replay for the first --opening-days days")
    ap.add_argument("--opening-days", type=int, default=0,
                    help="K: days [0, K) come from the tape, K.. from the planner")
    ap.add_argument("--residual", default=str(DEFAULT_RESIDUAL),
                    help="head_k.npz: ship the residual action head, RESIDUAL_ON=True "
                         "(default: the shipped head_940)")
    ap.add_argument("--no-residual", action="store_true",
                    help="build without the residual head (RESIDUAL_ON stays False)")
    ap.add_argument("--kernel2", action="store_true",
                    help="[V56PACK1] ship the embedded V56 kernel (implied when plan.KERNEL2_ON defaults True; "
                         "refused on a tree whose default is OFF)")
    args = ap.parse_args()
    if args.kernel2 and not kernel2_default():
        ap.error("--kernel2 but plan.KERNEL2_ON default is False")
    args.kernel2 = kernel2_default()

    if args.opening and args.opening_days <= 0:
        ap.error("--opening needs --opening-days K with K > 0")
    if args.opening_days and not args.opening:
        ap.error("--opening-days needs --opening")

    opening = Path(args.opening) if args.opening else None
    residual = None if args.no_residual else Path(args.residual)
    if residual is not None and not residual.is_file():
        ap.error(f"--residual: no head at {residual}")
    out = build(Path(args.theta), Path(args.out), opening, args.opening_days,
                residual, args.kernel2)
    bad = forbidden_imports()
    if bad:
        print("FORBIDDEN IMPORTS:", *bad, sep="\\n  ")
        sys.exit(1)
    size = out.stat().st_size
    if args.kernel2:
        print("kernel2: agent/v56kernel.py -> kagg3/agent/v56kernel.py, main.py passes configuration, KERNEL2_ON=True")
    if opening:
        print(f"opening: {opening} -> {TAPE_NAME}, days [0, {args.opening_days})")
    if residual is not None:
        print(f"residual: {residual} -> {RESIDUAL_NPZ}, "
              f"{RESIDUAL_HEAD_PY.name} -> {RESIDUAL_MODULE}, RESIDUAL_ON=True")
    print(f"{out}  {size/1e6:.2f} MB  sha256={hashlib.sha256(out.read_bytes()).hexdigest()}")
    assert size < 100 * 1024 * 1024, "submission exceeds the 100 MiB limit"
