# 映射清单 lint（R29 验收判据：四字段齐+来源 URL 在册+抓取日期在场+禁区标注齐）
from __future__ import annotations

import json
from pathlib import Path

from shared.discover_campaign_roots import RootDiscoveryError, discover_campaign_roots

__all__ = ["ALLOWED_RISK", "check_reference_map"]

# 禁区冲突度取值域（契约钉死；越界即 fail）
ALLOWED_RISK = frozenset({"无", "低", "中", "高", "禁区同族"})
# 四字段（逐条非空判据）与全字段（映射清单条目形状）
_FOUR_FIELDS = ("evidence", "hook", "expected_signal", "risk")
_ALL_FIELDS = ("evidence", "hook", "expected_signal", "risk", "source_url", "fetched_date")
# markdown 表头别名（归一化后→字段名；表头不可识别即格式 fail）
_HEADER_ALIASES = {
    "evidence": "evidence", "证据": "evidence",
    "hook": "hook", "挂接面": "hook",
    "expectedsignal": "expected_signal", "预期信号": "expected_signal",
    "risk": "risk", "禁区冲突度": "risk",
    "sourceurl": "source_url", "来源url": "source_url", "url": "source_url",
    "fetcheddate": "fetched_date", "抓取日期": "fetched_date",
}
_FORMAT_REASON = "映射清单格式不可解析（接受 list[dict] / JSON list / markdown 表）"


def check_reference_map(mapping, index_doc=None):
    """四字段非空+来源 URL 在 INDEX 在册+抓取日期在场+禁区冲突度∈{无,低,中,高,禁区同族}；输出缺项清单。错误: 格式不可解析→fail。

    约束：
    - mapping 主格式=list[{"evidence","hook","expected_signal","risk","source_url","fetched_date"}]，
      亦接受 JSON list 串与 markdown 表（表头认英文字段名/中文别名）；非 str 字段值按空缺计（fail-closed）。
    - index_doc=references INDEX 路径；缺省=战役根 fn_docs/hybrid/references/INDEX.md
      （shared.discover_campaign_roots 程序化发现，R20 不拼字面战役路径）。URL 在册=字符串包含比对。
    - 输出 {"pass": bool, "missing": [{"entry": int|None, "field": str, "reason": str}]}；
      格式不可解析/INDEX 不可读一律 fail（不猜、不抛、不半通过）。
    """
    missing: list[dict] = []
    # —— 解析（list 主格式 / JSON 串 / markdown 表）——
    entries = None
    if isinstance(mapping, list):
        entries = mapping
    elif isinstance(mapping, str):
        text = mapping.strip()
        if not text:
            missing.append({"entry": None, "field": "format", "reason": _FORMAT_REASON})
            return {"pass": False, "missing": missing}
        if text[0] in "[{":
            try:
                loaded = json.loads(text)
            except ValueError:
                loaded = None
            if isinstance(loaded, list):
                entries = loaded
            else:
                missing.append({"entry": None, "field": "format", "reason": _FORMAT_REASON})
                return {"pass": False, "missing": missing}
        else:
            rows = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
            header = []
            if rows:
                cells = [c.strip().lower().replace(" ", "").replace("_", "") for c in rows[0].strip().strip("|").split("|")]
                header = [_HEADER_ALIASES.get(c) for c in cells]
            if not rows or not any(header):
                missing.append({"entry": None, "field": "format", "reason": _FORMAT_REASON})
                return {"pass": False, "missing": missing}
            entries = []
            for row in rows[1:]:
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                if cells and all(c.strip(":").strip("-") == "" for c in cells):
                    continue  # 表头分隔行
                item = {}
                for idx, name in enumerate(header):
                    if name is not None and name not in item:
                        item[name] = cells[idx] if idx < len(cells) else ""
                entries.append(item)
    else:
        missing.append({"entry": None, "field": "format", "reason": _FORMAT_REASON})
        return {"pass": False, "missing": missing}

    if not all(isinstance(e, dict) for e in entries):
        missing.append({"entry": None, "field": "format", "reason": _FORMAT_REASON})
        return {"pass": False, "missing": missing}

    # —— INDEX 在册比对面（不可读→fail-closed，即使清单为空也不放行）——
    if index_doc is None:
        try:
            index_path = Path(discover_campaign_roots()["campaign_root"]) / "fn_docs" / "hybrid" / "references" / "INDEX.md"
        except RootDiscoveryError:
            index_path = None
    else:
        index_path = Path(index_doc)
    try:
        index_text = index_path.read_text(encoding="utf-8") if index_path is not None else None
    except OSError:
        index_text = None
    if index_text is None:
        missing.append({"entry": None, "field": "index_doc", "reason": "references INDEX 不可读（无法核验来源 URL 在册）"})
        return {"pass": False, "missing": missing}

    # —— 逐条校验（顺序：四字段→禁区取值→来源 URL→抓取日期）——
    for i, entry in enumerate(entries):
        values = {}
        for name in _ALL_FIELDS:
            value = entry.get(name)
            values[name] = value.strip() if isinstance(value, str) else ""
        for name in _FOUR_FIELDS:
            if not values[name]:
                missing.append({"entry": i, "field": name, "reason": "四字段缺项（证据/挂接面/预期信号/禁区冲突度须齐）"})
        if values["risk"] and values["risk"] not in ALLOWED_RISK:
            missing.append({"entry": i, "field": "risk", "reason": "禁区冲突度取值非法：" + values["risk"]})
        if not values["source_url"]:
            missing.append({"entry": i, "field": "source_url", "reason": "来源 URL 缺项"})
        elif values["source_url"] not in index_text:
            missing.append({"entry": i, "field": "source_url", "reason": "来源 URL 不在 references INDEX 在册"})
        if not values["fetched_date"]:
            missing.append({"entry": i, "field": "fetched_date", "reason": "抓取日期缺项"})
    return {"pass": not missing, "missing": missing}
