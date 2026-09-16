---
id: zhou2024SymmetryaugmentedMultiagentReinforcement
name: 对称性增强MADRL的大规模UAV轨迹与用户调度（SymmQMIX）
field: [多智能体强化学习, 等变网络, 无人机轨迹]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: EP2Net 排列等变网络 + 旋转/反射对称数据增强是对大规模实体调度状态空间爆炸的通用压缩手段，整合进 QMIX 形成 SymmQMIX 后论文自评最终性能约 4.5 倍、样本效率约 100 倍提升——对称性先验可平移到任何实体可交换的大规模分配/调度题
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 显式建模对称先验（实体无固定顺序、场景整体旋转/镜像不改变问题本质）的思路可用于大规模调度类数模题的模型设计，对称数据增强提升样本利用率的论证可写进智能优化章节
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 4 架 UAV 服务 64 个地面用户的代表性规模场景，为农业传感网/大规模农田节点的多机服务可扩展性提供量化参照
    reuse_cost: 低
sources:
  - paper_title: "Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Scheduling"
    doi: 10.1109/TMC.2024.3437679
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 对称性增强MADRL的大规模UAV轨迹与用户调度（SymmQMIX）

## 单行摘要

针对多 UAV 轨迹设计与地面用户调度联合优化中状态-动作空间随规模膨胀的问题，利用 UAV 与用户实体间的排列、旋转、反射对称性：EP2Net 使策略网络对实体排列保持等变，结合旋转/反射数据增强把冗余经验转化为等价样本，整合进 QMIX 形成 SymmQMIX——在 4 UAV + 64 用户代表场景中实现约 4.5 倍最终性能与约 100 倍样本效率提升。

## 方法快照

- 问题设定：UAV 作移动基站服务大量地面用户（应急通信类场景），空间位置决定服务集合与通信质量，轨迹与调度必须联合优化；核心挑战是可扩展性而非单次求解。
- 对称性来源：实体排列不变、整体旋转/镜像不改变问题本质；普通 MADRL 无法利用这些对称性时，会重复学习大量等价经验。
- EP2Net：处理实体排列等变性——输入实体顺序变化时输出动作同步变化，比 permutation invariance 更适配轨迹-调度联合问题。
- 对称数据增强：每条经验样本衍生更多等价样本，显著提升样本利用率。
- 整合：EP2Net + 对称增强 + QMIX 值分解 = SymmQMIX；页内自评对比 QMIX 与其他 symmetry-enhanced MADRL 基线均优（复现 medium）；平台与训练硬件未披露。

## 比赛映射要点

- 算法赛：大规模实体分配/调度题可移植"等变网络 + 对称增强"组合，是超越普通 QMIX/策略网络的差异化组件。
- 数模赛：对称先验建模与样本效率论证思路可用于大规模调度问题的模型合理性分析。
- 双创申报：多机对大规模节点的服务覆盖能力量化参照（机数-用户规模配比）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2024_对称性增强的UAV轨迹与用户调度MADRL`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `zhou2024SymmetryaugmentedMultiagentReinforcement` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 性能数字（4.5 倍/100 倍）为论文自报、经 vault 页转述，引用请以原文复核。
- 复现性承自 vault 页自评（medium，仿真验证、实现平台与硬件未披露）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
