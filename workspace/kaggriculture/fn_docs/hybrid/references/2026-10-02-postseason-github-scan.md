# 2026-10-02 战后开源潮收割第二轮·提前首扫——GitHub 站外兑现爆发：15 新仓+35 新推送，#1 队 M&M&P&Q 官方解落地

> 抓取时点 **2026-10-02 10:40–11:25 UTC**（截止 09-30 23:59 UTC 后 ~35h；原计划 10-07/10-15 两档，用户令提前）。通道：GitHub REST（`gh api`，r-y-ren 鉴权）+ HF API + HN Algolia / Google News RSS / Bing RSS / dev.to / crossref / Reddit / DDG / Mojeek。基线=09-30 全量 393 仓+收官 6 仓（`2026-09-30-github-sweep4.md`、`2026-10-01-postdeadline-scan.md`）。纪律：逐条带来源 URL+抓取时间戳；自报数字标"自报"；查不到写"未找到更新"。
> **方法学警示（读本篇前必读）**：赛名/仓语料真实拼写=**kaggriculture（k-a-g-g-r-i-c-u-l-t-u-r-e，双 g）**。本会话 10:43–10:55Z 一段曾以走样拼写（单 g/插字形）查询，命中的是另一 14 仓小语料，一度得出"393→14 语料塌缩、42 在册仓 404 删除潮"的**假信号**，11:00Z 前已全部推翻重查（所有名称改自 `query_slug.txt`/搜索 JSON 程序化派生）。并行件 `2026-10-02-postseason-platform-scan.md` 记 msdsm 仓"曾可见后 404"极可能同源（本扫描 11:25Z 复核该仓 ALIVE）。教训定理候选：**手键专名=测量链污染源，凡名称敏感查询必须程序化派生**。

## 一、判据判定表（四块增量：有/无+依据）

| # | 判据 | 判定 | 依据（均 2026-10-02 实抓） |
|---|---|---|---|
| 1 | GitHub 新增（新仓/新推送/榜顶账号/高质量仓/doanthuan） | **有，量级大** | `q=kaggriculture` total=**428**（vs 393 基线，+35）；`created:>2026-09-30`=**15 仓**（全在 10-01/10-02）；`pushed:>2026-09-30`=**35 仓**（至 10-02 10:38:49Z）；榜顶账号动作 **2 确证+1 相邻**（msdsm=kaggriculture-solution=M&M&P&Q #1 官方解、atsushi11o7=kaggriculture=LB #25 成员产线、flexonafft 转制件入库）；doanthuan 终态 **b3251226 维持无新 commit**；高质量仓 4 动 5 静 |
| 2 | 全网检索（拆解文/获奖感言/开源声明） | **未找到独立站外文**（受限界约束） | HN Algolia 0、Google News RSS 0、Bing RSS 0 相关（10 条模糊噪声）、dev.to 0、crossref 0；DDG captcha/Mojeek 拦截/Reddit 403/PullPush 限流——**拆解集中在 GitHub README 与 Kaggle 讨论区/notebook**（745073 M&M&P&Q 预告帖、744999 jwj1342 postmortem——平台侧由并行件覆盖） |
| 3 | HF datasets/models | **无更新** | models=1（sweeden-ttu，lastModified 2026-09-16）、datasets=4（最新 sweeden-ttu 2026-09-17）——与基线全同，未找到更新 |
| 4 | 甄别（提交件 vs 研究/转制+许可） | **命中提交件级开源 ≥10 件** | 自称 promoted/final/submitted 的：M&M&P&Q 官方解（#1）、CarsonBurke（自报 #12）、sunyuxiang136（自报银牌）、eeshsaxena（自报 #322/银牌）、egoring（自报峰 14/收官 117）、jwj1342（自报双方案已提交）、TaeyanG4（c1200+提交号）、debmalyaroy（v63+提交号）、ki-fine（R7+提交号 56713467）、romansvet（自报 #330）、Sam-wiz（final pair）、Eugenius-Lesmana（submitted）、Linus-Ma（公开底座+8 私有层）——详见 §三 |

## 二、关键读数

