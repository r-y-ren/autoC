# -*- coding: utf-8 -*-
# 【中文】build.py —— v48_hybrid 确定性装配器（assemble_package，R1-R5/R7）
# ===========================================================================
# 产物 = v48_derivative/main.py（sha256 dadee25a…2664a，107,008B）逐字前缀 +
#   追加块：三补丁源码（patches/*.py 只读、逐字内联进 b85|zlib blob，解码
#   与源字节一致，源 sha 登记）+ 统一仲裁接线（重定义 agent，基底 except
#   兜底逐字保留）。基底零行修改：五零改动区（磁带/路由/反克隆抢卖/槽位
#   重排/终局清仓）以前缀构造保持字节一致（audit_base.py 分区审计）。
# 仲裁次序（统一）：终局清仓 > 反克隆抢卖 > P3 卖单时点调整 > P1 中期卖单
#   接管 > 剧本默认；P2 在策略步返回前否决产线步骤（买畜/建棚，唯一碰产线
#   的补丁）。补丁异常一律回退该补丁未应用的 v48 原生动作（fail-safe）。
# 构建期开关：P1_ON/P2_ON/P3_ON（模块级常量，非运行时 env）；提交构建全开；
#   旗关构建=对应补丁零接线（blob 项/导入/接线/登记注记全部不发射，字节级
#   可验证，本脚本内存自证并写入 manifest）。
# 确定性：零时间戳/固定序/纯函数拼接；双次构建与双次打包逐字节一致由本
#   脚本自证。打包与 v48_derivative 同口径：单成员 main.py，mtime=0/
#   uid=gid=0/mode 0644，gzip mtime=0。
# CLI：python build.py [--p1 on|off] [--p2 on|off] [--p3 on|off] [--p4 on|off]
#   全开 → 写本目录 main.py/submission.tar.gz/build_manifest.json/README.md；
#   任一旗关 → 仅写 tmp/main_<flags>.py（诊断用，不产包不覆盖提交件）。
# ---------------------------------------------------------------------------
# 变更记录（R8 F4b，2026-09-22，结构性增补——漂移登记三则之一）：
#   增 P4 旗（默认 off，--p4 on 开；战后资产，不进当前提交件）：blob 内嵌
#   v48h.lead_protection（patches/lead_protection.py，F4a 产物）+ 装载注册
#   + 卖单面接线——agent() 返回前、P1/P3 之后调用
#   build_lead_protection(obs, day, sells)，day=step//24（_v48_get 可观
#   口径，P1/P3 先例）。P4 自带门栈（day>=24 且 lead>=3000、保护时点
#   6/12/18、step>=717 清仓窗让位；未触发/异常=原对象零足迹），不经 P1
#   defer 探针门控——其工作窗（d24+ 终局前夜）与 defer 的终局倾倒让位窗
#   重叠属设计本意（前移锁价正是要在该窗动作）。无扰动自证（旗面增量
#   不改变既有构建）：P4 off 时其全部发射位（旗行/头注/导入/接线/身份
#   尾注；blob 项与模块序本就按 on 过滤）整体不发射，任一 P1-P3 旗面
#   组合的构建与增补前逐字节一致（v4b 对照 = tmp/build_v5.py ④ 自证；
#   根提交件 P1-P3 全开亦同）。副作用登记：P4 默认 off 后，无参 CLI 恒
#   走诊断件路径（tmp/main_p1110.py），根提交件不再被无参调用再生；
#   --p4 on 全开会以含 P4 内容覆盖根提交件（冻结期 ba1b44c 禁用）。
# 变更记录（R8-v2 F5，2026-09-22，结构性增补）：
#   P4 触发面升级双条件并集【day>=15 且峰回撤 peak-lead>=2000 且
#   lead>=1500】∪【day>=24 且 lead>=3000】（v1 判决 FAIL 0/14 尸检：触发
#   过晚，9/14 局峰值日在 d17 前，6 局重演 P4 形态从未在场）；接线增峰
#   值运行寄存器 _V48H_P4_REGISTER（模块级 dict，P4 on 时发射、off 零痕
#   迹，token 集增 _V48H_P4_REGISTER 入零接线验证）；调用签名改
#   _v48h_p4_build(..., register=_V48H_P4_REGISTER)。P4 off 构建的无扰动
#   自证口径不变（P4 全发射位整体不发射）。
# ===========================================================================
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
import os
import re
import sys
import tarfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                      # kaggle_simulations/
SOFTWARE = os.path.dirname(KSIM)                  # software/
CAMP = os.path.dirname(SOFTWARE)                  # 战役根 kaggriculture/

