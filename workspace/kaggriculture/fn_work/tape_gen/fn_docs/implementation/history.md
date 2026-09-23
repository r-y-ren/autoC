# history.md
| 完成日期 | 批次 | 清单 | 验收摘要 |
|---|---|---|---|
| 2026-09-22 | T1 | load_replay_corpus, extract_and_filter_seats, mine_trajectories | 14 passed；语料 182 局（/tmp 缓存先持久化 round26 74 局+round27-ext 37 局，14 投影件全被 full 去重压制）；轨迹库 364 席=保留 162+剔我方 185+克隆 17+其他 0；双跑逐字节一致；抽查清单 12 局（3 克隆行独立复核匹配） |
| 2026-09-23 | T1 | load_replay_corpus, extract_and_filter_seats, mine_trajectories | 14 passed+双跑逐字节；182 局/保留 162 席；抽查 12 局含旁路复核 |
| 2026-09-23 | T2 | 库+变体七函数 | 74 passed+双跑逐字节；骨干=真实赢家轨迹（42 席共享）；1 事件对齐分叉；v48 真值件载入金标准全过；8 市场变体 |
| 2026-09-23 | T3 | 搜索+选择六函数 | 97 passed；空间 320（10 件×2^5）+微轴扇出 2；对手级分离 109/48（30.6%）不相交+挖掘源圈禁；粗筛 320×8→精评 6×111→微轴→留出 3×51；真实搜索 852s/3490 rollouts；最终件 route:default+clone_preempt（留出 0.4706/+440，稀疏惩罚 λ=0.02 登记可调）；账本 22 行自证。事故+修复：误删 gitignored references/data 5.4G（/tmp 缓存+API 重抓恢复 162/162）；发现并修复 twin seat1 obs.step=None 致 seat-1 局全损（tape_gen 侧计数器补步，首跑作废重跑） |
| 2026-09-23 | T3 | 搜索+选择六函数 | 97 passed；320 候选 852s；最终=default+clone_preempt（留出 0.4706）；强闭环全负=v48 消融复现。**批内事故**：误删 workspace/（git restore+缓存回填+API 重抓 162/162 恢复）；发现 legacy twin seat-1 obs.step=None 缺陷（tape_gen 侧计数器修复，legacy 未动） |
| 2026-09-23 | T4 | 组装+管线四函数 | 127 passed；候选包 e8e8fbdf 四门绿；**M1=0/16 互胜 0.0<0.45 FAIL**（分档 BELOW_LINE：管线全通双跑一致，结构线未到）；候选自打 140k>v48 自打 92.7k=市场耦合假说 |
