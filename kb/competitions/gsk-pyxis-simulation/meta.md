---
id: gsk-pyxis-simulation
name: "GSK Pyxis Portfolio Challenge（GSK 药企研发组合 agent 对抗赛）"
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: upcoming
award_levels:
  - name: "1st place"
    count_or_ratio: "$15,000"
    note: gsk.ai 官方页 Prizes 节直抓（来源[4]）；Kaggle Prizes 页未上线未交叉验证，待开赛复核
  - name: "2nd place"
    count_or_ratio: "$12,000"
    note: 同上（来源[4]）
  - name: "3rd place"
    count_or_ratio: "$9,000"
    note: 同上（来源[4]）
  - name: "4th place"
    count_or_ratio: "$8,000"
    note: 同上（来源[4]）
  - name: "5th place"
    count_or_ratio: "$6,000"
    note: 同上（来源[4]）；monetary 五档合计 $50,000（撰写时算术汇总，非页面原文口径）
  - name: "Non-monetary"
    note: "An invitation to co-author the post-competition proceedings paper（赛后论文集共同作者邀请，gsk.ai 官方页直抓，来源[4]）——对学术型队伍是奖金之外的差异化激励"
organizer: "Sponsor：GSK plc（葛兰素史克，via gsk.ai / GSK.ai 团队）；Kaggle 平台承办（Simulation 类，赛 slug gsk-simulation）"
key_dates:
  "2026开赛（官方公告）":
    date: "2026-09-29"
    verified: true
    note: "gsk.ai 官方页 Timeline 原文 '29 September 2026: Competition opens'（来源[4]）。⚠ 截至 2026-10-05 Kaggle 赛站仍 404、官方 CLI API 检索无此赛（来源[5]）——公告开赛日已过 6 天而 Kaggle 未上线，实际开赛延期，待复核"
  "entry_deadline（官方公告）":
    date: "2027-01-04"
    verified: true
    note: "gsk.ai Timeline 原文 '4 January 2027: Entry deadline (rules must be accepted to compete) and team merger deadline'（来源[4]）；Kaggle 页上线后以赛站 Timeline 复核"
  "final_submission_deadline（官方公告）":
    date: "2027-01-11"
    verified: true
    note: "gsk.ai Timeline 原文 '11 January 2027: Final submission deadline'（来源[4]）；同上待复核"
  "ladder_convergence（官方公告描述）":
    date: "2027-01-11 终交后约两周，随后最终 Bradley-Terry 锦标赛定榜"
    verified: false
    note: "gsk.ai 原文 'Games will continue running for roughly two weeks after the deadline to reduce rating uncertainty, followed by a final Bradley-Terry tournament to produce the final leaderboard'（来源[4]）；与 Kaggle 仿真赛惯例（kaggriculture 同款）一致，具体定榜日待官方细化"
deliverables:
  - "自主 AI agent：main.py 含 agent(observation, configuration) 函数置于压缩包根（单文件直接提交，多文件打 tar.gz，亦支持 Notebook 提交），经 Kaggle CLI 提交至 gsk-simulation（来源[2][3]）"
  - "引擎与提交链路已先行可得：pip install -U kaggle-environments 后 make(\"pyxis\") 本地对战内置 agent（knapsack/random/do_nothing）调试，kaggle competitions submit 提交（来源[2][3]）"
  - "赛题定位（gsk.ai 官方口径）：'Build an AI agent that manages a simulated pharmaceutical R&D portfolio of drug programs'——AI agent 即交付物本体（来源[4]）"
ai_policy:
  summary: >-
    截至 2026-10-05 实抓的全部可用官方材料（gsk.ai 挑战页全文、kaggle-environments 仓库 pyxis 环境三文档 README/AGENTS/QUICKSTART）均未见任何 AI 工具使用限制条款；赛题目标本身就是"构建 AI agent"（AI 使用是赛题本体而非受限项），官方页明示 "Full competition rules, eligibility requirements and terms are available via the Kaggle competition page"——正式规则与资格条款以尚未上线的 Kaggle 赛站为准，故 AI/资格条款标注"待开赛核验"。已可确认的相邻约束：①隐私——参赛即向 GSK 提供注册用户名与邮箱，用于按 Official Rules 联络发奖（gsk.ai 隐私节）；②仿真赛引擎侧已知红线（引擎 README，非 AI 条款）：非法动作/异常/超时即判负（forfeit），种子对 agent 不可见。
  url: "https://gsk.ai/pyxis-portfolio-challenge"
  checked: "2026-10-05"
