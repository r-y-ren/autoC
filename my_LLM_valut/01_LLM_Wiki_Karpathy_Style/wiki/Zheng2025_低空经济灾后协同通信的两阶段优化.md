---
tags: [论文, 低空经济, 灾后通信, 两阶段优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zheng2025UAVSwarmenabledCollaborative.md
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
  - two-stage optimization
  - collaborative beamforming
  - diffusion model-enabled PSO (DM-PSO)
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zheng2025_低空经济灾后协同通信的两阶段优化

## 单行摘要
论文从低空经济视角设计面向灾后通信的 UAV swarm 协同自组网，先求最优多路径流量路由与理论速率上界，再用 DM-PSO 联合优化参与 UAV 的激励权重与部署位置，使实际传输率逼近上界并验证网络在突发情形下的鲁棒性。

## 题目驱动研究框架
- 研究场景：低空经济背景下的灾后长距离协同通信。
- 研究对象：地面设备、多个 UAV swarm、远端 AP，以及提供控制计算能力的 HAP。
- 核心问题：传统 UAV 自组网在远距离灾后通信中可靠性差，难以同时兼顾路由与协同波束形成。
- 标题承诺的方法：用 two-stage optimization 组织 post-disaster collaborative communications。
- 期望效果：提高全网传输率，并在异常情形下维持鲁棒性。

## Algorithm Design 快照
作者把问题拆成非常清晰的两阶段。第一阶段先利用理论分析和现有方法求多路径 traffic routing，并给出网络传输率的理论上界；第二阶段在该路由结构上，把实际系统写成 V-RPTRMOP，通过 DM-PSO 联合优化参与 UAV 的激励权重和空间位置，使实际传输率逼近上界。这个设计避免了把路由、部署和协同波束形成一次性揉进超大一体化问题。

## 图1系统框架草案
- 源端：灾区地面设备。
- 中间层：多个 UAV swarm 组成的协同自组网，使用 collaborative beamforming 中继。
- 控制层：HAP 作为高空协调中心，负责算法执行与控制策略生成。
- 目的端：远端接入点 AP。
- 两阶段流程：先多路径流量路由，再 UAV 激励与位置协同优化。

## System Model
### 1. 灾后协同自组网
- UAV swarm 形成多段空中协同链路，为灾区地面设备与远端 AP 建立长距离通信桥梁。
- HAP 不直接参与数据转发，而作为高空协调枢纽负责控制与优化。

### 2. 协同波束形成与部署耦合
- 每架参与 UAV 的激励权重和部署位置共同决定链路传输率。
- 因此“路由”只解决流量分配问题，实际物理层性能还取决于第二阶段部署优化。

### 3. 鲁棒性关注
- 论文专门评估了三类 unexpected situations 对系统传输率的影响。
- 这意味着它比普通灾后覆盖论文更强调系统韧性。

## Algorithm Design 详解
### 1. 第一阶段：多路径路由
- 先获得最优多路径 traffic routing 和网络理论传输率上界。
- 这一阶段解决的是全局流量如何穿过 UAV swarm 网络。

### 2. 第二阶段：DM-PSO 优化
- 在固定路由基础上，把问题重写为惩罚版变体。
- 再通过 diffusion model-enabled PSO 联合调整 UAV 位置与激励电流权重。
- 目标是让实际传输率尽量接近理论上界。

### 3. 实验结论
- 仿真结果表明两阶段方法明显优于传统处理方式，并在三类意外场景下保持更好的鲁棒性。
- 它为“低空经济 + 灾后通信 + UAV swarm 协同网络”提供了一条很完整的方法链。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：灾后协同通信合成网络场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 场景设置：多 UAV swarm 协同自组网，含 HAP 控制枢纽和远端 AP
- 对比基线：传统单阶段或非协同方法
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露完整仿真平台与 DM-PSO 代码实现

## Introduction 写作素材
- 低空经济并不只是民用物流新概念，它也在灾后通信中提供了新的协同基础设施视角。
- 远距离灾后传输的瓶颈不只在覆盖，还在于路由、协同阵列和高空协调枢纽的统一组织。
- 因而这篇论文适合支撑“灾后通信正在从临时覆盖走向系统级协同网络设计”的写作判断。

## Related Work 写作素材
- 传统灾后 UAV 通信多聚焦覆盖、单跳中继或简单部署。
- 协同波束形成若不与多路径路由结合，很难充分发挥 swarm 能力。
- 这篇论文的特点是把理论上界、路由设计和 swarm 优化拆成清晰的两阶段框架。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[低空经济（LAE）]]
- [[两阶段优化]]
- [[协同安全中继通信]]
- [[空中通信与协同传输]]
- [[多无人机协同]]

## 来源
- [原文](../raw/markdown/zheng2025UAVSwarmenabledCollaborative.md)
