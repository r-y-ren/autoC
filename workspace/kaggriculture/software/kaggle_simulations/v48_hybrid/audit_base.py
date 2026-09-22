# -*- coding: utf-8 -*-
# 【中文】audit_base.py —— load_v48_base 审计（R1：基底完整性五区零改动证明）
# ===========================================================================
# 职责（responsibility.md：load_v48_base [L0|新增]）：
#   1) 装载基底字节 + sha256 校验（dadee25a…2664a；不符即抛，非零退出）；
#   2) 对混合 main.py 做分区 diff 审计：
#      a) 前缀逐字证明：hybrid 以基底字节为逐字前缀 ⇒ 基底一切行区域
#         （含五零改动区）字节一致；
#      b) 行级 diff 归因：difflib 操作码只允许 equal/insert 且 insert 全部
#         位于基底末行之后 ⇒ 零条基底行被修改/删除；
#      c) 五零改动区逐区证明（区界清单 + 语义载体逐字节比对）：
#         磁带=_V48_ROUTES 字面区+解码路由表；路由=v48.fast_route_router
#         模块源+_V48_CONFIG 行；反克隆抢卖=v44.gold_floor 模块源+
#         _V48_GOLD_CONFIG 行；槽位重排=scripts.v22_market_impact+
#         v23.policy_library 模块源；终局清仓=v19_terminal+
#         scripts.v19_terminal 模块源——模块源从基底与混合件各自解出
#         _V48_MODULES blob 后逐字节比对相等；
#      d) 改动仅落在三注入点：追加块内 `_V48_POLICY(` 仅出现于重定义
#         agent 内 1 次；P2/P1/P3 三条接线语句各恰好 1 次；
#      e) 基底 except 兜底逐字：重定义 agent 的 except 块与基底 agent 的
#         except 块文本逐字相等；
#      f) 内联补丁源完整性：追加块 _V48H_MODULES blob 解出的三补丁源与
#         patches/*.py 字节一致（源 sha 登记）；
#      g) 旗面/入口：P1_ON/P2_ON/P3_ON 常量解析；追加块最后顶层 def 为
#         _v48hybrid_entrypoint（官方 get_last_callable 取最后 callable）。
#   纯文本/解码级审计（不 exec 被审件）。输出：JSON 判定打印到 stdout；
#   audit_pass=false 或任何校验失败 ⇒ 退出码 1。
# CLI：python audit_base.py [--hybrid PATH] [--base PATH]
# ===========================================================================
from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import os
import re
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)

BASE_MAIN_DEFAULT = os.path.join(KSIM, "v48_derivative", "main.py")
HYBRID_MAIN_DEFAULT = os.path.join(HERE, "main.py")

BASE_SHA256 = ("dadee25a9840313218384208c53b2c4752f82c3209"
               "cc654632e0b96c65e2664a")
BASE_BYTES_EXPECT = 107008

# 五零改动区 → 语义载体（模块键 = _V48_MODULES 解码后的源码键）
ZONES = [
    ("tape", "磁带（719 步预录整季动作序列）",
     ["__routes__"], "route_blob"),
    ("routing", "路由（v48.fast_route_router + _V48_CONFIG）",
     ["v48.fast_route_router"], "config_line:_V48_CONFIG"),
    ("anti_clone", "反克隆抢卖（v44.gold_floor + _V48_GOLD_CONFIG）",
     ["v44.gold_floor"], "config_line:_V48_GOLD_CONFIG"),
    ("slot_reorder", "卖单槽位重排（scripts.v22_market_impact + "
     "v23.policy_library）",
     ["scripts.v22_market_impact", "v23.policy_library"], None),
    ("terminal", "终局清仓（v19_terminal 两步机）",
     ["v19_terminal", "scripts.v19_terminal"], None),
]

EXPECTED_PATCH_MODULES = ("v48h.p1_midgame_sell_layer",
                          "v48h.p2_economic_guard",
                          "v48h.p3_milestone_monitor")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# load_v48_base：装载 + sha 校验
# ---------------------------------------------------------------------------
def load_v48_base(path: str) -> dict:
    data = open(path, "rb").read()
    sha = sha256_bytes(data)
    if sha != BASE_SHA256 or len(data) != BASE_BYTES_EXPECT:
        raise SystemExit(f"base sha/size mismatch: {sha} ({len(data)}B)，"
                         f"期望 {BASE_SHA256[:16]}… ({BASE_BYTES_EXPECT}B)")
    return {"main_source": data, "sha256": sha, "bytes": len(data)}


# ---------------------------------------------------------------------------
# 文本工具：b85 blob 提取（不 exec）
# ---------------------------------------------------------------------------
def extract_b85_blob(source: str, marker: str) -> bytes:
    lines = source.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(marker):
            start = i
            break
    if start is None:
        raise SystemExit(f"marker not found: {marker}")
    frags = []
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if s == ")":
            return base64.b85decode("".join(frags).encode("ascii"))
        if s == "(":
            continue
        for m in re.finditer(r"'([^']*)'", lines[j]):
            frags.append(m.group(1))
    raise SystemExit(f"blob terminator not found after marker: {marker}")


