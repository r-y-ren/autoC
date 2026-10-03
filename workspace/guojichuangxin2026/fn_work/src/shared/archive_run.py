"""运行目录整体归档 fn_docs/results（只拷不移，同名加序号，清单回写）（shared 块）。"""
from __future__ import annotations

import json
import shutil
from pathlib import Path


def archive_run(run_dir, archive_root: str = "fn_docs/results") -> str:
    """归档 = 完整拷贝（原件留工程运行区）；manifest 回写 archived_to。"""
    src = Path(run_dir)
    if not src.is_dir():
        raise FileNotFoundError(f"运行目录不存在: {src}")
    scenario = src.parent.name
    dest_root = Path(archive_root) / scenario
    dest_root.mkdir(parents=True, exist_ok=True)
    dest, n = dest_root / src.name, 2
    while dest.exists():
        dest = dest_root / f"{src.name}+{n}"
        n += 1
    shutil.copytree(src, dest)
    man = dest / "manifest.json"
    if man.exists():
        try:
            m = json.loads(man.read_text(encoding="utf-8"))
        except Exception:
            m = {}
        m["archived_to"] = str(dest)
        man.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    return str(dest)
