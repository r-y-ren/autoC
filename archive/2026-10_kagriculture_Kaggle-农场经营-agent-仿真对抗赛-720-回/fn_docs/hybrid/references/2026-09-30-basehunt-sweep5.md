# 2026-09-30 新基座猎寻扫查册（第五轮）——非 v48 族完整可跑基座专项

> 任务：猎寻**不同架构的完整可跑基座**（预训练模型/RL 权重/模仿学习件/独立架构 agent，非 v48 族衍生）；顺带开源兑现复验（截止 ~13h 放码高危窗）、09-29 日包/语料行为新形态、今日策略文。基线：2026-09-30-kaggle-sweep4.md、2026-09-30-github-sweep4.md。
> 通道：HF REST API（models/datasets/spaces+commits）、GitHub REST API、kaggle CLI 2.2.4（kernels list 全量/kernels pull 解包/leaderboard/topics/用户级 kernels list）、georgy 语料本地重算（/tmp/scan7/georgy/ 469k 特征行+509k agents 行）。工作件 /tmp/scan9/（未入仓）。
> 纪律：逐条带来源 URL+抓取日期（均 **2026-09-30**）；自报标"自报"；我方解包/重算标"重算"；查不到写"未找到"。榜面快照 08:43:29Z。**注意：本轮为"新基座角"扫查，多数候选为存量公开件此前未入册，非窗口增量**；学习式件一律按禁区9 只登记不采。

---

## 〇、直接回答

**"有无新基座？"——有，5 件可跑学习式基座 + 1 件权重孤立件，但没有一件能直接换我方底盘；真正可入池的只有 hesoponyo 纯 RL Transformer 与 kaitofukami minimax 两件。**

1. **hesoponyo/pure-rl-agent-bc-ppo-self-play（头号新基座）**：entity-token Transformer 每单位策略，BC ~4,600 公开回放 → PPO 自博弈（Rust 向量化环境）；**提交形可跑**：main.py 内嵌 lzma+base85 fp16/fp32 权重 + 纯 Python forward（stdlib only）+ agent(obs) 入口。自报中位 money **$81,000 vs public_top1** / $121,470 vs starter。
2. **kaitofukami v58 Minimax Closed Loop**：公开状态 best-response（轨迹记忆+4 checkpoint 续局/时机专家），zlib+base85 内嵌 main.py；自报 58/58 胜 v57 已见 29 流、238/238 五回归面板。行为形态非 48/BUY5 族。
3. **djamilabenchikh V16-RC5 + GNN + Double DQN 残差**：专家底盘 + 窄干预残差（只推迟 premium SELL 一回合），推理权重=JSON 纯 Python 可跑。
4. **mzcao7 LightGBM+XGBoost 树集成**（peak 2476.8 自报，**Apache-2.0 随包**，yhay81 路线资产）。
5. **KiroSamurai HF IL checkpoint**（v4 arch 权重+校准件）——但配套 GitHub 仓 **404 私有/删除**，权重孤立不可跑。
6. **sweeden-ttu MuZero 全栈**——架构完整但 **.pt 权重未入库**，且其自评 buoy gate 显示 MuZero 头候选 **0-4 负于自家启发式**（自证不可用）。

**开源兑现仍未落地**（顶强 36 账号 kagri 件全 0；GitHub 0 新仓）；**行为面：池顶克隆单一形态 vs 顶强 20 队全部非族形态**（≥6 种高分异形态，全在私有自适应手里）。

---

## 一、新基座候选清单（架构/可跑性/许可/池测价值）

