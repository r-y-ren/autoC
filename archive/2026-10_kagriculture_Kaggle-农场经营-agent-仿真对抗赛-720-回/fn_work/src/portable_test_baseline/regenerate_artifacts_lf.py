"""以 LF 规范化重建旧树 exports 工件类 index 及其登记工件，双 sha 对照消除 CRLF 变体双值。

上游: R6, R20（详见 fn_docs/responsibility.md）

实现要点：
- 源事实：旧树 index 由 Windows autocrlf 机构建提交，登记 sha256 为 CRLF 字节口径
  （例: ablations/champ-vs-champ-r3p0-smoke.json 登记 c8a17920…=CRLF 值，POSIX
  fresh clone 盘上为 LF 字节 39ebe3…）→ POSIX 上 sha 校验类测试（旧树
  test_build_determinism / test_p3::TestPackaging / test_artifact_indexes）挂。
  旧树冻结不可改——一切重建产物只落 <战役根>/fn_work/artifacts/。
- 输入面=旧树 software/exports/*/index.json（"exports 根级 index 类"代表性集，
  程序化 glob 发现，零字面路径；当前实测五件: ablations/external/online/
  replay_dna/replay_profiles）。条目 path 为仓相对 posix 路径，经
  shared.discover_campaign_roots 定位仓根解析，且必须落在战役树内（fail-closed）。
- 双 sha 登记：每工件双口径并列——legacy_registered_sha256（index 原值，Windows
  机口径即 CRLF 值）+ lf_sha256（LF 规范化后重算）；盘上字节口径（disk_sha256/
  行末分类）只入对照报告，不入重建 index——重建 index 只含机器无关量，任何平台
  重跑字节一致。normalize_lf = CRLF→LF + 孤 CR→LF（完整规范化）。
- 打包工件类不重建：二进制 tar 与 CRLF 无关（test_p3::TestPackaging 挂因是登记
  sha 口径而非 tar 内容），kaggle_simulations/**/submission.tar.gz 原样登记说明。
  文本/二进制按后缀表+首 8KB 空字节嗅探双判。
- 确定性门（"生成不确定即失败"）：每个写出文件落盘后重读逐字节+sha 复核，不符
  即 ArtifactRebuildError；报告/重建 index 不含时间戳，同输入同机器重跑逐字节
  幂等（roundtrip 由镜像测试钉住）。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = [
    "ArtifactRebuildError",
    "TEXT_SUFFIXES",
    "BINARY_SUFFIXES",
    "normalize_lf",
    "classify_line_endings",
    "discover_export_indexes",
    "regenerate_artifacts_lf",
]

# 文本类后缀（LF 重建对象）；打包/二进制类后缀（不重建，登记说明）
TEXT_SUFFIXES = frozenset({".json", ".md", ".txt", ".csv", ".py", ".yaml", ".yml", ".log"})
BINARY_SUFFIXES = frozenset({
    ".tar", ".gz", ".tgz", ".zip", ".bin", ".pkl", ".parquet",
    ".png", ".jpg", ".pdf", ".xlsx", ".whl",
})

# 重建 index 的机器无关元数据（不含时间戳/主机名/盘上口径）
_LF_REBUILD_META = {
    "schema": "lf-rebuild/1.0",
    "policy": "CRLF->LF normalized rebuild; sha256 = LF-byte digest",
    "legacy_sha256_meaning": "index 原登记值（Windows autocrlf 机口径，多为 CRLF 值）",
}


class ArtifactRebuildError(RuntimeError):
    """LF 重建失败（确定性破坏/输入不可解析/路径越界）——fail-closed。"""


def normalize_lf(data: bytes) -> bytes:
    """完整 LF 规范化：CRLF→LF，孤 CR→LF（与 git autocrlf checkout 口径兼容）。"""
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def classify_line_endings(data: bytes) -> str:
    """字节序列行末分类: BINARY/CRLF/LF/MIXED（首 8KB 空字节嗅探二进制）。"""
    if b"\x00" in data[:8192]:
        return "BINARY"
    crlf = data.count(b"\r\n")
    cr = data.count(b"\r")
    if cr == 0:
        return "LF"
    if crlf and cr == crlf:
        return "CRLF"
    return "MIXED"


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_binary_artifact(path: Path) -> bool:
    suffix = path.suffix.lower()
    if suffix in BINARY_SUFFIXES:
        return True
    if suffix in TEXT_SUFFIXES:
        return False
    try:
        head = path.read_bytes()[:8192]
    except OSError:
        return False
    return b"\x00" in head


def _write_bytes_deterministic(target: Path, data: bytes, expected_sha: str) -> None:
    """确定性写出：落盘后重读逐字节+sha 复核，不符即 fail-closed。"""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    reread = target.read_bytes()
    if reread != data or _sha256_hex(reread) != expected_sha:
        raise ArtifactRebuildError(
            f"重建不确定: {target} 写后复核不一致（期望 sha {expected_sha}）"
        )


def discover_export_indexes() -> list[Path]:
    """程序化发现旧树 exports 根级 index 类工件源（software/exports/*/index.json）。"""
    software_root = discover_campaign_roots()["software_root"]
    exports = software_root / "exports"
    if not exports.is_dir():
        raise ArtifactRebuildError(f"旧树 exports 目录不存在: {exports}")
    return sorted(p for p in exports.glob("*/index.json") if p.is_file())


