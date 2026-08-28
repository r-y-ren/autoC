---
id: gh-UditAkhourii_cdaf
name: "CDAF: 视频的 agent 可读文本边车格式——一次生成、逐次省 token"
field: [LLM agents, 多模态视频理解]
directions: [黑客松与数据竞赛]
published: "2026-08-26"
maturity: demo
signal:
  venue: GitHub
  stars: 96
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "视频类 agent 作品（AI 剪辑/视频问答/素材库检索）的省 token 底座：视频旁生成一次带时间戳的纯文本描述（.cdaf 边车，SHA-256 锚定新鲜度），此后 agent 读几百 token 文本而非重跑视频理解——作者实测每问题 303 vs 3066 prompt token（10.1 倍）、延迟 -35%，且『选片变 grep、时间戳段直接映射剪辑序列』；零依赖校验核心 + npx cdaf-skill 一条命令装进编码 agent，赛场当天可接入"
    reuse_cost: "低"
    open_source: "https://github.com/UditAkhourii/cdaf（MIT；agent skill 为 npm 包 cdaf-skill）"
sources:
  - url: https://github.com/UditAkhourii/cdaf
    title: "UditAkhourii/cdaf: CDAF — Cached Descriptive Asset Files"
    accessed: "2026-08-28"
  - url: https://raw.githubusercontent.com/UditAkhourii/cdaf/main/README.md
    title: "README 全文（规格 v1.0 / 组件表 / 基准数据 / agent skill 协议）"
    accessed: "2026-08-28"
---

# CDAF：让 AI agent 停止重复"看"同一段视频的文本边车格式

## 是什么

UditAkhourii 于 2026-08-26 开源的开放格式+工具链（96 star/6 fork，API 实查 2026-08-28；MIT）：CDAF = Cached Descriptive Asset Files，与视频同名的纯文本边车文件（`clip.mp4` + `clip.cdaf`）。头部为键值元数据，锚定所描述视频的 SHA-256 与字节数——视频一改，合规工具判边车 STALE 并拒绝使用；正文是面向 LLM 阅读优化的 markdown：Summary / 带时间戳的 Segments / Transcript / On-screen Text / Tags（SPEC.md v1.0，README 实抓 2026-08-28）。组件齐全：零依赖解析校验核心（sidecar.py，纯标准库）、生成器（Gemini Files API 自带 key，另有 --local 本地模型通道免 API key）、CLI（generate/validate/read/status）、可复现基准（bench.py 用 ffmpeg 按脚本配方合成测试视频，ground truth 精确、判分客观、无 LLM judge）、agent skill（`npx cdaf-skill` 装进 ~/.claude/skills 或 --print 粘贴到任意 agent 框架）、arXiv 预印本草稿与 Zenodo 存档。

## 解决什么问题

视频理解按曝光计费（作者引用 Gemini 级模型约 263 token/秒），同一素材库在多任务/多 agent/多会话中被反复"观看"；且视频不在文本域——Remotion 等 agent 原生剪辑工具其余环节全文本化后，唯独视频理解这步要把素材送去多模态模型。CDAF 把视频理解变成一次性成本，之后全是文本读取与 grep。

## 相比前方法优势

- 相比每次任务重跑视频模型：基准（gemini-2.5-flash、20 问，README 实抓 2026-08-28）边车作答 20/20 vs 直接看片 19/20，prompt token 303 vs 3066（10.1 倍），延迟 2.24s vs 3.46s；按其数据每问省 2763 token、生成一次 3601 token 约两问回本，token 节省随时长线性增长（作者称 60 秒片约 50 倍）；
- 相比"口头约定 agent 先看缓存"：新鲜度做进工具而非提示词——`cdaf read`/`validate` 对 STALE 边车直接拒绝（探索用字节快检、重大决策用全量哈希），杜绝"描述的是旧片"这一静默错误；
- 相比闭源产品的内部缓存：开放规格 v1.0 + 可复现基准（合成视频、无数据集许可负担），且模型无关——Gemini 只是一个后端实现，Claude/GPT/本地 VLM 可插同一 Sidecar 类型。

## 局限（如实标注）

- 基准规模小且合成：20 个问题、单一模型（gemini-2.5-flash）、ffmpeg 合成素材；"生产环境成本约 1/25"为作者自述口径，未经第三方复现；
- 描述质量封顶可答范围：边车没写到的细节 agent 永远看不到，细粒度空间推理仍需回看原片，格式本身不保证描述完整度；
- 协议是约定不是强制：收益前提是流水线里所有 agent 都遵守 sidecar-first，skill 只对安装了它的 agent 生效；
- 生成后端现有 Gemini 与 --local 两个实现，Claude/GPT 后端是 README 承诺的"可插槽"而非现成代码；PyPI 正式包在路线图上，当前 pip 装法为 git+subdirectory；
- 项目很年轻：创建 2026-08-26、96 star/6 fork（API 实查 2026-08-28），格式生态与长期维护未经验证。

## 如何用于比赛

1. **视频类黑客松（主用）**：做 AI 剪辑/视频问答/素材管理作品时把"看片"换成"读 .cdaf"——省下的 token/延迟直接变成可演示的规模差（素材库大一个量级）；时间戳 Segments 行可映射 Remotion `<Sequence>`/剪辑决策，"选片 = grep .cdaf"是现成的差异化叙事。reuse_cost 低：`npx cdaf-skill` + pip CLI 当天接入，校验路径零依赖零 key。
2. **多模态数据预处理**：赛前对训练素材批量生成描述做 EDA/错误分析，文本化后全库可检索，替代逐个打开视频的人工看片环节。
