"""active_candidate.json 降级历史台账的处置记录与时点闸（动作本身=09-30 收口后执行，时点未到即拒绝执行动作、只许记录）。

上游: R4, R17, R21（详见 fn_docs/responsibility.md）

实现要点：
- 输出=<战役根>/fn_docs/active_candidate_disposition.md（测试经 output_path 重定向
  tmp，不写战役树）。记录态渲染确定性（快照事实来自传入 snapshot，不含时间戳；
  闸状态行的 now 取注入时钟或系统当日，属裁决信息非文档事实）。
- 现状快照（默认载荷=软件树 active_candidate.json 实测事实）：v72 时代——
  last_promoted_frozen=v72-frozen（sha c44e2b25…，published_holdout attempt 5），
  working=v14.3-sellrace-working（development），online_submission_refs=[]（空）。
- 时点闸（fail-closed）：GATE_DATE=2026-09-30（终局收口日）。now<=GATE_DATE 时
  execute=True 一律抛 DemotionGateError（含闸语义排查提示）——收口前只许产出
  记录，物理降级动作拒绝；now>GATE_DATE（即 10-01 起）方许执行。时钟可注入
  （now 参数接 date/datetime），测试不依赖系统日期。
- 物理动作语义（收口后）：读 ledger json，整体降级为历史台账形态
  （schema_version 加 "-historical" 后缀 + demoted_at/demote_reason 留痕 +
  原内容原样收进 historical 键），写回 ledger_path——不删任何字段，可回滚。
  现阶段生产环境只走记录态；本实现为战后动作预置且受闸硬断言。
- 不现在补记/不动在役身份链（R17：避免动在役身份链；补记与降级均战后）。
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = [
    "GATE_DATE",
    "DemotionGateError",
    "DEFAULT_SNAPSHOT",
    "DEMOTION_PLAN",
    "default_output_path",
    "default_ledger_path",
    "render_disposition_record",
    "demote_active_candidate_ledger",
]

# 时点闸：2026-09-30 终局收口日；收口前（含当日）物理动作一律拒绝
GATE_DATE = _dt.date(2026, 9, 30)


class DemotionGateError(RuntimeError):
    """时点未到即请求物理降级（fail-closed）：收口前只许产出记录。"""


# 现状快照默认载荷（源: 软件树 active_candidate.json 实测，2026-09-21 读取）
DEFAULT_SNAPSHOT = {
    "read_at": "2026-09-21（记录生成时实测读取）",
    "schema_version": "1.0",
    "working": {
        "label": "v14.3-sellrace-working",
        "status": "development",
        "sha256": "f1f46638b8b747b46282065f5e37f584a42d5f155a7b428b16d7be7625d185f7",
    },
    "last_promoted_frozen": {
        "label": "v72-frozen",
        "status": "frozen",
        "sha256": "c44e2b254686fc34ebfd055f51519f2aaac4a09bc68e2ac1f959f35b7ac90748",
    },
    "published_holdout": {
        "status": "published",
        "attempt_index": 5,
        "candidate_sha256": "c44e2b254686fc34ebfd055f51519f2aaac4a09bc68e2ac1f959f35b7ac90748",
    },
    "online_submission_refs": [],
    "era_summary": "v72 时代（在役身份链 working+promoted 冻结态并存；online_refs 空=无在册线上引用）",
}

# 降级预案（R17：战后降级为历史台账，不现在补记）
DEMOTION_PLAN = {
    "action": "降级 active_candidate.json 为历史台账（historical ledger）",
    "precondition": "终局收口（2026-09-30）完成之后；收口前物理动作被时点闸拒绝",
    "steps": [
        "1. 收口后读取在册 active_candidate.json，整体收进 historical 键（不删字段，可回滚）",
        "2. schema_version 追加 -historical 后缀，登记 demoted_at 与 demote_reason",
        "3. 新立（或移交）战后现役身份链载体，旧台账只读留档",
    ],
    "not_now": "不现在补记、不现在降级——避免动在役身份链（R17 明文）",
}

_REQUIRED_SNAPSHOT_KEYS = (
    "schema_version",
    "working",
    "last_promoted_frozen",
    "online_submission_refs",
)


def default_output_path() -> Path:
    """处置记录默认输出路径：<战役根>/fn_docs/active_candidate_disposition.md（不写盘）。"""
    campaign_root = discover_campaign_roots()["campaign_root"]
    return campaign_root / "fn_docs" / "active_candidate_disposition.md"


def default_ledger_path(campaign_root: Path | None = None) -> Path:
    """台账默认路径：<战役根>/software/active_candidate.json（不写盘）。"""
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    return campaign_root / "software" / "active_candidate.json"


def _as_date(now) -> _dt.date:
    """时钟归一：None=系统当日；datetime 取其 date；date 原样。"""
    if now is None:
        return _dt.date.today()
    if isinstance(now, _dt.datetime):
        return now.date()
    if isinstance(now, _dt.date):
        return now
    raise ValueError(f"now 必须为 date/datetime/None，实得 {type(now).__name__}")


def _validate_snapshot(snapshot: dict) -> None:
    if not isinstance(snapshot, dict):
        raise ValueError(f"snapshot 必须为 dict，实得 {type(snapshot).__name__}")
    missing = [k for k in _REQUIRED_SNAPSHOT_KEYS if k not in snapshot]
    if missing:
        raise ValueError(f"现状快照缺失键: {missing}（快照缺失即失败，不降级渲染）")


def _gate_status(now_date: _dt.date, execute: bool) -> dict:
    """时点闸裁决：收口前物理动作一律 refused，记录态恒 allowed。"""
    if now_date > GATE_DATE:
        action = "executed" if execute else "permitted-not-requested"
    else:
        action = "refused" if execute else "record-only"
    return {
        "now": now_date.isoformat(),
        "gate_date": GATE_DATE.isoformat(),
        "phase": "post-closeout" if now_date > GATE_DATE else "pre-closeout",
        "physical_action": action,
    }


def _apply_demotion(ledger_path: Path, now_date: _dt.date, reason: str) -> dict:
    """物理降级（仅收口后可达）：原内容整体收进 historical 键，可回滚。"""
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    demoted = {
        "schema_version": f"{ledger.get('schema_version', '1.0')}-historical",
        "demoted_at": now_date.isoformat(),
        "demote_reason": reason,
        "historical": ledger,
    }
    ledger_path.write_text(
        json.dumps(demoted, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return demoted


def render_disposition_record(snapshot: dict, gate: dict, executed: bool) -> str:
    """确定性渲染处置记录（快照事实来自传入载荷；闸状态行如实反映注入时钟裁决）。"""
    lines: list[str] = []
    lines.append("# active_candidate 降级处置记录（R17/R21）")
    lines.append("")
    lines.append("## 现状快照")
    lines.append("")
    if snapshot.get("read_at"):
        lines.append(f"- 读取时点: {snapshot['read_at']}")
    lines.append(f"- schema_version: {snapshot.get('schema_version', '—')}")
    working = snapshot.get("working") or {}
    lines.append(f"- working: {working.get('label', working if isinstance(working, str) else '—')}"
                 f"（status={working.get('status', '—')}，sha256={str(working.get('sha256', '—'))[:12]}…）")
    promoted = snapshot.get("last_promoted_frozen") or {}
    lines.append(f"- last_promoted_frozen: {promoted.get('label', '—')}"
                 f"（status={promoted.get('status', '—')}，sha256={str(promoted.get('sha256', '—'))[:12]}…）")
    holdout = snapshot.get("published_holdout") or {}
    if holdout:
        lines.append(f"- published_holdout: {holdout.get('status', '—')}"
                     f"（attempt {holdout.get('attempt_index', '—')}）")
    refs = snapshot.get("online_submission_refs")
    lines.append(f"- online_submission_refs: {refs!r}（{'空=无在册线上引用' if not refs else '非空'}）")
    if snapshot.get("era_summary"):
        lines.append(f"- 时代定性: {snapshot['era_summary']}")
    lines.append("")
    lines.append("## 降级预案（战后执行）")
    lines.append("")
    lines.append(f"- 动作: {DEMOTION_PLAN['action']}")
    lines.append(f"- 前置条件: {DEMOTION_PLAN['precondition']}")
    for step in DEMOTION_PLAN["steps"]:
        lines.append(f"- {step}")
    lines.append(f"- 边界: {DEMOTION_PLAN['not_now']}")
    lines.append("")
    lines.append("## 时点闸（fail-closed 断言）")
    lines.append("")
    lines.append(f"- 闸日: {gate['gate_date']}（终局收口日）；裁决时钟 now={gate['now']}"
                 f"（阶段={gate['phase']}）。")
    lines.append("- 语义: 收口前（now<=闸日，含收口日当日）物理降级动作一律拒绝"
                 "（DemotionGateError），只许产出本记录；收口后（now>闸日）方许执行。")
    lines.append(f"- 本次裁决: physical_action={gate['physical_action']}"
                 + ("（已执行：ledger 已降级为历史台账并留痕）" if executed else "（未请求物理动作，纯记录态）"))
    lines.append("")
    lines.append("## 记录元信息")
    lines.append("")
    lines.append("- 生成器: fn_work/src/record_governance_dispositions/demote_active_candidate_ledger.py"
                 "（record_governance_dispositions 编排叶）")
    lines.append("- 台账归宿: software/active_candidate.json（在役身份链，收口前零写入）。")
    lines.append("")
    return "\n".join(lines)


def demote_active_candidate_ledger(
    snapshot: dict,
    *,
    now=None,
    execute: bool = False,
    ledger_path: Path | None = None,
    campaign_root: Path | None = None,
    output_path: Path | None = None,
) -> dict:
    """产出 active_candidate 降级处置记录；物理降级受时点闸硬断言。

    Args:
        snapshot: 现状快照（schema_version/working/last_promoted_frozen/
            online_submission_refs 等），缺键即 ValueError。
        now: 时钟（date/datetime；None=系统当日）——闸判定与留痕用，可注入。
        execute: True=请求物理降级；收口前（now<=2026-09-30）抛 DemotionGateError。
        ledger_path: 台账路径（execute 时写；None=<战役根>/software/active_candidate.json）。
        campaign_root: 战役根（None=按目录特征程序化发现，R20）。
        output_path: 输出路径（None=<战役根>/fn_docs/active_candidate_disposition.md）。

    Returns:
        裁决 dict：{"output_path", "snapshot", "plan", "gate", "executed"}。

    Raises:
        DemotionGateError: 时点未到而请求物理动作（收口前只许记录）。
    """
    _validate_snapshot(snapshot)
    now_date = _as_date(now)
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    if output_path is None:
        output_path = campaign_root / "fn_docs" / "active_candidate_disposition.md"
    if ledger_path is None:
        ledger_path = default_ledger_path(campaign_root)

    executed = False
    demoted = None
    if execute:
        if now_date <= GATE_DATE:
            raise DemotionGateError(
                f"时点闸拒绝: now={now_date.isoformat()} <= 收口日 {GATE_DATE.isoformat()}——"
                "2026-09-30 收口前只许产出处置记录，物理降级动作一律拒绝"
                "（排查: 战后重试，或去掉 execute 走纯记录态。）"
            )
        demoted = _apply_demotion(
            ledger_path, now_date,
            reason="战后降级: 终局收口完成，在役身份链退役为历史台账（R17）",
        )
        executed = True

    gate = _gate_status(now_date, execute)
    text = render_disposition_record(snapshot, gate, executed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8", newline="\n")
    return {
        "output_path": output_path,
        "snapshot": snapshot,
        "plan": DEMOTION_PLAN,
        "gate": gate,
        "executed": executed,
        "demoted_ledger": demoted,
    }
