# 2026-10-02 #1 官方解技术拆解进复盘轨（msdsm/kagriculture-solution）

> 任务：P2 冠军解拆解（registry a51050-2 前半："拆解报告落档（含神经系vs规则系架构位差专节）"）。
> 对象：Kaggle kaggriculture #1 M&M&P&Q（榜分 ~3067）官方解仓库 `msdsm/kagriculture-solution`（**NO-LICENSE**）+ 讨论帖 745073。
> 纪律执行：产物只落本战役；本文件只增不改 INDEX/JOURNAL/requirements/registry（文末附"需登记行"）；不 git commit；不做在线提交；全程静态拆解（无第三方代码执行）；结论均带出处，自报数字标"**自报**"，我方推算标"**我方复算**"，OCR 来源标"**OCR**"，查不到写"未找到"。

## 0. 材料边界（先立边界，再拆解）

**仓库状态判定（2026-10-02 12:03–12:13 UTC 实查）：404，不可得，全量快照分支不成立。**

| 探查路 | 结果 | 时刻(UTC) |
|---|---|---|
| `api.github.com/repos/msdsm/kagriculture-solution` ×3 | 404 Not Found | 12:03/12:07/12:11 |
| 网页 / `git ls-remote` / raw / codeload | 全部 404（"Repository not found"） | 12:04–12:11 |
| GitHub 搜索 `kagriculture-solution in:name` | total 0 | 12:12 |
| Wayback CDX（prefix）/ Software Heritage / ecosyste.ms / Sourcegraph(`kagg-engine`) | 空 / NotFound / 404 / 0 命中 | 12:08–12:20 |
| 2 个 fork（缓存显示 forks_count=2） | 无法定位；团队六账号公开仓列表无 fork | 12:13 |

该仓"时而 404 时而公开"确证：本战役 `postseason-github/gh_search_correct_*.json`（抓取 2026-10-02 10:57 UTC）里该仓**公开可见**（id 1400989714、created 2026-10-02T03:17:00Z、pushed 2026-10-02T03:30:47Z、size 2346KB、stars 5、forks 2、language Python、default_branch main）；12:07 UTC `/users/msdsm/repos` 一次响应仍列出该仓、12:10 复查即消失（应为边缘缓存或可见性翻动态）。**材料边界**：源树、`docs/*.md`（training-lineage/data/architecture/training/operations）、`configs/*.json`、`THIRD_PARTY_NOTICES.md` 一律**未拿到**；`msdsm_full/` 快照目录**未创建**（不造假目录）。可用材料四路：

1. **README 快照**：`ext/postseason-github/readmes/msdsm_kaggriculture-solution.README.md`（11,199 字节，SHA256 2ff409bf…，公开窗口内抓取）——下称 **README**，行号引用即该文件行号。
2. **官方 docs 三图**：README:16-29 引用的 `docs/images/{overview,training_detail,model_detail}.png` 与讨论帖 745073 正文附件**同源**，已从附件渠道抓回（3200px 宽原图）+ tesseract 双跑 OCR，落 `ext/msdsm-teardown/`（provenance.md + SHA256SUMS.txt）——下称 **图1/图2/图3 + OCR**。图2（training_detail，3200×5295）即 README:100 所指 `docs/training-lineage.md` 的图化版，**逐阶段表以 OCR 全录于 §1**。
3. **讨论帖 745073 全文**：`ext/postseason-platform/github_and_topic745073_raw.json`（10:57 UTC 缓存）+ `ext/msdsm-teardown/topic745073_refetch_2026-10-02.json`（12:05 UTC 复抓，9 评论，与缓存无差异）。
4. **仓元数据**：gh_search 缓存（上表）。源码级细节（真实超参、动作表、Rust/C++ 实现）**无从核对**，凡涉实现只引 README/图面文本。

## 1. 拆解维度①：训练谱系（BC→PPO 交替；逐阶段表全录）

