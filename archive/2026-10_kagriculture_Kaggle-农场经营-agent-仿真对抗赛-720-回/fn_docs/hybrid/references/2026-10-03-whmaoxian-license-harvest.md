# WHmaoxian123 归档仓：许可裁定材料与选择性收割（dff20b-3）

- 日期：2026-10-03（抓取窗口 ~06:05–06:5x UTC；比赛截止后 ~3 天，官方终评窗至 10-14）
- 对象：`WHmaoxian123/kaggriculture`（owner/repo 程序化派生自 monitor-round2-github 报告正文正则，仓元数据 `full_name` 复核；10-01T02:53:41Z 建、pushed_at 10-01T03:25:24Z、单提交仓）
- 任务：许可普查 → 裁定书（建议案）→ 选择性收割（≤3G）→ 候选初筛（12-fold 快筛）→ candidate_v8_dsm ↔ DSM 队关系探查
- 原始拉取物：`ext/whmaoxian_harvest/`（provenance.md + SHA256SUMS.txt，28 件）；快筛证据：`fn_work/legacy_software/kaggle_simulations/orderbook_whmx_lab/evidence/whmx_screen.json`
- 纪律：实抓带来源+时间戳；自报标"自报"；不做在线提交；第三方代码仅 bwrap 沙箱内执行；专名零手键

## 0. 判据判定表

| 判据 | 状态 | 一句话结论 |
|---|---|---|
| 许可普查 | **完成** | 混态确证：根级无许可+根 README 明言"不添加额外授权"；逐件 Apache-2.0 覆盖仅 submissions 18/20 目录（155/6,997 文件=2.2%、3.2% 字节）；检查点（7 个工作区快照 zip ~666MB）与备份差集（5,438 文件 4.19GB）**零覆盖** |
| 选择性收割 | **完成** | 源码树 clone（HEAD ed63c7f6，40/40 sha 抽验）+ Release 5 小件 + ZIP64 字节区间取样（检查点 3 件+官方 replay 5 件，8/8 manifest sha 一致）；总量 1.8G ≤ 3G；2.15GB 分卷未整下 |
| 候选初筛 | **完成** | 3 件终件候选（r3/r4_2/r5）全部装载成功、12-fold×4 面板全跑完：三件全档 **BEATS_CEILING**（vs 王座 H1 h2h 0.75/0.8333/0.8333），288 面板局+90 认证局零红局 |
| DSM 关系探查 | **完成** | candidate_v8_dsm=DSM 公开 replay 条件化路由代理（内嵌恰好 24 局 DSM episode 动作带、0 局 Vadim），档案自述三重否认私有码；DSM=终榜第 3（2945.5）；无 DSM 私码/成员接触证据（只登记） |

（verdict 数值以 §4 证据 JSON 为准）

## 1. 许可普查（裁定书材料）

### 1.1 仓结构（git tree，7,481 条目=6,997 blob+484 树，未截断）

| 组 | 文件数 | 字节 | 许可状态 |
|---|---:|---:|---|
| `project/research/**` | 5,620 | 1,475,317,432 | 无任何 LICENSE 覆盖（含 v10_top10 2,661 文件、claude_20260929 634 文件、`.training/` 整个 vendored Python venv） |
| `project/results/**` | 460 | 14,333,013 | 无 |
| `project/external/**` | 366 | 33,448,360 | 2 个子目录有 Apache-2.0 LICENSE.txt（fieldcraft、arlene_shop）+NOTICE |
| `project/submissions/**` | 220 | 53,989,147 | **18/20 候选目录带 Apache-2.0 LICENSE.txt+NOTICE.txt**（缺：release_v4、release_v5） |
| `project/experiments/**` | 173 | 77,338,541 | 无 |
| `project/` 根+反馈等 | 135+18 | ~2.7M | 无 |
| 仓根 4 文件 | 4 | 3,208,987 | README.md/.gitattributes/ARCHIVE_MANIFEST.json/READABLE_FILES.json；**无 LICENSE**（repo meta `license: null`） |

