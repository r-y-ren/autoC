# Kaggriculture 提交 SOP v4

> 适用对象: 战役 III m3 冻结候选（rotation-ranch）与 round-2 人工线上提交。
> 责任: Kaggle 账号操作、Validation Episode 复核、线上反馈记录、止损裁决和终交锁定均由队伍人工执行; AI 不代操作账号、不代签。
> 证据纪律: 战役 II 与战役 III 两个已发布 holdout 均只允许 verify; 禁止重跑、重抽、重放后择优、替换或覆盖。
> 常量声明: 本手册中的额度与阈值（每日提交 ≤5 次、每候选 ≤2 次/日、每轮回拉 ≥3 局、公共局累计 ≥6 局且胜率低于 50%、09-30 终交）是蓝图契约常量, 不是实测数字。
> 身份声明: 第 0 节的哈希为提交前检查门的权威值, 全部来自 `workspace/metrics.json` 对应键（键名见各节）, 不从旧报告或终端历史抄值。

## 0. 权威身份与正式产物

当前冻结候选必须同时满足以下精确身份:

- candidate: `workspace/software/kaggle_simulations/agent/main.py`
- candidate SHA-256: `5713c17eadf1d026d2ccfbc2361bf65f457e8d11843053c74fe4ec261a7a37ee`
- frozen git ref: `b47bc16f426fbfeeab645e86a5b4453d45b5779a`
- frozen manifest: `workspace/software/m3_frozen_manifest.json`
- manifest SHA-256: `67e08238e44b7c76a262f34baea27fe6c721bfb545cacb0fe239a6c76a6d3b2a`
- 快照: `workspace/software/m3_frozen_candidate.b64`（快照文件 SHA-256 `7ac70b002c1fa472f5325347c0a5707780ca6708c82c6679555b389ebd180059`, 解码后 SHA-256 与 candidate SHA-256 一致）
- formal export: `workspace/software/exports/eval_results.json`
- formal export SHA-256: `a87bc26e285722b14d85b5012b3da87b142a7e9b8680527fc0ecb0ea44de0404`
- validated schema: `2.0`
- metrics 来源键: `metrics.software.m3_frozen_candidate_identity`, `metrics.software.m4_confirmatory_export_traceability`

历史身份（仅审计, 不得为当前候选背书）: 战役 II 冻结候选 SHA-256 `7c482921857562e6b7cd58a3ac4bde358981c180cc233ad3913948e5fcafa66a` 与其 export（SHA-256 前缀 `ac7684d8`）整段降级为历史记录; 其 holdout 结论受固定对手池分布偏移、不外推新候选限制约束。

- [ ] **V4-01** 从 `workspace/metrics.json` 读取上述身份（`m3_frozen_candidate_identity` 与 `m4_confirmatory_export_traceability`）, 不从旧报告、终端历史或聊天记录抄值。
- [ ] **V4-02** 计算候选 SHA-256, 必须与精确值一致:

```bash
sha256sum workspace/software/kaggle_simulations/agent/main.py
```

- [ ] **V4-03** 计算正式 export SHA-256, 必须与精确值一致:

```bash
sha256sum workspace/software/exports/eval_results.json
```

- [ ] **V4-04** 任一 SHA 不一致立即停止; 不得用重新运行 holdout 的方式"修复"不一致。
- [ ] **V4-05** 候选文件必须是冻结身份对应的文件本体, 且不是工作区中另一个同名副本或未冻结的修改版。

## 1. 已发布 holdout 保护门（两代 holdout 均适用）

当前正式证据是两个已发布、未失效的一次性 attempt: 战役 II attempt（index 1, 前代候选）与战役 III attempt（index 2, m4 holdout v2, 绑定第 0 节身份）。两代种子均已公开, 只可用于重现性检查, 不可再声称为新独立确认。

- [ ] **V4-06** 禁止运行任何会创建新 attempt、继续比赛、重新抽种子或覆盖正式 export 的 holdout 命令。
- [ ] **V4-07** 禁止依据已公开结果修改策略后, 再用同一批种子复测并替换当前结论。
- [ ] **V4-08** 禁止重抽多批种子后择优发布, 也禁止把失败 attempt 删除后重来（m4 的 attempt-1 证据目录按原样保留）。
- [ ] **V4-09** 仅运行 verify-only 检查, 该命令不得启动新对局:

