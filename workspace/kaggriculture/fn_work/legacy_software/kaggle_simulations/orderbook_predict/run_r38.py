# -*- coding: utf-8 -*-
"""run_r38_iteration（R21 L0）：编排。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
build_sellflow_library 建库 → build_r38 产 r38 件 → judge_predict_replay
判决（26 败局[晚崩 15 局重点]+10 胜局对照+闭环副证）→ 判正才
verify_r38_gates 五门 → 全绿交发射（standing 台账）；判负→收档不建发射版。
evidence 四件+台账。

编排口径（实现与测试同钉）：
- 段序=建库段→构建段→判决段→门禁段→发射/收档段。判正=judge 判据全绿
  （overall.criteria 全 True 且 overall.pass；缺判据或任一红即判负，
  fail-closed）；判正才进门禁（判负→gates 记 skipped 不进门禁）；门禁段
  verify_r38_gates fail-closed 全跑（门内全跑不短路归 gates_r38）。
- 建库/构建链对账：build_r38 自建同源库（/tmp/r33audit 契约钉），其返回
  library_sha256 与本段建库审计 sha256_of_library 不符即 RuntimeError
  （fail-closed，落 run_summary 后上抛）。
- verdict（R21 出口预绑定，如实生成不许改判）：判据全绿（判正∧五门全绿）→
  {"verdict": "POSITIVE", "launch_ready": true}+发射台账 launch_ledger.json
  （沿 R37 standing 代执行惯例）；任一判据红（判负，或门禁任一门红）→
  {"verdict": "NEGATIVE", "launch_ready": false, "reason": …}+收档台账
  archive_ledger.json（archive_note="判负收档留赛后资产，不建发射版"，
  不建发射版）；Error→fail-closed：run_summary 留痕后上抛，不改判不重试。
- evidence 四件落 <out_dir>/evidence/：sellflow_library_realrun.json（建库
  审计，真跑件形态）/build_r38_realrun.json（构建审计）/judge_predict_realrun
  .json（判决 evidence 原件）/gates_r38_realrun.json（verify_r38_gates 自写，
  evidence_dir 重指本目录）+台账（launch_ledger.json 或 archive_ledger.json）
  +run_summary.json（阶段态记录，含 Error 留痕）。

【签名微调登记（批间）】run_r38_iteration(out_dir=None, n_judgment=None,
corpus=None, bench=None)：
- out_dir：证据/台账落点根与构建产物根（缺省本包 orderbook_predict/，build
  产物落 <out_dir>/build/）；测试以 tmp 覆盖防覆写真台账。
- n_judgment：判决闭环副证主对局数（缺省 None=judge 验收档 16 局；传入即写
  bench["n_games_main"]，与 bench 同给时覆盖之；≥2 偶数校验归
  judge_predict_replay，非法即 ValueError fail-closed）。
- corpus：判决语料局单（缺省固定 26 败局+10 对照，R21 判决同单——
  analysis20_rows 的 r34a L 20 局+/tmp/kagr22 6 灾难局（replay 路径钉 a22
  缓存）+a22 对照 10 局；条目=局号或 replay 路径，重叠条目按唯一局去重计
  归 judge_predict_replay）。
- bench：判决闭环副证配置（缺省 None=judge 验收档：vs r37 主对 16 局+vs
  r34a 辅对 8 局，seed 41000/42000 起）。
首参与返回主键不变（{library, build, judgment, gates, verdict}）。
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict, Optional, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

from orderbook_predict import build_r38 as _b38         # noqa: E402
from orderbook_predict import gates_r38 as _g38         # noqa: E402
from orderbook_predict import judge_predict as _jp      # noqa: E402
from orderbook_predict import sellflow as _sf           # noqa: E402

EVIDENCE_DIR = os.path.join(HERE, "evidence")

R37_MAIN = os.path.join(KSIM, "orderbook_r37", "build", "main.py")
SELLFLOW_REPLAY_DIR = "/tmp/r33audit"   # 契约钉：与 build_r38 建库同源
DEFAULT_CORPUS = (
    # 26 败局 = analysis20_rows 的 r34a L 20 局（episode id）
    "112938600", "112949172", "112951544", "112958934", "112964927",
    "112967289", "112968467", "112976582", "112980045", "112980852",
    "112988237", "112990619", "112990764", "112998363", "112998777",
    "113002280", "113084351", "113094793", "113099386", "113105969",
    # + /tmp/kagr22 的 6 灾难局（replay 路径钉 a22 缓存；与上重叠按唯一局去重）
    "/tmp/kagr22/episode-112938600-replay.json",
    "/tmp/kagr22/episode-112968467-replay.json",
    "/tmp/kagr22/episode-112976582-replay.json",
    "/tmp/kagr22/episode-113002280-replay.json",
    "/tmp/kagr22/episode-113094793-replay.json",
    "/tmp/kagr22/episode-113099386-replay.json",
    # 10 对照 = /tmp/kagr22 对照集（episode id）
    "112937338", "112943297", "112969611", "112971928", "112973096",
    "112983518", "112984665", "112986874", "112992971", "113064702",
)
EVIDENCE_LIBRARY = "sellflow_library_realrun.json"
EVIDENCE_BUILD = "build_r38_realrun.json"
EVIDENCE_JUDGMENT = "judge_predict_realrun.json"
EVIDENCE_GATES = _g38.SUMMARY_NAME          # gates_r38_realrun.json（自写）
EVIDENCE_LAUNCH = "launch_ledger.json"
EVIDENCE_ARCHIVE = "archive_ledger.json"
EVIDENCE_RUN = "run_summary.json"


def _write_json(path: str, payload: Any) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return path


def _judgment_flag(ev: Any) -> bool:
    """judge evidence 总判据：判据全绿（criteria 全 True 且 overall.pass）。

    缺判据/缺 overall 即 False（fail-closed，不许改判）。
    """
    overall = (ev or {}).get("overall") or {}
    crit = overall.get("criteria") or {}
    return bool(overall.get("pass")) and bool(crit) and all(
        bool(v) for v in crit.values())


def _artifacts(build: Dict[str, Any]) -> Dict[str, Any]:
    """台账件身份（launch/archive 同构；manifest 描述文案+sha 链）。"""
    manifest = build.get("manifest") or {}
    return {
        "main_path": build.get("main_path"),
        "main_sha256": build.get("main_sha256"),
        "tar_sha256": build.get("tar_sha256"),
        "description": manifest.get("description"),
        "base_sha_chain": manifest.get("base_sha_chain"),
    }


def _standing_launch(build: Dict[str, Any], evidence_dir: str) -> Dict[str, Any]:
    """发射段：standing 代执行+台账留痕（launch_ledger.json，沿 R37 惯例）。"""
    record = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol": "run-r38-standing-launch/1.0",
        "standing": ("standing 授权代执行（主会话沿 SOP 执行实际提交："
                     "每日≤5/候选≤2/Error 即停）"),
        "ref": "PENDING",
        "artifacts": _artifacts(build),
        "condition": "判决+门禁全绿交发射（R21 发射条款）",
        "judgments": ["judge_predict_replay"],
        "gates_ledger": os.path.join(evidence_dir, EVIDENCE_GATES),
    }
    record["ledger_path"] = _write_json(
        os.path.join(evidence_dir, EVIDENCE_LAUNCH), record)
    return record


def _archive_ledger(build: Dict[str, Any], reason: str, stage: Dict[str, Any],
                    evidence_dir: str) -> Dict[str, Any]:
    """收档段：判负收档留赛后资产，不建发射版（archive_ledger.json）。"""
    gates_stage = stage.get("gates") or {}
    record = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol": "run-r38-archive/1.0",
        "archive_note": "判负收档留赛后资产，不建发射版",
        "verdict": "NEGATIVE",
        "launch_ready": False,
        "reason": reason,
        "artifacts": _artifacts(build),
        "judgment": stage.get("judgment"),
        "gates": gates_stage,
        "gates_ledger": (None if gates_stage.get("skipped")
                         else os.path.join(evidence_dir, EVIDENCE_GATES)),
    }
    record["ledger_path"] = _write_json(
        os.path.join(evidence_dir, EVIDENCE_ARCHIVE), record)
    return record


def run_r38_iteration(out_dir: Optional[str] = None,
                      n_judgment: Optional[int] = None,
                      corpus: Optional[Sequence[str]] = None,
                      bench: Optional[Dict[str, Any]] = None,
                      ) -> Dict[str, Any]:
    """编排：建库→构建→判决→（判正才）门禁→发射/收档裁决；evidence 四件+台账。

    签名意图：输入: 无（CLI） / 输出: {library, build, judgment, gates, verdict} /
    错误: fail-closed（任一判据红即判负收档不建发射版；Error 落 run_summary 后
    上抛）。
    可选参见签名微调登记（out_dir/n_judgment/corpus/bench）。
    """
    t0 = time.perf_counter()
    root = os.path.abspath(out_dir or HERE)
    evidence_dir = os.path.join(root, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    stage: Dict[str, Any] = {"library": None, "build": None,
                             "judgment": None, "gates": None}
    try:
        # ---- ① build_sellflow_library 建库（真库语料，契约钉） ----------
        built = _sf.build_sellflow_library(SELLFLOW_REPLAY_DIR)
        audit = built.get("build_audit") or {}
        lib_ev = {"n_keys": len((built.get("library") or {}).get("keys") or {}),
                  **audit}
        lib_path = _write_json(
            os.path.join(evidence_dir, EVIDENCE_LIBRARY), lib_ev)
        stage["library"] = {
            "n_files": audit.get("n_files"),
            "n_keys": lib_ev["n_keys"],
            "n_used": audit.get("n_used"),
            "sha256_of_library": audit.get("sha256_of_library"),
            "evidence_path": lib_path,
        }

        # ---- ② build_r38 产 r38 件（库随块内嵌，链对账 fail-closed） ----
        build = _b38.build_r38(R37_MAIN, out_dir=os.path.join(root, "build"))
        build_path = _write_json(
            os.path.join(evidence_dir, EVIDENCE_BUILD), {
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "generated_by": "run_r38_iteration",
                "r37_main_path": R37_MAIN,
                "build": build,
            })
        stage["build"] = {
            "main_path": build.get("main_path"),
            "main_sha256": build.get("main_sha256"),
            "tar_sha256": build.get("tar_sha256"),
            "block_sha": build.get("block_sha"),
            "library_sha256": build.get("library_sha256"),
            "evidence_path": build_path,
        }
        main_path = build.get("main_path")
        if not main_path:
            raise RuntimeError(f"build_r38 未返回 main_path：{build!r}")
        if build.get("library_sha256") != audit.get("sha256_of_library"):
            raise RuntimeError(
                "库 sha 对账红：build=%s 建库审计=%s"
                % (build.get("library_sha256"), audit.get("sha256_of_library")))

        # ---- ③ judge_predict_replay 判决（26 败局+10 对照+闭环副证） ----
        judge_bench: Any = bench
        if n_judgment is not None:
            judge_bench = dict(bench or {})
            judge_bench["n_games_main"] = n_judgment
        judgment = _jp.judge_predict_replay(
            main_path,
            list(corpus if corpus is not None else DEFAULT_CORPUS),
            judge_bench)
        jud_path = _write_json(
            os.path.join(evidence_dir, EVIDENCE_JUDGMENT), judgment)
        crit = ((judgment or {}).get("overall") or {}).get("criteria") or {}
        judgment_green = _judgment_flag(judgment)
        red_criteria = [k for k, v in crit.items() if not v]
        stage["judgment"] = {
            "pass": judgment_green,
            "criteria": crit,
            "red": red_criteria,
            "evidence_path": jud_path,
        }

        # ---- ④ 门禁（判正才进门；fail-closed 全跑不短路） ---------------
        if judgment_green:
            gates = _g38.verify_r38_gates(main_path, evidence_dir=evidence_dir)
            gates_green = bool(gates.get("overall"))
            stage["gates"] = {
                "overall": gates_green,
                "gates_passed": gates.get("gates_passed"),
                "summary_path": gates.get("summary_path"),
            }
        else:
            gates = {"skipped": True, "overall": False,
                     "reason": "判负→不进门禁（判正才验五门）"}
            stage["gates"] = {"skipped": True, "overall": False}
            gates_green = False

        # ---- ⑤ 出口裁决（R21 出口预绑定：全绿交发射/任一红收档） -------
        launch_ready = bool(judgment_green and gates_green)
        if launch_ready:
            reason = None
        elif not judgment_green:
            reason = ("判决判据红：" + ", ".join(red_criteria)) if red_criteria \
                else "判决判据红（缺判据/overall.pass 非 True）"
        else:
            red_gates = [k for k, v in (gates.get("gates_passed") or {}).items()
                         if not v]
            reason = ("门禁红：" + ", ".join(red_gates)) if red_gates \
                else "门禁红（overall 非 True）"
        verdict: Dict[str, Any] = {
            "verdict": "POSITIVE" if launch_ready else "NEGATIVE",
            "launch_ready": launch_ready,
            "reason": reason,
            "judgment_green": judgment_green,
            "gates_green": gates_green,
            "standing_launch": None,
            "archive_ledger": None,
        }
        if launch_ready:
            verdict["standing_launch"] = _standing_launch(build, evidence_dir)
        else:
            verdict["archive_ledger"] = _archive_ledger(
                build, reason, stage, evidence_dir)

        summary = {
            "protocol": "run-r38/1.0",
            "stage": stage,
            "verdict": verdict,
            "wall_s": round(time.perf_counter() - t0, 1),
        }
        path = _write_json(os.path.join(evidence_dir, EVIDENCE_RUN), summary)
        return {
            "library": built,
            "build": build,
            "judgment": judgment,
            "gates": gates,
            "verdict": {**verdict, "run_summary_path": path},
        }
    except Exception as exc:
        fail = {"protocol": "run-r38/1.0", "stage": stage,
                "verdict": {"launch_ready": False, "verdict": "ERROR",
                            "reason": f"{type(exc).__name__}: {exc}",
                            "judgment_green": False, "gates_green": False,
                            "standing_launch": None, "archive_ledger": None},
                "error": f"{type(exc).__name__}: {exc}",
                "wall_s": round(time.perf_counter() - t0, 1)}
        _write_json(os.path.join(evidence_dir, EVIDENCE_RUN), fail)
        raise