BASE_MAIN = os.path.join(KSIM, "v48_derivative", "main.py")
PATCH_DIR = os.path.join(HERE, "patches")
SYNC_PROBE = os.path.join(SOFTWARE, "scripts", "sync_online_probe.py")

OUT_MAIN = os.path.join(HERE, "main.py")
OUT_TAR = os.path.join(HERE, "submission.tar.gz")
OUT_MANIFEST = os.path.join(HERE, "build_manifest.json")
OUT_README = os.path.join(HERE, "README.md")
TMP_DIR = os.path.join(HERE, "tmp")

BASE_SHA256 = ("dadee25a9840313218384208c53b2c4752f82c3209"
               "cc654632e0b96c65e2664a")
BASE_BYTES_EXPECT = 107008

SUBMIT_MESSAGE = "public derivative with modifications (market/economic-guard layers)"

# 补丁登记：旗名 → (blob 模块名, patches/ 源文件, 一句话角色, 接线符号集)
#   接线符号集 = 旗关构建中必须零出现的原文 token（零接线字节级验证）。
PATCHES = {
    "P1": {
        "module": "v48h.p1_midgame_sell_layer",
        "source": "midgame_sell_layer.py",
        "role": "midgame sell takeover (three-gate planner)",
        "tokens": ("v48h.p1_midgame_sell_layer", "_v48h_p1_apply",
                   "_v48h_p1_defer", "apply_to_market_orders",
                   "should_defer_to_tape"),
    },
    "P2": {
        "module": "v48h.p2_economic_guard",
        "source": "economic_guard.py",
        "role": "dead-pair economic guard (production veto)",
        "tokens": ("v48h.p2_economic_guard", "_v48h_p2_vetoe",
                   "vetoe_animal_and_shed_steps"),
    },
    "P3": {
        "module": "v48h.p3_milestone_monitor",
        "source": "milestone_monitor.py",
        "role": "milestone sell-timing monitor",
        "tokens": ("v48h.p3_milestone_monitor", "_v48h_p3_assess",
                   "_v48h_p3_adjust_timing", "_v48h_p3_sell_timing",
                   "assess_milestone_deviation", "adjust_sell_timing",
                   "_V48H_TURNS_PER_DAY"),
    },
    "P4": {
        "module": "v48h.lead_protection",
        "source": "lead_protection.py",
        "role": "lead-protection conservative sell timing (R8-v2 post-war)",
        "tokens": ("v48h.lead_protection", "_v48h_p4_build",
                   "build_lead_protection", "_V48H_P4_REGISTER"),
    },
}
PATCH_ORDER = ("P1", "P2", "P3", "P4")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_base() -> bytes:
    data = open(BASE_MAIN, "rb").read()
    if len(data) != BASE_BYTES_EXPECT or sha256_bytes(data) != BASE_SHA256:
        raise SystemExit(f"base sha/size mismatch: {sha256_bytes(data)} "
                         f"({len(data)}B)")
    if not data.endswith(b"\n"):
        raise SystemExit("base must end with newline")
    return data


