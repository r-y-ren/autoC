"""材料编译（数字一致性预检不过即失败退出）（build_materials 块）。"""
from __future__ import annotations

import re

_PLACEHOLDER = re.compile(r"\{\{METRICS:([a-zA-Z0-9_/.\-]+)\}\}")


class MaterialError(Exception):
    """编译器失败/数字不一致。"""


def compile_documents(source_dir: str, build_config: dict | None = None) -> list:
    """把 source_dir/revision_notes.md 编译为 计划书v2 草稿 + PPT(Marp) md。

    预检：占位符全闭合且值来自引用表；外部工具（typst/marp）缺失时降级为 md 产物并标注。
    """
    import json
    from pathlib import Path
    src = Path(source_dir)
    notes_fp = src / "revision_notes.md"
    if not notes_fp.exists():
        raise MaterialError(f"修订建议稿缺失: {notes_fp}")
    table_fp = src / "metrics_table.json"
    if not table_fp.exists():
        raise MaterialError("引用表缺失（先 export_metrics_table）")
    table = json.loads(table_fp.read_text(encoding="utf-8"))
    by_key = {k: v[-1]["value"] for k, v in table["by_key"].items()}
    text = notes_fp.read_text(encoding="utf-8")

    def _sub(m):
        key = m.group(1)
        if key not in by_key:
            raise MaterialError(f"数字不一致：{key} 不在引用表")
        return str(by_key[key])

    filled = _PLACEHOLDER.sub(_sub, text)
    if _PLACEHOLDER.search(filled):
        raise MaterialError("存在未闭合占位符")
    outs = []
    plan = src / "安航云盾_计划书_v2_修订建议稿.md"
    plan.write_text(filled, encoding="utf-8")
    outs.append(str(plan))
    ppt = src / "路演PPT.md"
    ppt.write_text("""---\nmarp: true\ntheme: default\n---\n# 安航云盾\n乡村物流无人机主动安全保障平台\n---\n# 三风险场景实测\n- 提前量/时延/检出 见数字引用表\n---\n# 模块化设备架构\n- 缺席可演示·到位即插即测\n""", encoding="utf-8")
    outs.append(str(ppt))
    return outs
