---
competition_id: devpost-treehacks-2026
last_verified: 2026-08-28
coverage:
  - 2026
confidence: 低
sources:
  - url: https://treehacks-2026.devpost.com/
    title: "Devpost 赛站首页（评审三轴 / AI 署名条款 / 奖项结构——一手依据）"
    accessed: "2026-08-28"
  - url: https://ose.stanford.edu/news/treehacks-12-sam-altman-and-llamas
    title: "Stanford OSE 校方源（'audacious but feasible' 取向 / hack packs / 现场组队）"
    accessed: "2026-08-28"
  - url: https://stanforddaily.com/2026/02/15/12th-annual-treehacks/
    title: "Stanford Daily 校媒（大奖作品与评审文化报道——二手降级）"
    accessed: "2026-08-28"
---

# TreeHacks 模式库（patterns）

> coverage 仅 2026 且名单只取得部分（大奖 1 席 + 2 个类别奖）：结论置信度低，全部注明信源等级。待 Devpost winners 页补抓后回填。

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- **一手（Devpost 首页直抓）**：评审三轴 Creativity / Technical Complexity / Social Impact；主办方另设 most creative / best hardware hack / most impactful / most technically complex 四类目（二手：Daily）。
- **校方源（OSE 直抓）**：赛制鼓励 "audacious but feasible"（大胆但可行）；提供 "hack packs" 起步代码降低新手门槛、现场配队——成品完成度文化的制度性保障。
- 观察（样本=1 届大奖）：Social Impact 轴上视障辅助硬件拿下大奖，与三轴口径一致（二手佐证，非统计结论）。

## 二、方法论分布（获奖作品的方法/方案套路）

| 模式 | 出现频次/占比 | 代表年份与条目 | 可迁移性 |
|---|---|---|---|
| CV 感知 + 执行机构闭环（软硬结合辅具） | 1/1 大奖（非随机样本，频次不代表总体占比） | 2026 Shepherd（大奖） | 高：开源 CV + 成熟硬件件；对硬件测试项须列人工测试 |
| AI agent 互操作/通信类应用 | 1 席类别奖 | 2026 HackOverflow（fetch.ai 奖，二手） | 高：纯软件、36h 可完成 |
| 可持续/环保方向 | 1 席类别奖 | 2026 ZoneZero（Ecopreneurship 奖，二手） | 中 |

## 三、往届差异化点（什么样的作品拿到了最高奖）

- 样本不足（本届名单部分 + 历届未采集）。可证的仅：大奖=软硬结合 + 高社会影响 + 36 小时内可演示（2026 一手结构 × 二手事实）。
- 机制性差异（一手）：大奖是**硬件实物**（iPhone 17 Pro Max×每队员 等）而非现金——主办方价值取向偏"极客荣誉"而非奖金激励；现金大顶在赞助商赛道（Human Capital $200K fellowship / Visa $10K）。

## 四、反面观察（常见失分模式，若有依据）

- **一手红线（Devpost Requirements 直抓）**：hack 须在 36 小时内完成（赛前成品搬运违规）；AI 工具使用必须署名；队 >5 人违规；须线下到场。
- 资格红线：18+、在校/应届（ accredit 大学）。
- 二手观察（Daily）：15,000+ 申请筛 1,000——入选门槛在申请材料叙事（未取得申请评审标准原文，标待核）。

## 五、赛点检查表（评审标准 → 可执行检查项）

- [ ] 项目叙事同时覆盖三轴：创意点 / 技术复杂度点 / 社会影响点各一句话可陈述
- [ ] 36 小时内可完成的最小可演示闭环（"audacious but feasible"）——砍需求到 demo 可跑
- [ ] AI 工具使用清单与署名（合规硬条款）
- [ ] 硬件类项目：现场演示预案与故障兜底（录屏备份）
- [ ] 队伍 ≤5 人、全员到场；报名申请材料提早打磨（15k→1k 筛选）
- [ ] 赞助商赛道加选（用其 API 可得额外奖项，"optional" 但为低成本增益）

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合：AI 工具全放行（仅署名义务）+ agent/edge AI 赛道密集——合规栈成本近零；36h 现场制对远程/自动化交付不友好，**须线下到场**，属"人工出席型"目标，快循环排期时按 2027 届（约 2027-02）预留行程。
- 获奖模板观察（低置信）："辅助科技 + CV 闭环"与"agent 互操作"两类与评审三轴对齐度高；hack packs 机制说明主办方重新手可及性——不必堆 SOTA。
- 奖金口径四说的教训（见 meta）：对"奖金总额"必须区分现金/价值/宣传三口径再入库，禁止直接采信单一 banner 数字——已沉淀为本条目方法论。
