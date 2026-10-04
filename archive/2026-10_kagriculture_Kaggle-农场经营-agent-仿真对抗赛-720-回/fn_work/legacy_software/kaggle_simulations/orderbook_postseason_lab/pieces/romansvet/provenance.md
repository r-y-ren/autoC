# provenance — romansvet（romansvet/kaggriculture）

- **repo URL**: https://github.com/romansvet/kaggriculture
- **commit sha**: `4444cc7a977466a501957ed09cd64951afafa5e7`（HEAD，2026-10-01T21:01:45+03:00 "Replace stale submission/UPLOAD.md with a note on the two final uploads"）
- **抓取时间**: 2026-10-02 12:06Z（git clone --depth 1，GitHub REST 11:0xZ 复核 license=Apache-2.0、pushed=2026-10-01T18:01:48Z）
- **许可**: Apache-2.0（仓内 LICENSE + NOTICE）
- **自报声明**（README.md/submission/UPLOAD.md，抓取 2026-10-02，自报未复核）:
  - "The agent peaked at a rating of 2,858 and finished the submission period at 2,230 (rank 330 of 10,246, provisional until the final evaluation ends)."
  - 终两席=v rp27_vm_m3（Kaggle submission 56718602，2026-09-30 ~20:58 UTC 上传，archive md5 1133b789592a586aaecb9683c56ea3c3，37 文件）+ vrp26_hyb_eve_vrp（56707958）——`submission/` 即 vrp27 解包原样
  - 策略=~7.7k 浮点 ES 网络（OpenAI-ES over bit-exact JAX 复现环境）+ 15.8k 行日规划器 + PPO residual head；"pure numpy plus one small C kernel"
  - 190 负结果 build log（docs/strategy/BUILD-STORY.md，自报）
- **装载形态**: 整包多文件（需适配器=清 kagg3 模块缓存）——`submission/`（37 文件：`main.py` 3,934B 入口 + `kagg3/` 包 + `theta.npy` 30,896B + `residual_head.npz` 59,370B + `engine.lock.json`）。入口=末 callable `agent(observation, configuration=None)`（文件内注释明言 "this must remain the LAST callable defined in the module -- the loader picks the final callable"）。依赖 numpy（前向纯 numpy，逐游戏日内一次）。权重随仓（theta.npy/residual_head.npz）。装载= j23._load_entry(submission/main.py)（loader 自动挂 exec_dir 进 sys.path，`import kagg3` 自解析）；harness 适配层每局前清 `sys.modules` 的 `kagg3*`（对齐官方逐局全新解释器语义，A 件本体零修改）。
- **归档说明**: 本目录=仓库 shallow clone 原样归档（含 .git，1,649 文件，含 src/、docs/ 全谱系与 artifacts/）；判决 harness 只读 `submission/`。
- clone HEAD: 4444cc7a977466a501957ed09cd64951afafa5e7（.git 已按嵌套仓纪律移除，源树全保留）
