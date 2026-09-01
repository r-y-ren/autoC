# references/INDEX.md —— 参考资料台账

每新增一个文件登记一行；无来源登记的文件视为脏数据（验收可开单）。

| 路径（相对本战役根） | 来源 URL | 抓取日期 | 用途 | 引用它的产物/任务 |
|---|---|---|---|---|
| （历史）`software/vendor/kaggle_environments-1.32.7+nodeps-py3-none-any.whl` | https://www.kaggle.com | 2026-08 | 本地评估环境依赖（评估链 manifest 引用的规范路径，位于 software/ 内） | kgenv/ |
| （历史）`software/exports/intel/*.md` | 见各文件头部 | 2026-08 | 情报摘要（分析脚本引用，位于 software/exports/intel/） | exports/ |

| `references/data/replay-corpus/` | https://www.kaggle.com/competitions/kaggriculture（官方回放库，corpus_fetch 抓取） | 2026-08 | 60 集冻结回放语料（m1/m2 验收链输入，~1.8G） | corpus_integrity / corpus_build / test_replay_corpus |
| `references/data/replay-dna/` | https://www.kaggle.com/datasets/destbreso/kaggriculture-replay-genomes | 2026-08 | 回放 DNA 数据集（barcodes/consensus/field_validation，~108M） | dna_integrity / analyze_dna_forensics |
| `references/data/online-replays/` | https://www.kaggle.com/competitions/kaggriculture/leaderboard（线上对局 API + 榜单 zip） | 2026-08 | round2-7 线上对局回放与榜单（~1.5G） | online_pool / test_replay_success / corpus_fetch |
| `references/data/intel-notebooks/` | https://www.kaggle.com/competitions/kaggriculture/code（公开 notebook 原件快照） | 2026-08 | 外部选手 notebook/情报原件（~75M） | exports/intel 摘要的上游原件 |

<!-- 新条目从这里追加 -->
