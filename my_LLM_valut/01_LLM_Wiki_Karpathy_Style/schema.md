# Wiki 配置文档

这个配置文档告诉 LLM 如何维护这个知识库。它遵循 Andrej Karpathy 的 LLM Wiki 设计模式，但会进一步适配用户的论文精读与论文写作工作流。

---

## 核心原则

### 1. LLM 完全拥有
LLM 负责撰写和维护 `wiki/` 目录中的所有内容。用户负责选择论文、判断研究方向和审阅结果。LLM 会：
- 摄取新源时创建或更新页面
- 维护页面间的交叉引用
- 沉淀可复用的系统建模知识
- 将阅读结果组织成可写作的知识资产
- 更新索引和日志

### 2. 持久化、复合性产物
Wiki 是持续演化的研究知识库，而不是临时读书笔记：
- 论文页保留单篇论文的细节与差异
- 建模页沉淀跨论文复用的系统建模设计
- 主题页组织研究主线与方法谱系
- 综合页沉淀阶段性判断与研究路线图

### 3. 分层职责与证据边界
- `raw/` 是原始证据层，默认不可修改
- `wiki/` 是正式知识层，承载可复用、可查询、可写作的稳定页面
- `synthesis/` 是候选沉淀层，存放 AI 对话压缩卡片与待编译洞见
- `output/` 是正式输出层，存放论文、书稿、博客、PPT 等成果索引与文件
- 任何写入 `wiki/` 的事实主张，都应尽量可追溯到 `raw/`；`synthesis/` 只能作为候选入口，不能直接冒充证据源
- `output/` 中的内容只有在用户明确要求摄取时，才可作为新的编译对象进入 `wiki/`

### 4. 论文页与建模页并存
常见系统建模设计不应只留在论文页，也不应完全脱离论文页。

正确做法是两层并存：
- **论文页**：记录该论文具体采用了什么建模假设、变量、约束和算法设计
- **系统建模页**：抽象出跨论文复用的建模套路，例如[[无人机能耗模型]]、[[计算卸载模型]]、[[任务队列与时延保障模型]]

**判断规则**：
- 仅在单篇论文中出现、且明显不可复用的建模细节，可以只放在论文页
- 一旦某种模型在 2 篇及以上论文中重复出现，或明显会进入用户后续写作，就应创建或更新系统建模页

### 5. 文献分层，不分库
这个 wiki 的主组织轴始终是主题、概念、建模和研究主线，而不是按论文级别拆目录。

正确做法是：
- 所有论文继续进入同一个 `wiki/`
- 通过 frontmatter 标注文献层级与使用角色
- 在主题页和综合页中明确区分“主干证据”“支撑材料”“探索信号”

**核心判断**：
- `venue_tier` 表示来源级别，例如 `CCF-A`、`CCF-B`、`CCF-C`、`Survey`
- `evidence_tier` 表示这篇论文在当前知识库中的证据权重，例如 `core`、`supporting`、`exploratory`
- `paper_role` 表示这篇论文的使用角色，例如 `anchor`、`supporting`、`comparison`、`survey`、`inspiration`
- 这三者相关，但不能混为一谈

**原则**：
- 不因为论文级别不同而拆成多个 wiki
- 不让低层级论文直接支撑高强度结论，除非用户明确指定
- 综述页通常承担结构化入口，而不是单篇方法证明

### 6. 实验与复现证据必须结构化沉淀
这个 wiki 不只记录“论文提出了什么”，还要记录“论文如何验证、能否复现、离真实系统还有多远”。

正确做法是两层并存：
- **论文页**：记录该论文具体使用了什么数据、平台、框架、硬件与评测证据
- **实验资产页**：抽象出跨论文复用的实验资源节点，例如[[Shenzhen IoV 轨迹数据]]、[[FLAME 数据集]]、[[MindSpore]]、[[PX4]]、[[Jetson Xavier NX]]

**核心关注点**：
- 是否使用真实数据、公开数据、合成数据或文献复用数据
- 是否依赖 MATLAB、PyTorch、MindSpore、AirSim、ROS/Gazebo、PX4、ns-3 等平台或软件栈
- 是否说明 GPU、CPU、飞控、板卡、无人机型号等物理配置
- 是否有开源代码、数据或配置
- 当前结果属于仿真、trace-driven、半实物、原型还是实飞验证

