---
id: arxiv-2608.26604
name: "hoBIT: A Profile-Aware Retrieval-Augmented Chatbot for University Academic Advising"
field: [RAG, 个性化检索, 对话系统]
directions: [黑客松与数据竞赛]
published: "2026-08-27"
maturity: demo
signal:
  venue: "EMNLP 2026 System Demonstrations Track（接收，arXiv Comments 自述）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "垂直问答赛题（校园服务/政务咨询/企业知识库）的『按人给答案』检索设计：同一问题因用户画像（院系/年级/计划）答案不同，profile-blind 检索会捞出看似合理但不适用的证据；proFILL 两个可搬设计——(a) 画像条件化检索索引，(b) 渐进式按需问询画像属性（由查询意图+初始检索结果引导，避免开场连环问隐私）——无训练、open-weight 本地部署即可落地，答辩叙事从 RAG 套壳升级为画像感知的检索+交互设计"
    reuse_cost: 低
sources:
  - url: https://arxiv.org/abs/2608.26604
    title: "hoBIT: A Profile-Aware Retrieval-Augmented Chatbot for University Academic Advising"
    accessed: "2026-08-28"
---

# hoBIT/proFILL：画像感知的高校学业咨询 RAG 聊天机器人

> 来源：https://arxiv.org/abs/2608.26604 （arXiv v1 提交于 2026-08-27，cs.IR 跨 cs.LG，作者 Kim、Lee、Kim、Kang（韩国中央大学系）；Comments 自述"Accepted to the System Demonstrations Track at EMNLP 2026"；页无代码链接；抓取日期 2026-08-28）

## 是什么

arXiv 2608.26604 提出 **proFILL**：把作者所在学校的现行规则式学业咨询聊天机器人 hoBIT 改造为画像感知 RAG 系统的方法（以下均来自本次抓取的摘要页）：

- 问题设定：学业咨询中**同一问题在不同 department、admission cohort、degree program 下需要不同答案**，画像盲（profile-blind）的检索器会捞出"看似合理但不适用"的证据；
- proFILL **不预取全量用户画像**，而是**渐进式只采集当前查询所需的画像属性**——由查询意图与初始检索结果引导；
- 采集到必要属性后，在 **profile-aware 索引**上做条件化检索；
- 实验与人类偏好研究：proFILL 优于多种 RAG 基线、被目标用户偏好，且可用 open-weight 模型实现低成本的本地（on-premise）部署。

## 解决什么问题

政策/规则类问答的知识库内容天然按人群切分（资格、期限、流程都随院系/年级/项目而变），通用 RAG 对所有用户检索同一索引，答案"通用正确、个体错误"。既有做法要么开场向用户索要全量画像（交互成本与隐私负担高、用户流失），要么画像与检索脱钩。

## 相比前方法优势

- **按需渐进问询 vs 全量预取**：只问"这条查询判别所需"的最小属性集，把问询成本压到必要处，交互负担与隐私暴露同时下降；
- **画像条件化检索**：让检索阶段就感知画像，而非生成后再打补丁，从源头抑制"不适用证据"进入上下文；
- 实证三件套齐全：自动化对比（优于多样 RAG 基线）+ 人类偏好研究（目标用户）+ 部署可行性（open-weight 本地化），是 demo track 级的完整证据链。

## 局限

- **无公开代码/实现**（runnable=false）：arXiv 页无代码链接，2026-08-28 在 GitHub 检索 "proFILL chatbot"/"hoBIT advising" 无对应仓库——复用需按摘要自实现；
- **单机构场景**：hoBIT 是作者本校现行系统，画像维度（院系/cohort/项目）与规则文档结构绑定单一高校，迁移到其他领域需重建画像 schema 与索引划分；
- venue 信号为 arXiv Comments 自述的 EMNLP 2026 demo track 接收，正式出版待会议；
- 摘要未披露画像条件化检索相对于更简单的"检索后画像过滤"基线的消融，增量来源（索引条件化 vs 问询策略）无法从摘要区分。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松数据与算法题中的垂直问答/智能助赛道——校园服务、政务咨询、企业内部知识库等"政策因人群而异"的赛题（选课资格、补贴申领、报销规则、入职流程均是此类）。
- **打法**：
  (a) **索引按画像维度预切**：答案片段入库时标注适用 cohort（元数据过滤或分索引），检索时以已知画像条件化；
  (b) **渐进问询作为交互亮点**：先无画像检索，若候选证据跨 cohort 冲突，再向用户提出**最小必要**的澄清问题——"系统知道自己在什么情况下需要问你"本身就是答辩差异化点；
  (c) **open-weight 本地部署**应对数据敏感赛题（学生/患者/企业内部数据不出域）。
- **答辩差异化**：现场演示"同一个问题，两个画像两种正确答案，而通用 RAG 答错其一"——用赛题真实规则文档构造对照即可，成本极低。
- **成本**：reuse_cost=低——无训练，标准 RAG 组件（向量索引 + LLM + 元数据过滤），工程量集中在画像属性 schema 设计与问询策略；无现成代码是唯一摩擦，方法可从摘要完整复原。