def decode_modules(source: str, var: str, marker: str) -> dict:
    raw = extract_b85_blob(source, marker)
    return json.loads(zlib.decompress(raw).decode("utf-8"))


def literal_span(source: str, marker: str) -> tuple[int, int]:
    """marker 赋值语句的行界（1-based，闭区间）——区界清单用。"""
    lines = source.split("\n")
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith(marker)) + 1
    for j in range(start, len(lines)):
        if lines[j].rstrip() == ")).decode(\"utf-8\"))":
            return (start, j + 1)
    raise SystemExit(f"literal end not found for {marker}")


def find_line(source: str, prefix: str) -> int:
    for i, ln in enumerate(source.split("\n")):
        if ln.startswith(prefix):
            return i + 1
    raise SystemExit(f"line not found: {prefix}")


def extract_agent_except(source: str, last: bool) -> str:
    """agent() 的 except 兜底块（逐字）。last=True 取最后一个 def agent。"""
    lines = source.split("\n")
    starts = [i for i, ln in enumerate(lines)
              if ln.startswith("def agent(obs, configuration=None):")]
    if not starts:
        raise SystemExit("agent() not found")
    start = starts[-1] if last else starts[0]
    except_at = None
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("    except Exception:"):
            except_at = j
            break
        if lines[j] and lines[j][0] not in (" ", "\t"):
            break
    if except_at is None:
        raise SystemExit("agent() except block not found")
    block = []
    for j in range(except_at, len(lines)):
        ln = lines[j]
        if j > except_at and ln and ln[0] not in (" ", "\t"):
            break
        block.append(ln)
    while block and not block[-1]:
        block.pop()
    return "\n".join(block)