### 1.1 训练口径（图2 脚注区 OCR + README:98-150）

- **环境步数换算**：1 game = 719 decisions × 2 players = **1,438 env steps**；任一玩家走一步记一步（图2 脚注，OCR）。
- **PPO 设计**：current-policy 自对弈、双座位都学；终局胜负和奖励 +1/0/−1，折扣 γ=1；GAE λ=0.97；PPO clip 0.2；teacher KL 正则（图2 脚注，OCR）。rollout 采样双座位、teacher 为 KL 参照（README:122）。
- **BC 语义**：behavior cloning，每条 trajectory = 一个 teacher 座位；BC 数据集计数含 held-out（图2 脚注，OCR）。
- **卡片计数语义**：每卡显示该段/run 总数、**不含祖先**；分支共享祖先不得相加；总量排除 BC、critic 拟合、评测与废弃/重跑；并行线总量含赛后（截止后）工作；计数截至 **2026-10-01 02:03** 停手（图2 脚注，OCR）。
- README:122 明言：`configs/ppo.json` 只是**单卡 64 局/rollout 的示例**，非赛中真实异构 GPU 分配；README:150：12→24 层用 Net2Net（`scripts/grow_model.py`），`--preserve-optimizer` 可连优化器状态一起长。

### 1.2 逐阶段表（图2 OCR 全录；日期=图面时间轴 2026-09-01…09-30）

| # | 时点 | 阶段卡 | 数据/规模 | 备注（图面原文要点，OCR） |
|---|---|---|---|---|
| 1 | 09-01 | Random initialization | — | |
| 2 | 09-01 | Strong public replays | Top 20 + 11 extra + 5 historical teachers；去重后 34 份提交；3,806 unique games | teacher 数据源=公开提交 |
| 3 | | **BC 1** | 4,459 trajectories – 30 epochs | |
| 4 | | **PPO 1** | 472.1M env steps / 328,320 games | |
| 5 | 09-05 | Refreshed top 20 submissions | 3,993 unique games（09-05 刷新） | |
| 6 | | **BC 2** | 4,560 trajectories – 10 epochs | |
| 7 | | **PPO 2** | 900.8M / 626,400 | resumed from a saved policy |
| 8 | | Reset heads – masked PPO | 52.80M / 36,720 | keep the pretrained trunk（重置头、保预训练躯干） |
| 9 | 09-10 | Early heuristic agent | 89 public replay trajectories | rule-based / search-based play |
| 10 | | **BC 3** | 89 trajectories – 1 epoch | |
| 11 | | **PPO 3** | 2.140B / 1,487,952 | separate sell-head distillation*（*卖出量头蒸馏另用 96 局自对弈） |
| 12 | 09-12 | Net2Net growth + PPO | 886.3M / 616,320 | continue from the grown policy |
| 13 | 09-13 | Two public teachers | 214+138=352 trajectories；335 unique games | |
| 14 | | **BC 4** | **352 或 369** trajectories – 3 epochs | OCR 双跑分歧：psm11=352 / psm6=369；无法裁决，两读数并存 |
| 15 | 09-16 | **PPO 4** | 1.329B / 923,904 | 卡面注 **Cumulative: 5.780B env steps** |
| 16 | | Seven public submissions | 849 teacher trajectories | |
| 17 | | **反馈回路**（图1 全图=此回路） | ①观察 BC+PPO 后策略弱点：番茄密集店铺配置、极度偏斜/重复店铺类型 →②改进 planner：任务/路线/交易规划、局部搜索+模拟退火 →③定向自对弈造数：100 局标准店铺 + 100 局 22 个番茄相关店铺 + 100 局 23 个同类型店铺 = 300 局×2 座位 = **600 trajectories**（"Shop overrides for teacher-data generation only"，仅造数用） | |
| 18 | | Continue PPO – Net2Net growth | 155.7M additional / 108,288 | resume this saved policy；scale on September 19 |
| 19 | 09-21 | BC – two public teachers | 112+125=237 trajectories – 3 epochs | |
| 20 | 09-25 | **BC 5** | 849+600=1,449 trajectories – 2 epochs | 含启发式 600 条定向数据 |
| 21 | | PPO – scaled policy | 2.223B / 1,545,984 | "forks use intermediate policies"；卡侧注 "Final-day handoff（…critic）"（OCR 残缺） |
| 22 | 09-26–29 | Fit critic → **PPO 5（大 run）** | **6.142B / 4,271,151** | two saved policies shown below |
| 23 | | 两个存档策略 | **Late policy**（September 29）、**Final base**（September 30） | 从 #22 存出 |
| 24 | | BC – eight submissions | 956 trajectories collected** – 3 epochs | **956 条已收集、accepted 数未核**（图注原文） |
| 25 | 09-29–30 | **Action rules** 卡 | 见 §3.3 | "Used at inference and in the final PPO stage."（推理与末段 PPO 都用） |
| 26 | | Further growth + BC | Two public submissions；256 trajectories – 3 epochs | "Grow again with Net2Net" |
| 27 | | PPO – replay refresh | 2.354B / 1,636,992 | |
| 28 | | **Rule-aware PPO** | Extra env steps: **not recovered** | Sequential action masks；Integrate into PPO；Apply at inference |
| 29 | | PPO – deeper policy | 230.3M / 160,128 | |
| 30 | | Late-policy fork – PPO | 384.3M / 267,264 | "Net2Net – no additional BC" |
| 31 | | Final-base fork – PPO | 485.4M / 337,536 | "Net2Net – no additional BC" |
| 32 | 09-30 | **Final A** | **10.23M 参数** | NN + action repair；Final-day search controller |
| 33 | | **Final B** | **10.23M 参数** | NN + sequential masks；Neural policy on every day |

