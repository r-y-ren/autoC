---
tags: [论文, 大模型, 无人机规划, 具身智能]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/chen2025TypeFlyLowlatencyDrone.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - prototype
data_origin:
  - self_collected
platforms:
  - Python
frameworks:
  - YOLOv8
datasets: []
hardware_stack:
  - Ryze Tello drone
  - NVIDIA RTX4090 GPU
  - 16-core Ryzen 7950X CPU
  - 64 GB RAM
artifact_availability: open
reproducibility_level: high
---

# Chen2025 TypeFly 低时延大模型无人机规划

## 单行摘要
论文提出 TypeFly 系统，通过为无人机任务规划设计轻量语言 MiniSpec、流式解释执行和 probe 机制，显著降低 LLM 生成控制计划的响应时延。

## 题目驱动研究框架
- 研究场景：自然语言驱动的交互式无人机任务规划。
- 研究对象：用户指令、视觉场景描述、远端 LLM、MiniSpec 运行时和无人机技能库。
- 核心问题：LLM 逐 token 生成计划导致响应时间过长，难以用于时敏型无人机控制。
- 标题承诺的方法：low-latency drone planning with large language models。
- 期望效果：让无人机更快开始执行动作，并在复杂任务中保持较好可用性与一致性。
- 标题与正文的偏差：标题强调 low-latency planning，但正文真正的方法创新在于“新语言 + stream interpreting + selective probe”的系统组合。

## Algorithm Design 快照
论文面向自然语言驱动的无人机控制，研究如何减少 LLM 生成计划的响应延迟。作者观察到传统让 LLM 输出 Python 或 PDDL 计划会因为 token 长、必须等整段计划生成完成后再执行而导致启动慢，因此设计了专门面向无人机规划的 MiniSpec 语言，并配套实现流式解释执行的 MiniSpec runtime。系统通过 Prompt Generator 融合用户指令和视觉场景描述，调用远端 LLM 生成 MiniSpec 程序；运行时在代码尚未完全生成时就开始执行可执行片段；对需运行时环境判断的分支则用 probe 机制向 LLM 发起极短回复查询，从而兼顾延迟、计划简洁性和环境适应性。

## 图1系统框架草案
- 系统实体：用户、视觉编码器、Prompt Generator、Remote LLM、MiniSpec runtime、无人机技能库、真实无人机。
- 任务/数据流：用户给出自然语言任务，视觉模块生成场景描述，Prompt Generator 形成规划提示，LLM 生成 MiniSpec 计划，runtime 边接收边解释并调用技能执行。
- 控制/优化变量：计划表示语言、可执行片段划分、是否触发 probe、是否 replan。
- 约束来源：LLM token 生成延迟、无人机交互实时性、场景动态变化、技能库规模。
- 画图提醒：图里要把“计划生成”和“计划执行”画成重叠流水，而不是串行流程，才能体现低时延核心思想。

## System Model
- TypeFly 并不把 LLM 当作完整控制器，而是作为 plan generator；实际执行由 runtime 和系统技能承担。
- 系统输入由两部分构成：用户自然语言任务描述与视觉编码器生成的场景文本描述。
- MiniSpec 是一种为 token efficiency 和 stream interpreting 设计的轻量计划语言，相比 Python/PDDL 更短、更适合边生成边执行。
- 系统还设计了高层技能、低层技能、probe 和 replan，使计划既可简洁，又能在环境变化时重新规划。

## Algorithm Design 详解
- 第一步是语言设计：作者发现规划延迟与输出 token 长度高度相关，因此用 MiniSpec 压缩语法，减少计划长度。
- 第二步是流式执行：MiniSpec runtime 可在接收到完整计划前就识别出可执行 statement 并开始执行，降低首动作时延。
- 第三步是 probe 机制：对依赖运行时场景信息的分支，不让 LLM 重新完整规划，而是只回答一个极短问题，减少额外 token 开销。
- 第四步是高层技能设计：通过少量高频高层技能降低 LLM 编程负担，但又避免技能库过大反而增加 prompt 成本。
- 第五步是异常与重规划：当技能失败或环境变化时，系统可停止当前计划并触发 replan，提高交互式任务成功率。

## 实验证据卡片
- 验证类型：原型系统/测试床验证
- 数据来源：自采/自建场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：代码或资产已公开
- 复现判断：`high`
- 证据备注：论文包含真实室内飞行原型验证，硬件链条较完整，但场景规模仍偏小。

## Introduction 写作素材
- LLM 在机器人规划中的问题不只是“会不会规划”，更是“来不来得及规划”。
- 在无人机这类时敏交互系统中，首个动作的启动延迟会显著影响用户体验与任务可行性。
- 因而，优化计划表示语言和解释执行流程，与优化 LLM 本身同样重要。
- 这篇论文很适合支撑“从云侧大模型能力走向具身无人机实时规划”的前沿引入。

## Related Work 写作素材
- 与直接输出 Python 程序的 LLM 规划方法相比，本文通过 MiniSpec 缩短输出 token 序列。
- 与需等待完整计划后再执行的方法相比，本文采用 stream interpreting 实现 plan-execution overlap。
- 与完全在线逐步问答式规划相比，本文用 selective probe 在延迟和适应性之间取折中。
- 相关工作写作时，可以把它放进“LLM for embodied UAV planning”分支，而不是传统 MEC 卸载分支。

## 相关系统建模页
- 无

## 相关概念与主题页
- [[大语言模型驱动无人机规划]]
- [[空中边缘大模型前沿]]

## 来源
- [原文](../raw/markdown/chen2025TypeFlyLowlatencyDrone.md)
