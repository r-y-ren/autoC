# Kaggriculture 项目完整归档

比赛项目于 2026-10-01（Asia/Taipei）归档。仓库为私有，归属 **WHmaoxian123（Lvasi）**。

## 文件在哪里

- `project/`：可以直接浏览的源码、文档、配置和历史提交包。
- [完整备份下载](https://github.com/WHmaoxian123/kaggriculture/releases/tag/archive-20261001)：包含原项目目录中的每一个文件，包括反馈、对战记录、实验数据、检查点、运行环境和缓存。
- `ARCHIVE_MANIFEST.json`：逐文件大小、SHA-256 和原目录结构。
- `READABLE_FILES.json`：直接放入仓库的原文件清单；其余原文件同样完整保存在备份中。

## 恢复

下载 Release 中列出的所有备份文件。如果备份是分卷，下载 `restore.cmd` 和 `restore.ps1`，将其与全部分卷及 `archive_info.json` 放在同一目录，双击 `restore.cmd`，校验后生成完整 ZIP；如果是单个 ZIP，可直接解压。解压后恢复 `kaggriculture/` 目录。移动后的 Python 虚拟环境可能需要依据 `requirements-lock.txt` 重新建立。

完整备份：12431 个文件，未压缩 5848439267 字节。

备份 SHA-256：`b921e233083f4f04c5bdb2a7c4d09c2a888f6f30105cc72ba0f314307e416e6a`。

保留项目内原有 LICENSE、NOTICE 和来源记录。本归档不添加额外的授权许可，不代表已验证线上分数或比赛最终排名。
