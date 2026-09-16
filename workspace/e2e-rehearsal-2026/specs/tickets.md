# Tickets：数据叙事小工具（E2E rehearsal）

> 发布方式：local-files 模式（本仓库无 issue tracker；写入纪律圈禁 specs/，故合并为单文件，每票独立成节、字段齐全）。
> 依赖序编号：01 起，blockers 在前。波次拓扑 = 蓝图 `depends_on`：**W1 = m1 票（01–03）全部在前；W2 = m2 票（04）blocked-by m1 票**。
> m1 票间的 blocked-by 仅表达里程碑内的工件依赖（契约/键名冻结的客观顺序），未新增任何跨里程碑依赖边；跨波次边只有 m2←m1，出自蓝图。
> 技术范围：纯 Python stdlib（零第三方依赖）；Typst→PDF 唯一编译通道 = `~/.venvs/autoc/bin/python -c "import typst; ..."`。
> 验收项 ID（a1/a2/a3）出自蓝图 frontmatter，冻结不改；票内其余勾选项为工程级验收，不带 a 前缀。

---

# 01: 样例数据与 CLI 统计闭环（m1/W1）

**What to build:** 从零打通"数据 → 统计"的可用闭环：准备一份样例 CSV（落战役 references/data/ 并在 references INDEX 登记来源），实现统计 CLI——读入该 CSV，输出统计 JSON（行数/列数/数值列均值与最大值），并提供 `--check` 自检模式（输出统计并按结果给退出码）。附带覆盖外部行为的 unittest 基础测试（CSV→统计、`--check` 退出码、非数值列处理）。完成后可独立演示：一条命令对样例 CSV 出统计 JSON 且自检退出码 0。

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] 样例 CSV 落 references/data/，references INDEX 登记其来源（战役圈禁/引用纪律）
- [ ] CLI 对样例 CSV 输出统计 JSON（行数/列数/数值列均值与最大值），纯 stdlib 实现
- [ ] `--check` 自检模式：输出合法统计并以退出码 0 结束；输入异常以非 0 退出
- [ ] 覆盖上述外部行为的 unittest 测试存在且全绿
- [ ] a1：CLI 对样例 CSV 输出统计 JSON 且自检退出码 0（蓝图验收 cmd 通过）

---

# 02: 接口契约冻结与 metrics 分片（m1/W1）

**What to build:** 把票 01 的真实输出固化为两个角色间的唯一契约：撰写 software↔document 接口契约（统计 JSON 的形状、键名、metrics 键命名——报告侧只许消费这里冻结的名字），并把 CLI 实测数字写入 software/metrics.json 分片（报告所需的全部数字一次入片）。完成后可独立验证：metrics 分片中每个数字与 CLI 实测输出逐键一致，契约键名与 CLI 输出对齐。

**Blocked by:** 01（契约与键名必须冻结自真实 CLI 输出，不得先验编造）。

**Status:** ready-for-agent

- [ ] interface/contract.md 存在，明确统计 JSON 形状与 metrics 键名（software↔document 契约）
- [ ] software/metrics.json 分片存在，数字全部来自 CLI 实测（数据纪律：无编造/估计）
- [ ] metrics 键名与契约、CLI 输出三者逐键对齐
- [ ] 报告所需数字全部入片，无遗漏（m2 消费面完备）

---

# 03: 报告数字核验脚本与测试集收口（m1/W1）

**What to build:** 实现 m1 的最后一个工件：报告数字核验脚本——解析报告 PDF 文本，对 metrics 分片中的数字逐键核验命中（PDF 存在且全部命中 → 退出码 0；任一缺失/不命中 → 非 0），并为其外部行为补 unittest（命中与未命中两分支）。本票同时收口整个 m1 测试集：全战役 unittest discover 全绿。完成后 a1/a2 两条机检 cmd 均可通过，m1 完整可验收。

**Blocked by:** 02（核验脚本按契约冻结的 metrics 键名编写）。

**Status:** ready-for-agent

- [ ] 核验脚本存在：报告 PDF 存在性检查 + 数字逐键命中 metrics 分片，命中 0 / 缺失非 0
- [ ] 核验脚本外部行为（命中/未命中分支）有 unittest 且全绿
- [ ] a2：CLI 单元测试全过（蓝图验收 cmd `unittest discover` 通过，含全 m1 测试集）
- [ ] m1 全部工件齐备（CLI + tests + 样例数据 + 契约 + metrics 分片 + 核验脚本），a1 保持绿

---

# 04: 一页报告 Typst→PDF，数字全量命中 metrics（m2/W2）

**What to build:** document 侧消费 m1 全部产物的单一纵切：以 Typst 撰写一页报告（内容围绕样例数据的统计叙事），经唯一编译通道 `~/.venvs/autoc/bin/python -c "import typst; ..."` 产出 PDF；报告中一切数字只引用 metrics 分片的 `metrics.software.*` 键，不出现任何片外实测数字。完成后对 PDF 运行票 03 的核验脚本须退出码 0，a3 机检通过，m2 收口。

**Blocked by:** 01, 02, 03（蓝图拓扑：m2 depends_on m1；报告需 m1 的样例数据、冻结契约与 metrics 分片、核验脚本）。

**Status:** ready-for-agent

- [ ] Typst 报告源 + 编译产物 PDF 存在；编译仅经 `~/.venvs/autoc` 的 typst 包通道完成
- [ ] 报告为一页，围绕样例数据统计叙事，结构完整
- [ ] 报告中全部数字只引 `metrics.software.*` 键，无片外实测数字
- [ ] a3：报告 PDF 存在且其中数字逐键命中 metrics.json（蓝图验收 cmd：核验脚本通过）
- [ ] a1/a2 在 m2 期间保持绿（无回归）

---

## 波次视图

| 波次 | 里程碑 | 票 | 阻塞关系 |
|---|---|---|---|
| W1 | m1（software） | 01, 02, 03 | 01 无阻塞；02←01；03←02（里程碑内工件依赖） |
| W2 | m2（document） | 04 | 04←01,02,03（蓝图 m2 depends_on m1） |

frontier 推进规则：先 W1（01 → 02 → 03），m1 全绿后进入 W2（04）。