图面总账（OCR）：**"FINAL A: 11.922B ENV STEPS ON THE RETAINED PPO PATH — 8,290,767 games × 1,438 = 11,922,122,946 env steps. Final B adds PPO whose exact rollout count was not recovered."**（"精确 rollout 数未找回"指 #28 rule-aware PPO）。旁注："These parallel weights are not used in Final A or B"（并行权重不进终件）。

### 1.3 retained path 算术分解（**我方复算**）

对图 13 张 PPO 卡的 game 数做子集枚举：**唯一**子集和=8,290,767 的是 {PPO1 328,320 + PPO2 626,400 + masked 36,720 + PPO3 1,487,952 + Net2Net-PPO 616,320 + PPO4 923,904 + PPO5 4,271,151}；其 env steps 逐卡相加=11,923.0M≈11.922B（卡面圆整差），与图面 11.922B 吻合。含义：图面"retained PPO path"=主干 BC1→PPO1→BC2→PPO2→masked→BC3→PPO3→Net2Net-PPO→BC4→PPO4→（反馈回路）→BC5→Fit critic→PPO5 这条链；**#18/#21/#27/#29/#30/#31 六张卡（cont/scaled/refresh/deeper/两 fork，合计 4,104,752 games）落在该 tally 之外**（对应脚注"Extra env steps / 并行线 / 去弃重跑不计入"口径）。注意：这是按图面算术反推的分解，非其文字陈述；#21/#27/#30/#31 与 Final A/B 的确切箭头拓扑在栅格图上无法无歧义还原（见 §5 限界）。

## 2. 拆解维度②：架构（12-block 10.23M Transformer、动作空间、条件掩码、20M 族）

来源：图3 OCR + README:5,12,144-150。**两个终件同构：10,225,070 参数**（含 value head 66,051；trunk+actor 10,159,019）。

**观测（结构化 token，≤264 tokens）**：200 farm cells + 40 units + 1 global + 12 commodity/animal + 1 memory + 10 market-order slots = 264（分项 OCR，**我方复算**合计对上）；124-feature schema 按 token 型选特征、每型 learned projection + token-type adapters；**memory token 用固定规则从公开信息推断对手库存**（对手库存追踪）。

