# INTEGRATION.md —— orderbook_p4up_lab 接入 run_judgment 管线（安全窗口执行）

状态：**2026-10-02 交付即插件，未接入**。P1 正在用既有判决 harness 跑池测，本包
不改任何既有共享文件（`orderbook_*_lab` 既有目录、`run_judgment.py`、`judge_*.py`
一律未动）；本文件=安全窗口的接入说明书。全部代码为纯 stdlib、离线、无网。

## 1. 模块图

| 文件 | 职责 |
|---|---|
| `records.py` | EpisodeRecord 归一模型 + 两种动作指纹：`canon`（x-ray cell 10，逐位严比）/ `bundle_key`（leoprovorov cell 11，MOVE 并类+数量丢弃+market 集合） |
| `adapters.py` | 入口 A：kaggle-environments 回放 blob → record（**t+1 对齐**，cell 40 陷阱）；入口 B：feats-band.jsonl 行 → day0 片段 record（hands 通道缺、量桶化，lossy_notes 全程声明）；compact JSONL 读写 |
| `criteria.py` | 六判据实现 + `CRITERIA_SPEC`（每判据：定义→输入→输出→阈值来源；x-ray 自校准数全标"自报"） |
| `divergence.py` | leoprovorov D(t)/K(t)/p10/p25/p50 磁带长度刻度（cell 11/17 数学区） |
| `baseline.py` + `data/opponents_baseline.json` | 11 队 p10/p25/p50 自报基线（cell 16 ROWS）+ 口径注 + 来源 + 我方派生 tape_tier 分层 + `profile_lookup()` 最近邻 |
| `extract_replays.py` | parquet 回放分片 → compact records（duckdb **恒走 bwrap 沙箱**，断网/根只读/仅 /tmp 可写） |
| `run_report.py` | 六判据 + 磁带画像 + 基线分层样例报告 CLI（evidence JSON + txt） |
| `samples/` | TFC 2026-09-23 cohort（24 局 compact records）+ 样例报告 |
| `test_*.py` | pytest 94 判例（金值/边界/负例）；`python3 -m pytest orderbook_p4up_lab/` 全绿 |

## 2. 数据契约（新数据源接入只需 ~20 行适配）

判据层只认 `EpisodeRecord`：`stream/opp_stream`（逐拍 action dict，720 拍形）、
`world`（前两店有序对，判据①组内读数用）、`margin/opp/opp_sub`（判据②战绩）、
`prices_t`（判据⑤）、`occ/pres/unlocked` 10x10 网格（判据⑥）、`window`（片段标记）。
已有两入口（回放 blob / feats-band）；本地 sim（kgenv/sim_bridge）回放如需第三入口，
按 `adapters.replay_to_record` 的字段映射写一个 `sim_to_record` 即可，判据层零改动。

## 3. 安全窗口接入 run_judgment（建议步骤）

前提：P1 池测结束、全局 idle（D14）。按序：

1. **不动** `orderbook_surge_lab/` 任何文件；在 `orderbook_p4up_lab/` 新增
   `judgment_hook.py`（薄封装）：输入=池测 per-game 结果 + 可得流，输出=evidence
   里一个 `p4up` 块。
2. `run_judgment.py` 末段（evidence 落盘前）加 3-5 行：若 `--p4up` 开关开启则调
   `judgment_hook.emit_p4up(...)` 把六判据读数并入 evidence JSON。**开关默认关**，
   未开则零行为变化（P1 重跑不受扰）。
3. 流数据分级接法（按池测实际可得）：
   - 有逐局流（回放/快照）→ `adapters.replay_to_record`（或 sim 适配器）→
     六判据全量 + `divergence.tape_profile`；
   - 仅有汇总行 → 仅 `baseline.profile_lookup` 分层 + `tape_profile` 需流时显式
     INSUFFICIENT（不编数）。
4. 证据纪律：每判据输出自带 `threshold` 字段（阈值随判声明，cell 33）；
   "自报"数字只进 spec 注记不进读数；INSUFFICIENT_DATA 如实落册（fail-soft 读数、
   fail-closed 放行）。
5. 跑一遍既有测试确认零回归：`python3 -m pytest orderbook_surge_lab orderbook_p4up_lab`。
6. contract_version bump 随接入 commit+push（接力纪律），JOURNAL 登记。

## 4. 与 49 P1 评测协议整包的衔接点