**判断规则**：
- 即使没有图片双链，实验文字信息也应先被抽取到论文页
- 一旦某个数据源、平台或硬件在 2 篇及以上论文中重复出现，或明显会进入用户后续工程选型，应创建或更新实验资产页
- 如果论文只说“simulation results show”，却没有说明平台、数据或硬件，则必须在论文页明确标记“证据不完整”

---

## 目录结构

```text
01_LLM_Wiki_Karpathy_Style/
├── raw/
│   ├── markdown/
│   ├── pdfs/
│   ├── assets/
│   └── scripts/
├── synthesis/
│   └── AI_Inbox.md
├── output/
│   ├── index.md
│   ├── papers/
│   ├── books/
│   ├── blogs/
│   └── slides/
├── wiki/
│   ├── index.md
│   ├── log.md
│   └── [各种页面].md
├── schema.md
└── README.md
```

**关键点**：
- Wiki 保持扁平目录，不按子目录拆分
- 页面分类通过页面内容与 `index.md` 实现，而不是通过深层目录结构实现
- `index.md` 和 `log.md` 始终是单文件
- `synthesis/` 和 `output/` 是当前项目内部目录，不再依赖外部同名目录
- `raw/`、`wiki/`、`synthesis/`、`output/` 各自职责不同，不应混写

---

## 使用入口与 Schema 更新协议

### 日常使用入口
- 项目的日常说明入口是当前目录的 `README.md`
- 正式知识库入口是 `wiki/index.md`
- AI 对话的候选沉淀入口是 `synthesis/AI_Inbox.md`
- 个人输出的统一登记入口是 `output/index.md`
- 以上入口用于“防忘”，但真正的编译规则仍然只以本 `schema.md` 为准

### Schema 更新协议
每次更新 `schema.md` 时，必须同时完成下面 4 件事：
1. 更新本文末尾的 `版本` 与 `更新` 日期
2. 在 `wiki/log.md` 追加一条 `update | schema.md` 记录
3. 如果工作流、目录职责或使用方式发生变化，同步更新当前目录 `README.md`
4. 在最终答复中明确说明“这次 schema 改了什么、会影响什么”

**不允许**：
- 只改 `schema.md` 而不留痕
- 修改工作流后不更新 README
- 把 `raw/` 当作可写层

---

## 操作

### 摄取（Ingest）- 添加新论文

当用户将新论文放入 `raw/markdown/` 并要求摄取时：

**工作流程**：
1. 从 `raw/markdown/` 读取论文
2. 先判定文献分层元数据：`literature_type`、`venue_tier`、`evidence_tier`、`paper_role`、`use_for`
3. 基于论文标题先创建“题目驱动研究框架”
4. 先写 `Algorithm Design` 快照，而不是先写 Introduction
5. 从论文中提取系统框架图信息，生成“图1草案”描述
6. 再完善 `System Model` 与 `Algorithm Design` 细节
7. 抽取实验与复现证据：验证类型、数据来源、平台/框架、硬件、开源情况、复现判断
8. 提炼标签和对照材料，为 `Introduction` 与 `Related Work` 积累素材
9. 创建或更新论文页
10. 创建或更新相关系统建模页、概念页、主题页、实验资产页
11. 更新 `wiki/index.md`
12. 在 `wiki/log.md` 追加条目
13. 确保新旧页面形成双向链接

**重要**：
- 这是一次完整摄取，不拆成机械的多轮“编译/提取/链接”流水线
- 单篇论文通常应触及 6-15 个页面
- 摄取的目标不是生成摘要，而是把论文并入正在生长的研究网络
- 文献分层的判定优先级为：`用户显式指定 > 论文页已有 frontmatter > schema 默认规则 > LLM 基于论文内容推断`

---

### 查询（Query）- 提问

当用户提问时：
1. 先读 `wiki/index.md`
2. 定位相关论文页、建模页、概念页和主题页
3. 综合答案并标出来源
4. 如果答案本身有长期价值，则写回 wiki 为新页面

**适合回写 wiki 的内容**：
- 模型对比
- 方法谱系梳理
- 研究空白判断
- 写作提纲式综合

---

### 沉淀（Synthesize）- AI 对话候选入箱

当用户希望把一轮 AI 对话中的高价值内容保留下来，但又不想直接写入 `wiki/` 时：

1. 将内容压缩成候选卡片，而不是复制整段对话
2. 写入 `synthesis/AI_Inbox.md`
3. 必须标出类型，例如 `sourced`、`inferred`、`decision`、`writing`
4. 必须尽量给出依据页面
5. 只有在后续再次审阅后，才把其中稳定内容正式编译进 `wiki/`

