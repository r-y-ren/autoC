---
id: mao2025UAVassistedCommunicationsSAGINISAC
name: SAGIN-ISAC 移动用户跟踪与鲁棒波束赋形
field: [空天地一体化网络, 通感一体化, 鲁棒波束赋形]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: EKF 递推移动用户状态并把定位误差显式转写成信道不确定性的建模链路，可迁移到运动目标状态预测加预测误差量化的赛题，预测结果直接服务下游决策而非只报精度
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: outage 机会约束经 Bernstein 型不等式转可计算形式、再以 SDR 加一阶近似加 SCA 逐步凸化的鲁棒优化组件，可直接用于通信覆盖类仿真优化赛题
    reuse_cost: 中
sources:
  - paper_title: UAV-assisted Communications in SAGIN-ISAC：Mobile User Tracking and Robust Beamforming
    doi: 10.1109/JSAC.2024.3460065
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# SAGIN-ISAC 移动用户跟踪与鲁棒波束赋形

## 单行摘要

面向卫星、UAV 与地面移动用户构成的 SAGIN-ISAC 系统，论文把「移动用户位置如何获取」直接写进通信优化主问题：以空间辅助（卫星持续供位）或 ISAC 本地感知加 EKF 递推两条路线预测用户位置分布，再在 outage 约束下联合优化 UAV 轨迹、发射波束与目标速率以最大化能效——感知不是外部先验，而是与通信优化耦合的闭环环节。

## 方法快照

- 系统架构：LEO 卫星提供 space-air 辅助定位；多天线 ISAC-UAV 既当通信节点又当感知节点，跟踪并服务多个移动用户。
- 双位置获取机制：space-assisted（卫星侧持续提供较精确位置）与 ISAC-assisted（首时隙卫星校准、后续时隙 UAV 本地观测加 EKF 递推）两条路线。
- 不确定性传导：用户位置分布映射为后续时隙信道分布，替代完美 CSI 假设。
- 鲁棒可处理化：Bernstein 型不等式把 outage 概率约束改写为可计算形式，再用 SDR、一阶近似与 SCA 得到逐步可解的凸近似。
- 优化目标：在 outage、功率与轨迹因果约束下最大化系统能效，并对比两套跟踪机制的开销与精度权衡。

## 比赛映射要点

- 数模预测评估类：EKF 状态递推加「预测误差显式进入下游决策」是预测-决策一体化的建模套路，适合移动目标轨迹预测、定位误差敏感的评估题，与只输出点预测的常规做法形成差异化。
- 黑客松优化类：机会约束（outage）转凸的 Bernstein/SDR/SCA 工具链是通信覆盖、无人机路径随机优化环节的现成组件。
- 局限：纯仿真验证（合成轨迹与信道场景），未披露代码与硬件环境，runnable 为否；复用需自建信道与轨迹仿真。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Mao2025_SAGIN-ISAC中的移动用户跟踪与鲁棒波束赋形`（frontmatter 4 枚举字段迁移：venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium）。
- bib 回填：citekey `mao2025UAVassistedCommunicationsSAGINISAC` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）；bib 标题中的 ASCII 冒号改全角「：」写入，在此留痕。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
