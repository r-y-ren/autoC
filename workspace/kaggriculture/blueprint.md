---
campaign:
  competition_id: kaggle-kaggriculture
  name: kagriculture
  theme: Kaggle 农场经营 agent 仿真对抗赛（720 回合供应链博弈，终榜 BT 两两对局史收敛）

scope:
  deliverables:
    - 竞赛在线提交件（自动化 bot；终评活跃对={C_final 重投 56721419, h1x_a 56721643}，发射台账见证据）
    - fn-ladder hybrid 判决轨（判决机 sim_bridge 认证/池测 harness/回放对拍管线/提案 registry 台账与效果闭环）
    - 赛后情报与复盘资产（两轮赛后搜寻、冠军代码解剖、行为指纹库、方法论技能 compete-strategy）
  out_of_scope:
    - 旧树迁移工具收口（fn-refactor 遗留：fn_work/tests/migrate_snapshot_suite 等 12 项测试败/error，随旧树重构处理）
    - 官方终评 BT 定榜对表（约 10-14 出榜，归档后以 archive 复盘跟进）
    - 神经系训练产线（算力不满足；基座路线决策书 baseroute-v2 已评估）

tech_stack:
  - name: 规则式 agent（Python 单文件，kaggle-environments 1.32.7 钉版引擎）
    kb_tech_ids: [kaggle-kaggriculture]
    rationale: KB-2 无对应技术卡；选型依据=引擎源码逐条核验（fn_docs/references/digests/engine-factsheet）+判决机池测实证；赛后基座路线决策书（baseroute-v2）维持规则系+混合系方向
    reuse_cost: 中
  - name: 判决基建（sim_bridge 对拍认证 + 双席折叠池测 + bwrap 沙箱装载）
    kb_tech_ids: [kaggle-kaggriculture]
    rationale: 评测尺与终榜口径对齐（池内稳健 BT 口径教训入册）；支撑 R11-R29 全部单变量 A/B 判决
    reuse_cost: 低

interface_contracts:
  - between: [software, document]
    contract_file: workspace/kagriculture/fn_docs/hybrid/requirements.md

milestones:
  - id: m0-adopt
    task: 基座采纳与合成（V48/ahmed 血统核验、haodou V82 采纳、H1 合成）
    owner_role: software
    depends_on: []
  - id: m1-judge
    task: 判决基建（sim_bridge 认证、池测 harness、回放对拍、读数 SOP）
    owner_role: software
    depends_on: [m0-adopt]
  - id: m2-iterate
    task: 迭代轮 R11-R29 与发射（判决先行、单变量 A/B、在线提交逐发用户裁决）
    owner_role: software
    depends_on: [m1-judge]
  - id: m3-intel
    task: 赛后情报与复盘（开源潮收割、冠军解剖、指纹带分析、方法论技能落档）
    owner_role: document
    depends_on: [m2-iterate]

acceptance:
  checklist:
    - id: sw-registry
      category: software
      item: 提案台账 registry.jsonl 全行 JSON 可解析且效果闭环有终态记录
      method: 自动
      cmd: >-
        python3 -c "import json,glob;R=glob.glob('workspace/kaggr*/fn_docs/hybrid/analyses/registry.jsonl')[0];rows=[json.loads(l) for l in open(R) if l.strip()];assert len(rows)==43;assert any(r.get('status')=='achieved' for r in rows);print('registry ok',len(rows))"
    - id: sw-evidence
      category: software
      item: 判决证据 JSON 全部可解析且非空集（orderbook_*_lab/evidence）
      method: 自动
      cmd: >-
        python3 -c "import json,glob,pathlib;W=glob.glob('workspace/kaggr*/')[0];fs=list(pathlib.Path(W).rglob('evidence/*.json'));assert len(fs)>100;[json.load(open(f)) for f in fs];print('evidence ok',len(fs))"
    - id: sw-test-track
      category: software
      item: 交付面测试全过（排除 out_of_scope 登记的旧树迁移工具套件及 2 项已知工具链败例）
      method: 自动
      cmd: >-
        cd /mnt/data/Code/autoC/$(ls -d workspace/kaggr*/) && python3 -m pytest fn_work/tests --ignore=fn_work/tests/migrate_snapshot_suite --deselect fn_work/tests/shared/test_discover_campaign_roots.py::test_cwd_and_start_path_independence --deselect fn_work/tests/portable_test_baseline/test_regenerate_artifacts_lf.py::test_real_tree_anchor_dual_sha -q
    - id: doc-ledger
      category: document
      item: 分析报告与情报文档落档且 references/INDEX.md 登记
      method: 自动
      cmd: >-
        test -s "$(ls -d workspace/kaggr*/fn_docs/hybrid/analyses/registry.jsonl)" && test -s "$(ls -d workspace/kaggr*/fn_docs/hybrid/references/INDEX.md)" && ls "$(ls -d workspace/kaggr*/fn_docs/hybrid/analyses/)" | grep -q '2026-10' && echo doc-ledger ok
    - id: doc-metrics
      category: document
      item: metrics.json 可解析
      method: 自动
      cmd: >-
        python3 -c "import json,glob;M=glob.glob('workspace/kaggr*/fn_docs/governance/metrics.json')[0];json.load(open(M));print('metrics ok')"

workflow:
  auto_chain: false

compliance:
  ai_policy_reviewed: true
  mode: apply
  policy_basis: KB 条目 kaggle-kaggriculture：竞赛本体即 agent 对抗（提交物=自动化 bot），AI 辅助原创合规；按 AGENTS.md 合规底线保留人机分工记录（发射逐发经用户裁决，见 fn_docs/governance/JOURNAL.md 各发射行）
  notes: 归档前置补蒸馏（战役以 fn-ladder requirements 契约运行，本蓝图为归档器要求的结构化蒸馏）；旧树迁移工具 12 项测试遗留与终评 BT 对表显式出范围，不虚标验收；run-1 失败根因=清单 cmd 手拼路径污染+sw-evidence 空集假过，已修测量链（glob 派生路径+断言非空）非放宽
---
