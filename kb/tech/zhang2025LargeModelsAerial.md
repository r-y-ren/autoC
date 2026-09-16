---
id: zhang2025LargeModelsAerial
name: 空中边缘大模型的边云三流协同演化
field: [边缘智能, 大模型, 边云协同]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 带宽受限下边云分工的建模样板——任务分配比例、残差上传比例、量化比特三变量联合决策，可迁移到端侧小模型+云端大模型兜底的低成本推理管线设计（如树莓派/手机端部署演示）
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业低空巡检视觉方案的技术支撑点——农田网络带宽受限，机载小模型常态执行、云端大模型负责难样本与模型持续更新（JSAC 2025），契合无人机+AI 双创叙事
    reuse_cost: 低
sources:
  - paper_title: "Large Models for Aerial Edges：An Edge-Cloud Model Evolution and Communication Paradigm"
    doi: 10.1109/JSAC.2024.3460078
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 空中边缘大模型的边云三流协同演化

## 单行摘要

提出空地一体化边云模型演化框架：用特征流、残差数据流与模型流三条传输组织 UAV 边缘小模型与云端大模型的协同，联合优化边云任务分配比例、残差量化比特与上下行带宽，以整体 joint mAP 最大化为目标——把研究问题从「任务是否卸载」推进到「模型能力如何在边云间随通信条件动态演化」。

## 方法快照

- 系统组成：前端 UAV（采集帧 + 机载小模型）与地面云服务器（大模型推理 + 边缘模型更新）；主分析单位为单 UAV，可推广多机。
- 三流建模：上行含特征流与残差数据流（残差量化位数决定云端可恢复质量），下行模型流用于更新边缘模型，三流共享带宽、相互耦合。
- 目标函数：整体 mAP 表达为云端 mAP、边缘 mAP 与任务分配比例的函数，用 g(·)、h(·) 刻画数据流与模型流对性能的影响。
- 求解路径：联合 mAP 最大化拆为数据流设计与特征流/模型流设计两个子问题；推导整体 mAP 闭式下界并在此之上设计求解流程。
- 关键洞见：与传统边云推理卸载不同，模型更新被显式纳入系统设计；指标从时延/能耗转向模型效果（mAP）。
- 验证：数值仿真，实验数据复用既有结果或文献拟合（涉及 CIFAR10），部分资产公开，未给平台栈；更适合取其系统思路与资源分配结论而非复现基线。

## 比赛映射要点

- 黑客松算法赛：端云分工三变量（任务比例/残差比例/量化比特）的权衡框架可直接用于带宽受限演示场景的推理管线调参叙事；相比「全跑本地」或「全上云」的朴素方案有明确差异化。
- 双创申报：智慧农业低空巡检是「无人机+大模型」叙事的自然落点——农田 4G/5G 覆盖弱、机载算力有限，边云演化框架恰好回应「模型如何在现场持续变强」这一评审追问。

## 关联概念
- 空中边缘大模型前沿
- 边云模型协同

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhang2025_空中边缘大模型的边云协同演化`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `zhang2025LargeModelsAerial` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。**留痕**：bib 原标题含 ASCII 冒号（`Large Models for Aerial Edges: An ...`），按前波 YAML 约定改全角冒号写入 paper_title。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/borrowed_from_prior_work/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
