# 能力契约清单（CAPABILITIES.md）

> 版本 v1.0（2026-08-27）｜能力层唯一登记表。
> 规则：**新增能力必须先登记再实现**；已具备的能力只登记、不重复建设。
> 反推链：业务目标（DESIGN.md 双循环）→ 阶段任务 → 能力需求。

---

## 1. 追溯表：业务目标 → 能力需求

| 业务目标 | 阶段任务 | 所需能力（ID 见下文） |
|---|---|---|
| **G1 慢循环·KB 维护** | 赛事发现与网页抓取 | 基线-01/02/03（内建检索、browser-use、CUA）；RSSHub（T3 决策） |
| | API 结构化拉取 | S-02、S-03 脚本；gh / curl（已装）；kaggle CLI（T3+密钥） |
| | 获奖作品逐篇解构 | 基线-04（pdf 技能）；C-01 章程；S-01 校验 |
| | 科技雷达评分入库 | S-03；C-02 章程；min_signal 门槛（directions 配置） |
| | 质量闸与索引重建 | S-01、H-02、S-04；quarantine 流程 |
| | 定时调度与断点续跑 | Cron（内建）；budget.yaml 硬约束 |
| **G2 快循环·作品交付** | 推荐矩阵与蓝图 | K-02；blueprint.schema.json；profile.yaml |
| | 并发工程交付 | K-03；C-03/C-04/C-05 章程；Bash 沙箱；硬件路线（决策 D2） |
| | 实测数据契约 | metrics.json 约定；browser-use 实测取证 |
| | 竞赛文档生成 | K-06、K-07；marp/typst CLI（T3 装）；基线-04/05 |
| | 验收-修复-熔断 | K-04；S-05；H-01 守卫；retry 状态 |
| | 归档 | K-05；S-06；git tag |
| **G3 治理横切** | 写入边界 | H-01（已装）、H-02；各章程禁止清单 |
| | 上下文隔离 | 子 agent 并发（内建）；章程分片纪律；INDEX 只读纪律 |
| | 用户入口与可观测 | M-01…M-05 命令；H-03 状态播报；workspace/JOURNAL.md |

---

## 2. 能力基线（已具备——登记在案，勿重复建设）

### 客户端内建
| ID | 能力 | 用途 |
|---|---|---|
| 基线-01 | WebSearch / WebFetch | L2 信源检索与抓取 |
| 基线-02 | Bash 沙箱 | 编译 / 测试 / 仿真 / CLI 调用 |
| 基线-03 | 子 agent（Agent） | 上下文隔离 + 并发分片 |
| 基线-04 | Cron | 慢循环定时增量 |
| 基线-05 | node_repl | 浏览器自动化运行时 |

### 插件已装
| ID | 能力 | 用途 |
|---|---|---|
| 基线-06 | browser-use（control-browser / web-gui-tester） | JS 渲染页面抓取；前端作品实测取证 |
| 基线-07 | zcode-cua | 图片型获奖名单视觉读取；GUI 软件自测 |
| 基线-08 | document-skills（docx/pptx/pdf/xlsx） | 申报书/BP/论文/财务表格生成——**挑战杯类文档直接复用，不自研** |
| 基线-09 | diagram-maker | 论文/BP 架构图与配图 |

### 本地 CLI（已安装）
git 2.48｜python 3.14（+3.12 备用）｜node 24 / npm 11｜gh 2.92｜curl 8.12

---

## 3. 能力缺口（待赋予）

### 3.1 钩子（.zcode/config.json → hooks.events）

| ID | 能力 | 依赖 | 状态/层 |
|---|---|---|---|
| H-01 | PreToolUse 写入路径守卫 | scripts/guard/guard_path.py | ✅ Phase 0 已装（冒烟 10/10） |
| H-02 | PostToolUse KB 即时校验（kb/ 写入即跑 lint，不合格当场反馈） | S-01 + pyyaml/jsonschema | ✅ 本轮已装（钩子模式验证通过） |
| H-03 | SessionStart 状态播报（当前阶段/战役/熔断计数） | .flow/state.json | T2 |

### 3.2 脚本（scripts/）

| ID | 能力 | 说明 | 层 |
|---|---|---|---|
| S-01 | lint_kb.py | frontmatter 解析 → schema 校验 → 不合格移 quarantine（单文件/钩子/全量三模式；YAML 日期已规范化） | ✅ 本轮已落地 |
| S-02 | sync_competitions.py | API/聚合源增量拉取赛事（arXiv/gh/curl 起点） | T2·模块期 |
| S-03 | sync_tech.py | 科技雷达：拉取→主键去重→信号评分→卡片骨架 | T2·模块期 |
| S-04 | build_index.py | 重建 kb/INDEX.md（瘦协调者入口） | T2 |
| S-05 | run_acceptance.py | 验收执行器：跑清单、记证据、开工单、更新 retry | T2 |
| S-06 | archive_campaign.py | workspace → archive/（mv + git tag + 只读）→ 复位 | T2 |
| S-07 | test_guard.py | 守卫回归测试 | ✅ 本轮已落地（14/14 通过） |

### 3.3 角色章程（.zcode/agents/）——能力契约本体

