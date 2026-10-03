"""组装计划书逐节修订建议+可粘贴段落（占位符带 metrics 键）（build_materials 块）。"""
from __future__ import annotations

import re

from build_materials.export_metrics_table import MaterialError

_PLACEHOLDER = re.compile(r"\{\{METRICS:([a-zA-Z0-9_/.\-]+)\}\}")

_TEMPLATE = """# 安航云盾 计划书修订建议（AI 辅助草稿，团队消化改写用）

> 人机分工记录：本稿由 AI 辅助生成（fn-ladder B11），采纳进正式计划书时须团队独立改写；
> 数字占位符（METRICS:键 形式，双花括号包裹）由 export_metrics_table 的实测值替换——材料数字唯一来源。

## 4.2 渐进风险预测与突发故障识别——修订建议
- 原文：保序回归校准概率。
- 修订：保序回归校准 + 共形预测区间（90% 有限样本覆盖率）；实测覆盖率
  {{METRICS:lowbat_headwind/conformal_coverage}}（设计目标 0.90）。
- 可粘贴段落：对渐进风险，系统输出未来 1/3/5/10 秒进入危险状态的概率，并经共形校准层
  包装为带统计保证的区间；提前量实测 P10={{METRICS:lowbat_headwind/lead_p10_s}} 秒
  （中位数 {{METRICS:lowbat_headwind/lead_median_s}} 秒，达标比例
  {{METRICS:lowbat_headwind/lead_hit_rate}}）。

## 4.1/5.1 链路一致性检测（DroneMA 式）——修订建议
- 可粘贴段落：链路健康度在协议层指标外增加 RSSI-距离一致性证据；链路退化场景实测
  检出 {{METRICS:link_degrade/detected}}、正常段误报 {{METRICS:link_degrade/false_alarms}} 次。

## 7.1/7.4 测试验证与指标——修订建议
- 电机故障确认时延 P90 实测 {{METRICS:motor_fail/confirm_p90_s}} 秒（设计目标 ≤0.2 秒）；
  类型正确率 {{METRICS:motor_fail/type_accuracy}}。
- 频谱站模块化实证：拔除设备全功能可演示（回放模式），接入后同管线实采——
  sdr_check 自检 {{METRICS:sdr_check/pass}}。
"""


def draft_revision_notes(metrics_table: dict, frontier_doc: str) -> str:
    """metrics_table: export_metrics_table 产物；frontier_doc: 补强方案路径（留档引用）。"""
    keys = set(metrics_table.get("keys", []))
    out = _TEMPLATE.replace("{{FRONTIER_DOC}}", str(frontier_doc))
    missing = sorted(m.group(1) for m in _PLACEHOLDER.finditer(out)
                     if m.group(1) not in keys)
    if missing:
        raise MaterialError(f"引用键缺失（先跑 eval 产分片）: {missing}")
    return out