| # | 件 | 架构 | 可跑性（推理入口） | 许可 | 池测价值 |
|---|---|---|---|---|---|
| 1 | **hesoponyo/pure-rl-agent-bc-ppo-self-play**（https://www.kaggle.com/code/hesoponyo/pure-rl-agent-bc-ppo-self-play ，notebook 780KB，lastRun 09-16，6 票） | 每单位 entity-token **Transformer 策略**：BC(4.6k 回放)→PPO 自博弈（Rust 向量环境）；fp16/fp32 混合权重；推理期仅 sticky 目标 + no-idle 两规则 + 自回归 tile 选择 | **可跑**：%%writefile main.py 内嵌 lzma+base85 权重单字面量 + 纯 Python forward，agent(obs) 入口，stdlib only；大模型超 1s actTimeout 已自弃 | 无明确 LICENSE（局部引用 alperen metacounter Apache-2.0 件）→干净室 | **高**：可直接入对手池（学习式整件、行为非族形态）；禁区9 不采为我方策略，作 A1 对手/P4 对照。自报 $81k vs public_top1（seeds 30401-30412 双席 24 局，自报未复核） |
| 2 | **kaitofukami/238-238-known-streams-v58-minimax-closed-loop**（https://www.kaggle.com/code/kaitofukami/238-238-known-streams-v58-minimax-closed-loop ，lastRun 09-01，48 票） | **minimax closed loop**：公开状态 best-response——option-preserving 路线底盘 + 4 个可观测 checkpoint 选兼容续局/市场时机专家；不需对手身份/seed/未来动作 | **可跑**：zlib+base85 payload（SHA256 校验）展开即 main.py，notebook 直接产 submission.tar.gz | 未见 LICENSE →干净室 | **高（对手件）**：轨迹记忆 best-response=对录像系对手强反制形态；自报 58/58（29 流双席）/238/238（自报未复核） |
| 3 | **djamilabenchikh/graph-reinforcement-learning**（https://www.kaggle.com/code/djamilabenchikh/graph-reinforcement-learning ，lastRun 09-23，5 票） | V16-RC5 专家底盘（base85 内嵌源）+ **GNN(GCNConv)+Double DQN 残差**：学习件只判"是否把 premium SELL 推迟一回合"（窄干预） | **可跑**：agent(obs) 打包 submission.tar.gz；推理权重=JSON 纯 Python（_G_WEIGHTS），无 torch 依赖 | 未见 LICENSE（V16 底盘来源未钉）→干净室 | 中：学习式残差（禁区9 记录）；"专家底盘+窄残差"形态是学习式合规化的参考形 |
| 4 | **mzcao7/kaggriculture-2476-8-peak-lightgbm-xgboost**（https://www.kaggle.com/code/mzcao7/kaggriculture-2476-8-peak-lightgbm-xgboost ，lastRun 09-18，4 票） | **LightGBM+XGBoost CPU 树集成**晚局 routing：配对反事实训练+grouped CV；路线资产=yhay81 shop-router-0908 | **可跑**：agent(obs,config) + main.py 打包 tar；权重件另发 https://www.kaggle.com/datasets/mzcao7/kaggriculture-lightgbm-xgboost-agent | **Apache-2.0 随包**（LGBM-APACHE-2.0.txt）→可署名移植 | 中：学习式（禁区9 记录）；2476.8 peak=中游件；树集成形态可作 A1 对手指纹 |
| 5 | **KiroSamurai/kaggriculture-il（HF dataset）**（https://huggingface.co/datasets/KiroSamurai/kaggriculture-il ，09-06 后无更新，1085 下载） | 监督克隆 **v4 网**（width=128 depth=4 use_z conditional_units conditional_market）：bootstrap_v4/step_003000.msgpack 4.9MB + calibration_1327_v4.json + 9.7GB/20,494 局 episode 库（08-07→09-05）+ 冻结切分 34,115 train/53 holdout | **不可跑**：配套 https://github.com/Kirosamurai/kaggriculture **404（私有/删除）**，net16 loader/工具链不在公开面；权重孤立 | license: other / kaggle-competition-replays（回放受竞赛条款） | **低（当下）/高（若开仓）**：唯一带训练基线的 IL 权重件；开仓即成完整 IL 基座。仅登记 |
| 6 | **sweeden-ttu/kaggriculture_1_37_muzero**（https://github.com/sweeden-ttu/kaggriculture_1_37_muzero ，09-27 建/09-28 20:29Z 推，493 文件） | **Sampled MuZero** 全栈：28 通道 10×10 空间 ResNet + 因子化三头（15/32/20）+ 601 原子价值头 + SimSiam + PER + 4 阶段 curriculum（BC→bootstrap→MCTS-distill→LoRA-PPO）+ league/PFSP + 打包器 | **半可跑**：dist/main.py（1,054,298B，Apache-2.0 头）="Hybrid Direct 底盘（**V57 族**+shiiin9 盘口移植+EXP 层）+ MUZERO EXPAND GATE 嫁接"，**.pt 权重未入库**（仅作者本地卷），无权重时 try/except 回落启发式=可跑但非 MuZero | 文件头 Apache-2.0（无 LICENSE 文件） | **低**：**buoy_gate_report.json 自证 MuZero 头候选 0-4 负自家启发式冠军**（reward 0 vs 163-190k，门槛 0.55 未过）；README"Rank#1/4000+"虚标。可跑件本身=48/V57 族衍生非新基座 |
| 7 | **diffmap/kaggicultureRL**（https://github.com/diffmap/kaggicultureRL ，MIT，08-20 后无更新） | PPO 单座/双座自博弈 + behavior_mimicry + Rust 批量引擎（maturin）；model.py 49KB 策略网定义 | **无权重、无提交形 agent**（108 文件无 .pt） | MIT | 低：训练框架基座（要自训）；禁区9 |
| 8 | **THLPH/Kaggriculture_AdvancedFarmer RL_Lion**（https://github.com/THLPH/Kaggriculture_AdvancedFarmer/tree/RL_Lion ，09-30 02:38Z 后无新） | RL_v2/v2_1/RL_LION notebook + mp_worker.py（FarmPolicy nn.Module + MpVecKag 向量环境） | 无权重发布 | 未见 | 低：禁区9 训练件 |
| 9 | **pranav-bot/kaggriculture IQL/Meta-CFR**（https://github.com/pranav-bot/kaggriculture ，09-29 17:38Z 后静默） | experiments/iql_value/*.pt ×4（328KB，IQL 价值网权重+训练脚本+tests）+ meta/cfr.py 17KB + Hybrid Grandmaster 44KB 启发式提交件（双队分工/Day0 3牛2羊） | 权重在仓；IQL 进提交件与否未证；Grandmaster 件可跑 | 无 LICENSE | 中低：**唯一仓内 RL 权重**；禁区9 记录 |
| 10 | **sweeden-ttu HF model/dataset**（https://huggingface.co/models/sweeden-ttu/kaggriculture-season-training 、/datasets/sweeden-ttu/...） | **非 agent 基座**：model 仓仅 2 PNG；dataset=24 张农场渲染图 winner 分类 demo（16/4/4，OpenRail-M） | 不适用 | OpenRail-M | **无**：此前"权重在册"判定降级修正——无权重无推理件 |
| 11 | **savadogoodgadama75/kaggriculture-agent-demo**（https://huggingface.co/spaces/savadogoodgadama75/kaggriculture-agent-demo ，09-14） | "V8 FSM+BFS"启发式（submission3.py stdlib，TARGET_HANDS=11/COWS=8/SHEEP=6）；gradio 壳不真跑 agent | submission3.py 有 agent 入口可跑 | 无 | 低：弱启发式；池测可跑但预期垫底 |
| 12 | **whzy3185/kagriculture**（https://github.com/whzy3185/kagriculture ，09-30 06:23-07:40 首推 GitHub） | **族衍生非新基座**：Metav4/Pipe16 系（PROVENANCE 钉 dmitriigluzdov/nathanjacob，SHA fd39dffa 族）EXP-007~066 工作台+确定性打包+tape 回放评测 | 可跑（main.py 1MB 级族件） | 上游 Apache-2.0（LICENSE/NOTICE/PROVENANCE 齐） | 中：**EXP066 liquidity-wool-flush** 自报修 2 条官方 wool-race 败录 +1,032/+300、12 强开源 134-0-10、40 局平 EXP054；reports/EXP045_EXP054_KAGGLE_FAILURE_OPTIMIZATION_**20260930**.md=今日新情报（自报未复核） |

