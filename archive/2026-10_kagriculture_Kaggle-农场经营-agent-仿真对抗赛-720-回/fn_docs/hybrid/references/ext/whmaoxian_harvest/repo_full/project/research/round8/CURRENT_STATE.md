## 最新状态：第八轮已完成（2026-09-23）

用户恢复工作后，剩余258局已全部补完；三策略各480确认局均有效。最终选择市场融合v8：385胜95负，积分80.21%，相对v7提高14.79个百分点，三比较校正区间7.08～21.88个百分点。DSM修复确认54.17%，未通过选版门槛。已准备本地正式包 submissions/release_v8/submission.tar.gz，根main.py已同步，原v7保留，尚未上传Kaggle。

请以 RELEASE_V8.md、RESEARCH_ROUND8.md末尾及submissions/release_v8/release_manifest.json为准。确认集已用于最终选择，不再是未见数据；40个reserve世界尚未使用。本轮2496局有效完整比赛，另240条入口异常保留。后续需根据线上反馈决定新一轮，不必再续跑下方历史暂停任务。

---

以下为保留的历史交接记录：

# 最新状态：用户要求暂停记录

2026-09-22 18:01 已停止所有本轮模拟。请优先读根 CONTINUE_ROUND8.md；以下较早运行状态已被覆盖。v7确认480/480，市场融合确认480/480，新DSM确认222/480（剩258），全部已完成记录有效。确认fitness仍未展开，候选均已通过技术验收，尚未选择或发布v8。续跑根 resume_round8_confirmation.ps1，然后 assess_round8.py，再在门槛通过时 publish_round8_selection.py。

# 第八轮续接入口（2026-09-22）

用户目标：继续多轮对抗，尽力冲3000–3200，重点观察DSM/Vadim。用户刚询问额度与进度；整体估算75%，短暂暂停保存后，用户明确要求继续，**当前授权为继续工作，直到用户叫停**。

所有代码与数据在 `C:/Users/ASUS/Documents/ChatGPT/kaggriculture`。不要改官方参考AGENTS.md、README.md，不要改镜像sources。`.venv/Scripts/python.exe`；官方环境1.32.7。没有进行线上提交。

## 最新续接补充

两套旧确认均480有效，仍未读取fitness。新237681开发240已完成，171胜51负18平，75.0%，超过主候选70.4167%，进入confirmation：`results/round8_dsm_contract_entry_confirmation.json`，6worker，240开发无运行错误。新技术包已通过，`submissions/candidate_v8_dsm/submission.tar.gz` SHA `92bf3540b8b03439127081507ab9248c3fa8ee5d6e0c2d3ec51d045752194ec0`。

最终请用 `assess_round8.py --phase confirmation`（只在新480完成后）及 `publish_round8_selection.py`；旧finalize_round8.main已禁用。两候选三比较做Bonferroni校正，协议及代码已独立审查。评估绑定精确种子、席位和对手hash；publisher保护根入口/构建脚本，复制验收归档原字节。后续更新以JSONL/实际进程为准。

## 关键状态

- 根 `main.py` 仍为v7，SHA `273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197`。原release_v7保留。
- 主候选 `experiments/round8_bounded_production.py` SHA `9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e`。入口`round8_production_fusion_agent`。
- 新挑战者 `experiments/round8_top2_dsm_contract_entry.py` SHA `23768116945ebd7500b2e2298616ff6dd974d27ce2c839643cc7d3e3d4cada57`。入口`round8_dsm_contract_agent`。
- **截至本文件写入，尚未读取任何confirmation强度结果**。只读过完成数量、有效性和时间。保持该隔离，先完成挑战者development再决定是否推进。
- 20开发世界、40确认世界、40reserve已冻结：`league_seeds.json`。两席与各对手同世界不能算独立样本。reserve未使用。

## 正在运行的面板与续跑

通用：`league_round8.py`以JSONL任务ID续跑，manifest锁住源码、对手和种子。JSON摘要可能落后于JSONL。勿删除失败记录，也勿对同一输出改源码/对手。

六对手依次：`submissions/release_v6/main.py submissions/release_v7/main.py external/orderbook.py external/round8/master2965/main.py experiments/round8_top2_dsm_strict.py external/round8/fieldcraft/main.py`。

1. 主候选confirmation：输出`results/round8_candidate_confirmation.json`，40世界480局。短暂停止时408已存；恢复后本文件写入前464有效。候选上述9fa。运行4worker。
2. v7 confirmation：输出`results/round8_v7_confirmation.json`，40世界480局，**已480有效**。与主候选配对。
3. 新237681 development：输出`results/round8_dsm_contract_entry_development20.json`，20世界240局，已启动3worker，尚未完成。完整结束前不下强度结论。

