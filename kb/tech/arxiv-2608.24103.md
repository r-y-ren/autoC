---
id: arxiv-2608.24103
name: 'ACE: A Self-Correcting Agentic Canvas Editor for Multi-Slide Presentation Automation'
field: [LLM agents, 文档智能, 演示自动化]
directions: [黑客松与数据竞赛]
published: "2026-08-25"
maturity: paper
signal:
  venue: "EMNLP 2026 Industry Track（v1 comments 标注 Main paper）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "PPT/文档自动化类赛题的完整作品骨架：①层级场景图编辑器替代平面绝对坐标元素，免除 agent 反复重算坐标破坏布局；②CARE 内容感知路由只喂当前相关的 deck 切片（实测 ~89% 平均输入 token 缩减、~44% 成本下降、1.75× 速度）；③无 ground-truth 的自校正回路——IF judge 的自然语言 critique 直接变成下一轮指令（4.23 vs 3.81，p=.010；26 人盲评 58.7% 胜率，81% 偏好自校正输出）。三个组件全是 prompt/工程级，无需训练"
    reuse_cost: 中
    open_source: "无（arXiv 页未附仓库，场景图需按目标格式自建）"
sources:
  - url: https://arxiv.org/abs/2608.24103
    title: 'ACE: A Self-Correcting Agentic Canvas Editor for Multi-Slide Presentation Automation'
    accessed: "2026-08-28"
---

# ACE：多页演示自动化的自校正智能体画布编辑器

> 来源：https://arxiv.org/abs/2608.24103 （arXiv v1 提交于 2026-08-25，cs.AI，comments: 26 pages, 12 figures, EMNLP 2026 Industry Track (Main paper)；抓取日期 2026-08-28）

## 是什么

arXiv 2608.24103（Jang、Lee、Park、Kwak）面向商用设计平台上的 LLM 编辑 agent，提出 **ACE** 系统（以下描述均来自本次抓取的摘要页）：

- **背景痛点**：遗留文档格式只暴露"平面的、绝对定位的元素"，agent 必须重算坐标并经常破坏布局；且设计没有唯一 ground truth，diff-against-reference 类指标会惩罚"有效但不同"的方案；
- **三个组件**：
  1. 建立在**层级场景图（hierarchical scene-graph）**之上的 agentic 编辑器，配 98 个工具的演示专用动作空间；
  2. **CARE 内容感知路由器**：只向模型提供相关的 deck 切片，平均削减约 89% 的输入 token；
  3. **自校正回路**：由"无 ground-truth"的 instruction-following judge 驱动，其自然语言 critique 直接作为下一轮的编辑指令；
- **关键结果**：单轮场景图编辑即可匹敌同骨干的迭代式 agentic HTML 流水线；自校正把 IF 分数从 3.81 提到 4.23（94 任务基准，配对 p=.010，并由 out-of-loop judge 复现），速度 1.75×、成本降约 44%；视觉质量均值统计不可区分，但 26 名盲评中 ACE 获 58.7% 决定性胜率、81% 偏好自校正输出；跨三个 judge 家族排名稳健；66% 案例一轮即停；strict-peak 回滚消除回归。

## 解决什么问题

LLM 编辑 agent 落地设计平台的两个实际障碍：平面坐标格式导致的布局破坏（工程可靠性），与"设计无唯一正确答案"导致的自动评估失真（评估方法学）——后者使 diff 类指标无法用于多轮自校正的信号来源。

## 相比前方法优势

- 用层级场景图从**表示层**根治坐标重算问题，而不是让模型学会更小心地算坐标；
- 自校正信号不依赖参考答案（ground-truth-free judge），适配"一对多正确解"的创作类任务——绕开了 diff 指标的根本缺陷；
- CARE 路由让大动作空间（98 工具）与长文档（多 slide）在成本上可行：token 减 89% 而质量不降；
- 工业赛道论文，全部指标围绕部署关切（速度/成本/盲评偏好）而非单纯离线分数。

## 局限

- **无开源**（arXiv 页无仓库链接，runnable=false）：场景图表示、98 工具动作空间、CARE 路由、judge 提示词均需按目标格式自行重建；
- 94 任务的内部基准 + 单一商业场景（多页演示），向其他文档格式外推未验证；
- 视觉质量均值与对照统计不可区分——优势主要体现在指令遵循与人工偏好，不是产出质量的碾压；
- 26 人盲评规模中等；自校正回路依赖 judge 质量，跨 judge 家族稳健性虽有检验但 out-of-loop judge 只保留三分之二增益。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松数据与算法题中一切"文档/幻灯片/设计自动化"作品——AI 生成 PPT、报告排版、画布类工具；亦适配需要"AI 自动改稿"叙事的办公自动化题。
- **可直接搬的三个模式**：
  1. **场景图中间表示**：先把目标文档解析为层级树再让 agent 编辑树而非坐标——一次工程投入，换掉整个"坐标崩坏"失败类；
  2. **内容感知路由**：长文档任务只检索/注入当前操作相关的切片，现场可展示 token 成本对比曲线；
  3. **critique-as-instruction 自校正**：judge 的自然语言批评直接拼进下一轮 prompt，无需训练、无需参考答案——这是"有效但不同也判对"的创作类任务上做自校正的标准答案。
- **叙事打法**：demo 放"平面坐标编辑 vs 场景图编辑"的布局破坏对照，再放自校正前后 4.23/3.81 式的 IF 分数提升；评委可现场盲评，与论文 58.7% 胜率实验形成呼应。
- **成本核算**：reuse_cost=中——三模式均为工程实现，但场景图解析与 98 工具级动作空间需按赛题格式裁剪重建；论文数字只能作方法佐证不能照抄（铁律 4：对外数字须自测）。