def extract_base_agent_except(base_text: str) -> str:
    """基底 agent() 的 except 兜底块（逐字，含缩进）——接线块原样复用。"""
    lines = base_text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("def agent(obs, configuration=None):"):
            start = i
            break
    if start is None:
        raise SystemExit("base agent() not found")
    except_at = None
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("    except Exception:"):
            except_at = j
            break
        if lines[j].startswith("def ") or lines[j].startswith("_"):
            break
    if except_at is None:
        raise SystemExit("base agent() except block not found")
    block = []
    for j in range(except_at, len(lines)):
        ln = lines[j]
        if j > except_at and ln and not ln.startswith("    "):
            break
        block.append(ln)
    while block and not block[-1]:
        block.pop()
    return "\n".join(block)


def wrap_b85(payload: bytes, width: int = 78) -> str:
    text = base64.b85encode(zlib.compress(payload, 9)).decode("ascii")
    return "\n".join(f"    '{text[i:i + width]}'"
                     for i in range(0, len(text), width))


def extract_slug() -> tuple[str, str]:
    """从 sync_online_probe.py 程序化提取比赛 slug（README 提交命令用）。"""
    src = open(SYNC_PROBE, "r", encoding="utf-8").read()
    m = re.search(r'"competition":\s*"([A-Za-z0-9_.-]+)"', src)
    if not m:
        raise SystemExit("competition slug not found in sync_online_probe.py")
    return m.group(1), SYNC_PROBE