**共享 Transformer 躯干**：12 个 pre-LayerNorm residual blocks；宽 256；8 attention heads；FFN 256→1,024→256 GELU；**selective 2D rotary** 位置编码；dropout 0。

**动作头（type-specific heads 读出 token）**：
- **Unit policy**：每个己方单位 **500 action candidates**；
- **Market policy**：10 个订单槽，每槽 **1,903 decoded candidates**，含 9 种 goods × 100 档绝对卖出量（0–99 绝对卖量是候选的主要来源）；
- **Value head**：global token→256→标量，配对零和 critic。

**模型增长（Net2Net，保起点策略）**：10M 线 6→12 blocks（终 12-block=10.23M）；20M 线 24 blocks ≈19.7M；更深分支 29 blocks / FFN 1,072 ≈24.4M。推理 **JAX on CPU FP32**（图3 OCR + README:73）。

**条件掩码**（训练/推理两侧口径）：README:82 `actions/` 明列 "Action vocabulary, quantities and **conditional masks**"；Agent B 的 sequential masks 见 §3.2；Final A 靠 Action rules 在推理期实现同类约束（§3.3）。README:168-170：打包器**检查 checkpoint 的 mask 设置**，`export_policy.py --sequential-masks` 只改动作选择配置、不产 Agent B 权重。

## 3. 拆解维度③：推理控制器（Agent A/B；"10M+ 规则补丁"分类）

### 3.1 Agent A（Final A）：置信度修复 + 存储规则 + 末日搜索（图3 OCR + README:7-9）

- 常规回合：**greedy 选 NN 动作→再修复或替换**（"choose greedy NN actions, then repair or replace them"）；
- **Confidence-ordered repair（置信度排序修复）**：按置信序重派冲突动作、可插入种子购买；
- **末日接管**：day 29（最后一天）**先规划后执行**——"final-day handoff"：搜索预算 **dawn 时刻约 6 秒**，然后执行并调整交易；**时间预算不足或搜索失败即回退 NN**（保底永远在）。

### 3.2 Agent B（Final B）：顺序掩码 + rule-aware PPO（图3 OCR + README:9-10,135-141）

- 全程神经策略（含最后一天），不用末日搜索控制器；
- **Sequential action selection**：先 farmer、后 workers，逐步**预留 tiles 与 seeds**；
- **Rule-aware PPO**：PPO 的 rollout 采样与 log-prob 重算**用同一套条件掩码**；**被迫 SELL/DROP 分量从 policy loss 剔除**（结果仍训练 value）；
- 仍套溢出/终局清仓规则；种子购买来自 market policy（图3 OCR）。

### 3.3 "10M+ 规则补丁"全类清单（能列尽列；图3 + 图2 Action rules 卡）

| 类 | 内容（出处：图3 OCR / 图2 OCR） | 归属 |
|---|---|---|
| R1 冲突/重复任务修复 | prevent duplicate tasks；reassign conflicts（置信度序） | A |
| R2 种子库存超支防护 | seed-inventory overspending 拦截 | A |
| R3 无用动作屏蔽 | reject off-board moves、unproductive fertilizer / care | A |
| R4 存储溢出预测与出售 | 预测动作+交易后的库存，超容量 **100** 即卖溢出、**保留饲料小麦** | A+B |
| R5 溢出出售排序+价格更新 | 按现价/基准价排序卖溢出、更新价格 | A+B |
| R6 末两动作清仓 | sell remaining stock on the last two actions | A+B |
| R7 强制最终 DROP | 终局 shed 的单位强制 DROP | A+B |
| R8 抑制晚买/雇佣/购地 | suppress late buying, hiring and land purchases | A+B |
| R9 置信度动作修复 | confidence-ordered repair，可插入 seed buys | A |
| R10 末日搜索控制器 | day 29：任务分配/路线/收获/交付优化、交易规划最大化终局钱、局部搜索+模拟退火+多重启、~6s 预算、失败回退 NN | A |
| R11 顺序掩码（内生为训练约束） | farmer→workers 序贯出招、预留 tiles/seeds；进 PPO 损失口径 | B |

