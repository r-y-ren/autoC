---
id: tianchi-ant-lingbot-vla-2026
name: 蚂蚁灵波具身大模型挑战赛（天池 532514·AI大模型赛）
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: active
organizer: "共同发起：蚂蚁灵波科技、魔搭社区、阿里云天池；战略合作伙伴：AMD（算力）、松灵机器人（真机硬件）；独家内容合作伙伴：小红书科技（详情页 §9，2026-10-10 核验）"
key_dates:
  报名与线上初赛:
    date: "2026-09-11 ~ 2026-10-26（即日起报名，10-26 24:00 初赛提交截止）"
    verified: true
    note: "详情页赛程节（intro §2）+ 提交截止（task §2.3、QA 赛制#3）多节一致；起点 09-11 来自列表卡窗口口径；抓取时点页面显示『报名剩 16 日 18 时』"
  AMD专项算力窗口:
    date: "2026-09-15 14:00 ~ 2026-10-26 20:00"
    verified: true
    note: "详情页 intro §3.3：约 200 张 GPU（Radeon Cloud，ROCm 栈），规模动态调整，限赛事用途"
  初赛评审:
    date: "2026-10-27 ~ 2026-11-05"
    verified: true
    note: "详情页 intro §2"
  决赛名单公示:
    date: "2026-11-06"
    verified: true
    note: "详情页 intro §2 与 §3.4 双节一致"
  上海线下决赛:
    date: "2026-11-13 ~ 2026-11-15"
    verified: true
    note: "详情页 intro §2（单一官方信源，列表卡窗口终点 11-15 一致）；主办方提供入围团队交通与住宿；详细安排另行通知"
award_levels:
  - name: 一等奖
    count_or_ratio: "1 名"
    note: "现金 ¥80,000 + 荣誉证书 + 魔搭赞助 5,000 魔粒值 & 500 小时 Notebook GPU"
  - name: 二等奖
    count_or_ratio: "2 名"
    note: "现金 ¥50,000 + 荣誉证书 + 3,000 魔粒值 & 300 小时 Notebook GPU"
  - name: 三等奖
    count_or_ratio: "3 名"
    note: "现金 ¥20,000 + 荣誉证书 + 2,000 魔粒值 & 200 小时 Notebook GPU"
  - name: 优秀奖
    count_or_ratio: "若干"
    note: "现金 ¥5,000 + 荣誉证书 + 1,000 魔粒值 & 100 小时 Notebook GPU；页面奖池口径 ¥280,000（名义合计）"
deliverables:
  - "评测结果 results.json（clean 与 randomized 两 setting × 50 任务测试次数/成功次数，按官方模板）"
  - "代码材料（README.md / train.sh / eval.sh / configs/ / src/）"
  - "模型权重 checkpoint（与评测结果对应）"
  - "复现与调优说明 reproduction_report.md（训练/评测方式、参数配置、模型改动、调优思路、复现步骤）"
  - "真机创新可选任务：demo_video.mp4（完整执行过程）+ demo_report.md（目标/设备/数据/方案/效果）"
  - "小红书创作活动（可选）：xiaohongshu_info.md（账号名 + 笔记链接）"
ai_policy:
  summary: "已核详情页三个 tab 全文（赛事介绍/赛题与数据/常见Q&A，2026-10-10）：未见任何 LLM/AI 工具使用限制类条款——赛题本体即视觉-语言-动作（VLA）大模型训练调优赛，用 AI 训练/调优是命题本身。违规作弊定义（详情页 §10.1）：使用非授权训练数据或违反数据使用规范；人工遥控、剪辑伪造或硬编码演示；刷分、恶意干扰评测或机器刷量；抄袭盗用代码方案视频。配套机制：提交须含可复现材料（代码+权重+复现说明），入围决赛者从训练到推理全程复现核验，最终成绩以官方复测为准。"
  url: https://tianchi.aliyun.com/competition/entrance/532514
  checked: 2026-10-10
