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
| H-03 | SessionStart 状态播报（当前阶段/战役/熔断计数） | scripts/guard/session_status.py | ✅ T2 已装（additionalContext 注入验证通过） |

### 3.2 脚本（scripts/）

| ID | 能力 | 说明 | 层 |
|---|---|---|---|
| S-01 | lint_kb.py | frontmatter 解析 → schema 校验 → 不合格移 quarantine（单文件/钩子/全量三模式；YAML 日期已规范化） | ✅ 本轮已落地 |
| S-02 | sync_competitions.py | web 信源快照（kb/raw/snapshots/）+ 关键词候选提取（candidates 队列） | ✅ T2 已落地（selftest 通过） |
| S-03 | sync_tech.py | arXiv API + gh 搜索 → 规范化 ID 去重 → 候选队列（成品卡片仍由 Hunter 判定；field 间限速 ≥3s + 失败退避重试，兑现 budget.yaml） | ✅ T2 落地，T3-c 补限速 |
| S-04 | build_index.py | 重建 kb/INDEX.md（跑批记录 append-only 保留） | ✅ T2 已落地 |
| S-05 | run_acceptance.py | 验收执行器：cmd 自动执行 + 证据存档 + 重试熔断 + run-N.json | ✅ T2 已落地（冒烟通过） |
| S-06 | archive_campaign.py | fail 拒归档 / dry-run / mv + git tag + workspace 复位 + idle | ✅ T2 已落地（冒烟通过） |
| S-07 | test_guard.py | 守卫回归测试 | ✅ 本轮已落地（16/16 通过） |
| S-08 | test_lint.py | lint 回归测试（目标识别/日期格式/跳过清单，12 用例） | ✅ T2 校准已落地（12/12 通过） |
| S-09 | merge_metrics.py | 角色指标分片 → 顶层汇总（metrics.<role>.<键>；K-03 前置项落地） | ✅ T2 已落地 |
| S-10 | test_acceptance.py | 验收执行器回归（cmd/超时杀树/仅fail计数/schema，5 用例） | ✅ T2.1 已落地（5/5） |
| S-11 | test_archive.py | 归档闸门回归（pending_agent/fail/pass 含 tag 内容审计，4 用例） | ✅ T2.1 已落地（4/4） |
| S-12 | test_index.py | 索引回归（跑批记录多行 append-only 保留） | ✅ T2.1 已落地 |
| S-13 | ocr_pdf.py | PDF 解析：有文本层直取；无文本层逐页渲染 → tesseract OCR → 文本 + 置信度报告（判断仍归 Scraper） | ✅ T3-c 本轮落地 |
| S-15 | export_digest.py | 方向情报简报导出（D6 交付层）：条目层纯投影 → export/digest-<方向>-<月>.md，每3天跑批刷新/当月最后一次跑批自动转正式版 | ✅ T3-d 落地（selftest 通过） |

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
| K-01 | kb-sync | 慢循环编排：读方向配置→collect 态→分片派发 C-01/C-02→API 脚本→S-01→S-04→changelog+commit→idle | ✅ T2 已落地 |
| K-02 | strategy-gen | 读 INDEX+profile→矩阵/一鱼多吃/蓝图草稿→schema 校验→呈报用户（唯一闸门） | ✅ T2 已落地 |
| K-03 | campaign-run | 读蓝图→deliver 态→任务包→并发派发→merge_metrics 汇总→派发 C-05→JOURNAL | ✅ T2 已落地（前置项已按 D3 裁决） |
| K-04 | accept-run | verify 态→S-05→工单路由回环（熔断）→分析报告 | ✅ T2 已落地 |
| K-05 | archive-run | archive 态→S-06→workspace 复位→idle | ✅ T2 已落地 |
| K-06 | marp-deck | 模板+metrics 汇总→答辩 PPT（marp-cli 导出 pptx） | ✅ T2 已落地 |
| K-07 | typst-report | 模板+metrics 汇总→报告 PDF（typst） | ✅ T2 已落地 |
| K-08 | kb-deep-sync | 慢循环全量深度跑批（D7 每 3 天）：增量入库+老化重验(12d)/拒绝台账复核/quarantine 清理/winners-patterns 推进/简报导出 | ✅ T3-c 落地，T3-d 按 D7 合并节奏改写 |

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
| E-01 | marp-cli（npm） | PPT 导出 | ✅ T3-c 已装（4.5.0，模板冒烟通过） | T3 |
| E-02 | typst（winget） | 报告排版 | ✅ T3-c 已装（0.15.1，模板冒烟通过） | T3 |
| E-03 | platformio（pip·挂 3.12） | 固件编译测试 | ✅ T3-d 已装（6.1.19，native 编译运行冒烟通过） | T3 |
| E-04 | kicad（winget，含 kicad-cli） | PCB 生成 | ✅ T3-d 已装（10.0.5，gerber 导出冒烟通过；用户级路径见 ENVIRONMENT） | T3 |
| E-05 | wokwi-mcp | 有状态电路仿真（官方 MCP） | 路线决策 D2（仅实测需要会话级交互时评估） | T3 |
| E-06 | kicad-mcp（社区） | PCB 交互生成 | 可选，逐个评估 | T3 |
| E-07 | RSSHub | 公众号信源中转 | D5 缓判至挑战杯类方向启用；届时 clone 进 tools/ | T3 |
| E-08 | Kaggle API key | 赛题/榜单拉取 | Kaggle 方向启用时（用户提供） | T3 |
| E-09 | Tesseract OCR（UB-Mannheim，含 chi_sim） | 扫描件 PDF/图片文字化（S-13 依赖） | ✅ T3-c 已装 | T3 |
| E-10 | pypdfium2 / pdfplumber / pillow | PDF 渲染与表格化（S-13 及 Scraper 表格分片） | ✅ T3-c 已装 | T3 |
| E-11 | OpenSCAD | 结构件代码化生成 → STL（hardware 章程已引用） | ✅ T3-d 已装（无头 STL 冒烟通过） | T3 |
| E-13 | MPLAB XC8 | PIC18F 固件编译（PlatformIO 不支持 PIC；profile 设备含 pic18f） | 按需：首个用到 PIC 的蓝图出现时先评估再装 | T3 |
| E-12 | Wokwi CLI | 固件仿真自测（--expect-text 断言式验收） | ✅ T3-e 已装并断言冒烟通过（0.26.1；官方件+自建 Arduino ESP32 双验证；Community License=公开/开源项目口径） | T3 |