# ---------------------------------------------------------------------------
# 追加块装配（旗关 → 对应补丁段整体不发射：blob 项/导入/助手/接线/登记注记）
# ---------------------------------------------------------------------------
def build_block(flags: dict, base_text: str, patch_sources: dict,
                patch_shas: dict) -> str:
    on = {k: bool(flags[k]) for k in PATCH_ORDER}
    b_except = extract_base_agent_except(base_text)

    header = [
        "",
        "",
        "# ===========================================================================",
        "# v48_hybrid append block -- assembled by build.py (assemble_package,",
        "# R1-R5/R7); do not hand-edit: regenerate with `python build.py`.",
        f"# Base above = v48_derivative/main.py, sha256 {BASE_SHA256},",
        "# byte-verbatim prefix: zero modified base lines; the five zero-change",
        "# zones (tape / routing / anti-clone preemptive sell / sell-slot",
        "# reorder / terminal liquidation) are byte-identical by prefix",
        "# construction -- partitioned diff audit: audit_base.py.",
        "# Patch modules embedded verbatim below (blob decode == patches/*.py):",
    ]
    for key in PATCH_ORDER:
        if on[key]:
            header.append(f"#   {key} {PATCHES[key]['module']}  "
                          f"sha256 {patch_shas[key]}  "
                          f"{PATCHES[key]['role']}")
    if on["P4"]:
        # P4 专属头注（P4 off 时不发射——无扰动自证，见文件头变更记录）。
        # R8-v2（F5，2026-09-22）：触发面改双条件并集【day>=15 且峰回撤
        # peak-lead>=2000 且 lead>=1500】∪【day>=24 且 lead>=3000】；峰值经
        # 运行峰寄存器跟踪（编排处持有 _V48H_P4_REGISTER，跨回合注入）。
        header += [
            "# P4 lead-protection (R8-v2 post-war asset): runs last on the",
            "# sell side, after P1/P3; self-gated trigger union [day>=15 &",
            "# drawdown peak-lead>=2000 & lead>=1500] OR [day>=24 &",
            "# lead>=3000], running peak held in the orchestrator-owned",
            "# register _V48H_P4_REGISTER (injected per call; patch module",
            "# stays stateless); protective hour 6/12/18 & step<717 terminal",
            "# stand-down; no trigger / any error -> original sell list",
            "# untouched -- it is NOT gated by the P1 defer probe: its",
            "# working window (d15+ lead-collapse in progress, eve of the",
            "# endgame dump) overlaps the probe's endgame-dump stand-down",
            "# by design (front-loaded price-lock selling is precisely for",
            "# that window).",
        ]
    header += [
        "# Unified arbitration: terminal liquidation > anti-clone preemptive",
        "# sell > P3 sell-timing adjust > P1 midgame takeover > tape default.",
        "# The defer probe is P1's arbitration predicate (terminal frame /",
        "# endgame dump day>=26 / near-clone active frame / d0 -> every",
        "# sell-side patch stands down that step; v48 native wins).",
        "# P2 vetoes production steps (market BUY_ANIMAL removal, farmer/hands",
        "# BUILD_PASTURE -> PASS) on the policy step before it is returned --",
        "# the only patch touching the production line.",
        "# fail-safe: every patch call is individually wrapped; a failing patch",
        "# leaves the unpatched v48-native action for that patch; policy",
        "# exceptions still fall to the base handler below, byte-verbatim.",
        "# Build-time patch switches (module constants, not runtime env);",
        "# submission build = all on; a flag-off rebuild carries zero wiring",
        "# for that patch (byte-verifiable, see build_manifest.json).",
    ]
    # P4 旗行仅 on 时发射（P1-P3 先例是恒发射）：P4 off 构建须与增补前
    # 逐字节一致（无扰动自证），故 off 不留任何 P4 痕迹。
    flag_lines = [f"_V48H_{k}_ON = {on[k]!r}"
                  for k in PATCH_ORDER if k != "P4" or on["P4"]]
    if on["P4"]:
        # R8-v2：P4 峰值运行寄存器（编排处持有的跨回合状态；模块级 dict，
        # 每席每局独立装载天然隔离——P2 模块级 streak 先例；补丁模块自身
        # 保持纯函数，寄存器经参数注入）。
        flag_lines.append("_V48H_P4_REGISTER = {}")

    modules = {PATCHES[k]["module"]: patch_sources[k]
               for k in PATCH_ORDER if on[k]}
    blob_lines = wrap_b85(json.dumps(modules, sort_keys=True,
                                     ensure_ascii=True).encode("ascii"))
    order_items = ", ".join(repr(PATCHES[k]["module"])
                            for k in PATCH_ORDER if on[k])
    blob_part = [
        "",
        "_V48H_MODULES = json.loads(zlib.decompress(base64.b85decode(",
        "(",
        blob_lines,
        ")",
        ")).decode(\"utf-8\"))",
        f"_V48H_MODULE_ORDER = [{order_items}]",
        "for _v48h_name in _V48H_MODULE_ORDER:",
        "    _v48_load(_v48h_name, _V48H_MODULES[_v48h_name])",
        "",
    ]

    imports = []
    if on["P1"]:
        imports += [
            "from v48h.p1_midgame_sell_layer import "
            "apply_to_market_orders as _v48h_p1_apply",
            "from v48h.p1_midgame_sell_layer import "
            "should_defer_to_tape as _v48h_p1_defer",
            "",
        ]
    if on["P2"]:
        imports += [
            "from v48h.p2_economic_guard import "
            "vetoe_animal_and_shed_steps as _v48h_p2_vetoe",
            "",
        ]
    if on["P3"]:
        imports += [
            "from v48h.p3_milestone_monitor import "
            "TURNS_PER_DAY as _V48H_TURNS_PER_DAY",
            "from v48h.p3_milestone_monitor import "
            "assess_milestone_deviation as _v48h_p3_assess",
            "from v48h.p3_milestone_monitor import "
            "adjust_sell_timing as _v48h_p3_adjust_timing",
            "",
        ]
    if on["P4"]:
        imports += [
            "from v48h.lead_protection import "
            "build_lead_protection as _v48h_p4_build",
            "",
        ]

    helpers = []
    if on["P1"]:
        helpers += [
            "",
            "def _v48h_native_sell_frame(obs):",
            "    \"\"\"Unified v48-priority defer probe (P1's arbitration",
            "    predicate): terminal frame / endgame dump / near-clone active",
            "    frame / d0 -> True.  Any probe error defers (v48 native).\"\"\"",
            "    try:",
            "        return bool(_v48h_p1_defer(obs))",
            "    except Exception:",
            "        return True",
        ]
    if on["P3"]:
        helpers += [
            "",
            "def _v48h_p3_sell_timing(obs, step_out):",
            "    \"\"\"P3 seam: adjust timing of the SELL subset of",
            "    step_out[\"market\"] only (defer non-urgent sells on milestone",
            "    deviation).  Non-SELL market slots (BUY_* -- P2's veto face)",
            "    and farmer/hands are never touched; kept orders keep their",
            "    original slots (identity-based merge, relative order kept).\"\"\"",
            "    if not isinstance(step_out, dict):",
            "        return step_out",
            "    market = step_out.get(\"market\")",
            "    if not isinstance(market, list):",
            "        return step_out",
            "    step = int(_v48_get(obs, \"step\", 0) or 0)",
            "    deviation = _v48h_p3_assess(obs, step // _V48H_TURNS_PER_DAY)",
            "    if not isinstance(deviation, dict) or not deviation.get(\"deviated\"):",
            "        return step_out",
            "    sells = [o for o in market if isinstance(o, (list, tuple)) and o",
            "             and o[0] == \"SELL\"]",
            "    if not sells:",
            "        return step_out",
            "    kept = _v48h_p3_adjust_timing(sells, deviation)",
            "    if kept is sells or len(kept) == len(sells):",
            "        return step_out",
            "    kept_ids = {id(o) for o in kept}",
            "    if not kept_ids <= {id(o) for o in sells}:",
            "        return step_out          # unknown objects: fail-safe, no change",
            "    out = dict(step_out)",
            "    out[\"market\"] = [o for o in market",
            "                     if not (isinstance(o, (list, tuple)) and o",
            "                             and o[0] == \"SELL\")",
            "                     or id(o) in kept_ids]",
            "    return out",
        ]

    agent_body = [
        "",
        "",
        "def agent(obs, configuration=None):",
        "    try:",
        "        _policy_out = _V48_POLICY(obs, configuration)",
    ]
    if on["P2"]:
        agent_body += [
        "        if _V48H_P2_ON:",
        "            try:",
        "                _policy_out = _v48h_p2_vetoe([_policy_out], obs)[0]",
        "            except Exception:",
        "                pass",
        ]
    if on["P1"]:
        agent_body += [
        "        _v48h_defer_frame = _v48h_native_sell_frame(obs)",
        ]
    elif on["P3"]:
        agent_body += [
        "        _v48h_defer_frame = False   # P1 off: no defer probe; P3 ungated",
        ]
    if on["P1"]:
        agent_body += [
        "        if _V48H_P1_ON and not _v48h_defer_frame:",
        "            try:",
        "                _policy_out[\"market\"] = _v48h_p1_apply(",
        "                    obs, _policy_out[\"market\"])",
        "            except Exception:",
        "                pass",
        ]
    if on["P3"]:
        agent_body += [
        "        if _V48H_P3_ON and not _v48h_defer_frame:",
        "            try:",
        "                _policy_out = _v48h_p3_sell_timing(obs, _policy_out)",
        "            except Exception:",
        "                pass",
        ]
    if on["P4"]:
        # P4 卖单面接线（R8-v2 F5）：day=step//24（_v48_get 可观口径，P1/P3
        # 先例）；峰值寄存器 _V48H_P4_REGISTER 跨回合注入（R8-v2 签名变更：
        # build_lead_protection(obs, day, sells, config=None, register=None)）。
        # P4 自带门栈（双条件并集触发/保护时点/717 让位），不经 defer 探针。
        agent_body += [
        "        if _V48H_P4_ON:",
        "            try:",
        "                _policy_out[\"market\"] = _v48h_p4_build(",
        "                    obs, int(_v48_get(obs, \"step\", 0) or 0) // 24,",
        "                    _policy_out[\"market\"],",
        "                    register=_V48H_P4_REGISTER)",
        "            except Exception:",
        "                pass",
        ]
    agent_body += ["        return _policy_out"]
    agent_body += b_except.split("\n")   # 基底 except 兜底逐字（同缩进级）

    tail = [
        "",
        "",
        "def _v48hybrid_entrypoint(obs, configuration=None):",
        "    return agent(obs, configuration)",
        "",
        "",
        "agent.v48hybrid = {",
        f"    \"base_sha256\": {BASE_SHA256!r},",
        "    \"patches\": {",
    ]
    for key in PATCH_ORDER:
        if key == "P4" and not on["P4"]:
            continue          # P4 off：身份尾注零 P4 痕迹（无扰动自证）
        tail.append(f"        {key!r}: {patch_shas[key]!r},")
    flag_items = [f'"{k}_ON": {on[k]!r}'
                  for k in PATCH_ORDER if k != "P4" or on["P4"]]
    tail += [
        "    },",
        '    "flags": {' + ", ".join(flag_items) + "},",
        "}",
        "",
    ]

    parts = [header, flag_lines, blob_part, imports, helpers, agent_body, tail]
    return "\n".join("\n".join(p) for p in parts if p) + "\n"


