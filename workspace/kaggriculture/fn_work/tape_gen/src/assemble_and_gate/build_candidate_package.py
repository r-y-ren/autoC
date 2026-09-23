"""build_candidate_package（L1，R6）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

候选包 = 换 RouteLibrary 字节进 v48 执行外壳（只读基底
``fn_work/legacy_software/kaggle_simulations/v48_derivative/main.py``，
dadee25a…2664a，107,008B）：

* **手术面 = 唯一的 ``_V48_ROUTES`` 路由 blob**（zlib+base85 内嵌 JSON）。
  机制区（``_V48_MODULES`` 模块源 blob、``_V48_CONFIG`` 路由器事件窗、
  ``_V48_GOLD_CONFIG`` 反射层参数、装载器/入口）与反射层逐字节保留——
  由前后缀逐字节一致自证（build_v6b.py 同法）。
* **配置面零改**：最终件配置（final_selection.json）与外壳缺省一致性
  fail-closed 校验——clone_preempt=on 即外壳 ``clone_preempt_horizon=2``
  本就开、``clone_streak_required=24`` 同缺省；market_maker/slot_reorder/
  dead_price_guard 外壳本就未接线（=关）。一致 → 只换库；不一致 → 拒绝
  出包（配置手术超出声明的手术面）。
* **路由器语义登记（实测）**：v48 ``fast_route_router.build_fast_route_router``
  对路由字典做 ``set(routes) != {6 路由名}`` **build 时 fail-closed**——
  字面 2 路由库直接喂会 ValueError（T2 证的"载入兼容"是
  ``v23.policy_library``/磁带回放形态）。因此 6 槽 **别名填充**：全部
  路由器槽 ← 库最终件磁带（逐字节同一条）→ 任何路由事件切换后落到的
  磁带与 default 完全相同，**行为等价于"事件不匹配时保持 default"**。
  库的 fork 路由（fork_s73_e72，触发步 72）早于全部路由器事件窗
  （88/120/153/216/160）且机制区零改禁改 route_event——按库登记但
  不接线（最终件本就未选它）。
* 确定性打包：canonical JSON、双跑 build 逐字节一致、tar 单 main.py
  全零元数据（build.py pack_tar 同口径）、blob 编码回路 == 库。

产物：``fn_work/tape_gen/candidate/{main.py, submission.tar.gz,
manifest.json}``。错误：基底 sha/体积漂移、库/最终件缺失、路由非 719
步、配置不一致、手术越界、非确定性——全部 fail-closed。
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import re
import tarfile
import zlib
from pathlib import Path

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
_KSIM = (_CAMPAIGN_ROOT / "fn_work" / "legacy_software"
         / "kaggle_simulations")

#: 只读执行外壳（v48_derivative，R2 基座冻结面）。
SHELL_MAIN = _KSIM / "v48_derivative" / "main.py"
SHELL_SHA256 = ("dadee25a9840313218384208c53b2c4752f82c3209"
                "cc654632e0b96c65e2664a")
SHELL_BYTES = 107008

DEFAULT_LIBRARY_DIR = _TAPE_GEN_ROOT / "library"
DEFAULT_SELECTION_PATH = _TAPE_GEN_ROOT / "search" / "final_selection.json"
DEFAULT_OUTPUT_DIR = _TAPE_GEN_ROOT / "candidate"

#: v48 fast_route_router 构建契约要求的 6 路由名（ROUTES 真值转录）。
ROUTER_SLOTS = ("default", "yarn_fast", "farm_fast", "yarn_second",
                "yarn_third", "bakery_capital")

N_STEPS = 719

#: ``_V48_ROUTES`` blob 定位与编解码（tape_surgery_v2 同式，独立内联——
#: 磁带手术正则属本管线契约面，不 import 旧树脚本）。
_ROUTES_RE = re.compile(
    r"_V48_ROUTES = json\.loads\(zlib\.decompress\(base64\.b85decode\(\n"
    r"\(\n"
    r"(.*?)"
    r"\n\)\n\)\)\.decode\(\"utf-8\"\)\)",
    re.S,
)
_B85_WIDTH = 78


class PackageError(RuntimeError):
    """候选包构建 fail-closed。"""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _dump_routes(routes) -> str:
    """T2 build_route_library 同口径 canonical dump（跨阶段哈希对账用）。"""
    return json.dumps(routes, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def decode_blob_body(body: str):
    """blob 文本体（引号行串）→ 路由字典。"""
    text = "".join(re.findall(r"'([^']*)'", body))
    return json.loads(zlib.decompress(
        base64.b85decode(text)).decode("utf-8"))


def encode_blob_body(routes) -> str:
    """路由字典 → blob 文本体（与外壳既有编码同形：b85(zlib(compact JSON))
    78 列引号行）。"""
    payload = json.dumps(routes, ensure_ascii=True,
                         separators=(",", ":")).encode("ascii")
    text = base64.b85encode(zlib.compress(payload, 9)).decode("ascii")
    return "\n".join(f"    '{text[i:i + _B85_WIDTH]}'"
                     for i in range(0, len(text), _B85_WIDTH))


def _shell_gold_config(base_text: str) -> dict:
    """从外壳源文本提取 ``_V48_GOLD_CONFIG`` 关键缺省（防手抄漂移）。"""
    m = re.search(r"_V48_GOLD_CONFIG = _V48GoldConfig\(\*\*(.*?)\)\n",
                  base_text, re.S)
    if not m:
        raise PackageError("_V48_GOLD_CONFIG literal not found in shell")
    body = m.group(1)

    def _int(key):
        mm = re.search(rf"'{key}':\s*(-?\d+)", body)
        if not mm:
            raise PackageError(f"shell gold config missing {key}")
        return int(mm.group(1))

    return {
        "clone_preempt_horizon": _int("clone_preempt_horizon"),
        "clone_streak_required": _int("clone_streak_required"),
    }


def _load_inputs(payload):
    library_dir = Path(payload.get("library_dir") or DEFAULT_LIBRARY_DIR)
    routes_path = library_dir / "routes.json"
    if not routes_path.is_file():
        raise PackageError(f"library routes.json missing (fail-closed): "
                           f"{routes_path}")
    routes = payload.get("routes")
    if routes is None:
        routes = json.loads(routes_path.read_text(encoding="utf-8"))
    for name, steps in routes.items():
        if not isinstance(steps, list) or len(steps) != N_STEPS:
            raise PackageError(f"route {name} must be {N_STEPS} steps "
                               f"(fail-closed)")

    selection = payload.get("selection")
    if selection is None:
        sel_path = Path(payload.get("selection_path")
                        or DEFAULT_SELECTION_PATH)
        if not sel_path.is_file():
            raise PackageError(f"final_selection.json missing "
                               f"(fail-closed): {sel_path}")
        selection = json.loads(sel_path.read_text(encoding="utf-8"))
    return routes, selection, routes_path


def _check_config_matches_shell(selection, shell_gold) -> dict:
    """最终件配置 vs 外壳缺省（一致才允许只换库；R6 手术面声明）。"""
    switches = selection.get("switches") or {}
    thresholds = selection.get("thresholds") or {}
    shell_preempt_on = shell_gold["clone_preempt_horizon"] > 0
    problems = []
    if bool(switches.get("clone_preempt")) != shell_preempt_on:
        problems.append(f"clone_preempt={switches.get('clone_preempt')} != "
                        f"shell horizon "
                        f"{shell_gold['clone_preempt_horizon']}")
    if int(thresholds.get("clone_streak_required", -1)) != \
            shell_gold["clone_streak_required"]:
        problems.append(f"clone_streak_required="
                        f"{thresholds.get('clone_streak_required')} != "
                        f"shell {shell_gold['clone_streak_required']}")
    for name in ("slot_reorder", "market_maker", "dead_price_guard"):
        if switches.get(name):
            problems.append(f"{name}=on but shell never wires it")
    if problems:
        raise PackageError(
            "final selection config diverges from shell defaults — "
            "config surgery would leave the declared surgical face "
            f"(fail-closed): {'; '.join(problems)}")
    return {
        "shell_clone_preempt_horizon": shell_gold["clone_preempt_horizon"],
        "shell_clone_streak_required": shell_gold["clone_streak_required"],
        "selection_matches_shell_defaults": True,
        "surgical_face": "library_blob_only",
        "note": "clone_preempt=on 是外壳缺省本就开；其余开关外壳未接线"
                "=关；终局清仓/杂草修复属外壳机制基底非消融轴——配置面零改",
    }


def _slot_map(routes, selection) -> dict:
    """6 路由器槽 ← 最终件磁带（别名填充；见模块 docstring 语义登记）。"""
    piece = selection.get("piece") or ""
    if not piece.startswith("route:"):
        raise PackageError(f"final piece must be a route piece, got "
                           f"{piece!r} (fail-closed)")
    route_name = piece[len("route:"):]
    if route_name not in routes:
        raise PackageError(f"final piece route missing from library "
                           f"(fail-closed): {route_name}")
    tape = routes[route_name]
    return {slot: tape for slot in ROUTER_SLOTS}


def _pack_tar(source: bytes) -> bytes:
    """确定性 tar.gz（v48_hybrid build.pack_tar 同口径：单 main.py、
    全零元数据、gzip mtime=0）。"""
    import gzip
    buf = io.BytesIO()
    gz = gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0)
    with tarfile.open(fileobj=gz, mode="w") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(source)
        info.mode = 0o644
        info.mtime = 0
        info.uid = 0
        info.gid = 0
        tar.addfile(info, io.BytesIO(source))
    gz.close()
    return buf.getvalue()


def _build_once(payload) -> dict:
    """单次构建（纯函数）：返回 main/tar 字节与手术面证据。"""
    base_path = Path(payload.get("base_main") or SHELL_MAIN)
    base_bytes = base_path.read_bytes()
    if len(base_bytes) != SHELL_BYTES or \
            _sha256_bytes(base_bytes) != SHELL_SHA256:
        raise PackageError(f"shell base drift (fail-closed): "
                           f"{base_path} sha="
                           f"{_sha256_bytes(base_bytes)}")
    base_text = base_bytes.decode("utf-8")

    routes, selection, routes_path = _load_inputs(payload)
    shell_gold = _shell_gold_config(base_text)
    config_check = _check_config_matches_shell(selection, shell_gold)
    slot_map = _slot_map(routes, selection)

    m = _ROUTES_RE.search(base_text)
    if not m:
        raise PackageError("_V48_ROUTES blob not found in shell")
    lo, hi = m.span(1)
    body_new = encode_blob_body(slot_map)
    surgered = base_text[:lo] + body_new + base_text[hi:]

    # ---- 手术面自证 ----
    if surgered[:lo] != base_text[:lo] or \
            surgered[lo + len(body_new):] != base_text[hi:]:
        raise PackageError("surgery leaked outside the routes blob span "
                           "(fail-closed)")
    main_bytes = surgered.encode("utf-8")
    compile(main_bytes, "main.py", "exec")
    m2 = _ROUTES_RE.search(surgered)
    if decode_blob_body(m2.group(1)) != slot_map:
        raise PackageError("blob encode/decode roundtrip mismatch "
                           "(fail-closed)")
    tar_bytes = _pack_tar(main_bytes)
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        names = tar.getnames()
        inner = tar.extractfile("main.py").read()
    if names != ["main.py"] or inner != main_bytes:
        raise PackageError("tar member/byte mismatch (fail-closed)")

    return {
        "main_bytes": main_bytes,
        "tar_bytes": tar_bytes,
        "span": [lo, lo + len(body_new)],
        "orig_span": [lo, hi],
        "routes": routes,
        "selection": selection,
        "shell_gold": shell_gold,
        "config_check": config_check,
        "slot_map": slot_map,
        "routes_path": routes_path,
        "base_path": base_path,
    }


def build_candidate_package(payload=None):
    """意图级签名；真值在责任文档。

    payload 可覆盖：library_dir / routes / selection_path / selection /
    base_main / output_dir / package_id / skip_write。返回 manifest
    （含 paths 与全部身份哈希）。
    """
    payload = dict(payload or {})
    first = _build_once(payload)
    second = _build_once(payload)          # 双跑确定性自证
    if first["main_bytes"] != second["main_bytes"] or \
            first["tar_bytes"] != second["tar_bytes"]:
        raise PackageError("build is not deterministic (fail-closed)")

    main_bytes, tar_bytes = first["main_bytes"], first["tar_bytes"]
    routes, selection = first["routes"], first["selection"]
    slot_map = first["slot_map"]

    fork_names = [name for name in routes if name not in ROUTER_SLOTS]
    library_manifest = {}
    lib_manifest_path = (Path(payload.get("library_dir")
                              or DEFAULT_LIBRARY_DIR)
                         / "library_manifest.json")
    if lib_manifest_path.is_file():
        library_manifest = json.loads(
            lib_manifest_path.read_text(encoding="utf-8"))
    routes_canonical_sha = _sha256_bytes(_dump_routes(routes).encode("utf-8"))
    if library_manifest.get("routes_sha256") not in (None,
                                                     routes_canonical_sha):
        raise PackageError("library_manifest routes_sha256 mismatch vs "
                           "routes.json (fail-closed)")

    manifest = {
        "package_id": payload.get("package_id") or "tapegen-c1",
        "variant": {
            "name": "tape_gen candidate package",
            "assembler": "assemble_and_gate/build_candidate_package.py",
            "rationale": "R6：T2 路由库最终件（T3 留出裁决 route:default"
                         "+clone_preempt）换字节进 v48 执行外壳；机制区/"
                         "反射层零改；配置面与外壳缺省一致故只换库",
        },
        "base": {
            "path": str(first["base_path"]),
            "sha256": SHELL_SHA256,
            "bytes": SHELL_BYTES,
            "readonly": True,
        },
        "surgical_face": {
            "kind": "routes_blob_swap",
            "blob_span": first["span"],
            "orig_blob_span": first["orig_span"],
            "prefix_suffix_byte_identical": True,
            "mechanism_zone": "byte-identical (_V48_MODULES/_V48_CONFIG/"
                              "_V48_GOLD_CONFIG/loader/entry)",
            "reflection_layers": "byte-identical (gold preemption/"
                                 "terminal liquidation/weed repair)",
            "config_face": first["config_check"],
        },
        "router_semantics": {
            "required_route_names": list(ROUTER_SLOTS),
            "literal_library_dict": (
                "fail-closed: build_fast_route_router 对 set(routes)!="
                "{6 名} build 时 ValueError（实测；T2 所证载入兼容是"
                "policy_library/磁带回放形态，非 fast_route_router）"),
            "slot_fill": "alias: 全部 6 槽 ← 最终件磁带（逐字节同一条）",
            "behavior": "任何路由事件切换后落到的磁带与 default 逐字节"
                        "相同——磁带行为等价于事件不匹配时保持 default；"
                        "唯一跨名副作用=CloneSellPreemption 在换名步清空"
                        "due 债（v48 原生机制区设计，未改动；门禁数字对"
                        "整包端到端实测，含该行为）",
            "fork_routes_unwired": {
                name: {
                    "wired": False,
                    "reason": "触发步早于全部路由器事件窗"
                              "(88/120/153/216/160)；机制区零改禁改 "
                              "route_event；最终件本就未选它",
                } for name in fork_names},
        },
        "library": {
            "routes_path": str(first["routes_path"]),
            "n_routes": len(routes),
            "route_names": sorted(routes),
            "routes_canonical_sha256": routes_canonical_sha,
            "library_manifest_routes_sha256":
                library_manifest.get("routes_sha256"),
            "final_piece": selection.get("piece"),
        },
        "selection": {
            "candidate_id": selection.get("candidate_id"),
            "piece": selection.get("piece"),
            "switches": selection.get("switches"),
            "thresholds": selection.get("thresholds"),
            "selection_sha256": selection.get("selection_sha256"),
        },
        "products": {
            "main_py": {"bytes": len(main_bytes),
                        "sha256": _sha256_bytes(main_bytes)},
            "submission_tar_gz": {"bytes": len(tar_bytes),
                                  "sha256": _sha256_bytes(tar_bytes),
                                  "members": ["main.py"]},
        },
        "deterministic_double_build": True,
        "blob_roundtrip_ok": True,
        "stdlib_only": True,
        "router_semantics_slot_map_sha256": {
            slot: _sha256_bytes(_dump_routes(slot_map[slot])
                                .encode("utf-8"))
            for slot in ROUTER_SLOTS},
    }

    output_dir = Path(payload.get("output_dir") or DEFAULT_OUTPUT_DIR)
    if not payload.get("skip_write"):
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "main.py").write_bytes(main_bytes)
        (output_dir / "submission.tar.gz").write_bytes(tar_bytes)
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2,
                       sort_keys=True) + "\n", encoding="utf-8")
    manifest["paths"] = {
        "main": str(output_dir / "main.py"),
        "tar": str(output_dir / "submission.tar.gz"),
        "manifest": str(output_dir / "manifest.json"),
        "output_dir": str(output_dir),
    }
    return manifest


def _cli() -> int:
    import sys
    manifest = build_candidate_package()
    print(json.dumps({k: manifest[k] for k in
                      ("package_id", "surgical_face", "library",
                       "selection", "products",
                       "deterministic_double_build")},
                     ensure_ascii=False, indent=2, sort_keys=True))
    print(f"out -> {manifest['paths']['output_dir']}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
