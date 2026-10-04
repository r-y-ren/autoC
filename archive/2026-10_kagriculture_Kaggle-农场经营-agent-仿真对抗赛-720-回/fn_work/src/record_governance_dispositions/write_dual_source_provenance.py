"""dadee25a 双源血统记录（kaitofukami 08-31 首拉+ahmedberatozer 09-20 拉回，各自日期/sha/许可现状，原创归属标"两账号间未定"），全库对外引用处去单源断言。

上游: R4, R17, R21（详见 fn_docs/responsibility.md）

实现要点：
- 输出=<战役根>/fn_docs/provenance_dadee25a.md（测试经 output_path 重定向 tmp，
  不写战役树）。文档确定性渲染：同一证据两次生成逐字节一致（无时间戳），
  一切事实来自传入 source_evidence（引用纪律：不凭记忆补证据）。
- 双源=同 sha（dadee25a…）经两条独立账号通道入库：源A kaitofukami
  "40/40 Early Floor | 39/46 Top-10 | v48 Fast Routes"（2026-08-31 首拉，记录方
  opponents/PROVENANCE.md）；源B ahmedberatozer "kaggriculture-v48-clear-the-queue"
  （2026-09-20 拉回，记录方 v48plus/README，references/INDEX.md L38 实证）。
  许可现状：A=无显式许可，B=Apache-2.0 声明待核。原创归属=两账号间未定。
- 单源断言扫描（R4 验收"全库 grep"的可执行化）：扫描面=两记录文件+对外文档面
  （docs/**/*.md）；规则=文件内提及两账号标记恰一个→单源断言残留，两个→双源，
  零个→与血统无关。残留清单入文档，处置=旧树冻结，战后随迁移副本物理统一
  （旧树 PROVENANCE/v48plus README 本轮不改）。
- 在跑线上资产 ref 56400478 的引用规则=双源并列，不单源断言。
"""

from __future__ import annotations

from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = [
    "SOURCE_A_MARKERS",
    "SOURCE_B_MARKERS",
    "DEFAULT_RECORD_FILES",
    "ONLINE_REF_RULE",
    "default_output_path",
    "render_provenance_record",
    "scan_single_source_assertions",
    "write_dual_source_provenance",
]

# 账号识别标记（大小写不敏感；A=首拉方，B=拉回方）
SOURCE_A_MARKERS = ("kaitofukami",)
SOURCE_B_MARKERS = ("ahmedberatozer", "berat ozer")

# 默认扫描面之一：两记录文件（战役根相对路径，R20：不拼字面战役名）
DEFAULT_RECORD_FILES = (
    "software/kaggle_simulations/opponents/PROVENANCE.md",
    "software/kaggle_simulations/v48plus/README.md",
)
# 对外文档面（战役根相对 glob）
EXTERNAL_DOC_GLOB = "docs/**/*.md"

# 血统锚点（写入文档的引用规则）
ONLINE_REF_RULE = (
    "在跑线上资产 ref 56400478（dadee25a 衍生）的一切对外引用=双源并列"
    "（kaitofukami 2026-08-31 首拉 + ahmedberatozer 2026-09-20 拉回），"
    "禁止单源断言任一账号为唯一来源。"
)

_REQUIRED_TOP_KEYS = ("artifact_sha256", "online_ref", "sources", "original_attribution")
_REQUIRED_SOURCE_KEYS = (
    "key",
    "account",
    "notebook",
    "acquired_date",
    "channel",
    "record_file",
    "license",
)


def default_output_path() -> Path:
    """血统记录默认输出路径：<战役根>/fn_docs/provenance_dadee25a.md（不写盘）。"""
    campaign_root = discover_campaign_roots()["campaign_root"]
    return campaign_root / "fn_docs" / "provenance_dadee25a.md"


