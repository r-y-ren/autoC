# R29 研究轨指挥（只挖不改：产物=报告+登记，绝不落代码改动）
from __future__ import annotations

from pathlib import Path

from run_r29_mining.check_reference_map import check_reference_map
from run_r29_mining.register_opponent_pool_seeds import register_opponent_pool_seeds

__all__ = ["run_r29_mining"]

# 报告文件名（analyses/31-*.md 判据面；确定性固定名，无时间戳）
_REPORT_NAME = "31-r29-reference-map.md"
_MAP_FIELDS = ("evidence", "hook", "expected_signal", "risk", "source_url", "fetched_date")


def run_r29_mining(corpus, out_dir):
    """编排研究轮：候选甄选→映射清单起草（四字段）→check_reference_map 过检→报告落 analyses/31+INDEX 登记→register_opponent_pool_seeds 回灌。不实施代码改动。错误: 检查不过→打回（不落盘）。

    约束：
    - corpus=dict：{"candidates": 甄选面 list[dict]（六字段+可选 selected=False 剔除）、
      "roster": 名录 list[{"name","score_band","note"}]、"index_doc"/"pool_file"/"sop_doc": 路径（可缺省）}。
    - 甄选=剔除 selected=False+按 (source_url, hook) 保序去重；起草=逐条投影六字段（缺项留空交 lint 报）。
    - index_doc 缺省=out_dir/references/INDEX.md（URL 在册比对面兼登记面）；
      pool_file/sop_doc 缺省=out_dir 下两件（追加写）。
    - 过检前零落盘：lint 不过→返回 {"pass": False, "missing": …}，报告/INDEX/种子/SOP 一概不动。
    """
    out = Path(out_dir)
    if not isinstance(corpus, dict):
        return {"pass": False, "missing": [{"entry": None, "field": "corpus", "reason": "语料非 dict"}],
                "report_path": None, "index_path": None, "registry": None}
    candidates = corpus.get("candidates")
    if not isinstance(candidates, list):
        return {"pass": False, "missing": [{"entry": None, "field": "corpus", "reason": "candidates 缺失或非 list"}],
                "report_path": None, "index_path": None, "registry": None}
    roster = corpus.get("roster")
    roster = roster if isinstance(roster, list) else []

    # —— 候选甄选（确定性：显式剔除+同源同挂接面保序去重）——
    selected = []
    seen: set[tuple] = set()
    for cand in candidates:
        if isinstance(cand, dict) and cand.get("selected") is False:
            continue
        key = (
            cand.get("source_url") if isinstance(cand, dict) else None,
            cand.get("hook") if isinstance(cand, dict) else None,
        )
        if key in seen:
            continue
        seen.add(key)
        if isinstance(cand, dict):
            selected.append({name: cand.get(name, "") for name in _MAP_FIELDS})
        else:
            selected.append(cand)  # 非 dict 原样透传，交 lint 格式门 fail

    # —— 过检（fail-closed：不过即打回，全程零落盘）——
    index_path = Path(corpus["index_doc"]) if corpus.get("index_doc") else out / "references" / "INDEX.md"
    check = check_reference_map(selected, index_doc=index_path)
    if not check["pass"]:
        return {"pass": False, "missing": check["missing"],
                "report_path": None, "index_path": None, "registry": None}

    # —— 报告落 analyses/31-*.md（确定性渲染：无时间戳、逐格转义竖线）——
    report_path = out / "analyses" / _REPORT_NAME
    lines = ["# 31 R29 全网源码对标映射清单（只挖不改）", ""]
    lines.append("交付面=映射清单报告+references INDEX 登记+对手池种子/SOP 回灌留痕；本工具不实施任何代码改动。")
    lines.append("")
    lines.append(f"映射条目数：{len(selected)}；名录回灌对象：{len(roster)}。")
    lines.append("")
    lines.append("## 映射清单（逐条四字段：证据[URL+行级]/挂接面/预期信号/禁区冲突度）")
    lines.append("")
    lines.append("| # | 证据[URL+行级] | 挂接面 | 预期信号 | 禁区冲突度 | 来源 URL | 抓取日期 |")
    lines.append("|---|---|---|---|---|---|---|")
    for i, entry in enumerate(selected, 1):
        cells = []
        for name in _MAP_FIELDS:
            value = entry.get(name, "") if isinstance(entry, dict) else ""
            value = "" if value is None else str(value)
            cells.append(value.replace("|", "\\|").replace("\n", " ").strip())
        lines.append("| " + " | ".join([str(i), *cells]) + " |")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # —— references INDEX 登记（追加一行登记本报告；不改旧行）——
    urls: list[str] = []
    dates: list[str] = []
    for entry in selected:
        url = str(entry.get("source_url", "") or "").strip()
        date = str(entry.get("fetched_date", "") or "").strip()
        if url and url not in urls:
            urls.append(url)
        if date and date not in dates:
            dates.append(date)
    row = (
        "| ../analyses/" + _REPORT_NAME
        + " | " + "、".join(urls)
        + " | " + "、".join(dates)
        + " | R29 映射清单报告（只挖不改） | run_r29_mining 回灌登记 |"
    )
    old_index = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    index_body = old_index
    if index_body and not index_body.endswith("\n"):
        index_body += "\n"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(index_body + row + "\n", encoding="utf-8")

    # —— 名录/SOP 回灌（追加不改旧种子；重复/冲突跳过并记录）——
    pool_file = Path(corpus["pool_file"]) if corpus.get("pool_file") else out / "opponent_pool_seeds.md"
    sop_doc = Path(corpus["sop_doc"]) if corpus.get("sop_doc") else out / "readout_sop.md"
    registry = register_opponent_pool_seeds(roster, pool_file, sop_doc)

    return {
        "pass": True,
        "missing": [],
        "report_path": str(report_path),
        "index_path": str(index_path),
        "registry": registry,
    }
