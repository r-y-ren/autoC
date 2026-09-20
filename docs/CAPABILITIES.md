# 能力契约清单（CAPABILITIES.md）

> 版本 v1.0（2026-08-27）｜能力层唯一登记表。
> 规则：**新增能力必须先登记再实现**；已具备的能力只登记、不重复建设。
> 反推链：业务目标（DESIGN.md 双循环）→ 阶段任务 → 能力需求。

---

## 1. 追溯表：业务目标 → 能力需求

| 业务目标 | 阶段任务 | 所需能力（ID 见下文） |
|---|---|---|
| **G1 慢循环·KB 维护** | 赛事发现与网页抓取 | 基线-01/02/03（内建检索、browser-use、CUA）；E-17 Trafilatura（静态页正文降噪）；RSSHub（T3 决策） |
| | API 结构化拉取 | S-02、S-03 脚本；gh / curl（已装）；E-16 DuckDB（大表聚合）；kaggle CLI（T3+密钥） |
| | 获奖作品逐篇解构 | 基线-04（pdf 技能）；E-14 MinerU；E-15 ast-grep（陌生库 AST 检索）；C-01 章程；S-01 校验 |
| | 科技雷达评分入库 | S-03；C-02 章程；min_signal 门槛（directions 配置） |
| | 质量闸与索引重建 | S-01、H-02、S-04；quarantine 流程 |
| | 定时调度与断点续跑 | Cron（内建）；budget.yaml 硬约束 |
| **G2 快循环·作品交付** | 推荐矩阵与蓝图 | K-02；blueprint.schema.json；profile.yaml |
| | 并发工程交付 | K-03；C-03/C-04/C-05 章程；Bash 沙箱；E-15 ast-grep；E-18 bwrap（不可信代码隔离）；硬件路线（决策 D2） |
| | 实测数据契约 | metrics.json 约定；browser-use 实测取证 |
| | 竞赛文档生成 | K-06、K-07（marp=波内草稿）；正式答辩 PPT=K-12（ppt-master 双用户门，票10）；基线-04/05 |
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
git 2.48｜python 3.14（+3.12 备用）｜node 24 / npm 11｜gh 2.92｜curl 8.12｜ast-grep 0.45｜duckdb 1.5（Linux 主力机 ~/.local/bin 静态二进制）

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
| S-01 | lint_kb.py | frontmatter 解析 → schema 校验 → 不合格移 quarantine（单文件/钩子/全量三模式；YAML 日期已规范化；T4.3 增正文层 `--structure` 检查：winners 四节/patterns 六节/survey 必备节，WARN 级不隔离） | ✅ 本轮已落地 |
| S-02 | sync_competitions.py | web 信源快照（kb/raw/snapshots/）+ 关键词候选提取（candidates 队列） | ✅ T2 已落地（selftest 通过） |
| S-03 | sync_tech.py | arXiv API + gh 搜索 + **HF Papers（/api/daily_papers，T4.4 接入：upvotes 门槛+方向关键词过滤，与 arXiv 共用 arxiv-* ID 自然去重，PwC 继任者）** → 规范化 ID 去重 → 候选队列（成品卡片仍由 Hunter 判定；field 间限速 ≥3s + 失败退避重试） | ✅ T2 落地，T3-c 限速，T4.4 增 HF 源（实测黑客松方向产出真实候选） |
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
| S-16 | inbox_intake.py | kb/inbox/ 外来资料消费（票03）：三分路由/配额/未溯源线索/战役提示；test_inbox 10/10 | ✅ 2026-09-16 升级票03 |
| S-17 | vault_bib_backfill.py | my_LLM_valut bib→citekey 映射回填（票04，一次性；DOI 覆盖 91%） | ✅ 一次性已用毕（vault 已删） |
| S-18 | contract_check.py | 契约版本本地 vs 上游校验（票01 补全：多机错配防护） | ✅ 2026-09-16 升级票01 |
| S-19 | test_guard_seam.py | 守卫缝回归 16 例（票10 review-fix：verify docs/JOURNAL、decide strategy/、specs/、三不变量） | ✅ 2026-09-16 升级票10 |

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
| K-01 | kb-sync | 慢循环编排：读方向配置→collect 态→分片派发 C-01/C-02→API 脚本→S-01→S-04→changelog+commit→idle；inbox 投递箱消费（S-16·票03） | ✅ T2 已落地（票03 增补） |
| K-02 | strategy-gen | grilling 前置（票07·strategy/grill-notes）→读 INDEX+profile→矩阵/一鱼多吃/蓝图草稿（含 auto_chain 开关行·票08）→schema 校验→呈报用户（唯一闸门） | ✅ T2 已落地（票07/08 增补） |
| K-03 | campaign-run | 读蓝图→deliver 态→auto_chain 时 planner 先行规格派生（票09·specs/，拓扑不变）→任务包（票单细化）→并发派发（software 包级自检前置）→波门→merge_metrics→C-05→JOURNAL | ✅ T2 已落地（票09 增补） |
| K-04 | accept-run | verify 态→S-05→工单路由回环（熔断）→分析报告 | ✅ T2 已落地 |
| K-05 | archive-run | archive 态→S-06→workspace 复位→idle | ✅ T2 已落地 |
| K-06 | marp-deck | 模板+metrics 汇总→答辩 PPT 波内草稿（票10 降级定位；正式产线=K-12 /ppt） | ✅ T2 已落地（票10 降级） |
| K-07 | typst-report | 模板+metrics 汇总→报告 PDF（typst） | ✅ T2 已落地 |
| K-09 | direction-discovery | 方向冷启动：信源目录驱动搜索分片→筛选建条→锚点回填→全景报告（框架泛化入口） | ✅ 批次1已落地 |
| K-08 | kb-deep-sync | 慢循环全量深度跑批（D7 每 3 天）：增量入库+老化重验(12d)/拒绝台账复核/quarantine 清理/winners-patterns 推进/简报导出 | ✅ T3-c 落地，T3-d 按 D7 合并节奏改写 |
| K-10 | kb-full-build | 全量知识库一次性构建编排（D11：W0-W5 波次、配额豁免质量不降） | ✅ D11 已落地（补登 2026-09-02） |
| K-11 | self-run | 人工主导交付会话（D13 副驾模式）：豁免瘦协调者/角色矩阵/波次编排（限战役根内），不变量照旧，蓝图改必校验留痕，熔断人工接管出口 | ✅ 2026-09-02 已落地 |
| K-12 | ppt-run | 正式答辩 PPT 产线（升级票10）：/accept 通过后、/archive 前——document 产内容简报（数字只出自 metrics）→ ppt-master Default 双用户门（Gate1/2），项目路由 docs/ppt/；Marp（K-06）降为波内草稿 | ✅ 2026-09-16 升级票10 |
| K-13 | ppt-self | PPT 阶段人工副驾（升级票11）：/self 同款语义限 docs 子树——人指挥微调简报/版式/pptx，数字回 metrics 溯源，与 /ppt 互换续跑 | ✅ 2026-09-16 升级票11 |

