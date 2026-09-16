---
tags: [论文, 任务卸载, 轨迹规划, 蚁群优化, MEC]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2024BiobjectiveAntColony.md
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
  - field_test
data_origin:
  - mixed
platforms: []
frameworks:
  - bi-ACO
  - FSGM
  - SDM
  - PUM
  - Pareto optimization
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2024 双目标蚁群优化的UAV辅助MEC轨迹与卸载规划

## 单行摘要
论文在多 UAV 辅助 MEC 系统中联合处理轨迹规划与多阶段任务卸载，通过 bi-ACO 同时最小化总成本与总完成时间。

## 题目驱动研究框架
- 研究场景：UAV-assisted MEC 中的移动边缘服务与任务执行。
- 研究对象：多架 UAV、地面智能设备、保留 UAV 与按需 UAV、三阶段任务。
- 核心问题：在能源、截止期、位置和优先级约束下，如何同时规划 UAV 访问路线和任务执行/返回流程。
- 标题承诺的方法：bi-objective ant colony optimization for trajectory planning and task offloading.
- 期望效果：得到兼顾系统总成本与总完成时间的 Pareto 解集。
- 标题与正文的偏差：正文亮点不只是 bi-objective，而是把 multi-stage task offloading 的前后依赖直接嵌进 UAV 路径生成过程。

## Algorithm Design 快照
论文研究 UAV-assisted MEC 中“去哪飞”和“哪一步任务在哪执行”同时决定的问题。任务被拆分为数据上传、计算执行和结果回传三阶段，因此同一个地面设备可能需要 UAV 访问两次，路径与卸载之间存在强耦合。作者提出 bi-ACO 框架，通过具有不同目标偏好的异构蚁群构造解，并用 FSGM 生成可行解、SDM 提升解多样性，再通过 PUM 更新多组信息素矩阵。最终系统输出一组非支配解，用于平衡总成本与任务完成时间。

## 图1系统框架草案
- 系统实体：地面智能设备、保留 UAV、按需 UAV、基站/停机点。
- 任务/数据流：UAV 访问设备拉取数据，完成计算后再回访设备或发送结果。
- 控制/优化变量：设备访问顺序、每个任务阶段的执行时点、是否启用按需 UAV。
- 约束来源：电量、截止期、设备位置、任务优先级、任务阶段先后关系。
- 画图提醒：图中要突出“同一任务分三阶段”“一次或两次访问设备”“按需 UAV 有更高成本”这三个特征。

## System Model
- 每个任务分为数据传输、任务计算和结果传输三阶段，不同阶段对 UAV 飞行/悬停状态有不同要求。
- UAV 资源分为固定保留资源和高成本的按需资源，形成价格结构差异。
- 优化目标同时关注系统总成本与任务完成时间，因此是 Pareto 多目标调度。
- 任务优先级、能量预算和截止期共同定义可行域。

## Algorithm Design 详解
- FSGM：快速构造满足能量与任务阶段约束的可行解，是整个搜索过程的底座。
- SDM：对高质量解做拆分重组，提高非支配解集的多样性。
- PUM：对不同任务阶段使用多对信息素矩阵进行更新，使蚁群能表达多目标偏好。
- bi-ACO：通过多个异构 colony 同时探索不同目标权重下的可行解，最终形成近似 Pareto 前沿。
- 实验结论：在多种规模和地面设备分布下，bi-ACO 在效果和鲁棒性上优于 NSGA-II、SA、VND、GLS 和 ACO-DSP。

## 实验证据卡片
- 验证类型：数值仿真；可行性现场测试
- 数据来源：合成地图与不同设备分布场景
- 平台与软件：未说明
- 硬件与算力：未明确披露
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出了运行时间、Pareto 指标和 field tests 可行性说明，但现场测试细节主要在附录中。

## Introduction 写作素材
- 任务卸载与轨迹规划在移动 UAV-MEC 中不应分开，因为任务阶段顺序会反向决定路径结构。
- 当系统同时含保留 UAV 和按需 UAV 时，资源价格结构会直接改变轨迹与卸载策略。
- 这篇论文适合支撑“组合式元启发算法仍然是复杂 UAV-MEC 联合调度的重要路线”的引言判断。

## Related Work 写作素材
- 与只研究单阶段任务卸载的工作相比，本文显式处理多阶段任务依赖。
- 与只做轨迹优化的工作相比，本文将设备二次访问与结果回传嵌入路径生成。
- 与单目标启发式算法相比，本文更强调非支配解集而不是单个最优点。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[双目标蚁群优化]]
- [[任务卸载]]
- [[轨迹优化]]
- [[任务卸载与资源分配研究主线]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/wang2024BiobjectiveAntColony.md)