1. **语料**：`q=kaggriculture`（name/description/readme）total=**428**（10:57Z）vs 393（09-30 17:52Z 基线）→ **+35**。收敛口径：截止后新建 15 + 09-30 17:52 后至 24:00 新建 4（含收官 6 中的 4 件）+ 尾部未逐行的 28 仓差额——过滤查询（15/35）为单页全量，总数与分页集合（400 行）的 28 行差属排序截断非缺失。大小写变体 `kaggriculture/Kaggriculture/KAGGRICULTURE` 三查 428/428/428（GitHub 搜索大小写不敏感）。**单 g 误拼语料另 14 仓**（含 whzy3185/kagriculture——真·单 g 命名，已入册 whzy_exp066；yinwun/kagriculture 等），不并入计数。
2. **截止后新仓 15（created:>2026-09-30）**：msdsm/kaggriculture-solution（★5，M&M&P&Q 官方解）、Sam-wiz/Kaggriculture（Apache-2.0，final pair）、Freakz2z/Kaggriculture（★1，Apache-2.0，研究档案）、Linus-Ma/Kaggriculture（★1，Apache-2.0，XIAO MA 队 67 次实投）、ki-fine/kaggriculture-agent-portfolio（NOASSERTION，R7 提交号 56713467）、egoring/Kaggriculture（韩选手自报峰 14/收官 117）、eeshsaxena/kaggriculture-shepherds-ledger（自报 #322 银牌）、debmalyaroy/kaggriculture（MIT，Rust v63 提交号 56718979/56720196）、sunyuxiang136/kaggriculture-silver-agent（Apache-2.0，自报银牌单文件 5.8MB main.py）、curryrobert1111/KaggriCulture-（无 README）、Eugenius-Lesmana/kaggle-kaggriculture-public（Apache-2.0，F4+counter submitted）、aleffita/kaggriculture-agent-arena（Apache-2.0，工具平台）、romansvet/kaggriculture（Apache-2.0，自报 #330+190 负结果 build log）、EduardoTostesC/kaggriculture-agent（Apache-2.0，V035-V045 自报 5196 名）、SanTanBan/kaggriculture（NOASSERTION，InSociEUP 队全记录）。
3. **截止后新推送 35**：含上述 15 + 老仓新动作 20——**atsushi11o7/kaggriculture（LB #25 成员，10-01 11:55:38Z）**、CarsonBurke/kaggriculture（10-02 06:35，自报 #12，MIT）、TaeyanG4（10-01 02:33，终件 c1200）、jwj1342/Kaggriculture（10-01 19:14，postmortem+release 归档）、graceyunliu/kaggriculture（10-02 10:38:49Z→11:10 仍跑）、sweeden-ttu（10-02 01:12 README 改写）、the-genius-man（10-02 02:48 bot feedback）、jamesidriss（10-02 09:53，postmortem_champion）、j-mordan/shane-t-code/xantugs/Kachua7/vitalclick/Manav20032008/aleixlopezpascual/StackOverflowed512/ChaYujin-kr/PavelSavchenkov/daulettoibazar/theredbluepill-kg-v3。
4. **榜顶账号动作（③）**：**2 确证+1 相邻**。① msdsm/kaggriculture-solution=**M&M&P&Q（LB #1）官方 solution 源码**（贡献表 morim3/msdsm/BergBuch/qistripute × LB 成员 morimo/msd0110/piiiiiiiiii/qistripute，qistripute 精确同名+morim3=Kohei Morimoto≈morimo——高置信推定）；② **atsushi11o7**（LB CSV #25 同名精确）=kaggriculture 训练产线（BC→PPO→PyTorch 导出）；③ flexonafft（Igor Zharov）MLKaggleTasks 10-01 15:12 新增本赛转制件 2 ipynb（farming_score_v4 345,682B+v43_recovering_lost_harvests 351,073B）。**未兑现名单**：DECEM(zy1343930734)/majkel1337/masspeaks/mtmrs1/yaphellee/tarosqrd2/tetsu2131/shiiin9/haodou092/georgymarin/leoprovorov/alperen5252525 全部 **GitHub 无此账号或无本赛仓**（users 探测 404/无命中）；alperen Aydın 姓名搜索 21 候选抽验 8 个零命中→**头号目标 alperen 私有产线仍未公开**。M&M&P&Q 其余成员（morimo/msd0110/piiiiiiiiii/BergBuch/morim3/qistripute）gists 全 0、无第二件。
5. **doanthuan ④**：`doanthuan/kaggriculture` HEAD=**b3251226**（2026-09-30T00:41:35Z"Switch to tetsutani step1009 with a deeper sale look-ahead"）——**终态维持，无新 commit**（11:0x 复核）。
6. **高质量仓 ⑤**：graceyunliu results 分支自进化循环**仍在全速跑**（11:10:02Z commit "evolve: report 20261002-064010"；自报 population 13,777/held-out 8,379/PASS 894、本轮 held_pass 0、前沿对手 O162_THREE_SHOPS65、clone=tape_majkel1337_114061801）；sweeden-ttu 两笔 README 改写（10-02 00:47/01:12，"Trace Language theory of Agents" 宣言体，代码仍 09-27）；the-genius-man 持续自动 feedback commit（10-01 11:57→10-02 02:48）；jamesidriss 持续更新（postmortem_champion=2945 Farm v9/3+seat-1 崩溃修复自报）；elrensmin（终态 09-30 09:23）/Seyamalam（08-05 静态）/smdesai27（09-05 静态）/The-DuO-0（08-26 静态）/ashok205（2023 旧仓）**零增量**。
7. **收官 6 仓复查**：Amar-Sayed/Maro_Agent-、amrrs/kaggriculture-feel-the-agi（Apache-2.0）、meghanai28/kaggriculture_hybrid、Driw0x/Kaggriculture（Apache-2.0）四件截止后无新推送（均09-30 晚冻结）；the-genius-man 与 jamesidriss 两件截止后持续活跃。6 仓全健在。
8. **HF ③**：零新增（读数见 §一）。**开源兑现路径结论修正**：Kaggle kernels 侧兑现=0（并行件 22 账号核验）但 **GitHub 个人仓侧兑现=爆发**——榜顶解选择在 GitHub README 体系发布而非 Kaggle。