def _resolve_entry_source(root_base: Path, rel: str, campaign_root: Path,
                          software_root: Path) -> Path:
    """路径锚（2026-09-23 大整合）：index 条目登记的是旧布局 repo 相对路径
    （…/software/exports/…）。旧布局下按原路径直取；新布局（software 树已迁
    fn_work/legacy_software）下，原路径缺失且条目位于本战役 software/ 子树时
    改指迁移新位。其余情形保持原路径（由调用方 missing 分支 fail-closed）。"""
    src = root_base / rel
    if src.is_file():
        return src
    try:
        campaign_rel = src.resolve().relative_to(campaign_root.resolve())
    except ValueError:
        return src
    parts = campaign_rel.parts
    if parts and parts[0] == "software":
        relocated = software_root.joinpath(*parts[1:])
        if relocated.is_file():
            return relocated
    return src


def _resolve_index_paths(artifact_sources) -> list[Path]:
    if artifact_sources is None:
        index_paths = discover_export_indexes()
    elif isinstance(artifact_sources, (str, Path)):
        base = Path(artifact_sources)
        if base.is_dir():
            index_paths = sorted(p for p in base.glob("*/index.json") if p.is_file())
        elif base.is_file():
            index_paths = [base]
        else:
            raise ArtifactRebuildError(f"工件源路径不存在: {base}")
    else:
        index_paths = [Path(p) for p in artifact_sources]
        for p in index_paths:
            if not p.is_file():
                raise ArtifactRebuildError(f"index 工件源不是文件: {p}")
    if not index_paths:
        raise ArtifactRebuildError("未发现任何 exports 根级 index 类工件源（空集 fail-closed）")
    return index_paths


def _register_packaging_artifacts(software_root: Path, display) -> list[dict]:
    """打包工件类登记（不重建）：二进制 tar 与 CRLF 无关，原样登记+说明。"""
    out = []
    sims = software_root / "kaggle_simulations"
    for tar in sorted(sims.glob("**/submission.tar.gz")) if sims.is_dir() else []:
        out.append({
            "path": display(tar),
            "sha256": _sha256_hex(tar.read_bytes()),
            "size_bytes": tar.stat().st_size,
            "rebuilt": False,
            "reason": "二进制打包件与 CRLF 无关（旧树挂因=登记 sha 口径，非 tar 内容），不重建，原样登记",
        })
    return out


