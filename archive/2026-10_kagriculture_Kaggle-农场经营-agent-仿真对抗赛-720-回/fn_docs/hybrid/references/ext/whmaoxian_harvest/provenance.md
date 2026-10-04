# whmaoxian_harvest 原始拉取物 provenance（ext/whmaoxian_harvest/）

- 抓取窗口：**2026-10-03 ~06:05–06:5x UTC**（比赛 09-30 23:59 UTC 截止后 ~3 天；官方终评窗至 10-14 23:59）
- 任务：`dff20b-3：WHmaoxian123 归档许可裁定与选择性收割`（五件并行任务之一）
- 通道：GitHub REST（`gh api`，账号 r-y-ren 鉴权）+ `gh release download`（Release 资产）+ `git clone --depth 1`（https）
- 上游对照基线：`../monitor-round2-github/`（2026-10-02 18:56–19:35Z 快照；tree/releases/repo JSON 与本轮回灌比对一致——`releases_fresh_20261003.json` sig 比对 True、pushed_at 仍 10-01T03:25:24Z）
- **专名纪律执行记录**：owner/repo（`WHmaoxian123/kaggriculture`）自 `../monitor-round2-github/2026-10-02-monitor-round2-github.md` 报告正文正则程序化派生（`([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)` 过滤 maoxian），再经仓元数据 JSON `full_name` 字段复核；全程零手键专名。

## 收割清单（总量 ~1.8G ≤ 3G 预算；磁盘收后余 72G）

| 组 | 内容 | 来源/命令 | 时刻 (UTC) | 完整性 |
|---|---|---|---|---|
| `repo_full/` | git 源码树全量（6,997 文件 1.7G 工作树） | `git clone --depth 1 https://github.com/WHmaoxian123/kaggriculture.git`（msdsm_full 先例：克隆后记 HEAD、删嵌套 .git） | ~06:1x | HEAD=`ed63c7f6321198c310b80e0e86c131432c47f175`（2026-10-01T10:54:37+08:00 "Archive Kaggriculture project with complete backup manifest"，单提交仓）；`CLONE_HEAD_SHA.txt` 留痕；vs `ARCHIVE_MANIFEST.json` 逐文件 sha256 抽验 **40/40 一致** |
| `release_small/` | Release `archive-20261001` 5 小件：`archive_info.json`(1,147B)/`restore.cmd`(94B)/`restore.ps1`(1,283B)/`manifest.json`≡仓内 `ARCHIVE_MANIFEST.json`（sha256 5866e09c… 双侧一致，未重复下载）/分卷尾 `part005`(2,859,968B) | `gh release download` | 06:09 | part005 sha256=`3f31a778…` 与 archive_info 钉值一致 |
| `checkpoint_sample/` | 检查点取样 3 件：`round10_20260923_150427.zip`(40,167,681B)+`round10_latest.json`(311B)+`checkpoint_round10.py`(3,158B) | part001（512MB，用后已删）ZIP64 中央目录定位字节区间抽取（`release_small/parse_cd.py`/`extract_range.py`） | 06:1x | part001 sha256=`cfc43da9…` 与 archive_info 一致；三件 sha256 与 manifest 逐文件值**全一致**（8e331f…/c32fc1…/8165bc…） |
| `feedback_replays/` | 官方对局 replay 5 件（各 ~32.4MB）：V10反馈/113447926、V7反馈/111934255、V8反馈/112293400、V9反馈信息/112455606、反馈信息3/111485103 | part001+part005 字节区间抽取（`extract_feedback.py`）；反馈信息/111094987 与 反馈信息2/111474023 在 part004 未下载，按需可补 | 06:3x | 5/5 sha256 与 manifest 一致 |
| `license_texts/` | 许可裁定材料 9 件：根 README、submissions r5/dsm 的 LICENSE.txt+NOTICE.txt+README.md、external fieldcraft/arlene_shop LICENSE.txt、（numpy 上游 LICENSE 404=路径带 .training 前缀目录 contents API 不可达，登记） | `gh api repos/.../contents` | 06:0x | 见 SHA256SUMS |

## Release 资产清单（tag `archive-20261001`，2026-10-03 复核与 10-02 抓取零变动）

| 资产 | 大小 (B) | sha256（archive_info.json 钉值） | 处置 |
|---|---|---|---|
| archive_info.json | 1,147 | — | 已下 |
| kaggriculture-complete-20261001.zip.part001 | 536,870,912 | cfc43da903e5bdd7012e32b32cfea162e2766527577c2c46ed251524445a0dcc | 临时下（取样后删，哈希钉死可复下） |
| .part002 | 536,870,912 | 7f1fbdc610d8298c740b2829786fcd981061c9ceefaee7390aaec609b568a15f | 不下 |
| .part003 | 536,870,912 | 5ca4f8c4982553416b4e6aa7cd1b2149965eb683ff04c959e248895d3fe9fe85 | 不下 |
| .part004 | 536,870,912 | d5e84a713eeec781cc12451c0dec3ae39c6bd7d9c46d2080d5bec9ac6d2792c5 | 不下（反馈信息1/2 在此卷） |
| .part005 | 2,859,968 | 3f31a77800b99278e874eb1319681c32be3d0fdfd4420ad0d887a9c253f133f9 | 已下 |
| manifest.json | 3,202,054 | 5866e09c134897c8a743ed62b8ab7e967a165869bd3c6049a588e3cd0d077046 | ≡ repo_full/ARCHIVE_MANIFEST.json（未重复下载） |
| restore.cmd / restore.ps1 | 94 / 1,283 | — | 已下 |

拼合 ZIP 整体：2,150,343,616B，sha256 `b921e233083f4f04c5bdb2a7c4d09c2a888f6f30105cc72ba0f314307e416e6a`（README 自报，**未整下未复核**——分卷拼接+逐件 manifest 抽验为替代完整性证据）。

## 快筛件拷贝

`fn_work/legacy_software/kaggle_simulations/orderbook_whmx_lab/pieces/{r3,r4_2,r5}/main.py` = `repo_full/project/submissions/release_v10_{r3,r4_2,r5}/main.py` 原样拷贝（tar 内 byte-identical 已核；三件 sha256 与各 README 自报 6/6 一致）。

快筛结果（2026-10-03 ~06:16–06:50 UTC，bwrap、12 fold 双席、面板 {H1,mpx,r40,A}）：三件全 **BEATS_CEILING**——r3 vs H1 0.75（9W3L，margin +602.6）、r4_2 0.8333（10W2L，+1320.9）、r5 0.8333（10W2L，+1368.5）；每件 sim_bridge 在环认证 30/30、零红局；总计 408 局次/1986.9s。证据 `orderbook_whmx_lab/evidence/whmx_screen.json`（逐局行含 banks/margin_clean/realized_px）。

## 版权纪律提示

本目录保存 clone 源码树（公开仓 git 通道）、Release 元数据/清单/尾卷、**未整体下载 2.15GB 备份**；检查点与反馈 replay 仅按预算取样。research/**（5,620 文件）与备份差集（5,438 文件）**零许可覆盖**——再分发/入库移植需先过许可裁定（见报告 §裁定书）。`repo_full` 内 submissions/*（18/20 目录）逐件 Apache-2.0。
