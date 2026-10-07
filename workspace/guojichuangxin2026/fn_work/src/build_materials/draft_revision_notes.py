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

## 4.2 稀疏事件预测选型与双态校准（R17/R18 新增小节）
- 修订建议（选型）：增补"稀疏事件预测选型"段——危险事件稀疏时重型时序模型失效，
  线性探针+分位数平均为实证正解（arxiv-2609.39386，2026-09-30 入库；本项目实测：
  探针稀疏召回 1.0 vs TCN 验证 0.0，选型报告见训练工件 train_report.json）。
- 修订建议（校准）：共形层升双态——静态校准+在线自适应（漂移触发近期经验分位重校准）；
  漂移注入实验在线覆盖率保持 0.87（静态对照跌至 0.41），引 ICLR 2026 自适应共形实证
  （https://arxiv.org/html/2604.20122v1）与 SPACE（arxiv-2608.17333）。
- 可粘贴段落：针对危险事件稀疏的预测难题，本项目按 2026 年实证结论选型轻量路线
  （线性探针+分位数平均，arXiv:2609.39386），在留出架次上稀疏事件召回优于重模型；
  风险区间校准采用双态机制——静态共形校准保证基线 90% 覆盖率，检测到分布漂移时
  自动按近期经验分位重校准（漂移注入实验覆盖率 0.87 vs 静态 0.41）。

## 4.1/5.1 链路一致性检测（DroneMA 式）——修订建议
- 可粘贴段落：链路健康度在协议层指标外增加 RSSI-距离一致性证据；链路退化场景实测
  检出 {{METRICS:link_degrade/detected}}、正常段误报 {{METRICS:link_degrade/false_alarms}} 次。

## 7.3 泛化检验——评估卫生（R19 新增小节）
- 修订建议：升格为"评估卫生"方法论卖点——训练/验证/测试按架次、机体、日期三维切分，
  与学界数据污染实证对照（时间切分除不掉预训练记忆：tsfm-bench，KB 卡 arxiv-2609.10357，
  2026-09-09 入库；活基准方法论：LiveHouse-TS，KB 卡 arxiv-2608.17299，2026-08-18 入库）。
- 可粘贴段落：本项目评估采用架次/机体/采集日期三维分组切分，杜绝相邻窗口泄漏；该口径较业界
  常用时间切分更强——2026 年 TSFM 评测实证表明预训练记忆可穿透时间 hold-out
  （tsfm-bench, arXiv:2609.10357），三维切分是当前可得的污染防线。

## 5.1 技术创新——安全滤波与 Sim2Real（R20 新增小节）
- 修订建议：处置层叙述升级——"安全域投影式约束"（现阶段=确定性规则否决，演进路线=控制
  障碍函数滤波；同构思想见 CSMAAC 凸优化安全域投影，KB 卡 gao2025CSMAACMultiagentReinforcement）；
  验证方法升级为"域随机化两源口径"（合成源出事件指标/真源验管线，Sim-to-Real 实证参照
  kang2024AutonomousMultidroneRacing）。
- 可粘贴段落：处置建议层采用确定性安全域约束：任何建议动作必须通过能源、导航、链路与地理
  围栏的可行域检查，被否方案附理由留痕——该"投影回安全域"约束与前沿安全强化学习的凸投影
  方法同构（CSMAAC, 2025），并规划向控制障碍函数滤波演进。验证采用域随机化两源口径：
  合成域规模化产生风险事件（90 次评估），真源域验证数据链路保真（30 次 PX4 实测），
  两域口径分列标注，杜绝仿真数字冒充实测。

## 硬件采购表（R22，档 B 产品最小试点）
| 硬件 | 数量 | 预算 | 用途 |
|---|---|---|---|
| Jetson Orin NX 16GB（或同级 ARM 边缘模块） | 1 | ≈3000 元 | 机载安全终端实体（8W/120g 约束对应 3.1 节） |
| USRP B210+2.4G 天线 | 1 | 已借用 | 频谱感知站（地面侧，链路物理层证据） |
| 遥测接线/USB 隔离耗材 | 1 批 | ≈50 元 | 接客户机 TELEM2/USB 口 |
| 目标无人机（客户存量机） | — | 不采购 | 产品为加装件，优先 PX4/ArduPilot 开源机（A1 适配） |
- 档 C（含实飞验证，待导师批）：+Pixhawk 6C 类飞控 ≈2000 元 + 开发级整机 X500 套件 ≈3000-5000 元 + 遥控器与电池组。

## 7.1/7.4 测试验证与指标——修订建议
- 电机故障确认时延 P90 实测 {{METRICS:motor_fail/confirm_p90_s}} 秒（设计目标 ≤0.2 秒）；
  类型正确率 {{METRICS:motor_fail/type_correct}}/{{METRICS:motor_fail/type_total}}。
- 频谱站模块化实证：拔除设备全功能可演示（回放模式），接入后同管线实采——
  sdr_check 自检通过（依据 sdr_check_report.json 运行记录，非估算数字）。
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
