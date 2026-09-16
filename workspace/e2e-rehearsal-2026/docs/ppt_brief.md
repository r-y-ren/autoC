# 答辩 PPT 内容简报（ppt_brief）

- 战役：e2e-rehearsal-2026（LA Hacks AI Hackathon 2026 · E2E 彩排靶 · prep 模式）
- 文档性质：K-12 /ppt 第一环产物（战役归档物），交 ppt-master 作内容输入源；产物落位由 ppt-run 路由至 `<战役根>/docs/ppt/`
- 撰写：document 子 agent（verify 态，`acceptance/run-2.json` result=pass 之后、/archive 之前）
- 输入（全只读）：`docs/report.typ`（最终报告源）、`blueprint.md`、`acceptance/run-2.json`、`metrics.json`
- 数字纪律：一切实测数字仅出自 `metrics.software.<键>`（对照表见 §4）；非 metrics 数值仅为任务包给定的彩排假设与结构标识符（声明见 §6）

## 1. 受众与时长（彩排假设）

- 受众：赛事评审（技术背景混合假设；Gate1 沟通契约可校正）
- 时长与篇幅：评审 3 分钟 / 不超过 5 页（彩排假设，任务包给定）；P3 主表为核心停留页
- 目标：讲清"零依赖统计 CLI + 数字逐键可溯源"的主张，并让评审能当场核验数字（P3 主表自带来源键列）

## 2. 核心主张线（一句话）

> 零第三方依赖的统计 CLI 把样例 CSV 一步实测为逐键可溯源的统计 JSON——从实测、核验到叙事全链闭环，验收全项通过。

支撑骨架：工具（P2）→ 实测（P3）→ 质量（P4）→ 叙事（P5）。

## 3. 逐页要点

### P1 · 封面：数据叙事小工具——样例数据统计叙事

- 定位：读 CSV、输出统计 JSON、数字逐键可溯源的命令行工具（blueprint 交付范围）
- 演示数据：样例 CSV（列名 name、score、hours）共 6 行 × 3 列（`metrics.software.rows`、`metrics.software.cols`）
- 背景：LA Hacks AI 2026 E2E 彩排靶；交付物 = 统计 CLI + 一页报告 + 本答辩 PPT

### P2 · 方案：零依赖统计 CLI 与自检

- 工作流：样例 CSV → stats_cli.py → 统计 JSON（数据规模与数值列的非缺失计数、均值、最大值）→ 报告 / PPT 按键消费
- 工程约束：仅 Python 标准库、零第三方依赖（blueprint tech_stack rationale：最小闭环、零依赖可自检）
- 自检：`--check` 自检模式正常退出（验收机检项 a1）

### P3 · 实测结果（核心页 · 全键主表）

- 数据规模：6 行（不含表头）× 3 列 —— `metrics.software.rows`、`metrics.software.cols`
- score 列：非缺失 6 个、均值 88.0、最大 95.0 —— `metrics.software.score_count`、`metrics.software.score_mean`、`metrics.software.score_max`
- hours 列：非缺失 6 个、均值 5.5、最大 8.0 —— `metrics.software.hours_count`、`metrics.software.hours_mean`、`metrics.software.hours_max`

口径注（可作页面脚注）：全部为 stats_cli 实测值（metrics `_meta.method`），无估计/编造；主表第三列即来源键，供评审当场对勘。

### P4 · 质量闭环：从测试到验收

- 单元测试全过（机检 a2）；CLI 自检通过（机检 a1）
- 报告 PDF 数字逐键核验通过（check_report.py，机检 a3）：对外文档零片外数字
- 验收结论：run-2 result=pass，a1/a2/a3 全通过，未触发熔断（`acceptance/run-2.json`）

### P5 · 数据叙事与收束

- 观测完整：score、hours 非缺失计数均为 6，与数据行数一致（`metrics.software.score_count`、`metrics.software.hours_count`、`metrics.software.rows`）
- 高分集中：score 均值 88.0 贴近最大 95.0（`metrics.software.score_mean`、`metrics.software.score_max`）
- 投入不解释成绩：hours 自偏小投入（均值 5.5）至最大投入 8.0 均有覆盖（`metrics.software.hours_mean`、`metrics.software.hours_max`），成绩与投入未见同步消长——收束：这套"读法"由工具可复现、由 metrics 可核验

## 4. 图表清单与数据来源（含数字-键对照）

| 图表 | 位置 | 形式与注意 | 数据来源（键名） |
|---|---|---|---|
| 实测统计主表 | P3 | 指标 / 实测值 / 来源键三列表（沿用报告表式） | `metrics.software.rows`、`metrics.software.cols`、`metrics.software.score_count`、`metrics.software.score_mean`、`metrics.software.score_max`、`metrics.software.hours_count`、`metrics.software.hours_mean`、`metrics.software.hours_max` |
| score / hours 均值-最大值并列图（可选） | P5 | 并列条形；量纲不同（分 / 小时），只并列展示，不作因果或回归主张 | `metrics.software.score_mean`、`metrics.software.score_max`、`metrics.software.hours_mean`、`metrics.software.hours_max` |
| 工作流示意 | P2 | 样例 CSV → stats_cli.py → 统计 JSON → 报告 / PPT；无数字 | blueprint 范围与 `interface/contract.md` |

注：图表只使用 metrics 聚合键；行级原始数据（references 样例 CSV）属登记参考物，不进入 PPT 数字面。

数字-键对照（本简报全部实测数字）：

| 简报数字 | 来源键 |
|---|---|
| 6（数据行数，不含表头；P1/P3/P5） | `metrics.software.rows` |
| 3（数据列数；P1/P3） | `metrics.software.cols` |
| 6（score 非缺失计数；P3/P5） | `metrics.software.score_count` |
| 88.0（score 均值；P3/P5） | `metrics.software.score_mean` |
| 95.0（score 最大值；P3/P5） | `metrics.software.score_max` |
| 6（hours 非缺失计数；P3/P5） | `metrics.software.hours_count` |
| 5.5（hours 均值；P3/P5） | `metrics.software.hours_mean` |
| 8.0（hours 最大值；P3/P5） | `metrics.software.hours_max` |

## 5. 风险与 Q&A 预案

1. **样例规模小，结论代表性存疑** → 预案：明示战役定位为 E2E 彩排靶（prep 范本，blueprint theme），价值在"实测 + 逐键溯源"的方法链而非样例结论本身；数据换代只需重跑 CLI 并刷新 metrics 分片，PPT 数字随键可溯更新。
2. **数字可信度被追问（是否编造）** → 预案：每页数字均带键名，P3 主表第三列即来源键；可当场打开 `metrics.json` 与 `acceptance/run-2.json` 对勘；报告 PDF 已过 check_report.py 逐键核验（a3 通过）。

## 6. 尾注

- **人机分工（一行）**：本简报与全部工程文档由 AI（document 子 agent）撰写，统计工具 / 测试 / 数字核验器由 AI 编写并经人工复核；用户参与蓝图确认与 ppt-master Gate1/Gate2 用户门（对齐 blueprint 人机分工与报告附录）。
- **数字纪律声明**：本简报一切实测数字仅取自 `metrics.json` 的 `metrics.software.<键>` 已有键（值域即 §4 对照表）；出现的其余数值仅为任务包给定的彩排假设（评审时长 3 分钟、篇幅不超过 5 页）与结构 / 流程标识符（页码 P1–P5、验收项 a1–a3、run-2、里程碑 m1/m2 等），均非性能数字，不得作为数据进入 PPT 图表。
