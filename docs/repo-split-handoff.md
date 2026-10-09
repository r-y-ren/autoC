# repo-split 两机交接清单（2026-10-09）

git 拆分（spec r-y-ren/autoC#2，票 T1–T6）已落地：**主库只留工作流面，产物各建独立 git**。
本清单给第二台机器（及未来新机）接手用。

## 仓库清单

| 路径 | GitHub 仓库 | 内容 |
|---|---|---|
| 主库根 | `r-y-ren/autoC` | 流程面：`.zcode/` `config/` `scripts/` `kb/` 清洗层 `docs/` AGENTS.md |
| `workspace/chuangxin2026/` | `r-y-ren/autoC-chuangxin2026` | 战役全量（代码/文档/JOURNAL/metrics/references） |
| `workspace/guojichuangxin2026/` | `r-y-ren/autoC-guojichuangxin2026` | 同上 |
| `workspace/ptcg-playground-2026/` | `r-y-ren/autoC-ptcg-playground-2026` | 同上 |
| `export/` | `r-y-ren/autoC-export` | KB 交付导出层 |
| `kb/raw/` | `r-y-ren/autoC-kbraw` | 原始抓取文档（引用溯源证据） |
| `archive/2026-08_Kaggriculture-…/` | `r-y-ren/autoC-kaggriculture` | 归档快照 + `archive/…` tag |
| `archive/2026-10_kagriculture_…/` | `r-y-ren/autoC-kagriculture` | 归档快照 + `archive/…` tag |

## 第二台机器接手步骤

1. **主库**：在交付分支上 `git pull --rebase`（当前 `deliver/kaggriculture-audit`；合流 `main` 的时机沿用既有里程碑约定，若你只看 main 会拿不到拆分提交）。
   ⚠ 拆分提交会让旧跟踪的产物文件从工作区消失（正常现象，内容在各项目库）；
   **未跟踪大件不受影响**（PX4 树、数据目录、回放 json 等 ignored 内容原地保留）。
2. **逐项目库收敛**（保留本机未跟踪大件）：
   ```bash
   python scripts/maint/repo_split.py --remote-base https://github.com/r-y-ren adopt --skip-archive
   ```
   无 `.flow` manifest 时按主库清单 `config/repo_split_repos.json` 收敛（随主库走，是新机器的事实源）；
   某分区目录已被 pull 清空（如纯文本的 `export/`）就先 `mkdir -p <path>` 再重跑。
   要连归档快照库一起收敛就去掉 `--skip-archive`。
   手动等价（每库）：`mkdir -p <path> && cd <path> && git init -b main && git remote add origin <url> && git fetch origin && git reset --hard origin/main`。
   **新战役**：`init_state --campaign <cid>` 登记后立即
   `python scripts/maint/repo_split.py --remote-base https://github.com/r-y-ren bootstrap --path workspace/<cid> --push`。
3. **校验**：各库 `git status` 干净、`HEAD == origin/main`；如旧机器可提供
   `.flow/repo_split/manifest.json`（逐文件 sha256 基线），可跑
   `python scripts/maint/repo_split.py verify --manifest <该文件>` 做全量对账。
4. **开机契约校验**：`python scripts/guard/contract_check.py` 预期输出
   `契约一致 v19（本地=上游）`（契约版本只随主库走，"上游"=主库上游）。
5. **大文件跨机**：各库大件维持本机留存不随 git 走（既有忽略口径继承进各项目库），
   跨机仍靠物理搬运（"本地保留优先"纪律不变）。

## 日常纪律（拆分后）

- 阶段留痕：JOURNAL 记行 + **项目仓库** commit + 立即 push；主库只在工作流面变更时 commit（契约变更随 commit bump）。
- 归档：`/archive` 脚本自动在项目仓库 commit + `archive/…` tag + push；主库零提交；warn 时手动 `git push --tags` 补推。
- 审计：主库审计流程面、项目库审计产物面；L2 物理守卫与阶段级写入策略不变。

## 迁移事实

- 执行日期 2026-10-09；迁移器 `scripts/maint/repo_split.py`（plan/apply/verify/adopt/snapshot/push，27 测绿）。
- 备份：旧机器 `.flow/repo_split/backup-2026-10-09.bundle`（1.7G 全历史镜像，验证通过前勿删）。
- 主库历史**未重写**（旧历史中的产物保留，`.git` 体积短期不变）；filter-repo 瘦身另行立项。
