# Kaggriculture 软件交付（workspace/software）

Kaggle Simulation Competition **Kaggriculture**（Google/Kaggle 农场经营 720 回合博弈）的
bot、本地评估基建、机制量化工具与增强策略 A/B。

当前 working candidate `v10.3` 仅为 development，尚未针对本轮运行新的 holdout 或线上提交；下文的线上记录属于历史 v10.2/v10.3 前序提交观测，不能作为当前候选验证。

**评估规则变更（2026-09-02，用户决策）**：本地对手池（同族实现的 bots）**不再作为候选强度参考与上线门禁**——同族偏移已被多轮线上实测证实（本地 holdout 94.3% 对 v10.2 线上 42.9%）。此后候选验证以**线上天梯实测**为准（提交流程见 sop-v4；线上样本仍受 ≥6 局评估门与止损线约束）。保留仍然有效的两类检查：① 单元/契约测试与身份链校验（代码行为契约，非对手比较）；② 引擎一致性冒烟（smoke_boot）。`run_eval`/`iterate_gate`/`ablate`/`check_opponent_strength` 等本地对手评估资产保留为可选诊断工具，不再是上线前置条件。

**引擎边界声明**：本地对局运行在**官方引擎**上——PyPI `kaggle-environments` 1.32.7 的
`kaggriculture` 场景（本仓 vendor 了去依赖元数据/去可视化资源的重打包 wheel，引擎代码未改动，
见 `vendor/WHEEL_PROVENANCE.md`）。本地评估结果代表官方规则语义，但**不等价于** Kaggle 线上
天梯（对手分布不同、未做线上提交）。

## 一键命令（仓库根目录执行）