def build_once(flags: dict) -> bytes:
    base = load_base()
    base_text = base.decode("utf-8")
    patch_sources, patch_shas = {}, {}
    for key in PATCH_ORDER:
        raw = open(os.path.join(PATCH_DIR, PATCHES[key]["source"]),
                   "rb").read()
        patch_sources[key] = raw.decode("utf-8")
        patch_shas[key] = sha256_bytes(raw)
    return base + build_block(flags, base_text, patch_sources,
                              patch_shas).encode("utf-8")


def verify_zero_wiring(all_on: bytes) -> dict:
    """旗关变体（内存构建，仅该旗关）对相应补丁 token 的原文出现数须为 0；
    全开件中 token 必须在场（接线真实存在）。"""
    result = {}
    on_text = all_on.decode("utf-8")
    for key in PATCH_ORDER:
        variant = build_once({k: (k != key) for k in PATCH_ORDER})
        text = variant.decode("utf-8")
        hits = {tok: text.count(tok) for tok in PATCHES[key]["tokens"]}
        result[key] = {
            "zero_wiring_ok": all(v == 0 for v in hits.values()),
            "token_hits": hits,
            "tokens_present_when_on": all(
                on_text.count(tok) >= 1 for tok in PATCHES[key]["tokens"]),
        }
    return result