图2 Action rules 卡三行原文："Avoid conflicting tasks and seed overspending / Mask useless fertilizer, care, off-board moves / Sell storage overflow; liquidate at game end"，注 **"Used at inference and in the final PPO stage"**——规则同时是末段 PPO 的环境约束。其旁白序列"Apply at inference / Integrate into PPO"正是两条路线：A=推理期补丁，B=**做进 PPO（内生化）**。

## 4. 拆解维度④：工程（Rust 批环境 / C++17 planner / 打包产线 / pin）

（全部出自 README，行号随引；源码未得，无实现细节可核。）

- **栈**：Python 3.12+；神经实现 **JAX + Optax**（版本 pin 至最终训练源）；批环境 **Rust（`native/engine/`，Rust 1.88+，`kagg-engine==0.3.24`）**；搜索教师与 Agent A 另用 **C++17 planner**（`scripts/build_search.py` 构建，Kaggle 归档需 Linux x86-64 产物）（README:45-71）。
- **规则 pin**：`kaggle-environments==1.32.7`；推理 FP32 on CPU（README:73）。
- **打包产线**：`scripts/package_submission.py`（README:152-170）——校验 checkpoint 的 mask 设置→写自包含 `python/main.py` 入口→导出神经参数→记录文件哈希；**Agent A 归档内含编译好的 search 库，Agent B 不含**。只产本地文件。
- **评测**：`scripts/evaluate.py`（README:172-187）双进程对打、每 seed 双座位各打一遍；自注"不完全复现 Kaggle 容器调度与计时"。
- **训练脚本族**（README:104-150）：`init_model.py`（10m.json / 6-block bootstrap）、`train_bc.py`、`warmup_critic.py`（只拟合 critic、冻 actor+trunk）、`train_ppo.py`（`--max-env-steps`、`--resume`、`--enable-sequential-masks`）、`grow_model.py`（Net2Net 12→24）；BC→PPO 循环以 PPO ckpt 喂下轮 BC `--initial`；BC 换新优化器、PPO resume 恢复优化器/RNG/seed 游标（README:133）。
- **目录即产品结构**（README:77-94）：observations（typed tokens+对手库存追踪）/ model（Transformer+attention kernels+Net2Net）/ actions（词表+数量+条件掩码）/ data（replay 标签+启发式自对弈）/ training（BC/critic/PPO/rollouts/ckpts）/ agents（greedy 推理+两终控制器）/ heuristics（单位动作修复+存储出售+搜索移交）/ search（py wrapper+C++ search+local rules）+ configs 全套 preset + k8s 通用 Job 模板 + tests 冒烟（含 Net2Net 保函数检查）。
- **README:216**：仓库组织参照 Orbit Wars 解仓（IsaiahPressman/kaggle-orbit-wars）；算法自研。README:12：**checkpoint/replay 数据/编译产物 "supplied separately by the user"——权重未随仓公开**。
- **算力口径（自报，讨论帖 745073 #3531578，msd0110，2026-10-02 05:48 UTC）**："10M PPO run 最多 17×A100 + 29×A30（均值约 7×A100+20×A30）；20M PPO run 最多 26×A100"。旁证：提问者称"在你仓里看到 A100/A30 字样但没找到数量"（#3531570）——硬件线索原在仓内（现不可得）。

## 5. 拆解维度⑤：架构位差专节（核心）——"规则=修复器" vs "规则=生成器"

### 5.1 两种架构位

