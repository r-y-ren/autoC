<!-- ppt-master-schema: design-spec/v1 -->
# rehearsal-deck - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | rehearsal-deck |
| Canvas Format | PPT 16:9（1280×720，ppt169） |
| Page Count | 5 |
| Primary Language | zh-CN |
| Target Audience | 大赛评审（现场答辩场景） |
| Communication Intent | 用 3 分钟让评审相信作品的数字可信、链路可复验；主张先行、证据跟上 |
| Desired Audience Outcome | 评审在 3 分钟内理解作品价值并认可"每个数字都可一键追溯"的质量主张 |
| Core Message / Ask / Action | 最小数据叙事闭环：零依赖 CLI 产出 8 项实测指标，报告与 PPT 数字全部一键可溯 |
| Delivery Context | 现场答辩（primary）；赛后归档留痕（secondary） |
| Artifact Afterlife | 战役归档物（人机分工与数字溯源留痕） |
| Reading Mode | presentation |
| Content Strategy | balanced（源简报为权威底稿，允许为金字塔断言重组标题与顺序，事实与数字不变） |
| Design Style | 方向 1：结论先行·实证金字塔（mode=pyramid + visual style=dark-tech，用户点名科技深色） |
| AI Image Acquisition Path | not applicable（image_usage=none） |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — workflow default（3 分钟逐页口径） |
| Custom Animations | disabled — workflow default |
| Narration Audio | disabled — workflow default |
| Created Date | 2026-09-16 |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 上下 56px / 左右 80px |
| Content Area | x:80–1200, y:56–664 |

## III. Visual Theme

### Theme Style

- **Mode**: pyramid（断言式标题=结论；证据其下；数字配可支撑对比或直接含义，不虚构基准）
- **Visual style**: dark-tech（深色画布、发光强调、几何精确；克制的细网格/节点线；深度来自发光与分层而非投影）
- **Theme**: 深空仪表台——数字是唯一主角，青蓝发光即注意力
- **Tone**: 冷静、精确、可信

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #0B1220 | 深藏青主底（暗负空间=深度） |
| Secondary background | #111A2E | 卡片/面板层底 |
| Primary | #38BDF8 | 主结构色（标题强调、主图形线框） |
| Accent | #22D3EE | 发光强调（metrics 数字、活跃节点——注意力的唯一执笔者） |
| Secondary accent | #F59E0B | 琥珀次强调（闭环/警示语义，少量） |
| Body text | #E2E8F0 | 正文 |
| Secondary text | #94A3B8 | 说明、注释、来源行 |
| Divider | #1E293B | 细分隔线/网格线 |

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | 高对比无衬线，断言式短句 | Microsoft YaHei | Arial | 'Noto Sans SC', 'PingFang SC', sans-serif |
| Body | 清爽无衬线，低装饰 | Microsoft YaHei | Arial | 'Noto Sans SC', 'PingFang SC', sans-serif |
| Data | 等宽数字（metrics 数值与键名） | Consolas | Consolas | 'JetBrains Mono', 'Courier New', monospace |

- **Title stack**: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', Arial, sans-serif
- **Body stack**: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', Arial, sans-serif
- **Data stack**: Consolas, 'JetBrains Mono', 'Courier New', monospace
- **Role rationale**: Data 角色承载全部 metrics 数值/键名与来源键标注（dark-tech 的 monospace 纪律），递归出现故单列。

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 30 |
| Title | 54 |
| Subtitle | 36 |
| Annotation | 20 |

## V. Layout Principles

### Deck-wide Direction

- **Hierarchy direction**: 断言标题（左上锚定）→ 一行结论 → 证据区（发光数字/主表居中偏下）→ 来源行（页脚，secondary_text）
- **Composition tendency**: 深色负空间留白承压；每页一个发光焦点（一个数字或一张表）；细网格/括号线仅在分区时出现
- **Cross-page continuity**: 跨页母题为"发光电路细线 + 等宽来源键标签"（P1 埋下，P3/P4 复用其节点样式）；标题位置与页脚来源行全组恒定
- **Spacing posture**: breathing（5 页 3 分钟，每页一个论点，疏朗为大）
- **Spacing anchors**: 页边距 80/56px；块间距 32px；栏间距 24px；圆角 6px（近直角）；正文行距 44px

## VI. Icon Usage Specification

- **Primary bundled library**: tabler-outline
- **Stroke Width**: 2

| Icon Path | Suitable Scenarios |
| --- | --- |
| tabler-outline/terminal-2 | CLI 工具/命令行语义（P2） |
| tabler-outline/table | 数据表/指标表（P3） |
| tabler-outline/chart-bar | 数值对比/统计（P3） |
| tabler-outline/circle-check | 验收通过/质量项（P4） |
| tabler-outline/refresh | 闭环/回归（P4） |
| tabler-outline/target-arrow | 目标/收束主张（P5） |

## VII. Visualization Reference List

| Page | Family | Template | Usage |
| --- | --- | --- | --- |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---|

（image_usage=none：无图像资源行；digital-dashboard 渲染仅作风格记名，不产生任务。）

## IX. Content Outline

### Part 1: 开场主张

#### Slide 01 - 封面·核心主张

