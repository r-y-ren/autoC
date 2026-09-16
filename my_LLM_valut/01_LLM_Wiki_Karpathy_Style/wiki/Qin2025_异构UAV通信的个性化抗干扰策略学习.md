---
tags: [论文, 抗干扰通信, 个性化联邦强化学习, 异构UAV]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/qin2025MultiagentReinforcementLearning.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - Personalized Federated Soft Actor-Critic (PFSAC)
  - stochastic Stackelberg game
  - federated reinforcement learning
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Qin2025_异构UAV通信的个性化抗干扰策略学习

## 单行摘要
论文在异构 UAV 对间通信与智能干扰共存的环境中，将抗干扰过程建模为随机 Stackelberg 博弈，并提出 PFSAC 以融合全局联邦模型与本地策略模型，让不同硬件能力和任务需求的 UAV 对学习个性化信道与功率抗干扰策略。

## 题目驱动研究框架
- 研究场景：异构 UAV 网络中的对间通信，面临智能干扰器与同频干扰双重压力。
- 研究对象：多个 UAV pair、多个 jammer、离散信道与功率级别。
- 核心问题：同构假设下的统一抗干扰策略无法适应不同 UAV 的硬件能力、功率范围与任务门限。
- 标题承诺的方法：在 adversarial game environments 中，通过 personalized MARL 学习 anti-interference strategies。
- 期望效果：提升通信速率、降低传输代价，并在异构网络中保持更强抗干扰能力。

## Algorithm Design 快照
论文把 jammer 视为先行动的 leader，把异构 UAV 网络视为 follower，从而构成随机 Stackelberg 博弈。每对 UAV 会周期性做频谱感知，再联合选择信道与功率级别。与统一全球模型不同，PFSAC 让各 UAV 对下载全局模型后与本地模型按权重混合，从而既共享干扰模式知识，又保留个体化决策偏好。这使“联邦学习”在这里不再只是训练预测模型，而是直接进入异构 UAV 抗干扰控制闭环。

## 图1系统框架草案
- 系统实体：`N` 个 UAV pair、`K` 个 jammer、`M` 类任务、共享信道集合。
- 感知输入：本地 CSI、同频干扰、jammer 干扰、任务门限与功率等级。
- 动作输出：每对 UAV 的信道选择与离散功率选择。
- 博弈关系：jammer 先选干扰动作，UAV 网络随后响应。
- 学习机制：联邦服务器聚合全局知识，UAV 对本地融合后执行个性化策略。

## System Model
### 1. 异构 UAV 对通信
- 网络由多个 UAV pair 构成，每对 UAV 具有不同的功率范围与任务速率门限。
- 系统不依赖全局完美 CSI，而是采用周期性本地感知。
- 通信成功由速率是否超过任务门限决定。

### 2. 干扰与信道模型
- 同频 UAV 之间会产生内部共信道干扰。
- 外部 jammer 会在共享信道上发起恶意干扰。
- 论文同时建模 LoS/NLoS 概率路径损耗与 Nakagami-m 小尺度衰落。

### 3. 离散功率与信道决策
- UAV 与 jammer 的功率被离散成多个级别。
- 最终目标是通过联合信道与功率决策最大化长期奖励，而不是瞬时 SINR。

## Algorithm Design 详解
### 1. 随机 Stackelberg 博弈
- jammer 作为 leader 先发起干扰，UAV 作为 follower 再做响应。
- 这一设定比纯协作 MARL 更符合抗干扰环境中的先后手关系。

### 2. PFSAC 的个性化思想
- 全局模型负责汇聚跨 UAV 的干扰环境共性。
- 本地模型负责保留个体 UAV 的硬件差异和任务偏好。
- 两者融合后，每个 UAV 对可以形成 personalized anti-jamming 策略。

### 3. 实验结论
- 与 `FSAC`、`FD3PG`、`ISAC`、`IDQN` 和随机方法相比，`PFSAC` 在平均奖励和抗干扰性能上持续更强。
- 论文还比较了不同本地:全局混合权重，显示 `7:3` 左右更优。
- 它的重要性在于把异构性和联邦个性化正式引入 UAV 抗干扰研究。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：异构 UAV 对与 jammer 的合成网络环境
- 平台与软件：原文未明确说明
- 硬件与算力：未说明
- 场景设置：系统考察 `4-12` 对 UAV、`1-4` 个 jammer、`5-10` 个信道及不同飞行高度
- 对比基线：`FSAC`、`FD3PG`、`ISAC`、`IDQN`、随机策略
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露训练硬件、软件栈和完整超参数表

## Introduction 写作素材
- 异构 UAV 网络中的抗干扰问题不能再用单一统一策略处理。
- 联邦协作若不考虑个体差异，只能共享知识，不能保证个体最优。
- 因而未来抗干扰通信需要同时处理“共享知识”和“个性决策”两个层面。

## Related Work 写作素材
- 传统抗干扰方法依赖预定义模式或单智能体学习。
- 独立多智能体学习虽然分布式，但缺乏信息共享，容易产生同频冲突。
- 纯联邦强化学习能共享模型，但若忽略异构性，仍难做到真正个性化适配。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[抗干扰通信]]
- [[个性化联邦强化学习]]
- [[联邦学习]]
- [[对抗式多智能体强化学习]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/qin2025MultiagentReinforcementLearning.md)