def _validate_evidence(source_evidence: dict) -> None:
    """证据完整性门（fail-closed）：缺键即抛，消息列全缺失项。"""
    if not isinstance(source_evidence, dict):
        raise ValueError(f"source_evidence 必须为 dict，实得 {type(source_evidence).__name__}")
    missing = [k for k in _REQUIRED_TOP_KEYS if not source_evidence.get(k)]
    if missing:
        raise ValueError(f"双源证据缺失顶层键: {missing}（证据缺失即失败，不降级渲染）")
    sources = source_evidence["sources"]
    if not isinstance(sources, list) or len(sources) != 2:
        raise ValueError(f"sources 必须为恰 2 个源的列表（双源记录），实得 {sources!r}")
    for src in sources:
        if not isinstance(src, dict):
            raise ValueError(f"源条目必须为 dict，实得 {src!r}")
        miss = [k for k in _REQUIRED_SOURCE_KEYS if not src.get(k)]
        if miss:
            raise ValueError(f"源 {src.get('key', '?')} 证据缺失键: {miss}")


def scan_single_source_assertions(campaign_root: Path) -> dict:
    """扫描两记录文件+对外文档面，产出单源断言残留清单。

    规则（确定性）：文件提及源A标记与源B标记（大小写不敏感）——
    恰一个→single-source 残留；两个→dual-source；零个→unrelated（与血统无关）。
    返回 {"targets", "counts", "residuals", "dual", "unrelated"}，路径为战役根相对。
    """
    targets: list[str] = list(DEFAULT_RECORD_FILES)
    docs_dir = campaign_root / "docs"
    if docs_dir.is_dir():
        targets.extend(
            str(p.relative_to(campaign_root)) for p in sorted(docs_dir.glob("**/*.md"))
        )
    counts: dict[str, str] = {}
    residuals: list[dict] = []
    dual: list[str] = []
    unrelated: list[str] = []
    for rel in targets:
        path = campaign_root / rel
        if not path.is_file():
            counts[rel] = "missing"
            unrelated.append(rel)
            continue
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        has_a = any(m in text for m in SOURCE_A_MARKERS)
        has_b = any(m in text for m in SOURCE_B_MARKERS)
        if has_a and has_b:
            counts[rel] = "dual-source"
            dual.append(rel)
        elif has_a:
            counts[rel] = "single-source(A)"
            residuals.append(
                {"path": rel, "mentions": "A(kaitofukami)", "missing": "B(ahmedberatozer)"}
            )
        elif has_b:
            counts[rel] = "single-source(B)"
            residuals.append(
                {"path": rel, "mentions": "B(ahmedberatozer)", "missing": "A(kaitofukami)"}
            )
        else:
            counts[rel] = "unrelated"
            unrelated.append(rel)
    return {
        "targets": targets,
        "counts": counts,
        "residuals": residuals,
        "dual": dual,
        "unrelated": unrelated,
    }


def _render_source_block(src: dict) -> list[str]:
    lines = []
    for label, key in (
        ("账号", "account"),
        ("notebook", "notebook"),
        ("拉取日期", "acquired_date"),
        ("来源通道", "channel"),
        ("sha", "artifact_sha256_evidence"),
        ("记录文件", "record_file"),
        ("许可现状", "license"),
    ):
        if src.get(key):
            lines.append(f"- {label}: {src[key]}")
    if src.get("notes"):
        lines.append(f"- 备注: {src['notes']}")
    return lines