- **Audience move**: 未知 → 3 秒内抓住"可信数字"这一核心主张并愿意听下去
- **Relationships**: 核心主张（parent）· 三个支撑标签：零依赖/实测/可溯源（membership）· 战役名与用途注记（annotation）
- **Composition**: 中央大字主张 + 底部三个等宽标签胶囊；背景一条低透明度发光电路细线自左下向右上（跨页母题起点）；超大低透明度"3′"数字暗纹在右侧背景层
- **Title**: 可信数字，一键复验
- **Core message**: 最小数据叙事闭环——从 CSV 到答辩 PPT，每个数字都能追溯到实测
- **Content**: 主标题 · 副题（数据叙事小工具 · E2E 彩排范本）· 三标签：零依赖 / 8 项实测指标 / 全键溯源 · 页脚来源行（e2e-rehearsal-2026 · metrics 8 键）
- **Cover impact (binding)**: 钩子=「可信数字，一键复验」八个字 + 一处发光下划线；其余全部低亮度

### Part 2: 证据链

#### Slide 02 - 方案：零依赖 CLI

- **Audience move**: 看过主张 → 理解方案极简性（一条命令、零第三方依赖、自带自检）
- **Relationships**: 命令行输入（order:1）→ stats_cli 处理（order:2，parent）→ 统计 JSON 输出与 --check 自检（order:3，membership 于输出）；"零依赖"与"自检"构成对比对（contrast）
- **Composition**: 左侧终端面板（secondary_bg 圆角近直角卡）内等宽命令与输出 JSON 摘要；右侧两枚发光小卡：零依赖（纯 stdlib）/- -check 自检退出码；terminal-2 图标点缀面板题标
- **Title**: 一条命令，把原始 CSV 变成可引用指标
- **Core message**: 零依赖是可信的前提——没有黑盒，任何机器都能复跑
- **Content**: 命令 `python stats_cli.py --csv sample.csv --check` · 输出键：rows/cols/numeric.{count,mean,max} · 纯 Python stdlib · 29 项单元测试
- **Fact IDs**: metrics.software.rows

#### Slide 03 - 实测结果：8 项指标全可溯

- **Audience move**: 知道有工具 → 看到全部实测数字并相信"每个都能一键查到出处"
- **Relationships**: 8 项指标构成两族（parent=指标总表）：数据规模族 rows/cols（membership）· 分布族 score/hours 的 count/mean/max（membership）；来源键列把每行 link 到 metrics.json
- **Composition**: 页面主体=发光边框指标表（8 行：指标/含义/实测值/来源键），实测值列用 Data 角色大号等宽+青色发光，来源键列低亮度等宽；表上方一行断言结论
- **Title**: 8 项实测指标，全部一键可溯
- **Core message**: 数字不是写出来的，是测出来的——表右列即 metrics 键名
- **Content**: rows=6 · cols=3 · score_count=6 · score_mean=88.0 · score_max=95.0 · hours_count=6 · hours_mean=5.5 · hours_max=8.0（每行标注 metrics.software.<键>）
- **Visualization**: 指标总表（纯文本网格，8 行 4 列）
- **Native-ready**: metrics-table=yes
- **Fact IDs**: metrics.software.rows, metrics.software.cols, metrics.software.score_count, metrics.software.score_mean, metrics.software.score_max, metrics.software.hours_count, metrics.software.hours_mean, metrics.software.hours_max

#### Slide 04 - 质量闭环

- **Audience move**: 认可数字 → 相信生产过程本身可复验（测试先行、验收左移、全链溯源）
- **Relationships**: 质量三环（membership 于"闭环"parent）：TDD 红→绿（order:1）· 波门左移 a1/a2（order:2）· 终验 a3 全过（order:3）；三环首尾相接成环（link）
- **Composition**: 三枚节点卡沿一条发光弧线排布（refresh 图标居环心低亮度），每卡：环名/断言/证据注记；琥珀色仅用于"左移不烧熔断"这一处语义点
- **Title**: 质量闭环：测试先行，验收左移，数字全溯源
- **Core message**: 链路上每一环都有自动化证据，3 分钟内可全部复跑
- **Content**: TDD 29 测试（红→绿留痕）· 波门左移 a1/a2 PASS · 终验 result=pass（a1-a3，retry 0/3）· 报告 PDF 数字逐键命中（a3）
- **Fact IDs**: metrics.software.score_mean
- **Motion suggestion**: 三环沿弧线依次点亮（闭环单元自 P3 的发光表延续为 P4 的环节点）

### Part 3: 收束

#### Slide 05 - 收束·数据叙事

- **Audience move**: 理解全链路 → 带走一句话结论与复验入口
- **Relationships**: 结论句（parent）· 复验三入口：a1/a2/a3 命令（membership）· 归档注记（annotation）
- **Composition**: 中央大字收束句 + 其下一条等宽复验命令行（唯一发光体）；target-arrow 图标小号点缀句前；页脚人机分工一行
- **Title**: 三分钟看完：从数据到答辩的完整闭环
- **Core message**: 作品即证据——跑一遍验收命令，数字自己说话
- **Content**: 收束句 · 复验命令 `python check_report.py`（退出码 0）· 人机分工：agent 产全部工程物 / 人确认蓝图与用户门 · 归档：workspace/e2e-rehearsal-2026
- **Closing impact (binding)**: 收束=「作品即证据」+ 一条可复制的等宽复验命令；不再新增信息
- **Fact IDs**: metrics.software.hours_max

## X. Speaker Notes Requirements

- **Generation**: enabled
- **Filename**: 与 svg_output/ 各页 SVG 同名（notes/01_*.md …）
- **Content**: 每页以结论口吻开场再给事实（pyramid register）；数字口播用自然语言读法（如"八十八分"）；全部事实取自本规格与 metrics 键，不引入片外数字
- **Total duration**: ≈180 秒（5 页均摊 30-40 秒）
- **Notes style**: 正式而口语化（现场答辩口径）
- **Presentation purpose**: 3 分钟内让评审相信数字可信、链路可复验