### 3.5 命令（.zcode/commands/）——用户入口

| ID | 命令 | 作用 | 层 |
|---|---|---|---|
| M-01 | /kb-sync | 手动触发慢循环（cron 之外的补偿入口） | ✅ 本轮已落盘（契约入口，指向 K-01） |
| M-02 | /attack | 发起快循环：刷新 KB→K-02 决策 | ✅ 本轮已落盘（契约入口，指向 K-02） |
| M-03 | /status | 查 phase/战役/JOURNAL/熔断 | ✅ 本轮已落盘（即时可用） |
| M-04 | /accept | 手动触发验收（K-04） | ✅ 本轮已落盘（契约入口，指向 K-04） |
| M-06 | /discover | 方向冷启动入口（指向 K-09） | ✅ 批次1已落地 |
| M-07 | /deliver | 交付会话入口（指向 K-03；多会话工作流的制作起点，含 mode 闸门与跨会话续跑说明） | ✅ 2026-08-28 已落地 |
| M-05 | /archive | 手动归档（K-05） | ✅ 本轮已落盘（契约入口，指向 K-05） |
| M-08 | /self | 人工主导交付入口（指向 K-11；/deliver 的姊妹入口，人指挥主会话直接动手；熔断后人工接管亦走此） | ✅ 2026-09-02 已落地 |
| M-12 | /ppt | 正式答辩 PPT 入口（指向 K-12；窗口=/accept 通过后、/archive 前；细节微调姊妹入口 /ppt-self） | ✅ 2026-09-16 升级票10 |
| M-13 | /ppt-self | PPT 阶段人工副驾入口（指向 K-13；/ppt 的姊妹入口，豁免限 docs 子树） | ✅ 2026-09-16 升级票11 |

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
| E-14 | MinerU 4（pip·专用 venv `~/.venvs/mineru`，py3.12+torch 2.14 CPU） | 文档→Markdown 本地解析与查阅（版面/表格/公式/OCR；**原生直通 22 类输入**：pdf/图片/Office/ODF/html/epub/csv/ofd 等，soffice 后备；doclib 定位符 read/search 按页查阅）——C-01/C-02 难读文档主力，S-13 降为无环境兜底；全局技能 `~/.zcode/skills/mineru/`（wrapper+查阅循环 SOP） | ✅ 2026-09-20 已装并验证（standard 档 VLM；文本层 17页/11s 表格完整还原、扫描件 OCR、原生 docx/pptx/html、locator 查阅循环均通过；**--remote 云解析按合规禁用**；Linux 主力机） | T3 |
| E-15 | ast-grep（静态二进制 ~/.local/bin） | AST 结构化代码检索/重构（software 解构陌生开源库；与 rg 互补） | ✅ 2026-09-20 已装（D15） | T3 |
| E-16 | DuckDB CLI（静态二进制 ~/.local/bin） | 本地 CSV/Parquet/JSON 大表聚合（hunter/software 交互式探索；脚本保持 stdlib 不接线） | ✅ 2026-09-20 已装（D15） | T3 |
| E-17 | trafilatura（autoc venv） | 静态页正文降噪：S-02 快照旁 `.extract.md` sidecar（try-import 降级）+ scraper 分片首选 | ✅ 2026-09-20 已装（D15） | T3 |
| E-18 | bwrap 0.12（系统包）+ wrapper 技能 ~/.zcode/skills/bwrap-run | 不可信第三方代码执行隔离（根只读+默认断网；仅点名场景强制，日常编译测试不套） | ✅ 2026-09-20 登记封装（D15） | T3 |
| E-19 | 本地轻量 VL（Ollama/qwen2.5-vl） | 4.5v 远程视觉分流兜底 | watch：限流实证 ≥2 次再评（本机无独显+RAM 紧张，D15） | T3 |
| — | Docling | 表格/公式结构化第二主力候选 | watch：MinerU standard 档出现表格还原系统性缺陷实证再评（D15；S-13 无环境兜底语义不动） | T3 |

