# 2026-10-02 基座路线决策书材料（P5 神经系路线侦察：学习系/规则系/混合系三选评估）

> 任务性质：**侦察项**（registry a51050-5）——产出下战役基座路线决策书材料；不立交付项、不做训练、不算力采购、不改产线。
> 抓取时点 **2026-10-02 12:05–13:10 UTC**（截止 09-30 23:59 后 ~36h；终评窗 deadline 2026-10-14 23:59 收敛中）。通道：GitHub REST/`gh api`（r-y-ren 鉴权）+ HF API + 本地 bwrap 沙箱试跑（CarsonBurke 仓，MIT）。纪律：逐条带来源+戳；自报数字标"自报"；查不到写"未找到"；专名（仓名/赛名）一律自 `ext/postseason-github/query_slug.txt` 锚或 API JSON 程序化派生（教训定理候选"专名查询禁手键"——本会话手键单 g 走样两次踩中 404 假象，见附录限界 3）。
> 对照基线：`2026-10-02-postseason-platform-scan.md`（745073 榜首 writeup/榜面）、`2026-10-02-postseason-github-scan.md`（428 仓语料/甄别表）、`analyses/2026-10-02-a51050.md`（P5 立项）、`analyses/50-2026-10-01-fingerprint-band.md`（族天花板）、`analyses/35/36`（外挂定理）。

## 一、判据判定表（四评估面：拿到材料/未拿到）

| # | 评估面 | 判定 | 依据 |
|---|---|---|---|
| 1 | 真件可得性（msdsm 仓/权重；CarsonBurke 权重随仓否） | **拿到**（两仓现状+权重缺口定论） | 两仓均 ALIVE（derived-URL 复核 12:08Z）；msdsm NO-LICENSE+权重三路（仓内/release/HF）均**未放**；CarsonBurke MIT 但**权重/检查点不随仓**（仅 TB 训练日志走 LFS） |
| 2 | 可复现性评估（CarsonBurke 逐项 vs msdsm） | **拿到**（含沙箱实测编译/测试/parity 三读数） | CarsonBurke：cargo test **56/56 过**、pytest 抽样 **177/179**（2 失败=参考对手件未随仓分发，非代码故障）、parity oracle **2 局逐转移精确平价**；msdsm：源码树完整但 NO-LICENSE+权重缺+自报算力（17×A100+29×A30）=现状不可复现 |
| 3 | 我方评测基建对神经系件能力盘点 | **拿到**（能力面+三缺口清单） | 黑盒池测已证 3 件（godv7/V94/EXP-066）；神经件新门槛=运行时依赖供给+多文件/权重伴随装载 shim+确定性门；判定"非无障碍、无结构性障碍" |
| 4 | 混合系特别评估（修复器 vs 外挂定理+最小可行形态） | **拿到** | msdsm heuristics 源码级形态定位（约束域修复器）+外挂定理（教训定理 4 及 36 精化）比对+M1-M4 接口清单 |
| 附 | **真件强度实测**（registry 预期信号之一） | **未拿到** | 权重均未投放+msdsm NO-LICENSE——无真件可测；转 a51050-2/10-07·10-15 监控档后补 |

## 二、真件可得性（任务 1）

### 2.1 msdsm/kaggriculture-solution（#1 M&M&P&Q 官方解）

