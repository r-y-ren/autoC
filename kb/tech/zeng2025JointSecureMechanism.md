---
id: zeng2025JointSecureMechanism
name: CNN-LSTM多任务学习的UAV团队FDI攻击联合防护
field: [无人机安全, FDI 攻击检测, 多任务学习]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: CNN+LSTM 共享骨干 + 分层多任务头（检测/定位/补偿一体化）可整体迁移到工业与物联网时序数据的异常检测定位赛题，experience replay 缓解长时训练遗忘的技巧通用
    reuse_cost: 中
  - track: 数模-预测与评估
    edge: 对受扰时序数据同时输出「是否异常/异常部件/偏差面积」的评估框架，可直接用于故障诊断与风险评估类题目的多输出建模
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 植保/巡检无人机队应对链路攻击与故障的团队级安全防护方案（3 架 DJI Tello 真实飞行验证），是申报书安全可信章节的现成技术点
    reuse_cost: 低
sources:
  - paper_title: A Joint Secure Mechanism of Multi-Task Learning for a UAV Team under FDI Attacks
    doi: 10.1109/TMC.2025.3551537
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# CNN-LSTM多任务学习的UAV团队FDI攻击联合防护

## 单行摘要

面向多 UAV 团队上下行链路同时遭受虚假数据注入（FDI）攻击的飞行安全问题，提出 CNN+LSTM 提取团队时空特征、分层多任务学习同时输出攻击检测、受损部件定位与控制补偿的联合安全框架，并用 experience replay 缓解长时训练的知识衰减，在仿真与 3 架 DJI Tello Robomaster TT 真实飞行中验证。

## 方法快照

- 威胁设定：uplink 控制指令与 downlink 状态数据同时被注入伪造数据，攻击可持续、可多机多部件、可绕过传统 BDD——单侧正确信息假设下的经典防御直接失效。
- 时空特征：CNN 挖掘多机空间关联，LSTM 捕捉跨时间步演化，共享特征骨干支撑三个子任务联合训练。
- 分层多任务：检测、定位、补偿以分层结构维持逻辑关联，把原本分散的三件事合并进一个模型。
- 迭代学习：借鉴 RL 的 experience replay，缓解长期训练中的知识遗忘与性能衰减。
- 验证：仿真 + 真实飞行（RTX 3060 训练，3×DJI Tello 演示），评测检测/定位性能、偏差面积与补偿效果，对比六类基线。

## 比赛映射要点

- 黑客松/算法赛：时序传感数据异常检测+定位题（电网、水质、设备监控）可复用其「CNN 空间关联 + LSTM 时序演化 + 多任务头」结构；补偿思想可化为异常下的修复/兜底输出，是超越单纯分类基线的差异点。
- 数模诊断题：多输出（有无故障/故障位置/影响量化）评估框架与偏差面积类指标可直接搬用。
- 双创申报：无人机队安全防护与可信作业段落可引用其真实飞行验证设定，成本低、说服力强。

## 关联概念
- 虚假数据注入攻击（FDI）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zeng2025_多任务学习驱动的UAV团队FDI联合防护`（4 枚举字段承自页 frontmatter）。
- bib 回填：citekey `zeng2025JointSecureMechanism` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性 medium 承自 vault 页自评：含真实飞行验证但未公开训练代码、攻击注入脚本与标注数据，如需引用请以原文复核。
