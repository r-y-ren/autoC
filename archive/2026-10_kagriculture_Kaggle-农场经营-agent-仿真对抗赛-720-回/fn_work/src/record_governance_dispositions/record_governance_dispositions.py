"""治理处置记录编排（双源归源/蓝图失效声明/active_candidate 降级），产出 fn_docs 处置记录汇编。

上游: R4, R17, R21（详见 fn_docs/responsibility.md）

实现要点：
- 编排三叶（write_dual_source_provenance / declare_blueprint_cmd_invalidation /
  demote_active_candidate_ledger）+ 记录 schema 校验，汇编落
  <战役根>/fn_docs/governance_dispositions.md（索引三件）。
- 输入=处置清单（disposition_list）：恰三项，每项 {"kind", "payload"}，kind 取
  三枚举（dual_source_provenance / blueprint_cmd_invalidation / active_candidate_demotion），
  各恰一次（缺叶/重复/未知 kind 均 ValueError，fail-closed 不猜）。payload 缺省
  （None/{}/[]）时回落各叶内置默认载荷（入库实测事实）。
- 记录 schema 校验（生成后事实门）：逐叶输出文档必须存在且含必需标记——
  血统记录含两账号+"两账号间未定"+ref 56400478+残留清单；失效声明含两条 cmd id
  +"不存在"+静默事实；降级处置含"时点闸"+"降级"+现状快照键。缺标记即
  ValueError（记录不齐不许宣称编排成功）。
- 时点闸语义沿降级叶（now 透传；execute 不在编排面暴露——编排只产记录，
  物理动作战后单叶调用）。
- 确定性：汇编文档由三叶裁决与固定索引渲染，无时间戳；实跑入口
  default_disposition_list() 提供入库事实默认载荷。
"""

from __future__ import annotations

from pathlib import Path

from record_governance_dispositions.declare_blueprint_cmd_invalidation import (
    DEFAULT_INVALID_CMDS,
    DEFAULT_SILENT_FACT,
    declare_blueprint_cmd_invalidation,
)
from record_governance_dispositions.demote_active_candidate_ledger import (
    DEFAULT_SNAPSHOT,
    demote_active_candidate_ledger,
)
from record_governance_dispositions.write_dual_source_provenance import (
    write_dual_source_provenance,
)
from shared.discover_campaign_roots import discover_campaign_roots

__all__ = [
    "KIND_PROVENANCE",
    "KIND_BLUEPRINT_INVALIDATION",
    "KIND_ACTIVE_CANDIDATE",
    "KIND_PAYLOAD_DEFAULTS",
    "DEFAULT_DUAL_SOURCE_EVIDENCE",
    "default_disposition_list",
    "default_output_path",
    "validate_record_schema",
    "record_governance_dispositions",
]

KIND_PROVENANCE = "dual_source_provenance"
KIND_BLUEPRINT_INVALIDATION = "blueprint_cmd_invalidation"
KIND_ACTIVE_CANDIDATE = "active_candidate_demotion"
_KINDS = (KIND_PROVENANCE, KIND_BLUEPRINT_INVALIDATION, KIND_ACTIVE_CANDIDATE)

# 入库实测默认载荷：源A/B 证据（源: opponents/PROVENANCE.md、v48plus/README、
# references/INDEX.md L38——引用纪律，逐字段可溯源）
DEFAULT_DUAL_SOURCE_EVIDENCE = {
    "artifact_sha256": "dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a",
    "artifact_bytes": 107008,
    "online_ref": 56400478,
    "requirement": "R4",
    "original_attribution": "两账号间未定",
    "sources": [
        {
            "key": "A",
            "account": "kaitofukami",
            "notebook": "40/40 Early Floor | 39/46 Top-10 | v48 Fast Routes",
            "acquired_date": "2026-08-31",
            "channel": "kaggle kernels pull（首拉，自解包 cell 执行重建）",
            "artifact_sha256_evidence": "dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a（与 notebook §7 公布值逐字节一致）",
            "record_file": "software/kaggle_simulations/opponents/PROVENANCE.md",
            "license": "无显式许可（notebook 未附开源许可；只作对手重放，不挖实现）",
            "notes": "作者自报面板: first-20 40/40、Top-10 holdout 39/46、Top-30 97/140（冻结动作流重放，非天梯分）",
        },
        {
            "key": "B",
            "account": "ahmedberatozer",
            "notebook": "kaggriculture-v48-clear-the-queue（Kaggriculture V48 — Clear the Queue）",
            "acquired_date": "2026-09-20",
            "channel": "kaggle kernels pull（终局期 fresh-sweep 拉回）",
            "artifact_sha256_evidence": "base=其提交包解码真源码 dadee25a…（notebook 内嵌源 sha 4b540288…）",
            "record_file": "software/kaggle_simulations/v48plus/README.md",
            "license": "Apache-2.0（notebook 声明，待核）",
            "notes": "实证: references/INDEX.md L38（fresh-20260920 批次含 ahmedberatozer/v48-clear-the-queue）",
        },
    ],
}