- **仓现状：ALIVE、公开**（2026-10-02 12:08Z 复核）。`users/msdsm/repos` 列表+search+direct GET 三路一致：`private=false`、created 2026-10-02T03:17:00Z、pushed 2026-10-02T03:30:47Z、★5、size 2346KB、语言 Python、分支仅 main、releases 0、tags 0。账号 06:37Z 有本仓 WatchEvent（自 star）。**更正并行件判读**：platform-scan"10:55 后 404/疑转私"极可能=拼写污染同源假象（github-scan 方法学警示已预言；本会话手键单 g 亦两次 404，derived URL 全部 200）——以 derived URL 为准，仓自 03:30 后无新 push。
- **源码树完整性（172 项，静态）**：训练/推理/打包全套在——`python/kaggriculture/`（model/training/agents/heuristics/search/observations/actions/data）、`native/engine/`（Rust 批环境 201KB 源）、`scripts/`（train_bc/train_ppo/export_policy/package_submission/evaluate）、`configs/`（10m/20m/bootstrap/deeper/smoke+agent_a/b）、`docs/`（architecture/training/training-lineage/data/operations+source-provenance.json）、Dockerfile+k8s 模板、tests/test_smoke.py。**但 README 明文："Checkpoints, replay datasets and compiled binaries are supplied separately by the user."**
- **权重投放状态：未找到**（三路核验 12:1xZ）：①仓内无任何权重/检查点文件（tree 无 .pkl/.pt/ckpt；`checkpoints.py` 只是"trusted pickle"加载器）；②releases=0、tags=0；③HF `api/models|datasets`（按 slug 锚派生查询）=1 模型（sweeden-ttu）/4 数据集，**无 msdsm 发布物**。→ 任务书"若权重已放→记录链接与许可"分支**不触发**；维持 a51050-2 二轮+10-07/10-15 监控档盯放。
- **许可：NO-LICENSE**（license=null）→ 按纪律**只登记不搬运**；本次对该仓仅限静态阅读 README/docs 公开文本+API 元数据，未搬移任何代码入产线/池测。

### 2.2 CarsonBurke/kaggriculture（自报 #12，MIT）

- **仓现状：ALIVE、公开、MIT**（12:08Z）：created 2026-08-12T19:20:30Z、pushed 2026-10-02T06:35:15Z、★1、size 4473KB、语言 Python、分支 {main, nextlat, archive/a90a578, archive/launch-8564e38f}、releases 0、tags 0。
- **权重/检查点是否随仓：否（定论）**。全树 323 项无任何 .pt/.pth/.ckpt/.safetensors/权重 blob；`.lfsconfig`+`.gitattributes` 显示 LFS **仅**承载 `results/tensorboard/**` 训练日志（~100MB，缺省 fetchexclude 不随 clone）；三个分支树逐一核验（含 archive 两支）零检查点文件。最终提交检查点只以**名字+自报分数**出现在 `results/README.md`（自报）：`ppo-overnight-1260` 2853.4 / `ppo-overnight-lr3-3379` 2793.9 / `ppo-overnight-lr3-3085` 2777.6；血统 bc→ppo-overnight(1–2535)→ppo-overnight-lr3(2536–3379)。
- 另注：`docs/solution.md`（2026-10-01 版）=生产配置长文（实体注意力+LeJEPA+WDL critic+PPO 细则），`docs/mechanics/` = 规则书，`docs/experiments/runs.md` 329KB 实验日志——**知识件随仓，力量件（权重）不随仓**。

## 三、可复现性评估（任务 2）

### 3.1 CarsonBurke（MIT 全开源）逐项

| 项 | 读数 | 判定 |
|---|---|---|
| 仓完整性 | 323 项：src 47 模块（ppo.py 270KB/rollout.py 195KB/lejepa 94KB/league 42KB…）+rust/kagg_env（core.rs 237KB 位级仿真+parity_oracle+binding_safety）+scripts 110+（train_bc/train_ppo/build_submission/validate/evaluate×6/probe×30+）+tests 120 文件+uv.lock 635KB+rust-toolchain.toml | **完整（研究+产线+测试三层俱全）** |
| 文档质量 | README（产线五步命令）、docs/solution.md（生产配置逐节）、docs/training-reference.md 93KB、mechanics 8 件规则书、experiments/proposals/reviews 分层且标注"dated records，以代码为准" | **优（超一般开源解仓）** |
| 依赖清单 | `pyproject.toml`：核心仅 `kaggle-environments==1.32.7`（与我方本地 1.32.7 同版钉）；dev=pytest+ruff；train=tensorboard+`torch>=2.13`；requires-python `>=3.11,<3.14`；Rust=nightly-2025-12-13 钉死（rust-toolchain.toml，含理由注释=编译器入 source identity）；PyO3+Rayon+ndarray（Cargo.lock 锁定） | **清单干净、双端钉版** |
| 编译门槛（实测） | 本机（16 核/22GB/无独显/Python 3.14.7）：`cargo test --release`（bwrap 沙箱、断网、CARGO_HOME 隔离）**56 passed / 0 failed**；首跑 Python 扩展构建被其**拒建**——`rust_env._verify_pinned_toolchain` 要求 rustup 可执行以核验钉版工具链（"nothing enforces rust-toolchain.toml…the identity would misstate which compiler built it"）= 溯源防线自证，PATH 补 rustup 后构建通过 | **低门槛（本机可编译）+高纪律（溯源校验）** |
| 运行门槛（实测） | uv sync（CPU torch）venv **5.8GB**（torch 2.13.0 轮子，cuda=False CPU 可跑）；pytest 抽 2 文件 **177 passed / 2 failed**——2 失败均 `opponents.py` FileNotFoundError=**参考对手件（kaito v27/boatlee v16 等公开件）按设计不随仓分发**，非代码故障；`parity_oracle.py --build --games 2 --steps 719`（bwrap）= **2 局 1,438 联合转移逐项精确平价**（"exact state/conv+structured encoding/potential/utility/reward parity"，vs 官方 kaggle_environments 引擎） | **可运行；Python 全套测试需自备参考对手件（我方对手池可替代供给）** |
| 22GB 无独显可行性 | 仿真/评测/推理链可行（README："Training needs a CUDA GPU"；推理 CPU 兼容）；**训练不可行**——其 PPO 3,379 iterations×232 局/波+BC 16 epochs 在 CUDA GPU 上"overnight"级，CPU 复算=周-月级不现实；无权重→无从跳过训练 | **评测可、训练不可；真件复现=否（权重缺）** |

