# sync_documentation 收口报告（W4 文档层，B14 实跑）

> 生成：fn_work/src/sync_documentation/sync_documentation.py（2026-09-22T02:35:35+08:00）。
> 对账口径：修正副本覆盖 gap_table §一全部 8 项对应面（旧树物理修正战后；新文档面锚点逐项在档）。

## 三叶产物

- **fix_bc_track_records**：修正副本 8 件（README 3 处 diff+票面 03/08/04-07 六件 Status diff=9 处），diff 注册=fn_work/doc_fixes/bc_track/diff_registry.json（战后套用清单，台账依据=JOURNAL 2026-09-21 收口行）。
- **retire_codemap_with_errata**：勘误 E1/E2/E3/E4 落 fn_work/doc_fixes/codemap_errata.md；退役时点=战后 fn-close 期（旧树冻结解除，与 archive_forensic_assets 注册表同批执行）。
- **codify_probes_policy**：策略文档落 fn_work/doc_fixes/probes_policy.md；现存 6 份摘要全部入库（all_tracked）；不一致 1 条（规则面缺口，已标 postwar_action）。

## gap_table §一 8 项对账（新文档面清零核对）

| # | 旧面失准表述 | 实况 | 新文档面覆盖（对应面） | 清零 |
|---|---|---|---|---|
| 1 | README 功能表#1『stdlib-only 单文件自包含程序』 | tar.gz 多模块包（main+src 10+planner 6）；『薄装载器』表述反而正确 | fn_docs/README.md §工作流程A#1+功能#1（多模块包修正面） | ✓ |
| 2 | README 流程A#1『九个功能模块』 | _MODULE_ORDER=10 模块（wave 加入后）；main.py 头注释同过期 | fn_docs/README.md §A#1『十个』+responsibility.md 迁移口径 | ✓ |
| 3 | README 功能表#3『Elo/BT 评级（顺序无关批量）』 | Elo 顺序敏感（其序恰为冻结回归门依据）；仅 BT 批量顺序无关 | fn_docs/README.md 功能#3（双轨口径拆分） | ✓ |
| 4 | README 功能表#3 将『红线清单』列为本地评估体系组成 | redlines.py 零 gate/arena 消费，孤儿模块 | fn_docs/responsibility.md R13/R14 处置（economy/redlines 移测试资产区） | ✓ |
| 5 | README 功能表#7『四套公开顶级 bot 的解码版（v48/2945/island-ga/kaggri）』 | 库内 opponents/ 仅 v48_main+v72 两套；2945/island-ga/kaggri 系 machine-local references（gitignored）不入库 | fn_docs/README.md 功能#7『入库两套』+本批 codemap_errata E4 | ✓ |
| 6 | README 功能表#2/流程隐含『孪生与 d0 反事实=可信计算』 | 孪生本身逐位保真成立；harness 席位错位使 me_seat=1 局 d0 反事实/离线基准数字系伪影（已知勘误，重算入台账） | fn_docs/README.md 功能#2 口径注+recalculation_ledger.md 双口径台账 | ✓ |
| 7 | README 工作流程 D『每波过查→/accept 全量验收→分片汇总入 metrics』 | /accept 链 09-01 起静默（m6/m7 无验收记录）；事实治理=JOURNAL 详记+git 提交+metrics 分片 | fn_docs/README.md §D 实际治理现状（诚实口径） | ✓ |
| 8 | CODEMAP『economy.py market.py 消费』『profile_v48_gap 在役』『53 tests』『opponents』 | economy 零消费；profile_v48_gap 路径损坏必崩；51 tests；入库两套 | 本批 doc_fixes/codemap_errata.md（E1-E4 勘误+退役标记） | ✓ |

## 战后动作（旧树冻结解除后套用）

- bc_track 修正副本+diff 注册（9 处）按 diff_registry.json 战后套用并跑 R7 复现命令核验
- CODEMAP 勘误（4 条）战后套用，CODEMAP 随 fn-close 退役（替代面=responsibility.md+包 docstring）
- postwar_action: 战后把 exports/probes 白名单补为 !**/*.md（或目录级规则），套用前新增摘要须手工 git add -f

## 裁决: PASS（8/8 清零）
