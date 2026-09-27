# -*- coding: utf-8 -*-
"""run_r40_iteration（R23 L0）：编排。

责任契约（fn_docs/hybrid/responsibility.md【R23 增补】）：
build_r40 产 r40 件 → judge_r23 判决（败局 12 局定向重演+联赛 300-500+分段
统计+仿真器对照）→ 分项+总判全绿才 verify_r40_gates 五门 → 交发射（standing
台账）；任一红→收档（预绑定）。evidence+台账。

编排口径（实现与测试同钉）：
- 段序=构建段→判决段→门禁段→发射/收档段。
- 判决=judge_r23 六判据（evidence overall.criteria+overall.pass）分项+总判
  全绿才进门禁；缺判据或任一红即判负，fail-closed，不许改判。**gates 段语义
  （本实现选定，B24 先例同款）：判红不进门禁**——gates 记 {"skipped": True,
  "overall": False} 不执行五门（留证从简，判决 evidence 已是判负主证）；判正
  进门禁 verify_r40_gates fail-closed 全跑（门内全跑不短路归 gates_r40）。
- verdict（R23 出口预绑定，如实生成不许改判）：六判据+五门全绿→
  {"verdict": "POSITIVE", "launch_ready": true}+发射台账 launch_ledger.json
  （沿 R37 standing 代执行惯例）；任一红（判负，或门禁任一门红）→
  {"verdict": "NEGATIVE", "launch_ready": false, "reason": …}+收档台账
  archive_ledger.json（archive_note="判负收档留赛后资产，不建发射版"，不建
  发射版）；Error→fail-closed：run_summary 留痕后上抛，不改判不重试。
- evidence 落 <out_dir>/evidence/：run_r40_build_realrun.json（构建审计
  wrapper）/run_r40_judge_realrun.json（判决 evidence 原件）/gates_r40_realrun
  .json（verify_r40_gates 自写，evidence_dir 重指本目录）+台账（launch_
  ledger.json 或 archive_ledger.json）+run_summary.json（阶段态记录，含
  Error 留痕）。命名留档：build_r40_realrun.json/retape_lots_realrun.json/
  route_library_realrun.json/sim_bridge_realrun.json 为 B29-B31 批证据件
  （test_build/retape/route_library/sim_bridge 历史台账），本编排不覆写；
  run_summary.json/archive_ledger.json/launch_ledger.json 为收口件。

【签名微调登记（批间）】run_r40_iteration(out_dir=None, corpus=None,
bench=None)：
- out_dir：证据/台账落点根与构建产物根（缺省本包 orderbook_r40/，build 产物
  落 <out_dir>/build/）；测试以 tmp 覆盖防覆写真台账。
- corpus：判决定向重演语料（缺省 DEFAULT_CORPUS=build_r40.LOSS_IDS 败局
  12 局 id 单同源原样；传入即透传 judge_r23，形态沿 judge 惯例=局号或 replay
  路径）。
- bench：判决副证配置（缺省 None=judge_r23 验收档：联赛 300-500+榜前强手
  样本+仿真器对照 ≥30 局）。
首参与返回主键不变（{build, judgment, gates, verdict}）。
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

from orderbook_r40 import build_r40 as _b40            # noqa: E402
from orderbook_r40 import gates_r40 as _g40            # noqa: E402
from orderbook_r40 import judge_r23 as _j23            # noqa: E402

EVIDENCE_DIR = os.path.join(HERE, "evidence")

R37_MAIN = os.path.join(KSIM, "orderbook_r37", "build", "main.py")
# 判决定向重演缺省语料=败局 12 局 id 单（build_r40.LOSS_IDS 同源，分析24 败局
# 谱系；条目形态沿 judge 惯例=局号）
DEFAULT_CORPUS = tuple(_b40.LOSS_IDS)
EVIDENCE_BUILD = "run_r40_build_realrun.json"
EVIDENCE_JUDGMENT = "run_r40_judge_realrun.json"
EVIDENCE_GATES = _g40.SUMMARY_NAME          # gates_r40_realrun.json（自写）
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
    """judge_r23 evidence 总判据：六判据全绿（criteria 全 True 且 overall.pass）。

    缺判据/缺 overall 即 False（fail-closed，不许改判）。
    """
    overall = (ev or {}).get("overall") or {}
    crit = overall.get("criteria") or {}
    return bool(overall.get("pass")) and bool(crit) and all(
        bool(v) for v in crit.values())


def _artifacts(build: Dict[str, Any]) -> Dict[str, Any]:
    """台账件身份（launch/archive 同构；manifest 描述文案+sha 链+三 sha 自证）。"""
    manifest = build.get("manifest") or {}
    return {
        "main_path": build.get("main_path"),
        "main_sha256": build.get("main_sha256"),
        "tar_sha256": build.get("tar_sha256"),
        "block_sha": build.get("block_sha"),
        "library_sha256": build.get("library_sha256"),
        "sell_lots_change_sha256": build.get("sell_lots_change_sha256"),
        "description": manifest.get("description"),
        "base_sha_chain": manifest.get("base_sha_chain"),
    }


def _standing_launch(build: Dict[str, Any], evidence_dir: str) -> Dict[str, Any]:
    """发射段：standing 代执行+台账留痕（launch_ledger.json，沿 R37 惯例）。"""
    record = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol": "run-r40-standing-launch/1.0",
        "standing": ("standing 授权代执行（主会话沿 SOP 执行实际提交："
                     "每日≤5/候选≤2/Error 即停）"),
        "ref": "PENDING",
        "artifacts": _artifacts(build),
        "condition": "六判据+五门全绿交发射（R23 发射条款）",
        "judgments": ["judge_r23"],
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
        "protocol": "run-r40-archive/1.0",
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


def run_r40_iteration(out_dir: Optional[str] = None,
                      corpus: Optional[Sequence[Any]] = None,
                      bench: Optional[Dict[str, Any]] = None,
                      ) -> Dict[str, Any]:
    """编排：构建→判决（六判据分项+总判）→（全绿才）门禁→发射/收档裁决。

    签名意图：输入: 无（CLI） / 输出: {build, judgment, gates, verdict} /
    错误: fail-closed（任一红即判负收档不建发射版；Error 落 run_summary 后
    上抛）。
    可选参见签名微调登记（out_dir/corpus/bench）。
    """
    t0 = time.perf_counter()
    root = os.path.abspath(out_dir or HERE)
    evidence_dir = os.path.join(root, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    stage: Dict[str, Any] = {"build": None, "judgment": None, "gates": None}
    try:
        # ---- ① build_r40 产 r40 件（库内建+三 sha 自证，fail-closed） ----
        build = _b40.build_r40(R37_MAIN, out_dir=os.path.join(root, "build"))
        build_path = _write_json(
            os.path.join(evidence_dir, EVIDENCE_BUILD), {
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "generated_by": "run_r40_iteration",
                "r37_main_path": R37_MAIN,
                "build": build,
            })
        stage["build"] = {
            "main_path": build.get("main_path"),
            "main_sha256": build.get("main_sha256"),
            "tar_sha256": build.get("tar_sha256"),
            "block_sha": build.get("block_sha"),
            "library_sha256": build.get("library_sha256"),
            "sell_lots_change_sha256": build.get("sell_lots_change_sha256"),
            "evidence_path": build_path,
        }
        main_path = build.get("main_path")
        if not main_path:
            raise RuntimeError(f"build_r40 未返回 main_path：{build!r}")

        # ---- ② judge_r23 判决（六判据：败局重演+联赛+分段+仿真对照） ----
        judgment = _j23.judge_r23(
            main_path,
            list(corpus if corpus is not None else DEFAULT_CORPUS),
            bench)
        jud_path = _write_json(
            os.path.join(evidence_dir, EVIDENCE_JUDGMENT), judgment)
        crit = ((judgment or {}).get("overall") or {}).get("criteria") or {}
        judgment_green = _judgment_flag(judgment)
        red_criteria = [k for k, v in crit.items() if not v]
        stage["judgment"] = {
            "pass": judgment_green,
            "n_criteria": len(crit),
            "criteria": crit,
            "red": red_criteria,
            "evidence_path": jud_path,
        }

        # ---- ③ 门禁（分项+总判全绿才进；判红不进门禁记 skipped——B24 语义） --
        if judgment_green:
            gates = _g40.verify_r40_gates(main_path, evidence_dir=evidence_dir)
            gates_green = bool(gates.get("overall"))
            stage["gates"] = {
                "overall": gates_green,
                "gates_passed": gates.get("gates_passed"),
                "summary_path": gates.get("summary_path"),
            }
        else:
            gates = {"skipped": True, "overall": False,
                     "reason": "六判据红→不进门禁（全绿才验五门）"}
            stage["gates"] = {"skipped": True, "overall": False}
            gates_green = False

        # ---- ④ 出口裁决（R23 出口预绑定：全绿交发射/任一红收档） -------
        launch_ready = bool(judgment_green and gates_green)
        if launch_ready:
            reason = None
        elif not judgment_green:
            reason = ("六判据红：" + ", ".join(red_criteria)) if red_criteria \
                else "六判据红（缺判据/overall.pass 非 True）"
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
            "protocol": "run-r40/1.0",
            "stage": stage,
            "verdict": verdict,
            "wall_s": round(time.perf_counter() - t0, 1),
        }
        path = _write_json(os.path.join(evidence_dir, EVIDENCE_RUN), summary)
        return {
            "build": build,
            "judgment": judgment,
            "gates": gates,
            "verdict": {**verdict, "run_summary_path": path},
        }
    except Exception as exc:
        fail = {"protocol": "run-r40/1.0", "stage": stage,
                "verdict": {"launch_ready": False, "verdict": "ERROR",
                            "reason": f"{type(exc).__name__}: {exc}",
                            "judgment_green": False, "gates_green": False,
                            "standing_launch": None, "archive_ledger": None},
                "error": f"{type(exc).__name__}: {exc}",
                "wall_s": round(time.perf_counter() - t0, 1)}
        _write_json(os.path.join(evidence_dir, EVIDENCE_RUN), fail)
        raise
