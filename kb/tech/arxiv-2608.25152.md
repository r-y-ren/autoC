---
id: arxiv-2608.25152
name: "Belief Cascades Drive Persuasion in LLM Agent Networks"
field: [LLM agents, 多智能体仿真, 舆情传播]
directions: [黑客松与数据竞赛]
published: "2026-08-25"
maturity: paper
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "数模-数据分析与决策"
    edge: "用 LLM 智能体替换经典传播微分方程做舆情/观点演化 ABM 仿真：belief probe（逐轮探针测真实立场）+ exposure provenance（暴露溯源）提供论文级可量化轨迹，与套 SIR/Voter/deGroot 模型的队伍拉开方法论档次"
    reuse_cost: 中
  - track: "黑客松-数据与算法"
    edge: "『观点动力学沙盘』demo：真实 ego-network 拓扑上的可说服/可级联多智能体系统，现场展示说服级联的量化测量协议，超出聊天机器人式 LLM demo 的平均水准"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2608.25152
    title: "Belief Cascades Drive Persuasion in LLM Agent Networks"
    accessed: "2026-08-28"
---

# Belief Cascades：LLM 智能体网络中的信念级联说服

> 来源：https://arxiv.org/abs/2608.25152 （arXiv v1 提交于 2026-08-25，cs.CL/cs.AI；抓取日期 2026-08-28）

## 是什么

arXiv 2608.25152（Qiu、Liu、Venkit 等，cs.CL 主分类）提出一个受控测试床（testbed），研究有目标的说服者如何在基于**真实 ego-network 拓扑**构建的 LLM 智能体网络中改变其他智能体的立场（以下描述均来自本次抓取的摘要页）：

- 实验覆盖 **4 个 LLM 骨干、5 张图、55 条政策陈述**；说服效果取决于拓扑、说服者竞争、话题与模型先验的交互；
- 核心发现："直接暴露可靠地预测下一轮立场变化"；**同伴中继效应**真实存在但更弱——未被指派说服任务的智能体也会传导说服力（belief cascade）；
- 方法论警示：只分析消息文本会漏测立场移动——策略只有部分被文字兑现、行动可与文本背离、被说服者很少自己说出探测到的立场变化；
- 结论：说服应作为**轨迹级与暴露级过程**评估，工具是 belief probes（信念探针）、exposure provenance（暴露溯源）与 action logs（行动日志）。

## 解决什么问题

多智能体 LLM 系统（辩论、协同研究、用户模拟、信息中介）中，agent 间说服是基础能力却缺乏受控测量手段；且主流的"看文本猜立场"评估方式被证明会系统性漏测说服效果。

## 相比前方法优势

- 社会学真实拓扑（ego-network）而非随机图/全连接图，说服动力学结论更接近真实传播结构；
- 把说服从"文本分析问题"重构为"轨迹 + 暴露的测量问题"，给出可复用的三件套测量协议（probe / provenance / log）；
- 同时量化直接暴露与同伴中继两级效应，并跨 4 个骨干验证结论的稳健性。

## 局限

- **无代码、无数据发布**（arXiv 摘要页未见仓库链接，runnable=false），testbed 需按论文自行搭建；
- 效果依赖骨干模型与话题先验——论文明确说服结果随模型/主题组合而变，不是稳定普适常数；
- LLM 智能体的立场变化 ≠ 真实人类舆情，向真实社会结论外推需谨慎；均为 v1 预印本，未见同行评审信号。

## 如何用于比赛（比赛映射展开）

- **数模类（数据分析与决策赛种）**：舆情演化 / 谣言传播 / 观点极化类赛题，主流打法是 SIR、Voter、deGroot 等经典模型；本卡提供升级路线——用 LLM 智能体做异质主体 ABM，belief probe 每轮采样真实立场构成轨迹数据，exposure provenance 记录谁被谁的消息触达，可直接画出"级联传播树 + 立场时间线"两类论文级图；模型比较章节天然有 4 骨干 × 拓扑 × 话题的实验设计模板。
- **黑客松类（数据与算法赛种）**：做"观点动力学沙盘"作品——用户上传社交网络（或用公开数据集），指定说服者与政策话题，可视化 belief cascade 如何沿拓扑扩散；差异化在于**测量协议本身就是卖点**（多数同类 demo 只能展示对话，无法量化说服力），评委可看到逐轮立场热力图与中继效应分解。
- **成本**：核心开销是 LLM API 调用（每个智能体每轮一次生成 + probe），拓扑可用公开 ego-network 数据集；无现成代码，中等工程量（reuse_cost=中）。