credibility: 官网
last_verified: "2026-10-05"
sources:
  - url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/pyxis/README.md"
    title: "pyxis 环境官方 README（Kaggle/kaggle-environments master 分支；赛制规则参考全文：2 人对抗/100 步/£5B/管线/PTRS/共享市场/BD 拍卖/临床站点/营销/计分；首行明示 environment=pyxis, competition=gsk-simulation。快照 kb/raw/gsk-pyxis-simulation/pyxis-README.md）"
    accessed: "2026-10-05"
  - url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/pyxis/AGENTS.md"
    title: "pyxis 官方 AGENTS.md（agent 开发与提交全流程：obs 解码/动作头/非法动作判负/本地测试/Kaggle CLI 提交与 episodes/replays/logs；快照 pyxis-AGENTS.md）"
    accessed: "2026-10-05"
  - url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/pyxis/QUICKSTART.md"
    title: "pyxis 官方 QUICKSTART.md（三步提交路径与 gsk-simulation 赛站入口；快照 pyxis-QUICKSTART.md）"
    accessed: "2026-10-05"
  - url: "https://gsk.ai/pyxis-portfolio-challenge"
    title: "GSK 官方挑战页（JS 渲染 SPA，正文内嵌于 HTML 的富文本 JSON 块，trafilatura 返回 None 后实体反转义恢复；Timeline/Prizes/Official Rules/隐私条款全文；快照 kb/raw/gsk-pyxis-simulation/gsk-ai-pyxis-page.html + 抽取视图 gsk-ai-pyxis-page.extract.md）"
    accessed: "2026-10-05"
  - url: "https://www.kaggle.com/competitions/gsk-simulation"
    title: "Kaggle 赛站存在性复核：HTTP 404（2026-10-05 curl -L 直测，与主会话同日预核验一致）；另以 Kaggle 官方 CLI（已认证凭据）'kaggle competitions list -s gsk' 与 '-s pyxis' 双查询均返回 'No competitions found'——Kaggle 侧截至该日未上线（CLI 查询无公开匿名 URL，方法记录于此）"
    accessed: "2026-10-05"
---

# GSK Pyxis Portfolio Challenge（gsk-pyxis-simulation）— meta

> 本文事实均来自 frontmatter `sources` 所列页面于 **2026-10-05** 的实抓；信源等级：GSK 官方页（gsk.ai）与 Kaggle 官方仓库（kaggle-environments）均为官网/官方一级信源。**本条目为"未上线候选"条目**：Kaggle 赛站截至核验日 404，全部赛程数字为赞助方公告口径，未经 Kaggle 赛站二次确认（各字段 note 内逐条标注）。

## 状态判定（本条目核心结论）

- **引擎先行、赛站未上线的仿真赛候选**：kaggle-environments 官方仓库 master 已收录环境 `pyxis`，其 README 首行明示 "The Kaggle environment is `pyxis`; the competition is `gsk-simulation`"（来源[1]）；但赛站 https://www.kaggle.com/competitions/gsk-simulation 于 2026-10-05 返回 HTTP 404，且官方 CLI API 双查询（-s gsk / -s pyxis）均无此赛（来源[5]）。
- **与既往模式一致**：环境先入 wheel、赛站后上线是 Kaggle 仿真赛临近开赛的既往模式（kaggriculture 同款）；本赛特殊点在于**赞助方公告的开赛日（2026-09-29）已过 6 天而赛站仍未上线**——存在发布延期，`status: upcoming` 据实保留，建议开赛后立即回填核验。
- 修正主会话预核验口径一处：任务包原判"开赛时间未知、奖金未知"——实抓 gsk.ai 官方页（JS 页正文内嵌于 HTML，需实体反转义提取）后**时间线与奖金均已官方公布**（见下两节）；"尚未上线"判断本身经双通道复核成立。

## 赛事概况

- 主办：GSK plc（葛兰素史克）赞助，经 GSK.ai 团队运营 gsk.ai 挑战页；Kaggle 平台承办（来源[4][1]）。GSK 自述动机：资产管理优化与竞争性药物研发此前被分开研究——"组合模型忽略竞争者，博弈论模型只能从历史数据估计行为"；本赛是三者（组合优化 × 竞争博弈 × 多智能体仿真基准）的首个结合，问题背景为 $300B/年的产业（来源[4]）。
- 赛题：两名 agent 对抗经营模拟药企研发组合——决定资助/继续/放弃哪些药物项目，与对手在同一批资产与市场上竞争；破产立即判负，存活则按净现金流（NCF）定胜负，资助项目约 80% 会失败（来源[4][1]）。
- 可玩入口：https://gsk.ai/pyxis-portfolio-challenge（可对战内置 baseline agent、回放对局，/play/ 子页 HTTP 200）；replay.json 可上传该页可视化（来源[1][4]）。
- 评测机制（官方公告）：终交后天梯继续对局约两周以降低评级方差，随后跑最终 **Bradley-Terry 锦标赛**定榜（来源[4]）——与 kaggriculture 完全同款，Simulation 赛无 Private Leaderboard 的平台惯例预计沿用（推断，待赛站 rules 核验）。

