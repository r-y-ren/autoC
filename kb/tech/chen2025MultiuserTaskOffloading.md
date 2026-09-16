---
id: chen2025MultiuserTaskOffloading
name: JULTO：UAV-LEO卫星边缘多用户博弈卸载
field: [移动边缘计算, 博弈论, 空天地一体网络]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 多用户竞争有限资源的潜在博弈建模 + Nash 均衡分布式求解（附 price of anarchy 均衡质量分析），可迁移到多主体资源竞争分配类决策赛题，对比集中式求解有"自利主体下分布式收敛"的差异化卖点
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 地面基础设施薄弱区域（山区/牧场/灾区）的空天地协同算力供给方案支撑——UAV 无线供能 + LEO 卫星覆盖窗口约束构成完整系统叙事，可作智慧农业远程监测类项目的技术底座
    reuse_cost: 低
sources:
  - paper_title: Multi-User Task Offloading in UAV-assisted LEO Satellite Edge Computing：A Game-Theoretic Approach
    doi: 10.1109/TMC.2024.3465591
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# JULTO：UAV-LEO 卫星边缘多用户博弈卸载

## 单行摘要

面向地形复杂、地面通信薄弱区域，将 UAV 与 LEO 卫星联合组成 ULSE 边缘网络；在多用户竞争有限资源、卫星覆盖时间受限的条件下，把每个用户的卸载决策（本地/UAV/LEO 三选）建模为 LUTO-Game，证明其为潜在博弈并设计分布式 JULTO 算法迭代收敛到 Nash 均衡，最小化时延与能耗加权的个人成本。

## 方法快照

- 问题构造：UAV/LEO 计算资源上界 + LEO 轨道运动导致的覆盖时间窗（coverage window）+ 用户传输功率约束，原问题证明为 NP-hard。
- 成本建模：本地、UAV 卸载、LEO 卸载三套异构成本模型；UAV 侧额外提供无线能量传输，使两类卸载的成本结构不同。
- 博弈重构：每个用户为理性参与者，以时延能耗加权个人成本为目标构造 LUTO-Game，用势函数证明 Nash 均衡存在。
- 分布式求解：JULTO 允许多用户并行更新卸载选择，并给出 price of anarchy 刻画分布式均衡与集中式最优的差距。
- 建模要点：LEO 覆盖时间窗不是细节约束，而是决定系统可行性的核心要素——这是与普通 UAV-MEC 卸载的本质区别。

## 比赛映射要点

- 数模决策类：共享算力/频谱/灌溉窗口等多主体竞争分配赛题，可用"潜在博弈 + 最优响应迭代 + POA 分析"替代单层整数规划，为分布式决策提供收敛性与最优性差距的双重量化论证。
- 双创申报：智慧农业远程监测（山地果园、牧场）等场景，空天地一体边缘算力 + 无人机补能的方案叙事有 CCF-A 方法背书；覆盖窗口约束可直接类比为"服务可用时段"约束。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Chen2025_空天地一体LEO卫星边缘计算多用户卸载`（frontmatter 4 枚举字段已迁移到本卡：venue_tier/evidence_tier/paper_role/reproducibility_level）。
- bib 回填：citekey `chen2025MultiuserTaskOffloading` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- 留痕：bib 标题含 ASCII 冒号（Edge Computing: A Game-Theoretic…），按格式规约改为全角冒号写入 frontmatter。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 low）承自 vault 页自评，如需引用请以论文原文复核。