credibility: 官网
last_verified: 2026-10-10
sources:
  - url: https://tianchi.aliyun.com/competition/entrance/532514
    title: "天池 532514 赛题详情页（官方一手）。browser-use 渲染三 tab 快照：kb/raw/tianchi-ant-lingbot-vla-2026/detail-intro-20261010.md（赛事介绍）、detail-task-20261010.md（赛题与数据）、detail-qa-20261010.md（常见Q&A）。本条目赛程/赛制/数据规则/推理边界/奖金/组队/IP 全部事实依据，正文以 [intro/task/qa §n] 简称引用"
    accessed: 2026-10-10
  - url: https://tianchi.aliyun.com/competition/
    title: "天池竞赛列表页快照（browser-use，kb/raw/tianchi-list/snapshot-20261010.md）：窗口口径 2026.09.11~11.15 与团队数 1523（早间时点），用于与详情页交叉核对"
    accessed: 2026-10-10
  - url: https://huggingface.co/robbyant/lingbot-vla-v2-6b
    title: "赛事指定基座模型权重 HF 模型卡（WebFetch 直抓：~6B 参数/架构组件/Apache-2.0/预训练数据规模/下载量）"
    accessed: 2026-10-10
  - url: https://github.com/Robbyant/lingbot-vla-v2
    title: "LingBot-VLA 2.0 官方代码仓（WebFetch 直抓：VLM 底座 Qwen3-VL-4B-Instruct、55 维动作向量、RoboTwin post-trained 权重官方成绩 93.52% clean / 92.80% randomized）"
    accessed: 2026-10-10
  - url: https://robotwin-platform.github.io
    title: "RoboTwin 2.0 官方项目主页（WebFetch 直抓：50 双臂任务/5 机器人本体/731 物体库/五轴 domain randomization）"
    accessed: 2026-10-10
  - url: https://modelscope.cn/models/Robbyant/lingbot-vla-v2-6b
    title: "赛事指定权重 ModelScope 镜像（官方资源清单 [intro §8] 所载；正文未消费，2026-10-10 curl 验证可达）"
    accessed: 2026-10-10
  - url: https://technology.robbyant.com/lingbot-vla-v2
    title: "LingBot-VLA 2.0 模型介绍页（官方资源清单 [intro §8] 所载；正文未消费，curl 验证可达）"
    accessed: 2026-10-10
  - url: https://huggingface.co/datasets/TianxingChen/RoboTwin2.0
    title: "RoboTwin 2.0 官方开源数据集（赛事指定训练数据源 [intro §8、qa 资源#1]；正文未消费，curl 验证可达）"
    accessed: 2026-10-10
  - url: https://github.com/AMD-DEV-CONTEST/Embodied-AI-Challenge-AMD-Platform-2026-09
    title: "AMD 赛事专用算力领取指南（官方资源清单 [intro §8] 所载；正文未消费，curl 验证可达）"
    accessed: 2026-10-10
  - url: https://github.com/ZiguanWang/Robotwin-radeon-cloud/blob/main/Reproduce_Guide.md
    title: "AMD 代码参考样例：Radeon Cloud 复现指南（官方资源清单 [intro §8] 所载；未消费）"
    accessed: 2026-10-10
---

# 蚂蚁灵波具身大模型挑战赛（天池 532514） — meta

> 引用简称（均抓取于 2026-10-10，原始快照在 `kb/raw/tianchi-ant-lingbot-vla-2026/`）：
> **[intro]** = 赛事介绍 tab（detail-intro-20261010.md）；**[task]** = 赛题与数据 tab（detail-task-20261010.md）；**[qa]** = 常见 Q&A tab（detail-qa-20261010.md）。三者同为官方详情页 https://tianchi.aliyun.com/competition/entrance/532514 的分节内容。

## 概况（2026-10-10 详情页实抓，替换原列表卡口径）

- 由蚂蚁灵波科技、魔搭社区、阿里云天池共同发起的具身智能算法赛：基于开源 **LingBot-VLA 2.0** 预训练模型搭建统一评测体系，线上初赛 + 线下真机黑客马拉松两阶段，面向全球企业/高校/个人开发者开放，无学历职业限制。[intro §1/§4]
- 规模（抓取时点 2026-10-10 晚）：团队数 **1533**，页面奖金口径 **¥280,000**，报名倒计时"剩 16 日 18 时"；标签 #机器人 #计算机视觉。[intro 头部]（列表卡早间快照为 1523，系时点差异非规则差异）
- 命题意图原文：让开发者"在统一任务与真实机器人场景中验证模型复现、训练调优、泛化评测和真机适配能力"。[intro §1]

## 赛制结构