---

## 4. 能力选型原则

**内建 > CLI（Bash 调用）> 自研脚本 > MCP**。MCP 仅在需要*有状态交互*（如 Wokwi 仿真会话）或封装复杂协议时引入；纯命令行可解决的不引 MCP，控制外部依赖面与信任面。外部 MCP 接入前逐个评估（来源、维护状态、权限面）。

## 5. 分层推进

- **T1 能力契约固化**：✅ 完成——S-01、S-07、H-02、C-01…C-06、M-01…M-05、本文档；验证：守卫回归 14/14，lint 三模式（单文件/钩子/全量+隔离）实测通过
- **T2 编排技能与慢循环脚本**：✅ 完成——S-02…S-06、S-09、K-01…K-07、H-03；验证：守卫 16/16、lint 12/12、三脚本 selftest、验收/汇总/归档链路隔离冒烟（fail 拒归档、tag、复位、retry 累计）
- **T2.1 修复轮（审查驱动）**：✅ 完成——5 个实测缺陷（跑批记录丢行 / pending_agent 绕闸门 / tag 先于 commit / cmd 超时崩溃+孤儿进程劫持 / 循环变量泄漏）+ 2 语义裁决（见 D4）+ retry.max 单一事实来源；新增 S-10/S-11/S-12 三套回归，全量 12+5+4+1 用例通过
- **T3 外部接入（按模块启用）**：E-01…E-04/E-09…E-11 已装并冒烟；E-05…E-08/E-12 按需（凭据/方向类）
- **T3-d 能力收口轮**：✅ 完成（2026-08-27）——硬件三件套安装冒烟（pio/kicad-cli/openscad）、S-15 简报导出层、K-01/K-08 预检+收尾断言、验收 cmd 模板库、D6 交付层裁决
- **T4.3 改进轮**：✅（2026-08-28）——远程备份（r-y-ren/autoC 私有仓 + 跑批收尾自动 push）；正文层结构 lint（首跑抓 3 真实漂移）；scraper/hunter 自检强制化 + K-02 证据强度标注；INDEX 跑批表成本列（分片/token/墙钟）
- **T4.1 工作流完善轮（P1-P4）**：✅（2026-08-27）——P1 SPA 抓取修复（catalog SPA 清单 + 主会话预抓规则 + scraper 章程『搜索快照禁作唯一事实源』，Nova 事故机制化）；P2 _surveys 生产触发必查（≥3 卡 / 30 天 / maturity 变化）；P3 作品分析报告模板（六节，挂 acceptor）；P4 watch 项扫描进 K-08 预检
- **T4 内容框架轮（批次 1 框架件）**：✅（2026-08-27）——schema 三改（meta.award_levels 数据驱动覆盖标准 / tech-card.directions 转必填 / competition_fit.track 六值词表枚举）；winners/patterns/survey 三通用模板（去特化措辞，四节深构含"不足与可改进点"）；config/sources/catalog.md 信源目录；K-09+M-09 落盘；K-02"大显身手"信号显式化；存量 6 卡 track 词表回填

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

