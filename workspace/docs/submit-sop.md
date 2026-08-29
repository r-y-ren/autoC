# Kaggriculture 提交 SOP v3

> 适用对象: m3-redocument 冻结候选与后续人工线上提交。
> 责任: Kaggle 账号操作、Validation Episode 复核、线上反馈记录和终交锁定均由队伍人工执行。
> 证据纪律: 当前已发布 holdout 只允许 verify; 禁止重跑、重抽、重放后择优、替换或覆盖。

## 0. 权威身份与正式产物

当前冻结候选必须同时满足以下精确身份:

- candidate: `workspace/software/kaggle_simulations/agent/main.py`
- candidate SHA-256: `7c482921857562e6b7cd58a3ac4bde358981c180cc233ad3913948e5fcafa66a`
- frozen git ref: `decff3b236fd4cddd8bd6c5fbb1c1226f529a195`
- formal export: `workspace/software/exports/eval_results.json`
- formal export SHA-256: `ac7684d853e368a26bf8685d6649d3d4d711a13a9eaacdadb6ff89c7aa5504f7`
- validated schema: `2.0`
- metrics 来源键: `metrics.software.frozen_candidate_identity`, `metrics.software.confirmatory_export_traceability`

- [ ] **V3-01** 从 `workspace/metrics.json` 读取上述身份, 不从旧报告、终端历史或聊天记录抄值。
- [ ] **V3-02** 计算候选 SHA-256, 必须与精确值一致:

```bash
sha256sum workspace/software/kaggle_simulations/agent/main.py
```

- [ ] **V3-03** 计算正式 export SHA-256, 必须与精确值一致:

```bash
sha256sum workspace/software/exports/eval_results.json
```

- [ ] **V3-04** 任一 SHA 不一致立即停止; 不得用重新运行 holdout 的方式“修复”不一致。

## 1. 已发布 holdout 保护门

当前正式证据是一个已发布、未失效的一次性 attempt。种子已经公开, 因而只可用于重现性检查, 不可再声称为新独立确认。

- [ ] **V3-05** 禁止运行任何会创建新 attempt、继续比赛、重新抽种子或覆盖正式 export 的 holdout 命令。
- [ ] **V3-06** 禁止依据已公开结果修改策略后, 再用同一批种子复测并替换当前结论。
- [ ] **V3-07** 禁止重抽多批种子后择优发布, 也禁止把失败 attempt 删除后重来。
- [ ] **V3-08** 仅运行 verify-only 检查, 该命令不得启动新对局:

```bash
python workspace/software/scripts/run_holdout.py --verify-published --require-frozen
```

- [ ] **V3-09** verify-only 结果必须确认: candidate hash 匹配、published=true、invalidated=false、完整矩阵、AB/BA 对称、零异常、一次性状态未被改变。

## 2. 正式 export 检查

- [ ] **V3-10** 执行正式 schema、语义与跨字段验证:

```bash
python workspace/software/scripts/check_eval_contract.py --mode official --input workspace/software/exports/eval_results.json
```

- [ ] **V3-11** 检查结果必须为通过; 任一 schema、candidate identity、seed domain、expected/actual、AB/BA、异常状态或统计一致性错误都应中止提交。
- [ ] **V3-12** 核对 `workspace/metrics.json` 中 `confirmatory_export_traceability` 的 `export_sha256`, `validated_schema` 和 JSON Pointer 映射均指向当前正式 export。
- [ ] **V3-13** 不运行 `merge_metrics.py` 来掩盖正式 export 错误; 只有 software 责任角色确认权威分片后才能重新汇总。

## 3. 提交前候选检查

- [ ] **V3-14** 确认提交文件仍为第 0 节精确 SHA 的冻结候选, 且不是工作区中另一个同名副本。
- [ ] **V3-15** 运行不改变候选和正式证据的冒烟与测试:

```bash
python workspace/software/smoke_boot.py
python -m pytest workspace/software/tests -q
```

