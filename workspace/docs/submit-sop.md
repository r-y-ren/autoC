# Kaggriculture 提交 SOP v2（成稿——可执行检查单）

> 适用：Kaggle Simulation Competition「Kaggriculture」（competitionId 147734）。
> 状态：波次 4/4（m3-polish）成稿。基线：第一轮归档 `submit-sop.md`（7 节、19 项检查单，只读参照）。
> 规模：**基础 19 项（B01-B19，沿用 v1 槽位、基线数值随本轮 metrics 更新）+ 新增四组 17 项（N1×3 / N2×5 / N3×4 / N4×5）= 36 项**，每项独立编号、可勾选、可执行。
> 责任分工：全部步骤**队伍人工执行**（蓝图 `man-reg` / `man-submit` / `man-final`），AI 框架不代操作 Kaggle 账号。
> 事实来源：官方 rules / Timeline / Evaluation / How-to-Play（2026-08-28 经 Kaggle 官方 ListPages API 直抓，经 `kb/competitions/kaggle-kaggriculture/meta.md` 转引）；关键日期——开赛 2026-07-29，**终交 2026-09-30 11:59 PM UTC**，榜单收敛 10-01 至约 10-15。
> 本地基线数值出处：`workspace/metrics.json`（键名随项标注；线上未发生指标如实 null）。

## 0. 第 0 天（立即）：报名核对——前置门（man-reg）

- [ ] **B01** 打开赛站 Overview 与 Rules：<https://www.kaggle.com/competitions/kaggriculture>
- [ ] **B02** **人工核对 Entry Deadline**：官方 API Timeline 该字段为模板变量（`${competition.ProhibitNewEntrantsExplicitDeadline}`）未解析，**截止日无官方数值**——以赛站页面显示为准，不得臆测
- [ ] **B03** 确认当前可报名，点 Join Competition 完成报名（18+ 资格、非制裁地区）
- [ ] **B04** 团队设置：队伍 3 人（上限 5 人合规）；**单账号纪律**——rules 明文禁止多账号报名/提交（"You cannot sign up to Kaggle from multiple accounts..."），全队共用一个账号提交
- [ ] **B05** 顺手核对奖池徽标：官方 rules/Prizes 双处为 $50,000（10×$5,000）；若列表页显示 $60,000 属待核口径，记录截图反馈至 KB 待核清单

### 新增组 1：报名前置门强化（本轮新增，对应 man-reg 置顶）

- [ ] **N1-1** **前置门规则**：报名（man-reg）未完成，不进入本 SOP §1 及之后的任何步骤——man-submit 的第 1 项前置检查即核对报名状态（勾选 B03 完成）
- [ ] **N1-2** Entry Deadline 核对结果**截图存档**，并把赛站显示数值回填《待核项台账》（§7 表第 1 行状态列）；仍是"缺失/以页面为准"也如实记录
- [ ] **N1-3** man-reg 完成后在《提交台账》记一行（日期 / 操作人 / 截图存档路径），作为人工项合规留痕

## 1. 提交前本地检查（每次提交必跑，仓库根目录——本轮升级为"本地四查"）

```bash
python workspace/software/smoke_boot.py                            # 一查 冒烟：exit 0 才继续
python -m pytest workspace/software/tests -q                       # 二查 测试：101/101（metrics: m2_tests_total / m2_tests_passed）
python workspace/software/scripts/run_eval.py --rounds 4           # 三查 148 局矩阵：对照 metrics 查回归
python workspace/software/scripts/run_eval.py --rounds 2 --assert-regression   # 四查 冻结回归线：exit 0
```

- [ ] **B06** 四条命令全部通过；三查结果与 `workspace/metrics.json` 记录无未预期回归——重点核对 submission 全池 Elo 第一（`m2_elo_ratings_full_pool`：1500.8）与对强敌胜率（`m2_matchup_win_rates`）不低于当前台账版本
- [ ] **B07** 确认提交文件为 `workspace/software/kaggle_simulations/agent/main.py`，且 `LLM_PROVIDER=None`（默认关闭，提交形态 stdlib-only、不依赖任何外部模型/网络）
- [ ] **B08** 资源裕量自查：本地单局均值见 `metrics.software.avg_episode_runtime_seconds`（2.66 s/局）；线上容器 HDD/RAM/vCPU 限额官方未解析（待核），bot 保持 stdlib-only、无重初始化

## 2. 提交操作与 Validation Episode

```bash
kaggle competitions submit kaggriculture -f workspace/software/kaggle_simulations/agent/main.py
```

- [ ] **B09** 提交后在赛站 Submissions 页确认 **Validation Episode 通过**（自博弈 720 回合跑通；显示 Error 即失败，回到 §1 排查后再提交——**失败提交同样消耗当日额度**）
- [ ] **B10** 在《提交台账》记录：日期、commit hash、本地评估摘要（Elo / 对强敌战绩，引自 `workspace/metrics.json` 更新）、Validation 状态、线上反馈

## 3. 每日提交纪律（rules：每日 ≤5 次，仅最近 2 次计入最终评估）

**核心风险**：最终评估只跟踪**最近 2 次**提交——任何新提交都会顶掉旧版本；临近终交的随手提交会覆盖最优版本。第一轮本节为节奏建议，本轮强化为**逐次检查列**（新增组 2）。

### 新增组 2：每次提交前的逐次检查列（本轮新增）

