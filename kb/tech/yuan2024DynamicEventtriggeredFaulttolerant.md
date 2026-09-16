---
id: yuan2024DynamicEventtriggeredFaulttolerant
name: 具规定性能的动态事件触发容错编队协同控制
field: [无人机编队控制, 容错控制, 事件触发]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 规定性能函数给跟踪误差设显式上下界、事件触发机制量化通信节流、LMI 求解控制器参数——这套"误差有界 + 触发次数/通信开销"分析框架可用于无人机编队/轨迹类赛题的安全约束建模与通信资源权衡评估
    reuse_cost: 高
  - track: 双创-文书与申报
    edge: 植保/巡检无人机编队在执行器故障与风扰下仍能安全编队飞行（跟踪误差不越界 + 机间不碰撞）的容错控制技术点，直接支撑低空农业装备可靠性章节
    reuse_cost: 低
sources:
  - paper_title: Dynamic Event-Triggered Fault-Tolerant Cooperative Resilient Tracking Control with Prescribed Performance for UAVs
    doi: 10.1007/s11432-023-4099-x
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 具规定性能的动态事件触发容错编队协同控制

## 单行摘要

面向固定翼 leader-follower 编队在执行器故障、外部扰动与有限通信资源下的协同跟踪问题，提出基于动态事件触发故障观测器的容错控制框架：动态事件触发机制仅在触发条件满足时更新观测器与控制律以节流通信；规定性能函数（PPC）把跟踪误差约束在预设边界内并与最小安全距离联动实现碰撞规避；H∞ 指标抑制风扰湍流，控制器/观测器增益摄动下保持非脆弱；最终归为 LMI 求解，仿真对比优于传统 H∞ 控制。

## 方法快照

- 编队模型：1 leader + 多 follower 固定翼 UAV，显式考虑执行器故障、有界外部扰动与控制/观测增益摄动。
- 动态事件触发故障观测器（DET fault observer）：故障检测 + 按需更新，降低编队通信负担与控制更新冗余。
- 规定性能控制（PPC）：误差变换使跟踪误差始终落在预设边界内，边界与最小安全距离联动给出碰撞规避条件——控制目标从渐近稳定升级为有界安全稳定。
- 韧性设计：H∞ 指标抗扰 + 非脆弱控制器应对增益摄动。
- 求解：LMI 求控制器参数；theory + simulation 验证。

## 比赛映射要点

- 数模编队/轨迹赛题：论文的可用产出是建模思路而非现成代码——规定性能函数给"误差不许超过某界"类约束提供了标准数学表达，事件触发的触发次数统计可作为通信开销/资源约束的量化论证；LMI 求解需 MATLAB/YALMIP，迁移成本高，仅在赛题明确涉及编队控制时选用。
- 双创申报：农业无人机编队作业（植保集群、巡检编队）的可靠性叙事——故障后仍能在有限通信下安全编队，是装备可靠性论证的硬技术点。

## 关联概念（vault 枢纽页折叠于此，不独立成卡）

- **事件触发容错控制**：不按固定周期更新控制，而在误差/状态触发条件满足时才激活观测器与控制律，同时兼顾故障估计与安全稳定；把节流通信与容错安全统一起来，适合通信受限、节点分散的 UAV 编队系统。本卡是其当前语料中的代表实现。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Yuan2024_具规定性能的动态事件触发容错协同跟踪控制`（frontmatter 4 枚举字段已迁移至本卡）；枢纽页 `事件触发容错控制.md` 已折叠进上文关联概念节。
- bib 回填：citekey `yuan2024DynamicEventtriggeredFaulttolerant` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（theory+simulation、synthetic 场景、复现性 medium、无开源）承自 vault 页自评，如需引用请以论文原文复核。
