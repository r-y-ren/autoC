# 战役总账与结构地图（COMPENDIUM，2026-09-23 大整合版）

> 本文=kaggressulture 战役的顶层总结与新结构唯一地图（用户令"开展总结+彻底整理：只留 fn_docs/ 与 fn_work/ 两目录"）。

## 一、战役总账（2026-08-28 → 09-30 赛季）
- **线上终局**：终榜对守成（零提交冻结至 09-30）；过程件：v48 公开衍生版（线上峰值带 1105-1146）、v48-hybrid-v2（1080.8，探针 25W-11L-2T）、v4b（≈v48 行为+死价保险）；我方原创最好 v14.1@543.6。全程 28 轮发射、台账 20-28 全 COMPLETE。
- **研究闭案五件**（证明级，详见 analyses/）：①卖侧保果无正参数区域（先知 1/14 可救+84 配置零翻正）；②参数级运营调整全拒（五臂+均衡口袋）；③孪生反事实噪声底 p90≈9k（本地涨线上跌之谜）；④巨人结构不可用固定磁带从外部复刻（R9 五线 1/5，镜像自打假阳）；⑤seated 口径必须构建期硬前置（方法论铁律）。
- **资产**：fn_work/ 新结构代码库（398 测试基线）；孪生/法证/画像全链；M0 引擎经济模型（22.9KB 机器可算）；123 局赢家计量；14 局领先崩塌语料+三门；四份战后搬移注册表。

## 二、新结构地图（根目录只有两个目录）
```
kaggressulture/
├── fn_docs/                      # 一切知识与治理
│   ├── COMPENDIUM.md             # 本文（顶层地图）
│   ├── README.md / requirements.md / responsibility.md / implementation/   # 重构梯（R1-R20 已实施，fn-close 终检待战后）
│   ├── analyses/ results/ machine_context.md recalculation_ledger.md provenance_dadee25a.md ...   # 分析轮全档
│   ├── governance/               # JOURNAL.md（未来追加在此）/ blueprint.md / strategy.md / metrics.json / acceptance/
│   ├── docs/                     # 原 docs/（SOP/决策树/findings/设计契约 12 件）
│   ├── hybrid/                   # v48_hybrid 梯全档（requirements/analyses/results/replays-lead-collapse…）
│   └── references/               # 情报 digests+INDEX+data/（410MB 本机语料，gitignored）
└── fn_work/                      # 一切代码
    ├── src/ tests/               # 重构梯新结构（398P 基线；含 snapshot 迁移套件）
    ├── legacy_software/          # 原软件整树（冻结提交链/kgenv/57 脚本/exports/v48_hybrid 代码/vendored wheel）——archival，路径锚已双布局兼容
    ├── snapshot_tests/           # 原快照套件（等价门 subprocess 目标=承重件，随行保留）
    └── artifacts/ minimal_repro_set/ …（重构梯产物）
```

## 三、整并账本（move/dedupe ledger）
| 原位 | 新位 | 处置 |
|---|---|---|
| JOURNAL/blueprint/strategy/metrics/acceptance/ | fn_docs/governance/ | 平移（治理脚本固定路径失效=登记退役；未来 JOURNAL 追加在 new 位） |
| docs/ | fn_docs/docs/ | 平移 |
| references/（含 410MB data） | fn_docs/references/ | 原子平移+gitignore 改写 |
| software/ 整树 901 件 | fn_work/legacy_software/ | git mv 纯 rename（零字节改动） |
| v48_hybrid/fn_docs/ | fn_docs/hybrid/ | 并入 |
| snapshot_tests/ | fn_work/snapshot_tests/ | 真重复但承重（等价门目标）→随行保留非删除 |
| hardware/（仅 .gitkeep） | — | 删除（空壳） |
| .pytest_cache/ | — | 删除（垃圾） |
**路径修复清单**：discover_campaign_roots 双布局/rollout conftest×2/等价门套件锚/snapshot 迁移模板/unify+guard 族发现器/regenerate_artifacts_lf 锚/online_probe replay_dir+campaign_root_from_software 双布局/.gitignore 3 行。**验证**：fn_work 套件 398P×2（=整合前基线）；监控链实测（round-28 close COMPLETE+gate 绿，回放落新位）。

## 四、合规声明
- 本次=重构梯 fn-close 终态动作的提前执行（用户 2026-09-23 明令），旧树零字节改动（纯 rename）；
- 与 AGENTS.md 标准布局（workspace/<cid>/{blueprint,JOURNAL,…}）的偏离：治理脚本（merge_metrics//accept/guard）固定路径失效，退役登记；跨机接力需同步本 commit；
- 零提交冻结与终榜对不受影响；09-30 前监控在新路径照常。
