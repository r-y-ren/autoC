# 远程评测环境预备（remote-eval-prep，2026-10-02）

> 性质：**环境预备记录，非评测本身**。目标：赛后开源潮神经系件评测的运行时供给（P5 侦察缺口=本机无 GPU/torch-jax）。
> 盯防标的：msdsm #1 官方解权重（"supplied separately" 未放）与 CarsonBurke checkpoint（未放）——一旦投放按 §五 SOP 立即评测。
> 纪律执行：远程机（first WSL2）**只装环境、零战役产物**（D14）；venv 隔离不动系统 python；一切留痕只在本报告。
> 时间窗：2026-10-02 19:00–19:25 UTC（远程本地钟 UTC+8 = 2026-10-03 02:56–03:17）。链路：rypc → KVM-Hub headscale → first-prod 100.100.0.6（`ssh wsl`=WSL2 :2222 / `ssh win`=Windows :22）。

## 一、远程机环境事实表（实测）

| 事实 | 值 | 实测方式 |
|---|---|---|
| OS / 内核 | Ubuntu 24.04.5 LTS（noble）/ 5.15.167.4-microsoft-standard-WSL2 | `cat /etc/os-release`、`uname -r` |
| python3 | /usr/bin/python3，3.12.3（系统级**无 pip3**） | `python3 --version`、`which pip3`（空） |
| venv 供给 | 初始 **缺 ensurepip**（无 python3-venv）→ `wsl-sudo apt-get install -y python3-venv` 补齐（python3-venv 3.12.3-0ubuntu2.1 + python3.12-venv 3.12.3-1ubuntu0.17 + python3-pip-whl 24.0+dfsg-1ubuntu1.3） | `import venv, ensurepip` 前后对照 |
| 磁盘 | / 1007G 总 / **954G 可用**（装后占用变化 ≪1%） | `df -h /` |
| 内存 | 31Gi 总（~30Gi 可用）+ 8Gi swap | `free -h` |
| GPU | **NVIDIA GeForce RTX 4070 Laptop GPU**（GPU 0，UUID GPU-0a1b4023-…，P0 35C 16W/140W） | `/usr/lib/wsl/lib/nvidia-smi`（nvidia-smi 不在 PATH） |
| 显存 | **8188MiB**（WSL2 vGPU，跑测时占用 1640MiB 基线） | nvidia-smi Memory-Usage |
| 驱动 / CUDA | NVIDIA-SMI **615.71.08**，KMD 616.92，CUDA UMD **13.4** | nvidia-smi 表头 |
| CUDA 可用性 | `/dev/dxg` 在（crw-rw-rw- 10,127）；`/usr/lib/wsl/lib/libcuda.so{,.1,.1.1}` 在、ldconfig 已收编；nvcc 无（不需要，wheel 自带 runtime） | `ls`、`ldconfig -p` |
| 网络 | download.pytorch.org/whl/cu124..cu130 全 200、pypi.org 200（直连可用，实测下载 ~11 MB/s） | `curl -sI` |

## 二、安装清单与版本

venv：**`~/kag_eval_venv/`**（python3.12.3 / pip 26.2.1 / setuptools 84.0.0 / wheel 0.48.0）。安装链 torch→jax→kaggle-environments 一轮过（`STAGE_CHAIN_EXIT=0`，无 resolver 冲突、无版本覆写）。

| 组件 | 版本 | 来源/备注 |
|---|---|---|
| torch | **2.13.0+cu129**（cuda_build 12.9，triton 3.7.1） | `pip install torch --index-url https://download.pytorch.org/whl/cu129`；cu12x 中取现行最新（cu129 有 cp312 轮子至 2.13.0；GPU SM8.9 对 cu124–cu130 全支持，按任务书钉 cu12x 口径取 cu129） |
| jax | **0.11.2**（jaxlib 0.11.2 + jax-cuda12-plugin/pjrt 0.11.2） | `pip install "jax[cuda12]"` 官方现行装法 |
| kaggle-environments | **1.32.7**（钉死，判决口径同版） | pypi |
| nvidia-cu12 运行时栈 | cudnn 9.20.0.48 / nccl 2.29.7 / cublas 12.9.1.4 / cuda-runtime 12.9.79 / cuda-nvrtc-nvcc-nvjitlink 12.9.86 / cufft 11.4.1.4 / cusolver 11.7.5.82 / cusparse 12.5.10.65 / cusparseLt 0.8.1 / cupti 12.9.79 / cufile 1.14.1.1 / curand 10.3.10.19 / nvshmem 3.4.5 / nvtx 12.9.79 | torch 与 jax 共用一套（jax 侧版本下限被 torch 的 == 钉自动满足，零冲突） |
| 数值栈 | numpy 2.5.3 / scipy 1.18.1 / pandas 3.0.6 / packaging 26.3 | kaggle-environments 依赖树带入 |

