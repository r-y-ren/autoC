# 攻略（workspace/strategy.md）——第三类交付物之一，决策阶段正式产物

---
generated_at: 2026-08-28
direction: 数模与时序预测（主线）/ 黑客松与数据竞赛（支线）
profile_ref: config/profile.yaml
kb_snapshot: 31ea4e1
---

## 一、赛事情报摘要

- **cumcm**（全国大学生数学建模竞赛）：2026 赛窗 09-10 18:00 → 09-13 20:00（72 小时通讯赛，verified 双源），报名经学校至 09-07 截止；2025 年 68311 队，全国一等奖 391 队（≈0.57%）、二等奖 1551 队，另有赛区两级奖缓冲；交付物为纸质/电子论文+支撑材料+**AI 工具使用详情.pdf（2026 新要求）**；AI 政策=可用须申报、核心建模须人主导；竞期严禁队外交流（规则第 5 条，违者取消资格）。
- **kaggle-rsna-knee-abnormality-detection**：entry 10-15、submission 10-22（verified）；$77K；首个"影像+放射报告"双模态 RSNA 数据集；外部数据与模型允许；获奖须 CC-BY-NC 开源+视频。
- **kaggle-kaggriculture**：Google 自办 agentic RL 农场博弈仿真赛；开赛 07-29、终交 09-30、entry_deadline 未核实（meta 标 unknown）；政策最宽松（数据 Apache 2.0、LLM+agent 放行）。
- **tianchi-qoder-thursday**：系列赛 2026-07-16 至 2027-07-31（长窗口随时可进）；Qoder（阿里 AI 编程工具）冠名，官方鼓励 AI 使用。
- **heywhale-mineru-mdic2026**：MinerU 数据智能与前沿语料挑战赛，active；对 AI/开源工具明确开放。⚠ 关键日期与规模在 INDEX 层截断，证据薄弱。
- **mlh-ghw-data**：09-11~17 线上免费数据主题周，挑战积分制无现金奖；MLH 规则无 AI 限制条款。
- **lablabai-assemblyai-voice-2026**：09-01~30 线上月赛，$10K；强制 AssemblyAI 技术栈；新平台（往届兑现记录待核）。
- **mcm-icm**：2027-01-28 开赛（upcoming，远期锚点）；COMAP 允许负责任使用 AI。

## 二、赛道对比矩阵（六维）

| 赛事 | 时间窗 | 技术契合 | 通吃度 | 画像匹配 | 竞争密度 | 合规风险 |
|---|---|---|---|---|---|---|
| **cumcm** | ★强：13 天后开赛，正处 2-10 周最优区（meta verified）【cumcm】 | ★强：KB-2 数模向卡 30+ 张 × patterns 23/23 全量覆盖【cumcm+KB-2】 | ★强：数模栈直通 MCM/ICM 2027-01【mcm-icm】 | ★强：MCM M 奖+蓝桥杯国三（profile.history 已验证能力） | ★中：68311 队、国一 0.57%，但赛区两级评奖提供缓冲带【cumcm】 | 低：prep 模式，工具链赛前交付，赛中零介入 |
| kaggle-rsna-knee | ★强：10-15/10-22，与 CUMCM 无缝衔接（meta verified）【kaggle-rsna】 | ★中：医学影像栈独立，KB-2 仅 edge 医疗 demo 弱命中【arxiv-2608.22108】 | ★弱：栈难复用回数模线 | ★中：ML/可视化可迁移，无医学影像参赛史 | ★高：$77K Kaggle 医学旗舰天梯 | 低：外部数据允许，apply 可行但获奖开源义务重 |
| kaggle-kaggriculture | ★中：终交 09-30，但 entry 截止未核实（unknown）【kaggle-kaggriculture】 | ★强：agent 仿真 × KB-2 LLM-agent 卡 40+，UrbanGround runnable 强映射【arxiv-2608.27456】 | ★中：agent 栈可复用 Qoder/lablab.ai | ★中：RL/仿真经验未证实；4070 8GB 算力边际 | ★中：2000+ 队，新赛种早期（证据有限，降权告知） | 低：LLM+agent 明文放行 |
| tianchi-qoder-thursday | ★强：系列至 2027-07，随时入局【tianchi-qoder-thursday】 | ★强：LLM 应用题 × RAG/agent 卡群命中 | ★中：可作 agent 线练兵场 | ★强：全栈 web 画像直配 | ⚠低证据：INDEX 无规模数据，本维降权 | 低：AI 鼓励型 |
| heywhale-mineru-mdic2026 | ⚠低证据：关键日期 INDEX 截断，本维降权【heywhale-mineru-mdic2026】 | ★中：文档解析/RAG 卡命中【arxiv-2608.25123】 | ★中 | ★中 | ⚠低证据 | 低：AI 开放 |
| mlh-ghw-data | ★冲突：09-11~17 与 CUMCM 72h 完全重叠【mlh-ghw-data】 | ★中 | ★弱：积分制无现金、作品轻量 | ★中：线上免费但英文环境+时差 | ★低：无奖金压力 | 低：无 AI 条款 |
| lablabai-assemblyai-voice | ★中：09 月全月窗口【lablabai-assemblyai-voice-2026】 | ★中：强制语音栈 | ★弱 | ★中 | ⚠低证据：新平台 | 低：强制栈+MIT 合规 |
| mcm-icm（锚点） | ★远：2027-01-28，非本战役窗口【mcm-icm】 | ★强：同数模栈 | —（一鱼多吃终点） | ★强：M 奖卫冕 | ★中 | 低 |

