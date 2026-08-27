---
competition_id: kaggle-kaggriculture
last_verified: 2026-08-28
coverage: []
confidence: 低
sources:
  - url: https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734
    title: "Kaggle 官方 ListPages API：Evaluation / How to Play / Foundational Rules / rules（排名机制与游戏机制一手依据）"
    accessed: "2026-08-28"
---

# Kaggriculture 模式库（patterns）

> coverage 为空（未放榜，定榜约 2026-10-15）：第一版仅沉淀**官方一手的排名机制与游戏机制**，方法论分布待 winners 数据回填。confidence 低 = 无获奖样本，非信源可疑。

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- **无评委打分**：本赛是纯 Simulation Competition——Elo 式天梯排位（只看胜负平、不看净胜金币差）+ 终局 Bradley-Terry 锦标赛定榜（Evaluation 页 2026-08-28 直抓；rules 直抓 "There is no Private Leaderboard in Simulation competitions"）。"评审偏好"在此等价于**环境机制偏好**：谁在 720 回合内银行存款最多谁赢。
- 官方叙事取向（Description 页）：把农场博弈定位为供应链/动态定价/不确定下资源分配的沙盒——方案叙事若对齐"enterprise operations"语系更契合主办风向（观察级推论，无获奖样本佐证）。

## 二、方法论分布（获奖作品的方法/方案套路）

- 无数据（未放榜）。下轮按最终榜 Top 10 方案回填：预期轴为 RL 训练族（self-play/PPO 族）、规划与启发式混合、市场做市/限价策略、多 agent 劳动调度。

## 三、往届差异化点（什么样的作品拿到了最高奖）

- 无数据（按首届处理，待核）。

## 四、反面观察（常见失分模式，若有依据）

- **环境机制红线（How to Play 直抓，均为可验证的机械性失分）**：作物两天不浇水→变杂草（产出清零）；动物两天不喂→逃跑不可找回（投资全损）；番茄/草莓仅 4 次产出后衰败（长期占用地块负收益）；西瓜不施肥 10 天才达上限（机会成本）。
- **规则红线（rules 直抓）**：多账号提交违规；超每日 5 次提交/最终仅最近 2 份有效——临近终交日的提交管理是工程性风险点。
- Validation Episode 自博弈跑不通即 Error——提交前本地回归（getting-started 页指引）是硬要求。

## 五、赛点检查表（评审标准 → 可执行检查项）

- [ ] agent 通过 Validation Episode（自博弈无错跑完 720 回合）
- [ ] 浇水/喂养调度无两天断档（作物杂草化/动物逃跑双红线）
- [ ] 产出-占用比核算：优先高 Yield/tile/day 序列（蛋 1.00 > 麦 0.80 > 胡萝卜 0.75 > 奶 0.50，How to Play 官方表）
- [ ] 市场出货策略考虑价格对自身出货的反应（动态市场机制）
- [ ] 长线资本投资（买地/建牲口设施）与赛季终点（day 30）倒推回收期核算
- [ ] 提交管理：终交前确认最近 2 份提交为最优版本
- [ ] 合规：外部模型/数据过 Reasonableness Standard；获奖方案按 CC-BY 4.0 可开源

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合度高：agentic RL + 不完全信息经济博弈 + 谷歌官方背书；**窗口开放中**（终交 2026-09-30），是本方向当前可实际参赛的首选目标之一。
- 工程要点：Python kit + /kaggle_simulations/agent/ 部署路径 + 无 Private LB（最终榜由持续对局统计定出）——验收清单应含"本地可复跑对局"项。
- 数据政策极宽松（Apache 2.0 + CC-BY 4.0 获奖许可），无 LLM 禁令——合规栈成本几乎为零；但 agent 须在 Kaggle 仿真容器内自主运行，API 型 LLM 是否可用取决于容器网络策略（官方页未载明，列待核，勿臆测）。
