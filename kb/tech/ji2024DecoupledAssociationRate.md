---
id: ji2024DecoupledAssociationRate
name: RSMA 解耦关联的 UAV 蜂窝 MADRL 优化
field: [UAV 辅助蜂窝网络, 速率分裂多址, 多智能体强化学习]
published: 2024-01-01
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
    edge: 上下行解耦关联与速率分裂的联合接入问题写成鲁棒 POMDP 后用 CTDE 求解，改进的 clip-and-count PPO（内在奖励 + 改进裁剪）可直接移植到多智能体资源分配/接入调度类赛题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: UAV 基站应急补盲与偏远农田联网场景中，上下行解耦与 RSMA 干扰管理是频谱效率与组播覆盖论证的技术亮点
    reuse_cost: 低
sources:
  - paper_title: "Decoupled Association With Rate Splitting Multiple Access in UAV-Assisted Cellular Networks Using Multi-Agent Deep Reinforcement Learning"
    doi: 10.1109/TMC.2023.3256404
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# RSMA 解耦关联的 UAV 蜂窝 MADRL 优化

## 单行摘要

把全双工多 UAV 蜂窝网络中的上下行解耦关联、RSMA 波束赋形与公共速率分配统一建模为带回传与功率约束的鲁棒 POMDP，用多智能体 DRL 集中训练分布执行，并设计改进的 clip-and-count PPO（内在奖励 + 改进裁剪机制），在上下行需求不对称与组播/单播并存的干扰环境中取得更高总速率与更快收敛。

## 方法快照

- 网络形态：一个 MBS 与多架 UAV 基站经容量受限回传互联；用户上行/下行可分别关联不同节点（解耦关联），利用 UL/DL 需求不对称。
- 干扰管理：下行面向多组播组的 RSMA（公共流 + 私有流拆分），上行强弱用户配对的速率分裂接入；全双工自干扰与跨链路干扰显式建模。
- 优化链路：非凸联合优化（关联、组播选择、波束赋形、公共速率）→ 鲁棒 POMDP（单 UAV 观测不全）→ MADRL 集中训练分布执行。
- 训练技巧：clip-and-count PPO——内在奖励提升探索效率，改进裁剪机制稳定训练。
- 验证：Python 3.6 + PyTorch 数值仿真（NVIDIA GTX 2080），合成蜂窝场景，未开源。

## 比赛映射要点

- 黑客松/算法赛：解耦关联的思路（上下行/读写/供需两侧分开匹配）与 clip-and-count PPO 组件都可独立移植；CTDE 骨架适配一切「局部观测 + 全局指标」的多智能体题。
- 双创申报：应急通信补盲、偏远农田联网是智慧农业与低空经济申报的常见痛点，RSMA 组播效率与解耦接入是可量化的技术论证点。

## 关联概念
- 速率分裂多址（RSMA）
- 蜂窝连接无人机通信

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Ji2024_RSMA解耦关联的UAV辅助蜂窝网络多智能体优化`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `ji2024DecoupledAssociationRate` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16），页内容与 bib 条目相符。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: unknown，故 runnable 如实标 false）；速率增益等数字如需引用请以论文原文复核。