- 许可文本实测：`submissions/*/LICENSE.txt` 与 `external/round10/arlene_shop/LICENSE.txt` 均为标准 Apache-2.0 全文（11,358B）；`external/round8/fieldcraft/LICENSE.txt` 为无附录短式（10,137B）；`.training/` site-packages 内 3 个 LICENSE.txt 是 numpy/scipy/joblib **上游自有许可**（非 WHmaoxian123 授权，contents API 不可达未取正文，按 dist-info 常识登记）。
- 覆盖占比：位于"带 LICENSE.txt 目录内"的文件 155/6,997=**2.2%**（字节口径 3.2%）；submissions 树整体 220/6,997=3.1%。
- NOTICE 链（实抓 `release_v10_r5/NOTICE.txt` 8,122B 全文）：继承谱系 shiiin9 Orderbook → Ahmed Berat Ozer V55/V56/EXP277/EXP293 → nathanjacob pipe16 → haideptry "The 2965 Master Hybrid Engine" → 本地 V9/V10 层；关键原句：**"Local additions are under Apache-2.0, consistent with the inherited code"**、"These are the source's embedded license statements; no absent standalone Master NOTICE/LICENSE or independently verified license metadata is invented"。即 Apache-2.0 授予针对**本地增改**，上游段保留上游署名（上游许可证真实性未逐源独立复核——登记为限界）。

### 1.2 Release 备份（archive-20261001）与"检查点"

- 拼合 ZIP 2,150,343,616B（README 自报整体 sha256 b921e233…，未整下未复核）；manifest（≡仓内 ARCHIVE_MANIFEST.json，sha256 5866e09c 双侧一致）登记 **12,431 文件/5,848,439,267B**。
- **备份差集**（只在 Release、不在 git）：5,438 文件/4,191,741,687B——research 4,188、.venv 965、results 203（对局 replay）、__pycache__ 30、experiments 24、external 13、checkpoints 7、反馈目录 7、submissions 1。**零 Apache-2.0 覆盖**。
- **`checkpoints/` 实测形态**（part001 字节区间取样，8/8 sha 与 manifest 一致）：7 个 zip（40–132MB，共 ~666MB）+2 个 json 指针。样本 `round10_20260923_150427.zip`（280 条目）内容=**工作区状态快照**（research/results/experiments 的代码+数据+CONTINUE_*.md 续作文档），非模型权重（全仓 0 个 .pt/.pth/.safetensors；`.f32/.npz` 数据集仅 3 件小样本）。zip 内仅 external/arlene_shop 自带 LICENSE/NOTICE，**检查点整体无许可授予**。
- 检查点是否"代码的衍生=Apache-2.0 附带"：**两可论证如实记录**——正方：zip 内容主体是已被逐件 Apache-2.0 覆盖的 submissions 代码与未覆盖 research 代码的混合快照，若视为"已授权代码的副本/衍生"，Apache-2.0 §1 可延展；反方：检查点是独立分发物，含 5,438 零覆盖文件中的 research/results 数据，且作者明言归档"不添加额外的授权许可"，无明示授予即无授予。裁定书按反方保守处理，正方留档。

### 1.3 Release 资产清单（名称/大小/哈希）

见 `ext/whmaoxian_harvest/provenance.md` §Release 资产清单（9 资产：archive_info.json、part001–005、manifest.json、restore.cmd、restore.ps1；每卷 sha256 钉值齐备；10-03 复核与 10-02 抓取零变动，download_count 全部 ≤2）。

## 2. 裁定书（建议案，判定权在用户）

### 口径 A（从严）：仅逐件 Apache-2.0 明示覆盖的文本/代码可用，检查点弃

- **依据**：①repo meta license=null+仓根无 LICENSE 文件（GitHub 无许可公共仓=默认保留全部权利）；②根 README 原句"保留项目内原有 LICENSE、NOTICE 和来源记录。**本归档不添加额外的授权许可**"——作者明知并刻意选择了"逐件授予、整体不授予"的结构；③18 个 submissions 目录 LICENSE.txt+NOTICE.txt 构成清晰的 Apache-2.0 明示授予（含专利授权+再分发条件）；④检查点/备份差集无任何授予；⑤NOTICE 链自证上游段（haideptry Master 等）许可证系"源内嵌声明"未独立核证，从严口径下按"本地增改=Apache-2.0"取用最稳。
- **可用范围**：`project/submissions/{release_v6..v10_r5, candidate_*}`（18 目录，含 r3/r4_2/r5 终件与 candidate_v8_dsm）+ external/{fieldcraft,arlene_shop} 两目录——执行/评估/内部池测/再分发（携 LICENSE+NOTICE）。
- **风险**：损失 research/ 的情报再利用权（只能读不能搬）；上游段许可真实性未逐源复核（NOTICE 自认"未发明不存在的独立 LICENSE"=上游无独立许可证文件，仅内嵌声明）；release_v4/v5 两目录无 LICENSE.txt 连带不可用。