def regenerate_artifacts_lf(artifact_sources=None, output_root=None, *,
                            repo_root=None, campaign_boundary=None) -> tuple[Path, dict]:
    """LF 规范化重建 exports 工件类 index 及登记工件，产出双 sha 对照报告。

    Args:
        artifact_sources: None=程序化发现旧树 exports 根级 index 类；Path/str 目录
            （其下 */index.json）；或 index 路径可迭代集。
        output_root: 重建产物根；None=<战役根>/fn_work/artifacts/（新建属许可）。
            产物镜像仓相对路径布局，index 重建为 LF 值登记版（附 legacy 双口径）。
        repo_root: 条目 path 的解析基座；None=discover_campaign_roots 定位仓根
            （默认口径，测试注入 tmp 工件树时覆写）。
        campaign_boundary: 条目安全性边界（越界即 fail-closed）；None=战役根。

    Returns:
        (artifacts_root: Path, report: dict)。report 含逐条目双 sha 对照表
        （legacy=CRLF 口径登记值 / LF=规范化重算值 双登记）、集合统计、打包件
        不重建登记、报告文件路径。

    Raises:
        ArtifactRebuildError: 无工件源 / index 不可解析 / 条目越出安全边界 /
            写后确定性复核失败——一律 fail-closed，不留半成品语义。
    """
    discovered = discover_campaign_roots()
    campaign_root = discovered["campaign_root"]
    software_root = discovered["software_root"]
    root_base = Path(repo_root) if repo_root is not None else discovered["repo_root"]
    boundary = Path(campaign_boundary) if campaign_boundary is not None else campaign_root

    def _display(path: Path) -> str:
        try:
            return path.resolve().relative_to(root_base.resolve()).as_posix()
        except ValueError:
            return str(path)

    index_paths = _resolve_index_paths(artifact_sources)
    artifacts_root = Path(output_root) if output_root is not None else (
        campaign_root / "fn_work" / "artifacts")
    artifacts_root.mkdir(parents=True, exist_ok=True)

    dual_table: list[dict] = []
    collections: dict[str, dict] = {}

    for index_path in index_paths:
        collection = index_path.parent.name
        try:
            index_data = json.loads(index_path.read_bytes().decode("utf-8"))
        except (OSError, ValueError) as exc:
            raise ArtifactRebuildError(f"index 不可解析: {index_path}: {exc}") from exc
        entries = index_data.get("entries", [])
        stats = {
            "index_source": _display(index_path),
            "entries_total": len(entries),
            "rebuilt_lf": 0,
            "skipped_binary": 0,
            "missing": 0,
            "legacy_matches_disk": 0,
            "legacy_is_crlf_variant": 0,
        }
        rebuilt_entries = []
        for entry in entries:
            rel = entry.get("path", "")
            legacy_sha = entry.get("sha256")
            src = _resolve_entry_source(root_base, rel, campaign_root,
                                        software_root)
            if not src.is_file():
                stats["missing"] += 1
                dual_table.append({
                    "collection": collection, "path": rel,
                    "legacy_registered_sha256": legacy_sha,
                    "disk_sha256": None, "lf_sha256": None,
                    "disk_line_endings": "ABSENT",
                    "status": "missing",
                })
                kept = dict(entry)
                kept["lf_status"] = "missing"
                rebuilt_entries.append(kept)
                continue
            try:
                src.resolve().relative_to(boundary.resolve())
            except ValueError:
                raise ArtifactRebuildError(
                    f"index 条目越出安全边界（拒绝读写）: {rel}") from None
            if _is_binary_artifact(src):
                stats["skipped_binary"] += 1
                dual_table.append({
                    "collection": collection, "path": rel,
                    "legacy_registered_sha256": legacy_sha,
                    "disk_sha256": _sha256_hex(src.read_bytes()),
                    "lf_sha256": None,
                    "disk_line_endings": "BINARY",
                    "status": "skipped_binary",
                })
                kept = dict(entry)
                kept["lf_status"] = "skipped_binary"
                rebuilt_entries.append(kept)
                continue
            raw = src.read_bytes()
            lf_bytes = normalize_lf(raw)
            lf_sha = _sha256_hex(lf_bytes)
            disk_sha = _sha256_hex(raw)
            _write_bytes_deterministic(artifacts_root / rel, lf_bytes, lf_sha)
            stats["rebuilt_lf"] += 1
            if legacy_sha == disk_sha:
                stats["legacy_matches_disk"] += 1
            if legacy_sha is not None and legacy_sha != lf_sha and disk_sha == lf_sha:
                stats["legacy_is_crlf_variant"] += 1
            dual_table.append({
                "collection": collection, "path": rel,
                "legacy_registered_sha256": legacy_sha,
                "disk_sha256": disk_sha,
                "lf_sha256": lf_sha,
                "disk_line_endings": classify_line_endings(raw),
                "status": "rebuilt_lf",
            })
            rebuilt = dict(entry)
            rebuilt["sha256"] = lf_sha
            rebuilt["legacy_sha256"] = legacy_sha
            rebuilt["lf_status"] = "rebuilt_lf"
            rebuilt_entries.append(rebuilt)
        # 重建 index（LF 值登记 + legacy 双口径 + 机器无关元数据；不含输出位置
        # 等环境量——重建 index 本身位置无关，任何平台/目录重跑逐字节一致）
        rebuilt_index = dict(index_data)
        rebuilt_index["entries"] = rebuilt_entries
        rebuilt_index["lf_rebuild"] = dict(_LF_REBUILD_META)
        index_out = artifacts_root / _display(index_path)
        index_bytes = (json.dumps(rebuilt_index, indent=2, ensure_ascii=False)
                       + "\n").encode("utf-8")
        _write_bytes_deterministic(index_out, index_bytes, _sha256_hex(index_bytes))
        collections[collection] = stats

    packaging = _register_packaging_artifacts(software_root, _display)
    totals = {
        "collections": len(collections),
        "entries": sum(s["entries_total"] for s in collections.values()),
        "rebuilt_lf": sum(s["rebuilt_lf"] for s in collections.values()),
        "skipped_binary": sum(s["skipped_binary"] for s in collections.values()),
        "missing": sum(s["missing"] for s in collections.values()),
        "legacy_is_crlf_variant": sum(s["legacy_is_crlf_variant"]
                                      for s in collections.values()),
        "packaging_not_rebuilt": len(packaging),
    }
    report = {
        "artifact_sources": [_display(p) for p in index_paths],
        "output_root": str(artifacts_root),
        "collections": collections,
        "dual_sha_table": dual_table,
        "packaging_artifacts_not_rebuilt": packaging,
        "totals": totals,
    }
    # 对照报告落盘（JSON+Markdown，无时间戳，确定性字节）
    report_json = artifacts_root / "lf_rebuild_report.json"
    rj_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    _write_bytes_deterministic(report_json, rj_bytes, _sha256_hex(rj_bytes))
    lines = [
        "# LF 重建双 sha 对照报告（regenerate_artifacts_lf）",
        "",
        f"- 工件源（exports 根级 index 类）: {len(index_paths)} 件",
        f"- 条目总数 {totals['entries']}：重建 {totals['rebuilt_lf']}、"
        f"二进制跳过 {totals['skipped_binary']}、缺失 {totals['missing']}",
        f"- legacy=CRLF 口径登记值与 LF 值不同且盘上即 LF（Windows autocrlf 变体）: "
        f"{totals['legacy_is_crlf_variant']} 条",
        f"- 打包工件类不重建（二进制与 CRLF 无关）: {len(packaging)} 件",
        "",
        "| collection | path | legacy_registered_sha256 | lf_sha256 | 盘上行末 | 状态 |",
        "|---|---|---|---|---|---|",
    ]
    for row in dual_table:
        lines.append("| {} | {} | {} | {} | {} | {} |".format(
            row["collection"], row["path"],
            row["legacy_registered_sha256"] or "—",
            row["lf_sha256"] or "—",
            row["disk_line_endings"], row["status"]))
    report_md = artifacts_root / "lf_rebuild_report.md"
    md_bytes = ("\n".join(lines) + "\n").encode("utf-8")
    _write_bytes_deterministic(report_md, md_bytes, _sha256_hex(md_bytes))
    report["report_files"] = [str(report_json), str(report_md)]
    return artifacts_root, report
