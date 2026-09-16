---
id: zhu2023AttitudeControlNovel
name: 新型倾转翼UAV悬停姿态控制
field: [倾转翼无人机, 飞行控制]
published: 2023-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 智慧农业无人机平台选型论证的实证背书——倾转翼把长续航与无跑道垂起放进同一平台（THU-TW001 真机 2.31m 翼展/23kg 起飞重量多组飞行试验），申报书平台章节与答辩可直接引用
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 含无人机硬件赛道的创新实践中，"系留试飞→积分补偿对照→速度补偿对照"的递进验证流程与悬停稳定性评估方法可直接套用
    reuse_cost: 中
sources:
  - paper_title: Attitude Control of a Novel Tilt-Wing UAV in Hovering Flight
    doi: 10.1007/s11432-022-3605-5
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 新型倾转翼UAV悬停姿态控制

## 单行摘要

围绕新型倾转翼原型 THU-TW001 的悬停姿态控制：主/尾翼分别带可倾转推进系统，新型分布式推进布局引入时变动力学与额外阻尼力矩；作者不用复杂非线性控制，而以变量增益线性/平方根控制律配合内环速度补偿抵消推进阻尼效应，系留与自由飞行对照试验证明速度补偿比积分补偿更适合该原型。

## 方法快照

- 平台结构：内翼固定 + 外翼可倾转，两大幅桨与两片小桨两组倾转螺旋桨；悬停控制力矩靠前后桨差分推力。
- 控制难点：新型推进布局带来时变动力学与额外阻尼力矩，悬停不再等价于普通多旋翼。
- 控制律：变量增益线性/平方根控制律保证响应速度与鲁棒性；姿态内环引入飞行速度补偿削弱推进阻尼效应。
- 验证路径：系留试飞 → 无补偿自由飞行 → 积分补偿飞行 → 速度补偿飞行四组对照；真实飞行数据，未披露完整飞控软件栈与参数表，论文自报结果。

## 比赛映射要点

- 双创：农业植保场景的垂起平台选型依据（续航 vs 起降场地约束），有 SCIS 真机实证的方法可作技术背书。
- 黑客松/创新实践：对照式飞行验证方法论（逐步加补偿、可复现的稳定性对照）是硬件类赛道可直接照做的工程流程。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhu2023_新型倾转翼UAV悬停姿态控制`（venue_tier/evidence_tier/paper_role/reproducibility_level 自页 frontmatter 迁移）。
- bib 回填：citekey `zhu2023AttitudeControlNovel` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2023），按 2023-01-01 填写；验证类信息（prototype/field_test、复现性 medium、无开源说明）承自 vault 页自评，如需引用请以论文原文复核。
