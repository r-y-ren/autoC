# 名录回灌（追加不改旧种子；换血判定法+跨频道线索入 SOP 留痕）
from __future__ import annotations

import re
from pathlib import Path

__all__ = ["CROSS_CHANNEL_LEADS", "TURNOVER_RULE", "register_opponent_pool_seeds"]

# "对手换血"判定法（R29 裁决：写入读数 SOP 留痕的固定文本，确定性渲染）
TURNOVER_RULE = (
    "对手换血判定法：读数窗内对手池若出现「新面孔入池或旧种子掉出」（名录成员集合变动），"
    "则该窗读数判定为对手群体换血，不作自身退化归因；换血窗与非换血窗分段统计，不得混池平均。"
)
# 跨频道线索登记（R29 点名的两条；登记入 SOP 留痕，不入种子定义）
CROSS_CHANNEL_LEADS = (
    "nikital7（Kaggle kernel: 4000x-environment-speedup-kaggriculture）",
    "Nikita Lugovoy（提交件 55440039）",
)
_SEED_LINE = re.compile(r"^-\s*name=(?P<name>.+?)\s*\|\s*score_band=(?P<band>.*?)\s*\|\s*note=(?P<note>.*)$")


def register_opponent_pool_seeds(roster, pool_file, sop_doc):
    """顶层名录并入对手池种子定义（追加不改旧种子）+'对手换血'判定法入 SOP 留痕+跨频道线索登记。错误: 重复/冲突→跳过并记录。

    约束：
    - roster=list[{"name","score_band","note"}]；pool_file/sop_doc=路径（追加写；旧内容原样保留）。
    - 种子行格式：`- name=<name> | score_band=<band> | note=<note>`；判重以 name 为准：
      同名同档→重复，同名异档→冲突，均跳过不写入（不改旧种子）。
    - 返回 {"definition": 更新后定义全文, "record": 留痕文本, "added": [name],
      "skipped": [{"name","reason"}]}；确定性（无时间戳，同输入同输出）。
    """
    pool_path = Path(pool_file)
    sop_path = Path(sop_doc)
    old_text = pool_path.read_text(encoding="utf-8") if pool_path.exists() else ""

    # 旧种子名→档位（仅认种子行；其余行原样保留不算种子）
    known: dict[str, str] = {}
    for line in old_text.splitlines():
        matched = _SEED_LINE.match(line.strip())
        if matched:
            known.setdefault(matched.group("name"), matched.group("band"))

    added: list[str] = []
    skipped: list[dict] = []
    new_lines: list[str] = []
    for item in roster:
        if not isinstance(item, dict):
            skipped.append({"name": None, "reason": "名录项非 dict，跳过"})
            continue
        name = item.get("name")
        name = name.strip() if isinstance(name, str) else ""
        band = item.get("score_band")
        band = band.strip() if isinstance(band, str) else ""
        note = item.get("note")
        note = note.strip() if isinstance(note, str) else ""
        if not name:
            skipped.append({"name": None, "reason": "名录项 name 空，跳过"})
            continue
        if name in known:
            if known[name] == band:
                skipped.append({"name": name, "reason": "重复（同名同档已有种子），跳过"})
            else:
                skipped.append({"name": name, "reason": f"冲突（同名异档：旧={known[name]!r} 新={band!r}），跳过"})
            continue
        known[name] = band
        added.append(name)
        new_lines.append(f"- name={name} | score_band={band} | note={note}")

    # 追加写种子定义（不覆盖旧内容；旧文本为空则补文件头）
    if new_lines:
        body = old_text
        if body and not body.endswith("\n"):
            body += "\n"
        if not body:
            body = "# 对手池种子定义（追加式）\n"
        definition = body + "\n".join(new_lines) + "\n"
    else:
        definition = old_text
    if definition != old_text:
        pool_path.parent.mkdir(parents=True, exist_ok=True)
        pool_path.write_text(definition, encoding="utf-8")

    # SOP 留痕（换血判定法+回灌摘要+跨频道线索；追加写）
    record_lines = ["## R29 对手池回灌留痕", TURNOVER_RULE]
    record_lines.append("种子回灌：" + ("；".join(f"{n} 入池" for n in added) if added else "无新增"))
    record_lines.append(
        "跳过记录：" + ("；".join(f"{s['name'] or '<匿名>'}（{s['reason']}）" for s in skipped) if skipped else "无")
    )
    record_lines.append("跨频道线索登记：" + "；".join(CROSS_CHANNEL_LEADS))
    record = "\n".join(record_lines) + "\n"
    old_sop = sop_path.read_text(encoding="utf-8") if sop_path.exists() else ""
    sop_path.parent.mkdir(parents=True, exist_ok=True)
    sop_path.write_text(old_sop + record, encoding="utf-8")

    return {"definition": definition, "record": record, "added": added, "skipped": skipped}