| 维度 | msdsm（#1，~3067） | 我方磁带系（v48 衍生→H1/C_final 谱系；同门 haodou/tetsutani 顶带 ~2216-2345） |
|---|---|---|
| 动作主生成器 | **神经策略**（264-token 观测→Transformer→500 候选/单位、1,903 候选/订单槽） | **磁带剧本**（预录整季产线：开局花到~$190、d6 买地+5 牛、d10 买地+12 雇工…，见 README.md:7） |
| 规则的位置 | 生成器**输出之后**：修复/替换/投影（置信度修复、屏蔽、溢出清仓）；末日才整段接管（搜索） | 生成器**本身**就是规则（剧本=规则流）；外挂层是薄补丁（反克隆抢卖/卖单槽位重排/终局清仓） |
| 规则与生成器的分工 | 互补：NN 管"想做什么"，规则管"合法/不浪费/账目" | 重叠：外挂层常常重做基座内生已有的机制 |
| 失败保底 | 回退 NN（时间不足/搜索失败） | 无第二生成器可回退，剧本即全部 |
| 状态条件化 | 全状态条件化（观测入网） | 窄反应层条件化，主体固定剧本 |

### 5.2 为何"外挂定理（外挂必负）"在其架构下不成立

我方定理（分析35:19 定稿语："想加的机制若基座内层已有，外层再实现必负；要做就做进内层"；分析36:13 精化："**外挂必负=重复内生机能；补缺型外挂（X1）无恙**"）的适用前提是：**外挂与基座同为动作生成器**。磁带系里外挂层若重做基座内生机制（R28 账本双计→604 恒等违例；I2 HERD/COURIER 与 H1 同源冗余；K1 相位错峰 vs H1 已调时序——四次同型失败，分析35:19、分析47:14），等于两个生成器抢方向盘，必然双计/互踩。

而 msdsm 的规则是**修复器/控制器，不是第二个生成器**：
1. **它不产生主意**——主意全由 NN greedy 给出；规则只做可行性投影（去冲突/去浪费/守账目）。修复器重复不了"策略函数"，因为它根本不输出偏好，只裁剪输出集。
2. **它占据的是 NN 结构性弱位**：跨单位资源互斥（种子/地块/库存）与终局全局优化——恰是逐单位出招的策略网络难保的性质。补缺型，非重复型（对照我方 X1"无恙"判例）。
3. **末日搜索是"能力异质"的换轨**（局部搜索+模拟退火+多重启做任务/路线/交易全局规划），不是把 NN 的活再干一遍；且带 NN 保底回退，永远不会与 NN 对打抢戏。
4. **其"内生化"路线（Final B）反向印证定理**：把规则做进 PPO（sequential masks 进 rollout 采样与 log-prob 口径、被迫 SELL/DROP 剔出 policy loss）——这正是我方"要做就做进内层"的同构动作。冠军从另一头走到了同一条结论。

**结论**：外挂定理的本体是"生成位不可双占"，不是"规则无用"。规则放在**修复位/投影位/换轨位**（补缺）时不但不负，还是 #1 的核心赢件；规则放在**生成位**重复内生机制时必负——这在神经系里同样成立（若他们再训一个并行策略来"修"主策略，一样翻车）。

### 5.3 与磁带系（haodou/tetsutani）及我方 H1/C_final 对表

- **同门顶带**（references/2026-09-28-family-topband-deepcut-scan.md:3）：tetsutani 2307 / haodou092 2216——全部是磁带系；其增益来自**生成器内容**（变现时机+需求门控，实现价 +1.35pt、早卖 3.7 天，分析34:19）。我方 v48→H1→C_final 的增益同样来自生成器内容+薄补丁（采纳先例 +1000 级/次）。
- **位差读数**：磁带系天花板 ~2300 带（自报/扫描口径），冠军 ~3067——**~700 分差是"固定剧本+窄反应" vs "全状态条件化策略+修复器"的范式差**，不是调参差。磁带的强项（可解释、字节稳定、门槛好立、单兵可维护）恰是神经系的弱项，反之亦然。
- **H1/C_final 谱系镜像**（分析48:3-13）：我方终盘教训是"选优尺（h2h）与终评尺（全场 BT）错位、非传递环 C_final>H1>mpx>C_final"；msdsm 侧对应物是其**双线并验**（10M 线=更多自对弈局数假设、20M 线=更多参数假设，各配独立 PPO 预算）+ 13 件量级的 teacher 横扫——他们把"哪个更强"的判断建立在自对弈规模与多教师回放上，而非单一对照对打。

