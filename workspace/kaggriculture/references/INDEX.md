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
| `references/data/tetsuya-probe-0831/` | https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-08-31（外部回放数据集，抓取清单=包内 plan-tetsuya/plan-early.json） | 2026-09-02 | round-13 v10.9 深度匹配探针会话归档（混合包，用户指令整体迁入：raw/ 6 局 tetsuya 对局外部回放 ~185M + val/ 5 局本地验证 + variant_*.py 三开局变体 a_open_shift/ab/b_carrot + filelist/shard-0831 清单） | OPP-SUPPLY observer V0 验证语料（设计 v2 引用的"tetsuya 6 局"）；round-13 v10.9 探针复盘 |
| `references/data/online-replays/round21/` | https://www.kaggle.com/competitions/kaggriculture（`kaggle competitions episodes 56006990` + `kaggle competitions replay <eid>` + `kaggle competitions leaderboard kaggriculture -d`） | 2026-09-04 | v13.7（ref 56006990）线上 7 公开局 + 1 验证局回放，及当日公榜 zip | 本次线上对战复盘 |
| `references/data/online-replays/round20/` | https://www.kaggle.com/competitions/kaggriculture（`kaggle competitions episodes 56004582` + `kaggle competitions replay <eid>`） | 2026-09-04 | v13.6（ref 56004582）线上 25 公开局 + 1 验证局回放 | 与 round-21 对照的上一版生产样本 |