**规则**：
- `synthesis/AI_Inbox.md` 是候选层，不是正式事实层
- 无来源、不可复用、纯聊天型内容不入箱
- 进入 `wiki/` 前仍要经过正常的编译与链接过程

---

### 健康检查（Lint）- 定期检查

定期检查 wiki 健康状况：
1. 页面矛盾
2. 过时主张
3. 孤立页面
4. 缺失的建模页或概念页
5. 缺失反向链接
6. 死链接
7. 论文页与建模页之间的引用缺口
8. 用户写作工作流相关字段是否缺失
9. 论文页是否缺少 `venue_tier`、`evidence_tier`、`paper_role`
10. 主题页中的主结论是否过度依赖 `supporting` 或 `exploratory` 文献
11. 综述论文是否被误当作方法证明页使用
12. 论文页是否缺少 `validation_type`、`data_origin`、`artifact_availability`、`reproducibility_level`
13. 标记为 `prototype` 或 `field_test` 的论文是否缺少明确的 `hardware_stack`
14. 标记为 `public_dataset` 的论文是否没有写明具体数据集名称
15. 主题页或综合页是否把纯仿真结论写成“已被真实系统充分验证”

**输出**：
- 问题列表
- 修复建议
- 不自动修复，先呈现给用户

---

## 页面类型规范

### 1. 论文页
论文页是单篇论文的精读入口，必须服务于后续论文写作，而不是只做摘要归档。

**推荐结构**：
1. 单行摘要
2. 题目驱动研究框架
3. `Algorithm Design` 快照
4. 图1系统框架草案
5. `System Model`
6. `Algorithm Design` 详解
7. 实验证据卡片
8. `Introduction` 写作素材
9. `Related Work` 写作素材
10. 相关系统建模页
11. 相关概念/主题页

**额外要求**：
- `题目驱动研究框架` 要把标题视为研究意图的初始假设
- 明确指出标题中哪些对象、问题、方法和效果是论文真正成立的主轴
- 如果论文标题与正文重点不完全一致，要标出这种偏差

**Algorithm Design 快照要求**：
- 用一段中文完成
- 不超过 400 字
- 必须同时说明：场景、研究对象、存在问题、具体方法、期望效果

**图1系统框架草案要求**：
- 不要求真正画图，但要给出清晰的文字框架
- 至少包含：系统实体、任务/数据流、控制/优化变量、约束来源
- 目标是让用户后续可以直接据此画论文第一张图

**实验证据卡片要求**：
- 必须至少回答：验证类型、数据来源、平台/软件、硬件/算力、开源情况、复现判断
- 当信息缺失时，明确写 `未说明` 或 `证据不完整`，不要假装论文写过
- 对真实数据、公开平台、原型系统和实飞测试要单独标出，因为这些信息对后续工程路线特别重要
- 对 trace-driven 仿真要明确写出“真实数据驱动，但仍非真实部署”

### 2. 系统建模页
系统建模页用于沉淀跨论文复用的建模设计。

**常见页名示例**：
- [[无人机能耗模型]]
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[任务队列与时延保障模型]]
- [[服务放置模型]]

**推荐结构**：
1. 定义
2. 为什么重要
3. 常见建模方式
4. 常见变量与参数
5. 常见约束形式
6. 当前语料中的代表论文
7. 写作提醒与常见坑

**写法要求**：
- 抽象共性，不抄单篇论文结构
- 明确变体之间的差异与适用场景
- 能直接为用户写 `System Model` 提供复用素材

### 3. 实验资产页
实验资产页用于沉淀跨论文复用的数据集、仿真平台、软件框架、硬件配置和复现资产。

**常见页名示例**：
- [[Shenzhen IoV 轨迹数据]]
- [[FLAME 数据集]]
- [[MindSpore]]
- [[AirSim]]
- [[PX4]]
- [[Jetson Xavier NX]]

**推荐结构**：
1. 定义与来源
2. 当前语料中的使用论文
3. 在哪些研究问题中常见
4. 优势与局限
5. 复现提醒
6. 与用户未来工程项目的连接点

### 4. 概念页
概念页解释稳定知识对象，例如 [[任务卸载]]、[[Lyapunov优化]]、[[多智能体强化学习]]。

### 5. 主题页
主题页组织研究主线，例如某一问题域的演化、方法谱系或前沿趋势。

