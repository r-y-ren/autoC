# workspace/ —— 当前战役活跃开发区（v1 单战役约束）

**生命周期**：决策阶段生成 `strategy.md` + `blueprint.md` → 用户确认 → 交付阶段填充 `software/` `hardware/` `docs/` → 验收填充 `acceptance/` → `archive_campaign.py` 整体移入 `archive/` 并清空本目录，开启下一战役。

| 文件/目录 | 归属角色 | 说明 |
|---|---|---|
| `strategy.md` | Strategy | 攻略六节（strategy-template：矩阵/大显身手信号/一鱼多吃/合规风险/推荐结论；decide 态可写） |
| `blueprint.md` | Strategy | ★ 唯一蓝图契约，须过 blueprint.schema.json 校验 |
| `JOURNAL.md` | 协调者 | 阶段流转日志（提交入库，可审计） |
| `metrics.json` | Software/Hardware | 实测数据；Document Agent 数字唯一合法来源 |
| `software/` | Software | 代码 + 沙箱测试 |
| `hardware/` | Hardware | BOM / 引脚表 / 固件 |
| `docs/` | Document | 报告（Typst）+ PPT（Marp）源码 |
| `acceptance/` | 验收 | 执行记录 / 失败工单 / 分析报告（交付期只读） |

守卫策略与写入矩阵见 `scripts/guard/guard_path.py` 与 `docs/DESIGN.md` §6.2。
