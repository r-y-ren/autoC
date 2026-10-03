# 远程算力链路工具面修复（remotecompute-fixes，2026-10-03，任务 dff20b-4）

> 性质：工具面修复记录（用户已授权）。对象：`2026-10-02-remote-eval-prep.md` §四异常 1/2 的根治落地 + 触发器文档化。
> 本机=rypc（轻薄本）；远程=性能本 first 的 WSL2 Ubuntu（`ssh wsl` = 100.100.0.6:2222，`ssh win` = 100.100.0.6:22，Windows 用户 **oss**，WSL 用户 renyxin）。
> 时间窗：2026-10-03 06:03–06:35 UTC。纪律：先备份后改、改完必验证；不 git commit；不动插件缓存；远程零战役产物（D14）。

## 一、判据判定表

| 判据 | 判定 | 一句话结论 |
|---|---|---|
| 修 A：.wslconfig `vmIdleTimeout=3600000` + 空转 5min 存活 | **过** | 拔保活空转 300s×2 连续存活（uptime 连续 25min 无重启），VM 未再被回收；期间曾有一次约 9 分钟的端口 2222 可达性抖动窗（VM 实际 Running，见 §三限界），自愈未复现 |
| 修 B：env 归一 FW_PASS/WIN_PASS | **过** | env 仅存 FW_PASS/WIN_PASS（WSL_PASS 与别名消除，备份 env.bak），`wsl-sudo` → `sudo-ok`+root+exit 0，`ssh wsl`/`ssh win` 全通 |
| 触发器文档化 | **过** | prep 文档末尾追加"触发器（2026-10-03 增补）"节：T1/T2/T3 三触发条件+判定口径+盯防清单 6 项+判定人（T3 用户独占） |
| 报告落盘 | **过** | 本文件（含改动前后状态/验证输出全文/回滚方法/需登记行） |

## 二、修 A：WSL VM 空闲自灭根治

### 2.1 改动前后状态

| 项 | 前 | 后 |
|---|---|---|
| `C:\Users\oss\.wslconfig` | `[wsl2]` 仅 networkingMode=mirrored / dnsTunneling=true / autoProxy=true（**无 vmIdleTimeout**，默认 60000ms=60s） | 追加 **`vmIdleTimeout=3600000`**（1h），余三行原样保留 |
| 备份 | — | Windows 侧 `C:\Users\oss\.wslconfig.bak-20261003`（copy 成功"已复制 1 个文件"） |
| 保活 | `ssh win 'wsl.exe -d Ubuntu --exec sleep 3600'` 挂载保活（每小时断） | **已无任何保活**（本机 ps 无保活进程，验证期全靠 vmIdleTimeout） |

环境事实：WSL **2.4.11.0**（Windows 10.0.26300，Win11 内核 5.15.167.4-1）；Ubuntu `/etc/wsl.conf` 有 `[boot] systemd=true`（systemd 常驻=distro 层不随会话退出而停，VM 层回收才是要治的对象）。

终态 `type C:\Users\oss\.wslconfig` 实读：

```
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
vmIdleTimeout=3600000
```

改动流程：读原文件留档 → Windows 侧 copy 备份 → 本地起草 `/tmp/wslconfig.new` → `powershell Set-Content`（stdin 管道，ascii 编码）写入 → `type` 回读逐行核对 → `wsl.exe --shutdown` → `wsl.exe -d Ubuntu --exec /bin/true` 拉起（新配置随 VM 冷启动生效，uptime 证实确已重启）。

### 2.2 验证输出（全文，UTC）

**① 拉起后基础链路**（挂载 sleep-25 会话期间）：

```
$ ssh wsl 'echo alive; uptime -p'      # 会话挂载中
alive / up 3 minutes
$ ssh wsl 'systemctl is-active ssh'
active
```

**② 关键验证：拔保活空转 5 分钟（期间零连接），连续两次**：

```
$ date -u '+idle-start %H:%M:%S UTC'; sleep 300; ... ssh wsl 'echo alive; uptime -p'
idle-start 06:18:58 UTC → probe 06:23:58 UTC：alive / up 20 minutes   ← 第 1 次 过
$ （第 2 次）
dark 300s from 06:25:01 → probe-time 06:30:01 UTC：alive / up 25 minutes ← 第 2 次 过
```