def default_output_path() -> Path:
    """汇编默认输出路径：<战役根>/fn_docs/governance_dispositions.md（不写盘）。"""
    campaign_root = discover_campaign_roots()["campaign_root"]
    return campaign_root / "fn_docs" / "governance_dispositions.md"


def default_disposition_list() -> list:
    """实跑默认处置清单：三叶载荷全部取入库实测事实默认值。"""
    return [
        {"kind": KIND_PROVENANCE, "payload": DEFAULT_DUAL_SOURCE_EVIDENCE},
        {"kind": KIND_BLUEPRINT_INVALIDATION, "payload": DEFAULT_INVALID_CMDS},
        {"kind": KIND_ACTIVE_CANDIDATE, "payload": DEFAULT_SNAPSHOT},
    ]


_KIND_PAYLOAD_DEFAULTS = {
    KIND_PROVENANCE: DEFAULT_DUAL_SOURCE_EVIDENCE,
    KIND_BLUEPRINT_INVALIDATION: DEFAULT_INVALID_CMDS,
    KIND_ACTIVE_CANDIDATE: DEFAULT_SNAPSHOT,
}


def _validate_envelope(disposition_list: list) -> list[str]:
    """处置清单信封校验（fail-closed）：三项、kind 枚举内、各恰一次。"""
    if not isinstance(disposition_list, list):
        raise ValueError(f"disposition_list 必须为 list，实得 {type(disposition_list).__name__}")
    if not disposition_list:
        raise ValueError("disposition_list 为空——编排面要求三叶齐备（缺叶即拒）")
    kinds: list[str] = []
    for i, entry in enumerate(disposition_list):
        if not isinstance(entry, dict) or "kind" not in entry:
            raise ValueError(f"处置项[{i}] 必须为含 kind 键的 dict，实得 {entry!r}")
        kind = entry["kind"]
        if kind not in _KINDS:
            raise ValueError(f"处置项[{i}] kind={kind!r} 不在枚举 {_KINDS}（未知处置类别，拒绝）")
        kinds.append(kind)
    missing = [k for k in _KINDS if k not in kinds]
    if missing:
        raise ValueError(f"处置清单缺叶: {missing}（编排面要求三叶齐备，缺叶即拒）")
    duplicated = sorted({k for k in kinds if kinds.count(k) > 1})
    if duplicated:
        raise ValueError(f"处置清单重复叶: {duplicated}（各处置恰一次）")
    return kinds


def _resolve_payload(entry: dict) -> object:
    """载荷回落：显式空载荷（None/{}/[]）→ 各叶内置入库事实默认值。"""
    payload = entry.get("payload")
    if payload is None or payload == {} or payload == []:
        return _KIND_PAYLOAD_DEFAULTS[entry["kind"]]
    return payload


# 记录 schema 校验标记（生成后事实门）
_RECORD_SCHEMA_MARKERS = {
    "provenance_dadee25a.md": (
        "kaitofukami", "ahmedberatozer", "两账号间未定", "56400478", "残留清单",
    ),
    "blueprint_cmd_invalidation.md": (
        "doc-compile", "doc-consistency", "不存在", "静默事实",
    ),
    "active_candidate_disposition.md": (
        "时点闸", "降级", "online_submission_refs", "v72-frozen",
    ),
}


def validate_record_schema(fn_docs_dir: Path) -> dict:
    """逐记录 schema 校验：文件存在+必需标记齐备；缺即 ValueError。"""
    results = {}
    for filename, markers in _RECORD_SCHEMA_MARKERS.items():
        path = fn_docs_dir / filename
        if not path.is_file():
            raise ValueError(f"处置记录缺失: {path}（记录不齐不许宣称编排成功）")
        text = path.read_text(encoding="utf-8")
        miss = [m for m in markers if m not in text]
        if miss:
            raise ValueError(f"处置记录 {filename} 缺 schema 标记: {miss}")
        results[filename] = {"exists": True, "markers": len(markers), "missing": []}
    return results