## 赛制与规则（pyxis 引擎 README 全文直抓，来源[1]）

**基本盘**：2 人零和对抗；100 个行动步（开局前市场先以 do-nothing 策略空转 500 步并重置时钟，起手即成熟市场）；起始现金 **£5B**（全 GBP 计价）；最多 40 个资产槽（新资产按均值回归过程到达，均衡 ~35）；在售收入仅 **35%** 计入现金（`reinvestment_percentage`），成本全额扣除。

**资产管线**：Phase 1 → 2 → 3 → 监管审批 → 上市；约 **80% 资产失败**（attrition）；审批需 1-3 步、成功率 85-95%、申报费 £50M；上市后收入持续至专利到期。**PTRS（成功概率）隐藏**：每资产自带一次免费噪声读数（单样本平均绝对误差 ~21%），试验结果按真实值掷骰；可购更多读数（精度加权均值，误差 ~1/√N 收缩；成本 = 0.05 × 该试验剩余成本，单步第 1-5 次按 1×/2×/4×/7×/12× 累计计价；43 个可读槽 = 40 资产 + 3 BD）。

**共享市场**：双方药物在同适应症竞争，收入份额按 `1/n^α` 惩罚——首位进入者只受 ~15% 惩罚，至第 4 位进入者升至满额 **α = 2.0**；先发独占与先发奖励被禁用。**情报泄露**：对手管线推进阶段时以 20%/50%/70% 概率（Phase 1→2 / 2→3 / 3→审批）向你推送 alert；营销花费亦会泄露（BE 每次花费 0.8 概率泄露，只泄露 TA/适应症/次数不含金额）。

**BD 资产拍卖**：BD 资产按 Poisson λ=1.3 随机到达（至多 3 槽），预推进至 Phase 1/2/3；未售出停留至多 3 步；一价密封投标（£M，0 弃权，上限 £100B），**无支付能力检查——赢标价超出现金即破产**。

**临床站点**：并行试验硬上限，起始 4 个；`upgrade` 购站按 £500M 起的 Fibonacci 曲线计价（1×/1×/2×/3×/5×…），建站需 2 步；第 10 步起每 20 步拍卖一个即用站点（同为一价密封标，无支付能力检查）。

**营销双通道**：DC（按适应症的需求创造，+0.10 共享需求乘子，成本锚定全池最大药物 0.035×，乘子 ~3 步半衰期衰减回 1.0）；BE（按资产的品牌投入，+0.25 brand_score，对小药杠杆最大，成本 0.0175×该药自身 max_revenue，仅上市药物可用）。

**回合顺序与破产**：每步先结算 BD/站点拍卖，再按"站点建成→计提试验成本→购站→开新试验/弃置→读数计费→收收入→计营销→试验结算→新资产到达"推进，最后市场更新。**破产（现金 < 0）在每个扣费后即时检查**——试验成本与读数先于收入扣费，故存在"本可被收入覆盖的破产"；破产方后续动作被忽略；双双破产则存活更久者胜。

**计分**：NCF = 终局现金 − 初始现金（= Σ(0.35×收入 − 成本)，含拍卖支出）；奖励 1.0/0.5/0.0（胜/平/负）。**非法动作、异常、超时（actTimeout 60s/步，runTimeout 1200s/局）即判负**（status INVALID/ERROR/TIMEOUT，对手得 1.0）。

**观测与动作**：观测仅含己方组合（对手信息只经 alert 到达）；`obs` 为 1534 维浮点（Globals 6 + 资产 40×29 + BD 3×18 + 适应症市场 9×6 + 告警 20×13）+ `actionMask` 离散动作头掩码 + cash/enpv/bankrupt/step/remainingOverageTime。动作头 7 个：investments(40×3)、bd_bids(3)、ptrs_research(43×11)、demand_creation(9×2)、brand_equity(40×2)、upgrade(1)、site_bid(1)；缺省头补 no-op（`{}` 即合法 pass）；掩码可行性为一阶判断（逐项独立判费，组合仍可能超支）；两个出价头不设掩码，**动作空间自身即校验器**——长度/类型/越界（含负值与 >£100B）均判负。