### 3.2 msdsm 对比（NO-LICENSE+权重未放+自报算力）

- **复现三重墙**：①许可墙（NO-LICENSE=不可合法搬运/衍生，只可研究）；②权重墙（"supplied separately"未放，复现只能从头训练）；③算力墙（自报未复核：10M 线峰值 17×A100+29×A30、20M 线 26×A100；训练血统自报 8,290,767 局自对弈/11,922,122,946 env steps——Final A 祖先路径，`docs/training-lineage.md`）——本机 16 核/22GB/无独显**差 2-3 个量级**，CPU 不可能。
- 可借鉴面（静态、NO-LICENSE 下只研究不搬运）：JAX 实现（非 torch）+Rust 批环境 kagg-engine 0.3.24+C++17 planner（terminal_search.cpp 58.9KB）；**"Inference uses FP32 on CPU"**（自报）→ 将来若放权重，推理侧在我机可跑；configs/model/10m.json=d_model 256/12 层/8 头/FFN 1024；Agent A heuristics 开关={shed_night, shed_final, fertilize_mask, same_tile, seed_stock, care_mask, offboard_mask, search_from_day:29}——修复器形态证据（见 §五）。
- **净读**：CarsonBurke=MIT+完整+可编译可测，但**无权重→#12 强度真件不可复现**；msdsm=源码全但**三重墙→现状不可复现**。两件共同缺口都是"力量件"（权重），共同保有的是"知识件"（训练配方/架构/评测协议）。**下战役若要神经系基座，复现路线的现实形态=按公开配方重训（需 GPU 预算）或等权重投放后真件实测（评测路线），不是"拿现成权重"。**

## 四、我方评测基建对神经系件的能力盘点（任务 3）

**已证能力（黑盒池测三件先例）**：`j23._load_entry`（orderbook_r40/judge_r23.py）单文件黑盒装载=官方 last-callable 语义（全新命名空间+末 callable+exec_dir 入 sys.path），零修改直跑；判决机三级 BEATS_CEILING/COMPETITIVE/WEAK（h2h 对王座 H1/oc_c3+面板 mpx/r40/A）；中性块折 674000+i*131×双席 24 局/对、fail-closed；sim_bridge（debmalyaroy kaggsim，Apache-2.0）30 局对照认证+wall_speedup 留档；噪声地板已知（r40 自镜像 48/48 tie；块间 h2h 极差 0.125-0.22）。**实绩**：godv7 WEAK（0.25/0.083）/V94 COMPETITIVE/EXP-066 COMPETITIVE（vs_H1 0.4167）三 verdict 全落档。

