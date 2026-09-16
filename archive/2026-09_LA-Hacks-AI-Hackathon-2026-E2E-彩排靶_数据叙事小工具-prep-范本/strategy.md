# strategy.md（E2E 彩排 · 最小攻略）

## 1. 情报摘要

- 靶标赛事：**cala-hacks-ai-2026**（LA Hacks AI Hackathon 2026，黑客松与数据竞赛方向，status=upcoming）——kb/competitions/cala-hacks-ai-2026/（2026-09-09 实抓建条）。选它作彩排靶的理由：交付物形态简单（黑客松 demo 型）、ai_policy=未发现限制条款（prep 模式无合规张力）、条目新鲜（last_verified 2026-09-09）。
- KB-2 支撑卡（示例引用，证明策略可回链卡库）：chen2025TypeFlyLowlatencyDrone（LLM×无人机规划）、wang2024EnsuringThresholdAoI（真实群智感知数据集卡）。

## 2. 六维矩阵（单靶彩排，维度作演示性打分）

| 维度 | 评分 | 证据强度 |
|---|---|---|
| 时间窗匹配 | 中（upcoming，彩排当日即可闭环） | 条目 key_dates（强） |
| 技术契合度 | 高（demo 型工具与 KB-2 卡片方法可自由组合） | 演示性——彩排不依赖（弱，如实降权） |
| 通吃度 | 低（单赛道彩排，不评估复投） | 不适用（如实标注） |
| 画像匹配 | 高（Python 全栈队画像完全覆盖 stdlib CLI） | profile.yaml（强） |
| 竞争密度 | 不评估（彩排不投递） | 无数据（如实标注） |
| 合规风险 | 低（无 AI 条款；prep 模式零投递） | 条目 ai_policy（强） |

## 3. 大显身手信号行

近 90 天入库新卡 × 本赛命中：chen2025TypeFlyLowlatencyDrone、wang2024EnsuringThresholdAoI（演示性引用——彩排作品实际只用 stdlib，此行验证格式）。

## 4. 一鱼多吃路线

彩排单靶不评估（格式保留）：demo CLI → 报告 → PPT 三态产物本身即验证交付链复用形态。

## 5. 合规与风险

- mode=**prep**（赛前范本级示例作品；不报名不投递）。依据：条目 ai_policy「未发现 AI 政策条款：官网为 React SPA 单页落地页，实抓 HTML」（2026-09-09）。
- 风险：无（产物即弃；跑完 /archive 归档）。

## 6. 推荐结论

**推荐：以 cala-hacks-ai-2026 为靶跑升级链路彩排**（理由：交付形态最简 + 合规最干净 + 条目新鲜）。备选：lablabai-assemblyai-voice-2026（active，但有强制技术栈条款，彩排不取）。交付开关：**auto_chain=true**（本次彩排核心被测项）。
