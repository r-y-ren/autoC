# -*- coding: utf-8 -*-
"""build_2965_adopt（R16 L0）：2965 三增量采纳双件构建编排（r34a/r34b）。

责任契约（fn_docs/hybrid/responsibility.md【R16 增补】）：
- build_2965_adopt()：CLI 编排——fetch_2965_source 取公开件源（gzip 载荷解码，
  sha 钉死 fail-closed）→ merge_increments 三增量受控移植到 L3 基座副本+
  移除 layer S 尾块（EXP402 替代，用户裁决）产 r34a → apply_2965_constants
  产 r34b（恰三处：P_EVERY 2→3 / CA_MARGIN −15→−5 / OR2_SLOT 8→20；RACE
  不变）→ audit_diff_vs_2965 双件对原件逐字节差异归因 → 确定性打包双产物+
  manifest（sha 链沿 r30/v48 配方：tarfile mtime0 uid/gid0 mode644、gzip
  mtime0、member set ['main.py']、双跑逐字节）。任一步不确定即抛（fail-closed）。
- 产物：orderbook_2965_adopt/{a,b}/{main.py,submission.tar.gz,
  build_manifest.json}；基座/在飞件/2965 原件零改动。

三增量（haideptry/the-2965-master-hybrid-engine，09-24，Apache-2.0）：
- EXP402：step≥624 剩余可种植上限截 BUY_SEED（含 pending 队列）——替代我方
  layer S 尾块（r34 链由 _cxd_agent 直出，_cxs_* 全数不在场）；
- EXP410：FERTILIZE 增益预检（双算产量无增益 PASS）；
- _IG：开场修复（step29 wheat 缺位回 BUILD_PASTURE）+市场队列清穴（不可执行
  现金卖单归零挪位）。
2965 尾部其余块（_LEDGER/_NEW 遥测包装、尾部常数重指 2/44/8/−25、_HR 群饲
PICKUP 增广）**不在三增量授权面内，不采纳**——审计归因类
2965_tail_not_adopted（雷达决策面未及尾部覆盖块与 _HR 第四增量，本轮解码
新发现，记 method_notes）。
"""

from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
from typing import Any, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                              # kaggle_simulations/
SOFTWARE = os.path.dirname(KSIM)                          # legacy_software/
CAMPAIGN = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(SOFTWARE))))                          # 战役根（相对推导）
L3_DIR = os.path.join(KSIM, "orderbook_l3_derivative")
L1_DIR = os.path.join(KSIM, "orderbook_l1_derivative")
L3_MAIN = os.path.join(L3_DIR, "main.py")                 # fine 钳制+layer S（本包拆解）
LAYER_S_BLOCK = os.path.join(L1_DIR, "layer_s_block.py")

KERNEL_SLUG = "haideptry/the-2965-master-hybrid-engine"
# sha 钉死（双源核实：雷达解码注记 + 本轮独立解码；notebook cell2 自称同值）。
# 上游漂移即抛（fail-closed：任一步不确定即抛，不静默换源）。
EXPECTED_SHA256_2965 = ("bc8f84641d8e5ae8e083089c79572ed873b0f32dd"
                        "071572f5efdcf342ec1143f")
FETCH_DIR = "/tmp/2965src"                # kaggle kernels pull 落点
DECODE_DIR = "/tmp/2965decoded"           # gzip 载荷解码产物缓存
KAGGLE_BIN = os.path.expanduser("~/.local/bin/kaggle")

# r34b 常数面（恰三处；AST 前的行级定位断言单点）：
CONSTANT_SPECS: Tuple[Tuple[str, str, str], ...] = (
    ("_V92_P_EVERY", "2", "3"),
    ("_CA_MARGIN", "-15.0", "-5.0"),
    ("_OR2_SLOT_MARGIN", "8.0", "20.0"),
)
# r34a 保留我方 layer-D 常数（RACE 两处 40/44 均不动——2965 中段 41 亦不采纳）。

SIZE_CAP_BYTES = 100 * 1024 * 1024
R34_LAST_CALLABLE = "_cxd_agent"

