# fn-ladder 文件 → 答辩叙事段映射（PPT 资产层，v2）

数据源改道（2026-10-09）：PPT 取材不再依赖 metrics.json 链，直接面向 fn-ladder 产物布局。
取材器 `scripts/ppt/collect_deck_material.py` 按本表抽取，数字**逐项标注来源文件**。

| 叙事段 | fn 来源 | 说明 |
|---|---|---|
| 一、作品（目标与价值） | `fn_docs/requirements.md`（R1..Rn） | 一句话主张取最高价值需求；指标即需求里的量化条款 |
| 二、方法（结构与实现） | `fn_docs/responsibility.md` + `implementation/functions.md`（+tracker） | 职责树 + 函数级状态（stub/implemented/tested/wired/blocked） |
| 三、实测（数据与图表） | `fn_work/runs/**` + `fn_docs/results/**` | 取材器数据表；每行必须带来源（文件:行/键） |
| 四、对比（基准与优劣） | 目标 × 实测对照 | 同名/含同名键对照；对不上就并列展示并注明 |
| 五、总结（结论与展望） | `fn_docs/acceptance.md` | 六道终检摘要；缺失如实标注 |
| 补充·进度 | `fn_docs/implementation/tracker.md` | 步骤账本（done/total），注记在方法段尾 |
| 补充·分析 | `fn_docs/analyses/`（报告 + registry.jsonl） | 对比/结论段的分析证据 |

**数字纪律**：初稿数字只允许来自取材器数据表（带来源标注）；任何"约/预计/业内一般"式数字禁止上片。
缺失项在末页"缺失"注记，不得用占位数字顶替。
