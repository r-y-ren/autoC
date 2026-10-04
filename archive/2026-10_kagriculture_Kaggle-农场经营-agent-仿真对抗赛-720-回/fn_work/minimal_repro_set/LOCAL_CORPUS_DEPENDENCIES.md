# 非入库语料依赖声明（LOCAL_CORPUS_DEPENDENCIES）

- 机制: package_minimal_repro_set → declare_local_corpus_dependencies（R19/G23）
- 用途: fresh clone 持最小集复算时，显式声明哪些结论仍依赖主力机语料、缺什么、如何在主力机补齐（不冒充可复算）。

## 1. 哪些结论依赖主力机语料（本机/fresh clone 不可复算）

- | G23 | 原始回放证据（references/data ~GB 语料、线上回放）gitignored：21/27 Track-B 脚本与 corpus/observer 族本机不可跑、8 skip 同因——fresh clone 不可复算画像与法证结论 | 数据归宿裁决（本机留存声明/小体积入库/接受不可复算） |
- 关键事实：**corpus_integrity（蓝图验收 cmd）本机实测 exit=1**（references/data/replay-corpus/manifest.json gitignored 缺失）——验收绿灯只在持数据机器成立（G23）。
- 口径: "990+2" 基线仅在 Windows 主力机 + 语料在机成立（口径原文见源文档）

## 2. 缺失件与补齐办法（逐件，来自收集登记）

- `software/exports/probes/planner_flagoff/golden_v138.json`（flagoff_golden）——补齐: 主力机重跑 python software/scripts/planner_flagoff_golden.py --emit 捕获基线写入该路径后，重跑本收集函数（README 旗关等价节）
- `references/data/online-replays/round23/episode-110634204-replay.json`（disaster_replay）——补齐: 主力机自线上 episode 拉取通道重新下载 round23 ep110634204 回放至该路径后，重跑本收集函数
- `software/exports/probes/twin_fidelity/fidelity_report.json`（twin_fidelity_manifest）——补齐: 主力机重跑 python software/scripts/twin_fidelity.py 生成后，重跑本收集函数
- `references/data/replay-corpus/manifest.json`（twin_fidelity_manifest）——补齐: 主力机 python software/scripts/corpus_fetch.py --stage 重建台账后，重跑本收集函数

## 3. 数据依赖 skip 清单（缺什么逐项标注，源=fn_docs/machine_context.md）

- 本次运行 0 个数据依赖 skip（本机无缺失项触发；历史口径的语料缺机 skip×8 见上节旧树分类）。

## 4. 环境性失败/skip 分类中语料相关项（历史事实口径）

- **gitignored 数据缺机×3**: （语料/参考数据不在库内）——复现链依赖 machine-local gitignored 语料，缺机即挂
- **语料缺机 skip×8**: （8 skipped 全为语料缺机）——数据依赖项显式 skip（缺语料），非代码缺陷

## 5. 来源（引用纪律）

- fn_docs/behavior_inventory.md [在库]（读取日期 2026-09-22）
- fn_docs/machine_context.md [在库]（读取日期 2026-09-22）
- 收集登记: fn_work/minimal_repro_set/MANIFEST.json（本函数调用方落盘）