# ---------------------------------------------------------------------------
# 分区 diff 审计主入口
# ---------------------------------------------------------------------------
def audit(base_path: str, hybrid_path: str) -> dict:
    base_info = load_v48_base(base_path)
    base = base_info["main_source"]
    hybrid = open(hybrid_path, "rb").read()
    base_text = base.decode("utf-8")
    hybrid_text = hybrid.decode("utf-8")

    # a) 前缀逐字
    prefix_ok = hybrid.startswith(base)

    # b) 行级 diff 归因（只允许 equal/insert，insert 全在基底行数之后）
    base_lines = base_text.split("\n")
    hybrid_lines = hybrid_text.split("\n")
    sm = difflib.SequenceMatcher(None, base_lines, hybrid_lines,
                                 autojunk=False)
    ops = sm.get_opcodes()
    bad_ops = [op for op in ops if op[0] not in ("equal", "insert")]
    insert_ops = [op for op in ops if op[0] == "insert"]
    inserts_after_base = all(op[1] >= len(base_lines) - 1
                             for op in insert_ops)
    modified_base_lines = 0
    for tag, i1, i2, _, _ in ops:
        if tag in ("replace", "delete"):
            modified_base_lines += i2 - i1
    diff_ok = (not bad_ops) and inserts_after_base and prefix_ok

    # c) 五零改动区逐区证明
    base_modules = decode_modules(
        base_text, "_V48_MODULES = ",
        "_V48_MODULES = json.loads(zlib.decompress(base64.b85decode(")
    hybrid_modules = decode_modules(
        hybrid_text, "_V48_MODULES = ",
        "_V48_MODULES = json.loads(zlib.decompress(base64.b85decode(")
    base_routes_raw = extract_b85_blob(
        base_text, "_V48_ROUTES = json.loads(zlib.decompress(base64.b85decode(")
    hybrid_routes_raw = extract_b85_blob(
        hybrid_text, "_V48_ROUTES = json.loads(zlib.decompress(base64.b85decode(")
    routes_span = literal_span(
        base_text, "_V48_ROUTES = json.loads(zlib.decompress(base64.b85decode(")
    modules_span = literal_span(
        base_text, "_V48_MODULES = json.loads(zlib.decompress(base64.b85decode(")

    zone_reports = []
    for key, desc, module_keys, extra in ZONES:
        rep = {"zone": key, "desc": desc, "carriers": [], "identical": True}
        if key == "tape":
            rep["carriers"].append({
                "kind": "decoded_route_payload",
                "base_span": list(routes_span),
                "identical": base_routes_raw == hybrid_routes_raw,
            })
        for mk in module_keys:
            if mk == "__routes__":
                continue
            rep["carriers"].append({
                "kind": "bundled_module_source",
                "module": mk,
                "blob_span": list(modules_span),
                "identical": (base_modules.get(mk)
                              == hybrid_modules.get(mk)),
            })
        if extra and extra.startswith("config_line:"):
            var = extra.split(":", 1)[1]
            ln = find_line(base_text, f"{var} = ")
            rep["carriers"].append({
                "kind": "config_line",
                "var": var,
                "base_line": ln,
                "identical": (ln <= len(base_lines)
                              and hybrid_lines[ln - 1] == base_lines[ln - 1]),
            })
        rep["identical"] = all(c["identical"] for c in rep["carriers"]) \
            and diff_ok
        zone_reports.append(rep)

    # 追加块
    appended = hybrid_text[len(base_text):]

    # d) 改动仅落在三注入点
    injection = {
        "policy_call_sites_in_appended":
            len(re.findall(r"_V48_POLICY\(obs, configuration\)", appended)),
        "P2_seam": len(re.findall(
            r"_policy_out = _v48h_p2_vetoe\(\[_policy_out\], obs\)\[0\]",
            appended)),
        "P1_seam": len(re.findall(
            r"_policy_out\[\"market\"\] = _v48h_p1_apply\(", appended)),
        "P3_seam": len(re.findall(
            r"_policy_out = _v48h_p3_sell_timing\(obs, _policy_out\)",
            appended)),
    }
    injection_ok = (injection["policy_call_sites_in_appended"] == 1
                    and injection["P2_seam"] == 1
                    and injection["P1_seam"] == 1
                    and injection["P3_seam"] == 1)

    # e) 基底 except 兜底逐字
    except_ok = (extract_agent_except(base_text, last=False)
                 == extract_agent_except(hybrid_text, last=True))

    # f) 内联补丁源完整性
    hybrid_patch_modules = decode_modules(
        hybrid_text, "_V48H_MODULES = ",
        "_V48H_MODULES = json.loads(zlib.decompress(base64.b85decode(")
    patch_report = {}
    for module, rel in zip(EXPECTED_PATCH_MODULES,
                           ("P1", "P2", "P3")):
        src_path = os.path.join(HERE, "patches",
                                {"P1": "midgame_sell_layer.py",
                                 "P2": "economic_guard.py",
                                 "P3": "milestone_monitor.py"}[rel])
        src = open(src_path, "rb").read()
        embedded = hybrid_patch_modules.get(module)
        patch_report[rel] = {
            "module": module,
            "source": f"patches/{os.path.basename(src_path)}",
            "sha256": sha256_bytes(src),
            "verbatim_inline_ok": embedded == src.decode("utf-8"),
        }
    patches_ok = all(v["verbatim_inline_ok"] for v in patch_report.values())

    # g) 旗面 + 最后入口
    flags = {f"P{i}_ON": None for i in (1, 2, 3)}
    for i in (1, 2, 3):
        m = re.search(rf"^_V48H_P{i}_ON = (True|False)$", hybrid_text,
                      re.M)
        flags[f"P{i}_ON"] = (m.group(1) == "True") if m else None
    top_defs = re.findall(r"^def (\w+)", appended, re.M)
    entrypoint_ok = bool(top_defs) and top_defs[-1] == "_v48hybrid_entrypoint"

    audit_pass = bool(diff_ok and prefix_ok
                      and all(z["identical"] for z in zone_reports)
                      and injection_ok and except_ok and patches_ok
                      and all(v is not None for v in flags.values())
                      and entrypoint_ok)

    return {
        "protocol": "v48-hybrid-load-base-audit/1.0",
        "base": {"path": os.path.relpath(base_path, KSIM),
                 "sha256": base_info["sha256"],
                 "bytes": base_info["bytes"],
                 "sha_verified": True},
        "hybrid": {"path": os.path.relpath(hybrid_path, KSIM),
                   "sha256": sha256_bytes(hybrid),
                   "bytes": len(hybrid)},
        "prefix_verbatim_ok": prefix_ok,
        "diff_attribution": {
            "opcodes_summary": {op[0]: True for op in ops},
            "bad_ops": [list(op) for op in bad_ops],
            "inserts_after_base_lines": inserts_after_base,
            "modified_base_lines": modified_base_lines,
            "inserted_lines_total": sum(op[4] - op[3]
                                        for op in insert_ops),
        },
        "zero_change_zones": zone_reports,
        "injection_points": {**injection, "only_injection_points_ok":
                             injection_ok},
        "base_except_verbatim_ok": except_ok,
        "patch_sources_inline": patch_report,
        "flags": flags,
        "last_top_level_def_in_append_block": (top_defs[-1]
                                               if top_defs else None),
        "entrypoint_last_ok": entrypoint_ok,
        "audit_pass": audit_pass,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="v48_hybrid load_v48_base "
                                             "partitioned diff audit")
    ap.add_argument("--hybrid", default=HYBRID_MAIN_DEFAULT)
    ap.add_argument("--base", default=BASE_MAIN_DEFAULT)
    args = ap.parse_args()
    report = audit(args.base, args.hybrid)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    print(f"audit_pass = {report['audit_pass']}")
    return 0 if report["audit_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
