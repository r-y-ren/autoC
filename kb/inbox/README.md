# kb/inbox/ —— 外来资料投递箱（升级票03，2026-09-16）

把任意资料文件（赛事章程 PDF、论文、他人分享的材料……）丢进本目录即可，**下次 kb-sync / kb-deep-sync 跑批会自动检查并消费**。本目录被 gitignore（本机暂存区），消化产物（候选队列→条目/卡片）才入库。

## 投递约定

- **零门槛**：直接丢文件，无任何强制格式。
- **建议伴随 sidecar**（同名 + `.meta.yaml`，如 `rules.pdf` → `rules.pdf.meta.yaml`）：

  ```yaml
  kind: comp          # comp=赛事资料 / tech=论文技术 / lead=线索（可省，脚本会按文件名关键词辅助分类）
  title: 2026 大数据挑战赛章程
  source_url: https://example.com/notice.pdf   # 关键：有它才算"已溯源"，资料才能晋级候选队列
  dropped_at: "2026-09-16"
  note: 群里转发的，含赛制变更
  intended: 智慧农业                              # 可选：意向方向提示
  ```

## 消费规则（`python scripts/kb/inbox_intake.py`）

- 三分路由：**comp** → 赛事候选队列（条目增补/新条目）；**tech** → 技术卡候选队列；**无法归类或未溯源** → `kb/raw/leads/` 线索区并在报告点名催补。
- **未溯源（无 sidecar 或缺 source_url）永远只当线索**，不晋级可引用条目（铁律 1）；原件会被移入 `kb/raw/leads/`（不会被自动重扫），**补好 sidecar 后把文件放回 inbox 重新投递**即可在下轮晋级。
- 每轮消费上限见 `config/budget.yaml → quotas.inbox_files_per_run`（默认 20），超出留存下轮，**不删不拒**。
- 消费后的原件移 `kb/raw/inbox-processed/<时间戳>/` 留审计。
- 文件涉及**活跃战役**时只在跑批报告提示，不会自动改动战役文件——是否引用由你在战役会话决定。

## 多机注意

inbox 是**本机**暂存区（gitignore 不跨机）：在 A 机丢的文件等 A 机跑批消化；跨机转移资料请走其他通道或等对应机器的 sync。