## 二、开源兑现复验（08:43Z，截止前 ~15h）

- **Kaggle 顶强 20 队 36 个 member 账号逐个 kernels list --user**：kaggriculture 件**全数 0**（仅他题旧件：ttyn4519 18 行/jjinho 14/gengsr 11/justnik77 5/proptiter 3/pavelsavchenkov 2）。与 sweep4 口径一致。
- **GitHub**：`created:>09-29` **0 新仓**；`pushed:>05:20Z` 仅 **pieva/kaggriculture-agent** 一件（https://github.com/pieva/kaggriculture-agent ，06:17Z 推，V48 planning/ENGINE_CONTRACT 工作台，族系工作区非新基座，无 LICENSE）。
- 讨论区：743993 开源帖仍 **6 回复无新增**；无新帖（744364/744380 已录 sweep3）。**兑现仍未落地，窗口=截止后**（触发再扫）。
- kernels 增量（05:20Z→08:43Z）：新 run 仅 4 件——adilshamim8 101（06:47 重跑）、**akashbabu17/kaggriculture-autonomous-multi-agent-farming**（06:50，tiered-BFS swarm 启发式演示件，vs random 基线，低值）、haodou V91（07:02 重跑）、farhanabidtech786（08:00 重跑）；**0 新建件**。
- 榜面（08:43:29Z）：M&M&P&Q **3091.4 #1**（07:56 新交，3109→3091=收敛噪声）、DSM 2950.3 #3、Tufa 2938.8 #4；终交潮收敛噪声持续。