**内置 agent 与配置**：`knapsack`（每步解 0/1 背包的预算优化启发式）、`random`（无种子，不可复现）、`do_nothing`；episodeSteps 默认 1000（框架步上限，对局 101 步封顶）；seed 对 agent 擦除（存 env.info["seed"]）。

## 工程与提交链路（AGENTS.md / QUICKSTART.md 直抓，来源[2][3]）

- 本地：`pip install -U kaggle-environments`（任何含 pyxis 的近期版本）→ `make("pyxis", configuration={"seed": 42}, debug=True)` → `env.run([agent, "knapsack"])`；整局 101 步对 do_nothing 约 15 秒；`env.render(mode="ipython")` 可视化，`env.toJSON()` 导出 replay。
- **引擎训练 API 随环境捆绑**（importable，非 Kaggle 计分路径）：PettingZoo `ParallelEnv`（agent id `pharma_0/1`）、`make_multi_agent_train_env(flatten_obs=False)` 出字典观测、`.train([None, "knapsack"])` 出 gym.Env 单代理训练循环（掩码兼容 MaskablePPO）、`evaluate(...)` 批量对战（每 seed 换座双打）、指标三组（PerEvaluation/PerEpisode/PerStep：胜率/NCF/破产率等，`config.yaml` 列全量）——**本地 RL 自博弈训练栈官方开箱即用**。
- obs 解码捷径：提交内可 import 捆绑引擎，用 `unflatten_to_dict_obs` 把 1534 维向量还原为字典视图（cash/assets/bd_market/indication_markets/alerts），解码器实例只建一次复用；临床站点全局量需直读 `obs[2:6]`。
- 提交：根目录 `main.py` 含 `agent` 函数；单文件直接 `-f main.py`，多文件打 tar.gz；`kaggle competitions submit gsk-simulation`；赛前列表验证 `kaggle competitions list -s "gsk-simulation"`；赛后 `episodes`/`replay`/`logs` 取对局与调试日志；`leaderboard gsk-simulation -s` 看榜。
- 参赛前置动作：在 Kaggle 赛站点 "Join Competition" 接受规则（QUICKSTART 明示）。

## 时间线与奖金（全部为 gsk.ai 公告口径，Kaggle 侧待上线复核）

| 节点 | 公告日 | 状态 |
|---|---|---|
| Competition opens | 2026-09-29 | **公告已过而 Kaggle 未上线（延期）** |
| Entry deadline（规则接受 + 组队合并截止） | 2027-01-04 | 待上线复核 |
| Final submission deadline | 2027-01-11 | 待上线复核 |
| 终局定榜 | 终交后约两周对局 + 最终 Bradley-Terry 锦标赛 | 描述性，无具体日 |

奖金：1st $15,000 / 2nd $12,000 / 3rd $9,000 / 4th $8,000 / 5th $6,000（合计 $50,000）；另设非现金奖：赛后论文集（post-competition proceedings paper）共同作者邀请——对学术型队伍是显著差异化激励（来源[4]）。

## AI 政策与合规

- 实抓材料（gsk.ai 全文 + 引擎三文档）**未见任何 AI 工具限制条款**；赛题本体即"构建 AI agent"。正式规则/资格条款官方明示以 Kaggle 赛站为准，该站未上线 → **待开赛核验**（frontmatter ai_policy）。
- 已知相邻约束：参赛即向 GSK 提供注册用户名/邮箱（隐私节）；引擎层判负红线（非法动作/异常/超时/超额出价）与 seed 擦除（防 seed 探测）是工程侧合规点（来源[1][2][4]）。

## 待办（开赛后触发）

- [ ] **上线核验（最高优先）**：赛站 404 → 上线后立即复核 rules/timeline/prizes/evaluation 四页（ListPages API 路径），回填 key_dates 的 Kaggle 侧 verified 双源确认，核销"公告已过未上线"异常。
- [ ] rules 页 AI/资格/组队（1 人还是多人、team merger 细则）条款全文核验，消除 ai_policy "待开赛核验"。
- [ ] Simulation 赛平台惯例核验：无 Private Leaderboard、每日提交次数上限、validation episode 预检等（kaggriculture 同款假设逐条证实/证伪）。
- [ ] winners 分片：本赛为首届且未开赛，无历届获奖作品可构——winners/ 目录不建；开赛后按 meta.award_levels 前两级（1st/2nd）深构终榜 top 作品。
- [ ] gsk.ai /play/ 对战内置 baseline 的强度手感实测（可作快循环热身基线），非本分片职责，转交战役层。
