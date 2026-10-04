"""market_ledger 归位编排（R15/G17）：扫描旧树 scripts/ 检出无入口库件、在 fn_work 内建立新结构库位（market_ledger 源文件逐字节复制，可独立演进）、产出改线注册（旧 consumers 清单+新 import 路径）落盘 fn_work/library_relocation.json，返回裁决 dict（断链即失败）。

上游: R15（详见 fn_docs/responsibility.md）

实现要点：
- 旧树冻结（D14/终局隔离）：本批零物理搬移——库位=fn_work/src/
  relocate_library_modules/market_ledger.py 的**逐字节副本**（非薄包装
  re-export：包装件会反向依赖冻结旧树，战后旧件一移即断；副本可独立
  演进）。副本字节与源严格等价（sha256 双验），来源与战后改线方案以
  本 docstring+注册表双登记（不改副本字节，头注释登记职责由注册表
  承接）。
- 三步编排：①scan_for_library_misplacement 扫旧树 scripts/（只读），
  G17 源事实核验——market_ledger 必须在无入口库件清单内，缺位即
  fail-closed（源事实漂移）；清单内其余库件登记 additional_misplaced
  不静默（R15 管辖外，移交 fn-close 裁决）。②建库位：逐字节复制+
  sha256 等价断言+import 回探（importlib 按 path 装载副本，公开名
  OfficialMarketLedger/make_ledger_runner/summarize 在场即链通，
  缺名/语法坏=断链即失败）。③改线注册：扫 software 全域（scripts 平铺
  +其余子树递归，含 tests）找 market_ledger 消费方（import 语句/带引号
  文件名引用两形态，逐条带行号与改线指引），注册表落盘
  fn_work/library_relocation.json（战后 fn-close 搬移执行清单，
  同 archive_registry.json 形制）。
- 战后改线方案（注册表 postwar_execution）：rm 副本后 git mv 旧树源件
  至库位（副本与源逐字节等价，git mv 承接文件历史）；consumers 逐件
  改线至新 import（fn_work/src 在 sys.path 时
  ``from relocate_library_modules.market_ledger import OfficialMarketLedger``）；
  改线后跑 R15 验收：scripts/ 无无入口库件扫描断言+全量测试绿。
- 路径全由调用方传入或程序化发现（R20：模块内零字面战役路径）；
  scripts_dir 缺省=自本文件上溯发现战役根（blueprint.md+fn_docs 特征）
  下 software/scripts；library_dir 缺省=本模块所在包目录；探针不可注入
  面（复制/装载为确定性步骤），镜像测试以 tmp 假战役树全链演练。
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from relocate_library_modules.scan_for_library_misplacement import (
    scan_for_library_misplacement,
)

__all__ = ["relocate_library_modules", "LIB_MODULE", "NEW_IMPORT_MODULE",
           "LIB_PUBLIC_NAMES", "REGISTRY_NAME"]

# G17 源事实：唯一裁决归位件（software/scripts/market_ledger.py，无入口库模块）
LIB_MODULE = "market_ledger.py"
NEW_IMPORT_MODULE = "relocate_library_modules.market_ledger"
# 库位公开面（消费方 import 的名字；缺位=断链）
LIB_PUBLIC_NAMES = ("OfficialMarketLedger", "make_ledger_runner", "summarize")
REGISTRY_NAME = "library_relocation.json"

_REGISTRY_CONTRACT = "R15 relocate_library_modules（fn_docs/responsibility.md）"

# 消费方 import 面两形态（同 scan_for_library_misplacement 口径）
_IMPORT_STMT_TMPL = (
    r"(?m)^[ \t]*(?:import[ \t]+(?:[\w.]*\.)?{mod}\b"
    r"|from[ \t]+(?:[\w.]*\.)?{mod}[ \t]+import\b)"
)
_FILENAME_REF_TMPL = r"[\"']{file}[\"']"


def _discover_campaign_root() -> Path:
    """自本文件上溯发现战役根（特征=含 blueprint.md+fn_docs；R20 程序化发现）。"""
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "blueprint.md").is_file() \
                and (candidate / "fn_docs").is_dir():
            return candidate
    raise RuntimeError(
        "战役根发现失败（blueprint.md+fn_docs 特征未命中）: "
        f"自 {Path(__file__).resolve()} 上溯")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _find_consumers(campaign_root: Path, lib_stem: str,
                    lib_file: str) -> list:
    """software 全域找库件消费方（scripts 平铺+其余子树递归，除 __pycache__）。

    返回条目 {"file": 战役根相对路径, "line": 行号, "kind": import语句|文件名引用,
    "snippet": 命中行原文}，按 (file, line) 排序；同文件多形态逐条登记。
    """
    software = campaign_root / "software"
    hosts = sorted(
        p for p in software.rglob("*.py")
        if "__pycache__" not in p.parts and p.name != lib_file
    ) if software.is_dir() else []
    patterns = [
        ("import语句", re.compile(
            _IMPORT_STMT_TMPL.format(mod=re.escape(lib_stem)))),
        ("文件名引用", re.compile(
            _FILENAME_REF_TMPL.format(file=re.escape(lib_file)))),
    ]
    entries = []
    for host in hosts:
        text = host.read_text(encoding="utf-8", errors="replace")
        for kind, pattern in patterns:
            for match in pattern.finditer(text):
                entries.append({
                    "file": host.relative_to(campaign_root).as_posix(),
                    "line": text.count("\n", 0, match.start()) + 1,
                    "kind": kind,
                    "snippet": match.group(0).strip()[:120],
                })
    # 同文件同形态同行去重（import 与 from 各命中一次即两条，保留）
    deduped = {(_e["file"], _e["line"], _e["kind"]): _e for _e in entries}
    return [deduped[k] for k in sorted(deduped)]


def _import_roundtrip(copy_path: Path) -> dict:
    """库位副本 import 回探（按 path 装载，公开名在场即链通；异常=断链）。"""
    try:
        spec = importlib.util.spec_from_file_location(
            "relocated_market_ledger_roundtrip", copy_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001 — 任何装载失败均折为断链裁决
        return {"import_ok": False, "detail": f"副本装载失败: {exc!r}"}
    missing = [name for name in LIB_PUBLIC_NAMES
               if not hasattr(module, name)]
    if missing:
        return {"import_ok": False,
                "detail": f"公开名缺位（断链）: {missing}"}
    return {"import_ok": True,
            "detail": "装载成功，公开名全在场: "
                      + ", ".join(LIB_PUBLIC_NAMES)}


def _postwar_execution(consumers: list, source_rel: str, dest_rel: str) -> dict:
    return {
        "when": "fn-close 期（战后收口，旧树冻结解除后）",
        "registry_only": True,
        "steps": [
            f"rm {dest_rel} && git mv {source_rel} {dest_rel}"
            f"（副本与源逐字节等价，git mv 承接文件历史至库位）",
            f"consumers {len(consumers)} 条逐件改线：import 语句改 "
            f"`from {NEW_IMPORT_MODULE} import …`（fn_work/src 需在 "
            "sys.path）；带引号文件名引用（importlib path 装载）改指向"
            f" {dest_rel}",
            "旧件移出后跑 R15 验收：scripts/ 无无入口库件扫描断言"
            "（scan_for_library_misplacement 返回空）+全量测试绿",
        ],
        "note": "additional_misplaced 若非空，其余无入口库件战后另行裁决"
                "（本注册表不辖），未裁决前不搬移。",
    }


def relocate_library_modules(scripts_dir=None, *, library_dir=None,
                             registry_path=None) -> dict:
    """库件归位编排：扫描旧树→建库位（逐字节副本+回探）→改线注册落盘。

    Args:
        scripts_dir: <战役根>/software/scripts（只读，G17 源件所在）；
            None=自本模块上溯发现战役根后推导。
        library_dir: 库位目录（副本落点 <library_dir>/market_ledger.py）；
            None=本模块所在包目录（fn_work/src/relocate_library_modules）。
        registry_path: 注册表落盘路径；None=<战役根>/fn_work/library_relocation.json。

    Returns:
        裁决 dict：{overall, market_ledger_detected, scan{scanned,misplaced},
        additional_misplaced, library{source,dest,sha256_source,sha256_copy,
        byte_equal,new_import_module,import_ok,import_detail,public_names},
        consumers, registry_path, summary}。overall ⇔ G17 件检出+副本逐字节
        等价+import 回探链通+注册表落盘。

    Raises:
        ValueError: scripts 目录缺失 / G17 源事实核验失败（market_ledger
            未检出为无入口库件或不在场）/ 副本写后 sha256 不等价（断链即失败）。
    """
    scripts = Path(scripts_dir) if scripts_dir is not None else (
        _discover_campaign_root() / "software" / "scripts")
    if not scripts.is_dir():
        raise ValueError(f"scripts 目录不存在或非目录: {scripts}")
    campaign_root = scripts.parent.parent
    library = Path(library_dir) if library_dir is not None \
        else Path(__file__).resolve().parent
    reg_path = Path(registry_path) if registry_path is not None \
        else campaign_root / "fn_work" / REGISTRY_NAME

    # ---- ① 扫描旧树（只读）+ G17 源事实核验 ----
    misplaced = scan_for_library_misplacement(scripts)
    scanned = sorted(p.name for p in scripts.glob("*.py")
                     if p.name != "__init__.py")
    entry = next((e for e in misplaced if e["file"] == LIB_MODULE), None)
    source = scripts / LIB_MODULE
    if entry is None:
        raise ValueError(
            f"G17 源事实核验失败：{LIB_MODULE} 未检出为无入口库件"
            f"（在场={source.is_file()}，扫描清单位={len(misplaced)} 件）——"
            f"源件已被搬走/获得入口标记/失消费者，fail-closed 拒绝归位。")
    additional_misplaced = [e["file"] for e in misplaced
                            if e["file"] != LIB_MODULE]

    # ---- ② 建库位：逐字节复制 + sha256 等价 + import 回探 ----
    copy_path = library / LIB_MODULE
    library.mkdir(parents=True, exist_ok=True)
    copy_path.write_bytes(source.read_bytes())
    sha_source, sha_copy = _sha256(source), _sha256(copy_path)
    byte_equal = sha_source == sha_copy
    if not byte_equal:
        raise ValueError(
            f"库位副本与源 sha256 不等价（断链即失败）: {sha_source} != "
            f"{sha_copy} @ {copy_path}")
    roundtrip = _import_roundtrip(copy_path)
    if not roundtrip["import_ok"]:
        raise ValueError(f"库位副本 import 回探失败（断链即失败）: "
                         f"{roundtrip['detail']}")

    # ---- ③ 改线注册：旧 consumers 清单+新 import 路径，落盘 ----
    consumers = _find_consumers(campaign_root, Path(LIB_MODULE).stem, LIB_MODULE)
    source_rel = source.relative_to(campaign_root).as_posix()
    dest_rel = copy_path.relative_to(campaign_root).as_posix()
    library_record = {
        "module": LIB_MODULE,
        "source": source_rel,
        "dest": dest_rel,
        "sha256_source": sha_source,
        "sha256_copy": sha_copy,
        "byte_equal": True,
        "new_import_module": NEW_IMPORT_MODULE,
        "public_names": list(LIB_PUBLIC_NAMES),
        "import_ok": True,
        "import_detail": roundtrip["detail"],
    }
    overall = True  # 至此全部门内断言已过（fail-closed 先行）
    summary = (f"扫描 {len(scanned)} 件检出无入口库件 {len(misplaced)} 件"
               f"（G17 件 {LIB_MODULE} 在列，消费方 {len(consumers)} 条）；"
               f"库位 {dest_rel} 逐字节副本 sha256 等价+import 回探链通；"
               f"注册表落盘——PASS")
    verdict = {
        "overall": overall,
        "market_ledger_detected": True,
        "scan": {"scanned": len(scanned),
                 "misplaced": [{"file": e["file"],
                                "importers": e["importers"]}
                               for e in misplaced]},
        "additional_misplaced": additional_misplaced,
        "library": library_record,
        "consumers": consumers,
        "summary": summary,
    }
    registry = {
        "contract": _REGISTRY_CONTRACT,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "frozen_tree": True,
        "library": library_record,
        "rewiring": {
            "new_import_module": NEW_IMPORT_MODULE,
            "old_import_forms": [c["snippet"] for c in consumers],
        },
        "consumers": consumers,
        "scan": verdict["scan"],
        "additional_misplaced": additional_misplaced,
        "postwar_execution": _postwar_execution(
            consumers, source_rel, dest_rel),
        "verdict": verdict,
    }
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    reg_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    verdict["registry_path"] = str(reg_path)
    return verdict