def _render_assembly(dispositions: list, schema_results: dict) -> str:
    """确定性渲染处置汇编（索引三件；无时间戳）。"""
    index = {
        KIND_PROVENANCE: ("provenance_dadee25a.md", "R4",
                          "dadee25a 双源血统（kaitofukami 08-31 首拉 + ahmedberatozer 09-20 拉回，"
                          "原创归属两账号间未定）+ 全库单源断言扫描清单"),
        KIND_BLUEPRINT_INVALIDATION: ("blueprint_cmd_invalidation.md", "R17",
                                      "蓝图 2 条失效验收 cmd（docs/report.typ、"
                                      "docs/check_report_metrics.py 不存在）+ 09-01 后 /accept 静默事实；"
                                      "处置=战后经 /attack 修订"),
        KIND_ACTIVE_CANDIDATE: ("active_candidate_disposition.md", "R17/R21",
                                "active_candidate 现状快照（v72 时代/online_refs 空）+ 战后降级预案"
                                "+ 时点闸（2026-09-30 收口前只许记录，物理动作拒绝）"),
    }
    lines: list[str] = []
    lines.append("# 治理处置记录汇编（record_governance_dispositions · R4/R17/R21）")
    lines.append("")
    lines.append("本汇编索引三件处置记录；各记录事实与判据见其正文。")
    lines.append("")
    lines.append("| 处置 | 记录文件（fn_docs/） | 需求 | 要点 |")
    lines.append("|---|---|---|---|")
    for d in dispositions:
        filename, req, summary = index[d["kind"]]
        lines.append(f"| {d['kind']} | {filename} | {req} | {summary} |")
    lines.append("")
    lines.append("## 记录 schema 校验")
    lines.append("")
    lines.append("| 记录 | 存在 | 必需标记数 | 缺失 |")
    lines.append("|---|---|---|---|")
    for filename, r in schema_results.items():
        lines.append(f"| {filename} | {r['exists']} | {r['markers']} | {r['missing'] or '无'} |")
    lines.append("")
    lines.append("## 编排元信息")
    lines.append("")
    lines.append("- 生成器: fn_work/src/record_governance_dispositions/record_governance_dispositions.py（W4 治理处置编排）")
    lines.append("- 编排语义: 只产记录不改物理面（旧树冻结；蓝图修订战后 /attack；台账降级战后受时点闸）。")
    lines.append("")
    return "\n".join(lines)


def record_governance_dispositions(
    disposition_list: list,
    *,
    now=None,
    campaign_root: Path | None = None,
    output_path: Path | None = None,
) -> dict:
    """编排三叶处置记录+schema 校验，落 fn_docs 汇编文档。

    Args:
        disposition_list: 处置清单——恰三项 {"kind", "payload"}（kind 见枚举；
            payload 可省/空=用各叶入库事实默认载荷）。also 接受
            default_disposition_list()。
        now: 时钟透传降级叶（date/datetime；None=系统当日；测试可注入）。
        campaign_root: 战役根（None=按目录特征程序化发现，R20）。
        output_path: 汇编输出路径（None=<战役根>/fn_docs/governance_dispositions.md）。

    Returns:
        裁决 dict：{"schema_valid", "campaign_root", "dispositions", "records",
        "assembly_output"}。
    """
    _validate_envelope(disposition_list)
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    if output_path is None:
        output_path = campaign_root / "fn_docs" / "governance_dispositions.md"

    dispositions = []
    for entry in disposition_list:
        kind = entry["kind"]
        payload = _resolve_payload(entry)
        if kind == KIND_PROVENANCE:
            verdict = write_dual_source_provenance(
                payload, campaign_root=campaign_root,
                output_path=campaign_root / "fn_docs" / "provenance_dadee25a.md",
            )
        elif kind == KIND_BLUEPRINT_INVALIDATION:
            verdict = declare_blueprint_cmd_invalidation(
                payload, campaign_root=campaign_root,
                output_path=campaign_root / "fn_docs" / "blueprint_cmd_invalidation.md",
            )
        else:
            verdict = demote_active_candidate_ledger(
                payload, now=now, execute=False, campaign_root=campaign_root,
                output_path=campaign_root / "fn_docs" / "active_candidate_disposition.md",
            )
        dispositions.append({"kind": kind, "status": "recorded", "verdict": verdict})

    schema_results = validate_record_schema(campaign_root / "fn_docs")
    text = _render_assembly(dispositions, schema_results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8", newline="\n")
    return {
        "schema_valid": True,
        "campaign_root": campaign_root,
        "dispositions": dispositions,
        "records": schema_results,
        "assembly_output": output_path,
    }