续跑参数：`.venv/Scripts/python.exe league_round8.py --candidate <上述候选路径> --opponents <上述六对手> --split <development或confirmation> --workers 4 --output <上述输出>`。输出重定向同名log以免提前暴露confirmation强度。

电脑16核32线程但仅16GB RAM。8个模拟worker曾使可用内存不足1GB，不要无限开池；新模型不要修改已冻结文件。

## 已有证据

主候选20开发世界240局：169胜71负，v7同面板123胜85负32平；积分提高12.5个百分点，按世界bootstrap95%为2.92–20.83个百分点。分对手见`RESEARCH_ROUND8.md`与`results/round8_combined_development_comparison.json`。对Master提升明显，对DSM严格代理仍11胜29负，与v7相同。

主候选技术归档 `submissions/candidate_v8/submission.tar.gz`，645772字节，SHA `017b3ee7a82943f378f0bb455a575dca796558c557bd823bcde039715daf3977`。官方文件两场完整比赛、标准库隔离连续1438动作、键顺序/跨局reset通过。`validation.json`的strength_approval=false是技术工具不做强度决策，不代表失败。最终如选择主候选，直接复制已测归档字节，不必重压。

新DSM修复：原严格复现路线在step241现金27，雇工需要34+55，卖奶位于之后，造成缺2名工人并死亡5草莓1瓜。只在现金不足时前置既有可用库存销售，不改路线/数量，三个诊断败局分别改善38832、40059、43283金币，原两个赢局不变。这五场是有意选择的开发诊断，不能代替泛化。

**旧文件陷阱：** `round8_top2_dsm_contract.py` SHA7735...重复定义agent，官方get_last_callable选到了三参数helper；`round8_dsm_contract_development20.jsonl`的240行全部入口异常，**0完整对局**。原五场显式选agent有策略意义但不验证提交入口。新237681只加唯一末尾函数，官方文件完整720状态、719动作逐个等价，首/最大0.240秒，无错。见`top2/contract_entry_full_validation.json`。旧文件与失败记录保留。

## 最终选择必须完成的事

1. 等新挑战者240开发全结束，比较六对手分布、胜/平积分、尾部失败。不能只用五个诊断局选择。
2. 若挑战者有竞争力，原样在40确认世界跑480局；v7和主候选确认面板可复用。两候选都看确认时报告两者并校正选择，多候选Bonferroni区间已加入`compare_round8.py --familywise-candidates 2`，必要比较三对时取3。或者使用全新reserve作最终选择确认。不要在确认上调参再称独立。
3. 237681若入围，还需用`build_release_round8.py --profile generic`独立打包验证，完整NOTICE/LICENSE在`research/round8/top2/compact_NOTICE.txt`及`compact_LICENSE.txt`。目前没有此归档。
4. `finalize_round8.py`尚未运行，硬编码9fa主候选及原始95%准入。选择挑战者或两个确认候选时必须先修改适配。它写root/main、release_v8、RELEASE_V8、builders，不能提前运行。计数必须排除240入口失败。
5. 更新`RESEARCH_ROUND8.md`、来源登记和提交说明。最终报告实际本地提升与可提交文件，不保证线上3000，不把复现代理说成作者私有程序。

## 研究资产与后续线索

- `TOP2_PUBLIC_METHODS.md`：核对203公开主帖、DSM三成员与Vadim账号，没有取得两队公开方法/私有源码；明确搜索覆盖缺口。
- `top2/STRATEGY_FINDINGS.md`：各24新研究回放，另各5封存；48原局官方精确复现。第216步各24不同状态，不能只按商店拼路线。
- `DSM_CANDIDATE_CROSSCHECK.md`：原DSMstrict对三公开策略48局28胜20负，严重败局用于cash诊断。
- `top2/CONTRACT_FINDINGS.md`与`CONTRACT_REVIEW.md`：cash修复、入口故障、边界审查。
- 剩余step182现金84不足购麦10+草莓100，当前cash修复未解决；top2子任务正在只读追因，禁止改冻结237681。
- projected_shed动物PLACE满仓边界、required忽略其他购买花款正由production子任务核查实际路线可达性，未确认是否影响候选。
- 番茄19株完整运输修复仅已知seed688041503有效；240主开发与80新随机前缀均未触发，不能称广泛增益。
- 初始开发对照、三组64局市场消融、16局粮食保留、末期投入8局零触发等都保留。完整策略研究见根`RESEARCH_ROUND8.md`。

没有更新Codex全局记忆。此文件是项目内续接说明，运行状态需以实际进程/JSONL重新核验。