- [ ] **N2-1** 核对**当日已用额度 ≤5**（与《提交台账》"当日提交序号 1-5"计数列联动，防遗忘性超限）
- [ ] **N2-2** 本次提交对应**明确的实验假设与本地矩阵依据**（在台账注明；禁止无依据的随手提交）
- [ ] **N2-3** §1 本地四查全过才提交（任一查失败即中止本次提交）
- [ ] **N2-4** **每日收尾提交 = 当日最优版本**（保证"最近 2 次计入"里至少含一个最优版；台账"是否收尾最优提交"列勾选）
- [ ] **N2-5** 当日额度用尽前 30 分钟自查：最近 2 次提交是否均需保留？不需要的立即用剩余额度以最优版本收尾

《提交台账》本轮新增两列：**当日提交序号（1-5）**、**是否收尾最优提交**。

## 4. 天梯观察（每日 10 分钟）

- [ ] **B11** 记录本队线上 skill rating 与近期对局结果（Elo 式：只看胜负平，净胜金币不影响评分）
- [ ] **B12** 将线上反馈同步 software 侧：校准本地对手池（引入线上同类评级 bot）、更新 `workspace/metrics.json` 线上三键（当前如实 null，见新增组 3）
- [ ] **B13** 评估口径提醒：天梯高方差，不追单局结论，以滚动窗口趋势判断版本强弱

### 新增组 3：天梯反馈回填 metrics 流程（本轮新增，键名对齐 `workspace/docs/metrics-keys.md`）

- [ ] **N3-1** 每日观察窗口记录：本队 skill rating 数值 + 近期对局结果摘要（胜/负/平与对手风格观察），先记入《提交台账》线上反馈列
- [ ] **N3-2** 将记录转录至 `workspace/metrics.json` 预留键：`online_ladder_games`（累计线上对局数）、`online_skill_rating`（当日 skill rating）——未发生观察的日子保持 null，不估数
- [ ] **N3-3** 若线上评级 / 对局形态与本地池**明显背离**（如本地稳赢的对手类型线上频繁出现且失利）：把校准动作（替换 / 引入了哪个对手变体）记录至 `online_feedback_calibration` 键，并交 software 侧执行对手池校准（本地四查 + 回归门重跑后才算完成）
- [ ] **N3-4** 口径纪律：回填只录实测数值与动作记录，禁止由线上单局推导"胜率提升 X%"类派生数字（铁律 4）

## 5. 09-15 切换决策点（主攻/备选裁决）

- [ ] **B14** 若至 09-15 天梯排名趋势 + 迭代边际收益显示投入产出比不佳，启动备选：切 **kaggle-rsna-knee**（10-15 报名截止、10-22 终交）；切换不浪费——本地评估基建（gym 封装 / Elo / 矩阵 / 迭代门）为通用资产；决策由队伍人工裁决（strategy.md 预设兜底路径）

## 6. 终交前检查单（2026-09-30 11:59 PM UTC 前完成，man-final）

- [ ] **B15** **最近 2 次提交为最优版本**（最易翻车项：终交日不做随手提交；如需最后调整，最后两次提交都应是最优候选）
- [ ] **B16** 两次计入提交的 **Validation Episode 均 Passed**（逐条在赛站 Submissions 页核对）
- [ ] **B17** 本地评估最终无回归（§1 四查末次全过）；最优 commit 已记录台账
- [ ] **B18** 无多账号操作；提交文件 stdlib-only、无外部网络依赖
- [ ] **B19** 确认无需再动：榜单 10-01 起继续跑对局至收敛（约 10-15），期间无法改提交

### 新增组 4：终交「最近 2 份最优」锁定检查（本轮新增，man-final 验收强化）

- [ ] **N4-1** 终交日（09-30）**禁止新增实验性提交**——当日仅允许"最优候选重提交"一种操作（且计入 N2-1 额度检查）
- [ ] **N4-2** 最近 2 次提交 = 台账最优候选：**commit hash 双核对**（赛站 Submissions 页逐条 vs 本地《提交台账》）；终版对账结果回填 `metrics.software.final_submission_commits`（当前 null，锁定时落两份 hash）
- [ ] **N4-3** 两次计入提交的 Validation Episode 均 Passed——**双核对**（B16 的逐条复核 + 台账状态列一致），任一不符立即用剩余额度以最优版本覆盖
- [ ] **N4-4** 核对完成后由队伍**人工签字确认**（操作人 + 日期 + 两份 commit hash，记入《提交台账》终交锁定行）——man-final 验收留痕，AI 不代签
- [ ] **N4-5** 签字后向全队通告"提交已锁定"，此后至 10-01 榜单启动前不再触碰提交入口

## 7. 待核项台账（随观察回填，来源 meta.md 待核清单）

| 待核项 | 状态 | 核对方式 |
|---|---|---|
| Entry Deadline 官方数值 | 缺失（API 模板变量未解析） | 第 0 天人工核对赛站（§0 / N1-2，截图回填） |
| 奖池 $50K vs $60K 双口径 | $50K 官方双处直抓采信；$60K 待核 | 赛站奖池徽标 + 列表页截图（B05） |
| agent 运行环境资源限额 | FAQ 模板变量未解析 | 观察线上 Validation/对局日志；bot 保持轻量（B08） |
| API 型 LLM 容器网络策略 | 官方未载明 | 如启用 LLM 模块须先实测；当前默认关、提交形态不依赖（B07） |

## 计数汇总

| 组 | 项数 | 编号 |
|---|---|---|
| 基础（v1 槽位沿用，基线更新） | 19 | B01-B19 |
| 新增组 1 报名前置门 | 3 | N1-1 - N1-3 |
| 新增组 2 每日纪律逐次检查列 | 5 | N2-1 - N2-5 |
| 新增组 3 天梯回填流程 | 4 | N3-1 - N3-4 |
| 新增组 4 终交锁定 | 5 | N4-1 - N4-5 |
| **合计** | **36** | —— |