**神经系件三缺口（评测"无障碍"判定=否，但无结构性障碍）**：
1. **运行时依赖供给**：本机 python3.14 无 torch/jax（实测 find_spec 均 False）；msdsm=JAX、CarsonBurke=torch。评测前需一次性 bwrap 外装 CPU 轮子（CarsonBurke 全量 venv 实测 5.8GB）——一次性基建成本，非每件成本。
2. **多文件/权重伴随装载 shim**：`_load_entry` 是单文件语义——兄弟 .py 可经 sys.path import，但命名空间无 `__file__`、cwd=裁判 cwd；神经成品（msdsm `package_submission`=main.py+参数导出+搜索库二进制；CarsonBurke `build_submission`=checkpoint+provenance tar.gz）按 `__file__`/相对路径开权重会失败。需 harness 层小适配（解包+入口映射+cwd/__file__ shim，L1 软层、评测基建非产线，不触外挂定理）。
3. **确定性门**：面板折同 seed 双席折叠要求逐 seed 行为确定；CarsonBurke 文档明言 argmax 与 temperature-1 采样"行为不同、分开报告"——若成品推理带采样则折叠失真。对策=装箱前重跑动作流哈希+发射四件套（装载/时长/确定性/体积登记）照旧加一道。
- 时长预算（预估，未实测）：10.23M Transformer FP32 CPU 推理×719 步×24 局/对×面板 4-5 对≈数小时/件；sim_bridge 提速机制在；16 核并行（workers 现 2 可调）。
- **结论**："评测神经系件"的障碍不在判决口径（已证）而在**真件不可得**（权重未放）+上述三缺口（一次性工程）。一旦 msdsm/CB 权重投放，我方黑盒池测可接（CB MIT 可直接入池；msdsm NO-LICENSE 入池与否需用户许可裁定）。

## 五、混合系路线特别评估（任务 4）

### 5.1 msdsm"规则修复器"形态=规则作用在神经输出上

- **Agent A**（README+configs）：神经提案→**置信度序动作修复**（confidence-ordered action repair）+存储规则（shed_night/shed_final）+施肥/同格/种子库存/照料/离板掩码（fertilize_mask/same_tile/seed_stock/care_mask/offboard_mask）+**末日搜索控制器**（search_from_day=29，C++ planner）。规则域=合法性/资源冲突/库存浪费（README："rules prevent resource conflicts and wasted inventory"）。
- **Agent B**：顺序掩码（sequential masks）**训练与推理同构**（"The same conditional masks during training and inference"）。
- 旁证：Farmcore（745119，榜 #4-5）同形态——21.5M 单前传 draft+6 层 corrector 改写 25% 单位目标/74% 回合市场单（自报）；"神经提案+修复器"是榜顶一族共用形态。

### 5.2 为何修复器架构不受外挂定理约束（修复器≠外挂生成器）

外挂定理两阶（我方战役实证）：**教训定理 4**（分析35/47）"想加的机制若基座内层已有，外层再实现必负；要做就做进内层"——反例族 R28 账本双计→I2 HERD/COURIER 冗余→K1 相位错峰对打（4 次同型失败）；**分析36 精化**"外挂必负=重复内生机能；补缺型外挂（X1）无恙"（inner≡outer 46/46 折全平）。修复器属 **X1 补缺族**而非定理打击的重复族，三点机制差：
1. **作用域不同**：反例外挂全在**决策域**（卖多少/何时卖/牧群编排——基座内层已有机制）重复决策→对打/双计；修复器在**约束域**（动作合法性/资源账本/库存浪费投影回可行集）+**基座盲区**（末日搜索）作业——神经策略内生**没有**硬合法性保证机制，不构成"重复内生机能"。
2. **训推同构/干预有界**：Agent B 掩码训练推理同一套=策略在训练期就适应修复器在场（修复器成为环境的一部分，无训推分布漂移）；Agent A 只按置信度修低置信/非法动作，不重决高置信动作。
3. **修复器无自有目标函数**：它是投影算子不是竞争策略；反例外挂各自带目标/时序假设（I2/K1），与基座调好的机制对打。
- 边界警示：若把修复器换成"神经再决策"（如学习式卖流生成器叠在规则基座上），即回到定理打击面——**必负**。

### 5.3 混合系最小可行形态（我方规则系+学习式组件的接口，按补缺域排序）