```bash
# 1) 依赖安装（锁定）
python -m pip install -q -r workspace/kaggriculture/software/requirements.txt

# 2) 冒烟自检（起环境 -> 自博弈 -> 契约校验 -> 退出码判定，超时看门狗 300s）
python workspace/kaggriculture/software/smoke_boot.py

# 3) 测试套件
python -m pytest workspace/kaggriculture/software/tests -q

# 3b) 外部 H2H 正式证据（只读黑盒压力测试；与 promotion/holdout 隔离）
#     v48/v72 字节留在 kaggle_simulations/opponents，输出可指定到任意用户路径
python workspace/kaggriculture/software/scripts/h2h_external_probe.py \
  --out workspace/kaggriculture/software/exports/external/v48-smoke.json \
  --opponents v48 --seeds 101,102
python workspace/kaggriculture/software/scripts/check_external_h2h.py \
  --input workspace/kaggriculture/software/exports/external/v48-smoke.json

# 3c) 顺序无关 BT/Davidson 描述性评级（不证明 holdout 泛化；Elo 仍为历史附录）
python workspace/kaggriculture/software/scripts/fit_bradley_terry.py \
  --input workspace/kaggriculture/software/exports/eval_results.dev.json \
  --output workspace/kaggriculture/software/exports/external/ratings.dev.json \
  --bootstrap 200 --bootstrap-seed 20260831

# 4) 强度门（认证池全体——m1 强对手 + m2 线上风格对手——须对冻结弱池 >=50% 胜率，不达标退出码 1）
python workspace/kaggriculture/software/scripts/check_opponent_strength.py --rounds 3

# 5) 开发评估（所有 pair×seed 均跑 AB/BA；只写 eval_results.dev.json）
python workspace/kaggriculture/software/scripts/run_eval.py --rounds 4

# 5b) 扩展池开发评估（--extended-pool 把 m2 线上风格对手加入矩阵；正式 export 保持冻结矩阵）
python workspace/kaggriculture/software/scripts/run_eval.py --quick --extended-pool

# 6) 正式开发门发布（完整矩阵 + 回归门通过后才原子替换 eval_results.json）
python workspace/kaggriculture/software/scripts/run_eval.py --rounds 4 --assert-regression --official

# 7) m2a 契约自证（缺对手/单座位/异常 fail-closed；发布原子性）
python workspace/kaggriculture/software/scripts/check_eval_contract.py --mode gate
python workspace/kaggriculture/software/scripts/check_eval_contract.py --mode export

# 8) 失败模式探针（submission 对全池多种子深记录，产出 failure_modes.md 的证据层）
python workspace/kaggriculture/software/scripts/analyze_failure_modes.py --rounds 8

# 9) 完整迭代门（8 必测对手 × 4 seeds × AB/BA = 64 局；自定义子集仅 exploratory）
python workspace/kaggriculture/software/scripts/iterate_gate.py --candidate workspace/kaggriculture/software/kaggle_simulations/agent/main.py --label candidate --rounds 4 --require-complete

# 10) 只读身份自检（working/frozen/published 三类身份以 active_candidate.json 为准；
#     校验含 README 投影，从仓库根直接运行）
python workspace/kaggriculture/software/scripts/check_candidate_identity.py

# 11) LLM A/B（每局重建 provider/budget；无完整 KG_LLM_* 时只做 NullProvider 自检）
python workspace/kaggriculture/software/scripts/run_llm_ab.py --rounds 4

# 12) m1 回放语料（战役 III）：重建画像档案 + 完整性校验（原始回放在 gitignored .tmp-corpus/）
python workspace/kaggriculture/software/scripts/corpus_build.py
python workspace/kaggriculture/software/scripts/corpus_integrity.py --mode official

# 13) holdout 证据链（一次性；只可验证，不可重跑/换种子）：
#     attempt-1（战役 II 92.9%）归档于 exports/holdout/attempt-1/；
#     attempt-2（m3 候选 5713c17e，576 局，84.4%）归档于 exports/holdout/attempt-2/；
#     attempt-3（r3-3 r4 候选 9298751f，全池 10 agent × C(10,2)=45 对 × 8 新种子
#     × AB/BA = 720 局，46 种子排除）归档于 exports/holdout/attempt-3/；
#     attempt-5（v7.2 候选 c44e2b25，11 对手全池 × 8 新种子 × AB/BA）为当前权威代，
#     发布于 exports/holdout/published/，正式投影原子替换 eval_results.json；
#     历史/现行身份一律以 active_candidate.json 为准
python workspace/kaggriculture/software/scripts/run_holdout.py --verify-published --require-frozen
python workspace/kaggriculture/software/scripts/check_eval_contract.py --mode official --input workspace/kaggriculture/software/exports/eval_results.json

# 14) r3-P0 分层构建基础设施（战役 III round-3）：
#     a) 成功口径回放分析（observation 状态差分；影子校验 0 mismatch 才可信）
python workspace/kaggriculture/software/scripts/replay_deep_stats.py <replay.json>... --success-json workspace/kaggriculture/software/exports/online/<name>_success_stats.json
#     b) 配对消融门（candidate vs 冻结 champion，同 (对手, 种子, 座位) 配对；
#        合并门三指标：新风格池胜率 >= / 最差单风格胜率 >= / 灾难败局率 <=，产物仅入 exports/ablations/）
python workspace/kaggriculture/software/scripts/ablate.py --candidate workspace/kaggriculture/software/kaggle_simulations/agent/main.py --label <layer-label>

# 15) P2 DNA/liveness 离线法证（仅显式本地 .tmp-dna 四件套；不运行 replay/engine/network）
python workspace/kaggriculture/software/scripts/analyze_dna_forensics.py \
  --barcodes .tmp-dna/barcodes.csv \
  --consensus .tmp-dna/consensus.csv \
  --references .tmp-dna/reference_barcodes.csv \
  --field-validation .tmp-dna/field_validation.json
python workspace/kaggriculture/software/scripts/check_dna_forensics.py
```

### P2 DNA/liveness scope

`exports/replay_dna/` is an offline exploratory identity/liveness evidence layer. It consumes only the explicit local `barcodes.csv`, `consensus.csv`, `reference_barcodes.csv`, and `field_validation.json` under `.tmp-dna`; all four inputs are source-hashed and the report is recomputed during verification. Each barcode is exactly 30 ordered lowercase 10-hex loci, with the genome accession defined as the first 8 characters of the SHA-1 of the concatenated bands. Stability is the mean per-locus modal agreement across all episodes in one submission-wide group (both seats; team must be unambiguous). RMP uses the field-specific allele frequencies and declared floor, with the notebook's exact strict thresholds.

