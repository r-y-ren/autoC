---
id: gh-squall01337_mixamo-llm-mocap
name: "mixamo-llm-mocap: 视频到 Mixamo 角色动画的 agent 可操作全管线"
field: [LLM agents, 3D 动画与动作捕捉]
directions: [黑客松与数据竞赛]
published: "2026-08-17"
maturity: demo
signal:
  venue: GitHub
  stars: 204
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "AIGC/创意类黑客松的高视觉冲击项目底座：锁定机位视频→任意 Mixamo 角色干净 FK 动画的全自动 10 阶段管线（GVHMR 姿态估计→数值节拍分析→JSON 动作规格→方向保持重定向→Blender MCP 应用→数值 QA 门→逐帧参考对比→双角色碰撞检查→渲染展示），且全管线 CLI/socket 化、决策全部来自数值而非人眼——'AI agent 端到端操作专业软件管线'的工程范式（数字门控 + PITFALLS 文档喂给下一个 agent）可整体迁移到任何 agent+DCC 软件的赛题；204 star 配 44 fork 的高复现意愿比"
    reuse_cost: "高"
    open_source: "https://github.com/squall01337/mixamo-llm-mocap（MIT + 第三方组件附注）"
sources:
  - url: https://github.com/squall01337/mixamo-llm-mocap
    title: "squall01337/mixamo-llm-mocap: Turn any video into a Mixamo-rig animation"
    accessed: "2026-08-28"
  - url: https://raw.githubusercontent.com/squall01337/mixamo-llm-mocap/main/LICENSE
    title: "LICENSE 全文（MIT + Mixamo/GVHMR/SMPL-X/Blender MCP 第三方附注）"
    accessed: "2026-08-28"
---

# mixamo-llm-mocap：无动捕服、视频直出 Mixamo 角色动画的 agent 化管线

## 是什么

squall01337 于 2026-08-17 发布的 Python 管线（204 star/44 fork，API 实查 2026-08-28）：把锁定机位、首尾带 T-pose 书挡的视频（实拍或 AI 生成）转成任意 Mixamo 角色上的干净 FK 动画，支持单人与双人对打（按画面左右分轨）。10 阶段：GVHMR（SMPL-X 网格恢复，外部仓库）估计 33 关键点 → analyze_landmarks.py 数值节拍检测 → 人写（或 agent 写）action_specs/*.json（支撑脚日程/握拳时机/收势锁定等"视频里看不出来的信息"）→ lift_to_mixamo.py 保方向重定向（按自测骨骼长度重建位置）→ apply_mixamo_fk.py 在实时 Blender 内经 Blender MCP 施加 FK 朝向 + 脚底求解（Mixamo 骨架 FK-only，无 IK）→ qa_clip.py 数值 QA 门（爆骨/髋跳/滑脚/根漂移）→ compare_reference.py 逐帧对视频比对并报告偏差帧窗口 → 双角色间距/触及/穿插检查 → BVH 网格级碰撞 → 渲染 side-by-side 展示视频（README 实抓 2026-08-28）。

## 解决什么问题

无动捕服设备时的角色动画生产：AI 生成视频好看但骨骼不可用，手工 K 帧费时；通用重定向又常出滑脚、爆骨、双角色穿插。本项目用"估计器出方向 + 规格出视频不可知信息 + 数值门兜底"三段分工解决。

## 相比前方法优势

- 相比直接用 GVHMR/A2M 输出：本管线保方向但按目标角色实测骨骼长度重建位置，脚底解算到地面高度零滑步；
- 相比人工 K 帧：动作即数据（JSON spec），新动作是写 spec 不是写代码，五个 worked example 覆盖单招到双人对打；
- 相比"眼看着调"：QA 与参考对比全是数值门，"手太高"这类反馈变成帧窗口编号，agent 可据此迭代；"数值和眼睛冲突时通常是数值（代理错配）"的经验也写进文档；
- 对 agent 友好是设计目标而非副产物：每阶段是 CLI 或 socket 调用、节拍决策来自数值、docs/PITFALLS.md 固化全部踩坑供下一个操作者（人或 AI）复用。

## 局限（如实标注）

- **复现成本高**：GVHMR 需另克隆 + 约 5GB checkpoint（HuggingFace 镜像）、SMPL-X 身体模型需 MPI 官网注册下载、Blender 5.1+ 与官方 Blender MCP 插件、约 8GB VRAM GPU（作者 RTX 4080 开发）——赛场需半天到一天预装，且 Windows 专属配方；
- **许可分层**：仓库本体 MIT，但 GitHub API 报 NOASSERTION 因 LICENSE 附第三方条款：Mixamo 角色受 Adobe 条款约束（禁止再分发，用户自行下载）、GVHMR 及其 checkpoint 独立许可、**SMPL-X 注册门控许可（研究用途，商业化赛题需先行核查）**（LICENSE 全文实抓 2026-08-28）；
- **维护迹象弱**：创建 2026-08-17、最后推送 2026-08-18，一天内推送完毕后无更新（API 实查）；本质是一个完成度很高的作品型仓库而非社区项目；
- 拍摄约束硬：锁定机位 + T-pose 书挡 + 双人按画面分轨（追踪 id 接触时不可靠的场景用画面侧分轨替代）。

## 如何用于比赛

1. **AIGC/创意黑客松（主用）**：以本管线为底座做"文字/视频到打斗动画"的展示型作品：demo GIF 级视觉效果开箱即用，赛场差异化押在"agent 闭环操作"——让 agent 读 analyze_landmarks 数值写 beat sheet、跑完全管线、按 compare_reference 的偏差帧窗口自动迭代，讲"AI agent 当动画总监"的故事。reuse_cost 高：预装清单长，必须赛前完成环境（INSTALL.md 有 Windows 实测配方）；商用赛道先过 SMPL-X/GVHMR 许可关。
2. **范式迁移（不碰动画也能用）**：其"数值门控 + 阶段全 CLI 化 + 踩坑文档结构化给 agent"的三件套是 agent 操控任何专业软件（CAD/GIS/仿真）赛题的通用工程模板——评审看得到可度量的质量门而非"看起来对了"。