DESCRIPTIONS = {
    "a": "public derivative, adopted increments (EXP402/402/IG)",
    "b": "public derivative, adopted increments (EXP402/402/IG) + constants",
}


class BuildAdoptError(RuntimeError):
    """构建 fail-closed：fetch/移植/常数/审计任一步不确定即抛。"""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return _sha256_bytes(fh.read())


def _line_index(lines: List[str], needle: str, what: str,
                after: Optional[int] = None,
                first: bool = False) -> int:
    """单点行定位（fail-closed：非恰一即抛；after 限定其后；first=True 取
    首个命中——IG 块尾锚 'kaggle_submission_agent = agent' 在 2965 尾部块
    （_NEW/_HR 后）同名重指，须取 bridge 后首个）。"""
    hits = [i for i, ln in enumerate(lines)
            if ln == needle and (after is None or i > after)]
    if not hits or (len(hits) != 1 and not first):
        raise BuildAdoptError(f"{what} 锚行定位数 {len(hits)}（期望 1）：{needle!r}")
    return hits[0]


def _line_startswith_index(lines: List[str], prefix: str, what: str,
                           after: Optional[int] = None) -> int:
    hits = [i for i, ln in enumerate(lines)
            if ln.startswith(prefix) and (after is None or i > after)]
    if len(hits) != 1:
        raise BuildAdoptError(f"{what} 锚前缀定位数 {len(hits)}（期望 1）：{prefix!r}")
    return hits[0]


# ---------------------------------------------------------------------------
# fetch_2965_source
# ---------------------------------------------------------------------------
def _decode_notebook(nb_path: str, out_path: str) -> str:
    """ipynb → main.py：cell 内 AGENT_B64 三引号载荷 b64+gzip 解码+CRLF 归一。"""
    with open(nb_path, "r", encoding="utf-8") as fh:
        nb = json.load(fh)
    blob = None
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source") or [])
        m = re.search(r'AGENT_B64\s*=\s*"""(.*?)"""', src, re.S)
        if m:
            blob = m.group(1).strip()
            break
    if blob is None:
        raise BuildAdoptError(f"notebook 无 AGENT_B64 载荷：{nb_path}")
    try:
        raw = gzip.decompress(base64.b64decode(blob))
    except Exception as exc:
        raise BuildAdoptError(f"b64+gzip 解码失败：{type(exc).__name__}: {exc}") from exc
    normalized = raw.replace(b"\r\n", b"\n")   # 与 2965 cell5 校验语义一致
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(normalized)
    return _sha256_bytes(normalized)