### 6. 对比页
对比页回答“X 与 Y 的关系/差异是什么”这类问题，适合沉淀写作中的判别性观点。

### 7. 综合页
综合页组织阶段性的整体判断，例如研究路线图、综述框架、写作导图。

---

## 用户论文写作工作流适配

这个 wiki 必须兼容用户的论文精读与论文写作风格。

### 第一步：标题先行
- 论文题目非常重要
- 题目在写作过程中可能持续变化
- 因此摄取时先根据标题拟定研究主体、问题、方法和创新意图
- 但要把标题视为“可修订框架”，而不是不可变结论

### 第二步：从 Algorithm Design 开始
在摄取论文时，优先生成：
- 一段 400 字以内的 `Algorithm Design` 快照
- 一份 `图1系统框架草案`

### 第三步：补全 System Model 与 Algorithm Design
- 论文页应详细记录系统实体、变量、约束、优化目标、求解思路
- 其中可复用的建模设计需要同步沉淀到系统建模页

### 第四步：抽取实验与复现证据
- 论文页应额外记录实验验证方式、数据来源、平台/软件、硬件配置和开源情况
- 对真实数据、公开平台、硬件配置要优先抽取，因为这些信息直接关系到后续复现价值
- 对“只做仿真”的工作要明确标注，不要与真实系统验证混淆

### 第五步：反向支持 Introduction 与 Related Work
- 通过论文标签、问题类型、方法类型、贡献类型积累写作素材
- `Introduction` 素材要回答“为什么值得研究”
- `Related Work` 素材要回答“与哪些已有工作相比，差异在哪里”

**因此，摄取顺序优先级为**：
`标题理解 → Algorithm Design 快照 → 图1草案 → System Model → Algorithm Design 详解 → 实验证据抽取 → Introduction/Related Work 素材`

---

## 文献分层管理

### 为什么要分层
- 当前用户默认优先编译 CCF A 类核心论文
- 后续会逐步纳入 CCF B、CCF C、综述、前沿信号论文
- 如果不分层，页面里的观点会看起来权重相同，影响写作判断

### 分层字段
- `venue_tier`：来源级别
- `literature_type`：论文类型
- `evidence_tier`：证据权重
- `paper_role`：在当前知识库中的使用角色
- `use_for`：最适合支持哪些写作任务

### 推荐枚举
- `venue_tier`: `CCF-A | CCF-B | CCF-C | Survey | arXiv | Report | Unknown`
- `literature_type`: `method | survey | system | benchmark | theory | application`
- `evidence_tier`: `core | supporting | exploratory`
- `paper_role`: `anchor | supporting | comparison | survey | inspiration`
- `use_for`: `main_citation | introduction | related_work | system_model | methodology | taxonomy | idea_seed`
- `validation_type`: `theory | simulation | trace_driven | emulation | prototype | field_test | literature_review`
- `data_origin`: `synthetic | public_dataset | self_collected | borrowed_from_prior_work | mixed | literature_corpus | unknown`
- `artifact_availability`: `open | partial | closed | unknown`
- `reproducibility_level`: `high | medium | low | unknown`

### 默认规则
如果用户没有显式说明，则采用以下默认映射：

1. `CCF-A` 方法论文
- `literature_type: method`
- `evidence_tier: core`
- `paper_role: anchor`
- `use_for` 默认包含：`main_citation`, `methodology`, `system_model`

2. `CCF-B` 方法论文
- `literature_type: method`
- `evidence_tier: supporting`
- `paper_role: supporting`
- `use_for` 默认包含：`related_work`, `methodology`, `system_model`

3. `CCF-C` / workshop / arXiv 类前沿论文
- `literature_type: method` 或 `system`
- `evidence_tier: exploratory`
- `paper_role: inspiration`
- `use_for` 默认包含：`idea_seed`, `related_work`

4. 综述论文
- `literature_type: survey`
- `venue_tier: Survey`
- `evidence_tier: supporting`
- `paper_role: survey`
- `use_for` 默认包含：`taxonomy`, `introduction`, `related_work`

### 可提升规则
- 如果用户明确说某篇 `CCF-B` 是该问题的主锚点，可将其提升为 `evidence_tier: core`
- 如果某篇综述承担该方向的结构骨架，也可提升为 `evidence_tier: core`
- 如果某篇 `CCF-A` 只作为启发而不作为主结论支撑，也可以降为 `supporting`

### 用户何时需要手动指定
通常不需要用户在编译前手动修改 YAML。

