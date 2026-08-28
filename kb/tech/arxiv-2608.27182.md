---
id: arxiv-2608.27182
name: "TraceBench: Controlled Evaluation of LLM Agents for Time-Series Root-Cause Attribution"
field: [LLM agents, 时序异常检测, 根因分析]
directions: [黑客松与数据竞赛]
published: "2026-08-27"
maturity: paper
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "AIOps/工业 RCA 赛题的打法库：三条受控实验发现直接可执行——(a) 域上下文注入显著增益→给 agent 喂系统机理文档；(b) agent 靠数值控制台而非可视化探索→工具面按统计探查设计；(c) 强制写脚本映射样本→标签反而更差→评测接口避免全量脚本化。仿真式任务生成（物理系统改参数=注入根因）可低成本自造带真值根因的评测集，解决 RCA 赛题『无 ground truth 无法自评』的痛点"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2608.27182
    title: "TraceBench: Controlled Evaluation of LLM Agents for Time-Series Root-Cause Attribution"
    accessed: "2026-08-28"
  - url: https://tracebench.github.io
    title: "TraceBench 项目站（2026-08-28 实抓仅能核实标题与描述，工件链接未能核实）"
    accessed: "2026-08-28"
---

# TraceBench：时序根因归因 LLM 智能体的受控评测

> 来源：https://arxiv.org/abs/2608.27182 （arXiv v1 提交于 2026-08-27，cs.LG，作者 Bendinelli、Dox、Holz；页无 Comments 字段；附 ancillary 文件 tracebench_representative_agent_trajectory.pdf；抓取日期 2026-08-28）

## 是什么

arXiv 2608.27182 提出 **TraceBench**：仿真式受控根因归因任务生成框架（以下描述均来自本次抓取的摘要页）：

- 每个任务给 agent 一段**物理动力学系统仿真输出的时序**，agent 须判断仿真中段是否有系统参数被改动、若有则定位是哪个参数（参数改动即受控注入的根因，真值已知）；
- 任务由**三个可解释的机械系统**生成；**四个 LLM agent** 在受控条件下评测；
- 三条关键发现：agent **显著受益于域上下文**；探索数据主要靠**数值控制台输出**而非可视化；被要求**写 Python 脚本把样本映射为预测标签时表现更差**（对比直接提交预测）；
- 摘要声称在项目站 tracebench.github.io 发布数据集、agent 轨迹、实验结果与排行榜。

## 解决什么问题

LLM agent 越来越多地被用于真实系统的时序异常检测与根因分析，但真实数据没有已知根因真值，无法在受控条件下分离"归因能力"与"数据巧合"——该领域此前没有系统化受控评测。

## 相比前方法优势

- **仿真生成 → 根因真值可控已知**：改哪个参数、何时改，全部可操纵，可做因果干净的 agent 行为分析；
- 机械系统可解释，规避"黑盒仿真器自己也解释不了根因"的问题；
- 受控操纵条件（域上下文有无、交互接口形态）而非只报总分，得出**接口与上下文层面的设计结论**——比单纯排行榜更有工程可操作性。

## 局限

- **发布工件未能核实**（runnable=false）：2026-08-28 实抓 tracebench.github.io 仅能确认站点存在及标题/描述（"controllable benchmark for agentic root-cause analysis of time series"，与论文对应），数据集/排行榜等工件链接未能抓到（疑似 JS 渲染或尚未填充）；GitHub 检索 "tracebench" 无对应论文仓；arXiv 页无代码链接——复用前需人工再核站点；
- 域窄：三个机械系统的结论外推到 IT 链路/微服务 trace 等 AIOps 主流场景需重建仿真；
- 仅评测四个 agent，结论样本小；v1 无 venue。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松数据与算法题中的 AIOps/工业智能赛道（异常检测+根因归因是企业挑战赛高频题型）。
- **打法（三条发现即三条对策）**：(a) **域上下文注入**——把系统机理文档（部件关系、参数含义、正常范围）写进 agent 上下文或检索库；(b) **工具面设计**——提供统计探查工具（分布/变化点/相关性数值输出），不要指望模型自己"看图找异常"；(c) **接口设计**——让 agent 逐段提交归因判断并即时反馈，避免一次性全量脚本化输出。
- **自造评测集**：借其仿真式任务生成方法论（选可解释系统→正常段跑稳→中段改一个参数→问 agent 定位），即可低成本造出带根因真值的自评集——RCA 赛题最缺的就是真值。
- **成本**：reuse_cost=中——若项目站工件后续可下载则更低；自建仿真任务生成器为中等工程量，无训练需求。