This is producer/source-attested precomputed barcode evidence, not an independent replay reconstruction: `extractor_status=source_extractor_not_published`. `IDENTICAL / SAME SOURCE` means only 30-band anchor equality; it does not prove the same agent or a real source. DNA stability is separate from engine action liveness. The artifacts are explicitly exploratory and are not strength, promotion, holdout, online, or performance evidence. DNA outputs are restricted to `workspace/kaggriculture/software/exports/replay_dna/`, and action, observation, state, market, price, quantity, inventory, and raw trace fields are rejected recursively.

<!-- ACTIVE_CANDIDATE_IDENTITY:BEGIN -->
working_candidate_sha256=67e68c3acf29aae65e90838ea759ba51a82de75259b45d612931c779350c1003
working_candidate_status=development
last_promoted_frozen_sha256=c44e2b254686fc34ebfd055f51519f2aaac4a09bc68e2ac1f959f35b7ac90748
published_holdout_candidate_sha256=c44e2b254686fc34ebfd055f51519f2aaac4a09bc68e2ac1f959f35b7ac90748
published_holdout_attempt_index=5
engine=kaggle-environments 1.32.7 kaggriculture
<!-- ACTIVE_CANDIDATE_IDENTITY:END -->

## External H2H 与评级限制

`h2h_external_probe.py` 生成 `external-h2h/2.0`。每局包含唯一 `game_id`、显式 seed/AB-BA 座位、720-state completion、producer-attested activity traces、异常原因与 rewards/margin；验证器从这些生产者声明的 traces 重算活性汇总并校验赛程和 W/L/T/margin，复核候选/对手 SHA、运行时 Kaggle 包关键源码与 vendored wheel 字节一致、active candidate 身份、输入闭包和 canonical digest。该契约验证内部一致性与当前工作区来源，不提供防篡改签名，也不把 traces 描述为验证器从原始引擎回放独立重建。v48 在 `opponents/PROVENANCE.md` 中没有可验证的复用许可，因此只能作为只读黑盒压力对手，不能进入 submission 或被描述为正式胜率证据。v48 历史 smoke fixture `exports/external/v48-seed101-smoke.json` 继续绑定 v10.2 SHA `360714f1…`，不是 v10.3/M-G 证据；active working SHA 变化后，strict validator 应对该历史 fixture fail-closed。

`fit_bradley_terry.py` 使用全批次 Bradley-Terry（无和局）或 Davidson（含和局）模型；固定 zero-sum identifiability，断连图 fail-closed，完全分离时使用已披露的 Gaussian MAP 正则。置信区间按 seed clustered bootstrap，固定 `--bootstrap-seed` 且与输入行顺序无关。BT/Davidson 评级是描述性排名，不是 holdout 泛化证明；只有 CI 完全跨越预注册 margin 才给出 tier，否则为 `same`/`uncertain`。

## Active Candidate Identity

`active_candidate.json` is the machine-readable source of truth for candidate roles.
The working candidate is development-only and must not be described as frozen or
holdout-tested. The last promoted frozen candidate and the published holdout
identity are historical references until a separately approved freeze; no new
holdout seeds are generated or consumed by this software wave.

## 目录

