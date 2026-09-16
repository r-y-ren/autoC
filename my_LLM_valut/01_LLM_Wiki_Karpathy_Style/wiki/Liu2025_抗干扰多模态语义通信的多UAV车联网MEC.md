---
tags: [论文, 语义通信, 车联网, 抗干扰, 多智能体强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/liu2025MultiUAVassistedMECInternet.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - SC-MA-TD3
  - semantic communication
  - TD3
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Liu2025 抗干扰多模态语义通信的多UAV车联网MEC

## 单行摘要
论文在多 UAV 辅助 IoV-MEC 中引入多模态 [[多模态语义通信]]，并在存在恶意干扰机时通过 SC-MA-TD3 联合优化 UAV 轨迹、用户关联与信道选择，以降低通信与计算时延并维持语义准确度。

## 题目驱动研究框架
- 研究场景：城市车联网 MEC 中，车辆图像数据、路侧文本数据与 UAV 俯视信息共同组成多模态任务。
- 研究对象：车辆、RSU、多个 UAV、干扰机以及语义通信与边缘计算联合系统。
- 核心问题：多模态任务需要跨设备聚合，链路又会受到恶意干扰，传统按比特传输的方案既耗资源又难保持任务语义完整。
- 标题承诺的方法：combined multi-modal semantic communication under jamming attacks。
- 期望效果：在减小时延的同时提高语义恢复精度，并利用多 UAV 协同增强抗干扰能力。
- 标题与正文的偏差：正文更强调“UAV 在多模态接收中的位置选择与协作”，而不是仅把语义通信当成压缩工具。

## Algorithm Design 快照
论文关注车联网 MEC 中的多模态任务接入问题：车辆上传图像，RSU 提供文本，UAV 再结合空中视角完成联合分析。但在城市环境里，车辆与 RSU 的地面链路易受遮挡，且恶意干扰机会持续在多信道上发射干扰功率。为此，作者把语义通信引入多模态数据接入，仅传输对任务真正有用的语义信息，并进一步让多个 UAV 协作选择飞行位置、关联对象与信道。由于问题高度动态且非凸，作者提出 SC-MA-TD3，多智能体地学习 UAV 之间的协同行为，以同时降低通信和计算时延、抑制干扰影响并保持语义准确性。

## 图1系统框架草案
- 系统实体：车辆图像用户、RSU 文本用户、多个 UAV、一台干扰机。
- 任务/数据流：车辆图像语义、RSU 文本语义与 UAV 俯视信息被汇聚到 UAV 侧完成联合分析。
- 控制/优化变量：UAV 轨迹、用户关联、信道选择、语义接收位置。
- 约束来源：干扰机功率、多 UAV 协同、空地链路质量、语义准确度约束。
- 画图提醒：建议把“图像用户”“文本用户”“UAV 俯视信息”画成三路语义输入，再用干扰机侧箭头突出对接收阶段的破坏。

## System Model
- 系统包含图像采集点、车辆图像上传用户、RSU 文本用户、多个 UAV 和一个持续发射干扰的 jammer。
- UAV 既承担空中接入点角色，也承担一定计算和多模态融合能力。
- 任务质量不再只由 bit error 决定，而要由语义准确度衡量恢复结果与原始信息的一致性。
- 决策目标是同时优化关联、轨迹与信道选择，使多模态语义接入在受干扰环境中仍然可用。

## Algorithm Design 详解
- 先定义通信与计算联合时延以及语义准确度约束，把抗干扰多模态接入写成联合优化问题。
- 再用多智能体 TD3 结构，让每架 UAV 在局部决策下学习与其他 UAV 的协作行为。
- 语义通信减少了上传负担，但 UAV 的位置与信道选择决定了语义数据能否稳定汇聚。
- 该文说明语义通信在 UAV-MEC 中不是单独一层编码模块，而是会反向影响轨迹、关联和边缘计算组织。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成车辆、RSU、UAV 与干扰场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文完整给出了场景与算法思路，但未披露统一仿真平台与硬件环境。

## Introduction 写作素材
- 语义通信进入 UAV-MEC 后，优化对象不再只是传输比特，而是“以多模态任务完成为目标的有效信息流”。
- 恶意干扰下的车联网场景能放大语义通信与 UAV 协同接入的互补性。
- UAV 的价值不仅是补 LoS，还在于为空地多模态汇聚提供几何可调度性。

## Related Work 写作素材
- 传统 UAV-assisted IoV MEC 主要优化时延、能耗或卸载比例，很少把语义准确度写入主目标。
- 现有语义通信工作多聚焦单链路或单模态，缺少多 UAV 协同抗干扰设计。
- 该文把语义通信、多模态融合和多智能体 UAV 协同合并为统一决策问题。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[多模态语义通信]]
- [[空中通信与协同传输]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/liu2025MultiUAVassistedMECInternet.md)