### 5.4 对下战役基座选择的含义

1. **首选形态**："学习型提议器 + 规则修复器/投影器 + 末日换轨搜索"三层栈；规则只占修复位/换轨位，绝不占生成位重复内生机制（外挂定理继续有效，且被冠军反向印证）。
2. **若受算力约束留在确定性基座**：增量应砸进生成器内容（磁带剧本的时机/门控），外挂只做补缺型（X1 型）；想加的新机制一律"做进内层"。
3. **基建前置**：8.29M 局自对弈（11.9B env steps）背后的 Rust 批环境+双座位 rollout+critic 拟合+Net2Net 续训是入场券；下战役若走神经路线，批环境吞吐与"BC→PPO 交替+teacher KL"流水线要在蓝图期立项（挂 registry a51050-5）。
4. **评测尺**：冠军的规则同时进"末段 PPO 环境约束"（Action rules 卡注记）——约束内生到训练环境而非只在推理打补丁，与我方分析48"换尺"教训合成：行为约束与选优判据都要放在**终评口径**（全场稳健）上设计。

## 6. 讨论帖 745073 全文口径（承诺 writeup / 权重 / 自报数字清单）

帖："[1st Place (currently)] A preview of our solution: BC, Self-Play PPO, and Heuristics — M & M & P & Q"，作者 msd0110，2026-10-02 03:38 UTC，54 票，9 评论（12:05 UTC 复抓无新评论）。要点：

- **自报战绩口径**：赛中不同时点以 10M 线、20M 线、独立启发式 planner **三者都拿过 #1**；最终选 **"10M model with a rule-based action patch at inference time"**（=Final A）。
- **自报规模**："final 10M model's training lineage includes approximately **8.29 million self-play games**"（图2 精确化为 8,290,767 局/11.922B env steps）。
- **自报算力**（#3531578）：10M PPO **up to 17×A100 + 29×A30**（均值 ~7×A100+20×A30）；20M PPO up to **26×A100**。
- **自报训练现象**（#3531565，答"二轮 BC 后掉点是否正常"）：PPO 后再 BC 的 ckpt 对 BC 前 ckpt **100 局全败**；但从该 ckpt 恢复 PPO 自对弈 **~60,000 局后反超**——佐证其 BC→PPO 交替是"摔一跤再爬"的常态。
- **承诺的详解 writeup**："We'll publish a detailed writeup once the ratings have converged and the final standings are confirmed."——**截至 2026-10-02 未发布**（本帖即预告帖）。
- **权重链接**：帖内**未找到**任何 checkpoint/权重链接；README:12 亦称 checkpoints "supplied separately"。未找到。
- **自报 vs 官方图一致性**：帖文与图2/图3 三图同源（附件即 README 引用的 docs/images）；数字口径一致。

## 7. NO-LICENSE 纪律执行

只研究不搬运：未向我方任何产线/工件/implementation 目录拷贝其代码（其源码本就不可得）；引用仅限 README 短句（带行号）与官方论坛贴图的 OCR 摘句（带图名）；原始证据（论坛贴图+OCR+帖文 JSON）隔离存放于 `ext/msdsm-teardown/`（自有 provenance+SHA256），与我方产线物理分离。若权重日后投放：实测走判决跑批、其架构"参考不复制"。

## 8. 异常与限界（汇总）