```
workspace/kaggriculture/software/
├── kaggle_simulations/agent/main.py   可提交 bot（官方 kit 结构，自包含 stdlib-only；
│                                      上传：kaggle competitions submit kaggriculture -f main.py）
├── kgenv/                             本地评估包
│   ├── engine.py                      官方引擎单局对局器（结构化结果/每日资金曲线）
│   ├── gym_env.py                     gym 风格单智能体封装（可插拔对手策略）
│   ├── economy.py                     收益模型（价格曲线/作物周期/动物产出/雇佣/地价）
│   ├── redlines.py                    机制红线检查表（浇水/喂养/产出上限/shed/期限）
│   ├── elo.py                         Elo 评级（只按胜负平，对齐官方天梯语义）
│   ├── bradley_terry.py               顺序无关 BT/Davidson 批拟合、seed bootstrap CI
│   ├── arena.py                       对局编排 + 复盘日志 + 提交 bot 加载
│   ├── regression.py                  冻结回归线断言（--assert-regression 的纯逻辑核心；
│   │                                  m1 起只在冻结池子流上断言，强对手不改变冻结线）
│   ├── variance.py                    种子方差统计（Wilson 胜率区间 / t 分数资金差区间）
│   ├── replay_profile.py              回放画像提取器（纯函数：资金曲线/畜群轨迹/作物轮替/
│   │                                  雇佣强度/外购饲料/卖出价格分布/终局抛售构成）
│   └── bots/                          baseline_wheat / greedy_carrot / cow_baron /
│                                       melon_hoarder / expansionist /
│                                       online_pool.py：crop_rotator(榜首式) /
│                                       template_wheat(rank6-28模板式) /
│                                       self_feed_ranch(Milan式) /
│                                       near_band_diversified(近段带, exploratory) /
│                                       LLM provider（默认关）
├── scripts/run_eval.py                全池 matchup 矩阵 + Elo + 方差报告 + 确定性探针 +
│                                       exports 产出（schema v1.1）+ 回归门旗标
├── scripts/h2h_external_probe.py      外部黑盒 H2H 正式契约生成（development-only）
├── scripts/check_external_h2h.py      外部 H2H verify-only 结构/语义/SHA/闭包校验
├── scripts/fit_bradley_terry.py      BT/Davidson 描述性评级与 clustered bootstrap CI
├── scripts/check_opponent_strength.py 强度门：新对手对冻结弱池 >=50% 胜率断言
├── scripts/analyze_failure_modes.py   失败模式探针（多种子深记录 + 证据报告生成）
├── scripts/corpus_fetch.py            回放语料抓取通道（HTTP range 探针/日分片选局/下载/
│                                       manifest 登记；只读网络，<=2 分片 & ~3GB 预算守卫）
├── scripts/corpus_build.py            m1 画像档案构建（完整性门 -> 逐局画像 -> 分层汇总 MD）
├── scripts/corpus_integrity.py        语料完整性校验（official 严格 / dev 宽松）
├── smoke_boot.py                      冒烟自检（验收命令）
├── tests/                             pytest：收益模型/红线/agent 契约/对局器/回归门/
│                                       新对手单测/方差统计
├── exports/
│   ├── schema.json                    软件->文档接口契约（1.1 历史只读兼容；2.0 正式语义）
│   ├── holdout_schema.json            一次性 holdout 证据 schema 2.0（attempt 1/2/3 尺寸自适应）
│   ├── external_h2h_schema.json        外部黑盒 H2H 证据 schema（非 promotion/holdout）
│   ├── external/                       用户生成的外部 H2H 与评级报告建议位置
│   ├── eval_results.json              仅正式门通过后原子发布的评估证据（当前 =
│   │                                  exports/holdout/published/ attempt-5 投影）
│   ├── eval_results.dev.json          quick/dev 隔离产物，不可作为正式证据
│   ├── holdout/                       attempt-1/ + attempt-2/ + attempt-3/（冻结档案）
│   │                                  + published/（attempt-5 权威代：export/replay/
│   │                                  seed_manifest/software_metrics 四件套）
│   │                                  + 公开 seed_manifest.json 投影
│   ├── eval_audit.md(+summary.json)   评估保真度审计清单（ABE-Ralph 式，逐项 pass/warn）
│   ├── failure_modes.md(+summary)     失败模式清单（FM-1..4，含证据局号）
│   ├── failure_probe_report.md        失败探针自动证据层（分差曲线/价格轨迹）
│   ├── replay_profiles/               m1 回放画像档案（profiles/*.json + index.json +
│   │                                  exclusions.json + band_summary.md；不放原始回放）
│   └── logs/                          replay_log.jsonl / failure_probe_log.jsonl
│                                       （每局一行的对局记录 + 每日资金 + 共享市场价格）
├── metrics.json                       实测指标分片（只写实测值，禁编造）
├── requirements.txt                   锁定依赖（含 vendor wheel，需从仓库根安装）
└── vendor/                            官方引擎 nodeps 重打包 wheel + 出处说明
```

## 对手池（m1-vertical 波次 2 强化后）

