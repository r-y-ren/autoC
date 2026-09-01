# workspace/ —— 当前战役活跃开发区（v1 单战役约束）

**生命周期**：决策阶段生成 `strategy.md` + `blueprint.md` → 用户确认 → 交付阶段填充 `software/` `hardware/` `docs/` → 验收填充 `acceptance/` → `archive_campaign.py` 整体移入 `archive/` 并清空本目录，开启下一战役。

| 文件/目录 | 归属角色 | 说明 |
|---|---|---|
| `strategy.md` | Strategy | 对比矩阵 + 一鱼多吃路线（decide 态可写） |
| `blueprint.md` | Strategy | ★ 唯一蓝图契约，须过 blueprint.schema.json 校验 |
| `JOURNAL.md` | 协调者 | 阶段流转日志（提交入库，可审计） |
| `metrics.json` | merge_metrics.py | 分片汇总生成物（角色禁写；分片在 software//hardware/ 下） |
| `software/` | Software | 代码 + 沙箱测试 + metrics 分片 |
| `hardware/` | Hardware | BOM / 引脚表 / 固件 + metrics 分片 |
| `references/` | 抓取材料的角色 | ★ 外部参考资料/数据/第三方包的**唯一归宿**（rules/data/code/digests 子目录，登记见其 INDEX.md） |
| `docs/` | Document | 报告（Typst）+ PPT（Marp）源码 |
| `acceptance/` | 验收 | 执行记录 / 失败工单 / 分析报告（交付期只读） |

守卫策略与写入矩阵见 `scripts/guard/guard_path.py` 与 `docs/DESIGN.md` §6.2。