### 口径 B（从宽）：仓整体按 Apache-2.0 处理

- **依据**：①作者意图宽松——公开全量归档+restore 脚本+manifest 哈希，README 称"仓库为私有"却实际公开（PublicEvent 10-01）；②18/20 提交目录+2 个 external 目录共 20 个 Apache-2.0 锚点遍布仓内；③全部提交候选（作者的核心作品）均在覆盖内，research 只是其过程材料，作者未对任何文件标注保密或限制。
- **风险**：①与根 README 明文相反（"不添加额外的授权许可"最自然读法=根级/整体无授予）——从宽需无视作者明示文本，法律上站不住；②research/ 含第三方公开 notebook 提取件（fieldcraft/shoprouter/Boey 等）与官方对局 replay，作者本就无权以 Apache-2.0 再授权他人/platform 内容；③.venv 上游 BSD 等许可混入，整仓单许可声明与事实不符；④若作者日后主张权利（README 自称"私有"留有伏笔），从宽收割面越大回退成本越高。

### 推荐：**口径 A（从严）+ 阅读-收割两区制**

- **阅读区**（全仓）：repo_full clone 留档作情报源（研究方法论、对手建模素材、反馈 replay、ROUND_RESULTS——只读不搬）。
- **收割区**（Apache-2.0 明示覆盖）：18 个 submissions 目录——本任务快筛已只动用收割区三件（合规先例）；后续池测/移植亦限此区，再分发必须携带原 LICENSE.txt+NOTICE.txt 并保留上游署名链。
- **禁区**：检查点 7 zip、备份差集 5,438 文件——不搬运、不再分发、不入 KB 条目正文（可登记存在性与哈希）；反馈 replay 若需用，优先从 Kaggle 官方 endpoint 直取（平台数据回官方渠道，provenance 更干净）。
- 理由：文本证据（README 明示）+ 结构证据（repo meta null vs 逐件 LICENSE）+ 上游混权事实三者同向；从严口径的情报损失已被"阅读区"补偿，而法律暴露面最小。

## 3. 选择性收割清单（预算执行）

| 项 | 量 | 完整性 |
|---|---|---|
| `repo_full/` git 源码树 | 6,997 文件/1.7G 工作树；HEAD ed63c7f6（删嵌套 .git，msdsm_full 先例） | vs ARCHIVE_MANIFEST.json 逐文件 sha256 抽验 40/40 |
| Release 小件 | archive_info/restore.cmd/restore.ps1/part005（2.86MB） | part005 sha 与 archive_info 钉值一致 |
| manifest | ≡仓内 ARCHIVE_MANIFEST.json（sha256 5866e09c 两侧一致，零下载复用） | 12,431 文件清单全解析 |
| 检查点取样 | round10_20260923_150427.zip（40MB）+round10_latest.json+checkpoint_round10.py | 3/3 sha=manifest 值（part001 临时下载用后删，哈希钉死可复下） |
| 反馈 replay 取样 | 5 件官方对局 JSON（V7/V8/V9/V10 反馈+反馈信息3，各 ~32.4MB） | 5/5 sha=manifest 值；反馈信息1/2 在 part004 未下（按需可补） |
| 快筛件拷贝 | orderbook_whmx_lab/pieces/{r3,r4_2,r5}/main.py | tar 内 byte-identical；6/6 sha=README 自报值 |

总占用 1.8G（≤3G 预算）；2.15GB 分卷未整下；磁盘收后 72G。

## 4. 候选初筛（12-fold 快筛，判决惯例）