| bot | 风格一句话 | solo 终局资金(vs pass, seed 101) |
|---|---|---|
| cow_baron | 奶牛男爵：6 牛近栏每日喂养+照护（照护银行化 3 奶/2 天），小麦自给饲料，牛奶 130 闸门分批放货 | 48962 |
| melon_hoarder | 囤瓜波段：12+12 双波西瓜、无动物，190 高闸门囤货-放货节奏 | 36751 |
| expansionist | 扩张流：全四象限买地 + 7-8 雇工的工业化小麦庄园 + 6 鹅肥料院（自施肥 6 单/块） | 22007 |
| baseline_wheat / greedy_carrot / starter / random / pass | 第一轮冻结弱池（Elo 1245.8 以下） | 10506 / 6704 / … |

强度认证：三新对手对冻结弱池 3 种子全胜（`check_opponent_strength.py --rounds 3`，9/9 each）；
对 submission 的威胁见 `exports/failure_modes.md`（cow_baron 7/8、melon_hoarder 8/8 胜 submission——
第一轮"24/24 全胜"的弱池假象已被打破，失败模式成为 m2 迭代的输入）。

## Bot 策略（kaggle_simulations/agent/main.py，m2-full 波次 3 起）

"奶牛引擎 + 显式市场门控"（全部机制来自官方 How-to-Play/engine 源码；失败模式驱动的
重构，逐 FM 对策见 `exports/failure_modes.md` 顶部状态标注与 `exports/logs/iteration_gate_log.jsonl`）：

1. **奶牛引擎（FM-1 对策）**：shed 环形建 PASTURE 养牛（受照护奶牛 3 奶/2 天 = 1.5/天，
   单位经济碾压鹅的 2 蛋/天 × 50）；牛群按「现金闸门 + 每日 pace 上限」分期扩张至 10 头
   上限（NE 扩地后环形牛栏 + 18-22 块施肥小麦 = 劳动天花板内的最优规模，实测 8/10/12
   三档对比取 10）；奶价 <90（需求枯竭）自动冻结扩栏。
2. **小麦基座（FM-2/FM-3 对策）**：第 0-1 天先种满小麦再扩栏（饲料管线先行）；小麦 age-2
   自施肥（4 → 6 单位/块）；季中**零溢价作物敞口**——瓜双波全部移除，因为 MELON 无商铺
   消费 + 平方 glut 曲线可被任何对手战略性砸穿，而小麦 log 曲线 + 奶的城镇日常消费不可。
3. **选择性干预市场门控（蓝图选型 arxiv-2608.15291 方法论迁移，main.py `_market_gates`
   内逐条注释曲线依据）**：奶 HOARD(<105)/RELEASE(清仓式放行,峰值 145+ 加大)/压力护盘
   (shed≥70 排水防 100 格丢弃悬崖)/终局衰减闸；肥料 50 闸门 + 个位数库存上限（棚位让奶）；
   小麦 12 闸门日放盈余；第 29 天清仓一切——只计银行存款。
4. **劳动与后勤**：黎明 HIRE 突发雇佣（hand 每晨清零且只有 h≤2 可雇，单订单/回合会卡在
   3 人——实测修复）；多载具小麦分桶配送（单载具 24 回合喂不完 10+ 头牛环）；PLACE 优先级
   压过收割（未落位牛零产出且占棚位）；小麦 age≥5 腐烂抢救权重。
5. **可插拔 LLM 决策钩子（默认关闭）**：`LLM_PROVIDER=None`，A/B 基建侧专用。

### LLM 可插拔决策接口（默认关闭）

`kgenv/bots/llm_provider.py`：`NullProvider`（默认）/ `OpenAICompatProvider`
（读 `KG_LLM_PROVIDER` / `KG_LLM_BASE_URL` / `KG_LLM_API_KEY` / `KG_LLM_MODEL` 环境变量）。
带调用次数与时长预算闸（Reasonableness Standard 的机械化落地，参照 ProgRouter 成本路由与
Bayesian Self-Escalation 思路），任何失败超时都回退启发式决策，绝不阻塞回合。
main.py 中的 `LLM_PROVIDER=None` 钩子同样默认关闭——提交形态不依赖任何外部模型。
（规则依据：赛事 rules 允许外部模型，LLM 订阅级费用符合 Reasonableness Standard。）

## 实测结果摘要

**m0 复活会话（2026-08-28，弱池时代）**：40 局全长评估 107.36s；submission 24/24 全胜
（弱池+baseline），平均终局资金 30631.46；Elo submission 1460.9 > baseline_wheat 1245.8 >
greedy_carrot 1162.2；回归门 PASS（20 局 55.49s）。