| # | 形态 | 补缺性质 | 承接 | 风险 |
|---|---|---|---|---|
| M1 | 学习式对手/店存**预测器**（godv7 shop_predictor 反向研究=全场唯一"预测商店库存"机制，registry bbd4f5-3 在册）→ 作为既有决策层输入特征 | 我方无预测器=真缺口（X1） | godv7 黑店机制反向研究提案 | 低（纯输入件，不产动作） |
| M2 | 学习式**终局评估/搜索引导**（对 msdsm search_from_day 29 形态；我方 latefade/终局执行=已知弱点域，分析25/42） | 基座无内生搜索=补缺 | 终局执行分析资产 | 中（接触决策域末端，须池测门） |
| M3 | 学习式**选优副尺**（小模型预测变体 h2h/终局钱，为 P4 面板 BT 提供先验，降池测成本） | 工具域 | P4 判决基建 | 低（不进产线） |
| M4 | 反例形态（**不做**）：神经磁带生成器直接替换/叠加磁带生成 | 决策域重复 | — | 按教训定理 4 判**必负** |

## 六、三路线成本-收益-风险表（任务 5）

| 面 | 学习系（BC→自对弈 PPO 换基座） | 规则系（磁带+订单簿+外挂层，H1/C_final 谱系） | 混合系（规则基座+补缺学习组件） |
|---|---|---|---|
| 数据 | episodes 语料在手（官方日更 09-30/10-01 出包+georgymarin v80+）；msdsm 自报 849+600 条 BC 轨迹可对标 | 无需 | 补缺小模型监督语料同左（万级样本够 M1/M2） |
| 算力 | **不可行**：msdsm 自报 8.29M 局/11.9B env steps+17×A100+29×A30（自报未复核）；CarsonBurke README"Training needs a CUDA GPU"；本机 16 核/22GB/无独显差 2-3 量级 | 池测 CPU 已够（现行产线） | 补缺小模型 CPU 可训（可行） |
| 许可 | msdsm NO-LICENSE（只登记不搬运）；CarsonBurke MIT 但无权重 | 自有 | 自有+MIT 件可改可衍生 |
| 复现门槛 | 权重未放→只能重训→算力墙=**现状不可复现** | 已证可复现（本战役全程自持） | 中（接口工程+双栈维护） |
| 收益上限 | #1 族 3066 带（榜面 10-02 快照）；行为指纹牛系族顶 3047（分析50） | 羊系做满≈**2625 封顶**（分析50 P5）；本战役实测峰 ~2074/终评态 1743；残余=鹅蛋线（P3 半句未测）/产线再设计（49 P4） | 介于两系：补缺域增量未知（M1 预测命中→选优/M2 终局→latefade），须池测定；不承诺 +400 带 |
| 风险 | 高（无算力/无权重/许可墙/自报不可复核） | 中低（天花板可见：台阶一级二测全负——day0 加重 missed/tomato reversed） | 中（补缺件过拟合池测；两面性=神经件不确定面收窄在可测模块） |
| 本机可行性（22GB 无独显） | 训练 **0**；权重放出后评测可接 | **全可行**（现行） | **可行**（M1-M3 CPU 级） |

## 七、决策建议 + 需用户确认点（最终选择归用户）

**建议（三选一）：混合系为下战役基座首选**——以规则系 H1/C_final 谱系为不动基座，只做补缺域学习组件（M1 预测器→M2 终局搜索评估→M3 选优副尺），逐件过池测门。依据：①学习系整线被三重墙锁死（无 GPU/无权重/许可），当前资源下期望收益=0 且不可复现（§三实测）；②规则系残余增量实测悲观（台阶一级二测全负、羊系带 2625 封顶 vs 牛系 3047 族差）；③混合系走外挂定理保护的 X1 补缺域，成本 CPU 级、每件可独立判决可回退，且与"权重放出后真件实测"路线（registry a51050-2）正交兼容——若学习系证据翻转（见确认点 2/3），可升格。
**路线次序**：混合系（主）‖ 规则系残余小项（鹅蛋线 P3 半句、产线再设计 49 P4，作为混合主线并行备选）> 学习系（挂起至权重/算力证据翻转）。

