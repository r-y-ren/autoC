# 04: 纯 Python 推理包与交付四件套

**What to build:** 把最好 BC 候选变成可提交物：量化权重硬编码进 .py 的纯 Python 前向（stdlib-only、离线、推理确定性：同 obs 逐字节同输出、无集合迭代序依赖），standalone 包独立于 v14.x chassis；过 build 确定性/--check、stdlib 扫描、100MB 限、身份链登记四件套。仅在 03 产出接近门的候选时执行。

**Blocked by:** 03

**Status:** ready-for-agent

- [ ] 权重硬编码推理模块 + 确定性测试（黄金哈希式）
- [ ] 包 ≤100KB 级、stdlib 扫描零违规
- [ ] build --check 逐字节一致 + 身份链登记
