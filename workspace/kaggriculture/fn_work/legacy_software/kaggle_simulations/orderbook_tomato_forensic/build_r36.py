# -*- coding: utf-8 -*-
"""build_r36（R18 L1）：r34a 之上的白名单条件构建。

责任契约（fn_docs/hybrid/responsibility.md【R18 增补】）：
- build_r36_conditional(adopt_manifest, r34a_main_path, out_dir)：仅当 Phase T/
  判决清单中标 adopt 的项才并入——麦簇阈值（final_price_guard 31→T 三锚）/
  _CXTB 三常数（9000/0.75/2.4 胜点）/ _CXTB 阶梯化（80 单位拆批逐批过边际线
  的受控尾块）；diff 审计恰=并入项白名单；确定性打包沿 R16 配方（tarfile
  mtime0/uid/gid0/mode644、gzip mtime0、member ['main.py']、双跑逐字节）。
  任一步不确定即抛（fail-closed）。

变体文本构造器（apply_wheat_threshold/apply_cxtb_constants/stepped_block_text）
同时供 forensic 判决实验复用——单一真源，保证"判决实验的变体=构建并入的字节"。
"""

from __future__ import annotations

import difflib
import hashlib
import io
import json
import os
import sys
import tarfile
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(KSIM)
for _p in (KSIM, HERE, os.path.join(KSIM, "orderbook_2965_adopt")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from orderbook_2965_adopt import build_adopt as _ba
except ImportError:                                    # 脚本态
    from build_adopt import build_adopt as _ba         # type: ignore
from orderbook_r35 import phase_v as _pv              # KSIM 已在 sys.path

R34A_MAIN = os.path.join(KSIM, "orderbook_2965_adopt", "a", "main.py")
R34A_LAST_CALLABLE = "_cxd_agent"       # r34a 官方入口（未阶梯化时 r36 同名）
SIZE_CAP_BYTES = 100 * 1024 * 1024
DESCRIPTION = ("public derivative, tomato-commit stepped "
               "+ adjudicated tweaks")

# ---- 受控变更锚（各恰一处；多/少即抛） ----
WHEAT_CODE_OLD = "            if price < 31:"
WHEAT_TELEM_OLD = 'final_price_guard.telemetry={"sale_price_threshold":31}'
WHEAT_COMMENT_OLD = "# Correctly last-bound visible-price sale guard experiment; threshold=31."
CXTB_MINREV_OLD = "_CXTB_MIN_REVENUE = 9000"
CXTB_THEIR_OLD = "_CXTB_THEIR_UNITS = 0.75"
CXTB_SLACK_OLD = "_CXTB_DRAIN_SLACK = 2.4"
WHEAT_BASELINE = 31
CXTB_CONSTANTS_BASELINE = (9000, 0.75, 2.4)

R36_LAST_CALLABLE_STEPPED = "_r36_agent"   # 阶梯化尾块追加后的官方入口锚


class BuildR36Error(RuntimeError):
    """构建 fail-closed。"""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _replace_once(text: str, old: str, new: str, what: str) -> str:
    n = text.count(old)
    if n != 1:
        raise BuildR36Error(f"{what} 锚定位数 {n}（期望 1）")
    return text.replace(old, new)


def _fmt_num(v: float) -> str:
    return repr(v) if isinstance(v, float) else str(v)


# ---------------------------------------------------------------------------
# 变体构造器（判决实验与构建共用）
# ---------------------------------------------------------------------------
def apply_wheat_threshold(text: str, threshold: int) -> str:
    """麦簇守卫阈值 31→T（代码行+遥测行+注释行三锚，缺一即抛）。"""
    t = int(threshold)
    text = _replace_once(text, WHEAT_CODE_OLD,
                         "            if price < %d:" % t, "wheat guard code")
    text = _replace_once(
        text, WHEAT_TELEM_OLD,
        'final_price_guard.telemetry={"sale_price_threshold":%d}' % t,
        "wheat guard telemetry")
    text = _replace_once(
        text, WHEAT_COMMENT_OLD,
        "# Correctly last-bound visible-price sale guard experiment; threshold=%d." % t,
        "wheat guard comment")
    return text


def apply_cxtb_constants(text: str, min_revenue: int, their_units: float,
                         drain_slack: float) -> str:
    """_CXTB 三常数受控替换（各恰一处）。"""
    text = _replace_once(text, CXTB_MINREV_OLD,
                         "_CXTB_MIN_REVENUE = %d" % int(min_revenue),
                         "_CXTB_MIN_REVENUE")
    text = _replace_once(text, CXTB_THEIR_OLD,
                         "_CXTB_THEIR_UNITS = %s" % _fmt_num(float(their_units)),
                         "_CXTB_THEIR_UNITS")
    text = _replace_once(text, CXTB_SLACK_OLD,
                         "_CXTB_DRAIN_SLACK = %s" % _fmt_num(float(drain_slack)),
                         "_CXTB_DRAIN_SLACK")
    return text


STEPPED_HEADER = "# ==== R18 stepped tomato commitment (adjudicated; split the " \
                 "80-unit face into batches) ===="


def stepped_block_text(batches: Sequence[int],
                        density: float = 9000.0 / 80.0) -> str:
    """阶梯化尾块（受控模板；batches 如 (5,5)/(4,3,3)——每批在各自决策日
    以自身的边际线（density×该批单位数）重演 CXTB 投影后决定并入与否）。

    首批：day18 承诺时刻将 BUY_SEED 10 截为 batches[0]；后续批：day 19/20
    逐批评审，过线才追加种子。仅作用于 V219 全量承诺签名步，其余动作原样。
    """
    bs = tuple(int(b) for b in batches)
    if len(bs) not in (2, 3) or sum(bs) != 10 or any(b <= 0 for b in bs):
        raise BuildR36Error(f"batches 形态异常：{bs}（2-3 批和为 10）")
    body = STEPPED_HEADER + """

_R36_STEP_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_R36_BATCHES = %r
_R36_BATCH_DENSITY = %r
_R36_STEP_REPORT = dict(b1_cut=0, batches_added=0, batches_skipped=0, errors=0)
_R36_STEP_STATES = {}


def _r36_yield_days(plant_day):
    return [d for d in range(plant_day + 8, min(plant_day + 12, 30))]


def _r36_batch_revenue(obs, tiles, plant_day):
    \"\"\"该批自身单位在决策日的 CXTB 式投影收入（引擎价格曲线逐单位结算）。\"\"\"
    inventory = float(obs['market']['inventory']['TOMATO'])
    day = int(obs['step']) // 24
    shops = float(sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET')
                      for s in obs['town']['unlocked_shops']))
    pending = {22: 0.25, 24: 0.25}
    days = _r36_yield_days(plant_day)
    last = max(days)
    theirs = _cxtb_their_supply(obs, last)
    revenue = 0.0
    for d in range(day, last + 1):
        shops += pending.get(d, 0.0)
        inventory -= 1.0 + 6.0 * shops - _CXTB_DRAIN_SLACK
        inventory += theirs.get(d, 0.0)
        if d in days:
            for _ in range(tiles * 2):
                revenue += _r37_market_price('TOMATO', int(round(inventory)))
                inventory += 1
    return revenue


def _r36_step_agent(observation, configuration=None):
    action = _R36_STEP_PARENT(observation, configuration)
    try:
        step = int(observation['step'])
        seat = int(observation['player'])
        day = step // 24
        if step == 0:
            _R36_STEP_STATES[seat] = {'cut': 0, 'done': 0}
        st = _R36_STEP_STATES.get(seat) or {'cut': 0, 'done': 0}
        orders = action.get('market') or []
        if st['cut'] == 0 and day == 18:
            if (any(o and o[0] == 'BUY_LAND' for o in orders)
                    and any(o == ['BUY_SEED', 'TOMATO', 10] for o in orders)):
                action = copy.deepcopy(action)
                action['market'] = [
                    ['BUY_SEED', 'TOMATO', _R36_BATCHES[0]]
                    if o == ['BUY_SEED', 'TOMATO', 10] else o for o in orders]
                st['cut'] = 1
                _R36_STEP_REPORT['b1_cut'] += 1
        elif st['cut'] and st['done'] < len(_R36_BATCHES) - 1 and day == 18 + st['done'] + 1:
            tiles = _R36_BATCHES[st['done'] + 1]
            units = tiles * 2 * len(_r36_yield_days(day))
            if _r36_batch_revenue(observation, tiles, day) >= _R36_BATCH_DENSITY * units:
                if len(orders) < MAX_ORDERS:
                    action = copy.deepcopy(action)
                    action['market'] = orders + [['BUY_SEED', 'TOMATO', tiles]]
                    st['done'] += 1
                    _R36_STEP_REPORT['batches_added'] += 1
            else:
                st['done'] = len(_R36_BATCHES)
                _R36_STEP_REPORT['batches_skipped'] += 1
        _R36_STEP_STATES[seat] = st
    except Exception:
        _R36_STEP_REPORT['errors'] += 1
    return action


_r36_agent = _r36_step_agent
""" % (bs, float(density))
    return body


def apply_cxtb_stepped(text: str, batches: Sequence[int],
                       density: float = 9000.0 / 80.0) -> str:
    """阶梯化尾块受控追加（在 r34a 尾部追加；末 callable 变为 _r36_agent）。"""
    if not text.endswith("\n"):
        raise BuildR36Error("r34a 不以换行结尾（拼接语义变化）")
    return text + stepped_block_text(batches, density)


# ---------------------------------------------------------------------------
# diff 审计（r36 对 r34a 变更集恰=并入项白名单）
# ---------------------------------------------------------------------------
STEPPED_CLASS = "cxtb_stepped(appended tail block)"
WHEAT_CLASS = "wheat_step91_threshold(scan winner)"
CONSTANTS_CLASS = "cxtb_constants(scan winner)"
COSMETIC_CLASS = "blank_cosmetic"


def _is_wheat_price_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("if price < ") and s.endswith(":") \
        and s[11:-1].isdigit()


def _classify_r36_hunk(ours: List[str], theirs: List[str]) -> str:
    joined = "\n".join(ours + theirs)
    if (("threshold=" in joined or "sale_price_threshold" in joined)
            and "final_price_guard" in joined):
        return WHEAT_CLASS
    if any(_is_wheat_price_line(ln) for ln in ours + theirs):
        return WHEAT_CLASS
    if ("_R36_STEP_PARENT" in joined or "_r36_agent" in joined
            or "_r36_step_agent" in joined
            or "R18 stepped tomato commitment" in joined):
        return STEPPED_CLASS
    if "_CXTB_MIN_REVENUE" in joined or "_CXTB_THEIR_UNITS" in joined \
            or "_CXTB_DRAIN_SLACK" in joined:
        return CONSTANTS_CLASS
    nonblank = [ln for ln in ours + theirs if ln.strip()]
    if all(ln.lstrip().startswith("#") for ln in nonblank) or not nonblank:
        return COSMETIC_CLASS
    return "UNATTRIBUTED"


def _is_contiguous_slice(part: List[str], whole: List[str]) -> bool:
    """part 是否为 whole 的连续子段（追加块被 diff 拆分为多 hunk 时逐一容差，
    但所有 part 拼起来必须恰好重构 whole——由调用面 expected 集合保证单源）。"""
    if not part:
        return False
    for i in range(len(whole) - len(part) + 1):
        if whole[i:i + len(part)] == part:
            return True
    return False


def audit_diff_vs_r34a(r34a_path: str, r36_path: str,
                       expected_stepped_append: Optional[List[str]] = None
                       ) -> Dict[str, Any]:
    """r36 对 r34a 逐行 diff 归因；白名单外差异=红。

    expected_stepped_append 给定时（构建面），阶梯尾块类 hunk 的插入非空行
    必须与期望追加块逐行相等（防杂散行混入尾块 hunk 逃逸归因）。
    """
    ours = open(r34a_path, encoding="utf-8").read().split("\n")
    theirs = open(r36_path, encoding="utf-8").read().split("\n")
    sm = difflib.SequenceMatcher(None, ours, theirs, autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        klass = _classify_r36_hunk(ours[i1:i2], theirs[j1:j2])
        if klass == STEPPED_CLASS and expected_stepped_append is not None:
            inserted = [ln for ln in theirs[j1:j2] if ln.strip()]
            klass = "UNATTRIBUTED" if not _is_contiguous_slice(
                inserted,
                [ln for ln in expected_stepped_append if ln.strip()]) else klass
        hunks.append({"tag": tag, "class": klass,
                      "r34a_span": [i1 + 1, i2], "r36_span": [j1 + 1, j2],
                      "r34a_lines": i2 - i1, "r36_lines": j2 - j1,
                      "sample_r34a": ours[i1][:90] if i2 > i1 else None,
                      "sample_r36": theirs[j1][:90] if j2 > j1 else None})
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


def _py_compile_ok(text: str, tag: str) -> None:
    import py_compile
    import tempfile
    fd, tmp = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        py_compile.compile(tmp, doraise=True)
    except py_compile.PyCompileError as exc:
        raise BuildR36Error(f"{tag} py_compile 失败：{exc}") from exc
    finally:
        os.unlink(tmp)


def _package(out_dir: str, main_path: str, extra: Dict[str, Any]) -> Dict[str, Any]:
    main_bytes = open(main_path, "rb").read()
    tar1, tar2 = build_tar_bytes(main_bytes), build_tar_bytes(main_bytes)
    if tar1 != tar2:
        raise BuildR36Error("tar 双跑不一致（非可复现）")
    os.makedirs(out_dir, exist_ok=True)
    tar_path = os.path.join(out_dir, "submission.tar.gz")
    with open(tar_path, "wb") as fh:
        fh.write(tar1)
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as tar:
        names = tar.getnames()
        inner = tar.extractfile("main.py").read() if "main.py" in names else None
    if names != ["main.py"] or inner != main_bytes:
        raise BuildR36Error(f"tar 成员/内层 main 校验失败：{names}")
    manifest = {
        "schema": "orderbook_r36_manifest/1.0",
        "generated": time.strftime("%Y-%m-%d"),
        "variant": "r36",
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
# build_r36_conditional（编排）
# ---------------------------------------------------------------------------
def build_r36_conditional(adopt_manifest: Dict[str, Any],
                          r34a_main_path: str = R34A_MAIN,
                          out_dir: Optional[str] = None) -> Dict[str, Any]:
    """白名单条件构建。

    adopt_manifest 形如：
      {"cxtb_stepped": {"adopt": bool, "batches": (5,5), "density": 112.5},
       "cxtb_constants": {"adopt": bool, "min_revenue": int,
                          "their_units": float, "drain_slack": float},
       "wheat_threshold": {"adopt": bool, "threshold": int}}
    任一项 adopt=True 才落对应编辑；全 False → 抛（无条件项为零，构建无意义）。
    """
    t0 = time.perf_counter()
    out_dir = out_dir or HERE
    with open(r34a_main_path, "r", encoding="utf-8") as fh:
        r34a_text = fh.read()
    r34a_sha = _sha256_bytes(r34a_text.encode("utf-8"))
    adopted: Dict[str, Any] = {}
    expected_append: Optional[List[str]] = None
    text = r34a_text

    stepped = adopt_manifest.get("cxtb_stepped") or {}
    if stepped.get("adopt"):
        batches = tuple(int(b) for b in stepped["batches"])
        density = float(stepped.get("density", 9000.0 / 80.0))
        text = apply_cxtb_stepped(text, batches, density)
        block = stepped_block_text(batches, density)
        expected_append = block.split("\n")
        adopted["cxtb_stepped"] = {"batches": list(batches),
                                   "density": density}

    consts = adopt_manifest.get("cxtb_constants") or {}
    if consts.get("adopt"):
        text = apply_cxtb_constants(
            text, int(consts["min_revenue"]),
            float(consts["their_units"]), float(consts["drain_slack"]))
        adopted["cxtb_constants"] = {
            "min_revenue": int(consts["min_revenue"]),
            "their_units": float(consts["their_units"]),
            "drain_slack": float(consts["drain_slack"])}

    wheat = adopt_manifest.get("wheat_threshold") or {}
    if wheat.get("adopt"):
        text = apply_wheat_threshold(text, int(wheat["threshold"]))
        adopted["wheat_threshold"] = int(wheat["threshold"])

    if not adopted:
        raise BuildR36Error("adopt_manifest 无 adopt=True 项（r36 无条件项，不构建）")

    # —— 校验链（fail-closed）——
    _py_compile_ok(text, "r36")
    ns = _pv._exec_namespace(text, "r36_build_check")
    last_key = [k for k, v in ns.items() if callable(v)][-1]
    expect_last = (R36_LAST_CALLABLE_STEPPED
                   if adopted.get("cxtb_stepped") else R34A_LAST_CALLABLE)
    if last_key != expect_last:
        raise BuildR36Error(
            f"r36 末 callable key={last_key!r}（期望 {expect_last!r}）")
    for sym in ("_cxtb_agent", "e402_agent", "final_price_guard", "_CXTB_REPORT"):
        if sym not in ns:
            raise BuildR36Error(f"r36 符号缺失：{sym}")
    cv = _ba._constant_values(text)
    for key, want in (("_V92_P_EVERY", 2), ("_CA_MARGIN", -15.0),
                      ("_OR2_SLOT_MARGIN", 8.0), ("V9_RACE_DEFAULT", [40, 44])):
        if cv.get(key) != want:
            raise BuildR36Error(f"r36 常数 {key}={cv.get(key)!r}（期望 {want!r}）")
    # 三常数/阈值装载值回读（exec 命名空间真值，防文本/语义漂移）
    if adopted.get("cxtb_constants"):
        got = (ns.get("_CXTB_MIN_REVENUE"), ns.get("_CXTB_THEIR_UNITS"),
               ns.get("_CXTB_DRAIN_SLACK"))
        want_c = (adopted["cxtb_constants"]["min_revenue"],
                  adopted["cxtb_constants"]["their_units"],
                  adopted["cxtb_constants"]["drain_slack"])
        if got != want_c:
            raise BuildR36Error(f"_CXTB 常数装载值 {got!r} != 期望 {want_c!r}")
    if adopted.get("cxtb_stepped"):
        if tuple(ns.get("_R36_BATCHES") or ()) != tuple(
                adopted["cxtb_stepped"]["batches"]):
            raise BuildR36Error("_R36_BATCHES 装载值不符")

    os.makedirs(os.path.join(out_dir, "evidence"), exist_ok=True)
    main_path = os.path.join(out_dir, "main.py")
    with open(main_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    if open(main_path, "rb").read() != text.encode("utf-8"):
        raise BuildR36Error("r36 回读不一致")

    diff_audit = audit_diff_vs_r34a(r34a_main_path, main_path,
                                    expected_stepped_append=expected_append)
    expected_classes = {COSMETIC_CLASS}
    if adopted.get("cxtb_stepped"):
        expected_classes.add(STEPPED_CLASS)
    if adopted.get("cxtb_constants"):
        expected_classes.add(CONSTANTS_CLASS)
    if adopted.get("wheat_threshold"):
        expected_classes.add(WHEAT_CLASS)
    stray = set(diff_audit["attribution"]) - expected_classes
    if not diff_audit["ok"] or stray:
        raise BuildR36Error(
            f"diff 审计白名单外差异（fail-closed）：stray={sorted(stray)}，"
            f"unattributed={len(diff_audit['unattributed'])}")
    audit_path = os.path.join(out_dir, "evidence", "diff_audit_r36_vs_r34a.json")
    with open(audit_path, "w", encoding="utf-8") as fh:
        json.dump(diff_audit, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    manifest = _package(out_dir, main_path, {
        "mode": "r34a + R18 conditional whitelist",
        "last_callable": last_key,
        "adopted": adopted,
        "adopt_manifest": adopt_manifest,
        "provenance": {
            "base_r34a_main": r34a_sha,
            "base_r34a_pkg": "orderbook_2965_adopt/a（在飞件 ref 56526029 同字节）",
            "change_audit": {"diff_audit_path": audit_path},
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
        "last_callable": last_key,
        "out_dir": os.path.abspath(out_dir),
        "diff_attribution": diff_audit["attribution"],
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return summary