```bash
python workspace/software/scripts/run_holdout.py --verify-published --require-frozen
```

- [ ] **V4-10** verify-only 结果必须确认: candidate hash 匹配、published=true、invalidated=false、完整矩阵、AB/BA 对称、零异常、一次性状态未被改变。

## 2. 正式 export 检查

- [ ] **V4-11** 执行正式 schema、语义与跨字段验证:

```bash
python workspace/software/scripts/check_eval_contract.py --mode official --input workspace/software/exports/eval_results.json
```

- [ ] **V4-12** 检查结果必须为通过; 任一 schema、candidate identity、seed domain、expected/actual、AB/BA、异常状态或统计一致性错误都应中止提交。
- [ ] **V4-13** 核对 `workspace/metrics.json` 中 `m4_confirmatory_export_traceability` 的 `export_sha256`、`validated_schema` 和 JSON Pointer 映射均指向当前正式 export。
- [ ] **V4-14** 不运行 `merge_metrics.py` 来掩盖正式 export 错误; 只有 software 责任角色确认权威分片后才能重新汇总。

## 3. 提交前候选检查

- [ ] **V4-15** 确认提交文件仍为第 0 节精确 SHA 的冻结候选。
- [ ] **V4-16** 运行不改变候选和正式证据的冒烟与测试:

```bash
python workspace/software/smoke_boot.py
python -m pytest workspace/software/tests -q
```

- [ ] **V4-17** 冒烟或测试失败立即停止; 不得借用旧 holdout 结果为已变化或失败的候选背书。
- [ ] **V4-18** 确认提交形态 stdlib-only、离线自主运行, 不依赖外部 LLM、网络 API 或未申报文件。
- [ ] **V4-19** 确认对手池与门禁必测名单为 m2 更新后的 8 对手版本（`metrics.software.m2_gate_required_opponents`: cow_baron、melon_hoarder、expansionist、baseline_wheat、crop_rotator、template_wheat、self_feed_ranch、near_band_diversified）, 缺失必测对手的赛程会被契约检查拒绝。
- [ ] **V4-20** 在提交台账记录 candidate SHA、git ref、formal export SHA、检查时间、操作人和验证结果。

## 4. 人工线上提交与 round-2 天梯采样协议

round-2 采样是预算内的信息采集, 不是对本地 holdout 的线上重放; 每一次提交都要消耗额度, 额度台账先于提交存在。

- [ ] **V4-21** 提交前确认账号已报名且团队/账号使用符合竞赛规则。
- [ ] **V4-22** 将候选提交至 Kaggle; AI 不代操作账号。
- [ ] **V4-23** 提交前核对当日计数: 每日提交至多 5 次（`<=5/day`）。
- [ ] **V4-24** 提交前核对该候选当日计数: 每候选至多 2 次/日（`<=2/candidate/day`）。
- [ ] **V4-25** 每次提交前确认它会如何影响"最近 2 次提交"; 新提交不得无意覆盖应保留版本。
- [ ] **V4-26** Validation Episode 返回 Error 即停当日提交并上报, 不得以连续重试掩盖错误; 排查产生的新策略版本按第 6 节新候选规则处理。
- [ ] **V4-27** 在 Submissions 页面确认 Validation Episode 状态, 并把状态、提交时间和线上返回信息记入台账; 台账逐次记录提交序号、candidate SHA、Validation 状态与是否保留, 对接 `metrics.software.unmeasured.online_feedback_calibration` 的 `round2_sampling_ledger` 子字段（round-2 发生前保持 null）。

## 5. 竞赛运行约束

以下是提交操作约束, 不是本 SOP 已执行声明:

- [ ] **V4-28** 额度台账（每日总量、每候选当日量）在任何一次提交动作之前更新, 而不是事后补记。
- [ ] **V4-29** 台账与赛站记录对不上时, 以赛站为准并停止当日后续提交直至澄清。
- [ ] **V4-30** 终交前由人工逐条确认最近 2 次提交都是拟保留版本, 且两条 Validation Episode 状态符合要求。
- [ ] **V4-31** 未看到赛站记录前, 不得把任何一项标记为已执行。

## 6. 回拉与复盘循环（round-2 核心）

线上反馈是新证据, 不是对当前已发布 holdout 的回填或修订。每一轮提交都以"回拉-复盘"闭环。

