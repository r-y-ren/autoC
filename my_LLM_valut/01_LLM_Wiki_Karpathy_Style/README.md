# 01_LLM_Wiki_Karpathy_Style

这是当前正在使用的主知识库工程。它以 Andrej Karpathy 的极简 LLM Wiki 理念为基础，但已经适配为一个“单项目自洽”的研究工作区。

真正的编译规则以 [schema.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/schema.md) 为准；本 README 负责说明这个目录现在怎么用。

---

## 这是什么

这个目录现在同时承载 4 类内容：

1. `raw/`
源文献与原始材料的不可变输入层。

2. `wiki/`
正式编译后的知识库层。

3. `synthesis/`
AI 对话沉淀、候选洞见和临时综合层。

4. `output/`
你的正式输出层，比如论文、书稿、博客和 PPT 的登记与组织。

这意味着 `01_LLM_Wiki_Karpathy_Style` 本身就是完整工作区。

---

## 目录结构

```text
01_LLM_Wiki_Karpathy_Style/
├── raw/
│   ├── markdown/        # 论文 markdown 源
│   ├── pdfs/            # 原始 PDF
│   ├── assets/          # 图片、图表与双链素材
│   └── scripts/         # 原始材料处理脚本
├── wiki/
│   ├── index.md         # 正式知识库总入口
│   ├── log.md           # 仅追加的活动日志
│   └── *.md             # 论文页、概念页、主题页、综合页
├── synthesis/
│   └── AI_Inbox.md      # AI 对话的候选沉淀入口
├── output/
│   ├── index.md         # 正式输出总入口
│   ├── papers/
│   ├── books/
│   ├── blogs/
│   └── slides/
├── schema.md            # 唯一编译规则
└── README.md            # 本文件
```

---

## 每层职责

### `raw/`
- 只放原始材料
- 默认不可修改
- 所有正式知识都应尽量可追溯回这里

### `wiki/`
- 只放正式编译后的知识页
- 这里是后续查询、写作和研究判断的主入口
- 页面类型包括论文页、概念页、系统建模页、主题页、对比页和综合页

### `synthesis/`
- 只放“还没正式进入 wiki”的候选沉淀
- 不复制整段 AI 对话
- 只放压缩卡片、候选判断和待编译洞见

### `output/`
- 只放你的正式输出索引和输出文件
- 包括论文、书稿、博客、PPT 等
- 输出物不直接等于知识库页面；如需反哺知识库，再显式编译回 `wiki/`

---

## 日常使用

### 1. 导入论文
把新论文放到：

- `raw/markdown/`
- 如有 PDF，同步放到 `raw/pdfs/`
- 如有图片素材，放到 `raw/assets/`

### 2. 编译知识库
告诉 LLM：

```text
请根据 schema.md 编译 raw/markdown/ 中的新论文。
```

LLM 会按 [schema.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/schema.md)：
- 创建或更新论文页
- 生长概念页、建模页、主题页
- 更新 [wiki/index.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/wiki/index.md)
- 追加 [wiki/log.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/wiki/log.md)

### 3. 沉淀 AI 对话
如果某轮对话有长期价值，不直接复制全文，而是要求：

```text
请把这轮对话沉淀到 synthesis/AI_Inbox.md
```

### 4. 管理正式输出
如果你在写论文、博客或 PPT，就把结果登记到：

- [output/index.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/output/index.md)

需要时再把其中稳定、可复用的知识反向编译回 `wiki/`。

---

## 最常用入口

- 正式知识库入口：[wiki/index.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/wiki/index.md)
- 活动日志：[wiki/log.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/wiki/log.md)
- AI 候选沉淀入口：[synthesis/AI_Inbox.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/synthesis/AI_Inbox.md)
- 正式输出入口：[output/index.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/output/index.md)
- 编译规则：[schema.md](/Users/wupengfei/Downloads/my_LLM_valut/01_LLM_Wiki_Karpathy_Style/schema.md)

---

## 使用原则

- `raw/` 是证据输入层，不拿来写结论
- `wiki/` 是正式知识层，不放临时聊天记录
- `synthesis/` 是候选层，不直接当事实来源
- `output/` 是成果层，不自动等于知识库
- 如果目录职责发生变化，优先更新本 README 和 `schema.md`

---

## 当前状态

现在的 `01_LLM_Wiki_Karpathy_Style` 已经是：

- 一个可持续扩容的论文编译器
- 一个可查询的正式 wiki
- 一个可沉淀 AI 对话的轻量候选层
- 一个可管理论文与写作成果的输出层

后续使用时，优先把“怎么编译”交给 `schema.md`，把“这个目录是做什么的”交给本 README。