## 三、甄别表（"公开件≠提交件"纪律：身份判定+许可+池测建议）

**A. 更可能=提交件/官方解（自称 promoted/final/submitted）**

| 件（抓取 10-02） | 自报口径（未复核） | 许可 | 池测判决建议 |
|---|---|---|---|
| **msdsm/kaggriculture-solution**（★5） | M&M&P&Q #1 官方解："submitted-agent implementations"；12-block 10.23M Transformer A/B 双终件、BC→自对弈 PPO、Rust 批环境 kagg-engine 0.3.24+C++17 planner、打包产线 | **NO-LICENSE→只登记不搬运** | **最高优先**（等许可裁定后再入池）；权重/二进制"supplied separately"另发——追 release/HF/Kaggle dataset |
| CarsonBurke/kaggriculture（★1） | "final submissions placed 12th of 10,246"（自报 #12）；BC→PPO、Rust 位级对齐仿真+parity oracle、LeJEPA 世界模型、联盟 PPO | **MIT** | **高**：许可干净+技术件完整；先确认权重（.lfsconfig 指向 LFS）是否随仓 |
| sunyuxiang136/kaggriculture-silver-agent | "银牌方案完整源码"（自报；官方未发奖）；2965 Hybrid V39/V46 谱系三模态（黄金磁带+DSM DP+泊松截胡） | **Apache-2.0** | **高**：main.py 5,814,850B 单文件即交件形态，可直接入池 |
| TaeyanG4/kaggriculture-strategy-meta | 终件 `agent/c1200_final.py`（=验证版 c1064 字节同）；提交号 56719658/56722176（后者自报 10-01 交——**晚于截止，存疑待核**） | **Apache-2.0** | **高**：单文件终件可直接入池 |
| eeshsaxena/kaggriculture-shepherds-ledger | "322nd of 10,246（top 3.1%），Silver medal"（自报）；Shepherd's Ledger 磁带底盘+自研层；FINDINGS/WRITEUP/KAGGLE_WRITEUP 三份拆解 | NO-LICENSE | 中（只登记；拆解文本可引用） |
| egoring/Kaggriculture | 峰 14（2,819，09-02）/收官 117（2,505.9）（自报）；对手族路由 466 局 438 胜、WASH 洗麦、oracle 对手模型 719/719 复现、FIXORD、录像带流水线 97.3%+G0-G6 门 | NO-LICENSE | 中（只登记；tape_build/tape_gates 工具链与 Docker 镜像 ghcr.io/egoring/… 有情报价值） |
| jwj1342/Kaggriculture（★1） | "RL is all you need"队；两终方案 Mixed deferred/Wool priority **均已提交**；postmortem notebook+discussion/744999+release postmortem-2026-10-01 | NO-LICENSE | 中（只登记；复盘文本收割归平台轨） |
| debmalyaroy/kaggriculture（新仓，旧仓-simulation 已 404） | Rust "route+layers" v63.14/16 提交号 56718979/56720196（自报 41W12L1D/53W11L） | **MIT** | 中高（Rust 重件；底盘=公开 route+修复 chassis+反应层） |
| ki-fine/kaggriculture-agent-portfolio | 三人团队整合者；R7 提交号 56713467（自报平台已收）；复盘含"AI 写入未经授权否决规则"教训 | NOASSERTION | 中（先核 LICENSE 实文） |
| romansvet/kaggriculture | "peaked 2,858 / 收官 2,230（rank 330 provisional）"（自报）；190 负结果 build log+writeup 2026-10-01；7.7k 浮点 ES 策略+numpy/C 提交件 | **Apache-2.0** | 中高（提交件在 `submission/`，weights 随仓） |
| Sam-wiz/Kaggriculture | final pair=subAB_m30b（Harvest-V78 磁带+BRX2 卖单层）+subAC_v8（r34l-rudr44 市场簿族）；107 提交件全存档 | **Apache-2.0** | 中（双底盘对冲；r34l 族=榜顶 Rudra-r34l 名族外证） |
| Eugenius-Lesmana/kaggle-kaggriculture-public | "Finished, submitted"：F4+counter+race+wheat round-trip+look-ahead10+snipe | **Apache-2.0** | 中 |
| Linus-Ma/Kaggriculture（★1） | XIAO MA 队 67 次实投；**公开底座+8 私有层**（公开件≠提交件范式） | **Apache-2.0** | 低（私有层缺失=公开件不等于交件） |
| atsushi11o7/kaggriculture（LB #25） | BC→PPO→PyTorch 导出训练产线（submission/model_weights.pt 构建期导出，仓内未见权重） | NO-LICENSE | 中（只登记；产线口径=10M 级 BC+PPO，与 #1 同构互证） |
| SanTanBan/kaggriculture | InSociEUP 队（自报 #1704/1620.9 provisional）；终两席=tetsutani Step1009+cha22 **公开件字节原样**；+Claude Code 协作全轨迹 | NOASSERTION | 低（无自有终件；"公开件当提交"生态位再证） |