def render_provenance_record(source_evidence: dict, scan: dict) -> str:
    """确定性渲染双源血统记录（无时间戳/主机名；事实全部来自传入证据）。"""
    src_a, src_b = source_evidence["sources"]
    if str(src_a.get("key", "")).upper() != "A":
        src_a, src_b = src_b, src_a
    lines: list[str] = []
    lines.append(f"# dadee25a 双源血统记录（{source_evidence.get('requirement', 'R4')}）")
    lines.append("")
    lines.append("## 血统对象")
    lines.append("")
    lines.append(f"- artifact sha256: `{source_evidence['artifact_sha256']}`")
    if source_evidence.get("artifact_bytes"):
        lines.append(f"- 字节数: {source_evidence['artifact_bytes']}（源A 记录方公布口径）")
    lines.append(f"- 定性: v48 公开衍生；在跑线上资产 ref {source_evidence['online_ref']}")
    lines.append("")
    lines.append("## 源 A（首拉）")
    lines.append("")
    lines.extend(_render_source_block(src_a))
    lines.append("")
    lines.append("## 源 B（拉回）")
    lines.append("")
    lines.extend(_render_source_block(src_b))
    lines.append("")
    lines.append("## 原创归属")
    lines.append("")
    lines.append(
        f"- **{source_evidence['original_attribution']}**（两账号通道各自独立入库同 sha；"
        "无证据裁断唯一原创方，对外不得断言任一账号为唯一作者。）"
    )
    lines.append("")
    lines.append("## 在跑线上资产引用规则")
    lines.append("")
    lines.append(f"- {ONLINE_REF_RULE}")
    lines.append("")
    lines.append("## 全库单源断言扫描（两记录文件+对外文档面）")
    lines.append("")
    lines.append(
        "- 扫描规则: 文件内提及两账号标记（大小写不敏感）恰一个=单源断言残留；"
        f"两个=双源；零个=与血统无关。扫描面=两记录文件 + `{EXTERNAL_DOC_GLOB}`。"
    )
    lines.append(
        f"- 扫描目标 {len(scan['targets'])} 件：双源 {len(scan['dual'])}、"
        f"单源残留 {len(scan['residuals'])}、无关/缺失 {len(scan['unrelated'])}。"
    )
    lines.append("")
    lines.append("### 残留清单（旧树冻结，战后处置）")
    lines.append("")
    if scan["residuals"]:
        lines.append("| 文件（战役根相对） | 仅提及 | 缺失源 |")
        lines.append("|---|---|---|")
        for r in scan["residuals"]:
            lines.append(f"| {r['path']} | {r['mentions']} | {r['missing']} |")
        lines.append("")
        lines.append(
            "- 处置: 残留文件属旧树（冻结），其单源表述的物理统一随新结构迁移副本"
            "落地执行（迁移副本按本记录双源化改写），旧树本体战后修改；"
            "新结构对外文档自即日起按上方【在跑线上资产引用规则】节双源引用。"
        )
    else:
        lines.append("- （扫描面内无单源断言残留。）")
    lines.append("")
    lines.append("### 对外文档面（docs/）结论")
    lines.append("")
    doc_face = [t for t in scan["targets"] if t not in DEFAULT_RECORD_FILES]
    if doc_face:
        for rel in doc_face:
            lines.append(f"- {rel}: {scan['counts'].get(rel, 'missing')}")
    else:
        lines.append("- （docs/ 下无 .md 或目录不存在——对外文档面零命中，无单源断言。）")
    lines.append("")
    lines.append("## 记录元信息")
    lines.append("")
    lines.append(
        "- 生成器: fn_work/src/record_governance_dispositions/write_dual_source_provenance.py"
        "（record_governance_dispositions 编排叶）"
    )
    lines.append(
        "- 引用纪律: 本记录一切源事实来自入库证据（opponents/PROVENANCE.md、"
        "v48plus/README、references/INDEX.md L38），不凭记忆撰写。"
    )
    lines.append("")
    return "\n".join(lines)


def write_dual_source_provenance(
    source_evidence: dict,
    *,
    campaign_root: Path | None = None,
    output_path: Path | None = None,
) -> dict:
    """生成双源血统记录文档并执行单源断言扫描。

    Args:
        source_evidence: 双源证据（artifact_sha256/online_ref/sources×2/
            original_attribution 等），缺键即 ValueError（证据缺失即失败）。
        campaign_root: 战役根（None=按目录特征程序化发现，R20）。
        output_path: 输出路径（None=<战役根>/fn_docs/provenance_dadee25a.md）。

    Returns:
        裁决 dict：{"output_path", "sources", "original_attribution",
        "online_reference_rule", "scan"}。
    """
    _validate_evidence(source_evidence)
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    if output_path is None:
        output_path = campaign_root / "fn_docs" / "provenance_dadee25a.md"
    scan = scan_single_source_assertions(campaign_root)
    text = render_provenance_record(source_evidence, scan)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8", newline="\n")
    return {
        "output_path": output_path,
        "sources": source_evidence["sources"],
        "original_attribution": source_evidence["original_attribution"],
        "online_reference_rule": ONLINE_REF_RULE,
        "scan": scan,
    }
