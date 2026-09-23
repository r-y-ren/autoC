# history.md
| 完成日期 | 批次 | 清单 | 验收摘要 |
|---|---|---|---|
| 2026-09-22 | T1 | load_replay_corpus, extract_and_filter_seats, mine_trajectories | 14 passed；语料 182 局（/tmp 缓存先持久化 round26 74 局+round27-ext 37 局，14 投影件全被 full 去重压制）；轨迹库 364 席=保留 162+剔我方 185+克隆 17+其他 0；双跑逐字节一致；抽查清单 12 局（3 克隆行独立复核匹配） |
| 2026-09-23 | T1 | load_replay_corpus, extract_and_filter_seats, mine_trajectories | 14 passed+双跑逐字节；182 局/保留 162 席；抽查 12 局含旁路复核 |
| 2026-09-23 | T2 | 库+变体七函数 | 74 passed+双跑逐字节；骨干=真实赢家轨迹（42 席共享）；1 事件对齐分叉；v48 真值件载入金标准全过；8 市场变体 |
