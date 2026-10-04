## 最新状态：第八轮已完成（2026-09-23）

用户恢复工作后，剩余258局已全部补完；三策略各480确认局均有效。最终选择市场融合v8：385胜95负，积分80.21%，相对v7提高14.79个百分点，三比较校正区间7.08～21.88个百分点。DSM修复确认54.17%，未通过选版门槛。已准备本地正式包 submissions/release_v8/submission.tar.gz，根main.py已同步，原v7保留，尚未上传Kaggle。

请以 RELEASE_V8.md、RESEARCH_ROUND8.md末尾及submissions/release_v8/release_manifest.json为准。确认集已用于最终选择，不再是未见数据；40个reserve世界尚未使用。本轮2496局有效完整比赛，另240条入口异常保留。后续需根据线上反馈决定新一轮，不必再续跑下方历史暂停任务。

---

以下为保留的历史交接记录：

# 下次从这里继续：第八轮暂停交接

**最新用户指令（2026-09-22 18:01，Asia/Shanghai）：额度即将用完，开始记录。当前已暂停，整体估计85%。** 此状态覆盖较早的“继续工作”记录。所有本轮模拟进程已停止，JSONL已保存，根main.py仍为v7，没有线上提交或发布v8。

## 下次第一步

先读本文件、`research/round8/CURRENT_STATE.md`、`research/round8/PROTOCOL.md`。保留所有冻结候选及旧失败记录，不重新调参或重跑已经完成的任务。项目目录：`C:/Users/ASUS/Documents/ChatGPT/kaggriculture`，Python使用`.venv/Scripts/python.exe`，官方引擎1.32.7。

## 现在完成到了哪里

| 面板 | 完成且有效 | 总计划 | 待完成 |
|---|---:|---:|---:|
| v7 独立确认 | 480 | 480 | 0 |
| 市场融合候选 独立确认 | 480 | 480 | 0 |
| DSM修复候选 独立确认 | 222 | 480 | **258** |

**以上确认集强度成绩尚未向模型展开读取**，只核对过数量、有效性、耗时。两个候选在读取确认成绩前已冻结；240开发局完成后，DSM修复75.0%积分，市场融合70.4167%，按事先协议两者都进入确认。最终谁更强尚未判断，不能提前称某个包为最终版。

## 续跑与最终验收顺序

1. 在项目根目录运行 `./resume_round8_confirmation.ps1`，只补齐剩余258局；JSONL以任务ID续跑，manifest锁定源码/对手/地图。6个worker已在本机运行过，可用内存约2.5GB；不要同时开额外大池。
2. 新面板达到480有效后，运行 `.venv/Scripts/python.exe assess_round8.py --phase confirmation`。它先验证两个开发面板完整，确认精确40世界×6冻结对手×2席，再报告主候选-v7、DSM修复-v7、DSM修复-主候选三比较，Bonferroni校正区间控制选择偏差。
3. 只有评估存在`selected`且技术验收通过，运行 `.venv/Scripts/python.exe publish_round8_selection.py`。它复制已经测过的归档字节至release_v8、更新根入口与构建脚本，保留v7。旧`finalize_round8.py`主入口已禁用，勿恢复绕过新协议。
4. 更新`RESEARCH_ROUND8.md`末尾的独立确认结果与本交接状态，核查RELEASE_V8.md、release_manifest.json、selection.json、根main及归档hash。最终回复给提交包和研究报告链接，说明真实线上分数仍待Kaggle充分匹配。没有授权购买算力或联系其他参赛者。
5. 若没有候选达到独立门槛，不强行发布为已验证升级。后续改动不得继续把已读确认集当未见数据，使用尚未使用的40个reserve世界。

## 两份候选均已通过技术验收

- 市场融合：`experiments/round8_bounded_production.py`，SHA `9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e`。待选归档`submissions/candidate_v8/submission.tar.gz`，SHA `017b3ee7a82943f378f0bb455a575dca796558c557bd823bcde039715daf3977`。
- DSM现金修复：`experiments/round8_top2_dsm_contract_entry.py`，SHA `23768116945ebd7500b2e2298616ff6dd974d27ce2c839643cc7d3e3d4cada57`。待选归档`submissions/candidate_v8_dsm/submission.tar.gz`，SHA `92bf3540b8b03439127081507ab9248c3fa8ee5d6e0c2d3ec51d045752194ec0`。
- 每份均做两场官方文件路径完整运行、标准库隔离连续1438动作、原始/排序JSON键、跨局状态重置。具体证据在各自validation.json，不需要无故重做。
- 根main与已发布v7 SHA仍应为`273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197`。

## 必须保留的发现与限制

- DSM与Vadim各24公开研究回放，另各5封存，48原局官方精确复现。没有取得两位私有源码；不能称重构代理为作者算法，不能以本地胜负宣称战胜真实榜首。
- DSM现金修复解决卖奶排在雇工之后的问题，三个诊断败局改善约3.9–4.3万金币；开发总体171胜51负18平。它仍有种子短缺等经济限制。
- 旧7735候选官方入口错误，240次启动报错、0完整局。新237681仅补唯一末尾入口，719动作逐个等价。失败记录不删除、不计为240完整比赛。
- 提前草莓种子反事实会挤占麦与后续取料，已拒绝直接加入；详见`top2/SEED_TIMING_FINDINGS.md`。
- 库存投影与混合买单的两个边界已确认；24条路线17,256步审查未发现实际新增损害，保留限制。详见`top2/CONTRACT_REVIEW.md`。
- 番茄19株只在已知开发图证实，240随机开发与80前缀检查未触发；不要夸大成主要收益。
- 来源、公开检索覆盖、消融失败、独立审查都已经写入RESEARCH_ROUND8.md、SOURCES_REGISTRY.md及research/round8/。

## 保存内容

工作文件均保留原位；`checkpoints/round8_20260922_paused.zip`是本次暂停快照，包含源码、研究材料、完整与部分对抗记录、两候选归档及交接说明。ZIP内有逐文件SHA清单。更早的before_final_selection.zip不含当时还在运行的DSM确认记录，续接优先使用paused版本。

不要从候选包名称推断它已被选中。下次继续的关键只有：补258局 → 按冻结协议评估 → 通过才发布。