**uptime 连续性判读（根治的核心证据）**：VM 于 06:04 随 `wsl --shutdown`+新配置冷启动，此后"up 3→14→20→25 minutes"单调连续，穿过全部黑窗（零挂载会话、零入站连接）无一次归零——即 25 分钟内 VM/系统/sshd 全程未停，对照修复前"60-90s 即整 VM 回收"，**空闲自灭已根治**。

**③ 全链复核**（修 B 完成后一并验，06:3x UTC）：

```
$ ssh wsl 'echo wsl-ok; whoami; hostname'
wsl-ok / renyxin / first
$ ssh win 'echo win-ok'
win-ok
```

### 2.3 若仍灭的退路（本轮未启用，仅存档操作步骤）

vmIdleTimeout 若日后失效（WSL 升级回归/配置被覆盖），退回**常驻保活计划任务**方案（Windows 计划任务每 30min 拉一次 wsl.exe，管理员 cmd 一条命令）：

```
schtasks /create /tn "WSL-Keepalive" /tr "wsl.exe -d Ubuntu --exec /bin/true" /sc minute /mo 30 /ru oss /rl LIMITED
```

（GUI 等价：任务计划程序→创建任务→触发器"每 30 分钟重复"→操作"启动程序 `wsl.exe`"参数 `-d Ubuntu --exec /bin/true`。删除：`schtasks /delete /tn "WSL-Keepalive" /f`。）

## 三、异常与限界（修 A）

1. **06:06–06:15 出现过一窗端口 2222 可达性抖动**：拉起后 +10s 探测超时、首次 5min 黑窗探测超时（06:12:39）、+30s 探测超时（06:15:29）——但同一时刻 Windows 侧 `wsl --list` 显示 Ubuntu **Running**，且 06:17:40 复测 `Test-NetConnection localhost -Port 2222`=True、`uptime`=14min 连续、`ss -tln` 有 `0.0.0.0:2222 LISTEN`，证明 **VM/sshd 从未死**，是 mirrored 网络/tailscale 路径的入站可达性瞬时抖动，自愈后 25+ 分钟未复现（两次 5min 黑窗探测均直连成功，ConnectTimeout=30）。昨天记载的"连执行中 ssh 都被掐"很可能混有此成分。**鉴别 SOP**（日后遇"连不上"先跑再下结论）：`ssh win 'wsl --list'`（Stopped 持续=VM 真回收）→ `ssh win 'powershell Test-NetConnection localhost -Port 2222'`（Windows 侧 True 而 tailscale 侧 False=网络路径问题，非 WSL 生命周期）→ `ssh win 'wsl.exe -d Ubuntu --exec uptime -p'`（uptime 归零=发生过重启）。三次抖动探测用的 ConnectTimeout=12–20s，不能排除 DERP 中继慢握手放大；正式评测起跑前建议先 `ssh wsl 'echo ready'` 探活。
2. `wsl --list` 的 "Stopped" 读数会误导（06:13 读到 Stopped 但 VM 实际连续运行），判定存活以 uptime 连续性 + 端口实测为准。
3. vmIdleTimeout=3600000 意味着**最后一次使用后 VM 仍驻留 1 小时**（占内存 ~1-2GB 级 vmmem）；性能本若长期不用远程算力，可 `ssh win 'wsl --shutdown'` 手动回收，或调低该值。
4. `.wslconfig` 由 Windows 侧 WSL 在 VM 冷启动时读取；日后任何修改都要跟一次 `wsl --shutdown` 才生效。

## 四、修 B：wsl-sudo 凭据变量名归一

### 4.1 改动前后状态

| 项 | 前 | 后 |
|---|---|---|
| `~/.config/remote-compute/env`（600） | `WSL_PASS`+`WIN_PASS` 为主，文件尾临时追加 `FW_PASS`（与 WSL_PASS 同值的别名行） | **仅 `FW_PASS` + `WIN_PASS`**（canonical；WSL_PASS 行更名归位，别名行删除，注释同步改指 wsl-sudo/ssh win） |
| 备份 | — | 同目录 `~/.config/remote-compute/env.bak`（600，406B 原文全量） |
| `~/.local/bin/wsl-sudo` | 读 `FW_PASS`（与技能模板脚本一致） | **未改**（本就是 canonical 端） |

消费面普查（改动前实测）：本机 `~/.local/bin/` 下**唯一**消费该 env 的脚本是 `wsl-sudo`，且只读 `FW_PASS`（grep 全目录证实，无 fw-sudo/first 等其他读者）——删除 WSL_PASS 无任何破坏面。

