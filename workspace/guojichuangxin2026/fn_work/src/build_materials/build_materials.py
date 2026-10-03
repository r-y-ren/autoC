"""材料构建总入口：汇总分片→引用表+修订建议+编译（build_materials 块）。"""
from __future__ import annotations


def build_materials(run_dirs: list, materials_config: dict | None = None) -> dict:
    """三步：export_metrics_table→draft_revision_notes→compile_documents；产出路径清单。"""
    import json
    from pathlib import Path
    from build_materials.compile_documents import MaterialError, compile_documents
    from build_materials.draft_revision_notes import draft_revision_notes
    from build_materials.export_metrics_table import export_metrics_table

    cfg = materials_config or {}
    work = Path(cfg.get("work_dir", "materials"))
    work.mkdir(parents=True, exist_ok=True)
    table = export_metrics_table(run_dirs)
    (work / "metrics_table.json").write_text(
        json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    notes = draft_revision_notes(table, cfg.get("frontier_doc", "strategy/frontier-tech.md"))
    (work / "revision_notes.md").write_text(notes, encoding="utf-8")
    outs = compile_documents(str(work), cfg)
    return {"metrics_table": str(work / "metrics_table.json"),
            "revision_notes": str(work / "revision_notes.md"), "compiled": outs,
            "n_runs": table["n_runs"]}