def fetch_2965_source(kernel_slug: str = KERNEL_SLUG) -> Dict[str, Any]:
    """拉取/解码 2965 公开件源+sha 登记；失败重试一次（再失败即抛）。

    优先用既有解码缓存（sha 复核）；缺缓存则 kaggle kernels pull（token 经
    `kaggle auth print-access-token` 注入环境）→ 解码。返回
    {path, sha256, source: cache|pull, notebook_path?}。sha 与
    EXPECTED_SHA256_2965 不符即抛（fail-closed）。
    """
    out_path = os.path.join(DECODE_DIR, "main2965.py")
    last_error: Optional[str] = None
    for attempt in (1, 2):
        try:
            if os.path.isfile(out_path):
                sha = _sha256_file(out_path)
                if sha == EXPECTED_SHA256_2965:
                    return {"path": out_path, "sha256": sha, "source": "cache"}
            env = dict(os.environ)
            token = subprocess.run(
                [KAGGLE_BIN, "auth", "print-access-token"],
                capture_output=True, text=True, timeout=60)
            if token.returncode == 0 and token.stdout.strip():
                env["KAGGLE_API_TOKEN"] = token.stdout.strip()
            shutil.rmtree(FETCH_DIR, ignore_errors=True)
            os.makedirs(FETCH_DIR, exist_ok=True)
            pull = subprocess.run(
                [KAGGLE_BIN, "kernels", "pull", kernel_slug, "-p", FETCH_DIR],
                capture_output=True, text=True, timeout=180, env=env)
            if pull.returncode != 0:
                raise BuildAdoptError(f"kernels pull 退出 {pull.returncode}: "
                                      f"{pull.stderr.strip()[:300]}")
            nb_files = [f for f in os.listdir(FETCH_DIR) if f.endswith(".ipynb")]
            if len(nb_files) != 1:
                raise BuildAdoptError(f"pull 落点 ipynb 数 {len(nb_files)}（期望 1）")
            nb_path = os.path.join(FETCH_DIR, nb_files[0])
            sha = _decode_notebook(nb_path, out_path)
            if sha != EXPECTED_SHA256_2965:
                raise BuildAdoptError(
                    f"2965 源 sha 漂移：{sha} != 钉死值 {EXPECTED_SHA256_2965}")
            return {"path": out_path, "sha256": sha, "source": "pull",
                    "notebook_path": nb_path}
        except (BuildAdoptError, OSError, subprocess.SubprocessError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt == 1:
                time.sleep(2)
                continue
    raise BuildAdoptError(f"fetch_2965_source 两次失败（fail-closed）：{last_error}")


# ---------------------------------------------------------------------------
# merge_increments
# ---------------------------------------------------------------------------
def _strip_layer_s(l3_main_path: str) -> Tuple[bytes, Dict[str, Any]]:
    """L3 main.py → 钳制前躯（去 layer S 尾块）：逐字节分解证明。

    L3 main.py = main_clamped 前躯 + 两空行 + layer_s_block 全文（r13 build
    配方）。分解即移除 layer S（EXP402 替代，用户裁决）；任何一字节对不上
    即抛（不猜边界）。
    """
    base = open(l3_main_path, "rb").read()
    block = open(LAYER_S_BLOCK, "rb").read()
    sep = b"\n\n"
    idx = base.find(sep + block)
    if idx < 0 or base[idx + len(sep) + len(block):] != b"":
        raise BuildAdoptError(
            "L3 main.py 非 [钳制前躯+两空行+layer S 块] 逐字节构成（尾部有残留）")
    clamped = base[:idx]
    audit = {
        "l3_main_sha256": _sha256_bytes(base),
        "layer_s_block_sha256": _sha256_bytes(block),
        "clamped_prefix_sha256": _sha256_bytes(clamped),
        "layer_s_removed_bytes": len(base) - len(clamped) - len(sep),
    }
    if b"_cxs_" in clamped:
        raise BuildAdoptError("钳制前躯意外含 _cxs_ 符号（layer S 渗入前躯）")
    return clamped, audit


def _exec_last_callable(text: str, tag: str) -> Tuple[str, Dict[str, Any]]:
    """官方 last-callable 语义装载（sys.path.append→exec→pop）；返回 (名字, ns)。"""
    env: Dict[str, Any] = {"__name__": "build_adopt_probe", "__file__": tag}
    exec_dir = HERE
    sys.path.append(exec_dir)
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        exec(compile(text, tag, "exec"), env)
    finally:
        sys.path.pop()
        sys.dont_write_bytecode = old
    entries = [(k, v) for k, v in env.items()
               if callable(v) and not (k.startswith("__") and k.endswith("__"))]
    if not entries:
        raise BuildAdoptError(f"{tag} 装载后无 callable")
    return entries[-1][0], env


def _py_compile_ok(text: str, tag: str) -> None:
    import py_compile
    import tempfile
    fd, tmp = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        py_compile.compile(tmp, doraise=True)
    except py_compile.PyCompileError as exc:
        raise BuildAdoptError(f"{tag} py_compile 失败：{exc}") from exc
    finally:
        os.unlink(tmp)


def _extract_increment_blocks(src_lines: List[str]) -> Dict[str, List[str]]:
    """2965 源三增量块抽取（锚行定位，字节保持原序原空白）。"""
    i402 = _line_startswith_index(src_lines, "# EXP402: cap late seed purchases",
                                  "EXP402 块首")
    i402_end = _line_index(src_lines, "kaggle_submission_agent=e402_agent",
                           "EXP402 块尾")
    i410 = _line_startswith_index(src_lines, "# EXP410: do not consume",
                                  "EXP410 块首")
    i_bridge = _line_startswith_index(src_lines,
                                      "# Bridge: set agent to outermost",
                                      "IG bridge 行")
    ig_end = _line_index(src_lines, "kaggle_submission_agent = agent", "IG 块尾",
                         after=i_bridge, first=True)
    if not (i402 < i402_end < i410 < i_bridge < ig_end):
        raise BuildAdoptError(f"三增量锚序异常：{i402}/{i402_end}/{i410}/"
                              f"{i_bridge}/{ig_end}")
    blocks = {
        "e402": src_lines[i402:i402_end + 1],
        "e410_ig": src_lines[i410:ig_end + 1],   # EXP410+bridge+IG（内含原空行）
    }
    for name, blk in blocks.items():
        if not blk or any(ln.strip() == "" for ln in blk[:1]):
            raise BuildAdoptError(f"{name} 块抽取为空/畸形")
    return blocks


def merge_increments(l3_main_path: str, src2965_path: str,
                     out_path: str) -> Dict[str, Any]:
    """三增量受控移植+移除 layer S 尾块 → r34a main+变更集审计。

    拼接语义：我方 round-2 常数注释行（单点锚）替换为 2965 [EXP402 块 + 空
    行 + EXP410/bridge/IG 块]（与 2965 文件内该位置的排布逐字一致）；前缀/
    后缀对我方钳制前躯逐字节恒等；尾部 _cxs_* 全数不在场（layer S 移除）；
    末 callable=_cxd_agent（CXTB/CXD 包裹链自适应，链序=base→PG→E402→E410
    →IG→CXTB→CXD）。变更超白名单即抛。
    """
    clamped, comp = _strip_layer_s(l3_main_path)
    text = clamped.decode("utf-8")
    base_lines = text.split("\n")
    if base_lines and base_lines[-1] != "":
        raise BuildAdoptError("钳制前躯不以换行结尾（拆解语义变化）")
    base_lines = base_lines[:-1]

    src_lines = open(src2965_path, "r", encoding="utf-8").read().split("\n")
    if src_lines and src_lines[-1] == "":
        src_lines = src_lines[:-1]
    blocks = _extract_increment_blocks(src_lines)

    round2 = ("# ==== round 2: _V92_P_EVERY=2, _CA_MARGIN=-15.0, "
              "V9_RACE_DEFAULT=44, _OR2_SLOT_MARGIN=8.0 ====")
    i_round2 = _line_index(base_lines, round2, "round-2 注释行（拼接点）")

    merged = (base_lines[:i_round2] + blocks["e402"] + [""]
              + blocks["e410_ig"] + base_lines[i_round2 + 1:])
    merged_text = "\n".join(merged) + "\n"

    # —— 校验链（fail-closed）——
    suffix = base_lines[i_round2 + 1:]
    if merged[:i_round2] != base_lines[:i_round2]:
        raise BuildAdoptError("前缀对钳制前躯不恒等")
    if merged[-len(suffix):] != suffix:
        raise BuildAdoptError("后缀对钳制前躯不恒等")
    _py_compile_ok(merged_text, "r34a")
    ast.parse(merged_text)
    last_name, ns = _exec_last_callable(merged_text, "r34a")
    if last_name != R34_LAST_CALLABLE:
        raise BuildAdoptError(f"r34a 末 callable={last_name!r}（期望 "
                              f"{R34_LAST_CALLABLE!r}）")
    required = ("e402_agent", "e410_agent", "_ig_standard",
                "_ig_guard_opening", "_ig_close_queue", "_E402_REPORT",
                "_E410_REPORT", "_IG_REPORT")
    missing = [n for n in required if n not in ns]
    if missing:
        raise BuildAdoptError(f"r34a 增量符号缺失：{missing}")
    leaked = sorted(k for k in ns if k.startswith("_cxs") or k == "_cxs_agent")
    if leaked:
        raise BuildAdoptError(f"r34a 残留 layer S 符号：{leaked}")
    # 常数面保持我方值（AST 实值断言，防注释错位）：
    consts = _constant_values(merged_text)
    expect = {"_V92_P_EVERY": 2, "_CA_MARGIN": -15.0, "_OR2_SLOT_MARGIN": 8.0,
              "V9_RACE_DEFAULT": [40, 44]}
    for key, want in expect.items():
        got = consts.get(key)
        if got != want:
            raise BuildAdoptError(f"r34a 常数 {key}={got!r}（期望 {want!r}）")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(merged_text)
    if open(out_path, "rb").read() != merged_text.encode("utf-8"):
        raise BuildAdoptError(f"r34a 回读不一致：{out_path}")
    return {
        "composition": comp,
        "splice": {
            "replaced_line": round2,
            "replaced_at_base_line": i_round2 + 1,
            "inserted_lines": len(blocks["e402"]) + 1 + len(blocks["e410_ig"]),
            "prefix_lines_identical": True,
            "suffix_lines_identical": True,
        },
        "increments": {
            "e402_block_lines": len(blocks["e402"]),
            "e410_ig_block_lines": len(blocks["e410_ig"]),
        },
        "last_callable": last_name,
        "layer_s_absent": True,
        "constants_kept_ours": {k: consts[k] for k in
                                ("_V92_P_EVERY", "_CA_MARGIN",
                                 "_OR2_SLOT_MARGIN", "V9_RACE_DEFAULT")},
        "main_sha256": _sha256_bytes(merged_text.encode("utf-8")),
        "main_bytes": len(merged_text.encode("utf-8")),
        "out_path": os.path.abspath(out_path),
    }


def _constant_values(text: str) -> Dict[str, Any]:
    """模块级常数赋值实值（AST）：同名多次赋值收 list（RACE 两处先 40 后 44）。"""
    tree = ast.parse(text)
    values: Dict[str, Any] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            try:
                literal = ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in (
                        "_V92_P_EVERY", "_CA_MARGIN", "_OR2_SLOT_MARGIN",
                        "V9_RACE_DEFAULT"):
                    if target.id in values:
                        if not isinstance(values[target.id], list):
                            values[target.id] = [values[target.id]]
                        values[target.id].append(literal)
                    else:
                        values[target.id] = literal
    return values


# ---------------------------------------------------------------------------
# apply_2965_constants
# ---------------------------------------------------------------------------
def apply_2965_constants(r34a_main_path: str, out_path: str) -> Dict[str, Any]:
    """r34b 常数面——恰三处替换（3/−5/20；RACE 不动）；定位数≠3 类错即抛。"""
    lines = open(r34a_main_path, "r", encoding="utf-8").read().split("\n")
    changed: List[Dict[str, Any]] = []
    for name, old, new in CONSTANT_SPECS:
        old_line, new_line = f"{name} = {old}", f"{name} = {new}"
        hits = [i for i, ln in enumerate(lines) if ln == old_line]
        if len(hits) != 1:
            raise BuildAdoptError(f"常数 {name} 旧值行定位数 {len(hits)}（期望 1）")
        lines[hits[0]] = new_line
        changed.append({"name": name, "line": hits[0] + 1, "old": old, "new": new})
    if len(changed) != 3:
        raise BuildAdoptError(f"替换数 {len(changed)}（期望恰 3）")
    text = "\n".join(lines)
    _py_compile_ok(text, "r34b")
    consts = _constant_values(text)
    want = {"_V92_P_EVERY": 3, "_CA_MARGIN": -5.0, "_OR2_SLOT_MARGIN": 20.0,
            "V9_RACE_DEFAULT": [40, 44]}
    for key, value in want.items():
        if consts.get(key) != value:
            raise BuildAdoptError(f"r34b 常数 {key}={consts.get(key)!r}"
                                  f"（期望 {value!r}）")
    diff_lines = [i + 1 for i, (a, b) in enumerate(
        zip(open(r34a_main_path, encoding="utf-8").read().split("\n"), lines))
        if a != b]
    if diff_lines != [c["line"] for c in changed]:
        raise BuildAdoptError(f"r34a→r34b 实差行 {diff_lines} 与登记不符")
    last_name, _ns = _exec_last_callable(text, "r34b")
    if last_name != R34_LAST_CALLABLE:
        raise BuildAdoptError(f"r34b 末 callable={last_name!r}")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return {
        "changes": changed,
        "n_changed_lines": len(diff_lines),
        "race_untouched": consts["V9_RACE_DEFAULT"] == [40, 44],
        "last_callable": last_name,
        "main_sha256": _sha256_bytes(text.encode("utf-8")),
        "main_bytes": len(text.encode("utf-8")),
        "out_path": os.path.abspath(out_path),
    }


# ---------------------------------------------------------------------------
# audit_diff_vs_2965
# ---------------------------------------------------------------------------
# 白名单归因规则（顺序敏感：先区间后标记）。白名单外差异=红。
_TAIL_ANCHOR = "submission_v59 = agent"   # 2965 尾部块起点（_NEW 起）


def _classify_hunk(ours: List[str], theirs: List[str], theirs_all: List[str],
                   j1: int, j2: int) -> str:
    """单个 diff hunk → 白名单类名；不可归因 → 'UNATTRIBUTED'。"""
    joined = "\n".join(ours + theirs)
    # ① 2965 尾部块（_NEW 包装/尾部常数重指/_HR 群饲增量）：整块不采纳
    tail_start = next((i for i, ln in enumerate(theirs_all)
                       if ln == _TAIL_ANCHOR), None)
    if tail_start is not None and j2 > tail_start:
        return "2965_tail_not_adopted(ledger/new/constants-override/_HR)"
    # ② 我方 CARROT2 钳制层
    if ("_ca_clamped_target" in joined or "_ca_future_plant_demand" in joined
            or "q = min(_CA_BUFFER" in joined):
        return "our_carrot2_clamp"
    # ③ 我方 T-B 番茄门（2965 无此块）
    if "_CXTB" in joined or "cxtb" in joined or "counter T-B" in joined:
        return "our_tb_tomato_gate"
    # ④ 我方 host-agnostic 包裹注释（CXTB 装载语注释）
    if "host-agnostic variant" in joined or "_CXTB_PARENT" in joined:
        return "our_cxtb_host_wrapper_comment"
    # ⑤ 2965 _LEDGER 遥测包装（submission_v57）
    if "_LEDGER" in joined or "submission_v57" in joined:
        return "2965_ledger_wrapper_not_adopted"
    # ⑥ 常数面差（r34a 保留我方值 vs 2965 中段值）
    for name in ("_V92_P_EVERY", "_CA_MARGIN", "_OR2_SLOT_MARGIN"):
        if any(ln.startswith(f"{name} =") for ln in ours + theirs):
            return "constants_delta(r34a_keeps_ours)"
    if any(ln.startswith("V9_RACE_DEFAULT") for ln in ours + theirs):
        return "race_delta(ours_44_vs_2965_41_midfile)"
    # ⑦ counter D 两处变体差（我方 fixed 可入槽位 vs 2965 continue；装载习语）
    if "_CXD_HOST" in joined:
        return "counter_d_host_idiom(ours_last_callable)"
    if "slots.append(i); fixed.append(o)" in joined or \
            "Keep every purchase/hire at its original index" in joined:
        return "counter_d_fixed_movable_variant(ours)"
    # ⑧ 注释/空行化妆差（纯注释行；或代码前缀同、仅行尾注释异——如 3589
    # path = None 行尾注释）
    nonblank = [ln for ln in ours + theirs if ln.strip()]
    if all(ln.lstrip().startswith("#") for ln in nonblank) or not nonblank:
        return "comment_or_blank_cosmetic"
    if (len(ours) == 1 and len(theirs) == 1
            and ours[0].split("#")[0] == theirs[0].split("#")[0]
            and ours[0].split("#")[0].strip()):
        return "comment_or_blank_cosmetic"
    return "UNATTRIBUTED"


def audit_diff_vs_2965(r34a_path: str, r34b_path: str,
                       src2965_path: str) -> Dict[str, Any]:
    """双件对 2965 原件逐行 diff 归因；白名单外差异=红（UNATTRIBUTED）。

    r34b 与原件的差异应恰为我方层（CARROT2 钳制叠加+T-B+装载习语）或
    明示不采纳面（ledger/尾块/RACE 中段 41）；r34a 另含常数面差。
    """
    import difflib
    theirs = open(src2965_path, encoding="utf-8").read().split("\n")
    result: Dict[str, Any] = {"src2965_sha256": _sha256_file(src2965_path)}
    ok_all = True
    for label, path in (("a", r34a_path), ("b", r34b_path)):
        ours = open(path, encoding="utf-8").read().split("\n")
        sm = difflib.SequenceMatcher(None, ours, theirs, autojunk=False)
        hunks: List[Dict[str, Any]] = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            klass = _classify_hunk(ours[i1:i2], theirs[j1:j2], theirs, j1, j2)
            hunks.append({
                "tag": tag, "class": klass,
                "our_span": [i1 + 1, i2], "their_span": [j1 + 1, j2],
                "our_lines": i2 - i1, "their_lines": j2 - j1,
                "sample_ours": ours[i1][:100] if i2 > i1 else None,
                "sample_theirs": theirs[j1][:100] if j2 > j1 else None,
            })
        attribution: Dict[str, int] = {}
        for h in hunks:
            attribution[h["class"]] = attribution.get(h["class"], 0) + 1
        unattributed = [h for h in hunks if h["class"] == "UNATTRIBUTED"]
        ok = not unattributed
        ok_all = ok_all and ok
        result[label] = {
            "ok": ok, "n_hunks": len(hunks), "attribution": attribution,
            "unattributed": unattributed, "hunks": hunks,
        }
    result["ok"] = ok_all
    return result


# ---------------------------------------------------------------------------
# 确定性打包（r30/v48 配方）
# ---------------------------------------------------------------------------
def build_tar_bytes(main_bytes: bytes) -> bytes:
    """v48_derivative_launch_check.build_tar_bytes 同款配方（零改动语义）。"""
    buf = io.BytesIO()
    gz = gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0)
    with tarfile.open(fileobj=gz, mode="w") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main_bytes)
        info.mode = 0o644
        info.mtime = 0
        info.uid = 0
        info.gid = 0
        tar.addfile(info, io.BytesIO(main_bytes))
    gz.close()
    return buf.getvalue()


