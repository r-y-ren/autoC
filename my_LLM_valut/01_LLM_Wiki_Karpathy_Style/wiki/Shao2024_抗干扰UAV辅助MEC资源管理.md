---
tags: [论文, UAV辅助MEC, 抗干扰通信, 资源管理]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/shao2024DeepReinforcementLearningbased.md
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
  - prototype
data_origin:
  - mixed
platforms: []
frameworks:
  - PER-MATD3
  - MATD3
  - jamming sensing and communication (JSC)
datasets: []
hardware_stack:
  - 12th Gen Intel Core i5-12400 CPU
  - Raspberry Pi 4B
  - DJI Tello
  - USRP N210
  - USRP X310
artifact_availability: unknown
reproducibility_level: medium
---

# Shao2024_抗干扰UAV辅助MEC资源管理

## 单行摘要
论文面向恶意干扰下的多 UAV-assisted MEC，联合优化 CPU 频率调节、带宽分配与信道选择，并提出带优先经验回放的 PER-MATD3，在仿真与室内原型实验中同时降低系统时延、能耗与综合成本。

## 题目驱动研究框架
- 研究场景：多 UAV 为地面用户提供计算与通信服务，但同时遭遇恶意 jammer 和共信道干扰。
- 研究对象：多架 UAV、地面用户、干扰器、带 CPU 动态调频能力的 UAV MEC 节点。
- 核心问题：在动态 CSI、时变计算能力与干扰存在时，如何做跨计算-通信域的联合资源管理。
- 标题承诺的方法：以 DRL-based resource management 解决 against jamming 的 UAV-assisted MEC。
- 期望效果：在真实约束下最小化时延与能耗加权系统成本。

## Algorithm Design 快照
这篇论文最值得注意的是，它没有只做信道抗干扰，也没有只做卸载，而是把 `CPU frequency adjustment + bandwidth allocation + channel selection` 三个动作同时写入多智能体连续控制问题。作者进一步引入 JSC 机制感知 jammed channel，并使用 PER-MATD3 加速训练，让 UAV 能在动态环境中联合平衡时延与能耗。这使它成为“抗干扰通信”和“UAV-assisted MEC 资源管理”真正交叉的一篇代表论文。

## 图1系统框架草案
- 系统实体：多架 UAV MEC 节点、地面用户、多个 jammer。
- 感知输入：CPU 基频、带宽占用、CSI、jammer 状态、用户负载。
- 决策输出：频率调节参数、带宽分配参数、信道选择因子。
- 学习模块：PER-MATD3 actor-critic 结构。
- 目标函数：最小化时延与能耗的加权系统成本。

## System Model
### 1. 计算与通信联合模型
- 每架 UAV 既承担任务处理，又承担无线传输，因此 CPU 频率调节和带宽分配同时影响系统表现。
- 系统状态包含 CPU 频率、CSI、带宽、信道干扰等多维信息。
- 这比只做“功率-信道”抗干扰要更贴近 MEC 真实资源管理。

### 2. 干扰感知
- jammer 会主动攻击部分信道。
- UAV 不仅要避开 jammer，还要避免多 UAV 之间的共信道干扰。
- 因而最佳决策依赖于实时频谱感知，而不是静态信道分配。

### 3. 成本目标
- 目标不是单一速率最大化，而是时延与能耗的加权成本最小化。
- 这让它天然适合接入当前 wiki 的“任务卸载与资源分配”主线。

## Algorithm Design 详解
### 1. PER-MATD3
- 在多 UAV 连续动作空间下，作者采用 MATD3 处理高维联合动作。
- 再通过 prioritized experience replay 提升关键经验利用率，加快收敛。

### 2. JSC 的作用
- JSC 让系统显式感知被 jammer 占据的信道。
- 因此“信道选择”不再是普通资源分配，而是带干扰感知的防御动作。

### 3. 实验结论
- 仿真中，PER-MATD3-JSC 在系统成本、时延、能耗上均优于 MATD3、单智能体 TD3、静态频率和随机策略。
- 原型实验使用 `DJI Tello + Raspberry Pi 4B + USRP` 验证了实际频谱感知与信道规避效果。
- 这使它成为当前库里少数同时给出“仿真 + 室内实验”的抗干扰 MEC 论文。

## 实验证据卡片
- 验证类型：`simulation` + `prototype`
- 数据来源：部分环境信息来自真实采集后重仿真，另含室内原型实验
- 平台与软件：原文未给出完整软件栈
- 硬件与算力：训练 CPU 为 `12th Gen Intel Core i5-12400`；实验使用 `Raspberry Pi 4B`、`DJI Tello`、`USRP N210`、`USRP X310`
- 场景设置：`1000m x 1000m` 仿真区域，`4-12` 架 UAV，`5MHz` 带宽，室内实验使用 `2.4GHz` 五信道通信
- 对比基线：`MATD3-JSC`、`PER-TD3-JSC`、静态频率、无信道选择、随机策略
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未给出完整代码、频谱感知实现细节和训练框架版本

## Introduction 写作素材
- 在 UAV-assisted MEC 中，恶意干扰会同时破坏通信时延和任务处理成本。
- 因而资源管理必须跨“计算 + 通信”两层联动，而不能只做链路对抗。
- 这篇论文适合支撑“抗干扰问题需要进入 MEC 联合控制主线”的引言逻辑。

## Related Work 写作素材
- 只优化轨迹或功率的抗干扰方法无法覆盖 MEC 中的 CPU/带宽联合决策。
- 单智能体 RL 难以处理多 UAV 之间的动作耦合与共信道干扰。
- 本文把频谱感知、频率控制、带宽分配和信道选择统一到多智能体连续控制框架中。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[抗干扰通信]]
- [[任务卸载与资源分配研究主线]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]
- [[多智能体强化学习]]

## 来源
- [原文](../raw/markdown/shao2024DeepReinforcementLearningbased.md)