完整 freeze 145 行留远程 `~/kag_eval_pip_freeze.txt`（非战役文件）。摘要（关键行）：

```
torch==2.13.0+cu129  triton==3.7.1
jax==0.11.2  jaxlib==0.11.2  jax-cuda12-plugin==0.11.2  jax-cuda12-pjrt==0.11.2
kaggle-environments==1.32.7  numpy==2.5.3  scipy==1.18.1  pandas==3.0.6
nvidia-cudnn-cu12==9.20.0.48  nvidia-nccl-cu12==2.29.7  nvidia-cublas-cu12==12.9.1.4
nvidia-cuda-runtime-cu12==12.9.79  nvidia-cuda-nvrtc-cu12==12.9.86  nvidia-nvjitlink-cu12==12.9.86
```

### nvidia-smi 完整输出（2026-10-02 19:17:44 UTC）

```
Sat Oct  3 03:17:44 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 615.71.08              KMD Version: 616.92        CUDA UMD Version: 13.4     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4070 ...    On  |   00000000:01:00.0 Off |                  N/A |
| N/A   35C    P0             16W /  140W |    1640MiB /   8188MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

## 三、烟测结果（4/4 过）

venv python 直跑，输出原文：

```
=== SMK1 torch CUDA tensor ===
torch 2.13.0+cu129 | cuda_build 12.9 | cudnn 92000
cuda_available True | device_count 1
device_name NVIDIA GeForce RTX 4070 Laptop GPU
matmul_checksum 52336.34765625
mem_alloc_MB 16.1 | mem_reserved_MB 22.0
=== SMK2 jax GPU backend ===
jax 0.11.2 | devices [CudaDevice(id=0)] | default_backend gpu
jax_gpu_sum 56.0
=== SMK3 kaggle-environments ===
kaggle-environments 1.32.7 | import ok
=== SMK4 MLP forward on GPU ===
mlp_out_shape (32, 10) | loss 1.5284367799758911
grad_ok True | cuda_mem_MB 24.3
=== ALL SMK DONE ===
```

| 判据 | 内容 | 判定 |
|---|---|---|
| ① torch CUDA 张量运算 | 1024×1024 matmul on cuda:0，checksum 52336.35，显存读数 16.1/22.0 MB | **过** |
| ② jax GPU 后端 | `jax.devices()=[CudaDevice(id=0)]`，default_backend=gpu | **过** |
| ③ kaggle-environments | 导入成功 + 版本 1.32.7 | **过** |
| ④ MLP 前向 on GPU | Linear(64→128→10) 前向+反向，shape (32,10)，全参数梯度落位，显存 24.3 MB | **过**（推理/训练链路全通） |

## 四、异常与处置记录

1. **WSL VM 空闲自灭（本轮最费时的坑）**：Ubuntu 处于 Stopped；`ssh win 'wsl.exe -d Ubuntu --exec /bin/true'` 拉起后 **~60–90s 无挂载客户端即 VM 整体回收**，连执行中的 ssh 会话都被直接掐断（"closed by remote host"），后续连接超时。处置：以挂载客户端保活——后台常驻 `ssh win 'wsl.exe -d Ubuntu --exec sleep 3600'`（wsl.exe 会话挂在 = VM 不回收），此后 75s+ 静置与全部安装/烟测稳定。**长期建议**：Windows 侧 `.wslconfig` [wsl2] 调大/关闭 `vmIdleTimeout`，或把保活并入 wsl-boot 流（待用户裁决，本轮未改系统配置）。
2. **wsl-sudo 凭据变量名错位**：`~/.config/remote-compute/env` 为 `WSL_PASS/WIN_PASS`，而 wsl-sudo 读 `FW_PASS`（技能权威模板也是 FW_PASS/FIRST_PASS）→ `FW_PASS: 未绑定的变量`。处置：env 文件追加 `FW_PASS=`（值与 WSL_PASS 同源，不落明文于任何日志），命名归一待用户裁决。
3. **python3-venv/ensurepip 系统缺失**：Ubuntu 镜像未带 → `wsl-sudo apt-get install -y python3-venv` 一轮补齐，之后 venv+ensurepip ok。
4. **jax/XLA 初始化 OOM 噪声（不影响功能）**：SMK2 导入时 XLA 预分配探测按 75% 显存尝试 6.00GiB→5.40→4.86→4.37GiB 连报 `CUDA_ERROR_OUT_OF_MEMORY` 后回退小池，随后 GPU 计算全绿。成因=WSL2 vGPU 8GB 且宿主侧有 1640MiB 基线占用，XLA 默认预分配过激。**评测运行建议**：起跑设 `XLA_PYTHON_CLIENT_PREALLOCATE=false`（或 `XLA_PYTHON_CLIENT_MEM_FRACTION=0.25`），torch/jax 同池跑神经件时留 ≥2GB 余量。
5. **torch ≥2.6 `torch.load` 默认 `weights_only=True`**：第三方 checkpoint 装载可能报 UnpicklingError——权重装载 SOP（§五 步 2）已预置对策。
6. **显存上限 8188MiB**：msdsm 12-block 10.23M 参数件、CarsonBurke 级 checkpoint 均远够；大 batch 池测按 8GB 预算取舍。

## 五、权重到位后评测 SOP（三步草案）

盯防标的：**msdsm #1 官方解权重**（supplied separately，未放）与 **CarsonBurke checkpoint**（未放）。任一到位即启动：

1. **传权重**：权重落地源（msdsm 仓 release/另发通道，或 CarsonBurke 仓随附件）→ `scp`/`rsync` 至远程 `~/kag_eval_weights/<target>/`（远程家目录，D14 不入战役树）；先记 **SHA256** 与文件清单再动；本机侧同步留来源 URL+抓取时间戳。
2. **装载**：`~/kag_eval_venv/bin/python` 装载 checkpoint（`torch.load(..., weights_only=True)` 优先；报 UnpicklingError 且信源为官方权重时才降级 `weights_only=False` 并在留痕注明）；架构对表 msdsm-teardown 的 12-block 10.23M 参数表（CarsonBurke 件格式装载时实勘后回填）；先跑 1 局前向 on cuda:0 确认推理链路 + 显存占用读数。
3. **判决机口径跑池测**：kaggle-environments **==1.32.7** 同版钉死（判决口径不动）；面板口径复用 `fn_work/legacy_software/kaggle_simulations/orderbook_postseason_lab/judge_pooltest_arena.py` 同构（674000+i*131 双席折叠、sim_bridge 30/30 认证），远程 GPU 只替换"神经件推理执行位"；产出 h2h 面板与 `2026-10-02-opensrc-pooltest.md` 的 BEATS_CEILING 同尺对照，读数回本机后按铁律 4 经 merge_metrics 落 metrics.json，逐条带局次与时间戳。

## 需登记行

```
| `2026-10-02-remote-eval-prep.md` | 远程实测（ssh wsl/ssh win，2026-10-02 19:00-19:25 UTC）：nvidia-smi/pip freeze/烟测 4 项全输出；pip 源 download.pytorch.org/whl/cu129 + pypi.org；[前次] 2026-10-02-baseroute-recon.md（神经系三墙）、2026-10-02-monitor-baseline.md（msdsm 权重未放基线） | 2026-10-02 | 远程评测环境预备完成：first WSL2（RTX 4070 Laptop 8GB/驱动 615.71.08/CUDA UMD 13.4）venv 隔离装 torch 2.13.0+cu129 + jax 0.11.2 cuda12 + kaggle-environments==1.32.7 一轮零冲突；四项烟测（torch CUDA matmul/jax CudaDevice/kaggle-env 导入/MLP 前向反向）4/4 过；坑=WSL VM 空闲自灭需挂载保活、wsl-sudo FW_PASS 变量名错位（已补别名）、jax XLA 预分配 OOM 噪声（PREALLOCATE=false 可消） | msdsm #1 官方权重/CarsonBurke checkpoint 一旦投放即评测（SOP 三步=传权重→装载→判决机口径跑池测）；.wslconfig vmIdleTimeout 与 env 变量名归一呈裁 |
```