def _package(dir_path: str, main_path: str, manifest_extra: Dict[str, Any]) -> Dict[str, Any]:
    """main → 确定性 tar（双跑逐字节）+manifest（r30 身份链键集）。"""
    main_bytes = open(main_path, "rb").read()
    tar1, tar2 = build_tar_bytes(main_bytes), build_tar_bytes(main_bytes)
    if tar1 != tar2:
        raise BuildAdoptError(f"tar 双跑不一致（非可复现）：{dir_path}")
    tar_path = os.path.join(dir_path, "submission.tar.gz")
    with open(tar_path, "wb") as fh:
        fh.write(tar1)
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as tar:
        names = tar.getnames()
        inner = tar.extractfile("main.py").read() if "main.py" in names else None
    if names != ["main.py"] or inner != main_bytes:
        raise BuildAdoptError(f"tar 成员/内层 main 校验失败：{names}")
    manifest = {
        "schema": "orderbook_2965_adopt_manifest/1.0",
        "generated": time.strftime("%Y-%m-%d"),
        "main_sha256": _sha256_bytes(main_bytes),
        "main_bytes": len(main_bytes),
        "tar_sha256": _sha256_bytes(tar1),
        "tar_bytes": len(tar1),
        "tar_members": names,
        "tar_rebuild_reproducible": True,
        "tar_size_ok": len(tar1) <= SIZE_CAP_BYTES,
    }
    manifest.update(manifest_extra)
    manifest_path = os.path.join(dir_path, "build_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return manifest


# ---------------------------------------------------------------------------
# build_2965_adopt（编排）
# ---------------------------------------------------------------------------
def build_2965_adopt() -> Dict[str, Any]:
    """CLI 编排：fetch→merge→constants→audit→双件打包+manifest。"""
    t0 = time.perf_counter()
    fetched = fetch_2965_source()
    a_dir, b_dir = os.path.join(HERE, "a"), os.path.join(HERE, "b")
    a_main, b_main = os.path.join(a_dir, "main.py"), os.path.join(b_dir, "main.py")
    for d in (a_dir, b_dir):
        os.makedirs(os.path.join(d, "evidence"), exist_ok=True)
    merge_audit = merge_increments(L3_MAIN, fetched["path"], a_main)
    const_audit = apply_2965_constants(a_main, b_main)
    diff_audit = audit_diff_vs_2965(a_main, b_main, fetched["path"])
    if not diff_audit["ok"]:
        unattr = {k: diff_audit[k]["unattributed"][:3]
                  for k in ("a", "b") if diff_audit[k]["unattributed"]}
        raise BuildAdoptError(f"diff 审计白名单外差异（fail-closed）：{unattr}")
    audit_path = os.path.join(HERE, "evidence", "audit_diff_vs_2965.json")
    os.makedirs(os.path.dirname(audit_path), exist_ok=True)
    with open(audit_path, "w", encoding="utf-8") as fh:
        json.dump(diff_audit, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    manifests = {}
    for label, d, main, desc, extra in (
            ("a", a_dir, a_main, DESCRIPTIONS["a"],
             {"variant": "r34a", "mode": "increments_ours_constants"}),
            ("b", b_dir, b_main, DESCRIPTIONS["b"],
             {"variant": "r34b", "mode": "increments_2965_constants"})):
        manifests[label] = _package(d, main, {
            "variant": extra["variant"], "mode": extra["mode"],
            "description": desc,
            "candidate": ("haideptry/the-2965-master-hybrid-engine 三增量采纳"
                          f"（EXP402/EXP410/_IG；{extra['variant']}）"
                          "——我 L3 钳制基座移植件，Apache-2.0"),
            "source_2965": {
                "kernel_slug": KERNEL_SLUG,
                "sha256": fetched["sha256"],
                "fetched_via": fetched["source"],
                "license": "Apache-2.0（embedded notices）",
            },
            "constants": ({"P_EVERY": 2, "CA_MARGIN": -15.0,
                           "OR2_SLOT": 8.0, "RACE": [40, 44]}
                          if label == "a" else
                          {"P_EVERY": 3, "CA_MARGIN": -5.0,
                           "OR2_SLOT": 20.0, "RACE": [40, 44]}),
            "provenance": {
                "base_l3_main": merge_audit["composition"]["l3_main_sha256"],
                "layer_s_block": merge_audit["composition"]["layer_s_block_sha256"],
                "clamped_prefix": merge_audit["composition"]["clamped_prefix_sha256"],
                "layer_s_removed": True,
                "increments": "EXP402+EXP410+_IG（2965 锚行抽取，字节保持）",
                "not_adopted": ("2965 尾部块：_LEDGER/_NEW 遥测包装、尾部常数"
                                "重指(2/44/8/-25)、_HR 群饲 PICKUP 增广——不在"
                                "三增量授权面"),
            },
        })
    summary = {
        "ok": True,
        "a": {"main_sha256": manifests["a"]["main_sha256"],
              "main_bytes": manifests["a"]["main_bytes"],
              "tar_sha256": manifests["a"]["tar_sha256"],
              "tar_bytes": manifests["a"]["tar_bytes"]},
        "b": {"main_sha256": manifests["b"]["main_sha256"],
              "main_bytes": manifests["b"]["main_bytes"],
              "tar_sha256": manifests["b"]["tar_sha256"],
              "tar_bytes": manifests["b"]["tar_bytes"]},
        "diff_attribution": {k: diff_audit[k]["attribution"]
                             for k in ("a", "b")},
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return summary


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:
        print("usage: python build_adopt.py（无参，产物落本包 a/b）",
              file=sys.stderr)
        return 2
    build_2965_adopt()
    return 0


if __name__ == "__main__":
    sys.exit(main())