**B. 研究工具/转制/杂项**（不入池或仅工具借用）：aleffita/kaggriculture-agent-arena（LiteRT-LM 多 GPU 竞技平台，Apache-2.0）、theredbluepill/kg-v3（MIT，Orbit Wars RL 库改编）、graceyunliu（自进化研究实验室）、sweeden-ttu（AGI 宣言体+MuZero 栈，权重缺）、the-genius-man（Optuna+自对弈联盟研究件）、FlexonaFFt/MLKaggleTasks（转制仓：god's-mode v4 与 ahmed V43 两 ipynb）、EduardoTostesC/j-mordan/PavelSavchenkov/Kachua7/vitalclick/xantugs/StackOverflowed512/ChaYujin-kr/curryrobert1111/Manav20032008/shane-t-code/aleixlopezpascual/daulettoibazar/Freakz2z（研究档案/中低分复盘/工具箱，详见 ext/readmes/）。

## 四、异常与限界

1. **拼写陷阱（本次最大测量链事故+教训）**：10:43–10:55Z 以走样拼写查询，假信号链=「语料 393→14 塌缩→42/52 在册仓 404→删除潮（含 doanthuan/graceyunliu/Seyamalam 等）→仓在用户列表可见但 GET 404 的'实时删除'怪象」。11:00Z 以 `query_slug.txt`+搜索 JSON 程序化派生名称后全部推翻：**37/39 在册仓健在**（缺的2 个=早已 404 的 Kirosamurai/XZDang13）、doanthuan 终态未变、Seyamalam/elrensmin 静态未删。并行件对 msdsm 仓的 404 判读建议同源复查。**建议入教训定理：专名查询禁手键**。
2. **全网通道限界**：DDG html/lite=captcha（c21b）、Bing HTML=反爬（微软首页噪声）、Mojeek=拦截、Reddit JSON/RSS=403、PullPush=限流、`search/gists` 端点=404（弃用）→"未找到独立站外拆解文"是在**可见通道**（HN/Google News/Bing RSS/dev.to/crossref）内成立的弱结论，非全网实证；X/Twitter、Medium 未能直接抓取。
3. **语料截断**：428 语料按 updated 排序仅收前 400 行逐行（尾部 28 仓=最不活跃，风险低）；15/35 过滤查询为单页全量。单 g 误拼 14 仓未逐行深挖（无榜顶名，边际）。
4. **自报数字全部未复核**：各仓名次/奖牌（银牌、#12、#322、#117、#330、#14 等）均为自报；官方口径=两周对局史+BT 单次定榜，**终榜 ~10-15 出**（jamesidriss/SanTanBan/egoring 自述一致；其中 jamesidriss 称"deadline extended to 2026-10-14"指收敛/评测窗，与并行件 731587 官方口径需并读）。TaeyanG4 自报 10-01 有提交号=晚于截止，待平台侧核。
5. **身份推定标注**：msdsm 仓=M&M&P&Q 为**高置信推定**（qistripute 精确同名+四人贡献表对 LB 四成员+10M/20M 双模型线规模吻合），非官宣自证；atsushi11o7=#25 为 LB CSV 同名精确命中。
6. **并行件交叉互证**（`2026-10-02-postseason-platform-scan.md`）：其 745073 帖 M&M&P&Q 预告（自报 BC+自对弈 PPO 10M+规则补丁/829 万局）与本扫描 msdsm README（100M env steps 量级、A/B 双件）同源互证=**#1 队真源**；其"kernel 侧开源 0"与本扫描"GitHub 侧兑现爆发"合起来=兑现路径结论（§二.8）。

