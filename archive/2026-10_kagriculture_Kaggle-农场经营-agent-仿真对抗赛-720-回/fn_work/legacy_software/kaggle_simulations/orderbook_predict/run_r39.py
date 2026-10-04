# -*- coding: utf-8 -*-
"""run_r39_iteration（R22 L0）：编排（PREDICT v2）。

责任契约（fn_docs/hybrid/responsibility.md【R22 增补】）：
build_r39 产 r39 件 → judge_predict_replay[改造] 判决（26 败局+10 对照+
闭环副证 vs r37+反制模拟臂）→ 六判据全绿才 verify_r39_gates 五门 → 全绿
交发射（standing 台账）；任一红→收档（沿 R21 预绑定）。evidence+台账。

编排口径（实现与测试同钉）：
- 段序=构建段→判决段→门禁段→发射/收档段（r39 无独立建库段：v2 流库由
  build_r39 内建并三 sha 自证，链对账归 build_r39 fail-closed 自检）。
- 判决=judge_predict_replay v2 六判据（control_not_flipped/late_flip_ge_third
  /h2h_vs_r37_ge_055/action_throttle/counter_arm_not_worse/
  realized_px_not_down）全绿才进门禁；缺判据或任一红即判负，fail-closed，
  不许改判。**gates 段语义（本实现选定，B24 先例同款）：判红不进门禁**——
  gates 记 {"skipped": True, "overall": False} 不执行五门（留证从简，判决
  evidence 已是判负主证）；判正进门禁 verify_r39_gates fail-closed 全跑
  （门内全跑不短路归 gates_r39）。
- verdict（R22 出口预绑定，如实生成不许改判）：六判据全绿∧五门全绿→
  {"verdict": "POSITIVE", "launch_ready": true}+发射台账 launch_ledger.json
  （沿 R37 standing 代执行惯例）；任一判据红（判负，或门禁任一门红）→
  {"verdict": "NEGATIVE", "launch_ready": false, "reason": …}+收档台账
  archive_ledger.json（archive_note="判负收档留赛后资产，不建发射版"，
  不建发射版）；Error→fail-closed：run_summary 留痕后上抛，不改判不重试。
- evidence 落 <out_dir>/evidence/：run_r39_build_realrun.json（构建审计
  wrapper）/run_r39_judge_realrun.json（判决 evidence 原件）/gates_r39_realrun
  .json（verify_r39_gates 自写，evidence_dir 重指本目录）+台账（launch_
  ledger.json 或 archive_ledger.json）+run_summary.json（阶段态记录，含
  Error 留痕）。命名留档：build_r39_realrun.json/judge_predict_v2*_realrun
  .json 为 B26/B27 批证据件（test_build_r39/judge 历史台账），本编排不覆写；
  run_summary.json/archive_ledger.json 为收口件（覆写 r38 旧档=正式收档）。

【签名微调登记（批间）】run_r39_iteration(out_dir=None, n_judgment=None,
corpus=None, bench=None)：
- out_dir：证据/台账落点根与构建产物根（缺省本包 orderbook_predict/，build
  产物落 <out_dir>/build/）；测试以 tmp 覆盖防覆写真台账。
- n_judgment：判决闭环副证主对局数（缺省 None=judge 验收档 16 局；传入即写
  bench["n_games_main"]，与 bench 同给时覆盖之；≥2 偶数校验归
  judge_predict_replay，非法即 ValueError fail-closed）。
- corpus：判决语料局单（缺省固定 26 败局+10 对照，R22 判决同单——
  analysis20_rows 的 r34a L 20 局+/tmp/kagr22 6 灾难局（replay 路径钉 a22
  缓存）+a22 对照 10 局；条目=局号或 replay 路径，重叠条目按唯一局去重计
  归 judge_predict_replay）。
- bench：判决闭环副证配置（缺省 None=judge 验收档：vs r37 主对 16 局+vs
  r34a 辅对 8 局+反制臂 8+8，seed 41000/42000/43000/44000 起）。
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

from orderbook_predict import build_r39 as _b39         # noqa: E402
from orderbook_predict import gates_r39 as _g39         # noqa: E402
from orderbook_predict import judge_predict as _jp      # noqa: E402

EVIDENCE_DIR = os.path.join(HERE, "evidence")

R37_MAIN = os.path.join(KSIM, "orderbook_r37", "build", "main.py")
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
EVIDENCE_BUILD = "run_r39_build_realrun.json"
EVIDENCE_JUDGMENT = "run_r39_judge_realrun.json"
EVIDENCE_GATES = _g39.SUMMARY_NAME          # gates_r39_realrun.json（自写）
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
    """judge evidence 总判据：六判据全绿（criteria 全 True 且 overall.pass）。

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
        "protocol": "run-r39-standing-launch/1.0",
        "standing": ("standing 授权代执行（主会话沿 SOP 执行实际提交："
                     "每日≤5/候选≤2/Error 即停）"),
        "ref": "PENDING",
        "artifacts": _artifacts(build),
        "condition": "六判据+五门全绿交发射（R22 发射条款）",
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
        "protocol": "run-r39-archive/1.0",
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