## 三、大显身手信号（近 90 天 KB-2 新卡 × 该赛 patterns 命中）

- **cumcm**：**最强命中**——patterns.md（D11 三层全量）方法论分布 × 时序新卡群：`arxiv-2608.17284`（DNBNet 不规则时序去偏，2025C 类"NIPT 时点判定"题直接对口）+ `arxiv-2608.17293`（Beyond-MSE 评估，评奖标准"结果的正确性"的量化差异化）+ `arxiv-2608.16098`（AsyTO 轻量多变量，8GB 无云算力友好）+ `arxiv-2608.17333`（SPACE 共形区间，"假设的合理性"呈现升级）。
- **kaggle-kaggriculture**：`arxiv-2608.27456`（UrbanGround 城市 agent 沙盒，runnable demo 接 VLM 即跑）+ `arxiv-2608.25500`（CaSKG 技能检索）+ `arxiv-2608.25992`（ProgRouter 编排）——agent 赛种现成底座。
- **tianchi-qoder-thursday**：RAG/agent 卡群命中（`arxiv-2608.25123`/`arxiv-2608.26604`/`arxiv-2608.26385`）。
- **heywhale-mineru-mdic2026**：`arxiv-2608.25123`（SelfGraphRAG）+ `arxiv-2608.26604`（hoBIT）文档/语料向命中。
- **kaggle-rsna-knee**：仅 `arxiv-2608.22108`（edge 医疗 demo）弱命中——如实降权。
- **mlh-ghw-data / lablabai-assemblyai-voice / mcm-icm**：无 90 天内强新卡专项命中（mcm-icm 复用数模线卡群，非新增信号）。

## 四、一鱼多吃路线

**主线（数模线，推荐）**：CUMCM 2026 工具链（时序方法库+论文编译链+72h SOP）→ **MCM/ICM 2027-01-28**（改造量**低**：同栈换题，模板链/方法库/SOP 全直用，M 奖队伍卫冕路径）→ 延伸：亚太杯等校外数模赛（KB 未收录，如需可再 /discover）。

**支线（agent 线，可选并行）**：agent 沙盒栈（UrbanGround `arxiv-2608.27456` 等）→ Qoder 星期四系列（改造**低-中**：单题单投）→ lablab.ai 月赛（改造**中**：强制栈适配）。

**不建线**：RSNA 医学影像栈改造成本**高**且与两线均不复用——只作时间窗衔接的备选，不作主线。

## 五、合规与风险

**模式判定**：CUMCM = **prep**（数模竞期限外部交流类，schema 注明必须 prep）。依据 meta.ai_policy 原文摘引：
> "参赛队可以使用但不要求必须使用，须遵循公开透明原则，**确保核心建模与分析由参赛队主导**，并对AI生成内容逐项人工审查与核实"（《人工智能工具使用规定（2026年试行）》）
> "竞赛期间必须独立完成，严禁与队外任何人（含指导教师）交流讨论赛题"（参赛规则第5条）

→ 推论：**赛中（09-10~13）不得运行本框架的编排/交付流程**（外部交流风险+人主导红线双重约束）；本战役只交付赛前资产，赛中由队伍以自有工具形态使用并按 2026 规定自行申报 AI 使用。

风险清单：
1. **报名时点**：赛区报名 09-07 20:00 截止且经学校教务（cumcm.cnki.net）——队伍人工事项，战役第 0 天核查（缓解：列入 manual 验收项+日历提醒）。
2. **赛题不命中时序方向**：CUMCM 五题选一，工具链按"预测与评估"最优武装但非唯一（缓解：方法库覆盖清洗/回归/优化通用底座+patterns 选题决策树）。
3. **时间冲突**：mlh-ghw-data 与赛期完全重叠→已从推荐剔除；agent 支线若并行须在 09-07 前完成首轮。
4. **模板合规变动**：论文格式规范 2026 修订稿已实抓（来源[7]），摘要页/匿名要求已入编译链验收。

## 六、推荐结论

**推荐第一名：CUMCM 2026 冲奖工具链与实战体系（cumcm，prep 模式）**

理由：① 六维中五维强证据（时间窗 13 天最优区、技术契合 patterns 全量+30 卡、画像 M 奖已验证、通吃度直通 MCM 2027、合规 prep 零风险），唯一 ★中 维度（竞争密度）有赛区两级评奖缓冲；② KB 武装厚度全库第一：23/23 patterns + winners 双年深构 + 时序卡群与 2025C 类真题直接对口；③ 交付物（工具链+SOP+演练）无论赛果如何均为 MCM/ICM 2027 卫冕的复用资产——失败模式被一鱼多吃兜底。

**备选：kaggle-rsna-knee-abnormality-detection**（apply 模式）——时间窗与 CUMCM 无缝衔接（10-15/10-22）、外部数据允许降低冷启动；但竞争密度 ★高、医学影像栈独立（通吃度 ★弱），且 8GB 显存须走 Efficiency 赛道。若主战役提前收官且队伍有余力，再议。

**agent 线支线**（kaggle-kaggriculture / tianchi-qoder-thursday）：与主线不冲突的可选练兵，不占主战役里程碑；kaggriculture 的 entry 截止时间未核实，投前须先补核。