| ID | 角色 | 允许写根（与 DESIGN §6.2 一致） | 层 |
|---|---|---|---|
| C-01 | scraper | kb/competitions/、kb/raw/ | ✅ 本轮已落盘（.zcode/agents/scraper.md） |
| C-02 | hunter | kb/tech/、kb/raw/ | ✅ 本轮已落盘（hunter.md） |
| C-03 | software | workspace/software/、workspace/metrics.json | ✅ 本轮已落盘（software.md） |
| C-04 | hardware | workspace/hardware/ | ✅ 本轮已落盘（hardware.md，按 D2=CLI 优先编写） |
| C-05 | document | workspace/docs/（数字仅引 metrics.json） | ✅ 本轮已落盘（document.md） |
| C-06 | acceptor | workspace/acceptance/（只开工单不修作品） | ✅ 本轮已落盘（acceptor.md） |

> Strategy 不设子 agent 章程：决策阶段需要与用户交互，运行在主会话，其规程并入 K-02 技能。

### 3.4 技能（.zcode/skills/）

| ID | 技能 | 职责（SOP） | 层 |
|---|---|---|---|
| K-01 | kb-sync | 慢循环编排：读方向配置→collect 态→分片派发 C-01/C-02→API 脚本→S-01→S-04→changelog+commit→idle | T2 |
| K-02 | strategy-gen | 读 INDEX+profile→矩阵/一鱼多吃/蓝图草稿→schema 校验→呈报用户（唯一闸门） | T2 |
| K-03 | campaign-run | 读蓝图→deliver 态→任务包→并发派发→汇合派发 C-05→JOURNAL | T2 |
| K-04 | accept-run | verify 态→S-05→工单路由回环（熔断）→分析报告 | T2 |
| K-05 | archive-run | archive 态→S-06→workspace 复位→idle | T2 |
| K-06 | marp-deck | 模板+metrics→答辩 PPT（marp-cli 导出 pptx） | T2 |
| K-07 | typst-report | 模板+metrics→报告 PDF（typst） | T2 |

### 3.5 命令（.zcode/commands/）——用户入口

| ID | 命令 | 作用 | 层 |
|---|---|---|---|
| M-01 | /kb-sync | 手动触发慢循环（cron 之外的补偿入口） | ✅ 本轮已落盘（契约入口，指向 K-01） |
| M-02 | /attack | 发起快循环：刷新 KB→K-02 决策 | ✅ 本轮已落盘（契约入口，指向 K-02） |
| M-03 | /status | 查 phase/战役/JOURNAL/熔断 | ✅ 本轮已落盘（即时可用） |
| M-04 | /accept | 手动触发验收（K-04） | ✅ 本轮已落盘（契约入口，指向 K-04） |
| M-05 | /archive | 手动归档（K-05） | ✅ 本轮已落盘（契约入口，指向 K-05） |

### 3.6 外部引入（安装/密钥/部署）

| ID | 项 | 用途 | 引入条件 | 层 |
|---|---|---|---|---|
| E-01 | marp-cli（npm） | PPT 导出 | K-06 启用时 | T3 |
| E-02 | typst（winget） | 报告排版 | K-07 启用时 | T3 |
| E-03 | platformio（pip·挂 3.12） | 固件编译测试 | 硬件模块启用时 | T3 |
| E-04 | kicad（winget，含 kicad-cli） | PCB 生成 | 硬件模块启用时 | T3 |
| E-05 | wokwi-mcp | 有状态电路仿真（官方 MCP） | 路线决策 D2 | T3 |
| E-06 | kicad-mcp（社区） | PCB 交互生成 | 可选，逐个评估 | T3 |
| E-07 | RSSHub | 公众号信源中转 | 慢循环公众号策略确定时 | T3 |
| E-08 | Kaggle API key | 赛题/榜单拉取 | Kaggle 方向启用时（用户提供） | T3 |

---

## 4. 能力选型原则

**内建 > CLI（Bash 调用）> 自研脚本 > MCP**。MCP 仅在需要*有状态交互*（如 Wokwi 仿真会话）或封装复杂协议时引入；纯命令行可解决的不引 MCP，控制外部依赖面与信任面。外部 MCP 接入前逐个评估（来源、维护状态、权限面）。

## 5. 分层推进

- **T1 能力契约固化（本轮）**：✅ 完成——S-01、S-07、H-02、C-01…C-06、M-01…M-05、本文档；验证：守卫回归 14/14，lint 三模式（单文件/钩子/全量+隔离）实测通过
- **T2 编排技能与慢循环脚本**：K-01…K-07、S-02…S-06、H-03
- **T3 外部接入（按模块启用）**：E-01…E-08

## 6. 决策记录

- **D1 赋能范围** ✅ 已裁决（2026-08-27）：选 **T1 契约固化**——技能（K-*）留到模块实现期随脚本一起固化，避免引用空壳脚本的死 SOP
- **D2 硬件能力路线** ✅ 已裁决（2026-08-27）：选 **CLI 优先**——pio/kicad-cli/wokwi CLI 全走 Bash；E-05（wokwi-mcp）/E-06（kicad-mcp）后置，仅当实测需要仿真会话级有状态交互时再评估引入；C-04 章程已按此路线编写
