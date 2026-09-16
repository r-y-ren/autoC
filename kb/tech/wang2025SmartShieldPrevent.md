---
id: wang2025SmartShieldPrevent
name: Smart Shield：协同智能干扰反空中窃听
field: [物理层安全, 多智能体强化学习, 友好干扰]
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
    edge: QMIX + dueling DDQN 在 Dec-POMDP 局部观测下的低耦合多智能体协同骨架（不共享观测、避免信息共享延迟），可迁移到多智能体在线对抗/巡防/协同防御类赛题，与需全局信息共享的 MADDPG 类基线形成差异化
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济安防叙事的差异化技术点——把友好干扰从静态辅助手段升级为多地面干扰节点在线协同的动态"智能屏蔽层"
    reuse_cost: 低
sources:
  - paper_title: Smart Shield：Prevent Aerial Eavesdropping via Cooperative Intelligent Jamming Based on Multi-Agent Reinforcement Learning
    doi: 10.1109/TMC.2024.3505206
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# Smart Shield：协同智能干扰反空中窃听

## 单行摘要

面向高速机动的空中窃听威胁，用多个地面干扰节点（GJ）通过 QMIX 协同学习实时轨迹与干扰功率，在合法用户与机动 AAV 窃听者之间形成动态干扰屏蔽带，在保障合法链路质量前提下最大化瞬时保密容量。

## 方法快照

- 问题建模：多 GJ + 机动 AAV 窃听者建模为 Dec-POMDP——每个 GJ 只依赖局部观测决策，无法获得全局且无延迟的窃听轨迹信息。
- 分层学习：单智能体用 dueling DDQN 缓解大状态/动作空间下的过估计、稳定逼近本地最优干扰动作；团队层用 QMIX 混合网络把个体价值函数合成团队价值函数，避免节点间实时共享局部观测。
- 决策变量：GJ 移动轨迹 + 发射功率联合优化；评测指标为瞬时保密容量与不同部署参数下的安全收益，对比固定干扰/非协同干扰基线。
- 关键洞察：对抗机动窃听者时，友好干扰应视为多智能体在线协同控制问题而非静态点状防御。
- 实现环境：Python 3.8 + PyTorch 1.11，Intel i7-1165G7 单机训练；代码未公开。

## 比赛映射要点

- 黑客松/算法赛：多智能体协同围堵/拦截/巡防类赛题（如无人机反制、多车围捕）可直接套用其"局部观测 + QMIX 混合价值"骨架；差异化卖点在于不依赖智能体间实时通信，契合弱通信约束赛题设定。
- 双创申报：低空经济安防/涉密区域防护场景的技术支撑点——动态反窃听屏蔽层比固定干扰基站方案更适应机动威胁。
- 数模延伸：Dec-POMDP 建模思路可用于"信息不完全下的多主体协同决策"类赛题的模型假设论证。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 键修正：分片清单原键 `Eavesdr` 为截断错键；经页内 sources 核对，真实文件为 `Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md`（Eavesdr 为 Eavesdropping 截断），对应 bib 键 `wang2025SmartShieldPrevent`，本卡以真实键作 id 与文件名。
- 提炼来源：my_LLM_valut wiki 页 `Wang2025_基于协同智能干扰屏蔽的空中窃听防护`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `wang2025SmartShieldPrevent` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- 留痕：bib 标题原为 ASCII 冒号「Smart Shield: Prevent Aerial Eavesdropping...」，按分片规则改全角冒号写入 paper_title。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 medium、代码未披露）承自 vault 页自评，如需引用请以论文原文复核。
