---
id: zhou2025VerDTVersatileDigital
name: VerDT：工业 CPS UAV 物流的多功能双数字孪生框架
field: [数字孪生, 工业 CPS, UAV 物流]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: DJI FlyCart-30 真机数据采集加硬件在环双重验证，作低空智慧物流/工业无人机配送申报项目的技术方案与可行性证据链，可信度高于纯仿真文献
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 真实采集数据经 GAN 扩充再进 Gazebo/ROS 虚拟物流空间的高保真仿真构建流程，可直接作无人机/机器人类黑客松搭建赛题环境的工程模板
    reuse_cost: 中
  - track: Kaggle-竞赛
    edge: 真实 UAV 图像经 GAN/CNN 扩充支撑孪生环境构建的思路，可迁移到小样本图像赛题的数据增强环节作为差异化点
    reuse_cost: 中
sources:
  - paper_title: VerDT：A Versatile Digital Twins Framework for UAVs-based Industrial Cyber-Physical Systems
    doi: 10.1109/TMC.2025.3567284
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# VerDT：工业 CPS UAV 物流的多功能双数字孪生框架

## 单行摘要

面向工业 CPS 中的 UAV 智能物流提出 VerDT 多功能数字孪生框架：边缘侧资源调度 twin（DT_RS）与路径规划 twin（DT_PP）协同分工，用真实 DJI 物流无人机采集环境状态并以 GAN 扩充构建高保真虚拟物流空间，经 Gazebo + ROS 硬件在环验证降低分发时延、提高成功率。

## 方法快照

- 双孪生分解：DT_RS 负责资源协同组织，DT_PP 在调度结果上导出低时延低能耗路径；标题强调 versatile，正文真正的结构核心即 DT_RS + DT_PP 双孪生协同（vault 页自评指出的标题与正文偏差）。
- 数据链路：真实 DJI 物流 UAV（FlyCart-30、搭载 Manifold 的机载电脑、风速/深度视觉/相机/超声传感器）采集速度、姿态、风速与建筑信息；GAN 与 CNN 扩充图像与内容数据，增强虚拟环境构建精度。
- 虚拟环境与验证：Gazebo + ROS 构建物流孪生空间承载仿真，硬件在环闭环验证；指标为分发时延、成功率、能耗与拥塞下鲁棒性。
- 定位对比：与只做物流调度的工作相比把路径规划 twin 单独抽出；与只做虚拟映射的 DT 工作相比强调双 twin 决策功能；与传统物流仿真相比引入真实数据采集与硬件在环闭环；未说明开源，复现性 medium。

## 比赛映射要点

- 双创申报：仿真 + 真机原型双验证是申报书可行性章节的强证据形态，可直接借鉴其「物理层-采集层-孪生层-虚拟层」四层架构叙事。
- 黑客松/算法赛：赛题环境搭建可复用「真实数据 → GAN 扩充 → Gazebo/ROS 虚拟空间」流程，快速构建可复现的仿真赛道。
- 数据类竞赛：小样本真实采集数据 + 生成式扩充的组合是图像/感知类赛题的通用增强手段。

## 关联概念（vault 概念页折叠于此，不独立成卡）

- **双数字孪生协同**：把不同职能的数字孪生分拆成多个相互协作的 twin（如一个负责资源调度、另一个负责路径规划或执行控制），把不同时间尺度和不同优化对象拆开处理，使数字孪生更像边缘决策系统而非单纯可视化镜像；语料中代表论文即本卡 VerDT 与姊妹篇 HaDT（同样以调度 twin + 路径 twin 协同支撑物流执行）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2025_VerDT工业CPS多功能数字孪生物流框架`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）；枢纽概念页 `双数字孪生协同.md` 已折叠进「关联概念」节。
- bib 回填：citekey `zhou2025VerDTVersatileDigital` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）；bib 标题原文含 ASCII 冒号（VerDT 后接冒号空格），按 YAML 纪律改全角冒号写入 sources.paper_title。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation+prototype、Gazebo/ROS、DJI 硬件、复现性 medium、artifact 未知）承自 vault 页自评，如需引用请以论文原文复核。
