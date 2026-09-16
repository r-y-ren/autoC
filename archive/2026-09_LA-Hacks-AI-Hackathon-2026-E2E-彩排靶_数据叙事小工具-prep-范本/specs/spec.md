# Spec：数据叙事小工具（E2E rehearsal m1/m2）

> 发布方式：local-files 模式（本仓库无 issue tracker，以本文件代发布）。
> 状态：**ready-for-agent**。来源：`blueprint.md`（用户已确认）+ `strategy/grill-notes.md`（授权假设）。
> 硬边界：技术范围 = 纯 Python stdlib（零第三方依赖）；Typst→PDF 编译唯一通道 = `~/.venvs/autoc/bin/python -c "import typst; ..."`；验收项 ID（a1/a2/a3）出自蓝图 frontmatter，不得增、改、删。

## Problem Statement

用户需要一个可在当日完成、零外部依赖的端到端彩排靶：验证"grilling → 蓝图 → 自动链 → 验收 → PPT"全链路在升级后的工作流中真实可走通。当前战役目录只有蓝图与策略件，尚无任何可执行产物——没有能读 CSV 出统计的 CLI，没有可供报告引用的实测数字（metrics），也没有最终的一页 PDF 报告。验收 agent 无法机检任何东西。

## Solution

按两个里程碑交付：

- **m1（software，W1）**：数据统计 CLI（`stats_cli.py`）+ 单元测试 + 样例 CSV（落 `references/data/` 并登记 INDEX）+ software↔document 接口契约（`interface/contract.md`）+ `software/metrics.json` 分片 + 报告数字核验脚本（`check_report.py`）。CLI 读取 CSV 输出统计 JSON（行数/列数/数值列均值与最大值），`--check` 自检模式给出退出码。
- **m2（document，W2，blocked by m1）**：一页报告，Typst 源 → PDF；报告中一切数字只引用 `metrics.software.*` 键，由 m1 的核验脚本逐键命中。

答辩 PPT 不属于 m1/m2（走 K-12 /ppt 正式产线），本 spec 不细化。

## User Stories

1. As a 软件交付 agent, I want stats_cli.py 读入样例 CSV 并输出统计 JSON（行数/列数/数值列均值与最大值）, so that 报告侧有唯一可信数字来源。
2. As a 软件交付 agent, I want `--check` 自检模式在输出合法统计后以退出码 0 结束, so that 验收 cmd（a1）可机检通过。
3. As a 验收 agent, I want CLI 对样例 CSV 输出统计 JSON 且自检退出码 0, so that 我能不依赖人工判断地关闭验收项 a1。
4. As a 软件交付 agent, I want 一套覆盖核心外部行为的 unittest 测试可经 `python -m unittest discover` 全过, so that 验收 cmd（a2）可机检通过。
5. As a 验收 agent, I want CLI 单元测试全部通过, so that 我能确认统计逻辑无回归。
6. As a 软件交付 agent, I want 样例 CSV 落在 `references/data/sample.csv` 且在 references INDEX 登记来源, so that 战役圈禁（D14）与引用纪律（铁律 1/3）同时满足。
7. As a 软件交付 agent, I want interface/contract.md 明确 software↔document 的产物契约（统计 JSON 的形状与 metrics 键名）, so that document 侧消费 m1 产物时不需口头约定。
8. As a 软件交付 agent, I want 实测数字写入 `software/metrics.json` 分片（含报告用全部数字）, so that 报告数字有唯一归宿且符合数据纪律（铁律 4）。
9. As a 文档交付 agent, I want 用 Typst 撰写一页报告并经 `~/.venvs/autoc/bin/python` 的 typst 包编译为 PDF, so that 交付物是可分发的 PDF 且不引入构建依赖面。
10. As a 文档交付 agent, I want 报告中每个数字都映射到 `metrics.software.*` 键, so that 数字可溯源、无编造。
11. As a 软件交付 agent, I want check_report.py 能解析 PDF 文本并逐键核验命中 metrics.json, so that 验收 cmd（a3）可机检通过。
12. As a 验收 agent, I want 报告 PDF 存在且其中数字逐键命中 metrics.json, so that 我能不依赖人工判断地关闭验收项 a3。
13. As a 协调 agent, I want m2 的全部工作在 m1 完成后才开始, so that 波次拓扑与蓝图 depends_on 一致、无依赖倒置。
14. As a 用户, I want 全部交付物零第三方 Python 依赖, so that 在任意有 Python 3 的环境可自检复现。
15. As a 协调 agent, I want m1/m2 各阶段完成后在 JOURNAL.md 留痕, so that 阶段纪律（铁律 6）可审计。

