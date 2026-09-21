# 测试基线机器语境声明（machine_context）

> R6 声明物：历史口径与通用口径并列——任何“绿基线”结论必须先读本文档确认机器语境。实测数字只来自当次运行记录，禁止编造。

## 历史口径（“990+2”仅主力机）

- 基线标签: 990+2
- 口径: "990+2" 基线仅在 Windows 主力机 + 语料在机成立（口径原文见源文档）
- 同 commit POSIX 对照: 本 Linux 机同 commit 实测 976 passed / 8 failed / 8 skipped（992 collected）
- 来源: fn_docs/behavior_inventory.md §5（分片 E：测试基线实测）

### 旧树环境性失败/skip 分类（历史事实）

- **CRLF 工件×3**: test_build_determinism、test_p3::TestPackaging、test_artifact_indexes——Windows autocrlf 机构建提交的登记 sha 为 CRLF 字节口径，POSIX fresh clone 盘上为 LF
- **gitignored 数据缺机×3**: （语料/参考数据不在库内）——复现链依赖 machine-local gitignored 语料，缺机即挂
- **Windows-only 断言×2**: normcase 大小写折叠语义、Path("C:/…").is_absolute() 语义——断言依赖 Windows 特有语义，POSIX 上必然为假
- **语料缺机 skip×8**: （8 skipped 全为语料缺机）——数据依赖项显式 skip（缺语料），非代码缺陷

## fn_work 通用口径（本机实测）

- 运行命令: `python -m pytest /mnt/data/Code/autoC/workspace/kaggriculture/fn_work/tests -q --tb=no -rs`
- 平台: Linux-7.2.6-arch2-1-x86_64-with-glibc2.44；Python: 3.14.7
- 汇总行原文: `226 passed in 148.78s (0:02:28)`
- passed: 226
- failed: 0
- skipped: 0

## 数据依赖项 skip 清单（缺什么逐项标注）

- 本次运行 0 个数据依赖 skip（本机无缺失项触发；历史口径的语料缺机 skip×8 见上节旧树分类）。

## CRLF/LF 双兼容策略（仓外 .gitattributes 不可加，一切靠工件+测试双兼容）

- 工件侧：旧树 index 冻结不改；exports 工件类在 `fn_work/artifacts/` 以 LF 规范化重建，双 sha 登记（legacy=CRLF 口径原值 / LF=规范化重算值），POSIX 校验走 LF 值。
- 实测计数: exports index 类 5 件、条目 100：LF 重建 100、二进制跳过 0、缺失 0；legacy=CRLF 口径变体 79 条双 sha 登记（产物根 /mnt/data/Code/autoC/workspace/kaggriculture/fn_work/artifacts）
- 测试侧：路径等价断言用 `paths_equivalent`（normcase 双平台封装）、绝对路径判断用 `is_absolute_cross_platform`（补盘符/UNC 语义）；打包二进制件与 CRLF 无关，不重建仅登记。

## 断言双平台化（Windows-only 模式扫描）

- 扫描与修正: 扫描 59 文件，Windows-only 命中 0、改写 0、残留 0（残留>0 即裁决失败）

## Windows 主力机复检边界（人工/跨机事项）

- R6 验收要求“同 commit 在 Windows 主力机基线不回退”——该复检只能在 Windows 主力机执行，本机不可代跑；重建/修正后首次 Windows 复跑若回退，portable_test_baseline 裁决即失败（fail-closed）。
- 备注: 本机不可执行；同 commit Windows 主力机复跑若基线回退，本裁决口径即失败（R6）