---

## 4. 能力选型原则

**内建 > CLI（Bash 调用）> 自研脚本 > MCP**。MCP 仅在需要*有状态交互*（如 Wokwi 仿真会话）或封装复杂协议时引入；纯命令行可解决的不引 MCP，控制外部依赖面与信任面。外部 MCP 接入前逐个评估（来源、维护状态、权限面）。

## 5. 分层推进

- **T1 能力契约固化**：✅ 完成——S-01、S-07、H-02、C-01…C-06、M-01…M-05、本文档；验证：守卫回归 14/14，lint 三模式（单文件/钩子/全量+隔离）实测通过
- **T2 编排技能与慢循环脚本**：✅ 完成——S-02…S-06、S-09、K-01…K-07、H-03；验证：守卫 16/16、lint 12/12、三脚本 selftest、验收/汇总/归档链路隔离冒烟（fail 拒归档、tag、复位、retry 累计）
- **T2.1 修复轮（审查驱动）**：✅ 完成——5 个实测缺陷（跑批记录丢行 / pending_agent 绕闸门 / tag 先于 commit / cmd 超时崩溃+孤儿进程劫持 / 循环变量泄漏）+ 2 语义裁决（见 D4）+ retry.max 单一事实来源；新增 S-10/S-11/S-12 三套回归，全量 12+5+4+1 用例通过
- **T3 外部接入（按模块启用）**：E-01…E-04/E-09…E-11 已装并冒烟；E-05…E-08/E-12 按需（凭据/方向类）
- **T3-d 能力收口轮**：✅ 完成（2026-08-27）——硬件三件套安装冒烟（pio/kicad-cli/openscad）、S-15 简报导出层、K-01/K-08 预检+收尾断言、验收 cmd 模板库、D6 交付层裁决

## 6. 决策记录

- **D1 赋能范围** ✅ 已裁决（2026-08-27）：选 **T1 契约固化**——技能（K-*）留到模块实现期随脚本一起固化，避免引用空壳脚本的死 SOP
- **D2 硬件能力路线** ✅ 已裁决（2026-08-27）：选 **CLI 优先**——pio/kicad-cli/wokwi CLI 全走 Bash；E-05（wokwi-mcp）/E-06（kicad-mcp）后置，仅当实测需要仿真会话级有状态交互时再评估引入；C-04 章程已按此路线编写
- **D3 K-03 前置项处置** ✅ 已裁决并落地（2026-08-27，T2）：
  1. metrics 并发风险 → **分片制**（角色写 workspace/<role>/metrics.json，S-09 汇总为顶层生成物，守卫 deliver 态拒写该生成物；三份章程同步，回归用例固化）
  2. 角色身份级守卫 → **v1 不引入**（钩子负载无调用者身份；全局 active_role 破坏并发派发）。跨角色越界维持 L1 章程 + L3 git 审计；真实写冲突点已被分片制消除