**m1 波次 2（2026-08-28，对手池强化 + 失败模式证据）**：

- 全池矩阵（9 bot × 36 对 × 4 种子 + A/B + 探针 = 148 局 + 4 探针，346.94s），
  148/148 局恰好 720 回合；两次同配置独立运行 Elo 表完全一致（仅涉 random 对手的奖励漂移）
- Elo（k=32）：cow_baron 1460.3 > **submission 1422.8** > melon_hoarder 1391.3 >
  expansionist 1289.6 > baseline_wheat 1170.6 > greedy_carrot 1155.8 > starter 1058.3 >
  pass 991.5 > random 859.7；池最高 Elo 1162.2 → **1460.3**
- submission 对池：对 cow_baron **0/4**（均差 -17772）、对 melon_hoarder **0/4**（-5410）——
  第一轮"全胜"被强池打破；对 expansionist 4/4（+10014）、对弱池与 baseline 全胜
- 失败探针（种子 201-208 × 8 对手 = 64 局）：submission 49W-15L；失败模式 4 条
  （`exports/failure_modes.md`：奶牛引擎经济压制 / 二波瓜重植被锁死 / 开局爬坡被压制 /
  共享肥料贬值）
- 方差报告：最不稳对局 baseline_wheat vs greedy_carrot（0.75，CI95 [0.30,0.95]，跨种子
  翻转）；submission 相关对局无翻转
- 评估审计：**8 pass / 3 warn / 0 fail**（`exports/eval_audit.md`）
- 回归门：PASS（74 局 196.17s，冻结子流上断言；含一次数据驱动的冻结序修订
  random/pass 对调，见 `kgenv/regression.py` docstring 与审计第 6 项）
- 测试：**84 passed**（新增新对手单测 / 方差统计 / 冻结池门语义 / 复盘价格日志）
- 复现性：确定性对手同配对同种子奖励逐位一致；引擎 `random` 对手奖励漂移（未被子完全
  钉死，已声明边界）

**m2 波次 3（2026-08-28，失败模式驱动的策略重构）**：

- submission 换引擎：鹅+瓜 → **奶牛+施肥小麦+显式市场门控**；16 条迭代门记录
  （`exports/logs/iteration_gate_log.jsonl`），每轮候选改动先过头对头门再合入
- 全池矩阵（148 局，363.11s）：**submission Elo 1500.8 全池第一**（W36-0L），cow_baron
  1419.6 第二；m1 时 submission 1422.8 居第二
- 对 m1 两大苦主：**cow_baron 10W-2L**（矩阵 4-0 + 探针 6-2，均差 +3996；m1 为 1-7）、
  **melon_hoarder 11W-1L**（+21091；m1 为 0-8）；探针总战绩 53W-3L（m1 为 49W-15L）
- 残留负局：cow_baron 种子 204/206（城镇零奶类商铺的需求枯竭局，奶价 9-40 双方地板）、
  melon_hoarder 种子 208（-1413）——均为市场随机性，非对手可针对行为
- 回归门 PASS（m2 复跑，冻结线未动）；测试 **101 passed**（新增 17 条策略单测）；
  smoke_boot PASS（3.7s）
- LLM A/B harness 就绪（`scripts/run_llm_ab.py` 一条命令）；本环境无 KG_LLM_* key，
  NullProvider 通路自检实测（4 局 / 1294 次咨询全部回退启发式 / 0 预算阻断），
  `llm_ab_win_rate` 如实置 null 待 key

**m4 holdout v2（2026-08-29，一次性独立 holdout，候选 5713c17e）**：

- attempt-2 `b75258615f75baf54275ff54`：9 agent 全池 C(9,2)=36 对 × 8 新种子 × AB/BA = **576 局**
  （2250.71s），零异常局；种子 `secrets` 生成，与全部 38 个历史种子交集 0，运行后公开
  （`exports/holdout/seed_manifest.json`）；候选哈希运行前/后与冻结值全等
- **候选 128 局 108W-20L-0T（score_rate 0.84375，Wilson95 [0.771, 0.8965]）**；顺序无关
  成对统计（64 个 (对手,种子) AB/BA 单元，t 95% CI）estimate 0.84375，CI [0.7551, 0.9324]