49 P1=「评测协议整包进 P4 判决尺（alperen 四件套 + shiiin9 世界 CI + ΔΦ lockstep
+ 选优双尺）」。本包（P3 判决尺升级）与其是同一 P4 尺的两把补尺，衔接点：

| 49 P1 组件 | 本包衔接 | 接法 |
|---|---|---|
| 选优双尺化（面板 BT+弱面门为主尺） | **对手分层**：`baseline.profile_lookup` 的 tape_tier（DAY0_FIRE/EARLY_FORK/SHOP1_FORK/SIX_DAY_TAPE）给 BT 面板按磁带形态配对手；C2 基因群给"该打谁"清单（foreign group 负 margin_med=靶单） | panel 组局时读 baseline + C2 输出 |
| alperen frozen-rival 复盘 | **C2 镜像线**：plan≥0.95 认同录/同底盘对手——"frozen rival"=镜像或纯回放，C1 PURE_REPLAY 直接指认 | 配对前 kinship 预扫 |
| alperen 12 种子簇 paired CI / shiiin9 64 世界级 CI | **C1 WITHIN-WORLD**：同世界组内互比=剥掉店抽 seed 效应后的行为读数，正是世界分层 CI 的行为侧同源口径 | 世界组=CI 簇的分组键复用 |
| shiiin9 wrapper 陷阱检测（假 +PASS） | **C1 分类**：REPAIRING_SCRIPT/PURE_REPLAY 的通道指纹（market-only 变动）与"假 PASS 卫生"同族；C4 语言指纹 SCRIPT 锚（自报 1.00/0.91-1.00/0.74-0.91）可作 wrapper 体检 | 放行门加 C1/C4 读数 |
| ΔΦ lockstep（卖单实验目标函数） | **C5 crater**：卖流对抗性读数（一阶伤害=数量×价差）= ΔΦ 的对手伤害侧；S8 尖拍捕获可测其砸价伤害 | 卖单实验 evidence 加 C5 块 |
| 跨块 ≥3 块同向协议 | **C3 收敛三件套**：DRIFT/SIGN FLIPS/n 判"读数是否已停"，阈值随判声明；配对速率只换算 reread ETA 不进判决 | 判决重跑节奏用 C3 输出定读数时刻 |
| 反伪影纪律 | **C6 半分闸** r≥0.9：热图/棋盘类判决不过闸只当噪声 | 棋盘类读数全走 C6 闸 |

合并建议：49 P1 落地时把上述七行作为 P4 判决尺的"读数清单"合并成一张表
（判据→门禁级→阈值），比两包各自为战省一次返工。

## 5. 已知限界（接入时保持声明）

- 事后镜：六判据只读已发生对局，对未提交变体无预测力（x-ray 自述）。
- t<48 可观测盲区；语言指纹日带从 d6 起——恰好在六日磁带终点之后，磁带族的
  磁带段本身不进语言读数（样例 TFC=SCHEDULER 读数即此限界实证，见报告 §四）。
- 判据③需评分轨迹（ListEpisodes updatedScore 序列）；回放本体无此字段，
  接入时从池测台账/lb 拉取传入 `convergence(traj)`。
- leoprovorov 基线数字全自报（数据源已撤回）；对读必带口径差声明
  （胜局 vs 全集、样本窗 ≤09-20 vs 09-23、版本混样）。

## 6. 复现命令

```bash
cd fn_work/legacy_software/kaggle_simulations
python3 -m pytest orderbook_p4up_lab/ -q            # 94 判例全绿
python3 -m orderbook_p4up_lab.extract_replays \     # duckdb 走 bwrap
  --shards-dir ../../fn_docs/hybrid/references/ext/fingerprint-scan/raw/ashok205-shards \
  --feats-band ../../fn_docs/hybrid/references/ext/fingerprint-scan/band-analysis/feats-band.jsonl \
  --team "THIRD FARM CLUB" --src replays_2026-09-23.parquet --limit 24 \
  --out orderbook_p4up_lab/samples/cohort_tfc_20260923.jsonl
python3 -m orderbook_p4up_lab.run_report \
  --records orderbook_p4up_lab/samples/cohort_tfc_20260923.jsonl \
  --feats-band ../../fn_docs/hybrid/references/ext/fingerprint-scan/band-analysis/feats-band.jsonl \
  --feats-team "THIRD FARM CLUB" \
  --out orderbook_p4up_lab/samples/xray_p4up_sample_report.json
```
