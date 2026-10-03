# 公开代码来源与本轮选择

获取日期：2026-09-21。通过 Kaggle 官方公开 kernels/pull 接口下载 Notebook；原始响应保存在 `external/*_response.json`。只提取源码单元，没有执行 Notebook 中的安装、下载或提交单元。

| 作者与作品 | Notebook 版本 | 保存的代码 | 用途 |
|---|---:|---|---|
| [Roxy / Adaptive Public-State Multi-Route](https://www.kaggle.com/code/yamakawanin/kaggriculture-adaptive-public-state-multi-route) | 1 | `external/roxy_exact.py` | 外部对照 |
| [Rayk Kretzschmar / Findings from Zero to Top Meta](https://www.kaggle.com/code/raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta) | 22 | `external/rayk_c94.py`、`external/rayk_c95.py` | 复现；C95 用于外部对照 |
| [Ahmed Berat Özer / V38 Smarter Feed, Stronger Margins](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) | 2 | `external/ahmed_exact.py` | v5 采用的完整策略 |

上述公开 Notebook 标示 Apache-2.0。Ahmed 源码本身包含完整许可和多个上游作者署名；发布文件原样保留这些内容。本轮没有原创其生产路线、学习模型或策略融合，不将上游成果描述为自行训练成果。

## 源码 SHA-256

- Roxy：`9b5e1157af3d4a643fcd818f5c290003d2672230d5ae8c0024fae0836cc894df`
- Rayk C94：`7b0e5a7b9d18dc583f5789e50a54dca43561f6d08c1c616b4219bf50bcb8311f`
- Rayk C95：`489f5d197527f107027626cce79d850fd2ca90edd43d94384b849b6511e27bdb`
- Ahmed V38：`a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e`

均与各 Notebook 自述的冻结源码哈希匹配。最初提取的 `roxy_v1.py`、`ahmed_v38.py` 被 Windows 文本写入转换为 CRLF，仍保存以对应初期对战报告中的哈希；`*_exact.py` 使用原始 LF 字节。它们仅换行不同，源码逻辑一致。v5 提交包采用精确 LF 原版，并另外验证实际包。

压缩载荷和 exec 字符串已解码为 `external/decoded_*.py`、`rayk_nested.py`、`ahmed_nested*.py` 供审阅；嵌入的 JSON 路线数据不当作程序执行。检查了导入、嵌套执行和外部访问调用，最终实际包也完成禁用第三方包的连续推理核验。这是针对本次冻结版本的检查，不是对所有上游版本作安全保证。

Igor 的原先检索链接本次公开下载返回 404，未把它算作已复现对手。当前只取得两套外部参照策略，且公开方案可能共享部分上游路线，不能宣称完成了十种独立强手联赛。


## 2026-09-21 第二轮公开策略与回放研究

- [Ahmed V53](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v53-opening-signature)：`external/ahmed_v53.py`；SHA-256 `20fe549dd4573b9fd1dfb32a1782c205fa74f0edfdfd6cbe935079533e0a9d0e`。
- [Dmitrii One More Wheat](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-one-more-wheat)：`external/one_more_wheat.py`；SHA-256 `10f58185b916392ca39697c83f67f455df81a74dfb6eb1aacd60fd81d50c9970`。v6 原样采用，附带原始 NOTICE 和 LICENSE。
- [Nathan Pipe16](https://www.kaggle.com/code/nathanjacob/kaggriculture-pipe16-idle-workers)：`external/pipe16.py`；SHA-256 `827ddf2997fa442e80baadebc4cc91ffaeedec1ff333c1fa7d872b0f1d448181`。

原始 Notebook API 响应与静态解码结果保存在 external，重现入口为 extract_research_candidates.py。三个来源均保留上游署名。前十回放索引、对应提交 ID、原始 episode JSON 与研究/验证划分在 research/top10。自制市场扩展未通过升级标准，保留作负面实验，未进入提交包。

## 2026-09-22：v7 来源

- [shiiin9 / Your Market List Is an Order Book](https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book)，Notebook版本2，`external/orderbook.py`；SHA-256 `a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab`。
- [Ahmed Berat Ozer / V56 Smarter Seeds and Fertilizer](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer)，Notebook版本1，`external/ahmed_v56.py`；SHA-256 `a1ad0fd1d174477ee2cbdd561a812bcb7029647ce34599e79d6b79e9057eff6c`。
- v7保留Orderbook完整源码，仅接入V56种子与肥料机制，修改父入口以保留市场排序层，增加真实入口和错误计数汇总。融合构建脚本为`build_round7_orderbook_v56.py`；完整审查见`research/round7/SOURCE_AUDIT_AND_FUSION.md`。
- Vadim Vasilenko（提交56427964）、DSM（56444344）公开回放用于18场研究及独立模仿实验，原始episode编号和实际成交编译在`research/round7/top2/`。未取得作者私有决策源码，模仿路线未进入v7包。
- yomogii公开episode111747876用于19株番茄空间调度实验，来源标注保留在实验源码；该实验未通过发布门槛，未进入v7。

本轮所有发布源码保留原有Apache-2.0许可证与署名，并在包内NOTICE中列明融合来源。本轮本地验证结果见RELEASE_V7.md，不借用作者自报胜率作为我们的成绩。

## 2026-09-22：round8 待用来源与证据边界

以下是已取得的研究来源和候选归属，不表示候选已通过最终强度验收或完成发布。原始 Notebook 响应保存在 `external/round8/*_response.json`；压缩载荷采用 `ast.literal_eval` 加静态解码提取，未执行 Notebook 的安装、下载或提交单元。嵌套可执行字符串与导入审计见 `research/round8/public_source_audit.json`。

| 作者与作品 | 版本 | 保存文件与用途 |
|---|---:|---|
| [haideptry / The 2965 Master Hybrid Engine](https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine) | 4 | `external/round8/master2965/main.py`；公开对照及 R148 / ADV / IG 组件来源 |
| [hakdevelopment / Kaggriculture 2887 Score Fieldcraft Agent](https://www.kaggle.com/code/hakdevelopment/kaggriculture-2887-score-fieldcraft-agent) | 4 | `external/round8/fieldcraft/main.py` 与 `mirror_plan.py`；两文件公开对照 |
| [leoprovorov / A Song of Ice and Fire, Fixed Flexible](https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible) | 13 | `external/round8/icefire/main.py`；静态审查及公开对照 |

冻结源 SHA-256：

- Master2965：`93831c18a43c49312a71fa67171224681c52c3fade0259403e8d8fae7973565f`。
- Fieldcraft main：`4aa771451850e68892fc1a847211f0bebffd511d6d3a508a7bb9969e5b881091`；mirror_plan：`65727d56185b2d61fa6ca6ec999650b4a1f7dc060099ccbee8ce88d35a3b05a0`。
- Icefire：`0a502ea62d10373281973ce7aebad5935ba73743e5c507c6f00ce49af260ee03`。

Master 中的 R148 溢出回收保留 Ahmed Berat Ozer EXP277 归属；ADV 提前出售保留 Ahmed EXP293 及其注明的 sdy623 / jaxa623 “Beyond 48-0” 机制归属；IG 开局保护和卖单整理保留 Master 上游来源。本地工作是接口融合、最终订单观测同步、组合诊断，以及把 ADV 限制到 step < 696；不是原创这些公开组件。组件边界与哈希见 `research/round8/public_fusion_manifest.json`。候选保留嵌入的 Apache-2.0 声明、完整上游 NOTICE 和 LICENSE；不虚构未取得的 Master 独立许可证元数据。

19 株番茄空间规划参考 yomogii 的公开 episode `111747876`，本地实现根据观测决定是否扩种、如何雇工养护和返仓。它属于回放启发的本地实现，不是取得了 yomogii 的代理源码。冻结候选 `experiments/round8_bounded_production.py` 的 SHA-256 为 `9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e`；完整 NOTICE 位于 `submissions/candidate_v8/NOTICE.txt`。其技术验收与最终强度选择分别记录，不互相替代。

DSM（denden12 / shimishige / masspeaks）和 Vadim Vasilenko（vadimvasilenko）的公开回放各 24 场用于研究；原始 episode、账号、提交 ID 与划分见 `research/round8/top2/`。**没有取得两队的私有决策源码，回放观察不能表述为作者公开算法。** 我们的 DSM 重构代理及 compact 版本是本地研究程序，运行时 Chassis 的公开上游归属独立保留；完整说明和许可见 `research/round8/top2/compact_NOTICE.txt`、`compact_LICENSE.txt`。

直接一手方法核查见 [TOP2_PUBLIC_METHODS.md](research/round8/TOP2_PUBLIC_METHODS.md)：核对了本赛题 203 篇公开主帖和四个作者账号的可读取 Code，找到 masspeaks 的防诈骗讨论，未取得两队本赛题方法文档或代理源码。该报告明确保留匿名列表计数差异、历史评论和 Writeups 未完全展开等覆盖限制；不能把“本次未找到”说成“他们肯定从未公开”。本地重构对手的胜负也不能代替与真实在线代理的对抗结果。
