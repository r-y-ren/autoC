"""bc_track/README 复现命令路径修正+issues/03/08/04-07 票面状态与 JOURNAL 对齐（旧树冻结：修正以"修正副本+diff 注册（战后套用清单）"形态交付，物理修正战后套用——W3 注册表先例）。

上游: R7, R16, R18（详见 fn_docs/responsibility.md）

实现要点：
- 旧树 software/bc_track/ 全程只读；产物落 fn_work/doc_fixes/bc_track/：
  README.md 修正副本（kaggressure→kaggriculture 等逐处 diff）+ issues/03-08
  票面状态修正副本（03=closed-done 弃牌已裁决、08=closed 已关账、04-07=
  closed-not-triggered 未触发关闭）+ diff_registry.json（战后套用清单）。
- 台账事实源=JOURNAL BC 收口行（2026-09-20 交付行+2026-09-21 正式裁决行：
  "票 03 判定：弃牌收刀（379b41e）+ M1 结论正式勘误 + 票 08 关账"，⑤款=
  "票 04/05/06/07 按'过门才继续'不触发（GPU 未租用零成本）"）；解析缺行即
  fail-closed（DocFixError），不猜状态。
- 修正=最小 diff：README 三处（L10 路径拼写 kaggressure→kaggriculture /
  L5 "src//planner/" 双斜杠 / L50 票 03 节标题补正式裁决行号）；票面仅
  替换 **Status:** 行，正文零改动；issues/01/02 不在本批修正面（范围=
  responsibility 所列 03/08/04-07），注册表 out_of_scope_notes 如实披露。
- 每处 diff 逐条登记 old/new/line/reason/evidence；行号按旧树原文实算；
  注册表零绝对路径（战役根相对，跨机可 commit）。
- 路径全由调用方传入或经 shared.discover_campaign_roots 发现（R20）。
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["DocFixError", "fix_bc_track_records", "read_journal_rows"]

# JOURNAL 行选取标记：命中任一(票号关键词, 判定关键词)组合者=BC 收口行
_BC_ROW_MARKERS = (("票 03", "弃牌"), ("票 08", "关账"))
# 票面在册编号（本批修正面）
_TICKET_IDS = ("03", "04", "05", "06", "07", "08")
_STATUS_LINE_RE = re.compile(r"^\*\*Status:\*\*.*$", re.MULTILINE)
_DATE_RE = re.compile(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|")
_COMMIT_RE = re.compile(r"（([0-9a-f]{7,40})）")


class DocFixError(RuntimeError):
    """文档修正前置不满足（台账缺行/原文锚点失配/票面缺 Status 行）——fail-closed。"""


def read_journal_rows(journal_source, campaign_root=None) -> list[str]:
    """读 JOURNAL 台账行。journal_source: None=自战役根读 JOURNAL.md；str/Path=该文件；list=行串直用。"""
    if isinstance(journal_source, (list, tuple)):
        return [str(r) for r in journal_source]
    if journal_source is not None:
        path = Path(journal_source)
    elif campaign_root is not None:
        path = Path(campaign_root) / "JOURNAL.md"
    else:
        path = discover_campaign_roots()["campaign_root"] / "JOURNAL.md"
    if not path.is_file():
        raise DocFixError(f"JOURNAL 台账不存在: {path}")
    return path.read_text(encoding="utf-8").splitlines()


def _extract_bc_closeout(rows: list[str]) -> dict:
    """自 JOURNAL 行提取 BC 收口台账（正式裁决行=最末命中行）。缺行 fail-closed。"""
    hits = [
        r for r in rows
        if any(a in r and b in r for a, b in _BC_ROW_MARKERS)
    ]
    if not hits:
        raise DocFixError(
            "JOURNAL 台账中未找到 BC 收口行（标记=『票 03』+『弃牌』或『票 08』+『关账』）——"
            "票面状态无事实源，拒绝生成修正副本。"
        )
    formal = hits[-1]
    date_m = _DATE_RE.search(formal)
    commit_m = _COMMIT_RE.search(formal)
    clause_m = re.search(r"⑤([^⑤]*)", formal)
    return {
        "date": date_m.group(1) if date_m else None,
        "commit": commit_m.group(1) if commit_m else None,
        "clause5": clause_m.group(1).strip() if clause_m else "",
        "gpu_unrented": "GPU 未租用" in formal,
        "row_count": len(hits),
        "row_snippets": [h[:120] for h in hits],
    }


def _require(text: str, needle: str, where: str) -> None:
    if text.count(needle) != 1:
        raise DocFixError(f"{where} 原文锚点失配（期望恰 1 处，实得 {text.count(needle)}）: {needle!r}")


def _line_no(text: str, needle: str) -> int:
    return text[: text.index(needle)].count("\n") + 1


def _ticket_status(ticket_id: str, ledger: dict) -> tuple[str, str]:
    """票面新 Status 行与理由。返回 (new_status_line, reason)。"""
    date = ledger["date"] or "2026-09-21"
    commit = ledger["commit"] or ""
    commit_txt = f"，commit {commit}" if commit else ""
    if ticket_id == "03":
        new = (
            f"**Status:** closed-done（{date} 正式裁决=弃牌收刀{commit_txt}——JOURNAL 收口行"
            f"『票 03 判定：弃牌收刀』+ M1 结论正式勘误置顶；最好候选中位 1,995 = 门 A 的 6.2%，"
            f"塌方 12/12 ≠ 0；差距归因见下，收刀）"
        )
        reason = "票面 09-20 done 态补正式裁决口径（09-21 收口行+379b41e+勘误置顶）"
    elif ticket_id == "04":
        new = (
            f"**Status:** closed-not-triggered（{date} 未触发关闭：前置 03 未过门，"
            f"按『过门才继续』不触发——JOURNAL 收口行⑤；零执行零成本）"
        )
        reason = "ready-for-agent 态过期：03 弃牌后按票链门条件不触发"
    elif ticket_id == "05":
        new = (
            f"**Status:** closed-not-triggered（{date} 未触发关闭：前置 04 未执行，"
            f"『任一不过则出具书面弃牌结论』条款由 03 收口行承担——JOURNAL 收口行⑤；零执行零成本）"
        )
        reason = "ready-for-agent 态过期：弃牌结论已由 03 收口，05 硬门链不触发"
    elif ticket_id == "06":
        new = (
            f"**Status:** closed-not-triggered（{date} 未触发关闭：02/03 证据未表明算力是瓶颈，"
            f"GPU 未租用零成本——JOURNAL 收口行⑤）"
        )
        reason = "条件票未触发：GPU 未租用（台账明示零成本）"
    elif ticket_id == "07":
        new = (
            f"**Status:** closed-not-triggered（{date} 永久关闭：BC 未过门不解锁 RL 微调——"
            f"票面条款『BC 未过门则本票永久关闭』+ JOURNAL 收口行⑤）"
        )
        reason = "stretch 票永久关闭：解锁条件（03 过门）未达成"
    elif ticket_id == "08":
        new = (
            f"**Status:** closed（{date} 已关账：03 弃牌直接触发——JOURNAL 收口行『票 08 关账』；"
            f"保留资产与终局程序状态复核见该行⑤及尾段：24h 复采样在飞→09-25 对结构决策→"
            f"09-27 冻结→09-30 终交）"
        )
        reason = "ready-for-agent 态过期：已按 03 弃牌路径关账"
    else:  # pragma: no cover - 编号白名单外
        raise DocFixError(f"票号超出本批修正面: {ticket_id}")
    return new, reason


def fix_bc_track_records(journal_ledger=None, *, campaign_root=None,
                         doc_fixes_root=None) -> dict:
    """生成 bc_track 修正副本+diff 注册（旧树只读，产物落 fn_work/doc_fixes/bc_track/）。

    Args:
        journal_ledger: JOURNAL 台账来源（None=自战役根读；str/Path=文件；list=行串）。
        campaign_root: 战役根（None=特征发现）。
        doc_fixes_root: 修正副本落位根（None=campaign_root/fn_work/doc_fixes）。

    Returns:
        dict：corrected_files（战役根相对）/ diff_count / registry 路径 / ledger 台账摘要。

    Raises:
        DocFixError: 台账缺收口行 / 原文锚点失配 / 票面缺 Status 行 / 票面不齐。
    """
    roots = discover_campaign_roots() if campaign_root is None else None
    campaign_root = Path(campaign_root) if campaign_root is not None else roots["campaign_root"]
    if doc_fixes_root is None:
        doc_fixes_root = campaign_root / "fn_work" / "doc_fixes"

    ledger = _extract_bc_closeout(
        read_journal_rows(journal_ledger, campaign_root=campaign_root))

    # ---------- ① README 修正副本 ----------
    readme_src = campaign_root / "software" / "bc_track" / "README.md"
    if not readme_src.is_file():
        raise DocFixError(f"bc_track/README 不存在: {readme_src}")
    readme_old = readme_src.read_text(encoding="utf-8")

    readme_fixes = [
        {
            "old": "cd workspace/kaggressure/software",
            "new": "cd workspace/kaggriculture/software",
            "reason": "复现命令路径拼写：kaggressure→kaggriculture（R7 复现命令逐条可 cd）",
            "evidence": "workspace/ 目录实测：kaggriculture 在册，kaggressure 不存在",
        },
        {
            "old": "不改 src//planner/",
            "new": "不改 src/、planner/",
            "reason": "路径写法：双斜杠笔误→并列两目录",
            "evidence": "目录实测：src/ 与 planner/ 为两个并列目录",
        },
        {
            "old": "## 票 03 迭代结果（2026-09-20，判定=弃牌）",
            "new": (
                f"## 票 03 迭代结果（2026-09-20 迭代、{ledger['date']} 正式裁决=弃牌收刀"
                f"{(' ' + ledger['commit']) if ledger['commit'] else ''}）"
            ),
            "reason": "README 票 03 节标题与 JOURNAL 正式裁决行对齐（09-21 收口+commit）",
            "evidence": f"JOURNAL {ledger['date']} 收口行: {ledger['row_snippets'][-1]}",
        },
    ]
    readme_new = readme_old
    for fix in readme_fixes:
        _require(readme_new, fix["old"], "software/bc_track/README.md")
        readme_new = readme_new.replace(fix["old"], fix["new"])

    out_root = doc_fixes_root / "bc_track"
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "README.md").write_text(readme_new, encoding="utf-8")

    entries = []
    for fix in readme_fixes:
        entries.append({
            "file": "software/bc_track/README.md",
            "copy": "fn_work/doc_fixes/bc_track/README.md",
            "line": _line_no(readme_old, fix["old"]),
            "old": fix["old"],
            "new": fix["new"],
            "reason": fix["reason"],
            "evidence": fix["evidence"],
        })

    # ---------- ② issues/03-08 票面状态修正副本 ----------
    issues_src = campaign_root / "software" / "bc_track" / "issues"
    tickets = sorted(issues_src.glob("*.md"))
    by_id = {p.name[:2]: p for p in tickets}
    missing = [t for t in _TICKET_IDS if t not in by_id]
    if missing:
        raise DocFixError(f"票面不齐（缺 {missing}）——本批修正面 03-08 须全在册")

    issues_out = out_root / "issues"
    issues_out.mkdir(parents=True, exist_ok=True)
    for tid in _TICKET_IDS:
        src = by_id[tid]
        old_text = src.read_text(encoding="utf-8")
        found = _STATUS_LINE_RE.findall(old_text)
        if len(found) != 1:
            raise DocFixError(f"票面缺/多 Status 行（期望恰 1 行）: {src.name}")
        new_line, reason = _ticket_status(tid, ledger)
        old_line = found[0]
        new_text = old_text.replace(old_line, new_line, 1)
        (issues_out / src.name).write_text(new_text, encoding="utf-8")
        entries.append({
            "file": f"software/bc_track/issues/{src.name}",
            "copy": f"fn_work/doc_fixes/bc_track/issues/{src.name}",
            "line": _line_no(old_text, "**Status:**"),
            "old": old_line,
            "new": new_line,
            "reason": reason,
            "evidence": f"JOURNAL {ledger['date']} 收口行"
                        + (f"（⑤{ledger['clause5'][:60]}…）" if ledger["clause5"] else ""),
        })

    # ---------- ③ diff 注册（战后套用清单，W3 先例形态） ----------
    registry = {
        "contract": "R7 fix_bc_track_records（fn_docs/responsibility.md）——旧树冻结："
                    "修正以修正副本+diff 注册交付，战后套用",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "frozen_tree": True,
        "source_tree": "software/bc_track/（本批只读，零字节改动）",
        "corrected_copy_root": "fn_work/doc_fixes/bc_track/",
        "postwar_execution": {
            "when": "fn-close 期（战后收口，旧树冻结解除后）",
            "registry_only": True,
            "steps": [
                "按 entries 逐条把 old→new 套用至旧树对应文件"
                "（README 三处行替换；issues/03-08 的 **Status:** 行替换）",
                "套用后跑 R7 验收：README 复现命令逐条可 cd"
                "（cd workspace/kaggriculture/software 成立）",
                "票账一致复核：issues 03/08/04-07 Status 与 JOURNAL"
                " 2026-09-20/2026-09-21 BC 收口行对读一致",
            ],
        },
        "ledger_basis": {
            "journal": "JOURNAL.md",
            "formal_row_date": ledger["date"],
            "formal_row_commit": ledger["commit"],
            "row_count": ledger["row_count"],
            "row_snippets": ledger["row_snippets"],
        },
        "entries": entries,
        "out_of_scope_notes": [
            "issues/01/02 Status 行未在本批修正面（responsibility 范围=03/08/04-07）；"
            "其 checkbox 已全勾，完成态以 JOURNAL 2026-09-20 M0/M1 交付行为准",
        ],
    }
    registry_path = out_root / "diff_registry.json"
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    try:
        rel_root = out_root.relative_to(campaign_root)
        rel_files = [str(rel_root / "README.md")]
        rel_files += [str(rel_root / "issues" / by_id[t].name) for t in _TICKET_IDS]
        rel_files += [str(rel_root / "diff_registry.json")]
    except ValueError:  # 测试假树：doc_fixes 落在战役根外
        rel_files = [str(p) for p in sorted(out_root.rglob("*")) if p.is_file()]

    return {
        "corrected_files": rel_files,
        "diff_count": len(entries),
        "readme_diffs": len(readme_fixes),
        "ticket_diffs": len(_TICKET_IDS),
        "registry": str(registry_path),
        "ledger": ledger,
    }