def pack_tar(source: bytes) -> bytes:
    """确定性 tar.gz（v48_derivative 同口径：单 main.py，全零元数据）。"""
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
    gz.close()   # 写 gzip trailer（tarfile 不代管传入的 fileobj）
    return buf.getvalue()


def build_readme(slug: str, slug_src: str, main_sha: str, main_bytes: int,
                 tar_sha: str, tar_bytes: int, patch_shas: dict,
                 patch_sizes: dict, flags: dict,
                 wiring: dict) -> str:
    here_abs = HERE
    lines = []
    a = lines.append
    a("# v48_hybrid — v48 混合候选提交包（方案甲，assemble_package 产物）")
    a("")
    a("> 本目录产物全部由 `python build.py` 确定性生成（零时间戳/固定序，"
      "双跑逐字节一致）；`python audit_base.py` 为基底五区零改动分区审计。"
      "基底 `../v48_derivative/main.py` 与 `patches/*.py` 只读不改。")
    a("")
    a("## 身份链（identity chain）")
    a("")
    a("| 件 | sha256 | 字节 |")
    a("|---|---|---|")
    a(f"| 基底 `../v48_derivative/main.py` | `{BASE_SHA256}` | "
      f"{BASE_BYTES_EXPECT} |")
    for key in PATCH_ORDER:
        a(f"| {key} `patches/{PATCHES[key]['source']}` | "
          f"`{patch_shas[key]}` | {patch_sizes[key]} |")
    a(f"| 混合 `main.py`（基底逐字前缀 + 追加块） | `{main_sha}` | "
      f"{main_bytes} |")
    a(f"| `submission.tar.gz`（单成员 main.py，确定性 tar） | `{tar_sha}` | "
      f"{tar_bytes} |")
    a("")
    flag_txt = " ".join(f"{k}_ON={flags[k]}" for k in PATCH_ORDER)
    a(f"开关状态：`{flag_txt}`（提交构建全开；旗关重建=对应补丁零接线，"
      "字节级验证见 `build_manifest.json` 的 `flag_off_zero_wiring`）")
    a("")
    a("## 仲裁次序（追加块内统一实现）")
    a("")
    a("终局清仓 > 反克隆抢卖 > P3 卖单时点调整 > P1 中期卖单接管 > "
      "剧本默认；P2 在策略步返回前否决产线步骤（market `BUY_ANIMAL` 删除、"
      "farmer/hands `BUILD_PASTURE`→`PASS`，唯一碰产线的补丁）。"
      "补丁异常一律回退该补丁未应用的 v48 原生动作；基底 except 兜底逐字保留。")
    a("")
    a("## 提交（人工执行；蓝图 out_of_scope）")
    a("")
    a("```bash")
    a(f"cd {here_abs}")
    a(f"kaggle competitions submit -c {slug} -f submission.tar.gz "
      f"-m \"{SUBMIT_MESSAGE}\"")
    a("```")
    a("")
    a(f"- slug `{slug}` 由 build.py 从 `software/scripts/sync_online_probe.py`"
      f" 程序化提取（`\"competition\": \"{slug}\"`）。")
    a(f"- 描述文案（`-m`）：{SUBMIT_MESSAGE}")
    a("- 提交预算：每日≤5、每候选≤2、Error 即停（继承 SOP）。")
    a("")
    a("## 门禁结果（F3 verify_offline_gates 回填；此处为占位）")
    a("")
    a("| 门 | 判据 | 结果 | 数字 |")
    a("|---|---|---|---|")
    a("| h2h | seated ≥16 局 vs 纯 v48 互胜 ≥0.65 | PENDING | — |")
    a("| panel | 孪生 d0 反事实资金 ratio ≥0.98 | PENDING | — |")
    a("| zero-new-anomalies | 全 DONE 且异常集对照纯 v48 零新增 | PENDING | — |")
    a("| launch fourgate | 装载语义/双席自打 DONE/确定性/体积身份链 | "
      "PENDING | — |")
    a("")
    a("本批次（F2）冒烟已执行：官方装载语义（干净 -I 子进程 "
      "get_last_callable 复刻）、vendored 引擎双席自打 ≥2 局 DONE、"
      "确定性双跑逐字节——数字见批次报告与 `tmp/` 探针产物。")
    a("")
    a("## 目录结构")
    a("")
    a("- `main.py` — 基底逐字前缀 + 追加块（三补丁 blob + 仲裁接线 + 入口）")
    a("- `submission.tar.gz` — 提交包（单成员 main.py，mtime=0/uid=gid=0/"
      "mode 0644，gzip mtime=0）")
    a("- `build_manifest.json` — 基底 sha/混合 main sha/包 sha/补丁清单/"
      "开关状态/零接线验证/门禁占位")
    a("- `build.py` / `audit_base.py` — 装配器与分区审计（确定性，可复跑）")
    a("- `patches/` — 三补丁叶与其测试（F1 产物，只读）")
    a("- `tmp/` — 冒烟/诊断临时产物（不入库语义，旗关诊断件亦落此）")
    a("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="v48_hybrid deterministic "
                                             "assembler")
    ap.add_argument("--p1", choices=("on", "off"), default="on")
    ap.add_argument("--p2", choices=("on", "off"), default="on")
    ap.add_argument("--p3", choices=("on", "off"), default="on")
    ap.add_argument("--p4", choices=("on", "off"), default="off")   # R8 F4b
    args = ap.parse_args()
    flags = {"P1": args.p1 == "on", "P2": args.p2 == "on",
             "P3": args.p3 == "on", "P4": args.p4 == "on"}
    all_on = all(flags.values())

    first = build_once(flags)
    second = build_once(flags)
    if first != second:
        raise SystemExit("build is not deterministic")
    compile(first, "main.py", "exec")

    if not all_on:
        os.makedirs(TMP_DIR, exist_ok=True)
        tag = "".join("1" if flags[k] else "0" for k in PATCH_ORDER)
        out = os.path.join(TMP_DIR, f"main_p{tag}.py")
        with open(out, "wb") as h:
            h.write(first)
        print(json.dumps({"diagnostic_build": out,
                          "flags": flags,
                          "sha256": sha256_bytes(first),
                          "bytes": len(first)}, indent=2))
        return 0

    wiring = verify_zero_wiring(first)

    base = load_base()
    prefix_ok = first.startswith(base)
    if not prefix_ok:
        raise SystemExit("hybrid main.py is not a byte-verbatim base prefix")

    tar_bytes = pack_tar(first)
    tar_again = pack_tar(build_once(flags))
    if tar_again != tar_bytes:
        raise SystemExit("tar packing is not deterministic")
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as t:
        names = t.getnames()
        inner = t.extractfile("main.py").read()
    if names != ["main.py"] or inner != first:
        raise SystemExit("tar member/byte mismatch")

    with open(OUT_MAIN, "wb") as h:
        h.write(first)
    with open(OUT_TAR, "wb") as h:
        h.write(tar_bytes)

    slug, slug_src = extract_slug()
    patch_shas, patch_sizes = {}, {}
    for key in PATCH_ORDER:
        raw = open(os.path.join(PATCH_DIR, PATCHES[key]["source"]),
                   "rb").read()
        patch_shas[key] = sha256_bytes(raw)
        patch_sizes[key] = len(raw)

    manifest = {
        "base": {"path": "software/kaggle_simulations/v48_derivative/main.py",
                 "sha256": BASE_SHA256, "bytes": BASE_BYTES_EXPECT,
                 "verbatim_prefix": prefix_ok},
        "patches": {key: {"module": PATCHES[key]["module"],
                          "source": f"patches/{PATCHES[key]['source']}",
                          "sha256": patch_shas[key],
                          "bytes": patch_sizes[key],
                          "role": PATCHES[key]["role"]}
                    for key in PATCH_ORDER},
        "flags": {f"{k}_ON": flags[k] for k in PATCH_ORDER},
        "flag_off_zero_wiring": {k: wiring[k]["zero_wiring_ok"]
                                 and wiring[k]["tokens_present_when_on"]
                                 for k in PATCH_ORDER},
        "main_py": {"bytes": len(first), "sha256": sha256_bytes(first),
                    "base_prefix_bytes": BASE_BYTES_EXPECT},
        "submission_tar_gz": {"bytes": len(tar_bytes),
                              "sha256": sha256_bytes(tar_bytes),
                              "members": names,
                              "deterministic_double_pack": True},
        "deterministic_double_build": True,
        "stdlib_only": True,
        "competition_slug": {"value": slug,
                             "extracted_from":
                                 "software/scripts/sync_online_probe.py"},
        "submit_message": SUBMIT_MESSAGE,
        "gate_results": {"status": "PENDING",
                         "note": "F3 verify_offline_gates 回填：h2h/panel/"
                                 "zero-new-anomalies/launch-fourgate"},
    }
    with open(OUT_MANIFEST, "w", encoding="utf-8") as h:
        json.dump(manifest, h, indent=2, sort_keys=True)
        h.write("\n")

    readme = build_readme(slug, slug_src, sha256_bytes(first), len(first),
                          sha256_bytes(tar_bytes), len(tar_bytes),
                          patch_shas, patch_sizes, flags, wiring)
    with open(OUT_README, "w", encoding="utf-8") as h:
        h.write(readme)

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