- **D10 第三类交付物细节裁决** ✅ 已裁决并落地（2026-08-28，用户四项拍板）：
  1. 攻略载体 → **strategy.md 模板化**（六节：情报摘要/六维矩阵/大显身手信号/一鱼多吃/合规风险/推荐结论；不另造导出层，随归档保留）
  2. 合规模式 → **三分进 schema 硬校验**：compliance.mode ∈ prep（赛前范本级，默认）/ apply（申报制参赛型，须附 policy_basis 原文摘引）/ assist（赛中支持，零介入）；if/then 硬校验 apply/assist 必带佐证
  3. 建议呈报 → **矩阵+明确推荐**（四块固定格式：六维矩阵含一句证据/大显身手信号行含卡片 ID/一鱼多吃路线图/推荐第一名+理由+备选；无可推荐窗口时诚实兜底禁止硬推）
  4. 快循环整链验证 → **暂不验证**（用户裁定时机；机制全绿状态维持，D10 如实记录不催办）
  落地件：strategy-template / blueprint-template（含"完整可实用"四标准与分类型验收默认线）/ blueprint.schema compliance 改造 / K-02 呈报流程改写 / test_lint 夹具同步

- **D11 全量构建裁决** ✅（2026-08-28，用户指令"不限 token"）：一次性全量知识库构建（K-10 编排）——
  cron 暂停（规格存 PENDING-CRON.md，完成后恢复）、配额豁免但质量门槛不降、W0-W5 波次推进每波提交、
  完成标准=结构 lint 零 WARN + 队列清空 + 全 patterns 六节 + surveys 按族 + 正式简报

- **D12 波次化交付落地** ✅（2026-08-28，首场战役实证驱动）：K-03 从"按角色归并三包单趟"重构为
  **依赖图驱动的波次编排**——milestones.depends_on 拓扑分层成波（环检测 fail-fast；无依赖轻蓝图自然单波向后兼容）、
  波内并行派发、波间质量门（可编译/测试/接口契约/metrics 落盘/JOURNAL+commit，波门即断点）、
  document 双阶段（第 1 波大纲包+末波成稿包）、验收左移（run_acceptance --only 前缀过滤：
  scoped 诊断不烧熔断额度、result 封顶 pending_agent 防误开归档闸）；blueprint-template 增
  骨架→竖切→完整→打磨四阶段默认模板。验证：test_acceptance 增场景 F（7/7），全量回归绿。