## 五、建议（可行动项分级）

### P0 [立即·高] 池测判决排队（许可干净者先行）
- 入池序：**sunyuxiang136 main.py**（Apache-2.0 单文件交件形态，自报银牌）→ **TaeyanG4 c1200_final.py**（Apache-2.0 字节级交件）→ **CarsonBurke**（MIT 自报 #12，先确认权重）→ **romansvet submission/**（Apache-2.0，theta.npy 随仓）→ debmalyaroy v63（MIT，Rust 重件殿后）。全部按"自报≠可迁移"惯例走 bwrap 池测，判决只认本池实测。
- 无许可件（msdsm/jwj1342/egoring/eeshsaxena/atsushi11o7/ChaYujin-kr 等）**只登记不搬运**；若要测 #1 件，走用户裁决/上游许可申请。
- 分流：流程级（池测判据沿用六判据；属战后复盘轨）。

### P1 [高] #1 队官方解技术拆解进复盘轨
- msdsm README 全套 docs（training-lineage/data/architecture/training/source-provenance）=首个榜顶产线级口径（10M/20M 假设检验、BC→PPO 交替、KL 参考、Net2Net 加深、A=搜索修复控制器/B=顺序掩码全神经）；与我方 H1/C_final 谱系、haodou V94、tetsutani 磁带系做终局对标。
- 注意权重缺口："Checkpoints…supplied separately"→追 release/HF/Kaggle dataset 后续投放（P2 监控项）。
- 分流：流程级（kb 跑批+复盘轨）。

### P2 [高] 开源潮监控排程刷新（10-07/10-15 二档保留）
- 盯：① msdsm 权重/数据集投放；② DECEM(zy1343930734)/majkel1337 两大强是否开 GitHub/发 writeup（截止 10-02 均无账号）；③ alperen5252525 私有产线（头号目标，仍无公开动作）；④ graceyunliu 自进化循环 PASS 数是否破千；⑤ 10-15 官方终榜公布日的获奖感言潮（预期兑现高峰）。
- 分流：流程级。

### P3 [中] 复盘文本收割（平台轨协作）
- eeshsaxena FINDINGS/WRITEUP、jwj1342 postmortem notebook+744999、romansvet 190 负结果 build log、Linus-Ma 67 实投方法论、ki-fine 赛后反思（AI 越权教训）——均为可引用拆解文本，建议随复盘轨入 kb（带来源+自报标注）。
- 分流：流程级。