- [ ] **V3-16** 冒烟或测试失败立即停止; 不得借用旧 holdout 结果为已变化或失败的候选背书。
- [ ] **V3-17** 确认提交形态 stdlib-only、离线自主运行, 不依赖外部 LLM、网络 API 或未申报文件。
- [ ] **V3-18** 在提交台账记录 candidate SHA、git ref、formal export SHA、检查时间、操作人和验证结果。

## 4. 人工线上提交

- [ ] **V3-19** 提交前确认账号已报名且团队/账号使用符合竞赛规则。
- [ ] **V3-20** 将候选提交至 Kaggle; AI 不代操作账号。
- [ ] **V3-21** 在 Submissions 页面确认 Validation Episode 状态, 并把状态、提交时间和线上返回信息记入台账。
- [ ] **V3-22** Validation Episode 失败时停止使用该提交作为候选证据; 排查产生的新策略版本按第 6 节处理。

## 5. 竞赛运行约束

以下是提交操作约束, 不是本 SOP 已执行声明:

- [ ] **V3-23** 提交前核对当日计数, 保持每日提交不超过 5 次(`<=5/day`)。
- [ ] **V3-24** 每次提交前确认它会如何影响“最近 2 次提交”; 新提交不得无意覆盖应保留版本。
- [ ] **V3-25** 台账逐次记录当日提交序号、candidate SHA、Validation Episode 和是否保留。
- [ ] **V3-26** 终交前由人工逐条确认最近 2 次提交都是拟保留版本, 且两条 Validation Episode 状态符合要求。
- [ ] **V3-27** 未看到赛站记录前, 不得把任何一项标记为已执行。

## 6. 线上反馈与新候选规则

线上反馈是新证据, 不是对当前已发布 holdout 的回填或修订。任何根据线上反馈形成的策略变化都会产生新候选。

- [ ] **V3-28** 原样记录线上反馈: 提交 ID、candidate SHA、时间、Validation 状态、平台返回值和可观察对局现象。
- [ ] **V3-29** `online_ladder_games`, `online_skill_rating`, `online_feedback_calibration` 只在真实线上证据存在后由责任角色写入; 未发生时保持 null。
- [ ] **V3-30** 不用本地 holdout 推导、代填或解释为线上指标。
- [ ] **V3-31** 若线上反馈触发任何策略或代码变化, 为新候选计算新 SHA、建立新冻结记录, 当前 holdout 结论不得迁移到新候选。
- [ ] **V3-32** 新候选需要新的、此前未公开且未用于开发的独立确认种子; 必须在候选冻结后生成, 且不得复用当前公开种子。
- [ ] **V3-33** 新确认仍须执行完整 AB/BA、异常 fail-closed、schema/语义校验与原子发布; 结果无论好坏都不得按表现重抽或替换。
- [ ] **V3-34** 只有新候选的新独立确认完成后, 才能更新面向该新候选的确认性报告; 历史 attempt 保留审计记录。

## 7. 终交锁定

- [ ] **V3-35** 人工核对最近 2 次提交的提交 ID、candidate SHA、git ref 与 Validation Episode 状态。
- [ ] **V3-36** 将最终保留的 2 个 commit/hash 交由责任角色回填 `metrics.software.unmeasured.final_submission_commits` 对应接口; 回填前保持 null。
- [ ] **V3-37** 操作人、复核人和日期在台账签字; AI 不代签。
- [ ] **V3-38** 锁定后不再进行实验性提交; 若确需变化, 重新执行新候选流程并重新评估“最近 2 次”约束。

## 停止条件

出现以下任一情况立即停止提交流程并上报:

- candidate SHA 或 formal export SHA 与第 0 节不一致;
- verify-only 检查试图启动新对局或改变 attempt 状态;
- schema、语义、跨字段、完整矩阵、AB/BA 或异常检查失败;
- 策略已变化但仍试图引用当前公开 holdout;
- 线上结果尚未产生却要求填写非 null 线上指标;
- 当日提交额度或最近 2 次提交状态无法确认。