## Implementation Decisions

- 里程碑拓扑固定为蓝图值：m1（software）→ m2（document，depends_on: [m1]）。不得发明新依赖或跨里程碑重排。
- 交付物拆解（m1）：统计 CLI（CSV→统计 JSON，`--check` 自检退出码）、unittest 测试集、样例 CSV（`references/data/` + INDEX 登记）、接口契约文档（software↔document）、`software/metrics.json` 分片、报告数字核验脚本 `check_report.py`。
- 统计 JSON 的键即契约：行数、列数、数值列均值与最大值——具体键名在接口契约中冻结，metrics 分片与报告引用同一套键名。
- metrics 分片是报告数字的唯一来源：报告侧禁止出现任何 metrics 之外的实测数字（数据纪律）。
- 交付物拆解（m2）：Typst 报告源 + 编译产物 PDF；编译唯一通道为 `~/.venvs/autoc/bin/python -c "import typst; ..."`，报告中数字只引 `metrics.software.*` 键。
- 核验脚本属 m1（蓝图原文：m1 含"报告数字核验脚本"），其存在使 a3 的 cmd 在 m2 产物出现后即可机检。
- 第三方包允许面为零：仅 Python stdlib（csv/json/unittest/argparse/sys 等）；typst 仅作为宿主 venv 中的**编译通道**（非工程依赖、不进 requirements/工程 import 面）。
- 所有文件归宿遵循战役圈禁（D14）：全部落在本战役根内；references 子树登记 INDEX。
- PPT（deliverable 之一）不在 m1/m2 内实现，走 K-12 /ppt 产线，用户门为 ppt-master Gate1/Gate2。

## Testing Decisions

- 好的测试只测外部行为：从 CLI 进程边界与公共函数签名观测（进什么 CSV、出什么 JSON、什么退出码），不测内部实现细节。
- 测试接缝取**最高接缝 = CLI 进程边界**（即 a1 的 exec cmd 形态）：`--csv <样例> --check` 输出统计 JSON 且退出码 0；单元测试以同一命令形态或直接调用入口函数覆盖。
- 第二接缝为 PDF 数字核验（a3 的 exec cmd 形态）：check_report.py 解析 PDF 文本，逐键命中 metrics.json——测外部行为（存在性、命中/未命中退出码），不测解析器内部。
- 模块受测面：stats_cli（CSV 解析、统计计算、JSON 输出、`--check` 语义）、check_report（PDF 存在性、数字命中判定）。
- 先例：本战役为首个软件产物，无既有测试可参照；采用 stdlib unittest（与验收 cmd a2 的 `python -m unittest discover` 对齐）。
- 验收即测试的最终口径：a1/a2/a3 三条 exec cmd 全过即里程碑达成，无 manual 项。

## Out of Scope

- 真实报名与投递、云端部署、多用户/网络功能（蓝图 out_of_scope 原文）。
- 任何第三方 Python 依赖。
- 答辩 PPT 的生产（K-12 产线，非 m1/m2 里程碑）。
- 新增/修改/删除验收项（a1/a2/a3 冻结）。
- 其他战役目录的一切读写。

## Further Notes

- 彩排模式（compliance mode: prep）：作品按"AI 辅助原创"标准产出，归档时保留人机分工记录。
- 本 spec 与票单（同目录 tickets.md）由 planner 于 K-03 步 1.5 产出；蓝图若再变更须重过 schema 校验（本 spec 不授权改蓝图）。
- grill-notes 的 6 条授权假设（时间窗当日、零依赖、auto_chain 开启等）已全部体现在本 spec 决策中。