- 候选挑选依据（README/文件名/时间戳）：终两席自报=R4.2（56683114）+R5；R5 README（09-30 21:15，Claude）自述"本地验证通过，Claude 未上传"、用途替换 R3 重交（56683134）→ 选 **r3 / r4_2 / r5** 三件；release_v4（3.7KB tar 早期件）/v5（自报线上 1290.1 那版）与 candidate_* 系非终件不入本轮。
- 可跑性预检：三件均为规则式纯 Python 单文件（import 仅标准库 base64/copy/itertools/json/math/random/zlib；无权重/无大依赖）；官方 last-callable 装载语义实测：r4_2/r5 末位 callable=`kaggle_hpx2_final_agent`（与自报入口一致）、r3 末位命名空间赋值 `kaggle_endx_submission_agent=endx_agent`（NOTICE 链里"重定义不改命名空间插入位"的工程细节与此吻合）。
- **快筛 verdict（bwrap 沙箱、面板 {H1 王座, mpx, r40, A}、674000+i*131 i=0..11、每对 12 fold 双席 24 局、每件另跑 sim_bridge 在环认证 30 局）**：

| 件 | vs H1 h2h | vs mpx | vs r40 | vs A | 红局 | verdict |
|---|---|---|---|---|---|---|
| r3 | 0.75（9W3L，margin +602.6） | 0.6667 | 0.9167 | 0.875 | 0/96 | **BEATS_CEILING** |
| r4_2 | 0.8333（10W2L，margin +1320.9） | 0.8333 | 0.9167 | 0.9167 | 0/96 | **BEATS_CEILING** |
| r5 | 0.8333（10W2L，margin +1368.5） | 0.8333 | 0.9167 | 0.9167 | 0/96 | **BEATS_CEILING** |

- 读数注：三件强度序 r4_2 ≈ r5 > r3（r4_2 与 r5 各对 h2h 完全相同、margin +1320.9 vs +1368.5——与"R5=R4.2+一处 margin 20 改动"的等强度自述同构；r3→r4_2 差分 99 行=三个减浪费层）；三件 sim_bridge 在环认证各 30/30 一致、engine=sim、零红局（0/288）。对照上轮开源潮池测（syx 0.9167/taeyan 0.8333/romansvet 0.8333 vs H1），本仓终件 r4_2/r5=0.8333 与 taeyan/romansvet 同档、r3=0.75 略低但仍过王座线。自报线上 1290.1（v5）/终两席提交号均为自报未核。
- 总预算：408 局次（baseline 30+每件认证 30×3+面板 288），1986.9s。
- 证据：`orderbook_whmx_lab/evidence/whmx_screen.json`（逐局行含 banks/margin_clean/realized_px）。

## 5. candidate_v8_dsm ↔ DSM 队关系探查（只登记不推断）

- **文件签名比对（决定性）**：candidate_v8_dsm/main.py（565,868B）内嵌单段 base85+zlib 数据 `_R8_DEMOS`，解码为 dict——**恰好 24 个键=DSM 24 局研究 episode ID 字符串**（111940707/111932964/…），与 `research/round8/top2/proxy_provenance.json` 的 DSM 研究集 **24/24 全等**，与 Vadim 研究集交集 **0**；每键含 719 步动作带+30 步契约层。对照 `dsm_episodes.json`：这些 episode 全部是 **DSM 提交 56444344（teamId 16732748，研究时点分 ~3101）的官方公开对局**。
- **档案自述（三重否认）**：NOTICE.txt 原句"NOT DSM private source, DSM's complete algorithm, an official DSM release, or an endorsement by DSM"、"No private model, notebook, credentials, or unpublished source were obtained"、v7 NOTICE"The repository's Vadim/DSM public-replay research is separate: this artifact contains no claim of access to either author's private strategy source code"。研究方法（STRATEGY_FINDINGS.md，2026-09-22）：24 屺冻结 study/5 局 sealed、按 episode ID 哈希冻结、严格路由器仅在完整实体状态相符时切换示范路线。
- **DSM 侧身份**（本地 monitor-baseline LB CSV @10-02T12:34Z）：DSM=**终榜第 3**（TeamId 16732748，2945.5，成员 denden12/masspeaks/shimishige）——任务简报"#4"与实测名次差异登记（可能混用 10-01 快照或 provisional 口径，不择一）。
- **结论登记**：candidate_v8_dsm 与 DSM 队的关系=**公开 replay 研究的条件化路由代理**（作者重建、非 DSM 私码、非 DSM 成员作品、无接触证据）；该候选 NOT promoted（README"not promoted"，round8 未晋级）。交叉注：romansvet 仓 docs/strategy/2026-09-23-dsmland1.md 显示同期第三方也在研究 DSM 公开对局——公开 replay 研究是赛后多队共同行为模式。

