# -*- coding: utf-8 -*-
"""run_r37_iteration（R19/R20 L0）：编排。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
build_r37 产 r37 合一件（白名单三件：守卫块/羊时序/尾盘修剪）→
judge_cash_guard_replay（6 灾难局+10 胜局对照重演）+ judge_sheep_league
（300-500 局联赛）→ verify_r37_gates fail-closed 全跑 → 判决+门禁全绿
交发射（standing 代执行+台账留痕，Error 即停）；任一红即停不发射。
evidence 三件（build 审计/replay 判决/联赛判决）+门禁台账。

编排口径（实现与测试同钉）：
- 段序=build →判决段→门禁段→发射段。任一段红即停在段界不发射（"任一红
  即停"）：判决段任一判决红 → **不进门禁**（gates 记 skipped）不发射；
  门禁段 overall 红 → 不发射；Error（异常）即停——落 run_summary 后上抛，
  不发射不重试（SOP：每日≤5/候选≤2）。
- 判决段两件（judge_cash_guard_replay、judge_sheep_league）各自 fail-closed
  全跑（R19/R20 归因分属两条判决线，段内不短路；两 judge 单局级"不短路全跑"
  自带）。判决红=judge 返回 overall.pass 不为 True（judge 自身 fail-closed
  聚合口径）。
- 门禁段只在判决全绿后进入（判决红→不进门禁），进入即 verify_r37_gates
  fail-closed 全跑（门内全跑不短路归 gates_r37）。
- 发射段（判决+门禁全绿才进）：standing 代执行+台账留痕——写
  evidence/launch_ledger.json（件身份 main/tar sha、描述文案、ref PENDING、
  "standing 授权代执行（主会话沿 SOP 执行实际提交：每日≤5/候选≤2/Error
  即停）"）；台账写入自身 Error 同样即停（上抛）。
- evidence 落 <out_dir>/evidence/：三件 build_audit.json（build_r37 返回审计
  件）/replay_judgment.json（judge_cash_guard_replay 判决）/judge_sheep_league
  .json（联赛判决）+门禁台账 gates_r37_realrun.json（verify_r37_gates 自写，
  evidence_dir 重指本目录）+run_summary.json（阶段态记录）+launch_ledger.json
  （发射段台账，仅全绿路）。

【签名微调登记（批间）】run_r37_iteration(out_dir=None, n_league_games=400,
corpus=None, opponents=None)：
- out_dir：证据/台账落点根与构建产物根（缺省本包 orderbook_r37/，build 产物
  落 <out_dir>/build/）；测试以 tmp 覆盖防覆写真台账。
- n_league_games：联赛总对局数（缺省 400；300-500 验收区间，judge_sheep_
  league n_games 同参，≥2 偶数）。
- corpus：重演语料局单（缺省固定 6 灾难局+10 对照局 episode id，R19 判决同
  单；条目=局号或 replay 路径）。
- opponents：强对手样本清单（缺省 r33 variant_tuned/r30 orderbook_derivative/
  v48_derivative 三件，R20 判决代理口径）。
首参与返回主键不变（{build, judgments, gates, verdict}）。
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

from orderbook_r37 import build_r37 as _b37          # noqa: E402
from orderbook_r37 import gates_r37 as _g37          # noqa: E402
from orderbook_r37 import judge_league as _jl        # noqa: E402
from orderbook_r37 import judge_replay as _jr        # noqa: E402

EVIDENCE_DIR = os.path.join(HERE, "evidence")

R34A_MAIN = os.path.join(KSIM, "orderbook_2965_adopt", "a", "main.py")
DEFAULT_CORPUS = (
    "112938600", "112968467", "112976582",   # 灾难局 6 件（R19 固定单）
    "113002280", "113094793", "113099386",
    "112937338", "112943297", "112969611",   # 对照局 10 件（同窗抽样）
    "112971928", "112973096", "112983518",
    "112984665", "112986874", "112992971", "113064702",
)
DEFAULT_OPPONENTS = (
    os.path.join(KSIM, "orderbook_l3_derivative", "variant_tuned", "main.py"),
    os.path.join(KSIM, "orderbook_derivative", "main.py"),
    os.path.join(KSIM, "v48_derivative", "main.py"),
)
EVIDENCE_BUILD = "build_audit.json"
EVIDENCE_REPLAY = "replay_judgment.json"
EVIDENCE_LEAGUE = "judge_sheep_league.json"
EVIDENCE_LAUNCH = "launch_ledger.json"
EVIDENCE_RUN = "run_summary.json"


def _write_json(path: str, payload: Any) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return path


def _overall_flag(ev: Any) -> bool:
    """judge evidence 总判据：overall.pass（两 judge fail-closed 聚合口径）。"""
    return bool((ev or {}).get("overall", {}).get("pass"))


def _standing_launch(build: Dict[str, Any], evidence_dir: str) -> Dict[str, Any]:
    """发射段：standing 代执行+台账留痕（Error 即停；SOP 每日≤5/候选≤2）。"""
    manifest = build.get("manifest") or {}
    record = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol": "run-r37-standing-launch/1.0",
        "standing": ("standing 授权代执行（主会话沿 SOP 执行实际提交："
                     "每日≤5/候选≤2/Error 即停；09-28 后不新发）"),
        "ref": "PENDING",
        "artifacts": {
            "main_path": build.get("main_path"),
            "main_sha256": build.get("main_sha256"),
            "tar_sha256": build.get("tar_sha256"),
            "description": manifest.get("description"),
            "base_sha_chain": manifest.get("base_sha_chain"),
        },
        "condition": "判决+门禁全绿交发射（R19/R20 发射条款）",
        "judgments": ["judge_cash_guard_replay", "judge_sheep_league"],
        "gates_ledger": os.path.join(evidence_dir, _g37.SUMMARY_NAME),
    }
    record["ledger_path"] = _write_json(
        os.path.join(evidence_dir, EVIDENCE_LAUNCH), record)
    return record


def run_r37_iteration(out_dir: Optional[str] = None,
                      n_league_games: int = 400,
                      corpus: Optional[Sequence[str]] = None,
                      opponents: Optional[Sequence[str]] = None,
                      ) -> Dict[str, Any]:
    """编排：构建→判决两件→门禁→发射裁决；evidence 三件+门禁台账。

    签名意图：输入: 无（CLI） / 输出: {build, judgments, gates, verdict} /
    错误: fail-closed（任一红即停不发射；Error 落 run_summary 后上抛）。
    可选参见签名微调登记（out_dir/n_league_games/corpus/opponents）。
    """
    t0 = time.perf_counter()
    root = os.path.abspath(out_dir or HERE)
    evidence_dir = os.path.join(root, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    stage: Dict[str, Any] = {"build": None, "judgments": None, "gates": None}
    try:
        # ---- ① build_r37 产 r37 合一件（白名单三件） ----------------------
        build = _b37.build_r37(R34A_MAIN, out_dir=os.path.join(root, "build"))
        _write_json(os.path.join(evidence_dir, EVIDENCE_BUILD), {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "generated_by": "run_r37_iteration",
            "r34a_main_path": R34A_MAIN,
            "build": build,
        })
        stage["build"] = {k: build.get(k) for k in
                          ("main_path", "main_sha256", "tar_sha256",
                           "r34a_sha256", "grid_info_note")}
        main_path = build.get("main_path")
        if not main_path:
            raise RuntimeError(f"build_r37 未返回 main_path：{build!r}")

        # ---- ② 判决两件（各自 fail-closed 全跑；任一红停在段界） ----------
        replay_ev = _jr.judge_cash_guard_replay(
            main_path, list(corpus if corpus is not None else DEFAULT_CORPUS))
        _write_json(os.path.join(evidence_dir, EVIDENCE_REPLAY), replay_ev)
        league_ev = _jl.judge_sheep_league(
            main_path, R34A_MAIN,
            list(opponents if opponents is not None else DEFAULT_OPPONENTS),
            n_games=n_league_games)
        _write_json(os.path.join(evidence_dir, EVIDENCE_LEAGUE), league_ev)
        replay_ok, league_ok = _overall_flag(replay_ev), _overall_flag(league_ev)
        judgments_green = bool(replay_ok and league_ok)
        stage["judgments"] = {
            "judge_cash_guard_replay": {
                "pass": replay_ok,
                "aggregate": (replay_ev.get("aggregate")
                              if isinstance(replay_ev, dict) else None),
                "evidence_path": os.path.join(evidence_dir, EVIDENCE_REPLAY),
            },
            "judge_sheep_league": {
                "pass": league_ok,
                "config": (league_ev.get("config")
                           if isinstance(league_ev, dict) else None),
                "evidence_path": os.path.join(evidence_dir, EVIDENCE_LEAGUE),
            },
            "green": judgments_green,
        }

        # ---- ③ 门禁（判决全绿才进门；fail-closed 全跑不短路） -------------
        if judgments_green:
            gates = _g37.verify_r37_gates(main_path, evidence_dir=evidence_dir)
            stage["gates"] = {
                "overall": bool(gates.get("overall")),
                "gates_passed": gates.get("gates_passed"),
                "summary_path": gates.get("summary_path"),
            }
            gates_green = bool(gates.get("overall"))
        else:
            gates = {"skipped": True, "overall": False,
                     "reason": "判决红→不进门禁（任一红即停不发射）"}
            stage["gates"] = {"skipped": True, "overall": False}
            gates_green = False

        # ---- ④ 发射裁决（判决+门禁全绿才交发射） -------------------------
        launch_ready = bool(judgments_green and gates_green)
        verdict: Dict[str, Any] = {
            "launch_ready": launch_ready,
            "verdict": "LAUNCH" if launch_ready else "HOLD",
            "judgments_green": judgments_green,
            "gates_green": gates_green,
            "standing_launch": None,
        }
        if launch_ready:
            verdict["standing_launch"] = _standing_launch(build, evidence_dir)
        summary = {
            "protocol": "run-r37/1.0",
            "stage": stage,
            "verdict": verdict,
            "wall_s": round(time.perf_counter() - t0, 1),
        }
        path = _write_json(os.path.join(evidence_dir, EVIDENCE_RUN), summary)
        return {
            "build": build,
            "judgments": {"judge_cash_guard_replay": replay_ev,
                          "judge_sheep_league": league_ev},
            "gates": gates,
            "verdict": {**verdict, "run_summary_path": path},
        }
    except Exception as exc:
        fail = {"protocol": "run-r37/1.0", "stage": stage,
                "verdict": {"launch_ready": False, "verdict": "HOLD",
                            "standing_launch": None},
                "error": f"{type(exc).__name__}: {exc}",
                "wall_s": round(time.perf_counter() - t0, 1)}
        _write_json(os.path.join(evidence_dir, EVIDENCE_RUN), fail)
        raise


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:
        print("usage: python run_r37.py（无参，evidence 落本包 evidence/）",
              file=sys.stderr)
        return 2
    result = run_r37_iteration()
    print(json.dumps({k: result[k] for k in ("verdict",)}, ensure_ascii=False,
                     indent=1))
    return 0 if result["verdict"]["launch_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
