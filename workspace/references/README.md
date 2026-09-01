# references/ —— 外部参考资料与数据的唯一归宿

**规则：战役进行中抓取/下载的一切外部材料，一律放在本目录对应的子目录，不得散落在 `software/`、`docs/`、workspace 根或其他任何位置。**

| 子目录 | 放什么 | 例子 |
|---|---|---|
| `rules/` | 赛方规则、Evaluation 说明、meta 页面快照 | `kaggriculture-rules-2026-08.md` |
| `data/` | 外部数据集、榜单快照、回放语料清单 | `leaderboard-0901.json` |
| `code/` | 第三方包（wheel）、外部仓库快照 | `kaggle_environments-1.32.7.whl` |
| `digests/` | 技术情报：讨论区摘要、榜首/对手解构、论文笔记 | `top-solution-analysis.md` |

## 硬性要求

1. **登记**：每新增一个文件，必须在 `INDEX.md` 登记（路径 / 来源 URL / 抓取日期 / 用途）。无来源的文件视为脏数据，验收可开单。
2. **出处**（AGENTS.md 铁律 1）：一切分析性内容逐条携带 `来源 URL + 抓取日期`，禁止凭模型记忆撰写。
3. **本工程产物不放这里**：`software/exports/` 只放本工程评估产物；本目录只放**外部获取**的材料。工程内部的临时探针输出放 `software/exports/probes/`，不要落在 `software/` 根或 `.tmp-*` 目录。

## 历史遗留说明

`software/vendor/`（wheel）与 `software/exports/intel/`（情报摘要）是本目录建立前的历史落点，已被脚本/manifest 引用，**保持原位不迁移**；此后新增的外部材料一律进本目录。
