"""最小可复算集入库编排：收集 → 预算断言 → 依赖声明 → MANIFEST 落盘 → 裁决。

上游: R19（详见 fn_docs/responsibility.md）

实现要点：
- 编排序：①collect_gate_golden_files（四类清单收集，missing 登记不中断）
  → ②enforce_size_budget（仅对 collected 件，定桩 单件 2 MiB/总量 10 MiB；
  超标 fail-closed=ok=false 且绝不截断）→ ③declare_local_corpus_dependencies
  （以 registry 的 missing 件+fn_docs 扫描渲染声明）→ ④MANIFEST.json 落盘
  （确定性内容：无时钟字段，时间由 JOURNAL/git 记账；path 字段一律战役根
  相对——B7 评审修正：内嵌绝对路径破坏跨机重跑逐字节一致）。
- 盘上 manifest 的 checks 不含 manifest_written 自指字段（B7 评审修正：写盘
  前序列化故恒 false、误导 fresh clone 读者）；该字段仅在返回值裁决 dict
  写盘成功后回填 true。
- 裁决 dict：ok = 收集完成 AND 预算通过 AND manifest/声明落盘；complete =
  missing==0（R19 fresh-clone 口径——本机缺 gitignored 语料时 complete=false
  但 ok=true，缺失逐件带 backfill，主力机重跑本函数即补齐）。
- 三叶可注入（collector/budget_checker/dependency_declarer，测试用）；
  minimal_set_manifest 兼容旧桩签名首位=类别列表（None=四类全收）。
"""

from __future__ import annotations

import json
from pathlib import Path

from package_minimal_repro_set.collect_gate_golden_files import (
    CATEGORY_ORDER,
    collect_gate_golden_files,
)
from package_minimal_repro_set.declare_local_corpus_dependencies import (
    declare_local_corpus_dependencies,
)
from package_minimal_repro_set.enforce_size_budget import (
    DEFAULT_BUDGET,
    SizeBudgetExceeded,
    enforce_size_budget,
)
from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["package_minimal_repro_set"]

MANIFEST_SCHEMA = "minimal-repro-set/1.0"
MANIFEST_NAME = "MANIFEST.json"


def _campaign_rel(path_value, campaign_root: Path):
    """path 字段战役根相对化（B7 评审修正）：跨机重跑逐字节一致。

    None 透传；战役根内的绝对/相对路径转 str(Path(...).relative_to(campaign_root))；
    根外路径（异常注入等）原样保留，不冒充相对。
    """
    if path_value is None:
        return None
    path = Path(path_value)
    try:
        return str(path.relative_to(campaign_root))
    except ValueError:
        return str(path)


def package_minimal_repro_set(minimal_set_manifest=None, budget=None, *,
                              campaign_root=None, output_root=None,
                              collector=None, budget_checker=None,
                              dependency_declarer=None) -> dict:
    """编排三叶并落 MANIFEST，返回 fail-closed 裁决 dict。

    Args:
        minimal_set_manifest: 类别列表（None=四类全收；列表项须在四类清单内）。
        budget: 预算 dict（None=enforce_size_budget 定桩常量）。
        campaign_root: 战役根；None=shared.discover_campaign_roots 发现。
        output_root: 收集落点；None=<战役根>/fn_work/minimal_repro_set。
        collector/budget_checker/dependency_declarer: 三叶注入（测试）。

    Returns:
        裁决 dict：{ok, complete, checks, counts, budget, manifest_path,
        registry, declaration}——ok=false 即失败（预算超标/落盘失败），缺失件
        只降 complete 不降 ok（登记回填通道，不冒充齐备）。
    """
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    campaign_root = Path(campaign_root)
    if output_root is None:
        output_root = campaign_root / "fn_work" / "minimal_repro_set"
    output_root = Path(output_root)

    if collector is None:
        collector = collect_gate_golden_files
    if budget_checker is None:
        budget_checker = enforce_size_budget
    if dependency_declarer is None:
        dependency_declarer = declare_local_corpus_dependencies

    # ① 收集（missing 登记不中断）
    file_set, registry = collector(minimal_set_manifest, campaign_root=campaign_root,
                                   dest_dir=output_root)
    collected_n = len(file_set)
    missing = [r for r in registry if r.get("status") == "missing"]
    total_bytes = sum(int(r["size"]) for r in file_set)

    # ② 预算断言（仅 collected 件；超标 fail-closed 不截断）
    budget_violations: list = []
    budget_ok = True
    try:
        budget_checker(file_set, budget)
    except SizeBudgetExceeded as exc:
        budget_ok = False
        budget_violations = list(exc.violations)

    # ③ 非入库语料依赖声明（missing 件回填通道入声明）
    declaration = dependency_declarer(
        {"missing_files": [
            {"category": r["category"], "source_path": r["source_path"],
             "backfill": r["backfill"]} for r in missing]},
        campaign_root=campaign_root,
        output_path=output_root / "LOCAL_CORPUS_DEPENDENCIES.md")

    # ④ MANIFEST 落盘（确定性：固定序、无时钟字段、path 字段战役根相对）
    manifest_path = output_root / MANIFEST_NAME
    checks = {
        "collect": {"ok": True, "collected": collected_n, "missing": len(missing)},
        "size_budget": {"ok": budget_ok, "total_bytes": total_bytes,
                        "violations": budget_violations},
        # manifest_written 为自指字段（写盘前序列化故恒 false、误导 fresh clone
        # 读者）——不入盘上 checks，仅在返回值裁决 dict 写盘成功后回填 true。
        "declaration_written": bool(declaration.get("written")),
    }
    verdict = {
        "schema": MANIFEST_SCHEMA,
        "category_order": list(minimal_set_manifest) if minimal_set_manifest
        else list(CATEGORY_ORDER),
        "counts": {"collected": collected_n, "missing": len(missing),
                   "total_bytes": total_bytes},
        "budget": {**DEFAULT_BUDGET, **(budget or {})},
        "verdict": {},
        "declaration": {"path": _campaign_rel(declaration.get("output_path"),
                                              campaign_root),
                        "written": bool(declaration.get("written"))},
        "registry": registry,
    }
    verdict["verdict"]["complete"] = len(missing) == 0
    verdict["verdict"]["checks"] = checks
    # 落盘前先按已知检查算 ok（manifest_written 未知不计入）——预算/声明失败时
    # 盘上 verdict 即 False；写盘成功不改变结论，写盘失败则无盘上件、终算 False。
    pre_ok = (checks["collect"]["ok"] and checks["size_budget"]["ok"]
              and checks["declaration_written"])
    verdict["verdict"]["ok"] = pre_ok
    try:
        output_root.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(verdict, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        # 写盘后回填：checks 已随 verdict 序列化落盘，此处仅改内存对象——
        # 返回值裁决 dict 见 manifest_written=true，盘上 manifest 恒无该键。
        checks["manifest_written"] = True
    except OSError:
        checks["manifest_written"] = False

    # 落盘完成后终算 ok（manifest_written 计入，fail-closed）
    final_ok = pre_ok and checks["manifest_written"]
    verdict["verdict"]["ok"] = final_ok

    return {
        "ok": final_ok,
        "complete": verdict["verdict"]["complete"],
        "checks": checks,
        "counts": verdict["counts"],
        "budget": verdict["budget"],
        "manifest_path": str(manifest_path),
        "registry": registry,
        "declaration": verdict["declaration"],
    }