- [ ] **V4-32** 每次提交后回拉不少于 3 局公共天梯回放完成复盘（episode 级清单入台账, 对接 `round2_pullback_reviews` 子字段; 排除 EPISODE_TYPE_VALIDATION 自博弈）。
- [ ] **V4-33** 原样记录线上反馈: 提交 ID、candidate SHA、时间、Validation 状态、平台返回值和可观察对局现象。
- [ ] **V4-34** 复盘产出三件套: 失败模式台账更新（延续 FM-O 编号族）、画像档案滚动更新（携带来源 URL 与抓取日期）、是否触发新候选的判定。
- [ ] **V4-35** 跨局复核纪律: 同选手不少于 3 局一致才可更新对手池参数; 单局结论一律标 exploratory。
- [ ] **V4-36** 复盘产生的任何策略或代码变化都构成新候选: 为其计算新 SHA、建立新冻结记录, 走 m3 开发门与 m4 holdout 流程（新独立确认种子, 不得复用任何已公布种子）, 当前 holdout 结论不得迁移到新候选。
- [ ] **V4-37** `online_ladder_games`、`online_skill_rating`、`online_feedback_calibration` 只在真实线上证据存在后由责任角色写入; 未发生时保持 null, 不用本地 holdout 推导、代填或解释为线上指标。

## 7. 止损线与转备选

- [ ] **V4-38** 触发条件: 新候选线上公共局累计不少于 6 局（`>=6` 公共局）且胜率低于 50%（`<50%`; 阈值为蓝图契约常量）。
- [ ] **V4-39** 触发动作: 停止本方向调参; 转备选方向接力; 判定与动作记录入 `stop_loss_status` 子字段并上报队伍。
- [ ] **V4-40** 边界声明: 止损是资源分配决策, 不得写成对线上实力、名次或获奖的结论。

## 8. 终交锁定

- [ ] **V4-41** 09-30 前人工核对最近 2 次提交的提交 ID、candidate SHA、git ref 与 Validation Episode 状态。
- [ ] **V4-42** 将最终保留的 2 个 commit/hash 交由责任角色回填 `metrics.software.unmeasured.final_submission_commits`; 回填前保持 null。
- [ ] **V4-43** 操作人、复核人和日期在台账签字; AI 不代签。
- [ ] **V4-44** 锁定后不再进行实验性提交; 若确需变化, 重新执行新候选流程并重新评估"最近 2 次"约束。

## 9. 停止条件

出现以下任一情况立即停止提交流程并上报:

- candidate SHA 或 formal export SHA 与第 0 节不一致;
- verify-only 检查试图启动新对局或改变任一代 attempt 状态;
- schema、语义、跨字段、完整矩阵、AB/BA 或异常检查失败;
- 策略已变化但仍试图引用任一代旧 holdout/旧确认;
- Validation Episode 返回 Error 后仍被要求继续提交, 或当日额度/最近 2 次状态无法确认;
- 止损线已触发但未执行转备选动作;
- 线上结果尚未产生却要求填写非 null 线上指标;
- 台账与赛站记录不一致且无法当场澄清。

## 与 metrics 键的对接

| SOP 环节 | 键位 |
|---|---|
| 0 身份 | `m3_frozen_candidate_identity`, `m4_confirmatory_export_traceability` |
| 1-2 holdout/export 保护 | `m4_holdout_run_status`, `m4_holdout_integrity_pass` |
| 3 提交前检查 | `m2_gate_required_opponents`, `m2_opponent_pool_certification`, smoke/测试键 |
| 4 采样额度台账 | `unmeasured.online_feedback_calibration.round2_sampling_ledger` |
| 6 回拉复盘 | `unmeasured.online_feedback_calibration.round2_pullback_reviews` |
| 7 止损 | `unmeasured.online_feedback_calibration.stop_loss_status` |
| 8 终交 | `unmeasured.final_submission_commits`, `unmeasured.online_skill_rating` |

## 成稿自检

- 节数: 10（0-9; v3 的 8 节 + 新增第 6 节回拉与复盘循环、第 7 节止损线与转备选）。
- 检查项编号: V4-01..V4-44 连续无跳号。
- 权威身份切换: 战役 II 身份（前缀 7c482921）降级为历史记录, 当前门为战役 III 候选（前缀 5713c17e）与 m4 export（前缀 a87bc26e）。
- 一切额度与阈值为蓝图契约常量; 一切线上数值待人工执行后经 unmeasured 键回填, 本手册不预填。
