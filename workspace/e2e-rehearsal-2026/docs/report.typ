// 单页报告（document 侧交付物）：消费路径按接口契约——直接读 software 分片，变量名冻结为 metrics。
// 数字纪律：本页全部实测数字仅以 metrics 键引用——取值形 metrics.<键>、规范形 metrics.software.键；
// 除键值外本源不出现任何数字（日期、版本号、页码均不例外）。

#let metrics = json("../software/metrics.json")

= 数据叙事小工具：样例数据统计叙事报告

战役彩排交付物 · document 侧 · 单页报告 · 数字全量引自 metrics 实测分片

*方法：* 以无第三方依赖的标准库统计命令行工具，读入登记于战役 references 的样例 CSV（表头列名序：name、score、hours），实测数据规模与数值列（score、hours）的非缺失计数、均值与最大值；本页全部实测数字按接口契约逐键引用 software 分片，无片外数字。

== 结果（实测值均来自 metrics 分片键）

#table(
  columns: (auto, auto, auto),
  table.header([指标（含义）], [实测值], [metrics 键（规范形）]),
  [数据行数（不含表头）], [#metrics.rows 行], [`metrics.software.rows`],
  [数据列数], [#metrics.cols 列], [`metrics.software.cols`],
  [score 列非缺失观测数], [#metrics.score_count 个], [`metrics.software.score_count`],
  [score 列均值], [#metrics.score_mean 分], [`metrics.software.score_mean`],
  [score 列最大值], [#metrics.score_max 分], [`metrics.software.score_max`],
  [hours 列非缺失观测数], [#metrics.hours_count 个], [`metrics.software.hours_count`],
  [hours 列均值], [#metrics.hours_mean 小时], [`metrics.software.hours_mean`],
  [hours 列最大值], [#metrics.hours_max 小时], [`metrics.software.hours_max`],
)

*叙事读法：* 数值观测完整无缺失；score 集中于高分段、均值距最大值不远；hours 自偏小投入至最大投入均有覆盖，且成绩高低与投入时长未见同步消长。

*附录 · 人机分工：* 统计工具、测试与数字核验器由 AI 编写并经人工复核；本报告由 AI 撰写与排版，全部实测数字经核验器逐键核对，人工审定后随战役归档。