### P4 [中] 测量链纪律升级（本案特有）
- 战役级约定：**专名（赛名/队名/仓名/handle）查询一律自文件/上游 JSON 派生，禁手键**；扫描脚本加拼写锚（`query_slug.txt` 已存 ext/postseason-github/）。
- 分流：流程级（可进 guard/verify 惯例）。

## 六、来源清单（均 2026-10-02 10:40–11:25 UTC 抓取，URL 内赛名拼写以 ext/query_slug.txt 为准）

| # | 来源 URL / 端点 | 通道 | 版本/戳 |
|---|---|---|---|
| G1 | api.github.com/search/repositories?q=kaggriculture（p1-p4，updated desc） | REST | 10:57Z；total=428，收 400 行 |
| G2 | 同上 + pushed:>2026-09-30 / created:>2026-09-30 | REST | 10:57Z；35 仓/15 仓 |
| G3 | 同上 q=Kaggriculture/KAGGRICULTURE 大小写变体 | REST | 11:08Z；428/428/428 |
| G4 | repos/doanthuan/kaggriculture/commits | REST | 11:0xZ；HEAD b3251226 @2026-09-30T00:41:35Z |
| G5 | repos/{msdsm/kaggriculture-solution, CarsonBurke/kaggriculture, atsushi11o7/kaggriculture, sunyuxiang136/kaggriculture-silver-agent, …}/readme | REST raw | 10:58–11:05Z；35 件 README 全文 |
| G6 | repos/{TaeyanG4,egoring,eeshsaxena,jwj1342,debmalyaroy,romansvet,Sam-wiz,ki-fine,msdsm,atsushi11o7,…}/contents | REST | 11:1xZ |
| G7 | users/{64 目标 handle}+repos+gists（自 LB CSV+文档派生：majkel1337/zy1343930734/masspeaks/mtmrs1/yaphellee/atsushi11o7/morim3/msdsm/BergBuch/qistripute/alperen5252525/haodou092/shiiin9/tarosqrd2/georgymarin/leoprovorov/flexonafft/whzy3185/…） | REST | 10:56–11:02Z |
| G8 | search/users?q=alperen+aydin（21 候选）+ 8 候选 repos 过滤 | REST | 11:1xZ；零命中 |
| G9 | repos/{graceyunliu/kaggriculture}commits?sha=results + contents/evolve/reports/latest.md?ref=results | REST raw | 11:10Z；report 20261002-064010（自报） |
| G10 | repos/FlexonaFFt/MLKaggleTasks（contents+commits） | REST | 11:1xZ；public-comp/kaggriculture/ 2 ipynb |
| G11 | 在册仓存在性普查 39 名（repo_census2.txt 文档派生） | REST | 11:09Z；37 ALIVE/2 GONE（Kirosamurai、XZDang13 早已 404） |
| H1 | huggingface.co/api/models|datasets?search=kaggriculture | REST | 11:03Z；1/4，最新 09-17 |
| W1 | hn.algolia.com/api/v1/search_by_date（story+comment） | REST | 11:04Z；0 相关 |
| W2 | news.google.com/rss/search?q=%22kaggriculture%22 | RSS | 11:14Z；0 |
| W3 | bing.com/search?q=%22kaggriculture%22&format=rss + html 双查 | web | 11:08–11:14Z；RSS 10 条模糊噪声、HTML 反爬 |
| W4 | html.duckduckgo.com + lite.duckduckgo.com、mojeek.com | web | 11:07–11:15Z；captcha c21b/拦截 |
| W5 | reddit.com/r/kaggle/search.rss + .json、api.pullpush.io | web | 11:12–11:15Z；403/限流 |
| W6 | dev.to/search/feed、api.crossref.org | REST | 11:15Z；0/0 |
| X1 | [并行件] `2026-10-02-postseason-platform-scan.md`（745073/744999 帖、榜面、22 账号 kernel 核验） | 交叉互证 | 10:39–10:58Z |
| [前次] | `2026-09-30-github-sweep4.md`、`2026-10-01-postdeadline-scan.md`（393 仓基线+收官 6 仓+开源兑现 0 断言） | — | 对比基线 |
