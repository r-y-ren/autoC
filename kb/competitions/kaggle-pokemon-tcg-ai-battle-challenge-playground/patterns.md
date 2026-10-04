---
competition_id: kaggle-pokemon-tcg-ai-battle-challenge-playground
last_verified: 2026-10-05
coverage: []
confidence: 低
sources:
  - url: https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=168019
    title: "Kaggle 官方 ListPages API（本赛全页原件）：Description/Evaluation/rules/How to Play/How to Submit/data-description（官方一手机制与合规红线依据）"
    accessed: "2026-10-05"
---

# PTCG AI Battle Challenge — Playground 模式库（patterns）

> coverage 为空（首届在赛，终榜 2027-01-22 才定）：本文件第一版仅沉淀**官方一手机制与合规红线**，方法论分布/往届差异化待 winners 数据到位后回填。confidence 低 = 无获奖样本佐证，非信源可疑。
> 姊妹条目 kaggle-pokemon-tcg-ai-battle-challenge-strategy 的 patterns 为"报告型赛道"范式（70/20/10）；本赛为纯天梯对战型，两库不可混用。

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- **一手证据（Evaluation 页 2026-10-05 直抓）**：天梯 skill rating（Gaussian N(μ,σ²)，μ0=600 起评）——胜负平二值更新 μ，**净胜局数不影响评分**；终榜由 Bradley-Terry 锦标赛定，非累积天梯分。含义：稳定胜率 > 单局爆发；终评只看"最新 2 个提交 + 至多 2 个 Final Submissions"。
- 官方 Description 明示取向："Using rule-based programming alone may not ensure a high ranking"——纯规则脚本被官方点名天花板，引导学习方法（RL/搜索/混合）；同时 "Not knowing what cards an opponent holds presents a core challenge"——不完全信息处理是核心区分度。
- 无 Private Leaderboard（rules §2.10）：天梯即终局，长期挂机跑局与截止前换强势 agent 同样计分——策略上是"持续在场"游戏。

## 二、方法论分布（获奖作品的方法/方案套路）

| 模式 | 出现频次/占比 | 代表年份与条目 | 可迁移性 |
|---|---|---|---|
| 无数据（首届未放榜） | — | — | — |

- 下轮回填轴（官方材料已给观察点）：RL（self-play + 官方每日 top episode 导出做 BC/IL 预热）、不完全信息建模（对手手牌/卡组分布推断）、搜索（合法动作空间上的 MCTS 类）、deck.csv 构筑策略（数据页 EN/JA 卡表元数据挖掘）。

## 三、往届差异化点（什么样的作品拿到了最高奖）

- 无数据（首届）。待 2027-01-22 终榜后按 Top 5 的 Leaderboard 回放 + 论坛帖回填。

## 四、反面观察（常见失分模式，若有依据）

- **一手红线（rules/FAQ 直抓）**：①对局评测中 agent 不得联网读写外部信息（§2.8）——任何"在线查询卡表"设计直接违规；②Validation Episode 自博弈跑不通即标 Error，不进配对池——提交前本地 SDK 冒烟为硬前置；③只跟踪最新 2 个提交——临截止连发新 agent 会挤掉被跟踪的强势版本；④单账号、队限 5 人；⑤不得公开分享 Pokémon Elements（公开代码分享限赛内论坛/notebook 且须 OSI 许可）。
- Playground 无奖牌/现金（rules §7 + Prizes 页）——误按 Featured 赛投入产出模型规划属预期错位，非失分实录。

## 五、赛点检查表（评审标准 → 可执行检查项；快循环验收清单的派生源）

- [ ] 提交包 = .tar.gz，顶层 main.py（非嵌套）+ deck.csv（How to Submit 页硬格式）
- [ ] agent 路径 /kaggle_simulations/agent/，文件导入路径适配（FAQ 页）
- [ ] 对局内零网络/零外部信息读写（rules §2.8 红线自查）
- [ ] 提交前经官方 SDK（与赛内同逻辑）本地自博弈冒烟，避免 Validation Episode Error
- [ ] bo3 赛制下的"整场决策"（含让一追一的翻盘面）而非单局贪心（abstract 页 bo3 口径）
- [ ] 不完全信息处理方案有成文设计（官方点名的核心挑战）
- [ ] 截止节奏：每日 5 次额度内迭代，保持"最新 2 个提交"始终为最强版本；终交前锁定至多 2 个 Final Submissions
- [ ] 消费官方每日 top episode 导出（论坛）做 BC/IL 预训练——官方明示的数据杠杆
- [ ] 外部数据/LLM/AMLT 使用留痕（Reasonableness Standard 证据链），自训模型权重确权归我方（rules §3.18 豁免条款）

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合：本框架方向下**当前唯一可报名的 agentic 对抗仿真赛**（同日列表页快照核验）；窗口至 2027-01-08，约 3 个月，适合作为 agentic RL 技术练兵与 kaggle-environments 工程栈演练（cabt 与 kaggriculture 同栈）。
- 回报结构清醒认知：Swag 无现金、Playground 无奖牌——参赛定位是能力验证与 KB 情报采集（每日 top episode + 他队回放是 agentic 博弈的一手语料），非奖项收益。
- 合规栈：LLM/AMLT/外部数据全部放行（Reasonableness Standard），获奖无强制开源（Winner License None）——与 Strategy 赛的 MIT 强开源形成对照；自训权重归参赛者但禁赛外/商用；Pokémon Elements（卡面/IP 素材）红线用于多媒体产物检查。