**需用户确认点**：
1. **三选一裁决**：是否采纳"混合系=规则基座+补缺域学习组件（M1→M2→M3）"的立项口径（学习系整线暂不立项）？
2. **许可裁定**：msdsm NO-LICENSE 前提下，权重若投放，**黑盒池测判决算不算"搬运"**？若判可测→真件实测入 a51050-2 二轮（只测不改、verdict 落档）；若判不可→维持只登记，学习系真件面永久缺位。
3. **算力边界**：下战役是否维持**零采购、CPU-only**？若你能提供 GPU/云预算，学习系（自训 BC 小线或 CB 配方重跑）需重开评估——本报告"学习系不可行"结论以零采购为前提。
4. **M1/M2 训练边界**：补缺组件=小模型监督学习（CPU 可训），训练数据=官方 episodes 语料——是否认可该边界（不做自对弈 RL）？
5. **本侦察项结案口径**：registry a51050-5 预期信号"决策书落档（含真件强度实测）"——决策书已落档、**真件实测缺位**（权重未投放，非本项可控）；建议按"achieved（1/2，真件实测转 a51050-2/监控档）"落分或维持 pending 至权重事件，二选一请裁。

## 附录：限界与自报声明

1. **自报未复核清单**：msdsm 17×A100+29×A30/26×A100、829 万局自对弈、11.922B env steps、"849+600 轨迹"；CarsonBurke #12 of 10,246、2853.4/2793.9/2777.6 公榜分、"placed 12th（snapshot 2026-10-02）"。终榜 ~10-14 BT 定榜后对表。
2. **许可边界**：msdsm=NO-LICENSE，本次仅静态阅读其 README/docs 公开文本+API 元数据，未搬移代码/权重入任何产线或池测；CarsonBurke=MIT，克隆件仅落 /tmp 沙箱试验（未入工程目录），试跑读数只登记数字不入库其代码。战役圈禁（D14）：本报告为唯一落档产物，试跑件全在 /tmp 临时区。
3. **测量链**：专名走样再证——本会话手键单 g 仓名两次致 curl/git 404 假象（msdsm 仓"404 震荡"判读应以此为准：derived URL 全程 200，仓无转私）；一切 URL 自 `query_slug.txt` 锚/API JSON 派生后复核。未鉴权 API 限额 60/h 曾中断一轮，gh 鉴权通道（5000/h）补足。
4. **试跑限界**：parity oracle 仅 2 局（官方门 8 局口径；读数"exact parity"方向不变）；pytest 仅抽 2 文件（179 例，2 失败=参考对手件缺）；GPU 训练无从试（无 GPU）；神经推理时长为预估未实测。
5. **未找到**：msdsm 权重/检查点发布物（仓内/release/HF 三路）；CarsonBurke 检查点（全分支）；两仓之外的独立站外拆解文（延续 10-02 github-scan 通道限界）；DECEM/Majkel/alperen 开源（延续在册未兑现名单）。

## 需登记行（本报告未改 INDEX.md/registry.jsonl，待主会话/用户登记）

1. `references/INDEX.md` 追加：
   `| 2026-10-02-baseroute-recon.md | GitHub REST/gh api：users/{msdsm,CarsonBurke}/repos+git/trees（recursive，4 分支）+releases/tags+contents README/docs/configs/pyproject/lfsconfig（12:05-12:20Z）；HF api/models|datasets（slug 锚派生）；bwrap 沙箱试跑 CarsonBurke（cargo test/pytest 抽样/parity_oracle）；[内参] analyses/35,36（外挂定理）、50（族天花板）、2026-10-02-a51050.md（P5 立项） | 2026-10-02 | P5 神经系路线侦察·基座路线决策书材料：msdsm/CarsonBurke 双仓 ALIVE 但权重均未投放（msdsm NO-LICENSE 三重墙=现状不可复现；CarsonBurke MIT 试跑 cargo 56/56+pytest 177/179+parity 2 局精确平价=基建可复现而真件缺）；评测基建三缺口（依赖供给/多文件 shim/确定性门）判定非无障碍无结构障碍；混合系修复器=约束域补缺 X1 不触外挂定理，最小可行 M1 预测器/M2 终局搜索/M3 选优副尺；三路线表+决策建议（混合系首选）+5 确认点 | 下战役蓝图基座路线三选输入（用户裁决）；a51050-2/监控档真件实测排队 |`
2. `analyses/registry.jsonl` a51050-5 行状态更新（建议，二选一待裁）：
   `{"id": "a51050-5", "status": "achieved", "scored_in": "2026-10-02-baseroute-recon.md（决策书材料落档；真件实测缺位=权重未投放，转 a51050-2/10-07·10-15 监控档）"}` 或维持 `"status": "pending"` 至权重事件后一并落分。
