# 01: 多机协作地基

**What to build:** 两台接力维护的机器开机即可见协作纪律与错配警示：AGENTS.md 新增多机协作节（接力纪律：开工 pull --rebase / 阶段 commit 即 push / 远程为交接唯一事实源 / 归档后 push --tags；"一台 KB 维护+一台战役"分工并行明文认可；deep-sync cron 仅单机启用）；契约版本字段与 bump 惯例落地；SessionStart 播报脚本增加契约版本行与插件可用性检查行（直接调用脚本即可断言输出，不依赖钩子当前是否启用）；DESIGN.md 增加插件清单（mattpocock / ppt-master / superpowers / document-skills 的版本与安装命令）；.gitignore 预加 `kb/inbox/`。

**Blocked by:** None（可立即开工）

**Status:** ready-for-agent

- [x] AGENTS.md 含多机协作节，覆盖接力四纪律、分工并行认可、cron 单机规则、归档 tag push
- [x] 契约版本字段存在且完成一次 bump；播报脚本直接调用输出版本行
- [x] 插件可用性检查直接调用输出各插件在/缺状态（人为临时重命名一个插件目录可触发缺失警示）
- [x] DESIGN.md 含插件清单+版本+安装命令
- [x] .gitignore 含 `kb/inbox/`
