# probes/ —— 工程内部开发探针输出

评估/调参过程的中间产物按主题分子目录（2026-09-01 起 `.tmp-*` 散落目录全部归位于此）：
`r3/ r5/ v7/ v9/ mf/ mg/ intel/`（候选对比、参数扫描、情报分析输出）。

- 候选源码（agent/main.py 等身份锁定文件）provenance 注释里的旧 `.tmp-*` 路径
  **保持原样**（SHA 锁定，改一字节即断身份链）；本目录内历史探针脚本同理。
- 外部抓取的参考材料不放这里——去 `workspace/kaggriculture/references/`。
- 本目录 gitignore（README 除外），大文件与中间产物不入库。