- **D4 T2.1 语义裁决** ✅ 已裁决（2026-08-27，审查修复轮）：
  1. retry 计数语义 → **仅 result=fail 计入**（pending_manual/pending_agent 是"等待"不是"修复失败重试"，manual-heavy 战役不应因状态检查误触熔断）
  2. 候选队列生命周期 → **消费即归档**（K-01 消费后移 candidates/processed/）+ **拒绝台账**（kb/tech/.rejections.yaml：id/reason/stars/decided；stars 达快照 ×2 自动放行重评，解决"10 星被拒的仓库涨到 500 星也进不了候选"的信号增长堵点）
  3. retry.max 单一事实来源 → **config/budget.yaml**（init_state.py / run_acceptance.py 均读取）
- **D5 T3-c 能力补全裁决** ✅ 已裁决（2026-08-27）：
  1. MCP 结论 → **本轮零新增 MCP**（OCR/表格/视觉/文档链全部有 CLI/内建解，符合 §4 选型原则）；E-07 RSSHub **缓判**至挑战杯/创新创业类方向启用时再裁决，届时 clone 进 `tools/`（gitignore，本机 node 直跑，不用 docker）
  2. 第三方开源工具落位纪律 → 一律 clone 进 gitignored `tools/` + ENVIRONMENT.md 记版本，不污染 git 主干与审计面
  3. S-13 编号说明 → 计划稿的 "S-12 ocr_pdf" 与已登记 S-12（test_index）撞号，OCR 脚本按 **S-13** 登记
  4. 双频慢循环 → 每日轻量增量 + 每周深度评估（**已被 D7 修订**为每 3 天全量深度单 cron）
- **D6 知识库交付层裁决** ✅ 已裁决（2026-08-27，T3-d）：
  1. 读者 → **团队自用**（决策输入口径：直接给结论与证据链，合规红线照实写；导览见 kb/README.md）
  2. 形式 → **源库不动，导出层纯投影**——export/digest-<方向>-<月>.md 方向情报简报（S-15 生成：赛事日历倒计时/技术雷达速览/patterns 第五节/合规提醒）；每条结论回链条目 ID，**分析增量只允许发生在条目层**，导出物是纯重组
  3. 节奏 → ~~挂周深度 cron~~（D7 修订：每 3 天跑批刷新草稿，当月最后一次跑批自动转正式版，判定内置 S-15 `--interval-days`）；深度赛事攻略包（Typst 编译）待 patterns 覆盖 ≥2 赛后按需启动

- **D7 慢循环调度合并** ✅ 已裁决（2026-08-27，用户指令）：原"每日轻量 + 每周深度"双 cron 合并为**每 3 天 09:00 一次全量深度**（automation-617d9635）。配套：①K-08 改写为全量 SOP（含增量拉取步骤；K-01 保留为手动轻量补偿入口）；②老化重验阈值 14→12 天对齐节奏；③S-15 正式版判定由"最后一个周六"改为"当月最后一次跑批（today+interval 跨月）"，新增 `--interval-days`（默认 3）

- **D8 EDA/仿真工具面评估** ✅ 已裁决（2026-08-27，T3-e）：
  1. Wokwi CLI → **已装**（官方安装脚本，非 npm；Community License 对公开/开源项目免费，token 已配置）。`--expect-text/--fail-text` 提供断言式仿真验收，接入 acceptance-cmds 模板
  2. EDA MCP（E-05 wokwi-mcp / E-06 kicad-mcp）→ **维持不引入**：KiCad 工程（.kicad_sch/.kicad_pcb）为文本 s-表达式，agent 可在守卫边界内直接生成/编辑；kicad-cli 覆盖 DRC 与 gerber/钻孔/贴装等制造输出；无"会话级有状态交互"需求即不引 MCP（§4 选型原则）
  3. HDL 分析/仿真 → 未启用；首个含 HDL 里程碑的蓝图出现时再评估（yosys/iverilog CLI 可覆盖，届时按"先登记再实现"办理，登记为 E-14+）
  4. PIC18F 工具链缺口 → 如实登记 E-13（MPLAB XC8，按需未装），不假装 PlatformIO 可覆盖

- **D9 审查遗留项闭合** ✅ 已裁决（2026-08-27，全量门禁审查后修复轮）：
  1. retry.max **实时同步**（取消快照语义）：run_acceptance 每次读取、init_state 每次流转都从 budget 刷新 max（保留 count/tripped；budget 不可读时不覆盖已有值）；test_acceptance 增场景 E 固化
  2. same_host_interval_ms **落脚本**：sync_competitions 同主机抓取间隔强制执行（rps 总约束仍为技能层，budget 头注如实标注）
  3. tech-card **directions 字段落地**（原"第二方向启用前再做"提前完成）：schema 可选字段、sync_tech 候选自动打标（多方向合并）、hunter 章程继承、INDEX 增方向列、简报按方向过滤（未标注卡不进方向简报）、存量 6 卡已回填
  4. export_digest.py 内部 2 处 D7 措辞残留修复（审查漏掉的第 5/6 处：文件头注释与 patterns 占位句）
