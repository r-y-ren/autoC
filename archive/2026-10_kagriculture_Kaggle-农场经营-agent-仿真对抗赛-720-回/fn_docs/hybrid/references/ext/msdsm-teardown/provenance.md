# msdsm-teardown 原始拉取物 provenance

- 抓取窗口：**2026-10-02 12:03–12:23 UTC**（curl + git + kaggle CLI 2.2.4 + tesseract OCR）
- 任务：`P2 冠军解拆解`（#1 官方解 msdsm/kagriculture-solution 技术拆解进复盘轨，registry a51050-2）
- 本目录性质：**替代性证据包**。GitHub 仓 `msdsm/kagriculture-solution` 在抓取窗口内全程 404（API/网页/git ls-remote/raw/codeload 五路一致），无法按原计划做 `msdsm_full/` 源树快照；本目录保存从 Kaggle 讨论帖 745073 附件渠道抢救到的官方 `docs/images/*.png` 三图 + OCR 文本 + 745073 复抓 JSON。

## 文件清单

| 文件 | 内容 | 来源/命令 | 抓取时刻 (UTC) |
|---|---|---|---|
| `docs_images/overview.png` | 官方 overview 图（01/03 TRAINING LOOP，3200×2100） | 讨论帖 745073 正文附件 `kaggle-forum-message-attachments/.../overview.png`（generation=1790912189252135） | 12:06 |
| `docs_images/training_detail.png` | 官方 training history 图（02/03，3200×5295，含逐阶段训练谱系表） | 同上（generation=1790912211323350） | 12:06 |
| `docs_images/model_detail.png` | 官方 architecture & inference 图（03/03，3200×2175） | 同上（generation=1790912225588059） | 12:06 |
| `ocr/*.ocr6.txt` / `*.ocr11.txt` | 三图 tesseract（eng，psm 6 / psm 11）双跑 OCR | `tesseract <png> <out> --psm 6/11`（eng.traineddata 自 tessdata_fast 下载至 /tmp 使用） | 12:07–12:09 |
| `ocr/bottom2x.txt` | training_detail 底部带（forks/Final A/Final B 区）1.7× LANCZOS 放大后 psm 4 OCR（读序最可靠） | PIL crop+resize → tesseract --psm 4 | 12:18 |
| `topic745073_refetch_2026-10-02.json` | 讨论帖 745073 主题+9 评论复抓（含 authorName；与 10:57 UTC 缓存对比无新评论） | `kaggle competitions topics show 745073 --format json --page-size 200` | 12:05 |

## 外部交叉核验（均无镜像，留证）

- GitHub REST `/repos/msdsm/kagriculture-solution`：404（12:03、12:07、12:11 三次）；`git ls-remote`、raw、codeload、网页均 404。
- GitHub 搜索 `kagriculture-solution in:name`：total 0（12:12）；仓元数据（id 1400989714、created 2026-10-02T03:17Z、pushed 03:30:47Z、size 2346KB、stars 5、forks 2、Python）取自本战役 `postseason-github/gh_search_correct_*.json`（抓取 10:57 UTC，其时仓公开可见）。
- Wayback CDX（prefix 查询）：空；archive.org availability：429 后空。Software Heritage：`Origin ... not found`。ecosyste.ms：404。grep.app：被 Vercel 拦截。Sourcegraph 全局搜索 `kagg-engine`：0 命中。
- 2 个 fork（forks_count=2）无法定位：仓库转 404 后 fork 不可枚举，团队四人（msdsm/msd0110/morim3/BergBuch/piiiiiiiii/qistripute）公开仓列表均无该仓 fork（12:13 探测）。

## 校验

`SHA256SUMS.txt`（11 文件）。README 快照本体在 `../postseason-github/readmes/msdsm_kagriculture-solution.README.md`（SHA256 2ff409bf1dee6806…，见该目录 SHA256SUMS.txt）。

## 纪律

NO-LICENSE 仓：只研究不搬运。本目录仅存其公开发布于 Kaggle 论坛的说明图与我方 OCR 产物、论坛帖文本；未拷贝任何源码入我方产线/工件目录。
