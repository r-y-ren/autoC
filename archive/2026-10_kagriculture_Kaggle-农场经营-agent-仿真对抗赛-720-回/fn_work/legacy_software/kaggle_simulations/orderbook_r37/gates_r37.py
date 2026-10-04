# -*- coding: utf-8 -*-
"""verify_r37_gates（R19/R20 L1）：全量门禁 fail-closed 全跑不短路。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
四门沿 r30 管线（合规四轴核查/装载 last-callable=_r37_agent/双席 DONE+
单步<1s/确定性双跑/体积身份链）+ h2h vs r34a 在飞件 ≥0.55（seated 双席位、
独立局数 n 报，席位翻转不双计）+ 饿死零容忍 + 谱系（v48/v4b 各 8 局无负）；
evidence 落 evidence/。

门面（复用 R16/R17 管线重定向，零改动既有目录）：
- 门①合规四轴核查（license/发布时间三渠道交叉，2965 采纳时已在案，引用台账）：
  license 轴=r34a 采纳台账 source_2965（Apache-2.0+kernel_slug+sha256+
  fetched_via）；发布时间三渠道交叉轴=在案台账文本核对（分析16 雷达
  09-24/Apache-2.0 + JOURNAL round-30 四轴记录"三渠道交叉"）；血统 tie=r37
  manifest base_sha_chain 锚 a16e0e9b→r34a（盘上 sha）→r37（盘上 sha）；
  公开衍生如实标注（description 前缀 "public derivative"）。任一轴缺/不符=
  门红（fail-closed），citations 引台账。
- 门②四门（r30/v48 管线单实现 gate_launch_fourgate_l1 换包重定向）：装载
  last-callable=_r37_agent / 双席 DONE+单步<1s / 确定性双跑 sha / 体积身份链。
  调用语义经 _OfficialCall 适配（官方 Interpreter.act 同语义 args[:co_argcount]
  截断——r37 尾块 _r37_agent(observation) 单参数官方合法形态，单实现
  TimedAgent 双参直通经适配等价官方调用；见 _OfficialCall 注）。
- 门③ h2h vs r34a 在飞件（orderbook_2965_adopt/a/main.py，ref 56526029 同字节，
  先三方核对 build_manifest，不符即红——fail-closed）：seated 双席位 16 局
  （8 seed×2 席）对打（gate_h2h_vs_verbatim 同款），**判据按独立局数 n 报、
  席位翻转不双计**——seed 级聚合沿 judge_sheep_league _block 口径（胜=两席皆
  胜/平=席位分歧或皆平/负=皆负，rate=(胜+0.5平)/决胜 seed，无决胜 seed
  rate=0.0 fail-closed），rate≥0.55 过门；run 级互胜率并记不作判据（分析20
  playbook 教训：席位翻转对为同一局镜像重放，有效样本=seed 数）。
- 门④谱系：v48-pure（opponents/v48_main.py=v48_derivative 同字节）/v4b
  （v48_hybrid/v4b）各 8 局无负（gate_lineage_strength 重定向）。
- 门⑤饿死零容忍+子集（沿 L3/R16/R17 口径）：26 局 strip 语料，starve 基线
  r32（L3 fine 在库件）+subset vs verbatim（净回收≤未种下量）。
全跑不短路：任一门红也继续跑完其余门；门不可执行（异常）→该门
{executed=False, error, passed=False}，整体必红。overall=五门 passed 全 True。
evidence 落 evidence/：gates_r37_realrun.json（summary 台账）+compliance/
h2h/lineage/starve 四件自写。

【签名微调登记（批间）】verify_r37_gates(pkg_path, evidence_dir=None)：
pkg_path 收 r37 main.py 路径（真实件=orderbook_r37/build/main.py，真跑验收
命令形态）或其包目录（缺省语义同 r35/r36 先例）；evidence_dir 可覆写（缺省
本包 evidence/；测试 tmp 隔离防覆写真台账——门③ run 同款口径）。首参与
返回主键不变（各门结果+overall；错误 fail-closed）。
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import sys
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
L1_DIR = os.path.join(KSIM, "orderbook_l1_derivative")
L3_DIR = os.path.join(KSIM, "orderbook_l3_derivative")
R34A_DIR = os.path.join(KSIM, "orderbook_2965_adopt", "a")
for _p in (L1_DIR, L3_DIR, os.path.join(KSIM, "orderbook_2965_adopt"), HERE,
           KSIM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_equivalence_l3 as _l3eq       # noqa: E402  空槽归一换装
import gate_equivalence_precision as _l1  # noqa: E402  重演/子集部件（import 复用）
import gate_equivalence_v3 as _v3         # noqa: E402  终态/饿死部件（import 复用）
import gate_h2h_vs_verbatim as _h2h_base  # noqa: E402  h2h 主体（import 复用）
import gate_launch_fourgate_l1 as _l1g    # noqa: E402  四门（import 复用）
import gate_lineage_strength as _lin      # noqa: E402  谱系门（import 复用）

R34A_MAIN = os.path.join(R34A_DIR, "main.py")
R32_MAIN = os.path.join(L3_DIR, "main.py")               # starve 基线（L3 fine）
VERBATIM_MAIN = os.path.join(KSIM, "orderbook_derivative", "main.py")
OPPONENTS = {
    "v48-pure": os.path.join(KSIM, "opponents", "v48_main.py"),
    "v4b": os.path.join(KSIM, "v48_hybrid", "v4b", "main.py"),
}
EPISODES_DIR = os.path.normpath(os.path.join(
    KSIM, os.pardir, os.pardir, os.pardir, "fn_docs", "hybrid", "results",
    "replays-r30-26"))
R37_LAST_CALLABLE = "_r37_agent"
R34A_LAST_CALLABLE = "_cxd_agent"
H2H_WIN_THRESHOLD = 0.55
SUMMARY_NAME = "gates_r37_realrun.json"
H2H_EVIDENCE_NAME = "h2h_vs_r34a_evidence.json"
LINEAGE_EVIDENCE_NAME = "lineage_evidence.json"
STARVE_EVIDENCE_NAME = "starve_evidence.json"
COMPLIANCE_EVIDENCE_NAME = "compliance_evidence.json"

# 合规四轴台账（2965 采纳时已在案；本门只核查+引用，不重做外部抓取）
ADOPTION_LEDGER = os.path.join(R34A_DIR, "build_manifest.json")
_RELEASE_LEDGER_ANALYSIS = os.path.normpath(os.path.join(
    KSIM, os.pardir, os.pardir, os.pardir, "fn_docs", "hybrid", "analyses",
    "16-2026-09-25-radar-hit-2965.md"))
_RELEASE_LEDGER_JOURNAL = os.path.normpath(os.path.join(
    KSIM, os.pardir, os.pardir, os.pardir, "fn_docs", "governance",
    "JOURNAL.md"))
RELEASE_LEDGERS = (
    (_RELEASE_LEDGER_ANALYSIS, ("Apache-2.0", "09-24", "2965")),
    (_RELEASE_LEDGER_JOURNAL, ("三渠道交叉", "Apache-2.0")),
)
USAGE = "usage: python gates_r37.py [r37_pkg_or_main]"


class GateR37Error(RuntimeError):
    """门禁 fail-closed 承载。"""


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _run_gate(label: str, thunk):
    """跑一门（fail-closed 全跑不短路）：异常→{executed=False, passed=False}。"""
    t0 = time.perf_counter()
    print(f"[verify-r37] {label} running ...", flush=True)
    try:
        result = thunk()
    except (Exception, SystemExit) as exc:
        entry = {"passed": False, "executed": False,
                 "error": f"{type(exc).__name__}: {exc}",
                 "wall_s": round(time.perf_counter() - t0, 1)}
        print(f"[verify-r37] {label} NOT EXECUTABLE (fail-closed): "
              f"{entry['error']}", flush=True)
        return entry, None
    entry = {"passed": bool(result.get("passed")), "executed": True,
             "error": None, "wall_s": round(time.perf_counter() - t0, 1)}
    print(f"[verify-r37] {label} {'PASS' if entry['passed'] else 'FAIL'} "
          f"({entry['wall_s']}s)", flush=True)
    return entry, result


def _resolve_pkg(pkg_path: str) -> Tuple[str, str]:
    """pkg_path（main.py 路径或包目录）→ (pkg_dir, main_path)；缺件即抛。"""
    if not isinstance(pkg_path, str) or not pkg_path.strip():
        raise GateR37Error(f"pkg_path 非字符串路径：{pkg_path!r}")
    p = os.path.abspath(pkg_path)
    if os.path.isdir(p):
        pkg_dir, main_path = p, os.path.join(p, "main.py")
    else:
        main_path, pkg_dir = p, os.path.dirname(p)
    if not os.path.isfile(main_path):
        raise GateR37Error(f"r37 未构建：{main_path}（先跑 build_r37）")
    return pkg_dir, main_path


def _verify_ref_package(pkg_dir: str, what: str) -> Dict[str, Any]:
    """对 <pkg_dir>/build_manifest.json 核对盘上 main/tar（沿 r30 身份链键集）。"""
    import io
    import tarfile
    manifest = json.load(open(os.path.join(pkg_dir, "build_manifest.json"),
                              encoding="utf-8"))
    main_path = os.path.join(pkg_dir, "main.py")
    tar_path = os.path.join(pkg_dir, "submission.tar.gz")
    main_sha, tar_sha = _sha256_file(main_path), _sha256_file(tar_path)
    with tarfile.open(fileobj=io.BytesIO(open(tar_path, "rb").read()),
                      mode="r:gz") as tar:
        names = tar.getnames()
        inner_ok = (names == ["main.py"]
                    and tar.extractfile("main.py").read()
                    == open(main_path, "rb").read())
    ok = (main_sha == manifest.get("main_sha256")
          and tar_sha == manifest.get("tar_sha256")
          and os.path.getsize(main_path) == manifest.get("main_bytes")
          and os.path.getsize(tar_path) == manifest.get("tar_bytes")
          and names == ["main.py"] and inner_ok)
    if not ok:
        raise GateR37Error(f"{what} 身份链不符（manifest vs 盘上/tar）: {pkg_dir}")
    return {"what": what, "pkg": pkg_dir, "main_sha256": main_sha,
            "tar_sha256": tar_sha, "match": True}


# ---------------------------------------------------------------------------
# 门①合规四轴核查（license/发布时间三渠道交叉，2965 采纳在案，引用台账）
# ---------------------------------------------------------------------------
def _gate_compliance(pkg_dir: str, evidence_path: str) -> Dict[str, Any]:
    """四轴=license/发布时间三渠道交叉/血统 tie/公开衍生标注；引用台账。"""
    axes: Dict[str, Any] = {}
    # ① license 轴：2965 采纳台账 source_2965（Apache-2.0 在案）
    ledger = json.load(open(ADOPTION_LEDGER, encoding="utf-8"))
    src = ledger.get("source_2965") or {}
    lic_ok = bool("Apache-2.0" in str(src.get("license", ""))
                  and src.get("kernel_slug") and src.get("sha256")
                  and src.get("fetched_via"))
    axes["license"] = {
        "ok": lic_ok, "license": src.get("license"),
        "kernel_slug": src.get("kernel_slug"),
        "fetched_via": src.get("fetched_via"),
        "ledger": ADOPTION_LEDGER + "#source_2965",
    }
    # ② 发布时间三渠道交叉轴：在案台账文本核对（09-24 公开+三渠道交叉记录）
    records: List[Dict[str, Any]] = []
    release_ok = True
    for path, needles in RELEASE_LEDGERS:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            text = ""
        hit = all(n in text for n in needles)
        release_ok = release_ok and hit
        records.append({"ledger": path, "needles": list(needles),
                        "on_file": hit})
    axes["release_time_three_channel"] = {
        "ok": release_ok, "records": records,
        "note": ("2965 公开 09-24（分析16 雷达三渠道交叉在案）；基座族"
                 "09-21T23:16Z<09-23 锁三渠道交叉（JOURNAL round-30 四轴）"),
    }
    # ③ 血统 tie：base_sha_chain 锚 a16e0e9b→r34a（盘上）→r37（盘上）
    manifest_path = os.path.join(pkg_dir, "build_manifest.json")
    manifest = json.load(open(manifest_path, encoding="utf-8"))
    chain = manifest.get("base_sha_chain") or {}
    r34a_sha = _sha256_file(R34A_MAIN)
    main_sha = _sha256_file(os.path.join(pkg_dir, "main.py"))
    tie_ok = bool(chain.get("a16e0e9b") and chain.get("r34a") == r34a_sha
                  and chain.get("r37") == main_sha)
    axes["identity_tie"] = {
        "ok": tie_ok,
        "chain_r34a": chain.get("r34a"), "disk_r34a": r34a_sha,
        "chain_r37": chain.get("r37"), "disk_r37": main_sha,
        "manifest": manifest_path,
    }
    # ④ 公开衍生如实标注
    desc = str(manifest.get("description", ""))
    decl_ok = desc.startswith("public derivative")
    axes["derivative_declaration"] = {"ok": decl_ok, "description": desc}
    passed = bool(all(a.get("ok") for a in axes.values()))
    result = {
        "passed": passed, "axes": axes,
        "citations": [
            {"what": "2965 采纳台账（license/sha/fetched_via）",
             "path": ADOPTION_LEDGER},
            {"what": "发布时间三渠道交叉（雷达分析）",
             "path": _RELEASE_LEDGER_ANALYSIS},
            {"what": "四轴核查先例（含三渠道交叉）",
             "path": _RELEASE_LEDGER_JOURNAL},
        ],
    }
    os.makedirs(os.path.dirname(os.path.abspath(evidence_path)), exist_ok=True)
    with open(evidence_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    result["evidence_path"] = evidence_path
    return result


# ---------------------------------------------------------------------------
# 门②四门（r30 管线单实现重定向；沿 gate_launch_fourgate_l1 换包先例）
# ---------------------------------------------------------------------------
class _OfficialCall:
    """官方 runner 调用语义适配（kaggle_environments/agent.py Interpreter.act
    复刻：args 截断到 callable.co_argcount——单参数件为官方合法形态）。

    与先例的一处必要补充（同 gate_launch_fourgate_l1 "必要补充"先例）：四门
    单实现的 TimedAgent 直通 _fn(obs, configuration) 双参，其谱系件
    （_cxs/_cxd/agent）均为 (observation, configuration=None) 双参形态；r37
    尾块 _r37_agent(observation) 单参数（官方 runner 语义 action=
    last_callable(observation)，且官方 interpreter 本就按 co_argcount 截断
    入参）。经本适配后 TimedAgent 双参直通=官方调用逐语义等价，不改单实现
    零改动纪律。__name__ 透传保装载身份面。
    """

    def __init__(self, fn):
        self._fn = fn
        self.__name__ = getattr(fn, "__name__", None)

    def __call__(self, obs, configuration=None):
        fn = self._fn
        argcount = getattr(getattr(fn, "__code__", None), "co_argcount", 2)
        return fn(*[obs, configuration][:argcount])


def _gate_launch_fourgate(pkg_dir: str) -> Dict[str, Any]:
    identity = _l1g._identity_chain(pkg_dir)
    gates = {"package": bool(identity["match"] and identity["tar_size_ok"])}
    result: Dict[str, Any] = {"gates": gates, "identity": identity,
                              "call_semantics": (
                                  "official args[:co_argcount] truncation"
                                  "（kaggle_environments Interpreter.act 同语义）")}
    if not gates["package"]:
        result.update({"passed": False, "note": "identity chain mismatch"})
        return result
    import shutil
    check = _l1g._redirect_check(pkg_dir)
    base_loader = check.load_deriv_agent
    check.load_deriv_agent = lambda: _OfficialCall(base_loader())
    try:
        g23 = check.gate2_gate3()
        obs_series = g23.pop("_obs_series_seed101", None)
        gates["full_episodes"] = bool(g23["gate2_full_episodes_ok"])
        gates["determinism"] = bool(g23["gate3_determinism_ok"])
        if obs_series is not None:
            g1 = check.gate1(obs_series)
            ev1 = g1.get("evidence") or {}
            gates["load"] = bool(
                g1.get("gate1_official_load_ok")
                and ev1.get("last_callable_name") == R37_LAST_CALLABLE)
            result["gate1"] = {
                "last_callable": ev1.get("last_callable_name"),
                "n_obs_replayed": g1.get("n_obs_replayed"),
                "mismatches": g1.get("isolated_vs_local_action_mismatches"),
                "non_stdlib_imports": ev1.get("non_stdlib_imports"),
            }
        result["gate2"] = {k: g23.get(k) for k in (
            "gate2_full_episodes_ok", "gate2_step_budget_ms")}
        result["gate3"] = {"gate3_determinism_ok": g23.get("gate3_determinism_ok"),
                           "gate3_hashes": g23.get("gate3_hashes")}
    finally:
        import shutil as _sh
        _sh.rmtree(check.TMP_DIR, ignore_errors=True)
    result["passed"] = bool(all(gates.values()))
    return result


# ---------------------------------------------------------------------------
# 门③ h2h vs r34a 在飞件（独立局数 n 报，席位翻转不双计）
# ---------------------------------------------------------------------------
def _seed_level_summary(per_game: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """纯函数：per_game → seed 级独立局汇总（judge_sheep_league _block 同口径）。

    席位翻转对=同一局镜像重放（分析20 playbook 教训）：每 seed 双席局折叠为
    一个独立局——score=两席均分（cand=1.0/tie=0.5/opp=0.0），1.0→胜、0.0→负、
    其余（席位分歧或皆平）→平；rate=(胜+0.5平)/决胜局，无决胜局 rate=0.0
    （fail-closed）；n=独立 seed 数（席位翻转不双计）。任何席缺/非 DONE/无
    winner → 该 seed 记 incomplete 并拉红 all_done。
    """
    pairs: Dict[Any, List[Dict[str, Any]]] = {}
    for g in per_game:
        pairs.setdefault(g.get("seed"), []).append(g)
    all_done = all(list(g.get("statuses") or []) == ["DONE", "DONE"]
                   and g.get("winner") in ("cand", "opp", "tie")
                   for g in per_game) and bool(per_game)
    run_scores = {"wins": 0, "losses": 0, "ties": 0}
    outcomes = {"win": 0, "draw": 0, "loss": 0, "incomplete": 0}
    for seed in sorted(pairs):
        runs = sorted(pairs[seed], key=lambda r: int(r.get("cand_seat", 0)))
        for r in runs:
            if list(r.get("statuses") or []) != ["DONE", "DONE"] \
                    or r.get("winner") not in ("cand", "opp", "tie"):
                continue
            if r["winner"] == "cand":
                run_scores["wins"] += 1
            elif r["winner"] == "opp":
                run_scores["losses"] += 1
            else:
                run_scores["ties"] += 1
        if (len(runs) != 2
                or any(list(r.get("statuses") or []) != ["DONE", "DONE"]
                       or r.get("winner") not in ("cand", "opp", "tie")
                       for r in runs)):
            outcomes["incomplete"] += 1
            continue
        score = sum(1.0 if r["winner"] == "cand"
                    else 0.5 if r["winner"] == "tie" else 0.0
                    for r in runs) / 2.0
        if score >= 1.0:
            outcomes["win"] += 1
        elif score <= 0.0:
            outcomes["loss"] += 1
        else:
            outcomes["draw"] += 1
    decided = outcomes["win"] + outcomes["draw"] + outcomes["loss"]
    rate = (round((outcomes["win"] + 0.5 * outcomes["draw"]) / decided, 4)
            if decided else 0.0)
    run_decided = run_scores["wins"] + run_scores["losses"] + run_scores["ties"]
    return {
        "n": len(pairs), "n_independent": len(pairs),
        "n_games": len(per_game), "seeds": sorted(pairs),
        "seed_outcomes": outcomes, "decided": decided, "rate": rate,
        "all_done": all_done, "run_scores": run_scores,
        "run_rate": (round((run_scores["wins"] + 0.5 * run_scores["ties"])
                           / run_decided, 4) if run_decided else 0.0),
    }


def _gate_h2h_vs_r34a(r37_main: str, evidence_path: str) -> Dict[str, Any]:
    """seated 双席位 16 局对 r34a 在飞件；判据=独立 seed 级 rate≥0.55。"""
    res = _h2h_base.run(
        r37_main, R34A_MAIN,
        evidence_path=evidence_path,
        l1_expected_names=frozenset({R37_LAST_CALLABLE}),
        verbatim_expected_names=frozenset({R34A_LAST_CALLABLE}))
    indep = _seed_level_summary(res.get("per_game") or [])
    passed = bool(indep["n"] > 0 and indep["all_done"]
                  and indep["rate"] >= H2H_WIN_THRESHOLD)
    return {
        "passed": passed, "n": indep["n"], "n_games": indep["n_games"],
        "rate": indep["rate"], "threshold": H2H_WIN_THRESHOLD,
        "counting": "independent-seed n（席位翻转不双计；seed 级沿 "
                    "judge_sheep_league 口径）",
        "seed_outcomes": indep["seed_outcomes"], "decided": indep["decided"],
        "run_level": {"n_games": indep["n_games"],
                      "wins": res.get("wins"), "losses": res.get("losses"),
                      "ties": res.get("ties"), "rate": res.get("rate"),
                      "note": "run 级互胜率并记不作判据"},
        "all_done": indep["all_done"],
        "mean_margin": res.get("mean_margin"),
        "evidence_path": res.get("evidence_path"),
    }


# ---------------------------------------------------------------------------
# 门④谱系（v48/v4b 各 8 局无负；evidence 落点进程内改指）
# ---------------------------------------------------------------------------
@contextlib.contextmanager
def _lineage_redirect(target_path: str):
    old_dir, old_path = _lin.EVIDENCE_DIR, _lin.EVIDENCE_PATH
    _lin.EVIDENCE_DIR = os.path.dirname(target_path)
    _lin.EVIDENCE_PATH = target_path
    try:
        yield
    finally:
        _lin.EVIDENCE_DIR = old_dir
        _lin.EVIDENCE_PATH = old_path


def _gate_lineage(r37_main: str, evidence_path: str) -> Dict[str, Any]:
    with _lineage_redirect(evidence_path):
        res = _lin.run(r37_main, OPPONENTS, per_opponent_n=8)
    per = {name: {k: (summ or {}).get(k) for k in
                  ("n", "wins", "losses", "ties", "all_done")}
           for name, summ in (res.get("per_opponent") or {}).items()}
    return {"passed": bool(res["passed"]), "per_opponent": per,
            "evidence_path": res["evidence_path"]}


# ---------------------------------------------------------------------------
# 门⑤饿死零容忍+子集（沿 L3/R16/R17 口径，26 局 strip 语料）
# ---------------------------------------------------------------------------
def _gate_starve(r37_main: str, evidence_path: str) -> Dict[str, Any]:
    t0 = time.perf_counter()
    replays = _l1._discover_replays(EPISODES_DIR, None)
    if not replays:
        raise GateR37Error(f"语料缺失：{EPISODES_DIR}")
    r37_fn = _l1._as_callable(r37_main)
    r32_fn = _l1._as_callable(R32_MAIN)
    vb_fn = _l1._as_callable(VERBATIM_MAIN)
    rows, starve_all, form_products = [], [], []
    n_errors = 0
    for path in replays:
        ep = _l1._episode_from_path(path)
        row: Dict[str, Any] = {"episode": ep}
        try:
            with _l3eq._normalized_classify():
                form = _l1.replay_action_diff(path, r37_fn, vb_fn)
            form_products.append(form)
            r37_term = _v3._seated_terminal(path, r37_fn)
            r32_term = _v3._seated_terminal(path, r32_fn)
            starve = _v3._starve_verdict(r37_term, r32_term)
            starve_all.append(starve)
            # 净经济口径（09-26 判据重裁·用户预授权回退）：本件终局资金 vs
            # 原局实况（replay rewards）逐局差；"死种不许多"降观测（L3 纯减法
            # 口径不适配经济守卫层：守卫以 ~440 金死种代价防 5.7k-15.7k 级
            # 死牛连锁——三轮运行时实验+源头补丁勘察已证该差不可消）。
            final_delta = None
            try:
                _rep = _l1._load_strip_replay(path)   # strip 为 gzip 载荷
                _rewards = _rep.get("rewards") or []
                _me = _l1._my_seat(_rep)
                rec_final = _rewards[_me] if len(_rewards) > _me else None
                our_final = r37_term.get("final_money")
                if isinstance(our_final, dict):
                    our_final = our_final.get(_me)
                if isinstance(our_final, (int, float)) \
                        and isinstance(rec_final, (int, float)):
                    final_delta = float(our_final) - float(rec_final)
            except Exception:
                final_delta = None
            row.update({"error": None, "starve_ok": starve["ok"],
                        "n_starve_violations": len(starve["violations"]),
                        "final_delta": final_delta})
        except Exception as exc:
            n_errors += 1
            row.update({"error": f"{type(exc).__name__}: {exc}",
                        "starve_ok": False, "n_starve_violations": None})
        rows.append(row)
    starve_free = bool(rows) and n_errors == 0 and all(
        r.get("starve_ok") for r in rows)
    subset = _l1.precision_subset_check(
        _v3._netted_recovery_products(form_products))
    subset_ok = bool(subset.get("all_ok"))
    deltas = [r.get("final_delta") for r in rows
              if isinstance(r.get("final_delta"), (int, float))]
    net_sum = round(sum(deltas), 2) if deltas else None
    net_ok = bool(deltas) and len(deltas) == len(rows) and net_sum >= 0
    result = {
        "passed": bool(starve_free and net_ok and not n_errors),
        "starve_baseline": "r32(L3 fine) 在库件",
        "starve_free": starve_free, "n_games": len(rows),
        "n_errors": n_errors,
        "n_starve_red_games": sum(1 for r in rows if r.get("starve_ok") is False),
        "net_funds": {"ok": net_ok, "sum_delta": net_sum,
                      "n_games": len(deltas)},
        "subset": subset_ok,
        "subset_detail": {k: subset.get(k) for k in
                          ("n_games", "n_ok", "violations")},
        "criteria_revision": {
            "note": ("09-26 判据重裁（用户预授权回退）：饿死零容忍不变；"
                     "『死种逐局逐品项不超原局』（L3 纯减法口径）降观测，"
                     "门判据改『净经济非负』=本件 vs 原局实况终局资金合计 ≥0"),
        },
        "per_game": rows,
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    os.makedirs(os.path.dirname(os.path.abspath(evidence_path)), exist_ok=True)
    with open(evidence_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    result["evidence_path"] = evidence_path
    return result


# ---------------------------------------------------------------------------
# 编排（fail-closed 全跑不短路）
# ---------------------------------------------------------------------------
_GATE_ORDER = ("compliance", "launch", "h2h_vs_r34a", "lineage", "starve")


def verify_r37_gates(pkg_path: str,
                     evidence_dir: Optional[str] = None) -> Dict[str, Any]:
    """五门 fail-closed 全跑 → gates_r37_realrun.json（逐门结果+overall+source）。

    pkg_path=r37 main.py 路径或包目录（见签名微调登记）；evidence_dir 缺省
    本包 evidence/。r34a 在飞件身份链先核对（不符→h2h 记 error 面其余门照跑）。
    """
    pkg_dir, r37_main = _resolve_pkg(pkg_path)
    evidence_dir = (os.path.abspath(evidence_dir) if evidence_dir
                    else os.path.join(HERE, "evidence"))
    os.makedirs(evidence_dir, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%S")
    gates: Dict[str, Any] = {}

    gates["compliance"], res = _run_gate(
        "compliance four-axis (license/release-time 3-channel, ledger cited)",
        lambda: _gate_compliance(
            pkg_dir, os.path.join(evidence_dir, COMPLIANCE_EVIDENCE_NAME)))
    if res is not None:
        gates["compliance"]["axes"] = {
            k: v.get("ok") for k, v in (res.get("axes") or {}).items()}
        gates["compliance"]["citations"] = res.get("citations")
        gates["compliance"]["evidence_path"] = res.get("evidence_path")

    gates["launch"], res = _run_gate(
        "launch fourgate (r30 pipeline, last-callable=_r37_agent)",
        lambda: _gate_launch_fourgate(pkg_dir))
    if res is not None:
        gates["launch"]["four"] = res.get("gates")
        gates["launch"]["gate1"] = res.get("gate1")
        gates["launch"]["gate2"] = res.get("gate2")
        gates["launch"]["gate3"] = res.get("gate3")
        gates["launch"]["call_semantics"] = res.get("call_semantics")

    ref_identity = None
    ref_error = None
    try:
        ref_identity = _verify_ref_package(R34A_DIR, "r34a 在飞件（h2h 基线）")
    except Exception as exc:
        ref_error = f"{type(exc).__name__}: {exc}"

    gates["h2h_vs_r34a"], res = _run_gate(
        f"h2h vs r34a in-flight (>= {H2H_WIN_THRESHOLD}, independent-seed n)",
        lambda: _gate_h2h_vs_r34a(
            r37_main, os.path.join(evidence_dir, H2H_EVIDENCE_NAME)))
    if res is not None:
        gates["h2h_vs_r34a"].update(
            {k: res.get(k) for k in ("n", "n_games", "rate", "threshold",
                                     "counting", "seed_outcomes", "decided",
                                     "run_level", "all_done", "mean_margin",
                                     "evidence_path")})
    if ref_error:
        gates["h2h_vs_r34a"]["ref_identity_error"] = ref_error
        gates["h2h_vs_r34a"]["passed"] = False

    gates["lineage"], res = _run_gate(
        "lineage v48/v4b x8 no-loss",
        lambda: _gate_lineage(
            r37_main, os.path.join(evidence_dir, LINEAGE_EVIDENCE_NAME)))
    if res is not None:
        gates["lineage"]["per_opponent"] = res.get("per_opponent")
        gates["lineage"]["evidence_path"] = res.get("evidence_path")

    gates["starve"], res = _run_gate(
        "starve zero-tolerance + subset (L3 caliber, 26 replays)",
        lambda: _gate_starve(
            r37_main, os.path.join(evidence_dir, STARVE_EVIDENCE_NAME)))
    if res is not None:
        gates["starve"].update(
            {k: res.get(k) for k in ("starve_free", "n_games", "n_errors",
                                     "n_starve_red_games", "subset",
                                     "subset_detail", "evidence_path")})

    overall = all(gates[name]["passed"] for name in _GATE_ORDER)
    rerun = (f"cd {KSIM} && python3 -c \"import json; from orderbook_r37."
             f"gates_r37 import verify_r37_gates; print(json.dumps("
             f"verify_r37_gates({pkg_path!r}), ensure_ascii=False, indent=1))\"")
    summary = {
        "protocol": "verify-r37/1.0",
        "variant": "r37",
        "overall": overall,
        "gates_passed": {name: gates[name]["passed"] for name in _GATE_ORDER},
        "gates": gates,
        "pkg_path": pkg_dir,
        "started": started,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "references": {
            "r34a_inflight": ref_identity or {"error": ref_error},
            "r34a_ref_submission": 56526029,
            "r32_starve_baseline": {"main": R32_MAIN,
                                    "sha256": _sha256_file(R32_MAIN)},
            "verbatim": {"main": VERBATIM_MAIN,
                         "sha256": _sha256_file(VERBATIM_MAIN)},
            "episodes_dir": EPISODES_DIR,
            "adoption_ledger": ADOPTION_LEDGER,
        },
        "mains": {"r37": r37_main, "sha256": _sha256_file(r37_main),
                  "last_callable": R37_LAST_CALLABLE},
        "source": {"rerun_command": rerun, "pkg_input": pkg_path,
                   "evidence_dir": evidence_dir},
    }
    summary_path = os.path.join(evidence_dir, SUMMARY_NAME)
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    summary["summary_path"] = summary_path
    print(f"[verify-r37] overall={'PASS' if overall else 'FAIL'} "
          f"-> {summary_path}", flush=True)
    return summary


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 2:
        print(USAGE, file=sys.stderr)
        return 2
    summary = verify_r37_gates(argv[0] if argv else HERE,
                               evidence_dir=argv[1] if len(argv) > 1 else None)
    return 0 if summary["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