1. **源树不可得**：仓 404（震荡窗口实证），`msdsm_full/` 未建；`docs/training-lineage.md / architecture.md / training.md / data.md / operations.md`、configs、C++/Rust/JAX 源码全部未拿到——维度①②③靠三图 OCR 兜底，④只有 README 级信息。
2. **OCR 误差**：图2 分辨率 3200×5295、卡片密集，数字经双跑 psm6/psm11+局部放大交叉核对并以算术自洽性校验（8,290,767×1,438=11,922,122,946 ✓），但 **BC4 轨迹数 352/369 两读数无法裁决**；#21 卡侧注（"Final-day handoff…critic"）残缺；**fork/存档策略与 Final A/B 的箭头拓扑无法从栅格图无歧义还原**（§1.3 的 retained path 分解是算术反推，非文字实证）。
3. **自报不可复核**：829 万局、17×A100+29×A30（均值口径）、26×A100、"三线都拿过 #1"、"60,000 局反超"均单方自报，无消融/无第三方验证；其榜分 ~3067 为我方既有读数引用（非本次实测）。
4. **权重未投放**："supplied separately"且仓已转 404——**真件强度实测（a51050-2 后半 / a51050-5 判据）无从执行**，须待其重开仓或投放权重。
5. **2 个 fork 失踪**：forks_count=2 但 fork 不可枚举（仓转 404 连带），无法用 fork 兜底拿源码。
6. **人名-账号映射为推断**：README 表（morim3/msdsm/BergBuch/qistripute）与帖文（morim3/msd0110/Piiiiiiiii/qistripute）两套署名，msdsm≈msd0110、BergBuch≈Piiiiiiiii 为对应推断（职责文案一致），非实证。

## 需登记行

**A. `fn_docs/hybrid/references/INDEX.md` 追加 2 行（含证据包）：**

| 路径（相对本目录） | 来源 URL | 抓取日期 | 用途 | 引用它的产物/任务 |
|---|---|---|---|---|
| `2026-10-02-msdsm-teardown.md` | GitHub：https://github.com/msdsm/kagriculture-solution （404，元数据取自 ext/postseason-github/gh_search_correct_*.json@2026-10-02 10:57 UTC）；讨论区：https://www.kaggle.com/competitions/kaggriculture/discussion/745073 （含正文附件 docs/images 三图）；README 快照 ext/postseason-github/readmes/msdsm_kaggriculture-solution.README.md | 2026-10-02 | #1 官方解拆解：训练谱系全录（8,290,767 局/11.922B env steps retained path）/10.23M 架构/Agent A·B 控制器与 11 类规则补丁/工程栈；架构位差专节（修复器≠生成器，外挂定理边界） | 复盘轨；下战役基座决策（a51050-5）；权重投放后实测队列 |
| `ext/msdsm-teardown/`（provenance.md+SHA256SUMS.txt+docs_images 三图+ocr 七件+topic745073_refetch） | 同上（三图=745073 论坛附件；topic JSON=kaggle CLI 复抓） | 2026-10-02 | 冠军解证据包（NO-LICENSE 隔离存放，只研究不搬运） | 2026-10-02-msdsm-teardown.md |

**B. `fn_docs/hybrid/analyses/registry.jsonl` a51050-2 状态行建议改写**（本任务仅完成前半，后半待权重）：

```json
{"id": "a51050-2", "date": "2026-10-02", "phenomenon": "#1 官方解技术拆解进复盘轨（msdsm docs 全套+745073 详解+权重投放后真件实测）", "target": "复盘轨知识资产", "expected_signal": "拆解报告落档（含神经系vs规则系架构位差专节）；权重投放后真件强度实测", "status": "partial", "scored_in": "拆解报告已落档 references/2026-10-02-msdsm-teardown.md（架构位差专节§5）；docs 源树未得（仓 404）改用官方三图 OCR 全录；真件实测阻塞于权重未投放（supplied separately）"}
```
