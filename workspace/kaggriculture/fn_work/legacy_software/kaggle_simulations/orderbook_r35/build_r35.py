# -*- coding: utf-8 -*-
"""build_r35（R17 L1）：r34a 之上的白名单合并构建。

责任契约（fn_docs/hybrid/responsibility.md【R17 增补】）：
- build_r35(adopt_manifest, r34a_main_path, out_dir)：改 1（CA_MARGIN
  −15→−25 中段真值 + 2965 尾部 _HR 群饲 PICKUP/PLACE 增广块移植，
  _LEDGER/_NEW 遥测除外）+ Phase V 胜者项（sheep 6→8 / tomato 门参数 /
  V93 路由表扩条）；diff 审计恰=并入项白名单；确定性打包+manifest
  （沿 R16 配方：tarfile mtime0/uid/gid0/mode644、gzip mtime0、member
  set ['main.py']、双跑逐字节）。任一步不确定即抛（fail-closed）。
"""

from __future__ import annotations

import ast
import difflib
import hashlib
import io
import json
import os
import sys
import tarfile
import time
from typing import Any, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(KSIM)
for _p in (KSIM, HERE, os.path.join(KSIM, "orderbook_2965_adopt")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from orderbook_2965_adopt import build_adopt as _ba
except ImportError:                                    # 脚本态
    from build_adopt import build_adopt as _ba          # type: ignore

from orderbook_r35 import phase_v as _pv

R34A_MAIN = os.path.join(KSIM, "orderbook_2965_adopt", "a", "main.py")
R35_LAST_CALLABLE = "agent"          # _HR 包装后官方入口（last-callable）
SIZE_CAP_BYTES = 100 * 1024 * 1024
DESCRIPTION = ("public derivative, merged iteration "
               "(tail constants + HR + adjudicated increments)")

CA_OLD = "_CA_MARGIN = -15.0"
CA_NEW = "_CA_MARGIN = -25.0"
HR_PARENT_OLD = "_HR_PARENT = agent"
HR_PARENT_NEW = "_HR_PARENT = _cxd_agent"

# 改 2 羊 6→8 受控变更集（day-11 六羊臂区 1964-2073；逐行唯一锚）。
SHEEP_EDITS: Tuple[Tuple[str, str], ...] = (
    ("    extra=([['BUY_LAND'],['BUY_ANIMAL','SHEEP',6]] if initial else [])"
     "+[['BUY_PRODUCT','WHEAT',6],['HIRE'],['HIRE']]",
     "    extra=([['BUY_LAND'],['BUY_ANIMAL','SHEEP',8]] if initial else [])"
     "+[['BUY_PRODUCT','WHEAT',8],['HIRE'],['HIRE']]"),
    ("    incoming=6+6*initial",
     "    incoming=8+8*initial"),
    ("    budget=7000*initial+6*(int(obs['market']['prices']['WHEAT'])+10)",
     "    budget=8000*initial+8*(int(obs['market']['prices']['WHEAT'])+10)"),
    ("    if not 0<shortage<=6 or state.get('rescue_today',0)+shortage>6"
     ":return action",
     "    if not 0<shortage<=8 or state.get('rescue_today',0)+shortage>8"
     ":return action"),
    ("    if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) "
     "for x in range(5,8)):return False",
     "    if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) "
     "for x in range(5,9)):return False"),
    ("                for i in range(2):state['workers'][pending['first']+i]"
     "=[(x,5+i) for x in range(5,8)]",
     "                for i in range(2):state['workers'][pending['first']+i]"
     "=[(x,5+i) for x in range(5,9)]"),
    ("        funded='SE' in farm['unlocked_quadrants']"
     " and (not pending['initial'] or private['shed'].get('SHEEP',0)>=6)",
     "        funded='SE' in farm['unlocked_quadrants']"
     " and (not pending['initial'] or private['shed'].get('SHEEP',0)>=8)"),
)

V93_TABLE_OLD = "_V93_ROUTE_BY_RIVAL = {(229.0, 9989): 128}"


class BuildR35Error(RuntimeError):
    """构建 fail-closed。"""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _py_compile_ok(text: str, tag: str) -> None:
    import py_compile
    import tempfile
    fd, tmp = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        py_compile.compile(tmp, doraise=True)
    except py_compile.PyCompileError as exc:
        raise BuildR35Error(f"{tag} py_compile 失败：{exc}") from exc
    finally:
        os.unlink(tmp)


# ---------------------------------------------------------------------------
# 改 1：_HR 块移植（源=2965 原件尾部；_LEDGER/_NEW 遥测除外）
# ---------------------------------------------------------------------------
def extract_hr_block(src2965_path: str) -> Tuple[List[str], Dict[str, Any]]:
    """2965 尾部 `_HR_PARENT = agent` … 末行 `kaggle_submission_agent = agent`
    块抽取（字节保持）；返回（块行列表, 审计）。"""
    lines = open(src2965_path, "r", encoding="utf-8").read().split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    starts = [i for i, ln in enumerate(lines) if ln == HR_PARENT_OLD]
    if len(starts) != 1:
        raise BuildR35Error(f"_HR_PARENT 行定位数 {len(starts)}（期望 1）")
    start = starts[0]
    ends = [i for i, ln in enumerate(lines) if ln == "kaggle_submission_agent = agent"]
    after = [i for i in ends if i > start]
    if not after:
        raise BuildR35Error("_HR 块尾锚缺失")
    end = after[-1]
    block = lines[start:end + 1]
    if len(block) < 20 or "def agent" not in "\n".join(block):
        raise BuildR35Error(f"_HR 块形态异常（{len(block)} 行）")
    banned = ("_LEDGER", "_NEW_PARENT", "submission_v57", "submission_v59")
    leaked = [b for b in banned if any(b in ln for ln in block)]
    if leaked:
        raise BuildR35Error(f"_HR 块渗入遥测符号 {leaked}（授权面外）")
    audit = {"src2965_sha256": _sha256_bytes(
        open(src2965_path, "rb").read()), "src_span": [start + 1, end + 1],
        "lines": len(block), "telemetry_excluded": list(banned)}
    return block, audit


def apply_change_one(text: str, src2965_path: str) -> Tuple[str, Dict[str, Any]]:
    """改 1 无条件项：CA_MARGIN 真值（中段 4475 单点）+ _HR 尾块移植。"""
    if text.count(CA_OLD) != 1:
        raise BuildR35Error(f"CA_MARGIN 旧行定位数 {text.count(CA_OLD)}")
    text = text.replace(CA_OLD, CA_NEW)
    hr_block, hr_audit = extract_hr_block(src2965_path)
    adapted = [HR_PARENT_NEW] + hr_block[1:]
    if not text.endswith("\n"):
        raise BuildR35Error("r34a 不以换行结尾（拼接语义变化）")
    # 尾锚别名：官方 get_last_callable 按 env 插入序取末 callable——
    # 'agent' 键位在前躯（重绑不后移），故尾置新键 _r35_agent 作官方入口
    # （2965 原件无此锚，其 _HR 在 last-callable 语义下被 _HR_PARENT 影子
    # 化；我方以显式锚保增广生效，记 method_notes）。
    append = "\n\n" + "\n".join(adapted) + "\n_r35_agent = agent\n"
    text = text + append
    hr_audit["entry_anchor"] = {"key": "_r35_agent", "fn_name": "agent"}
    hr_audit["_adapted_lines"] = adapted + ["_r35_agent = agent"]
    hr_audit["adapted_first_line"] = {"old": HR_PARENT_OLD, "new": HR_PARENT_NEW}
    hr_audit["block_sha256"] = _sha256_bytes("\n".join(adapted).encode("utf-8"))
    return text, {"ca_margin": {"old": CA_OLD, "new": CA_NEW}, "hr_block": hr_audit}


def apply_sheep_eight(text: str) -> Tuple[str, Dict[str, Any]]:
    """改 2（条件并入）：day-11 六羊臂 6→8（七行受控变更集）。"""
    changes = []
    for old, new in SHEEP_EDITS:
        n = text.count(old)
        if n != 1:
            raise BuildR35Error(f"羊 6→8 锚行定位数 {n}（期望 1）：{old[:60]!r}")
        text = text.replace(old, new)
        changes.append({"old": old, "new": new})
    return text, {"sheep_6to8": changes}


def apply_tomato_params(text: str, price: int, money: int) -> Tuple[str, Dict[str, Any]]:
    """改 3（条件并入）：番茄门两参数（复用 phase_v 的两行受控替换）。"""
    new_text = _pv._tomato_variant_text(text, price, money)
    return new_text, {"tomato_gate": {"CROP_MIN_PRICE": int(price),
                                      "money_gate": int(money)}}


def apply_route_entries(text: str, entries: Dict[str, int]) -> Tuple[str, Dict[str, Any]]:
    """改 4（条件并入）：_V93_ROUTE_BY_RIVAL 只加表项（既有项逐键保留）。"""
    import ast as _ast
    old_ns = _pv._exec_namespace(text, "r35_route_old")
    old_table = dict(old_ns["_V93_ROUTE_BY_RIVAL"])
    merged = dict(old_table)
    added = {}
    for key, route in entries.items():
        rk = (tuple(key) if isinstance(key, (list, tuple))
              else _parse_rkey(str(key)))
        if rk in merged and merged[rk] != int(route):
            raise BuildR35Error(f"路由表改写既有项 {rk}（只加表项纪律）")
        if rk not in merged:
            merged[rk] = int(route)
            added[str(rk)] = int(route)
    rendered = "_V93_ROUTE_BY_RIVAL = " + repr(
        {k: v for k, v in sorted(merged.items())})
    if text.count(V93_TABLE_OLD) != 1:
        raise BuildR35Error(f"V93 表行定位数 {text.count(V93_TABLE_OLD)}")
    text = text.replace(V93_TABLE_OLD, rendered)
    ns = _pv._exec_namespace(text, "r35_route_new")
    got = dict(ns["_V93_ROUTE_BY_RIVAL"])
    if got != merged:
        raise BuildR35Error("V93 表替换后装载值与合并表不符")
    return text, {"route_table": {"kept": {str(k): v for k, v in old_table.items()},
                                   "added": added}}


def _parse_rkey(text: str) -> Tuple[float, int]:
    val = ast.literal_eval(text)
    if not (isinstance(val, tuple) and len(val) == 2):
        raise BuildR35Error(f"rkey 形态异常：{text!r}")
    return (float(val[0]), int(val[1]))


# ---------------------------------------------------------------------------
# diff 审计（r35 对 r34a 变更集恰=并入项白名单）
# ---------------------------------------------------------------------------
def _classify_r35_hunk(ours: List[str], theirs: List[str]) -> str:
    joined = "\n".join(ours + theirs)
    if any(ln.strip().startswith("_CA_MARGIN =") for ln in ours + theirs):
        return "ca_margin_true_value(-25, 2965 tail)"
    if "_HR_PARENT" in joined or "_HR_REPORT" in joined:
        return "hr_tail_append(_HR group-feeding, _LEDGER excluded)"
    if "BUY_ANIMAL','SHEEP'" in joined or "incoming=" in joined \
            or "shortage<=" in joined or "range(5,9)" in joined \
            or "SHEEP',0)>=8" in joined or "budget=8000*initial" in joined:
        return "sheep_6to8(day-11 arm)"
    if "CROP_MIN_PRICE=" in joined or "farm['money'] <" in joined:
        return "tomato_gate_params(scan winner)"
    if "_V93_ROUTE_BY_RIVAL" in joined:
        return "route_table_entries(expansion)"
    nonblank = [ln for ln in ours + theirs if ln.strip()]
    if all(ln.lstrip().startswith("#") for ln in nonblank) or not nonblank:
        return "blank_cosmetic"
    return "UNATTRIBUTED"


def audit_diff_vs_r34a(r34a_path: str, r35_path: str,
                       expected_hr_append: Optional[List[str]] = None) -> Dict[str, Any]:
    """r35 对 r34a 逐行 diff 归因；白名单外差异=红。

    expected_hr_append 给定时（构建面），hr_tail_append 类的 hunk 其插入
    非空行必须与期望追加块逐行相等（防杂散行混入尾块 hunk 逃逸归因）。
    """
    ours = open(r34a_path, encoding="utf-8").read().split("\n")
    theirs = open(r35_path, encoding="utf-8").read().split("\n")
    sm = difflib.SequenceMatcher(None, ours, theirs, autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        klass = _classify_r35_hunk(ours[i1:i2], theirs[j1:j2])
        if (klass.startswith("hr_tail_append")
                and expected_hr_append is not None):
            inserted = [ln for ln in theirs[j1:j2] if ln.strip()]
            if inserted != [ln for ln in expected_hr_append if ln.strip()]:
                klass = "UNATTRIBUTED"
        hunks.append({"tag": tag, "class": klass,
                      "r34a_span": [i1 + 1, i2], "r35_span": [j1 + 1, j2],
                      "r34a_lines": i2 - i1, "r35_lines": j2 - j1,
                      "sample_r34a": ours[i1][:90] if i2 > i1 else None,
                      "sample_r35": theirs[j1][:90] if j2 > j1 else None})
    attribution: Dict[str, int] = {}
    for h in hunks:
        attribution[h["class"]] = attribution.get(h["class"], 0) + 1
    unattributed = [h for h in hunks if h["class"] == "UNATTRIBUTED"]
    return {"ok": not unattributed, "n_hunks": len(hunks),
            "attribution": attribution, "unattributed": unattributed,
            "hunks": hunks}


# ---------------------------------------------------------------------------
# 确定性打包（R16 配方复用）
# ---------------------------------------------------------------------------
def build_tar_bytes(main_bytes: bytes) -> bytes:
    return _ba.build_tar_bytes(main_bytes)


def _package(out_dir: str, main_path: str, extra: Dict[str, Any]) -> Dict[str, Any]:
    main_bytes = open(main_path, "rb").read()
    tar1, tar2 = build_tar_bytes(main_bytes), build_tar_bytes(main_bytes)
    if tar1 != tar2:
        raise BuildR35Error("tar 双跑不一致（非可复现）")
    os.makedirs(out_dir, exist_ok=True)
    tar_path = os.path.join(out_dir, "submission.tar.gz")
    with open(tar_path, "wb") as fh:
        fh.write(tar1)
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as tar:
        names = tar.getnames()
        inner = tar.extractfile("main.py").read() if "main.py" in names else None
    if names != ["main.py"] or inner != main_bytes:
        raise BuildR35Error(f"tar 成员/内层 main 校验失败：{names}")
    manifest = {
        "schema": "orderbook_r35_manifest/1.0",
        "generated": time.strftime("%Y-%m-%d"),
        "variant": "r35",
        "description": DESCRIPTION,
        "main_sha256": _sha256_bytes(main_bytes),
        "main_bytes": len(main_bytes),
        "tar_sha256": _sha256_bytes(tar1),
        "tar_bytes": len(tar1),
        "tar_members": names,
        "tar_rebuild_reproducible": True,
        "tar_size_ok": len(tar1) <= SIZE_CAP_BYTES,
    }
    manifest.update(extra)
    with open(os.path.join(out_dir, "build_manifest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return manifest


# ---------------------------------------------------------------------------
# build_r35（编排）
# ---------------------------------------------------------------------------
def build_r35(adopt_manifest: Dict[str, Any],
              r34a_main_path: str = R34A_MAIN,
              out_dir: Optional[str] = None) -> Dict[str, Any]:
    """白名单合并构建。

    adopt_manifest 形如 phase_v_adjudicate 的输出（sheep/tomato/route 各含
    adopt+params）。并入面：改 1 恒并；三项条件项 adopt=True 才并。
    """
    t0 = time.perf_counter()
    out_dir = out_dir or HERE
    src2965 = _ba.fetch_2965_source()
    with open(r34a_main_path, "r", encoding="utf-8") as fh:
        r34a_text = fh.read()
    r34a_sha = _sha256_bytes(r34a_text.encode("utf-8"))

    adopted = {"ca_margin": True, "hr_tail": True}
    text, audit1 = apply_change_one(r34a_text, src2965["path"])
    expected_hr_append = ["", ""] + audit1["hr_block"]["_adapted_lines"] \
        if "_adapted_lines" in audit1["hr_block"] else None
    audit = {"change_1": audit1}

    sheep = (adopt_manifest or {}).get("sheep") or {}
    if sheep.get("adopt") and sheep.get("params"):
        text, ch = apply_sheep_eight(text)
        audit["change_2_sheep"] = ch
        adopted["sheep_6to8"] = True
    tomato = (adopt_manifest or {}).get("tomato") or {}
    if tomato.get("adopt") and tomato.get("params"):
        p = tomato["params"]
        text, ch = apply_tomato_params(text, p["CROP_MIN_PRICE"], p["money_gate"])
        audit["change_3_tomato"] = ch
        adopted["tomato_gate"] = True
    route = (adopt_manifest or {}).get("route") or {}
    if route.get("adopt") and route.get("params"):
        entries = route["params"]["_V93_ROUTE_BY_RIVAL"]
        parsed = {_parse_rkey(k): int(v) for k, v in entries.items()}
        text, ch = apply_route_entries(text, parsed)
        audit["change_4_route"] = ch
        adopted["route_table"] = True

    # —— 校验链（fail-closed）——
    _py_compile_ok(text, "r35")
    ast.parse(text)
    ns = _pv._exec_namespace(text, "r35_build_check")
    last_key = [k for k, v in ns.items() if callable(v)][-1]
    last = ns[last_key]
    if last_key != "_r35_agent" or getattr(last, "__name__", None) != R35_LAST_CALLABLE:
        raise BuildR35Error(
            f"r35 末 callable key={last_key!r} name={getattr(last, '__name__', None)!r}"
            f"（期望 key='_r35_agent'/name={R35_LAST_CALLABLE!r}）")
    for sym in ("_HR_PARENT", "_HR_REPORT", "_cxd_agent", "e402_agent",
                "_ig_standard"):
        if sym not in ns:
            raise BuildR35Error(f"r35 符号缺失：{sym}")
    for banned in ("_NEW_PARENT", "_LEDGER_PARENT", "submission_v57", "_cxs_agent"):
        if banned in ns:
            raise BuildR35Error(f"r35 渗入授权面外符号：{banned}")
    consts = _ba._constant_values(text)
    expect = {"_V92_P_EVERY": 2, "_CA_MARGIN": -25.0, "_OR2_SLOT_MARGIN": 8.0,
              "V9_RACE_DEFAULT": [40, 44]}
    for key, want in expect.items():
        if consts.get(key) != want:
            raise BuildR35Error(f"r35 常数 {key}={consts.get(key)!r}（期望 {want!r}）")

    os.makedirs(os.path.join(out_dir, "evidence"), exist_ok=True)
    main_path = os.path.join(out_dir, "main.py")
    with open(main_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    if open(main_path, "rb").read() != text.encode("utf-8"):
        raise BuildR35Error("r35 回读不一致")

    diff_audit = audit_diff_vs_r34a(r34a_main_path, main_path,
                                     expected_hr_append=expected_hr_append)
    expected_classes = {"ca_margin_true_value(-25, 2965 tail)",
                        "hr_tail_append(_HR group-feeding, _LEDGER excluded)",
                        "blank_cosmetic"}
    if adopted.get("sheep_6to8"):
        expected_classes.add("sheep_6to8(day-11 arm)")
    if adopted.get("tomato_gate"):
        expected_classes.add("tomato_gate_params(scan winner)")
    if adopted.get("route_table"):
        expected_classes.add("route_table_entries(expansion)")
    stray = set(diff_audit["attribution"]) - expected_classes
    if not diff_audit["ok"] or stray:
        raise BuildR35Error(
            f"diff 审计白名单外差异（fail-closed）：stray={sorted(stray)}，"
            f"unattributed={len(diff_audit['unattributed'])}")
    audit_path = os.path.join(out_dir, "evidence", "diff_audit_r35_vs_r34a.json")
    with open(audit_path, "w", encoding="utf-8") as fh:
        json.dump(diff_audit, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    manifest = _package(out_dir, main_path, {
        "mode": "r34a + merged iteration (whitelist)",
        "adopted": adopted,
        "adopt_manifest": adopt_manifest,
        "provenance": {
            "base_r34a_main": r34a_sha,
            "base_r34a_pkg": "orderbook_2965_adopt/a（在飞件 ref 56526029 同字节）",
            "source_2965": {"kernel_slug": _ba.KERNEL_SLUG,
                            "sha256": src2965["sha256"],
                            "fetched_via": src2965["source"],
                            "license": "Apache-2.0（embedded notices）"},
            "change_audit": audit,
        },
        "diff_audit": {"path": audit_path,
                       "attribution": diff_audit["attribution"],
                       "ok": diff_audit["ok"]},
    })
    summary = {
        "ok": True,
        "adopted": adopted,
        "main_sha256": manifest["main_sha256"],
        "main_bytes": manifest["main_bytes"],
        "tar_sha256": manifest["tar_sha256"],
        "tar_bytes": manifest["tar_bytes"],
        "last_callable": R35_LAST_CALLABLE,
        "out_dir": os.path.abspath(out_dir),
        "diff_attribution": diff_audit["attribution"],
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return summary