## 6. 异常与限界

1. **numpy 上游 LICENSE 正文未取**：`.training/` 前缀目录 contents API 404（raw+json 双试）；按 dist-info 惯例登记为上游 BSD 系，不影响裁定主结论。
2. **拼合 ZIP 整体 sha256 未复核**（需整下 2.15GB，超预算）：以分卷钉值哈希（archive_info）+ZIP64 中央目录解析+8/8 取样件 manifest sha 全一致为替代完整性证据。
3. **反馈信息1/2 未取样**（在 part004，未下载）：按需可补，方法已在 extract_feedback.py 固化。
4. **release_v4/v5 无 LICENSE.txt**：v5 为自报线上 1290.1 那版——从严口径下不可用（略讽刺但如实登记）；如需池测须先补授权或等作者补件。
5. **上游许可证真实性未逐源复核**：NOTICE 自证上游仅内嵌声明（haideptry Master 等），我方未逐一回溯各 notebook 源核实其 Apache-2.0 状态；收割区再分发时以 NOTICE 链署名为准。
6. **DSM 名次两读**（简报 #4 vs 终榜快照 #3）：登记不择一；dsm_episodes 的 initialScore ~3101 是研究时点（09-22）读数非终榜。
7. **检查点许可两可论证**已双记录（§1.2）；推荐案取保守侧。
8. **可见性时序未决延续**：README 自称"仓库为私有"但仓现公开、PublicEvent 10-01——monitor-round2 已登记双假设，本轮无新证据。
9. 快筛为 12 fold 中性块口径，非线上评级；"Never quote the peak"；自报数字（1290.1/56683114/56683134/56415376）全部未经平台侧核。

## 7. 建议（分级）

- **P0（裁定）**：采纳口径 A——阅读-收割两区制；收割区=submissions 18 目录（Apache-2.0 携证使用），禁区=检查点+备份差集；反馈 replay 用官方 endpoint 直取。
- **P1（情报利用）**：r4_2/r5 已证 BEATS_CEILING 梯队——按开源潮同流程进入复盘轨（方法论拆解：固定商店重打消运气、NOTICE 链谱系考古、终局两席战术）；research/claude_20260929 与 v10_top10 的 bc_integration 是 Claude 协作方法论一手材料（只读）。
- **P2（盯防）**：①作者是否补根级许可或 release_v4/v5 LICENSE（决定禁区是否解禁）；②DSM/Farmcore 等前队是否开仓；③终榜 10-14/15 落定后名次自报核验（含本仓 56683114/56683134 是否实存）。

## 需登记行（主会话执行，本任务不代改）

- references/INDEX.md：`| 2026-10-03-whmaoxian-license-harvest | dff20b-3 | WHmaoxian123 仓许可裁定材料+选择性收割+终件快筛+DSM 关系探查 | ext/whmaoxian_harvest/ |`（按 INDEX 实际列式调整）
- fn_docs/hybrid/analyses/registry.jsonl（若裁决入 analyses 轨）：`{"task_id":"dff20b-3","date":"2026-10-03","type":"license-harvest","repo":"WHmaoxian123/kaggriculture","verdicts":{"r3":"BEATS_CEILING","r4_2":"BEATS_CEILING","r5":"BEATS_CEILING"},"license_rule":"strict-A","evidence":"orderbook_whmx_lab/evidence/whmx_screen.json"}`（schema 以 config/templates 实际契约核对后入）
- JOURNAL.md（阶段行，由主会话按铁律 6 补）：`2026-10-03 dff20b-3 WHmaoxian123 许可裁定+收割+快筛 完成（1.8G/预算3G）`
