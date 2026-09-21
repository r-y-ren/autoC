"""bc_track/models 权重证据件归档登记（R12）：注册表条目+战后搬移路径，本批零物理移动（旧树冻结）。

上游: R12（详见 fn_docs/responsibility.md）

实现要点：
- models_dir 全件登记（权重 .py + 训练报告 .json），逐件 {file, size_bytes,
  kind, reason, postwar_dest}；总量以实测字节计（铁律 4：不估数）。
- 证据归档区布局=战役根内 forensics_archive/bc_models/（新定义，fn-close 期
  按注册表逐件 git mv；战役圈禁内，合规 D14）——本函数只产路径，不建目录、
  不搬移、不改旧树一字节。
- 契约"错误: 无"指无业务规则失败；目录不存在/为空属环境结构性缺失，
  仍 fail-closed（ValueError），与 B7"缺失登记"惯例一致处仅限件级：缺件
  不适用（models/ 全件登记，无外部具名清单）。
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["archive_bc_models", "BC_MODELS_POSTWAR_DIR"]

# 证据归档区（战役根相对）：本批定义的战后落位布局，注册表即执行清单
BC_MODELS_POSTWAR_DIR = "forensics_archive/bc_models"

_REASON = ("R12/G14：bc 权重证据件（自动生成物，结论已留痕 metrics/issues），"
           "移证据归档区、不进新结构代码面")


def archive_bc_models(models_dir) -> dict:
    """登记 bc_track/models 证据件到归档注册表（不物理移动）。

    Args:
        models_dir: models 目录路径（<战役根>/software/bc_track/models）；
            须存在且非空，否则环境性 fail-closed。

    Returns:
        dict：
        {"entries": [{file, size_bytes, kind: 权重|报告, reason,
                      postwar_dest}…按文件名排序],
         "total_bytes": 实测字节合计, "weights_bytes": 权重件字节合计,
         "moved": False, "mode": "registry-only"}
        moved 恒 False——本批为登记态，物理搬移属战后 fn-close 期。
    """
    directory = Path(models_dir)
    if not directory.is_dir():
        raise ValueError(
            f"models 目录不存在或非目录: {directory}\n"
            f"排查: 确认传入 <战役根>/software/bc_track/models（R12 证据件所在）。")
    files = sorted(p for p in directory.iterdir() if p.is_file())
    if not files:
        raise ValueError(f"models 目录为空，无证据件可登记: {directory}")

    entries = []
    for path in files:
        suffix = path.suffix.lower()
        kind = "权重" if suffix == ".py" else "报告"
        entries.append({
            "file": path.name,
            "size_bytes": path.stat().st_size,
            "kind": kind,
            "reason": _REASON,
            "postwar_dest": f"{BC_MODELS_POSTWAR_DIR}/{path.name}",
        })

    return {
        "entries": entries,
        "total_bytes": sum(e["size_bytes"] for e in entries),
        "weights_bytes": sum(e["size_bytes"] for e in entries
                             if e["kind"] == "权重"),
        "moved": False,
        "mode": "registry-only",
    }
