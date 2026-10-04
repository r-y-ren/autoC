# 蓝图失效验收 cmd 留档声明（R17）

## 失效 cmd 清单（2 条）

| id | cmd（蓝图原文） | 指向路径（战役根相对） | 判定 |
|---|---|---|---|
| doc-compile | `typst compile --root workspace/kaggriculture workspace/kaggriculture/docs/report.typ workspace/kaggriculture/docs/report.pdf` | docs/report.typ | 不存在 |
| doc-consistency | `python workspace/kaggriculture/docs/check_report_metrics.py` | docs/check_report_metrics.py | 不存在 |

### doc-compile

- cmd: `typst compile --root workspace/kaggriculture workspace/kaggriculture/docs/report.typ workspace/kaggriculture/docs/report.pdf`
- 指向: `docs/report.typ`（战役根下不存在，本声明落档时实测）
- 失效原因: report.typ 从未入库（docs/ 下不存在），cmd 自蓝图订立即不可执行

### doc-consistency

- cmd: `python workspace/kaggriculture/docs/check_report_metrics.py`
- 指向: `docs/check_report_metrics.py`（战役根下不存在，本声明落档时实测）
- 失效原因: check_report_metrics.py 从未入库（docs/ 下不存在），cmd 自蓝图订立即不可执行

## 09-01 后 /accept 静默事实

- 最后一次触碰两条 cmd 的 /accept: acceptance/run-29（2026-09-01T08:08:31）——doc-compile=fail（evidence: doc-compile.log）；doc-consistency=pass（但检查脚本本身不存在——口径存疑的 pass）。
- 其后 acceptance/run-30（2026-09-01T08:12:37+08:00）: p1-r5 scoped 检查单（8 项），含 doc cmds=False。
- 其后 acceptance/run-31（2026-09-01T04:05:02+00:00）: p2 scoped 检查单（11 项），含 doc cmds=False。
- 事实定性: 2026-09-01 之后全部 /accept 均为 scoped 检查单，doc-compile/doc-consistency 两条 cmd 既未被执行、也无正式失效登记——失效状态被静默旁路而非显式处置。

## 处置

- 战后经 /attack 修订蓝图：两条失效 cmd 随蓝图修订一并移除或替换为可执行等价项，并重过 schema 校验+用户确认。本声明只留档，不改蓝图文件。

## 记录元信息

- 生成器: fn_work/src/record_governance_dispositions/declare_blueprint_cmd_invalidation.py（record_governance_dispositions 编排叶）
- 事实源: blueprint.md acceptance.checklist 原文 + acceptance/run-29..31 入库记录；本叶只声明，不动蓝图（蓝图修订须经 schema 校验+用户确认，战后 /attack 职权）。