- 逐对：cow_baron / melon_hoarder / expansionist / baseline_wheat 各 **16-0**；
  crop_rotator 12-4、template_wheat 10-6、self_feed_ranch 14-2、near_band_diversified 8-8
  ——20 负全部来自 m2 线上风格对手，旧池零负；与开发门 57-7-0 的偏差集中在波 3 遗留风险
  （near_band 8 负 / template_wheat 6 负 / crop_rotator 4 负），self_feed 反而由 5-3 改善到 14-2
- 座位分层：AB 55-9 / BA 53-11（两层 score_rate 0.859/0.828）；Elo 附录（描述性、顺序敏感）：
  template_wheat 1535.1 全池第一，submission 1349.0 第五
- 数字全部来自 metrics 键 `m4_*`（16 键，见 `workspace/kaggriculture/metrics.json`）；战役 II attempt-1 的
  92.9% 结论保留在历史键 `holdout_*`/`confirmatory_*` 与 `exports/holdout/attempt-1/` 冻结档案，
  二者分属不同候选（7c482921 vs 5713c17e），互不外推

**r3-3 r4 holdout（2026-08-29，一次性独立 holdout，候选 9298751f，git_ref 1644397）**：

- attempt-3 `14ffd5eb33785ae8af94cf73`：10 agent 全池（9 对手含 scale_ranch）C(10,2)=45 对
  × 8 新种子 × AB/BA = **720 局**（2179.8s），零异常局、360/360 座位均衡、0 缺镜像；
  种子 `secrets` 生成，与全部 **46** 个历史种子（27 开发/回归 + 8 attempt-1 + 3 线上
  + 8 attempt-2 已公布）交集 0，运行后立即公开（`exports/holdout/seed_manifest.json`）；
  候选哈希运行前/后与冻结值全等，评估器闭包（含 vendored 引擎 wheel）运行前后不变
- **候选 144 局 142W-2L-0T（score_rate 0.986111，Wilson95 [0.9508, 0.9962]）**；顺序无关
  成对统计（72 个 (对手,种子) AB/BA 单元，t 95% CI）estimate 0.986111，CI [0.966628, 1.0]
- 逐对：melon_hoarder / expansionist / baseline_wheat / crop_rotator / template_wheat /
  self_feed_ranch / **scale_ranch（新增）** 各 **16-0**；cow_baron 15-1、
  near_band_diversified 15-1 ——2 负均为 AB 座（候选先手），分差悬殊（-24494 / -45813）
- 座位分层：AB 70-2（0.9722）/ BA 72-0（1.0）；Elo 附录（描述性、顺序敏感）：
  submission 1701.6 全池第一，near_band_diversified 1506.7 第二
- attempt-2（m4，84.4%）权威代已字节不变归档于 `exports/holdout/attempt-2/`；
  数字全部来自 metrics 键 `r4_holdout_*`/`r4_confirmatory_*`（16 键）；三代证据
  （7c482921 / 5713c17e / 9298751f）互不外推

## 已知边界

- 当前 v10.3 working candidate 未做新的 Kaggle 线上提交，且 `holdout_status=not_run`；历史线上提交与 21 局 round-7 观测属于 v10.2，详见 `exports/online/round7_ledger.json` 和 metrics 中的历史记录。
- 引擎为官方 1.32.7；若 Kaggle 线上 kit 升级机制，需以官方页面直抓为准复核。
- 对手池在 m1 波次 2 已强化（最强 Elo 见 metrics `opponent_pool_max_elo`），但强对手与
  submission 同属启发式家族，存在"同族变体过拟合"风险（eval_audit.md 第 7 项 warn）；天梯
  真实对手分布仍需线上反馈校准。
- 引擎 `random` 对手的奖励未被子完全钉死（种子外熵源），跨会话漂移；矩阵中涉 random 的
  对局奖励可能逐会话漂移，胜负判定与 Elo 序在本池强度差下稳定（eval_audit.md 第 1 项）。
- 矩阵每对只打单座位（p0 视角 × N 种子），未做座位对换；引擎市场为逐单 lockstep，座位
  不对称性预计可忽略（eval_audit.md 第 8 项 warn）。
