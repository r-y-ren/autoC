---
id: kang2024AutonomousMultidroneRacing
name: Sim-to-Real 多无人机自主竞速（IPPO）
field: [多智能体强化学习, 无人机竞速, Sim-to-Real]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: Kaggle-竞赛
    edge: Kaggle simulation/RL 赛题（Lux AI 类多智能体环境）可直接复用「局部观测 + IPPO + 技能奖励塑形（穿门/超车/安全间距/越界惩罚）+ 并行采样随机初始化」配方，毫秒级决策时延约束与比赛实时性要求同构
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: AirSim 仿真训练 + 物理模拟器中间校验 + 真机迁移的三层 sim-to-real 管线，以及不依赖全局地图的局部感知多机避碰控制，适配机器人/无人机类 hackathon
    reuse_cost: 中
sources:
  - paper_title: "Autonomous Multi-Drone Racing Method Based on Deep Reinforcement Learning"
    doi: 10.1007/s11432-023-4029-9
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# Sim-to-Real 多无人机自主竞速（IPPO）

## 单行摘要

通过局部感知观测、面向竞速技能的多目标奖励塑形与 sim-to-real 训练设计，把多无人机竞速策略从 Microsoft AirSim 仿真迁移到真实户外竞速：不依赖全局赛道与边界信息，仅凭本地可见赛道特征，用 IPPO 训练穿门、超车、安全间距与越界惩罚等技能，在仿真对抗与真实户外竞速中均优于依赖全局轨道信息的基线，且控制决策时延为毫秒级。

## 方法快照

- 问题形态：多机竞速建模为马尔可夫博弈，观测仅含本地可见赛道局部特征（无全局赛道地图），放大了局部感知与实时决策约束。
- 奖励塑形：编码竞速技能——穿门、超车、安全间距、越界/边界惩罚，把抽象的「飞得快且不撞」拆成可学习的技能项。
- 训练设计：IPPO 独立策略学习 + 并行采样 + 随机初始化；训练环境注入竞速无人机的动态响应特性，使策略贴近真实控制对象。
- Sim-to-Real：物理模拟器作中间校验层，再迁移到真实硬件平台完成户外竞速验证。
- 验证：Microsoft AirSim 仿真 + 真实户外竞速（CUAV V5+ 飞控、i7-12700H + RTX 3060 地面终端）；开源情况论文未说明。

## 比赛映射要点

- Kaggle：仿真对抗类赛题（Lux AI、Halite 一系）的得分点正是「局部观测 + 多智能体交互 + 实时决策」，本文奖励塑形清单可直接当配方表用。
- 黑客松/机器人赛：三层迁移管线（仿真训练 → 物理模拟器 → 真机）是可复用的工程模板；「不用全局地图」的设定贴近真实赛场。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Kang2024_基于深度强化学习的自主多无人机竞速`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `kang2024AutonomousMultidroneRacing` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16），页内容与 bib 条目相符。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: unknown，故 runnable 如实标 false）；竞速圈速等结果如需引用请以论文原文复核。
