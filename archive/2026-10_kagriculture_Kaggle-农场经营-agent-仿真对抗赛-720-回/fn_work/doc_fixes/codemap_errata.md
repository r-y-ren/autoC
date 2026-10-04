# CODEMAP 勘误记录与退役标记（R16/R19-勘误部分）

> 对象：software/CODEMAP.md（2026-09-21 版，本批只读零改动——旧树冻结）。
> 形态：勘误记录+退役标记；CODEMAP 物理退役=战后 fn-close（套用本记录后随新结构落地）。
> 生成：fn_work/src/sync_documentation/retire_codemap_with_errata.py（B14，2026-09-22T02:35:35+08:00）。

## 勘误（4 处失准，证据=本批实读实测）

### E1（CODEMAP L93，主题: profile_v48_gap）
- **CODEMAP 原文**：C 节『sprintA_structure_probe.py / profile_v48_gap.py / m4_switchover_regression.py / solver_shadow_stats.py | …（历史在役）』——profile_v48_gap 被归入在役面
- **实况**：输出路径损坏，不可复跑：scripts/profile_v48_gap.py:22-24 的 REPO_ROOT 解析为 workspace/ 容器目录（SOFTWARE_ROOT 上两级），:100 再拼 'workspace/kaggriculture/software/exports/probes/intel' 得双重前缀 workspace/workspace/…（不存在），:101 scratch.mkdir(exist_ok=True) 无 parents=True 即 FileNotFoundError——一跑即崩
- **证据**：profile_v48_gap.py:22-24/100-101 实读；workspace/ 下无 workspace/ 子目录（实测）
- **修正口径**：归类改『历史件（路径损坏，复跑需先修输出路径与语料依赖）』；v48 差距画像的现役事实面=exports/replay_profiles 台账与 fn_docs 记录

### E2（CODEMAP L40，主题: economy）
- **CODEMAP 原文**：B 节『kgenv/economy.py | 经济语义镜像（价格公式/棚容/城镇需求——market.py 消费）』
- **实况**：market.py 消费不实：全库 economy 导入扫描仅三处——kgenv/__init__.py:19（eager 再导出）、kgenv/redlines.py:33（自身即评估链孤儿）、tests/test_economy.py:11（测试）；提交链 src/market.py 与 scripts/ 零消费
- **证据**：grep 'kgenv.economy|from .economy|import economy' 全库实测三命中，market.py 零命中
- **修正口径**：口径改『评估链孤儿库件（仅测试与再导出消费）』；处置=R13/R14 移测试资产区（fn_docs/responsibility.md downgrade_dormant_assets 块）

### E3（CODEMAP L95，主题: tests）
- **CODEMAP 原文**：D 节『tests/（53 个测试文件，基线 990 passed+2 skipped）』
- **实况**：tests/test_*.py 实数 51（另有 conftest.py 引导件非测试）；基线 990+2 系 Windows 主力机+语料在机口径（本机 Linux 976P/8F/8S 属环境性，R6 机器语境）
- **证据**：ls tests/test_*.py | wc -l = 51（实测）；机器语境见 fn_docs/machine_context.md
- **修正口径**：计数改 51；基线数字挂机器语境标注（机器无关化=R6 portable_test_baseline）

### E4（CODEMAP L111，主题: opponents）
- **CODEMAP 原文**：E 节『opponents/ | 本地陪练源码：v48_main.py（top-10 解码版）、v72_main.py（历史代）+PROVENANCE.md』——未标注入库落差
- **实况**：入库恰两套（ls 实测：v48_main.py+v72_main.py+PROVENANCE.md）；旧 README 面『四套公开顶级 bot 的解码版（v48/2945/island-ga/kaggri）』中 2945/island-ga/kaggri 系 machine-local references（gitignored）不入库——本行未标注该落差，与 README 旧面叠加留有『≥三套在库』误读空间
- **证据**：kaggle_simulations/opponents/ 目录实测两 .py；opponents/PROVENANCE.md 仅两源记录；gap_table §一#5（证据=opponents/、PROVENANCE.md）
- **修正口径**：入库清单=两套口径（fn_docs/README.md 功能#7 已回写『入库两套』）；2945/island-ga/kaggri 标注为本机 references 参考件

## 退役标记

- **时点**：战后 fn-close 期（旧树冻结解除，与 archive_forensic_assets 注册表同批执行）。
- **替代面**：
  - fn_docs/responsibility.md——新结构单一事实源（功能块/子函数/职责/签名意图/核验命令）
  - fn_work/src/<功能块>/<模块>.py 包 docstring——逐文件用途与实现要点
- **退役附注（清单漂移，非勘误主项）**：G 节 probes 子目录清单（round23_forensics/v48_launch/v48plus）与现状（planner_bench/twin_fidelity/v143_sellrace/v15_ignition）漂移——probes 清理所致；probes 面策略由本批 fn_work/doc_fixes/probes_policy.md 显式化