终态 env 结构（值打码）：

```
# 凭据文件：…
# 用法：把 <> 占位换成真实密码，保存即可。
# wsl-sudo 命令用时自动读取本文件（FW_PASS）；WIN_PASS 为 ssh win 密码备援。不需要 export 到 shell。

# WSL 侧（wsl-sudo 提权用；用户 renyxin）
FW_PASS=<REDACTED>

# Windows 侧（ssh win 密码登录备援；用户 OSS，key 免密后闲置）
WIN_PASS=<REDACTED>
```

### 4.2 验证输出（全文）

```
$ wsl-sudo 'echo sudo-ok; whoami'
sudo-ok
root
exit=0
$ ssh wsl 'echo wsl-ok; whoami; hostname'
wsl-ok / renyxin / first
$ ssh win 'echo win-ok'
win-ok
```

### 4.3 插件缓存差异建议（未改缓存，呈用户裁决）

remote-compute 技能权威模板（`…/my-plugin/0.2.1/skills/remote-compute/scripts/env.template`）Windows 侧变量名为 **`FIRST_PASS`**，与本机 canonical `WIN_PASS` 及任务口径不一致。建议在用户自己的插件源仓（非缓存目录）改模板两行后随插件升级分发：

```diff
- # wsl-sudo 读 FW_PASS；FIRST_PASS 仅为 ssh win 密码登录的备援（key 免密后闲置）
+ # wsl-sudo 读 FW_PASS；WIN_PASS 仅为 ssh win 密码登录的备援（key 免密后闲置）
- FIRST_PASS='<Windows OSS 账户密码>'
+ WIN_PASS='<Windows OSS 账户密码>'
```

（SKILL.md L67 只提 FW_PASS，无需动；wsl-sudo 脚本模板与本机已一致。）

## 五、触发器文档化

`2026-10-02-remote-eval-prep.md` 末尾已追加**"触发器（2026-10-03 增补）"**节：T1 msdsm #1 官方解权重投放 / T2 CarsonBurke checkpoint 投放 / T3 WHmaoxian123 检查点许可裁定通过，任一命中即走该文 §五 SOP 三步（传权重→装载→判决机口径跑池测）；附 6 项盯防清单（msdsm/Carson+debmal/WHmaoxian/超王座三件/10-14~15 终榜窗/次级四项）与判定人（T1/T2 主会话呈报+用户裁决，T3 用户独占裁决）。触发节同时回链本报告（运行时前提已落实）。

## 六、回滚方法

| 改动 | 回滚命令 | 生效条件 |
|---|---|---|
| 修 A .wslconfig | `ssh win 'copy /Y C:\Users\oss\.wslconfig.bak-20261003 C:\Users\oss\.wslconfig'` + `ssh win 'wsl.exe --shutdown'` | VM 下次冷启动 |
| 修 B env | `cp ~/.config/remote-compute/env.bak ~/.config/remote-compute/env` | 即时（wsl-sudo 下次调用） |
| 触发器节 | 删除 prep 文档"触发器（2026-10-03 增补）"整节（或 git 还原本文件，未 commit） | 即时 |

## 需登记行

```
| `2026-10-03-remotecompute-fixes.md` | 本机 rypc→`ssh win`/`ssh wsl` 实操验证（06:03-06:35 UTC，全程输出留档本文）；[前因] 2026-10-02-remote-eval-prep.md §四异常 1/2 | 2026-10-03 | 远程链路两处工具面修复：①`.wslconfig` 追加 vmIdleTimeout=3600000（备份 .bak-20261003，WSL 2.4.11 冷启动生效）→拔保活空转 300s×2 连续存活、uptime 25min 连续无回收，空闲自灭根治；期间一窗 2222 端口可达性抖动（VM 实为 Running，mirrored/路径层，自愈，鉴别 SOP 已录）②env 归一 FW_PASS/WIN_PASS 消除 WSL_PASS/别名（备份 env.bak，wsl-sudo→sudo-ok/root/exit0，ssh wsl+win 全通）；触发器节增补进 prep 文档（T1 msdsm 权重/T2 CarsonBurke ckpt/T3 WHmaoxian 裁定→SOP 三步）；技能模板 FIRST_PASS→WIN_PASS 差异呈裁未动缓存 | 评测起跑免保活；遇"连不上"先跑 §三鉴别 SOP 再定性 |
```