- **D13 人工主导交付会话** ✅ 已裁决并落地（2026-09-02，用户指令）：补齐 /attack 确认后"只有 /deliver
  自动编排、人工直接指挥会被章程/铁律限制"的缺口——新增 M-08 /self + K-11 self-run（副驾模式）：
  1. **零机制改动**：不新增阶段、不改守卫与状态模型——/self 与 /deliver 同处 deliver 阶段（"人工主导是
     谁在干活的差别，不是能写哪里的边界差别"，L2 阶段边界对人机一视同仁）
  2. **豁免集（限战役根内）**：瘦协调者约束、L1 角色写入矩阵、K-03 波次编排/波门；蓝图可改但改必重校验+
     JOURNAL 留痕+契约级改动先呈报影响面
  3. **不变量集（不豁免）**：archive/ 只读、state.json 只归脚本、acceptance/ 只经 /accept、顶层 metrics.json
     只经 merge_metrics、references/ 归宿、实测数字纪律、终验全量清单——人工主导 ≠ 绕过验收
  4. **互操作**：与 /deliver 可随时互换续跑（波门重查兜住人工改动回归）；熔断 tripped 后 /self 即人工接管
     出口（修好 --reset 再 /accept）。AGENTS.md 增设"人工主导会话（/self）"条款使其对全部会话生效

- **D14 战役圈禁落地** ✅ 已裁决并落地（2026-09-02，用户指令）：任一战役活跃（decide/deliver/verify/archive）
  且全局 idle 时，工程目录与项目根对 Write/Edit 工具锁定（仅放行 .flow/**；state.json 由全局不变量先行拒写）——
  战役生成/下载的一切文件只许落所属战役根 workspace/<cid>/**。补的缺口：此前战役活跃期全局 phase=idle 对
  非战役路径放行 *，根目录对战役会话完全敞开（.tmp-tetsuya/ 根目录散落即实证）。要点：
  1. kb 维护不受影响（collect 批次语义不变，可与活跃战役并行）；工程改动等全部战役 idle 后进行
  2. 容器 README 例外收紧为"全局 idle 且无活跃战役"（原实现与自身注释"战役期锁工程层"不符，一并修正）
  3. 脚本级写入（merge_metrics/archive_campaign 等经 Bash）不经 Write 工具，不在此层，L3 审计兜底
  验证：test_guard 39/39（新增圈禁 7 用例 + 无活跃战役工程自举 1 例；3 个既有用例预期翻转并注明 D14）、
  test_init_state 5/5

- **D15 工具链升级质询轮** ✅ 已裁决（2026-09-20，grill-me 会话）：采纳 **E-15 ast-grep / E-16 DuckDB**（交互式工具位，S-02/S-03 脚本保持 stdlib 不接线）、**E-17 trafilatura**（S-02 快照旁 `.extract.md` 正文 sidecar，try-import 无环境降级；scraper 静态页正文首选）、**E-18 bwrap wrapper**（全局技能 bwrap-run；仅"执行不可信第三方代码"场景强制，默认 --unshare-net，依赖装外执行在内；日常编译测试不套）；**否决 Docling**（破坏 S-13"无 MinerU 环境"兜底语义，且 MinerU standard 档表格还原实证已够——登记 watch：表格系统性缺陷实证再评）；**暂缓 E-19 本地 VL**（无独显 + RAM 紧张 + 4.5v 限流无实证——watch：限流实证 ≥2 次再评）；pdfplumber 收拢为"脚本内部依赖"措辞（不卸载，agent 交互式探索首选 duckdb/MinerU）；image-search 维持原样（用户裁定）。安装路线：本机 sudo 无免密通道 → ast-grep/duckdb 走 GitHub 静态二进制 `~/.local/bin`。两战役活跃期施工经用户显式授权（援引 D14 授权先例），契约 v13→v14。