更推荐的方式是用户在发起编译时直接说明：
- “这批按 CCF-B supporting 编译”
- “这篇综述按 survey/core 编译”
- “这篇虽然不是 A，但按 anchor 编译”

LLM 负责把这些指令写入 `wiki/` 论文页 frontmatter；`raw/` 仍保持不可变。

---

## 链接与元数据规范

### 链接
- 使用 Obsidian 风格链接：`[[页面名称]]`
- 论文页必须链接到相关建模页
- 建模页必须回链到代表论文
- 主题页必须串联相关论文页与概念页

### 前言元数据
可使用 YAML frontmatter：
```yaml
---
tags: [标签1, 标签2, 标签3]
created: 2026-04-07
updated: 2026-04-07
sources:
  - ../raw/markdown/example.md
venue: IEEE TMC
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: low
---
```

**规则**：
- 分层元数据写在 `wiki/` 页面 frontmatter 中，不写回 `raw/`
- 如果用户没有特别说明，LLM 依据 schema 默认规则填写
- 如果后续判断变化，可以更新 `evidence_tier` 和 `paper_role`，但不随意改写 `sources`
- 实验元数据同样写在 `wiki/` frontmatter 中，不写回 `raw/`
- 当平台、硬件、数据来源无法确认时，用空列表和 `unknown`，不要编造
- 如果后续补齐图片双链或重新精读论文，可以增量更新实验元数据

### 内容指南
- 每个事实主张都应能追溯到来源
- 避免模糊措辞
- 明确区分“论文具体做法”和“跨论文抽象结论”
- 记录矛盾与建模差异
- 写作支持信息要可直接复用，不要只写空泛评价

---

## 索引规范

`wiki/index.md` 是所有内容的内容导向目录。

**推荐结构**：
```markdown
# 索引

## 论文
- [[论文页]] - 单行摘要

## 系统建模
- [[无人机能耗模型]] - 单行摘要
- [[计算卸载模型]] - 单行摘要

## 实验与复现
- [[实验资产页]] - 单行摘要

## 概念
- [[概念页]] - 单行摘要

## 主题
- [[主题页]] - 单行摘要

## 对比
- [[对比页]] - 单行摘要

## 综合
- [[综合页]] - 单行摘要
```

**规则**：
- 每次摄取都要检查是否需要更新“系统建模”分类
- 建模页优先收录具有复用价值的模型，不收录零散公式碎片
- 索引是查询入口，也是用户观察进度的面板

---

## 日志规范

`wiki/log.md` 是按时间顺序的仅追加记录。

**条目格式**：
```markdown
## [YYYY-MM-DD] action | 标题/描述
- 创建：[[页面A]], [[页面B]]
- 更新：[[页面C]], wiki/index.md
```

**操作**：
- `init` - 初始化
- `ingest` - 摄取新论文
- `query` - 回答问题并生成页面
- `lint` - 健康检查
- `update` - 结构升级或一般更新

---

## 领域特定说明

这是一个专注于 UAC / UAV-MEC / 空中边缘计算研究的 wiki。

**领域约定**：
- 重点关注：任务卸载、资源分配、轨迹优化、多UAV协同、安全与服务保障、边云协同、大模型前沿
- 同时持续关注：真实数据来源、开源实验平台、仿真器、硬件物理配置与复现可信度
- 论文源在 `raw/markdown/`
- 使用 Citation Key 作为源文件名
- 对组织有疑问时，优先考虑清晰、可复用、可写作

**源处理**：
- 原始 PDF 在 `raw/pdfs/` 中
- 转换后的 markdown 在 `raw/markdown/` 中
- 图片与图表素材在 `raw/assets/` 中
- 脚本与小工具在 `raw/scripts/` 中
- LLM 在 `wiki/` 中创建/更新正式知识页
- LLM 可在 `synthesis/` 中写入候选沉淀卡片
- LLM 可在 `output/` 中维护输出索引
- 永不修改 `raw/`

---

## 灵活性

这个配置文档是指南，不是僵硬模板：
- 页面结构可以随着研究深入而演化
- 如果新的建模类型高频出现，应及时新增系统建模页
- 如果用户形成新的写作习惯，应优先把该习惯吸收到摄取流程中
- 目标始终是：让 wiki 同时服务研究理解、论文写作和长期知识积累

---

**版本**：2.4  
**更新**：2026-04-09  
**基于**：Andrej Karpathy 的 LLM Wiki 模式 + 用户论文精读/写作工作流
