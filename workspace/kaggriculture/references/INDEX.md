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
| `references/data/online-replays/round20/`（2026-09-19 扩样） | https://www.kaggle.com/competitions/kaggriculture（`kaggle competitions episodes 56004582 --format json` + `kaggle competitions replay <eid>`，经 software/scripts/forensic_harvest.py 限量抓取最新 12 公开局，manifest 见目录内 forensic_manifest.json） | 2026-09-19 | 终交冲刺 ① 证据收口：round-20 扩样至 37 公开局 | cmp_*_deep_stats 法证对比；round20_sampling 刷新 |
| `references/data/online-replays/round21/`（2026-09-19 扩样） | 同上（ref 56006990，最新 12 公开局） | 2026-09-19 | 终交冲刺 ① 证据收口：round-21 扩样至 19 公开局 | 同上 |
| `references/data/online-replays/round8/` | 同上（ref 55943264 v10.3，最新 12 公开局） | 2026-09-19 | v10.3 线上现况对照样本（12 局 8W-4L，score 658.2） | cmp_round8_deep_stats；老候选 vs v13 系法证 |
| `references/data/online-replays/round15/` | 同上（ref 55965149 v12.2，最新 8 公开局） | 2026-09-19 | v12.2 线上现况对照样本（8 局 2W-6L，score 603.1） | cmp_round15_deep_stats |
| `references/data/online-replays/round18/` | 同上（ref 55991647 v13.4，最新 8 公开局） | 2026-09-19 | v13.4 激进包补采样（8 局 4W-4L，score 576.2） | cmp_round18_deep_stats |
| `references/data/online-replays/round19/` | 同上（ref 56003101 v13.5，最新 8 公开局） | 2026-09-19 | v13.5 plant19 补采样（8 局 4W-4L，score 532.2） | cmp_round19_deep_stats |
| `references/data/online-replays/cmp-v92/` | 同上（ref 55902180 v9.2 无台账锚定，直查 ref 抓最新 12 公开局） | 2026-09-19 | v9.2 线上现况对照组（12 局 6W-6L，score 663.3=本队现役最高） | cmp_cmp-v92_deep_stats；"为何 v13 系输给 v9.2" 法证 |