def run_r39_iteration(out_dir: Optional[str] = None,
                      n_judgment: Optional[int] = None,
                      corpus: Optional[Sequence[str]] = None,
                      bench: Optional[Dict[str, Any]] = None,
                      ) -> Dict[str, Any]:
    """编排：构建→判决（六判据）→（全绿才）门禁→发射/收档裁决；evidence+台账。

    签名意图：输入: 无（CLI） / 输出: {build, judgment, gates, verdict} /
    错误: fail-closed（任一判据红即判负收档不建发射版；Error 落 run_summary 后
    上抛）。
    可选参见签名微调登记（out_dir/n_judgment/corpus/bench）。
    """
    t0 = time.perf_counter()
    root = os.path.abspath(out_dir or HERE)
    evidence_dir = os.path.join(root, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    stage: Dict[str, Any] = {"build": None, "judgment": None, "gates": None}
    try:
        # ---- ① build_r39 产 r39 件（库内建+三 sha 自证，fail-closed） ----
        build = _b39.build_r39(R37_MAIN, out_dir=os.path.join(root, "build"))
        build_path = _write_json(
            os.path.join(evidence_dir, EVIDENCE_BUILD), {
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "generated_by": "run_r39_iteration",
                "r37_main_path": R37_MAIN,
                "build": build,
            })
        stage["build"] = {
            "main_path": build.get("main_path"),
            "main_sha256": build.get("main_sha256"),
            "tar_sha256": build.get("tar_sha256"),
            "block_sha": build.get("block_sha"),
            "library_sha256": build.get("library_sha256"),
            "shear_change_sha256": build.get("shear_change_sha256"),
            "evidence_path": build_path,
        }
        main_path = build.get("main_path")
        if not main_path:
            raise RuntimeError(f"build_r39 未返回 main_path：{build!r}")

        # ---- ② judge_predict_replay 判决（六判据：26 败局+10 对照+副证） ----
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
            "n_criteria": len(crit),
            "criteria": crit,
            "red": red_criteria,
            "evidence_path": jud_path,
        }

        # ---- ③ 门禁（六判据全绿才进；判红不进门禁记 skipped——B24 先例） ---
        if judgment_green:
            gates = _g39.verify_r39_gates(main_path, evidence_dir=evidence_dir)
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

        # ---- ④ 出口裁决（R22 出口预绑定：全绿交发射/任一红收档） -------
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
            "protocol": "run-r39/1.0",
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
        fail = {"protocol": "run-r39/1.0", "stage": stage,
                "verdict": {"launch_ready": False, "verdict": "ERROR",
                            "reason": f"{type(exc).__name__}: {exc}",
                            "judgment_green": False, "gates_green": False,
                            "standing_launch": None, "archive_ledger": None},
                "error": f"{type(exc).__name__}: {exc}",
                "wall_s": round(time.perf_counter() - t0, 1)}
        _write_json(os.path.join(evidence_dir, EVIDENCE_RUN), fail)
        raise
