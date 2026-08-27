---
competition_id: kaggle-pokemon-tcg-ai-battle-challenge-strategy
last_verified: 2026-08-28
coverage: []
confidence: 低
sources:
  - url: https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=131772
    title: "Kaggle 官方 ListPages API：Evaluation / Submission Requirements / rules / Description（评审标准与硬约束的一手依据）"
    accessed: "2026-08-28"
---

# PTCG AI Battle Challenge — Strategy Category 模式库（patterns）

> coverage 为空（首届未放榜，Judging 2026-09-14~10-11）：本文件第一版仅沉淀**官方一手评审标准与合规红线**，方法论分布/往届差异化待 winners 数据到位后回填。confidence 低 = 无获奖样本佐证，非信源可疑。

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- **一手证据（Evaluation 页 2026-08-28 直抓）**：Model Score 70%（方法阐述与选型理由的清晰度、原创性与技术稳健性、重复对局下的稳定性、"不依赖特定初始状态/对位/情境优势"、赛道内性能）+ Deck Score 20%（卡组概念与策略契合、关键卡选用）+ Report Score 10%（结构逻辑、图表/表格运用）。
- 官方 Description 明示取向："High leaderboard ranking may provide an advantage in performance scoring, but it does not guarantee a strong result... Participants in middle or lower tiers can still achieve high overall scores through deep analysis, originality, and well-structured reporting."——**报告深度与原创性 > 榜单名次**（信源等级：官网）。
- 二手佐证（Misprint，聚合站降级）：Strategy 评审看 "stability of approach, deck design, agent performance in simulation" 三要素，与官方 70/20/10 口径同构。

## 二、方法论分布（获奖作品的方法/方案套路）

- 无数据（首届未放榜）。下轮按 Finalist Writeup 逐篇回填：预期轴为 RL 算法族（self-play/league）、搜索与启发式混合、deck 构筑搜索空间处理、不完全信息建模。

## 三、往届差异化点（什么样的作品拿到了最高奖）

- 无数据（首届）。待 2026-10-11 后抓 8 名 Finalist 的 Writeup 对比 Model/Deck/Report 三轴的得分取向。

## 四、反面观察（常见失分模式，若有依据）

- **一手红线（rules/Submission Requirements 直抓）**：Writeup 超 2000 词 "may be subject to penalty"；草稿/未提交状态过截止线一律不评审；Media Gallery 使用违反 Pokémon Elements 许可的图片 → "will not be evaluated and are subject to disqualification"；赛后未删 Competition Data、跨队私享代码均违规。
- 评审维度含"不依赖特定初始状态与对位"——过度过拟合特定 matchup 的 agent 在 Model Score 上失分（一手标准推论，非失分实录）。

## 五、赛点检查表（评审标准 → 可执行检查项）

- [ ] Writeup ≤2000 词（硬限）且含 title/subtitle/详细分析/Track 选择四要素
- [ ] 方法阐述逐条回答"为什么选此策略/验证了哪些假设/如何体现对游戏机制的理解"（Description 原文三问）
- [ ] 提供重复对局/稳定条件下的表现证据（Model Score 之"稳定性"轴）
- [ ] 说明方法不依赖特定初始状态或对位优势（反过拟合声明）
- [ ] Deck 设计与策略主线对齐，关键卡选用有理由（Deck Score 20%）
- [ ] 图表服务于论证而非装饰（Report Score 10%；Media Gallery 建议来自真实模拟器 trace——二手线索级建议）
- [ ] 图片素材通过 Pokémon Elements 许可检查；提交前确认非草稿状态
- [ ] 前置完成 Simulation 赛道报名与同队提交（参赛资格硬前提）

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合：agentic RL/不完全信息博弈是本方向风向标，但**本届窗口已事实关闭**（Simulation Final Submission 2026-08-17 已过）——只作模式库样本跟踪，不作参赛目标。
- "策略报告型赛道"范式（榜单名次 ≠ 报告得分，70/20/10 三轴）对我方"AI 辅助原创报告"能力是高相关练习场：下届若续办，可用本检查表直接派生 acceptance.checklist。
- 合规栈：LLM/AMLT 使用合法（Reasonableness Standard），获奖强制 MIT 开源 + 全量可复现代码交付——作品工程须按"可开源、可复现"标准搭建。
