# Kaggriculture 提交 SOP（submit-sop.md）

> 适用：Kaggle Simulation Competition「Kaggriculture」（competitionId 147734）。
> 责任分工：本 SOP 全部步骤为**队伍人工执行**（蓝图验收项 `man-reg` 报名 / `man-submit` 提交与天梯观察）；AI 框架不代操作 Kaggle 账号。
> 事实来源：官方 rules / Timeline / Evaluation / How to-Play（2026-08-28 经 Kaggle 官方 ListPages API 直抓，经 `kb/competitions/kaggle-kaggriculture/meta.md` 转引）；关键日期——开赛 2026-07-29，**终交 2026-09-30 11:59 PM UTC**，榜单收敛 2026-10-01 至约 10-15。

## 0. 第 0 天（立即）：报名核对 —— 唯一硬时点风险

- [ ] 打开赛站 Overview 与 Rules：<https://www.kaggle.com/competitions/kaggriculture>
- [ ] **人工核对 Entry Deadline**：官方 API Timeline 该字段为模板变量（`${competition.ProhibitNewEntrantsExplicitDeadline}`）未解析，**截止日无官方数值**——以赛站页面显示为准，不得臆测
- [ ] 确认当前可报名（2026-08-28 赛事 active），点 Join Competition 完成报名（18+ 资格、非制裁地区）
- [ ] 团队设置：队伍 3 人（上限 5 人合规）；**单账号纪律**——rules 明文禁止多账号报名/提交（"You cannot sign up to Kaggle from multiple accounts..."），全队共用一个账号提交
- [ ] 顺手核对奖池徽标：官方 rules/Prizes 双处为 $50,000（10×$5,000）；若列表页显示 $60,000 属待核口径，记录截图反馈至 KB 待核清单

## 1. 提交前本地检查（每次提交必跑，仓库根目录）

```bash
python workspace/software/smoke_boot.py                  # 冒烟：exit 0 才继续
python -m pytest workspace/software/tests -q             # 45/45 通过才继续
python workspace/software/scripts/run_eval.py --rounds 4 # 40 局评估：对照上轮指标查回归
```

- [ ] 三条命令全部通过；评估结果与 `workspace/metrics.json` 记录无未预期回归
- [ ] 确认提交文件为 `workspace/software/kaggle_simulations/agent/main.py`，且 `LLM_PROVIDER=None`（默认关闭，提交形态不依赖任何外部模型/网络）
- [ ] 资源裕量自查：本地平均单局耗时见 `metrics.software.avg_episode_runtime_seconds`；线上容器 HDD/RAM/vCPU 限额官方未解析（待核），bot 应保持 stdlib-only、无重初始化

## 2. 提交操作与 Validation Episode

```bash
kaggle competitions submit kaggriculture -f workspace/software/kaggle_simulations/agent/main.py
```

- [ ] 提交后在赛站 Submissions 页确认 **Validation Episode 通过**（自博弈 720 回合跑通；显示 Error 即失败，回到第 1 步排查后再提交——失败提交同样消耗当日额度）
- [ ] 在《提交台账》（队伍自建表格）记录：日期、commit hash、本地 40 局评估摘要（胜率/Elo/终局资金均值，引自 `workspace/metrics.json` 更新）、Validation 状态、线上反馈

## 3. 每日迭代纪律（rules：每日 ≤5 次，仅最近 2 次计入最终评估）

- **核心风险**：最终评估只跟踪**最近 2 次**提交——任何新提交都会顶掉旧版本；临近终交的随手提交会覆盖最优版本。
- 节奏建议：
  - 白天实验性提交 ≤3 次（每次对应明确的假设与本地评估依据）
  - **当日收尾必须以当日最优版本作最后一次提交**（保证「最近 2 次」里至少有一个最优版）
  - 每日额度用尽前 30 分钟自查：最近 2 次提交是否都想保留？
- 只提交本地 40 局评估无回归的版本；禁止提交未跑第 1 节检查的版本

## 4. 天梯观察（每日 10 分钟）

- [ ] 记录本队线上 skill rating 与近期对局结果（Elo 式：只看胜负平，净胜金币不影响评分）
- [ ] 将线上反馈同步 software 侧：校准本地对手池（引入线上同类评级 bot）、更新 `workspace/metrics.json` 的 `online_ladder_games` / `online_skill_rating`（当前为 null，如实待补）
- [ ] 评估口径提醒：天梯高方差，不追单局结论，以滚动窗口趋势判断版本强弱

## 5. 09-15 切换决策点（主攻/备选裁决）

- [ ] 若至 09-15 评估器显示投入产出比不佳（天梯排名趋势 + 迭代边际收益），启动备选：切 **kaggle-rsna-knee**（10-15 报名截止、10-22 终交）
- 切换不浪费：本地评估基建（gym 封装/Elo/复盘日志）与实验管理流程为通用资产
- 决策由队伍人工裁决（strategy.md 预设的兜底路径）

## 6. 终交前检查单（2026-09-30 11:59 PM UTC 前完成）

- [ ] **最近 2 次提交为最优版本**（此为最易翻车项：终交日不要再做随手提交；如需最后调整，最后两次提交都应是最优候选）
- [ ] 两次计入提交的 Validation Episode 均 Passed
- [ ] 本地 40 局评估最终无回归；最优 commit 已记录台账
- [ ] 无多账号操作；提交文件 stdlib-only、无外部网络依赖
- [ ] 确认无需再动：榜单 10-01 起继续跑对局至收敛（约 10-15），期间无法改提交

## 7. 待核项台账（随观察回填，来源 meta.md 待核清单）

| 待核项 | 状态 | 核对方式 |
|---|---|---|
| Entry Deadline 官方数值 | 缺失（API 模板变量未解析） | 第 0 天人工核对赛站（§0） |
| 奖池 $50K vs $60K 双口径 | $50K 官方双处直抓采信；$60K 待核 | 赛站奖池徽标 + 列表页截图 |
| agent 运行环境资源限额 | FAQ 模板变量未解析 | 观察线上 Validation/对局日志；bot 保持轻量 |
| API 型 LLM 容器网络策略 | 官方未载明 | 如启用 LLM 模块须先实测；当前默认关、不依赖 |