## 三、行为新形态（georgy 语料重算，最新切片=ep id ≥109244623）

- **池面克隆单一形态统治**：≥2600 rating 段 80%+ 提交为同一指纹 **crew11-12 / 首地 d6 / tiles 238-239 / C-M-S-T-W=31/12/33/0/163**（=48/step1009 族形态，与 sweep4"step1009 灌满天梯"互证）。
- **顶强 20 队最新提交指纹与克隆形态全部相异**（重算，median@n≥1）：
  - **#1 M&M&P&Q**（sub 56254996）：d7/256 tiles/19-17-**64**-**10**-146（草莓 64、番茄 10）
  - **DSM**（56267093）：301 tiles/**92**-14-31-13-151（胡萝卜 92）
  - **UMG**（56256813）：296/76-16-14-17-174；**Vadim**（56374127）：285/38-14-30-12-192
  - **Boey**（56309208）：315/**122**-11-17-0-156（胡萝卜 122）；**Majkel1337**（56407295）：**d3**/302/75-13-17-15-182
  - 吃白饭的大肥鱼：d5/301/96-15-18-18-154；proptiter：252/8-10-53-12-169
- **结论：≥6 种非族高分异形态**（番茄>0、tiles≥250、胡萝卜/草莓偏重、开地 d3/d5/d7 皆有）——与 48 族克隆（0 番茄/238 tiles/d6）皆异；BUY5 型（day0 买 5 牲畜）对照指纹未取得，标注为"非克隆形态"。**这些新形态全部在私有自适应顶强手里，无对应公开整件**（与"顶强=私有自适应"一致）。行为线索不构成可下载基座。

## 四、资料增量（顺带）

- **今日新策略文/教程：未找到**（讨论区 0 新帖；744364/744380/743716/741743 均已录）。
- 存量方法学分析件（窗口归属未钉，本轮顺带登记）：zhincez "ten-ppo-runs-one-fake-win-zero-real-ones"（10 次 PPO 0 真胜=RL 路线反面证据，禁区9 旁证）、dariushafshar 评分噪声四件（rating decay/last-callable trap/小样本 shakeup）、rogerrogerroger3r 量尺三件、hank0123、starkhushi 6-engine-traps、busyaprime "what-actually-wins"。
- whzy3185 reports/EXP045_EXP054_KAGGLE_FAILURE_OPTIMIZATION_20260930.md（09-30）：官方 wool-race 败录优化实录（自报）。

## 五、来源清单（均 2026-09-30 抓取）

