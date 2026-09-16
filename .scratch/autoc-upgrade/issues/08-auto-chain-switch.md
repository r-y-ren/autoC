# 08: 蓝图 auto_chain 开关

**What to build:** 蓝图 schema 新增 `workflow.auto_chain` 布尔字段（默认 true），/attack 呈报蓝图时开关可见、用户可在确认时翻转——"这次交付要不要自动跑规格链"在唯一人工闸门处一并拍板，无需记第二个配置点。

**Blocked by:** 07（K-02 同技能文件，先落 grill 步避免双改）

**Status:** ready-for-agent

- [x] 蓝图 schema 含 workflow.auto_chain（默认 true），正/负例过 schema 校验
- [x] /attack 呈报蓝图时可见开关值
- [x] 确认蓝图后，开关值随蓝图存档可查