- **两阶段**：线上初赛（仿真必做任务 + 真机创新可选任务）→ 上海线下真机黑客马拉松决赛。[intro §1、task §1]
- **初赛评审仅筛人**：初赛结果只用于筛选入围决赛团队，不与决赛成绩累加；决赛最终奖项以线下真机评测结果 + 官方评审为准。[intro §3.4]
- **选拔逻辑**（主办方口径原文要点）：按提交评测结果的**任务成功率从高到低依次进行复现核验**，结合真机 Demo 综合选拔；**入围决赛团队从训练到推理全流程复现**——复现细节缺失导致的核验失败后果自负。[qa 赛制#4、task §2.4]
- **提交机会**：初赛期间**一共 3 次**（非每天 3 次）。[qa 赛制#1]
- 提交物与目录结构：见 frontmatter `deliverables`（Zip 打包经天池入口，10-26 24:00 截止）。[task §2.3/§2.4/§2.5]

## 基座与数据规则（本赛核心约束）

- **强制统一基座**：必做任务须基于赛事指定 **LingBot-VLA 2.0 预训练模型**（HF/ModelScope：`robbyant/lingbot-vla-v2-6b`）训练调优。[task §2.1、qa 赛题#1]
  - 允许**大幅结构改造**：只要求主干从 LingBot-VLA 2.0 初始化，**无必留模块、无参数比例要求**。[qa 赛题#6]
  - **禁用 RoboTwin 官方权重作起点**——统一从赛事指定权重出发。[qa 赛题#14]
- **训练数据锁定**：RoboTwin 2.0 中 **Aloha-AgileX 的 50 个任务 clean 数据，每任务 50 条**；randomized 数据**只能用于测试**，禁参与训练，**禁外部数据**。[task §2.1、qa 赛题#1]（数据格式 LeRobot/原始不限，qa 资源#3）
- **评测口径**：提交**单一权重**（50 任务 cotrain），分别在 `clean2clean`（对应 seen 指令）与 `clean2random`（对应 unseen 指令）两 setting 下测 **50 任务 × 各 100 次**；最终成绩**以官方复测为准**。[qa 赛题#10/#11/#12、task §2.1]

## 推理与数据增广边界（Q&A 主办方口径逐条）

**禁止**：
- 按任务 ID / instruction 做 task-specific 路由（不公平，明令禁止）。[qa 赛题#8]
- 多 checkpoint/模型 ensemble；推理阶段**只能使用一份权重**。[qa 赛题#9]
- 多 seed 投票类测试时适应。[qa 赛题#17]
- 改光照、桌面高度等外观后**重新生成 observation**（官方 randomization 除外）。[qa 赛题#18-4]
- 基于 simulator 的**额外 rollout 训练**——所有训练监督必须严格来自 clean demonstration。[qa 赛题#18-5]

**允许（带条件）**：
- 其他公开预训练模块/权重（vision encoder、depth/segmentation encoder）——须在 README 声明来源与用法。[qa 赛题#7]
- LoRA 训练后 **merge 回基座**的全量权重可提交——须在 Config/README 说明改动。[qa 赛题#4]
- AMD 环境：评测结果可在 **ROCm + MPLib** 下生成，正常提交并在 README 说明环境细节保证可复现。[qa 赛题#5]
- 数据增广白名单：视觉亮度/颜色噪声；机器人状态扰动；训练机制内部加噪（如 diffusion 式加噪去噪，不额外生成 demonstration）。[qa 赛题#18-1/2/3]
- **初赛无推理时延/显存限制**（决赛边缘算力有显式限制，数值待决赛通知）。[qa 赛题#16]

## 真机创新可选任务（初赛加分项）

- 基于 LingBot-VLA 2.0 完成真实机器人 Demo：**不限场景/任务/数据/机器人本体**，支持单臂、双臂、移动双臂。[task §2.2]
- 考察新颖性、挑战性、真实落地价值与工程实现；**禁人工遥控、剪辑伪造、硬编码演示**。[task §2.2]
- **不设固定分值**：作为初赛评审补充材料，按完成质量作筛选参考。[task §2.2、qa 赛题#2]

## 线下决赛（真机黑客马拉松，11-13~15 上海）

- **赛题开幕当天公布**；统一线下空间，基于 LingBot-VLA 2.0 完成模型适配、现场调试、真机推理评测；**现场真机打分 = 决赛最终评奖依据**。[task §3]
- 主办方统一提供：机械臂、数采设备、任务物料、标准预采数据集、边缘推理算力、现场技术支持；硬件伙伴为**松灵 Cobot Magic 移动双臂数采平台**。[task §3、intro §9]
- 日程（拟）：Day 1 签到/设备领取/环境调试 + 规则宣讲；Day 2–3 数据采集、模型训练/微调、真机推理与正式评测，第三日下午关闭评测与提交通道。[task 决赛日程]
- **专家数据采集每场景 5 次上限**：按采集发起次数计（与 seed 无关，换 seed/重试均计入）；达上限后该场景不得再采，策略评估不受影响、须如实记录成绩。[qa 赛题#13]

## 奖金与 AMD 特别奖励

- 奖金结构见 frontmatter `award_levels`（一等 1×¥80,000 / 二等 2×¥50,000 / 三等 3×¥20,000 / 优秀 若干×¥5,000，另附魔搭魔粒值与 Notebook GPU 时）。[intro §5]
- AMD 特别奖励：使用 AMD 专项算力完成作品且**决赛前三名** → **AMD Radeon RX 9000 系列显卡实物**；成功提交者 +100 AMD 开发者积分；优秀案例获 AMD 社区报道/直播/ROCm 曝光。[intro §7]
- 小红书创作活动（旁支）：话题 #灵波开发者 #LingBot，互动量+质量排序前 30 名得限量周边；真机 Demo 可参与创意征集活动。[intro §6]

## 组队 / 算力 / 合规与 IP

- **组队 2–5 人**，指定 1 名队长；可一人报名但报名完成后**必须组队才能参赛**；每人仅限一队，初赛提交截止后名单锁定。[intro §3.2、qa 赛制#2]
- **不统一提供基础训练算力**（自备）；AMD Radeon Cloud 专项算力自愿以队申请：2026-09-15 14:00 ~ 10-26 20:00，基础约 **200 张 GPU**，ROCm 栈，仅限赛事用途。[intro §3.3]
- 主办方（上海蚂蚁灵波科技）内部员工可参赛、可排名，**不参与奖金奖项**。[intro §4]
- 作弊红线（§10.1）：非授权训练数据/违反数据规范；人工遥控、剪辑伪造、硬编码演示；刷分与恶意干扰评测；抄袭盗用。违规取消资格并追回奖金。[intro §10.1]
- **IP**：参赛作品完整著作权归团队；授予主办方免费、非独占、不可转授权使用许可（公示/展示/科普/非商业传播），期限为活动期间 + 3 年，地域为中国境内（不含港澳台）。[intro §10.2]

## 基座模型技术事实（2026-10-10 WebFetch 直抓 HF 模型卡 / GitHub 仓 / RoboTwin 主页）

- **LingBot-VLA 2.0**（`robbyant/lingbot-vla-v2-6b`）：~6B 参数（6.4B F32，safetensors 约 25.5 GB），**Apache-2.0**；动作空间覆盖 arms/end-effectors/grippers/dexterous hands/waist/head/mobile-base；稀疏 MoE action expert（细粒度专家分割 + 共享专家隔离）；未来预测代理任务；教师模型 DINO-Video（语义时序先验）+ LingBot-Depth（几何线索），Dual-Query Distillation；预训练约 60,000 小时（50,000h 机器人轨迹 × 20 种本体配置 + 10,000h 第一人称人类视频）。HF 模型卡（月下载 1,516，抓取时点）。
- GitHub 仓补充：VLM 底座为 **Qwen3-VL-4B-Instruct**，统一 **55 维 canonical action/state 向量**；训练栈 PyTorch 2.8 / flash-attn 2.8.3 / LeRobot 格式数据 / Muon 优化器 / FSDP2（致谢 VeOmni/LeRobot/TorchTitan）；官方另发布 RoboTwin 后训练权重 `lingbot-vla-v2-6b-robotwin`，自报 **93.52% clean / 92.80% randomized**（超过 π0.5 与 LingBot-VLA 1.0）。
- **RoboTwin 2.0** 基准：**50 个双臂协作操作任务**、**5 种机器人本体**、对象库 731 实例/147 类；沿 clutter/lighting/background/tabletop height/language **五轴 domain randomization**（"randomized"即启用这些扰动，"clean"为默认环境——主页未显式定义 clean/randomized 词对，此为页面语义反推）。注：赛题页的"Aloha-AgileX 本体"口径出自赛事方（RoboTwin 主页未逐列本体名，一致性待其 tasks 文档核验）。

## 与既有具身线条目的关系

- 与 `tianchi-cross-embodied-cognition-2026`（532508，"2026具身世界realworld挑战赛"赛道二，主办中国中检）为**不同赛事**：本赛发起方为蚂蚁灵波科技/魔搭社区，命题基于开源 LingBot-VLA 2.0 统一基座，勿混淆。

## 数据缺口与待核验

- [ ] **winners/ 未建**：赛事进行中（放榜约 2026-11-15 后），按 `award_levels` 前两级（一等奖 1 名、二等奖 2 名）补建。
- [ ] 赛题规则解读帖 https://tianchi.aliyun.com/forum/post/1081761 （[task §2.1] 链接）未消费——内含官方评测模板与"必读_模板和目录要求"细节，参赛前必读。
- [ ] ModelScope 镜像 / technology.robbyant.com 介绍页 / AMD 指南仓 / RoboTwin 数据集页均未消费正文（已 curl 验证 200 可达）。
- [ ] "Aloha-AgileX" 本体名与 RoboTwin 2.0 官方 tasks 文档的一致性待核（主页仅称 5 embodiments）。
- [ ] 决赛细节（场地、边缘算力显式限制数值、决赛日程终版、晋级名额）官方口径为"另行通知/赛前通知"，未发布。
- [ ] `patterns.md` 已建（章程反推层，confidence 低）；获奖实证层待放榜。