| 来源 URL | 通道 | 读数 |
|---|---|---|
| https://www.kaggle.com/code/hesoponyo/pure-rl-agent-bc-ppo-self-play | kernels pull 解包 780KB | Transformer BC+PPO、lzma+85 权重、$81k 自报 |
| https://www.kaggle.com/code/kaitofukami/238-238-known-streams-v58-minimax-closed-loop | kernels pull 311KB | minimax closed loop、zlib+85 main.py、58/58 自报 |
| https://www.kaggle.com/code/djamilabenchikh/graph-reinforcement-learning | kernels pull 97KB | V16+GNN+DoubleDQN 残差、JSON 权重 |
| https://www.kaggle.com/code/mzcao7/kaggriculture-2476-8-peak-lightgbm-xgboost 、https://www.kaggle.com/datasets/mzcao7/kaggriculture-lightgbm-xgboost-agent | kernels pull | 树集成、Apache-2.0 |
| https://huggingface.co/datasets/KiroSamurai/kaggriculture-il 、https://github.com/Kirosamurai/kaggriculture | HF API+GitHub API | IL 权重在/仓 404 |
| https://github.com/sweeden-ttu/kaggriculture_1_37_muzero （README/artifacts/buoy_gate_report.json/dist/main.py/scripts/embed_muzero_weights.py/docs/training/*） | GitHub API+raw | MuZero 全栈、权重缺、gate 0-4 |
| https://huggingface.co/models/sweeden-ttu/kaggriculture-season-training 、/datasets/sweeden-ttu/kaggriculture-season-training 、/spaces/savadogoodgadama75/kaggriculture-agent-demo 、/datasets/ThanThoai9x/kaggriculture-rsp-decisions | HF API | 2 PNG/24 图 demo/V8 BFS/RSP 反事实数据集（登记） |
| https://github.com/diffmap/kaggicultureRL 、/THLPH/Kaggriculture_AdvancedFarmer/tree/RL_Lion 、/pranav-bot/kaggriculture （experiments/iql_value/*、src/kaggriculture/meta/cfr.py） | GitHub API+raw | 无权重/IQL×4 权重在仓 |
| https://github.com/whzy3185/kagriculture 、/pieva/kaggriculture-agent | GitHub API+raw | 族系工作台×2 |
| https://www.kaggle.com/code/akashbabu17/kaggriculture-autonomous-multi-agent-farming | kernels pull | BFS swarm 演示 |
| kernels 全量（dateRun/dateCreated 各 300）+ 顶强 36 账号 kernels list --user | CLI | 4 新 run/0 新建；顶强全 0 |
| https://www.kaggle.com/competitions/kaggriculture/leaderboard （快照 2026-09-30T08:43:29）+ topics list | CLI | 见二 |
| georgy 语料（/tmp/scan7/georgy/ agents.csv+episode_features.csv+daily_stats.csv，09-30 00:43 版） | 本地重算 | 见三 |
| [前次] 2026-09-30-kaggle-sweep4.md、2026-09-30-github-sweep4.md | 基线 | — |

## 六、限制

① hesoponyo $81k/$121k、kaitofukami 58/58、mzcao 2476.8、whzy EXP066 +1,032 全为自报未复核；② KiroSamurai 仓 404 不能断言删除（可能私有）；③ MuZero buoy 0-4 为其自评单次报告（4 局小样本），reward 0 疑似运行异常，但门槛未过事实明确；④ 存量件（hesoponyo 09-16/kaito 09-01/djamil 09-23/mzcao 09-18）为新基座角首入册，非本窗口增量；⑤ BUY5 族对照指纹未取得，"非族形态"仅对 48/step1009 克隆形态证否；⑥ 语料 replay_coverage 09-29=0.001，行为重算用的是 episodes 元数据非 replay；⑦ IQL 权重是否进入任何提交件未证；⑧ pieva/whzy 两工作台只读 README/PROVENANCE/tree，未逐文件精读；⑨ 正式池测（跑分对局）未做——本册只判"可跑性"与价值预估。
